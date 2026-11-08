"""Neural crest, chapter 2: Mark It, Move It.

COLOR MAP (one colour per concept, shared by every chapter of the series)
  YELLOW = neural crest cells; donor (grafted) cells are yellow with a BLUE mark
  BLUE   = the built-in mark: quail chromatin block, dye (a dark clump with a blue edge)
  VIOLET = the generic tag in the opening idea (scene s02 only; not the chromatin mark)
  TEAL   = neurons and ganglia (peripheral neural derivatives)
  GREEN  = route taken / observed result (route arrow, cholinergic neurons that lit up)
  RED    = doubt, a crack in a rule
  GREY   = embryo structure, host tissue, labels
  GOLD   = questions, predict cards, highlights
  TEXT   = pigment cells, cartilage (neutral), plain labels
"""
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

VIOLET = "#C792EA"
CLUMP = "#0E3F5C"      # dark fill of the dense chromatin block (edge is BLUE)


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def P(x, y):
    return np.array([x, y, 0.0])


def lab(txt, x, y, size=32, color=TEXT, **kw):
    return T(txt, size, color, **kw).move_to(P(x, y))


def lab_l(txt, xl, y, size=32, color=TEXT):
    t = T(txt, size, color)
    t.move_to(P(xl, y))
    t.shift(RIGHT * t.width / 2)
    return t


def path(*pts):
    return VMobject().set_points_smoothly([P(*p) if len(p) == 2 else np.array(p) for p in pts])


def crest(r=0.22, op=0.65, color=YELLOW):
    return Circle(radius=r, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=op)


def mark_block(r):
    return RoundedRectangle(corner_radius=r * 0.08, width=r * 0.62, height=r * 0.42, stroke_width=0,
                            fill_color=BLUE, fill_opacity=1)


def donor(r=0.22, x=0.0, y=0.0):
    c = crest(r, 0.85)
    b = mark_block(r).move_to(c.get_center() + np.array([r * 0.12, -r * 0.1, 0]))
    return VGroup(c, b).move_to(P(x, y))


def plain_cell(r, color=GREY, op=0.3, x=0.0, y=0.0):
    return Circle(radius=r, stroke_color=color, stroke_width=1.8, fill_color=color, fill_opacity=op).move_to(P(x, y))


def pale_cell(r, x, y):
    """A cell in a fixed section: pale, nothing about it says it is labelled."""
    return Circle(radius=r, stroke_color=TEXT, stroke_width=2, fill_color=TEXT, fill_opacity=0.6).move_to(P(x, y))


def qmark(x, y, size=64, r=0.5):
    q = T("?", size, GOLD, weight=BOLD)
    back = Circle(radius=r, stroke_width=0, fill_color=BG, fill_opacity=0.85)
    return VGroup(back, q).move_to(P(x, y))


def blob(cx, cy, r, seed=3, n=8):
    rng = random.Random(seed)
    pts = []
    for i in range(n):
        a = 2 * np.pi * i / n
        rr = r * rng.uniform(0.82, 1.15)
        pts.append(P(cx + rr * np.cos(a), cy + rr * 0.85 * np.sin(a)))
    m = VMobject(stroke_color=BLUE, stroke_width=3, fill_color=CLUMP, fill_opacity=1)
    m.set_points_smoothly(pts + [pts[0]])
    return m


def tube_bar(y=2.9, w=12.4, h=1.3):
    return RoundedRectangle(corner_radius=0.5, width=w, height=h, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.2).move_to(P(0, y))


def grey_field(seed=3):
    rng = random.Random(seed)
    cells = []
    for i in range(13):
        for j in range(5):
            x = -6.0 + i * 1.0 + rng.uniform(-0.1, 0.1)
            y = 1.3 - j * 1.1 + rng.uniform(-0.1, 0.1)
            cells.append(plain_cell(0.42, GREY, 0.28, x, y))
    return VGroup(*cells)


# ---------------------------------------------------------------------------------------------
# embryo cartoon shared by the predict-1 scenes and the reverse graft
# ---------------------------------------------------------------------------------------------
EMB_X = -3.2
NECK_Y = 1.5
ADR_Y = -1.5
ARR_X = -5.15
COL_X = 4.7          # centre of the right-hand text column


def embryo_body(cx=EMB_X):
    body = RoundedRectangle(corner_radius=1.1, width=2.8, height=5.6, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.15).move_to(P(cx, -0.9))
    head = Circle(0.95, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.15).move_to(P(cx, 2.8))
    return VGroup(head, body)


def level_line(y, color=GREY, cx=EMB_X):
    return DashedLine(P(cx - 1.5, y), P(cx + 1.5, y), color=color, stroke_width=3, dash_length=0.15)


def neck_level():
    return VGroup(level_line(NECK_Y), lab_l("neck (vagal)", EMB_X + 1.65, NECK_Y, 32, GREY))


def adr_level():
    return VGroup(level_line(ADR_Y), lab_l("adrenal level", EMB_X + 1.65, ADR_Y + 0.0, 32, GREY))


def cells_at(y, cx=EMB_X, r=0.38, dxs=(-0.8, 0.0, 0.8)):
    return VGroup(*[donor(r, cx + dx, y) for dx in dxs])


def move_arrow(y0, y1, color=GOLD):
    return Arrow(P(ARR_X, y0), P(ARR_X, y1), buff=0, color=color, stroke_width=6, tip_length=0.34)



def pred1_home():
    lbl = lab("at home:\ncells that release", COL_X, 1.95, 32, GREY)
    c1 = chip("noradrenaline", TEXT, 34).move_to(P(COL_X, 0.65))
    c2 = chip("adrenaline", TEXT, 34).move_to(P(COL_X, -0.4))
    return lbl, c1, c2


def pred1_questions():
    q1 = chip("where will it go?", GOLD, 32).move_to(P(COL_X, -1.65))
    q2 = chip("what transmitter?", GOLD, 32).move_to(P(COL_X, -2.85))
    return q1, q2


def trunk_label():
    return lab_l("adrenomedullary trunk", EMB_X + 1.65, ADR_Y - 0.55, 28, YELLOW)


def pred1_final():
    """The question left on screen after s10 (also held by s11)."""
    emb = embryo_body()
    neck = neck_level()
    adr = adr_level()
    tl = trunk_label()
    cells = cells_at(NECK_Y)
    arr = move_arrow(ADR_Y + 0.2, NECK_Y - 0.2)
    pred = chip("Predict", GOLD, 32).move_to(P(COL_X, 3.3))
    home = VGroup(*pred1_home())
    q1, q2 = pred1_questions()
    return dict(emb=emb, neck=neck, adr=adr, tl=tl, cells=cells, arr=arr, pred=pred, home=home, q1=q1, q2=q2)


# ----- the gut ring, ganglia and donor cells (s12, s13, s13b) -----
RING_C = (2.7, -0.1)
GANG_R = 2.7
GANG_POS = [(RING_C[0] + GANG_R * np.cos(np.radians(a)), RING_C[1] + GANG_R * np.sin(np.radians(a)))
            for a in (90, 210, 330)]


def gut_ring():
    return Annulus(inner_radius=1.9, outer_radius=3.5, stroke_color=GREY, stroke_width=3,
                   fill_color=GREY, fill_opacity=0.22).move_to(P(*RING_C))


def ganglion(x, y, w=1.7, h=1.3, color=TEAL, op=0.4):
    return Ellipse(width=w, height=h, stroke_color=color, stroke_width=3, fill_color=color,
                   fill_opacity=op).move_to(P(x, y))


def ring_cells_final():
    out = []
    for (gx, gy) in GANG_POS:
        out.append(donor(0.25, gx - 0.35, gy))
        out.append(donor(0.25, gx + 0.35, gy))
    return out


def ring_labels(with_ganglia=True):
    ring_lab = lab("gut wall", RING_C[0], RING_C[1] + 0.5, 36, GREY)
    gang_lab = lab("enteric\nganglia", RING_C[0], RING_C[1] - 0.45, 32, TEAL)
    return ring_lab, gang_lab


LIT = (0, 3, 4)


def rev2_scene(lit=True):
    ring = gut_ring()
    gl = [ganglion(x, y) for (x, y) in GANG_POS]
    cs = ring_cells_final()
    if lit:
        for i in LIT:
            cs[i][0].set_fill(GREEN, 0.95).set_stroke(GREEN)
    ring_lab, gang_lab = ring_labels()
    return ring, gl, cs, ring_lab, gang_lab


def rev2_left(stage):
    """Left-hand column of s13: stage 1 = donor neurons + acetylcholine, 2 = + at-home comparison, 3 = + result tag."""
    l1 = lab("some donor neurons", -3.7, 2.7, 34, GREEN)
    l2 = chip("acetylcholine", GREEN, 36).move_to(P(-3.7, 1.6))
    hl = lab("at home (trunk):", -3.7, 0.0, 32, TEXT)
    hc1 = chip("noradrenaline", TEXT, 32).move_to(P(-3.7, -0.9))
    hc2 = chip("adrenaline", TEXT, 32).move_to(P(-3.7, -1.9))
    pr = chip("population result", GOLD, 32, fill_opacity=1).move_to(P(2.7, -3.3))
    pr[0].set_fill(BG, opacity=1)
    pr.set_z_index(5)
    return l1, l2, hl, hc1, hc2, pr


# ----- head sections (s15, s16) -----
PAN_CY = -0.15
PAN_W, PAN_H = 6.1, 5.5
PAN_LX, PAN_RX = -3.5, 3.5


def head_panel(cx, cy=PAN_CY):
    frame = RoundedRectangle(corner_radius=0.3, width=PAN_W, height=PAN_H, stroke_color=GREY, stroke_width=3,
                             fill_color=GREY, fill_opacity=0.08).move_to(P(cx, cy))
    tube = Circle(0.6, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.25
                  ).move_to(P(cx, cy + 1.9))
    arches = [Ellipse(width=1.9, height=1.5, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                      fill_opacity=0.18).move_to(P(cx + s * 1.9, cy - 0.6)) for s in (-1, 1)]
    cart = [Ellipse(width=1.0, height=0.65, stroke_color=TEXT, stroke_width=2, fill_color=TEXT,
                    fill_opacity=0.5).move_to(P(cx + s * 1.9, cy - 0.6)) for s in (-1, 1)]
    return VGroup(frame, tube, *arches, *cart)


def head_donor_pts(cx, cy, mode):
    pts = []
    for s in (-1, 1):
        ax, ay = cx + s * 1.9, cy - 0.6
        if mode == "early":
            offs = [(0, 0.5), (0.62, 0.22), (-0.62, 0.22), (0.6, -0.45), (-0.6, -0.45)]
        else:
            offs = [(-0.24, 0.1), (0.24, 0.1), (0.0, -0.14), (0.6, -0.42), (-0.6, -0.42)]
        pts += [(ax + dx, ay + dy) for dx, dy in offs]
    return pts


def head_donors(cx, cy, mode):
    return VGroup(*[donor(0.17, x, y) for (x, y) in head_donor_pts(cx, cy, mode)])


# ----- embryo / dish for the predict-3 scenes (s17 to s19) -----
EMB2 = (4.2, -0.45)
DISH = (-4.0, 0.3)
DISH_R = 2.6
HDR = (0.75, 3.4)


def embryo2():
    body = RoundedRectangle(corner_radius=1.0, width=2.6, height=5.2, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.15).move_to(P(EMB2[0], EMB2[1]))
    head = Circle(0.85, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.15
                  ).move_to(P(EMB2[0], 2.85))
    return VGroup(head, body)


def dish_shape():
    return Circle(DISH_R, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.1).move_to(P(*DISH))


NEURON_POS = [(-1.1, 0.7), (0.1, 1.3), (1.2, 0.55), (-0.8, -0.7), (0.2, -0.15)]
PIGMENT_POS = [(1.25, -0.95), (-0.1, -1.3), (-1.5, -0.1)]
FOUNDER = (EMB2[0], 0.9)


def colony():
    ns = VGroup(*[plain_cell(0.33, TEAL, 0.85, DISH[0] + x, DISH[1] + y) for x, y in NEURON_POS])
    ps = VGroup(*[plain_cell(0.33, TEXT, 0.8, DISH[0] + x, DISH[1] + y) for x, y in PIGMENT_POS])
    return ns, ps


def dish_chips():
    n = chip("neurons", TEAL, 32).move_to(P(-5.4, -3.3))
    p = chip("pigment cells", TEXT, 32).move_to(P(-2.4, -3.3))
    return n, p


def embryo_founder():
    return crest(0.38, 0.9).move_to(P(*FOUNDER))


def embryo_q():
    return qmark(EMB2[0], -0.9, 96, 0.65)


def pred3_state():
    dish = dish_shape()
    ns, ps = colony()
    dl = lab("dish", DISH[0], 3.4, 40, GREY)
    chips = dish_chips()
    emb = embryo2()
    el = lab("embryo", EMB2[0], -3.5, 36, GREY)
    founder = embryo_founder()
    q = embryo_q()
    pred = chip("Predict", GOLD, 34).move_to(P(*HDR))
    return dict(dish=dish, ns=ns, ps=ps, dl=dl, chips=chips, emb=emb, el=el, founder=founder, q=q, pred=pred)


def add_pred3(scene, st):
    scene.add(st["dish"], st["ns"], st["ps"], st["dl"], *st["chips"], st["emb"], st["el"], st["founder"], st["q"],
              st["pred"])


# ---------------------------------------------------------------------------------------------
# scenes
# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "The Neural Crest: Cells That Leave Home"
    TITLE = "Mark It, Move It"

    def construct(self):
        brand = T("BIOCHEMISTRYPEDIA", 28, TEAL, weight=BOLD).set_opacity(0.95)
        lesson = T(self.LESSON.upper(), 30, GREY)
        title = T(self.TITLE, 96, font=TITLE_FONT)
        fit(title, max_w=12.2)
        rule = Line(LEFT * 1.6, RIGHT * 1.6, color=GOLD, stroke_width=5)
        g = VGroup(brand, lesson, title, rule).arrange(DOWN, buff=0.5)
        fit(g, max_w=12.4)
        self.play(FadeIn(g, shift=UP * 0.12), run_time=0.5)
        self.finish()


class S01Q(SpokenScene):
    def construct(self):
        tube, field = tube_bar(), grey_field()
        tl = lab("neural tube", 4.3, 2.9, 32, GREY)
        cell = crest(0.5, 0.95).move_to(P(-1.5, 2.9))
        self.play(FadeIn(tube), FadeIn(field), FadeIn(tl), FadeIn(cell), run_time=0.4)
        self.at("that leaves")
        rt = path((-1.5, 2.9), (-1.4, 1.5), (-0.2, -0.1), (1.5, -1.5))
        self.play(MoveAlongPath(cell, rt), run_time=0.8)
        self.play(cell.animate.set_fill(GREY, 0.28).set_stroke(GREY, 1.8).scale(0.84), FadeIn(qmark(1.5, -1.5)),
                  run_time=0.5)
        self.finish()


class S02Mark(SpokenScene):
    def construct(self):
        tube, field = tube_bar(), grey_field()
        tl = lab("neural tube", 4.3, 2.9, 32, GREY)
        self.add(tube, field, tl)
        cell = crest(0.5, 0.95).move_to(P(-1.5, 2.9))
        self.play(FadeIn(cell), run_time=0.3)
        tag = RoundedRectangle(corner_radius=0.05, width=0.46, height=0.3, stroke_width=0, fill_color=VIOLET,
                               fill_opacity=1).move_to(P(-1.12, 3.1))
        mk = lab("mark", 0.6, 2.9, 36, VIOLET)
        mkline = Line(P(0.05, 2.95), P(-0.85, 3.08), color=VIOLET, stroke_width=3)
        self.at("mark it")
        self.play(FadeIn(tag, shift=DOWN * 0.2), FadeIn(mk), Create(mkline), run_time=0.4)
        grp = VGroup(cell, tag)
        self.at("before it goes")
        c0 = grp.get_center()
        rt = VMobject().set_points_smoothly([c0, c0 + P(0.1, -1.4), c0 + P(1.3, -3.0), c0 + P(3.0, -4.4)])
        self.play(FadeOut(mk), FadeOut(mkline), MoveAlongPath(grp, rt), run_time=1.0)
        self.at("and the mark")
        mk2 = lab("still marked", 3.6, -2.3, 34, VIOLET)
        self.play(FadeIn(mk2), run_time=0.4)
        self.at("has to last")
        self.play(Indicate(tag, color=VIOLET, scale_factor=2.0), run_time=0.9)
        self.finish()


def mudpuppy():
    body = Ellipse(width=4.6, height=1.3, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.25)
    head = Ellipse(width=1.8, height=1.25, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                   fill_opacity=0.3).move_to(P(-2.6, 0.0))
    pts = [P(2.0, 0.6), P(3.4, 0.55), P(4.9, 0.1), P(3.4, -0.55), P(2.0, -0.6)]
    tail = VMobject(stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.25)
    tail.set_points_smoothly(pts + [pts[0]])
    legs = VGroup()
    for (x, y, d) in ((-1.4, -0.55, -1), (1.2, -0.55, -1), (-1.1, 0.55, 1), (1.4, 0.55, 1)):
        end = P(x - 0.4, y + d * 0.7)
        legs.add(Line(P(x, y), end, color=GREY, stroke_width=9))
        for ang in (-25, 0, 25):
            a = (270 if d < 0 else 90) + ang
            legs.add(Line(end, end + P(0.28 * np.cos(a * DEGREES), 0.28 * np.sin(a * DEGREES)),
                          color=GREY, stroke_width=4))
    gills = VGroup()
    for s in (1, -1):
        for (ex, ey) in ((-3.75, 1.2), (-3.2, 1.45), (-2.65, 1.5)):
            base = P(-2.85 + 0.0, s * 0.5)
            end = P(ex, s * ey)
            gills.add(Line(base, end, color=GREY, stroke_width=5))
            for f in (0.35, 0.55, 0.75, 0.95):
                p = base + (end - base) * f
                gills.add(Line(p, p + P(-0.3, s * 0.08), color=GREY, stroke_width=3))
                gills.add(Line(p, p + P(0.3, s * 0.08), color=GREY, stroke_width=3))
    eyes = VGroup(Dot(P(-3.0, 0.3), radius=0.08, color=TEXT), Dot(P(-3.0, -0.3), radius=0.08, color=TEXT))
    return VGroup(tail, body, legs, head, gills, eyes)


class S03Platt(SpokenScene):
    def construct(self):
        name = T("Julia Platt", 60, font=TITLE_FONT).move_to(P(0, 0.4))
        self.play(FadeIn(name, shift=UP * 0.15), run_time=0.7)
        animal = mudpuppy().scale(1.3)
        animal.move_to(P(0.0, 0.25))
        year = T("1893", 58, GOLD, font=TITLE_FONT).move_to(P(4.6, 3.25))
        self.at("in 1893")
        self.play(name.animate.scale(0.8).move_to(P(-4.0, 3.25)), FadeIn(year, shift=UP * 0.15),
                  FadeIn(animal, shift=UP * 0.15), run_time=1.0)
        self.at("mud puppy")
        l1 = lab("mudpuppy", 0, -2.55, 54, TEXT)
        self.play(FadeIn(l1), run_time=0.5)
        self.at("a salamander")
        l2 = lab("a salamander", 0, -3.35, 42, GREY)
        self.play(FadeIn(l2), run_time=0.5)
        self.finish()


def mini_section(cx, cy, w, h):
    """One fixed section of a head: frame, neural tube and the two arches (proportional to w, h)."""
    frame = RoundedRectangle(corner_radius=0.25, width=w, height=h, stroke_color=GREY, stroke_width=3,
                             fill_color=GREY, fill_opacity=0.08).move_to(P(cx, cy))
    tube = Circle(0.098 * h, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.25
                  ).move_to(P(cx, cy + 0.34 * h))
    arches = [Ellipse(width=0.35 * w, height=0.2 * h, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                      fill_opacity=0.18).move_to(P(cx + s * 0.26 * w, cy - 0.15 * h)) for s in (-1, 1)]
    return VGroup(frame, tube, *arches), arches


class S04Arches(SpokenScene):
    def construct(self):
        cy, w, h = -0.3, 4.0, 5.6
        xs = [-4.3, 0.0, 4.3]
        secs, arch_lists, titles = [], [], []
        for i, x in enumerate(xs):
            s, a = mini_section(x, cy, w, h)
            secs.append(s)
            arch_lists.append(a)
            titles.append(lab(f"section {i + 1}", x, 3.2, 32, GREY))
        self.play(LaggedStart(*[AnimationGroup(FadeIn(s), FadeIn(t)) for s, t in zip(secs, titles)], lag_ratio=0.3),
                  run_time=1.2)
        tube_y = cy + 0.34 * h
        c1 = VGroup(*[pale_cell(0.17, xs[0] + dx, tube_y - 0.75) for dx in (-0.35, 0.0, 0.35)])
        c2 = VGroup(*[pale_cell(0.17, xs[1] + s * dx, tube_y - dy) for s in (-1, 1)
                      for dx, dy in ((0.6, 1.1), (0.95, 1.95))])
        ay = cy - 0.15 * h
        c3 = VGroup(*[pale_cell(0.17, xs[2] + s * 1.04 + dx, ay + dy) for s in (-1, 1)
                      for dx, dy in ((-0.25, 0.12), (0.25, -0.12))])
        self.at("she followed")
        self.play(FadeIn(c1), run_time=0.5)
        self.at("from the crest")
        self.play(FadeIn(c2), run_time=0.6)
        self.at("into the arches")
        al = lab("arches", xs[2], cy - 1.95, 32, GREY)
        lines = VGroup(*[Line(P(xs[2] + s * 0.25, cy - 1.72), P(xs[2] + s * 1.0, ay - 0.58), color=GREY,
                              stroke_width=2.5) for s in (-1, 1)])
        self.play(FadeIn(c3), FadeIn(al), Create(lines), run_time=0.7)
        self.at("head cartilage")
        cl = lab("head cartilage", xs[2], cy - 2.5, 32, TEXT)
        self.play(*[a.animate.set_fill(TEXT, 0.3).set_stroke(TEXT) for a in arch_lists[2]], FadeIn(cl), run_time=0.8)
        self.finish()


class S05Doubt(SpokenScene):
    def construct(self):
        card = RoundedRectangle(corner_radius=0.3, width=12.4, height=2.8, stroke_color=GREY, stroke_width=4,
                                fill_color=GREY, fill_opacity=0.15).move_to(P(0, 2.35))
        txt = T("Cartilage comes from mesoderm", 56, font=TITLE_FONT).move_to(P(0, 2.85))
        rule = lab("the rule", -4.9, 1.5, 30, GOLD)
        self.play(FadeIn(card), Write(txt), FadeIn(rule), run_time=1.5)
        self.at("her evidence")
        thumbs = VGroup()
        for x in (-4.2, 0, 4.2):
            s, _ = mini_section(x, -0.95, 3.8, 3.0)
            thumbs.add(s)
        note = lab("fixed sections: no living cell labelled", 0, -3.3, 34, GREY)
        self.play(FadeIn(thumbs, shift=UP * 0.15), FadeIn(note), run_time=0.9)
        self.at("claim was long")
        crack = VMobject(color=RED, stroke_width=9).set_points_as_corners(
            [P(-0.5, 3.75), P(0.25, 3.2), P(-0.35, 2.6), P(0.3, 2.0), P(-0.15, 0.95)])
        dbt = chip("long doubted", RED, 36).move_to(P(3.7, 1.5))
        self.play(Create(crack), card.animate.set_stroke(RED), txt.animate.set_opacity(0.65), FadeIn(dbt),
                  run_time=0.8)
        self.finish()


def nucleus(cx, cy, quail, R=2.5):
    nuc = Circle(R, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.22).move_to(P(cx, cy))
    nct = P(cx - 0.26 * R, cy + 0.23 * R)
    nucleolus = Circle(0.2 * R, stroke_color=TEXT, stroke_width=2, fill_color=TEXT, fill_opacity=0.6).move_to(nct)
    bc = nct + P(0.24 * R, -0.22 * R)
    rng = random.Random(7 if quail else 11)
    specks = VGroup()
    while len(specks) < 14:
        p = P(cx + rng.uniform(-0.9, 0.9) * R, cy + rng.uniform(-0.9, 0.9) * R)
        if np.linalg.norm(p - P(cx, cy)) < 0.85 * R and np.linalg.norm(p - nct) > 0.45 * R \
                and np.linalg.norm(p - bc) > 0.4 * R:
            specks.add(Dot(p, radius=0.06, color=GREY))
    g = VGroup(nuc, specks, nucleolus)
    block_ = blob(bc[0], bc[1], 0.19 * R, seed=5)
    return g, block_


class S06Quail(SpokenScene):
    def construct(self):
        qn, qblock = nucleus(-3.55, -0.1, True)
        cn, _ = nucleus(3.55, -0.1, False)
        self.play(FadeIn(qn), FadeIn(cn), run_time=0.5)
        self.at("lasting mark")
        mk = lab("the lasting mark", 0, 3.4, 40, BLUE)
        self.play(FadeIn(mk, shift=DOWN * 0.1), run_time=0.5)
        self.at("nicole")
        name = lab("Nicole Le Douarin", 0, 3.4, 40, TEXT)
        self.play(ReplacementTransform(mk, name), run_time=0.5)
        self.at("quail nuclei")
        ql = lab("quail", -3.55, 3.3, 42, TEXT)
        self.play(FadeIn(ql), qn[0].animate.set_stroke(TEXT), run_time=0.5)
        self.at("dense block")
        bl = lab("dense block of chromatin", -3.55, -3.45, 32, BLUE)
        ln = Line(P(-3.55, -3.15), qblock.get_bottom(), color=BLUE, stroke_width=3)
        self.play(GrowFromCenter(qblock), FadeIn(bl), Create(ln), run_time=0.8)
        self.at("chick nuclei")
        cl = lab("chick", 3.55, 3.3, 42, TEXT)
        self.play(FadeIn(cl), cn[0].animate.set_stroke(TEXT), run_time=0.5)
        self.at("lack it")
        nb = lab("no block", 3.55, -3.45, 32, GREY)
        self.play(FadeIn(nb), run_time=0.5)
        self.finish()


def mcell(r, x, y):
    out = Circle(r, stroke_color=YELLOW, stroke_width=2.5, fill_color=YELLOW, fill_opacity=0.22)
    nuc = Circle(r * 0.55, stroke_color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=0.35)
    blk = RoundedRectangle(corner_radius=r * 0.05, width=r * 0.4, height=r * 0.3, stroke_width=1.5,
                           stroke_color=BLUE, fill_color=CLUMP, fill_opacity=1
                           ).move_to(nuc.get_center() + np.array([r * 0.12, -r * 0.1, 0]))
    return VGroup(out, nuc, blk).move_to(P(x, y))


STAGES = {
    1: ([(-5.7, 0.0)], 1.1),
    2: ([(-2.0, 1.05), (-2.0, -1.05)], 0.95),
    4: ([(1.5 + dx, dy) for dx in (-0.8, 0.8) for dy in (-0.8, 0.8)], 0.75),
    8: ([(5.55 + dx, dy) for dx in (-0.62, 0.62) for dy in (-1.86, -0.62, 0.62, 1.86)], 0.56),
}


def stage(n):
    pos, rr = STAGES[n]
    return VGroup(*[mcell(rr, x, y) for (x, y) in pos])


def cnt_label(n, txt):
    xs = {1: -5.7, 2: -2.0, 4: 1.5, 8: 5.55}
    return lab(txt, xs[n], 3.4, 36, GREY)


class S07Built(SpokenScene):
    def construct(self):
        g1 = stage(1)
        c1 = cnt_label(1, "1 cell")
        a1 = Arrow(P(-4.4, 0), P(-3.2, 0), buff=0, color=GOLD, stroke_width=5, tip_length=0.28)
        dv = lab("divide", -3.8, 0.6, 32, GOLD)
        g2 = stage(2)
        self.add(g1, c1, a1, dv)
        self.play(*[TransformFromCopy(g1[0], c) for c in g2],
                  FadeIn(cnt_label(2, "2 cells")), run_time=0.6)
        self.at("built into")
        mk = lab("the mark", -5.7, -2.3, 34, BLUE)
        blk = g1[0][2]
        mkline = Line(P(-5.7, -1.95), blk.get_bottom() + DOWN * 0.02, color=BLUE, stroke_width=3)
        self.play(FadeIn(mk), Create(mkline), blk.animate.scale(1.4), run_time=0.8)
        self.at("neither fades")
        self.play(*[Indicate(c[2], color=BLUE) for c in g2], run_time=0.5)
        self.at("nor dilutes")
        a2 = Arrow(P(-0.9, 0), P(-0.25, 0), buff=0, color=GOLD, stroke_width=5, tip_length=0.25)
        g4 = stage(4)
        self.play(GrowArrow(a2), *[TransformFromCopy(g2[i // 2], c) for i, c in enumerate(g4)],
                  FadeIn(cnt_label(4, "4 cells")), run_time=0.7)
        self.at("as cells divide")
        a3 = Arrow(P(3.2, 0), P(4.0, 0), buff=0, color=GOLD, stroke_width=5, tip_length=0.25)
        g8 = stage(8)
        self.play(GrowArrow(a3), *[TransformFromCopy(g4[i // 2], c) for i, c in enumerate(g8)],
                  FadeIn(cnt_label(8, "8 cells")), run_time=0.7)
        note = lab("same mark in every cell", 0, -3.5, 38, BLUE)
        self.play(FadeIn(note), run_time=0.4)
        self.finish()


def quail_segment(x, y, w=3.0, h=2.6):
    r = Rectangle(width=w, height=h, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.35)
    dots = VGroup(*[Dot(P(dx * w / 3.0, dy * h / 2.6), radius=0.1, color=BLUE)
                    for dx in (-0.8, 0.0, 0.8) for dy in (-0.6, 0.6)])
    return VGroup(r, dots).move_to(P(x, y))


def chick_tube(x0, x1, y, h=2.6):
    return Rectangle(width=x1 - x0, height=h, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                     fill_opacity=0.2).move_to(P((x0 + x1) / 2, y))


class S08Iso(SpokenScene):
    def construct(self):
        ty = -0.4
        left, right = chick_tube(-6.7, -1.5, ty), chick_tube(1.5, 6.7, ty)
        seg = quail_segment(0, 1.8)
        cl = lab("chick", -4.1, -2.35, 38, GREY)
        ql = lab("quail", 3.1, 1.8, 38, YELLOW)
        scene1 = VGroup(left, right, seg, cl, ql)
        self.play(FadeIn(left), FadeIn(right), FadeIn(cl), run_time=0.4)
        self.play(FadeIn(seg, shift=DOWN * 0.2), FadeIn(ql), run_time=0.4)
        self.at("into a chick")
        self.play(seg.animate.move_to(P(0, ty)), FadeOut(ql), run_time=0.8)
        self.at("same level")
        br = Line(P(-1.5, -1.95), P(1.5, -1.95), color=GOLD, stroke_width=5)
        sl = lab("same level", 0, -2.65, 38, GOLD)
        self.play(FadeIn(sl), Create(br), run_time=0.4)
        self.at("then map")
        # the later section
        hd = lab("a later section", 0, 3.3, 36, GREY)
        panel = RoundedRectangle(corner_radius=0.3, width=12.4, height=5.7, stroke_color=GREY, stroke_width=3,
                                 fill_color=GREY, fill_opacity=0.08).move_to(P(0, -0.35))
        stube = Circle(0.95, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.25).move_to(P(-4.0, 1.3))
        stl = lab("neural tube", -4.0, 0.0, 32, GREY)
        gang = ganglion(2.4, -1.3, 4.2, 2.6)
        gl = lab("ganglion", 2.4, 0.55, 38, TEAL)
        sec = VGroup(hd, panel, stube, stl, gang, gl)
        self.play(FadeOut(VGroup(left, right, seg, cl, sl, br)), FadeIn(sec), run_time=0.6)
        self.at("quail cells")
        pos = [(-0.7, 0.4), (0.0, 0.55), (0.7, 0.4), (-0.35, -0.2), (0.35, -0.2), (0.0, -0.8), (-0.9, -0.65),
               (0.9, -0.65)]
        cells = VGroup(*[donor(0.28, 2.4 + x, -1.3 + y * 0.8) for x, y in pos])
        qlab = lab("quail cells", -1.1, -1.3, 36, YELLOW)
        ql2 = Arrow(P(0.2, -1.3), P(1.25, -1.3), buff=0, color=YELLOW, stroke_width=4, tip_length=0.22)
        self.play(LaggedStart(*[FadeIn(c, scale=0.4) for c in cells], lag_ratio=0.08), FadeIn(qlab), GrowArrow(ql2),
                  run_time=0.9)
        self.finish()


def braid_curves(state, y0=-1.7, A=1.55, x0=-4.3, x1=4.8, n=90):
    xs = np.linspace(x0, x1, n)
    pts_o, pts_r = [], []
    for x in xs:
        if state == "braid":
            c = np.cos(4 * np.pi * (x - x0) / (x1 - x0))
            yo, yr = y0 + A * c, y0 - A * c
        else:
            yo, yr = y0 + A, y0 - A
        pts_o.append(P(x, yo))
        pts_r.append(P(x, yr))
    co = VMobject(color=YELLOW, stroke_width=8).set_points_smoothly(pts_o)
    cr = VMobject(color=GREEN, stroke_width=8).set_points_smoothly(pts_r)
    return co, cr


def tip(p, color):
    t = Triangle(color=color, fill_opacity=1, stroke_width=0).scale(0.22).rotate(-PI / 2)
    t.move_to(p + RIGHT * 0.14)
    return t


class S09Why(SpokenScene):
    def construct(self):
        ty = 1.5
        left, right = chick_tube(-6.7, -3.6, ty, 1.2), chick_tube(-1.6, 6.7, ty, 1.2)
        seg = quail_segment(-2.6, ty, 2.0, 1.2)
        gap_mark = DashedVMobject(Rectangle(width=2.0, height=1.2, color=GREY, stroke_width=2).move_to(P(-2.6, ty)),
                                  num_dashes=24)
        self.play(FadeIn(left), FadeIn(right), FadeIn(seg), run_time=0.5)
        why = qmark(0, -1.7, 130, 1.0)
        self.at("cannot say why")
        self.play(FadeIn(why, scale=0.6), run_time=0.6)
        self.at("origin and")
        co, cr = braid_curves("sep")
        t1, t2 = tip(co.get_end(), YELLOW), tip(cr.get_end(), GREEN)
        ol = lab("origin", -5.55, -1.7 + 1.55, 36, YELLOW)
        rl = lab("route", -5.55, -1.7 - 1.55, 36, GREEN)
        self.play(FadeOut(why), Create(co), Create(cr), FadeIn(ol), FadeIn(rl), run_time=0.8)
        self.play(FadeIn(t1), FadeIn(t2), run_time=0.2)
        self.at("tangled")
        bo, br = braid_curves("braid")
        self.play(Transform(co, bo), Transform(cr, br), run_time=1.3)
        self.at("separate them")
        so, sr = braid_curves("sep")
        self.add(gap_mark)
        arm1 = Line(P(-3.1, ty + 0.75), P(-2.6, ty + 1.45), color=TEXT, stroke_width=7)
        arm2 = Line(P(-2.1, ty + 0.75), P(-2.6, ty + 1.45), color=TEXT, stroke_width=7)
        han = Line(P(-2.6, ty + 1.45), P(-2.6, ty + 1.85), color=TEXT, stroke_width=7)
        hand = VGroup(arm1, arm2, han)
        self.play(Transform(co, so), Transform(cr, sr), FadeIn(hand), run_time=0.8)
        self.at("move the")
        grab = VGroup(seg, hand)
        self.play(grab.animate.shift(UP * 0.55), run_time=0.3)
        self.play(grab.animate.shift(RIGHT * 5.6), run_time=0.7)
        self.finish()


class S10Pred1(SpokenScene):
    def construct(self):
        emb = embryo_body()
        pred = chip("Predict", GOLD, 32).move_to(P(COL_X, 3.3))
        self.play(FadeIn(emb), FadeIn(pred), run_time=0.6)
        self.at("take trunk crest")
        cells = cells_at(ADR_Y)
        tl = trunk_label()
        self.play(FadeIn(cells, scale=0.6), FadeIn(tl), run_time=0.6)
        self.at("adrenal level")
        adr = adr_level()
        self.play(FadeIn(adr), run_time=0.5)
        self.at("at home")
        hl, hc1, hc2 = pred1_home()
        self.play(FadeIn(hl), run_time=0.5)
        self.at("noradrenaline")
        self.play(FadeIn(hc1, shift=UP * 0.1), run_time=0.5)
        self.at("adrenaline")
        self.play(FadeIn(hc2, shift=UP * 0.1), run_time=0.5)
        neck = neck_level()
        self.at("move it")
        self.play(FadeIn(neck), run_time=0.5)
        self.at("into the neck")
        arr = move_arrow(ADR_Y + 0.2, NECK_Y - 0.2)
        self.play(GrowArrow(arr), cells.animate.move_to(P(EMB_X, NECK_Y)), run_time=1.0)
        self.at("where will it go")
        q1, q2 = pred1_questions()
        self.play(FadeIn(q1, shift=UP * 0.1), run_time=0.5)
        self.at("what transmitter")
        self.play(FadeIn(q2, shift=UP * 0.1), run_time=0.5)
        self.finish()


class S11Pause(NarratedScene):
    def construct(self):
        st = pred1_final()
        self.add(*st.values())
        self.play(Succession(Indicate(st["q1"], scale_factor=1.1, color=GOLD, run_time=1.2),
                             Indicate(st["q2"], scale_factor=1.1, color=GOLD, run_time=1.2),
                             Indicate(st["q1"], scale_factor=1.1, color=GOLD, run_time=1.2),
                             Indicate(st["q2"], scale_factor=1.1, color=GOLD, run_time=1.2)))
        self.finish()


def stream(cells, p, run_time, lag=0.15):
    start = p.point_from_proportion(0)
    anims = []
    for c in cells:
        o = c.get_center() - start
        anims.append(UpdateFromAlphaFunc(
            c, lambda m, a, o=o: m.move_to(p.point_from_proportion(a) + o * (1 - a)), run_time=run_time))
    return LaggedStart(*anims, lag_ratio=lag)


class S12Rev1(SpokenScene):
    def construct(self):
        tc = (-4.9, 2.3)
        tube = Circle(1.15, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.2).move_to(P(*tc))
        tl = lab_l("neural tube", -3.4, 3.2, 32, GREY)
        dl = lab_l("quail donor", -3.4, 2.15, 32, YELLOW)
        ring = gut_ring()
        rl, _ = ring_labels()
        pos = [(-0.45, 0.4), (0.15, 0.5), (0.55, 0.05), (-0.55, -0.2), (0.0, -0.1), (0.3, -0.55)]
        cells = VGroup(*[donor(0.24, tc[0] + x, tc[1] + y) for x, y in pos])
        route = path((-4.9, 1.1), (-4.4, -0.2), (-2.6, -1.0), (0.0, -1.1))
        dash = DashedVMobject(route, num_dashes=24).set_color(GREEN)
        rtl = lab("neck crest route", -3.3, -2.0, 34, GREEN)
        self.play(FadeIn(tube), FadeIn(tl), FadeIn(dl), FadeIn(ring), FadeIn(rl), FadeIn(cells), Create(dash),
                  FadeIn(rtl), run_time=0.6)
        self.play(stream(list(cells), route, 1.4, 0.1), run_time=1.4)
        self.at("into the gut")
        spread = [(RING_C[0] + GANG_R * np.cos(np.radians(a)), RING_C[1] + GANG_R * np.sin(np.radians(a)))
                  for a in np.linspace(205, 120, 6)]
        self.play(*[c.animate.move_to(P(x, y)) for c, (x, y) in zip(cells, spread)], run_time=0.8)
        self.at("form enteric")
        gl = [ganglion(x, y) for (x, y) in GANG_POS]
        finals = ring_cells_final()
        _, ga = ring_labels()
        self.play(*[GrowFromCenter(g) for g in gl],
                  *[c.animate.move_to(f.get_center()) for c, f in zip(cells, finals)],
                  FadeIn(ga), run_time=0.8)
        self.finish()


class S13Rev2(SpokenScene):
    def construct(self):
        ring, gl, cs, ring_lab, gang_lab = rev2_scene(lit=False)
        self.add(ring, *gl, *cs, ring_lab, gang_lab)
        l1, l2, hl, hc1, hc2, pr = rev2_left(1)
        self.play(FadeIn(l1), run_time=0.4)
        self.at("cholinergic")
        lit = [cs[i] for i in LIT]
        self.play(*[c[0].animate.set_fill(GREEN, 0.95).set_stroke(GREEN) for c in lit],
                  *[Flash(c, color=GREEN, flash_radius=0.45, line_length=0.12) for c in lit], run_time=0.7)
        self.at("use acetylcholine")
        self.play(FadeIn(l2, shift=UP * 0.1), run_time=0.6)
        self.at("changed", lead=-0.15)
        self.play(FadeIn(hl), FadeIn(hc1), FadeIn(hc2), run_time=0.2)
        self.at("what the population", lead=0)
        self.add(pr)
        self.finish()


class S13bBeat(NarratedScene):
    def construct(self):
        ring, gl, cs, ring_lab, gang_lab = rev2_scene(lit=True)
        l1, l2, hl, hc1, hc2, pr = rev2_left(3)
        self.add(ring, *gl, *cs, ring_lab, gang_lab, l1, l2, hl, hc1, hc2, pr)
        self.finish()


class S14Reverse(SpokenScene):
    def construct(self):
        SH = 3.2   # the embryo starts in the middle of the frame and slides left when the targets come in
        emb = embryo_body().shift(RIGHT * SH)
        neck = neck_level().shift(RIGHT * SH)
        adr = adr_level().shift(RIGHT * SH)
        cells = cells_at(NECK_Y, r=0.30, dxs=(-0.95, 0, 0.95)).shift(RIGHT * SH)
        vl = T("vagal\ncrest", 32, YELLOW)
        vl.move_to(P(EMB_X + SH - 2.95, NECK_Y))
        vl.add_updater(lambda m: m.move_to(P(cells.get_center()[0] - 2.95, cells.get_center()[1])))
        self.play(FadeIn(emb), FadeIn(neck), FadeIn(adr), FadeIn(cells), FadeIn(vl), run_time=0.6)
        self.at("other way")
        arr = move_arrow(NECK_Y - 0.2, ADR_Y + 0.2).shift(RIGHT * SH)
        self.play(GrowArrow(arr), run_time=0.5)
        self.at("neck crest placed")
        self.play(cells.animate.move_to(P(EMB_X + SH, ADR_Y)), run_time=1.0)
        self.at("adrenal level")
        self.play(adr.animate.set_color(GOLD), run_time=0.5)
        self.at("adrenal medulla")
        gland = Ellipse(width=4.8, height=2.8, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                        fill_opacity=0.12).move_to(P(4.4, 1.5))
        medulla = Ellipse(width=3.0, height=1.7, stroke_color=GREY, stroke_width=2, fill_color=GREY,
                          fill_opacity=0.22).move_to(P(4.4, 1.5))
        gl = lab("adrenal medulla", 4.4, 3.35, 34, TEXT)
        sg = ganglion(4.4, -1.5, 4.8, 1.7)
        sl = lab("sympathetic ganglion", 4.4, -3.0, 34, TEAL)
        # Both destinations are fully visible before their spoken names.
        self.add(gland, medulla, gl, sg, sl)
        self.play(VGroup(emb, neck, adr, cells, arr).animate.shift(LEFT * SH), run_time=0.5)
        mcells = VGroup(*[donor(0.26, 4.4 + dx, 1.5 + dy) for dx, dy in
                          ((-0.9, 0.0), (0.0, 0.35), (0.9, 0.0), (-0.45, -0.35), (0.45, -0.35))])
        self.play(*[GrowFromCenter(m) for m in mcells], run_time=0.6)
        self.at("sympathetic derivatives")
        sgc = VGroup(*[donor(0.28, 4.4 + dx, -1.5) for dx in (-1.5, -0.5, 0.5, 1.5)])
        self.play(*[GrowFromCenter(m) for m in sgc], run_time=0.7)
        self.finish()


def panel_titles():
    tl = lab("early trunk-to-head graft", PAN_LX, 3.25, 32, YELLOW)
    tr = lab("trunk crest in head tissue", PAN_RX, 3.25, 32, YELLOW)
    return tl, tr


class S15Skel(SpokenScene):
    def construct(self):
        pl, pr = head_panel(PAN_LX), head_panel(PAN_RX)
        tl, tr = panel_titles()
        cl = lab("cartilage: mostly unlabelled", PAN_LX, -3.45, 32, TEXT)
        cr = lab("head tissue: context matters", PAN_RX, -3.45, 30, TEXT)
        donors = head_donors(PAN_LX, PAN_CY, "early")
        # Show actual donors and complete captions from the opening frame.
        self.add(pl, pr, tl, tr, cl, cr, donors)
        self.at("skeleton")
        self.play(*[Indicate(c, color=TEXT, scale_factor=1.15) for c in (pl[4], pl[5], pr[4], pr[5])],
                  run_time=0.8)
        self.at("trunk crest")
        self.play(Indicate(donors, color=YELLOW, scale_factor=1.08), run_time=0.7)
        self.at("little or no")
        self.play(Indicate(cl, color=TEXT, scale_factor=1.05), run_time=0.6)
        self.finish()


class S16Rule(SpokenScene):
    def construct(self):
        pl, pr = head_panel(PAN_LX), head_panel(PAN_RX)
        tl, tr = panel_titles()
        dl = head_donors(PAN_LX, PAN_CY, "early")
        cl = lab("cartilage: mostly unlabelled", PAN_LX, -3.45, 32, TEXT)
        cr = lab("head tissue: context matters", PAN_RX, -3.45, 30, TEXT)
        old = VGroup(pl, pr, tl, tr, dl, cl, cr)
        self.add(old)
        self.at("can make cartilage")
        rd = head_donors(PAN_RX, PAN_CY, "labelled")
        rc = lab("some cartilage labelled", PAN_RX, -3.45, 32, TEXT)
        self.remove(cr)
        self.add(rd, rc)
        self.play(Indicate(rd, color=YELLOW, scale_factor=1.08), run_time=0.7)
        self.at("so the start")
        r1 = T("the start biases the options", 56, YELLOW, font=TITLE_FONT).move_to(P(0, 0.9))
        self.play(FadeOut(VGroup(old, rd, rc)), FadeIn(r1, shift=UP * 0.12), run_time=0.7)
        self.at("and the surroundings")
        r2 = T("the surroundings help choose", 56, GREEN, font=TITLE_FONT).move_to(P(0, -0.9))
        self.play(FadeIn(r2, shift=UP * 0.12), run_time=0.7)
        self.finish()


class S17Pred3(SpokenScene):
    def construct(self):
        pred = chip("Predict", GOLD, 34).move_to(P(*HDR))
        self.play(FadeIn(pred), run_time=0.4)
        dish = dish_shape()
        dl = lab("dish", DISH[0], 3.4, 40, GREY)
        one = crest(0.38, 0.95).move_to(P(*DISH))
        self.at("one cell")
        self.play(FadeIn(one, scale=0.6), run_time=0.4)
        self.at("in a dish")
        self.play(FadeIn(dish), FadeIn(dl), run_time=0.5)
        ns, ps = colony()
        cn, cp = dish_chips()
        self.at("makes neurons")
        self.play(LaggedStart(*[GrowFromPoint(c, P(*DISH)) for c in ns], lag_ratio=0.12), FadeOut(one),
                  FadeIn(cn), run_time=0.8)
        self.at("and pigment cells")
        self.play(LaggedStart(*[GrowFromPoint(c, P(*DISH)) for c in ps], lag_ratio=0.15), FadeIn(cp), run_time=0.7)
        self.at("in the embryo")
        emb = embryo2()
        el = lab("embryo", EMB2[0], -3.5, 36, GREY)
        self.play(FadeIn(emb), FadeIn(el), FadeIn(embryo_founder(), scale=0.6), FadeIn(embryo_q()), run_time=0.7)
        self.finish()


class S18Pause(NarratedScene):
    def construct(self):
        st = pred3_state()
        add_pred3(self, st)
        q = st["q"]
        self.play(Succession(*[Indicate(q, scale_factor=1.25, color=GOLD, run_time=1.25) for _ in range(4)]))
        self.finish()


class S19Rev3(SpokenScene):
    def construct(self):
        st = pred3_state()
        add_pred3(self, st)
        nn = T("Not\nnecessarily.", 44, GOLD, font=TITLE_FONT).move_to(P(HDR[0], 0.4))
        self.play(FadeOut(st["pred"]), FadeIn(nn), run_time=0.5)
        self.at("dish shows")
        self.play(Transform(st["dl"], lab("dish: can make", DISH[0], 3.4, 40, TEXT)),
                  st["dish"].animate.set_stroke(TEXT), run_time=0.7)
        self.at("tracing")
        founder = st["founder"]
        pts = [(3.55, 1.95), (4.95, 1.4), (3.65, -0.3), (4.75, -1.5)]
        kids = VGroup(*[donor(0.3, EMB2[0], 0.9) for _ in pts])
        self.play(FadeOut(st["q"]), FadeOut(founder), FadeIn(kids), run_time=0.4)
        self.play(*[k.animate.move_to(P(x, y)) for k, (x, y) in zip(kids, pts)], run_time=1.2)
        self.at("did make")
        self.play(Transform(st["el"], lab("embryo: did make", EMB2[0], -3.5, 38, TEXT)),
                  *[Flash(k, color=BLUE, flash_radius=0.5, line_length=0.12) for k in kids], run_time=0.8)
        self.finish()


class S201988(SpokenScene):
    def construct(self):
        yr = T("1988", 48, GOLD, font=TITLE_FONT).move_to(P(0, 3.4))
        py, ph = -0.45, 5.7
        pc = RoundedRectangle(corner_radius=0.3, width=5.9, height=ph, stroke_color=GREY, stroke_width=3,
                              fill_color=GREY, fill_opacity=0.08).move_to(P(-3.85, py))
        pe = RoundedRectangle(corner_radius=0.3, width=6.8, height=ph, stroke_color=GREY, stroke_width=3,
                              fill_color=GREY, fill_opacity=0.08).move_to(P(3.4, py))
        hc = lab("quail cranial crest, 1988", -3.85, 2.6, 30, TEXT)
        he = lab("chick trunk, dye-filled clone, 1988", 3.4, 2.6, 30, TEXT)
        self.add(yr, pc, pe, hc, he)
        self.at("both methods")
        w1 = Circle(1.15, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.1).move_to(P(-5.5, 1.0))
        w2 = Circle(1.15, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.1).move_to(P(-5.5, -1.35))
        body = RoundedRectangle(corner_radius=0.7, width=2.1, height=4.2, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.15).move_to(P(1.3, -1.15))
        head = Circle(0.6, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.15).move_to(P(1.3, 1.45))
        ntube = RoundedRectangle(corner_radius=0.2, width=0.4, height=3.6, stroke_color=GREY, stroke_width=2,
                                 fill_color=GREY, fill_opacity=0.3).move_to(P(1.3, -0.85))
        self.play(FadeIn(w1), FadeIn(w2), FadeIn(head), FadeIn(body), FadeIn(ntube), run_time=0.8)
        self.at("single cells")
        offs = [(-0.45, 0.4), (0.4, 0.45), (0.0, -0.05), (-0.45, -0.45), (0.45, -0.4)]
        mix = VGroup(*[plain_cell(0.26, c, 0.85, -5.5 + x, 1.0 + y)
                       for (x, y), c in zip(offs, [TEAL, TEXT, TEAL, TEXT, TEAL])])
        single = VGroup(*[plain_cell(0.26, TEAL, 0.85, -5.5 + x, -1.35 + y) for x, y in offs])
        ml = lab("mixed\nclone", -3.0, 1.0, 32, TEXT)
        sl = lab("single-type\nclone", -3.0, -1.35, 32, TEXT)
        clone = VGroup(*[crest(0.22, 0.95, BLUE).move_to(P(1.3 + dx, -0.5 + dy))
                         for dx, dy in ((-0.45, 0.7), (0.4, 0.75), (0.0, 0.1), (-0.4, -0.55), (0.4, -0.6))])
        leg_n = VGroup(Dot(P(-6.35, -2.95), radius=0.14, color=TEAL), lab_l("neurons", -6.1, -2.95, 28, TEAL))
        leg_p = VGroup(Dot(P(-4.2, -2.95), radius=0.14, color=TEXT), lab_l("pigment cells", -3.95, -2.95, 28, TEXT))
        self.play(FadeIn(mix, scale=0.5), FadeIn(single, scale=0.5), FadeIn(ml), FadeIn(sl), FadeIn(clone, scale=0.5),
                  FadeIn(leg_n), FadeIn(leg_p), run_time=1.0)
        self.at("several types")
        hd2 = lab("possible clone outcomes", 4.7, 1.8, 26, GOLD)
        chips = VGroup()
        arrows = VGroup()
        for txt, col, y in (("neurons", TEAL, 0.7), ("pigment cells", TEXT, -0.6),
                            ("stay in tube", GREY, -1.9)):
            c = chip(txt, col, 28)
            c.move_to(P(5.0, y))
            chips.add(c)
            arrows.add(Arrow(P(2.05, -0.45), c.get_left() + LEFT * 0.04, buff=0.04, color=GOLD, stroke_width=3,
                             tip_length=0.2))
        self.play(FadeIn(hd2), LaggedStart(*[AnimationGroup(GrowArrow(a), FadeIn(c)) for a, c in zip(arrows, chips)],
                                         lag_ratio=0.2), run_time=1.2)
        self.at("whether the typical")
        db = lab("typical cell?", 0, -3.6, 36, GOLD)
        self.play(FadeIn(db, shift=UP * 0.1), run_time=0.5)
        self.at("still debated")
        self.play(Transform(db, lab("typical cell: still debated", 0, -3.6, 36, GOLD)), run_time=0.6)
        # Hold the complete result through the last spoken word; cut to the takeaway.
        self.wait(max(0.1, self.narration_s + 0.1 - self.elapsed()))


class S21Take(SpokenScene):
    def construct(self):
        t = lab("The takeaway", 0, 0, 36, GOLD)
        self.add(t)
        self.at("move the cells")
        l1 = T("Move the cells, and the pattern appears.", 52, font=TITLE_FONT).move_to(P(0, -0.55))
        fit(l1, max_w=12.4)
        self.play(t.animate.move_to(P(0, 0.65)), FadeIn(l1, shift=UP * 0.15), run_time=0.7)
        self.at("the start biases")
        l2 = T("The start biases the options,", 52, YELLOW, font=TITLE_FONT).move_to(P(0, -1.25))
        fit(l2, max_w=12.4)
        self.play(t.animate.move_to(P(0, 1.3)), l1.animate.move_to(P(0, 0)),
                  FadeIn(l2, shift=UP * 0.15), run_time=0.6)
        self.at("and the journey")
        l3 = T("and the journey helps choose.", 52, GREEN, font=TITLE_FONT).move_to(P(0, -1.75))
        fit(l3, max_w=12.4)
        self.play(t.animate.move_to(P(0, 2.15)), l1.animate.move_to(P(0, 0.85)),
                  l2.animate.move_to(P(0, -0.55)), FadeIn(l3, shift=UP * 0.15), run_time=0.6)
        self.finish()


class S22End(EndCard):
    LINE = "The start biases the options, and the journey helps choose."

    def construct(self):
        line = T("The start biases the options,\nand the journey helps choose.", 52, font=TITLE_FONT)
        fit(line, max_w=12.2)
        sub = T("biochemistrypedia.com", 30, color=TEAL)
        g = VGroup(line, sub).arrange(DOWN, buff=0.6)
        self.play(FadeIn(line, shift=UP * 0.15), run_time=self.beat(0.3))
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        self.finish()
