"""Chapter 1: One Neuron, One Target (Neurotrophins, Trk Receptors and p75)

COLOR MAP (one color per concept, shared by every chapter of this lesson)
  BLUE    = the neurotrophin (NGF) itself, mature or precursor body
  ORANGE  = the pro-domain (the extra front stretch of proNGF)
  PINK    = Trk receptors (TrkA, TrkB, TrkC) and their kinase feet
  VIOLET  = p75 (and Fas, its death-receptor relative); the death domain
  YELLOW  = sortilin
  WHITE   = the cutting enzymes (scissors)
  GREEN   = survival
  RED     = death (apoptosis)
  SAND    = the partner proteins p75 uses (hexagons); Fas's partners are grey triangles
  GREY    = membrane, cells, outlines, unknowns, scope notes
  TEXT    = the rules, questions and highlights
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PINK = "#E879B9"
ORANGE = "#F29E4C"
VIOLET = "#A98BE0"
SAND = "#D8C3A0"
SCIS = "#FFFFFF"
PALE = "#C9CEDA"          # bright grey for captions that must be read
MY = -0.5                 # membrane height in the receptor scenes


# ---------------------------------------------------------------- helpers
def lab(text, color, x, y, size=26, **kw):
    return T(text, size, color, **kw).move_to([x, y, 0])


def arr(a, b, color=GREY, w=5):
    return Arrow(a, b, buff=0, color=color, stroke_width=w, tip_length=0.22,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=12)


def dasharr(a, b, color=GREY, w=5):
    d = DashedLine(a, b, color=color, stroke_width=w, dash_length=0.13)
    d.add_tip(tip_length=0.22)
    return d


def membrane(y=MY):
    return Rectangle(width=14.3, height=0.36, stroke_width=0, fill_color=GREY, fill_opacity=0.5).move_to([0, y, 0])


def inside(y=MY):
    top = y - 0.18
    h = top + 4.1
    return Rectangle(width=14.3, height=h, stroke_width=0, fill_color=GREY, fill_opacity=0.07).move_to([0, top - h / 2, 0])


def tails_of(cx, cy, s):
    return VGroup(*[RoundedRectangle(corner_radius=0.1 * s, width=0.26 * s, height=0.8 * s, stroke_color=ORANGE,
                                     stroke_width=3, fill_color=ORANGE, fill_opacity=0.7)
                    .move_to([cx + sx * 0.5 * s, cy + 0.695 * s, 0]) for sx in (-1, 1)])


def dimer(cx, cy, s=1.0, tails=False, color=BLUE):
    bodies = [Ellipse(width=0.95 * s, height=0.75 * s, stroke_color=color, stroke_width=3,
                      fill_color=color, fill_opacity=0.5).move_to([cx + sx * 0.5 * s, cy, 0]) for sx in (-1, 1)]
    g = VGroup(*bodies)
    g.bodies = VGroup(*bodies)
    g.tails = tails_of(cx, cy, s)
    if tails:
        g.add(*g.tails)
    return g


def ghost_dimer(cx, cy, s=1.0):
    """A faint dashed dimer with dashed tails: 'maybe there'."""
    parts = []
    for sx in (-1, 1):
        parts.append(DashedVMobject(Ellipse(width=0.95 * s, height=0.75 * s, stroke_color=BLUE, stroke_width=3.5)
                                    .move_to([cx + sx * 0.5 * s, cy, 0]), num_dashes=22))
        parts.append(DashedVMobject(RoundedRectangle(corner_radius=0.1 * s, width=0.26 * s, height=0.8 * s,
                                                     stroke_color=ORANGE, stroke_width=3.5)
                                    .move_to([cx + sx * 0.5 * s, cy + 0.695 * s, 0]), num_dashes=16))
    g = VGroup(*parts)
    g.set_stroke(opacity=0.8)
    return g


def cell(x, y, r=0.6, color=GREY, op=0.14, sw=4):
    body = Circle(radius=r, stroke_color=color, stroke_width=sw, fill_color=color, fill_opacity=op)
    nuc = Circle(radius=r * 0.36, stroke_width=0, fill_color=color, fill_opacity=0.45)
    g = VGroup(body, nuc).move_to([x, y, 0])
    g.body, g.nuc = body, nuc
    return g


def trk(x, y=MY, ecd=2.6, icd=1.3, w=0.7, foot_r=0.45):
    bar = RoundedRectangle(corner_radius=0.2, width=w, height=ecd + icd, stroke_color=PINK, stroke_width=3,
                           fill_color=PINK, fill_opacity=0.55).move_to([x, y + (ecd - icd) / 2, 0])
    foot = Circle(radius=foot_r, stroke_color=PINK, stroke_width=3, fill_color=PINK, fill_opacity=0.4).move_to(
        [x, y - icd - 0.3 * foot_r / 0.45, 0])
    g = VGroup(bar, foot)
    g.bar, g.foot = bar, foot
    return g


def stalk(x, y=MY, ecd=2.6, icd=0.9, color=VIOLET, op=0.55, w=0.7):
    """A plain receptor rod (p75 or Fas before the death domain is drawn)."""
    bar = RoundedRectangle(corner_radius=0.2, width=w, height=ecd + icd, stroke_color=color, stroke_width=3,
                           fill_color=color, fill_opacity=op).move_to([x, y + (ecd - icd) / 2, 0])
    g = VGroup(bar)
    g.bar = bar
    return g


def ddomain(x, y=MY, icd=0.9, op=0.95, k=1.0):
    """The death-domain block, hanging from the bottom of the rod."""
    return RoundedRectangle(corner_radius=0.25 * k, width=1.3 * k, height=0.9 * k, stroke_color=VIOLET, stroke_width=3,
                            fill_color=VIOLET, fill_opacity=op).move_to([x, y - icd - 0.45 * k, 0])


def p75(x, y=MY, ecd=2.6, icd=0.9, w=0.7, k=1.0, op=0.55, dd_op=0.95):
    """The one p75 glyph used from the death-domain scene on: rod plus death-domain block."""
    bar = stalk(x, y, ecd, icd, VIOLET, op, w).bar
    dd = ddomain(x, y, icd, dd_op, k)
    g = VGroup(bar, dd)
    g.bar, g.dd = bar, dd
    return g


def sortilin(x_bar, ym, cup_y, s=1.4, bottom=None, flip=False):
    """Yellow bar with a hook; cup_y = height of the hook's centre. flip puts the hook on the right."""
    r = 0.28 * s
    top = cup_y + r
    bot = ym - 1.0 if bottom is None else bottom
    bar = RoundedRectangle(corner_radius=0.12, width=0.26 * s, height=top - bot, stroke_color=YELLOW,
                           stroke_width=3, fill_color=YELLOW, fill_opacity=0.5).move_to([x_bar, (top + bot) / 2, 0])
    if flip:
        cup = Arc(radius=r, start_angle=PI / 2, angle=PI, stroke_color=YELLOW, stroke_width=8).move_to(
            [x_bar + 0.49 * s - r * 0.5, cup_y, 0])
    else:
        cup = Arc(radius=r, start_angle=-PI / 2, angle=PI, stroke_color=YELLOW, stroke_width=8).move_to(
            [x_bar - 0.49 * s + r * 0.5, cup_y, 0])
    g = VGroup(bar, cup)
    g.bar, g.cup = bar, cup
    return g


def clamp_parts(xc, ym, s, ecd, icd=0.7, k=1.0, tails=True):
    """proNGF, p75 and sortilin laid out so p75 touches the body and sortilin's hook grips a pro-domain."""
    cy = ym + ecd + 0.375 * s
    d = dimer(xc, cy, s, tails=tails)
    p = p75(xc - 0.5 * s, ym, ecd=ecd, icd=icd, w=0.26 * s * 1.8, k=k)
    so = sortilin(xc + 0.5 * s + 0.66 * s, ym, cy + 0.695 * s, s, bottom=ym - icd - 0.5 * k)
    return d, p, so, cy


def skull(x, y, s=1.0, color=RED):
    head = Circle(radius=0.45 * s, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.25)
    jaw = RoundedRectangle(corner_radius=0.06 * s, width=0.5 * s, height=0.28 * s, stroke_color=color, stroke_width=4,
                           fill_color=color, fill_opacity=0.25).move_to([0, -0.5 * s, 0])
    eyes = VGroup(*[Circle(radius=0.11 * s, stroke_width=0, fill_color=color, fill_opacity=1).move_to([sx * 0.18 * s, 0.05 * s, 0])
                    for sx in (-1, 1)])
    teeth = VGroup(*[Line([sx * 0.1 * s, -0.4 * s, 0], [sx * 0.1 * s, -0.62 * s, 0], color=color, stroke_width=3) for sx in (-1, 1)])
    return VGroup(head, jaw, eyes, teeth).move_to([x, y, 0])


def scissors(x, y, s=1.0):
    a = Line([-0.55 * s, -0.32 * s, 0], [0.85 * s, 0.2 * s, 0], color=SCIS, stroke_width=6)
    b = Line([-0.55 * s, 0.32 * s, 0], [0.85 * s, -0.2 * s, 0], color=SCIS, stroke_width=6)
    h = VGroup(*[Circle(radius=0.17 * s, stroke_color=SCIS, stroke_width=5).move_to([-0.62 * s, sy * 0.33 * s, 0]) for sy in (-1, 1)])
    g = VGroup(a, b, h).move_to([x, y, 0])
    g.a, g.b = a, b
    return g


def snip(scene, sc, t=0.15):
    """Close and reopen the scissors blades in place."""
    sa, ea = sc.a.get_start(), sc.a.get_end()
    sb, eb = sc.b.get_start(), sc.b.get_end()
    mid = (ea + eb) / 2
    scene.play(sc.a.animate.put_start_and_end_on(sa, mid + DOWN * 0.01), sc.b.animate.put_start_and_end_on(sb, mid + UP * 0.01), run_time=t)
    scene.play(sc.a.animate.put_start_and_end_on(sa, ea), sc.b.animate.put_start_and_end_on(sb, eb), run_time=t)


GANG_X, GANG_K = -3.7, 1.2


def neuron_cluster(cx=GANG_X, k=GANG_K):
    """The ganglion: a highlighted neuron at the right edge of a cluster of cell bodies (scenes 3 to 5)."""
    rows = {0.0: [-2, -1, 0, 1], 0.87: [-1.5, -0.5, 0.5, 1.5], -0.87: [-1.5, -0.5, 0.5, 1.5], 1.74: [-1, 0, 1], -1.74: [-1, 0, 1]}
    others = VGroup(*[cell(cx + dx * k, dy * k, 0.5 * k / 1.2) for dy, dxs in rows.items() for dx in dxs])
    hl = cell(cx + 2.0 * k, 0.0, 0.55 * k / 1.2, TEXT, 0.25, 6)
    return hl, others


def vessel():
    """A short wavy tube: the target's blood vessel."""
    ys = np.linspace(2.6, -2.0, 60)
    left = [[5.0 + 0.16 * np.sin(2.4 * y), y, 0] for y in ys]
    right = [[6.1 + 0.16 * np.sin(2.4 * y), y, 0] for y in ys]
    pts = left + right[::-1]
    v = VMobject(stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.16)
    v.set_points_as_corners(pts + [pts[0]])
    return v


def axon_curve():
    return CubicBezier(np.array([-0.75, 0, 0]), np.array([0.8, 1.0, 0]), np.array([2.6, -1.0, 0]), np.array([4.95, 0, 0]),
                       stroke_color=GREY, stroke_width=6)


def vessel_labels():
    tl = lab("target", PALE, 5.55, 3.1, 30)
    bl = VGroup(T("blood vessel", 28, PALE), T("or gland", 28, PALE)).arrange(DOWN, buff=0.1).move_to([5.55, -2.85, 0])
    return tl, bl


# two dishes: r 2.3, dimers sit inside the dish top, labels above and results below
DY_D, R_D = -0.55, 2.3
DISH_POS = [(-1.05, 0.25), (1.05, 0.2), (-0.85, -1.0), (0.85, -1.05), (0.0, -0.4)]
DIMER_DY = 1.3
LABEL_Y = 2.3
RES_Y = -3.3
TOP_Y = 3.45


def dish(x, y=DY_D, r=R_D):
    d = Circle(radius=r, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.07).move_to([x, y, 0])
    cells = VGroup(*[cell(x + dx, y + dy, 0.4, GREY, 0.2, 4) for dx, dy in DISH_POS])
    g = VGroup(d, cells)
    g.dish, g.cells = d, cells
    return g


def frags(x, y, r=0.6):
    return VGroup(*[Dot([x + r * np.cos(a), y + r * np.sin(a), 0], radius=0.05, color=RED) for a in (0.5, 2.2, 3.9, 5.4)])


def target_block(x, y, w=2.4, h=3.0, size=32):
    box = RoundedRectangle(corner_radius=0.3, width=w, height=h, stroke_color=GREY, stroke_width=4,
                           fill_color=GREY, fill_opacity=0.2).move_to([x, y, 0])
    return VGroup(box, lab("target", GREY, x, y, size))


def hexa(color=SAND, r=0.26):
    return RegularPolygon(6, radius=r, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.6)


def tri(color=GREY, r=0.3):
    return Triangle(stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.6).scale(r)


def grey_dot(pos):
    return Circle(radius=0.22, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.6).move_to(pos)


# ---------------------------------------------------------------- scenes
class S00Title(TitleCard):
    LESSON = "Neurotrophins, Trk Receptors and p75"
    TITLE = "One Neuron, One Target"


class S01(SpokenScene):
    def construct(self):
        A, B = cell(-3.4, 0.0, 1.5, GREY, 0.14, 5), cell(3.4, 0.0, 1.5, GREY, 0.14, 5)
        d1 = dimer(-3.4, 3.1, 0.8)
        d2 = dimer(3.4, 3.1, 0.8)
        self.play(FadeIn(A), FadeIn(B), FadeIn(d1), run_time=0.7)
        self.at("keep a neuron")
        self.play(d1.animate.move_to([-3.4, 1.85, 0]), run_time=0.6)
        alive = lab("alive", GREEN, -3.4, -2.1, 38)
        self.play(A.body.animate.set_stroke(GREEN), FadeIn(alive), run_time=0.5)
        self.at("How can the same")
        q = lab("How can the same factor kill another cell?", TEXT, 0, -3.3, 32)
        self.play(FadeIn(q), FadeIn(d2), run_time=0.5)
        self.at("same factor")
        self.play(d2.animate.move_to([3.4, 1.85, 0]), run_time=0.6)
        self.at("kill another cell")
        fr = VGroup(*[Dot([3.4 + 1.25 * np.cos(a), 0.0 + 1.25 * np.sin(a), 0], radius=0.08, color=RED) for a in np.linspace(0.3, 6.0, 7)])
        dies = lab("dies", RED, 3.4, -2.1, 38)
        self.play(B.animate.scale(0.7).set_color(RED), d2.animate.move_to([3.4, 1.4, 0]), FadeIn(fr, scale=0.6),
                  FadeIn(dies), run_time=0.8)
        self.finish()


class S02(SpokenScene):
    def construct(self):
        ys = [2.2, 0.75, -0.7, -2.15]
        cells = [cell(-4.9, y, 0.6) for y in ys]
        axons = [Line([-4.3, y, 0], [2.6, y, 0], color=GREY, stroke_width=6) for y in ys]
        head = lab("recap: the rule from the last lesson", PALE, 0, 3.5, 28)
        self.play(FadeIn(head), *[FadeIn(c) for c in cells], *[Create(a) for a in axons], run_time=1.0)
        self.at("A target makes")
        tb = target_block(5.4, 0, 2.4, 6.2)
        self.play(FadeIn(tb), run_time=0.6)
        self.at("a limited amount")
        d = [dimer(4.5, 2.2, 0.55), dimer(4.5, 0.75, 0.55)]
        self.play(*[FadeIn(x) for x in d], run_time=0.4)
        self.play(*[x.animate.shift(LEFT * 1.0) for x in d], run_time=0.8)
        self.at("survival factor")
        sf = lab("survival factor", BLUE, 2.0, 2.92, 28)
        ld = Line([3.1, 2.7, 0], [3.5, 2.45, 0], color=BLUE, stroke_width=3)
        self.play(FadeIn(sf), Create(ld), run_time=0.5)
        self.at("Neurons that fail")
        self.play(*[Indicate(cells[i], color=TEXT, scale_factor=1.25) for i in (2, 3)], run_time=0.8)
        self.at("get enough")
        self.play(*[cells[i].body.animate.set_stroke(RED) for i in (2, 3)],
                  *[cells[i].animate.set_opacity(0.3) for i in (2, 3)],
                  *[axons[i].animate.set_opacity(0.25) for i in (2, 3)],
                  axons[0].animate.put_start_and_end_on([-4.3, 2.2, 0], [2.85, 2.2, 0]),
                  axons[1].animate.put_start_and_end_on([-4.3, 0.75, 0], [2.85, 0.75, 0]), run_time=1.0)
        self.finish()


def neck_icon():
    head = Circle(radius=1.5, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.1).move_to([4.3, 1.4, 0])
    neck = Rectangle(width=1.1, height=1.6, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.1).move_to([4.3, -0.7, 0])
    gang = Ellipse(width=0.8, height=0.55, stroke_color=TEXT, stroke_width=4, fill_color=TEXT, fill_opacity=0.35).move_to([4.3, -0.6, 0])
    return head, neck, gang


class S03(SpokenScene):
    def construct(self):
        hl, others = neuron_cluster(0.0, 1.5)
        cc = VGroup(hl, others).get_center()
        others.shift(-cc)
        hl.shift(-cc)
        both = VGroup(hl, others)
        self.play(FadeIn(others, lag_ratio=0.05), FadeIn(hl, scale=0.5), run_time=0.8)
        self.at("sympathetic neuron")
        nl = lab("sympathetic\nneuron", TEXT, 5.4, 0.0, 30)
        ld = Line(hl.get_right() + RIGHT * 0.05, [4.3, 0.0, 0], color=TEXT, stroke_width=3)
        self.play(FadeIn(nl), Create(ld), Indicate(hl, color=TEXT, scale_factor=1.3), run_time=0.7)
        self.at("cluster of nerve")
        self.play(Indicate(others, color=PALE, scale_factor=1.06), run_time=0.8)
        self.at("in the neck")
        target_center = VGroup(*neuron_cluster()).get_center()
        head, neck, gang = neck_icon()
        for m in (head, neck):
            m.set_stroke(PALE, 5).set_fill(GREY, 0.22)
        gl = lab("superior cervical ganglion", TEXT, GANG_X, -3.2, 28)
        nkl = lab("neck", PALE, 5.75, -0.7, 28)
        self.play(FadeOut(nl), FadeOut(ld), both.animate.scale(0.8).move_to(target_center),
                  FadeIn(head), FadeIn(neck), FadeIn(gang), FadeIn(nkl), FadeIn(gl), run_time=0.6)
        link = DashedLine([-0.5, -0.1, 0], [3.8, -0.6, 0], color=TEXT, stroke_width=4)
        self.play(Create(link), run_time=0.4)
        self.finish()


class S04(SpokenScene):
    def construct(self):
        hl, others = neuron_cluster()
        gl = lab("superior cervical ganglion", TEXT, GANG_X, -3.2, 28)
        self.add(hl, others, gl)
        ax, tube = axon_curve(), vessel()
        tl, bl = vessel_labels()
        self.at("Its axon")
        self.play(Create(ax), run_time=1.4)
        self.at("to a target")
        self.play(FadeIn(tube), FadeIn(tl), run_time=0.5)
        self.at("blood vessel")
        self.play(FadeIn(bl), run_time=0.5)
        self.finish()


class S05(SpokenScene):
    def construct(self):
        hl, others = neuron_cluster()
        gl = lab("superior cervical ganglion", TEXT, GANG_X, -3.2, 28)
        ax, tube = axon_curve(), vessel()
        tl, bl = vessel_labels()
        self.add(hl, others, gl, ax, tube, tl, bl)
        self.at("The target makes")
        ds = [dimer(4.75, 1.3, 0.7), dimer(4.75, -1.2, 0.7), dimer(4.75, -2.0, 0.7)]
        self.play(*[FadeIn(x) for x in ds], run_time=0.3)
        self.play(ds[0].animate.move_to([3.4, 1.3, 0]), ds[1].animate.move_to([2.9, -1.2, 0]),
                  ds[2].animate.move_to([3.7, -2.0, 0]), run_time=1.0)
        self.at("nerve growth factor")
        nl = lab("nerve growth factor (NGF)", BLUE, 1.5, 2.45, 30)
        ld = Line([2.9, 2.2, 0], [3.3, 1.65, 0], color=BLUE, stroke_width=3)
        self.play(FadeIn(nl), Create(ld), run_time=0.6)
        self.finish()


GRID = [(-3.4, 1.9), (3.4, 1.9), (-3.4, -1.5), (3.4, -1.5)]
NAMES = [("NGF", "nerve growth factor"), ("BDNF", "brain-derived\nneurotrophic factor"),
         ("NT-3", "neurotrophin 3"), ("NT-4", "neurotrophin 4")]


def grid_dimers(s=1.7):
    return [dimer(x, y, s) for x, y in GRID]


def name_tag(i, x, y):
    ab, fn = NAMES[i]
    g = VGroup(T(ab, 34, BLUE, weight=BOLD), T(fn, 24, GREY, line_spacing=0.6)).arrange(DOWN, buff=0.12)
    return g.move_to([x, y, 0])


class S06(SpokenScene):
    def construct(self):
        ds = grid_dimers()
        self.add(ds[0])
        self.play(Indicate(ds[0], color=BLUE, scale_factor=1.08), run_time=0.8)
        self.at("one of four")
        for d in ds[1:]:
            self.play(FadeIn(d, scale=0.6), run_time=0.25)
        self.at("neurotrophins")
        h = lab("neurotrophins", BLUE, 0, 3.4, 36)
        self.play(FadeIn(h), run_time=0.5)
        self.finish()


class S07(SpokenScene):
    def construct(self):
        ds = grid_dimers()
        h = lab("neurotrophins", BLUE, 0, 3.4, 36)
        self.add(*ds, h)
        cues = ["NGF", "Brain Derived", "Neurotrophin 3", "Neurotrophin 4"]
        for i in range(4):
            self.at(cues[i])
            x, y = GRID[i]
            self.play(FadeIn(name_tag(i, x, y - 1.3)), Indicate(ds[i], color=BLUE), run_time=0.8)
        self.finish()


class S08(SpokenScene):
    def construct(self):
        ds = grid_dimers()
        ab = [lab(NAMES[i][0], BLUE, x, y - 1.1, 34) for i, (x, y) in enumerate(GRID)]
        h = lab("neurotrophins", BLUE, 0, 3.4, 36)
        self.add(*ds, *ab, h)
        self.play(FadeOut(h), run_time=0.2)
        dl = lab("each one a dimer", TEXT, 0, 3.4, 38)
        self.play(FadeIn(dl), run_time=0.2)
        self.at("a dimer")
        # slow split: the two chains take slightly different tints while apart
        A_T, B_T = "#3E8FB8", "#8FE3F4"
        self.play(*[d.bodies[0].animate.shift(LEFT * 0.6).set_fill(A_T, 0.6).set_stroke(A_T) for d in ds],
                  *[d.bodies[1].animate.shift(RIGHT * 0.6).set_fill(B_T, 0.6).set_stroke(B_T) for d in ds], run_time=0.9)
        self.at("held together")
        self.play(*[d.bodies[0].animate.shift(RIGHT * 0.6).set_fill(BLUE, 0.5).set_stroke(BLUE) for d in ds],
                  *[d.bodies[1].animate.shift(LEFT * 0.6).set_fill(BLUE, 0.5).set_stroke(BLUE) for d in ds], run_time=0.8)
        self.at("share one fold")
        box = DashedVMobject(RoundedRectangle(corner_radius=0.3, width=11.6, height=5.8, stroke_color=TEXT, stroke_width=3).move_to([0, -0.1, 0]), num_dashes=70)
        bt = lab("one shared fold", TEXT, 0, -3.5, 30)
        self.play(Create(box), FadeIn(bt), run_time=0.8)
        self.finish()


TRK_X, P75_X = -2.7, 2.7


class S09(SpokenScene):
    def construct(self):
        ds = grid_dimers()
        ab = [lab(NAMES[i][0], BLUE, x, y - 1.1, 34) for i, (x, y) in enumerate(GRID)]
        old = VGroup(*ds, *ab)
        axon = Line([-6.8, -0.5, 0], [-1.6, -0.5, 0], color=GREY, stroke_width=14)
        tip = Circle(radius=2.3, stroke_color=GREY, stroke_width=7, fill_color=GREY, fill_opacity=0.2).move_to([0, -0.5, 0])
        tipg = VGroup(axon, tip)
        atl = lab("axon tip", PALE, 0, 2.2, 32)
        self.add(old)
        self.play(FadeOut(old, shift=UP * 0.4), FadeIn(tipg), FadeIn(atl), run_time=0.6)
        self.at("two kinds")
        mem, cyt = membrane(), inside()
        t, p = trk(TRK_X), stalk(P75_X)
        t.set_opacity(0)
        p.set_opacity(0)
        self.add(t, p)
        tl, pl = lab("Trk", PINK, TRK_X, 2.55, 40), lab("p75", VIOLET, P75_X, 2.55, 40)
        self.play(tipg.animate.scale(2.5, about_point=[0, -0.5, 0]).set_opacity(0), FadeOut(atl), FadeIn(mem), FadeIn(cyt),
                  t.animate.set_opacity(1), p.animate.set_opacity(1), FadeIn(tl), FadeIn(pl), run_time=0.7)
        self.finish()


class S10(SpokenScene):
    def construct(self):
        mem, cyt = membrane(), inside()
        t1, p = trk(TRK_X), stalk(P75_X)
        l1, pl = lab("Trk", PINK, TRK_X, 2.55, 40), lab("p75", VIOLET, P75_X, 2.55, 40)
        self.add(cyt, mem, t1, p, l1, pl)
        self.play(FadeOut(p), FadeOut(pl), t1.animate.shift(LEFT * 1.3), l1.animate.shift(LEFT * 1.3), run_time=0.5)
        t2, t3 = trk(0.0), trk(4.0)
        self.at("three track")
        self.play(FadeIn(t2), FadeIn(t3), run_time=0.4)
        self.at("track receptors")
        note = VGroup(T("Trk", 34, PINK, weight=BOLD), T("is said", 26, GREY), T("track", 34, PINK, weight=BOLD)).arrange(RIGHT, buff=0.2).move_to([0, 3.4, 0])
        self.play(FadeIn(note), run_time=0.5)
        names = [lab(n, PINK, x, 2.55, 40) for n, x in zip(("TrkA", "TrkB", "TrkC"), (-4.0, 0.0, 4.0))]
        self.at("track a")
        self.play(ReplacementTransform(l1, names[0]), run_time=0.3)
        self.at("track b")
        self.play(FadeIn(names[1]), run_time=0.25)
        self.at("track c")
        self.play(FadeIn(names[2]), run_time=0.25)
        self.finish()


def trk_row():
    mem, cyt = membrane(), inside()
    rs = [trk(x) for x in (-4.0, 0.0, 4.0)]
    names = [lab(n, PINK, x, 2.55, 40) for n, x in zip(("TrkA", "TrkB", "TrkC"), (-4.0, 0.0, 4.0))]
    return mem, cyt, rs, names


class S11(SpokenScene):
    def construct(self):
        mem, cyt, rs, names = trk_row()
        note = VGroup(T("Trk", 34, PINK, weight=BOLD), T("is said", 26, GREY), T("track", 34, PINK, weight=BOLD)).arrange(RIGHT, buff=0.2).move_to([0, 3.4, 0])
        self.add(cyt, mem, *rs, *names, note)
        self.at("receptor tyrosine")
        head = lab("receptor tyrosine kinase", PINK, 0, 3.4, 36)
        self.play(FadeOut(note), FadeIn(head), run_time=0.5)
        self.at("kinase")
        glows = [Circle(radius=0.6, stroke_width=0, fill_color=PINK, fill_opacity=0.35).move_to(r.foot.get_center()) for r in rs]
        kl = [lab("kinase domain", PINK, r.foot.get_x(), -2.95, 26) for r in rs]
        self.play(*[FadeIn(g) for g in glows], *[r.foot.animate.set_fill(PINK, 1.0) for r in rs], *[FadeIn(k) for k in kl], run_time=0.8)
        self.at("prefers")
        d = dimer(-2.0, 0.6, 1.3)
        q = lab("?", TEXT, -2.0, 2.0, 90)
        self.play(FadeOut(head), FadeIn(d, shift=DOWN * 0.2), FadeIn(q), run_time=0.4)
        self.at("particular")
        self.play(d.animate.shift(RIGHT * 4.0), q.animate.shift(RIGHT * 4.0), run_time=0.7)
        self.at("factors")
        self.play(Indicate(d, color=BLUE, scale_factor=1.2), run_time=0.7)
        self.at("chapter 2")
        ch = lab("Chapter 2 matches factors to receptors", PALE, 0, -3.55, 30)
        self.play(FadeOut(d), FadeOut(q), FadeIn(ch), run_time=0.6)
        self.finish()


P75A = -1.2   # p75's place while the four factors dock on it


class S12(SpokenScene):
    def construct(self):
        mem, cyt, rs, names = trk_row()
        for r in rs:
            r.foot.set_fill(PINK, 1.0)
        glows = [Circle(radius=0.6, stroke_width=0, fill_color=PINK, fill_opacity=0.35).move_to(r.foot.get_center()) for r in rs]
        kl = [lab("kinase domain", PINK, r.foot.get_x(), -2.95, 26) for r in rs]
        ch = lab("Chapter 2 matches factors to receptors", PALE, 0, -3.55, 30)
        old = VGroup(*rs, *names, *glows, *kl, ch)
        self.add(cyt, mem, old)
        p = stalk(P75A)
        self.play(FadeOut(old), FadeIn(p), run_time=0.5)
        self.at("p75")
        pl = lab("p75", VIOLET, P75A + 1.2, 0.6, 40)
        self.play(FadeIn(pl), run_time=0.3)
        xs = (-5.3, -2.6, 0.1, 2.8)
        ds = [dimer(x, 3.3, 0.7) for x in xs]
        lbs = [lab(NAMES[i][0], BLUE, xs[i] + 1.35, 3.3, 26) for i in range(4)]
        lns = [Line([x + 0.1, 2.9, 0], [P75A, 2.15, 0], color=VIOLET, stroke_width=3) for x in xs]
        for i, cue in enumerate(["binds", "all", "four", "factors"]):
            self.at(cue)
            self.play(FadeIn(ds[i]), FadeIn(lbs[i]), Create(lns[i]), run_time=0.3)
        self.at("and it has")
        lit = Circle(radius=0.55, stroke_color=PINK, stroke_width=3, fill_color=PINK, fill_opacity=1.0).move_to([3.4, -1.7, 0])
        lg = Circle(radius=0.75, stroke_width=0, fill_color=PINK, fill_opacity=0.35).move_to(lit.get_center())
        tl = lab("a Trk kinase", PINK, 3.4, -2.75, 28)
        self.play(FadeIn(lg), FadeIn(lit), FadeIn(tl), run_time=0.4)
        self.at("it has")
        ghost = DashedVMobject(Circle(radius=0.55, stroke_color=TEXT, stroke_width=4).move_to([P75A, -1.7, 0]), num_dashes=16)
        nk = lab("no kinase", TEXT, P75A, -2.7, 34, weight=BOLD)
        self.play(FadeIn(ghost), FadeIn(nk), run_time=0.4)
        self.finish()


PX, FX = -3.0, 3.0   # p75 and Fas positions in scenes 13 to 16


def fas_rod(op=0.3):
    f = stalk(FX, ecd=2.2, icd=0.9, op=op)
    f.bar.set_stroke(VIOLET, opacity=0.55)
    return f


def base_pair():
    mem, cyt = membrane(), inside()
    p = stalk(PX)
    f = fas_rod()
    ls = VGroup(lab("p75", VIOLET, PX, 2.6, 40), lab("Fas", VIOLET, FX, 2.6, 40), lab("death receptor", PALE, FX + 1.9, 1.0, 26))
    return mem, cyt, p, f, ls


class S13(SpokenScene):
    def construct(self):
        mem, cyt = membrane(), inside()
        p = stalk(P75A)
        pl = lab("p75", VIOLET, P75A + 1.2, 0.6, 40)
        self.add(cyt, mem, p, pl)
        _, _, p2, f, ls = base_pair()
        self.play(p.animate.move_to([PX, p.get_y(), 0]), FadeOut(pl), FadeIn(ls[0]), run_time=0.6)
        self.at("relative of")
        self.play(FadeIn(f), run_time=0.5)
        self.play(FadeIn(ls[1]), run_time=0.4)
        br = VGroup(Line([PX, 3.6, 0], [FX, 3.6, 0], color=PALE, stroke_width=4),
                    Line([PX, 3.6, 0], [PX, 3.25, 0], color=PALE, stroke_width=4),
                    Line([FX, 3.6, 0], [FX, 3.25, 0], color=PALE, stroke_width=4))
        bl = lab("relatives", PALE, 0, 3.0, 30)
        self.play(Create(br), FadeIn(bl), run_time=0.6)
        self.at("death receptor")
        self.play(FadeIn(ls[2]), run_time=0.6)
        self.finish()


def death_row():
    """Dots, dashed arrow and chip for the 'can lead toward apoptosis' picture."""
    parts = [grey_dot([PX - 0.5, -2.75, 0]), grey_dot([PX + 0.5, -2.75, 0])]
    ar = dasharr([PX + 0.95, -2.75, 0], [PX + 1.95, -2.75, 0], RED)
    cl = lab("can lead to", PALE, PX + 1.75, -3.25, 24)
    ap = chip("apoptosis", RED, 28).move_to([PX + 3.55, -2.75, 0])
    return parts, ar, cl, ap


class S14(SpokenScene):
    def construct(self):
        mem, cyt, p, f, ls = base_pair()
        self.add(cyt, mem, p, f, ls)
        ddf, ddp = ddomain(FX, op=0.45), ddomain(PX)
        self.play(FadeIn(ddf, scale=0.5), run_time=0.5)
        lf = lab("death domain", VIOLET, FX + 2.3, -1.85, 26)
        self.play(FadeIn(lf), run_time=0.4)
        self.at("carries a death")
        self.play(FadeIn(ddp, scale=0.5), run_time=0.5)
        lp = lab("death domain", VIOLET, PX - 2.3, -1.85, 26)
        self.play(FadeIn(lp), Indicate(ddp, color=VIOLET), run_time=0.5)
        self.at("stretch")
        il = lab("inside the cell", PALE, 0.0, -0.95, 26)
        self.play(FadeIn(il), Indicate(ddp, color=TEXT, scale_factor=1.3), run_time=0.8)
        parts, ar, cl, ap = death_row()
        self.at("bind proteins")
        dl = lab("proteins", PALE, PX, -3.5, 24)
        for c in parts:
            c.shift(DOWN * 0.3)
        self.play(*[FadeIn(c) for c in parts], FadeIn(dl), run_time=0.3)
        self.play(parts[0].animate.shift(UP * 0.3), parts[1].animate.shift(UP * 0.3), run_time=0.6)
        self.at("leading toward")
        self.play(Create(ar), FadeIn(cl), run_time=0.5)
        self.at("apoptosis")
        self.play(FadeIn(ap), run_time=0.5)
        self.finish()


class S15(SpokenScene):
    def construct(self):
        mem, cyt, p, f, ls = base_pair()
        ddf, ddp = ddomain(FX, op=0.45), ddomain(PX)
        parts, ar, cl, ap = death_row()
        dl = lab("proteins", PALE, PX, -3.5, 24)
        lf = lab("death domain", VIOLET, FX + 2.3, -1.85, 26)
        lp = lab("death domain", VIOLET, PX - 2.3, -1.85, 26)
        il = lab("inside the cell", PALE, 0.0, -0.95, 26)
        self.add(cyt, mem, p, f, ls, ddf, ddp, *parts, ar, cl, ap, dl, lf, lp, il)
        self.play(FadeOut(ar), FadeOut(ap), FadeOut(cl), FadeOut(il), FadeOut(lf), FadeOut(lp), FadeOut(dl), run_time=0.3)
        self.at("does not use")
        hx = [hexa(r=0.3).move_to(c.get_center()) for c in parts]
        pl = lab("p75's proteins", SAND, PX, -3.4, 26)
        self.play(*[Transform(c, h) for c, h in zip(parts, hx)], FadeIn(pl), run_time=0.5)
        self.at("protein's")
        ts = [tri().move_to(pos) for pos in ([FX - 0.5, -2.75, 0], [FX + 0.5, -2.75, 0])]
        fl = lab("Fas's proteins", PALE, FX, -3.4, 26)
        self.play(*[FadeIn(t, shift=UP * 0.3) for t in ts], FadeIn(fl), run_time=0.5)
        self.at("uses", lead=0.4)
        ne = lab("not the same", TEXT, 0.0, -2.75, 32, weight=BOLD)
        self.play(FadeIn(ne), run_time=0.3)
        self.finish()


class S16(SpokenScene):
    def construct(self):
        mem, cyt, p, f, ls = base_pair()
        ddf, ddp = ddomain(FX, op=0.45), ddomain(PX)
        hx = [hexa(r=0.3).move_to(pos) for pos in ([PX - 0.5, -2.75, 0], [PX + 0.5, -2.75, 0])]
        ts = [tri().move_to(pos) for pos in ([FX - 0.5, -2.75, 0], [FX + 0.5, -2.75, 0])]
        pl = lab("p75's proteins", SAND, PX, -3.4, 26)
        fl = lab("Fas's proteins", PALE, FX, -3.4, 26)
        ne = lab("not the same", TEXT, 0.0, -2.75, 32, weight=BOLD)
        fas = VGroup(f, ls[1], ls[2], ddf, *ts, fl, ne)
        mine = VGroup(p, ddp, *hx, ls[0])
        self.add(cyt, mem, fas, mine, pl)
        self.play(FadeOut(fas), FadeOut(pl), mine.animate.shift(RIGHT * 2.6), run_time=0.7)
        px = PX + 2.6   # p75 now at -0.4
        self.at("partners")
        pt = lab("partners", SAND, px, -3.4, 28)
        self.play(FadeIn(pt), *[Indicate(h, color=SAND) for h in hx], run_time=0.8)
        self.at("With a partner")
        self.play(FadeOut(pt), *[FadeOut(h) for h in hx], run_time=0.4)
        self.at("partner called")
        s = 1.4
        xb = px + 0.35 + 0.13 * s   # bar centre when it touches the rod
        so = sortilin(xb + 4.2, MY, 0.7, s, bottom=-1.2, flip=True)
        self.play(FadeIn(so), run_time=0.3)
        self.play(so.animate.shift(LEFT * 4.2), run_time=0.9)
        sl = lab("sortilin", YELLOW, xb + 1.6, 1.35, 34)
        self.play(FadeIn(sl), run_time=0.4)
        self.at("can kill")
        sk = skull(px + 1.2, 3.0, 1.1)
        self.play(FadeIn(sk, scale=0.5), run_time=0.6)
        self.finish()


class S17(SpokenScene):
    def construct(self):
        s, cy = 2.6, -0.7
        d = dimer(0, cy, s)
        nm = lab("NGF", BLUE, 0, -2.7, 42)
        self.at("NGF is")
        self.play(FadeIn(d, scale=0.6), FadeIn(nm), run_time=0.8)
        self.at("longer precursor")
        self.play(*[GrowFromEdge(t, DOWN) for t in d.tails], run_time=0.9)
        self.at("pro NGF")
        pn = lab("proNGF", BLUE, 0, -2.7, 42)
        self.play(Transform(nm, pn), run_time=0.5)
        self.at("extra front")
        self.play(*[Indicate(t, color=ORANGE, scale_factor=1.2) for t in d.tails], run_time=0.8)
        self.at("pro domain")
        pd = lab("pro-domain", ORANGE, 4.5, 1.3, 38)
        ln = Line([3.0, 1.3, 0], [1.6, 1.3, 0], color=ORANGE, stroke_width=3)
        self.play(FadeIn(pd), Create(ln), run_time=0.6)
        self.finish()


class S18(SpokenScene):
    def construct(self):
        s, cy = 2.2, -0.6
        d = dimer(0, cy, s, tails=True)
        nm = lab("proNGF", BLUE, 0, -2.5, 42)
        self.add(d, nm)
        cut_y = cy + 1.05
        sc = scissors(-5.2, cut_y, 0.9)
        enz = lab("enzymes", SCIS, -5.2, cut_y + 1.1, 32)
        self.play(FadeIn(sc), FadeIn(enz), run_time=0.3)
        self.at("cut the")
        cx_left = -0.5 * s - 0.54
        self.play(sc.animate.move_to([cx_left, cut_y, 0]), FadeOut(enz), run_time=0.3)
        snip(self, sc, 0.08)
        tl, tr = d[2], d[3]
        cx_right = 0.5 * s - 0.54
        self.play(tl.animate.shift(UP * 0.9 + LEFT * 0.3).set_opacity(0), sc.animate.move_to([cx_right, cut_y, 0]), run_time=0.3)
        snip(self, sc, 0.08)
        self.play(tr.animate.shift(UP * 0.9 + RIGHT * 0.3).set_opacity(0), sc.animate.shift(RIGHT * 1.8).set_opacity(0), run_time=0.3)
        self.at("leave mature")
        mn = lab("mature NGF", BLUE, 0, -2.5, 42)
        self.play(Transform(nm, mn), run_time=0.5)
        self.at("Sortilin", lead=1.4)
        s2, xc, cy2 = 2.1, 3.0, -0.5
        target = dimer(-3.5, cy2, s2, tails=True)
        target[2:].set_opacity(0)
        d2 = dimer(xc, cy2, s2, tails=True)
        nm2 = lab("proNGF", BLUE, xc, -2.1, 36)
        self.play(Transform(d, target), nm.animate.move_to([-3.5, -2.1, 0]).scale(0.85), FadeIn(d2), FadeIn(nm2), run_time=0.6)
        self.at("Sortilin")
        so = sortilin(xc + 0.5 * s2 + 0.66 * s2, 0, cy2 + 0.695 * s2, s2, bottom=-1.7)
        sl = lab("sortilin", YELLOW, 5.3, 2.0, 32)
        self.play(FadeIn(so), FadeIn(sl), run_time=0.5)
        self.at("grips")
        self.play(Indicate(so.cup, color=YELLOW, scale_factor=1.4), run_time=0.7)
        self.finish()


class S18b(SpokenScene):
    def construct(self):
        ym, s, xc, ecd = -1.2, 1.8, 1.6, 1.7
        d, p, so, cy = clamp_parts(xc, ym, s, ecd, icd=0.9, k=1.0)
        # a shared sortilin foot a little longer so its label sits level with p75's
        mem, cyt = membrane(ym), inside(ym)
        px = xc - 0.5 * s
        nlp = lab("p75", VIOLET, px, -3.45, 32)
        nls = lab("sortilin", YELLOW, so.bar.get_x(), -3.45, 32)
        self.add(cyt, mem, p, so, nlp, nls)
        d.shift(UP * 1.2)
        self.at("with")
        self.play(Indicate(p, color=VIOLET), Indicate(so, color=YELLOW), run_time=0.7)
        self.at("binds the")
        pl = lab("proNGF", BLUE, xc, 3.6, 28)
        self.play(FadeIn(d, shift=UP * 0.1), run_time=0.3)
        self.play(d.animate.shift(DOWN * 1.2), run_time=0.6)
        self.play(FadeIn(pl), run_time=0.2)
        self.at("tightly")
        hl1 = Circle(radius=0.5, stroke_color=TEXT, stroke_width=6).move_to([px, cy - 0.35 * s, 0])
        hl2 = Circle(radius=0.55, stroke_color=TEXT, stroke_width=6).move_to([xc + 0.5 * s + 0.2 * s, cy + 0.695 * s, 0])
        tag = lab("tight", TEXT, xc + 0.5, ym + 0.75, 44, weight=BOLD)
        self.play(Create(hl1), Create(hl2), FadeIn(tag), run_time=0.5)
        self.wait(0.3)
        lx = -4.8
        lp = p75(lx, ym, ecd=ecd, icd=0.9, w=0.26 * s * 1.8)
        lm = dimer(lx + 0.5 * s, cy, s)
        lm.set_opacity(0.55)
        lml = lab("mature NGF", BLUE, lx + 0.5 * s, 3.6, 28)
        ring = DashedVMobject(Circle(radius=0.5, stroke_color=PALE, stroke_width=3).move_to([lx, cy - 0.35 * s, 0]), num_dashes=12)
        lw = lab("weaker", PALE, lx + 1.9, ym + 1.1, 36)
        lwl = DashedLine([lx + 1.35, ym + 1.3, 0], [lx + 0.5, 0.45, 0], color=PALE, stroke_width=3)
        lnp = lab("p75", VIOLET, lx, -3.45, 32)
        self.play(FadeIn(lp), FadeIn(lm), FadeIn(lml), FadeIn(ring), FadeIn(lw), Create(lwl), FadeIn(lnp), run_time=0.6)
        self.finish()


class S19(SpokenScene):
    def construct(self):
        nc = cell(0, -0.4, 1.9, GREY, 0.14, 5)
        self.play(FadeIn(nc), run_time=0.4)
        c1 = chip("Puzzle 1", TEXT, 30).move_to([-5.4, 3.4, 0])
        self.at("puzzles")
        self.play(FadeIn(c1), run_time=0.4)
        self.at("First")
        pts = [(-4.9, 1.2), (-4.0, -2.4), (4.0, -2.4), (4.9, 1.2)]
        ds = [dimer(x, y, 1.3) for x, y in pts]
        lbs = [lab(NAMES[i][0], BLUE, x, y - 0.9, 32) for i, (x, y) in enumerate(pts)]
        self.play(*[FadeIn(d, scale=0.6) for d in ds], *[FadeIn(l) for l in lbs], run_time=0.4)
        self.at("how does")
        q = lab("Which factor is mine?", TEXT, 0.4, 3.35, 46, weight=BOLD)
        self.play(FadeIn(q, shift=DOWN * 0.15), run_time=0.5)
        self.at("its own")
        qm = lab("?", TEXT, 0.0, -0.4, 90)
        self.play(FadeIn(qm, scale=0.6), run_time=0.6)
        self.finish()


class S20(SpokenScene):
    def construct(self):
        chip2 = chip("Puzzle 2", TEXT, 30).move_to([-5.4, 3.4, 0])
        ds = dish(0.0)
        d = dimer(0.0, 3.1, 0.7)
        self.play(FadeIn(chip2), FadeIn(ds), FadeIn(d), run_time=0.6)
        self.at("cultured", lead=1.4)
        self.play(d.animate.move_to([0.0, DY_D + DIMER_DY, 0]), run_time=0.8)
        dl = lab("mature NGF", BLUE, 0.0, LABEL_Y, 30)
        self.play(FadeIn(dl), run_time=0.4)
        self.at("cultured sympathetic")
        cl = lab("cultured sympathetic neurons", PALE, 0.0, RES_Y, 28)
        self.play(FadeIn(cl), run_time=0.5)
        self.at("they survive")
        sv = lab("survive", GREEN, 0.0, RES_Y, 36)
        self.play(*[c.body.animate.set_stroke(GREEN) for c in ds.cells], FadeOut(cl), FadeIn(sv), run_time=0.7)
        self.finish()


def two_dish_final(dead=True):
    d1, d2 = dish(-3.4), dish(3.4)
    for c in d1.cells:
        c.body.set_stroke(GREEN)
    fr = VGroup()
    if dead:
        for c in d2.cells:
            c.scale(0.55).set_color(RED)
        fr = VGroup(*[frags(3.4 + dx, DY_D + dy, 0.45) for dx, dy in DISH_POS])
    m1 = dimer(-3.4, DY_D + DIMER_DY, 0.7)
    m1l = lab("mature NGF", BLUE, -3.4, LABEL_Y, 30)
    pro = dimer(3.4, DY_D + DIMER_DY, 0.7, tails=True)
    pl = lab("uncut proNGF", BLUE, 3.4, LABEL_Y, 30)
    sv = lab("survive", GREEN, -3.4, RES_Y, 36)
    dd = lab("die", RED, 3.4, RES_Y, 36)
    return VGroup(d1, d2, fr, m1, m1l, pro, pl, sv, dd)


class S21(SpokenScene):
    def construct(self):
        d1 = dish(0.0)
        for c in d1.cells:
            c.body.set_stroke(GREEN)
        m1 = dimer(0.0, DY_D + DIMER_DY, 0.7)
        m1l = lab("mature NGF", BLUE, 0.0, LABEL_Y, 30)
        sv = lab("survive", GREEN, 0.0, RES_Y, 36)
        g1 = VGroup(d1, m1, m1l, sv)
        chip2 = chip("Puzzle 2", TEXT, 30).move_to([-5.4, 3.4, 0])
        self.add(g1, chip2)
        d2 = dish(3.4)
        pro = dimer(3.4, 3.1, 0.7, tails=True)
        self.play(g1.animate.shift(LEFT * 3.4), FadeOut(chip2), FadeIn(d2), FadeIn(pro), run_time=0.7)
        self.at("before its pro")
        self.play(pro.animate.shift(DOWN * (3.1 - (DY_D + DIMER_DY))), run_time=0.6)
        pl = lab("uncut proNGF", BLUE, 3.4, LABEL_Y, 30)
        self.play(FadeIn(pl), run_time=0.3)
        self.at("has been cut")
        self.play(Indicate(pro.tails, color=ORANGE, scale_factor=1.3), run_time=0.8)
        self.at("Barbara")
        cap = lab("Barbara Hempstead, 2001", PALE, 0, TOP_Y, 32)
        self.play(FadeIn(cap), run_time=0.5)
        self.at("neurons died")
        fr = [frags(3.4 + dx, DY_D + dy, 0.45) for dx, dy in DISH_POS]
        self.play(*[c.animate.scale(0.55).set_color(RED) for c in d2.cells], *[FadeIn(f) for f in fr], run_time=1.0)
        dd = lab("die", RED, 3.4, RES_Y, 36)
        self.play(FadeIn(dd), run_time=0.4)
        self.finish()


class S22(SpokenScene):
    def construct(self):
        g = two_dish_final()
        cap = lab("Barbara Hempstead, 2001", PALE, 0, TOP_Y, 32)
        self.add(g, cap)
        self.at("opposite fates")
        self.play(Indicate(g[7], color=GREEN, scale_factor=1.2), Indicate(g[8], color=RED, scale_factor=1.2), run_time=0.9)
        self.at("Where would you look")
        q = lab("Where is the difference?", TEXT, 0, TOP_Y, 38)
        self.play(FadeOut(cap), FadeIn(q), run_time=0.6)
        self.finish()


class S23Pause(NarratedScene):
    def construct(self):
        g = two_dish_final()
        q = lab("Where is the difference?", TEXT, 0, TOP_Y, 38)
        self.add(g, q)
        self.finish()


class S24(SpokenScene):
    def construct(self):
        g = two_dish_final()
        q = lab("Where is the difference?", TEXT, 0, TOP_Y, 38)
        self.add(g, q)
        mem, cyt = membrane(), inside()
        t, p = trk(-2.8), p75(2.8)
        self.at("Look at")
        self.play(g.animate.scale(4, about_point=[3.4, DY_D, 0]).set_opacity(0), FadeOut(q), run_time=0.5)
        self.at("receptors")
        self.play(FadeIn(cyt), FadeIn(mem), FadeIn(t), FadeIn(p), run_time=0.6)
        tl = lab("Trk", PINK, -2.8, 2.55, 40)
        pl = lab("p75", VIOLET, 2.8, 2.55, 40)
        self.play(FadeIn(tl), FadeIn(pl), run_time=0.4)
        self.finish()


def rule_banner(size=32):
    a = lab("The target supplies the factor.", TEXT, 0, 3.5, size)
    b = lab("The neuron's receptors decide what it means.", TEXT, 0, 3.0, size)
    fit(b, max_w=12.4)
    return VGroup(a, b)


class S25(SpokenScene):
    def construct(self):
        tag = lab("the one idea to carry", GOLD, 0, 3.3, 38)
        tb = target_block(-4.7, -1.0, 3.0, 4.4)
        c = cell(4.2, -1.1, 2.5, GREY, 0.14, 5).body
        self.play(FadeIn(tag), FadeIn(tb), FadeIn(c), run_time=0.6)
        self.at("one idea")
        d = dimer(-1.9, -1.0, 1.2)
        tk = trk(3.4, 1.27, ecd=0.9, icd=0.5, foot_r=0.25)
        pp = p75(5.0, 1.27, ecd=0.9, icd=0.45, w=0.7, k=0.5)
        self.play(FadeIn(d, shift=RIGHT * 0.2), FadeIn(tk), FadeIn(pp), run_time=0.6)
        self.at("The target supplies")
        a = lab("The target supplies the factor.", TEXT, 0, 3.35, 40)
        b = lab("The neuron's receptors decide what it means.", TEXT, 0, 2.65, 40)
        fit(b, max_w=12.4)
        self.play(FadeOut(tag), run_time=0.25)
        self.play(FadeIn(a), d.animate.move_to([-0.2, -1.0, 0]), run_time=1.0)
        self.at("receptors decide")
        self.play(FadeIn(b), run_time=0.6)
        self.at("what it means")
        q = lab("?", TEXT, 4.2, -1.4, 100)
        self.play(FadeIn(q, scale=0.6), run_time=0.6)
        self.finish()


class S26(SpokenScene):
    def construct(self):
        ban = rule_banner()
        ym = -0.5
        mem, cyt = membrane(ym), inside(ym)
        self.add(ban, cyt, mem)
        self.at("A track receptor")
        t = trk(-4.6, ym, ecd=1.8, icd=0.8)
        d1 = dimer(-4.6, ym + 1.8 + 0.34, 0.9)
        tl = lab("Trk", PINK, -3.4, 0.0, 34)
        self.play(FadeIn(t), FadeIn(tl), FadeIn(d1, shift=DOWN * 0.3), run_time=0.8)
        self.at("stay alive")
        o1 = chip("stay alive", GREEN, 30).move_to([-4.6, -3.1, 0])
        a1 = arr([-4.6, t.foot.get_bottom()[1] - 0.05, 0], [-4.6, -2.7, 0], GREEN)
        self.play(GrowArrow(a1), FadeIn(o1), run_time=0.6)
        self.at("p75")
        p = p75(-0.9, ym, ecd=1.8, icd=0.7, k=0.9)
        d2 = dimer(-0.9, ym + 1.8 + 0.34, 0.9)
        pl = lab("p75", VIOLET, 0.4, 0.0, 34)
        self.play(FadeIn(p), FadeIn(pl), FadeIn(d2, shift=DOWN * 0.3), run_time=0.8)
        self.at("die")
        o2 = chip("can say die", RED, 30).move_to([-0.9, -3.1, 0])
        a2 = dasharr([-0.9, p.dd.get_bottom()[1] - 0.05, 0], [-0.9, -2.7, 0], RED)
        self.play(Create(a2), FadeIn(o2), run_time=0.6)
        self.at("with")
        xc, s = 3.2, 0.9
        d3, p3, so, cy = clamp_parts(xc, ym, s, 1.8, icd=0.7, k=0.9)
        self.play(FadeIn(p3), FadeIn(so), run_time=0.6)
        sl = lab("sortilin", YELLOW, so.bar.get_x() + 0.2, ym - 1.55, 26)
        self.play(FadeIn(sl), run_time=0.3)
        self.at("uncut precursor")
        self.play(FadeIn(d3, shift=DOWN * 0.3), run_time=0.6)
        self.at("that way")
        o3 = chip("die", RED, 30).move_to([xc + 0.3, -3.1, 0])
        a3 = arr([xc - 0.45, p3.dd.get_bottom()[1] - 0.05, 0], [xc - 0.45, -2.7, 0], RED)
        sk = skull(xc + 1.45, -3.1, 0.55)
        self.play(GrowArrow(a3), FadeIn(o3), FadeIn(sk), run_time=0.6)
        self.finish()


class S27(SpokenScene):
    def construct(self):
        ban = rule_banner()
        ym, s, xc, ecd = -0.9, 1.35, 1.2, 1.5
        mem, cyt = membrane(ym), inside(ym)
        d, p, so, cy = clamp_parts(xc, ym, s, ecd, icd=0.7, k=0.8)
        px = xc - 0.5 * s
        pl = lab("p75", VIOLET, px, ym - 2.1, 28)
        sl = lab("sortilin", YELLOW, so.bar.get_x() + 0.1, ym - 2.1, 28)
        ta, tb = trk(-5.4, ym, ecd=ecd, icd=0.8), trk(-4.05, ym, ecd=ecd, icd=0.8)
        tl = lab("Trk", PINK, -4.725, ym - 2.1, 30)
        self.add(ban, cyt, mem, p, so, d, pl, sl, ta, tb, tl)
        self.at("Cutting")
        cut_y = cy + 0.75
        sc = scissors(xc - 3.6, cut_y, 0.8)
        self.play(FadeIn(sc), run_time=0.3)
        lx_t, rx_t = xc - 0.5 * s - 0.48, xc + 0.5 * s - 0.48
        self.play(sc.animate.move_to([lx_t, cut_y, 0]), run_time=0.5)
        self.at("removes the stretch")
        snip(self, sc, 0.1)
        self.play(d.tails[0].animate.shift(UP * 0.5).set_opacity(0), sc.animate.move_to([rx_t, cut_y, 0]), run_time=0.35)
        snip(self, sc, 0.1)
        self.play(d.tails[1].animate.shift(UP * 0.5).set_opacity(0), sc.animate.shift(RIGHT * 1.5).set_opacity(0), run_time=0.5)
        self.at("grips")
        ng = lab("nothing to grip", YELLOW, so.bar.get_x() + 1.9, cy + 0.7 * s, 28)
        self.play(Indicate(so.cup, color=YELLOW, scale_factor=1.5), FadeIn(ng), run_time=0.8)
        self.at("changes")
        self.play(FadeOut(ng), run_time=0.3)
        self.at("receptors the factor")
        wk = lab("weaker", PALE, px - 1.6, ym + 0.5, 30)
        wl = Line([px - 0.95, ym + 0.65, 0], [px - 0.25, ym + 1.05, 0], color=PALE, stroke_width=3)
        cp = dimer(xc, cy, s)
        cp.set_fill(opacity=0).set_stroke(opacity=0)
        self.add(cp)
        self.play(d.bodies.animate.set_fill(BLUE, 0.2).set_stroke(BLUE, opacity=0.5), FadeIn(wk), Create(wl), run_time=0.5)
        self.play(cp.animate.set_fill(BLUE, 0.5).set_stroke(BLUE, opacity=1).shift(RIGHT * (-4.725 - xc)), run_time=1.0)
        self.at("best")
        self.play(ta.foot.animate.set_fill(PINK, 1.0), tb.foot.animate.set_fill(PINK, 1.0), run_time=0.6)
        bl = lab("works best", GREEN, -4.725, ym - 2.6, 32, weight=BOLD)
        self.play(FadeIn(bl), run_time=0.4)
        self.finish()


class S28(SpokenScene):
    def construct(self):
        emb = DashedVMobject(Ellipse(width=12.2, height=5.6, stroke_color=GREY, stroke_width=4).move_to([0, -0.1, 0]), num_dashes=64)
        el = lab("normal embryo", PALE, 0, 3.3, 34)
        q1 = lab("?", TEXT, -1.9, 1.7, 64)
        self.play(Create(emb), FadeIn(el), FadeIn(q1), run_time=0.5)
        self.at("uncut precursor")
        gh = ghost_dimer(-3.6, 0.3, 1.6)
        self.play(FadeIn(gh, scale=0.8), run_time=0.6)
        self.at("reaches")
        ar = dasharr([-2.2, 0.0, 0], [-0.85, -0.35, 0], TEXT, 4)
        q2 = lab("?", TEXT, -1.5, 0.4, 64)
        self.play(Create(ar), FadeIn(q2), run_time=0.6)
        self.at("neurons")
        cs = VGroup(*[cell(x, y, 0.75) for x, y in ((0.0, -0.5), (3.4, 0.9), (3.9, -1.7), (-1.2, -2.0))])
        self.play(FadeIn(cs, lag_ratio=0.3), run_time=0.9)
        self.at("still unsettled")
        q = lab("how much? unsettled", TEXT, 0, -3.45, 40)
        self.play(FadeIn(q), run_time=0.7)
        self.finish()


class S29(SpokenScene):
    def construct(self):
        ym = -0.7
        tb = target_block(0, 3.05, 5.0, 1.2, 34)
        d = dimer(0, 1.9, 1.2)
        mem, cyt = membrane(ym), inside(ym)
        t, p = trk(-3.2, ym, ecd=1.5, icd=0.7), p75(2.6, ym, ecd=1.5, icd=0.7, k=0.9)
        so = sortilin(2.6 + 0.35 + 0.13 * 1.3, ym, 0.0, 1.3, bottom=ym - 0.6, flip=True)
        sl = lab("sortilin", YELLOW, 4.9, -0.3, 26)
        self.play(FadeIn(tb), FadeIn(d), FadeIn(cyt), FadeIn(mem), FadeIn(t), FadeIn(p), FadeIn(so), FadeIn(sl), run_time=0.8)
        self.at("factor comes from")
        fl = lab("the factor", BLUE, 2.5, 1.9, 30)
        self.play(Indicate(d, color=BLUE, scale_factor=1.15), FadeIn(fl), run_time=0.8)
        self.at("its meaning")
        a1 = arr([-0.9, 1.4, 0], [-3.0, 1.0, 0], BLUE, 4)
        a2 = arr([0.9, 1.4, 0], [2.3, 1.0, 0], BLUE, 4)
        self.play(GrowArrow(a1), GrowArrow(a2), FadeOut(fl), run_time=0.4)
        self.at("comes from the receptors")
        o1 = chip("stay alive", GREEN, 32).move_to([-3.2, -3.1, 0])
        o2 = chip("can say die", RED, 32).move_to([2.6, -3.1, 0])
        b1 = arr([-3.2, t.foot.get_bottom()[1] - 0.05, 0], [-3.2, -2.7, 0], GREEN)
        b2 = dasharr([2.6, p.dd.get_bottom()[1] - 0.05, 0], [2.6, -2.7, 0], RED)
        self.play(GrowArrow(b1), FadeIn(o1), Create(b2), FadeIn(o2), run_time=0.8)
        self.finish()


class S30End(EndCard):
    LINE = "The factor comes from the target; its meaning comes from the receptors."
