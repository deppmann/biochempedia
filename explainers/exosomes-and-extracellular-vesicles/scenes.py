"""Exosomes and extracellular vesicles: an exosome is named by its origin  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = the receptor (transferrin receptor): a stalk with a round head, head = the part that sat outside the cell
  TEAL   = a small vesicle (outline): internal vesicle, exosome, microvesicle, "vesicle" labels
  YELLOW = cytosol, the cell's own fluid (the tint of the cell interior and the fill inside every vesicle)
  PURPLE = the multivesicular body / endosome, and the "formed inside it" origin of an exosome
  RED    = the lysosome and digestion (the incinerator door)
  GREEN  = the street door: released from the cell, intact
  ORANGE = tetraspanin markers (the small dots on a vesicle's surface)
  GOLD   = the message (a signal carried to another cell)
  GREY   = membranes (plasma membrane), labels, what is unknown or not shown (dashed)

No molecular structures: a receptor is a stalk with a round head, a vesicle is a circle, the
compartment is a ring, membranes are lines, the cytosol is a tint. Nothing is drawn atom by atom.

Layout changes with the action (nothing sits in a fixed stage):
  s01 the cell surface fills the lower frame, vesicles are thrown up and away;
  s02 the compartment is huge, centred, and fills the frame height;
  s03 it shrinks left, a lysosome comes in on the right and the cell surface on top;
  s04 a flat membrane, one bud, large;  s05 one wide cell surface;  s06 a three-part diagram.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"

CY = 0.14                                   # cytosol tint opacity (background AND inside vesicles)
CYC = interpolate_color(ManimColor(BG), ManimColor(YELLOW), CY)   # the cytosol as a flat colour (for patches)


# ---------------------------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------------------------
def dv(deg):
    a = np.radians(deg)
    return np.array([np.cos(a), np.sin(a), 0.0])


def P(x, y):
    return np.array([x, y, 0.0])


def bchip(text, color=BLUE, size=24, pad=0.2, **kw):
    """chip with an opaque backing so lines drawn behind it do not show through."""
    c = chip(text, color, size=size, pad=pad, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def ghost_chip(text, size=24, color=GREY):
    """a dashed chip: something not yet known, or not shown."""
    t = T(text, size, color)
    box = RoundedRectangle(corner_radius=0.14, width=t.width + 0.44, height=t.height + 0.34)
    back = box.copy().set_stroke(width=0).set_fill(BG, 1)
    return VGroup(back, DashedVMobject(box, num_dashes=max(18, int(box.width * 9))).set_color(color), t)


def strike(m, color=RED, w=7):
    return Line(m.get_corner(DL) + [-0.08, -0.04, 0], m.get_corner(UR) + [0.08, 0.04, 0], color=color, stroke_width=w)


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def darr(a, b, color=GREY, w=4, tip=0.2):
    """dashed arrow: a path that is not established."""
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    line = DashedLine(a, b - d * tip * 0.9, color=color, stroke_width=w, dash_length=0.12)
    perp = np.array([-d[1], d[0], 0.0])
    head = Polygon(b, b - d * tip + perp * tip * 0.5, b - d * tip - perp * tip * 0.5, stroke_width=0,
                   fill_color=color, fill_opacity=1)
    return VGroup(line, head)


def pop(m, s=1.3):
    return m.animate(rate_func=there_and_back).scale(s)


def glow(*mobs, s=1.1, color=TEXT):
    """flash each mobject in place (one animation per mobject)."""
    return [Indicate(m, color=color, scale_factor=s) for m in mobs]


def membrane_line(y, x0=-6.3, x1=6.3, color=GREY, w=12):
    return Line(P(x0, y), P(x1, y), color=color, stroke_width=w).set_cap_style(CapStyleType.ROUND)


def tint_rect(top, bottom=-4.1):
    """the cytosol: a tint over everything between `top` and `bottom` (whole frame width)."""
    r = Rectangle(width=14.4, height=top - bottom, stroke_width=0, fill_color=YELLOW, fill_opacity=CY)
    r.move_to(P(0, (top + bottom) / 2))
    r.set_z_index(-5)
    return r


def lolli(base, d, length=0.5, head=0.11, w=5.0, color=BLUE):
    """a receptor: a stalk standing on a membrane, a round head at its tip (the part that sat outside the cell)."""
    base, d = np.array(base, float), np.array(d, float)
    d = d / np.linalg.norm(d)
    tip = base + d * length
    return VGroup(Line(base, tip, color=color, stroke_width=w), Dot(tip, radius=head, color=color))


def lol_dims(r):
    return 0.8 * r + 0.1, 0.06 + 0.10 * r, 3.0 + 3.5 * r        # stalk length, head radius, stroke width


class Ves:
    """a vesicle: circle with cytosol inside and receptors (and tetraspanin dots) on its outer face."""

    def __init__(self, c, r=0.35, angles=(), marks=(), edge=3.5, color=TEAL):
        self.c, self.r = np.array(c, float), r
        self.back = Circle(radius=r, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(self.c)
        self.body = Circle(radius=r, stroke_color=color, stroke_width=edge, fill_color=YELLOW,
                           fill_opacity=CY).move_to(self.c)
        s, h, w = lol_dims(r)
        self.lols = [lolli(self.c + r * dv(a), dv(a), s, h, w) for a in angles]
        self.marks = [Dot(self.c + r * dv(a), radius=0.05 + 0.05 * r, color=ORANGE) for a in marks]

    def shell(self):
        return VGroup(self.back, self.body)

    def group(self):
        return VGroup(self.back, self.body, *self.marks, *self.lols)


class Mvb:
    """the multivesicular body: a ring with internal vesicles, built at radius R around centre c."""
    ANG = [130, 58, -14, -86, -158]            # where the five vesicles sit (degrees round the ring)
    LOL = [(95, 165), (30, 95), (-45, 20), (-115, -50), (-195, -130)]

    def __init__(self, c, R, ring_w=7, with_lols=True):
        self.c, self.R = np.array(c, float), R
        self.ring = Circle(radius=R, stroke_color=PURPLE, stroke_width=ring_w, fill_color=BG,
                           fill_opacity=1).move_to(self.c)
        self.centers = [self.c + 0.58 * R * dv(a) for a in self.ANG]
        self.ves = [Ves(p, 0.17 * R, self.LOL[i] if with_lols else ()) for i, p in enumerate(self.centers)]

    def group(self):
        return VGroup(self.ring, *[v.group() for v in self.ves])


# --- a bud: the membrane pushes into a space, away from the cytosol, and pinches off a vesicle ----------
def _stadium(c, n_deg, hl, hw, k=14):
    n, t = dv(n_deg), dv(n_deg + 90)
    tip, base = c + n * (hl - hw), c - n * (hl - hw)
    pts = [tip + hw * (np.cos(np.radians(a)) * n + np.sin(np.radians(a)) * t) for a in np.linspace(-90, 90, k + 1)]
    pts += [base + hw * (np.cos(np.radians(a)) * n + np.sin(np.radians(a)) * t) for a in np.linspace(90, 270, k + 1)]
    return pts + [pts[0]]


def _finger(p, n_deg, L, w, k=14):
    """an open U: a tube of cytosol standing on the membrane at p, running along n for length L."""
    n, t = dv(n_deg), dv(n_deg + 90)
    tip = p + n * max(L - w, 0.0)
    pts = [p - t * w]
    pts += [tip + w * (np.cos(np.radians(a)) * n + np.sin(np.radians(a)) * t) for a in np.linspace(-90, 90, k + 1)]
    pts += [p + t * w]
    return pts


def _pair(pts, edge=3.5):
    body = VMobject().set_points_as_corners(pts).set_stroke(TEAL, edge).set_fill(YELLOW, CY)
    back = VMobject().set_points_as_corners(pts).set_stroke(width=0).set_fill(BG, 1)
    return VGroup(back, body)


class Bud:
    """Phase 1 (grow): a finger of cytosol pushes along n from the membrane at p.
    Phase 2 (pinch): it closes into a vesicle, shrinks to a circle of radius r and travels to c_final."""

    def __init__(self, p, n_deg, c_final, r, L=0.95, w=0.27, patch_w=0.5):
        self.p, self.n_deg, self.cf, self.r, self.L, self.w = np.array(p, float), n_deg, np.array(c_final, float), r, L, w
        self.holder = VGroup(self._patch(1.0, 0.12), *_pair(_finger(self.p, n_deg, 0.12, 0.12)))
        self.patch_w = patch_w

    def _patch(self, op, pw):
        # hides the membrane right where the finger opens onto the cytosol side
        rect = Rectangle(width=2 * pw + 0.04, height=0.26, stroke_width=0, fill_color=CYC, fill_opacity=op)
        rect.rotate(np.radians(self.n_deg + 90)).move_to(self.p)
        return rect

    def outline(self, a):
        """the bud's outline (a list of points) and its centre, at progress a."""
        if a < 0.5:
            u = a / 0.5
            Lc, wc = 0.12 + (self.L - 0.12) * u, 0.12 + (self.w - 0.12) * u
            return _finger(self.p, self.n_deg, Lc, wc), self.p + dv(self.n_deg) * (Lc / 2), wc, 1.0
        u = (a - 0.5) / 0.5
        u = u * u * (3 - 2 * u)
        n = dv(self.n_deg)
        c0 = self.p + n * (self.L / 2)
        hl, hw = self.L / 2 + (self.r - self.L / 2) * u, self.w + (self.r - self.w) * u
        c = c0 + (self.cf - c0) * u
        return _stadium(c, self.n_deg, hl, hw), c, self.w, 1.0 - min(1.0, u * 3)

    def state(self, a):
        pts, c, pw, op = self.outline(a)
        return VGroup(self._patch(op, pw), *_pair(pts))

    def rider(self, a, theta, flat_base, stalk, head, w, blend=0.3):
        """a receptor that stands on the flat membrane at flat_base, then rides on the bud's outer face
        (the face away from the cytosol) at angle theta from the bud's centre, its head pointing out."""
        pts, c, _, _ = self.outline(a)
        P_ = np.array(pts[:-1]) if np.allclose(pts[0], pts[-1]) else np.array(pts)
        ang = np.degrees(np.arctan2(P_[:, 1] - c[1], P_[:, 0] - c[0]))
        d = np.abs(((ang - theta + 180) % 360) - 180)
        i = int(np.argmin(d))
        t = P_[min(i + 1, len(P_) - 1)] - P_[max(i - 1, 0)]
        nrm = np.array([t[1], -t[0], 0.0])
        nrm = nrm / (np.linalg.norm(nrm) + 1e-9)
        if np.dot(nrm, P_[i] - c) < 0:
            nrm = -nrm
        s = min(1.0, a / blend)
        s = s * s * (3 - 2 * s)
        base = (1 - s) * np.array(flat_base, float) + s * P_[i]
        dr = (1 - s) * dv(self.n_deg) + s * nrm
        return lolli(base, dr / np.linalg.norm(dr), stalk, head, w)

    def anim_with(self, riders, specs, a0, a1, **kw):
        """grow/pinch the bud while the riders (receptors) are carried on it. specs = [(theta, flat_base, stalk, head, w)]."""
        group = VGroup(self.holder, *riders)

        def upd(m, al):
            a = a0 + (a1 - a0) * al
            self.holder.become(self.state(a))
            for r, sp in zip(riders, specs):
                r.become(self.rider(a, *sp))
        return UpdateFromAlphaFunc(group, upd, **kw)

    def anim(self, a0, a1, **kw):
        return UpdateFromAlphaFunc(self.holder, lambda m, a: m.become(self.state(a0 + (a1 - a0) * a)), **kw)

    def grow(self, **kw):
        return self.anim(0.0, 0.5, **kw)

    def pinch(self, **kw):
        return self.anim(0.5, 1.0, **kw)


class Film(SpokenScene):
    def outro(self, *anims, then=None, run_time=0.3, then_time=0.7):
        """start as the last word ends (the voice leaves about 0.4 s of silence), clear what the next scene
        does not inherit, then (optionally) change the picture to the next scene's first frame."""
        rest = self.narration_s - 0.3 - self.elapsed()
        if rest > 0:
            self.wait(rest)
        if anims:
            self.play(*anims, run_time=run_time)
        if then:
            self.play(*then, run_time=then_time)
            self.wait(0.05)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Exosomes and Extracellular Vesicles"
    TITLE = "An exosome is named by its origin"


# ---------------------------------------------------------------------------------------------
S1_MEM = -1.45                    # the cell surface in scene 1
S1_X = [-2.5, -1.25, 0.0, 1.25, 2.5]
S1_TO = [P(-2.5, 0.8), P(-1.25, 1.85), P(0.0, 1.0), P(1.25, 1.85), P(2.5, 0.8)]
S1_Q = P(2.5, -2.55)              # the question-mark box inside the cell


def q_box(c):
    box = RoundedRectangle(corner_radius=0.16, width=1.7, height=1.15).move_to(c)
    back = box.copy().set_stroke(width=0).set_fill(BG, 1)
    edge = DashedVMobject(box, num_dashes=30).set_color(PURPLE)
    q = T("?", 44, TEXT, weight=BOLD).move_to(c)
    return VGroup(back, edge, q)


class S01Question(Film):
    """a red blood cell throws its receptors out on vesicles; rubbish or a message; but from where?"""

    def construct(self):
        tint = tint_rect(S1_MEM)
        mem = membrane_line(S1_MEM, w=16)
        self.add(tint)
        cell_lbl = T("nearly mature\nred blood cell", 28, TEXT, line_spacing=0.9).move_to(P(-2.7, -2.55))
        self.at("red blood cell")
        self.play(Create(mem), FadeIn(cell_lbl, shift=UP * 0.1), run_time=0.8)

        # the receptors stand on the membrane
        lols = [lolli(P(x, S1_MEM + 0.09), UP, 0.7, 0.14, 6.0) for x in S1_X]
        rec_lbl = T("transferrin receptor", 26, BLUE).move_to(P(-4.7, -0.65))
        ptr = Line(P(-3.0, -0.65), P(-2.6, -0.65), color=BLUE, stroke_width=3)
        self.at("throws its")
        self.play(LaggedStart(*[GrowFromPoint(l, l[0].get_start()) for l in lols], lag_ratio=0.1),
                  FadeIn(rec_lbl), Create(ptr), run_time=0.9)

        # thrown out of the cell, each one in a small vesicle
        vs = [Ves(c, 0.58, [90]) for c in S1_TO]
        self.at("out of the cell")
        self.play(FadeOut(rec_lbl), FadeOut(ptr),
                  LaggedStart(*[AnimationGroup(ReplacementTransform(l, v.lols[0]), GrowFromCenter(v.shell()))
                                for l, v in zip(lols, vs)], lag_ratio=0.12), run_time=1.5)

        # "still sitting in membrane"
        self.at("still sitting")
        self.play(*[Indicate(v.body, color=TEAL, scale_factor=1.12) for v in vs], run_time=0.8)

        # about 50 nanometres, and what a vesicle is
        vlbl = VGroup(T("vesicle", 30, TEAL, weight=BOLD), T("about 50 nanometres", 22, GREY)).arrange(DOWN, buff=0.1)
        vlbl.move_to(P(4.6, -0.1))
        vptr = Line(P(3.2, 0.1), P(3.0, 0.4), color=TEAL, stroke_width=3)
        self.at("across")
        self.play(FadeIn(vlbl, shift=LEFT * 0.1), Create(vptr), run_time=0.6)
        self.at("small sac")
        self.play(Indicate(vs[4].body, color=TEXT, scale_factor=1.3), run_time=0.8)

        # the puzzle: rubbish, or a message
        rub = ghost_chip("rubbish disposal", 26).move_to(P(-4.6, 2.5))
        msg = ghost_chip("a message?", 26).move_to(P(4.6, 2.5))
        self.at("rubbish disposal")
        self.play(FadeIn(rub, shift=RIGHT * 0.15), run_time=0.5)
        self.at("a message")
        self.play(FadeIn(msg, shift=LEFT * 0.15), run_time=0.5)

        # where do they come from? an unknown inside the cell
        qb = q_box(S1_Q)
        path = darr(P(2.5, -1.95), P(2.5, 0.12), PURPLE, w=6)
        self.at("come from")
        self.play(FadeIn(qb, scale=0.8), Create(path[0]), FadeIn(path[1]), run_time=0.9)
        self.play(pop(qb[2], 1.4), run_time=0.5)
        # into the cell: the unknown becomes the next scene's compartment
        ring = Circle(radius=2.6, stroke_color=PURPLE, stroke_width=7, fill_color=BG, fill_opacity=1).move_to(P(0, -0.1))
        solid = RoundedRectangle(corner_radius=0.16, width=1.7, height=1.15, stroke_color=PURPLE, stroke_width=4,
                                 fill_color=BG, fill_opacity=1).move_to(S1_Q)
        self.remove(qb[1], qb[2]); self.add(solid, qb[2])
        self.outro(FadeOut(VGroup(mem, cell_lbl, rub, msg, vlbl, vptr, path, *[v.group() for v in vs])),
                   then=[ReplacementTransform(solid, ring), FadeOut(qb[0]), FadeOut(qb[2]),
                         Transform(tint, tint_rect(4.1))])


# ---------------------------------------------------------------------------------------------
M2_C = P(0, -0.1)
M2_R = 3.2


class S02Inward(Film):
    """the endosome membrane buds inward, away from the cytosol, and pinches off vesicles; receptors ride on them."""

    def construct(self):
        tint = tint_rect(4.1)
        m = Mvb(M2_C, M2_R, with_lols=True)
        self.add(tint, m.ring)

        endo = T("endosome", 32, PURPLE, weight=BOLD).move_to(P(-5.0, 2.1))
        e_ptr = Line(P(-3.85, 1.95), P(-2.85, 1.55), color=PURPLE, stroke_width=3)
        inside = T("inside the cell", 32, GREY).move_to(P(-4.9, -2.75))
        self.at("inside the cell")
        self.play(m.ring.animate(rate_func=there_and_back).scale(1.03), FadeIn(inside, shift=UP * 0.1), run_time=0.8)
        self.at("called an")
        self.play(FadeIn(endo, shift=RIGHT * 0.1), Create(e_ptr), run_time=0.6)

        # the first bud: inward, away from the cytosol
        buds = []
        for i, v in enumerate(m.ves):
            p = m.c + M2_R * dv(m.ANG[i])
            buds.append(Bud(p, m.ANG[i] + 180, v.c, v.r, L=1.2, w=0.38))
        b0 = buds[0]
        self.add(b0.holder)
        self.at("inward")
        self.play(b0.grow(run_time=1.0, rate_func=smooth))
        cyto = T("cytosol", 32, YELLOW, weight=BOLD).move_to(P(-5.2, -2.75))
        self.at("own fluid")
        self.play(ReplacementTransform(inside, cyto), tint.animate(rate_func=there_and_back).set_fill(YELLOW, 0.3), run_time=1.0)

        self.at("pinches off")
        self.play(b0.pinch(run_time=1.0))
        for b in buds[1:]:
            self.add(b.holder)
        self.at("small vesicles")
        self.play(LaggedStart(*[Succession(b.grow(run_time=0.5), b.pinch(run_time=0.5)) for b in buds[1:]],
                              lag_ratio=0.3), run_time=2.0)

        # receptors ride on the vesicles, their heads pointing out
        head = m.ves[2].lols[0][1].get_center()
        rec = T("receptor", 30, BLUE, weight=BOLD).move_to(P(5.0, -2.3))
        r_ptr = Line(P(3.85, -2.1), head + P(0.2, -0.15), color=BLUE, stroke_width=3)
        lol_anims = [GrowFromPoint(l, l[0].get_start()) for v in m.ves for l in v.lols]
        self.at("carry")
        self.play(LaggedStart(*lol_anims, lag_ratio=0.04), FadeIn(rec), Create(r_ptr), run_time=1.2)

        mvb = T("multivesicular\nbody", 30, PURPLE, weight=BOLD, line_spacing=0.9).move_to(P(4.85, 2.0))
        m_ptr = Line(P(3.5, 1.75), P(2.95, 1.25), color=PURPLE, stroke_width=3)
        self.at("packed with")
        self.play(ReplacementTransform(endo, mvb), ReplacementTransform(e_ptr, m_ptr),
                  m.ring.animate(rate_func=there_and_back).scale(1.03), run_time=0.9)
        # carry the compartment, small, to the left of the cell for scene 3
        tgt = S3_START
        self.remove(*[b.holder for b in buds])
        self.add(*[v.shell() for v in m.ves])
        grp = VGroup(m.ring, *[v.group() for v in m.ves])
        self.outro(FadeOut(VGroup(mvb, m_ptr, rec, r_ptr, cyto)),
                   then=[grp.animate.scale(K3, about_point=m.c).shift(tgt - m.c)])


R3 = 1.9
K3 = R3 / M2_R
S3_START = P(-2.1, -1.25)           # where the small compartment sits at the start of scene 3
S3_YM = 1.5                        # the cell surface
S3_LY = P(4.4, -1.5)               # the lysosome
S3_RLY = 1.4


def small_mvb():
    """the compartment of scene 2, scaled down and moved to its place at the start of scene 3."""
    m = Mvb(M2_C, M2_R, with_lols=True)
    grp = VGroup(m.ring, *[v.group() for v in m.ves])
    grp.scale(K3, about_point=m.c).shift(S3_START - m.c)
    return m, grp


def open_ring(c, R, a_deg, ring_w=7):
    """the compartment after it has fused with the cell surface: a ring open at the top."""
    arc = Arc(radius=R, start_angle=np.radians(90 + a_deg), angle=np.radians(360 - 2 * a_deg), arc_center=c,
              stroke_color=PURPLE, stroke_width=ring_w)
    arc.set_fill(BG, 1)
    arc.set_z_index(-1)
    return arc


def dimmer(mob, f, **kw):
    """scale every opacity in mob by f (animated); call again with 1/f to restore exactly."""
    subs = list(mob.family_members_with_points())
    orig = [(m.get_fill_opacity(), m.get_stroke_opacity()) for m in subs]

    def upd(_, a):
        k = 1 + (f - 1) * a
        for m, (fo, so) in zip(subs, orig):
            m.set_fill(opacity=min(1.0, fo * k))
            m.set_stroke(opacity=min(1.0, so * k))
    return UpdateFromAlphaFunc(mob, upd, **kw)


def check_mark(c, s=0.3, color=GREEN, w=8):
    c = np.array(c, float)
    return VMobject().set_points_as_corners([c + s * P(-0.9, 0.0), c + s * P(-0.3, -0.7), c + s * P(1.0, 0.9)]).set_stroke(color, w)


class S03Doors(Film):
    """one compartment, two doors: the lysosome (digested) or the cell surface (released intact)."""

    def construct(self):
        tint = tint_rect(4.1)
        m, grp = small_mvb()
        self.add(tint, grp)
        R = R3
        ym = S3_YM
        c0 = S3_START

        sort = T("sorting\nroom", 28, GREY, line_spacing=0.9).move_to(P(-5.2, -1.25))
        self.at("sorting room")
        self.play(FadeIn(sort, shift=UP * 0.1), m.ring.animate(rate_func=there_and_back).scale(1.04), run_time=0.8)

        # two doors: the lysosome on the right, the cell surface above
        lyso = Circle(radius=S3_RLY, stroke_color=RED, stroke_width=6, fill_color=BG, fill_opacity=1).move_to(S3_LY)
        lyso_t = Circle(radius=S3_RLY, stroke_width=0, fill_color=RED, fill_opacity=0.10).move_to(S3_LY)
        lyso_g = VGroup(lyso, lyso_t)
        memL = Line(P(-6.3, ym), P(c0[0], ym), color=GREY, stroke_width=16).set_cap_style(CapStyleType.ROUND)
        memR = Line(P(c0[0], ym), P(6.3, ym), color=GREY, stroke_width=16).set_cap_style(CapStyleType.ROUND)
        a_in = arr(P(c0[0] + R + 0.1, -1.1), S3_LY + P(-S3_RLY - 0.1, -0.15), RED, w=5)
        a_st = arr(c0 + P(0, R + 0.1), P(c0[0], ym - 0.12), GREEN, w=5)
        self.at("two doors")
        self.play(Transform(tint, tint_rect(ym)), FadeIn(lyso_g, shift=LEFT * 0.3), Create(memL), Create(memR),
                  run_time=1.0)
        inc = T("incinerator", 28, RED).move_to(P(1.7, -0.45))
        self.at("one to the")
        self.play(GrowArrow(a_in), FadeIn(inc, shift=UP * 0.1), run_time=0.7)
        street = T("street", 28, GREEN).move_to(P(-1.0, 0.95))
        self.at("and one to")
        self.play(GrowArrow(a_st), FadeIn(street, shift=RIGHT * 0.1), run_time=0.7)

        # door one: fuses with the lysosome; its vesicles are digested
        ly_lbl = T("lysosome", 30, RED, weight=BOLD).move_to(S3_LY + P(0, -S3_RLY - 0.38))
        vg = VGroup(*[v.group() for v in m.ves])
        touch = S3_LY - (S3_LY - c0) / np.linalg.norm(S3_LY - c0) * (R + S3_RLY + 0.04)
        self.at("fuses with")
        self.play(FadeOut(inc), FadeOut(street), FadeOut(a_st), FadeOut(a_in), FadeOut(sort),
                  grp.animate.shift(touch - c0), FadeIn(ly_lbl, shift=UP * 0.1), run_time=1.0)
        self.at("their cargo")
        self.play(FadeOut(m.ring), vg.animate.scale(0.6).move_to(S3_LY), lyso.animate(rate_func=there_and_back).scale(1.05), run_time=0.9)
        dig = T("digested", 30, RED, weight=BOLD).move_to(S3_LY + P(0, S3_RLY + 0.38))
        self.at("digested")
        self.play(*[v.body.animate.set_stroke(RED).set_fill(RED, 0.25) for v in m.ves],
                  *[l.animate.set_color(RED) for v in m.ves for l in v.lols], run_time=0.5)
        self.play(FadeOut(vg, scale=0.2), FadeIn(dig, shift=DOWN * 0.1), run_time=0.7)

        # door two: the same kind of compartment goes to the surface instead
        m2, grp2 = small_mvb()
        self.remove(grp)
        self.at("But the same")
        self.play(FadeOut(dig), FadeOut(ly_lbl), FadeOut(lyso_g), FadeIn(grp2), run_time=0.8)
        self.at("move to the")
        cy_f = ym - R * np.cos(np.radians(36))
        up_to = P(c0[0], ym - R - 0.1)
        self.play(grp2.animate.shift(up_to + P(0, -R) - c0 + P(0, R)), run_time=0.8)
        hw = R * np.sin(np.radians(36))
        arc = open_ring(P(c0[0], cy_f), R, 36)
        self.at("fuse with")
        self.play(grp2.animate.shift(P(0, cy_f - (ym - R - 0.1))),
                  FadeOut(m2.ring), FadeIn(arc),
                  memL.animate.put_start_and_end_on(P(-6.3, ym), P(c0[0] - hw, ym)),
                  memR.animate.put_start_and_end_on(P(c0[0] + hw, ym), P(6.3, ym)), run_time=0.9)
        pm = T("plasma membrane", 26, GREY).move_to(P(3.0, 1.1))
        self.at("plasma membrane")
        self.play(FadeIn(pm, shift=UP * 0.1), run_time=0.5)

        # its vesicles are then outside the cell, intact
        xs = [c0[0] + 1.25 * k for k in (-2, -1, 0, 1, 2)]
        ys = [2.5, 2.62, 2.5, 2.62, 2.5]
        anims = []
        for i, (v, x, y) in enumerate(zip(m2.ves, xs, ys)):
            c_now = v.body.get_center()
            gate = P(c0[0] + (x - c0[0]) * 0.3, ym - 0.05)
            tgt = P(x, y)
            anims.append(Succession(v.group().animate(run_time=0.4).shift(gate - c_now),
                                    v.group().animate(run_time=0.6).shift(tgt - c_now).scale(1.4, about_point=tgt),
                                    Rotate(VGroup(*v.lols), angle=np.radians(65 - Mvb.LOL[i][0]), about_point=tgt, run_time=0.4)))
        self.at("Its vesicles", nth=1)
        self.play(LaggedStart(*anims, lag_ratio=0.1), run_time=1.15)
        out_lbl = T("outside the cell", 26, GREY).move_to(P(4.9, 3.0))
        self.at("outside the cell")
        self.play(FadeIn(out_lbl, shift=LEFT * 0.1), run_time=0.5)
        self.at("intact")
        self.play(*[Indicate(v.body, color=TEAL, scale_factor=1.25) for v in m2.ves], run_time=0.8)
        exo = T("exosomes", 34, TEAL, weight=BOLD).move_to(P(2.3, 2.55))
        self.at("exosomes")
        self.play(FadeIn(exo, shift=LEFT * 0.1), run_time=0.5)

        # the word names an origin
        orig = T("origin", 32, PURPLE, weight=BOLD).move_to(P(-5.55, 0.2))
        o_ptr = darr(P(-4.85, 0.2), P(-4.1, 0.2), PURPLE, w=4)
        self.at("names an origin")
        self.play(FadeIn(orig, shift=RIGHT * 0.1), Create(o_ptr[0]), FadeIn(o_ptr[1]), run_time=0.8)
        mvb_l = T("multivesicular body", 28, PURPLE, weight=BOLD).move_to(P(c0[0], cy_f - R - 0.4))
        self.at("formed inside")
        self.play(arc.animate(rate_func=there_and_back).set_stroke(width=13), run_time=0.8)
        self.at("body")
        self.play(FadeIn(mvb_l, shift=UP * 0.1), run_time=0.6)
        self.outro(FadeOut(VGroup(arc, *[v.group() for v in m2.ves], memL, memR, pm, out_lbl, exo, orig, o_ptr,
                                  mvb_l)),
                   then=[Transform(tint, tint_rect(-1.5))], then_time=0.4)


class S04Geometry(Film):
    """a bud grows into the compartment, away from the cytosol: the receptors on its outer face point out."""

    def construct(self):
        Y0 = -1.5
        tint = tint_rect(Y0)
        self.add(tint)
        mem = Line(P(-6.3, Y0), P(6.3, Y0), color=PURPLE, stroke_width=12).set_cap_style(CapStyleType.ROUND)
        cyto = T("cytosol", 32, YELLOW, weight=BOLD).move_to(P(-2.0, -2.6))
        lumen = T("inside the compartment", 26, GREY).move_to(P(-3.9, -1.05))
        VC = P(0, 0.7)
        bud = Bud(P(0, Y0), 90, VC, 1.0, L=1.6, w=0.6)
        # receptors stand in the flat membrane, heads into the compartment (the side away from the cytosol)
        STALK, HEAD, LW = 0.9, 0.16, 6.5
        specs = [(160, P(-0.45, Y0 + 0.06), STALK, HEAD, LW), (90, P(0.0, Y0 + 0.06), STALK, HEAD, LW),
                 (20, P(0.45, Y0 + 0.06), STALK, HEAD, LW)]
        riders = [lolli(sp[1], UP, STALK, HEAD, LW) for sp in specs]
        for r in riders:
            r.set_z_index(2)
        self.add(bud.holder)
        self.at("direction of")
        self.play(Create(mem), FadeIn(cyto), FadeIn(lumen),
                  LaggedStart(*[GrowFromPoint(r, r[0].get_start()) for r in riders], lag_ratio=0.15), run_time=0.9)

        # the bud grows up into the compartment, carrying the receptors; it is open to the cytosol below
        self.at("budding")
        self.play(bud.anim_with(riders, specs, 0.0, 0.5, run_time=3.0, rate_func=smooth))
        self.at("away from")
        self.play(bud.holder[2].animate(rate_func=there_and_back).set_fill(YELLOW, 0.5),
                  pop(cyto, 1.15), run_time=1.1)

        # it pinches off: the inside is now a sample of cytosol, and the receptors face out
        self.at("inside of")
        self.play(bud.anim_with(riders, specs, 0.5, 1.0, run_time=1.6))
        v = Ves(VC, 1.0, [])
        v.lols = riders
        self.remove(bud.holder)
        self.add(v.shell())
        cin = T("cytosol", 28, YELLOW).move_to(VC)
        self.at("sample of")
        self.play(FadeIn(cin, scale=0.8), run_time=0.6)

        # the outer face carries the receptors, heads out
        outer = T("outer face", 30, TEAL, weight=BOLD).move_to(P(4.5, 2.45))
        optr = Line(P(3.4, 2.35), P(0.78, 1.47), color=TEAL, stroke_width=3)
        self.at("outer face")
        self.play(FadeIn(outer, shift=LEFT * 0.1), Create(optr),
                  v.body.animate(rate_func=there_and_back).set_stroke(width=9), run_time=1.0)
        was = T("was the outside\nof the cell", 26, GREY, line_spacing=0.9).move_to(P(4.6, 1.6))
        self.at("outside of the cell")
        self.play(FadeIn(was, shift=LEFT * 0.1), run_time=0.6)

        rec_lbl = T("receptor", 28, BLUE, weight=BOLD).move_to(P(4.6, 0.15))
        rec_ptr = Line(P(3.55, 0.3), riders[2][1].get_center() + P(0.2, -0.12), color=BLUE, stroke_width=3)
        self.at("a receptor")
        self.play(FadeOut(outer), FadeOut(optr), FadeOut(was), *[pop(l[1], 1.8) for l in riders],
                  FadeIn(rec_lbl, shift=LEFT * 0.1), Create(rec_ptr), run_time=0.9)
        out_arrows = VGroup()
        for l in riders:
            hc = l[1].get_center()
            d = (hc - VC) / np.linalg.norm(hc - VC)
            out_arrows.add(arr(hc + 0.3 * d, hc + 0.8 * d, BLUE, w=5, tip=0.2))
        faces = T("faces outward", 28, BLUE, weight=BOLD).move_to(P(4.6, 0.15))
        self.at("still faces outward")
        self.play(LaggedStart(*[GrowArrow(x) for x in out_arrows], lag_ratio=0.1), ReplacementTransform(rec_lbl, faces),
                  FadeOut(rec_ptr), run_time=1.0)

        # now beside the plasma membrane
        memR = Line(P(0.45, Y0), P(6.3, Y0), color=GREY, stroke_width=12).set_cap_style(CapStyleType.ROUND)
        pl = [lolli(P(x, Y0 + 0.06), UP, 0.9, 0.16, 6.5) for x in (1.7, 3.4, 5.1)]
        pl_arr = [arr(P(x, Y0 + 0.06 + 0.9 + 0.3), P(x, Y0 + 0.06 + 0.9 + 0.85), BLUE, w=5, tip=0.2) for x in (1.7, 3.4, 5.1)]
        pm = T("plasma membrane", 26, GREY).move_to(P(3.4, -2.2))
        outside = T("outside the cell", 26, GREY).move_to(P(4.6, 2.95))
        left = VGroup(v.group(), cin, out_arrows)
        self.at("as it did")
        self.play(FadeOut(faces), left.animate.shift(LEFT * 3.3),
                  mem.animate.put_start_and_end_on(P(-6.3, Y0), P(-0.45, Y0)), run_time=1.1)
        self.at("plasma membrane")
        self.play(Create(memR), LaggedStart(*[GrowFromPoint(l, l[0].get_start()) for l in pl], lag_ratio=0.15),
                  FadeIn(pm), FadeIn(outside), run_time=1.0)
        self.play(LaggedStart(*[GrowArrow(x) for x in pl_arr], lag_ratio=0.15), run_time=0.7)
        self.outro(FadeOut(VGroup(mem, memR, cyto, lumen, pm, outside, *pl, *pl_arr, left)))


class S05Lookalike(Film):
    """exosome and microvesicle: different origins, identical on the outside, so in the medium you cannot tell."""

    def construct(self):
        ym = -1.5
        cx, R, a = -2.8, 1.1, 38
        cy = ym - R * np.cos(np.radians(a))
        hw = R * np.sin(np.radians(a))
        tint = tint_rect(ym)
        arc = open_ring(P(cx, cy), R, a, ring_w=6)
        memL = Line(P(-6.3, ym), P(cx - hw, ym), color=GREY, stroke_width=16).set_cap_style(CapStyleType.ROUND)
        memR = Line(P(cx + hw, ym), P(6.3, ym), color=GREY, stroke_width=16).set_cap_style(CapStyleType.ROUND)
        inner = [Ves(P(cx + dx, cy + dy), 0.2) for dx, dy in [(-0.45, -0.25), (0.1, -0.6), (0.5, -0.1)]]
        ANG, MARK = [30, 90, 150], [210, 250, 330]
        exo = Ves(P(cx, 0.75), 0.7, ANG, marks=MARK)
        self.add(tint, arc, memL, memR, *[v.shell() for v in inner], exo.shell(), *exo.lols)

        # the microvesicle buds straight outward from the plasma membrane
        mx = 2.8
        bud = Bud(P(mx, ym), 90, P(mx, 0.75), 0.7, L=1.3, w=0.45)
        mv = Ves(P(mx, 0.75), 0.7, ANG, marks=MARK)
        self.add(bud.holder)
        self.at("bud straight")
        self.play(bud.grow(run_time=1.0))
        self.at("called")
        self.play(bud.pinch(run_time=0.9))
        self.remove(bud.holder)
        self.add(mv.shell())
        mv_name = T("microvesicle", 32, TEAL, weight=BOLD).move_to(P(mx, 3.15))
        self.play(LaggedStart(*[GrowFromPoint(l, l[0].get_start()) for l in mv.lols], lag_ratio=0.1),
                  FadeIn(mv_name, shift=DOWN * 0.1), run_time=0.8)

        # different by origin
        ex_name = T("exosome", 32, TEAL, weight=BOLD).move_to(P(cx, 3.15))
        ex_tag = T("formed in a multivesicular body", 22, PURPLE).move_to(P(cx, 2.7))
        mv_tag = T("budded from the cell surface", 22, GREY).move_to(P(mx, 2.7))
        self.at("different kind")
        self.play(FadeIn(ex_name, shift=DOWN * 0.1), FadeIn(ex_tag), FadeIn(mv_tag), run_time=0.9)

        # same orientation, overlapping size
        self.at("same orientation")
        self.play(*[pop(l[1], 1.8) for l in exo.lols + mv.lols], run_time=0.9)
        sz = [DoubleArrow(P(x - 0.7, -0.2), P(x + 0.7, -0.2), buff=0, color=GREY, stroke_width=4, tip_length=0.14)
              for x in (cx, mx)]
        sz_lbl = T("sizes overlap", 24, GREY).move_to(P((cx + mx) / 2, -0.2))
        self.at("overlap in size")
        self.play(*[GrowFromCenter(d) for d in sz], FadeIn(sz_lbl), run_time=0.8)

        # the usual markers sit on both
        tet = T("tetraspanin", 28, ORANGE, weight=BOLD).move_to(P((cx + mx) / 2, 1.35))
        p1 = Line(P(-0.8, 1.2), exo.c + 0.7 * dv(330) + P(0.1, 0.1), color=ORANGE, stroke_width=3)
        p2 = Line(P(0.8, 1.2), mv.c + 0.7 * dv(210) + P(-0.1, 0.1), color=ORANGE, stroke_width=3)
        self.at("usual markers")
        self.play(FadeOut(sz_lbl), *[FadeOut(d) for d in sz], *[GrowFromCenter(d) for d in exo.marks + mv.marks],
                  FadeIn(tet, shift=DOWN * 0.1), Create(p1), Create(p2), run_time=1.0)
        self.at("both kinds")
        self.play(*[pop(d, 1.8) for d in exo.marks + mv.marks], run_time=0.7)

        # in the medium nothing tells them apart: the tags go and the two swap places
        med = T("culture medium", 28, GREY).move_to(P(0, -1.0))
        self.at("culture medium")
        self.play(FadeOut(ex_name), FadeOut(mv_name), FadeOut(ex_tag), FadeOut(mv_tag), FadeOut(tet), FadeOut(p1), FadeOut(p2),
                  FadeIn(med), exo.group().animate.shift(P(1.0, 0)), mv.group().animate.shift(P(-1.0, 0)),
                  run_time=1.2)
        self.at("no agreed test")
        self.play(exo.group().animate(path_arc=-PI / 2).shift(P(3.6, 0)),
                  mv.group().animate(path_arc=-PI / 2).shift(P(-3.6, 0)), run_time=1.3)
        qA = T("?", 60, TEXT, weight=BOLD).move_to(exo.body.get_center() + P(0, 2.0))
        qB = T("?", 60, TEXT, weight=BOLD).move_to(mv.body.get_center() + P(0, 2.0))
        self.at("tells them")
        self.play(GrowFromCenter(qA), GrowFromCenter(qB), run_time=0.7)
        self.outro(FadeOut(VGroup(tint, arc, memL, memR, *[v.shell() for v in inner], exo.group(), mv.group(), med, qA, qB)))


class S06Rule(Film):
    """the rule: say exosome only when the origin is shown; otherwise say extracellular vesicle."""

    def construct(self):
        YB, YA = 1.0, -2.0
        mB = Mvb(P(-4.0, YB), 1.5, ring_w=6, with_lols=False)
        mB_g = VGroup(mB.ring, *[v.group() for v in mB.ves])
        vB = Ves(P(1.1, YB), 0.72, [30, 90, 150], marks=[210, 330])
        aB = arr(P(-2.4, YB), P(0.3, YB), PURPLE, w=6)
        chipB = bchip("exosome", TEAL, 32).move_to(P(1.1, 3.05))
        self.at("exosome")
        self.play(FadeIn(vB.group(), scale=0.8), FadeIn(chipB, shift=DOWN * 0.1), run_time=0.7)
        self.at("where it formed")
        self.play(FadeIn(mB_g, scale=0.9), GrowArrow(aB), run_time=0.8)
        tests = [ghost_chip(t, 28).move_to(P(x, -1.2)) for t, x in (("size", -2.6), ("markers", 0.0), ("orientation", 2.9))]
        # each test gets a "?" badge: it is not a reliable way to show the origin
        marks = []
        for c in tests:
            ring_ = Circle(radius=0.2, stroke_color=GREY, stroke_width=3, fill_color=BG, fill_opacity=1)
            q_ = T("?", 26, TEXT, weight=BOLD).move_to(ring_)
            marks.append(VGroup(ring_, q_).move_to(c.get_corner(UR) + P(0.05, 0.05)))
        for nm, c, k in zip(("size", "markers", "orientation"), tests, marks):
            self.at(nm)
            self.play(FadeIn(c, shift=UP * 0.1), run_time=0.35)
            self.play(FadeIn(k, scale=0.5), run_time=0.35)
        nr = T("not reliable", 26, GREY).move_to(P(0.15, -2.0))
        self.at("reliably")
        self.play(FadeIn(nr, shift=UP * 0.1), run_time=0.5)

        # a separate job: the message
        tgt_box = RoundedRectangle(corner_radius=0.2, width=1.9, height=1.6, stroke_color=GREY, stroke_width=3).move_to(P(5.3, YB))
        tgt_lbl = T("target cell", 24, GREY).move_to(tgt_box)
        msg = darr(P(2.5, YB), P(4.2, YB), GOLD, w=5)
        msg_l = T("message?", 26, GOLD, weight=BOLD).move_to(P(3.2, YB - 0.45))
        self.at("carries a message")
        self.play(FadeOut(VGroup(*tests, *marks, nr)), FadeIn(tgt_box), FadeIn(tgt_lbl), Create(msg[0]), FadeIn(msg[1]),
                  FadeIn(msg_l), run_time=0.9)
        self.at("separate job")
        self.play(dimmer(VGroup(mB_g, aB), 0.3, run_time=0.6))
        ctl = T("needs controls", 24, GREY).move_to(P(3.2, YB - 1.1))
        self.at("needs controls")
        self.play(FadeIn(ctl, shift=UP * 0.1), run_time=0.5)

        # to call it an exosome: show the origin
        shown = T("origin shown", 26, GREEN, weight=BOLD).move_to(P(-1.05, YB - 0.55))
        ck = check_mark(P(-1.05, YB + 0.55))
        self.at("To call that")
        self.play(FadeOut(VGroup(tgt_box, tgt_lbl, msg, msg_l, ctl)), dimmer(VGroup(mB_g, aB), 1 / 0.3), run_time=0.7)
        self.at("must also show")
        self.play(aB.animate(rate_func=there_and_back).set_stroke(width=11), mB.ring.animate(rate_func=there_and_back).set_stroke(width=11),
                  run_time=0.8)
        mvb_l = T("multivesicular body", 26, PURPLE, weight=BOLD).move_to(P(-4.0, YB - 2.05))
        self.at("came from")
        self.play(FadeIn(shown, shift=UP * 0.1), Create(ck), FadeIn(mvb_l, shift=UP * 0.1), run_time=0.7)

        # the default: extracellular vesicle
        qbox = q_box(P(-4.0, YA))
        aA = darr(P(-3.0, YA), P(0.3, YA), GREY, w=5)
        vA = Ves(P(1.1, YA), 0.72, [30, 90, 150], marks=[210, 330])
        nos = T("origin not shown", 26, GREY).move_to(P(-1.35, YA - 0.55))
        chipA = bchip("extracellular vesicle", TEAL, 28).move_to(P(4.5, YA))
        self.at("urges authors")
        self.play(FadeIn(qbox), FadeIn(vA.group(), scale=0.8), Create(aA[0]), FadeIn(aA[1]), FadeIn(nos), run_time=0.9)
        self.at("extracellular vesicle")
        self.play(FadeIn(chipA, shift=LEFT * 0.1), run_time=0.6)
        self.at("unless they can show")
        self.play(aB.animate(rate_func=there_and_back).set_stroke(width=11), pop(ck, 1.4), run_time=0.8)

        # the rule
        self.at("keep this rule")
        self.play(dimmer(VGroup(qbox, aA, vA.group(), nos, chipA), 0.45, run_time=0.7))
        self.at("say exosome")
        self.play(*glow(chipB[1], chipB[2], s=1.12, color=TEAL), run_time=0.8)
        self.at("show where it formed")
        self.play(aB.animate(rate_func=there_and_back).set_stroke(width=12), mB.ring.animate(rate_func=there_and_back).set_stroke(width=12),
                  pop(ck, 1.5), run_time=0.9)
        self.finish()


class S07End(EndCard):
    LINE = "Say exosome only when you can show where it formed."
