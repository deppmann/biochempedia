"""A Second Place to Double  (chapter 2 of "What Makes the Human Brain Big")

COLOR MAP (same map as chapter 1 and scenes.old.py; one colour per concept, whole series)
  BLUE   = classical radial glia / founder progenitors, and intermediate progenitors (the units)
  YELLOW = neurons, and the columns they stack into
  GREEN  = area, and symmetric (doubling) divisions
  PURPLE = thickness, and asymmetric (adding) divisions
  PINK   = outer radial glia
  ORANGE = a gene or protein (here: the PAX6, SOX2 and TBR2 markers)
  RED    = missing / no contact
  GREY   = ventricle, brain surface, labels (LG = the brighter grey used for labels), de-emphasised things
  GOLD   = the question and the final rule
All tissues, cells and counts are schematic; the toy lineage is a simulation, not a measurement.
"""
import random

import numpy as np

from bp_style import *

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58BB8"
LG = "#BCC3CF"      # label grey: brighter than GREY so labels read on the dark ground


# ----------------------------------------------------------------------------- helpers
def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.04, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def darr(a, b, color=GREY, w=5, tip=0.2):
    return DoubleArrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                       max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def bar(x0, x1, y, color=GREY, h=0.24):
    return RoundedRectangle(corner_radius=0.08, width=x1 - x0, height=h, stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=0.35).move_to([(x0 + x1) / 2, y, 0])


def dot(x, y, color, r=0.16):
    return Circle(radius=r, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=0.9).move_to([x, y, 0])


def heading(text, color=TEXT, size=30):
    return T(text, size, color, font=TITLE_FONT).move_to([0, 3.5, 0])


def lab(text, size, color, x, y, **kw):
    return T(text, size, color, **kw).move_to([x, y, 0])


def left_lab(text, size, color, x_left, y, **kw):
    t = T(text, size, color, **kw)
    return t.move_to([x_left + t.width / 2, y, 0])


def right_lab(text, size, color, x_right, y, **kw):
    t = T(text, size, color, **kw)
    return t.move_to([x_right - t.width / 2, y, 0])


def tint(lo, hi, color, op=0.07, x0=-6.6, x1=6.6):
    return Rectangle(width=x1 - x0, height=hi - lo, stroke_width=0, fill_color=color,
                     fill_opacity=op).move_to([(x0 + x1) / 2, (lo + hi) / 2, 0])


def till(scene, t):
    """Wait until the scene clock reads t seconds."""
    rest = t - scene.elapsed()
    if rest > 0.02:
        scene.wait(rest)


def add_drift(group, amp=0.12, seed=1):
    """Make every member of the group wander slightly: a time-lapse feel."""
    rng = np.random.default_rng(seed)
    base = [m.get_center().copy() for m in group]
    par = [(rng.uniform(0, 6), rng.uniform(0, 6), rng.uniform(1.2, 2.4)) for _ in group]
    clock = {"t": 0.0}

    def upd(g, dt):
        clock["t"] += dt
        for m, b, (p1, p2, w) in zip(g, base, par):
            m.move_to(b + amp * np.array([np.sin(w * clock["t"] + p1), np.cos(0.8 * w * clock["t"] + p2), 0]))
    group.add_updater(upd)


# ----------------------------------------------------------------------------- the cortical wall
SUR_Y = 2.75     # brain surface
VEN_Y = -3.3     # ventricle
VZ = (-3.2, -2.3)
ISVZ = (-2.3, -1.5)
OSVZ = (-1.5, 2.75)


def wall_base():
    return VGroup(bar(-6.6, 6.6, VEN_Y),
                  right_lab("ventricle", 28, LG, 6.6, -2.9),
                  Line([-6.6, SUR_Y, 0], [6.6, SUR_Y, 0], color=GREY, stroke_width=4),
                  right_lab("brain surface", 28, LG, 6.6, 3.12))


def founder(x, w=1.1, fibre=True):
    patch = Ellipse(width=w, height=0.4, stroke_color=BLUE, stroke_width=3, fill_color=BLUE,
                    fill_opacity=0.5).move_to([x, -2.75, 0])
    if not fibre:
        return patch
    f = Line([x, -2.55, 0], [x, SUR_Y, 0], color=BLUE, stroke_width=3).set_opacity(0.35)
    return VGroup(patch, f)


S02_X = [-1.0, 1.5, 3.9]


def svz_parts(split=True):
    """Everything s02 builds, in its final state (for s03)."""
    d = {}
    d["vz_tint"] = tint(*VZ, BLUE, 0.07)
    d["vz_lab"] = left_lab("ventricular zone", 28, BLUE, -6.6, -2.75)
    d["founders"] = VGroup(*[founder(x) for x in S02_X])
    d["svz_tint"] = tint(ISVZ[0], SUR_Y, GREY, 0.07)
    d["split"] = DashedLine([-6.6, OSVZ[0], 0], [6.6, OSVZ[0], 0], color=LG, stroke_width=3, dash_length=0.18)
    d["isvz_tint"] = tint(ISVZ[0], ISVZ[1], GREY, 0.12)
    d["isvz_lab"] = left_lab("inner subventricular zone", 28, LG, -6.6, -1.9)
    d["osvz_lab"] = left_lab("outer subventricular zone", 28, LG, -6.6, 2.3)
    return d


def zone_stage(label_color=PINK):
    """The wall with zone tints and zone labels: the stage for the outer radial glia scenes."""
    return VGroup(tint(*VZ, BLUE, 0.06), tint(*ISVZ, GREY, 0.08), tint(OSVZ[0], SUR_Y, PINK, 0.07),
                  left_lab("ventricular zone", 28, BLUE, -6.6, -2.75),
                  left_lab("inner subventricular zone", 28, LG, -6.6, -1.9),
                  left_lab("outer subventricular zone", 28, label_color, -6.6, 2.3), wall_base())


def org(x, y, tx, r=0.6):
    """An outer radial glial cell: a pink body and a fibre running to the surface (top x follows tx)."""
    body = dot(x, y, PINK, r)
    fibre = always_redraw(lambda: Line(body.get_top(), [tx.get_value(), SUR_Y, 0], color=PINK,
                                       stroke_width=4).set_opacity(0.85))
    return body, fibre


# ----------------------------------------------------------------------------- scenes
class S00Title(TitleCard):
    LESSON = "What Makes the Human Brain Big"
    TITLE = "A Second Place to Double"


class S01Q(SpokenScene):
    def construct(self):
        x0 = -5.8
        UNIT = 0.85          # one week
        MONTH = UNIT * 4.3
        h_len = 12.5 * UNIT  # human: months, more than 12 weeks
        h_name = left_lab("human: months", 34, TEXT, x0, 3.2)
        h_bar = bar(x0, x0 + h_len, 2.5, BLUE, 0.7)
        m_name = left_lab("mouse: about a week", 34, TEXT, x0, 1.65)
        m_bar = bar(x0, x0 + UNIT, 0.95, BLUE, 0.7)
        axis = Line([x0, 0.25, 0], [6.5, 0.25, 0], color=LG, stroke_width=4)
        ticks = VGroup()
        tlabs = VGroup()
        for xx, txt in [(0, "0"), (UNIT, "1 week"), (MONTH, "1 month"), (2 * MONTH, "2 months"), (3 * MONTH, "3 months")]:
            ticks.add(Line([x0 + xx, 0.25, 0], [x0 + xx, 0.05, 0], color=LG, stroke_width=3))
        tlabs.add(lab("0", 26, LG, x0, -0.2))
        tlabs.add(lab("1 week", 26, LG, x0 + UNIT + 0.35, -0.2))
        tlabs.add(lab("1 month", 26, LG, x0 + MONTH + 0.55, -0.2))
        tlabs.add(lab("2 months", 26, LG, x0 + 2 * MONTH, -0.2))
        tlabs.add(lab("3 months", 26, LG, x0 + 3 * MONTH, -0.2))
        tlabs[1].shift(LEFT * 0.0)
        note = right_lab("schematic, not to scale", 26, LG, 6.6, -0.75)
        q1 = lab("Where might extra divisions happen?", 38, GOLD, 0, -1.7)
        q2 = lab("And why wouldn't they simply make our cortex thick?", 34, GOLD, 0, -2.75)
        fit(q2, max_w=12.4)
        self.at("Human neurogenesis")
        self.play(FadeIn(h_name), GrowFromEdge(h_bar, LEFT), FadeIn(axis), FadeIn(ticks), FadeIn(tlabs), FadeIn(note),
                  run_time=1.4)
        self.at("mouse")
        self.play(FadeIn(m_name), GrowFromEdge(m_bar, LEFT), run_time=0.6)
        self.at("Where might")
        self.play(FadeIn(q1, shift=UP * 0.15), run_time=0.6)
        self.at("And why")
        self.play(FadeIn(q2, shift=UP * 0.15), run_time=0.6)
        self.finish()


class S02Model(SpokenScene):
    def construct(self):
        p = svz_parts()
        base = wall_base()
        head = heading("Rakic's model", GOLD)
        # the wall at the start: ventricle, the zone of progenitors, the zone above, the surface
        above = tint(VZ[1], SUR_Y, GREY, 0.07)
        self.add(base, head, p["vz_tint"], above, p["vz_lab"], p["founders"])
        prog_lab = lab("progenitors", 30, BLUE, S02_X[1], -1.85)
        self.at("progenitors")
        self.play(FadeIn(prog_lab), Indicate(p["founders"], color=BLUE, scale_factor=1.08), run_time=0.9)
        self.at("But in")
        self.play(FadeOut(prog_lab), FadeTransform(head, heading("Fetal monkey cortex", GOLD)), run_time=0.5)
        self.at("the zone above")
        self.play(Indicate(above, color=LG, scale_factor=1.0), run_time=0.8)
        self.at("split")
        self.play(Create(p["split"]), FadeIn(p["isvz_tint"]), FadeIn(p["isvz_lab"]), FadeIn(p["osvz_lab"]),
                  run_time=0.6)
        self.finish()


def s02_final(extra=True):
    p = svz_parts()
    return [wall_base(), heading("Fetal monkey cortex", GOLD), p["vz_tint"], p["svz_tint"], p["isvz_tint"],
            p["split"], p["vz_lab"], p["founders"], p["isvz_lab"], p["osvz_lab"]]


class S03Q2(SpokenScene):
    def construct(self):
        mobs = s02_final()
        self.add(*mobs)
        osvz_lab = mobs[-1]
        glow = Rectangle(width=13.2, height=SUR_Y - OSVZ[0], stroke_color=GOLD, stroke_width=4,
                         fill_color=GOLD, fill_opacity=0.10).move_to([0, (OSVZ[0] + SUR_Y) / 2, 0])
        q = T("?", 190, GOLD, font=TITLE_FONT).move_to([2.2, 0.65, 0])
        self.at("dividing")
        self.play(FadeIn(glow), osvz_lab.animate.set_color(GOLD), run_time=0.5)
        self.at("outer part")
        self.play(FadeIn(q, scale=0.5), run_time=0.7)
        self.finish()


class S04Hansen(SpokenScene):
    def construct(self):
        cx, w = 0.2, 5.6
        top, bot = 2.9, -3.0
        body = RoundedRectangle(corner_radius=0.55, width=w, height=top - bot, stroke_color=LG, stroke_width=6,
                                fill_color=BG, fill_opacity=1).move_to([cx, (top + bot) / 2, 0])

        def band(lo, hi, color, op):
            return Rectangle(width=w - 0.3, height=hi - lo, stroke_width=0, fill_color=color,
                             fill_opacity=op).move_to([cx, (lo + hi) / 2, 0])
        bands = VGroup(band(-2.65, -1.85, BLUE, 0.13), band(-1.85, -0.75, GREY, 0.13), band(-0.75, 2.55, PINK, 0.12))
        ven = Line([cx - w / 2 + 0.3, -2.75, 0], [cx + w / 2 - 0.3, -2.75, 0], color=GREY, stroke_width=6)
        surf = Line([cx - w / 2 + 0.3, 2.62, 0], [cx + w / 2 - 0.3, 2.62, 0], color=GREY, stroke_width=4)
        lx = cx + w / 2 + 0.2
        labs = VGroup(left_lab("brain surface", 26, LG, lx, 2.62),
                      left_lab("outer subventricular\nzone", 26, PINK, lx, 0.9, line_spacing=0.8),
                      left_lab("inner subventricular\nzone", 26, LG, lx, -1.3, line_spacing=0.8),
                      left_lab("ventricular zone", 26, BLUE, lx, -2.3),
                      left_lab("ventricle", 26, LG, lx, -3.05))
        rng = np.random.default_rng(4)
        cells = VGroup()
        for lo, hi, n in [(-2.5, -2.0, 4), (-1.7, -0.9, 4), (-0.5, 2.3, 8)]:
            for _ in range(n):
                cells.add(dot(rng.uniform(cx - 2.0, cx + 2.0), rng.uniform(lo, hi), LG, 0.13).set_opacity(0.75))
        star = dot(cx - 0.9, -0.3, LG, 0.2)
        star_ring = Circle(radius=0.34, stroke_color=TEXT, stroke_width=3).move_to(star)
        star_g = VGroup(star, star_ring)
        year = T("2010", 70, GOLD, font=TITLE_FONT).move_to([-4.7, 1.7, 0])
        names = VGroup(T("Hansen, Lui, Parker", 30, TEXT), T("and Kriegstein", 30, TEXT),
                       T("living human fetal\ncortex slices", 26, LG, line_spacing=0.8)).arrange(DOWN, buff=0.3).move_to([-4.7, -0.15, 0])
        card_box = RoundedRectangle(corner_radius=0.15, width=3.9, height=names.height + 0.5, stroke_color=LG,
                                    stroke_width=2.5).move_to(names)
        tag_dot = Circle(radius=0.11, stroke_width=0, fill_color=GOLD, fill_opacity=1).move_to([-1.0, 3.42, 0])
        tag = left_lab("time-lapse", 28, GOLD, -0.8, 3.42)
        self.add(body, bands, ven, surf, labs, cells, star_g)
        self.play(FadeIn(year, shift=UP * 0.1), FadeIn(card_box), FadeIn(names), run_time=0.4)
        self.at("filmed")
        add_drift(cells, 0.14, 3)
        self.play(FadeIn(tag), FadeIn(tag_dot), star_g.animate.move_to([cx + 0.9, 1.9, 0]), run_time=1.4)
        self.at("human fetal cortex")
        self.play(Indicate(body, color=TEXT, scale_factor=1.02), run_time=0.8)
        self.finish()


CELL_X, CELL_Y0, CELL_R = 1.4, -0.4, 1.0


class S05Markers(SpokenScene):
    def construct(self):
        stage = zone_stage()
        head = lab("Human fetal cortex", 28, LG, 0, 3.5)
        cell = dot(CELL_X, CELL_Y0, PINK, CELL_R)
        glow = VGroup(*[Circle(radius=CELL_R + 0.3 * k, stroke_width=0, fill_color=ORANGE,
                               fill_opacity=0.17 - 0.04 * k).move_to(cell) for k in (1, 2, 3)])
        pax = chip("PAX6", ORANGE, 36).move_to([5.0, 1.1, 0])
        sox = chip("SOX2", ORANGE, 36).move_to([5.0, -1.0, 0])
        l1 = Line(cell.get_right(), pax.get_left(), color=ORANGE, stroke_width=3)
        l2 = Line(cell.get_right(), sox.get_left(), color=ORANGE, stroke_width=3)
        self.add(stage, head)
        self.at("They found cells")
        self.play(FadeIn(cell, scale=0.6), run_time=0.6)
        self.at("markers")
        self.play(FadeIn(glow), run_time=0.8)
        self.at("proteins")
        self.play(Create(l1), FadeIn(pax), run_time=0.6)
        self.at("and")
        self.play(Create(l2), FadeIn(sox), run_time=0.6)
        self.finish()


class S06Shape(SpokenScene):
    def construct(self):
        stage = zone_stage()
        head = lab("Human fetal cortex", 28, LG, 0, 3.5)
        cell = dot(CELL_X, CELL_Y0, PINK, CELL_R)
        self.add(stage, head, cell)
        fibre = Line(cell.get_top(), [CELL_X, SUR_Y, 0], color=PINK, stroke_width=4).set_opacity(0.85)
        fib_lab = left_lab("fibre toward the surface", 28, PINK, CELL_X + 0.5, 2.2)
        cross = VGroup(Line([CELL_X - 0.22, -1.63, 0], [CELL_X + 0.22, -2.07, 0], color=RED, stroke_width=7),
                       Line([CELL_X - 0.22, -2.07, 0], [CELL_X + 0.22, -1.63, 0], color=RED, stroke_width=7))
        gap_lab = left_lab("no process to the ventricle", 30, RED, CELL_X + 0.6, -1.85)
        self.at("kept a fiber")
        self.play(Create(fibre), run_time=1.5, rate_func=linear)
        self.play(FadeIn(fib_lab), run_time=0.4)
        self.at("no process")
        self.play(Create(cross), run_time=0.5)
        self.at("touching")
        self.play(FadeIn(gap_lab), run_time=0.5)
        self.finish()


class S07Move(SpokenScene):
    def construct(self):
        stage = zone_stage()
        head = lab("Human fetal cortex", 28, LG, 0, 3.5)
        tx = ValueTracker(CELL_X)
        body, fibre = org(CELL_X, CELL_Y0, tx, CELL_R)
        self.add(stage, head, fibre, body)
        ghost = DashedVMobject(Circle(radius=CELL_R, color=LG, stroke_width=4), num_dashes=20).move_to([CELL_X, CELL_Y0, 0])
        ghost_lab = right_lab("where it was", 28, LG, CELL_X - CELL_R - 0.2, CELL_Y0)
        Y1 = 1.15
        self.at("moved")
        self.add(ghost)
        self.play(FadeIn(ghost_lab), body.animate.scale(0.8).move_to([CELL_X, Y1, 0]), run_time=1.6)
        self.at("Daughters")
        fibre.set_z_index(2)
        d2 = dot(CELL_X, Y1, PINK, CELL_R * 0.8)
        self.add(d2)
        keep = right_lab("keeps the fibre", 28, PINK, CELL_X - 1.4, Y1)
        self.play(body.animate.scale(0.875), d2.animate.scale(0.875).move_to([CELL_X + 1.8, Y1, 0]),
                  FadeOut(ghost_lab), FadeOut(ghost), FadeIn(keep), run_time=0.8)
        self.at("divide again")
        loop = Arc(radius=0.95, start_angle=PI * 0.75, angle=PI * 0.9, color=PINK, stroke_width=4)
        loop.move_arc_center_to(body.get_center())
        loop.add_tip(tip_length=0.2)
        again = right_lab("can divide again", 28, PINK, CELL_X - 1.4, Y1)
        self.play(Create(loop), FadeTransform(keep, again), run_time=0.7)
        self.at("become")
        self.play(d2.animate.set_color(BLUE), run_time=0.5)
        self.at("intermediate")
        ip_lab = lab("intermediate\nprogenitor", 28, BLUE, CELL_X + 1.8, -0.05, line_spacing=0.8)
        self.play(FadeIn(ip_lab), run_time=0.5)
        self.at("progenitors")
        tbr = chip("TBR2", ORANGE, 28).move_to([CELL_X + 1.8, -1.05, 0])
        self.play(FadeIn(tbr), run_time=0.5)
        self.at("soon")
        link = arr([CELL_X + 2.6, Y1, 0], [4.7, Y1, 0], YELLOW)
        self.play(GrowArrow(link), run_time=0.5)
        self.at("neurons")
        n_lab = lab("neurons", 28, YELLOW, 5.4, 0.25)
        neurons = VGroup(dot(5.4, 1.6, YELLOW, 0.3), dot(5.4, 0.9, YELLOW, 0.3))
        self.play(TransformFromCopy(d2, neurons), FadeIn(n_lab), run_time=0.7)
        self.finish()


class S08Macaque(SpokenScene):
    def construct(self):
        stage = zone_stage()
        head = lab("Human fetal cortex", 28, LG, 0, 3.5)
        MX, MY = 2.8, 0.7
        tx = ValueTracker(MX)
        body, fibre = org(MX, MY, tx, CELL_R)
        self.add(stage, head, fibre, body)
        label = lab("outer radial glia", 32, PINK, MX, MY - 1.55)
        caption = left_lab("one common shape; others occur", 26, LG, -6.5, -0.75)
        self.at("outer radial glia")
        self.play(FadeIn(label), FadeIn(caption), run_time=0.5)
        self.at("Later imaging")
        card = VGroup(T("Betizeau and colleagues, 2013", 28, TEXT), T("fetal macaque", 28, LG)).arrange(DOWN, buff=0.2)
        card_box = RoundedRectangle(corner_radius=0.15, width=card.width + 0.5, height=card.height + 0.4,
                                    stroke_color=LG, stroke_width=2.5).move_to(card)
        card = VGroup(card_box, card).move_to([-3.9, 0.85, 0])
        self.play(FadeIn(card), FadeTransform(head, lab("Fetal macaque cortex", 28, LG, 0, 3.5)), run_time=0.7)
        self.at("making proliferative")
        tx2 = ValueTracker(MX)
        b2, f2 = org(MX, MY, tx2, CELL_R)
        self.add(f2, b2)
        two = lab("two progenitors", 32, PINK, MX, MY - 1.55)
        self.play(body.animate.scale(0.8).move_to([MX - 1.3, MY, 0]), b2.animate.scale(0.8).move_to([MX + 1.3, MY, 0]),
                  tx.animate.set_value(MX - 1.7), tx2.animate.set_value(MX + 1.7),
                  FadeOut(label), run_time=1.0)
        self.play(FadeIn(two), run_time=0.4)
        self.finish()


class S09Second(SpokenScene):
    def construct(self):
        stage = zone_stage(PINK)
        head = lab("Fetal macaque cortex", 30, LG, 0, 3.5)
        fx = [-1.0, 1.4, 3.8]
        founders = VGroup(*[founder(x, 1.2, fibre=False) for x in fx])
        f_lab = lab("founders", 28, BLUE, fx[1], -1.95)
        oy = 0.6
        orgs = VGroup()
        trk = []
        for x in fx:
            tx = ValueTracker(x)
            b, f = org(x, oy, tx, 0.7)
            orgs.add(VGroup(f, b))
            trk.append((b, tx))
        o_lab = lab("outer radial glia", 28, PINK, fx[1], oy - 1.15)
        c1 = chip("doubles", GREEN, 28).move_to([5.75, -2.2, 0])
        c2 = chip("doubles", GREEN, 28).move_to([5.75, oy, 0])
        self.add(stage, head, founders, f_lab)
        self.at("they can be")
        self.play(FadeIn(orgs), FadeIn(o_lab), FadeIn(c1), FadeIn(c2), run_time=0.5)
        self.at("second site")
        self.play(FadeTransform(head, heading("A second site of doubling, seen in macaque", GOLD)), run_time=0.5)
        self.at("doubling", lead=0.3)
        fcopy = founder(fx[1], 1.2, fibre=False)
        self.add(fcopy)
        tx_c = ValueTracker(fx[1])
        b2, f2 = org(fx[1], oy, tx_c, 0.7)
        self.add(f2, b2)
        b1, tx1 = trk[1]
        self.play(founders[1].animate.shift(LEFT * 0.7), fcopy.animate.shift(RIGHT * 0.7),
                  b1.animate.shift(LEFT * 0.75), b2.animate.shift(RIGHT * 0.75),
                  tx1.animate.set_value(fx[1] - 0.9), tx_c.animate.set_value(fx[1] + 0.9),
                  run_time=0.6)
        self.finish()


# ---- the toy lineage
RX0, RX1, RYT = -4.9, 4.1, 2.15
RSTEP = (RX1 - RX0) / 59
GRID_X = [-4.275 + 0.95 * c for c in range(10)]
GRID_Y = [1.3 - 0.62 * r for r in range(6)]
TOY_LABEL = "toy lineage: a simulation, not a measurement"


def toy_slots():
    return [np.array([GRID_X[c], GRID_Y[r], 0]) for r in range(6) for c in range(10)]


def toy_ruler():
    ticks = VGroup(*[Line([RX0 + k * RSTEP, RYT - 0.2, 0], [RX0 + k * RSTEP, RYT, 0], color=LG, stroke_width=2)
                     for k in range(60)])
    base = Line([RX0, RYT, 0], [RX1, RYT, 0], color=LG, stroke_width=3)
    return VGroup(base, ticks)


def toy_top():
    return right_lab(TOY_LABEL, 28, LG, 6.6, 3.55)


def count_label(tracker):
    def make():
        n = int(round(tracker.get_value()))
        return T(f"{n} neurons", 46, YELLOW).move_to([0, -3.1, 0])
    return always_redraw(make)


class S10Toy(SpokenScene):
    def construct(self):
        q = T("How much can a little\ndoubling matter?", 52, GOLD, font=TITLE_FONT, line_spacing=0.8).move_to([0, 0.2, 0])
        self.play(FadeIn(q, shift=UP * 0.15), run_time=0.7)
        self.at("Take a toy lineage")
        big = T("A toy lineage", 64, GOLD, font=TITLE_FONT).move_to([0, 0.2, 0])
        self.play(FadeOut(q), FadeIn(big), run_time=0.6)
        self.at("One progenitor")
        top = toy_top()
        prog = dot(RX0, RYT + 0.55, BLUE, 0.3)
        p_lab = lab("progenitor", 28, BLUE, RX0 + 0.3, RYT + 1.1)
        self.play(FadeOut(big), run_time=0.25)
        self.remove(big, q)
        self.play(FadeIn(top), FadeIn(prog, scale=0.5), FadeIn(p_lab), run_time=0.5)
        self.at("60 rounds")
        ruler = toy_ruler()
        r_lab = left_lab("60 rounds", 30, TEXT, RX1 + 0.3, RYT)
        slots = toy_slots()
        ghosts = VGroup(*[Circle(radius=0.22, stroke_color=GREY, stroke_width=2).move_to(sl).set_fill(opacity=0).set_stroke(GREY, 2, opacity=0.6) for sl in slots])
        self.play(Create(ruler[0]), FadeIn(ruler[1], lag_ratio=0.03), FadeIn(r_lab), FadeIn(ghosts, lag_ratio=0.02), run_time=1.0)
        self.at("each division", lead=0.4)
        cnt = ValueTracker(0)
        count = count_label(cnt)
        neurons = VGroup(*[dot(RX0 + k * RSTEP, RYT - 0.1, YELLOW, 0.22).set_opacity(0) for k in range(60)])
        self.add(neurons, count)

        def runner(k0, k1):
            def f(m, a):
                k = k0 + (k1 - k0) * a
                cnt.set_value(min(60, int(k)))
                prog.move_to([RX0 + min(k, 59) * RSTEP, RYT + 0.55, 0])
                for i, n in enumerate(m):
                    s = float(np.clip((k - i) / 5.0, 0, 1))
                    if k <= i:
                        n.set_opacity(0)
                        continue
                    n.set_opacity(0.95)
                    start = np.array([RX0 + i * RSTEP, RYT - 0.1, 0])
                    n.move_to(start + (slots[i] - start) * s)
            return f
        self.play(FadeOut(p_lab), run_time=0.2)
        self.play(UpdateFromAlphaFunc(neurons, runner(0, 1.0), run_time=0.7, rate_func=linear))
        self.play(UpdateFromAlphaFunc(neurons, runner(1.0, 65), run_time=1.2, rate_func=linear))
        self.finish()


def toy_final():
    """The s10 end state: ruler, progenitor at the right end, 60 neurons in the grid."""
    g = VGroup()
    g.add(toy_ruler(), left_lab("60 rounds", 30, TEXT, RX1 + 0.3, RYT), dot(RX1, RYT + 0.55, BLUE, 0.3), toy_top())
    ns = VGroup(*[dot(s[0], s[1], YELLOW, 0.22).set_opacity(0.95) for s in toy_slots()])
    return g, ns


class S11Sixty(SpokenScene):
    def construct(self):
        g, ns = toy_final()
        total = lab("60 neurons", 46, YELLOW, 0, -3.1)
        self.add(g, ns, total)
        self.at("60")
        self.play(Indicate(ns, color=YELLOW, scale_factor=1.05), Indicate(total, color=YELLOW, scale_factor=1.15),
                  run_time=1.0)
        self.finish()


# ---- the predict diagram (compact layout; DY shifts it down for the first scene)
def diagram(dy=0.0, tags=True):
    d = {}
    d["P"] = dot(-5.0, 1.15 + dy, BLUE, 0.5)
    d["P_lab"] = lab("progenitor", 28, BLUE, -5.0, 0.4 + dy)
    d["a1"] = arr([-4.35, 1.45 + dy, 0], [-2.4, 2.05 + dy, 0], PURPLE)
    d["o1"] = VGroup(dot(-1.7, 2.05 + dy, BLUE, 0.35), dot(-0.85, 2.05 + dy, YELLOW, 0.35))
    d["l1"] = left_lab("a progenitor and a neuron", 30, PURPLE, 0.0, 2.05 + dy)
    d["a2"] = arr([-4.35, 0.85 + dy, 0], [-2.4, 0.25 + dy, 0], GREEN)
    d["o2"] = VGroup(dot(-1.7, 0.25 + dy, BLUE, 0.35), dot(-0.85, 0.25 + dy, BLUE, 0.35))
    d["l2"] = left_lab("two progenitors", 30, GREEN, 0.0, 0.25 + dy)
    d["p9"] = lab("9 in 10", 38, PURPLE, -3.2, 2.75 + dy)
    d["p1"] = lab("1 in 10", 38, GREEN, -3.2, -0.45 + dy)
    return d


CHOICE_TXT = ["about 60", "a few hundred", "thousands"]


def choice_chips():
    chips = VGroup(*[chip(t, LG, 38, pad=0.3) for t in CHOICE_TXT]).arrange(RIGHT, buff=0.45).move_to([0, -2.45, 0])
    return chips


class S12Predict(SpokenScene):
    def construct(self):
        g, ns = toy_final()
        total = lab("60 neurons", 46, YELLOW, 0, -3.1)
        self.add(g, ns, total)
        pred = T("Predict.", 96, GOLD, font=TITLE_FONT).move_to([0, 0, 0])
        self.play(FadeOut(g), FadeOut(ns), FadeOut(total), FadeIn(pred), run_time=0.6)
        DY = -1.1
        d = diagram(DY)
        self.at("Now")
        self.play(FadeTransform(pred, heading("Predict", GOLD)), FadeIn(d["P"]), FadeIn(d["P_lab"]), run_time=0.7)
        self.at("in every round")
        d["p9"] = lab("otherwise", 34, PURPLE, -3.2, 2.75 + DY)
        self.play(GrowArrow(d["a1"]), FadeIn(d["o1"]), FadeIn(d["l1"]), FadeIn(d["p9"]), run_time=0.9)
        self.at("1 in 10")
        self.play(GrowArrow(d["a2"]), FadeIn(d["p1"]), run_time=0.7)
        self.at("making 2 progenitors")
        self.play(FadeIn(d["o2"], scale=0.6), FadeIn(d["l2"]), run_time=0.7)
        self.at("instead")
        self.play(FadeTransform(d["p9"], lab("9 in 10", 38, PURPLE, -3.2, 2.75 + DY)), run_time=0.5)
        self.finish()


def predict_frame(boxes=True):
    d = diagram(0.0)
    note = lab("no cell stops or dies", 32, TEXT, 0, -0.95)
    g = VGroup(lab("On average, how many neurons?", 34, GOLD, 0, 3.5), *d.values(), note)
    chips = choice_chips()
    return g, chips


class S12bPredict2(SpokenScene):
    def construct(self):
        DY = -1.1
        d = diagram(DY)
        head = heading("Predict", GOLD)
        grp = VGroup(*d.values())
        self.add(head, grp)
        self.play(grp.animate.shift(UP * 1.1), run_time=0.8)
        note = lab("no cell stops or dies", 32, TEXT, 0, -0.95)
        self.at("keeps dividing")
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.6)
        self.at("On average")
        self.play(FadeTransform(head, lab("On average, how many neurons?", 34, GOLD, 0, 3.5)), run_time=0.6)
        chips = choice_chips()
        self.at("about 60")
        self.play(FadeIn(chips[0], shift=UP * 0.15), run_time=0.5)
        self.at("a few hundred")
        self.play(FadeIn(chips[1], shift=UP * 0.15), run_time=0.5)
        self.at("thousands")
        self.play(FadeIn(chips[2], shift=UP * 0.15), run_time=0.5)
        self.finish()


class S13Pause(NarratedScene):
    def construct(self):
        g, chips = predict_frame()
        self.add(g, chips)
        self.finish()


# ---- the lineage tree (one simulated run, first rounds) and the average curves
TREE_ROUNDS = 20


def sim_tree(seed, rounds=TREE_ROUNDS, p=0.1):
    r = random.Random(seed)

    def node(tb):
        t = tb
        while t < rounds:
            if r.random() < p:
                return {"tb": tb, "ts": t + 1, "ch": [node(t + 1), node(t + 1)], "split": True}
            t += 1
        return {"tb": tb, "ts": rounds, "ch": [], "split": False}
    return node(0)


def count_leaves(n):
    return 1 if not n["ch"] else sum(count_leaves(c) for c in n["ch"])


def pick_seed():
    for s in range(1, 800):
        n = count_leaves(sim_tree(s))
        if 6 <= n <= 8:
            return s
    return 1


TREE_SEED = pick_seed()
TX0, TX1, TYMIN, TYMAX = -6.3, -1.65, -1.95, 2.35


def tree_geometry():
    root = sim_tree(TREE_SEED)
    leaves = []

    def collect(n):
        if not n["ch"]:
            leaves.append(n)
        for c in n["ch"]:
            collect(c)
    collect(root)
    nl = len(leaves)
    for i, n in enumerate(leaves):
        n["y"] = TYMAX - (TYMAX - TYMIN) * i / max(1, nl - 1)

    def place(n):
        for c in n["ch"]:
            place(c)
        if n["ch"]:
            n["y"] = (n["ch"][0]["y"] + n["ch"][1]["y"]) / 2
    place(root)
    X = lambda t: TX0 + (TX1 - TX0) * t / TREE_ROUNDS
    horiz, vert, drops = [], [], []

    def walk(n):
        horiz.append((n["tb"], n["ts"], n["y"]))
        last = n["ts"] - (1 if n["split"] else 0)
        for r in range(n["tb"], last):
            drops.append((r + 0.5, n["y"]))
        if n["ch"]:
            vert.append((n["ts"], n["ch"][0]["y"], n["ch"][1]["y"]))
        for c in n["ch"]:
            walk(c)
    walk(root)
    return X, horiz, vert, drops, nl


def tree_slices(nslices=10):
    X, horiz, vert, drops, nl = tree_geometry()
    per = TREE_ROUNDS / nslices
    out = []
    for s in range(nslices):
        a, b = s * per, (s + 1) * per
        hb = VMobject(stroke_color=BLUE, stroke_width=4)
        hb.set_fill(opacity=0)
        for ts, te, y in sorted([(max(ts, a), min(te, b), y) for ts, te, y in horiz if te > a and ts < b]):
            hb.start_new_path(np.array([X(ts), y, 0]))
            hb.add_line_to(np.array([X(te), y, 0]))
        vb = VMobject(stroke_color=GREEN, stroke_width=5)
        vb.set_fill(opacity=0)
        for t, ya, yb in sorted([(t, ya, yb) for t, ya, yb in vert if a <= t < b or (s == nslices - 1 and t == b)]):
            vb.start_new_path(np.array([X(t), ya, 0]))
            vb.add_line_to(np.array([X(t), yb, 0]))
        ds = VGroup(*[Dot([X(r), y - 0.16, 0], radius=0.07, color=YELLOW) for r, y in drops if a <= r < b])
        out.append(VGroup(hb, vb, ds))
    return out


def tree_static():
    sl = tree_slices()
    return VGroup(*sl)


def tree_frame():
    y = -2.35
    axis = arr([TX0, y, 0], [TX1 + 0.2, y, 0], LG, 3)
    l0 = left_lab("round 0", 26, LG, TX0 - 0.1, -2.75)
    l1 = right_lab("round 20", 26, LG, TX1 + 0.25, -2.75)
    title = lab("one simulated run", 28, LG, (TX0 + TX1) / 2, 2.92)
    # legend
    s1 = Line([-6.5, -3.33, 0], [-6.5, -2.98, 0], color=GREEN, stroke_width=5)
    t1 = left_lab("= two progenitors", 26, LG, -6.2, -3.15)
    s2 = Line([-6.65, -3.55, 0], [-6.2, -3.55, 0], color=BLUE, stroke_width=4)
    s2d = Dot([-6.42, -3.71, 0], radius=0.07, color=YELLOW)
    t2 = left_lab("= progenitor + neuron", 26, LG, -6.05, -3.55)
    leg = VGroup(s1, t1, s2, s2d, t2)
    return VGroup(axis, l0, l1, title), leg


# chart geometry (right side)
CX0, CX1 = 0.7, 6.5
PB, PSC = 1.05, 1.3 / 300.0      # pool chart: base y, units per progenitor
NB, NSC = -2.7, 2.4 / 3000.0    # neuron chart: base y, units per neuron
CX = lambda r: CX0 + (CX1 - CX0) * r / 60.0
POOL = [1.1 ** t for t in range(61)]
NEUR = [9 * (1.1 ** t - 1) for t in range(61)]       # expected neurons after t rounds


def poly(pts, color, w=5):
    m = VMobject(stroke_color=color, stroke_width=w)
    m.set_fill(opacity=0)
    m.set_points_as_corners([np.array(p) for p in pts])
    return m


def chart_axes():
    ax = VGroup()
    ax.add(Line([CX0, PB, 0], [CX0, PB + 1.4, 0], color=LG, stroke_width=3),
           Line([CX0, PB, 0], [CX1, PB, 0], color=LG, stroke_width=3),
           Line([CX0, NB, 0], [CX0, NB + 2.5, 0], color=LG, stroke_width=3),
           Line([CX0, NB, 0], [CX1, NB, 0], color=LG, stroke_width=3))
    for v in (0, 300):
        ax.add(right_lab(str(v), 26, LG, CX0 - 0.18, PB + v * PSC))
    for v in (0, 1000, 2000, 3000):
        ax.add(right_lab(f"{v:,}", 26, LG, CX0 - 0.18, NB + v * NSC))
    for r in (0, 20, 40, 60):
        ax.add(Line([CX(r), NB, 0], [CX(r), NB - 0.12, 0], color=LG, stroke_width=3))
        ax.add(lab(str(r), 26, LG, CX(r), NB - 0.4))
    ax.add(lab("round", 26, LG, CX(30), NB - 0.85))
    ax.add(lab("average over many runs", 28, LG, (CX0 + CX1) / 2, 2.92))
    ax.add(left_lab("progenitors in the pool", 26, BLUE, CX0 + 0.3, PB + 1.5))
    return ax


def pool_curve():
    return poly([(CX(t), PB + POOL[t] * PSC, 0) for t in range(61)], BLUE, 6)


def neuron_curve():
    return poly([(CX(t), NB + NEUR[t] * NSC, 0) for t in range(61)], YELLOW, 6)


def equation(y=3.58):
    a = M("expected neurons = 9 × (1.1", 28, YELLOW)
    b = M("60", 22, YELLOW)
    c = M(" − 1) ≈ 2,700", 28, YELLOW)
    b.next_to(a, RIGHT, buff=0.03).align_to(a, UP).shift(UP * 0.08)
    c.next_to(b, RIGHT, buff=0.1).align_to(a, DOWN)
    return VGroup(a, b, c).move_to([0, y, 0])


def lab_pool_a():
    return left_lab("pool × 1.1 each round", 28, BLUE, CX0 + 0.35, PB + 0.65)


def lab_pool_b():
    return lab("about 300 progenitors still cycling", 28, BLUE, 3.4, 0.55)


def lab_neur():
    d = DashedLine([CX0, NB + 2731 * NSC, 0], [CX1, NB + 2731 * NSC, 0], color=YELLOW, stroke_width=3, dash_length=0.15)
    t = left_lab("about 2,700 on average", 28, YELLOW, CX0 + 0.3, -0.05)
    return VGroup(d, t)


class S14Reveal(SpokenScene):
    def construct(self):
        g, chips = predict_frame()
        self.add(g, chips)
        slices = tree_slices()
        frame_tree, legend = tree_frame()
        axes = chart_axes()
        self.at("Thousands")
        self.play(chips[2].animate.set_color(GREEN).scale(1.1), chips[0].animate.set_opacity(0.25),
                  chips[1].animate.set_opacity(0.25), run_time=0.7)
        self.at("Each doubling")
        self.play(FadeOut(g), FadeOut(chips), run_time=0.4)
        self.play(FadeIn(frame_tree), FadeIn(legend), run_time=0.4)
        self.play(LaggedStart(*[AnimationGroup(Create(s[0], rate_func=linear), Create(s[1], rate_func=linear),
                                               FadeIn(s[2])) for s in slices], lag_ratio=1.0), run_time=2.4)
        self.at("so the pool")
        pc = pool_curve()
        self.play(AnimationGroup(FadeIn(axes, run_time=0.3),
                                 Succession(Wait(0.2), Create(pc, rate_func=linear, run_time=1.2)),
                                 Succession(Wait(0.7), FadeIn(lab_pool_a(), run_time=0.4))))
        self.at("each round")
        self.play(FadeIn(lab_pool_b()), run_time=0.4)
        self.at("compound interest")
        nc = neuron_curve()
        eq = equation()
        self.play(Create(nc, rate_func=linear), FadeIn(eq, shift=DOWN * 0.1), run_time=1.0)
        self.play(FadeIn(lab_neur()), run_time=0.4)
        self.finish()


def s14_final():
    ft, lg = tree_frame()
    return VGroup(tree_static(), ft, lg), VGroup(chart_axes(), pool_curve(), neuron_curve(), lab_pool_a(),
                                                 lab_pool_b(), lab_neur()), equation()


# ---- the payoff bar chart
BAX = -4.6
BBASE = -2.1
BSC = 4.5 / 3000.0
BX_A, BX_D = -1.6, 2.4


def bars_axis():
    g = VGroup(Line([BAX, BBASE, 0], [BAX, BBASE + 4.65, 0], color=LG, stroke_width=3),
               Line([BAX, BBASE, 0], [6.2, BBASE, 0], color=LG, stroke_width=3))
    for v in (0, 1000, 2000, 3000):
        g.add(Line([BAX - 0.12, BBASE + v * BSC, 0], [BAX, BBASE + v * BSC, 0], color=LG, stroke_width=3))
        g.add(right_lab(f"{v:,}", 26, LG, BAX - 0.2, BBASE + v * BSC))
    g.add(left_lab("neurons after 60 rounds", 26, LG, -6.4, 2.85))
    return g


def bar_a():
    h = max(0.07, 60 * BSC)
    r = Rectangle(width=2.2, height=h, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE,
                  fill_opacity=0.6).move_to([BX_A, BBASE + h / 2, 0])
    return VGroup(r, lab("60", 40, PURPLE, BX_A, BBASE + h + 0.4), lab("adding only", 30, PURPLE, BX_A, BBASE - 0.45))


def bar_d():
    h = 2731 * BSC
    r = Rectangle(width=2.2, height=h, stroke_color=GREEN, stroke_width=3, fill_color=GREEN,
                  fill_opacity=0.4).move_to([BX_D, BBASE + h / 2, 0])
    return VGroup(r, lab("about 2,700 on average", 36, GREEN, BX_D, BBASE + h + 0.45),
                  lab("a little doubling", 30, GREEN, BX_D, BBASE - 0.45))


def caption15():
    return fit(lab("Given enough rounds, a little doubling outgrows a lot of adding.", 30, GOLD, 0, -3.45), max_w=12.4)


class S15Reveal2(SpokenScene):
    def construct(self):
        tree, chartg, eq = s14_final()
        self.add(tree, chartg, eq)
        ax = bars_axis()
        cap = caption15()
        self.play(FadeOut(tree), FadeOut(chartg), FadeIn(ax), FadeIn(cap), run_time=0.8)
        self.at("a little doubling")
        bd = bar_d()
        self.play(GrowFromEdge(bd[0], DOWN), FadeIn(bd[1:]), run_time=0.7)
        self.at("a lot of adding")
        ba = bar_a()
        self.play(GrowFromEdge(ba[0], DOWN), FadeIn(ba[1:]), run_time=0.5)
        self.finish()


class S16Beat(NarratedScene):
    def construct(self):
        self.add(equation(), bars_axis(), caption15(), bar_d(), bar_a())
        self.finish()


# ---- fibres: straight columns versus a fan
COLX = [-4.0, -2.0, 0.0, 2.0, 4.0]
BASE_Y = -3.4
CELL_Y = -2.15
ROW0, ROWD = -1.35, 0.62
ROW_Y = [ROW0 + ROWD * k for k in range(6)]
S_LO, S_HI = 0.4, 2.2
NEU_R = 0.2


def straight_stage(S, with_cells=True):
    base = bar(-5.6, 5.6, BASE_Y)
    band = Rectangle(width=9.4, height=1.0, stroke_width=0, fill_color=PINK, fill_opacity=0.10).move_to([-0.2, CELL_Y, 0])
    cells = VGroup(*[dot(x, CELL_Y, PINK, 0.3) for x in COLX])
    fibres = always_redraw(lambda: VGroup(*[Line([x, CELL_Y + 0.28, 0], [x, S.get_value(), 0], color=PINK,
                                                 stroke_width=4).set_opacity(0.85) for x in COLX]))
    surf = always_redraw(lambda: VGroup(Line([-5.0, S.get_value(), 0], [5.0, S.get_value(), 0], color=GREY, stroke_width=5),
                                        left_lab("surface", 28, LG, 5.15, S.get_value())))
    thick = always_redraw(lambda: VGroup(darr([-5.7, BASE_Y + 0.12, 0], [-5.7, S.get_value(), 0], PURPLE, 5),
                                         T("thickness", 28, PURPLE).rotate(PI / 2).move_to(
                                             [-6.2, (BASE_Y + S.get_value()) / 2, 0])))
    return base, band, cells, fibres, surf, thick


def stage_labels():
    return VGroup(left_lab("ventricle", 28, LG, 4.7, -3.0), left_lab("outer zone", 28, PINK, 4.7, CELL_Y))


def neuron(x, y):
    return dot(x, y, YELLOW, NEU_R).set_opacity(0.95)


def climb(d, x, y_end, rt=1.6):
    y0 = CELL_Y + 0.5

    def f(m, a):
        m.set_opacity(0.95 if a > 0 else 0.0)
        m.move_to([x, y0 + (y_end - y0) * a, 0])
    return UpdateFromAlphaFunc(d, f, run_time=rt, rate_func=smooth)


def s17_head():
    return left_lab("Why no thicker cortex?", 32, GOLD, -6.6, 3.5, font=TITLE_FONT)


def s17_cart():
    return left_lab("cartoon: surface and packing fixed", 28, LG, -6.6, 2.9)


def fibre_label():
    return left_lab("radial glial\nfibre", 26, PINK, 4.6, (ROW_Y[1] + ROW_Y[2]) / 2, line_spacing=0.8)


Q17 = "What would extra neurons do?"


def s17_final(S, rows=3, with_question=True, cart=True):
    base, band, cells, fibres, surf, thick = straight_stage(S)
    g = VGroup(s17_head(), base, band, cells, fibres, surf, thick, stage_labels(), fibre_label())
    if cart:
        g.add(s17_cart())
    for k in range(rows):
        for x in COLX:
            g.add(neuron(x, ROW_Y[k]))
    if with_question:
        g.add(lab(Q17, 42, GOLD, 0, 2.0))
    return g


class S17Predict(SpokenScene):
    def construct(self):
        S = ValueTracker(S_LO)
        base, band, cells, fibres, surf, thick = straight_stage(S)
        head, cart = s17_head(), s17_cart()
        slab = stage_labels()
        self.add(head, cart, base, band, cells, surf, slab)
        self.at("thicker")
        self.play(FadeIn(thick), run_time=0.6)
        till(self, 1.9)
        pred = T("Predict.", 56, GOLD, font=TITLE_FONT).move_to([2.8, 3.45, 0])
        self.play(FadeIn(pred, shift=UP * 0.15), run_time=0.5)
        self.at("New neurons")
        self.play(FadeOut(pred), FadeIn(fibres), run_time=0.8)
        specs = [(k, x) for k in range(3) for x in COLX]
        dots = [neuron(x, ROW_Y[k]).set_opacity(0.0) for k, x in specs]
        for d in dots:
            self.add(d)
        anims = [climb(d, x, ROW_Y[k]) for (k, x), d in zip(specs, dots)]
        fl = fibre_label()
        self.at("climb")
        self.play(AnimationGroup(LaggedStart(*anims, lag_ratio=0.1, run_time=2.4),
                                 Succession(Wait(0.8), FadeIn(fl, run_time=0.4))))
        self.at("If every")
        self.play(Indicate(fibres, color=WHITE, scale_factor=1.0), run_time=1.2)
        self.at("with packing fixed")
        self.play(Indicate(cart, color=GOLD, scale_factor=1.06), run_time=0.8)
        self.at("what would extra neurons")
        q = lab(Q17, 42, GOLD, 0, 2.0)
        self.play(FadeIn(q, shift=UP * 0.15), run_time=0.6)
        self.finish()


class S18Pause(NarratedScene):
    def construct(self):
        self.add(s17_final(ValueTracker(S_LO)))
        self.finish()


class S19Reveal(SpokenScene):
    def construct(self):
        S = ValueTracker(S_LO)
        g = s17_final(S, with_question=False)
        q = lab(Q17, 42, GOLD, 0, 2.0)
        self.add(g, q)
        self.play(FadeOut(q), run_time=0.4)
        new = []
        for k in range(3, 6):
            for x in COLX:
                n = neuron(x, ROW_Y[k]).set_opacity(0)
                self.add(n)
                new.append((k, n))
        self.at("they would stack")
        anims = []
        for k, n in new:
            anims.append(Succession(Wait((k - 3) * 0.55), n.animate(run_time=0.3).set_opacity(0.95)))
        self.play(AnimationGroup(*anims), S.animate.set_value(S_HI), run_time=2.0)
        self.at("thicken")
        txt = right_lab("the cortex thickens", 32, PURPLE, 6.5, 3.5)
        self.play(FadeIn(txt), run_time=0.35)
        self.finish()


def fan_curve(x):
    p0, p3 = np.array([x, CELL_Y + 0.28, 0]), np.array([1.55 * x, S_HI - 0.25, 0])
    c1, c2 = np.array([x, -0.5, 0]), np.array([1.3 * x, 0.35, 0])
    return CubicBezier(p0, c1, c2, p3, stroke_color=PINK, stroke_width=4).set_fill(opacity=0).set_stroke(opacity=0.85)


FAN_F = [0.2 + 0.8 * k / 5 for k in range(6)]


def fan_pos(i, k, curves=None):
    c = (curves or [fan_curve(x) for x in COLX])[i]
    return c.point_from_proportion(FAN_F[k])


def surf_label_fan():
    return right_lab("surface", 28, LG, 6.6, S_HI + 0.32)


def fan_arrow():
    return darr([-6.3, 3.0, 0], [6.3, 3.0, 0], GREEN, 6), lab("favours area", 36, GREEN, 0, 3.5)


def fan_final():
    curves = [fan_curve(x) for x in COLX]
    g = VGroup(bar(-5.6, 5.6, BASE_Y),
               Rectangle(width=9.4, height=1.0, stroke_width=0, fill_color=PINK, fill_opacity=0.10).move_to([-0.2, CELL_Y, 0]),
               VGroup(*[dot(x, CELL_Y, PINK, 0.3) for x in COLX]), VGroup(*curves),
               stage_labels(),
               Line([-6.4, S_HI, 0], [6.4, S_HI, 0], color=GREY, stroke_width=5),
               surf_label_fan())
    ns = VGroup(*[neuron(*fan_pos(i, k, curves)[:2]) for i in range(5) for k in range(6)])
    return g, ns, VGroup(*fan_arrow())


class S20Fan(SpokenScene):
    def construct(self):
        S = ValueTracker(S_HI)
        base, band, cells, fibres, surf, thick = straight_stage(S)
        cart, head = s17_cart(), s17_head()
        slab = stage_labels()
        fl = fibre_label()
        cols = VGroup(*[neuron(x, ROW_Y[k]) for x in COLX for k in range(6)])   # index i*6+k
        self.add(base, band, cells, fibres, surf, thick, cols, head, cart, slab, fl)
        curves = [fan_curve(x) for x in COLX]
        wide = Line([-6.4, S_HI, 0], [6.4, S_HI, 0], color=GREY, stroke_width=5)
        surf_lab = surf_label_fan()
        # the straight picture goes away, then the fan is drawn on a clean stage
        self.at("fibers diverge")
        self.play(FadeOut(fibres), FadeOut(thick), FadeOut(cart), FadeOut(head), FadeOut(fl), FadeOut(cols),
                  run_time=0.8)
        self.play(*[Create(c) for c in curves], run_time=1.2)
        self.at("outward")
        self.play(FadeOut(surf), GrowFromCenter(wide), FadeIn(surf_lab), run_time=0.8)
        # new neurons climb the fan: each travels up its curved fibre to its place
        fan_ns = VGroup(*[neuron(0, 0).set_opacity(0) for _ in range(30)])
        self.add(fan_ns)

        def climb_fan(m, a):
            for i in range(5):
                for k in range(6):
                    n = m[i * 6 + k]
                    start = (5 - k) * 0.07
                    p = float(np.clip((a - start) / 0.5, 0, 1))
                    if p <= 0:
                        n.set_opacity(0)
                        continue
                    n.set_opacity(0.95)
                    pt = curves[i].point_from_proportion(FAN_F[k] * p)
                    n.move_to(pt)
        self.at("That favors")
        arrow, area_l = fan_arrow()
        self.play(GrowFromCenter(arrow), UpdateFromAlphaFunc(fan_ns, climb_fan, run_time=2.2, rate_func=linear))
        self.at("area")
        self.play(FadeIn(area_l, shift=UP * 0.1), run_time=0.5)
        self.finish()


class S21Beat(NarratedScene):
    def construct(self):
        g, ns, ar = fan_final()
        self.add(g, ns, ar)
        self.finish()


# ---- species
SP_X = [-5.1, -1.7, 1.7, 5.1]
SP_NAMES = ["mouse", "ferret", "macaque", "human"]
ZB, ZT = -2.3, 2.4     # zone bottom / top
ZBIG = 3.05
PW = 3.1


def zone_box(i, top=ZT, width=PW, dx=0.0):
    return Rectangle(width=width, height=top - ZB, stroke_color=PINK, stroke_width=3, fill_color=PINK,
                     fill_opacity=0.07).move_to([SP_X[i] + dx, (ZB + top) / 2, 0])


def cell_dots(i, n, top=ZT, width=PW, dx=0.0, seed=0):
    """Distinct, deterministic grids with margins and a pitch greater than dot diameter."""
    cx, cy = SP_X[i] + dx, (ZB + top) / 2
    if n <= 4:
        pts = [(-0.6, -0.9), (0.7, -0.2), (-0.3, 0.9)][:n]
        return VGroup(*[dot(cx + x, cy + y, PINK, 0.15) for x, y in pts])
    cols = 4 if n < 20 else 5
    rows = int(np.ceil(n / cols))
    pitch_x = (width - 0.8) / (cols - 1)
    pitch_y = min(0.72, (top - ZB - 0.9) / max(1, rows - 1))
    pts = []
    for r in range(rows):
        k = min(cols, n - r * cols)
        for c in range(k):
            x = cx + (c - (k - 1) / 2) * pitch_x
            y = cy + ((rows - 1) / 2 - r) * pitch_y
            # A mirrored stagger differentiates the ferret and macaque schematics.
            if i == 1:
                y += 0.10 if c % 2 else -0.10
            elif i == 2:
                y += -0.10 if c % 2 else 0.10
            pts.append((x, y))
    return VGroup(*[dot(x, y, PINK, 0.15) for x, y in pts])


SP_COUNTS = [3, 14, 14, 14]


def base_lab(text, size, color, x, y_bottom):
    """A label whose baseline sits at the same height for every name (a hidden 'g' fixes the box)."""
    t = T(text + "g", size, color)
    t[-1].set_opacity(0)
    vis = VGroup(*t[:-1])
    t.shift(RIGHT * (x - vis.get_center()[0]))
    t.align_to(np.array([0, y_bottom, 0]), DOWN)
    return t


def species_title():
    return left_lab("Outer radial glia", 34, PINK, -6.6, 3.5, font=TITLE_FONT)


def species_legend():
    return lab("one dot = an outer radial glial cell (schematic)", 26, LG, 0, -3.5)


def species_names(human_big=False):
    g = VGroup()
    for i in range(4):
        x = SP_X[i] + (0.0 if not (human_big and i == 3) else 0.0)
        g.add(base_lab(SP_NAMES[i], 30, TEXT if (i == 3 and human_big) else LG, x, -3.0))
    return g


def species_all(human_big=False):
    boxes = [zone_box(i) for i in range(4)]
    dots_ = [cell_dots(i, SP_COUNTS[i]) for i in range(4)]
    if human_big:
        boxes[3] = zone_box(3, top=ZBIG).set_stroke(PINK, 5)
        dots_[3] = cell_dots(3, 30, top=ZBIG, seed=7)
    return boxes, dots_


class S22Species(SpokenScene):
    def construct(self):
        boxes, dots_ = species_all()
        names = species_names()
        self.add(species_title(), species_legend(), *boxes, *dots_, names)
        self.at("not uniquely human")
        self.play(Indicate(VGroup(boxes[3], dots_[3]), color=PINK, scale_factor=1.03), run_time=0.8)
        self.at("Mice")
        self.play(Indicate(VGroup(boxes[0], dots_[0]), color=PINK, scale_factor=1.04), run_time=0.8)
        self.at("ferrets")
        self.play(Indicate(VGroup(boxes[1], dots_[1]), color=PINK, scale_factor=1.03), run_time=0.7)
        self.at("primates")
        self.play(Indicate(VGroup(boxes[2], dots_[2]), color=PINK, scale_factor=1.03),
                  Indicate(VGroup(boxes[3], dots_[3]), color=PINK, scale_factor=1.03), run_time=0.9)
        self.finish()


class S23Human(SpokenScene):
    def construct(self):
        boxes, dots_ = species_all()
        names = species_names()
        self.add(species_title(), species_legend(), *boxes, *dots_, names)
        self.at("subventricular zone")
        osv = right_lab("outer subventricular zone", 26, PINK, 6.7, 3.5)
        self.play(FadeIn(osv), names[3].animate.set_color(TEXT), run_time=0.6)
        self.at("especially large")
        nb, nd = zone_box(3, top=ZBIG).set_stroke(PINK, 5), cell_dots(3, 30, top=ZBIG, seed=7)
        self.play(FadeOut(dots_[3]), run_time=0.2)
        self.play(Transform(boxes[3], nb), FadeIn(nd), run_time=1.1)
        self.finish()


def brain_outline(cx, folded, a=2.6, b=2.0, cy=0.15):
    if folded:
        f = lambda t: np.array([cx + a * (1 + 0.04 * np.sin(14 * t)) * np.cos(t),
                                cy + b * (1 + 0.04 * np.sin(14 * t)) * np.sin(t), 0])
    else:
        f = lambda t: np.array([cx + a * np.cos(t), cy + b * np.sin(t), 0])
    return ParametricFunction(f, t_range=[0, TAU, 0.01], stroke_color=TEXT, stroke_width=6).set_fill(YELLOW, 0.06)


def brain_zone(cx, a=2.6, b=2.0, cy=0.15, n=14, seed=0):
    outer = Ellipse(width=2 * a * 0.76, height=2 * b * 0.76, stroke_color=PINK, stroke_width=3, fill_color=PINK,
                    fill_opacity=0.12).move_to([cx, cy, 0])
    inner = Ellipse(width=2 * a * 0.5, height=2 * b * 0.5, stroke_color=PINK, stroke_width=3, fill_color=BG,
                    fill_opacity=1).move_to([cx, cy, 0])
    rng = np.random.default_rng(seed)
    dots_ = VGroup(*[dot(cx + a * 0.63 * np.cos(t), cy + b * 0.63 * np.sin(t), PINK, 0.15)
                     for t in np.linspace(0.2, TAU + 0.2, n, endpoint=False)])
    return VGroup(outer, inner), dots_


HUM_X, MAR_X = -3.4, 3.4


class S24Marmoset(SpokenScene):
    def construct(self):
        boxes, dots_ = species_all(human_big=True)
        names = species_names(human_big=True)
        title = species_title()
        osv = right_lab("outer subventricular zone", 26, PINK, 6.7, 3.5)
        self.add(title, osv, species_legend(), *boxes, *dots_, names)
        h_out, m_out = brain_outline(HUM_X, True), brain_outline(MAR_X, False)
        h_zone, h_dots = brain_zone(HUM_X, n=16, seed=1)
        m_zone, m_dots = brain_zone(MAR_X, n=10, seed=2)
        h_name = lab("human: folded cortex", 30, TEXT, HUM_X, -2.45)
        m_name = lab("marmoset: nearly smooth", 30, TEXT, MAR_X, -2.45)
        z_lab = lab("outer zone", 28, PINK, MAR_X, 3.0)
        z_line = Line([MAR_X, 2.72, 0], [MAR_X, 1.72, 0], color=PINK, stroke_width=3)
        self.at("marmoset")
        gone = [m for m in list(self.mobjects) if m is not title]
        self.play(*[FadeOut(m) for m in gone], run_time=0.5)
        self.play(FadeIn(h_out), FadeIn(h_zone), FadeIn(h_dots), FadeIn(h_name), run_time=0.5)
        self.play(FadeIn(m_out), FadeIn(m_zone), FadeIn(m_name), run_time=0.5)
        self.at("nearly smooth")
        self.play(Indicate(m_out, color=TEXT, scale_factor=1.0), run_time=0.7)
        self.at("has them too")
        self.play(FadeIn(m_dots, lag_ratio=0.1), FadeIn(z_lab), FadeIn(z_line), run_time=0.9)
        self.at("not enough")
        gold = lab("not enough for folding alone", 36, GOLD, 0, -3.4)
        self.play(FadeIn(gold, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---- the take-home
S25_SUR = 2.55


def s25_final():
    ven = bar(-6.6, 6.6, VEN_Y)
    ven_l = right_lab("ventricle", 28, LG, 6.6, -2.9)
    surf = Line([-6.6, S25_SUR, 0], [6.6, S25_SUR, 0], color=GREY, stroke_width=4)
    surf_l = left_lab("brain surface", 28, LG, -6.6, S25_SUR + 0.32)
    t_vz = tint(*VZ, BLUE, 0.07)
    t_os = tint(OSVZ[0], S25_SUR, PINK, 0.07)
    vz_l = left_lab("ventricular zone", 28, BLUE, -6.6, -2.75)
    os_l = left_lab("outer subventricular zone", 28, PINK, -6.6, -0.95)
    f1 = Ellipse(width=1.2, height=0.44, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.5).move_to([-2.9, -2.75, 0])
    f2 = Ellipse(width=1.2, height=0.44, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.5).move_to([-1.0, -2.75, 0])
    f_lab = left_lab("founders double", 30, GREEN, -0.1, -2.75)
    ffib = VGroup(*[Line([x, -2.55, 0], [x, S25_SUR, 0], color=BLUE, stroke_width=3).set_opacity(0.5) for x in (-2.9, -1.0)])
    o1, o2 = dot(1.6, 0.5, PINK, 0.65), dot(4.2, 0.5, PINK, 0.65)
    o_lab = lab("outer radial glia double", 30, GREEN, 2.9, -0.4)
    fibs = VGroup(CubicBezier(o1.get_top(), [1.6, 1.5, 0], [0.4, 2.0, 0], [-0.6, S25_SUR, 0], stroke_color=PINK, stroke_width=5),
                  CubicBezier(o2.get_top(), [4.2, 1.5, 0], [5.4, 2.0, 0], [6.3, S25_SUR, 0], stroke_color=PINK, stroke_width=5))
    fibs.set_fill(opacity=0)
    area_a = darr([-3.0, 3.05, 0], [6.4, 3.05, 0], GREEN, 9, tip=0.28)
    area_l = lab("favours area", 40, GREEN, 1.7, 3.55)
    th = darr([-6.1, 0.4, 0], [-6.1, S25_SUR - 0.05, 0], PURPLE, 5)
    th_l = T("thickness", 28, PURPLE).rotate(PI / 2).move_to([-5.65, 1.5, 0])
    return dict(ven=ven, ven_l=ven_l, surf=surf, surf_l=surf_l, t_vz=t_vz, t_os=t_os, vz_l=vz_l, os_l=os_l, f1=f1, f2=f2,
                f_lab=f_lab, ffib=ffib, o1=o1, o2=o2, o_lab=o_lab, fibs=fibs, area_a=area_a, area_l=area_l, th=th, th_l=th_l)


class S25Take(SpokenScene):
    def construct(self):
        d = s25_final()
        f1c, o1c = d["f1"].copy().move_to([-1.95, -2.75, 0]), d["o1"].copy().move_to([2.9, 0.5, 0])
        f_lab0 = left_lab("founders", 30, BLUE, -0.1, -2.75)
        o_lab0 = lab("outer radial glia", 30, PINK, 2.9, -0.4)
        self.add(d["t_vz"], d["t_os"], d["ven"], d["ven_l"], d["surf"], d["surf_l"], d["vz_l"], d["os_l"], f1c, f_lab0)
        self.at("can double")
        f2c = f1c.copy()
        self.add(f2c)
        self.play(f1c.animate.move_to([-2.9, -2.75, 0]), f2c.animate.move_to([-1.0, -2.75, 0]),
                  FadeTransform(f_lab0, d["f_lab"]), FadeIn(d["ffib"]), run_time=0.8)
        self.at("Outer radial glia")
        self.play(FadeIn(o1c, scale=0.6), FadeIn(o_lab0), run_time=0.7)
        self.at("double", nth=1)
        o2c = o1c.copy()
        self.add(o2c)
        self.play(o1c.animate.move_to([1.6, 0.5, 0]), o2c.animate.move_to([4.2, 0.5, 0]),
                  FadeTransform(o_lab0, d["o_lab"]), run_time=0.8)
        self.at("fanned fibers")
        self.play(Create(d["fibs"]), run_time=1.0)
        self.at("favor area")
        self.play(FadeIn(d["area_a"]), FadeIn(d["area_l"]), run_time=0.6)
        self.at("over thickness")
        self.play(GrowFromCenter(d["th"]), FadeIn(d["th_l"]), run_time=0.5)
        self.finish()


class S26End(EndCard):
    LINE = "Two places to double; fanned fibres favour area over thickness."

    def construct(self):
        d = s25_final()
        back = VGroup(*d.values())
        self.add(back)
        self.play(FadeOut(back), run_time=0.4)
        self.remove(back)
        line = T("Two places to double;\nfanned fibres favour area over thickness.", 46, TEXT, font=TITLE_FONT, line_spacing=0.9)
        fit(line, max_w=12.4)
        plate = RoundedRectangle(corner_radius=0.2, width=line.width + 0.8, height=line.height + 0.7, stroke_width=0,
                                 fill_color=BG, fill_opacity=1).move_to(line)
        sub = T("biochemistrypedia.com", size=24, color=TEAL).next_to(plate, DOWN, buff=0.3)
        self.play(FadeIn(plate), FadeIn(line, shift=UP * 0.15), run_time=self.beat(0.3))
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        self.finish()
