"""One Job, Three Birthplaces: chapter 1 of "Where Glia Come From"  (Biochemistrypedia chaptered film)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one colour per concept; same map as the lesson's earlier film, shared by all chapters)
  BLUE   = neural tube lineage: radial glia, astrocytes, oligodendrocytes, ependymal cells, the spinal cord
  ORANGE = yolk sac and microglia
  PURPLE = neural crest, Schwann cells, satellite glia
  TEXT   = neurons and axons (white)
  RED    = a gene removed, a loss, the open question
  GREY   = outlines, labels, de-emphasized (a cell whose birthplace is not yet shown)
  GOLD   = the take-home rule
NOTE for reviewers: the script's visual notes say "gold / sage / clay"; those are the words for ORANGE / BLUE /
PURPLE here (yolk sac = orange, neural tube = blue, neural crest = purple). Nothing else differs.
In this chapter a glial cell is coloured by where it was BORN (that is the idea of the film), so
oligodendrocytes and astrocytes share the neural tube colour and differ by shape.
"""
import numpy as np
import os
from bp_style import *  # noqa: F401,F403

# Keep the rendering log in the temporary render workspace.
_BaseSpokenScene = SpokenScene
class SpokenScene(_BaseSpokenScene):
    def at(self, phrase, lead=0.2, nth=0):
        rest = self.t_of(phrase, nth) - lead - self.elapsed()
        if rest > 0.02:
            self.wait(rest)

_BaseText = T
def T(text, size=30, *args, **kwargs):
    return _BaseText(text, max(26, size), *args, **kwargs)

TUBE, YOLK, CREST = BLUE, ORANGE, PURPLE
LIGHT = "#D0D0D0"       # a glial cell whose birthplace is not shown yet (clearly brighter than the dim neurons)
NOTE = "#C4C4C4"


def V(x, y=0.0):
    return np.array([x, y, 0.0])


def pol(c, r, deg):
    return np.array(c) + r * np.array([np.cos(np.deg2rad(deg)), np.sin(np.deg2rad(deg)), 0])


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def bracket(x0, x1, y, color=GREY, up=0.22, w=4):
    m = VMobject(stroke_color=color, stroke_width=w)
    m.set_points_as_corners([V(x0, y + up), V(x0, y), V(x1, y), V(x1, y + up)])
    return m


def poly(points, color, w=5):
    m = VMobject(stroke_color=color, stroke_width=w)
    m.set_points_as_corners([V(*p) for p in points])
    return m


def badge(m, r=0.21, dx=0.06, dy=0.06):
    """A small red 'removed' badge beside a name (the name itself stays readable)."""
    c = Circle(radius=r, stroke_color=RED, stroke_width=3, fill_color=BG, fill_opacity=1)
    d = r * 0.5
    x = VGroup(Line(V(-d, d), V(d, -d), color=RED, stroke_width=5), Line(V(-d, -d), V(d, d), color=RED, stroke_width=5))
    return VGroup(c, x).move_to(m.get_corner(UR) + V(dx, dy))


def leader(a, b, color=GREY, w=2.5):
    return Line(a, b, color=color, stroke_width=w, stroke_opacity=0.8)


DEFAULT_COL = {"micro": YOLK, "astro": TUBE, "oligo": TUBE, "epend": TUBE, "schwann": CREST, "sat": CREST}


def glia(kind, pos=ORIGIN, s=1.0, col=None):
    col = col or DEFAULT_COL[kind]
    pos = np.array(pos, dtype=float)
    if kind == "astro":
        g = Star(n=7, outer_radius=0.4, inner_radius=0.18, color=col, stroke_width=3,
                 fill_color=col, fill_opacity=0.45)
    elif kind == "oligo":
        parts = []
        for a in (30, 150, 270):
            tip = 0.5 * np.array([np.cos(np.deg2rad(a)), np.sin(np.deg2rad(a)), 0])
            parts.append(Line(ORIGIN, tip, color=col, stroke_width=7))
            parts.append(Circle(radius=0.07, stroke_width=0, fill_color=col, fill_opacity=1).move_to(tip))
        body = Circle(radius=0.2, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.6)
        g = VGroup(*parts, body)
    elif kind == "micro":
        parts = []
        for a in range(15, 360, 60):
            d = np.array([np.cos(np.deg2rad(a)), np.sin(np.deg2rad(a)), 0])
            end = 0.3 * d
            parts.append(Line(ORIGIN, end, color=col, stroke_width=2.5))
            for da in (-38, 38):
                t = np.array([np.cos(np.deg2rad(a + da)), np.sin(np.deg2rad(a + da)), 0])
                parts.append(Line(end, end + 0.14 * t, color=col, stroke_width=2))
        body = Circle(radius=0.14, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.8)
        g = VGroup(*parts, body)
    elif kind == "epend":
        body = RoundedRectangle(corner_radius=0.08, width=0.62, height=0.5, stroke_color=col, stroke_width=3,
                                fill_color=col, fill_opacity=0.5).move_to([0, -0.1, 0])
        cil = [Line([x, 0.15, 0], [x + dx, 0.42, 0], color=col, stroke_width=2.5)
               for x, dx in [(-0.2, -0.06), (-0.1, -0.02), (0, 0), (0.1, 0.02), (0.2, 0.06)]]
        g = VGroup(body, *cil)
    elif kind == "schwann":
        ax = Line([-0.7, 0, 0], [0.7, 0, 0], color=TEXT, stroke_width=3)
        body = RoundedRectangle(corner_radius=0.15, width=0.85, height=0.34, stroke_color=col, stroke_width=3,
                                fill_color=col, fill_opacity=0.5)
        g = VGroup(ax, body)
    elif kind == "sat":
        cell_ = Circle(radius=0.2, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.8)
        dots = [Circle(radius=0.08, stroke_width=0, fill_color=col, fill_opacity=1)
                .move_to(0.36 * np.array([np.cos(np.deg2rad(a)), np.sin(np.deg2rad(a)), 0])) for a in range(0, 360, 60)]
        g = VGroup(cell_, *dots)
    else:
        raise ValueError(kind)
    return g.scale(s).move_to(pos)


def neuron(pos, s=1.0, dim=False):
    """A neuron: a triangle cell body, two short dendrites and one long axon (clearly not a glial icon)."""
    body = Triangle(stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.85).scale(0.22)
    body.move_to(V(0, 0.05))
    den = [Line(V(-0.08, 0.2), V(-0.3, 0.45), color=TEXT, stroke_width=3),
           Line(V(0.08, 0.2), V(0.3, 0.45), color=TEXT, stroke_width=3)]
    axon = Line(V(0, -0.14), V(0, -0.62), color=TEXT, stroke_width=3)
    g = VGroup(body, *den, axon).scale(s).move_to(pos)
    if dim:
        g.set_opacity(0.3)
    return g


def ghost(center, r=0.45, w=4):
    """A dashed circle: a cell that is missing."""
    return DashedVMobject(Circle(radius=r, color=GREY, stroke_width=w), num_dashes=14).move_to(center)


# ---------------------------------------------------------------- legend of birthplaces
def legend(names=("tube", "yolk", "crest"), size=28, y=3.5):
    spec = {"tube": ("neural tube", TUBE), "yolk": ("yolk sac", YOLK), "crest": ("neural crest", CREST)}
    xs = {3: [-4.4, 0.0, 4.4], 2: [-4.4, 4.4]}[len(names)]
    return VGroup(*[T(spec[n][0], size, spec[n][1]).move_to(V(x, y)) for n, x in zip(names, xs)])


# ---------------------------------------------------------------- axon-and-wrapping panels (s07 onward)
def cell(kind, cx, cy, w, h, present=True, precursor=False):
    """A panel holding one axon and the glia that wrap it. kind: 'cns' (oligodendrocyte) or 'pns' (Schwann)."""
    col = TUBE if kind == "cns" else CREST
    panel = RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_color=col, stroke_width=3,
                             fill_color=col, fill_opacity=0.06).move_to([cx, cy, 0])
    ay = cy - 0.1 * h
    axon = Line([cx - 0.46 * w, ay, 0], [cx + 0.46 * w, ay, 0], color=TEXT, stroke_width=5)
    xs = [cx - 0.27 * w, cx, cx + 0.27 * w]
    if precursor:
        parts = VGroup(*[Circle(radius=0.15, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.85)
                         .move_to([x, ay + 0.2, 0]) for x in xs])
        return VGroup(panel, axon, parts)
    segs = [RoundedRectangle(corner_radius=0.08, width=0.2 * w, height=0.17 * h, stroke_color=col, stroke_width=3,
                             fill_color=col, fill_opacity=0.55).move_to([x, ay, 0]) for x in xs]
    if kind == "cns":
        body = Circle(radius=0.075 * h, stroke_color=col, stroke_width=3, fill_color=col,
                      fill_opacity=0.7).move_to([cx, cy + 0.27 * h, 0])
        arms = [Line(body.get_center(), [x, ay + 0.085 * h, 0], color=col, stroke_width=4) for x in xs]
        extra = [body] + arms
    else:
        extra = [Circle(radius=0.045 * h, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.9)
                 .move_to([x, ay + 0.085 * h + 0.04 * h, 0]) for x in xs]
    parts = VGroup(*segs, *extra)
    if not present:
        parts.set_opacity(0.15)
    return VGroup(panel, axon, parts)


SL = (-3.9, -0.5, 5.0, 4.2)      # single-row geometry: left (spinal cord) and right (nerve)
SR = (3.9, -0.5, 5.0, 4.2)
R1L, R1R = (-1.0, 1.65, 4.8, 2.7), (4.2, 1.65, 4.8, 2.7)      # two-row geometry
R2L, R2R = (-1.0, -1.35, 4.8, 2.7), (4.2, -1.35, 4.8, 2.7)


def lab(text, color, x, y, size=24):
    return T(text, size, color).move_to([x, y, 0])


def header(kind):
    """Single-row header: small icon + cell name."""
    if kind == "cns":
        ic = glia("oligo", V(-5.8, 2.75), 0.9)
        nm = T("oligodendrocytes", 28, TUBE).move_to(V(-3.3, 2.75))
    else:
        ic = glia("schwann", V(2.2, 2.75), 0.9)
        nm = T("Schwann cells", 28, CREST).move_to(V(4.5, 2.75))
    return ic, nm


def olig_chips(x=0.0, y1=0.95, y2=-0.35, size=40):
    c1 = chip("Olig1", TEXT, size, pad=0.26).move_to(V(x, y1))
    c2 = chip("Olig2", TEXT, size, pad=0.26).move_to(V(x, y2))
    return c1, c2


def question_state(q=True, chips_between=True):
    """The frame at the end of s08 and through the pause: oligodendrocytes gone, nerve Schwann cells in question."""
    d = {}
    d["leg"] = legend(("tube", "crest"), 26, 3.55)
    d["hL"] = header("cns")
    d["hR"] = header("pns")
    d["pL"] = cell("cns", *SL, present=False)
    d["xL"] = Cross(d["pL"][2], stroke_color=RED, stroke_width=6)
    d["pR"] = cell("pns", *SR, present=True)
    d["c1"], d["c2"] = olig_chips()
    d["b1"], d["b2"] = badge(d["c1"]), badge(d["c2"])
    if q:
        d["q"] = T("?", 72, RED, weight=BOLD).move_to(V(6.3, 2.75))
        d["ql"] = T("lose them too?", 30, RED).move_to(V(3.9, -3.15))
    return d


def add_all(scene, d):
    for v in d.values():
        if isinstance(v, (tuple, list)):
            scene.add(*v)
        else:
            scene.add(v)


# ====================================================================================================
class S00Title(TitleCard):
    LESSON = "Where Glia Come From"
    TITLE = "One Job, Three Birthplaces"

    def construct(self):
        brand = T("BIOCHEMISTRYPEDIA", size=20, color=TEAL, weight=BOLD).set_opacity(0.9)
        lesson = T(self.LESSON.upper(), size=22, color=GREY)
        title = T(self.TITLE, size=54, font=TITLE_FONT)
        fit(title, max_w=11.5)
        rule = Line(LEFT * 1.2, RIGHT * 1.2, color=GOLD, stroke_width=4)
        g = VGroup(brand, lesson, title, rule).arrange(DOWN, buff=0.32)
        self.play(FadeIn(brand, shift=UP * 0.1), FadeIn(lesson, shift=UP * 0.1), run_time=self.beat(0.25))
        self.play(FadeIn(title, shift=UP * 0.1), GrowFromCenter(rule), run_time=self.beat(0.35))
        self.wait(self.beat(0.2))
        self.finish()


# ---------------------------------------------------------------------------------------------------
BK = 1.20
BRAIN_X, BRAIN_Y = -0.6, 0.15
MG_POS = [(-1.8, 0.7), (-1.2, -0.5), (-0.7, 1.4), (0.2, 0.3), (0.7, -0.8), (1.0, 1.3), (1.9, 0.4), (1.7, -0.7)]


def brain(cx=BRAIN_X, cy=BRAIN_Y, k=BK):
    """Side view of a mouse brain: cortex, olfactory bulb, cerebellum, brainstem."""
    st = dict(stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.12)
    cortex = Ellipse(width=5.0 * k, height=3.9 * k, **st).move_to([cx + 0.2 * k, cy + 0.4 * k, 0])
    bulb = Ellipse(width=1.2 * k, height=1.0 * k, **st).move_to([cx - 2.75 * k, cy - 0.15 * k, 0])
    cb = Ellipse(width=1.9 * k, height=1.3 * k, **st).move_to([cx + 2.0 * k, cy - 1.75 * k, 0])
    stem = RoundedRectangle(corner_radius=0.2, width=0.7 * k, height=1.3 * k, **st).move_to(
        [cx + 0.7 * k, cy - 2.0 * k, 0])
    return VGroup(stem, bulb, cb, cortex)


def brain_microglia(cx=BRAIN_X, cy=BRAIN_Y, k=BK, s=1.5):
    return [glia("micro", V(cx + x * k, cy + y * k), s) for x, y in MG_POS]


class S01Q(SpokenScene):
    def construct(self):
        br = brain()
        mg = brain_microglia()
        top = T("mouse brain", 30, GREY).move_to(V(BRAIN_X, 3.45))
        qm = T("?", 260, RED, weight=BOLD).move_to(V(4.7, -0.5))
        self.at("in a mouse")
        self.add(br, top, *mg, qm)
        self.wait(0.3)
        self.at("immune cells")
        self.play(Indicate(VGroup(*mg), color=YOLK), run_time=0.5)
        il = T("immune cells", 30, YOLK).move_to(V(4.7, 2.4))
        ld = leader(V(2.7, 2.2), mg[6].get_center() + V(0.3, 0.3), YOLK)
        self.play(FadeIn(il), Create(ld), run_time=0.5)
        self.at("not made")
        self.play(Indicate(VGroup(*mg), color=YOLK, scale_factor=1.05), run_time=1.2)
        self.at("so where were they made")
        self.play(Indicate(qm), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------------
HEAD = V(-4.0, 1.5)
YC = V(2.9, 0.1)


def embryo_shape():
    head = Ellipse(width=4.8, height=3.2).move_to(HEAD + V(0.3, 0))
    body = Ellipse(width=3.6, height=3.6).move_to(V(-3.7, -1.35))
    return Union(head, body, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.12)


def yolk_cells():
    ps = [V(0.5, 0.9), V(1.3, -0.6), V(1.5, 1.5), V(2.3, 0.3), V(0.7, -1.4), V(2.0, -1.6)]
    return [Circle(radius=0.2, stroke_color=YOLK, stroke_width=3, fill_color=YOLK, fill_opacity=0.9).move_to(p)
            for p in ps]


def cell_path(p0, target):
    m = VMobject()
    m.set_points_smoothly([p0, V(-0.5, -0.3), V(-2.7, -0.9), V(-3.3, 0.4), target])
    return m


class S02(SpokenScene):
    def construct(self):
        br = brain()
        mg = VGroup(*brain_microglia())
        self.add(br, mg)
        self.at("microglia")
        lbl = T("microglia", 40, YOLK).move_to(V(BRAIN_X, 3.4))
        self.play(FadeIn(lbl), Indicate(mg, color=YOLK, scale_factor=1.06), run_time=1.1)
        emb = embryo_shape()
        e95 = T("about E9.5", 30, GREY).move_to(V(-4.0, 3.45))
        emb_l = T("mouse embryo", 26, GREY).move_to(V(-4.0, -3.5))
        self.at("in mice")
        self.play(FadeOut(mg), FadeOut(lbl), br.animate.scale(0.56).move_to(HEAD + V(0, 0.05)), FadeIn(emb),
                  FadeIn(e95), FadeIn(emb_l), run_time=1.2)
        yolk = Ellipse(width=7.0, height=5.6, stroke_color=YOLK, stroke_width=4, fill_color=YOLK,
                       fill_opacity=0.12).move_to(YC)
        stalk = Line(V(-2.2, -1.2), V(-0.45, -0.8), color=GREY, stroke_width=9, stroke_opacity=0.6)
        cells = yolk_cells()
        ylab = T("yolk sac", 36, YOLK).move_to(YC + V(1.5, 0.9))
        out = T("outside the embryo", 28, YOLK).move_to(YC + V(0, -3.15))
        # Cells are visible in the sac before they migrate, with two retained as the source.
        self.play(FadeIn(yolk), FadeIn(stalk), *[FadeIn(c) for c in cells], FadeIn(ylab),
                  run_time=0.55)
        targets = [HEAD + V(-0.7, 0.2), HEAD + V(-0.25, -0.35),
                   HEAD + V(0.25, 0.3), HEAD + V(0.7, -0.15)]
        paths = [cell_path(c.get_center(), t) for c, t in zip(cells[:4], targets)]
        route = cell_path(V(1.0, -0.6), HEAD + V(0.3, 0.1))
        route.set_stroke(YOLK, width=4, opacity=0.65)
        self.at("descend from")
        self.play(Create(route), run_time=0.35)
        self.play(LaggedStart(*[MoveAlongPath(c, path, rate_func=linear) for c, path in zip(cells[:4], paths)],
                              lag_ratio=0.18), FadeIn(out), run_time=3.4)
        self.play(*[Transform(c, glia("micro", t, 0.65)) for c, t in zip(cells[:4], targets)], run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------------
def build_field():
    spec = [("micro", (-5.0, 1.3)), ("astro", (-2.4, -1.5)), ("oligo", (0.2, 1.3)),
            ("astro", (2.5, -0.9)), ("micro", (4.9, 1.5)), ("oligo", (-0.6, -2.2))]
    gl = [glia(k, V(*p), 1.6, LIGHT) for k, p in spec]
    rs = np.random.RandomState(11)
    pts = [np.array(p) for _, p in spec]
    ns = []
    tries = 0
    while len(ns) < 14 and tries < 4000:
        tries += 1
        p = np.array([rs.uniform(-6.2, 6.2), rs.uniform(-3.0, 1.9)])
        if all(np.linalg.norm(p - q) > 1.5 for q in pts):
            pts.append(p)
            ns.append(neuron(V(*p), 0.9, dim=True))
    return gl, ns


def field_labels():
    l_g = T("glia", 34, LIGHT, weight=BOLD).move_to(V(-4.8, 3.2))
    l_n = T("neurons", 30, GREY).move_to(V(0, 3.2))
    l_b = T("not one birthplace", 34, TEXT).move_to(V(4.2, 3.2))
    return l_g, l_n, l_b


class S03(SpokenScene):
    def construct(self):
        gl, ns = build_field()
        l_g, l_n, l_b = field_labels()
        self.add(*gl, l_g)
        self.at("glia")
        self.play(Indicate(VGroup(*gl), color=LIGHT, scale_factor=1.03), run_time=0.6)
        self.at("among neurons")
        self.play(LaggedStart(*[FadeIn(n, scale=0.4) for n in ns], lag_ratio=0.05), FadeIn(l_n), run_time=1.0)
        self.at("share one")
        self.play(FadeIn(l_b, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------------
TC = V(-3.4, 0.1)           # big neural tube
COLX = 2.2
COLY = [2.1, 0.1, -1.9]


def big_tube(lit=True):
    c = TUBE if lit else GREY
    return Annulus(inner_radius=0.6, outer_radius=2.9, stroke_color=c, stroke_width=4, fill_color=c,
                   fill_opacity=0.14 if lit else 0.04).move_to(TC)


def spokes():
    return VGroup(*[Line(pol(TC, 0.65, a), pol(TC, 2.85, a), color=TUBE, stroke_width=3).set_opacity(0.8)
                    for a in range(0, 360, 30)])


class S04(SpokenScene):
    def construct(self):
        gl, ns = build_field()
        l_g, l_n, l_b = field_labels()
        self.add(*gl, *ns, l_g, l_n, l_b)
        astro, oligo = gl[1], gl[2]
        others = [m for m in gl if m is not astro and m is not oligo]
        tube = big_tube(False)
        names = ["astrocyte", "oligodendrocyte", "ependymal"]
        kinds = ["astro", "oligo", "epend"]
        epend = glia("epend", V(COLX, COLY[2]), 1.5, LIGHT)
        icons = [astro, oligo, epend]
        # the field clears; two cells move into a column, the tube outline appears
        self.at("astrocytes")
        self.play(FadeOut(VGroup(*ns, *others, l_g, l_n, l_b)),
                  astro.animate.move_to(V(COLX, COLY[0])).scale(1.5 / 1.6),
                  oligo.animate.move_to(V(COLX, COLY[1])).scale(1.5 / 1.6),
                  FadeIn(tube), run_time=1.0)
        labs = [T(n, 26, LIGHT).next_to(ic, RIGHT, buff=0.3) for n, ic in zip(names, icons)]
        labs[0].next_to(V(COLX, COLY[0]), RIGHT, buff=0.85)
        self.play(FadeIn(labs[0]), run_time=0.3)
        self.at("oligodendrocytes")
        labs[1].next_to(V(COLX, COLY[1]), RIGHT, buff=0.85)
        self.play(FadeIn(labs[1]), run_time=0.3)
        self.at("ependymal")
        self.play(FadeIn(epend, scale=0.4), run_time=0.4)
        labs[2].next_to(epend, RIGHT, buff=0.3)
        self.play(FadeIn(labs[2]), run_time=0.3)
        # the cause first: the tube wall lights up, radial glia span it, a neuron then an astrocyte bud off
        tube_l = T("neural tube", 30, TUBE).move_to(V(TC[0], -3.45))
        self.at("come from")
        self.play(tube.animate.set_stroke(TUBE).set_fill(TUBE, 0.14), run_time=0.6)
        self.at("neural tube")
        self.play(FadeIn(tube_l), run_time=0.4)
        sp = spokes()
        self.at("most come")
        self.play(LaggedStart(*[Create(s) for s in sp], lag_ratio=0.1), run_time=0.9)
        nb = neuron(pol(TC, 0.95, 30), 1.6)
        ab = glia("astro", pol(TC, 0.95, 210), 1.0)
        self.at("same pool")
        self.play(FadeIn(nb, scale=0.4), run_time=0.3)
        self.play(nb.animate.move_to(pol(TC, 2.3, 30)), run_time=0.6)
        rg_l = T("radial glia", 30, TUBE).move_to(V(TC[0], 3.45))
        rg_ld = leader(V(TC[0], 3.2), pol(TC, 2.9, 90), TUBE)
        self.at("radial glia")
        self.play(FadeIn(rg_l), Create(rg_ld), FadeIn(ab, scale=0.4), run_time=0.4)
        self.play(ab.animate.move_to(pol(TC, 2.2, 210)), run_time=0.6)
        nb_l = T("neuron", 26, TEXT).move_to(V(-1.1, 2.15))
        self.add(nb_l)
        # only then: the three icons take the tube colour and arrows link them to it
        ars = [arr(V(-0.45, 0.1), V(1.1, y), TUBE, 4, 0.2) for y in COLY]
        self.play(*[GrowArrow(a) for a in ars],
                  *[Transform(ic, glia(k, ic.get_center(), 1.5)) for ic, k in zip(icons, kinds)],
                  *[l.animate.set_color(TUBE) for l in labs], run_time=0.65)
        self.finish()


def s04_end():
    d = {}
    d["tube"] = big_tube(True)
    d["tube_l"] = T("neural tube", 30, TUBE).move_to(V(TC[0], -3.45))
    d["sp"] = spokes()
    d["rg_l"] = T("radial glia", 30, TUBE).move_to(V(TC[0], 3.45))
    d["rg_ld"] = leader(V(TC[0], 3.2), pol(TC, 2.9, 90), TUBE)
    d["nb"] = VGroup(neuron(pol(TC, 2.3, 30), 1.6), T("neuron", 26, TEXT).move_to(V(-1.1, 2.15)))
    d["ab"] = glia("astro", pol(TC, 2.2, 210), 1.0)
    d["icons"] = [glia(k, V(COLX, y), 1.5) for k, y in zip(["astro", "oligo", "epend"], COLY)]
    d["labs"] = [T(n, 26, TUBE).next_to(V(COLX, y), RIGHT, buff=b)
                 for n, y, b in zip(["astrocyte", "oligodendrocyte", "ependymal"], COLY, [0.85, 0.85, 0.3])]
    d["labs"][2].next_to(d["icons"][2], RIGHT, buff=0.3)
    d["ars"] = [arr(V(-0.45, 0.1), V(1.1, y), TUBE, 4, 0.2) for y in COLY]
    return d


# ---------------------------------------------------------------------------------------------------
ROWY = [2.35, 0.35, -1.75]
SLOTX = [-1.5, 1.6, 4.9]
SRCX = -5.0
BUSY = -0.95


def mini_tube(cx, cy, r=0.62):
    return Annulus(inner_radius=0.2, outer_radius=r, stroke_color=TUBE, stroke_width=3, fill_color=TUBE,
                   fill_opacity=0.14).move_to([cx, cy, 0])


def bus_line():
    return VGroup(*[poly([(SRCX, ROWY[2] + 0.64), (SRCX + 0.8, -0.72),
                         (x, -0.72)], CREST, 5) for x in SLOTX[:2]])


def bus_drops():
    return [arr(V(x, -0.72), V(x, ROWY[2] + 0.3), CREST, 6, 0.3) for x in SLOTX[:2]]


def s05_rows():
    """The finished map of s05: three birthplaces, six cell types. Returns dict."""
    d = {}
    d["tube"] = mini_tube(SRCX, ROWY[0])
    d["tube_l"] = T("neural tube", 24, TUBE).move_to(V(SRCX, ROWY[0] - 1.0))
    d["ic0"] = [glia(k, V(SLOTX[i], ROWY[0]), 1.5) for i, k in enumerate(["astro", "oligo", "epend"])]
    d["lb0"] = [T(n, 24, TUBE).move_to(V(SLOTX[i], ROWY[0] - 0.85)) for i, n in enumerate(["astrocyte", "oligodendrocyte", "ependymal"])]
    d["ar0"] = arr(V(-4.25, ROWY[0]), V(-2.6, ROWY[0]), TUBE, 5)
    d["yolk"] = Ellipse(width=2.4, height=1.2, stroke_color=YOLK, stroke_width=4, fill_color=YOLK,
                        fill_opacity=0.14).move_to(V(SRCX, ROWY[1]))
    d["yolk_l"] = T("yolk sac", 24, YOLK).move_to(V(SRCX, ROWY[1]))
    d["ic1"] = glia("micro", V(SLOTX[0], ROWY[1]), 1.5)
    d["lb1"] = T("microglia", 24, YOLK).move_to(V(SLOTX[0], ROWY[1] - 0.85))
    d["ar1"] = arr(V(-3.7, ROWY[1]), V(-2.6, ROWY[1]), YOLK, 5)
    d["crest"] = mini_tube(SRCX, ROWY[2]).set_color(CREST)
    d["crest_cells"] = VGroup(*[Dot(pol(V(SRCX, ROWY[2]), 0.75, a), radius=0.15, color=CREST) for a in (45, 70, 95, 120, 145)])
    d["crest_l"] = T("neural crest", 24, CREST).move_to(V(SRCX, ROWY[2] - 0.95))
    d["ic2"] = [glia("schwann", V(SLOTX[0], ROWY[2]), 1.7), glia("sat", V(SLOTX[1], ROWY[2]), 1.5)]
    d["lb2"] = [T("Schwann cell", 24, CREST).move_to(V(SLOTX[0], ROWY[2] - 0.85)),
                T("satellite glia", 24, CREST).move_to(V(SLOTX[1], ROWY[2] - 0.85))]
    d["crest_cells"].add(*[Dot(V(x, -0.72), radius=0.14, color=CREST) for x in (-4.1, -3.45, -2.8, -2.15, -0.75, 0.1, 0.9)])
    d["bus"] = bus_line()
    d["drops"] = bus_drops()
    return d


class S05(SpokenScene):
    def construct(self):
        d = s05_rows()
        self.add(d["tube"], d["tube_l"], *d["ic0"], *d["lb0"], d["ar0"],
                 d["ic1"], d["lb1"], d["yolk"], d["yolk_l"], d["ar1"])
        self.at("microglia")
        self.play(Indicate(d["ic1"], color=YOLK), Indicate(d["yolk"], color=YOLK), run_time=0.6)
        self.at("yolk sac")
        self.play(Indicate(d["ar1"], color=YOLK), run_time=0.5)
        sw = glia("schwann", V(SLOTX[0], ROWY[2]), 1.7, GREY)
        sw_l = T("Schwann cell", 24, GREY).move_to(V(SLOTX[0], ROWY[2] - 0.85))
        self.at("schwann cells")
        self.play(FadeIn(sw, scale=0.4), FadeIn(sw_l), run_time=0.5)
        st = glia("sat", V(SLOTX[1], ROWY[2]), 1.5, GREY)
        st_l = T("satellite glia", 24, GREY).move_to(V(SLOTX[1], ROWY[2] - 0.85))
        self.at("satellite glia")
        self.play(FadeIn(st, scale=0.4), FadeIn(st_l), run_time=0.5)
        # the neural crest: the tube with crest cells on its dorsal edge; they stream away along the nerve route
        crest = d["crest"]
        dots = [Circle(radius=0.16, stroke_width=2, stroke_color=CREST, fill_color=CREST, fill_opacity=1)
                .move_to(pol(V(SRCX, ROWY[2]), 0.75, a)) for a in (60, 75, 90, 105, 120, 90)]
        self.at("neural crest", lead=1.0)
        self.play(FadeIn(crest), FadeIn(d["crest_l"]), FadeIn(VGroup(*dots), scale=0.3), run_time=0.35)
        self.add(d["crest_cells"])
        paths = []
        for i, dot in enumerate(dots):
            tx = SLOTX[0] if i < 3 else SLOTX[1]
            pth = VMobject()
            pth.set_points_as_corners([dot.get_center(), V(SRCX + 0.8, -0.72), V(tx, -0.72), V(tx, ROWY[2] + 0.4)])
            paths.append(pth)
        self.play(*[MoveAlongPath(dot, p) for dot, p in zip(dots, paths)], Create(d["bus"]),
                  *[GrowArrow(a) for a in d["drops"]],
                  Transform(sw, d["ic2"][0]), Transform(st, d["ic2"][1]),
                  sw_l.animate.set_color(CREST), st_l.animate.set_color(CREST), run_time=1.1)
        self.play(*[FadeOut(dot) for dot in dots], run_time=0.25)
        self.finish()


def rebuild_s05(scene):
    d = s05_rows()
    scene.add(d["tube"], d["tube_l"], *d["ic0"], *d["lb0"], d["ar0"], d["yolk"], d["yolk_l"], d["ic1"], d["lb1"],
              d["ar1"], d["crest"], d["crest_cells"], d["crest_l"], *d["ic2"], *d["lb2"], d["bus"], *d["drops"])
    return d


# ---------------------------------------------------------------------------------------------------
class S06(SpokenScene):
    def construct(self):
        d = rebuild_s05(self)
        leg = legend(("tube", "yolk", "crest"), 32, 3.5)
        oligo, sch = d["ic0"][1], d["ic2"][0]
        oligo_l, sch_l = d["lb0"][1], d["lb2"][0]
        rest = [d["tube"], d["tube_l"], d["ic0"][0], d["ic0"][2], d["lb0"][0], d["lb0"][2], d["ar0"], d["crest_cells"],
                d["yolk"], d["yolk_l"], d["ic1"], d["lb1"], d["ar1"], d["crest"], d["crest_l"], d["ic2"][1],
                d["lb2"][1], d["bus"], *d["drops"]]
        self.play(FadeIn(leg, shift=DOWN * 0.1), run_time=0.4)
        self.at("take two cells")
        self.play(*[FadeOut(m) for m in rest],
                  oligo.animate.scale(2.6 / 1.5).move_to(V(-3.9, 0.4)),
                  sch.animate.scale(2.2 / 1.7).move_to(V(3.9, 0.4)),
                  oligo_l.animate.scale(28 / 24).move_to(V(-3.9, -1.3)),
                  sch_l.animate.scale(28 / 24).move_to(V(3.9, -1.3)), run_time=0.9)
        sj = T("same job", 38, TEXT, font=TITLE_FONT).move_to(V(0, -0.5))
        self.at("same job")
        self.play(FadeIn(sj, scale=0.8), run_time=0.5)
        self.finish()


def rebuild_s06(scene):
    oligo = glia("oligo", V(-3.9, 0.4), 2.6)
    sch = glia("schwann", V(3.9, 0.4), 2.2)
    oligo_l = T("oligodendrocyte", 28, TUBE).move_to(V(-3.9, -1.3))
    sch_l = T("Schwann cell", 28, CREST).move_to(V(3.9, -1.3))
    sj = T("same job", 38, TEXT, font=TITLE_FONT).move_to(V(0, -0.5))
    leg = legend(("tube", "yolk", "crest"), 32, 3.5)
    scene.add(oligo, sch, oligo_l, sch_l, sj, leg)
    return oligo, sch, oligo_l, sch_l, sj, leg


# ---------------------------------------------------------------------------------------------------
class S07(SpokenScene):
    def construct(self):
        oligo, sch, oligo_l, sch_l, sj, leg = rebuild_s06(self)
        pL = cell("cns", *SL)
        pR = cell("pns", *SR)
        hL, hR = header("cns"), header("pns")
        leg2 = legend(("tube", "crest"), 26, 3.55)
        # both panels are built at once; the icons move up to their headers
        self.play(FadeOut(leg[1]), FadeOut(oligo_l), FadeOut(sch_l),
                  Transform(VGroup(leg[0], leg[2]), leg2),
                  oligo.animate.scale(0.9 / 2.6).move_to(hL[0].get_center()),
                  sch.animate.scale(0.9 / 2.2).move_to(hR[0].get_center()),
                  FadeIn(hL[1]), FadeIn(hR[1]), FadeIn(pL[0]), FadeIn(pR[0]), Create(pL[1]), Create(pR[1]),
                  run_time=0.9)
        pR[2].set_opacity(0.35)
        self.add(pR[2])
        segsL, extraL = pL[2][:3], pL[2][3:]
        segsR, extraR = pR[2][:3], pR[2][3:]
        self.at("wrap")
        c_l = lab("central axons", TUBE, SL[0], -3.2, 28)
        p_l = lab("peripheral axons", CREST, SR[0], -3.2, 28)
        self.add(c_l, p_l)
        self.play(Create(extraL, lag_ratio=0.25), run_time=0.9)
        self.at("in myelin")
        my = T("myelin", 26, TUBE).move_to(V(SL[0], -2.05))
        self.play(*[GrowFromCenter(s) for s in segsL], FadeIn(my), run_time=0.9)
        self.at("myelinating schwann cells")
        self.play(Indicate(hR[1], color=CREST, scale_factor=1.1), pR[2].animate.set_opacity(1), run_time=0.8)
        self.at("wrap", nth=1)
        self.play(Indicate(extraR, color=CREST), run_time=0.8)
        self.at("myelin", nth=1)
        my2 = T("myelin", 26, CREST).move_to(V(SR[0], -2.05))
        self.play(*[GrowFromCenter(s) for s in segsR], FadeIn(my2), run_time=0.8)
        self.finish()


def rebuild_s07(scene, with_job=True):
    d = {}
    d["leg"] = legend(("tube", "crest"), 26, 3.55)
    d["hL"] = header("cns")
    d["hR"] = header("pns")
    d["pL"] = cell("cns", *SL)
    d["pR"] = cell("pns", *SR)
    d["cl"] = lab("central axons", TUBE, SL[0], -3.2, 28)
    d["pl"] = lab("peripheral axons", CREST, SR[0], -3.2, 28)
    d["my1"] = T("myelin", 26, TUBE).move_to(V(SL[0], -2.05))
    d["my2"] = T("myelin", 26, CREST).move_to(V(SR[0], -2.05))
    if with_job:
        d["sj"] = T("same job", 38, TEXT, font=TITLE_FONT).move_to(V(0, -0.5))
    add_all(scene, d)
    return d


# ---------------------------------------------------------------------------------------------------
class S08(SpokenScene):
    def construct(self):
        d = rebuild_s07(self)
        c1, c2 = olig_chips()
        b1, b2 = badge(c1), badge(c2)
        self.at("olig1")
        self.play(FadeOut(d["cl"]), FadeOut(d["pl"]), FadeOut(d["sj"]), FadeOut(d["my2"]), FadeIn(c1, shift=UP * 0.2),
                  run_time=0.5)
        self.at("olig2")
        self.play(FadeIn(c2, shift=UP * 0.2), run_time=0.4)
        self.at("have no")
        self.play(GrowFromCenter(b1), GrowFromCenter(b2), run_time=0.5)
        self.at("spinal cord", lead=0.1)
        parts = d["pL"][2]
        self.play(parts.animate.set_opacity(0.15), FadeOut(d["my1"]), run_time=0.6)
        self.play(Create(Cross(parts, stroke_color=RED, stroke_width=6)), run_time=0.4)
        self.at("should they lose")
        q = T("?", 72, RED, weight=BOLD).move_to(V(6.3, 2.75))
        ql = T("lose them too?", 30, RED).move_to(V(3.9, -3.15))
        self.play(FadeIn(q, scale=0.4), FadeIn(ql), run_time=0.6)
        self.at("schwann cells of their nerves", lead=0.0)
        self.play(Indicate(d["pR"][2], color=CREST, scale_factor=1.04), run_time=1.0)
        self.finish()


class S09Pause(NarratedScene):
    def construct(self):
        d = question_state(True)
        add_all(self, d)
        self.finish()


# ---------------------------------------------------------------------------------------------------
RING = V(2.5, 0.85)
CREST_POS = [V(3.25, 0.85), V(3.2, 1.08), V(3.1, 1.28), V(2.95, 1.42), V(3.3, 0.6)]


def crest_icon():
    ring = Circle(radius=0.5, stroke_color=TUBE, stroke_width=3, fill_color=TUBE, fill_opacity=0.18).move_to(RING)
    ring_t = T("cord", 22, TUBE).move_to(RING)
    dots = VGroup(*[Circle(radius=0.16, stroke_width=2, stroke_color=CREST, fill_color=CREST, fill_opacity=1).move_to(p) for p in CREST_POS])
    cl = T("neural crest", 26, CREST).move_to(V(5.0, 1.25))
    ld = leader(V(3.95, 1.25), V(3.55, 1.1), CREST)
    return VGroup(ring, ring_t), dots, cl, ld


def root_note():
    return VGroup(T("root Schwann cells also", 26, NOTE), T("need motor axons", 26, NOTE)).arrange(DOWN, buff=0.1).move_to(V(3.9, -1.85))


class S10(SpokenScene):
    def construct(self):
        d = question_state(True)
        add_all(self, d)
        still = lab("still there", CREST, SR[0], -3.15, 30)
        self.at("no")
        self.play(FadeOut(d["q"]), FadeOut(d["ql"]), FadeIn(still), FadeIn(root_note()), Indicate(d["pR"][2], color=CREST, scale_factor=1.04),
                  run_time=1.0)
        ring, dots, cl, ld = crest_icon()
        out = lab("outside the cord", CREST, 4.9, 0.6, 26)
        self.at("neural crest")
        self.play(FadeIn(ring), FadeIn(dots, scale=0.3), FadeIn(cl), Create(ld), run_time=0.5)
        self.add(dots.copy())
        self.at("outside the cord")
        tgt = [V(2.55, -0.4), V(3.9, -0.4), V(5.25, -0.4), V(2.55, -0.4), V(3.9, -0.4)]
        self.play(*[dot.animate.move_to(t) for dot, t in zip(dots, tgt)], FadeIn(out), run_time=1.0)
        self.play(FadeOut(dots), Indicate(d["pR"][2], color=CREST, scale_factor=1.04), run_time=0.5)
        no_need = lab("not expected to need Olig genes", CREST, 3.7, -3.15, 26)
        note = root_note()
        self.at("so they")
        self.wait(0.4)
        self.at("do not need")
        self.play(FadeOut(still), FadeIn(no_need), Indicate(d["c1"], color=RED), Indicate(d["c2"], color=RED),
                  run_time=0.8)
        self.finish()


def s10_end(scene):
    d = question_state(False)
    ring, dots, cl, ld = crest_icon()
    d["ring"], d["cl"], d["ld"], d["dots"] = ring, cl, ld, dots
    d["out"] = lab("outside the cord", CREST, 4.9, 0.6, 26)
    d["note"] = root_note()
    d["no_need"] = lab("not expected to need Olig genes", CREST, 3.7, -3.15, 26)
    add_all(scene, d)
    return d


# ---------------------------------------------------------------------------------------------------
CORE = V(-2.8, -0.05)
STRIP_Y = -1.05


def pmn_diagram():
    cord = Ellipse(width=6.1, height=6.3, stroke_color=TUBE, stroke_width=4,
                   fill_color=TUBE, fill_opacity=0.08).move_to(V(-3, 0))
    canal = Circle(radius=0.28, color=GREY).move_to(V(-3, 0.1))
    strip = RoundedRectangle(width=2.4, height=0.85, corner_radius=0.12, color=TUBE,
                             fill_color=TUBE, fill_opacity=0.8).move_to(V(-3, -0.9))
    mn = neuron(V(-4.65, -2.1), 1.6)
    opc = Circle(radius=0.46, color=TUBE, fill_color=TUBE, fill_opacity=0.8).move_to(V(-1.35, -1.9))
    arrows = VGroup(arr(strip.get_left(), mn.get_top(), TUBE, 3), arr(strip.get_right(), opc.get_top(), TUBE, 3))
    labels = VGroup(T("motor neurons", 26).move_to(V(-4.7, -3.5)),
                    T("OPCs", 26, TUBE).move_to(V(-1.35, -3.5)),
                    T("ventral pMN", 28, TUBE).move_to(V(-3, 0.7)),
                    T("dorsal", 26, GREY).move_to(V(-3, 3.45)))
    c1, c2 = olig_chips(size=40)
    c1.move_to(V(1.65, 2.7)); c2.move_to(V(4.5, 2.7))
    labels.add(leader(V(-4.65, -3.2), V(-4.65, -2.5), TEXT),
               leader(V(-1.35, -3.2), V(-1.35, -2.3), TUBE))
    labels.add(leader(c1.get_left(), V(-1.8, -0.5), TUBE))
    labels.add(T("OPCs = oligodendrocyte", 26, TUBE).move_to(V(3.25, -0.55)),
               T("precursors", 26, TUBE).move_to(V(3.25, -1.0)))
    heading = VGroup(T("same birthplace,", 34), T("lost together", 34)).arrange(DOWN).move_to(V(3.25, 0.8))
    hedge = VGroup(T("pMN cells take", 28, NOTE), T("another fate", 28, NOTE)).arrange(DOWN).move_to(V(3.25, -2))
    return cord, canal, strip, mn, opc, arrows, labels, c1, c2, heading, hedge

class S11(SpokenScene):
    def construct(self):
        cord, canal, strip, mn, opc, arrows, labels, c1, c2, heading, hedge = pmn_diagram()
        self.add(cord, canal, strip, mn, opc, arrows, labels, c1, c2)
        self.at("these mice")
        self.play(Indicate(strip, color=TUBE), run_time=0.65)
        self.at("motor neurons", lead=0)
        self.play(mn.animate.set_fill(opacity=0.08).set_stroke(GREY, opacity=0.8),
                  opc.animate.set_fill(opacity=0.08).set_stroke(GREY, opacity=0.8),
                  FadeIn(badge(c1)), FadeIn(badge(c2)), FadeIn(heading), FadeIn(hedge), run_time=0.65)
        self.at("made by")
        self.play(Indicate(arrows, color=TUBE), run_time=0.6)
        self.at("same strip")
        self.play(Indicate(strip), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------------
def row_chips():
    c1 = chip("Olig1", TEXT, 36, pad=0.24).move_to(V(-5.2, 2.3))
    c2 = chip("Olig2", TEXT, 36, pad=0.24).move_to(V(-5.2, 1.0))
    c3 = chip("ErbB3", TEXT, 36, pad=0.24).move_to(V(-5.2, -1.35))
    return c1, c2, c3


def ghost_row(cellmob):
    parts = cellmob[2]
    return [ghost(p.get_center(), 0.2, 3).set_color(RED) for p in parts]


def row1(final=True):
    d = {}
    d["p1L"] = cell("cns", *R1L, present=False)
    d["x1L"] = Cross(d["p1L"][2], stroke_color=RED, stroke_width=6)
    d["p1R"] = cell("pns", *R1R, present=True)
    d["l1L"] = lab("oligodendrocytes", TUBE, R1L[0], R1L[1] - 1.05, 24)
    d["l1R"] = lab("Schwann cells", CREST, R1R[0], R1R[1] - 1.05, 24)
    c1, c2, _ = row_chips()
    d["c1"], d["c2"] = c1, c2
    d["b1"], d["b2"] = badge(c1), badge(c2)
    return d


def row2(final=True, left_label="oligodendrocytes"):
    d = {}
    d["p2L"] = cell("cns", *R2L, present=True)
    d["p2R"] = cell("pns", *R2R, precursor=True)
    d["l2L"] = lab(left_label, TUBE, R2L[0], R2L[1] - 1.05, 24)
    _, _, c3 = row_chips()
    d["c3"] = c3
    d["b3"] = badge(c3)
    if final:
        d["p2R"][2].set_opacity(0.0)
        d["g2R"] = VGroup(*ghost_row(d["p2R"]))
        d["l2R"] = lab("Schwann cell precursors", CREST, R2R[0], R2R[1] - 1.05, 24)
    return d


def flat_list(d):
    out = []
    for m in d.values():
        out.extend(m if isinstance(m, (tuple, list)) else [m])
    return out


class S12(SpokenScene):
    def construct(self):
        # carry the end of s11 (the cord cross-section) as it was
        parts = pmn_diagram()
        parts[3].set_fill(opacity=0.08).set_stroke(GREY, opacity=0.8)
        parts[4].set_fill(opacity=0.08).set_stroke(GREY, opacity=0.8)
        cord = VGroup(*parts, badge(parts[7]), badge(parts[8]))
        self.add(cord)
        # the cord scene is replaced at once by row 1: the result of the first example
        leg = legend(("tube", "crest"), 26, 3.55)
        r1 = row1()
        self.at("the reverse")
        self.play(FadeOut(cord), FadeIn(leg), *[FadeIn(m) for m in flat_list(r1)], run_time=0.8)
        r2 = row2(final=False)
        # row 1 dims while row 2 builds
        self.at("remove the receptor")
        self.play(*[m.animate.set_opacity(0.3) for m in flat_list(r1)],
                  FadeIn(r2["p2L"]), FadeIn(r2["p2R"]), FadeIn(r2["l2L"]), run_time=0.8)
        self.at("receptor", lead=-0.4)
        self.play(FadeIn(r2["c3"], shift=UP * 0.2), run_time=0.4)
        self.play(GrowFromCenter(r2["b3"]), run_time=0.3)
        self.at("and nerves lose")
        gh = VGroup(*ghost_row(r2["p2R"]))
        self.play(*[p.animate.shift(DOWN * 0.5).set_opacity(0.0) for p in r2["p2R"][2]], FadeIn(gh), run_time=0.8)
        self.at("schwann cell")
        lab2 = lab("Schwann cell precursors", CREST, R2R[0], R2R[1] - 1.05, 24)
        self.play(FadeIn(lab2), run_time=0.4)
        self.at("oligodendrocytes do not need it")
        self.play(Indicate(r2["p2L"][2], color=TUBE, scale_factor=1.04), FadeOut(r2["l2L"]),
                  FadeIn(lab("develops normally", TUBE, R2L[0], R2L[1] - 1.05, 24)), run_time=1.0)
        self.finish()


def final_rows(scene, left_label="develops normally"):
    leg = legend(("tube", "crest"), 26, 3.55)
    r1 = row1()
    r2 = row2(True, left_label)
    scene.add(leg, *flat_list(r1), *flat_list(r2))
    return leg, r1, r2


class S13Beat(NarratedScene):
    def construct(self):
        final_rows(self)
        self.finish()


# ---------------------------------------------------------------------------------------------------
class S14(SpokenScene):
    def construct(self):
        leg, r1, r2 = final_rows(self)
        plain = T("same job, different early requirements", 36, TEXT, font=TITLE_FONT).move_to(V(0, -3.3))
        first = T("same job", 36, TEXT, font=TITLE_FONT).move_to(V(0, -3.3))
        self.at("same job")
        self.play(FadeIn(first, scale=0.9), run_time=0.5)
        faded = T("same job, different early requirements", 36, TEXT, font=TITLE_FONT, t2c={"job": "#4A4A4A"}) \
            .move_to(V(0, -3.3))
        names = [r1["l1L"], r1["l1R"], r2["l2L"], r2["l2R"]]
        self.at("different early requirements")
        self.play(Transform(first, plain), run_time=0.4)
        # the word 'job' fades; the birthplace colours stay on the panels and the legend
        self.play(Transform(first, faded), *[n.animate.set_color(GREY) for n in names],
                  Indicate(r1["c1"], color=GOLD), Indicate(r1["c2"], color=GOLD), Indicate(r2["c3"], color=GOLD),
                  run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------------
class S14b(SpokenScene):
    def construct(self):
        leg = legend(("tube", "crest"), 26, 3.55)
        oc = glia("oligo", V(-4.3, 1.55), 2.8)
        sc = glia("schwann", V(4.3, 1.55), 2.0)
        ol = T("oligodendrocyte", 28, TUBE).move_to(V(-4.3, 0.1))
        sl = T("Schwann cell", 28, CREST).move_to(V(4.3, 0.1))
        ob = T("born in the neural tube", 24, TUBE).move_to(V(-4.3, -0.4))
        sb = T("born in the neural crest", 24, CREST).move_to(V(4.3, -0.4))
        self.add(leg, oc, sc, ol, sl, ob, sb)
        card = chip("Sox10", TEXT, 46, pad=0.32).move_to(V(0, 1.55))
        a1 = arr(V(-1.5, 1.55), V(-2.65, 1.55), TEXT, 5, 0.2)
        a2 = arr(V(1.5, 1.55), V(2.6, 1.55), TEXT, 5, 0.2)
        shared = T("some genes are shared", 36, TEXT, font=TITLE_FONT).move_to(V(0, -3.3))
        self.add(card, a1, a2, shared)
        self.at("does not guarantee")
        self.play(Indicate(card), run_time=0.6)

        def stages(cx, col, lit):
            bar = VGroup(*[Rectangle(width=0.9, height=0.5, stroke_color=GREY, stroke_width=2, fill_color=GREY,
                                     fill_opacity=0.12).move_to(V(cx - 1.35 + 0.9 * i, -1.35)) for i in range(4)])
            bar[lit].set_stroke(col).set_fill(col, 0.85)
            axis = arr(V(cx - 1.9, -1.95), V(cx + 1.9, -1.95), GREY, 3, 0.15)
            early = T("early", 24, GREY).move_to(V(cx - 1.45, -2.4))
            late = T("late", 24, GREY).move_to(V(cx + 1.45, -2.4))
            dev = T("development", 24, GREY).move_to(V(cx, -2.95))
            return bar, VGroup(axis, early, late, dev)
        (b1, ax1), (b2, ax2) = stages(-4.3, TUBE, 2), stages(4.3, CREST, 0)
        t1 = T("needed at one stage", 24, TUBE).move_to(V(-4.3, -0.8))
        t2 = T("needed at another", 24, CREST).move_to(V(4.3, -0.8))
        self.at("both lineages")
        self.play(FadeIn(ax1), FadeIn(ax2), run_time=0.5)
        self.at("at different stages")
        self.play(FadeIn(b1), FadeIn(b2), FadeIn(t1), FadeIn(t2), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------------
IX = [-5.25, -3.15, -1.05, 1.05, 3.15, 5.25]
IY = -0.5
KINDS6 = ["astro", "oligo", "epend", "micro", "schwann", "sat"]
COLS6 = [TUBE, TUBE, TUBE, YOLK, CREST, CREST]
LINE1 = "Glia is a job, not a lineage."
LINE2 = "Ask where the cell was born."
LINE3 = "And what its progenitor needed from that gene, then."
LINE4 = "What the cell does: a weaker guide."
CARDY = [2.85, 2.2, 1.55, 0.9]


def icon_row(colored):
    return [glia(k, V(x, IY), (1.4 if k == "schwann" else 1.9), (c if colored else GREY)) for k, x, c in zip(KINDS6, IX, COLS6)]


def group_marks():
    br = [bracket(-5.9, -0.45, -1.5, TUBE), bracket(0.45, 1.65, -1.5, YOLK), bracket(2.55, 5.85, -1.5, CREST)]
    lb = [lab("neural tube", TUBE, -3.15, -2.1, 28), lab("yolk sac", YOLK, 1.05, -2.1, 28),
          lab("neural crest", CREST, 4.2, -2.1, 28)]
    return br, lb


def card_line(n, text=None, size=None, color=TEXT):
    text = text or [LINE1, LINE2, LINE3, LINE4][n]
    size = size or [40, 40, 34, 30][n]
    t = T(text, size, color, font=TITLE_FONT).move_to(V(0, CARDY[n]))
    return fit(t, max_w=12.2)


def card_head():
    return T("the idea to carry", 28, GOLD).move_to(V(0, 3.55))


class S15(SpokenScene):
    def construct(self):
        head = card_head()
        icons = icon_row(False)
        line = card_line(0)
        self.add(head, *icons, line)
        self.at("so here is")
        self.play(Indicate(head, color=GOLD), run_time=0.6)
        one = bracket(-6.3, 6.3, -1.5, GREY)
        one_l = lab("one job", LIGHT, 0, -2.1, 30)
        self.at("is a job")
        self.play(Indicate(line, color=GOLD, scale_factor=1.03), Create(one), FadeIn(one_l), run_time=0.7)
        br, lb = group_marks()
        self.at("not a lineage")
        self.play(FadeOut(one), FadeOut(one_l),
                  *[Transform(i, glia(k, i.get_center(), (1.4 if k == "schwann" else 1.9), c)) for i, k, c in zip(icons, KINDS6, COLS6)],
                  run_time=0.7)
        self.play(*[Create(b) for b in br], *[FadeIn(l) for l in lb], run_time=0.7)
        self.finish()


def rebuild_s15(scene):
    icons = icon_row(True)
    br, lb = group_marks()
    line = card_line(0)
    head = card_head()
    scene.add(*icons, *br, *lb, line, head)
    return icons, br, lb, line, head


class S16(SpokenScene):
    def construct(self):
        icons, br, lb, line, head = rebuild_s15(self)
        l2 = card_line(1)
        self.play(FadeIn(l2), run_time=0.3)
        # the gene is an input to the rule, not something struck out
        gene = chip("a gene", TEXT, 26, pad=0.22).move_to(V(-4.4, 1.55))
        ga = arr(V(-3.3, 1.55), V(-2.2, 1.55), TEXT, 5, 0.2)
        gq = T("which glia are lost?", 26, LIGHT).move_to(V(0.1, 1.55))
        self.at("a gene")
        self.play(FadeIn(gene, shift=RIGHT * 0.2), run_time=0.4)
        self.play(GrowArrow(ga), FadeIn(gq), run_time=0.5)
        self.at("ask where")
        self.play(FadeOut(VGroup(gene, ga, gq)), Indicate(l2, color=GOLD, scale_factor=1.03), run_time=0.6)
        self.at("was born")
        self.play(*[Indicate(l, color=GOLD, scale_factor=1.2) for l in lb], run_time=1.0)
        self.finish()


class S17(SpokenScene):
    def construct(self):
        head = card_head()
        t1, t2, t3 = card_line(0), card_line(1), card_line(2)
        prog = Circle(radius=1.15, stroke_color=TUBE, stroke_width=4,
                      fill_color=TUBE, fill_opacity=0.2).move_to(V(-4.3, -1.15))
        pl = T("progenitor", 28, TUBE).move_to(prog)
        gene = chip("gene", TEXT, 36).move_to(V(-0.9, -1.15))
        need = arr(V(-1.95, -1.15), V(-3.1, -1.15), TEXT, 6)
        nl = T("needed", 28).move_to(V(-2.5, -0.55))
        axis = arr(V(-5.9, -2.75), V(5.9, -2.75), GREY, 4)
        tl = T("time", 26, GREY).move_to(V(5.5, -3.25))
        mk = bracket(-5.3, -3.3, -2.75, GOLD, up=0.25, w=6)
        mkl = T("that time", 28, GOLD).move_to(V(-4.3, -3.25))
        cd = glia("schwann", V(4.5, -1.0), 1.9, GREY)
        cdl = T("what the cell does", 28, GREY).move_to(V(4.5, -2.1))
        self.add(head, t1, t2, prog, pl, gene, need, nl, axis, tl, mk, mkl, cd, cdl)
        self.at("then ask")
        self.play(FadeIn(t3), run_time=0.5)
        self.at("its progenitor")
        self.play(Indicate(prog, color=TUBE, scale_factor=1.03), run_time=0.4)
        self.at("needed from")
        self.play(Indicate(gene, color=TEXT), Indicate(need, color=TEXT), run_time=0.5)
        self.at("at that time")
        self.play(Indicate(mk, color=GOLD), run_time=0.6)
        l4 = card_line(3, color=LIGHT)
        self.at("what the cell does")
        self.play(FadeIn(l4), Indicate(cd, color=GREY), run_time=0.5)
        self.at("weaker guide")
        self.play(Indicate(l4, color=TEXT, scale_factor=1.03), cd.animate.set_opacity(0.45), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------------
def deficit(t):
    # Normalized schematic recovery: smoothstep expansion of surviving waves,
    # exactly normal at t >= 8; no fitted rate or measured times are implied.
    u = np.clip(t / 8.0, 0.0, 1.0)
    return 0.3 + 0.7 * (3 * u**2 - 2 * u**3)


class S18(SpokenScene):
    def construct(self):
        ttl = T("First deficit versus final count", 34, TEXT, font=TITLE_FONT).move_to(V(-1, 3.4))
        tag = T("schematic", 26, GREY).move_to(V(5.7, 3.4))
        ax = Axes(x_range=[0, 10, 2], y_range=[0, 1.2, 0.4], x_length=8.8, y_length=5.4,
                  axis_config={"color": GREY, "stroke_width": 3, "include_ticks": False, "include_tip": True},
                  ).move_to(V(-0.8, -0.3))
        xl = T("time after the gene is removed", 26, GREY).move_to(V(-0.8, -3.35))
        yt = [T(s, 26, GREY).move_to(ax.c2p(0, v) + V(-0.65, 0)) for s, v in (("0", 0.0), ("50%", 0.5), ("100%", 1.0))]
        yl = T("cells, % of normal", 26, GREY).move_to(V(-3.0, 2.65))
        normal = DashedVMobject(ax.plot(lambda t: 1.0, x_range=[0, 10], color=GREY, stroke_width=3), num_dashes=30)
        nl = T("normal", 26, GREY).move_to(ax.c2p(9.0, 1.0) + V(0, 0.4))
        mut = ax.plot(deficit, x_range=[0, 10], color=RED, stroke_width=6)
        self.add(ax, xl, *yt, yl, normal, nl, tag, ttl)
        self.at("the rule predicts")
        # first deficit: anchored at the start of the curve
        x0 = 0.3
        start = Dot(ax.c2p(x0, deficit(x0)), color=RED, radius=0.11)
        gap1 = DoubleArrow(ax.c2p(x0, deficit(x0) + 0.02), ax.c2p(x0, 0.98), color=RED, stroke_width=6, buff=0,
                           tip_length=0.2)
        gl = T("first deficit", 28, RED).move_to(ax.c2p(2.2, 0.14))
        self.at("first deficit")
        self.play(FadeIn(start, scale=0.4), Create(gap1), FadeIn(gl), run_time=0.7)
        # the rest of the curve: the animal compensates; the final count is read outside the plot
        fc = T("final count", 28, TEXT).move_to(V(5.3, 1.1))
        fc2 = T("back to normal", 26, NOTE).move_to(V(5.3, 0.65))
        fc3 = T("in this example", 26, NOTE).move_to(V(5.3, 0.3))
        fld = leader(V(4.1, 1.1), ax.c2p(9.9, deficit(9.9)), TEXT)
        self.at("not the final count")
        self.play(Create(mut), run_time=1.2)
        self.play(FadeIn(fc), Create(fld), FadeIn(fc2), FadeIn(fc3), run_time=0.5)
        comp = T("animal compensates", 26, TEXT).move_to(V(5.3, -1.6))
        comp_a = arr(V(4.2, -1.3), ax.c2p(5.5, deficit(5.5)) + V(0.15, -0.1), TEXT, 4, 0.18)
        self.at("compensates")
        self.play(FadeIn(comp), GrowArrow(comp_a), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------------
class S19Take(SpokenScene):
    def construct(self):
        nq = T("Next question", 44, GOLD, font=TITLE_FONT).move_to(V(0, 3.15))
        self.add(nq)
        self.at("next question")
        c = V(-2.4, 0.1)
        body = Circle(radius=1.7, stroke_color=TEXT, stroke_width=4, fill_color=CREST, fill_opacity=0.25).move_to(c)
        nuc = Circle(radius=0.75, stroke_color=CREST, stroke_width=3, fill_color=CREST, fill_opacity=0.7).move_to(c + V(-0.25, 0.15))
        specks = VGroup(*[Circle(radius=0.07, stroke_width=0, fill_color=CREST, fill_opacity=0.8)
                          .move_to(c + V(1.0 * np.cos(a), 1.0 * np.sin(a))) for a in np.linspace(0.3, 6.0, 7)])
        cellg = VGroup(body, nuc, specks)
        sl = T("a stained cell", 30, TEXT).move_to(V(-2.4, -2.2))
        qm = T("?", 240, RED, weight=BOLD).move_to(V(2.6, -0.1))
        ql = T("How do you find out where a cell was born?", 38, TEXT, font=TITLE_FONT).move_to(V(0, -3.2))
        fit(ql, max_w=12.2)
        self.add(cellg, sl, qm, ql)
        self.at("how do you find out")
        self.play(Indicate(qm, scale_factor=1.05), run_time=0.5)
        self.finish()


class S20End(EndCard):
    LINE = "Glia is a job, not a lineage."
