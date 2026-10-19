"""Electron microscopy: seeing below the limit of light  (Biochemistrypedia methods film)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = light (the light wave, the light-microscope limit)
  BLUE   = the electron beam and the knife (the apparatus)
  GREY   = cells, membranes, tissue, de-emphasised text
  ORANGE = a liquid the tissue is put in (fixative, solvent, resin) and the vesicle tracer
  PURPLE = heavy metal (osmium, uranyl acetate, lead, the platinum-carbon replica, dark stain on a micrograph)
  ICE    = water and ice
  RED    = artefact, distortion, the pitfall
  GREEN  = a control
  GOLD   = dates and the closing rule
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
ICE = "#7F8CFF"
PANEL = "#D5D8DF"     # light 'micrograph' ground
INK = "#2B2140"       # dark stained features on the panel


# ---------------------------------------------------------------------------------------------
def lab(text, size=24, color=GREY, **kw):
    return T(text, size, color, **kw)


def stack(texts, colors=None, size=22, buff=0.1, align=ORIGIN):
    g = VGroup(*[T(t, size, (colors[i] if colors else TEXT)) for i, t in enumerate(texts)])
    return g.arrange(DOWN, buff=buff, aligned_edge=align)


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def poly(pts, color=YELLOW, w=5, closed=False):
    m = VMobject()
    pts = [np.array([p[0], p[1], 0.0]) for p in pts]
    if closed:
        pts = pts + [pts[0]]
    m.set_points_as_corners(pts)
    m.set_stroke(color, w)
    return m


def wave(x0, x1, y, amp, wl, color, w=5, n=400, phase=0.0):
    xs = np.linspace(x0, x1, n)
    return poly([[x, y + amp * np.sin(2 * np.pi * (x - x0) / wl + phase)] for x in xs], color, w)


def beaker(cx, cy, w=2.6, h=2.2, liquid=ORANGE, level=0.72, op=0.28):
    walls = poly([[cx - w / 2, cy + h / 2], [cx - w / 2, cy - h / 2], [cx + w / 2, cy - h / 2], [cx + w / 2, cy + h / 2]], GREY, 4)
    liq = Rectangle(width=w - 0.07, height=h * level - 0.04, stroke_width=0, fill_color=liquid, fill_opacity=op)
    liq.move_to([cx, cy - h / 2 + 0.035 + (h * level - 0.04) / 2, 0])
    return VGroup(liq, walls)


def tissue(cx, cy, w=1.0, h=0.7):
    body = RoundedRectangle(corner_radius=0.18, width=w, height=h, stroke_color=TEXT, stroke_width=2.5,
                            fill_color=GREY, fill_opacity=0.5)
    dots = VGroup(*[Circle(radius=0.07, stroke_width=1.5, stroke_color=TEXT, fill_color=GREY, fill_opacity=0.5)
                    .move_to([dx, dy, 0]) for dx, dy in [(-0.25, 0.1), (0.1, -0.12), (0.28, 0.12), (-0.05, 0.16), (-0.2, -0.17)]])
    g = VGroup(body, dots)
    g.scale(w / 1.0)
    return g.move_to([cx, cy, 0])


def sec_square(cx, cy, r, s=1.0, color=GREY, ring=TEXT, ring_op=0.5):
    sq = Rectangle(width=s, height=s, stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.18)
    ci = Circle(radius=r * s, stroke_color=ring, stroke_width=3, fill_color=ring, fill_opacity=0.10).set_stroke(opacity=ring_op)
    g = VGroup(sq, ci)
    g.ci = ci
    g.sq = sq
    return g.move_to([cx, cy, 0])


def clear(scene, t=0.5, keep=()):
    ms = [m for m in scene.mobjects if m not in keep]
    scene.play(*[FadeOut(m) for m in ms], run_time=t)


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Methods library"
    TITLE = "Seeing Below the Limit of Light"


# ---------------------------------------------------------------------------------------------
class S01Problem(SpokenScene):
    """two touching cells hide their gap under the light limit; a much shorter wavelength can ask for fine structure."""

    def construct(self):
        cy = 0.5
        cL = Circle(radius=1.5, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.14).move_to([-1.56, cy, 0])
        cR = Circle(radius=1.5, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.14).move_to([1.56, cy, 0])
        nl = lab("neuron", 26, GREY).move_to([-2.05, cy, 0])
        nr = lab("neuron", 26, GREY).move_to([2.05, cy, 0])
        cells = VGroup(cL, cR, nl, nr)

        self.at("A good light microscope")
        self.play(FadeIn(cells), run_time=0.7)
        self.at("resolves a little")
        disc = Circle(radius=0.95, stroke_color=YELLOW, stroke_width=4, fill_color=YELLOW, fill_opacity=0.22).move_to([0, cy, 0])
        disc_lbl = lab("light limit: a little over 200 nm", 26, YELLOW).move_to([0, -1.95, 0])
        self.play(GrowFromCenter(disc), FadeIn(disc_lbl, shift=UP * 0.1), run_time=0.7)

        self.at("Two neurons touching")
        q = chip("two cells, or one continuous network?", color=TEXT, size=26).move_to([0, 3.3, 0])
        self.play(FadeIn(q, shift=DOWN * 0.15), run_time=0.6)
        self.at("because the gap")
        gap_a = arr([0, 2.85, 0], [0, 1.45, 0], TEXT, w=4, tip=0.16)
        gap_l = lab("the gap", 26, TEXT).move_to([0, 2.5, 0])
        gap_l.next_to(gap_a, RIGHT, buff=0.15).shift(UP * 0.4)
        self.play(GrowArrow(gap_a), FadeIn(gap_l), run_time=0.5)
        self.at("far below that")
        far = lab("far below the limit", 26, TEXT).move_to([0, -2.6, 0])
        self.play(FadeIn(far, shift=UP * 0.1), run_time=0.5)

        # --- electrons: a much shorter wavelength
        self.at("Electrons have")
        old = VGroup(q, gap_a, gap_l, far, disc_lbl, nl, nr)
        small = VGroup(cL, cR, disc)
        wl_y = wave(-1.6, 6.2, 2.0, 0.5, 3.0, YELLOW, 5)
        wl_t = lab("light", 28, YELLOW).move_to([-1.6, 3.0, 0]).align_to(wl_y, LEFT)
        self.play(FadeOut(old), small.animate.scale(0.5).move_to([-4.6, 0.5, 0]),
                  Create(wl_y, rate_func=linear), FadeIn(wl_t), run_time=1.0)
        self.at("much shorter wavelength")
        we = wave(-1.6, 6.2, -0.3, 0.5, 0.5, BLUE, 4)
        we_t = lab("electrons: a much shorter wavelength", 28, BLUE).move_to([2.3, 0.6, 0])
        self.play(Create(we, rate_func=linear), FadeIn(we_t), run_time=1.2)

        self.at("fine structure")
        names = ["membranes", "junctions", "vesicles", "organelles"]
        chips = [chip(n, color=GREY, size=26) for n in names]
        row = VGroup(*chips).arrange(RIGHT, buff=0.3).move_to([0, -2.4, 0])
        head = lab("the fine structure of a cell:", 26, TEXT).next_to(row, UP, buff=0.35)
        self.play(FadeIn(head), run_time=0.4)
        self.at("membranes")
        self.play(FadeIn(chips[0], shift=UP * 0.1), run_time=0.3)
        self.at("junctions")
        self.play(FadeIn(chips[1], shift=UP * 0.1), run_time=0.3)
        self.at("vesicles")
        self.play(FadeIn(chips[2], shift=UP * 0.1), run_time=0.3)
        self.at("organelles")
        self.play(FadeIn(chips[3], shift=UP * 0.1), run_time=0.3)
        self.at("scale")
        nm = lab("at nanometre scale", 26, BLUE).next_to(row, DOWN, buff=0.3)
        self.play(FadeIn(nm), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Prepare(SpokenScene):
    """fix, dehydrate, embed: a piece of tissue moves through three baths and ends as a hard block."""

    def construct(self):
        xs = [-4.6, 0.0, 4.6]
        by = 0.55
        b1 = beaker(xs[0], by, w=3.2, h=2.7)
        b2 = beaker(xs[1], by, w=3.2, h=2.7, op=0.2)
        b3 = beaker(xs[2], by, w=3.2, h=2.7, op=0.38, level=0.8)
        ty = by - 0.45
        t = tissue(xs[0], ty, w=1.4)
        h1 = lab("1  Fix", 34, TEXT, weight=BOLD).move_to([xs[0], 3.05, 0])
        h2 = lab("2  Dehydrate", 34, TEXT, weight=BOLD).move_to([xs[1], 3.05, 0])
        h3 = lab("3  Embed", 34, TEXT, weight=BOLD).move_to([xs[2], 3.05, 0])

        self.at("First fix")
        self.play(FadeIn(b1), FadeIn(h1), FadeIn(t), run_time=0.6)
        self.at("mainly cross")
        l1 = lab("glutaraldehyde", 24, ORANGE).move_to([xs[0], -1.1, 0])
        l2 = lab("cross-links proteins", 22, GREY).move_to([xs[0], -1.5, 0])
        self.play(FadeIn(l1), FadeIn(l2), run_time=0.5)
        self.at("Osmium tetroxide")
        l3 = lab("osmium tetroxide", 24, PURPLE).move_to([xs[0], -2.05, 0])
        l4 = lab("reacts with lipids,", 22, GREY).move_to([xs[0], -2.45, 0])
        l5 = lab("adds electron density", 22, GREY).move_to([xs[0], -2.85, 0])
        self.play(FadeIn(l3), FadeIn(l4), FadeIn(l5), run_time=0.6)
        self.at("The fixative must diffuse")
        ins = VGroup(*[arr([xs[0] + dx * 1.15, ty + dy * 0.95, 0], [xs[0] + dx * 0.85, ty + dy * 0.68, 0], ORANGE, w=4, tip=0.12)
                       for dx, dy in [(-1, 0), (1, 0), (0, 1), (0, -1)]])
        self.play(*[GrowArrow(a) for a in ins], run_time=0.6)
        self.at("slow infiltration")
        ang = np.linspace(0, 2 * np.pi, 120)
        wob = poly([[xs[0] + (0.82 + 0.06 * np.sin(11 * a)) * np.cos(a) * 1.0, ty + (0.64 + 0.06 * np.sin(11 * a)) * np.sin(a)]
                    for a in ang], RED, 4)
        red = lab("may distort membranes", 24, RED).move_to([xs[0], 2.5, 0])
        self.play(FadeIn(wob), FadeIn(red), run_time=0.6)

        self.at("Then solvent")
        self.play(FadeOut(ins), FadeOut(wob), FadeOut(red), FadeOut(VGroup(l1, l2, l3, l4, l5)), run_time=0.4)
        self.play(FadeIn(b2), FadeIn(h2), run_time=0.4)
        mover = VGroup(t)
        self.play(mover.animate.shift(UP * 2.1), run_time=0.35)
        self.play(mover.animate.shift(RIGHT * 4.6), run_time=0.45)
        self.play(mover.animate.shift(DOWN * 2.1), run_time=0.35)
        s1 = lab("acetone or ethanol", 24, ORANGE).move_to([xs[1], -1.1, 0])
        self.play(FadeIn(s1), run_time=0.4)
        self.at("replaces the water")
        drops = VGroup(*[Circle(radius=0.07, stroke_width=0, fill_color=ICE, fill_opacity=0.95).move_to(
            [xs[1] + dx, ty + dy, 0]) for dx, dy in [(-0.4, 0.14), (0.0, -0.14), (0.4, 0.17), (-0.17, 0.24), (0.17, -0.25), (-0.4, -0.2)]])
        self.play(FadeIn(drops), run_time=0.3)
        s2 = lab("replaces the water", 22, ICE).move_to([xs[1], -1.5, 0])
        outs = [(-0.9, 0.3), (-0.6, 0.55), (0.9, 0.4), (0.5, 0.7), (0.9, -0.1), (-0.8, -0.3)]
        self.play(*[d.animate.shift(np.array([ox, oy, 0])).set_opacity(0) for d, (ox, oy) in zip(drops, outs)],
                  FadeIn(s2), run_time=1.2)

        self.at("Last resin")
        self.play(FadeIn(b3), FadeIn(h3), run_time=0.4)
        self.play(mover.animate.shift(UP * 2.1), run_time=0.35)
        self.play(mover.animate.shift(RIGHT * 4.6), run_time=0.45)
        self.play(mover.animate.shift(DOWN * 2.1), run_time=0.35)
        r1 = lab("resin soaks in", 24, ORANGE).move_to([xs[2], -1.1, 0])
        self.play(FadeIn(r1), run_time=0.4)
        self.at("hard plastic block")
        block = Rectangle(width=2.6, height=1.8, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.5)
        block.move_to([xs[2], ty, 0])
        r2 = lab("sets into a hard", 22, GREY).move_to([xs[2], -1.6, 0])
        r3 = lab("plastic block", 22, GREY).move_to([xs[2], -2.0, 0])
        self.play(FadeOut(b3[0]), FadeIn(block), FadeIn(r2), FadeIn(r3), run_time=0.8)
        mover.set_z_index(5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Section(SpokenScene):
    """block is cut into thin sections that lie in a ribbon on a grid; stain; the beam passes through; the image."""

    def construct(self):
        # --- cut
        by = 0.5
        block = Rectangle(width=2.6, height=1.5, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.5).move_to([-3.4, by, 0])
        cellb = Circle(radius=0.4, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.12).move_to([-3.4, by, 0])
        knife = Polygon([-1.95, by + 1.0, 0], [-1.95, by - 1.0, 0], [-1.45, by + 1.0, 0], stroke_color=BLUE, stroke_width=4,
                        fill_color=BLUE, fill_opacity=0.45)
        kl = lab("ultramicrotome", 26, BLUE).move_to([-3.4, 2.4, 0])
        self.at("An ultramicrotome")
        self.play(FadeIn(block), FadeIn(cellb), FadeIn(knife), FadeIn(kl), run_time=0.7)
        self.at("glass or diamond")
        kl2 = lab("glass or diamond knife", 24, BLUE).move_to([-3.4, 1.9, 0])
        self.play(FadeIn(kl2), knife.animate.set_fill(BLUE, 0.8), run_time=0.5)
        self.at("cuts sections")
        slabs = VGroup()
        for k in range(3):
            s = Rectangle(width=0.13, height=1.5, stroke_color=GREY, stroke_width=2, fill_color=TEXT, fill_opacity=0.5).move_to([-2.1, by, 0])
            slabs.add(s)
            self.play(s.animate.move_to([0.4 + 0.25 * k, by, 0]), run_time=0.55)
        self.at("nanometers thick")
        thick = lab("roughly 60 to 80 nm thick", 26, TEXT).move_to([1.3, -0.7, 0])
        pt = arr([0.45, -0.45, 0], [0.45, by - 0.78, 0], TEXT, w=3, tip=0.14)
        self.play(FadeIn(thick), GrowArrow(pt), run_time=0.5)

        # --- ribbon on a grid
        self.at("Serial sections")
        clear(self, 0.5)
        ry = 0.8
        gx = [-2.9, -1.45, 0.0, 1.45, 2.9]
        grid = VGroup(Rectangle(width=8.2, height=2.0, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.06).move_to([0, ry, 0]))
        for gxl in np.linspace(-4.0, 4.0, 17):
            grid.add(Line([gxl, ry - 1.0, 0], [gxl, ry + 1.0, 0], color=GREY, stroke_width=1).set_opacity(0.35))
        for gyl in np.linspace(ry - 0.9, ry + 0.9, 5):
            grid.add(Line([-4.1, gyl, 0], [4.1, gyl, 0], color=GREY, stroke_width=1).set_opacity(0.35))
        gl = lab("grid", 26, GREY).move_to([-3.5, ry - 1.4, 0])
        radii = [0.14, 0.31, 0.42, 0.3, 0.12]
        secs = [sec_square(x, ry, r, s=1.3, ring_op=0.45) for x, r in zip(gx, radii)]
        self.play(FadeIn(grid), FadeIn(gl), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(s) for s in secs], lag_ratio=0.25), run_time=1.2)
        rb = lab("a ribbon of serial sections", 26, TEXT).move_to([0.8, ry - 1.4, 0])
        self.play(FadeIn(rb), run_time=0.4)
        self.at("one cell can be followed")
        self.play(LaggedStart(*[s.ci.animate.set_stroke(TEXT, 5, 1.0).set_fill(TEXT, 0.35) for s in secs], lag_ratio=0.3), run_time=1.4)
        fl = lab("one cell, followed section to section", 26, TEXT).move_to([0, -1.55, 0])
        self.play(FadeIn(fl), run_time=0.4)

        # --- stain
        self.at("stained with")
        self.play(FadeOut(rb), FadeOut(fl), FadeOut(gl), run_time=0.3)
        c1 = chip("uranyl acetate", color=PURPLE, size=26).move_to([-2.4, 3.0, 0])
        a1 = arr([-2.4, 2.55, 0], [-1.45, ry + 0.8, 0], PURPLE, w=4, tip=0.15)
        self.play(FadeIn(c1), GrowArrow(a1), *[s.sq.animate.set_fill(PURPLE, 0.45).set_stroke(PURPLE, 3) for s in secs], run_time=0.8)
        self.at("then lead citrate")
        c2 = chip("lead citrate", color=PURPLE, size=26).move_to([2.4, 3.0, 0])
        a2 = arr([2.4, 2.55, 0], [1.45, ry + 0.8, 0], PURPLE, w=4, tip=0.15)
        self.play(FadeIn(c2), GrowArrow(a2), *[s.ci.animate.set_stroke(PURPLE, 6, 1.0).set_fill(PURPLE, 0.6) for s in secs], run_time=0.8)
        self.at("add contrast")
        ct = lab("add contrast", 28, PURPLE).move_to([0, -1.2, 0])
        self.play(FadeIn(ct), run_time=0.4)

        # --- beam through one section
        self.at("The beam passes")
        keep = secs[2]
        self.play(*[FadeOut(m) for m in self.mobjects if m is not keep], run_time=0.5)
        self.play(keep.animate.scale(1.7).move_to([0, 0.7, 0]), run_time=0.5)
        beam = Rectangle(width=3.0, height=0.35, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.5).move_to([0, 3.3, 0])
        bl = lab("electron beam", 26, BLUE).move_to([-3.6, 3.3, 0])
        ax = [-0.8, -0.4, 0.0, 0.4, 0.8]
        top = 0.7 + 1.1
        arrows = VGroup(*[arr([x, 3.1, 0], [x, top, 0], BLUE, w=4, tip=0.14) for x in ax])
        sl = lab("stained section", 26, PURPLE).move_to([-3.6, 0.7, 0])
        self.play(FadeIn(beam), FadeIn(bl), FadeIn(sl), *[GrowArrow(a) for a in arrows], run_time=0.8)
        pass_idx = [0, 2, 4]
        bot = 0.7 - 1.1
        pl_top = -1.55
        outs = VGroup(*[arr([ax[i], bot, 0], [ax[i], pl_top, 0], BLUE, w=4, tip=0.14) for i in pass_idx])
        self.play(*[GrowArrow(a) for a in outs], run_time=0.6)
        self.at("absorbed")
        ab = Circle(radius=0.09, stroke_width=0, fill_color=RED, fill_opacity=1).move_to([ax[1], top - 0.07, 0])
        abl = lab("absorbed", 26, RED).move_to([3.2, 1.9, 0])
        abk = Line([2.3, 1.9, 0], [ax[1] + 0.12, top - 0.07, 0], color=RED, stroke_width=2)
        self.play(FadeIn(ab, scale=2), FadeIn(abl), Create(abk), run_time=0.4)
        self.at("and scattered")
        sc = arr([ax[3], bot, 0], [ax[3] + 0.8, bot - 0.7, 0], RED, w=4, tip=0.14)
        scl = lab("scattered", 26, RED).move_to([3.0, -0.6, 0])
        self.play(GrowArrow(sc), FadeIn(scl), run_time=0.4)
        self.at("flat projection")
        panel = Rectangle(width=5.0, height=1.0, stroke_color=GREY, stroke_width=3, fill_color=PANEL, fill_opacity=1).move_to([0, -2.1, 0])
        spots = VGroup(*[Circle(radius=0.13, stroke_width=0, fill_color=INK, fill_opacity=0.95).move_to([x, -2.1, 0]) for x in (ax[1], ax[3])])
        pl = lab("image: a flat projection", 26, TEXT).move_to([-4.6, -2.1, 0])
        self.play(FadeIn(panel), FadeIn(spots), FadeIn(pl), run_time=0.7)
        self.at("of dead")
        dl = lab("a thin slice of dead, prepared tissue", 26, TEXT).move_to([0, -3.1, 0])
        self.play(FadeIn(dl), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Routes(SpokenScene):
    """three other routes: fast freezing, scanning surfaces, freeze-fracture replica."""

    def construct(self):
        xs = [-4.5, 0.0, 4.5]
        h1 = lab("Freezing", 30, TEXT, weight=BOLD).move_to([xs[0], 3.1, 0])
        h2 = lab("Scanning EM", 30, TEXT, weight=BOLD).move_to([xs[1], 3.1, 0])
        h3 = lab("Freeze-fracture", 30, TEXT, weight=BOLD).move_to([xs[2], 3.1, 0])

        # panel 1
        self.at("Freezing is another")
        self.play(FadeIn(h1), run_time=0.4)
        blob = Ellipse(width=2.4, height=1.7, stroke_color=TEXT, stroke_width=3, fill_color=GREY, fill_opacity=0.3).move_to([xs[0], 1.1, 0])
        wig = VGroup(*[poly([[xs[0] + dx + 0.1 * np.sin(5 * t + k), 1.1 + dy + t * 0.0] for t in np.linspace(-1, 1, 30)], GREY, 3)
                       for k, (dx, dy) in enumerate([(-0.0, 0.3), (0.0, 0.0), (0.0, -0.3)])])
        for k, w in enumerate(wig):
            pts = [[xs[0] + t * 0.7, 1.1 + (k - 1) * 0.3 + 0.08 * np.sin(8 * t + k)] for t in np.linspace(-1, 1, 40)]
            w.become(poly(pts, GREY, 3))
        self.play(FadeIn(blob), FadeIn(wig), run_time=0.5)
        self.at("pressure freezing")
        hp = lab("high-pressure freezing", 24, ICE).move_to([xs[0], -0.5, 0])
        self.play(FadeIn(hp), run_time=0.4)
        self.at("stops cell activity")
        self.play(blob.animate.set_fill(ICE, 0.5).set_stroke(ICE, 4), FadeOut(wig), run_time=0.6)
        n1 = lab("stops activity quickly", 24, TEXT).move_to([xs[0], -1.1, 0])
        self.play(FadeIn(n1), run_time=0.3)
        self.at("suppresses damaging")
        n2 = lab("suppresses damaging", 24, GREEN).move_to([xs[0], -1.9, 0])
        n3 = lab("ice crystals", 24, GREEN).move_to([xs[0], -2.3, 0])
        self.play(FadeIn(n2), FadeIn(n3), run_time=0.5)

        # panel 2
        self.at("Scanning electron microscopy")
        self.play(FadeIn(h2), run_time=0.4)
        prof = [[xs[1] + t, 0.4 + 0.45 * np.sin(2.1 * t) + 0.18 * np.sin(5.3 * t + 1)] for t in np.linspace(-1.8, 1.8, 120)]
        surf = poly(prof, GREY, 5)
        fill = Polygon(*[np.array([p[0], p[1], 0.0]) for p in prof], np.array([xs[1] + 1.8, -0.7, 0.0]), np.array([xs[1] - 1.8, -0.7, 0.0]),
                       stroke_width=0, fill_color=GREY, fill_opacity=0.25)
        self.play(FadeIn(fill), Create(surf), run_time=0.6)
        self.at("images surfaces")
        bm = arr([prof[0][0], prof[0][1] + 1.6, 0], [prof[0][0], prof[0][1] + 0.12, 0], BLUE, w=5, tip=0.16)
        tr = ValueTracker(0)

        def upd(m):
            i = int(tr.get_value() * (len(prof) - 1))
            x, y = prof[i]
            m.become(arr([x, y + 1.6, 0], [x, y + 0.12, 0], BLUE, w=5, tip=0.16))
        bm.add_updater(upd)
        self.add(bm)
        self.play(tr.animate.set_value(1.0), run_time=1.9, rate_func=linear)
        bm.remove_updater(upd)
        sn = lab("surfaces,", 24, TEXT).move_to([xs[1], -1.3, 0])
        sn2 = lab("not slices", 24, TEXT).move_to([xs[1], -1.7, 0])
        self.play(FadeIn(sn), FadeIn(sn2), run_time=0.4)

        # panel 3
        self.at("freeze fracture")
        self.play(FadeIn(h3), run_time=0.4)
        blk = Rectangle(width=3.0, height=1.4, stroke_color=ICE, stroke_width=3, fill_color=ICE, fill_opacity=0.35).move_to([xs[2], 0.6, 0])
        self.play(FadeIn(blk), run_time=0.3)
        jag = [[xs[2] - 1.5 + 0.375 * k, 1.3 + (0.22 if k % 2 else -0.05) + (0.1 if k in (3, 5) else 0)] for k in range(9)]
        fr = Polygon(*[np.array([p[0], p[1], 0.0]) for p in jag], np.array([xs[2] + 1.5, -0.1, 0.0]), np.array([xs[2] - 1.5, -0.1, 0.0]),
                     stroke_color=ICE, stroke_width=3, fill_color=ICE, fill_opacity=0.35)
        self.play(ReplacementTransform(blk, fr), run_time=0.7)
        fz = lab("frozen, then fractured", 22, ICE).move_to([xs[2], -0.55, 0])
        self.play(FadeIn(fz), run_time=0.3)
        self.at("carbon replica")
        rep = poly(jag, PURPLE, 6)
        rl = lab("platinum-carbon replica", 22, PURPLE).move_to([xs[2], 2.6, 0])
        self.play(Create(rep), FadeIn(rl), run_time=0.8)
        self.at("The replica")
        self.play(rep.animate.shift(UP * 0.55), fr.animate.set_opacity(0.15), FadeOut(fz), run_time=0.8)
        n4 = lab("the replica is imaged,", 24, PURPLE).move_to([xs[2], -1.3, 0])
        n5 = lab("not the tissue", 24, GREY).move_to([xs[2], -1.7, 0])
        self.play(FadeIn(n4), FadeIn(n5), run_time=0.4)
        self.at("planar views")
        n6 = lab("planar views of the internal", 22, TEXT).move_to([xs[2], -2.4, 0])
        n7 = lab("organisation of membranes", 22, TEXT).move_to([xs[2], -2.8, 0])
        self.play(FadeIn(n6), FadeIn(n7), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Reading(SpokenScene):
    """a schematic synapse read feature by feature: dark membranes, cleft, vesicles, thickened postsynaptic membrane."""

    def construct(self):
        px = -2.4
        GR = "#7B8191"
        panel = Rectangle(width=7.4, height=6.6, stroke_color=GREY, stroke_width=3, fill_color=PANEL, fill_opacity=1).move_to([px, 0, 0])
        tagl = T("schematic", 26, "#4B4F5C", weight=BOLD).move_to([px - 2.75, 3.0, 0])
        faint = 0.28
        pre = RoundedRectangle(corner_radius=0.7, width=6.6, height=2.5, stroke_color=INK, stroke_width=6, fill_color=INK, fill_opacity=0.10)
        pre.move_to([px, 1.25, 0])
        post = RoundedRectangle(corner_radius=0.7, width=6.6, height=2.5, stroke_color=INK, stroke_width=6, fill_color=INK, fill_opacity=0.10)
        post.move_to([px, -1.85, 0])
        pre_bot = 1.25 - 1.25
        post_top = -1.85 + 1.25
        mid = (pre_bot + post_top) / 2
        vs = VGroup()
        pts = [(-2.6, 0.38), (-2.0, 0.42), (-1.4, 0.34), (-0.8, 0.44), (-0.2, 0.36), (0.4, 0.42), (1.0, 0.34), (1.6, 0.4), (-2.3, 0.85), (-1.6, 0.9),
               (-0.9, 0.95), (-0.3, 0.85), (0.4, 0.92), (1.1, 0.85), (-1.9, 1.4), (-0.5, 1.5), (0.8, 1.4), (-1.2, 1.95), (0.2, 2.0)]
        for dx, y in pts:
            vs.add(Circle(radius=0.17, stroke_color=INK, stroke_width=3, fill_color=PANEL, fill_opacity=1).move_to([px + dx, y, 0]))
        thick = Rectangle(width=4.2, height=0.2, stroke_width=0, fill_color=INK, fill_opacity=1).move_to([px, post_top - 0.12, 0])
        pre.set_stroke(opacity=faint); post.set_stroke(opacity=faint)
        for v in vs:
            v.set_stroke(opacity=faint)
        thick.set_fill(opacity=faint)

        self.at("Here is a synapse")
        self.play(FadeIn(panel), FadeIn(tagl), FadeIn(pre), FadeIn(post), FadeIn(vs), FadeIn(thick), run_time=0.8)
        self.at("Dark is where")
        hm = lab("dark = heavy metal bound", 26, PURPLE).move_to([4.15, 3.05, 0])
        self.play(pre.animate.set_stroke(opacity=1.0), post.animate.set_stroke(opacity=1.0),
                  *[v.animate.set_stroke(opacity=1.0) for v in vs], thick.animate.set_fill(opacity=1.0), FadeIn(hm), run_time=0.9)

        LX = 1.85
        def col(texts, colors, y, size=22):
            g = stack(texts, colors, size=size, buff=0.08, align=LEFT)
            g.move_to([0, y, 0]).align_to([LX, 0, 0], LEFT)
            return g

        def leader(frm, to):
            return Line(frm, to, color=GR, stroke_width=2)

        self.at("stay separate")
        sep = col(["two separate membranes"], [TEXT], 0.85)
        e1 = leader([sep.get_left()[0] - 0.08, 0.85, 0], [px + 3.0, pre_bot - 0.02, 0])
        e2 = leader([sep.get_left()[0] - 0.08, 0.85, 0], [px + 3.0, post_top + 0.02, 0])
        self.play(FadeIn(sep), Create(e1), Create(e2), run_time=0.7)
        self.at("gap, not continuity")
        cl = col(["a cleft: a gap,", "not continuity"], [TEXT, TEXT], 0.25)
        self.play(FadeIn(cl), run_time=0.5)
        self.at("De Robertis and Bennett")
        dm = DoubleArrow([px + 2.2, pre_bot, 0], [px + 2.2, post_top, 0], buff=0, color=PURPLE, stroke_width=4, tip_length=0.1)
        m1 = col(["cleft 10 to 15 nm", "De Robertis and Bennett 1955"], [TEXT, GREY], -0.6)
        ml = leader([m1.get_left()[0] - 0.08, -0.5, 0], [px + 2.28, mid, 0])
        self.play(FadeIn(dm), FadeIn(m1), Create(ml), run_time=0.7)
        self.at("found about")
        m2 = col(["about 20 nm", "Palay 1956"], [TEXT, GREY], -1.55)
        self.play(FadeIn(m2), run_time=0.5)
        self.at("Small vesicles")
        vl = col(["small vesicles crowd", "the presynaptic side"], [TEXT, TEXT], 2.0)
        v_l = leader([vl.get_left()[0] - 0.08, 1.95, 0], [px + 1.75, 0.45, 0])
        self.play(FadeIn(vl), Create(v_l), Indicate(vs, color=PURPLE, scale_factor=1.0), run_time=0.8)
        self.at("membrane is thickened")
        pl = col(["thickened postsynaptic", "membrane"], [TEXT, TEXT], -2.75)
        p_l = leader([pl.get_left()[0] - 0.08, -2.65, 0], [px + 2.1, post_top - 0.14, 0])
        self.play(FadeIn(pl), Create(p_l), Indicate(thick, color=PURPLE, scale_factor=1.15), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Pitfalls(SpokenScene):
    """a fixation artefact in Bacillus cereus and its control; dead cells, few cells, and the controls for those."""

    def construct(self):
        def bacillus(cx, cy, pockets=False, color=GREY):
            body = RoundedRectangle(corner_radius=0.95, width=4.6, height=1.9, stroke_color=color, stroke_width=4,
                                    fill_color=color, fill_opacity=0.14).move_to([cx, cy, 0])
            g = VGroup(body)
            if pockets:
                for dx, dy, d in [(-1.3, 0.85, -1), (0.2, 0.85, -1), (-0.6, -0.85, 1), (1.2, -0.85, 1)]:
                    p = Circle(radius=0.27, stroke_color=RED, stroke_width=4, fill_color=RED, fill_opacity=0.25).move_to([cx + dx, cy + dy + d * 0.16, 0])
                    g.add(p)
            return g

        hd = lab("Bacillus cereus", 30, TEXT, slant=ITALIC).move_to([0, 3.35, 0])
        self.at("Fixation can create")
        self.play(FadeIn(hd), run_time=0.4)
        L = bacillus(-3.4, 2.0)
        R = bacillus(3.4, 2.0)
        Ll = lab("conventional fixation", 26, TEXT).move_to([-3.4, 0.65, 0])
        Rl = lab("freezing and", 26, TEXT).move_to([3.4, 0.75, 0])
        Rl2 = lab("freeze substitution", 26, TEXT).move_to([3.4, 0.35, 0])
        self.play(FadeIn(L), FadeIn(R), run_time=0.5)
        self.at("In Bacillus cereus")
        self.play(FadeIn(Ll), FadeIn(Rl), FadeIn(Rl2), run_time=0.5)
        self.at("conventional fixation gave")
        pk = bacillus(-3.4, 2.0, pockets=True)
        pkl = lab("pocket-like invaginations", 26, RED).move_to([-3.4, 0.0, 0])
        self.play(ReplacementTransform(L, pk), FadeIn(pkl), run_time=0.8)
        self.at("that were absent")
        ab = lab("absent", 26, GREEN).move_to([3.4, -0.1, 0])
        self.play(FadeIn(ab), run_time=0.5)
        self.at("The control is")
        ctl = chip("control: confirm with an independent preservation method", color=GREEN, size=26).move_to([0, -1.0, 0])
        self.play(FadeIn(ctl, shift=UP * 0.1), run_time=0.7)

        self.at("every cell")
        cells = VGroup(*[Circle(radius=0.38, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.14).move_to([-5.4 + 1.0 * k, -2.4, 0]) for k in range(3)])
        crosses = VGroup(*[T("✕", 30, RED, weight=BOLD).move_to(c) for c in cells])
        dl = lab("every cell imaged is dead", 24, RED).move_to([-4.4, -3.3, 0])
        self.play(FadeIn(cells), FadeIn(crosses), FadeIn(dl), run_time=0.7)
        self.at("few cells are imaged")
        fw = lab("few cells imaged in detail", 24, TEXT).move_to([-4.4 + 0.0, -3.3, 0])
        fw.move_to([-0.95, -2.4, 0])
        self.play(FadeIn(fw), run_time=0.5)
        self.at("so compare fixation methods")
        arrow = arr([1.2, -2.4, 0], [1.9, -2.4, 0], GREEN, w=5, tip=0.18)
        cm = stack(["compare fixation methods,", "examine many cells"], [GREEN, GREEN], size=26, align=LEFT, buff=0.1)
        cm.move_to([0, -2.4, 0]).align_to([2.1, 0, 0], LEFT)
        self.play(GrowArrow(arrow), FadeIn(cm), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07Unlocked1(SpokenScene):
    """ER and dense particles (Palade and Porter 1954, Palade 1955); vesicle recycling (Heuser and Reese 1973)."""

    def construct(self):
        # ---------- left: schematic reticulum
        lx = -3.5
        cyc = 1.2
        outline = RoundedRectangle(corner_radius=1.1, width=5.8, height=3.3, stroke_color=GREY, stroke_width=3,
                                   fill_color=GREY, fill_opacity=0.08).move_to([lx, cyc, 0])
        nuc = Circle(radius=0.62, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.2).move_to([lx - 1.7, cyc + 0.2, 0])
        sheets = VGroup()
        dots = VGroup()
        for k, y in enumerate([cyc + 0.95, cyc + 0.32, cyc - 0.3, cyc - 0.92]):
            x0, x1 = lx - 0.65 + (0.0 if k % 2 == 0 else 0.1), lx + 2.3
            xs = np.linspace(x0, x1, 80)
            ys = [y + 0.12 * np.sin(2.5 * (x - x0) + k) for x in xs]
            sheets.add(poly([[a, b] for a, b in zip(xs, ys)], TEXT, 4))
            for j in range(11):
                i = int(3 + j * 6.5)
                dots.add(Dot([xs[i], ys[i] + 0.12, 0], radius=0.06, color=PURPLE))
        tg = lab("schematic", 24, GREY, weight=BOLD).move_to([lx - 2.0, -0.7, 0])
        hl = lab("endoplasmic reticulum", 28, TEXT).move_to([lx, 3.3, 0])
        DY, SY = -2.55, -3.15
        self.at("In 1954")
        d1 = lab("1954", 30, GOLD, weight=BOLD).move_to([lx, DY, 0])
        self.play(FadeIn(outline), FadeIn(nuc), FadeIn(tg), FadeIn(d1), run_time=0.6)
        self.at("found the endoplasmic reticulum")
        self.play(Create(sheets, lag_ratio=0.3), FadeIn(hl), run_time=1.1)
        src1 = lab("Palade and Porter 1954", 22, GREY).move_to([lx, SY, 0])
        self.play(FadeIn(src1), run_time=0.3)
        self.at("In 1955")
        d2 = lab("1955", 30, GOLD, weight=BOLD).move_to([lx, DY, 0])
        self.play(ReplacementTransform(d1, d2), FadeOut(src1), run_time=0.4)
        self.at("dense particles")
        pl = lab("dense particles, 100 to 150 Å", 24, PURPLE).move_to([lx, -1.45, 0])
        self.play(FadeIn(dots, lag_ratio=0.05), FadeIn(pl), run_time=1.0)
        self.at("preferentially on its membranes")
        src2 = lab("Palade 1955", 22, GREY).move_to([lx, SY, 0])
        self.play(Indicate(dots, color=PURPLE, scale_factor=1.0), FadeIn(src2), run_time=0.8)

        # ---------- Heuser and Reese: the left panel leaves, this one fills the frame
        self.at("In 1973")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.5)
        hr = lab("frog neuromuscular junction", 28, TEXT).move_to([0, 3.62, 0])
        d3 = lab("1973", 28, GOLD, weight=BOLD).move_to([-1.3, -3.45, 0])
        src3 = lab("Heuser and Reese", 24, GREY).move_to([0.9, -3.45, 0])
        self.play(FadeIn(hr), FadeIn(d3), FadeIn(src3), run_time=0.4)
        sy = 1.55
        term = RoundedRectangle(corner_radius=0.5, width=8.0, height=1.5, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.08).move_to([0, sy, 0])
        vx = [-3.2 + 0.7 * k for k in range(7)]
        vy = [sy + (0.2 if k % 2 else -0.05) for k in range(7)]
        ves = VGroup(*[Circle(radius=0.17, stroke_color=TEXT, stroke_width=2.5, fill_color=TEXT, fill_opacity=0.2).move_to([x, y, 0]) for x, y in zip(vx, vy)])
        cist = Ellipse(width=1.5, height=0.36, stroke_color=TEXT, stroke_width=2.5, fill_color=TEXT, fill_opacity=0.2).move_to([3.0, sy - 0.1, 0])
        cl = lab("cisterna", 24, GREY).move_to([3.0, sy + 0.45, 0])
        self.at("stimulated frog")
        stim = chip("stimulate: 10 Hz", color=TEXT, size=26).move_to([-3.0, 2.85, 0])
        self.play(FadeIn(term), FadeIn(ves), FadeIn(cist), FadeIn(cl), FadeIn(stim, shift=DOWN * 0.1), run_time=0.6)
        self.at("and fixed samples")
        fx = lab("then fixed samples", 24, GREY).move_to([3.0, 2.85, 0])
        self.play(FadeIn(fx), run_time=0.4)
        base = -1.2
        ax0, ax1 = -1.6, 3.4
        axis = VGroup(Line([ax0, base, 0], [ax1, base, 0], color=GREY, stroke_width=3),
                      Line([ax0, base, 0], [ax0, base + 2.0, 0], color=GREY, stroke_width=3))
        yl = stack(["vesicle membrane", "depleted"], [GREY, GREY], size=24, align=RIGHT).move_to([-3.6, base + 1.0, 0])
        self.at("Membrane in vesicles")
        self.play(FadeIn(axis), FadeIn(yl), run_time=0.4)
        self.at("in vesicles fell")
        b1 = Rectangle(width=1.2, height=0.7, stroke_width=0, fill_color=RED, fill_opacity=0.8).move_to([ax0 + 1.1, base + 0.35, 0])
        t1 = lab("30%", 26, TEXT).next_to(b1, UP, buff=0.08)
        x1 = lab("1 min", 22, GREY).move_to([ax0 + 1.1, base - 0.3, 0])
        mv = VGroup(*[arr([vx[k], vy[k] + 0.2, 0], [vx[k], sy + 0.68, 0], GREY, w=3, tip=0.1) for k in (1, 3)])
        self.play(GrowFromEdge(b1, DOWN), FadeIn(t1), FadeIn(x1), ves[1].animate.set_opacity(0.15), ves[3].animate.set_opacity(0.15),
                  FadeIn(mv), run_time=0.8)
        self.at("minute")
        b2 = Rectangle(width=1.2, height=1.4, stroke_width=0, fill_color=RED, fill_opacity=0.8).move_to([ax0 + 3.0, base + 0.7, 0])
        t2 = lab("60%", 26, TEXT).next_to(b2, UP, buff=0.08)
        x2 = lab("15 min", 22, GREY).move_to([ax0 + 3.0, base - 0.3, 0])
        cm = arr([vx[0], sy - 0.62, 0], [2.2, sy - 0.62, 0], GREY, w=3, tip=0.12)
        self.play(GrowFromEdge(b2, DOWN), FadeIn(t2), FadeIn(x2), ves[5].animate.set_opacity(0.15), ves[2].animate.set_opacity(0.15),
                  GrowArrow(cm), run_time=0.8)
        self.at("and a tracer entered")
        tr = chip("stimulating: tracer in cisternae", color=ORANGE, size=24).move_to([-2.9, -2.4, 0])
        self.play(FadeIn(tr, shift=UP * 0.1), run_time=0.5)
        self.at("then vesicles")
        tr2 = chip("rest: tracer in vesicles", color=ORANGE, size=24).move_to([3.0, -2.4, 0])
        ar = arr([tr.get_right()[0] + 0.1, -2.4, 0], [tr2.get_left()[0] - 0.1, -2.4, 0], ORANGE, w=4, tip=0.14)
        self.play(GrowArrow(ar), FadeIn(tr2), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
class S08Unlocked2(SpokenScene):
    """apoptosis seen as distinct from necrosis (Kerr, Wyllie, Currie 1972); then the rule."""

    def construct(self):
        y = 0.7
        d = lab("1972", 30, GOLD, weight=BOLD).move_to([0, 3.3, 0])
        self.at("In 1972")
        self.play(FadeIn(d), run_time=0.4)

        def cell(cx, r, nuc_r, nuc_op):
            c = Circle(radius=r, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.14).move_to([cx, y, 0])
            n = Circle(radius=nuc_r, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=nuc_op).move_to([cx, y, 0])
            return VGroup(c, n)
        c0 = cell(-4.5, 1.3, 0.5, 0.15)
        l0 = lab("a cell", 26, GREY).move_to([-4.5, y - 1.8, 0])
        self.at("described apoptosis")
        self.play(FadeIn(c0), FadeIn(l0), run_time=0.6)
        self.at("distinct from necrosis")
        nec = lab("distinct from necrosis", 28, TEXT).move_to([0, 2.5, 0])
        self.play(FadeIn(nec), run_time=0.5)
        self.at("condensation")
        c1 = cell(-0.4, 0.85, 0.55, 0.55)
        a1 = arr([-2.9, y, 0], [-1.6, y, 0], GREY, w=5, tip=0.2)
        l1 = lab("condensation", 26, GREY).move_to([-0.4, y - 1.4, 0])
        self.play(GrowArrow(a1), TransformFromCopy(c0, c1), FadeIn(l1), run_time=0.9)
        self.at("breakup")
        a2 = arr([1.1, y, 0], [2.4, y, 0], GREY, w=5, tip=0.2)
        frs = VGroup()
        for dx, dy, rr in [(-0.7, 0.65, 0.4), (0.4, 0.8, 0.38), (0.95, -0.05, 0.42), (-0.45, -0.6, 0.38), (0.55, -0.8, 0.33)]:
            f = Circle(radius=rr, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.14).move_to([4.5 + dx, y + dy, 0])
            f.add(Circle(radius=rr * 0.5, stroke_width=0, fill_color=TEXT, fill_opacity=0.5).move_to(f.get_center()))
            frs.add(f)
        l2 = lab("breakup", 26, GREY).move_to([4.5, y - 1.8, 0])
        self.play(GrowArrow(a2), TransformFromCopy(c1, frs), FadeIn(l2), run_time=0.9)
        self.at("membrane")
        ml = lab("membrane-bound, well-preserved fragments", 26, TEXT).move_to([3.0, -2.15, 0])
        self.play(FadeIn(ml), run_time=0.6)
        src = lab("Kerr, Wyllie and Currie 1972", 24, GREY).move_to([-2.5, -2.85, 0])
        self.play(FadeIn(src), run_time=0.4)

        self.at("Keep this rule")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.6)
        rule = VGroup(T("Conventional electron microscopy", 38, TEXT), T("shows structure in dead, fixed tissue,", 38, TEXT), T("never motion.", 38, TEXT)).arrange(DOWN, buff=0.22)
        box = SurroundingRectangle(rule, color=GOLD, stroke_width=3, buff=0.45, corner_radius=0.2)
        head = lab("KEEP THIS RULE", 26, GOLD, weight=BOLD).next_to(box, UP, buff=0.25)
        extra = lab("Confirm a structure with an independent preservation method.", 26, GREEN).next_to(box, DOWN, buff=0.45)
        grp = VGroup(rule, box, head, extra).move_to([0, 0, 0])
        self.play(FadeIn(head), Create(box), run_time=0.5)
        self.at("electron microscopy shows")
        self.play(FadeIn(rule, shift=UP * 0.15), run_time=1.0)
        self.at("Confirm a structure")
        self.play(FadeIn(extra, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S09End(EndCard):
    LINE = "Conventional electron microscopy shows structure in dead, fixed tissue, never motion."
