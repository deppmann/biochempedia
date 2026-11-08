"""PLC, IP3, DAG and protein kinase C: the kinase that needs both halves  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = phospholipase C, the enzyme that cuts the lipid
  PINK   = IP3, the half that leaves (and the head half of the PIP2 ticket)
  ORANGE = DAG, the half that stays (and the tail half of the PIP2 ticket)
  YELLOW = calcium (the dots, the C2 hand that needs it, the calcium bars)
  PURPLE = protein kinase C (body, label)
  RED    = the pseudosubstrate plug that blocks the active site, and "off"
  GREEN  = on: an active kinase (outline, open active site, the "both" bar)
  GOLD   = a phosphate (the round "P" badge)
  GREY   = membranes, the endoplasmic reticulum, channels, labels, structure

No molecular structures: PIP2 is a two-part ticket (a pink head and an orange tail joined by a
dashed perforation), the kinase is a purple block with a notch, a red plug and two hands, phosphates
are "P" badges, calcium is a dot, the cell's compartments are bars and rounded boxes.

Two framings of the same membrane, so the lipid can be seen big and then in context:
  MICRO (scene 2)                  one lipid fills the frame (the membrane band is 1.5 tall)
  MACRO (scenes 1 and 3 to 6)      the whole membrane along the top, the cytosol and what is in it below
Each change is animated at the end of a scene, after the narration (Film.outro), so the next scene
starts on exactly the picture the last one left.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#F08BB4"

K = 1.5 / 0.7                                         # zoom between the close-up of the lipid and the whole-membrane view
TXM = [-4.2, -2.8, -1.4, 0.0, 3.1, 4.3, 5.5]          # where the lipids sit along the membrane (macro x)
CUT = 3                                               # the lipid that is cut (x = 0)
PS = 1.25                                             # size of the kinase
KY = -0.1 - 1.63 * PS                                 # y of the kinase's body: its folded hands just clear y = 0
IP3_AT = (-1.5, 0.95)                                 # where the IP3 half is when the camera is back on the whole membrane


# ---------------------------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=26, pad=0.2, **kw):
    """chip with an opaque backing so lines drawn behind it do not show through. [back, box, label]"""
    c = chip(text, color, size=size, pad=pad, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def arr(a, b, color=GREY, w=5, tip=0.2):
    a, b = np.array([a[0], a[1], 0.0]), np.array([b[0], b[1], 0.0])
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def pbadge(r=0.17):
    c = Circle(radius=r, stroke_color=GOLD, stroke_width=2, fill_color=GOLD, fill_opacity=1)
    return VGroup(c, T("P", 22, BG, weight=BOLD).move_to(c))


def pop(m, s=1.35):
    return m.animate(rate_func=there_and_back).scale(s)


def glow(*mobs, s=1.1, color=TEXT):
    return [Indicate(m, color=color, scale_factor=s) for m in mobs]


def hglow(h, s=1.08, color=TEXT):
    """flash a hand's outline and label (not its opaque backing, which would turn solid)."""
    return [Indicate(h.box, color=color, scale_factor=s), Indicate(h[2], color=color, scale_factor=s)]


def dot(pos, color=YELLOW, r=0.09):
    return Dot(np.array([pos[0], pos[1], 0.0]), radius=r, color=color)


def seg(a, b, color=GREY, w=3, dashed=False):
    a, b = np.array([a[0], a[1], 0.0]), np.array([b[0], b[1], 0.0])
    if dashed:
        return DashedLine(a, b, color=color, stroke_width=w, dash_length=0.12)
    return Line(a, b, color=color, stroke_width=w)


def qbox(center, size=0.9):
    """a dashed box with a question mark in it: the part nobody has named yet."""
    c = np.array([center[0], center[1], 0.0])
    shape = RoundedRectangle(corner_radius=0.14, width=size, height=size)
    back = shape.copy().set_stroke(width=0).set_fill(BG, 1).move_to(c)
    edge = DashedVMobject(shape.copy().move_to(c), num_dashes=24).set_color(GREY)
    q = T("?", 40, TEXT, weight=BOLD).move_to(c)
    return VGroup(back, edge, q)


def cloud(n=20, seed=11):
    """where the calcium that left the store ends up in the cytosol (scenes 3 and 4 agree on it)."""
    rng = np.random.RandomState(seed)
    return [(rng.uniform(-3.4, 3.4), rng.uniform(0.25, 1.45)) for _ in range(n)]


# ---------------------------------------------------------------------------------------------
# the membrane and its lipids (two framings)
# ---------------------------------------------------------------------------------------------
class Fr:
    """one framing of the membrane. s scales every size; yb is the y of the membrane's inner face."""

    def __init__(self, s, yb, micro):
        self.s, self.yb, self.micro = s, yb, micro
        self.band_h = 1.5 * s
        self.band_y = yb + self.band_h / 2
        self.tw, self.tail_h, self.head_h = 1.5 * s, 1.0 * s, 0.95 * s

    def x(self, xm):
        return xm * (K if self.micro else 1.0)

    def y(self, ym):
        """a macro y, seen in this framing."""
        return ym if not self.micro else self.yb + K * (ym - 2.15)


MACRO = Fr(1 / K, 2.15, False)   # membrane band 2.15 .. 2.85
MICRO = Fr(1.0, 1.2, True)       # membrane band 1.2 .. 2.7


def membrane(F):
    return RoundedRectangle(corner_radius=0.1, width=12.6, height=F.band_h, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.35).move_to([0, F.band_y, 0])


def lipid_vis(F, i):
    """how visible lipid i is: the cut one fully, its neighbours dimmer, and none that fall outside the frame."""
    if i == CUT:
        return 1.0
    x = F.x(TXM[i])
    return 0.55 if abs(x) + F.tw / 2 <= 6.3 else 0.0


def tail_tile(F, i, vis=None):
    v = lipid_vis(F, i) if vis is None else vis
    return RoundedRectangle(corner_radius=0.08 * F.s, width=F.tw, height=F.tail_h, stroke_color=ORANGE, stroke_width=2.5,
                            stroke_opacity=v, fill_color=ORANGE, fill_opacity=0.35 * v).move_to([F.x(TXM[i]), F.yb + F.tail_h / 2, 0])


def head_tile(F, i, vis=None):
    v = lipid_vis(F, i) if vis is None else vis
    return RoundedRectangle(corner_radius=0.08 * F.s, width=F.tw, height=F.head_h, stroke_color=PINK, stroke_width=2.5,
                            stroke_opacity=v, fill_color=PINK, fill_opacity=0.28 * v).move_to([F.x(TXM[i]), F.yb - F.head_h / 2, 0])


def perf_line(F, i, vis=None):
    v = lipid_vis(F, i) if vis is None else vis
    x, w = F.x(TXM[i]), F.tw
    d = DashedVMobject(Line([x - w / 2, F.yb, 0], [x + w / 2, F.yb, 0]), num_dashes=9)
    return d.set_color(TEXT).set_stroke(width=3, opacity=v)


def lipid(F, i):
    """one PIP2 ticket: [tail (in the membrane), head (in the cytosol), perforation]."""
    g = VGroup(tail_tile(F, i), head_tile(F, i), perf_line(F, i))
    g.tail, g.head, g.perf = g[0], g[1], g[2]
    return g


class Stage(VGroup):
    """the membrane and its row of lipids."""

    def __init__(self, F):
        self.F = F
        self.mem = membrane(F)
        self.tix = [lipid(F, i) for i in range(len(TXM))]
        super().__init__(self.mem, *self.tix)


def stage_to(old, new, skip_cut=False):
    """morph one framing of the stage into the other. With skip_cut the cut lipid's head and perforation are gone."""
    anims = [Transform(old.mem, new.mem)]
    for i, (a, b) in enumerate(zip(old.tix, new.tix)):
        if i == CUT and skip_cut:
            anims.append(Transform(a.tail, b.tail))
        else:
            anims.append(Transform(a, b))
    return anims


def torn_stage(F):
    """the membrane after the cut: every lipid but the cut one, and the cut one's tail (DAG) on its own."""
    st = Stage(F)
    tail = st.tix[CUT].tail
    st.remove(st.tix[CUT])
    return st, tail


def chip_for(text, F):
    """the enzyme chip, sitting just right of the cut lipid and just under the membrane."""
    if F.micro:
        c = bchip(text, BLUE, 28, pad=0.22)
        return c.move_to([0.9 + c.width / 2, F.y(1.85), 0])
    c = bchip(text, BLUE, 26, pad=0.2)
    return c.move_to([0.43 + c.width / 2, 1.85, 0])


# ---------------------------------------------------------------------------------------------
# protein kinase C: a shape that acts
# ---------------------------------------------------------------------------------------------
class Pkc:
    """Folded shut: a purple block with a notch (the active site), a red plug (the pseudosubstrate) sitting in the
    notch, and two arms ending in a yellow C2 hand and an orange C1 hand. Reaching the membrane with both hands
    pulls the plug out of the notch. The arms are redrawn from the plug to each hand every frame."""

    def __init__(self, cx=0.0, cy=KY, label="kinase", s=PS):
        self.s = s
        c = np.array([cx, cy, 0.0])
        self.body = RoundedRectangle(corner_radius=0.22 * s, width=3.0 * s, height=1.4 * s, stroke_color=PURPLE, stroke_width=4,
                                     fill_color=PURPLE, fill_opacity=0.25).move_to(c)
        self.lab = T(label, 28, PURPLE).move_to(c + DOWN * 0.22 * s)
        self.slot = Rectangle(width=0.9 * s, height=0.46 * s, stroke_color=GREY, stroke_width=3, fill_color=BG,
                              fill_opacity=1).move_to(c + UP * (0.7 * s - 0.23 * s))
        self.plug = RoundedRectangle(corner_radius=0.06 * s, width=0.7 * s, height=0.26 * s, stroke_color=RED, stroke_width=3,
                                     fill_color=RED, fill_opacity=0.85).move_to(self.slot.get_center() + DOWN * 0.02 * s)
        self.h2 = self._hand("C2", YELLOW, s).move_to(c + np.array([-1.62 * s, 1.35 * s, 0]))
        self.h1 = self._hand("C1", ORANGE, s).move_to(c + np.array([1.62 * s, 1.35 * s, 0]))
        self.arm2 = Line(LEFT, RIGHT, color=PURPLE, stroke_width=4)
        self.arm1 = Line(LEFT, RIGHT, color=PURPLE, stroke_width=4)
        self.tether = Line(LEFT, RIGHT, color=PURPLE, stroke_width=3)
        self.arm2.add_updater(lambda m: m.put_start_and_end_on(self.plug.get_top(), self.h2.get_bottom()))
        self.arm1.add_updater(lambda m: m.put_start_and_end_on(self.plug.get_top(), self.h1.get_bottom()))
        self.tether.add_updater(lambda m: m.put_start_and_end_on(self.body.get_corner(UR) + LEFT * 0.35 * s, self.plug.get_right()))
        for a in (self.arm2, self.arm1, self.tether):
            a.update(0)
        self.group = VGroup(self.body, self.slot, self.tether, self.plug, self.arm2, self.arm1, self.lab, self.h2, self.h1)

    @staticmethod
    def _hand(txt, color, s):
        label = T(txt, 26, color, weight=BOLD)
        box = RoundedRectangle(corner_radius=0.14 * s, width=1.15 * s, height=0.56 * s, stroke_color=color, stroke_width=3,
                               fill_color=color, fill_opacity=0.22)
        back = RoundedRectangle(corner_radius=0.14 * s, width=1.15 * s, height=0.56 * s, stroke_width=0, fill_color=BG, fill_opacity=1)
        g = VGroup(back, box, label.move_to(box))
        g.box = box
        return g

    def core(self):
        """the parts that move with the kinase (the arms follow them by themselves)."""
        return [self.body, self.slot, self.plug, self.lab, self.h2, self.h1]

    def center(self):
        return self.body.get_center()

    def rest_h2(self):
        return self.center() + np.array([-1.62 * self.s, 1.35 * self.s, 0])

    def rest_h1(self):
        return self.center() + np.array([1.62 * self.s, 1.35 * self.s, 0])

    def rest_plug(self):
        return self.slot.get_center() + DOWN * 0.02 * self.s

    def on(self):
        """active: green outline, open (green) active site."""
        return [self.body.animate.set_stroke(GREEN, 5), self.slot.animate.set_stroke(GREEN, 4).set_fill(GREEN, 0.3)]


def lamp(text, color, pos):
    return T(text, 30, color, weight=BOLD).move_to([pos[0], pos[1], 0])


PACE = 1.25   # the real voice is about a quarter slower than the draft voice these moves were first timed to


class Film(SpokenScene):
    def play(self, *anims, **kw):
        if kw.get("run_time") is not None:
            kw["run_time"] = kw["run_time"] * PACE
        super().play(*anims, **kw)

    def outro(self, *anims, then=None, after=None, run_time=0.4):
        """hold until the narration ends, clear what the next scene does not inherit, then (optionally)
        change framing. These run after the last word, so they add a short breath between scenes."""
        rest = self.narration_s - 0.02 - self.elapsed()
        if rest > 0:
            self.wait(rest)
        if anims:
            self.play(*anims, run_time=run_time)
        if then:
            self.play(*then, run_time=1.0)
        if after:
            self.play(*after, run_time=0.45)
        if then or after:
            self.wait(0.15)
        self.finish()


class S00Title(TitleCard):
    LESSON = "PLC, IP3, DAG and Protein Kinase C"
    TITLE = "The kinase that needs both halves"


# ---------------------------------------------------------------------------------------------
class S01Question(Film):
    """a lipid is cut somewhere on the membrane; a folded kinase waits below; how can it know? (MACRO)"""

    def construct(self):
        F = MACRO
        st = Stage(F)
        rec = RoundedRectangle(corner_radius=0.2, width=0.5, height=1.9, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.5).move_to([-5.6, 2.5, 0])
        rec_lbl = T("receptor", 24, GREY).move_to([-4.5, 3.1, 0])
        self.play(FadeIn(st), FadeIn(rec), FadeIn(rec_lbl), run_time=0.4)

        # the kinase, far from the lipid
        k = Pkc(0.0, KY)
        self.at("a kinase")
        self.play(FadeIn(k.group, shift=UP * 0.3), run_time=0.8)

        # the unknown path between the lipid and the kinase
        path = seg([0, 0.15], [0, 1.6], GREY, 4, dashed=True)
        box = qbox([0, 0.85])
        cutx = F.x(TXM[CUT])
        self.at("has just been cut")
        self.play(Create(path), FadeIn(box, scale=0.8), Indicate(st.tix[CUT][1], color=TEXT, scale_factor=1.15), run_time=0.9)
        self.at("here and now")
        self.play(Flash(np.array([cutx, 1.93, 0]), color=TEXT, line_length=0.3, flash_radius=0.4, num_lines=12), run_time=0.7)

        # the receptor fires, the enzyme arrives and cuts
        self.at("A receptor fires")
        self.play(Indicate(rec, color=TEXT, scale_factor=1.12), Flash(np.array([-5.6, 3.45, 0]), color=TEXT, line_length=0.3,
                                                                         flash_radius=0.35, num_lines=12), run_time=0.8)
        enz = chip_for("enzyme", F)
        goal = enz.get_center().copy()
        enz.move_to([-4.9, 1.0, 0])
        self.at("an enzyme")
        self.play(FadeIn(enz, shift=RIGHT * 0.2), run_time=0.4)
        self.at("cuts a lipid")
        self.play(enz.animate.move_to(goal), run_time=0.9)
        self.play(Flash(np.array([cutx + 0.35, 2.15, 0]), color=BLUE, line_length=0.3, flash_radius=0.35, num_lines=10), run_time=0.5)

        # the kinase waits
        cyt = T("cytosol", 24, GREY).move_to([-5.2, -0.4, 0])
        self.at("The kinase waits")
        self.play(FadeIn(cyt), *glow(k.body, k.lab, s=1.05, color=PURPLE), run_time=0.8)
        self.at("What could tell")
        self.play(Indicate(box[2], color=TEXT, scale_factor=1.4), run_time=0.9)

        # zoom in on the lipid: the kinase and the question go, the membrane comes close
        enz2 = chip_for("enzyme", MICRO)
        big = Stage(MICRO)
        self.outro(FadeOut(k.group), FadeOut(path), FadeOut(box), FadeOut(cyt), FadeOut(rec), FadeOut(rec_lbl),
                   then=[*stage_to(st, big), Transform(enz, enz2)], run_time=0.5)


# ---------------------------------------------------------------------------------------------
class S02Cut(Film):
    """one ticket torn along its perforation: the pink head leaves, the orange tail stays. (MICRO)"""

    def construct(self):
        F = MICRO
        yb = F.yb
        st = Stage(F)
        enz = chip_for("enzyme", F)
        self.add(st, enz)
        cut_i = st.tix[CUT]

        # the enzyme's blade points at the perforation
        blade = arr([1.3, yb - 0.25, 0], [0.82, yb + 0.02, 0], BLUE, w=6, tip=0.22)
        pip = T("PIP2", 32, TEXT, weight=BOLD).move_to([0.0, yb - 0.475, 0])
        self.at("The lipid is")
        self.play(FadeIn(blade), FadeIn(pip, shift=RIGHT * 0.1), Indicate(cut_i[0], color=ORANGE, scale_factor=1.05),
                  Indicate(cut_i[1], color=PINK, scale_factor=1.05), run_time=0.9)
        face = seg([-6.2, yb], [-4.0, yb], TEXT, 5)
        face_lbl = T("inside surface", 24, GREY).move_to([-5.1, yb - 0.38, 0])
        self.at("of the membrane")
        self.play(Create(face), FadeIn(face_lbl), run_time=0.6)

        # the enzyme gets its name
        plc = chip_for("phospholipase C", F)
        self.at("phospholipase")
        self.play(Transform(enz[0], plc[0]), Transform(enz[1], plc[1]), FadeOut(enz[2]), FadeIn(plc[2]),
                  FadeOut(face), FadeOut(face_lbl), run_time=0.7)
        enz = VGroup(enz[0], enz[1], plc[2])
        self.at("torn along")
        self.play(Flash(np.array([0.78, yb, 0]), color=BLUE, line_length=0.35, flash_radius=0.45, num_lines=12),
                  FadeOut(cut_i.perf), FadeOut(pip), FadeOut(blade), cut_i.head.animate.shift(DOWN * 0.45),
                  pop(enz, 1.06), run_time=0.9)

        # the head half: IP3, with three phosphates
        ip3_lbl = T("IP3", 32, PINK, weight=BOLD).move_to(cut_i.head.get_center() + UP * 0.12)
        self.at("One half")
        self.play(FadeIn(ip3_lbl), Indicate(cut_i.head, color=PINK, scale_factor=1.08), run_time=0.6)
        hc = cut_i.head.get_center()
        ps = [pbadge().move_to(hc + np.array([dx, -0.26, 0])) for dx in (-0.45, 0.0, 0.45)]
        self.at("three phosphates")
        self.play(LaggedStart(*[FadeIn(p, scale=0.4) for p in ps], lag_ratio=0.3), run_time=1.1)
        ip3 = VGroup(cut_i.head, ip3_lbl, *ps)
        # leaves: the zoom-out of the next scene starts from here
        gx, gy = F.x(IP3_AT[0]), F.y(IP3_AT[1])
        self.at("dissolves in water")
        self.play(ip3.animate.move_to([gx, gy, 0]).rotate(0.1), run_time=1.8)

        # the tail half: DAG
        dag_lbl = T("DAG", 32, ORANGE, weight=BOLD).move_to(cut_i.tail.get_center())
        self.at("The other half")
        self.play(FadeIn(dag_lbl), Indicate(cut_i.tail, color=ORANGE, scale_factor=1.06), run_time=0.7)
        self.at("stays in the membrane")
        self.play(*glow(cut_i.tail, dag_lbl, s=1.1, color=ORANGE), run_time=0.8)

        # two messengers, in two places
        two = T("two second messengers, in two places", 26, TEXT).move_to([1.9, -2.7, 0])
        self.at("One cut makes")
        self.play(FadeIn(two, shift=UP * 0.1), run_time=0.6)
        self.at("in two places")
        self.play(*glow(ip3[0], ip3[1], s=1.12, color=PINK), *glow(dag_lbl, cut_i.tail, s=1.1, color=ORANGE), run_time=0.9)

        # zoom out: the membrane goes back along the top; IP3 is on its way
        macro = Stage(MACRO)
        ip3_m = bchip("IP3", PINK, 26).move_to([IP3_AT[0], IP3_AT[1], 0])
        dag_m = T("DAG", 26, ORANGE, weight=BOLD).move_to([0.0, 1.8, 0])
        self.outro(FadeOut(two), FadeOut(enz),
                   then=[*stage_to(st, macro, skip_cut=True), FadeOut(VGroup(*ps)), FadeOut(ip3[1]),
                         ReplacementTransform(ip3[0], ip3_m[1]), FadeIn(ip3_m[2]),
                         ReplacementTransform(dag_lbl, dag_m)], run_time=0.5)


# ---------------------------------------------------------------------------------------------
class S03Calcium(Film):
    """IP3 travels to the endoplasmic reticulum, opens its channel, and calcium streams out. (MACRO)"""

    def construct(self):
        F = MACRO
        st, tail = torn_stage(F)
        self.add(st, tail)
        ip3 = bchip("IP3", PINK, 26).move_to([IP3_AT[0], IP3_AT[1], 0])
        dag = T("DAG", 26, ORANGE, weight=BOLD).move_to([0.0, 1.8, 0])
        self.add(ip3, dag)

        # the endoplasmic reticulum, full of calcium, with a closed gate in its wall
        er = RoundedRectangle(corner_radius=0.35, width=7.2, height=1.7, stroke_color=GREY, stroke_width=4,
                              fill_color=GREY, fill_opacity=0.12).move_to([-0.6, -2.2, 0])
        gap = Rectangle(width=1.75, height=0.2, stroke_width=0, fill_color=BG, fill_opacity=1).move_to([0, -1.35, 0])
        door_l = Line([-0.8, -1.35, 0], [0.0, -1.35, 0], color=GREY, stroke_width=10)
        door_r = Line([0.0, -1.35, 0], [0.8, -1.35, 0], color=GREY, stroke_width=10)
        er_lbl = VGroup(Rectangle(width=3.9, height=0.4, stroke_width=0, fill_color=BG, fill_opacity=1),
                        T("endoplasmic reticulum", 26, GREY))
        er_lbl[1].move_to(er_lbl[0])
        er_lbl.move_to([-1.2, -2.75, 0])
        rng = np.random.RandomState(7)
        er_dots = []
        while len(er_dots) < 40:
            x, y = rng.uniform(-3.9, 2.7), rng.uniform(-2.5, -1.55)
            if abs(x) < 0.9 and y > -1.8:
                continue
            if -3.2 < x < 0.8 and y < -2.5:
                continue
            er_dots.append(dot([x, y], YELLOW, 0.08))
        ER = VGroup(er, gap, door_l, door_r, er_lbl, *er_dots)

        self.at("Follow the half")
        self.play(*glow(ip3[1], ip3[2], s=1.15, color=PINK), run_time=0.7)
        self.at("diffuses")
        wob = [np.array([-0.9, 0.5, 0]), np.array([0.3, 0.15, 0]), np.array([-0.15, -0.1, 0]), np.array([0.0, -0.3, 0])]
        path = VMobject().set_points_smoothly([ip3.get_center(), *wob])
        self.play(MoveAlongPath(ip3, path), FadeIn(ER, shift=UP * 0.3), run_time=2.2, rate_func=smooth)
        self.at("a calcium store")
        self.play(LaggedStart(*[pop(d, 1.8) for d in er_dots[::2]], lag_ratio=0.08), run_time=1.2)

        # the channel
        chan = T("channel", 24, GREY).move_to([-1.75, -1.0, 0])
        self.at("A channel")
        self.play(FadeIn(chan), Indicate(door_l, color=TEXT, scale_factor=1.05), Indicate(door_r, color=TEXT, scale_factor=1.05), run_time=0.8)
        self.at("when")
        self.play(ip3.animate.move_to([0.0, -0.95, 0]), run_time=0.5)
        self.at("binds")
        self.play(Rotate(door_l, 85 * DEGREES, about_point=np.array([-0.8, -1.35, 0])),
                  Rotate(door_r, -85 * DEGREES, about_point=np.array([0.8, -1.35, 0])), pop(ip3, 1.12), run_time=0.9)

        # the two bars: free calcium in the store against the resting cytosol
        base = -2.5
        axis = seg([3.85, base], [6.15, base], GREY, 3)
        title = T("free calcium", 24, GREY).move_to([5.0, 0.95, 0])

        def bar(x, h):
            return Rectangle(width=0.8, height=max(h, 0.04), stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW,
                             fill_opacity=0.35).move_to([x, base + max(h, 0.04) / 2, 0])

        b_er, b_cy = bar(4.35, 2.7), bar(5.65, 0.0)
        l_er = T("store", 22, GREY).move_to([4.35, -2.85, 0])
        l_cy = T("cytosol", 22, GREY).move_to([5.65, -2.85, 0])
        x1000 = M("1000×", 24, YELLOW).move_to([4.35, 0.5, 0])
        self.at("The store holds")
        self.play(Create(axis), FadeIn(title), FadeIn(l_er), FadeIn(l_cy), run_time=0.6)
        self.play(GrowFromEdge(b_er, DOWN), FadeIn(b_cy), run_time=0.7)
        self.at("times the resting")
        self.play(FadeIn(x1000, shift=DOWN * 0.1), run_time=0.5)
        self.at("or more")
        self.play(Indicate(b_er, color=YELLOW, scale_factor=1.04), run_time=0.6)

        # the fast rise: twenty dots leave through the gate and spread through the cytosol
        movers = er_dots[1::2][:20]
        stream = []
        for d, (fx, fy) in zip(movers, cloud()):
            xg = (1 if fx > 0 else -1) * rng.uniform(0.5, 0.7)
            stream.append(Succession(d.animate(run_time=0.45).move_to([xg, -1.45, 0]),
                                     d.animate(run_time=0.9).move_to([fx, fy, 0])))
        self.at("So an open channel")
        self.play(LaggedStart(*stream, lag_ratio=0.07), Transform(b_cy, bar(5.65, 0.8)), run_time=1.9)
        self.at("stays in the membrane")
        self.play(*glow(tail, dag, s=1.12, color=ORANGE), run_time=0.8)

        # on to the kinase: the store and the chart go; the calcium and the DAG stay
        ER.remove(*movers)
        self.add(*movers)
        self.outro(FadeOut(ER), FadeOut(ip3), FadeOut(chan), FadeOut(VGroup(axis, title, b_er, b_cy, l_er, l_cy, x1000)))


# ---------------------------------------------------------------------------------------------
class S04Kinase(Film):
    """meet the kinase: the plug in the active site, the C2 hand that needs calcium, the C1 hand that binds DAG. (MACRO)"""

    def construct(self):
        F = MACRO
        st, tail = torn_stage(F)
        dag = T("DAG", 26, ORANGE, weight=BOLD).move_to([0.0, 1.8, 0])
        ca = [dot(p) for p in cloud()]
        self.add(st, tail, dag, *ca)

        k = Pkc(0.0, KY)
        self.at("Now meet")
        self.play(FadeIn(k.group, shift=UP * 0.3), run_time=0.9)
        newlab = T("protein kinase C", 28, PURPLE).move_to(k.lab)
        self.at("protein kinase C")
        self.play(FadeOut(k.lab), FadeIn(newlab), run_time=0.5)
        sub = T("puts phosphates on serines and threonines", 24, GREY).move_to([0.0, -3.3, 0])
        self.at("serines")
        self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.6)

        # folded shut
        shut = T("folded shut", 24, GREY).move_to([-4.2, k.rest_h2()[1], 0])
        self.at("folded shut")
        self.play(FadeIn(shut), *hglow(k.h2, 1.06, PURPLE), *hglow(k.h1, 1.06, PURPLE), run_time=0.7)

        # the plug in the active site
        pseudo = T("pseudosubstrate", 24, RED).move_to([-4.5, KY + 0.35, 0])
        pline = seg([pseudo.get_right()[0] + 0.1, pseudo.get_right()[1]], [k.plug.get_left()[0] - 0.03, k.plug.get_center()[1]], RED, 3)
        self.at("pseudosubstrate")
        self.play(FadeOut(shut), FadeIn(pseudo, shift=RIGHT * 0.1), Create(pline), pop(k.plug, 1.25), run_time=0.7)
        asite = T("active site", 24, GREY).move_to([4.0, KY + 0.35, 0])
        aline = seg([asite.get_left()[0] - 0.1, asite.get_left()[1]], [k.slot.get_right()[0] + 0.02, k.slot.get_center()[1] - 0.05], GREY, 3)
        self.at("active site")
        self.play(FadeIn(asite), Create(aline), Indicate(k.slot, color=TEXT, scale_factor=1.12), run_time=0.7)

        # C2 needs calcium to land
        self.at("part lands")
        up2 = arr([k.h2.get_center()[0], k.h2.get_top()[1] + 0.05], [k.h2.get_center()[0], 1.55], YELLOW, w=4)
        self.play(FadeOut(pseudo), FadeOut(pline), FadeOut(asite), FadeOut(aline),
                  k.h2.box.animate.set_stroke(YELLOW, 5), GrowArrow(up2), run_time=0.8)
        near = min(ca, key=lambda d: np.linalg.norm(d.get_center() - np.array([k.rest_h2()[0], 0.0, 0])))
        self.at("holds calcium")
        self.play(near.animate.move_to(k.h2.get_top() + UP * 0.12), run_time=0.8)
        self.play(pop(near, 1.8), run_time=0.4)

        # C1 binds DAG in the membrane
        c1_line = arr([k.h1.get_center()[0], k.h1.get_top()[1] + 0.05], [0.2, 1.6], ORANGE, w=4)
        self.at("part binds")
        self.play(k.h1.box.animate.set_stroke(ORANGE, 5), GrowArrow(c1_line), run_time=0.8)
        self.at("in the membrane")
        self.play(*glow(tail, dag, s=1.12, color=ORANGE), run_time=0.7)

        # the next scene starts from a plain membrane and the folded kinase
        self.outro(FadeOut(sub), FadeOut(up2), FadeOut(c1_line), FadeOut(dag), FadeOut(tail),
                   FadeOut(VGroup(*ca)), FadeOut(VGroup(*st.tix)),
                   k.h2.box.animate.set_stroke(YELLOW, 3), k.h1.box.animate.set_stroke(ORANGE, 3), run_time=0.5)


# ---------------------------------------------------------------------------------------------
class S05Alone(Film):
    """one signal at a time: C2 grips a calcium-bearing membrane, or C1 a DAG-bearing one, and lets go. (MACRO)"""

    def construct(self):
        F = MACRO
        mem = membrane(F)
        k = Pkc(0.0, KY, label="protein kinase C")
        self.add(mem, k.group)
        rng = np.random.RandomState(5)
        lift = 0.14 * PS

        # many reasons: calcium and DAG turn up here and there with no cut at all
        sparks = [dot([x, y], YELLOW, 0.09) for x, y in [(-4.4, 0.8), (-3.0, 1.6), (4.3, 0.3), (3.4, 1.4), (-4.9, -0.9), (4.9, -1.2)]]
        tiles = [Rectangle(width=0.7, height=0.467, stroke_color=ORANGE, stroke_width=2.5, fill_color=ORANGE, fill_opacity=0.35)
                 .move_to([x, 2.15 + 0.233, 0]) for x in (-4.8, 1.2, 4.4)]
        self.at("Each signal alone")
        self.play(LaggedStart(*[FadeIn(m, scale=0.3) for m in (sparks[0], tiles[0], sparks[2], tiles[2], sparks[4], tiles[1], sparks[1],
                                                                   sparks[3], sparks[5])], lag_ratio=0.18), run_time=2.0)

        # case one: calcium through a voltage-gated channel
        cx = -1.9
        post = dict(corner_radius=0.06, width=0.32, height=0.9, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.7)
        ch_l = RoundedRectangle(**post).move_to([cx - 0.2, 2.6, 0])
        ch_r = RoundedRectangle(**post).move_to([cx + 0.2, 2.6, 0])
        ch_lbl = T("voltage-gated channel", 24, GREY).move_to([cx - 0.9, 3.3, 0])
        case_a = T("calcium alone", 28, YELLOW, weight=BOLD).move_to([-4.6, 0.55, 0])
        self.at("Calcium also rises")
        self.play(FadeOut(VGroup(*sparks)), FadeOut(VGroup(*tiles)), FadeIn(ch_l), FadeIn(ch_r), FadeIn(ch_lbl), run_time=0.8)
        a_dots = [dot([cx + rng.uniform(-0.08, 0.08), 2.45]) for _ in range(7)]
        a_tgt = [(cx + rng.uniform(-1.0, 1.0), rng.uniform(0.85, 1.6)) for _ in range(7)]
        a_tgt[0] = (cx - 0.5, 1.3)
        self.at("channel opens")
        self.play(ch_l.animate.shift(LEFT * 0.17), ch_r.animate.shift(RIGHT * 0.17), run_time=0.3)
        self.add(*a_dots)
        self.play(LaggedStart(*[d.animate.move_to([x, y, 0]) for d, (x, y) in zip(a_dots, a_tgt)], lag_ratio=0.1), run_time=1.0)
        self.at("With calcium alone")
        self.play(FadeIn(case_a, shift=RIGHT * 0.1), run_time=0.5)
        # C2 takes a calcium ion, reaches the membrane, and cannot hold on
        self.at("holds the membrane")
        hand_up = np.array([cx, 1.83, 0])
        self.play(a_dots[0].animate.move_to(k.h2.get_top() + UP * 0.12), run_time=0.3)
        self.play(k.h2.animate.move_to(hand_up), a_dots[0].animate.move_to(hand_up + np.array([-0.5, 0.34, 0])),
                  k.plug.animate.shift(UP * lift), run_time=0.6)
        self.at("weakly")
        self.play(k.h2.animate.move_to(k.rest_h2()), a_dots[0].animate.move_to(k.rest_h2() + np.array([-0.9, 0.1, 0])),
                  k.plug.animate.move_to(k.rest_plug()), run_time=0.8)
        off_a = lamp("largely off", RED, [3.9, KY + 0.2])
        self.at("stays largely off")
        self.play(FadeIn(off_a, scale=0.8), run_time=0.5)

        # case two: DAG from some other lipid enzyme
        dx = 1.9
        other = bchip("other lipid enzyme", GREY, 24).move_to([4.5, 1.75, 0])
        d_tile = Rectangle(width=0.7, height=0.467, stroke_color=ORANGE, stroke_width=2.5, fill_color=ORANGE,
                           fill_opacity=0.35).move_to([dx, 2.15 + 0.233, 0])
        case_b = T("DAG alone", 28, ORANGE, weight=BOLD).move_to([-4.6, 0.55, 0])
        self.at("Other lipid enzymes")
        self.play(FadeOut(VGroup(ch_l, ch_r, ch_lbl)), FadeOut(VGroup(*a_dots)), FadeOut(case_a), FadeOut(off_a),
                  FadeIn(other, shift=LEFT * 0.2), run_time=0.8)
        self.at("also make")
        self.play(FadeIn(d_tile, scale=0.4), Flash(np.array([dx, 2.4, 0]), color=ORANGE, line_length=0.25, flash_radius=0.35, num_lines=10),
                  run_time=0.7)
        self.at("DAG alone")
        self.play(FadeIn(case_b, shift=RIGHT * 0.1), run_time=0.5)
        self.at("holds weakly")
        hand_up1 = np.array([dx, 1.83, 0])
        self.play(k.h1.animate.move_to(hand_up1), k.plug.animate.shift(UP * lift), run_time=0.6)
        self.at("weakly too")
        self.play(k.h1.animate.move_to(k.rest_h1()), k.plug.animate.move_to(k.rest_plug()), run_time=0.8)
        off_b = lamp("largely off", RED, [3.9, KY + 0.2])
        self.at("stays largely off", nth=1)
        self.play(FadeIn(off_b, scale=0.8), run_time=0.5)

        # next: the chart goes on the right, so the kinase moves left; the membrane goes plain again
        self.outro(FadeOut(VGroup(other, d_tile, case_b, off_b)),
                   then=[m.animate.shift(LEFT * 3.4) for m in k.core()])


# ---------------------------------------------------------------------------------------------
class S06Together(Film):
    """thirty times thirty is nine hundred; the cut gives both signals at once; both hands grip and the plug comes out. (MACRO)"""

    def construct(self):
        F = MACRO
        mem = membrane(F)
        k = Pkc(-3.4, KY, label="protein kinase C")
        self.add(mem, k.group)
        rng = np.random.RandomState(3)
        lift = 0.12 * PS

        # each contact alone: reach, touch, let go
        self.at("weak alone")
        for h, rest in ((k.h2, k.rest_h2()), (k.h1, k.rest_h1())):
            up = np.array([rest[0], 1.83, 0])
            self.play(h.animate.move_to(up), k.plug.animate.shift(UP * lift), run_time=0.3)
            self.play(h.animate.move_to(rest), k.plug.animate.move_to(k.rest_plug()), run_time=0.3)

        # the chart: how strongly the kinase favors the membrane
        base = -2.55
        axis = seg([0.85, base], [6.2, base], GREY, 3)
        title = T("example: favors the membrane", 26, GREY).move_to([3.5, 1.55, 0])

        def bar(x, h, color):
            return Rectangle(width=1.0, height=max(h, 0.04), stroke_color=color, stroke_width=3, fill_color=color,
                             fill_opacity=0.35).move_to([x, base + max(h, 0.04) / 2, 0])

        xs = [1.7, 3.5, 5.3]
        H = 3.1
        names = [T("calcium\nalone", 22, YELLOW, line_spacing=0.8), T("DAG\nalone", 22, ORANGE, line_spacing=0.8),
                 T("both", 22, GREEN)]
        for n, x in zip(names, xs):
            n.move_to([x, base - 0.42, 0])
        self.at("binding energies")
        self.play(Create(axis), FadeIn(title), *[FadeIn(n) for n in names], run_time=0.7)
        b1, b2 = bar(xs[0], H * 30 / 900, YELLOW), bar(xs[1], H * 30 / 900, ORANGE)
        t1 = M("30×", 26, YELLOW).move_to([xs[0], base + 0.5, 0])
        t2 = M("30×", 26, ORANGE).move_to([xs[1], base + 0.5, 0])
        self.at("contact alone favors")
        self.play(GrowFromEdge(b1, DOWN), GrowFromEdge(b2, DOWN), FadeIn(t1, shift=UP * 0.1), FadeIn(t2, shift=UP * 0.1), run_time=0.9)
        b3 = bar(xs[2], H, GREEN)
        t3 = M("900×", 30, GREEN, weight=BOLD).move_to([xs[2], base + H + 0.4, 0])
        self.at("the pair favors")
        self.play(GrowFromEdge(b3, DOWN), run_time=1.5, rate_func=smooth)
        self.play(FadeIn(t3, shift=DOWN * 0.1), pop(t3, 1.15), run_time=0.6)

        # the cut gives both at once: the chart goes, the kinase slides under the lipid
        k_shift = 3.4 - 0.775
        self.at("appear together")
        self.play(FadeOut(VGroup(axis, title, b1, b2, b3, t1, t2, t3, *names)),
                  *[m.animate.shift(RIGHT * k_shift) for m in k.core()], run_time=1.0)
        lip = lipid(F, CUT)
        plc = chip_for("phospholipase C", F)
        self.at("phospholipase")
        self.play(FadeIn(lip), FadeIn(plc, shift=LEFT * 0.2), run_time=0.6)
        ip3_lbl = T("IP3", 24, PINK, weight=BOLD).move_to(lip.head.get_center())
        head = VGroup(lip.head, ip3_lbl)
        c_dots = [dot([rng.uniform(-3.8, -3.2), -4.3]) for _ in range(7)]
        c_tgt = [(-3.2, 1.65), (-2.65, 1.5), (-3.45, 1.2), (-2.9, 1.05), (-2.45, 0.8), (-3.5, 0.75), (-2.95, 0.6)]
        self.add(*c_dots)
        ca_lbl = T("calcium", 24, YELLOW).move_to([-4.2, 0.4, 0])
        dag_lbl = T("DAG", 24, ORANGE, weight=BOLD).move_to([0.95, 2.5, 0])
        self.at("just cut")
        self.play(Flash(np.array([0.35, 2.15, 0]), color=BLUE, line_length=0.3, flash_radius=0.4, num_lines=10),
                  FadeOut(lip.perf), FadeIn(ip3_lbl), FadeIn(dag_lbl), run_time=0.4)
        self.play(head.animate.move_to([0.0, 0.85, 0]), run_time=0.3)
        self.play(head.animate.move_to([2.7, 0.2, 0]).set_opacity(0.0),
                  LaggedStart(*[d.animate.move_to([x, y, 0]) for d, (x, y) in zip(c_dots, c_tgt)], lag_ratio=0.1),
                  FadeIn(ca_lbl), run_time=1.1)

        # both hands grip; the plug is pulled out; the kinase is on
        self.at("Only then is")
        h2_up, h1_up = np.array([-1.55, 1.83, 0]), np.array([0.0, 1.83, 0])
        self.play(FadeOut(plc), k.h2.animate.move_to(h2_up), k.h1.animate.move_to(h1_up), k.plug.animate.shift(UP * 0.3 * PS),
                  c_dots[0].animate.move_to(h2_up + np.array([-0.45, 0.34, 0])), run_time=1.0)
        self.at("held firmly")
        self.play(*hglow(k.h2, 1.08, TEXT), *hglow(k.h1, 1.08, TEXT), run_time=0.7)
        self.at("free its active")
        self.play(k.plug.animate.shift(UP * 1.1 * PS), *k.on(), run_time=1.0)
        det = T("coincidence detector", 28, GREEN, weight=BOLD).move_to([-0.775, KY - 1.12, 0])
        on = lamp("on", GREEN, [2.3, KY])
        self.at("coincidence detector")
        self.play(FadeIn(det, shift=UP * 0.1), FadeIn(on, scale=0.8), run_time=0.7)
        self.at("keep this rule")
        self.play(pop(det, 1.1), pop(on, 1.3), run_time=0.8)
        self.at("strongly")
        self.play(*hglow(k.h2, 1.08, TEXT), *hglow(k.h1, 1.08, TEXT), run_time=0.8)
        self.at("when calcium")
        self.play(*glow(*c_dots, s=1.5, color=YELLOW), run_time=0.8)
        self.at("DAG arrive")
        self.play(*glow(lip.tail, dag_lbl, s=1.15, color=ORANGE), run_time=0.8)
        self.at("arrive together")
        self.play(*glow(*c_dots, s=1.5, color=YELLOW), *glow(lip.tail, s=1.15, color=ORANGE),
                  *hglow(k.h2, 1.06, TEXT), *hglow(k.h1, 1.06, TEXT), run_time=0.9)
        self.finish()


class S07End(EndCard):
    LINE = "Conventional protein kinase C responds strongly when calcium and DAG arrive together."
