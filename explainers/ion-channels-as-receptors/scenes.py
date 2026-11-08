"""Ion channels as receptors: the signal opens a hole and the gradient does the rest  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = the signal, the key that opens a gate (transmitter, voltage, heat)
  BLUE   = membrane proteins: the ion channel, the pump, an ordinary receptor
  ORANGE = sodium ions, and E for sodium
  TEAL   = potassium ions, and E for potassium
  PINK   = the push of a difference in concentration (the gradient)
  PURPLE = the membrane voltage: the pull, the scale and its marker
  GOLD   = ATP, the energy a pump spends
  GREEN  = a gate that is open
  RED    = a gate that is shut, and what is ruled out
  GREY   = membrane, labels, the usual route that a channel does not use

No molecular structures: a channel is two blue blocks with a pore between them and two flaps that swing
open; a pump is two blocks around a cup that flips; an ion is a small circle with a plus; the membrane
is a bar; the voltage is a scale computed from the numbers in the lesson (E = -90 mV for potassium,
+60 mV for sodium, rest = -70 mV).

Two stages:
  STAGE A (scenes 1 and 2) the whole membrane across the frame, proteins in the middle.
  STAGE B (scenes 3 to 6)  the channel patch on the left, the voltage scale on the right, the middle
                           column holds the push and pull arrows, then the rule.
"""
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
PINK = "#F08BB4"

MEM_H = 1.2           # membrane thickness
A_PUMP, A_CHAN = -3.3, 3.3      # stage A: x of the pump and of the channel
B_X, B_K = -4.05, 1.1           # stage B: x and size of the channel patch
B_MEM = (-6.3, -1.8)            # stage B membrane extent
AX = 3.5                        # x of the voltage scale
V_REST, V_NA, V_K = -70, 60, -90


# ---------------------------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=24, pad=0.2, **kw):
    """chip with an opaque backing so lines drawn behind it do not show through."""
    c = chip(text, color, size=size, pad=pad, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def ghost_chip(text, size=24, color=GREY):
    t = T(text, size, color)
    box = RoundedRectangle(corner_radius=0.14, width=t.width + 0.4, height=t.height + 0.32)
    back = box.copy().set_stroke(width=0).set_fill(BG, 1)
    return VGroup(back, DashedVMobject(box, num_dashes=max(18, int(box.width * 9))).set_color(color), t)


def strike(m, color=RED):
    return Line(m.get_corner(DL) + [-0.08, -0.04, 0], m.get_corner(UR) + [0.08, 0.04, 0], color=color, stroke_width=7)


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=20)


def pop(m, s=1.3):
    return m.animate(rate_func=there_and_back).scale(s)


def glow(*mobs, s=1.1, color=TEXT):
    return [Indicate(m, color=color, scale_factor=s) for m in mobs]


def clock(center, r=0.45):
    center = np.array(center, float)
    face = Circle(radius=r, stroke_color=GREY, stroke_width=4).move_to(center)
    ticks = VGroup(*[Line(center + (r - 0.11) * v, center + r * v, color=GREY, stroke_width=4) for v in (UP, RIGHT, DOWN, LEFT)])
    hand = Line(center, center + UP * (r - 0.15), color=TEXT, stroke_width=5)
    pin = Dot(center, radius=0.05, color=TEXT)
    g = VGroup(face, ticks, hand, pin)
    g.hand, g.c = hand, center
    return g


def label(text, color=GREY, size=24, weight=NORMAL, back=False):
    t = T(text, size, color, weight=weight)
    if not back:
        return t
    b = Rectangle(width=t.width + 0.16, height=t.height + 0.12, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(t)
    return VGroup(b, t)


# ---------------------------------------------------------------------------------------------
# membrane, ions, channel, pump
# ---------------------------------------------------------------------------------------------
def membrane(x0=-6.3, x1=6.3, y=0.0, h=MEM_H):
    return RoundedRectangle(corner_radius=0.1, width=x1 - x0, height=h, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.35).move_to([(x0 + x1) / 2, y, 0])


def ion(color=ORANGE, r=0.18):
    c = Circle(radius=r, stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.3)
    h = Line([-r * 0.5, 0, 0], [r * 0.5, 0, 0], color=color, stroke_width=3)
    v = Line([0, -r * 0.5, 0], [0, r * 0.5, 0], color=color, stroke_width=3)
    return VGroup(c, h, v)


def fade_ion(p, a):
    p[0].set_stroke(opacity=a).set_fill(opacity=0.3 * a)
    p[1].set_stroke(opacity=a)
    p[2].set_stroke(opacity=a)


def scatter(n, box, seed, avoid=(), gap=0.52, color=ORANGE, r=0.18):
    """n ions at random, well spaced, inside box = (x0, x1, y0, y1), never inside an avoid box."""
    x0, x1, y0, y1 = box
    rng = random.Random(seed)
    pts, tries = [], 0
    while len(pts) < n and tries < 40000:
        tries += 1
        p = (rng.uniform(x0, x1), rng.uniform(y0, y1))
        if any(a0 <= p[0] <= a1 and b0 <= p[1] <= b1 for a0, a1, b0, b1 in avoid):
            continue
        if any((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 < gap ** 2 for q in pts):
            continue
        pts.append(p)
    return VGroup(*[ion(color, r).move_to([x, y, 0]) for x, y in pts])


def flaps(cx, k, a):
    """the gate: one door hinged on the left pore wall. a = 0 shut (red, across the pore), a = 1 open (green, standing along the wall)."""
    pw, ft = 0.8 * k, 0.17 * k
    col = interpolate_color(ManimColor(RED), ManimColor(GREEN), a)
    hinge = np.array([cx - pw / 2, 0.0, 0.0])
    f = RoundedRectangle(corner_radius=ft / 2, width=pw, height=ft, stroke_width=0, fill_color=col, fill_opacity=1)
    f.move_to(hinge + np.array([pw / 2, 0, 0]))
    f.rotate(a * PI / 2, about_point=hinge)
    f.shift(np.array([(ft / 2) * a, 0, 0]))
    return VGroup(f)


def channel(cx, k=1.0, a=0.0, color=BLUE):
    """[pore, left block, right block, flaps]: two blocks with a pore between and a gate across it."""
    pw, bw, hh = 0.8 * k, 0.9 * k, 2.0 * k
    pore = Rectangle(width=pw, height=MEM_H + 0.08, stroke_width=0, fill_color=BG, fill_opacity=1).move_to([cx, 0, 0])

    def block(x):
        back = RoundedRectangle(corner_radius=0.16 * k, width=bw, height=hh, stroke_width=0, fill_color=BG, fill_opacity=1).move_to([x, 0, 0])
        body = RoundedRectangle(corner_radius=0.16 * k, width=bw, height=hh, stroke_color=color, stroke_width=3.5,
                                fill_color=color, fill_opacity=0.4).move_to([x, 0, 0])
        return VGroup(back, body)
    g = VGroup(pore, block(cx - pw / 2 - bw / 2), block(cx + pw / 2 + bw / 2), flaps(cx, k, a))
    g.cx, g.k = cx, k
    return g


def swing(ch, a0, a1, run_time=0.45):
    """open (a0 < a1) or shut the gate of a channel, turning the flaps for real."""
    cx, k = ch.cx, ch.k

    def upd(m, alpha):
        ch[3].become(flaps(cx, k, a0 + (a1 - a0) * alpha))
    return UpdateFromAlphaFunc(ch, upd, run_time=run_time)


def reshape(ch, cx, k, a):
    """move and resize a channel (Transform), remembering where it now is so that swing() still works."""
    tgt = channel(cx, k, a)
    ch.cx, ch.k = cx, k
    return Transform(ch, tgt)


def pump(cx, k=1.0):
    """[cavity, left block, right block]: two blocks around a cavity that holds a cup."""
    cw, bw, hh = 1.05 * k, 0.8 * k, 2.0 * k
    cav = Rectangle(width=cw, height=MEM_H + 0.08, stroke_width=0, fill_color=BG, fill_opacity=1).move_to([cx, 0, 0])

    def block(x):
        back = RoundedRectangle(corner_radius=0.16 * k, width=bw, height=hh, stroke_width=0, fill_color=BG, fill_opacity=1).move_to([x, 0, 0])
        body = RoundedRectangle(corner_radius=0.16 * k, width=bw, height=hh, stroke_color=BLUE, stroke_width=3.5,
                                fill_color=BLUE, fill_opacity=0.4).move_to([x, 0, 0])
        return VGroup(back, body)
    return VGroup(cav, block(cx - cw / 2 - bw / 2), block(cx + cw / 2 + bw / 2))


def cup(cx, up=False):
    """the pump's cup: a ring with a gap, open to the inside (down) or to the outside (up)."""
    a = Arc(radius=0.36, start_angle=-60 * DEGREES, angle=300 * DEGREES, color=BLUE, stroke_width=9).move_to([cx, 0, 0])
    if up:
        a.rotate(PI, about_point=np.array([cx, 0, 0]))
    return a


def flow(ions, xs, y_a, y_b):
    """animations that carry each ion from y_a to y_b along its own lane, fading in and out at the ends."""
    out = []
    for p, x in zip(ions, xs):
        pa, pb = np.array([x, y_a, 0.0]), np.array([x, y_b, 0.0])

        def upd(m, alpha, pa=pa, pb=pb):
            m.move_to(pa + (pb - pa) * alpha)
            fade_ion(m, max(0.0, min(1.0, alpha / 0.1, (1 - alpha) / 0.1)))
        fade_ion(p, 0.0)
        p.move_to(pa)
        out.append(UpdateFromAlphaFunc(p, upd, rate_func=linear))
    return out


def stream(color, x, y_a, y_b, n=6, lanes=None, r=0.18):
    """n ions, one after another, down (or up) one lane. Returns (ions, animations to run in a LaggedStart)."""
    ions = [ion(color, r) for _ in range(n)]
    xs = [x + (lanes[i % len(lanes)] if lanes else 0.0) for i in range(n)]
    return ions, flow(ions, xs, y_a, y_b)


# ---------------------------------------------------------------------------------------------
# the voltage scale (stage B)
# ---------------------------------------------------------------------------------------------
def vy(v):
    """height of a voltage on the scale: -95 mV at the bottom, +65 mV at the top."""
    return -3.0 + (v + 95) * 6.0 / 160.0


def mv(v):
    return f"{'+' if v > 0 else '−'}{abs(v)} mV"


def axis():
    line = Line([AX, vy(-95), 0], [AX, vy(65), 0], color=GREY, stroke_width=4)
    zero = Line([AX - 0.14, vy(0), 0], [AX + 0.14, vy(0), 0], color=GREY, stroke_width=3)
    zl = M("0 mV", 22, GREY).next_to(zero, RIGHT, buff=0.12)
    ttl = T("membrane voltage", 24, PURPLE, weight=BOLD).move_to([AX + 0.1, 3.3, 0])
    return VGroup(line, zero, zl, ttl)


def etag(name, v, color):
    """E for one ion: a tick on the scale and its name and value to the right. [tick, name, value]"""
    tick = Line([AX - 0.2, vy(v), 0], [AX + 0.2, vy(v), 0], color=color, stroke_width=6)
    t1 = T(f"E {name}", 24, color, weight=BOLD)
    t2 = M(mv(v), 22, color)
    VGroup(t1, t2).arrange(DOWN, aligned_edge=LEFT, buff=0.06).next_to(tick, RIGHT, buff=0.15)
    g = VGroup(tick, t1, t2)
    g.tick, g.t1, g.t2 = tick, t1, t2
    return g


def marker(v):
    y = vy(v)
    tri = Polygon([AX - 0.1, y, 0], [AX - 0.5, y + 0.2, 0], [AX - 0.5, y - 0.2, 0], fill_color=PURPLE, fill_opacity=1, stroke_width=0)
    tick = Line([AX - 0.12, y, 0], [AX + 0.12, y, 0], color=PURPLE, stroke_width=5)
    return VGroup(tri, tick)


def mlabel(v, text=None):
    t = M(text or mv(v), 24, PURPLE, weight=BOLD)
    return t.next_to([AX + 0.2, vy(v), 0], RIGHT, buff=0.12)


def drag(v_from, e_val, color, w=7):
    """an arrow along the scale from the marker toward an E."""
    return Arrow([AX - 0.78, vy(v_from), 0], [AX - 0.78, vy(e_val), 0], buff=0, color=color, stroke_width=w, tip_length=0.24,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=20)


# push and pull panel (stage B, scene 3)
PUSH_X, PULL_X, ION_X, Y0 = -0.2, 1.4, 0.6, 0.0
PUSH_L, SC = 1.8, 0.03


def pull_arrow(v):
    d = -v * SC       # downward length; negative means the pull points up
    vis = abs(d) >= 0.14
    a = Arrow([PULL_X, Y0, 0], [PULL_X, Y0 - (d if vis else 0.14), 0], buff=0, color=PURPLE, stroke_width=9, tip_length=0.3,
              max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=30)
    if not vis:
        a.set_stroke(opacity=0).set_fill(opacity=0)
    return a


def push_arrow():
    return Arrow([PUSH_X, Y0, 0], [PUSH_X, Y0 - PUSH_L, 0], buff=0, color=PINK, stroke_width=9, tip_length=0.3,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=30)


# ---------------------------------------------------------------------------------------------
# stage B populations
# ---------------------------------------------------------------------------------------------
B_AVOID = [(B_X - 0.9, B_X + 0.9, -3.6, 3.6)]
B_OUT, B_IN = (-6.1, -2.0, 1.62, 2.78), (-6.1, -2.0, -2.78, -1.62)


def crowd_b(kind):
    """kind 'na': many sodium ions outside, few inside.  kind 'k': many potassium ions inside, few outside."""
    if kind == "na":
        g = VGroup(scatter(9, B_OUT, 21, B_AVOID, color=ORANGE), scatter(2, B_IN, 22, B_AVOID, color=ORANGE))
    else:
        g = VGroup(scatter(2, B_OUT, 23, B_AVOID, color=TEAL), scatter(9, B_IN, 24, B_AVOID, color=TEAL))
    return g


def strips():
    """pink bands behind the outside and inside crowds: the difference in concentration."""
    o = RoundedRectangle(corner_radius=0.15, width=4.5, height=1.64, stroke_color=PINK, stroke_width=2.5, fill_color=PINK, fill_opacity=0.1).move_to([-4.05, 2.2, 0])
    i = RoundedRectangle(corner_radius=0.15, width=4.5, height=1.64, stroke_color=PINK, stroke_width=2.5, fill_color=PINK, fill_opacity=0.1).move_to([-4.05, -2.2, 0])
    return VGroup(o, i)


def side_labels():
    o = T("outside", 22, GREY).move_to([-1.2, 0.95, 0])
    i = T("inside", 22, GREY).move_to([-1.2, -0.95, 0])
    return VGroup(o, i)


def ch_name(kind):
    return T("sodium channel" if kind == "na" else "potassium channel", 26, ORANGE if kind == "na" else TEAL, weight=BOLD).move_to([B_X, 3.28, 0])


# ---------------------------------------------------------------------------------------------
class Film(SpokenScene):
    def room(self, phrase, nth=0, lead=0.2):
        """seconds left before the narrator says `phrase` (so a long animation can be cut to fit)."""
        return max(0.3, self.t_of(phrase, nth) - lead - self.elapsed())

    def outro(self, *anims, then=None, after=None, run_time=0.38):
        """hold until the narration ends, clear what the next scene does not inherit, then (optionally)
        change layout (`then`, and `after` once that has settled)."""
        rest = self.narration_s - 0.02 - self.elapsed()
        if rest > 0:
            self.wait(rest)
        if anims:
            self.play(*anims, run_time=run_time)
        if then:
            self.play(*then, run_time=0.9)
        if after:
            self.play(*after, run_time=0.45)
        if then or after:
            self.wait(0.15)
        self.finish()


class S00Title(TitleCard):
    LESSON = "Ion Channels as Receptors"
    TITLE = "The signal opens a hole"


# ---------------------------------------------------------------------------------------------
class S01Hole(Film):
    """A channel hands the signal to nothing: it opens a hole, ions pour through. Which way? (STAGE A)"""

    def construct(self):
        mem = membrane()
        self.play(FadeIn(mem), run_time=0.4)
        sig = bchip("signal", YELLOW, 26).move_to([0, 1.3, 0])
        self.play(FadeIn(sig, shift=DOWN * 0.3), run_time=0.5)

        # the question, posed in the picture: an unknown answer inside the cell
        qbox = ghost_chip("?", 60)
        qbox[2].set_color(TEXT)
        qbox.move_to([0, -1.9, 0])
        self.at("answer a signal")
        self.play(FadeIn(qbox, scale=0.8), run_time=0.5)
        ck = clock([1.9, 2.6, 0])
        ms = T("about a millisecond", 26, GREY).next_to(ck, RIGHT, buff=0.25)
        self.at("in about a")
        self.play(FadeIn(ck), FadeIn(ms), run_time=0.3)
        self.play(Rotate(ck.hand, -TAU / 4, about_point=ck.c), run_time=0.6)

        # the usual route: receptor, G protein, kinase
        rec = RoundedRectangle(corner_radius=0.2, width=0.55, height=2.0, stroke_color=BLUE, stroke_width=3.5, fill_color=BLUE, fill_opacity=0.4).move_to([-3.3, 0, 0])
        rec_back = RoundedRectangle(corner_radius=0.2, width=0.55, height=2.0, stroke_width=0, fill_color=BG, fill_opacity=1).move_to([-3.3, 0, 0])
        rec_g = VGroup(rec_back, rec)
        rec_l = T("receptor", 26, BLUE).move_to([-3.3, 2.35, 0])
        self.at("Most receptors")
        self.play(FadeOut(qbox), FadeOut(ck), FadeOut(ms), FadeIn(rec_g), FadeIn(rec_l), sig.animate.move_to([-3.3, 1.55, 0]), run_time=0.8)
        gp = bchip("G protein", GREY, 24).move_to([-3.3, -1.75, 0])
        ka = bchip("kinase", GREY, 24).move_to([-3.3, -2.95, 0])
        a1 = arr([-3.3, -1.0, 0], gp.get_top(), GREY)
        a2 = arr(gp.get_bottom(), ka.get_top(), GREY)
        self.at("such as")
        self.play(GrowArrow(a1), FadeIn(gp, shift=DOWN * 0.15), run_time=0.5)
        self.at("or a")
        self.play(GrowArrow(a2), FadeIn(ka, shift=DOWN * 0.15), run_time=0.5)

        # the channel hands it to nothing
        ch = channel(A_CHAN, 1.0, 0.0)
        sig2 = bchip("signal", YELLOW, 26).move_to([A_CHAN, 1.55, 0])
        chl = T("ion channel", 26, BLUE).move_to([A_CHAN, 2.35, 0])
        self.at("channel hands")
        self.play(FadeIn(ch), FadeIn(sig2, shift=DOWN * 0.2), FadeIn(chl), run_time=0.7)
        nothing = ghost_chip("nothing", 26)
        nothing.move_to([A_CHAN, -1.85, 0])
        self.at("to nothing")
        self.play(FadeIn(nothing, shift=UP * 0.1), run_time=0.5)

        # the signal opens a hole: the channel comes to the middle and grows
        self.at("The signal opens")
        self.play(FadeOut(VGroup(rec_g, rec_l, gp, ka, a1, a2, sig, nothing, chl)),
                  reshape(ch, 0, 1.7, 0.0), sig2.animate.move_to([0, 2.7, 0]), run_time=0.9)
        self.play(swing(ch, 0, 1, 0.5))

        # ions pour through, in both directions: nobody has said which way yet
        down, da = stream(ORANGE, 0, 2.05, -2.05, n=6, lanes=[0.0])
        up, ua = stream(ORANGE, 0, -2.05, 2.05, n=6, lanes=[0.42])
        self.add(*down, *up)
        self.at("pour through")
        self.play(LaggedStart(*[a for pr in zip(da, ua) for a in pr], lag_ratio=0.1), run_time=min(2.6, self.room("the voltage across")))

        # the voltage across the membrane
        vb = DoubleArrow([-2.65, 0.6, 0], [-2.65, -0.6, 0], buff=0, color=PURPLE, stroke_width=6, tip_length=0.22)
        vl = T("voltage", 28, PURPLE, weight=BOLD).next_to(vb, LEFT, buff=0.25)
        self.at("the voltage across")
        self.play(GrowFromCenter(vb), FadeIn(vl), run_time=0.6)
        self.play(*glow(vb, s=1.12, color=PURPLE), run_time=0.5)

        big = VGroup(T("about ten million ions", 28, ORANGE), T("every second", 28, ORANGE)).arrange(DOWN, buff=0.12, aligned_edge=LEFT).move_to([-4.3, 2.55, 0])
        d2, d2a = stream(ORANGE, 0, 2.05, -2.05, n=8, lanes=[0.0])
        u2, u2a = stream(ORANGE, 0, -2.05, 2.05, n=8, lanes=[0.42])
        self.add(*d2, *u2)
        self.at("One open")
        wait_label = max(0.1, self.t_of("million ions") - 0.2 - self.elapsed())
        self.play(LaggedStart(*[a for pr in zip(d2a, u2a) for a in pr], lag_ratio=0.1),
                  Succession(Wait(wait_label), FadeIn(big, shift=RIGHT * 0.1, run_time=0.5)),
                  run_time=min(6.0, self.room("which way")))

        # which way?
        wy = DoubleArrow([2.65, -2.1, 0], [2.65, 2.1, 0], buff=0, color=GREY, stroke_width=7, tip_length=0.3)
        qq = T("?", 64, TEXT, weight=BOLD).move_to([3.4, 0, 0])
        self.at("which way")
        self.play(GrowFromCenter(wy), FadeIn(qq, scale=0.6), run_time=0.7)
        self.play(pop(qq, 1.25), run_time=0.6)
        # leave the channel closed and small, at the right, for the next scene
        self.outro(FadeOut(VGroup(vb, vl, big, wy, qq, sig2)),
                   then=[reshape(ch, A_CHAN, 1.0, 1.0)])


# ---------------------------------------------------------------------------------------------
def crowd_a(seed=31):
    avoid_p = [(A_PUMP - 1.3, A_PUMP + 1.3, -3.6, 3.6)]
    avoid_c = [(A_CHAN - 1.3, A_CHAN + 1.3, -3.6, 3.6)]
    lab = [(-6.3, -4.7, -1.3, 1.3), (A_PUMP - 1.6, A_PUMP + 1.6, -2.7, -1.7), (A_CHAN - 1.6, A_CHAN + 1.6, -2.7, -1.7)]
    av = avoid_p + avoid_c + lab
    out = scatter(24, (-5.9, 5.9, 1.55, 3.0), seed, av)
    inn = scatter(4, (-5.9, 5.9, -3.0, -1.55), seed + 1, av)
    return VGroup(out, inn)


class S02Gate(Film):
    """Two kinds of protein: a pump carries ions uphill, slowly; a channel lets them run downhill, fast. (STAGE A)"""

    def construct(self):
        mem = membrane()
        ch = channel(A_CHAN, 1.0, 1.0)
        # the gate was left open by scene 1; shut it so the keys can open it
        self.add(mem, ch)
        pm = pump(A_PUMP)
        ring = cup(A_PUMP)
        crowd = crowd_a()
        out_l, in_l = T("outside", 22, GREY).move_to([-5.45, 0.95, 0]), T("inside", 22, GREY).move_to([-5.45, -0.95, 0])
        self.at("Two kinds of")
        self.play(FadeIn(pm), FadeIn(ring), FadeIn(out_l), FadeIn(in_l), swing(ch, 1, 0, 0.6), run_time=0.7)
        self.at("move ions across")
        self.play(LaggedStart(*[FadeIn(i, scale=0.6) for i in list(crowd[0]) + list(crowd[1])], lag_ratio=0.03), run_time=1.0)

        # the pump
        pl = T("pump", 26, BLUE, weight=BOLD).move_to([A_PUMP - 1.95, 0, 0])
        pl_b = VGroup(Rectangle(width=pl.width + 0.16, height=pl.height + 0.12, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(pl), pl)
        carried = ion(ORANGE).move_to([A_PUMP, -1.95, 0])
        self.at("A pump binds")
        self.play(FadeIn(pl_b), FadeIn(carried, scale=0.6), run_time=0.4)
        self.play(carried.animate.move_to([A_PUMP, 0, 0]), run_time=0.7)
        unit = VGroup(ring, carried)
        self.at("changes shape to")
        self.play(Rotate(unit, PI, about_point=np.array([A_PUMP, 0, 0])), run_time=1.0)
        up_l = T("uphill", 24, GREY).move_to([A_PUMP - 0.6, 2.2, 0])
        self.at("uphill")
        self.play(carried.animate.move_to([A_PUMP, 1.9, 0]), FadeIn(up_l), run_time=0.8)
        atp = bchip("ATP", GOLD, 24).move_to([A_PUMP + 1.95, 0, 0])
        self.at("if it spends")
        self.play(FadeIn(atp, scale=0.8), run_time=0.4)
        self.play(atp.animate.move_to([A_PUMP + 1.0, 0.0, 0]).scale(0.5).set_opacity(0), run_time=0.6)

        # the channel
        cl = T("channel", 26, BLUE, weight=BOLD).move_to([A_CHAN + 1.95, 0, 0])
        cl_b = VGroup(Rectangle(width=cl.width + 0.16, height=cl.height + 0.12, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(cl), cl)
        self.at("A channel is")
        self.play(FadeOut(up_l), FadeIn(cl_b), run_time=0.4)
        self.at("with a gate")
        self.play(*glow(ch[3][0], s=1.5, color=TEXT), run_time=0.6)

        # three keys, one after another
        key = bchip("transmitter", YELLOW, 22).move_to([A_CHAN, 3.1, 0])
        self.at("which a transmitter")
        self.play(FadeIn(key), run_time=0.2)
        self.play(key.animate.move_to([A_CHAN, 1.65, 0]), run_time=0.5)
        self.play(swing(ch, 0, 1, 0.3))
        k2 = bchip("voltage", YELLOW, 22).move_to([A_CHAN, 1.65, 0])
        self.at("a voltage")
        self.play(swing(ch, 1, 0, 0.2), run_time=0.2)
        self.play(ReplacementTransform(key, k2), run_time=0.3)
        self.play(swing(ch, 0, 1, 0.3))
        k3 = bchip("heat", YELLOW, 22).move_to([A_CHAN, 1.65, 0])
        self.at("or heat")
        self.play(swing(ch, 1, 0, 0.2), run_time=0.2)
        self.play(ReplacementTransform(k2, k3), run_time=0.3)
        self.play(swing(ch, 0, 1, 0.3))

        # open: ions run downhill
        down_l = T("downhill", 24, GREY).move_to([A_CHAN - 0.6, 2.2, 0])
        self.at("Once it is open")
        self.play(FadeOut(k3), run_time=0.3)
        ions, anims = stream(ORANGE, A_CHAN + 0.08, 1.9, -1.9, n=8)
        self.add(*ions)
        self.at("run downhill")
        self.play(FadeIn(down_l), LaggedStart(*anims, lag_ratio=0.16), run_time=min(2.2, self.room("at around")))
        ten = T("around ten million a second", 24, ORANGE).move_to([A_CHAN, -2.15, 0])
        self.at("at around")
        ions2, anims2 = stream(ORANGE, A_CHAN + 0.08, 1.9, -1.9, n=8)
        self.add(*ions2)
        self.play(FadeIn(ten), LaggedStart(*anims2, lag_ratio=0.16), run_time=min(2.0, self.room("while a pump")))

        # the pump is slow
        few = T("a few hundred", 24, BLUE).move_to([A_PUMP, -2.15, 0])
        self.at("while a pump")
        self.play(Rotate(ring, PI, about_point=np.array([A_PUMP, 0, 0])), run_time=1.3)
        self.at("a few hundred")
        self.play(FadeIn(few), run_time=0.4)
        # gradients: pink bands behind the crowds
        st = VGroup(
            RoundedRectangle(corner_radius=0.15, width=12.4, height=1.9, stroke_color=PINK, stroke_width=2.5, fill_color=PINK, fill_opacity=0.08).move_to([0, 2.25, 0]),
            RoundedRectangle(corner_radius=0.15, width=12.4, height=1.9, stroke_color=PINK, stroke_width=2.5, fill_color=PINK, fill_opacity=0.08).move_to([0, -2.25, 0]))
        gl = T("gradient", 26, PINK, weight=BOLD).move_to([-5.2, 0, 0])
        self.at("build")
        self.play(FadeIn(st), run_time=0.6)
        ions3, anims3 = stream(ORANGE, A_CHAN + 0.08, 1.9, -1.9, n=8)
        self.add(*ions3)
        self.at("channels spend them")
        self.play(LaggedStart(*anims3, lag_ratio=0.16), run_time=1.8)
        # leave the channel for scene 3: the patch of membrane goes left and shrinks; the crowd is rebuilt there
        crowd_b_na = crowd_b("na")
        mem_b = membrane(*B_MEM)
        self.outro(FadeOut(VGroup(pm, ring, carried, pl_b, cl_b, out_l, in_l, ten, few, down_l, crowd, st)),
                   then=[Transform(mem, mem_b), reshape(ch, B_X, B_K, 1.0)],
                   after=[FadeIn(crowd_b_na), FadeIn(side_labels())])


# ---------------------------------------------------------------------------------------------
def equation():
    eq1 = T("driving force", 26, TEXT, weight=BOLD)
    eq2 = VGroup(T("=", 24, TEXT), T("membrane voltage", 24, PURPLE), T("\u2212", 24, TEXT), T("E", 24, TEXT)).arrange(RIGHT, buff=0.12)
    eq = VGroup(eq1, eq2).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
    eq.move_to([0.45, 2.45, 0])
    return eq, eq1, eq2


def scene_b_state(kind="na"):
    mem = membrane(*B_MEM)
    ch = channel(B_X, B_K, 1.0)
    crowd = crowd_b(kind)
    sides = side_labels()
    nm = ch_name(kind)
    ax = axis()
    tag_na, tag_k = etag("sodium", V_NA, ORANGE), etag("potassium", V_K, TEAL)
    return mem, ch, crowd, sides, nm, ax, tag_na, tag_k


class S03Pushpull(Film):
    """The push of the gradient and the pull of the voltage on one sodium ion; slide the voltage to the E where they balance. (STAGE B)"""

    def construct(self):
        mem = membrane(*B_MEM)
        ch = channel(B_X, B_K, 1.0)
        crowd = crowd_b("na")
        sides = side_labels()
        self.add(mem, ch, crowd, sides)

        vt = ValueTracker(V_REST)
        base = DashedLine([PUSH_X, Y0, 0], [PULL_X, Y0, 0], color=GREY, stroke_width=3, dash_length=0.1)
        panel_ion = ion(ORANGE, 0.26).move_to([ION_X, Y0, 0])
        push = push_arrow()
        pull = always_redraw(lambda: pull_arrow(vt.get_value()))
        push_l = T("push", 30, PINK, weight=BOLD).next_to([PUSH_X, Y0, 0], LEFT, buff=0.2)
        pull_l = T("pull", 30, PURPLE, weight=BOLD).next_to([PULL_X, Y0, 0], RIGHT, buff=0.2)

        self.at("Downhill has two")
        ions, anims = stream(ORANGE, B_X + 0.08, 1.5, -1.5, n=5)
        self.add(*ions)
        self.play(FadeIn(base), FadeIn(panel_ion), LaggedStart(*anims, lag_ratio=0.18), run_time=min(1.8, self.room("push from")))
        self.at("push from")
        self.play(GrowArrow(push), FadeIn(push_l), run_time=0.6)
        sts = strips()
        self.at("difference in")
        self.play(FadeIn(sts), run_time=0.5)
        self.at("and a pull")
        self.add(pull)
        self.play(FadeIn(pull_l), FadeOut(sts), run_time=0.6)
        # the scale and the minus signs: the voltage across the membrane
        ax = axis()
        minus = VGroup(*[Line([x - 0.12, -1.0, 0], [x + 0.12, -1.0, 0], color=PURPLE, stroke_width=6) for x in (-6.05, -5.75, -2.35, -2.05)])
        self.at("the voltage across")
        self.play(FadeIn(ax), FadeIn(minus), run_time=0.6)

        # sodium
        nm = ch_name("na")
        self.at("Take sodium")
        self.play(FadeIn(nm, shift=DOWN * 0.1), *glow(*crowd[0], s=1.2, color=ORANGE), run_time=0.8)
        self.at("mostly outside")
        self.play(*glow(*crowd[0], s=1.25, color=TEXT), run_time=0.7)

        # rest
        mk = always_redraw(lambda: marker(vt.get_value()))
        ml = mlabel(V_REST)
        self.at("resting neuron")
        self.add(mk)
        self.play(FadeIn(ml), FadeIn(mk), run_time=0.5)
        self.play(*glow(ml, s=1.2, color=TEXT), run_time=0.6)

        # slide the voltage until push and pull balance
        self.at("For each ion")
        self.play(FadeOut(ml), FadeOut(minus), run_time=0.4)
        self.at("one voltage")
        self.play(vt.animate.set_value(V_NA), run_time=min(2.6, self.room("push and pull balance")))
        bal = T("balance", 30, TEXT, weight=BOLD).move_to([(PUSH_X + PULL_X) / 2, Y0 + 2.45, 0])
        self.at("push and pull balance")
        self.play(FadeIn(bal, shift=DOWN * 0.1), pop(push, 1.1), run_time=0.6)

        # E
        tag = etag("sodium", V_NA, ORANGE)
        self.at("equilibrium potential")
        self.play(FadeIn(tag.tick), FadeIn(tag.t1), run_time=0.5)
        self.at("for sodium it is")
        self.play(FadeIn(tag.t2, shift=LEFT * 0.1), run_time=0.5)
        self.play(*glow(tag.t1, tag.t2, s=1.12), run_time=0.6)

        # back to rest for the next scene
        self.outro(FadeOut(VGroup(base, panel_ion, push, push_l, pull_l, bal)), FadeOut(pull),
                   then=[vt.animate.set_value(V_REST)], after=[FadeIn(mlabel(V_REST))])


# ---------------------------------------------------------------------------------------------
class S04Drag(Film):
    """E for potassium; an open channel drags the voltage toward the E of the ion it passes; one subtraction. (STAGE B)"""

    def construct(self):
        mem, ch, na, sides, nm, ax, tag_na, tag_k = scene_b_state("na")
        vt = ValueTracker(V_REST)
        mk = always_redraw(lambda: marker(vt.get_value()))
        ml = mlabel(V_REST)
        self.add(mem, ch, na, sides, nm, ax, tag_na.tick, tag_na.t1, tag_na.t2, mk, ml)

        # potassium lives inside
        k = crowd_b("k")
        nk = ch_name("k")
        self.at("keeps potassium mostly")
        self.play(FadeOut(na), FadeOut(nm), FadeIn(k), FadeIn(nk), run_time=0.8)
        self.at("for potassium")
        self.play(FadeIn(tag_k.tick), FadeIn(tag_k.t1), run_time=0.5)
        self.at("is about")
        self.play(FadeIn(tag_k.t2, shift=LEFT * 0.1), run_time=0.5)

        # an open channel drags the voltage toward the E of the ion it passes
        ions, anims = stream(TEAL, B_X + 0.08, -1.5, 1.5, n=3)
        self.add(*ions)
        d_k = drag(V_REST, V_K, TEAL)
        self.at("An open channel drags")
        self.play(FadeOut(ml), GrowArrow(d_k), LaggedStart(*anims, lag_ratio=0.3), run_time=1.4)
        self.play(vt.animate.set_value(-79), Transform(d_k, drag(-79, V_K, TEAL)), run_time=0.8)
        self.at("toward the")
        d_na = drag(V_REST, V_NA, ORANGE)
        self.play(FadeOut(d_k), vt.animate.set_value(V_REST), FadeOut(k), FadeOut(nk), FadeIn(na), FadeIn(nm), run_time=0.8)
        ions2, anims2 = stream(ORANGE, B_X + 0.08, 1.5, -1.5, n=6)
        self.add(*ions2)
        self.play(GrowArrow(d_na), LaggedStart(*anims2, lag_ratio=0.2), run_time=1.4)
        self.play(vt.animate.set_value(-52), Transform(d_na, drag(-52, V_NA, ORANGE)), run_time=0.8)

        # one subtraction
        d_k2 = drag(V_REST, V_K, TEAL)
        self.at("one subtraction")
        self.play(vt.animate.set_value(V_REST), Transform(d_na, drag(V_REST, V_NA, ORANGE)), FadeIn(d_k2), run_time=0.9)
        self.play(*glow(d_na, d_k2, s=1.15, color=TEXT), run_time=0.7)
        eq, eq1, eq2 = equation()
        self.at("The driving force")
        self.play(FadeIn(eq1, shift=DOWN * 0.1), run_time=0.5)
        self.at("is the membrane")
        self.play(FadeIn(eq2[0]), FadeIn(eq2[1]), run_time=0.5)
        self.at("voltage minus")
        self.play(FadeIn(eq2[2]), FadeIn(eq2[3]), *glow(tag_na.t1, tag_k.t1, s=1.1), run_time=0.6)
        self.outro(FadeOut(d_k2), FadeOut(d_na), FadeIn(mlabel(V_REST)))


# ---------------------------------------------------------------------------------------------
class S05Numbers(Film):
    """At rest sodium is 130 mV from its E and rushes in; potassium is 20 mV from its E and leaks out. (STAGE B)"""

    def construct(self):
        mem, ch, na, sides, nm, ax, tag_na, tag_k = scene_b_state("na")
        eq, eq1, eq2 = equation()
        vt = ValueTracker(V_REST)
        mk = always_redraw(lambda: marker(vt.get_value()))
        ml = mlabel(V_REST)
        self.add(mem, ch, na, sides, nm, ax, tag_na, tag_k, mk, ml, eq)

        # sodium: 130 mV
        d_na = drag(V_REST, V_NA, ORANGE)
        n130 = T("130 mV", 34, ORANGE, weight=BOLD).next_to(d_na, LEFT, buff=0.2)
        self.play(*glow(ml, s=1.2, color=TEXT), run_time=0.6)
        self.at("sodium is")
        self.play(GrowArrow(d_na), FadeIn(n130), run_time=0.8)
        self.at("away from its")
        self.play(*glow(tag_na.t1, tag_na.t2, s=1.15), run_time=0.6)
        ions, anims = stream(ORANGE, B_X + 0.08, 1.5, -1.5, n=5)
        ions_b, anims_b = stream(ORANGE, B_X + 0.08, 1.5, -1.5, n=7)
        self.add(*ions, *ions_b)
        self.at("So it rushes in")
        self.play(FadeOut(d_na), FadeOut(n130), FadeOut(ml), LaggedStart(*anims, lag_ratio=0.2), run_time=min(1.6, self.room("the cell")))
        less = T("less negative", 24, PURPLE)
        self.at("the cell")
        self.play(LaggedStart(*anims_b, lag_ratio=0.2), vt.animate.set_value(-35), run_time=min(2.4, self.room("becomes less negative")))
        self.at("becomes less negative")
        less.next_to([AX + 0.2, vy(-35), 0], RIGHT, buff=0.15)
        self.play(FadeIn(less, shift=LEFT * 0.1), run_time=0.5)

        # potassium: 20 mV
        k = crowd_b("k")
        nk = ch_name("k")
        d_k = drag(V_REST, V_K, TEAL)
        n20 = T("20 mV", 34, TEAL, weight=BOLD).next_to(d_k, LEFT, buff=0.2)
        self.at("Potassium is only")
        self.play(FadeOut(less), vt.animate.set_value(V_REST), FadeOut(na), FadeOut(nm), FadeIn(k), FadeIn(nk), run_time=1.0)
        self.play(GrowArrow(d_k), FadeIn(n20), run_time=0.6)
        self.at("from its", nth=1)
        self.play(*glow(tag_k.t1, tag_k.t2, s=1.15), run_time=0.6)
        ions2, anims2 = stream(TEAL, B_X + 0.08, -1.5, 1.5, n=2)
        ions3, anims3 = stream(TEAL, B_X + 0.08, -1.5, 1.5, n=2)
        self.add(*ions2, *ions3)
        self.at("leaks out gently")
        self.play(FadeOut(d_k), FadeOut(n20), LaggedStart(*anims2, lag_ratio=0.5), run_time=min(2.0, self.room("pulls the voltage")))
        self.at("pulls the voltage")
        self.play(LaggedStart(*anims3, lag_ratio=0.5), vt.animate.set_value(-80), run_time=1.6)
        self.outro(FadeOut(k), FadeOut(nk), then=[vt.animate.set_value(V_REST)], after=[FadeIn(na), FadeIn(nm), FadeIn(mlabel(V_REST))])


# ---------------------------------------------------------------------------------------------
class S06Rule(Film):
    """Few ions change the voltage, the crowds stay the same; the signal opens the hole and the gradient does the rest. (STAGE B)"""

    def construct(self):
        mem, ch, na, sides, nm, ax, tag_na, tag_k = scene_b_state("na")
        eq, eq1, eq2 = equation()
        vt = ValueTracker(V_REST)
        mk = always_redraw(lambda: marker(vt.get_value()))
        ml = mlabel(V_REST)
        self.add(mem, ch, na, sides, nm, ax, tag_na, tag_k, mk, ml, eq)

        # a few ions are enough to move the voltage a long way
        ions, anims = stream(ORANGE, B_X + 0.08, 1.5, -1.5, n=3)
        self.add(*ions)
        self.at("Very few ions")
        self.play(FadeOut(ml), LaggedStart(*anims, lag_ratio=0.35), vt.animate.set_value(-40), run_time=min(2.4, self.room("the concentrations barely")))
        sts = strips()
        barely = T("barely shifts", 30, PINK, weight=BOLD).move_to([0.45, 0.1, 0])
        self.at("the concentrations barely")
        self.play(FadeIn(sts), FadeIn(barely), run_time=0.6)
        made = ghost_chip("new molecules", 26)
        made.move_to([0.45, -1.9, 0])
        cross = strike(made)
        self.at("nothing has to")
        self.play(FadeIn(made), run_time=0.4)
        self.play(Create(cross), run_time=0.4)
        msg = T("the message", 30, PURPLE, weight=BOLD).next_to([AX + 0.2, vy(-40), 0], RIGHT, buff=0.15)
        self.at("The voltage is the")
        self.play(FadeOut(sts), FadeOut(barely), FadeOut(made), FadeOut(cross), FadeIn(msg, shift=LEFT * 0.1),
                  *glow(mk, s=1.5, color=PURPLE), run_time=0.8)

        # the rule: shut the gate, then let the signal open it
        self.at("So keep this rule")
        self.play(FadeOut(msg), FadeOut(eq), vt.animate.set_value(V_REST), swing(ch, 1, 0, 0.6), run_time=0.8)
        sig = bchip("signal", YELLOW, 26).move_to([B_X, 3.05, 0])
        self.play(FadeIn(sig), run_time=0.2)
        self.play(sig.animate.move_to([B_X, 1.55, 0]), run_time=0.5)
        self.at("the signal opens a")
        self.play(swing(ch, 0, 1, 0.5), *glow(sig, s=1.12, color=YELLOW))
        sts2 = strips()
        self.at("and the gradient")
        self.play(FadeOut(sig), FadeIn(sts2), run_time=0.6)
        ions2, anims2 = stream(ORANGE, B_X + 0.08, 1.5, -1.5, n=8)
        self.add(*ions2)
        self.at("does the rest")
        self.play(LaggedStart(*anims2, lag_ratio=0.2), vt.animate.set_value(-45), run_time=2.2)
        self.finish()


class S07End(EndCard):
    LINE = "The signal opens a hole, and the gradient does the rest."
