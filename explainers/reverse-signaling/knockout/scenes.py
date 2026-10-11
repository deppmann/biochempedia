"""Reverse signaling, section film: reading a knockout (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = the receptor: its outer rod, the cup that grips, the kinase on its inner end
  YELLOW = the ligand (a B-type ephrin): its stalk, the knob the cup grips, its tail
  GREEN  = the forward signal (into the receptor's cell)
  ORANGE = the reverse signal (into the ephrin's cell)
  RED    = removed / lost (the crosses)
  GREY   = membranes, cells, labels, the grip, the organ

No molecular structures: bars, a cup that closes on a round knob, a wavy tail with dots, a labelled blob.
One framing throughout (both cells, one above the other, the grip in the middle), then a plain
layout of labelled chips for the last scene.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"

CELL_W = 12.2
TY_T = (0.28, 0.54, 0.80)          # where the three tyrosines sit along the tail (0 = membrane, 1 = tip)


# ---------------------------------------------------------------------------------------------
# framings
# ---------------------------------------------------------------------------------------------
class Lay:
    """One framing. k scales the proteins; gy is the height of the grip; xs are the two columns."""

    def __init__(self, k, gy, x):
        self.k, self.gy, self.xs = k, gy, (-x, x)
        self.h, self.m = 0.95 * k, 0.28 * k     # grip to membrane, membrane thickness
        self.u = 0.3 * k                         # how far each cell sits back before the cells touch
        self.tail_len = 1.0 * k
        self.sw = 3 * k ** 0.5
        self.pr = 0.125 * k                      # phosphate badge radius

    def tm_lo(self): return self.gy + self.h                 # face of the upper membrane toward the gap
    def tm_hi(self): return self.gy + self.h + self.m
    def bm_hi(self): return self.gy - self.h                 # face of the lower membrane toward the gap
    def bm_lo(self): return self.gy - self.h - self.m
    def top_edge(self): return self.tm_hi() + 1.0 * self.k
    def bot_edge(self): return self.bm_lo() - 1.12 * self.k
    def kin_y(self): return self.tm_hi() + 0.55 * self.k
    def cup_top(self): return self.gy + 0.56 * self.k


FULL = Lay(k=1.3, gy=0.0, x=1.3)
LOW = Lay(k=2.0, gy=1.35, x=2.3)


def tail_pt(L, x, t):
    return np.array([x + 0.07 * L.k * np.sin(2 * PI * 1.25 * t), L.bm_lo() - t * L.tail_len, 0])


# ---------------------------------------------------------------------------------------------
# the parts
# ---------------------------------------------------------------------------------------------
def backed(shape):
    """a shape with an opaque backing, so lines drawn behind it do not show through."""
    back = shape.copy().set_stroke(width=0).set_fill(BG, 1)
    return VGroup(back, shape)


def rod(L, x, y0, y1, color):
    shape = RoundedRectangle(corner_radius=0.12 * L.k, width=0.42 * L.k, height=abs(y1 - y0), stroke_color=color,
                             stroke_width=L.sw, fill_color=color, fill_opacity=0.4).move_to([x, (y0 + y1) / 2, 0])
    return backed(shape)


def kinase_blob(L, x):
    k = L.k
    shape = RoundedRectangle(corner_radius=0.24 * k, width=1.3 * k, height=0.56 * k, stroke_color=BLUE,
                             stroke_width=L.sw, fill_color=BLUE, fill_opacity=0.25).move_to([x, L.kin_y(), 0])
    return backed(shape), T("kinase", 24, BLUE).move_to(shape).set_z_index(3)


def cup_shape(L, x, closed):
    """the receptor's grip: a cup that opens downward. Closed, it wraps most of the way round the knob."""
    k = L.k
    start, ang = (-45 * DEGREES, 270 * DEGREES) if closed else (0.0, 180 * DEGREES)
    a = AnnularSector(inner_radius=0.36 * k, outer_radius=0.56 * k, angle=ang, start_angle=start,
                      color=BLUE, fill_opacity=1, stroke_width=0)
    return a.shift([x, L.gy, 0])


def knob_shape(L, x):
    return Circle(radius=0.27 * L.k, stroke_color=YELLOW, stroke_width=2, fill_color=YELLOW,
                  fill_opacity=1).move_to([x, L.gy, 0])


def tail_shape(L, x, dots=True):
    """the ephrin's tail: a wavy line with three dots (its tyrosines)."""
    curve = ParametricFunction(lambda t: tail_pt(L, x, t), t_range=[0, 1], color=YELLOW,
                               stroke_width=6 * L.k ** 0.5)
    ds = [Dot(tail_pt(L, x, t), radius=0.085 * L.k, color=YELLOW) for t in TY_T]
    g = VGroup(curve, *ds)
    if not dots:
        for d in ds:
            d.set_opacity(0)
    return g


class World:
    """Both cells and the pair(s) of proteins that grip across them, in one framing.

    parts() lists everything in drawing order and is the same length in every framing, so a change
    of framing is a Transform of each part into its twin. One pair sits in the middle (n=1); two
    sit side by side (n=2, a cluster). upper=False leaves out the receptor's cell, which is above
    the frame in the zoomed framing.
    """

    def __init__(self, L, n=1, tail=True, dots=True, frag=False, closed=True, apart=False):
        self.L, self.has_tail = L, tail
        self.xs = [0.0] if n == 1 else list(L.xs)
        k = L.k
        top_lo, top_hi = L.tm_lo(), L.top_edge()
        self.cell_t = RoundedRectangle(corner_radius=0.12, width=CELL_W, height=top_hi - top_lo, stroke_color=GREY,
                                       stroke_width=2.5, fill_color=GREY, fill_opacity=0.07).move_to([0, (top_lo + top_hi) / 2, 0])
        self.mem_t = RoundedRectangle(corner_radius=0.08, width=CELL_W, height=L.m, stroke_color=GREY, stroke_width=3,
                                      fill_color=GREY, fill_opacity=0.35).move_to([0, top_lo + L.m / 2, 0])
        bot_hi, bot_lo = L.bm_hi(), L.bot_edge()
        self.cell_b = RoundedRectangle(corner_radius=0.12, width=CELL_W, height=bot_hi - bot_lo, stroke_color=GREY,
                                       stroke_width=2.5, fill_color=GREY, fill_opacity=0.07).move_to([0, (bot_hi + bot_lo) / 2, 0])
        self.mem_b = RoundedRectangle(corner_radius=0.08, width=CELL_W, height=L.m, stroke_color=GREY, stroke_width=3,
                                      fill_color=GREY, fill_opacity=0.35).move_to([0, L.bm_lo() + L.m / 2, 0])
        for c in (self.cell_t, self.cell_b):
            c.set_z_index(-3)
        for m in (self.mem_t, self.mem_b):
            m.set_z_index(-2)
        self.rod, self.kin, self.klab, self.cup, self.erod, self.knob, self.tail = [], [], [], [], [], [], []
        for x in self.xs:
            y1 = L.cup_top() + 0.3 * k if frag else L.kin_y()
            self.rod.append(rod(L, x, L.cup_top(), y1, BLUE))
            kb, kl = kinase_blob(L, x)
            self.kin.append(kb)
            self.klab.append(kl)
            self.cup.append(cup_shape(L, x, closed))
            self.erod.append(rod(L, x, L.bm_lo(), L.gy, YELLOW))
            self.knob.append(knob_shape(L, x))
            self.tail.append(tail_shape(L, x, dots))
        if apart:
            for m in self.top_list():
                m.shift(UP * L.u)
            for m in self.bot_list(True):
                m.shift(DOWN * L.u)

    def top_list(self):
        return [self.cell_t, self.mem_t, *self.rod, *self.kin, *self.klab, *self.cup]

    def bot_list(self, all_tails=False):
        return [self.cell_b, self.mem_b, *(self.tail if (self.has_tail or all_tails) else []), *self.erod, *self.knob]

    def parts(self, pairs=None, upper=True):
        idx = range(len(self.xs)) if pairs is None else pairs
        out = [self.cell_b, self.mem_b] + ([self.cell_t, self.mem_t] if upper else [])
        for i in idx:
            if self.has_tail:
                out.append(self.tail[i])
            out += [self.erod[i], self.knob[i], self.rod[i]]
            if upper:
                out += [self.kin[i], self.klab[i]]
            out.append(self.cup[i])
        return out

    def pair_parts(self, i, upper=False):
        return self.parts(pairs=[i], upper=upper)[4 if upper else 2:]

    def together(self, f=1.0):
        """animations: the two cells close up (f of the way)."""
        u = self.L.u * f
        return [m.animate.shift(DOWN * u) for m in self.top_list()] + [m.animate.shift(UP * u) for m in self.bot_list()]

    def apart(self, f=1.0):
        u = self.L.u * f
        return [m.animate.shift(UP * u) for m in self.top_list()] + [m.animate.shift(DOWN * u) for m in self.bot_list()]

    def grip(self, closed=True):
        return [Transform(c, cup_shape(self.L, x, closed)) for c, x in zip(self.cup, self.xs)]


def reframe(old, new):
    """morph each part into the same part of another framing."""
    return [Transform(a, b) for a, b in zip(old, new)]


# ---------------------------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=24, pad=0.2, **kw):
    c = chip(text, color, size=size, pad=pad, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def ghost_chip(text, color=GREY, size=22):
    """a dashed chip: something that is NOT there (or not known)."""
    t = T(text, size, color)
    box = RoundedRectangle(corner_radius=0.14, width=t.width + 0.4, height=t.height + 0.32)
    back = box.copy().set_stroke(width=0).set_fill(BG, 1)
    return VGroup(back, DashedVMobject(box, num_dashes=max(18, int(box.width * 9))).set_color(color), t)


def strike(m, color=RED):
    return Line(m.get_corner(DL) + np.array([-0.08, -0.04, 0]), m.get_corner(UR) + np.array([0.08, 0.04, 0]),
                color=color, stroke_width=7)


def hstrike(m, color=RED, w=6):
    """a strike-through line along the middle of a label."""
    y = m.get_center()[1]
    return Line([m.get_left()[0] - 0.1, y, 0], [m.get_right()[0] + 0.1, y, 0], color=color, stroke_width=w)


def sarrow(a, b, color, w=7, dashed=False):
    a, b = np.array(a, float), np.array(b, float)
    if dashed:
        d = (b - a) / np.linalg.norm(b - a)
        line = DashedLine(a, b - d * 0.22, color=color, stroke_width=w, dash_length=0.14)
        tip = Triangle(fill_color=color, fill_opacity=1, stroke_width=0).scale(0.15).rotate(np.arctan2(d[1], d[0]) - PI / 2).move_to(b - d * 0.1)
        return VGroup(line, tip)
    return Arrow(a, b, buff=0, color=color, stroke_width=w, tip_length=0.28, max_tip_length_to_length_ratio=0.45)


def pop(m, s=1.35):
    return m.animate(rate_func=there_and_back).scale(s)


def glow(*mobs, s=1.1, color=TEXT):
    """flash each mobject in place (one Indicate each: wrapping them in a VGroup would re-add them on top)."""
    return [Indicate(m, color=color, scale_factor=s) for m in mobs]


def pbadge(L):
    c = Circle(radius=L.pr, stroke_color=GOLD, stroke_width=2, fill_color=GOLD, fill_opacity=1)
    return VGroup(c, T("P", 22, BG, weight=BOLD).move_to(c))


def sdot(color, pos):
    return Dot(radius=0.14, color=color).set_stroke(TEXT, 2).move_to(pos)


def qmark(pos, color=GREY, r=0.5):
    back = Circle(radius=r, stroke_width=0, fill_color=BG, fill_opacity=1)
    ring = DashedVMobject(Circle(radius=r), num_dashes=24).set_color(color)
    return VGroup(back, ring, T("?", 40, TEXT, weight=BOLD)).move_to(pos)


def follow(mob, ref, off, edge=ORIGIN):
    """keep a label at a fixed offset from another mobject while that one moves."""
    off = np.array([*off, 0.0][:3], float)

    def upd(m):
        m.move_to(ref.get_center() + off, aligned_edge=edge)
    mob.add_updater(upd)
    upd(mob)
    return mob


def src_blob(center, size=24):
    shape = RoundedRectangle(corner_radius=0.28, width=1.25, height=0.72, stroke_color=PURPLE, stroke_width=4,
                             fill_color=PURPLE, fill_opacity=0.35)
    g = VGroup(shape.copy().set_stroke(width=0).set_fill(BG, 1), shape, T("Src", size, PURPLE, weight=BOLD))
    g[2].move_to(shape)
    return g.move_to(center)


class Film(SpokenScene):
    def outro(self, *anims, then=None, after=None, run_time=0.38):
        """hold until the narration ends, clear what the next scene does not inherit, then (optionally)
        change framing (`then`, and `after` once that has settled)."""
        rest = self.narration_s - 0.02 - self.elapsed()
        if rest > 0:
            self.wait(rest)
        if anims:
            self.play(*anims, run_time=run_time)
        if then:
            self.play(*then, run_time=1.0)
        if after:
            self.play(*after, run_time=0.45)
        if then or after:
            self.wait(0.15)
        self.finish()


def fwd_pts(L, xr):
    """the forward-signal arrow: out of the receptor's kinase, into the upper cell."""
    p0 = np.array([xr + 0.7 * L.k, L.kin_y(), 0])
    return p0, p0 + RIGHT * 2.3


def rev_pts(L, xr):
    """the reverse-signal arrow: out of the tail's tip, into the lower cell."""
    y = L.bm_lo() - 0.93 * L.tail_len
    p0 = np.array([xr + 0.25, y, 0])
    return p0, p0 + RIGHT * 2.3


def fwd_label(L, xr):
    p0, p1 = fwd_pts(L, xr)
    return T("forward signal", 26, GREEN).move_to([(p0[0] + p1[0]) / 2, p0[1] - 0.42, 0])


def rev_label(L, xr):
    p0, p1 = rev_pts(L, xr)
    return T("reverse signal", 26, ORANGE).move_to([(p0[0] + p1[0]) / 2, p0[1] + 0.42, 0])



# ---------------------------------------------------------------------------------------------
# this film
# ---------------------------------------------------------------------------------------------
L1 = FULL
ORGAN_POS = np.array([-4.2, 0.0, 0])
GRIP_POS = np.array([3.9, 0.0, 0])


def eph_of(W):
    return [W.tail[0], W.erod[0], W.knob[0]]


def rec_of(W):
    return [W.rod[0], W.kin[0], W.klab[0], W.cup[0]]


def cell_labels():
    a = T("receptor's cell", 24, GREY).move_to([-5.9, 2.55, 0], aligned_edge=LEFT)
    b = T("ephrin's cell", 24, GREY).move_to([-5.9, -2.55, 0], aligned_edge=LEFT)
    return a, b


def f_arrow(dashed=False):
    f0, f1 = fwd_pts(L1, 0.0)
    return sarrow(f0, f1, GREEN, 6, dashed)


def r_arrow(dashed=False):
    r0, r1 = rev_pts(L1, 0.0)
    return sarrow(r0, r1, ORANGE, 6, dashed)


def f_label():
    return T("forward signal", 26, GREEN).move_to([2.15, 1.85, 0])


def r_label():
    return T("reverse signal", 26, ORANGE).move_to([2.2, -2.4, 0])


def organ_pair():
    organ = ghost_chip("organ", GREY, 26).move_to(ORGAN_POS)
    return organ, strike(organ)


class Film1(Film):
    def setup_world(self, ephrin=True, closed=True):
        W = World(L1, n=1, tail=True, dots=True, closed=closed)
        skip = [] if ephrin else eph_of(W)
        self.add(*[m for m in W.parts() if not any(m is s_ for s_ in skip)])
        a, b = cell_labels()
        self.add(a, b)
        return W, a, b


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Reverse Signaling"
    TITLE = "Which direction did you remove?"


# ---------------------------------------------------------------------------------------------
class S01Organ(Film1):
    """two cells, both signals, then the gene for the ephrin is deleted and an organ fails. (FULL)"""

    def construct(self):
        W = World(L1, n=1, tail=True, dots=True, closed=True, apart=True)
        self.add(*W.parts())
        W2 = None
        ca, cb = cell_labels()
        el = follow(T("B-type ephrin", 28, YELLOW), W.knob[0], (1.0, -0.45), LEFT)
        rl = follow(T("receptor", 28, BLUE), W.cup[0], (1.0, 0.45), LEFT)

        self.at("Picture two cells")
        self.play(*W.together(), FadeIn(ca), FadeIn(cb), run_time=0.9)
        self.at("B type ephrin")
        self.play(FadeIn(el, shift=RIGHT * 0.1), *glow(W.knob[0], s=1.2), run_time=0.5)
        self.at("its receptor")
        self.play(FadeIn(rl, shift=RIGHT * 0.1), *glow(W.cup[0], s=1.1), run_time=0.5)
        self.at("When the two proteins bind")
        self.play(Indicate(W.mem_b, color=TEXT, scale_factor=1.0), run_time=0.7)

        fa, fl = f_arrow(), f_label()
        ra, rlab = r_arrow(), r_label()
        d1 = sdot(GREEN, [0, L1.gy, 0])
        self.at("the receptor signals")
        self.play(FadeIn(d1, scale=0.5), run_time=0.2)
        self.play(d1.animate.move_to([0, L1.kin_y() - 0.28, 0]), run_time=0.5)
        self.play(GrowArrow(fa), d1.animate.move_to(fwd_pts(L1, 0.0)[1]), run_time=0.5)
        self.at("the forward signal")
        self.play(FadeIn(fl, shift=UP * 0.1), FadeOut(d1), run_time=0.4)

        d2 = sdot(ORANGE, [0, L1.gy, 0])
        self.at("A second message")
        self.play(FadeIn(d2, scale=0.5), run_time=0.2)
        self.play(d2.animate.move_to([0, L1.bm_lo() - 0.9, 0]), run_time=0.6)
        self.play(GrowArrow(ra), d2.animate.move_to(rev_pts(L1, 0.0)[1]), run_time=0.5)
        self.at("That is reverse signaling")
        self.play(FadeIn(rlab, shift=UP * 0.1), FadeOut(d2), run_time=0.4)

        # delete the gene: the ephrin goes, the grip opens
        self.at("delete the gene")
        self.play(*[FadeOut(m) for m in (*eph_of(W), el, fa, fl, ra, rlab)], *W.grip(False), run_time=1.0)
        organ, ox = organ_pair()
        self.at("an organ fails")
        self.play(FadeIn(organ, shift=RIGHT * 0.1), run_time=0.4)
        self.play(Create(ox), run_time=0.4)
        q = qmark(GRIP_POS)
        self.at("What did you take away")
        self.play(FadeIn(q, scale=0.6), run_time=0.4)
        self.play(pop(q, 1.2), run_time=0.7)

        self.outro(FadeOut(q), FadeOut(rl))


# ---------------------------------------------------------------------------------------------
class S02Three(Film1):
    """the knockout removes three things at once. (FULL)"""

    def construct(self):
        W, ca, cb = self.setup_world(ephrin=False, closed=False)
        organ, ox = organ_pair()
        self.add(organ, ox)
        fa, fl = f_arrow(True), f_label()
        ra, rl = r_arrow(True), r_label()
        fx, rx = hstrike(fl), hstrike(rl)
        gl = T("grip", 32, TEXT).move_to(GRIP_POS)
        gx = hstrike(gl)

        self.at("the forward signal")
        self.play(FadeIn(fa), FadeIn(fl), run_time=0.4)
        self.at("signal into", nth=0)
        self.play(Create(fx), Indicate(W.cell_t, color=GREEN, scale_factor=1.0), run_time=0.5)
        self.at("the reverse signal")
        self.play(FadeIn(ra), FadeIn(rl), run_time=0.4)
        self.at("signal into", nth=1)
        self.play(Create(rx), Indicate(W.cell_b, color=ORANGE, scale_factor=1.0), run_time=0.5)
        self.at("plain grip")
        self.play(FadeIn(gl), run_time=0.4)
        self.at("held the two cells")
        self.play(Create(gx), run_time=0.4)
        self.play(*glow(gl, s=1.15), run_time=0.6)

        # next scene: the ephrin returns and the pair grips again
        ret = eph_of(World(L1, n=1, tail=True, dots=True, closed=True))
        self.outro(*[FadeOut(m) for m in (fa, fl, fx, ra, rl, rx, gl, gx, organ, ox)],
                   then=[FadeIn(m) for m in ret] + W.grip(True))
        self._ret = ret


# ---------------------------------------------------------------------------------------------
class S03Receptor(Film1):
    """delete the receptor instead: its outer part was a ligand for the other cell. (FULL)"""

    def construct(self):
        W, ca, cb = self.setup_world(ephrin=True, closed=True)

        ghost = VGroup(*[m.copy().set_opacity(0.0) for m in (W.rod[0], W.cup[0])])
        self.at("Deleting the")
        ghosts = [m.copy() for m in (W.rod[0], W.cup[0])]
        for g in ghosts:
            g.set_z_index(0)
        self.play(*[FadeOut(m) for m in rec_of(W)], *[FadeIn(g.set_opacity(0.0)) for g in ghosts], run_time=0.8)
        q1 = qmark([4.4, -0.75, 0])
        self.at("the same problem")
        self.play(FadeIn(q1, scale=0.6), run_time=0.4)

        self.at("outer part")
        ol = T("outer part", 28, BLUE).move_to([1.1, 0.8, 0], aligned_edge=LEFT)
        lead = Line([1.05, 0.85, 0], [0.34, 1.35, 0], color=BLUE, stroke_width=3)
        outline = VGroup(*[m.copy() for m in (W.rod[0], W.cup[0])])
        for m in outline:
            m.set_fill(BLUE, 0.12).set_stroke(BLUE, 3, opacity=0.9)
        self.play(FadeIn(outline), FadeIn(ol), Create(lead), run_time=0.7)
        ll = T("a ligand for the other cell", 28, BLUE).move_to([1.1, 0.25, 0], aligned_edge=LEFT)
        self.at("a ligand for")
        self.play(FadeIn(ll, shift=RIGHT * 0.1), run_time=0.5)
        self.play(*glow(W.knob[0], s=1.2), run_time=0.5)

        self.at("one deletion cannot")
        self.play(pop(q1, 1.25), run_time=0.8)

        self.outro(*[FadeOut(m) for m in (q1, ol, lead, ll, outline, ca, cb, *[p for p in W.parts() if not any(p is r for r in rec_of(W))])])


# ---------------------------------------------------------------------------------------------
class S04Cannot(Film1):
    """three losses, one failed organ: which? Then the design problem, unanswered. (chips)"""

    def construct(self):
        cf = chip("forward signal", GREEN, size=28).move_to([-3.9, 2.55, 0])
        cr = chip("reverse signal", ORANGE, size=28).move_to([0.0, 2.55, 0])
        cg = chip("grip", GREY, size=28).move_to([3.9, 2.55, 0])
        organ = ghost_chip("organ", GREY, 30).move_to([0.0, 0.85, 0])
        ox = strike(organ)
        arrows = [sarrow([c.get_center()[0] * 0.6, 2.0, 0], [organ.get_center()[0] + (c.get_center()[0]) * 0.18, 1.3, 0], GREY, 4)
                  for c in (cf, cr, cg)]
        q = qmark([2.1, 0.85, 0], r=0.42)

        self.at("cannot tell you")
        self.play(FadeIn(organ, shift=UP * 0.1), Create(ox), run_time=0.5)
        self.at("which loss")
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.15) for c in (cf, cr, cg)], lag_ratio=0.3),
                  LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.3), run_time=1.3)
        self.at("does not say which")
        self.play(FadeIn(q, scale=0.6), run_time=0.4)
        self.play(pop(q, 1.2), run_time=0.6)

        hdr = T("DESIGN PROBLEM", 24, GOLD, weight=BOLD).move_to([0, -0.55, 0])
        self.at("design problem")
        self.play(FadeIn(hdr, shift=UP * 0.1), run_time=0.4)
        q1 = T("How could we disrupt reverse signaling", 34, TEXT, t2c={"reverse signaling": ORANGE})
        q2 = T("while leaving forward signaling intact?", 34, TEXT, t2c={"forward signaling": GREEN})
        q1.move_to([0, -1.3, 0])
        q2.move_to([0, -1.95, 0])
        self.at("How could we disrupt")
        self.play(FadeIn(q1, shift=UP * 0.1), run_time=0.7)
        self.at("while leaving")
        self.play(FadeIn(q2, shift=UP * 0.1), run_time=0.7)
        bc = chip("B-class ephrin", YELLOW, size=28).move_to([0, -3.0, 0])
        self.at("of the B class")
        self.play(FadeIn(bc, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05End(EndCard):
    LINE = "The knockout cannot tell you which loss caused the defect."
