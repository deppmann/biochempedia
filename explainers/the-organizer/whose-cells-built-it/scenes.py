"""The Organizer, chapter 2: Whose Cells Built It?  (Biochemistrypedia chaptered film)

COLOR MAP (one color per concept, whole film; shared with the other chapters)
  BLUE   = ectoderm on its way to skin / host ectoderm / the responder (competent ectoderm)
  PURPLE = neural fate (neural plate, neural tube, axis)
  GREEN  = mesoderm (stroke); somites
  CREAM  = donor origin: the pale graft, cells with no pigment, notochord; "organizer"
  AMBER  = pigment granules (dots on a cell mean: host cell, from the pigmented embryo)
  YELLOW = the signal / what moves or is highlighted
  GREY   = outlines, neutral embryos, labels
  RED    = the open question
A cell's fill shows where it came from (cream = donor; fate colour + amber dots = host);
its outline shows what it became.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
CREAM = "#F2EBD3"
AMBER = "#E39A3C"
AMBER_T = "#FFC266"   # brighter amber for text on the dark ground
PURPLE_T = "#D2B0F0"
RED_T = "#FF8A80"
GREYL = "#BAC1CE"   # label grey
CY = 0.1
DOT_OFFS = ((-0.15, 0.04), (-0.04, 0.15), (0.12, 0.08), (0.14, -0.1), (-0.07, -0.11), (0.02, -0.01))


# ------------------------------------------------------------------ helpers
def cell(x, y, fate=BLUE, r=0.3, donor=False, dots=False):
    if donor:
        c = Circle(radius=r, stroke_color=fate, stroke_width=3, fill_color=CREAM, fill_opacity=0.85)
    else:
        c = Circle(radius=r, stroke_color=fate, stroke_width=3, fill_color=fate, fill_opacity=0.5)
    g = VGroup(c)
    if dots:
        for dx, dy in DOT_OFFS:
            g.add(Dot([dx * r / 0.3, dy * r / 0.3, 0], radius=0.04 * r / 0.3 * 1.15, color=AMBER))
    g.move_to([x, y, 0])
    g.base, g.r = c, r
    return g


def paint(g, fate, donor=False):
    if donor:
        return g.base.animate.set_stroke(fate).set_fill(CREAM, 0.85)
    return g.base.animate.set_stroke(fate).set_fill(fate, 0.5)


def dots_of(g):
    """amber dots to add to a cell that has none (host marker), at the cell's current place."""
    r = g.base.radius
    c = g.base.get_center()
    return [Dot(c + np.array([dx * r / 0.3, dy * r / 0.3, 0]), radius=0.04 * r / 0.3 * 1.15, color=AMBER) for dx, dy in DOT_OFFS]


def lab(text, color=GREY, size=24, **kw):
    return T(text, size, GREYL if color == GREY else color, **kw)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def ring_pos(n, c, R, off=0.5, span=TAU, start=-PI / 2):
    out = []
    for k in range(n):
        a = start + span * (k + off) / n - (span - TAU) / 2 * 0
        out.append(np.array([c[0] + R * np.cos(a), c[1] + R * np.sin(a), 0]))
    return out


def open_pos(n, c, R, gap=PI * 0.55):
    """cells on a U (a ring with an opening at the top)."""
    span = TAU - gap
    out = []
    for k in range(n):
        a = -PI / 2 - span / 2 + span * k / (n - 1)
        out.append(np.array([c[0] + R * np.cos(a), c[1] + R * np.sin(a), 0]))
    return out


def pt(c, rx, ry, a):
    return np.array([c[0] + rx * np.cos(a), c[1] + ry * np.sin(a), 0])


def arc_on(c, rx, ry, a1, a2, color=YELLOW, w=11):
    return ParametricFunction(lambda t: np.array([c[0] + rx * np.cos(t), c[1] + ry * np.sin(t), 0]),
                              t_range=[a1, a2, 0.04], color=color, stroke_width=w)


def tangent_angle(rx, ry, a):
    return np.arctan2(ry * np.cos(a), -rx * np.sin(a))


def normal(rx, ry, a):
    n = np.array([np.cos(a) / rx, np.sin(a) / ry, 0])
    return n / np.linalg.norm(n)


def capsule(c, rx, ry, a, L=2.2, th=0.46, color=PURPLE, lift=0.1):
    cap = RoundedRectangle(corner_radius=th / 2, width=L, height=th, stroke_color=color, stroke_width=3,
                           fill_color=color, fill_opacity=0.6)
    cap.rotate(tangent_angle(rx, ry, a))
    cap.move_to(pt(c, rx, ry, a) + normal(rx, ry, a) * lift)
    return cap


def patch_at(c, rx, ry, a, w=0.8, h=0.42, fill=YELLOW, stroke=YELLOW):
    p = RoundedRectangle(corner_radius=0.1, width=w, height=h, stroke_color=stroke, stroke_width=3,
                         fill_color=fill, fill_opacity=0.9)
    p.rotate(tangent_angle(rx, ry, a))
    p.move_to(pt(c, rx, ry, a))
    return p


def scatter(c, rx, ry, n=34, seed=4, radius=0.06):
    rng = np.random.RandomState(seed)
    out = VGroup()
    while len(out) < n:
        p = rng.uniform(-1, 1, 2)
        if p[0] ** 2 + p[1] ** 2 < 0.78:
            out.add(Dot([c[0] + p[0] * rx, c[1] + p[1] * ry, 0], radius=radius, color=AMBER))
    return out


def embryo(c, rx, ry, kind="neutral"):
    col, op = {"neutral": (GREY, 0.22), "pale": (CREAM, 0.55), "dark": (AMBER, 0.28)}[kind]
    return Ellipse(width=2 * rx, height=2 * ry, stroke_color=col, stroke_width=4, fill_color=col,
                   fill_opacity=op).move_to([c[0], c[1], 0])


def hexcluster(c, r=0.5, fate=GREY, donor=False, dots=False):
    sp = 2.15 * r
    pos = [(0, 0)] + [(sp * np.cos(k * PI / 3), sp * np.sin(k * PI / 3)) for k in range(6)]
    return VGroup(*[cell(c[0] + dx, c[1] + dy, fate, r, donor, dots) for dx, dy in pos])


# ------------------------------------------------------------------ hypothesis cards
CARD_W, CARD_H = 6.5, 6.4
CX1, CX2 = -3.5, 3.5


def card_frame(cx, color=GREY, sw=3):
    return RoundedRectangle(corner_radius=0.2, width=CARD_W, height=CARD_H, stroke_color=color, stroke_width=sw,
                            fill_color=BG, fill_opacity=1).move_to([cx, CY, 0])


def card_title(cx, text, color=TEXT):
    return T(text, 30, color, weight=BOLD).move_to([cx, CY + 2.85, 0])


def strip_row(cx, y, n=9, sp=0.66, r=0.3, dots=False):
    return [cell(cx + (i - (n - 1) / 2) * sp, y, BLUE, r, dots=dots) for i in range(n)]


def graft_row(cx, y, r=0.3, sp=0.66):
    return [cell(cx + (i - 1) * sp, y, CREAM, r, donor=True) for i in range(3)]


RING_Y, RING_R = CY + 1.3, 0.8


def card_ring(cx, kind):
    pos = ring_pos(8, [cx + RING_DX, RING_Y], RING_R)
    if kind == "donor":
        return [cell(p[0], p[1], PURPLE, 0.27, donor=True) for p in pos]
    return [cell(p[0], p[1], PURPLE, 0.27) for p in pos]


H1_NOTE = "in its own embryo, the dorsal lip mainly\nmakes notochord and dorsal mesoderm"
STRIP_Y, HOSTLAB_Y, GRAFT_Y, NOTE_Y = CY - 0.4, CY + 0.1, CY - 1.78, CY - 2.68
RING_DX = -0.45


def host_lab(cx):
    return lab("host ectoderm (future skin)", BLUE, 26).move_to([cx, HOSTLAB_Y, 0])


def h1_state():
    """card 1 complete + card 2 empty frame."""
    d = {}
    d["f1"], d["f2"] = card_frame(CX1), card_frame(CX2)
    d["t1"] = card_title(CX1, "1 · Self-differentiation")
    d["t2"] = T("2", 30, GREY, weight=BOLD).move_to([CX2, CY + 2.85, 0])
    d["strip"] = strip_row(CX1, STRIP_Y)
    d["hl"] = host_lab(CX1)
    d["graft"] = graft_row(CX1, GRAFT_Y)
    d["glab"] = lab("graft", CREAM, 26).move_to([CX1 + 1.55, GRAFT_Y, 0])
    d["ring"] = card_ring(CX1, "donor")
    d["tag"] = lab("tube =\ndonor cells", CREAM, 26, line_spacing=0.8).move_to([CX1 + 1.95, RING_Y, 0])
    d["note"] = lab(H1_NOTE, GREY, 26, line_spacing=0.8).move_to([CX1, NOTE_Y, 0])
    fit(d["note"], max_w=6.1)
    return d


def h2_state():
    d = {}
    d["t2"] = card_title(CX2, "2 · Induction")
    d["strip"] = strip_row(CX2, STRIP_Y)
    d["hl"] = host_lab(CX2)
    d["graft"] = graft_row(CX2, GRAFT_Y)
    d["glab"] = lab("graft", CREAM, 26).move_to([CX2 + 1.55, GRAFT_Y, 0])
    d["ring"] = card_ring(CX2, "host")
    d["tag"] = lab("tube =\nhost cells", PURPLE, 26, line_spacing=0.8).move_to([CX2 + 1.95, RING_Y, 0])
    d["arrows"] = VGroup(*[arr([CX2 + 0.66 * k, GRAFT_Y + 0.35, 0], [CX2 + 0.66 * k, STRIP_Y - 0.62, 0], YELLOW, w=5, tip=0.14) for k in (-1, 0, 1)])
    return d


def cards_final_mobs():
    """Both cards as they stand at the end of s04: (list of mobjects, dict handles)."""
    s, h = h1_state(), h2_state()
    for i in (3, 4, 5):
        h["strip"][i].base.set_stroke(PURPLE).set_fill(PURPLE, 0.5)
    f2 = s["f2"].set_stroke(TEXT)
    mobs = [s["f1"], f2, s["t1"], h["t2"], *s["strip"], s["hl"], *s["graft"], s["glab"], *s["ring"], s["tag"], s["note"],
            *h["strip"], h["hl"], *h["graft"], h["glab"], *h["ring"], h["tag"], h["arrows"]]
    return mobs, s, h


class S00Title(TitleCard):
    LESSON = "The Organizer: Spemann and Mangold"
    TITLE = "Whose Cells Built It?"


# ------------------------------------------------------------------ 1  the question
class S01Q(SpokenScene):
    def construct(self):
        c, rx, ry = [0, -0.15], 2.5, 2.3
        emb = embryo(c, rx, ry)
        self.add(emb)
        a_lip, a_site = np.radians(132), np.radians(-38)
        lip = arc_on(c, rx, ry, a_lip - 0.3, a_lip + 0.3)
        lab_lip = lab("dorsal lip", YELLOW, 26).move_to([-3.9, 2.0, 0])
        self.at("dorsal lip")
        self.play(Create(lip), FadeIn(lab_lip), run_time=0.5)
        patch = patch_at(c, rx, ry, a_lip)
        self.at("moved to a new place")
        self.play(FadeOut(lab_lip), FadeOut(lip), FadeIn(patch), run_time=0.3)
        path = ArcBetweenPoints(pt(c, rx, ry, a_lip) + normal(rx, ry, a_lip) * 0.3,
                                pt(c, rx, ry, a_site) + normal(rx, ry, a_site) * 0.3, angle=-PI * 0.9)
        self.play(MoveAlongPath(patch, path), run_time=1.3)
        cap = capsule(c, rx, ry, a_site)
        lab_ax = lab("second axis", PURPLE, 26).move_to([5.0, -0.9, 0])
        self.at("second body")
        self.play(GrowFromPoint(cap, pt(c, rx, ry, a_site)), FadeIn(lab_ax), run_time=0.8)
        tv = np.array([np.cos(tangent_angle(rx, ry, a_site)), np.sin(tangent_angle(rx, ry, a_site)), 0])
        qs = VGroup(*[T("?", 44, RED, weight=BOLD).move_to(cap.get_center() + tv * dx + normal(rx, ry, a_site) * 0.95)
                      for dx in (-0.5, 0.0, 0.5)])
        q = T("Whose cells built it?", 42, TEXT, font=TITLE_FONT).move_to([0, -3.35, 0])
        self.at("whose cells built it")
        self.play(FadeIn(qs, lag_ratio=0.2), FadeIn(q, shift=UP * 0.15), run_time=0.8)
        self.finish()


# ------------------------------------------------------------------ 2  same species
class S02Same(SpokenScene):
    def construct(self):
        cl, cr, R = [-3.6, 0.1], [3.6, 0.1], 2.3
        el, er = embryo(cl, R, R), embryo(cr, R, R)
        a_lip, a_site = np.radians(35), np.radians(-140)
        lip = arc_on(cl, R, R, a_lip - 0.3, a_lip + 0.3)
        self.add(el, er, lip)
        sp = lab("one species", GREY, 28).move_to([0, 3.4, 0])
        br = Line([-5.8, 2.95, 0], [5.8, 2.95, 0], color=GREY, stroke_width=3)
        d_l = lab("donor", CREAM, 30).move_to([-3.6, -2.55, 0])
        h_l = lab("host", BLUE, 30).move_to([3.6, -2.55, 0])
        self.at("within one species")
        self.play(FadeIn(sp), Create(br), FadeIn(d_l), FadeIn(h_l), run_time=0.6)
        patch = patch_at(cl, R, R, a_lip)
        self.at("had given", lead=0.5)
        self.play(FadeOut(lip), FadeIn(patch), run_time=0.2)
        path = ArcBetweenPoints(pt(cl, R, R, a_lip) + normal(R, R, a_lip) * 0.3,
                                pt(cr, R, R, a_site) + normal(R, R, a_site) * 0.3, angle=PI * 0.55)
        self.play(MoveAlongPath(patch, path), run_time=0.9)
        cap = capsule(cr, R, R, a_site, L=2.0)
        l_ax = lab("extra axial structures", PURPLE, 28).move_to([3.6, -3.35, 0])
        self.at("extra axial structures")
        self.play(GrowFromPoint(cap, pt(cr, R, R, a_site)), FadeIn(l_ax), run_time=0.8)
        self.at("donor and host cells")
        cl_cells = hexcluster([-3.6, 0.2], 0.55)
        cr_cells = hexcluster([3.6, 0.2], 0.55)
        l_d = lab("donor cells", CREAM, 30).move_to([-3.6, -2.85, 0])
        l_h = lab("host cells", BLUE, 30).move_to([3.6, -2.85, 0])
        self.play(FadeOut(VGroup(el, er, patch, cap, l_ax, sp, br, d_l, h_l)), run_time=0.4)
        self.play(FadeIn(cl_cells, scale=1.6), FadeIn(cr_cells, scale=1.6), FadeIn(l_d), FadeIn(l_h), run_time=0.7)
        eq = T("=", 80, TEXT, weight=BOLD).move_to([0, 0.2, 0])
        self.at("look alike")
        self.play(FadeIn(eq, scale=0.6), run_time=0.4)
        self.finish()


# ------------------------------------------------------------------ 3  reading 1
class S03H1(SpokenScene):
    def construct(self):
        s = h1_state()
        self.at("two readings", lead=0.05)
        self.play(FadeIn(s["f1"]), FadeIn(s["f2"]), FadeIn(s["t2"]), run_time=0.5)
        self.at("self differentiation")
        self.play(FadeIn(s["t1"], shift=UP * 0.1), run_time=0.4)
        self.at("graft cells")
        self.play(LaggedStart(*[FadeIn(c) for c in s["strip"]], lag_ratio=0.04),
                  LaggedStart(*[FadeIn(c) for c in s["graft"]], lag_ratio=0.1), FadeIn(s["glab"]), FadeIn(s["hl"]), run_time=0.9)
        self.at("own origin")
        self.play(*[Indicate(c, color=YELLOW, scale_factor=1.25) for c in s["graft"]], FadeIn(s["note"]), run_time=0.9)
        self.at("make the tube themselves")
        self.play(LaggedStart(*[FadeIn(c, scale=0.4) for c in s["ring"]], lag_ratio=0.1), FadeIn(s["tag"]), run_time=1.0)
        self.finish()


class S04H2(SpokenScene):
    def construct(self):
        s = h1_state()
        self.add(s["f1"], s["f2"], s["t1"], s["t2"], *s["strip"], s["hl"], *s["graft"], s["glab"], *s["ring"], s["tag"], s["note"])
        h = h2_state()
        self.at("induction")
        self.play(FadeOut(s["t2"]), FadeIn(h["t2"], shift=UP * 0.1), s["f2"].animate.set_stroke(TEXT), run_time=0.5)
        self.at("the graft changes")
        self.play(LaggedStart(*[FadeIn(c) for c in h["strip"]], lag_ratio=0.04),
                  LaggedStart(*[FadeIn(c) for c in h["graft"]], lag_ratio=0.1), FadeIn(h["glab"]), FadeIn(h["hl"]), run_time=0.9)
        self.at("fate of its")
        self.play(LaggedStart(*[GrowArrow(a) for a in h["arrows"]], lag_ratio=0.1), run_time=0.5)
        self.play(*[paint(h["strip"][i], PURPLE) for i in (3, 4, 5)], run_time=0.6)
        self.at("host cells build")
        self.play(LaggedStart(*[FadeIn(c, scale=0.4) for c in h["ring"]], lag_ratio=0.1), FadeIn(h["tag"]), run_time=1.0)
        self.finish()


# ------------------------------------------------------------------ 5  credit
class S05Colour(SpokenScene):
    def construct(self):
        word = T("colour", 96, TEXT, font=TITLE_FONT).move_to([0, 0.5, 0])
        dp = Circle(radius=0.8, stroke_color=CREAM, stroke_width=4, fill_color=CREAM, fill_opacity=0.6).move_to([-4.6, 0.5, 0])
        dd = Circle(radius=0.8, stroke_color=AMBER, stroke_width=4, fill_color=AMBER, fill_opacity=0.28).move_to([4.6, 0.5, 0])
        dd_dots = scatter([4.6, 0.5], 0.8, 0.8, 12, seed=7, radius=0.07)
        self.play(FadeIn(word, shift=UP * 0.15), FadeIn(dp), FadeIn(dd), FadeIn(dd_dots), run_time=0.8)
        self.at("mangold")
        self.play(FadeOut(VGroup(word, dp, dd, dd_dots)), run_time=0.4)
        name = T("Hilde Mangold", 64, TEXT, font=TITLE_FONT).move_to([0, 1.3, 0])
        role = lab("doctoral student", GREY, 32).move_to([0, 0.4, 0])
        self.play(FadeIn(name, shift=UP * 0.15), FadeIn(role), run_time=0.6)
        lbl = T("Hans Spemann's laboratory, Freiburg", 36, CREAM).move_to([0, -0.9, 0])
        self.at("spemann's laboratory")
        self.play(FadeIn(lbl, shift=UP * 0.1), run_time=0.6)
        self.at("doctoral thesis")
        self.play(Indicate(role, color=YELLOW, scale_factor=1.15), run_time=0.9)
        self.finish()


# ------------------------------------------------------------------ 6  two species
EL, ER = [-3.5, 0.8], [3.5, 0.8]
ER_R = 2.4


class S06Species(SpokenScene):
    def construct(self):
        el, er = embryo(EL, ER_R, ER_R, "pale"), embryo(ER, ER_R, ER_R, "dark")
        d = scatter(ER, ER_R, ER_R, 46)
        self.add(el, er, d)
        n1 = T("Triton cristatus", 32, CREAM, slant=ITALIC).move_to([-3.5, -2.0, 0])
        n2 = T("Triton taeniatus", 32, AMBER_T, slant=ITALIC).move_to([3.5, -2.0, 0])
        self.at("species")
        self.play(FadeIn(n1), FadeIn(n2), run_time=0.5)
        self.at("cells of one")
        self.play(Indicate(el, color=CREAM, scale_factor=1.03), run_time=0.4)
        s1 = lab("little pigment", CREAM, 30).move_to([-3.5, -2.75, 0])
        self.at("carry little pigment")
        self.play(FadeIn(s1), run_time=0.4)
        self.at("cells of the other")
        self.play(Indicate(er, color=AMBER, scale_factor=1.03), run_time=0.4)
        s2 = lab("pigment granules", AMBER_T, 30).move_to([3.5, -2.75, 0])
        self.at("carry pigment granules", lead=0.0)
        self.play(FadeIn(s2), run_time=0.35)
        self.finish()


# ------------------------------------------------------------------ 7  the marker
class S07Marker(SpokenScene):
    def construct(self):
        frame = RoundedRectangle(corner_radius=0.2, width=12.6, height=4.4, stroke_color=GREY, stroke_width=3,
                                 fill_color=GREY, fill_opacity=0.06).move_to([0, 0.3, 0])
        donors = {(0, 4), (1, 3), (1, 4), (2, 4)}
        cells = []
        for row, (n, x0, y) in enumerate([(9, -5.2, 1.45), (8, -4.55, 0.3), (9, -5.2, -0.85)]):
            for i in range(n):
                cells.append((row, i, cell(x0 + 1.3 * i, y, BLUE, 0.58, donor=(row, i) in donors, dots=(row, i) not in donors)))
        grp = VGroup(*[c for _, _, c in cells])
        sec = lab("a thin section of tissue", GREY, 28).move_to([0, 2.85, 0])
        self.play(FadeIn(frame), FadeIn(grp, lag_ratio=0.02), FadeIn(sec), run_time=0.8)
        self.at("stay visible")
        host = [d for _, _, c in cells for d in c[1:]]
        self.play(*[Indicate(d, color=YELLOW, scale_factor=1.8) for d in host], run_time=1.0)
        lm = T("lineage marker", 52, AMBER_T, font=TITLE_FONT, weight=BOLD).move_to([0, 3.3, 0])
        self.at("so color")
        self.play(FadeOut(sec), FadeIn(lm, shift=UP * 0.1), run_time=0.4)
        l_d = lab("pale cell: donor", CREAM, 32).move_to([2.6, -2.7, 0])
        l_h = lab("pigmented cell: host", AMBER_T, 32).move_to([-3.6, -2.7, 0])
        pal = [c for r_, i_, c in cells if (r_, i_) == (2, 4)][0]
        pig = [c for r_, i_, c in cells if (r_, i_) == (2, 1)][0]
        a_d = arr([1.8, -2.25, 0], [0.15, -1.5, 0], CREAM)
        a_h = arr([-3.7, -2.25, 0], [-3.9, -1.5, 0], AMBER_T)
        self.at("shows which")
        self.play(FadeIn(l_d), GrowArrow(a_d), FadeIn(l_h), GrowArrow(a_h), run_time=0.7)
        self.finish()


# ------------------------------------------------------------------ 8  cut
PALE_C, HOST_C, ER2 = [0, -0.2], [3.5, -0.2], 2.3
LIP_A = np.radians(125)


class S08Cut(SpokenScene):
    def construct(self):
        pale = embryo(PALE_C, ER2, ER2, "pale")
        lip = arc_on(PALE_C, ER2, ER2, LIP_A - 0.22, LIP_A + 0.22)
        dates = T("1921 and 1922", 52, TEXT, font=TITLE_FONT).move_to([0, 3.2, 0])
        self.play(FadeIn(pale), FadeIn(lip), FadeIn(dates), run_time=0.5)
        cutbox = DashedVMobject(RoundedRectangle(corner_radius=0.1, width=1.25, height=0.8, stroke_color=YELLOW, stroke_width=4), num_dashes=24)
        cutbox.rotate(tangent_angle(ER2, ER2, LIP_A)).move_to(pt(PALE_C, ER2, ER2, LIP_A))
        self.at("cut a piece", lead=0.6)
        self.play(Create(cutbox), run_time=0.35)
        piece = patch_at(PALE_C, ER2, ER2, LIP_A, w=1.0, h=0.6, fill=CREAM, stroke=YELLOW)
        notch = RoundedRectangle(corner_radius=0.1, width=1.0, height=0.6, stroke_color=GREY, stroke_width=3,
                                 fill_color=BG, fill_opacity=1).rotate(tangent_angle(ER2, ER2, LIP_A)).move_to(pt(PALE_C, ER2, ER2, LIP_A))
        self.play(FadeOut(lip), FadeOut(cutbox), FadeIn(notch), FadeIn(piece), run_time=0.2)
        self.play(piece.animate.move_to([3.1, 1.2, 0]).scale(1.2), run_time=0.7)
        l_lip = lab("dorsal lip", YELLOW, 28).move_to([3.1, 2.05, 0])
        self.at("dorsal lip")
        self.play(FadeIn(l_lip), run_time=0.4)
        l_pale = lab("pale gastrula", CREAM, 28).move_to([0, -3.0, 0])
        self.at("pale gastrula")
        self.play(FadeIn(l_pale), run_time=0.4)
        self.finish()


def cut_state():
    pale = embryo(PALE_C, ER2, ER2, "pale")
    notch = RoundedRectangle(corner_radius=0.1, width=1.0, height=0.6, stroke_color=GREY, stroke_width=3,
                             fill_color=BG, fill_opacity=1).rotate(tangent_angle(ER2, ER2, LIP_A)).move_to(pt(PALE_C, ER2, ER2, LIP_A))
    piece = patch_at(PALE_C, ER2, ER2, LIP_A, w=1.2, h=0.72, fill=CREAM, stroke=YELLOW).move_to([3.1, 1.2, 0])
    l_pale = lab("pale gastrula", CREAM, 28).move_to([0, -3.0, 0])
    return pale, notch, piece, l_pale


class S09Place(SpokenScene):
    def construct(self):
        pale, notch, piece, l_pale = cut_state()
        left = VGroup(pale, notch, piece, l_pale)
        self.add(left)
        host = embryo(HOST_C, ER2, ER2, "dark")
        hd = scatter(HOST_C, ER2, ER2, 42)
        self.play(left.animate.shift(LEFT * 3.5), FadeIn(host), FadeIn(hd), run_time=0.4)
        self.at("placed it", lead=0.3)
        target = np.array([HOST_C[0], HOST_C[1] - ER2 + 0.7, 0])
        self.play(piece.animate(path_arc=-PI * 0.5).scale(0.9).rotate(-tangent_angle(ER2, ER2, LIP_A)).move_to(target), run_time=1.1)
        belly = lab("belly", TEXT, 30).move_to([3.5, -3.1, 0])
        hl = lab("pigmented gastrula", AMBER_T, 30).move_to([3.5, 2.65, 0])
        self.play(FadeIn(belly), FadeIn(hl), Indicate(host, color=AMBER, scale_factor=1.04), run_time=0.6)
        skin = lab("future belly skin", BLUE, 30).move_to([3.5, -3.1, 0])
        self.at("tissue that would")
        self.play(ReplacementTransform(belly, skin), run_time=0.6)
        note = lab("host stages in the series varied", GREY, 26).move_to([3.5, 3.45, 0])
        self.at("become skin")
        self.play(FadeIn(note), run_time=0.5)
        self.finish()


# ------------------------------------------------------------------ 10  second plate
SEC_Y = -2.1


class S10Rise(SpokenScene):
    def construct(self):
        xs = [-5.2, -2.6, 0, 2.6, 5.2]
        embs = []
        for x in xs:
            e = embryo([x, 0.2], 1.1, 1.1, "dark")
            dd = scatter([x, 0.2], 1.1, 1.1, 14, seed=int(x * 7 + 3) % 9 + 1, radius=0.05)
            p = patch_at([x, 0.2], 1.1, 1.1, -PI / 2, w=0.5, h=0.3, fill=CREAM, stroke=CREAM)
            embs.append(VGroup(e, dd, p))
        self.play(FadeIn(VGroup(*embs), lag_ratio=0.05), run_time=0.5)
        self.at("embryos died")
        self.play(*[FadeOut(embs[i]) for i in (0, 1, 3, 4)], run_time=0.9)
        self.at("in the survivors")
        self.play(embs[2].animate.scale(2.6).shift(UP * 0.1), run_time=0.8)
        # section view of the survivor: host tissue below, ectoderm strip on top, graft inside
        body = RoundedRectangle(corner_radius=0.3, width=12.4, height=3.1, stroke_color=AMBER, stroke_width=3,
                                fill_color=AMBER, fill_opacity=0.16).move_to([0, SEC_Y + 0.2, 0])
        bd = scatter([0, SEC_Y + 0.2], 6.0, 1.4, 60, seed=5, radius=0.05)
        for d in bd:
            d.set_opacity(0.8)
        strip = [cell((i - 5) * (1.75 * (TAU - PI * 0.55) / 8), 0.0, BLUE, 0.46) for i in range(11)]
        graft = [cell((i - 1) * 0.95, -1.65, CREAM, 0.42, donor=True) for i in range(3)]
        l_host = lab("pigmented host embryo (section)", AMBER_T, 28).move_to([-2.9, -3.65, 0])
        l_graft = lab("graft", CREAM, 28).move_to([2.2, -1.65, 0])
        self.at("second neural plate")
        self.play(FadeOut(embs[2]), FadeIn(body), FadeIn(bd), FadeIn(VGroup(*strip), lag_ratio=0.02), FadeIn(VGroup(*graft)),
                  FadeIn(l_host), FadeIn(l_graft), run_time=0.5)
        plate = list(range(1, 10))
        l_plate = lab("second neural plate", TEXT, 34).move_to([3.8, 1.45, 0])
        self.play(*[paint(strip[i], GREY) for i in plate], FadeIn(l_plate), run_time=0.5)
        self.at("rose")
        self.play(*[strip[i].animate.shift(UP * 0.55) for i in plate], l_plate.animate.shift(UP * 0.3), run_time=0.6)
        ctr = [0, 1.2]
        self.at("folded")
        # Bend a chain with fixed arc length, so adjacent cells stay apart
        # throughout folding, rather than crossing on straight tween paths.
        def bend_plate(group, alpha):
            step = (TAU - PI * 0.55) / 8
            for k, c in enumerate(group):
                theta = (k - 4) * step * alpha
                if alpha < 1e-6:
                    x, rise = (k - 4) * step * 1.75, 0
                else:
                    radius = 1.75 / alpha
                    x, rise = radius * np.sin(theta), radius * (1 - np.cos(theta))
                c.move_to([x, 0.55 - 1.1 * alpha + rise, 0])
        self.play(UpdateFromAlphaFunc(VGroup(*[strip[i] for i in plate]), bend_plate),
                  FadeOut(l_plate), run_time=1.0)
        # Preserve the U's cell ordering when the opening closes.
        cp = ring_pos(9, ctr, 1.75, off=0, start=-PI / 2 - TAU * 4 / 9)
        self.at("closed into")
        self.play(*[strip[i].animate.move_to(cp[k]) for k, i in enumerate(plate)], run_time=0.8)
        l_tube = lab("second neural tube", TEXT, 30).move_to([4.3, 1.55, 0])
        self.play(FadeIn(l_tube), run_time=0.4)
        self.finish()


# ------------------------------------------------------------------ 11-13  prediction table
ROWY = [1.9, -0.1, -2.3]
LBX, RBX = -3.2, 2.9
LW, RW, RH = 5.4, 6.2, 1.95


def box(x, y, w, h=RH, color=GREY, op=0.08, sw=2.5):
    return RoundedRectangle(corner_radius=0.15, width=w, height=h, stroke_color=color, stroke_width=sw,
                            fill_color=color, fill_opacity=op).move_to([x, y, 0])


def row_label(i, text, sub=None):
    t = T(text, 30, TEXT, weight=BOLD)
    if sub:
        s = lab(sub, GREY, 26, line_spacing=0.8)
        g = VGroup(t, s).arrange(DOWN, buff=0.1)
    else:
        g = VGroup(t)
    return g.move_to([LBX, ROWY[i], 0])


def answer(i, kind):
    """icons + text inside the right-hand box of row i."""
    y = ROWY[i]
    if kind == "pale":
        ic = [cell(0, 0, PURPLE, 0.3, donor=True) for _ in range(4)]
        txt = "nearly all pale"
    elif kind == "pig":
        ic = [cell(0, 0, PURPLE, 0.3, dots=True) for _ in range(4)]
        txt = "nearly all pigmented"
    else:
        ic = [cell(0, 0, PURPLE, 0.3, donor=True), cell(0, 0, PURPLE, 0.3, dots=True), cell(0, 0, PURPLE, 0.3, donor=True), cell(0, 0, PURPLE, 0.3, dots=True)]
        txt = "a mix; host cells still induced"
    icons = VGroup(*ic).arrange(RIGHT, buff=0.12)
    t = T(txt, 28, TEXT)
    g = VGroup(icons, t).arrange(DOWN, buff=0.12).move_to([RBX, y, 0])
    return g


def qmark(i):
    return T("?", 64, RED_T, weight=BOLD).move_to([RBX, ROWY[i], 0])


def table_state():
    d = {}
    d["head_l"] = lab("reading", GREY, 28).move_to([LBX, 3.4, 0])
    d["head_r"] = lab("colour of the new tube", GREY, 28).move_to([RBX, 3.4, 0])
    d["lb"] = [box(LBX, ROWY[i], LW) for i in range(2)]
    d["rb"] = [box(RBX, ROWY[i], RW) for i in range(2)]
    d["lt"] = [row_label(0, "1  Self-differentiation"), row_label(1, "2  Induction")]
    d["q"] = [qmark(0), qmark(1)]
    d["ans"] = [answer(0, "pale"), answer(1, "pig")]
    d["lb3"], d["rb3"] = box(LBX, ROWY[2], LW), box(RBX, ROWY[2], RW)
    d["lt3"] = row_label(2, "3  Both", "host cells still show induction")
    d["ans3"] = answer(2, "mix")
    d["pred"] = T("Predict: what colour is the new tube?", 40, YELLOW, font=TITLE_FONT).move_to([0, ROWY[2], 0])
    return d


class S11Q(SpokenScene):
    def construct(self):
        d = table_state()
        self.play(FadeIn(d["head_l"]), FadeIn(d["head_r"]), *[FadeIn(b) for b in d["lb"] + d["rb"]], run_time=0.5)
        self.at("predict", lead=0.0)
        self.play(FadeIn(d["pred"], shift=UP * 0.1), run_time=0.5)
        self.at("simply grew")
        self.play(FadeIn(d["lt"][0]), d["rb"][0].animate.set_stroke(YELLOW), run_time=0.5)
        self.at("what color")
        self.play(FadeIn(d["q"][0], scale=0.5), run_time=0.5)
        self.at("changed its")
        self.play(FadeIn(d["lt"][1]), d["rb"][1].animate.set_stroke(YELLOW), run_time=0.5)
        self.play(FadeIn(d["q"][1], scale=0.5), run_time=0.5)
        self.finish()


def add_table_question(scene):
    d = table_state()
    scene.add(d["head_l"], d["head_r"], *d["lb"], *d["rb"], *d["lt"], *d["q"], d["pred"])
    d["rb"][0].set_stroke(YELLOW)
    d["rb"][1].set_stroke(YELLOW)
    return d


class S12Pause(NarratedScene):
    def construct(self):
        add_table_question(self)
        self.finish()


class S13Pred(SpokenScene):
    def construct(self):
        d = add_table_question(self)
        d["rb"][0].set_stroke(GREY)
        d["rb"][1].set_stroke(GREY)
        self.at("if the graft grew", lead=0.0)
        self.play(d["lb"][0].animate.set_stroke(YELLOW), run_time=0.3)
        self.at("tube should be pale", lead=0.3)
        self.play(FadeOut(d["q"][0]), run_time=0.25)
        self.play(FadeIn(d["ans"][0], shift=UP * 0.1), run_time=0.5)
        self.at("if it changed")
        self.play(d["lb"][0].animate.set_stroke(GREY), d["lb"][1].animate.set_stroke(YELLOW),
                  FadeOut(d["pred"]), FadeIn(d["lb3"]), FadeIn(d["rb3"]),
                  FadeIn(d["lt3"]), FadeIn(d["ans3"]), run_time=0.5)
        self.at("tube should be pigmented", lead=0.3)
        self.play(FadeOut(d["q"][1]), run_time=0.25)
        self.play(FadeIn(d["ans"][1], shift=UP * 0.1), run_time=0.5)
        self.play(d["lb"][1].animate.set_stroke(GREY), run_time=0.2)
        self.finish()


# ------------------------------------------------------------------ 14-16  the sections
RC, RR, RN, RRAD = [-1.3, 0.45], 2.0, 12, 0.5


def tube12(c=RC, R=RR, r=RRAD):
    pos = ring_pos(RN, c, R, off=0.5)
    return [cell(p[0], p[1], PURPLE, r) for p in pos]


FLOOR = (0, 1)   # the two cells at the bottom of the ring


class S14Reveal1(SpokenScene):
    def construct(self):
        tube = tube12()
        cap = lab("section through the second neural tube", GREY, 26).move_to([-1.3, -3.0, 0])
        self.at("in one embryo", lead=0.0)
        self.play(FadeIn(VGroup(*tube), lag_ratio=0.05), FadeIn(cap), run_time=0.9)
        l_p = lab("pigmented: host cells", AMBER, 30).move_to([4.2, 1.9, 0])
        a_p = arr([2.2, 1.8, 0], [1.1, 1.3, 0], AMBER)
        self.at("second tube was pigmented")
        dots = [d for i in range(2, RN) for d in dots_of(tube[i])]
        self.play(*[FadeIn(d, scale=2.2) for d in dots], FadeIn(l_p), GrowArrow(a_p), run_time=1.0)
        l_s = lab("pale: from the graft", CREAM, 30).move_to([4.3, -1.7, 0])
        a_s = arr([2.2, -1.8, 0], [-0.55, -1.95, 0], CREAM)
        self.at("narrow pale strip")
        self.play(*[paint(tube[i], PURPLE, donor=True) for i in FLOOR], FadeIn(l_s), GrowArrow(a_s), run_time=0.8)
        self.finish()


def reveal1_state():
    tube = tube12()
    for i in FLOOR:
        tube[i].base.set_fill(CREAM, 0.85)
    dots = [d for i in range(2, RN) for d in dots_of(tube[i])]
    cap = lab("section through the second neural tube", GREY, 26).move_to([-1.3, -3.0, 0])
    l_p = lab("pigmented: host cells", AMBER, 30).move_to([4.2, 1.9, 0])
    a_p = arr([2.2, 1.8, 0], [1.1, 1.3, 0], AMBER)
    l_s = lab("pale: from the graft", CREAM, 30).move_to([4.3, -1.7, 0])
    a_s = arr([2.2, -1.8, 0], [-0.55, -1.95, 0], CREAM)
    return tube, dots, cap, l_p, a_p, l_s, a_s


C15, R15, r15 = [-1.3, 1.2], 1.6, 0.4


def tube15():
    pos = ring_pos(RN, C15, R15, off=0.5)
    tube = [cell(p[0], p[1], PURPLE, r15, dots=True) for p in pos]
    return tube


def below15():
    noto = cell(C15[0], -1.55, CREAM, 0.55, donor=True)
    meso = [cell(C15[0] + dx, -1.55, GREEN, 0.42, donor=True) for dx in (-2.3, -1.3, 1.3, 2.3)]
    l_p = lab("pigmented: host cells", AMBER, 30).move_to([4.2, 2.1, 0])
    a_p = arr([2.2, 2.0, 0], [0.5, 1.6, 0], AMBER)
    l_n = lab("second notochord", CREAM, 30).move_to([4.2, -2.6, 0])
    a_n = arr([2.0, -2.5, 0], [-0.65, -2.0, 0], CREAM)
    l_m = lab("pale nearby mesoderm", CREAM, 28).move_to([4.2, -1.2, 0])
    a_m = arr([2.0, -1.3, 0], [-0.4, -1.45, 0], CREAM)
    return noto, meso, l_p, a_p, l_n, a_n, l_m, a_m


class S15Reveal2(SpokenScene):
    def construct(self):
        tube, dots, cap, l_p, a_p, l_s, a_s = reveal1_state()
        self.add(*tube, *dots, cap, l_p, a_p, l_s, a_s)
        fd = [d for i in FLOOR for d in dots_of(tube[i])]
        self.at("in another")
        self.play(*[paint(tube[i], PURPLE) for i in FLOOR], *[FadeIn(d, scale=2.2) for d in fd],
                  FadeOut(l_s), FadeOut(a_s), FadeOut(cap), run_time=0.8)
        allc = VGroup(*tube, *dots, *fd)
        self.at("whole tube")
        self.play(allc.animate.scale(0.8, about_point=np.array([RC[0], RC[1], 0])).shift(np.array([C15[0] - RC[0], C15[1] - RC[1], 0])),
                  FadeOut(l_p), FadeOut(a_p), run_time=0.7)
        l_p2 = lab("pigmented: host cells", AMBER, 30).move_to([4.2, 2.1, 0])
        a_p2 = arr([2.2, 2.0, 0], [0.5, 1.6, 0], AMBER)
        self.play(FadeIn(l_p2), GrowArrow(a_p2), run_time=0.5)
        noto, meso, _, _, l_n, a_n, l_m, a_m = below15()
        self.at("pale graft lay beneath")
        self.play(FadeIn(noto, shift=UP * 0.2), FadeIn(VGroup(*meso), lag_ratio=0.15), run_time=0.9)
        self.at("as a notochord")
        self.play(FadeIn(l_n), GrowArrow(a_n), run_time=0.5)
        self.at("nearby mesoderm")
        self.play(FadeIn(l_m), GrowArrow(a_m), run_time=0.5)
        self.finish()


def reveal2_state(scene):
    t2 = tube15()
    noto, meso, l_p, a_p, l_n, a_n, l_m, a_m = below15()
    scene.add(*t2, noto, *meso, l_p, a_p, l_n, a_n, l_m, a_m)


class S16Beat(NarratedScene):
    def construct(self):
        reveal2_state(self)
        self.finish()


# ------------------------------------------------------------------ 17  both happened
class S17Won(SpokenScene):
    def construct(self):
        mobs, s, h = cards_final_mobs()
        self.add(*mobs)
        s["f2"].set_stroke(YELLOW, width=6)       # card 2 lit from the start
        both = T("both happened", 38, TEXT, font=TITLE_FONT, weight=BOLD).move_to([0, -3.68, 0])
        self.at("host ectoderm", lead=0.0)
        self.play(Indicate(VGroup(*h["strip"], h["hl"]), color=YELLOW, scale_factor=1.06), run_time=0.9)
        self.at("made a neural tube")
        self.play(*[Indicate(c, color=YELLOW, scale_factor=1.2) for c in h["ring"]], run_time=0.8)
        # card 1: the graft's own cells became notochord
        noto = cell(CX1 - 1.3, RING_Y, CREAM, 0.5, donor=True)
        new_tag = lab("graft's own cells\nbecame notochord", CREAM, 26, line_spacing=0.8).move_to([CX1 + 1.3, RING_Y, 0])
        self.at("for the tube")
        self.play(*[ReplacementTransform(c, noto) if k == 0 else FadeOut(c) for k, c in enumerate(s["ring"])],
                  FadeOut(s["tag"]), run_time=0.6)
        self.play(FadeIn(new_tag), s["f1"].animate.set_stroke(CREAM, width=5), run_time=0.5)
        self.at("induction explained")
        self.play(FadeIn(both, shift=UP * 0.1), run_time=0.4)
        self.finish()


# ------------------------------------------------------------------ 18  definition
def def_state(scene=None):
    d = {}
    d["title"] = T("induction", 64, YELLOW, font=TITLE_FONT, weight=BOLD).move_to([0, 3.1, 0])
    d["text"] = T("a change in the fate of one tissue,\ncaused by a signal from another", 38, TEXT, line_spacing=0.9).move_to([0, 1.55, 0])
    d["top"] = [cell(-5.6 + 0.9 * i, -0.35, BLUE, 0.4) for i in range(9)]
    d["bot"] = [cell(-3.2 + 0.9 * i, -2.5, CREAM, 0.4, donor=True) for i in range(3)]
    d["l_top"] = lab("one tissue:\nits fate changes", BLUE, 28).move_to([4.3, -0.35, 0])
    d["l_bot"] = lab("another tissue:\nsends the signal", CREAM, 28).move_to([3.3, -2.5, 0])
    d["arrows"] = VGroup(*[arr([-3.2 + 0.9 * i, -1.95, 0], [-3.2 + 0.9 * i, -0.95, 0], YELLOW, w=6, tip=0.2) for i in range(3)])
    return d


class S18Def(SpokenScene):
    def construct(self):
        d = def_state()
        self.at("induction is a change", lead=0.0)
        self.play(FadeIn(d["title"], shift=UP * 0.1), FadeIn(d["text"]), FadeIn(VGroup(*d["top"]), lag_ratio=0.04),
                  FadeIn(VGroup(*d["bot"]), lag_ratio=0.1), run_time=0.9)
        self.at("fate of one tissue")
        self.play(FadeIn(d["l_top"]), run_time=0.4)
        self.at("caused by a signal")
        self.play(FadeIn(d["l_bot"]), LaggedStart(*[GrowArrow(a) for a in d["arrows"]], lag_ratio=0.1), run_time=0.7)
        self.play(*[paint(d["top"][i], PURPLE) for i in range(2, 7)], run_time=0.7)
        self.finish()


# ------------------------------------------------------------------ 19-20  three roles
AXC = 3.4   # x centre of the axis diagram
TUBE_C = [AXC, 1.2]
NOTO_C = [AXC, -0.95]
SOM_L, SOM_R = [AXC - 2.3, 0.35], [AXC + 2.3, 0.35]


def role_list(n):
    heads = ["Its own cells\nbecome notochord", "Recruits host mesoderm\ninto somites", "Induces host ectoderm\nto become a neural tube"]
    ys = [1.7, -0.3, -2.4]
    out = []
    for k in range(n):
        num = T(str(k + 1), 40, YELLOW, weight=BOLD).move_to([-6.2, ys[k], 0])
        txt = T(heads[k], 28, TEXT, line_spacing=0.85)
        txt.next_to(num, RIGHT, buff=0.3).align_to(num, UP).shift(DOWN * 0.0)
        txt.move_to([txt.get_center()[0], ys[k], 0])
        out.append(VGroup(num, txt))
    return out


def somite(c):
    blk = RoundedRectangle(corner_radius=0.12, width=1.25, height=1.25, stroke_color=GREEN, stroke_width=4,
                           fill_color=GREEN, fill_opacity=0.18).move_to([c[0], c[1], 0])
    cs = VGroup(*[cell(c[0] + dx, c[1] + dy, GREEN, 0.2, dots=True) for dx in (-0.28, 0.28) for dy in (-0.28, 0.28)])
    return VGroup(blk, cs)


def fate_chips():
    """vertebra and muscle chips under each somite."""
    out = []
    for c in (SOM_L, SOM_R):
        out.append(chip("vertebra", GREEN, 26).move_to([c[0], c[1] - 1.1, 0]))
        out.append(chip("muscle", GREEN, 26).move_to([c[0], c[1] - 1.8, 0]))
    return VGroup(*out)


class S19Roles(SpokenScene):
    def construct(self):
        hdr = lab("the graft did", GREY, 28).move_to([-4.4, 3.2, 0])
        nums = VGroup(*[T(str(k + 1), 40, GREY, weight=BOLD).move_to([-6.2, y, 0]) for k, y in enumerate([1.7, -0.3, -2.4])])
        self.at("three things", lead=0.3)
        self.play(FadeIn(hdr), FadeIn(nums, lag_ratio=0.3), run_time=0.8)
        r1 = role_list(1)[0]
        noto = cell(NOTO_C[0], NOTO_C[1], CREAM, 0.6, donor=True)
        l_n = lab("notochord", CREAM, 28).move_to([AXC, -1.95, 0])
        self.at("own cells")
        self.play(FadeOut(nums[0]), FadeIn(r1), run_time=0.5)
        self.at("became notochord")
        self.play(FadeIn(noto, scale=1.6), FadeIn(l_n), run_time=0.7)
        self.finish()


class S19bSomites(SpokenScene):
    def construct(self):
        hdr = lab("the graft did", GREY, 28).move_to([-4.4, 3.2, 0])
        nums = VGroup(*[T(str(k + 1), 40, GREY, weight=BOLD).move_to([-6.2, y, 0]) for k, y in enumerate([1.7, -0.3, -2.4])])
        r1 = role_list(1)[0]
        noto = cell(NOTO_C[0], NOTO_C[1], CREAM, 0.6, donor=True)
        l_n = lab("notochord", CREAM, 28).move_to([AXC, -1.95, 0])
        self.add(hdr, nums[1], nums[2], r1, noto, l_n)
        r2 = role_list(2)[1]
        self.at("recruited host mesoderm")
        self.play(FadeOut(nums[1]), FadeIn(r2), run_time=0.4)
        loose = []
        for c in (SOM_L, SOM_R):
            for dx, dy in ((-0.5, 0.45), (0.45, 0.5), (-0.4, -0.5), (0.5, -0.4)):
                loose.append(cell(c[0] + dx, c[1] + dy, GREEN, 0.2, dots=True))
        self.play(FadeIn(VGroup(*loose), lag_ratio=0.1), run_time=0.8)
        som_l, som_r = somite(SOM_L), somite(SOM_R)
        l_s1 = lab("somite", GREEN, 26).move_to([SOM_L[0], SOM_L[1] + 1.15, 0])
        l_s2 = lab("somite", GREEN, 26).move_to([SOM_R[0], SOM_R[1] + 1.15, 0])
        self.at("into somites")
        self.play(ReplacementTransform(VGroup(*loose[:4]), som_l), ReplacementTransform(VGroup(*loose[4:]), som_r),
                  FadeIn(l_s1), FadeIn(l_s2), run_time=0.9)
        ghost = DashedVMobject(Circle(radius=1.2, stroke_color=GREY, stroke_width=3).move_to([TUBE_C[0], TUBE_C[1], 0]), num_dashes=22)
        self.at("blocks beside the tube")
        self.play(Create(ghost), run_time=0.7)
        self.at("vertebrae")
        self.play(FadeIn(fate_chips(), shift=UP * 0.1, lag_ratio=0.15), run_time=0.8)
        self.finish()


def roles_state(scene, with_tube=False):
    hdr = lab("the graft did", GREY, 28).move_to([-4.4, 3.2, 0])
    r = role_list(3)
    noto = cell(NOTO_C[0], NOTO_C[1], CREAM, 0.6, donor=True)
    l_n = lab("notochord", CREAM, 28).move_to([AXC, -1.95, 0])
    som_l, som_r = somite(SOM_L), somite(SOM_R)
    l_s1 = lab("somite", GREEN, 26).move_to([SOM_L[0], SOM_L[1] + 1.15, 0])
    l_s2 = lab("somite", GREEN, 26).move_to([SOM_R[0], SOM_R[1] + 1.15, 0])
    return hdr, r, noto, l_n, som_l, som_r, l_s1, l_s2, fate_chips()


class S20Role3(SpokenScene):
    def construct(self):
        hdr, r, noto, l_n, som_l, som_r, l_s1, l_s2, l_v = roles_state(self)
        nums3 = T("3", 40, GREY, weight=BOLD).move_to([-6.2, -2.4, 0])
        ghost = DashedVMobject(Circle(radius=1.2, stroke_color=GREY, stroke_width=3).move_to([TUBE_C[0], TUBE_C[1], 0]), num_dashes=22)
        self.add(hdr, r[0], r[1], nums3, noto, l_n, som_l, som_r, l_s1, l_s2, l_v, ghost)
        self.at("induced host ectoderm")
        self.play(FadeOut(nums3), FadeIn(r[2]), run_time=0.4)
        plate = [cell(AXC + (i - 3) * 0.85, 3.0, BLUE, 0.26, dots=True) for i in range(7)]
        self.play(FadeIn(VGroup(*plate), lag_ratio=0.08), run_time=0.7)
        cp = ring_pos(7, TUBE_C, 0.95)
        op = open_pos(7, TUBE_C, 0.95)
        self.at("to become a neural tube")
        self.play(*[paint(c, PURPLE) for c in plate], FadeOut(ghost), run_time=0.4)
        self.play(*[plate[i].animate.move_to(op[i]) for i in range(7)], run_time=0.8)
        self.play(*[plate[i].animate.move_to(cp[i]) for i in range(7)], run_time=0.6)
        left, right = AXC - 3.5, AXC + 3.5
        l_org = T("organizer", 52, CREAM, font=TITLE_FONT, weight=BOLD)
        self.at("the name organizer")
        l_org.move_to([AXC, 3.45, 0])
        top = VGroup(Line([left, 3.0, 0], [right, 3.0, 0], color=CREAM, stroke_width=4),
                     Line([left, 3.0, 0], [left, 2.75, 0], color=CREAM, stroke_width=4),
                     Line([right, 3.0, 0], [right, 2.75, 0], color=CREAM, stroke_width=4))
        self.play(Create(top), FadeIn(l_org, shift=UP * 0.1), run_time=0.8)
        self.finish()


# ------------------------------------------------------------------ 21  where
class S21Where(SpokenScene):
    def construct(self):
        c, rx, ry = [0, 0.1], 6.3, 3.5
        body = Ellipse(width=2 * rx, height=2 * ry, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.14).move_to([c[0], c[1], 0])
        gx, gy = 2.3, -1.2
        graft = RoundedRectangle(corner_radius=0.1, width=0.8, height=0.5, stroke_color=CREAM, stroke_width=3,
                                 fill_color=CREAM, fill_opacity=0.85).move_to([gx, gy, 0])
        l_g = lab("graft", CREAM, 28).move_to([gx, gy - 0.6, 0])
        ax1 = RoundedRectangle(corner_radius=0.3, width=8.6, height=0.6, stroke_color=PURPLE, stroke_width=3,
                               fill_color=PURPLE, fill_opacity=0.6).move_to([0, 1.5, 0])
        l_1 = lab("the host's own axis, along its back", PURPLE_T, 30).move_to([0, 2.4, 0])
        self.play(FadeIn(body), FadeIn(graft), FadeIn(l_g), GrowFromEdge(ax1, LEFT), FadeIn(l_1), run_time=0.8)
        ax2 = RoundedRectangle(corner_radius=0.25, width=5.0, height=0.5, stroke_color=PURPLE, stroke_width=3,
                               fill_color=PURPLE, fill_opacity=0.6).rotate(0.12).move_to([gx - 0.6, gy + 0.25, 0])
        l_2 = lab("second axis, at the graft", PURPLE_T, 30).move_to([0.8, -2.55, 0])
        self.at("second axis")
        self.play(FadeOut(l_g), run_time=0.2)
        self.play(GrowFromEdge(ax2, LEFT), FadeIn(l_2), run_time=0.9)
        self.at("not along")
        self.play(Indicate(ax1, color=YELLOW, scale_factor=1.04), run_time=0.9)
        self.finish()


# ------------------------------------------------------------------ 22  instruction
PL, PR = [-3.5, 0.5], [3.5, 0.5]


def panel(c):
    return Ellipse(width=6.0, height=4.2, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.12).move_to([c[0], c[1], 0])


def src(x, y):
    return Circle(radius=0.25, stroke_color=CREAM, stroke_width=3, fill_color=CREAM, fill_opacity=0.85).move_to([x, y, 0])


def pat(x, y, ang=0.0):
    return RoundedRectangle(corner_radius=0.2, width=2.4, height=0.42, stroke_color=PURPLE, stroke_width=3,
                            fill_color=PURPLE, fill_opacity=0.6).rotate(ang).move_to([x, y, 0])


class S22Instr(SpokenScene):
    def construct(self):
        pl, pr = panel(PL), panel(PR)
        s1, p1 = src(-4.4, 0.1), pat(-3.0, 0.1, 0.0)
        s2, p2 = src(2.3, -0.6), pat(3.7, -0.6, 0.0)
        self.play(FadeIn(pl), FadeIn(s1), FadeIn(p1), run_time=0.5)
        l_s = lab("source", CREAM, 26).move_to([-4.4, -0.7, 0])
        mv = arr([-0.3, 0.5, 0], [0.6, 0.5, 0], YELLOW)
        self.at("pattern followed")
        self.play(FadeIn(l_s), FadeIn(pr), GrowArrow(mv), FadeIn(s2, shift=UP * 0.4), run_time=0.6)
        self.at("the source")
        self.play(FadeIn(p2, shift=RIGHT * 0.3), run_time=0.6)
        txt = T("the organizer decides where", 44, TEXT, font=TITLE_FONT).move_to([0, -2.6, 0])
        self.at("organizer decides")
        self.play(FadeIn(txt, shift=UP * 0.15), run_time=0.7)
        self.at("where neural tissue")
        self.play(Indicate(p1, color=YELLOW, scale_factor=1.15), Indicate(p2, color=YELLOW, scale_factor=1.15), run_time=0.9)
        self.finish()


HOW_Y, HOW_H = -0.75, 5.3


def how_frames():
    how = T("how?", 64, RED_T, font=TITLE_FONT, weight=BOLD).move_to([0, 3.0, 0])
    f1 = RoundedRectangle(corner_radius=0.2, width=6.6, height=HOW_H, stroke_color=GREY, stroke_width=3, fill_color=BG, fill_opacity=1).move_to([CX1, HOW_Y, 0])
    f2 = RoundedRectangle(corner_radius=0.2, width=6.6, height=HOW_H, stroke_color=GREY, stroke_width=3, fill_color=BG, fill_opacity=1).move_to([CX2, HOW_Y, 0])
    return how, f1, f2


def how_go(purple=False):
    t1 = T("a go signal", 36, YELLOW, weight=BOLD).move_to([CX1, 1.2, 0])
    c1 = cell(CX1 + 1.8, -1.2, PURPLE if purple else BLUE, 0.75)
    sg = chip("signal", YELLOW, 30).move_to([CX1 - 1.9, -1.2, 0])
    ag = arr([CX1 - 0.8, -1.2, 0], [CX1 + 0.85, -1.2, 0], YELLOW, w=7)
    return t1, c1, sg, ag


def how_brake(released=False):
    t2 = T("a released brake", 36, RED_T, weight=BOLD).move_to([CX2, 1.2, 0])
    c2 = cell(CX2, -2.0, PURPLE if released else BLUE, 0.75)
    stem = Line([CX2, -0.4, 0], [CX2, -1.2, 0], color=RED_T, stroke_width=8)
    bar = Line([CX2 - 1.0, -0.4, 0], [CX2 + 1.0, -0.4, 0], color=RED_T, stroke_width=12)
    bl = lab("brake", RED_T, 30).move_to([CX2 + 2.2, -0.4, 0])
    return t2, c2, VGroup(stem, bar, bl)


class S22bHow(SpokenScene):
    def construct(self):
        pl, pr = panel(PL), panel(PR)
        s1, p1 = src(-4.4, 0.1), pat(-3.0, 0.1)
        s2, p2 = src(2.3, -0.6), pat(3.7, -0.6)
        l_s = lab("source", CREAM, 26).move_to([-4.4, -0.7, 0])
        mv = arr([-0.3, 0.5, 0], [0.6, 0.5, 0], YELLOW)
        txt = T("the organizer decides where", 44, TEXT, font=TITLE_FONT).move_to([0, -2.6, 0])
        old = VGroup(pl, pr, s1, p1, s2, p2, l_s, mv, txt)
        self.add(old)
        how, f1, f2 = how_frames()
        self.at("does not yet say how", lead=0.0)
        self.play(FadeOut(old), FadeIn(how, scale=0.7), run_time=0.6)
        t1, c1, sg, ag = how_go()
        self.at("go signal")
        self.play(FadeIn(f1), FadeIn(t1), FadeIn(c1), FadeIn(sg), run_time=0.4)
        self.play(GrowArrow(ag), run_time=0.3)
        self.play(paint(c1, PURPLE), run_time=0.3)
        t2, c2, brake = how_brake()
        self.at("releasing")
        self.play(FadeIn(f2), FadeIn(t2), FadeIn(c2), FadeIn(brake), run_time=0.4)
        self.at("break")
        self.play(brake.animate.shift(UP * 0.9).rotate(0.4).set_opacity(0.0), run_time=0.7)
        self.play(paint(c2, PURPLE), run_time=0.4)
        self.finish()


class S22cBeat(NarratedScene):
    def construct(self):
        how, f1, f2 = how_frames()
        t1, c1, sg, ag = how_go(True)
        t2, c2, brake = how_brake(True)
        self.add(how, f1, f2, t1, c1, sg, ag, t2, c2)
        self.finish()


# ------------------------------------------------------------------ 23  competence
INC, RES = [-3.7, 0.0], [3.7, 0.0]


def tissue(c, fate, donor=False, r=0.75):
    return VGroup(*[cell(c[0] + dx, c[1] + dy, fate, r, donor) for dx in (-1.55, 0.0, 1.55) for dy in (-0.82, 0.82)])


class S23Comp(SpokenScene):
    def construct(self):
        inc = tissue(INC, CREAM, donor=True)
        res = tissue(RES, BLUE)
        l_i = lab("inducer", CREAM, 36).move_to([INC[0], -2.15, 0])
        a = arr([-1.35, 0.0, 0], [1.35, 0.0, 0], YELLOW, w=8, tip=0.32)
        self.add(inc, l_i, a, res)
        l_r = lab("responder", BLUE, 36).move_to([RES[0], -2.15, 0])
        self.at("responder must")
        self.play(FadeIn(l_r), Indicate(res, color=BLUE, scale_factor=1.05), run_time=0.7)
        self.at("able to answer")
        self.play(*[paint(c, PURPLE) for c in res], run_time=0.8)
        br = Brace(res, UP, color=BLUE, buff=0.15)
        comp = T("competence", 50, BLUE, font=TITLE_FONT, weight=BOLD).next_to(br, UP, buff=0.15)
        self.at("is competence")
        self.play(GrowFromCenter(br), FadeIn(comp, shift=UP * 0.1), run_time=0.7)
        self.finish()


# ------------------------------------------------------------------ 24-25  the series
Y0, HH = -1.9, 4.1
X0, X1 = -5.6, 5.9
SLOT = 2.0
CTRL_X = 4.7
GAP_X = 3.2


def bar_x(i):
    return X0 + SLOT * (i + 0.5) if i < 4 else CTRL_X


def chart_axes():
    d = {}
    d["base"] = Line([X0, Y0, 0], [X1, Y0, 0], color=GREY, stroke_width=3)
    d["yax"] = Line([X0, Y0, 0], [X0, Y0 + HH + 0.15, 0], color=GREY, stroke_width=3)
    d["ticks"] = VGroup(*[M(f"{v}", 26, GREYL).move_to([X0 - 0.5, Y0 + v / 100 * HH, 0]) for v in (0, 50, 100)])
    d["div"] = DashedLine([GAP_X, Y0 - 0.1, 0], [GAP_X, Y0 + HH + 0.1, 0], color=GREY, stroke_width=2.5)
    d["ctrl_head"] = lab("control", YELLOW, 32).move_to([CTRL_X, Y0 + HH + 0.35, 0])
    return d


def chart_bar(i, v, cat, ctrl=False):
    x = bar_x(i)
    h = max(0.04, v / 100 * HH)
    b = Rectangle(width=SLOT * 0.6, height=h, stroke_color=YELLOW if ctrl else PURPLE, stroke_width=4 if ctrl else 3,
                  fill_color=PURPLE, fill_opacity=0.6).move_to([x, Y0 + h / 2, 0])
    val = M(f"{v}%", 28, TEXT).move_to([x, Y0 + h + 0.32, 0])
    ct = lab(cat, YELLOW if ctrl else GREYL, 26, line_spacing=0.8).move_to([x, Y0 - 0.62, 0])
    return b, val, ct


CATS4 = ["early\ngastrula", "mid\ngastrula", "late\ngastrula", "early\nneurula"]
V4 = [90, 70, 15, 0]
CTRL_CAT = "late organizer,\nearly ectoderm"


def chart_titles():
    yl = lab("% of wrapped pieces forming neural tissue", GREYL, 26).move_to([X0 + 4.15, 3.55, 0])
    cap = lab("ectoderm of each age, wrapped around early organizer", TEXT, 30).move_to([X0 + 5.3, 3.0, 0])
    tag = lab("hypothetical numbers", GREYL, 26, slant=ITALIC).move_to([5.0, 3.55, 0])
    return yl, cap, tag


def wrap_icon():
    inner = Circle(radius=0.55, stroke_color=CREAM, stroke_width=3, fill_color=CREAM, fill_opacity=0.85)
    ring = Annulus(inner_radius=0.7, outer_radius=1.0, color=BLUE, fill_opacity=0.6, stroke_width=2)
    g = VGroup(ring, inner).move_to([CTRL_X, 0.4, 0])
    l1 = lab("early organizer", CREAM, 26).move_to([CTRL_X, -0.95, 0])
    l2 = lab("wrapped in ectoderm", BLUE, 26).move_to([CTRL_X, 1.85, 0])
    return VGroup(g, l1, l2)


def brace_text():
    br = Brace(Line([bar_x(0) - 0.8, Y0 - 0.9, 0], [bar_x(3) + 0.8, Y0 - 0.9, 0]), DOWN, color=BLUE, buff=0.05)
    br.stretch_to_fit_height(0.18)
    br.shift(UP * (Y0 - 1.13 - br.get_top()[1]))
    txt = T("the loss is in the responder", 34, BLUE, font=TITLE_FONT).next_to(br, DOWN, buff=0.06)
    return br, txt


class S24Series(SpokenScene):
    def construct(self):
        ax = chart_axes()
        yl, cap, tag = chart_titles()
        bars = [chart_bar(i, v, c) for i, (v, c) in enumerate(zip(V4, CATS4))]
        icon = wrap_icon()
        self.add(cap)  # readable from the opening, including before the wrap cue
        self.play(Create(ax["base"]), Create(ax["yax"]), FadeIn(ax["ticks"]), FadeIn(yl), FadeIn(tag), run_time=0.6)
        self.at("wrap", lead=0.0)
        self.play(FadeIn(icon, scale=0.8), FadeIn(VGroup(*[b[2] for b in bars]), lag_ratio=0.2), run_time=1.2)
        self.at("around early organizer")
        self.play(Indicate(icon[0][1], color=CREAM, scale_factor=1.07), run_time=0.5)
        self.at("the response falls")
        self.play(GrowFromEdge(bars[0][0], DOWN), FadeIn(bars[0][1]), run_time=0.5)
        self.play(GrowFromEdge(bars[1][0], DOWN), FadeIn(bars[1][1]), run_time=0.5)
        self.at("largely stops")
        self.play(GrowFromEdge(bars[2][0], DOWN), FadeIn(bars[2][1]), run_time=0.5)
        self.play(GrowFromEdge(bars[3][0], DOWN), FadeIn(bars[3][1]), run_time=0.5)
        self.finish()


def chart_s24_state(scene, with_icon=True):
    ax = chart_axes()
    yl, cap, tag = chart_titles()
    bars = [chart_bar(i, v, c) for i, (v, c) in enumerate(zip(V4, CATS4))]
    scene.add(ax["base"], ax["yax"], ax["ticks"], yl, cap, tag, *[m for b in bars for m in b])
    return ax, bars


class S25Ctrl(SpokenScene):
    def construct(self):
        ax, bars = chart_s24_state(self)
        icon = wrap_icon()
        self.add(icon)
        cb, cv, cc = chart_bar(4, 85, CTRL_CAT, ctrl=True)
        self.at("the control", lead=0.0)
        self.play(FadeOut(icon), Create(ax["div"]), FadeIn(ax["ctrl_head"]), run_time=0.7)
        self.at("late organizer")
        self.play(FadeIn(cc), run_time=0.5)
        self.at("young ectoderm")
        self.play(GrowFromEdge(cb, DOWN), FadeIn(cv), run_time=0.8)
        br, txt = brace_text()
        self.at("loss is in")
        self.play(GrowFromCenter(br), FadeIn(txt, shift=UP * 0.1), run_time=0.8)
        self.finish()


def chart_final(scene):
    ax, bars = chart_s24_state(scene)
    cb, cv, cc = chart_bar(4, 85, CTRL_CAT, ctrl=True)
    br, txt = brace_text()
    scene.add(ax["div"], ax["ctrl_head"], cb, cv, cc, br, txt)


class S26Beat(NarratedScene):
    def construct(self):
        chart_final(self)
        self.finish()


# ------------------------------------------------------------------ 27  the take
class S27Take(SpokenScene):
    def construct(self):
        cx = -3.3
        strip = [cell(cx + (i - 4) * 0.78, -1.0, BLUE, 0.36, dots=True) for i in range(9)]
        graft = [cell(cx + (i - 1) * 0.78, -2.1, CREAM, 0.36, donor=True) for i in range(3)]
        pos = ring_pos(9, [cx, 1.3], 1.2)
        tube = [cell(p[0], p[1], PURPLE, 0.36, dots=True) for p in pos]
        tube[0].base.set_fill(CREAM, 0.85)          # one pale graft cell on the floor: "most of the tube"
        for d in list(tube[0])[1:]:
            tube[0].remove(d)
        t1 = T("Host cells built\nthe second neural tube", 40, TEXT, font=TITLE_FONT, line_spacing=0.9).move_to([3.4, 1.4, 0])
        tag = lab("most of the tube: host cells", TEXT, 32).move_to([cx, 3.5, 0])
        t2 = T("at the graft", 40, YELLOW, font=TITLE_FONT).move_to([3.4, -0.3, 0])
        t3 = T("while they could\nstill answer", 40, BLUE, font=TITLE_FONT, line_spacing=0.9).move_to([3.4, -1.9, 0])
        g_lab = lab("graft", CREAM, 26).move_to([cx + 1.75, -2.1, 0])
        resp = lab("host ectoderm: able to answer", BLUE, 26).move_to([cx, -3.1, 0])
        self.play(FadeIn(VGroup(*strip), lag_ratio=0.03), FadeIn(VGroup(*graft)), FadeIn(g_lab), run_time=0.6)
        self.at("host cells built")
        self.play(FadeIn(t1, shift=UP * 0.1), LaggedStart(*[FadeIn(c, scale=0.4) for c in tube], lag_ratio=0.08), FadeIn(tag), run_time=1.2)
        self.at("at the graft")
        self.play(FadeIn(t2, shift=UP * 0.1), *[Indicate(c, color=YELLOW, scale_factor=1.25) for c in graft], run_time=0.8)
        self.at("while they", lead=0.35)
        self.play(FadeIn(t3, shift=UP * 0.1), FadeIn(resp), *[Indicate(c, color=BLUE, scale_factor=1.2) for c in strip], run_time=0.8)
        self.finish()


class S28End(EndCard):
    LINE = "Host cells built the second neural tube while they could still answer."

    def construct(self):
        a, b = T("Host cells built the second neural tube", 42, TEXT, font=TITLE_FONT), T("while they could still answer.", 42, TEXT, font=TITLE_FONT)
        line = VGroup(a, b).arrange(DOWN, buff=0.25)
        fit(line, max_w=11.5)
        sub = T("biochemistrypedia.com", size=22, color=TEAL)
        g = VGroup(line, sub).arrange(DOWN, buff=0.45)
        self.play(FadeIn(line, shift=UP * 0.15), run_time=self.beat(0.3))
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        self.finish()

