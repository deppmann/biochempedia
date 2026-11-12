"""A Theory Built in Steps (Cells Are Everywhere, film 2)

Same look as film 1 (../scenes.py): dark ground, one colour per concept.
COLOUR MAP
  BLUE   = the eye line (100 um) and water      TAN   = cork boxes (cell walls)
  GREEN  = green alga / plants                  TEAL  = Paramecium
  YELLOW = vocabulary, the lit step             LILAC = a generic living cell
The size ladder (left) is computed: y = Y0 + DEC * (log10(size in um) + 1).
The timeline (bottom) is evenly spaced and marked schematic.
The panel (right) holds the cell theory's three parts, lit as the story earns them.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

BROWN = "#B9784A"
AMBER = "#F2A93B"
PAPER = "#F2F2F2"
STEEL = "#B8C0CC"
TAN = "#D2B48C"
TAN_D = "#A9854E"
CELLC = "#C9B6F0"
CELLD = "#6E57A6"
INK = "#2B3345"

AX = -4.4          # x of the ladder axis
Y0 = -2.7          # y of 0.1 um
DEC = 1.05         # height of one decade (one rung)
EYE_X1 = -3.4      # right end of the eye line
C = np.array([0.2, 0.5, 0])   # centre of the microscope view
RV = 2.2                      # radius of the microscope view

TX = [-2.6, -0.8, 1.0, 2.8]
TLAB = ["1665", "1676", "about 1840", "1850s"]
TLY = -3.3
TL_X0, TL_X1 = -3.2, 3.5

LINES = ["All living things\nare made of one\nor more cells.",
         "The cell is the\nbasic unit of life.",
         "All cells come\nfrom cells that\nalready exist."]


def Y(v):
    return Y0 + DEC * (np.log10(v) + 1)


RUNGS = [(0.1, "0.1 µm"), (1, "1 µm"), (10, "10 µm"), (100, "100 µm"), (1000, "1,000 µm"), (10000, "10 mm")]


# ---------------------------------------------------------------- icons (film 1 look)

def icon(kind, s=1.0):
    if kind == "alga":
        return VGroup(Circle(0.3 * s, stroke_color="#2E7D32", stroke_width=3, fill_color=GREEN, fill_opacity=1),
                      Circle(0.09 * s, stroke_width=0, fill_color="#B7E4A0", fill_opacity=0.9).shift(UL * 0.1 * s))
    if kind == "para":
        body = Ellipse(width=1.0 * s, height=0.42 * s, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.55)
        hairs = VGroup()
        for th in np.linspace(0, 2 * np.pi, 26, endpoint=False):
            p = np.array([0.5 * s * np.cos(th), 0.21 * s * np.sin(th), 0])
            n = np.array([np.cos(th) * 0.5, np.sin(th) * 0.21, 0])
            n = n / np.linalg.norm(n)
            hairs.add(Line(p, p + n * 0.09 * s, color=TEAL, stroke_width=2))
        return VGroup(body, hairs)
    raise ValueError(kind)


def microscope(h=2.8):
    s = h / 2.8
    col = STEEL
    base = RoundedRectangle(corner_radius=0.08, width=1.7, height=0.2, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.8).move_to([0, -1.4, 0])
    arm = VMobject(color=col, stroke_width=14)
    arm.set_points_smoothly([[0.55, -1.3, 0], [0.9, -0.6, 0], [0.85, 0.3, 0], [0.4, 0.95, 0]])
    tube = Line([0.18, 1.2, 0], [-0.12, -0.05, 0], color=col, stroke_width=30)
    eyep = Line([0.2, 1.25, 0], [0.26, 1.55, 0], color=col, stroke_width=16)
    obj = Line([-0.13, -0.05, 0], [-0.16, -0.3, 0], color=TEAL, stroke_width=12)
    stage = Line([-0.75, -0.7, 0], [0.6, -0.7, 0], color=col, stroke_width=9)
    slide = Rectangle(width=0.7, height=0.07, stroke_width=0, fill_color=PAPER, fill_opacity=0.9).move_to([-0.2, -0.62, 0])
    g = VGroup(base, arm, stage, slide, tube, eyep, obj)
    g.scale(s)
    g.lens = obj
    return g


def wobble(m, amp=0.04, w=1.3, ph=0.0):
    base = m.get_center().copy()
    t = [ph]

    def u(mm, dt):
        t[0] += dt
        mm.move_to(base + np.array([amp * np.sin(w * t[0] + ph), amp * np.cos(1.3 * w * t[0] + ph), 0]))
    m.add_updater(u)
    return m


def swim(m, c, rx, ry, w, ph):
    """A swimmer wandering on a smooth closed path around c, turning to face where it is going."""
    t = [0.0]
    prev = [0.0]

    def pos(tt):
        return np.array([c[0] + rx * np.sin(w * tt + ph), c[1] + ry * np.sin(1.31 * w * tt + 2.1 * ph), 0])

    m.move_to(pos(0))

    def u(mm, dt):
        t[0] += dt
        p, q = pos(t[0]), pos(t[0] + 0.05)
        ang = np.arctan2(q[1] - p[1], q[0] - p[0])
        mm.rotate(ang - prev[0])
        prev[0] = ang
        mm.move_to(p)
    m.add_updater(u)
    return m


def view_circle(c=C, r=RV):
    """A microscope view: white circle, black rim."""
    c = np.array([c[0], c[1], 0])
    rim = Circle(r, stroke_color="#0B0D12", stroke_width=12, fill_color=PAPER, fill_opacity=0.96).move_to(c)
    ring = Circle(r + 0.09, stroke_color=STEEL, stroke_width=2.5).move_to(c)
    return VGroup(rim, ring)


def cork_boxes(c=C, r=RV, bw=0.72, bh=0.54, wall=3.0):
    """Rows of hollow TAN boxes, staggered like a honeycomb, all inside the view."""
    boxes = []
    for j in range(-5, 6):
        y = c[1] + j * bh
        off = 0.5 * bw if j % 2 else 0.0
        for i in range(-6, 7):
            x = c[0] + i * bw + off
            ok = all(np.hypot(x + sx * bw / 2 - c[0], y + sy * bh / 2 - c[1]) <= r - 0.1 for sx in (-1, 1) for sy in (-1, 1))
            if ok:
                boxes.append((j, Rectangle(width=bw, height=bh, stroke_color=TAN_D, stroke_width=wall,
                                           fill_color=TAN, fill_opacity=0.22).move_to([x, y, 0])))
    rows = {}
    for j, b in boxes:
        rows.setdefault(j, VGroup()).add(b)
    g = VGroup(*[rows[j] for j in sorted(rows)])
    return g


def ghost(box):
    """A ghostly living cell inside one box."""
    cx, cy = box.get_center()[:2]
    body = Ellipse(width=0.46, height=0.32, stroke_color="#6B7A99", stroke_width=2.5, fill_color="#8D9BBA", fill_opacity=0.55)
    nuc = Dot(radius=0.07, color="#4A5878")
    return VGroup(body, nuc).move_to([cx, cy, 0])


def cork_card(s=1.0):
    g = VGroup(RoundedRectangle(corner_radius=0.1, width=0.8 * s, height=0.8 * s, stroke_color=TAN_D, stroke_width=3,
                                fill_color=PAPER, fill_opacity=1))
    for dx in (-0.17, 0.17):
        for dy in (-0.17, 0.17):
            g.add(Square(0.3 * s, stroke_color=TAN_D, stroke_width=3, fill_color=TAN, fill_opacity=0.35).move_to([dx * s, dy * s, 0]))
    return g


def stopper(s=1.0):
    body = RoundedRectangle(corner_radius=0.12 * s, width=1.2 * s, height=1.7 * s, stroke_color=TAN_D, stroke_width=4,
                            fill_color=TAN, fill_opacity=0.95)
    top = Ellipse(width=1.2 * s, height=0.32 * s, stroke_color=TAN_D, stroke_width=3, fill_color="#E3CBA2", fill_opacity=1).move_to(body.get_top())
    dots = VGroup(*[Dot(radius=0.045 * s, color=TAN_D).move_to(body.get_center() + np.array([dx * s, dy * s, 0]))
                    for dx, dy in [(-0.3, 0.3), (0.25, 0.5), (0.1, -0.1), (-0.25, -0.4), (0.3, -0.5), (-0.05, 0.6), (0.35, 0.05)]])
    return VGroup(body, dots, top)


def book(s=1.0):
    l = RoundedRectangle(corner_radius=0.05, width=0.95 * s, height=1.2 * s, stroke_color=STEEL, stroke_width=3, fill_color=PAPER, fill_opacity=1).shift(LEFT * 0.48 * s)
    r = RoundedRectangle(corner_radius=0.05, width=0.95 * s, height=1.2 * s, stroke_color=STEEL, stroke_width=3, fill_color=PAPER, fill_opacity=1).shift(RIGHT * 0.48 * s)
    sp = Line(l.get_corner(UR), l.get_corner(DR), color=STEEL, stroke_width=4)
    return VGroup(l, r, sp)


def book_lines(bk):
    out = VGroup()
    l, r = bk[0], bk[1]
    for side in (l, r):
        cx, cy = side.get_center()[:2]
        for k in range(4):
            y = cy + 0.4 - k * 0.27
            out.add(Line([cx - 0.3, y, 0], [cx + 0.3 - 0.07 * (k % 2) * 3, y, 0], color="#6B7A99", stroke_width=2.5))
    return out


def tree(s=1.0):
    return VGroup(Rectangle(width=0.22 * s, height=0.6 * s, stroke_width=0, fill_color="#8B6B4A", fill_opacity=1).shift(DOWN * 0.45 * s),
                  Circle(0.52 * s, stroke_color="#2E7D32", stroke_width=3, fill_color=GREEN, fill_opacity=0.85).shift(UP * 0.2 * s))


def dog(s=1.0):
    col = "#C9A27A"
    body = Ellipse(width=1.0 * s, height=0.5 * s, stroke_color="#8A6A45", stroke_width=3, fill_color=col, fill_opacity=1)
    head = Circle(0.26 * s, stroke_color="#8A6A45", stroke_width=3, fill_color=col, fill_opacity=1).move_to([0.5 * s, 0.3 * s, 0])
    ear = Ellipse(width=0.14 * s, height=0.28 * s, stroke_width=0, fill_color="#8A6A45", fill_opacity=1).move_to([0.42 * s, 0.42 * s, 0])
    eye = Dot(radius=0.03 * s, color=INK).move_to([0.58 * s, 0.34 * s, 0])
    legs = VGroup(*[Line([x * s, -0.2 * s, 0], [x * s, -0.55 * s, 0], color="#8A6A45", stroke_width=5) for x in (-0.3, -0.12, 0.2, 0.38)])
    tail = Line([-0.48 * s, 0.05 * s, 0], [-0.7 * s, 0.35 * s, 0], color="#8A6A45", stroke_width=5)
    return VGroup(legs, tail, body, head, ear, eye)


def mushroom(s=1.0):
    cap = Arc(radius=0.5 * s, start_angle=0, angle=PI, stroke_color="#A9694F", stroke_width=3, fill_color="#D98E73", fill_opacity=1)
    cap.add(Line(cap.get_start(), cap.get_end(), color="#A9694F", stroke_width=3))
    cap.shift(UP * 0.12 * s)
    stem = Rectangle(width=0.3 * s, height=0.5 * s, stroke_color="#B9B09A", stroke_width=2, fill_color="#EDE6D5", fill_opacity=1).shift(DOWN * 0.2 * s)
    spots = VGroup(*[Dot(radius=0.05 * s, color="#F5E6DC").move_to([x * s, y * s, 0]) for x, y in [(-0.2, 0.3), (0.1, 0.4), (0.25, 0.22)]])
    return VGroup(stem, cap, spots)


def waterdrop(s=1.0):
    d = Circle(0.38 * s, stroke_color="#BFE6F2", stroke_width=3, fill_color=BLUE, fill_opacity=0.55).shift(DOWN * 0.1 * s)
    tip = Polygon([-0.3 * s, 0.08 * s, 0], [0.3 * s, 0.08 * s, 0], [0, 0.78 * s, 0], stroke_color="#BFE6F2", stroke_width=3,
                  fill_color=BLUE, fill_opacity=0.55)
    return VGroup(tip, d)


def cell(r=0.5, nuc=True):
    g = VGroup(Circle(r, stroke_color=CELLC, stroke_width=3.5, fill_color=CELLC, fill_opacity=0.35))
    if nuc:
        g.add(Dot(radius=r * 0.3, color=CELLD).shift(UR * r * 0.15))
    return g


def dividing(tp, ts, c, R):
    """One round cell that elongates, pinches in the middle (tp 0..1) and splits apart (ts distance)."""
    def build():
        p, s = tp.get_value(), ts.get_value()
        L = R * (1 + 0.6 * p)

        def h(x):
            return R * max(1 - abs(x / L) ** (2 + 0.9 * p), 0.0) ** (0.5 - 0.12 * p) * (1 - p * np.exp(-(x / (0.38 * L)) ** 2))
        g = VGroup()
        sty = dict(stroke_color=CELLC, stroke_width=4, fill_color=CELLC, fill_opacity=0.35)
        if p < 0.999:
            xs = np.linspace(-L, L, 120)
            pts = [[c[0] + x, c[1] + h(x), 0] for x in xs] + [[c[0] + x, c[1] - h(x), 0] for x in xs[::-1]]
            g.add(VMobject(**sty).set_points_as_corners(pts + [pts[0]]))
        else:
            for sg in (-1, 1):
                xs = np.linspace(0, sg * L, 80)
                ups = [[c[0] + sg * s + x, c[1] + h(x), 0] for x in xs]
                lows = [[c[0] + sg * s + x, c[1] - h(x), 0] for x in xs[::-1]]
                pts = ups + lows
                g.add(VMobject(**sty).set_points_as_corners(pts + [pts[0]]))
        for sg in (-1, 1):
            g.add(Dot([c[0] + sg * (0.5 * L * p + s), c[1], 0], radius=0.2 * R + 0.04, color=CELLD))
        return g
    return always_redraw(build)


def beaker(c=(0.2, 0.3), w=2.6, h=3.6, fluid=1.0):
    cx, cy = c
    wall = VMobject(stroke_color="#9FD3E6", stroke_width=5)
    wall.set_points_as_corners([[cx - w / 2 - 0.15, cy + h / 2 + 0.05, 0], [cx - w / 2, cy + h / 2, 0], [cx - w / 2, cy - h / 2, 0],
                                [cx + w / 2, cy - h / 2, 0], [cx + w / 2, cy + h / 2, 0], [cx + w / 2 + 0.15, cy + h / 2 + 0.05, 0]])
    fh = (h - 0.25) * fluid
    fl = Rectangle(width=w - 0.1, height=max(fh, 0.01), stroke_width=0, fill_color=BLUE, fill_opacity=0.22)
    fl.move_to([cx, cy - h / 2 + 0.05 + fh / 2, 0])
    return VGroup(fl, wall)


BEAKER_CELLS = [(-0.6, -0.9, 0.3), (0.5, -1.15, 0.26), (0.0, -0.2, 0.34), (-0.55, 0.6, 0.27), (0.55, 0.35, 0.3), (0.05, 1.05, 0.25)]


def rule_panel_parts():
    ttl = T("The cell theory", 26, TEAL, weight=BOLD)
    groups = []
    for t in LINES:
        txt = T(t, 24, GREY)
        box = RoundedRectangle(corner_radius=0.14, width=2.95, height=txt.height + 0.34, stroke_color=GREY, stroke_width=2.5,
                               fill_color=GREY, fill_opacity=0.06).move_to(txt)
        groups.append(VGroup(box, txt))
    col = VGroup(*groups).arrange(DOWN, buff=0.3)
    ttl.next_to(col, UP, buff=0.3)
    allp = VGroup(ttl, col)
    allp.move_to([5.25, 0.15, 0])
    if allp.height > 6.4:
        allp.scale(6.4 / allp.height).move_to([5.25, 0.15, 0])
    return ttl, groups


class CH(SpokenScene):
    """A scene with the carried frame: size ladder (left), timeline (bottom), the theory panel (right)."""

    def chrome(self, marker=None, lit=(), parts=("ladder", "tl", "panel"), add=True):
        axis = Line([AX, Y(0.1), 0], [AX, Y(10000), 0], color=STEEL, stroke_width=5)
        ticks = [Line([AX - 0.14, Y(v), 0], [AX + 0.14, Y(v), 0], color=STEEL, stroke_width=4) for v, _ in RUNGS]
        labs = []
        for v, t in RUNGS:
            lab = T(t, 22, TEXT)
            lab.move_to([AX - 0.22 - lab.width / 2, Y(v), 0])
            labs.append(lab)
        self.eye = Line([AX, Y(100), 0], [EYE_X1, Y(100), 0], color=BLUE, stroke_width=8)
        el = T("eye line", 24, BLUE, weight=BOLD)
        el.move_to([AX - 0.22 - el.width / 2, Y(100) + 0.4, 0])
        tag = T("schematic", 22, GREY).move_to([-5.7, 3.62, 0])
        self.ladder = VGroup(axis, *ticks, *labs, self.eye, el, tag)
        # timeline
        self.tl_line = Line([TL_X0, TLY, 0], [TL_X1, TLY, 0], color=STEEL, stroke_width=5)
        self.tl_ticks = VGroup(*[Line([x, TLY - 0.1, 0], [x, TLY + 0.1, 0], color=STEEL, stroke_width=4) for x in TX])
        self.tl_labs = [T(t, 24, TEXT).move_to([x, TLY + 0.4, 0]) for x, t in zip(TX, TLAB)]
        self.prog = Line([TL_X0, TLY, 0], [TL_X0, TLY, 0], color=YELLOW, stroke_width=8)
        self.dot = Dot(radius=0.15, color=YELLOW).move_to([TL_X0, TLY, 0])
        self.marker = None
        if marker is not None:
            self.prog.put_start_and_end_on([TL_X0, TLY, 0], [TX[marker], TLY, 0])
            self.dot.move_to([TX[marker], TLY, 0])
            self.tl_labs[marker].set_color(YELLOW)
            self.marker = marker
        else:
            self.dot.set_opacity(0)
        self.tl = VGroup(self.tl_line, self.prog, self.tl_ticks, *self.tl_labs, self.dot)
        # panel
        self.ptitle, self.pgroups = rule_panel_parts()
        self.lit = set()
        for i in lit:
            self.set_lit(i)
        self.panel = VGroup(self.ptitle, *self.pgroups)
        if add:
            if "ladder" in parts:
                self.add(self.ladder)
            if "tl" in parts:
                self.add(self.tl)
            if "panel" in parts:
                self.add(self.panel)

    def set_lit(self, i):
        g = self.pgroups[i]
        g[1].set_color(YELLOW)
        g[0].set_stroke(YELLOW, 4).set_fill(YELLOW, 0.12)
        self.lit.add(i)

    def light(self, i, run_time=1.0):
        g = self.pgroups[i]
        self.lit.add(i)
        self.play(g[1].animate.set_color(YELLOW), g[0].animate.set_stroke(YELLOW, 4).set_fill(YELLOW, 0.12), run_time=run_time)
        self.play(Indicate(g, color=YELLOW, scale_factor=1.06), run_time=0.8)

    def move_marker(self, j, run_time=1.0):
        anims = [self.prog.animate.put_start_and_end_on([TL_X0, TLY, 0], [TX[j], TLY, 0]),
                 self.dot.animate.move_to([TX[j], TLY, 0]).set_opacity(1),
                 self.tl_labs[j].animate.set_color(YELLOW)]
        if self.marker is not None and self.marker != j:
            anims.append(self.tl_labs[self.marker].animate.set_color(TEXT))
        self.marker = j
        self.play(*anims, run_time=run_time)


# ---------------------------------------------------------------- scene builders shared between scenes

def make_s02_end():
    stp = stopper(0.8).move_to([-2.4, -0.4, 0])
    bk = book(1.0).move_to([-2.3, 2.2, 0])
    lines = book_lines(bk)
    sc = microscope(3.4).move_to([2.2, 0.4, 0])
    plate = RoundedRectangle(corner_radius=0.03, width=1.1, height=0.1, stroke_color=PAPER, stroke_width=2,
                             fill_color="#0B0D12", fill_opacity=1).move_to([1.96, -0.37, 0])
    slc = Ellipse(width=0.85, height=0.08, stroke_color=TAN_D, stroke_width=2, fill_color=TAN, fill_opacity=1).move_to([1.96, -0.29, 0])
    beam = VGroup(Polygon([1.75, -1.2, 0], [2.25, -1.2, 0], [2.45, -0.42, 0], [1.5, -0.42, 0], stroke_width=0, fill_color=YELLOW, fill_opacity=0.35),
                  Polygon([1.5, -0.3, 0], [2.45, -0.3, 0], [2.04, 0.0, 0], [1.9, 0.0, 0], stroke_width=0, fill_color=YELLOW, fill_opacity=0.3))
    return stp, bk, lines, sc, plate, slc, beam


def make_s08_calendar():
    pages = VGroup()
    for k in range(5):
        pg = VGroup(RoundedRectangle(corner_radius=0.1, width=2.1, height=2.1, stroke_color=STEEL, stroke_width=3, fill_color=PAPER, fill_opacity=1),
                    Rectangle(width=2.1, height=0.4, stroke_width=0, fill_color=STEEL, fill_opacity=1).shift(UP * 0.85))
        pages.add(pg)
    return pages


class S00Title(TitleCard):
    LESSON = "Cells Are Everywhere"
    TITLE = "A Theory Built in Steps"


# ---------------------------------------------------------------- s01

class S01Question(CH):
    def construct(self):
        self.chrome(marker=None, parts=(), add=False)
        self.play(FadeIn(self.ladder), FadeIn(self.tl), run_time=1.0)
        self.at("three parts")
        self.play(FadeIn(self.ptitle, shift=DOWN * 0.1), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(g, shift=LEFT * 0.2) for g in self.pgroups], lag_ratio=0.5), run_time=1.8)
        self.at("But how")
        row = VGroup(tree(1.35), dog(1.35), mushroom(1.35), waterdrop(1.35))
        for g, x in zip(row, [-2.2, -0.6, 1.0, 2.6]):
            g.move_to([x, -0.6, 0])
        self.play(LaggedStart(*[FadeIn(g, shift=UP * 0.3, scale=0.6) for g in row], lag_ratio=0.3), run_time=1.3)
        for i, g in enumerate(row):
            wobble(g, 0.05, 1.1 + 0.2 * i, i)
        self.at("come to know")
        q = T("?", 190, TEXT, weight=BOLD).move_to([0.2, 1.75, 0])
        q.t = 0.0

        def qp(m, dt):
            m.t += dt
            m.set_opacity(0.7 + 0.3 * np.sin(3 * m.t))
        q.add_updater(qp)
        self.play(FadeIn(q, scale=0.4), run_time=0.8)
        self.at("Seeing cells")
        self.play(LaggedStart(*[Indicate(g, color=YELLOW, scale_factor=1.12) for g in row], lag_ratio=0.35), run_time=2.2)
        self.at("It started")
        for g in row:
            g.clear_updaters()
        q.clear_updaters()
        stp = stopper(1.5).move_to([0.2, 0.3, 0])
        self.play(FadeOut(row), FadeOut(q), GrowFromCenter(stp), run_time=1.1)
        self.at("slice of cork")
        self.play(Indicate(stp, color=YELLOW, scale_factor=1.08), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------- s02

class S02Hooke(CH):
    def construct(self):
        self.chrome(marker=None)
        stp = stopper(1.5).move_to([0.2, 0.3, 0])
        self.add(stp)
        _, bk, lines, sc, plate, slc, beam = make_s02_end()
        self.at("In 1665")
        self.move_marker(0, 1.0)
        self.at("Robert Hooke published")
        self.play(stp.animate.scale(0.8 / 1.5).move_to([-2.4, -0.4, 0]), FadeIn(bk, shift=DOWN * 0.3), run_time=1.2)
        self.at("drawings")
        self.play(Create(lines), run_time=1.6)
        self.at("microscope")
        self.play(FadeIn(sc, shift=LEFT * 0.4), run_time=1.1)
        self.add(plate)
        self.play(FadeIn(plate), run_time=0.4)
        self.at("He cut")
        knife = VGroup(Polygon([0, 0, 0], [0.9, 0, 0], [0.9, -0.12, 0], [0.1, -0.1, 0], stroke_width=0, fill_color=STEEL, fill_opacity=1),
                       Rectangle(width=0.5, height=0.14, stroke_width=0, fill_color="#8B6B4A", fill_opacity=1).shift(RIGHT * 1.15 + DOWN * 0.03))
        knife.move_to([-3.2, 0.42, 0])
        self.add(knife)
        self.play(knife.animate.shift(RIGHT * 1.75), run_time=1.0, rate_func=smooth)
        self.at("thin slice")
        sl = Ellipse(width=0.95, height=0.1, stroke_color=TAN_D, stroke_width=2, fill_color=TAN, fill_opacity=1).move_to([-2.4, 0.38, 0])
        self.add(sl)
        self.play(knife.animate.shift(RIGHT * 1.1 + UP * 0.2).set_opacity(0), sl.animate.shift(UP * 0.35), run_time=0.8)
        self.at("cork and")
        path = ArcBetweenPoints(sl.get_center(), slc.get_center(), angle=-0.6)
        self.play(MoveAlongPath(sl, path), run_time=1.3)
        self.at("shone light")
        self.add(slc)
        self.remove(sl)
        beam.set_opacity(0)
        self.add(beam)
        self.play(beam[0].animate.set_fill(opacity=0.38), beam[1].animate.set_fill(opacity=0.34), run_time=1.0)
        beam.t = 0.0

        def flick(m, dt):
            m.t += dt
            m[0].set_fill(opacity=0.33 + 0.07 * np.sin(4 * m.t))
        beam.add_updater(flick)
        self.finish()


# ---------------------------------------------------------------- s03

class S03Boxes(CH):
    def construct(self):
        self.chrome(marker=0)
        stp, bk, lines, sc, plate, slc, beam = make_s02_end()
        self.add(stp, bk, lines, sc, plate, slc, beam)
        circ = view_circle()
        circ.scale(0.1).move_to(slc)
        self.add(circ)
        self.remove(slc)
        self.play(FadeOut(stp), FadeOut(bk), FadeOut(lines), FadeOut(sc), FadeOut(plate), FadeOut(beam),
                  circ.animate.scale(10).move_to(C), run_time=0.8)
        boxes = cork_boxes()
        self.at("tiny spaces")
        self.play(LaggedStart(*[FadeIn(r, scale=0.8) for r in boxes], lag_ratio=0.3), run_time=1.5)
        self.at("thin walls")
        self.play(LaggedStart(*[Indicate(r, color="#7A5A22", scale_factor=1.0) for r in boxes], lag_ratio=0.06), run_time=1.9)
        self.at("honeycomb")
        self.play(LaggedStart(*[Indicate(r, color=YELLOW, scale_factor=1.0) for r in boxes], lag_ratio=0.05), run_time=1.8)
        self.at("He called")
        lab = chip("cells", YELLOW, 40, pad=0.2, fill_opacity=0.9)
        lab[0].set_fill(INK, 0.95)
        lab.move_to(C)
        self.play(FadeIn(lab, scale=0.5), run_time=0.6)
        self.at("Under his lens")
        card = cork_card(1.0).move_to([-3.85, Y(10), 0])
        card.set_z_index(10)
        self.play(FadeOut(lab), FadeIn(card, shift=UP * 0.2), run_time=0.7)
        self.at("crossed")
        self.play(card.animate.move_to([-3.85, Y(300), 0]), run_time=1.6, rate_func=smooth)
        self.play(Indicate(self.eye, color=BLUE, scale_factor=1.0), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------- s04 / s05

def build_predict_world(scene):
    circ = view_circle()
    boxes = cork_boxes()
    card = cork_card(1.0).move_to([-3.85, Y(300), 0])
    q = T("?", 120, TEXT, weight=BOLD).move_to([-2.75, 0.2, 0])
    pp = T("Pause and predict", 34, YELLOW, weight=BOLD).move_to([0.2, 3.0, 0])
    return circ, boxes, card, q, pp


class S04Predict(CH):
    def construct(self):
        self.chrome(marker=0)
        circ, boxes, card, q, pp = build_predict_world(self)
        self.add(circ, boxes, card)
        tr = tree(1.3).move_to([-2.5, 2.0, 0])
        self.at("Cork comes")
        self.play(FadeIn(tr, shift=UP * 0.3), run_time=0.8)
        self.play(Indicate(tr, color=YELLOW, scale_factor=1.12), run_time=1.0)
        self.at("Look closely")
        self.play(FadeOut(tr), LaggedStart(*[Indicate(r, color=YELLOW, scale_factor=1.0) for r in boxes], lag_ratio=0.3), run_time=2.4)
        self.at("Were")
        self.play(FadeIn(q, scale=0.4), FadeIn(pp, shift=DOWN * 0.1), run_time=0.8)
        self.play(Indicate(q, color=YELLOW, scale_factor=1.12), run_time=1.0)
        self.finish()


class S05Pause(CH):
    def construct(self):
        self.chrome(marker=0)
        circ, boxes, card, q, pp = build_predict_world(self)
        self.add(circ, boxes, card, q, pp)
        q.t = 0.0

        def qp(m, dt):
            m.t += dt
            m.set_opacity(0.6 + 0.4 * np.sin(3.5 * m.t))
        q.add_updater(qp)
        pp.t = 0.0

        def pu(m, dt):
            m.t += dt
            m.set_opacity(0.75 + 0.25 * np.sin(2.0 * m.t))
        pp.add_updater(pu)
        # the boxes shimmer slowly (empty, still, waiting)
        for k, r in enumerate(boxes.family_members_with_points()):
            r.t = 0.4 * k

            def sh(m, dt):
                m.t += dt
                m.set_fill(TAN, 0.18 + 0.1 * np.sin(1.6 * m.t))
            r.add_updater(sh)
        bar = Line([TL_X0, -3.7, 0], [6.7, -3.7, 0], color=YELLOW, stroke_width=7)
        self.add(bar)
        self.play(Transform(bar, Line([6.7, -3.7, 0], [6.7, -3.7, 0], color=YELLOW, stroke_width=7)),
                  run_time=self.narration_s - 0.3, rate_func=linear)
        self.finish()


# ---------------------------------------------------------------- s06

class S06Reveal(CH):
    def construct(self):
        self.chrome(marker=0)
        circ = view_circle()
        boxes = cork_boxes()
        card = cork_card(1.0).move_to([-3.85, Y(300), 0])
        self.add(circ, boxes, card)
        allb = list(boxes.family_members_with_points())
        target = min(allb, key=lambda b: np.hypot(*(b.get_center()[:2] - C[:2] - np.array([0.3, 0.2]))))
        lab = T("dead cells", 32, YELLOW, weight=BOLD).move_to([0.2, -2.25, 0])
        self.at("dead")
        self.play(target.animate.set_stroke(YELLOW, 6), run_time=0.5)
        g = ghost(target)
        self.play(FadeIn(g, scale=0.6), FadeIn(lab, shift=UP * 0.1), run_time=0.9)
        self.play(Indicate(g, color=YELLOW, scale_factor=1.15), run_time=0.9)
        self.at("Only their walls")
        lab2 = T("walls only", 32, YELLOW, weight=BOLD).move_to(lab)
        self.play(FadeOut(g), target.animate.set_stroke(TAN_D, 3.5), Transform(lab, lab2), run_time=1.0)
        self.play(*[r.animate.set_stroke("#7A5A22", 6) for r in allb], run_time=1.0)
        self.at("saw the outside")
        self.play(*[r.animate.set_stroke(YELLOW, 6) for r in allb], run_time=1.2)
        self.play(*[r.animate.set_stroke("#7A5A22", 6) for r in allb], run_time=0.8)
        self.at("living parts")
        gs = VGroup(*[ghost(b) for b in allb])
        gs.set_opacity(0)
        self.add(gs)
        lab3 = T("not seen", 32, YELLOW, weight=BOLD).move_to(lab)
        self.play(gs.animate.set_opacity(0.45), Transform(lab, lab3), run_time=1.3)
        self.play(gs.animate.set_opacity(0.25), run_time=1.5)
        self.finish()


# ---------------------------------------------------------------- s07

def make_letter():
    card = RoundedRectangle(corner_radius=0.1, width=3.0, height=2.1, stroke_color=STEEL, stroke_width=3, fill_color=PAPER, fill_opacity=1)
    yr = T("1676", 34, INK, weight=BOLD).move_to(card.get_top() + DOWN * 0.4)
    ln = VGroup(*[Line([-1.1, 0.35 - k * 0.32, 0], [1.1 - 0.2 * (k % 2), 0.35 - k * 0.32, 0], color="#6B7A99", stroke_width=2.5) for k in range(4)])
    ln.move_to(card.get_center() + DOWN * 0.25)
    return VGroup(card, yr, ln)


def make_swimmers(c=C, spread=1.35):
    sw = VGroup()
    specs = [("para", 0.95, 1.2, 0.8, 0.9, 0.0), ("alga", 1.1, 0.8, 1.0, 1.2, 1.3), ("para", 0.95, 0.9, 1.1, 0.7, 2.4),
             ("alga", 1.2, 1.2, 0.7, 1.0, 3.7), ("para", 0.95, 1.0, 1.0, 1.1, 4.8), ("alga", 1.0, 0.6, 1.1, 1.3, 5.9)]
    for kind, sc, rx, ry, w, ph in specs:
        m = icon(kind, sc)
        swim(m, c, rx * spread / 1.35 * 1.2, ry * spread / 1.35 * 1.2, w, ph)
        sw.add(m)
    return sw


class S07Leeuwenhoek(CH):
    def construct(self):
        self.chrome(marker=0)
        self.at("In a letter")
        letter = make_letter().move_to([0.2, 0.7, 0])
        self.play(FadeIn(letter, shift=UP * 0.3), run_time=0.8)
        self.at("1676")
        self.move_marker(1, 1.0)
        self.play(Create(letter[2]), run_time=1.0)
        self.at("Antoni")
        name = T("Leeuwenhoek", 30, YELLOW, weight=BOLD).move_to([-2.3, 1.75, 0])
        self.play(letter.animate.scale(0.5).move_to([-2.3, 2.75, 0]), FadeIn(name, shift=UP * 0.1), run_time=1.0)
        self.at("described")
        drop = waterdrop(1.8).move_to([0.2, 0.4, 0])
        self.play(FadeIn(drop, scale=0.5), run_time=0.9)
        wobble(drop, 0.06, 1.2, 0)
        self.wait(1.6)
        self.at("He used")
        drop.clear_updaters()
        plate = RoundedRectangle(corner_radius=0.08, width=2.4, height=1.5, stroke_color="#7A5A22", stroke_width=4,
                                 fill_color="#B8893D", fill_opacity=1)
        hole = Circle(0.22, stroke_color="#4A3512", stroke_width=5, fill_color="#CFE9F2", fill_opacity=0.9)
        glint = Dot(radius=0.05, color=PAPER).shift(UL * 0.08)
        rivets = VGroup(*[Dot(radius=0.06, color="#7A5A22").move_to(p) for p in [[-1.0, 0.6, 0], [1.0, 0.6, 0], [-1.0, -0.6, 0], [1.0, -0.6, 0]]])
        brass = VGroup(plate, rivets, hole, glint).move_to([1.7, 0.1, 0])
        eye = VGroup(Ellipse(width=1.3, height=0.7, stroke_color=TEXT, stroke_width=4, fill_color=PAPER, fill_opacity=1),
                     Circle(0.24, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.9), Dot(radius=0.1, color=BG)).move_to([1.7, 2.0, 0])
        self.play(drop.animate.scale(0.6).move_to([-1.6, 0.0, 0]), FadeIn(brass, shift=LEFT * 0.4), run_time=1.1)
        self.play(FadeIn(eye, shift=DOWN * 0.2), run_time=0.7)
        self.at("single tiny lens")
        one = T("one tiny lens", 30, YELLOW, weight=BOLD).move_to([1.7, -1.35, 0])
        self.play(FadeIn(one, shift=UP * 0.1), Indicate(hole, color=YELLOW, scale_factor=1.8), run_time=1.1)
        self.play(Indicate(hole, color=YELLOW, scale_factor=1.8), run_time=0.9)
        self.at("Water from")
        well = T("well water", 32, BLUE, weight=BOLD).move_to([0.2, -1.5, 0])
        self.play(FadeOut(letter), FadeOut(name), FadeOut(brass), FadeOut(eye), FadeOut(one),
                  drop.animate.scale(1 / 0.6).move_to([0.2, 0.4, 0]), FadeIn(well, shift=UP * 0.1), run_time=1.1)
        wobble(drop, 0.06, 1.2, 0)
        self.at("clear")
        self.play(Indicate(drop, color=YELLOW, scale_factor=1.1), run_time=1.0)
        self.at("yet he")
        drop.clear_updaters()
        circ = view_circle()
        circ.scale(0.2).move_to(drop)
        self.add(circ)
        self.play(FadeOut(well), FadeOut(drop), circ.animate.scale(5).move_to(C), run_time=1.1)
        sw = make_swimmers()
        sw.set_opacity(0)
        self.add(sw)
        self.at("many tiny")
        self.play(sw.animate.set_opacity(1), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------- s08

C8 = np.array([1.3, 0.7, 0])
R8 = 1.9


class S08Rainwater(CH):
    def construct(self):
        self.chrome(marker=1)
        circ = view_circle()
        sw = make_swimmers()
        self.add(circ, sw)
        # carry the view from film's last scene, then reshape it to make room
        dish = VGroup(Ellipse(width=3.2, height=0.9, stroke_color="#9FD3E6", stroke_width=5, fill_color=BLUE, fill_opacity=0.3),
                      Ellipse(width=2.6, height=0.5, stroke_width=0, fill_color=BLUE, fill_opacity=0.35).shift(UP * 0.08)).move_to([-1.6, -1.8, 0])
        pages = make_s08_calendar()
        texts = ["nothing", "nothing", "nothing", "30 May", "31 May"]
        # build stack: first page on top
        pgs = []
        for k, t in enumerate(texts):
            pg = make_s08_calendar()[0].copy() if False else VGroup(
                RoundedRectangle(corner_radius=0.1, width=2.1, height=2.1, stroke_color=STEEL, stroke_width=3, fill_color=PAPER, fill_opacity=1),
                Rectangle(width=2.0, height=0.38, stroke_width=0, fill_color=STEEL, fill_opacity=1).shift(UP * 0.85),
                T(t, 30, INK, weight=BOLD).shift(DOWN * 0.15))
            if len(t) > 7:
                fit(pg[2], max_w=1.8)
            pg.move_to([-2.1, 1.5, 0])
            pgs.append(pg)
        stack = VGroup(*reversed(pgs))
        self.play(FadeOut(sw), circ.animate.scale(R8 / RV).move_to(C8), FadeIn(dish, shift=UP * 0.2), FadeIn(stack), run_time=0.9)
        wobble(dish, 0.04, 1.0, 0)

        def flip(k, rt=0.6):
            self.play(pgs[k].animate.shift(UP * 0.4 + LEFT * 0.4).rotate(0.35).set_opacity(0), run_time=rt)
        self.at("again and again")
        flip(0, 0.7)
        self.wait(0.3)
        flip(1, 0.7)
        self.at("At first")
        nth = T("nothing", 34, INK, weight=BOLD).move_to(C8)
        self.play(FadeIn(nth, scale=0.8), run_time=0.7)
        self.play(Indicate(nth, color=YELLOW, scale_factor=1.12), run_time=1.0)
        self.at("alive in it")
        self.play(Indicate(circ[0], color=BLUE, scale_factor=1.0), run_time=0.9)
        self.at("Then one day")
        flip(2, 0.7)
        self.play(FadeOut(nth), run_time=0.3)
        self.at("a few tiny")
        s1 = icon("para", 0.9)
        s2 = icon("alga", 1.0)
        swim(s1, C8, 0.8, 0.6, 1.0, 0.3)
        swim(s2, C8, 0.6, 0.8, 1.2, 2.0)
        sw2 = VGroup(s1, s2)
        sw2.set_opacity(0)
        self.add(sw2)
        self.play(sw2.animate.set_opacity(1), run_time=0.9)
        self.at("the next day")
        flip(3, 0.7)
        more = VGroup(*[icon(k, sc) for k, sc in [("para", 0.9), ("alga", 1.0), ("para", 0.9), ("alga", 1.0), ("para", 0.9)]])
        for i, m in enumerate(more):
            swim(m, C8, 0.4 + 0.2 * (i % 3), 0.5 + 0.15 * (i % 2), 0.9 + 0.1 * i, 0.9 * i + 1)
        more.set_opacity(0)
        self.add(more)
        self.at("more")
        self.play(more.animate.set_opacity(1), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------- s09

C9 = np.array([0.2, 1.0, 0])
R9 = 1.9


def blurry(c, r):
    g = VGroup()
    for (dx, dy, rr) in [(-0.7, 0.3, 0.7), (0.4, -0.3, 0.8), (0.6, 0.6, 0.5), (-0.2, -0.7, 0.55)]:
        for k, op in enumerate([0.18, 0.12, 0.08]):
            g.add(Circle(rr * (1 + 0.35 * k), stroke_width=0, fill_color="#7C8AA5", fill_opacity=op).move_to([c[0] + dx, c[1] + dy, 0]))
    return g


class S09Rule(CH):
    def construct(self):
        self.chrome(marker=1)
        circ = view_circle(C9, R9)
        bl = blurry(C9, R9)
        bl.set_opacity(0)
        self.at("When a view")
        self.play(FadeIn(circ, scale=0.6), run_time=0.9)
        self.add(bl)
        self.play(bl.animate.set_opacity(1), run_time=1.0)
        self.at("he said so")
        box = Square(0.6, stroke_color=TEXT, stroke_width=4).move_to([-1.9, -1.75, 0])
        tick = VGroup(Line([-2.1, -1.75, 0], [-1.95, -1.9, 0], color=YELLOW, stroke_width=7), Line([-1.95, -1.9, 0], [-1.65, -1.55, 0], color=YELLOW, stroke_width=7))
        self.play(Create(box), run_time=0.5)
        self.play(Create(tick), run_time=0.5)
        self.at("did not count")
        lab = T("unclear: not counted", 30, YELLOW, weight=BOLD).next_to(box, RIGHT, buff=0.3)
        self.play(FadeIn(lab, shift=RIGHT * 0.2), Indicate(circ[0], color=YELLOW, scale_factor=1.0), run_time=1.0)
        self.at("careful records")
        sheet = VGroup(RoundedRectangle(corner_radius=0.1, width=2.9, height=3.4, stroke_color=STEEL, stroke_width=3, fill_color=PAPER, fill_opacity=1))
        rows = VGroup()
        for k in range(5):
            y = 1.2 - k * 0.6
            rows.add(Line([-1.1, y, 0], [0.7, y, 0], color="#6B7A99", stroke_width=2.5))
            if k % 2 == 0:
                rows.add(VGroup(Line([0.95, y, 0], [1.05, y - 0.1, 0], color=INK, stroke_width=4), Line([1.05, y - 0.1, 0], [1.25, y + 0.18, 0], color=INK, stroke_width=4)))
            else:
                rows.add(T("?", 26, INK, weight=BOLD).move_to([1.1, y, 0]))
        rec = VGroup(sheet, rows).move_to([0.2, 0.9, 0])
        self.play(FadeOut(VGroup(circ, bl, box, tick, lab)), FadeIn(rec, shift=UP * 0.3), run_time=0.9)
        self.play(Create(rows), run_time=1.6)
        self.at("seeing nothing")
        left = VGroup(RoundedRectangle(corner_radius=0.15, width=2.7, height=2.2, stroke_color=TEXT, stroke_width=4, fill_color=BLUE, fill_opacity=0.15),
                      T("I saw\nnothing", 32, TEXT, weight=BOLD)).move_to([-1.7, 0.7, 0])
        right = VGroup(RoundedRectangle(corner_radius=0.15, width=2.7, height=2.2, stroke_color=TEXT, stroke_width=4, fill_color=YELLOW, fill_opacity=0.12),
                       T("nothing\nis there", 32, TEXT, weight=BOLD)).move_to([2.1, 0.7, 0])
        self.play(FadeOut(rec), run_time=0.4)
        self.play(FadeIn(left, shift=RIGHT * 0.3), run_time=0.7)
        self.at("is not the same")
        ne = VGroup(Line([-0.3, 0.88, 0], [0.7, 0.88, 0], color=YELLOW, stroke_width=9), Line([-0.3, 0.52, 0], [0.7, 0.52, 0], color=YELLOW, stroke_width=9),
                    Line([0.0, 1.15, 0], [0.4, 0.25, 0], color=YELLOW, stroke_width=9)).move_to([0.2, 0.7, 0])
        self.play(GrowFromCenter(ne), run_time=0.8)
        self.at("nothing being there")
        self.play(FadeIn(right, shift=LEFT * 0.3), run_time=0.9)
        self.play(Indicate(ne, color=YELLOW, scale_factor=1.25), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------- s10

def plant_circle(c, r=1.45):
    circ = view_circle(c, r)
    boxes = VGroup()
    bw, bh = 0.6, 0.5
    for j in range(-3, 4):
        for i in range(-4, 5):
            x = c[0] + i * bw + (0.5 * bw if j % 2 else 0)
            y = c[1] + j * bh
            if all(np.hypot(x + sx * bw / 2 - c[0], y + sy * bh / 2 - c[1]) <= r - 0.12 for sx in (-1, 1) for sy in (-1, 1)):
                boxes.add(VGroup(Rectangle(width=bw, height=bh, stroke_color="#2E7D32", stroke_width=3, fill_color=GREEN, fill_opacity=0.35).move_to([x, y, 0]),
                                 Dot(radius=0.05, color="#2E7D32").move_to([x + 0.1, y - 0.07, 0])))
    return circ, boxes


def animal_circle(c, r=1.45):
    circ = view_circle(c, r)
    cells = VGroup()
    d = 0.5
    for j in range(-3, 4):
        for i in range(-4, 5):
            x = c[0] + i * d + (0.5 * d if j % 2 else 0)
            y = c[1] + j * d * 0.87
            if np.hypot(x - c[0], y - c[1]) <= r - 0.3:
                cells.add(VGroup(Circle(0.22, stroke_color="#8E6FC2", stroke_width=3, fill_color=CELLC, fill_opacity=0.6).move_to([x, y, 0]),
                                 Dot(radius=0.07, color=CELLD).move_to([x + 0.03, y + 0.02, 0])))
    return circ, cells


def leaf(s=1.0):
    body = Ellipse(width=1.3 * s, height=0.75 * s, stroke_color="#2E7D32", stroke_width=3, fill_color=GREEN, fill_opacity=0.9).rotate(0.4)
    vein = Line([-0.55 * s, -0.2 * s, 0], [0.55 * s, 0.2 * s, 0], color="#2E7D32", stroke_width=3)
    return VGroup(body, vein)


def tissue(s=1.0):
    slab = RoundedRectangle(corner_radius=0.12 * s, width=1.3 * s, height=0.7 * s, stroke_color="#8E6FC2", stroke_width=3, fill_color=CELLC, fill_opacity=0.5)
    dots = VGroup(*[Dot(radius=0.07 * s, color=CELLD).move_to([x * s, y * s, 0]) for x, y in [(-0.4, 0.15), (0, 0.1), (0.4, 0.15), (-0.2, -0.15), (0.2, -0.15)]])
    return VGroup(slab, dots)


class S10PlantsAnimals(CH):
    def construct(self):
        self.chrome(marker=1)
        left = VGroup(RoundedRectangle(corner_radius=0.15, width=2.7, height=2.2, stroke_color=TEXT, stroke_width=4, fill_color=BLUE, fill_opacity=0.15),
                      T("I saw\nnothing", 32, TEXT, weight=BOLD)).move_to([-1.7, 0.7, 0])
        right = VGroup(RoundedRectangle(corner_radius=0.15, width=2.7, height=2.2, stroke_color=TEXT, stroke_width=4, fill_color=YELLOW, fill_opacity=0.12),
                       T("nothing\nis there", 32, TEXT, weight=BOLD)).move_to([2.1, 0.7, 0])
        ne = VGroup(Line([-0.3, 0.88, 0], [0.7, 0.88, 0], color=YELLOW, stroke_width=9), Line([-0.3, 0.52, 0], [0.7, 0.52, 0], color=YELLOW, stroke_width=9),
                    Line([0.0, 1.15, 0], [0.4, 0.25, 0], color=YELLOW, stroke_width=9)).move_to([0.2, 0.7, 0])
        self.add(left, right, ne)
        sc = microscope(3.4).move_to([0.2, 0.4, 0])
        sc.lens.set_stroke(opacity=1)
        self.at("Microscopes")
        self.play(FadeOut(left), FadeOut(right), FadeOut(ne), run_time=0.4)
        self.play(FadeIn(sc, scale=0.8), run_time=0.7)
        sc.t = 0.0

        def glow(m, dt):
            m.t += dt
            m.lens.set_stroke(opacity=0.65 + 0.35 * np.sin(2.4 * m.t))
        sc.add_updater(glow)
        self.at("kept getting")
        self.play(sc.animate.scale(1.15), run_time=2.0, rate_func=smooth)
        self.at("By about")
        self.move_marker(2, 1.0)
        self.wait(1.2)
        self.at("scientists had")
        lc, lcells = plant_circle([-1.5, 0.55])
        ac, acells = animal_circle([2.0, 0.55])
        lf = leaf(1.1).move_to([-1.5, 2.75, 0])
        ts = tissue(1.1).move_to([2.0, 2.75, 0])
        self.at("many plants")
        lc.save_state()
        lc.scale(0.1).move_to(lf)
        self.add(lc)
        plab = T("plants", 32, GREEN, weight=BOLD).move_to([-1.5, -1.5, 0])
        self.play(FadeOut(sc, scale=0.5), FadeIn(lf, shift=DOWN * 0.2), lc.animate.restore(), FadeIn(plab, shift=UP * 0.1), run_time=1.2)
        self.at("animals")
        ac.save_state()
        ac.scale(0.1).move_to(ts)
        self.add(ac)
        alab = T("animals", 32, CELLC, weight=BOLD).move_to([2.0, -1.5, 0])
        self.play(FadeIn(ts, shift=DOWN * 0.2), ac.animate.restore(), FadeIn(alab, shift=UP * 0.1), run_time=1.2)
        self.at("found cells")
        self.play(LaggedStart(*[FadeIn(b, scale=0.5) for b in lcells], lag_ratio=0.06),
                  LaggedStart(*[FadeIn(b, scale=0.5) for b in acells], lag_ratio=0.06), run_time=2.2)
        self.at("strong evidence")
        self.light(0, 1.2)
        self.play(Indicate(plab, color=YELLOW, scale_factor=1.15), Indicate(alab, color=YELLOW, scale_factor=1.15), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------- s11

class S11Fluid(CH):
    def construct(self):
        self.chrome(marker=2, lit=(0,))
        one = cell(0.85).move_to([-0.6, 0.4, 0])
        q = T("?", 190, TEXT, weight=BOLD).move_to([1.7, 0.5, 0])
        q.t = 0.0

        def qp(m, dt):
            m.t += dt
            m.set_opacity(0.7 + 0.3 * np.sin(3 * m.t))
        q.add_updater(qp)
        self.at("But where")
        self.play(FadeIn(one, scale=0.5), run_time=0.8)
        self.at("new cells come")
        self.play(FadeIn(q, scale=0.4), run_time=0.7)
        self.play(Indicate(one, color=YELLOW, scale_factor=1.15), run_time=1.0)
        self.at("At first")
        q.clear_updaters()
        bk = beaker()
        fl = bk[0]
        fl.save_state()
        fl.stretch_to_fit_height(0.05, about_edge=DOWN)
        self.add(fl)
        self.play(FadeOut(one), FadeOut(q), Create(bk[1]), fl.animate.restore(), run_time=1.3)
        old = chip("old idea", YELLOW, 32, pad=0.2).move_to([0.2, 2.8, 0])
        self.at("some scientists")
        self.play(FadeIn(old, shift=DOWN * 0.1), run_time=0.7)
        self.at("new cells formed")
        cells = VGroup()
        for (dx, dy, r) in BEAKER_CELLS:
            cells.add(cell(r).move_to([0.2 + dx, 0.3 + dy, 0]))
        self.play(LaggedStart(*[GrowFromCenter(c) for c in cells], lag_ratio=0.5), run_time=3.4)
        self.at("crystals")
        for i, c in enumerate(cells):
            wobble(c, 0.07, 1.0 + 0.15 * i, i)
        self.play(*[Indicate(c, color=YELLOW, scale_factor=1.0) for c in cells], run_time=1.6)
        self.at("Then a new cell")
        nop = chip("no parent cell needed", YELLOW, 30, pad=0.18).move_to([0.2, -2.0, 0])
        self.play(FadeIn(nop, shift=UP * 0.1), run_time=0.8)
        self.at("That idea")
        self.play(FadeOut(nop), run_time=0.4)
        lens = VGroup(Circle(0.55, stroke_color=STEEL, stroke_width=7, fill_color=BLUE, fill_opacity=0.1),
                      Line([0.4, -0.4, 0], [0.95, -0.95, 0], color=STEEL, stroke_width=11)).move_to([-2.4, 1.4, 0])
        self.play(FadeIn(lens), run_time=0.4)
        self.play(lens.animate.move_to([-0.1, 0.3, 0]), run_time=1.0)
        self.at("looking harder")
        self.play(lens.animate.move_to([0.6, -0.5, 0]).scale(1.3), run_time=1.6)
        self.finish()


# ---------------------------------------------------------------- s12

class S12Divide(CH):
    def construct(self):
        self.chrome(marker=2, lit=(0,))
        bk = beaker()
        cells = VGroup()
        for (dx, dy, r) in BEAKER_CELLS:
            cells.add(cell(r).move_to([0.2 + dx, 0.3 + dy, 0]))
        old = chip("old idea", YELLOW, 32, pad=0.2).move_to([0.2, 2.8, 0])
        world = VGroup(bk, cells, old)
        self.add(world)
        self.play(world.animate.scale(0.82).move_to([-1.7, 0.2, 0]), run_time=1.2)
        self.at("1850s")
        self.move_marker(3, 1.0)
        self.at("showed that")
        tp, ts = ValueTracker(0), ValueTracker(0)
        cc = np.array([1.55, 0.4, 0])
        R = 0.85
        div = dividing(tp, ts, cc, R)
        d0 = cell(R).move_to(cc)
        d0[1].move_to(cc)
        self.play(FadeIn(d0, scale=0.6), run_time=0.9)
        self.at("a cell divides")
        self.remove(d0)
        self.add(div)
        self.play(tp.animate.set_value(1.0), run_time=2.6, rate_func=smooth)
        self.at("One cell becomes")
        self.play(ts.animate.set_value(0.47), run_time=1.6, rate_func=smooth)
        self.at("The theory dropped")
        x = VGroup(Line([-2.85, 2.0, 0], [-0.55, -1.4, 0], color=RED, stroke_width=12), Line([-0.55, 2.0, 0], [-2.85, -1.4, 0], color=RED, stroke_width=12))
        self.play(Create(x), run_time=0.9)
        self.at("kept the rest")
        self.light(2, 1.2)
        self.finish()


# ---------------------------------------------------------------- s13

def step_icons():
    i1 = cork_card(0.8)
    i2 = VGroup(Ellipse(width=1.1, height=0.4, stroke_color="#9FD3E6", stroke_width=3, fill_color=BLUE, fill_opacity=0.4),
                icon("para", 0.4).shift(UP * 0.02))
    i3 = VGroup(leaf(0.55).shift(LEFT * 0.35), tissue(0.55).shift(RIGHT * 0.35))
    i4 = VGroup(cell(0.28, False).shift(LEFT * 0.3), cell(0.28, False).shift(RIGHT * 0.3))
    return [i1, i2, i3, i4]


class S13Close(CH):
    def construct(self):
        self.chrome(marker=3, lit=(0, 2))
        blocks, icons = VGroup(), step_icons()
        cols = [TAN, BLUE, GREEN, CELLC]
        for k, x in enumerate(TX):
            top = -1.5 + 1.1 * k
            b = Rectangle(width=1.4, height=top + 2.55, stroke_color=cols[k], stroke_width=4, fill_color=cols[k], fill_opacity=0.28)
            b.move_to([x, -2.55 + (top + 2.55) / 2, 0])
            icons[k].move_to([x, top + 0.7, 0])
            blocks.add(b)
        for lab in self.tl_labs:
            lab.set_color(TEXT)
        self.at("The three parts")
        self.play(*[l.animate.set_color(YELLOW) for l in self.tl_labs], self.tl_line.animate.set_color(YELLOW), run_time=0.8)
        for k in range(4):
            self.play(FadeIn(blocks[k], shift=UP * 0.5), run_time=0.55)
        self.at("Many steps")
        for k in range(4):
            self.play(FadeIn(icons[k], shift=DOWN * 0.3, scale=0.6), run_time=0.6)
            self.wait(0.25)
        self.at("Each one added")
        self.play(LaggedStart(*[Indicate(VGroup(b, ic), color=YELLOW, scale_factor=1.05) for b, ic in zip(blocks, icons)], lag_ratio=0.35), run_time=2.0)
        self.at("the cell theory")
        self.light(1, 1.2)
        self.play(*[Indicate(g, color=YELLOW, scale_factor=1.04) for g in self.pgroups], run_time=1.0)
        self.finish()


class S14End(EndCard):
    LINE = "Better microscopes gave evidence, and the cell theory grew and changed."
