"""Neural crest, chapter 1: One Border, Many Destinations.

COLOR MAP (one colour per concept, shared by all three chapters; taken from scenes.old.py)
  YELLOW = neural crest cells and the crest border (gold band)
  TEAL   = neurons and glia of the gut wall, sensory/sympathetic ganglia, Schwann cells (peripheral neural derivatives)
  TEXT   = pigment (white forelock, melanocytes) and skeleton (bone, cartilage): neutral white
  GREY   = embryonic structures, outlines, labels
  RED    = failure / missing development (distal gut, broken gene)
  GOLD   = explanatory highlights and the gene icon
  SLATE  = neural plate and neural tube
  SKIN   = pale future skin
  LEVEL colours (location along the body only, never a cell type):
         cranial INDIGO, vagal GREEN, cardiac PURPLE, trunk ORANGE, sacral PINK
         (cranial is indigo, not teal-blue, so it cannot be mistaken for neurons)
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

SLATE = "#6B7A99"
SKIN = "#D6BFA3"
HAIR = "#8A7869"
INDIGO = "#5C86F2"
PURPLE = "#B58CE0"
ORANGE = "#F2994A"
PINK = "#E58FB5"
LEVELCOL = dict(cranial=INDIGO, vagal=GREEN, cardiac=PURPLE, trunk=ORANGE, sacral=PINK)


def P3(x, y):
    return np.array([x, y, 0.0])


def dimc(color, f=0.3):
    return interpolate_color(ManimColor(BG), ManimColor(color), f)


def lab(txt, x, y, size=26, color=TEXT, **kw):
    return T(txt, size, color, **kw).move_to(P3(x, y))


def crest_cell(r=0.17):
    return Circle(radius=r, stroke_color=YELLOW, stroke_width=2, fill_color=YELLOW, fill_opacity=0.9)


def qmark(x, y):
    q = T("?", 56, GOLD, weight=BOLD)
    back = Circle(radius=0.42, stroke_width=0, fill_color=BG, fill_opacity=1)
    return VGroup(back, q).move_to(P3(x, y))


def swap(old, new, rt=0.5):
    """Fade one label out and its replacement in (no letter-by-letter morph)."""
    return [Succession(FadeOut(old, run_time=0.2), FadeIn(new, run_time=0.3))]


def arrow(a, b, color=YELLOW, sw=3.5):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=sw, max_tip_length_to_length_ratio=0.18)


def diamond(p, s=0.3):
    return Square(s, fill_color=GOLD, fill_opacity=1, stroke_color=BG, stroke_width=2).rotate(PI / 4).move_to(p)


# ---------------------------------------------------------------------------------------------
# the child's face and the gut (chapters open with them; the puzzle returns at the end)
# ---------------------------------------------------------------------------------------------
FACE_C = (-3.2, 0.35)
FACE_R = 2.1
GUT_X0, GUT_X1 = 1.0, 6.6
GUT_H = 2.8


def make_face(cx=FACE_C[0], cy=FACE_C[1], r=FACE_R):
    head = Circle(r, stroke_color=SKIN, stroke_width=3, fill_color=SKIN, fill_opacity=0.35).move_to(P3(cx, cy))
    hair = AnnularSector(inner_radius=r * 0.8, outer_radius=r * 1.07, angle=PI * 0.9, start_angle=PI * 0.05,
                         arc_center=P3(cx, cy), fill_color=HAIR, fill_opacity=1, stroke_width=0)
    ears = VGroup(*[Ellipse(width=0.34 * r, height=0.6 * r, stroke_color=SKIN, stroke_width=3, fill_color=SKIN,
                            fill_opacity=0.5).move_to(P3(cx + sgn * r * 1.02, cy - 0.05)) for sgn in (-1, 1)])
    eyes = VGroup(*[Circle(0.11, stroke_width=0, fill_color=TEXT, fill_opacity=1).move_to(P3(cx + sgn * 0.62, cy + 0.2))
                    for sgn in (-1, 1)])
    mouth = Arc(radius=0.7, start_angle=PI + 0.55, angle=PI - 1.1, arc_center=P3(cx, cy + 0.2), color=TEXT,
                stroke_width=3)
    forelock = Ellipse(width=0.58, height=1.25, stroke_color=TEXT, stroke_width=1, fill_color=TEXT, fill_opacity=1)
    ang = np.deg2rad(62)
    forelock.rotate(ang - PI / 2).move_to(P3(cx + r * 0.95 * np.cos(ang), cy + r * 0.95 * np.sin(ang)))
    base = VGroup(ears, head, hair, eyes, mouth)
    return base, forelock, ears


def make_gut(x0=GUT_X0, x1=GUT_X1, y=0.35, h=GUT_H, frac=0.58):
    ln = x1 - x0
    tube = RoundedRectangle(corner_radius=1.0, width=ln, height=h, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.14).move_to(P3((x0 + x1) / 2, y))
    xs = np.linspace(x0 + 0.8, x0 + frac * ln - 0.45, 6)
    dots = VGroup(*[Circle(0.2, stroke_width=0, fill_color=TEAL, fill_opacity=1).move_to(P3(x, y + (0.5 if i % 2 else -0.5)))
                    for i, x in enumerate(xs)])
    dlen = ln * (1 - frac) - 0.05
    distal = RoundedRectangle(corner_radius=0.9, width=dlen, height=h + 0.2, stroke_color=RED, stroke_width=3,
                              fill_color=RED, fill_opacity=0.10)
    distal.move_to(P3(x1 - dlen / 2 - 0.02, y))
    return tube, dots, distal


class FaceGut:
    """Everything the opening puzzle uses, built once so scenes 1, 2, 16 and 17 share it."""

    def __init__(self, cy=0.35):
        self.cy = cy
        self.face, self.forelock, self.ears = make_face(cy=cy)
        self.tube, self.dots, self.distal = make_gut(y=cy)
        # one question mark at each finding: the ear, the forelock and the gut
        self.qs = [qmark(-6.25, cy + 0.55), qmark(-4.2, cy + 2.55), qmark(5.3, cy + 2.25)]

    def labels(self):
        fx = FACE_C[0] - FACE_R * 1.02
        face_lab = lab("hearing loss", -4.75, -3.05, 26)
        ear_line = Line(P3(fx, self.cy - 0.72), P3(fx, -2.8), color=GREY, stroke_width=2.5)
        fore_lab = lab("white forelock", -0.7, 3.25, 26)
        fore_line = Line(P3(-1.6, 3.0), P3(-2.0, 2.5), color=GREY, stroke_width=2.5)
        gut_lab = lab("no nerve cells", 5.0, -1.7, 26, RED)
        return face_lab, ear_line, fore_lab, fore_line, gut_lab


# ---------------------------------------------------------------------------------------------
# the folding sheet (scenes 3, 4, 5): 18 cells, computed geometry
# ---------------------------------------------------------------------------------------------
CW = 0.68
KINDS = ["skin"] * 3 + ["crest"] * 2 + ["plate"] * 8 + ["crest"] * 2 + ["skin"] * 3
NCELL = len(KINDS)
SL = 12 * CW
PHI = 0.995 * PI
Y0 = -3.0
TH0 = 4.6          # thickness of the flat neural plate (tall columnar cells)
KCOL = {"skin": SKIN, "crest": YELLOW, "plate": SLATE, "grey": GREY}
KFILL = {"skin": 0.5, "crest": 0.9, "plate": 0.65, "grey": 0.4}


def fold_geom(t):
    phi = PHI * t
    k = 2 * phi / SL
    th = TH0 - (TH0 - 0.6) * min(1.0, t / 0.5)
    ths = 0.9 - 0.3 * t

    def pn(s):
        if k < 1e-6:
            return np.array([s, 0.0]), np.array([0.0, 1.0])
        a = k * s
        return np.array([np.sin(a) / k, (1 - np.cos(a)) / k]), np.array([-np.sin(a), np.cos(a)])

    EL, _ = pn(-SL / 2)
    ER, _ = pn(SL / 2)
    cells = []
    for i in range(NCELL):
        if i < 3:
            j = 2 - i
            xa = EL[0] - j * CW
            xb = xa - CW
            y = EL[1]
            c = [(xa, y), (xb, y), (xb, y + ths), (xa, y + ths)]
        elif i >= 15:
            j = i - 15
            xa = ER[0] + j * CW
            xb = xa + CW
            y = ER[1]
            c = [(xa, y), (xb, y), (xb, y + ths), (xa, y + ths)]
        else:
            s0 = -SL / 2 + (i - 3) * CW
            p0, n0 = pn(s0)
            p1, n1 = pn(s0 + CW)
            c = [p0, p1, p1 + th * n1, p0 + th * n0]
        cells.append(np.array(c, float))
    return cells, pn, th, k


class Sheet:
    def __init__(self, t=0.0, Z=1.0, cx=0.0, cy=Y0, kinds=None):
        self.kinds = list(kinds or KINDS)
        self.cells = [Polygon(P3(i, 0), P3(i + 1, 0), P3(i + 1, 1), P3(i, 1)) for i in range(NCELL)]
        for c, k in zip(self.cells, self.kinds):
            c.set_fill(KCOL[k], KFILL[k]).set_stroke(BG, 2.5)
        self.apply(t, Z, cx, cy)

    def apply(self, t, Z=1.0, cx=0.0, cy=Y0):
        self.t, self.Z, self.cx, self.cy = t, Z, cx, cy
        geo, self.pn, self.th, self.k = fold_geom(t)
        self.corners = []
        for poly, c in zip(self.cells, geo):
            pts = [P3(cx + Z * x, cy + Z * y) for x, y in c]
            self.corners.append(pts)
            poly.set_points_as_corners(pts + [pts[0]])

    def arc(self, s):
        """Position and inward normal (scene units) of the outer surface at arclength s from the dorsal-ventral midpoint."""
        p, n = self.pn(s)
        return P3(self.cx + self.Z * p[0], self.cy + self.Z * p[1]), P3(n[0], n[1])

    def centroid(self, i):
        return sum(self.corners[i]) / 4

    def anim(self, t0, t1, Z0=1.0, Z1=1.0, cy0=Y0, cy1=Y0):
        def f(m, a):
            a = smooth(a)
            self.apply(t0 + (t1 - t0) * a, Z0 + (Z1 - Z0) * a, 0.0, cy0 + (cy1 - cy0) * a)
        return UpdateFromAlphaFunc(VGroup(*self.cells), f)

    def recolor(self, idxs, kind):
        return [self.cells[i].animate.set_fill(KCOL[kind], KFILL[kind]) for i in idxs]


SKIN_IDX = [0, 1, 2, 15, 16, 17]
CREST_IDX = [3, 4, 13, 14]
PLATE_IDX = list(range(5, 13))


def paint_stage(sh, stage):
    for i, c in enumerate(sh.cells):
        k = "grey" if stage == "grey" else sh.kinds[i]
        c.set_fill(KCOL[k], KFILL[k])


def xspan(sh, idx):
    xs = [p[0] for i in idx for p in sh.corners[i]]
    return min(xs), max(xs)


def sheet_labels(sh):
    """The scene-3 labels, built from a flat sheet at t=0 (scene 4 rebuilds them, then lets them go)."""
    top = sh.cy + TH0
    x_pl, x_sl, x_sr = xspan(sh, PLATE_IDX), xspan(sh, [0, 1, 2]), xspan(sh, [15, 16, 17])
    x_all = (x_sl[0], x_sr[1])

    def bracket(x0, x1, y, col):
        return VGroup(Line(P3(x0, y), P3(x1, y), color=col, stroke_width=3),
                      Line(P3(x0, y), P3(x0, y - 0.15), color=col, stroke_width=3),
                      Line(P3(x1, y), P3(x1, y - 0.15), color=col, stroke_width=3))
    d = {}
    d["ecto_br"] = bracket(x_all[0] + 0.05, x_all[1] - 0.05, top + 0.95, GREY)
    d["ecto"] = lab("ectoderm", 0, top + 1.4, 30, GREY)
    d["plate"] = lab("neural plate", (x_pl[0] + x_pl[1]) / 2, top + 0.4, 28, SLATE)
    sky = sh.cy + 0.9 + 0.38
    d["skinL"] = lab("future skin", (x_sl[0] + x_sl[1]) / 2, sky, 26, SKIN)
    d["skinR"] = lab("future skin", (x_sr[0] + x_sr[1]) / 2, sky, 26, SKIN)
    bl = sum(xspan(sh, [3, 4])) / 2
    brr = sum(xspan(sh, [13, 14])) / 2
    d["crL"] = lab("neural crest", bl, sh.cy - 0.42, 26, YELLOW)
    d["crR"] = lab("neural crest", brr, sh.cy - 0.42, 26, YELLOW)
    return d


# ---------------------------------------------------------------------------------------------
# the body axis and its five levels (scenes 7 to 10)
# ---------------------------------------------------------------------------------------------
BODY_X = -3.9
BANDS = [("cranial", 3.4, 2.1), ("vagal", 2.1, 1.3), ("cardiac", 1.3, 0.5), ("trunk", 0.5, -1.9), ("sacral", -1.9, -3.4)]


def make_body():
    outline = RoundedRectangle(corner_radius=0.5, width=1.06, height=6.9, stroke_color=GREY, stroke_width=3,
                               fill_opacity=0).move_to(P3(BODY_X, 0))
    bands = {}
    order = []
    cr = RoundedRectangle(corner_radius=0.45, width=0.94, height=1.9, stroke_width=0).move_to(P3(BODY_X, 3.4 - 0.95))
    sa = RoundedRectangle(corner_radius=0.45, width=0.94, height=2.1, stroke_width=0).move_to(P3(BODY_X, -3.4 + 1.05))
    bands["cranial"], bands["sacral"] = cr, sa
    for name, ytop, ybot in BANDS:
        if name not in bands:
            bands[name] = Rectangle(width=0.94, height=ytop - ybot, stroke_width=0).move_to(P3(BODY_X, (ytop + ybot) / 2))
    for name in ("cranial", "sacral", "vagal", "cardiac", "trunk"):
        bands[name].set_fill(LEVELCOL[name], 1.0)
        order.append(bands[name])
    labels = {}
    for name, ytop, ybot in BANDS:
        t = T(name, 26, LEVELCOL[name])
        t.move_to(P3(BODY_X - 0.62 - t.width / 2, (ytop + ybot) / 2))
        labels[name] = t
    return outline, bands, labels, order


def set_levels(bands, labels, active=None, f_dim=0.28):
    for name in bands:
        on = active is None or name in active
        col = LEVELCOL[name]
        bands[name].set_fill(col if on else dimc(col, f_dim), 1.0)
        labels[name].set_color(col if on else dimc(col, 0.5))


def add_body(scene, active=None):
    outline, bands, labels, order = make_body()
    set_levels(bands, labels, active)
    scene.add(*order, outline, *labels.values())
    return outline, bands, labels


def stream(path, color=YELLOW, sw=3, op=0.5):
    return VMobject(color=color, stroke_width=sw).set_points(path.get_points()).set_stroke(opacity=op)


def flow_group(scene, paths, n=3, rt=1.5, lag=0.2, r=0.14, color=YELLOW):
    """Dots travel along every path together; returns the dots."""
    dots, anims = [], []
    for p in paths:
        for j in range(n):
            d = Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=0.95).move_to(p.get_start())
            dots.append(d)
            anims.append(Succession(Wait(j * lag * rt / n), MoveAlongPath(d, p, run_time=rt * (1 - lag))))
    scene.add(*dots)
    scene.play(*anims, run_time=rt)
    return dots


# ---------------------------------------------------------------------------------------------
# the idea card (scenes 11 to 14, 19)
# ---------------------------------------------------------------------------------------------
FATE_DEF = [("bone and cartilage", TEXT), ("gut neurons", TEAL), ("sensory neurons", TEAL), ("pigment cells", TEXT)]
BAND_X = -3.7
DOT_X = 0.7
FAV = [2, 3]    # sensory neurons and pigment cells: the fates a trunk-level start favours
LINE1 = "the start biases the options"
LINE2 = "route and stopping place help choose"
ROW1, ROW2 = -2.65, -3.2


class Card:
    def __init__(self, gap=1.1, top=2.0, title=True):
        self.frame = RoundedRectangle(corner_radius=0.3, width=12.9, height=7.5, stroke_color=GOLD, stroke_width=2.5,
                                      stroke_opacity=0.45, fill_opacity=0)
        ys = [top - gap * i for i in range(4)]
        self.ys = ys
        cyc = sum(ys) / 4
        self.cyc = cyc
        sp = 0.59 * gap
        self.cells = VGroup(*[crest_cell(0.24).move_to(P3(BAND_X, cyc + (2 - i) * sp)) for i in range(5)])
        self.band_y = cyc - 2 * sp - 0.7
        self.band_label = lab("crest border", BAND_X, self.band_y, 26, YELLOW)
        self.src = P3(BAND_X + 0.42, cyc)
        self.dots, self.fate_labels, self.arrows = [], [], []
        for (name, col), y in zip(FATE_DEF, ys):
            d = Circle(0.22, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.2).move_to(P3(DOT_X, y))
            self.dots.append(d)
            tl = T(name, 28, col)
            tl.move_to(P3(1.4 + tl.width / 2, y))
            self.fate_labels.append(tl)
            self.arrows.append(arrow(self.src, P3(DOT_X - 0.42, y), YELLOW, 3.2))
        self.title1 = T("One border,", 48, TEXT, font=TITLE_FONT)
        self.title2 = T("many destinations", 48, GOLD, font=TITLE_FONT)
        self.title = VGroup(self.title1, self.title2).arrange(RIGHT, buff=0.3).move_to(P3(0, 3.05))

    def start_label(self):
        return T("start: one level\n(here, trunk)", 26, YELLOW, line_spacing=0.7).move_to(P3(BAND_X, self.band_y - 0.1))

    def lines(self, which):
        t = [T(LINE1, 34, GOLD).move_to(P3(0, ROW1)), T(LINE2, 34, GOLD).move_to(P3(0, ROW2))]
        return t[which]

    def weights(self, on=True):
        """The fates a trunk-level start favours get thick arrows; the others thin and faint."""
        out = []
        for i, (a, d) in enumerate(zip(self.arrows, self.dots)):
            if i in FAV:
                out += [a.animate.set_stroke(width=9), d.animate.set_fill(d.get_color(), 0.7)]
            else:
                out += [a.animate.set_stroke(width=1.5, opacity=0.3)]
        return out

    def diamonds(self):
        return [diamond(self.arrows[i].point_from_proportion(p)) for i in FAV for p in (0.3, 0.55, 0.8)]

    def ring(self):
        return Circle(0.36, color=GOLD, stroke_width=4).move_to(self.dots[3].get_center())


def card_base(scene, c, stage):
    """Add the card as it stands at the start of scene `stage` (12, 13 or 14): what earlier scenes built."""
    scene.add(c.frame, c.title, c.cells)
    for a, d, l in zip(c.arrows, c.dots, c.fate_labels):
        scene.add(a, d, l)
    objs = {}
    if stage >= 12:
        scene.remove(c.band_label)
        objs["band"] = c.start_label()
        br = Brace(c.cells, LEFT, buff=0.12, color=YELLOW)
        pl = T("population", 26, YELLOW).next_to(br, LEFT, buff=0.15)
        objs["br"], objs["pl"] = br, pl
        objs["l1"] = c.lines(0)
        scene.add(objs["band"], br, pl, objs["l1"])
        for i, (a, d) in enumerate(zip(c.arrows, c.dots)):
            if i in FAV:
                a.set_stroke(width=9)
                d.set_fill(d.get_color(), 0.7)
            else:
                a.set_stroke(width=1.5, opacity=0.3)
    else:
        scene.add(c.band_label)
    if stage >= 13:
        objs["dia"] = c.diamonds()
        objs["ring"] = c.ring()
        objs["l2"] = c.lines(1)
        c.dots[3].set_fill(c.dots[3].get_color(), 1.0)
        scene.add(*objs["dia"], objs["ring"], objs["l2"])
    return objs


# ---------------------------------------------------------------------------------------------
# scenes
# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "The Neural Crest: Cells That Leave Home"
    TITLE = "One Border, Many Destinations"

    def construct(self):
        brand = T("BIOCHEMISTRYPEDIA", size=20, color=TEAL, weight=BOLD).set_opacity(0.9)
        lesson = T(self.LESSON.upper(), size=22, color=GREY)
        title = T(self.TITLE, size=54, font=TITLE_FONT)
        fit(title, max_w=11.5)
        rule = Line(LEFT * 1.2, RIGHT * 1.2, color=GOLD, stroke_width=4)
        g = VGroup(brand, lesson, title, rule).arrange(DOWN, buff=0.32)
        # the whole title is up after 0.4 s and stays for about two seconds
        self.play(FadeIn(g, shift=UP * 0.1), run_time=0.4)
        self.wait(2.2)
        self.play(FadeOut(g), run_time=0.3)
        self.finish()


class S01Q(SpokenScene):
    def construct(self):
        g = FaceGut()
        face_lab, ear_line, fore_lab, fore_line, gut_lab = g.labels()
        self.play(FadeIn(g.face), run_time=0.35)
        self.at("loss", lead=0.1)
        self.play(Indicate(g.ears, color=GOLD, scale_factor=1.25), FadeIn(face_lab), Create(ear_line), run_time=0.6)
        self.at("white", lead=0.1)
        self.play(FadeIn(g.forelock, scale=1.3), FadeIn(fore_lab), Create(fore_line), run_time=0.6)
        self.at("stretch", lead=0.1)
        self.play(FadeIn(g.tube), FadeIn(g.dots), run_time=0.6)
        self.at("nerve cells", lead=0.2)
        self.play(FadeIn(g.distal), FadeIn(gut_lab), run_time=0.6)
        self.at("why", lead=0.1)
        self.play(LaggedStart(*[FadeIn(q, scale=0.5) for q in g.qs], lag_ratio=0.45, run_time=1.4))
        self.finish()


class S02Patient(SpokenScene):
    def construct(self):
        g = FaceGut()
        face_lab, ear_line, fore_lab, fore_line, gut_lab = g.labels()
        self.add(g.face, g.forelock, g.tube, g.dots, g.distal, face_lab, ear_line, fore_lab, fore_line, gut_lab, *g.qs)
        hs = VGroup(T("Hirschsprung disease", 28, TEXT), T("(gut)", 26, GREY)).arrange(DOWN, buff=0.12).move_to(P3(3.9, -2.2))
        wa = VGroup(T("Waardenburg syndrome", 28, TEXT), T("(pigment, hearing)", 26, GREY)).arrange(DOWN, buff=0.12).move_to(P3(-3.2, -3.05))
        gene = chip("one mutant gene", GOLD, size=28).move_to(P3(1.3, 3.3))
        gl = gene[0].get_left()
        l1 = Line(gl + DOWN * 0.1, P3(-1.9, 2.5), color=GOLD, stroke_width=3.5)
        l2 = Line(gene.get_bottom() + RIGHT * 0.5, P3(3.0, 1.8), color=GOLD, stroke_width=3.5)
        l3 = CubicBezier(gl + UP * 0.1, P3(-2.0, 3.75), P3(-6.4, 3.3), P3(-5.9, 0.6)).set_stroke(GOLD, 3.5)
        l3 = VMobject(color=GOLD, stroke_width=3.5).set_points(l3.get_points())
        self.at("disease", lead=0.6)
        self.play(FadeOut(gut_lab), FadeOut(g.qs[2]), FadeIn(hs), run_time=0.6)
        self.at("syndrome", lead=0.9)
        # the old finding labels go first, then the syndrome label arrives
        self.play(*[FadeOut(m) for m in (face_lab, ear_line, fore_lab, fore_line, g.qs[0], g.qs[1])], run_time=0.35)
        self.play(FadeIn(wa), run_time=0.45)
        self.at("one mutant", lead=0.3)
        self.play(FadeIn(gene, scale=0.8), Create(l1), Create(l2), Create(l3), run_time=0.9)
        self.at("hold that", lead=0.2)
        self.play(Indicate(gene, color=GOLD, scale_factor=1.12), run_time=0.9)
        self.finish()


class S03Border(SpokenScene):
    def construct(self):
        sh = Sheet(0.0)
        paint_stage(sh, "grey")
        L = sheet_labels(sh)
        self.play(FadeIn(VGroup(*sh.cells)), run_time=0.5)
        self.at("ectoderm", lead=0.3)
        self.play(Create(L["ecto_br"]), FadeIn(L["ecto"]), run_time=0.5)
        self.at("splits", lead=0.2)
        self.play(*sh.recolor(PLATE_IDX, "plate"), *sh.recolor(SKIN_IDX, "skin"), run_time=0.6)
        self.at("neural plate", lead=0.15)
        self.play(FadeIn(L["plate"], shift=DOWN * 0.1), run_time=0.5)
        self.at("future skin", lead=0.15)
        self.play(FadeIn(L["skinL"], shift=DOWN * 0.1), FadeIn(L["skinR"], shift=DOWN * 0.1), run_time=0.5)
        self.at("neural crest", lead=0.1)
        self.play(*sh.recolor(CREST_IDX, "crest"), FadeIn(L["crL"]), FadeIn(L["crR"]), run_time=0.8)
        self.at("border between", lead=0.1)
        self.play(*[Indicate(sh.cells[i], color=YELLOW, scale_factor=1.06) for i in CREST_IDX], run_time=1.0)
        self.finish()


Z4, CY4 = 1.5, -2.75


class S04Tube(SpokenScene):
    def construct(self):
        sh = Sheet(0.0)
        L = sheet_labels(sh)
        self.add(*sh.cells, *L.values())
        tube_lab = T("neural tube", 28, SLATE).move_to(P3(2.3 + 1.25, CY4 + 1.95))
        # where the crest labels will sit once the tube has closed
        fin = Sheet(1.0, Z4, 0.0, CY4)
        crest_labs = []
        for i in (4, 13):
            s = -SL / 2 + (i - 3 + 0.5) * CW
            p, n = fin.arc(s)
            c = fin.centroid(i)
            sgn = -1 if i == 4 else 1
            t = lab("neural crest", p[0] + sgn * 3.4, c[1] + 0.35, 28, YELLOW)
            end = p + (-n) * 0.1
            start = t.get_right() + RIGHT * 0.08 if sgn < 0 else t.get_left() + LEFT * 0.08
            crest_labs.append(VGroup(t, Line(start, end, color=YELLOW, stroke_width=2.5)))
        self.at("plate", lead=0.15)
        fold = sh.anim(0.0, 1.0, 1.0, Z4, Y0, CY4)
        self.play(fold, FadeOut(VGroup(*L.values()), run_time=0.7),
                  Succession(Wait(1.1), FadeIn(tube_lab, run_time=0.4)), run_time=2.3)
        self.at("border cells", lead=0.2)
        self.play(*[Indicate(sh.cells[i], color=YELLOW, scale_factor=1.12) for i in CREST_IDX],
                  *[FadeIn(g) for g in crest_labs], run_time=1.0)
        self.at("along its top", lead=0.1)
        top = CY4 + Z4 * 2 / fin.k + 0.9 * Z4 * 0.7
        dl = lab("dorsal midline: the top of the tube", 0, 3.45, 28, YELLOW)
        a = arrow(P3(0, 3.1), P3(0, top + 0.1), YELLOW, 3.5)
        self.play(FadeIn(dl), GrowArrow(a), run_time=0.7)
        self.finish()


class S05Leave(SpokenScene):
    def construct(self):
        Z, cy = Z4, CY4
        sh = Sheet(1.0, Z, 0.0, cy)
        ytop = cy + Z * 2 / sh.k
        NS = 56
        ss = np.linspace(-SL / 2, SL / 2, NS + 1)
        segs = [VMobject(color=GREY, stroke_width=6).set_points_as_corners([sh.arc(s)[0] for s in np.linspace(ss[j], ss[j + 1], 4)])
                for j in range(NS)]
        mem = VGroup(*segs)
        chick = lab("chick trunk", -4.9, 3.4, 30, GREY)
        self.add(*sh.cells, mem, chick)
        # inset: two neighbours joined by contacts
        fr = RoundedRectangle(corner_radius=0.2, width=4.0, height=3.0, stroke_color=GREY, stroke_width=2.5,
                              fill_color=BG, fill_opacity=1).move_to(P3(4.8, -2.0))
        cA = RoundedRectangle(corner_radius=0.18, width=1.2, height=1.5, stroke_color=YELLOW, stroke_width=3,
                              fill_color=YELLOW, fill_opacity=0.8).move_to(P3(4.0, -1.8))
        cB = cA.copy().move_to(P3(5.6, -1.8))
        ys = (-0.4, 0.0, 0.4)
        hL = [Line(P3(4.6, -1.8 + dy), P3(4.8, -1.8 + dy), color=TEXT, stroke_width=7) for dy in ys]
        hR = [Line(P3(4.8, -1.8 + dy), P3(5.0, -1.8 + dy), color=TEXT, stroke_width=7) for dy in ys]
        jl = lab("contacts", 4.8, -3.05, 26, TEXT)
        inset = VGroup(fr, cA, cB, *hL, *hR, jl)
        self.at("they", lead=0.4)
        self.play(FadeIn(inset), run_time=0.3)
        self.at("let go", lead=0.0)
        circs = []
        anims = [cA.animate.shift(LEFT * 0.35), cB.animate.shift(RIGHT * 0.35)]
        anims += [h.animate.shift(LEFT * 0.35).set_stroke(opacity=0) for h in hL]
        anims += [h.animate.shift(RIGHT * 0.35).set_stroke(opacity=0) for h in hR]
        for i in CREST_IDX:
            c = crest_cell(0.34).move_to(sh.centroid(i))
            circs.append(c)
            anims.append(ReplacementTransform(sh.cells[i], c))
        self.play(*anims, run_time=0.9)
        # exits: out of the tube and under the skin, never over it
        exits, exs = [], []
        for i in CREST_IDX:
            s = -SL / 2 + (i - 3 + 0.5) * CW
            p, n = sh.arc(s)
            exits.append(p + (-n) * 0.33)
            exs.append(s)
        gaps = VGroup(*[segs[j] for j in range(NS) if any(abs(0.5 * (ss[j] + ss[j + 1]) - s) < 0.3 for s in exs)])
        self.wait(0.5)
        self.play(FadeOut(inset), run_time=0.3)
        self.at("break", lead=0.0)
        ml = T("basement\nmembrane", 28, GREY, line_spacing=0.8).move_to(P3(-5.4, -0.9))
        ma = arrow(P3(-4.4, -0.9), P3(-2.2, -0.9), GREY, 3.5)
        ecto = [sh.cells[i] for i in SKIN_IDX]
        moves = [circs[k].animate.move_to(exits[k]) for k in (0, 3, 1, 2)]
        self.play(FadeOut(gaps, run_time=0.5),
                  *[e.animate.shift(UP * 0.6) for e in ecto],
                  Succession(Wait(0.3), LaggedStart(*moves, lag_ratio=0.25, run_time=1.0)),
                  Succession(Wait(0.35), AnimationGroup(FadeIn(ml), GrowArrow(ma), run_time=0.5)),
                  run_time=1.4)
        paths = []
        targets = {0: -2.9, 1: -4.3, 2: 4.3, 3: 2.9}
        for k in range(4):
            sx = -1 if k < 2 else 1
            st = exits[k]
            ly = ytop - 0.15
            paths.append(VMobject().set_points_smoothly([st, P3(st[0] + sx * 0.5, ly), P3(sx * 2.0, ly), P3(targets[k], ly)]))
        self.at("crawl", lead=0.3)
        self.play(LaggedStart(*[MoveAlongPath(circs[k], paths[k]) for k in (0, 3, 1, 2)], lag_ratio=0.2, run_time=1.1))
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.3)
        # mouse head: folds still open
        mh = Sheet(0.55, 1.45, 0.0, -2.6)
        self.add(*mh.cells)
        mlab = lab("mouse head: many leave before closure", 0, 3.45, 30, GREY)
        self.at("mouse head", lead=0.3)
        self.play(FadeIn(mlab), *[FadeIn(c) for c in mh.cells], run_time=0.4)
        tipL, tipR = mh.arc(-SL / 2)[0], mh.arc(SL / 2)[0]
        skin_y = tipL[1]
        self.at("many", lead=0.3)
        mc = [crest_cell(0.34).move_to(mh.centroid(i)) for i in CREST_IDX]
        self.play(*[ReplacementTransform(mh.cells[i], c) for i, c in zip(CREST_IDX, mc)], run_time=0.3)
        dest = [P3(-4.7, skin_y - 0.65), P3(-3.3, skin_y - 0.65), P3(3.3, skin_y - 0.65), P3(4.7, skin_y - 0.65)]
        self.play(LaggedStart(*[c.animate.move_to(d) for c, d in zip(mc, dest)], lag_ratio=0.2, run_time=0.8))
        self.at("folds", lead=0.1)
        gap = DoubleArrow(P3(tipL[0] + 0.3, skin_y + 0.8), P3(tipR[0] - 0.3, skin_y + 0.8), color=GREY, buff=0, stroke_width=3.5)
        note = lab("folds still open", 0, skin_y + 1.4, 28, GREY)
        self.play(FadeIn(note), GrowFromCenter(gap), run_time=0.6)
        self.finish()


class S06Emt(SpokenScene):
    def construct(self):
        emt = T("epithelial-to-mesenchymal transition", 38, GOLD)
        tag = T("(EMT)", 38, GOLD)
        title = VGroup(emt, tag).arrange(DOWN, buff=0.1).move_to(P3(0, 3.0))
        self.add(title)
        xs = [-5.1, -3.5, -1.9]
        CYc = -0.45
        cells = VGroup(*[RoundedRectangle(corner_radius=0.25, width=1.5, height=4.4, stroke_color=YELLOW if i == 1 else SLATE,
                                          stroke_width=3, fill_color=YELLOW if i == 1 else SLATE,
                                          fill_opacity=0.6 if i == 1 else 0.45).move_to(P3(xs[i], CYc)) for i in range(3)])
        nuclei = VGroup(*[Circle(0.42, stroke_width=0, fill_color=BG, fill_opacity=0.55).move_to(P3(xs[i], CYc - 1.5)) for i in range(3)])
        contacts = VGroup(*[Line(P3(xm - 0.18, y), P3(xm + 0.18, y), color=TEXT, stroke_width=6)
                            for xm in (-4.3, -2.7) for y in (0.9, 0.1, -0.7, -1.5)])
        polar = VGroup(*[Line(P3(xs[i] - 0.55, CYc + 2.0), P3(xs[i] + 0.55, CYc + 2.0), color=TEXT, stroke_width=7) for i in range(3)])
        sheet_lab = lab("cell in a sheet", -3.5, -3.1, 30, GREY)
        self.play(FadeIn(cells), FadeIn(nuclei), run_time=0.5)
        self.play(FadeIn(contacts), FadeIn(polar), run_time=0.4)
        self.at("cell in a sheet", lead=0.2)
        self.play(FadeIn(sheet_lab), Indicate(cells[1], color=YELLOW, scale_factor=1.04), run_time=0.7)
        self.at("free", lead=0.15)
        free = Circle(1.35, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.85).move_to(P3(3.6, CYc))
        fnuc = Circle(0.5, stroke_width=0, fill_color=BG, fill_opacity=0.5).move_to(P3(3.6, CYc))
        # Move the actual attached cell: contacts release before it rounds up.
        mid = cells[1]
        self.play(FadeOut(contacts), FadeOut(polar[1]),
                  mid.animate.shift(UP * 0.65), nuclei[1].animate.shift(UP * 0.65),
                  run_time=0.35)
        path = Arrow(P3(-1.0, CYc), P3(1.8, CYc), color=YELLOW, buff=0, stroke_width=5)
        self.play(ReplacementTransform(mid, free),
                  ReplacementTransform(nuclei[1], fnuc), GrowArrow(path), run_time=0.85)
        free_lab = lab("free cell", 3.6, -2.35, 30, YELLOW)
        self.play(FadeIn(free_lab), run_time=0.4)
        self.at("epithelial", lead=0.15)
        self.play(Indicate(emt, color=TEXT, scale_factor=1.04), run_time=0.8)
        self.at("transition", lead=0.4)
        self.play(Indicate(tag, color=TEXT, scale_factor=1.15), run_time=0.7)
        self.finish()


class S07Levels(SpokenScene):
    def construct(self):
        outline, bands, labels, order = make_body()
        head = lab("head", BODY_X + 1.0, 3.0, 28, GREY, )
        tail = lab("tail", BODY_X + 1.0, -3.0, 28, GREY)
        head.set_x(BODY_X + 0.8 + head.width / 2)
        tail.set_x(BODY_X + 0.8 + tail.width / 2)
        self.add(*order, outline, *labels.values(), head, tail)
        self.at("differs", lead=0.1)
        self.play(LaggedStart(*[Indicate(bands[n], color=WHITE, scale_factor=1.15) for n in ("cranial", "vagal", "cardiac", "trunk", "sacral")],
                              lag_ratio=0.25, run_time=1.4))
        self.finish()


def rp(p, c=(2.6, 0.2), s=0.88):
    return P3(c[0] + s * (p[0] - c[0]), c[1] + s * (p[1] - c[1]))


class S08Cranial(SpokenScene):
    def construct(self):
        outline, bands, labels = add_body(self, active=["cranial"])
        # A continuous profile: domed skull, brow, nose, lips, chin and jaw.
        profile = [(1.0, -1.4), (0.65, -0.2), (0.65, 1.5), (1.25, 2.7),
                   (2.5, 3.15), (3.7, 2.9), (4.35, 2.05), (4.4, 1.2),
                   (4.65, 0.65), (5.25, 0.0), (4.72, -0.2), (4.7, -0.65),
                   (4.95, -0.85), (4.65, -1.0), (4.6, -1.75), (4.0, -2.2),
                   (2.75, -2.0), (1.8, -1.2)]
        silhouette = Polygon(*[rp(p) for p in profile], stroke_color=GREY,
                             stroke_width=3, fill_color=GREY, fill_opacity=0.1).round_corners(0.16)
        vault = VMobject(stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.14)
        vault.set_points_smoothly([rp(p) for p in [(0.9, 0.5), (0.9, 1.65), (1.6, 2.65),
                                  (2.7, 2.9), (3.7, 2.45), (4.15, 1.55)]])
        vault.add_line_to(rp((0.9, 0.5)))
        jaw = Polygon(*[rp(p) for p in [(2.0, -0.65), (2.75, -1.35), (4.35, -1.15),
                      (4.35, -1.7), (3.9, -1.95), (2.8, -1.75), (1.85, -0.9)]],
                      stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.14).round_corners(0.12)
        cheek = Ellipse(width=1.05, height=0.55, stroke_color=GREY, stroke_width=3,
                        fill_color=GREY, fill_opacity=0.14).move_to(rp((3.75, -0.3)))
        eye = Circle(0.23, stroke_color=GREY, stroke_width=3, fill_color=BG, fill_opacity=1).move_to(rp((3.95, 0.65)))
        nose = Line(rp((4.5, 0.55)), rp((4.9, 0.0)), color=GREY, stroke_width=3)
        head = VGroup(silhouette, vault, jaw, cheek, eye, nose)
        st = P3(BODY_X + 0.5, 2.75)
        ends = [rp((3.75, -0.3)), rp((4.0, -1.5)), rp((2.6, -1.45)), rp((3.45, 2.1)), rp((1.7, 2.0))]
        paths = []
        for e in ends:
            paths.append(CubicBezier(st, P3(-1.6, 3.2 if e[1] > 0 else 1.0), P3(e[0] - 1.8, e[1]), e))
        lines = [stream(p, YELLOW, 3, 0.5) for p in paths]
        self.play(FadeIn(head), *[Create(l) for l in lines], run_time=0.5)
        dots = flow_group(self, paths, n=2, rt=1.1, lag=0.4, r=0.13)
        cl = chip("face and much of the skull:\ncartilage and bone", TEXT, size=28).move_to(P3(2.6, -3.15))
        self.at("cartilage", lead=0.1)
        self.play(FadeIn(cl), *[d.animate.set_opacity(0) for d in dots], run_time=0.5)
        self.at("face", lead=0.1)
        self.play(jaw.animate.set_fill(TEXT, 0.7).set_stroke(TEXT),
                  cheek.animate.set_fill(TEXT, 0.7).set_stroke(TEXT), run_time=0.6)
        self.at("much of", lead=0.0)
        self.play(vault.animate.set_fill(TEXT, 0.6).set_stroke(TEXT), run_time=0.7)
        self.finish()


class S09Vagal(SpokenScene):
    def construct(self):
        outline, bands, labels = add_body(self, active=["vagal", "sacral"])
        gut = RoundedRectangle(corner_radius=0.8, width=2.0, height=6.0, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.14).move_to(P3(1.3, 0.0))
        glab = lab("gut wall", 4.0, 2.0, 30, GREY)
        gl_line = Line(P3(2.4, 2.0), P3(3.0, 2.0), color=GREY, stroke_width=2.5)
        pv = CubicBezier(P3(BODY_X + 0.5, 1.7), P3(-1.5, 2.6), P3(-0.2, 3.7), P3(1.3, 2.75))
        ps = CubicBezier(P3(BODY_X + 0.5, -2.65), P3(-1.5, -3.5), P3(-0.2, -3.9), P3(1.3, -2.75))
        self.add(gut, glab, gl_line, stream(pv, GREEN, 4, 0.6), stream(ps, PINK, 4, 0.6))
        d1 = [Circle(0.14, stroke_width=0, fill_color=GREEN, fill_opacity=1).move_to(pv.get_start()) for _ in range(4)]
        d2 = [Circle(0.14, stroke_width=0, fill_color=PINK, fill_opacity=1).move_to(ps.get_start()) for _ in range(3)]
        self.add(*d1)
        self.play(LaggedStart(*[MoveAlongPath(d, pv) for d in d1], lag_ratio=0.2, run_time=0.8))
        self.at("sacral", lead=0.2)
        self.add(*d2)
        self.play(LaggedStart(*[MoveAlongPath(d, ps) for d in d2], lag_ratio=0.2, run_time=1.0))
        self.at("neurons", lead=0.1)
        rows = [2.4, 1.7, 1.0, 0.3, -0.4, -1.1, -1.8]

        def gang(x, y, col):
            return Ellipse(width=0.5, height=0.36, stroke_color=TEAL, stroke_width=2.5, fill_color=col, fill_opacity=0.95).move_to(P3(x, y))
        vag = [gang(1.3 + sx * 0.45, y, GREEN) for y in rows for sx in (-1, 1)]
        sac = [gang(0.85, -2.35, PINK), gang(1.75, -2.35, PINK), gang(1.3, -2.7, PINK)]
        self.play(LaggedStart(*[FadeIn(g, scale=0.4) for g in vag], lag_ratio=0.07, run_time=1.3),
                  Succession(Wait(1.0), LaggedStart(*[FadeIn(g, scale=0.4) for g in sac], lag_ratio=0.25, run_time=0.6)),
                  *[d.animate.set_opacity(0) for d in d1 + d2], run_time=1.5)
        self.at("gut wall", lead=0.1)
        tl = lab("neurons and glia", 5.0, 0.3, 30, TEXT)
        tl_line = Line(P3(2.4, 0.3), P3(3.0, 0.3), color=GREY, stroke_width=2.5)
        self.play(FadeIn(tl), FadeIn(tl_line), run_time=0.5)
        self.finish()


def ganglion(x, y, w=1.2, h=0.8, color=TEAL):
    return Ellipse(width=w, height=h, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.5).move_to(P3(x, y))


class S10Trunk(SpokenScene):
    def construct(self):
        outline, bands, labels = add_body(self, active=["trunk"])
        src = P3(BODY_X + 0.5, -0.7)
        X = 1.5
        ys = [2.8, 1.4, 0.0, -1.4, -2.8]
        # row 0: a dorsal root ganglion beside the neural tube
        tube0 = Circle(0.4, stroke_color=SLATE, stroke_width=3, fill_color=SLATE, fill_opacity=0.5).move_to(P3(X - 0.7, ys[0]))
        drg = VGroup(tube0, ganglion(X + 0.4, ys[0], 1.0, 0.7))
        # row 1: a chain of sympathetic ganglia
        chain = VGroup(Line(P3(X - 0.85, ys[1]), P3(X + 0.85, ys[1]), color=GREY, stroke_width=3),
                       *[ganglion(X + dx, ys[1], 0.5, 0.42) for dx in (-0.85, 0.0, 0.85)])
        # row 2: adrenal gland (medulla in teal) above a kidney outline
        kid = Ellipse(width=1.9, height=1.0, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.15).move_to(P3(X, ys[2] - 0.2))
        gland = Ellipse(width=1.0, height=0.55, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.4).move_to(P3(X, ys[2] + 0.4))
        med = Circle(0.15, stroke_width=0, fill_color=TEAL, fill_opacity=1).move_to(gland.get_center())
        adr = VGroup(kid, gland, med)
        # row 3: a nerve with Schwann cells wrapped round it
        nerve = Line(P3(X - 1.1, ys[3]), P3(X + 1.1, ys[3]), color=GREY, stroke_width=5)
        wraps = VGroup(*[RoundedRectangle(corner_radius=0.1, width=0.45, height=0.4, stroke_color=TEAL, stroke_width=2,
                                          fill_color=TEAL, fill_opacity=0.6).move_to(P3(X - 0.65 + 0.65 * j, ys[3])) for j in range(3)])
        nerve_g = VGroup(nerve, wraps)
        # row 4: skin line with pigment cells
        skin = Line(P3(X - 1.1, ys[4] - 0.2), P3(X + 1.1, ys[4] - 0.2), color=SKIN, stroke_width=6)
        mel = VGroup(*[Circle(0.11, stroke_width=0, fill_color=TEXT, fill_opacity=1).move_to(P3(X - 0.75 + 0.5 * j, ys[4] + 0.0)) for j in range(4)])
        skin_g = VGroup(skin, mel)
        dests = [drg, chain, adr, nerve_g, skin_g]
        names = ["sensory neurons", "sympathetic neurons", "adrenal medulla", "Schwann cells", "melanocytes"]
        labs = []
        for n, y in zip(names, ys):
            t = T(n, 26, TEXT)
            t.move_to(P3(2.95 + t.width / 2, y))
            labs.append(t)
        arrows = [arrow(src, P3(X - 1.35, y), YELLOW, 3.2) for y in ys]

        def reveal(i):
            return [GrowArrow(arrows[i]), FadeIn(dests[i], scale=0.8), FadeIn(labs[i])]
        self.at("sensory", lead=0.2)
        self.play(*reveal(0), run_time=0.8)
        self.at("sympathetic", lead=0.2)
        self.play(*reveal(1), run_time=0.8)
        self.at("adrenal medulla", lead=0.2)
        self.play(*reveal(2), run_time=0.8)
        self.at("schwann cells", lead=0.2)
        self.play(*reveal(3), run_time=0.7)
        self.at("melanocytes", lead=0.2)
        self.play(*reveal(4), run_time=0.8)
        self.at("the pigment", lead=0.2)
        pc = T("(pigment cells)", 26, TEXT).move_to(P3(2.95 + labs[4].width / 2, ys[4] - 0.5))
        pc.align_to(labs[4], LEFT)
        self.play(FadeIn(pc), run_time=0.5)
        self.finish()


class S11Idea(SpokenScene):
    def construct(self):
        c = Card(gap=1.5, top=1.8)
        c.band_label.move_to(P3(BAND_X, -3.15))
        self.add(c.frame, c.title)
        for d in c.dots:
            d.set_stroke(opacity=0.3).set_fill(d.get_color(), 0.05)
        self.add(*c.dots)
        self.play(FadeIn(c.cells), FadeIn(c.band_label), run_time=0.6)
        self.at("idea", lead=0.0)
        self.play(Indicate(c.title, color=GOLD, scale_factor=1.04), run_time=0.8)
        self.at("one border", lead=0.15)
        self.play(Indicate(c.cells, color=YELLOW, scale_factor=1.12), Indicate(c.title1, color=TEXT, scale_factor=1.06), run_time=0.9)
        self.at("many", lead=0.15)
        self.play(Indicate(c.title2, color=TEXT, scale_factor=1.05),
                  LaggedStart(*[GrowArrow(a) for a in c.arrows], lag_ratio=0.2),
                  LaggedStart(*[d.animate.set_stroke(opacity=1).set_fill(d.get_color(), 0.2) for d in c.dots], lag_ratio=0.2),
                  LaggedStart(*[FadeIn(l) for l in c.fate_labels], lag_ratio=0.2), run_time=1.5)
        self.finish()


class S12Range(SpokenScene):
    def construct(self):
        c = Card()
        card_base(self, c, 11)
        self.at("where along", lead=0.0)
        start = c.start_label()
        self.play(*swap(c.band_label, start), run_time=0.5)
        self.at("crest population", lead=0.2)
        br = Brace(c.cells, LEFT, buff=0.12, color=YELLOW)
        pl = T("population", 26, YELLOW).next_to(br, LEFT, buff=0.15)
        self.play(GrowFromCenter(br), FadeIn(pl), run_time=0.6)
        self.at("biases", lead=0.2)
        self.play(FadeIn(c.lines(0)), *c.weights(), run_time=1.0)
        self.finish()


class S13Choose(SpokenScene):
    def construct(self):
        c = Card()
        card_base(self, c, 12)
        self.at("signals", lead=0.3)
        dia = c.diamonds()
        self.play(LaggedStart(*[FadeIn(d, scale=2) for d in dia], lag_ratio=0.15, run_time=1.0))
        self.at("where it stops", lead=0.2)
        ring = c.ring()
        self.play(Create(ring), run_time=0.6)
        self.at("help decide", lead=0.2)
        self.play(FadeIn(c.lines(1)), c.dots[3].animate.set_fill(c.dots[3].get_color(), 1.0),
                  Flash(c.dots[3], color=GOLD, flash_radius=0.5), run_time=0.9)
        self.at("fates", lead=0.0)
        self.play(Indicate(c.dots[3], color=GOLD, scale_factor=1.4), run_time=0.8)
        self.finish()


class S14Scope(SpokenScene):
    def construct(self):
        c = Card()
        o = card_base(self, c, 13)
        # the route diamonds belong to scene 13: let them go first
        self.play(FadeOut(VGroup(*o["dia"])), FadeOut(o["ring"]), run_time=0.5)
        self.at("populations", lead=0.1)
        n1 = T("a population, not every cell", 34, TEXT).move_to(P3(0, ROW1))
        self.play(FadeOut(o["l1"]), FadeOut(o["l2"]), run_time=0.25)
        self.play(FadeIn(n1),
                  Indicate(c.cells, color=YELLOW, scale_factor=1.15),
                  *[c.arrows[i].animate.set_stroke(opacity=0.12) for i in (0, 1)],
                  *[c.arrows[i].animate.set_stroke(width=4, opacity=0.35) for i in FAV], run_time=0.9)
        self.at("single cells", lead=0.2)
        c0, c1 = c.cells[0], c.cells[4]
        rings = [Circle(0.4, color=GOLD, stroke_width=4).move_to(c0.get_center()),
                 Circle(0.4, color=GOLD, stroke_width=4).move_to(c1.get_center())]
        self.play(*[Create(r) for r in rings], run_time=0.6)
        self.at("already biased", lead=0.2)
        # Back off along each arrow's direction, including the sloping top route.
        def biased_arrow(cell, dot):
            start = cell.get_center() + RIGHT * 0.45
            direction = dot.get_center() - start
            end = dot.get_center() - direction / np.linalg.norm(direction) * 0.65
            return arrow(start, end, GOLD, 4.5)
        e1 = biased_arrow(c0, c.dots[2])
        e2 = biased_arrow(c1, c.dots[3])
        n2 = T("some cells are biased early", 34, GOLD).move_to(P3(0, ROW2))
        self.play(GrowArrow(e1), GrowArrow(e2), FadeIn(n2), run_time=1.0)
        self.finish()


class S15Shared(SpokenScene):
    def construct(self):
        band = VGroup(*[crest_cell(0.22).move_to(P3(-5.9, 1.9 - 0.63 * i)) for i in range(7)])
        bl = lab("crest border", -5.55, -3.3, 26, YELLOW)
        X = -3.4
        ys = [2.5, 0.0, -2.5]
        gut_ico = VGroup(RoundedRectangle(corner_radius=0.3, width=1.9, height=0.9, stroke_color=GREY, stroke_width=3,
                                          fill_color=GREY, fill_opacity=0.14),
                         *[Circle(0.11, stroke_width=0, fill_color=TEAL, fill_opacity=1).move_to(P3(-0.7 + 0.35 * j, 0.16 * (1 if j % 2 else -1))) for j in range(5)]).move_to(P3(X, ys[0]))
        skin_ico = VGroup(Rectangle(width=1.9, height=0.4, stroke_color=SKIN, stroke_width=3, fill_color=SKIN, fill_opacity=0.45),
                          *[Circle(0.12, stroke_width=0, fill_color=TEXT, fill_opacity=1).move_to(P3(-0.7 + 0.47 * j, 0.0)) for j in range(4)]).move_to(P3(X, ys[1]))
        spiral = ParametricFunction(lambda t: np.array([0.075 * t * np.cos(t), 0.075 * t * np.sin(t), 0]), t_range=[0.6, 4 * PI],
                                    color=TEXT, stroke_width=4).move_to(P3(X, ys[2]))
        icons = [gut_ico, skin_ico, spiral]
        names = [("gut neurons", TEAL), ("skin\npigment cells", TEXT), ("inner ear\npigment cells", TEXT)]
        labs = []
        for (n, col), y in zip(names, ys):
            t = T(n, 28, col, line_spacing=0.8)
            t.move_to(P3(-2.1 + t.width / 2, y))
            labs.append(t)
        gene = VGroup(RoundedRectangle(corner_radius=0.3, width=2.5, height=3.0, stroke_color=GOLD, stroke_width=4,
                                       fill_color=GOLD, fill_opacity=0.15),
                      T("same\ngene", 40, GOLD, line_spacing=0.8)).move_to(P3(5.3, 0.0))
        gleft = gene[0].get_left()[0]
        links = [Line(P3(-5.5, 1.5 - 1.25 * i), P3(X - 1.1, y), color=YELLOW, stroke_width=3.5) for i, y in enumerate(ys)]
        wires = [Line(P3(l.get_right()[0] + 0.25, y), P3(gleft, 0.9 * (y / 2.5)), color=GOLD, stroke_width=3.5) for l, y in zip(labs, ys)]
        self.at("many tissues", lead=0.0)
        self.play(FadeIn(band), FadeIn(bl),
                  LaggedStart(*[FadeIn(i, scale=0.8) for i in icons], lag_ratio=0.25),
                  LaggedStart(*[FadeIn(l) for l in labs], lag_ratio=0.25), run_time=1.0)
        self.at("share", lead=0.1)
        self.play(LaggedStart(*[Create(l) for l in links], lag_ratio=0.25), run_time=1.0)
        self.at("same genes", lead=0.2)
        self.play(FadeIn(gene, scale=0.85), LaggedStart(*[Create(w) for w in wires], lag_ratio=0.2), run_time=1.0)
        self.at("one failed gene", lead=0.2)
        xm = VGroup(Line(UL * 0.3, DR * 0.3, color=RED, stroke_width=8), Line(UR * 0.3, DL * 0.3, color=RED, stroke_width=8))
        xm.move_to(gene[0].get_top() + UP * 0.7)
        self.play(gene[0].animate.set_stroke(RED).set_fill(RED, 0.15), gene[1].animate.set_color(RED),
                  *[w.animate.set_color(RED) for w in wires], *[Create(stroke) for stroke in xm], run_time=0.6)
        self.at("unrelated", lead=0.6)
        self.play(*[Indicate(l, color=RED, scale_factor=1.12) for l in labs], run_time=1.0)
        self.finish()


def puzzle_layout():
    """Scenes 16 and 17: the puzzle again, lowered a little to leave room for the question above."""
    g = FaceGut(cy=-0.2)
    g.qs = [qmark(-5.34, -0.25), qmark(-1.35, 2.5), qmark(5.3, -0.2)]
    return g


class S16Predict(SpokenScene):
    def construct(self):
        g = puzzle_layout()
        self.add(g.face, g.forelock, g.tube, g.dots, g.distal, *g.qs)
        pred = lab("Predict", 0, 3.3, 42, GOLD)
        self.add(pred)
        self.at("gut neurons", lead=0.1)
        self.play(Indicate(g.tube, color=TEAL, scale_factor=1.03), Indicate(g.dots, color=TEAL, scale_factor=1.4), run_time=0.8)
        self.at("pigment", lead=0.1)
        self.play(Indicate(g.forelock, color=TEXT, scale_factor=1.5), run_time=0.8)
        self.at("share a start", lead=0.1)
        band = VGroup(*[crest_cell(0.19).move_to(P3(-0.45 + 0.45 * i, 1.35)) for i in range(3)])
        sl = lab("shared start", 0.0, 2.05, 26, YELLOW)
        l1 = Line(P3(-0.75, 1.4), P3(-1.8, 1.9), color=YELLOW, stroke_width=3.5)
        l2 = Line(P3(0.75, 1.3), P3(1.6, 1.0), color=YELLOW, stroke_width=3.5)
        self.play(FadeIn(band), FadeIn(sl), Create(l1), Create(l2), run_time=0.8)
        self.at("what could", lead=0.15)
        q = lab("What could one broken gene do?", 0, 3.3, 40, GOLD)
        self.play(*swap(pred, q), run_time=0.5)
        self.at("broken gene", lead=0.3)
        gene = chip("one broken gene", RED, size=28).move_to(P3(3.8, -2.7))
        self.play(FadeIn(gene, scale=0.8), run_time=0.6)
        self.finish()


class S17Pause(NarratedScene):
    def construct(self):
        g = puzzle_layout()
        q = lab("What could one broken gene do?", 0, 3.3, 40, GOLD)
        self.add(g.face, g.forelock, g.tube, g.dots, g.distal, *g.qs, q)
        for n in "54321":
            d = lab(n, 0.0, -2.9, 56, GREY)
            self.play(FadeIn(d, run_time=0.2))
            self.wait(0.6)
            self.play(FadeOut(d, run_time=0.2))
        self.finish()


class S18Reveal(SpokenScene):
    def construct(self):
        band = VGroup(*[crest_cell(0.22).move_to(P3(-5.8, 1.5 - 0.6 * i)) for i in range(6)])
        bl = lab("shared start", -5.8, -2.0, 26, YELLOW)
        enteric = chip("enteric precursors", TEAL, size=34, fill_opacity=0.3).move_to(P3(-0.3, 1.9))
        mtxt = T("melanocytes\n(pigment, hearing)", 34, TEXT, line_spacing=0.8)
        mbox = RoundedRectangle(corner_radius=0.14, width=mtxt.width + 0.5, height=mtxt.height + 0.5, stroke_color=TEXT,
                                stroke_width=2.5, fill_color=TEXT, fill_opacity=0.3)
        mel = VGroup(mbox, mtxt.move_to(mbox)).move_to(P3(-0.3, -1.7))
        a1 = arrow(P3(-5.2, 0.4), enteric.get_left() + LEFT * 0.1, YELLOW, 3.5)
        a2 = arrow(P3(-5.2, -0.1), mel.get_left() + LEFT * 0.1, YELLOW, 3.5)
        gene = chip("one gene", GOLD, size=34, fill_opacity=0.25).move_to(P3(5.0, 0.1))
        w1 = Line(gene.get_left() + UP * 0.1, enteric.get_right() + RIGHT * 0.05, color=GOLD, stroke_width=4)
        w2 = Line(gene.get_left() + DOWN * 0.1, mel.get_right() + RIGHT * 0.05, color=GOLD, stroke_width=4)
        self.add(band, bl, enteric, mel, a1, a2)
        self.at("it could", lead=0.0)
        self.play(FadeIn(gene, scale=0.8), Create(w1), Create(w2), run_time=0.45)
        self.at("fail", lead=0.1)
        xm = VGroup(Line(UL * 0.35, DR * 0.35, color=RED, stroke_width=9), Line(UR * 0.35, DL * 0.35, color=RED, stroke_width=9))
        xm.move_to(gene.get_top() + UP * 0.6)
        self.play(gene.animate.set_color(RED), w1.animate.set_color(RED), w2.animate.set_color(RED), *[Create(stroke) for stroke in xm], run_time=0.4)
        self.at("both lineages", lead=0.1)
        # Both boxes take the same failed style in the same animation.
        self.play(*[m.animate.set_color(GREY).set_opacity(0.38) for m in (enteric, mel, a1, a2)], run_time=0.5)
        self.at("both need", lead=0.1)
        self.play(Indicate(w1, color=GOLD, scale_factor=1.0), Indicate(w2, color=GOLD, scale_factor=1.0), run_time=0.9)
        self.at("chapter", lead=0.3)
        ch = lab("Chapter 3 names the genes", 0.0, 3.3, 36, GOLD)
        self.play(FadeIn(ch), run_time=0.2)
        self.finish()


class S19Take(SpokenScene):
    def construct(self):
        c = Card(gap=1.45, top=1.55)
        self.add(c.frame, c.cells, c.band_label)
        for a, d, l in zip(c.arrows, c.dots, c.fate_labels):
            self.add(a, d, l)
        tk = lab("The takeaway", 0, 3.15, 44, GOLD, font=TITLE_FONT)
        self.add(tk)
        t1 = T("The start biases the options,", 38, GOLD, font=TITLE_FONT).move_to(P3(0, 3.3))
        t2 = T("and the journey helps choose.", 38, GOLD, font=TITLE_FONT).move_to(P3(0, 2.65))
        self.at("the start", lead=0.1)
        self.play(FadeOut(tk), run_time=0.2)
        self.play(FadeIn(t1), *c.weights(), run_time=0.8)
        self.at("and the journey", lead=0.1)
        dia = c.diamonds()
        ring = c.ring()
        self.play(FadeIn(t2), *[FadeIn(d, scale=2) for d in dia], Create(ring), c.dots[3].animate.set_fill(TEXT, 1.0), run_time=1.0)
        self.finish()


class S20End(EndCard):
    LINE = "The start biases the options, and the journey helps choose."
