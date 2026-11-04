"""Ventral to Dorsal: Sonic Hedgehog and BMP in the Neural Tube, chapter 2: Naming the Signal

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, shared by every chapter of this lesson; from scenes.old.py)
  YELLOW = Sonic hedgehog (Shh) and the signaling it causes
  TEAL   = notochord and floor plate (the source tissue), and floor-plate markers
  BLUE   = motor neurons (the pMN domain) and their markers (deeper blue "#5C8DF0", distinct from TEAL)
  ORANGE = ventral interneuron classes (the p3 side of the map)
  RED    = repression (T-bars, Gli repressor) and nothing else
  PURPLE = Patched
  GREEN  = "on": active Smoothened, Gli activator
  PINK   = Gli proteins (full length)
  GREY   = tube wall, neutral cells, axes, "off"
  GOLD   = the one highlight (puzzle boxes, "predict", credits cards)
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

BLUE = "#5C8DF0"   # a deeper blue than the house BLUE, so motor neurons never read as the teal floor plate
ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
PINK = "#E58AC8"
PLANT = "#7FA06A"


# ---------------------------------------------------------------------------------------------
# small helpers
def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def inhib(a, b, color=RED, w=5):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    b = b - d * 0.04
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w), Line(b + perp * 0.22, b - perp * 0.22, color=color, stroke_width=w + 1))


def xmark(box, color=TEXT, w=8, inset=0.12):
    l, r, t, b = box.get_left()[0] + inset, box.get_right()[0] - inset, box.get_top()[1] - inset, box.get_bottom()[1] + inset
    return VGroup(Line([l, t, 0], [r, b, 0], color=color, stroke_width=w), Line([l, b, 0], [r, t, 0], color=color, stroke_width=w))


def gene_box(label, color, w=2.6, h=1.1, size=40, x=0, y=0):
    box = RoundedRectangle(corner_radius=0.14, width=w, height=h, stroke_color=color, stroke_width=3,
                           fill_color=color, fill_opacity=0.16).move_to([x, y, 0])
    return VGroup(box, T(label, size, color, weight=BOLD).move_to(box))


# ---------------------------------------------------------------------------------------------
# the neural tube map (cross-section, dorsal up), shared with every chapter
DOM_COLOR = {"p3": ORANGE, "pMN": BLUE, "p2": ORANGE, "p1": ORANGE, "p0": ORANGE}


class Tube:
    def __init__(self, cx=0.0, cy=0.0, W=4.8, H=4.8, N=24, cr=0.15, rings=(0.55, 0.78), nr=0.38):
        self.cx, self.cy, self.W, self.H, self.nr = cx, cy, W, H, nr
        self.outer = Ellipse(width=W, height=H, stroke_color=GREY, stroke_width=5, fill_color=GREY, fill_opacity=0.07).move_to([cx, cy, 0])
        self.canal = Ellipse(width=0.34 * W, height=0.34 * H, stroke_color=GREY, stroke_width=2.5,
                             fill_color=BG, fill_opacity=1).move_to([cx, cy, 0])
        self.cells, self.info = VGroup(), []
        for i in range(N):
            th = -PI / 2 + (i + 0.5) * 2 * PI / N
            m = -np.sin(th)
            if m <= 0:
                dom = "dorsal"
            elif m > 0.96:
                dom = "p3"
            elif m > 0.7:
                dom = "pMN"
            elif m > 0.5:
                dom = "p2"
            elif m > 0.25:
                dom = "p1"
            else:
                dom = "p0"
            for rho in rings:
                c = Circle(radius=cr, stroke_color=GREY, stroke_width=1.5, fill_color=GREY, fill_opacity=0.3)
                c.move_to([cx + rho * W / 2 * np.cos(th), cy + rho * H / 2 * np.sin(th), 0])
                self.cells.add(c)
                self.info.append((dom, np.cos(th)))
        self.epi = ParametricFunction(lambda t: np.array([cx + (W / 2 + 0.3) * np.cos(t), cy + (H / 2 + 0.3) * np.sin(t), 0]),
                                      t_range=[PI * 0.27, PI * 0.73], stroke_color=GREY, stroke_width=5).set_stroke(opacity=0.7)
        self.roof = RoundedRectangle(corner_radius=0.06, width=0.9 * W / 4.8, height=0.2, stroke_color=TEXT, stroke_width=2.5,
                                     fill_color=TEXT, fill_opacity=0.35).move_to([cx, cy + H / 2 - 0.17, 0])
        self.fp = RoundedRectangle(corner_radius=0.06, width=0.9 * W / 4.8, height=0.2, stroke_color=TEAL, stroke_width=3,
                                   fill_color=TEAL, fill_opacity=0.6).move_to([cx, cy - H / 2 + 0.17, 0])
        self.noto = Circle(radius=nr, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.35
                           ).move_to([cx, cy - H / 2 - 0.1 - nr, 0])

    def group(self, noto=True, epi=True):
        g = VGroup(self.outer, self.canal, self.cells, self.roof, self.fp)
        if epi:
            g.add(self.epi)
        if noto:
            g.add(self.noto)
        return g

    def sel(self, dom=None, side=None):
        """cells whose domain is in `dom` (str or list); side = +1 right, -1 left."""
        dom = [dom] if isinstance(dom, str) else dom
        out = []
        for c, (d, cs) in zip(self.cells, self.info):
            if (dom is None or d in dom) and (side is None or np.sign(cs) == side):
                out.append(c)
        return out

    def paint_normal(self):
        for c, (d, _) in zip(self.cells, self.info):
            if d in DOM_COLOR:
                c.set_stroke(DOM_COLOR[d]).set_fill(DOM_COLOR[d], 0.55)

    def paint_knockout(self):
        for c, (d, _) in zip(self.cells, self.info):
            if d == "dorsal" or d == "p0":
                continue
            c.set_stroke(GREY, opacity=0.28).set_fill(GREY, 0)

    def paint_rescue(self):
        self.paint_knockout()
        for c, (d, _) in zip(self.cells, self.info):
            if d in ("pMN", "p2", "p1", "p0"):
                col = DOM_COLOR[d]
                c.set_stroke(col, opacity=1).set_fill(col, 0.55)

    def ghost_fp(self):
        self.fp.set_stroke(GREY, width=2, opacity=0.4).set_fill(GREY, 0)


def halo(mob, color=YELLOW, extra=0.16):
    h = mob.copy().set_fill(color, 0.25).set_stroke(color, width=7, opacity=0.9)
    h.scale((mob.width + 2 * extra) / mob.width)
    return h


# ---------------------------------------------------------------------------------------------
# the four puzzles strip, carried from chapter 1
STRIP_Y = -2.95
BOX_TXT = ["1  told, then\nrecruits", "2  what is the\nsignal", "3  how is a\nslope read", "4  how does a\nslope become\nlines"]
BOX_X = [-5.1, -1.7, 1.7, 5.1]


def strip():
    boxes = VGroup()
    for x, txt in zip(BOX_X, BOX_TXT):
        rect = RoundedRectangle(corner_radius=0.12, width=3.2, height=1.6, stroke_color=GREY, stroke_width=2.5,
                                fill_color=GREY, fill_opacity=0.08).move_to([x, STRIP_Y, 0])
        lab = T(txt, 24, GREY, line_spacing=0.8).move_to(rect)
        boxes.add(VGroup(rect, lab))
    # box 1 is done in chapter 1
    boxes[0][0].set_stroke(TEAL).set_fill(TEAL, 0.14)
    boxes[0][1].set_color(TEAL)
    return boxes


def light_box(box, color=GOLD):
    return [box[0].animate.set_stroke(color, width=4).set_fill(color, 0.2), box[1].animate.set_color(TEXT)]


# ---------------------------------------------------------------------------------------------
# little animals and pages
def mouse(cx, cy, s=1.0):
    st = dict(stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.35)
    body = Ellipse(width=1.5 * s, height=0.85 * s, **st).move_to([cx, cy, 0])
    head = Ellipse(width=0.75 * s, height=0.6 * s, **st).move_to([cx - 0.85 * s, cy - 0.05 * s, 0])
    ear = Circle(radius=0.2 * s, **st).move_to([cx - 0.7 * s, cy + 0.38 * s, 0])
    nose = Dot([cx - 1.22 * s, cy - 0.08 * s, 0], radius=0.06 * s, color=TEXT)
    tail = ArcBetweenPoints([cx + 0.72 * s, cy - 0.05 * s, 0], [cx + 1.55 * s, cy + 0.4 * s, 0], angle=-1.0,
                            stroke_color=GREY, stroke_width=4)
    legs = VGroup(Line([cx - 0.3 * s, cy - 0.4 * s, 0], [cx - 0.3 * s, cy - 0.62 * s, 0], color=GREY, stroke_width=4),
                  Line([cx + 0.35 * s, cy - 0.4 * s, 0], [cx + 0.35 * s, cy - 0.62 * s, 0], color=GREY, stroke_width=4))
    return VGroup(tail, body, head, ear, nose, legs)


def zebrafish(cx, cy, s=1.0):
    st = dict(stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.35)
    body = Ellipse(width=1.8 * s, height=0.75 * s, **st).move_to([cx, cy, 0])
    tail = Polygon([cx + 0.8 * s, cy, 0], [cx + 1.35 * s, cy + 0.42 * s, 0], [cx + 1.35 * s, cy - 0.42 * s, 0], **st)
    eye = Dot([cx - 0.6 * s, cy + 0.08 * s, 0], radius=0.07 * s, color=TEXT)
    stripes = VGroup(*[Line([cx - 0.35 * s, cy + dy * s, 0], [cx + 0.75 * s, cy + dy * s, 0], color=TEXT, stroke_width=2.5, stroke_opacity=0.6)
                       for dy in (-0.16, 0.0, 0.16)])
    return VGroup(tail, body, eye, stripes)


def chick(cx, cy, s=1.0):
    st = dict(stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.35)
    body = Circle(radius=0.5 * s, **st).move_to([cx + 0.1 * s, cy - 0.05 * s, 0])
    head = Circle(radius=0.28 * s, **st).move_to([cx - 0.38 * s, cy + 0.5 * s, 0])
    beak = Polygon([cx - 0.62 * s, cy + 0.55 * s, 0], [cx - 0.9 * s, cy + 0.47 * s, 0], [cx - 0.62 * s, cy + 0.4 * s, 0],
                   stroke_color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=0.6)
    eye = Dot([cx - 0.45 * s, cy + 0.56 * s, 0], radius=0.05 * s, color=TEXT)
    legs = VGroup(Line([cx - 0.05 * s, cy - 0.55 * s, 0], [cx - 0.05 * s, cy - 0.85 * s, 0], color=GREY, stroke_width=4),
                  Line([cx + 0.3 * s, cy - 0.55 * s, 0], [cx + 0.3 * s, cy - 0.85 * s, 0], color=GREY, stroke_width=4))
    return VGroup(legs, body, head, beak, eye)


def fly(cx, cy, s=1.0):
    st = dict(stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.35)
    body = Ellipse(width=1.0 * s, height=0.4 * s, **st).move_to([cx, cy, 0])
    head = Circle(radius=0.22 * s, **st).move_to([cx - 0.6 * s, cy, 0])
    w1 = Ellipse(width=0.9 * s, height=0.32 * s, stroke_color=TEXT, stroke_width=2, fill_color=TEXT, fill_opacity=0.15
                 ).rotate(0.6).move_to([cx + 0.1 * s, cy + 0.38 * s, 0])
    w2 = Ellipse(width=0.9 * s, height=0.32 * s, stroke_color=TEXT, stroke_width=2, fill_color=TEXT, fill_opacity=0.15
                 ).rotate(-0.1).move_to([cx + 0.35 * s, cy + 0.3 * s, 0])
    legs = VGroup(*[Line([cx + dx * s, cy - 0.15 * s, 0], [cx + (dx - 0.12) * s, cy - 0.45 * s, 0], color=GREY, stroke_width=3)
                    for dx in (-0.25, 0.05, 0.3)])
    return VGroup(legs, w1, w2, body, head)


def page(cx, cy, w, h):
    r = RoundedRectangle(corner_radius=0.08, width=w, height=h, stroke_color=TEXT, stroke_width=3,
                         fill_color=TEXT, fill_opacity=0.07).move_to([cx, cy, 0])
    head = T("Cell", 28, TEXT, font=TITLE_FONT, weight=BOLD).move_to([cx, cy + h / 2 - 0.4, 0])
    n = int((h - 1.3) / 0.3)
    lines = VGroup(*[Line([cx - w / 2 + 0.3, cy + h / 2 - 0.95 - 0.3 * k, 0],
                          [cx + w / 2 - 0.3 - (0.4 if k % 3 == 2 else 0), cy + h / 2 - 0.95 - 0.3 * k, 0],
                          color=GREY, stroke_width=3, stroke_opacity=0.7) for k in range(n)])
    return VGroup(r, head, lines)


# ---------------------------------------------------------------------------------------------
EXPL_OFFS = [(-0.3, 0.3), (0.0, 0.3), (0.3, 0.3), (-0.3, 0.0), (0.0, 0.0), (0.3, 0.0), (-0.3, -0.3), (0.0, -0.3), (0.3, -0.3)]


# ---------------------------------------------------------------------------------------------
# small layout helpers used by the fix round
def left_at(mob, x, y):
    """put a mobject with its LEFT edge at x and centre at y."""
    mob.move_to([x + mob.width / 2, y, 0])
    return mob


def leader(a, b, color=GREY, w=2.5):
    return Line([a[0], a[1], 0], [b[0], b[1], 0], color=color, stroke_width=w)


def legend_rows(items, x, y, size=26, gap=0.55):
    rows = []
    for i, (c, t) in enumerate(items):
        sw = RoundedRectangle(corner_radius=0.05, width=0.34, height=0.34, stroke_color=c, stroke_width=2,
                              fill_color=c, fill_opacity=0.6)
        tx = T(t, size, c, weight=BOLD)
        tx.next_to(sw, RIGHT, buff=0.2)
        row = VGroup(sw, tx)
        row.move_to([x + row.width / 2, y - i * gap, 0])
        rows.append(row)
    return rows


LEG_FP = (TEAL, "floor plate")
LEG_MN = (BLUE, "motor neurons")
LEG_IN = (ORANGE, "ventral interneurons")


# ---------------------------------------------------------------------------------------------
# dishes and explants
DISH_W, DISH_H = 6.2, 3.8
DISH_Y = -0.05
DX = (-3.5, 3.5)


def expl_y(cy, h):
    return cy - h / 2 + 0.75


EXPL_Y = expl_y(DISH_Y, DISH_H)
EXPL_PITCH, EXPL_SIDE = 0.39, 0.36


def explant(cx, cy, color=GREY, o=0.35):
    """nine neutral grey squares: the one explant shape used from the cut in the plate to the last dish."""
    return VGroup(*[Square(side_length=EXPL_SIDE, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=o
                           ).move_to([cx + (dx / 0.3) * EXPL_PITCH, cy + (dy / 0.3) * EXPL_PITCH, 0]) for dx, dy in EXPL_OFFS])


def dish(cx, cy, w=DISH_W, h=DISH_H):
    L, R, top, bot = cx - w / 2, cx + w / 2, cy + h / 2, cy - h / 2
    shell = VMobject(stroke_color=TEXT, stroke_width=4).set_points_as_corners([[L, top, 0], [L + 0.3, bot, 0], [R - 0.3, bot, 0], [R, top, 0]])
    lev = top - 0.3
    xl = lambda y: L + 0.3 * (top - y) / h
    xr = lambda y: R - 0.3 * (top - y) / h
    liquid = Polygon([xl(lev), lev, 0], [xl(bot), bot, 0], [xr(bot), bot, 0], [xr(lev), lev, 0],
                     stroke_width=0, fill_color=TEXT, fill_opacity=0.1)
    return VGroup(liquid, shell)


def protein_dots(cx, cy, n, w=DISH_W, h=DISH_H, seed=1, r=0.1):
    rs = np.random.RandomState(seed)
    out, tries = [], 0
    top, bot, ey = cy + h / 2 - 0.6, cy - h / 2 + 0.3, expl_y(cy, h)
    while len(out) < n and tries < 3000:
        tries += 1
        x = cx + rs.uniform(-w / 2 + 0.8, w / 2 - 0.8)
        y = rs.uniform(bot, top)
        if abs(x - cx) < 1.0 and abs(y - ey) < 0.9:
            continue
        if any((x - a) ** 2 + (y - b) ** 2 < 0.3 for a, b in out):
            continue
        out.append((x, y))
    return VGroup(*[Circle(radius=r, stroke_width=0, fill_color=YELLOW, fill_opacity=0.95).move_to([x, y, 0]) for x, y in out])


# ---------------------------------------------------------------------------------------------
# the brake membrane (shared by s10, s11, s12, s17)
MEM_Y = -0.1
PX, SX = -3.2, 3.2
BW, BHT = 2.8, 4.4
LAB_Y, STATE_Y, ARM_Y = 1.3, -1.35, 1.0


def membrane():
    return Rectangle(width=9.2, height=1.1, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.3).move_to([0, MEM_Y, 0])


def block(x, color, o=0.4):
    return RoundedRectangle(corner_radius=0.2, width=BW, height=BHT, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=o
                            ).move_to([x, MEM_Y, 0])


def brake_scene(on=False):
    d = {}
    d["mem"] = membrane()
    d["p"] = block(PX, PURPLE, 0.4)
    d["s"] = block(SX, GREEN if on else GREY, 0.6 if on else 0.3)
    d["plab"] = T("Patched", 28, PURPLE, weight=BOLD).move_to([PX, LAB_Y, 0])
    d["slab"] = T("Smoothened", 28, TEXT, weight=BOLD).move_to([SX, LAB_Y, 0])
    d["state"] = T("on" if on else "off", 36, GREEN if on else GREY, weight=BOLD).move_to([SX, STATE_Y, 0])
    d["tbar"] = inhib([PX + BW / 2 + 0.1, ARM_Y, 0], [SX - BW / 2 - 0.1, ARM_Y, 0])
    d["shh"] = chip("Sonic hedgehog", YELLOW, 30).move_to([PX, 2.4, 0])
    d["analogy"] = T("an analogy, not physical contact", 26, GREY).move_to([0, -3.2, 0])
    return d


def brake_arm():
    """the brake as a lever from Patched pressing a pad on Smoothened."""
    arm = Line([PX + BW / 2, ARM_Y, 0], [SX - BW / 2 - 0.3, ARM_Y, 0], color=TEXT, stroke_width=8)
    pad = RoundedRectangle(corner_radius=0.08, width=0.3, height=1.2, stroke_color=RED, stroke_width=3,
                           fill_color=RED, fill_opacity=0.75).move_to([SX - BW / 2 - 0.15, ARM_Y, 0])
    return VGroup(arm, pad)


# ---------------------------------------------------------------------------------------------
# the cell for the Gli scenes
CELL_C = np.array([0.0, -0.9, 0.0])
BASE = np.array([0.0, 1.65, 0.0])
BAR_ROWS = [1.0, 0.1, -0.8]
LW, RW, BH = 1.2, 1.8, 0.55
NUC = np.array([0.0, -2.3, 0.0])
GLI_LAB = np.array([3.1, 0.3, 0.0])
REP_X = [-1.5, 0.0, 1.5]


def cell_body():
    body = Ellipse(width=10.8, height=5.1, stroke_color=GREY, stroke_width=5, fill_color=GREY, fill_opacity=0.08).move_to(CELL_C)
    nuc = Ellipse(width=5.4, height=1.9, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.15).move_to(NUC)
    cil = Line(BASE, BASE + UP * 1.75, color=TEXT, stroke_width=8).set_stroke(opacity=0.85)
    tip = Dot(BASE + UP * 1.75, radius=0.1, color=TEXT)
    bb = Circle(radius=0.14, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.5).move_to(BASE)
    return VGroup(body, nuc, cil, tip, bb)


def cell_labels():
    """small labels: cell, nucleus, cilium (each with a leader)."""
    cell_l = T("cell", 26, GREY).move_to([-3.6, 0.3, 0])
    nuc_l = T("nucleus", 26, GREY).move_to([-4.3, -1.25, 0])
    nuc_ln = leader([-3.5, -1.35], [-2.15, -1.85])
    cil_l = T("cilium", 26, TEXT).move_to([1.95, 2.6, 0])
    cil_ln = leader([1.45, 2.6], [0.2, 2.55], TEXT)
    return cell_l, VGroup(nuc_l, nuc_ln), VGroup(cil_l, cil_ln)


def gli_bar(y, color=PINK, x=0.0):
    left = Rectangle(width=LW, height=BH, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.55).move_to([x - RW / 2, y, 0])
    right = Rectangle(width=RW, height=BH, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.3).move_to([x + LW / 2, y, 0])
    return VGroup(left, right)


def slash(bar):
    x = (bar[0].get_right()[0] + bar[1].get_left()[0]) / 2
    y = bar[0].get_center()[1]
    return Line([x + 0.16, y + 0.45, 0], [x - 0.16, y - 0.45, 0], color=TEXT, stroke_width=6)


def rep_piece(x):
    return Rectangle(width=LW, height=BH, stroke_color=RED, stroke_width=3, fill_color=RED, fill_opacity=0.6).move_to([x, NUC[1], 0])


class Scn(SpokenScene):
    def after(self, phrase, dt, nth=0):
        """wait until `dt` seconds after the narrator starts `phrase` (for names a transcriber may spell differently)."""
        rest = self.t_of(phrase, nth) + dt - self.elapsed()
        if rest > 0.02:
            self.wait(rest)


# =============================================================================================
class S00Title(TitleCard):
    LESSON = "Ventral to Dorsal: Sonic Hedgehog and BMP in the Neural Tube"
    TITLE = "Naming the Signal"


# ---------------------------------------------------------------------------------------------
class S01Q(Scn):
    def construct(self):
        tb = Tube(cx=0, cy=0.85, W=4.2, H=4.2, nr=0.34, cr=0.13)
        boxes = strip()
        boxes[1][0].set_stroke(GREY)
        lab_t = T("neural tube", 26, GREY).move_to([-3.6, 2.3, 0])
        lab_n = T("notochord", 26, TEAL).move_to([-3.0, -1.75, 0])
        lt = Line([-2.5, 2.3, 0], [-1.7, 2.1, 0], color=GREY, stroke_width=2)
        ln = Line([-1.85, -1.75, 0], [-0.4, -1.75, 0], color=TEAL, stroke_width=2)
        self.play(FadeIn(tb.group()), FadeIn(boxes), FadeIn(lab_t), FadeIn(lt), FadeIn(lab_n), FadeIn(ln), run_time=0.5)

        ar = arr([0, tb.noto.get_top()[1] + 0.02, 0], [0, 0.0, 0], TEXT, 7, 0.3)
        q = T("?", 56, TEXT, weight=BOLD).move_to([1.05, -1.7, 0])
        self.play(GrowArrow(ar), run_time=1.3)
        self.play(FadeIn(q, scale=0.7), run_time=0.4)

        self.at("What is it")
        what = T("what is it?", 44, TEXT).move_to([-4.6, 0.6, 0])
        self.play(FadeIn(what, shift=RIGHT * 0.2), *light_box(boxes[1]), run_time=0.7)

        self.at("how does a cell")
        target = tb.sel("p1", +1)[1]
        ring = Circle(radius=0.3, stroke_color=GOLD, stroke_width=5).move_to(target.get_center())
        rc = T("how does a cell\nreceive it?", 36, TEXT, line_spacing=0.9).move_to([4.8, 0.9, 0])
        rl = Line([ring.get_right()[0], ring.get_center()[1], 0], [3.4, 0.7, 0], color=GOLD, stroke_width=2.5)
        self.play(Create(ring), FadeIn(rc, shift=LEFT * 0.2), Create(rl), run_time=0.8)
        self.play(Indicate(target, color=GOLD, scale_factor=1.6), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
PAGE_X = [-4.2, 0.0, 4.2]
PG_Y, PG_W, PG_H = -0.1, 3.6, 4.6


class S02Cell(Scn):
    def construct(self):
        pages = [page(x, PG_Y, PG_W, PG_H) for x in PAGE_X]
        shifts = (-1, 0, 1)
        # the pages slide in at once, so the frame is never empty
        self.play(LaggedStart(*[FadeIn(p, shift=RIGHT * 3.5 * -sg) for p, sg in zip(pages, shifts)], lag_ratio=0.15), run_time=1.1)
        self.at("December")
        lab = T("Cell, December 1993", 46, TEXT, font=TITLE_FONT).move_to([0, 3.15, 0])
        self.play(FadeIn(lab, shift=DOWN * 0.15), run_time=0.7)

        self.at("Three papers")
        self.play(LaggedStart(*[Indicate(p[0], color=GOLD, scale_factor=1.04) for p in pages], lag_ratio=0.3), run_time=1.0)

        self.at("one issue")
        br = Brace(VGroup(*pages), DOWN, buff=0.12, color=GOLD)
        bl = T("one issue", 32, GOLD).next_to(br, DOWN, buff=0.1)
        self.play(GrowFromCenter(br), FadeIn(bl), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Cell2(Scn):
    def construct(self):
        pages = [page(x, PG_Y, PG_W, PG_H) for x in PAGE_X]
        lab = T("Cell, December 1993", 46, TEXT, font=TITLE_FONT).move_to([0, 3.15, 0])
        self.add(*pages, lab)

        # the pages drop and shrink to the bottom; the fly takes the middle of the frame
        small = [page(x, -2.15, 3.0, 1.9) for x in PAGE_X]
        self.play(FadeOut(lab), *[Transform(p, sm) for p, sm in zip(pages, small)], run_time=1.0)

        self.at("vertebrate")
        fl = fly(-2.3, 1.0, 3.2)
        self.play(FadeIn(fl, shift=RIGHT * 0.3), run_time=0.8)
        self.at("of hedgehog")
        hh = chip("hedgehog", YELLOW, 40).move_to([2.2, 1.3, 0])
        self.play(FadeIn(hh, shift=DOWN * 0.15), run_time=0.6)
        self.at("a fly")
        fl_l = T("a fly gene", 32, TEXT).move_to([-2.3, -0.4, 0])
        self.play(FadeIn(fl_l), run_time=0.4)
        self.at("secreted signal")
        dots = VGroup(*[Circle(radius=0.12, stroke_width=0, fill_color=YELLOW, fill_opacity=0.95).move_to([-0.9 + dx, 1.0 + dy, 0])
                        for dx, dy in [(0.0, 0.1), (0.1, -0.15), (-0.1, 0.3)]])
        self.add(dots)
        self.play(LaggedStart(*[d.animate.shift(RIGHT * (1.0 + 0.4 * i)) for i, d in enumerate(dots)], lag_ratio=0.25), run_time=1.0)

        # make room: the fly group moves to the top row, the animals fill the middle
        self.at("in mouse")
        ans = [mouse(0, 0.55, 1.5), zebrafish(0, 0.55, 1.5), chick(0, 0.7, 1.6)]
        for a, x in zip(ans, PAGE_X):
            a.move_to([x, 0.7, 0])
        nm = ["mouse", "zebrafish", "chick"]
        cr = ["McMahon", "Ingham", "Tabin"]
        self.play(FadeOut(dots), FadeOut(fl_l), fl.animate.scale(0.45).move_to([-3.4, 3.1, 0]), hh.animate.move_to([0.0, 3.1, 0]), run_time=0.5)
        for i, cue in enumerate([None, "in zebrafish", "in chick"]):
            if cue:
                self.at(cue)
            lb = T(nm[i], 32, TEXT).move_to([PAGE_X[i], min(-0.75, ans[i].get_bottom()[1] - 0.3), 0])
            cl = T(cr[i], 30, TEXT, font=TITLE_FONT, weight=BOLD).move_to([PAGE_X[i], -3.45, 0])
            self.play(FadeIn(ans[i], shift=DOWN * 0.2), FadeIn(lb), FadeIn(cl), run_time=0.45)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Expr(Scn):
    def construct(self):
        cx, cy, W = -3.4, 0.6, 5.0
        tb = Tube(cx=cx, cy=cy, W=W, H=W, nr=0.38)
        self.play(FadeIn(tb.group()), run_time=0.8)
        self.at("sonic hedgehog")
        shh = chip("Sonic hedgehog (Shh)", YELLOW, 30).move_to([cx, -3.3, 0])
        self.play(FadeIn(shh, shift=UP * 0.15), run_time=0.6)

        X0 = -0.6
        # once, here: the anatomy that later chapters rely on
        self.at("expressed")
        epi_pt = [cx + (W / 2 + 0.3) * np.cos(PI * 0.32), cy + (W / 2 + 0.3) * np.sin(PI * 0.32)]
        roof_pt = [tb.roof.get_right()[0], tb.roof.get_center()[1]]
        vz_pt = [cx + 0.55 * (W / 2) * np.cos(0.7), cy + 0.55 * (W / 2) * np.sin(0.7)]
        can_pt = [cx + 0.17 * W, cy + 0.05]
        anat = []
        for text, y, pt in [("roof plate", 3.3, roof_pt), ("epidermis", 2.6, epi_pt), ("ventricular zone", 1.75, vz_pt), ("central canal", 0.55, can_pt)]:
            t = left_at(T(text, 26, GREY), X0, y)
            ln = leader([X0 - 0.1, y], pt)
            anat.append(VGroup(t, ln))
        self.play(LaggedStart(*[FadeIn(a) for a in anat], lag_ratio=0.25), run_time=1.0)

        self.at("notochord")
        h1 = halo(tb.noto)
        l1 = left_at(T("notochord", 26, TEAL), X0, -2.2)
        ln1 = leader([X0 - 0.1, -2.2], [tb.noto.get_right()[0] + 0.15, tb.noto.get_center()[1]], TEAL)
        ar = arr([cx, -3.0, 0], [cx, tb.noto.get_bottom()[1] - 0.12, 0], YELLOW, 6, 0.25)
        self.play(FadeIn(h1), FadeIn(l1), Create(ln1), GrowArrow(ar), run_time=0.8)
        self.at("floor plate")
        h2 = halo(tb.fp, extra=0.1)
        l2 = left_at(T("floor plate", 26, TEAL), X0, -1.2)
        ln2 = leader([X0 - 0.1, -1.2], [tb.fp.get_right()[0] + 0.1, tb.fp.get_center()[1]], TEAL)
        self.play(FadeIn(h2), FadeIn(l2), Create(ln2), run_time=0.8)

        self.at("the grafts")
        gcx, gcy, GW = 4.4, 0.9, 3.2
        mt = Tube(cx=gcx, cy=gcy, W=GW, H=GW, N=18, cr=0.12, rings=(0.58, 0.8), nr=0.28)
        gnoto = Circle(radius=0.28, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.35).move_to([gcx + GW / 2 + 0.38, gcy, 0])
        gt = T("the graft from chapter 1", 26, GREY).move_to([gcx + 0.2, 3.3, 0])
        gl = T("graft", 26, TEAL).move_to([6.3, 2.05, 0])
        gln = leader([6.3, 1.8], [gcx + GW / 2 + 0.36, gcy + 0.3], TEAL)
        self.play(FadeIn(mt.group(noto=False, epi=False)), FadeIn(gt), run_time=0.7)
        self.play(FadeIn(mt.noto), FadeIn(gnoto), FadeIn(gl), Create(gln), run_time=0.7)
        near = [c for c in mt.cells if c.get_center()[0] > gcx + 0.7 and abs(c.get_center()[1] - gcy) < 0.75]
        self.play(*[c.animate.set_stroke(TEAL).set_fill(TEAL, 0.6) for c in near], run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Mouse(Scn):
    def construct(self):
        BY = 0.2
        brain = RoundedRectangle(corner_radius=1.5, width=11.6, height=5.6, stroke_color=GREY, stroke_width=6,
                                 fill_color=GREY, fill_opacity=0.08).move_to([0, BY, 0])
        fp = RoundedRectangle(corner_radius=0.1, width=8.4, height=0.3, stroke_color=TEAL, stroke_width=3,
                              fill_color=TEAL, fill_opacity=0.6).move_to([0, BY - 2.8 + 0.5, 0])
        fpl = T("floor plate", 26, TEAL).move_to([0, BY - 2.8 + 1.0, 0])
        ttl = T("mouse brain, schematic", 28, GREY).move_to([-3.6, 3.35, 0])
        self.play(FadeIn(brain), FadeIn(fp), FadeIn(ttl), FadeIn(fpl), run_time=0.8)

        PXc, PYc = -2.6, 0.7
        patch = RoundedRectangle(corner_radius=0.3, width=3.0, height=1.3, stroke_color=YELLOW, stroke_width=4,
                                 fill_color=YELLOW, fill_opacity=0.25).move_to([PXc, PYc, 0])
        l1 = T("Shh forced on", 32, YELLOW, weight=BOLD).move_to([PXc, PYc + 1.2, 0])
        self.at("forcing the gene")
        self.play(FadeIn(patch, scale=0.8), FadeIn(l1, shift=UP * 0.1), run_time=0.8)
        l2 = T("where Shh is normally absent", 28, TEXT).move_to([PXc + 0.4, PYc - 1.15, 0])
        self.at("normally absent")
        self.play(FadeIn(l2), run_time=0.5)
        self.at("switched on")
        self.play(Indicate(patch, color=YELLOW, scale_factor=1.08), run_time=0.7)
        l3 = T("floor-plate genes on", 32, TEAL, weight=BOLD).move_to([3.0, PYc, 0])
        a3 = arr([PXc + 1.6, PYc, 0], [l3.get_left()[0] - 0.15, PYc, 0], TEAL, 6, 0.25)
        self.at("floor plate genes")
        self.play(patch.animate.set_stroke(TEAL).set_fill(TEAL, 0.6), GrowArrow(a3), FadeIn(l3, shift=LEFT * 0.1), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
SHEET_CX = [(i - 8) * 0.52 for i in range(17)]
SHEET_Y = [2.5, 2.0, 1.5]


def sheet():
    cells = VGroup(*[Rectangle(width=0.46, height=0.46, stroke_color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=0.35
                               ).move_to([x, y, 0]) for y in SHEET_Y for x in SHEET_CX])
    piece = VGroup(*[c for c in cells if abs(c.get_center()[0]) < 0.6])
    return cells, piece


class S06Dish(Scn):
    def construct(self):
        cells, piece = sheet()
        lab = T("neural plate", 28, GREY).move_to([0, 3.35, 0])
        DW, DH, DCY = 8.0, 2.6, -1.4
        dsh = dish(0, DCY, DW, DH)
        # the plate and the dish are on screen together from the first frame
        self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.01), FadeIn(lab), FadeIn(dsh), run_time=0.9)
        self.at("laboratory")
        jl = T("Jessell laboratory", 30, TEXT).move_to([-4.6, 3.35, 0])
        self.play(FadeIn(jl), run_time=0.5)
        chp = chip("the protein", YELLOW, 28).move_to([0, 0.35, 0])
        dots = protein_dots(0, DCY, 16, DW, DH, seed=2)
        self.at("put the protein")
        self.play(FadeIn(chp, shift=DOWN * 0.1), run_time=0.5)
        for d in dots:
            d.shift(UP * 1.5).set_opacity(0)
        self.add(dots)
        self.play(LaggedStart(*[d.animate.shift(DOWN * 1.5).set_opacity(1) for d in dots], lag_ratio=0.06), run_time=1.3)

        self.at("An")
        cut = Rectangle(width=1.7, height=1.7, stroke_color=GOLD, stroke_width=4).move_to(piece.get_center())
        el = T("explant", 36, GOLD, weight=BOLD).move_to([3.7, 0.8, 0])
        eln = leader([2.7, 0.9], [0.95, 1.4], GOLD, 3)
        self.play(Create(cut), piece.animate.set_stroke(GOLD), FadeIn(el), Create(eln), run_time=0.7)
        self.at("small piece")
        self.play(piece.animate.set_fill(GOLD, 0.5), run_time=0.4)
        self.at("of tissue")
        ey = expl_y(DCY, DH)
        tgt = explant(0, ey)
        self.play(FadeOut(cut), FadeOut(el), FadeOut(eln),
                  *[pc.animate.move_to(t.get_center()).scale(EXPL_SIDE / 0.46).set_stroke(GREY).set_fill(GREY, 0.35) for pc, t in zip(piece, tgt)],
                  run_time=0.9)
        el2 = T("explant", 36, GOLD, weight=BOLD).move_to([0, -3.55, 0])
        eln2 = Line([0, -3.25, 0], [0, ey - 0.65, 0], color=GOLD, stroke_width=3)
        self.at("grown in")
        self.play(FadeIn(el2), Create(eln2), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
def dose_dishes():
    d = [dish(x, DISH_Y) for x in DX]
    e = [explant(x, EXPL_Y) for x in DX]
    return d, e


def dose_dots():
    return protein_dots(DX[0], DISH_Y, 16, seed=3), protein_dots(DX[1], DISH_Y, 4, seed=5)


LAB_Y2 = DISH_Y - DISH_H / 2 - 0.5
CHIP_Y2 = LAB_Y2 - 0.8


class S07Dose(Scn):
    def construct(self):
        cr = T("Roelink and colleagues, 1995", 32, TEXT).move_to([0, 3.4, 0])
        d, e = dose_dishes()
        # credit and both dishes arrive together
        self.play(FadeIn(cr, shift=DOWN * 0.1), FadeIn(VGroup(*d)), FadeIn(VGroup(*e)), run_time=0.8)
        self.at("gave explants")
        self.play(*[Indicate(g, color=GOLD, scale_factor=1.12) for g in e], run_time=0.8)
        fr = chip("purified signaling fragment", YELLOW, 30).move_to([0, 2.7, 0])
        hi, lo = dose_dots()
        self.at("purified signaling")
        self.play(FadeIn(fr, shift=DOWN * 0.15), run_time=0.5)
        for g in (hi, lo):
            for dd in g:
                dd.shift(UP * 1.6).set_opacity(0)
        self.add(hi, lo)
        self.play(LaggedStart(*[dd.animate.shift(DOWN * 1.6).set_opacity(1) for dd in list(hi) + list(lo)], lag_ratio=0.03), run_time=1.1)
        l1 = T("higher Shh", 36, YELLOW).move_to([DX[0], LAB_Y2, 0])
        l2 = T("lower Shh", 36, YELLOW).move_to([DX[1], LAB_Y2, 0])
        self.at("of the protein")
        self.play(FadeIn(l1), FadeIn(l2), run_time=0.6)
        self.finish()


def dose_base():
    cr = T("Roelink and colleagues, 1995", 32, TEXT).move_to([0, 3.4, 0])
    d, e = dose_dishes()
    hi, lo = dose_dots()
    l1 = T("higher Shh", 36, YELLOW).move_to([DX[0], LAB_Y2, 0])
    l2 = T("lower Shh", 36, YELLOW).move_to([DX[1], LAB_Y2, 0])
    return cr, d, e, hi, lo, l1, l2


class S08Dose2(Scn):
    def construct(self):
        cr, d, e, hi, lo, l1, l2 = dose_base()
        self.add(cr, *d, *e, hi, lo, l1, l2)
        self.at("At the higher")
        self.play(Indicate(l1, color=YELLOW, scale_factor=1.15), run_time=0.8)
        self.at("floor plate markers")
        c1 = chip("floor-plate markers", TEAL, 28).move_to([DX[0], CHIP_Y2, 0])
        self.play(*[c.animate.set_stroke(TEAL).set_fill(TEAL, 0.7) for c in e[0]], FadeIn(c1, shift=UP * 0.1), run_time=0.9)
        self.at("Lower ones")
        self.play(Indicate(l2, color=YELLOW, scale_factor=1.15), run_time=0.8)
        self.at("motor neuron markers")
        c2 = chip("motor neuron markers", BLUE, 28).move_to([DX[1], CHIP_Y2, 0])
        self.play(*[c.animate.set_stroke(BLUE).set_fill(BLUE, 0.7) for c in e[1]], FadeIn(c2, shift=UP * 0.1), run_time=0.9)
        self.finish()


class S09Dose3(Scn):
    def construct(self):
        cr, d, e, hi, lo, l1, l2 = dose_base()
        for c in e[0]:
            c.set_stroke(TEAL).set_fill(TEAL, 0.7)
        for c in e[1]:
            c.set_stroke(BLUE).set_fill(BLUE, 0.7)
        c1 = chip("floor-plate markers", TEAL, 28).move_to([DX[0], CHIP_Y2, 0])
        c2 = chip("motor neuron markers", BLUE, 28).move_to([DX[1], CHIP_Y2, 0])
        self.add(*d, *e, hi, lo, l1, l2, c1, c2)
        same = chip("same Shh", YELLOW, 34).move_to([0, 2.7, 0])
        self.at("One protein")
        self.play(FadeIn(same, scale=0.8), run_time=0.7)
        rim_y = DISH_Y + DISH_H / 2
        a1 = arr([-0.6, 2.4, 0], [DX[0] + 0.6, rim_y + 0.05, 0], YELLOW, 6)
        a2 = arr([0.6, 2.4, 0], [DX[1] - 0.6, rim_y + 0.05, 0], YELLOW, 6)
        self.at("different doses")
        self.play(GrowArrow(a1), GrowArrow(a2), run_time=0.7)
        fin = T("one protein, two doses, two fates", 38, TEXT).move_to([0, 3.5, 0])
        self.at("different ventral fates")
        self.play(FadeIn(fin, shift=DOWN * 0.1), Indicate(c1, color=TEAL), Indicate(c2, color=BLUE), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S10Brake(Scn):
    def construct(self):
        d = brake_scene()
        d["p"].set_fill(GREY, 0.3).set_stroke(TEXT)
        q = T("how does a cell receive it?", 42, TEXT).move_to([0, 3.3, 0])
        rl = T("receptor", 28, TEXT, weight=BOLD).move_to([PX, LAB_Y, 0])
        ml = T("membrane\nprotein", 28, TEXT, weight=BOLD, line_spacing=0.8).move_to([SX, LAB_Y, 0])
        self.play(FadeIn(d["mem"]), FadeIn(d["p"]), FadeIn(d["s"]), FadeIn(q, shift=DOWN * 0.1), FadeIn(rl), FadeIn(ml), run_time=0.7)
        brk = brake_arm()
        bl = T("brake", 32, RED, weight=BOLD).move_to([0, ARM_Y + 0.65, 0])
        self.at("Think of")
        self.play(Create(brk[0]), run_time=0.4)
        self.play(FadeIn(brk[1], shift=RIGHT * 0.2), FadeIn(bl), run_time=0.4)
        self.finish()


class S11Brake2(Scn):
    def construct(self):
        d = brake_scene()
        d["p"].set_fill(GREY, 0.3).set_stroke(TEXT)
        rl = T("receptor", 28, TEXT, weight=BOLD).move_to([PX, LAB_Y, 0])
        ml = T("membrane\nprotein", 28, TEXT, weight=BOLD, line_spacing=0.8).move_to([SX, LAB_Y, 0])
        brk = brake_arm()
        bl = T("brake", 32, RED, weight=BOLD).move_to([0, ARM_Y + 0.65, 0])
        q = T("how does a cell receive it?", 42, TEXT).move_to([0, 3.3, 0])
        self.add(d["mem"], d["p"], d["s"], rl, ml, brk, bl, q)
        self.at("The receptor")
        self.play(FadeOut(q), run_time=0.4)
        self.at("patched")
        self.play(d["p"].animate.set_stroke(PURPLE).set_fill(PURPLE, 0.4), Transform(rl, d["plab"]), run_time=0.6)
        self.at("is the brake")
        self.play(Transform(brk, d["tbar"]), run_time=0.7)
        self.at("holds a")
        self.play(FadeIn(d["analogy"]), run_time=0.6)
        self.at("membrane protein")
        self.play(Indicate(d["s"], color=TEXT, scale_factor=1.06), run_time=0.8)
        self.at("smoothened")
        self.play(Transform(ml, d["slab"]), run_time=0.4)
        self.at("switched off")
        self.play(FadeIn(d["state"], shift=UP * 0.1), run_time=0.5)
        self.finish()


class S12Brake3(Scn):
    def construct(self):
        d = brake_scene()
        d["p"].set_fill(PURPLE, 0.4).set_stroke(PURPLE)
        self.add(d["mem"], d["p"], d["s"], d["plab"], d["slab"], d["state"], d["tbar"], d["analogy"])
        d["shh"].move_to([PX, 3.3, 0])
        # the caption leaves first; the chip starts inside the frame
        self.play(FadeOut(d["analogy"]), run_time=0.4)
        self.play(FadeIn(d["shh"], shift=DOWN * 0.1), run_time=0.4)
        self.at("binds patched")
        self.play(d["shh"].animate.move_to([PX, 2.4, 0]), run_time=0.8)
        self.at("lifts the")
        self.play(FadeOut(d["tbar"]), run_time=0.8)
        self.at("freed")
        self.play(Indicate(d["s"], color=GREEN, scale_factor=1.08), run_time=0.7)
        self.at("turns on")
        on = T("on", 36, GREEN, weight=BOLD).move_to([SX, STATE_Y, 0])
        self.play(d["s"].animate.set_stroke(GREEN).set_fill(GREEN, 0.6), Transform(d["state"], on), run_time=0.8)
        self.finish()
# ---------------------------------------------------------------------------------------------
class S13Gli(Scn):
    def construct(self):
        cb = cell_body()
        cell_l, nuc_l, cil_l = cell_labels()
        self.play(FadeIn(cb), FadeIn(cell_l), FadeIn(nuc_l), FadeIn(cil_l), run_time=0.9)
        bars = VGroup(*[gli_bar(y) for y in BAR_ROWS])
        self.at("transcription factors")
        self.play(LaggedStart(*[FadeIn(b, scale=0.8) for b in bars], lag_ratio=0.25), run_time=1.2)
        big = T("Gli", 60, PINK, weight=BOLD).move_to(GLI_LAB)
        gl = leader([2.4, 0.3], [1.65, 0.3], PINK)
        self.at("called the")
        self.play(FadeIn(big, shift=LEFT * 0.2), Create(gl), run_time=0.7)
        note = T("said glee", 28, GREY).move_to([GLI_LAB[0], GLI_LAB[1] - 0.65, 0])
        self.after("called the", 1.6)
        self.play(FadeIn(note), run_time=0.5)
        self.finish()


def carried_cell(bars=True):
    cb = cell_body()
    cell_l, nuc_l, cil_l = cell_labels()
    return cb, cell_l, nuc_l, cil_l


class S14Gli2(Scn):
    def construct(self):
        cb, cell_l, nuc_l, cil_l = carried_cell()
        bars = VGroup(*[gli_bar(y) for y in BAR_ROWS])
        big = T("Gli", 60, PINK, weight=BOLD).move_to(GLI_LAB)
        gl = leader([2.4, 0.3], [1.65, 0.3], PINK)
        self.add(cb, cell_l, nuc_l, cil_l, bars, big, gl)
        sig_l = T("signal absent", 34, YELLOW).move_to([-4.4, 3.2, 0])
        self.at("Without the signal")
        self.play(FadeIn(sig_l, shift=DOWN * 0.1), run_time=0.6)
        g3 = T("Gli3", 60, PINK, weight=BOLD).move_to(GLI_LAB)
        self.at("above all")
        self.play(Transform(big, g3), run_time=0.6)
        slashes = VGroup(*[slash(b) for b in bars])
        self.at("is cut")
        self.play(FadeIn(slashes), run_time=0.4)
        reps = [rep_piece(x) for x in REP_X]
        anims = []
        for b, y, rp in zip(bars, BAR_ROWS, reps):
            anims.append(b[1].animate.shift(RIGHT * 0.6).set_opacity(0.0))
            anims.append(Transform(b[0], rp))
        self.at("short repressor")
        self.play(FadeOut(slashes), *anims, run_time=1.6)
        rl = T("Gli repressor", 28, RED, weight=BOLD).move_to([0, -0.85, 0])
        rln = leader([0, -1.15], [0, -1.95], RED)
        self.play(FadeIn(rl), Create(rln), run_time=0.6)
        self.at("primary cilium")
        cl = T("primary cilium", 30, GOLD).move_to([2.35, 2.6, 0])
        cln = leader([0.95, 2.6], [0.2, 2.55], GOLD)
        self.play(FadeOut(cil_l), FadeIn(cl), Create(cln), cb[2].animate.set_stroke(GOLD, opacity=1), cb[4].animate.set_stroke(GOLD).set_fill(GOLD, 0.6), run_time=0.7)
        self.play(Indicate(cb[4], color=GOLD, scale_factor=2.2), run_time=0.7)
        self.finish()


class S15Gli3(Scn):
    def construct(self):
        cb, cell_l, nuc_l, cil_l = carried_cell()
        reps = [rep_piece(x) for x in REP_X]
        g3 = T("Gli3", 60, PINK, weight=BOLD).move_to(GLI_LAB)
        sig_l = T("signal absent", 34, YELLOW).move_to([-4.4, 3.2, 0])
        rl = T("Gli repressor", 28, RED, weight=BOLD).move_to([0, -0.85, 0])
        rln = leader([0, -1.15], [0, -1.95], RED)
        cl = T("primary cilium", 30, GOLD).move_to([2.35, 2.6, 0])
        cln = leader([0.95, 2.6], [0.2, 2.55], GOLD)
        cb[2].set_stroke(GOLD, opacity=1)
        cb[4].set_stroke(GOLD).set_fill(GOLD, 0.6)
        self.add(cb, cell_l, nuc_l, cl, cln, *reps, g3, sig_l, rl, rln)
        sig_p = T("signal present", 34, YELLOW, weight=BOLD).move_to([-4.4, 3.2, 0])
        gli = T("Gli", 60, PINK, weight=BOLD).move_to(GLI_LAB)
        self.at("With the signal")
        self.play(Transform(sig_l, sig_p), Transform(g3, gli), run_time=0.6)
        # fewer repressor pieces: two of the three are gone, one stays in the nucleus
        self.at("less repressor")
        rl2 = T("Gli repressor", 28, RED, weight=BOLD).move_to([3.3, -0.95, 0])
        rln2 = leader([2.9, -1.25], [1.7, -1.95], RED)
        self.play(FadeOut(reps[0], scale=0.5), FadeOut(reps[1], scale=0.5), Transform(rl, rl2), Transform(rln, rln2), run_time=0.8)
        # full-length Gli appears, then acts in the same nucleus as the remaining repressor
        bars = [gli_bar(-2.05, PINK).scale(0.5).move_to([-0.9, -2.05, 0]), gli_bar(-2.7, PINK).scale(0.5).move_to([-0.9, -2.7, 0])]
        self.at("full length")
        self.play(*[FadeIn(b) for b in bars], run_time=0.6)
        self.at("acts as")
        self.play(*[b.animate.set_color(GREEN) for b in bars], run_time=0.8)
        al = T("Gli activator", 28, GREEN, weight=BOLD).move_to([-2.0, -0.85, 0])
        aln = leader([-1.6, -1.15], [-1.0, -1.85], GREEN)
        self.at("activator")
        self.play(FadeIn(al), Create(aln), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class ScaleRig:
    """A balance scale whose beam tilts; loads ride on the pans."""

    def __init__(self, scene):
        self.sc = scene
        self.piv = np.array([0.0, 1.0, 0.0])
        self.L = 4.4
        self.t = ValueTracker(0.0)
        self.pan_l = self._pan()
        self.pan_r = self._pan()

    def _pan(self):
        return VMobject(stroke_color=TEXT, stroke_width=5).set_points_as_corners([[-1.75, 0.5, 0], [-1.55, -0.5, 0], [1.55, -0.5, 0], [1.75, 0.5, 0]])

    def ends(self):
        a = self.t.get_value()
        d = np.array([np.cos(a), np.sin(a), 0])
        return self.piv - self.L * d, self.piv + self.L * d

    def pan_c(self, side):
        e = self.ends()[side]
        return e + np.array([0, -1.7, 0])

    def build(self):
        sc = self
        fulc = Polygon([0, 1.0, 0], [-1.0, -2.6, 0], [1.0, -2.6, 0], stroke_color=TEXT, stroke_width=4, fill_color=TEXT, fill_opacity=0.1)
        beam = always_redraw(lambda: Line(sc.ends()[0], sc.ends()[1], color=TEXT, stroke_width=9))
        pivd = Dot(self.piv, radius=0.14, color=TEXT)

        def strings(side):
            def f():
                c = sc.pan_c(side)
                e = sc.ends()[side]
                return VGroup(Line(e, c + np.array([-1.75, 0.5, 0]), color=GREY, stroke_width=3),
                              Line(e, c + np.array([1.75, 0.5, 0]), color=GREY, stroke_width=3))
            return always_redraw(f)

        self.pan_l.add_updater(lambda m: m.move_to(sc.pan_c(0)))
        self.pan_r.add_updater(lambda m: m.move_to(sc.pan_c(1)))
        return [fulc, beam, pivd, strings(0), strings(1), self.pan_l, self.pan_r]

    def load(self, side, mob):
        mob.add_updater(lambda m: m.move_to(self.pan_c(side) + np.array([0, -0.05, 0])))
        return mob


class S16Gli4(Scn):
    def construct(self):
        rig = ScaleRig(self)
        parts = rig.build()
        # the scale fills the frame from the first words
        self.play(*[FadeIn(p) for p in parts], run_time=0.8)
        prog = VGroup(Circle(radius=0.65, stroke_color=TEXT, stroke_width=5, fill_color=TEXT, fill_opacity=0.12),
                      Circle(radius=0.26, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.3))
        prog.move_to([0, 3.0, 0])
        pl = T("progenitor", 36, TEXT, weight=BOLD).move_to([2.3, 3.0, 0])
        self.at("a progenitor")
        self.play(FadeIn(prog, scale=0.7), FadeIn(pl), run_time=0.6)
        rd = arr([0, 2.3, 0], [0, 1.25, 0], GOLD, 7, 0.3)
        self.at("reads")
        self.play(GrowArrow(rd), run_time=0.5)
        self.at("balance")
        self.play(Indicate(parts[1], color=GOLD, scale_factor=1.0), run_time=0.5)
        al = rig.load(0, chip("Gli activator", GREEN, 30))
        rl = rig.load(1, chip("Gli repressor", RED, 30))
        self.at("of activator")
        self.add(al)
        self.play(FadeIn(al), rig.t.animate.set_value(0.13), run_time=0.7)
        self.at("against repressor")
        self.add(rl)
        sa = T("signal absent", 30, YELLOW).move_to([4.3, -2.9, 0])
        sp = T("signal present", 30, YELLOW).move_to([-4.3, -2.9, 0])
        self.play(FadeIn(rl), rig.t.animate.set_value(-0.18), FadeIn(sa), run_time=0.7)
        self.play(rig.t.animate.set_value(0.18), FadeOut(sa), FadeIn(sp), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
PLANT_X = 5.55


def plant(x=PLANT_X):
    stem = Line([x, -3.0, 0], [x, 2.5, 0], color=PLANT, stroke_width=10)
    leaves = VGroup()
    for k, y in enumerate((-2.4, -1.4, -0.4, 0.6, 1.6)):
        for sgn in (-1, 1):
            leaves.add(Ellipse(width=1.0, height=0.6, stroke_color=PLANT, stroke_width=3, fill_color=PLANT, fill_opacity=0.5
                               ).rotate(sgn * 0.45).move_to([x + sgn * 0.42, y + (0.2 if sgn > 0 else 0), 0]))
    top = Ellipse(width=0.6, height=1.0, stroke_color=PLANT, stroke_width=3, fill_color=PLANT, fill_opacity=0.6).move_to([x, 2.8, 0])
    return VGroup(stem, leaves, top)


class S17Cyclo(Scn):
    def construct(self):
        d = brake_scene(on=True)
        d["p"].set_fill(PURPLE, 0.4).set_stroke(PURPLE)
        d["shh"].move_to([PX, 2.4, 0])
        self.add(d["mem"], d["p"], d["s"], d["plab"], d["slab"], d["state"], d["shh"])
        cyc = chip("cyclopamine", TEXT, 30).move_to([0.0, MEM_Y, 0])
        self.at("Cyclopamine")
        self.play(FadeIn(cyc, shift=DOWN * 0.15), run_time=0.6)
        pl = plant()
        vl = T("Veratrum", 28, TEXT).move_to([PLANT_X, -3.5, 0])
        self.at("from a plant")
        self.play(FadeIn(pl, shift=UP * 0.2), FadeIn(vl), run_time=0.9)
        self.at("blocks")
        off = T("off", 36, GREY, weight=BOLD).move_to([SX, STATE_Y, 0])
        self.play(cyc.animate.next_to(d["s"], LEFT, buff=0.04).set_y(MEM_Y), run_time=0.5)
        self.play(d["s"].animate.set_stroke(GREY).set_fill(GREY, 0.3), Transform(d["state"], off), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S18Ko(Scn):
    def construct(self):
        nl = T("necessity", 44, TEXT).move_to([0, 3.3, 0])
        strand = RoundedRectangle(corner_radius=0.3, width=12.4, height=2.0, stroke_color=GREY, stroke_width=4,
                                  fill_color=GREY, fill_opacity=0.15).move_to([0, -0.9, 0])
        genes = VGroup(gene_box("", GREY, w=3.4, h=1.3, x=-4.1, y=-0.9), gene_box("Shh", YELLOW, w=3.4, h=1.3, size=52, x=0, y=-0.9),
                       gene_box("", GREY, w=3.4, h=1.3, x=4.1, y=-0.9))
        ms = mouse(0, 1.55, 1.9)
        # the mouse and the gene strip are on screen from the first word
        self.play(FadeIn(nl, shift=DOWN * 0.1), FadeIn(strand), FadeIn(genes), FadeIn(ms, shift=DOWN * 0.2), run_time=0.8)
        self.at("knockout")
        kl = T("knockout", 60, TEXT, weight=BOLD).move_to([0, -2.9, 0])
        self.play(FadeIn(kl, shift=UP * 0.1), run_time=0.6)
        self.at("deliberately")
        xm = xmark(genes[1][0], TEXT, 10)
        self.play(Create(xm), genes[1][0].animate.set_fill(YELLOW, 0.05), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
TCX, TCY, TW = -3.0, 0.45, 5.4
X0R = 0.7


def big_tube():
    return Tube(cx=TCX, cy=TCY, W=TW, H=TW, nr=0.38)


class S19Ko2(Scn):
    def construct(self):
        tb = big_tube()
        tb.paint_normal()
        self.add(tb.group())
        normal = left_at(T("normal", 48, TEXT, weight=BOLD), X0R, 3.2)
        rows = legend_rows([LEG_FP, LEG_MN, LEG_IN], X0R, 1.3)
        self.play(FadeIn(normal), *[FadeIn(r) for r in rows], run_time=0.5)
        # swap the case label and clear the cells in the same animation
        nos = left_at(T("no Shh", 48, TEXT, weight=BOLD, t2c={"Shh": YELLOW}), X0R, 3.2)
        cr = left_at(T("Chiang, Beachy and\ncolleagues, 1996", 26, TEXT, line_spacing=0.9), X0R, 2.3)
        ven = [c for c, (dm, _) in zip(tb.cells, tb.info) if dm not in ("dorsal", "p0")]
        self.at("lacking")
        self.play(ReplacementTransform(normal, nos), FadeIn(cr),
                  *[c.animate.set_stroke(GREY, opacity=0.28).set_fill(GREY, 0) for c in ven], run_time=1.0)
        fpl = left_at(T("no floor plate", 30, TEAL), X0R, -2.5)
        fp_r = [tb.fp.get_right()[0] + 0.05, tb.fp.get_center()[1]]
        fln = leader([X0R - 0.1, -2.5], fp_r, TEAL)
        self.at("no floor plate")
        self.play(tb.fp.animate.set_stroke(GREY, width=2, opacity=0.4).set_fill(GREY, 0), FadeIn(fpl), Create(fln), run_time=0.8)
        ml = left_at(T("most ventral\ncell types missing", 34, TEXT, line_spacing=0.9), X0R, -1.2)
        self.at("lack most")
        self.play(FadeIn(ml, shift=UP * 0.1), run_time=0.7)
        self.finish()


def ko_tube():
    tb = big_tube()
    tb.paint_knockout()
    tb.ghost_fp()
    return tb


def rescue_tube():
    tb = big_tube()
    tb.paint_rescue()
    tb.ghost_fp()
    return tb


# ---------------------------------------------------------------------------------------------
class S20Logic(Scn):
    def construct(self):
        card = RoundedRectangle(corner_radius=0.25, width=11.8, height=6.6, stroke_color=GOLD, stroke_width=3,
                                fill_color=GOLD, fill_opacity=0.05).move_to([0, 0.0, 0])
        ht = T("hypothesis", 44, GOLD, weight=BOLD).move_to([0, 2.65, 0])
        sent = T("Shh's main job:\nstop Gli3 repressor forming", 58, TEXT, line_spacing=0.95,
                 t2c={"Shh": YELLOW, "Gli3 repressor": RED}).move_to([0, 0.75, 0])
        # the sentence is in the card from the first frame
        self.play(FadeIn(card), FadeIn(ht, shift=DOWN * 0.1), FadeIn(sent, shift=UP * 0.1), run_time=0.8)
        shh = chip("Sonic hedgehog", YELLOW, 38).move_to([-3.3, -1.9, 0])
        gl = chip("Gli3 repressor", RED, 38).move_to([3.4, -1.9, 0])
        self.at("main job")
        self.play(FadeIn(shh, shift=DOWN * 0.2), run_time=0.7)
        self.at("to stop")
        ih = inhib([shh.get_right()[0] + 0.15, -1.9, 0], [gl.get_left()[0] - 0.15, -1.9, 0], RED, 9)
        self.play(Create(ih), run_time=0.8)
        self.at("repressor from")
        self.play(FadeIn(gl, shift=LEFT * 0.2), run_time=0.7)
        self.finish()


def predict_items():
    d = {}
    d["title"] = T("Predict", 56, GOLD, weight=BOLD).move_to([0, 3.2, 0])
    d["shh"] = gene_box("Shh", YELLOW, w=3.6, h=1.6, size=60, x=-3.5, y=1.4)
    d["shhx"] = xmark(d["shh"][0], TEXT, 9)
    d["gli"] = gene_box("Gli3", PINK, w=3.6, h=1.6, size=60, x=3.5, y=1.4)
    d["glix"] = xmark(d["gli"][0], TEXT, 9)
    d["cells"] = VGroup(*[DashedVMobject(Circle(radius=0.6, stroke_color=GREY, stroke_width=3), num_dashes=14).move_to([x, -0.9, 0])
                          for x in np.linspace(-4.8, 4.8, 8)])
    d["q"] = T("what happens to the ventral cells?", 50, TEXT).move_to([0, -2.6, 0])
    return d


class S21Predict(Scn):
    def construct(self):
        d = predict_items()
        # the word Predict arrives with the two boxes and the unknown cells
        self.play(FadeIn(d["title"], shift=DOWN * 0.1), FadeIn(d["shh"]), FadeIn(d["gli"]), FadeIn(d["cells"]), FadeIn(d["q"]), run_time=0.8)
        self.at("lacking sonic")
        self.play(Create(d["shhx"]), run_time=0.6)
        self.at("what should")
        self.play(Indicate(d["q"], color=GOLD, scale_factor=1.04), run_time=0.7)
        self.at("removing")
        self.play(Create(d["glix"]), run_time=0.6)
        self.at("ventral cells")
        self.play(Indicate(d["cells"], color=GOLD, scale_factor=1.08), run_time=0.8)
        self.finish()


class S22Pause(NarratedScene):
    def construct(self):
        d = predict_items()
        self.add(*d.values())
        self.add(d["shhx"], d["glix"])
        pp = T("pause and predict", 32, GOLD, weight=BOLD).move_to([0, -3.1, 0])
        bar_bg = Rectangle(width=8.0, height=0.14, stroke_width=0, fill_color=GREY, fill_opacity=0.35).move_to([0, -3.6, 0])
        bar = Rectangle(width=8.0, height=0.14, stroke_width=0, fill_color=GOLD, fill_opacity=0.9).move_to([0, -3.6, 0])
        self.add(pp, bar_bg, bar)
        self.play(bar.animate.stretch_to_fit_width(0.01, about_edge=LEFT).align_to(bar_bg, LEFT), run_time=4.9, rate_func=linear)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S23Reveal(Scn):
    def construct(self):
        tb = ko_tube()
        self.add(tb.group())
        no1 = left_at(T("no Shh", 40, TEXT, weight=BOLD, t2c={"Shh": YELLOW}), X0R, 3.2)
        self.add(no1)
        no2 = left_at(T("no Gli3", 40, TEXT, weight=BOLD, t2c={"Gli3": PINK}), X0R, 2.5)
        cr = left_at(T("Litingtung and Chiang, 2000", 26, TEXT), X0R, 1.75)
        self.play(FadeIn(no2, shift=LEFT * 0.2), FadeIn(cr), run_time=0.5)
        rows = legend_rows([LEG_MN, LEG_IN], X0R, 0.6)
        self.at("motor neurons")
        self.play(*[c.animate.set_stroke(BLUE, opacity=1).set_fill(BLUE, 0.55) for c in tb.sel("pMN")], FadeIn(rows[0], shift=LEFT * 0.2), run_time=0.9)
        self.at("interneuron classes")
        self.play(*[c.animate.set_stroke(ORANGE, opacity=1).set_fill(ORANGE, 0.55) for c in tb.sel(["p2", "p1", "p0"])],
                  FadeIn(rows[1], shift=LEFT * 0.2), run_time=0.9)
        self.finish()


class S24Reveal2(Scn):
    def construct(self):
        tb = rescue_tube()
        self.add(tb.group())
        no1 = left_at(T("no Shh", 40, TEXT, weight=BOLD, t2c={"Shh": YELLOW}), X0R, 3.2)
        rows = legend_rows([LEG_MN, LEG_IN], X0R, -0.4)
        self.add(no1, *rows)
        gl = gene_box("Gli3", PINK, w=2.4, h=1.0, size=38, x=4.4, y=2.1)
        glx = xmark(gl[0], TEXT, 8)
        self.at("Removing")
        self.play(FadeIn(gl), Create(glx), run_time=0.6)
        tgt = max(tb.sel("pMN", +1), key=lambda c: c.get_center()[0]).get_center()
        a = arr([3.3, 1.7, 0], [tgt[0] + 0.45, tgt[1] + 0.1, 0], PINK, 6)
        al = left_at(T("part of Shh's job", 30, YELLOW), 2.7, 0.55)
        self.at("did part of")
        self.play(GrowArrow(a), FadeIn(al), run_time=0.9)
        dm = left_at(T("double-mutant\nrescue", 44, GOLD, weight=BOLD, line_spacing=0.9), X0R, -2.3)
        self.at("double mutant")
        self.play(FadeIn(dm, shift=UP * 0.1), run_time=0.8)
        self.finish()


class S24bLogic(Scn):
    def construct(self):
        dm = T("double-mutant rescue", 46, GOLD, weight=BOLD).move_to([-1.6, 3.3, 0])
        self.add(dm)
        g1 = gene_box("Shh", YELLOW, w=3.2, h=1.3, size=48, x=-3.7, y=1.55)
        g2 = gene_box("Gli3", PINK, w=3.2, h=1.3, size=48, x=3.7, y=1.55)
        x1, x2 = xmark(g1[0], TEXT, 9), xmark(g2[0], TEXT, 9)
        self.add(g1, g2, x1, x2)
        da = DoubleArrow([-1.85, 1.55, 0], [1.85, 1.55, 0], color=TEXT, stroke_width=7, tip_length=0.28, buff=0)
        gi = T("genes interact", 40, TEXT).move_to([0, 0.55, 0])
        self.at("genes interact")
        self.play(GrowFromCenter(da), FadeIn(gi, shift=UP * 0.1), run_time=0.8)
        qm = T("how?", 50, GOLD, weight=BOLD).move_to([4.9, 3.3, 0])
        self.at("not how")
        self.play(FadeIn(qm, scale=0.7), run_time=0.6)
        items = [chip("Shh", YELLOW, 44, pad=0.32), chip("Patched", PURPLE, 44, pad=0.32), chip("Smoothened", GREEN, 44, pad=0.32),
                 chip("Gli3 repressor", RED, 44, pad=0.32)]
        items[0].move_to([-3.2, -1.0, 0]); items[1].move_to([3.2, -1.0, 0])
        items[2].move_to([3.2, -2.85, 0]); items[3].move_to([-3.2, -2.85, 0])
        bars = [inhib([items[0].get_right()[0] + 0.06, -1.0, 0], [items[1].get_left()[0] - 0.06, -1.0, 0], RED, 6),
                inhib([3.2, items[1].get_bottom()[1] - 0.06, 0], [3.2, items[2].get_top()[1] + 0.06, 0], RED, 6),
                inhib([items[2].get_left()[0] - 0.06, -2.85, 0], [items[3].get_right()[0] + 0.06, -2.85, 0], RED, 6)]
        self.at("known pathway")
        self.play(LaggedStart(*[AnimationGroup(FadeIn(it, shift=UP * 0.1), Create(b)) for it, b in zip(items, bars + [VGroup()])], lag_ratio=0.35),
                  run_time=0.9)
        fr = RoundedRectangle(corner_radius=0.25, width=11.8, height=3.55, stroke_color=GOLD, stroke_width=4).move_to([0, -2.0, 0])
        bl = T("the how", 48, GOLD, weight=BOLD).move_to([0, -1.92, 0])
        self.at("supplies the")
        self.play(FadeOut(qm), Create(fr), FadeIn(bl), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S25Takeaway(Scn):
    def construct(self):
        tk = T("takeaway", 48, GOLD, weight=BOLD).move_to([0, 3.0, 0])
        cap = T("much of what\nShh does in the\nspinal cord", 56, TEXT, line_spacing=0.95, t2c={"Shh": YELLOW}).move_to([3.9, -0.5, 0])
        self.play(FadeIn(tk, shift=DOWN * 0.1), FadeIn(cap, shift=LEFT * 0.2), run_time=0.7)
        shh = chip("Sonic hedgehog", YELLOW, 56).move_to([-3.5, 1.3, 0])
        gl = chip("Gli3 repressor", RED, 56).move_to([-3.5, -2.5, 0])
        self.at("sonic hedgehog")
        self.play(FadeIn(shh, shift=RIGHT * 0.2), run_time=0.7)
        ih = inhib([-3.5, shh.get_bottom()[1] - 0.12, 0], [-3.5, gl.get_top()[1] + 0.12, 0], RED, 10)
        self.at("block")
        self.play(Create(ih), FadeIn(gl), run_time=0.7)
        self.at("repressor")
        self.play(Indicate(gl, color=GOLD, scale_factor=1.06), run_time=0.7)
        self.finish()


class S26Takeaway2(Scn):
    def construct(self):
        tcx = -2.4
        tb = Tube(cx=tcx, cy=0.9, W=4.2, H=4.2, nr=0.34, cr=0.13)
        boxes = strip()
        boxes[1][0].set_stroke(GOLD, width=4).set_fill(GOLD, 0.2)
        boxes[1][1].set_color(TEXT)
        h1, h2 = halo(tb.noto), halo(tb.fp, extra=0.1)
        self.add(tb.group(), h1, h2, boxes)
        self.at("signal is")
        new = T("2  Sonic hedgehog,\nread through\na brake", 24, YELLOW, line_spacing=0.8).move_to(boxes[1][0])
        self.play(boxes[1][0].animate.set_stroke(YELLOW, width=4).set_fill(YELLOW, 0.18), FadeOut(boxes[1][1]), run_time=0.4)
        self.play(FadeIn(new), run_time=0.5)
        # the mini brake, centred near x = 3.6
        MY, MX0 = 0.75, 3.6
        mem = Rectangle(width=4.4, height=0.45, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.3).move_to([MX0, MY, 0])
        pb = RoundedRectangle(corner_radius=0.15, width=1.1, height=2.0, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=0.4).move_to([MX0 - 1.15, MY, 0])
        sb = RoundedRectangle(corner_radius=0.15, width=1.1, height=2.0, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.3).move_to([MX0 + 1.15, MY, 0])
        tb_ = inhib([MX0 - 0.5, MY + 0.55, 0], [MX0 + 0.55, MY + 0.55, 0], RED, 6)
        pl_ = T("Patched", 26, PURPLE, weight=BOLD).move_to([MX0 - 1.15, MY - 1.4, 0])
        sl_ = T("Smoothened", 26, TEXT, weight=BOLD).move_to([MX0 + 1.3, MY - 1.4, 0])
        shh_c = chip("Sonic hedgehog", YELLOW, 28).move_to([MX0 - 1.8, 3.2, 0])
        self.play(FadeIn(shh_c, shift=DOWN * 0.1), run_time=0.5)
        self.at("read through")
        self.play(FadeIn(VGroup(mem, pb, sb, pl_, sl_)), Create(tb_), run_time=0.7)
        # Shh docks on Patched, lifts the brake; Smoothened turns on
        self.play(shh_c.animate.move_to([MX0 - 1.15, MY + 1.3, 0]), run_time=0.6)
        self.play(FadeOut(tb_), sb.animate.set_stroke(GREEN).set_fill(GREEN, 0.55), run_time=0.6)
        self.at("Next")
        self.play(*light_box(boxes[2]), run_time=0.8)
        self.after("Next", 1.2)
        self.play(Indicate(boxes[2][0], color=GOLD, scale_factor=1.04), run_time=0.8)
        self.finish()


class S27End(EndCard):
    LINE = "The signal is Sonic hedgehog, read through a brake."
