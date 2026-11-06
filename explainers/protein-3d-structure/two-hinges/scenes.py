# Chapter 2: Two Hinges per Residue
# COLOR MAP (shared with all chapters of the protein 3D structure series)
#   BLUE    the protein / polypeptide chain / residues
#   ORANGE  backbone geometry constraints: the rigid peptide plane (cards), the phi/psi hinges, trans/cis, the lock
#   YELLOW  nonpolar (hydrophobic) side chains     (not used in this chapter)
#   PURPLE  polar / charged residues                (not used in this chapter)
#   TEAL    water                                   (not used in this chapter)
#   GREEN   the native fold, allowed / surviving    (not used in this chapter)
#   RED     forbidden, eliminated, misfolded        (not used in this chapter)
#   GREY    labels, frames, structure; atom letters sit in light-grey rings
# Atoms are drawn only as lettered badges and the bonds between them as lines (a labelled schematic,
# not a structure). Backbone "cards" are plain plates. Nothing here is a molecular drawing.
#
# The card chain (s14-s21) is computed, not sketched: a 4-residue backbone is built atom by atom from
# its phi and psi angles (standard bond lengths and angles, peptide bond fixed trans), each card is the
# outline of one peptide plane, and every swing is a real rotation about the named bond, projected.
import numpy as np
from bp_style import *

ORANGE = "#F29E4C"
LIGHT = "#C9CED8"
CY = 0.15          # vertical centre of the big atom picture
LS = 38            # standard label size


def unit(v):
    v = np.asarray(v, float)
    return v / np.linalg.norm(v)


def G(text, size=LS, color=TEXT, **kw):
    """Label in Georgia (has proper lower-case Greek: φ ψ α)."""
    return T(text, size=size, color=color, font=TITLE_FONT, **kw)


def leader(lab, target, color=GREY, buff=0.12, sw=2.5):
    """Thin line from the edge of a label to the thing it names."""
    c = lab.get_center()
    d = np.asarray(target, float) - c
    hw, hh = lab.width / 2 + buff, lab.height / 2 + buff
    t = min(hw / max(abs(d[0]), 1e-6), hh / max(abs(d[1]), 1e-6))
    a = c + d * min(t, 0.95)
    b = np.asarray(target, float) - unit(d) * 0.12
    return Line(a, b, color=color, stroke_width=sw)


# ---------------------------------------------------------------- hull helper
def hull2(pts):
    pts = sorted(set((round(p[0], 5), round(p[1], 5)) for p in pts))
    if len(pts) < 3:
        return pts

    def cr(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cr(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def padded_hull(points, pads, n=40):
    S = []
    for p, r in zip(points, pads):
        if r <= 0:
            S.append((p[0], p[1]))
        else:
            for t in np.linspace(0, 2 * np.pi, n, endpoint=False):
                S.append((p[0] + r * np.cos(t), p[1] + r * np.sin(t)))
    return hull2(S)


# ---------------------------------------------------------------- bead chain (scenes 1-2)
def beadchain(seed, n=100, w=11.6, h=5.0, cy=-0.15):
    k = seed * 101 + 7
    while True:
        rng = np.random.RandomState(k)
        k += 1
        ang = rng.uniform(0, 2 * np.pi)
        pts = [np.zeros(2)]
        turn = 0.0
        for _ in range(n - 1):
            turn = 0.75 * turn + rng.normal(0, 0.32)
            ang += turn
            pts.append(pts[-1] + np.array([np.cos(ang), np.sin(ang)]))
        P = np.array(pts)
        ratio = np.ptp(P[:, 0]) / max(np.ptp(P[:, 1]), 1e-6)
        if 1.8 < ratio < 2.8:
            break
    P -= (P.max(0) + P.min(0)) / 2
    P *= min(w / np.ptp(P[:, 0]), h / np.ptp(P[:, 1]))
    P[:, 1] += cy
    line = VMobject(stroke_color=BLUE, stroke_width=4)
    line.set_points_smoothly([np.array([x, y, 0.0]) for x, y in P])
    beads = [Dot([x, y, 0], radius=0.075, color=BLUE) for x, y in P]
    return VGroup(line, *beads), P


def bead(x, y, r):
    return Circle(radius=r, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.2).move_to([x, y, 0])


# ---------------------------------------------------------------- atom badges, bonds, clusters
# schematic layout (bond angles about 120 degrees), in units of s
POS = {"C": (-1.0, 0.0), "N": (1.0, 0.0), "O": (-1.8, 1.386), "H": (1.7, -1.212), "Ca1": (-2.0, -1.732), "Ca2": (2.0, 1.732)}
POS_CIS = dict(POS, H=(1.7, 1.212), Ca2=(2.0, -1.732))


def CA(size, color):
    return G("Cα", size=size, color=color)


def mk_atom(name, pos, s, lit=False):
    r = max(0.3, 0.4 * s)
    lab = "Cα" if name.startswith("Ca") else name
    col = ORANGE if lit else LIGHT
    c = Circle(radius=r, stroke_color=col, stroke_width=4, fill_color=(ORANGE if lit else BG),
               fill_opacity=(0.45 if lit else 1.0)).move_to(pos)
    if len(lab) == 2:
        t = CA(max(24, 28 * s), TEXT)
    else:
        t = T(lab, size=max(26, 34 * s), color=TEXT)
    t.move_to(pos)
    return VGroup(c, t)


def mk_bond(p, q, order, r, col=LIGHT, w=5):
    u = unit(q - p)
    n = np.array([-u[1], u[0], 0.0])
    a, b = p + u * r, q - u * r
    off = 0.14 * r / 0.4 if order > 1 else 0.0
    off = min(off, 0.13)
    l1 = Line(a - n * off, b - n * off, color=col, stroke_width=w)
    l2 = Line(a + n * off, b + n * off, color=col, stroke_width=w)
    l2.set_stroke(opacity={1: 0.0, 1.5: 0.45, 2: 1.0}[order])
    return VGroup(l1, l2)


def charge(sign, at, s):
    rr = 0.2 * max(1.0, s)
    c = Circle(radius=rr, stroke_color=ORANGE, stroke_width=3, fill_color=BG, fill_opacity=1)
    t = T(sign, size=34 * max(1.0, s) * 0.95, color=ORANGE, weight=BOLD)
    return VGroup(c, t.move_to(c)).move_to(at).set_z_index(3)


class Cl:
    """The peptide-bond atoms as lettered badges joined by lines."""

    def __init__(self, cx=0.0, cy=CY, s=1.35, cis=False, ca=False, co=1, cn=1, cn_col=LIGHT, minus=False, plus=False, lit=()):
        pos = POS_CIS if cis else POS
        names = ["C", "O", "N", "H"] + (["Ca1", "Ca2"] if ca else [])
        self.s = s
        self.r = r = max(0.3, 0.4 * s)
        self.p = {n: np.array([cx + pos[n][0] * s, cy + pos[n][1] * s, 0.0]) for n in names}
        p = self.p
        self.atoms = {n: mk_atom(n, p[n], s, n in lit) for n in names}
        self.b = {"CO": mk_bond(p["C"], p["O"], co, r), "CN": mk_bond(p["C"], p["N"], cn, r, cn_col, 7 if cn_col != LIGHT else 5),
                  "NH": mk_bond(p["N"], p["H"], 1, r)}
        if ca:
            self.b["Ca1C"] = mk_bond(p["Ca1"], p["C"], 1, r)
            self.b["NCa2"] = mk_bond(p["N"], p["Ca2"], 1, r)
        d = np.array([np.cos(np.radians(38)), np.sin(np.radians(38)), 0.0])
        self.minus = charge("−", p["O"] + d * (r + 0.32 * max(1, s)), s)
        self.plus = charge("+", p["N"] + d * (r + 0.32 * max(1, s)), s)
        if not minus:
            self.minus.set_opacity(0)
        if not plus:
            self.plus.set_opacity(0)
        self.g = VGroup(*self.b.values(), *self.atoms.values(), self.minus, self.plus)

    def pts(self):
        return [self.p[n] for n in self.p]


def plane_of(cl, pad=0.3, fill=0.14):
    pts = padded_hull([q[:2] for q in cl.pts()], [cl.r + pad] * len(cl.p))
    return Polygon(*[np.array([x, y, 0.0]) for x, y in pts], stroke_color=ORANGE, stroke_width=3,
                   fill_color=ORANGE, fill_opacity=fill).set_z_index(-1)


PX = 3.35      # panel centres at +-PX
PC = -0.35     # panel cluster centre y
PS = 1.35      # panel cluster scale


def panel(cx, title):
    fr = RoundedRectangle(corner_radius=0.2, width=6.3, height=6.4, stroke_color=GREY, stroke_width=3).move_to([cx, -0.05, 0])
    tt = T(title, size=40, color=TEXT).move_to([cx, 2.6, 0])
    return fr, tt


def dim(cx):
    return RoundedRectangle(corner_radius=0.2, width=6.3, height=6.4, stroke_width=0, fill_color=BG, fill_opacity=0.62).move_to([cx, -0.05, 0]).set_z_index(5)


def pcl(cx, **kw):
    return Cl(cx=cx, cy=PC, s=PS, **kw)


def lock(sc=1.0, color=ORANGE):
    body = RoundedRectangle(corner_radius=0.08 * sc, width=0.62 * sc, height=0.5 * sc, stroke_color=TEXT, stroke_width=2.5,
                            fill_color=color, fill_opacity=1.0)
    sh = Arc(radius=0.2 * sc, start_angle=0, angle=PI, arc_center=body.get_top(), stroke_color=color, stroke_width=7 * sc)
    key = Dot(body.get_center(), radius=0.06 * sc, color=BG)
    return VGroup(sh, body, key).set_z_index(12)


def rot_arrow(center, ang, rl=0.6, rs=0.2, color=ORANGE, t0=-100, t1=140, sw=5):
    """A curved arrow that circles an axis lying along screen direction `ang` (radians)."""
    ts = np.radians(np.linspace(t0, t1, 40))
    loc = np.array([[rs * np.cos(t), rl * np.sin(t)] for t in ts])
    tan = np.array([-rs * np.sin(ts[-1]), rl * np.cos(ts[-1])])
    tan /= np.linalg.norm(tan)
    nrm = np.array([-tan[1], tan[0]])
    tip = loc[-1] + tan * 0.2
    b1, b2 = loc[-1] + nrm * 0.13, loc[-1] - nrm * 0.13
    R = np.array([[np.cos(ang), -np.sin(ang)], [np.sin(ang), np.cos(ang)]])
    f = lambda q: np.array([*(R @ q + np.array(center[:2])), 0.0])
    arc = VMobject(stroke_color=color, stroke_width=sw)
    arc.set_points_smoothly([f(q) for q in loc])
    head = Polygon(f(tip), f(b1), f(b2), stroke_width=1, stroke_color=color, fill_color=color, fill_opacity=1)
    return VGroup(arc, head).set_z_index(11)


# ================================================================== the computed backbone (s14-s21)
def _place(a, b, c, L, ang, tor):
    ang, tor = np.radians(ang), np.radians(tor)
    bc = unit(c - b)
    n = unit(np.cross(b - a, bc))
    m = np.cross(n, bc)
    d = np.array([-L * np.cos(ang), L * np.sin(ang) * np.cos(tor), L * np.sin(ang) * np.sin(tor)])
    return c + d[0] * bc + d[1] * m + d[2] * n


def backbone(phi=None, psi=None):
    """4 residues. phi[i], psi[i] for residue i (1..4), degrees; peptide bonds trans (omega 180)."""
    ph = {1: 180, 2: 180, 3: 180, 4: 180}
    ps = {1: 180, 2: 180, 3: 180, 4: 180}
    ph.update(phi or {})
    ps.update(psi or {})
    A = {"N1": np.array([0.0, 0, 0]), "A1": np.array([1.46, 0, 0])}
    t = np.radians(111)
    A["C1"] = A["A1"] + 1.52 * np.array([-np.cos(t), np.sin(t), 0])
    for i in range(1, 4):
        N, Ca, C = A[f"N{i}"], A[f"A{i}"], A[f"C{i}"]
        A[f"N{i+1}"] = _place(N, Ca, C, 1.33, 116, ps[i])
        A[f"A{i+1}"] = _place(Ca, C, A[f"N{i+1}"], 1.46, 122, 180)
        A[f"O{i}"] = _place(A[f"A{i+1}"], A[f"N{i+1}"], C, 1.23, 123, 0)
        A[f"H{i+1}"] = _place(Ca, C, A[f"N{i+1}"], 1.0, 119, 0)
        A[f"C{i+1}"] = _place(C, A[f"N{i+1}"], A[f"A{i+1}"], 1.52, 111, ph[i + 1])
    return A


REF = backbone()
_o = np.mean([REF[f"A{i}"] for i in range(1, 5)], axis=0)
_ex = unit(REF["A4"] - REF["A1"])
_ez = np.array([0.0, 0.0, 1.0])
_B = np.array([_ex, np.cross(_ez, _ex), _ez])
TILT = np.radians(-24)
_V = np.array([[1, 0, 0], [0, np.cos(TILT), -np.sin(TILT)], [0, np.sin(TILT), np.cos(TILT)]]) @ _B
SC = 1.12
OFF = np.array([0.0, 0.0])


def P3(A, name, off=None):
    q = _V @ (A[name] - _o)
    o = OFF if off is None else off
    return np.array([SC * q[0] + o[0], SC * q[1] + o[1], 0.0])


def depth(A, name):
    return (_V @ (A[name] - _o))[2]


PAD = 0.62   # padding (angstrom) around C, O, N, H in a card outline


def _card_atoms(k):
    return [f"A{k}", f"C{k}", f"O{k}", f"N{k+1}", f"H{k+1}", f"A{k+1}"]


def _card_frame(A, k):
    C, N, Ca = A[f"C{k}"], A[f"N{k+1}"], A[f"A{k}"]
    e1 = unit(N - C)
    e3 = unit(np.cross(e1, Ca - C))
    e2 = np.cross(e3, e1)
    return C, e1, e2, e3


def _outline_uv(k):
    C, e1, e2, _ = _card_frame(REF, k)
    names = _card_atoms(k)
    pts = [((REF[n] - C) @ e1, (REF[n] - C) @ e2) for n in names]
    pads = [0 if n.startswith("A") else PAD for n in names]
    return padded_hull(pts, pads, n=24)


OUT_UV = {k: _outline_uv(k) for k in (1, 2, 3)}
CARD_BONDS = lambda k: [(f"A{k}", f"C{k}", 1), (f"C{k}", f"O{k}", 2), (f"C{k}", f"N{k+1}", 1.5),
                        (f"N{k+1}", f"H{k+1}", 1), (f"N{k+1}", f"A{k+1}", 1)]


def card_poly(A, k, off=None, fill=None, sw=3):
    C, e1, e2, e3 = _card_frame(A, k)
    pts = []
    for u, v in OUT_UV[k]:
        X = C + u * e1 + v * e2
        q = _V @ (X - _o)
        o = OFF if off is None else off
        pts.append(np.array([SC * q[0] + o[0], SC * q[1] + o[1], 0.0]))
    nz = abs((_V @ e3)[2])
    f = (0.17 + 0.2 * nz) if fill is None else fill
    return Polygon(*pts, stroke_color=ORANGE, stroke_width=sw, fill_color=interpolate_color(ManimColor(BG), ManimColor(ORANGE), f), fill_opacity=1.0)


def bond_line(A, a, b, order=1, col=LIGHT, w=3, op=0.6, off=None):
    p, q = P3(A, a, off), P3(A, b, off)
    u = unit(q - p)
    ga = 0.0 if a.startswith("A") else 0.2
    gb = 0.0 if b.startswith("A") else 0.2
    p2, q2 = p + u * ga, q - u * gb
    if order == 1:
        return VGroup(Line(p2, q2, color=col, stroke_width=w, stroke_opacity=op))
    n = np.array([-u[1], u[0], 0.0]) * 0.055
    l2op = op if order == 2 else op * 0.5
    return VGroup(Line(p2 - n, q2 - n, color=col, stroke_width=w, stroke_opacity=op),
                  Line(p2 + n, q2 + n, color=col, stroke_width=w, stroke_opacity=l2op))


def chain_mob(A, hl=None, let_op=0.9, cards=(1, 2, 3), off=None, joints=True, stubs=True):
    """The card chain for atom set A. hl maps 'X-Y' bond names to (colour, width)."""
    hl = hl or {}
    groups = []
    for k in cards:
        g = VGroup(card_poly(A, k, off))
        for a, b, o in CARD_BONDS(k):
            key = f"{a}-{b}"
            if key in hl:
                col, w = hl[key]
                g.add(bond_line(A, a, b, o, col, w, 1.0, off))
            else:
                g.add(bond_line(A, a, b, o, off=off))
        for n in (f"C{k}", f"O{k}", f"N{k+1}", f"H{k+1}"):
            g.add(T(n[0], size=33, color=TEXT).set_opacity(let_op).move_to(P3(A, n, off)))
        dep = np.mean([depth(A, n) for n in _card_atoms(k)])
        groups.append((dep, g))
    groups.sort(key=lambda x: x[0])
    out = VGroup()
    if stubs:
        s1 = Line(P3(A, "A1", off), P3(A, "A1", off) + (P3(A, "N1", off) - P3(A, "A1", off)) * 0.8,
                  color=LIGHT, stroke_width=3, stroke_opacity=0.45)
        s4 = Line(P3(A, "A4", off), P3(A, "A4", off) + (P3(A, "C4", off) - P3(A, "A4", off)) * 0.8,
                  color=LIGHT, stroke_width=3, stroke_opacity=0.45)
        out.add(VGroup(s1, s4))
    else:
        out.add(VGroup())
    out.add(VGroup(*[g for _, g in groups]))
    if joints:
        lo, hi = min(cards), max(cards) + 1
        out.add(VGroup(*[Dot(P3(A, f"A{j}", off), radius=0.13, color=TEXT).set_z_index(8) for j in range(lo, hi + 1)]))
    else:
        out.add(VGroup())
    return out


def bond_mid(A, a, b, off=None):
    return (P3(A, a, off) + P3(A, b, off)) / 2


def bond_ang(A, a, b, off=None):
    d = P3(A, b, off) - P3(A, a, off)
    return np.arctan2(d[1], d[0])


def axis_line(A, a, b, ext=1.4, off=None):
    p, q = P3(A, a, off), P3(A, b, off)
    u = unit(q - p)
    return DashedLine(p - u * ext, q + u * ext, color=TEXT, stroke_width=3, dash_length=0.14).set_z_index(10)


def hinge_arrow(A, a, b, off=None, rl=0.48, rs=0.17):
    return rot_arrow(bond_mid(A, a, b, off), bond_ang(A, a, b, off), rl=rl, rs=rs)


def out_dir(A, j):
    """Screen direction pointing away from the cards that meet at joint j."""
    near = []
    if j - 1 >= 1:
        near += [P3(A, n) for n in _card_atoms(j - 1)]
    if j <= 3:
        near += [P3(A, n) for n in _card_atoms(j)]
    return unit(P3(A, f"A{j}") - np.mean(near, axis=0))


# ================================================================== scenes
class S00Title(TitleCard):
    LESSON = "Protein three-dimensional structure: the sequence sets the shape"
    TITLE = "Two Hinges per Residue"


Q01 = "Can it bend any way at all?"
BC_LAST = 3     # seed of the last bead-chain shape in s01


def _clear_link():
    """The link with the most free space around it (so the zoom lands on an uncluttered spot)."""
    _, P = beadchain(BC_LAST)
    best, bi = -1, 0
    for i in range(10, len(P) - 11):
        m = (P[i] + P[i + 1]) / 2
        d = np.hypot(*(P - m).T)
        d[max(0, i - 6):i + 8] = 99
        if d.min() > best:
            best, bi = d.min(), i
    return bi


LINK = _clear_link()   # the link the camera zooms in on (between beads LINK and LINK+1)


class S01(SpokenScene):
    def construct(self):
        ch, _ = beadchain(0)
        tag = T("a chain of 100 residues", size=40, color=TEXT).move_to([0, -3.35, 0])
        q = T(Q01, size=50, color=TEXT).move_to([0, 3.3, 0])
        self.play(Create(ch[0]), LaggedStart(*[FadeIn(b) for b in ch[1:]], lag_ratio=0.01), run_time=0.9)
        self.at("hundred residues", lead=0.0)
        self.play(FadeIn(tag, shift=UP * 0.1), run_time=0.5)
        self.at("bend any way")
        for sd in (1, 2, BC_LAST):
            self.play(Transform(ch, beadchain(sd)[0]), run_time=0.68, rate_func=smooth)
        self.at("Can it", lead=0.0)
        self.play(FadeIn(q, shift=DOWN * 0.1), run_time=0.45)
        self.finish()


def big_pair():
    bl, br = bead(-3.7, CY, 1.2), bead(3.7, CY, 1.2)
    link = Line([-2.5, CY, 0], [2.5, CY, 0], color=ORANGE, stroke_width=9)
    labs = VGroup(T("residue", size=34, color=BLUE).move_to(bl), T("residue", size=34, color=BLUE).move_to(br))
    return bl, br, link, labs


def pep_label():
    lab = T("peptide bond", size=42, color=ORANGE).move_to([0, CY - 2.0, 0])
    arr = Arrow(lab.get_top() + UP * 0.05, [0, CY - 0.18, 0], buff=0.08, color=ORANGE, stroke_width=5,
                max_tip_length_to_length_ratio=0.25)
    return VGroup(lab, arr)


class S02(SpokenScene):
    def construct(self):
        ch, P = beadchain(BC_LAST)
        q = T(Q01, size=50, color=TEXT).move_to([0, 3.3, 0])
        tag = T("a chain of 100 residues", size=40, color=TEXT).move_to([0, -3.35, 0])
        self.add(ch, q, tag)
        a, b = P[LINK], P[LINK + 1]
        mid = np.array([(a[0] + b[0]) / 2, (a[1] + b[1]) / 2, 0.0])
        ring = Circle(radius=0.42, stroke_color=ORANGE, stroke_width=4).move_to(mid)
        link = Line([a[0], a[1], 0], [b[0], b[1], 0], color=ORANGE, stroke_width=9)
        self.at("the bond that")
        self.play(FadeOut(q), FadeOut(tag), Create(ring), FadeIn(link), run_time=0.4)
        # zoom: the whole chain grows about that link, turned so the link lies flat
        ang = np.arctan2(b[1] - a[1], b[0] - a[0])
        f = 7.4 / np.hypot(b[0] - a[0], b[1] - a[1])
        world = VGroup(ch, link)
        bl, br, big, labs = big_pair()

        base = world.copy()

        def zoom(m, al):
            m.become(base.copy())
            m.rotate(-ang * al, about_point=mid).shift(-mid * al)
            m.scale(1 + (f - 1) * al ** 2, about_point=ORIGIN)
            for i, b_ in enumerate(m[0][1:]):
                if i not in (LINK, LINK + 1):
                    b_.set_opacity(1 - al)
        self.play(FadeOut(ring), UpdateFromAlphaFunc(world, lambda m, al: zoom(m, smooth(al))), run_time=0.75)
        b0, b1 = world[0][1 + LINK], world[0][2 + LINK]
        self.play(ReplacementTransform(b0, bl), ReplacementTransform(b1, br), ReplacementTransform(world[1], big),
                  FadeOut(world[0][0]), run_time=0.2)
        self.remove(world)
        self.add(bl, br, big)
        self.at("one residue", lead=0.0)
        self.play(FadeIn(labs[0]), Indicate(bl, color=BLUE, scale_factor=1.06), run_time=0.4)
        self.at("to the next", lead=0.0)
        self.play(FadeIn(labs[1]), Indicate(br, color=BLUE, scale_factor=1.06), run_time=0.4)
        pl = pep_label()
        pre = T("the bond", size=42, color=ORANGE).move_to(pl[0])
        self.play(FadeIn(pre), GrowArrow(pl[1]), run_time=0.25)
        self.at("peptide bond", lead=0.1)
        self.play(ReplacementTransform(pre, pl[0]), run_time=0.25)
        self.finish()


class S03(SpokenScene):
    def construct(self):
        bl, br, link, labs = big_pair()
        pl = pep_label()
        self.add(bl, br, link, labs, pl)
        self.play(FadeOut(pl), run_time=0.4)
        full = Cl()
        self.at("the carbon", lead=0.0)
        self.play(FadeIn(full.atoms["C"], scale=0.6), link.animate.set_color(GREY).set_stroke(width=6), run_time=0.5)
        self.at("CO group", lead=0.0)
        self.play(Create(full.b["CO"]), FadeIn(full.atoms["O"], scale=0.6), run_time=0.6)
        self.at("the nitrogen", lead=0.0)
        full.b["CN"].set_color(ORANGE)
        self.play(FadeIn(full.atoms["N"], scale=0.6), Create(full.b["CN"]), run_time=0.6)
        self.at("NH group", lead=0.0)
        self.play(Create(full.b["NH"]), FadeIn(full.atoms["H"], scale=0.6), run_time=0.6)
        self.finish()


class S04(SpokenScene):
    def construct(self):
        bl, br, link, labs = big_pair()
        link.set_color(GREY).set_stroke(width=6)
        cl = Cl(cn_col=ORANGE)
        self.add(bl, br, link, labs, cl.g)
        f1, t1 = panel(-PX, "form 1")
        f2, t2 = panel(PX, "form 2")
        a = pcl(-PX)
        b = pcl(PX)
        self.play(FadeOut(VGroup(bl, br, link, labs)), run_time=0.6)
        self.at("two ways")
        self.play(Transform(cl.g, a.g), TransformFromCopy(cl.g, b.g), Create(f1), Create(f2),
                  FadeIn(t1), FadeIn(t2), run_time=0.9)
        self.finish()


def lbl_near(cl, a, b, text, side=1, dist=0.62, color=LIGHT, size=36):
    """Label beside the bond a-b, on the left (+1) or right (-1) of the direction a->b."""
    p, q = cl.p[a], cl.p[b]
    u = unit(q - p)
    n = np.array([-u[1], u[0], 0.0]) * side
    t = T(text, size=size, color=color)
    m = (p + q) / 2
    t.move_to(m + n * (dist + 0.5 * abs(n[0]) * t.width / 1.0 * 0.6 + 0.5 * abs(n[1]) * t.height))
    return t


def s05_labels(a):
    tdb = lbl_near(a, "C", "O", "double", side=-1, color=LIGHT)
    tsg = T("single", size=36, color=ORANGE).move_to((a.p["C"] + a.p["N"]) / 2 + DOWN * 0.62)
    return tdb, tsg


class S05(SpokenScene):
    def construct(self):
        f1, t1 = panel(-PX, "form 1")
        f2, t2 = panel(PX, "form 2")
        a = pcl(-PX)
        b = pcl(PX)
        ov = dim(PX)
        self.add(f1, f2, t1, t2, a.g, b.g)
        self.play(FadeIn(ov), run_time=0.4)
        tdb, tsg = s05_labels(a)
        self.at("share a double", lead=0.0)
        self.play(Transform(a.g, pcl(-PX, co=2).g), FadeIn(tdb), run_time=0.5)
        self.at("The bond from")
        self.play(Transform(a.g, pcl(-PX, co=2, cn_col=ORANGE).g), run_time=0.5)
        self.at("single", lead=0.0)
        self.play(FadeIn(tsg, shift=DOWN * 0.1), run_time=0.4)
        self.finish()


def s06_labels(b):
    return T("double", size=36, color=ORANGE).move_to((b.p["C"] + b.p["N"]) / 2 + DOWN * 0.62)


class S06(SpokenScene):
    def construct(self):
        f1, t1 = panel(-PX, "form 1")
        f2, t2 = panel(PX, "form 2")
        a = pcl(-PX, co=2, cn_col=ORANGE)
        b = pcl(PX)
        ov2, ov1 = dim(PX), dim(-PX)
        tdb, tsg = s05_labels(a)
        self.add(f1, f2, t1, t2, a.g, b.g, tdb, tsg, ov2)
        self.play(FadeOut(ov2), FadeIn(ov1), run_time=0.5)
        self.at("negative charge", lead=0.0)
        self.play(Transform(b.g, pcl(PX, minus=True).g), run_time=0.45)
        self.at("share a double", lead=0.0)
        tdn = s06_labels(b)
        self.play(Transform(b.g, pcl(PX, cn=2, cn_col=ORANGE, minus=True).g), FadeIn(tdn), run_time=0.5)
        self.at("positive charge", lead=0.0)
        self.play(Transform(b.g, pcl(PX, cn=2, cn_col=ORANGE, minus=True, plus=True).g), run_time=0.45)
        self.finish()


def blend(**kw):
    return Cl(cx=0, cy=CY, s=1.35, co=2, cn=1.5, cn_col=ORANGE, **kw)


def partial_label(cl):
    lab = T("partial double-bond character", size=40, color=ORANGE).move_to([0, -3.2, 0])
    ln = leader(lab, (cl.p["C"] + cl.p["N"]) / 2 + DOWN * 0.12, color=ORANGE)
    return VGroup(lab, ln)


class S07(SpokenScene):
    def construct(self):
        f1, t1 = panel(-PX, "form 1")
        f2, t2 = panel(PX, "form 2")
        a = pcl(-PX, co=2, cn_col=ORANGE)
        b = pcl(PX, cn=2, cn_col=ORANGE, minus=True, plus=True)
        tdb, tsg = s05_labels(a)
        tdn = s06_labels(b)
        ov1 = dim(-PX)
        self.add(f1, f2, t1, t2, a.g, b.g, tdb, tsg, tdn, ov1)
        # the two drawings are two views of one bond: a resonance arrow between them
        a_s, b_s = Cl(cx=-3.9, cy=PC, s=1.1, co=2, cn_col=ORANGE), Cl(cx=3.9, cy=PC, s=1.1, cn=2, cn_col=ORANGE, minus=True, plus=True)
        dbl = DoubleArrow([-1.15, PC, 0], [1.15, PC, 0], buff=0, color=TEXT, stroke_width=6, tip_length=0.3)
        self.at("real bond")
        self.play(FadeOut(ov1), FadeOut(VGroup(f1, f2, tdb, tsg, tdn)), Transform(a.g, a_s.g), Transform(b.g, b_s.g),
                  t1.animate.move_to([-3.9, 2.4, 0]), t2.animate.move_to([3.9, 2.4, 0]), run_time=0.7)
        self.at("blend", lead=0.0)
        bl = T("a blend", size=40, color=TEXT).next_to(dbl, UP, buff=0.25)
        self.play(GrowFromCenter(dbl), FadeIn(bl), run_time=0.5)
        tgt = blend()
        tgt2 = blend()
        tgt2.g.set_opacity(0)
        self.at("so the bond")
        self.play(FadeOut(VGroup(t1, t2, dbl, bl)), Transform(a.g, tgt.g), Transform(b.g, tgt2.g), run_time=1.1)
        self.remove(b.g)
        pl = partial_label(tgt)
        self.at("partly double", lead=0.0)
        self.play(FadeIn(pl[0], shift=UP * 0.1), Create(pl[1]), run_time=0.5)
        self.finish()


RY = CY - 1.0   # ruler height


def ruler_objs(cl):
    x0, x1 = cl.p["C"][0], cl.p["N"][0]
    rule = DoubleArrow([x0, RY, 0], [x1, RY, 0], buff=0, color=TEXT, stroke_width=4, tip_length=0.2)
    t0 = Line([x0, RY - 0.16, 0], [x0, RY + 0.16, 0], color=TEXT, stroke_width=4)
    t1 = Line([x1, RY - 0.16, 0], [x1, RY + 0.16, 0], color=TEXT, stroke_width=4)
    val = T("1.32 Å", size=40, color=TEXT, weight=BOLD)
    val.move_to([0, RY - 0.5, 0])
    return VGroup(rule, t0, t1), val


def ref_bar(cl):
    x0, x1 = cl.p["C"][0], cl.p["N"][0]
    L = (x1 - x0) * 1.47 / 1.32          # a plain C-N single bond, same scale
    y = RY - 1.55
    bar = Line([x0, y, 0], [x0 + L, y, 0], color=GREY, stroke_width=5, stroke_opacity=0.7)
    e0 = Line([x0, y - 0.13, 0], [x0, y + 0.13, 0], color=GREY, stroke_width=4, stroke_opacity=0.7)
    e1 = Line([x0 + L, y - 0.13, 0], [x0 + L, y + 0.13, 0], color=GREY, stroke_width=4, stroke_opacity=0.7)
    t = T("an ordinary single C–N bond is longer", size=36, color=GREY).move_to([0, y - 0.45, 0])
    return VGroup(bar, e0, e1, t)


class S08(SpokenScene):
    def construct(self):
        cl = blend()
        pl = partial_label(cl)
        self.add(cl.g, pl)
        self.play(FadeOut(pl), run_time=0.35)
        rule, val = ruler_objs(cl)
        ref = ref_bar(cl)
        self.at("makes it short", lead=0.0)
        self.play(Create(rule), FadeIn(ref), run_time=0.6)
        self.at("about 1 32", lead=0.0)
        self.play(FadeIn(val, shift=UP * 0.1), run_time=0.45)
        self.finish()


class S09(SpokenScene):
    def construct(self):
        cl = blend()
        rule, val = ruler_objs(cl)
        ref = ref_bar(cl)
        self.add(cl.g, rule, val, ref)
        self.play(FadeOut(VGroup(rule, val, ref)), run_time=0.4)
        mid = (cl.p["C"] + cl.p["N"]) / 2
        arr = rot_arrow(mid, 0.0, rl=0.85, rs=0.3)
        right = VGroup(cl.atoms["N"], cl.atoms["H"], cl.b["NH"])
        self.at("cannot twist")
        self.play(Create(arr[0]), FadeIn(arr[1]), run_time=0.5)
        self.at("without losing")
        for _ in range(2):
            self.play(right.animate.stretch(0.3, 1, about_point=mid), Rotate(arr, 0.5, about_point=mid), run_time=0.35, rate_func=smooth)
            self.play(right.animate.stretch(1 / 0.3, 1, about_point=mid), Rotate(arr, -0.5, about_point=mid), run_time=0.25, rate_func=rush_from)
        self.at("does not rotate", lead=0.0)
        lk = lock(1.8).move_to(mid + UP * 1.3)
        tl = T("no rotation", size=40, color=ORANGE).move_to([3.9, 1.6, 0])
        self.play(FadeOut(arr), FadeIn(lk, scale=1.4), FadeIn(tl), run_time=0.5)
        self.finish()


class S10(SpokenScene):
    def construct(self):
        cl = blend()
        mid = (cl.p["C"] + cl.p["N"]) / 2
        lk = lock(1.8).move_to(mid + UP * 1.3)
        tl = T("no rotation", size=40, color=ORANGE).move_to([3.9, 1.6, 0])
        self.add(cl.g, lk, tl)
        full = Cl(ca=True, co=2, cn=1.5, cn_col=ORANGE)
        pl = plane_of(full)
        lab = T("one flat\nplane", size=42, color=ORANGE, line_spacing=0.8).move_to([-5.35, 1.2, 0])
        self.play(FadeOut(lk), FadeOut(tl), run_time=0.3)
        self.at("atoms", lead=0.1)
        self.play(FadeIn(full.atoms["Ca1"], scale=0.6), FadeIn(full.atoms["Ca2"], scale=0.6),
                  Create(full.b["Ca1C"]), Create(full.b["NCa2"]), run_time=0.5)
        self.at("flat plane", lead=0.1)
        self.play(FadeIn(pl), FadeIn(lab), run_time=0.5)
        self.finish()


def full6(**kw):
    return Cl(ca=True, co=2, cn=1.5, cn_col=ORANGE, **kw)


def res_labels(cl):
    r1 = T("first\nresidue", size=38, color=BLUE, line_spacing=0.8).move_to([-5.35, -2.0, 0])
    r2 = T("next\nresidue", size=38, color=BLUE, line_spacing=0.8).move_to([5.35, 2.2, 0])
    l1 = leader(r1, cl.p["Ca1"] + LEFT * cl.r, color=BLUE)
    l2 = leader(r2, cl.p["Ca2"] + RIGHT * cl.r, color=BLUE)
    return VGroup(r1, l1), VGroup(r2, l2)


class S11(SpokenScene):
    def construct(self):
        cl = full6()
        pl = plane_of(cl)
        lab = T("one flat\nplane", size=42, color=ORANGE, line_spacing=0.8).move_to([-5.35, 1.2, 0])
        self.add(pl, cl.g, lab)
        self.play(FadeOut(lab), run_time=0.3)
        state = {"cur": None}

        def light(name):
            anims = []
            if state["cur"]:
                anims.append(Transform(cl.atoms[state["cur"]], mk_atom(state["cur"], cl.p[state["cur"]], 1.35, False)))
            anims.append(Transform(cl.atoms[name], mk_atom(name, cl.p[name], 1.35, True)))
            state["cur"] = name
            self.play(*anims, run_time=0.35)

        r1, r2 = res_labels(cl)
        self.at("alpha carbon", lead=0.0)
        light("Ca1")
        self.at("first residue", lead=0.0)
        self.play(FadeIn(r1), run_time=0.4)
        self.at("its carbon", lead=0.0)
        light("C")
        self.at("oxygen", lead=0.0)
        light("O")
        self.at("the nitrogen", lead=0.0)
        light("N")
        self.at("hydrogen", lead=0.0)
        light("H")
        self.at("next residue", lead=0.0)
        self.play(FadeIn(r2), run_time=0.4)
        self.at("and that residues alpha carbon", lead=0.0)
        light("Ca2")
        self.finish()


def axis_ext(cl, ext=1.5):
    """Dashed extensions of the C-N bond axis, drawn only outside the atoms."""
    y = cl.p["C"][1]
    l = DashedLine(cl.p["C"] + LEFT * (cl.r + ext), cl.p["C"] + LEFT * (cl.r + 0.08), color=TEXT, stroke_width=3, dash_length=0.14)
    r = DashedLine(cl.p["N"] + RIGHT * (cl.r + 0.08), cl.p["N"] + RIGHT * (cl.r + ext), color=TEXT, stroke_width=3, dash_length=0.14)
    return VGroup(l, r)


def trans_label():
    return T("trans", size=54, color=ORANGE, weight=BOLD).move_to([5.3, -0.6, 0])


class S12(SpokenScene):
    def construct(self):
        cl = full6(lit=("Ca2",))
        pl = plane_of(cl)
        r1, r2 = res_labels(cl)
        self.add(pl, cl.g, r1, r2)
        self.play(FadeOut(r1), FadeOut(r2), Transform(cl.atoms["Ca2"], mk_atom("Ca2", cl.p["Ca2"], 1.35, False)), run_time=0.4)
        self.at("two alpha carbons", lead=0.0)
        self.play(Transform(cl.atoms["Ca1"], mk_atom("Ca1", cl.p["Ca1"], 1.35, True)),
                  Transform(cl.atoms["Ca2"], mk_atom("Ca2", cl.p["Ca2"], 1.35, True)), run_time=0.5)
        ax = axis_ext(cl)
        self.at("opposite sides", lead=0.0)
        self.play(Create(ax), run_time=0.6)
        self.play(Indicate(cl.atoms["Ca1"], color=ORANGE, scale_factor=1.15), Indicate(cl.atoms["Ca2"], color=ORANGE, scale_factor=1.15), run_time=0.8)
        self.at("the transform", lead=0.0)
        self.play(FadeIn(trans_label(), shift=LEFT * 0.1), run_time=0.5)
        self.finish()


C13Y = 0.6
S13S = 1.05


def side(cx, cis, lit=()):
    cl = Cl(cx=cx, cy=C13Y, s=S13S, cis=cis, ca=True, co=2, cn=1.5, cn_col=ORANGE, lit=lit)
    return cl, plane_of(cl, pad=0.22)


def s13_end():
    tl, tpl = side(-3.3, False, lit=("Ca1", "Ca2"))
    cs, cpl = side(3.3, True, lit=("Ca1", "Ca2"))
    tr2 = T("trans", size=44, color=ORANGE, weight=BOLD).move_to([-3.3, -2.45, 0])
    ctxt = T("cis", size=44, color=ORANGE, weight=BOLD).move_to([2.75, -2.45, 0])
    rare = chip("rare", ORANGE, size=36).move_to([3.85, -2.45, 0])
    t1 = T("more common at X–", size=40, color=TEXT)
    t2 = T("Pro", size=40, color=ORANGE, weight=BOLD)
    t3 = T("bonds", size=40, color=TEXT)
    VGroup(t1, t2).arrange(RIGHT, buff=0.06, aligned_edge=DOWN)
    t3.next_to(t2, RIGHT, buff=0.2).align_to(t1, DOWN)
    VGroup(t1, t2, t3).move_to([0, -3.3, 0])
    return tl, tpl, cs, cpl, tr2, ctxt, rare, t1, t2, t3


class S13(SpokenScene):
    def construct(self):
        cl = full6(lit=("Ca1", "Ca2"))
        pl = plane_of(cl)
        ax = axis_ext(cl)
        tr = trans_label()
        self.add(pl, cl.g, ax, tr)
        tl, tpl, cs, cpl, tr2, ctxt, rare, t1, t2, t3 = s13_end()
        self.play(FadeOut(ax), ReplacementTransform(tr, tr2), Transform(cl.g, tl.g), Transform(pl, tpl), run_time=0.45)
        cs0, _ = side(3.3, True)
        self.at("cis", lead=0.0)
        self.play(FadeIn(cpl), FadeIn(cs0.g), run_time=0.5)
        self.at("same side", lead=0.0)
        self.play(Transform(cs0.g, cs.g), FadeIn(ctxt), run_time=0.5)
        self.at("rare", lead=0.0)
        self.play(FadeIn(rare, shift=LEFT * 0.1), run_time=0.4)
        self.at("more common", lead=0.0)
        self.play(FadeIn(t1, shift=UP * 0.1), FadeIn(t3, shift=UP * 0.1), run_time=0.4)
        self.at("proline", lead=0.0)
        self.add(t2)
        self.play(Indicate(t2, color=ORANGE, scale_factor=1.25), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------- chain scenes
TAG_OFF = {1: np.array([0.15, -0.72, 0]), 2: np.array([0.0, 0.62, 0]), 3: np.array([0.0, -0.62, 0]), 4: np.array([-0.15, -0.72, 0])}


def joint_tags(A, js=(1, 2, 3, 4)):
    return VGroup(*[CA(38, TEXT).move_to(P3(A, f"A{j}") + TAG_OFF[j]) for j in js])


def pep_bond_note(A):
    labs, lines = VGroup(), VGroup()
    for k, x in zip((1, 2, 3), (-4.3, 0.0, 4.3)):
        v = card_poly(A, k).get_vertices()
        b = v[np.argmin(v[:, 1])]
        lab = T("peptide bond", size=36, color=TEXT).move_to([x, -3.3, 0])
        labs.add(lab)
        lines.add(Line(lab.get_top() + UP * 0.08, b + DOWN * 0.08, color=GREY, stroke_width=2.5))
    return VGroup(labs, lines)


class S14(SpokenScene):
    def construct(self):
        tl, tpl, cs, cpl, tr2, ctxt, rare, t1, t2, t3 = s13_end()
        self.add(tpl, tl.g, cpl, cs.g, tr2, ctxt, rare, t1, t2, t3)
        A = REF
        full = chain_mob(A)
        stubs, cards, joints = full
        # card 1 is the trans plane: morph it in place
        c1 = [g for g in cards if True][0]
        k1 = None
        for g in cards:
            if np.allclose(g[0].get_center(), card_poly(A, 1).get_center(), atol=1e-3):
                k1 = g
        rest = VGroup(*[g for g in cards if g is not k1])
        self.play(FadeOut(VGroup(cpl, cs.g, tr2, ctxt, rare, t1, t2, t3)), run_time=0.5)
        letters = {"C": k1[6], "O": k1[7], "N": k1[8], "H": k1[9]}
        anims = [Transform(tpl, k1[0])]
        for n, m in letters.items():
            anims.append(ReplacementTransform(tl.atoms[n][1], m))
            anims.append(FadeOut(tl.atoms[n][0]))
        for kb, (bn) in zip(("Ca1C", "CO", "CN", "NH", "NCa2"), (1, 2, 3, 4, 5)):
            anims.append(ReplacementTransform(tl.b[kb], k1[bn]))
        anims.append(ReplacementTransform(tl.atoms["Ca1"], joints[0]))
        anims.append(ReplacementTransform(tl.atoms["Ca2"], joints[1]))
        self.play(*anims, run_time=1.0)
        self.remove(tpl)
        self.add(k1)
        self.at("string of flat")
        grow = []
        for g in rest:
            grow.append(FadeIn(g, scale=0.7))
        self.play(LaggedStart(*grow, lag_ratio=0.45), LaggedStart(*[GrowFromCenter(d) for d in joints[2:]], lag_ratio=0.45),
                  FadeIn(stubs), run_time=1.6)
        note = pep_bond_note(A)
        self.at("one card", lead=0.0)
        self.play(FadeIn(note[0]), Create(note[1]), run_time=0.6)
        self.finish()


class S15(SpokenScene):
    def construct(self):
        A = REF
        self.add(chain_mob(A))
        note = pep_bond_note(A)
        self.add(note)
        self.play(FadeOut(note), run_time=0.4)
        tags = joint_tags(A)
        dots = VGroup(*[Dot(P3(A, f"A{j}"), radius=0.2, color=TEXT).set_z_index(9) for j in range(1, 5)])
        self.at("joined", lead=0.0)
        self.play(LaggedStart(*[Flash(d, color=TEXT, line_length=0.2, flash_radius=0.35) for d in dots], lag_ratio=0.15), run_time=0.7)
        self.at("alpha carbon", lead=0.0)
        self.play(LaggedStart(*[FadeIn(t) for t in tags], lag_ratio=0.1), run_time=0.6)
        self.at("Watch what")
        self.play(*[Indicate(d, scale_factor=1.6, color=ORANGE) for d in dots], run_time=0.9)
        self.finish()


# the joint everything happens at: Ca2 (top apex). Its three bonds in a row: N2-A2, A2-C2, C2-N3
HL3 = {"N2-A2": (TEXT, 7), "A2-C2": (TEXT, 7), "C2-N3": (TEXT, 7)}


def s16_labels(A, stage):
    """stage 0: names; 1: C-N locked; 2: both hinges turn."""
    j = P3(A, "A2")
    nl = G("N–Cα" + (": turns" if stage >= 2 else ""), size=38, color=(ORANGE if stage >= 2 else TEXT)).move_to([j[0] - 3.0, 3.3, 0])
    cl = G("Cα–C" + (": turns" if stage >= 2 else ""), size=38, color=(ORANGE if stage >= 2 else TEXT)).move_to([j[0] + 3.0, 3.3, 0])
    pl = G("C–N" + (": locked" if stage >= 1 else ""), size=38, color=(ORANGE if stage >= 1 else TEXT)).move_to([bond_mid(A, "C2", "N3")[0] + 1.2, -3.3, 0])
    ln = leader(nl, bond_mid(A, "N2", "A2"))
    lc = leader(cl, bond_mid(A, "A2", "C2"))
    lp = leader(pl, bond_mid(A, "C2", "N3") + DOWN * 0.05)
    return VGroup(nl, ln), VGroup(cl, lc), VGroup(pl, lp)


def s16_lock(A):
    m = bond_mid(A, "C2", "N3")
    a = bond_ang(A, "C2", "N3")
    return lock(1.0).move_to(m + 0.5 * np.array([-np.sin(a), np.cos(a), 0]))


class S16(SpokenScene):
    def construct(self):
        A = REF
        base = chain_mob(A)
        tags = joint_tags(A)
        self.add(base, tags)
        self.play(FadeOut(tags), run_time=0.4)
        hl = chain_mob(A, hl=HL3)
        L0 = s16_labels(A, 0)
        self.at("backbone bonds", lead=0.0)
        self.play(Transform(base, hl), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(l) for l in L0], lag_ratio=0.3), run_time=0.9)
        L1 = s16_labels(A, 1)
        hl1 = dict(HL3, **{"C2-N3": (ORANGE, 9)})
        lk = s16_lock(A)
        self.at("frozen", lead=0.0)
        self.play(Transform(base, chain_mob(A, hl=hl1)), Transform(L0[2], L1[2]), FadeIn(lk, scale=1.4), run_time=0.6)
        L2 = s16_labels(A, 2)
        ap = hinge_arrow(A, "N2", "A2")
        aq = hinge_arrow(A, "A2", "C2")
        self.at("Only two can turn", lead=0.1)
        self.play(FadeIn(ap), FadeIn(aq), Transform(L0[0], L2[0]), Transform(L0[1], L2[1]), run_time=0.3)
        tag = CA(40, TEXT).move_to(P3(A, "A2") + TAG_OFF[2])
        self.at("one on each side", lead=0.0)
        self.play(FadeIn(tag), Indicate(base[2][1], scale_factor=2.0, color=ORANGE), run_time=0.8)
        self.finish()


def s16_end(A):
    hl1 = dict(HL3, **{"C2-N3": (ORANGE, 9)})
    L2 = s16_labels(A, 2)
    L1 = s16_labels(A, 1)
    return chain_mob(A, hl=hl1), VGroup(L2[0], L2[1], L1[2]), s16_lock(A), hinge_arrow(A, "N2", "A2"), hinge_arrow(A, "A2", "C2"), CA(40, TEXT).move_to(P3(A, "A2") + TAG_OFF[2])


def phi_labels():
    nm = G("rotation about the N–Cα bond", size=36, color=TEXT).move_to([-3.3, 3.3, 0])
    nml = leader(nm, bond_mid(REF, "N2", "A2"))
    ph = G("= φ  (phi)", size=50, color=ORANGE).next_to(nm, RIGHT, buff=0.3)
    return nm, nml, ph


def psi_labels():
    nm = G("rotation about the Cα–C bond", size=36, color=TEXT).move_to([-3.3, 3.3, 0])
    nml = leader(nm, bond_mid(REF, "A2", "C2"))
    ph = G("= ψ  (psi)", size=50, color=ORANGE).next_to(nm, RIGHT, buff=0.3)
    return nm, nml, ph


PHI_SWING = 250     # phi of residue 2 after the swing in s17 (from 180)
PSI_SWING = 250     # psi of residue 2 after the swing in s18 (from 180)


class S17(SpokenScene):
    def construct(self):
        base, labs, lk, ap, aq, tag = s16_end(REF)
        self.add(base, labs, lk, ap, aq, tag)
        th = ValueTracker(180.0)
        hl = {"N2-A2": (TEXT, 7)}
        chain = always_redraw(lambda: chain_mob(backbone(phi={2: th.get_value()}), hl=hl))
        self.play(FadeOut(VGroup(labs, lk, ap, aq, tag)), Transform(base, chain_mob(REF, hl=hl)), run_time=0.6)
        self.remove(base)
        self.add(chain)
        ax = axis_line(REF, "N2", "A2", ext=1.2)
        arr = hinge_arrow(REF, "N2", "A2", rl=0.55, rs=0.2)
        self.at("hinge turn")
        self.play(Create(ax), FadeIn(arr), run_time=0.45)
        self.play(th.animate.set_value(PHI_SWING), run_time=1.7, rate_func=smooth)
        self.at("the bond from nitrogen", lead=0.0)
        hl["N2-A2"] = (ORANGE, 10)
        nm, nml, ph = phi_labels()
        self.play(FadeIn(nm), Create(nml), run_time=0.5)
        self.at("phi", lead=0.0)
        self.play(FadeIn(ph, shift=DOWN * 0.1), run_time=0.4)
        self.finish()


def s17_end():
    A = backbone(phi={2: PHI_SWING})
    hl = {"N2-A2": (ORANGE, 10)}
    nm, nml, ph = phi_labels()
    return chain_mob(A, hl=hl), axis_line(REF, "N2", "A2", ext=1.2), hinge_arrow(REF, "N2", "A2", rl=0.55, rs=0.2), VGroup(nm, nml, ph)


class S18(SpokenScene):
    def construct(self):
        base, ax, arr, labs = s17_end()
        self.add(base, ax, arr, labs)
        ph = ValueTracker(PHI_SWING)
        ps = ValueTracker(180.0)
        hl = {}
        chain = always_redraw(lambda: chain_mob(backbone(phi={2: ph.get_value()}, psi={2: ps.get_value()}), hl=hl))
        self.remove(base)
        self.add(chain)
        self.play(FadeOut(VGroup(ax, arr, labs)), ph.animate.set_value(180.0), run_time=0.9, rate_func=smooth)
        hl["A2-C2"] = (TEXT, 7)
        ax2 = axis_line(REF, "A2", "C2", ext=1.2)
        arr2 = hinge_arrow(REF, "A2", "C2", rl=0.55, rs=0.2)
        self.at("other", lead=0.0)
        self.play(Create(ax2), FadeIn(arr2), run_time=0.45)
        self.play(ps.animate.set_value(PSI_SWING), run_time=1.7, rate_func=smooth)
        self.at("the bond from the alpha", lead=0.0)
        hl["A2-C2"] = (ORANGE, 10)
        nm, nml, psl = psi_labels()
        self.play(FadeIn(nm), Create(nml), run_time=0.5)
        self.at("psi", lead=0.0)
        self.play(FadeIn(psl, shift=DOWN * 0.1), run_time=0.4)
        self.finish()


def s18_end():
    A = backbone(psi={2: PSI_SWING})
    hl = {"A2-C2": (ORANGE, 10)}
    nm, nml, psl = psi_labels()
    return chain_mob(A, hl=hl), axis_line(REF, "A2", "C2", ext=1.2), hinge_arrow(REF, "A2", "C2", rl=0.55, rs=0.2), VGroup(nm, nml, psl)


# ---------------------------------------------------------------- dials (s19-s20)
# target hinge settings for the "after" chain in s19 (degrees)
BEND = {"phi2": 120.0, "psi2": -150.0, "phi3": 90.0, "psi3": -180.0}
DIAL_POS = {"phi2": np.array([-3.6, 3.22, 0]), "psi2": np.array([-1.6, 3.22, 0]),
            "phi3": np.array([1.6, -3.22, 0]), "psi3": np.array([3.6, -3.22, 0])}


def dial(c, val, glyph):
    R = 0.45
    ring = Circle(radius=R, stroke_color=GREY, stroke_width=3, fill_color=BG, fill_opacity=1).move_to(c)
    ticks = VGroup(*[Line(c + R * np.array([np.cos(a), np.sin(a), 0]) * 0.78, c + R * np.array([np.cos(a), np.sin(a), 0]),
                          color=GREY, stroke_width=3) for a in np.radians([0, 90, 180, 270])])
    a = np.radians(val)
    nd = Line(c, c + 0.42 * np.array([np.cos(a), np.sin(a), 0]), color=ORANGE, stroke_width=6)
    hub = Dot(c, radius=0.06, color=ORANGE)
    g = G(glyph, size=50, color=ORANGE).next_to(ring, LEFT, buff=0.12)
    return VGroup(ring, ticks, nd, hub, g)


def dial_set(vals, A, off=None, tf=None, lead_op=1.0):
    out = VGroup()
    for key, glyph in (("phi2", "φ"), ("psi2", "ψ"), ("phi3", "φ"), ("psi3", "ψ")):
        out.add(dial(DIAL_POS[key], vals[key], glyph))
    # one leader per joint, from the pair to its joint
    for pair, j in ((("phi2", "psi2"), 2), (("phi3", "psi3"), 3)):
        c = (DIAL_POS[pair[0]] + DIAL_POS[pair[1]]) / 2
        tgt = P3(A, f"A{j}", off)
        if tf is not None:
            tgt = tf(tgt)
        d = unit(tgt - c)
        start = c + d * (0.5 / max(abs(d[1]), 0.35))
        out.add(Line(start, tgt - d * 0.18, color=GREY, stroke_width=2.5, stroke_opacity=lead_op))
    return out


def bent(vals):
    return backbone(phi={2: vals["phi2"], 3: vals["phi3"]}, psi={2: vals["psi2"], 3: vals["psi3"]})


FLAT = {"phi2": 180.0, "psi2": 180.0, "phi3": 180.0, "psi3": 180.0}


def lerp_vals(a, b, t):
    out = {}
    for k in a:
        d = ((b[k] - a[k] + 180) % 360) - 180
        out[k] = a[k] + d * t
    return out


_bp = np.vstack([card_poly(bent(BEND), k, np.zeros(2)).get_vertices()[:, :2] for k in (1, 2, 3)])
B_OFF = -(_bp.min(0) + _bp.max(0)) / 2   # chain offset once it bends (keeps the bent chain centred)


def ghost(A):
    g = VGroup(*[card_poly(A, k).set_fill(opacity=0).set_stroke(GREY, width=2, opacity=0.3) for k in (1, 2, 3)])
    return DashedVMobject(g[0], num_dashes=40), DashedVMobject(g[1], num_dashes=40), DashedVMobject(g[2], num_dashes=40)


class S19(SpokenScene):
    def construct(self):
        base, ax, arr, labs = s18_end()
        self.add(base, ax, arr, labs)
        ps = ValueTracker(PSI_SWING)
        self.remove(base)
        flat_now = always_redraw(lambda: chain_mob(backbone(psi={2: ps.get_value()})))
        self.add(flat_now)
        self.play(FadeOut(VGroup(ax, arr, labs)), ps.animate.set_value(180.0), run_time=0.7, rate_func=smooth)
        self.remove(flat_now)
        tt = ValueTracker(0.0)
        offt = lambda: OFF + (B_OFF - OFF) * tt.get_value()
        cur = lambda: lerp_vals(FLAT, BEND, tt.get_value())
        chain = always_redraw(lambda: chain_mob(bent(cur()), off=offt()))
        self.add(chain)
        d0 = dial_set(FLAT, REF)
        a1, a2 = VGroup(d0[0], d0[1], d0[4]), VGroup(d0[2], d0[3], d0[5])
        self.at("per residue", lead=0.0)
        self.play(FadeIn(a1), run_time=0.5)
        self.at("repeated down", lead=0.0)
        self.play(FadeIn(a2), run_time=0.5)
        lt = ValueTracker(1.0)
        dials = always_redraw(lambda: dial_set(cur(), bent(cur()), off=offt(), lead_op=lt.get_value()))
        self.add(dials)
        self.remove(a1, a2, d0)
        gh = VGroup(*ghost(REF)).set_z_index(-2)
        self.at("Together", lead=0.0)
        self.play(FadeIn(gh), lt.animate.set_value(0.0), run_time=0.3)
        self.play(tt.animate.set_value(1.0), run_time=1.6, rate_func=smooth)
        self.play(FadeOut(gh), lt.animate.set_value(1.0), run_time=0.5)
        self.finish()


class S20(SpokenScene):
    def construct(self):
        tt = ValueTracker(0.0)
        spin = {"phi2": 2, "psi2": -1, "phi3": -2, "psi3": 1}    # whole turns before settling

        def cur():
            u = 1 - (1 - tt.get_value()) ** 3       # fast, then slowing to a stop
            return {k: BEND[k] + 360.0 * spin[k] * u for k in BEND}

        def card_box(A):
            P = np.vstack([card_poly(A, k, B_OFF).get_vertices() for k in (1, 2, 3)])
            return P.min(0), P.max(0)
        lo0, hi0 = card_box(bent(BEND))
        home = (lo0 + hi0) / 2

        def fitter(A):
            """Camera that follows the spinning chain: zoom out just enough to keep it between the dial rows."""
            lo, hi = card_box(A)
            k = min(1.0, 5.2 / (hi[1] - lo[1]), 11.6 / (hi[0] - lo[0]))
            c = (lo + hi) / 2
            return lambda p: home + (np.asarray(p) - c) * k

        def chain_now():
            A = bent(cur())
            f = fitter(A)
            m = chain_mob(A, off=B_OFF)
            m.apply_function(f)
            return m
        lt = ValueTracker(1.0)
        chain = always_redraw(chain_now)
        dials = always_redraw(lambda: dial_set(cur(), bent(cur()), off=B_OFF, tf=fitter(bent(cur())), lead_op=lt.get_value()))
        self.add(chain, dials)
        self.play(lt.animate.set_value(0.0), run_time=0.2)
        self.play(tt.animate.set_value(1.0), run_time=3.0, rate_func=linear)
        self.play(lt.animate.set_value(1.0), run_time=0.3)
        q = T("?", size=170, color=TEXT, weight=BOLD).move_to([5.3, 1.9, 0]).set_z_index(12)
        self.at("how much freedom", lead=0.0)
        self.play(FadeIn(q, scale=1.3), run_time=0.5)
        self.finish()


class S21(SpokenScene):
    def construct(self):
        tt = ValueTracker(1.0)
        offt = lambda: OFF + (B_OFF - OFF) * tt.get_value()
        cur = lambda: lerp_vals(FLAT, BEND, tt.get_value())
        chain = always_redraw(lambda: chain_mob(bent(cur()), off=offt()))
        dials = dial_set(BEND, bent(BEND), off=B_OFF)
        q = T("?", size=170, color=TEXT, weight=BOLD).move_to([5.3, 1.9, 0]).set_z_index(12)
        self.add(chain, dials, q)
        self.play(FadeOut(dials), FadeOut(q), tt.animate.set_value(0.0), run_time=1.0, rate_func=smooth)
        self.remove(chain)
        A = REF
        cm = chain_mob(A)
        self.add(cm)
        lk = s16_lock(A)
        hl1 = {"C2-N3": (ORANGE, 9)}
        flat = T("flat and rigid", size=40, color=ORANGE)
        flat.move_to([bond_mid(A, "C2", "N3")[0] + 1.2, -3.3, 0])
        fl = leader(flat, bond_mid(A, "C2", "N3") + DOWN * 0.05)
        self.at("flat and rigid", lead=0.0)
        self.play(Transform(cm, chain_mob(A, hl=hl1)), FadeIn(lk, scale=1.4), FadeIn(flat), Create(fl), run_time=0.6)
        j = P3(A, "A2")
        ap = hinge_arrow(A, "N2", "A2")
        aq = hinge_arrow(A, "A2", "C2")
        lp = G("φ", size=64, color=ORANGE).move_to([j[0] - 2.2, 3.2, 0])
        lq = G("ψ", size=64, color=ORANGE).move_to([j[0] + 2.2, 3.2, 0])
        llp = leader(lp, bond_mid(A, "N2", "A2"), color=ORANGE)
        llq = leader(lq, bond_mid(A, "A2", "C2"), color=ORANGE)
        two = T("two hinges", size=40, color=TEXT).move_to([j[0], 3.3, 0])
        self.at("Each residue", lead=0.0)
        self.play(FadeIn(ap), FadeIn(aq), FadeIn(lp), FadeIn(lq), Create(llp), Create(llq), run_time=0.5)
        self.at("two hinges", lead=0.0)
        self.play(FadeIn(two), run_time=0.3)
        self.finish()


class S22End(EndCard):
    LINE = "The peptide bond is flat and cannot twist, so each residue turns on just two hinges, phi and psi."

    def construct(self):
        l1 = T("The peptide bond is flat and cannot twist,", size=50, font=TITLE_FONT)
        l2 = T("so each residue turns on just two hinges,", size=50, font=TITLE_FONT)
        l3 = T("phi and psi.", size=50, font=TITLE_FONT, color=ORANGE)
        line = VGroup(l1, l2, l3).arrange(DOWN, buff=0.3)
        fit(line, max_w=12.2)
        sub = T("biochemistrypedia.com", size=26, color=TEAL)
        g = VGroup(line, sub).arrange(DOWN, buff=0.55)
        self.play(FadeIn(line, shift=UP * 0.15), run_time=self.beat(0.3))
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        self.finish()
