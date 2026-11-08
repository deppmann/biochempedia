# COLOR MAP (shared by every chapter of this lesson's series; one color per concept)
#   BLUE    the protein / polypeptide chain / residues, the peptide-plane cards, candidate dots
#   ORANGE  backbone geometry: the phi/psi hinges and dials, the Ramachandran axes, warnings
#   YELLOW  nonpolar (hydrophobic) side chains, the hydrophobic effect (not used in this chapter)
#   PURPLE  polar / charged residues (not used in this chapter)
#   TEAL    water, interactive cue on cards (not used in this chapter)
#   GREEN   allowed / surviving / the native fold: allowed cells of the map
#   RED     forbidden, clash, disfavored, wrong
#   GOLD    elastase (not used in this chapter)
#   GREY    labels, frames, structure
# NOTHING here draws a molecular structure: peptide planes are rounded cards on two hinges,
# the "atoms" are plain labelled nubs, the coil is a smooth curve, the plot is computed.
import numpy as np
from bp_style import *

ORANGE = "#F29E4C"
PURPLE = "#B58CE0"

# ---------------------------------------------------------------- the schematic Ramachandran map
# (centre phi, centre psi, half-axis phi, half-axis psi, tilt in degrees), same schematic family
# as the lesson's earlier film: beta (broad), right-handed alpha (compact), left-handed (small).
ISL = {"b": (-115, 128, 60, 38, -25), "a": (-63, -42, 28, 25, 0), "l": (57, 47, 20, 26, 0)}


def _in(phi, psi, p, k=1.0, mirror=False):
    c0, c1, a, b, rot = p
    if mirror:
        c0, c1, rot = -c0, -c1, rot
    r = np.radians(rot)
    dx, dy = phi - c0, psi - c1
    u = dx * np.cos(r) + dy * np.sin(r)
    v = -dx * np.sin(r) + dy * np.cos(r)
    return (u / (a * k)) ** 2 + (v / (b * k)) ** 2 <= 1


def which(phi, psi):
    for k, p in ISL.items():
        if _in(phi, psi, p):
            return k
    return None


def gly_ok(phi, psi):
    for p in ISL.values():
        if _in(phi, psi, p, 1.45) or _in(phi, psi, p, 1.3, mirror=True):
            return True
    return False


NG = 36
CELL = 360 / NG
CENTERS = [(-180 + (i + .5) * CELL, -180 + (j + .5) * CELL) for i in range(NG) for j in range(NG)]
ALLOWED = [(a, b, which(a, b)) for a, b in CENTERS if which(a, b)]
BLANK = [(a, b) for a, b in CENTERS if not which(a, b) and not any(
    which(a + da, b + db) for da in (-25, 0, 25) for db in (-25, 0, 25))]
SHARE = len(ALLOWED) / len(CENTERS)   # share of the schematic map that is open (computed)
_rng = np.random.RandomState(11)


def _inside(k, shrink=0.78):
    """A random point well inside island k (so a plausible structure sits on the island, not at its edge)."""
    c0, c1, a, b, rot = ISL[k]
    r = np.radians(rot)
    while True:
        u, v = _rng.uniform(-1, 1, 2)
        if u * u + v * v <= 1:
            break
    u, v = u * a * shrink, v * b * shrink
    return (c0 + u * np.cos(r) - v * np.sin(r), c1 + u * np.sin(r) + v * np.cos(r))


GOOD = [_inside(k) for k in ("b",) * 14 + ("a",) * 12 + ("l",) * 8]
_rng.shuffle(GOOD)
BAD = [_inside(k) for k in ("b", "a", "a", "b", "l", "b", "a")]
for _ in range(19):
    a, b = BLANK[_rng.randint(len(BLANK))]
    BAD.append((a + _rng.uniform(-4, 4), b + _rng.uniform(-4, 4)))
_rng.shuffle(BAD)
OUTLIER = (112, -78)
RX = 1.5   # left edge of the right-hand text column
GREEK = "αβφψ"


def _font(t):
    return TITLE_FONT if any(g in t for g in GREEK) else FONT


def tagbox(txt, color=TEXT, size=30, pos=None):
    t = T(txt, size=size, color=color, font=_font(txt))
    bk = Rectangle(width=t.width + 0.22, height=t.height + 0.14, stroke_width=0, fill_color=BG, fill_opacity=0.6).move_to(t)
    g = VGroup(bk, t).set_z_index(8)
    if pos is not None:
        g.move_to(pos)
    return g


def rcol(lines, y=1.6, gap=0.2, x=RX):
    """Stack of (text, color, size) lines, left aligned in the right-hand column."""
    mobs = [T(t, size=s, color=c, font=_font(t)) for t, c, s in lines]
    g = VGroup(*mobs).arrange(DOWN, aligned_edge=LEFT, buff=gap)
    g.move_to([0, y, 0]).align_to([x, 0, 0], LEFT)
    return g


def mcol(lines, y=0.0, gap=0.2, x=RX):
    """Same, in the monospace face (for numbers)."""
    mobs = [M(t, size=s, color=c) for t, c, s in lines]
    g = VGroup(*mobs).arrange(DOWN, aligned_edge=LEFT, buff=gap)
    g.move_to([0, y, 0]).align_to([x, 0, 0], LEFT)
    return g


def title_mob():
    return T("Ramachandran plot", size=38, font=TITLE_FONT).move_to([0, 3.55, 0]).align_to([RX, 0, 0], LEFT)


class Kit:
    """The Ramachandran map: frame, computed allowed cells, ticks, axis names."""

    def __init__(self, cx=-2.2, cy=0.1, pw=6.0, ticks=True, names=True, op=0.7):
        self.cx, self.cy, self.pw = cx, cy, pw
        c = np.array([cx, cy, 0.0])
        self.c = c
        self.c2p = lambda phi, psi: c + np.array([phi / 360 * pw, psi / 360 * pw, 0.0])
        self.frame = Square(pw, color=GREY, stroke_width=3).move_to(c).set_z_index(6)
        self.hl = Line(self.frame.get_left(), self.frame.get_right(), color=GREY, stroke_width=1.5).set_opacity(0.5).set_z_index(6)
        self.vl = Line(self.frame.get_bottom(), self.frame.get_top(), color=GREY, stroke_width=1.5).set_opacity(0.5).set_z_index(6)
        self.tint = Square(pw, stroke_width=0, fill_color=RED, fill_opacity=0.10).move_to(c).set_z_index(1)
        s = pw / NG
        self.cols = [VGroup() for _ in range(NG)]
        self.isl = {k: VGroup() for k in ISL}
        self.gly = VGroup()
        for i in range(NG):
            for j in range(NG):
                phi, psi = CENTERS[i * NG + j]
                k = which(phi, psi)
                if k:
                    sq = Square(s, stroke_width=0.8, stroke_color=GREEN, fill_color=GREEN, fill_opacity=op).move_to(self.c2p(phi, psi)).set_z_index(3)
                    self.cols[i].add(sq)
                    self.isl[k].add(sq)
                elif gly_ok(phi, psi):
                    self.gly.add(Square(s, stroke_width=0.8, stroke_color=BLUE, fill_color=BLUE, fill_opacity=0.3).move_to(self.c2p(phi, psi)).set_z_index(2))
        self.cells = VGroup(*self.isl.values())
        h = pw / 2
        TS = 26
        self.xt = VGroup(*[M(v, size=TS, color=GREY).move_to(c + np.array([dx, -h - 0.33, 0]))
                           for v, dx in (("−180°", -h + 0.35), ("0°", 0), ("180°", h - 0.35))])
        self.yt = VGroup(*[M(v, size=TS, color=GREY).move_to(c + np.array([-h - 0.2, dy, 0]), aligned_edge=RIGHT)
                           for v, dy in (("180°", h), ("0°", 0), ("−180°", -h))])
        # axis letters sit beside their own axis, with a small arrow along it
        xl = M("φ", size=40, color=ORANGE).move_to(c + np.array([h / 2 - 0.8, -h - 0.33, 0]))
        xar = Arrow(xl.get_right() + RIGHT * 0.1, xl.get_right() + RIGHT * 0.75, color=ORANGE, buff=0, stroke_width=5, max_tip_length_to_length_ratio=0.4)
        yl = M("ψ", size=40, color=ORANGE).move_to(c + np.array([-h - 0.5, h / 2 - 0.2, 0]))
        yar = Arrow(yl.get_top() + UP * 0.1, yl.get_top() + UP * 0.75, color=ORANGE, buff=0, stroke_width=5, max_tip_length_to_length_ratio=0.4)
        self.xa = VGroup(xl, xar)
        self.ya = VGroup(yl, yar)
        self.static = VGroup(self.frame, self.hl, self.vl)
        if ticks:
            self.static.add(self.xt, self.yt)
        if names:
            self.static.add(self.xa, self.ya)

    def tag(self, k, text=None, size=42):
        phi, psi = ISL[k][0], ISL[k][1]
        txt = text or {"b": "β", "a": "α", "l": "αL"}[k]
        return tagbox(txt, TEXT, size, self.c2p(phi, psi))

    def dot(self, phi, psi, color=BLUE, r=0.085):
        return Dot(self.c2p(phi, psi), radius=r, color=color).set_z_index(7)

    def outline(self, k, color=TEXT):
        c0, c1, a, b, rot = ISL[k]
        e = Ellipse(width=2 * a / 360 * self.pw, height=2 * b / 360 * self.pw, color=color, stroke_width=3)
        e.rotate(np.radians(rot)).move_to(self.c2p(c0, c1)).set_z_index(7)
        return e

    def glow(self, scene, k, run_time=0.6):
        others = [self.isl[o] for o in ISL if o != k]
        scene.play(self.isl[k].animate.set_opacity(1.0), *[o.animate.set_opacity(0.3) for o in others], run_time=run_time)

    def glow_anims(self, k):
        return [self.isl[k].animate.set_opacity(1.0)] + [self.isl[o].animate.set_opacity(0.3) for o in ISL if o != k]

    def all_on_anims(self):
        return [g.animate.set_opacity(0.7) for g in self.isl.values()]

    def leader(self, psi, x_from_phi, color=GREY, y_end=None):
        """Dashed line from the island's right edge, at the island's height, to the text column."""
        y = self.c2p(0, psi)[1] if y_end is None else y_end
        return DashedLine(self.c2p(x_from_phi, psi), np.array([RX - 0.15, y, 0.0]), dash_length=0.12, color=color, stroke_width=3).set_z_index(5)


# entries in the column, level with their island: (psi, leader start phi)
ENT = {"b": (128, -52), "l": (47, 82), "a": (-42, -30)}
EY = {"b": 2.55, "l": 0.6, "a": -1.5}   # centre of each island's text block (all lines laid out up front)
ENTRY_LINES = {
    "b": [("β: extended strands", TEXT, 42), ("like the beta sheet", TEXT, 38)],
    "a": [("α: compact island", TEXT, 42), ("right-handed helix", TEXT, 38), ("φ ≈ −57°, ψ ≈ −47°", ORANGE, 36)],
    "l": [("αL: small island", TEXT, 42), ("left-handed", TEXT, 38), ("mostly glycine", BLUE, 38)],
}


def entry(k):
    """Column text block level with island k, every line at full contrast; the caller fades the lines in one by one."""
    return rcol(ENTRY_LINES[k], y=EY[k], gap=0.14)


# ---------------------------------------------------------------- the two-card model
H1 = np.array([-0.1, -0.55])
H2 = np.array([0.45, 0.63])
C1 = np.array([-1.5, -0.55])
NO = np.array([-1.9, -0.05])
CW, CH = 2.8, 0.9
DIALS = ((-5.4, 2.3), (-3.8, 2.3))


def _u(a):
    return np.array([np.cos(a), np.sin(a)])


def _n(a):
    return np.array([-np.sin(a), np.cos(a)])


class Rig:
    """Two flat cards (peptide planes) on two hinges. phi is held; psi turns card 2."""

    def __init__(self, sc=1.5, org=(1.1, -1.55), psi=20, dials=True):
        self.sct, self.oxt, self.oyt = ValueTracker(sc), ValueTracker(org[0]), ValueTracker(org[1])
        self.psi = ValueTracker(psi)
        self.alpha = ValueTracker(0)
        self.dial_a = ValueTracker(0)
        self.nubs = ValueTracker(0)
        self.stub = ValueTracker(0)
        self.hl = ValueTracker(0)
        self.glowk = ValueTracker(0.28)
        self.lab = {k: ValueTracker(0) for k in ("c", "n", "s", "bb", "pl", "pl1")}
        self.body = always_redraw(self.build)
        self.dials = always_redraw(self.build_dials) if dials else VGroup()

    @property
    def sc(self):
        return self.sct.get_value()

    @property
    def org(self):
        return np.array([self.oxt.get_value(), self.oyt.get_value()])

    def zoom_anims(self, sc, org):
        return [self.sct.animate.set_value(sc), self.oxt.animate.set_value(org[0]), self.oyt.animate.set_value(org[1])]

    def L(self, p):
        return np.array([self.org[0] + self.sc * p[0], self.org[1] + self.sc * p[1], 0.0])

    def geom(self):
        t = np.radians(self.psi.get_value())
        u, n = _u(t), _n(t)
        nn = H2 + 2.41 * u + 0.45 * n
        sb = H2 + 2.6 * u + 0.45 * n
        st = sb + 0.55 * n
        return t, u, n, nn, sb, st

    def clash_nh(self):
        t, u, n, nn, sb, st = self.geom()
        return np.linalg.norm(nn - NO) < 0.40

    def clash_stub(self):
        t, u, n, nn, sb, st = self.geom()
        return -2.9 - 0.03 < st[0] < -0.1 + 0.03 and -1.0 - 0.03 < st[1] < -0.1 + 0.03

    def build(self):
        a = self.alpha.get_value()
        if a < 0.01:
            return VGroup()
        S = self.sc
        t, u, n, nn, sb, st = self.geom()
        hl = self.hl.get_value()
        kw = dict(stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=(0.28 + 0.3 * hl) * a, stroke_opacity=a)
        card1 = RoundedRectangle(corner_radius=0.18 * S, width=CW * S, height=CH * S, **kw).move_to(self.L(C1))
        card2 = RoundedRectangle(corner_radius=0.18 * S, width=CW * S, height=CH * S, **kw).rotate(t).move_to(self.L(H2 + 1.4 * u))
        link = Line(self.L(H1), self.L(H2), color=GREY, stroke_width=5, stroke_opacity=a)
        hing = VGroup(Dot(self.L(H1), radius=0.13 * S, color=ORANGE), Dot(self.L(H2), radius=0.13 * S, color=ORANGE)).set_opacity(a)
        g = VGroup(card1, card2, link, hing)
        nb = self.nubs.get_value() * a
        if nb > 0.01:
            red = self.clash_nh()
            col = RED if red else TEXT
            o = Circle(radius=0.2 * S, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.9 * nb, stroke_opacity=nb).move_to(self.L(NO))
            q = Circle(radius=0.2 * S, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.9 * nb, stroke_opacity=nb).move_to(self.L(nn))
            g.add(o, q)
            if red:
                mid = (self.L(NO) + self.L(nn)) / 2
                g.add(Circle(radius=0.55 * S, stroke_color=RED, stroke_width=3, fill_color=RED, fill_opacity=self.glowk.get_value() * nb,
                             stroke_opacity=nb).move_to(mid))
        sv = self.stub.get_value() * a
        if sv > 0.01:
            red = self.clash_stub()
            col = RED if red else TEXT
            g.add(Line(self.L(sb), self.L(st), color=col, stroke_width=14 * S, stroke_opacity=sv),
                  Dot(self.L(st), radius=0.1 * S, color=col, fill_opacity=sv))
            if red:
                g.add(Circle(radius=0.5 * S, stroke_color=RED, stroke_width=3, fill_color=RED, fill_opacity=0.1 + self.glowk.get_value() * sv,
                             stroke_opacity=sv).move_to(self.L(st)))
        ang = t - np.pi if np.degrees(t) > 90 else t
        sz = 30
        # C=O: label below the plane, leader up to the nub
        vc = self.lab["c"].get_value() * a
        if vc > 0.01:
            g.add(Line(self.L(np.array([-1.9, -1.1])), self.L(NO + np.array([0.0, -0.1])), color=GREY, stroke_width=3, stroke_opacity=vc),
                  T("C=O", size=sz, color=TEXT).move_to(self.L(np.array([-1.9, -1.4]))).set_opacity(vc).set_z_index(9))
        # N-H: label above the second plane, leader down to the nub
        vn = self.lab["n"].get_value() * a
        if vn > 0.01:
            top = nn - 1.5 * n
            g.add(Line(self.L(nn - 0.25 * n), self.L(nn - 1.1 * n), color=GREY, stroke_width=3, stroke_opacity=vn),
                  T("N–H", size=sz, color=TEXT).move_to(self.L(top)).set_opacity(vn).set_z_index(9))
        # side chain: label at the left, leader to the stub
        vs = self.lab["s"].get_value() * a
        if vs > 0.01:
            lp = self.L(np.array([-3.55, -0.4]))
            tx = T("side chain", size=sz, color=TEXT).move_to(lp).set_opacity(vs).set_z_index(9)
            g.add(tx, Line(tx.get_right() + RIGHT * 0.05, self.L((sb + st) / 2), color=GREY, stroke_width=3, stroke_opacity=vs))
        # backbone: label below the first plane
        vb = self.lab["bb"].get_value() * a
        if vb > 0.01:
            g.add(Line(self.L(np.array([-1.5, -1.1])), self.L(np.array([-1.5, -1.0])) + DOWN * 0.15, color=GREY, stroke_width=3, stroke_opacity=vb),
                  T("backbone", size=sz, color=TEXT).move_to(self.L(np.array([-1.5, -1.4]))).set_opacity(vb).set_z_index(9))
        v = self.lab["pl"].get_value() * a
        if v > 0.01:
            g.add(T("plane", size=sz, color=TEXT).rotate(ang).move_to(self.L(H2 + 1.0 * u)).set_opacity(v).set_z_index(9))
        v = self.lab["pl1"].get_value() * a
        if v > 0.01:
            g.add(T("plane", size=sz, color=TEXT).move_to(self.L(np.array([-1.5, -0.55]))).set_opacity(v).set_z_index(9))
        return g

    def build_dials(self):
        a = self.dial_a.get_value()
        if a < 0.01:
            return VGroup()
        g = VGroup()
        for (cx, cy), ang, sym in zip(DIALS, (65, self.psi.get_value()), "φψ"):
            ring = Circle(radius=0.6, stroke_color=ORANGE, stroke_width=5, stroke_opacity=a, fill_color=ORANGE, fill_opacity=0.10 * a).move_to([cx, cy, 0])
            nd = Line([cx, cy, 0], [cx, cy, 0] + 0.5 * np.append(_u(np.radians(ang)), 0), color=ORANGE, stroke_width=8, stroke_opacity=a)
            g.add(ring, nd, Dot([cx, cy, 0], radius=0.07, color=ORANGE, fill_opacity=a),
                  M(sym, size=44, color=ORANGE).move_to([cx, cy - 1.05, 0]).set_opacity(a))
        return g

    def add_to(self, scene):
        # build the current state now, so the very first frame of the scene is not blank
        self.body.become(self.build())
        if not isinstance(self.dials, VGroup) or len(self.dials.submobjects) or True:
            try:
                self.dials.become(self.build_dials())
            except Exception:
                pass
        scene.add(self.body, self.dials)

    def ring(self, scene, p, color=ORANGE, r=0.3, rt=0.7):
        pts = p if isinstance(p, list) else [p]
        cs = [Circle(radius=r * self.sc, color=color, stroke_width=5).move_to(self.L(q)) for q in pts]
        scene.add(*cs)
        scene.play(*[c.animate.scale(2.5).set_stroke(opacity=0) for c in cs], run_time=rt)
        scene.remove(*cs)


def rig_state(rig, psi, alpha=1, dials=1, nubs=0, stub=0):
    rig.psi.set_value(psi)
    rig.alpha.set_value(alpha)
    rig.dial_a.set_value(dials)
    rig.nubs.set_value(nubs)
    rig.stub.set_value(stub)


ZOOM = dict(sc=2.2, org=(2.2, -0.4))   # the clash scenes zoom in on the folded-back cards


def held_label(text="held", i=0, color=GREY):
    x, y = DIALS[i]
    return T(text, size=30, color=color).move_to([x, y - 1.65, 0])


# ================================================================== scenes
class S00Title(TitleCard):
    LESSON = "Protein three-dimensional structure"
    TITLE = "The Map of Allowed Shapes"

    def construct(self):
        brand = T("BIOCHEMISTRYPEDIA", size=24, color=TEAL, weight=BOLD).set_opacity(0.9)
        lesson = T(self.LESSON.upper(), size=26, color=GREY)
        title = fit(T(self.TITLE, size=64, font=TITLE_FONT), max_w=12.0)
        rule = Line(LEFT * 1.4, RIGHT * 1.4, color=GOLD, stroke_width=4)
        g = VGroup(brand, lesson, title, rule).arrange(DOWN, buff=0.36)
        # the whole title is on screen within the first second, then held
        self.play(FadeIn(g, shift=UP * 0.1), run_time=0.7)
        self.finish()


class S01(SpokenScene):
    def construct(self):
        r = Rig()
        rig_state(r, 20, alpha=1, dials=0)
        r.add_to(self)
        q = fit(T("How many of those settings actually work?", size=44, color=GREY), max_w=12.2).move_to([0, 3.5, 0])
        self.add(q)  # the question is on screen from the first frame
        self.at("hinges")
        self.play(r.dial_a.animate.set_value(1), run_time=0.3)
        r.ring(self, [H1, H2], rt=0.5)
        self.at("sounds like")
        self.play(r.psi.animate.set_value(52), run_time=1.0, rate_func=smooth)
        self.play(r.psi.animate.set_value(35), run_time=1.0, rate_func=smooth)
        self.at("how many")
        self.play(q.animate.set_color(TEXT), Indicate(q, scale_factor=1.06, color=TEXT), run_time=0.8)
        self.finish()


class S02(SpokenScene):
    def construct(self):
        r = Rig()
        rig_state(r, 35)
        r.add_to(self)
        q = fit(T("How many of those settings actually work?", size=44, color=TEXT), max_w=12.2).move_to([0, 3.5, 0])
        self.add(q)
        self.wait(0.2)
        self.at("linked cards")
        self.play(r.hl.animate.set_value(1), FadeOut(q), run_time=0.4)
        self.play(r.hl.animate.set_value(0), run_time=0.5)
        self.at("hold one hinge")
        held = held_label("held", 0)
        self.play(FadeIn(held), run_time=0.3)
        r.ring(self, H1, rt=0.5)
        self.at("and turn")
        turning = held_label("turning", 1, ORANGE)
        self.play(FadeIn(turning), r.psi.animate.set_value(120), run_time=1.6, rate_func=smooth)
        self.finish()


class S03(SpokenScene):
    def construct(self):
        r = Rig()
        rig_state(r, 120)
        r.add_to(self)
        self.add(held_label("held", 0), held_label("turning", 1, ORANGE))
        self.play(r.psi.animate.set_value(160), run_time=1.2, rate_func=smooth)
        self.at("an atom on")
        self.play(r.nubs.animate.set_value(1), run_time=0.4)
        at1 = T("atom", size=30).move_to([-4.6, -0.5, 0])
        self.play(FadeIn(at1), r.psi.animate.set_value(180), *r.zoom_anims(**{"sc": ZOOM["sc"], "org": ZOOM["org"]}), run_time=0.9, rate_func=smooth)
        self.at("runs into")
        self.play(r.psi.animate.set_value(186), run_time=0.3, rate_func=smooth)
        self.play(r.glowk.animate.set_value(0.6), run_time=0.3)
        self.at("on the next")
        self.play(r.glowk.animate.set_value(0.25), run_time=0.3)
        self.play(r.glowk.animate.set_value(0.6), run_time=0.3)
        self.finish()


class S04(SpokenScene):
    def construct(self):
        r = Rig(**ZOOM)
        rig_state(r, 186, nubs=1)
        r.glowk.set_value(0.6)
        r.add_to(self)
        self.add(held_label("held", 0), held_label("turning", 1, ORANGE))
        self.at("co group")
        self.play(r.lab["c"].animate.set_value(1), run_time=0.4)
        self.at("comes too close")
        self.play(r.psi.animate.set_value(160), run_time=0.5)
        self.at("close to")
        self.play(r.psi.animate.set_value(186), run_time=0.4)
        self.at("nh group")
        self.play(r.lab["n"].animate.set_value(1), run_time=0.4)
        self.at("or a side")
        self.play(r.nubs.animate.set_value(0), r.lab["c"].animate.set_value(0), r.lab["n"].animate.set_value(0),
                  r.psi.animate.set_value(172), run_time=0.5)
        self.at("side chain")
        self.play(r.stub.animate.set_value(1), r.lab["s"].animate.set_value(1), run_time=0.4)
        self.at("runs into")
        self.play(r.psi.animate.set_value(192), run_time=0.7, rate_func=smooth)
        self.at("backbone")
        self.play(r.lab["bb"].animate.set_value(1), run_time=0.4)
        self.finish()


class S05(SpokenScene):
    def construct(self):
        r = Rig(**ZOOM)
        rig_state(r, 192, nubs=0, stub=1)
        r.lab["s"].set_value(1)
        r.lab["bb"].set_value(1)
        r.glowk.set_value(0.1)
        r.add_to(self)
        self.add(held_label("held", 0), held_label("turning", 1, ORANGE))
        self.at("atoms would")
        self.play(r.nubs.animate.set_value(1), r.lab["s"].animate.set_value(0), r.lab["bb"].animate.set_value(0),
                  r.psi.animate.set_value(188), r.glowk.animate.set_value(0.5), run_time=0.7)
        self.at("same space")
        lab = T("steric clash", size=46, color=RED).move_to([5.0, 0.4, 0])
        a1 = Arrow(lab.get_left() + LEFT * 0.1, r.L(NO) + RIGHT * 1.15 + UP * 0.1, color=RED, buff=0.05, stroke_width=6)
        a2 = Arrow(lab.get_left() + LEFT * 0.1 + DOWN * 0.2, r.L(np.array([-1.88, -0.89])) + RIGHT * 1.1, color=RED, buff=0.05, stroke_width=6)
        self.play(FadeIn(lab, shift=LEFT * 0.15), GrowArrow(a1), GrowArrow(a2), run_time=0.6)
        self.play(r.glowk.animate.set_value(0.3), run_time=0.4)
        self.at("strongly")
        l2 = T("strongly disfavored", size=34, color=TEXT).move_to([4.7, 2.1, 0])
        self.play(FadeIn(l2, shift=UP * 0.1), run_time=0.5)
        self.finish()


def stage(scene, kit, cells=False, tint=False):
    scene.add(kit.static)
    if tint:
        scene.add(kit.tint)
    if cells:
        scene.add(kit.cells)


class S06(SpokenScene):
    def construct(self):
        r = Rig(**ZOOM)
        rig_state(r, 188, nubs=1, stub=1)
        r.glowk.set_value(0.3)
        r.add_to(self)
        hl_, tl_ = held_label("held", 0), held_label("turning", 1, ORANGE)
        self.add(hl_, tl_)
        k = Kit(ticks=False, names=False)
        self.play(r.alpha.animate.set_value(0), r.dial_a.animate.set_value(0), FadeOut(hl_), FadeOut(tl_),
                  Create(k.frame), FadeIn(k.hl), FadeIn(k.vl), run_time=0.5)
        self.remove(r.body, r.dials)
        px, py = ValueTracker(0), ValueTracker(0)
        dot = always_redraw(lambda: Dot(k.c2p(px.get_value(), py.get_value()), radius=0.12, color=TEXT).set_z_index(8))
        ro = always_redraw(lambda: mcol([(f"φ = {int(round(px.get_value())):+d}°", ORANGE, 40),
                                         (f"ψ = {int(round(py.get_value())):+d}°", ORANGE, 40)], y=0.6))
        self.add(dot, ro)
        self.at("every pair")
        rng = np.random.RandomState(5)
        for _ in range(8):
            self.play(px.animate.set_value(rng.uniform(-160, 160)), py.animate.set_value(rng.uniform(-160, 160)), run_time=0.26, rate_func=smooth)
        self.play(FadeOut(dot), FadeOut(ro), run_time=0.2)
        self.at("phi along")
        a1 = rcol([("φ", ORANGE, 56), ("along the bottom", TEXT, 38)], y=1.5)
        self.play(FadeIn(k.xa), FadeIn(a1, shift=LEFT * 0.1), run_time=0.5)
        self.at("psi up")
        a2 = rcol([("ψ", ORANGE, 56), ("up the side", TEXT, 38)], y=-0.6)
        self.play(FadeIn(k.ya), FadeIn(a2, shift=LEFT * 0.1), run_time=0.5)
        self.finish()


class S07(SpokenScene):
    def construct(self):
        k = Kit(ticks=False)
        stage(self, k)
        # a number line in the right column that runs in step with the axes
        x0, x1, ny = 1.9, 6.5, 0.2
        nl = Line([x0, ny, 0], [x1, ny, 0], color=GREY, stroke_width=4)
        marks = VGroup(*[Line([x, ny - 0.15, 0], [x, ny + 0.15, 0], color=GREY, stroke_width=4) for x in (x0, (x0 + x1) / 2, x1)])
        labs = [M(v, size=26, color=GREY).move_to([x, ny - 0.55, 0]) for v, x in (("−180°", x0), ("0°", (x0 + x1) / 2), ("180°", x1))]
        hd = rcol([("φ and ψ each run", TEXT, 38)], y=1.4)
        self.play(FadeIn(nl), FadeIn(marks), FadeIn(hd), run_time=0.5)
        h = k.pw / 2
        c = k.c
        m = ValueTracker(-180)
        mk = always_redraw(lambda: Dot([x0 + (m.get_value() + 180) / 360 * (x1 - x0), ny, 0], radius=0.17, color=ORANGE).set_z_index(8))
        dx = always_redraw(lambda: Dot(k.c2p(m.get_value(), -180), radius=0.13, color=ORANGE).set_z_index(8))
        dy = always_redraw(lambda: Dot(k.c2p(-180, m.get_value()), radius=0.13, color=ORANGE).set_z_index(8))
        self.add(mk, dx, dy)
        self.at("minus 180")
        self.play(FadeIn(k.xt[0]), FadeIn(k.yt[2]), FadeIn(labs[0]), Indicate(mk, scale_factor=1.6, color=ORANGE), run_time=0.5)
        self.at("to plus")
        self.play(m.animate.set_value(0), FadeIn(k.xt[1]), FadeIn(k.yt[1]), FadeIn(labs[1]), run_time=0.6, rate_func=linear)
        self.at("plus 180")
        self.play(m.animate.set_value(180), FadeIn(k.xt[2]), FadeIn(k.yt[0]), FadeIn(labs[2]), run_time=0.8, rate_func=linear)
        self.play(FadeOut(dx), FadeOut(dy), run_time=0.3)
        self.finish()


class S08(SpokenScene):
    def construct(self):
        k = Kit()
        stage(self, k)
        scan = Line(k.c2p(-180, -180), k.c2p(-180, 180), color=ORANGE, stroke_width=4).set_z_index(8)
        self.add(scan)
        cols = [g for g in k.cols if len(g)]
        h = len(cols) // 2
        l1 = rcol([("no clash:", GREY, 34), ("shaded", GREEN, 44)], y=1.7)
        self.play(FadeIn(l1, shift=LEFT * 0.1), run_time=0.3)

        def sweep(cs, a0, a1, rt):
            self.play(LaggedStart(*[FadeIn(g) for g in cs], lag_ratio=0.12, run_time=rt, rate_func=linear),
                      UpdateFromAlphaFunc(scan, lambda mm, a: mm.move_to(k.c2p(-180 + 360 * (a0 + (a1 - a0) * a), 0)), run_time=rt, rate_func=linear))
        sweep(cols[:h], 0.0, 0.5, 1.0)
        self.at("clash")
        l2 = rcol([("clash:", GREY, 34), ("left empty", RED, 44)], y=0.2)
        self.play(FadeIn(l2, shift=LEFT * 0.1), run_time=0.3)
        sweep(cols[h:], 0.5, 1.0, 1.3)
        self.play(FadeOut(scan), run_time=0.2)
        self.at("ramachandran", lead=2.4)
        nm = rcol([("G. N. Ramachandran", TEXT, 32)], y=-1.6)
        bx = SurroundingRectangle(nm, color=GOLD, buff=0.22, corner_radius=0.12, stroke_width=3)
        self.play(FadeIn(nm, shift=UP * 0.12), Create(bx), run_time=0.6)
        self.at("did this")
        nm2 = rcol([("did this calculation", GREY, 34)], y=-2.65)
        self.play(FadeIn(nm2, shift=UP * 0.1), run_time=0.5)
        self.finish()


class S09(SpokenScene):
    def construct(self):
        k = Kit()
        stage(self, k, cells=True)
        self.at("survivors")
        t1 = rcol([("survivors", GREEN, 52)], y=1.9)
        self.play(FadeIn(t1, shift=LEFT * 0.1), LaggedStart(*[Indicate(g, scale_factor=1.06, color=GREEN) for g in k.isl.values()], lag_ratio=0.3, run_time=1.4))
        self.at("compact islands")
        t2 = rcol([("a few compact", TEXT, 40), ("islands", TEXT, 40)], y=0.5)
        self.play(FadeIn(t2, shift=LEFT * 0.1), run_time=0.4)
        self.at("rest of")
        e = tagbox("empty", GREY, 36, k.c2p(100, -105))
        t3 = rcol([("the rest of the map", GREY, 38), ("is empty", RED, 48)], y=-1.4)
        self.play(FadeIn(e), FadeIn(t3, shift=LEFT * 0.1), run_time=0.6)
        self.finish()


class S10(SpokenScene):
    def construct(self):
        k = Kit()
        stage(self, k, cells=True)
        dis = tagbox("disfavored", RED, 34, k.c2p(-125, -135))
        self.at("small fraction")
        self.play(FadeIn(k.tint), FadeIn(dis), run_time=0.5)
        # a share bar: the green sliver is the open share of this map, the rest is disfavored
        W, by = 5.2, 1.5
        cap = T("all φ, ψ pairs", size=30, color=GREY).move_to([RX + W / 2, by + 0.75, 0])
        bar = Rectangle(width=W, height=0.7, stroke_color=GREY, stroke_width=3, fill_color=RED, fill_opacity=0.3).move_to([RX + W / 2, by, 0])
        sw = max(0.35, W * SHARE)
        sl = Rectangle(width=sw, height=0.7, stroke_width=0, fill_color=GREEN, fill_opacity=0.9).align_to(bar, LEFT).align_to(bar, UP).shift(RIGHT * 0)
        sl.move_to([RX + sw / 2, by, 0])
        sf = T("small fraction", size=44, color=GREEN).move_to([RX, by - 0.95, 0]).align_to([RX, 0, 0], LEFT)
        self.play(FadeIn(cap), FadeIn(bar), run_time=0.4)
        self.play(GrowFromEdge(sl, LEFT), FadeIn(sf, shift=UP * 0.1), run_time=0.5)
        self.at("open to")
        lg = rcol([("open to the backbone", GREEN, 36)], y=-0.9)
        self.play(FadeIn(lg, shift=LEFT * 0.1), LaggedStart(*[Indicate(g, scale_factor=1.06, color=GREEN) for g in k.isl.values()], lag_ratio=0.25, run_time=1.2))
        self.at("this is the")
        title = title_mob()
        self.play(FadeIn(title, shift=DOWN * 0.1), run_time=0.5)
        self.finish()


def map_state(scene, kit, title=True, dis=True, dis_pos=(-125, -135), tint=True):
    stage(scene, kit, cells=True, tint=tint)
    out = []
    if title:
        tt = title_mob()
        scene.add(tt)
        out.append(tt)
    if dis:
        d = tagbox("disfavored", RED, 34, kit.c2p(*dis_pos))
        scene.add(d)
        out.append(d)
    return out


class S11(SpokenScene):
    def construct(self):
        k = Kit()
        map_state(self, k)
        px, py = ValueTracker(110), ValueTracker(100)
        dot = always_redraw(lambda: Dot(k.c2p(px.get_value(), py.get_value()), radius=0.13, color=TEXT).set_z_index(8))
        ring = always_redraw(lambda: Circle(radius=0.3, color=ORANGE, stroke_width=5).move_to(k.c2p(px.get_value(), py.get_value())).set_z_index(8))
        ro = always_redraw(lambda: mcol([(f"φ = {int(round(px.get_value())):+d}°".replace("+0", "0"), ORANGE, 44),
                                         (f"ψ = {int(round(py.get_value())):+d}°".replace("+0", "0"), ORANGE, 44)], y=0.6))
        self.add(dot, ring, ro)
        t = rcol([("Here is the test", TEXT, 50)], y=1.9)
        self.play(FadeIn(t, shift=LEFT * 0.1), run_time=0.5)
        self.at("both angles")
        self.play(px.animate.set_value(0), py.animate.set_value(0), run_time=1.5, rate_func=smooth)
        self.at("right in the")
        self.play(Indicate(ring, scale_factor=1.5, color=ORANGE), run_time=0.8)
        self.at("will that")
        q = rcol([("Will that pair", TEXT, 50), ("survive?", TEXT, 50)], y=-1.7)
        self.play(FadeIn(q, shift=UP * 0.12), run_time=0.5)
        self.finish()


class S12Pause(NarratedScene):
    def construct(self):
        k = Kit()
        map_state(self, k)
        d = k.dot(0, 0, color=TEXT, r=0.13)
        ring = Circle(radius=0.3, color=ORANGE, stroke_width=5).move_to(d).set_z_index(8)
        ro = mcol([("φ = 0°", ORANGE, 44), ("ψ = 0°", ORANGE, 44)], y=1.7)
        q = rcol([("Allowed", TEXT, 60), ("or not?", TEXT, 60)], y=-0.15)
        self.add(d, ring, ro, q)
        tr = ValueTracker(0)
        cen = np.array([RX + 1.0, -2.2, 0])
        base = Circle(radius=0.8, color=GREY, stroke_width=4).move_to(cen)
        arc = always_redraw(lambda: Arc(radius=0.8, start_angle=PI / 2, angle=-TAU * (1 - tr.get_value()) + 1e-4, color=ORANGE, stroke_width=10, arc_center=cen))
        num = always_redraw(lambda: M(str(int(np.ceil(max(0.0, 5 * (1 - tr.get_value())) - 1e-6))) if tr.get_value() < 0.999 else "0", size=48, color=ORANGE).move_to(cen))
        self.add(base, arc, num)
        self.play(tr.animate.set_value(1.0), run_time=self.narration_s, rate_func=linear)
        self.finish()


class S13(SpokenScene):
    def construct(self):
        k = Kit()
        map_state(self, k)
        d = k.dot(0, 0, color=TEXT, r=0.13)
        ring = Circle(radius=0.3, color=ORANGE, stroke_width=5).move_to(d).set_z_index(8)
        self.add(d, ring)
        r = Rig(sc=1.55, org=(5.95, -1.1), psi=186, dials=False)
        rig_state(r, 186, alpha=1, dials=0, nubs=1)
        r.glowk.set_value(0.3)
        r.add_to(self)
        ro = M("φ = 0°, ψ = 0°", size=30, color=ORANGE).move_to([4.2, -3.1, 0])
        no = T("No.", size=64, color=RED).move_to([0, 2.3, 0]).align_to([RX, 0, 0], LEFT)
        # the red overlap and the red dot are on screen from the first word, "No"
        d.set_color(RED)
        ring.set_color(RED)
        self.add(no, ro)
        self.at("atoms of")
        self.play(r.glowk.animate.set_value(0.65), run_time=0.3)
        self.play(r.glowk.animate.set_value(0.3), run_time=0.3)
        self.at("peptide planes")
        self.play(r.lab["pl"].animate.set_value(1), r.lab["pl1"].animate.set_value(1), run_time=0.4)
        self.at("run into")
        self.play(r.psi.animate.set_value(160), run_time=0.4, rate_func=smooth)
        self.play(r.psi.animate.set_value(186), run_time=0.4, rate_func=smooth)
        self.play(r.glowk.animate.set_value(0.65), run_time=0.3)
        self.play(r.glowk.animate.set_value(0.3), run_time=0.3)
        self.at("center of")
        big = Circle(radius=0.5, color=RED, stroke_width=5).move_to(k.c2p(0, 0)).set_z_index(7)
        em = tagbox("empty", RED, 42, k.c2p(100, -118))
        ld = Line(k.c2p(0, 0) + DOWN * 0.3 + RIGHT * 0.3, em.get_left() + LEFT * 0.02, color=RED, stroke_width=3).set_z_index(7)
        self.play(Create(big), FadeIn(em), Create(ld), run_time=0.6)
        self.finish()


def island_base(k, tags=("b", "a", "l"), dim_entries=()):
    """Static map with the previously met islands' tags; returns tag mobs."""
    out = []
    for s in tags:
        t = k.tag(s)
        out.append(t)
    return out


def old_entries(k, keys):
    """Earlier islands' column text and leaders, at full contrast."""
    g = VGroup()
    for s in keys:
        g.add(entry(s), k.leader(*ENT[s], y_end=EY[s]))
    return g


class S14(SpokenScene):
    def construct(self):
        k = Kit()
        map_state(self, k)
        self.at("islands")
        self.play(LaggedStart(*[Indicate(g, scale_factor=1.06, color=GREEN) for g in k.isl.values()], lag_ratio=0.2, run_time=1.0))
        self.at("broad one", lead=0.3)
        o = k.outline("b")
        tb = k.tag("b")
        e = entry("b")
        ld = k.leader(*ENT["b"], y_end=EY["b"])
        self.play(*k.glow_anims("b"), Create(o), FadeIn(tb), FadeIn(e[0], shift=LEFT * 0.1), Create(ld), run_time=0.7)
        self.at("like the beta")
        self.play(FadeIn(e[1], shift=LEFT * 0.1), run_time=0.4)
        self.finish()


class S15(SpokenScene):
    def construct(self):
        k = Kit()
        map_state(self, k)
        self.add(k.tag("b"), old_entries(k, ["b"]))
        for g in k.isl.values():
            g.set_opacity(0.7)
        self.at("compact one", lead=0.0)
        o = k.outline("a")
        ta = k.tag("a")
        e = entry("a")
        ld = k.leader(*ENT["a"], y_end=EY["a"])
        self.play(*k.glow_anims("a"), Create(o), FadeIn(ta), FadeIn(e[0], shift=LEFT * 0.1), Create(ld), run_time=0.6)
        self.at("right handed")
        self.play(FadeIn(e[1], shift=LEFT * 0.1), run_time=0.4)
        self.at("alpha helix")
        m = k.dot(-57, -47, color=TEXT, r=0.1)
        self.play(FadeIn(m, scale=2), FadeIn(e[2], shift=LEFT * 0.1), run_time=0.5)
        self.finish()


class S16(SpokenScene):
    def construct(self):
        k = Kit()
        map_state(self, k)
        self.add(k.tag("b"), k.tag("a"), old_entries(k, ["b", "a"]))
        k.isl["b"].set_opacity(0.7)
        k.isl["a"].set_opacity(0.7)
        self.at("small island", lead=0.0)
        o = k.outline("l")
        tl = k.tag("l")
        e = entry("l")
        ld = k.leader(*ENT["l"], y_end=EY["l"])
        self.play(*k.glow_anims("l"), Create(o), FadeIn(tl), FadeIn(e[0], shift=LEFT * 0.1), Create(ld), run_time=0.6)
        self.at("left handed")
        self.play(FadeIn(e[1], shift=LEFT * 0.1), run_time=0.4)
        self.at("mostly by")
        self.play(FadeIn(e[2], shift=LEFT * 0.1), run_time=0.4)
        self.finish()


class S17(SpokenScene):
    def construct(self):
        k = Kit()
        map_state(self, k, dis=False)
        for s in ISL:
            self.add(k.tag(s, size=40))
        lg0 = VGroup(Square(0.34, stroke_width=0, fill_color=BLUE, fill_opacity=0.6), T("glycine", size=38, color=BLUE)).arrange(RIGHT, buff=0.25)
        lg0.move_to([0, 2.5, 0]).align_to([RX, 0, 0], LEFT)
        k.gly.set_opacity(0.2)
        g = Dot(k.c2p(57, 47), radius=0.22, color=BLUE).set_z_index(9)
        trail = TracedPath(g.get_center, stroke_color=BLUE, stroke_width=7, dissipating_time=1.1).set_z_index(8)
        gt = VGroup(tagbox("glycine can also", BLUE, 30), tagbox("go here", BLUE, 30)).arrange(DOWN, buff=0.02).move_to(k.c2p(98, -122)).set_z_index(9)
        self.add(trail)
        self.play(FadeIn(k.gly), FadeIn(lg0, shift=LEFT * 0.1), FadeIn(g, scale=1.8), run_time=0.7)
        self.at("roams")
        self.play(FadeIn(gt), run_time=0.3)
        pts = [(120, -110), (170, -160), (-160, 150), (-80, -35), (57, 47)]
        for a, b in pts:
            self.play(g.animate.move_to(k.c2p(a, b)), run_time=0.4, rate_func=smooth)
        self.at("other residue")
        lg1 = VGroup(Square(0.34, stroke_width=0, fill_color=GREEN, fill_opacity=0.7), T("other residues", size=38, color=GREEN)).arrange(RIGHT, buff=0.25)
        lg1.next_to(lg0, DOWN, buff=0.25, aligned_edge=LEFT)
        wd = rcol([("wider,", TEXT, 40), ("not unlimited", TEXT, 40)], y=0.5)
        self.play(FadeIn(lg1, shift=LEFT * 0.1), FadeIn(wd, shift=LEFT * 0.1), run_time=0.5)
        self.at("side chain")
        s1 = rcol([("side chain = H", TEXT, 44)], y=-1.0)
        self.play(FadeIn(s1, shift=LEFT * 0.1), run_time=0.5)
        self.at("single hydrogen")
        s2 = rcol([("no Cβ", TEXT, 38)], y=-1.8)
        self.play(FadeIn(s2, shift=LEFT * 0.1), run_time=0.4)
        self.at("bumps into")
        s3 = rcol([("fewer clashes", GREEN, 44)], y=-2.7)
        self.play(FadeIn(s3, shift=LEFT * 0.1), run_time=0.5)
        self.finish()


def coil_curve(cx, cy, h=4.7, turns=4):
    ts = np.linspace(0, turns * TAU, 220)
    pts = [np.array([1.05 * np.sin(t), (t / (turns * TAU) - 0.5) * h + 0.3 * np.cos(t), 0.0]) for t in ts]
    m = VMobject(stroke_color=BLUE, stroke_width=10)
    m.set_points_smoothly(pts)
    m.move_to([cx, cy, 0])
    return m


def strand_curve(cx, cy, h=4.7):
    ys = np.linspace(-h / 2, h / 2, 17)
    pts = [np.array([0.3 * (-1) ** i, y, 0.0]) for i, y in enumerate(ys)]
    m = VMobject(stroke_color=BLUE, stroke_width=10)
    m.set_points_smoothly(pts)
    m.move_to([cx, cy, 0])
    return m


class S18(SpokenScene):
    def construct(self):
        k = Kit()
        map_state(self, k)
        for t in ISL:
            self.add(k.tag(t, size=44))
        intro = rcol([("Each island", TEXT, 50), ("matches a", TEXT, 50), ("real shape", TEXT, 50)], y=0.2, gap=0.18)
        self.add(intro)
        self.at("real shape")
        self.play(LaggedStart(*[Indicate(g, scale_factor=1.06, color=GREEN) for g in k.isl.values()], lag_ratio=0.2, run_time=1.0))
        self.at("helix island", lead=0.0)
        coil = coil_curve(4.2, -0.1)
        h = T("helix island: coil", size=42).move_to([4.2, -3.2, 0])
        self.play(*k.glow_anims("a"), FadeOut(intro), Create(coil), FadeIn(h, shift=UP * 0.1), run_time=1.3)
        self.at("strand island", lead=0.35)
        st = strand_curve(4.2, -0.1)
        h2 = VGroup(T("strand island:", size=40), T("stretched chain", size=40)).arrange(DOWN, buff=0.1).move_to([4.2, -3.25, 0])
        self.play(*k.glow_anims("b"), Transform(coil, st), FadeOut(h), FadeIn(h2, shift=UP * 0.1), run_time=0.7)
        self.finish()


class S19(SpokenScene):
    def construct(self):
        k = Kit()
        map_state(self, k, dis=False)
        for s in ISL:
            self.add(k.tag(s, size=44))
        self.at("also a check", lead=0.0)
        hd = rcol([("a check on", TEXT, 40), ("new structures", TEXT, 40)], y=2.2)
        self.play(FadeIn(hd, shift=LEFT * 0.1), run_time=0.5)
        self.at("new structures")
        # a schematic chain (one wavy line) with a dot per residue
        N = 34
        pos = lambda f: np.array([4.2 + 0.7 * np.sin(f * 3.2 * TAU / 2), 1.3 - 3.7 * f, 0.0])
        chain = VMobject(stroke_color=BLUE, stroke_width=6)
        chain.set_points_smoothly([pos(f) for f in np.linspace(0, 1, 90)])
        res = VGroup(*[Dot(pos(f), radius=0.11, color=BLUE).set_z_index(4) for f in np.linspace(0, 1, N)])
        cap = VGroup(T("each residue:", size=42, color=TEXT), T("one φ, ψ pair", size=42, color=TEXT, font=TITLE_FONT)).arrange(DOWN, buff=0.12).move_to([4.2, -3.2, 0])
        self.play(Create(chain), FadeIn(res), FadeIn(cap), run_time=0.9)
        self.at("plot every")
        dots = VGroup(*[Dot(r.get_center(), radius=0.085, color=BLUE).set_z_index(7) for r in res])
        self.add(dots)
        self.play(LaggedStart(*[d.animate.move_to(k.c2p(*p)) for d, p in zip(dots, GOOD)], lag_ratio=0.03, run_time=1.8))
        self.finish()


def tick_mark(pos, color=GREEN):
    v = VMobject(stroke_color=color, stroke_width=10)
    v.set_points_as_corners([pos + np.array([-0.3, 0.0, 0]), pos + np.array([-0.08, -0.25, 0]), pos + np.array([0.32, 0.3, 0])])
    return v


def warn_mark(pos, color=ORANGE):
    tri = Triangle(color=color, stroke_width=6).scale(0.34).move_to(pos)
    ex = T("!", size=34, color=color, weight=BOLD).move_to(pos + DOWN * 0.04)
    return VGroup(tri, ex)


PCY = 0.0
PW = 5.2


def panel(cx, dots):
    kk = Kit(cx=cx, cy=PCY, pw=PW)
    for g in kk.isl.values():
        g.set_opacity(0.7)
    tags = VGroup(*[kk.tag(s, size=30) for s in ISL])
    ds = VGroup(*[kk.dot(a, b, r=0.075) for a, b in dots])
    allm = VGroup(kk.static, kk.tint, kk.cells, tags, ds)
    return kk, ds, allm


class S20(SpokenScene):
    def construct(self):
        # start from the full map with the scattered dots (end of the last scene)
        k0 = Kit()
        map_state(self, k0, dis=False)
        d0 = VGroup(*[k0.dot(a, b, r=0.085) for a, b in GOOD])
        self.add(d0)
        kl, dl, left = panel(-3.0, GOOD)
        kr, dr, right = panel(3.9, BAD)
        ok = tick_mark(np.array([-4.3, 3.2, 0]))
        okt = T("plausible", size=42, color=GREEN).move_to([-2.7, 3.2, 0])
        w = warn_mark(np.array([1.6, 3.2, 0]))
        wt = T("something wrong", size=40, color=ORANGE).move_to([4.2, 3.2, 0])
        olds = [m for m in self.mobjects]
        right_all = VGroup(right, w, wt)
        self.play(*[FadeOut(m) for m in olds], FadeIn(left), FadeIn(ok), FadeIn(okt), FadeIn(right_all), run_time=0.7)
        self.remove(*olds)
        self.at("plausible")
        self.play(Indicate(okt, scale_factor=1.12, color=GREEN), Indicate(ok, scale_factor=1.2, color=GREEN), run_time=0.7)
        self.at("many stray")
        self.play(Indicate(wt, scale_factor=1.12, color=ORANGE), Indicate(w, scale_factor=1.3, color=ORANGE), run_time=0.8)
        self.finish()


def ring_outlier(k):
    p = k.c2p(*OUTLIER)
    d = Dot(p, radius=0.12, color=BLUE).set_z_index(9)
    rg = Circle(radius=0.3, color=ORANGE, stroke_width=5).move_to(p).set_z_index(9)
    return d, rg


OUT_Y = 0.1 + OUTLIER[1] / 60


class S21(SpokenScene):
    def construct(self):
        # two panels (end of the last scene) give way to one clean map with no dots
        kl, dl, left = panel(-3.0, GOOD)
        kr, dr, right = panel(3.9, BAD)
        self.add(left, right)
        k = Kit()
        tt = title_mob()
        self.play(FadeOut(left), FadeOut(right), FadeIn(VGroup(k.static, k.tint, k.cells, tt)), run_time=0.5)
        self.add(k.static, k.tint, k.cells, tt)
        dis = tagbox("disfavored", RED, 34, k.c2p(-125, -135))
        self.add(dis)
        f1 = rcol([("forbidden", RED, 48), ("= strongly disfavored,", RED, 36), ("not impossible", TEXT, 44)], y=1.5, gap=0.15)
        self.play(FadeIn(f1[0], shift=LEFT * 0.1), run_time=0.4)
        self.at("strongly")
        self.play(FadeIn(f1[1], shift=LEFT * 0.1), run_time=0.4)
        self.at("not impossible")
        self.play(FadeIn(f1[2], shift=LEFT * 0.1), run_time=0.4)
        self.at("a few residues")
        d, rg = ring_outlier(k)
        self.play(FadeIn(d, scale=2.0), Create(rg), run_time=0.5)
        self.at("strained spots")
        ol = T("outlier", size=44, color=ORANGE).move_to([0, OUT_Y, 0]).align_to([RX, 0, 0], LEFT)
        ld = DashedLine(rg.get_right() + RIGHT * 0.02, ol.get_left() + LEFT * 0.12, dash_length=0.12, color=ORANGE, stroke_width=3).set_z_index(9)
        self.play(FadeIn(ol, shift=LEFT * 0.1), Create(ld), run_time=0.5)
        self.at("held by")
        hb = rcol([("held in place by", GREY, 34), ("its surroundings", GREY, 34)], y=OUT_Y - 1.2)
        self.play(FadeIn(hb, shift=LEFT * 0.1), run_time=0.5)
        self.finish()


class S22(SpokenScene):
    def construct(self):
        k = Kit()
        map_state(self, k, dis=False)
        self.add(tagbox("disfavored", RED, 34, k.c2p(-125, -135)))
        d, rg = ring_outlier(k)
        ol = T("outlier", size=44, color=ORANGE).move_to([0, OUT_Y, 0]).align_to([RX, 0, 0], LEFT)
        ld = DashedLine(rg.get_right() + RIGHT * 0.02, ol.get_left() + LEFT * 0.12, dash_length=0.12, color=ORANGE, stroke_width=3).set_z_index(9)
        f1 = rcol([("forbidden", RED, 48), ("= strongly disfavored,", RED, 36), ("not impossible", TEXT, 44)], y=1.5, gap=0.15)
        self.add(d, rg, ol, ld, f1)
        self.at("outliers are")
        pulse = Circle(radius=0.3, color=ORANGE, stroke_width=5).move_to(rg)
        self.add(pulse)
        self.play(pulse.animate.scale(2.2).set_stroke(opacity=0), FadeOut(f1), run_time=0.6)
        self.remove(pulse)
        self.at("matter for")
        cp = chip("often catalytic", TEXT, size=44).move_to([RX + 2.1, OUT_Y - 1.5, 0])
        ar = DashedLine(ol.get_bottom() + DOWN * 0.08, cp.get_top() + UP * 0.05, dash_length=0.14, color=ORANGE, stroke_width=6)
        ar.add_tip(tip_length=0.25)
        ar.get_tip().set_color(ORANGE)
        self.play(Create(ar), FadeIn(cp, shift=UP * 0.1), run_time=0.7)
        self.at("catalysis")
        ca = T("may sit at an active site", size=34, color=GREY).next_to(cp, DOWN, buff=0.3).align_to([RX, 0, 0], LEFT)
        self.play(FadeIn(ca, shift=UP * 0.1), run_time=0.4)
        self.finish()


class S23(SpokenScene):
    def construct(self):
        k = Kit()
        map_state(self, k, dis=False)
        self.add(tagbox("disfavored", RED, 34, k.c2p(-125, -135)))
        for s in ISL:
            self.add(k.tag(s, size=48))
        self.at("most hinge")
        m1 = rcol([("Most settings", RED, 52), ("crash.", RED, 52)], y=1.4)
        self.play(FadeIn(m1, shift=LEFT * 0.1), Indicate(k.tint, scale_factor=1.0, color=RED), run_time=0.8)
        self.at("backbone is")
        m2 = rcol([("A few local", GREEN, 46), ("shapes remain:", GREEN, 46), ("β, α and αL", TEXT, 48)], y=-1.2)
        self.play(FadeIn(m2, shift=LEFT * 0.1), LaggedStart(*[Indicate(g, scale_factor=1.08, color=GREEN) for g in k.isl.values()], lag_ratio=0.25, run_time=1.4))
        self.finish()


class S24End(EndCard):
    LINE = "Most pairs clash. Three islands remain: helix, strand, left-handed."

    def construct(self):
        ls = VGroup(*[T(t, size=54, font=TITLE_FONT) for t in ("Most pairs clash.", "Three islands remain:", "helix, strand, left-handed.")])
        ls.arrange(DOWN, buff=0.3)
        sub = T("biochemistrypedia.com", size=30, color=TEAL)
        g = VGroup(ls, sub).arrange(DOWN, buff=0.7).move_to(ORIGIN)
        self.play(FadeIn(ls, shift=UP * 0.15), run_time=self.beat(0.3))
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        self.finish()
