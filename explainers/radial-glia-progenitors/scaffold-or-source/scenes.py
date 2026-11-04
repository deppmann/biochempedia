"""Scaffold or Source?  (chapter 3 of "The Ventricular Zone: Radial Glia as Stem Cells")

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one colour per concept; shared with the other chapters of this lesson)
  BLUE   = the radial glial cell (outline, fibre)
  YELLOW = highlight / the thing to look at
  TEAL   = cell-cycle state (cells caught in S phase or mitosis)
  GREEN  = a neuron (outline, process, ring, diamond). Never a fill that means "labelled".
  GREY   = ventricle, pia, labels, the old "scaffold only" reading, unknown cells
  RED    = the open question, a STOP sequence, a blind spot, a strike-through
  LIME   = GFP / reporter: the glowing, inherited mark. Only ever a fill or a glow.
  AMBER  = the human GFAP promoter (a promoter lamp)
  INDIGO = Cre recombinase (the scissors)
  PINK   = the dye that fills a recorded cell
  GOLD   = title rule and source tags only
A labelled radial glial cell is a BLUE outline with a LIME fill; a labelled neuron is a GREEN outline with
processes and a LIME fill. The outline says what the cell is, the lime says it carries the mark.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

LIME = "#B7F05A"
AMBER = "#E0A030"
INDIGO = "#9B7BFF"
PINK = "#F08FBF"

YB = -2.75           # ventricle strip when a ledger sits at the bottom
YT = 3.3             # pia
LED_Y = -3.4         # evidence ledger, same place every time
SX = -4.4            # x of the followed radial glial cell in the filming scenes
SYB = -2.75          # ventricle of the filming slice
SSO = SYB + 0.47     # soma height in the filming slice
ROW_NAMES = ["sorting", "fate map", "filming", "recording"]
TOP = 3.2
ROW_E = [2.5, 1.25, 0.0, -1.25, -3.0]        # header bottom, then the four row bottoms
E3 = [-6.55, -3.95, 0.1, 6.55]                # table with two data columns
E4 = [-6.55, -4.45, -1.05, 2.45, 6.55]        # table with three data columns


# ------------------------------------------------------------------ pieces
def stage(x0=-6.6, x1=6.6, yb=YB, vlab=True, plab=True):
    w, cx = x1 - x0, (x0 + x1) / 2
    g = VGroup(Rectangle(width=w, height=0.44, stroke_width=0, fill_color=GREY, fill_opacity=0.28).move_to([cx, yb, 0]),
               Rectangle(width=w, height=0.16, stroke_width=0, fill_color=GREY, fill_opacity=0.6).move_to([cx, YT, 0]))
    if vlab:
        g.add(T("ventricle", 24, GREY).move_to([x0 + 1.0, yb, 0]))
    if plab:
        g.add(T("pia", 24, GREY).move_to([x1 - 0.45, 3.62, 0]))
    return g


def glia(x, soma_y, color=BLUE, top=3.05, r=0.30, w=7, mark=False):
    """A radial glial cell. mark=True: the reporter fills it (lime), the outline stays blue."""
    fc = LIME if mark else color
    fibre = Line([x, soma_y + r, 0], [x, top, 0], stroke_color=fc, stroke_width=w)
    foot = Line([x - 0.28, top, 0], [x + 0.28, top, 0], stroke_color=fc, stroke_width=8)
    soma = Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=fc, fill_opacity=0.55 if mark else 0.35).move_to([x, soma_y, 0])
    return VGroup(fibre, foot, soma)


def dims(xs, soma_y, op=0.25):
    g = VGroup(*[glia(x, soma_y, w=4) for x in xs])
    g.set_opacity(op)
    return g


def glow(mob):
    c = mob.copy()
    c.set_color(LIME)
    c.set_stroke(width=15, opacity=0.28)
    c.set_fill(opacity=0)
    return c


def neuron(x, y, r=0.26, mark=False, proc=True):
    """A neuron: soma with a leading and a trailing process. Green outline; lime fill only if it carries the mark."""
    soma = Circle(radius=r, stroke_color=GREEN, stroke_width=3.5, fill_color=LIME if mark else GREEN, fill_opacity=0.9 if mark else 0.55)
    parts = [soma]
    if proc:
        parts.append(Line([0, r, 0], [0, r * 2.4, 0], stroke_color=GREEN, stroke_width=4))
        parts.append(Line([0, -r, 0], [0, -r * 2.4, 0], stroke_color=GREEN, stroke_width=2.5))
    g = VGroup(*parts).move_to([x, y, 0])
    g.set_z_index(5)
    return g


def ring(x, y, lit=False, r=0.25):
    """A cortical neuron seen from afar: a green ring; lime inside when the reporter is on."""
    c = Circle(radius=r, stroke_color=GREEN, stroke_width=4, stroke_opacity=1 if lit else 0.55,
               fill_color=LIME if lit else GREEN, fill_opacity=0.9 if lit else 0.07).move_to([x, y, 0])
    c.set_z_index(5)
    return c


def diamond(x, y, s=0.42):
    d = Square(side_length=s, stroke_color=GREEN, stroke_width=4, stroke_opacity=0.9,
               fill_color=GREEN, fill_opacity=0.07).rotate(PI / 4).move_to([x, y, 0])
    d.set_z_index(5)
    return d


def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def heading(text, x=0.0, y=3.35, size=34):
    return T(text, size, TEXT, font=TITLE_FONT).move_to([x, y, 0])


def lt(text, size, color, xl, y):
    """Text whose LEFT edge sits at xl."""
    t = T(text, size, color)
    return t.move_to([xl + t.width / 2, y, 0])


def led(tag, *chips):
    """Evidence ledger along the bottom (same place every time). Returns the group; parts are its children in order."""
    g = VGroup(T(tag, 26, GREY), *chips).arrange(RIGHT, buff=0.28)
    if g.width > 13.2:
        g.scale(13.2 / g.width)
    g.move_to([-6.65 + g.width / 2, LED_Y, 0])
    return g


def lchip(text, color=TEXT):
    return bchip(text, color, 26, pad=0.13)


def filmstrip(x0, x1, y0, y1):
    frame = Rectangle(width=x1 - x0, height=y1 - y0, stroke_color=GREY, stroke_width=3).move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0])
    holes = VGroup()
    for yy in np.arange(y0 + 0.3, y1 - 0.2, 0.55):
        for xx in (x0 + 0.14, x1 - 0.14):
            holes.add(Square(side_length=0.17, stroke_width=0, fill_color=GREY, fill_opacity=0.7).move_to([xx, yy, 0]))
    return VGroup(frame, holes)


def scissors(color=INDIGO):
    p = ORIGIN
    a1 = VGroup(Line(p, [0.30, -0.95, 0], stroke_color=color, stroke_width=6),
                Line(p, [-0.34, 0.5, 0], stroke_color=color, stroke_width=6),
                Circle(radius=0.2, stroke_color=color, stroke_width=5).move_to([-0.42, 0.72, 0]))
    a2 = VGroup(Line(p, [-0.30, -0.95, 0], stroke_color=color, stroke_width=6),
                Line(p, [0.34, 0.5, 0], stroke_color=color, stroke_width=6),
                Circle(radius=0.2, stroke_color=color, stroke_width=5).move_to([0.42, 0.72, 0]))
    pv = Dot(p, radius=0.07, color=color)
    return VGroup(a1, a2, pv)


def snip(sc, run=0.18):
    c = sc[2].get_center()
    return [Rotate(sc[0], 0.32, about_point=c, run_time=run), Rotate(sc[1], -0.32, about_point=c, run_time=run)]


def unsnip(sc, run=0.18):
    c = sc[2].get_center()
    return [Rotate(sc[0], -0.32, about_point=c, run_time=run), Rotate(sc[1], 0.32, about_point=c, run_time=run)]


def mini_dna(x, y, scale=1.0, on=True):
    a = Rectangle(width=0.45, height=0.28, stroke_color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=0.5)
    b = Rectangle(width=0.55, height=0.28, stroke_color=LIME, stroke_width=2, fill_color=LIME, fill_opacity=0.85)
    g = VGroup(a, b).arrange(RIGHT, buff=0.03).scale(scale).move_to([x, y, 0])
    g.set_z_index(6)
    return g


# ------------------------------------------------------------------ table
def row_y(i):
    return (ROW_E[i] + ROW_E[i + 1]) / 2


def table(edges, heads, name_x=None):
    bot = ROW_E[-1]
    grid = VGroup()
    for y in [TOP] + ROW_E:
        grid.add(Line([edges[0], y, 0], [edges[-1], y, 0], stroke_color=GREY, stroke_width=2, stroke_opacity=0.6))
    for x in edges:
        grid.add(Line([x, TOP, 0], [x, bot, 0], stroke_color=GREY, stroke_width=2, stroke_opacity=0.6))
    hcols = [GREY, TEXT, RED]
    heads_m = [T(h, 26, hcols[i]).move_to([(edges[i + 1] + edges[i + 2]) / 2, (TOP + ROW_E[0]) / 2, 0])
               for i, h in enumerate(heads)]
    nx = (edges[0] + edges[1]) / 2 if name_x is None else name_x
    rows_m = [T(n, 26, TEXT).move_to([nx, row_y(i), 0]) for i, n in enumerate(ROW_NAMES)]
    return grid, heads_m, rows_m


def cell_lines(lines, edges, col, row, color=TEXT, size=24, dy=0.0, buff=0.07):
    """A cell's text as one Text per line (so a strike-through can sit on each line)."""
    g = VGroup(*[T(l, size, color) for l in lines]).arrange(DOWN, buff=buff)
    return g.move_to([(edges[col + 1] + edges[col + 2]) / 2, row_y(row) + dy, 0])


ENT_A = [["few or no", "neurons"], ["cortical neurons", "stay dark"], ["radial glia never", "make a neuron"],
         ["dividing cells", "look different"]]
ENT_B = [["in culture,", "they made neurons"], ["nearly all projection", "neurons labeled;", "interneurons not"],
         ["a daughter became", "a neuron and climbed", "the parental fibre"],
         ["radial glial shape;", "markers on nearly all", "dividing cells"]]
ENT_C = [["a dish shows", "potential, not fate"], ["rests on when the", "promoter switches on"],
         ["a slice, followed for", "hours to days"]]
ENT_C3 = [["an electrode samples", "only cells it can reach"], ["a marker is not", "a family tree"]]


def full_table():
    """The finished table: two filled columns and an empty blind-spot column (header not yet drawn)."""
    grid, hm, rm = table(E4, ["if only a scaffold", "what was seen", "blind spot"])
    a = [cell_lines(ENT_A[i], E4, 0, i, GREY, buff=0.24) for i in range(4)]
    b = [cell_lines(ENT_B[i], E4, 1, i, TEXT) for i in range(4)]
    # only the three blind spots that are spoken; the two unspoken ones live in s14/s16 and s20
    c = [cell_lines(ENT_C[0], E4, 2, 0, RED),
         cell_lines(ENT_C3[0], E4, 2, 3, RED, dy=0.42), cell_lines(ENT_C3[1], E4, 2, 3, RED, dy=-0.42)]
    return grid, hm, rm, a, b, c


def band_rows(edges):
    """The three lines of evidence as bands over the table: [(band, badge, label)]."""
    out = []
    spec = [(0, 1, "1", "one group, mouse"), (2, 2, "2", "rat"), (3, 3, "3", "rat")]
    for r0, r1, num, lab in spec:
        ytop, ybot = ROW_E[r0] - 0.06, ROW_E[r1 + 1] + 0.06
        band = RoundedRectangle(corner_radius=0.12, width=edges[-1] - edges[0] - 0.12, height=ytop - ybot,
                                stroke_color=YELLOW, stroke_width=3.5).move_to([(edges[0] + edges[-1]) / 2, (ytop + ybot) / 2, 0])
        badge = VGroup(Circle(radius=0.26, stroke_color=YELLOW, stroke_width=3.5, fill_color=BG, fill_opacity=1),
                       T(num, 28, YELLOW)).move_to([edges[0] + 0.38, (ytop + ybot) / 2, 0])
        lt_ = T(lab, 30, YELLOW)
        label = VGroup(Rectangle(width=lt_.width + 0.3, height=0.5, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(lt_), lt_)
        label.move_to([(edges[2] + edges[3]) / 2, (ytop + ybot) / 2, 0])
        out.append((band, badge, label))
    return out


NAME_X3 = -4.9


def q_table():
    grid, hm, rm = table(E3, ["if only a scaffold", "what was seen"], name_x=NAME_X3)
    return grid, hm, rm, band_rows(E3)


# ------------------------------------------------------------------ shared sub-scenes (dish)
DISH_C = np.array([0.0, -1.2, 0])
LAND = [(-2.8, -1.45), (-1.4, -2.0), (0.0, -2.2), (1.4, -2.0), (2.8, -1.45)]


def make_dish():
    d = Arc(radius=4.2, start_angle=PI, angle=PI, stroke_color=GREY, stroke_width=5, fill_color=GREY, fill_opacity=0.12)
    d.stretch(0.75, 1)
    d.move_to(DISH_C)
    return d


def make_funnel():
    return Polygon([-2.4, 2.4, 0], [2.4, 2.4, 0], [0.5, 0.8, 0], [-0.5, 0.8, 0], stroke_color=GREY, stroke_width=5,
                   fill_color=GREY, fill_opacity=0.15)


def lime_cell(x, y, r=0.32):
    """A sorted, GFP-carrying radial glial cell: blue outline, lime fill."""
    c = Circle(radius=r, stroke_color=BLUE, stroke_width=4, fill_color=LIME, fill_opacity=0.6).move_to([x, y, 0])
    c.set_z_index(4)
    return c


def dish_state():
    dish = make_dish()
    dlab = T("dish", 30, GREY).move_to([5.9, -1.5, 0])
    dtie = Line([5.4, -1.5, 0], [4.0, -1.5, 0], stroke_color=GREY, stroke_width=2)
    cells = VGroup(*[lime_cell(x, y) for x, y in LAND])
    funnel = make_funnel()
    flab = T("sorter", 30, GREY).move_to([4.3, 1.7, 0])
    return dish, dlab, dtie, cells, funnel, flab


# ================================================================== scenes
class S00Title(TitleCard):
    LESSON = "The Ventricular Zone: Radial Glia as Stem Cells"
    TITLE = "Scaffold or Source?"


# fibres for the opening three scenes: the followed cell is the right-most one
F_OPEN = [-6.0, -4.6, -3.2, -1.8, -0.4, 1.0]
HERO = 1.0
YB0 = -3.2
SO0 = YB0 + 0.47


class S01Q(SpokenScene):
    def construct(self):
        st = stage(-6.6, 3.3, YB0)
        nb = dims(F_OPEN[:-1], SO0)
        g = glia(HERO, SO0)
        n = neuron(HERO + 0.33, SO0 + 0.8)
        sc = bchip("scaffold", BLUE, 44).move_to([5.1, 2.4, 0])
        l1 = arr([sc.get_left()[0], 2.4, 0], [HERO + 0.2, 2.4, 0], color=BLUE, w=4)
        orr = T("or", 36, GREY).move_to([5.1, 0.3, 0])
        src = bchip("source?", RED, 44).move_to([5.1, -1.0, 0])
        l2 = arr([src.get_left()[0], -1.0, 0], [HERO + 0.4, SO0 + 0.1, 0], color=RED, w=4)
        self.play(FadeIn(st), FadeIn(nb), Create(g), run_time=0.8)
        self.at("glial fibers")
        self.play(Indicate(g[0], color=YELLOW, scale_factor=1.0), run_time=0.6)
        self.at("guide young neurons")
        self.play(FadeIn(n, scale=0.5), run_time=0.5)
        self.at("outward")
        self.play(n.animate.set_y(1.2), run_time=1.3)
        self.at("Are those same cells")
        self.play(FadeIn(sc), GrowArrow(l1), Indicate(g, color=YELLOW, scale_factor=1.03), run_time=0.9)
        self.at("also the source")
        self.play(FadeIn(orr), FadeIn(src, scale=0.9), GrowArrow(l2), Indicate(g[2], color=YELLOW, scale_factor=1.4), run_time=0.9)
        self.finish()


class S02Rakic(SpokenScene):
    def construct(self):
        yb = -3.2
        so = yb + 0.47
        st = stage(-6.6, 2.75, yb)
        xs = [-5.9, -4.75, -3.6, -2.45, -1.3, -0.15, 1.0, 2.15]
        gs = VGroup(*[glia(x, so, w=5) for x in xs])
        tag = bchip("Rakic, 1972", GOLD, 32).move_to([4.85, 3.2, 0])
        label = T("fetal rhesus\nmonkey cortex", 28, GREY).move_to([4.85, 2.3, 0])
        ns = [neuron(-5.57, -1.0), neuron(-4.42, 1.9), neuron(-3.27, 0.2), neuron(-0.97, 1.5), neuron(1.33, -0.8), neuron(2.48, 0.6)]
        star = ns[5]
        nl = T("young neuron", 30, GREEN).move_to([4.85, 1.45, 0])
        nlead = arr([3.9, 1.3, 0], [2.85, 0.75, 0], color=GREEN, w=3, tip=0.16)
        # electron-micrograph style inset
        bx = Rectangle(width=3.6, height=3.7, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.2).move_to([4.85, -0.95, 0])
        bx2 = Rectangle(width=3.4, height=3.5, stroke_color=GREY, stroke_width=1.5).move_to([4.85, -0.95, 0])
        ifib = Line([3.95, -2.05, 0], [3.95, 0.7, 0], stroke_color=BLUE, stroke_width=12)
        ineu = neuron(4.82, -0.85, r=0.55)
        ifl = T("fibre", 26, BLUE).move_to([3.95, -2.45, 0])
        inl = T("neuron", 26, GREEN).move_to([5.75, -2.45, 0])
        icap = T("close-up (schematic)", 26, GREY).move_to([4.85, -3.3, 0])
        link = DashedLine([2.8, 0.45, 0], [3.05, -0.1, 0], color=GREY, stroke_width=3)
        yr = T("1972", 44, GOLD).move_to([4.85, 3.2, 0])
        self.play(FadeIn(st), run_time=0.3)
        self.at("1972")
        self.play(FadeIn(yr, scale=0.8), LaggedStart(*[Create(g) for g in gs], lag_ratio=0.12), run_time=1.4)
        self.at("Pasko Rakic")
        self.play(FadeOut(yr), FadeIn(tag), run_time=0.5)
        self.at("monkey cortex")
        self.play(FadeIn(label), Create(link), FadeIn(bx), FadeIn(bx2), FadeIn(ifib), FadeIn(ifl), FadeIn(icap), run_time=0.8)
        self.at("young neurons pressed")
        self.play(LaggedStart(*[FadeIn(n, scale=0.4) for n in ns], lag_ratio=0.1), FadeIn(nl), GrowArrow(nlead), run_time=0.7)
        self.at("pressed against")
        self.play(FadeIn(ineu, scale=0.5), FadeIn(inl), run_time=0.7)
        self.at("radial fibers")
        self.play(Indicate(gs, color=YELLOW, scale_factor=1.0), run_time=0.9)
        self.finish()


class S03Scaffold(SpokenScene):
    def construct(self):
        st = stage(-6.6, 3.3, YB0)
        nb = dims(F_OPEN[:-1], SO0)
        g = glia(HERO, SO0)
        n = neuron(HERO + 0.33, 0.6)
        sc = bchip("scaffold", BLUE, 44).move_to([5.1, 2.4, 0])
        tie = arr([sc.get_left()[0], 2.4, 0], [HERO + 0.2, 2.4, 0], color=BLUE, w=4)
        other = Circle(radius=0.48, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.3).move_to([2.35, SO0 + 0.05, 0])
        src = T("source?", 44, RED).move_to([4.9, -1.3, 0])
        sl = arr([4.0, -1.5, 0], [2.8, SO0 + 0.35, 0], color=RED, w=4)
        bud = neuron(2.35, SO0 + 0.05)
        self.add(st, nb, g, n)
        self.at("Radial glia")
        self.play(Indicate(g[0], color=YELLOW, scale_factor=1.0), run_time=0.6)
        self.at("scaffolds")
        self.play(FadeIn(sc), GrowArrow(tie), run_time=0.7)
        self.at("some other cell")
        self.play(FadeIn(other, scale=0.5), FadeIn(src), GrowArrow(sl), run_time=0.8)
        self.at("ventricular zone")
        self.play(Indicate(st[0], color=YELLOW, scale_factor=1.0), FadeIn(bud, scale=0.4), run_time=0.7)
        self.play(bud.animate.move_to([HERO + 0.33, SO0 + 0.8, 0]), run_time=1.2)
        self.finish()


class S04Three(SpokenScene):
    def construct(self):
        grid, hm, rm, bands = q_table()
        banner = T("rodent studies, around the year 2000", 28, GREY).move_to([0, 3.58, 0])
        badges = [VGroup(b[1]) for b in bands]
        self.play(Create(grid), FadeIn(hm[0]), FadeIn(hm[1]), run_time=1.3)
        self.at("three lines")
        self.play(LaggedStart(*[AnimationGroup(Create(b[0]), FadeIn(b[1], scale=0.5)) for b in bands], lag_ratio=0.35), run_time=1.1)
        self.at("in rodents")
        self.play(FadeIn(banner), run_time=0.5)
        self.at("four methods")
        self.play(FadeIn(rm[0], shift=RIGHT * 0.2), run_time=0.3)
        self.play(FadeIn(rm[1], shift=RIGHT * 0.2), FadeIn(bands[0][2]), run_time=0.3)
        self.play(FadeIn(rm[2], shift=RIGHT * 0.2), FadeIn(bands[1][2]), run_time=0.3)
        self.play(FadeIn(rm[3], shift=RIGHT * 0.2), FadeIn(bands[2][2]), run_time=0.3)
        self.finish()


class S05Ask(SpokenScene):
    def construct(self):
        grid, hm, rm, bands = q_table()
        banner = T("rodent studies, around the year 2000", 28, GREY).move_to([0, 3.58, 0])
        self.add(grid, *hm, *rm, banner)
        for b in bands:
            b[0].set_stroke(opacity=0.3)
            b[1].set_opacity(0.5)
            b[2].set_opacity(0.5)
            self.add(b[0], b[1], b[2])
        self.at("each one")
        self.play(*[Indicate(r, color=YELLOW, scale_factor=1.15) for r in rm], run_time=0.9)
        self.at("if radial glia were only a scaffold")
        cx = (E3[1] + E3[2]) / 2
        box = RoundedRectangle(corner_radius=0.1, width=E3[2] - E3[1] - 0.12, height=TOP - ROW_E[-1] - 0.1,
                               stroke_color=YELLOW, stroke_width=5).move_to([cx, (TOP + ROW_E[-1]) / 2, 0])
        self.play(Create(box), hm[0].animate.set_color(YELLOW), run_time=0.9)
        self.at("what would we see")
        pt = T("if only a\nscaffold, what\nwould we see?", 30, TEXT, line_spacing=0.9)
        prompt = VGroup(Rectangle(width=pt.width + 0.3, height=pt.height + 0.3, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(pt), pt)
        prompt.move_to([cx, (ROW_E[0] + ROW_E[-1]) / 2 + 0.55, 0])
        qm = T("?", 90, RED).move_to([cx, ROW_E[-1] + 0.6, 0])
        self.play(FadeIn(prompt, scale=0.9), FadeIn(qm, scale=0.5), run_time=0.9)
        self.finish()


class S06Sort(SpokenScene):
    def construct(self):
        yb = -3.2
        so = yb + 0.47
        st = stage(-6.6, 0.6, yb)
        xs = [-5.9, -4.7, -3.5, -2.3, -1.1, 0.1]
        gs = VGroup(*[glia(x, so) for x in xs])
        gl = VGroup(*[glow(g) for g in gs])
        head = heading("Sorting, in mouse", 4.2, 3.2, 36)
        prom = bchip("human GFAP\npromoter", AMBER, 38).move_to([4.2, 1.1, 0])
        gfp = bchip("GFP", LIME, 64).move_to([4.2, -1.6, 0])
        link = arr(prom.get_bottom(), gfp.get_top(), color=GREY, w=7, tip=0.3)
        self.play(FadeIn(st), LaggedStart(*[Create(g) for g in gs], lag_ratio=0.1), run_time=0.7)
        self.at("sorting")
        self.play(FadeIn(head), run_time=0.5)
        self.at("make GFP")
        self.play(FadeIn(gfp, scale=0.8), FadeIn(gl), *[g.animate.set_color(LIME) for g in gs], run_time=1.1)
        self.at("from a human")
        self.play(FadeIn(prom, scale=0.9), GrowArrow(link), run_time=0.8)
        self.finish()


class S07Gfap(SpokenScene):
    def construct(self):
        lp = RoundedRectangle(corner_radius=0.5, width=6.0, height=5.7, stroke_color=BLUE, stroke_width=4,
                              fill_color=BLUE, fill_opacity=0.12).move_to([-3.45, 0.05, 0])
        rp = RoundedRectangle(corner_radius=0.5, width=6.0, height=5.7, stroke_color=BLUE, stroke_width=4,
                              fill_color=BLUE, fill_opacity=0.12).move_to([3.45, 0.05, 0])
        name = T("rodent radial glia", 34, BLUE).move_to([-3.45, 2.1, 0])
        name2 = T("the same cells", 34, BLUE).move_to([3.45, 2.1, 0])
        d1 = Dot([-4.5, 0.55, 0], radius=0.2, color=TEXT)
        d2 = Dot([-2.3, -0.1, 0], radius=0.2, color=TEXT)
        pl = T("little GFAP protein", 34, TEXT).move_to([-3.45, -1.9, 0])
        pa = arr([-2.9, -1.5, 0], [-2.35, -0.35, 0], color=GREY, w=4, tip=0.2)
        prom = bchip("human GFAP\npromoter fragment", AMBER, 32).move_to([3.45, 0.95, 0])
        lamp = Circle(radius=0.55, stroke_color=AMBER, stroke_width=5, fill_color=AMBER, fill_opacity=0.06).move_to([3.0, -1.1, 0])
        pull = arr([3.0, 0.15, 0], [3.0, -0.5, 0], color=AMBER, w=6, tip=0.25)
        lab = T("active", 36, AMBER).move_to([5.0, -1.1, 0])
        lead = arr([4.4, -1.1, 0], [3.65, -1.1, 0], color=AMBER, w=5)
        self.play(FadeIn(lp), FadeIn(name), run_time=0.8)
        self.at("make little GFAP")
        self.play(FadeIn(d1), FadeIn(d2), FadeIn(pl), Create(pa), run_time=0.9)
        self.at("that human promoter")
        self.play(FadeIn(rp), FadeIn(name2), FadeIn(prom, scale=0.9), FadeIn(lamp), GrowArrow(pull), run_time=1.0)
        self.at("active in them")
        self.play(lamp.animate.set_fill(opacity=0.95), FadeIn(lab), GrowArrow(lead),
                  rp.animate.set_stroke(LIME, width=7).set_fill(LIME, opacity=0.18), run_time=1.0)
        self.finish()


class S08Dish(SpokenScene):
    def construct(self):
        dish, dlab, dtie, cells_done, funnel, flab = dish_state()
        xs = [-3.6 + 0.8 * i for i in range(10)]
        tray = RoundedRectangle(corner_radius=0.2, width=8.6, height=0.95, stroke_color=GREY, stroke_width=3).move_to([0, 3.15, 0])
        limes, greys = [], []
        for k, x in enumerate(xs):
            if k % 2 == 0:
                limes.append(lime_cell(x, 3.15, 0.27))
            else:
                greys.append(Circle(radius=0.27, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.3).move_to([x, 3.15, 0]))
        ledger = led("sorting", lchip("scaffold only: few or no neurons", GREY))
        q = T("?", 140, RED).move_to([0, -0.85, 0])
        gl_ = T("sorted green cells", 30, LIME).move_to([0, -0.2, 0])
        self.play(FadeIn(tray), *[FadeIn(c) for c in limes + greys], Create(funnel), FadeIn(flab), Create(dish), FadeIn(dlab), Create(dtie), run_time=0.6)
        self.at("green cells were sorted")
        anims = []
        for c, (lx, ly) in zip(limes, LAND):
            c0 = c.get_center()
            p = VMobject().set_points_as_corners([c0, [c0[0] * 0.2, 2.9, 0], [0, 1.9, 0], [0, 0.6, 0], [lx, ly, 0]])
            anims.append(MoveAlongPath(c, p))
        side = [b.animate.shift(RIGHT * 1.6 + UP * 0.2).set_opacity(0) for b in greys]
        self.play(LaggedStart(*anims, lag_ratio=0.3), *side, run_time=2.2)
        self.play(FadeOut(tray), FadeIn(gl_), run_time=0.3)
        self.at("If they were only")
        self.play(FadeIn(ledger), run_time=0.6)
        self.at("Did they make any")
        self.play(FadeOut(gl_), FadeIn(q, scale=0.6), run_time=0.6)
        self.finish()


class S09Pause(NarratedScene):
    def construct(self):
        dish, dlab, dtie, cells, funnel, flab = dish_state()
        ledger = led("sorting", lchip("scaffold only: few or no neurons", GREY))
        q = T("?", 140, RED).move_to([0, -0.85, 0])
        self.add(dish, dlab, dtie, cells, funnel, flab, ledger, q)
        self.wait(self.narration_s)


class S10Dishrev(SpokenScene):
    def construct(self):
        dish, dlab, dtie, cells, funnel, flab = dish_state()
        exp = lchip("scaffold only: few or no neurons", GREY)
        seen = lchip("seen: made neurons", TEXT)
        ledger = led("sorting", exp, seen)
        q = T("?", 140, RED).move_to([0, -0.85, 0])
        self.add(dish, dlab, dtie, cells, funnel, flab, ledger[0], ledger[1], q)
        dlab2 = T("dish,\nin culture", 28, GREY).move_to([5.8, -1.5, 0])
        blind = bchip("a dish shows potential, not fate", RED, 34).move_to([0, 1.9, 0])
        nl = T("neurons", 36, GREEN).move_to([0, 0.5, 0])
        self.at("In culture")
        self.play(FadeOut(q), FadeOut(funnel), FadeOut(flab), Transform(dlab, dlab2), run_time=0.5)
        ns = VGroup(*[neuron(x, y + 1.15, 0.27) for x, y in LAND])
        nlead = arr([0, 0.15, 0], [0, -0.55, 0], color=GREEN, w=5)
        self.at("made neurons")
        self.play(LaggedStart(*[TransformFromCopy(cells[i], ns[i]) for i in range(5)], lag_ratio=0.15), FadeIn(ledger[2]),
                  FadeIn(nl), GrowArrow(nlead), run_time=1.3)
        self.at("shows potential")
        self.play(FadeIn(blind), run_time=0.6)
        self.finish()


def embryo():
    """A mouse embryo in profile: domed head with snout, ear and eye, curled body, limb buds and a tail. Cortex = blue dome."""
    hc = np.array([-3.2, 0.95, 0])
    body = Ellipse(width=5.2, height=1.8, stroke_color=GREY, stroke_width=3, fill_color=BG, fill_opacity=1).rotate(0.12).move_to([-1.7, -1.85, 0])
    tail = Arc(radius=0.9, start_angle=-PI / 2, angle=PI * 0.95, stroke_color=GREY, stroke_width=3).move_to([1.35, -2.1, 0])
    limbs = VGroup(Ellipse(width=0.9, height=0.5, stroke_color=GREY, stroke_width=3, fill_color=BG, fill_opacity=1).rotate(-0.9).move_to([-0.6, -2.6, 0]),
                   Ellipse(width=0.9, height=0.5, stroke_color=GREY, stroke_width=3, fill_color=BG, fill_opacity=1).rotate(-0.5).move_to([-3.1, -2.65, 0]))
    snout = Ellipse(width=1.5, height=1.1, stroke_color=GREY, stroke_width=3, fill_color=BG, fill_opacity=1).move_to(hc + np.array([-2.0, -0.85, 0]))
    head = Circle(radius=2.1, stroke_color=GREY, stroke_width=3, fill_color=BG, fill_opacity=1).move_to(hc)
    ear = Arc(radius=0.4, start_angle=-PI / 2, angle=PI, stroke_color=GREY, stroke_width=3).move_to(hc + np.array([1.6, -0.6, 0]))
    eye = Dot(radius=0.13, color=GREY).move_to(hc + np.array([-1.45, -0.55, 0]))
    nose = Dot(radius=0.08, color=GREY).move_to(hc + np.array([-2.65, -0.9, 0]))
    vent = Ellipse(width=1.0, height=1.5, stroke_color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=0.35).move_to(hc + DOWN * 0.1)
    cortex = Arc(radius=1.78, start_angle=PI * 0.1, angle=PI * 0.8, stroke_color=BLUE, stroke_width=14, arc_center=hc)
    dots = VGroup(*[Dot(hc + 1.78 * np.array([np.cos(a), np.sin(a), 0]), radius=0.11, color=INDIGO)
                    for a in np.linspace(PI * 0.14, PI * 0.86, 9)])
    return VGroup(tail, limbs, body, snout, head, ear, eye, nose, vent, cortex), dots, hc


class S11Cre(SpokenScene):
    def construct(self):
        emb, dots, hc = embryo()
        elab = T("living mouse embryo", 28, GREY).move_to([-2.2, -3.55, 0])
        clab = T("cortex", 30, BLUE).move_to([hc[0], 3.45, 0])
        head = heading("Fate mapping", 3.9, 3.2, 38)
        cre = bchip("Cre recombinase", INDIGO, 36).move_to([3.9, 0.1, 0])
        prom = bchip("GFAP promoter", AMBER, 36).move_to([3.9, 1.6, 0])
        link = arr(prom.get_bottom(), cre.get_top(), color=GREY)
        self.play(FadeIn(emb), FadeIn(elab), FadeIn(clab), FadeIn(head), run_time=0.9)
        self.at("An enzyme called")
        self.play(FadeIn(cre, scale=0.9), run_time=0.7)
        self.at("made from a GFAP")
        self.play(FadeIn(prom, scale=0.9), GrowArrow(link), run_time=0.7)
        self.play(FadeIn(dots, scale=0.4), run_time=0.9)
        self.finish()


def blk(text, color, w, h=2.0, size=40):
    box = RoundedRectangle(corner_radius=0.14, width=w, height=h, stroke_color=color, stroke_width=3.5,
                           fill_color=color, fill_opacity=0.16)
    back = RoundedRectangle(corner_radius=0.14, width=w, height=h, stroke_width=0, fill_color=BG, fill_opacity=1)
    return VGroup(back, box, T(text, size, color))


class S12Cut(SpokenScene):
    def construct(self):
        y0 = -0.4
        line = Line([-6.6, y0, 0], [6.6, y0, 0], color=GREY, stroke_width=6)
        prom = blk("promoter", GREY, 3.9, h=3.0, size=48).move_to([-4.15, y0, 0])
        stop = blk("STOP", RED, 2.9, h=3.0, size=58).move_to([-0.65, y0, 0])
        rep = blk("reporter gene", GREY, 5.2, h=3.0, size=48).move_to([3.5, y0, 0])
        sc = scissors().scale(1.4)
        lab = T("Cre", 40, INDIGO)
        grp = VGroup(sc, lab)
        lab.next_to(sc, RIGHT, buff=0.4).shift(UP * 0.5)
        py = y0 + 1.5 + 1.33          # blade tips just touch the top edge of the STOP box

        def goto(x, y):
            return grp.animate.shift(np.array([x, y, 0]) - sc[2].get_center())
        grp.shift(np.array([-2.15, 3.3, 0]) - sc[2].get_center())
        self.play(FadeIn(line), FadeIn(prom), FadeIn(stop), FadeIn(rep), run_time=0.3)
        self.at("cuts out")
        self.play(FadeIn(grp, shift=DOWN * 0.3), goto(-2.15, py), run_time=0.4)
        self.play(*snip(sc, 0.12))
        self.play(*unsnip(sc, 0.1))
        self.at("stop sequence")
        self.play(goto(0.85, py), run_time=0.4)
        self.play(*snip(sc, 0.12))
        self.play(*unsnip(sc, 0.1), stop.animate.shift(DOWN * 2.6).set_opacity(0.0), run_time=0.6)
        self.at("reporter gene")
        self.play(Indicate(rep, color=LIME, scale_factor=1.04), FadeOut(grp),
                  prom.animate.shift(RIGHT * 3.0), run_time=1.0)
        self.at("change in the DNA")
        br = Brace(VGroup(prom, rep), DOWN, color=TEXT, buff=0.3)
        bl = T("a change in the DNA", 42, TEXT).next_to(br, DOWN, buff=0.2)
        self.play(GrowFromCenter(br), FadeIn(bl), rep[1].animate.set_stroke(LIME), rep[2].animate.set_color(LIME), run_time=0.9)
        self.finish()


def cell_big(x, y, r=0.95, kind="glia"):
    """A big cell for the inheritance scene: outline = type, lime fill = carries the reporter."""
    col = BLUE if kind == "glia" else GREEN
    return Circle(radius=r, stroke_color=col, stroke_width=5, fill_color=BLUE, fill_opacity=0.25).move_to([x, y, 0])


class S13Perm(SpokenScene):
    def construct(self):
        DX = (-4.4, 0.0, 4.4)
        DY = -0.55
        parent = cell_big(0, 2.6, 0.85)
        pb = mini_dna(0, 2.6, 1.4)
        kids = [cell_big(x, DY, 1.2) for x in DX]
        kb = [mini_dna(x, DY, 1.9) for x in DX]
        arrows = [arr([0, 1.7, 0], [x, 0.7, 0], color=GREY, w=5) for x in DX]
        head = T("cut DNA", 34, LIME).move_to([2.6, 2.6, 0])
        lamps = [Circle(radius=0.3, stroke_color=AMBER, stroke_width=4, fill_color=AMBER, fill_opacity=0.95).move_to([x, -2.55, 0]) for x in DX]
        llab = T("promoter on", 28, AMBER).move_to([DX[0], -3.2, 0])
        llab2 = T("promoter on", 28, AMBER).move_to([DX[1], -3.2, 0])
        llab3 = T("promoter on", 28, AMBER).move_to([DX[2], -3.2, 0])
        nl = T("neuron", 38, GREEN).move_to([DX[2], 2.0, 0])
        self.play(FadeIn(parent), FadeIn(pb), FadeIn(head), run_time=0.7)
        self.at("copied into every")
        self.play(LaggedStart(*[AnimationGroup(Create(a), FadeIn(k), TransformFromCopy(pb, b)) for a, k, b in zip(arrows, kids, kb)],
                              lag_ratio=0.3), run_time=1.4)
        self.play(parent.animate.set_fill(LIME, opacity=0.4), *[k.animate.set_fill(LIME, opacity=0.4) for k in kids], run_time=0.4)
        self.at("even after")
        self.play(*[FadeIn(l) for l in lamps], FadeIn(llab), FadeIn(llab2), FadeIn(llab3), run_time=0.8)
        self.at("switches off")
        off = T("promoter off", 28, GREY).move_to([DX[2], -3.2, 0])
        self.play(lamps[2].animate.set_fill(opacity=0.05), Transform(llab3, off), run_time=0.7)
        self.at("in a neuron")
        nneu = VGroup(Line([DX[2], DY + 1.2, 0], [DX[2], 1.65, 0], stroke_color=GREEN, stroke_width=6),
                      Line([DX[2], DY - 1.2, 0], [DX[2], -1.85, 0], stroke_color=GREEN, stroke_width=3.5))
        self.play(kids[2].animate.set_stroke(GREEN, width=6), Create(nneu), FadeIn(nl), run_time=0.8)
        self.play(Indicate(kids[2], color=LIME, scale_factor=1.1), Indicate(kb[2], color=LIME, scale_factor=1.3), run_time=0.9)
        self.finish()


# ------------------------------------------------------------- cortex scenes
FIB_X = [-5.9, -4.6, -3.3, -2.0, -0.7, 0.6]
N_COLS = [-5.25, -3.95, -2.65, -1.35, -0.05, 1.25]
N_ROWS = [1.0, 1.8, 2.6]
DIAM_SLOTS = [(-3.95, 1.0), (-1.35, 1.0), (1.25, 1.0)]
RING_LABEL_Y = 2.6


def cortex():
    st = stage(-6.6, 2.0, YB)
    gs = VGroup(*[glia(x, YB + 0.47, w=4) for x in FIB_X])
    ns = VGroup()
    for y in N_ROWS:
        for x in N_COLS:
            if (x, y) not in DIAM_SLOTS:
                ns.add(ring(x, y))
    return st, gs, ns


def neuron_label(text, y=2.6):
    t = T(text, 30, GREEN)
    return t.move_to([3.0 + t.width / 2, y, 0])


EXP_FATE = "scaffold only: cortical neurons dark"


class S14Crep(SpokenScene):
    def construct(self):
        st, gs, ns = cortex()
        lab = neuron_label("cortical\nneurons")
        pa = arr([3.0, RING_LABEL_Y, 0], [1.6, RING_LABEL_Y, 0], color=GREEN, w=3, tip=0.16)
        ledger = led("fate map", lchip(EXP_FATE, GREY))
        q = T("?", 140, RED).move_to([4.8, 0.3, 0])
        self.play(FadeIn(st), Create(gs), run_time=1.0)
        self.play(FadeIn(ns), run_time=0.6)
        self.at("cortical neurons")
        self.play(FadeIn(lab), GrowArrow(pa), run_time=0.6)
        self.at("stay dark")
        self.play(FadeIn(ledger), Indicate(ns, color=GREY, scale_factor=1.0), run_time=0.8)
        self.at("What did the fate map show")
        self.play(FadeIn(q, scale=0.6), run_time=0.6)
        self.finish()


class S15Pause(NarratedScene):
    def construct(self):
        st, gs, ns = cortex()
        lab = neuron_label("cortical\nneurons")
        pa = arr([3.0, RING_LABEL_Y, 0], [1.6, RING_LABEL_Y, 0], color=GREEN, w=3, tip=0.16)
        ledger = led("fate map", lchip(EXP_FATE, GREY))
        q = T("?", 140, RED).move_to([4.8, 0.3, 0])
        self.add(st, gs, ns, lab, pa, ledger, q)
        self.wait(self.narration_s)


class S16Crerev(SpokenScene):
    def construct(self):
        st, gs, ns = cortex()
        lab = neuron_label("cortical\nneurons")
        pa = arr([3.0, RING_LABEL_Y, 0], [1.6, RING_LABEL_Y, 0], color=GREEN, w=3, tip=0.16)
        ledger = led("fate map", lchip(EXP_FATE, GREY), lchip("seen: projection neurons lit", TEXT))
        q = T("?", 140, RED).move_to([4.8, 0.3, 0])
        self.add(st, gs, ns, lab, pa, ledger[0], ledger[1], q)
        # interneurons wait, outside the wall, in their own region
        zone = DashedVMobject(RoundedRectangle(corner_radius=0.25, width=3.5, height=2.5, stroke_color=GREY, stroke_width=3),
                              num_dashes=40).move_to([5.05, -1.1, 0])
        lanes = [-0.4, -1.1, -1.8]
        diams = VGroup(*[diamond(3.8, y) for y in lanes])
        dlab = T("interneurons", 28, TEXT).move_to([5.5, -0.55, 0])
        dsub = T("local, inhibitory", 26, TEXT).move_to([5.45, -1.1, 0])
        dno = T("no reporter", 30, RED).move_to([5.45, -1.75, 0])
        vf = bchip("born in the\nventral forebrain", TEXT, 28).move_to([5.1, 0.75, 0])
        vfa = arr([3.9, -1.1, 0], [2.4, -1.1, 0], color=TEXT, w=4, tip=0.2)
        rep = T("carry the reporter", 30, LIME).move_to([3.0 + 1.8, 1.6, 0])
        rep.move_to([3.0 + rep.width / 2, 1.6, 0])
        self.at("all cortical")
        self.play(Transform(lab, neuron_label("cortical projection\nneurons")), FadeOut(q),
                  LaggedStart(*[n.animate.set_fill(LIME, opacity=0.9).set_stroke(GREEN, opacity=1) for n in ns], lag_ratio=0.03),
                  run_time=1.5)
        self.at("carried the reporter")
        self.play(FadeIn(ledger[2]), FadeIn(rep), run_time=0.6)
        self.at("Cortical interneurons")
        self.play(FadeIn(zone), FadeIn(diams, scale=0.5), FadeIn(dlab), run_time=0.7)
        self.at("local inhibitory cells")
        self.play(FadeIn(dsub), run_time=0.5)
        self.at("did not")
        self.play(FadeIn(dno), run_time=0.5)
        self.at("They are born in")
        self.play(FadeOut(dlab), FadeOut(dsub), FadeOut(dno), FadeIn(vf), run_time=0.5)
        self.at("ventral forebrain")
        paths = []
        for d, y, (sx, sy) in zip(diams, lanes, [(1.25, 1.0), (-1.35, 1.0), (-3.95, 1.0)]):
            p = VMobject().set_points_as_corners([[3.8, y, 0], [sx, y, 0], [sx, sy, 0]])
            paths.append(MoveAlongPath(d, p))
        self.play(*paths, run_time=1.3)
        self.finish()


# ------------------------------------------------------------- filming scenes
BRAIN_C = np.array([-2.2, 0.0, 0])


class S17Film(SpokenScene):
    def construct(self):
        brain = Ellipse(width=8.2, height=6.2, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.07).move_to(BRAIN_C)
        v1 = Ellipse(width=1.1, height=3.6, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.4).move_to([-3.7, 0, 0])
        v2 = Ellipse(width=1.1, height=3.6, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.4).move_to([-0.7, 0, 0])
        blab = T("rat embryo brain", 28, GREY).move_to([-2.2, -3.4, 0])
        vlab = T("ventricles", 26, GREY).move_to([-2.2, 0.0, 0])
        u = np.array([0.93, 0.37, 0.0])
        u = u / np.linalg.norm(u)
        tip_in = np.array([-0.45, 0.4, 0.0])
        shift = 2.4
        tip = tip_in + u * shift
        ang = np.arctan2(u[1], u[0])
        needle = Line(tip, tip + u * 1.35, stroke_color=TEXT, stroke_width=5)
        barrel = Rectangle(width=2.2, height=0.75, stroke_color=TEXT, stroke_width=4, fill_color=BG, fill_opacity=1)
        barrel.rotate(ang).move_to(tip + u * 2.45)
        plunger = Line(tip + u * 3.55, tip + u * 4.1, stroke_color=TEXT, stroke_width=6)
        dots = VGroup(*[Dot(tip + u * (1.75 + 0.4 * i), radius=0.13, color=LIME) for i in range(4)])
        syr = VGroup(needle, barrel, plunger, dots)
        d = -u
        vlab2 = T("GFP retrovirus", 34, LIME).move_to([4.5, 3.25, 0])
        self.play(Create(brain), FadeIn(v1), FadeIn(v2), run_time=1.0)
        self.at("filming lineage")
        self.play(FadeIn(vlab), run_time=0.4)
        self.at("in rat")
        self.play(FadeIn(blab), run_time=0.4)
        self.at("A retrovirus carrying")
        self.play(FadeIn(syr, shift=DOWN * 0.2), FadeIn(vlab2), run_time=0.8)
        self.at("injected into the ventricles")
        self.play(syr.animate.shift(d * shift), FadeOut(vlab), FadeOut(vlab2), run_time=1.0)
        out = [Dot([-0.7 + 0.1 * (i - 1.5), 0.5 - 0.5 * i, 0], radius=0.13, color=LIME) for i in range(4)]
        out2 = [Dot([-3.7 + 0.1 * (i - 1.5), 0.5 - 0.5 * i, 0], radius=0.13, color=LIME) for i in range(4)]
        self.play(*[Transform(dots[i], out[i]) for i in range(4)], *[FadeIn(o, scale=0.5) for o in out2], run_time=1.0)
        self.finish()


SLICE_DIMS = (-6.1, 0.6, 1.5)


def slice_base():
    st = stage(-6.6, 2.0, SYB, plab=False)
    dim = dims(SLICE_DIMS, SSO, op=0.3)
    return st, dim


def slice_film(top=3.55, bottom=-3.2):
    return filmstrip(-6.65, 2.1, bottom, top)


def tree_node(kind, x, y):
    if kind == "g":
        c = Circle(radius=0.3, stroke_color=BLUE, stroke_width=4, fill_color=LIME, fill_opacity=0.65).move_to([x, y, 0])
        c.set_z_index(4)
        return c
    return neuron(x, y, 0.26, mark=True)


class S18Inherit(SpokenScene):
    def construct(self):
        st, dim = slice_base()
        rnd_c = np.array([SX, SYB + 0.22 + 0.62, 0])
        hero = glia(SX, SSO)
        fibre0, foot0, soma = hero
        round_cell = Circle(radius=0.62, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.3).move_to(rnd_c)
        vx = [-6.2, -5.2, -3.6, -2.8, -1.9, -0.9, 0.0, 1.0, 1.8]
        virus = VGroup(*[Dot([x, SYB + 0.5, 0], radius=0.14, color=LIME) for x in vx])
        vlab = T("GFP retrovirus", 28, LIME).move_to([0.3, -1.3, 0])
        vlead = arr([-0.5, -1.65, 0], [-0.95, SYB + 0.65, 0], color=LIME, w=3, tip=0.16)
        dlab = T("dividing", 32, YELLOW).move_to([-2.5, -1.45, 0])
        dlead = arr([-3.4, -1.55, 0], [SX + 0.75, -1.75, 0], color=YELLOW, w=3, tip=0.16)
        # lineage tree, right column
        P = {"r": (5.0, 2.3), "a": (3.9, 0.8), "b": (6.1, 0.8), "c": (3.0, -0.7), "d": (4.8, -0.7)}
        kind = {"r": "g", "a": "g", "b": "n", "c": "g", "d": "n"}
        edges = [("r", "a"), ("r", "b"), ("a", "c"), ("a", "d")]
        tl = VGroup(*[Line([*P[a], 0], [*P[b], 0], stroke_color=LIME, stroke_width=4) for a, b in edges])
        tn = {k: tree_node(kind[k], *P[k]) for k in P}
        tlab = T("every descendant\ninherits the mark", 28, LIME).move_to([4.5, -2.15, 0])
        lg1 = tree_node("g", 0, 0).scale(0.7)
        lg2 = neuron(0, 0, 0.15, mark=True)
        lt1 = T("radial glial cell", 22, TEXT)
        lt2 = T("neuron", 22, TEXT)
        leg = VGroup(VGroup(lg1, lt1).arrange(RIGHT, buff=0.12), VGroup(lg2, lt2).arrange(RIGHT, buff=0.12)).arrange(RIGHT, buff=0.3)
        leg.move_to([2.35 + leg.width / 2, -3.35, 0])
        film = slice_film()
        flab = T("a living slice", 30, TEXT).move_to([4.55, 3.45, 0])
        flead = arr([3.45, 3.45, 0], [2.15, 3.4, 0], color=GREY, w=3, tip=0.16)
        self.play(FadeIn(st), FadeIn(dim), FadeIn(fibre0), FadeIn(foot0), FadeIn(soma), FadeIn(virus), FadeIn(vlab), GrowArrow(vlead), run_time=1.0)
        self.at("enters only dividing")
        self.play(*[v.animate.shift(UP * 0.3) for v in virus], run_time=0.8)
        self.at("dividing cells")
        self.play(FadeOut(soma), FadeIn(round_cell), fibre0.animate.put_start_and_end_on([SX, rnd_c[1] + 0.6, 0], [SX, 3.05, 0]).set_stroke(width=3),
                  FadeIn(dlab), GrowArrow(dlead), run_time=0.9)
        self.at("and these")
        near = virus[3]
        others = [v for i, v in enumerate(virus) if i != 3]
        self.play(near.animate.move_to(rnd_c), *[FadeOut(v) for v in others], FadeOut(vlab), FadeOut(vlead), run_time=0.8)
        gl = glow(round_cell)
        self.play(FadeOut(near), round_cell.animate.set_fill(LIME, opacity=0.65), fibre0.animate.set_color(LIME),
                  foot0.animate.set_color(LIME), FadeIn(gl), FadeOut(dlab), FadeOut(dlead), run_time=0.6)
        self.at("divide right at the ventricle")
        self.play(Indicate(round_cell, color=YELLOW, scale_factor=1.15), Indicate(st[0], color=YELLOW, scale_factor=1.0), run_time=0.9)
        self.at("Every descendant")
        self.play(FadeIn(tn["r"], scale=0.5), run_time=0.25)
        self.play(AnimationGroup(Create(tl[0]), Create(tl[1]), FadeIn(tn["a"]), FadeIn(tn["b"])), run_time=0.45)
        self.play(AnimationGroup(Create(tl[2]), Create(tl[3]), FadeIn(tn["c"]), FadeIn(tn["d"])), run_time=0.45)
        self.play(FadeIn(leg), run_time=0.3)
        self.at("inherits the mark")
        soma_new = Circle(radius=0.30, stroke_color=BLUE, stroke_width=3, fill_color=LIME, fill_opacity=0.55).move_to([SX, SSO, 0])
        self.play(FadeIn(tlab), Create(film), FadeIn(flab), GrowArrow(flead), Transform(round_cell, soma_new), FadeOut(gl),
                  fibre0.animate.put_start_and_end_on([SX, SSO + 0.3, 0], [SX, 3.05, 0]).set_stroke(width=7), run_time=1.1)
        self.finish()


def marked_hero():
    """The followed cell in the slice: interphase, lime fill, blue outline."""
    return glia(SX, SSO, mark=True)


def time_axis():
    ax = arr([3.4, 3.1, 0], [3.4, -3.0, 0], color=GREY, w=4, tip=0.25)
    tl = T("time-lapse", 28, GREY).move_to([4.9, 3.4, 0])
    ys = [1.9, 0.2, -1.5]
    names = ["rounds up", "divides", "two daughters"]
    dots = [Circle(radius=0.15, stroke_color=YELLOW, stroke_width=3, fill_color=BG, fill_opacity=1).move_to([3.4, y, 0]) for y in ys]
    labs = [lt(n, 32, TEXT, 3.8, y) for n, y in zip(names, ys)]
    return VGroup(ax, tl), dots, labs


class S19Divide(SpokenScene):
    def construct(self):
        st, dim = slice_base()
        film = slice_film()
        g = marked_hero()
        gg = glow(g[0])
        axis, dots, labs = time_axis()
        self.add(st, dim, film, gg, g[0], g[1], g[2], axis, *dots)
        self.at("A green radial glial cell")
        self.play(Indicate(g[2], color=YELLOW, scale_factor=1.4), run_time=0.7)
        self.at("divides")
        rc = np.array([SX, SYB + 0.22 + 0.85, 0])
        rnd = Circle(radius=0.85, stroke_color=BLUE, stroke_width=4, fill_color=LIME, fill_opacity=0.65).move_to(rc)
        self.play(FadeOut(g[2]), FadeIn(rnd), g[0].animate.put_start_and_end_on([SX, rc[1] + 0.85, 0], [SX, 3.05, 0]).set_stroke(width=4),
                  dots[0].animate.set_fill(YELLOW), FadeIn(labs[0]), run_time=1.0)
        self.at("at the ventricle")
        d1 = Circle(radius=0.4, stroke_color=BLUE, stroke_width=4, fill_color=LIME, fill_opacity=0.65).move_to([SX, SSO + 0.08, 0])
        d2 = Circle(radius=0.4, stroke_color=TEXT, stroke_width=4, fill_color=LIME, fill_opacity=0.65).move_to(rc)
        d2.set_z_index(1)
        self.add(d2)
        self.play(Transform(rnd, d1), d2.animate.move_to([SX + 1.2, SSO + 0.08, 0]),
                  g[0].animate.put_start_and_end_on([SX, SSO + 0.48, 0], [SX, 3.05, 0]).set_stroke(width=7),
                  dots[1].animate.set_fill(YELLOW), FadeIn(labs[1]), run_time=1.3)
        self.at("keeps its fiber")
        kf = T("keeps its\nfibre", 34, YELLOW).move_to([SX + 2.4, 1.1, 0])
        kfa = arr([SX + 1.45, 1.1, 0], [SX + 0.15, 1.1, 0], color=YELLOW, w=5)
        self.play(Indicate(g[0], color=YELLOW, scale_factor=1.0), FadeIn(kf), GrowArrow(kfa),
                  dots[2].animate.set_fill(YELLOW), FadeIn(labs[2]), run_time=1.0)
        self.finish()


class S20Climb(SpokenScene):
    def construct(self):
        st, dim = slice_base()
        film = slice_film(bottom=-3.0)
        g = marked_hero()
        gg = glow(g[0])
        d2 = Circle(radius=0.4, stroke_color=TEXT, stroke_width=4, fill_color=LIME, fill_opacity=0.65).move_to([SX + 1.2, SSO + 0.08, 0])
        rat = bchip("Noctor and colleagues\nrat, 2001", GOLD, 26).move_to([-1.9, 2.25, 0])
        # Miyata inset
        panel = RoundedRectangle(corner_radius=0.18, width=4.25, height=5.15, stroke_color=GREY, stroke_width=3).move_to([4.6, -0.38, 0])
        mtag = bchip("Miyata and colleagues\nmouse, 2001", GOLD, 24).move_to([4.6, 1.4, 0])
        ground = Line([2.7, -2.4, 0], [6.5, -2.4, 0], stroke_color=GREY, stroke_width=3)
        psoma = Circle(radius=0.34, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.35).move_to([3.6, -1.6, 0])
        fib = Line([3.6, -1.26, 0], [3.6, 0.65, 0], stroke_color=BLUE, stroke_width=7)
        mneu = neuron(4.55, -1.6, 0.34, proc=False)
        ghost = DashedVMobject(Circle(radius=0.34, stroke_color=GREEN, stroke_width=3), num_dashes=14).move_to([4.55, -1.6, 0])
        fl = T("fibre", 26, BLUE).move_to([4.2, 0.45, 0])
        pl = T("parent", 24, BLUE).move_to([3.6, -2.7, 0])
        nl = T("neuron", 24, GREEN).move_to([5.5, -1.6, 0])
        ledger = led("filming", lchip("scaffold only: no neurons from glia", GREY), lchip("seen: a neuron daughter", TEXT))
        self.add(st, dim, film, gg, g, d2)
        self.at("Its daughter becomes a neuron")
        nn = neuron(SX + 1.2, SSO + 0.08, 0.33, mark=True)
        nlab = T("neuron", 32, GREEN).move_to([SX + 1.6, 1.35, 0])
        pfl = T("parental fibre", 28, BLUE).move_to([SX + 2.55, -0.2, 0])
        pfa = arr([SX + 1.2, -0.2, 0], [SX + 0.2, -0.2, 0], color=BLUE, w=4, tip=0.18)
        self.play(FadeIn(rat), FadeOut(d2), FadeIn(nn, scale=0.6), dim.animate.set_opacity(0.15), FadeIn(ledger[0]), FadeIn(ledger[1]), run_time=0.7)
        self.at("moves out along")
        self.play(nn.animate.move_to([SX + 0.34, 1.3, 0]), FadeIn(pfl), GrowArrow(pfa), run_time=2.0)
        self.play(FadeIn(nlab), FadeIn(ledger[2]), run_time=0.5)
        self.at("and colleagues saw")
        self.play(FadeIn(panel), FadeIn(mtag), FadeIn(ground), FadeIn(psoma), FadeIn(fib), FadeIn(mneu), FadeIn(pl), FadeIn(nl), run_time=0.8)
        self.at("newborn neuron inherit")
        self.play(FadeIn(fl), FadeIn(ghost), Indicate(mneu, color=YELLOW, scale_factor=1.3), run_time=0.8)
        self.at("the fiber itself")
        mv = arr([4.5, -1.2, 0], [3.95, -0.45, 0], color=GREEN, w=4, tip=0.18)
        self.play(GrowArrow(mv), run_time=0.4)
        self.play(mneu.animate.move_to([3.6, -0.1, 0]), nl.animate.move_to([4.65, -0.1, 0]), FadeOut(mv), run_time=1.2)
        self.finish()


# ------------------------------------------------------------- recording scenes
REC_CELLS = [(-5.8, -1.7), (-4.3, -2.0), (-4.5, -0.3), (-0.2, -1.9), (1.2, -1.0), (2.6, -1.9), (4.0, -0.9), (-3.6, 1.1)]
TARGET = np.array([-2.2, -1.5, 0])
TIP = np.array([-1.75, -0.95, 0])
PU = np.array([0.715, 0.7, 0.0])


def rec_cells(color=GREY, op=0.25):
    cs = VGroup(*[Circle(radius=0.55, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=op).move_to([x, y, 0])
                  for x, y in REC_CELLS])
    return cs


def pipette():
    n = np.array([-PU[1], PU[0], 0.0])
    L = 5.0
    tip, end = TIP, TIP + PU * L
    pts = [tip + n * 0.03, end + n * 0.3, end - n * 0.3, tip - n * 0.03]
    outer = Polygon(*pts, stroke_color=TEXT, stroke_width=4, fill_color=BG, fill_opacity=1)
    pts2 = [tip + n * 0.012 + PU * 0.05, end - PU * 0.1 + n * 0.2, end - PU * 0.1 - n * 0.2, tip - n * 0.012 + PU * 0.05]
    inner = Polygon(*pts2, stroke_width=0, fill_color=PINK, fill_opacity=0.85)
    return outer, inner, end


class S21Rec(SpokenScene):
    def construct(self):
        st = stage(-6.6, 6.6, YB)
        cs = rec_cells()
        target = Circle(radius=0.7, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.25).move_to(TARGET)
        plab = T("precursors", 30, GREY).move_to([-5.5, 0.95, 0])
        outer, inner, end = pipette()
        elab = T("electrode", 32, TEXT).move_to([4.6, 2.55, 0])
        elead = arr([3.45, 2.5, 0], [end[0] + 0.3, end[1] + 0.0, 0], color=TEXT, w=3, tip=0.16)
        dlab = T("dye", 36, PINK).move_to([4.0, 1.3, 0])
        dlead = arr([3.45, 1.3, 0], [1.2, 1.25, 0], color=PINK, w=4, tip=0.2)
        self.play(FadeIn(st), FadeIn(cs), FadeIn(target), run_time=0.6)
        self.at("recording")
        self.play(FadeIn(plab), run_time=0.4)
        self.at("precursors")
        self.play(Indicate(cs, color=YELLOW, scale_factor=1.0), run_time=0.7)
        self.at("recorded with an electrode")
        self.play(FadeIn(outer, shift=DOWN * 0.8 + LEFT * 0.8), FadeIn(elab), GrowArrow(elead), run_time=1.1)
        self.play(Indicate(target, color=YELLOW, scale_factor=1.15), run_time=0.6)
        self.at("filled with dye")
        self.play(FadeIn(inner), FadeIn(dlab), GrowArrow(dlead), run_time=0.5)
        fill = Circle(radius=0.05, stroke_width=0, fill_color=PINK, fill_opacity=0.85).move_to(TIP)
        self.add(fill)
        self.play(fill.animate.scale(14).move_to(TARGET), target.animate.set_stroke(PINK), run_time=1.2)
        self.finish()


class S22Recrev(SpokenScene):
    def construct(self):
        st = stage(-6.6, 6.6, YB)
        cs = rec_cells()
        target = Circle(radius=0.7, stroke_color=PINK, stroke_width=3, fill_color=PINK, fill_opacity=0.8).move_to(TARGET)
        outer, inner, end = pipette()
        pip = VGroup(outer, inner)
        self.add(st, cs, target, pip)
        self.at("The filled cells")
        self.play(FadeOut(pip), Indicate(target, color=YELLOW, scale_factor=1.15), run_time=0.8)
        self.at("shape of radial glia")
        fx = TARGET[0]
        fibre = Line([fx, TARGET[1] + 0.7, 0], [fx, 3.05, 0], stroke_color=BLUE, stroke_width=6)
        foot = Line([fx - 0.28, 3.05, 0], [fx + 0.28, 3.05, 0], stroke_color=BLUE, stroke_width=8)
        tail = Line([fx, TARGET[1] - 0.7, 0], [fx, YB + 0.22, 0], stroke_color=BLUE, stroke_width=4)
        rl = T("radial glial\nshape", 32, BLUE).move_to([fx + 2.0, 2.0, 0])
        rla = arr([fx + 1.0, 1.85, 0], [fx + 0.1, 1.5, 0], color=BLUE, w=4, tip=0.18)
        self.play(Create(fibre), Create(tail), run_time=1.4)
        self.play(FadeIn(foot), target.animate.set_stroke(BLUE, width=5), FadeIn(rl), GrowArrow(rla), run_time=0.7)
        self.at("Radial glial markers")
        leg_dot = Dot([3.3, 2.85, 0], radius=0.14, color=BLUE)
        leg = lt("radial glial marker", 26, BLUE, 3.55, 2.85)
        self.play(FadeIn(leg_dot), FadeIn(leg), run_time=0.5)
        self.at("nearly all")
        rings, marks = VGroup(), VGroup()
        cells = [(x, y) for x, y in REC_CELLS] + [(TARGET[0], TARGET[1])]
        skip = 4   # one small exception
        for k, (x, y) in enumerate(cells):
            rr = 0.82 if k == len(cells) - 1 else 0.65
            rings.add(Circle(radius=rr, stroke_color=TEAL, stroke_width=6, fill_opacity=0).move_to([x, y, 0]))
            if k != skip:
                marks.add(Dot([x, y, 0], radius=0.2, color=BLUE).set_z_index(6))
        self.play(FadeIn(rings), LaggedStart(*[FadeIn(m, scale=0.3) for m in marks], lag_ratio=0.1), run_time=1.3)
        self.at("caught in S phase")
        cl = T("cells caught in S phase\nor mitosis", 30, TEAL).move_to([4.7, 1.75, 0])
        cla = arr([4.6, 1.05, 0], [4.1, -0.15, 0], color=TEAL, w=3, tip=0.16)
        few = T("few unmarked", 26, GREY).move_to([1.2, 0.05, 0])
        seen = lchip("seen: glial shape and markers", TEXT)
        ledger = led("recording", lchip("scaffold only: cells look different", GREY), seen)
        self.play(FadeIn(cl), GrowArrow(cla), FadeIn(few), FadeIn(ledger), run_time=0.8)
        self.finish()


class S23Blind(SpokenScene):
    def construct(self):
        grid, hm, rm, a, b, c = full_table()
        self.add(grid, hm[0], hm[1], *rm, *a, *b)
        self.at("blind spot")
        cbox = Rectangle(width=E4[4] - E4[3] - 0.08, height=TOP - ROW_E[-1] - 0.08, stroke_color=RED, stroke_width=4).move_to([(E4[3] + E4[4]) / 2, (TOP + ROW_E[-1]) / 2, 0])
        self.play(FadeIn(hm[2]), Create(cbox), run_time=0.7)
        self.at("a dish shows potential")
        self.play(FadeIn(c[0], scale=1.15), run_time=0.6)
        self.play(Indicate(c[0], color=YELLOW, scale_factor=1.08), run_time=0.6)
        self.at("electrode samples only")
        self.play(FadeIn(c[1], scale=1.15), run_time=0.6)
        self.play(Indicate(c[1], color=YELLOW, scale_factor=1.08), run_time=0.6)
        self.at("marker is not a family tree")
        self.play(FadeIn(c[2], scale=1.15), run_time=0.6)
        self.play(Indicate(c[2], color=YELLOW, scale_factor=1.08), run_time=0.6)
        self.finish()


class S24Differ(SpokenScene):
    def construct(self):
        grid, hm, rm, a, b, c = full_table()
        self.add(grid, *hm, *rm, *a, *b, *c)
        self.at("blind spots differ")
        self.play(LaggedStart(*[Indicate(x, color=YELLOW, scale_factor=1.1) for x in c], lag_ratio=0.2), run_time=1.4)
        self.at("every result")
        cx = (E4[1] + E4[2]) / 2
        frame = Rectangle(width=E4[2] - E4[1] - 0.08, height=ROW_E[0] - ROW_E[-1] - 0.08, stroke_color=YELLOW, stroke_width=5).move_to([cx, (ROW_E[0] + ROW_E[-1]) / 2, 0])
        self.play(Create(frame), run_time=0.7)
        self.at("went against a scaffold only view")
        strikes = []
        for i in range(4):
            for t in a[i]:
                mid = t.get_center()[1] + 0.03
                p0, p1 = [t.get_left()[0] - 0.1, mid, 0], [t.get_right()[0] + 0.1, mid, 0]
                if i in (1, 2):
                    strikes.append(Line(p0, p1, stroke_color=RED, stroke_width=4))
                else:
                    strikes.append(DashedLine(p0, p1, dash_length=0.13, stroke_color=RED, stroke_width=4))
        self.play(LaggedStart(*[Create(s) for s in strikes], lag_ratio=0.12), run_time=1.5)
        self.at("fate map and the films")
        h2 = RoundedRectangle(corner_radius=0.1, width=E4[-1] - E4[0] - 0.1, height=ROW_E[1] - ROW_E[3] - 0.1,
                              stroke_color=GREEN, stroke_width=5).move_to([(E4[0] + E4[-1]) / 2, (ROW_E[1] + ROW_E[3]) / 2, 0])
        tags = [T("ancestry seen", 22, GREEN).move_to([(E4[0] + E4[1]) / 2, row_y(i) - 0.3, 0]) for i in (1, 2)]
        self.play(FadeOut(frame), Create(h2), rm[1].animate.shift(UP * 0.22), rm[2].animate.shift(UP * 0.22), run_time=0.8)
        self.at("neuronal ancestry directly")
        al = T("ancestry seen directly", 34, GREEN).move_to([0, -3.5, 0])
        self.play(FadeIn(tags[0]), FadeIn(tags[1]), FadeIn(al), run_time=0.7)
        self.finish()


class S25Take(SpokenScene):
    def construct(self):
        yb = -3.2
        so = yb + 0.47
        st = stage(-6.6, 2.0, yb, plab=False)
        xs = [-5.9, -4.7, -3.5, -2.3, -1.1, 0.1]
        hero = 0.1
        nb = dims(xs[:-1], so)
        g = glia(hero, so)
        n = neuron(hero + 0.42, so + 1.1)
        scope = T("embryonic\nrodent cortex", 30, GREY).move_to([4.75, 3.2, 0])
        g1 = bchip("guides migrating\nneurons", BLUE, 32).move_to([4.75, 1.5, 0])
        t1 = arr([g1.get_left()[0], 1.5, 0], [hero + 0.85, 1.5, 0], color=BLUE, w=4)
        g2 = bchip("makes most\nof them", BLUE, 32).move_to([4.75, -1.9, 0])
        t2 = arr([g2.get_left()[0], -1.9, 0], [hero + 0.4, so + 0.15, 0], color=BLUE, w=4)
        pia = T("pia", 24, GREY).move_to([-6.1, 3.6, 0])
        self.add(st, nb, g, n, pia)
        self.at("embryonic rodent cortex")
        self.play(FadeIn(scope), run_time=0.5)
        self.at("the cell that guides migrating neurons")
        self.play(n.animate.set_y(1.5), FadeIn(g1), GrowArrow(t1), run_time=1.6)
        self.at("is also the cell")
        self.play(FadeIn(g2), GrowArrow(t2), Indicate(g, color=YELLOW, scale_factor=1.03), run_time=0.9)
        self.at("makes most of them")
        for y in (-1.4, -0.5, 0.4):
            b = neuron(hero - 0.68, so + 0.05)
            self.play(FadeIn(b, scale=0.4), run_time=0.2)
            self.play(b.animate.move_to([hero - 0.68, y, 0]), run_time=0.4)
        self.finish()


class S26End(EndCard):
    LINE = "In embryonic rodent cortex, the guiding cell also makes most neurons."
