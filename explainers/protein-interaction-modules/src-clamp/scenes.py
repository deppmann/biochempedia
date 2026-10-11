"""Protein modules: Src holds itself off with its own SH2 and SH3 (Biochemistrypedia section film).
Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = the reading domains, SH2 and SH3, and the cups that close on their targets
  PURPLE = the kinase domain
  GREY   = structure: membrane, linker, tail, labels
  ORANGE = a tyrosine (527 on the tail, 416 on the activation loop)
  GOLD   = a phosphate badge
  TEAL   = Csk, the enzyme that phosphorylates tyrosine 527
  YELLOW = a better ligand that takes a domain (PDGF receptor, FAK, beta-arrestin)
  RED    = inactive / the lost off-switch
  GREEN  = active
No molecular structures: domains are labelled chips, grips are open cups, the tail is a line.
Everything is a schematic and is marked "schematic, not to scale".
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"

MEM_Y = -2.85
KC = np.array([1.2, -0.3, 0])          # kinase centre, folded
SH2P = np.array([-1.75, 0.45, 0])
SH3P = np.array([-1.75, -1.0, 0])
CUP2 = np.array([-1.75, 1.2, 0])       # SH2 cup centre (mouth up)
CUP3 = np.array([-2.78, -1.0, 0])      # SH3 cup centre (mouth left)
LINK_CLOSED = np.array([-3.5, -1.0, 0])
LINK_FREE = np.array([-4.4, 0.35, 0])
STAT = np.array([5.0, -0.3, 0])


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def pbadge(r=0.19):
    c = Circle(radius=r, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=1)
    return VGroup(c, T("P", 22, BG, weight=BOLD).move_to(c))


def ynode(letter="Y", color=ORANGE, r=0.27):
    c = Circle(radius=r, stroke_color=color, stroke_width=3.5, fill_color=color, fill_opacity=0.35)
    return VGroup(c, T(letter, 24, TEXT, weight=BOLD).move_to(c))


def cup(center, mouth, color=BLUE, r=0.5):
    """an open cup (a C shape) whose mouth faces the direction `mouth` (radians)."""
    a = Arc(radius=r, start_angle=mouth + 50 * DEGREES, angle=260 * DEGREES, color=color, stroke_width=7)
    return a.move_arc_center_to(np.array(center, float))


def smooth(pts, color=GREY, w=6):
    m = VMobject(stroke_color=color, stroke_width=w, fill_opacity=0)
    m.set_points_smoothly([np.array([x, y, 0.0]) for x, y in pts])
    return m


TAIL_CLOSED = [(3.5, 0.75), (4.1, 1.0), (4.2, 1.9), (3.6, 2.4), (1.0, 2.45), (-1.2, 2.4), (-1.75, 1.95), (-1.75, 1.47)]
TAIL_FREE = [(3.5, 0.75), (4.1, 0.95), (4.7, 1.35), (5.2, 1.8), (5.55, 2.2), (5.75, 2.6), (5.85, 2.95), (5.9, 3.2)]
# the free tail ends higher than the safe edge allows for a node, so the node sits earlier on the path:
TAIL_FREE = [(3.5, 0.75), (3.9, 0.9), (4.3, 1.1), (4.7, 1.35), (5.0, 1.6), (5.3, 1.85), (5.5, 2.05), (5.65, 2.25)]
NODE_CLOSED = np.array([-1.75, 1.2, 0])
NODE_FREE = np.array([5.65, 2.25, 0])


def membrane():
    bar = RoundedRectangle(corner_radius=0.1, width=12.4, height=0.3, stroke_color=GREY, stroke_width=3,
                           fill_color=GREY, fill_opacity=0.35).move_to([0, MEM_Y, 0])
    lbl = T("inner face of the plasma membrane", 22, GREY).move_to([-3.0, MEM_Y - 0.5, 0])
    note = T("schematic, not to scale", 22, GREY).move_to([4.2, MEM_Y - 0.5, 0])
    return bar, lbl, note


def kin_fold(active=False):
    rect = RoundedRectangle(corner_radius=0.3, width=4.6, height=2.8, stroke_color=PURPLE, stroke_width=4,
                            fill_color=PURPLE, fill_opacity=0.42 if active else 0.14).move_to(KC)
    lbl = T("kinase", 30, PURPLE).move_to(KC + UP * 0.8)
    return VGroup(rect, lbl)


def status(text, color):
    c = chip(text, color, size=26)
    return c.move_to(STAT)


def link_chip(pos):
    return chip("linker", GREY, size=24, pad=0.13).move_to(pos)


def row_parts():
    """the unfolded chain in a row: SH3 SH2 linker kinase tail + the tyrosine node."""
    sh3 = chip("SH3", BLUE, 26)
    sh2 = chip("SH2", BLUE, 26)
    lk = chip("linker", GREY, 24, pad=0.13)
    kd = chip("kinase domain", PURPLE, 26)
    tl = chip("tail", GREY, 24, pad=0.13)
    yn = ynode()
    row = VGroup(sh3, sh2, lk, kd, tl, yn).arrange(RIGHT, buff=0.1).move_to([0.45, 0.3, 0])
    return dict(sh3=sh3, sh2=sh2, lk=lk, kd=kd, tl=tl, yn=yn, row=row)


def myr_line(top):
    """the myristate anchor: a line from the SH3 chip down to the membrane."""
    x = top[0]
    return Line([x, top[1], 0], [x, MEM_Y + 0.15, 0], color=GREY, stroke_width=5)


def myr_label(x, ytop):
    return T("myristate", 22, GREY).move_to([x + 1.0, (ytop + MEM_Y) / 2 - 0.1, 0])


def partner(label, tip=CUP2, color=YELLOW, with_badge=False, extra=None):
    """a better ligand: a chip with a stalk whose tip sits in the cup at `tip`."""
    c = chip(label, color, size=24)
    s_end = tip + np.array([-0.34, 0.94, 0]) * 1.0
    c.move_to(s_end + LEFT * (0.1 + c.width / 2))
    stalk = Line(c.get_right() + RIGHT * 0.0, tip, color=color, stroke_width=5)
    g = VGroup(stalk, c)
    if with_badge:
        b = pbadge(0.19).move_to(tip)
        g.add(b)
    return g


class Film(SpokenScene):
    def outro(self, *anims, run_time=0.4):
        rest = self.narration_s - 0.02 - self.elapsed()
        if rest > 0:
            self.wait(rest)
        if anims:
            self.play(*anims, run_time=run_time)
        self.finish()


class S00Title(TitleCard):
    LESSON = "Protein Modules: SH2, SH3, PTB, PDZ and PH"
    TITLE = "A protein that clamps itself off"


# ---------------------------------------------------------------------------------------------
class S01Parts(Film):
    """a bare bar and a question; it fills in with the parts of Src in the order named."""

    def construct(self):
        bar, mlbl, note = membrane()
        R = row_parts()
        row = R["row"]
        ghost = RoundedRectangle(corner_radius=0.25, width=row.width + 0.4, height=row.height + 0.5,
                                 stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.08).move_to(row)
        glbl = T("Src", 34, TEXT, weight=BOLD).move_to(ghost.get_corner(UR) + np.array([-0.7, 0.45, 0]))
        top_y = ghost.get_top()[1] + 0.25
        loop = ArcBetweenPoints(np.array([2.8, top_y, 0]), np.array([-3.4, top_y, 0]), angle=PI / 3,
                                color=YELLOW, stroke_width=5).add_tip(tip_length=0.25)
        q = T("?", 60, YELLOW, weight=BOLD).move_to([0.1, top_y + 1.05, 0])
        self.add(bar, mlbl, note)
        self.play(FadeIn(ghost), FadeIn(glbl), run_time=0.7)
        self.at("read its own tail")
        self.play(Create(loop), FadeIn(q, scale=0.6), run_time=0.9)
        self.play(Indicate(q, color=YELLOW, scale_factor=1.25), run_time=0.6)

        self.at("fatty acid")
        self.play(FadeOut(VGroup(q, loop)), run_time=0.4)

        # myristate anchor
        top = R["sh3"].get_bottom()
        line = myr_line([top[0], ghost.get_bottom()[1]])
        mlab = myr_label(top[0], ghost.get_bottom()[1])
        self.play(Create(line), FadeIn(mlab), run_time=0.8)
        self.at("inner face")
        self.play(Indicate(bar, color=GREY, scale_factor=1.0), run_time=0.7)

        self.at("Then come")
        self.play(FadeIn(R["sh3"], scale=0.8), run_time=0.45)
        self.wait(0.5)
        self.play(FadeIn(R["sh2"], scale=0.8), run_time=0.45)
        self.at("a linker")
        self.play(FadeIn(R["lk"], scale=0.8), run_time=0.45)
        self.at("kinase domain")
        self.play(FadeIn(R["kd"], scale=0.9), run_time=0.5)
        self.at("short tail")
        self.play(FadeIn(R["tl"], scale=0.9), run_time=0.45)
        self.at("tail ends")
        yn = R["yn"]
        yl = T("tyrosine 527", 26, ORANGE).next_to(yn, DOWN, buff=0.45)
        yl.move_to([min(yl.get_center()[0], 4.6), yl.get_center()[1], 0])
        cn = T("chicken numbering", 22, GREY).next_to(yl, DOWN, buff=0.12)
        ar = Arrow(yl.get_top() + UP * 0.02, yn.get_bottom(), buff=0.05, color=ORANGE, stroke_width=4, tip_length=0.15)
        self.play(FadeIn(yn, scale=0.5), FadeIn(yl), GrowArrow(ar), run_time=0.6)
        self.play(FadeIn(cn), run_time=0.4)
        self.outro()


# ---------------------------------------------------------------------------------------------
class S02Clamp(Film):
    """Csk phosphorylates the tail; the chain folds; the SH2 cup closes on the phosphotyrosine and the SH3 cup on the linker."""

    def construct(self):
        bar, mlbl, note = membrane()
        R = row_parts()
        row = R["row"]
        ghost = RoundedRectangle(corner_radius=0.25, width=row.width + 0.4, height=row.height + 0.5,
                                 stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.08).move_to(row)
        top = R["sh3"].get_bottom()
        line = myr_line([top[0], ghost.get_bottom()[1]])
        mlab = myr_label(top[0], ghost.get_bottom()[1])
        yn = R["yn"]
        yl = T("tyrosine 527", 26, ORANGE).next_to(yn, DOWN, buff=0.45)
        yl.move_to([min(yl.get_center()[0], 4.6), yl.get_center()[1], 0])
        self.add(bar, mlbl, note, ghost, R["sh3"], R["sh2"], R["lk"], R["kd"], R["tl"], yn, yl, line, mlab)

        # --- Csk puts a phosphate on the tyrosine ----------------------------------------------------
        csk = chip("Csk", TEAL, 28).move_to(yn.get_center() + UP * 1.5 + LEFT * 0.2)
        carr = Arrow(csk.get_bottom(), yn.get_top() + UP * 0.05, buff=0.05, color=TEAL, stroke_width=5, tip_length=0.2)
        self.at("enzyme")
        self.play(FadeIn(csk, shift=DOWN * 0.2), run_time=0.5)
        self.at("puts a phosphate")
        self.play(GrowArrow(carr), run_time=0.35)
        pb = pbadge().move_to(yn.get_center() + np.array([0.3, 0.3, 0]))
        self.play(FadeIn(pb, scale=0.4), run_time=0.4)
        self.wait(0.3)

        # --- the tail folds back ----------------------------------------------------------------
        sh3 = chip("SH3", BLUE, 26).move_to(SH3P)
        sh2 = chip("SH2", BLUE, 26).move_to(SH2P)
        lk = link_chip(LINK_CLOSED)
        kin = kin_fold()
        tail = smooth(TAIL_CLOSED)
        nodeg = VGroup(yn, pb)
        top3 = SH3P + DOWN * 0.3
        myr2 = myr_line([SH3P[0], SH3P[1] - 0.3])
        mlab2 = myr_label(SH3P[0], SH3P[1] - 0.3)
        mlab2.move_to([SH3P[0] + 1.0, (SH3P[1] - 0.3 + MEM_Y) / 2 - 0.05, 0])
        # a short path for the node: it follows the tail as it is drawn
        self.at("folds back")
        self.play(FadeOut(VGroup(csk, carr, yl, ghost)),
                  ReplacementTransform(R["sh3"], sh3), ReplacementTransform(R["sh2"], sh2),
                  ReplacementTransform(R["lk"], lk), ReplacementTransform(R["kd"], kin),
                  ReplacementTransform(line, myr2), ReplacementTransform(mlab, mlab2),
                  FadeOut(R["tl"]), run_time=1.4)
        self.play(Create(tail, rate_func=linear), MoveAlongPath(nodeg, tail, rate_func=linear), run_time=1.5)
        nodeg.move_to(NODE_CLOSED + np.array([0.0, 0.0, 0.0]))
        # keep the badge on the node's corner
        nodeg[1].move_to(nodeg[0].get_center() + np.array([0.3, 0.3, 0]))

        # --- the two grips ----------------------------------------------------------------------
        c2 = cup(CUP2, PI / 2)
        c3 = cup(CUP3, PI)
        self.at("grips the", nth=0)
        self.play(Create(c2), run_time=0.5)
        self.play(Indicate(c2, color=BLUE, scale_factor=1.12), run_time=0.5)
        self.at("grips the", nth=1)
        self.play(Create(c3), run_time=0.5)
        self.play(Indicate(c3, color=BLUE, scale_factor=1.12), run_time=0.5)
        self.at("back of the kinase")
        self.play(Indicate(kin[0], color=PURPLE, scale_factor=1.03), run_time=0.6)
        st = status("inactive", RED)
        self.at("hold it")
        self.play(FadeIn(st, shift=LEFT * 0.2), run_time=0.5)
        self.outro()


# ---------------------------------------------------------------------------------------------
def closed_src(scene, active=False):
    """rebuild the folded, clamped Src exactly as scene 2 leaves it; returns the pieces."""
    bar, mlbl, note = membrane()
    kin = kin_fold(active)
    sh2 = chip("SH2", BLUE, 26).move_to(SH2P)
    sh3 = chip("SH3", BLUE, 26).move_to(SH3P)
    lk = link_chip(LINK_CLOSED)
    myr = myr_line([SH3P[0], SH3P[1] - 0.3])
    ml = myr_label(SH3P[0], SH3P[1] - 0.3)
    ml.move_to([SH3P[0] + 1.0, (SH3P[1] - 0.3 + MEM_Y) / 2 - 0.05, 0])
    tail = smooth(TAIL_CLOSED)
    yn = ynode().move_to(NODE_CLOSED)
    pb = pbadge().move_to(yn.get_center() + np.array([0.3, 0.3, 0]))
    c2 = cup(CUP2, PI / 2)
    c3 = cup(CUP3, PI)
    st = status("inactive", RED)
    scene.add(bar, mlbl, note, kin, sh2, sh3, lk, myr, ml, tail, yn, pb, c2, c3, st)
    return dict(bar=bar, kin=kin, sh2=sh2, sh3=sh3, lk=lk, myr=myr, ml=ml, tail=tail, yn=yn, pb=pb, c2=c2, c3=c3, st=st)


class S03Open(Film):
    """the loose clamp: better ligands take the SH2 and SH3 cups; tyrosine 416 gets a phosphate; the kinase is active."""

    def construct(self):
        P = closed_src(self)
        loose = T("loose clamp", 26, GREY).move_to([1.2, 2.95, 0])
        self.at("deliberately loose")
        self.play(FadeIn(loose), Indicate(P["c2"], color=BLUE, scale_factor=1.15), Indicate(P["c3"], color=BLUE, scale_factor=1.15),
                  run_time=0.8)

        pf = T("poor fit", 26, RED).move_to(loose)
        self.at("fits the")
        self.play(ReplacementTransform(loose, pf), Indicate(P["yn"], color=ORANGE, scale_factor=1.2), run_time=0.6)

        # a better ligand arrives at the SH2 cup
        bl = partner("better ligand", with_badge=True)
        shift = np.array([-1.0, 0.7, 0])
        bl.shift(shift)
        self.at("better ligand")
        self.play(FadeOut(pf), FadeIn(bl, shift=RIGHT * 0.1), run_time=0.5)
        pd = partner("PDGF receptor", with_badge=True).shift(shift)
        tail_free = smooth(TAIL_FREE)
        tgt_node = NODE_FREE
        self.at("phosphorylated")
        self.play(ReplacementTransform(bl, pd), run_time=0.4)
        self.at("does this")
        self.play(pd.animate.shift(-shift),
                  Transform(P["tail"], tail_free),
                  P["yn"].animate.move_to(tgt_node), P["pb"].animate.move_to(tgt_node + np.array([0.3, 0.3, 0])),
                  run_time=1.0)
        # the second example takes the same cup: label and tip swap in one move
        fak = partner("FAK", with_badge=False)
        lab_fak = T("switched on by integrins", 22, GREY).move_to([-4.0, 3.15, 0])
        self.at("So does")
        self.play(ReplacementTransform(pd, fak), run_time=0.5)
        self.at("integrins")
        self.play(FadeIn(lab_fak, shift=DOWN * 0.1), run_time=0.5)

        # beta-arrestin takes the SH3 cup
        arr_g = partner("beta-arrestin", tip=CUP3, with_badge=False)
        # re-aim: stalk comes straight from the left
        arr_c = chip("beta-arrestin", YELLOW, 24).move_to(CUP3 + LEFT * (0.5 + 1.4) + DOWN * 0.0)
        arr_stalk = Line(arr_c.get_right(), CUP3, color=YELLOW, stroke_width=5)
        arr = VGroup(arr_stalk, arr_c)
        pro = T("proline-rich", 22, YELLOW).next_to(arr_c, DOWN, buff=0.15)
        arr_start = arr.copy().shift(DOWN * 1.1 + LEFT * 0.0)
        self.at("such as")
        self.play(FadeOut(lab_fak), FadeIn(arr_start), run_time=0.4)
        self.at("can take")
        self.play(Transform(arr_start, arr), P["lk"].animate.move_to(LINK_FREE), FadeIn(pro), run_time=1.0)

        # tyrosine 416
        self.at("Once open")
        opened = T("clamp open", 26, TEXT).move_to([1.2, 2.95, 0])
        self.play(FadeIn(opened), run_time=0.4)
        loop = chip("activation loop", PURPLE, 22, pad=0.14).move_to(KC + np.array([-0.35, -0.7, 0]))
        y416 = ynode().scale(0.9).move_to(loop.get_right() + RIGHT * 0.42)
        yl = T("tyrosine 416", 24, ORANGE).move_to([y416.get_center()[0] + 0.3, -2.0, 0])
        self.at("phosphorylates")
        self.play(FadeIn(loop), FadeIn(y416, scale=0.5), FadeIn(yl), run_time=0.6)
        pb416 = pbadge().move_to(y416.get_center() + np.array([0.28, 0.28, 0]))
        self.at("its own")
        self.play(FadeIn(pb416, scale=0.4), run_time=0.4)
        on = status("active", GREEN)
        self.at("stays active")
        self.play(ReplacementTransform(P["st"], on),
                  P["kin"][0].animate.set_fill(PURPLE, 0.42), run_time=0.6)
        self.outro()


# ---------------------------------------------------------------------------------------------
class S04Viral(Film):
    """v-Src has no tail: nothing for SH2 to grip. c-Src with tyrosine 527 changed to F does the same."""

    def construct(self):
        P = closed_src(self)
        head = T("c-Src", 34, TEXT, weight=BOLD).move_to([-4.9, 3.05, 0])
        self.add(head)

        # shift of the domains when the clamp has not formed
        d = np.array([-0.7, 0.0, 0])
        vhead = T("v-Src", 34, TEXT, weight=BOLD).move_to(head)
        self.at("lost the tail")
        self.play(ReplacementTransform(head, vhead),
                  Uncreate(P["tail"]), FadeOut(P["yn"]), FadeOut(P["pb"]), FadeOut(P["st"]), run_time=1.0)
        empty = T("nothing to grip", 26, RED).move_to([-4.3, 2.15, 0])
        self.at("nothing to grip")
        self.play(FadeIn(empty, shift=DOWN * 0.1), Indicate(P["c2"], color=RED, scale_factor=1.25), run_time=0.7)
        on = status("active", GREEN)
        self.at("never forms")
        self.play(P["sh2"].animate.shift(d), P["c2"].animate.shift(d), P["sh3"].animate.shift(d), P["c3"].animate.shift(d),
                  P["lk"].animate.move_to(LINK_FREE + LEFT * 0.4 + DOWN * 0.0),
                  P["myr"].animate.shift(d), P["ml"].animate.shift(d),
                  FadeIn(on), P["kin"][0].animate.set_fill(PURPLE, 0.42),
                  FadeOut(empty), run_time=1.0)

        # case two: the tyrosine is changed. Clear the old result in the same move that brings in the new case.
        chead = T("c-Src, tyrosine 527 changed", 28, TEXT, weight=BOLD).move_to([-3.4, 3.05, 0])
        tail = smooth(TAIL_FREE)
        fnode = ynode("F", color=GREY).move_to(NODE_FREE)
        self.at("Changing")
        self.play(ReplacementTransform(vhead, chead), FadeOut(on),
                  P["kin"][0].animate.set_fill(PURPLE, 0.14), run_time=0.8)
        self.play(Create(tail, rate_func=linear), MoveAlongPath(fnode, tail, rate_func=linear), run_time=1.0)
        fl = T("phenylalanine", 24, GREY).move_to([2.6, 3.15, 0])
        self.at("phenylalanine")
        self.play(FadeIn(fl, shift=DOWN * 0.1), Indicate(fnode, color=GREY, scale_factor=1.2), run_time=0.6)
        on2 = status("active", GREEN)
        self.at("does the same")
        self.play(FadeIn(on2), P["kin"][0].animate.set_fill(PURPLE, 0.42), run_time=0.6)
        tr = T("transforms cells", 26, GREEN).move_to([4.6, -1.1, 0])
        self.at("transform cells")
        self.play(FadeIn(tr, shift=UP * 0.1), run_time=0.5)

        # the viral form: the off-switch is gone
        vhead2 = T("v-Src", 34, TEXT, weight=BOLD).move_to([-4.9, 3.05, 0])
        offsw = T("off-switch", 30, RED).move_to([-3.4, 2.1, 0])
        cross = VGroup(Line(offsw.get_corner(DL) + LEFT * 0.1, offsw.get_corner(UR) + RIGHT * 0.1, color=RED, stroke_width=6),
                       Line(offsw.get_corner(UL) + LEFT * 0.1, offsw.get_corner(DR) + RIGHT * 0.1, color=RED, stroke_width=6))
        self.at("viral form")
        self.play(ReplacementTransform(chead, vhead2), FadeOut(VGroup(tail, fnode, fl, tr)), run_time=0.8)
        self.at("lost its")
        self.play(FadeIn(offsw), run_time=0.3)
        self.play(Create(cross), run_time=0.5)
        self.outro()


class S05End(EndCard):
    LINE = "The viral form is always on because it has lost its off-switch."
