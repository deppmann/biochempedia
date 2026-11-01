"""Netrin and DCC: one cue, two answers  (Biochemistrypedia explainer, developmental neuroscience)

COLOR MAP (one color per concept, whole video)
  YELLOW = netrin, the cue (source dot and its fading contours)
  BLUE   = the growth cone and its axon
  TEAL   = DCC receptor (cups on the growth cone surface)
  PURPLE = UNC5 receptor (cups)
  ORANGE = cyclic AMP inside the growth cone (dots)
  PINK   = antibody to DCC (caps that fill the DCC cups)
  GREEN  = attraction, the turn toward the source
  RED    = repulsion, the turn away; also a blocked signal
  GREY   = pipette, ghost arrows, outlines
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58BD0"

START = np.array([-1.0, -1.5, 0.0])
SRC = np.array([5.4, 0.4, 0.0])
R = 1.0  # growth cone radius


def bchip(text, color=BLUE, size=24, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def smooth(points):
    m = VMobject()
    m.set_points_smoothly([np.array(p, float) for p in points])
    return m


PATH_TOWARD = [START, [0.6, -1.25, 0], [2.2, -0.3, 0], [3.25, 0.3, 0]]
PATH_AWAY = [START, [-0.15, -1.1, 0], [-1.4, 0.1, 0], [-2.9, 0.9, 0], [-3.9, 1.3, 0]]
PATH_STRAIGHT = [START, [0.0, -1.5, 0], [1.0, -1.5, 0]]


def axon_in():
    return Line([-6.3, -1.5, 0], START, color=BLUE, stroke_width=11).set_z_index(-1)


def cups(center, angles, color, scale=1.0):
    out = VGroup()
    for deg in angles:
        phi = np.radians(deg)
        u = np.array([np.cos(phi), np.sin(phi), 0])
        c = center + (R * scale + 0.45 * scale) * u
        sw = 8 * max(scale, 0.6)
        out.add(Arc(radius=0.27 * scale, start_angle=phi + PI / 2, angle=PI, arc_center=c,
                    stroke_color=color, stroke_width=sw))
        out.add(Line(center + R * scale * u, center + (R + 0.18) * scale * u, color=color, stroke_width=sw * 0.8))
    return out


def caps(center, angles, scale=1.0):
    out = VGroup()
    for deg in angles:
        phi = np.radians(deg)
        u = np.array([np.cos(phi), np.sin(phi), 0])
        c = center + (R * scale + 0.45 * scale) * u
        out.add(Circle(radius=0.21 * scale, stroke_color=PINK, stroke_width=3, fill_color=PINK,
                       fill_opacity=0.95).move_to(c))
    return out


DCC_A = [30, 70, 110]
UNC_A = [-30, -70, -110]


def body(center, scale=1.0):
    bg = Circle(radius=R * scale, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(center)
    disc = Circle(radius=R * scale, stroke_color=BLUE, stroke_width=5, fill_color=BLUE, fill_opacity=0.25)
    disc.move_to(center)
    fil = VGroup()
    for deg in [0, 150, 180, 210]:
        phi = np.radians(deg)
        u = np.array([np.cos(phi), np.sin(phi), 0])
        fil.add(Line(center + R * scale * u, center + (R + 0.3) * scale * u, color=BLUE, stroke_width=4))
    return VGroup(bg, disc, fil)


DOT_OFFS = [(-0.3, 0.2), (0.0, 0.35), (0.25, 0.15), (-0.1, -0.1), (0.3, -0.2), (-0.35, -0.3), (0.05, -0.4)]


def dots(center, scale=1.0, live=True):
    g = VGroup()
    for dx, dy in DOT_OFFS:
        d = Circle(radius=0.095 * scale, stroke_color=ORANGE, stroke_width=2)
        if live:
            d.set_fill(ORANGE, 1)
        else:
            d.set_fill(ORANGE, 0).set_stroke(GREY, opacity=0.5)
        d.move_to(center + np.array([dx, dy, 0]) * 1.25 * scale)
        g.add(d)
    return g


def stage():
    """the netrin source and its fading contours"""
    arcs = VGroup()
    radii = [1.1, 2.3, 3.7, 5.2, 6.9, 8.7]
    ops = [0.95, 0.75, 0.58, 0.42, 0.3, 0.2]
    for r, o in zip(radii, ops):
        a = min(0.6, np.arcsin(min(1.0, 2.2 / r)))
        arc = Arc(radius=r, start_angle=PI - a, angle=2 * a, arc_center=SRC, stroke_color=YELLOW,
                  stroke_width=4, stroke_opacity=o).set_z_index(-2)
        arcs.add(arc)
    src = Circle(radius=0.3, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.95).move_to(SRC)
    lbl = T("netrin source", 24, YELLOW).move_to(SRC + DOWN * 0.8)
    return arcs, src, lbl


def pipette():
    p = Polygon([6.3, 2.5, 0], [6.05, 2.3, 0], [5.5, 0.62, 0], stroke_color=GREY, stroke_width=3,
                fill_color=GREY, fill_opacity=0.5)
    return p


def btext(text, size=26, color=GREY):
    t = T(text, size, color)
    back = Rectangle(width=t.width + 0.2, height=t.height + 0.14, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(t)
    return VGroup(back, t)


def banner(text, color):
    return T(text, 30, color, weight=BOLD).move_to([-1.6, 3.15, 0])


def run(self, mobs, path, t, rate=linear):
    """move a list of mobjects along a path while drawing the axon trail."""
    full = smooth(path).set_stroke(BLUE, 11).set_fill(opacity=0).set_z_index(-1)
    trail = full.copy()
    trail.pointwise_become_partial(full, 0, 0.001)
    self.add(trail)
    g = VGroup(*mobs)
    last = [np.array(path[0], float)]

    def step(m, a):
        a = max(a, 0.001)
        p = full.point_from_proportion(a)
        m.shift(p - last[0])
        last[0] = p
        trail.pointwise_become_partial(full, 0, a)

    self.play(UpdateFromAlphaFunc(g, step, rate_func=rate), run_time=t)
    return trail


class S00Title(TitleCard):
    LESSON = "Netrin and DCC"
    TITLE = "Netrin Guides Growing Axons"


def base_stage(self, with_axon=True):
    arcs, src, lbl = stage()
    self.add(arcs, src, lbl)
    axon = axon_in()
    self.add(axon)
    return arcs, src, lbl, axon

def mini(center, receptors, live=None):
    s = 0.65
    parts = VGroup(body(center, s))
    if "d" in receptors:
        parts.add(cups(center, DCC_A, TEAL, s))
    if "u" in receptors:
        parts.add(cups(center, UNC_A, PURPLE, s))
    if live is not None:
        parts.add(dots(center, s, live=live))
    return parts

def row(cx, y, receptors, live, toward, label, color):
    ic = mini(np.array([cx, y, 0]), receptors, live)
    if toward:
        ar = Arrow([cx + 1.05, y, 0], [cx + 2.5, y, 0], buff=0, color=GREEN, stroke_width=8)
    else:
        ar = Arrow([cx - 1.05, y, 0], [cx - 2.5, y, 0], buff=0, color=RED, stroke_width=8)
    tx = T(label, 26, color).move_to([cx, y - 1.3, 0])
    return VGroup(ic, ar, tx)

smooth_rate = rate_functions.ease_in_out_sine


# Tissue drawings are schematic cross-sections, not molecular structures.
def heading(text, color=TEXT):
    return T(text, 32, color, weight=BOLD).move_to([0, 3.2, 0])


def label(text, x, y, color=TEXT, size=24):
    return T(text, size, color).move_to([x, y, 0])


def cord(center, scale=1.0, wrong=False, progenitor=True, floor=True):
    c = np.array(center, float)
    def pt(x, y):
        return c + np.array([x, y, 0]) * scale
    outline = Ellipse(width=4.6*scale, height=4.5*scale, color=GREY, stroke_width=3).move_to(c)
    mid = DashedLine(pt(0, 2.15), pt(0, -2.15), color=GREY, stroke_width=2)
    canal = Ellipse(width=.55*scale, height=1.5*scale, color=GREY, stroke_width=3).move_to(pt(0, .55))
    fp = RoundedRectangle(width=.65*scale, height=.28*scale, corner_radius=.06,
                          color=GREY, fill_color=GREY, fill_opacity=.3).move_to(pt(0, -2.05))
    progenitors = VGroup(*[Dot(pt(x, y), radius=.10*scale, color=GREY)
                           for x in [-.48, .48] for y in [.2, .65, 1.1]])
    deposits = VGroup(*[Dot(pt(x,y), radius=.075*scale, color=YELLOW)
                        for x,y in [(-2.02,.8),(-2.12,.25),(-2.0,-.4),(-1.7,-1.05),(-1.2,-1.62),(-.65,-1.9)]])
    fcue = VGroup(*[Dot(pt(x,-1.96), radius=.07*scale, color=YELLOW) for x in [-.2,0,.2]])
    points = [(-1.55,1.4),(-1.9,.55),(-1.7,-.65),(-.85,-1.62),(.4,-1.65),(1.55,-1.0)]
    if wrong:
        points = [(-1.55,1.4),(-1.65,.6),(-.7,.1),(-.95,.8),(-.25,1.35)]
    route = smooth([pt(x,y) for x,y in points]).set_stroke(BLUE, 6)
    tip = body(pt(*points[-1]), .15*scale)
    anatomy = VGroup(outline, mid, canal, fp, progenitors)
    cues = VGroup()
    if progenitor:
        cues.add(deposits)
    if floor:
        cues.add(fcue)
    return VGroup(anatomy, cues, route, tip)


def explant(pos, color=BLUE):
    return RoundedRectangle(width=.8, height=.9, corner_radius=.2, color=color,
                            fill_color=color, fill_opacity=.25).move_to(pos)


def bundles(x0, x1, y=0):
    return VGroup(*[smooth([[x0,y+d,0],[(x0+x1)/2,y+d*.75,0],[x1,y+d*.5,0]])
                   .set_stroke(BLUE, 5) for d in [-.26,0,.26]])


def dish(cx):
    return RoundedRectangle(width=5.8, height=3.6, corner_radius=.3, color=GREY,
                            fill_color=GREY, fill_opacity=.04).move_to([cx,0,0])


def clear(scene):
    scene.play(FadeOut(Group(*scene.mobjects)), run_time=.35)


class S01Question(SpokenScene):
    def construct(self):
        h = heading('Netrin guides growing axons')
        cue = bchip('netrin', YELLOW, 28).move_to([4.4,1.3,0])
        normal = cord([-2.3,0,0], .94, progenitor=False, floor=False)
        self.at('Netrin is a')
        self.play(FadeIn(h), FadeIn(cue), FadeIn(normal[0]), run_time=.7)
        self.at('developing spinal cord')
        nlabel = label('spinal cord · normal', -2.3,-2.7,BLUE)
        mid = label('ventral midline', 3.7,-1.7,GREY)
        self.play(FadeIn(nlabel), FadeIn(mid), run_time=.5)
        self.at('grow toward the midline')
        self.play(Create(normal[2]), FadeIn(normal[3]), run_time=2.0)
        self.at('Netrin helps guide')
        self.play(Indicate(normal[2], color=BLUE), run_time=.7)
        self.at('In mice lacking netrin')
        mutant = cord([3,0,0], .94, wrong=True, progenitor=False, floor=False)
        ml = label('mouse lacking netrin-1',3,-2.7,RED)
        self.play(FadeOut(cue), FadeOut(mid), FadeIn(mutant[0]), FadeIn(ml), run_time=.6)
        self.at('take wrong routes')
        self.play(Create(mutant[2]), FadeIn(mutant[3]), run_time=.8)
        self.at('several forebrain crossings')
        clear(self)
        h = heading('Forebrain · a separate comparison')
        normal_brain = VGroup(Ellipse(width=2,height=2.7,color=GREY).move_to([-4,.4,0]),
                              Ellipse(width=2,height=2.7,color=GREY).move_to([-1.8,.4,0]))
        missing = normal_brain.copy().shift(RIGHT*6)
        bridges = VGroup(*[Line([-3.3,y,0],[-2.5,y,0],color=BLUE,stroke_width=7) for y in [-.1,.5,1.1]])
        gaps = VGroup(*[Line([2.7,y,0],[2.9,y,0],color=BLUE,stroke_width=7) for y in [-.1,.5,1.1]],
                      *[Line([3.3,y,0],[3.5,y,0],color=BLUE,stroke_width=7) for y in [-.1,.5,1.1]])
        self.play(FadeIn(h),FadeIn(normal_brain),FadeIn(missing),FadeIn(bridges),FadeIn(gaps),
                  FadeIn(label('normal crossings',-2.9,-1.5,BLUE)),
                  FadeIn(label('crossings missing',3.1,-1.5,RED)),run_time=.6)
        self.at('How does this cue')
        clear(self)
        cone = body(np.array([0,0,0]),1.25)
        ax = Line([-5.8,0,0],[-1.25,0,0],color=BLUE,stroke_width=11)
        self.play(FadeIn(cone),Create(ax),FadeIn(heading('How does netrin guide the moving tip?')),
                  FadeIn(label('growth cone',0,-2,BLUE,30)),run_time=.7)
        self.finish()


class S01Evidence(SpokenScene):
    def construct(self):
        h = heading('Embryonic rat spinal cord · collagen gel')
        left, right = dish(-3.2), dish(3.2)
        lone = explant([-4.4,0,0])
        paired = explant([1.6,0,0])
        self.at('The first clue')
        self.play(FadeIn(h),Create(left),Create(right),run_time=.7)
        self.at('dorsal spinal cord alone')
        self.play(FadeIn(lone),FadeIn(paired),
                  FadeIn(label('dorsal explant',-4.4,1.2,BLUE)),
                  FadeIn(label('dorsal explant',1.7,1.2,BLUE)),run_time=.5)
        self.at('few or no axons')
        alone_result = label('few or no axons',-3.2,-2.3,GREY)
        self.play(FadeIn(alone_result),run_time=.5)
        self.at('floor plate nearby')
        fp = explant([5.1,0,0],GREY)
        fl = label('floor plate',5.1,1.2,GREY)
        self.play(FadeIn(fp),FadeIn(fl),run_time=.5)
        self.at('axon bundles grew toward')
        ax = bundles(2.05,4.15)
        self.play(Create(ax),run_time=1.15)
        self.at('pieces never touched')
        gap = VGroup(Line([4.2,-.8,0],[4.65,-.8,0],color=TEXT,stroke_width=3),
                     label('gap',4.4,-1.2,TEXT,22))
        self.play(FadeIn(gap),run_time=.45)
        self.at('Something crossed the gel')
        moving = Dot([4.6,.65,0],color=YELLOW,radius=.1)
        self.play(FadeIn(moving),run_time=.2)
        self.play(moving.animate.move_to([2.1,.65,0]),run_time=.8)
        self.play(FadeOut(moving),run_time=.2)
        self.at('cells made to secrete')
        cells = VGroup(*[Circle(radius=.2,color=GREY,fill_color=GREY,fill_opacity=.4)
                       .move_to([5.1+dx,dy,0]) for dx,dy in [(-.16,0),(.15,.2),(.15,-.2)]])
        self.play(ReplacementTransform(fp,cells),ReplacementTransform(fl,label('netrin cells',5,1.2,YELLOW)),
                  FadeOut(gap),run_time=.6)
        self.at('at a distance')
        self.play(FadeIn(label('Culture: attraction at a distance',0,-3.1,GREEN,28)),run_time=.5)
        self.finish()


class S01Local(SpokenScene):
    def construct(self):
        tissue = cord([-1,0,0],1.05)
        self.at('But in the mouse embryo')
        self.play(FadeIn(heading('Mouse embryo · local presentation')),
                  FadeIn(tissue[0]),run_time=.65)
        fp_label = label('floor plate',-.9,-2.85,GREY)
        self.play(FadeIn(fp_label),run_time=.4)
        self.at('ventricular zone progenitors')
        pl = label('ventricular-zone\nprogenitors',3.9,1.6,GREY,26)
        ptr = Arrow([2.25,1.45,0],[-.4,.85,0],color=GREY,buff=.12)
        self.play(FadeIn(pl),GrowArrow(ptr),Indicate(tissue[0][4],color=GREY),run_time=.65)
        self.at('make netrin')
        packet = Dot([-.5,.8,0],color=YELLOW,radius=.13)
        self.play(FadeIn(packet),run_time=.3)
        self.at('lay it down')
        self.play(packet.animate.move_to([-3.12,.25,0]),run_time=.7)
        self.play(FadeOut(packet),FadeIn(tissue[1][0]),run_time=.4)
        pial = label('pial surface',-4.8,-2.3,GREY)
        pointer = Arrow([-4.35,-1.9,0],[-3,-.7,0],color=GREY,buff=.1)
        self.play(FadeIn(pial),GrowArrow(pointer),run_time=.45)
        self.at('along the')
        self.play(Create(tissue[2]),FadeIn(tissue[3]),run_time=1.0)
        self.at('The growth cone')
        self.play(FadeOut(ptr),FadeOut(pl),FadeIn(label('netrin beside the axon route',3.5,.7,YELLOW,24)),run_time=.4)
        self.play(Indicate(tissue[1][0],color=YELLOW,scale_factor=1.08),run_time=.8)
        self.finish()


class S01Sources(SpokenScene):
    def construct(self):
        self.at('Deleting netrin only')
        h = heading('Mouse · netrin source deletions')
        control = cord([-4.3,0,0],.68)
        no_floor = cord([0,0,0],.68,floor=False)
        no_prog = cord([4.3,0,0],.68,progenitor=False,wrong=True)
        self.play(FadeIn(h),FadeIn(control),FadeIn(no_floor[0]),FadeIn(no_floor[1]),
                  FadeIn(label('control',-4.3,2.1)),
                  FadeIn(label('floor plate deletion',0,2.1,RED)),run_time=.6)
        self.at('left most')
        self.play(Create(no_floor[2]),FadeIn(no_floor[3]),
                  FadeIn(label('most on course',0,-2,GREEN)),run_time=.9)
        self.at('Deleting it from those')
        self.play(FadeIn(no_prog[0]),FadeIn(no_prog[1]),
                  FadeIn(label('progenitor deletion',4.3,2.1,RED)),run_time=.55)
        self.at('caused errors')
        self.play(Create(no_prog[2]),FadeIn(no_prog[3]),FadeIn(label('routing errors',4.3,-2,RED)),run_time=.65)
        self.at('Later studies found')
        clear(self)
        tissue = cord([-2.8,0,0],.95)
        self.play(FadeIn(heading('Both netrin sources contribute')),FadeIn(tissue),run_time=.55)
        fl = label('floor plate netrin',3,1.3,YELLOW,28)
        pr = label('progenitor netrin',3,-1.1,YELLOW,28)
        self.at('still contributes')
        self.play(FadeIn(fl),Indicate(tissue[1][1],color=YELLOW),run_time=.6)
        self.at('working with progenitor')
        self.play(FadeIn(pr),Indicate(tissue[1][0],color=YELLOW),run_time=.6)
        self.at('So the dish shows')
        clear(self)
        self.play(FadeIn(heading('Two settings · complementary evidence')),
                  FadeIn(dish(-3.3)),FadeIn(explant([-4.7,0,0])),FadeIn(explant([-1.6,0,0],YELLOW)),
                  Create(bundles(-4.25,-2.45)),run_time=.65)
        self.play(FadeIn(label('Culture',-3.3,2.3)),
                  FadeIn(label('attraction at a distance',-3.3,-2.3,GREEN)),run_time=.4)
        self.at('The mouse shows')
        self.play(FadeIn(cord([3.4,0,0],.8)),FadeIn(label('Mouse embryo',3.4,2.3)),
                  FadeIn(label('local cue · cooperating sources',3.4,-2.3,YELLOW,22)),run_time=.7)
        self.finish()


class S02Attract(SpokenScene):
    def construct(self):
        center = np.array([-2.4,-.4,0])
        cone = body(center)
        receptors = cups(center,DCC_A,TEAL)
        src = Dot([4.8,.9,0],radius=.25,color=YELLOW)
        self.at('Now ask how')
        self.play(FadeIn(heading('How the growth cone reads netrin')),FadeIn(cone),
                  Create(Line([-6,-.4,0],[-3.4,-.4,0],color=BLUE,stroke_width=11)),
                  FadeIn(src),FadeIn(label('netrin',4.8,.1,YELLOW)),run_time=.7)
        self.at('Receptors on its surface')
        self.play(LaggedStart(*[GrowFromCenter(c) for c in receptors],lag_ratio=.1),run_time=.7)
        self.at('One receptor is called')
        tag = label('DCC',-2.4,1.7,TEAL,30)
        self.play(FadeIn(tag),run_time=.5)
        self.at('usually mediates attraction')
        path = [center,[-1,-.3,0],[.6,.3,0],[2.1,.8,0]]
        self.play(FadeOut(tag),run_time=.2)
        run(self,[cone,receptors],path,1.25,rate=rate_functions.ease_in_out_sine)
        self.play(FadeIn(label('DCC: usually attraction',0,-2.3,GREEN,28)),run_time=.4)
        self.at('Netrin binds cells')
        clear(self)
        self.play(FadeIn(heading('Separate assays: binding and outgrowth')),run_time=.35)
        cell_c = np.array([-3.6,.4,0])
        cell = VGroup(body(cell_c,.65),cups(cell_c,DCC_A,TEAL,.65))
        bound = Dot([-2.1,1.4,0],color=YELLOW,radius=.15)
        self.play(FadeIn(cell),FadeIn(label('DCC-displaying cells',-3.6,2.1,TEAL)),FadeIn(bound),run_time=.45)
        self.play(bound.animate.move_to(cell_c + np.array([.32,.88,0])),run_time=.7)
        self.play(FadeIn(label('netrin binding',-3.6,-1.4,YELLOW)),run_time=.4)
        self.at('an antibody to')
        tissue = explant([3,.35,0])
        ab = bchip('anti-DCC',PINK,26).move_to([3,1.9,0])
        netrin = bchip('netrin',YELLOW,24).move_to([5,.35,0])
        self.play(FadeIn(tissue),FadeIn(ab),FadeIn(netrin),run_time=.6)
        self.at('blocks')
        stop = Line([3.7,-.15,0],[3.7,.85,0],color=PINK,stroke_width=7)
        self.play(Create(stop),run_time=.4)
        self.at('outgrowth from spinal')
        self.play(FadeIn(label('outgrowth blocked',3.4,-1.4,PINK)),
                  FadeIn(label('spinal-cord explant',3.4,-2.2,BLUE)),run_time=.5)
        self.finish()


class S03Repel(SpokenScene):
    def construct(self):
        self.at('UNC5 receptors')
        h = heading('Worm touch neurons · add UNC5',PURPLE)
        before = body(np.array([-3.3,-.4,0]),.65)
        after_c = np.array([3.3,-.4,0])
        after = body(after_c,.65)
        unc = cups(after_c,UNC_A,PURPLE,.65)
        cue = VGroup(Line([-5.9,-2.2,0],[5.9,-2.2,0],color=YELLOW,stroke_width=5),
                     label('ventral UNC-6 = worm netrin',0,-2.85,YELLOW,26))
        # The untreated touch axon runs longitudinally, not dorsally toward/away from UNC-6.
        old_axon = Line([-5.8,-.4,0],[-3.95,-.4,0],color=BLUE,stroke_width=7)
        self.play(FadeIn(h),FadeIn(cue),run_time=.6)
        self.at('In worms')
        self.play(FadeIn(before),Create(old_axon),FadeIn(after),
                  FadeIn(label('before UNC5 expression',-3.4,2.1,GREY)),
                  FadeIn(label('after UNC5 expression',3.3,2.1,PURPLE)),run_time=.6)
        self.at('forcing this receptor')
        self.play(FadeIn(unc),run_time=.6)
        self.at('axons away from the cue')
        path = [after_c,[3.45,-.1,0],[3.6,.45,0],[3.6,1.05,0]]
        run(self,[after,unc],path,.85)
        self.at('The cue stayed the same')
        self.play(Indicate(cue,color=YELLOW,scale_factor=1.02),run_time=.65)
        self.at('Changing the receptor')
        self.play(Indicate(unc,color=PURPLE,scale_factor=1.12),run_time=.65)
        self.at('Treat this as a starting')
        clear(self)
        self.play(FadeIn(heading('A starting point')),
                  FadeIn(bchip('DCC: usually attraction',TEAL,30).move_to([0,1.5,0])),
                  FadeIn(bchip('UNC5: repulsion',PURPLE,30).move_to([0,.1,0])),run_time=.6)
        self.at('can also take part')
        self.play(FadeIn(label('Repulsion can also involve DCC',0,-1.3,TEAL,28)),run_time=.6)
        self.at('other receptors and partners')
        self.play(FadeIn(label('Other receptors and partners also matter',0,-2.6,GREY,26)),run_time=.6)
        self.finish()


class S04Inside(SpokenScene):
    def construct(self):
        center = START.copy()
        cone,dcc,ds = body(center),cups(center,DCC_A,TEAL),dots(center)
        _,src,nl = stage()
        self.at('One smaller point')
        h = heading('Smaller point: cultured frog spinal growth cones')
        self.play(FadeIn(h),FadeIn(cone),FadeIn(dcc),FadeIn(ds),Create(axon_in()),
                  FadeIn(pipette()),FadeIn(src),FadeIn(nl),run_time=.7)
        self.at('frog spinal growth cones')
        trail = run(self,[cone,dcc,ds],PATH_TOWARD,1.4,rate=rate_functions.ease_in_out_sine)
        on = label('cAMP signalling · attraction',0,-3.1,GREEN,26)
        self.play(FadeIn(on),run_time=.4)
        self.at('Blocking cyclic')
        # Reset the prior turn and its result together before the blocked case.
        self.play(FadeOut(cone),FadeOut(dcc),FadeOut(ds),FadeOut(trail),FadeOut(on),run_time=.25)
        cone,dcc,ds = body(center),cups(center,DCC_A,TEAL),dots(center,live=False)
        blocked = bchip('cAMP signalling blocked',ORANGE,26).move_to([-1,1.2,0])
        self.play(FadeIn(cone),FadeIn(dcc),FadeIn(ds),FadeIn(blocked),run_time=.4)
        self.at('into repulsion')
        self.play(FadeOut(blocked), run_time=.2)
        run(self,[cone,dcc,ds],PATH_AWAY,1.05,rate=rate_functions.ease_in_out_sine)
        self.play(FadeIn(label('repulsion',0,-3.1,RED,28)),run_time=.25)
        self.at('An antibody to')
        clear(self)
        self.play(FadeIn(heading('Anti-DCC blocks both turns',PINK)),run_time=.3)
        groups = []
        for y,live,txt in [(1.1,True,'cAMP signalling'),(-1.35,False,'cAMP blocked')]:
            p = np.array([-.8,y,0])
            g = VGroup(body(p,.62),cups(p,DCC_A,TEAL,.62),dots(p,.62,live=live),caps(p,DCC_A,.62))
            groups.append(g)
            self.play(FadeIn(g),FadeIn(label(txt,-4.3,y,ORANGE,26)),run_time=.3)
        self.at('stopped both turns')
        self.play(*[g.animate.shift(RIGHT*1.1) for g in groups],
                  FadeIn(label('no turn',3,1.1,PINK,28)),FadeIn(label('no turn',3,-1.35,PINK,28)),run_time=.8)
        self.at('This is a worked example')
        self.play(FadeIn(label('Worked example in this assay',0,-2.6,TEXT,27)),run_time=.5)
        self.at('not a rule for every axon')
        self.play(FadeIn(label('Not a universal prediction rule',0,-3.3,GREY,24)),run_time=.5)
        self.finish()


class S07End(EndCard):
    LINE = "Netrin guides axons; local presentation and receptor context shape the response."
