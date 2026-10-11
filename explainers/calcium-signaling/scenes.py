"""Calcium signaling: a messenger the cell can only move  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = calcium: every ion (dot), the Ca chip, the level in the gauge
  GREEN  = ON: the channel and its open gate, the active site once it is freed
  RED    = OFF / blocking: the pump, the buffers, the segment that blocks the active site, crossed-out routes
  BLUE   = calmodulin (its lobes and its pockets)
  PURPLE = enzymes (the enzymes that make and break cyclic AMP, CaM kinase II and its strand)
  TEAL   = cyclic AMP, the messenger that IS built and broken
  GOLD   = ATP and the phosphate badge
  GREY   = membranes, the ER, labels, parts not yet known, calcium taken out of play

No molecular structures: channel and pump are blobs and a door, calmodulin is two rings with small cups
for its pockets, the kinase is a box with a slot, DNA-free. Calcium is a dot. The crowd of dots is a
picture of concentration (many outside, few in the cytosol, a medium crowd in the ER); the numbers
are written beside it.

One stage for scenes 2 to 4: membrane across the top (a piece of it is the gate), the outside above,
the cytosol below, the ER at the bottom right, a level gauge at the left.
"""
import types

import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"

# ---------------------------------------------------------------------------------------------
# the stage (scenes 2 to 4)
# ---------------------------------------------------------------------------------------------
MEM_Y, MEM_H = 1.5, 0.3
GATE_X, GATE_W = -2.0, 0.9
PIVOT = np.array([GATE_X - GATE_W / 2, MEM_Y, 0.0])
POOL_BOX = (-3.5, 4.0, 1.9, 3.02)          # the outside crowd
CYT_BOX = (-3.5, 4.0, -0.85, 1.1)           # where cytosol dots may sit
ER_C, ER_W, ER_H = (1.8, -2.15), 4.4, 2.3
ER_BOX = (-0.05, 3.65, -2.75, -1.28)             # where ER dots may sit
PUMP_X = 0.8
GX, GB, GH = -4.1, -3.15, 3.7               # gauge: x, bottom, full height (= 1 micromolar)
REST_H = GH / 10                            # 100 nM is a tenth of 1 micromolar
BUF_C = [(-2.8, -1.9), (-1.3, -1.9)]        # the two buffers (scene 4)
BUF_W, BUF_H = 1.4, 1.1


def bchip(text, color=BLUE, size=26, pad=0.2, **kw):
    """chip with an opaque backing so lines drawn behind it do not show through. [back, box, label]"""
    c = chip(text, color, size=size, pad=pad, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def btext(text, size=24, color=GREY, **kw):
    t = T(text, size, color, **kw)
    back = Rectangle(width=t.width + 0.2, height=t.height + 0.12, stroke_width=0, fill_color=BG,
                     fill_opacity=1).move_to(t)
    return VGroup(back, t).set_z_index(8)


def ghost_chip(text, size=26, color=GREY):
    t = T(text, size, color)
    box = RoundedRectangle(corner_radius=0.14, width=t.width + 0.44, height=t.height + 0.44)
    back = RoundedRectangle(corner_radius=0.14, width=box.width, height=box.height, stroke_width=0,
                            fill_color=BG, fill_opacity=1)
    return VGroup(back, DashedVMobject(box, num_dashes=max(18, int(box.width * 9))).set_color(color), t)


def strike(m, color=RED):
    return Line(m.get_corner(DL) + [-0.08, -0.04, 0], m.get_corner(UR) + [0.08, 0.04, 0], color=color, stroke_width=7)


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def pbadge(k=1.0):
    c = Circle(radius=0.18 * k, stroke_color=GOLD, stroke_width=2, fill_color=GOLD, fill_opacity=1)
    return VGroup(c, T("P", 22 * k, BG, weight=BOLD).move_to(c)).set_z_index(9)


def pop(m, s=1.35):
    return m.animate(rate_func=there_and_back).scale(s)


def glow(*mobs, s=1.1, color=TEXT):
    return [Indicate(m, color=color, scale_factor=s) for m in mobs]


def ping(p, color=TEXT):
    """a small burst of light at a point."""
    return Flash(np.array(p, float), color=color, line_length=0.16, flash_radius=0.34, num_lines=9, run_time=0.9)


def path_of(*pts):
    return VMobject().set_points_as_corners([np.array(p, float) for p in pts])


def dot(p, color=YELLOW, r=0.085):
    return Dot(np.array(p, float), radius=r, color=color).set_z_index(5)


def scatter(n, box, mind, seed, pts=None, avoid=None):
    """n random points in box, no two closer than mind, none rejected by avoid()."""
    rng = np.random.RandomState(seed)
    have = [np.array(q, float) for q in (pts or [])]
    out = []
    for _ in range(80000):
        if len(out) == n:
            break
        p = np.array([rng.uniform(box[0], box[1]), rng.uniform(box[2], box[3]), 0.0])
        if avoid and avoid(p):
            continue
        if any(np.linalg.norm(p - q) < mind for q in have + out):
            continue
        out.append(p)
    assert len(out) == n, (len(out), n)
    return out


def _cyt_avoid(p):
    if -2.8 < p[0] < 0.25 and p[1] > 0.5:                    # under the gate: door, labels
        return True
    if np.hypot(p[0] - PUMP_X, p[1] + 0.8) < 0.5:           # above the pump
        return True
    if 1.0 < p[0] < 4.0 and -0.85 < p[1] < -0.2:            # the strip along the ER: ATP chip, labels
        return True
    if -1.0 < p[0] < 0.5 and -0.85 < p[1] < -0.4:           # the pump's name
        return True
    return False


def world():
    """every dot position of scenes 2 to 4, the same each time it is asked for."""
    W = types.SimpleNamespace()
    W.pool = scatter(80, POOL_BOX, 0.23, seed=11)
    W.rest = scatter(4, CYT_BOX, 1.1, seed=3, avoid=_cyt_avoid)
    W.flood = scatter(36, CYT_BOX, 0.36, seed=5, pts=W.rest, avoid=_cyt_avoid)
    W.er = scatter(20, ER_BOX, 0.24, seed=7)
    W.er_new = scatter(12, ER_BOX, 0.24, seed=9, pts=W.er)
    order = sorted(range(len(W.pool)), key=lambda i: np.linalg.norm(W.pool[i] - np.array([GATE_X, 2.0, 0])))
    W.src = order[:36]                                       # the pool dots nearest the gate
    return W


def membrane_set():
    """(left, door, right): the membrane across the stage; the door is a piece of it."""
    xl, xr = -6.3, 6.3
    gl, gr = GATE_X - GATE_W / 2, GATE_X + GATE_W / 2

    def piece(x0, x1, name):
        return RoundedRectangle(corner_radius=0.1, width=x1 - x0, height=MEM_H, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.35).move_to([(x0 + x1) / 2, MEM_Y, 0])
    left, right = piece(xl, gl - 0.03, "l"), piece(gr + 0.03, xr, "r")
    door = RoundedRectangle(corner_radius=0.08, width=GATE_W, height=MEM_H, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.35).move_to([GATE_X, MEM_Y, 0])
    return left, door, right


def posts():
    """the two green posts that make the gate a channel."""
    xs = [PIVOT[0] - 0.16, GATE_X + GATE_W / 2 + 0.16]
    return VGroup(*[RoundedRectangle(corner_radius=0.08, width=0.26, height=0.78, stroke_color=GREEN, stroke_width=3,
                                     fill_color=GREEN, fill_opacity=0.3).move_to([x, MEM_Y, 0]) for x in xs])


def open_door(door):
    return Rotate(door, -PI / 2, about_point=PIVOT)


def close_door(door):
    return Rotate(door, PI / 2, about_point=PIVOT)


def hang_door(door):
    """put the door straight into the open position (for a scene that starts with the gate open)."""
    door.rotate(-PI / 2, about_point=PIVOT)
    return door


def er_blob():
    return RoundedRectangle(corner_radius=0.85, width=ER_W, height=ER_H, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.12).move_to([ER_C[0], ER_C[1], 0])


def gauge_parts():
    out = Rectangle(width=0.4, height=GH, stroke_color=GREY, stroke_width=3).move_to([GX, GB + GH / 2, 0])
    return out


def gauge_fill(h):
    h = max(h, 0.02)
    return Rectangle(width=0.4, height=h, stroke_width=0, fill_color=YELLOW, fill_opacity=0.85).move_to([GX, GB + h / 2, 0])


def tick(y, text, color=GREY):
    lbl = M(text, 22, color).next_to([GX - 0.3, y, 0], LEFT, buff=0.06)
    ln = Line([GX - 0.3, y, 0], [GX - 0.2, y, 0], color=color, stroke_width=3)
    return VGroup(ln, lbl)


def pump_mob():
    blob = RoundedRectangle(corner_radius=0.2, width=0.95, height=0.56, stroke_color=RED, stroke_width=4,
                            fill_color=RED, fill_opacity=0.3).move_to([PUMP_X, -1.0, 0])
    cup = AnnularSector(inner_radius=0.12, outer_radius=0.24, angle=200 * DEGREES, start_angle=170 * DEGREES,
                        color=RED, fill_opacity=1, stroke_width=0).shift([PUMP_X, -0.62, 0])
    back = RoundedRectangle(corner_radius=0.2, width=0.95, height=0.56, stroke_width=0, fill_color=BG,
                            fill_opacity=1).move_to(blob)
    return VGroup(back, blob, cup).set_z_index(6)


def buffer_slots(c):
    """12 places for dots inside a buffer: two rows of six under its label."""
    return [np.array([c[0] + (j - 2.5) * 0.19, c[1] - 0.08 - 0.26 * r, 0.0]) for r in range(2) for j in range(6)]


def buffer_mob(c):
    box = RoundedRectangle(corner_radius=0.16, width=BUF_W, height=BUF_H, stroke_color=RED, stroke_width=3,
                           fill_color=RED, fill_opacity=0.16).move_to([c[0], c[1], 0])
    back = RoundedRectangle(corner_radius=0.16, width=BUF_W, height=BUF_H, stroke_width=0, fill_color=BG,
                            fill_opacity=1).move_to(box)
    lbl = T("buffer", 22, RED).move_to([c[0], c[1] + 0.34, 0])
    return VGroup(back, box, lbl).set_z_index(3)


def stage_dots(W, pool=True, rest=True, er=True, flood=False, vacated=False):
    """the dots of the stage as lists: (pool, rest, er, flood)."""
    pool_d = [dot(p) for p in W.pool] if pool else []
    rest_d = [dot(p) for p in W.rest] if rest else []
    er_d = [dot(p) for p in W.er] if er else []
    flood_d = [dot(p) for p in W.flood] if flood else []
    return pool_d, rest_d, er_d, flood_d


class Film(SpokenScene):
    def outro(self, *anims, run_time=0.38):
        """hold until the narration ends, then clear what the next scene does not inherit."""
        rest = self.narration_s - 0.02 - self.elapsed()
        if rest > 0:
            self.wait(rest)
        if anims:
            self.play(*anims, run_time=run_time)
        self.finish()


class S00Title(TitleCard):
    LESSON = "Calcium: The Messenger Kept at Arm's Length"
    TITLE = "A messenger the cell can only move"


# ---------------------------------------------------------------------------------------------
class S01Puzzle(Film):
    """cAMP is built and broken; calcium is an element, so neither route exists. How can it carry a message?"""

    def construct(self):
        XL, XR, XM = -4.4, 0.6, 4.7
        head = T("other messengers", 28, GREY).move_to([XL, 3.2, 0])
        e1 = bchip("enzyme", PURPLE, 34).move_to([XL, 2.15, 0])
        camp = bchip("cyclic AMP", TEAL, 36).move_to([XL, 0.2, 0])
        e2 = bchip("enzyme", PURPLE, 34).move_to([XL, -1.95, 0])
        a1 = arr(e1.get_bottom(), camp.get_top(), PURPLE)
        a2 = arr(camp.get_bottom(), e2.get_top(), PURPLE)
        lb1 = T("built", 28, GREY).next_to(a1, RIGHT, buff=0.2)
        lb2 = T("broken", 28, GREY).next_to(a2, RIGHT, buff=0.2)
        l1 = T("makes", 28, GREY).next_to(a1, RIGHT, buff=0.2)
        l2 = T("destroys", 28, GREY).next_to(a2, RIGHT, buff=0.2)
        gone = ghost_chip("cyclic AMP", 36, TEAL).move_to(camp)

        self.at("Every other second")
        self.play(Write(head), run_time=1.5)
        self.at("is built")
        self.play(GrowArrow(a1), FadeIn(lb1), FadeIn(camp, scale=0.6), run_time=0.7)
        self.at("and then broken")
        self.play(GrowArrow(a2), FadeIn(lb2), ReplacementTransform(camp, gone), run_time=0.7)

        # the same cycle, with its parts named
        self.at("One enzyme makes")
        self.play(FadeIn(e1, shift=DOWN * 0.15), ReplacementTransform(lb1, l1), run_time=0.6)
        camp2 = bchip("cyclic AMP", TEAL, 36).move_to([XL, 0.2, 0])
        self.play(ReplacementTransform(gone, camp2), run_time=0.5)
        self.at("another enzyme destroys")
        gone2 = ghost_chip("cyclic AMP", 36, TEAL).move_to(camp2)
        self.play(FadeIn(e2, shift=UP * 0.15), ReplacementTransform(lb2, l2), run_time=0.6)
        self.play(ReplacementTransform(camp2, gone2), run_time=0.5)

        ca = bchip("Ca²⁺", YELLOW, 46).move_to([XR, 0.2, 0])
        el = T("an element", 28, GREY).next_to(ca, DOWN, buff=0.35)
        self.at("Calcium is an element")
        self.play(FadeIn(ca, scale=0.7), FadeIn(el, shift=UP * 0.1), run_time=0.6)

        g1 = ghost_chip("enzyme", 34).move_to([XR, 2.15, 0])
        g2 = ghost_chip("enzyme", 34).move_to([XR, -1.95, 0])
        d1 = DashedLine(g1.get_bottom(), ca.get_top() + UP * 0.05, color=GREY, stroke_width=4, dash_length=0.12)
        d2 = DashedLine(ca.get_bottom() + DOWN * 0.7, g2.get_top(), color=GREY, stroke_width=4, dash_length=0.12)
        x1, x2 = strike(g1), strike(g2)
        self.at("No enzyme can make it")
        self.play(FadeIn(g1), Create(d1), run_time=0.5)
        self.play(Create(x1), run_time=0.35)
        self.at("none can break")
        self.play(FadeIn(g2), Create(d2), run_time=0.5)
        self.play(Create(x2), run_time=0.35)

        msg = ghost_chip("a message", 32).move_to([XM, 0.2, 0])
        q = T("?", 64, YELLOW, weight=BOLD).next_to(msg, UP, buff=0.2)
        ar = arr(ca.get_right() + RIGHT * 0.05, msg.get_left(), YELLOW, w=7)
        self.at("So how can")
        self.play(FadeOut(el), run_time=0.3)
        self.play(GrowArrow(ar), FadeIn(msg), run_time=0.6)
        self.at("carry a message")
        self.play(FadeIn(q, scale=0.5), run_time=0.4)
        self.play(pop(q, 1.3), run_time=0.7)
        self.outro(FadeOut(VGroup(head, e1, e2, a1, a2, l1, l2, gone2, ca, g1, g2, d1, d2, x1, x2, msg, q, ar)))


# ---------------------------------------------------------------------------------------------
class S02Held(Film):
    """calcium is moved out and kept out: a few dots in the cytosol, a crowd outside, a medium crowd in the ER."""

    def construct(self):
        W = world()
        L, D, R = membrane_set()
        er = er_blob()
        self.play(FadeIn(L), FadeIn(D), FadeIn(R), FadeIn(er), run_time=0.45)

        # the cell moves calcium out
        xs = [0.6, 1.6, 2.6]
        outs = [Arrow([x, 0.75, 0], [x, 2.35, 0], buff=0, color=YELLOW, stroke_width=7, tip_length=0.28,
                      max_tip_length_to_length_ratio=0.5).set_z_index(5) for x in xs]
        self.at("moves calcium out")
        self.play(LaggedStart(*[GrowArrow(a) for a in outs], lag_ratio=0.25), run_time=0.9)
        pool_d = [dot(p) for p in W.pool]
        self.at("keeps it out")
        self.play(FadeOut(VGroup(*outs)),
                  LaggedStart(*[FadeIn(d, shift=UP * 0.5) for d in pool_d], lag_ratio=0.012), run_time=1.4)

        # the cytosol and its level
        cyt_lbl = T("cytosol", 24, GREY).move_to([-5.2, 1.0, 0])
        gout = gauge_parts()
        gfill = gauge_fill(REST_H)
        t100 = tick(GB + REST_H, "100 nM", YELLOW)
        rest_d = [dot(p) for p in W.rest]
        self.at("A resting cell")
        self.play(FadeIn(cyt_lbl), Create(gout), run_time=0.6)
        self.at("holds free calcium")
        self.play(FadeIn(gfill), LaggedStart(*[FadeIn(d, scale=0.4) for d in rest_d], lag_ratio=0.2), run_time=0.8)
        self.at("the main fluid")
        self.play(*[Indicate(d, color=YELLOW, scale_factor=2.2) for d in rest_d], Indicate(cyt_lbl, color=TEXT, scale_factor=1.15),
                  run_time=0.9)
        self.at("near")
        self.play(FadeIn(t100, shift=RIGHT * 0.1), run_time=0.5)

        # the outside, and how much higher it is
        out_lbl = T("outside\nthe cell", 24, GREY, line_spacing=0.8).move_to([-5.2, 2.55, 0])
        out_val = M("1 to 2 mM", 24, YELLOW).move_to([5.3, 2.75, 0])
        ratio = DoubleArrow([4.35, 0.25, 0], [4.35, 2.45, 0], buff=0, color=TEXT, stroke_width=5, tip_length=0.22)
        ratio_l = T("10,000 to\n20,000\ntimes higher", 22, TEXT, line_spacing=0.85).move_to([5.4, 0.6, 0])
        self.at("Outside")
        self.play(FadeIn(out_lbl), run_time=0.4)
        self.at("the level is")
        self.play(FadeIn(out_val, shift=LEFT * 0.1), run_time=0.5)
        self.at("millimolar")
        self.play(GrowArrow(ratio), *[Indicate(pool_d[k], color=YELLOW, scale_factor=1.9) for k in range(0, 80, 5)], run_time=1.2)
        self.at("times higher")
        self.play(FadeIn(ratio_l), run_time=0.6)

        # the ER
        er_d = [dot(p) for p in W.er]
        er_lbl = T("endoplasmic reticulum", 22, GREY).move_to([ER_C[0], -3.0, 0])
        er_val = M("several\nhundred\nµM", 22, YELLOW, line_spacing=0.85).move_to([5.4, -2.1, 0])
        self.at("The endoplasmic")
        self.play(er.animate.set_stroke(TEXT, 5), FadeIn(er_lbl), run_time=0.6)
        self.at("folded compartment")
        self.play(er.animate.set_stroke(GREY, 3), run_time=0.5)
        self.at("calcium store")
        self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in er_d], lag_ratio=0.05), run_time=1.0)
        self.at("There")
        self.play(FadeIn(er_val, shift=LEFT * 0.1), run_time=0.5)
        self.at("several hundred")
        self.play(*[Indicate(d, color=YELLOW, scale_factor=1.9) for d in er_d[::2]], run_time=1.0)
        self.outro(FadeOut(VGroup(cyt_lbl, out_lbl, out_val, ratio, ratio_l, er_lbl, er_val)))


# ---------------------------------------------------------------------------------------------
class S03Gate(Film):
    """the gate (a piece of the membrane) opens; calcium from the crowd outside pours in; the level rises tenfold."""

    def construct(self):
        W = world()
        L, D, R = membrane_set()
        er = er_blob()
        pool_d, rest_d, er_d, _ = stage_dots(W)
        gout = gauge_parts()
        gfill = gauge_fill(REST_H)
        t100 = tick(GB + REST_H, "100 nM", YELLOW)
        self.add(L, D, R, er, gout, gfill, t100, *pool_d, *rest_d, *er_d)

        dam = btext("a dam", 28, TEXT).move_to([2.6, MEM_Y, 0])
        self.at("Think of a dam")
        self.play(FadeIn(dam), *glow(L, R, D, s=1.0), run_time=0.7)
        res = T("reservoir", 26, GREY).move_to([0.2, 3.32, 0])
        self.at("The reservoir")
        self.play(FadeIn(res, shift=DOWN * 0.1), run_time=0.5)
        self.at("a steady cost")
        self.play(*[Indicate(d, color=YELLOW, scale_factor=2.0) for d in pool_d[::4]], run_time=0.8)

        pst = posts()
        gate_l = btext("gate", 28, GREEN).move_to([GATE_X, 0.78, 0])
        self.at("opening one gate")
        self.play(FadeOut(dam), D.animate.set_stroke(GREEN, 4).set_fill(GREEN, 0.3), FadeIn(pst), FadeIn(gate_l), run_time=0.6)
        self.at("a flood at once")
        self.play(*glow(D, s=1.15), run_time=0.6)

        # the cell makes nothing
        new = ghost_chip("new calcium", 24).move_to([-2.05, -2.95, 0])
        xx = strike(new)
        self.at("To send a calcium signal")
        self.play(FadeOut(res), FadeOut(gate_l), run_time=0.4)
        self.at("makes nothing")
        self.play(FadeIn(new), run_time=0.4)
        self.play(Create(xx), run_time=0.35)

        # the gate opens; ions pressed against the far side come through
        self.at("It opens a channel")
        self.play(FadeOut(new), FadeOut(xx), open_door(D), run_time=0.7)
        rng = np.random.RandomState(4)
        movers = []
        for k, i in enumerate(W.src):
            off = rng.uniform(-0.2, 0.2)
            pth = path_of(W.pool[i], [GATE_X + off, MEM_Y + 0.5, 0], [GATE_X + off, MEM_Y - 0.5, 0], W.flood[k])
            movers.append(MoveAlongPath(pool_d[i], pth, rate_func=smooth))
        gfill_new = gauge_fill(GH)
        self.at("ions already pressed")
        self.play(LaggedStart(*movers, lag_ratio=0.035), Transform(gfill, gfill_new), run_time=3.0)
        ms = btext("milliseconds", 24, GREY).move_to([-0.9, 0.85, 0])
        self.at("within milliseconds")
        self.play(FadeIn(ms), run_time=0.4)

        # refill the crowd where the ions left, quietly; the reservoir stays high
        newpool = [dot(W.pool[i]) for i in W.src]
        self.at("The starting level")
        self.play(FadeOut(ms), LaggedStart(*[FadeIn(d, scale=0.4) for d in newpool], lag_ratio=0.02), run_time=1.0)
        self.add(*newpool)
        self.play(*glow(t100[1], s=1.2), *[Indicate(d, color=YELLOW, scale_factor=2.2) for d in rest_d], run_time=0.7)
        flooded = [pool_d[i] for i in W.src]
        self.at("a modest number")
        self.play(LaggedStart(*[Indicate(d, color=YELLOW, scale_factor=1.8) for d in flooded[::2]], lag_ratio=0.05), run_time=1.4)
        bra = DoubleArrow([GX + 0.5, GB + REST_H, 0], [GX + 0.5, GB + GH, 0], buff=0, color=TEXT, stroke_width=5, tip_length=0.2)
        tenx = T("×10", 34, TEXT, weight=BOLD).next_to(bra, RIGHT, buff=0.12)
        self.at("raises it")
        self.play(GrowArrow(bra), FadeIn(tenx), run_time=0.7)
        t1 = tick(GB + GH, "1 µM", YELLOW)
        self.at("to about one")
        self.play(FadeIn(t1, shift=RIGHT * 0.1), run_time=0.5)
        self.play(*glow(gfill, s=1.08), run_time=0.6)
        self.outro(FadeOut(VGroup(bra, tenx)))


# ---------------------------------------------------------------------------------------------
class S04Pump(Film):
    """every channel has a pump against it: the gate shuts, SERCA moves two ions per ATP, buffers take the rest."""

    def construct(self):
        W = world()
        L, D, R = membrane_set()
        hang_door(D)
        D.set_stroke(GREEN, 4).set_fill(GREEN, 0.3)
        pst = posts()
        er = er_blob()
        pool_d, rest_d, er_d, flood_d = stage_dots(W, flood=True)
        gout = gauge_parts()
        gfill = gauge_fill(GH)
        t100, t1 = tick(GB + REST_H, "100 nM", YELLOW), tick(GB + GH, "1 µM", YELLOW)
        self.add(L, D, R, pst, er, gout, gfill, t100, t1, *pool_d, *rest_d, *er_d, *flood_d)

        pump = pump_mob()
        chan_l = btext("channel", 26, GREEN).move_to([-0.9, 0.85, 0])
        pump_l = btext("pump", 26, RED).move_to([PUMP_X - 1.0, -0.62, 0])
        self.at("Every channel")
        self.play(FadeIn(chan_l), *glow(D, s=1.1), run_time=0.6)
        self.at("has a pump")
        self.play(FadeIn(pump, scale=0.6), FadeIn(pump_l), run_time=0.6)

        path_a = arr([GATE_X + 0.15, MEM_Y + 0.75, 0], [GATE_X + 0.15, MEM_Y - 0.9, 0], GREEN, w=7)
        path_a.set_z_index(7)
        self.at("A channel only opens")
        self.play(FadeOut(chan_l), GrowArrow(path_a), run_time=0.6)
        self.at("path")
        self.play(*glow(path_a, s=1.2), run_time=0.6)
        self.at("the gradient")
        self.play(*[Indicate(pool_d[i], color=YELLOW, scale_factor=1.7) for i in W.src[:8]], run_time=0.9)

        # the gate shuts
        self.at("When it closes")
        self.play(FadeOut(path_a), close_door(D), run_time=0.7)
        self.play(D.animate.set_stroke(GREY, 3).set_fill(GREY, 0.35), run_time=0.25)

        # the pump runs
        sel = sorted(range(36), key=lambda i: np.linalg.norm(W.flood[i] - np.array([PUMP_X, -0.7, 0])))
        pumped, buffered = sel[:12], sel[12:]
        atp_home = np.array([PUMP_X + 1.35, -0.45, 0])
        pumped_n = [0]

        def cycle(n, slow=False):
            k = pumped_n[0]
            if k >= 12:
                return
            ia, ib = pumped[k], pumped[k + 1]
            pumped_n[0] += 2
            atp = bchip("ATP", GOLD, 22, pad=0.12).move_to(atp_home).set_z_index(7)
            paths = []
            for j, i in enumerate((ia, ib)):
                dx = (-0.13, 0.13)[j]
                tgt = W.er_new[k + j]
                paths.append(MoveAlongPath(flood_d[i], path_of(W.flood[i], [PUMP_X + dx, -0.5, 0], [PUMP_X + dx, -1.45, 0], tgt),
                                           rate_func=smooth))
            level = REST_H + (GH - REST_H) * (36 - pumped_n[0]) / 36
            self.play(FadeIn(atp, shift=LEFT * 0.2), run_time=0.15 if not slow else 0.25)
            self.play(atp.animate.move_to([PUMP_X + 0.75, -0.55, 0]), run_time=0.2 if not slow else 0.3)
            self.play(LaggedStart(*paths, lag_ratio=0.3), FadeOut(atp), Transform(gfill, gauge_fill(level)),
                      run_time=0.55 if not slow else 0.9)

        self.at("a pump spends energy")
        self.play(FadeOut(pump_l), run_time=0.3)
        self.at("take calcium out")
        t_stop = self.t_of("The pump called") - 0.45
        while self.elapsed() + 0.9 < t_stop and pumped_n[0] < 12:
            cycle(1)
        self.at("The pump called")
        serca = btext("SERCA", 28, RED).move_to([PUMP_X - 1.2, -0.62, 0])
        self.play(FadeIn(serca), run_time=0.4)
        two = T("2 Ca²⁺ per ATP", 26, GOLD).move_to([PUMP_X + 2.7, -0.5, 0])
        two.set_z_index(8)
        self.at("moves two calcium ions")
        if pumped_n[0] < 12:
            cycle(1, slow=True)
        self.at("for each")
        self.play(FadeIn(two), run_time=0.4)
        t_stop = self.t_of("Buffer proteins") - 0.45
        while self.elapsed() + 0.9 < t_stop and pumped_n[0] < 12:
            cycle(1)
        while pumped_n[0] < 12 and self.elapsed() + 0.6 < t_stop:
            cycle(1)

        # buffers
        bufs = [buffer_mob(c) for c in BUF_C]
        self.at("Buffer proteins")
        self.play(FadeOut(serca), FadeOut(two), *[FadeIn(b, scale=0.7) for b in bufs], run_time=0.6)
        slots = [buffer_slots(c) for c in BUF_C]
        # each buffer takes its nearest twelve of the remaining dots
        remaining = list(buffered)
        moves = []
        for bi, c in enumerate(BUF_C):
            remaining.sort(key=lambda i: np.linalg.norm(W.flood[i] - np.array([c[0], c[1], 0])))
            mine, remaining = remaining[:12], remaining[12:]
            for s_i, i in enumerate(mine):
                moves.append(flood_d[i].animate.move_to(slots[bi][s_i]).set_color(GREY))
        self.at("bind calcium")
        self.play(LaggedStart(*moves, lag_ratio=0.05), Transform(gfill, gauge_fill(REST_H)), run_time=1.6)
        oop = T("out of play", 24, GREY).move_to([-2.05, -3.1, 0])
        self.at("out of play")
        self.play(FadeIn(oop), run_time=0.4)
        self.outro()


# ---------------------------------------------------------------------------------------------
# scene 5 and 6: calmodulin reads the rise
# ---------------------------------------------------------------------------------------------
X0S = 0.0                                # where calmodulin first sits, mid-frame, before the kinase arrives
XC0, RY, LR = -2.0, 0.58, 0.9            # calmodulin centre x, the rope's height, lobe radius
SEP0 = 3.0                                # lobe centres this far apart before they close
SEP1 = 0.5                                # and this far apart around the rope
GAP_OPEN = 160 * DEGREES                  # how wide a lobe opens its mouth
PULL = 2.2                                # how far the grip draws the strand
BODY_X0, BODY_X1, BODY_Y0, BODY_Y1 = -0.6, 4.0, -2.2, 0.4
SLOT_X0, SLOT_X1 = 0.2, 2.0
STRAND_Y = RY
# the four pockets, relative to their lobe's centre: (dx, dy, the direction each one opens)
CUPS = [(0.16, 0.58, 75 * DEGREES), (-0.58, 0.16, 165 * DEGREES), (0.16, -0.58, -75 * DEGREES), (-0.58, -0.16, -165 * DEGREES)]


def cup_mob(c, theta, r_in=0.13, r_out=0.25, color=BLUE, op=1.0):
    """a pocket: a small cup that opens toward direction theta."""
    a = AnnularSector(inner_radius=r_in, outer_radius=r_out, angle=200 * DEGREES, start_angle=theta + PI - 100 * DEGREES,
                      color=color, fill_opacity=op, stroke_width=0)
    return a.shift(np.array([c[0], c[1], 0.0]))


def cup_pos(i, xc, sep):
    """where the calcium of pocket i sits: 0, 1 top lobe; 2, 3 bottom lobe."""
    top = i < 2
    cy = RY + (sep / 2 if top else -sep / 2)
    dx, dy, _ = CUPS[i]
    return np.array([xc + dx, cy + dy, 0.0])


def calmodulin(XC, SEP, GAP, OP):
    """two lobes (rings) with two pockets each, rebuilt from four numbers so they can open, close, move and fade."""
    def build():
        xc, sep, gap, op = XC.get_value(), SEP.get_value(), GAP.get_value(), OP.get_value()
        g = VGroup()
        for up in (True, False):
            cy = RY + (sep / 2 if up else -sep / 2)
            face = -PI / 2 if up else PI / 2
            start, ang = face + gap / 2, TAU - gap - 0.002
            g.add(Sector(radius=LR, start_angle=start, angle=ang, arc_center=[xc, cy, 0], fill_color=BLUE,
                         fill_opacity=0.12 * op, stroke_width=0))
            g.add(Arc(radius=LR, start_angle=start, angle=ang, arc_center=[xc, cy, 0], stroke_color=BLUE,
                      stroke_width=11, stroke_opacity=op))
        for i in range(4):
            g.add(cup_mob(cup_pos(i, xc, sep), CUPS[i][2], op=op))
        return g.set_z_index(2)
    return always_redraw(build)


def kinase_mobs():
    """(body, notch cover, notch outline, strand rope, blocker, label, site label) of CaM kinase II."""
    cx, cy = (BODY_X0 + BODY_X1) / 2, (BODY_Y0 + BODY_Y1) / 2
    body = RoundedRectangle(corner_radius=0.25, width=BODY_X1 - BODY_X0, height=BODY_Y1 - BODY_Y0, stroke_color=PURPLE,
                            stroke_width=4, fill_color=PURPLE, fill_opacity=0.18).move_to([cx, cy, 0])
    cover = Rectangle(width=SLOT_X1 - SLOT_X0, height=1.0, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(
        [(SLOT_X0 + SLOT_X1) / 2, BODY_Y1 - 0.5 + 0.05, 0])
    notch = VMobject(stroke_color=GREY, stroke_width=4, fill_opacity=0)
    notch.set_points_as_corners([[SLOT_X0, BODY_Y1, 0], [SLOT_X0, BODY_Y1 - 0.95, 0], [SLOT_X1, BODY_Y1 - 0.95, 0], [SLOT_X1, BODY_Y1, 0]])
    rope_x0 = XC0 - 1.1
    rope = RoundedRectangle(corner_radius=0.1, width=SLOT_X0 - rope_x0, height=0.22, stroke_width=0, fill_color=PURPLE,
                            fill_opacity=1).move_to([(rope_x0 + SLOT_X0) / 2, STRAND_Y, 0])
    blocker = RoundedRectangle(corner_radius=0.1, width=SLOT_X1 + 0.15 - SLOT_X0, height=0.22, stroke_width=0,
                               fill_color=RED, fill_opacity=1).move_to([(SLOT_X0 + SLOT_X1 + 0.15) / 2, STRAND_Y, 0])
    label = T("CaM kinase II", 30, PURPLE, weight=BOLD).move_to([1.7, -1.5, 0])
    site = T("active site", 22, GREY).move_to([(SLOT_X0 + SLOT_X1) / 2, BODY_Y1 - 0.5, 0])
    body.set_z_index(0)
    cover.set_z_index(1)
    notch.set_z_index(1)
    site.set_z_index(2)
    label.set_z_index(2)
    rope.set_z_index(3)
    blocker.set_z_index(3)
    return body, cover, notch, rope, blocker, label, site


class S05Read(Film):
    """a pocket takes calcium; calmodulin's two lobes fill, open and close on a rope; the rope draws a blocking segment out of the kinase's site."""

    def construct(self):
        # one pocket, big
        big = cup_mob([X0S, RY], PI / 2, r_in=0.62, r_out=1.2)
        cup_l = T("a pocket", 34, BLUE).move_to([X0S + 3.3, RY + 0.55, 0])
        lined = T("lined with oxygens", 28, GREY).move_to([X0S + 3.3, RY - 0.05, 0])
        ca1 = dot([X0S, RY + 2.8, 0], r=0.26)
        self.at("A protein senses")
        self.play(FadeIn(big, scale=0.8), run_time=0.7)
        self.at("calcium")
        self.play(FadeIn(ca1, shift=DOWN * 0.3), run_time=0.5)
        self.at("a pocket")
        self.add(ca1)
        self.play(FadeIn(cup_l, shift=LEFT * 0.1), ca1.animate.move_to([X0S, RY + 0.12, 0]), run_time=0.7)
        self.at("lined with oxygens")
        self.play(FadeIn(lined, shift=LEFT * 0.1), run_time=0.5)

        # calmodulin forms: four pockets, two in each of two lobes
        XC, SEP, GAP, OP = ValueTracker(X0S), ValueTracker(SEP0), ValueTracker(0.0), ValueTracker(0.0)
        cam = calmodulin(XC, SEP, GAP, OP)
        cam_l = T("calmodulin", 34, BLUE, weight=BOLD).move_to([X0S, 3.38, 0])
        self.add(cam)
        self.at("Calmodulin is")
        self.play(FadeOut(cup_l), FadeOut(lined), FadeOut(ca1), FadeOut(big), OP.animate.set_value(1.0), run_time=0.8)
        self.play(FadeIn(cam_l, shift=DOWN * 0.1), run_time=0.4)
        self.at("four of these")
        self.play(LaggedStart(*[ping(cup_pos(i, X0S, SEP0)) for i in range(4)], lag_ratio=0.25), run_time=1.3)
        ef = T("EF hand", 30, BLUE).move_to([X0S - 2.6, RY + SEP0 / 2 + 0.7, 0])
        ef_line = Line(ef.get_right() + RIGHT * 0.05, cup_pos(1, X0S, SEP0) + LEFT * 0.22, color=BLUE, stroke_width=3)
        self.at("called")
        self.play(FadeIn(ef, shift=RIGHT * 0.1), Create(ef_line), run_time=0.6)
        self.at("two in each")
        self.play(*[ping(cup_pos(i, X0S, SEP0)) for i in (0, 1)], run_time=0.6)
        self.at("of two lobes")
        self.play(*[ping(cup_pos(i, X0S, SEP0)) for i in (2, 3)], run_time=0.6)

        # calcium binds, the lobes open, then close on a rope
        cas = [dot(cup_pos(i, X0S, SEP0) + 1.9 * np.array([np.cos(CUPS[i][2]), np.sin(CUPS[i][2]), 0]), r=0.1) for i in range(4)]
        self.at("When calcium binds")
        self.play(FadeOut(ef), FadeOut(ef_line), FadeIn(VGroup(*cas)), run_time=0.3)
        self.play(*[c.animate.move_to(cup_pos(i, X0S, SEP0)) for i, c in enumerate(cas)], run_time=0.9)
        for i, c in enumerate(cas):
            c.add_updater(lambda m, i=i: m.move_to(cup_pos(i, XC.get_value(), SEP.get_value())))
        self.at("the lobes open")
        self.play(GAP.animate.set_value(GAP_OPEN), run_time=0.9)

        body, cover, notch, rope, blocker, klabel, site = kinase_mobs()
        strand = VGroup(rope, blocker)
        kin = VGroup(body, cover, notch)
        self.at("then close around")
        self.play(FadeIn(kin, shift=LEFT * 0.7), FadeIn(strand, shift=LEFT * 0.7), XC.animate.set_value(XC0),
                  cam_l.animate.shift(LEFT * (X0S - XC0)), run_time=1.0)
        hel = T("helix", 28, PURPLE).move_to([XC0 - 2.3, RY, 0])
        hel_line = Line(hel.get_right() + RIGHT * 0.05, [XC0 - 1.2, RY, 0], color=PURPLE, stroke_width=3)
        self.at("a helix")
        self.play(FadeIn(hel, shift=RIGHT * 0.1), Create(hel_line), run_time=0.5)
        self.at("like two hands")
        self.play(SEP.animate.set_value(SEP1), run_time=1.0)
        self.at("gripping a rope")
        self.play(*glow(rope, s=1.1), run_time=0.6)

        # the kinase
        self.at("In the enzyme")
        self.play(FadeOut(hel), FadeOut(hel_line), FadeIn(klabel, shift=UP * 0.1), run_time=0.6)
        self.at("kinase")
        self.play(Indicate(klabel, color=TEXT, scale_factor=1.15), run_time=0.7)
        self.at("a segment")
        self.play(*glow(blocker, s=1.15, color=RED), run_time=0.7)
        self.at("the active site")
        self.play(FadeIn(site, shift=DOWN * 0.1), notch.animate.set_stroke(RED, 5), run_time=0.6)
        self.at("and blocks it")
        self.play(*glow(blocker, s=1.1, color=RED), run_time=0.6)

        # the grip pulls the strand clear
        self.at("Calmodulin grips")
        self.play(ping([XC0 - 0.9, RY, 0]), ping([XC0 + 0.9, RY, 0]), run_time=0.6)
        self.at("beside")
        self.play(*glow(rope, s=1.1), *glow(blocker, s=1.1, color=RED), run_time=0.6)
        self.at("pulls it clear")
        self.play(XC.animate.set_value(XC0 - PULL), strand.animate.shift(LEFT * PULL), cam_l.animate.shift(LEFT * PULL),
                  notch.animate.set_stroke(GREEN, 5), run_time=1.5)
        self.outro()


class S06Rule(Film):
    """the freed site phosphorylates a substrate; then the opening comparison returns with its answer: calcium is moved."""

    def construct(self):
        # rebuild the end of scene 5
        XC, SEP, GAP, OP = ValueTracker(XC0 - PULL), ValueTracker(SEP1), ValueTracker(GAP_OPEN), ValueTracker(1.0)
        cam = calmodulin(XC, SEP, GAP, OP)
        cas = [dot(cup_pos(i, XC0 - PULL, SEP1), r=0.1) for i in range(4)]
        cam_l = T("calmodulin", 34, BLUE, weight=BOLD).move_to([XC0 - PULL, 3.38, 0])
        body, cover, notch, rope, blocker, klabel, site = kinase_mobs()
        strand = VGroup(rope, blocker).shift(LEFT * PULL)
        notch.set_stroke(GREEN, 5)
        self.add(body, cover, notch, strand, klabel, site, cam, *cas, cam_l)

        nx = (SLOT_X0 + SLOT_X1) / 2
        sub = bchip("substrate", GREY, 24, pad=0.14).move_to([nx, 1.6, 0]).set_z_index(4)
        self.at("A rise in an ion")
        self.play(*[ping(c.get_center()) for c in cas], FadeOut(site), FadeIn(sub, shift=DOWN * 0.2), run_time=0.8)
        p = pbadge(1.15).move_to([nx, BODY_Y1 - 0.8, 0])
        self.at("a phosphate")
        self.play(sub.animate.move_to([nx, BODY_Y1 - 0.3, 0]), FadeIn(p, scale=0.5), run_time=0.6)
        self.at("on a protein")
        self.play(p.animate.move_to(sub.get_corner(UR) + [0.0, 0.0, 0]), run_time=0.5)
        self.play(pop(p, 1.5), *glow(sub[1], s=1.1, color=GOLD), run_time=0.6)

        # clear, and bring the opening comparison back
        XL, XR = -3.7, 3.5
        gone = VGroup(body, cover, notch, strand, klabel, cam_l, sub, p, *cas)
        e1 = bchip("enzyme", PURPLE, 34).move_to([XL, 2.4, 0])
        camp = bchip("cyclic AMP", TEAL, 36).move_to([XL, 0.45, 0])
        e2 = bchip("enzyme", PURPLE, 34).move_to([XL, -1.5, 0])
        a1 = arr(e1.get_bottom(), camp.get_top(), PURPLE)
        a2 = arr(camp.get_bottom(), e2.get_top(), PURPLE)
        l1 = T("makes", 28, GREY).next_to(a1, RIGHT, buff=0.2)
        l2 = T("destroys", 28, GREY).next_to(a2, RIGHT, buff=0.2)
        self.at("The cell made nothing")
        self.play(FadeOut(gone), OP.animate.set_value(0.0), run_time=0.6)
        self.remove(cam)
        self.at("Cyclic")
        self.play(FadeIn(e1, shift=DOWN * 0.15), run_time=0.4)
        self.play(GrowArrow(a1), FadeIn(l1), FadeIn(camp, scale=0.7), run_time=0.6)
        self.at("and then")
        self.play(FadeIn(e2, shift=UP * 0.15), GrowArrow(a2), FadeIn(l2), run_time=0.5)
        gone_c = ghost_chip("cyclic AMP", 36, TEAL).move_to(camp)
        self.at("broken")
        self.play(ReplacementTransform(camp, gone_c), run_time=0.5)

        chn = bchip("channel", GREEN, 34).move_to([XR, 2.4, 0])
        ca = bchip("Ca²⁺", YELLOW, 46).move_to([XR, 0.45, 0])
        pmp = bchip("pump", RED, 34).move_to([XR, -1.5, 0])
        b1 = arr(chn.get_bottom(), ca.get_top(), GREEN, w=7)
        b2 = arr(ca.get_bottom(), pmp.get_top(), RED, w=7)
        m1 = T("in", 30, GREEN).next_to(b1, RIGHT, buff=0.2)
        m2 = T("out", 30, RED).next_to(b2, RIGHT, buff=0.2)
        self.at("A channel lets")
        self.play(FadeIn(chn, shift=DOWN * 0.15), run_time=0.4)
        self.play(GrowArrow(b1), FadeIn(m1), FadeIn(ca, scale=0.7), run_time=0.6)
        self.at("a pump takes it out")
        self.play(FadeIn(pmp, shift=UP * 0.15), GrowArrow(b2), FadeIn(m2), run_time=0.6)

        # the rule
        w_made = T("made", 34, GREY).move_to([0.5, -3.0, 0])
        w_dest = T("destroyed", 34, GREY).move_to([2.55, -3.0, 0])
        w_move = T("moved", 38, GREEN, weight=BOLD).move_to([5.0, -3.0, 0])
        self.at("So keep this rule")
        self.play(*glow(ca[1], ca[2], s=1.1), run_time=0.6)
        self.at("cannot be made")
        self.play(FadeIn(w_made), run_time=0.3)
        self.play(Create(strike(w_made)), run_time=0.3)
        self.at("or destroyed")
        self.play(FadeIn(w_dest), run_time=0.3)
        self.play(Create(strike(w_dest)), run_time=0.3)
        self.at("the cell moves it")
        self.play(FadeIn(w_move, scale=0.8), *glow(ca[1], ca[2], s=1.15), run_time=0.7)
        self.finish()


class S07End(EndCard):
    LINE = "Calcium cannot be made or destroyed, so the cell moves it."
