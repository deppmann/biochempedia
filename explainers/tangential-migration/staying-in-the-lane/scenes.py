"""Tangential migration, chapter 3: Staying in the Lane (Biochemistrypedia chaptered film)

COLOR MAP (one color per concept, shared by all chapters; taken from scenes.old.py)
  ORANGE = inhibitory interneuron (the travelling cell); also the lanes (streams) they travel in
  BLUE   = excitatory pyramidal neurons and their dividing precursors (made in the cortex's own wall)
  TEAL   = the chemokine CXCL12
  PURPLE = its receptor CXCR4 (the little tab on the cell)
  PINK   = Neuregulin-3 (ligand made by the cortical plate)
  GOLD   = its receptor ErbB4 (tab on the cell); also the word "proposed"
  YELLOW = open question marks
  RED    = missing / blocked / mutant (no CXCR4)
  GREEN  = a match (tick mark)
  TEXT   = the immune cell in the one-second aside; plain labels
  GREY   = tissue: cortical wall, meninges, bead, chambers, zone labels
"""
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
PINK = "#E8739B"

# ---- cortical wall geometry (big version) ------------------------------------------------------------
WX0, WX1 = -6.5, 2.8
LX = 3.25                      # left edge of the zone-label column
BANDS = {"men": (3.3, 3.0), "mz": (3.0, 2.2), "cp": (2.2, 0.4), "iz": (0.4, -1.4), "svz": (-1.4, -2.4),
         "vent": (-2.4, -3.0)}
FILL = {"men": 0.5, "mz": 0.08, "cp": 0.16, "iz": 0.06, "svz": 0.12, "vent": 0.02}
NAMES = {"men": "meninges", "mz": "marginal zone", "cp": "cortical plate", "iz": "intermediate zone",
         "svz": "subventricular zone", "vent": "ventricle"}
LANE_TOP, LANE_DEEP = 2.6, -1.3
XR = (-6.2, 2.5)               # where the streams run (big wall)


def wall(x0=WX0, x1=WX1, s=1.0):
    g = VGroup()
    g.bands = {}
    for k, (ya, yb) in BANDS.items():
        ya, yb = ya * s, yb * s
        r = Rectangle(width=x1 - x0, height=ya - yb, stroke_color=GREY, stroke_width=1.5, stroke_opacity=0.6,
                      fill_color=GREY, fill_opacity=FILL[k]).move_to([(x0 + x1) / 2, (ya + yb) / 2, 0])
        g.bands[k] = r
        g.add(r)
    return g


def zlabel(k, color=GREY, text=None, y=None):
    ya, yb = BANDS[k]
    yc = (ya + yb) / 2 if y is None else y
    t = T(text or NAMES[k], 26, color)
    if t.width > 3.35:
        t = VGroup(*[T(a, 26, color) for a in (text or NAMES[k]).rsplit(" ", 1)]).arrange(DOWN, buff=0.04, aligned_edge=LEFT)
    t.move_to([LX + t.width / 2, yc, 0])
    tick = Line([WX1 + 0.05, yc, 0], [LX - 0.12, yc, 0], color=color, stroke_width=1.5, stroke_opacity=0.6)
    g = VGroup(tick, t)
    g.t = t
    return g


def lane_rect(y, h, x0, x1, color=ORANGE, op=0.14, sop=0.5):
    return RoundedRectangle(corner_radius=min(0.3, h / 2), width=x1 - x0, height=h, stroke_color=color, stroke_width=1.5,
                            stroke_opacity=sop, fill_color=color, fill_opacity=op).move_to([(x0 + x1) / 2, y, 0])


def lanes_big(op=0.14):
    return VGroup(lane_rect(LANE_TOP, 0.62, XR[0] - 0.2, XR[1] + 0.2, op=op),
                  lane_rect(LANE_DEEP, 1.0, XR[0] - 0.2, XR[1] + 0.2, op=op))


def cell(color=ORANGE, r=0.17, tab=False, tabcolor=PURPLE, sw=2):
    c = Circle(radius=r, stroke_color=color, stroke_width=sw, fill_color=color, fill_opacity=0.9)
    g = VGroup(c)
    g.c = c
    g.tab = None
    g.tabvis = 1.0
    if tab:
        t = RoundedRectangle(corner_radius=0.03, width=r * 0.55, height=r * 1.2, stroke_color=tabcolor, stroke_width=1,
                             fill_color=tabcolor, fill_opacity=1).move_to(c.get_right() + RIGHT * r * 0.2)
        g.tab = t
        g.add(t)
    return g


def set_vis(g, o):
    g.c.set_fill(opacity=0.9 * o).set_stroke(opacity=o)
    if g.tab is not None:
        g.tab.set_fill(opacity=o * g.tabvis).set_stroke(opacity=o * g.tabvis)


def streamer(g, speed, xr, master):
    g.speed = speed
    g.master = master

    def up(m, dt):
        m.shift(RIGHT * m.speed * dt)
        x = m.get_center()[0]
        if x > xr[1]:
            m.shift(LEFT * (xr[1] - xr[0]))
            x = m.get_center()[0]
        set_vis(m, m.master.get_value() * max(0.0, min(1.0, (x - xr[0]) / 0.5, (xr[1] - x) / 0.5)))
    g.add_updater(up)
    set_vis(g, master.get_value())
    return g


def stream_cells(master, tab=False, xr=XR, ytop=LANE_TOP, ydeep=LANE_DEEP, s=1.0):
    out = []
    w = xr[1] - xr[0]
    for y, fr, sp, dy in ((ytop, (0.08, 0.28, 0.5, 0.7, 0.9), 1.0, (0,) * 5),
                          (ydeep, (0.04, 0.2, 0.37, 0.55, 0.72, 0.9), 0.9, (0.2, -0.2, 0.0, 0.25, -0.15, 0.1))):
        for i, f in enumerate(fr):
            g = cell(tab=tab).move_to([xr[0] + f * w, y + dy[i] * s, 0])
            streamer(g, sp * (w / 8.7) ** 0.5, xr, master)
            out.append(g)
    return out


def stop_updaters(cells):
    for c in cells:
        c.clear_updaters()


def teal_dots(seed=2, x0=XR[0], x1=XR[1], n=16):
    rnd = random.Random(seed)
    ds = []
    for y, hh in ((LANE_TOP, 0.26), (LANE_DEEP, 0.42)):
        for _ in range(n):
            ds.append(Dot([rnd.uniform(x0, x1), y + rnd.uniform(-hh, hh), 0], radius=0.055, color=TEAL))
    return VGroup(*ds)


def pulse_band(sc, band, lab=None, op=0.42, t=0.35):
    base = band.get_fill_opacity()
    anims = [band.animate.set_fill(opacity=op)]
    if lab is not None:
        anims.append(FadeIn(lab, shift=LEFT * 0.1))
    sc.play(*anims, run_time=t)
    sc.play(band.animate.set_fill(opacity=base), run_time=t)


def tabs_around(center, r, angles, color=PURPLE, w=None, h=None):
    w = w or r * 0.2
    h = h or r * 0.38
    g = VGroup()
    for a in angles:
        th = np.radians(a)
        d = r + h / 2 - 0.04
        t = RoundedRectangle(corner_radius=w * 0.25, width=w, height=h, stroke_color=color, stroke_width=1.5,
                             fill_color=color, fill_opacity=1).rotate(th - PI / 2)
        t.move_to([center[0] + d * np.cos(th), center[1] + d * np.sin(th), 0])
        g.add(t)
    return g


def check(center, size=0.5, color=GREEN):
    cx, cy = center
    v = VMobject(color=color, stroke_width=9)
    v.set_points_as_corners([[cx - size * 0.6, cy, 0], [cx - size * 0.2, cy - size * 0.45, 0], [cx + size * 0.7, cy + size * 0.5, 0]])
    return v


def qmark(size=90, pos=(0, 0)):
    return T("?", size, YELLOW, weight=BOLD).move_to([pos[0], pos[1], 0])


def lab_left(text, size, color, x, y):
    t = T(text, size, color)
    t.move_to([x + t.width / 2, y, 0])
    return t


# =====================================================================================================
class S00Title(TitleCard):
    LESSON = "Tangential Migration: Interneurons and the Long Way Round"
    TITLE = "Staying in the Lane"


# ---------------------------------------------------------------------------------------------------
class S01Q(SpokenScene):
    def construct(self):
        w = wall()
        self.add(w)
        dots = VGroup(*[cell().move_to([-6.4 - i*0.65, LANE_DEEP, 0]) for i in range(4)])
        self.add(dots)
        self.at("inside the cortex")
        self.play(dots.animate.shift(RIGHT*3.4), run_time=1.7, rate_func=linear)
        self.at("interneurons")
        self.play(dots.animate.shift(RIGHT*0.7), run_time=0.5)
        arrow = DashedLine([-1.5, 0.15, 0], [-1.5, 1.4, 0], color=YELLOW, stroke_width=5).add_tip(tip_length=0.25)
        q = qmark(80, (-0.9, 1.35))
        self.at("dive into")
        self.play(Create(arrow), FadeIn(q, scale=0.6), run_time=0.5)
        self.at("cortical plate")
        pulse_band(self, w.bands["cp"], op=0.4, t=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------------
class S02Top(SpokenScene):
    def construct(self):
        w = wall()
        self.add(w)
        self.at("meninges")
        pulse_band(self, w.bands["men"], zlabel("men"), op=0.8)
        self.at("marginal zone")
        pulse_band(self, w.bands["mz"], zlabel("mz"))
        self.at("cortical plate")
        pulse_band(self, w.bands["cp"], zlabel("cp"))
        self.finish()


class S03Deep(SpokenScene):
    def construct(self):
        w = wall()
        labs = {k: zlabel(k) for k in NAMES}
        self.add(w, labs["men"], labs["mz"], labs["cp"])
        self.at("intermediate zone")
        pulse_band(self, w.bands["iz"], labs["iz"])
        self.at("subventricular zone")
        pulse_band(self, w.bands["svz"], labs["svz"])
        self.at("zone", nth=1)
        self.play(FadeIn(labs["vent"], shift=LEFT * 0.1), run_time=0.5)
        self.finish()


def full_wall(sc, labels=("men", "mz", "cp", "iz", "svz", "vent")):
    w = wall()
    labs = {k: zlabel(k) for k in labels}
    sc.add(w, *labs.values())
    return w, labs


class S04Streams(SpokenScene):
    def construct(self):
        w, labs = full_wall(self)
        master = ValueTracker(0)
        cells = stream_cells(master)
        ls = lanes_big(op=0.0)
        ls.set_stroke(opacity=0)
        plate_dots = VGroup(cell(r=0.14).move_to([-2.2, 1.0, 0]), cell(r=0.14).move_to([0.6, 1.6, 0]))
        plate_dots.set_opacity(0.0)
        self.add(ls, plate_dots, *cells)
        self.add(T("interneurons", 28, ORANGE).move_to([-2, -3.45, 0]))
        self.at("two streams")
        self.play(ls.animate.set_fill(opacity=0.18).set_stroke(opacity=0.6), master.animate.set_value(1),
                  plate_dots.animate.set_opacity(0.6), run_time=1.4)
        self.at("one runs")
        self.add(T("marginal stream", 26, ORANGE).move_to([-2, 1.98, 0]))
        self.play(ls[0].animate.set_fill(opacity=0.4).set_stroke(opacity=1.0), run_time=0.5)
        self.at("the other deep")
        self.add(T("deep stream", 26, ORANGE).move_to([-2, -0.58, 0]))
        self.play(ls[0].animate.set_fill(opacity=0.18).set_stroke(opacity=0.6),
                  ls[1].animate.set_fill(opacity=0.4).set_stroke(opacity=1.0), run_time=0.5)
        self.wait(1.0)
        self.play(ls[1].animate.set_fill(opacity=0.18).set_stroke(opacity=0.6), run_time=0.5)
        self.finish()


def lane_world(sc, tint=False):
    """wall + zone labels + lanes + streaming cells + two plate dots (the state at the end of s04)."""
    w, labs = full_wall(sc)
    master = ValueTracker(1)
    cells = stream_cells(master)
    ls = lanes_big(op=0.18)
    pd = VGroup(cell(r=0.14).move_to([-2.2, 1.0, 0]), cell(r=0.14).move_to([0.6, 1.6, 0])).set_opacity(0.6)
    sc.add(ls, pd, *cells)
    ls.pd = pd
    return w, labs, ls, cells


class S05Chemo(SpokenScene):
    def construct(self):
        w, labs, ls, cells = lane_world(self)
        VGroup(*labs.values()).set_opacity(0.72)
        glow = VGroup(lane_rect(LANE_TOP, 0.9, XR[0] - 0.3, XR[1] + 0.3, TEAL, 0.0, 0.0),
                      lane_rect(LANE_DEEP, 1.3, XR[0] - 0.3, XR[1] + 0.3, TEAL, 0.0, 0.0))
        self.add(glow)
        self.bring_to_back(glow)
        dots = teal_dots()
        self.at("lined with")
        self.play(glow.animate.set_fill(opacity=0.22), LaggedStart(*[FadeIn(d, scale=0.3) for d in dots], lag_ratio=0.01),
                  run_time=0.6)
        chem = T("chemokine", 30, TEAL).move_to([-1.9, -3.25, 0])
        self.at("chemokine")
        self.play(FadeIn(chem, shift=UP * 0.1), run_time=0.5)
        self.at("small secreted")
        self.play(LaggedStart(*[Indicate(d, color=TEAL, scale_factor=2.2) for d in dots[::2]], lag_ratio=0.04), run_time=1.2)
        # aside: what chemokines are known for
        self.at("first known")
        stop_updaters(cells)
        right = VGroup(*[labs[k] for k in labs])
        right.set_opacity(0.72)
        src = VGroup(*[Dot([0.7 + 0.28 * np.cos(a) * r, 0.4 + 0.28 * np.sin(a) * r, 0], radius=0.06, color=TEAL)
                       for a, r in ((0, 0.3), (1, 1.2), (2, 0.8), (3, 1.4), (4, 0.5), (5, 1.0), (6, 1.6), (2.5, 2.0), (4.5, 1.9))])
        im = Circle(radius=0.34, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.25).move_to([-1.7, 0.4, 0])
        cap = T("immune cell", 28, TEXT).move_to([0.1, -0.35, 0])
        self.play(FadeIn(src, scale=0.4), FadeIn(im, scale=0.6), run_time=0.6)
        self.play(im.animate.move_to([0.1, 0.4, 0]), FadeIn(cap), run_time=1.2)
        self.finish()


class S06Cxcl12(SpokenScene):
    def construct(self):
        w, labs, ls, cells = lane_world(self)
        VGroup(*labs.values()).set_opacity(0.72)
        glow = VGroup(lane_rect(LANE_TOP, 0.9, XR[0] - 0.3, XR[1] + 0.3, TEAL, 0.22, 0.0),
                      lane_rect(LANE_DEEP, 1.3, XR[0] - 0.3, XR[1] + 0.3, TEAL, 0.22, 0.0))
        self.add(glow)
        self.bring_to_back(glow)
        dots = teal_dots()
        self.add(dots)
        chem = T("chemokine", 30, TEAL).move_to([-1.9, -3.25, 0])
        self.add(chem)
        VGroup(*labs.values()).set_opacity(0.72)
        c12 = chip("CXCL12", TEAL, 30).move_to([-1.9, -2.95, 0])
        self.at("called CXCL12")
        self.play(ReplacementTransform(chem, c12), run_time=0.7)
        arrows_top = VGroup(*[Arrow([x, 3.0, 0], [x, 2.05, 0], buff=0, color=TEAL, stroke_width=7, tip_length=0.2, max_stroke_width_to_length_ratio=10)
                              for x in np.linspace(-5.4, 1.8, 7)])
        self.at("meninges make")
        self.play(w.bands["men"].animate.set_fill(color=TEAL, opacity=0.8), LaggedStart(*[GrowArrow(a) for a in arrows_top], lag_ratio=0.1),
                  run_time=1.2)
        prec = VGroup()
        for x in np.linspace(-5.2, 1.6, 6):
            prec.add(VGroup(cell(BLUE, 0.12).move_to([x - 0.15, -2.1, 0]), cell(BLUE, 0.12).move_to([x + 0.15, -2.1, 0])))
        arrows_low = VGroup(*[Arrow([p.get_center()[0], -1.95, 0], [p.get_center()[0], -1.0, 0], buff=0, color=TEAL, stroke_width=7,
                                    tip_length=0.2, max_stroke_width_to_length_ratio=10) for p in prec])
        blab = VGroup(T("dividing precursors of projection neurons", 30, TEXT),
                      T("in the subventricular zone", 28, TEXT)).arrange(DOWN, buff=0.12)
        blab.move_to([-1.85, 1.0, 0])
        self.at("dividing precursors")
        self.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in prec], lag_ratio=0.12), run_time=1.0)
        self.play(FadeOut(ls.pd), FadeIn(blab), LaggedStart(*[GrowArrow(a) for a in arrows_low], lag_ratio=0.08), run_time=1.0)
        self.finish()


class S07Cxcr4(SpokenScene):
    def construct(self):
        w, labs, ls, cells = lane_world(self)
        stop_updaters(cells)
        pick = cells[8]
        big = cell(ORANGE, 1.6, sw=4).move_to([-1.2, 0.0, 0])
        rest = VGroup(w, *labs.values(), ls, ls.pd, *[c for c in cells if c is not pick])
        name = T("interneuron", 30, ORANGE).move_to([-1.2, -2.5, 0])
        self.at("interneurons carry")
        self.play(FadeOut(rest), ReplacementTransform(pick, big), FadeIn(name), run_time=0.8)
        angles = [150, 112, 70, 25, -20, -60, -200, 200]
        tabs = tabs_around([-1.2, 0], 1.6, [20, 60, 100, 140, 180, 220, 300, 340], PURPLE, w=0.34, h=0.62)
        self.at("its receptor")
        self.play(LaggedStart(*[FadeIn(t, scale=0.4) for t in tabs], lag_ratio=0.12), run_time=1.0)
        chp = chip("CXCR4", PURPLE, 34).move_to([4.6, 1.4, 0])
        tp = tabs[1].get_center()
        ln = Line(chp.get_left() + LEFT * 0.05, tp + RIGHT * 0.25 + UP * 0.1, color=PURPLE, stroke_width=3)
        self.at("CXCR4")
        self.play(Create(ln), FadeIn(chp), Indicate(tabs[1], color=PURPLE, scale_factor=1.4), run_time=0.8)
        self.finish()


# ---- chamber assay -----------------------------------------------------------------------------------
CH_X0, CH_X1 = -5.8, 3.4
PORES = [-4.6, -3.0, -1.4, 0.2, 1.8]
CELL_TOP = [(-4.6, 1.1), (-3.0, 1.75), (-1.4, 1.0), (0.2, 1.7), (1.8, 1.1), (-0.7, 1.9)]
CELL_BOT = [(-4.6, -0.9), (-3.0, -1.5), (-1.4, -1.1), (0.2, -1.8), (1.8, -1.3)]
MX, MY0, MY1, BASE_Y = 4.95, -2.5, 2.0, -1.55


def chamber():
    cx = (CH_X0 + CH_X1) / 2
    wd = CH_X1 - CH_X0
    top = Rectangle(width=wd, height=2.68, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.07).move_to([cx, 1.46, 0])
    bot = Rectangle(width=wd, height=2.68, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.07).move_to([cx, -1.46, 0])
    segs = []
    edges = [CH_X0]
    for p in PORES:
        segs.append((edges[-1], p - 0.35))
        edges.append(p + 0.35)
    segs.append((edges[-1], CH_X1))
    mem = VGroup(*[Rectangle(width=b - a, height=0.1, stroke_width=0, fill_color=GREY, fill_opacity=0.8).move_to([(a + b) / 2, 0, 0])
                   for a, b in segs])
    g = VGroup(top, bot, mem)
    g.top, g.bot = top, bot
    return g


def level_rect(h):
    h = max(h, 0.02)
    return Rectangle(width=0.36, height=h, stroke_width=0, fill_color=ORANGE, fill_opacity=0.85).move_to([MX, MY0 + h / 2, 0])


def meter_parts():
    frame = Rectangle(width=0.4, height=MY1-MY0, stroke_color=GREY).move_to([MX,(MY0+MY1)/2,0])
    base = Line([MX-.3,BASE_Y,0],[MX+.3,BASE_Y,0],color=TEXT)
    heading = VGroup(T("cells crossing",26),T("relative to baseline",26)).arrange(DOWN,buff=.1).move_to([4.7,3.4,0])
    low = T("1×",26).move_to([5.75,BASE_Y,0])
    high = VGroup(T(">1×",26),T("baseline",26)).arrange(DOWN,buff=.08).move_to([5.95,1.6,0])
    return VGroup(frame,base,heading,low,high)


def dots_in(x0, x1, y0, y1, n, seed, avoid=None):
    rnd = random.Random(seed)
    out = []
    while len(out) < n:
        x, y = rnd.uniform(x0, x1), rnd.uniform(y0, y1)
        if avoid and avoid[0] < x < avoid[1] and avoid[2] < y < avoid[3]:
            continue
        out.append(Dot([x, y, 0], radius=0.055, color=TEAL))
    return VGroup(*out)


H_BASE = BASE_Y - MY0
H_HIGH = 3.6


class S08Chamber(SpokenScene):
    def construct(self):
        self.add(chamber(), meter_parts())
        cells = VGroup(*[cell(r=.2).move_to([x,y,0]) for x,y in CELL_TOP])
        self.add(cells)
        fill = level_rect(H_BASE); self.add(fill)
        self.at("precursor cells")
        self.add(T("precursor cells",26,ORANGE).move_to([-1,3.25,0]))
        dots = dots_in(-5.5,3.1,-2.1,-.3,34,3)
        self.at("move towards")
        self.add(dots, chip("CXCL12",TEAL,26).move_to([-4.6,-2.45,0]))
        self.play(*[cells[i].animate.move_to([*CELL_BOT[i],0]) for i in range(5)],
                  Transform(fill,level_rect(H_HIGH)),run_time=1.5)
        self.at("placed on one side")
        self.play(Indicate(fill),run_time=.5)
        self.finish()


def chamber_world(sc, crossed=0, meter=H_BASE):
    ch=chamber(); fill=level_rect(meter)
    cells=VGroup(*[cell(r=.2).move_to([*(CELL_BOT[i] if i<crossed else xy),0]) for i,xy in enumerate(CELL_TOP)])
    dots=dots_in(-5.5,3.1,-2.1,-.3,34,3)
    sc.add(ch,meter_parts(),fill,dots,cells)
    return ch,cells,fill,dots


class S09Even(SpokenScene):
    def construct(self):
        ch,cells,fill,dots=chamber_world(self,crossed=5,meter=H_HIGH)
        self.add(chip("CXCL12",TEAL,26).move_to([-4.6,-2.45,0]))
        self.at("spread evenly")
        # New assay: reset cells as the even condition is introduced.
        self.add(dots_in(-5.5,3.1,.3,2.1,34,5),chip("CXCL12",TEAL,26).move_to([-4.6,2.45,0]))
        for c,xy in zip(cells,CELL_TOP): c.move_to([*xy,0])
        self.play(Transform(fill,level_rect(H_BASE)),run_time=.8)
        self.at("no extra crossing")
        self.play(cells[0].animate.move_to([*CELL_BOT[0],0]),run_time=.7)
        self.finish()


def assay_comparison(sc):
    sc.add(T("cells crossing (relative to baseline)",32).move_to([0,3.15,0]))
    baseline=-2.3
    sc.add(Line([-5.5,baseline,0],[5.5,baseline,0],color=GREY))
    for x,h,label,col in [(-2.8,4.3,"gradient",ORANGE),(2.8,1.1,"even",TEAL)]:
        sc.add(Rectangle(width=2,height=h,fill_color=col,fill_opacity=.7,stroke_color=col).move_to([x,baseline+h/2,0]))
        sc.add(T(label,32).move_to([x,-2.8,0]))
    sc.add(DashedLine([-5.3,-1.2,0],[5.3,-1.2,0],color=TEXT))
    sc.add(T("1× baseline",26).move_to([0,-.8,0]),T("several-fold",26,ORANGE).move_to([-2.8,2.5,0]))
    sc.add(T("Qualitative assay result; exact fold change not given",26,GREY).move_to([0,-3.45,0]))


class S09bDiff(SpokenScene):
    def construct(self):
        assay_comparison(self)
        self.at("a difference")
        self.add(VGroup(T("In this assay:",28),T("they follow",28),T("a difference",28)).arrange(DOWN,buff=.18).move_to([2.7,.8,0]))
        self.finish()


class S10Beat(NarratedScene):
    def construct(self):
        assay_comparison(self)
        self.add(VGroup(T("In this assay:",28),T("they follow",28),T("a difference",28)).arrange(DOWN,buff=.18).move_to([2.7,.8,0]))
        self.finish()


# ---- two walls ----------------------------------------------------------------------------------------
MS = 0.9
MW_L = (-6.4, -0.4)
MW_R = (0.4, 6.4)


def mini_lane_y():
    return LANE_TOP * MS, LANE_DEEP * MS


def mini_world(sc, wild_stream=True, master=None):
    wl = wall(*MW_L, s=MS)
    wr = wall(*MW_R, s=MS)
    yt, yd = mini_lane_y()
    ll = VGroup(lane_rect(yt, 0.56, MW_L[0] + 0.1, MW_L[1] - 0.1), lane_rect(yd, 0.9, MW_L[0] + 0.1, MW_L[1] - 0.1))
    lr = VGroup(lane_rect(yt, 0.56, MW_R[0] + 0.1, MW_R[1] - 0.1, RED, 0.0, 0.7), lane_rect(yd, 0.9, MW_R[0] + 0.1, MW_R[1] - 0.1, RED, 0.0, 0.7))
    for r in lr:
        r.set_stroke(color=RED, opacity=0.7)
    sc.add(wl, wr, ll, lr)
    master = master or ValueTracker(1)
    xr = (MW_L[0] + 0.15, MW_L[1] - 0.15)
    cells = []
    w = xr[1] - xr[0]
    for y, fr in ((yt, (0.1, 0.35, 0.6, 0.85)), (yd, (0.05, 0.3, 0.55, 0.8))):
        for f in fr:
            c = cell().move_to([xr[0] + f * w, y, 0])
            if wild_stream:
                streamer(c, 0.8, xr, master)
            cells.append(c)
    sc.add(*cells)
    return wl, wr, ll, lr, cells


class S11Q(SpokenScene):
    def construct(self):
        wl, wr, ll, lr, cells = mini_world(self)
        wr.set_opacity(0)
        lr.set_opacity(0)
        # (rebuilt below with fades)
        self.remove(wr, lr)
        hl = T("wild type", 28, TEXT).move_to([-3.4, 3.4, 0])
        self.add(hl)
        hr = T("no CXCR4", 28, RED).move_to([3.4, 3.4, 0])
        wr2 = wall(*MW_R, s=MS)
        yt, yd = mini_lane_y()
        lr2 = VGroup(lane_rect(yt, 0.56, MW_R[0] + 0.1, MW_R[1] - 0.1, RED, 0.0, 0.7), lane_rect(yd, 0.9, MW_R[0] + 0.1, MW_R[1] - 0.1, RED, 0.0, 0.7))
        self.at("take the receptor")
        self.play(FadeIn(wr2), FadeIn(lr2), FadeIn(hr), run_time=0.9)
        q1, q2 = qmark(70, (3.4, yt)), qmark(70, (3.4, yd))
        qt = T("Where do the interneurons end up?", 28, TEXT).move_to([0, -3.3, 0])
        self.at("where do")
        self.play(FadeIn(q1, scale=0.6), FadeIn(q2, scale=0.6), FadeIn(qt), run_time=0.7)
        self.finish()


class S12Pause(NarratedScene):
    def construct(self):
        wl, wr, ll, lr, cells = mini_world(self, wild_stream=False)
        yt, yd = mini_lane_y()
        self.add(T("wild type", 28, TEXT).move_to([-3.4, 3.4, 0]), T("no CXCR4", 28, RED).move_to([3.4, 3.4, 0]),
                 qmark(70, (3.4, yt)), qmark(70, (3.4, yd)), T("Where do the interneurons end up?", 28, TEXT).move_to([0, -3.3, 0]))
        self.finish()


class S13Who(SpokenScene):
    def construct(self):
        self.add(T("2008 · in mice", 40).move_to([0, 3.3, 0]))
        receptors = []
        for x in [-3.3, 3.3]:
            self.add(cell(r=1.55).move_to([x, 0.45, 0]))
            receptor = RoundedRectangle(corner_radius=0.06, width=0.3, height=0.65,
                                       stroke_color=PURPLE, fill_color=PURPLE, fill_opacity=1)
            receptor.move_to([x + 1.55, 0.45, 0])
            tag = T("CXCR4", 30, PURPLE).move_to([x, 2.4, 0])
            self.add(receptor, tag)
            receptors.append(receptor)
        self.at("blocked")
        blocker = Line(receptors[0].get_center() + LEFT * 0.42,
                       receptors[0].get_center() + RIGHT * 0.42,
                       color=RED, stroke_width=12)
        self.play(Create(blocker), FadeIn(T("blocked", 32, RED).move_to([-3.3, -1.65, 0])), run_time=0.3)
        self.at("deleted")
        self.play(FadeOut(receptors[1]), FadeIn(T("deleted", 32, RED).move_to([3.3, -1.65, 0])), run_time=0.3)
        self.add(T("López-Bendito, Marín and colleagues", 26).move_to([0, -2.65, 0]),
                 T("Li, Pleasure, Rubenstein and colleagues", 26).move_to([0, -3.25, 0]))
        self.finish()


# ---- mutants ------------------------------------------------------------------------------------------
def mk_path(xs, ys, xe, xt, yt, ue):
    def p(u):
        if u < ue:
            return np.array([xs + (xe - xs) * u / ue, ys, 0.0])
        s = min(1.0, (u - ue) / (1 - ue))
        s = s * s * (3 - 2 * s)
        return np.array([xe + (xt - xe) * s, ys + (yt - ys) * s, 0.0])
    return p


TOP_D = [(-6.3, -5.0, -5.3, 1.7), (-5.7, -4.6, -4.4, 1.25), (-5.1, -4.0, -3.6, 1.95), (-4.5, -3.4, -3.9, 0.9), (-3.9, -3.0, -2.7, 1.45)]
DEEP_D = [(-6.3, -5.2, -5.1, 0.8), (-5.6, -4.5, -4.2, 0.62), (-5.0, -4.0, -3.4, 0.6), (-4.4, -3.5, -4.75, 0.65), (-3.8, -2.8, -2.6, 1.0)]


class S14Reveal(SpokenScene):
    def construct(self):
        w, labs = full_wall(self, labels=())
        ls = lanes_big(op=0.12)
        self.add(ls)
        mut = chip("no CXCR4", RED, 28).move_to([-1.9, -3.25, 0])
        self.add(mut, T("wild type: continued travel in lanes",26,GREY).move_to([-1.8,3.65,0]))
        self.add(T("entered at an earlier stage",26,RED).move_to([-1.8,-2.65,0]))
        self.add(T("wild type spread",26,GREY).move_to([4.5,-.15,0]),
                 DoubleArrow([-6.3,-.15,0],[2.5,-.15,0],buff=0,color=GREY))
        tr = ValueTracker(0.0)
        dots = VGroup()
        for i, (xs, xe, xt, yt) in enumerate(TOP_D):
            g = cell().move_to([xs, LANE_TOP, 0])
            p = mk_path(xs, LANE_TOP, xe, xt, yt, 0.3 + 0.04 * i)
            g.add_updater(lambda m, p=p: m.move_to(p(tr.get_value())))
            dots.add(g)
        for i, (xs, xe, xt, yt) in enumerate(DEEP_D):
            g = cell().move_to([xs, LANE_DEEP + (-0.2 if i % 2 else 0.2), 0])
            p = mk_path(xs, LANE_DEEP + (-0.2 if i % 2 else 0.2), xe, xt, yt, 0.34 + 0.04 * i)
            g.add_updater(lambda m, p=p: m.move_to(p(tr.get_value())))
            dots.add(g)
        self.add(dots)
        self.at("left their streams")
        self.play(tr.animate.set_value(1.0), run_time=2.6, rate_func=linear)
        cplab = zlabel("cp")
        self.at("spread less widely", lead=0.1)
        pulse_band(self, w.bands["cp"], cplab, op=0.3, t=0.3)
        # The two spans share the same horizontal scale and left alignment to tissue.
        mutant_span = VGroup(Line([-5.5, -0.55, 0], [-2.4, -0.55, 0], color=RED, stroke_width=5),
                             Line([-5.5, -0.4, 0], [-5.5, -0.7, 0], color=RED, stroke_width=5),
                             Line([-2.4, -0.4, 0], [-2.4, -0.7, 0], color=RED, stroke_width=5))
        lm = lab_left("mutant spread", 26, RED, -1.95, -0.55)
        self.play(Create(mutant_span), FadeIn(lm), run_time=0.7)
        self.finish()


def layer_caption():
    return VGroup(*[T(line, 25, ORANGE) for line in
                    ("most too deep;", "a few reach", "upper layers")]).arrange(DOWN, buff=0.08).move_to([4.65, 0, 0])


def layer_result(sc, settled=False):
    sc.add(T("late-born cells",32,ORANGE).move_to([-3,3.4,0]),chip("no CXCR4",RED,28).move_to([3.7,3.35,0]))
    for y,name in [(1.4,"upper layers"),(-1.4,"deep layers")]:
        sc.add(Rectangle(width=9,height=2.7,stroke_color=GREY,fill_color=GREY,fill_opacity=.12).move_to([-1.6,y,0]),T(name,28).move_to([4.5,y,0]))
    band=Rectangle(width=8.8,height=.6,stroke_color=TEXT,fill_color=TEXT,fill_opacity=.12).move_to([-1.6,2,0])
    sc.add(band,T("normal late-born position",26).move_to([-1.6,2.55,0]))
    pts=[(-4.8,-1.6),(-3.6,-2.2),(-2.4,-1.9),(-1.4,-2.4),(-3,2.0),(-1,2.0)]
    cs=VGroup(*[cell(r=.22).move_to([x,y if settled else -.3+.22*i,0]) for i,(x,y) in enumerate(pts)])
    sc.add(cs,T("schematic distribution",26,GREY).move_to([0,-3.35,0]))
    if settled: sc.add(layer_caption())
    return cs,pts


class S15Layer(SpokenScene):
    def construct(self):
        cs,pts=layer_result(self)
        self.at("too deep")
        self.play(*[cs[i].animate.move_to([*pts[i],0]) for i in range(4)],run_time=.65)
        self.at("not all")
        self.play(*[cs[i].animate.move_to([*pts[i],0]) for i in [4,5]],run_time=.5)
        self.add(layer_caption())
        self.finish()


class S16Beat(NarratedScene):
    def construct(self):
        layer_result(self,True)
        self.finish()


class S17One(SpokenScene):
    def construct(self):
        a=chip("early entry",ORANGE,44).move_to([-3.5,2.3,0])
        b=chip("narrow spread",ORANGE,44).move_to([3.3,2.3,0])
        self.add(a,b)
        d=VGroup(T("one defect could",44,RED),T("explain both",44,RED)).arrange(DOWN).move_to([0,-2,0])
        arrows=VGroup(*[Arrow([x,-1.1,0],ob.get_bottom(),color=RED,stroke_width=7) for x,ob in [(-.8,a),(.8,b)]])
        self.at("can come")
        self.play(FadeIn(d),Create(arrows),run_time=.6)
        self.finish()


# ---- toy model: x = speed * min(t, exit time); table values are illustrative. ----
def toy_world(sc, early=False):
    sc.add(T("Illustrative model: distance = speed × time in lane",30).move_to([0,3.45,0]))
    sc.add(T("normal: 50 µm/h · 48 h → 2.4 mm",28).move_to([0,2.85,0]))
    label="leaves sooner: 50 µm/h · 12 h → 0.6 mm" if early else "slower: 25 µm/h · same 48 h → 1.2 mm"
    sc.add(T(label,28).move_to([0,.25,0]))
    cs=[]
    for y in [2,-.6]:
        sc.add(lane_rect(y,.55,-5.8,5.6,ORANGE,.2),T("lane",26,GREY).move_to([6.1,y,0]))
        sc.add(Line([-5.8,y-.8,0],[5.6,y-.8,0],color=GREY),T("plate",26,GREY).move_to([6.1,y-.8,0]))
        c=cell(r=.2).move_to([-5.5,y,0]);cs.append(c);sc.add(c)
    for y,exit_h in [(-2.15,48),(-2.65,12 if early else 48)]:
        sc.add(Line([-5.5,y,0],[5.1,y,0],color=GREY))
        x=-5.5+10.6*exit_h/48
        sc.add(Line([x,y-.13,0],[x,y+.13,0],color=ORANGE,stroke_width=7))
    sc.add(T("0 h",26).move_to([-5.5,-3.15,0]),T("48 h · normal exit",26,ORANGE).move_to([4.65,-3.15,0]))
    if early: sc.add(T("12 h · early entry",26,ORANGE).move_to([-2.85,-3.15,0]))
    else: sc.add(T("same entry time",26).move_to([0,-3.15,0]))
    return cs


def run_toy(sc,cs,early):
    clock=ValueTracker(0)
    exits=[48,12 if early else 48]; speeds=[50,50 if early else 25]
    for c,y,v,e in zip(cs,[2,-.6],speeds,exits):
        # A short continuous radial move begins at the exit time.
        c.add_updater(lambda m,y=y,v=v,e=e: m.move_to([-5.5+10.6*(v*min(clock.get_value(),e))/2400,y-.8*min(1,max(0,(clock.get_value()-e)/3)),0]))
    cursors=VGroup(*[Dot([-5.5,y,0],radius=.08,color=TEXT) for y in [-2.15,-2.65]])
    for c,y in zip(cursors,[-2.15,-2.65]):
        c.add_updater(lambda m,y=y:m.move_to([-5.5+10.6*min(clock.get_value(),48)/48,y,0]))
    sc.add(cursors)
    sc.play(clock.animate.set_value(51),run_time=1.8,rate_func=linear)
    cursors.clear_updaters(recursive=True)
    for c in cs:c.clear_updaters()


class S18Slow(SpokenScene):
    def construct(self):
        cs=toy_world(self)
        self.at("moving more slowly")
        run_toy(self,cs,False)
        self.at("not enter early")
        self.play(Indicate(cs[1]),run_time=.4)
        self.finish()


class S19Soon(SpokenScene):
    def construct(self):
        cs=toy_world(self,True)
        self.at("leave the lane")
        run_toy(self,cs,True)
        self.at("matches the mutants")
        self.add(T("fits the mutants",30,GREEN).move_to([0,-3.65,0]))
        self.finish()


# ---- beads ---------------------------------------------------------------------------------------------
DISH_C = (-1.6, 0.0)


def dish(c=DISH_C, R=3.3, bead_r=0.55):
    d = Circle(radius=R, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.07).move_to([c[0], c[1], 0])
    halo = VGroup(*[Circle(radius=bead_r + 0.28 * k, stroke_width=0, fill_color=TEAL, fill_opacity=0.16 - 0.04 * k).move_to([c[0], c[1], 0])
                    for k in range(1, 4)])
    bead = Circle(radius=bead_r, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.55).move_to([c[0], c[1], 0])
    g = VGroup(d, halo, bead)
    g.halo, g.bead = halo, bead
    return g


def scatter_pts(n, seed, c=DISH_C, rmin=1.5, rmax=2.9):
    rnd = random.Random(seed)
    pts = []
    for i in range(n):
        a = 2 * np.pi * (i + rnd.uniform(-0.25, 0.25)) / n
        r = rnd.uniform(rmin, rmax)
        pts.append([c[0] + r * np.cos(a), c[1] + r * np.sin(a), 0])
    return pts


def ring_pts(n, c=DISH_C, r=0.95):
    return [[c[0] + r * np.cos(2 * np.pi * i / n + 0.3), c[1] + r * np.sin(2 * np.pi * i / n + 0.3), 0] for i in range(n)]


def bead_label():
    a = T("bead soaked", 26, TEAL)
    b = T("in CXCL12", 26, TEAL)
    g = VGroup(a, b).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
    g.move_to([2.7 + g.width / 2, 0.0, 0])
    return g


class S20Beads(SpokenScene):
    def construct(self):
        lane = lane_rect(0.3, 0.9, -5.5, 5.5, ORANGE, 0.16)
        lw = lab_left("lane", 26, GREY, 5.0, 1.2)
        cs = VGroup(*[cell().move_to([x, 0.3, 0]) for x in (-4.4, -2.9, -1.4, 0.1, 1.6, 3.1)])
        self.add(lane, lw, cs)
        self.at("must leave")
        self.play(cs[2].animate.move_to([-1.4, -1.9, 0]), cs[4].animate.move_to([1.6, -1.9, 0]), run_time=1.0)
        d = dish()
        emb = chip("embryonic", ORANGE, 26).move_to([4.6, 1.8, 0])
        cells = VGroup(*[cell().move_to(p) for p in scatter_pts(9, 3)])
        bl = bead_label()
        self.at("embryonic interneurons")
        self.remove(lane, lw, cs)
        self.add(d, cells, emb)
        self.at("gathered near")
        rp = ring_pts(9)
        self.play(*[c.animate.move_to(p) for c, p in zip(cells, rp)], run_time=1.0)
        self.at("beads soaked")
        self.play(FadeIn(bl), Indicate(d.bead, color=TEAL, scale_factor=1.2), run_time=0.7)
        self.finish()


class S21Newborn(SpokenScene):
    def construct(self):
        d = dish()
        emb = chip("embryonic", ORANGE, 26).move_to([4.6, 1.8, 0])
        cells = VGroup(*[cell().move_to(p) for p in ring_pts(9)])
        bl = bead_label()
        self.add(d, emb, cells, bl)
        new = chip("newborn", ORANGE, 26).move_to([4.6, 1.8, 0])
        newc = VGroup(*[cell().move_to(p) for p in scatter_pts(9, 11)])
        self.play(FadeOut(cells), FadeIn(newc), ReplacementTransform(emb, new), run_time=0.6)
        self.at("newborn mice")
        rnd = random.Random(2)
        self.play(*[c.animate.shift([rnd.uniform(-0.3, 0.3), rnd.uniform(-0.3, 0.3), 0]) for c in newc], run_time=1.8)
        self.finish()


class S22Leave(SpokenScene):
    def construct(self):
        lane = lane_rect(0.0, 2.1, -6.4, 6.4, ORANGE, 0.14)
        dots = teal_dots(5, -6.2, 6.2, 0)
        rnd = random.Random(8)
        dots = VGroup(*[Dot([rnd.uniform(-6.2, 6.2), rnd.uniform(-0.95, 0.95), 0], radius=0.055, color=TEAL) for _ in range(34)])
        big = cell(ORANGE, 0.75, sw=3).move_to([-1.0, 0.0, 0])
        tabs = tabs_around([-1.0, 0], 0.75, [20, 60, 100, 140, 180, 220, 300, 340], PURPLE, w=0.16, h=0.3)
        self.add(lane, dots, big, tabs)
        prop = chip("proposed", GOLD, 26).move_to([4.6, -2.8, 0])
        self.add(prop)
        self.at("leave a lane")
        self.play(tabs.animate.set_opacity(0.12), run_time=.45)
        self.play(big.animate.move_to([-1.0, -2.6, 0]), tabs.animate.shift(DOWN * 2.6), run_time=.7)
        self.at("stop answering")
        self.play(Indicate(tabs,scale_factor=1.1),run_time=.3)
        self.finish()


class S22bAges(SpokenScene):
    def construct(self):
        cl, cr = (-3.6, 0.65), (3.6, 0.65)
        dl, dr = dish(cl, 2.2, 0.4), dish(cr, 2.2, 0.4)
        left = VGroup(*[cell(r=0.15).move_to(p) for p in ring_pts_c(8, cl, 0.75)])
        right = VGroup(*[cell(r=0.15).move_to(p) for p in scatter_pts(8, 4, cr, 1.2, 1.95)])
        ll = chip("embryonic", ORANGE, 24).move_to([cl[0], -2.05, 0])
        lr = chip("newborn", ORANGE, 24).move_to([cr[0], -2.05, 0])
        self.add(dl,dr,left,right,ll,lr,T("different ages",32).move_to([0,3.25,0]))
        arr = DashedLine([-1.1, 0.4, 0], [1.1, 0.4, 0], color=YELLOW, stroke_width=4).add_tip(tip_length=0.2)
        q = qmark(60, (0, 0.95))
        self.at("single cells")
        self.play(Create(arr), FadeIn(q, scale=0.6), run_time=0.7)
        fits = T("fits the idea", 32, TEXT)
        proof = T("— does not prove it", 32, TEXT)
        VGroup(fits, proof).arrange(RIGHT, buff=0.2).move_to([0, -2.95, 0])
        self.at("fits the idea")
        self.play(FadeIn(fits), run_time=0.5)
        self.at("does not prove")
        self.play(FadeIn(proof), run_time=0.5)
        self.finish()


def ring_pts_c(n, c, r):
    return ring_pts(n, c, r)


class S22cPlate(SpokenScene):
    def construct(self):
        w = wall()
        ls = lanes_big(op=0.12)
        cp = zlabel("cp", y=1.9)
        self.add(w, ls, cp)
        top = cell(r=0.24, tab=True, tabcolor=GOLD).move_to([-3.0, LANE_TOP, 0])
        deep = cell(r=0.24, tab=True, tabcolor=GOLD).move_to([-3.0, LANE_DEEP, 0])
        self.add(top, deep)
        rnd = random.Random(6)
        pdots = VGroup(*[Dot([rnd.uniform(-1.8, 2.5), rnd.uniform(0.6, 2.0), 0], radius=0.07, color=PINK) for _ in range(22)])
        nrg = zlabel("cp", PINK, "Neuregulin-3", y=1.0)
        self.at("also makes")
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in pdots], lag_ratio=0.03), FadeIn(nrg), run_time=1.2)
        ar_t = Arrow([-3.0, 0.95, 0], [-3.0, 2.35, 0], buff=0, color=PINK, stroke_width=7, tip_length=0.22)
        ar_d = Arrow([-3.0, 0.35, 0], [-3.0, -1.05, 0], buff=0, color=PINK, stroke_width=7, tip_length=0.22)
        self.at("attracts interneurons")
        self.play(GrowArrow(ar_t), GrowArrow(ar_d), run_time=0.9)
        erb_top = T("ErbB4",28,GOLD).move_to([-4.7,2.65,0])
        self.add(erb_top,Line(erb_top.get_right(),top.tab.get_center(),color=GOLD))
        erb = T("ErbB4", 28, GOLD).move_to([-1.2, -2.0, 0])
        ln = Line([-1.6, -1.85, 0], deep.tab.get_center() + DOWN * 0.05 + RIGHT * 0.03, color=GOLD, stroke_width=2)
        self.at("carry its receptor")
        self.play(FadeIn(erb), Create(ln), Indicate(deep.tab, color=GOLD, scale_factor=1.8), Indicate(top.tab, color=GOLD, scale_factor=1.8),
                  run_time=1.0)
        self.finish()


class S22dOpen(SpokenScene):
    def construct(self):
        c = cell(ORANGE, 2.3, sw=4).move_to([-3.8, 0.0, 0])
        tabs = tabs_around([-3.8, 0], 2.3, [20, 60, 100, 140, 180, 220, 300, 340], PURPLE, w=0.35, h=0.6).set_opacity(0.2)
        lab = T("CXCR4 dims", 26, PURPLE).move_to([-3.8, -3.2, 0])
        pull = Arrow([2.1, 0.2, 0], [6.1, 0.2, 0], buff=0, color=PINK, stroke_width=10, tip_length=0.4)
        pl = T("Neuregulin-3 pulls", 26, PINK).move_to([4.1, -1.0, 0])
        self.add(c, tabs, lab, pull, pl)
        q = qmark(180, (0.0, 0.2))
        self.at("the two")
        self.play(FadeIn(q, scale=0.5), run_time=0.6)
        self.at("still being worked")
        self.play(Indicate(q, color=YELLOW, scale_factor=1.2), run_time=0.8)
        self.finish()


class S23Turn(SpokenScene):
    def construct(self):
        w = wall()
        ls = lanes_big(op=0.12)
        cp = zlabel("cp", y=2.0)
        lines = VGroup(*[DashedLine([-6.4, y, 0], [2.7, y, 0], color=GREY, stroke_width=1.5, stroke_opacity=0.5) for y in (1.8, 1.2, 0.7)])
        self.add(w, ls, lines, cp)
        d = cell(r=0.22).move_to([-5.6, LANE_DEEP, 0])
        for x, y in ((-4.6, LANE_DEEP + 0.2), (-5.9, LANE_DEEP - 0.25), (-4.3, LANE_TOP), (-5.5, LANE_TOP)):
            self.add(cell().move_to([x, y, 0]))
        self.add(d)
        route = CubicBezier([-3.0, LANE_DEEP, 0], [-2.0, LANE_DEEP, 0], [-2.1, -0.2, 0], [-2.1, 1.2, 0])
        self.at("then the cells", lead=.6)
        self.play(d.animate.move_to([-3.0, LANE_DEEP, 0]), run_time=0.35, rate_func=linear)
        self.at("turn into the plate")
        self.play(MoveAlongPath(d, route), run_time=0.65)
        layer = lab_left("their layer", 28, TEXT, LX, 1.2)
        self.at("toward their layer")
        self.play(Indicate(d, color=ORANGE, scale_factor=1.6), FadeIn(layer), run_time=0.7)
        self.finish()


class S24Take(SpokenScene):
    def construct(self):
        l1 = T("Born outside the cortex, steered by", 40, TEXT, font=TITLE_FONT)
        l1b = T("what the cell can read.", 40, TEXT, font=TITLE_FONT)
        g1 = VGroup(l1, l1b).arrange(DOWN, buff=0.15).move_to([0, 1.8, 0])
        self.add(g1)
        l2 = T("In the lanes, chemokine signalling", 40, TEXT, font=TITLE_FONT)
        l2b = T("helps hold a cell in place.", 40, TEXT, font=TITLE_FONT)
        g2 = VGroup(l2, l2b).arrange(DOWN, buff=0.15).move_to([0, -1.3, 0])
        self.at("in the lanes")
        self.play(FadeIn(g2, shift=UP * 0.15), run_time=0.9)
        self.finish()


class S25End(EndCard):
    LINE = "Chemokine signalling helps keep interneurons in their lanes."
