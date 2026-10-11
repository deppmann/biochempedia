"""Death receptors, BCL-2 and caspases: the safeguard comes before the cut  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  RED     = caspases and the cut (a dashed outline is an inactive precursor, a solid one is active)
  TEAL    = the platform that gathers caspases: the bar, APAF-1, the wheel (apoptosome)
  ORANGE  = cytochrome c
  PURPLE  = effectors BAX and BAK
  GREEN   = guards (BCL-2, BCL-xL) and the bar that holds an effector in check
  YELLOW  = sensors (BAD, BID) and their BH3 helix, and the stress that switches them on
  GREY    = membranes, labels, the target protein, things that are not there or not yet used
  TEXT    = names, ghosts that are struck out, the gate

No molecular structures: caspases, effectors and guards are labelled blobs, the groove is a dashed
slot, the helix is a labelled capsule, the wheel is seven small blobs round a hub, membranes are bars.

Story, in the order it is told (each scene answers "what holds this off?" for the one before):
  1 puzzle    ready within hours, never by mistake; a cut cannot be undone
  2 gather    a caspase is stored whole; step one is a gathering, every step after is a cut
  3 parts     the platform's two parts are kept apart by the outer mitochondrial membrane
  4 family    what opens that membrane (effectors), what holds them (guards), what fills a guard (sensors)
  5 balance   sensors must outnumber guards; then the membrane opens and cytochrome c leaves
  6 rule      the whole chain in order; the decision is the first link
"""
from types import SimpleNamespace as NS

import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F28C28"


# ---------------------------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------------------------
def rr(w, h, r=None):
    return RoundedRectangle(corner_radius=r if r is not None else min(0.25, h / 2.2), width=w, height=h)


def bchip(text, color=BLUE, size=24, pad=0.2, **kw):
    """chip with an opaque backing so lines drawn behind it do not show through."""
    c = chip(text, color, size=size, pad=pad, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def ghost_chip(text, size=22):
    """a dashed grey chip: something that is NOT there."""
    t = T(text, size, GREY)
    box = RoundedRectangle(corner_radius=0.14, width=t.width + 0.4, height=t.height + 0.32)
    return VGroup(DashedVMobject(box, num_dashes=max(18, int(box.width * 9))).set_color(GREY), t)


def strike(m, color=TEXT, w=7):
    return Line(m.get_corner(DL) + [-0.08, -0.04, 0], m.get_corner(UR) + [0.08, 0.04, 0], color=color, stroke_width=w)


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def pop(m, s=1.3):
    return m.animate(rate_func=there_and_back).scale(s)


def glow(*mobs, s=1.1, color=TEXT):
    return [Indicate(m, color=color, scale_factor=s) for m in mobs]


def clock(center, r=0.45):
    center = np.array(center, float)
    face = Circle(radius=r, stroke_color=GREY, stroke_width=4).move_to(center)
    ticks = VGroup(*[Line(center + (r - 0.11) * v, center + r * v, color=GREY, stroke_width=4) for v in (UP, RIGHT, DOWN, LEFT)])
    hand = Line(center, center + UP * (r - 0.15), color=TEXT, stroke_width=5)
    pin = Dot(center, radius=0.05, color=TEXT)
    g = VGroup(face, ticks, hand, pin)
    g.hand, g.c = hand, center
    return g


def blob(label, color, w, h, size=22, fill=0.3, pos=ORIGIN, r=None):
    """a labelled rounded blob with an opaque backing: [back, body, label]."""
    back = rr(w, h, r).set_stroke(width=0).set_fill(BG, 1)
    body = rr(w, h, r).set_stroke(color, 3.5).set_fill(color, fill)
    lbl = T(label, size, color) if label else Dot(radius=0.001, color=BG)
    g = VGroup(back, body, lbl)
    g.body, g.lbl = body, lbl
    return g.move_to(pos)


# ---- caspases: dashed outline = inactive precursor, solid = active -----------------------------
def casp(label="", w=1.55, h=0.95, size=22, active=False, pos=ORIGIN):
    """[back, fill, dashed outline, solid outline, label]"""
    back = rr(w, h).set_stroke(width=0).set_fill(BG, 1)
    fl = rr(w, h).set_stroke(width=0).set_fill(RED, 0.5 if active else 0.1)
    dash = DashedVMobject(rr(w, h), num_dashes=max(14, int(2 * (w + h) * 4))).set_stroke(RED, 3.5, opacity=0.0 if active else 1.0)
    solid = rr(w, h).set_stroke(RED, 4.5, opacity=1.0 if active else 0.0).set_fill(RED, 0)
    lbl = T(label, size, TEXT) if label else Dot(radius=0.001, color=BG)
    g = VGroup(back, fl, dash, solid, lbl)
    g.fl, g.dash, g.solid, g.lbl = fl, dash, solid, lbl
    return g.move_to(pos)


def casp_on(g):
    """animations that switch a caspase on: dashed outline becomes solid, the fill deepens."""
    return [g.fl.animate.set_fill(RED, 0.5), g.dash.animate.set_stroke(opacity=0.0), g.solid.animate.set_stroke(opacity=1.0)]


def slash(c, L=1.6, ang=-65, color=RED, w=9):
    a = ang * DEGREES
    d = np.array([np.cos(a), np.sin(a), 0]) * L / 2
    c = np.array(c, float)
    return Line(c - d, c + d, color=color, stroke_width=w)


def cut_play(scene, c, L=1.6, ang=-65, extra=(), run_time=0.5):
    """a red slash with a spark at c; the slash then fades. `extra` animations run alongside."""
    sl = slash(c, L, ang)
    scene.play(Create(sl), Flash(np.array(c, float), color=TEXT, line_length=0.3, flash_radius=0.4, num_lines=10),
               *extra, run_time=run_time)
    scene.play(FadeOut(sl), run_time=0.2)


# ---- the membrane and the Bcl-2 family strip ---------------------------------------------------
def mem_segs(y, h, pore, x0=-6.3, x1=6.3):
    """the outer mitochondrial membrane as [left, middle (the pore), right]."""
    def mk(xa, xb):
        return RoundedRectangle(corner_radius=0.06, width=xb - xa, height=h, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.4).move_to([(xa + xb) / 2, y, 0])
    return VGroup(mk(x0, -pore), mk(-pore, pore), mk(pore, x1))


G4 = dict(my=-1.83, mh=0.46, eh=2.1, gh=3.0, ew=1.7, gw=2.4, ex=1.35, gx=4.4, pore=0.5, sz=28, slot_w=1.6, slot_h=0.5, inset=0.25)
G5 = dict(my=-2.62, mh=0.34, eh=0.95, gh=1.5, ew=1.5, gw=2.0, ex=1.15, gx=3.6, pore=0.4, sz=22, slot_w=1.3, slot_h=0.3, inset=0.14)


def guard(name, x, g):
    w, h = g["gw"], g["gh"]
    cy = g["mt"] + h / 2
    b = blob(name, GREEN, w, h, g["sz"], pos=[x, cy, 0])
    b[2].move_to([x, cy - h * 0.22, 0])
    sy = cy + h / 2 - g["slot_h"] / 2 - g["inset"]
    slot = DashedVMobject(rr(g["slot_w"], g["slot_h"], 0.12), num_dashes=24).set_stroke(TEXT, 2.5).move_to([x, sy, 0])
    out = VGroup(b[0], b[1], b[2], slot)
    out.body, out.lbl, out.slot = b[1], b[2], slot
    return out


def hold_bar(side, g):
    """the hold: it runs out of the guard's groove, over to its effector and down onto it ([across, down, cap])."""
    sy = g["mt"] + g["gh"] - g["slot_h"] / 2 - g["inset"]        # height of the groove
    x0 = side * (g["gx"] - g["slot_w"] / 2)                      # the end of the groove that faces the effector
    xe, yt = side * g["ex"], g["mt"] + g["eh"]                   # centre of the effector, top of the effector
    return VGroup(Line([x0, sy, 0], [xe, sy, 0], color=GREEN, stroke_width=7),
                  Line([xe, sy, 0], [xe, yt + 0.03, 0], color=GREEN, stroke_width=7),
                  Line([xe - 0.3, yt + 0.03, 0], [xe + 0.3, yt + 0.03, 0], color=GREEN, stroke_width=9))


def make_strip(g):
    """the membrane with the two effectors and the two guards that hold them (everything in check)."""
    g = {**g, "mt": g["my"] + g["mh"] / 2}
    mem = mem_segs(g["my"], g["mh"], g["pore"])
    bax = blob("BAX", PURPLE, g["ew"], g["eh"], g["sz"], pos=[-g["ex"], g["mt"] + g["eh"] / 2, 0])
    bak = blob("BAK", PURPLE, g["ew"], g["eh"], g["sz"], pos=[g["ex"], g["mt"] + g["eh"] / 2, 0])
    g1, g2 = guard("BCL-2", -g["gx"], g), guard("BCL-xL", g["gx"], g)
    b1, b2 = hold_bar(-1, g), hold_bar(1, g)
    return NS(g=g, mem=mem, bax=bax, bak=bak, g1=g1, g2=g2, b1=b1, b2=b2,
              all=VGroup(mem, bax, bak, g1, g2, b1, b2))


def eff_on(e):
    return [e.body.animate.set_fill(PURPLE, 0.85), e.lbl.animate.set_color(TEXT)]


def eff_off(e):
    return [e.body.animate.set_fill(PURPLE, 0.3), e.lbl.animate.set_color(PURPLE)]


def sensor(name, x, y_chip, dy=0.82):
    """a sensor: its name chip with its short helix hanging from it (a labelled capsule)."""
    ch = bchip(name, YELLOW, 26).move_to([x, y_chip, 0])
    cap = RoundedRectangle(corner_radius=0.2, width=1.3, height=0.4, stroke_color=YELLOW, stroke_width=3,
                           fill_color=YELLOW, fill_opacity=0.85).move_to([x, y_chip - dy, 0])
    lbl = T("helix", 22, BG, weight=BOLD).move_to(cap)
    link = Line(ch.get_bottom(), cap.get_top(), color=YELLOW, stroke_width=4)
    s = VGroup(link, cap, lbl, ch)
    s.cap, s.lbl, s.ch = cap, lbl, ch
    return s


def ushape(x0, x1, ytop, ybot, bevel=0.22, color=GREY, w=3):
    """an open-topped outline (left side, bottom, right side): the mitochondrion below its outer membrane."""
    pts = [[x0, ytop, 0], [x0, ybot + bevel, 0], [x0 + bevel, ybot, 0], [x1 - bevel, ybot, 0], [x1, ybot + bevel, 0], [x1, ytop, 0]]
    return VMobject().set_points_as_corners(pts).set_stroke(color, w, opacity=0.8).set_fill(opacity=0)


def disc(pos, r=0.26):
    return Circle(radius=r, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE, fill_opacity=0.85).move_to(pos)


def reframe(old, new):
    return [Transform(a, b) for a, b in zip(old, new)]


class Film(SpokenScene):
    def outro(self, *anims, then=None, after=None, run_time=0.38):
        """hold until the narration ends, clear what the next scene does not inherit, then (optionally)
        change framing (`then`, and `after` once that has settled)."""
        rest = self.narration_s - 0.02 - self.elapsed()
        if rest > 0:
            self.wait(rest)
        if anims:
            self.play(*anims, run_time=run_time)
        if then:
            self.play(*then, run_time=0.9)
        if after:
            self.play(*after, run_time=0.45)
        if then or after:
            self.wait(0.15)
        self.finish()


class S00Title(TitleCard):
    LESSON = "Death Receptors, BCL-2 and Caspases"
    TITLE = "The safeguard comes before the cut"


# ---------------------------------------------------------------------------------------------
class S01Puzzle(Film):
    """ready within hours, never by mistake; a caspase cuts and nothing undoes a cut: where is the safeguard?"""

    def construct(self):
        ck = clock([-5.2, 2.4, 0], r=0.62)
        hrs = T("ready within hours", 34, TEXT).next_to(ck, RIGHT, buff=0.4)
        self.at("How can")
        self.play(FadeIn(ck), FadeIn(hrs, shift=RIGHT * 0.12), run_time=0.5)
        self.at("within hours")
        self.play(Rotate(ck.hand, -TAU * 0.8, about_point=ck.c), run_time=1.0)
        mis = ghost_chip("by mistake", 34).move_to([3.6, 2.4, 0])
        self.at("still never")
        self.play(FadeIn(mis, shift=LEFT * 0.12), run_time=0.4)
        self.at("by mistake")
        self.play(Create(strike(mis)), run_time=0.4)

        # the killer
        cas = casp("killer", 3.4, 1.9, 40, active=True, pos=[-3.7, -0.9, 0])
        self.at("The killer")
        self.play(GrowFromCenter(cas), run_time=0.6)
        self.at("called a")
        name = T("caspase", 40, TEXT).move_to(cas.lbl)
        self.play(FadeOut(cas.lbl), FadeIn(name), run_time=0.4)

        # it cuts other proteins
        pL = rr(2.5, 1.5).set_stroke(GREY, 3.5).set_fill(GREY, 0.25).move_to([2.25, -0.9, 0])
        pR = rr(2.5, 1.5).set_stroke(GREY, 3.5).set_fill(GREY, 0.25).move_to([4.75, -0.9, 0])
        plab = T("protein", 32, GREY).move_to([3.5, -2.15, 0])
        a1 = arr([-1.95, -0.9, 0], [0.7, -0.9, 0], GREY, w=6)
        self.at("It cuts")
        self.play(FadeIn(VGroup(pL, pR), shift=LEFT * 0.2), FadeIn(plab), GrowArrow(a1), run_time=0.6)
        self.at("other proteins")
        cut_play(self, [3.5, -0.9, 0], L=2.2, ang=-72,
                 extra=(pL.animate.shift(LEFT * 0.35), pR.animate.shift(RIGHT * 0.35)), run_time=0.55)

        # nothing undoes it
        ua = arr([1.2, 0.4, 0], [2.7, 0.4, 0], GREY, w=7)
        ub = arr([5.8, 0.4, 0], [4.3, 0.4, 0], GREY, w=7)
        self.at("Nothing undoes")
        self.play(GrowArrow(ua), GrowArrow(ub), run_time=0.6)
        self.at("a cut")
        no = strike(VGroup(ua, ub), TEXT, 8)
        self.play(Create(no), run_time=0.4)

        # the puzzle: where does the safeguard sit?
        gate_back = rr(1.3, 1.7).set_stroke(width=0).set_fill(BG, 1).move_to([-0.6, -0.9, 0])
        gate_edge = DashedVMobject(rr(1.3, 1.7), num_dashes=30).set_color(TEXT).move_to([-0.6, -0.9, 0])
        q = T("?", 60, TEXT, weight=BOLD).move_to([-0.6, -0.9, 0])
        gate = VGroup(gate_back, gate_edge, q)
        self.at("where can the")
        self.play(FadeIn(gate, scale=0.8), run_time=0.5)
        sg = T("safeguard", 32, TEXT).move_to([-0.6, -2.2, 0])
        self.at("its safeguard")
        self.play(FadeIn(sg, shift=UP * 0.1), pop(q, 1.5), run_time=0.6)
        self.outro(FadeOut(VGroup(ck, hrs, mis, cas, name, pL, pR, plab, a1, ua, ub, no, gate, sg)))


# ---------------------------------------------------------------------------------------------
class S02Gather(Film):
    """a caspase is stored as a precursor; step one is a gathering on a platform, every step after is a cut."""

    def construct(self):
        CW, CH = 1.8, 1.0
        loose = [(-5.0, 1.7), (-2.4, 2.7), (-0.3, 1.4), (2.0, 2.6)]
        chains = [casp("caspase", CW, CH, 22, pos=[x, y, 0]) for x, y in loose]
        self.at("Every")
        self.play(LaggedStart(*[FadeIn(c, scale=0.7) for c in chains], lag_ratio=0.2), run_time=1.0)
        pre = T("inactive precursor", 28, GREY).move_to([-2.6, 0.35, 0])
        self.at("inactive precursor")
        self.play(FadeIn(pre, shift=UP * 0.1), *[pop(c, 1.12) for c in chains], run_time=0.8)
        self.at("such as")
        self.play(*[Transform(c.lbl, T("caspase-9", 22, TEXT).move_to(c.lbl)) for c in chains], run_time=0.5)
        one = T("a single chain", 28, GREY).move_to([-2.6, 0.35, 0])
        self.at("single inactive chain")
        self.play(FadeOut(pre), FadeIn(one), Indicate(chains[1], color=RED, scale_factor=1.2), run_time=0.8)

        # the platform
        plat = rr(8.8, 0.36, 0.1).set_stroke(TEAL, 3).set_fill(TEAL, 0.55).move_to([-1.9, -2.15, 0])
        plab = T("platform", 30, TEAL).move_to([-1.9, -2.8, 0])
        self.at("a platform")
        self.play(GrowFromCenter(plat), FadeIn(plab, shift=UP * 0.1), run_time=0.6)
        slots = [-5.4, -3.1, -0.8, 1.5]
        yv = -1.97 + CH / 2
        self.at("gathers several copies")
        self.play(FadeOut(one), LaggedStart(*[c.animate.move_to([x, yv, 0]) for c, x in zip(chains, slots)], lag_ratio=0.15),
                  run_time=1.5)
        self.at("pair up")
        self.play(chains[1].animate.shift(LEFT * 0.5), chains[3].animate.shift(LEFT * 0.5), run_time=0.5)
        self.play(*[a for c in chains for a in casp_on(c)], run_time=0.6)

        # the active pair cuts an executioner (a pair that is already paired, but inactive)
        exL, exR = casp("", 1.7, CH, pos=[3.55, 1.2, 0]), casp("", 1.7, CH, pos=[5.25, 1.2, 0])
        ex = VGroup(exL, exR)
        exlab = T("executioner", 30, TEXT).move_to([4.4, 2.2, 0])
        a1 = arr([1.5, -0.95, 0], [3.45, 0.6, 0], RED, w=6)
        self.at("Then it cuts")
        self.play(GrowArrow(a1), run_time=0.45)
        self.at("an executioner")
        self.play(FadeIn(ex, shift=LEFT * 0.2), FadeIn(exlab), run_time=0.5)
        inact = T("inactive", 26, GREY).move_to([4.7, 0.25, 0])
        self.at("already paired")
        self.play(Indicate(exL, color=RED, scale_factor=1.12), Indicate(exR, color=RED, scale_factor=1.12), run_time=0.7)
        self.at("but inactive")
        self.play(FadeIn(inact, shift=UP * 0.1), run_time=0.4)

        # one gathering, then cuts all the way
        step1 = T("first step: a gathering", 30, TEAL).move_to([-1.9, -2.8, 0])
        self.at("first step")
        self.play(FadeOut(plab), FadeIn(step1), *glow(plat, s=1.04, color=TEAL), run_time=0.7)
        c1 = T("cut", 32, RED, weight=BOLD).move_to([1.5, 0.15, 0])
        self.at("every step after")
        cut_play(self, [4.4, 1.2, 0], L=2.0, ang=-70, extra=[FadeOut(inact), *[a for p in ex for a in casp_on(p)]], run_time=0.5)
        self.play(FadeIn(c1, shift=UP * 0.1), run_time=0.3)
        pa = rr(1.7, 0.9).set_stroke(GREY, 3.5).set_fill(GREY, 0.25).move_to([3.55, -1.15, 0])
        pb = rr(1.7, 0.9).set_stroke(GREY, 3.5).set_fill(GREY, 0.25).move_to([5.25, -1.15, 0])
        plab2 = T("protein", 26, GREY).move_to([4.4, -1.95, 0])
        a2 = arr([4.4, 0.65, 0], [4.4, -0.6, 0], RED, w=6)
        self.at("is a cut")
        self.play(GrowArrow(a2), FadeIn(VGroup(pa, pb)), FadeIn(plab2), run_time=0.45)
        c2 = T("cut", 32, RED, weight=BOLD).move_to([5.25, 0.05, 0])
        cut_play(self, [4.4, -1.15, 0], L=1.7, ang=-70,
                 extra=[pa.animate.shift(LEFT * 0.3), pb.animate.shift(RIGHT * 0.3), FadeIn(c2)], run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
# the stage of scene 3: cytosol on top, the mitochondrion below, a wheel hub in the middle
W3 = np.array([0.0, 0.8, 0.0])
R3 = 2.0
MEM3 = dict(y=-2.0, h=0.4, pore=0.7)


def spoke(k, r=R3):
    a = PI / 2 + k * TAU / 7
    return W3 + r * np.array([np.cos(a), np.sin(a), 0])


class S03Parts(Film):
    """the platform's two parts are kept apart; open the membrane and they meet and gather caspase-9."""

    def construct(self):
        # Apaf-1 sits scattered in the cytosol
        scatter = [(-5.6, 2.4), (-3.8, 1.2), (-5.4, -0.1), (-3.9, 2.95), (3.8, 2.8), (5.4, 1.5), (3.9, 0.1)]
        apafs = [blob("", TEAL, 0.8, 0.8, pos=[x, y, 0]) for x, y in scatter]
        self.at("One part")
        self.play(LaggedStart(*[FadeIn(a, scale=0.6) for a in apafs], lag_ratio=0.12), run_time=0.9)
        self.at("the platform")
        self.play(*[pop(a, 1.2) for a in apafs], run_time=0.6)
        aplab = T("APAF-1", 32, TEAL).move_to([5.2, 0.1, 0])
        ptr = Line([4.55, 0.1, 0], [4.32, 0.1, 0], color=TEAL, stroke_width=3)
        self.at("sits in")
        self.play(FadeIn(aplab, shift=LEFT * 0.1), Create(ptr), run_time=0.5)
        cyt = T("cytosol", 28, GREY).move_to([-5.4, 3.25, 0])
        self.at("the cytosol")
        self.play(FadeIn(cyt), run_time=0.4)

        # cytochrome c is behind the outer membrane
        mem = mem_segs(MEM3["y"], MEM3["h"], MEM3["pore"])
        mito = ushape(-6.3, 6.3, -2.2, -3.5)
        mitolab = T("mitochondrion", 26, GREY).move_to([-4.5, -3.2, 0])
        xs = [-3.6, -2.4, -1.2, 0.0, 1.2, 2.4, 3.6]
        discs = [disc([x, -2.65, 0], 0.28) for x in xs]
        dlab = T("cytochrome c", 26, ORANGE).move_to([1.4, -3.2, 0])
        self.at("The other part")
        self.play(FadeIn(mito), FadeIn(mem), run_time=0.6)
        self.at("cytochrome")
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in discs], lag_ratio=0.1), FadeIn(dlab), run_time=0.8)
        omlab = T("outer membrane", 26, GREY).move_to([-4.5, -1.5, 0])
        self.at("outer membrane")
        self.play(FadeIn(omlab), Indicate(mem, color=TEXT, scale_factor=1.0), run_time=0.6)
        self.at("mitochondrion")
        self.play(FadeIn(mitolab), run_time=0.4)
        ring = DashedVMobject(Circle(radius=R3 + 0.45).move_to(W3), num_dashes=44).set_color(GREY)
        hubg = DashedVMobject(Circle(radius=0.8).move_to(W3), num_dashes=18).set_color(GREY)
        nop = T("no platform", 28, GREY).move_to(W3 + [0, 1.55, 0])
        ghost = VGroup(ring, hubg, nop)
        self.at("no platform")
        self.play(FadeIn(ghost), run_time=0.5)
        x_out = strike(ring, TEXT, 7)
        self.play(Create(x_out), run_time=0.4)

        # open the membrane: cytochrome c escapes
        self.at("membrane opens")
        self.play(FadeOut(ghost), FadeOut(x_out), FadeOut(mem[1], scale=0.3), FadeOut(omlab), run_time=0.5)
        rise = []
        for i, d in enumerate(discs):
            tx = -3.3 + i * 1.1
            path = VMobject().set_points_as_corners([d.get_center(), np.array([0, -2.45, 0]), np.array([0, -1.5, 0]), np.array([tx, -1.3, 0])])
            rise.append(MoveAlongPath(d, path))
        self.at("escapes")
        self.play(LaggedStart(*rise, lag_ratio=0.1), FadeOut(dlab), run_time=1.5)

        # cytochrome c and dATP make seven Apaf-1 assemble into a wheel
        datp = bchip("dATP", TEXT, 28).move_to([-4.1, -0.45, 0])
        self.at("nucleotide")
        self.play(FadeIn(datp, shift=RIGHT * 0.2), FadeOut(aplab), FadeOut(ptr), FadeOut(cyt), run_time=0.5)
        spokes = [spoke(k) for k in range(7)]
        inner = [spoke(k, R3 - 0.55) for k in range(7)]
        hub = Circle(radius=0.8, stroke_color=TEAL, stroke_width=3.5, fill_color=TEAL, fill_opacity=0.18).move_to(W3)
        self.at("seven copies")
        self.play(datp.animate.move_to(W3).scale(0.8), run_time=0.6)
        self.play(FadeOut(datp, scale=0.3), FadeIn(hub, scale=0.5), run_time=0.3)
        self.at("assemble into")
        self.play(*[a.animate.move_to(p) for a, p in zip(apafs, spokes)],
                  *[d.animate.move_to(p) for d, p in zip(discs, inner)], run_time=1.3)

        # the wheel gathers caspase-9
        wl = T("apoptosome", 32, TEXT).move_to([4.6, 1.75, 0])
        wl2 = T("seven APAF-1", 28, TEAL).move_to([4.6, 1.15, 0])
        self.at("This wheel")
        self.play(*glow(hub, s=1.1), *[pop(a, 1.12) for a in apafs], FadeIn(wl, shift=LEFT * 0.1), FadeIn(wl2, shift=LEFT * 0.1), run_time=0.6)
        caps = [casp("caspase-9", 1.8, 1.0, 22, pos=[-5.3, y, 0]) for y in (2.85, 1.7, 0.55, -0.6)]
        self.at("gathers")
        self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in caps], lag_ratio=0.15), run_time=0.8)
        minis = [(-0.25, 0.25), (0.25, 0.25), (-0.25, -0.25), (0.25, -0.25)]
        self.play(*[FadeOut(c.lbl) for c in caps], run_time=0.2)
        self.play(*[Transform(c, casp("", 0.42, 0.42, pos=W3 + [mx, my, 0])) for c, (mx, my) in zip(caps, minis)], run_time=0.9)
        gl = T("caspase-9", 30, RED).move_to([-4.6, 1.1, 0])
        gp = Line([-3.55, 1.1, 0], [-0.85, 1.1, 0], color=RED, stroke_width=3)
        self.play(FadeIn(gl), Create(gp), run_time=0.5)
        s4 = make_strip(G4)
        self.outro(FadeOut(VGroup(*apafs, *discs, hub, *caps, gl, gp, wl, wl2, mito, mitolab)),
                   then=[Transform(mem[0], s4.mem[0]), Transform(mem[2], s4.mem[2]), FadeIn(s4.mem[1])])


# ---------------------------------------------------------------------------------------------
class S04Family(Film):
    """the Bcl-2 family at the outer membrane: effectors open it, guards hold the effectors, sensors fill a guard's groove."""

    def construct(self):
        s = make_strip(G4)
        self.add(s.mem)
        lab = T("outer membrane", 26, GREY).move_to([-3.4, -2.55, 0])
        for e in (s.bax, s.bak):
            e.body.set_fill(PURPLE, 0.3)
        self.at("At that")
        self.play(LaggedStart(FadeIn(s.g1, shift=DOWN * 0.2), FadeIn(s.bax, shift=DOWN * 0.2), FadeIn(s.bak, shift=DOWN * 0.2),
                              FadeIn(s.g2, shift=DOWN * 0.2), lag_ratio=0.2), FadeIn(lab), run_time=1.0)
        self.at("named for")
        self.play(*glow(s.g1.body, s.g1.lbl, s.g2.body, s.g2.lbl, s=1.05), run_time=0.6)
        self.at("decides")
        self.play(*[pop(m, 1.05) for m in (s.g1, s.bax, s.bak, s.g2)], run_time=0.6)

        # a colour key for the three classes, filled in as each is named
        ky = 3.15
        dots = [Circle(radius=0.14, stroke_width=0, fill_color=c, fill_opacity=1).move_to([x, ky, 0])
                for c, x in zip((PURPLE, GREEN, YELLOW), (-3.0, -0.3, 1.7))]
        self.at("three classes")
        self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in dots], lag_ratio=0.25), run_time=0.7)

        # effectors open the membrane once activated
        t1 = T("effectors", 26, PURPLE).next_to(dots[0], RIGHT, buff=0.18)
        self.at("the effectors")
        self.play(FadeIn(t1, shift=RIGHT * 0.1), *glow(s.bax.body, s.bak.body, s=1.06), run_time=0.6)
        # a ghost of what an activated effector would do: the membrane itself never opens here
        ghost = DashedVMobject(rr(2 * G4["pore"] + 0.14, G4["mh"] + 0.2, 0.06), num_dashes=24).set_color(TEXT).move_to([0, G4["my"], 0])
        gtag = T("if activated", 24, TEXT).move_to([0.9, -2.55, 0])
        self.at("open the outer")
        self.play(FadeIn(ghost), FadeIn(gtag, shift=UP * 0.1), *glow(s.bax.body, s.bak.body, s.bax.lbl, s.bak.lbl, s=1.06), run_time=0.6)
        # guards hold them in check
        t2 = T("guards", 26, GREEN).next_to(dots[1], RIGHT, buff=0.18)
        self.at("its relatives")
        self.play(*glow(s.g1.body, s.g1.lbl, s.g2.body, s.g2.lbl, s=1.05), run_time=0.6)
        self.at("the guards")
        self.play(FadeIn(t2, shift=RIGHT * 0.1), run_time=0.4)
        self.at("hold them")
        self.play(FadeOut(ghost), FadeOut(gtag),
                  LaggedStart(*[Create(m) for m in (*s.b1[:2], s.b1[2], *s.b2[:2], s.b2[2])], lag_ratio=0.25), run_time=1.0)

        # sensors carry one short helix that fits a guard's groove
        sa = sensor("BAD", -4.4, 2.8)
        sb = sensor("BID", 4.4, 2.8)
        t3 = T("sensors", 26, YELLOW).next_to(dots[2], RIGHT, buff=0.18)
        self.at("The sensors")
        self.play(FadeIn(sa, shift=DOWN * 0.4), FadeIn(sb, shift=DOWN * 0.4), FadeIn(t3, shift=RIGHT * 0.1), run_time=0.7)
        self.at("one short")
        self.play(pop(sa.cap, 1.25), pop(sa.lbl, 1.25), pop(sb.cap, 1.25), pop(sb.lbl, 1.25), run_time=0.7)
        self.at("It fits into")
        self.play(*glow(s.g1.slot, s=1.15), run_time=0.5)
        tgt = s.g1.slot.get_center()
        dy = tgt[1] - sa.cap.get_center()[1]
        self.at("a groove")
        self.play(sa.animate.shift(DOWN * (-dy)), run_time=0.9)
        self.at("occupies it")
        self.play(*glow(s.g1.body, sa.cap, s=1.05, color=YELLOW), FadeOut(s.b1), run_time=0.7)
        n = make_strip(G5)
        self.outro(FadeOut(sa), FadeOut(sb), FadeOut(VGroup(lab, t1, t2, t3, *dots)), FadeIn(s.b1),
                   then=reframe([s.mem[0], s.mem[1], s.mem[2], s.bax, s.bak, s.g1, s.g2, s.b1, s.b2],
                                [n.mem[0], n.mem[1], n.mem[2], n.bax, n.bak, n.g1, n.g2, n.b1, n.b2]))


# ---------------------------------------------------------------------------------------------
SAW_P = np.array([0.0, 1.45, 0.0])


class S05Balance(Film):
    """sensors must outnumber guards; then the grooves fill, the effectors are free and cytochrome c leaves."""

    def construct(self):
        s = make_strip(G5)
        self.add(s.all)
        xs = [-3.6, -2.4, -1.2, 0.0, 1.2, 2.4, 3.6]
        discs = [disc([x, -3.12, 0], 0.2) for x in xs]
        dlab = T("cytochrome c", 24, ORANGE).move_to([5.05, -3.12, 0])
        self.add(*discs, dlab)

        # the seesaw: guards on the left, sensors (not yet switched on) on the right
        beam = Line(SAW_P + [-3.5, 0, 0], SAW_P + [3.5, 0, 0], color=GREY, stroke_width=9)
        gb = [rr(0.8, 0.55, 0.14).set_stroke(GREEN, 3.5).set_fill(GREEN, 0.4).move_to(SAW_P + [x, 0.32, 0]) for x in (-2.0, -1.0)]
        sl = [DashedVMobject(rr(0.8, 0.55, 0.14), num_dashes=16).set_color(GREY).move_to(SAW_P + [x, 0.32, 0]) for x in (1.0, 2.0, 3.0)]
        pl = [rr(0.8, 0.55, 0.14).set_stroke(YELLOW, 3.5, opacity=0).set_fill(YELLOW, 0).move_to(SAW_P + [x, 0.32, 0]) for x in (1.0, 2.0, 3.0)]
        saw_items = VGroup(beam, *gb, *sl, *pl)
        self.add(*pl)
        fulcrum = Polygon([-0.5, 0.55, 0], [0.5, 0.55, 0], [0, 1.4, 0], stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.35)
        tilt = 9 * DEGREES
        saw_items.rotate(tilt, about_point=SAW_P)
        glab = T("guards", 28, GREEN).move_to([-2.4, 0.2, 0])
        slab = T("sensors", 28, YELLOW).move_to([2.4, 0.2, 0])

        self.at("In a healthy")
        self.play(FadeIn(fulcrum), Create(beam), run_time=0.6)
        self.at("guards and")
        self.play(*[FadeIn(b, scale=0.6) for b in gb], FadeIn(glab), run_time=0.6)
        eflab = T("effectors", 24, PURPLE).move_to([0, -1.05, 0])
        self.at("effectors")
        self.play(FadeIn(eflab), *glow(s.bax.body, s.bak.body, s=1.06), run_time=0.6)

        # their proportion sets how hard to push
        push = arr([4.0, 3.3, 0], [4.0, 2.4, 0], YELLOW, w=7, tip=0.26)
        pushlab = T("push", 28, YELLOW).move_to([5.0, 2.95, 0])
        self.at("proportion")
        self.play(FadeOut(eflab), *[FadeIn(x) for x in sl], FadeIn(slab), run_time=0.5)
        self.at("how hard")
        self.play(GrowArrow(push), FadeIn(pushlab, shift=LEFT * 0.1), run_time=0.5)

        # a stress switches on sensors one at a time; when they outnumber the guards the beam tips
        stlab = T("stress", 28, YELLOW).move_to([5.0, 2.95, 0])
        self.at("A stress")
        self.play(Transform(pushlab, stlab), run_time=0.4)

        def on(i):
            return [pl[i].animate.set_fill(YELLOW, 0.85).set_stroke(opacity=1.0), sl[i].animate.set_stroke(opacity=0.0)]

        def lean(deg):
            return Rotate(saw_items, angle=deg * DEGREES, about_point=SAW_P)

        self.at("switch on")
        self.play(*on(0), run_time=0.25)
        self.play(lean(-4), run_time=0.45)
        self.at("sensors")
        self.play(*on(1), run_time=0.25)
        self.play(lean(-5), run_time=0.45)
        self.at("outnumber")
        self.play(*on(2), run_time=0.25)
        self.play(lean(-7), run_time=0.55)
        self.play(*glow(*pl, s=1.1, color=YELLOW), run_time=0.5)

        # the grooves fill, the hold bars let go, the pore opens
        c1 = s.g2.slot.get_center()
        c2 = s.g1.slot.get_center()
        cap = lambda: RoundedRectangle(corner_radius=0.15, width=1.0, height=0.26, stroke_color=YELLOW, stroke_width=3,
                                       fill_color=YELLOW, fill_opacity=0.85)
        def fly(p, end, via):
            path = VMobject().set_points_smoothly([p.get_center(), *via, end])
            return MoveAlongPath(p, path)

        self.at("guards are")
        # a sensor that leaves the beam stops being weighed on it: the beam always matches what is on it
        saw_items.remove(pl[0])
        self.play(FadeOut(glab), FadeOut(slab), fly(pl[0], c1, [np.array([2.6, 0.0, 0])]), lean(7), run_time=0.8)
        self.play(Transform(pl[0], cap().move_to(c1)), run_time=0.25)
        saw_items.remove(pl[1])
        self.play(fly(pl[1], c2, [np.array([1.4, -0.1, 0]), np.array([-1.6, -0.4, 0])]), lean(5), run_time=0.9)
        self.play(Transform(pl[1], cap().move_to(c2)), run_time=0.25)
        self.at("are free")
        self.play(FadeOut(s.b1, shift=DOWN * 0.15), FadeOut(s.b2, shift=DOWN * 0.15), *eff_on(s.bax), *eff_on(s.bak), run_time=0.5)
        self.at("membrane opens")
        self.play(FadeOut(s.mem[1], scale=0.3), run_time=0.4)

        # cytochrome c escapes
        rise = []
        for i, d in enumerate(discs):
            tx = -3.6 + i * 1.2
            path = VMobject().set_points_as_corners([d.get_center(), np.array([0, -2.62, 0]), np.array([0, -0.9, 0]), np.array([tx, -0.6, 0])])
            rise.append(MoveAlongPath(d, path))
        self.at("escapes")
        self.play(LaggedStart(*rise, lag_ratio=0.1), FadeOut(dlab), run_time=1.5)
        self.outro()


# ---------------------------------------------------------------------------------------------
# scene 6: five small pictures, read left to right and then right to left, lit one by one
POS = [(-4.2, 1.65), (0.0, 1.65), (4.2, 1.65), (4.2, -1.65), (0.0, -1.65)]
IK = 1.5             # icon scale


def seg(x):
    return rr(0.56, 0.2, 0.05).set_stroke(GREY, 3).set_fill(GREY, 0.4).move_to([x, -0.45, 0])


def icon_saw():
    """a tipped seesaw: two guards on the left, three sensors on the right."""
    beam = Line([-0.78, 0, 0], [0.78, 0, 0], color=GREY, stroke_width=6)
    g = [rr(0.25, 0.22, 0.06).set_stroke(GREEN, 2.5).set_fill(GREEN, 0.4).move_to([x, 0.15, 0]) for x in (-0.56, -0.28)]
    y = [rr(0.25, 0.22, 0.06).set_stroke(YELLOW, 2.5).set_fill(YELLOW, 0.85).move_to([x, 0.15, 0]) for x in (0.12, 0.4, 0.68)]
    items = VGroup(beam, *g, *y)
    items.rotate(-9 * DEGREES, about_point=np.array([0, 0, 0.0]))
    fulc = Polygon([-0.25, -0.45, 0], [0.25, -0.45, 0], [0, -0.04, 0], stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.35)
    return VGroup(fulc, items)


def icon_pore():
    bx = rr(0.42, 0.5, 0.1).set_stroke(PURPLE, 3).set_fill(PURPLE, 0.85).move_to([-0.43, -0.1, 0])
    bk = rr(0.42, 0.5, 0.1).set_stroke(PURPLE, 3).set_fill(PURPLE, 0.85).move_to([0.43, -0.1, 0])
    return VGroup(seg(-0.5), seg(0.5), bx, bk)


def icon_cytc():
    ds = [disc([x, y, 0], 0.12) for x, y in ((0, -0.45), (-0.3, -0.1), (0.3, -0.1), (-0.5, 0.25), (0, 0.2), (0.5, 0.25), (0, 0.6))]
    return VGroup(seg(-0.5), seg(0.5), *ds)


def icon_wheel():
    ring = [Circle(radius=0.11, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.6).move_to(
        0.62 * np.array([np.cos(PI / 2 + k * TAU / 7), np.sin(PI / 2 + k * TAU / 7), 0])) for k in range(7)]
    hub = Circle(radius=0.3, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.18)
    ms = [rr(0.18, 0.18, 0.04).set_stroke(RED, 2.5).set_fill(RED, 0.5).move_to([dx, dy, 0]) for dx, dy in ((-0.1, 0.1), (0.1, 0.1), (-0.1, -0.1), (0.1, -0.1))]
    return VGroup(hub, *ring, *ms)


def icon_cut():
    a = rr(0.7, 0.42, 0.1).set_stroke(GREY, 3).set_fill(GREY, 0.3).move_to([-0.42, 0, 0])
    b = rr(0.7, 0.42, 0.1).set_stroke(GREY, 3).set_fill(GREY, 0.3).move_to([0.42, 0, 0])
    sl = Line([0.0, 0.55, 0], [0.0, -0.55, 0], color=RED, stroke_width=7)
    return VGroup(a, b, sl)


class S06Rule(Film):
    """the whole chain in order; the decision is the first link and nothing undoes the last."""

    def construct(self):
        makers = [icon_saw, icon_pore, icon_cytc, icon_wheel, icon_cut]
        icons = [m().scale(IK).move_to([x, y, 0]) for m, (x, y) in zip(makers, POS)]
        words = ["balance tips", "membrane opens", "cytochrome c escapes", "wheel gathers caspase-9", "cuts begin"]
        caps = [T(w, 28, TEXT).move_to([x, y - 1.3 - (0.2 if i == 3 else 0.0), 0]) for i, (w, (x, y)) in enumerate(zip(words, POS))]
        arrows = [arr([-2.75, 1.65, 0], [-1.4, 1.65, 0], GREY, w=6, tip=0.2),
                  arr([1.4, 1.65, 0], [2.75, 1.65, 0], GREY, w=6, tip=0.2),
                  arr([4.2, 0.1, 0], [4.2, -0.5, 0], GREY, w=6, tip=0.2),
                  arr([3.0, -1.65, 0], [1.4, -1.65, 0], GREY, w=6, tip=0.2)]
        self.add(*icons, *caps, *arrows)
        for m in (*icons, *caps, *arrows):
            m.save_state()
            m.set_opacity(0.25)

        def lit(i):
            anims = [Restore(icons[i]), Restore(caps[i])]
            if i > 0:
                anims.append(Restore(arrows[i - 1]))
            return anims

        self.at("whole chain")
        self.play(*[pop(x, 1.08) for x in icons], run_time=0.7)
        self.at("sensors outnumber")
        self.play(*lit(0), run_time=0.5)
        self.at("open the membrane")
        self.play(*lit(1), run_time=0.5)
        self.at("escapes")
        self.play(*lit(2), run_time=0.5)
        self.at("wheel assembles")
        self.play(*lit(3), run_time=0.5)
        self.at("the cuts begin")
        self.play(*lit(4), run_time=0.5)

        # the rule: the decision is the first link
        box = rr(2.7, 3.0, 0.2).set_stroke(TEXT, 3).move_to([-4.2, 1.1, 0])
        dec = T("decided here", 34, TEXT, weight=BOLD).move_to([-4.2, 3.05, 0])
        self.at("balance of")
        self.play(Create(box), FadeIn(dec, shift=DOWN * 0.1), run_time=0.7)
        self.at("before the first")
        self.play(pop(icons[0], 1.12), run_time=0.6)
        back = arr([-5.7, -1.2, 0], [-2.9, -1.2, 0], GREY, w=7, tip=0.26)
        nwb = T("no way back", 36, TEXT, weight=BOLD).move_to([-4.3, -2.3, 0])
        self.at("nothing undoes")
        self.play(GrowArrow(back), FadeIn(nwb, shift=UP * 0.1), run_time=0.6)
        self.play(Create(strike(back, TEXT, 8)), run_time=0.4)
        self.finish()


class S07End(EndCard):
    LINE = "The balance decides before the first cut, because nothing undoes a cut."
