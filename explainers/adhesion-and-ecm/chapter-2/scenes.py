"""Links That Feel the Pull - adhesion and ECM, chapter 2.

Same colour map as chapter 1 (YELLOW calcium; BLUE cadherin; PURPLE integrin; TEAL adaptors;
GREEN actin; PINK keratin; ORANGE matrix; GOLD pull; GREY cell structure), plus CORAL = myosin II.
All diagrams are schematic labelled cartoons, never molecular structures.
"""

import numpy as np
from bp_style import *  # noqa: F401,F403


PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E87DB0"


def label(text, p, color=TEXT, size=28):
    return T(text, size=size, color=color).move_to(p)


def cell(cx, cy=0.55, w=2.7, h=3.75):
    body = RoundedRectangle(corner_radius=0.35, width=w, height=h,
                            stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.14).move_to([cx, cy, 0])
    nucleus = Ellipse(width=0.82, height=1.0, stroke_color=GREY, stroke_width=2,
                      fill_color=GREY, fill_opacity=0.28).move_to([cx, cy + 0.15, 0])
    return VGroup(body, nucleus)


def rope(y, amp=0.18, x0=-6.45, x1=6.45, phase=0.0, color=ORANGE, width=5):
    xs = np.linspace(x0, x1, 80)
    pts = [[x, y + amp * np.sin(1.55 * x + phase), 0] for x in xs]
    return VMobject(color=color, stroke_width=width).set_points_smoothly(pts)


def drifting_dots(points, color=YELLOW, radius=0.075, vx=0.07, vy=0.035,
                  bounds=(-6.5, 6.5, -3.5, 3.5)):
    """Small, continually moving particles for narrated fluid/gel holds."""
    group = VGroup(*[Dot(p, radius=radius, color=color) for p in points])
    xmin, xmax, ymin, ymax = bounds
    for i, dot in enumerate(group):
        dot.velocity = np.array([vx * (1 if i % 2 else -1), vy * (1 if i % 3 else -1), 0.0])

        def drift(m, dt, xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax):
            m.shift(m.velocity * dt)
            x, y = m.get_x(), m.get_y()
            if x < xmin: m.set_x(xmax)
            if x > xmax: m.set_x(xmin)
            if y < ymin: m.set_y(ymax)
            if y > ymax: m.set_y(ymin)
        dot.add_updater(drift)
    return group


def world(separated=False, with_label=True):
    shift = 0.38 if separated else 0.0
    xs = [-4.5 - shift, -1.5 - shift / 3, 1.5 + shift / 3, 4.5 + shift]
    cells = VGroup(*[cell(x, 0.55, 2.62 if not separated else 2.32,
                              3.75 if not separated else 3.32) for x in xs])
    basement = RoundedRectangle(corner_radius=0.08, width=12.9, height=0.26,
                                stroke_color=ORANGE, stroke_width=2.5,
                                fill_color=ORANGE, fill_opacity=0.28).move_to([0, -1.5, 0])
    ropes = VGroup(*[rope(y, 0.16, phase=i * 0.7, width=4)
                     for i, y in enumerate((-2.05, -2.55, -3.05, -3.45))])
    haze = Rectangle(width=13.0, height=2.15, stroke_width=0,
                     fill_color=ORANGE, fill_opacity=0.10).move_to([0, -2.55, 0])
    pts = [(-6 + i * 0.92, 2.72 + 0.28 * ((i * 7) % 3), 0) for i in range(14)]
    calcium = drifting_dots(pts, bounds=(-6.35, 6.35, 2.62, 3.55))
    lab = label("a sheet of epithelial cells", [-4.45, 3.38, 0], TEXT, 28)
    return VGroup(haze, ropes, basement, cells, calcium, *( [lab] if with_label else [] ))


def membrane(x, height=6.5):
    return RoundedRectangle(corner_radius=0.08, width=0.24, height=height,
                            stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.45).move_to([x, 0, 0])


def cad_arm(start, end, sag=0.0):
    p0, p1 = np.array(start, float), np.array(end, float)
    pts = []
    for i in range(5):
        u = i / 4
        p = p0 * (1-u) + p1 * u
        p[1] -= sag * np.sin(np.pi * u)
        pts.append(p)
    lines = VGroup(*[Line(pts[i], pts[i+1], color=BLUE, stroke_width=5) for i in range(4)])
    beads = VGroup(*[RoundedRectangle(corner_radius=0.05, width=0.25, height=0.25,
                                      stroke_color=BLUE, stroke_width=2,
                                      fill_color=BLUE, fill_opacity=0.5).move_to(p) for p in pts])
    return VGroup(lines, beads)


def calcium_joints(start, end):
    p0, p1 = np.array(start, float), np.array(end, float)
    return VGroup(*[Dot(p0 * (1-u) + p1 * u, radius=0.075, color=YELLOW)
                    for u in (0.125, 0.375, 0.625, 0.875)])


def arm_field(sag=0.0):
    arms, ca = VGroup(), VGroup()
    for y in (-1.65, 0, 1.65):
        arms.add(cad_arm([-1.9, y, 0], [-0.08, y, 0], sag),
                 cad_arm([1.9, y, 0], [0.08, y, 0], sag))
        ca.add(calcium_joints([-1.9, y, 0], [-0.08, y, 0]),
               calcium_joints([1.9, y, 0], [0.08, y, 0]))
    return arms, ca


def beaded_cable(a, b, color=GREEN, count=13):
    a, b = np.array(a, float), np.array(b, float)
    line = Line(a, b, color=color, stroke_width=5)
    beads = VGroup(*[Dot(a * (1-u) + b * u, radius=0.085, color=color)
                     for u in np.linspace(0, 1, count)])
    return VGroup(line, beads)


def adaptor(text, x, y=0):
    return chip(text, TEAL, size=28, pad=0.16).move_to([x, y, 0])


def chain_parts(y=0.35, show_labels=False):
    """Same landmarks for scenes 3–8: membrane x=±1.05, grip at x=0."""
    left_mem, right_mem = membrane(-1.05, 4.5), membrane(1.05, 4.5)
    # Keep the chain in one recognisable world: these broad, quiet cell interiors
    # make the intracellular/extracellular distinction readable without competing
    # with the coloured links.
    cell_fields = VGroup(
        Rectangle(width=5.25, height=5.55, stroke_width=0,
                  fill_color=GREY, fill_opacity=0.20).move_to([-3.68, 0, 0]),
        Rectangle(width=5.25, height=5.55, stroke_width=0,
                  fill_color=GREY, fill_opacity=0.20).move_to([3.68, 0, 0]),
    ).set_z_index(-2)
    larm = cad_arm([-1.05, y, 0], [-0.08, y, 0])
    rarm = cad_arm([1.05, y, 0], [0.08, y, 0])
    ca = VGroup(calcium_joints([-1.05, y, 0], [-0.08, y, 0]),
                calcium_joints([1.05, y, 0], [0.08, y, 0]))
    tails = VGroup(Line([-1.05, y, 0], [-1.55, y, 0], color=BLUE, stroke_width=5),
                   Line([1.05, y, 0], [1.55, y, 0], color=BLUE, stroke_width=5))
    lb, la = adaptor("β-catenin", -2.55, y), adaptor("α-catenin", -4.45, y)
    rb, ra = adaptor("β-catenin", 2.55, y), adaptor("α-catenin", 4.45, y)
    connectors = VGroup(Line([-1.55,y,0], lb.get_right(), color=TEAL, stroke_width=4),
                        Line(lb.get_left(), la.get_right(), color=TEAL, stroke_width=4),
                        Line([1.55,y,0], rb.get_left(), color=TEAL, stroke_width=4),
                        Line(rb.get_right(), ra.get_left(), color=TEAL, stroke_width=4))
    lcable = beaded_cable([-6.35,y,0], la.get_left(), GREEN, 12)
    rcable = beaded_cable(ra.get_right(), [6.35,y,0], GREEN, 12)
    labs = VGroup()
    if show_labels:
        labs.add(label("actin cable", [-5.15, 1.1, 0], GREEN),
                 label("cadherin", [0, 1.1, 0], BLUE))
    return dict(cell_fields=cell_fields, membranes=VGroup(left_mem,right_mem), arms=VGroup(larm,rarm), calcium=ca,
                tails=tails, adaptors=VGroup(lb,la,rb,ra), connectors=connectors,
                cables=VGroup(lcable,rcable), labels=labs)


def chain_group(d):
    return VGroup(d["cell_fields"], d["membranes"], d["arms"], d["calcium"], d["tails"],
                  d["adaptors"], d["connectors"], d["cables"], d["labels"])


def force_arrows(horizontal=True):
    if horizontal:
        return VGroup(Arrow([-5.55,2.25,0],[-6.55,2.25,0],buff=0,color=GOLD,stroke_width=8),
                      Arrow([5.55,2.25,0],[6.55,2.25,0],buff=0,color=GOLD,stroke_width=8))
    return VGroup(Arrow([0,3.1,0],[0,2.05,0],buff=0,color=GOLD,stroke_width=8),
                  Arrow([0,-3.1,0],[0,-2.05,0],buff=0,color=GOLD,stroke_width=8))


def tags(y=-1.25):
    texts = ("1 partner outside", "2 receptor", "3 adaptors", "4 cable")
    positions = ((2.2, y), (-.7, y), (-2.9, y), (-5.2, y))
    return VGroup(*[chip(t, TEXT, size=28, pad=0.13, fill_opacity=0.08).move_to([x, yy, 0])
                    for t, (x, yy) in zip(texts, positions)])


def integrin_world():
    membrane_bar = RoundedRectangle(corner_radius=0.08, width=12.8, height=0.28,
                                    stroke_color=GREY, stroke_width=3,
                                    fill_color=GREY, fill_opacity=0.42).move_to([0,0,0])
    haze = Rectangle(width=12.8, height=3.4, stroke_width=0, fill_color=ORANGE,
                     fill_opacity=0.13).move_to([0,-1.85,0])
    ropes = VGroup(*[rope(y, 0.14, phase=i*.8, width=4)
                     for i,y in enumerate((-1.35,-2.05,-2.75,-3.35))])
    alpha = RoundedRectangle(corner_radius=.22,width=.68,height=1.85,stroke_color=PURPLE,
                             stroke_width=4,fill_color=PURPLE,fill_opacity=.30).move_to([-.38,0,0])
    beta = alpha.copy().move_to([.38,0,0])
    al = label("α", alpha, TEXT, 30); bl = label("β", beta, TEXT, 30)
    strand = rope(-2.0, .22, -4.6, 4.6, .7, ORANGE, 5)
    rgd = chip("RGD", ORANGE, size=28, pad=.14).move_to([0,-1.25,0])
    return dict(membrane=membrane_bar,haze=haze,ropes=ropes,
                integrin=VGroup(alpha,beta,al,bl),strand=strand,rgd=rgd)




# =====================================================================================
# CHAPTER 2 additions. New colour: CORAL = myosin II motor. Everything else as chapter 1.
# =====================================================================================
CORAL = "#FF6F61"
RY = 0.2          # y of the talin row
TX = 4.2          # x of the integrin / talin chain in the cell-interior view
MARK = (3, 7, 10)  # the three representative blocks that hide a vinculin site


def backing(m, pad=0.18, op=0.82):
    return Rectangle(width=m.width + 2 * pad, height=m.height + 2 * pad, stroke_width=0,
                     fill_color=BG, fill_opacity=op).move_to(m)


def wander(m, x0, x1, y0, y1, vx, vy):
    """Slow drifting inside a box, bouncing off its walls."""
    m.v = np.array([vx, vy, 0.0])

    def u(mm, dt):
        mm.shift(mm.v * dt)
        p = mm.get_center()
        if p[0] < x0 or p[0] > x1:
            mm.v[0] *= -1
            mm.shift(RIGHT * (np.clip(p[0], x0, x1) - p[0]))
        if p[1] < y0 or p[1] > y1:
            mm.v[1] *= -1
            mm.shift(UP * (np.clip(p[1], y0, y1) - p[1]))
    m.add_updater(u)
    return m


def wobble(m, amp=0.1, sp=1.0, ph=0.0):
    """Small relative back-and-forth motion (safe under scaling and shifting)."""
    m._t = 0.0
    m._o = np.zeros(3)

    def u(mm, dt):
        mm._t += dt
        o = np.array([amp * np.sin(sp * mm._t + ph), amp * np.cos(0.8 * sp * mm._t + ph), 0.0])
        mm.shift(o - mm._o)
        mm._o = o
    m.add_updater(u)
    return m


def motes(n, x0, x1, y0, y1, color=TEAL, seed=1, op=0.35):
    rng = np.random.RandomState(seed)
    g = VGroup()
    for _ in range(n):
        d = Dot([rng.uniform(x0, x1), rng.uniform(y0, y1), 0], radius=rng.uniform(0.03, 0.06), color=color)
        d.set_opacity(op)
        wander(d, x0, x1, y0, y1, rng.uniform(-0.3, 0.3), rng.uniform(-0.25, 0.25))
        g.add(d)
    return g


def beads_on(line, n=8, speed=0.06, color=GREEN, r=0.085):
    """Dots riding along a line (relative to it, so they follow any scaling). speed = fraction per second."""
    g = VGroup(*[Dot(radius=r, color=color) for _ in range(n)])
    g.u = [i / n for i in range(n)]
    g.speed = ValueTracker(speed)

    def u(m, dt):
        a, b = line.get_start(), line.get_end()
        for i, d in enumerate(m):
            m.u[i] = (m.u[i] + m.speed.get_value() * dt) % 1
            d.move_to(a + (b - a) * m.u[i])
    g.add_updater(u)
    u(g, 0)
    return g


def jig(m, y0, amp=0.05, sp=2.4, ph=0.0):
    m._t = 0.0
    m.jamp = amp

    def u(mm, dt):
        mm._t += dt
        mm.set_y(y0 + mm.jamp * np.sin(sp * mm._t + ph))
    m.add_updater(u)
    return m


def bob(m, amp=0.12, sp=1.5):
    m._t = 0.0
    m._o = 0.0
    m.bamp = amp

    def u(mm, dt):
        mm._t += dt
        o = mm.bamp * np.sin(sp * mm._t)
        mm.shift(RIGHT * (o - mm._o))
        mm._o = o
    m.add_updater(u)
    return m


class IW:
    """The cell-interior view used through the film: membrane across the middle, matrix below,
    integrin chain at x = TX (purple, teal talin bar, orange fibronectin), two green actin cables."""
    pass


def int_world():
    w = IW()
    w.field = Rectangle(width=14.4, height=6.3, stroke_width=0, fill_color=GREY, fill_opacity=0.22).move_to([0, 0.95, 0]).set_z_index(-3)
    w.haze = Rectangle(width=14.4, height=1.7, stroke_width=0, fill_color=ORANGE, fill_opacity=0.2).move_to([0, -3.15, 0]).set_z_index(-3)
    w.mem = RoundedRectangle(corner_radius=0.08, width=14.2, height=0.28, stroke_color=GREY, stroke_width=3,
                             fill_color=GREY, fill_opacity=0.45).move_to([0, -2.2, 0])
    w.ropes = VGroup(rope(-2.75, 0.14, -7.1, 7.1, 0.3, ORANGE, 3), rope(-3.4, 0.14, -7.1, 7.1, 1.1, ORANGE, 3))
    w.strand = rope(-3.3, 0.2, -7.1, 7.1, 0.7, ORANGE, 5)
    w.link = Line([TX, -2.7, 0], [TX, -3.22, 0], color=ORANGE, stroke_width=5)
    w.integ = VGroup(*[RoundedRectangle(corner_radius=0.1, width=0.34, height=1.0, stroke_color=PURPLE, stroke_width=4,
                                        fill_color=PURPLE, fill_opacity=0.45).move_to([TX + dx, -2.2, 0]) for dx in (-0.2, 0.2)])
    w.talin = RoundedRectangle(corner_radius=0.1, width=0.28, height=2.8, stroke_color=TEAL, stroke_width=3,
                               fill_color=TEAL, fill_opacity=0.45).move_to([TX, -0.3, 0])
    w.cab_up = Line([-2.2, 1.3, 0], [TX, 1.3, 0], color=GREEN, stroke_width=6)
    w.cab_lo = Line([-6.4, 0.3, 0], [1.6, 0.3, 0], color=GREEN, stroke_width=6)
    w.net = VGroup(Line([-6.4, 0.3, 0], [-7.0, 1.1, 0]), Line([-6.4, 0.3, 0], [-7.0, -0.5, 0]),
                   Line([-5.5, 0.3, 0], [-6.2, -0.7, 0])).set_stroke(GREEN, 3, opacity=0.8)
    w.arrows = VGroup(Triangle(color=GREEN, fill_opacity=1).scale(0.16).rotate(-PI / 2).move_to([2.3, 1.3, 0]),
                      Triangle(color=GREEN, fill_opacity=1).scale(0.16).rotate(PI / 2).move_to([-3.4, 0.3, 0]))
    w.beads_up = beads_on(w.cab_up, 9, -0.06)
    w.beads_lo = beads_on(w.cab_lo, 11, 0.06)
    w.parts = [w.field, w.haze, w.ropes, w.strand, w.link, w.mem, w.integ, w.talin, w.cab_up, w.cab_lo,
               w.net, w.arrows, w.beads_up, w.beads_lo]
    return w


def make_myo():
    bar = RoundedRectangle(corner_radius=0.11, width=2.2, height=0.22, stroke_color=CORAL, stroke_width=3,
                           fill_color=CORAL, fill_opacity=0.55).move_to([-0.3, 0.8, 0])
    h1, h2 = Dot([-1.4, 0.8, 0], radius=0.2, color=CORAL), Dot([0.8, 0.8, 0], radius=0.2, color=CORAL)
    s1 = Line([-1.4, 0.8, 0], [-1.4, 0.3, 0], color=CORAL, stroke_width=5)
    s2 = Line([0.8, 0.8, 0], [0.8, 1.3, 0], color=CORAL, stroke_width=5)
    g = VGroup(s1, s2, bar, h1, h2)
    g.heads = VGroup(h1, h2)
    bob(g, 0.14, 1.6)
    return g


def add_vinc():
    """Two activated vinculin blocks beside the stretched talin, each with a tie to the upper cable."""
    b1 = RoundedRectangle(corner_radius=0.08, width=0.6, height=0.36, stroke_color=TEAL, stroke_width=3,
                          fill_color=TEAL, fill_opacity=0.5).move_to([3.55, 0.5, 0])
    b2 = b1.copy().move_to([3.55, -0.55, 0])
    d1, d2 = Dot([TX - 0.14, 0.5, 0], radius=0.07, color=TEXT), Dot([TX - 0.14, -0.55, 0], radius=0.07, color=TEXT)
    t1 = Line([3.55, 0.68, 0], [3.55, 1.3, 0], color=TEAL, stroke_width=5)
    t2 = VMobject(color=TEAL, stroke_width=5).set_points_as_corners([[3.25, -0.55, 0], [2.95, -0.55, 0], [2.95, 1.3, 0]])
    return dict(blocks=VGroup(b1, b2), dots=VGroup(d1, d2), ties=VGroup(t1, t2))


def gold_blob(r=0.14):
    return VGroup(Dot(radius=r * 2.4, color=GOLD).set_opacity(0.28), Dot(radius=r, color=GOLD))


def path_of(pts):
    return VMobject().set_points_as_corners([np.array([p[0], p[1], 0.0]) for p in pts])


# ---------- the talin row ----------
def rod_xs(stretch=False):
    pitch = 0.792 if stretch else 0.72
    return [-4.32 + pitch * i for i in range(13)]


def make_rod(stretch=False, mark=True, jiggle=True, amp=0.04):
    xs = rod_xs(stretch)
    line = Line([-4.6, RY, 0], [xs[-1] + 0.3, RY, 0], color=TEAL, stroke_width=4)
    blocks = []
    for i, x in enumerate(xs):
        b = RoundedRectangle(corner_radius=0.12, width=0.56, height=1.3, stroke_color=TEAL, stroke_width=3,
                             fill_color=TEAL, fill_opacity=0.32).move_to([x, RY, 0])
        if mark and i in MARK:
            b.set_stroke(TEXT, 3, opacity=0.85)
        if jiggle:
            jig(b, RY, amp, 2.4, i * 0.7)
        blocks.append(b)
    return line, blocks


def latch_icon(open_=True):
    """A latch: a bar hinged at its left end that either lies over a white site (closed) or swings up (open).
    The bar is redrawn from the dot's position every frame, so it travels with whatever carries the dot."""
    dot = Dot(ORIGIN, radius=0.1, color=TEXT)
    ang = ValueTracker(70 * DEGREES if open_ else 0.0)
    bar = RoundedRectangle(corner_radius=0.06, width=0.7, height=0.2, stroke_color=TEXT, stroke_width=2,
                           fill_color=GREY, fill_opacity=1)

    def u(m):
        c = dot.get_center()
        op = dot.get_fill_opacity()
        m.become(RoundedRectangle(corner_radius=0.06, width=0.7, height=0.2, stroke_color=TEXT, stroke_width=2,
                                  fill_color=GREY, fill_opacity=op).move_to(c).rotate(ang.get_value(), about_point=c + LEFT * 0.35))
        m.set_stroke(TEXT, 2, opacity=op)
    bar.add_updater(u)
    u(bar)
    g = VGroup(dot, bar)
    g.dot, g.bar, g.ang = dot, bar, ang
    return g


def ai_chip(text, size=26, open_=True):
    c = chip(text, TEAL, size=size, pad=0.14)
    la = latch_icon(open_).next_to(c, RIGHT, buff=0.55)
    g = VGroup(c, la)
    g.c, g.la = c, la
    return g


def latch_close(g):
    return g.la.ang.animate.set_value(0.0)


def latch_open(g):
    return g.la.ang.animate.set_value(70 * DEGREES)


# ---------- chapter 1's world, with the chains, for the zoom scenes ----------
WP = np.array([-1.5, -1.4, 0.0])
ZK = 2.0
ZS = np.array([1.5, 0.6, 0.0])
PC = np.array([0.0, -0.8, 0.0])


def build_world(motors=False):
    base = world(False, with_label=False)
    W = VGroup(*base[:4])
    ca = VGroup(*[Dot([-6 + i * 0.92, 2.72 + 0.28 * ((i * 7) % 3), 0], radius=0.075, color=YELLOW) for i in range(14)])
    for i, d in enumerate(ca):
        wobble(d, 0.1, 0.8 + 0.05 * i, i)
    cx = (-4.5, -1.5, 1.5, 4.5)
    blues, cas = VGroup(), VGroup()
    for gx in (-3.0, 0.0, 3.0):
        for y in (1.1, 0.2):
            blues.add(Line([gx - 0.36, y, 0], [gx + 0.36, y, 0], color=BLUE, stroke_width=6))
            cas.add(Dot([gx, y, 0], radius=0.07, color=YELLOW))
    purples = VGroup(*[RoundedRectangle(corner_radius=0.06, width=0.4, height=0.5, stroke_color=PURPLE, stroke_width=3,
                                        fill_color=PURPLE, fill_opacity=0.5).move_to([x, -1.45, 0]) for x in cx])
    pinks = VGroup(*[Line([x - 0.95, -0.5, 0], [x + 0.95, -0.5, 0], color=PINK, stroke_width=5) for x in cx])
    W.add(ca, blues, cas, purples, pinks)
    if motors:
        ms = VGroup(*[RoundedRectangle(corner_radius=0.08, width=0.7, height=0.2, stroke_color=CORAL, stroke_width=2,
                                       fill_color=CORAL, fill_opacity=0.6).move_to([x, -0.1, 0]) for x in cx])
        for i, m in enumerate(ms):
            bob(m, 0.12, 1.4 + 0.1 * i)
        W.add(ms)
        W.motors = ms
    W.A, W.B, W.C = (Dot([0, 0, 0], radius=0.001).set_opacity(0), Dot([1, 0, 0], radius=0.001).set_opacity(0),
                     Dot([0, 1, 0], radius=0.001).set_opacity(0))
    W.add(W.A, W.B, W.C)
    pts = [(-4.5, -.5), (-3, .15), (-1.5, -.5), (-1.5, -1.5), (-1.5, -2.5), (1.5, -2.5), (1.5, -1.5), (1.5, -.5),
           (3, .15), (4.5, -.5), (4.5, -1.5), (4.5, -2.5), (-4.5, -2.5), (-4.5, -1.5)]
    P = [np.array(p, float) for p in pts] + [np.array(pts[0], float)]
    seg = [np.linalg.norm(P[i + 1] - P[i]) for i in range(len(P) - 1)]
    L = sum(seg)
    pg = gold_blob(0.15)
    pg.s = 0.0

    def upd(m, dt):
        m.s = (m.s + dt * L / 9.0) % L
        s = m.s
        for i, sl in enumerate(seg):
            if s <= sl:
                loc = P[i] + (P[i + 1] - P[i]) * (s / sl)
                break
            s -= sl
        A, B, C = W.A.get_center(), W.B.get_center(), W.C.get_center()
        m.move_to(A + loc[0] * (B - A) + loc[1] * (C - A))
    pg.add_updater(upd)
    upd(pg, 0)
    W.add(pg)
    W.pulse = pg
    return W


def zoom_in(W, k=1.0):
    """Put the world in the zoomed state (k=1: first zoom, ends in the title; k=2: title end)."""
    W.scale(ZK, about_point=WP).shift(ZS)
    if k >= 2:
        W.scale(1.4, about_point=PC)
    return W


# =====================================================================================
# Scenes
# =====================================================================================
class S00Link(SpokenScene):
    def construct(self):
        W = build_world()
        self.play(FadeIn(W), run_time=1.0)
        q = T("Can pull change a link?", size=40)
        q.move_to([0, 3.45, 0])
        qg = VGroup(backing(q), q)
        self.at("Can that pull")
        self.play(FadeIn(qg, shift=DOWN * 0.12), run_time=0.6)
        self.at("inside the cell")
        self.play(W.animate.scale(ZK, about_point=WP).shift(ZS), run_time=1.7, rate_func=smooth)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Adhesion and the extracellular matrix"
    TITLE = "Links That Feel the Pull"

    def construct(self):
        W = zoom_in(build_world(), 1)
        q = T("Can pull change a link?", size=40).move_to([0, 3.45, 0])
        qg = VGroup(backing(q), q)
        title = T(self.TITLE, size=56, font=TITLE_FONT)
        fit(title, max_w=11.5)
        rule = Line(LEFT * 1.3, RIGHT * 1.3, color=GOLD, stroke_width=4)
        g = VGroup(title, rule).arrange(DOWN, buff=0.3)
        bk = backing(g, 0.4, 0.55)
        self.add(W, qg)
        self.play(W.animate.scale(1.4, about_point=PC), FadeOut(qg), FadeIn(VGroup(bk, g), shift=UP * 0.12), run_time=1.5)
        self.play(FadeOut(VGroup(bk, g)), run_time=0.35)
        self.finish()


class S02Myosin(SpokenScene):
    def construct(self):
        iw = int_world()
        iw.beads_up.speed.set_value(0)
        iw.beads_lo.speed.set_value(0)
        cyto = motes(10, -6.5, 3.5, -1.8, 3.6, GREY, 3, 0.4)
        self.play(FadeIn(VGroup(*iw.parts)), FadeIn(cyto), run_time=0.8)
        self.at("a motor protein")
        myo = make_myo()
        self.play(GrowFromCenter(myo), iw.beads_up.speed.animate.set_value(-0.07), iw.beads_lo.speed.animate.set_value(0.07), run_time=1.0)
        self.at("myosin 2")
        ml = label("myosin II", [-3.3, 0.8, 0], CORAL, 30)
        mline = Line([-2.3, 0.8, 0], [-1.7, 0.8, 0], color=CORAL, stroke_width=3)
        self.play(FadeIn(ml), Create(mline), run_time=0.6)
        self.at("grips the actin")
        self.play(Indicate(myo.heads, color=CORAL, scale_factor=1.35), run_time=0.9)
        self.at("slides them past")
        self.play(iw.beads_up.speed.animate.set_value(-0.1), iw.beads_lo.speed.animate.set_value(0.1), run_time=1.0)
        self.at("under load")
        a1 = Arrow([1.3, 1.7, 0], [2.9, 1.7, 0], buff=0, color=GOLD, stroke_width=8)
        a2 = Arrow([-0.2, -0.05, 0], [-1.9, -0.05, 0], buff=0, color=GOLD, stroke_width=8)
        pull = label("cell-generated pull", [-3.4, 2.7, 0], GOLD, 30)
        self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(pull), run_time=0.8)
        self.at("That pull reaches")
        blob = gold_blob().move_to([1.0, 1.3, 0])
        self.add(blob)
        self.play(MoveAlongPath(blob, path_of([(1.0, 1.3), (TX, 1.3), (TX, -1.7), (TX, -2.7), (TX, -3.22)])),
                  run_time=1.7, rate_func=linear)
        self.at("down to the matrix")
        self.play(FadeOut(blob), Transform(iw.strand, rope(-3.3, 0.0, -7.1, 7.1, 0.7, ORANGE, 5)), run_time=1.0)
        self.finish()


def rod_scene_base(scene, stretch=False, vinc_chips=False):
    line, blocks = make_rod(stretch)
    scene.add(line, *blocks)
    return line, blocks


def left_chip():
    c = RoundedRectangle(corner_radius=0.1, width=0.5, height=1.5, stroke_color=PURPLE, stroke_width=4,
                         fill_color=PURPLE, fill_opacity=0.45).move_to([-5.55, RY, 0])
    t = Line([-5.3, RY, 0], [-4.62, RY, 0], color=PURPLE, stroke_width=5)
    return VGroup(c, t)


def right_cable():
    ln = Line([4.9, RY, 0], [6.7, RY, 0], color=GREEN, stroke_width=6)
    return VGroup(ln, beads_on(ln, 4, 0.08))


class S03Rod(SpokenScene):
    def construct(self):
        iw = int_world()
        myo = make_myo()
        self.add(*iw.parts, myo)
        others = VGroup(*[p for p in iw.parts if p is not iw.talin], myo)
        bar = RoundedRectangle(corner_radius=0.14, width=9.2, height=1.3, stroke_color=TEAL, stroke_width=3,
                               fill_color=TEAL, fill_opacity=0.32).move_to([0, RY, 0])
        lc, rc = left_chip(), right_cable()
        self.play(FadeOut(others), Transform(iw.talin, bar), FadeIn(lc), FadeIn(rc), run_time=2.2)
        self.add(Rectangle(width=14.4, height=8.2, stroke_width=0, fill_color=GREY, fill_opacity=0.14).set_z_index(-3))
        self.at("adapter")
        lab = label("talin", [0, 2.7, 0], TEAL, 32)
        self.play(FadeIn(lab), run_time=0.5)
        self.at("long rod")
        line, blocks = make_rod(False, mark=False)
        bg = VGroup(*blocks)
        self.play(ReplacementTransform(iw.talin, bg), FadeIn(line), run_time=1.6)
        schem = label("schematic", [5.7, -3.5, 0], GREY, 24)
        self.add(schem)
        self.at("13 small bundles")
        n = ValueTracker(0)
        counter = always_redraw(lambda: M(f"{int(np.clip(np.ceil(n.get_value()), 1, 13))} / 13", size=44).move_to([0, -1.7, 0]))
        fns = []
        for i, b in enumerate(blocks):
            fn = (lambda m, i=i: m.set_fill(TEAL, opacity=0.75 if int(np.ceil(n.get_value())) - 1 == i else 0.32))
            b.add_updater(fn)
            fns.append(fn)
        self.add(counter)
        lab2 = label("talin rod: 13 helix bundles", [0, 2.7, 0], TEAL, 32)
        self.play(n.animate.set_value(13), Succession(Wait(1.5), FadeTransform(lab, lab2, run_time=0.6), Wait(1.0)),
                  run_time=3.1, rate_func=linear)
        for b, fn in zip(blocks, fns):
            b.remove_updater(fn)
            b.set_fill(TEAL, opacity=0.32)
        self.remove(counter)
        self.at("Each bundle is folded")
        self.play(LaggedStart(*[Indicate(b, scale_factor=1.15, color=TEAL) for b in blocks], lag_ratio=0.12), run_time=2.2)
        self.finish()


class S04Hidden(SpokenScene):
    def construct(self):
        line, blocks = make_rod(False, mark=False)
        lc, rc = left_chip(), right_cable()
        lab = label("talin rod: 13 helix bundles", [0, 2.7, 0], TEAL, 32)
        schem = label("schematic", [5.7, -3.5, 0], GREY, 24)
        fld = Rectangle(width=14.4, height=8.2, stroke_width=0, fill_color=GREY, fill_opacity=0.14).set_z_index(-3)
        self.add(fld)
        myo = VGroup(RoundedRectangle(corner_radius=0.08, width=0.6, height=0.22, stroke_color=CORAL, stroke_width=2,
                                      fill_color=CORAL, fill_opacity=0.6).move_to([5.8, 0.62, 0]))
        bob(myo, 0.35, 0.8)
        self.add(line, *blocks, lc, rc, lab, schem, myo)
        mk = [blocks[i] for i in MARK]
        dots = VGroup(*[Dot([blocks[i].get_x(), RY, 0], radius=0.1, color=TEXT) for i in MARK])
        self.at("hide binding sites")
        ex = label("examples, not a count", [-4.4, -3.5, 0], GREY, 24)
        site = label("hidden vinculin site", [1.224, -1.3, 0], TEXT, 28)
        arr = Arrow([1.224, -0.95, 0], [1.224, -0.5, 0], buff=0, color=TEXT, stroke_width=3, max_tip_length_to_length_ratio=0.3)
        self.play(*[b.animate.set_fill(TEAL, opacity=0.06) for b in mk], FadeIn(dots), FadeIn(ex), run_time=1.2)
        self.play(FadeIn(site), GrowArrow(arr), run_time=0.6)
        self.at("Vinculin")
        v1 = chip("vinculin", TEAL, size=26, pad=0.14).move_to([-2.5, 1.7, 0])
        v2 = chip("vinculin", TEAL, size=26, pad=0.14).move_to([2.5, 1.7, 0])
        wander(v1, -4.4, -0.9, 1.25, 2.0, 0.35, -0.3)
        wander(v2, 0.9, 4.4, 1.25, 2.0, -0.3, -0.35)
        self.play(FadeIn(v1), FadeIn(v2), run_time=0.7)
        self.at("While a bundle stays folded")
        self.play(*[b.animate.set_fill(TEAL, opacity=0.32).set_stroke(TEXT, 3, opacity=0.85) for b in mk],
                  FadeOut(dots), FadeOut(site), FadeOut(arr), run_time=1.2)
        self.at("tucked away")
        self.play(*[Indicate(b, color=TEXT, scale_factor=1.12) for b in mk], run_time=1.4)
        self.finish()


def clamp():
    return RoundedRectangle(corner_radius=0.08, width=0.5, height=1.6, stroke_color=GREY, stroke_width=4,
                            fill_color=GREY, fill_opacity=0.6).move_to([-5.4, RY, 0])


def test_pieces(positions):
    ps = VGroup(*[RoundedRectangle(corner_radius=0.08, width=0.9, height=0.5, stroke_color=TEAL, stroke_width=3,
                                   fill_color=TEAL, fill_opacity=0.5).move_to([x, y, 0]) for x, y in positions])
    return ps


class S05Predict(SpokenScene):
    def construct(self):
        line, blocks = make_rod(False)
        lc, rc = left_chip(), right_cable()
        lab = label("talin rod: 13 helix bundles", [0, 2.5, 0], TEAL, 32)
        schem = label("schematic", [5.7, -3.5, 0], GREY, 24)
        self.add(line, *blocks, lc, rc, lab, schem)
        cl = clamp()
        lab2 = label("purified talin rod piece", [0, 2.5, 0], TEAL, 32)
        dust = motes(12, -6.5, 6.5, -3.4, 3.0, TEAL, 5, 0.3)
        self.play(FadeOut(rc), Transform(lc, cl), FadeTransform(lab, lab2), FadeIn(dust), run_time=1.6)
        self.at("stretch it")
        arrow = Arrow([4.8, RY, 0], [5.8, RY, 0], buff=0, color=GOLD, stroke_width=9)
        xs2 = rod_xs(True)
        line2 = Line([-4.6, RY, 0], [xs2[-1] + 0.3, RY, 0], color=TEAL, stroke_width=4)
        self.play(GrowArrow(arrow), Transform(line, line2), *[b.animate.set_x(x) for b, x in zip(blocks, xs2)],
                  arrow.animate.shift(RIGHT * 0.9), run_time=2.0)
        for b in blocks:
            b.jamp = 0.01
        self.at("test piece")
        tp = test_pieces([(-1.0, -2.2), (1.0, -2.2)])
        for t in tp:
            wobble(t, 0.08, 1.0)
        tl = label("vinculin head (test piece)", [0, -3.0, 0], TEAL, 28)
        self.play(FadeIn(tp), FadeIn(tl), run_time=0.8)
        self.at("What happens")
        q = T("Stretch talin: hidden sites?", size=40).move_to([0, 3.45, 0])
        self.play(FadeIn(q, shift=DOWN * 0.1), run_time=0.6)
        self.at("hidden sites")
        self.play(*[Indicate(blocks[i], color=TEXT, scale_factor=1.15) for i in MARK], run_time=1.4)
        self.finish()


class S06Pause(NarratedScene):
    def construct(self):
        xs = rod_xs(True)
        line = Line([-4.6, RY, 0], [xs[-1] + 0.3, RY, 0], color=TEAL, stroke_width=4)
        blocks = []
        for i, x in enumerate(xs):
            b = RoundedRectangle(corner_radius=0.12, width=0.56, height=1.3, stroke_color=TEAL, stroke_width=3,
                                 fill_color=TEAL, fill_opacity=0.32).move_to([x, RY, 0])
            if i in MARK:
                b.set_stroke(TEXT, 3, opacity=0.85)
            jig(b, RY, 0.01, 2.4, i * 0.7)
            blocks.append(b)
        cl = clamp()
        arrow = Arrow([5.7, RY, 0], [6.7, RY, 0], buff=0, color=GOLD, stroke_width=9)
        lab = label("purified talin rod piece", [0, 2.5, 0], TEAL, 32)
        schem = label("schematic", [5.7, -3.5, 0], GREY, 24)
        tp = test_pieces([(-1.0, -2.2), (1.0, -2.2)])
        for t in tp:
            wobble(t, 0.08, 1.0)
        tl = label("vinculin head (test piece)", [0, -3.0, 0], TEAL, 28)
        q = T("Stretch talin: hidden sites?", size=40).move_to([0, 3.45, 0])
        dust = motes(12, -6.5, 6.5, -3.4, 3.0, TEAL, 5, 0.3)
        self.add(line, *blocks, cl, arrow, lab, schem, tp, tl, q, dust)
        for _ in range(4):
            self.play(arrow.animate.shift(RIGHT * 0.12), *[Indicate(blocks[i], color=TEXT, scale_factor=1.1) for i in MARK],
                      rate_func=there_and_back, run_time=1.1)
        self.finish()


def dashed_of(b, w=0.34, h=2.1):
    r = RoundedRectangle(corner_radius=0.08, width=w, height=h).move_to([b.get_x(), RY, 0])
    return DashedVMobject(r, num_dashes=24, dashed_ratio=0.55).set_stroke(TEAL, 3)


class S07Reveal(SpokenScene):
    def construct(self):
        xs = rod_xs(True)
        line = Line([-4.6, RY, 0], [xs[-1] + 0.3, RY, 0], color=TEAL, stroke_width=4)
        blocks = []
        for i, x in enumerate(xs):
            b = RoundedRectangle(corner_radius=0.12, width=0.56, height=1.3, stroke_color=TEAL, stroke_width=3,
                                 fill_color=TEAL, fill_opacity=0.32).move_to([x, RY, 0])
            if i in MARK:
                b.set_stroke(TEXT, 3, opacity=0.85)
            jig(b, RY, 0.01, 2.4, i * 0.7)
            blocks.append(b)
        cl = clamp()
        arrow = Arrow([5.7, RY, 0], [6.7, RY, 0], buff=0, color=GOLD, stroke_width=9)
        lab = label("purified talin rod piece", [0, 2.5, 0], TEAL, 32)
        schem = label("schematic", [5.7, -3.5, 0], GREY, 24)
        tp = test_pieces([(-1.0, -2.2), (1.0, -2.2)])
        for t in tp:
            wobble(t, 0.08, 1.0)
        tl = label("vinculin head (test piece)", [0, -3.0, 0], TEAL, 28)
        q = T("Stretch talin: hidden sites?", size=40).move_to([0, 3.45, 0])
        dust = motes(12, -6.5, 6.5, -3.4, 3.0, TEAL, 5, 0.3)
        self.add(line, *blocks, cl, arrow, lab, schem, tp, tl, q, dust)
        mk = [blocks[i] for i in MARK]
        self.at("unfold")
        dashed = [dashed_of(b) for b in mk]
        for b in mk:
            b.jamp = 0
        self.play(FadeOut(q),
                  *[b.animate.stretch_to_fit_height(2.1).stretch_to_fit_width(0.34).set_fill(TEAL, opacity=0.08).set_stroke(opacity=0)
                    for b in mk], *[FadeIn(d) for d in dashed], run_time=1.2)
        unf = label("unfolded", [mk[1].get_x(), 1.8, 0], TEAL, 28)
        self.play(FadeIn(unf), run_time=0.4)
        self.at("hidden sites open")
        dots = VGroup(*[Dot([b.get_x(), RY, 0], radius=0.1, color=TEXT) for b in mk])
        self.play(FadeIn(dots), run_time=0.4)
        self.play(*[d.animate.move_to([b.get_x(), RY - 1.05, 0]) for d, b in zip(dots, mk)], run_time=1.0)
        self.at("test pieces bind")
        self.play(tp[0].animate.move_to([mk[0].get_x(), -1.4, 0]), tp[1].animate.move_to([mk[1].get_x(), -1.4, 0]),
                  tl.animate.move_to([(mk[0].get_x() + mk[1].get_x()) / 2, -2.15, 0]), run_time=1.4)
        self.play(*[Flash(d, color=TEXT, flash_radius=0.4, line_length=0.15) for d in dots[:2]], run_time=0.6)
        self.at("Back in a cell")
        iw = int_world()
        iw.strand.become(rope(-3.3, 0.0, -7.1, 7.1, 0.7, ORANGE, 5))
        myo = make_myo()
        cyto = motes(8, -6.5, 3.5, -1.8, 3.6, GREY, 3, 0.4)
        oldstuff = VGroup(line, *blocks, cl, arrow, lab, schem, tp, tl, dust, unf, dots, *dashed)
        self.play(FadeOut(oldstuff), FadeIn(VGroup(*iw.parts)), FadeIn(myo), FadeIn(cyto), run_time=1.2)
        self.at("activated vinculin")
        v = add_vinc()
        vl = label("activated vinculin", [1.15, -0.55, 0], TEAL, 28)
        self.play(FadeIn(v["blocks"]), FadeIn(v["dots"]), FadeIn(vl), run_time=0.9)
        self.at("another tie")
        self.play(Create(v["ties"]), run_time=1.0)
        self.at("to actin")
        b1, b2, b3 = gold_blob(), gold_blob(), gold_blob()
        paths = [[(1.0, 1.3), (TX, 1.3), (TX, -1.7)],
                 [(1.5, 1.3), (3.55, 1.3), (3.55, 0.5), (TX - 0.1, 0.5), (TX, -0.3), (TX, -1.7)],
                 [(1.9, 1.3), (2.95, 1.3), (2.95, -0.55), (TX - 0.1, -0.55), (TX, -1.0), (TX, -1.7)]]
        self.add(b1, b2, b3)
        self.play(*[MoveAlongPath(b, path_of(p)) for b, p in zip((b1, b2, b3), paths)], run_time=1.8, rate_func=linear)
        self.play(FadeOut(VGroup(b1, b2, b3)), run_time=0.3)
        self.at("pulling can recruit")
        rr = label("pull can recruit reinforcements", [0, 3.3, 0], TEXT, 34)
        self.play(FadeIn(VGroup(backing(rr), rr)), run_time=0.7)
        self.finish()


class S08Numbers(SpokenScene):
    def construct(self):
        F = ValueTracker(0)
        UPS, DOWNS, REP = [8, 13, 19, 24], [5, 8, 12, 16], [2, 5, 8, 11]
        state = [0, 0, 0, 0]

        def tether():
            f = F.get_value()
            for k in range(4):
                if f > UPS[k]:
                    state[k] = 1
                elif f < DOWNS[k]:
                    state[k] = 0
            y = -2.65
            g = VGroup()
            for i in range(13):
                op = i in REP and state[REP.index(i)]
                h = 0.5 if op else 0.2
                b = RoundedRectangle(corner_radius=0.05, width=0.6, height=h, stroke_color=TEAL, stroke_width=3,
                                     fill_color=TEAL, fill_opacity=0.08 if op else 0.4).move_to([-3.5, y + h / 2, 0])
                g.add(b)
                y += h + 0.02
            bead = Circle(radius=0.42, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.55).move_to([-3.5, y + 0.45, 0])
            fld = DashedLine([-3.5, y + 0.9, 0], [-3.5, 2.75, 0], color=GOLD, stroke_width=4)
            return VGroup(g, bead, fld)

        stack = always_redraw(tether)
        surface = Rectangle(width=3.4, height=0.2, stroke_color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=0.5).move_to([-3.5, -2.8, 0])
        magnet = VGroup(RoundedRectangle(corner_radius=0.08, width=1.5, height=0.5, stroke_color=GREY, stroke_width=3,
                                         fill_color=GREY, fill_opacity=0.55),
                        Rectangle(width=0.3, height=0.3, stroke_width=0, fill_color=GREY, fill_opacity=0.7).shift(LEFT * 0.55 + DOWN * 0.3),
                        Rectangle(width=0.3, height=0.3, stroke_width=0, fill_color=GREY, fill_opacity=0.7).shift(RIGHT * 0.55 + DOWN * 0.3)
                        ).move_to([-3.5, 3.0, 0])
        X0, K = 1.0, 5.2 / 30
        box = Rectangle(width=5.2, height=0.8, stroke_color=GREY, stroke_width=3).move_to([X0 + 2.6, 0.2, 0])
        band = Rectangle(width=20 * K, height=1.3, stroke_width=0, fill_color=GOLD, fill_opacity=0.14).move_to([X0 + 15 * K, 0.2, 0])
        gfill = always_redraw(lambda: Rectangle(width=max(0.01, F.get_value() * K), height=0.8, stroke_width=0,
                                                fill_color=GOLD, fill_opacity=0.85).move_to([X0 + max(0.01, F.get_value() * K) / 2, 0.2, 0]))
        ticks = VGroup(*[M(str(v), size=24, color=TEXT).move_to([X0 + v * K, -0.62, 0]) for v in (0, 10, 20, 30)])
        fl = label("force (pN)", [3.6, -1.3, 0], GOLD, 30)
        schem = label("schematic, not data", [4.6, -3.5, 0], GREY, 24)
        cyto = motes(8, 0.5, 6.6, -3.4, 3.6, GOLD, 7, 0.18)
        self.add(stack)
        tw = label("magnetic tweezers: one molecule", [-3.4, -3.5, 0], TEXT, 28)
        self.play(FadeIn(tw), FadeIn(surface), FadeIn(magnet), FadeIn(VGroup(box, band, ticks, fl, schem)), FadeIn(cyto), run_time=1.0)
        self.add(gfill)
        self.at("pulled a bead")
        self.play(F.animate.set_value(3), run_time=1.0)
        self.at("single mouse")
        self.play(Indicate(surface, color=TEAL, scale_factor=1.04), run_time=0.8)
        self.at("Bundles unfolded")
        self.play(F.animate.set_value(28), run_time=5.0, rate_func=linear)
        bl = label("unfolding events (about)", [X0 + 15 * K, 1.3, 0], GOLD, 28)
        self.add(bl)
        self.at("They refolded")
        self.play(F.animate.set_value(3), run_time=2.8, rate_func=linear)
        self.at("A model")
        self.play(F.animate.set_value(15), run_time=1.2, rate_func=linear)
        mb = label("model: force buffer", [3.6, 2.5, 0], TEXT, 32)
        self.play(FadeIn(mb), F.animate.set_value(9), run_time=1.2, rate_func=linear)
        self.play(F.animate.set_value(13), run_time=1.0, rate_func=linear)
        self.finish()


class S09Catenin(SpokenScene):
    def construct(self):
        iw = int_world()
        iw.strand.become(rope(-3.3, 0.0, -7.1, 7.1, 0.7, ORANGE, 5))
        v = add_vinc()
        myo = make_myo()
        ivg = VGroup(*iw.parts, myo, v["blocks"], v["ties"], v["dots"])
        d = chain_parts(y=0.35)
        chain = chain_group(d)
        for dd in d["calcium"]:
            for c in dd:
                wobble(c, 0.06, 1.2)
        cyto = motes(10, -6.5, 6.5, -2.4, 2.6, TEAL, 11, 0.3)
        chain.shift(UP * 8)
        self.add(ivg, chain, cyto)
        self.play(ivg.animate.shift(DOWN * 8), chain.animate.shift(DOWN * 8), run_time=1.8, rate_func=smooth)
        self.remove(ivg)
        self.at("Alpha")
        ra = d["adaptors"][3]
        self.play(Indicate(ra, color=TEAL, scale_factor=1.1), run_time=0.8)
        self.at("hidden vinculin site")
        dot = Dot([ra.get_x() + 0.62, 0.07, 0], radius=0.09, color=TEXT)
        hs = label("hidden vinculin site", [4.45, 1.15, 0], TEXT, 26)
        self.play(ra[0].animate.set_fill(TEAL, opacity=0.05), FadeIn(dot), FadeIn(hs), run_time=1.0)
        self.at("tension opens it")
        arrows = force_arrows()
        vc = chip("activated vinculin", TEAL, size=26, pad=0.14).move_to([4.45, -1.6, 0])
        self.play(GrowArrow(arrows[0]), GrowArrow(arrows[1]), dot.animate.move_to([ra.get_x() + 0.62, -0.24, 0]),
                  ra[0].animate.set_stroke(TEXT, 3, opacity=0.7), FadeIn(vc), run_time=0.8)
        self.play(vc.animate.move_to([4.45, -0.62, 0]), run_time=0.8)
        tie = Line([ra.get_x() + 0.62, -0.24, 0], [ra.get_x() + 0.62, 0.07, 0], color=TEAL, stroke_width=5)
        self.play(Flash(dot, color=TEXT, flash_radius=0.4, line_length=0.15), Create(tie), run_time=0.6)
        self.at("So both chains")
        lbls = VGroup(hs)
        self.play(FadeOut(lbls), FadeOut(arrows), run_time=0.4)
        for a in d["adaptors"]:
            a[1].set_opacity(0)
        vc[1].set_opacity(0)
        chain_stuff = VGroup(chain, dot, vc, tie)
        iw2 = int_world()
        iw2.strand.become(rope(-3.3, 0.0, -7.1, 7.1, 0.7, ORANGE, 5))
        v2 = add_vinc()
        myo2 = make_myo()
        low = VGroup(*iw2.parts, myo2, v2["blocks"], v2["ties"], v2["dots"])
        low.scale(0.42).move_to([0, -2.2, 0])
        self.play(chain_stuff.animate.scale(0.46).move_to([0, 2.1, 0]), FadeIn(low), run_time=1.6)
        g1 = SurroundingRectangle(chain_stuff, color=GOLD, buff=0.08, stroke_width=4)
        g2 = SurroundingRectangle(low, color=GOLD, buff=0.04, stroke_width=4)
        both = label("both chains can reinforce", [0, 0.0, 0], TEXT, 28)
        self.play(Create(g1), Create(g2), FadeIn(both), run_time=0.9)
        self.finish()


class S10Autoinhibition(SpokenScene):
    def construct(self):
        iw = int_world()
        iw.strand.become(rope(-3.3, 0.0, -7.1, 7.1, 0.7, ORANGE, 5))
        bgw = VGroup(*iw.parts)
        bgw.set_opacity(0.3)
        cyto = motes(10, -6.5, 6.5, -1.8, 3.0, TEAL, 13, 0.3)
        q = T("Is force the only key?", size=42).move_to([0, 3.45, 0])
        self.play(FadeIn(bgw), FadeIn(cyto), FadeIn(q, shift=DOWN * 0.1), run_time=0.9)
        self.at("and vinculin")
        t1 = ai_chip("talin", 36, True).move_to([-4.2, -0.9, 0])
        t2 = ai_chip("vinculin", 36, True).move_to([0.2, -0.9, 0])
        for g, (a, b) in ((t1, (-4.8, -3.6)), (t2, (-0.8, 1.2))):
            wander(g, a, b, -1.3, -0.5, 0.3, 0.12)
        self.play(FadeIn(t1), FadeIn(t2), run_time=0.9)
        self.at("fold shut")
        self.play(latch_close(t1), latch_close(t2), run_time=1.0)
        self.at("hiding their binding sites")
        self.play(Indicate(t1.la.bar, color=TEXT), Indicate(t2.la.bar, color=TEXT), run_time=1.2)
        self.at("self closing")
        al = label("autoinhibition: sites masked", [-1.5, 2.45, 0], TEXT, 34)
        sc = label("schematic", [-5.7, -3.5, 0], GREY, 24)
        self.play(FadeIn(VGroup(backing(al), al)), FadeIn(sc), run_time=0.8)
        self.finish()


def mito(cx, cy=-0.75):
    o = Ellipse(width=5.2, height=2.3, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.2).move_to([cx, cy, 0])
    xs = np.linspace(cx - 1.8, cx + 1.8, 60)
    inner = VMobject(color=GREY, stroke_width=3).set_points_smoothly([[x, cy + 0.5 * np.sin(3.2 * (x - cx)), 0] for x in xs])
    return VGroup(o, inner)


class S11Mitochondria(SpokenScene):
    def construct(self):
        cyto = motes(14, -6.6, 6.6, -3.4, 3.0, GREY, 17, 0.3)
        title = label("mitochondrial test: no force", [0, 3.45, 0], TEXT, 34)
        mL, mR = mito(-3.4), mito(3.4)
        self.play(FadeIn(title), FadeIn(mL), FadeIn(mR), FadeIn(cyto), run_time=1.2)
        self.at("Normal auto inhibited")
        nf = label("normal forms", [-3.4, -2.6, 0], TEXT, 30)
        vL = ai_chip("wild-type vinculin", 26, False).move_to([-3.7, 1.0, 0])
        tL = ai_chip("wild-type talin", 26, False).move_to([-3.7, 2.45, 0])
        wobble(tL, 0.06, 1.0)
        self.play(FadeIn(nf), FadeIn(vL), FadeIn(tL), run_time=1.0)
        self.at("did not bind")
        self.play(tL.animate.shift(DOWN * 0.55), run_time=0.6)
        self.play(tL.animate.shift(UP * 0.55), run_time=0.6, rate_func=rush_from)
        self.at("Releasing either")
        ar = label("autoinhibition released", [3.4, -2.6, 0], TEXT, 30)
        vR = ai_chip("wild-type vinculin", 26, False).move_to([3.1, 1.0, 0])
        tR = ai_chip("wild-type talin", 26, False).move_to([3.1, 2.45, 0])
        self.play(FadeIn(ar), FadeIn(vR), FadeIn(tR), run_time=1.0)
        self.at("protein's autoinhibition")
        self.play(latch_open(vR), run_time=0.7)
        self.at("enabled binding")
        self.play(latch_open(tR), run_time=0.6)
        self.play(tR.animate.move_to([3.1, 2.05, 0]), run_time=0.9)
        self.play(Flash(Dot([3.1 - 0.1, 1.6, 0]), color=TEXT, flash_radius=0.5, line_length=0.18), run_time=0.5)
        self.at("Those active forms")
        old = VGroup(title, mL, mR, nf, vL, tL, ar, vR, tR, cyto)
        # the fibroblast on fibronectin
        haze = Rectangle(width=14.4, height=1.9, stroke_width=0, fill_color=ORANGE, fill_opacity=0.14).move_to([0, -3.05, 0])
        ropes = VGroup(*[rope(y, 0.2, -7.1, 7.1, i * 0.8, ORANGE, 4) for i, y in enumerate((-2.3, -2.9, -3.5))])
        cellb = Ellipse(width=10.5, height=3.2, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.16).move_to([0, 0.6, 0])
        nuc = Ellipse(width=2.6, height=1.1, stroke_color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=0.3).move_to([0, 1.5, 0])
        motors = VGroup(*[RoundedRectangle(corner_radius=0.08, width=0.8, height=0.24, stroke_color=CORAL, stroke_width=2,
                                           fill_color=CORAL, fill_opacity=0.65).move_to([x, 0.3, 0]) for x in (-4, -2, 0, 2, 4)])
        for i, m in enumerate(motors):
            bob(m, 0.18, 1.5 + 0.15 * i)
        fib = VGroup(haze, ropes, cellb, nuc, motors)
        self.play(FadeOut(old), FadeIn(fib), run_time=1.4)
        self.at("disorganized adhesions")
        streaks = VGroup(*[VMobject(color=TEAL, stroke_width=7).set_points_as_corners(
            [[x, -1.0, 0], [x + 0.35, -1.4, 0], [x - 0.1, -1.85, 0], [x + 0.25, -2.3, 0]]) for x in (-4.4, -2.2, 0.3, 2.5, 4.6)])
        ac = chip("activated talin-vinculin", TEAL, size=26, pad=0.14).move_to([0, -0.5, 0])
        self.play(Create(streaks), FadeIn(ac), run_time=1.6)
        self.at("myosin 2 was blocked")
        ml = label("myosin II blocked", [0, 2.75, 0], CORAL, 32)
        for m in motors:
            m.bamp = 0
        self.play(*[m.animate.set_fill(GREY, opacity=0.5).set_stroke(GREY) for m in motors], FadeIn(ml), run_time=0.9)
        self.at("was blocked")
        ap = label("adhesions persist, not fully mature", [0, 3.45, 0], TEXT, 32)
        self.play(FadeIn(ap), run_time=0.7)
        self.finish()


class S12Hedge(SpokenScene):
    def construct(self):
        iw = int_world()
        iw.strand.become(rope(-3.3, 0.0, -7.1, 7.1, 0.7, ORANGE, 5))
        myo = make_myo()
        bgw = VGroup(*iw.parts, myo)
        bgw.set_opacity(0.3)
        pl = RoundedRectangle(corner_radius=0.15, width=6.5, height=3.2, stroke_color=GREY, stroke_width=3,
                              fill_color=BG, fill_opacity=0.7).move_to([-3.45, 2.15, 0])
        pr = RoundedRectangle(corner_radius=0.15, width=6.5, height=3.2, stroke_color=GREY, stroke_width=3,
                              fill_color=BG, fill_opacity=0.7).move_to([3.45, 2.15, 0])
        # left panel: pull stretches a talin bundle row and exposes a site
        lx = [-5.0 + 0.7 * i for i in range(5)]
        lblocks = VGroup(*[RoundedRectangle(corner_radius=0.1, width=0.5, height=0.7, stroke_color=TEAL, stroke_width=3,
                                            fill_color=TEAL, fill_opacity=0.32).move_to([x, 2.0, 0]) for x in lx])
        lline = Line([-5.3, 2.0, 0], [-1.9, 2.0, 0], color=TEAL, stroke_width=4)
        for i, b in enumerate(lblocks):
            jig(b, 2.0, 0.03, 2.4, i)
        self.play(FadeIn(bgw), FadeIn(pl), FadeIn(lline), FadeIn(lblocks), run_time=0.6)
        self.at("So force can")
        pa = Arrow([-1.85, 2.0, 0], [-0.95, 2.0, 0], buff=0, color=GOLD, stroke_width=8)
        pt = label("pull", [-1.1, 2.7, 0], GOLD, 30)
        self.play(GrowArrow(pa), FadeIn(pt), run_time=0.6)
        self.at("expose")
        nx = [-5.0 + 0.86 * i for i in range(5)]
        lline2 = Line([-5.3, 2.0, 0], [-1.3, 2.0, 0], color=TEAL, stroke_width=4)
        b2 = lblocks[2]
        self.play(Transform(lline, lline2), *[b.animate.set_x(x) for b, x in zip(lblocks, nx)], pa.animate.shift(RIGHT * 0.6),
                  b2.animate.stretch_to_fit_height(1.3).stretch_to_fit_width(0.34).set_fill(TEAL, opacity=0.08), run_time=0.8)
        sdot = Dot([b2.get_x(), 1.35, 0], radius=0.1, color=TEXT)
        self.play(FadeIn(sdot), Flash(sdot, color=TEXT, flash_radius=0.4, line_length=0.15), run_time=0.6)
        self.at("while engineered")
        self.play(FadeIn(pr), run_time=0.6)
        ept = label("engineered fibroblast test", [3.45, 3.3, 0], TEXT, 28)
        tc = ai_chip("talin", 26, False).move_to([1.9, 2.1, 0])
        vc = ai_chip("vinculin", 26, False).move_to([5.1, 1.15, 0])
        wobble(vc, 0.06, 1.0)
        wobble(tc, 0.06, 1.0, 1.0)
        self.play(FadeIn(ept), FadeIn(tc), FadeIn(vc), run_time=0.8)
        self.at("auto inhibition")
        al = label("autoinhibition", [2.2, 1.2, 0], TEAL, 26)
        self.play(FadeIn(al), run_time=0.5)
        self.at("can bypass")
        self.play(latch_open(tc), run_time=0.7)
        self.play(vc.animate.move_to([4.7, 2.1, 0]), run_time=1.0)
        self.play(Flash(Dot([vc.c.get_left()[0], 2.1, 0]), color=TEXT, flash_radius=0.5, line_length=0.18), run_time=0.5)
        self.at("not known")
        tl = label("normal tissue signals: unknown", [-0.4, -0.2, 0], TEXT, 32)
        qm = T("?", size=64, color=TEXT).move_to([4.2, -0.2, 0])
        qm.add_updater(lambda m, dt: m.set_opacity(0.6 + 0.4 * np.sin(4 * self.renderer.time)))
        self.play(FadeIn(VGroup(backing(tl, 0.15, 0.85), tl)), FadeIn(qm), run_time=0.8)
        self.finish()


class S13Scale(SpokenScene):
    def construct(self):
        line, blocks = make_rod(False, mark=False)
        bg = VGroup(line, *blocks)
        lab = label("one molecule: a few pN", [0, 1.9, 0], TEXT, 34)
        cyto = motes(10, -6.5, 6.5, -3.4, 3.4, TEAL, 21, 0.28)
        self.play(FadeIn(bg), FadeIn(lab), FadeIn(cyto), run_time=0.9)
        # the whole cell on its matrix
        haze = Rectangle(width=14.4, height=2.9, stroke_width=0, fill_color=ORANGE, fill_opacity=0.14).move_to([0, -2.55, 0])
        ropes = VGroup(*[rope(y, 0.2, -7.1, 7.1, i * 0.8, ORANGE, 4) for i, y in enumerate((-1.9, -2.5, -3.1, -3.7))])
        cellb = Ellipse(width=12.4, height=3.8, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.16).move_to([0, 0.9, 0])
        xs = np.linspace(-5.6, 5.6, 29)
        chains = VGroup(*[RoundedRectangle(corner_radius=0.06, width=0.28, height=0.6, stroke_color=PURPLE, stroke_width=3,
                                           fill_color=PURPLE, fill_opacity=0.5).move_to([x, -1.2, 0]) for x in xs])
        for i, c in enumerate(chains):
            c._ph = i * 0.5
            c.add_updater(lambda m, dt, self=self: m.set_stroke(PURPLE, 3, opacity=0.55 + 0.45 * np.sin(2.5 * self.renderer.time - m._ph) ** 2))
        cell_all = VGroup(haze, ropes, cellb, chains)
        self.at("not the pull")
        for b in blocks:
            b.clear_updaters()
        marker = RoundedRectangle(corner_radius=0.06, width=0.28, height=0.6, stroke_color=TEAL, stroke_width=4,
                                  fill_color=TEAL, fill_opacity=0.6).move_to([0, -1.2, 0])
        self.play(Transform(bg, marker), FadeOut(lab), FadeIn(cell_all), run_time=1.4)
        self.at("whole cell")
        wl = label("whole cell: many chains", [0, 3.6, 0], TEXT, 34)
        self.play(FadeIn(wl), run_time=0.6)
        # pan to the adherens chain
        d = chain_parts(y=0.35)
        chain = chain_group(d)
        chain.shift(UP * 8)
        self.add(chain)
        self.at("One more link")
        old = VGroup(cell_all, bg, wl)
        self.play(old.animate.shift(DOWN * 8), chain.animate.shift(DOWN * 8), run_time=1.5, rate_func=smooth)
        self.remove(old)
        self.at("where the catenins")
        ring = Circle(radius=0.38, stroke_color=TEXT, stroke_width=4).move_to([5.85, 0.35, 0])
        self.play(Create(ring), run_time=0.7)
        self.at("behaves oddly")
        qm = T("?", size=64, color=TEXT).move_to([5.85, 1.3, 0])
        qm.add_updater(lambda m, dt: m.set_opacity(0.55 + 0.45 * np.sin(5 * self.renderer.time)))
        self.play(FadeIn(qm), run_time=0.4)
        self.play(Indicate(ring, color=TEXT, scale_factor=1.25), run_time=1.0)
        self.at("text picks")
        cl = label("catenin to actin: next", [3.6, -1.2, 0], TEXT, 32)
        self.play(FadeIn(VGroup(backing(cl, 0.12, 0.7), cl)), run_time=0.6)
        self.finish()


class S14Return(SpokenScene):
    def construct(self):
        W = build_world(motors=True)
        zoom_in(W, 2)
        self.add(W)
        q = T("Can pull change a link?", size=40).move_to([0, 3.45, 0])
        self.play(W.animate.scale(1 / 1.4, about_point=PC).shift(-ZS).scale(1 / ZK, about_point=WP),
                  run_time=3.8, rate_func=smooth)
        self.at("Some links do not")
        qg = VGroup(backing(q, 0.15, 0.85), q)
        self.play(FadeIn(qg), run_time=0.6)
        self.at("Pulling can open")
        ties = VGroup()
        for x in (-4.5, -1.5, 1.5, 4.5):
            ties.add(Line([x + 0.3, -1.2, 0], [x + 0.3, -0.62, 0], color=TEAL, stroke_width=6))
        for gx in (-3.0, 0.0, 3.0):
            ties.add(Line([gx - 0.55, 0.85, 0], [gx - 0.55, 0.25, 0], color=TEAL, stroke_width=6))
        self.play(LaggedStart(*[Create(t) for t in ties], lag_ratio=0.18), run_time=2.6)
        self.at("Engineered release")
        panel = RoundedRectangle(corner_radius=0.15, width=7.4, height=1.5, stroke_color=GREY, stroke_width=3,
                                 fill_color=BG, fill_opacity=0.96).move_to([0, -2.9, 0])
        pl = label("engineered test: no force", [0, -2.35, 0], TEXT, 24)
        tc = ai_chip("talin", 28, False).move_to([-2.2, -3.35, 0])
        vc = ai_chip("vinculin", 28, False).move_to([2.2, -3.35, 0])
        self.play(FadeIn(panel), FadeIn(pl), FadeIn(tc), FadeIn(vc), run_time=0.9)
        self.at("release from")
        self.play(latch_open(tc), run_time=0.7)
        self.play(vc.animate.move_to([0.75, -3.35, 0]), run_time=1.0)
        self.play(Flash(Dot([vc.c.get_left()[0], -3.35, 0]), color=TEXT, flash_radius=0.5, line_length=0.18), run_time=0.4)
        self.at("bypass force")
        ans = label("Sometimes; engineered release bypasses force.", [0, 2.85, 0], TEXT, 32)
        self.play(FadeIn(VGroup(backing(ans, 0.15, 0.85), ans)), run_time=0.8)
        self.finish()


class S15End(EndCard):
    LINE = "Adhesion links do not just hold; pull opens sites that reinforce them."
