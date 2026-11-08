"""Enough, Needed, and Kept (Developmental Neuroscience explainer, motor-neuron-code, chapter 2)

COLOR MAP (one colour per concept, same as chapter 1 and the old single film)
  BLUE   = Lhx3 (and Lhx4)
  YELLOW = Isl1
  PURPLE = NLI (the cofactor)
  PINK   = Mnx1 (and its relative MNR2)
  ORANGE = V2 interneuron and its genes (Chx10)
  GREEN  = motor neuron and its genes
  SEA    = a motor neuron of a different kind (mutant subclass), always ringed in GREEN
  GOLD   = Olig1 / Olig2, the progenitor factors
  MINT   = the electroporated side of the chick cord (marker colour only)
  RED    = absent / deleted / crossed out / fails
  GREY   = cells, tissue, structure, labels
  TEXT   = the lock, the question marks, neutral cards
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58AB5"
MINT = "#8FE3C0"
SEA = "#2E8B57"
LG = "#B4BBC8"             # light grey for secondary text (readable on the dark ground)

CW, CH = 4.8, 6.6          # spinal cord section, at scale 1
CR = 0.33                  # cell radius, at scale 1
# cell positions in cord-local coordinates (cord centre = 0,0)
MN_R = [(0.7, -0.75), (1.4, -0.75), (0.7, -1.45), (1.4, -1.45), (0.7, -2.15), (1.4, -2.15)]
MN_L = [(-x, y) for x, y in MN_R]
V2_R = [(0.7, 1.0), (1.4, 1.0), (0.7, 0.3), (1.4, 0.3)]
# the same twelve cells after the Mnx1 deletion: columns blurred
SC_R = [(0.45, -0.7), (1.55, -0.8), (1.0, -1.3), (1.6, -1.6), (0.5, -1.85), (1.15, -2.2)]
SC_L = [(-0.55, -0.85), (-1.45, -0.75), (-1.7, -1.5), (-0.9, -1.4), (-1.1, -2.15), (-0.35, -2.0)]

BIGC = np.array([-3.0, -0.15, 0.0])   # the big cord used in the chick and mouse scenes
KB = 0.97                             # about 6.4 units tall: 80% of the frame
COLX = 3.0                            # x centre of the label column to the right of the big cord


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.05, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def cross(center, w=1.0, h=0.7, color=RED, sw=7):
    c = np.array(center, float)
    return VGroup(Line(c + [-w / 2, h / 2, 0], c + [w / 2, -h / 2, 0], color=color, stroke_width=sw),
                  Line(c + [-w / 2, -h / 2, 0], c + [w / 2, h / 2, 0], color=color, stroke_width=sw))


def check(center, s=1.0, color=GREEN, sw=9):
    c = np.array(center, float)
    return VMobject(color=color, stroke_width=sw).set_points_as_corners(
        [c + [-0.55 * s, 0.0, 0], c + [-0.15 * s, -0.45 * s, 0], c + [0.6 * s, 0.5 * s, 0]])


def left_at(m, x, y):
    m.move_to([x, y, 0])
    m.shift(RIGHT * (x - m.get_left()[0]))
    return m


def leader(a, b, color=GREY, w=2.5):
    return Line(np.array(a, float), np.array(b, float), color=color, stroke_width=w).set_opacity(0.85)


def cord_parts(c, k=1.0, fill=0.0):
    """Spinal cord section: outline, midline, central canal, and the right half (electroporated tint)."""
    c = np.array([c[0], c[1], 0.0])
    outline = Ellipse(width=CW * k, height=CH * k, stroke_color=GREY, stroke_width=3,
                      fill_color=GREY, fill_opacity=0.07).move_to(c)
    mid = Line(c + [0, CH * k / 2 - 0.2 * k, 0], c + [0, -CH * k / 2 + 0.2 * k, 0], color=GREY, stroke_width=2).set_opacity(0.4)
    canal = Ellipse(width=0.32 * k, height=0.55 * k, stroke_color=GREY, stroke_width=2,
                    fill_color=BG, fill_opacity=1).move_to(c + [0, 0.6 * k, 0])
    e2 = Ellipse(width=CW * k, height=CH * k).move_to(c)
    r2 = Rectangle(width=CW * k / 2 + 0.3, height=CH * k + 0.6).move_to(c + [(CW * k / 2 + 0.3) / 2, 0, 0])
    half = Intersection(e2, r2, stroke_width=0, fill_color=MINT, fill_opacity=fill)
    return VGroup(outline, mid, canal, half)


def P(c, k, lp):
    return np.array([c[0] + k * lp[0], c[1] + k * lp[1], 0.0])


def cell(p, r, color, fo=0.45, sw=3):
    return Circle(radius=r, stroke_color=color, stroke_width=sw, fill_color=color, fill_opacity=fo).move_to(p)


def dashed_cell(p, r):
    d = DashedVMobject(Circle(radius=r).move_to(p), num_dashes=14)
    return d.set_stroke(GREY, 3, opacity=0.9)


def rc(k):
    """cell radius at cord scale k (a little larger than the cord scale on small cords)"""
    return CR * k * (1.0 if k > 0.9 else 1.12)


def cells_at(c, k, locs, color, fo=0.45):
    return VGroup(*[cell(P(c, k, lp), rc(k), color, fo) for lp in locs])


def mutant_cells(c, k, locs):
    """The same cells as a different kind of motor neuron: rounded squares, green ring, darker fill."""
    out = []
    for lp in locs:
        r = rc(k) * 0.92
        sq = RoundedRectangle(corner_radius=0.35 * r, width=2 * r, height=2 * r, stroke_color=GREEN, stroke_width=3,
                              fill_color=SEA, fill_opacity=0.85).move_to(P(c, k, lp))
        out.append(sq)
    return VGroup(*out)


def neuron(pos, radius=0.7, color=GREEN):
    body = Circle(radius=radius, color=color, stroke_width=4, fill_color=color, fill_opacity=0.18).move_to(pos)
    branches = VGroup(*[Line(body.get_center() + radius * np.array([np.cos(a), np.sin(a), 0]),
                              body.get_center() + radius * 1.5 * np.array([np.cos(a), np.sin(a), 0]),
                              color=color, stroke_width=4) for a in (2.3, 3.1, 3.9)])
    return VGroup(body, branches)


def tbar(a, b, color=PINK, w=6, bar=0.45):
    """A repression symbol: a line from a to b ending in a bar."""
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    n = np.array([-d[1], d[0], 0.0])
    return VGroup(Line(a, b, color=color, stroke_width=w),
                  Line(b + n * bar / 2, b - n * bar / 2, color=color, stroke_width=w + 2))


def padlock(c, closed=False, color=TEXT, s=1.0):
    c = np.array(c, float)
    body = RoundedRectangle(corner_radius=0.14, width=1.3, height=1.0, stroke_color=color, stroke_width=5,
                            fill_color=color, fill_opacity=0.22).move_to(c)
    hole = Circle(radius=0.1, stroke_width=0, fill_color=color, fill_opacity=0.9).move_to(c + [0, 0.05, 0])
    top = c + [0, 0.5, 0]
    lift = 0.0 if closed else 0.3
    left = Line(top + [-0.38, lift, 0], top + [-0.38, lift + 0.3, 0], color=color, stroke_width=8)
    right = Line(top + [0.38, lift, 0], top + [0.38, lift + 0.3, 0], color=color, stroke_width=8)
    arc = Arc(radius=0.38, start_angle=0, angle=PI, color=color, stroke_width=8).move_to(top + [0, lift + 0.3, 0])
    shackle = VGroup(left, arc, right)
    g = VGroup(shackle, body, hole)
    if s != 1.0:
        g.scale(s, about_point=c)
    return g


def band(y, h=1.8, w=13.2):
    return RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_color=GREY, stroke_width=2,
                            fill_color=GREY, fill_opacity=0.05).move_to([0, y, 0]).set_stroke(opacity=0.6)


def del_chip(name, color, size=34):
    """A chip for a deleted gene: the name stays readable; a red cross badge sits on its corner."""
    ch = chip(name, color, size)
    out = DashedVMobject(RoundedRectangle(corner_radius=0.14, width=ch.width + 0.16, height=ch.height + 0.16)
                         .move_to(ch.get_center()), num_dashes=30).set_stroke(RED, 3)
    r = 0.24
    badge = VGroup(Circle(radius=r, stroke_width=0, fill_color=RED, fill_opacity=1),
                   cross([0, 0, 0], w=0.26, h=0.26, color=TEXT, sw=4)).move_to(ch.get_corner(UR) + [0.05, 0.05, 0])
    return VGroup(ch, out, badge)


def pad(m, k=0.1):
    return m


class Film(SpokenScene):
    """SpokenScene whose clock ignores any earlier scene it replayed to get its starting frame."""
    _t0 = 0.0

    def elapsed(self):
        return self.renderer.time - self._t0


def prior(scene, cls):
    """Rebuild the last frame of an earlier scene (animations skipped, cues ignored) and return its
    named objects, so a scene starts exactly where the last one ended."""
    outer = not getattr(scene, "_replaying", False)
    if outer:
        scene._replaying = True
        scene.next_section(skip_animations=True)
        scene.at = lambda *a, **k: None
    cls.construct(scene)
    if outer:
        del scene.at
        scene._replaying = False
        scene.next_section()
        scene._t0 = scene.renderer.time
    return dict(scene.st)


def hold(scene, cls):
    """A pause or beat: the last frame of `cls`, held still."""
    prior(scene, cls)
    scene.wait(scene.narration_s + 0.4)


def countdown(scene, cls, label, pos, w=4.6):
    """The last frame of `cls`, held, with a 'pause' cue: a bar that drains over the silent seconds."""
    prior(scene, cls)
    pos = np.array(pos, float)
    lab = T(label, 30, GOLD, weight=BOLD).move_to(pos + [0, 0.45, 0])
    bar = Rectangle(width=w, height=0.2, stroke_width=0, fill_color=GOLD, fill_opacity=0.9).move_to(pos)
    track = Rectangle(width=w, height=0.2, stroke_color=GOLD, stroke_width=2, fill_opacity=0).move_to(pos)
    small = Rectangle(width=0.02, height=0.2, stroke_width=0, fill_color=GOLD, fill_opacity=0.9).move_to(pos + [-w / 2 + 0.01, 0, 0])
    scene.play(FadeIn(lab), FadeIn(track), FadeIn(bar), run_time=0.3)
    scene.play(Transform(bar, small), run_time=scene.narration_s - 0.3, rate_func=linear)
    scene.wait(0.4)


def mouse_icon(c, s=1.0):
    """A clean side-view mouse: one merged body outline (body, head, snout, ear), eye, nose, whiskers, tail."""
    c = np.array(c, float)
    body = Ellipse(width=2.5, height=1.45).move_to(c)
    head = Ellipse(width=1.35, height=1.05).move_to(c + [-1.35, 0.0, 0])
    snout = Ellipse(width=0.75, height=0.55).move_to(c + [-1.95, -0.1, 0])
    ear = Circle(radius=0.34).move_to(c + [-1.05, 0.62, 0])
    shape = Union(body, head, snout, ear, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.32)
    eye = Circle(radius=0.07, stroke_width=0, fill_color=TEXT, fill_opacity=1).move_to(c + [-1.6, 0.17, 0])
    nose = Circle(radius=0.07, stroke_width=0, fill_color=PINK, fill_opacity=1).move_to(c + [-2.3, -0.08, 0])
    wh = VGroup(*[Line(c + [-2.15, -0.05, 0], c + [-2.8, dy, 0], color=GREY, stroke_width=2) for dy in (0.15, -0.1, -0.3)])
    tail = ArcBetweenPoints(c + [1.2, 0.05, 0], c + [2.4, 0.8, 0], angle=-PI / 2.2, color=GREY, stroke_width=5)
    g = VGroup(tail, shape, eye, nose, wh)
    return g.scale(s, about_point=c)


def wp(lp):
    return P(BIGC, KB, lp)


def big_cells(locs, color, fo=0.45):
    return VGroup(*[cell(wp(lp), CR, color, fo) for lp in locs])


# ---------------------------------------------------------------------------------------------
# 00 title, 01 the question
# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Transcription Factor Codes: Building a Motor Neuron"
    TITLE = "Enough, Needed, and Kept"

    def construct(self):
        brand = T("BIOCHEMISTRYPEDIA", size=22, color=TEAL, weight=BOLD).set_opacity(0.9)
        lesson = T(self.LESSON.upper(), size=24, color=LG)
        title = T(self.TITLE, size=64, font=TITLE_FONT)
        rule = Line(LEFT * 1.6, RIGHT * 1.6, color=GOLD, stroke_width=4)
        g = VGroup(brand, lesson, title, rule).arrange(DOWN, buff=0.4).move_to(ORIGIN)
        self.add(brand, lesson)
        self.play(FadeIn(title, shift=UP * 0.1), GrowFromCenter(rule), run_time=0.45)
        self.finish()


class S01Q(Film):
    def construct(self):
        enough = T("enough?", 68, TEXT, font=TITLE_FONT).move_to([-4.2, 1.7, 0])
        needed = T("needed?", 68, TEXT, font=TITLE_FONT).move_to([-4.2, -1.7, 0])
        prot = chip("a protein", TEXT, 40).move_to([0.2, 1.7, 0])
        a = arr([1.7, 1.7, 0], [2.9, 1.7, 0], TEXT)
        mn = neuron([4.6, 1.7, 0], 1.0)
        row = VGroup(*[neuron([x, -1.7, 0], 0.8) for x in (0.4, 2.9, 5.4)])
        qs = VGroup(*[T("?", 60, TEXT, weight=BOLD).move_to([x, -0.35, 0]) for x in (0.4, 2.9, 5.4)])
        self.play(FadeIn(prot, shift=RIGHT * 0.2), run_time=0.3)
        self.at("enough")
        self.play(FadeIn(enough, scale=0.9), run_time=0.3)
        self.at("start making")
        self.play(GrowArrow(a), run_time=0.4)
        self.at("motor neuron")
        self.play(FadeIn(mn, scale=0.7), run_time=0.4)
        self.at("does every")
        self.play(FadeIn(needed, scale=0.9), LaggedStart(*[FadeIn(n, scale=0.7) for n in row], lag_ratio=0.25), run_time=0.9)
        self.at("need it")
        self.play(LaggedStart(*[FadeIn(q, shift=DOWN * 0.15) for q in qs], lag_ratio=0.2), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
# 02, 03 the two definitions (same cell, same frame)
# ---------------------------------------------------------------------------------------------
DC = np.array([2.9, -0.1, 0.0])      # the tested cell
FAC_START = np.array([-4.7, -2.2, 0.0])


def def_cell():
    return Circle(radius=1.7, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.12).move_to(DC)


def def_box():
    box = Rectangle(width=5.3, height=4.5).move_to(DC)
    return DashedVMobject(box, num_dashes=52).set_stroke(GREY, 3, opacity=0.85)


def title_at(txt):
    return left_at(T(txt, 66, TEXT, font=TITLE_FONT), -6.6, 2.7)


def def_at(txt):
    return left_at(T(txt, 36, TEXT, line_spacing=0.9), -6.6, 0.55)


class S02Suff(Film):
    def construct(self):
        cellc = def_cell()
        fac = chip("factor", TEXT, 38).move_to(FAC_START)
        title = title_at("sufficient")
        eff = T("effect", 48, GREEN, weight=BOLD).move_to(DC + [0, -0.6, 0])
        box = def_box()
        boxlab = T("the cells tested", 30, LG).move_to(DC + [0, -2.7, 0])
        defn = def_at("adding it\nproduces the effect,\nin the cells tested")
        self.play(FadeIn(cellc), run_time=0.3)
        self.at("factor")
        self.play(FadeIn(fac, shift=RIGHT * 0.2), run_time=0.4)
        self.at("sufficient")
        self.play(FadeIn(title, shift=DOWN * 0.1), run_time=0.4)
        self.at("adding it")
        a = arr(FAC_START + [1.1, 0.2, 0], DC + [-1.8, -0.75, 0], TEXT, w=7)
        add = T("add", 30, GOLD, weight=BOLD).move_to([-1.3, -1.0, 0])
        self.play(GrowArrow(a), FadeIn(add), FadeIn(defn, shift=UP * 0.1), run_time=0.3)
        self.play(fac.animate.move_to(DC + [0, 0.6, 0]), run_time=0.3)
        self.at("produces the effect")
        self.play(FadeOut(a), FadeOut(add), cellc.animate.set_stroke(GREEN).set_fill(GREEN, 0.3), FadeIn(eff, scale=0.8), run_time=0.6)
        self.at("in the cells")
        self.play(Create(box), FadeIn(boxlab), run_time=0.9)
        self.st = dict(cell=cellc, fac=fac, title=title, eff=eff, box=box, boxlab=boxlab, defn=defn)
        self.finish()


class S03Nec(Film):
    def construct(self):
        st = prior(self, S02Suff)
        cellc, fac, title, eff, defn = st["cell"], st["fac"], st["title"], st["eff"], st["defn"]
        self.at("necessary")
        new_title = title_at("necessary")
        new_def = def_at("without it,\nthe effect fails,\nin the cells tested")
        self.play(FadeOut(title, run_time=0.2), FadeOut(defn, run_time=0.2))
        self.play(FadeIn(new_title, shift=DOWN * 0.1), FadeIn(new_def, shift=UP * 0.1), run_time=0.3)
        self.at("if the")
        # the factor is taken out of the cell: it slides away, a red dashed outline stays where it was
        slot = DC + [0, 0.6, 0]
        ghost = DashedVMobject(RoundedRectangle(corner_radius=0.14, width=fac.width + 0.1, height=fac.height + 0.1).move_to(slot),
                               num_dashes=26).set_stroke(RED, 3)
        out_lab = T("removed", 30, RED).move_to(FAC_START + [0, -0.75, 0])
        self.play(fac.animate.move_to(FAC_START), FadeIn(ghost), FadeIn(out_lab), run_time=0.7)
        self.at("does not")
        x = cross(eff.get_center(), w=2.6, h=0.8)
        self.play(cellc.animate.set_stroke(GREY).set_fill(GREY, 0.12), eff.animate.set_color(GREY), Create(x), run_time=0.5)
        self.at("without it")
        self.play(Indicate(ghost, color=RED), run_time=0.7)
        self.st = dict(st, title=new_title, defn=new_def, ghost=ghost, out_lab=out_lab, x=x)
        self.finish()


# ---------------------------------------------------------------------------------------------
# 04 the two tests
# ---------------------------------------------------------------------------------------------
LEFT_C = np.array([-3.5, -0.15, 0.0])
RIGHT_C = np.array([4.1, -0.15, 0.0])
K4 = 0.76


def bolt(c, s=1.0, color=TEXT):
    c = np.array(c, float)
    pts = [c + [0.2 * s, 0.65 * s, 0], c + [-0.2 * s, 0.05 * s, 0], c + [0.08 * s, 0.05 * s, 0], c + [-0.25 * s, -0.65 * s, 0]]
    return VMobject(color=color, stroke_width=8).set_points_as_corners(pts)


class S04Chick(Film):
    def construct(self):
        div = Line([0.2, 3.7, 0], [0.2, -3.7, 0], color=GREY, stroke_width=2).set_opacity(0.4)
        cord = cord_parts(LEFT_C, K4)
        h1 = T("chick", 36, TEXT, weight=BOLD).move_to([-3.5, 3.45, 0])
        ctrl = T("control", 26, LG).move_to([-5.15, 2.75, 0])
        elec = T("electroporated", 26, MINT).move_to([-1.9, 2.75, 0])
        bl = bolt([-0.85, 0.2, 0], 1.3)
        lab1 = T("electroporation\ntests sufficiency", 28, TEXT, line_spacing=0.8).move_to([-3.4, -3.35, 0])
        h2 = T("mouse", 36, TEXT, weight=BOLD).move_to([4.0, 3.45, 0])
        emb = mouse_icon([2.1, 2.1, 0], 0.6)
        gene = del_chip("gene", TEXT, 36).move_to([1.1, -0.15, 0])
        x = Dot(radius=0.001).move_to(gene.get_center())
        cord2 = cord_parts(RIGHT_C, K4)
        ga = arr([1.95, -0.15, 0], [2.6, -0.15, 0], TEXT, w=5, tip=0.18)
        lab2 = T("gene deletion\ntests necessity", 28, TEXT, line_spacing=0.8).move_to([4.1, -3.35, 0])
        self.add(div, cord, ctrl)
        self.at("electroporation")
        self.play(FadeIn(bl, scale=1.3), cord[3].animate.set_fill(MINT, 0.3), FadeIn(elec), run_time=0.7)
        self.at("chick")
        self.play(FadeIn(h1), run_time=0.4)
        self.at("tests sufficiency")
        self.play(FadeIn(lab1, shift=UP * 0.15), run_time=0.5)
        self.at("gene")
        self.play(FadeIn(gene[0]), FadeIn(cord2), run_time=0.3)
        self.at("deletion")
        self.play(FadeIn(gene[1]), FadeIn(gene[2]), FadeIn(ga), run_time=0.3)
        self.at("mouse")
        self.play(FadeIn(h2), FadeIn(emb), run_time=0.3)
        self.at("tests necessity")
        self.play(FadeIn(lab2, shift=UP * 0.15), run_time=0.5)
        self.st = dict(div=div, cord=cord, h1=h1, ctrl=ctrl, elec=elec, bl=bl, lab1=lab1, h2=h2, emb=emb,
                       gene=gene, ga=ga, lab2=lab2, cord2=cord2)
        self.finish()


# ---------------------------------------------------------------------------------------------
# 05, 06 sufficient in chick
# ---------------------------------------------------------------------------------------------
def mk_leader_cells(chip_m, color=GREEN, y=None, tip_x=-1.25):
    y0 = chip_m.get_center()[1] if y is None else y
    return leader([chip_m.get_left()[0] - 0.1, y0, 0], [tip_x, y0, 0], color)


class S05Mnx(Film):
    def construct(self):
        cord = cord_parts(BIGC, KB, fill=0.3)
        labels = VGroup(T("control", 28, LG).move_to(BIGC + [-1.35, 3.35, 0]),
                        T("electroporated", 28, MINT).move_to(BIGC + [1.45, 3.35, 0]))
        cells = big_cells(MN_R, GREY, 0.25)
        cells_c = big_cells(MN_L, GREY, 0.25)
        v2 = big_cells(V2_R, ORANGE, 0.5)
        v2lab = T("V2 cells", 28, ORANGE).move_to([-4.05, 1.35, 0])
        mnlab = T("motor\nneurons", 26, LG).move_to([-6.1, -1.55, 0])
        self.add(cord, labels, cells_c, v2, v2lab, mnlab)
        self.play(FadeIn(cells), run_time=0.3)
        self.at("mnx1")
        mnx = chip("Mnx1", PINK, 46).move_to([COLX, 2.6, 0])
        self.play(FadeIn(mnx, shift=LEFT * 0.2), run_time=0.5)
        self.at("or its")
        orr = T("or", 32, LG).move_to([COLX, 1.75, 0])
        self.play(FadeIn(orr), run_time=0.3)
        self.at("relative")
        mnr = chip("MNR2", PINK, 46).move_to([COLX, 0.9, 0])
        self.play(FadeIn(mnr, shift=LEFT * 0.2), run_time=0.5)
        self.at("enough")
        a = arr([1.0, 1.7, 0], [-1.2, -0.75, 0], PINK, w=8)
        self.play(GrowArrow(a), run_time=0.6)
        self.at("trigger")
        self.play(LaggedStart(*[c.animate.set_color(GREEN).set_fill(GREEN, 0.5) for c in cells], lag_ratio=0.15), run_time=1.0)
        self.at("differentiation")
        mk = chip("motor-neuron\nmarkers", GREEN, 40).move_to([COLX, -1.6, 0])
        ld = mk_leader_cells(mk, GREEN, y=-1.6, tip_x=-1.26)
        self.play(FadeIn(mk, shift=UP * 0.2), Create(ld), run_time=0.6)
        self.st = dict(cord=cord, labels=labels, cells=cells, cells_c=cells_c, mnx=mnx, orr=orr, mnr=mnr, a=a, mk=mk, ld=ld, v2=v2, v2lab=v2lab, mnlab=mnlab)
        self.finish()


class S06Mnx2(Film):
    def construct(self):
        st = prior(self, S05Mnx)
        self.play(FadeOut(st["orr"]), FadeOut(st["mnr"]), FadeOut(st["a"]), run_time=0.3)
        self.at("also")
        v2 = st["v2"]
        v2c = chip("V2 genes", ORANGE, 40).move_to([COLX, 0.55, 0])
        vl = leader([v2c.get_left()[0] - 0.1, 0.5, 0], [-1.22, 0.5, 0], ORANGE)
        self.play(FadeIn(v2c, shift=LEFT * 0.2), Create(vl), run_time=0.3)
        self.at("represses")
        tb = tbar([COLX, 2.6 - 0.58, 0], [COLX, 0.55 + 0.6, 0], PINK, w=7)
        self.play(Create(tb), run_time=0.4)
        self.play(v2.animate.set_opacity(0.22), st["v2lab"].animate.set_opacity(0.4),
                  v2c.animate.set_opacity(0.4), vl.animate.set_opacity(0.3), run_time=0.8)
        self.st = dict(cord=st["cord"], labels=st["labels"], cells=st["cells"], cells_c=st["cells_c"], mnx=st["mnx"],
                       mk=st["mk"], ld=st["ld"], v2=v2, v2c=v2c, vl=vl, tb=tb, v2lab=st["v2lab"], mnlab=st["mnlab"])
        self.finish()


# ---------------------------------------------------------------------------------------------
# 07 to 14 the mouse deletion and what it shows
# ---------------------------------------------------------------------------------------------
class S07Predict(Film):
    def construct(self):
        cord = cord_parts(BIGC, KB)
        mlab = T("mouse", 30, LG, weight=BOLD).move_to(BIGC + [0, 3.4, 0])
        dashed = VGroup(*[dashed_cell(wp(lp), CR) for lp in MN_R + MN_L])
        pred = T("Predict.", 56, GOLD, font=TITLE_FONT).move_to([COLX, 3.1, 0])
        self.add(cord, mlab)
        self.play(FadeIn(dashed), FadeIn(pred), run_time=0.6)
        self.at("delete")
        mnx = del_chip("Mnx1", PINK, 42).move_to([COLX, 1.8, 0])
        self.play(FadeIn(mnx), run_time=0.5)
        self.at("are motor")
        q1 = chip("made?", TEXT, 40).move_to([COLX, 0.55, 0])
        dl = T("motor neurons", 28, LG).move_to([COLX, -1.95, 0])
        dld = leader([COLX - 1.5, -1.95, 0], [-1.25, -1.5, 0], LG)
        self.play(FadeIn(q1, shift=LEFT * 0.2), FadeIn(dl), Create(dld), run_time=0.6)
        self.at("does anything")
        q2 = chip("anything wrong?", TEXT, 40).move_to([COLX, -0.75, 0])
        self.play(FadeIn(q2, shift=LEFT * 0.2), run_time=0.5)
        self.st = dict(cord=cord, mlab=mlab, dashed=dashed, pred=pred, mnx=mnx, q1=q1, q2=q2, dl=dl, dld=dld)
        self.finish()


class S08Pause(Film):
    def construct(self):
        countdown(self, S07Predict, "pause and predict", [COLX, -3.4, 0])


class S09Reveal(Film):
    def construct(self):
        st = prior(self, S07Predict)
        solid = big_cells(MN_R + MN_L, GREEN, 0.5)
        self.play(FadeOut(st["pred"]), FadeOut(st["q2"]), FadeOut(st["q1"]), FadeOut(st["dl"]), FadeOut(st["dld"]), run_time=0.3)
        self.at("made")
        made = chip("made", GREEN, 40).move_to([COLX, 0.6, 0])
        self.play(FadeOut(st["dashed"]), LaggedStart(*[GrowFromCenter(c) for c in solid], lag_ratio=0.03),
                  FadeIn(made), run_time=0.45)
        self.at("on schedule")
        s1 = chip("on schedule", GREEN, 36).move_to([COLX, -0.6, 0])
        self.play(FadeIn(s1, shift=LEFT * 0.2), run_time=0.4)
        self.at("normal numbers")
        s2 = chip("normal numbers", GREEN, 36).move_to([COLX, -1.8, 0])
        self.play(FadeIn(s2, shift=LEFT * 0.2), run_time=0.4)
        self.st = dict(cord=st["cord"], mlab=st["mlab"], solid=solid, mnx=st["mnx"], made=made, s1=s1, s2=s2)
        self.finish()


def tangle(sx, sy, seed):
    rng = np.random.RandomState(seed)
    ex, ey = rng.uniform(5.0, 6.6), rng.uniform(-3.2, -0.5)
    xs = np.linspace(sx, ex, 40)
    t = (xs - sx) / (ex - sx)
    amp, w, ph = rng.uniform(0.35, 0.8), rng.uniform(5, 9), rng.uniform(0, 6)
    ys = sy + (ey - sy) * (3 * t ** 2 - 2 * t ** 3) + amp * np.sin(w * t + ph) * np.sin(np.pi * t)
    ys = np.clip(ys, -3.35, -0.55)
    return VMobject(color=GREEN, stroke_width=5).set_points_smoothly([[x, y, 0] for x, y in zip(xs, ys)])


class S10Reveal2(Film):
    def construct(self):
        st = prior(self, S09Reveal)
        solid = st["solid"]
        self.play(FadeOut(st["made"]), FadeOut(st["s1"]), FadeOut(st["s2"]), FadeOut(st["mnx"]), run_time=0.3)
        self.at("v2 interneuron")
        flick = [0, 3, 4, 7, 9]
        on = [solid[i].animate.set_color(ORANGE).set_fill(ORANGE, 0.6) for i in flick]
        off = [solid[i].animate.set_color(GREEN).set_fill(GREEN, 0.5) for i in flick]
        self.play(*on, run_time=0.3)
        self.play(*off, run_time=0.2)
        self.play(*[solid[i].animate.set_color(ORANGE).set_fill(ORANGE, 0.6) for i in flick], run_time=0.3)
        v2c = chip("V2 feature: Chx10", ORANGE, 28).move_to(BIGC + [0.0, 1.35, 0])
        self.play(FadeIn(v2c, shift=DOWN * 0.1), run_time=0.4)
        scatter = SC_R + SC_L
        self.at("columns")
        v2l = leader(v2c.get_bottom() + [0.4, 0, 0], wp(scatter[0]) + [0.0, 0.34, 0], ORANGE)
        moves = [solid[i].animate.move_to(wp(scatter[i])) for i in range(12)]
        col_lab = T("disordered columns", 32, TEXT, weight=BOLD).move_to([2.9, 1.0, 0])
        cl = leader([0.65, 0.8, 0], wp(scatter[1]) + [0.15, 0.38, 0], LG)
        self.play(*moves, FadeIn(v2l), FadeIn(col_lab, shift=LEFT * 0.2), Create(cl), run_time=0.7)
        self.at("axon paths")
        axons = VGroup(*[tangle(wp(scatter[i])[0] + 0.3, wp(scatter[i])[1], 11 + i) for i in range(6)])
        ax_lab = T("disordered axon paths", 32, TEXT, weight=BOLD).move_to([3.3, 0.1, 0])
        self.play(Create(axons), FadeIn(ax_lab, shift=LEFT * 0.2), run_time=0.9)
        self.at("disordered")
        credit = T("Arber et al. and Thaler et al., 1999", 26, LG).move_to([3.1, -3.62, 0])
        self.play(FadeIn(credit), Indicate(ax_lab, color=TEXT, scale_factor=1.05), run_time=0.7)
        self.st = dict(cord=st["cord"], mlab=st["mlab"], solid=solid, v2c=v2c, v2l=v2l,
                       col_lab=col_lab, cl=cl, ax_lab=ax_lab, axons=axons, credit=credit)
        self.finish()


class S11Beat(Film):
    def construct(self):
        hold(self, S10Reveal2)


class S12Keep(Film):
    def construct(self):
        st = prior(self, S10Reveal2)
        mnx = chip("Mnx1", PINK, 64).move_to([-3.9, 0.0, 0])
        self.play(*[FadeOut(m) for m in st.values()], run_time=0.4)
        self.play(FadeIn(mnx), run_time=0.3)
        self.at("needed to make")
        make = T("make", 76, TEXT, font=TITLE_FONT).move_to([0.3, 1.7, 0])
        a1 = arr([-2.0, 0.6, 0], [-0.95, 1.4, 0], PINK, w=8)
        self.play(GrowArrow(a1), FadeIn(make, shift=RIGHT * 0.2), run_time=0.6)
        self.at("motor neuron")
        x = cross([2.8, 1.7, 0], w=1.3, h=1.1, sw=11)
        no = T("no", 64, RED, weight=BOLD).move_to([4.4, 1.7, 0])
        self.play(Create(x), FadeIn(no), run_time=0.5)
        self.at("needed to keep")
        keep = T("keep", 76, TEXT, font=TITLE_FONT).move_to([0.3, -1.7, 0])
        a2 = arr([-2.0, -0.6, 0], [-0.95, -1.4, 0], PINK, w=8)
        self.play(GrowArrow(a2), FadeIn(keep, shift=RIGHT * 0.2), run_time=0.6)
        self.at("keep one")
        ck = check([2.8, -1.7, 0], s=1.5, sw=13)
        yes = T("yes", 64, GREEN, weight=BOLD).move_to([4.5, -1.7, 0])
        self.play(Create(ck), FadeIn(yes), run_time=0.6)
        self.st = dict(mnx=mnx, make=make, a1=a1, x=x, no=no, keep=keep, a2=a2, ck=ck, yes=yes)
        self.finish()


NEU_C = np.array([-2.3, -0.1, 0.0])
NEU_R = 2.55


class S13Lock(Film):
    def construct(self):
        st = prior(self, S12Keep)
        body = Circle(radius=NEU_R, stroke_color=GREEN, stroke_width=5, fill_color=GREEN, fill_opacity=0.14).move_to(NEU_C)
        nl = T("motor neuron", 34, GREEN).move_to(NEU_C + [0, 3.0, 0])
        mnx = chip("Mnx1", PINK, 38).move_to(NEU_C + [0, -1.85, 0])
        gone = [st[k] for k in ("make", "a1", "x", "no", "keep", "a2", "ck", "yes")]
        self.play(*[FadeOut(m) for m in gone], run_time=0.3)
        self.play(FadeIn(body), FadeIn(nl), ReplacementTransform(st["mnx"], mnx), run_time=0.6)
        v2c = chip("V2 genes", ORANGE, 44).move_to([4.5, -1.85, 0])
        v2s = T("interneuron programme", 28, LG).move_to([4.5, -2.75, 0])
        tb = tbar([mnx.get_right()[0] + 0.1, -1.85, 0], [v2c.get_left()[0] - 0.12, -1.85, 0], PINK)
        self.at("keep suppressing")
        self.play(FadeIn(v2c, shift=LEFT * 0.2), FadeIn(v2s), run_time=0.4)
        self.play(Create(tb), v2c.animate.set_opacity(0.3), v2s.animate.set_opacity(0.5), run_time=0.9)
        self.at("that is the")
        LS = 1.6
        lc = NEU_C + [-0.75, -0.3, 0]
        lock = padlock(lc, closed=False, s=LS)
        self.play(FadeIn(lock, shift=DOWN * 0.3), run_time=0.4)
        self.play(lock[0].animate.shift(DOWN * 0.3 * LS), run_time=0.35)
        lab = T("the lock", 48, TEXT, font=TITLE_FONT).move_to([2.6, 0.8, 0])
        ll = leader([lab.get_left()[0] - 0.15, 0.7, 0], lc + [1.15, 0.1, 0], TEXT)
        self.play(FadeIn(lab, shift=RIGHT * 0.2), Create(ll), run_time=0.4)
        self.st = dict(body=body, nl=nl, mnx=mnx, v2c=v2c, v2s=v2s, tb=tb, lock=lock, lab=lab, ll=ll)
        self.finish()


class S14Beat(Film):
    def construct(self):
        hold(self, S13Lock)


# ---------------------------------------------------------------------------------------------
# 15 to 19 the genotype table
# ---------------------------------------------------------------------------------------------
R1C, R1H = 1.6, 2.95
R2C, R2H = -0.85, 1.5
R3C, R3H = -2.55, 1.4
XA, XB, XC = -5.3, -2.75, -1.15


def headers():
    return VGroup(T("deleted", 26, RED, weight=BOLD).move_to([XA, 3.5, 0]),
                  T("motor neurons made?", 26, LG, weight=BOLD).move_to([XB + 0.5, 3.5, 0]),
                  T("what else", 26, LG, weight=BOLD).move_to([3.0, 3.5, 0]))


def gchip(name, color, pos):
    return chip(name, color, 30, pad=0.14).move_to(pos)


def sc(name, color, pos=None):
    return chip(name, color, 30, pad=0.1) if pos is None else chip(name, color, 30, pad=0.1).move_to(pos)


L1, L2, L3, L4 = R1C + 1.08, R1C + 0.38, R1C - 0.32, R1C - 1.02


def dim(b):
    return b.set_stroke(opacity=0.25)


class S15Olig(Film):
    def construct(self):
        hd = headers()
        r1, r2, r3 = band(R1C, R1H), dim(band(R2C, R2H)), dim(band(R3C, R3H))
        c1 = left_at(sc("progenitors", GOLD), XC, L1)
        self.play(FadeIn(hd, shift=DOWN * 0.15), FadeIn(r1), FadeIn(r2), FadeIn(r3), run_time=0.5)
        self.at("progenitors")
        self.play(FadeIn(c1, shift=LEFT * 0.2), run_time=0.5)
        self.at("both")
        o1 = gchip("Olig1", GOLD, [XA, R1C + 0.42, 0])
        self.play(FadeIn(o1, shift=DOWN * 0.2), run_time=0.4)
        self.at("and")
        o2 = gchip("Olig2", GOLD, [XA, R1C - 0.42, 0])
        self.play(FadeIn(o2, shift=DOWN * 0.2), run_time=0.4)
        self.at("are largely")
        v1 = T("largely no", 38, RED, weight=BOLD).move_to([XB, R1C, 0])
        self.play(FadeIn(v1, scale=0.8), run_time=0.5)
        self.st = dict(hd=hd, r1=r1, r2=r2, r3=r3, c1=c1, o1=o1, o2=o2, v1=v1)
        self.finish()


class S16Olig2(Film):
    def construct(self):
        st = prior(self, S15Olig)
        self.at("lineage tracing")
        t1 = left_at(T("lineage tracing suggested:", 34, TEXT), XC, 1.95)
        self.play(FadeIn(t1), run_time=0.4)
        self.at("progenitors")
        t2 = left_at(T("acts in progenitors", 32, GOLD, weight=BOLD), XC + 2.75, L1)
        self.play(FadeIn(t2), Indicate(st["c1"], color=GOLD), run_time=0.6)
        self.at("make")
        c2 = left_at(chip("V2 interneurons", ORANGE, 34, pad=0.1), XC, 1.12)
        a1 = Arrow(c2.get_right(), c2.get_right() + RIGHT * 0.5, buff=0.05, color=GREY, stroke_width=4, tip_length=0.18)
        self.play(FadeIn(c2, shift=LEFT * 0.2), run_time=0.4)
        self.at("then")
        c3 = chip("astrocytes", GREY, 34, pad=0.1).next_to(a1, RIGHT, buff=0.05)
        c3.set_y(1.12)
        self.play(GrowArrow(a1), FadeIn(c3, shift=LEFT * 0.2), run_time=0.5)
        self.at("instead")
        c4 = left_at(chip("oligodendrocytes", LG, 34, pad=0.1), XC + 0.7, 0.43)
        xx = cross([XC + 0.3, 0.43, 0], w=0.4, h=0.4, sw=5)
        self.play(FadeIn(c4), Create(xx), run_time=0.5)
        self.st = dict(st, t1=t1, t2=t2, c2=c2, a1=a1, c3=c3, c4=c4, xx=xx)
        self.finish()


class S17Isl(Film):
    def construct(self):
        st = prior(self, S16Olig2)
        self.play(st["r2"].animate.set_stroke(opacity=0.8), run_time=0.3)
        self.at("islet")
        i1 = gchip("Isl1", YELLOW, [XA, R2C, 0])
        self.play(FadeIn(i1, shift=DOWN * 0.2), run_time=0.4)
        self.at("not generated")
        v2 = T("no", 40, RED, weight=BOLD).move_to([XB, R2C + 0.25, 0])
        self.play(FadeIn(v2, scale=0.8), run_time=0.5)
        self.at("at all")
        n2 = left_at(T("a class of Engrailed1\ninterneurons also fails", 30, TEXT, line_spacing=0.8), XC, R2C)
        cr = T("Pfaff et al., 1996", 30, TEXT).move_to([XB - 0.1, R2C - 0.45, 0])
        self.play(FadeIn(n2), FadeIn(cr), run_time=0.6)
        self.st = dict(st, i1=i1, v2=v2, n2=n2, cr=cr)
        self.finish()


class S18Lhx(Film):
    def construct(self):
        st = prior(self, S17Isl)
        q = T("?", 60, TEXT, weight=BOLD).move_to([XB, R3C, 0])
        self.at("puzzle")
        self.play(st["r3"].animate.set_stroke(opacity=0.8), FadeIn(q, scale=0.8), run_time=0.5)
        self.at("delete")
        l3 = gchip("Lhx3", BLUE, [XA, R3C + 0.34, 0])
        self.play(FadeIn(l3, shift=DOWN * 0.2), run_time=0.4)
        self.at("and")
        l4 = gchip("Lhx4", BLUE, [XA, R3C - 0.34, 0])
        self.play(FadeIn(l4, shift=DOWN * 0.2), run_time=0.4)
        self.at("still")
        yes = T("yes", 44, GREEN, weight=BOLD).move_to([XB, R3C, 0])
        self.play(ReplacementTransform(q, yes), run_time=0.5)
        self.st = dict(st, l3=l3, l4=l4, yes=yes)
        self.finish()


C19 = np.array([-2.6, -0.15, 0.0])


def route_pair(sx, sy, end_x, rise):
    """Usual route (dashed, straight out) and the new route (solid, bending up) from the same cell."""
    usual = DashedLine([sx, sy, 0], [end_x, sy, 0], dash_length=0.22, color=GREY, stroke_width=6)
    t = np.linspace(0, 1, 30)
    xs = sx + (end_x - sx) * t
    ys = sy + rise * (3 * t ** 2 - 2 * t ** 3)
    new = VMobject(color=GREEN, stroke_width=7).set_points_smoothly([[x, y, 0] for x, y in zip(xs, ys)])
    return usual, new


class S19Lhx2(Film):
    def construct(self):
        # fresh frame: the table was left behind at the cut; carry only the row's three facts, rebuilt in the top corner
        cord = cord_parts(C19, KB)
        mlab = T("mouse", 30, LG, weight=BOLD).move_to(C19 + [0, 3.4, 0])
        cells = VGroup(*[cell(P(C19, KB, lp), CR, GREEN, 0.5) for lp in MN_R + MN_L])
        dl = T("deleted:", 26, RED, weight=BOLD).move_to([0.8, 3.3, 0])
        l3 = gchip("Lhx3", BLUE, [2.4, 3.3, 0])
        l4 = gchip("Lhx4", BLUE, [4.0, 3.3, 0])
        yes = T("motor neurons made: yes", 32, GREEN, weight=BOLD).move_to([3.2, 2.45, 0])
        self.add(cord, mlab, cells, dl, l3, l4, yes)
        self.at("subclass")
        mut = mutant_cells(C19, KB, MN_R + MN_L)
        t1 = left_at(T("subclass changes", 34, TEXT, weight=BOLD), 0.6, 1.65)
        tl = leader([0.5, 1.65, 0], P(C19, KB, (1.4, -0.75)) + [0.2, 0.3, 0], LG)
        self.play(ReplacementTransform(cells, mut), FadeIn(t1, shift=RIGHT * 0.15), Create(tl), run_time=0.7)
        self.at("which way")
        sc_ = P(C19, KB, (1.4, -1.45))
        usual, new = route_pair(sc_[0] + 0.3, sc_[1], 5.7, 2.3)
        ul = T("usual route", 34, LG).move_to([4.5, sc_[1] - 0.5, 0])
        self.play(Create(usual), FadeIn(ul), run_time=0.7)
        self.at("axons")
        nl = T("new route", 34, GREEN, weight=BOLD).move_to([4.5, 1.25, 0])
        self.play(Create(new), FadeIn(nl), run_time=1.0)
        self.st = dict(cord=cord, mlab=mlab, cells=mut, dl=dl, l3=l3, l4=l4, yes=yes, t1=t1, tl=tl, usual=usual, new=new,
                       ul=ul, nl=nl)
        self.finish()
        self.wait(1.0)  # Hold the completed route comparison for inspection.


# ---------------------------------------------------------------------------------------------
# 20, 21 the apparent contradiction
# ---------------------------------------------------------------------------------------------
class S20Predict(Film):
    def construct(self):
        # left statement: the complex
        lt = T("Lhx3 is in the\nmotor-neuron complex", 32, TEXT, line_spacing=0.8).move_to([-3.4, 2.75, 0])
        lh = chip("Lhx3", BLUE, 40).move_to([-5.4, 0.7, 0])
        nl = chip("NLI", PURPLE, 40).move_to([-3.4, 0.7, 0])
        isl = chip("Isl1", YELLOW, 40).move_to([-1.4, 0.7, 0])
        links = VGroup(Line(lh.get_right(), nl.get_left(), color=GREY, stroke_width=6),
                       Line(nl.get_right(), isl.get_left(), color=GREY, stroke_width=6))
        box = RoundedRectangle(corner_radius=0.25, width=6.3, height=2.3, stroke_color=GREEN, stroke_width=4,
                               fill_color=GREEN, fill_opacity=0.06).move_to([-3.4, 0.7, 0])
        clab = T("motor-neuron complex", 30, GREEN).move_to([-3.4, -0.8, 0])
        # right statement: the mouse without Lhx3/4
        rt = T("motor neurons still form\nwithout Lhx3 and Lhx4", 32, TEXT, line_spacing=0.8).move_to([3.6, 2.75, 0])
        d3 = del_chip("Lhx3", BLUE, 34).move_to([2.3, 1.0, 0])
        d4 = del_chip("Lhx4", BLUE, 34).move_to([4.9, 1.0, 0])
        mc = VGroup(*[cell([2.4 + 0.85 * i + 0.0, -0.2 - 0.85 * j, 0], 0.35, GREEN, 0.5) for j in range(2) for i in range(3)])
        div = Line([0.1, 3.7, 0], [0.1, -1.95, 0], color=GREY, stroke_width=2).set_opacity(0.4)
        self.add(div)
        self.play(FadeIn(lt, shift=DOWN * 0.1), FadeIn(box), run_time=0.5)
        self.play(LaggedStart(FadeIn(lh, scale=0.8), FadeIn(nl, scale=0.8), FadeIn(isl, scale=0.8), lag_ratio=0.2),
                  Create(links), run_time=0.8)
        self.at("sits in")
        self.play(Indicate(lh, color=BLUE, scale_factor=1.15), run_time=0.7)
        self.at("motor neuron complex")
        self.play(FadeIn(clab), run_time=0.4)
        self.play(FadeIn(rt, shift=DOWN * 0.1), FadeIn(d3), FadeIn(d4), FadeIn(mc), run_time=0.8)
        self.at("how can")
        q = T("How can both be true?", 52, GOLD, font=TITLE_FONT).move_to([0, -2.3, 0])
        self.play(FadeIn(q, shift=UP * 0.2), run_time=0.6)
        self.st = dict(lt=lt, lh=lh, nl=nl, isl=isl, links=links, box=box, clab=clab, rt=rt, d3=d3, d4=d4, mc=mc, div=div, q=q)
        self.finish()


class S21Pause(Film):
    def construct(self):
        countdown(self, S20Predict, "pause and think", [0, -3.65, 0], w=5.0)


# ---------------------------------------------------------------------------------------------
# 22, 23 two different questions
# ---------------------------------------------------------------------------------------------
K22 = 0.86
CL = np.array([-3.4, -0.1, 0.0])
CRM = np.array([2.7, -0.1, 0.0])
CHICK_LOCS = [(0.7, -0.75), (1.4, -0.75), (0.7, -1.45), (1.4, -1.45), (0.7, -2.15), (1.4, -2.15)]


class S22Resolve(Film):
    def construct(self):
        div = Line([0.1, 3.7, 0], [0.1, -3.2, 0], color=GREY, stroke_width=2).set_opacity(0.4)
        cl = cord_parts(CL, K22, fill=0.3)
        cr = cord_parts(CRM, K22)
        self.add(div, cl, cr)
        self.at("different questions")
        s_lab = T("chick: sufficient", 36, TEXT, font=TITLE_FONT).move_to([-3.4, 3.5, 0])
        n_lab = T("mouse: necessary", 36, TEXT, font=TITLE_FONT).move_to([3.5, 3.5, 0])
        self.play(FadeIn(s_lab, shift=DOWN * 0.1), FadeIn(n_lab, shift=DOWN * 0.1), run_time=0.6)
        self.at("in")
        i1 = chip("Isl1", YELLOW, 32).move_to([-4.7, 2.8, 0])
        plus = T("+", 40, TEXT).move_to([-3.6, 2.8, 0])
        l1 = chip("Lhx3", BLUE, 32).move_to([-2.5, 2.8, 0])
        self.play(FadeIn(i1, shift=DOWN * 0.2), run_time=0.4)
        self.at("plus")
        self.play(FadeIn(plus), FadeIn(l1, shift=DOWN * 0.2), run_time=0.5)
        self.at("enough")
        cells = cells_at(CL, K22, CHICK_LOCS, GREY, 0.3)
        a = arr([-2.5, 2.35, 0], [-2.5, -0.15, 0], TEXT, w=7)
        self.play(GrowArrow(a), FadeIn(cells), run_time=0.6)
        self.at("start the")
        prog = T("motor-neuron programme", 28, GREEN).move_to([-3.4, -3.2, 0])
        self.play(*[c.animate.set_color(GREEN).set_fill(GREEN, 0.5) for c in cells], FadeIn(prog, shift=UP * 0.1), run_time=0.8)
        left = VGroup(cl, s_lab, i1, plus, l1, a, cells, prog)
        self.st = dict(div=div, cl=cl, cr=cr, s_lab=s_lab, n_lab=n_lab, i1=i1, plus=plus, l1=l1,
                       a=a, cells_l=cells, prog=prog, left=left)
        self.finish()


class S23Resolve2(Film):
    def construct(self):
        st = prior(self, S22Resolve)
        mc, mk = np.array([1.3, -0.1, 0.0]), 0.96
        self.play(st["left"].animate.scale(0.78).shift(LEFT * 0.7).set_opacity(0.35),
                  st["cr"].animate.scale(mk / K22).move_to(mc),
                  st["n_lab"].animate.set_x(2.0), FadeOut(st["div"]), run_time=0.4)
        self.at("motor neurons")
        cells = cells_at(mc, mk, MN_R + MN_L, GREEN, 0.5)
        self.play(LaggedStart(*[GrowFromCenter(c) for c in cells], lag_ratio=0.06), run_time=0.9)
        self.at("without")
        d3 = del_chip("Lhx3", BLUE, 30).move_to([0.2, 2.8, 0])
        d4 = del_chip("Lhx4", BLUE, 30).move_to([2.4, 2.8, 0])
        self.play(FadeIn(d3), FadeIn(d4), run_time=0.5)
        self.at("different kind")
        mut = mutant_cells(mc, mk, MN_R + MN_L)
        sx = P(mc, mk, (1.4, -1.45))
        usual, new = route_pair(sx[0] + 0.2, sx[1], 5.9, 2.0)
        dk = T("squares: different subclass", 32, GREEN).move_to([1.3, 1.75, 0])
        ul = T("usual route", 32, LG).move_to([4.8, sx[1] - 0.5, 0])
        key = T("circles: motor neurons", 28, LG).move_to([-4.0, -2.55, 0])
        self.play(ReplacementTransform(cells, mut), FadeIn(dk, shift=UP * 0.1), FadeIn(key), run_time=0.7)
        self.play(Create(usual), FadeIn(ul), run_time=0.4)
        self.play(Create(new), FadeIn(T("new route", 32, GREEN, weight=BOLD).move_to([4.8, 1.05, 0])), run_time=0.6)
        self.at("sufficient")
        ban = T("Sufficient is not the same as necessary.", 34, TEXT, font=TITLE_FONT).move_to([0.0, -3.52, 0])
        self.play(FadeIn(ban, shift=UP * 0.2), run_time=0.8)
        self.st = dict(st, cells_r=mut, d3=d3, d4=d4, usual=usual, new=new, ban=ban, dk=dk, ul=ul, key=key)
        self.finish()


class S24Beat(Film):
    def construct(self):
        hold(self, S23Resolve2)


# ---------------------------------------------------------------------------------------------
# 25 takeaway, 26 end
# ---------------------------------------------------------------------------------------------
class S25Take(Film):
    def construct(self):
        xs = [-4.4, 0.0, 4.4]
        words = [T(w, 80, TEXT, font=TITLE_FONT).move_to([x, 2.55, 0]) for w, x in zip(("enough", "needed", "kept"), xs)]
        for w in words:           # one shared baseline: align on the letters that have no descender
            keep = [g for g, ch in zip(w.submobjects, [c for c in w.text if c != " "]) if ch not in "gjpqy"]
            w.shift(UP * (2.2 - min(g.get_bottom()[1] for g in keep)))
        rule = Line([-6.4, 1.85, 0], [6.4, 1.85, 0], color=GOLD, stroke_width=4)

        def card(x, color, l1, l2):
            box = RoundedRectangle(corner_radius=0.2, width=4.1, height=2.5, stroke_color=color, stroke_width=3,
                                   fill_color=color, fill_opacity=0.08).move_to([x, 0.4, 0])
            t1 = T(l1, 34, color, weight=BOLD).move_to([x, 1.1, 0])
            t2 = T(l2, 30, TEXT, line_spacing=0.8).move_to([x, 0.1, 0])
            return VGroup(box, t1, t2)

        c1 = card(xs[0], MINT, "add it", "electroporation\n(chick)")
        c2 = card(xs[1], RED, "remove it", "gene deletion\n(mouse)")
        c3 = card(xs[2], PINK, "Mnx1", "keeps a motor\nneuron's identity")
        tk = T("takeaway", 30, GOLD, weight=BOLD).move_to([0, 3.6, 0])
        self.play(FadeIn(tk), run_time=0.3)
        self.at("enough")
        self.play(FadeIn(words[0], shift=UP * 0.2), FadeIn(c1, shift=UP * 0.15), Create(rule), run_time=0.6)
        self.at("needed")
        self.play(FadeIn(words[1], shift=UP * 0.2), FadeIn(c2, shift=UP * 0.15), run_time=0.6)
        self.at("kept")
        self.play(FadeIn(words[2], shift=UP * 0.2), FadeIn(c3, shift=UP * 0.15), run_time=0.6)
        self.at("different jobs")
        jobs = T("three different jobs", 46, GOLD).move_to([0, -1.45, 0])
        self.play(FadeIn(jobs, shift=UP * 0.15), run_time=0.5)
        self.at("each test")
        one = T("each test answers only one", 54, TEXT, font=TITLE_FONT).move_to([0, -2.75, 0])
        self.play(FadeIn(one, shift=UP * 0.15), run_time=0.6)
        self.finish()


class S26End(EndCard):
    LINE = "Enough, needed, and kept are different jobs; each test answers only one."

    def construct(self):
        a = T("Enough, needed, and kept are different jobs;", 46, TEXT, font=TITLE_FONT)
        b = T("each test answers only one.", 46, TEXT, font=TITLE_FONT)
        sub = T("biochemistrypedia.com", 26, TEAL)
        g = VGroup(a, b, sub).arrange(DOWN, buff=0.35)
        g[2].shift(DOWN * 0.3)
        g.move_to(ORIGIN)
        self.play(FadeIn(VGroup(a, b), shift=UP * 0.15), run_time=0.4)
        self.play(FadeIn(sub), run_time=0.2)
        self.finish()
