"""Chapter 3: Testing the Rule in Genes and Time  (What Makes the Human Brain Big)

COLOR MAP (one color per concept, same as chapters 1 and 2)
  BLUE   = progenitors (founders, basal progenitors); the units
  YELLOW = neurons, cortex, the neuron-making window
  GREEN  = doubling (symmetric) divisions, area
  PURPLE = adding (asymmetric) divisions, thickness
  PINK   = outer radial glia
  ORANGE = a gene or protein that is added, changed or removed
  RED    = removed / blocked / not shown / absent
  GREY   = board frame, species icons, de-emphasized
  LIGHT  = secondary labels (brighter grey)
  WHITE  = the transplanted human neuron (outline only differs from its mouse neighbours)
  GOLD   = the question mark and the final rule
All brains, cells, bars and curves are schematic.
"""

import numpy as np

from bp_style import *

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58BB8"
LIGHT = "#C3CAD6"


# ---------------------------------------------------------------- helpers
def left_at(m, x, y):
    return m.move_to([x + m.width / 2, y, 0])


def right_at(m, x, y):
    return m.move_to([x - m.width / 2, y, 0])


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.04, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def dot(x, y, color, r=0.16, fo=0.9):
    return Circle(radius=r, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=fo).move_to([x, y, 0])


def bar(x0, x1, y, color=YELLOW, h=0.5):
    return RoundedRectangle(corner_radius=0.1, width=x1 - x0, height=h, stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=0.35).move_to([(x0 + x1) / 2, y, 0])


def blob(a, b, eps, cx=0.0, cy=0.0, color=YELLOW):
    return ParametricFunction(
        lambda th: np.array([cx + a * (1 + eps * np.sin(11 * th)) * np.cos(th),
                             cy + b * (1 + eps * np.sin(11 * th)) * np.sin(th), 0]),
        t_range=[0, TAU, 0.02], stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.14)


def dashed_box(w, h, cx, cy, color=GREY):
    r = RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_color=color, stroke_width=3)
    return DashedVMobject(r, num_dashes=80).move_to([cx, cy, 0])


def outline_box(w, h, x, y, color=ORANGE, fo=0.0, sw=3):
    return RoundedRectangle(corner_radius=0.12, width=w, height=h, stroke_color=color, stroke_width=sw,
                            fill_color=color, fill_opacity=fo).move_to([x, y, 0])


def gcard(text, color, w, h, x, y, size=34, fo=0.3):
    return VGroup(outline_box(w, h, x, y, color, fo), T(text, size, TEXT).move_to([x, y, 0]))


# ---------------------------------------------------------------- icons (schematic cartoons, grey)
def _st(m, fo=0.25):
    return m.set_stroke(GREY, 2.5).set_fill(GREY, fo)


def mouse_icon():
    body = _st(Ellipse(width=0.75, height=0.44)).move_to([0.1, 0, 0])
    head = _st(Circle(radius=0.19)).move_to([-0.36, 0.0, 0])
    ear1 = _st(Circle(radius=0.1), 0.45).move_to([-0.3, 0.2, 0])
    ear2 = _st(Circle(radius=0.1), 0.45).move_to([-0.44, 0.18, 0])
    tail = ParametricFunction(lambda t: np.array([0.45 + 0.5 * t, 0.2 * np.sin(2.6 * t) * 1.0, 0]),
                              t_range=[0, 1], stroke_color=GREY, stroke_width=2.5)
    eye = Dot([-0.42, 0.04, 0], radius=0.025, color=TEXT)
    return VGroup(tail, body, head, ear1, ear2, eye)


def marmoset_icon():
    body = _st(Ellipse(width=0.46, height=0.4)).move_to([0.0, -0.1, 0])
    head = _st(Circle(radius=0.19)).move_to([-0.12, 0.26, 0])
    tuft1 = Line([-0.27, 0.38, 0], [-0.38, 0.5, 0], color=GREY, stroke_width=3)
    tuft2 = Line([0.03, 0.38, 0], [0.14, 0.5, 0], color=GREY, stroke_width=3)
    tail = ParametricFunction(lambda t: np.array([0.2 + 0.55 * t, -0.2 - 0.12 * np.sin(PI * t) + 0.5 * t * t, 0]),
                              t_range=[0, 1], stroke_color=GREY, stroke_width=2.5)
    eye = Dot([-0.17, 0.28, 0], radius=0.025, color=TEXT)
    return VGroup(tail, tuft1, tuft2, body, head, eye)


def organoid_icon():
    c1 = _st(Circle(radius=0.3)).move_to([-0.14, 0, 0])
    c2 = _st(Circle(radius=0.25)).move_to([0.17, 0.1, 0])
    c3 = _st(Circle(radius=0.22)).move_to([0.06, -0.2, 0])
    dots = VGroup(*[Dot(p, radius=0.04, color=TEXT) for p in ([-0.16, 0.05, 0], [0.18, 0.12, 0], [0.04, -0.2, 0])])
    return VGroup(c1, c2, c3, dots)


def slice_icon():
    dish = _st(Ellipse(width=1.05, height=0.28), 0.15).move_to([0, -0.2, 0])
    slab = _st(Ellipse(width=0.72, height=0.36), 0.4).move_to([0, -0.02, 0])
    dots = VGroup(*[Dot([x, -0.02, 0], radius=0.035, color=TEXT) for x in (-0.18, 0.0, 0.18)])
    return VGroup(dish, slab, dots)


# Ferret is left out of the strip and the board: the narration gives no ferret result (see fix_round notes).
ICONS = dict(mouse=mouse_icon, marmoset=marmoset_icon, organoid=organoid_icon, slice=slice_icon)
ICON_LABEL = dict(mouse="mouse", marmoset="marmoset", organoid="organoid", slice="cultured slice")


def strip():
    items, icons = VGroup(), {}
    for k in ["mouse", "marmoset", "organoid", "slice"]:
        ic = ICONS[k]().scale(1.15)
        lb = T(ICON_LABEL[k], 28, TEXT)
        g = VGroup(ic, lb).arrange(RIGHT, buff=0.14)
        icons[k] = ic
        items.add(g)
    items.arrange(RIGHT, buff=0.6)
    fit(items, max_w=12.6)
    items.move_to([0, 3.3, 0])
    return items, icons


# ---------------------------------------------------------------- the board
C1, C2, C3 = -5.2, -0.5, 4.3
SYS_ICON_X, SYS_TXT_X, EFF_X = -3.05, -2.4, 1.95
RY = dict(mouse=1.5, marm=0.78, slice=-0.12, nmouse=-1.1, norg=-2.05)
ESZ = 28


def board_frame():
    return RoundedRectangle(corner_radius=0.2, width=13.4, height=6.5, stroke_color=GREY, stroke_width=2.5
                            ).set_stroke(opacity=0.6).move_to([0, -0.45, 0])


def headers():
    h = VGroup(T("gene or change", 26, LIGHT).move_to([C1, 2.38, 0]),
               T("tested in", 26, LIGHT).move_to([C2, 2.38, 0]),
               T("effect on progenitors", 26, LIGHT).move_to([C3, 2.38, 0]))
    ul = Line([-6.5, 2.02, 0], [6.5, 2.02, 0], color=GREY, stroke_width=2).set_opacity(0.5)
    return VGroup(h, ul)


def scaffold():
    return VGroup(Line([-3.65, 2.02, 0], [-3.65, -2.55, 0], color=GREY, stroke_width=2).set_opacity(0.35),
                  Line([1.75, 2.02, 0], [1.75, -2.55, 0], color=GREY, stroke_width=2).set_opacity(0.35))


def sys_label(y, line1, gene=None, tag=None):
    parts = [T(line1, ESZ, TEXT)]
    if gene:
        parts.append(VGroup(T(gene, ESZ, ORANGE), T(tag, ESZ, RED)).arrange(RIGHT, buff=0.14))
    g = VGroup(*parts).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    return left_at(g, SYS_TXT_X, y)


def eff(y, lines):
    g = VGroup(*[T(t, ESZ, TEXT) for t in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
    return left_at(g, EFF_X, y)


ROWSPEC = dict(
    mouse=dict(icon="mouse", lab=lambda y: sys_label(y, "mouse embryo"),
               eff=lambda y: eff(y, ["more basal progenitors"])),
    marm=dict(icon="marmoset", lab=lambda y: sys_label(y, "marmoset fetus"),
              eff=lambda y: eff(y, ["larger neocortex"])),
    slice=dict(icon="slice", lab=lambda y: sys_label(y, "human fetal slice"),
               lab2=lambda y: sys_label(y, "human fetal slice", "ARHGAP11B", "blocked"),
               eff=lambda y: eff(y, ["fewer basal progenitors"])),
    nmouse=dict(icon="mouse", lab=lambda y: sys_label(y, "mouse cortex"),
                eff=lambda y: eff(y, ["progenitors kept dividing", "neurons delayed"])),
    norg=dict(icon="organoid", lab=lambda y: sys_label(y, "human organoid", "NOTCH2NL", "deleted"),
              eff=lambda y: eff(y, ["progenitors", "differentiate early"])),
)


def row_icon(key):
    ic = ICONS[ROWSPEC[key]["icon"]]().scale(0.85)
    return ic.move_to([SYS_ICON_X, RY[key], 0])


def row_static(key, full_label=True):
    sp = ROWSPEC[key]
    lab = sp.get("lab2", sp["lab"])(RY[key]) if full_label else sp["lab"](RY[key])
    return VGroup(row_icon(key), lab, sp["eff"](RY[key]))


def rows_static(keys):
    return VGroup(*[row_static(k) for k in keys])


def gene1():
    return chip("ARHGAP11B", ORANGE, 28).move_to([C1, 0.72, 0])


def gene2():
    c = chip("NOTCH2NL", ORANGE, 28).move_to([C1, -1.05, 0])
    sub = VGroup(T("raises Notch", 26, ORANGE), T("signalling", 26, ORANGE)).arrange(DOWN, buff=0.06).move_to([C1, -1.95, 0])
    return VGroup(c, sub)


def fly(scene, key, icons, rt=0.8, extra=()):
    """Copy a species icon from the strip into its row cell (extra animations play at the same time)."""
    ic = icons[ROWSPEC[key]["icon"]].copy()
    tgt = row_icon(key)
    scene.add(ic)
    scene.play(ic.animate.scale(0.85 / 1.15).move_to(tgt.get_center()), *extra, run_time=rt)
    return ic


GB_W, GB_X = 4.4, -1.6


def card3():
    A = VGroup(outline_box(8.0, 1.2, 0, 1.0, GREY, 0.25), left_at(T("ARHGAP11A", 40, TEXT), -3.7, 1.0))
    B = gcard("ARHGAP11B", ORANGE, GB_W, 1.2, GB_X, -0.7, 40, 0.3)
    cap = T("a partial copy of ARHGAP11A", 36, TEXT).move_to([0, -1.9, 0])
    return A, B, cap


# ---------------------------------------------------------------- scenes
class S00Title(TitleCard):
    LESSON = "What Makes the Human Brain Big"
    TITLE = "Testing the Rule in Genes and Time"

    def construct(self):
        brand = T("BIOCHEMISTRYPEDIA", size=20, color=TEAL, weight=BOLD).set_opacity(0.9)
        lesson = T(self.LESSON.upper(), size=24, color=LIGHT)
        title = T(self.TITLE, size=56, font=TITLE_FONT)
        fit(title, max_w=11.8)
        rule = Line(LEFT * 1.4, RIGHT * 1.4, color=GOLD, stroke_width=4)
        g = VGroup(brand, lesson, title, rule).arrange(DOWN, buff=0.36)
        self.add(g)  # complete from the first frame
        self.wait(self.beat(0.8))
        self.play(FadeOut(g), run_time=self.beat(0.2))
        self.finish()


GENES3 = ("gene A", "gene B", "gene C")


def human_chimp_diagram():
    xs = (-1.0, 1.6, 4.2)
    chips = VGroup(*[chip(n, ORANGE, 40).move_to([x, 1.65, 0]) for n, x in zip(GENES3, xs)])
    hl = right_at(T("human", 40, TEXT), -2.5, 1.65)
    ghosts = VGroup(*[DashedVMobject(RoundedRectangle(corner_radius=0.14, width=chips[0].width, height=chips[0].height,
                                                     stroke_color=RED, stroke_width=3), num_dashes=28).move_to([x, -0.95, 0])
                      for x in xs])
    cl = right_at(T("chimpanzee", 40, TEXT), -2.5, -0.95)
    return chips, hl, ghosts, cl


def gene_chips_col():
    return VGroup(*[chip(n, ORANGE, 36).move_to([C1, y, 0]) for n, y in zip(GENES3, (1.25, -0.2, -1.65))])


def qmarks():
    return VGroup(*[T("?", 56, GOLD, weight=BOLD).move_to([C3, y, 0]) for y in (1.25, -0.2, -1.65)])


def question(y=-3.05):
    return T("Do any of them change what progenitors do?", 36, GOLD).move_to([0, y, 0])


class S01Q(SpokenScene):
    def construct(self):
        frame = board_frame()
        chips, hl, ghosts, cl = human_chimp_diagram()
        human_positions = [c.copy() for c in chips]
        chips.arrange(RIGHT, buff=0.55).scale(1.25).move_to([0, 0.45, 0])
        q0 = question(-3.05)
        self.add(frame, q0)
        self.at("few genes")
        self.play(LaggedStart(*[GrowFromCenter(c) for c in chips], lag_ratio=0.3), run_time=0.9)
        self.at("in humans")
        self.play(*[Transform(c, target) for c, target in zip(chips, human_positions)],
                  FadeIn(hl), run_time=0.5)
        self.at("not in chimpanzees")
        self.play(LaggedStart(*[Create(g) for g in ghosts], lag_ratio=0.3), FadeIn(cl), run_time=0.9)
        hd = headers()
        gcol = gene_chips_col()
        self.at("do any of them")
        self.play(FadeOut(VGroup(hl, ghosts, cl)),
                  *[chips[i].animate.scale(36 / 40).move_to(gcol[i].get_center()) for i in range(3)],
                  q0.animate.move_to([0, -3.05, 0]), FadeIn(hd), run_time=0.8)
        self.at("change what")
        self.play(LaggedStart(*[FadeIn(q, scale=0.6) for q in qmarks()], lag_ratio=0.25), run_time=0.5)
        self.finish()


class S02System(SpokenScene):
    def construct(self):
        frame, hd, gcol, qm, qu = board_frame(), headers(), gene_chips_col(), qmarks(), question()
        self.add(frame, hd, gcol, qm, qu)
        brain = blob(2.6, 1.8, 0.035, 2.6, 0.0)
        bl = T("developing human brain", 30, TEXT).move_to([2.6, -2.15, 0])
        gc = chip("gene removed", ORANGE, 44).move_to([-3.6, 0.0, 0])
        cross = Cross(gc, stroke_color=RED, stroke_width=9).scale(1.1)
        self.play(FadeOut(VGroup(gcol, qm, qu)), FadeIn(gc, shift=LEFT * 0.2), run_time=0.5)
        self.at("removed")
        self.play(Create(cross), run_time=0.4)
        self.at("developing human brain")
        self.play(FadeIn(brain), FadeIn(bl), run_time=0.7)
        self.at("so each was")
        st, icons = strip()
        self.play(VGroup(gc, cross, brain, bl).animate.set_opacity(0.3), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(g, shift=DOWN * 0.2) for g in st], lag_ratio=0.7), run_time=2.2)
        self.finish()


class S03Arhgap(SpokenScene):
    def construct(self):
        frame, hd = board_frame(), headers()
        st, icons = strip()
        self.add(frame, hd, st)
        A, B, cap = card3()
        # an outline picks out the part of A that was copied, then travels down and becomes B
        ghost = outline_box(GB_W, 1.2, GB_X, 1.0, ORANGE, 0.0, 4)
        self.at("first")
        self.play(FadeIn(A), run_time=0.4)
        self.play(Create(ghost), run_time=0.4)
        self.play(ghost.animate.move_to([GB_X, -0.7, 0]), run_time=0.6)
        self.play(FadeOut(ghost), FadeIn(B), run_time=0.3)
        self.play(FadeIn(cap), run_time=0.4)
        self.finish()


class S04Arhgap2(SpokenScene):
    def construct(self):
        frame, hd = board_frame(), headers()
        st, icons = strip()
        A, B, cap = card3()
        self.add(frame, hd, st, A, B, cap)
        sc, g1 = scaffold(), gene1()
        self.play(FadeOut(VGroup(A, cap)), Transform(B, g1), FadeIn(sc), st.animate.set_opacity(0.6), run_time=0.6)
        self.at("mouse")
        lab = ROWSPEC["mouse"]["lab"](RY["mouse"])
        fly(self, "mouse", icons, extra=(FadeIn(lab),))
        self.at("increased")
        self.play(FadeIn(ROWSPEC["mouse"]["eff"](RY["mouse"]), shift=RIGHT * 0.15), run_time=0.5)
        self.at("marmoset")
        lab = ROWSPEC["marm"]["lab"](RY["marm"])
        fly(self, "marm", icons, extra=(FadeIn(lab),))
        self.at("enlarged")
        self.play(FadeIn(ROWSPEC["marm"]["eff"](RY["marm"]), shift=RIGHT * 0.15), run_time=0.5)
        self.finish()


def base_state(keys, strip_op=0.6, gene_a=True, gene_b=False):
    frame, hd, sc = board_frame(), headers(), scaffold()
    st, icons = strip()
    st.set_opacity(strip_op)
    g = VGroup(frame, hd, sc, st)
    if keys:
        g.add(rows_static(keys))
    if "norg" in keys:
        g.add(Line([-3.5, -1.58, 0], [6.5, -1.58, 0], color=GREY, stroke_width=2).set_opacity(0.65))
    if gene_a:
        g.add(gene1())
    if gene_b:
        g.add(gene2())
    return g, icons


class S05Slices(SpokenScene):
    def construct(self):
        g, icons = base_state(["mouse", "marm"])
        self.add(g)
        lab = ROWSPEC["slice"]["lab2"](RY["slice"])
        self.at("cultured")
        fly(self, "slice", icons, extra=(FadeIn(lab[0]),))
        self.at("blocking")
        self.play(FadeIn(lab[1]), run_time=0.4)
        self.at("reduced")
        self.play(FadeIn(ROWSPEC["slice"]["eff"](RY["slice"]), shift=RIGHT * 0.15), run_time=0.5)
        self.finish()


class S06Notch(SpokenScene):
    def construct(self):
        g, icons = base_state(["mouse", "marm", "slice"])
        self.add(g)
        YC = -1.45
        N2 = gcard("NOTCH2", GREY, 2.9, 0.9, C1, YC, 32, 0.25)
        ghost = outline_box(1.6, 0.9, C1 - 0.6, YC, ORANGE, 0.0, 4)
        N2NL = gcard("NOTCH2NL", ORANGE, 2.9, 0.9, C1, YC, 32, 0.3)
        cap = T("derived from part of NOTCH2", 28, TEXT).move_to([0, -3.1, 0])
        up = arr([2.35, YC - 0.3, 0], [2.35, YC + 0.35, 0], ORANGE, 6)
        raises = VGroup(T("raises Notch", 28, ORANGE), T("signalling", 28, ORANGE)).arrange(DOWN, buff=0.06)
        left_at(raises, 2.7, YC)
        self.at("next")
        self.play(FadeIn(N2), run_time=0.5)
        self.play(Create(ghost), run_time=0.3)
        self.play(FadeOut(N2), FadeOut(ghost), run_time=0.3)
        self.play(FadeIn(N2NL), FadeIn(cap), run_time=0.4)
        self.at("raises notch signaling")
        self.play(GrowArrow(up), FadeIn(raises), run_time=0.7)
        self.at("in mouse cortex")
        g2 = gene2()
        self.play(FadeOut(VGroup(up, raises)), run_time=0.4)
        self.play(Transform(N2NL, g2[0]), run_time=0.5)
        self.play(FadeIn(g2[1]), run_time=0.2)
        lab = ROWSPEC["nmouse"]["lab"](RY["nmouse"])
        fly(self, "nmouse", icons, rt=0.5, extra=(FadeIn(lab),))
        ef = ROWSPEC["nmouse"]["eff"](RY["nmouse"])
        self.at("kept progenitors")
        self.play(FadeIn(ef[0], shift=RIGHT * 0.15), run_time=0.5)
        self.at("delayed neurons")
        self.play(FadeIn(ef[1], shift=RIGHT * 0.15), run_time=0.5)
        self.finish()


class S07Notch2(SpokenScene):
    def construct(self):
        g, icons = base_state(["mouse", "marm", "slice", "nmouse"], gene_b=True)
        self.add(g)
        lab = ROWSPEC["norg"]["lab"](RY["norg"])
        self.at("deleted")
        fly(self, "norg", icons, rt=0.7, extra=(FadeIn(lab),))
        self.at("made progenitors")
        self.play(FadeIn(ROWSPEC["norg"]["eff"](RY["norg"]), shift=RIGHT * 0.15), run_time=0.5)
        self.finish()


def full_board(strip_op=0.6):
    g, icons = base_state(["mouse", "marm", "slice", "nmouse", "norg"], strip_op=strip_op, gene_b=True)
    return g


class S08Fit(SpokenScene):
    def construct(self):
        self.add(full_board())
        hl = RoundedRectangle(corner_radius=0.15, width=4.95, height=4.5, stroke_color=TEXT, stroke_width=3
                              ).set_stroke(opacity=0.8).move_to([4.25, -0.25, 0])
        div = Line([-6.5, -2.62, 0], [6.5, -2.62, 0], color=GREY, stroke_width=2).set_opacity(0.5)
        n1 = left_at(T("consistent with more doubling", 32, GREEN), -6.3, -3.0)
        n2 = left_at(T("division modes not scored", 32, "#FF8A80", weight=BOLD), -6.3, -3.45)
        self.at("both are consistent")
        self.play(Create(hl), run_time=0.7)
        self.at("more doubling")
        self.play(FadeIn(div), FadeIn(n1, shift=UP * 0.1), run_time=0.6)
        self.at("did not score")
        self.play(FadeIn(n2, shift=UP * 0.1), run_time=0.6)
        self.at("which kind of division")
        self.play(Indicate(n2, color="#FF8A80", scale_factor=1.06), run_time=0.8)
        self.finish()


# ---- time scenes
TX0 = -3.3
WK = 0.75  # units per week (true 1:8 ratio between mouse and rhesus)
TYS = dict(mouse=1.5, rhesus=0.15, human=-1.2)


def time_bars():
    yy = TYS
    names = {k: right_at(T(n, 30, TEXT), -3.6, yy[k]) for k, n in
             [("mouse", "mouse"), ("rhesus", "rhesus monkey"), ("human", "human")]}
    b = dict(mouse=bar(TX0, TX0 + 1 * WK, yy["mouse"], YELLOW, 0.7),
             rhesus=bar(TX0, TX0 + 8 * WK, yy["rhesus"], YELLOW, 0.7))
    # human: no number given, so the bar fades out to the right, open ended
    hs = VGroup(bar(TX0, TX0 + 8 * WK + 1.3, yy["human"], YELLOW, 0.7))
    for i in range(6):
        x0 = TX0 + 8 * WK + 1.3 + i * 0.3
        hs.add(Rectangle(width=0.3, height=0.7, stroke_width=0, fill_color=YELLOW,
                         fill_opacity=0.32 - 0.05 * i).move_to([x0 + 0.15, yy["human"], 0]))
    b["human"] = hs
    lb = dict(mouse=left_at(T("about a week", 28, TEXT), TX0 + 0.75 + 0.3, yy["mouse"]),
              rhesus=T("roughly two months", 28, TEXT).move_to([TX0 + 4 * WK, yy["rhesus"], 0]),
              human=T("longer still", 28, TEXT).move_to([4.8, yy["human"], 0]))
    mouse_x = T("to scale: one eighth", 24, LIGHT)
    left_at(mouse_x, TX0 + 0.75 + 0.3, yy["mouse"] - 0.5)
    lb["mouse2"] = mouse_x
    ya = -2.3
    axis = arr([TX0, ya, 0], [6.4, ya, 0], GREY, 4)
    ticks = VGroup()
    for wk, txt in [(1, "1 wk"), (4, "1 month"), (8, "2 months"), (12, "3 months")]:
        x = TX0 + wk * WK
        ticks.add(Line([x, ya - 0.1, 0], [x, ya + 0.1, 0], color=GREY, stroke_width=3),
                  T(txt, 26, LIGHT).move_to([x, ya - 0.42, 0]))
    axl = T("time", 26, LIGHT).move_to([6.0, ya + 0.42, 0])
    title = left_at(T("neurogenesis, timed", 30, LIGHT), -6.4, 2.45)
    return names, b, lb, axis, ticks, axl, title


class S09Time(SpokenScene):
    def construct(self):
        full = full_board()
        self.add(full)
        names, b, lb, axis, ticks, axl, title = time_bars()
        self.play(FadeOut(full[1:]), run_time=0.5)
        self.play(FadeIn(title), Create(axis), FadeIn(ticks), FadeIn(axl), FadeIn(names["mouse"]),
                  GrowFromEdge(b["mouse"], LEFT), FadeIn(names["rhesus"]),
                  GrowFromEdge(b["rhesus"], LEFT), run_time=0.8)
        self.at("neurogenesis takes")
        self.wait(0.1)
        self.at("week in the mouse")
        self.play(FadeIn(lb["mouse"]), FadeIn(lb["mouse2"]), run_time=0.4)
        self.at("roughly two months")
        self.play(FadeIn(lb["rhesus"]), run_time=0.4)
        self.at("and longer in humans")
        self.play(FadeIn(names["human"]), GrowFromEdge(b["human"][0], LEFT), FadeIn(b["human"][1:]), FadeIn(lb["human"]), run_time=0.8)
        self.finish()


def time_static():
    names, b, lb, axis, ticks, axl, title = time_bars()
    return VGroup(board_frame(), title, axis, ticks, axl, *names.values(), *b.values(), *lb.values())


# lineage panels: time runs left to right, shared by both lineages
def XK(k):
    return -5.0 + 2.5 * k


YS_SP, YS_N = 1.45, 0.9
YT = -1.95


def time_top():
    orig = Rectangle(width=5.0, height=0.45, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW,
                     fill_opacity=0.45).move_to([-2.5, 3.2, 0])
    extn = Rectangle(width=5.0, height=0.45, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW,
                     fill_opacity=0.18).move_to([2.5, 3.2, 0])
    lo = T("original time", 26, TEXT).move_to(orig)
    le = T("twice the time", 28, TEXT).move_to(extn)
    ticks = VGroup(*[Line([XK(k), 2.95, 0], [XK(k), 2.7, 0], color=YELLOW, stroke_width=3) for k in range(5)])
    return orig, extn, lo, le, ticks


def steady_parts():
    spine1 = Line([XK(0), YS_SP, 0], [XK(2), YS_SP, 0], color=BLUE, stroke_width=5)
    spine2 = Line([XK(2), YS_SP, 0], [XK(4), YS_SP, 0], color=BLUE, stroke_width=5)
    top = dot(XK(0), YS_SP, BLUE, 0.18)
    neurons = [VGroup(Line([XK(k), YS_SP, 0], [XK(k), YS_N + 0.18, 0], color=PURPLE, stroke_width=4),
                      dot(XK(k), YS_N, YELLOW, 0.17)) for k in range(1, 5)]
    return spine1, spine2, top, neurons


def tree():
    ys = {4: [YT + (i - 7.5) * 0.17 for i in range(16)]}
    for j in (3, 2, 1, 0):
        ys[j] = [(ys[j + 1][2 * i] + ys[j + 1][2 * i + 1]) / 2 for i in range(2 ** j)]
    levels = []
    for j in range(5):
        lv = VGroup()
        ln = VGroup()
        for i, y in enumerate(ys[j]):
            lv.add(dot(XK(j), y, BLUE, 0.17 - 0.025 * j))
            if j > 0:
                ln.add(Line([XK(j - 1), ys[j - 1][i // 2], 0], [XK(j), y, 0], color=GREEN, stroke_width=2.5))
        levels.append(VGroup(ln, lv))
    return levels


class S10Time2(SpokenScene):
    def construct(self):
        ts = time_static()
        self.add(ts)
        orig, extn, lo, le, tk = time_top()
        spine1, spine2, top, neurons = steady_parts()
        levels = tree()
        st_title = left_at(T("steady pool", 30, PURPLE), -5.0, 1.95)
        gr_title = left_at(T("growing pool", 30, GREEN), -5.0, -0.7)
        rl = [T(f"round {k + 1}", 26, LIGHT).move_to([(XK(k) + XK(k + 1)) / 2, 2.5, 0]) for k in range(4)]
        self.play(FadeOut(ts), run_time=0.4)
        self.play(FadeIn(orig), FadeIn(lo), FadeIn(tk[:3]), Create(spine1), FadeIn(top), FadeIn(rl[0]), FadeIn(rl[1]),
                  run_time=0.7)
        self.at("more rounds")
        self.play(FadeIn(extn), FadeIn(le), FadeIn(tk[3:]), Create(spine2), FadeIn(rl[2]), FadeIn(rl[3]), run_time=0.8)
        self.at("cell cycles")
        clocks = VGroup()
        for k in range(4):
            c = Arc(radius=0.75, start_angle=PI / 2, angle=-1.75 * PI, color=LIGHT, stroke_width=5)
            c.add_tip(tip_length=0.25)
            c.move_to([(XK(k) + XK(k + 1)) / 2, -0.9, 0])
            clocks.add(c)
        cyc = T("same cycle length", 34, LIGHT).move_to([0, -2.2, 0])
        brace = clocks
        self.play(FadeIn(cyc), LaggedStart(*[Create(c) for c in clocks], lag_ratio=0.3), run_time=0.9)
        self.at("a steady pool")
        self.play(FadeOut(cyc), FadeOut(brace), FadeIn(st_title), run_time=0.4)
        self.at("adds in step")
        self.play(LaggedStart(*[FadeIn(n, shift=DOWN * 0.1) for n in neurons], lag_ratio=0.6), run_time=1.3)
        lab1 = left_at(T("twice the time, twice the neurons", 28, TEXT), -5.0, -0.05)
        n2 = T("2", 32, TEXT, weight=BOLD).move_to([XK(2), 0.45, 0])
        n4 = T("4", 32, TEXT, weight=BOLD).move_to([XK(4), 0.45, 0])
        self.play(FadeIn(lab1), FadeIn(n2), FadeIn(n4), run_time=0.3)
        self.at("a growing pool")
        self.play(FadeIn(gr_title), FadeIn(levels[0]),
                  LaggedStart(*[FadeIn(l) for l in levels[1:]], lag_ratio=0.35), run_time=0.8)
        self.at("compounds")
        lab2 = T("gain compounds", 28, TEXT).move_to([-3.0, -3.35, 0])
        m4 = T("4", 30, TEXT, weight=BOLD).move_to([XK(2), -3.35, 0])
        m16 = T("16", 30, TEXT, weight=BOLD).move_to([XK(4), -3.35, 0])
        self.play(FadeIn(lab2), FadeIn(m4), FadeIn(m16), levels[4][1].animate.set_color(GREEN), run_time=0.6)
        self.finish()


# ---- maturation box
def recap():
    r = RoundedRectangle(corner_radius=0.15, width=7.8, height=0.62, stroke_color=GOLD, stroke_width=3,
                         fill_color=GOLD, fill_opacity=0.1).move_to([0, 3.4, 0])
    t = T("the rule: multiply, don't add", 28, GOLD).move_to(r)
    return VGroup(r, t)


def mat_box(title="outside the rule: maturation"):
    box = dashed_box(13.4, 6.4, 0, -0.35)
    t = T(title, 28, TEXT).move_to([0, 2.5, 0])
    return VGroup(box, t)


AGE = lambda a: -4.6 + 0.34 * a
DY = 0.95  # dendrite height


def dendrite(y=DY, L=0.75, r=0.14, soma_r=0.45, sw=4):
    soma = dot(-5.9, y, YELLOW, soma_r, 0.35)
    line = Line([-5.9 + soma_r, y, 0], [6.3, y, 0], color=YELLOW, stroke_width=sw * 2).set_opacity(0.85)
    spines = VGroup()
    for i in range(17):
        x = -4.6 + i * 0.66
        s_ = 1 if i % 2 == 0 else -1
        spines.add(Line([x, y, 0], [x, y + s_ * L, 0], color=YELLOW, stroke_width=sw),
                   dot(x, y + s_ * (L + r), YELLOW, r))
    return soma, line, spines


def dens(a):
    """Schematic spine density (not data): early-childhood peak, slow fall, adult level only after about 28."""
    if a < 3:
        return 0.6 + 1.6 * np.sin(PI / 2 * a / 3)
    if a < 29:
        return 1 + 1.2 * 0.5 * (1 + np.cos(PI * (a - 3) / 26))
    return 1.0


YA = -3.0


def PY(d):
    return YA + 0.9 * d


def spine_plot():
    axis = VGroup(Line([AGE(0), YA, 0], [AGE(30) + 0.3, YA, 0], color=GREY, stroke_width=3),
                  Line([AGE(0), YA, 0], [AGE(0), -0.9, 0], color=GREY, stroke_width=3))
    ylab = T("spine density", 26, LIGHT).rotate(PI / 2).move_to([AGE(0) - 0.4, -1.95, 0])
    ticks = VGroup(*[T(str(a), 26, LIGHT).move_to([AGE(a), YA - 0.33, 0]) for a in (0, 10, 20)],
                   T("30 years", 26, LIGHT).move_to([AGE(30) + 0.1, YA - 0.33, 0]))
    adult = DashedVMobject(Line([AGE(0), PY(1), 0], [AGE(30), PY(1), 0], color=LIGHT, stroke_width=3), num_dashes=40)
    adult_l = T("adult level", 26, LIGHT).move_to([AGE(25), PY(1) - 0.35, 0])
    curve = ParametricFunction(lambda a: np.array([AGE(a), PY(dens(a)), 0]), t_range=[0, 30, 0.1],
                               stroke_color=YELLOW, stroke_width=6)
    band = Rectangle(width=AGE(30) - AGE(20), height=YA * -1 - 0.9, stroke_width=0, fill_color=GOLD, fill_opacity=0.16
                     ).move_to([(AGE(20) + AGE(30)) / 2, (YA - 0.9) / 2 - 0.0, 0])
    band.stretch_to_fit_height(2.1).move_to([(AGE(20) + AGE(30)) / 2, YA + 1.05, 0])
    bl = T("third decade", 26, GOLD).move_to([(AGE(20) + AGE(30)) / 2, -0.7, 0])
    return axis, ylab, ticks, adult, adult_l, curve, band, bl


def mat_labels():
    lab = VGroup(T("human", 28, TEXT), T("neuron", 28, TEXT)).arrange(DOWN, buff=0.14)
    left_at(lab, -6.5, 0.1)
    pf = left_at(T("prefrontal cortex", 30, TEXT), -4.2, -0.7)
    sch = left_at(T("schematic", 24, LIGHT), -0.7, -0.7)
    return lab, pf, sch


class S11Mature(SpokenScene):
    def construct(self):
        rc, mb = recap(), mat_box()
        soma, line, spines = dendrite(-0.15, 1.45, 0.18, 0.6, 6)
        small = VGroup(*dendrite())
        lab, pf, sch = mat_labels()
        lab_big = lab.copy().move_to([-6.0, -1.1, 0])
        left_at(lab_big, -6.5, -1.1)
        axis, ylab, ticks, adult, adult_l, curve, band, bl = spine_plot()
        self.add(mb, rc, soma, line, lab_big)
        self.at("human neurons mature")
        self.at("spine density")
        self.play(LaggedStart(*[GrowFromPoint(s, s.get_start() if isinstance(s, Line) else s.get_center())
                                for s in spines], lag_ratio=0.04), run_time=1.0)
        self.at("prefrontal cortex")
        dend_big = VGroup(soma, line, spines)
        self.play(Transform(dend_big, small), Transform(lab_big, lab), FadeIn(pf), FadeIn(sch), Create(axis),
                  FadeIn(ylab), FadeIn(ticks), run_time=1.0)
        self.at("stays")
        self.play(Create(curve), run_time=1.2)
        self.at("adult levels")
        self.play(Create(adult), FadeIn(adult_l), run_time=0.6)
        self.at("third decade")
        self.play(FadeIn(band), FadeIn(bl), run_time=0.6)
        self.finish()


def mat_static(with_dend=True):
    g = VGroup(recap(), mat_box())
    if with_dend:
        soma, line, spines = dendrite()
        g.add(soma, line, spines)
    return g


class S12Srgap(SpokenScene):
    def construct(self):
        g = mat_static()
        axis, ylab, ticks, adult, adult_l, curve, band, bl = spine_plot()
        lab, pf, sch = mat_labels()
        self.add(g, lab, pf, sch, axis, ylab, ticks, adult, adult_l, curve, band, bl)
        self.play(FadeOut(VGroup(g[2:], lab, pf, sch, axis, ylab, ticks, adult, adult_l, curve, band, bl)), run_time=0.6)
        ch = chip("SRGAP2C", ORANGE, 40).move_to([-4.2, 1.3, 0])
        head = left_at(T("spine maturation in mouse cortical neurons", 30, TEXT), -2.0, 1.3)
        b1 = bar(-2.2, 0.2, 0.0, YELLOW, 0.9)
        b2 = bar(-2.2, 5.4, -1.6, YELLOW, 0.9)
        n1 = right_at(T("mouse neuron", 30, TEXT), -2.5, 0.0)
        n2 = right_at(VGroup(T("mouse neuron", 30, TEXT), VGroup(T("with", 30, TEXT), T("SRGAP2C", 30, ORANGE)).arrange(RIGHT, buff=0.14)).arrange(DOWN, aligned_edge=RIGHT, buff=0.08), -2.5, -1.6)
        slow = T("slower", 36, YELLOW).move_to([1.6, -1.6, 0])
        self.play(FadeIn(ch, shift=RIGHT * 0.2), FadeIn(head), run_time=0.6)
        self.play(FadeIn(n1), GrowFromEdge(b1, LEFT), run_time=0.6)
        self.at("slowed spine maturation")
        self.play(FadeIn(n2), GrowFromEdge(b2, LEFT), run_time=1.2)
        self.at("in mouse neurons")
        self.play(FadeIn(slow), run_time=0.4)
        self.finish()


# ---- transplant
def neuron_cell(x, y, s=1.0, op=0.4, color=YELLOW, sw=2.5):
    """Same shape for every neuron; only the colour differs for the human one."""
    soma = Circle(radius=0.22 * s, stroke_color=color, stroke_width=sw, fill_color=color,
                  fill_opacity=op).move_to([x, y, 0])
    arms = VGroup()
    for i in range(3):
        th = TAU * (i + 0.35) / 3
        L = 0.5 * s
        d = np.array([np.cos(th), np.sin(th), 0])
        a = np.array([x, y, 0]) + 0.22 * s * d
        b = np.array([x, y, 0]) + (0.22 * s + L) * d
        arms.add(Line(a, b, color=color, stroke_width=sw))
    arms.set_opacity(min(1.0, op + 0.3))
    return VGroup(arms, soma)


BY = 0.75  # cortex box centre
MOUSE_CELLS = [(-5.0, 0.9), (-3.4, -0.9), (-2.0, 0.9), (-1.7, -1.25), (2.1, 0.9), (2.0, -1.25), (3.7, -0.9), (5.1, 0.9)]


def tissue_mice(op=0.4):
    return VGroup(*[neuron_cell(x, BY + dy, 0.9, op) for x, dy in MOUSE_CELLS])


def tissue_box():
    return RoundedRectangle(corner_radius=0.2, width=12.4, height=4.5, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.06).move_to([0, BY, 0])


def tissue_label():
    return left_at(T("newborn mouse cortex", 28, LIGHT), -6.0, BY + 1.9)


def human_neuron(x, y):
    return neuron_cell(x, y, 0.9, 0.5, color=TEXT, sw=4)


def qpace(y=-2.3):
    return T("Whose pace do they keep?", 44, GOLD, font=TITLE_FONT).move_to([0, y, 0])


class S13Predict(SpokenScene):
    def construct(self):
        lead = T("Is the pace of maturation set by...", 36, LIGHT).move_to([0, 2.3, 0])
        body = chip("the body", GREY, 60).move_to([-3.9, 0.3, 0])
        cells = chip("the cells", YELLOW, 60).move_to([3.9, 0.3, 0])
        orr = T("or", 48, LIGHT).move_to([0, 0.3, 0])
        pred = T("Predict", 64, GOLD, font=TITLE_FONT).move_to([0, -1.9, 0])
        self.add(lead)
        self.at("by the body")
        self.play(FadeIn(body, shift=RIGHT * 0.2), run_time=0.5)
        self.at("or the cells")
        self.play(FadeIn(orr), FadeIn(cells, shift=LEFT * 0.2), run_time=0.5)
        rest = 2.6 - self.elapsed()
        if rest > 0:
            self.wait(rest)
        self.play(FadeIn(pred, scale=0.8), run_time=0.5)
        self.at("human neurons go")
        tb, mice, tl = tissue_box(), tissue_mice(), tissue_label()
        hx, hy = 0.2, -2.75
        hn = human_neuron(hx, hy)
        hl = left_at(T("human neuron", 30, TEXT), 1.5, hy)
        dbox = DashedVMobject(tb.copy().set_stroke(GREY, 3).set_fill(opacity=0), num_dashes=80)
        self.play(FadeOut(VGroup(lead, body, cells, orr, pred)), FadeIn(hn), FadeIn(hl), FadeIn(dbox), FadeIn(mice), FadeIn(tl), run_time=0.6)
        self.at("newborn mouse cortex")
        self.play(FadeOut(dbox), FadeIn(tb), run_time=0.6)
        self.play(hn.animate.move_to([0.2, BY, 0]), FadeOut(hl), run_time=0.9)
        self.at("whose pace")
        self.play(FadeIn(qpace(-2.05), shift=UP * 0.1), run_time=0.6)
        self.finish()


def predict_static(options=False):
    hn = human_neuron(0.2, BY)
    g = VGroup(tissue_box(), tissue_label(), tissue_mice(), hn, qpace(-2.05))
    if options:
        o1 = chip("mouse pace", YELLOW, 36).move_to([-3.2, -2.95, 0])
        o2 = chip("human pace", TEXT, 36).move_to([3.2, -2.95, 0])
        g.add(o1, o2)
    return g


class S14Pause(NarratedScene):
    def construct(self):
        base = predict_static()
        self.add(base)
        o1 = chip("mouse pace", YELLOW, 36).move_to([-3.2, -2.95, 0])
        o2 = chip("human pace", TEXT, 36).move_to([3.2, -2.95, 0])
        self.play(FadeIn(o1, shift=UP * 0.15), FadeIn(o2, shift=UP * 0.15), run_time=0.6)
        self.finish()


# s15-17: the answer
TX = -3.0
HY, MY = 0.65, -1.25
YAX = -2.65
MON = 1.1  # units per month


def tissue_strip():
    r = RoundedRectangle(corner_radius=0.15, width=10.0, height=1.65, stroke_color=GREY, stroke_width=3,
                         fill_color=GREY, fill_opacity=0.06).move_to([1.5, 2.85, 0])
    xs = [-1.2, 0.7, 2.6, 4.5, 6.2]
    mice = VGroup(*[neuron_cell(x, 2.85, 0.7, 0.4) for x in xs])
    hn = neuron_cell(-3.0, 2.85, 0.7, 0.5, color=TEXT, sw=4)
    lb = right_at(T("newborn mouse cortex", 26, LIGHT), 6.5, 2.18)
    hl = right_at(T("human neuron", 28, TEXT), -3.85, 3.2)
    ml = right_at(T("mouse neurons", 28, YELLOW), -3.85, 2.5)
    return VGroup(r, mice, hn, lb, hl, ml)


def answer_bars():
    names = VGroup(right_at(T("human neuron", 30, TEXT), TX - 0.25, HY),
                   right_at(T("mouse neurons", 30, YELLOW), TX - 0.25, MY))
    hb = VGroup(bar(TX, TX + 5.4, HY, TEXT, 1.05))
    for i in range(6):
        hb.add(Rectangle(width=0.3, height=1.05, stroke_width=0, fill_color=TEXT,
                         fill_opacity=0.32 - 0.05 * i).move_to([TX + 5.4 + i * 0.3 + 0.15, HY, 0]))
    mb = bar(TX, TX + 0.5, MY, YELLOW, 1.05)
    hl = T("many months", 32, TEXT).move_to([TX + 2.7, HY, 0])
    ml = left_at(T("weeks", 32, TEXT), TX + 0.75, MY)
    axis = arr([TX, YAX, 0], [6.3, YAX, 0], GREY, 4)
    ticks = VGroup()
    for x, txt in [(MON * m, f"{m} mo") for m in range(1, 7)]:
        ticks.add(Line([TX + x, YAX - 0.1, 0], [TX + x, YAX + 0.1, 0], color=GREY, stroke_width=3),
                  T(txt, 26, LIGHT).move_to([TX + x, YAX - 0.34, 0]))
    ticks.add(Line([TX + 0.28, YAX - 0.1, 0], [TX + 0.28, YAX + 0.1, 0], color=GREY, stroke_width=3),
              T("1 wk", 26, LIGHT).move_to([TX + 0.28, YAX + 0.38, 0]))
    axl = T("time", 26, LIGHT).move_to([5.9, YAX + 0.42, 0])
    head = left_at(T("spine and electrical maturation", 32, TEXT), -2.4, 1.55)
    return names, hb, mb, hl, ml, axis, ticks, axl, head


class S15Reveal(SpokenScene):
    def construct(self):
        names, hb, mb, hl, ml, axis, ticks, axl, head = answer_bars()
        ts = tissue_strip()
        tc = left_at(T("close to a human time course", 26, LIGHT), TX, HY - 0.78)
        self.add(ts, head, axis, ticks, axl)
        self.play(FadeIn(names[0]), GrowFromEdge(hb[0], LEFT), FadeIn(hb[1:]), run_time=1.5, rate_func=linear)
        self.play(FadeIn(hl), run_time=0.2)
        self.at("close to a human")
        self.play(FadeIn(tc), run_time=0.4)
        self.at("the mouse neurons around")
        self.play(FadeIn(names[1]), GrowFromEdge(mb, LEFT), run_time=0.5)
        self.at("long since matured")
        self.play(FadeIn(ml), run_time=0.4)
        self.finish()


def answer_static():
    names, hb, mb, hl, ml, axis, ticks, axl, head = answer_bars()
    tc = left_at(T("close to a human time course", 26, LIGHT), TX, HY - 0.78)
    return VGroup(tissue_strip(), head, axis, ticks, axl, *names, hb, mb, hl, ml, tc)


def tl_arrow():
    return arr([-3.0, 2.35, 0], [-3.0, HY + 0.5, 0], TEXT, 5)


class S16Reveal2(SpokenScene):
    def construct(self):
        self.add(answer_static())
        link = tl_arrow()
        cap = T("the timing travels with the cells", 36, TEXT, font=TITLE_FONT).move_to([0, -3.5, 0])
        self.at("at least part")
        self.play(GrowArrow(link), run_time=0.6)
        self.at("travels with")
        self.play(FadeIn(cap, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S17Beat(NarratedScene):
    def construct(self):
        self.add(answer_static())
        link = tl_arrow()
        cap = T("the timing travels with the cells", 36, TEXT, font=TITLE_FONT).move_to([0, -3.5, 0])
        self.add(link, cap)
        qual = T("at least part of", 28, GOLD, font=TITLE_FONT).move_to([-4.5, -3.0, 0])
        self.play(FadeIn(qual, shift=DOWN * 0.1), run_time=0.6)
        self.finish()


def panel(x, y, w, h):
    return RoundedRectangle(corner_radius=0.15, width=w, height=h, stroke_color=GREY, stroke_width=2.5
                            ).set_stroke(opacity=0.6).move_to([x, y, 0])


class S18Outside(SpokenScene):
    def construct(self):
        rc, mb = recap(), mat_box()
        self.add(mb, rc)
        pl, pr = panel(-3.3, -0.55, 6.1, 4.6), panel(3.3, -0.55, 6.1, 4.6)
        self.play(Create(pl), Create(pr), run_time=0.6)
        DYL = -0.35
        dl = Line([-6.0, DYL, 0], [-0.7, DYL, 0], color=YELLOW, stroke_width=9).set_opacity(0.85)
        sp = VGroup()
        for i in range(8):
            x = -5.5 + i * 0.7
            s = 1 if i % 2 == 0 else -1
            sp.add(Line([x, DYL, 0], [x, DYL + s * 0.8, 0], color=YELLOW, stroke_width=5),
                   dot(x, DYL + s * 0.95, YELLOW, 0.17))
        cl = T("shaped by maturation", 28, LIGHT).move_to([-3.3, -2.05, 0])
        hd1 = T("connections", 38, TEXT).move_to([-3.3, 1.35, 0])
        dots = VGroup(*[dot(1.4 + 1.3 * (i % 4), 0.5 - 1.15 * (i // 4), YELLOW, 0.4, 0.6) for i in range(8)])
        hd2 = T("neuron number", 38, TEXT).move_to([3.3, 1.35, 0])
        nc = T("not changed by maturation", 28, LIGHT).move_to([3.3, -2.05, 0])
        eq = T("=", 54, GOLD, weight=BOLD).move_to([0, -0.2, 0])
        self.at("maturation shapes")
        self.play(FadeIn(hd1), Create(dl), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(s_) for s_ in sp], lag_ratio=0.1), run_time=1.0)
        self.at("not neuron number")
        self.play(FadeIn(hd2), LaggedStart(*[FadeIn(d_, scale=0.6) for d_ in dots], lag_ratio=0.08), run_time=0.8)
        self.play(FadeIn(nc), run_time=0.4)
        self.at("outside the rule")
        self.play(Indicate(mb[0], color=TEXT, scale_factor=1.0), run_time=0.8)
        self.finish()


class S19None(SpokenScene):
    def construct(self):
        board = full_board(0.6)
        self.add(board)
        shade = Rectangle(width=14.3, height=8.1, stroke_width=0, fill_color=BG, fill_opacity=0.995)
        t = Text("no test shows that one gene\nmade the human cortex", font=FONT, font_size=38, color=TEXT,
                 line_spacing=0.9, t2c={"one gene": ORANGE})
        back = RoundedRectangle(corner_radius=0.2, width=t.width + 0.8, height=t.height + 0.35, stroke_color=RED,
                                stroke_width=3, fill_color=BG, fill_opacity=1.0).move_to([0, -3.0, 0])
        t.move_to(back)
        self.add(shade, back, t)
        self.finish()


class S20Take(SpokenScene):
    def construct(self):
        rule = T("Multiply, don't add", 64, GOLD, font=TITLE_FONT).move_to([0, 0.7, 0])
        lead = T("a leading explanation for our large cortex", 38, TEXT).move_to([0, -0.4, 0])
        SX = (-4.4, 0, 4.4)
        slots = VGroup(*[VGroup(DashedVMobject(RoundedRectangle(corner_radius=0.14, width=3.9, height=1.2,
                                                                 stroke_color=GOLD, stroke_width=3), num_dashes=40),
                                T("?", 52, GOLD, weight=BOLD)).move_to([x, -0.9, 0]) for x in SX])
        c1 = chip("founders", BLUE, 38).move_to([SX[0], -0.9, 0])
        c2 = chip("outer radial glia", PINK, 38).move_to([SX[1], -0.9, 0])
        c3 = chip("a longer clock", YELLOW, 38).move_to([SX[2], -0.9, 0])
        op = T("still open", 44, GOLD).move_to([0, -2.6, 0])
        self.at("multiply")
        self.play(FadeIn(rule, shift=UP * 0.15), run_time=0.8)
        self.at("a leading explanation")
        self.play(FadeIn(lead), run_time=0.6)
        self.at("how much came")
        self.play(rule.animate.move_to([0, 2.7, 0]), lead.animate.move_to([0, 1.65, 0]),
                  LaggedStart(*[FadeIn(s_, scale=0.8) for s_ in slots], lag_ratio=0.2), run_time=0.9)
        self.at("founders")
        self.play(FadeOut(slots[0]), run_time=0.15)
        self.play(FadeIn(c1), run_time=0.25)
        self.at("outer radial glia")
        self.play(FadeOut(slots[1]), run_time=0.15)
        self.play(FadeIn(c2), run_time=0.25)
        self.at("a longer clock")
        self.play(FadeOut(slots[2]), run_time=0.15)
        self.play(FadeIn(c3), run_time=0.25)
        self.at("still open")
        self.play(FadeIn(op, shift=UP * 0.1), run_time=0.5)
        self.finish()


class S21End(EndCard):
    LINE = "Multiply, don't add: a leading explanation for our large cortex."

    def construct(self):
        l1 = T("Multiply, don't add:", size=64, font=TITLE_FONT)
        l2 = T("a leading explanation for our large cortex", size=44, font=TITLE_FONT)
        fit(l2, max_w=12.4)
        sub = T("biochemistrypedia.com", size=26, color=TEAL)
        g = VGroup(l1, l2, sub).arrange(DOWN, buff=0.5)
        self.play(FadeIn(l1, shift=UP * 0.15), run_time=self.beat(0.2))
        self.play(FadeIn(l2), FadeIn(sub), run_time=self.beat(0.15))
        self.finish()
