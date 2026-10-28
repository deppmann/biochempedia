"""Reverse signaling: a ligand held in a membrane also receives a signal  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = the receptor: its outer rod, the cup that grips, the kinase on its inner end
  YELLOW = the ligand (an ephrin): its stalk, the knob the cup grips, its tail
  GREEN  = the forward signal (into the receptor's cell)
  ORANGE = the reverse signal (into the ligand's cell)
  PURPLE = a Src-family kinase (the kinase the ephrin tail borrows)
  GOLD   = a phosphate (the round "P" badge)
  TEAL   = the adaptor protein that binds the phosphorylated tail
  RED    = removed / ruled out (the crosses)
  GREY   = membranes, cells, labels, parts that are absent

No molecular structures: the receptor and the ligand are bars, the receptor's grip is a cup that
closes on a round knob, the ephrin tail is a wavy line with dots (its tyrosines), a kinase is a
labelled blob, a phosphate is a "P" badge.

Two framings of one picture (the same parts, rebuilt where they are the subject):
  FULL (scenes 1, 2, 5, 6)  both cells, one above the other, the grip in the middle.
  LOW  (scenes 3, 4)        zoomed to the ligand's cell; the receptor's cell is above the frame.
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
class S00Title(TitleCard):
    LESSON = "Reverse Signaling"
    TITLE = "A grip that signals both ways"


# ---------------------------------------------------------------------------------------------
class S01Question(Film):
    """a receptor grips a ligand held in another cell: which cell gets the message? (FULL)"""

    def construct(self):
        L = FULL
        W = World(L, n=1, tail=False, closed=False, apart=True)
        rl = follow(T("receptor", 30, BLUE), W.cup[0], (0.95, 0.5), LEFT)
        ll = follow(T("ligand", 30, YELLOW), W.knob[0], (0.95, -0.5), LEFT)
        self.play(*[FadeIn(m) for m in W.parts()], run_time=0.4)

        self.at("a receptor")
        self.play(FadeIn(rl, shift=RIGHT * 0.1), *glow(W.cup[0], s=1.1), run_time=0.4)
        self.at("grips")
        self.play(*W.together(), run_time=0.9)
        self.at("a ligand")
        self.play(FadeIn(ll, shift=RIGHT * 0.1), *glow(W.knob[0], s=1.2), run_time=0.5)
        self.play(*W.grip(True), run_time=0.4)
        self.at("stuck to another")
        self.play(Indicate(W.mem_b, color=TEXT, scale_factor=1.0), run_time=0.9)

        qa, qb = qmark([3.6, 2.3, 0]), qmark([3.6, -2.2, 0])
        self.at("which cell gets")
        self.play(FadeIn(qa, scale=0.6), FadeIn(qb, scale=0.6), run_time=0.5)
        self.at("the message")
        self.play(pop(qa, 1.3), run_time=0.4)
        self.play(pop(qb, 1.3), run_time=0.4)

        cl_t = T("receptor cell", 26, GREY).move_to([-4.5, 2.5, 0])
        cl_b = T("ligand cell", 26, GREY).move_to([-4.65, -2.6, 0])
        self.at("The receptor sits")
        self.play(*glow(W.rod[0][1], W.cup[0], s=1.05), Indicate(W.cell_t, color=TEXT, scale_factor=1.0), run_time=0.9)
        self.at("upper cell")
        self.play(FadeIn(cl_t, shift=RIGHT * 0.1), run_time=0.5)
        self.at("Its ligand")
        self.play(*glow(W.erod[0][1], W.knob[0], s=1.05), Indicate(W.cell_b, color=TEXT, scale_factor=1.0), run_time=0.9)
        self.at("lower cell")
        self.play(FadeIn(cl_b, shift=RIGHT * 0.1), run_time=0.5)

        self.at("Does the message")
        self.play(pop(qa, 1.15), pop(qb, 1.15), run_time=0.5)
        self.at("one of them")
        self.play(pop(qa, 1.3), run_time=0.4)
        self.play(pop(qb, 1.3), run_time=0.4)
        self.at("or both")
        self.play(pop(qa, 1.3), pop(qb, 1.3), run_time=0.5)
        self.at("Often")
        self.play(qa[1].animate.set_color(GREEN), qa[2].animate.set_color(GREEN),
                  qb[1].animate.set_color(ORANGE), qb[2].animate.set_color(ORANGE), run_time=0.6)
        self.outro(FadeOut(qa), FadeOut(qb), FadeOut(rl), FadeOut(ll), FadeOut(cl_t), FadeOut(cl_b))


# ---------------------------------------------------------------------------------------------
class S02TwoWays(Film):
    """the ligand has a tail inside its own cell; one grip, a forward signal and a reverse signal. (FULL)"""

    def construct(self):
        L = FULL
        W = World(L, n=1, tail=False, dots=False, closed=True)
        x0 = W.xs[0]
        cl_t = T("receptor cell", 26, GREY).move_to([-4.5, 2.5, 0])
        cl_b = T("ligand cell", 26, GREY).move_to([-4.65, -2.6, 0])
        self.add(*W.parts(), cl_t, cl_b)

        mp = T("membrane protein", 28, YELLOW).move_to([x0 + 0.5, -0.82, 0], aligned_edge=LEFT)
        self.at("membrane proteins")
        self.play(FadeIn(mp, shift=RIGHT * 0.1), *glow(W.erod[0][1], W.knob[0], s=1.06), run_time=0.7)

        tail = W.tail[0]
        tl = T("tail", 30, YELLOW).move_to([x0 + 0.55, -2.15, 0], aligned_edge=LEFT)
        self.at("a tail inside")
        self.play(FadeOut(mp), Create(tail, lag_ratio=0), run_time=1.0)
        W.has_tail = True
        self.play(FadeIn(tl, shift=RIGHT * 0.1), run_time=0.3)

        self.at("A tail in the cytosol")
        self.play(FadeOut(tl), Indicate(tail[0], color=TEXT, scale_factor=1.0), run_time=0.9)
        self.at("what you expect")
        self.play(*glow(W.kin[0][1], W.klab[0], W.rod[0][1], s=1.05), run_time=1.0)

        # the two proteins bind again
        self.at("When the two proteins")
        self.play(*W.grip(False), run_time=0.3)
        self.play(*W.apart(0.9), run_time=0.4)
        self.play(*W.together(0.9), run_time=0.5)
        self.play(*W.grip(True), run_time=0.3)

        # forward signal: up the receptor, out into its cell
        f0, f1 = fwd_pts(L, x0)
        dg = sdot(GREEN, [x0, L.gy, 0])
        fa = sarrow(f0, f1, GREEN)
        self.at("the receptor signals")
        self.play(FadeIn(dg, scale=0.5), run_time=0.15)
        self.play(dg.animate.move_to([x0, L.kin_y() - 0.28, 0]), run_time=0.7)
        self.at("into its own")
        self.play(GrowArrow(fa), dg.animate.move_to(f1), run_time=0.6)
        self.play(FadeOut(dg), run_time=0.2)
        fl = fwd_label(L, x0)
        self.at("That is the forward")
        self.play(FadeIn(fl, shift=UP * 0.1), run_time=0.4)

        # reverse signal: down the ligand and its new tail, out into its cell
        r0, r1 = rev_pts(L, x0)
        og = sdot(ORANGE, [x0, L.gy, 0])
        ra = sarrow(r0, r1, ORANGE)
        self.at("A second message")
        self.play(FadeIn(og, scale=0.5), run_time=0.12)
        self.play(og.animate.move_to([x0, L.bm_lo(), 0]), run_time=0.4)
        self.play(MoveAlongPath(og, tail[0]), run_time=0.6)
        self.at("passes into the cell")
        self.play(GrowArrow(ra), og.animate.move_to(r1), run_time=0.6)
        self.play(FadeOut(og), run_time=0.2)
        rl = rev_label(L, x0)
        self.at("That is reverse")
        self.play(FadeIn(rl, shift=DOWN * 0.1), run_time=0.4)

        # zoom to the ligand's cell: the receptor's cell and its kinase leave through the top
        W3 = World(LOW, n=1, frag=True, dots=True, closed=True)
        self.outro(FadeOut(fa), FadeOut(fl), FadeOut(ra), FadeOut(rl), FadeOut(cl_t), FadeOut(cl_b),
                   then=[FadeOut(W.cell_t, shift=UP * 1.5), FadeOut(W.mem_t, shift=UP * 1.5), FadeOut(W.kin[0], shift=UP * 1.5), FadeOut(W.klab[0], shift=UP * 1.5),
                         *reframe(W.parts(upper=False), W3.parts(upper=False))])


# ---------------------------------------------------------------------------------------------
class S03Tail(Film):
    """a B-type ephrin's tail has no enzyme, yet it is phosphorylated: the kinase must be in its own cell. (LOW)"""

    def construct(self):
        L = LOW
        W = World(L, n=1, frag=True, dots=True, closed=True)
        x0 = W.xs[0]
        self.add(*W.parts(upper=False))
        dy1 = tail_pt(L, x0, TY_T[0])
        mid_bm = (L.bm_lo() + L.bm_hi()) / 2

        eph = T("ephrin", 30, YELLOW).move_to([x0 + 0.6, 0.3, 0], aligned_edge=LEFT)
        self.at("are the clearest")
        self.play(FadeIn(eph, shift=RIGHT * 0.1), *glow(W.erod[0][1], W.knob[0], s=1.05), run_time=0.7)

        og = sdot(ORANGE, [x0, L.gy, 0])
        self.at("reverse signaling")
        self.play(FadeIn(og, scale=0.5), run_time=0.12)
        self.play(og.animate.move_to([x0, L.bm_lo(), 0]), run_time=0.5)
        self.play(MoveAlongPath(og, W.tail[0][0]), run_time=0.7)
        self.play(FadeOut(og), run_time=0.15)

        mem = T("membrane", 24, GREY).move_to([-4.6, mid_bm, 0])
        self.at("crosses the membrane")
        self.play(FadeIn(mem), FadeOut(eph), *glow(W.erod[0][1], s=1.05), run_time=0.6)

        tl = T("tail", 30, YELLOW).move_to([x0 - 0.5, dy1[1], 0], aligned_edge=RIGHT)
        self.at("short tail")
        self.play(FadeIn(tl, shift=LEFT * 0.1), Indicate(W.tail[0][0], color=TEXT, scale_factor=1.0), run_time=0.7)

        ne = ghost_chip("enzyme", GREY, 26).move_to([2.6, -2.55, 0])
        link = DashedLine([x0 + 0.3, -2.55, 0], ne.get_left(), color=GREY, stroke_width=4, dash_length=0.1)
        x1 = strike(ne)
        self.at("contains no enzyme")
        self.play(Create(link), FadeIn(ne), run_time=0.5)
        self.play(Create(x1), run_time=0.3)

        self.at("yet when")
        self.play(*glow(W.cup[0], W.knob[0], s=1.06), run_time=0.8)
        frag = T("outer part", 30, BLUE).move_to([x0 + 1.75, L.gy + 0.95, 0], aligned_edge=LEFT)
        flead = Line([x0 + 1.7, L.gy + 0.95, 0], [x0 + 0.68, L.gy + 0.95, 0], color=BLUE, stroke_width=3)
        ty, hw = L.cup_top() + 0.3 * L.k, 0.21 * L.k          # the cut end of the receptor's outer part
        cut = VMobject(color=TEXT, stroke_width=4)
        cut.set_points_as_corners([[x0 - hw, ty, 0], [x0 - hw / 2, ty + 0.12, 0], [x0, ty - 0.12, 0], [x0 + hw / 2, ty + 0.12, 0], [x0 + hw, ty, 0]])
        self.at("outer part")
        self.play(FadeIn(frag, shift=RIGHT * 0.1), Create(flead), Create(cut), FadeOut(tl), *glow(W.cup[0], s=1.05), run_time=0.7)

        pb = pbadge(L).move_to(dy1)
        pl = T("phosphate on a tyrosine", 28, GOLD).move_to([x0 + 0.6, dy1[1], 0], aligned_edge=LEFT)
        self.at("gains a phosphate")
        self.play(FadeIn(pb, scale=0.3), run_time=0.35)
        self.play(FadeIn(pl, shift=RIGHT * 0.1), pop(pb, 1.35), run_time=0.6)

        self.at("That outer part")
        self.play(*glow(W.cup[0], s=1.05), run_time=0.7)
        nk = ghost_chip("kinase", GREY, 26).move_to([x0 + 1.9, L.cup_top() + 0.3 * L.k + 0.0, 0])
        x2 = strike(nk)
        self.at("has no kinase")
        self.play(FadeIn(nk), run_time=0.3)
        self.play(Create(x2), run_time=0.3)
        self.at("neither does")
        self.play(Indicate(ne[2], color=TEXT, scale_factor=1.1), Indicate(x1, color=TEXT, scale_factor=1.1), run_time=0.7)

        kq = ghost_chip("kinase ?", PURPLE, 28).move_to([-3.6, -1.9, 0])
        self.at("So a kinase")
        self.play(FadeIn(kq, shift=RIGHT * 0.15), Indicate(W.cell_b, color=TEXT, scale_factor=1.0), run_time=0.8)
        self.at("own cell")
        self.play(Indicate(W.cell_b, color=TEXT, scale_factor=1.0), run_time=0.8)
        self.at("must do the work")
        self.play(pop(kq, 1.15), pop(pb, 1.3), run_time=0.6)

        self.outro(FadeOut(mem), FadeOut(ne), FadeOut(link), FadeOut(x1), FadeOut(frag), FadeOut(flead), FadeOut(cut), FadeOut(pl),
                   FadeOut(nk), FadeOut(x2))


# ---------------------------------------------------------------------------------------------
class S04Borrow(Film):
    """Src-family kinases gather at clustered ephrins and phosphorylate the tail; an adaptor binds. (LOW -> FULL)"""

    def construct(self):
        L = LOW
        W = World(L, n=2, frag=True, dots=True, closed=True)
        xa, xb = W.xs
        A = W.pair_parts(0)
        for m in A:                                   # the first pair starts where the last scene left it: in the middle
            m.shift(RIGHT * -xa)
        self.add(*W.parts(pairs=[0], upper=False))
        pa = [tail_pt(L, xa, t) for t in TY_T]
        pb_ = [tail_pt(L, xb, t) for t in TY_T]
        p1 = pbadge(L).move_to(tail_pt(L, 0.0, TY_T[0]))
        kq = ghost_chip("kinase ?", PURPLE, 28).move_to([-3.6, -1.9, 0])
        self.add(p1, kq)
        y1 = pa[0][1]

        self.at("Which kinase")
        self.play(pop(kq, 1.2), run_time=0.6)

        s1 = src_blob([-3.6, -1.9, 0])
        sl = follow(T("Src-family\nkinase", 24, PURPLE, line_spacing=0.6), s1, (0.35, -0.9), RIGHT)
        self.at("family kinases")
        self.play(ReplacementTransform(kq, s1), FadeIn(sl), run_time=0.6)

        self.at("gather where")
        self.play(s1.animate.move_to([-1.05, y1 - 0.15, 0]), run_time=0.6)

        # a second pair joins: a cluster
        s2 = src_blob([xb + 1.05, y1 - 0.15, 0])
        cl = T("cluster", 30, YELLOW).move_to([0, 0.3, 0])
        cla = [Arrow([sgn * 0.95, 0.3, 0], [sgn * 1.5, 0.3, 0], buff=0, color=YELLOW, stroke_width=4, tip_length=0.18)
               for sgn in (-1, 1)]
        self.at("cluster")
        self.play(*[m.animate.shift(LEFT * -xa) for m in [*A, s1, p1]],
                  *[FadeIn(m, shift=LEFT * 1.2) for m in W.pair_parts(1)],
                  FadeIn(s2, shift=LEFT * 0.8), run_time=1.0)
        self.play(FadeIn(cl), *[GrowArrow(a_) for a_ in cla], run_time=0.4)

        # the tails gain their phosphates while a Src-family kinase sits beside each one (no hand-over drawn)
        badges = [(pbadge(L).move_to(d), d) for d in (pa[1], pb_[0], pa[2], pb_[1], pb_[2])]
        self.at("help to put")
        self.play(FadeOut(cl), *[FadeOut(a_) for a_ in cla], pop(s1, 1.12), pop(s2, 1.12),
                  LaggedStart(*[FadeIn(b, scale=0.3) for b, _ in badges], lag_ratio=0.2), run_time=1.3)
        self.at("on the tail")
        self.play(*[pop(b, 1.25) for b, _ in badges], pop(p1, 1.25), run_time=0.6)

        # the adaptor
        ad = bchip("adaptor", TEAL, 26).move_to([0.0, y1, 0])
        self.at("then binds")
        self.play(FadeIn(ad, shift=UP * 0.1), run_time=0.4)
        self.play(ad.animate.move_to([xa + 0.39 + ad.width / 2, y1, 0]), run_time=0.6)
        self.at("phosphorylated tyrosines")
        self.play(*glow(ad[1], ad[2], s=1.08), pop(p1, 1.25), pop(badges[0][0], 1.25), pop(badges[2][0], 1.25), run_time=0.8)

        act = bchip("actin skeleton", GREY, 26).move_to([0.5, -2.85, 0])
        a1 = sarrow([ad.get_right()[0] - 0.1, ad.get_bottom()[1] - 0.02, 0], [act.get_center()[0] - 0.5, act.get_top()[1] + 0.04, 0], ORANGE, 6)
        self.at("It connects")
        self.play(GrowArrow(a1), run_time=0.5)
        self.at("proteins that reshape")
        self.play(FadeIn(act, shift=UP * 0.1), run_time=0.5)
        self.at("actin skeleton")
        self.play(*glow(act[1], act[2], s=1.08), run_time=0.7)

        self.at("This is")
        self.play(Indicate(W.tail[0][0], color=TEXT, scale_factor=1.0), Indicate(W.tail[1][0], color=TEXT, scale_factor=1.0), run_time=0.7)
        self.at("one route")
        self.play(*glow(s1[1], s1[2], s2[1], s2[2], s=1.12), run_time=0.8)

        W5 = World(FULL, n=2, tail=True, dots=True, closed=True)
        self.outro(FadeOut(s1), FadeOut(s2), FadeOut(sl), FadeOut(ad), FadeOut(act), FadeOut(a1), FadeOut(p1),
                   *[FadeOut(b) for b, _ in badges],
                   then=reframe(W.parts(upper=False), W5.parts(upper=False)),
                   after=[FadeIn(W5.cell_t), FadeIn(W5.mem_t), *[FadeIn(k_) for k_ in W5.kin], *[FadeIn(k_) for k_ in W5.klab]])


# ---------------------------------------------------------------------------------------------
class S05Test(Film):
    """a knockout removes both signals and the grip; an ephrin without its tail removes only the reverse signal. (FULL)"""

    def construct(self):
        L = FULL
        W5 = World(L, n=2, tail=True, dots=True, closed=True)
        W = W5
        xa, xb = W.xs
        self.add(*W.parts())
        eph_parts = [*W.tail, *W.erod, *W.knob]

        # delete the gene: the ephrins go, the cups let go
        self.at("delete the gene")
        self.play(*[FadeOut(m) for m in eph_parts], *W.grip(False), run_time=1.0)

        organ = ghost_chip("organ", GREY, 26).move_to([-4.2, 0.0, 0])
        ox = strike(organ)
        self.at("an organ fails")
        self.play(FadeIn(organ, shift=RIGHT * 0.1), run_time=0.4)
        self.at("fails to form")
        self.play(Create(ox), run_time=0.4)

        f0, f1 = fwd_pts(L, xb)
        r0, r1 = rev_pts(L, xb)
        fa_g, ra_g = sarrow(f0, f1, GREEN, 6, True), sarrow(r0, r1, ORANGE, 6, True)
        fl, rl = fwd_label(L, xb), rev_label(L, xb)
        fx, rx = hstrike(fl), hstrike(rl)
        self.at("the forward signal")
        self.play(FadeIn(fa_g), FadeIn(fl), run_time=0.4)
        self.play(Create(fx), run_time=0.3)
        self.at("the reverse signal")
        self.play(FadeIn(ra_g), FadeIn(rl), run_time=0.4)
        self.play(Create(rx), run_time=0.3)
        gl = T("grip", 30, TEXT).move_to([3.7, 0.0, 0])
        gx = hstrike(gl)
        self.at("the grip that held")
        self.play(FadeIn(gl), run_time=0.3)
        self.play(Create(gx), run_time=0.3)

        self.at("The knockout")
        self.play(LaggedStart(*[pop(m, 1.18) for m in (fl, gl, rl)], lag_ratio=0.35), run_time=1.2)

        # change the ephrin instead: it comes back, tail and all
        self.at("So change")
        self.play(*[FadeOut(m) for m in (organ, ox, fa_g, fl, fx, ra_g, rl, rx, gl, gx)],
                  *[FadeIn(m, shift=UP * 0.25) for m in eph_parts], run_time=0.9)

        ol = T("outer part", 28, YELLOW).move_to([xb + 0.7, -0.55, 0], aligned_edge=LEFT)
        lead1 = Line([xb + 0.65, -0.55, 0], [xb + 0.32, -0.55, 0], color=YELLOW, stroke_width=3)
        self.at("outer part")
        self.play(FadeIn(ol), Create(lead1), *glow(W.erod[1][1], W.knob[1], s=1.06), run_time=0.7)
        ml = T("membrane segment", 28, YELLOW).move_to([xb + 0.95, -2.05, 0], aligned_edge=LEFT)
        lead2 = Line([xb + 0.9, -2.0, 0], [xb + 0.45, -1.7, 0], color=YELLOW, stroke_width=3)
        mseg = Rectangle(width=0.7 * L.k, height=L.m, stroke_color=YELLOW, stroke_width=3).move_to([xb, L.bm_lo() + L.m / 2, 0])
        self.at("membrane segment")
        self.play(FadeIn(ml), Create(lead2), Create(mseg), run_time=0.7)

        # remove only the tail
        cuts = [Line([x - 0.35, L.bm_lo() - 0.12, 0], [x + 0.35, L.bm_lo() - 0.34, 0], color=RED, stroke_width=7) for x in (xa, xb)]
        self.at("remove only the tail")
        self.play(*[Create(c) for c in cuts], run_time=0.4)
        self.play(*[FadeOut(t, shift=DOWN * 0.3) for t in W.tail], *[FadeOut(c) for c in cuts], FadeOut(ol), FadeOut(lead1),
                  FadeOut(ml), FadeOut(lead2), FadeOut(mseg), run_time=0.7)

        sl = T("at the cell surface", 28, YELLOW).move_to([xb + 0.7, -0.55, 0], aligned_edge=LEFT)
        ck = VGroup(Line([0, 0, 0], [0.16, -0.16, 0], color=TEXT, stroke_width=6), Line([0.16, -0.16, 0], [0.5, 0.3, 0], color=TEXT, stroke_width=6))
        ck.next_to(sl, RIGHT, buff=0.2)
        self.at("reaches the surface")
        self.play(FadeIn(sl, shift=RIGHT * 0.1), Create(ck), *glow(W.knob[0], W.knob[1], s=1.25), run_time=0.8)

        # close the grip and measure the forward signal
        self.at("then measure")
        self.play(*W.grip(True), run_time=0.5)
        fa = sarrow(f0, f1, GREEN)
        dgs = [sdot(GREEN, [x, L.gy, 0]) for x in (xa, xb)]
        self.at("forward signal")
        self.play(*[FadeIn(d, scale=0.5) for d in dgs], FadeOut(sl), FadeOut(ck), run_time=0.2)
        self.play(*[d.animate.move_to([x, L.kin_y() - 0.28, 0]) for d, x in zip(dgs, (xa, xb))], run_time=0.6)
        self.play(GrowArrow(fa), dgs[1].animate.move_to(f1), FadeOut(dgs[0]), run_time=0.5)
        fl2 = T("forward signal?", 26, GREEN).move_to(fwd_label(L, xb))
        self.play(FadeIn(fl2, shift=UP * 0.1), FadeOut(dgs[1]), run_time=0.3)

        # the reverse signal is gone
        og = [sdot(ORANGE, [x, L.gy, 0]) for x in (xa, xb)]
        self.at("is gone")
        self.play(*[FadeIn(d, scale=0.5) for d in og], run_time=0.15)
        self.play(*[d.animate.move_to([x, L.bm_lo() + 0.02, 0]) for d, x in zip(og, (xa, xb))], run_time=0.6)
        stop = [Line([x - 0.35, L.bm_lo() - 0.1, 0], [x + 0.35, L.bm_lo() - 0.1, 0], color=RED, stroke_width=8) for x in (xa, xb)]
        ra2, rl2 = sarrow(r0, r1, ORANGE, 6, True), rev_label(L, xb)
        self.play(*[Create(s_) for s_ in stop], *[FadeOut(d) for d in og], FadeIn(ra2), FadeIn(rl2), run_time=0.4)
        rx2 = hstrike(rl2)
        self.play(Create(rx2), run_time=0.3)

        # next scene: the tails come back and both signals run
        self.outro(FadeOut(fa), FadeOut(fl2), FadeOut(ra2), FadeOut(rl2), FadeOut(rx2), *[FadeOut(s_) for s_ in stop],
                   then=[Create(t, lag_ratio=0) for t in W.tail])


# ---------------------------------------------------------------------------------------------
class S06Rule(Film):
    """other ligands do it too; the names record history; the rule. (FULL)"""

    def construct(self):
        L = FULL
        W = World(L, n=2, tail=True, dots=True, closed=True)
        xa, xb = W.xs
        self.add(*W.parts())
        f0, f1 = fwd_pts(L, xb)
        r0, r1 = rev_pts(L, xb)
        fa, ra = sarrow(f0, f1, GREEN), sarrow(r0, r1, ORANGE)
        fl, rl = fwd_label(L, xb), rev_label(L, xb)

        up = T("receptor", 30, BLUE).move_to([xb + 0.95, 0.5, 0], aligned_edge=LEFT)
        lo = T("ephrin", 30, YELLOW).move_to([xb + 0.95, -0.5, 0], aligned_edge=LEFT)
        self.at("Other ligands")
        self.play(FadeIn(up, shift=RIGHT * 0.1), FadeIn(lo, shift=RIGHT * 0.1), run_time=0.5)
        # both signals run
        dg = [sdot(GREEN, [x, L.gy, 0]) for x in (xa, xb)]
        og = [sdot(ORANGE, [x, L.gy, 0]) for x in (xa, xb)]
        self.at("work this way")
        self.play(*[FadeIn(d, scale=0.5) for d in dg + og], run_time=0.15)
        self.play(*[d.animate.move_to([x, L.kin_y() - 0.28, 0]) for d, x in zip(dg, (xa, xb))],
                  *[d.animate.move_to([x, L.bm_lo(), 0]) for d, x in zip(og, (xa, xb))], run_time=0.55)
        self.play(GrowArrow(fa), GrowArrow(ra), dg[1].animate.move_to(f1), og[1].animate.move_to(r1),
                  FadeOut(dg[0]), FadeOut(og[0]), run_time=0.5)
        self.play(FadeIn(fl), FadeIn(rl), FadeOut(dg[1]), FadeOut(og[1]), run_time=0.3)

        tnf = T("TNF", 30, YELLOW).move_to([xb + 0.95, -0.5, 0], aligned_edge=LEFT)
        self.at("acts as")
        # the other families are not drawn as ephrins: no "kinase" label, no tyrosine dots, only a plain tail
        self.play(ReplacementTransform(lo, tnf), *[FadeOut(k_) for k_ in W.klab],
                  *[d.animate.set_opacity(0) for t_ in W.tail for d in t_[1:]], *glow(ra, s=1.0), run_time=0.8)
        sem = T("semaphorin", 30, YELLOW).move_to([xb + 0.95, -0.5, 0], aligned_edge=LEFT)
        self.at("so does a fly")
        self.play(ReplacementTransform(tnf, sem), run_time=0.7)

        lig = T("ligand", 30, YELLOW).move_to([xb + 0.95, -0.5, 0], aligned_edge=LEFT)
        self.at("In each pair")
        self.play(ReplacementTransform(sem, lig), run_time=0.5)
        self.at("named receptor")
        self.play(Indicate(up, color=TEXT, scale_factor=1.12), run_time=0.6)
        self.at("also gives")
        self.play(*glow(W.cup[0], W.cup[1], s=1.12), Indicate(ra, color=TEXT, scale_factor=1.05), Indicate(rl, color=TEXT, scale_factor=1.08), run_time=0.8)
        self.at("named ligand")
        self.play(Indicate(lig, color=TEXT, scale_factor=1.12), run_time=0.6)
        self.at("also receives")
        self.play(Indicate(ra, color=TEXT, scale_factor=1.05), Indicate(rl, color=TEXT, scale_factor=1.08), run_time=0.8)

        # the names were fixed by history: they could change places
        self.at("fixed by history")
        self.play(up.animate(path_arc=PI / 2).move_to(lig.get_center()),
                  lig.animate(path_arc=PI / 2).move_to(up.get_center()), run_time=1.1)
        self.at("keep this rule")
        self.play(FadeOut(up), FadeOut(lig), run_time=0.4)
        self.at("can receive")
        self.play(Indicate(ra, color=TEXT, scale_factor=1.05), Indicate(rl, color=TEXT, scale_factor=1.08), run_time=0.7)
        self.at("as well as give")
        self.play(Indicate(fa, color=TEXT, scale_factor=1.05), Indicate(fl, color=TEXT, scale_factor=1.08), run_time=0.7)
        self.finish()


class S07End(EndCard):
    LINE = "A membrane ligand can receive a signal as well as give one."
