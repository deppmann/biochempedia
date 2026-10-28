"""Endocytosis and signaling endosomes: sealed inside, a receptor goes silent  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = the receptor (a bar through the membrane; the head is outside the cell or inside an endosome,
           the longer half is the tail, in the cytosol)
  GREEN  = signal on (a tail that can reach its partners)
  RED    = signal off / cut off (a sealed tail, a blocked route)
  PURPLE = partner proteins in the cytosol (round blobs on the tail), and Cbl, the enzyme that adds the tag
  ORANGE = the way in: the sequence on the tail, the adaptor, the clathrin coat, dynamin
  PINK   = ESCRT, and the patch of membrane it pushes in
  GOLD   = ubiquitin, the tag (round "Ub" badge)
  GREY   = membranes (thick bars and rings), labels, the things the narration says are not there

No molecular structures: a receptor is a bar, a membrane is a thick line or ring, a vesicle is a ring, partners
are blobs, the adaptor and dynamin are small blocks, the coat is a line, ubiquitin is a "Ub" badge.

Layouts:
  scenes 1 and 2   a strip of plasma membrane, receptors with tails down, one pit that deepens and pinches off
  scenes 3 to 6    one large endosome (a ring) fills the frame; its receptors sit on the outer face with the
                   tail out in the cytosol, and one patch of that ring is pushed in to make an inner vesicle.
The membrane is one fixed-length polyline (class Bud), so a receptor that rides on a point of the membrane
stays on it while the membrane bows in, which is how the pit and the inner vesicle are drawn.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F2994A"
PURPLE = "#B58CD9"
PINK = "#F08BB4"
MEM_W = 12


def V(x=0.0, y=0.0):
    return np.array([x, y, 0.0])


def unit(v):
    v = np.array(v, float)
    return v / (np.linalg.norm(v) + 1e-12)


def lft(t):
    """rotate a direction 90 degrees to the left."""
    return np.array([-t[1], t[0], 0.0])


def rgt(t):
    return np.array([t[1], -t[0], 0.0])


def ang(v):
    return np.arctan2(v[1], v[0])


def dirv(a):
    return V(np.cos(a), np.sin(a))


def lerp_dir(a, b, t):
    """turn from direction a to direction b by the short way."""
    da = (ang(b) - ang(a) + np.pi) % (2 * np.pi) - np.pi
    return dirv(ang(a) + da * t)


# ---------------------------------------------------------------------------------------------
# receptor
# ---------------------------------------------------------------------------------------------
class Rec(VGroup):
    """A receptor is one bar through the membrane. `nrm` points to the head, which is outside the cell (or inside
    an endosome or a vesicle); the longer half, the tail, points the other way, into the cytosol."""

    def __init__(self, pos=(0, 0, 0), nrm=(0, 1, 0), k=1.0, tail=BLUE):
        super().__init__()
        self.k = k
        self.HL, self.TL = 0.4 * k, 0.8 * k
        w = 11 * k ** 0.5
        self.body = Line(ORIGIN, UP, color=BLUE, stroke_width=w, cap_style=CapStyleType.ROUND)
        self.tailseg = Line(ORIGIN, UP, color=tail, stroke_width=w, cap_style=CapStyleType.ROUND)
        self.mark = Line(ORIGIN, UP, color=ORANGE, stroke_width=w + 3, cap_style=CapStyleType.ROUND).set_stroke(opacity=0)
        self.add(self.body, self.tailseg, self.mark)
        self.rides = []
        self.set_z_index(2)
        self.place(pos, nrm)

    def resize(self, k):
        self.k = k
        self.HL, self.TL = 0.4 * k, 0.8 * k
        w = 11 * k ** 0.5
        for m, extra in ((self.body, 0), (self.tailseg, 0), (self.mark, 3)):
            m.set_stroke(width=w + extra)
        return self

    def place(self, pos, nrm):
        self.pos, self.nrm = np.array(pos, float), unit(nrm)
        n = self.nrm
        self.body.put_start_and_end_on(self.pos - n * self.TL, self.pos + n * self.HL)
        self.tailseg.put_start_and_end_on(self.pos - n * self.TL, self.pos - n * 0.05)
        self.mark.put_start_and_end_on(self.pos - n * self.TL, self.pos - n * (self.TL - 0.3 * self.k))
        for m, along, side in self.rides:
            m.move_to(self.at(along, side))
        return self

    def at(self, along=0.0, side=0.0):
        """a point `along` beyond the tail tip (negative: back toward the membrane), `side` to one side of it."""
        n = self.nrm
        return self.pos - n * (self.TL + along) + rgt(n) * side

    def ride(self, m, along=0.0, side=0.0):
        self.rides.append((m, along, side))
        m.move_to(self.at(along, side))
        return m


# ---------------------------------------------------------------------------------------------
# membranes that can bow into a bud
# ---------------------------------------------------------------------------------------------
class LineHost:
    """a straight membrane. Travel is left to right; heads are on the left (up)."""

    def __init__(self, y=0.0):
        self.y = y

    def pt(self, u):
        return V(u, self.y)

    def tan(self, u):
        return V(1, 0)


class CircHost:
    """a ring. Travel is counter-clockwise; heads are on the left (toward the centre)."""

    def __init__(self, c, r):
        self.c, self.r = np.array([c[0], c[1], 0.0]), r
        self.circ = 2 * np.pi * r

    def pt(self, u):
        th = u / self.r
        return self.c + self.r * V(np.cos(th), np.sin(th))

    def tan(self, u):
        th = u / self.r
        return V(-np.sin(th), np.cos(th))

    def u_of(self, deg):
        return np.radians(deg) * self.r


class Bud:
    """A patch of a host membrane that can bow into a bud and pinch off.

    side=-1: the bud goes to the right of travel (a pit into the cytosol: heads end up inside the pit).
    side=+1: the bud goes to the left of travel (a vesicle into the lumen: tails end up inside the vesicle).
    The patch is `M` points. State A is the patch lying flat on the host; B1 is a deep bud on a neck;
    B2 is the same bud pinched to a point. Receptors ride on a patch index.
    """

    def __init__(self, host, uc, span, side, R, deep, pinch, m1=28, m2=10, m3=160, x_range=(-6.3, 6.3)):
        self.host, self.uc, self.span, self.side, self.R = host, uc, span, side, R
        self.m1, self.m2, self.m3 = m1, m2, m3
        self.M = 2 * m1 + 2 * m2 + m3
        u0, u1 = uc - span / 2, uc + span / 2
        self.A = np.array([host.pt(u) for u in np.linspace(u0, u1, self.M)])
        self.deep, self.pinch = deep, pinch
        self.B1 = self._flask(*deep)
        self.B2 = self._flask(*pinch)
        if isinstance(host, CircHost):
            self.pre = np.zeros((0, 3))
            self.post = np.array([host.pt(u) for u in np.linspace(u1, u0 + host.circ, 240)[1:]])
        else:
            lo, hi = x_range
            self.pre = np.array([host.pt(u) for u in np.linspace(lo, u0, 30)[:-1]])
            self.post = np.array([host.pt(u) for u in np.linspace(u1, hi, 30)[1:]])
        self.jmid = m1 + m2 + m3 / 2.0

    def D(self):
        T = self.host.tan(self.uc)
        return lft(T) if self.side > 0 else rgt(T)

    def geom(self, n, ln):
        h, uc, R = self.host, self.uc, self.R
        D = self.D()
        SL, SR = h.pt(uc - n), h.pt(uc + n)
        EL, ER = SL + D * ln, SR + D * ln
        mid, half = (EL + ER) / 2, np.linalg.norm(ER - EL) / 2
        ctr = mid + D * np.sqrt(max(R * R - half * half, 1e-6))
        return SL, SR, EL, ER, ctr, D

    def _flask(self, n, ln):
        h, uc, span, R, m1, m2, m3 = self.host, self.uc, self.span, self.R, self.m1, self.m2, self.m3
        SL, SR, EL, ER, ctr, D = self.geom(n, ln)
        mid = (EL + ER) / 2
        aL, aR = ang(EL - ctr), ang(ER - ctr)
        ccw = (aR - aL) % (2 * np.pi)

        def far(sw):
            a = aL + sw / 2
            return np.dot(ctr + R * dirv(a) - mid, D)

        sweep = max([ccw, ccw - 2 * np.pi], key=far)
        angs = aL + sweep * np.linspace(0, 1, m3)
        circ = ctr + R * np.stack([np.cos(angs), np.sin(angs), np.zeros(m3)], 1)
        left_app = [h.pt(u) for u in np.linspace(uc - span / 2, uc - n, m1 + 1)[:-1]]
        neck_l = [SL + D * ln * (k / m2) for k in range(m2)]
        neck_r = [SR + D * ln * (k / m2) for k in range(m2 - 1, -1, -1)]
        right_app = [h.pt(u) for u in np.linspace(uc + n, uc + span / 2, m1 + 1)[1:]]
        return np.array(left_app + neck_l + list(circ) + neck_r + right_app)

    def patch(self, a1, a2=0.0):
        if a2 > 0:
            return (1 - a2) * self.B1 + a2 * self.B2
        return (1 - a1) * self.A + a1 * self.B1

    def path(self, a1, a2=0.0):
        return np.vstack([self.pre, self.patch(a1, a2), self.post])

    def mem(self, a1=0.0, a2=0.0, color=GREY, w=MEM_W):
        m = VMobject(stroke_width=w, cap_style=CapStyleType.ROUND, joint_type=LineJointType.ROUND)
        m.set_points_as_corners(self.path(a1, a2))
        m.set_stroke(color, w).set_fill(opacity=0)
        return m

    def reshape(self, m, a1, a2=0.0):
        m.set_points_as_corners(self.path(a1, a2))

    def at(self, j, a1, a2=0.0, h=3.0):
        """position and head direction of the membrane at patch index j (a float)."""
        P = self.patch(a1, a2)
        top = len(P) - 1.001

        def g(x):
            x = min(max(x, 0.0), top)
            i = int(np.floor(x))
            f = x - i
            return P[i] * (1 - f) + P[i + 1] * f

        return g(j), lft(unit(g(j + h) - g(j - h)))

    def offset_curve(self, j0, j1, d, a1, a2=0.0, step=2):
        """points d beyond the tail side of the membrane between patch indices j0..j1."""
        pts = []
        for j in np.arange(j0, j1 + 0.01, step):
            p, n = self.at(j, a1, a2)
            pts.append(p - n * d)
        return np.array(pts)

    def circle_pts(self, a1=1.0, a2=1.0):
        P = self.patch(a1, a2)
        return P[self.m1 + self.m2: self.m1 + self.m2 + self.m3]

    def ctr_pinched(self):
        return self.geom(*self.pinch)[4]


def ring_mob(pts, color=GREY, w=MEM_W):
    pts = np.vstack([pts, pts[:1]])
    m = VMobject(stroke_width=w, cap_style=CapStyleType.ROUND, joint_type=LineJointType.ROUND)
    m.set_points_as_corners(pts)
    m.set_stroke(color, w).set_fill(opacity=0)
    return m


class BudRig:
    """Everything that moves while a bud forms: the membrane, the receptors on it, and (optionally) a coat with
    its connectors, two collars at the neck, and a highlighted stripe of the membrane."""

    def __init__(self, bud, mem, recs, js, k, coat=None, conns=None, collars=None, hl=None, hl_span=None):
        self.bud, self.mem, self.recs, self.js, self.k = bud, mem, recs, js, k
        self.coat, self.conns, self.collars, self.hl, self.hl_span = coat, conns, collars, hl, hl_span
        self.coat_along, self.coat_half = 0.62, 46

    def set(self, a1, a2=0.0):
        b = self.bud
        b.reshape(self.mem, a1, a2)
        for r, j in zip(self.recs, self.js):
            p, n = b.at(j, a1, a2)
            r.place(p, n)
        if self.coat is not None:
            pts = b.offset_curve(b.jmid - self.coat_half, b.jmid + self.coat_half, 0.8 * self.k + self.coat_along, a1, a2)
            self.coat.set_points_as_corners(pts)
            for r, c in zip(self.recs, self.conns):
                c.put_start_and_end_on(r.at(0.38 * self.k), r.at(self.coat_along))
        if self.hl is not None:
            P = b.patch(a1, a2)
            lo, hi = self.hl_span
            self.hl.set_points_as_corners(P[lo:hi])
        if self.collars is not None:
            n, ln = (b.deep if a2 <= 0 else ((1 - a2) * b.deep[0] + a2 * b.pinch[0], (1 - a2) * b.deep[1] + a2 * b.pinch[1]))
            SL, SR, EL, ER, ctr, D = b.geom(n, ln)
            T = b.host.tan(b.uc)
            self.collars[0].move_to((SL + EL) / 2 - T * 0.17)
            self.collars[1].move_to((SR + ER) / 2 + T * 0.17)

    def drive(self, f, **kw):
        return UpdateFromAlphaFunc(self.mem, lambda m, a: self.set(*f(a)), **kw)


class Vesicle:
    """A pinched-off bud as a rigid ring with its receptors, which can be set to any centre and turn."""

    def __init__(self, bud, js, k, old=None, rides=False, ring_color=GREY):
        c0 = bud.ctr_pinched()
        self.ring_local = bud.circle_pts() - c0
        self.local = []
        for j in js:
            p, n = bud.at(j, 1.0, 1.0)
            self.local.append((p - c0, n))
        self.ring = ring_mob(self.ring_local + c0, color=ring_color)
        self.recs = [Rec(p + c0, n, k=k) for p, n in self.local]
        if old is not None:
            for new, o in zip(self.recs, old):
                new.tailseg.set_color(o.tailseg.get_color())
                new.mark.set_stroke(opacity=o.mark.get_stroke_opacity())
                if rides:
                    new.rides = o.rides
                new.place(new.pos, new.nrm)
        self.c0, self.k = c0, k
        self.group = VGroup(self.ring, *self.recs)

    def set(self, c, rot=0.0, s=1.0):
        """centre c, turned by rot, drawn at scale s (the receptors shrink with it)."""
        c = np.array(c, float)
        Rm = np.array([[np.cos(rot), -np.sin(rot), 0], [np.sin(rot), np.cos(rot), 0], [0, 0, 1]])
        pts = s * self.ring_local @ Rm.T + c
        self.ring.set_points_as_corners(np.vstack([pts, pts[:1]]))
        for r, (p, n) in zip(self.recs, self.local):
            r.resize(self.k * s)
            r.place(c + s * (Rm @ p), Rm @ n)
        return self


# ---------------------------------------------------------------------------------------------
# small pieces
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=24, pad=0.2, **kw):
    """chip with an opaque backing so lines drawn behind it do not show through."""
    c = chip(text, color, size=size, pad=pad, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def ghost_chip(text, size=22):
    """a dashed grey chip: something that is NOT there."""
    t = T(text, size, GREY)
    box = RoundedRectangle(corner_radius=0.14, width=t.width + 0.4, height=t.height + 0.32)
    return VGroup(DashedVMobject(box, num_dashes=max(18, int(box.width * 9))).set_color(GREY), t)


def strike(m, color=RED):
    return Line(m.get_corner(DL) + [-0.08, -0.04, 0], m.get_corner(UR) + [0.08, 0.04, 0], color=color, stroke_width=7)


def inhib(a, b, color=RED, w=5, bar=0.24):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w), Line(b + perp * bar, b - perp * bar, color=color, stroke_width=w + 1))


def dashed_line(a, b, color=GREY, w=4):
    return DashedLine(a, b, color=color, stroke_width=w, dash_length=0.14)


def dashed_arrow(a, b, color=GREY, w=4):
    d = DashedLine(a, b, color=color, stroke_width=w, dash_length=0.14)
    d.add_tip(tip_length=0.22)
    return d


def clock(center, r=0.45):
    center = np.array(center, float)
    face = Circle(radius=r, stroke_color=GREY, stroke_width=4).move_to(center)
    ticks = VGroup(*[Line(center + (r - 0.11) * v, center + r * v, color=GREY, stroke_width=4) for v in (UP, RIGHT, DOWN, LEFT)])
    hand = Line(center, center + UP * (r - 0.15), color=TEXT, stroke_width=5)
    pin = Dot(center, radius=0.05, color=TEXT)
    g = VGroup(face, ticks, hand, pin)
    g.hand, g.c = hand, center
    return g


def blob(r=0.24, color=PURPLE):
    """a partner protein in the cytosol."""
    return Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.55).set_z_index(3)


def ubadge(r=0.21):
    c = Circle(radius=r, stroke_color=GOLD, stroke_width=2, fill_color=GOLD, fill_opacity=1)
    return VGroup(c, T("Ub", 22, BG, weight=BOLD).move_to(c)).set_z_index(4)


def pop(m, s=1.3):
    return m.animate(rate_func=there_and_back).scale(s)


def flash_tails(recs, s=1.0):
    return [Indicate(r.tailseg, color=TEXT, scale_factor=s) for r in recs]


def pointer(a, b, color=GREY, w=3):
    return Line(np.array(a, float), np.array(b, float), color=color, stroke_width=w)


def qbox(center, w=1.0, h=0.9):
    box = RoundedRectangle(corner_radius=0.14, width=w, height=h)
    d = DashedVMobject(box, num_dashes=26).set_color(GREY).move_to(center)
    q = T("?", 40, TEXT, weight=BOLD).move_to(center)
    return VGroup(d, q)


# ---------------------------------------------------------------------------------------------
# the layout shared by scenes 2 to 6
# ---------------------------------------------------------------------------------------------
K = 1.1                                    # receptor size in scenes 3 to 6
K2 = 1.15                                  # receptor size in scene 2 (zoomed in on one pit)
E_C, E_R = V(-1.8, -0.3), 3.0              # the endosome: centre and radius
ENDO = CircHost(E_C, E_R)
U_BUD = ENDO.u_of(20)                      # the patch that will be pushed in (20 degrees: on the right)
ENDO_BUD = Bud(ENDO, U_BUD, 7.0, +1, 1.5, (0.32, 0.5), (0.03, 0.08))
ILV_JS = [ENDO_BUD.jmid - 21, ENDO_BUD.jmid + 21]
HL_SPAN = (ENDO_BUD.m1 + ENDO_BUD.m2, ENDO_BUD.m1 + ENDO_BUD.m2 + ENDO_BUD.m3)

PIT = Bud(LineHost(2.7), 0.0, 9.4, -1, 1.4, (0.32, 0.6), (0.03, 0.1))
PIT_JS = [PIT.jmid + d for d in (-30, 0, 30)]
SC3 = K / K2                               # the vesicle is drawn this much smaller once the view zooms out
C0, ROT0 = V(3.5, 1.2), np.radians(106)    # where the vesicle waits at the start of scene 3
ILV_END = V(-1.6, 0.4)                     # where the inner vesicle settles in scenes 5 and 6


def on_endo(deg):
    u = ENDO.u_of(deg)
    return ENDO.pt(u), lft(ENDO.tan(u))


def escrt_pos(a, b):
    """where the ESCRT chip sits: just beyond the two ubiquitin badges."""
    mid = (a.at(0.0) + b.at(0.0)) / 2
    out = -unit(a.nrm + b.nrm)
    return mid + out * 0.85


class Film(SpokenScene):
    def outro(self, *anims, then=None, run_time=0.4, then_time=0.9):
        """hold until the narration ends, then tidy what the next scene does not inherit, then (optionally)
        move what it does inherit to where the next scene starts it."""
        rest = self.narration_s - 0.02 - self.elapsed()
        if rest > 0:
            self.wait(rest)
        if anims:
            self.play(*anims, run_time=run_time)
        if then:
            self.play(*then, run_time=then_time)
        self.finish()


class S00Title(TitleCard):
    LESSON = "Endocytosis and Signaling Endosomes"
    TITLE = "Sealed inside, a receptor goes silent"


# ---------------------------------------------------------------------------------------------
class S01Question(Film):
    """A pit takes in three receptors; where do they go, and what does the trip do to their signal?"""

    def construct(self):
        k = 1.0
        bud = Bud(LineHost(2.1), 0.0, 7.6, -1, 1.1, (0.3, 0.55), (0.03, 0.08))
        js = [bud.jmid + d for d in (-20, 0, 20)]
        mem = bud.mem()
        recs = [Rec(*bud.at(j, 0), k=k) for j in js]
        rig = BudRig(bud, mem, recs, js, k)
        side = [Rec(bud.host.pt(x), UP, k=k) for x in (-5.8, -4.5, -3.2, -1.9, 1.9, 3.2, 4.5, 5.8)]
        self.play(Create(mem), FadeIn(VGroup(*recs, *side)), run_time=0.5)

        self.at("swallows")
        self.play(rig.drive(lambda a: (a, 0.0)), run_time=1.5)

        br = VGroup(Line(V(-6.1, 2.95), V(6.1, 2.95)), Line(V(-6.1, 2.85), V(-6.1, 3.05)),
                    Line(V(6.1, 2.85), V(6.1, 3.05))).set_color(GREY).set_stroke(width=4)
        whole = T("whole surface", 26, GREY).move_to(V(0, 3.3))
        self.at("whole surface")
        self.play(Create(br), FadeIn(whole), run_time=0.6)

        ck = clock(V(5.1, 0.9), 0.55)
        half = T("half hour", 26, GREY).move_to(V(5.1, 0.1))
        self.at("every half")
        self.play(FadeIn(ck), FadeIn(half), run_time=0.3)
        self.play(Rotate(ck.hand, -TAU, about_point=ck.c), rig.drive(lambda a: (1.0, a)), run_time=1.1)
        v = Vesicle(bud, js, k)
        c0 = bud.ctr_pinched()
        v.set(c0, 0)
        self.remove(*recs)
        self.add(v.group)
        bud.reshape(mem, 0, 0)

        self.at("does not shrink")
        self.play(Indicate(mem, color=TEXT, scale_factor=1.0), run_time=0.8)

        self.at("Many receptors")
        self.play(*[Indicate(r, color=TEXT, scale_factor=1.12) for r in side], run_time=0.8)
        d = V(0, -1.0)
        self.at("make the trip")
        self.play(*[Indicate(r, color=TEXT, scale_factor=1.15) for r in v.recs], run_time=0.6)
        self.play(UpdateFromAlphaFunc(v.ring, lambda m, a: v.set(c0 + a * d)), run_time=1.0)

        tl = T("tail", 28, BLUE).move_to(V(-2.4, 0.9))
        tp = pointer(V(-2.6, 1.05), V(-3.1, 1.4), BLUE)
        self.at("tail of")
        self.play(FadeIn(tl), Create(tp), *flash_tails([*side]), run_time=0.7)
        arrow = Arrow(V(-4.5, 1.1), V(-4.5, 0.1), buff=0, color=GREY, stroke_width=6, tip_length=0.22)
        inside = T("inside the cell", 26, GREY).move_to(V(-4.5, -0.3))
        self.at("points into")
        self.play(GrowArrow(arrow), FadeIn(inside), run_time=0.6)

        q = qbox(V(0, -2.9), 1.1, 1.0)
        self.at("So where does")
        self.play(FadeOut(VGroup(tl, tp, arrow, inside)), FadeIn(q), run_time=0.8)

        lamp = DashedVMobject(Circle(radius=0.55), num_dashes=24).set_color(GREY).move_to(V(-3.3, -1.0))
        lq = T("?", 44, TEXT, weight=BOLD).move_to(V(-3.3, -1.0))
        lt = T("signal", 28, GREY).move_to(V(-3.3, -1.8))
        self.at("And what does")
        self.play(FadeIn(lamp), FadeIn(lq), FadeIn(lt), run_time=0.6)
        self.at("to its signal")
        self.play(pop(lq, 1.5), run_time=0.7)
        self.outro(*[FadeOut(m) for m in self.mobjects])


# ---------------------------------------------------------------------------------------------
class S02Enter(Film):
    """a receptor's tail carries a sequence; an adaptor reads it; a coat, a neck, a collar, a cut."""

    def construct(self):
        bud, k = PIT, K2
        mem = bud.mem()
        recs = [Rec(*bud.at(j, 0), k=k) for j in PIT_JS]
        ads = []
        for r in recs:
            a = RoundedRectangle(corner_radius=0.08, width=0.42, height=0.42, stroke_color=ORANGE, stroke_width=3,
                                 fill_color=ORANGE, fill_opacity=0.35).set_z_index(3)
            r.ride(a, along=0.26)
            ads.append(a)
        coat = VMobject(stroke_width=9, cap_style=CapStyleType.ROUND, joint_type=LineJointType.ROUND)
        coat.set_stroke(ORANGE, 9, opacity=0.95).set_fill(opacity=0)
        conns = [Line(ORIGIN, UP, color=ORANGE, stroke_width=5) for _ in recs]
        collars = [RoundedRectangle(corner_radius=0.08, width=0.22, height=0.52, stroke_color=ORANGE, stroke_width=3,
                                    fill_color=ORANGE, fill_opacity=0.55).set_z_index(3) for _ in range(2)]
        rig = BudRig(bud, mem, recs, PIT_JS, k, coat=coat, conns=conns, collars=collars)
        rig.coat_along, rig.coat_half = 0.8, 46
        rig.set(0, 0)
        y0 = bud.host.y

        self.play(Create(mem), FadeIn(VGroup(*recs)), run_time=0.5)

        s_lab = T("sequence", 28, ORANGE).move_to(V(-4.2, y0 - 0.7))
        s_ptr = pointer(V(-3.4, y0 - 0.72), V(-1.65, y0 - 1.05), ORANGE)
        self.at("tail sequence")
        self.play(*[r.mark.animate.set_stroke(opacity=1) for r in recs], FadeIn(s_lab), Create(s_ptr), run_time=0.6)

        a_lab = T("adaptor", 28, ORANGE).move_to(V(-4.2, y0 - 1.5))
        a_ptr = pointer(V(-3.45, y0 - 1.5), V(-1.55, y0 - 1.62), ORANGE)
        self.at("can read")
        self.play(FadeOut(s_lab), FadeOut(s_ptr), *[FadeIn(a, scale=0.6) for a in ads], FadeIn(a_lab), Create(a_ptr), run_time=0.6)

        c_lab = T("clathrin coat", 28, ORANGE).move_to(V(-4.4, y0 - 2.3))
        c_ptr = pointer(V(-3.2, y0 - 2.3), V(-1.95, y0 - 2.15), ORANGE)
        self.at("links the tail")
        self.play(FadeOut(a_lab), FadeOut(a_ptr), *[Create(c) for c in conns], run_time=0.4)
        self.at("coat of")
        self.play(Create(coat), FadeIn(c_lab), Create(c_ptr), run_time=0.7)

        self.at("pit deepens")
        self.play(FadeOut(c_lab), FadeOut(c_ptr), rig.drive(lambda a: (a, 0.0)), run_time=2.2)

        d_lab = T("dynamin", 28, ORANGE).move_to(V(3.8, y0 - 0.3))
        d_ptr = pointer(V(3.0, y0 - 0.3), V(0.8, y0 - 0.3), ORANGE)
        self.at("builds a collar")
        self.play(*[FadeIn(c, scale=0.5) for c in collars], FadeIn(d_lab), Create(d_ptr), run_time=0.6)

        self.at("neck is cut")
        self.play(FadeOut(d_lab), FadeOut(d_ptr), rig.drive(lambda a: (1.0, a)), run_time=0.9)
        v = Vesicle(bud, PIT_JS, k)
        c0 = bud.ctr_pinched()
        v.set(c0, 0)
        self.remove(*recs)
        self.add(v.group)
        bud.reshape(mem, 0, 0)
        extras = VGroup(*ads, coat, *conns)
        d = V(0, -0.75)
        self.at("is free")
        self.play(FadeOut(VGroup(*collars)), extras.animate.shift(d),
                  UpdateFromAlphaFunc(v.ring, lambda m, a: v.set(c0 + a * d)), run_time=1.1)
        # the coat is stripped; the bare vesicle turns, shrinks as the view zooms out, and moves off to the endosome
        c1 = c0 + d
        self.outro(FadeOut(extras), FadeOut(mem),
                   then=[UpdateFromAlphaFunc(v.ring, lambda m, a: v.set(c1 + a * (C0 - c1), a * ROT0, 1 + a * (SC3 - 1)))])


# ---------------------------------------------------------------------------------------------
TUBE_Y, TUBE_W = -1.61, 0.8
TX0, TX1, TX2 = 0.72, 2.5, 3.9         # the mouth on the endosome, where the capsule begins, where it ends
BAR_Y = 2.9


def tube():
    """a thin tube growing from the endosome: base walls, an open capsule at its end, and the pieces that close it."""
    hw = TUBE_W / 2
    top, bot = TUBE_Y + hw, TUBE_Y - hw
    walls = VGroup(Line(V(TX0, top), V(TX1, top)), Line(V(TX0, bot), V(TX1, bot))).set_stroke(GREY, MEM_W)
    for w in walls:
        w.set_cap_style(CapStyleType.ROUND)
    t = np.linspace(np.pi / 2, -np.pi / 2, 30)
    pts = [V(TX1, top), V(TX2, top)] + [V(TX2 + hw * np.cos(a), TUBE_Y + hw * np.sin(a)) for a in t] + [V(TX2, bot), V(TX1, bot)]
    body = VMobject(stroke_width=MEM_W, cap_style=CapStyleType.ROUND, joint_type=LineJointType.ROUND)
    body.set_points_as_corners(pts)
    body.set_stroke(GREY, MEM_W).set_fill(opacity=0)
    t2 = np.linspace(np.pi / 2, 3 * np.pi / 2, 30)
    left = VMobject(stroke_width=MEM_W, cap_style=CapStyleType.ROUND)
    left.set_points_as_corners([V(TX1 + hw * np.cos(a), TUBE_Y + hw * np.sin(a)) for a in t2])
    left.set_stroke(GREY, MEM_W).set_fill(opacity=0)
    patch = Rectangle(width=0.24, height=TUBE_W - 0.14, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(V(TX0 + 0.02, TUBE_Y))
    return walls, body, left, patch


def partner_on(rec, color=PURPLE):
    b = blob(color=color)
    rec.ride(b, along=-0.34, side=0.28)
    return b


class S03Endosome(Film):
    """the vesicle fuses with the early endosome; the receptors still signal from its outer face; one goes
    back to the surface through a tube."""

    def construct(self):
        v = Vesicle(PIT, PIT_JS, K2)
        v.set(C0, ROT0, SC3)
        endo = ENDO_BUD.mem(0, 0)
        self.add(v.group)
        self.play(Create(endo), run_time=0.5)

        Cc = E_C + (E_R + 1.3 * SC3) * dirv(np.arctan2(*(C0 - E_C)[1::-1]))
        self.at("reaches")
        self.play(UpdateFromAlphaFunc(v.ring, lambda m, a: v.set(C0 + a * (Cc - C0), ROT0, SC3)), run_time=0.8)

        p0 = [r.pos.copy() for r in v.recs]
        n0 = [r.nrm.copy() for r in v.recs]
        tg = [on_endo(d) for d in (-26, -4, 46)]
        recA, recB, recC = v.recs

        def land(m, a):
            for r, q0, m0, (q1, m1) in zip(v.recs, p0, n0, tg):
                r.place((1 - a) * q0 + a * q1, lerp_dir(m0, m1, a))
            v.ring.set_stroke(opacity=1 - a)

        elab = T("early endosome", 30, GREY).move_to(E_C + V(-0.4, -1.0))
        self.at("early endosome")
        self.play(FadeIn(elab), UpdateFromAlphaFunc(v.ring, land), run_time=1.3)
        self.remove(v.ring)
        self.at("first stop")
        self.play(Indicate(endo, color=TEXT, scale_factor=1.0), run_time=0.8)
        self.at("taken in")
        self.play(*[Indicate(r, color=TEXT, scale_factor=1.15) for r in v.recs], run_time=0.8)

        om = T("outer membrane", 24, GREY).move_to(V(-4.9, 2.85))
        omp = pointer(V(-4.25, 2.62), ENDO.pt(ENDO.u_of(135)) + V(-0.05, 0.05), GREY)
        self.at("outer membrane")
        self.play(FadeIn(om), Create(omp), Indicate(endo, color=TEXT, scale_factor=1.0), run_time=0.8)

        cyt = T("cytosol", 28, GREY).move_to(V(3.7, 1.45))
        self.at("into the cytosol")
        self.play(FadeIn(cyt), *flash_tails(v.recs, 1.0), run_time=0.7)

        pa, pb, pc = partner_on(recA), partner_on(recB), partner_on(recC)
        plab = T("partners", 28, PURPLE).move_to(V(3.8, 0.5))
        self.at("reach its partners")
        self.play(FadeOut(om), FadeOut(omp), FadeOut(cyt),
                  LaggedStart(*[FadeIn(b, scale=0.5) for b in (pa, pb, pc)], lag_ratio=0.25),
                  *[r.tailseg.animate.set_color(GREEN) for r in v.recs], FadeIn(plab), run_time=1.0)

        sig = T("can signal", 30, GREEN).move_to(V(3.8, 0.5))
        self.at("go on signaling")
        self.play(ReplacementTransform(plab, sig), *flash_tails(v.recs, 1.0), run_time=0.7)

        walls, body, left, patch = tube()
        self.at("spreads into")
        self.play(FadeOut(sig), FadeOut(pa), FadeIn(patch), Create(walls), Create(body), run_time=0.8)
        pA, nA = recA.pos.copy(), recA.nrm.copy()
        pT, nT = V((TX1 + TX2) / 2, TUBE_Y - TUBE_W / 2), V(0, 1)
        self.play(UpdateFromAlphaFunc(recA, lambda m, a: recA.place((1 - a) * pA + a * pT, lerp_dir(nA, nT, a))), run_time=1.0)

        cap = VGroup(body, left, recA)
        bar = Line(V(3.0, BAR_Y), V(6.2, BAR_Y), color=GREY, stroke_width=MEM_W, cap_style=CapStyleType.ROUND)
        surf = T("surface", 26, GREY).move_to(V(5.7, 3.3))
        delta = V(4.6 - (TX1 + TX2) / 2 - 0.5, 2.35 - TUBE_Y)
        self.at("pinch off")
        self.play(FadeOut(walls), FadeOut(patch), FadeIn(left), Create(bar), run_time=0.5)
        self.play(cap.animate.shift(RIGHT * 0.5), run_time=0.3)
        self.play(cap.animate.shift(delta), run_time=1.4)
        pA2 = pT + V(0.5, 0) + delta
        recA.place(pA2, nT)
        self.at("to the surface")
        self.play(FadeIn(surf), FadeOut(VGroup(body, left)),
                  UpdateFromAlphaFunc(recA, lambda m, a: recA.place(pA2 + a * V(0, BAR_Y - pA2[1]), nT)), run_time=0.8)
        self.outro(FadeOut(VGroup(bar, surf, recA)))


# ---------------------------------------------------------------------------------------------
class S04Tag(Film):
    """a tag, put on by Cbl and read by ESCRT, gathers two receptors into one patch."""

    def construct(self):
        endo = ENDO_BUD.mem(0, 0)
        B = Rec(*on_endo(-4), k=K, tail=GREEN)
        C = Rec(*on_endo(46), k=K, tail=GREEN)
        pb, pc = partner_on(B), partner_on(C)
        elab = T("early endosome", 30, GREY).move_to(E_C + V(-0.4, -1.0))
        self.add(endo, elab, B, C, pb, pc)

        route = dashed_arrow(V(0.85, -2.25), V(3.5, -2.25), GREY, 5)
        rlab = T("default route", 26, GREY).move_to(V(2.2, -2.75))
        self.at("default route")
        self.play(Create(route), FadeIn(rlab), run_time=0.7)
        rbar = Line(V(2.3, -1.97), V(2.3, -2.53), color=RED, stroke_width=9)
        tag0 = ubadge().move_to(V(3.9, 0.45))
        tlab = T("tag", 28, GOLD).next_to(tag0, RIGHT, buff=0.25)
        self.at("carries a tag")
        self.play(FadeIn(tag0, scale=0.6), FadeIn(tlab), Create(rbar), run_time=0.6)
        ulab = T("ubiquitin", 28, GOLD).next_to(tag0, RIGHT, buff=0.25)
        self.at("is ubiquitin")
        self.play(ReplacementTransform(tlab, ulab), FadeOut(VGroup(route, rlab, rbar)), run_time=0.6)

        self.at("active")
        self.play(*flash_tails([B, C], 1.0), run_time=0.7)
        cbl = bchip("Cbl", PURPLE, 24, pad=0.12).set_z_index(5)
        cbl.move_to(B.at(0.62))
        self.at("enzyme called")
        self.play(FadeIn(cbl, scale=0.6), run_time=0.5)
        ub_b, ub_c = ubadge(), ubadge()
        B.ride(ub_b, 0.17)
        C.ride(ub_c, 0.17)
        self.at("adds it")
        self.play(LaggedStart(TransformFromCopy(tag0, ub_b), cbl.animate.move_to(C.at(0.62)), TransformFromCopy(tag0, ub_c),
                              lag_ratio=0.5), run_time=1.1)

        chip = bchip("ESCRT", PINK, 24, pad=0.14).set_z_index(5).move_to(escrt_pos(B, C))
        lines = [Line(u.get_center(), chip.get_center(), color=PINK, stroke_width=4).set_z_index(1) for u in (ub_b, ub_c)]
        self.at("set of proteins")
        self.play(FadeOut(cbl), FadeOut(tag0), FadeOut(ulab), FadeIn(chip, scale=0.7), run_time=0.5)
        self.at("binds the tag")
        self.play(*[Create(l) for l in lines], *[Indicate(u, color=TEXT, scale_factor=1.25) for u in (ub_b, ub_c)], run_time=0.7)

        # the two receptors slide together along the outer face; the chip goes with them
        recs = [B, C]
        a0 = [ang(r.pos - E_C) for r in recs]
        a1 = [ang(ENDO_BUD.at(j, 0)[0] - E_C) for j in ILV_JS]

        def gather(m, a):
            for r, s0, s1 in zip(recs, a0, a1):
                u = E_R * (s0 + a * (s1 - s0))
                r.place(ENDO.pt(u), lft(ENDO.tan(u)))
            chip.move_to(escrt_pos(B, C))
            for l, u in zip(lines, (ub_b, ub_c)):
                l.put_start_and_end_on(u.get_center(), chip.get_center())

        self.at("gather the tagged")
        self.play(UpdateFromAlphaFunc(chip, gather), run_time=1.5)
        hl = VMobject(stroke_width=6, cap_style=CapStyleType.ROUND, joint_type=LineJointType.ROUND)
        hl.set_points_as_corners(ENDO_BUD.patch(0, 0)[HL_SPAN[0]:HL_SPAN[1]])
        hl.set_stroke(PINK, 6).set_fill(opacity=0).set_z_index(1)
        self.at("into a patch")
        self.play(FadeIn(hl), pop(chip, 1.12), run_time=0.7)
        self.outro(FadeOut(elab))


# ---------------------------------------------------------------------------------------------
class S05Seal(Film):
    """ESCRT pushes the patch in; the vesicle inside has the tails inside it; the partners cannot reach them."""

    def construct(self):
        bud = ENDO_BUD
        mem = bud.mem()
        recs = [Rec(*bud.at(j, 0), k=K, tail=GREEN) for j in ILV_JS]
        ubs = [ubadge(), ubadge()]
        for r, u in zip(recs, ubs):
            r.ride(u, 0.17)
        parts = [blob().move_to(r.at(-0.34, 0.28)) for r in recs]
        chip = bchip("ESCRT", PINK, 24, pad=0.14).set_z_index(5).move_to(escrt_pos(*recs))
        lines = [Line(u.get_center(), chip.get_center(), color=PINK, stroke_width=4).set_z_index(1) for u in ubs]
        hl = VMobject(stroke_width=6, cap_style=CapStyleType.ROUND, joint_type=LineJointType.ROUND)
        hl.set_stroke(PINK, 6).set_fill(opacity=0).set_z_index(1)
        rig = BudRig(bud, mem, recs, ILV_JS, K, hl=hl, hl_span=HL_SPAN)
        rig.set(0, 0)
        self.add(mem, hl, *recs, *ubs, *parts, chip, *lines)

        arrows = []
        for sgn in (-1, 1):
            u = U_BUD + sgn * 1.2
            p, inward = ENDO.pt(u), lft(ENDO.tan(u))
            arrows.append(Arrow(p - inward * 1.0, p - inward * 0.12, buff=0, color=PINK, stroke_width=10, tip_length=0.26))
        self.at("pushes the patch")
        self.play(*[FadeOut(l) for l in lines], *[GrowArrow(a) for a in arrows], run_time=0.4)
        self.play(rig.drive(lambda a: (a, 0.0)), run_time=1.5)

        self.at("pinches off")
        self.play(rig.drive(lambda a: (1.0, a)), run_time=0.7)
        v = Vesicle(bud, ILV_JS, K, old=recs, rides=True, ring_color=PINK)
        c0 = bud.ctr_pinched()
        v.set(c0, 0)
        self.remove(*recs, hl)
        self.add(v.group)
        bud.reshape(mem, 0, 0)
        d = ILV_END - c0
        self.play(*[FadeOut(a) for a in arrows], v.ring.animate.set_stroke(GREY), run_time=0.6)
        self.at("inside the endosome")
        self.play(UpdateFromAlphaFunc(v.ring, lambda m, a: v.set(c0 + a * d, 0)), run_time=1.6)

        tl = T("tail", 28, BLUE).move_to(V(-4.15, 0.3))
        tp = pointer(V(-3.78, 0.3), v.recs[0].at(-0.5), BLUE)
        self.at("which way")
        self.play(FadeIn(tl), Create(tp), *flash_tails(v.recs, 1.0), run_time=0.7)
        self.play(*flash_tails(v.recs, 1.0), run_time=0.7)

        sealed = T("sealed in", 28, TEXT).move_to(V(-1.6, -2.1))
        self.at("Inside that vesicle")
        self.play(FadeOut(tl), FadeOut(tp), FadeOut(chip), Indicate(v.ring, color=TEXT, scale_factor=1.0), FadeIn(sealed), run_time=0.8)

        self.at("sealed in")
        self.play(*[r.tailseg.animate.set_color(RED) for r in v.recs], run_time=0.5)

        tan = ENDO.tan(U_BUD)
        cen = ENDO.pt(U_BUD)
        bar = Line(cen - tan * 0.7, cen + tan * 0.7, color=RED, stroke_width=11).set_z_index(6)
        dl = [dashed_line(p.get_center(), cen + tan * s * 0.45, PURPLE, 6) for p, s in zip(parts, (-1, 1))]
        cyt = T("cytosol", 28, GREY).move_to(V(3.9, 1.0))
        self.at("cannot reach")
        self.play(*[Create(x) for x in dl], FadeIn(cyt), run_time=0.5)
        self.play(Create(bar), run_time=0.4)

        off = T("signal off", 30, RED, weight=BOLD).move_to(V(-1.6, -2.65))
        self.at("out of reach")
        self.play(*[p.animate.set_opacity(0.35) for p in parts], *[FadeOut(x) for x in dl], run_time=0.5)
        self.at("signal ends")
        self.play(FadeIn(off), run_time=0.6)

        lyso = ghost_chip("lysosome", 26).move_to(V(4.7, -2.9))
        arr = dashed_arrow(V(0.4, -2.9), V(3.55, -2.9), GREY, 4)
        self.at("the lysosome")
        self.play(FadeIn(lyso), Create(arr), run_time=0.7)
        self.outro(FadeOut(VGroup(bar, sealed, off, cyt, *parts)))


# ---------------------------------------------------------------------------------------------
class S06Break(Film):
    """a receptor that cannot be tagged misses its turn to the lysosome and keeps signaling for longer.
    The lesson does not say where MET signals, so it is drawn on a bare strip of membrane, not on the endosome."""

    def construct(self):
        endo = ENDO_BUD.mem(0, 0)
        v = Vesicle(ENDO_BUD, ILV_JS, K)
        v.set(ILV_END, 0)
        ubs = [ubadge(), ubadge()]
        for r, u in zip(v.recs, ubs):
            r.tailseg.set_color(RED)
            r.ride(u, 0.17)
        lyso = ghost_chip("lysosome", 26).move_to(V(4.9, -3.0))
        arr = dashed_arrow(V(0.3, -3.0), V(3.75, -3.0), GREY, 4)
        self.add(endo, v.group, *ubs, lyso, arr)

        stub = Line(V(2.4, 1.3), V(5.8, 1.3), color=GREY, stroke_width=MEM_W, cap_style=CapStyleType.ROUND)
        X = Rec(V(3.0, 1.3), UP, k=K)
        px = partner_on(X)
        some = T("in some lung cancers", 26, GREY).move_to(V(4.2, 2.95))
        self.at("break")
        self.play(FadeIn(stub), FadeIn(X, scale=0.5), run_time=0.6)
        self.at("lung cancers")
        self.play(FadeIn(some), run_time=0.5)
        met = T("MET", 32, BLUE, weight=BOLD).move_to(V(3.0, 2.3))
        self.at("the receptor")
        self.play(FadeIn(met), Indicate(X.body, color=TEXT, scale_factor=1.05), run_time=0.6)

        slot = DashedVMobject(RoundedRectangle(corner_radius=0.08, width=0.5, height=0.5), num_dashes=16).set_color(GREY)
        slot.move_to(X.at(0.34))
        no = strike(slot)
        dock = T("docking site", 26, GREY).move_to(V(5.0, 0.5))
        self.at("docking site")
        self.play(FadeOut(some), FadeIn(slot), FadeIn(dock), run_time=0.5)
        self.play(Create(no), run_time=0.4)

        cbl = bchip("Cbl", PURPLE, 24, pad=0.12).set_z_index(5)
        mini = Circle(radius=0.12, stroke_color=GOLD, stroke_width=2, fill_color=GOLD, fill_opacity=1).move_to(cbl.get_top() + UP * 0.1)
        grp = VGroup(cbl, mini).move_to(V(5.7, X.at(0.34)[1]))
        self.at("enzyme that adds")
        self.play(FadeOut(dock), FadeIn(grp, shift=LEFT * 0.3), run_time=0.5)
        self.play(grp.animate.shift(LEFT * 1.4), run_time=0.7)
        self.play(grp.animate.shift(RIGHT * 0.5), run_time=0.4)

        self.at("Poorly tagged")
        self.play(FadeOut(grp), run_time=0.5)

        a, b = V(3.0, -0.5), V(4.25, -2.55)
        esc = dashed_arrow(a, b, GREY, 4)
        mid = (a + b) / 2
        perp = lft(unit(b - a))
        escbar = Line(mid + perp * 0.3, mid - perp * 0.3, color=RED, stroke_width=9)
        self.at("escapes the lysosome")
        self.play(Create(esc), Create(escbar), run_time=0.7)

        keeps = T("keeps signaling", 26, GREEN, weight=BOLD).move_to(V(4.9, 0.1))
        self.at("keeps signaling")
        self.play(X.tailseg.animate.set_color(GREEN), FadeIn(px, scale=0.5), FadeIn(keeps), run_time=0.7)
        ck = clock(V(5.3, -1.2), 0.5)
        self.at("longer than")
        self.play(FadeIn(ck), run_time=0.3)
        self.play(Rotate(ck.hand, -TAU * 0.9, about_point=ck.c), run_time=1.3)

        kin = ghost_chip("overactive kinase", 26).move_to(V(4.4, 3.05))
        ks = strike(kin)
        self.at("overactive kinase")
        self.play(FadeOut(ck), FadeIn(kin), run_time=0.4)
        self.play(Create(ks), run_time=0.4)

        turn = T("its turn to the lysosome", 24, GREY).move_to(V(1.95, -2.6))
        self.at("misses its turn")
        self.play(FadeIn(turn), Indicate(arr, color=TEXT, scale_factor=1.0), run_time=0.8)

        self.at("So keep this rule")
        self.play(FadeOut(VGroup(stub, X, px, met, keeps, esc, escbar, kin, ks, slot, no, turn, lyso, arr)), run_time=0.6)
        G = Rec(*on_endo(-12), k=K, tail=GREEN)
        pg = partner_on(G)
        taken = T("taken in: can still signal", 26, GREEN, weight=BOLD).move_to(V(4.2, 0.0))
        self.at("taken in")
        self.play(FadeIn(G, scale=0.5), FadeIn(pg, scale=0.5), FadeIn(taken), run_time=0.7)
        seal = T("sealed in: cannot", 28, RED, weight=BOLD).move_to(V(-1.8, -2.15))
        self.at("sealed in")
        self.play(FadeIn(seal), Indicate(v.ring, color=TEXT, scale_factor=1.0), run_time=0.7)
        self.finish()


class S07End(EndCard):
    LINE = "Taken in, a receptor can still signal; sealed in, it cannot."
