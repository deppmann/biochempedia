# COLOR MAP (shared with the other chapters of this lesson; one color per concept)
#   BLUE    the protein / polypeptide chain / folded chain, the native curve
#   BETA    (lighter blue) only to tell the beta subunits of hemoglobin from the alpha subunits
#   ORANGE  cost: ordered water / lost entropy / a buried polar group with no partner / the destabilised curve
#   YELLOW  nonpolar (oily) side chains, the oily core, the sticky patch and its pocket
#   PURPLE  polar / charged side chains
#   TEAL    water (V-shaped symbols) and the interactive cue on cards
#   GREEN   satisfied / gained: bonded backbone groups, entropy gained, folded state
#   RED     forbidden or broken: crossed-out ideas, the unfolded state, sickle cell
#   TEXT    hydrogen bonds (dashed white lines), labels
#   GREY    labels, frames, axes
# NOTHING here draws a molecular structure: water is a V-shaped symbol, oily groups are blobs,
# chains are smooth curves with beads, C=O / N-H are text chips, proteins are labelled cartoons,
# and the melting curves are computed from a two-state equation (dG = dH (1 - T/Tm)).
import numpy as np
from bp_style import *

ORANGE = "#F29E4C"
PURPLE = "#B58CE0"
LIGHT = "#C9CED8"
BETA = "#9DB4FF"


def solid(color, a):
    return interpolate_color(ManimColor(BG), ManimColor(color), a)


def d2(p, c):
    return float(np.hypot(p[0] - c[0], p[1] - c[1]))


def V(x, y):
    return np.array([x, y, 0.0])


def tag(txt, color=TEXT, size=26, pos=None, weight=NORMAL):
    t = T(txt, size=size, color=color, weight=weight)
    bk = Rectangle(width=t.width + 0.26, height=t.height + 0.18, stroke_width=0, fill_color=BG, fill_opacity=0.92).move_to(t)
    g = VGroup(bk, t)
    if pos is not None:
        g.move_to(pos)
    return g.set_z_index(20)


# ---------------------------------------------------------------- water symbols
class Water(VMobject):
    """A V-shaped water symbol that jiggles. base/ang/amp are animated by `settle`."""

    def __init__(self, base, ang=0.0, amp=0.07, ph=0.0, color=TEAL, s=0.27, w=3.5, op=0.6):
        super().__init__()
        self.base = np.array([base[0], base[1], 0.0])
        self.ang, self.amp, self.ph, self.s = ang, amp, ph, s
        self.t = ph * 3
        self.set_stroke(color=color, width=w, opacity=op)
        self.set_fill(opacity=0)
        self.shape()
        self.add_updater(lambda m, dt: m.tick(dt))

    def pos(self):
        t = self.t
        return self.base + self.amp * np.array([np.sin(1.7 * t + self.ph), np.cos(1.3 * t + 1.7 * self.ph), 0.0])

    def shape(self):
        p = self.pos()
        a = self.ang + 2.0 * self.amp * np.sin(1.1 * self.t + 2 * self.ph)
        s = self.s
        loc = [(-0.85 * s, 0.6 * s), (0, -0.3 * s), (0.85 * s, 0.6 * s)]
        c, sn = np.cos(a), np.sin(a)
        self.set_points_as_corners([[p[0] + c * x - sn * y, p[1] + sn * x + c * y, 0.0] for x, y in loc])

    def tick(self, dt):
        self.t += dt
        self.shape()


def settle(waters, targets, amp_to=0.0, rt=1.0, spin=0.0, rate=smooth, s_to=None):
    """Animate waters to targets [(pos, ang)], optionally spinning; amp goes to amp_to."""
    data = [(w.base.copy(), w.ang, w.amp, np.array([tp[0][0], tp[0][1], 0.0]), tp[1]) for w, tp in zip(waters, targets)]
    s0 = [w.s for w in waters]

    def fn(_m, a):
        for w, (b0, a0, m0, b1, a1), sz in zip(waters, data, s0):
            if s_to is not None:
                w.s = sz + (s_to - sz) * a
            w.base = b0 + (b1 - b0) * a
            da = ((a1 - a0 + np.pi) % (2 * np.pi)) - np.pi
            w.ang = a0 + da * a + spin * a
            w.amp = m0 + (amp_to - m0) * a
    return UpdateFromAlphaFunc(Mobject(), fn, run_time=rt, rate_func=rate)


# ---------------------------------------------------------------- stage geometry (water scenes)
C1 = V(-1.1, 0)
C2 = V(1.0, 0)
C3 = V(3.9, 0)
BR = 1.1
RING_R = 1.65
rng = np.random.default_rng(11)
FIELD = []
for j, y in enumerate(np.arange(-3.3, 3.4, 0.82)):
    off = 0.5 if j % 2 else 0.0
    for x in np.arange(-6.4 + off, 6.6, 1.0):
        FIELD.append((x + rng.uniform(-.2, .2), y + rng.uniform(-.12, .12), rng.uniform(0, TAU), rng.uniform(0, TAU)))


def klass(f):
    a = d2(f, C1)
    if a < 1.4:
        return "in"
    if a < 2.25:
        return "near"
    if d2(f, C2) < 1.95:
        return "fb"
    if d2(f, C3) < 2.25:
        return "fv"
    return "far"


def polar(f, c=C1):
    return float(np.arctan2(f[1] - c[1], f[0] - c[0]))


_near = sorted([f for f in FIELD if klass(f) == "near"], key=polar)
if len(_near) % 2:
    _near = _near[:-1]
NEAR = _near
NN = len(NEAR)
KL = {id(f): klass(f) for f in FIELD}
NEAR_IDS = {id(f) for f in NEAR}


def kls(f):
    if id(f) in NEAR_IDS:
        return "near"
    k = KL[id(f)]
    return "in" if k == "near" else k


def fw(f, op=0.6, w=3.5):
    return Water((f[0], f[1]), ang=f[2], ph=f[3], op=op, w=w)


def ring_slots(c):
    out = []
    for k in range(NN):
        a = (k + 0.5) * TAU / NN
        out.append((c + RING_R * V(np.cos(a), np.sin(a)), a - PI / 2))
    return out


SLOT_A = ring_slots(C1)
SLOT_B = ring_slots(C2)
# merged plan: which ring waters survive when the blobs touch, which are squeezed out
KEEP_A = [k for k in range(NN) if d2(SLOT_A[k][0], C2) >= 1.9]
KEEP_B = [k for k in range(NN) if d2(SLOT_B[k][0], C1) >= 1.9]
for ka in list(KEEP_A):
    for kb in KEEP_B:
        if d2(SLOT_A[ka][0], SLOT_B[kb][0]) < 0.75 and ka in KEEP_A:
            KEEP_A.remove(ka)
FREE_A = [k for k in range(NN) if k not in KEEP_A]
FREE_B = [k for k in range(NN) if k not in KEEP_B]
MID = (C1 + C2) / 2


def neck_targets(n_top, n_bot):
    out = []
    for n, sgn in ((n_top, 1), (n_bot, -1)):
        for i in range(n):
            x = MID[0] + (i - (n - 1) / 2) * 0.95
            y = sgn * (2.75 + 0.12 * abs(i - (n - 1) / 2))
            out.append((V(x, y), 0.0))
    return out


FREE_ALL = [("A", k) for k in FREE_A] + [("B", k) for k in FREE_B]
_top = [fa for fa in FREE_ALL if (SLOT_A if fa[0] == "A" else SLOT_B)[fa[1]][0][1] >= 0]
_bot = [fa for fa in FREE_ALL if fa not in _top]
NECK = neck_targets(len(_top), len(_bot))
FREE_ORDER = _top + _bot
FAR_DEST = [(V(-4.4, 3.0), 0.5), (V(-2.2, 3.05), 1.0), (V(0.4, 3.1), 2.0), (V(4.4, 3.0), 0.5), (V(-4.4, -3.0), 0.5), (V(-2.2, -3.05), 1.0),
            (V(0.4, -3.1), 2.0), (V(4.4, -3.0), 0.5), (V(5.4, 1.0), 0.5), (V(5.4, -1.0), 0.5)]


def blobshape(c, r=BR, color=YELLOW, a=0.32, seed=0.0, sw=4):
    th = np.linspace(0, TAU, 30, endpoint=False)
    rr = r * (1 + 0.045 * np.sin(3 * th + seed) + 0.03 * np.sin(5 * th + 2 * seed))
    pts = [V(c[0] + q * np.cos(t), c[1] + q * np.sin(t)) for q, t in zip(rr, th)]
    m = VMobject(stroke_color=color, stroke_width=sw, fill_color=solid(color, a), fill_opacity=1)
    m.set_points_smoothly([*pts, pts[0]])
    return m.set_z_index(5)


def blob_with(c, label=None, r=BR, seed=0.0):
    b = blobshape(c, r, seed=seed)
    g = VGroup(b)
    if label:
        g.add(T(label, size=28, color=TEXT).move_to(c).set_z_index(6))
    return g


def hb_lines(waters, n=26, seed=3, lo=0.75, hi=1.25, skip=()):
    """Static dashed hydrogen-bond lines between close water pairs, with a flicker updater."""
    r = np.random.default_rng(seed)
    pairs = []
    for i in range(len(waters)):
        for j in range(i + 1, len(waters)):
            a, b = waters[i].base, waters[j].base
            if lo < np.hypot(*(a - b)[:2]) < hi and i not in skip and j not in skip:
                pairs.append((i, j))
    r.shuffle(pairs)
    used, out = set(), VGroup()
    for i, j in pairs:
        if i in used or j in used:
            continue
        used.update((i, j))
        a, b = waters[i].base, waters[j].base
        u = (b - a) / np.linalg.norm(b - a)
        ln = DashedLine(a + u * 0.24, b - u * 0.24, dash_length=0.07, dashed_ratio=0.55, color=TEXT, stroke_width=3)
        ln.ph = r.uniform(0, 6.28)
        ln.w = r.uniform(1.6, 3.0)
        ln.t = r.uniform(0, 3)

        def upd(m, dt):
            m.t += dt
            o = float(np.clip((np.sin(m.w * m.t + m.ph) + 0.15) * 2.2, 0, 1)) * 0.9
            m.set_stroke(opacity=o)
        ln.add_updater(upd)
        out.add(ln)
        if len(out) >= n:
            break
    return out


def ring_bonds(points, closed=True, maxd=1.7):
    out = VGroup()
    n = len(points)
    for i in range(n if closed else n - 1):
        a, b = points[i], points[(i + 1) % n]
        if np.hypot(*(a - b)[:2]) > maxd:
            continue
        u = (b - a) / np.linalg.norm(b - a)
        out.add(DashedLine(a + u * 0.25, b - u * 0.25, dash_length=0.08, dashed_ratio=0.6, color=TEXT, stroke_width=3.5).set_stroke(opacity=0.9))
    return out


class WaterStage:
    """Builds the field and the first oily blob for a given state of the story."""

    def __init__(self, upto="plain", merged=False):
        self.w = {}
        for f in FIELD:
            self.w.setdefault(kls(f), []).append(fw(f))
        # ordered list of near waters (sorted by polar angle) so slot k matches NEAR[k]
        self.near = [fw(f, op=0.75, w=4.5) for f in NEAR]
        self.inn = self.w.get("in", [])
        self.far = self.w.get("far", [])
        self.fv = self.w.get("fv", [])
        self.fb = self.w.get("fb", [])
        self.blob1 = blob_with(C1, "leucine", seed=0.3)
        self.blob2 = blob_with(C2, None, seed=1.7)


def exposed_arcs():
    a = np.arccos(np.clip((np.linalg.norm(C2 - C1) / 2) / BR, -1, 1))
    la = TAU - 2 * a
    A = Arc(radius=BR, start_angle=a, angle=la, arc_center=C1, color=YELLOW, stroke_width=11).set_z_index(7)
    B = Arc(radius=BR, start_angle=PI + a, angle=la, arc_center=C2, color=YELLOW, stroke_width=11).set_z_index(7)
    return VGroup(A, B)


def merged_state(ws, with_free=False):
    """Everything on stage once the two blobs touch and the freed waters are gone (or still at the neck)."""
    ring = []
    for k in KEEP_A:
        w = fw(NEAR[k], op=1, w=5.5)
        w.base, w.ang, w.amp = SLOT_A[k][0].copy(), SLOT_A[k][1], 0.0
        ring.append(w)
    for k in KEEP_B:
        w = fw(NEAR[k], op=1, w=5.5)
        w.base, w.ang, w.amp = SLOT_B[k][0].copy(), SLOT_B[k][1], 0.0
        ring.append(w)
    ring.sort(key=lambda w: polar(w.base, MID))
    bonds = ring_bonds([w.base for w in ring], maxd=1.5)
    return ring, bonds


def far_all(ws):
    return list(ws.far) + list(ws.fv)


# ================================================================== scenes
class S00Title(TitleCard):
    LESSON = "Protein Three-Dimensional Structure"
    TITLE = "Water Chooses"

    def construct(self):
        brand = T("BIOCHEMISTRYPEDIA", size=20, color=TEAL, weight=BOLD).set_opacity(0.9)
        lesson = T(self.LESSON.upper(), size=22, color=GREY)
        title = T(self.TITLE, size=54, font=TITLE_FONT)
        rule = Line(LEFT * 1.2, RIGHT * 1.2, color=GOLD, stroke_width=4)
        g = VGroup(brand, lesson, title, rule).arrange(DOWN, buff=0.32)
        self.play(FadeIn(g, shift=UP * 0.1), run_time=0.8)
        self.wait(1.5)
        self.play(FadeOut(g), run_time=0.4)
        self.finish()


def coil(x0, y0, length=3.0, amp=0.3, rot=0.0, color=BLUE, w=7):
    f = ParametricFunction(lambda t: np.array([t, amp * np.sin(t * 11), 0.0]), t_range=[0, length, 0.02], color=color, stroke_width=w)
    f.move_to([x0, y0, 0]).rotate(rot)
    return f


def strand(x0, y0, length=3.0, rot=0.0, color=BLUE):
    a = Arrow(V(-length / 2, 0), V(length / 2, 0), buff=0, stroke_width=16, tip_length=0.5, color=color, max_stroke_width_to_length_ratio=40)
    a.move_to([x0, y0, 0]).rotate(rot)
    return a


class S01(SpokenScene):
    def construct(self):
        items = [coil(-3.9, 2.35, 3.2, rot=0.15), strand(3.7, 2.45, 3.0, rot=-0.12), coil(-3.8, -2.35, 3.0, rot=-0.18),
                 strand(3.9, -2.4, 3.2, rot=0.15), coil(0.2, 3.1, 2.4, amp=0.25, rot=0.04), strand(0.0, -3.1, 2.6, rot=-0.05)]
        for i, m in enumerate(items):
            m.base_pos = m.get_center().copy()
            m.ph = 1.3 * i
            m.tt = 0.0

            def drift(mm, dt):
                mm.tt += dt
                tgt = mm.base_pos + np.array([0.35 * np.sin(0.9 * mm.tt + mm.ph), 0.18 * np.cos(0.7 * mm.tt + mm.ph), 0.0])
                mm.shift(tgt - mm.get_center())
            m.add_updater(drift)
        self.play(LaggedStart(*[FadeIn(m, scale=0.8) for m in items], lag_ratio=0.12), run_time=self.beat(0.35))
        self.at("chooses among them")
        q = T("What chooses among them?", size=52, color=TEXT)
        qb = tag("What chooses among them?", size=52)
        self.play(FadeIn(qb, shift=UP * 0.15), run_time=self.beat(0.2))
        self.finish()


class S02(SpokenScene):
    def construct(self):
        ws = WaterStage()
        allw = ws.inn + ws.near + ws.far + ws.fv + ws.fb
        self.play(FadeIn(VGroup(*allw)), run_time=self.beat(0.15))
        self.at("one oily side chain")
        self.play(GrowFromCenter(ws.blob1), *[FadeOut(w) for w in ws.inn], run_time=0.9)
        self.finish()


def base_scene_waters(ws, with_inn=False):
    return ws.near + ws.far + ws.fv + ws.fb


class S03(SpokenScene):
    def construct(self):
        ws = WaterStage()
        waters = base_scene_waters(ws)
        self.add(*waters, ws.blob1)
        self.wait(self.beat(0.1))
        self.at("hydrogen bond")
        lines = hb_lines(waters, n=28)
        leg_line = DashedLine(V(-0.4, 0), V(0.4, 0), dash_length=0.08, dashed_ratio=0.55, color=TEXT, stroke_width=3.5)
        leg = VGroup(tag("hydrogen bond", size=26)).arrange(RIGHT, buff=0.1)
        legend = VGroup(leg_line, leg).arrange(RIGHT, buff=0.15).move_to(V(4.7, 3.15)).set_z_index(21)
        self.play(FadeIn(lines), FadeIn(legend), run_time=0.9)
        self.finish()


class S04(SpokenScene):
    def construct(self):
        ws = WaterStage()
        waters = base_scene_waters(ws)
        lines = hb_lines(waters, n=28)
        self.add(*waters, ws.blob1, lines)
        self.at("next to the oily surface")
        close = sorted(ws.near, key=lambda w: d2(w.base, C1))[:6]
        self.play(*[w.animate.set_stroke(color=TEAL, width=7, opacity=1) for w in close], run_time=0.6)
        self.at("cannot hydrogen bond")
        stubs = VGroup()
        for w in close[:5]:
            p = w.base
            u = (C1 - p) / np.linalg.norm(C1 - p)
            a = p + u * 0.28
            b = C1 - u * (BR + 0.05)
            ln = DashedLine(a, b, dash_length=0.08, dashed_ratio=0.5, color=RED, stroke_width=3.5)
            m = (a + b) / 2
            x = VGroup(Line(m + V(-.13, -.13), m + V(.13, .13), color=RED, stroke_width=6), Line(m + V(-.13, .13), m + V(.13, -.13), color=RED, stroke_width=6))
            stubs.add(ln, x)
        stubs.set_z_index(8)
        self.play(Create(stubs), run_time=0.9)
        self.finish()


def ring_targets(c):
    return ring_slots(c)


class S05(SpokenScene):
    def construct(self):
        ws = WaterStage()
        waters = ws.far + ws.fv + ws.fb
        lines = hb_lines(waters, n=22)
        close = sorted(ws.near, key=lambda w: d2(w.base, C1))[:6]
        for w in close:
            w.set_stroke(width=7, opacity=1)
        self.add(*waters, *ws.near, ws.blob1, lines)
        self.at("forms a tighter")
        self.play(settle(ws.near, SLOT_A, amp_to=0.0, rt=1.3), *[w.animate.set_stroke(color=TEAL, width=5.5, opacity=1) for w in ws.near], run_time=1.3)
        self.at("more ordered network")
        bonds = ring_bonds([w.base for w in ws.near])
        lab = tag("ordered water", color=TEAL, size=30, pos=V(C1[0], 2.65))
        self.play(Create(bonds), FadeIn(lab), run_time=0.8)
        self.at("like a cage")
        self.play(Indicate(bonds, color=TEXT, scale_factor=1.0), run_time=0.9)
        self.finish()


def ordered_ring(ws):
    for w, (p, a) in zip(ws.near, SLOT_A):
        w.base, w.ang, w.amp = p.copy(), a, 0.0
        w.set_stroke(color=TEAL, width=5.5, opacity=1)
    return ring_bonds([w.base for w in ws.near])


class S06(SpokenScene):
    def construct(self):
        ws = WaterStage()
        waters = ws.far + ws.fv + ws.fb
        lines = hb_lines(waters, n=22)
        bonds = ordered_ring(ws)
        lab = tag("ordered water", color=TEAL, size=30, pos=V(C1[0], 2.65))
        self.add(*waters, *ws.near, ws.blob1, lines, bonds, lab)
        self.at("lost freedom")
        l1 = T("lost freedom", size=38, color=ORANGE)
        l2 = T("= lost entropy", size=38, color=ORANGE)
        col = VGroup(l1, l2).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
        plate = RoundedRectangle(corner_radius=0.16, width=col.width + 0.5, height=col.height + 0.4, stroke_color=ORANGE, stroke_width=3,
                                 fill_color=solid(ORANGE, 0.16), fill_opacity=1)
        box = VGroup(plate, col.move_to(plate)).move_to(V(4.1, 0.2)).set_z_index(22)
        l2.set_opacity(0)
        lead = Line(box.get_left() + LEFT * 0.03, V(0.75, 0.1), color=ORANGE, stroke_width=4).set_z_index(21)
        self.play(FadeIn(plate), FadeIn(l1, shift=LEFT * 0.2), Create(lead), run_time=0.6)
        self.at("lost entropy")
        self.play(l2.animate.set_opacity(1), Indicate(bonds, color=ORANGE, scale_factor=1.0), run_time=0.8)
        self.finish()


def tag_lab(txt, color, size=30, pos=None):
    return tag(txt, color=color, size=size, pos=pos)


class S07(SpokenScene):
    def construct(self):
        ws = WaterStage()
        waters = ws.far + ws.fv + ws.fb
        lines = hb_lines(waters, n=22)
        bonds = ordered_ring(ws)
        lab = tag("ordered water", color=TEAL, size=30, pos=V(C1[0], 2.65))
        lab2 = VGroup(tag("lost freedom", color=ORANGE, size=32), tag("= lost entropy", color=ORANGE, size=32)).arrange(DOWN, buff=0.08, aligned_edge=LEFT).move_to(V(3.7, 0.5))
        for w in ws.near:
            w.set_z_index(12)
        self.add(*waters, *ws.near, ws.blob1, lines, bonds, lab, lab2)
        self.wait(self.beat(0.05))
        self.play(FadeOut(lab), FadeOut(lab2), run_time=0.4)
        self.at("two oily side chains")
        # second blob with its own cage appears on the right; waters in the way make room
        b2 = blob_with(C3, None, seed=1.7)
        ring2 = [fw(NEAR[k], op=1, w=5.5) for k in range(NN)]
        for w, (p, a) in zip(ring2, ring_slots(C3)):
            w.base, w.ang, w.amp = p.copy(), a, 0.0
            w.set_stroke(color=TEAL, width=5.5, opacity=1)
            w.set_z_index(12)
        bonds2 = ring_bonds([w.base for w in ring2])
        away = list(ws.fb) + list(ws.fv)
        self.play(*[FadeOut(w) for w in away], FadeIn(b2), FadeIn(VGroup(*ring2)), FadeIn(bonds2), run_time=0.9)
        self.at("chains together")
        # slide the second blob with its cage; the squeezed-out waters go to the neck
        tgt_b = []
        for k in range(NN):
            if k in KEEP_B:
                tgt_b.append(SLOT_B[k])
            else:
                tgt_b.append(NECK[FREE_ORDER.index(("B", k))])
        tgt_a = []
        for k in range(NN):
            if k in KEEP_A:
                tgt_a.append(SLOT_A[k])
            else:
                tgt_a.append(NECK[FREE_ORDER.index(("A", k))])
        self.play(b2.animate.shift(C2 - C3), settle(ring2, tgt_b, amp_to=0.0, rt=1.3), settle(ws.near, tgt_a, amp_to=0.0, rt=1.3),
                  FadeOut(bonds), FadeOut(bonds2), run_time=1.3, rate_func=smooth)
        self.play(*[FadeIn(w) for w in ws.fv], run_time=0.3)
        self.at("less oily surface")
        arcs = exposed_arcs()
        free_ws = [ws.near[k] for k in FREE_A] + [ring2[k] for k in FREE_B]
        keep_w = [ws.near[k] for k in KEEP_A] + [ring2[k] for k in KEEP_B]
        keep_w.sort(key=lambda w: polar(w.base, MID))
        newb = ring_bonds([w.base for w in keep_w], maxd=1.5)
        self.play(Create(arcs), Create(newb), ws.blob1[0].animate.set_stroke(width=0), b2[0].animate.set_stroke(width=0),
                  settle(free_ws, [(w.base, w.ang) for w in free_ws], amp_to=0.0, rt=1.0, s_to=0.4), run_time=1.0)
        self.finish()


def merged_scene(scene, with_free=False, arcs=True, bonds=True, lines_n=22):
    """Rebuild the stage as it stands after the blobs touch. Returns pieces."""
    ws = WaterStage()
    far = ws.far + ws.fv
    lines = hb_lines(far, n=lines_n)
    b1 = blob_with(C1, "leucine", seed=0.3)
    b2 = blob_with(C2, None, seed=1.7)
    ring = []
    for k in KEEP_A:
        w = fw(NEAR[k], op=1, w=5.5)
        w.base, w.ang, w.amp = SLOT_A[k][0].copy(), SLOT_A[k][1], 0.0
        w.set_stroke(color=TEAL, width=5.5, opacity=1)
        ring.append(w)
    for k in KEEP_B:
        w = fw(NEAR[k], op=1, w=5.5)
        w.base, w.ang, w.amp = SLOT_B[k][0].copy(), SLOT_B[k][1], 0.0
        w.set_stroke(color=TEAL, width=5.5, opacity=1)
        ring.append(w)
    ring.sort(key=lambda w: polar(w.base, MID))
    for w in ring:
        w.set_z_index(12)
    rb = ring_bonds([w.base for w in ring], maxd=1.5)
    arc = exposed_arcs()
    free = []
    if with_free:
        for (side, k), (p, a) in zip(FREE_ORDER, NECK):
            w = Water((p[0], p[1]), ang=a, amp=0.05, ph=NEAR[k][3], op=1, w=5.5, s=0.4)
            w.set_z_index(12)
            free.append(w)
    b1[0].set_stroke(width=0)
    b2[0].set_stroke(width=0)
    scene.add(*far, *ring, *free, b1, b2, lines, rb, arc)
    return dict(far=far, ring=ring, free=free, b1=b1, b2=b2, lines=lines, rb=rb, arc=arc)


class S08(SpokenScene):
    def construct(self):
        st = merged_scene(self, with_free=True)
        free = st["free"]
        self.at("less water has to be caged")
        self.play(*[w.animate.set_stroke(color=ORANGE, width=6.5, opacity=1) for w in free], run_time=0.7)
        self.at("freed water tumbles away")
        dest = [FAR_DEST[i % len(FAR_DEST)] for i in range(len(free))]
        # send top ones up and bottom ones down
        dest = []
        ti = 0
        bi = 4
        for w in free:
            if w.base[1] > 0:
                dest.append(FAR_DEST[ti]); ti += 1
            else:
                dest.append(FAR_DEST[bi]); bi += 1
        self.play(settle(free, dest, amp_to=0.25, rt=1.5, spin=6.0), run_time=1.5)
        self.play(*[w.animate.set_stroke(color=TEAL, width=3.5, opacity=0.6) for w in free], run_time=0.3)
        self.at("gains entropy")
        g = tag("entropy gained", color=GREEN, size=34, pos=V(4.1, 1.0))
        self.play(FadeIn(g, shift=LEFT * 0.2), run_time=0.6)
        self.finish()


class S09(SpokenScene):
    def construct(self):
        st = merged_scene(self)
        g = tag("entropy gained", color=GREEN, size=34, pos=V(4.1, 1.0))
        self.add(g)
        self.at("drives the oily groups")
        ar = Arrow(g.get_left() + LEFT * 0.05, V(2.45, 0.2), buff=0.1, color=GREEN, stroke_width=7).set_z_index(15)
        self.play(GrowArrow(ar), run_time=0.7)
        self.at("hydrophobic effect", lead=0.5)
        shade = Rectangle(width=16, height=9, stroke_width=0, fill_color=BG, fill_opacity=0.78).set_z_index(30)
        title = T("hydrophobic effect", size=64, color=GOLD, font=TITLE_FONT).set_z_index(31)
        self.play(FadeIn(shade), FadeIn(title, scale=0.9), run_time=0.4)
        self.finish()


def small_blob(c, r=0.42, color=YELLOW):
    return blobshape(c, r, color=color, sw=3)


class S10(SpokenScene):
    def construct(self):
        tb = tag("oil pulls oil", size=92, pos=V(0, 0.4))
        self.wait(0.2)
        self.play(FadeIn(tb, shift=DOWN * 0.15), run_time=0.5)
        self.at("pulled to oil")
        strike = Line(tb.get_left() + RIGHT * 0.1, tb.get_right() + LEFT * 0.1, color=RED, stroke_width=14).set_z_index(25)
        self.play(Create(strike), run_time=0.45)
        self.at("oily groups attract water")
        claim = VGroup(tb, strike)
        rows = []
        for y, kind in ((1.15, "oil to oil"), (-1.55, "oil to water")):
            a = small_blob(V(-5.3, y), 0.8)
            arr = Arrow(V(-4.2, y), V(-2.2, y), buff=0, color=TEXT, stroke_width=11, tip_length=0.38)
            if kind == "oil to oil":
                b = small_blob(V(-1.3, y), 0.8)
            else:
                b = Water((-1.3, y), s=1.0, w=9, op=1, amp=0.0)
                b.ang = 0.0
            lab = T(kind, size=46, color=TEXT).move_to(V(-0.1, y)).align_to(V(-0.1, y), LEFT)
            rows.append((VGroup(a, arr, b), lab))
        self.play(claim.animate.scale(0.5).move_to(V(0, 3.0)), FadeIn(rows[0][0], shift=RIGHT * 0.2), FadeIn(rows[0][1]), run_time=0.7)
        self.play(FadeIn(rows[1][0], shift=RIGHT * 0.2), FadeIn(rows[1][1]), run_time=0.6)
        self.at("about as well")
        br = Brace(VGroup(rows[0][1], rows[1][1]), direction=RIGHT, color=GOLD)
        eq = T("about equal", size=42, color=GOLD).next_to(br, RIGHT, buff=0.2)
        self.play(GrowFromCenter(br), FadeIn(eq), run_time=0.7)
        self.finish()


class S11(SpokenScene):
    def construct(self):
        st = merged_scene(self)
        self.at("pushed together by water")
        arrows = VGroup(
            Arrow(V(-5.9, 0), V(-3.15, 0), buff=0, color=TEAL, stroke_width=11, tip_length=0.4),
            Arrow(V(5.9, 0), V(3.05, 0), buff=0, color=TEAL, stroke_width=11, tip_length=0.4),
            Arrow(V(-0.05, 3.55), V(-0.05, 2.1), buff=0, color=TEAL, stroke_width=11, tip_length=0.4),
            Arrow(V(-0.05, -3.55), V(-0.05, -2.1), buff=0, color=TEAL, stroke_width=11, tip_length=0.4),
        ).set_z_index(18)
        l1 = tag("pushed by water", color=TEAL, size=34, pos=V(-4.5, 0.75))
        l2 = tag("pushed by water", color=TEAL, size=34, pos=V(4.5, 0.75))
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.15), FadeIn(l1), FadeIn(l2), run_time=1.2)
        self.at("not pulled together")
        no = tag("pulled by each other", color=LIGHT, size=36, pos=V(3.6, -2.3))
        cross = Line(no.get_left() + LEFT * 0.05, no.get_right() + RIGHT * 0.05, color=RED, stroke_width=8).set_z_index(25)
        self.play(FadeIn(no), Create(cross), run_time=0.6)
        self.finish()


# ================================================================== the protein scenes (s12 - s14)
PC = V(-0.8, 0)
TYPES = "PYYPYPYYPYYPYPYP"


def unfolded_pos():
    return [V(-5.7 + 11.4 * i / 15, 1.3 * np.sin(i * 0.85 + 0.6)) for i in range(16)]


def folded_pos(c=PC):
    out = []
    ys = [0.5, 1.1, 0.8]
    k = 0
    for i, t in enumerate(TYPES):
        a = i * TAU / 16 + 0.3
        if t == "Y":
            r = ys[k % 3]
            k += 1
        else:
            r = 2.1
        out.append(c + V(r * np.cos(a), r * np.sin(a)))
    return out


def bead(pos, color, r=0.2):
    c = Circle(radius=r, stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.95).move_to(pos)
    return c.set_z_index(6)


def make_chain(beads):
    ch = VMobject(stroke_color=BLUE, stroke_width=5.5).set_z_index(3)
    ch.set_points_smoothly([b.get_center() for b in beads])
    ch.add_updater(lambda m: m.set_points_smoothly([b.get_center() for b in beads]))
    return ch


def protein(folded=True, polar_color=PURPLE):
    pos = folded_pos() if folded else unfolded_pos()
    beads = [bead(p, YELLOW if t == "Y" else polar_color) for p, t in zip(pos, TYPES)]
    return beads, make_chain(beads)


def amb_field(excl=None, op=0.22):
    out = []
    for f in FIELD:
        if excl is not None and d2(f, PC) < excl:
            continue
        out.append(fw(f, op=op, w=3))
    return out


def core_disc():
    return Circle(radius=1.45, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.13).move_to(PC).set_z_index(1)


def p_waters():
    out = []
    pos = folded_pos()
    for p, t in zip(pos, TYPES):
        if t == "P":
            a = np.arctan2(p[1] - PC[1], p[0] - PC[0])
            q = PC + 2.68 * V(np.cos(a), np.sin(a))
            w = Water((q[0], q[1]), ang=a - PI / 2, amp=0.04, ph=a, op=1, w=5)
            out.append(w)
    return out


class S12(SpokenScene):
    def construct(self):
        amb = amb_field()
        self.add(*amb)
        beads, chain = protein(folded=False, polar_color=PURPLE)
        self.play(FadeIn(chain), LaggedStart(*[FadeIn(b, scale=0.5) for b in beads], lag_ratio=0.06), run_time=1.6)
        self.at("nonpolar side chains")
        ys = [b for b, t in zip(beads, TYPES) if t == "Y"]
        b0 = beads[1]
        lab = tag("nonpolar", color=YELLOW, size=34, pos=b0.get_center() + UP * 1.0)
        ldl = Line(lab.get_bottom() + DOWN * 0.03, b0.get_top() + UP * 0.05, color=YELLOW, stroke_width=3).set_z_index(21)
        self.play(FadeIn(lab), Create(ldl), *[Indicate(b, color=YELLOW, scale_factor=1.7) for b in ys], run_time=0.9)
        self.at("buried in a core")
        inner = [w for w in amb if d2(w.base, PC) < 3.0]
        fp = folded_pos()
        core = core_disc()
        self.play(*[b.animate.move_to(p) for b, p in zip(beads, fp)], *[FadeOut(w) for w in inner], FadeOut(lab), FadeOut(ldl), run_time=1.4)
        corelab = tag("core", color=YELLOW, size=34, pos=V(3.6, 0.0))
        ar = Arrow(V(3.0, 0.0), V(PC[0] + 1.55, 0.0), buff=0, color=YELLOW, stroke_width=6).set_z_index(15)
        self.play(FadeIn(core), FadeIn(corelab), GrowArrow(ar), run_time=0.5)
        self.finish()


def protein_state(polar=PURPLE):
    beads, chain = protein(folded=True, polar_color=polar)
    return beads, chain


class S13(SpokenScene):
    def construct(self):
        amb = amb_field(excl=3.0)
        beads, chain = protein(folded=True, polar_color=PURPLE)
        core = core_disc()
        corelab = tag("core", color=YELLOW, size=34, pos=V(3.6, 0.0))
        ar = Arrow(V(3.0, 0.0), V(PC[0] + 1.55, 0.0), buff=0, color=YELLOW, stroke_width=6).set_z_index(15)
        self.add(*amb, core, chain, *beads, corelab, ar)
        self.wait(0.2)
        self.at("polar and charged")
        ps = [b for b, t in zip(beads, TYPES) if t == "P"]
        lab = tag("polar, charged", color=PURPLE, size=34, pos=V(4.4, 1.9))
        ldl = Line(lab.get_left() + LEFT * 0.03, ps[0].get_center() + V(0.25, 0.1), color=PURPLE, stroke_width=3).set_z_index(21)
        self.play(*[Indicate(b, color=PURPLE, scale_factor=1.7) for b in ps], FadeIn(lab), Create(ldl), FadeOut(corelab), FadeOut(ar), run_time=0.9)
        self.at("in the water")
        pw = p_waters()
        self.play(FadeIn(VGroup(*pw)), run_time=0.8)
        self.finish()


class S14(SpokenScene):
    def construct(self):
        amb = amb_field(excl=3.0)
        beads, chain = protein(folded=True, polar_color=PURPLE)
        core = core_disc()
        pw = p_waters()
        self.add(*amb, core, chain, *beads, *pw)
        sh = solid(BLUE, 0.3)
        left = Sector(radius=2.6, start_angle=PI / 2, angle=PI, arc_center=PC, stroke_color=BLUE, stroke_width=5,
                      fill_color=sh, fill_opacity=1).set_z_index(2)
        right = Sector(radius=2.6, start_angle=-PI / 2, angle=PI, arc_center=PC, stroke_color=BLUE, stroke_width=5,
                       fill_color=sh, fill_opacity=1).set_z_index(2)
        self.at("compact shape")
        self.play(FadeIn(left), FadeIn(right), run_time=0.6)
        self.wait(0.2)
        self.play(left.animate.shift(LEFT * 0.9), right.animate.shift(RIGHT * 0.9), run_time=0.7)
        self.at("tertiary structure")
        lab = tag("tertiary structure", color=TEXT, size=36, pos=V(4.2, 2.6))
        cl = tag("nonpolar core", color=YELLOW, size=32, pos=V(PC[0], -3.25))
        self.play(FadeIn(lab, shift=LEFT * 0.2), FadeIn(cl), run_time=0.6)
        self.finish()


# ================================================================== backbone burial (s15 - s17)
# schematic: six backbone groups, partners one turn (three groups) apart in the helix
XS = [-4.0, -2.4, -0.8, 0.8, 2.4, 4.0]
GROUPS = ["C=O", "N–H", "C=O", "N–H", "C=O", "N–H"]
PER = 4.8   # one helical turn spans three groups
CORE_TOP = 1.3
CHIP_UP = 0.62


def swater(pos, ang=0.0, op=0.3, w=3.5, color=TEAL, s=0.27):
    m = Water((pos[0], pos[1]), ang=ang, amp=0.0, op=op, w=w, s=s, color=color)
    m.clear_updaters()
    return m


def gchip(txt, color=LIGHT):
    c = chip(txt, color=color, size=28, pad=0.13, fill_opacity=0.2)
    c[0].set_fill(solid(color, 0.2), opacity=1)
    return c.set_z_index(8)


def chip_set(c, color):
    c[0].set_stroke(color=color).set_fill(solid(color, 0.2), opacity=1)
    c[1].set_color(color)
    return c


def chip_to(c, color):
    return [c[0].animate.set_stroke(color=color).set_fill(solid(color, 0.2), opacity=1), c[1].animate.set_color(color)]


class Buried:
    """The core band, the water above it, the backbone with six groups. sink = 0 (at the surface) or 1 (buried)."""

    def __init__(self, sink=0.0, bottom=-2.0):
        y0 = 1.85 - 2.75 * sink
        self.bottom = bottom
        self.core = RoundedRectangle(corner_radius=0.15, width=14.0, height=CORE_TOP - bottom, stroke_color=YELLOW, stroke_width=3, stroke_opacity=0.6,
                                     fill_color=YELLOW, fill_opacity=0.12).move_to([0, (CORE_TOP + bottom) / 2, 0]).set_z_index(0)
        self.corelab = T("core", size=30, color=YELLOW).move_to([5.9, CORE_TOP - 0.45, 0]).set_z_index(1)
        self.cap = T("schematic: spacing not to scale", size=26, color=GREY).move_to([4.3, bottom + (0.35 if bottom > -3 else 0.28), 0]).set_z_index(1)
        self.bulk = []
        for f in FIELD:
            if f[1] < CORE_TOP + 0.45:
                continue
            if any(abs(f[0] - x) < 0.7 for x in XS) and f[1] < 3.7:
                continue
            self.bulk.append(swater((f[0], f[1]), ang=f[2], op=0.3))
        self.partners = [swater((x, 1.85 + CHIP_UP + 0.85), ang=0.0, op=1.0, w=5) for x in XS]
        self.y0 = y0
        self.back = Line(V(-5.2, y0), V(5.2, y0), color=BLUE, stroke_width=9).set_z_index(3)
        self.chips = [gchip(t).move_to([x, y0 + CHIP_UP, 0]) for x, t in zip(XS, GROUPS)]
        self.stems = [Line(V(x, y0), V(x, y0 + CHIP_UP - 0.27), color=BLUE, stroke_width=5).set_z_index(3) for x in XS]

    def chain_g(self):
        return VGroup(self.back, *self.chips, *self.stems)


class S15(SpokenScene):
    def construct(self):
        b = Buried()
        self.add(b.core, b.corelab, b.cap, *b.bulk)
        self.play(FadeIn(VGroup(*b.partners)), Create(b.back), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(c) for c in b.chips], lag_ratio=0.1), *[Create(s) for s in b.stems], run_time=0.9)
        lines = [always_redraw(lambda c=c, p=p: DashedLine(c.get_top() + UP * 0.03, p.pos() - UP * 0.2, dash_length=0.09, dashed_ratio=0.55, color=TEXT, stroke_width=3.5).set_z_index(4))
                 for c, p in zip(b.chips, b.partners)]
        self.play(*[FadeIn(l) for l in lines], run_time=0.6)
        self.at("buried backbone groups")
        self.play(b.chain_g().animate.shift(DOWN * 2.75), run_time=1.0)
        self.at("lose their water partners")
        for l in lines:
            l.clear_updaters()
        self.play(*[FadeOut(l) for l in lines], run_time=0.7)
        self.finish()


def buried_scene(scene):
    b = Buried(sink=1.0)
    scene.add(b.core, b.corelab, b.cap, *b.bulk, *b.partners, b.back, *b.stems, *b.chips)
    return b


class S16(SpokenScene):
    def construct(self):
        b = buried_scene(self)
        self.at("buried polar group")
        ch = b.chips[1]
        self.play(Indicate(ch, color=ORANGE, scale_factor=1.25), run_time=0.8)
        self.at("no partner")
        np_ = tag("no partner", color=ORANGE, size=32, pos=ch.get_center() + UP * 0.72)
        self.play(FadeIn(np_), run_time=0.4)
        self.at("costs free energy")
        glow = Circle(radius=0.8, stroke_width=0, fill_color=ORANGE, fill_opacity=0.35).move_to(ch).set_z_index(7)
        cost = tag("costly", color=ORANGE, size=36, pos=ch.get_center() + DOWN * 1.05)
        self.play(FadeIn(glow), *chip_to(ch, ORANGE), FadeIn(cost), run_time=0.7)
        self.finish()


def arc_path(a, b, h):
    return ParametricFunction(lambda t: (1 - t) * a + t * b + UP * h * np.sin(PI * t), t_range=[0, 1, 0.02])


class S17(SpokenScene):
    def construct(self):
        b = Buried(sink=1.0)
        y0 = b.y0
        A = ValueTracker(0.0)

        def wy(x):
            return y0 + A.get_value() * np.cos(TAU * (x - XS[0]) / PER)
        wave = always_redraw(lambda: ParametricFunction(lambda t: np.array([t, wy(t), 0.0]), t_range=[-5.2, 5.2, 0.02], color=BLUE, stroke_width=9).set_z_index(3))
        chips = b.chips
        chip_set(chips[1], ORANGE)
        for c, x in zip(chips, XS):
            c.add_updater(lambda m, x=x: m.move_to([x, wy(x) + CHIP_UP, 0]))
        stems = [always_redraw(lambda x=x: Line(V(x, wy(x)), V(x, wy(x) + CHIP_UP - 0.27), color=BLUE, stroke_width=5).set_z_index(3)) for x in XS]
        self.add(b.core, b.corelab, b.cap, *b.bulk, wave, *stems, *chips)
        self.at("bond to itself")
        self.play(A.animate.set_value(0.45), run_time=1.3)
        hts = [0.5, 0.75, 1.0]
        pairs = []
        for i, h in zip((0, 1, 2), hts):
            pairs.append(always_redraw(lambda i=i, h=h: DashedVMobject(arc_path(chips[i].get_top() + UP * 0.03, chips[i + 3].get_top() + UP * 0.03, h),
                                                                       num_dashes=22, dashed_ratio=0.55).set_color(GREEN).set_stroke(width=5).set_z_index(9)))
        self.play(*[Create(p) for p in pairs], *[a for c in chips for a in chip_to(c, GREEN)], run_time=0.9)
        self.at("helices and sheets")
        hl = tag("helix", color=TEXT, size=32, pos=V(5.7, -0.2))
        self.play(FadeIn(hl), run_time=0.4)
        self.at("sheets are")
        ya, yb = -2.0, -2.75
        s1 = Arrow(V(-4.6, ya), V(4.6, ya), buff=0, color=BLUE, stroke_width=9, tip_length=0.35)
        s2 = Arrow(V(-4.6, yb), V(4.6, yb), buff=0, color=BLUE, stroke_width=9, tip_length=0.35)
        gx = (-2.6, 0.0, 2.6)
        co = [gchip("C=O").move_to([x, ya, 0]).scale(0.8) for x in gx]
        nh = [gchip("N–H").move_to([x, yb, 0]).scale(0.8) for x in gx]
        bonds = VGroup(*[DashedLine(c.get_bottom(), n.get_top(), dash_length=0.07, dashed_ratio=0.55, color=GREEN, stroke_width=5).set_z_index(9) for c, n in zip(co, nh)])
        for c, n in zip(co, nh):
            chip_set(c, GREEN)
            chip_set(n, GREEN)
        sl = tag("sheet", color=TEXT, size=32, pos=V(5.7, -2.6))
        tall = Buried(sink=1.0, bottom=-3.5)
        self.play(Transform(b.core, tall.core), b.cap.animate.move_to(tall.cap.get_center() + DOWN * 0.0), Create(s1), Create(s2), run_time=0.6)
        self.play(*[FadeIn(x) for x in co + nh], Create(bonds), FadeIn(sl), run_time=0.7)
        self.finish()


# ================================================================== assembly (s18 - s22)
CL = V(-1.0, 0)
SR = 1.34
SUBS = {"a1": (-1.4, 1.4, "α", BLUE, 0.2), "b1": (1.4, 1.4, "β", BETA, 1.1), "b2": (-1.4, -1.4, "β", BETA, 2.0), "a2": (1.4, -1.4, "α", BLUE, 3.1)}


def sub_blob(c, color=BLUE, seed=0.0, r=SR):
    return blobshape(c, r, color=color, a=0.3, seed=seed)


def patch(c, facing, r=SR):
    """A yellow arc on the side of a blob that faces `facing` (0 = right, PI = left)."""
    return Arc(radius=r, start_angle=facing - 0.55, angle=1.1, arc_center=c, color=YELLOW, stroke_width=14).set_z_index(7)


def letter(ch, c, color=TEXT):
    return T(ch, size=50, color=color, font=TITLE_FONT, weight=BOLD).move_to(c).set_z_index(8)


class S18(SpokenScene):
    def construct(self):
        cl, cr = CL + V(-3.2, 0), CL + V(3.2, 0)
        bl, br = sub_blob(cl, seed=0.4), sub_blob(cr, seed=1.3)
        tl = T("folded chain", size=26, color=TEXT).move_to(cl + V(-0.1, -0.35)).set_z_index(8)
        tr = T("folded chain", size=26, color=TEXT).move_to(cr + V(0.1, -0.35)).set_z_index(8)
        pl, pr = patch(cl, 0.0), patch(cr, PI)
        gl, gr = VGroup(bl, tl, pl), VGroup(br, tr, pr)
        self.play(FadeIn(gl, scale=0.8), FadeIn(gr, scale=0.8), run_time=1.0)
        self.at("folded chains")
        self.play(gl.animate.shift(RIGHT * 1.8), gr.animate.shift(LEFT * 1.8), run_time=1.5, rate_func=smooth)
        self.at("oily surface")
        lab = tag("oily surface", color=YELLOW, size=40, pos=CL + V(0, 2.55))
        ld = Line(lab.get_bottom() + DOWN * 0.03, CL + V(0, 0.55), color=YELLOW, stroke_width=4).set_z_index(21)
        self.play(FadeIn(lab, shift=DOWN * 0.15), Create(ld), Indicate(VGroup(pl, pr), color=YELLOW, scale_factor=1.15), run_time=0.8)
        self.finish()


def cluster(letters=True):
    out = {}
    for k, (dx, dy, ch, col, sd) in SUBS.items():
        c = CL + V(dx, dy)
        b = sub_blob(c, color=col, seed=sd)
        out[k] = (b, letter(ch, c) if letters else None)
    return out


def iface_patches():
    """The six yellow interface patches not already drawn on the top pair (a1-b1)."""
    c = {k: CL + V(v[0], v[1]) for k, v in SUBS.items()}
    return VGroup(patch(c["a1"], -PI / 2), patch(c["b2"], PI / 2), patch(c["b1"], -PI / 2), patch(c["a2"], PI / 2),
                  patch(c["b2"], 0.0), patch(c["a2"], PI))


class S19(SpokenScene):
    def construct(self):
        cl, cr = CL + V(-1.4, 0), CL + V(1.4, 0)
        bl, br = sub_blob(cl, seed=0.2), sub_blob(cr, seed=1.1)
        tl = T("folded chain", size=26, color=TEXT).move_to(cl + V(-0.1, -0.35)).set_z_index(8)
        tr = T("folded chain", size=26, color=TEXT).move_to(cr + V(0.1, -0.35)).set_z_index(8)
        pl, pr = patch(cl, 0.0), patch(cr, PI)
        self.add(bl, br, tl, tr, pl, pr)
        self.at("quaternary structure")
        q = tag("quaternary structure", color=TEXT, size=32, pos=V(4.3, 2.2))
        self.play(FadeIn(q, shift=LEFT * 0.2), run_time=0.6)
        self.at("hemoglobin is")
        hl = tag("hemoglobin", color=TEXT, size=32, pos=V(4.3, 1.3))
        c = cluster(letters=False)
        ip = iface_patches()
        self.play(bl.animate.move_to(CL + V(-1.4, 1.4)), br.animate.move_to(CL + V(1.4, 1.4)), tl.animate.move_to(CL + V(-1.5, 1.05)), tr.animate.move_to(CL + V(1.5, 1.05)),
                  pl.animate.shift(UP * 1.4), pr.animate.shift(UP * 1.4), FadeIn(c["b2"][0], shift=UP * 0.8), FadeIn(c["a2"][0], shift=UP * 0.8), FadeIn(hl), run_time=0.6)
        self.play(FadeOut(VGroup(tl, tr)), FadeIn(ip), run_time=0.3)
        self.at("two alpha")
        la = tag("α = alpha", color=BLUE, size=32, pos=V(4.3, 0.2))
        self.play(Write(letter("α", CL + V(-1.4, 1.4))), Write(letter("α", CL + V(1.4, -1.4))), FadeIn(la), run_time=0.7)
        self.at("two beta")
        lb = tag("β = beta", color=BETA, size=32, pos=V(4.3, -0.8))
        self.play(br.animate.set_stroke(color=BETA).set_fill(solid(BETA, 0.3), 1), Write(letter("β", CL + V(1.4, 1.4))), Write(letter("β", CL + V(-1.4, -1.4))), FadeIn(lb), run_time=0.7)
        self.at("working as one")
        frame = RoundedRectangle(corner_radius=0.4, width=6.0, height=6.0, stroke_color=GOLD, stroke_width=5).move_to(CL).set_z_index(9)
        self.play(Create(frame), run_time=0.8)
        self.finish()


def full_cluster(scene):
    c = cluster(letters=True)
    pats = VGroup(patch(CL + V(-1.4, 1.4), 0.0), patch(CL + V(1.4, 1.4), PI), iface_patches())
    for k, (b, l) in c.items():
        scene.add(b, l)
    scene.add(pats)
    return c, pats


VAL_ANG = 0.7


class S20(SpokenScene):
    def construct(self):
        c, pats = full_cluster(self)
        self.at("sickle cell")
        sc = tag("sickle cell", color=RED, size=40, pos=V(4.4, 3.1))
        bpos = CL + V(1.4, 1.4) + SR * V(np.cos(VAL_ANG), np.sin(VAL_ANG))
        bd = Circle(radius=0.3, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.95).move_to(bpos).set_z_index(9)
        lab = tag("Glu6, charged", color=PURPLE, size=34, pos=V(4.3, 2.1))
        lead = Line(bpos + V(0.3, 0), lab.get_left() + LEFT * 0.05, color=GREY, stroke_width=3).set_z_index(9)
        self.play(FadeIn(sc), FadeIn(bd, scale=0.4), FadeIn(lab), Create(lead), run_time=0.8)
        self.at("an oily residue")
        lab2 = tag("Val6, oily", color=YELLOW, size=34, pos=V(4.3, 2.1))
        self.play(bd.animate.set_color(YELLOW), ReplacementTransform(lab, lab2), run_time=0.8)
        self.at("where a charged one")
        was = tag("was: charged", color=PURPLE, size=32, pos=V(4.3, 1.2))
        self.play(FadeIn(was, shift=UP * 0.15), run_time=0.6)
        self.finish()


# --- hemoglobin bodies with a sticky patch (knob) and an oily pocket
HR_ = 1.1
KA = np.radians(35)


def hb_radii(open_):
    return (0.9 * HR_, 1.08 * HR_) if open_ else (HR_, HR_)


def knob_off(open_, s=1.0):
    rx, ry = hb_radii(open_)
    return V(rx * np.cos(KA), ry * np.sin(KA)) * s


class Hb:
    def __init__(self, c, open_=False, s=1.0):
        self.c = np.array(c, float)
        self.s = s
        rx, ry = hb_radii(open_)
        self.body = Ellipse(width=2 * rx * s, height=2 * ry * s, stroke_color=BLUE, stroke_width=4, fill_color=solid(BLUE, 0.3), fill_opacity=1).move_to(self.c).set_z_index(5)
        self.pocket = Circle(radius=0.34 * s, stroke_color=YELLOW, stroke_width=4, fill_color=BG, fill_opacity=1).move_to(self.c - knob_off(open_, s)).set_z_index(6)
        self.knob = Circle(radius=0.27 * s, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=1).move_to(self.c + knob_off(open_, s)).set_z_index(7)
        if not open_:
            self.pocket.set_opacity(0)

    def group(self):
        return VGroup(self.body, self.pocket, self.knob)


def badge(c):
    ci = Circle(radius=0.4, stroke_color=LIGHT, stroke_width=3, fill_color=solid(LIGHT, 0.3), fill_opacity=1)
    tx = T("O2", size=28, color=TEXT)
    return VGroup(ci, tx).move_to(c).set_z_index(8)


DOCK = knob_off(True) * 2


class S21(SpokenScene):
    def construct(self):
        c, pats = full_cluster(self)
        bead = Circle(radius=0.3, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.95).move_to(CL + V(1.4, 1.4) + SR * V(np.cos(VAL_ANG), np.sin(VAL_ANG))).set_z_index(9)
        self.add(bead)
        allc = VGroup(*[x for pair in c.values() for x in pair], pats, bead)
        h1, h2, h3 = Hb(V(-3.0, -2.4)), Hb(V(0, 0)), Hb(V(3.0, 2.4))
        hs = [h1, h2, h3]
        t1 = tag("hemoglobin (all 4 chains)", color=TEXT, size=30, pos=V(-3.4, 1.35))
        ld1 = Line(t1.get_right() + RIGHT * 0.03, h2.c + V(-0.85, 0.4), color=TEXT, stroke_width=3).set_z_index(9)
        self.play(FadeOut(allc, scale=0.3, target_position=h2.c), FadeIn(h2.group(), scale=0.7), FadeIn(h1.group(), scale=0.7), FadeIn(h3.group(), scale=0.7),
                  FadeIn(t1), Create(ld1), run_time=0.7)
        self.at("sticky patch")
        sp = tag("sticky patch (Val6)", color=YELLOW, size=32, pos=V(3.6, -0.5))
        ld = Line(sp.get_left() + LEFT * 0.05, h2.knob.get_center() + V(0.25, -0.1), color=YELLOW, stroke_width=3).set_z_index(9)
        self.play(FadeIn(sp), Create(ld), Indicate(h2.knob, color=YELLOW, scale_factor=1.6), run_time=0.7)
        self.at("once oxygen")
        bd = [badge(h.c + V(-0.15, -0.1)) for h in hs]
        ox = tag("O2 bound", color=LIGHT, size=30, pos=V(-3.6, 0.1))
        self.play(*[FadeIn(b, scale=0.5) for b in bd], FadeOut(sp), FadeOut(ld), FadeOut(t1), FadeOut(ld1), FadeIn(ox), run_time=0.5)
        self.at("is released")
        ox2 = tag("O2 released", color=LIGHT, size=30, pos=V(-3.6, 0.1))
        outs = [V(-1.0, 1.0), V(1.5, -1.5), V(-1.2, 1.2)]
        self.play(*[b.animate.shift(o * 1.4).set_opacity(0) for b, o in zip(bd, outs)], FadeOut(ox), FadeIn(ox2), run_time=0.8)
        self.at("the patch fits")
        o1, o2, o3 = Hb(h1.c, True), Hb(h2.c, True), Hb(h3.c, True)
        self.play(*[ReplacementTransform(h.body, o.body) for h, o in zip(hs, (o1, o2, o3))],
                  *[h.knob.animate.move_to(o.knob.get_center()) for h, o in zip(hs, (o1, o2, o3))], FadeOut(ox2), run_time=0.8)
        self.at("oily pocket")
        for h, o in zip(hs, (o1, o2, o3)):
            h.pocket.move_to(o.pocket.get_center())
        pk = tag("oily pocket", color=YELLOW, size=32, pos=V(-3.0, -0.9))
        pl = Line(pk.get_right() + RIGHT * 0.05, h2.pocket.get_center() + V(-0.35, -0.05), color=YELLOW, stroke_width=3).set_z_index(9)
        self.play(*[h.pocket.animate.set_opacity(1) for h in hs], FadeIn(pk), Create(pl), run_time=0.7)
        self.at("neighboring hemoglobin")
        g1 = VGroup(o1.body, h1.pocket, h1.knob)
        nb = tag("neighbouring hemoglobin", color=TEXT, size=28, pos=V(4.2, 0.3))
        self.play(g1.animate.shift(h2.c - DOCK - h1.c), FadeOut(pk), FadeOut(pl), FadeIn(nb), run_time=0.7)
        g3 = VGroup(o3.body, h3.pocket, h3.knob)
        self.play(g3.animate.shift(h2.c + DOCK - h3.c), run_time=0.7)
        self.finish()


class S22(SpokenScene):
    def construct(self):
        hs = {k: Hb(DOCK * k, True) for k in (-1, 0, 1)}
        for h in hs.values():
            self.add(h.group())
        self.at("unwanted contact", lead=0.0)
        rings = VGroup()
        ring_of = {}
        for k in (-1, 0):
            r = Circle(radius=0.42, stroke_color=ORANGE, stroke_width=6).move_to(DOCK * k + knob_off(True)).set_z_index(9)
            ring_of[k] = r
            rings.add(r)
        lab = tag("an unwanted interface", color=ORANGE, size=34, pos=V(3.7, -1.3))
        lead = always_redraw(lambda: Line(lab.get_left() + LEFT * 0.03, ring_of[0].get_center() + V(0.3, -0.25), color=ORANGE, stroke_width=3.5).set_z_index(21))
        self.play(Create(rings), FadeIn(lab), Create(lead), run_time=0.8)
        self.at("whole hemoglobins")
        mid = VGroup(*[h.group() for h in hs.values()], rings)
        sc = 0.85
        far = {k: Hb(DOCK * k * sc, True, sc) for k in (-2, 2)}
        newr = VGroup(*[Circle(radius=0.42 * sc, stroke_color=ORANGE, stroke_width=6).move_to(DOCK * k * sc + knob_off(True, sc)).set_z_index(9) for k in (-2, -1, 0, 1)])
        # rings on the three interfaces already drawn move with the group; add the two new ones
        extra = VGroup(newr[0], newr[3])
        self.play(mid.animate.scale(sc, about_point=ORIGIN), LaggedStart(FadeIn(far[-2].group()), FadeIn(far[2].group()), lag_ratio=0.5), FadeIn(extra), run_time=1.5)
        self.wait(0.2)
        self.at("same rule")
        rl = VGroup(tag("same rule:", color=YELLOW, size=34), tag("bury oily surface", color=YELLOW, size=34)).arrange(DOWN, buff=0.1).move_to(V(4.3, -2.7))
        self.play(FadeIn(rl, shift=UP * 0.15), run_time=0.6)
        self.finish()


# ================================================================== stability (s23 - s29)
def sq_icon(c, s=1.0):
    """an unfolded coil: a loose squiggle"""
    f = ParametricFunction(lambda t: np.array([t * 1.0, 0.3 * np.sin(2.6 * t) + 0.12 * np.sin(5.1 * t + 1), 0.0]), t_range=[-1.5, 1.5, 0.02], color=RED, stroke_width=7)
    return f.scale(s).move_to(c)


def fold_icon(c, r=0.7):
    return blobshape(c, r, color=BLUE, a=0.35, sw=4)


class S23(SpokenScene):
    def construct(self):
        yU, yF = 1.0, 0.15
        o = 0.9     # centres the diagram
        ub = Line(V(-5.2 + o, yU), V(-1.5 + o, yU), color=RED, stroke_width=10)
        fb = Line(V(1.5 + o, yF), V(5.0 + o, yF), color=GREEN, stroke_width=10)
        ax = Arrow(V(-6.0 + o, -2.9), V(-6.0 + o, 3.3), buff=0, color=GREY, stroke_width=4, tip_length=0.25)
        axl = T("free energy", size=28, color=GREY).rotate(PI / 2).move_to(V(-6.55 + o, 0.2))
        ul = T("unfolded coil", size=34, color=RED).move_to(V(-3.0 + o, yU - 0.5))
        ui = sq_icon(V(-3.0 + o, yU + 0.5), 0.9)
        fl = T("folded", size=34, color=GREEN).move_to(V(3.25 + o, yF - 0.5))
        fi = fold_icon(V(3.25 + o, yF + 0.85), 0.6)
        self.play(Create(ax), FadeIn(axl), Create(ub), Create(fb), FadeIn(ul), Create(ui), FadeIn(fl), FadeIn(fi, scale=0.6), run_time=0.8)
        self.at("folded protein")
        self.play(Indicate(fi, color=GREEN, scale_factor=1.25), run_time=0.6)
        self.at("marginally more stable")
        arr = DoubleArrow(V(0.0 + o, yU), V(0.0 + o, yF), buff=0, color=GOLD, stroke_width=6, tip_length=0.14, max_tip_length_to_length_ratio=0.45)
        dl = Line(V(-1.5 + o, yU), V(0.2 + o, yU), color=GOLD, stroke_width=2)
        gap = tag("small gap", color=GOLD, size=36, pos=V(0.0 + o, yF - 0.75))
        self.play(Create(arr), Create(dl), FadeIn(gap), run_time=0.8)
        self.at("than the unfolded")
        # a large reference standing on the unfolded level: the freedom the chain gives up (compare s24)
        rx = -5.55 + o
        ref = DoubleArrow(V(rx, yU), V(rx, yU + 2.4), buff=0, color=ORANGE, stroke_width=6, tip_length=0.25)
        refl = T("freedom given up", size=28, color=ORANGE).rotate(PI / 2).move_to(V(rx + 0.4, yU + 1.4))
        self.play(Create(ref), FadeIn(refl), run_time=0.7)
        self.finish()


def schip(text, color, size=30):
    label = T(text, size=size, color=color)
    box = RoundedRectangle(corner_radius=0.14, width=label.width + 0.44, height=label.height + 0.4, stroke_color=color, stroke_width=3,
                           fill_color=solid(color, 0.22), fill_opacity=1)
    return VGroup(box, label.move_to(box)).set_z_index(15)


class S24(SpokenScene):
    def construct(self):
        ang = ValueTracker(0.0)
        piv = V(0, 2.3)
        L = 3.75
        ends = lambda: (piv + L * V(-np.cos(ang.get_value()), -np.sin(ang.get_value())), piv + L * V(np.cos(ang.get_value()), np.sin(ang.get_value())))
        post = Line(piv, V(0, -3.2), color=GREY, stroke_width=8)
        base = Rectangle(width=2.4, height=0.25, stroke_width=0, fill_color=GREY, fill_opacity=1).move_to(V(0, -3.3))
        beam = always_redraw(lambda: Line(ends()[0], ends()[1], color=TEXT, stroke_width=9))
        hang = 2.6

        def pan(side):
            e = ends()[side]
            c = e + DOWN * hang
            return VGroup(Line(e, c + V(-1.7, 0), color=GREY, stroke_width=3), Line(e, c + V(1.7, 0), color=GREY, stroke_width=3),
                          Line(c + V(-1.8, 0), c + V(1.8, 0), color=TEXT, stroke_width=7))
        pl = always_redraw(lambda: pan(0))
        pr = always_redraw(lambda: pan(1))
        pivdot = Dot(piv, radius=0.12, color=TEXT)
        self.add(post, base, beam, pl, pr, pivdot)
        self.wait(0.3)
        free = schip("freedom given up", ORANGE)
        con = schip("contacts made", GREEN)
        wat = schip("water freed", TEAL)
        # the labels rest inside the pans, on a solid backing that hides the hanging lines
        free.add_updater(lambda m: m.move_to(ends()[0] + DOWN * (hang - 0.5)))
        con.add_updater(lambda m: m.move_to(ends()[1] + DOWN * (hang - 0.45)))
        wat.add_updater(lambda m: m.move_to(ends()[1] + DOWN * (hang - 1.25)))
        self.at("gives up a lot of freedom")
        self.add(free)
        self.play(FadeIn(free, shift=DOWN * 0.8), run_time=0.4)
        self.play(ang.animate.set_value(0.16), run_time=1.0)
        self.at("contacts")
        self.add(con, wat)
        self.play(FadeIn(con, shift=DOWN * 0.8), run_time=0.4)
        self.play(FadeIn(wat, shift=DOWN * 0.8), ang.animate.set_value(-0.035), run_time=1.0)
        self.at("only just pay")
        ah = tag("only just ahead", color=GOLD, size=36, pos=V(0, 3.45))
        self.play(Indicate(beam, color=GOLD, scale_factor=1.0), FadeIn(ah), run_time=0.8)
        self.finish()


# melting curves, computed from a two-state model: dG = dH (1 - T/Tm), fraction folded = 1 / (1 + exp(-dG / RT))
DH, RGAS = 400.0, 0.008314


def fold_frac(T_, Tm):
    dG = DH * (1 - T_ / Tm)
    return 1 / (1 + np.exp(-dG / (RGAS * T_)))


class Melt:
    def __init__(self, ox, oy, w, h, xl_dy=0.6):
        self.ox, self.oy, self.w, self.h = ox, oy, w, h
        self.axes = VGroup(Arrow(V(ox, oy), V(ox + w + 0.2, oy), buff=0, color=GREY, stroke_width=4, tip_length=0.22),
                           Arrow(V(ox, oy), V(ox, oy + h + 0.2), buff=0, color=GREY, stroke_width=4, tip_length=0.22))
        self.ticks = VGroup(T("0", size=26, color=GREY).move_to(V(ox - 0.3, oy)), T("1", size=26, color=GREY).move_to(V(ox - 0.3, oy + h)),
                            T("0.5", size=26, color=GREY).move_to(V(ox - 0.46, oy + h / 2)))
        self.xl = T("temperature", size=28, color=GREY).move_to(V(ox + w / 2, oy - xl_dy))
        self.yl = T("fraction folded", size=28, color=GREY).rotate(PI / 2).move_to(V(ox - 1.0, oy + h / 2))
        self.static = VGroup(self.axes, self.ticks, self.xl, self.yl)

    def x_of(self, Tm):
        return self.ox + self.w * (Tm - 300) / 80

    def curve(self, Tm, color=BLUE, width=7):
        return ParametricFunction(lambda t: np.array([self.ox + self.w * t, self.oy + self.h * fold_frac(300 + 80 * t, Tm), 0.0]),
                                  t_range=[0.0, 1.0, 0.005], color=color, stroke_width=width)

    def mid(self, Tm):
        return V(self.x_of(Tm), self.oy + self.h / 2)

    def drop(self, Tm, color, width=4):
        mid = self.mid(Tm)
        return VGroup(Dot(mid, radius=0.13, color=color).set_z_index(9),
                      DashedLine(mid, V(mid[0], self.oy), dash_length=0.1, color=color, stroke_width=width))


class S25(SpokenScene):
    def construct(self):
        m = Melt(-4.2, -2.6, 8.8, 5.2)
        self.play(FadeIn(m.static), run_time=0.5)
        fl = T("folded", size=30, color=GREEN).move_to(V(-3.1, 2.95))
        ufl = T("unfolded", size=30, color=RED).move_to(V(3.7, -1.95))
        self.add(fl, ufl)
        self.at("heat can undo")
        cur = m.curve(340)
        dot = Dot(V(m.ox, m.oy + m.h), radius=0.13, color=GOLD).set_z_index(9)
        self.add(dot)
        self.play(Create(cur, rate_func=linear), run_time=1.6)
        self.add(cur)
        self.at("melting temperature")
        mid = m.mid(340)
        mk = Dot(mid, radius=0.16, color=GOLD).set_z_index(9)
        vl = DashedLine(mid, V(mid[0], m.oy), dash_length=0.1, color=GOLD, stroke_width=4)
        tm = tag("Tm", color=GOLD, size=44, pos=mid + V(0.7, 0.55))
        self.play(FadeOut(dot), FadeIn(mk, scale=0.4), Create(vl), FadeIn(tm), run_time=0.7)
        self.at("half the molecules")
        hl = DashedLine(V(m.ox, mid[1]), mid, dash_length=0.1, color=GOLD, stroke_width=4)
        hn = tag("half unfolded", color=GOLD, size=32, pos=V(m.ox + 1.9, mid[1] + 0.5))
        self.play(Create(hl), FadeIn(hn), run_time=0.7)
        self.finish()


PR_ = 2.1   # panel blob radius (two panels fill over half the frame height)


def panel_blob(c, r=PR_):
    body = blobshape(c, r, color=BLUE, a=0.2, seed=0.5, sw=4).set_z_index(2)
    core = blobshape(c, r * 0.52, color=YELLOW, a=0.3, seed=1.1, sw=3).set_z_index(3)
    return VGroup(body, core)


def rbead(pos, name, color, sign="", r=0.52):
    c = Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=solid(color, 0.55), fill_opacity=1)
    t = T(name + sign, size=28, color=TEXT)
    return VGroup(c, t).move_to(pos).set_z_index(9)


LP = V(-3.4, 0.2)
RP = V(3.4, 0.2)
MINUS = "−"


def surf_pos(c, r=PR_):
    return c + (r - 0.02) * V(np.cos(0.6), np.sin(0.6))


def ring_timer(frac):
    tr = ValueTracker(frac)
    ring = always_redraw(lambda: Arc(start_angle=PI / 2, angle=TAU * max(tr.get_value(), 0.001), radius=0.5, color=GOLD, stroke_width=9).move_to([6.1, -3.35, 0]).set_z_index(20))
    back = Circle(radius=0.5, color=GREY, stroke_width=4).move_to([6.1, -3.35, 0])
    return tr, ring, back


class S26(SpokenScene):
    def construct(self):
        L, R = panel_blob(LP), panel_blob(RP)
        leu = rbead(LP, "Leu", YELLOW)
        lys = rbead(surf_pos(RP), "Lys", PURPLE, "+")
        hl = tag("buried in the core", color=YELLOW, size=34, pos=V(LP[0], 2.9))
        hr = tag("on the surface", color=PURPLE, size=34, pos=V(RP[0], 2.9))
        self.play(FadeIn(L), FadeIn(R), FadeIn(leu), FadeIn(lys), FadeIn(hl), FadeIn(hr), run_time=1.0)
        self.at("buried leucine")
        asp = rbead(LP, "Asp", PURPLE, MINUS)
        cl = tag("Leu → Asp", color=TEXT, size=36, pos=V(LP[0], -2.55))
        self.play(ReplacementTransform(leu, asp), FadeIn(cl), run_time=0.8)
        self.at("surface lysine")
        arg = rbead(surf_pos(RP), "Arg", PURPLE, "+")
        cr = tag("Lys → Arg", color=TEXT, size=36, pos=V(RP[0], -2.55))
        self.play(ReplacementTransform(lys, arg), FadeIn(cr), run_time=0.8)
        self.at("which one melts lower")
        q = tag("Which one melts lower?", color=GOLD, size=46, pos=V(-0.4, -3.4))
        total = 9.25 + 0.4 - self.elapsed() + 5.4
        tr, ring, back = ring_timer(1.0)
        self.add(back, ring)
        self.play(FadeIn(q, shift=UP * 0.15), run_time=0.7)
        rest = 9.25 + 0.4 - self.elapsed()
        self.play(tr.animate.set_value(1.0 - rest / total), run_time=max(rest, 0.1), rate_func=linear)
        self.finish()


class S27Pause(NarratedScene):
    def construct(self):
        L, R = panel_blob(LP), panel_blob(RP)
        asp = rbead(LP, "Asp", PURPLE, MINUS)
        arg = rbead(surf_pos(RP), "Arg", PURPLE, "+")
        hl = tag("buried in the core", color=YELLOW, size=34, pos=V(LP[0], 2.9))
        hr = tag("on the surface", color=PURPLE, size=34, pos=V(RP[0], 2.9))
        cl = tag("Leu → Asp", color=TEXT, size=36, pos=V(LP[0], -2.55))
        cr = tag("Lys → Arg", color=TEXT, size=36, pos=V(RP[0], -2.55))
        q = tag("Which one melts lower?", color=GOLD, size=46, pos=V(-0.4, -3.4))
        self.add(L, R, asp, arg, hl, hr, cl, cr, q)
        # the countdown ring began in the previous scene (about 2 s already used of ~7.6 s)
        total = 2.2 + 5.4
        tr, ring, back = ring_timer(1.0 - 2.2 / total)
        self.add(back, ring)
        self.play(tr.animate.set_value(0.001), run_time=5.3, rate_func=linear)
        self.finish()


class S28(SpokenScene):
    def construct(self):
        c = V(-3.5, 0.2)
        L = panel_blob(c, 1.9)
        asp = rbead(c, "Asp", PURPLE, MINUS)
        hd = tag("Leu → Asp in the core", color=TEXT, size=32, pos=V(c[0], 2.75))
        pack = VGroup(*[Circle(radius=0.17, stroke_color=YELLOW, stroke_width=2, fill_color=YELLOW, fill_opacity=0.9).move_to(c + 0.95 * V(np.cos(a), np.sin(a))).set_z_index(8)
                        for a in np.linspace(0.3, 0.3 + TAU, 7)[:-1]])
        m = Melt(0.9, -2.2, 5.2, 4.8, xl_dy=1.25)
        wt = m.curve(340)
        self.add(L, asp, hd, pack)
        self.play(FadeIn(m.static), Create(wt), run_time=0.5)
        self.at("buried aspartate")
        glow = Circle(radius=0.78, stroke_color=ORANGE, stroke_width=9, fill_color=ORANGE, fill_opacity=0.25).move_to(c).set_z_index(7)
        self.play(FadeIn(glow), asp.animate.set_stroke(color=ORANGE), run_time=0.7)
        self.at("it is charged")
        cw = tag("charged, no water to bond with", color=ORANGE, size=28, pos=V(c[0], -2.6))
        self.play(FadeIn(cw), run_time=0.6)
        self.at("breaks up the oily packing", lead=0.75)
        ghost = m.curve(340, color=GREY, width=4).set_stroke(opacity=0.7)
        gd = m.drop(340, GREY)
        new = m.curve(322, color=ORANGE)
        shifts = [0.18 * V(np.cos(a), np.sin(a)) for a in np.linspace(0.3, 0.3 + TAU, 7)[:-1]]
        self.add(ghost)
        self.play(Transform(wt, new), *[p.animate.shift(s * 1.0) for p, s in zip(pack, shifts)], FadeIn(gd), run_time=0.9)
        od = m.drop(322, ORANGE, width=5)
        lo = tag("lower Tm", color=ORANGE, size=34, pos=V(m.x_of(322) - 0.15, m.oy - 0.5))
        self.play(FadeIn(od), FadeIn(lo), run_time=0.4)
        self.finish()


class S29(SpokenScene):
    def construct(self):
        c = V(-3.5, 0.2)
        L = panel_blob(c, 1.9)
        sp = surf_pos(c, 1.9)
        lys = rbead(sp, "Lys", PURPLE, "+")
        hd = tag("Lys → Arg on the surface", color=TEXT, size=32, pos=V(c[0], 2.75))
        m = Melt(0.9, -2.2, 5.2, 4.8, xl_dy=1.25)
        wt = m.curve(340, color=GREY, width=4).set_stroke(opacity=0.7)
        gd = m.drop(340, GREY)
        self.add(L, lys, hd, m.static, wt, gd)
        self.at("surface swap")
        arg = rbead(sp, "Arg", PURPLE, "+")
        self.play(ReplacementTransform(lys, arg), run_time=0.7)
        self.at("still in water")
        ws = [swater(sp + V(0.95, 0.0), 0.0, op=1.0, w=5), swater(sp + V(0.6, 0.8), 0.4, op=1.0, w=5), swater(sp + V(0.75, -0.75), -0.4, op=1.0, w=5)]
        wl = tag("in water", color=TEAL, size=30, pos=sp + V(0.2, -1.5))
        self.play(*[FadeIn(w) for w in ws], FadeIn(wl), run_time=0.7)
        self.at("stability barely changes", lead=0.8)
        new = m.curve(339, color=BLUE)
        self.play(Create(new), run_time=0.8)
        bd = m.drop(339, BLUE, width=5)
        tb = tag("Tm barely moves", color=GREEN, size=34, pos=V(m.x_of(340) + 0.45, m.oy - 0.5))
        self.play(FadeIn(bd), FadeIn(tb), run_time=0.4)
        self.finish()


class S30(SpokenScene):
    def construct(self):
        G, AL = 0.12, 1.0     # standoff and (equal) arrow length for every push arrow
        cL = V(-3.2, 0.2)
        body = blobshape(cL, 1.6, color=BLUE, a=0.2, seed=0.5, sw=4).set_z_index(2)
        core = blobshape(cL, 0.9, color=YELLOW, a=0.3, seed=1.1, sw=3).set_z_index(3)
        cA, cB = V(1.9, 0.2), V(4.1, 0.2)
        ba = blobshape(cA, 1.0, color=BLUE, a=0.25, seed=0.2).set_z_index(2)
        bb = blobshape(cB, 1.0, color=BETA, a=0.25, seed=0.9).set_z_index(2)
        pa = Arc(radius=1.0, start_angle=-0.5, angle=1.0, arc_center=cA, color=YELLOW, stroke_width=12).set_z_index(5)
        pb = Arc(radius=1.0, start_angle=PI - 0.5, angle=1.0, arc_center=cB, color=YELLOW, stroke_width=12).set_z_index(5)
        self.add(body, core, ba, bb)
        self.at("water pushes oil inward")

        def push(c, r, deg):
            u = V(np.cos(np.radians(deg)), np.sin(np.radians(deg)))
            return Arrow(c + u * (r + G + AL), c + u * (r + G), buff=0, color=TEAL, stroke_width=11, tip_length=0.34, max_tip_length_to_length_ratio=0.5).set_z_index(18)
        arrs = VGroup()
        for a in (30, 90, 150, 210, 270, 330):
            arrs.add(push(cL, 1.6, a))
        for c, r, degs in ((cA, 1.0, (120, 240)), (cB, 1.0, (60, 300, 0))):
            for d in degs:
                arrs.add(push(c, r, d))
        self.play(LaggedStart(*[GrowArrow(a) for a in arrs], lag_ratio=0.08), run_time=1.5)
        self.at("burial builds")
        self.play(arrs.animate.set_opacity(0.8), run_time=0.5)
        self.at("the core")
        cg = Circle(radius=0.9, stroke_width=0, fill_color=YELLOW, fill_opacity=0.3).move_to(cL).set_z_index(4)
        cl = T("core", size=34, color=YELLOW).move_to(cL).set_z_index(10)
        self.play(FadeIn(cg), FadeIn(cl), run_time=0.6)
        self.at("the interfaces")
        self.play(Create(pa), Create(pb), run_time=0.5)
        il = tag("interface", color=YELLOW, size=42, weight=BOLD, pos=V(3.0, -2.2))
        self.play(FadeIn(il), run_time=0.4)
        self.finish()


class S31End(EndCard):
    LINE = "Water pushes oily side chains inward, and that burial builds\nthe core, the interfaces and a fold that is only just stable."
