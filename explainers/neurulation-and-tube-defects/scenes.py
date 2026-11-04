"""Neurulation and neural tube defects, chapter 1: Narrow First, Then Fold  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole series; same as scenes.old.py)
  BLUE   = the neural plate / neural folds / neural tube (the cells of the plate)
  ORANGE = skin (surface ectoderm / epidermis beside and over the plate)
  YELLOW = movement and reach: arrows, hinge point, step labels, the gap
  RED    = open, failed, too far apart
  GREEN  = meets, fused, closed, sealed (the seam of a closed tube)
  GREY   = labels, outlines, notochord, de-emphasised
  (TEAL = planar cell polarity: kept for later chapters, not used here)
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"


def sm(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def lab(text, color=TEXT, size=26, at=(0, 0), **kw):
    return T(text, size, color, **kw).move_to([at[0], at[1], 0])


def lab_l(text, color, size, xl, y):
    t = T(text, size, color)
    return t.move_to([xl + t.width / 2, y, 0])


def parr(p, q, color=YELLOW, w=7):
    return Arrow([p[0], p[1], 0], [q[0], q[1], 0], buff=0, color=color, stroke_width=w, tip_length=0.25,
                 max_tip_length_to_length_ratio=0.45)


def darr(p, q, color=YELLOW, w=6):
    return DoubleArrow([p[0], p[1], 0], [q[0], q[1], 0], buff=0, color=color, stroke_width=w, tip_length=0.25,
                       max_tip_length_to_length_ratio=0.3)


def dline(p, q, color=GREY, w=3):
    return DashedLine([p[0], p[1], 0], [q[0], q[1], 0], color=color, stroke_width=w, dash_length=0.12)


def flash(scene, pt, color=GREEN, r=0.7):
    ring = Circle(radius=0.12, color=color, stroke_width=7).move_to([pt[0], pt[1], 0])
    scene.add(ring)
    scene.play(ring.animate.scale(r / 0.12).set_stroke(opacity=0), run_time=0.6)
    scene.remove(ring)


# ---------------------------------------------------------------------------------------------
# cross-section of the embryo's back (computed from circular-arc geometry, plate length L is conserved)
# ---------------------------------------------------------------------------------------------
def XS(L, phi, thick=14, sep=0.0, seal=0.0, cx=0.0, cy=0.0, half=6.2, nz=1.0, skin_w=11):
    """Plate of arc length L bent through half-angle phi (0 = flat, pi = closed circle). The hinge sinks as the
    folds rise. sep sinks the closed tube under the skin; seal flattens the skin over it. cy = skin level."""
    phi = max(phi, 0.03)
    r = L / (2 * phi)
    ts = np.linspace(-phi, phi, 80)
    yh = -r * (1 - np.cos(phi)) / 2
    D = L / (2 * np.pi) + 0.2 + thick / 100.0
    xs = r * np.sin(ts)
    ys = yh + r * (1 - np.cos(ts)) - sep * D
    pts = np.array([[cx + x, cy + y, 0] for x, y in zip(xs, ys)])
    plate = VMobject(stroke_color=BLUE, stroke_width=thick, fill_opacity=0).set_points_smoothly(pts)
    xt = abs(xs[-1]) + (0.55 if phi > 0.1 else 0.12) * (1-seal)
    yt = (yh + r * (1 - np.cos(phi)) + (0.16 if phi > 0.1 else 0)) * (1 - seal)
    mid = xt + 0.3 * (half - xt)
    sl = VMobject(stroke_color=ORANGE, stroke_width=skin_w).set_points_as_corners(
        np.array([[cx - half, cy, 0], [cx - mid, cy, 0], [cx - xt, cy + yt, 0]]))
    sr = VMobject(stroke_color=ORANGE, stroke_width=skin_w).set_points_as_corners(
        np.array([[cx + half, cy, 0], [cx + mid, cy, 0], [cx + xt, cy + yt, 0]]))
    low = yh - sep * D
    nh = 0.42 * nz
    noto = Ellipse(width=1.0 * nz, height=nh, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                   fill_opacity=0.28).move_to([cx, cy + low - thick / 200.0 - nh / 2 - 0.08, 0])
    g = VGroup(sl, sr, plate, noto)
    g.geo = dict(tipL=pts[0].copy(), tipR=pts[-1].copy(),
                 hinge=np.array([cx, cy + low, 0]), top=np.array([cx, cy + ys[0], 0]), noto=noto.get_center())
    return g


# ---------------------------------------------------------------------------------------------
# top view of the embryo's back (s01-s06)
# ---------------------------------------------------------------------------------------------
TVC = (-3.5, -0.1)


def embryo():
    return RoundedRectangle(width=3.5, height=5.6, corner_radius=1.3, stroke_color=GREY, stroke_width=3,
                            fill_color=ORANGE, fill_opacity=0.18).move_to([TVC[0], TVC[1], 0])


def plate(pw, ph, color=BLUE):
    return RoundedRectangle(width=pw, height=ph, corner_radius=pw * 0.45, stroke_color=color, stroke_width=4,
                            fill_color=color, fill_opacity=0.5).move_to([TVC[0], TVC[1], 0])


# ---------------------------------------------------------------------------------------------
# top view of the whole tube (s11-s17, s23): fold edges, zipper sites, map of the sealed tube
# ---------------------------------------------------------------------------------------------
SITES = [(1.05, 1.1), (2.45, 0.6), (3.18, 0.25)]   # (y of site, spreading reach); site 0 = Closure 1
YT, YB = 3.45, -3.1


def wprof(y):
    if y >= 2.3:
        return 0.95 * np.sqrt(max(0.0, 1 - ((y - 2.3) / 1.15) ** 2))
    if y >= 1.0:
        return 0.42 + 0.53 * sm((y - 1.0) / 1.3)
    if y >= -2.7:
        return 0.42
    return 0.42 * np.sqrt(max(0.0, 1 - ((-2.7 - y) / 0.4) ** 2))


def zf(y, p, opens):
    f = 1.0
    for ys, E in SITES:
        f = min(f, sm((abs(y - ys) - p * E) / 0.35))
    for y0, y1, a in opens:
        win = sm((y - (y0 - 0.2)) / 0.4) * sm(((y1 + 0.2) - y) / 0.4)
        f = max(f, a * win)
    return f


class TV:
    def __init__(s, sx=2.6, sy=1.0, cx=-2.6, cy=0.0):
        s.sx, s.sy, s.cx, s.cy = sx, sy, cx, cy

    def P(s, x, y):
        return np.array([s.cx + x * s.sx, s.cy + y * s.sy, 0])

    def sil(s):
        ys = np.linspace(YT, YB, 140)
        pts = [s.P(wprof(y), y) for y in ys] + [s.P(-wprof(y), y) for y in ys[::-1]]
        pts.append(pts[0])
        return VMobject(stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.4).set_points_as_corners(np.array(pts))

    def seam(s):
        return Line(s.P(0, -2.95), s.P(0, 3.35), color=GREEN, stroke_width=9)

    def gap(s, p=10.0, opens=()):
        ys = np.linspace(YT, YB, 160)
        g = [0.78 * wprof(y) * zf(y, p, opens) for y in ys]
        pts = [s.P(-gg, y) for gg, y in zip(g, ys)] + [s.P(gg, y) for gg, y in zip(g[::-1], ys[::-1])]
        pts.append(pts[0])
        return VMobject(fill_color=BG, fill_opacity=1, stroke_width=0).set_points_as_corners(np.array(pts))

    def edges(s, opens):
        out = []
        for y0, y1, a in opens:
            ys = np.linspace(y1, y0, 50)
            for sg in (-1, 1):
                pts = [s.P(sg * 0.78 * wprof(y) * zf(y, 10, opens), y) for y in ys]
                out.append(VMobject(stroke_color=RED, stroke_width=5, stroke_opacity=min(1, a)).set_points_as_corners(np.array(pts)))
        return VGroup(*out)

    def dots(s, idx=(0, 1, 2)):
        return VGroup(*[Dot(s.P(0, SITES[i][0]), radius=0.14, color=GREEN) for i in idx])


MAP = TV(sx=2.0, cx=-1.9)


# All cross-section traces below come from XS circular-arc geometry.
# Trackers redraw the model each frame; no interpolation between unrelated paths.
STEP_Y = 3.25
ZOOM_CY = 0.1
CY_END = 1.1
ZL, ZT, ZNZ = 8.4, 78, 1.5


def zxs(phi, sep=0, seal=0, cy=ZOOM_CY):
    return XS(ZL, phi, ZT, sep, seal, cy=cy, half=6.0, nz=ZNZ)


def leader(text, point, pos, color=TEXT, size=30):
    t = lab(text, color, size, pos)
    start = t.get_left() if point[0] < pos[0] else t.get_right()
    if abs(point[0]-pos[0]) < 0.5:
        start = t.get_bottom() if point[1] < pos[1] else t.get_top()
    return VGroup(Line(start, point, color=color, stroke_width=2.5, buff=0.12), t)


def step(n, name):
    return lab(f"Step {n} · {name}", YELLOW, 40, (0, STEP_Y))


def noto_label(xs, pos=(3.9, -2.5)):
    return leader("notochord", xs.geo["noto"], pos, GREY, 28)


class S00Title(TitleCard):
    LESSON = "Neurulation and Neural Tube Defects"
    TITLE = "Narrow First, Then Fold"

    def construct(self):
        g = VGroup(T("BIOCHEMISTRYPEDIA", 26, TEAL),
                   T(self.LESSON, 28, GREY),
                   T(self.TITLE, 52, TEXT, font=TITLE_FONT)).arrange(DOWN, buff=0.5).move_to(ORIGIN)
        self.play(FadeIn(g), run_time=0.7)
        self.finish()


class S01Q(SpokenScene):
    def construct(self):
        emb, pl = embryo(), plate(1.8, 4.2)
        # The sheet occupies the left half; the question occupies the right from the first frame.
        q = lab("How does a sheet\nbecome a sealed tube?", TEXT, 36, (2.8, 0.5))
        flat = leader("flat sheet of cells", (-3.5, 1.1, 0), (-0.9, 2.65), BLUE, 30)
        self.add(emb, pl, q)
        self.at("a flat sheet")
        self.play(FadeIn(flat), run_time=0.45)
        self.at("fourth week")
        time = VGroup(Line([0.3,-1.3,0], [5.8,-1.3,0], color=YELLOW, stroke_width=6),
                      Line([0.3,-1.1,0], [0.3,-1.5,0], color=YELLOW),
                      Line([5.8,-1.1,0], [5.8,-1.5,0], color=YELLOW),
                      lab("week 3", TEXT, 30, (0.6,-1.9)),
                      lab("about week 4", YELLOW, 30, (4.8,-1.9)),
                      lab("after fertilization", GREY, 28, (3,-2.65)))
        self.play(FadeIn(time), run_time=0.6)
        self.at("sealed tube")
        self.play(Indicate(q, color=YELLOW, scale_factor=1.02), run_time=0.5)
        self.finish()


class S02Plate(SpokenScene):
    def construct(self):
        emb = embryo().stretch(1.16, 0).shift(RIGHT*.35)
        pl = plate(1.8, 4.2).shift(RIGHT*.35)
        xs = XS(4.4, .03, 150, cx=3.2, cy=.1, half=3, nz=2.2)
        orientation = lab("dorsal side up ↑", TEXT, 30, (3.2, 2.7))
        self.add(emb, pl, orientation)
        self.at("neural plate")
        nl = leader("neural plate", (-3.15,1.5,0), (-3.15,3.25), BLUE, 32)
        self.play(FadeIn(nl), run_time=.4)
        self.at("the midline")
        ml = DashedLine([-3.15,1.8,0],[-3.15,-2.1,0], color=TEXT, stroke_width=2)
        mlab = lab("midline · embryo’s back", TEXT, 28, (-3.15,-3.25))
        self.play(FadeIn(ml), FadeIn(mlab), run_time=.4)
        self.at("on either side")
        plane = Line([-5.4,-1.5,0],[-.9,-1.5,0], color=YELLOW, stroke_width=4)
        self.add(plane)
        self.play(plane.animate.shift(UP*2.8), FadeIn(xs, shift=DOWN*.65), run_time=.9)
        self.play(FadeOut(plane), run_time=.2)
        self.at("surface ectoderm")
        ect = leader("ectoderm\n(future skin)", (5.8,.1,0), (4.9,1.65), ORANGE, 28)
        neural = leader("neural plate", (3.2,.2,0), (1.6,1.65), BLUE, 28)
        nt = noto_label(xs, (3.8,-2.4))
        self.play(FadeIn(ect), FadeIn(neural), FadeIn(nt), run_time=.55)
        self.finish()


def shaping_state():
    return embryo(), plate(.8,4.8), XS(3.0,.03,190,cx=3.2,cy=0,half=3,nz=2.0)


class S05Shape(SpokenScene):
    def construct(self):
        emb, pl = embryo(), plate(1.8,3.2)
        xs = XS(4.6,.03,65,cx=3.2,cy=0,half=3,nz=2.0)
        hdr = step(1,"Shaping")
        self.add(emb,pl,xs,hdr)
        self.at("grow taller")
        taller = VGroup(parr((2.3,.5),(2.3,1.65)),parr((4.1,.5),(4.1,1.65)),
                        lab("taller cells", BLUE,30,(3.2,2.15)))
        self.play(Transform(xs,XS(4.6,.03,190,cx=3.2,cy=0,half=3,nz=2.0)), FadeIn(taller),run_time=.75)
        self.at("narrows from side")
        ins = VGroup(parr((-5.1,0),(-4.15,0)),parr((-1.9,0),(-2.85,0)))
        self.play(Transform(pl,plate(.8,3.2)),Transform(xs,shaping_state()[2]),FadeOut(taller),FadeIn(ins),run_time=.8)
        self.at("lengthens from head")
        length = darr((-1.05,-1.7),(-1.05,1.5))
        ends = VGroup(lab("head",TEXT,28,(-.25,2.5)),lab("tail",TEXT,28,(-.25,-2.65)))
        self.add(length)
        self.play(Transform(pl,plate(.8,4.8)),FadeOut(ins),
                  Transform(length,darr((-1.05,-2.5),(-1.05,2.3))),FadeIn(ends),run_time=1.1)
        self.finish()


class S06Hold(SpokenScene):
    def construct(self):
        emb,pl,xs = shaping_state()
        hdr = step(1,"Shaping")
        self.add(emb,pl,xs,hdr)
        self.at("hold on")
        box=SurroundingRectangle(hdr,color=YELLOW,buff=.15)
        self.play(FadeIn(box),run_time=.35)
        self.at("stays wide")
        ghost=DashedVMobject(plate(1.8,4.8,RED).set_fill(opacity=0),num_dashes=40)
        gl=lab("if it stays this wide",RED,28,(-3.5,-3.2))
        self.play(FadeIn(ghost),FadeIn(gl),run_time=.45)
        self.at("the folds may")
        # A wide midline with two bent flanks: the central span prevents contact.
        def wide_fold(b):
            # A broad floor and two circular flanks with tips that visibly turn inward.
            theta=np.linspace(0,2.1*b+.03,60)
            radius=1.8
            left=np.array([[2.0-radius*np.sin(t),-1.5+radius*(1-np.cos(t)),0] for t in theta])[::-1]
            right=left[::-1].copy();right[:,0]=6.4-right[:,0]
            middle=np.array([[x,-1.5,0] for x in np.linspace(2.0,4.4,30)])
            trace=VMobject(stroke_color=BLUE,stroke_width=65).set_points_as_corners(np.concatenate([left,middle,right]))
            return VGroup(trace,Ellipse(width=1.4,height=.6,color=GREY,fill_opacity=.25).move_to([3.2,-2.4,0]))
        bend=ValueTracker(0)
        self.remove(xs)
        folded=always_redraw(lambda:wide_fold(bend.get_value()))
        self.add(folded)
        self.play(bend.animate.set_value(1),run_time=.85)
        self.at("too far to go")
        reach=VGroup(darr((.45,1.8),(5.95,1.8),RED),lab("too far to reach",RED,30,(3.2,2.45)))
        self.play(FadeIn(reach),run_time=.4)
        self.finish()


class S07Bend(SpokenScene):
    def construct(self):
        phi=ValueTracker(.03)
        xs=always_redraw(lambda:zxs(phi.get_value()))
        self.add(xs,step(2,"Bending"))
        self.at("creases at")
        self.play(phi.animate.set_value(.5),run_time=.8)
        self.at("hinge points")
        hinge=leader("hinge point",zxs(.5).geo["hinge"],(-1.5,-1.5),YELLOW,28)
        self.play(FadeIn(hinge),run_time=.3)
        self.at("edges rise")
        self.play(phi.animate.set_value(1.55),FadeOut(hinge),run_time=1.0)
        self.at("folds")
        end=zxs(1.55)
        labels=VGroup(leader("neural folds",end.geo["tipL"],(-4.4,2.3),BLUE,30),
                      leader("neural folds",end.geo["tipR"],(4.4,2.3),BLUE,30),noto_label(end))
        self.play(FadeIn(labels),run_time=.35)
        self.finish()


class S08Fuse(SpokenScene):
    def construct(self):
        phi=ValueTracker(1.55)
        xs=always_redraw(lambda:zxs(phi.get_value()))
        nt=noto_label(zxs(1.55))
        fold_labels=VGroup(leader("neural folds",zxs(1.55).geo["tipL"],(-4.4,2.3),BLUE,30),
                           leader("neural folds",zxs(1.55).geo["tipR"],(4.4,2.3),BLUE,30))
        self.add(xs,step(3,"Meeting and fusion"),nt,fold_labels)
        self.at("move toward")
        arr=VGroup(parr((-3.1,2.25),(-1.4,2.25)),parr((3.1,2.25),(1.4,2.25)))
        self.play(FadeIn(arr),phi.animate.set_value(2.75),FadeOut(nt),FadeOut(fold_labels),run_time=1.0)
        self.at("meet")
        self.play(phi.animate.set_value(PI),FadeOut(arr),run_time=.55)
        self.at("fuse")
        top=zxs(PI).geo["top"]
        seam=VGroup(Dot(top,radius=.12,color=GREEN),leader("fusion seam",top,(3.6,2),GREEN,30),noto_label(zxs(PI)))
        self.play(FadeIn(seam),run_time=.35)
        self.finish()


class S09Sep(SpokenScene):
    def construct(self):
        sep,seal=ValueTracker(0),ValueTracker(0)
        xs=always_redraw(lambda:zxs(PI,sep.get_value(),seal.get_value(),ZOOM_CY+sep.get_value()))
        top=zxs(PI).geo["top"]
        seam=leader("fusion seam",top,(3.6,2),GREEN,30)
        self.add(xs,seam,step(4,"Separation"))
        self.at("tube separates")
        self.play(sep.animate.set_value(1),FadeOut(seam),run_time=1.2)
        self.at("seals over")
        self.play(seal.animate.set_value(1),run_time=.85)
        final=zxs(PI,1,1,CY_END)
        labels=VGroup(leader("epidermis seals over",(0,CY_END,0),(2.7,2.2),ORANGE,30),
                      leader("neural tube",(1.35,-.9,0),(4,-.7),BLUE,30),noto_label(final,(3.5,-2.8)))
        self.play(FadeIn(labels),run_time=.35)
        self.finish()


def map_labels():
    return VGroup(lab("mouse · top view",TEXT,34,(3.25,3.2)),
                  leader("head",MAP.P(0,YT),(-4.9,3.1),TEXT,28),
                  leader("tail",MAP.P(0,YB),(-4.5,-3),TEXT,28))


def map_base(p=.7,opens=(),tv=MAP):
    return VGroup(tv.sil(),tv.seam(),tv.gap(p,opens),tv.edges(opens))


def centered_map_labels():
    m=TV(sx=2,cx=0)
    return VGroup(lab("mouse · top view",TEXT,32,(4.4,3.2)),
                  leader("head",m.P(0,YT),(-4.5,3.1),TEXT,28),
                  leader("tail",m.P(0,YB),(-4.5,-3),TEXT,28))


class S11Zip(SpokenScene):
    def construct(self):
        m=TV(sx=2,cx=0)
        p=ValueTracker(-1.5)
        gap=always_redraw(lambda:m.gap(p.get_value()))
        self.add(m.sil(),m.seam(),gap)
        self.at("look from above")
        self.play(FadeIn(centered_map_labels()),run_time=.4)
        self.at("the mouse")
        self.play(FadeIn(lab("Closure spreads\nlike a zipper",TEXT,30,(4.4,-.5))),run_time=.35)
        self.at("begins at several sites")
        dots=m.dots()
        c1=leader("first site",m.P(0,SITES[0][0]),(4.2,1.4),GREEN,30)
        self.play(FadeIn(dots[0]),FadeIn(c1),p.animate.set_value(0),run_time=.45)
        self.play(FadeIn(dots[1]),run_time=.25)
        self.play(FadeIn(dots[2]),run_time=.25)
        self.at("spreads from each")
        self.play(p.animate.set_value(.7),run_time=1.25,rate_func=linear)
        self.finish()


def c1_labels():
    y=SITES[0][0]
    # Hindbrain is immediately cranial to Closure 1, midbrain is at y=2.4.
    c1=leader("Closure 1",MAP.P(0,y),(2.2,y),GREEN,34)
    hb=leader("hindbrain",MAP.P(.5,1.55),(2.7,2.1),TEXT,30)
    sc=leader("spinal cord",MAP.P(.4,-.8),(2.7,-1),TEXT,30)
    return VGroup(c1,hb,sc)


class S12C1(SpokenScene):
    def construct(self):
        m=TV(sx=2,cx=0)
        base,labels,ds=map_base(tv=m),centered_map_labels(),m.dots()
        self.add(base,labels,ds)
        c,h,s=c1_labels()
        self.at("first site")
        self.play(Transform(base,map_base()),Transform(labels,map_labels()),Transform(ds,MAP.dots()),run_time=.4)
        self.play(Indicate(ds[0],color=YELLOW,scale_factor=2),run_time=.35)
        self.at("closure one")
        self.play(FadeIn(c),run_time=.35)
        self.at("hindbrain")
        self.play(FadeIn(h),run_time=.35)
        self.at("spinal cord")
        self.play(FadeIn(s),run_time=.35)
        self.finish()


class S13Beat(NarratedScene):
    def construct(self):
        labels=c1_labels()
        self.add(map_base(),map_labels(),MAP.dots(),labels)
        self.play(Indicate(labels[0],color=YELLOW,scale_factor=1.04),run_time=1.5)
        self.finish()


def defect_labels(tv=MAP):
    return VGroup(leader("head end",tv.P(0,YT),(-4.8,3.15),TEXT,28),
                  leader("lower end",tv.P(0,YB),(-4.6,-3.1),TEXT,28),
                  lab("schematic\n(mouse-shaped, not human)",TEXT,26,(3,3.05)) if tv is MAP else
                  lab("schematic\n(mouse-shaped,\nnot human)",TEXT,24,(4.65,2.8)))


class S14Open(SpokenScene):
    def construct(self):
        m=TV(sx=2.9,sy=.96,cx=0,cy=-.1)
        op=[(-1.6,-.2,1)]
        self.add(map_base(10,op,tv=m),defect_labels(m))
        desc=leader("a stretch that\ndoes not close",m.P(.4,-.8),(4.1,.6),YELLOW,32)
        self.at("a stretch")
        box=DashedVMobject(RoundedRectangle(width=2.1,height=1.8,color=YELLOW),num_dashes=28).move_to(m.P(0,-.9))
        self.play(FadeIn(box),FadeIn(desc),run_time=.5)
        self.at("stays open for")
        hold=lab("stays open\nfor the rest of pregnancy",RED,30,(4.1,-1.4))
        self.play(FadeIn(hold),run_time=.4)
        self.at("names the defect")
        self.play(Indicate(box,color=RED,scale_factor=1.05),run_time=.6)
        self.finish()


class S15Anen(SpokenScene):
    def construct(self):
        op=[(2,3.45,1)]
        self.add(map_base(10,op),defect_labels())
        self.at("head end fails")
        name=leader("anencephaly",MAP.P(.6,2.8),(3.2,1.9),RED,38)
        self.play(FadeIn(name),run_time=.4)
        self.at("exposed brain tissue")
        # Scalloped tissue, with separate edge pieces that fade away on 'degenerates'.
        tissue=VGroup(*[Ellipse(width=.95,height=.85,color=BLUE,fill_opacity=.65).move_to(MAP.P(x,y))
                         for x,y in [(-.35,2.55),(.15,2.6),(-.15,3.0)]])
        ex=leader("exposed brain tissue",MAP.P(.2,2.7),(3.1,.7),BLUE,30)
        self.play(FadeIn(tissue),FadeIn(ex),run_time=.5)
        self.at("degenerates")
        crumbs=VGroup(*[Dot(MAP.P(x,y),radius=.08,color=BLUE) for x,y in [(-.5,2.9),(.4,2.8),(.2,3.2)]])
        self.add(crumbs)
        self.play(tissue.animate.scale(.45).set_opacity(.18),crumbs.animate.shift(UP*.4).set_opacity(0),run_time=1.1)
        self.finish()


class S16Mmc(SpokenScene):
    def construct(self):
        op=[(-3.1,-1.6,1)]
        self.add(map_base(10,op),defect_labels())
        self.at("lower end fails")
        self.play(Indicate(MAP.edges(op),color=RED,scale_factor=1.03),run_time=.4)
        self.at("cord itself")
        cord=VMobject(stroke_color=BLUE,stroke_width=20).set_points_smoothly(np.array([
            MAP.P(0,-.9),MAP.P(.04,-1.7),MAP.P(-.08,-2.2),MAP.P(0,-2.75)]))
        cl=leader("spinal cord",MAP.P(0,-2.2),(2.8,-.5),BLUE,32)
        self.play(Create(cord),FadeIn(cl),run_time=.5)
        self.at("open lesion")
        ol=leader("open lesion",MAP.P(.34,-2.7),(2.8,-2.8),RED,30)
        self.play(FadeIn(ol),run_time=.35)
        self.at("this is")
        mm=leader("myelomeningocele",MAP.P(.35,-1.9),(2.6,1.5),RED,34)
        self.play(FadeIn(mm),run_time=.4)
        self.at("open form")
        self.play(FadeIn(lab("open spina bifida",RED,32,(2.9,.7))),run_time=.35)
        self.finish()


class S17Crr(SpokenScene):
    def construct(self):
        m=TV(sx=2.9,sy=.96,cx=0,cy=-.1)
        op=[(-3.1,2.4,1)]
        self.add(map_base(10,op,tv=m),lab("mouse · top view",TEXT,28,(4.5,3.25)))
        self.at("closure one")
        pt=m.P(0,SITES[0][0])
        c=leader("Closure 1",pt,(-4.9,1.1),RED,32)
        cross=VGroup(Line(pt+[-.25,-.25,0],pt+[.25,.25,0],color=RED,stroke_width=7),
                     Line(pt+[-.25,.25,0],pt+[.25,-.25,0],color=RED,stroke_width=7))
        self.play(FadeIn(c),run_time=.3)
        self.at("never happens")
        self.play(FadeIn(cross),run_time=.3)
        self.at("midbrain")
        mb=leader("midbrain",m.P(.35,2.4),(4.35,2.2),TEXT,32)
        self.play(FadeIn(mb),run_time=.3)
        self.at("down the spine")
        arrow=parr((0,2.0),(0,-2.8),YELLOW)
        self.play(GrowArrow(arrow),run_time=.6)
        self.at("this is")
        cr=leader("craniorachischisis",(.35,-1,0),(3.9,-1),RED,34)
        self.play(FadeIn(cr),run_time=.35)
        self.finish()


# Circular-arc sections keep equal x/y scale, including the final closed circle.
def rule_xs(L=12,phi=1.65):
    xs=XS(L,phi,95,cx=0,cy=-.2,half=6.1,nz=1.6)
    xs.remove(xs[3])  # Focus this large reach demonstration on the folds and gap.
    return xs


def card():
    return VGroup(lab("One reason a tube can fail",YELLOW,30,(0,3.35)),
                  lab("The folds can close only a gap\ntheir bending can cover.",TEXT,28,(0,-3.05)))


def gapg(xs):
    a,b=xs.geo["tipL"],xs.geo["tipR"]
    y=max(a[1],b[1])+.65
    if b[0]-a[0] < .25:
        return VGroup(Dot(xs.geo["top"],radius=.12,color=GREEN),
                      lab("gap closed",GREEN,28,(0,y+.4)))
    # A thin bracket above the tissue, with no opaque midline box.
    return VGroup(darr((a[0],y),(b[0],y),YELLOW,5),
                  Line([a[0],y-.15,0],[a[0],y+.15,0],color=YELLOW),
                  Line([b[0],y-.15,0],[b[0],y+.15,0],color=YELLOW),
                  lab("the gap",YELLOW,28,(0,y+.4)))


def narrowing_arrows():
    return VGroup(parr((-5.7,-1.7),(-3.7,-1.7)),parr((5.7,-1.7),(3.7,-1.7)),
                  lab("narrowing continues as folds rise",YELLOW,28,(0,-3.05)))


class S20Rule(SpokenScene):
    def construct(self):
        phi=ValueTracker(1.1)
        xs=always_redraw(lambda:rule_xs(12,phi.get_value()))
        bracket=always_redraw(lambda:gapg(rule_xs(12,phi.get_value())))
        self.add(xs)
        c=card()
        self.at("one reason")
        self.play(FadeIn(c[0]),run_time=.35)
        self.at("the folds can close")
        self.play(FadeIn(c[1]),phi.animate.set_value(1.65),run_time=1.0)
        self.at("bending can cover")
        self.play(FadeIn(bracket),run_time=.45)
        self.finish()


def chips_row():
    return VGroup(lab("Other routes:",TEXT,28,(-4.6,3.2)),
                  lab("bending",RED,28,(-1.8,3.2)),lab("fusion",RED,28,(.8,3.2)),lab("sealing",RED,28,(3.4,3.2)))


class S21Mid(SpokenScene):
    def construct(self):
        L,phi=ValueTracker(12),ValueTracker(1.65)
        xs=always_redraw(lambda:rule_xs(L.get_value(),phi.get_value()))
        bracket=always_redraw(lambda:gapg(rule_xs(L.get_value(),phi.get_value())))
        c=card()
        self.add(xs,c,bracket)
        self.at("narrowing it")
        arr=narrowing_arrows()
        self.play(FadeOut(c[1]),FadeIn(arr),L.animate.set_value(10.8),phi.animate.set_value(1.95),run_time=1.1)
        self.at("overlaps folding")
        # Collapse the old card to free vertical room for the rising folds.
        self.play(FadeOut(c[0]),FadeOut(arr),run_time=.2)
        self.play(L.animate.set_value(10),phi.animate.set_value(2.65),run_time=1.0)
        self.play(phi.animate.set_value(PI),run_time=.8)
        self.at("failures of bending")
        routes=chips_row()
        self.play(FadeIn(routes[0:2]),run_time=.35)
        self.at("fusion")
        self.play(FadeIn(routes[2]),run_time=.25)
        self.at("sealing")
        self.play(FadeIn(routes[3]),run_time=.25)
        self.finish()


class S22Beat(NarratedScene):
    def construct(self):
        xs=rule_xs(10,PI)
        bracket=gapg(xs)
        self.add(xs,bracket,chips_row())
        self.play(Indicate(bracket,color=YELLOW,scale_factor=1.04),run_time=2.2)
        self.finish()


class S23Take(SpokenScene):
    def construct(self):
        L,phi=ValueTracker(5),ValueTracker(.03)
        xs=always_redraw(lambda:XS(L.get_value(),phi.get_value(),80,cx=-3.3,cy=.1,half=3,nz=1.5))
        tv=TV(sx=2.05,sy=.86,cx=2.3,cy=-.15)
        op=[(-1.7,-.3,1)]
        base=VGroup(tv.sil(),tv.seam(),tv.gap(10,op),tv.edges(op))
        self.add(xs,base,lab("Narrow first, then fold",TEXT,42,(0,3.25)),
                 lab("where closure fails",TEXT,28,(2.3,-3.25)))
        self.at("narrowing starts first")
        cap=lab("Narrowing starts first",BLUE,30,(-3.3,-1.9))
        self.play(L.animate.set_value(3.7),FadeIn(cap),run_time=.7)
        self.at("the folds rise")
        self.play(L.animate.set_value(3.3),phi.animate.set_value(1.6),run_time=.7)
        self.at("where closure fails")
        cap2=leader("Where closure fails\nnames the defect",tv.P(.32,-1),(4.9,.3),RED,26)
        self.play(FadeIn(cap2),run_time=.3)
        self.finish()


class S24End(EndCard):
    LINE = "Narrow first; where closure fails names the defect."

    def construct(self):
        # Two full-contrast takeaways remain readable through the complete final card.
        lines=VGroup(T("Narrowing starts first",38,BLUE),
                     T("and continues as the folds rise.",36,TEXT),
                     T("Where closure fails names the defect.",36,RED)).arrange(DOWN,buff=.35)
        self.add(lines,lab("biochemistrypedia.com",TEAL,28,(0,-2)))
        self.finish()
