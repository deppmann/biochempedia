# COLOR MAP (kept for the whole chapter series; one color per concept)
#   BLUE    the protein / polypeptide chain / candidate conformations still alive
#   ORANGE  backbone geometry constraints: peptide bond, rigid plane, phi/psi hinges, "geometry allows"
#   YELLOW  nonpolar (hydrophobic) side chains in general (chain beads)
#   PURPLE  polar residues (chain beads)
#   TEAL    water, buffer, the underlined phrase "in a given environment", "water chooses"
#   GREEN   the native fold, allowed / surviving, working (activity)
#   RED     forbidden, eliminated, misfolded, disease, loss of activity
#   GOLD    disulfide bonds and the cysteines that form them
#   GREY    labels, frames, structure, tubes
#   TEXT    reagents (urea, reducing agent), neutral words
# Sickle-cell residue: a charged RED bead with a minus sign (Glu6) that flips to a YELLOW oily bead (Val6),
# the same yellow as every other nonpolar bead in the series.
# NOTHING here draws a molecular structure: chains are smooth curves and bead strings, proteins are
# labelled blobs, and bridges are plain gold bars.
import numpy as np
from bp_style import *

ORANGE = "#F29E4C"
PURPLE = "#B58CE0"
LG = "#C9CED8"          # bright label grey (secondary labels)
OILY = YELLOW           # the oily (nonpolar) bead: same yellow as the series map
LESSON_TITLE = "Protein Three-Dimensional Structure: The Sequence Sets the Shape"

SEQ = [BLUE, PURPLE, YELLOW, BLUE, BLUE, PURPLE, YELLOW, BLUE, PURPLE, YELLOW, YELLOW, BLUE, PURPLE, BLUE, YELLOW]


# ------------------------------------------------------------------ helpers
def lab(txt, size=36, color=LG, **kw):
    return T(txt, size=size, color=color, **kw)


def veil(cx, cy, w, h, op=0.72):
    """A dark sheet that dims whatever is under it (fade it out to bring that part back)."""
    return Rectangle(width=w, height=h, stroke_width=0, fill_color=BG, fill_opacity=op).move_to([cx, cy, 0]).set_z_index(20)


def leader(a, b, color=LG, w=4):
    return Arrow(a, b, buff=0.05, color=color, stroke_width=w, max_tip_length_to_length_ratio=0.18, max_stroke_width_to_length_ratio=8)


class Chain:
    """A string of beads joined by links (a schematic polypeptide), through given points."""

    def __init__(self, pts, r=0.28, colors=None, link_w=6):
        self.pts = [np.array([p[0], p[1], 0.0]) for p in pts]
        n = len(self.pts)
        cols = colors or [SEQ[i % len(SEQ)] for i in range(n)]
        self.links = VGroup(*[Line(self.pts[i], self.pts[i + 1], color=GREY, stroke_width=link_w) for i in range(n - 1)])
        self.beads = VGroup(*[Dot(self.pts[i], radius=r, color=cols[i]).set_stroke(TEXT, 1.5, opacity=0.5) for i in range(n)])
        self.group = VGroup(self.links, self.beads)


def wave_pts(n, x0, x1, y, amp):
    xs = np.linspace(x0, x1, n)
    return [(x, y + amp * np.sin(2 * PI * i / (n - 1))) for i, x in enumerate(xs)]


# ---- compact (folded) and loose (coil) paths with the same number of points, so one turns into the other
NPT = 60


def _arc_resample(poly, n):
    d = np.r_[0, np.cumsum(np.linalg.norm(np.diff(poly, axis=0), axis=1))]
    u = np.linspace(0, d[-1], n)
    return np.stack([np.interp(u, d, poly[:, 0]), np.interp(u, d, poly[:, 1])], 1)


ROWS_Y = np.linspace(0.8, -0.8, 5)


def _half(y):
    return 1.05 * np.sqrt(max(0.0, 1 - (y / 1.0) ** 2)) + 0.05


def _folded():
    corners = []
    for k, y in enumerate(ROWS_Y):
        x = _half(y)
        corners += [(-x, y), (x, y)] if k % 2 == 0 else [(x, y), (-x, y)]
    P = _arc_resample(np.array(corners), 400)
    w = 15
    Q = P.copy()
    for i in range(len(P)):
        a, b = max(0, i - w), min(len(P), i + w + 1)
        Q[i] = P[a:b].mean(0)
    Q[0], Q[-1] = P[0], P[-1]
    R = _arc_resample(Q, NPT)
    return np.c_[R, np.zeros(NPT)]


def _coil(ay=1.0):
    s = np.linspace(0, 1, NPT)
    return np.stack([-1.45 + 2.9 * s, ay * (0.55 * np.sin(7 * s + 0.4) + 0.22 * np.sin(17 * s + 1.0)), np.zeros(NPT)], 1)


# (row a, row b, x): a gold bar joining two rows of the packed chain; four bars, clearly apart
BRIDGES = [(0, 2, -0.55), (1, 3, -0.12), (2, 4, 0.28), (1, 3, 0.7)]


class Enz:
    """Ribonuclease as a labelled cartoon: a closed-in blob with its chain, or a loose coil."""

    def __init__(self, kind="native", pos=ORIGIN, k=1.0, bridges=False, stroke=7, ay=1.0):
        self.k, self.pos = k, np.array(pos, dtype=float)
        pts = (_folded() if kind == "native" else _coil(ay)) * k + self.pos
        self.chain = VMobject(stroke_color=BLUE, stroke_width=stroke, fill_opacity=0)
        self.chain.set_points_smoothly(pts)
        self.blob = Ellipse(width=2.6 * k, height=2.0 * k, stroke_color=BLUE, stroke_width=3, fill_color=BLUE,
                            fill_opacity=0.14 if kind == "native" else 0.0).move_to(self.pos)
        if kind != "native":
            self.blob.set_stroke(opacity=0)
        self.bpts = [(np.array([x, ROWS_Y[a], 0.0]) * k + self.pos, np.array([x, ROWS_Y[b], 0.0]) * k + self.pos) for a, b, x in BRIDGES]
        rr = 0.08 * max(k, 0.7) + 0.04
        self.bridges = VGroup(*[VGroup(Line(a, b, color=GOLD, stroke_width=stroke + 1), Dot(a, radius=rr, color=GOLD).set_z_index(4), Dot(b, radius=rr, color=GOLD).set_z_index(4))
                                for a, b in self.bpts]) if bridges else VGroup()
        self.group = VGroup(self.blob, self.chain, self.bridges)


class Kit:
    """One test tube with its liquid, label, activity meter and enzyme. cx, cy, k place and scale it."""
    W, TOP, BOT, LIQ = 2.4, 2.2, -1.8, 1.2

    def __init__(self, cx, cy=0.0, k=1.0, side_label=False):
        self.cx, self.cy, self.k, self.side = cx, cy, k, side_label

    def P(self, dx, dy):
        return np.array([self.cx + dx * self.k, self.cy + dy * self.k, 0.0])

    def glass(self):
        r = self.W / 2
        c = self.P(0, self.BOT + r)
        return VGroup(Line(self.P(-r, self.TOP), self.P(-r, self.BOT + r)),
                      Arc(radius=r * self.k, start_angle=PI, angle=PI, arc_center=c),
                      Line(self.P(r, self.BOT + r), self.P(r, self.TOP))).set_stroke(GREY, 5)

    def liquid(self):
        r = self.W / 2
        c = self.P(0, self.BOT + r)
        rect = Rectangle(width=self.W * self.k, height=(self.LIQ - (self.BOT + r)) * self.k, stroke_width=0,
                         fill_color=TEAL, fill_opacity=0.2).move_to(c, aligned_edge=DOWN)
        sec = Sector(radius=r * self.k, start_angle=PI, angle=PI, arc_center=c, stroke_width=0,
                     fill_color=TEAL, fill_opacity=0.2)
        return VGroup(sec, rect)

    def label(self, i):
        if self.side:
            return T(f"tube {i}", size=36, color=TEXT).move_to(self.P(-2.3, 1.7))
        return T(f"tube {i}", size=36, color=TEXT).move_to(self.P(0, 2.68))

    def meter(self, val):
        """val: number 0..100, or None for an unknown ('?')."""
        w = 2.3 * self.k
        h = 0.34
        bar = Rectangle(width=w, height=h, stroke_color=LG, stroke_width=3, fill_opacity=0).move_to(self.P(0, -2.38))
        parts = [bar]
        if val:
            f = Rectangle(width=max(0.001, w * val / 100.0), height=h, stroke_width=0, fill_color=GREEN, fill_opacity=0.9)
            f.move_to(bar.get_left(), aligned_edge=LEFT)
            parts.append(f)
        txt = "activity ?" if val is None else f"activity {int(round(val))}%"
        col = TEXT if val is None else (RED if val < 1 else GREEN)
        parts.append(T(txt, size=36, color=col).next_to(bar, DOWN, buff=0.17))
        return VGroup(*parts)

    def enz(self, kind="native", bridges=False):
        y = -0.55 if kind == "native" else -0.4
        return Enz(kind, self.P(0, y), 0.75 * self.k, bridges=bridges, stroke=6, ay=1.6)

    def veil(self, op=0.72):
        return veil(self.cx, self.cy - 0.1 * self.k, 2.6 * self.k, 7.0 * self.k, op)


def meter_anim(kit, a, b, run_time):
    holder = kit.meter(a)

    def upd(mob, alpha):
        mob.become(kit.meter(a + (b - a) * alpha))
    return holder, UpdateFromAlphaFunc(holder, upd, run_time=run_time, rate_func=smooth)


TX = [-4.8, 0.0, 4.8]


def reagent(kind):
    return chip("urea", TEXT, size=36, pad=0.12) if kind == "urea" else chip("reducing agent", TEXT, size=36, pad=0.12)


def rack_reagents():
    urea = reagent("urea").move_to([-2.3, 3.38, 0])
    red = reagent("red").move_to([2.6, 3.38, 0])
    ua = leader([-2.0, 3.0, 0], [-0.42, 0.75, 0], TEXT, 5)
    ra = leader([2.2, 3.0, 0], [0.42, 0.75, 0], TEXT, 5)
    return urea, ua, red, ra


def quote_lines():
    ls = ["The fold is set by", "the amino acid sequence,", "in a given environment."]
    return VGroup(*[T(s, size=58, font=TITLE_FONT) for s in ls]).arrange(DOWN, buff=0.4)


def quote_head():
    return T("Anfinsen's conclusion", size=44, color=LG).move_to([0, 3.15, 0])


def pinned():
    t = T("in a given environment", size=40, color=TEXT, font=TITLE_FONT)
    u = Line(t.get_corner(DL) + DOWN * 0.1, t.get_corner(DR) + DOWN * 0.1, color=TEAL, stroke_width=5)
    return VGroup(t, u).to_corner(UL, buff=0.38)


# ------------------------------------------------------------------ 0. title
class S00Title(TitleCard):
    LESSON = LESSON_TITLE
    TITLE = "One String, One Shape"


# ------------------------------------------------------------------ 1-2. the hemoglobin chain and the swapped bead
HB_Y, HB_AMP, HB_R, SP = 0.3, 1.1, 0.55, 5


def hb_chain():
    cols = [SEQ[i] for i in range(12)]
    cols[SP] = RED
    return Chain(wave_pts(12, -5.8, 5.8, HB_Y, HB_AMP), r=HB_R, colors=cols)


def minus_on(p):
    return Line(p + LEFT * 0.2, p + RIGHT * 0.2, color=BG, stroke_width=9).set_z_index(3)


def hb_label():
    return T("hemoglobin", size=42).move_to([-4.4, 3.2, 0])


class S01(SpokenScene):
    def construct(self):
        ch = hb_chain()
        sp = ch.pts[SP]
        mn = minus_on(sp)
        self.play(Create(ch.links), LaggedStart(*[GrowFromCenter(b) for b in ch.beads], lag_ratio=0.08), FadeIn(hb_label(), shift=DOWN * 0.1), run_time=1.0)
        self.add(mn)
        ring = Circle(radius=0.82, color=TEXT, stroke_width=5).move_to(sp)
        self.play(Create(ring), run_time=0.4)
        self.at("break a protein")
        self.play(Indicate(VGroup(ch.beads[SP], mn), color=RED, scale_factor=1.5), ring.animate.set_stroke(width=8), run_time=0.9)
        self.at("How can a single")
        q = T("How can a single amino acid\nmatter that much?", size=46, line_spacing=0.9).move_to([0, -2.85, 0])
        self.play(FadeIn(q, shift=UP * 0.15), run_time=0.6)
        self.play(Indicate(VGroup(ch.beads[SP], mn), color=RED, scale_factor=1.4), run_time=0.8)
        self.finish()


def glu_tag(sp):
    name = T("Glu6", size=44, color=RED)
    tg = chip("charged", RED, size=36, pad=0.16)
    return VGroup(name, tg).arrange(RIGHT, buff=0.3).move_to(sp + UP * 1.6, aligned_edge=LEFT).shift(LEFT * 0.6)


def val_tag(sp):
    name = T("Val6", size=44, color=LG)
    tg = chip("oily (nonpolar)", OILY, size=36, pad=0.16)
    return VGroup(name, tg).arrange(RIGHT, buff=0.3).move_to(sp + UP * 1.6, aligned_edge=LEFT).shift(LEFT * 0.6)


class S02(SpokenScene):
    def construct(self):
        ch = hb_chain()
        sp = ch.pts[SP]
        mn = minus_on(sp)
        ring = Circle(radius=0.82, color=TEXT, stroke_width=8).move_to(sp)
        self.add(ch.group, mn, hb_label(), ring)
        self.at("sickle cell")
        sick = T("sickle cell anemia", size=46, color=RED, font=TITLE_FONT).move_to([2.6, 3.2, 0])
        self.play(FadeIn(sick, shift=DOWN * 0.1), run_time=0.7)
        self.at("one amino acid")
        self.play(Indicate(VGroup(ch.beads[SP], mn), color=RED, scale_factor=1.5), run_time=0.8)
        self.at("Glutamate at position")
        gt = glu_tag(sp)
        beta = T("beta-globin, position 6", size=38, color=LG).move_to([sp[0], -2.6, 0])
        arr = leader(beta.get_top() + UP * 0.05, sp + DOWN * 0.78)
        self.play(FadeIn(gt, shift=DOWN * 0.1), run_time=0.6)
        self.play(FadeIn(beta), GrowArrow(arr), run_time=0.6)
        self.at("becomes valine")
        vt = val_tag(sp)
        self.play(ch.beads[SP].animate.set_color(OILY), FadeOut(mn, scale=0.3), FadeTransform(gt, vt), run_time=1.0)
        self.finish()


# ------------------------------------------------------------------ 3. close-up: charged -> oily on the surface
class S03(SpokenScene):
    def construct(self):
        ch = hb_chain()
        sp0 = ch.pts[SP]
        ch.beads[SP].set_color(OILY)
        old = VGroup(ch.group, hb_label(), T("sickle cell anemia", size=46, color=RED, font=TITLE_FONT).move_to([2.6, 3.2, 0]),
                     Circle(radius=0.82, color=TEXT, stroke_width=8).move_to(sp0), val_tag(sp0),
                     T("beta-globin, position 6", size=38, color=LG).move_to([sp0[0], -2.6, 0]))
        self.add(old)
        self.play(FadeOut(old), run_time=0.35)
        c = np.array([-1.4, -0.35, 0])
        blob = Ellipse(width=8.2, height=5.9, stroke_color=BLUE, stroke_width=7, fill_color=BLUE, fill_opacity=0.14).move_to(c)
        name = T("hemoglobin", size=48).move_to(c + LEFT * 0.4)
        ang = 0.72
        sp = c + np.array([4.1 * np.cos(ang), 2.95 * np.sin(ang), 0])
        bead = Dot(sp, radius=0.62, color=RED).set_stroke(TEXT, 2, opacity=0.6).set_z_index(2)
        mn = Line(sp + LEFT * 0.27, sp + RIGHT * 0.27, color=BG, stroke_width=12).set_z_index(3)
        nm = T("Glu6", size=44, color=RED).move_to([4.6, 2.55, 0])
        tg = chip("charged", RED, size=36, pad=0.16).move_to([4.6, 1.65, 0])
        self.play(FadeIn(blob), FadeIn(name), GrowFromCenter(bead), FadeIn(mn), FadeIn(nm), FadeIn(tg), run_time=0.45)
        self.at("on the surface")
        edge = c + np.array([4.1 * np.cos(-0.12), 2.95 * np.sin(-0.12), 0])
        surf = T("outer surface", size=36, color=LG).move_to([4.75, -1.0, 0])
        arr = leader(surf.get_top() + UP * 0.05 + LEFT * 0.6, edge + RIGHT * 0.08)
        self.play(FadeIn(surf), GrowArrow(arr), run_time=0.45)
        self.at("an oily one")
        nm2 = T("Val6", size=44, color=LG).move_to(nm)
        tg2 = chip("oily (nonpolar)", OILY, size=36, pad=0.16).move_to([4.7, 1.65, 0])
        self.play(bead.animate.set_color(OILY), FadeOut(mn, scale=0.3), Transform(nm, nm2), FadeTransform(tg, tg2), run_time=0.7)
        self.finish()


# ------------------------------------------------------------------ 4. oxygen leaves, fibers form
class S04(SpokenScene):
    def construct(self):
        rng = np.random.RandomState(4)
        rows = [2.0, 0.35, -1.3]
        cols = [-3.6, -1.2, 1.2, 3.6]
        BW, BH = 2.5, 1.32
        blobs, oxs, rots = [], [], []
        for r_i, y in enumerate(rows):
            for c_i, x in enumerate(cols):
                sx = x * 1.25 + rng.uniform(-0.2, 0.2)
                sy = y * 1.12 + rng.uniform(-0.15, 0.15)
                rot = rng.uniform(-0.28, 0.28)
                b = Ellipse(width=BW, height=BH, stroke_color=BLUE, stroke_width=5, fill_color=BLUE, fill_opacity=0.2).rotate(rot).move_to([sx, sy, 0])
                o = VGroup(Dot(radius=0.13, color=TEXT), T("O2", size=30, color=TEXT)).arrange(RIGHT, buff=0.08).move_to([sx, sy, 0])
                blobs.append(b)
                oxs.append(o)
                rots.append(rot)
        lab_h = T("hemoglobin, carrying oxygen", size=36, color=LG).move_to([0, 3.35, 0])
        self.play(*[FadeIn(b, scale=0.8) for b in blobs], *[FadeIn(o) for o in oxs], FadeIn(lab_h), run_time=0.8)
        self.at("releases its oxygen")
        anims = []
        for o, b in zip(oxs, blobs):
            d = o.get_center() / (np.linalg.norm(o.get_center()) + 1e-6)
            anims.append(o.animate.shift(d * 1.3 + UP * 0.4).set_opacity(0))
        lab2 = T("hemoglobin, oxygen released", size=36, color=LG).move_to(lab_h)
        self.play(*anims, Transform(lab_h, lab2), run_time=1.3)
        self.at("sticks together")
        moves = []
        for i, b in enumerate(blobs):
            r_i, c_i = divmod(i, 4)
            moves.append(b.animate.rotate(-rots[i]).move_to([cols[c_i], rows[r_i], 0]))
        self.play(*moves, run_time=1.0, rate_func=smooth)
        self.at("long fibers")
        rods = VGroup(*[RoundedRectangle(corner_radius=0.66, width=4 * 2.4 + 0.35, height=BH + 0.3, stroke_color=RED, stroke_width=5).move_to([0, y, 0]) for y in rows])
        note = T("fibers form without oxygen", size=42, color=RED).move_to([0, -3.05, 0])
        self.play(FadeIn(note, shift=UP * 0.1), Create(rods), *[b.animate.set_color(RED).set_fill(RED, 0.2) for b in blobs], run_time=0.9)
        self.finish()


# ------------------------------------------------------------------ 5. sequence -> structure -> function
def big_box(text, color, x, y=0.7):
    box = RoundedRectangle(corner_radius=0.25, width=3.7, height=2.3, stroke_color=color, stroke_width=5, fill_color=color, fill_opacity=0.15)
    t = T(text, size=50, color=color)
    return VGroup(box, t.move_to(box)).move_to([x, y, 0])


class S05(SpokenScene):
    def construct(self):
        a = big_box("Sequence", BLUE, -4.55)
        b = big_box("Structure", GREEN, 0.0)
        c = big_box("Function", TEXT, 4.55)
        a1 = Arrow(a.get_right(), b.get_left(), buff=0.08, color=LG, stroke_width=8, max_tip_length_to_length_ratio=0.4)
        a2 = Arrow(b.get_right(), c.get_left(), buff=0.08, color=LG, stroke_width=8, max_tip_length_to_length_ratio=0.4)
        self.play(FadeIn(a, scale=0.9), run_time=0.5)
        self.at("changed the shape")
        self.play(GrowArrow(a1), FadeIn(b, shift=RIGHT * 0.2), run_time=0.6)
        self.at("changed the job")
        self.play(GrowArrow(a2), FadeIn(c, shift=RIGHT * 0.2), run_time=0.5)
        x = Cross(Square(side_length=1.3), stroke_color=RED, stroke_width=12).move_to([4.55, -1.55, 0])
        fl = T("function lost", size=42, color=RED).move_to([4.55, -2.85, 0])
        self.play(Create(x), FadeIn(fl, shift=UP * 0.1), c[0].animate.set_stroke(RED), run_time=0.6)
        self.finish()


# ------------------------------------------------------------------ 6. where is the shape stored?
BOXX = (-4.25, 0.0, 4.25)


def candidates():
    boxes = [RoundedRectangle(corner_radius=0.22, width=3.9, height=4.4, stroke_color=LG, stroke_width=4).move_to([x, -0.35, 0]) for x in BOXX]
    seq = Chain([(BOXX[0] - 1.3 + 0.65 * i, -0.35) for i in range(5)], r=0.3, colors=[BLUE, PURPLE, YELLOW, BLUE, PURPLE], link_w=7).group
    helper = Ellipse(width=2.8, height=2.0, stroke_color=BLUE, stroke_width=6, fill_color=BLUE, fill_opacity=0.2).move_to([0, -0.35, 0])
    cell = VGroup(Circle(radius=1.35, stroke_color=LG, stroke_width=5, fill_color=GREY, fill_opacity=0.12),
                  Circle(radius=0.45, stroke_color=LG, stroke_width=4)).move_to([BOXX[2], -0.35, 0])
    labs = [T(s, size=36).move_to([x, -3.15, 0]) for s, x in (("the sequence", BOXX[0]), ("a helper protein", BOXX[1]), ("the cell", BOXX[2]))]
    return boxes, [seq, helper, cell], labs


def where_q():
    return T("Where is the shape stored?", size=56, font=TITLE_FONT).move_to([0, 3.0, 0])


class S06(SpokenScene):
    def construct(self):
        q = where_q()
        boxes, icons, labs = candidates()
        self.play(FadeIn(q, shift=DOWN * 0.1), LaggedStart(*[FadeIn(VGroup(b, i, l), scale=0.94) for b, i, l in zip(boxes, icons, labs)], lag_ratio=0.2), run_time=1.3)
        self.at("stored precisely")
        self.play(*[Indicate(i, scale_factor=1.1, color=i.get_color()) for i in icons], run_time=0.9)
        self.at("But where")
        qm = VGroup(*[T("?", size=80, color=TEXT, font=TITLE_FONT).move_to([x + 1.45, 1.2, 0]) for x in BOXX])
        self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.1) for m in qm], lag_ratio=0.2), run_time=0.7)
        self.finish()


# ------------------------------------------------------------------ 7-8. primary structure (serpentine chain, 15 beads)
SROWS = [1.5, -0.1, -1.7]


def serp_pts():
    pts = []
    for i in range(15):
        r, c = divmod(i, 5)
        x = -4.4 + 2.2 * c if r % 2 == 0 else 4.4 - 2.2 * c
        pts.append((x, SROWS[r]))
    return pts


def seq_chain(colors=None):
    return Chain(serp_pts(), r=0.48, colors=colors, link_w=8)


def termini(ch):
    n = T("N-terminus", size=36, color=LG).move_to(ch.pts[0] + UP * 0.85)
    c = T("C-terminus", size=36, color=LG).move_to(ch.pts[-1] + DOWN * 0.85)
    return n, c


def ps_title():
    return T("primary structure = the sequence", size=48, font=TITLE_FONT).move_to([0, 3.2, 0])


class S07(SpokenScene):
    def construct(self):
        boxes, icons, labs = candidates()
        old = VGroup(*[VGroup(b, i, l) for b, i, l in zip(boxes, icons, labs)], where_q(),
                     *[T("?", size=80, color=TEXT, font=TITLE_FONT).move_to([x + 1.45, 1.2, 0]) for x in BOXX])
        self.add(old)
        ch = seq_chain(colors=[BLUE] * 15)
        self.play(FadeOut(old), run_time=0.4)
        self.play(Create(ch.links), LaggedStart(*[GrowFromCenter(b) for b in ch.beads], lag_ratio=0.06), run_time=1.1)
        n, c = termini(ch)
        self.play(FadeIn(n), FadeIn(c), run_time=0.4)
        self.at("primary structure")
        ps = ps_title()
        self.play(FadeIn(ps, shift=DOWN * 0.1), run_time=0.7)
        self.at("order of its amino acids")
        self.play(LaggedStart(*[b.animate.set_color(SEQ[i]) for i, b in enumerate(ch.beads)], lag_ratio=0.08), run_time=1.4)
        self.at("linked end to end")
        self.play(ch.links.animate.set_color(ORANGE).set_stroke(width=12), run_time=0.8)
        self.at("peptide bonds")
        mid = (ch.pts[10] + ch.pts[11]) / 2
        pl = T("peptide bond", size=36, color=ORANGE).move_to([mid[0], -3.05, 0])
        arr = leader(pl.get_top() + UP * 0.05, mid + DOWN * 0.12, ORANGE)
        self.play(FadeIn(pl), GrowArrow(arr), run_time=0.6)
        self.finish()


class S08(SpokenScene):
    def construct(self):
        ch = seq_chain()
        ch.links.set_color(ORANGE).set_stroke(width=12)
        n, c = termini(ch)
        ps = ps_title()
        mid = (ch.pts[10] + ch.pts[11]) / 2
        pl = T("peptide bond", size=36, color=ORANGE).move_to([mid[0], -3.05, 0])
        arr = leader(pl.get_top() + UP * 0.05, mid + DOWN * 0.12, ORANGE)
        self.add(ch.group, n, c, ps, pl, arr)
        self.at("exact")
        ring = Circle(radius=0.66, color=TEXT, stroke_width=6).move_to(ch.pts[0])
        self.play(FadeOut(pl), FadeOut(arr), FadeIn(ring), run_time=0.3)
        path = VMobject().set_points_as_corners(ch.pts)
        self.play(MoveAlongPath(ring, path), run_time=1.6, rate_func=linear)
        self.play(FadeOut(ring), run_time=0.3)
        self.at("Insulin")
        ins = T("insulin", size=56, font=TITLE_FONT).move_to([-3.7, 3.2, 0])
        anchor = np.array([1.75, 3.2, 0])
        num = M("1", size=72, color=TEXT).move_to(anchor, aligned_edge=RIGHT)
        res = T("residues", size=46, color=TEXT).next_to(anchor, RIGHT, buff=0.25)
        sch = T("schematic: not all 51 beads drawn", size=36, color=LG).move_to([2.35, 2.45, 0])
        self.play(FadeOut(ps), FadeIn(ins), FadeIn(num), FadeIn(res), FadeIn(sch), run_time=0.5)
        t_end = self.t_of("51 residues") - self.elapsed()
        self.play(UpdateFromAlphaFunc(num, lambda m, a: m.become(M(str(max(1, int(round(1 + 50 * a)))), size=72, color=TEXT).move_to(anchor, aligned_edge=RIGHT))),
                  run_time=max(0.6, t_end), rate_func=linear)
        self.play(Indicate(num, color=GREEN, scale_factor=1.15), run_time=0.6)
        self.at("one defined order")
        d = T("in one defined order", size=44, color=TEXT).move_to([-0.6, -3.1, 0])
        self.play(FadeIn(d, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ------------------------------------------------------------------ 9. Anfinsen and ribonuclease
RN = dict(pos=[0, 0.25, 0], k=2.45, stroke=10)


def anf_name():
    return T("Christian Anfinsen", size=56, font=TITLE_FONT).move_to([0, 3.25, 0])


def rn_labels(e):
    rn = T("ribonuclease", size=42, color=BLUE).move_to([0, -2.6, 0])
    ss = T("4 disulfide bonds", size=38, color=GOLD).move_to([0, -3.35, 0])
    a, b = e.bpts[3]
    tag = T("S–S", size=44, color=GOLD).move_to([4.5, 1.2, 0])
    ld = leader(tag.get_left() + LEFT * 0.08, (a + b) / 2 + RIGHT * 0.12, GOLD)
    return rn, ss, VGroup(tag, ld)


class S09(SpokenScene):
    def construct(self):
        nm = anf_name()
        e = Enz("native", bridges=True, **RN)
        self.play(FadeIn(nm, shift=DOWN * 0.1), FadeIn(e.blob), Create(e.chain), run_time=1.0)
        rn, ss, sst = rn_labels(e)
        self.at("ribonuclease")
        self.play(FadeIn(rn, shift=UP * 0.1), run_time=0.5)
        self.at("four disulfide bonds")
        self.play(LaggedStart(*[FadeIn(b, scale=0.6) for b in e.bridges], lag_ratio=0.3), FadeIn(ss, shift=UP * 0.1), FadeIn(sst[0]), GrowArrow(sst[1]), run_time=1.2)
        self.finish()


# ------------------------------------------------------------------ 10. tube one
class S10(SpokenScene):
    def construct(self):
        e = Enz("native", bridges=True, **RN)
        rn, ss, sst = rn_labels(e)
        nm = anf_name()
        self.add(nm, e.group, rn, ss, sst)
        kits = [Kit(x) for x in TX]
        gl = [k.glass() for k in kits]
        lq = [k.liquid() for k in kits]
        lb = [k.label(i + 1) for i, k in enumerate(kits)]
        k1 = kits[0]
        tiny = k1.enz("native", bridges=True)
        m1 = k1.meter(100)
        self.play(FadeOut(nm), FadeOut(rn), FadeOut(ss), FadeOut(sst), *[FadeIn(g) for g in gl], *[FadeIn(q) for q in lq], *[FadeIn(l) for l in lb],
                  FadeIn(m1), Transform(e.blob, tiny.blob), Transform(e.chain, tiny.chain), Transform(e.bridges, tiny.bridges), run_time=1.1)
        self.at("working enzyme")
        self.play(Indicate(VGroup(e.chain, e.bridges), color=BLUE, scale_factor=1.12), run_time=0.8)
        self.at("activity is full")
        self.play(Indicate(m1, color=GREEN, scale_factor=1.12), run_time=0.8)
        self.finish()


# ------------------------------------------------------------------ 11-12. tube two: urea + reducing agent
def rack(scene):
    kits = [Kit(x) for x in TX]
    d = {"kits": kits, "glass": [k.glass() for k in kits], "liq": [k.liquid() for k in kits], "lab": [k.label(i + 1) for i, k in enumerate(kits)]}
    scene.add(*d["glass"], *d["liq"], *d["lab"])
    return d


class S11(SpokenScene):
    def construct(self):
        d = rack(self)
        k1, k2, k3 = d["kits"]
        e1 = k1.enz("native", bridges=True)
        self.add(e1.group, k1.meter(100))
        e2 = k2.enz("native", bridges=True)
        m2 = k2.meter(100)
        self.play(FadeIn(k1.veil()), FadeIn(k3.veil()), FadeIn(e2.group), FadeIn(m2), run_time=0.6)
        urea, ua, red, ra = rack_reagents()
        self.at("added urea")
        self.play(FadeIn(urea, shift=DOWN * 0.1), GrowArrow(ua), run_time=0.6)
        self.at("a reducing agent")
        self.play(FadeIn(red, shift=DOWN * 0.1), GrowArrow(ra), run_time=0.6)
        self.at("The reducing agent")
        self.play(Indicate(red, color=RED, scale_factor=1.12), e2.bridges.animate.set_color(RED), run_time=0.9)
        self.at("broke the disulfide bonds")
        halves, anims = [], []
        for a, b in e2.bpts:
            u = (b - a) / np.linalg.norm(b - a)
            m = (a + b) / 2
            la, lb_ = Line(a, m - u * 0.03, color=RED, stroke_width=7), Line(m + u * 0.03, b, color=RED, stroke_width=7)
            halves += [la, lb_]
            anims += [la.animate.shift(-u * 0.3).set_opacity(0), lb_.animate.shift(u * 0.3).set_opacity(0)]
        self.remove(e2.bridges)
        self.add(*halves)
        self.play(*anims, run_time=0.8)
        self.at("Urea pulled")
        c2 = k2.enz("coil")
        self.remove(m2)
        holder, anim = meter_anim(k2, 100, 0, 1.5)
        self.add(holder)
        self.play(Transform(e2.chain, c2.chain), e2.blob.animate.set_stroke(opacity=0).set_fill(opacity=0), anim, Indicate(urea, scale_factor=1.12), run_time=1.5)
        self.finish()


class S12(SpokenScene):
    def construct(self):
        d = rack(self)
        k1, k2, k3 = d["kits"]
        e2 = k2.enz("coil")
        m2 = k2.meter(0)
        self.add(k1.enz("native", bridges=True).group, k1.meter(100), e2.chain, m2, k1.veil(), k3.veil())
        urea, ua, red, ra = rack_reagents()
        self.add(urea, ua, red, ra)
        self.at("Activity fell")
        self.play(Indicate(m2, color=RED, scale_factor=1.2), run_time=1.0)
        self.at("random coil")
        rc = random_coil_label(k2)
        self.play(FadeIn(rc[0], shift=LEFT * 0.1), GrowArrow(rc[1]), e2.chain.animate.set_color(RED), run_time=0.7)
        self.finish()


def random_coil_label(k2):
    t = T("random\ncoil", size=40, color=RED, line_spacing=0.85).move_to(k2.P(2.4, -0.2))
    return VGroup(t, leader(t.get_left() + LEFT * 0.08, k2.P(0.95, -0.35), RED))


# ------------------------------------------------------------------ 13. tube three: wash it away (tube 3 to the middle)
KN = dict(cx=0.0, cy=-0.35, k=1.12, side_label=True)


def nohelper():
    icon = Ellipse(width=1.6, height=1.1, stroke_color=BLUE, stroke_width=5, fill_color=BLUE, fill_opacity=0.2).move_to([-4.75, 0.75, 0])
    x = Cross(Square(side_length=1.15), stroke_color=RED, stroke_width=9).move_to(icon)
    t = T("no helper\nproteins", size=36, color=TEXT, line_spacing=0.9).move_to([-4.75, -0.75, 0])
    return VGroup(icon, x, t)


def buffer_air(kn):
    bf = T("buffer", size=38, color=TEAL).move_to([3.1, 0.35, 0])
    ba = leader(bf.get_left() + LEFT * 0.08, kn.P(0.6, 0.65), TEAL)
    air = T("air", size=38, color=LG).move_to([3.1, 1.5, 0])
    aa = leader(air.get_left() + LEFT * 0.08, kn.P(0.6, 1.75))
    return VGroup(bf, ba), VGroup(air, aa)


class S13(SpokenScene):
    def construct(self):
        d = rack(self)
        k1, k2, k3 = d["kits"]
        e1 = k1.enz("native", bridges=True)
        m1 = k1.meter(100)
        e2 = k2.enz("coil")
        e2.chain.set_color(RED)
        m2 = k2.meter(0)
        v1, v3 = k1.veil(), k3.veil()
        urea, ua, red, ra = rack_reagents()
        rc = random_coil_label(k2)
        self.add(ua, ra, e1.group, m1, e2.chain, m2, v1, v3, urea, red, rc)
        self.at("tube three")
        kn = Kit(**KN)
        cn = kn.enz("coil")
        cn.chain.set_color(RED)
        u_to = urea.copy().move_to([3.9, 0.55, 0])
        r_to = red.copy().move_to([3.9, -0.55, 0])
        keep = (d["glass"][2], d["liq"][2], d["lab"][2], e2.chain, urea, red)
        fade = [m for m in self.mobjects if m not in keep]
        self.play(*[FadeOut(m) for m in fade],
                  Transform(d["glass"][2], kn.glass()), Transform(d["liq"][2], kn.liquid()), Transform(d["lab"][2], kn.label(3)),
                  Transform(e2.chain, cn.chain), Transform(urea, u_to), Transform(red, r_to), run_time=0.9)
        self.at("washed the chemicals away")
        self.play(urea.animate.shift(DOWN * 4.0).set_opacity(0), red.animate.shift(DOWN * 4.0).set_opacity(0),
                  e2.chain.animate.set_color(BLUE), run_time=1.4, rate_func=rush_into)
        self.at("No other proteins")
        nh = nohelper()
        self.play(FadeIn(nh[0]), FadeIn(nh[2]), run_time=0.4)
        self.play(Create(nh[1]), run_time=0.4)
        self.at("Just the chain")
        self.play(Indicate(e2.chain, color=BLUE, scale_factor=1.12), run_time=0.7)
        bf, air = buffer_air(kn)
        self.at("a buffer")
        self.play(FadeIn(bf[0]), GrowArrow(bf[1]), run_time=0.35)
        self.at("and air")
        self.play(FadeIn(air[0]), GrowArrow(air[1]), run_time=0.35)
        self.finish()


# ------------------------------------------------------------------ 14-15. the test, and the pause
def question_text():
    q = T("If the cell's machinery stored the shape,\nwhat would tube 3 show?", size=44, line_spacing=0.9)
    fit(q, max_w=10.2)
    return q.move_to([-1.0, 2.85, 0])


RING_C = np.array([5.55, 2.8, 0])


class S14(SpokenScene):
    def construct(self):
        kn = Kit(**KN)
        e = kn.enz("coil")
        nh = nohelper()
        bf, air = buffer_air(kn)
        self.add(kn.glass(), kn.liquid(), kn.label(3), e.chain, nh, bf, air)
        self.at("the test")
        self.play(FadeOut(nh), FadeOut(bf), FadeOut(air), Indicate(e.chain, color=BLUE, scale_factor=1.1), run_time=0.8)
        self.at("If the cells")
        q = question_text()
        self.play(FadeIn(q, shift=DOWN * 0.1), run_time=0.8)
        self.at("what would")
        self.play(FadeIn(kn.meter(None)), run_time=0.5)
        self.finish()


class S15Pause(NarratedScene):
    def construct(self):
        kn = Kit(**KN)
        self.add(kn.glass(), kn.liquid(), kn.label(3), kn.enz("coil").chain, kn.meter(None), question_text())
        R = 0.92
        ring_bg = Circle(radius=R, stroke_color=GREY, stroke_width=6).move_to(RING_C)
        tr = ValueTracker(0)
        arc = always_redraw(lambda: Arc(radius=R, start_angle=PI / 2, angle=-TAU * (1 - tr.get_value()) + 1e-3, arc_center=RING_C,
                                        stroke_color=TEAL, stroke_width=10))
        num = always_redraw(lambda: M(str(max(1, int(np.ceil(5 * (1 - tr.get_value()) - 1e-6)))), size=50, color=TEXT).move_to(RING_C))
        self.add(ring_bg, arc, num)
        self.play(tr.animate.set_value(1.0), run_time=self.narration_s, rate_func=linear)
        self.finish()


# ------------------------------------------------------------------ 16. it refolds by itself
class S16(SpokenScene):
    def construct(self):
        kn = Kit(**KN)
        e = kn.enz("coil")
        m = kn.meter(None)
        q = question_text()
        R = 0.92
        ring = VGroup(Circle(radius=R, stroke_color=GREY, stroke_width=6).move_to(RING_C), M("1", size=50).move_to(RING_C))
        self.add(kn.glass(), kn.liquid(), kn.label(3), e.chain, e.blob, m, q, ring)
        self.play(FadeOut(q), FadeOut(ring), run_time=0.5)
        self.at("refolded")
        nat = kn.enz("native", bridges=True)
        self.play(Transform(e.chain, nat.chain), e.blob.animate.set_stroke(opacity=1).set_fill(opacity=0.14), run_time=1.0, rate_func=smooth)
        self.play(LaggedStart(*[Create(b) for b in nat.bridges], lag_ratio=0.2), run_time=0.6)
        self.at("full activity")
        self.remove(m)
        holder, anim = meter_anim(kn, 0.0001, 100, 0.9)
        self.add(holder)
        self.play(anim)
        holder.become(kn.meter(100))
        self.at("No helper")
        nh = nohelper()
        self.play(FadeIn(nh[0]), FadeIn(nh[2]), Create(nh[1]), run_time=0.6)
        self.at("only its own sequence")
        self.play(Indicate(e.chain, color=BLUE, scale_factor=1.12), run_time=0.8)
        self.at("that buffer")
        bf, air = buffer_air(kn)
        self.play(FadeIn(bf[0]), GrowArrow(bf[1]), run_time=0.4)
        self.finish()


# ------------------------------------------------------------------ 17-18. eight cysteines, 105 pairings
CYS = [26, 40, 58, 65, 72, 84, 95, 110]
CX = [-6.0 + 12.0 * (r - 1) / 123.0 for r in CYS]
CY = -0.9
NATIVE = ((0, 5), (1, 6), (2, 7), (3, 4))


def cys_dots():
    return VGroup(*[Dot([x, CY, 0], radius=0.24, color=GOLD).set_z_index(3) for x in CX])


def cys_line():
    return Line([-6.2, CY, 0], [6.2, CY, 0], color=BLUE, stroke_width=10)


def cys_labels():
    a = T("8 cysteines", size=46, color=GOLD)
    b = T("105 possible pairings", size=46, color=TEXT)
    return VGroup(a, b).arrange(RIGHT, buff=1.0).move_to([0, -2.1, 0])


def arc_pair(i, j, color=GOLD, op=0.6, w=5):
    i, j = sorted((i, j))
    a, b = np.array([CX[i], CY + 0.24, 0]), np.array([CX[j], CY + 0.24, 0])
    return ArcBetweenPoints(a, b, angle=-2.7, stroke_color=color, stroke_width=w, stroke_opacity=op)


def random_matching(rng):
    p = list(rng.permutation(8))
    return VGroup(*[arc_pair(p[2 * i], p[2 * i + 1]) for i in range(4)])


class S17(SpokenScene):
    def construct(self):
        rng = np.random.RandomState(17)
        line, dots, labs = cys_line(), cys_dots(), cys_labels()
        self.play(Create(line), LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.08), FadeIn(labs), run_time=0.7)
        self.at("disulfides")
        cur = None
        while self.elapsed() < self.narration_s + 0.2:
            new = random_matching(rng)
            if cur is not None:
                self.remove(cur)
            self.add(new)
            cur = new
            self.wait(0.33)
        self.finish()


class S18(SpokenScene):
    def construct(self):
        rng = np.random.RandomState(18)
        line, dots, labs = cys_line(), cys_dots(), cys_labels()
        self.add(line, dots, labs)
        cur = None
        t_stop = self.t_of("less than one time") - 0.2
        while self.elapsed() < t_stop - 0.15:
            new = random_matching(rng)
            if cur is not None:
                self.remove(cur)
            self.add(new)
            cur = new
            self.wait(0.33)
        if cur is not None:
            self.play(cur.animate.set_stroke(opacity=0.15), run_time=0.2)
        chance = T("random chance < 1%", size=50, color=RED).move_to([0, -3.15, 0])
        self.play(FadeIn(chance, shift=UP * 0.1), run_time=0.5)
        self.at("Yet the chain")
        native = VGroup(*[arc_pair(i, j, GOLD, 1.0, 8) for i, j in NATIVE])
        glow = VGroup(*[arc_pair(i, j, GOLD, 0.25, 18) for i, j in NATIVE])
        self.play(FadeOut(cur), FadeIn(glow), LaggedStart(*[Create(a) for a in native], lag_ratio=0.15), run_time=0.9)
        self.at("correct partners")
        self.play(Indicate(dots, color=GOLD, scale_factor=1.25), run_time=0.8)
        self.finish()


# ------------------------------------------------------------------ 19. Anfinsen's conclusion
class S19(SpokenScene):
    def construct(self):
        old = VGroup(cys_line(), cys_dots(), cys_labels(), T("random chance < 1%", size=50, color=RED).move_to([0, -3.15, 0]),
                     *[arc_pair(i, j, GOLD, 1.0, 8) for i, j in NATIVE], *[arc_pair(i, j, GOLD, 0.25, 18) for i, j in NATIVE])
        self.add(old)
        self.play(FadeOut(old), run_time=0.4)
        hd = quote_head()
        q = quote_lines().move_to([0, 0.1, 0])
        self.play(FadeIn(hd, shift=DOWN * 0.1), FadeIn(q[0], shift=UP * 0.15), run_time=0.6)
        self.at("amino acid sequence")
        self.play(FadeIn(q[1], shift=UP * 0.15), run_time=0.6)
        self.at("in a given environment")
        self.play(FadeIn(q[2], shift=UP * 0.15), run_time=0.6)
        u = Line(q[2].get_corner(DL) + DOWN * 0.12, q[2].get_corner(DR) + DOWN * 0.12, color=TEAL, stroke_width=6)
        self.play(Create(u), q[2].animate.set_color(TEAL), run_time=0.6)
        self.finish()


# ------------------------------------------------------------------ 20. the fold is the lowest free energy
BASE = -2.8
BOWL0 = -0.9


def bowl_y(x):
    return BOWL0 + 0.22 * x * x


class S20(SpokenScene):
    def construct(self):
        ax_x = Arrow([-5.0, BASE, 0], [5.6, BASE, 0], buff=0, color=LG, stroke_width=4, max_tip_length_to_length_ratio=0.03)
        ax_y = Arrow([-5.0, BASE, 0], [-5.0, 3.0, 0], buff=0, color=LG, stroke_width=4, max_tip_length_to_length_ratio=0.04)
        yl = T("free energy", size=36, color=LG).rotate(PI / 2).next_to(ax_y, LEFT, buff=0.25)
        xl = T("conformation", size=36, color=LG).next_to(ax_x, DOWN, buff=0.15)
        curve = ParametricFunction(lambda t: np.array([t, bowl_y(t), 0]), t_range=[-4.1, 4.1, 0.02], color=BLUE, stroke_width=8)
        hedge = T("for most small proteins", size=40, color=TEXT).move_to([0, 3.3, 0])
        x0 = -3.8
        ball = Dot([x0, bowl_y(x0) + 0.24, 0], radius=0.24, color=YELLOW).set_z_index(5)
        self.play(FadeIn(VGroup(ax_x, ax_y, yl, xl)), Create(curve), FadeIn(hedge), FadeIn(ball, scale=0.5), run_time=0.8)
        self.at("the fold is")
        tx = ValueTracker(0.0)

        def xb(s):   # damped roll from the left wall into the bottom
            return x0 * np.exp(-2.2 * s) * np.cos(2.6 * s)
        ball.add_updater(lambda b: b.move_to([xb(tx.get_value()), bowl_y(xb(tx.get_value())) + 0.24, 0]))
        self.play(tx.animate.set_value(2.2), run_time=1.6, rate_func=linear)
        ball.clear_updaters()
        self.play(ball.animate.move_to([0, bowl_y(0) + 0.24, 0]), run_time=0.15)
        self.at("state the chain")
        nl = T("native fold", size=40, color=GREEN).move_to([0, -1.6, 0])
        lf = T("lowest free energy", size=36, color=TEXT).move_to([0, -2.22, 0])
        self.play(ball.animate.set_color(GREEN), FadeIn(nl, shift=UP * 0.1), FadeIn(lf, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ------------------------------------------------------------------ 21. free energy is a trade
class S21(SpokenScene):
    def construct(self):
        piv = np.array([0.0, 1.9, 0.0])
        L = 4.3
        HANG = 1.7
        ang = ValueTracker(0.0)

        def endL():
            return piv + np.array([-L * np.cos(ang.get_value()), L * np.sin(ang.get_value()), 0])

        def endR():
            return piv + np.array([L * np.cos(ang.get_value()), -L * np.sin(ang.get_value()), 0])

        stand = VGroup(Line(piv, [0, -3.3, 0], color=LG, stroke_width=9), Line([-1.4, -3.3, 0], [1.4, -3.3, 0], color=LG, stroke_width=9),
                       Triangle(color=LG, fill_opacity=1).scale(0.25).move_to(piv + DOWN * 0.15))
        beam = always_redraw(lambda: Line(endL(), endR(), color=TEXT, stroke_width=9))

        def pan(end_fn):
            def f():
                e = end_fn()
                bot = e + DOWN * HANG
                return VGroup(Line(e, bot + LEFT * 1.6, color=LG, stroke_width=3), Line(e, bot + RIGHT * 1.6, color=LG, stroke_width=3),
                              Line(bot + LEFT * 1.75, bot + RIGHT * 1.75, color=TEXT, stroke_width=7))
            return always_redraw(f)

        pl, pr = pan(endL), pan(endR)
        hd = T("Free energy: a trade", size=48, font=TITLE_FONT).move_to([0, 3.35, 0])
        self.play(FadeIn(hd, shift=DOWN * 0.1), FadeIn(stand), FadeIn(beam), FadeIn(pl), FadeIn(pr), run_time=0.8)
        S = 1.05
        wl = Square(side_length=S, stroke_width=0, fill_color=BLUE, fill_opacity=0.9)
        wr1 = Square(side_length=S, stroke_width=0, fill_color=GREEN, fill_opacity=0.9)
        wr2 = Square(side_length=S, stroke_width=0, fill_color=TEAL, fill_opacity=0.9)
        ll = T("freedom\ngiven up", size=36, color=BLUE, line_spacing=0.9)
        lr1 = T("contacts made", size=36, color=GREEN)
        lr2 = T("water freed", size=36, color=TEAL)

        def ride(m, end_fn, off):
            m.add_updater(lambda mm: mm.move_to(end_fn() + off))
            m.update()
            return m
        ride(wl, endL, DOWN * (HANG - S / 2 - 0.05))
        ride(ll, endL, DOWN * (HANG + 0.75))
        ride(wr1, endR, DOWN * (HANG - S / 2 - 0.05) + LEFT * 0.6)
        ride(wr2, endR, DOWN * (HANG - S / 2 - 0.05) + RIGHT * 0.6)
        ride(lr1, endR, DOWN * (HANG + 0.5))
        ride(lr2, endR, DOWN * (HANG + 1.1))
        self.at("gives up freedom")
        self.play(FadeIn(wl, shift=DOWN * 0.3), FadeIn(ll), run_time=0.6)
        self.play(ang.animate.set_value(-0.07), run_time=0.6)
        self.at("favorable contacts")
        self.play(FadeIn(wr1, shift=DOWN * 0.3), FadeIn(lr1), run_time=0.5)
        self.play(ang.animate.set_value(0.0), run_time=0.5)
        self.at("freer water")
        self.play(FadeIn(wr2, shift=DOWN * 0.3), FadeIn(lr2), run_time=0.5)
        self.play(ang.animate.set_value(0.11), run_time=0.8, rate_func=smooth)
        self.finish()


# ------------------------------------------------------------------ 22. keep those words in mind
class S22(SpokenScene):
    def construct(self):
        q = quote_lines().move_to([0, 0.1, 0])
        u = Line(q[2].get_corner(DL) + DOWN * 0.12, q[2].get_corner(DR) + DOWN * 0.12, color=TEAL, stroke_width=6)
        q[2].set_color(TEAL)
        hd = quote_head()
        self.add(hd, q, u)
        self.play(q[0].animate.set_opacity(0.3), q[1].animate.set_opacity(0.3), hd.animate.set_opacity(0.3), run_time=0.8)
        self.at("in a given environment")
        self.play(Indicate(VGroup(q[2], u), color=TEAL, scale_factor=1.08), run_time=0.8)
        self.at("They will matter")
        pn = pinned()
        pn[0].set_color(TEAL)
        self.play(FadeOut(q[0]), FadeOut(q[1]), FadeOut(hd), run_time=0.35)
        self.play(Transform(q[2], pn[0]), Transform(u, pn[1]), run_time=0.8)
        self.finish()


# ------------------------------------------------------------------ 23-24. three questions
CARDS = [("Which shapes\nare possible?", -4.3), ("What picks\none?", 0.0), ("How is it\nfound so fast?", 4.3)]
CTOP = 2.55


def card(i, text, color=LG, x=0.0, h=5.6):
    box = RoundedRectangle(corner_radius=0.22, width=3.95, height=h, stroke_color=color, stroke_width=5, fill_color=BG, fill_opacity=1)
    box.move_to([x, CTOP - h / 2, 0])
    num = T(str(i), size=72, color=color, font=TITLE_FONT).move_to([x, CTOP - 0.75, 0])
    txt = VGroup(*[T(ln, size=40, color=TEXT) for ln in text.split("\n")]).arrange(DOWN, buff=0.18)
    txt.move_to([x, CTOP - 0.75 - (h - 0.75) / 2 - 0.1, 0])
    return VGroup(box, num, txt)


def pinned_teal():
    pn = pinned()
    pn[0].set_color(TEAL)
    return pn


class S23(SpokenScene):
    def construct(self):
        pn = pinned_teal()
        self.add(pn)
        cards = [card(i + 1, t, LG, x) for i, (t, x) in enumerate(CARDS)]
        self.at("Three questions")
        self.play(LaggedStart(*[FadeIn(c[1], shift=UP * 0.2) for c in cards], lag_ratio=0.25), run_time=0.9)
        for c, ph in zip(cards, ("Which shapes", "What picks one", "how is it found")):
            self.at(ph)
            self.play(Create(c[0]), FadeIn(c[2], shift=UP * 0.1), run_time=0.6)
            c[1].set_z_index(2)
            c[2].set_z_index(2)
        self.finish()


def answers():
    g = T("Geometry allows", size=40, color=ORANGE).move_to([-4.3, -2.3, 0])
    w = T("Water chooses", size=40, color=TEAL).move_to([0.0, -3.05, 0])
    ga = leader(g.get_top() + UP * 0.05, [-4.3, CTOP - 3.9 - 0.05, 0], ORANGE, 5)
    wa = leader(w.get_top() + UP * 0.05, [0.0, CTOP - 3.9 - 0.05, 0], TEAL, 5)
    box = DashedVMobject(RoundedRectangle(corner_radius=0.2, width=3.95, height=1.3, stroke_color=TEXT, stroke_width=4), num_dashes=44)
    box.move_to([4.3, -2.7, 0])
    open_t = VGroup(T("needs one", size=36, color=TEXT), T("more idea", size=36, color=TEXT)).arrange(DOWN, buff=0.12).move_to(box)
    return VGroup(g, ga), VGroup(w, wa), VGroup(box, open_t)


class S24(SpokenScene):
    def construct(self):
        pn = pinned_teal()
        cards = [card(i + 1, t, LG, x) for i, (t, x) in enumerate(CARDS)]
        for c in cards:
            c.set_z_index(1)
        self.add(pn, *cards)
        self.at("first two")
        small = [card(i + 1, t, TEXT if i < 2 else LG, x, h=3.9) for i, (t, x) in enumerate(CARDS)]
        small[2][1:].set_opacity(0.35)
        small[2][0].set_stroke(opacity=0.35)
        self.play(*[Transform(c, s) for c, s in zip(cards, small)], run_time=0.8)
        ga, wa, op = answers()
        self.at("Geometry allows")
        self.play(FadeIn(ga[0], shift=UP * 0.15), GrowArrow(ga[1]), cards[0][0].animate.set_stroke(ORANGE, 6), cards[0][1].animate.set_color(ORANGE), run_time=0.8)
        self.at("Water drives")
        self.play(FadeIn(wa[0], shift=UP * 0.15), GrowArrow(wa[1]), cards[1][0].animate.set_stroke(TEAL, 6), cards[1][1].animate.set_color(TEAL), run_time=0.8)
        self.at("third question")
        self.play(cards[2][0].animate.set_stroke(TEXT, 6, opacity=1), cards[2][1].animate.set_color(TEXT).set_opacity(1),
                  cards[2][2].animate.set_opacity(1), run_time=0.6)
        self.at("one more idea")
        self.play(Create(op[0]), FadeIn(op[1]), run_time=0.7)
        self.finish()


# ------------------------------------------------------------------ 25. the sequence holds the shape
HEAD = ("The shape of a protein", "is written in its sequence.")


class S25(SpokenScene):
    def construct(self):
        small = [card(i + 1, t, c, x, h=3.9) for i, ((t, x), c) in enumerate(zip(CARDS, (ORANGE, TEAL, TEXT)))]
        ga, wa, op = answers()
        old = VGroup(pinned_teal(), *small, ga, wa, op)
        self.add(old)
        self.play(FadeOut(old), run_time=0.4)
        a = T(HEAD[0], size=58, font=TITLE_FONT)
        b = T(HEAD[1], size=58, font=TITLE_FONT)
        VGroup(a, b).arrange(DOWN, buff=0.35).move_to([0, 1.5, 0])
        self.play(FadeIn(a, shift=UP * 0.1), run_time=0.4)
        self.at("written in")
        self.play(FadeIn(b, shift=UP * 0.1), run_time=0.4)
        self.at("its sequence")
        ch = Chain(wave_pts(13, -5.6, 5.6, -1.7, 0.45), r=0.36)
        self.play(Create(ch.links), LaggedStart(*[GrowFromCenter(x) for x in ch.beads], lag_ratio=0.05), run_time=0.8)
        self.finish()


class S26End(EndCard):
    LINE = "The shape of a protein is written in its sequence."
    LINE2 = "In the right buffer, it refolds with no helper."

    def construct(self):
        l1 = T(self.LINE, size=44, font=TITLE_FONT)
        l2 = T(self.LINE2, size=44, font=TITLE_FONT)
        s = min(12.2 / l1.width, 12.2 / l2.width)
        l1.scale(s)
        l2.scale(s)
        sub = T("biochemistrypedia.com", size=36, color=TEAL)
        g = VGroup(l1, l2, sub).arrange(DOWN, buff=0.45)
        g[2].shift(DOWN * 0.25)
        self.play(FadeIn(l1, shift=UP * 0.15), FadeIn(l2, shift=UP * 0.15), run_time=self.beat(0.3))
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        self.finish()
