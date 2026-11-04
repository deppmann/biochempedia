"""Courier or Relay?  (chapter 2 of "The Signal from the Target Travels Home", Biochemistrypedia)

Every self.at("...") cue waits for that phrase in audio/words.json (the transcript spellings are used).

COLOR MAP (one colour per concept for the whole chapter)
  YELLOW = NGF, the target's factor (radioactive NGF too)
  TRKA   = TrkA, the receptor (periwinkle blue)
  TEAL   = the courier: the signalling endosome carrying NGF and TrkA, and its path
  ORANGE = the relay: stretches of axon that switch on one after another
  PINK   = dynein, the motor
  PURPLE = the nucleus; LILAC = what CREB does in it (genes on)
  GOLD   = a phosphate badge (phosphorylated, active)
  GREEN  = survival only (cell bodies kept alive)
  RED    = the TrkA kinase inhibitor, and nothing else
  WHITE  = time, "stopped / blocked" marks, neutral headlines
  GREY   = outlines, chambers, structure
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
LILAC = "#D3B0F5"
PINK = "#E58FB8"
ORANGE = "#F2894C"
TRKA = "#6F95FF"
LIGHT = "#C3C9D6"
SOLID = interpolate_color(ManimColor(BG), ManimColor(GREY), 0.17)
TIP = 4.4
SINGLE_POLISH = dict(tube=3.3, body_r=2.25)


# ---------------------------------------------------------------------------------------------
# shared pieces
# ---------------------------------------------------------------------------------------------
class Neuron:
    """A neuron across the frame: cell body at left, axon, tip at right. p(x, y) maps neuron units to the frame.
    Defaults draw the big single-drawing neuron; ROWS parameters draw the slimmer one used when two are stacked."""

    def __init__(self, cx=0.5, cy=0.0, sc=1.0, tube=3.1, body_r=2.2, nuc_r=0.95, nuc_dx=-0.35, er=0.6):
        self.cx, self.cy, self.sc, self.tube, self.body_r, self.er = cx, cy, sc, tube, body_r, er
        h = tube * sc
        body = Circle(radius=body_r * sc).move_to(self.p(-5.0, 0))
        axon = RoundedRectangle(corner_radius=h / 2, width=(TIP + 5.0) * sc, height=h).move_to(self.p((TIP - 5.0) / 2, 0))
        self.cell = Union(body, axon).set_stroke(GREY, 3).set_fill(SOLID, 1)
        self.nuc = Circle(radius=nuc_r * sc, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE,
                          fill_opacity=0.35).move_to(self.p(-5.0 + nuc_dx, 0))
        self.park = -5.0 + nuc_dx + nuc_r + 0.15 + er      # where a courier stops: inside the soma, clear of the nucleus

    def p(self, x, y=0.0):
        return np.array([self.cx + x * self.sc, self.cy + y * self.sc, 0.0])

    def chamber(self, color):
        w, h = 2.9 * self.sc, (self.tube + 1.1) * self.sc
        fill = RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_width=0, fill_color=color,
                                fill_opacity=0.12).move_to(self.p(4.85, 0))
        edge = DashedVMobject(RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_color=color, stroke_width=3),
                              num_dashes=40).move_to(self.p(4.85, 0))
        return VGroup(fill, edge)


ROWS = dict(tube=1.9, body_r=1.4, nuc_r=0.65, nuc_dx=-0.2, er=0.45)
RS = 0.88                      # scale of the two stacked drawings
TOPC, BOTC = 1.95, -1.95
HALF = 0.95 * RS               # half the axon height in the stacked drawings


def rec_bar(pos, sc=1.0, color=TRKA):
    return RoundedRectangle(corner_radius=0.09 * sc, width=0.26 * sc, height=0.7 * sc, stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=0.85).move_to(pos)


def dot(pos, color, r=0.17):
    return Circle(radius=r, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=1).move_to(pos)


def endo(pos, r=0.45):
    """Signalling endosome: a teal bubble holding the receptor and the factor."""
    k = r / 0.45
    bubble = Circle(radius=r, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.22).move_to(pos)
    bar = rec_bar(pos + np.array([-0.12 * k, 0, 0]), 0.75 * k)
    d = dot(pos + np.array([0.14 * k, 0.02 * k, 0]), YELLOW, 0.12 * k)
    return VGroup(bubble, bar, d)


def pbadge(size=0.2):
    c = Circle(radius=size, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=1)
    return VGroup(c, T("P", max(18, int(size * 115)), BG, weight=BOLD).move_to(c))


def tag(text, color=TEXT, size=26, **kw):
    return T(text, size, color, **kw)


def dimmed(m, f=0.3):
    """A copy of m with every fill and stroke opacity multiplied by f (keeps unfilled parts unfilled)."""
    c = m.copy()
    for s_ in c.family_members_with_points():
        s_.set_fill(opacity=s_.get_fill_opacity() * f)
        s_.set_stroke(opacity=s_.get_stroke_opacity() * f)
    return c


def qmark(pos, size=64, color=TEXT):
    return T("?", size, color, weight=BOLD).move_to(pos)


def lit(nuc):
    nuc.set_fill(PURPLE, 0.95).set_stroke(GOLD, 4)
    return nuc


def nuc_badge(nuc):
    return pbadge(nuc.width * 0.32).move_to(nuc.get_center())


def block_sym(pos, sc=1.0):
    """Pink dynein dot under a white 'blocked' sign."""
    body = dot(pos, PINK, 0.15 * sc)
    ring = Circle(radius=0.31 * sc, stroke_color=TEXT, stroke_width=5).move_to(pos)
    slash = Line(pos + np.array([-0.22, 0.22, 0]) * sc, pos + np.array([0.22, -0.22, 0]) * sc, color=TEXT, stroke_width=5)
    return VGroup(body, ring, slash)


def tip_pair(n, k=1.4):
    """Receptor bar at the axon tip with its NGF dot just outside."""
    return rec_bar(n.p(TIP, 0), k * n.sc), dot(n.p(TIP + 0.42, 0), YELLOW, 0.17 * n.sc * k / 1.4)


def legend(x=-6.6, y=-3.55):
    r = rec_bar(ORIGIN, 0.6)
    a = T("TrkA receptor", 24, TRKA)
    d = dot(ORIGIN, YELLOW, 0.11)
    b = T("NGF", 24, YELLOW)
    g = VGroup(VGroup(r, a).arrange(RIGHT, buff=0.15), VGroup(d, b).arrange(RIGHT, buff=0.15)).arrange(RIGHT, buff=0.5)
    return g.move_to([x + g.width / 2, y, 0])


def at_off(scene, phrase, off=0.0):
    """Wait until `off` seconds after a phrase starts (for words the transcript dropped)."""
    rest = scene.t_of(phrase) + off - scene.elapsed()
    if rest > 0.02:
        scene.wait(rest)


def glide(scene, ev, orig, new_x, t, dim=None):
    """Slide a complex to x = new_x; dim=None keeps it as drawn, dim=f darkens it to f of its brightness."""
    tgt = dimmed(orig, dim) if dim is not None else orig.copy()
    tgt.shift(np.array([new_x - tgt.get_center()[0], ev.get_center()[1] - tgt.get_center()[1], 0]))
    scene.play(Transform(ev, tgt), run_time=t, rate_func=linear)


def lit_anim(nuc):
    return nuc.animate.set_fill(PURPLE, 0.95).set_stroke(GOLD, 4)


class S00Title(TitleCard):
    LESSON = "The Signal from the Target Travels Home"
    TITLE = "Courier or Relay?"


# ---------------------------------------------------------------------------------------------
# S01  the question
# ---------------------------------------------------------------------------------------------
class S01Q(SpokenScene):
    def construct(self):
        n = Neuron(cy=-0.35)
        title = T("Courier or Relay?", 54, TEXT, font=TITLE_FONT).move_to([0, 3.25, 0])
        block = RoundedRectangle(corner_radius=0.15, width=1.0, height=4.3, stroke_color=YELLOW, stroke_width=3,
                                 fill_color=YELLOW, fill_opacity=0.14).move_to(n.p(5.3, 0))
        dots = VGroup(*[dot(n.p(5.1, y), YELLOW, 0.17) for y in (-0.85, 0.0, 0.85)])
        self.play(FadeIn(title, shift=DOWN * 0.1), Create(n.cell), FadeIn(n.nuc), run_time=1.0)
        self.at("axon tip")
        rec = rec_bar(n.p(TIP, 0), 1.5)
        tl = tag("axon tip", YELLOW, 30, weight=BOLD).move_to([5.35, n.cy - 2.7, 0])
        self.play(FadeIn(block), FadeIn(dots, scale=0.6), FadeIn(rec), FadeIn(tl), run_time=0.8)
        self.at("cell body")
        cl = tag("cell body", TEXT, 30, weight=BOLD).move_to([n.p(-5.0)[0], n.cy - 2.7, 0])
        self.play(FadeIn(cl), Indicate(n.nuc, color=PURPLE, scale_factor=1.25), run_time=0.8)
        self.at("makes the trip")
        qs = VGroup()
        for x in (-2.3, 0.0, 2.3):
            box = RoundedRectangle(corner_radius=0.12, width=1.2, height=1.2, stroke_color=TEXT, stroke_width=3,
                                   fill_color=BG, fill_opacity=1).move_to(n.p(x, 0))
            qs.add(VGroup(box, T("?", 52, TEXT, weight=BOLD).move_to(box)))
        self.play(LaggedStart(*[FadeIn(q, scale=0.7) for q in qs[::-1]], lag_ratio=0.35), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
# S02  the first evidence: label builds up on the same side
# ---------------------------------------------------------------------------------------------
BIG = 1.25


def bp(x, y):
    """A point of the left panel drawn big and centred (the panel starts large, then makes room for the chick)."""
    return np.array([BIG * (x + 3.25), BIG * y, 0.0])


def big(m):
    m.scale(BIG, about_point=np.array([-3.25, 0, 0])).shift(RIGHT * 3.25)
    return m


class S02Label(SpokenScene):
    def construct(self):
        L = []

        def add(m):
            L.append(big(m))
            return m

        mid = add(DashedLine([-3.25, 2.2, 0], [-3.25, -2.0, 0], color=GREY, stroke_width=2, dash_length=0.12).set_opacity(0.6))

        def eye(x):
            return add(VGroup(Circle(radius=0.42, stroke_color=GREY, stroke_width=3, fill_color=SOLID, fill_opacity=1),
                              Circle(radius=0.14, stroke_width=0, fill_color=GREY, fill_opacity=1)).move_to([x, 1.55, 0]))

        def gang(x, y=-1.65):
            return add(Ellipse(width=1.25, height=0.8, stroke_color=GREY, stroke_width=3, fill_color=SOLID,
                               fill_opacity=1).move_to([x, y, 0]))
        e1, e2 = eye(-4.4), eye(-2.1)
        gl, gr = gang(-4.4), gang(-2.1)
        n1 = add(Line([-4.4, 1.1, 0], [-4.4, -1.25, 0], color=GREY, stroke_width=5))
        n2 = add(Line([-2.1, 1.1, 0], [-2.1, -1.25, 0], color=GREY, stroke_width=5))
        self.play(FadeIn(VGroup(mid, e1, e2, gl, gr, n1, n2)), run_time=0.7)

        self.at("radioactive")
        dots = VGroup(*[add(dot([-4.4 + dx, 1.55 + dy, 0], YELLOW, 0.1)) for dx, dy in ((-0.1, 0.1), (0.12, 0.0), (-0.05, -0.12))])
        rl = add(tag("radioactive NGF", YELLOW, 28, weight=BOLD).move_to([-4.0, 2.75, 0]))
        self.play(FadeIn(dots, scale=0.5), FadeIn(rl), run_time=0.6)
        self.at("placed in a target")
        tl = add(tag("eye", TEXT, 28, weight=BOLD).move_to([-5.35, 1.55, 0]))
        self.play(FadeIn(tl), Indicate(e1, color=YELLOW, scale_factor=1.2), run_time=0.6)
        self.at("built up")
        mover = VGroup(*[d.copy() for d in dots])
        self.add(mover)
        self.remove(dots)
        L.extend(mover)
        self.play(*[m.animate.move_to(bp(-4.4 + (i - 1) * 0.15, -1.45 - 0.05 * i)) for i, m in enumerate(mover)],
                  run_time=0.8, rate_func=smooth)
        self.at("matching ganglion")
        gname = add(tag("superior cervical ganglion", TEXT, 24).move_to([-3.25, -2.6, 0]))
        self.play(gl.animate.set_fill(YELLOW, 0.55).set_stroke(YELLOW, 4), FadeIn(gname), run_time=0.6)
        self.at("same side")
        ss = add(tag("same side", YELLOW, 28, weight=BOLD).move_to([-5.45, 0.0, 0]))
        self.play(FadeIn(ss), run_time=0.5)

        # ---- right: chick embryo
        self.at("in the chick")
        cord = RoundedRectangle(corner_radius=0.35, width=1.0, height=4.3, stroke_color=GREY, stroke_width=3,
                                fill_color=SOLID, fill_opacity=1).move_to([2.3, -0.35, 0])
        motor = RoundedRectangle(corner_radius=0.12, width=0.28, height=3.0, stroke_color=TEXT, stroke_width=2,
                                 fill_color=GREY, fill_opacity=0.55).move_to([2.2, -0.35, 0])
        ys = (1.1, -0.35, -1.8)
        gangs = VGroup(*[Ellipse(width=0.8, height=0.65, stroke_color=GREY, stroke_width=3, fill_color=SOLID,
                                 fill_opacity=1).move_to([3.7, y, 0]) for y in ys])
        links = VGroup(*[Line([2.8, y, 0], [3.3, y, 0], color=GREY, stroke_width=4) for y in ys],
                       *[Line([4.1, y, 0], [5.6, y, 0], color=GREY, stroke_width=5) for y in ys])
        leg = RoundedRectangle(corner_radius=0.35, width=0.8, height=3.4, stroke_color=GREY, stroke_width=3,
                               fill_color=SOLID, fill_opacity=1).move_to([6.0, -0.35, 0])
        ldots = VGroup(*[dot([6.0, y, 0], YELLOW, 0.1) for y in ys])
        legl = tag("leg", TEXT, 28, weight=BOLD).move_to([6.0, -2.45, 0])
        sg = tag("sensory ganglia", TEXT, 24).move_to([3.9, -2.75, 0])
        chick = tag("chick embryo", TEXT, 30, weight=BOLD).move_to([4.0, 2.85, 0])
        rl2 = tag("radioactive NGF", YELLOW, 26, weight=BOLD).move_to([5.15, 1.95, 0])
        lead2 = Arrow([5.85, 1.65, 0], [6.0, 1.3, 0], buff=0, color=YELLOW, stroke_width=3, tip_length=0.14)
        right = VGroup(cord, motor, links, gangs, leg, legl, sg, chick, rl2, lead2)
        movers = VGroup(*[d.copy() for d in ldots])
        shrink = VGroup(*L).animate.scale(1 / BIG, about_point=ORIGIN).shift(LEFT * 3.25)
        self.play(shrink, FadeIn(right), FadeIn(ldots, scale=0.5), run_time=0.6)
        self.add(movers)
        self.remove(ldots)
        self.play(*[m.animate.move_to([3.7, y, 0]) for m, y in zip(movers, ys)], run_time=0.35)
        self.at("motor neurons")
        ml = tag("motor\nneurons", TEXT, 28, line_spacing=0.8, weight=BOLD).move_to([-0.15, 0.45, 0])
        lead = Arrow([0.75, 0.3, 0], [2.0, 0.0, 0], buff=0, color=TEXT, stroke_width=3, tip_length=0.15)
        self.play(*[g.animate.set_fill(YELLOW, 0.55).set_stroke(YELLOW, 4) for g in gangs],
                  FadeIn(ml), Create(lead), motor.animate.set_stroke(TEXT, 4), run_time=0.6)
        self.at("stayed")
        ul = tag("unlabelled", LIGHT, 28, weight=BOLD).move_to([-0.15, -0.55, 0])
        self.play(FadeIn(ul), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
# S03  label is not function
# ---------------------------------------------------------------------------------------------
class S03Limit(SpokenScene):
    def construct(self):
        gang = Ellipse(width=5.4, height=3.8, stroke_color=YELLOW, stroke_width=4, fill_color=YELLOW,
                       fill_opacity=0.5).move_to([0, 0.15, 0])
        gl = tag("labelled ganglion", YELLOW, 32, weight=BOLD).move_to([0, -2.45, 0])
        rays = VGroup(*[dot([0 + dx, 0.15 + dy, 0], YELLOW, 0.14) for dx, dy in
                        ((-1.5, 0.6), (0.0, 0.9), (1.5, 0.45), (-0.8, -0.5), (0.8, -0.65), (0.1, 0.05))])
        self.play(FadeIn(gang, scale=0.8), FadeIn(gl), run_time=0.8)
        self.at("radioactivity went")
        where = tag("where the radioactivity went", TEXT, 30, weight=BOLD).move_to([0, 2.75, 0])
        self.play(FadeIn(rays, scale=0.4, lag_ratio=0.15), FadeIn(where), run_time=0.8)
        chips = VGroup(*[VGroup(RoundedRectangle(corner_radius=0.15, width=4.4, height=1.3, stroke_color=GREY,
                                                 stroke_width=3, fill_color=GREY, fill_opacity=0.1),
                                T(w, 44, TEXT, weight=BOLD)).move_to([3.4, y, 0])
                         for w, y in (("intact?", 2.0), ("active?", 0.15), ("survival?", -1.7))])
        for c in chips:
            c[1].move_to(c[0])
        self.at("not whether")
        grp = VGroup(gang, gl, rays, where)
        self.play(grp.animate.shift(LEFT * 3.4), FadeIn(chips[0], shift=LEFT * 0.3), run_time=0.7)
        self.at("mattered")
        self.play(FadeIn(chips[1], shift=LEFT * 0.3), run_time=0.4)
        self.at("for survival")
        self.play(FadeIn(chips[2], shift=LEFT * 0.3), run_time=0.4)
        self.play(chips[2][0].animate.set_stroke(TEXT, 5).set_fill(TEXT, 0.18), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
# the Campenot dish (S04 - S10)
# ---------------------------------------------------------------------------------------------
DY = -0.3
DH = 5.4
R1, R2 = 3.4, 2.85                   # header rows above the dish
BODIES = [(-1.4, DY + 1.65), (-1.4, DY), (-1.4, DY - 1.65), (0.5, DY + 0.83), (0.5, DY - 0.83)]
END_X = [5.35, 5.6, 5.4, 5.65, 5.5]
BR = 0.6
GAP_Y = DY + 0.415                   # the lane between two axons, used by the survival arrow


def dish_frame():
    outline = RoundedRectangle(corner_radius=0.3, width=12.6, height=DH, stroke_color=GREY, stroke_width=4).move_to([0, DY, 0])
    chambers = VGroup(*[Rectangle(width=w, height=DH - 0.2, stroke_width=0, fill_color=GREY, fill_opacity=0.07).move_to([x, DY, 0])
                        for x, w in ((-4.55, 3.3), (0, 5.0), (4.575, 3.3))])
    divs = VGroup(*[Rectangle(width=0.3, height=DH, stroke_width=0, fill_color=GREY, fill_opacity=0.95).move_to([x, DY, 0])
                    for x in (-2.7, 2.7)])
    divs.set_z_index(4)
    return outline, chambers, divs


def dish_cells(green=False):
    bodies, axons, tips = VGroup(), VGroup(), VGroup()
    for i, (x, y) in enumerate(BODIES):
        cell = Circle(radius=BR, stroke_color=GREY, stroke_width=3, fill_color=SOLID, fill_opacity=1)
        nuc = Circle(radius=0.36, stroke_color=PURPLE, stroke_width=2, fill_color=PURPLE, fill_opacity=0.3)
        if green:
            cell.set_fill(GREEN, 0.75).set_stroke(GREEN, 4)
        bodies.add(VGroup(cell, nuc).move_to([x, y, 0]))
        x0, x1 = x + BR, END_X[i]
        pts = [[x0, y, 0], [x0 + (x1 - x0) * 0.3, y + 0.05, 0], [x0 + (x1 - x0) * 0.62, y - 0.05, 0], [x1, y, 0]]
        axons.add(VMobject(stroke_color=GREY, stroke_width=6).set_points_smoothly(pts))
        tips.add(Circle(radius=0.12, stroke_width=0, fill_color=GREY, fill_opacity=1).move_to([x1, y, 0]))
    axons.set_z_index(1)
    tips.set_z_index(1)
    bodies.set_z_index(2)
    return bodies, axons, tips


def ngf_chamber():
    fill = Rectangle(width=3.3, height=DH - 0.2, stroke_width=0, fill_color=YELLOW, fill_opacity=0.13).move_to([4.575, DY, 0])
    pts = ((3.3, 1.245), (3.55, -0.415), (3.9, 2.1), (4.2, -1.245), (4.5, -2.1), (4.45, -0.415), (4.5, 1.245),
           (5.65, -0.415), (5.4, 1.245), (5.7, -1.245), (5.5, 2.05))
    ds = VGroup(*[dot([x, DY + y, 0], YELLOW, 0.11) for x, y in pts])
    return VGroup(fill, ds)


def chamber_names():
    return VGroup(tag("side chamber", LIGHT, 26).move_to([-4.55, -3.45, 0]),
                  tag("centre chamber", LIGHT, 26).move_to([0, -3.45, 0]),
                  tag("side chamber", LIGHT, 26).move_to([4.575, -3.45, 0]))


def top_labels():
    return (tag("no NGF", TEXT, 34, weight=BOLD).move_to([0, R1, 0]),
            tag("NGF", YELLOW, 34, weight=BOLD).move_to([4.575, R1, 0]))


def body_ring(color=TEXT, dashed=True):
    r = RoundedRectangle(corner_radius=0.6, width=3.9, height=4.95, stroke_color=color, stroke_width=4 if not dashed else 3)
    r.move_to([-0.4, DY, 0])
    return DashedVMobject(r, num_dashes=44) if dashed else r


def distal_box():
    r = RoundedRectangle(corner_radius=0.2, width=3.15, height=4.9, stroke_color=TEXT, stroke_width=3).move_to([4.55, DY, 0])
    return DashedVMobject(r, num_dashes=40)


def survival_arrow():
    # Follow the central neuron's axon back to its soma, including its gentle bends.
    x, y = BODIES[1]
    x0, x1 = x + BR, END_X[1]
    a = TipableVMobject(stroke_color=GREEN, stroke_width=7).set_points_smoothly([
        [x1, y, 0], [x0 + (x1 - x0) * 0.62, y - 0.05, 0],
        [x0 + (x1 - x0) * 0.3, y + 0.05, 0], [x0, y, 0]])
    a.add_tip(tip_length=0.3)
    a.set_z_index(6)
    return a


def state_s06(sc, ring_q=True):
    """The question asked in s06 (also held still in s07)."""
    o, ch, dv = dish_frame()
    bodies, axons, tips = dish_cells()
    ngf = ngf_chamber()
    no, yes = top_labels()
    ring = body_ring()
    q = qmark([0.4, DY + 2.1, 0], 50)
    sc.add(o, ch, dv, bodies, axons, tips, ngf, no, yes)
    if ring_q:
        sc.add(ring, q)
    return dict(o=o, ch=ch, dv=dv, bodies=bodies, axons=axons, tips=tips, ngf=ngf, no=no, yes=yes, ring=ring, q=q)


# ---------------------------------------------------------------------------------------------
class S04Dish(SpokenScene):
    def construct(self):
        o, ch, dv = dish_frame()
        name = tag("Campenot's dish", TEXT, 40, weight=BOLD).move_to([0, R1 + 0.15, 0])
        self.play(Create(o), FadeIn(name, shift=DOWN * 0.1), run_time=1.3)
        self.at("answered that")
        sub = tag("top view", LIGHT, 30).move_to([0, DY, 0])
        self.play(FadeIn(sub), run_time=0.5)
        self.at("sealed dividers")
        sl = tag("sealed dividers", LIGHT, 28, weight=BOLD).move_to([0, 2.75, 0])
        arrs = VGroup(*[Arrow([s_ * 1.3, 2.55, 0], [s_ * 2.55, DY + DH / 2 + 0.05, 0], buff=0.05, color=LIGHT, stroke_width=3,
                              tip_length=0.15) for s_ in (-1, 1)])
        self.play(*[GrowFromCenter(d) for d in dv], FadeIn(sl), FadeIn(arrs), FadeOut(sub), run_time=0.9)
        self.at("into chambers")
        names = chamber_names()
        self.play(FadeIn(ch), FadeIn(names), run_time=0.7)
        self.at("fluids do not mix")
        bars = VGroup()
        for s_ in (-1, 1):
            a, b = np.array([s_ * 1.7, DY, 0]), np.array([s_ * 3.7, DY, 0])
            mid = (a + b) / 2
            bars.add(VGroup(Arrow(a, b, buff=0, color=TEXT, stroke_width=6, tip_length=0.25),
                            Line(mid + UP * 0.4, mid - UP * 0.4, color=TEXT, stroke_width=9).set_z_index(5)))
        self.play(*[Create(b) for b in bars], run_time=0.8)
        self.finish()


class S05Plate(SpokenScene):
    def construct(self):
        o, ch, dv = dish_frame()
        names = chamber_names()
        self.add(o, ch, dv, names)
        bodies, axons, tips = dish_cells()
        self.at("cell bodies")
        cl = tag("cell bodies", TEXT, 32, weight=BOLD).move_to([-0.4, R1, 0])
        self.play(LaggedStart(*[FadeIn(b, scale=0.5) for b in bodies], lag_ratio=0.2), FadeIn(cl), run_time=1.3)
        self.at("axons grow")
        al = tag("axons", TEXT, 32, weight=BOLD).move_to([4.575, R1, 0])
        self.play(*[Create(a) for a in axons], FadeIn(al), run_time=1.5, rate_func=linear)
        self.play(FadeIn(tips, scale=0.5), run_time=0.2)
        self.at("into side chambers")
        na = tag("no axons", LIGHT, 28).move_to([-4.55, DY, 0])
        self.play(Indicate(tips, color=TEXT, scale_factor=1.6), FadeIn(na), run_time=0.8)
        self.finish()


class S06Ask(SpokenScene):
    def construct(self):
        o, ch, dv = dish_frame()
        bodies, axons, tips = dish_cells()
        names = chamber_names()
        self.add(o, ch, dv, bodies, axons, tips, names)
        # the question is the only thing asked: drop the earlier labels
        self.play(FadeOut(names), run_time=0.5)
        self.at("no NGF")
        no, yes = top_labels()
        self.play(FadeIn(no, shift=DOWN * 0.1), run_time=0.5)
        self.at("reach a chamber")
        ngf = ngf_chamber()
        self.play(FadeIn(ngf[0]), FadeIn(ngf[1], scale=0.4, lag_ratio=0.12), FadeIn(yes, shift=DOWN * 0.1), run_time=1.0)
        self.at("do the cell bodies")
        ring = body_ring()
        q = qmark([0.4, DY + 2.1, 0], 50)
        self.play(Create(ring), FadeIn(q, scale=0.5), run_time=0.8)
        self.finish()


class S07Pause(NarratedScene):
    def construct(self):
        state_s06(self)
        self.finish()


def survive_state(sc):
    """s08 end state: the question answered."""
    d = state_s06(sc, ring_q=False)
    for b in d["bodies"]:
        b[0].set_fill(GREEN, 0.75).set_stroke(GREEN, 4)
    ring = body_ring(GREEN, dashed=False)
    br = distal_box()
    arrow = survival_arrow()
    dl = tag("distal axons", TEXT, 30, weight=BOLD).move_to([4.575, R2, 0])
    sub = tag("the far ends near the terminals", TEXT, 26).move_to([3.4, -3.45, 0])
    sv = tag("cell bodies survive", GREEN, 30, weight=BOLD).move_to([-0.4, R2, 0])
    sc.add(ring, br, arrow, dl, sub, sv)
    d.update(ring=ring, br=br, arrow=arrow, dl=dl, sub=sub, sv=sv)
    return d


class S08Reveal(SpokenScene):
    def construct(self):
        d = state_s06(self)
        self.at("many survive")
        ring = body_ring(GREEN, dashed=False)
        sv = tag("cell bodies survive", GREEN, 30, weight=BOLD).move_to([-0.4, R2, 0])
        self.play(FadeOut(d["q"]), FadeOut(d["ring"]),
                  *[b[0].animate.set_fill(GREEN, 0.75).set_stroke(GREEN, 4) for b in d["bodies"]], Create(ring), FadeIn(sv),
                  run_time=1.0)
        self.at("distal axons")
        br = distal_box()
        dl = tag("distal axons", TEXT, 30, weight=BOLD).move_to([4.575, R2, 0])
        self.play(Create(br), FadeIn(dl), run_time=0.8)
        self.at("far ends")
        sub = tag("the far ends near the terminals", TEXT, 26).move_to([3.4, -3.45, 0])
        self.play(FadeIn(sub), run_time=0.6)
        self.at("keep the cell body")
        arrow = survival_arrow()
        self.play(Create(arrow), run_time=1.0)
        self.finish()


class S09Beat(NarratedScene):
    def construct(self):
        survive_state(self)
        self.finish()


class S10Riccio(SpokenScene):
    def construct(self):
        o, ch, dv = dish_frame()
        bodies, axons, tips = dish_cells(green=True)
        ngf = ngf_chamber()
        no, yes = top_labels()
        self.add(o, ch, dv, bodies, axons, tips, ngf, no, yes)
        self.at("with NGF only")
        credit = tag("Riccio and colleagues,\nGinty laboratory", LIGHT, 24, line_spacing=0.8).move_to([-5.1, 3.15, 0])
        self.play(Indicate(yes, color=YELLOW, scale_factor=1.2), FadeIn(credit), run_time=0.7)
        self.at("distal axons")
        br = distal_box()
        dl = tag("distal axons", TEXT, 30, weight=BOLD).move_to([4.575, R2, 0])
        self.play(Create(br), FadeIn(dl), run_time=0.7)
        self.at("became phosphorylated")
        badges = VGroup(*[nuc_badge(b[1]).set_z_index(6) for b in bodies])
        pl = tag("phosphorylated CREB", GOLD, 30, weight=BOLD).move_to([-0.1, R2, 0])
        self.play(*[b[1].animate.set_fill(PURPLE, 0.95).set_stroke(GOLD, 4) for b in bodies],
                  LaggedStart(*[FadeIn(b, scale=0.4) for b in badges], lag_ratio=0.1), FadeIn(pl), run_time=1.1)
        self.at("transcription factor")
        tl = tag("CREB: a transcription factor", LILAC, 30, weight=BOLD).move_to([-1.6, -3.45, 0])
        self.play(FadeIn(tl), run_time=0.6)
        self.at("switches genes on")
        gl = tag("that switches genes on", LILAC, 30, weight=BOLD)
        gl.next_to(tl, RIGHT, buff=0.3)
        self.play(FadeIn(gl), *[Flash(b[1], color=PURPLE, flash_radius=0.6, line_length=0.18) for b in bodies], run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
# S11  was it the same receptor, carried from the tip?
# ---------------------------------------------------------------------------------------------
class S11Active(SpokenScene):
    def construct(self):
        n = Neuron(cy=-0.1, **SINGLE_POLISH)
        cham = n.chamber(YELLOW)
        nl = tag("NGF", YELLOW, 32, weight=BOLD).move_to(n.p(4.85, n.tube / 2 + 1.1))
        lit(n.nuc)
        badge = nuc_badge(n.nuc)
        self.play(Create(n.cell), FadeIn(n.nuc), FadeIn(cham), FadeIn(nl), FadeIn(badge, scale=0.5), run_time=1.0)
        self.at("kinase activity")
        pos = [(-3.75, -0.85), (-3.6, 0.0), (-3.75, 0.85)]
        bars = VGroup(*[rec_bar(n.p(x, y), 1.1).rotate(a) for (x, y), a in zip(pos, (0.2, 0, -0.2))])
        rings = VGroup(*[Circle(radius=0.36, stroke_color=TRKA, stroke_width=4).move_to(b) for b in bars])
        self.play(FadeIn(bars, scale=0.6), Create(rings), run_time=0.8)
        self.at("cell body")
        ll = tag("TrkA kinase needed\nin the cell body", TRKA, 32, weight=BOLD, line_spacing=0.8).move_to([-4.2, 2.8, 0])
        self.play(FadeIn(ll, shift=DOWN * 0.1), run_time=0.7)
        self.at("same receptor")
        tipr, td = tip_pair(n, 1.6)
        self.play(FadeIn(tipr), FadeIn(td, scale=0.6), run_time=0.5)
        self.play(Indicate(tipr, color=TRKA, scale_factor=1.4), Indicate(bars, color=TRKA, scale_factor=1.4), run_time=0.8)
        self.at("carried from the tip")
        arr = DashedLine(n.p(TIP - 0.8, -0.3), n.p(-3.0, -0.3), color=TEAL, stroke_width=8, dash_length=0.24)
        arr.add_tip(tip_length=0.34)
        q = qmark(n.p(0.5, 0.55), 110, TEAL)
        qt = tag("carried from the tip?", TEAL, 34, weight=BOLD).move_to([n.p(0.5)[0], n.cy - n.tube / 2 - 0.55, 0])
        self.play(Create(arr), FadeIn(q, scale=0.5), FadeIn(qt), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
# S12 / S13  courier and relay
# ---------------------------------------------------------------------------------------------
S12_CY = 0.15


def courier_big_final():
    """s12 end state: the courier parked just inside the cell body, which is now lit."""
    n = Neuron(cy=S12_CY, **SINGLE_POLISH)
    e = endo(n.p(n.park, 0), 0.6)
    e[0].set_stroke(TEAL, 6).set_fill(TEAL, 0.5)
    lit(n.nuc)
    badge = nuc_badge(n.nuc)
    ngf = VGroup(*[dot(n.p(5.1, y), YELLOW, 0.14) for y in (-0.6, 0.6)])
    lab = tag("courier", TEAL, 46, weight=BOLD).move_to([n.p(3.2)[0], S12_CY + 1.55 + 0.5, 0])
    lg = legend()
    return n, VGroup(n.cell, n.nuc, badge, e, ngf, lab, lg)


class S12Courier(SpokenScene):
    def construct(self):
        n = Neuron(cy=S12_CY, **SINGLE_POLISH)
        rec, d = tip_pair(n, 1.6)
        ngf = VGroup(*[dot(n.p(5.1, y), YELLOW, 0.14) for y in (-0.6, 0.6)])
        self.play(FadeIn(VGroup(n.cell, n.nuc, rec, d, ngf)), run_time=0.4)
        self.at("how did it travel")
        self.play(Indicate(rec, color=TRKA, scale_factor=1.3), run_time=0.6)
        at_off(self, "how did it travel", 1.3)
        lab = tag("courier", TEAL, 46, weight=BOLD).move_to([n.p(3.2)[0], S12_CY + 1.55 + 0.5, 0])
        self.play(FadeIn(lab, shift=DOWN * 0.1), run_time=0.5)
        self.at("the NGF")
        lg = legend()
        pos = n.p(TIP - 1.0, 0)
        e = endo(pos, 0.6)
        self.play(FadeIn(e[0], scale=0.5), Transform(rec, e[1]), Transform(d, e[2]), FadeIn(lg), run_time=0.8)
        ev = VGroup(e[0], rec, d)
        self.at("complex itself")
        T_move = max(1.6, 6.95 - self.elapsed())
        self.play(ev.animate.shift(LEFT * (pos[0] - n.p(n.park, 0)[0])), run_time=T_move, rate_func=linear)
        badge = nuc_badge(n.nuc)
        self.play(e[0].animate.set_stroke(TEAL, 6).set_fill(TEAL, 0.5), Flash(ev[0], color=TEAL, flash_radius=1.0),
                  lit_anim(n.nuc), FadeIn(badge, scale=0.5), run_time=0.5)
        self.finish()


class Rows:
    """The two stacked drawings: courier on top, relay below."""

    def __init__(self):
        self.nt = Neuron(cy=TOPC, sc=RS, **ROWS)
        self.nb = Neuron(cy=BOTC, sc=RS, **ROWS)
        nt, nb = self.nt, self.nb
        self.ngf_t = VGroup(*[dot(nt.p(5.1, y), YELLOW, 0.13) for y in (-0.5, 0.5)])
        self.segs = segments(nb)
        self.tip_b = VGroup(*tip_pair(nb, 1.3))
        self.top = VGroup(nt.cell, nt.nuc, self.ngf_t)
        self.bot = VGroup(nb.cell, nb.nuc, self.segs, self.tip_b)
        x = 0.5 + RS * 3.9
        self.la = tag("courier", TEAL, 38, weight=BOLD).move_to([x, TOPC + HALF + 0.42, 0])
        self.lb = tag("relay", ORANGE, 38, weight=BOLD).move_to([x, BOTC + HALF + 0.42, 0])

    def x(self, local):
        return 0.5 + local * RS


EDGES = [-3.7, -0.7, 1.9, 4.5]   # proximal, middle, distal stretches (neuron units); the distal one reaches the tip receptor


def segments(n):
    sc = n.sc
    out = VGroup()
    for a, b in zip(EDGES[:-1], EDGES[1:]):
        out.add(RoundedRectangle(corner_radius=0.14 * sc, width=(b - a - 0.16) * sc, height=(n.tube - 0.45) * sc, stroke_color=GREY,
                                 stroke_width=2, fill_color=GREY, fill_opacity=0.0).move_to(n.p((a + b) / 2, 0)))
    return out


def light_seg(s_):
    return s_.animate.set_fill(ORANGE, 0.55).set_stroke(ORANGE, 3)


class S13Relay(SpokenScene):
    def construct(self):
        # carry s12's finished picture, then cross-fade to the two stacked drawings
        n0, big_g = courier_big_final()
        self.add(big_g)
        R = Rows()
        nt = R.nt
        e = endo(nt.p(nt.park, 0), 0.45 * RS)
        e[0].set_stroke(TEAL, 5).set_fill(TEAL, 0.5)
        lit(nt.nuc)
        badge_t = nuc_badge(nt.nuc)
        top = VGroup(R.top, e, badge_t)
        self.play(FadeOut(big_g), FadeIn(top), FadeIn(R.bot), FadeIn(R.la), FadeIn(R.lb, shift=DOWN * 0.1), run_time=0.8)
        self.at("each stretch")
        self.play(Transform(top, dimmed(top, 0.35)), light_seg(R.segs[2]), run_time=0.6)
        self.play(light_seg(R.segs[1]), run_time=0.5)
        self.play(light_seg(R.segs[0]), run_time=0.5)
        badge_b = nuc_badge(R.nb.nuc)
        self.play(lit_anim(R.nb.nuc), FadeIn(badge_b, scale=0.5), run_time=0.4)
        self.at("row of dominoes")
        self.play(Indicate(R.segs, color=ORANGE, scale_factor=1.03), run_time=0.6)
        lg = legend()
        self.at("no one molecule")
        self.play(FadeIn(lg), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
# S14 - S17  the dynein block
# ---------------------------------------------------------------------------------------------
BLK_X = 0.5 + 0.6 * RS          # the middle stretch's centre
MSG_POS = [1.1, 0.0, 0]


def block_parts(R):
    """Everything the block drawings add: endosome stuck before the block, signs, labels, tags."""
    nt = R.nt
    e = endo([0.5 + 2.3 * RS, TOPC, 0], 0.45 * RS)
    sign_t = block_sym([BLK_X, TOPC, 0])
    sign_b = block_sym([BLK_X, BOTC, 0])
    dyn_t = tag("dynein", PINK, 26, weight=BOLD).move_to([BLK_X, TOPC - HALF - 0.34, 0])
    dyn_b = tag("dynein", PINK, 26, weight=BOLD).move_to([BLK_X, BOTC - HALF - 0.34, 0])
    ld_t = Line([BLK_X, TOPC - HALF - 0.1, 0], [BLK_X, TOPC - 0.34, 0], color=PINK, stroke_width=2)
    ld_b = Line([BLK_X, BOTC - HALF - 0.1, 0], [BLK_X, BOTC - 0.34, 0], color=PINK, stroke_width=2)
    surv_t = tag("survival lost", TEXT, 26, weight=BOLD).move_to([-4.5, TOPC + 1.232 + 0.32, 0])
    surv_b = tag("survival lost", TEXT, 26, weight=BOLD).move_to([-4.5, BOTC - 1.232 - 0.32, 0])
    credit = tag("Heerssen and colleagues, 2004", LIGHT, 24).move_to([4.0, -3.55, 0])
    return dict(e=e, sign_t=sign_t, sign_b=sign_b, dyn_t=dyn_t, dyn_b=dyn_b, ld_t=ld_t, ld_b=ld_b, surv_t=surv_t, surv_b=surv_b,
                credit=credit)


def state_s14(sc):
    R = Rows()
    B = block_parts(R)
    q = tag("courier?", TEAL, 38, weight=BOLD).move_to(R.la)
    sc.add(R.top, B["e"], R.bot, q, R.lb, B["sign_t"], B["sign_b"], B["dyn_t"], B["dyn_b"], B["ld_t"], B["ld_b"], B["surv_t"],
           B["surv_b"], B["credit"])
    return R, B


class S14Dynein(SpokenScene):
    def construct(self):
        # start from s13's end state, then reset to a neutral picture while the blocks arrive
        R = Rows()
        nt = R.nt
        e0 = endo(nt.p(nt.park, 0), 0.45 * RS)
        e0[0].set_stroke(TEAL, 5).set_fill(TEAL, 0.5)
        lit(nt.nuc)
        bt = nuc_badge(nt.nuc)
        old_top = dimmed(VGroup(R.top, e0, bt), 0.35)
        for s_ in R.segs:
            s_.set_fill(ORANGE, 0.55).set_stroke(ORANGE, 3)
        lit(R.nb.nuc)
        bb = nuc_badge(R.nb.nuc)
        self.add(old_top, R.bot, bb, R.la, R.lb)
        # the neutral targets
        R2 = Rows()
        B = block_parts(R2)
        q = tag("courier?", TEAL, 38, weight=BOLD).move_to(R.la)
        self.at("blocking")
        self.play(FadeOut(old_top), FadeIn(R2.top), FadeIn(B["e"]),
                  FadeOut(bb), *[s_.animate.set_fill(GREY, 0.0).set_stroke(GREY, 2) for s_ in R.segs],
                  R.nb.nuc.animate.set_fill(PURPLE, 0.35).set_stroke(PURPLE, 3),
                  FadeIn(B["sign_t"], scale=0.5), FadeIn(B["sign_b"], scale=0.5),
                  FadeIn(B["dyn_t"]), FadeIn(B["dyn_b"]), FadeIn(B["ld_t"]), FadeIn(B["ld_b"]), FadeIn(B["credit"]),
                  run_time=0.9)
        self.at("stops survival")
        self.play(FadeIn(B["surv_t"], shift=UP * 0.1), FadeIn(B["surv_b"], shift=UP * 0.1), run_time=0.6)
        self.at("does that prove")
        self.play(FadeOut(R.la), FadeIn(q), run_time=0.4)
        self.finish()


class S15Pause(NarratedScene):
    def construct(self):
        state_s14(self)
        self.finish()


class S16Reveal(SpokenScene):
    def construct(self):
        R, B = state_s14(self)
        self.at("each relay step")
        extra = VGroup(*[block_sym([R.x(c), BOTC, 0]) for c in (-2.2, 3.2)])
        self.play(FadeIn(extra, scale=0.4, lag_ratio=0.3), run_time=0.8)
        self.at("stop too")
        top_g = VGroup(R.top, B["e"], B["sign_t"])
        bot_g = VGroup(R.bot, B["sign_b"], extra)
        self.play(Transform(top_g, dimmed(top_g, 0.28)), Transform(bot_g, dimmed(bot_g, 0.28)), run_time=0.8)
        self.at("this block")
        msg = tag("this block cannot tell them apart", TEXT, 30, weight=BOLD).move_to(MSG_POS)
        self.play(FadeIn(msg, shift=UP * 0.1), run_time=0.7)
        self.finish()


class S17Beat(NarratedScene):
    def construct(self):
        R, B = state_s14(self)
        extra = VGroup(*[block_sym([R.x(c), BOTC, 0]) for c in (-2.2, 3.2)])
        self.add(extra)
        top_g = VGroup(R.top, B["e"], B["sign_t"])
        bot_g = VGroup(R.bot, B["sign_b"], extra)
        for g in (top_g, bot_g):
            for s_ in g.family_members_with_points():
                s_.set_fill(opacity=s_.get_fill_opacity() * 0.28)
                s_.set_stroke(opacity=s_.get_stroke_opacity() * 0.28)
        self.add(tag("this block cannot tell them apart", TEXT, 30, weight=BOLD).move_to(MSG_POS))
        self.finish()


# ---------------------------------------------------------------------------------------------
# S18  block TrkA kinase only in the middle stretch
# ---------------------------------------------------------------------------------------------
S_KW = dict(tube=2.3, body_r=1.7, nuc_r=0.75, nuc_dx=-0.3, er=0.5)
S_CY = 1.4


def single():
    n = Neuron(cy=S_CY, **S_KW)
    segs = segments(n)
    rec, d = tip_pair(n, 1.4)
    return n, segs, VGroup(rec, d)


def inhibitor_marks(n, short=False):
    x0, x1 = n.p(EDGES[1] - 0.05)[0], n.p(EDGES[2] + 0.05)[0]
    y = n.cy - n.tube / 2 * n.sc - 0.25
    br = VGroup(Line([x0, y, 0], [x1, y, 0], color=RED, stroke_width=4),
                Line([x0, y, 0], [x0, y + 0.18, 0], color=RED, stroke_width=4),
                Line([x1, y, 0], [x1, y + 0.18, 0], color=RED, stroke_width=4))
    mx = (x0 + x1) / 2
    l1 = tag("TrkA kinase inhibitor", RED, 32, weight=BOLD).move_to([mx, y - 0.42, 0])
    l2 = tag("this stretch only", RED, 28).move_to([mx, y - 0.88, 0])
    return br, l1, l2


def grey_out(seg):
    seg.set_fill(GREY, 0.8).set_stroke(RED, 3)
    return seg


def empty_box(text, color, x, y=-2.35):
    box = RoundedRectangle(corner_radius=0.16, width=4.2, height=1.0, stroke_color=color, stroke_width=3,
                           fill_color=color, fill_opacity=0.08).move_to([x, y, 0])
    # Anchor to the rectangle, independent of the question mark's text metrics.
    label = T(text, 34, color, weight=BOLD).move_to(box)
    return VGroup(box, label)


def note_s18():
    return tag("A courier test needs transport to keep running.", LIGHT, 26).move_to([0.5, -1.5, 0])


def credit_ye():
    return tag("Ye, Kuruvilla, Zweifel and Ginty, 2003", LIGHT, 24).move_to([0, -3.6, 0])


def state_s18(sc):
    n, segs, tipg = single()
    grey_out(segs[1])
    br, l1, l2 = inhibitor_marks(n)
    note = note_s18()
    credit = credit_ye()
    c1 = empty_box("relay?", ORANGE, -2.6)
    c2 = empty_box("courier?", TEAL, 2.6)
    sc.add(n.cell, n.nuc, segs, tipg, br, l1, l2, note, credit, c1, c2)
    return dict(n=n, segs=segs, tipg=tipg, br=br, l1=l1, l2=l2, note=note, credit=credit, c1=c1, c2=c2)


class S18Middle(SpokenScene):
    def construct(self):
        n, segs, tipg = single()
        grp = VGroup(n.cell, n.nuc, segs, tipg)
        grp.shift(DOWN * 1.3)
        self.play(Create(n.cell), FadeIn(n.nuc), run_time=0.8)
        self.play(FadeIn(segs), FadeIn(tipg), run_time=0.5)
        credit = credit_ye()
        self.add(credit)
        self.at("middle stretch")
        self.play(grp.animate.shift(UP * 1.3), run_time=0.6)
        self.play(segs[1].animate.set_fill(GREY, 0.8).set_stroke(RED, 3), run_time=0.4)
        self.at("with an inhibitor")
        br, l1, l2 = inhibitor_marks(n)
        self.play(Create(br), FadeIn(l1, shift=UP * 0.1), FadeIn(l2), run_time=0.8)
        self.at("what does each model")
        c1 = empty_box("relay?", ORANGE, -2.6)
        c2 = empty_box("courier?", TEAL, 2.6)
        self.play(FadeIn(c1, shift=UP * 0.2), FadeIn(c2, shift=UP * 0.2), run_time=0.5)
        self.at("each model")
        note = note_s18()
        self.play(FadeIn(note), run_time=0.5)
        self.finish()


class S19Pause(NarratedScene):
    def construct(self):
        state_s18(self)
        self.finish()


# ---------------------------------------------------------------------------------------------
# S20  what each model predicts
# ---------------------------------------------------------------------------------------------
def inhibit_overlay(n):
    x0, x1 = n.p(EDGES[1])[0], n.p(EDGES[2])[0]
    return RoundedRectangle(corner_radius=0.12, width=(x1 - x0) - 0.1, height=(n.tube - 0.45) * n.sc, stroke_color=RED,
                            stroke_width=3, fill_color=GREY, fill_opacity=0.8).move_to([(x0 + x1) / 2, n.cy, 0])


def barred_arrow(a, b, color=TEXT, w=6):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    perp = np.array([-d[1], d[0], 0])
    mid = (a + b) / 2
    return VGroup(Arrow(a, b, buff=0, color=color, stroke_width=w, tip_length=0.25),
                  Line(mid + perp * 0.3, mid - perp * 0.3, color=color, stroke_width=w + 3))


def bracket_label(n, above=True, dy=0.0):
    """Red bracket under (or over) the grey stretch of a stacked drawing, with its label."""
    x0, x1 = n.p(EDGES[1] - 0.05)[0], n.p(EDGES[2] + 0.05)[0]
    mx = (x0 + x1) / 2
    if above:    # label sits in the gap between the two drawings, under the top axon
        y = n.cy - HALF - 0.13
        tick = 0.15
        l1y, l2y = y - 0.30, y - 0.69
    else:
        y = n.cy - HALF - 0.13
        tick = 0.15
        l1y, l2y = y - 0.30, y - 0.69
    br = VGroup(Line([x0, y, 0], [x1, y, 0], color=RED, stroke_width=4),
                Line([x0, y, 0], [x0, y + tick, 0], color=RED, stroke_width=4),
                Line([x1, y, 0], [x1, y + tick, 0], color=RED, stroke_width=4))
    l1 = tag("TrkA kinase inhibitor", RED, 26, weight=BOLD).move_to([mx, l1y, 0])
    l2 = tag("this stretch only", RED, 24).move_to([mx, l2y, 0])
    return VGroup(br, l1, l2)


class S20Pred(SpokenScene):
    def construct(self):
        d = state_s18(self)
        R = Rows()
        nt, nb = R.nt, R.nb
        top_g = VGroup(nt.cell, nt.nuc, inhibit_overlay(nt), R.ngf_t, *tip_pair(nt, 1.3))
        ev = endo([nt.p(TIP - 1.1)[0], TOPC, 0], 0.45 * RS)
        orig = ev.copy()
        bot_g = VGroup(nb.cell, nb.nuc, R.segs, R.tip_b)
        r_over = inhibit_overlay(nb)
        lab_t = bracket_label(nt)
        lab_b = bracket_label(nb)
        lg = legend()
        old = VGroup(*[v for k, v in d.items() if k not in ("n", "segs", "tipg")], d["n"].cell, d["n"].nuc, d["segs"], d["tipg"])
        self.play(FadeOut(old), FadeIn(top_g), FadeIn(ev), FadeIn(bot_g), FadeIn(r_over), FadeIn(R.la), FadeIn(R.lb),
                  FadeIn(lab_t), FadeIn(lab_b), FadeIn(lg), run_time=0.4)
        self.at("relay that")
        self.play(light_seg(R.segs[2]), run_time=0.5)
        self.at("each stretch")
        kin = VGroup(*[rec_bar(R.segs[i].get_center(), 0.85 * RS) for i in (0, 2)])
        self.play(FadeIn(kin, scale=0.5), run_time=0.5)
        self.at("break at the gap")
        stop = barred_arrow([nb.p(3.3)[0], BOTC + 0.0, 0], [nb.p(2.0)[0], BOTC + 0.0, 0])
        self.play(Create(stop), run_time=0.6)
        self.at("a carried complex")
        x_in, x_out, x_end = nt.p(EDGES[2])[0], nt.p(EDGES[1])[0], nt.p(nt.park)[0]
        t1 = max(0.4, self.t_of("pass through") - 0.2 - self.elapsed())
        t2 = max(0.4, self.t_of("signal again") - 0.2 - self.elapsed() - t1)
        glide(self, ev, orig, x_in, t1)
        glide(self, ev, orig, x_out, t2, dim=0.18)
        glide(self, ev, orig, x_end, 1.0)
        badge = nuc_badge(nt.nuc)
        self.play(ev[0].animate.set_stroke(TEAL, 5).set_fill(TEAL, 0.5), Flash(ev[0], color=TEAL, flash_radius=0.8),
                  lit_anim(nt.nuc), FadeIn(badge, scale=0.5), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
# S21  the result
# ---------------------------------------------------------------------------------------------
S21_KW = dict(tube=1.9, body_r=1.4, nuc_r=0.65, nuc_dx=-0.2, er=0.5)


def inset_parts():
    box = RoundedRectangle(corner_radius=0.2, width=12.0, height=2.15, stroke_color=GREY, stroke_width=2).move_to([0, -2.68, 0])
    box.set_stroke(opacity=0.7)
    cap = tag("labelled endosomes moving back along an axon", TEXT, 24).move_to([0, -1.9, 0])
    cred = tag("Heerssen and colleagues, 2004; Cui and colleagues, 2007", LIGHT, 22).move_to([0, -3.45, 0])
    tube = RoundedRectangle(corner_radius=0.3, width=8.4, height=0.6, stroke_color=GREY, stroke_width=3, fill_color=SOLID,
                            fill_opacity=1).move_to([0, -2.5, 0])
    eps = VGroup(*[endo([x, -2.5, 0], 0.22) for x in (-2.8, -0.9, 1.0, 2.9)])
    arr = Arrow([3.2, -3.0, 0], [-3.2, -3.0, 0], buff=0, color=TEAL, stroke_width=4, tip_length=0.2)
    lt = tag("tip", TEXT, 26, weight=BOLD).move_to([5.2, -2.5, 0])
    lc = tag("cell body", TEXT, 26, weight=BOLD).move_to([-5.15, -2.5, 0])
    return VGroup(box, cap, cred, tube, eps, arr, lt, lc)


def headline(dy):
    h1 = tag("Evidence against a TrkA-kinase relay,", TEXT, 28, weight=BOLD).move_to([0.5, -0.05 + dy, 0])
    h2 = tag("supports a courier", TEAL, 30, weight=BOLD).move_to([0.5, -0.5 + dy, 0])
    h3 = tag("though not against every kind of relay", LIGHT, 24).move_to([0.5, -0.92 + dy, 0])
    return VGroup(h1, h2, h3)


S21_TOP = 1.7


def s21_base(cy):
    n = Neuron(cy=cy, **S21_KW)
    segs = segments(n)
    grey_out(segs[1])
    rec, d = tip_pair(n, 1.3)
    br, l1, _ = inhibitor_marks_s21(n)
    return n, segs, VGroup(rec, d), br, l1


def inhibitor_marks_s21(n):
    x0, x1 = n.p(EDGES[1] - 0.05)[0], n.p(EDGES[2] + 0.05)[0]
    y = n.cy - HALF - 0.1
    br = VGroup(Line([x0, y, 0], [x1, y, 0], color=RED, stroke_width=4),
                Line([x0, y, 0], [x0, y + 0.15, 0], color=RED, stroke_width=4),
                Line([x1, y, 0], [x1, y + 0.15, 0], color=RED, stroke_width=4))
    mx = (x0 + x1) / 2
    l1 = tag("TrkA kinase inhibitor, this stretch only", RED, 24).move_to([mx, y - 0.3, 0])
    return br, l1, None


def state_s21(sc):
    n, segs, tipg, br, l1 = s21_base(S21_TOP)
    n.cell.set_stroke(GREEN, 5)
    lit(n.nuc)
    ev = endo(n.p(n.park, 0), 0.5)
    ev[0].set_stroke(TEAL, 5).set_fill(TEAL, 0.5)
    badge = nuc_badge(n.nuc)
    sv = tag("neuron survives", GREEN, 30, weight=BOLD).move_to([n.p(-5.0)[0], S21_TOP + 1.4 + 0.4, 0])
    ngf = dot(n.p(TIP - 0.45, 0), YELLOW, 0.17)
    chip_ = chip("NGF taken in (internalized)", YELLOW, 24, pad=0.14).move_to([4.15, S21_TOP + HALF + 0.55, 0])
    hl = headline(0.0)
    ins = inset_parts()
    sc.add(n.cell, n.nuc, segs, tipg, br, l1, ev, badge, sv, chip_, hl, ins)
    return n


class S21Result(SpokenScene):
    def construct(self):
        dy = -0.9
        n, segs, tipg, br, l1 = s21_base(S21_TOP + dy)
        ev = endo(n.p(TIP - 1.1, 0), 0.5)
        orig = ev.copy()
        self.add(n.cell, n.nuc, segs, tipg, br, l1, ev)
        self.at("signal still reached")
        t_total = max(2.0, self.t_of("neuron survived") - self.elapsed() - 0.1)
        x_in, x_out, x_end = n.p(EDGES[2])[0], n.p(EDGES[1])[0], n.p(n.park)[0]
        span = ev.get_center()[0] - x_end
        t1 = t_total * (ev.get_center()[0] - x_in) / span
        t2 = t_total * (x_in - x_out) / span
        glide(self, ev, orig, x_in, t1)
        glide(self, ev, orig, x_out, t2, dim=0.18)
        glide(self, ev, orig, x_end, t_total - t1 - t2)
        self.at("neuron survived")
        badge = nuc_badge(n.nuc)
        sv = tag("neuron survives", GREEN, 30, weight=BOLD).move_to([n.p(-5.0)[0], S21_TOP + dy + 1.4 + 0.4, 0])
        self.play(n.cell.animate.set_stroke(GREEN, 5), lit_anim(n.nuc), FadeIn(badge, scale=0.5),
                  ev[0].animate.set_stroke(TEAL, 5).set_fill(TEAL, 0.5), FadeIn(sv), run_time=0.7)
        hl = headline(dy)
        self.play(FadeIn(hl[0]), run_time=0.4)
        self.play(FadeIn(hl[1]), FadeIn(hl[2]), run_time=0.5)
        main = VGroup(n.cell, n.nuc, segs, tipg, br, l1, ev, badge, sv, hl)
        self.at("NGF also had")
        ins = inset_parts()
        self.play(main.animate.shift(UP * -dy), FadeIn(ins), run_time=0.9)
        self.at("taken into the cell")
        ngf = dot(n.p(TIP + 0.42, 0) + UP * -dy, YELLOW, 0.17)
        chip_ = chip("NGF taken in (internalized)", YELLOW, 24, pad=0.14).move_to([4.15, S21_TOP + HALF + 0.55, 0])
        self.play(FadeIn(chip_, shift=DOWN * 0.1), tipg[1].animate.shift(LEFT * 0.55), run_time=0.7)
        self.play(Indicate(tipg[1], color=YELLOW, scale_factor=1.8), run_time=0.6)
        self.finish()


class S22Beat(NarratedScene):
    def construct(self):
        n = state_s21(self)
        self.finish()


# ---------------------------------------------------------------------------------------------
# S23 / S24  two results keep the question open
# ---------------------------------------------------------------------------------------------
def progress(active):
    out = VGroup()
    for i, x in enumerate((-6.3, -5.5), 1):
        c = Circle(radius=0.28, stroke_color=TEXT if i == active else GREY, stroke_width=3,
                   fill_color=TEXT if i == active else BG, fill_opacity=1 if i == active else 0)
        t = T(str(i), 26, BG if i == active else GREY, weight=BOLD).move_to(c)
        out.add(VGroup(c, t).move_to([x, 3.4, 0]))
    return out


class S23Open(SpokenScene):
    def construct(self):
        prog = progress(1)
        n = Neuron(cy=-0.15, tube=2.6, body_r=1.85, nuc_r=0.7, nuc_dx=-0.3, er=0.4)
        # the whole axon, 1 mm, drawn with a length bar under it from the tip to the cell body
        x_t, x_s = n.p(TIP)[0], n.p(-5.0 + n.body_r)[0]
        ybar = -3.0
        bar = DoubleArrow([x_s, ybar, 0], [x_t, ybar, 0], buff=0, color=TEXT, stroke_width=4, tip_length=0.2)
        bl = tag("axon: about 1 mm", TEXT, 30, weight=BOLD).move_to([(x_s + x_t) / 2, ybar - 0.5, 0])
        self.play(FadeIn(prog, shift=DOWN * 0.1), Create(n.cell), FadeIn(n.nuc), run_time=0.7)
        self.play(Create(bar), FadeIn(bl), run_time=0.4)
        self.at("question open")
        tipd = VGroup(*[dot(n.p(TIP + 0.4, y), YELLOW, 0.17) for y in (-0.5, 0.5)])
        zero = tag("0 min", TEXT, 40, weight=BOLD).move_to([5.45, 3.2, 0])
        zl = tag("NGF reaches\nthe axons", YELLOW, 28, weight=BOLD, line_spacing=0.8).move_to([5.45, 2.35, 0])
        self.play(FadeIn(tipd, scale=0.6), FadeIn(zero, shift=DOWN * 0.1), FadeIn(zl), run_time=0.7)
        self.at("in the cell bodies")
        l1 = tag("TrkA phosphorylated\nin cell bodies", TRKA, 30, weight=BOLD, line_spacing=0.8).move_to([-3.45, 2.6, 0])
        self.play(FadeIn(l1, shift=DOWN * 0.1), run_time=0.6)
        self.at("phosphorylated")
        pb = nuc_badge(n.nuc)
        self.play(lit_anim(n.nuc), FadeIn(pb, scale=0.5), run_time=0.5)
        self.at("within a minute")
        wm = tag("1 min", TEXT, 36, weight=BOLD).next_to(l1, RIGHT, buff=0.45)
        time_bracket = Brace(VGroup(l1, wm), DOWN, buff=0.12, color=TEXT)
        self.play(FadeIn(wm, scale=0.8), Create(time_bracket), run_time=0.5)
        self.at("far faster")
        # 60 micrometres of a 1 mm axon is 6 percent of its length (axon drawn tip to cell body)
        length = x_t - x_s
        stretch = length * 0.06
        yc = n.cy
        path = Line([x_t - 0.4, yc, 0], [x_t - 0.4 - stretch, yc, 0], color=TEAL, stroke_width=14)
        e = endo([x_t - 0.4, yc, 0], 0.48)
        # Keep the true 6% distance on the axon and magnify that stretch below it.
        detail_y = -2.25
        zoom = 5.0
        detail_start = np.array([4.6, detail_y, 0])
        detail_path = Line(detail_start, detail_start + LEFT * stretch * zoom, color=TEAL, stroke_width=10)
        detail_endo = endo(detail_start, 0.5)
        pl = tag("endosome: about 60 micrometres\nin 1 min", TEAL, 26, weight=BOLD, line_spacing=0.8).move_to([-1.6, detail_y - 0.15, 0])
        detail_label = tag("5× detail", LIGHT, 22).move_to([5.7, detail_y, 0])
        lead = DashedLine([x_t - 0.4 - stretch / 2, yc - 0.5, 0],
                          [4.6 - stretch * zoom / 2, detail_y + 0.55, 0], color=TEAL, stroke_width=3)
        self.play(FadeIn(e, scale=0.5), Create(path), FadeIn(pl), Create(lead),
                  Create(detail_path), FadeIn(detail_endo), FadeIn(detail_label), run_time=0.8)
        self.at("endosomes move")
        self.play(e.animate.shift(LEFT * stretch), detail_endo.animate.shift(LEFT * stretch * zoom),
                  run_time=1.0, rate_func=linear)
        self.finish()


class S24Beads(SpokenScene):
    def construct(self):
        n = Neuron(cy=0.15, **SINGLE_POLISH)
        prog = progress(2)
        self.add(prog)
        self.play(Create(n.cell), FadeIn(n.nuc), run_time=0.7)
        self.at("fixed")
        beads = VGroup()
        c = np.array([n.p(TIP)[0] - n.tube / 2, n.cy, 0])        # centre of the rounded axon tip
        for ang in (-40, 0, 40):
            a = np.deg2rad(ang)
            pos = c + (n.tube / 2 + 0.5) * np.array([np.cos(a), np.sin(a), 0])
            b = Circle(radius=0.5, stroke_color=TEXT, stroke_width=3, fill_color=GREY, fill_opacity=0.5).move_to(pos)
            beads.add(VGroup(b, dot(pos + np.array([-0.2, 0.12, 0]), YELLOW, 0.12), dot(pos + np.array([0.14, -0.18, 0]), YELLOW, 0.12)))
        bl = tag("NGF fixed to beads", YELLOW, 30, weight=BOLD).move_to([4.2, 2.55, 0])
        self.play(FadeIn(beads, scale=0.6, lag_ratio=0.2), FadeIn(bl), run_time=0.7)
        self.at("supported survival", lead=0.0)
        sv = tag("neurons survive", GREEN, 30, weight=BOLD).move_to([-2.0, 2.95, 0])
        self.play(n.cell.animate.set_stroke(GREEN, 5), n.nuc.animate.set_fill(PURPLE, 0.95).set_stroke(GREEN, 4), FadeIn(sv),
                  run_time=0.7)
        self.at("little or no")
        lt = tag("little or no NGF transport detected", TEXT, 36, weight=BOLD).move_to([0.9, -2.7, 0])
        self.play(FadeIn(lt, shift=UP * 0.1), run_time=0.7)
        self.at("NGF transport")
        path = DashedLine(n.p(TIP, 0), n.p(-3.0, 0), color=TEAL, stroke_width=8, dash_length=0.26)
        path.add_tip(tip_length=0.34)
        pl = tag("dashed: what the assay could miss", TEAL, 28, weight=BOLD).move_to([0.9, -3.4, 0])
        self.play(Create(path), FadeIn(pl), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
# S25  takeaway
# ---------------------------------------------------------------------------------------------
class S25Take(SpokenScene):
    def construct(self):
        head = tag("Takeaway", LIGHT, 34, weight=BOLD).move_to([0, 3.3, 0])
        self.play(FadeIn(head), run_time=0.5)
        self.at("for survival")
        ev = endo([-3.0, 0.2, 0], 2.4 * 0.45)
        ev[0].set_stroke(TEAL, 6)
        c = T("Courier", 76, TEAL, font=TITLE_FONT).move_to([0.2, 0.55, 0]).align_to([-0.9, 0, 0], LEFT)
        s_ = tag("favoured, for survival", GREEN, 44).next_to(c, DOWN, buff=0.25).align_to(c, LEFT)
        top = VGroup(ev, c, s_)
        self.play(FadeIn(ev, scale=0.6), run_time=0.7)
        self.at("favors a courier")
        self.play(FadeIn(c, shift=RIGHT * 0.2), FadeIn(s_, shift=RIGHT * 0.2), run_time=0.9)
        self.at("faster signal")
        circ = DashedVMobject(Circle(radius=1.2, stroke_color=GREY, stroke_width=5), num_dashes=28).move_to([-3.0, -1.6, 0])
        q = qmark([-3.0, -1.6, 0], 90, GREY)
        f = T("A faster signal", 76, LIGHT, font=TITLE_FONT).move_to([0.2, -1.25, 0]).align_to([-0.9, 0, 0], LEFT)
        self.play(top.animate.shift(UP * 1.45), FadeIn(circ), FadeIn(q, scale=0.5), FadeIn(f, shift=RIGHT * 0.2),
                  FadeOut(head), run_time=0.9)
        self.at("still open")
        o = tag("open", TEXT, 44).next_to(f, DOWN, buff=0.25).align_to(f, LEFT)
        self.play(FadeIn(o, shift=RIGHT * 0.2), run_time=0.6)
        self.finish()


class S26End(EndCard):
    LINE = "For survival, the evidence favours a courier.\nA faster signal is open."
