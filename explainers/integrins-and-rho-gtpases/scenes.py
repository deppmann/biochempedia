"""Integrins: a grip the cell switches on from inside  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = a receptor: the integrin (alpha chain, legs, cup-shaped head; the beta chain is the
           same blue, a little lighter) and, in the last scene, the hormone receptor beside it
  YELLOW = the ligand the receptor grips (a knob hanging from the vessel wall)
  ORANGE = the signal on the vessel wall that starts the relay
  TEAL   = the message: the relay inside the cell, the pulse through the membrane, inside-out
  PURPLE = talin, the protein that throws the switch (and, in the last scene, "the cell decides")
  GREEN  = on: the open head, the tight grip, the cell stopped
  RED    = off / weak / ruled out (switched off, weak grip, the crossed-out boxes)
  GREY   = membranes, the vessel wall, the white blood cell, labels, parts not in the story

No molecular structures: the integrin is two thick bars (chains) that cross a membrane bar, bend
at a knee, and end in a cup (an open ring). The cup is the part that acts: closed and tipped back
it holds weakly, open and upright it holds tightly. Talin is a labelled chip, the ligand a knob
on a thread, the cell a circle.

One layout for the zoomed scenes (2 to 5):
  vessel wall across the top, the ligand hanging from it, the cell membrane across the lower
  middle, the integrin on it (x = X0), tails and talin below it, the relay on the left, a small
  readout (grip switch, cell status) on the right.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
BLUE2 = "#9BDCEB"      # the beta chain: the same blue, a little lighter, so the two chains can be told apart

# ---------------------------------------------------------------------------------------------
# layout
# ---------------------------------------------------------------------------------------------
WALL_Y = 3.2           # centre line of the vessel wall in the zoomed scenes
WALL_BOT = 3.05
YM = -1.55             # centre line of the cell membrane in the zoomed scenes
TM = 0.16              # half thickness of the membrane
X0 = 0.9               # x of the integrin in scenes 1 to 5
HOVER = np.array([X0, 2.64, 0.0])        # the ligand's knob, hanging just above the open head
ANCHOR = np.array([X0, WALL_BOT, 0.0])   # where its thread is fixed to the wall
KNOB_R = 0.24

# the integrin (scale 1)
K_H = 1.91             # knee height above the membrane centre line
L_UP = 0.9             # upper leg length
HEAD_OFF = 0.45        # head centre beyond the end of the upper legs
R_HEAD = 0.5           # radius of the cup
CH_OFF = 0.3           # each chain's distance from the middle
TAIL_L = 1.1           # tail length
CH_W, RING_W = 24, 16  # stroke widths of the chains and of the cup
BEND = 125.0           # degrees the upper legs fold at the knee
SPLAY = 24.0           # degrees each tail swings when talin binds
M_CLOSED, M_OPEN = 36.0, 140.0   # width of the cup's mouth, degrees

# right-hand readout
RX = 5.4


# ---------------------------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=26, pad=0.2, **kw):
    """chip with an opaque backing so lines drawn behind it do not show through."""
    c = chip(text, color, size=size, pad=pad, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def ghost_chip(text, size=24):
    """a dashed grey chip: something that is NOT part of the story."""
    t = T(text, size, GREY)
    box = RoundedRectangle(corner_radius=0.14, width=t.width + 0.4, height=t.height + 0.32)
    return VGroup(DashedVMobject(box, num_dashes=max(18, int(box.width * 9))).set_color(GREY), t)


def strike(m, color=RED):
    return Line(m.get_corner(DL) + [-0.08, -0.04, 0], m.get_corner(UR) + [0.08, 0.04, 0], color=color, stroke_width=7)


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def pop(m, s=1.2):
    """swell and settle, without recolouring (Indicate would hide the label on a chip)."""
    return m.animate(rate_func=there_and_back).scale(s)


def toggle(on=False, color=None, scale=1.0):
    c = color or (GREEN if on else RED)
    body = RoundedRectangle(corner_radius=0.5, width=2.0, height=1.0, stroke_color=c, stroke_width=5,
                            fill_color=c, fill_opacity=0.25)
    knob = Circle(radius=0.36, stroke_width=0, fill_color=TEXT, fill_opacity=1)
    knob.move_to(body.get_center() + RIGHT * (0.5 if on else -0.5))
    g = VGroup(body, knob)
    g.body, g.knob = body, knob
    g.scale(scale)
    return g


def flip(sw, on, color):
    off = sw.body.width * 0.25
    tgt = sw.body.get_center() + RIGHT * (off if on else -off)
    return [sw.knob.animate.move_to(tgt), sw.body.animate.set_stroke(color).set_fill(color, 0.25)]


def clock(center, r=0.55):
    center = np.array(center, float)
    face = Circle(radius=r, stroke_color=GREY, stroke_width=4).move_to(center)
    ticks = VGroup(*[Line(center + (r - 0.13) * v, center + r * v, color=GREY, stroke_width=4) for v in (UP, RIGHT, DOWN, LEFT)])
    hand = Line(center, center + UP * (r - 0.17), color=TEXT, stroke_width=5)
    pin = Dot(center, radius=0.06, color=TEXT)
    g = VGroup(face, ticks, hand, pin)
    g.hand, g.c = hand, center
    return g


def sweep(c, secs=1.0):
    """the clock hand makes one full turn."""
    return Rotate(c.hand, angle=-TAU, about_point=c.c, run_time=secs, rate_func=linear)


def membrane(y=YM, x0=-6.3, x1=6.3, h=2 * TM):
    return RoundedRectangle(corner_radius=0.08, width=x1 - x0, height=h, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.35).move_to([(x0 + x1) / 2, y, 0])


def wall_bar(y=WALL_Y, x0=-6.3, x1=6.3):
    return RoundedRectangle(corner_radius=0.08, width=x1 - x0, height=0.3, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.35).move_to([(x0 + x1) / 2, y, 0])


def knob_at(p, r=KNOB_R):
    return Circle(radius=r, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.9).move_to(p)


def thread(anchor, knob, r=KNOB_R):
    """the ligand's thread: a line from the wall to its knob, kept in step with the knob."""
    ln = Line(anchor, knob.get_center(), color=YELLOW, stroke_width=5)
    ln.add_updater(lambda m: m.put_start_and_end_on(anchor, knob.get_center() + UP * r))
    return ln


def ligand(anchor, p):
    k = knob_at(p)
    return VGroup(thread(anchor, k), k), k


# ---------------------------------------------------------------------------------------------
# the integrin: two chains, bent at a knee, ending in a cup. Everything is drawn from four numbers
# (position x, extension e, tail separation sep, mouth opening op) so a scene only moves the numbers.
# ---------------------------------------------------------------------------------------------
def _poly(pts, color, w):
    m = VMobject(joint_type=LineJointType.ROUND, cap_style=CapStyleType.ROUND)
    m.set_points_as_corners([np.array(p, float) for p in pts])
    m.set_stroke(color, w)
    m.set_fill(opacity=0)
    return m


class Ig:
    def __init__(self, x0=X0, e=1.0, sep=0.0, op=1.0, s=1.0, ym=YM, shown=1.0):
        self.s, self.ym = s, ym
        self.X, self.E, self.S, self.O = (ValueTracker(v) for v in (x0, e, sep, op))
        self.VA, self.VB, self.VH, self.GL, self.V = (ValueTracker(v) for v in (shown, shown, shown, 0.0, 1.0))
        self.mob = always_redraw(self._build)

    def labels(self):
        """alpha and beta, set beside the two tails (fixed: the tails swing only a little)."""
        s, x0, ym = self.s, self.X.get_value(), self.ym
        al = T("alpha", 26, BLUE).move_to([x0 - 1.5 * s, ym - 0.7 * s, 0])
        be = T("beta", 26, BLUE2).move_to([x0 + 1.45 * s, ym - 0.7 * s, 0])
        return al, be

    def geom(self):
        s, ym = self.s, self.ym
        x0, e, sep, op = (t.get_value() for t in (self.X, self.E, self.S, self.O))
        a = np.radians(90 - BEND * (1 - e))
        d = np.array([np.cos(a), np.sin(a), 0.0])
        pp = np.array([-np.sin(a), np.cos(a), 0.0])
        Km = np.array([x0, ym + K_H * s, 0.0])
        C = Km + d * (L_UP + HEAD_OFF) * s
        g = dict(C=C, d=d, a=a, K=Km, mouth=np.radians(M_CLOSED + (M_OPEN - M_CLOSED) * op))
        for k, o, sg in (("a", -CH_OFF, -1), ("b", CH_OFF, 1)):
            P0 = np.array([x0 + o * s, ym - TM, 0.0])
            M1 = np.array([x0 + o * s, ym + TM, 0.0])
            Ko = np.array([x0 + o * s, ym + K_H * s, 0.0])
            ang = np.radians(-90 + sg * SPLAY * sep)
            tu = np.array([np.cos(ang), np.sin(ang), 0.0])
            tip = P0 + TAIL_L * s * tu
            Eo = C - d * 0.45 * s - sg * pp * 0.2 * s
            g["pts_" + k] = [tip, P0, M1, Ko, Eo]
            g["K_" + k] = Ko
            g["tip_" + k] = tip
        return g

    def _build(self):
        g, s, V = self.geom(), self.s, self.V.get_value()
        out = []
        for k, tr, col in (("a", self.VA, BLUE), ("b", self.VB, BLUE2)):
            f = tr.get_value()
            m = _poly(g["pts_" + k], col, CH_W * s)
            if f < 0.999:
                m.pointwise_become_partial(_poly(g["pts_" + k], col, CH_W * s), 0, max(f, 0.001))
            m.set_stroke(col, CH_W * s, opacity=(1.0 if f > 0.002 else 0.0) * V)
            knee = Circle(radius=0.13 * s, stroke_color=col, stroke_width=4, fill_color=BG, fill_opacity=1).move_to(g["K_" + k])
            kv = (1.0 if f > 0.97 else 0.0) * V
            knee.set_stroke(opacity=kv).set_fill(opacity=kv)
            out += [m, knee]
        f = self.VH.get_value()
        mouth = g["mouth"]
        ring = Arc(radius=R_HEAD * s, start_angle=g["a"] + mouth / 2, angle=TAU - mouth, arc_center=g["C"],
                   stroke_color=BLUE, stroke_width=RING_W * s)
        if f < 0.999:
            part = Arc(radius=R_HEAD * s, start_angle=g["a"] + mouth / 2, angle=TAU - mouth, arc_center=g["C"])
            ring.pointwise_become_partial(part, 0, max(f, 0.001))
        ring.set_stroke(BLUE, RING_W * s, opacity=(1.0 if f > 0.002 else 0.0) * V)
        glow = Circle(radius=(R_HEAD + 0.24) * s, stroke_color=GREEN, stroke_width=7).move_to(g["C"])
        glow.set_stroke(GREEN, 7, opacity=self.GL.get_value() * V)
        out += [ring, glow]
        return VGroup(*out)


# ---------------------------------------------------------------------------------------------
# scene 1 objects (also rebuilt, in their final state, at the start of scene 2)
# ---------------------------------------------------------------------------------------------
S1_WALL_Y = 2.7
S1_R = 2.0
S1_CY = S1_WALL_Y - 0.15 - S1_R
CLOCK_C = np.array([-5.0, -2.45, 0.0])
GHOST_C = np.array([4.1, -2.1, 0.0])


def s1_cell(x):
    circ = Circle(radius=S1_R, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.12).move_to([x, S1_CY, 0])
    lbl = T("white blood cell", 30, TEXT).move_to([x, S1_CY - 0.25, 0])
    g = VGroup(circ, lbl)
    g.circ, g.lbl = circ, lbl
    return g


def s1_objects():
    o = {}
    o["wall"] = wall_bar(S1_WALL_Y)
    o["wlbl"] = T("vessel wall", 24, GREY).move_to([-5.2, 3.2, 0])
    o["inf"] = T("infection", 28, TEXT).move_to([X0, 3.2, 0])
    o["tick"] = Line([X0, 3.0, 0], [X0, 2.88, 0], color=TEXT, stroke_width=4)
    o["cell"] = s1_cell(X0)
    o["q"] = T("?", 80, TEXT, weight=BOLD).move_to([X0, 1.45, 0])
    cen = np.array([X0, S1_CY, 0.0])
    o["dots"] = VGroup(*[Dot(cen + 1.88 * np.array([np.cos(np.radians(a)), np.sin(np.radians(a)), 0]), radius=0.13, color=BLUE)
                         for a in (58, 74, 106, 122)]).set_opacity(0.8)
    o["rlbl"] = T("receptor that grips", 26, BLUE).move_to([4.75, 2.25, 0])
    o["lead"] = Line([3.2, 2.25, 0], [X0 + 1.88 * np.cos(np.radians(58)) + 0.18, 2.25, 0], color=GREY, stroke_width=3)
    o["off"] = T("switched off", 28, RED).move_to([4.75, 1.65, 0])
    o["clk"] = clock(CLOCK_C)
    o["clbl"] = T("about a second", 26, GREY).move_to(CLOCK_C + DOWN * 0.95)
    o["ghost"] = ghost_chip("new protein", 28).move_to(GHOST_C)
    o["strike"] = strike(o["ghost"])
    return o


# ---------------------------------------------------------------------------------------------
# the zoomed stage shared by scenes 2 to 5
# ---------------------------------------------------------------------------------------------
def stage():
    o = {}
    o["wall"] = wall_bar(WALL_Y)
    o["wlbl"] = T("vessel wall", 24, GREY).move_to([5.3, 2.55, 0])
    o["mem"] = membrane(YM)
    o["tint"] = Rectangle(width=14.4, height=4.0 + YM - TM, stroke_width=0, fill_color=GREY, fill_opacity=0.07).move_to(
        [0, (-4.0 + YM - TM) / 2, 0]).set_z_index(-5)
    o["out"] = T("outside", 24, GREY).move_to([-5.5, YM + 0.62, 0])
    o["ins"] = T("inside", 24, GREY).move_to([-5.5, YM - 0.62, 0])
    return o


def add_stage(scene, st):
    scene.add(st["tint"], st["wall"], st["wlbl"], st["mem"], st["out"], st["ins"])


def readout(on=False, flowing=True):
    """the small panel on the right: the grip switch and the state of the cell."""
    o = {}
    o["glbl"] = T("grip", 28, TEXT).move_to([RX, 1.95, 0])
    o["sw"] = toggle(on, scale=0.7).move_to([RX, 1.3, 0])
    o["state"] = T("ON" if on else "OFF", 28, GREEN if on else RED, weight=BOLD).move_to([RX, 0.65, 0])
    o["clbl"] = T("cell", 24, GREY).move_to([RX, -0.1, 0])
    o["chip"] = bchip("flowing" if flowing else "stopped", GREY if flowing else GREEN, 26).move_to([RX, -0.68, 0])
    return o


def add_readout(scene, r):
    scene.add(r["glbl"], r["sw"], r["state"], r["clbl"], r["chip"])


class S00Title(TitleCard):
    LESSON = "Integrins, Rho GTPases and cell movement"
    TITLE = "A grip switched on from inside"


# ---------------------------------------------------------------------------------------------
class S01Stop(SpokenScene):
    """A cell flows past a vessel wall and stops in about a second: too fast to make a new protein."""

    def construct(self):
        o = s1_objects()
        cellg = s1_cell(-3.9)

        self.play(FadeIn(o["wall"]), FadeIn(o["wlbl"]), run_time=0.6)
        self.at("white blood cell")
        self.play(FadeIn(cellg, scale=0.92), run_time=0.7)

        flow = VGroup(*[arr([x, -2.3, 0], [x + 1.0, -2.3, 0], GREY, w=4) for x in (-5.6, -4.2, -2.8)])
        flbl = T("flowing blood", 26, GREY).move_to([-4.0, -2.95, 0])
        self.at("carried along")
        t_c = self.elapsed()
        t_i = self.t_of("an infection") - 0.2
        t_s = self.t_of("can stop") - 0.2
        glide = max(2.0, t_s - t_c)
        label_in = Succession(Wait(max(0.0, t_i - t_c)),
                              AnimationGroup(FadeIn(o["inf"], shift=DOWN * 0.1), Create(o["tick"]), run_time=0.6))
        self.play(cellg.animate(run_time=glide, rate_func=linear).shift(RIGHT * (X0 - 0.7 + 3.9)),
                  AnimationGroup(LaggedStart(*[GrowArrow(a) for a in flow], lag_ratio=0.3), FadeIn(flbl), run_time=1.2),
                  label_in)

        self.at("can stop")
        self.play(cellg.animate.move_to([X0, S1_CY, 0]), FadeOut(flow), FadeOut(flbl), run_time=1.2, rate_func=smooth)

        self.at("about a second", lead=0.45)
        self.play(FadeIn(o["clk"]), FadeIn(o["clbl"]), run_time=0.3)
        self.play(sweep(o["clk"], 1.0))

        self.at("What switches its grip")
        self.play(FadeIn(o["q"], scale=0.6), run_time=0.5)
        self.play(pop(o["q"], 1.25), run_time=0.7)

        self.at("too short")
        self.play(FadeIn(o["ghost"], shift=UP * 0.15), run_time=0.5)
        self.at("new protein")
        self.play(Create(o["strike"]), run_time=0.4)

        self.at("already sit")
        self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in o["dots"]], lag_ratio=0.15),
                  FadeIn(o["rlbl"], shift=LEFT * 0.1), Create(o["lead"]), run_time=0.9)
        self.at("switched off")
        self.play(FadeIn(o["off"], shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Chains(SpokenScene):
    """Zoom into the cell edge: two chains cross the membrane, meet in a head that holds a ligand,
    end in short tails, and carry no enzyme."""

    def construct(self):
        o = s1_objects()
        # the end of scene 1, rebuilt
        self.add(o["wall"], o["wlbl"], o["inf"], o["tick"], o["cell"], o["q"], o["dots"], o["rlbl"], o["lead"], o["off"],
                 o["clk"], o["clbl"], o["ghost"], o["strike"])
        extras = VGroup(o["wlbl"], o["inf"], o["tick"], o["q"], o["rlbl"], o["lead"], o["off"], o["clk"], o["clbl"],
                        o["ghost"], o["strike"], o["dots"], o["cell"].lbl)
        st = stage()
        contact = np.array([X0, S1_WALL_Y - 0.15, 0.0])
        target = np.array([X0, YM + TM, 0.0])
        self.play(FadeOut(extras), FadeOut(o["wall"]), run_time=0.3)
        self.play(o["cell"].circ.animate.scale(10, about_point=contact).shift(target - contact), run_time=0.7, rate_func=smooth)
        self.play(FadeIn(st["mem"]), FadeIn(st["tint"]), FadeOut(o["cell"].circ), FadeIn(st["out"]), FadeIn(st["ins"]),
                  FadeIn(st["wall"]), FadeIn(st["wlbl"]), run_time=0.4)

        ig = Ig(shown=0.0)
        al, be = ig.labels()
        self.add(ig.mob)
        itag = T("integrin", 32, BLUE, weight=BOLD).move_to([RX - 0.1, 1.5, 0])
        self.at("wall is")
        self.play(FadeIn(itag, shift=LEFT * 0.1), ig.VA.animate.set_value(1), run_time=0.9)

        self.at("different chains")
        self.play(ig.VB.animate.set_value(1), run_time=0.9)

        self.at("called")
        self.play(FadeIn(al, scale=0.6), run_time=0.35)
        self.wait(0.25)
        self.play(FadeIn(be, scale=0.6), run_time=0.35)

        self.at("crosses the membrane")
        g = ig.geom()
        flashes = [ShowPassingFlash(Line(g["pts_" + k][1] + DOWN * 0.15, g["pts_" + k][2] + UP * 0.15, color=TEXT, stroke_width=14),
                                    time_width=1.0) for k in ("a", "b")]
        self.play(*flashes, run_time=0.9)

        brace = BraceBetweenPoints([X0 + 0.95, YM + TM + 0.1, 0], [X0 + 0.95, g["C"][1] + 0.55, 0], direction=RIGHT, color=GREY)
        blbl = T("outer parts", 26, GREY).next_to(brace, RIGHT, buff=0.15)
        self.at("outer parts")
        self.play(FadeIn(brace), FadeIn(blbl), run_time=0.6)

        hlbl = T("head", 30, BLUE).move_to([X0 - 1.35, g["C"][1], 0])
        self.at("form a head")
        self.play(ig.VH.animate.set_value(1), FadeIn(hlbl, shift=RIGHT * 0.1), run_time=0.8)

        lig, knob = ligand(ANCHOR, HOVER)
        llbl = T("ligand", 28, YELLOW).move_to(HOVER + [1.05, 0.0, 0])
        self.at("head that grips")
        self.play(FadeOut(brace), FadeOut(blbl), FadeIn(lig, shift=DOWN * 0.2), FadeIn(llbl, shift=LEFT * 0.1), run_time=0.7)

        tb = BraceBetweenPoints([X0 + 2.2, YM - TM - 0.05, 0], [X0 + 2.2, g["tip_b"][1], 0], direction=RIGHT, color=GREY)
        tlbl = T("short tails", 26, GREY).next_to(tb, RIGHT, buff=0.15)
        self.at("short tail")
        self.play(FadeIn(tb), FadeIn(tlbl), run_time=0.5)

        kin = ghost_chip("kinase", 26).move_to([X0 - 2.6, -3.12, 0])
        chn = ghost_chip("channel", 26).move_to([X0 + 3.4, -3.12, 0])
        self.at("There is no")
        self.play(FadeIn(kin, shift=UP * 0.15), run_time=0.5)
        self.play(Create(strike(kin)), run_time=0.4)
        self.at("and no")
        self.play(FadeIn(chn, shift=UP * 0.15), run_time=0.5)
        self.play(Create(strike(chn)), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
def s2_end(scene):
    """the end of scene 2, rebuilt: the stage, a drawn integrin, its ligand and the labels."""
    st = stage()
    ig = Ig()
    al, be = ig.labels()
    lig, knob = ligand(ANCHOR, HOVER)
    add_stage(scene, st)
    scene.add(ig.mob, al, be, lig)
    g = ig.geom()
    tb = BraceBetweenPoints([X0 + 2.2, YM - TM - 0.05, 0], [X0 + 2.2, g["tip_b"][1], 0], direction=RIGHT, color=GREY)
    extras = VGroup(
        T("integrin", 32, BLUE, weight=BOLD).move_to([RX - 0.1, 1.5, 0]),
        T("head", 30, BLUE).move_to([X0 - 1.35, g["C"][1], 0]),
        T("ligand", 28, YELLOW).move_to(HOVER + [1.05, 0.0, 0]),
        tb, T("short tails", 26, GREY).next_to(tb, RIGHT, buff=0.15))
    kin = ghost_chip("kinase", 26).move_to([X0 - 2.6, -3.12, 0])
    chn = ghost_chip("channel", 26).move_to([X0 + 3.4, -3.12, 0])
    extras.add(kin, chn, strike(kin), strike(chn))
    scene.add(extras)
    return st, ig, lig, knob, extras


class S03Bent(SpokenScene):
    """The legs fold at the knee, the head tips back and closes: the resting form holds weakly."""

    def construct(self):
        st, ig, lig, knob, extras = s2_end(self)
        self.play(FadeOut(extras), run_time=0.5)
        g = ig.geom()

        kn = T("knee", 28, GREY).move_to([X0 - 1.5, g["K"][1], 0])
        kar = arr([X0 - 0.95, g["K"][1], 0], [X0 - 0.5, g["K"][1], 0], GREY, w=4, tip=0.16)
        self.at("fold at")
        self.play(FadeIn(kn, shift=RIGHT * 0.1), GrowArrow(kar), run_time=0.5)

        self.at("a knee")
        self.play(ig.E.animate.set_value(0), run_time=1.5, rate_func=smooth)
        g = ig.geom()

        self.at("tips back")
        self.play(Flash(g["C"], color=TEXT, flash_radius=0.95, line_length=0.2, num_lines=10), run_time=0.8)

        self.at("head closed")
        self.play(ig.O.animate.set_value(0), run_time=0.7)

        weak = DashedLine(knob.get_center() + DOWN * KNOB_R, g["C"] + UP * 0.78 + RIGHT * 0.12, color=YELLOW,
                          stroke_width=4, dash_length=0.14)
        weak.set_opacity(0.8)
        wlbl = T("weak grip", 28, RED).move_to([X0 + 2.3, 1.3, 0])
        self.at("integrin holds")
        self.play(Create(weak), FadeIn(wlbl, shift=LEFT * 0.1), run_time=0.8)

        r = readout(False, True)
        self.at("flowing in")
        self.play(FadeIn(r["clbl"]), FadeIn(r["chip"], shift=LEFT * 0.2), run_time=0.7)

        self.at("grip is")
        self.play(FadeIn(r["glbl"]), FadeIn(r["sw"]), FadeIn(r["state"]), run_time=0.6)
        self.play(pop(r["state"], 1.25), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
SIG_X = -3.9
RELAY_Y = -3.1


REC_H = 1.1


def relay_parts():
    """the signal hangs on the wall, a receptor sits in the membrane under it, the relay starts inside."""
    sig = bchip("signal", ORANGE, 26).move_to([SIG_X, 2.3, 0])
    sthr = Line([SIG_X, WALL_BOT, 0], sig.get_top(), color=ORANGE, stroke_width=5)
    rec = RoundedRectangle(corner_radius=0.2, width=0.55, height=REC_H, stroke_color=BLUE, stroke_width=4,
                           fill_color=BLUE, fill_opacity=0.3).move_to([SIG_X, YM, 0])
    rlbl = T("receptor", 24, BLUE).move_to([SIG_X + 1.15, YM + 0.85, 0])
    relay = bchip("relay", TEAL, 26).move_to([SIG_X, RELAY_Y, 0])
    a_out = arr(sig.get_bottom(), rec.get_top(), ORANGE, w=6)
    a_in = arr(rec.get_bottom(), relay.get_top(), TEAL, w=6)
    return sig, sthr, rec, rlbl, relay, a_out, a_in


class S04Talin(SpokenScene):
    """A signal from the wall starts a relay, talin docks on the beta tail, the tails separate, the
    change runs through the membrane, the knee straightens and the cup opens."""

    def construct(self):
        st = stage()
        ig = Ig(e=0.0, op=0.0)
        al, be = ig.labels()
        lig, knob = ligand(ANCHOR, HOVER)
        r = readout(False, True)
        add_stage(self, st)
        add_readout(self, r)
        self.add(ig.mob, al, be, lig)
        g = ig.geom()

        # the signal and the relay on the left
        sig, sthr, rec, rlbl, relay, a_out, a_in = relay_parts()
        self.at("A signal on")
        self.play(FadeIn(sthr), FadeIn(sig, shift=DOWN * 0.15), FadeIn(rec), FadeIn(rlbl), run_time=0.7)
        self.at("relay inside the cell")
        self.play(GrowArrow(a_out), run_time=0.6)
        self.play(pop(rec, 1.15), run_time=0.3)
        self.play(GrowArrow(a_in), run_time=0.4)
        self.play(FadeIn(relay, shift=DOWN * 0.1), run_time=0.4)

        talin = bchip("talin", PURPLE, 26, pad=0.18).move_to([-1.6, -3.12, 0])
        a_tal = always_redraw(lambda: arr(relay.get_right() + DOWN * 0.1, talin.get_left(), TEAL, w=6))
        self.at("helps bring")
        self.add(a_tal)
        self.play(FadeIn(talin, shift=RIGHT * 0.15), run_time=0.6)

        dock = np.array([g["tip_b"][0], g["tip_b"][1] - 0.36, 0.0])
        self.at("protein called")
        self.play(talin.animate.move_to(dock), run_time=1.8, rate_func=smooth)
        talin.add_updater(lambda m: m.move_to(ig.geom()["tip_b"] + DOWN * 0.36))

        self.at("binds the tail")
        self.play(pop(talin, 1.2), run_time=0.7)

        self.at("the two tails")
        self.play(ig.S.animate.set_value(1), run_time=1.0, rate_func=smooth)

        self.at("passes through the membrane")
        g = ig.geom()
        fl = [ShowPassingFlash(_poly(g["pts_" + k], TEAL, 16), time_width=0.55) for k in ("a", "b")]
        self.play(*fl, run_time=1.1)

        self.at("outer part")
        self.play(ig.E.animate.set_value(1), run_time=1.5, rate_func=smooth)
        self.at("head opens")
        self.play(ig.O.animate.set_value(1), run_time=0.8)

        self.at("holds its")
        self.play(*flip(r["sw"], True, GREEN), ReplacementTransform(r["state"], T("ON", 28, GREEN, weight=BOLD).move_to(r["state"])),
                  ig.GL.animate.set_value(0.9), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
def s4_end(scene):
    """the end of scene 4, rebuilt."""
    st = stage()
    ig = Ig(e=1.0, sep=1.0, op=1.0)
    ig.GL.set_value(0.9)
    al, be = ig.labels()
    lig, knob = ligand(ANCHOR, HOVER)
    r = readout(True, True)
    sig, sthr, rec, rlbl, relay, a_out, a_in = relay_parts()
    talin = bchip("talin", PURPLE, 26, pad=0.18).move_to(ig.geom()["tip_b"] + DOWN * 0.36)
    talin.add_updater(lambda m: m.move_to(ig.geom()["tip_b"] + DOWN * 0.36))
    a_tal = always_redraw(lambda: arr(relay.get_right() + DOWN * 0.1, talin.get_left(), TEAL, w=6))
    add_stage(scene, st)
    add_readout(scene, r)
    scene.add(ig.mob, al, be, lig, sthr, sig, rec, rlbl, a_out, a_in, relay, talin, a_tal)
    return dict(st=st, ig=ig, lig=lig, knob=knob, r=r, sig=sig, rec=rec, relay=relay, talin=talin, a_tal=a_tal)


class S05Grip(SpokenScene):
    """The ligand drops into the open cup, the cell stops; nothing was made, so it takes a second;
    the message ran from inside to outside."""

    def construct(self):
        s = s4_end(self)
        ig, knob, r = s["ig"], s["knob"], s["r"]
        g = ig.geom()
        cup = g["C"] + g["d"] * 0.12

        self.at("grabs its")
        self.play(knob.animate.move_to(cup), run_time=0.9, rate_func=smooth)
        self.play(ig.GL.animate.set_value(1.0), pop(knob, 1.3), run_time=0.6)

        stopped = bchip("stopped", GREEN, 26).move_to(r["chip"])
        self.at("The cell stops")
        self.play(ReplacementTransform(r["chip"], stopped), run_time=0.6)

        ghost = ghost_chip("new protein", 26).move_to([-1.7, 2.1, 0])
        self.at("Nothing had to")
        self.play(FadeIn(ghost, shift=UP * 0.15), run_time=0.5)
        self.play(Create(strike(ghost)), run_time=0.4)

        clk = clock([-1.7, 0.95, 0])
        clbl = T("about a second", 26, GREY).move_to([-1.7, 0.1, 0])
        dot = Dot(s["sig"].get_bottom(), radius=0.14, color=TEAL)
        path = VMobject().set_points_as_corners([s["sig"].get_bottom(), s["rec"].get_top(), s["rec"].get_bottom(),
                                                 s["relay"].get_top(), s["relay"].get_right() + DOWN * 0.1, s["talin"].get_left()])
        self.at("about a second", lead=0.45)
        self.play(FadeIn(clk), FadeIn(clbl), FadeIn(dot), run_time=0.3)
        self.play(sweep(clk, 1.0), MoveAlongPath(dot, path, run_time=1.0, rate_func=linear))
        self.play(FadeOut(dot), pop(s["talin"], 1.15), run_time=0.5)

        up = arr([X0 + 1.25, -1.95, 0], [X0 + 1.25, 1.3, 0], TEAL, w=8)
        self.at("started inside")
        self.play(GrowArrow(up), run_time=1.6)
        il = T("inside-out", 28, TEAL, weight=BOLD).move_to([X0 + 2.45, -0.55, 0])
        self.at("this is called")
        self.play(FadeIn(il, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    """A hormone receptor waits for its ligand. The integrin sits among ligand and the cell decides."""

    def construct(self):
        LX, RXX, YM6, S6 = -3.2, 3.5, -0.9, 0.85
        div = DashedLine([0.1, 3.3, 0], [0.1, -3.4, 0], color=GREY, stroke_width=3, dash_length=0.15).set_opacity(0.4)

        # left panel: a hormone receptor and one ligand that arrives
        memL = membrane(YM6, -6.3, -0.4)
        bar = RoundedRectangle(corner_radius=0.25, width=0.7, height=2.2, stroke_color=BLUE, stroke_width=4,
                               fill_color=BLUE, fill_opacity=0.3).move_to([LX, YM6, 0])
        cupc = np.array([LX, YM6 + 1.1 + 0.42, 0.0])
        cup = Arc(radius=0.6, start_angle=np.radians(90 + 70), angle=TAU - np.radians(140), arc_center=cupc,
                  stroke_color=BLUE, stroke_width=RING_W)
        lbl_l = T("hormone receptor", 28, TEXT).move_to([LX, YM6 - 1.55, 0])
        lig_l = knob_at([LX - 2.2, 2.7, 0])
        left = VGroup(memL, bar, cup)

        self.play(FadeIn(div), run_time=0.4)
        self.at("hormone receptor")
        self.play(FadeIn(left), FadeIn(lbl_l), run_time=0.8)
        self.at("waits for")
        self.play(FadeIn(lig_l, scale=0.6), run_time=0.3)
        self.play(lig_l.animate.move_to(cupc + UP * 0.15), run_time=1.2, rate_func=smooth)
        dl = T("the ligand decides", 30, YELLOW, weight=BOLD).move_to([LX, -3.15, 0])
        self.play(FadeIn(dl, shift=UP * 0.1), run_time=0.5)

        # right panel: a bent integrin among many ligands
        memR = membrane(YM6, 0.4, 6.3)
        wallR = wall_bar(WALL_Y, 0.4, 6.3)
        ig = Ig(x0=RXX, e=0.0, op=0.0, s=S6, ym=YM6)
        al, be = ig.labels()
        specs = [(1.2, 1.6), (2.0, 2.5), (RXX, 2.64), (4.9, 2.4), (5.55, 1.4), (6.0, 2.55)]
        ligs = []
        for ax, ky in specs:
            lg, kn = ligand(np.array([ax, WALL_BOT, 0.0]), np.array([ax, ky, 0.0]))
            ligs.append((lg, kn))
        itx = T("integrin", 30, BLUE).move_to([RXX, -3.2, 0])
        self.at("surrounded by")
        self.play(FadeIn(memR), FadeIn(wallR), FadeIn(ig.mob), FadeIn(al), FadeIn(be), FadeIn(itx), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(lg, shift=DOWN * 0.2) for lg, _ in ligs], lag_ratio=0.15), run_time=1.4)

        g = ig.geom()
        self.at("controls the receptor")
        self.play(Flash(g["C"], color=TEXT, flash_radius=0.9, line_length=0.2, num_lines=10), run_time=0.8)
        self.at("all around")
        self.play(LaggedStart(*[pop(k, 1.3) for _, k in ligs], lag_ratio=0.12), run_time=1.2)

        r_gl = T("grip", 24, TEXT).move_to([5.7, -1.4, 0])
        r_sw = toggle(False, scale=0.5).move_to([5.7, -1.95, 0])
        r_st = T("OFF", 28, RED, weight=BOLD).move_to([5.7, -2.55, 0])
        self.at("stays off")
        self.play(FadeIn(r_gl), FadeIn(r_sw), FadeIn(r_st), run_time=0.5)

        g = ig.geom()
        talin = bchip("talin", PURPLE, 24, pad=0.16).move_to([RXX - 2.6, -2.5, 0])
        self.at("until the cell")
        self.play(FadeIn(talin, shift=RIGHT * 0.15), run_time=0.5)
        self.play(talin.animate.move_to(g["tip_b"] + DOWN * 0.34), run_time=1.2, rate_func=smooth)
        talin.add_updater(lambda m: m.move_to(ig.geom()["tip_b"] + DOWN * 0.34))

        self.at("change of shape")
        self.play(ig.S.animate.set_value(1), run_time=0.4)
        self.play(ig.E.animate.set_value(1), run_time=0.9, rate_func=smooth)
        self.play(ig.O.animate.set_value(1), run_time=0.4)
        g = ig.geom()
        knob = ligs[2][1]
        self.at("from inside")
        self.play(knob.animate.move_to(g["C"] + g["d"] * 0.12 * S6), ig.GL.animate.set_value(1.0),
                  *flip(r_sw, True, GREEN), ReplacementTransform(r_st, T("ON", 28, GREEN, weight=BOLD).move_to(r_st)),
                  run_time=0.9)

        dc = T("the cell decides", 30, PURPLE, weight=BOLD).move_to([RXX, -3.15, 0])
        self.at("Keep this rule")
        self.play(FadeOut(itx), FadeIn(dc, shift=UP * 0.1), run_time=0.6)
        self.at("not the ligand")
        self.play(pop(dl, 1.12), pop(dc, 1.12), run_time=0.7)
        self.at("decides when")
        self.play(Flash(g["C"], color=GREEN, flash_radius=1.0, line_length=0.22, num_lines=10), run_time=0.9)
        self.finish()


class S07End(EndCard):
    LINE = "The cell, not the ligand, decides when an integrin grips."
