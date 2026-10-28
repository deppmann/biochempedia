"""Notch: the receptor is the message  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  ORANGE = the ligand, fixed in the sending cell's membrane
  BLUE   = the Notch receptor: outer part, lock, stub (everything that stays outside or in the membrane)
  YELLOW = the receptor's inner part (NICD), and the message it carries once freed
  PURPLE = enzymes: the cutting proteases, and the enzymes of the kinase cascade
  TEAL   = CSL, the protein already sitting on the target genes
  RED    = off / stop: co-repressors, genes that are off, crossed-out boxes
  GREEN  = on: Mastermind, genes that are on
  GOLD   = numbered badges for the three cuts
  GREY   = cells, membranes, DNA, outlines, de-emphasized
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"

# ---------------------------------------------------------------------------------------------
# geometry of the contact stage (sender on top, receiver below), shared by scenes 1-4
# ---------------------------------------------------------------------------------------------
X0 = -1.2                  # x of the ligand/receptor pair
RW = 0.5                   # rod width
XR = X0 + 0.27             # receptor rod (right)
XL = X0 - 0.27             # ligand rod (left)
YS, YR, MT = 2.15, -1.75, 0.5       # sender membrane, receiver membrane (centres), membrane thickness
LL = 1.85                  # ligand length
YTIP = 0.9                 # tip of the receptor's outer part
YSITE = YR + MT / 2 + 0.45  # the hidden cut spot
PULL = 0.65                # how far the pull draws the ligand in
SEAMY = -0.25              # where the first cut (made while the receptor was built) sits on the outer part, before the pull
BX0, BX1 = -6.2, 6.2       # x range of the two cells at the contact stage
NX1 = 3.8                  # right edge of the cells in scene 1, before they widen
SLIDE = 2.4                # how far the receiving cell sits from the ligand in scene 1
PEEL = [np.array([0.85, 0.12, 0.0]), np.array([-0.85, 0.0, 0.0]), np.array([0.85, -0.12, 0.0])]
DZ = 3.0                   # scene 3 lifts the receiver by this much once the outer part has gone
SH4 = 4.7                  # total lift by the middle of scene 4 (membrane at the top, nucleus below)


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=26, **kw):
    """chip with an opaque backing so lines drawn behind it do not show through."""
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def badge(n, r=0.22):
    c = Circle(radius=r, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=1)
    return VGroup(c, T(str(n), 24, BG, weight=BOLD).move_to(c))


def pulse_badge(b, k=1.3):
    """a short swell and return that keeps the number readable (Indicate would recolor it into the badge)."""
    return Succession(b.animate(run_time=0.2).scale(k), b.animate(run_time=0.2).scale(1 / k))


def xmark(center, s=0.28, color=RED, w=7):
    cx, cy = center[0], center[1]
    return VGroup(Line([cx - s, cy - s, 0], [cx + s, cy + s, 0], color=color, stroke_width=w),
                  Line([cx - s, cy + s, 0], [cx + s, cy - s, 0], color=color, stroke_width=w))


def rect(x, y0, y1, color, w=RW, op=0.85):
    return Rectangle(width=w, height=y1 - y0, stroke_width=0, fill_color=color, fill_opacity=op).move_to([x, (y0 + y1) / 2, 0])


def mem_bar(y, x0=BX0, x1=BX1, h=MT):
    m = RoundedRectangle(corner_radius=0.12, width=x1 - x0, height=h, stroke_color=GREY, stroke_width=3,
                         fill_color=GREY, fill_opacity=0.35).move_to([(x0 + x1) / 2, y, 0])
    return m.set_z_index(-1)


def cell_body(y_edge, y_far, x0=BX0, x1=BX1):
    lo, hi = sorted((y_edge, y_far))
    b = Rectangle(width=x1 - x0, height=hi - lo, stroke_width=0, fill_color=GREY, fill_opacity=0.07)
    return b.move_to([(x0 + x1) / 2, (lo + hi) / 2, 0]).set_z_index(-2)


def inner_piece(x, ytop, k=1.0):
    """the receptor's inner part: a short stalk (inside the membrane) and a rounded domain below it."""
    stalk = rect(x, ytop - 0.35 * k, ytop, YELLOW, w=RW * k)
    blob = RoundedRectangle(corner_radius=0.28 * k, width=1.1 * k, height=0.7 * k, stroke_width=0,
                            fill_color=YELLOW, fill_opacity=0.9).move_to([x, ytop - 0.66 * k, 0])
    return VGroup(stalk, blob)


def pill(y):
    """one small module of the lock; the opaque back hides what lies behind it."""
    back = RoundedRectangle(corner_radius=0.12, width=1.4, height=0.24, stroke_width=0, fill_color=BG, fill_opacity=1)
    front = RoundedRectangle(corner_radius=0.12, width=1.4, height=0.24, stroke_color=BLUE, stroke_width=3,
                             fill_color=BLUE, fill_opacity=0.5)
    return VGroup(back, front).move_to([XR, y, 0])


def vesicle_at(c):
    return Circle(radius=0.5, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.15).move_to(c).set_z_index(1)


def cargo_at(c):
    """what sits inside the vesicle after the outer part has left with the ligand."""
    far = Rectangle(width=RW * 0.3, height=(YTIP - YSITE) * 0.3, stroke_width=0, fill_color=BLUE, fill_opacity=0.85).move_to(c + LEFT * 0.13)
    lig = Rectangle(width=RW * 0.3, height=LL * 0.3, stroke_width=0, fill_color=ORANGE, fill_opacity=0.85).move_to(c + RIGHT * 0.13)
    return VGroup(far, lig).set_z_index(2)


def stage(pulled=False, wide=True):
    """the contact stage as dict of named parts. pulled=True is the state at the end of scene 2."""
    d = PULL if pulled else 0.0
    S = {}
    x1 = BX1 if wide else NX1
    S["sbody"] = cell_body(YS + MT / 2, 3.5, BX0, x1)
    S["smem"] = mem_bar(YS, BX0, x1)
    S["rbody"] = cell_body(YR - MT / 2, -3.5, BX0, x1)
    S["rmem"] = mem_bar(YR, BX0, x1)
    S["lig"] = rect(XL, YS - MT / 2 - LL + d, YS + d, ORANGE)
    S["stub"] = rect(XR, YR, YSITE, BLUE)
    S["far"] = rect(XR, YSITE + d, YTIP + d, BLUE)
    S["inner"] = inner_piece(XR, YR)
    S["seam"] = Line([XR - 0.3, SEAMY + d, 0], [XR + 0.3, SEAMY + d, 0], color=BG, stroke_width=5).set_z_index(3)
    S["site"] = Dot([XR, YSITE, 0], radius=0.1, color=TEXT)
    S["pills"] = [pill(YSITE + 0.26), pill(YSITE), pill(YSITE - 0.26)]
    S["neck"] = None
    S["ves"] = None
    S["ring"] = None
    if pulled:
        for p, v in zip(S["pills"], PEEL):
            p.shift(v)
        S["neck"] = Line([XR, YSITE, 0], [XR, YSITE + d, 0], color=BLUE, stroke_width=5)
        S["ves"] = vesicle_at([XL, YS + d, 0])
        S["ring"] = Circle(radius=0.2, stroke_color=TEXT, stroke_width=3).move_to([XR, YSITE, 0])
    return S


LBL_SC = [-5.0, 2.95, 0]
LBL_RC = [-4.85, -3.0, 0]
LBL_LIG = [XL - 1.95, 1.1, 0]
LBL_REC = [XR + 1.5, 0.4, 0]


def cell_labels():
    return (T("sending cell", 24, GREY).move_to(LBL_SC), T("receiving cell", 24, GREY).move_to(LBL_RC))


class S00Title(TitleCard):
    LESSON = "Notch: Signaling by Contact and by Cutting"
    TITLE = "The receptor is the message"


# ---------------------------------------------------------------------------------------------
class S01Message(SpokenScene):
    """a row of cells without Notch -> a not-you message that cannot cross -> ligand and receptor fixed in two
    membranes -> they meet only where the cells touch."""

    def construct(self):
        xs = [-5.0 + 2.0 * i for i in range(6)]
        cells = VGroup(*[RoundedRectangle(corner_radius=0.3, width=1.7, height=1.7, stroke_color=GREY, stroke_width=3,
                                          fill_color=GREY, fill_opacity=0.08).move_to([x, -0.1, 0]) for x in xs])
        head = T("without Notch", 38, font=TITLE_FONT).move_to([0, 2.2, 0])
        self.play(FadeIn(head, shift=DOWN * 0.1), LaggedStart(*[Create(c) for c in cells], lag_ratio=0.12), run_time=1.3)

        self.at("too much nervous system")
        nerve = [T("nerve", 26).move_to(cells[i]) for i in (0, 1, 2, 4, 5)]
        self.play(LaggedStart(*[FadeIn(m, scale=0.85) for m in nerve], lag_ratio=0.12), run_time=1.0)
        self.at("too little skin")
        skin = T("skin", 26, GREY).move_to(cells[3])
        self.play(FadeIn(skin, scale=0.85), run_time=0.5)

        # two neighbours remain
        self.at("lets a cell")
        L = RoundedRectangle(corner_radius=0.5, width=5.7, height=4.6, stroke_color=GREY, stroke_width=3,
                             fill_color=GREY, fill_opacity=0.08).move_to([-2.95, -0.2, 0])
        R = L.copy().move_to([2.95, -0.2, 0])
        self.play(FadeOut(head), *[FadeOut(m) for m in (*nerve, skin)], *[FadeOut(cells[i]) for i in (0, 1, 4, 5)],
                  Transform(cells[2], L), Transform(cells[3], R), run_time=1.0)
        msg = chip("not you", YELLOW, size=36).move_to([-3.2, -0.2, 0])
        path = arr([-1.85, -0.2, 0], [1.5, -0.2, 0], YELLOW)
        self.at("not you")
        self.play(FadeIn(msg, scale=0.8), GrowArrow(path), run_time=0.6)

        # the message cannot cross
        self.at("never leaves")
        cross = xmark([0.0, -0.2, 0])
        self.play(FadeOut(path), msg.animate.shift(RIGHT * 1.45), run_time=0.6)
        self.play(Create(cross), run_time=0.3)
        qbox = DashedVMobject(RoundedRectangle(corner_radius=0.2, width=1.5, height=1.3), num_dashes=30).set_color(GREY).move_to([2.95, -0.2, 0])
        q = T("?", 64, YELLOW).move_to(qbox)
        self.play(msg.animate.shift(LEFT * 1.45), Create(qbox), FadeIn(q), run_time=0.7)

        # ligand and receptor, each fixed in its own cell's membrane
        S = stage(False, wide=False)
        W = stage(False)
        recv = ["rbody", "rmem", "stub", "far", "seam", "inner", "site"]
        lbl_sc, lbl_rc = cell_labels()
        lbl_lig = T("ligand", 26, ORANGE).move_to(LBL_LIG)
        lbl_rec = T("receptor", 26, BLUE).move_to(LBL_REC)
        shift = RIGHT * SLIDE
        for k in recv:
            S[k].shift(shift)
        for p in S["pills"]:
            p.shift(shift)
        lbl_rc.shift(shift)
        lbl_rec.shift(shift)
        self.at("The ligand is")
        self.play(FadeOut(msg), FadeOut(cross), FadeOut(qbox), FadeOut(q),
                  ReplacementTransform(cells[2], S["sbody"]), ReplacementTransform(cells[3], S["rbody"]),
                  run_time=0.9)
        self.play(Create(S["smem"]), Create(S["rmem"]), FadeIn(lbl_sc), FadeIn(lbl_rc), run_time=0.7)
        self.at("fixed in that")
        self.play(GrowFromPoint(S["lig"], [XL, YS, 0]), FadeIn(lbl_lig), run_time=0.8)
        self.at("receptor is fixed")
        self.play(GrowFromEdge(S["stub"], DOWN), GrowFromEdge(S["far"], DOWN), FadeIn(S["seam"]), FadeIn(S["inner"]), FadeIn(S["site"]),
                  *[FadeIn(p) for p in S["pills"]], FadeIn(lbl_rec), run_time=0.9)

        # they meet only where the cells touch
        grp = VGroup(S["rbody"], S["rmem"], S["stub"], S["far"], S["seam"], S["inner"], S["site"], *S["pills"], lbl_rc, lbl_rec)
        self.at("usually meet")
        self.play(grp.animate.shift(LEFT * SLIDE), run_time=0.9)
        ring = RoundedRectangle(corner_radius=0.2, width=1.3, height=1.0, stroke_color=TEXT, stroke_width=3).move_to([X0, 0.5, 0])
        self.at("where cells touch")
        self.play(Create(ring), Transform(S["sbody"], W["sbody"]), Transform(S["smem"], W["smem"]),
                  Transform(S["rbody"], W["rbody"]), Transform(S["rmem"], W["rmem"]), run_time=0.6)
        self.play(FadeOut(ring), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Pull(SpokenScene):
    """zoom on the bound pair: the lock hides the cut spot; the sender draws the ligand inward and the lock peels open."""

    def construct(self):
        S = stage(False)
        lbl_sc, lbl_rc = cell_labels()
        lbl_lig = T("ligand", 26, ORANGE).move_to(LBL_LIG)
        lbl_rec = T("receptor", 26, BLUE).move_to(LBL_REC)
        self.add(S["sbody"], S["smem"], S["rbody"], S["rmem"], S["lig"], S["stub"], S["far"], S["seam"], S["inner"], S["site"],
                 *S["pills"], lbl_sc, lbl_rc, lbl_lig, lbl_rec)

        ring = RoundedRectangle(corner_radius=0.2, width=1.3, height=1.0, stroke_color=TEXT, stroke_width=3).move_to([X0, 0.5, 0])
        self.at("Binding is not enough")
        self.play(Create(ring), run_time=0.5)
        self.play(FadeOut(ring), run_time=0.5)

        lock_lbl = T("lock", 26, BLUE).move_to([XR - 2.9, YSITE, 0])
        lock_ln = Line([XR - 2.55, YSITE, 0], [XR - 0.75, YSITE, 0], color=BLUE, stroke_width=2)
        self.at("folded into a lock")
        self.play(FadeIn(lock_lbl), Create(lock_ln), Indicate(VGroup(*S["pills"]), color=BLUE, scale_factor=1.12), run_time=0.8)
        spot = DashedVMobject(Circle(radius=0.7).move_to([XR, YSITE, 0]), num_dashes=24).set_color(TEXT)
        spot_lbl = T("cut spot", 24, TEXT).move_to([XR + 2.9, YSITE, 0])
        spot_ln = Line([XR + 0.72, YSITE, 0], [spot_lbl.get_left()[0] - 0.08, YSITE, 0], color=TEXT, stroke_width=2)
        self.at("hides the spot")
        self.play(Create(spot), FadeIn(spot_lbl), Create(spot_ln), run_time=0.7)

        pull = Arrow([XL - 0.6, 0.2, 0], [XL - 0.6, 1.3, 0], buff=0, color=TEXT, stroke_width=6, tip_length=0.25)
        self.at("must be pulled")
        self.play(GrowArrow(pull), run_time=0.6)

        ves = vesicle_at([XL, YS, 0])
        self.at("draws its ligand")
        self.play(FadeIn(ves, scale=0.8), run_time=0.3)
        self.play(S["lig"].animate.shift(UP * 0.3), ves.animate.shift(UP * 0.3), S["far"].animate.shift(UP * 0.3),
                  S["seam"].animate.shift(UP * 0.3), run_time=0.7)
        self.at("the tug passes")
        self.play(Indicate(S["far"], color=BLUE, scale_factor=1.1), Indicate(pull, color=TEXT, scale_factor=1.1), run_time=0.7)

        neck = always_redraw(lambda: Line([XR, YSITE, 0], [XR, S["far"].get_bottom()[1], 0], color=BLUE, stroke_width=5))
        self.add(neck)
        neck.set_z_index(-0.5)
        small = Circle(radius=0.2, stroke_color=TEXT, stroke_width=3).move_to([XR, YSITE, 0])
        self.at("peels the lock open")
        peel = [p.animate.shift(v) for p, v in zip(S["pills"], PEEL)]
        self.play(S["lig"].animate.shift(UP * 0.35), ves.animate.shift(UP * 0.35), S["far"].animate.shift(UP * 0.35),
                  S["seam"].animate.shift(UP * 0.35), *peel, FadeOut(lock_lbl), FadeOut(lock_ln), run_time=0.9)
        self.play(Transform(spot, small), FadeOut(spot_lbl), FadeOut(spot_ln), FadeOut(pull), run_time=0.6)
        self.play(Indicate(S["site"], color=TEXT, scale_factor=1.8), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Cuts(SpokenScene):
    """three numbered cuts: a seam from before, the ADAM cut at the spot, the gamma-secretase cut in the membrane."""

    def construct(self):
        S = stage(True)
        lbl_sc, lbl_rc = cell_labels()
        lbl_lig = T("ligand", 26, ORANGE).move_to(LBL_LIG)
        for k in ("sbody", "smem", "rbody", "rmem", "lig", "stub", "far", "seam", "inner", "site"):
            self.add(S[k])
        self.add(S["neck"], *S["pills"], S["ves"], S["ring"], lbl_sc, lbl_rc, lbl_lig)
        S["stub"].set_z_index(2)
        S["inner"].set_z_index(2)
        S["ring"].set_z_index(3)

        # first cut: already there (drawn since the receptor first appeared); the narration only points at it
        seam = S["seam"]
        seam_y = SEAMY + PULL
        ring1 = Circle(radius=0.42, stroke_color=TEXT, stroke_width=3).move_to([XR, seam_y, 0]).set_z_index(4)
        b1 = badge(1).move_to([XR + 0.95, seam_y, 0])
        note = T("made earlier", 24, GREY).move_to([XR + 2.6, seam_y, 0])
        note2 = T("made earlier, no signal", 24, GREY).move_to([XR + 3.0, seam_y, 0])
        self.at("the first cut")
        self.play(Create(ring1), FadeIn(b1, scale=0.5), run_time=0.6)
        self.at("receptor is made")
        self.play(FadeIn(note), run_time=0.5)
        self.at("no signal")
        self.play(ReplacementTransform(note, note2), pulse_badge(b1), run_time=0.6)

        # second cut: ADAM protease at the exposed spot
        adam = bchip("ADAM protease", PURPLE, 26).move_to([XR + 6.0, YSITE, 0])
        adam_to = [XR + 3.3, YSITE, 0]
        b2 = badge(2)
        self.at("After the pull")
        self.play(FadeOut(b1), FadeOut(note2), FadeOut(ring1), adam.animate.move_to(adam_to), run_time=0.9)
        b2.move_to(adam.get_right() + RIGHT * 0.45)
        link2 = arr(adam.get_left(), [XR + 0.3, YSITE, 0], PURPLE, w=4, tip=0.2)
        self.play(GrowArrow(link2), FadeIn(b2, scale=0.5), run_time=0.5)
        flash = Line([XR - 0.5, YSITE - 0.14, 0], [XR + 0.5, YSITE + 0.14, 0], color=TEXT, stroke_width=8).set_z_index(5)
        self.at("second cut")
        self.play(Create(flash), run_time=0.15)
        self.play(FadeOut(flash), FadeOut(S["neck"]), FadeOut(S["ring"]), FadeOut(S["site"]), FadeOut(link2), run_time=0.25)

        # the outer part leaves with the ligand
        vc = S["ves"].get_center()
        cargo = cargo_at(vc)
        self.at("outer part leaves")
        self.play(ReplacementTransform(S["far"], cargo[0]), ReplacementTransform(S["lig"], cargo[1]),
                  *[p.animate.scale(0.3).move_to(vc) for p in S["pills"]], FadeOut(seam),
                  lbl_lig.animate.move_to([XL + 1.6, vc[1], 0]), run_time=1.1)
        self.remove(*S["pills"])
        # the sender leaves the picture; the receiver rises to the middle of the frame, where the next cut happens
        send_grp = VGroup(S["sbody"], S["smem"], S["ves"], cargo, lbl_sc, lbl_lig)
        rbody2 = cell_body(YR + DZ - MT / 2, -3.5)
        stub_lbl = T("stub", 26, BLUE).move_to([XR - 1.3, YSITE + DZ - 0.2, 0])
        self.at("stub stays")
        self.play(FadeOut(send_grp, shift=UP * DZ), ReplacementTransform(S["rbody"], rbody2),
                  S["rmem"].animate.shift(UP * DZ), S["stub"].animate.shift(UP * DZ), S["inner"].animate.shift(UP * DZ),
                  adam.animate.shift(UP * DZ), b2.animate.shift(UP * DZ), run_time=1.0)
        self.play(FadeIn(stub_lbl), Indicate(S["stub"], color=BLUE, scale_factor=1.25), run_time=0.6)

        # third cut: gamma-secretase inside the membrane
        YR2 = YR + DZ
        ring_g = Ellipse(width=1.7, height=1.1, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=0.2).move_to([XR, YR2, 0])
        ring_g.set_z_index(1)
        gam = bchip("γ-secretase", PURPLE, 28).move_to([XR + 3.3, YR2 - 1.1, 0])
        link3 = Line([XR + 0.8, YR2 - 0.25, 0], gam.get_left(), color=PURPLE, stroke_width=3)
        b3 = badge(3).move_to(gam.get_right() + RIGHT * 0.45)
        self.at("Then")
        self.play(FadeIn(ring_g, scale=0.7), FadeIn(gam, shift=UP * 0.2), Create(link3), FadeIn(b3, scale=0.5), run_time=0.8)
        flash2 = Line([XR - 0.55, YR2, 0], [XR + 0.55, YR2, 0], color=TEXT, stroke_width=8).set_z_index(5)
        self.at("third cut")
        self.play(Create(flash2), run_time=0.15)
        self.play(FadeOut(flash2), run_time=0.2)
        self.at("inside the membrane")
        self.play(S["inner"].animate.shift(DOWN * 0.55), FadeOut(ring_g), FadeOut(stub_lbl), run_time=0.9)

        # why the order cannot change
        order = Arrow(b2.get_bottom() + DOWN * 0.05, b3.get_top() + UP * 0.05, buff=0, color=GOLD, stroke_width=4, tip_length=0.2)
        self.at("comes first")
        self.play(pulse_badge(b2), run_time=0.5)
        self.play(GrowArrow(order), pulse_badge(b3), run_time=0.7)
        self.play(FadeOut(VGroup(adam, b2, gam, b3, link3, order)), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Gene(SpokenScene):
    """the view drops to the nucleus: the inner part (NICD) joins CSL, pushes the co-repressors off, Mastermind arrives, genes on."""

    def construct(self):
        lbl_sc, lbl_rc = cell_labels()
        YR2 = YR + DZ
        rbody = cell_body(YR2 - MT / 2, -3.5)
        rmem = mem_bar(YR2)
        stub = rect(XR, YR2, YSITE + DZ, BLUE).set_z_index(2)
        inner = inner_piece(XR, YR2 - 0.55).set_z_index(2)
        self.add(rbody, rmem, stub, inner, lbl_rc)

        new_body = Rectangle(width=12.4, height=2.74 + 3.5, stroke_width=0, fill_color=GREY, fill_opacity=0.07).move_to([0, (2.74 - 3.5) / 2, 0]).set_z_index(-2)
        new_mem = mem_bar(YR + SH4, -6.2, 6.2)
        nuc = RoundedRectangle(corner_radius=1.0, width=11.0, height=4.3, stroke_color=GREY, stroke_width=4,
                               fill_color=GREY, fill_opacity=0.12).move_to([0, -1.3, 0])
        nuc_lbl = T("nucleus", 26, GREY).move_to([3.7, -3.05, 0])
        inner_lbl = T("inner part", 26, YELLOW).move_to([XR + 1.7, YR + SH4 - 0.55 - 0.5, 0])
        up = UP * (SH4 - DZ)

        self.at("frees the inner part")
        self.play(FadeOut(lbl_rc), ReplacementTransform(rbody, new_body), ReplacementTransform(rmem, new_mem),
                  stub.animate.shift(up), inner.animate.shift(up),
                  FadeIn(nuc, shift=up), FadeIn(nuc_lbl, shift=up), run_time=1.5)
        self.play(FadeIn(inner_lbl), run_time=0.4)
        nicd_lbl = T("NICD", 30, YELLOW, weight=BOLD).move_to(inner_lbl)
        self.at("which is called")
        self.play(ReplacementTransform(inner_lbl, nicd_lbl), Indicate(inner, color=YELLOW, scale_factor=1.15), run_time=0.7)

        # DNA, gene, CSL
        dna = Line([-5.0, -2.35, 0], [5.0, -2.35, 0], color=GREY, stroke_width=4)
        gene = RoundedRectangle(corner_radius=0.14, width=4.6, height=0.55, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.4).move_to([0, -2.35, 0])
        gene_lbl = T("target genes", 28, GREY).move_to([0, -3.0, 0])
        csl = bchip("CSL", TEAL, 36).move_to([0, -1.5, 0])
        nicd = bchip("NICD", YELLOW, 36).move_to([-3.9, -0.55, 0])
        self.at("enters the nucleus")
        self.play(ReplacementTransform(VGroup(inner, nicd_lbl), nicd), run_time=1.2)
        self.at("where")
        self.play(Create(dna), FadeIn(gene), run_time=0.6)
        self.at("binds")
        self.play(FadeIn(csl, shift=DOWN * 0.3), run_time=0.5)
        self.at("target genes")
        self.play(FadeIn(gene_lbl), run_time=0.4)

        # CSL keeps the genes off with co-repressors
        corep = bchip("co-repressors", RED, 32).move_to([0, -0.55, 0])
        off_lbl = T("genes off", 32, RED).move_to([3.8, -1.75, 0])
        self.at("keeps those genes off")
        self.play(gene.animate.set_stroke(RED).set_fill(RED, 0.25), FadeIn(off_lbl), run_time=0.6)
        self.at("off with")
        self.play(FadeIn(corep, shift=DOWN * 0.3), run_time=0.5)

        # NICD binds CSL and pushes the co-repressors off; Mastermind arrives
        self.at("binds", nth=1)
        self.play(nicd.animate.move_to([-3.0, -0.55, 0]), run_time=0.5)
        self.at("displaces the")
        self.play(FadeOut(corep, shift=RIGHT * 3.0 + UP * 0.6), nicd.animate.move_to([-1.3, -0.55, 0]), run_time=0.9)
        mm = bchip("Mastermind", GREEN, 32).move_to([2.1, -0.55, 0])
        self.at("recruits")
        self.play(FadeIn(mm, shift=LEFT * 2.5), run_time=0.9)
        on_lbl = T("genes on", 32, GREEN).move_to([3.8, -1.75, 0])
        self.at("genes turn on")
        self.play(gene.animate.set_stroke(GREEN).set_fill(GREEN, 0.55), ReplacementTransform(off_lbl, on_lbl), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Once(SpokenScene):
    """a kinase cascade fans out 1 -> 3 -> 9; Notch has no relay, and one cut receptor gives one inner part, once."""

    def construct(self):
        TY, BY = 1.75, -2.0
        lab_k = T("kinase cascade", 30, TEXT, weight=BOLD).move_to([-4.4, 3.1, 0])
        e0 = bchip("enzyme", PURPLE, 26).move_to([-5.0, TY, 0])
        ys1 = [TY + 0.95, TY, TY - 0.95]
        d1 = [Dot([-1.8, y, 0], radius=0.2, color=PURPLE) for y in ys1]
        a1 = [arr(e0.get_right(), d.get_left(), PURPLE, w=3, tip=0.16) for d in d1]
        d2, a2 = [], []
        for i, y in enumerate(ys1):
            for dy in (0.3, 0.0, -0.3):
                d2.append(Dot([1.8, y + dy, 0], radius=0.12, color=PURPLE))
        for i, d in enumerate(d2):
            a2.append(arr(d1[i // 3].get_right(), d.get_left(), PURPLE, w=2, tip=0.12))
        grows = T("signal grows", 28, PURPLE).move_to([4.6, TY, 0])

        self.at("In a kinase cascade")
        self.play(FadeIn(lab_k, shift=DOWN * 0.1), FadeIn(e0, shift=RIGHT * 0.2), run_time=0.7)
        self.at("many substrates")
        self.play(LaggedStart(*[AnimationGroup(GrowArrow(a), FadeIn(d, scale=0.5)) for a, d in zip(a1, d1)], lag_ratio=0.2), run_time=0.9)
        self.at("grows at every step")
        self.play(LaggedStart(*[AnimationGroup(GrowArrow(a), FadeIn(d, scale=0.5)) for a, d in zip(a2, d2)], lag_ratio=0.06), FadeIn(grows), run_time=1.3)
        top = VGroup(lab_k, e0, *d1, *a1, *d2, *a2, grows)

        # Notch lane
        lab_n = T("Notch", 30, BLUE, weight=BOLD).move_to([-5.6, -0.65, 0])
        rc = bchip("receptor", BLUE, 26).move_to([-4.7, BY, 0])
        gene = RoundedRectangle(corner_radius=0.12, width=2.2, height=0.5, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.4).move_to([4.7, BY, 0])
        gene_lbl = T("gene", 24, GREY).move_to([4.7, BY - 0.6, 0])
        line = arr(rc.get_right() + RIGHT * 0.1, gene.get_left() + LEFT * 0.1, GREY, w=4)

        def ghost(text, x):
            lab = T(text, 24, GREY)
            box = DashedVMobject(RoundedRectangle(corner_radius=0.14, width=lab.width + 0.5, height=0.7), num_dashes=36).set_color(GREY)
            g = VGroup(box, lab).move_to([x, -0.6, 0])
            return g, xmark([g.get_right()[0], g.get_top()[1], 0], 0.2, RED, 6)

        g1, x1 = ghost("second messenger", -1.4)
        g2, x2 = ghost("kinase relay", 2.2)
        self.at("has no second")
        self.play(top.animate.set_opacity(0.3), FadeIn(lab_n), FadeIn(rc, shift=RIGHT * 0.2), run_time=0.7)
        self.play(FadeIn(g1, shift=DOWN * 0.1), run_time=0.4)
        self.play(Create(x1), run_time=0.3)
        self.at("kinase relay")
        self.play(FadeIn(g2, shift=DOWN * 0.1), run_time=0.4)
        self.play(Create(x2), run_time=0.3)
        self.at("Between the membrane")
        self.play(GrowArrow(line), FadeIn(gene), FadeIn(gene_lbl), run_time=0.8)
        self.at("nothing multiplies")
        self.play(Indicate(line, color=TEXT, scale_factor=1.0), run_time=0.7)

        cut = Line(rc.get_corner(DL) + [0.1, 0.05, 0], rc.get_corner(UR) + [-0.1, -0.05, 0], color=TEXT, stroke_width=6)
        dot = Dot(rc.get_right() + RIGHT * 0.45, radius=0.2, color=YELLOW)
        dlab = T("inner part", 24, YELLOW).next_to(dot, UP, buff=0.18)
        self.at("One cut receptor")
        self.play(Create(cut), run_time=0.25)
        self.play(FadeOut(cut), FadeIn(dot, scale=0.4), FadeIn(dlab, shift=UP * 0.1), run_time=0.5)
        self.at("gives one")
        tgt = gene.get_left() + LEFT * 0.35
        self.play(dot.animate.move_to(tgt), dlab.animate.next_to(np.array([tgt[0], tgt[1], 0]), UP, buff=0.18), run_time=1.3, rate_func=smooth)
        self.play(Indicate(gene, color=YELLOW, scale_factor=1.1), FadeOut(dot), FadeOut(dlab), run_time=0.6)

        used = T("signals once", 26, RED).move_to([-4.7, BY - 0.85, 0])
        self.at("cannot be undone")
        self.play(rc.animate.set_opacity(0.35), run_time=0.6)
        self.at("signals once")
        self.play(FadeIn(used, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Count(SpokenScene):
    """a neighbour pulls two receptors, then two more; each cut sends one inner part to the nucleus and the counters rise
    in step; the rule closes as pull, cut, message."""

    def construct(self):
        XS = [-3.6, -1.8, 0.0, 1.8, 3.6]
        YS6, YR6 = 2.95, 0.75
        W6 = 0.2
        smem = mem_bar(YS6, -6.2, 6.2, h=0.3)
        rmem = mem_bar(YR6, -6.2, 6.2, h=0.3)
        nb_lbl = T("neighbour", 26, GREY).move_to([-5.0, 3.3, 0])
        nuc = RoundedRectangle(corner_radius=0.9, width=9.0, height=2.4, stroke_color=GREY, stroke_width=4,
                               fill_color=GREY, fill_opacity=0.12).move_to([0, -2.25, 0])
        nuc_lbl = T("nucleus", 24, GREY).move_to([3.0, -3.0, 0])
        ligs = [rect(x + 0.11, YS6 - 0.15 - 1.0, YS6, ORANGE, w=W6) for x in XS]
        stubs = [rect(x - 0.11, YR6, YR6 + 0.35, BLUE, w=W6) for x in XS]
        fars = [rect(x - 0.11, YR6 + 0.35, YR6 + 1.3, BLUE, w=W6) for x in XS]
        inns = [inner_piece(x - 0.11, YR6, k=0.55) for x in XS]
        for m in ligs + stubs + fars + inns:
            m.set_z_index(1)

        c1_lbl = T("pulled\nand cut", 24, TEXT, line_spacing=0.8).move_to([-5.4, -0.1, 0])
        c2_lbl = T("parts\nmade", 24, YELLOW, line_spacing=0.8).move_to([-5.4, -1.75, 0])

        def num(n, color, y):
            return M(str(n), 48, color).move_to([-5.4, y, 0])

        n1, n2 = num(0, TEXT, -0.85), num(0, YELLOW, -2.65)

        # the stage appears
        self.play(FadeIn(smem), FadeIn(rmem), FadeIn(nb_lbl), FadeIn(nuc), FadeIn(nuc_lbl), run_time=0.7)
        self.play(LaggedStart(*[AnimationGroup(FadeIn(l), FadeIn(s), FadeIn(f), FadeIn(i)) for l, s, f, i in zip(ligs, stubs, fars, inns)],
                              lag_ratio=0.1), run_time=0.9)
        self.at("a count")
        self.play(FadeIn(c1_lbl), FadeIn(n1), FadeIn(c2_lbl), FadeIn(n2), run_time=0.6)

        state = {"n": 0, "n1": n1, "n2": n2}
        slots = [[-1.4 + 0.7 * k, -2.0, 0] for k in range(5)]

        def pull_cut(i):
            """receptor i is pulled and cut: the outer part leaves with the ligand, the inner part falls to the nucleus."""
            k = state["n"] + 1
            flash = Line([XS[i] - 0.3, YR6 + 0.35, 0], [XS[i] + 0.1, YR6 + 0.35, 0], color=TEXT, stroke_width=6)
            self.play(ligs[i].animate.shift(UP * 0.45).set_opacity(0), fars[i].animate.shift(UP * 0.45).set_opacity(0),
                      Create(flash), run_time=0.3)
            self.remove(flash)
            dot = Dot(slots[state["n"]], radius=0.2, color=YELLOW)
            m1, m2 = num(k, TEXT, -0.85), num(k, YELLOW, -2.65)
            self.play(ReplacementTransform(inns[i], dot), ReplacementTransform(state["n1"], m1),
                      ReplacementTransform(state["n2"], m2), run_time=0.35)
            state["n"], state["n1"], state["n2"] = k, m1, m2

        self.at("one for one")
        pull_cut(0)
        pull_cut(1)
        self.at("has pulled")
        pull_cut(2)
        pull_cut(3)

        touch = DoubleArrow([4.75, 0.95, 0], [4.75, 2.8, 0], color=TEXT, stroke_width=4, tip_length=0.18, buff=0)
        touch_lbl = T("cells\ntouch", 24, TEXT, line_spacing=0.8).move_to([5.65, 1.9, 0])
        self.at("A cell mostly")
        self.play(GrowArrow(touch), FadeIn(touch_lbl), run_time=0.7)

        # the rule
        rest = [m for m in self.mobjects]
        c_rec = chip("one receptor", BLUE, 34)
        c_cut = chip("pulled and cut", PURPLE, 34)
        c_inn = chip("one inner part", YELLOW, 34)
        c_msg = chip("one message", YELLOW, 34)
        row = VGroup(c_rec, c_cut, c_inn).arrange(RIGHT, buff=0.85).move_to([0, 0.9, 0])
        w0 = row.width
        fit(row)
        c_msg.scale(row.width / w0).move_to([c_inn.get_center()[0], -1.3, 0])
        a1 = arr(c_rec.get_right(), c_cut.get_left(), GREY)
        a2 = arr(c_cut.get_right(), c_inn.get_left(), GREY)
        a3 = arr(c_inn.get_bottom(), c_msg.get_top(), YELLOW)
        self.at("one receptor", lead=0.8)
        self.play(*[FadeOut(m) for m in rest], run_time=0.4)
        self.at("one receptor")
        self.play(FadeIn(c_rec, shift=UP * 0.15), run_time=0.5)
        self.at("pulled and cut", nth=1)
        self.play(GrowArrow(a1), FadeIn(c_cut, shift=UP * 0.15), run_time=0.5)
        self.at("gives one")
        self.play(GrowArrow(a2), FadeIn(c_inn, shift=UP * 0.15), run_time=0.5)
        self.at("one message")
        self.play(GrowArrow(a3), FadeIn(c_msg, shift=UP * 0.15), run_time=0.5)
        self.finish()


class S07End(EndCard):
    LINE = "One receptor pulled and cut, one message."
