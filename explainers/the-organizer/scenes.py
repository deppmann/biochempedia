"""The Organizer, chapter 1: One Sheet, Two Fates  (Biochemistrypedia chaptered film)

COLOR MAP (one color per concept, the same in every chapter)
  BLUE   = ectoderm / skin (cells on their way to skin)
  PURPLE = neural fate (neural plate, neural tube, nervous system)
  GREEN  = mesoderm
  GREY   = endoderm, early undecided cells, outlines, labels
  CREAM  = donor tissue / the organizer (the dorsal-lip graft, notochord)
  YELLOW = the signal / what is highlighted or moves
  RED    = the open question
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
CREAM = "#F2EBD3"
EGG_LINE = "#C3C9D4"

CX0 = 1.2          # centre of the embryo in the first four scenes (labels live on the left)
LABX = -4.5
GX, GK = -2.9, 0.95  # gastrula position and scale from the layers scenes on


# ---------------------------------------------------------------- helpers
def cell(x, y, color=GREY, r=0.3, sw=3):
    fo = 0.85 if color == CREAM else 0.5
    return Circle(radius=r, stroke_color=color, stroke_width=sw, fill_color=color,
                  fill_opacity=fo).move_to([x, y, 0])


def paint(c, color):
    fo = 0.85 if color == CREAM else 0.5
    return c.animate.set_stroke(color).set_fill(color, fo)


def hi(g):
    return g.animate.set_stroke(opacity=1).set_fill(opacity=0.5)


def lo(g):
    return g.animate.set_stroke(opacity=0.25).set_fill(opacity=0.12)


def lab(text, color=GREY, size=28, **kw):
    return T(text, size, color, **kw)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.05, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def at_(x, y):
    return np.array([x, y, 0.0])


GR = [(3.0, 24), (2.4, 20), (1.8, 15)]   # (radius, number of cells) of the outer, middle, inner layer


def ring_pos(cx, cy, k, ring, i):
    R, n = GR[ring]
    a = TAU * i / n
    return np.array([cx + k * R * np.cos(a), cy + k * R * np.sin(a), 0.0])


def blast_ring(cx, cy, k=1.0, color=GREY):
    return [cell(*ring_pos(cx, cy, k, 0, i)[:2], color, r=0.3 * k, sw=3 * max(k, 0.6)) for i in range(24)]


def gastrula(cx, cy, k=1.0, cols=(BLUE, GREEN, GREY)):
    """three layers of cells with a slit (the blastopore) at angle 0. returns [outer, middle, inner]."""
    rings = []
    for ri, col in enumerate(cols):
        n = GR[ri][1]
        rings.append([cell(*ring_pos(cx, cy, k, ri, i)[:2], col, r=0.3 * k, sw=3 * max(k, 0.6)) for i in range(1, n)])
    return rings


def hex_discs(R=2.95, d=0.62, r=0.3, color=GREY):
    out = []
    rows = int(R / (d * 0.866)) + 1
    for j in range(-rows, rows + 1):
        y = j * d * 0.866
        off = d / 2 if j % 2 else 0
        for i in range(-12, 13):
            x = i * d + off
            if x * x + y * y <= R * R:
                out.append(cell(CX0 + x, y, color, r))
    return out


def sheet(n, y, spacing, r, color=BLUE):
    return [cell((i - (n - 1) / 2) * spacing, y, color, r) for i in range(n)]



RT = 0.95   # radius of the neural cells once the plate has rolled into a tube (columnar cells are taller)


def tube_geom(r, rt):
    """R: radius of the ring of five tube cells; up: height of the tube centre above the sheet row (the tube's
    bottom edge sits level with the sheet's bottom edge); xf: x offset of the first flat cell that touches the tube."""
    R = rt / np.sin(PI / 5)
    up = (rt - r) + R
    h = up - R * np.sin(np.radians(18))
    xf = R * np.cos(np.radians(18)) + np.sqrt(max((r + rt + 0.08) ** 2 - h * h, 0))
    return R, up, xf


def neurulate(cells, cx, row_y, r, rt, flats=()):
    """five sheet cells left to right: thicken into a plate, raise their edges, close into a tube that sits IN the
    sheet's row, while `flats` (list of (cell, new_x)) slide in to touch it. returns three functions; each returns
    the animations of one step (build them just before playing, because Manim's .animate shares one target per
    mobject)."""
    w, h = 1.6 * r, 3.0 * r
    k = r / 0.58
    dy = [0.95 * k, 0.5 * k, 0.3 * k, 0.5 * k, 0.95 * k]
    sp = 1.64 * r
    R, up, xf = tube_geom(r, rt)
    ang = {2: -90, 3: -18, 4: 54, 0: 126, 1: 198}

    def a1():
        return [c.animate.set_stroke(PURPLE).set_fill(PURPLE, 0.5).stretch_to_fit_width(w).stretch_to_fit_height(h)
                .shift(UP * (h / 2 - r)) for c in cells]

    def a2():
        return [c.animate.move_to([cx + (j - 2) * sp, row_y + dy[j] + r * 0.6, 0]) for j, c in enumerate(cells)]

    def a3():
        out = []
        for j, c in enumerate(cells):
            a = np.radians(ang[j])
            out.append(Transform(c, cell(cx + R * np.cos(a), row_y + up + R * np.sin(a), PURPLE, rt)))
        for c, nx in flats:
            out.append(c.animate.move_to([nx, row_y, 0]))
        return out

    return a1, a2, a3


def tube_cells(cx, row_y, r, rt):
    R, up, xf = tube_geom(r, rt)
    out = []
    for j in range(5):
        a = np.radians([126, 198, -90, -18, 54][j])
        out.append(cell(cx + R * np.cos(a), row_y + up + R * np.sin(a), PURPLE, rt))
    return out


def flat_xs(cx, r, rt, sp, n_each):
    """x positions of the flat sheet cells on each side of a rolled-up tube: (left list outward, right list outward)."""
    R, up, xf = tube_geom(r, rt)
    return [cx - xf - i * sp for i in range(n_each)], [cx + xf + i * sp for i in range(n_each)]



# ---- small icons -------------------------------------------------------------------------------
def skin_icon(cx, cy):
    band = RoundedRectangle(corner_radius=0.2, width=3.5, height=0.8, stroke_width=0, fill_color=BLUE,
                            fill_opacity=0.12).move_to([cx, cy, 0])
    cs = VGroup(*[cell(cx + (i - 2.5) * 0.52, cy, BLUE, 0.26, 3) for i in range(6)])
    return VGroup(band, cs)


def nerve_icon(cx, cy):
    brain = VGroup(*[Ellipse(width=1.65, height=1.7, stroke_color=PURPLE, stroke_width=4,
                             fill_color=PURPLE, fill_opacity=0.3).move_to([cx + side * 0.65, cy + 0.55, 0])
                     for side in (-1, 1)])
    fissure = Line([cx, cy + 0.05, 0], [cx, cy + 1.05, 0], color=PURPLE, stroke_width=3.5)
    gyri = VGroup(*[Arc(radius=0.22, start_angle=PI / 2, angle=PI * sg, stroke_color=PURPLE, stroke_width=3.5)
                    .move_to([cx + sg * -0.75, cy + 0.55 + dy, 0]) for sg in (-1, 1) for dy in (-0.28, 0.1, 0.48)])
    cord = RoundedRectangle(corner_radius=0.15, width=0.32, height=1.7, stroke_color=PURPLE, stroke_width=3,
                            fill_color=PURPLE, fill_opacity=0.7).move_to([cx, cy - 1.0, 0])
    ticks = VGroup(*[Line([cx - 0.16, cy - 0.45 - 0.3 * i, 0], [cx + 0.16, cy - 0.45 - 0.3 * i, 0], color=BG, stroke_width=2.5)
                     for i in range(1, 5)])
    return VGroup(brain, fissure, gyri, cord, ticks)


def muscle_icon(cx, cy):
    body = Ellipse(width=1.5, height=0.62, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.25).move_to([cx, cy, 0])
    fibres = VGroup(*[Line([cx - 0.55, cy + dy, 0], [cx + 0.55, cy + dy, 0], color=GREEN, stroke_width=2.5) for dy in (-0.12, 0, 0.12)])
    return VGroup(body, fibres)


def bone_icon(cx, cy):
    shaft = Rectangle(width=1.0, height=0.26, stroke_width=0, fill_color=GREEN, fill_opacity=0.5).move_to([cx, cy, 0])
    ends = VGroup(*[Circle(radius=0.17, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.5)
                    .move_to([cx + sx * 0.55, cy + sy * 0.13, 0]) for sx in (-1, 1) for sy in (-1, 1)])
    return VGroup(shaft, ends)


def rod_icon(cx, cy):
    return RoundedRectangle(corner_radius=0.14, width=1.5, height=0.28, stroke_color=CREAM, stroke_width=3,
                            fill_color=CREAM, fill_opacity=0.85).move_to([cx, cy, 0])


def lock_icon(cx, cy, color=BLUE):
    body = RoundedRectangle(corner_radius=0.06, width=0.4, height=0.3, stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=0.4).move_to([cx, cy - 0.06, 0])
    sh = Arc(radius=0.12, start_angle=0, angle=PI, stroke_color=color, stroke_width=3).move_to([cx, cy + 0.16, 0])
    return VGroup(body, sh)



# ---- the ectoderm panel carried from scene 5 into scene 6 ---------------------------------------------
def ecto_panel():
    t = lab("ectoderm", BLUE, 38, weight=BOLD).move_to([3.5, 2.7, 0])
    a = arr([1.9, 2.65, 0], [-1.0, 2.4, 0], BLUE)
    s = skin_icon(3.2, 1.5).stretch_to_fit_width(6.2).stretch_to_fit_height(1.0)
    sl = lab("skin", BLUE, 30).move_to([3.2, 2.2, 0])
    n = nerve_icon(3.2, -0.8).scale(1.15, about_point=at_(3.2, -0.8))
    nl = lab("brain and spinal cord", PURPLE, 30).move_to([3.2, -3.45, 0])
    return t, a, s, sl, n, nl


def rings_dim(rings, which):
    """set the layers in `which` (indices) to dim, the others to full."""
    for i, r in enumerate(rings):
        g = VGroup(*r)
        if i in which:
            g.set_stroke(opacity=0.25).set_fill(opacity=0.12)


# ---------------------------------------------------------------- titles
class S00Title(TitleCard):
    LESSON = "The Organizer: Spemann and Mangold"
    TITLE = "One Sheet, Two Fates"


# ---------------------------------------------------------------- larvae
def larva(cx, cy, h=6.0):
    """a newt larva seen from above: head with eyes, body, tail with a fin."""
    prof = [(0, 0.0), (0.015, 0.4), (0.05, 0.62), (0.11, 0.7), (0.17, 0.58), (0.25, 0.72), (0.4, 0.84), (0.55, 0.78),
            (0.68, 0.55), (0.78, 0.3), (0.86, 0.22), (0.93, 0.4), (0.985, 0.28), (1.0, 0.0)]
    ty = lambda t: cy + h / 2 - t * h
    left = [[cx - w, ty(t), 0] for t, w in prof]
    right = [[cx + w, ty(t), 0] for t, w in reversed(prof[1:-1])]
    body = VMobject(stroke_color=GREY, stroke_width=4, fill_color=BLUE, fill_opacity=0.14)
    body.set_points_smoothly(left + right + [left[0]])
    eyes = VGroup(*[Circle(radius=0.08, stroke_width=0, fill_color=GREY, fill_opacity=1).move_to([cx + s * 0.33, ty(0.075), 0])
                    for s in (-1, 1)])
    tube = Line([cx, ty(0.19), 0], [cx, ty(0.9), 0], color=PURPLE, stroke_width=14)
    return VGroup(body, eyes), tube, ty


class S01Q(SpokenScene):
    def construct(self):
        b1, t1, ty = larva(-4.0, 0.2)
        b2, t2, _ = larva(-0.6, 0.2)
        l_n = lab("no graft", GREY, 30).move_to([-4.0, -3.45, 0])
        l_h = lab("host with graft", GREY, 30).move_to([-0.6, -3.45, 0])
        self.play(FadeIn(b1), FadeIn(b2), Create(t1), Create(t2), FadeIn(l_n), FadeIn(l_h), run_time=0.5)
        px = -0.6 + 0.42
        patch = RoundedRectangle(corner_radius=0.06, width=0.42, height=0.3, stroke_color=YELLOW, stroke_width=4,
                                 fill_color=CREAM, fill_opacity=0.9).move_to([px, ty(0.55), 0])
        l_g = lab("graft", CREAM, 32).move_to([4.4, ty(0.55), 0])
        a_g = arr([3.5, ty(0.55), 0], [px + 0.3, ty(0.55), 0], CREAM)
        self.at("small graft")
        self.play(FadeIn(patch, scale=0.5), run_time=0.4)
        self.play(FadeIn(l_g), GrowArrow(a_g), run_time=0.4)
        tube2b = Line([px, ty(0.45), 0], [px, ty(0.22), 0], color=PURPLE, stroke_width=14)
        l_t = lab("second\nspinal cord", PURPLE, 32, line_spacing=0.8).move_to([4.5, 1.9, 0])
        a_t = arr([3.3, 1.8, 0], [px + 0.25, ty(0.3), 0], PURPLE)
        self.at("second spinal cord")
        self.play(Create(tube2b), FadeIn(l_t), GrowArrow(a_t), run_time=0.9)
        halo = Ellipse(width=0.8, height=2.0, stroke_color=BLUE, stroke_width=4, fill_opacity=0).move_to([px, ty(0.4), 0])
        l_s = lab("from cells\nmeant for skin", BLUE, 32, line_spacing=0.8).move_to([4.5, -0.9, 0])
        a_s = arr([3.3, -0.8, 0], [px + 0.42, ty(0.52), 0], BLUE)
        self.at("meant for skin")
        self.play(Create(halo), FadeIn(l_s), GrowArrow(a_s), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------- cleavage, blastula, gastrulation
CAV_END = 0.26


class S02Cleave(SpokenScene):
    def construct(self):
        R = 3.25
        egg = Circle(radius=R, stroke_color=GREY, stroke_width=5, fill_color=GREY, fill_opacity=0.22).move_to([CX0, 0, 0])
        self.play(FadeIn(egg, scale=0.85), run_time=0.7)
        l_egg = lab("egg", TEXT, 36).move_to([LABX, 0, 0])
        self.at("The egg")
        self.play(FadeIn(l_egg), run_time=0.3)

        def vline(a):
            h = np.sqrt(R * R - a * a) - 0.08
            return Line([CX0 + a, -h, 0], [CX0 + a, h, 0], color=EGG_LINE, stroke_width=4)

        def hline(b):
            w = np.sqrt(R * R - b * b) - 0.08
            return Line([CX0 - w, b, 0], [CX0 - w + 2 * w, b, 0], color=EGG_LINE, stroke_width=4)

        def count(text):
            return lab(text, GREY, 30).move_to([LABX, -0.5, 0])

        self.at("divides into")
        v0 = vline(0)
        l_c = lab("cleavage", TEXT, 40, weight=BOLD).move_to([LABX, 0.3, 0])
        n2 = count("2 cells")
        self.play(Create(v0), ReplacementTransform(l_egg, l_c), FadeIn(n2), run_time=0.35)
        h0 = hline(0)
        n4 = count("4 cells")
        self.play(Create(h0), ReplacementTransform(n2, n4), run_time=0.3)
        v1, v2 = vline(-1.6), vline(1.6)
        n8 = count("8 cells")
        self.play(Create(v1), Create(v2), ReplacementTransform(n4, n8), run_time=0.3)
        discs = VGroup(*hex_discs())
        many = count("many small cells")
        self.at("ball of smaller")
        self.play(FadeOut(VGroup(egg, v0, h0, v1, v2)), run_time=0.3)
        self.play(FadeIn(discs, lag_ratio=0.01), ReplacementTransform(n8, many), run_time=0.7)
        self.finish()


class S03Blastula(SpokenScene):
    def construct(self):
        C0 = np.array([CX0, 0, 0])
        discs = hex_discs()
        l_c = lab("cleavage", TEXT, 40, weight=BOLD).move_to([LABX, 0.3, 0])
        many = lab("many small cells", GREY, 30).move_to([LABX, -0.5, 0])
        cav = Circle(radius=2.7, stroke_width=0, fill_color=TEXT, fill_opacity=0.0).move_to(C0)
        self.add(cav, *discs, l_c, many)
        ring24 = blast_ring(CX0, 0, 1.0)
        slots = [ring_pos(CX0, 0, 1.0, 0, i) for i in range(24)]
        l_a = lab("amphibian\nembryo", TEXT, 36, line_spacing=0.8).move_to([LABX, 0, 0])
        self.at("amphibians")
        self.play(ReplacementTransform(l_c, l_a), FadeOut(many), run_time=0.4)
        # every cell slides to the rim: the outermost cell of each direction becomes the wall, the rest merge into it
        best = {}
        target = {}
        for c in discs:
            v = c.get_center() - C0
            idx = int(round((np.arctan2(v[1], v[0]) % TAU) / TAU * 24)) % 24
            target[id(c)] = idx
            rad = np.linalg.norm(v)
            if idx not in best or rad > best[idx][0]:
                best[idx] = (rad, c)
        keep = [best[i][1] for i in sorted(best)]
        extras = [c for c in discs if all(c is not k for k in keep)]
        self.at("ball becomes")
        self.play(*[c.animate.move_to(slots[target[id(c)]]) for c in discs],
                  cav.animate.set_fill(opacity=0.18), run_time=0.6)
        self.play(FadeOut(VGroup(*extras)), run_time=0.25)
        self.remove(*keep)
        self.add(*ring24)
        l_b = lab("blastula", TEXT, 40, weight=BOLD).move_to([LABX, 0, 0])
        self.at("blastula")
        self.play(ReplacementTransform(l_a, l_b), run_time=0.4)
        self.at("sphere of cells")
        self.play(Indicate(VGroup(*ring24), color=TEXT, scale_factor=1.04), run_time=0.8)
        l_cav = lab("fluid-filled\ncavity", TEXT, 34, line_spacing=0.8).move_to([CX0, 0, 0])
        self.at("fluid filled cavity")
        self.play(FadeIn(l_cav), cav.animate.set_fill(opacity=CAV_END), run_time=0.6)
        self.finish()


class S04Gast(SpokenScene):
    def construct(self):
        ring = blast_ring(CX0, 0, 1.0)
        cav = Circle(radius=2.7, stroke_width=0, fill_color=TEXT, fill_opacity=CAV_END).move_to([CX0, 0, 0])
        l_b = lab("blastula", TEXT, 40, weight=BOLD).move_to([LABX, 0, 0])
        l_cav = lab("fluid-filled\ncavity", TEXT, 34, line_spacing=0.8).move_to([CX0, 0, 0])
        self.add(cav, *ring, l_b, l_cav)
        l_g = lab("gastrulation", TEXT, 40, weight=BOLD).move_to([LABX, 0, 0])
        self.at("gastrulation")
        self.play(ReplacementTransform(l_b, l_g), FadeOut(l_cav), cav.animate.set_fill(opacity=0), run_time=0.5)
        # a stream of cells goes in through the gap at the right: middle-layer cells (green) first, inner-layer cells (grey) last
        start = np.array([CX0 + 3.0, 0, 0])
        outer = ring[1:]
        first = ring[0]
        mid = [cell(*ring_pos(CX0, 0, 1.0, 1, i)[:2], GREEN, 0.3) for i in range(1, 20)]
        inn = [cell(*ring_pos(CX0, 0, 1.0, 2, i)[:2], GREY, 0.3) for i in range(1, 15)]
        order = [m for pair in zip(mid[:9], mid[::-1][:9]) for m in pair] + [mid[9]]
        for i in range(7):
            order += [inn[i], inn[13 - i]]
        first_tgt = ring_pos(CX0, 0, 1.0, 2, 7)
        self.at("cells move inside")
        anims = [first.animate.move_to(first_tgt)]
        anims += [paint(c, BLUE) for c in outer]
        anims += [FadeIn(c, shift=c.get_center() - start) for c in order]
        self.play(LaggedStart(*anims, lag_ratio=0.045), run_time=1.8)
        self.at("sorts into three layers")
        self.play(Indicate(VGroup(*outer), color=BLUE, scale_factor=1.02),
                  Indicate(VGroup(*mid), color=GREEN, scale_factor=1.02), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------- the three layers
def g_state(dim=()):
    rings = gastrula(GX, 0, GK)
    for i in dim:
        VGroup(*rings[i]).set_stroke(opacity=0.25).set_fill(opacity=0.12)
    return rings


class S05Layers(SpokenScene):
    def construct(self):
        # carried over from scene 4: the finished gastrula at its old place, then it slides left
        rings = gastrula(CX0, 0, 1.0)
        allc = VGroup(*[c for r in rings for c in r])
        self.add(allc)
        self.play(allc.animate.scale(GK, about_point=at_(CX0, 0)).shift(at_(GX - CX0, 0)), run_time=0.3)
        t, a, s, sl, n, nl = ecto_panel()
        self.at("outer layer")
        self.play(lo(VGroup(*rings[1], *rings[2])), run_time=0.4)
        self.at("the ectoderm")
        self.play(FadeIn(t), GrowArrow(a), Indicate(VGroup(*rings[0]), color=BLUE, scale_factor=1.04), run_time=0.6)
        self.at("outer skin")
        self.play(FadeIn(s, lag_ratio=0.2), FadeIn(sl), run_time=0.5)
        self.at("nervous system")
        self.play(FadeIn(n, lag_ratio=0.3), FadeIn(nl), run_time=0.7)
        self.finish()


class S06Meso(SpokenScene):
    def construct(self):
        rings = g_state(dim=(1, 2))
        allc = VGroup(*[c for r in rings for c in r])
        t, a, s, sl, n, nl = ecto_panel()
        panel = VGroup(t, a, s, sl, n, nl)
        self.add(allc, panel)
        self.at("middle layer")
        self.play(FadeOut(panel), lo(VGroup(*rings[0])), hi(VGroup(*rings[1])), run_time=0.6)
        l_m = lab("mesoderm", GREEN, 38, weight=BOLD).move_to([3.5, 2.7, 0])
        a_m = arr([1.9, 2.65, 0], [-1.4, 1.8, 0], GREEN)
        self.at("the mesoderm")
        self.play(FadeIn(l_m), GrowArrow(a_m), Indicate(VGroup(*rings[1]), color=GREEN, scale_factor=1.04), run_time=0.6)
        mu, mul = muscle_icon(1.5, 1.2), lab("muscle", TEXT, 30).move_to([3.4, 1.2, 0])
        bo, bol = bone_icon(1.5, -0.1), lab("bone", TEXT, 30).move_to([3.1, -0.1, 0])
        no, nol = rod_icon(1.5, -1.4), lab("notochord", CREAM, 30).move_to([3.6, -1.4, 0])
        self.at("muscle")
        self.play(FadeIn(mu), FadeIn(mul), run_time=0.4)
        self.at("bone")
        self.play(FadeIn(bo), FadeIn(bol), run_time=0.3)
        self.at("and the")
        self.play(FadeIn(no), FadeIn(nol), run_time=0.4)
        self.at("a stiff rod")
        self.play(Indicate(no, color=CREAM, scale_factor=1.25), run_time=0.5)
        meso_items = VGroup(l_m, a_m, mu, mul, bo, bol, no, nol)
        l_e = lab("endoderm", GREY, 38, weight=BOLD).move_to([3.5, 2.7, 0])
        a_e = arr([1.9, 2.65, 0], [-1.7, 1.2, 0], GREY)
        self.at("inner layer")
        self.play(FadeOut(meso_items), lo(VGroup(*rings[1])), hi(VGroup(*rings[2])), FadeIn(l_e), GrowArrow(a_e), run_time=0.6)
        l_gut = lab("gut", TEXT, 36).move_to([GX, 0, 0])
        self.at("lines the gut")
        self.play(FadeIn(l_gut), Indicate(VGroup(*rings[2]), color=TEXT, scale_factor=1.05), run_time=0.6)
        self.finish()


class S06bBeat(NarratedScene):
    def construct(self):
        rings = g_state(dim=(0, 1))
        allc = VGroup(*[c for r in rings for c in r])
        l_e = lab("endoderm", GREY, 38, weight=BOLD).move_to([3.5, 2.7, 0])
        a_e = arr([1.9, 2.65, 0], [-1.7, 1.2, 0], GREY)
        l_gut = lab("gut", TEXT, 36).move_to([GX, 0, 0])
        self.add(allc, l_e, a_e, l_gut)
        self.finish()


# ---------------------------------------------------------------- blastopore and dorsal lip
class S07Lip(SpokenScene):
    def construct(self):
        rings = g_state()
        allc = VGroup(*[c for r in rings for c in r])
        self.add(allc)
        gapx = GX + 3.0 * GK
        a_in = arr([2.2, 0, 0], [GX - 0.9, 0, 0], YELLOW, w=6)
        l_in = lab("cells move in", YELLOW, 30).move_to([4.2, 0, 0])
        self.at("move inside")
        self.play(GrowArrow(a_in), FadeIn(l_in), run_time=0.7)
        slit = DashedLine([gapx, -0.3, 0], [gapx, 0.3, 0], color=TEXT, stroke_width=5)
        self.at("a slit")
        self.play(Create(slit), run_time=0.4)
        l_bl = lab("blastopore", TEXT, 34, weight=BOLD).move_to([3.7, -1.5, 0])
        a_bl = arr([2.3, -1.3, 0], [gapx + 0.15, -0.3, 0], TEXT)
        self.at("the blastopore")
        self.play(FadeIn(l_bl), GrowArrow(a_bl), run_time=0.5)
        lip = SurroundingRectangle(VGroup(rings[0][0], rings[1][0], rings[2][0]), buff=0.05, corner_radius=0.12,
                                   stroke_color=YELLOW, stroke_width=5, fill_color=YELLOW, fill_opacity=0.14)
        self.at("Its edge")
        self.play(FadeOut(a_in), FadeOut(l_in), Create(lip), run_time=0.6)
        back = Arc(radius=3.4, start_angle=np.radians(26), angle=np.radians(128), arc_center=[GX, 0, 0],
                   color=GREY, stroke_width=7)
        l_fb = lab("future back", GREY, 32).move_to([3.7, 2.95, 0])
        a_fb = arr([2.3, 2.9, 0], [GX + 3.4 * np.cos(np.radians(50)) + 0.05, 3.4 * np.sin(np.radians(50)) - 0.02, 0], GREY)
        self.at("on the future back")
        self.play(Create(back), FadeIn(l_fb), GrowArrow(a_fb), run_time=0.6)
        l_dl = lab("dorsal lip", YELLOW, 36, weight=BOLD).move_to([3.7, 1.35, 0])
        a_dl = arr([2.3, 1.25, 0], [0.4, 0.85, 0], YELLOW)
        self.at("dorsal lip")
        self.play(FadeIn(l_dl), GrowArrow(a_dl), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------- one sheet
RR, RS = 0.62, 1.15      # sheet cell radius and spacing (11 cells)
ROW_Y = -1.8            # the sheet's row; the tube rises from it and the labels sit above and below


class S08Sheet(SpokenScene):
    def construct(self):
        rings = g_state()
        allc = VGroup(*[c for r in rings for c in r])
        self.add(allc)
        self.at("watch the")
        self.play(lo(VGroup(*rings[1], *rings[2])), run_time=0.4)
        l_e = lab("ectoderm", BLUE, 38, weight=BOLD).move_to([3.5, 2.7, 0])
        self.at("the ectoderm")
        self.play(FadeIn(l_e), Indicate(VGroup(*rings[0]), color=BLUE, scale_factor=1.04), run_time=0.6)
        # the outer layer is cut open and laid flat: copies of its cells unroll into a sheet of 11 cells,
        # while the gastrula shrinks to the top of the frame
        outer = rings[0]
        copies = [c.copy() for c in outer]
        self.add(*copies)
        order = sorted(range(len(outer)), key=lambda j: ((np.degrees(TAU * (j + 1) / 24) - 90 + 180) % 360) - 180)
        pick = [order[int(round(v))] for v in np.linspace(0, len(order) - 1, 11)]
        row_x = [(i - 5) * RS for i in range(11)]
        anims = [copies[j].animate.scale(RR / (0.3 * GK)).move_to([row_x[i], ROW_Y, 0]) for i, j in enumerate(pick)]
        gone = [c for j, c in enumerate(copies) if j not in pick]
        self.play(*anims, FadeOut(VGroup(*gone)), allc.animate.scale(0.42, about_point=at_(GX, 0)).shift(at_(-GX, 2.2)),
                  l_e.animate.move_to([3.3, 2.2, 0]), run_time=1.0)
        band = RoundedRectangle(corner_radius=0.3, width=13.0, height=1.5, stroke_width=0, fill_color=BLUE,
                                fill_opacity=0.10).move_to([0, ROW_Y, 0])
        l_s = lab("one sheet", BLUE, 38, weight=BOLD).move_to([0, -3.4, 0])
        self.at("one sheet")
        self.play(FadeIn(band), FadeIn(l_s), run_time=0.5)
        self.finish()


def sheet_band():
    return RoundedRectangle(corner_radius=0.3, width=13.0, height=1.5, stroke_width=0, fill_color=BLUE,
                            fill_opacity=0.10).move_to([0, ROW_Y, 0])


class S09Plate(SpokenScene):
    def construct(self):
        cells = sheet(11, ROW_Y, RS, RR)
        band = sheet_band()
        l_one = lab("one sheet", BLUE, 38, weight=BOLD).move_to([0, -3.4, 0])
        self.add(band, l_one, *cells)
        plate = cells[3:8]
        br = Brace(VGroup(*plate), UP, color=GREY, buff=0.15)
        l_back = lab("back", GREY, 36)
        l_back.next_to(br, UP, buff=0.12)
        self.at("Along the back")
        self.play(FadeIn(br), FadeIn(l_back), FadeOut(l_one), run_time=0.5)
        lx, rx = flat_xs(0, RR, RT, RS, 3)
        flats = [(cells[2 - i], lx[i]) for i in range(3)] + [(cells[8 + i], rx[i]) for i in range(3)]
        a1, a2, a3 = neurulate(plate, 0, ROW_Y, RR, RT, flats)
        self.at("strip becomes")
        self.play(*a1(), FadeOut(br), run_time=0.6)
        l_np = lab("neural plate", PURPLE, 38, weight=BOLD).move_to([0, 0.4, 0])
        self.at("neural plate")
        self.play(ReplacementTransform(l_back, l_np), run_time=0.4)
        self.at("rolls up")
        self.play(*a2(), FadeOut(l_np), FadeOut(band), run_time=0.65)
        self.play(*a3(), run_time=0.85)
        l_nt = lab("neural tube", PURPLE, 38, weight=BOLD).move_to([5.0, 1.1, 0])
        a_nt = arr([3.6, 0.85, 0], [2.55, 0.5, 0], PURPLE)
        self.at("neural tube")
        self.play(FadeIn(l_nt), GrowArrow(a_nt), run_time=0.4)
        l_fb = lab("future brain and spinal cord", PURPLE, 32).move_to([0, -3.3, 0])
        self.at("future brain")
        self.play(FadeIn(l_fb), run_time=0.5)
        self.finish()


def tube_state():
    tube = tube_cells(0, ROW_Y, RR, RT)
    lx, rx = flat_xs(0, RR, RT, RS, 3)
    flat = [cell(x, ROW_Y, BLUE, RR) for x in lx + rx]
    return tube, flat


SIDE_X = 3.4   # x of the side labels (belly side / skin)


class S10Belly(SpokenScene):
    def construct(self):
        tube, flat = tube_state()
        self.add(*tube, *flat)
        l_bl = lab("belly side", GREY, 34).move_to([-SIDE_X, -3.35, 0])
        l_br = lab("belly side", GREY, 34).move_to([SIDE_X, -3.35, 0])
        self.at("On the belly")
        self.play(FadeIn(l_bl), FadeIn(l_br), run_time=0.5)
        self.at("stays flat")
        self.play(Indicate(VGroup(*flat), color=BLUE, scale_factor=1.08), run_time=0.7)
        s_l = lab("skin", BLUE, 42, weight=BOLD).move_to([-SIDE_X, -3.35, 0])
        s_r = lab("skin", BLUE, 42, weight=BOLD).move_to([SIDE_X, -3.35, 0])
        self.at("becomes skin")
        self.play(ReplacementTransform(l_bl, s_l), ReplacementTransform(l_br, s_r), run_time=0.5)
        self.finish()


def question_group():
    q1 = lab("Why does the back strip become neural,", TEXT, 36, t2c={"neural": PURPLE})
    q2 = lab("while the belly strip becomes skin?", TEXT, 36, t2c={"skin": BLUE})
    q1.move_to([0, 3.4, 0])
    q2.move_to([0, 2.75, 0])
    return q1, q2


def side_skin():
    return (lab("skin", BLUE, 42, weight=BOLD).move_to([-SIDE_X, -3.35, 0]),
            lab("skin", BLUE, 42, weight=BOLD).move_to([SIDE_X, -3.35, 0]))


class S11Q(SpokenScene):
    def construct(self):
        tube, flat = tube_state()
        s_l, s_r = side_skin()
        self.add(*tube, *flat, s_l, s_r)
        q1, q2 = question_group()
        self.at("why does the back")
        self.play(FadeIn(q1, shift=UP * 0.1), run_time=0.8)
        self.at("back strip")
        self.play(Indicate(VGroup(*tube), color=PURPLE, scale_factor=1.08), run_time=0.7)
        self.at("while the belly")
        self.play(FadeIn(q2, shift=UP * 0.1), Indicate(VGroup(*flat), color=BLUE, scale_factor=1.08), run_time=0.8)
        self.finish()


class S12Pause(NarratedScene):
    def construct(self):
        tube, flat = tube_state()
        s_l, s_r = side_skin()
        q1, q2 = question_group()
        self.add(*tube, *flat, s_l, s_r, q1, q2)
        R, up, xf = tube_geom(RR, RT)
        qm = T("?", 64, RED, weight=BOLD).move_to([0, ROW_Y + up, 0])
        qa = T("?", 80, RED, weight=BOLD).move_to([-(xf + RS), ROW_Y + 1.2, 0])
        qb = T("?", 80, RED, weight=BOLD).move_to([(xf + RS), ROW_Y + 1.2, 0])
        self.play(FadeIn(qm, scale=0.6), FadeIn(qa, scale=0.6), FadeIn(qb, scale=0.6), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------- two kinds of answer
CARD_Y = -0.2
C1, C2 = -3.4, 3.4
CELL_Y = -0.5


def card_frame(cx):
    return RoundedRectangle(corner_radius=0.25, width=6.2, height=5.4, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.06).move_to([cx, CARD_Y, 0])


def card_title(cx, text):
    return lab(text, GREY, 32, weight=BOLD).move_to([cx, 2.0, 0])


def card1_parts():
    cells = VGroup(*[cell(C1 + dx, CELL_Y, BLUE, 0.45) for dx in (-1.05, 0, 1.05)])
    l1 = lab("belly cells", BLUE, 30).move_to([C1, -1.5, 0])
    l2 = lab("already fixed as skin", TEXT, 30).move_to([C1 + 0.3, -2.2, 0])
    lock = lock_icon(C1 + 0.3 - l2.width / 2 - 0.4, -2.2, TEXT).scale(1.3)
    ch = chip("whatever lies next to them", GREY, 26).move_to([C1, 1.2, 0])
    ar = arr([C1, 0.85, 0], [C1, -0.05, 0], GREY)
    x = VGroup(Line([-0.28, -0.28, 0], [0.28, 0.28, 0], color=RED, stroke_width=9),
               Line([-0.28, 0.28, 0], [0.28, -0.28, 0], color=RED, stroke_width=9)).move_to([C1, 0.4, 0])
    return cells, l1, l2, lock, ch, ar, x


class S13A1(SpokenScene):
    def construct(self):
        f1, f2 = card_frame(C1), card_frame(C2)
        t1, t2 = card_title(C1, "answer 1"), card_title(C2, "answer 2")
        self.at("two kinds")
        self.play(FadeIn(f1), FadeIn(f2), FadeIn(t1), FadeIn(t2), run_time=0.6)
        cells, l1, l2, lock, ch, ar, x = card1_parts()
        self.at("Perhaps the belly")
        self.play(FadeIn(cells, lag_ratio=0.2), FadeIn(l1), run_time=0.6)
        self.at("already fixed")
        self.play(FadeIn(l2), FadeIn(lock), FadeIn(ch), GrowArrow(ar), Create(x), run_time=0.5)
        self.at("as skin")
        self.play(Indicate(cells, color=BLUE, scale_factor=1.1), run_time=0.5)
        self.finish()


def card2_cells():
    back = VGroup(*[cell(C2 - 2.0 + 0.82 * i, CELL_Y, PURPLE, 0.38) for i in range(3)])
    belly = VGroup(*[cell(C2 + 0.46 + 0.82 * i, CELL_Y, BLUE, 0.38) for i in range(3)])
    return back, belly


class S14A2(SpokenScene):
    def construct(self):
        f1, f2 = card_frame(C1), card_frame(C2)
        t1, t2 = card_title(C1, "answer 1"), card_title(C2, "answer 2")
        card1 = VGroup(*card1_parts())
        card1.set_opacity(0.7)
        card1[-1].set_opacity(0)
        self.add(f1, f2, t1, t2, card1)
        back, belly = card2_cells()
        l_bel = lab("belly cells", BLUE, 30).move_to([C2 + 1.3, -1.5, 0])
        l_ch = lab("can still change", TEXT, 30).move_to([C2 + 0.3, -2.2, 0])
        self.at("they can still change")
        self.play(FadeIn(belly, lag_ratio=0.2), FadeIn(l_bel), FadeIn(l_ch), run_time=0.7)
        ch = chip("something nearby", GREY, 26).move_to([C2, 1.2, 0])
        a_bel = arr([C2 + 0.35, 0.85, 0], [C2 + 1.3, -0.02, 0], YELLOW, w=6)
        self.at("something nearby")
        self.play(FadeIn(ch), GrowArrow(a_bel), run_time=0.6)
        l_bs = lab("back strip", PURPLE, 30).move_to([C2 - 1.2, -1.5, 0])
        a_bs = arr([C2 - 0.35, 0.85, 0], [C2 - 1.2, -0.02, 0], YELLOW, w=8)
        self.at("the back strip")
        self.play(FadeIn(back, lag_ratio=0.2), FadeIn(l_bs), GrowArrow(a_bs), run_time=0.6)
        self.at("what to become")
        self.play(Indicate(a_bs, color=YELLOW, scale_factor=1.15), Indicate(back, color=PURPLE, scale_factor=1.08), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------- the graft test
T_Y = 0.2
TR, TS = 0.38, 0.8    # cell radius and spacing in the 7-cell belly sheet
TCX = 2.7             # centre of the belly sheet
TRT = 0.55            # neural cell radius once the tube has formed
MG = (-4.3, 0.2, 0.75)  # the gastrula the graft is cut from (about 60% of the frame height)
BAR_W, BAR_H = 4.3, 0.5
BAR_Y = T_Y - TR - BAR_H / 2


def test_static():
    rings = gastrula(*MG)
    row = [cell(TCX + (i - 4) * TS, T_Y, BLUE, TR) for i in range(9)]
    return rings, row


def bar_piece():
    return RoundedRectangle(corner_radius=0.06, width=BAR_W, height=BAR_H, stroke_color=YELLOW, stroke_width=3,
                            fill_color=CREAM, fill_opacity=0.9).move_to([TCX, BAR_Y, 0])


def lip_box(rings):
    return SurroundingRectangle(VGroup(rings[0][0], rings[1][0], rings[2][0]), buff=0.05, corner_radius=0.08,
                                stroke_color=YELLOW, stroke_width=4, fill_color=YELLOW, fill_opacity=0.18)


def test_labels():
    return (lab("belly\nectoderm", BLUE, 30, line_spacing=0.8).move_to([5.7, 1.85, 0]),
            lab("dorsal-lip tissue = the organizer", CREAM, 30).move_to([TCX, BAR_Y - 0.65, 0]))


class S15Test(SpokenScene):
    def construct(self):
        rings, row = test_static()
        allc = VGroup(*[c for r in rings for c in r])
        self.play(FadeIn(allc), FadeIn(VGroup(*row), lag_ratio=0.05), run_time=0.8)
        lip = lip_box(rings)
        self.at("tests the first")
        self.play(Create(lip), run_time=0.5)
        p0 = ring_pos(MG[0], MG[1], MG[2], 0, 1)
        piece = RoundedRectangle(corner_radius=0.05, width=0.9, height=0.5, stroke_color=YELLOW, stroke_width=2,
                                 fill_color=CREAM, fill_opacity=0.9).move_to(p0)
        self.at("first answer")
        lifted = RoundedRectangle(corner_radius=0.06, width=0.9, height=0.5, stroke_color=YELLOW, stroke_width=3,
                                  fill_color=CREAM, fill_opacity=0.9).move_to(p0 + np.array([0.8, 1.2, 0]))
        self.add(piece)
        self.play(Transform(piece, lifted), lip.animate.set_fill(opacity=0).set_stroke(opacity=0.6), run_time=0.7)
        self.at("Put")
        self.play(piece.animate.move_to([TCX, 1.65, 0]), run_time=0.75)
        self.play(Transform(piece, bar_piece()), run_time=0.55)
        l_be, l_dl = test_labels()
        a_be = arr([5.4, 1.4, 0], [TCX + 2.4, T_Y + TR + 0.05, 0], BLUE)
        self.at("belly ectoderm")
        self.play(FadeIn(l_dl), FadeIn(l_be), GrowArrow(a_be), run_time=0.5)
        q = T("?", 90, RED, weight=BOLD).move_to([TCX, 1.75, 0])
        self.at("and watch")
        self.play(FadeIn(q, scale=0.5), Indicate(VGroup(*row[2:7]), color=BLUE, scale_factor=1.05), run_time=0.6)
        self.finish()


class S15bResult(SpokenScene):
    def construct(self):
        rings, row = test_static()
        allc = VGroup(*[c for r in rings for c in r])
        lip = lip_box(rings)
        lip.set_fill(opacity=0).set_stroke(opacity=0.6)
        piece = bar_piece()
        l_be, l_dl = test_labels()
        a_be = arr([5.4, 1.4, 0], [TCX + 2.4, T_Y + TR + 0.05, 0], BLUE)
        q = T("?", 90, RED, weight=BOLD).move_to([TCX, 1.75, 0])
        self.add(allc, lip, *row, piece, l_be, l_dl, a_be, q)
        l_org = lab("organizer graft: becomes notochord", CREAM, 28).move_to([TCX, BAR_Y - 0.65, 0])
        self.at("graft worked")
        self.play(Indicate(piece, color=YELLOW, scale_factor=1.04), ReplacementTransform(l_dl, l_org), run_time=0.7)
        plate = row[2:7]
        lx, rx = flat_xs(TCX, TR, TRT, TS, 2)
        a1, a2, a3 = neurulate(plate, TCX, T_Y, TR, TRT, [(row[1], lx[0]), (row[0], lx[1]), (row[7], rx[0]), (row[8], rx[1])])
        self.play(FadeOut(q), *a1(), run_time=0.5)
        self.at("belly cells built")
        self.play(*a2(), FadeOut(a_be), run_time=0.4)
        self.play(*a3(), run_time=0.5)
        l_nt = lab("second\nneural tube", PURPLE, 32, weight=BOLD, line_spacing=0.8).move_to([-0.55, 2.45, 0])
        a_nt = arr([0.75, 2.4, 0], [TCX - 1.2, 2.3, 0], PURPLE)
        self.at("second neural tube")
        host = lab("Host cells build much of the second back", TEXT, 30).move_to([0.8, 3.35, 0])
        self.play(FadeIn(l_nt), GrowArrow(a_nt), FadeIn(host), run_time=0.5)
        l_w = lab("Whose cells?", RED, 44, font=TITLE_FONT).move_to([0, -2.75, 0])
        l_c2 = lab("Chapter 2", GREY, 28).move_to([0, -3.45, 0])
        self.at("Chapter two")
        self.play(FadeIn(l_w, shift=UP * 0.1), FadeIn(l_c2), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------- the one idea
def header_small():
    t = lab("The one idea", GOLD, 36, font=TITLE_FONT).move_to([0, 3.3, 0])
    rule = Line([-1.0, 2.9, 0], [1.0, 2.9, 0], color=GOLD, stroke_width=3)
    return VGroup(t, rule)


class S16Done(SpokenScene):
    def construct(self):
        frame = RoundedRectangle(corner_radius=0.3, width=11.4, height=4.8, stroke_color=GOLD, stroke_width=3,
                                 fill_color=GOLD, fill_opacity=0.05).move_to([0, 0, 0])
        self.play(Create(frame), run_time=0.8)
        big = lab("The one idea", TEXT, 66, font=TITLE_FONT).move_to([0, 0.5, 0])
        sub = lab("to carry through this lesson", GREY, 34).move_to([0, -0.7, 0])
        self.at("gives this lesson")
        self.play(FadeIn(big, shift=UP * 0.15), run_time=0.6)
        self.at("one idea")
        self.play(FadeIn(sub), run_time=0.5)
        self.finish()


IX = -4.65     # icon column (centre)
TX = -2.1     # text column (left edge)
Y1, Y2, Y3 = 1.85, -0.45, -2.85


def icon1(cy):
    c = cell(IX, cy, BLUE, 0.5)
    nl, nr = cell(IX - 1.2, cy, GREY, 0.32), cell(IX + 1.2, cy, GREY, 0.32)
    a1 = arr([IX - 0.85, cy, 0], [IX - 0.58, cy, 0], YELLOW, w=6, tip=0.2)
    a2 = arr([IX + 0.85, cy, 0], [IX + 0.58, cy, 0], YELLOW, w=6, tip=0.2)
    return VGroup(c, nl, nr, a1, a2).scale(1.35, about_point=at_(IX, cy))


def icon2(cy):
    cs = VGroup(*[cell(IX + dx, cy + 0.5, BLUE, 0.42) for dx in (-1.0, 0, 1.0)])
    blk = RoundedRectangle(corner_radius=0.1, width=3.0, height=0.5, stroke_color=CREAM, stroke_width=3,
                           fill_color=CREAM, fill_opacity=0.85).move_to([IX, cy - 0.3, 0])
    lb = lab("organizer", CREAM, 28).move_to([IX, cy - 0.85, 0])
    return VGroup(cs, blk, lb).scale(1.4, about_point=at_(IX, cy))


def icon3(cy):
    c = cell(IX + 0.25, cy, BLUE, 0.7)
    signal = Dot([IX - 1.5, cy, 0], radius=0.16, color=YELLOW)
    a = arr([IX - 1.25, cy, 0], [IX - 0.55, cy, 0], YELLOW, w=7, tip=0.22)
    return VGroup(c, signal, a)


def line1():
    g = VGroup(lab("A cell's fate can be set", TEXT, 40, font=TITLE_FONT),
               lab("by its neighbours.", TEXT, 40, font=TITLE_FONT)).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    return g.move_to([TX, Y1, 0], aligned_edge=LEFT)


def line2():
    cs = [lab("Move the organizer somewhere new,", TEXT, 36, font=TITLE_FONT),
          lab("and host cells there build much of", TEXT, 36, font=TITLE_FONT),
          lab("a second back around it", TEXT, 36, font=TITLE_FONT)]
    body = VGroup(*cs).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    par = lab("(the graft itself becomes notochord)", CREAM, 32, font=TITLE_FONT)
    par.next_to(body, DOWN, buff=0.32, aligned_edge=LEFT)
    g = VGroup(body, par)
    g.move_to([TX, Y2, 0], aligned_edge=LEFT)
    return cs + [par], g


def line3():
    c1 = lab("But only while they are still competent,", TEXT, 36, font=TITLE_FONT, t2c={"competent": YELLOW})
    c2 = lab("that is, able to answer.", TEXT, 38, font=TITLE_FONT)
    g = VGroup(c1, c2).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    g.move_to([TX, Y3, 0], aligned_edge=LEFT)
    return c1, c2, g


class S17Idea1(SpokenScene):
    def construct(self):
        big = lab("The one idea", TEXT, 66, font=TITLE_FONT).move_to([0, 0.5, 0])
        sub = lab("to carry through this lesson", GREY, 34).move_to([0, -0.7, 0])
        frame = RoundedRectangle(corner_radius=0.3, width=11.4, height=4.8, stroke_color=GOLD, stroke_width=3,
                                 fill_color=GOLD, fill_opacity=0.05).move_to([0, 0, 0])
        self.add(frame, big, sub)
        hd = header_small()
        l1 = line1()
        i1 = icon1(Y1)
        l1.shift(DOWN * 1.65)
        i1.shift(DOWN * 1.65)
        self.play(FadeOut(frame), FadeOut(sub), ReplacementTransform(big, hd[0]), FadeIn(hd[1]),
                  FadeIn(l1, shift=RIGHT * 0.2), FadeIn(i1), run_time=0.7)
        self.at("by its")
        self.play(i1[0].animate.set_stroke(PURPLE).set_fill(PURPLE, 0.5), Indicate(i1[3:], color=YELLOW), run_time=0.7)
        self.finish()


def idea_base(upto):
    hd = header_small()
    l1 = line1()
    i1 = icon1(Y1)
    i1[0].set_stroke(PURPLE).set_fill(PURPLE, 0.5)
    l1.shift(DOWN * 1.65)
    i1.shift(DOWN * 1.65)
    return [hd, l1, i1]


class S18Idea2(SpokenScene):
    def construct(self):
        items = idea_base(1)
        self.add(*items)
        cs, g = line2()
        i2 = icon2(Y2).shift(DOWN * 0.6)
        g.shift(DOWN * 0.6)
        self.at("Move the organizer")
        self.play(items[1].animate.shift(UP * 1.2), items[2].animate.shift(UP * 1.2),
                  FadeIn(cs[0], shift=RIGHT * 0.2), FadeIn(i2), run_time=0.7)
        self.at("host cells")
        self.play(FadeIn(cs[1], shift=RIGHT * 0.2), FadeIn(cs[2], shift=RIGHT * 0.2),
                  paint(i2[0][1], PURPLE), run_time=0.8)
        self.at("The graft itself")
        self.play(FadeIn(cs[3], shift=RIGHT * 0.2), Indicate(i2[1], color=YELLOW, scale_factor=1.06), run_time=0.8)
        self.finish()


def idea_base2():
    items = idea_base(1)
    items[1].shift(UP * 1.2)
    items[2].shift(UP * 1.2)
    cs, g = line2()
    i2 = icon2(Y2).shift(DOWN * 0.6)
    g.shift(DOWN * 0.6)
    i2[0][1].set_stroke(PURPLE).set_fill(PURPLE, 0.5)
    return items + [g, i2]


class S19Idea3(SpokenScene):
    def construct(self):
        items = idea_base2()
        self.add(*items)
        c1, c2, g = line3()
        i3 = icon3(Y3)
        self.at("But only")
        self.play(items[1].animate.shift(UP * 0.45), items[2].animate.shift(UP * 0.45),
                  items[3].animate.shift(UP * 0.6), items[4].animate.shift(UP * 0.6),
                  FadeIn(c1, shift=RIGHT * 0.2), FadeIn(i3), run_time=0.8)
        self.at("competent")
        self.play(Indicate(c1, color=YELLOW, scale_factor=1.03), i3[1].animate.move_to([IX - 0.55, Y3, 0]), run_time=0.6)
        self.at("able to answer")
        self.play(FadeIn(c2, shift=RIGHT * 0.2), i3[1].animate.move_to([IX + 0.25, Y3, 0]), i3[0].animate.set_stroke(PURPLE).set_fill(PURPLE, 0.5), run_time=0.7)
        self.finish()


class S20Beat(NarratedScene):
    def construct(self):
        items = idea_base2()
        items[1].shift(UP * 0.45)
        items[2].shift(UP * 0.45)
        items[3].shift(UP * 0.6)
        items[4].shift(UP * 0.6)
        c1, c2, g = line3()
        i3 = icon3(Y3)
        i3[0].set_stroke(PURPLE).set_fill(PURPLE, 0.5)
        i3[1].move_to([IX + 0.25, Y3, 0])
        self.add(*items, g, i3)
        self.finish()


# ---------------------------------------------------------------- the limit
LY = -0.2


def limit_card(cx, word, color, sub):
    box = RoundedRectangle(corner_radius=0.3, width=4.2, height=4.6, stroke_color=color, stroke_width=4,
                           fill_color=color, fill_opacity=0.03).move_to([cx, LY, 0])
    box.set_stroke(opacity=0.3)
    w = lab(word, TEXT, 64, font=TITLE_FONT).move_to([cx, LY + 1.35, 0])
    s = lab(sub, TEXT, 34).move_to([cx, LY + 0.4, 0])
    return box, w, s


def lit(box):
    return box.animate.set_stroke(opacity=1).set_fill(opacity=0.1)


class S22Limit2(SpokenScene):
    def construct(self):
        title = lab("Notice one limit", TEXT, 44, font=TITLE_FONT).move_to([0, 3.15, 0])
        X1, X2, X3 = -4.5, 0.0, 4.5
        b1, w1, s1 = limit_card(X1, "who", GREEN, "changed fate")
        b2, w2, s2 = limit_card(X2, "where", GREEN, "it happened")
        b3, w3, s3 = limit_card(X3, "what", RED, "the signal is")
        self.at("Notice one limit")
        self.play(FadeIn(title, shift=UP * 0.1), FadeIn(b1), FadeIn(b2), FadeIn(b3), run_time=0.6)

        def tick(cx):
            return VGroup(Line([-0.5, 0, 0], [-0.15, -0.45, 0], color=GREEN, stroke_width=12),
                          Line([-0.15, -0.45, 0], [0.6, 0.55, 0], color=GREEN, stroke_width=12)).move_to([cx, LY - 1.15, 0])
        self.at("who changed fate")
        self.play(lit(b1), FadeIn(w1), FadeIn(s1), Create(tick(X1)), run_time=0.6)
        self.at("and where")
        self.play(lit(b2), FadeIn(w2), FadeIn(s2), Create(tick(X2)), run_time=0.6)
        q = T("?", 100, RED, weight=BOLD).move_to([X3, LY - 1.15, 0])
        self.at("Not what")
        self.play(lit(b3), FadeIn(w3), FadeIn(s3), FadeIn(q, scale=0.5), run_time=0.7)
        self.finish()


class S23Take(SpokenScene):
    def construct(self):
        self.clear()
        cells = sheet(10, 1.0, 1.3, 0.62)
        l_one = lab("one sheet", BLUE, 40, weight=BOLD).move_to([0, 2.6, 0])
        self.at("One sheet")
        self.play(FadeIn(VGroup(*cells), lag_ratio=0.06), run_time=0.4)
        self.add(l_one)
        l_n = lab("neural", PURPLE, 40, weight=BOLD).move_to([-3.25, 2.6, 0])
        l_s = lab("skin", BLUE, 40, weight=BOLD).move_to([3.25, 2.6, 0])
        self.at("two fates")
        self.play(*[paint(c, PURPLE) for c in cells[:5]], ReplacementTransform(l_one, VGroup(l_n, l_s)), run_time=0.8)
        blk = RoundedRectangle(corner_radius=0.12, width=6.4, height=0.55, stroke_color=CREAM, stroke_width=3,
                               fill_color=CREAM, fill_opacity=0.85).move_to([-3.25, -0.85, 0])
        l_org = lab("organizer", CREAM, 32).move_to([-3.25, -1.6, 0])
        ups = VGroup(*[arr([-3.25 + dx, -0.5, 0], [-3.25 + dx, 0.25, 0], YELLOW, w=6, tip=0.2) for dx in (-2.6, -1.3, 0, 1.3, 2.6)])
        self.at("neighbors can")
        self.play(FadeIn(blk, shift=UP * 0.2), FadeIn(l_org), LaggedStart(*[GrowArrow(a) for a in ups], lag_ratio=0.1), run_time=0.9)
        nxt = VGroup(lab("Next: whose cells built the second back", TEXT, 34, font=TITLE_FONT),
                     lab("?", RED, 40, font=TITLE_FONT, weight=BOLD)).arrange(RIGHT, buff=0.08).move_to([0, -2.95, 0])
        self.at("Next")
        self.play(FadeIn(nxt, shift=UP * 0.15), run_time=0.7)
        self.finish()


class S24End(EndCard):
    LINE = "One sheet, two fates, and neighbours can decide which."
