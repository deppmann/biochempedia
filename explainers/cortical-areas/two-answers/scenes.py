"""Cortical areas, chapter 2: Two Answers, a Year Apart  (Biochemistrypedia explainer)

Two ideas for where the cortical map comes from: Rakic's protomap (in the dividing cells) and
O'Leary's protocortex (brought in by thalamic axons). Then the three early proxies used to read a map.

COLOR MAP (one color per concept, shared with every chapter of this lesson)
  PURPLE = motor area            GREEN  = touch area, and its barrels
  PINK   = visual area           ORANGE = Emx2          BLUE   = Pax6
  YELLOW = FGF8 (not drawn in this chapter)
  TEXT   = thalamic axons (the input); also the protocortex idea (it is about the input)
  GOLD   = the protomap idea (it is about the dividing cells); NOT used before the answer is revealed
  TEAL   = the dye, in the connection proxy
  STAIN  = the gene stain in the marker-gene proxy (a royal blue, away from the motor lavender)
  RED    = something removed / crossed out / died
  GREY   = the sheet, labels, de-emphasized
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58BB5"
STAIN = "#3D6BFF"
DYE = TEAL
AREA_COL = [PURPLE, GREEN, PINK]
AREA_NAME = ["motor", "touch", "vision"]
WT = (0.38, 0.70)          # borders of the normal map, as fractions front to back
LBLC = "#C9CEDA"           # structural labels: light grey, readable on the dark ground
CELLC = "#AEB5C4"          # neutral progenitor cells
WHITE = "#FFFFFF"

# ---- the embryonic wall (side view, cut through) -------------------------------------------
WX0, WW = -5.2, 8.6
W_TOP, VZ_TOP, W_BOT, V_BOT = 2.1, -0.9, -2.2, -3.3
WXR = WX0 + WW
PEDGE = [WX0, WX0 + WT[0] * WW, WX0 + WT[1] * WW, WX0 + WW]            # patch / band edges
PC = [(PEDGE[i] + PEDGE[i + 1]) / 2 for i in range(3)]                  # patch centres
FIB = [c + d for c in PC for d in (-0.6, 0.6)]                          # radial-glia x positions
LBL_X = 3.75


def patch_of(x):
    return 0 if x < PEDGE[1] else (1 if x < PEDGE[2] else 2)


def wall_parts():
    wall = Rectangle(width=WW, height=W_TOP - W_BOT, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                     fill_opacity=0.08).move_to([WX0 + WW / 2, (W_TOP + W_BOT) / 2, 0])
    vz = Rectangle(width=WW, height=VZ_TOP - W_BOT, stroke_color=GREY, stroke_width=2, fill_color=GREY,
                   fill_opacity=0.28).move_to([WX0 + WW / 2, (VZ_TOP + W_BOT) / 2, 0])
    vent = Rectangle(width=WW, height=W_BOT - V_BOT, stroke_color=GREY, stroke_width=2, fill_color="#24496B",
                     fill_opacity=0.75).move_to([WX0 + WW / 2, (W_BOT + V_BOT) / 2, 0])
    return wall, vz, vent


def vz_cells(tinted=False, color=CELLC, r=0.15):
    g = VGroup()
    for j in range(2):
        for i in range(14):
            x = WX0 + 0.4 + i * (WW - 0.95) / 13 + 0.15 * (j % 2)
            c = AREA_COL[patch_of(x)] if tinted else color
            g.add(Circle(radius=r, stroke_color=c, stroke_width=2, fill_color=c, fill_opacity=0.8).move_to(
                [x, -1.35 - 0.45 * j, 0]))
    return g


def fibres(op=1.0):
    return VGroup(*[Line([x, W_BOT, 0], [x, W_TOP, 0], stroke_color="#C9D0DE", stroke_width=8, stroke_opacity=op)
                    for x in FIB])


def neuron(x, y, color=TEXT, r=0.16):
    return Circle(radius=r, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=0.9).move_to([x, y, 0])


def column_dots():
    g = VGroup()
    for x in FIB:
        g.add(VGroup(*[neuron(x, -0.45 + 0.55 * j, AREA_COL[patch_of(x)]) for j in range(5)]))
    return g


def make_map(x0, w, cy, h, labels=True, op=0.4, sw=3, size=28):
    xs = [x0, x0 + WT[0] * w, x0 + WT[1] * w, x0 + w]
    blocks, labs = VGroup(), VGroup()
    for i in range(3):
        r = Rectangle(width=xs[i + 1] - xs[i], height=h, stroke_color=AREA_COL[i], stroke_width=sw,
                      fill_color=AREA_COL[i], fill_opacity=op).move_to([(xs[i] + xs[i + 1]) / 2, cy, 0])
        blocks.add(r)
        if labels:
            labs.add(T(AREA_NAME[i], size, WHITE, weight=BOLD).move_to(r.get_center()))
    return VGroup(blocks, labs)


def pencil_map(x0, w, cy, h, soft=0.06, n=60):
    """A pencil sketch of the map: soft grey tone, dashed pencil outline, wobbly double-stroked borders (no hairlines)."""
    g = VGroup()
    cx = x0 + w / 2
    g.add(Rectangle(width=w, height=h, stroke_width=0, fill_color="#C9CEDA", fill_opacity=0.12).move_to([cx, cy, 0]))
    xm = (WT[0] + WT[1]) / 2
    g.add(Rectangle(width=(WT[1] - WT[0]) * w, height=h, stroke_width=0, fill_color="#C9CEDA", fill_opacity=0.14).move_to(
        [x0 + xm * w, cy, 0]))
    g.add(DashedVMobject(Rectangle(width=w, height=h, stroke_color=LBLC, stroke_width=4), num_dashes=46).move_to([cx, cy, 0]))
    for f in WT:
        for k, off in enumerate((-0.07, 0.07)):
            pts = [[x0 + f * w + off + 0.05 * np.sin(6 * t + 2 * k) , cy - h / 2 + t * h, 0] for t in np.linspace(0, 1, 24)]
            m = VMobject(stroke_color=LBLC, stroke_width=3, stroke_opacity=0.8)
            m.set_points_smoothly([np.array(p) for p in pts])
            g.add(DashedVMobject(m, num_dashes=14))
    return g


def idea_head(word, name, color):
    h = T(word, 54, color, font=TITLE_FONT, weight=BOLD)
    n = T(name, 32, LBLC)
    return VGroup(h, n).arrange(RIGHT, buff=0.55, aligned_edge=DOWN).move_to([-1.2, 3.25, 0])


def box(w, h, cx, cy, color=GREY, fo=0.1, sw=3, r=0.2):
    return RoundedRectangle(corner_radius=r, width=w, height=h, stroke_color=color, stroke_width=sw,
                            fill_color=color, fill_opacity=fo).move_to([cx, cy, 0])


def bundle(x0, y0, x1, y1, color, n=3, s0=0.12, s1=0.4, sw=4, op=1.0):
    g = VGroup()
    for o in (np.linspace(-1, 1, n) if n > 1 else [0.0]):
        g.add(CubicBezier([x0 + o * s0, y0, 0], [x0 + o * s0, (y0 + y1) / 2, 0], [x1 + o * s1, (y0 + y1) / 2, 0],
                          [x1 + o * s1, y1, 0], stroke_color=color, stroke_width=sw, stroke_opacity=op))
    return g


def check(cx, cy, s=1.0):
    c = VMobject(stroke_color=GREEN, stroke_width=8)
    c.set_points_as_corners([[-0.25 * s, 0.0, 0], [-0.07 * s, -0.22 * s, 0], [0.3 * s, 0.26 * s, 0]])
    return c.move_to([cx, cy, 0])


def pup(cx, cy, s=1.0):
    """A newborn mouse pup: pink and hairless, solid shapes so nothing shows through."""
    c, dark = "#EDA7A2", "#D58A8A"
    tail = CubicBezier([1.05, -0.1, 0], [1.6, -0.5, 0], [1.5, 0.3, 0], [1.95, 0.1, 0], stroke_color=c, stroke_width=6)
    body = Ellipse(width=2.4, height=1.3, stroke_color=c, stroke_width=3, fill_color=c, fill_opacity=1)
    head = Circle(radius=0.58, stroke_color=c, stroke_width=3, fill_color=c, fill_opacity=1).move_to([-1.25, 0.08, 0])
    ear = Circle(radius=0.17, stroke_color=dark, stroke_width=2, fill_color=dark, fill_opacity=1).move_to([-1.05, 0.6, 0])
    paw1 = Ellipse(width=0.5, height=0.28, stroke_color=dark, stroke_width=2, fill_color=dark, fill_opacity=1).move_to([-0.75, -0.55, 0])
    paw2 = Ellipse(width=0.5, height=0.28, stroke_color=dark, stroke_width=2, fill_color=dark, fill_opacity=1).move_to([0.6, -0.6, 0])
    eye = Line([-1.55, 0.2, 0], [-1.35, 0.2, 0], stroke_color="#6B3F3F", stroke_width=4)
    nose = Dot([-1.82, 0.02, 0], radius=0.07, color="#B76868")
    g = VGroup(tail, body, paw2, head, ear, paw1, eye, nose)
    return g.scale(s).move_to([cx, cy, 0])


def lab(text, x, y, size=26, color=LBLC, **kw):
    return T(text, size, color, **kw).move_to([x, y, 0])


def side_label(text, y, target_x=None, color=LBLC, size=26, x=LBL_X, line_spacing=0.9):
    """A label in the right-hand column with an optional thin leader line to the thing it names."""
    t = T(text, size, color, line_spacing=line_spacing).move_to([x, y, 0], aligned_edge=LEFT)
    g = VGroup(t)
    if target_x is not None:
        g.add(Line([x - 0.1, y, 0], [target_x, y, 0], stroke_color=color, stroke_width=2.5))
    return g


def wall_labels():
    surf = side_label("surface", 2.0, WXR)
    vzl = side_label("ventricular zone", -1.55, WXR)
    ven = side_label("ventricle", -2.75, WXR)
    return surf, vzl, ven


# =============================================================================================
class S00Title(TitleCard):
    LESSON = "Mapping the Cortex: Areas and Arealization"
    TITLE = "Two Answers, a Year Apart"

    def construct(self):
        brand = T("BIOCHEMISTRYPEDIA", size=22, color=TEAL, weight=BOLD)
        lesson = T(self.LESSON.upper(), size=24, color=LBLC)
        title = T(self.TITLE, size=56, font=TITLE_FONT)
        fit(title, max_w=11.5)
        rule = Line(LEFT * 1.4, RIGHT * 1.4, color=GOLD, stroke_width=4)
        g = VGroup(brand, lesson, title, rule).arrange(DOWN, buff=0.34)
        self.play(FadeIn(brand, shift=UP * 0.1), FadeIn(lesson, shift=UP * 0.1), run_time=self.beat(0.25))
        self.play(FadeIn(title, shift=UP * 0.1), GrowFromCenter(rule), run_time=self.beat(0.35))
        self.wait(self.beat(0.2))
        self.play(FadeOut(g), run_time=self.beat(0.2))
        self.finish()


# ---------------------------------------------------------------------------------------------
SHX, SHW, SHY, SHH = -5.5, 11.0, 1.2, 2.2      # s01 sheet
TH_Y = -2.9


class S01(SpokenScene):
    """The smooth sheet with a thalamus below it. The question, drawn: in the cells, or from the axons?"""

    def construct(self):
        q = T("Is the map already in the dividing cells,\nor brought in by the axons that arrive?", 34, TEXT,
              font=TITLE_FONT, line_spacing=0.9)
        fit(q, max_w=12.4)
        q.move_to([0, 3.0, 0])
        sheet = Rectangle(width=SHW, height=SHH, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                          fill_opacity=0.22).move_to([0, SHY, 0])
        sl = lab("cortical sheet", 4.0, SHY, 28, LBLC)
        self.play(FadeIn(q, shift=DOWN * 0.1), FadeIn(sheet), FadeIn(sl), run_time=0.7)
        cells = VGroup(*[Circle(radius=0.17, stroke_color=CELLC, stroke_width=2, fill_color=CELLC, fill_opacity=0.85).move_to(
            [-4.9 + 0.7 * i, SHY + (0.42 if i % 2 else -0.42), 0]) for i in range(12)])
        self.at("dividing cells")
        self.play(LaggedStart(*[FadeIn(c, scale=0.4) for c in cells], lag_ratio=0.06), run_time=0.9)
        tbox = box(SHW, 0.9, 0, TH_Y, GREY, 0.14, 3, 0.15)
        tl = lab("thalamus", 0, TH_Y, 28, LBLC)
        self.at("or is it")
        self.play(FadeIn(tbox), FadeIn(tl), run_time=0.5)
        ax = VGroup(*[bundle(x, TH_Y + 0.45, x, SHY - SHH / 2, TEXT, n=3, s0=0.15, s1=0.4, sw=5) for x in (-3.4, 0.0, 3.4)])
        self.at("brought in")
        self.play(LaggedStart(*[Create(a) for a in ax], lag_ratio=0.25), run_time=1.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
def name_card(name, year, color, cx):
    b = box(6.0, 5.2, cx, 0.0, color, 0.1, 4, 0.3)
    n = T(name, 72, TEXT, font=TITLE_FONT)
    y = T(year, 60, color, font=MONO, weight=BOLD)
    VGroup(n, y).arrange(DOWN, buff=0.5).move_to(b)
    return VGroup(b, n, y)


class S02(SpokenScene):
    def construct(self):
        c1 = name_card("Rakic", "1988", GOLD, -3.6)
        c2 = name_card("O'Leary", "1989", TEXT, 3.6)
        arr = DoubleArrow([-0.55, 0.0, 0], [0.55, 0.0, 0], buff=0, color=LBLC, stroke_width=5, tip_length=0.22)
        self.play(FadeIn(c1, shift=RIGHT * 0.3), run_time=0.5)
        self.at("a year apart")
        self.play(FadeIn(c2, shift=LEFT * 0.3), GrowFromCenter(arr), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03(SpokenScene):
    """Rakic 1988: protomap. A cutaway of the embryonic cortical wall, progenitors visible from the first moment."""

    def construct(self):
        wall, vz, vent = wall_parts()
        cells = vz_cells()
        cap = side_label("embryonic\ncortical wall,\ncut through", 0.2, WXR)
        self.play(FadeIn(wall, shift=UP * 0.15), FadeIn(vent, shift=UP * 0.15), FadeIn(cells), FadeIn(cap), run_time=0.8)
        head = idea_head("protomap", "Rakic, 1988", GOLD)
        self.at("pasko")
        self.play(FadeIn(head[1], shift=DOWN * 0.1), run_time=0.5)
        self.at("proposed the protomap")
        self.play(FadeIn(head[0], shift=UP * 0.1), run_time=0.8)
        self.finish()


class S04(SpokenScene):
    def construct(self):
        wall, vz, vent = wall_parts()
        cells = vz_cells()
        self.add(wall, vent, cells)
        surf, l_vz, l_v = wall_labels()
        self.play(Indicate(cells, color=TEXT, scale_factor=1.08), run_time=1.0)
        self.at("ventricular zone")
        self.play(FadeIn(vz), vz.animate.set_stroke(color=TEXT, width=4), FadeIn(l_vz, shift=LEFT * 0.2), run_time=0.8)
        self.at("layer of the brain wall")
        self.play(Indicate(vz, color=TEXT, scale_factor=1.03), run_time=0.9)
        self.at("next to the")
        self.play(Indicate(vent, color="#6FA8DC", scale_factor=1.02), run_time=0.6)
        self.at("filled ventricle")
        self.play(FadeIn(l_v, shift=LEFT * 0.2), Indicate(vent, color="#6FA8DC", scale_factor=1.03), run_time=0.9)
        self.finish()


def static_wall(with_cells=True):
    wall, vz, vent = wall_parts()
    vz.set_stroke(color=TEXT, width=4)
    return wall, vz, vent


class S05(SpokenScene):
    def construct(self):
        wall, vz, vent = static_wall()
        cells = vz_cells()
        surf, l_vz, l_v = wall_labels()
        self.add(wall, vz, vent, cells, l_vz, l_v)
        fib = fibres()
        ns = VGroup(*[neuron(x, -0.7) for x in FIB] + [neuron(x, -0.7) for x in FIB])
        rg = side_label("radial glia", 0.7, FIB[-1] + 0.1, color="#C9D0DE", size=30)
        self.play(LaggedStart(*[FadeIn(n, scale=0.4) for n in ns], lag_ratio=0.04), run_time=0.7)
        self.at("climb outward")
        self.play(LaggedStart(*[Create(f) for f in fib], lag_ratio=0.08), FadeIn(surf, shift=LEFT * 0.2), run_time=0.7)
        self.at("along radial")
        climb = [n.animate.move_to([n.get_x(), 1.5 if k < 6 else 0.4, 0]) for k, n in enumerate(ns)]
        self.play(AnimationGroup(LaggedStart(*climb, lag_ratio=0.08), Succession(Wait(0.4), FadeIn(rg)), lag_ratio=0.0),
                  run_time=1.95)
        self.at("scaffold cells")
        self.play(Indicate(fib, color=TEXT, scale_factor=1.0), run_time=0.8)
        span = DoubleArrow([WX0 - 0.3, W_BOT, 0], [WX0 - 0.3, W_TOP, 0], buff=0, color=LBLC, stroke_width=5, tip_length=0.22)
        self.at("span the wall")
        self.play(GrowFromCenter(span), run_time=0.7)
        self.finish()


def patch_tints():
    return VGroup(*[Rectangle(width=PEDGE[i + 1] - PEDGE[i] - 0.06, height=VZ_TOP - W_BOT - 0.06, stroke_width=0,
                              fill_color=AREA_COL[i], fill_opacity=0.30).move_to([PC[i], (VZ_TOP + W_BOT) / 2, 0])
                    for i in range(3)])


def rg_label():
    return side_label("radial glia", 0.7, FIB[-1] + 0.1, color="#C9D0DE", size=30)


class S06(SpokenScene):
    def construct(self):
        wall, vz, vent = static_wall()
        cells = vz_cells()
        fib = fibres(0.55)
        ns = VGroup(*[neuron(x, 1.5) for x in FIB] + [neuron(x, 0.4) for x in FIB])
        surf, l_vz, l_v = wall_labels()
        self.add(wall, vz, vent, cells, fib, ns, surf, l_vz, l_v, rg_label())
        cells_t = vz_cells(tinted=True)
        patches = patch_tints()
        cols = column_dots()
        self.at("neurons born")
        self.play(FadeOut(ns), FadeIn(patches), Transform(cells, cells_t), run_time=0.8)
        self.at("one patch")
        self.play(Indicate(patches[0], color=PURPLE, scale_factor=1.04), run_time=0.7)
        self.at("stack up")
        self.play(LaggedStart(*[LaggedStart(*[FadeIn(n, scale=0.4) for n in col], lag_ratio=0.12) for col in cols],
                              lag_ratio=0.18), run_time=1.5)
        self.finish()


MAP_Y, MAP_H = 3.15, 0.95


class S07(SpokenScene):
    def construct(self):
        wall, vz, vent = static_wall()
        cells_t = vz_cells(tinted=True)
        patches = patch_tints()
        cols = column_dots()
        fib = fibres(0.4)
        surf, l_vz, l_v = wall_labels()
        self.add(wall, vz, vent, patches, fib, cells_t, cols, surf, l_vz, l_v)
        outline = make_map(WX0, WW, MAP_Y, MAP_H, labels=False, op=0.0, sw=2.5)
        for r in outline[0]:
            r.set_stroke(color=LBLC)
        strip = make_map(WX0, WW, MAP_Y, MAP_H, op=0.5, sw=3, size=28)
        links = [DashedLine([c, W_TOP + 0.05, 0], [c, MAP_Y - MAP_H / 2, 0], color=AREA_COL[i], stroke_width=4) for i, c in enumerate(PC)]
        front = T("front", 26, LBLC).move_to([WX0 - 0.95, MAP_Y, 0])
        back = T("back", 26, LBLC).move_to([WXR + 0.75, MAP_Y, 0])
        cap = T("map seen\nfrom above", 26, LBLC, line_spacing=0.9).move_to([WXR + 1.35, MAP_Y, 0], aligned_edge=LEFT)
        self.at("differ by position")
        self.play(*[Indicate(p, color=AREA_COL[i], scale_factor=1.04) for i, p in enumerate(patches)], run_time=1.0)
        self.at("outline of the areas")
        self.play(Create(outline), FadeIn(front), FadeIn(back), FadeIn(cap), run_time=0.8)
        self.at("laid down")
        self.play(LaggedStart(*[AnimationGroup(FadeIn(strip[0][i]), FadeIn(strip[1][i]), Create(links[i]))
                                for i in range(3)], lag_ratio=0.3), run_time=0.7)
        self.at("where the cells are made")
        self.play(*[Indicate(p, color=AREA_COL[i], scale_factor=1.04) for i, p in enumerate(patches)], run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
CPX, CPW, CPY, CPH = -1.2, 9.4, -0.55, 5.8


def city_parts():
    outline = Rectangle(width=CPW, height=CPH, stroke_color=LBLC, stroke_width=3, fill_opacity=0).move_to([CPX, CPY, 0])
    ix0, iw = CPX - CPW / 2 + 0.2, CPW - 0.4
    edges = [ix0, ix0 + WT[0] * iw, ix0 + WT[1] * iw, ix0 + iw]
    zones, lots = VGroup(), VGroup()
    zc = []
    for i in range(3):
        w = edges[i + 1] - edges[i] - 0.1
        cx = (edges[i] + edges[i + 1]) / 2
        zc.append(cx)
        zones.add(Rectangle(width=w, height=CPH - 0.4, stroke_color=AREA_COL[i], stroke_width=3, fill_color=AREA_COL[i],
                            fill_opacity=0.4).move_to([cx, CPY, 0]))
        for dx in (-0.65, 0.65):
            for y in (CPY + 1.75, CPY, CPY - 1.75):
                lots.add(DashedVMobject(Square(side_length=1.0, stroke_color=TEXT, stroke_width=3), num_dashes=24).move_to(
                    [cx + dx, y, 0]))
    dl = side_label("district = area", CPY + 2.4, zc[2] + 1.0, color=WHITE, size=28, x=4.0)
    hl = side_label("house = neuron", CPY, zc[2] + 1.65, color=WHITE, size=28, x=4.0)
    return outline, zones, lots, dl, hl


class S08(SpokenScene):
    def construct(self):
        strip = make_map(WX0, WW, MAP_Y, MAP_H, op=0.5, size=28)
        self.add(strip)
        outline, zones, lots, dl, hl = city_parts()
        self.at("a city")
        self.play(Create(outline), FadeOut(strip[1]), run_time=0.5)
        self.at("zoned into")
        self.play(*[ReplacementTransform(strip[0][i], zones[i]) for i in range(3)], run_time=0.8)
        self.at("districts")
        self.play(FadeIn(dl, shift=LEFT * 0.2), run_time=0.5)
        self.at("before a single")
        self.play(LaggedStart(*[Create(l) for l in lots], lag_ratio=0.03), run_time=0.8)
        self.at("house")
        self.play(FadeIn(hl, shift=LEFT * 0.2), Indicate(lots[7], color=TEXT, scale_factor=1.25), run_time=0.45)
        self.at("is built")
        self.play(Indicate(lots[9], color=TEXT, scale_factor=1.25), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
def grey_wall():
    return Rectangle(width=WW, height=W_TOP - W_BOT, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                     fill_opacity=0.3).move_to([WX0 + WW / 2, (W_TOP + W_BOT) / 2, 0])


def wall_cap():
    return side_label("embryonic\ncortical wall", 0.2, WXR)


class S09(SpokenScene):
    """O'Leary 1989: protocortex. A uniform grey wall."""

    def construct(self):
        outline, zones, lots, dl, hl = city_parts()
        old = VGroup(outline, zones, lots, dl, hl)
        self.add(old)
        wall = grey_wall()
        capw = wall_cap()
        cen = wall.get_center().copy()
        wall.scale(1.25).move_to([cen[0] - 0.5, 0.0, 0])
        self.play(FadeOut(old), run_time=0.5)
        self.play(FadeIn(wall), run_time=0.6)
        head = idea_head("protocortex", "O'Leary, 1989", TEXT)
        self.at("dennis")
        self.play(FadeIn(head[1], shift=DOWN * 0.1), run_time=0.5)
        self.at("proposed the protocortex")
        self.play(FadeIn(head[0], shift=UP * 0.1), wall.animate.scale(1 / 1.25).move_to(cen), FadeIn(capw), run_time=0.8)
        self.finish()


def grey_vz():
    return Rectangle(width=WW, height=VZ_TOP - W_BOT, stroke_width=0, fill_color=GREY, fill_opacity=0.28).move_to(
        [WX0 + WW / 2, (VZ_TOP + W_BOT) / 2, 0])


class S10(SpokenScene):
    def construct(self):
        wall = grey_wall()
        head = idea_head("protocortex", "O'Leary, 1989", TEXT)
        capw = wall_cap()
        self.add(wall, head, capw)
        vz = grey_vz()
        cells = vz_cells()
        cx = WX0 + WW / 2
        same = T("same everywhere", 48, TEXT, font=TITLE_FONT, weight=BOLD).move_to([cx, 0.85, 0])
        eq = DoubleArrow([WX0 + 0.5, 0.0, 0], [WXR - 0.5, 0.0, 0], buff=0, color=TEXT, stroke_width=6, tip_length=0.25)
        self.at("young sheet")
        self.play(FadeIn(vz), FadeIn(cells), run_time=0.8)
        self.at("similar potential")
        self.play(GrowFromCenter(eq), run_time=0.7)
        self.at("everywhere")
        self.play(FadeIn(same, shift=UP * 0.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
SX0, SW, SCY, SH = -5.5, 11.0, 1.3, 1.9          # the young sheet, seen from the side as a bar
SBX = [SX0 + SW * f for f in (0.19, 0.54, 0.85)]  # where the three bundles land
TY = -2.9                                         # thalamus box


def sheet_bar(op=0.3):
    return Rectangle(width=SW, height=SH, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                     fill_opacity=op).move_to([SX0 + SW / 2, SCY, 0])


def thal_box():
    return box(SW, 0.9, 0, TY, GREY, 0.14, 3, 0.15)


def thal_label():
    return T("thalamus", 26, LBLC).move_to([SX0 + 0.12, TY, 0], aligned_edge=LEFT)


def bundles(op=1.0):
    return VGroup(*[bundle(x, TY + 0.45, x, SCY - SH / 2, AREA_COL[i], n=3, s0=0.2, s1=0.35, sw=6, op=op)
                    for i, x in enumerate(SBX)])


class S11(SpokenScene):
    def construct(self):
        head = idea_head("protocortex", "O'Leary, 1989", TEXT)
        wall = grey_wall()
        vz = grey_vz()
        cells = vz_cells()
        capw = wall_cap()
        self.add(head, wall, vz, cells, capw)
        sheet = sheet_bar()
        tb = thal_box()
        self.play(FadeOut(vz), FadeOut(cells), FadeOut(capw), ReplacementTransform(wall, sheet), FadeIn(tb), run_time=1.2)
        bs = bundles()
        self.at("the axons")
        self.play(LaggedStart(*[Create(b) for b in bs], lag_ratio=0.25), run_time=1.6)
        tl = thal_label()
        self.at("thalamus")
        self.play(FadeIn(tl, shift=RIGHT * 0.1), Indicate(tb, color=TEXT, scale_factor=1.02), run_time=0.7)
        self.finish()


class S12(SpokenScene):
    def construct(self):
        head = idea_head("protocortex", "O'Leary, 1989", TEXT)
        sheet = sheet_bar()
        tb = thal_box()
        bs = bundles()
        tl = thal_label()
        self.add(head, sheet, tb, bs, tl)
        nuc = VGroup(*[Circle(radius=0.3, stroke_color=AREA_COL[i], stroke_width=3, fill_color=AREA_COL[i],
                              fill_opacity=0.8).move_to([x, TY, 0]) for i, x in enumerate(SBX)])
        self.at("thalamic nuclei")
        self.play(LaggedStart(*[FadeIn(n, scale=0.4) for n in nuc], lag_ratio=0.2), run_time=0.9)
        pulses = [Dot(color=AREA_COL[i], radius=0.16).move_to([x, TY + 0.45, 0]) for i, x in enumerate(SBX)]
        self.at("send axons")
        self.play(*[MoveAlongPath(p, bs[i][1]) for i, p in enumerate(pulses)], run_time=1.2, rate_func=linear)
        glows = VGroup(*[Circle(radius=0.28, stroke_color=AREA_COL[i], stroke_width=5, fill_color=AREA_COL[i],
                                fill_opacity=0.5).move_to([x, SCY - SH / 2, 0]) for i, x in enumerate(SBX)])
        self.at("different parts")
        self.play(FadeOut(VGroup(*pulses)), LaggedStart(*[FadeIn(g, scale=0.5) for g in glows], lag_ratio=0.25), run_time=0.7)
        xs = [SX0, SX0 + SW * WT[0], SX0 + SW * WT[1], SX0 + SW]
        tint = VGroup(*[Rectangle(width=xs[i + 1] - xs[i], height=SH, stroke_width=0, fill_color=AREA_COL[i],
                                  fill_opacity=0.55).move_to([(xs[i] + xs[i + 1]) / 2, SCY, 0]) for i in range(3)])
        self.at("the input tells")
        self.play(LaggedStart(*[AnimationGroup(FadeIn(tint[i]), FadeOut(glows[i])) for i in range(3)], lag_ratio=0.3),
                  run_time=1.1)
        labs = VGroup(*[T(AREA_NAME[i], 32, WHITE, weight=BOLD).move_to([(xs[i] + xs[i + 1]) / 2, SCY, 0]) for i in range(3)])
        self.at("what to become")
        self.play(FadeIn(labs, shift=UP * 0.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
CW, CTOP, CBOT = 6.8, 3.85, -2.95
CH = CTOP - CBOT
CY = (CTOP + CBOT) / 2
CXL, CXR = -3.5, 3.5
PXO = 2.0   # pictogram centre, left of the card centre
ROW_Y = (1.2, -1.3)
HEAD_Y = 3.15
PW = 2.5     # pictogram width
CHK_Y = -3.5


def strip_bar(cx, cy, color, op=0.5, h=1.3):
    c = GREY if color is None else color
    return Rectangle(width=PW, height=h, stroke_color=c, stroke_width=3, fill_color=c,
                     fill_opacity=0.3 if color is None else op).move_to([cx, cy, 0])


def up_arrow(cx, cy, color):
    return Arrow([cx, cy - 0.55, 0], [cx, cy + 0.55, 0], buff=0, color=color, stroke_width=9, tip_length=0.32,
                 max_tip_length_to_length_ratio=0.5)


def pict_L1(px, y):
    sq = VGroup(*[Rectangle(width=0.8, height=1.7, stroke_color=AREA_COL[i], stroke_width=3, fill_color=AREA_COL[i],
                            fill_opacity=0.6).move_to([px + (i - 1) * 0.85, y + 0.4, 0]) for i in range(3)])
    line = Line([px - PW / 2, y - 0.7, 0], [px + PW / 2, y - 0.7, 0], stroke_color=LBLC, stroke_width=4)
    return VGroup(sq, line)


def pict_L2(px, y):
    m = make_map(px - PW / 2, PW, y + 0.8, 1.1, labels=False, op=0.6, sw=3)[0]
    bar = Rectangle(width=PW, height=0.6, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.2).move_to(
        [px, y - 0.25, 0])
    bl = T("thalamus", 26, LBLC).move_to(bar)
    # the red line sits below the bar, not through the word
    strike = Line([px - PW / 2, y - 0.62, 0], [px + PW / 2, y - 0.62, 0], stroke_color=RED, stroke_width=7)
    no = T("no input", 28, RED, weight=BOLD).move_to([px, y - 1.05, 0])
    return VGroup(m, bar, bl, strike, no)


def pict_R(px, y, strip_col, arrow_col):
    s = strip_bar(px, y + 0.6, strip_col, h=1.3)
    a = up_arrow(px, y - 0.65, arrow_col)
    return VGroup(s, a)


def item(kind, y, cx):
    px = cx - PXO
    if kind == "L1":
        pic = pict_L1(px, y)
        cap = "molecular\ndifferences across\nthe progenitors"
    elif kind == "L2":
        pic = pict_L2(px, y)
        cap = "some map that\nforms without\nthalamic input"
    elif kind == "R1":
        pic = pict_R(px, y, None, PURPLE)
        cap = "young cortex\ngiven new input"
    else:
        pic = pict_R(px, y, GREEN, GREEN)
        cap = "features that\nmatch the input"
    c = T(cap, 28, TEXT, line_spacing=0.9).move_to([cx - 0.45, y - 0.05, 0], aligned_edge=LEFT)
    return VGroup(pic, c)


def slot(cx):
    s = DashedVMobject(RoundedRectangle(corner_radius=0.18, width=4.8, height=0.95, stroke_color=GREY, stroke_width=3),
                       num_dashes=40).move_to([cx, HEAD_Y, 0])
    q = T("?", 48, LBLC, weight=BOLD).move_to([cx, HEAD_Y, 0])
    return VGroup(s, q)


def placeholder(cx, y):
    return DashedVMobject(RoundedRectangle(corner_radius=0.18, width=6.4, height=2.4, stroke_color=GREY, stroke_width=2),
                          num_dashes=44).move_to([cx, y, 0]).set_stroke(opacity=0.5)


def cards_state(lcol=GREY, rcol=GREY):
    d = {}
    d["lf"] = box(CW, CH, CXL, CY, lcol, 0.05, 3.5, 0.25)
    d["rf"] = box(CW, CH, CXR, CY, rcol, 0.05, 3.5, 0.25)
    d["lslot"] = slot(CXL)
    d["rslot"] = slot(CXR)
    d["lhead"] = T("protomap", 44, GOLD, font=TITLE_FONT, weight=BOLD).move_to([CXL, HEAD_Y, 0])
    d["rhead"] = T("protocortex", 44, TEXT, font=TITLE_FONT, weight=BOLD).move_to([CXR, HEAD_Y, 0])
    d["litems"] = [item(k, ROW_Y[i], CXL) for i, k in enumerate(("L1", "L2"))]
    d["ritems"] = [item(k, ROW_Y[i], CXR) for i, k in enumerate(("R1", "R2"))]
    d["rph"] = [placeholder(CXR, ROW_Y[0]), placeholder(CXR, ROW_Y[1])]
    d["q"] = T("Which idea would that support?", 38, TEXT, font=TITLE_FONT).move_to([0, -3.5, 0])
    return d


class S13(SpokenScene):
    def construct(self):
        d = cards_state()
        self.play(FadeIn(d["lf"]), FadeIn(d["rf"]), FadeIn(d["lslot"]), FadeIn(d["rslot"]), *[FadeIn(p) for p in d["rph"]],
                  run_time=0.8)
        self.at("molecular differences")
        self.play(FadeIn(d["litems"][0], shift=UP * 0.15), run_time=0.8)
        self.at("a map that forms")
        self.play(FadeIn(d["litems"][1], shift=UP * 0.15), run_time=0.9)
        self.at("which idea")
        self.play(FadeIn(d["q"], shift=UP * 0.1), run_time=0.7)
        self.finish()


class S14Pause(NarratedScene):
    """Silent beat: the question stays on screen, still, with a slow ring counting the pause down."""

    def construct(self):
        d = cards_state()
        self.add(d["lf"], d["rf"], d["lslot"], d["rslot"], *d["rph"], *d["litems"], d["q"])
        base = Circle(radius=0.34, stroke_color=GREY, stroke_width=6, fill_opacity=0).move_to([5.9, -3.5, 0])
        tr = ValueTracker(0.001)
        arc = always_redraw(lambda: Arc(radius=0.34, start_angle=PI / 2, angle=-TAU * max(tr.get_value(), 0.001),
                                        stroke_color=TEXT, stroke_width=9).move_arc_center_to([5.9, -3.5, 0]))
        self.add(base, arc)
        self.play(tr.animate.set_value(1.0), run_time=self.narration_s - 0.2, rate_func=linear)
        self.finish()


class S15(SpokenScene):
    def construct(self):
        d = cards_state()
        self.add(d["lf"], d["rf"], d["lslot"], d["rslot"], *d["rph"], *d["litems"], d["q"])
        self.play(FadeOut(d["q"]), FadeOut(d["lslot"]), FadeIn(d["lhead"], shift=UP * 0.1),
                  d["lf"].animate.set_stroke(color=GOLD).set_fill(GOLD, 0.07), run_time=0.9)
        self.at("that is what it predicts")
        self.play(Indicate(d["lf"], color=GOLD, scale_factor=1.02), run_time=1.0)
        self.finish()


class S16(SpokenScene):
    def construct(self):
        d = cards_state(GOLD, GREY)
        d["lf"].set_fill(GOLD, 0.07)
        self.add(d["lf"], d["rf"], d["lhead"], d["rslot"], *d["rph"], *d["litems"])
        self.play(FadeOut(d["rslot"]), FadeIn(d["rhead"], shift=UP * 0.1),
                  d["rf"].animate.set_stroke(color=TEXT).set_fill(TEXT, 0.07), run_time=0.9)
        self.at("young cortex given new input")
        self.play(FadeOut(d["rph"][0]), FadeIn(d["ritems"][0], shift=UP * 0.15), run_time=0.8)
        # second item: strip starts grey with a purple input arrow, takes the arrow's colour, then both change together
        grey_pic = pict_R(CXR - PXO, ROW_Y[1], None, PURPLE)
        cap = d["ritems"][1][1]
        self.at("take on features")
        self.play(FadeOut(d["rph"][1]), FadeIn(grey_pic, shift=UP * 0.15), FadeIn(cap, shift=UP * 0.15), run_time=0.8)
        self.at("that match")
        self.play(grey_pic[0].animate.set_stroke(PURPLE).set_fill(PURPLE, 0.5), run_time=0.7)
        self.at("the input")
        self.play(grey_pic[0].animate.set_stroke(GREEN).set_fill(GREEN, 0.5),
                  grey_pic[1].animate.set_color(GREEN), run_time=0.7)
        self.finish()


class S17(SpokenScene):
    def construct(self):
        d = cards_state(GOLD, TEXT)
        d["lf"].set_fill(GOLD, 0.07)
        d["rf"].set_fill(TEXT, 0.07)
        self.add(d["lf"], d["rf"], d["lhead"], d["rhead"], *d["litems"], *d["ritems"])
        gl = VGroup(check(CXL - 0.9, CHK_Y, 1.3), T("in part", 32, GREEN, weight=BOLD).move_to([CXL + 0.4, CHK_Y, 0]))
        gr = VGroup(check(CXR - 0.9, CHK_Y, 1.3), T("in part", 32, GREEN, weight=BOLD).move_to([CXR + 0.4, CHK_Y, 0]))
        self.at("came true")
        self.play(FadeIn(gl, scale=0.6), run_time=0.45)
        self.at("in part")
        self.play(FadeIn(gr, scale=0.6), run_time=0.45)
        self.finish()


# ---------------------------------------------------------------------------------------------
BX0, BW = -5.0, 8.5
INK_Y, INK_H = 1.0, 2.2
SK_Y0, SK_H0 = 0.5, 4.6          # the sketch, large and centred at first
SK_Y1, SK_H1 = 2.85, 1.0         # then it slides up and shrinks to a ghost
BTY = -3.0


class S18(SpokenScene):
    def construct(self):
        sketch = pencil_map(BX0, BW, SK_Y0, SK_H0)
        inked = make_map(BX0, BW, INK_Y, INK_H, op=0.55, sw=4, size=30)
        l1 = T("sketch from\nthe sheet", 26, LBLC, line_spacing=0.9).move_to([3.75, SK_Y1, 0], aligned_edge=LEFT)
        l2 = T("copy refined\nby its inputs", 26, WHITE, line_spacing=0.9).move_to([3.75, INK_Y, 0], aligned_edge=LEFT)
        tb = box(BW, 0.9, BX0 + BW / 2, BTY, GREY, 0.14, 3, 0.15)
        tl = T("thalamus", 28, LBLC).move_to([BX0 + 0.25, BTY, 0], aligned_edge=LEFT)
        cs = [BX0 + BW * f for f in (0.19, 0.54, 0.85)]
        ax = VGroup(*[bundle(x, BTY + 0.45, x, INK_Y - INK_H / 2, AREA_COL[i], n=3, s0=0.2, s1=0.4, sw=6)
                      for i, x in enumerate(cs)])
        # the (still empty) sheet that the copy will be drawn on
        sheet = Rectangle(width=BW, height=INK_H, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.12).move_to(
            [BX0 + BW / 2, INK_Y, 0])
        self.play(FadeIn(sketch), run_time=0.8)
        self.at("drawn twice")
        self.play(sketch.animate.stretch_to_fit_height(SK_H1).move_to([BX0 + BW / 2, SK_Y1, 0]),
                  FadeIn(sheet), FadeIn(tb), FadeIn(tl), run_time=0.9)
        self.at("first a sketch")
        self.play(FadeIn(l1, shift=LEFT * 0.1), LaggedStart(*[Create(a) for a in ax], lag_ratio=0.2), run_time=0.9)
        self.at("sheet")
        self.play(FadeIn(inked[0]), FadeIn(inked[1]), FadeIn(l2, shift=LEFT * 0.1), FadeOut(sheet), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S19(SpokenScene):
    def construct(self):
        m = pup(-3.4, 0.6, 1.6)
        ml = lab("newborn mouse", -3.4, -1.15, 28, LBLC)
        mp = make_map(0.5, 6.0, 0.6, 3.0, labels=False, op=0.0, sw=3)
        for r in mp[0]:
            r.set_stroke(color=LBLC)
        qs = VGroup(*[T("?", 60, LBLC, weight=BOLD).move_to([r.get_center()[0], 0.6, 0]) for r in mp[0]])
        dl = lab("dorsal map", 3.5, 2.5, 28, LBLC)
        q = T("How do you read a map in a newborn mouse?", 38, TEXT, font=TITLE_FONT).move_to([0, -2.9, 0])
        fit(q, max_w=12.4)
        self.play(FadeIn(m, shift=RIGHT * 0.2), FadeIn(ml), Create(mp), FadeIn(qs), FadeIn(dl), run_time=0.9)
        self.at("how do you read")
        self.play(FadeIn(q, shift=UP * 0.1), run_time=0.6)
        self.at("a map")
        self.play(Indicate(mp, color=TEXT, scale_factor=1.03), run_time=0.5)
        self.at("newborn mouse")
        self.play(Indicate(m, color=TEXT, scale_factor=1.05), run_time=0.8)
        self.finish()


class S20(SpokenScene):
    def construct(self):
        mA = pup(-3.5, 2.7, 1.5)
        cA = chip("no Emx2", ORANGE, 34).move_to([-3.5, 1.0, 0])
        mB = pup(3.5, 2.7, 1.5)
        cB = chip("no working Pax6", BLUE, 34).move_to([3.5, 1.0, 0])
        ay, bx, mx = -1.2, -1.5, 4.6
        axis = Arrow([-6.5, ay, 0], [6.6, ay, 0], buff=0, color=GREY, stroke_width=5, tip_length=0.25)
        t_lab = lab("time", -5.8, ay - 0.5, 26, LBLC)
        tick_b = Line([bx, ay - 0.25, 0], [bx, ay + 0.25, 0], stroke_color=TEXT, stroke_width=6)
        l_b = lab("birth", bx, ay - 0.65, 30, TEXT)
        tick_m = Line([mx, ay - 0.25, 0], [mx, ay + 0.25, 0], stroke_color=PINK, stroke_width=6)
        l_m = lab("areas mature", mx, ay - 0.65, 30, TEXT)
        self.play(FadeIn(mA, shift=RIGHT * 0.2), FadeIn(cA, shift=UP * 0.1), Create(axis), FadeIn(t_lab),
                  FadeIn(tick_b), FadeIn(l_b), FadeIn(tick_m), FadeIn(l_m), run_time=0.9)
        self.at("mice lacking", nth=1)
        self.play(FadeIn(mB, shift=LEFT * 0.2), FadeIn(cB, shift=UP * 0.1), run_time=0.8)
        x_mark = VGroup(Line([bx - 0.28, ay + 0.25, 0], [bx + 0.28, ay + 0.8, 0], stroke_color=RED, stroke_width=9),
                        Line([bx - 0.28, ay + 0.8, 0], [bx + 0.28, ay + 0.25, 0], stroke_color=RED, stroke_width=9))
        l_die = lab("die around birth", bx, ay + 1.25, 32, RED, weight=BOLD)
        self.at("die around birth")
        self.play(Create(x_mark), FadeIn(l_die, shift=DOWN * 0.1), run_time=0.8)
        gap = DoubleArrow([bx + 0.3, -2.65, 0], [mx - 0.1, -2.65, 0], buff=0, color=LBLC, stroke_width=5, tip_length=0.22)
        gl = lab("areas still immature at birth", (bx + mx) / 2, -3.25, 30, TEXT)
        self.at("before the areas mature")
        self.play(GrowFromCenter(gap), FadeIn(gl, shift=UP * 0.1), Indicate(l_m, color=PINK, scale_factor=1.1), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
HX = (-4.3, 0.0, 4.3)
HNAMES = ("marker genes", "connections", "barrel field")


def proxy_cards():
    g = VGroup()
    for i, x in enumerate(HX):
        b = box(3.9, 3.2, x, -1.1, GREY, 0.1, 3, 0.25)
        n = T(str(i + 1), 96, LBLC, font=TITLE_FONT).move_to(b)
        g.add(VGroup(b, n))
    return g


def header(active, labelled):
    g = VGroup()
    for i, x in enumerate(HX):
        on = (i == active)
        col = TEXT if on else GREY
        b = box(3.9, 0.8, x, 3.3, col, 0.18 if on else 0.06, 3, 0.2)
        txt = f"{i + 1}  {HNAMES[i]}" if i < labelled else str(i + 1)
        t = T(txt, 26, col, weight=BOLD if on else NORMAL).move_to(b)
        g.add(VGroup(b, t))
    return g


class S21(SpokenScene):
    def construct(self):
        a = T("area", 72, TEXT, font=TITLE_FONT).move_to([0, 2.9, 0])
        p = T("proxy", 72, TEAL, font=TITLE_FONT, weight=BOLD).move_to([0, 2.9, 0])
        d = T("proxy = a measurable stand-in for the real thing", 32, TEXT).move_to([0, 1.7, 0])
        fit(d, max_w=12.4)
        cards = proxy_cards()
        self.at("an area")
        self.play(FadeIn(a, shift=DOWN * 0.1), run_time=0.5)
        self.at("means a proxy")
        self.play(ReplacementTransform(a, p), FadeIn(d, shift=UP * 0.1), run_time=0.6)
        self.at("proxy")
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in cards], lag_ratio=0.3), run_time=0.9)
        self.finish()


SEC_C, SEC_S, SEC_SX, R_OUT, R_IN = (0.0, -0.6), 1.0, 1.5, 2.3, 1.75
SEC_HALF = SEC_S * SEC_SX * R_OUT
EDGE_ANG = float(np.arccos((WT[1] * 2 * SEC_HALF - SEC_HALF) / SEC_HALF))   # stain edge lines up with the touch/vision border


def section():
    base = Circle(radius=R_OUT, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.12)
    ring = Annulus(inner_radius=R_IN, outer_radius=R_OUT, stroke_width=0, fill_color=GREY, fill_opacity=0.4)
    stain = AnnularSector(inner_radius=R_IN, outer_radius=R_OUT, start_angle=12 * DEGREES, angle=EDGE_ANG - 12 * DEGREES,
                          stroke_width=0, fill_color=STAIN, fill_opacity=1.0)
    g = VGroup(base, ring, stain)
    g.stretch(SEC_SX, 0).scale(SEC_S).move_to([SEC_C[0], SEC_C[1], 0])
    return g


def ell_pt(ang_deg, rad=R_OUT):
    a = ang_deg * DEGREES
    return [SEC_C[0] + SEC_S * SEC_SX * rad * np.cos(a), SEC_C[1] + SEC_S * rad * np.sin(a), 0]


def edge_pt():
    return [SEC_C[0] + SEC_HALF * np.cos(EDGE_ANG), SEC_C[1] + SEC_S * R_OUT * np.sin(EDGE_ANG), 0]


def section_state():
    sec = section()
    sp = ell_pt(40, (R_OUT + R_IN) / 2)
    leg = VGroup(T("gene\nswitched on", 28, "#8FA8FF", weight=BOLD, line_spacing=0.9).move_to([4.1, 1.1, 0], aligned_edge=LEFT),
                 Line([4.0, 1.1, 0], [sp[0] + 0.05, sp[1], 0], stroke_color="#8FA8FF", stroke_width=3))
    isl = T("in situ\nhybridization", 30, TEXT, line_spacing=0.9).move_to([4.1, -1.5, 0], aligned_edge=LEFT)
    p2 = ell_pt(143, (R_OUT + R_IN) / 2)
    cx = VGroup(T("cortex", 28, LBLC).move_to([-5.7, p2[1], 0], aligned_edge=LEFT),
                Line([-4.55, p2[1], 0], [p2[0] - 0.05, p2[1], 0], stroke_color=LBLC, stroke_width=3))
    ts = T("tissue section", 28, LBLC).move_to([SEC_C[0], SEC_C[1], 0])
    return sec, leg, isl, cx, ts


class S22(SpokenScene):
    def construct(self):
        cards = proxy_cards()
        word = T("proxy", 72, TEAL, font=TITLE_FONT, weight=BOLD).move_to([0, 2.9, 0])
        d = T("proxy = a measurable stand-in for the real thing", 32, TEXT).move_to([0, 1.7, 0])
        self.add(cards, word, d)
        sec, leg, isl, cx, ts = section_state()
        self.play(FadeOut(word), FadeOut(d), Transform(cards, header(0, 0)), FadeIn(sec[0]), FadeIn(sec[1]),
                  FadeIn(cx), FadeIn(ts), run_time=0.8)
        self.at("marker genes")
        self.play(Transform(cards, header(0, 1)), run_time=0.6)
        self.at("switched on")
        self.play(FadeIn(sec[2], scale=0.9), FadeIn(leg, shift=RIGHT * 0.2), run_time=0.8)
        self.at("tissue section")
        self.play(FadeIn(isl, shift=LEFT * 0.2), Indicate(sec[0], color=TEXT, scale_factor=1.02), run_time=0.9)
        self.finish()


MAP2_Y, MAP2_H = 2.35, 0.8


class S23(SpokenScene):
    def construct(self):
        hdr = header(0, 1)
        sec, leg, isl, cx, ts = section_state()
        self.add(hdr, sec, leg, isl, cx, ts)
        ep = edge_pt()
        ring = Circle(radius=0.3, stroke_color=TEXT, stroke_width=5).move_to(ep)
        self.at("have borders")
        self.play(Create(ring), run_time=0.4)
        self.play(Indicate(ring, color=TEXT, scale_factor=1.3), run_time=0.5)
        m = make_map(-SEC_HALF, 2 * SEC_HALF, MAP2_Y, MAP2_H, op=0.5, size=26)
        link = DashedLine([ep[0], ep[1] + 0.3, 0], [ep[0], MAP2_Y - MAP2_H / 2, 0], color=TEXT, stroke_width=5)
        fl = T("future areas,\nseen from above", 26, LBLC, line_spacing=0.9).move_to([SEC_HALF + 0.3, MAP2_Y, 0], aligned_edge=LEFT)
        self.at("line up")
        self.play(FadeIn(m[0]), FadeIn(m[1]), Create(link), run_time=0.5)
        self.at("future areas")
        self.play(FadeIn(fl, shift=LEFT * 0.2), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
CBX0, CBW, CBCY, CBH = -5.0, 10.0, 1.5, 1.6
NY, NR = -1.9, 0.95                                     # thalamic nuclei row and radius
CBX = [CBX0 + CBW * f for f in ((0 + WT[0]) / 2, (WT[0] + WT[1]) / 2, (WT[1] + 1) / 2)]


def nucleus(x, color):
    ring = Circle(radius=NR, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.14).move_to([x, NY, 0])
    pts = [[x, NY, 0]] + [[x + 0.55 * np.cos(a), NY + 0.55 * np.sin(a), 0] for a in np.linspace(0, 2 * np.pi, 7)[:-1] + 0.3]
    dots = VGroup(*[Circle(radius=0.15, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=0.9).move_to(p)
                    for p in pts])
    return VGroup(ring, dots)


def cortex_bar():
    return make_map(CBX0, CBW, CBCY, CBH, op=0.45, size=28)


def wires():
    main = VGroup(*[bundle(CBX[i], NY + NR, CBX[i], CBCY - CBH / 2, AREA_COL[i], n=3, s0=0.3, s1=0.55, sw=5) for i in range(3)])
    thin = VGroup()
    for i, j in ((0, 1), (1, 0), (1, 2), (2, 1)):
        b = bundle(CBX[i] + 0.3 * (1 if j > i else -1), NY + NR - 0.05, CBX[j] + 0.6 * (-1 if j > i else 1), CBCY - CBH / 2,
                   AREA_COL[i], n=1, sw=2.5, op=0.8)[0]
        thin.add(DashedVMobject(b, num_dashes=14))
    return main, thin


def row_labels():
    return VGroup(lab("cortex", -5.95, CBCY, 26, LBLC), lab("thalamus", -5.95, NY, 26, LBLC))


class S24(SpokenScene):
    def construct(self):
        hdr = header(0, 1)
        sec, leg, isl, cx, ts = section_state()
        ep = edge_pt()
        m = make_map(-SEC_HALF, 2 * SEC_HALF, MAP2_Y, MAP2_H, op=0.5)
        fl = T("future areas,\nseen from above", 26, LBLC, line_spacing=0.9).move_to([SEC_HALF + 0.3, MAP2_Y, 0], aligned_edge=LEFT)
        old = VGroup(sec, leg, isl, cx, ts, m, fl, Circle(radius=0.3, stroke_color=TEXT, stroke_width=5).move_to(ep),
                     DashedLine([ep[0], ep[1] + 0.3, 0], [ep[0], MAP2_Y - MAP2_H / 2, 0], color=TEXT, stroke_width=5))
        self.add(hdr, old)
        nuc = [nucleus(x, AREA_COL[i]) for i, x in enumerate(CBX)]
        cb = cortex_bar()
        main, thin = wires()
        rl = row_labels()
        self.play(FadeOut(old), FadeIn(cb), *[FadeIn(n) for n in nuc], FadeIn(rl), run_time=0.8)
        self.at("connections")
        self.play(Transform(hdr, header(1, 2)), run_time=0.6)
        nl = lab("thalamic nucleus", CBX[0], -3.35, 26, TEXT)
        self.at("a thalamic nucleus")
        self.play(Indicate(nuc[0][0], color=PURPLE, scale_factor=1.08), FadeIn(nl, shift=UP * 0.1), run_time=0.8)
        self.at("cluster of neurons")
        self.play(Indicate(nuc[0][1], color=PURPLE, scale_factor=1.2), run_time=0.9)
        self.at("each one")
        self.play(LaggedStart(*[Indicate(n[0], color=AREA_COL[i], scale_factor=1.06) for i, n in enumerate(nuc)], lag_ratio=0.25),
                  run_time=0.5)
        self.at("projects")
        self.play(LaggedStart(*[Create(w) for w in main], lag_ratio=0.2), run_time=1.4)
        self.at("of cortex")
        self.play(LaggedStart(*[Create(w) for w in thin], lag_ratio=0.15), run_time=0.8)
        self.finish()


class S25(SpokenScene):
    def construct(self):
        hdr = header(1, 2)
        nuc = [nucleus(x, AREA_COL[i]) for i, x in enumerate(CBX)]
        cb = cortex_bar()
        main, thin = wires()
        nl = lab("thalamic nucleus", CBX[0], -3.35, 26, TEXT)
        self.add(hdr, cb, main, thin, *nuc, nl, row_labels())
        dx, dy = CBX[1] + 1.15, CBCY
        drop = Circle(radius=0.18, stroke_color=DYE, stroke_width=2, fill_color=DYE, fill_opacity=0.95).move_to([dx, dy, 0])
        dl = VGroup(T("dye", 28, DYE, weight=BOLD).move_to([dx, 2.6, 0]),
                    Line([dx, 2.4, 0], [dx, dy + 0.25, 0], stroke_color=DYE, stroke_width=3))
        self.wait(0.3)
        self.play(FadeIn(drop, scale=0.3), FadeIn(dl), run_time=0.5)
        ripple = Circle(radius=0.36, stroke_color=DYE, stroke_width=4, fill_opacity=0).move_to([dx, dy, 0])
        self.play(Transform(drop, ripple), run_time=0.6)
        back = bundle(CBX[1], CBCY - CBH / 2, CBX[1], NY + NR, DYE, n=3, s0=0.5, s1=0.3, sw=7)
        self.at("labels the")
        self.play(LaggedStart(*[Create(b) for b in back], lag_ratio=0.1), run_time=0.9)
        ln = lab("labelled neurons", CBX[1], -3.35, 26, DYE)
        self.at("thalamic neurons")
        self.play(*[d.animate.set_color(DYE) for d in nuc[1][1]], FadeIn(ln, shift=UP * 0.1), run_time=0.7)
        back2 = DashedVMobject(bundle(CBX[2] - 0.6, CBCY - CBH / 2, CBX[2] - 0.3, NY + NR - 0.05, DYE, n=1, s0=0, s1=0, sw=4)[0], num_dashes=14)
        few = lab("a few", CBX[2], -3.35, 26, DYE)
        self.at("sometimes in")
        self.play(Create(back2), run_time=0.7)
        self.play(*[nuc[2][1][k].animate.set_color(DYE) for k in (1, 4)], FadeIn(few, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
FSX, FSY, FSW, FSH = -0.9, 0.15, 8.8, 5.0   # flattened cortex


def barrel_pts():
    pts = []
    for r in range(5):
        y = FSY + (2 - r) * 0.95
        off = 0.5 if r % 2 else 0.0
        for k in range(6):
            x = FSX + (k - 2.5) * 1.05 + off - 0.25
            pts.append((x, y))
    return pts


def sheet_shape():
    return RoundedRectangle(corner_radius=1.5, width=FSW, height=FSH, stroke_color="#8E8B76", stroke_width=3,
                            fill_color="#9C9A84", fill_opacity=0.55).move_to([FSX, FSY, 0])


class S26(SpokenScene):
    def construct(self):
        hdr = header(1, 2)
        self.add(hdr)
        sheet = sheet_shape()
        barrels = VGroup(*[Circle(radius=0.34, stroke_color=GREEN, stroke_width=2.5, fill_color="#3B2F26", fill_opacity=0.97).move_to([x, y, 0])
                           for x, y in barrel_pts()])
        fb = DoubleArrow([FSX - FSW / 2, -2.85, 0], [FSX + FSW / 2, -2.85, 0], buff=0, color=LBLC, stroke_width=4, tip_length=0.2)
        front = T("front", 26, LBLC).move_to([FSX - FSW / 2 + 0.55, -3.4, 0])
        back = T("back", 26, LBLC).move_to([FSX + FSW / 2 - 0.5, -3.4, 0])
        fc = side_label("flattened cortex\n(top view)", 1.7, None, size=28)
        cox = side_label("cytochrome\noxidase stain", 0.0, None, color=TEXT, size=28)
        wk = side_label("first\npostnatal week", -1.5, None, color=GREEN, size=28)
        self.play(Transform(hdr, header(2, 3)), FadeIn(sheet), FadeIn(fb), FadeIn(front), FadeIn(back), run_time=0.7)
        self.at("barrel field")
        self.play(LaggedStart(*[FadeIn(b, scale=0.4) for b in barrels], lag_ratio=0.03), run_time=1.5)
        self.at("that survive past birth")
        self.play(FadeIn(wk, shift=LEFT * 0.2), run_time=0.7)
        self.at("a stain")
        self.play(FadeIn(cox, shift=LEFT * 0.2), run_time=0.6)
        self.at("flattened cortex")
        self.play(FadeIn(fc, shift=LEFT * 0.2), run_time=0.6)
        self.at("dark patches")
        self.play(Indicate(barrels, color=GREEN, scale_factor=1.12), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
AXY, BIRTH_X = -1.6, -2.2


def solid_chip(text, color, size=28):
    c = chip(text, color, size)
    under = RoundedRectangle(corner_radius=0.14, width=c.width, height=c.height, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(c)
    return VGroup(under, c)


class S27(SpokenScene):
    def construct(self):
        hdr = header(2, 3)
        self.add(hdr)
        c_mark = solid_chip("marker genes", TEXT, 34).move_to([BIRTH_X, 1.7, 0])
        c_conn = solid_chip("connections", TEXT, 34).move_to([BIRTH_X, 0.3, 0])
        c_barr = solid_chip("barrel field", GREEN, 34).move_to([0.8, 0.3, 0])
        axis = Arrow([-6.4, AXY, 0], [6.6, AXY, 0], buff=0, color=GREY, stroke_width=5, tip_length=0.25)
        t_lab = lab("time", -6.0, AXY - 0.65, 30, LBLC)
        tick = Line([BIRTH_X, AXY - 0.25, 0], [BIRTH_X, AXY + 0.25, 0], stroke_color=TEXT, stroke_width=7)
        vline = DashedLine([BIRTH_X, AXY, 0], [BIRTH_X, 1.7, 0], color=TEXT, stroke_width=3)
        l_b = lab("birth", BIRTH_X, AXY - 0.65, 34, TEXT)
        self.play(FadeOut(hdr), FadeIn(c_mark), FadeIn(c_conn), FadeIn(c_barr), run_time=0.7)
        self.at("die at birth")
        self.play(Create(axis), FadeIn(t_lab), FadeIn(tick), FadeIn(l_b), Create(vline), run_time=0.7)
        self.add(c_mark, c_conn)
        brace = Brace(VGroup(c_mark, c_conn, c_barr), UP, color=LBLC, buff=0.12)
        t1 = lab("early proxies", brace.get_center()[0], brace.get_top()[1] + 0.45, 36, TEXT, weight=BOLD)
        t2 = lab("stand in for mature areas", brace.get_center()[0], brace.get_top()[1] + 1.05, 30, LBLC)
        self.at("these proxies")
        self.play(GrowFromCenter(brace), FadeIn(t1, shift=DOWN * 0.1), run_time=0.6)
        self.at("stand in for mature areas")
        self.play(FadeIn(t2, shift=DOWN * 0.1), run_time=0.6)
        seg = Line([BIRTH_X, AXY, 0], [2.1, AXY, 0], stroke_color=GREEN, stroke_width=12)
        conn = DashedLine([0.8, 0.3 - 0.4, 0], [0.8, AXY, 0], color=GREEN, stroke_width=4)
        wk = lab("first postnatal\nweek", 0.8, AXY - 0.9, 34, GREEN, line_spacing=0.9)
        self.at("animals that survive")
        self.play(Create(seg), Create(conn), FadeIn(wk), run_time=0.7)
        d_l = Dot([4.1, AXY, 0], radius=0.28, color=GREEN)
        l_l = lab("later", 4.1, AXY - 0.65, 34, TEXT)
        self.at("allow later")
        self.play(FadeIn(d_l, scale=0.4), FadeIn(l_l, shift=UP * 0.1), run_time=0.5)
        d_a = Dot([6.0, AXY, 0], radius=0.28, color=GREEN)
        l_a = lab("adult", 6.0, AXY - 0.65, 34, TEXT)
        self.at("adult measures")
        self.play(FadeIn(d_a, scale=0.4), FadeIn(l_a, shift=UP * 0.1), run_time=0.5)
        note = lab("read each result at the age it was measured", 0.0, -3.65, 32, TEXT)
        fit(note, max_w=12.4)
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.6)
        self.finish()


PRX = -4.4
PRY = (1.95, -0.1, -2.15)
PCY = (1.5, -1.9)
PCX = 4.0


def stack_cards():
    g = VGroup()
    for i, y in enumerate(PRY):
        b = box(4.4, 1.8, PRX, y, TEXT, 0.1, 3, 0.2)
        t = T(HNAMES[i], 34, TEXT).move_to(b)
        g.add(VGroup(b, t))
    return g


def pred_card(name, line, color, y):
    b = box(5.6, 2.9, PCX, y, GREY, 0.06, 3, 0.25)
    h = T(name, 42, WHITE, font=TITLE_FONT, weight=BOLD).move_to([PCX, y + 0.65, 0])
    t = T(line, 30, TEXT, line_spacing=0.9).move_to([PCX, y - 0.5, 0])
    return VGroup(b, h, t)


class S28(SpokenScene):
    def construct(self):
        stack = stack_cards()
        title = lab("three proxies", PRX, 3.5, 30, TEXT)
        self.add(stack, title)
        pt = lab("two predictions", PCX, 3.5, 30, TEXT)
        pc1 = pred_card("protomap", "molecular differences,\nsome map without input", GREY, PCY[0])
        pc2 = pred_card("protocortex", "new input gives\nmatching features", GREY, PCY[1])
        self.at("two ideas")
        self.play(FadeIn(pt), FadeIn(pc1, shift=LEFT * 0.2), FadeIn(pc2, shift=LEFT * 0.2), run_time=0.8)
        brace = Brace(stack, RIGHT, color=LBLC, buff=0.12)
        ym = (PCY[0] + PCY[1]) / 2
        xl = PCX - 2.8 - 0.1
        arr = Arrow([brace.get_right()[0] + 0.05, ym, 0], [-0.6, ym, 0], buff=0, color=LBLC, stroke_width=7, tip_length=0.0)
        test = lab("test", (brace.get_right()[0] - 0.6) / 2 - 0.05, ym + 0.5, 34, TEXT, weight=BOLD)
        cap = lab("the proxies test both ideas", 0.0, -3.7, 30, TEXT, weight=BOLD)
        vl = Line([-0.6, PCY[0], 0], [-0.6, PCY[1], 0], stroke_color=LBLC, stroke_width=7)
        a1 = Arrow([-0.6, PCY[0], 0], [xl, PCY[0], 0], buff=0, color=GOLD, stroke_width=7, tip_length=0.28)
        a2 = Arrow([-0.6, PCY[1], 0], [xl, PCY[1], 0], buff=0, color=TEXT, stroke_width=7, tip_length=0.28)
        self.at("early")
        self.play(GrowFromCenter(brace), Create(arr), FadeIn(test), FadeIn(cap), Indicate(stack, color=TEXT, scale_factor=1.02),
                  run_time=0.7)
        self.play(Create(vl), GrowArrow(a1), GrowArrow(a2), run_time=0.5)
        self.finish()


class S29End(EndCard):
    LINE = "The two ideas make different predictions; early proxies can test them."

    def construct(self):
        line = T(self.LINE, size=42, font=TITLE_FONT)
        fit(line, max_w=11.8)
        sub = T("biochemistrypedia.com", size=28, color="#7FDCE3", weight=BOLD)
        g = VGroup(line, sub).arrange(DOWN, buff=0.45)
        self.play(FadeIn(line, shift=UP * 0.15), run_time=self.beat(0.3))
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        self.finish()
