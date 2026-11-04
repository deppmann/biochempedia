"""The Bax Trick  (chapter 3 of Competition: How Neurons Win a Target)

COLOR MAP (one color per concept, shared by every chapter; taken from scenes.old.py)
  BLUE   = a neuron whose fate is not yet decided (and the culture-dish neurons)
  GREEN  = a neuron that survives / is protected (Bax-null neurons)
  RED    = a neuron that dies, and the pro-death gene Bax
  YELLOW = nerve growth factor (NGF)
  PURPLE = the receptor TrkA (its level, its gene, its stain)
  PINK   = signaling downstream of TrkA
  ORANGE = the punishment signal (BDNF and NT-4)
  TEAL   = the receptor p75
  TEXT   = plain labels, white; also assay signal (stain, in situ dots, array spots)
  GOLD   = the question mark, "schematic" tags, "tagged for later", and one highlight at a time
  GREY   = ganglion outline, target, axons, axes, structure
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E8789F"
DARK = "#0f1117"


def P(x, y):
    return np.array([x, y, 0.0])


# ---------------------------------------------------------------------------------------------
# helpers
def cell(p, color=BLUE, r=0.26, op=0.85):
    return Circle(radius=r, stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=op).move_to(p)


def to_state(c, color, op=0.85):
    return c.animate.set_stroke(color, opacity=1.0).set_fill(color, opacity=op)


def ngf_dot(p, r=0.1):
    return Circle(radius=r, stroke_color=YELLOW, stroke_width=1.5, fill_color=YELLOW, fill_opacity=1).move_to(p)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.05, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def vbar(x, base, h, color=PURPLE, w=1.5):
    return Rectangle(width=w, height=max(h, 0.05), stroke_color=color, stroke_width=2, fill_color=color,
                     fill_opacity=0.85).move_to(P(x, base + max(h, 0.05) / 2))


def gang_outline(cx, cy, w, h):
    return Ellipse(width=w, height=h, stroke_color=GREY, stroke_width=3.5, fill_color=GREY, fill_opacity=0.08).move_to(P(cx, cy))


def gang_cells(cx, cy, w, h, sp=0.9, r=0.28, color=BLUE, op=0.85):
    """A hex-packed patch of neurons inside the ganglion outline; same arguments give the same cells."""
    rng = np.random.RandomState(11)
    m = r + 0.12
    pts = []
    for j in range(-12, 13):
        for i in range(-12, 13):
            x = i * sp + (sp / 2 if j % 2 else 0.0)
            y = j * sp * 0.866
            if (x / (w / 2 - m)) ** 2 + (y / (h / 2 - m)) ** 2 <= 1.0:
                pts.append((x + rng.uniform(-0.05, 0.05), y + rng.uniform(-0.05, 0.05)))
    return VGroup(*[cell(P(cx + x, cy + y), color, r, op) for x, y in pts])


def strike(c, color=TEXT, w=4):
    """A thin line through the middle of a chip that leaves its label readable."""
    return Line(c.get_left() + RIGHT * 0.05, c.get_right() + LEFT * 0.05, color=color, stroke_width=w).move_to(c.get_center())


def TL(lines, size=26, color=TEXT, buff=0.1):
    """Several short lines of text, centered on each other."""
    return VGroup(*[T(t, size, color) for t in lines]).arrange(DOWN, buff=buff)


def schematic_tag(x=5.7, y=-3.45, size=24):
    return T("schematic", size, GOLD).move_to(P(x, y))


def mouse(cx=0.0, cy=-0.4, s=1.7):
    """Schematic mouse outline, about 60% of the frame height. Returns (group, body_center)."""
    body = Ellipse(width=4.8, height=2.6)
    head = Ellipse(width=2.2, height=1.7).move_to(P(2.3, 0.1))
    ear1 = Circle(radius=0.5).move_to(P(1.7, 1.0))
    ear2 = Circle(radius=0.5).move_to(P(2.5, 1.1))
    shape = Union(body, head, ear1, ear2, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.14)
    nose = Circle(radius=0.12, stroke_color=GREY, fill_color=GREY, fill_opacity=1).move_to(P(3.35, 0.0))
    eye = Circle(radius=0.1, stroke_color=TEXT, fill_color=TEXT, fill_opacity=1).move_to(P(2.8, 0.3))
    tail = CubicBezier(P(-2.3, -0.3), P(-3.1, -0.6), P(-3.2, 0.7), P(-3.9, 0.8), stroke_color=GREY, stroke_width=5)
    g = VGroup(shape, nose, eye, tail)
    g.scale(s, about_point=ORIGIN)
    shift = P(cx, cy) - g.get_center()
    g.shift(shift)
    return g, shift.copy()


def dim_bars(cx, ys, w=3.2, h=0.52):
    return VGroup(*[RoundedRectangle(corner_radius=0.1, width=w, height=h, stroke_color=GREY, stroke_width=2.5,
                                     fill_color=GREY, fill_opacity=0.18).move_to(P(cx, y)) for y in ys])


def seg(x0, x1, color, text, y=3.2, h=0.9, size=28):
    r = Rectangle(width=x1 - x0, height=h, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=0.9)
    r.move_to(P((x0 + x1) / 2, y))
    t = T(text, size, DARK, weight=BOLD)
    if t.width > r.width - 0.3:
        t.scale((r.width - 0.3) / t.width)
    t.move_to(r)
    return VGroup(r, t)


# ganglia pair used in chapter scenes 5 to 7 (the pair fills about 65% of the frame height)
GXL, GXR, GY, GW, GH = -3.55, 3.55, 0.0, 5.4, 5.2


def ganglia_pair(color=BLUE, op=0.85, sp=0.82, r=0.26, gy=GY, gh=GH):
    oL, oR = gang_outline(GXL, gy, GW, gh), gang_outline(GXR, gy, GW, gh)
    cL = gang_cells(GXL, gy, GW, gh, sp, r, color, op)
    cR = gang_cells(GXR, gy, GW, gh, sp, r, color, op)
    return oL, oR, cL, cR


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Competition: How Neurons Win a Target"
    TITLE = "The Bax Trick"


# ---------------------------------------------------------------------------------------------
G1 = (-2.4, 0.1, 7.2, 5.4)       # big single ganglion, scenes 1 and 2


def survivors(n):
    return [i for i in range(n) if i % 5 == 0]


class S01(SpokenScene):
    def construct(self):
        out = gang_outline(*G1)
        cells = gang_cells(*G1, sp=0.95, r=0.3)
        lab = T("ganglion", 26, GREY).move_to(P(G1[0], -3.25))
        nchip = chip("NGF", YELLOW, 40).move_to(P(4.4, 2.4))
        src = T("target", 28, GREY).move_to(P(4.4, 3.4))
        ys = [1.3, 0.2, -0.9]
        dots = VGroup(*[ngf_dot(P(3.6, 2.15 - 0.12 * k), 0.12) for k in range(3)])
        q = T("?", 170, GOLD, weight=BOLD).move_to(P(4.4, -0.6))

        self.at("To learn")
        self.play(FadeIn(out), FadeIn(lab), LaggedStart(*[FadeIn(c, scale=0.4) for c in cells], lag_ratio=0.01),
                  run_time=0.6)
        self.at("NGF does")
        self.play(FadeIn(nchip, shift=DOWN * 0.2), FadeIn(src), FadeIn(dots), run_time=0.6)
        self.play(*[d.animate.move_to(P(1.7 + 0.45 * k, y)) for k, (d, y) in enumerate(zip(dots, ys))], run_time=1.5)
        self.at("you remove")
        x = Cross(nchip, stroke_color=RED, stroke_width=6).scale(0.9)
        self.play(Create(x), FadeOut(dots), run_time=0.7)
        self.at("the neurons die")
        dying = [i for i in range(len(cells)) if i not in survivors(len(cells))]
        self.play(*[to_state(cells[i], RED, 0.5) for i in dying], run_time=1.2)
        self.at("What now")
        self.play(FadeIn(q, scale=0.5), run_time=0.6)
        self.finish()


class S02(SpokenScene):
    def construct(self):
        out = gang_outline(*G1)
        cells = gang_cells(*G1, sp=0.95, r=0.3)
        n = len(cells)
        keep = survivors(n)
        for i in range(n):
            if i not in keep:
                cells[i].set_stroke(RED, opacity=1.0).set_fill(RED, opacity=0.5)
        lab = T("ganglion", 26, GREY).move_to(P(G1[0], -3.25))
        nchip = chip("NGF", YELLOW, 40).move_to(P(4.4, 2.4))
        x = Cross(nchip, stroke_color=RED, stroke_width=8).scale(0.9)
        self.add(out, cells, lab, nchip, x)

        self.at("Without NGF")
        self.play(Indicate(VGroup(nchip, x), color=YELLOW, scale_factor=1.1), run_time=0.8)
        self.at("neurons die")
        gone = [cells[i] for i in range(n) if i not in keep]
        self.play(LaggedStart(*[FadeOut(c, scale=0.3) for c in gone], lag_ratio=0.03), run_time=1.4)
        lbl = T("neuron loss confounds\nthe comparison", 30, GOLD, line_spacing=0.9).move_to(P(4.4, -0.3))
        self.at("Their loss")
        self.play(FadeIn(lbl, shift=LEFT * 0.2), run_time=0.8)
        self.at("comparison")
        self.play(Indicate(lbl, color=GOLD, scale_factor=1.06), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03(SpokenScene):
    def construct(self):
        who = T("Deppmann, Ginty and colleagues", 46, TEXT).move_to(P(0, 0.0))
        m, bc = mouse(0.0, -0.35, 1.7)
        gene = chip("Bax", RED, 48).move_to(bc + P(-0.6, 0.1))
        lbl = T("Bax removed", 40, TEXT).move_to(P(0, -3.4))
        x = strike(gene, TEXT, 5)

        self.play(FadeIn(who, shift=DOWN * 0.2), run_time=0.9)
        self.at("found a way")
        self.play(who.animate.scale(0.8).move_to(P(0, 3.4)), run_time=0.9)
        self.at("They used mice")
        self.play(Create(m[0]), FadeIn(m[1:]), run_time=0.8)
        self.at("lacking")
        self.play(FadeIn(gene, scale=0.6), run_time=0.35)
        self.play(Create(x), gene.animate.set_opacity(0.55), FadeIn(lbl), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04(SpokenScene):
    def construct(self):
        xs = [-5.0 + 2.0 * i for i in range(6)]
        NY = 0.1
        neurons = VGroup(*[cell(P(x, NY), BLUE, 0.68, 0.8) for x in xs])
        bax = chip("Bax", RED, 36).move_to(P(0, 2.8))
        pushes = VGroup(*[arr(P(0.3 * (x / 5.0), 2.3), P(x * 0.9, NY + 0.95), RED, 4, 0.16) for x in xs])
        gl = T("pro-death gene", 28, RED).move_to(P(3.3, 2.8))
        nchip = chip("NGF", YELLOW, 28).move_to(P(-5.2, -2.5))
        dots = VGroup(*[ngf_dot(P(-3.0 + 1.3 * i, -2.5), 0.13) for i in range(6)])
        wl = T("with NGF", 28, YELLOW).move_to(P(1.3, -3.3))
        legend = chip("Bax-null: survive", GREEN, 30).move_to(P(0, -1.35))

        self.play(LaggedStart(*[FadeIn(n, scale=0.4) for n in neurons], lag_ratio=0.03), FadeIn(nchip), FadeIn(dots),
                  FadeIn(wl), run_time=0.45)
        self.at("is the", lead=0.0)
        self.play(FadeIn(bax, shift=DOWN * 0.2), LaggedStart(*[GrowArrow(a) for a in pushes], lag_ratio=0.05), run_time=0.45)
        self.at("gene")
        self.play(FadeIn(gl), run_time=0.5)
        self.at("Without it")
        self.play(FadeOut(bax), FadeOut(pushes), FadeOut(gl), run_time=0.9)
        self.at("survive")
        self.play(*[to_state(n, GREEN, 0.85) for n in neurons], FadeIn(legend, shift=UP * 0.15), run_time=0.5)
        self.at("with or")
        self.play(Indicate(dots, color=YELLOW, scale_factor=1.25), run_time=0.7)
        wo = T("without NGF", 28, GREY).move_to(wl)
        self.at("without NGF")
        self.play(FadeOut(dots), Transform(wl, wo), run_time=0.7)
        self.play(*[Indicate(n, color=GREEN, scale_factor=1.12) for n in neurons], run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05(SpokenScene):
    def construct(self):
        oL, oR, cL, cR = ganglia_pair()
        self.at("compare two")
        self.play(FadeIn(oL), LaggedStart(*[FadeIn(c, scale=0.4) for c in cL], lag_ratio=0.02), run_time=0.55)
        self.at("ganglia")
        self.play(FadeIn(oR), LaggedStart(*[FadeIn(c, scale=0.4) for c in cR], lag_ratio=0.02), run_time=0.55)
        self.at("keep their")
        self.play(*[to_state(c, GREEN, 0.85) for c in list(cL) + list(cR)], run_time=0.8)
        self.finish()


def genotype_frame(scene):
    oL, oR, cL, cR = ganglia_pair(GREEN, 0.85)
    scene.add(oL, oR, cL, cR)
    return oL, oR, cL, cR


class S06(SpokenScene):
    def construct(self):
        oL, oR, cL, cR = genotype_frame(self)
        ll = T("Bax-null", 32, TEXT).move_to(P(GXL, 3.3))
        lr = T("Bax and NGF double-null", 30, TEXT).move_to(P(GXR, 3.3))
        cb1 = chip("no Bax", RED, 30).move_to(P(GXL, -3.3))
        cb2 = chip("no Bax", RED, 30).move_to(P(GXR - 1.2, -3.3))
        cn2 = chip("no NGF", YELLOW, 30).move_to(P(GXR + 1.2, -3.3))

        self.at("One comes from")
        self.play(FadeIn(ll), Indicate(oL, color=GREY, scale_factor=1.03), run_time=0.9)
        self.at("lacking")
        self.play(FadeIn(cb1, scale=0.7), run_time=0.7)
        self.at("the other comes")
        self.play(FadeIn(lr), Indicate(oR, color=GREY, scale_factor=1.03), run_time=0.9)
        self.at("mouse lacking", nth=1)
        self.play(FadeIn(cb2, scale=0.7), run_time=0.7)
        self.at("and NGF")
        self.play(FadeIn(cn2, scale=0.7), run_time=0.7)
        self.finish()


class S07(SpokenScene):
    def construct(self):
        oL, oR, cL, cR = genotype_frame(self)
        ll = T("Bax-null", 32, TEXT).move_to(P(GXL, 3.3))
        lr = T("Bax and NGF double-null", 30, TEXT).move_to(P(GXR, 3.3))
        self.add(ll, lr)
        da = DoubleArrow(P(-0.62, GY), P(0.62, GY), buff=0.0, color=YELLOW, stroke_width=7, tip_length=0.3)
        dl = chip("the difference is NGF", YELLOW, 34).move_to(P(0, -3.3))

        self.at("Because both")
        self.play(*[Indicate(c, color=GREEN, scale_factor=1.12) for c in list(cL) + list(cR)], run_time=1.0)
        self.at("any difference")
        self.play(GrowFromCenter(da), run_time=0.9)
        self.at("points to")
        self.play(FadeIn(dl, shift=UP * 0.2), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
GRX = (-3.3, 3.3)
SPG = 0.68
GRY = -0.45


def spot_pos(cx, r, c):
    return P(cx + (c - 2.5) * SPG, GRY + (2.5 - r) * SPG)


DIM = [(1, 2), (2, 4), (3, 1), (4, 3), (0, 5)]


def ganglion_icon(cx, cy, s=0.27):
    """The same ganglion as scenes 5 to 7, drawn small."""
    o = gang_outline(0, 0, GW, GH)
    cs = gang_cells(0, 0, GW, GH, 0.82, 0.26, GREEN, 0.85)
    cs.set_stroke(width=1.2)
    g = VGroup(o, cs).scale(s)
    return g.move_to(P(cx, cy))


class S08(SpokenScene):
    def construct(self):
        icons = [ganglion_icon(cx, 3.05) for cx in GRX]
        arrows = [arr(P(cx, 2.3), P(cx, 1.98), GREY, 5, 0.2) for cx in GRX]
        rl = [T("RNA", 26, TEXT).move_to(P(cx + 0.75, 2.14)) for cx in GRX]
        grids = []
        spots = [[], []]
        for k, cx in enumerate(GRX):
            frame = Rectangle(width=6 * SPG + 0.2, height=6 * SPG + 0.2, stroke_color=GREY, stroke_width=3,
                              fill_color=GREY, fill_opacity=0.08).move_to(P(cx, GRY))
            sp = VGroup(*[Circle(radius=0.22, stroke_width=0, fill_color=TEXT, fill_opacity=0.95).move_to(spot_pos(cx, r, c))
                          for r in range(6) for c in range(6)])
            spots[k] = sp
            grids.append(VGroup(frame, sp))
        names = [T("Bax-null", 26, TEXT).move_to(P(GRX[0], -2.9)), T("double-null", 26, TEXT).move_to(P(GRX[1], -2.9))]
        rings = VGroup(*[Circle(radius=0.32, stroke_color=GOLD, stroke_width=4).move_to(spot_pos(GRX[1], r, c)) for r, c in DIM])
        cand = T("candidate NGF-dependent genes", 30, GOLD).move_to(P(0, -3.55))

        self.play(*[FadeIn(i) for i in icons], run_time=0.8)
        self.at("whole ganglia")
        self.play(*[GrowArrow(a) for a in arrows], *[FadeIn(t) for t in rl], run_time=0.8)
        self.at("compared on")
        self.play(*[FadeIn(g, scale=0.9) for g in grids], FadeIn(names[0]), FadeIn(names[1]), run_time=1.0)
        self.at("Genes lower")
        self.play(*[spots[1][r * 6 + c].animate.set_fill(GREY, opacity=0.18) for r, c in DIM],
                  FadeIn(cand, shift=UP * 0.15), run_time=0.9)
        self.at("became")
        self.play(Create(rings), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S09(SpokenScene):
    def construct(self):
        PW, PH, PY = 4.3, 5.8, 0.35
        PX = [-4.55, 0.0, 4.55]
        HC = [PY + 1.45, PY - 1.45]            # centers of the Bax-null half and the double-null half
        STAIN = [{0, 2, 3, 5, 6}, {1, 6}]    # which of the 8 cells per half show signal (schematic)

        def panel(cx):
            return RoundedRectangle(corner_radius=0.15, width=PW, height=PH, stroke_color=GREY, stroke_width=3,
                                    fill_color=GREY, fill_opacity=0.08).move_to(P(cx, PY))

        def cpos(cx, hc, k):
            j, i = divmod(k, 4)
            return P(cx + (i - 1.5) * 0.82 + (0.41 if j % 2 else 0) - 0.2, hc + 0.1 - j * 0.8)

        def section(cx, stained):
            cs, sub = [], []
            for h, hc in enumerate(HC):
                sub.append(T(["Bax-null", "double-null"][h], 26, TEXT).move_to(P(cx, hc + 0.92)))
                for k in range(8):
                    on = stained and (k in STAIN[h])
                    cs.append(Circle(radius=0.27, stroke_color=GREY, stroke_width=2.5, fill_color=TEXT,
                                     fill_opacity=0.9 if on else 0.0).move_to(cpos(cx, hc, k)))
            div = DashedLine(P(cx - PW / 2 + 0.2, PY), P(cx + PW / 2 - 0.2, PY), color=GREY, stroke_width=2)
            return VGroup(div, *sub, *cs)

        def insitu_dots(cx):
            rng = np.random.RandomState(4)
            ds = []
            for h, hc in enumerate(HC):
                for k in sorted(STAIN[h]):
                    p = cpos(cx, hc, k)
                    for _ in range(4 if h == 0 else 2):
                        ds.append(Dot(P(p[0] + rng.uniform(-0.15, 0.15), p[1] + rng.uniform(-0.15, 0.15)), radius=0.05, color=TEXT))
            return VGroup(*ds)

        p1, p2, p3 = [panel(x) for x in PX]
        sec1 = section(PX[0], True)
        sec2 = section(PX[1], False)
        dots2 = insitu_dots(PX[1])

        DCY, DR = PY + 0.6, 1.95
        dish = Circle(radius=DR, stroke_color=GREY, stroke_width=3.5).move_to(P(PX[2], DCY))
        mid = DashedLine(P(PX[2], DCY - DR), P(PX[2], DCY + DR), color=GREY, stroke_width=2.5)
        lpos = [(-1.05, 0.9), (-0.55, -0.1), (-1.15, -0.75), (-0.5, 1.1), (-0.5, -1.0), (-1.2, 0.1), (-0.9, 1.3)]
        left = VGroup(*[cell(P(PX[2] + dx * 0.95, DCY + dy * 0.9), BLUE, 0.27, 0.85) for dx, dy in lpos])
        rpos = [(0.8, 0.5), (1.0, -0.6), (0.45, -0.1)]
        right = VGroup(*[cell(P(PX[2] + dx, DCY + dy), BLUE, 0.16, 0.3) for dx, dy in rpos])
        ngd = VGroup(*[ngf_dot(P(PX[2] - 0.35 - 0.38 * (i % 3) - 0.1, DCY + 1.2 - 0.5 * (i // 3) - 0.1 * (i % 2)), 0.08)
                       for i in range(9)])
        lw = T("with NGF", 30, YELLOW).move_to(P(PX[2] - 1.0, PY - 2.0))
        lwo = T("without", 30, GREY).move_to(P(PX[2] + 1.05, PY - 2.0))
        ly = PY - PH / 2 - 0.45
        l1 = T("staining", 28, TEXT).move_to(P(PX[0], ly))
        l2 = T("in situ hybridization", 26, TEXT).move_to(P(PX[1], ly))
        l3 = T("culture", 28, TEXT).move_to(P(PX[2], ly))
        sch = schematic_tag(5.6, -3.5)

        self.at("checked by")
        self.play(FadeIn(p1), FadeIn(p2), FadeIn(p3), FadeIn(sch), run_time=0.6)
        self.at("staining")
        self.play(FadeIn(sec1, scale=0.95), FadeIn(l1), run_time=0.8)
        self.at("in situ")
        self.play(FadeIn(sec2, scale=0.95), FadeIn(l2), run_time=0.6)
        self.play(FadeIn(dots2), run_time=0.6)
        self.at("in culture")
        self.play(FadeIn(dish), FadeIn(l3), run_time=0.4)
        self.at("with and")
        self.play(FadeIn(mid), FadeIn(left), FadeIn(ngd), FadeIn(lw), run_time=0.4)
        self.at("without NGF")
        self.play(FadeIn(right), FadeIn(lwo), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S10(SpokenScene):
    def construct(self):
        BX = [-4.95, -1.65, 1.65, 4.95]
        BW, BH, TOP = 3.1, 3.9, 2.0
        BY = TOP - BH / 2
        bins = VGroup(*[RoundedRectangle(corner_radius=0.15, width=BW, height=BH, stroke_color=GREY, stroke_width=3,
                                         fill_color=GREY, fill_opacity=0.07).move_to(P(x, BY)) for x in BX])
        texts = [["transcription", "factors"], ["synaptic", "genes"], ["metabolism", "and cell size"], ["axon", "growth"]]
        labs = [TL(t, 30).move_to(P(x, 2.75)) for t, x in zip(texts, BX)]
        rng = np.random.RandomState(2)
        fills = []
        for x in BX:
            rows = []
            for k in range(5):
                w = rng.uniform(2.0, 2.6)
                bar = RoundedRectangle(corner_radius=0.08, width=w, height=0.5, stroke_color=TEXT, stroke_width=1.5,
                                       fill_color=TEXT, fill_opacity=0.3).move_to(P(x, TOP - 0.55 - 0.72 * k))
                rows.append(VGroup(bar, T("gene", 24, TEXT).move_to(bar)))
            fills.append(VGroup(*rows))
        sch = schematic_tag(0, -2.75, 28)

        self.at("The list")
        self.play(FadeIn(bins), FadeIn(sch), run_time=0.8)
        for k, cue in enumerate(["transcription factors", "synaptic genes", "for metabolism", "for axon"]):
            self.at(cue)
            self.play(FadeIn(labs[k]), LaggedStart(*[FadeIn(r, shift=DOWN * 0.3) for r in fills[k]], lag_ratio=0.15),
                      run_time=1.3 if k != 1 else 1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
def question_frame():
    nA = VGroup(cell(P(-1.9, 2.55), BLUE, 0.7, 0.8), T("A", 34, TEXT).move_to(P(-1.9, 2.55)))
    nB = VGroup(cell(P(1.9, 2.55), BLUE, 0.7, 0.8), T("B", 34, TEXT).move_to(P(1.9, 2.55)))
    q1 = T("Which kind of gene could make", 42, GOLD).move_to(P(0, 0.85))
    q2 = T("a rich-get-richer loop?", 42, GOLD).move_to(P(0, 0.05))
    names = ["transcription factors", "synaptic genes", "metabolism and cell size", "axon growth"]
    cps = [(-5.4, -1.5), (0.6, -1.5), (-5.4, -2.35), (0.6, -2.35)]
    chips = VGroup(*[chip(n, GREY, 28).move_to(P(x, y), aligned_edge=LEFT) for n, (x, y) in zip(names, cps)])
    tag = T("pause and predict", 28, GREY).move_to(P(0, -3.15))
    return nA, nB, q1, q2, chips, tag


class S11(SpokenScene):
    def construct(self):
        nA, nB, q1, q2, chips, tag = question_frame()
        self.play(FadeIn(nA, scale=0.5), FadeIn(nB, scale=0.5), FadeIn(q1, shift=UP * 0.15), FadeIn(q2, shift=UP * 0.15),
                  run_time=0.8)
        self.at("kind of gene")
        self.play(LaggedStart(*[FadeIn(c, scale=0.8) for c in chips], lag_ratio=0.15), run_time=1.0)
        self.at("rich get richer")
        self.play(FadeIn(tag), Indicate(q2, color=GOLD, scale_factor=1.05), run_time=0.8)
        self.finish()


class S12Pause(NarratedScene):
    def construct(self):
        nA, nB, q1, q2, chips, tag = question_frame()
        self.add(nA, nB, q1, q2, chips, tag)
        track = Line(P(-4.0, -3.65), P(4.0, -3.65), color=GREY, stroke_width=4).set_opacity(0.25)
        prog = Line(P(-4.0, -3.65), P(4.0, -3.65), color=GOLD, stroke_width=6)
        self.add(track, prog)
        self.play(Uncreate(prog, rate_func=linear), run_time=4.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
LX = 4.1
LYS = [2.5, 1.5, 0.5, -0.5, -1.5, -2.5]


class S13(SpokenScene):
    def construct(self):
        NC, NR = P(-2.5, 0.0), 2.3
        neuron = cell(NC, BLUE, NR, 0.45)
        rec_ang = [150, 175, 200, 225]
        recs = VGroup()
        rpos = []
        for a in rec_ang:
            ang = a * DEGREES
            u = np.array([np.cos(ang), np.sin(ang), 0])
            base = NC + NR * u
            rr = RoundedRectangle(corner_radius=0.05, width=0.65, height=0.26, stroke_color=PURPLE, stroke_width=3,
                                  fill_color=PURPLE, fill_opacity=0.9).rotate(ang).move_to(base + 0.12 * u)
            recs.add(rr)
            rpos.append(base + 0.55 * u)
        dots = VGroup(*[ngf_dot(P(-6.4, p[1] + 0.05 * i), 0.14) for i, p in enumerate(rpos)])
        bars = dim_bars(LX, LYS, 3.2, 0.6)
        gene = chip("TrkA gene", PURPLE, 30).move_to(P(LX, LYS[2]))
        llab = T("genes on the list", 28, GREY).move_to(P(LX, 3.35))
        rlab = T("TrkA", 34, PURPLE).move_to(NC + P(-1.0, 0.1))
        link = Line(gene.get_left() + LEFT * 0.05, NC + P(NR + 0.05, 0.3), color=PURPLE, stroke_width=4)

        self.at("One whose product")
        self.play(FadeIn(neuron, scale=0.7), FadeIn(recs), run_time=1.0)
        self.at("catch more NGF")
        self.play(FadeIn(dots), run_time=0.2)
        self.play(*[d.animate.move_to(p) for d, p in zip(dots, rpos)], run_time=0.9)
        self.at("one gene")
        self.play(FadeIn(bars), FadeIn(llab), run_time=0.8)
        self.at("receptor itself")
        self.play(FadeOut(bars[2]), FadeIn(gene), Indicate(recs, color=PURPLE, scale_factor=1.3), FadeIn(rlab),
                  Create(link), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S14(SpokenScene):
    def construct(self):
        ny = 3.3
        cN = chip("NGF", YELLOW, 32).move_to(P(-2.4, ny))
        cT = chip("TrkA", PURPLE, 32).move_to(P(2.4, ny))
        a = arr(P(-1.1, ny), P(1.1, ny), GREY, 6, 0.28)
        raises = T("raises", 26, TEXT).move_to(P(0, ny - 0.5))
        gy, gh, gw, gx = -0.25, 4.7, 5.2, 3.65
        oL, oR = gang_outline(-gx, gy, gw, gh), gang_outline(gx, gy, gw, gh)
        cL = gang_cells(-gx, gy, gw, gh, 0.82, 0.26, PURPLE, 0.95)
        cR = gang_cells(gx, gy, gw, gh, 0.82, 0.26, PURPLE, 0.2)
        cR.set_stroke(GREY, opacity=0.8)
        g1 = T("Bax-null", 28, TEXT).move_to(P(-gx, -3.0))
        g2 = T("Bax and NGF double-null", 28, TEXT).move_to(P(gx, -3.0))
        s1 = T("NGF present", 26, YELLOW).move_to(P(-gx, -3.5))
        s2 = T("NGF absent", 26, GREY).move_to(P(gx, -3.5))
        tag = TL(["newborn", "ganglia,", "TrkA", "stain"], 30, TEXT, 0.12).move_to(P(0, -0.25))

        self.add(oL, oR, cL, cR, tag, g1, g2, s1, s2)
        self.at("NGF raises")
        self.play(FadeIn(cN), run_time=0.5)
        self.play(GrowArrow(a), FadeIn(cT, shift=RIGHT * 0.3), FadeIn(raises), run_time=0.9)
        self.at("newborn ganglia")
        self.play(Indicate(tag, color=GOLD, scale_factor=1.12), run_time=1.0)
        self.at("fell")
        self.play(Indicate(oR, color=GOLD, scale_factor=1.03), Indicate(s2, color=GOLD, scale_factor=1.15), run_time=1.1)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S15(SpokenScene):
    def construct(self):
        DC, R = P(-3.3, 0.35), 2.6
        dish = Circle(radius=R, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.08).move_to(DC)
        npos = [(-1.6, 1.2), (0.3, 1.7), (1.7, 0.8), (-0.8, -0.1), (1.0, -0.8), (-1.8, -1.2), (0.1, -1.8)]
        ncells = VGroup(*[cell(DC + P(dx, dy), BLUE, 0.4, 0.8) for dx, dy in npos])
        dpos = [(-1.8, 0.3), (-0.6, 0.6), (0.7, 1.9), (1.8, 1.2), (0.0, 0.2), (1.9, -0.4), (-0.5, -0.9), (1.2, -1.2),
                (-1.7, -1.5), (0.9, 0.1), (-0.2, 1.9), (-1.9, 1.4), (1.1, -1.8), (-1.0, 0.2)]
        ngd = VGroup(*[ngf_dot(DC + P(dx * 1.05, dy * 1.05), 0.11) for dx, dy in dpos])
        BX, BASE = 4.2, -2.4
        axis = VGroup(Line(P(2.7, BASE), P(5.8, BASE), color=GREY, stroke_width=3),
                      Line(P(2.7, BASE), P(2.7, 3.2), color=GREY, stroke_width=3))
        bar = vbar(BX, BASE, 0.9, PURPLE, 1.8)
        blab = T("TrkA level", 30, PURPLE).move_to(P(BX, 3.45))
        sch = schematic_tag(BX, -3.5)
        wl = T("with NGF", 30, YELLOW).move_to(P(-3.3, -3.1))
        wo = T("without NGF", 30, GREY).move_to(wl)
        bm = T("with NGF", 28, YELLOW).move_to(P(BX, -2.85))
        bm2 = T("NGF withdrawn", 28, GREY).move_to(P(BX, -2.85))

        self.at("In cultured")
        self.play(FadeIn(dish), FadeIn(ncells), FadeIn(axis), FadeIn(bar), FadeIn(blab), FadeIn(sch), run_time=0.5)
        self.at("track a")
        self.play(FadeIn(ngd, lag_ratio=0.1), FadeIn(wl), FadeIn(bm), Transform(bar, vbar(BX, BASE, 5.0, PURPLE, 1.8)), run_time=1.5)
        self.at("and fell")
        self.play(FadeOut(ngd), Transform(wl, wo), Transform(bm, bm2), Transform(bar, vbar(BX, BASE, 0.9, PURPLE, 1.8)), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
BARX, BBASE, BFULL = 0.0, -2.65, 4.8
SEG_A, SEG_B, SEG_C = (-6.4, -4.6), (-4.6, 1.0), (1.0, 6.4)


def signal_stuff():
    ghost = DashedVMobject(Rectangle(width=3.2, height=BFULL, stroke_color=GREY, stroke_width=3).move_to(P(BARX, BBASE + BFULL / 2)))
    lab = T("signaling downstream of TrkA", 28, PINK).move_to(P(-0.5, -3.2))
    normal = T("normal", 26, GREY).move_to(P(2.6, BBASE + BFULL - 0.25))
    return ghost, lab, normal


class S16(SpokenScene):
    def construct(self):
        ghost, lab, normal = signal_stuff()
        s1 = seg(*SEG_A, YELLOW, "NGF")
        s2 = seg(*SEG_B, GREY, "24 to 48 h without NGF")
        s3 = seg(*SEG_C, YELLOW, "NGF returns")
        bar = vbar(BARX, BBASE, BFULL, PINK, 3.0)
        low = T("still low", 32, PINK).move_to(P(3.0, BBASE + 1.2))
        sch = schematic_tag(5.6, -3.5)

        self.play(FadeIn(s1), FadeIn(ghost), GrowFromEdge(bar, DOWN), FadeIn(lab), FadeIn(normal), FadeIn(sch), run_time=0.35)
        self.at("long deprivation")
        self.play(GrowFromEdge(s2, LEFT), Transform(bar, vbar(BARX, BBASE, 0.9, PINK, 3.0)), run_time=1.1)
        self.at("signaling downstream")
        self.play(GrowFromEdge(s3, LEFT), run_time=1.0)
        self.at("greatly reduced")
        self.play(FadeIn(low, shift=LEFT * 0.2), Indicate(bar, color=PINK, scale_factor=1.04), run_time=1.0)
        self.finish()


class S17(SpokenScene):
    def construct(self):
        ghost, lab, normal = signal_stuff()
        s1 = seg(*SEG_A, YELLOW, "NGF")
        s2 = seg(*SEG_B, GREY, "12 h without NGF")
        s3 = seg(*SEG_C, YELLOW, "NGF returns")
        bar = vbar(BARX, BBASE, BFULL, PINK, 3.0)
        mostly = T("mostly sustained", 32, PINK).move_to(P(3.6, BBASE + BFULL * 0.68 - 0.2))
        sch = schematic_tag(5.6, -3.5)
        g2 = s2.copy().set_opacity(0.2)
        g3 = s3.copy().set_opacity(0.2)
        self.add(ghost, bar, lab, normal, s1, g2, g3, sch)

        self.at("deprived only briefly")
        self.play(FadeIn(s2), Transform(bar, vbar(BARX, BBASE, 0.9, PINK, 3.0)), run_time=1.3)
        self.at("sustain signaling")
        self.wait(0.3)
        self.at("NGF returned")
        self.play(FadeIn(s3), Transform(bar, vbar(BARX, BBASE, BFULL * 0.68, PINK, 3.0)),
                  FadeIn(mostly, shift=LEFT * 0.2), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
def loop_frame():
    top = chip("catches NGF", YELLOW, 34).move_to(P(0, 2.7))
    bot = chip("makes more TrkA", PURPLE, 34).move_to(P(0, -2.7))
    return top, bot


class S18(SpokenScene):
    def construct(self):
        top, bot = loop_frame()
        a1 = CurvedArrow(P(2.2, 2.4), P(2.2, -2.4), angle=-TAU / 5, color=GREY, stroke_width=6, tip_length=0.3)
        a2 = CurvedArrow(P(-2.2, -2.4), P(-2.2, 2.4), angle=-TAU / 5, color=GREY, stroke_width=6, tip_length=0.3)
        l1 = T("loop 1", 54, GOLD, weight=BOLD).move_to(P(0, 0.3))
        l2 = T("receptor level", 32, TEXT).move_to(P(0, -0.55))

        self.at("catches NGF")
        self.play(FadeIn(top, shift=DOWN * 0.2), run_time=0.7)
        self.at("makes more")
        self.play(Create(a1), run_time=0.9)
        self.play(FadeIn(bot, shift=UP * 0.2), run_time=0.7)
        self.at("that catches it")
        self.play(Create(a2), run_time=1.0)
        self.at("first loop")
        self.play(FadeIn(l1, scale=0.7), FadeIn(l2), run_time=0.8)
        self.play(Indicate(l1, color=GOLD, scale_factor=1.12), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S19(SpokenScene):
    def construct(self):
        PC, PR = P(-3.2, 0.2), 2.7
        a_ang0, a_ang = PI / 2, 0.52 * TAU
        secA = Sector(arc_center=PC, radius=PR, start_angle=a_ang0, angle=a_ang, stroke_color=TEXT, stroke_width=3,
                      fill_color=BLUE, fill_opacity=0.9)
        secB = Sector(arc_center=PC, radius=PR, start_angle=a_ang0 + a_ang, angle=0.48 * TAU, stroke_color=TEXT, stroke_width=3,
                      fill_color=BLUE, fill_opacity=0.45)
        mA, mB = a_ang0 + a_ang / 2, a_ang0 + a_ang + 0.24 * TAU
        tA = T("A  52%", 34, TEXT, weight=BOLD).move_to(PC + 1.5 * P(np.cos(mA), np.sin(mA)))
        tB = T("B  48%", 34, TEXT, weight=BOLD).move_to(PC + 1.5 * P(np.cos(mB), np.sin(mB)))
        pl = T("share of NGF caught", 30, YELLOW).move_to(P(-3.2, -3.35))
        pl2 = T("still 52 : 48", 32, GOLD).move_to(pl)
        cc = chip("capture", YELLOW, 34).move_to(P(3.7, 2.8))
        cs = chip("synthesis", PURPLE, 34).move_to(P(3.7, 1.5))
        pr = TL(["both in proportion", "to receptor"], 32, PURPLE).move_to(P(3.7, 0.0))
        lp = chip("loop 1 alone", GOLD, 36).move_to(P(3.7, -1.7))
        frozen = DashedVMobject(Circle(radius=PR + 0.25, stroke_color=GOLD, stroke_width=5).move_to(PC))

        self.at("But remember")
        self.play(GrowFromCenter(secA), GrowFromCenter(secB), run_time=1.0)
        self.at("two neurons")
        self.play(FadeIn(tA), FadeIn(tB), FadeIn(pl), run_time=0.8)
        self.at("With capture")
        self.play(FadeIn(cc, shift=LEFT * 0.2), run_time=0.7)
        self.at("and synthesis")
        self.play(FadeIn(cs, shift=LEFT * 0.2), run_time=0.7)
        self.at("in proportion")
        self.play(FadeIn(pr), run_time=0.8)
        self.at("this loop alone")
        self.play(FadeIn(lp, shift=UP * 0.2), run_time=0.7)
        self.at("keeps the shares")
        self.play(Create(frozen), run_time=0.9)
        self.at("where they started")
        self.play(Transform(pl, pl2), run_time=0.7)
        self.play(Indicate(pl, color=GOLD, scale_factor=1.1), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S20(SpokenScene):
    def construct(self):
        LX2 = -3.4
        bars = dim_bars(LX2, LYS, 3.4, 0.55)
        llab = T("genes on the list", 28, GREY).move_to(P(LX2, 3.35))
        bd = chip("BDNF", ORANGE, 30).move_to(P(LX2, LYS[1]))
        nt = chip("NT-4", ORANGE, 30).move_to(P(LX2, LYS[4]))
        p75 = chip("p75", TEAL, 44).move_to(P(4.0, 0.0))
        a1 = arr(P(LX2 + 1.0, LYS[1]), P(3.3, 0.6), ORANGE, 6, 0.28)
        a2 = arr(P(LX2 + 1.0, LYS[4]), P(3.3, -0.6), ORANGE, 6, 0.28)
        kl = T("can kill", 32, RED).move_to(P(4.0, -1.1))
        later = chip("matters later", GOLD, 36).move_to(P(3.9, 2.7))
        k1 = T("kills via p75", 28, TEAL).move_to(P(LX2 + 3.1, LYS[1] + 0.5))
        k2 = T("kills via p75", 28, TEAL).move_to(P(LX2 + 3.1, LYS[4] - 0.5))

        self.at("Two other genes")
        self.play(FadeIn(bars), FadeIn(llab), run_time=0.8)
        self.at("matter later")
        self.play(FadeIn(later, shift=DOWN * 0.2), run_time=0.7)
        self.at("BDNF and")
        self.play(FadeOut(bars[1]), FadeIn(bd), FadeIn(k1), run_time=0.7)
        self.at("and", lead=-0.2)
        self.play(FadeOut(bars[4]), FadeIn(nt), FadeIn(k2), run_time=0.7)
        self.at("neurotrophins")
        self.play(Indicate(VGroup(bd, nt), color=ORANGE, scale_factor=1.1), run_time=0.8)
        self.at("kill through")
        self.play(FadeIn(p75, scale=0.7), GrowArrow(a1), GrowArrow(a2), run_time=1.0)
        self.play(FadeIn(kl), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S21(SpokenScene):
    def construct(self):
        gx, gw, gh = -4.0, 3.8, 3.3
        icons = []
        for y in (1.95, -1.95):
            o = gang_outline(gx, y, gw, gh)
            cs = gang_cells(gx, y, gw, gh, 0.66, 0.19, GREEN, 0.85)
            icons.append(VGroup(o, cs))
        l1 = T("Bax-null", 28, TEXT).move_to(P(-0.1, 2.6))
        l2 = T("double-null", 28, TEXT).move_to(P(-0.1, -2.6))
        tgt = RoundedRectangle(corner_radius=0.25, width=4.5, height=6.6, stroke_color=GREY, stroke_width=4,
                               fill_color=GREY, fill_opacity=0.12).move_to(P(4.2, 0.0))
        tl = T("target", 30, GREY).move_to(P(4.2, 2.75))
        ax = VGroup(Line(P(gx + gw / 2, 1.9), P(1.95, 1.0), color=GREY, stroke_width=4),
                    Line(P(gx + gw / 2, -1.9), P(1.95, -1.0), color=GREY, stroke_width=4))
        qt = TL(["Do survivors", "innervate the", "target normally?"], 32, GOLD).move_to(P(4.2, 1.0))
        q = T("?", 120, GOLD, weight=BOLD).move_to(P(4.2, -1.0))
        tag = chip("last chapter", GOLD, 28).move_to(P(4.2, -2.6))

        self.at("The same two")
        self.play(*[FadeIn(i, scale=0.9) for i in icons], FadeIn(l1), FadeIn(l2), run_time=1.0)
        self.at("also answer")
        self.play(FadeIn(tgt), FadeIn(tl), Create(ax), run_time=1.0)
        self.at("a question")
        self.play(FadeIn(qt, shift=UP * 0.15), run_time=0.8)
        self.at("innervation")
        self.play(FadeIn(q, scale=0.5), run_time=0.7)
        self.at("The last chapter")
        self.play(FadeIn(tag, shift=DOWN * 0.2), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S22(SpokenScene):
    def construct(self):
        head = T("Takeaway", 40, GOLD, weight=BOLD).move_to(P(0, 3.35))
        div = Line(P(0, 2.7), P(0, -3.4), color=GREY, stroke_width=2.5).set_opacity(0.5)
        bax = chip("Bax", RED, 36).move_to(P(-3.4, 2.0))
        bx = strike(bax, TEXT, 4)
        neurons = VGroup(*[cell(P(-5.6 + 1.2 * i, 0.5), GREEN, 0.5, 0.85) for i in range(5)])
        ngfc = chip("NGF", YELLOW, 34).move_to(P(-3.4, -1.0))
        nx = strike(ngfc, RED, 4)
        alive = T("neurons stay alive", 36, GREEN).move_to(P(-3.4, -2.5))
        n2 = chip("NGF", YELLOW, 36).move_to(P(3.4, 2.0))
        t2 = chip("TrkA", PURPLE, 36).move_to(P(3.4, -0.9))
        a = arr(P(3.4, 1.3), P(3.4, -0.2), GREY, 6, 0.28)
        up = TL(["raises its", "own receptor"], 36, PURPLE).move_to(P(3.4, -2.55))

        self.at("Take away", lead=0.0)
        self.play(FadeIn(head), FadeIn(div), run_time=0.7)
        self.at("trick keeps")
        self.play(FadeIn(bax), FadeIn(neurons), run_time=0.5)
        self.play(Create(bx), run_time=0.3)
        self.at("alive without")
        self.play(FadeIn(ngfc), run_time=0.4)
        self.play(Create(nx), FadeIn(alive), run_time=0.7)
        self.at("It showed that")
        self.play(FadeIn(n2, shift=DOWN * 0.2), run_time=0.5)
        self.at("NGF raises")
        self.play(GrowArrow(a), FadeIn(t2, shift=UP * 0.2), FadeIn(up), run_time=0.8)
        self.finish()


class S23End(EndCard):
    LINE = "The Bax trick keeps neurons alive without NGF; NGF raises its receptor."

    def construct(self):
        l1 = T("The Bax trick keeps neurons alive", 48, font=TITLE_FONT)
        l2 = T("without NGF; NGF raises its receptor.", 48, font=TITLE_FONT)
        for t in (l1, l2):
            if t.width > 12.4:
                t.scale(12.4 / t.width)
        sub = T("biochemistrypedia.com", 24, color=TEAL)
        top = VGroup(l1, l2).arrange(DOWN, buff=0.3)
        g = VGroup(top, sub).arrange(DOWN, buff=0.6).move_to(ORIGIN)
        self.play(FadeIn(top, shift=UP * 0.15), run_time=self.beat(0.3))
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        self.finish()
