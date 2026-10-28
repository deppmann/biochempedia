"""GPCRs and trimeric G proteins: the receptor and its G protein decide the answer  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = acetylcholine, the signal (and its "agonist" tag)
  BLUE   = the receptor (the seven helices, "receptor", M2, M3)
  PURPLE = the G protein alpha part (Gα, and the names Gi / Gq / "G protein")
  ORANGE = beta gamma
  GREEN  = on / active: GTP, and the outline of Gα once GTP sits in it
  TEAL   = the targets that a messenger switches on (potassium channel, phospholipase C-β)
  PINK   = ions and small messengers (K+, IP3, Ca2+)
  RED    = ruled out (the crossed-out "instruction", the struck-out signal)
  GREY   = membranes, cell outlines, GDP, the unknown, labels
  GOLD   = title rule only

No molecular structures: the receptor is seven plain bars in a membrane band, the G protein parts are
labelled rounded blobs, GDP / GTP are chips, channels and enzymes are blocks and chips, ions are dots.

Framing: s02 and s03 are one stage (membrane band across the middle, receptor left of centre, G protein
under it). s04 and s05 keep that stage and add the target on the right and a small readout card on the
top left. s01 and s06 are the same two-cell picture, before and after the answer is filled in.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#F08BB4"

# ---- the stage -------------------------------------------------------------------------------
MEM_Y, MEM_H = 0.6, 2.5
BAND_TOP, BAND_BOT = MEM_Y + MEM_H / 2, MEM_Y - MEM_H / 2          # 1.85, -0.65
HW, HH, PITCH = 0.5, 2.7, 0.64                                     # helix width, length, spacing
RX = -0.9                                                          # centre of the helix bundle
HTOP, HBOT = MEM_Y + HH / 2, MEM_Y - HH / 2                        # 1.95, -0.75
NOTCH = 0.6                                                        # the three middle helices stop short: the pocket
SWING = 28 * DEGREES                                               # how far helix 6 swings out
GX = 0.61                                                          # x of the cavity and the G alpha tail
YB_WAIT, YB_DOCK = -2.35, -1.55                                    # G alpha centre: waiting, docked
FA = np.array([-3.9, -2.4, 0])                                     # G alpha-GTP once it has let go
FB = np.array([4.8, -2.4, 0])                                      # beta gamma once it has let go
LIG_DOCK = np.array([RX, HTOP - NOTCH + 0.33, 0])                  # acetylcholine in the pocket
CX = 4.2                                                           # x of the potassium channel
XC = 3.4                                                           # x centre of each cell column (s01, s06)


def hx(i):
    # the seventh bar stands a little apart, so helix 6 (the sixth) has room to swing out
    return RX + (i - 3) * PITCH + (1.5 if i == 6 else 0.0)


# s02 is drawn zoomed in (the receptor is the subject), then eases back to the stage s03 starts on
K2 = 1.35
Z0 = np.array([RX, MEM_Y, 0.0])
Z1 = np.array([-0.5, -0.15, 0.0])


def zp(p):
    return Z1 + K2 * (np.array(p, float) - Z0)


def zoom(m):
    return m.scale(K2, about_point=Z0).shift(Z1 - Z0)


# ---- helpers ---------------------------------------------------------------------------------
def G(text, size=28, color=PURPLE):
    """a Greek-letter label. Avenir draws alpha like a Latin a, so these use the serif title face."""
    return T(text, size, color, font=TITLE_FONT, weight=BOLD)


def bchip(text, color=BLUE, size=26, pad=0.2, **kw):
    """chip with an opaque backing so lines drawn behind it do not show through. [back, box, label]"""
    c = chip(text, color, size=size, pad=pad, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def ghost_chip(text, size=24):
    """a dashed grey chip: something that is NOT there."""
    t = T(text, size, GREY)
    box = RoundedRectangle(corner_radius=0.14, width=t.width + 0.4, height=t.height + 0.32)
    return VGroup(DashedVMobject(box, num_dashes=max(18, int(box.width * 9))).set_color(GREY), t)


def strike(m, color=RED):
    return Line(m.get_corner(DL) + [-0.08, -0.04, 0], m.get_corner(UR) + [0.08, 0.04, 0], color=color, stroke_width=7)


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def glow(*mobs, s=1.1, color=TEXT):
    """flash each mobject in place (one animation each: a new VGroup would re-add them on top)."""
    return [Indicate(m, color=color, scale_factor=s) for m in mobs]


def chip_glow(c, s=1.1, color=TEXT):
    return glow(c[1], c[2], s=s, color=color)


def band():
    return RoundedRectangle(corner_radius=0.12, width=12.6, height=MEM_H, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.2).move_to([0, MEM_Y, 0])


def side_labels():
    return VGroup(T("outside", 24, GREY).move_to([-5.6, 2.45, 0]), T("inside", 24, GREY).move_to([-5.6, -1.05, 0]))


# ---- the receptor: seven bars --------------------------------------------------------------------
def helix(i):
    x = hx(i)
    top = HTOP - (NOTCH if i in (2, 3, 4) else 0)
    h = top - HBOT
    back = RoundedRectangle(corner_radius=HW / 2, width=HW, height=h, stroke_width=0, fill_color=BG, fill_opacity=1)
    body = RoundedRectangle(corner_radius=HW / 2, width=HW, height=h, stroke_color=BLUE, stroke_width=3,
                            fill_color=BLUE, fill_opacity=0.35)
    return VGroup(back, body).move_to([x, (top + HBOT) / 2, 0])


def pivot6():
    return np.array([hx(5), HTOP, 0])


def receptor(swung=False):
    g = VGroup(*[helix(i) for i in range(7)])
    if swung:
        g[5].rotate(SWING, about_point=pivot6())
    return g


def silhouette():
    return RoundedRectangle(corner_radius=0.3, width=4.6, height=HH + 0.1, stroke_color=BLUE, stroke_width=3,
                            fill_color=BLUE, fill_opacity=0.18).move_to([RX, MEM_Y, 0])


def cavity():
    e = Ellipse(width=1.0, height=0.8).move_to([GX, -0.2, 0])
    return DashedVMobject(e, num_dashes=24).set_color(TEXT).set_stroke(width=3)


def ligand(center, tag=True, k=1.0):
    """[dot, label, (agonist tag)]: the label rides above the dot. k scales the dot and the label offsets."""
    dot = Circle(radius=0.28 * k, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=1).move_to(center)
    lab = T("acetylcholine", 26, YELLOW).move_to(np.array(center) + UP * 0.68 * k)
    g = VGroup(dot, lab)
    g.dot, g.lab = dot, lab
    if tag:
        g.add(T("agonist", 24, YELLOW).move_to(np.array(center) + UP * 1.08 * k))
    return g


# ---- the G protein -------------------------------------------------------------------------------
def galpha(x, yb, label="Gα", active=False):
    """[tail, back, body, label]; the tail is the part that fits the cavity."""
    tail = RoundedRectangle(corner_radius=0.14, width=0.4, height=0.9, stroke_color=PURPLE, stroke_width=3,
                            fill_color=PURPLE, fill_opacity=0.5).move_to([x, yb + 0.95, 0])
    back = RoundedRectangle(corner_radius=0.45, width=1.9, height=1.3, stroke_width=0, fill_color=BG,
                            fill_opacity=1).move_to([x, yb, 0])
    body = RoundedRectangle(corner_radius=0.45, width=1.9, height=1.3, stroke_color=GREEN if active else PURPLE,
                            stroke_width=3.5, fill_color=PURPLE, fill_opacity=0.3).move_to([x, yb, 0])
    lbl = G(label, 28, PURPLE).move_to([x, yb + 0.3, 0])
    return [tail, back, body, lbl]


def nuc(x, y, text, color):
    return bchip(text, color, 22, pad=0.12).move_to([x, y, 0])


def lobe(x, y, w, h, text, r=0.35):
    back = RoundedRectangle(corner_radius=r, width=w, height=h, stroke_width=0, fill_color=BG, fill_opacity=1)
    body = RoundedRectangle(corner_radius=r, width=w, height=h, stroke_color=ORANGE, stroke_width=3.5,
                            fill_color=ORANGE, fill_opacity=0.3)
    lab = G(text, 26, ORANGE)
    return VGroup(back, body, lab).move_to([x, y, 0])


def bgamma(x, y):
    """the beta gamma unit: one blob."""
    back = RoundedRectangle(corner_radius=0.45, width=1.5, height=1.2, stroke_width=0, fill_color=BG,
                            fill_opacity=1).move_to([x, y, 0])
    body = RoundedRectangle(corner_radius=0.45, width=1.5, height=1.2, stroke_color=ORANGE, stroke_width=3.5,
                            fill_color=ORANGE, fill_opacity=0.3).move_to([x, y, 0])
    lbl = G("βγ", 30, ORANGE).move_to([x, y, 0])
    return [back, body, lbl]


def shift_all(parts, v):
    return [p.animate.shift(v) for p in parts]


# ---- ions, targets, cards ------------------------------------------------------------------------------
def ion(text, x, y, r=0.26):
    c = Circle(radius=r, stroke_color=PINK, stroke_width=2.5, fill_color=PINK, fill_opacity=0.9)
    return VGroup(c, T(text, 22, BG, weight=BOLD).move_to(c)).move_to([x, y, 0])


def channel(opened):
    """the potassium channel: two blocks across the membrane; closed they touch, open they leave a gap."""
    off = 0.65 if opened else 0.275
    g = VGroup()
    for sgn in (-1, 1):
        back = RoundedRectangle(corner_radius=0.12, width=0.55, height=MEM_H, stroke_width=0, fill_color=BG, fill_opacity=1)
        body = RoundedRectangle(corner_radius=0.12, width=0.55, height=MEM_H, stroke_color=TEAL, stroke_width=3.5,
                                fill_color=TEAL, fill_opacity=0.4)
        g.add(VGroup(back, body).move_to([CX + sgn * off, MEM_Y, 0]))
    return g


def qbox(x, y, w=0.9, h=0.9):
    shape = RoundedRectangle(corner_radius=0.14, width=w, height=h).move_to([x, y, 0])
    back = shape.copy().set_stroke(width=0).set_fill(BG, 1)
    return VGroup(back, DashedVMobject(shape, num_dashes=24).set_color(GREY),
                  T("?", 40, TEXT, weight=BOLD).move_to([x, y, 0]))


def card():
    return RoundedRectangle(corner_radius=0.2, width=5.0, height=2.3, stroke_color=GREY, stroke_width=2).move_to([1.05, -2.15, 0])


def title_tag(text):
    return T(text, 28, GREY).move_to([-4.2, 3.2, 0])


def ticks(cx, y, h=0.22):
    xs = np.array([0, 0.3, 0.65, 1.05, 1.55, 2.15])
    xs = xs - xs.mean() + cx
    return VGroup(*[Line([x, y - h, 0], [x, y + h, 0], color=TEXT, stroke_width=6) for x in xs])


# ---- the two-cell picture (s01 and s06) ------------------------------------------------------------------
class Cells:
    """ACh on top; below, a heart pacemaker cell on the left and an airway muscle cell on the right.
    In each: arrow in, a box for the path (a question mark, then receptor -> G protein), arrow out, the outcome."""

    def __init__(self):
        self.ach = bchip("acetylcholine", YELLOW, 30).move_to([0, 2.95, 0])
        self.col = {}
        for side, tag in ((-1, "heart pacemaker cell"), (1, "airway muscle cell")):
            x = side * XC
            outline = RoundedRectangle(corner_radius=0.3, width=5.8, height=4.8, stroke_color=GREY, stroke_width=3).move_to([x, -0.95, 0])
            name = T(tag, 26, GREY).move_to([x, -3.0, 0])
            shape = RoundedRectangle(corner_radius=0.16, width=5.0, height=1.0).move_to([x, 0.55, 0])
            box = VGroup(shape.copy().set_stroke(width=0).set_fill(BG, 1), DashedVMobject(shape, num_dashes=48).set_color(GREY))
            q = T("?", 44, TEXT, weight=BOLD).move_to([x, 0.55, 0])
            a_in = arr([side * 0.55, 2.55, 0], [x, 1.1, 0], YELLOW)
            a_out = arr([x, 0.0, 0], [x, -0.5, 0], GREY)
            if side < 0:
                out = T("heart slows", 34, TEXT, weight=BOLD).move_to([x, -0.95, 0])
                glyph = ticks(x, -2.0)
            else:
                out = T("muscle contracts", 34, TEXT, weight=BOLD).move_to([x, -0.95, 0])
                glyph = RoundedRectangle(corner_radius=0.25, width=3.2, height=0.5, stroke_color=TEXT, stroke_width=3,
                                         fill_color=GREY, fill_opacity=0.5).move_to([x, -2.0, 0])
            self.col[side] = dict(outline=outline, name=name, box=box, q=q, a_in=a_in, a_out=a_out, out=out, glyph=glyph, x=x)

    def pair(self, side, left, right, lc=BLUE, rc=PURPLE):
        """the two chips and the arrow between them, in the box."""
        x = self.col[side]["x"]
        a = bchip(left, lc, 26).move_to([x - 1.35, 0.55, 0])
        b = bchip(right, rc, 26).move_to([x + 1.35, 0.55, 0])
        mid = arr([a.get_right()[0] + 0.05, 0.55, 0], [b.get_left()[0] - 0.05, 0.55, 0], GREY, w=4, tip=0.16)
        return a, mid, b


class S00Title(TitleCard):
    LESSON = "GPCRs and Trimeric G Proteins"
    TITLE = "The Receptor Decides the Answer"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    """one molecule, two opposite answers: who decides, the molecule or the cell? (the puzzle, two cells)"""

    def construct(self):
        C = Cells()
        L, R = C.col[-1], C.col[1]
        self.at("Acetylcholine")
        self.play(FadeIn(C.ach, shift=DOWN * 0.2), run_time=0.5)

        self.at("slows the heart")
        self.play(FadeIn(L["outline"]), FadeIn(L["name"]), GrowArrow(L["a_in"]), FadeIn(L["box"]), FadeIn(L["q"]), run_time=0.7)
        self.play(GrowArrow(L["a_out"]), FadeIn(L["out"], shift=DOWN * 0.1), run_time=0.4)
        self.play(LaggedStart(*[Create(t) for t in L["glyph"]], lag_ratio=0.3), run_time=1.0)

        self.at("makes the muscle")
        self.play(FadeIn(R["outline"]), FadeIn(R["name"]), GrowArrow(R["a_in"]), FadeIn(R["box"]), FadeIn(R["q"]), run_time=0.7)
        self.play(FadeIn(R["glyph"]), run_time=0.3)
        self.at("contract")
        self.play(GrowArrow(R["a_out"]), FadeIn(R["out"], shift=DOWN * 0.1), run_time=0.4)
        self.play(R["glyph"].animate.stretch_to_fit_width(1.7).stretch_to_fit_height(0.75), run_time=0.7)

        self.at("Who decides")
        self.play(*[Indicate(c["q"], color=YELLOW, scale_factor=1.3) for c in (L, R)], run_time=0.8)
        self.at("the molecule")
        self.play(*chip_glow(C.ach, 1.12), run_time=0.6)
        self.at("or the cell")
        self.play(*[Indicate(c["outline"], color=TEXT, scale_factor=1.02) for c in (L, R)], run_time=0.8)

        ghost = ghost_chip("instruction", 24).move_to([4.0, 2.95, 0])
        link = arr([C.ach.get_right()[0], 2.95, 0], [ghost.get_left()[0], 2.95, 0], GREY, w=3, tip=0.15)
        self.at("carries no instruction")
        self.play(GrowArrow(link), FadeIn(ghost), run_time=0.6)
        x1 = strike(ghost)
        self.play(Create(x1), run_time=0.4)

        self.at("Each cell decides")
        self.play(FadeOut(VGroup(link, ghost, x1)), *[Indicate(c["outline"], color=TEXT, scale_factor=1.02) for c in (L, R)],
                  run_time=0.8)
        recs, gps = [], []
        for side in (-1, 1):
            a, mid, b = C.pair(side, "receptor", "G protein")
            recs.append((a, mid, b))
        self.at("its receptor")
        self.play(*[FadeOut(c["q"]) for c in (L, R)], *[FadeIn(r[0], scale=0.8) for r in recs], run_time=0.6)
        self.at("G protein")
        self.play(*[GrowArrow(r[1]) for r in recs], *[FadeIn(r[2], scale=0.8) for r in recs], run_time=0.7)
        self.play(*[pulse for r in recs for pulse in chip_glow(r[2], 1.08, PURPLE)], run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Pocket(SpokenScene):
    """the seven-helix receptor: the agonist binds in a pocket, helix 6 swings out and opens a cavity. (zoomed in)"""

    def construct(self):
        mem = zoom(band())
        labs = VGroup(T("outside", 24, GREY).move_to([-5.6, 2.0, 0]), T("inside", 24, GREY).move_to([-5.6, -2.1, 0]))
        self.add(mem, labs)
        sil = zoom(silhouette())
        gp = T("GPCR", 30, BLUE, weight=BOLD).move_to([-0.5, -2.45, 0])
        self.at("This receptor")
        self.play(FadeIn(sil, scale=0.9), FadeIn(gp), run_time=0.7)

        self.at("coupled receptor")
        self.play(Indicate(sil, color=TEXT, scale_factor=1.03), run_time=0.8)
        self.at("Its chain")
        self.play(Indicate(gp, color=TEXT, scale_factor=1.25), run_time=0.8)

        rec = zoom(receptor())
        self.at("crosses the membrane")
        self.play(FadeOut(sil), LaggedStart(*[FadeIn(h, shift=UP * 0.25) for h in rec], lag_ratio=0.18), run_time=1.6)
        self.at("seven helices")
        self.play(LaggedStart(*[Indicate(h[1], color=TEXT, scale_factor=1.08) for h in rec], lag_ratio=0.18), run_time=1.4)

        dock = zp(LIG_DOCK)
        lig = ligand([4.0, 1.9, 0], tag=False, k=K2)
        self.at("Acetylcholine is")
        self.play(FadeIn(lig, shift=DOWN * 0.2), run_time=0.6)
        ag = T("agonist", 24, YELLOW).move_to(lig.dot.get_center() + UP * 1.08 * K2)
        self.at("agonist")
        self.play(FadeIn(ag, shift=DOWN * 0.1), run_time=0.4)
        lig.add(ag)
        self.at("activates its receptor")
        self.play(Indicate(lig.dot, color=TEXT, scale_factor=1.4), Indicate(rec[3][1], color=TEXT, scale_factor=1.04), run_time=0.7)

        self.at("binds in a pocket")
        self.play(lig.animate.shift(dock - lig.dot.get_center()), FadeOut(gp), run_time=1.3)
        self.at("favors")
        self.play(LaggedStart(*[Indicate(rec[i][1], color=TEXT, scale_factor=1.05) for i in (1, 2, 3, 4, 5)], lag_ratio=0.12),
                  run_time=0.9)

        pv = zp(pivot6())
        lab6 = T("helix 6", 26, BLUE, weight=BOLD).move_to(pv + np.array([1.5, 0.55, 0]))
        ptr = Line(pv + np.array([0.85, 0.43, 0]), pv + np.array([0.2, 0.13, 0]), color=BLUE, stroke_width=3)
        self.at("inner end of helix")
        self.play(FadeIn(lab6), Create(ptr), Indicate(rec[5][1], color=TEXT, scale_factor=1.12), run_time=0.8)
        self.at("swings outward")
        self.play(Rotate(rec[5], SWING, about_point=pv), run_time=1.4)
        cav = zoom(cavity())
        cav_lbl = T("cavity", 24, TEXT).move_to(zp([GX, -1.15, 0]))
        self.at("opens a cavity")
        self.play(Create(cav), FadeIn(cav_lbl), run_time=0.8)

        # after the last word: ease back to the stage the next scene starts on
        rest = self.narration_s - 0.02 - self.elapsed()
        if rest > 0:
            self.wait(rest)
        nlig, nrec, nlabs = ligand(LIG_DOCK), receptor(swung=True), VGroup(*side_labels())
        self.play(FadeOut(lab6), FadeOut(ptr), FadeOut(cav_lbl), run_time=0.3)
        self.play(Transform(mem, band()), *[Transform(rec[i], nrec[i]) for i in range(7)], Transform(cav, cavity()),
                  Transform(lig.dot, nlig.dot), lig.lab.animate.move_to(nlig.lab.get_center()),
                  ag.animate.move_to(nlig[2].get_center()),
                  labs[0].animate.move_to(nlabs[0].get_center()), labs[1].animate.move_to(nlabs[1].get_center()),
                  run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Loading(SpokenScene):
    """the receptor loads the G protein: GDP out, GTP in, Gα·GTP and βγ let go."""

    def construct(self):
        mem, labs = band(), side_labels()
        rec = receptor(swung=True)
        lig = ligand(LIG_DOCK)
        cav = cavity()
        self.add(mem, labs, rec, lig, cav)

        ga = galpha(GX, YB_WAIT)
        gdp = nuc(GX, YB_WAIT - 0.27, "GDP", GREY)
        bx, by = GX + 1.95, YB_WAIT
        gp_lab = T("G protein", 26, PURPLE).move_to([(GX + bx) / 2, -3.3, 0])
        self.at("Waiting just inside")
        self.play(FadeIn(VGroup(*ga), shift=UP * 0.3), run_time=0.7)
        self.at("a G protein")
        self.play(FadeIn(gp_lab), *glow(ga[2], ga[3], s=1.06, color=TEXT), run_time=0.6)
        self.at("holds")
        self.play(FadeIn(gdp, scale=0.7), run_time=0.5)

        # beta and gamma bind each other and become one unit
        beta = lobe(bx + 1.2, by + 0.45, 0.95, 0.95, "Gβ")
        gamma = lobe(bx + 2.0, by - 0.55, 0.8, 0.8, "Gγ", r=0.3)
        self.at("bind each other")
        self.play(FadeIn(beta, shift=LEFT * 0.2), FadeIn(gamma, shift=LEFT * 0.2), run_time=0.5)
        self.play(beta.animate.move_to([bx - 0.4, by + 0.1, 0]), gamma.animate.move_to([bx + 0.5, by - 0.1, 0]), run_time=0.9)
        bg = bgamma(bx, by)
        self.at("one unit")
        self.play(FadeOut(beta), FadeOut(gamma), FadeIn(VGroup(*bg)), run_time=0.5)

        # the active receptor grips the G protein: its tail fits the cavity
        dock = np.array([0, YB_DOCK - YB_WAIT, 0])
        self.at("The active receptor")
        self.play(LaggedStart(*[Indicate(h[1], color=TEXT, scale_factor=1.05) for h in rec], lag_ratio=0.08), run_time=0.9)
        self.at("grips")
        self.play(FadeOut(cav), FadeOut(gp_lab), *shift_all(ga, dock), gdp.animate.shift(dock), *shift_all(bg, dock), run_time=1.0)
        self.at("loosens")
        self.play(Wiggle(gdp, scale_value=1.15, rotation_angle=0.05 * TAU), run_time=1.0)
        self.at("leaves")
        self.play(gdp.animate.shift(DOWN * 1.5 + LEFT * 1.4).set_opacity(0), run_time=0.9)
        gtp = nuc(3.0, -3.1, "GTP", GREEN)
        slot = np.array([GX, YB_DOCK - 0.27, 0])
        self.at("takes the empty")
        self.play(FadeIn(gtp, shift=UP * 0.2), run_time=0.3)
        self.play(gtp.animate.move_to(slot), run_time=0.8)
        self.play(ga[2].animate.set_stroke(GREEN, 4), run_time=0.4)

        tb = T("textbook picture", 24, GREY).move_to([0.6, -3.3, 0])
        self.at("textbook picture")
        self.play(FadeIn(tb), run_time=0.4)
        pull = np.array([0, -0.7, 0])                         # first the tail comes out of the cavity
        free_a = FA - np.array([GX, YB_DOCK - 0.7, 0])        # then each part drifts away
        free_b = FB - np.array([bx, YB_DOCK - 0.7, 0])
        self.at("lets go")
        self.play(*shift_all(ga, pull), gtp.animate.shift(pull), *shift_all(bg, pull), run_time=0.6)
        self.play(*shift_all(ga, free_a), gtp.animate.shift(free_a), *shift_all(bg, free_b), FadeOut(tb), run_time=1.3)
        self.finish()


# ---------------------------------------------------------------------------------------------
def free_state():
    """what s03 leaves behind (and s04, s05 start from): receptor, ligand, Gα·GTP left, βγ right."""
    rec = receptor(swung=True)
    lig = ligand(LIG_DOCK)
    ga = galpha(FA[0], FA[1], active=True)
    gtp = nuc(FA[0], FA[1] - 0.27, "GTP", GREEN)
    bg = bgamma(FB[0], FB[1])
    return rec, lig, ga, gtp, bg


class S04Heart(SpokenScene):
    """pacemaker cell: M2 couples to Gi, free βγ opens a potassium channel, potassium leaves, the heart slows."""

    def construct(self):
        mem = band()
        rec, lig, ga, gtp, bg = free_state()
        self.add(mem, rec, lig, *ga, gtp, *bg)

        tag_a = T("messenger", 24, GREY).move_to([FA[0], -3.3, 0])
        tag_b = T("messenger", 24, GREY).move_to([FB[0], -3.3, 0])
        self.at("alpha with")
        self.play(*glow(ga[2], ga[3], s=1.08, color=TEXT), FadeIn(tag_a), run_time=0.7)
        self.at("free beta gamma")
        self.play(*glow(bg[1], bg[2], s=1.08, color=TEXT), FadeIn(tag_b), run_time=0.7)

        qa, qb = qbox(-5.7, FA[1]), qbox(CX, MEM_Y)
        da = DashedLine([FA[0] - 0.98, FA[1], 0], [-5.2, FA[1], 0], color=GREY, stroke_width=3, dash_length=0.1)
        db = DashedLine([FB[0] - 0.2, FB[1] + 0.7, 0], [CX + 0.3, MEM_Y - 0.5, 0], color=GREY, stroke_width=3, dash_length=0.1)
        self.at("each can find")
        self.play(FadeIn(qa), Create(da), FadeIn(qb), Create(db), run_time=0.8)

        ttl = title_tag("heart pacemaker cell")
        self.at("pacemaker cells")
        self.play(FadeIn(ttl, shift=DOWN * 0.1), FadeOut(qa), FadeOut(da), run_time=0.6)
        m2 = bchip("M2", BLUE, 26).move_to([-4.6, MEM_Y, 0])
        self.at("the receptor is")
        self.play(FadeIn(m2, shift=RIGHT * 0.15), LaggedStart(*[Indicate(h[1], color=TEXT, scale_factor=1.04) for h in rec],
                                                              lag_ratio=0.06), run_time=0.9)
        gi = bchip("Gi", PURPLE, 26, pad=0.12).move_to([FA[0] + 1.75, FA[1], 0])
        gi_lbl = G("Gαi", 28, PURPLE).move_to(ga[3])
        self.at("G protein called")
        self.play(FadeOut(tag_a), FadeIn(gi, shift=LEFT * 0.15), ReplacementTransform(ga[3], gi_lbl), run_time=0.7)

        ch0, ch1 = channel(False), channel(True)
        ch_lbl = T("potassium\nchannel", 22, TEAL, line_spacing=0.8).move_to([5.45, 2.6, 0])
        tb = T("textbook picture", 24, GREY).move_to([5.0, -2.9, 0])
        self.at("beta gamma")
        self.play(FadeIn(tb), run_time=0.4)
        self.play(FadeOut(tag_b), FadeOut(qb), FadeOut(db), FadeIn(ch0), FadeIn(ch_lbl),
                  *shift_all(bg, np.array([5.45 - FB[0], -1.25 - FB[1], 0])), run_time=1.2)
        self.at("potassium channel")
        self.play(*[Transform(a, b) for a, b in zip(ch0, ch1)], run_time=0.8)

        # potassium streams out through the gap, for as long as the scene runs
        Y0, Y1 = -1.4, 3.1
        ions = [ion("K⁺", CX, Y0 - 0.9 * k) for k in range(5)]

        def mover(m, dt):
            m.shift(UP * 2.0 * dt)
            y = m.get_center()[1]
            if y > Y1:
                m.shift(DOWN * (Y1 - Y0))
                y = m.get_center()[1]
            m.set_opacity(float(np.clip(min((y - Y0) / 0.5, (Y1 - y) / 0.8), 0, 1)))
        for d in ions:
            d.set_opacity(0)
            self.add(d)
        self.at("potassium leaves")
        for d in ions:
            d.add_updater(mover)
        self.wait(0.6)

        cd = card()
        thr = DashedLine([-1.1, -1.5, 0], [0.3, -1.5, 0], color=GREY, stroke_width=3, dash_length=0.12)
        thr_l = T("firing threshold", 22, GREY).move_to([1.95, -1.5, 0])
        mark = Line([-1.1, -1.95, 0], [0.3, -1.95, 0], color=TEXT, stroke_width=7)
        mark_l = T("membrane potential", 22, TEXT).move_to([1.95, -1.95, 0])
        self.at("moving the voltage")
        self.play(FadeIn(cd), Create(thr), FadeIn(thr_l), Create(mark), FadeIn(mark_l), run_time=0.8)
        self.at("away from threshold")
        self.play(mark.animate.shift(DOWN * 0.85), mark_l.animate.shift(DOWN * 0.85), run_time=1.3)

        camp = T("cAMP ↓", 22, PINK).move_to([-4.0, -3.05, 0])
        current = T("pacemaker current ↓", 22, TEXT).move_to([-4.0, -3.5, 0])
        self.at("Alpha lowers")
        self.play(*glow(ga[2], gi_lbl, s=1.08, color=TEXT), FadeIn(camp), run_time=0.7)
        self.at("pacemaker current")
        self.play(FadeIn(current), run_time=0.6)

        out = T("heart slows", 32, TEXT, weight=BOLD).move_to([-4.2, 2.65, 0])
        tk = ticks(-4.2, 2.2, 0.13)
        self.at("the heart slows")
        self.play(FadeIn(out, shift=DOWN * 0.1), run_time=0.4)
        self.play(LaggedStart(*[Create(t) for t in tk], lag_ratio=0.3), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Airways(SpokenScene):
    """airway muscle: M3 couples to Gq, Gα·GTP switches on phospholipase C-β, PIP2 -> IP3, calcium, contraction."""

    def construct(self):
        mem = band()
        rec, lig, ga, gtp, bg = free_state()
        self.add(mem, rec, lig, *ga, gtp, *bg)

        ttl = title_tag("airway muscle cell")
        self.at("airway muscle")
        self.play(FadeIn(ttl, shift=DOWN * 0.1), *[FadeOut(p) for p in bg], run_time=0.6)
        m3 = bchip("M3", BLUE, 26).move_to([-4.6, MEM_Y, 0])
        self.at("the receptor is")
        self.play(FadeIn(m3, shift=RIGHT * 0.15), LaggedStart(*[Indicate(h[1], color=TEXT, scale_factor=1.04) for h in rec],
                                                              lag_ratio=0.06), run_time=0.9)
        gq = bchip("Gq", PURPLE, 26, pad=0.12).move_to([FA[0] + 1.75, FA[1], 0])
        gq_lbl = G("Gαq", 28, PURPLE).move_to(ga[3])
        self.at("different G protein")
        self.play(FadeIn(gq, shift=LEFT * 0.15), ReplacementTransform(ga[3], gq_lbl), run_time=0.7)
        ga = [ga[0], ga[1], ga[2], gq_lbl]

        # Gα·GTP slides along the inner face to the enzyme
        px, py = 4.0, -1.35
        enz = bchip("enzyme", TEAL, 24).move_to([px, py, 0])
        plc = bchip("phospholipase\nC-β", TEAL, 22).move_to([px, py, 0])
        gdx = np.array([1.7 - FA[0], 0, 0])
        self.at("Alpha with")
        self.play(*glow(ga[2], gq_lbl, s=1.06, color=TEXT), run_time=0.5)
        self.at("switches on")
        self.play(*shift_all(ga, gdx), gtp.animate.shift(gdx), gq.animate.shift(gdx).set_opacity(0), FadeIn(enz, shift=LEFT * 0.2),
                  run_time=1.3)
        self.at("phospholipase")
        self.play(ReplacementTransform(enz, plc), run_time=0.5)
        self.play(plc[1].animate.set_stroke(GREEN, 4), run_time=0.4)

        pip = bchip("PIP2", GREY, 24).move_to([px, -0.2, 0])
        ip3 = bchip("IP3", PINK, 24).move_to([px, -0.2, 0])
        self.at("The enzyme cuts")
        self.play(FadeIn(pip, shift=DOWN * 0.1), *glow(plc[1], plc[2], s=1.06, color=TEXT), run_time=0.6)
        self.play(ReplacementTransform(pip, ip3), run_time=0.5)
        self.play(ip3.animate.move_to([5.8, -0.2, 0]), run_time=0.5)
        self.play(ip3.animate.move_to([5.8, -2.3, 0]), run_time=0.6)

        store = bchip("calcium store", GREY, 24).move_to([4.9, -3.2, 0])
        self.at("releases")
        self.play(FadeIn(store, shift=UP * 0.15), run_time=0.5)
        spots = [(3.4, -2.45), (4.3, -2.45), (5.2, -2.45), (6.0, -2.45)]
        cas = [ion("Ca²⁺", 4.9, -2.9, r=0.34) for _ in spots]
        self.at("stored calcium")
        self.play(FadeOut(ip3, scale=0.5), *[FadeIn(c) for c in cas], run_time=0.3)
        self.play(*[c.animate.move_to([x, y, 0]) for c, (x, y) in zip(cas, spots)], run_time=1.0)

        bar = RoundedRectangle(corner_radius=0.15, width=2.6, height=0.36, stroke_color=TEXT, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.5).move_to([-4.2, 2.2, 0])
        out = T("muscle contracts", 32, TEXT, weight=BOLD).move_to([-4.2, 2.65, 0])
        self.at("the muscle contracts")
        self.play(FadeIn(bar), FadeIn(out, shift=DOWN * 0.1), run_time=0.5)
        self.play(bar.animate.stretch_to_fit_width(1.4).stretch_to_fit_height(0.55), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    """the opening picture, answered: M2 + Gi in the heart, M3 + Gq in the airways; same acetylcholine."""

    def construct(self):
        C = Cells()
        L, R = C.col[-1], C.col[1]
        R["glyph"].stretch_to_fit_width(1.7).stretch_to_fit_height(0.75)
        parts = [C.ach]
        for c in (L, R):
            parts += [c["outline"], c["name"], c["box"], c["a_in"], c["a_out"], c["out"], c["glyph"]]
        pairs = {s: C.pair(s, "receptor", "G protein") for s in (-1, 1)}
        for s in (-1, 1):
            parts += list(pairs[s])
        self.add(*parts)

        new = {-1: C.pair(-1, "M2", "Gi"), 1: C.pair(1, "M3", "Gq")}
        self.at("In the heart")
        self.play(*[ReplacementTransform(pairs[-1][i], new[-1][i]) for i in (0, 2)], Indicate(L["outline"], color=TEXT, scale_factor=1.02),
                  run_time=0.9)
        self.at("the heart slows")
        self.play(*glow(L["out"], s=1.1, color=TEXT), *[Indicate(t, color=TEXT, scale_factor=1.2) for t in L["glyph"]], run_time=0.8)
        self.at("In the airways")
        self.play(*[ReplacementTransform(pairs[1][i], new[1][i]) for i in (0, 2)], Indicate(R["outline"], color=TEXT, scale_factor=1.02),
                  run_time=0.9)
        self.at("muscle contracts")
        self.play(*glow(R["out"], s=1.1, color=TEXT), R["glyph"].animate.stretch_to_fit_width(3.2).stretch_to_fit_height(0.5), run_time=0.5)
        self.play(R["glyph"].animate.stretch_to_fit_width(1.7).stretch_to_fit_height(0.75), run_time=0.5)

        self.at("is the same")
        self.play(*chip_glow(C.ach, 1.12), *glow(L["a_in"], R["a_in"], s=1.05, color=TEXT), run_time=0.8)
        self.at("are different")
        self.play(*[g for s in (-1, 1) for g in (chip_glow(new[s][0], 1.1, BLUE) + chip_glow(new[s][2], 1.1, PURPLE))], run_time=1.0)

        fade = [C.ach, L["a_in"], R["a_in"], L["a_out"], R["a_out"], L["out"], R["out"], L["glyph"], R["glyph"], L["name"], R["name"]]
        self.at("keep this rule")
        self.play(*[m.animate.set_opacity(0.3) for m in fade], run_time=0.7)
        self.at("decide")
        self.play(*[g for s in (-1, 1) for g in (chip_glow(new[s][0], 1.15, TEXT) + chip_glow(new[s][2], 1.15, TEXT))], run_time=1.0)
        x1 = strike(C.ach)
        self.at("not the signal")
        self.play(Create(x1), run_time=0.5)
        self.finish()


class S07End(EndCard):
    LINE = "The receptor, G protein and downstream proteins decide, not the signal."
