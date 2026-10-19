"""Adhesion and the extracellular matrix: two grips, each wired to a cable  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = calcium
  BLUE   = cadherin (the outer arms and the tail)
  PURPLE = integrin (alpha and beta lobes)
  ORANGE = the matrix (mesh, fibronectin, RGD tag, laminin, basement membrane)
  TEAL   = adaptor proteins inside the cell (catenins, p120, talin, vinculin, plectin)
  GREEN  = actin filaments
  PINK   = keratin filaments
  GOLD   = force and myosin
  RED    = blocked (myosin crossed out)
  GREY   = cells, membranes, labels
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E87DB0"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=24, pad=0.14):
    c = chip(text, color, size=size, pad=pad)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def btext(text, size=24, color=GREY):
    t = T(text, size, color)
    back = Rectangle(width=t.width + 0.2, height=t.height + 0.12, stroke_width=0, fill_color=BG,
                     fill_opacity=1).move_to(t)
    return VGroup(back, t)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=14)


def cell_rect(cx, cy, w, h, op=0.16):
    return RoundedRectangle(corner_radius=0.35, width=w, height=h, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=op).move_to([cx, cy, 0])


def mem_v(x, y0, y1, w=0.22):
    return RoundedRectangle(corner_radius=0.08, width=w, height=y1 - y0, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.5).move_to([x, (y0 + y1) / 2, 0])


def mem_h(y, x0=-6.3, x1=6.3, h=0.22):
    return RoundedRectangle(corner_radius=0.08, width=x1 - x0, height=h, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.5).move_to([(x0 + x1) / 2, y, 0])


def beaded(p0, p1, color=GREEN, spacing=0.3, r=0.1):
    p0, p1 = np.array(p0, float), np.array(p1, float)
    n = int(np.linalg.norm(p1 - p0) / spacing) + 1
    ln = Line(p0, p1, color=color, stroke_width=3)
    dots = [Dot(p0 + (p1 - p0) * i / max(n - 1, 1), radius=r, color=color) for i in range(n)]
    return VGroup(ln, *dots)


def rods(p0, p1, color=PINK, seg=0.34):
    p0, p1 = np.array(p0, float), np.array(p1, float)
    n = int(np.linalg.norm(p1 - p0) / seg)
    out = []
    for i in range(n):
        out.append(RoundedRectangle(corner_radius=0.05, width=seg - 0.05, height=0.15, stroke_width=0,
                                    fill_color=color, fill_opacity=0.95).move_to(p0 + (p1 - p0) * (i + 0.5) / n))
    return VGroup(*out)


def link(a, b, color=TEAL, w=3):
    return Line(a, b, color=color, stroke_width=w)


def lobe(x, y, label, h=1.7, w=0.5):
    r = RoundedRectangle(corner_radius=0.16, width=w, height=h, stroke_color=PURPLE, stroke_width=3,
                         fill_color=PURPLE, fill_opacity=0.35).move_to([x, y, 0])
    t = T(label, 24, TEXT).move_to(r)
    return VGroup(r, t)


# ---- cadherin arms -----------------------------------------------------------------------------
MEM_X = 2.0


def arm_pts(side, y, bend, sp=0.42):
    """side -1 = left cell, +1 = right cell. bend 0 = stiff and straight, >0 = limp, drooping."""
    dx = -side
    p = np.array([side * MEM_X + dx * 0.15, y, 0.0])
    pts = [p.copy()]
    for k in range(1, 5):
        ang = -bend * k
        p = p + sp * np.array([dx * np.cos(ang), np.sin(ang), 0.0])
        pts.append(p.copy())
    return pts


def arm_mob(pts):
    lines = VGroup(*[Line(pts[i], pts[i + 1], color=BLUE, stroke_width=4) for i in range(4)])
    beads = VGroup(*[RoundedRectangle(corner_radius=0.05, width=0.24, height=0.24, stroke_color=BLUE,
                                      stroke_width=2, fill_color=BLUE, fill_opacity=0.5).move_to(p) for p in pts])
    return VGroup(lines, beads)


def ca_dots(pts):
    return VGroup(*[Dot((pts[i] + pts[i + 1]) / 2, radius=0.08, color=YELLOW) for i in range(4)])


YS = [1.7, 0.0, -1.7]
LIMP = 0.3


def junction_cells():
    a = cell_rect(-4.15, -0.1, 4.3, 5.8)
    b = cell_rect(4.15, -0.1, 4.3, 5.8)
    ma = mem_v(-MEM_X, -3.0, 2.8)
    mb = mem_v(MEM_X, -3.0, 2.8)
    return a, b, ma, mb


def stiff_arms(ys=YS):
    out = {}
    for y in ys:
        out[(y, -1)] = arm_mob(arm_pts(-1, y, 0.0))
        out[(y, 1)] = arm_mob(arm_pts(1, y, 0.0))
    return out


def ca_all(ys=YS):
    g = VGroup()
    for y in ys:
        g.add(ca_dots(arm_pts(-1, y, 0.0)), ca_dots(arm_pts(1, y, 0.0)))
    return g


class S00Title(TitleCard):
    LESSON = "Adhesion and the extracellular matrix"
    TITLE = "Two grips, each wired to a cable"


# ---------------------------------------------------------------------------------------------
class S01Calcium(SpokenScene):
    """sheet of cells: calcium out, cells round up and part; back, they rejoin; zoom: limp arms stiffen."""

    def construct(self):
        xs = [-4.8, -2.4, 0.0, 2.4, 4.8]
        cells = VGroup(*[cell_rect(x, 0.2, 2.3, 3.0) for x in xs])
        circ = [Circle(radius=1.0, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.16)
                .move_to([x, 0.2 + (0.15 if i % 2 else -0.1), 0]) for i, x in enumerate(xs)]
        # calcium in the fluid: in the gaps and above and below the sheet
        pts = []
        for x in [-3.6, -1.2, 1.2, 3.6]:
            for y in [-0.9, 0.2, 1.3]:
                pts.append([x, y, 0])
        for x in np.linspace(-5.4, 5.4, 9):
            pts.append([x, 2.35, 0]); pts.append([x, -1.95, 0])
        ca = VGroup(*[Dot(p, radius=0.1, color=YELLOW) for p in pts])
        ca_lbl = VGroup(Dot(radius=0.1, color=YELLOW), T("calcium", 26, YELLOW)).arrange(RIGHT, buff=0.15)
        ca_lbl.move_to([0, 3.15, 0])
        sheet_lbl = T("a sheet of cultured epithelial cells", 26, GREY).move_to([0, -3.0, 0])

        self.play(FadeIn(cells), FadeIn(ca), FadeIn(ca_lbl), FadeIn(sheet_lbl), run_time=0.4)
        self.at("calcium away")
        self.play(FadeOut(ca, shift=UP * 0.3), run_time=0.8)
        self.at("round up")
        self.play(*[Transform(c, k) for c, k in zip(cells, circ)], run_time=1.0)
        self.at("Put it back")
        self.play(FadeIn(ca), run_time=0.7)
        rects = [cell_rect(x, 0.2, 2.3, 3.0) for x in xs]
        self.at("knit together")
        self.play(*[Transform(c, k) for c, k in zip(cells, rects)], run_time=1.0)
        self.at("What was the calcium")
        q = T("?", 96, YELLOW, weight=BOLD).move_to([0.0, 0.2, 0])
        self.play(FadeIn(q, scale=0.6), run_time=0.5)

        # ---- zoom to one junction -------------------------------------------------------------
        a, b, ma, mb = junction_cells()
        limp = {}
        for y in YS:
            limp[(y, -1)] = arm_mob(arm_pts(-1, y, LIMP))
            limp[(y, 1)] = arm_mob(arm_pts(1, y, LIMP))
        limp_all = VGroup(*limp.values())
        self.at("holding")
        self.play(FadeOut(VGroup(cells, ca, q, ca_lbl, sheet_lbl)), FadeIn(VGroup(a, b, ma, mb)),
                  FadeIn(limp_all), run_time=0.9)
        stiff = stiff_arms()
        cadl = T("cadherin", 28, BLUE).move_to([0, 2.7, 0])
        ca_new = ca_all()
        ca_leg = VGroup(Dot(radius=0.1, color=YELLOW), T("calcium", 26, YELLOW)).arrange(RIGHT, buff=0.15)
        ca_leg.move_to([0, -2.85, 0])
        self.at("stiffens")
        self.play(*[Transform(limp[k], stiff[k]) for k in limp], FadeIn(ca_new, scale=0.5), FadeIn(ca_leg),
                  run_time=1.3)
        self.at("adhesion proteins")
        self.play(FadeIn(cadl, shift=DOWN * 0.1), run_time=0.5)
        self.at("grip the next")
        self.play(*[Indicate(limp[k], color=BLUE, scale_factor=1.06) for k in limp], run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Cadherin(SpokenScene):
    """cadherin crosses the membrane; chain inside: beta-catenin, alpha-catenin, actin; p120; a pull travels."""

    def construct(self):
        a, b, ma, mb = junction_cells()
        stiff = stiff_arms()
        ca_new = ca_all()
        cadl = T("cadherin", 28, BLUE).move_to([0, 2.7, 0])
        ca_leg = VGroup(Dot(radius=0.1, color=YELLOW), T("calcium", 26, YELLOW)).arrange(RIGHT, buff=0.15)
        ca_leg.move_to([0, -2.85, 0])
        self.add(a, b, ma, mb, *stiff.values(), ca_new, cadl, ca_leg)

        # keep only the middle pair
        outer = VGroup(*[stiff[(y, s)] for y in (1.7, -1.7) for s in (-1, 1)])
        outer_ca = VGroup(*[ca_dots(arm_pts(s, y, 0.0)) for y in (1.7, -1.7) for s in (-1, 1)])
        mid_ca = VGroup(ca_dots(arm_pts(-1, 0.0, 0.0)), ca_dots(arm_pts(1, 0.0, 0.0)))
        self.remove(ca_new)
        self.add(outer_ca, mid_ca)

        tails = {}
        for s in (-1, 1):
            tails[s] = Line([s * MEM_X, 0, 0], [s * 2.55, 0, 0], color=BLUE, stroke_width=4)
        self.at("crosses the membrane")
        self.play(FadeOut(outer), FadeOut(outer_ca), *[Create(t) for t in tails.values()], run_time=0.9)
        self.at("outer arm binds")
        self.play(Indicate(VGroup(stiff[(0.0, -1)], stiff[(0.0, 1)]), color=BLUE, scale_factor=1.08), run_time=0.8)

        # chain on both sides (labels on the left cell only)
        def chain(s, labels):
            bt = bchip("β-catenin", TEAL, 24) if labels else bchip("β-catenin", TEAL, 24)
            bt.move_to([s * 3.4, 0.0, 0])
            al = bchip("α-catenin", TEAL, 24).move_to([s * 3.4, -1.2, 0])
            act = beaded([s * 6.0, -2.4, 0], [s * 2.3, -2.4, 0], GREEN)
            t2 = Line([s * MEM_X, 0, 0], [bt.get_left()[0] if s < 0 else bt.get_left()[0], 0, 0])
            return bt, al, act

        bA, aA, actA = chain(-1, True)
        bB, aB, actB = chain(1, False)
        # tail lengths to reach the chip edges
        tailA = Line([-MEM_X, 0, 0], [bA.get_right()[0], 0, 0], color=BLUE, stroke_width=4)
        tailB = Line([MEM_X, 0, 0], [bB.get_left()[0], 0, 0], color=BLUE, stroke_width=4)
        linkA = link([-3.4, bA.get_bottom()[1], 0], [-3.4, aA.get_top()[1], 0])
        linkB = link([3.4, bB.get_bottom()[1], 0], [3.4, aB.get_top()[1], 0])
        actlinkA = link([-3.4, aA.get_bottom()[1], 0], [-3.4, -2.4, 0])
        actlinkB = link([3.4, aB.get_bottom()[1], 0], [3.4, -2.4, 0])
        self.at("binds the tail directly")
        self.play(Transform(tails[-1], tailA), Transform(tails[1], tailB),
                  FadeIn(bA, scale=0.8), FadeIn(bB, scale=0.8), run_time=0.8)
        self.at("recruits")
        self.play(FadeIn(linkA), FadeIn(linkB), FadeIn(aA, shift=DOWN * 0.2), FadeIn(aB, shift=DOWN * 0.2),
                  run_time=0.7)
        self.at("actin filaments")
        actl = T("actin", 26, GREEN).move_to([-5.0, -1.95, 0])
        self.play(Create(actA), Create(actB), FadeIn(actlinkA), FadeIn(actlinkB), FadeIn(actl), run_time=1.0)

        p120 = bchip("p120", TEAL, 24).move_to([-2.85, 1.25, 0])
        p120l = link([-2.35, p120.get_bottom()[1], 0], [-2.35, 0.0, 0])
        self.at("third protein")
        self.play(FadeIn(p120, shift=DOWN * 0.2), FadeIn(p120l), run_time=0.7)

        self.at("So a pull")
        pull = arr([2.9, 2.0, 0], [5.4, 2.0, 0], GOLD, w=8, tip=0.3)
        self.play(GrowArrow(pull), run_time=0.5)
        path = [stiff[(0.0, 1)], stiff[(0.0, -1)], tails[-1], VGroup(*bA[1:]), VGroup(*aA[1:]), actA]
        for m in path:
            self.play(Indicate(m, color=GOLD, scale_factor=1.12), run_time=0.45)
        self.finish()


# ---------------------------------------------------------------------------------------------
def mesh_tiles(x0=-6.3, x1=6.3, y0=-3.0, y1=-1.75, tw=0.9):
    tiles = []
    x = x0
    while x + tw <= x1 + 1e-6:
        c = x + tw / 2
        g = VGroup(Line([x, y0, 0], [x + tw, y1, 0], color=ORANGE, stroke_width=2.5),
                   Line([x, y1, 0], [x + tw, y0, 0], color=ORANGE, stroke_width=2.5))
        g.cx = c
        tiles.append(g)
        x += tw
    return tiles


def focal_chain(x0=0.0, with_labels=True):
    """integrin + fibronectin + talin + vinculin + actin, built at centre x0."""
    d = {}
    d["alpha"] = lobe(x0 - 0.3, -0.9, "α")
    d["beta"] = lobe(x0 + 0.3, -0.9, "β")
    d["fn_beads"] = VGroup(*[Dot([x0, y, 0], radius=0.09, color=ORANGE) for y in (-2.95, -2.7, -2.45)])
    d["fn_line"] = Line([x0, -3.0, 0], [x0, -2.25, 0], color=ORANGE, stroke_width=3)
    d["rgd"] = bchip("RGD", ORANGE, 22, 0.1).move_to([x0, -2.0, 0])
    d["talin"] = bchip("talin", TEAL, 24).move_to([x0 + 0.65, 0.5, 0])
    d["actin"] = beaded([x0 - 2.8, 2.2, 0], [x0 + 2.8, 2.2, 0], GREEN)
    d["tlink"] = link([x0 + 0.65, 0.5 + d["talin"].height / 2, 0], [x0 + 0.65, 2.2, 0])
    d["bt"] = link([x0 + 0.3, -0.05, 0], [x0 + 0.3, 0.5 - d["talin"].height / 2, 0])
    d["vinc"] = bchip("vinculin", TEAL, 24).move_to([x0 + 2.6, 1.3, 0])
    d["vlink"] = VGroup(link([x0 + 2.6 - d["vinc"].width / 2, 1.3, 0], [x0 + 0.65 + d["talin"].width / 2, 0.5, 0]),
                        link([x0 + 2.6, 1.3 + d["vinc"].height / 2, 0], [x0 + 2.6, 2.2, 0]))
    d["l_int"] = T("integrin", 26, PURPLE).move_to([x0 - 1.7, -0.25, 0])
    d["l_fn"] = btext("fibronectin", 24, ORANGE).move_to([x0 + 1.45, -2.55, 0])
    d["l_act"] = T("actin", 26, GREEN).move_to([x0 - 2.2, 2.75, 0])
    return d


class S03Integrin(SpokenScene):
    """cell on a matrix mesh; integrin alpha/beta lobes grip the RGD tag of fibronectin; talin, actin, vinculin."""

    def construct(self):
        cell = RoundedRectangle(corner_radius=0.35, width=12.6, height=4.3, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.16).move_to([0, 1.25, 0])
        mem = mem_h(-0.9)
        tiles = mesh_tiles()
        mesh = VGroup(*tiles)
        l_mat = T("extracellular matrix", 26, ORANGE).move_to([-4.0, -3.28, 0])
        d = focal_chain(0.0)
        self.at("second grip")
        self.play(FadeIn(cell), FadeIn(mem), run_time=0.7)
        self.at("extracellular matrix")
        self.play(FadeIn(mesh, lag_ratio=0.05), FadeIn(l_mat), run_time=1.2)
        self.at("main matrix receptors")
        self.play(GrowFromCenter(d["alpha"]), GrowFromCenter(d["beta"]), FadeIn(d["l_int"]), run_time=0.8)
        self.at("alpha subunit")
        self.play(Indicate(d["alpha"], color=PURPLE, scale_factor=1.15), run_time=0.7)
        self.at("beta subunit")
        self.play(Indicate(d["beta"], color=PURPLE, scale_factor=1.15), run_time=0.7)
        eq = M("18 α + 8 β → 24 integrins", 32, PURPLE).move_to([0, 2.0, 0])
        self.at("Mammals have")
        self.play(FadeIn(eq, shift=UP * 0.15), run_time=0.6)
        self.at("Many")
        self.play(FadeOut(eq), run_time=0.4)
        self.at("short sequence")
        self.play(Create(d["fn_line"]), FadeIn(d["fn_beads"]), FadeIn(d["rgd"], shift=UP * 0.2), FadeIn(d["l_fn"]),
                  run_time=0.9)
        self.at("talin binds")
        self.play(FadeIn(d["talin"], shift=UP * 0.15), FadeIn(d["bt"]), run_time=0.6)
        self.at("links it to actin")
        self.play(Create(d["actin"]), FadeIn(d["tlink"]), FadeIn(d["l_act"]), run_time=0.9)
        self.at("vinculin reinforces")
        self.play(FadeIn(d["vinc"], shift=LEFT * 0.2), FadeIn(d["vlink"]), run_time=0.7)
        self.finish()


class S04Exception(SpokenScene):
    """the actin chain slides left; a hemidesmosome integrin binds laminin and ends on keratin via plectin."""

    def construct(self):
        cell = RoundedRectangle(corner_radius=0.35, width=12.6, height=4.3, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.16).move_to([0, 1.25, 0])
        mem = mem_h(-0.9)
        tiles = mesh_tiles()
        left = VGroup(*[t for t in tiles if t.cx < 0])
        right = VGroup(*[t for t in tiles if t.cx > 0])
        l_mat = T("extracellular matrix", 26, ORANGE).move_to([-4.0, -3.28, 0])
        d = focal_chain(0.0)
        chain = VGroup(d["alpha"], d["beta"], d["fn_beads"], d["fn_line"], d["rgd"], d["talin"], d["actin"],
                       d["tlink"], d["bt"], d["vinc"], d["vlink"], d["l_int"], d["l_fn"], d["l_act"])
        self.add(cell, mem, left, right, l_mat, chain)

        self.at("Not every integrin")
        self.play(Indicate(d["actin"], color=GREEN, scale_factor=1.04), run_time=0.8)
        self.at("Hemidesmosomes pin")
        # chain 2 geometry
        X2 = 3.4
        band = RoundedRectangle(corner_radius=0.06, width=6.0, height=0.5, stroke_color=ORANGE, stroke_width=3,
                                fill_color=ORANGE, fill_opacity=0.28).move_to([X2, -2.75, 0])
        l_bm = T("basement membrane", 24, ORANGE).move_to(band)
        hd = T("hemidesmosome", 26, GREY).move_to([X2, 2.95, 0])
        self.play(chain.animate.shift(LEFT * X2), FadeOut(right),
                  FadeIn(band), FadeIn(l_bm), FadeIn(hd), run_time=1.3)
        # chain 2 built at X2
        al = lobe(X2 - 0.3, -0.9, "α6")
        be = lobe(X2 + 0.3, -0.9, "β4")
        lam = bchip("laminin-332", ORANGE, 22, 0.1).move_to([X2, -2.0, 0])
        lam_s = Line([X2, -2.5, 0], [X2, -2.25, 0], color=ORANGE, stroke_width=3)
        plec = bchip("plectin", TEAL, 24).move_to([X2 + 0.2, 0.5, 0])
        pb = link([X2 + 0.3, -0.05, 0], [X2 + 0.3, 0.5 - plec.height / 2, 0])
        ker = rods([X2 - 2.8, 2.0, 0], [X2 + 2.8, 2.0, 0])
        pk = link([X2 + 0.2, 0.5 + plec.height / 2, 0], [X2 + 0.2, 1.93, 0])
        l_ker = T("keratin", 26, PINK).move_to([X2 + 2.0, 1.45, 0])
        l_int2 = T("integrin α6β4", 24, PURPLE).move_to([X2 - 1.75, -0.3, 0])
        self.at("There")
        self.play(GrowFromCenter(al), GrowFromCenter(be), FadeIn(l_int2), run_time=0.8)
        self.at("binds laminin")
        self.play(FadeIn(lam, shift=UP * 0.2), FadeIn(lam_s), run_time=0.7)
        self.at("connects through")
        self.play(FadeIn(plec, shift=UP * 0.15), FadeIn(pb), run_time=0.7)
        self.at("keratin filaments")
        self.play(Create(ker), FadeIn(pk), FadeIn(l_ker), run_time=0.9)
        self.at("Two chains")
        self.play(Indicate(d["actin"], color=GREEN, scale_factor=1.04), Indicate(ker, color=PINK, scale_factor=1.04),
                  run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
def rod_row(unf=(), y=0.0, n=13, ew=0.55, uw=1.45, gap=0.07, h=0.9):
    widths = [uw if i in unf else ew for i in range(n)]
    total = sum(widths) + gap * (n - 1)
    x = -total / 2
    items = []
    for i, w in enumerate(widths):
        hh = 0.12 if i in unf else h
        r = RoundedRectangle(corner_radius=min(0.08, hh / 2), width=w, height=hh, stroke_color=TEAL, stroke_width=2.5,
                             fill_color=TEAL, fill_opacity=0.8 if i in unf else 0.3).move_to([x + w / 2, y, 0])
        items.append(r)
        x += w + gap
    g = VGroup(*items)
    g.total = total
    return g


UNF = (2, 6, 10)


class S05Talin(SpokenScene):
    """myosin pulls the chain; the talin chip becomes 13 bundles; 12 pN raises vinculin binding events 1 -> 3."""

    def construct(self):
        bar = mem_v(-5.2, -1.2, 1.8)
        integ = RoundedRectangle(corner_radius=0.2, width=0.7, height=1.3, stroke_color=PURPLE, stroke_width=3,
                                 fill_color=PURPLE, fill_opacity=0.35).move_to([-5.2, 0.3, 0])
        l_int = T("integrin", 24, PURPLE).move_to([-5.2, -1.6, 0])
        talin = bchip("talin", TEAL, 28).move_to([-3.3, 0.3, 0])
        l1 = link([-4.85, 0.3, 0], [talin.get_left()[0], 0.3, 0])
        act = beaded([-2.2, 0.3, 0], [3.2, 0.3, 0], GREEN)
        l2 = link([talin.get_right()[0], 0.3, 0], [-2.2, 0.3, 0])
        l_act = T("actin", 26, GREEN).move_to([0.5, -0.45, 0])
        myo = bchip("myosin II", GOLD, 28).move_to([0.5, 1.9, 0])
        ml = VGroup(link([0.2, myo.get_bottom()[1], 0], [0.2, 0.38, 0], GOLD), link([0.8, myo.get_bottom()[1], 0], [0.8, 0.38, 0], GOLD))
        pullarr = arr([3.4, 0.3, 0], [5.6, 0.3, 0], GOLD, w=9, tip=0.32)
        self.play(FadeIn(VGroup(bar, integ, l_int, talin, l1, l2, act, l_act)), run_time=0.3)
        self.at("pulls on its adhesions")
        self.play(FadeIn(myo, shift=DOWN * 0.2), FadeIn(ml), GrowArrow(pullarr), run_time=0.8)
        q = T("?", 64, TEXT, weight=BOLD).move_to([-3.3, 1.5, 0])
        self.at("links themselves")
        self.play(FadeIn(q, scale=0.6), Indicate(VGroup(*talin[1:]), color=TEXT, scale_factor=1.15), run_time=0.8)

        # ---- the purified rod ------------------------------------------------------------------
        folded = rod_row((), y=1.4)
        lab = T("purified talin rod", 28, TEAL).move_to([0, 2.75, 0])
        self.at("purified")
        self.play(FadeOut(VGroup(bar, integ, l_int, l1, l2, act, l_act, myo, ml, pullarr, q)),
                  ReplacementTransform(talin, folded), FadeIn(lab), run_time=1.1)
        y0 = folded.get_bottom()[1] - 0.35
        br = VGroup(Line([folded.get_left()[0], y0 + 0.12, 0], [folded.get_left()[0], y0, 0], color=GREY, stroke_width=3),
                    Line([folded.get_left()[0], y0, 0], [folded.get_right()[0], y0, 0], color=GREY, stroke_width=3),
                    Line([folded.get_right()[0], y0, 0], [folded.get_right()[0], y0 + 0.12, 0], color=GREY, stroke_width=3))
        n13 = T("13 helical bundles", 26, GREY).move_to([0, y0 - 0.4, 0])
        self.at("stack of")
        self.play(Create(br), FadeIn(n13), run_time=0.8)

        # ---- stretched at 12 pN ----------------------------------------------------------------
        a_l = arr([folded.get_left()[0] - 0.1, 1.4, 0], [folded.get_left()[0] - 1.3, 1.4, 0], GOLD, w=9, tip=0.3)
        a_r = arr([folded.get_right()[0] + 0.1, 1.4, 0], [folded.get_right()[0] + 1.3, 1.4, 0], GOLD, w=9, tip=0.3)
        pn = M("12 pN", 30, GOLD).move_to([0, 3.35, 0])
        self.at("Stretched at")
        self.play(FadeOut(lab), GrowArrow(a_l), GrowArrow(a_r), FadeIn(pn), run_time=0.8)

        # counter
        head = T("vinculin-head binding events", 26, GREY).move_to([0, -1.05, 0])
        one = VGroup(Dot(radius=0.13, color=TEAL), T("at most 1", 26, TEXT)).arrange(DOWN, buff=0.25)
        three = VGroup(Dot(radius=0.13, color=TEAL), Dot(radius=0.13, color=TEAL), Dot(radius=0.13, color=TEAL))
        three.arrange(RIGHT, buff=0.3)
        three = VGroup(three, T("as many as 3", 26, TEXT)).arrange(DOWN, buff=0.25)
        one.move_to([-3.0, -2.3, 0]); three.move_to([3.0, -2.3, 0])
        ar = arr([-1.5, -2.1, 0], [1.5, -2.1, 0], GREY, w=5)
        self.at("more vinculin")
        self.play(FadeIn(head), FadeOut(VGroup(br, n13)), run_time=0.6)
        self.at("from one at most")
        self.play(FadeIn(one, shift=UP * 0.15), run_time=0.5)
        self.at("as many as three")
        self.play(GrowArrow(ar), FadeIn(three, shift=UP * 0.15), run_time=0.7)

        # ---- the reading: bundles unfold --------------------------------------------------------
        unf = rod_row(tuple(range(13)), y=1.4, uw=0.7)
        a_l2 = arr([unf.get_left()[0] - 0.1, 1.4, 0], [unf.get_left()[0] - 0.8, 1.4, 0], GOLD, w=9, tip=0.3)
        a_r2 = arr([unf.get_right()[0] + 0.1, 1.4, 0], [unf.get_right()[0] + 0.8, 1.4, 0], GOLD, w=9, tip=0.3)
        self.at("force unfolds")
        self.play(Transform(folded, unf), Transform(a_l, a_l2), Transform(a_r, a_r2), run_time=1.1)
        sites = VGroup()
        XS = [-3.0, 0.0, 3.0]
        vins = VGroup(*[bchip("vinculin", TEAL, 22, 0.1).move_to([x, 0.35, 0]) for x in XS])
        vl = VGroup(*[link([x, vins[0].get_top()[1], 0], [x, 1.2, 0]) for x in XS])
        self.at("exposes vinculin sites")
        self.play(FadeIn(sites, scale=0.4), run_time=0.5)
        self.play(FadeIn(vins, shift=UP * 0.2), FadeIn(vl), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    """autoinhibition flap opens; talin on a mitochondrion recruits vinculin with myosin blocked; two systems."""

    def construct(self):
        body = RoundedRectangle(corner_radius=0.2, width=3.4, height=1.6, stroke_color=TEAL, stroke_width=4,
                                fill_color=TEAL, fill_opacity=0.25)
        name = T("talin or\nvinculin", 26, TEAL, line_spacing=0.6).move_to(body.get_center() + LEFT * 0.8)
        site = Circle(radius=0.2, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.9).move_to(
            body.get_center() + RIGHT * 0.8)
        flap = Rectangle(width=0.9, height=0.3, stroke_color=TEAL, stroke_width=3, fill_color=TEAL,
                         fill_opacity=0.9).move_to(site.get_center())
        prot = VGroup(body, name, site, flap).scale(1.3).move_to([0, 0.5, 0])
        l_auto = T("autoinhibition", 32, TEAL).move_to([0, -1.1, 0])
        self.play(FadeIn(prot), run_time=0.3)
        self.at("shut state")
        self.play(FadeIn(l_auto), run_time=0.5)

        # ---- into the cell -------------------------------------------------------------------
        cellp = RoundedRectangle(corner_radius=0.5, width=5.6, height=5.5, stroke_color=GREY, stroke_width=3,
                                 fill_color=GREY, fill_opacity=0.14).move_to([3.5, 0.25, 0])
        l_cell = T("mouse fibroblast", 24, GREY).move_to([3.5, 3.3, 0])
        mito = Ellipse(width=3.2, height=1.5, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.2)
        mito.move_to([3.5, 0.2, 0])
        l_mito = T("mitochondrion", 24, GREY).move_to([3.5, -0.8, 0])
        self.at("mouse fibroblasts")
        target = prot.copy().scale(0.55 / 1.3).move_to([3.5, 1.7, 0])
        nn = T("talin", 28, TEAL).scale(0.55).move_to(target[1].get_center())
        target[1].become(nn)
        anchor = link([3.5, 0.95, 0], [3.5, 1.27, 0], TEAL, 4)
        self.play(FadeIn(cellp), FadeIn(l_cell), FadeIn(mito), FadeIn(l_mito), FadeOut(l_auto),
                  Transform(prot, target), FadeIn(anchor), run_time=1.2)
        vin = bchip("vinculin", TEAL, 24).move_to([5.35, 2.7, 0])
        fl = prot[3]
        self.at("releasing it")
        self.play(Rotate(fl, angle=PI * 0.55, about_point=fl.get_left()), run_time=0.8)
        site_c = prot[2].get_center()
        self.at("talin and vinculin associate")
        vl = link([prot[0].get_right()[0], 1.7, 0], [4.6, 1.7, 0], TEAL, 3)
        self.play(vin.animate.move_to([5.35, 1.7, 0]), run_time=0.9)
        self.play(FadeIn(vl), run_time=0.2)
        myo = bchip("myosin II", GOLD, 24).move_to([3.5, -1.75, 0])
        cross = VGroup(Line(myo.get_corner(UL), myo.get_corner(DR), color=RED, stroke_width=5),
                       Line(myo.get_corner(DL), myo.get_corner(UR), color=RED, stroke_width=5))
        self.at("blocked")
        self.play(FadeIn(myo), run_time=0.4)
        self.play(Create(cross), run_time=0.5)

        # ---- the left panel: force exposes sites -----------------------------------------------
        unf = rod_row(UNF, y=0.3)
        unf.scale(4.3 / unf.total)
        unf.move_to([-3.6, 0.3, 0])
        a_l = arr([unf.get_left()[0] - 0.05, 0.3, 0], [unf.get_left()[0] - 0.55, 0.3, 0], GOLD, w=7, tip=0.22)
        a_r = arr([unf.get_right()[0] + 0.05, 0.3, 0], [unf.get_right()[0] + 0.55, 0.3, 0], GOLD, w=7, tip=0.22)
        sites = VGroup(*[Dot(unf[i].get_center(), radius=0.06, color=TEXT) for i in UNF])
        l_pur = T("purified fragment", 26, TEAL).move_to([-3.5, 3.3, 0])
        l_force = T("force can expose sites", 26, GOLD).move_to([-3.5, -3.1, 0])
        self.at("Purified fragments")
        self.play(FadeIn(l_pur), FadeIn(unf), FadeIn(a_l), FadeIn(a_r), FadeIn(sites), run_time=0.9)
        self.at("force can expose")
        self.play(FadeIn(l_force, shift=UP * 0.1), run_time=0.5)
        l_act = T("activation can, without force", 26, TEAL).move_to([3.5, -3.1, 0])
        self.at("A cell assay")
        self.play(FadeIn(l_act, shift=UP * 0.1), run_time=0.6)
        self.at("Keep the systems apart")
        div = VGroup(DashedLine([-0.1, 3.4, 0], [-0.1, 0.9, 0], color=GREY, stroke_width=3),
                     DashedLine([-0.1, -1.0, 0], [-0.1, -3.4, 0], color=GREY, stroke_width=3))
        self.play(Create(div), run_time=0.6)
        self.at("which route dominates")
        tq = VGroup(Circle(radius=0.45, stroke_color=GREY, stroke_width=3, fill_color=BG, fill_opacity=1),
                    T("?", 44, TEXT, weight=BOLD)).move_to([-0.1, 0.3, 0])
        tl = T("in a tissue", 22, GREY).move_to([-0.1, -0.5, 0])
        self.play(FadeIn(tq, scale=0.6), FadeIn(tl), run_time=0.7)
        self.finish()


class S07End(EndCard):
    LINE = "Force can expose sites. Activation can do it without force."
