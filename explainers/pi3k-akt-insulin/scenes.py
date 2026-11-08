"""PI 3-kinase, Akt and insulin: a membrane address for Akt  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = insulin, the signal outside the cell
  BLUE   = the insulin receptor
  TEAL   = IRS-1, the docking protein, and the tyrosines on its tail
  ORANGE = kinases at the membrane that put a phosphate on something: PI 3-kinase, PDK1, mTORC2
  PURPLE = Akt
  PINK   = a reading domain, drawn as a cup that closes on a phosphate: SH2 (on PI 3-kinase), PH (on Akt and PDK1)
  GOLD   = a phosphate (the round "P" badge); a lipid head wearing one is PIP3
  GREEN  = on / active (Akt at the end), and the ticks of the three checks
  RED    = blocked (insulin cannot cross the membrane)
  WHITE  = glucose and glycogen (the outcome); the plain lipid head is GREY
  GREY   = membrane, PIP2 lipid heads, proteins that are not named, labels, parts not yet used

No molecular structures: receptor and kinases are labelled blobs, a lipid is a stalk with a round head,
a domain is a cup, a phosphate is a "P" badge, the fatty acid anchor is a short curved line.

Two framings of the same picture:
  WIDE  (scenes 1, 2, 6)  the whole relay, membrane near the top, the cytosol below.
  CLOSE (scenes 3, 4, 5)  zoomed on the inner face of the membrane where PIP3 is made and Akt arrives.
Scene 2 ends by zooming from WIDE to CLOSE, so scene 3 starts on exactly the picture scene 2 left.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#F08BB4"

# ---------------------------------------------------------------------------------------------
# geometry, in WIDE units; a Fr maps them to the screen
# ---------------------------------------------------------------------------------------------
MEM_Y, MEM_H = 1.9, 0.34
MEM_BOT = MEM_Y - MEM_H / 2                  # underside of the membrane
LIP_X = [0.5, 1.2, 1.9, 2.6, 3.3, 4.0]       # the PIP2 / PIP3 lipids
HEAD_Y, BADGE_Y = 1.28, 0.93                 # lipid head and the phosphate under it
AKT_GRIP, PDK_GRIP = LIP_X[1], LIP_X[4]      # the lipids that hold Akt and PDK1
AKT_C = np.array([AKT_GRIP + 0.45, BADGE_Y - 0.84, 0])      # Akt when held at the membrane
PDK_C = np.array([PDK_GRIP + 0.45, BADGE_Y - 0.80, 0])
WAIT = np.array([1.9, -1.1, 0])              # where Akt drifts before the lipid exists
REC_X = -4.2                                 # the insulin receptor
IRS_X, IRS_Y = -2.3, 1.32                    # IRS-1 and its tail
TAIL_Y = [0.55, -0.25, -1.05, -1.7]          # the four tyrosines on the tail
TAIL_END = -1.85
PI3K_C = np.array([-0.87, 0.55, 0])          # PI 3-kinase, docked on the top tyrosine
CUP_R = 0.4                                  # radius of a reading cup


class Fr:
    """A framing: k = zoom, (fx, fy) = the WIDE point that sits at the middle of the screen."""

    def __init__(self, k, fx=0.0, fy=0.0):
        self.k, self.fx, self.fy = k, fx, fy

    def p(self, x, y=None):
        if y is None:
            x, y = x[0], x[1]
        return np.array([(x - self.fx) * self.k, (y - self.fy) * self.k, 0.0])

    def sw(self, w):
        return w * self.k ** 0.5


WIDE = Fr(1.0)
RELAY = Fr(1.3, -2.0, 0.75)
CLOSE = Fr(1.6, 1.3, 0.0)


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=26, pad=0.16, **kw):
    """chip with an opaque backing so lines drawn behind it do not show through."""
    c = chip(text, color, size=size, pad=pad, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def strike(m, color=RED):
    return Line(m.get_corner(DL) + [-0.08, -0.04, 0], m.get_corner(UR) + [0.08, 0.04, 0], color=color, stroke_width=7)


def pbadge(F=WIDE, r=0.19):
    c = Circle(radius=r * F.k, stroke_color=GOLD, stroke_width=2, fill_color=GOLD, fill_opacity=1)
    return VGroup(c, T("P", 22 * F.k, BG, weight=BOLD).move_to(c))


def pop(m, s=1.35):
    """swell and settle, without recolouring (Indicate would hide the P on a badge)."""
    return m.animate(rate_func=there_and_back).scale(s)


def glow(*mobs, s=1.1, color=TEXT):
    """flash each mobject in place: one animation per mobject."""
    return [Indicate(m, color=color, scale_factor=s) for m in mobs]


def membrane(F):
    return RoundedRectangle(corner_radius=0.1 * F.k, width=12.6 * F.k, height=MEM_H * F.k, stroke_color=GREY,
                            stroke_width=F.sw(3), fill_color=GREY, fill_opacity=0.35).move_to(F.p(0, MEM_Y))


def blob(F, c, text, color, w, h, size=30, bold=True):
    """a labelled rounded blob with an opaque backing: [back, body, label]."""
    k = F.k
    back = RoundedRectangle(corner_radius=0.26 * k, width=w * k, height=h * k, stroke_width=0, fill_color=BG, fill_opacity=1)
    body = RoundedRectangle(corner_radius=0.26 * k, width=w * k, height=h * k, stroke_color=color, stroke_width=F.sw(3.5),
                            fill_color=color, fill_opacity=0.28)
    lbl = T(text, size * k, color, weight=BOLD if bold else NORMAL)
    g = VGroup(back, body, lbl).move_to(c)
    g.body, g.lbl = body, lbl
    return g


def recolor_blob(g, color):
    return [g.body.animate.set_stroke(color).set_fill(color, 0.28), g.lbl.animate.set_color(color)]


def cup(center, r, face="up", closed=False, color=PINK):
    """a reading domain: a bowl that opens toward `face`; closed = the same bowl, nearly shut."""
    a0 = {"up": 170, "left": 260, "down": 350, "right": 80}[face]
    start, ang = (a0 - 45, 290) if closed else (a0, 200)
    s = AnnularSector(inner_radius=r * 0.62, outer_radius=r, angle=ang * DEGREES, start_angle=start * DEGREES,
                      color=color, fill_opacity=1, stroke_width=0)
    return s.shift(center)


def tick(c, s=0.2):
    a, b, d = c + np.array([-s, 0.0, 0]), c + np.array([-s * 0.3, -s * 0.8, 0]), c + np.array([s, s * 0.9, 0])
    return VGroup(Line(a, b, color=GREEN, stroke_width=9), Line(b, d, color=GREEN, stroke_width=9))


def lipids(F):
    """the row of PIP2 lipids hanging from the inner face of the membrane: list of [stalk, head]."""
    out = []
    for x in LIP_X:
        stem = Line(F.p(x, MEM_BOT), F.p(x, HEAD_Y + 0.15), color=GREY, stroke_width=F.sw(3))
        head = Circle(radius=0.15 * F.k, stroke_color=GREY, stroke_width=F.sw(2.5), fill_color=GREY,
                      fill_opacity=0.5).move_to(F.p(x, HEAD_Y))
        out.append(VGroup(stem, head))
    return out


def lip_badge(F, i):
    return pbadge(F, 0.17).move_to(F.p(LIP_X[i], BADGE_Y))


def clock(center, r=0.45):
    center = np.array(center, float)
    face = Circle(radius=r, stroke_color=GREY, stroke_width=4).move_to(center)
    ticks = VGroup(*[Line(center + (r - 0.11) * v, center + r * v, color=GREY, stroke_width=4) for v in (UP, RIGHT, DOWN, LEFT)])
    hand = Line(center, center + UP * (r - 0.15), color=TEXT, stroke_width=5)
    pin = Dot(center, radius=0.05, color=TEXT)
    g = VGroup(face, ticks, hand, pin)
    g.hand, g.c = hand, center
    return g


# Akt and its parts ------------------------------------------------------------------------------
CUP_OFF = np.array([-0.45, 0.84, 0])
LOOP_OFF = np.array([0.85, 0.10, 0])           # the activation loop bulges out of the right edge
LOOP_TIP = np.array([1.05, 0.10, 0])
TAIL_OFF = np.array([-0.30, -0.50, 0])
TAIL_TIP = np.array([-0.30, -0.95, 0])


def akt_blob(F, c):
    return blob(F, c, "Akt", PURPLE, 1.7, 1.0, 34)


def akt_cup(F, c, closed=False):
    return cup(np.array(c) + F.k * CUP_OFF, CUP_R * F.k, "up", closed)


def akt_loop(F, c):
    return Arc(radius=0.2 * F.k, start_angle=-PI / 2, angle=PI, stroke_color=PURPLE, stroke_width=F.sw(5)).move_arc_center_to(np.array(c) + F.k * LOOP_OFF)


def akt_tail(F, c):
    a, b = np.array(c) + F.k * TAIL_OFF, np.array(c) + F.k * TAIL_TIP
    return VGroup(Line(a, b, color=PURPLE, stroke_width=F.sw(5)), Dot(b, radius=0.08 * F.k, color=PURPLE))


def kinase_p(F, c, tip):
    """a phosphate sitting on an Akt site (c = Akt body centre)."""
    return pbadge(F, 0.17).move_to(np.array(c) + F.k * tip)


# ---------------------------------------------------------------------------------------------
class Film(SpokenScene):
    def drift(self, m, amp=0.16, ph=0.0):
        """let a mobject wander a little around where it is now (the cytosol is crowded and moving)."""
        def offset():
            t = self.renderer.time + ph
            return amp * np.array([np.sin(0.9 * t), 0.8 * np.cos(1.3 * t), 0.0])
        state = {"off": offset()}

        def upd(mob):
            off = offset()
            mob.shift(off - state["off"])
            state["off"] = off
        m.add_updater(upd)
        m._drift = (upd, state)

    def stop(self, m):
        """stop the wandering where it is."""
        if getattr(m, "_drift", None):
            m.remove_updater(m._drift[0])
            m._drift = None

    def attach(self, g, *parts):
        """make parts (already on screen) belong to g so they travel with it."""
        self.remove(*parts)
        g.add(*parts)

    def outro(self, *anims, then=None, run_time=0.4):
        """hold until the narration ends, clear what the next scene does not inherit, then (optionally)
        change framing. These run after the last word, so they add a short breath between scenes."""
        rest = self.narration_s - 0.02 - self.elapsed()
        if rest > 0:
            self.wait(rest)
        if anims:
            self.play(*anims, run_time=run_time)
        if then:
            self.play(*then, run_time=1.0)
            self.wait(0.15)
        self.finish()


class S00Title(TitleCard):
    LESSON = "PI 3-Kinase, Akt and Insulin"
    TITLE = "A membrane address for Akt"


# ---------------------------------------------------------------------------------------------
class S01Puzzle(Film):
    """insulin stays outside; glucose is stored; Akt waits inside; the path between them is unknown. (WIDE)"""

    def construct(self):
        F = WIDE
        mem = membrane(F)
        out_l = T("outside the cell", 22, GREY).move_to([-5.0, 2.55, 0])
        in_l = T("inside the cell", 22, GREY).move_to([-5.0, 1.25, 0])
        ins = bchip("insulin", YELLOW, 34).move_to([0, 3.0, 0])
        self.at("Insulin never")
        self.play(FadeIn(mem), FadeIn(out_l), FadeIn(in_l), FadeIn(ins, shift=DOWN * 0.2), run_time=0.4)
        bar = Line([-1.05, 2.13, 0], [1.05, 2.13, 0], color=RED, stroke_width=10)
        no = T("never crosses", 28, RED).move_to([2.55, 2.55, 0])
        self.at("never crosses")
        self.play(ins.animate.move_to([0, 2.55, 0]), Create(bar), FadeIn(no), run_time=0.5)
        self.play(ins.animate(rate_func=there_and_back).shift(DOWN * 0.12), run_time=0.4)

        ck = clock([-4.4, 0.0, 0], 0.55)
        mins = T("minutes", 26, GREY).move_to([-4.4, -0.85, 0])
        glu = bchip("glucose", TEXT, 32).move_to([5.1, 2.85, 0])
        self.at("Yet within minutes")
        self.play(FadeIn(ck), FadeIn(mins), FadeIn(glu, shift=DOWN * 0.15), run_time=0.4)
        self.play(Rotate(ck.hand, -TAU / 5, about_point=ck.c), run_time=0.8)
        self.at("pulls glucose")
        self.play(glu.animate.move_to([5.1, 0.7, 0]), run_time=0.9)
        gly = bchip("glycogen", TEXT, 32).move_to([5.1, 0.7, 0])
        self.at("stores it as")
        self.play(ReplacementTransform(glu, gly), run_time=0.5)

        akt = blob(F, [0, -2.45, 0], "Akt", PURPLE, 1.7, 1.0, 34)
        akt.scale(1.3)
        self.at("one kinase")
        self.play(FadeIn(akt, scale=0.8), run_time=0.5)
        self.at("drifts")
        self.drift(akt)
        cyt = T("cytosol", 26, GREY).move_to([-2.6, -2.45, 0])
        self.at("in the cytosol")
        self.play(FadeIn(cyt), run_time=0.4)
        inact = T("inactive", 28, GREY).move_to([2.6, -2.45, 0])
        self.at("inactive")
        self.play(FadeIn(inact), run_time=0.4)

        # the path nobody has drawn yet
        path = DashedLine([0, 1.66, 0], [0, -1.6, 0], color=GREY, stroke_width=4, dash_length=0.12)
        tipm = Triangle(fill_color=GREY, fill_opacity=1, stroke_width=0).scale(0.14).rotate(PI).move_to([0, -1.62, 0])
        qs = VGroup()
        for y in (0.95, 0.0, -0.95):
            shape = RoundedRectangle(corner_radius=0.14, width=0.95, height=0.78)
            back = shape.copy().set_stroke(width=0).set_fill(BG, 1).move_to([0, y, 0])
            edge = DashedVMobject(shape.copy().move_to([0, y, 0]), num_dashes=24).set_color(GREY)
            q = T("?", 38, TEXT, weight=BOLD).move_to([0, y, 0])
            qs.add(VGroup(back, edge, q))
        self.at("How does a message")
        self.play(Create(path), FadeIn(tipm), LaggedStart(*[FadeIn(b, scale=0.8) for b in qs], lag_ratio=0.3), run_time=1.1)
        self.at("from outside")
        self.play(*glow(ins[1], ins[2], s=1.12), run_time=0.6)
        self.at("reach it")
        self.play(LaggedStart(*[pop(b[2], 1.6) for b in qs], lag_ratio=0.25), *glow(akt.body, akt.lbl, s=1.1), run_time=1.0)
        # clear everything the next scene rebuilds differently; Akt settles back to its start spot
        self.stop(akt)
        self.outro(FadeOut(VGroup(ck, mins, gly, bar, no, cyt, inact, out_l, in_l)), akt.animate.move_to([0, -2.45, 0]))


# ---------------------------------------------------------------------------------------------
class S02Relay(Film):
    """insulin -> receptor -> IRS-1 tail -> SH2 cups -> PI 3-kinase. (WIDE, zoomed to RELAY, ending in a zoom to CLOSE)"""

    def construct(self):
        W, R, C = WIDE, RELAY, CLOSE
        k, p = R.k, R.p
        mem = membrane(W)
        ins = bchip("insulin", YELLOW, 34).move_to([0, 2.55, 0])
        path = DashedLine([0, 1.66, 0], [0, -1.6, 0], color=GREY, stroke_width=4, dash_length=0.12)
        tipm = Triangle(fill_color=GREY, fill_opacity=1, stroke_width=0).scale(0.14).rotate(PI).move_to([0, -1.62, 0])
        qs = VGroup()
        for y in (0.95, 0.0, -0.95):
            shape = RoundedRectangle(corner_radius=0.14, width=0.95, height=0.78)
            back = shape.copy().set_stroke(width=0).set_fill(BG, 1).move_to([0, y, 0])
            edge = DashedVMobject(shape.copy().move_to([0, y, 0]), num_dashes=24).set_color(GREY)
            qs.add(VGroup(back, edge, T("?", 38, TEXT, weight=BOLD).move_to([0, y, 0])))
        akt = blob(W, [0, -2.45, 0], "Akt", PURPLE, 1.7, 1.0, 34)
        akt.scale(1.3)
        self.add(mem, path, tipm, qs, ins, akt)

        # the unknown path gives way to the real one; the view moves in on the left; insulin goes to its receptor
        self.play(FadeOut(VGroup(path, tipm, qs)), mem.animate.become(membrane(R)),
                  ins.animate.scale(k).move_to(p(REC_X, 2.55)), akt.animate.scale(k / 1.3).move_to(p(WAIT)), run_time=0.9)
        self.drift(akt, ph=1.0)

        # the receptor: a bar through the membrane, its kinase on the inner end
        rbar_h = 1.6
        rback = RoundedRectangle(corner_radius=0.12 * k, width=0.42 * k, height=rbar_h * k, stroke_width=0, fill_color=BG, fill_opacity=1)
        rbar = RoundedRectangle(corner_radius=0.12 * k, width=0.42 * k, height=rbar_h * k, stroke_color=BLUE, stroke_width=R.sw(4),
                                fill_color=BLUE, fill_opacity=0.4)
        rkin = RoundedRectangle(corner_radius=0.16 * k, width=0.95 * k, height=0.5 * k, stroke_color=BLUE, stroke_width=R.sw(4),
                                fill_color=BLUE, fill_opacity=0.55).move_to(p(REC_X, 0.92))
        rec = VGroup(rback, rbar).move_to(p(REC_X, 1.95))
        rec_all = VGroup(rec, rkin)
        rec_lbl = T("receptor", 26, BLUE).move_to(p(-5.2, 2.4))
        self.at("its receptor")
        self.play(GrowFromPoint(rec_all, p(REC_X, MEM_Y)), ins.animate.move_to(p(REC_X, 3.1)), FadeIn(rec_lbl), run_time=0.7)
        tk = T("tyrosine\nkinase", 24, BLUE, line_spacing=0.8).move_to(p(-5.25, 0.92))
        self.at("tyrosine kinase")
        self.play(FadeIn(tk, shift=RIGHT * 0.1), *glow(rkin, s=1.1), run_time=0.6)

        # the receptor phosphorylates itself
        rp = [pbadge(R).move_to(p(-3.6, 1.0)), pbadge(R).move_to(p(REC_X, 0.45))]
        self.at("adds phosphates")
        self.play(LaggedStart(*[FadeIn(b, scale=0.4) for b in rp], lag_ratio=0.4), run_time=0.7)

        # IRS-1 appears beside it and takes a phosphate
        irs = blob(R, p(IRS_X, IRS_Y), "IRS-1", TEAL, 1.2, 0.62, 26)
        self.at("and then to those")
        self.play(FadeIn(irs, shift=LEFT * 0.15), run_time=0.5)
        p_irs = pbadge(R)
        p_irs.move_to(rp[0])
        self.at("docking protein")
        self.add(p_irs)
        self.play(p_irs.animate(path_arc=-0.6).move_to(p(IRS_X - 0.5, IRS_Y - 0.45)), run_time=0.7)
        dock_lbl = T("docking protein", 24, TEAL).move_to(p(-0.35, IRS_Y))
        self.play(FadeIn(dock_lbl), run_time=0.3)

        # held at the membrane
        grip = Line(p(IRS_X - 0.55, MEM_BOT), p(IRS_X + 0.55, MEM_BOT), color=TEAL, stroke_width=8)
        self.at("held at the membrane")
        self.play(FadeOut(dock_lbl), Create(grip), run_time=0.5)
        self.play(FadeOut(grip), run_time=0.3)

        # a long tail with many tyrosines
        tail = Line(p(IRS_X, IRS_Y - 0.31), p(IRS_X, TAIL_END), color=TEAL, stroke_width=R.sw(5))
        dots = [Circle(radius=0.1 * k, stroke_color=TEAL, stroke_width=R.sw(3), fill_color=TEAL, fill_opacity=1).move_to(p(IRS_X, y)) for y in TAIL_Y]
        self.at("long tail")
        self.play(Create(tail), p_irs.animate.move_to(p(IRS_X, TAIL_Y[0])), LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.2), run_time=1.2)
        self.bring_to_front(p_irs)
        self.at("many tyrosines")
        self.play(LaggedStart(*[pop(d, 1.8) for d in dots[1:]], lag_ratio=0.25), run_time=0.9)

        # the receptor phosphorylates the tail
        tp = [pbadge(R).move_to(rp[i % 2].get_center()) for i in range(3)]
        self.at("has phosphorylated")
        self.add(*tp)
        self.play(LaggedStart(*[t.animate(path_arc=-0.5 if i == 0 else 0.4).move_to(p(IRS_X, y)) for i, (t, y) in enumerate(zip(tp, TAIL_Y[1:]))],
                              lag_ratio=0.3), run_time=1.4)
        tip_badges = [p_irs] + tp

        # proteins with SH2 domains dock: three of them, each with a pink cup that closes on a phosphate
        pi3k = blob(R, p(PI3K_C) + RIGHT * 0.8 * k, "protein", GREY, 2.1, 0.8, 24, bold=False)
        others = [blob(R, p(-1.22, y) + RIGHT * 0.8 * k, "protein", GREY, 1.4, 0.5, 22, bold=False) for y in TAIL_Y[1:3]]
        cups_open = [cup(p(IRS_X, y), CUP_R * k, "left", False) for y in TAIL_Y[:3]]
        self.at("proteins with")
        self.play(FadeIn(pi3k, shift=LEFT * 0.2), *[FadeIn(o, shift=LEFT * 0.2) for o in others], run_time=0.6)
        self.at("dock on it")
        self.play(pi3k.animate.move_to(p(PI3K_C)), *[o.animate.move_to(p(-1.22, y)) for o, y in zip(others, TAIL_Y[1:3])],
                  *[FadeIn(c) for c in cups_open], run_time=0.9)
        cups_closed = [cup(p(IRS_X, y), CUP_R * k, "left", True) for y in TAIL_Y[:3]]
        self.play(*[Transform(c, cc) for c, cc in zip(cups_open, cups_closed)], run_time=0.5)

        # the SH2 domain is the cup
        sh2 = T("SH2 domain", 28, PINK, weight=BOLD).move_to(p(-0.3, -1.62))
        ptr = Line(p(-1.45, -1.5), p(-2.0, -1.22), color=PINK, stroke_width=3)
        self.at("domain binds")
        self.play(FadeIn(sh2), Create(ptr), *glow(*cups_open, s=1.3), run_time=0.7)
        self.at("a phosphorylated")
        self.play(*[pop(b, 1.4) for b in tip_badges[:3]], run_time=0.7)

        # one of them is PI 3-kinase
        pi3k_real = blob(R, p(PI3K_C), "PI 3-kinase", ORANGE, 2.1, 0.8, 24)
        self.at("one such protein")
        self.play(ReplacementTransform(pi3k, pi3k_real), run_time=0.7)
        self.play(*glow(pi3k_real.body, pi3k_real.lbl, s=1.08), run_time=0.5)

        # clear the two other proteins, then move in on the membrane (CLOSE)
        world = VGroup(mem, rec_all, rec_lbl, tk, ins, *rp, irs, tail, *dots, *tip_badges, pi3k_real, cups_open[0], akt)
        self.stop(akt)
        self.outro(FadeOut(VGroup(*others, sh2, ptr, cups_open[1], cups_open[2])),
                   then=[world.animate.scale(C.k / R.k, about_point=ORIGIN).shift(C.k * np.array([R.fx - C.fx, R.fy - C.fy, 0]))])


# ---------------------------------------------------------------------------------------------
def relay_end(F):
    """what scene 2 leaves behind, rebuilt in framing F: membrane, IRS-1 and its phosphorylated tail,
    PI 3-kinase docked on the top phosphate, and Akt waiting in the cytosol (not drifting yet)."""
    mem = membrane(F)
    irs = blob(F, F.p(IRS_X, IRS_Y), "IRS-1", TEAL, 1.2, 0.62, 26)
    tail = Line(F.p(IRS_X, IRS_Y - 0.31), F.p(IRS_X, TAIL_END), color=TEAL, stroke_width=F.sw(5))
    dots = [Circle(radius=0.1 * F.k, stroke_color=TEAL, stroke_width=F.sw(3), fill_color=TEAL, fill_opacity=1).move_to(F.p(IRS_X, y)) for y in TAIL_Y]
    badges = [pbadge(F).move_to(F.p(IRS_X, y)) for y in TAIL_Y]
    pi3k = blob(F, F.p(PI3K_C), "PI 3-kinase", ORANGE, 2.1, 0.8, 24)
    cp = cup(F.p(IRS_X, TAIL_Y[0]), CUP_R * F.k, "left", True)
    akt = blob(F, F.p(WAIT), "Akt", PURPLE, 1.7, 1.0, 34)
    return mem, irs, tail, dots, badges, pi3k, cp, akt


# ---------------------------------------------------------------------------------------------
class S03Lipid(Film):
    """PI 3-kinase at the membrane turns PIP2 into PIP3: a membrane address. (CLOSE)"""

    def construct(self):
        F = CLOSE
        mem, irs, tail, dots, badges, pi3k, cp, akt = relay_end(F)
        self.add(mem, tail, *dots, irs, *badges, pi3k, cp, akt)
        self.drift(akt, ph=2.0)

        # the substrate: PIP2 lipid heads hang from the inner face
        lips = lipids(F)
        self.at("now sits at")
        self.play(*glow(pi3k.body, pi3k.lbl, s=1.06), run_time=0.6)
        self.at("the membrane")
        self.play(LaggedStart(*[FadeIn(l, shift=DOWN * 0.15) for l in lips], lag_ratio=0.12), run_time=1.0)
        self.at("where its substrate")
        self.play(*glow(*[l[1] for l in lips], s=1.25), run_time=0.7)
        lbl2 = T("PIP2", 28, GREY, weight=BOLD).move_to(F.p(4.85, HEAD_Y))
        self.at("a lipid called")
        self.play(FadeIn(lbl2, shift=LEFT * 0.15), run_time=0.5)

        # the catalytic subunit adds a phosphate to the 3 position
        cat = T("catalytic subunit", 24, ORANGE).move_to(F.p(-0.65, -0.42))
        cat_ptr = Line(F.p(-0.4, -0.2), F.p(-0.4, 0.12), color=ORANGE, stroke_width=3)
        self.at("catalytic subunit")
        self.play(FadeIn(cat), Create(cat_ptr), *glow(pi3k.body, s=1.05), run_time=0.7)
        newp = [lip_badge(F, i) for i in range(len(LIP_X))]
        src = pbadge(F, 0.17).move_to(F.p(0.3, 0.55))
        self.at("adds a phosphate")
        self.play(FadeIn(src, scale=0.4), run_time=0.3)
        self.play(src.animate.move_to(newp[0].get_center()), run_time=0.6)
        self.remove(src)
        self.add(newp[0])
        lab3 = T("3-phosphate", 24, GOLD).move_to(F.p(1.4, 0.5))
        self.at("position of the")
        self.play(FadeIn(lab3, shift=UP * 0.1), pop(newp[0], 1.5), run_time=0.6)

        # the product is PIP3
        lbl3 = T("PIP3", 28, TEXT, weight=BOLD).move_to(F.p(4.85, HEAD_Y))
        self.at("The product")
        self.play(FadeOut(lab3), FadeOut(cat), FadeOut(cat_ptr), ReplacementTransform(lbl2, lbl3),
                  LaggedStart(*[FadeIn(b, scale=0.4) for b in newp[1:]], lag_ratio=0.15), run_time=1.3)
        addr = T("membrane address", 30, TEXT, weight=BOLD).move_to(F.p(2.25, 0.5))
        self.at("is a membrane")
        self.play(FadeIn(addr, shift=UP * 0.1), LaggedStart(*[pop(b, 1.4) for b in newp], lag_ratio=0.1), run_time=1.1)
        self.stop(akt)
        self.outro(FadeOut(addr))


# ---------------------------------------------------------------------------------------------
def lipid_row_pip3(F):
    """the row after PI 3-kinase has worked: lipids with a phosphate each, and the PIP3 label."""
    lips = lipids(F)
    badges = [lip_badge(F, i) for i in range(len(LIP_X))]
    lbl3 = T("PIP3", 28, TEXT, weight=BOLD).move_to(F.p(4.85, HEAD_Y))
    return lips, badges, lbl3


class S04Grip(Film):
    """the PH domain is a cup on Akt's amino end; PIP3 holds Akt against the membrane. (CLOSE)"""

    def construct(self):
        F = CLOSE
        mem, irs, tail, dots, badges, pi3k, cp, akt = relay_end(F)
        lips, lb, lbl3 = lipid_row_pip3(F)
        self.add(mem, tail, *dots, irs, *badges, pi3k, cp, *lips, *lb, lbl3, akt)
        self.drift(akt, ph=3.0)
        k = F.k

        c0 = akt.body.get_center()
        pcup = akt_cup(F, c0, False)
        self.at("domain at")
        self.stop(akt)
        self.play(GrowFromCenter(pcup), run_time=0.5)
        self.attach(akt, pcup)
        self.drift(akt, ph=3.5)
        ph = T("PH domain", 26, PINK, weight=BOLD).move_to(pcup.get_center() + np.array([-1.95, 0.1, 0]))
        self.play(FadeIn(ph, shift=RIGHT * 0.1), run_time=0.4)
        am = T("amino end", 24, GREY).move_to(akt.body.get_left() + np.array([-0.95, -0.15, 0]))
        self.at("amino end")
        self.play(FadeIn(am, shift=RIGHT * 0.1), run_time=0.4)

        self.at("domain binds")
        self.play(*glow(pcup, s=1.3), LaggedStart(*[pop(b, 1.4) for b in lb], lag_ratio=0.08), run_time=0.9)

        # Akt leaves the cytosol and rises to the lipid
        self.at("leaves the cytosol")
        self.stop(akt)
        goal = F.p(AKT_C)
        below = goal + np.array([0.0, -0.5 * k, 0])
        self.play(FadeOut(ph), FadeOut(am), akt.animate.move_to(below), run_time=1.2)
        closed = akt_cup(F, goal, True)
        self.at("lipid holds it")
        self.play(akt.animate.move_to(goal), run_time=0.5)
        self.play(Transform(pcup, closed), run_time=0.4)
        self.play(*glow(pcup, s=1.25), run_time=0.4)
        hold = T("held against the membrane", 26, GREY).move_to(F.p(2.4, -0.95))
        self.at("against the membrane")
        self.play(FadeIn(hold, shift=UP * 0.1), run_time=0.5)
        self.at("now at the address")
        self.play(*glow(akt.body, akt.lbl, s=1.08), *glow(*lb, s=1.25), run_time=0.8)
        self.outro(FadeOut(VGroup(hold, irs, tail, *dots, *badges, pi3k, cp)))


# ---------------------------------------------------------------------------------------------
def pdk_blob(F, c):
    return blob(F, c, "PDK1", ORANGE, 1.5, 0.9, 30)


def pdk_cup(F, c, closed=False):
    return cup(np.array(c) + F.k * np.array([-0.45, 0.80, 0]), CUP_R * F.k, "up", closed)


def held_akt(F):
    """Akt held at the membrane by its PH cup (as scene 4 leaves it)."""
    akt = akt_blob(F, F.p(AKT_C))
    cp = akt_cup(F, F.p(AKT_C), True)
    akt.add(cp)
    akt.cup = cp
    return akt


class S05Two(Film):
    """PDK1, held by its own PH cup, phosphorylates the loop; mTORC2 phosphorylates the tail; Akt is on. (CLOSE)"""

    def construct(self):
        F = CLOSE
        k = F.k
        mem = membrane(F)
        lips, lb, lbl3 = lipid_row_pip3(F)
        akt = held_akt(F)
        self.add(mem, *lips, *lb, lbl3, akt)
        ac = F.p(AKT_C)

        # a second kinase, held by its own PH domain next to Akt
        start = np.array([4.7, -1.2, 0])
        pdk = pdk_blob(F, F.p(start))
        self.at("A second kinase")
        self.play(FadeIn(pdk, shift=UP * 0.2), run_time=0.5)
        pc = pdk_cup(F, F.p(start), False)
        self.at("its own")
        self.play(GrowFromCenter(pc), run_time=0.5)
        self.attach(pdk, pc)
        goal = F.p(PDK_C)
        self.at("holds it there")
        self.play(pdk.animate.move_to(goal), run_time=0.9)
        self.play(Transform(pc, pdk_cup(F, goal, True)), run_time=0.4)
        self.play(*glow(pc, s=1.25), run_time=0.4)

        # PDK1 puts a phosphate on a threonine in Akt's activation loop
        loop = akt_loop(F, ac)
        p1 = pbadge(F, 0.17).move_to(goal + np.array([-0.75 * k, -0.05, 0]))
        self.at("adds a phosphate")
        self.play(GrowFromCenter(loop), FadeIn(p1, scale=0.4), run_time=0.6)
        self.attach(akt, loop)
        tip1 = ac + k * LOOP_TIP
        lead1 = Line(F.p(2.78, 0.0), F.p(2.78, -2.0), color=GREY, stroke_width=2.5)
        thr = T("threonine in the activation loop", 24, GOLD).move_to(F.p(2.78, -2.2))
        self.at("a threonine")
        self.play(FadeIn(thr, shift=UP * 0.1), Create(lead1), run_time=0.6)
        self.at("activation loop")
        self.play(p1.animate(path_arc=0.5).move_to(tip1), run_time=0.7)
        self.at("needs a phosphate")
        self.play(pop(p1, 1.5), run_time=0.7)

        # mTORC2 puts a second phosphate near the tail
        m2c = F.p(0.15, -1.15)
        m2 = blob(F, m2c, "mTORC2", ORANGE, 1.7, 0.7, 26)
        self.at("A separate kinase")
        self.play(FadeIn(m2, shift=RIGHT * 0.2), run_time=0.5)
        tail = akt_tail(F, ac)
        p2 = pbadge(F, 0.17).move_to(m2c + np.array([0.85 * k + 0.3, 0.0, 0]))
        self.at("second phosphate")
        self.play(Create(tail), FadeIn(p2, scale=0.4), run_time=0.6)
        self.attach(akt, tail)
        tip2 = ac + k * TAIL_TIP
        lead2 = Line(F.p(AKT_C[0] + TAIL_TIP[0], -1.0), F.p(AKT_C[0] + TAIL_TIP[0], -1.42), color=GREY, stroke_width=2.5)
        ser = T("serine near the tail", 24, GOLD).move_to(F.p(AKT_C[0] + TAIL_TIP[0], -1.62))
        self.at("near the tail")
        self.play(p2.animate(path_arc=-0.5).move_to(tip2), run_time=0.7)
        self.at("on a serine")
        self.play(FadeIn(ser, shift=UP * 0.1), Create(lead2), run_time=0.5)

        # the first does most of the work; together, full activity
        self.at("first phosphate")
        self.play(p1.animate.scale(1.45), run_time=0.5)
        self.at("does most of")
        self.play(*glow(p1, s=1.25), run_time=0.6)
        self.at("the second adds")
        self.play(pop(p2, 1.5), run_time=0.6)
        act = T("active", 30, GREEN, weight=BOLD).move_to(F.p(0.05, 0.05))
        self.at("full activity")
        self.play(akt.body.animate.set_stroke(GREEN, F.sw(6)).set_fill(GREEN, 0.2), akt.lbl.animate.set_color(GREEN),
                  FadeIn(act, shift=RIGHT * 0.1), run_time=0.7)
        self.outro(FadeOut(VGroup(pdk, m2, thr, lead1, ser, lead2, act)), p1.animate.scale(1 / 1.45))


# ---------------------------------------------------------------------------------------------
def full_akt(F, c, with_p=False, green=False):
    """Akt with its cup, loop and tail (optionally with both phosphates), centre at screen point c."""
    akt = akt_blob(F, c)
    cp = akt_cup(F, c, False)
    lp = akt_loop(F, c)
    tl = akt_tail(F, c)
    akt.add(cp, lp, tl)
    akt.cup, akt.loop, akt.tail = cp, lp, tl
    akt.pl = kinase_p(F, c, LOOP_TIP)
    akt.pt = kinase_p(F, c, TAIL_TIP)
    if with_p:
        akt.add(akt.pl, akt.pt)
    if green:
        akt.body.set_stroke(GREEN, F.sw(6)).set_fill(GREEN, 0.2)
        akt.lbl.set_color(GREEN)
    return akt


class S06Rule(Film):
    """three checks on the finished Akt; then Akt with no insulin: normal stays in the cytosol, an anchored copy is on."""

    def construct(self):
        F = CLOSE
        k = F.k
        mem = membrane(F)
        lips, lb, lbl3 = lipid_row_pip3(F)
        akt = held_akt(F)
        ac = F.p(AKT_C)
        lp, tl = akt_loop(F, ac), akt_tail(F, ac)
        pl, pt = kinase_p(F, ac, LOOP_TIP), kinase_p(F, ac, TAIL_TIP)
        akt.add(lp, tl)
        akt.body.set_stroke(GREEN, F.sw(6)).set_fill(GREEN, 0.2)
        akt.lbl.set_color(GREEN)
        self.add(mem, *lips, *lb, lbl3, akt, pl, pt)

        # why a lipid and two phosphates? each is a check
        self.at("a lipid")
        self.play(*glow(akt.cup, s=1.3), run_time=0.6)
        self.at("two phosphates")
        self.play(pop(pl, 1.5), pop(pt, 1.5), run_time=0.7)
        t_a = tick(F.p(0.45, 0.62), 0.22)
        t_b = tick(F.p(3.15, 0.2), 0.22)
        t_c = tick(F.p(0.9, -0.95), 0.22)
        self.at("Each is a")
        self.play(LaggedStart(Create(t_a), Create(t_b), Create(t_c), lag_ratio=0.45), run_time=1.4)
        self.at("on mainly where")
        self.play(*glow(*lb, s=1.3), run_time=0.8)

        # reset to a new question: no insulin. The membrane stays; everything else is rebuilt wider.
        F2 = Fr(1.3, 0.0, 0.35)
        p = F2.p
        k2 = F2.k
        self.at("With no insulin")
        self.play(FadeOut(VGroup(*lips, *lb, lbl3, akt, pl, pt, t_a, t_b, t_c)),
                  mem.animate.become(membrane(F2)), run_time=0.7)
        noins = T("no insulin", 32, YELLOW, weight=BOLD).move_to([0, 3.0, 0])
        div = DashedLine(p(0, 1.5), p(0, -2.6), color=GREY, stroke_width=3, dash_length=0.12)
        tl_l = T("normal Akt", 30, TEXT, weight=BOLD).move_to([-3.6, 3.0, 0])
        self.play(FadeIn(noins, shift=DOWN * 0.1), Create(div), FadeIn(tl_l), run_time=0.6)
        left = full_akt(F2, p(-2.6, -1.0))
        self.at("stays in the")
        self.play(FadeIn(left, shift=UP * 0.2), run_time=0.5)
        self.drift(left, ph=0.5)
        inact = T("inactive", 28, GREY).move_to(p(-2.6, -2.45))
        cyt = T("cytosol", 24, GREY).move_to(p(-4.6, -1.0))
        self.play(FadeIn(inact), FadeIn(cyt), run_time=0.4)

        # the anchored copy
        tl_r = T("anchored Akt", 30, TEXT, weight=BOLD).move_to([3.6, 3.0, 0])
        rx = 2.6
        right = full_akt(F2, p(rx, -1.0))
        a0 = right.body.get_center()
        anc_pts = [a0 + k2 * np.array(v) for v in ([0.6, 0.5, 0], [0.35, 0.95, 0], [0.85, 1.35, 0], [0.6, 1.75, 0])]
        anchor = CubicBezier(*anc_pts, color=GREY, stroke_width=7)
        anc_lbl = T("fatty acid anchor", 24, GREY).move_to(a0 + k2 * np.array([1.6, 1.3, 0]))
        self.at("permanent fatty acid")
        self.play(FadeIn(tl_r), FadeIn(right, shift=UP * 0.2), run_time=0.5)
        self.drift(right, ph=2.0)
        self.at("anchor")
        self.play(Create(anchor), FadeIn(anc_lbl, shift=RIGHT * 0.1), run_time=0.6)
        self.stop(right)
        self.attach(right, anchor)
        goal = p(rx, AKT_C[1])
        dy = goal[1] - right.body.get_center()[1]
        self.at("sits at the membrane")
        self.play(right.animate.shift(goal - right.body.get_center() + np.array([0.0, 0.0, 0.0])),
                  anc_lbl.animate.shift(UP * dy), run_time=1.0)
        bc = right.body.get_center()
        pl2, pt2 = kinase_p(F2, bc, LOOP_TIP), kinase_p(F2, bc, TAIL_TIP)
        self.at("gains both")
        self.play(FadeIn(pl2, scale=0.4), run_time=0.4)
        self.play(FadeIn(pt2, scale=0.4), run_time=0.4)
        act = T("active", 30, GREEN, weight=BOLD).move_to(bc + np.array([-2.0, -0.1, 0]))
        self.at("and is active")
        self.play(right.body.animate.set_stroke(GREEN, 6).set_fill(GREEN, 0.2), right.lbl.animate.set_color(GREEN),
                  FadeIn(act, shift=RIGHT * 0.1), run_time=0.7)

        # the rule: what the anchor does by force, PIP3 does by being an address
        cx = right.cup.get_center()[0]
        stem = Line(p(0, MEM_BOT)[1] * UP + cx * RIGHT, p(0, HEAD_Y + 0.15)[1] * UP + cx * RIGHT, color=GREY, stroke_width=3)
        head = Circle(radius=0.15 * k2, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.5).move_to([cx, p(0, HEAD_Y)[1], 0])
        badge = pbadge(F2, 0.17).move_to([cx, p(0, BADGE_Y)[1], 0])
        lab = T("PIP3", 28, TEXT, weight=BOLD).move_to([cx + 1.2, p(0, HEAD_Y)[1], 0])
        closed = cup(np.array([cx, p(0, BADGE_Y)[1], 0]), CUP_R * k2, "up", True)
        self.at("Keep this rule")
        right.remove(anchor)
        self.add(anchor)
        self.play(FadeOut(anchor), FadeOut(anc_lbl), run_time=0.4)
        self.at("first puts")
        self.play(FadeIn(VGroup(stem, head)), FadeIn(badge, scale=0.4), FadeIn(lab), run_time=0.6)
        self.play(Transform(right.cup, closed), run_time=0.4)
        self.at("right place")
        self.play(*glow(right.body, right.lbl, s=1.08), *glow(right.cup, s=1.3), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "PIP3 puts Akt in place and opens it."
