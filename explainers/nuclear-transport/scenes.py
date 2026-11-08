"""Nuclear transport: a gradient sets the direction  (Biochemistrypedia explainer, Cell Biology)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = cargo (the protein being moved)
  ORANGE = signal tag on the cargo (NLS, NES)
  BLUE   = import receptors (importin alpha, importin beta, transportin)
  PURPLE = export receptor (CRM1)
  GREEN  = Ran with GTP (on); also the nucleus tint where RanGTP is high
  RED    = Ran with GDP (off); also the crossed-out "push"
  TEAL   = the helper enzymes and carrier (RCC1, RanGAP1, NTF2)
  GREY   = membranes, pores, FG repeats, chromatin, place labels
"""
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"

PORES = (-2.3, 0.0, 2.3)      # y of the three pore channels (half-height 0.6)


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def stage(labels=True):
    """Nuclear envelope as two bars with three pores. Cytoplasm on the left, nucleus on the right."""
    g = VGroup()
    for (a, b) in [(-3.4, -3.0), (-1.6, -0.7), (0.7, 1.6), (3.0, 3.4)]:
        for x in (-0.45, 0.45):
            g.add(RoundedRectangle(corner_radius=0.06, width=0.16, height=b - a, stroke_color=GREY, stroke_width=2,
                                   fill_color=GREY, fill_opacity=0.45).move_to([x, (a + b) / 2, 0]))
    fg = VGroup()
    for yc in PORES:
        for sgn in (1, -1):
            for x in (-0.3, 0.0, 0.3):
                y0 = yc + sgn * 0.7
                y1 = yc + sgn * 0.44
                fg.add(Line([x, y0, 0], [x, y1, 0], color=GREY, stroke_width=3))
                fg.add(Dot([x, y1, 0], radius=0.05, color=GREY))
    g.add(fg)
    g.fg = fg
    lab = VGroup()
    if labels:
        lab.add(T("cytoplasm", 26, GREY).move_to([-4.4, -3.15, 0]))
        lab.add(T("nucleus", 26, GREY).move_to([4.4, -3.15, 0]))
    g.lab = lab
    return VGroup(g, lab)


def cargo(pos, tag=None):
    """Yellow circle; optional orange signal tag above its right shoulder. Returns VGroup(circle, [tag])."""
    c = Circle(radius=0.28, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.85)
    c.move_to(pos)
    g = VGroup(c)
    if tag:
        lab = T(tag, 22, BG, weight=BOLD)
        box = RoundedRectangle(corner_radius=0.08, width=lab.width + 0.2, height=0.34, stroke_width=0,
                               fill_color=ORANGE, fill_opacity=1)
        t = VGroup(box, lab.move_to(box)).move_to(np.array(pos) + np.array([0.0, 0.42, 0]))
        g.add(t)
    g.body = c
    return g


def blob(text, color, w, h=0.62, size=26, pos=(0, 0)):
    r = RoundedRectangle(corner_radius=0.22, width=w, height=h, stroke_color=color, stroke_width=3.5,
                         fill_color=color, fill_opacity=0.3)
    t = T(text, size, color).move_to(r)
    return VGroup(r, t).move_to([pos[0], pos[1], 0])


def bchip(text, color, size=24):
    c = chip(text, color, size=size)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def rdot(pos, color, r=0.13):
    return Dot([pos[0], pos[1], 0], radius=r, color=color)


def legend():
    g = VGroup()
    for i, (col, txt) in enumerate([(GREEN, "RanGTP"), (RED, "RanGDP")]):
        d = rdot((0, 0), col, 0.15)
        t = T(txt, 24, col)
        row = VGroup(d, t).arrange(RIGHT, buff=0.18)
        g.add(row)
    g.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([-5.15, 2.85, 0])
    return g


def _sample(rng, xr, yr, n, avoid, sep=0.62, pts=None):
    pts = list(pts or [])
    out = []
    guard = 0
    while len(out) < n and guard < 20000:
        guard += 1
        p = (rng.uniform(*xr), rng.uniform(*yr))
        if any(a[0] <= p[0] <= a[2] and a[1] <= p[1] <= a[3] for a in avoid):
            continue
        if any((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 < sep ** 2 for q in pts + out):
            continue
        out.append(p)
    return out


RECHARGED = (2.3, -2.3)      # where NTF2's Ran ends up


def gradient_points():
    """Fixed dot positions shared by scenes 4, 5 and 6. Keeps the action band |y|<1.05 and helper zones clear."""
    rng = random.Random(11)
    band = (-7, -1.5, 7, 1.5)
    legend_zone = (-6.4, 2.3, -4.0, 3.5)
    gap_zone = (-4.4, -1.7, -1.8, -0.8)         # RanGAP1 chip
    ntf2_zone = (-6.4, -2.95, 2.9, -1.75)         # NTF2 route
    chrom = (1.8, 1.8, 6.1, 3.3)                  # chromatin + RCC1
    pore_zone = (-1.0, -3.5, 1.0, 3.5)
    nuc = _sample(rng, (1.1, 6.0), (-2.8, 3.3), 11, [band, ntf2_zone, chrom, pore_zone], sep=0.8, pts=[RECHARGED])
    cyt_green = _sample(rng, (-6.0, -1.2), (-2.8, 3.3), 2, [band, legend_zone, gap_zone, ntf2_zone, pore_zone], sep=0.9)
    cyt_red = _sample(rng, (-6.0, -1.2), (-2.8, 3.3), 6, [band, legend_zone, gap_zone, ntf2_zone, pore_zone], sep=0.8,
                      pts=cyt_green)
    return nuc, cyt_green, cyt_red





NUC_G, CYT_G, CYT_R = gradient_points()


def tint():
    return Rectangle(width=5.75, height=6.9, stroke_width=0, fill_color=GREEN, fill_opacity=0.08).move_to([3.425, 0, 0])


def gradient_group():
    """Everything that shows the gradient: tint, green dots in the nucleus, a few green and many red outside."""
    tn = tint()
    ng = VGroup(*[rdot(p, GREEN) for p in NUC_G], rdot(RECHARGED, GREEN))
    cg = VGroup(*[rdot(p, GREEN) for p in CYT_G])
    cr = VGroup(*[rdot(p, RED) for p in CYT_R])
    return tn, ng, cg, cr


def pore_arrow_words(scene, text, color=GREY):
    t = T(text, 24, color)
    return t


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "The nuclear envelope and nuclear transport"
    TITLE = "A gradient sets the direction"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    """Proteins made in the cytoplasm, an unknown box in the nucleus, two-way traffic with a question."""

    def construct(self):
        st = stage()
        self.play(FadeIn(st), run_time=0.1)
        pts = [(-5.0, 1.6), (-4.0, 0.7), (-5.2, -0.3), (-3.9, -1.3), (-3.2, 1.9)]
        dots = VGroup(*[Circle(radius=0.28, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.85)
                        .move_to([x, y, 0]) for x, y in pts])
        lbl = T("proteins", 28, YELLOW).move_to([-4.3, -2.35, 0])
        self.at("Every protein")
        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.2), FadeIn(lbl), run_time=1.6)
        box = DashedVMobject(RoundedRectangle(corner_radius=0.3, width=3.0, height=3.2, stroke_color=GREY, stroke_width=4),
                             num_dashes=40).move_to([3.7, 0, 0])
        q = T("?", 90, GREY).move_to(box)
        a1 = arr([-2.4, 0.0, 0], [2.0, 0.0, 0], YELLOW)
        self.at("brought in")
        self.play(GrowArrow(a1), FadeIn(box), FadeIn(q), run_time=1.2)
        a2 = DoubleArrow([-2.4, 0.0, 0], [2.0, 0.0, 0], buff=0, color=GREY, stroke_width=5, tip_length=0.22)
        self.at("both directions")
        self.play(ReplacementTransform(a1, a2), run_time=0.8)
        self.at("run one way")
        a3 = arr([-2.4, 0.0, 0], [2.0, 0.0, 0], GREY)
        qc = T("?", 60, YELLOW, weight=BOLD).move_to([-1.6, 0.85, 0])
        self.play(ReplacementTransform(a2, a3), FadeIn(qc), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Passport(SpokenScene):
    """small things stroll across; a large cargo needs a signal, importin alpha and beta; it moves through the FG repeats."""

    def construct(self):
        st = stage()
        self.add(st)
        pore = st[0]
        lab_pore = T("nuclear pore complex", 24, GREY).move_to([-2.6, 1.35, 0])
        self.at("complexes")
        self.play(FadeIn(lab_pore), Indicate(VGroup(pore.fg), color=TEXT, scale_factor=1.0), run_time=1.0)
        smalls = VGroup(*[Dot([-3.5 - 0.5 * i, 0.15 * (-1) ** i, 0], radius=0.1, color=GREY) for i in range(4)])
        sl = T("small molecules", 24, GREY).move_to([-3.3, -0.85, 0])
        self.at("stroll across")
        self.add(smalls, sl)
        self.play(FadeOut(lab_pore), *[d.animate.shift(RIGHT * (7.0 + 0.2 * i)) for i, d in enumerate(smalls)], run_time=1.5, rate_func=linear)
        self.play(FadeOut(smalls), FadeOut(sl), run_time=0.3)
        cg = cargo([-4.6, 0, 0])
        cl = T("large protein", 24, YELLOW).move_to([-4.6, -0.85, 0])
        self.at("large protein")
        self.play(FadeIn(cg, shift=RIGHT * 0.3), FadeIn(cl), run_time=0.5)
        self.play(cg.animate.shift(RIGHT * 1.7), cl.animate.shift(RIGHT * 1.7), run_time=0.9)
        self.play(cg.animate.shift(LEFT * 0.35), cl.animate.shift(LEFT * 0.35), run_time=0.4)
        # the passport: orange tag
        tag_src = cargo([0, 0, 0], tag="NLS")[1]
        tag_src.move_to(cg.body.get_center() + np.array([0.0, 0.42, 0]))
        self.at("short signal")
        self.play(FadeIn(tag_src, shift=DOWN * 0.3), FadeOut(cl), run_time=0.6)
        cg.add(tag_src)
        # importin alpha
        cx = cg.body.get_center()
        al = blob("α", BLUE, 0.62, 0.56, 28, pos=(cx[0] + 0.62, cx[1] - 1.3))
        al_l = T("importin α", 24, BLUE).next_to(al, DOWN, buff=0.18)
        self.at("alpha reads")
        self.play(FadeIn(al), FadeIn(al_l), run_time=0.4)
        self.play(al.animate.move_to([cx[0] + 0.6, cx[1], 0]), al_l.animate.move_to([cx[0] + 0.6, cx[1] - 0.7, 0]), run_time=0.8)
        be = blob("β", BLUE, 0.9, 0.62, 28, pos=(cx[0] + 1.5, cx[1] - 1.3))
        be_l = T("importin β", 24, BLUE)
        be_l.move_to([cx[0] + 1.9, cx[1] - 1.45, 0])
        self.at("beta binds")
        self.play(FadeOut(al_l), FadeIn(be), FadeIn(be_l), run_time=0.4)
        self.play(be.animate.move_to([cx[0] + 1.35, cx[1], 0]), be_l.animate.move_to([cx[0] + 1.35, cx[1] - 0.8, 0]), run_time=0.8)
        cx_all = VGroup(cg, al, be)
        self.at("moves the complex")
        self.play(FadeOut(be_l), cx_all.animate.shift(RIGHT * 2.5), run_time=1.3)
        self.at("repeats")
        self.play(Indicate(pore.fg, color=TEXT, scale_factor=1.0), cx_all.animate.shift(RIGHT * 2.9), run_time=1.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Rule(SpokenScene):
    """No pushing; the load is put down on one side; Ran GTP (on) and Ran GDP (off)."""

    def construct(self):
        st = stage()
        self.add(st)
        # same place as the end of scene 2: complex in the nucleus
        cg = cargo([1.35, 0, 0], tag="NLS")
        al = blob("α", BLUE, 0.62, 0.56, 28, pos=(1.9, 0))
        be = blob("β", BLUE, 0.9, 0.62, 28, pos=(2.65, 0))
        cx = VGroup(cg, al, be)
        self.add(cx)
        self.at("does not set")
        pa = DoubleArrow([-1.9, 0, 0], [-0.0 - 0.9, 0, 0], buff=0, color=GREY, stroke_width=5)
        self.play(Indicate(st[0].fg, color=TEXT, scale_factor=1.0), run_time=1.0)
        # a "push" arrow, crossed out
        push = T("push", 30, RED).move_to([-3.2, 0.0, 0])
        arrow = arr([-2.5, 0, 0], [-1.1, 0, 0], RED, 6)
        x1 = Line([-4.0, 0.45, 0], [-2.4, -0.45, 0], color=RED, stroke_width=7)
        self.at("push anyone")
        self.play(FadeIn(push), GrowArrow(arrow), run_time=0.6)
        self.play(Create(x1), run_time=0.4)
        self.at("loads down")
        self.play(FadeOut(push), FadeOut(arrow), FadeOut(x1), run_time=0.3)
        self.play(cg.animate.shift(DOWN * 0.1 + RIGHT * 0.1), cg[0].animate.shift(DOWN * 0.0), run_time=0.1)
        self.play(cg.animate.shift(RIGHT * 0.9 + UP * 0.9), run_time=1.0)
        self.play(FadeOut(VGroup(cg, al, be)), run_time=0.5)
        gtp = bchip("Ran + GTP", GREEN, 28).move_to([-3.2, 1.0, 0])
        gdp = bchip("Ran + GDP", RED, 28).move_to([-3.2, -1.0, 0])
        on = T("on", 28, GREEN, weight=BOLD).next_to(gtp, LEFT, buff=0.25)
        off = T("off", 28, RED, weight=BOLD).next_to(gdp, LEFT, buff=0.25)
        self.at("depends on")
        self.play(FadeIn(gtp, shift=UP * 0.2), run_time=0.5)
        sw1 = arr([-3.7, 0.55, 0], [-3.7, -0.55, 0], GREY, 4)
        sw2 = arr([-2.7, -0.55, 0], [-2.7, 0.55, 0], GREY, 4)
        self.at("on with")
        self.play(FadeIn(on), run_time=0.4)
        self.play(FadeIn(gdp, shift=DOWN * 0.2), GrowArrow(sw1), GrowArrow(sw2), run_time=0.8)
        self.at("off with")
        self.play(FadeIn(off), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Gradient(SpokenScene):
    """RCC1 on chromatin makes RanGTP in the nucleus; RanGAP1 hydrolyses it outside; NTF2 returns RanGDP."""

    def construct(self):
        st = stage()
        self.add(st)
        gtp = bchip("Ran + GTP", GREEN, 28).move_to([-3.2, 1.0, 0])
        gdp = bchip("Ran + GDP", RED, 28).move_to([-3.2, -1.0, 0])
        self.add(gtp, gdp)
        lg = legend()
        tn, ng, cg_, cr = gradient_group()
        self.at("In the nucleus")
        self.play(ReplacementTransform(VGroup(gtp, gdp), lg), run_time=0.9)
        chrom = RoundedRectangle(corner_radius=0.3, width=4.1, height=1.25, stroke_color=GREY, stroke_width=3,
                                 fill_color=GREY, fill_opacity=0.18).move_to([3.95, 2.55, 0])
        chl = T("chromatin", 24, GREY).move_to([2.95, 2.55, 0])
        rcc = bchip("RCC1", TEAL, 26).move_to([5.0, 2.55, 0])
        self.at("chromatin")
        self.play(FadeIn(chrom), FadeIn(chl), FadeIn(rcc, scale=0.8), run_time=0.8)
        # RanGTP spreads out from RCC1
        seeds = VGroup(*[rdot(rcc.get_center() + DOWN * 0.1, GREEN) for _ in NUC_G])
        for s_ in seeds:
            s_.set_opacity(0)
        self.add(seeds)
        self.at("loads")
        self.play(FadeIn(tn), LaggedStart(*[s_.animate.set_opacity(1).move_to([p[0], p[1], 0]) for s_, p in zip(seeds, NUC_G)],
                                          lag_ratio=0.12), run_time=2.2)
        self.at("made in the nucleus")
        self.play(Indicate(seeds, color=GREEN, scale_factor=1.25), run_time=0.8)
        # cytoplasm
        gap = bchip("RanGAP1", TEAL, 26).move_to([-3.2, -1.2, 0])
        h_dot = rdot((-2.0, -1.2), GREEN)
        self.at("In the cytoplasm")
        self.play(FadeIn(gap, scale=0.8), FadeIn(h_dot), run_time=0.7)
        self.at("break down")
        self.play(h_dot.animate.set_color(RED), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(d) for d in cr], lag_ratio=0.15), run_time=1.2)
        self.at("stays low")
        self.play(FadeIn(cg_), run_time=0.6)
        # NTF2
        ntf = bchip("NTF2", TEAL, 26).move_to([-3.6, -2.3, 0])
        rd = rdot((-2.55, -2.3), RED)
        self.at("brings")
        self.play(FadeIn(ntf, scale=0.8), FadeIn(rd), run_time=0.5)
        grp = VGroup(ntf, rd)
        self.play(grp.animate.shift(RIGHT * 4.85), run_time=2.2)
        self.at("recharged")
        self.play(rd.animate.set_color(GREEN), run_time=0.5)
        self.play(FadeOut(ntf), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Loads(SpokenScene):
    """Importin: loads where RanGTP is low, drops it when RanGTP binds. Exportin: holds cargo only with RanGTP."""

    def construct(self):
        st = stage()
        tn, ng, cg_, cr = gradient_group()
        lg = legend()
        self.add(tn, st, lg, ng, cg_, cr)
        # importin and its cargo, in the cytoplasm
        cg = cargo([-5.0, 0, 0], tag="NLS")
        al = blob("α", BLUE, 0.62, 0.56, 28, pos=(-3.5, 0))
        be = blob("β", BLUE, 0.9, 0.62, 28, pos=(-2.75, 0))
        imp_l = T("importin", 24, BLUE).move_to([-3.1, -0.75, 0])
        self.at("couriers read")
        self.play(FadeIn(cg), FadeIn(al), FadeIn(be), FadeIn(imp_l), run_time=0.8)
        self.at("loads cargo")
        self.play(cg.animate.shift(RIGHT * 0.88), run_time=0.8)
        comp = VGroup(cg, al, be)
        self.play(FadeOut(imp_l), comp.animate.shift(RIGHT * 5.3), run_time=2.0)
        # RanGTP binds importin beta
        src = ng[0]
        flier = rdot(src.get_center(), GREEN, 0.15)
        self.add(flier)
        self.at("drops it")
        self.play(flier.animate.move_to(be.get_top() + UP * 0.02), run_time=0.6)
        self.play(cg.animate.shift(RIGHT * 0.8 + UP * 0.7), FadeOut(VGroup(al, be, flier)), run_time=0.9)
        # export
        self.at("such as")
        self.play(FadeOut(cg), run_time=0.5)
        crm = blob("CRM1", PURPLE, 1.2, 0.62, 26, pos=(2.5, 0))
        ex_c = cargo([4.3, 0, 0], tag="NES")
        self.play(FadeIn(crm), FadeIn(ex_c), run_time=0.6)
        fl2 = rdot(ng[3].get_center(), GREEN, 0.15)
        self.add(fl2)
        self.at("only together")
        self.play(fl2.animate.move_to(crm.get_top() + UP * 0.02), run_time=0.6)
        self.play(ex_c.animate.move_to([3.45, 0, 0]) if False else ex_c.animate.shift(LEFT * 0.9), run_time=0.6)
        grp = VGroup(crm, ex_c, fl2)
        self.play(grp.animate.shift(LEFT * 5.7), run_time=2.0)
        self.at("breaks the complex")
        self.play(fl2.animate.set_color(RED), run_time=0.4)
        self.play(ex_c.animate.shift(RIGHT * 0.9 + UP * 0.7), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    """Transportin crosses with no Ran; the gradient decides where loads are picked up and dropped; the rule."""

    def construct(self):
        st = stage()
        self.add(st)
        self.at("energy spent")
        push = T("energy to push?", 28, GREY).move_to([-3.2, 1.55, 0])
        self.play(FadeIn(push), run_time=0.5)
        self.at("Not on pushing")
        cr = Line([-4.6, 1.35, 0], [-1.8, 1.75, 0], color=RED, stroke_width=7)
        self.play(Create(cr), run_time=0.5)
        note = T("test tube: no Ran, no nucleotide", 24, GREY).move_to([-3.4, 2.55, 0])
        tr = blob("transportin", BLUE, 2.0, 0.62, 24, pos=(-3.2, 0))
        ca = cargo([-4.6, 0, 0])
        self.at("test tube")
        self.play(FadeOut(push), FadeOut(cr), FadeIn(note), FadeIn(tr), FadeIn(ca), run_time=0.7)
        comp = VGroup(tr, ca)
        self.at("carried cargo")
        self.play(comp.animate.shift(RIGHT * 6.2), run_time=2.6)
        tn, ng, cg_, cr_ = gradient_group()
        lg = legend()
        self.at("builds and resets")
        self.play(FadeOut(comp), FadeOut(note), FadeIn(tn), FadeIn(lg), run_time=0.6)
        self.play(FadeIn(ng), FadeIn(cg_), LaggedStart(*[FadeIn(d) for d in cr_], lag_ratio=0.1), run_time=1.5)
        c1 = bchip("the pore is open", GREY, 30).move_to([-3.3, 0, 0])
        c2 = bchip("RanGTP sets the direction", GREEN, 30).move_to([3.5, 0, 0])
        self.at("pore is open")
        self.play(FadeIn(c1, shift=RIGHT * 0.2), run_time=0.6)
        self.at("sets the direction")
        self.play(FadeIn(c2, shift=LEFT * 0.2), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "The pore is open. Ran GTP sets the direction."
