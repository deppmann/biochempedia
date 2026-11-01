"""Exosomes and extracellular vesicles: an exosome is named by its origin  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = surface proteins (MHC and receptors): a stalk with a round head, head = the part that sat outside the cell
  TEAL   = a small vesicle (outline): internal vesicle, exosome, microvesicle, "vesicle" labels
  YELLOW = cytosol, the cell's own fluid (the tint of the cell interior and the fill inside every vesicle)
  PURPLE = the multivesicular body / endosome, and the "formed inside it" origin of an exosome
  RED    = the lysosome and digestion (the incinerator door)
  GREEN  = the street door: released from the cell, intact
  ORANGE = peptide carried by MHC (or existing tetraspanin helper markers)
  GOLD   = the message (a signal carried to another cell)
  GREY   = membranes (plasma membrane), labels, what is unknown or not shown (dashed)

No molecular structures: a receptor is a stalk with a round head, a vesicle is a circle, the
compartment is a ring, membranes are lines, the cytosol is a tint. Nothing is drawn atom by atom.

Layouts follow the new narration: recognition, inward budding, two exits, geometry,
three target-cell routes, and separation controls.
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


# Original helper entry points retained for the shared drawing vocabulary.
M2_C = P(0, -0.1)
M2_R = 3.2
R3 = 1.9
K3 = R3 / M2_R
S3_START = P(-2.1, -1.25)

def q_box(c):
    box = RoundedRectangle(corner_radius=0.16, width=1.7, height=1.15).move_to(c)
    back = box.copy().set_stroke(width=0).set_fill(BG, 1)
    edge = DashedVMobject(box, num_dashes=30).set_color(PURPLE)
    q = T("?", 44, TEXT, weight=BOLD).move_to(c)
    return VGroup(back, edge, q)

def small_mvb():
    """the compartment of scene 2, scaled down and moved to its place at the start of scene 3."""
    m = Mvb(M2_C, M2_R, with_lols=True)
    grp = VGroup(m.ring, *[v.group() for v in m.ves])
    grp.scale(K3, about_point=m.c).shift(S3_START - m.c)
    return m, grp

# The original title and end cards are retained verbatim.
class S00Title(TitleCard):
    LESSON = "Exosomes and Extracellular Vesicles"
    TITLE = "An exosome is named by its origin"


def mhc(base, direction=UP, length=0.4):
    """Schematic display protein with an orange peptide badge at its head."""
    protein = lolli(base, direction, length, 0.10, 4)
    peptide = RoundedRectangle(width=0.24, height=0.10, corner_radius=0.04,
                               stroke_width=0, fill_color=ORANGE, fill_opacity=1)
    peptide.move_to(protein[1]).rotate(np.arctan2(direction[1], direction[0]) - PI / 2)
    return VGroup(protein, peptide)


def display_ves(c, r=0.45, angle=0):
    v = Ves(c, r)
    v.lols = [mhc(c + r * dv(angle), dv(angle), 0.35)]
    return v


class DisplayBud(Bud):
    def rider(self, a, *spec):
        receptor = super().rider(a, *spec)
        return mhc(receptor[0].get_start(), receptor[0].get_unit_vector(), receptor[0].get_length())


class S01Signal(SpokenScene):
    def construct(self):
        cell = Circle(radius=1.25, color=GREY, fill_color=YELLOW, fill_opacity=CY).move_to(P(-4.7, 0))
        label = T("donor cell", 28, GREY).move_to(P(-4.7, -1.8))
        ves = [display_ves(P(-3.2, y), 0.38) for y in (0.7, -0.7)]
        self.at("Cells release")
        self.play(Create(cell), FadeIn(label), run_time=0.6)
        self.at("extracellular vesicles")
        self.play(*[FadeIn(v.shell(), scale=0.3) for v in ves], run_time=0.7)
        ev = T("extracellular vesicles", 28, TEAL).move_to(P(-0.8, 2.7))
        self.play(FadeIn(ev), run_time=0.5)
        self.at("carry a signal")
        self.play(*[v.shell().animate.shift(RIGHT * 2.0) for v in ves], run_time=1.3)
        self.at("immune system")
        self.play(Transform(label, T("B cell", 28, GREY).move_to(label)), run_time=0.5)
        self.at("that carry")
        # Rebuild displays at the shells' new positions.
        for v in ves:
            v.lols = [mhc(v.body.get_center() + RIGHT * v.r, RIGHT, 0.35)]
        prot = T("MHC class II", 28, BLUE).move_to(P(-0.8, 1.9))
        self.play(*[FadeIn(v.lols[0][0]) for v in ves], FadeIn(prot), run_time=0.6)
        self.at("holding a peptide")
        pep = T("peptide", 26, ORANGE).move_to(P(-0.8, -2.0))
        self.play(FadeIn(pep), *[FadeIn(v.lols[0][1]) for v in ves], run_time=0.6)
        targets = [Circle(radius=0.95, color=GREY, fill_color=GREY, fill_opacity=0.07).move_to(P(4.0, y)) for y in (1.4, -1.4)]
        names = [T("T cell", 26, GREY).move_to(P(5.65, y)) for y in (1.4, -1.4)]
        # A cup fits the top peptide; a triangular head differs on the lower cell.
        cup = VMobject().set_points_as_corners([P(2.7,1.62),P(2.7,1.18),P(3.05,1.18),P(3.05,1.62)]).set_stroke(BLUE,5)
        other = Triangle(color=GREY, fill_opacity=0.15).scale(0.22).move_to(P(2.85,-1.4))
        self.at("switch on T cells")
        self.play(FadeOut(ev), FadeOut(prot), FadeOut(pep), *[Create(t) for t in targets],
                  *[FadeIn(t) for t in names], Create(cup), FadeIn(other), run_time=0.7)
        self.at("whose receptor")
        self.play(*[v.group().animate.move_to(P(2.05, y)) for v,y in zip(ves,(1.4,-1.4))], run_time=0.9)
        self.at("recognizes that peptide")
        signal = arr(P(3.15,1.4),P(4.45,1.4),GOLD)
        self.play(targets[0].animate.set_stroke(GOLD,7).set_fill(GOLD,0.20), GrowArrow(signal), run_time=0.6)
        self.at("Nothing has to get inside")
        none = T("nothing enters the cell", 30, GOLD).move_to(P(0,-3.1))
        self.play(FadeIn(none), run_time=0.6)
        self.at("A scrap of membrane")
        self.play(*[Indicate(v.body,color=TEAL) for v in ves], run_time=0.8)
        self.finish()


class S02Inward(SpokenScene):
    def construct(self):
        tint = Rectangle(width=12.8,height=6.5,stroke_width=0,fill_color=YELLOW,fill_opacity=CY)
        m = Mvb(P(-0.5,0),2.45,with_lols=False)
        # Three large buds keep the compartment legible.
        centers = [P(-1.5,0.8),P(0.55,0.7),P(-0.4,-1.1)]
        ves = [display_ves(c,0.46,90) for c in centers]
        cyto = T("cytosol",30,YELLOW).move_to(P(-5.1,-2.7))
        endo = T("endosome",30,PURPLE).move_to(P(4.5,1.5))
        self.at("Where do these vesicles")
        self.play(FadeIn(tint),Create(m.ring),run_time=0.7)
        self.at("inside the cell")
        self.play(FadeIn(cyto),run_time=0.5)
        self.at("called an endosome")
        self.play(FadeIn(endo),run_time=0.5)
        buds=[]
        for a,v in zip((145,35,270),ves):
            b=Bud(m.c+m.R*dv(a),a+180,v.c,v.r,L=1.1,w=0.34)
            buds.append(b)
        self.at("buds inward")
        self.add(buds[0].holder)
        self.play(buds[0].grow(run_time=1.0))
        self.at("away from the cytosol")
        self.play(Indicate(cyto,color=YELLOW),run_time=0.7)
        self.at("pinches off small vesicles")
        self.play(buds[0].pinch(run_time=0.7))
        self.remove(buds[0].holder); self.add(ves[0].shell())
        for b in buds[1:]: self.add(b.holder)
        self.play(*[Succession(b.grow(run_time=0.6),b.pinch(run_time=0.6)) for b in buds[1:]],run_time=1.2)
        for b in buds[1:]: self.remove(b.holder)
        self.add(*[v.shell() for v in ves[1:]])
        self.at("carry receptors")
        self.play(*[FadeIn(v.lols[0][0]) for v in ves],run_time=0.5)
        self.at("multivesicular body")
        self.play(Transform(endo,T("multivesicular\nbody",28,PURPLE).move_to(P(4.5,1.5))),run_time=0.6)
        self.at("In B cells")
        bl=T("B cell",28,GREY).move_to(P(-5.1,2.7))
        self.play(FadeIn(bl),run_time=0.5)
        self.at("loaded with peptide")
        ml=T("MHC II + peptide",26,BLUE).move_to(P(4.5,-0.8))
        self.play(*[FadeIn(v.lols[0][1]) for v in ves],FadeIn(ml),run_time=0.6)
        self.finish()


class S03Doors(SpokenScene):
    def construct(self):
        m=Mvb(P(-2.8,-0.8),1.55,with_lols=False); group=m.group()
        mem=membrane_line(1.5)
        ly=Circle(radius=1.05,color=RED,fill_color=RED,fill_opacity=0.1).move_to(P(4,-1.0))
        sort=T("sorting room",28,PURPLE).move_to(P(-3,-2.9))
        self.at("Picture this compartment")
        self.play(FadeIn(group),FadeIn(sort),run_time=0.6)
        self.at("two doors")
        self.play(Create(mem),Create(ly),run_time=0.6)
        inc=T("incinerator",28,RED).move_to(P(4,-2.5))
        street=T("street",28,GREEN).move_to(P(-3,2.5))
        route = arr(P(-0.9,-0.8),P(2.7,-1),RED)
        self.at("incinerator")
        self.play(FadeIn(inc),GrowArrow(route),run_time=0.5)
        self.at("street")
        self.play(FadeIn(street),run_time=0.5)
        self.at("fuses with a lysosome")
        self.play(FadeOut(sort),FadeOut(route),Transform(inc,T("lysosome",28,RED).move_to(inc)),group.animate.scale(0.5).move_to(ly),run_time=0.8)
        self.at("are digested")
        self.play(group.animate.set_color(RED),run_time=0.4)
        self.play(FadeOut(group,scale=0.1),run_time=0.5)
        fresh=Mvb(P(-2.8,-0.8),1.55,with_lols=False); fg=fresh.group()
        self.at("If it moves")
        self.play(FadeOut(ly),FadeOut(inc),FadeIn(fg),run_time=0.6)
        self.at("cell surface")
        self.play(fg.animate.shift(UP*0.65),run_time=0.7)
        self.at("fuses with the plasma membrane")
        arc=open_ring(P(-2.8,0.25),1.55,36)
        gap=1.55*np.sin(np.radians(36))
        split=VGroup(membrane_line(1.5,-6.3,-2.8-gap),membrane_line(1.5,-2.8+gap,6.3))
        self.play(FadeOut(fresh.ring),FadeIn(arc),ReplacementTransform(mem,split),FadeOut(street),run_time=0.7)
        self.at("released intact")
        self.play(*[v.group().animate.move_to(P(-2.8+(i-2)*0.15,1.4)) for i,v in enumerate(fresh.ves)],run_time=0.45)
        self.play(*[v.group().animate.move_to(P(-5+i*1.05,2.55)) for i,v in enumerate(fresh.ves)],run_time=0.55)
        self.at("are exosomes")
        ex=T("exosomes",32,TEAL).move_to(P(3.1,2.55))
        self.play(FadeIn(ex),run_time=0.5)
        self.at("young red blood cells")
        redcell=Ellipse(width=2.1,height=1.3,color=GREY,fill_color=RED,fill_opacity=0.16).move_to(P(3.6,-1.2))
        rlabel=T("young red blood cell",24,GREY).move_to(P(3.6,-2.45))
        self.play(FadeIn(redcell),FadeIn(rlabel),run_time=0.6)
        rec=lolli(P(3.6,-0.55),UP,0.4)
        self.at("throwing out transferrin receptors")
        rv=Ves(P(3.6,0.25),0.28,[90])
        self.play(FadeIn(rec),run_time=0.3)
        self.play(ReplacementTransform(rec,rv.lols[0]),FadeIn(rv.shell()),run_time=0.7)
        self.finish()


class S04Geometry(SpokenScene):
    def construct(self):
        y=-1.5; center=P(-2.7,0.55)
        mem=membrane_line(y,-6.3,-0.25,color=PURPLE)
        tint=tint_rect(y)
        cyto=T("cytosol",30,YELLOW).move_to(P(-3,-2.65))
        lumen=T("compartment interior",24,PURPLE).move_to(P(-3.5,2.9))
        bud=DisplayBud(P(-2.7,y),90,center,0.85,L=1.6,w=0.55)
        specs=[(150,P(-3.05,y),0.5,0.1,4),(30,P(-2.35,y),0.5,0.1,4)]
        riders=[mhc(s[1],UP,0.5) for s in specs]
        self.at("direction of budding")
        self.play(Create(mem),FadeIn(tint),FadeIn(cyto),FadeIn(lumen),*[FadeIn(r) for r in riders],run_time=0.7)
        self.add(bud.holder)
        self.at("bud forms away")
        self.play(bud.anim_with(riders,specs,0,0.5,run_time=1.3))
        self.at("inside of an exosome")
        self.play(bud.anim_with(riders,specs,0.5,1,run_time=1.0))
        self.remove(bud.holder)
        v=Ves(center,0.85);v.lols=riders;self.add(v.shell())
        self.at("sample of cytosol")
        inside=T("cytosol",24,YELLOW).move_to(center)
        self.play(FadeIn(inside),run_time=0.5)
        self.at("outer face")
        outer=T("outer face",26,TEAL).move_to(P(0.7,1.6))
        ptr=Line(P(-0.4,1.6),P(-1.9,0.85),color=TEAL)
        self.play(FadeIn(outer),Create(ptr),run_time=0.5)
        self.at("outside of the cell")
        outside=T("outside the cell",26,GREY).move_to(P(3.8,2.9))
        self.play(FadeIn(outside),run_time=0.5)
        self.at("an MHC molecule")
        name=T("MHC + peptide",26,BLUE).move_to(P(-3.0,2.15))
        self.play(FadeIn(name),run_time=0.5)
        self.at("still points outward")
        arrows=[arr(center+1.45*dv(a),center+1.95*dv(a),GOLD) for a in (150,30)]
        self.play(FadeOut(outer),FadeOut(ptr),*[GrowArrow(a) for a in arrows],run_time=0.6)
        self.at("plasma membrane")
        pm=membrane_line(y,0.4,6.3)
        proteins=[mhc(P(x,y),UP,0.75) for x in (2.3,4.4)]
        pl=T("plasma membrane",24,GREY).move_to(P(3.6,-2.1))
        pa=[arr(P(x,-0.3),P(x,0.4),GOLD) for x in (2.3,4.4)]
        self.play(Create(pm),*[FadeIn(p) for p in proteins],FadeIn(pl),*[GrowArrow(a) for a in pa],run_time=0.7)
        self.at("show a ligand")
        self.play(*[Indicate(r[1],color=ORANGE) for r in riders+proteins],run_time=0.7)
        self.finish()


class S05ThreeWays(SpokenScene):
    def construct(self):
        xs=(-4.4,0,4.4)
        headings=[T(t,28,TEAL).move_to(P(x,2.9)) for x,t in zip(xs,("Surface signal","Fusion","Uptake"))]
        membranes=[Line(P(x-1.7,0),P(x+1.7,0),color=GREY,stroke_width=10) for x in xs]
        ves=[display_ves(P(x,1.1),0.42,270) for x in xs]
        self.at("A vesicle could act")
        self.play(*[FadeIn(h) for h in headings],*[Create(m) for m in membranes],*[FadeIn(v.group()) for v in ves],run_time=0.8)
        receptor=VMobject().set_points_as_corners([P(-4.65,0.6),P(-4.65,0.25),P(-4.15,0.25),P(-4.15,0.6)]).set_stroke(BLUE,5)
        self.at("ligand on its surface")
        self.play(Create(receptor),run_time=0.4)
        self.at("bind a receptor")
        self.play(ves[0].group().animate.shift(DOWN*0.2),run_time=0.5)
        signal=arr(P(-4.4,-0.25),P(-4.4,-1.3),GOLD)
        self.at("nothing has to get in")
        self.play(GrowArrow(signal),FadeIn(T("signal",26,GOLD).move_to(P(-4.4,-1.8))),run_time=0.5)
        self.at("can fuse")
        self.play(ves[1].group().animate.move_to(P(0,0)),run_time=0.6)
        gap=VGroup(Line(P(-1.7,0),P(-0.5,0),color=GREY,stroke_width=10),Line(P(0.5,0),P(1.7,0),color=GREY,stroke_width=10))
        cargo=VGroup(*[Dot(P(dx,0),radius=0.09,color=YELLOW) for dx in (-0.2,0,0.2)])
        self.at("release its contents")
        self.play(FadeOut(ves[1].group()),ReplacementTransform(membranes[1],gap),FadeIn(cargo),run_time=0.4)
        self.play(cargo.animate.shift(DOWN*1.3),FadeIn(T("cytosol",26,YELLOW).move_to(P(0,-2.2))),run_time=0.6)
        self.at("target can swallow it")
        endo=Circle(radius=0.72,color=PURPLE).move_to(P(4.4,-1.05))
        self.play(ves[2].group().animate.move_to(P(4.4,-1.05)),Create(endo),run_time=0.8)
        self.at("Swallowing alone")
        question=T("signal?",28,GREY).move_to(P(5.6,-2.5))
        self.play(FadeIn(question),run_time=0.5)
        self.at("ends in the lysosome")
        ly=Circle(radius=0.6,color=RED,fill_color=RED,fill_opacity=0.12).move_to(P(3.35,-2.5))
        ll=T("lysosome",22,RED).move_to(P(3.35,-3.35))
        self.play(Create(ly),FadeIn(ll),VGroup(endo,ves[2].group()).animate.scale(0.45).move_to(ly),run_time=0.8)
        self.finish()


class S06Controls(SpokenScene):
    def construct(self):
        tube=RoundedRectangle(width=2,height=4.1,corner_radius=0.45,color=GREY).move_to(P(-3.8,0))
        ves=[Ves(P(-4.15+i*0.6,-1.45),0.22) for i in range(2)]
        clumps=VGroup(*[Circle(radius=0.13,color=GREY,fill_color=GREY,fill_opacity=1).move_to(P(-4.3+i*0.35,-1.8)) for i in range(4)])
        title=T("centrifuge pellet",28,GREY).move_to(P(-3.8,2.7))
        self.at("Proving a case takes controls")
        self.play(Create(tube),FadeIn(title),run_time=0.6)
        self.at("collects vesicles")
        self.play(*[FadeIn(v.shell()) for v in ves],run_time=0.5)
        self.at("protein clumps")
        lab=T("vesicles + protein clumps",26,GREY).move_to(P(1.6,-1.6))
        self.play(FadeIn(clumps),FadeIn(lab),run_time=0.5)
        self.at("activity floats")
        gradient=VGroup(*[Rectangle(width=1.9,height=0.65,stroke_width=0,fill_color=PURPLE,fill_opacity=0.08+i*0.055).move_to(P(-3.8,1.65-i*0.65)) for i in range(6)])
        gradient.set_z_index(-2)
        activity=Dot(P(-3.8,-1.45),radius=0.11,color=GOLD)
        act=T("activity",26,GOLD).move_to(P(-0.7,0.9))
        self.play(FadeIn(gradient),FadeIn(activity),FadeIn(act),FadeOut(lab),run_time=0.5)
        self.at("density gradient")
        band=Line(P(-4.7,0.65),P(-2.9,0.65),color=TEAL,stroke_width=5)
        self.play(*[v.shell().animate.shift(UP*2.1) for v in ves],activity.animate.move_to(P(-3.8,0.9)),Create(band),Transform(title,T("density gradient",28,PURPLE).move_to(title)),run_time=0.9)
        self.at("whether it is specific")
        specific=T("specific response?",30,GOLD).move_to(P(2.5,1.3))
        self.play(FadeIn(specific),run_time=0.5)
        self.at("T cell response")
        match=T("matching T cell → signal",26,GOLD).move_to(P(2.5,0.35))
        self.play(FadeIn(match),run_time=0.5)
        self.at("mind the name")
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=0.5)
        ex=Ves(P(-3,0.5),0.65,[45,135]); mv=Ves(P(3,-1.3),0.65,[45,135])
        origin=T("exosome\nfrom inside a compartment",24,PURPLE).move_to(P(-3,2.7))
        self.add(ex.group(),origin)
        self.at("bud straight from the cell surface")
        membrane=membrane_line(-1.3,0.4,6.2)
        bud=Bud(P(3,-1.3),90,P(3,0.5),0.65,L=1.2,w=0.4)
        self.play(Create(membrane),run_time=0.3); self.add(bud.holder)
        self.play(bud.grow(run_time=0.55),run_time=0.55)
        self.play(bud.pinch(run_time=0.55),run_time=0.55)
        self.remove(bud.holder)
        mv=Ves(P(3,0.5),0.65,[45,135]);self.add(mv.group())
        surface=T("microvesicle\nfrom the cell surface",24,GREY).move_to(P(3,2.7))
        self.at("look the same")
        self.play(FadeIn(surface),*[Indicate(v.body,color=TEAL) for v in (ex,mv)],run_time=0.6)
        self.at("unless you can show")
        self.play(FadeOut(membrane),FadeOut(origin),FadeOut(surface),run_time=0.5)
        self.at("where a vesicle formed")
        unknown=T("origin?",30,GREY).move_to(P(0,2.5))
        self.play(FadeIn(unknown),run_time=0.5)
        self.at("extracellular vesicle")
        both=T("extracellular vesicle",36,TEAL).move_to(P(0,-1.65))
        self.play(FadeIn(both),run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "Say exosome only when you can show where it formed."
