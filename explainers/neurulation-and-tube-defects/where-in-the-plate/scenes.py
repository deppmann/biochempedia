"""Neurulation and neural tube defects, chapter 2: Where in the Plate?  (Biochemistrypedia chaptered film)

COLOR MAP (one colour per concept, shared by every chapter of this film)
  BLUE   = the neural plate, the neural folds, cells of the plate
  ORANGE = skin (the epidermis beside the plate)
  VIOLET = the midline (the book, the floor strip, the midline stripe)
  YELLOW = movement and reach: folds rising and moving, a crawling cell, hinge points, injected tracer
  TEAL   = planar cell polarity / Frizzled / Dishevelled / Vangl2
  RED    = open or failed closure
  GOLD   = injected / Dishevelled-blocked region (neutral experimental condition)
  PINK   = Van Gogh / Prickle, opposite PCP side
  GREEN  = meets, fused, closed, normal
  GREY   = labels, outlines, de-emphasised
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
VIOLET = "#B58CF0"
PINK = "#F0A6CA"
TY = -2.65      # table top in the hands cartoon
TT = 0.7       # thickness of a hand


def darr(p, q, color=GREY, w=4):
    return DoubleArrow(p, q, buff=0, color=color, stroke_width=w, tip_length=0.22,
                       max_tip_length_to_length_ratio=0.3)


def parr(p, q, color=YELLOW, w=6):
    return Arrow(p, q, buff=0, color=color, stroke_width=w, tip_length=0.25,
                 max_tip_length_to_length_ratio=0.4)


def ring_flash(self, pt, color=GREEN, r=0.7):
    ring = Circle(radius=0.12, color=color, stroke_width=6).move_to(pt)
    self.play(ring.animate.scale(r / 0.12).set_stroke(opacity=0), run_time=0.6)
    self.remove(ring)


def span(self, a, b, lo=0.6, hi=2.4, pad=0.35):
    return float(max(lo, min(hi, self.t_of(b) - self.t_of(a) - pad)))


# ---------------------------------------------------------------- hands cartoon
def bar(px, py, L, ang, side, t=TT, vscale=1.22, **kw):
    # Recognisable hand in profile: thumb, deep web notch, palm and four fingertips.
    # The touching thumb tip is the pivot; mirror the entire rotated silhouette.
    loc = [(0, 0), (.18, .15), (.65, .12), (.95, -.18),
           (.72, -.38), (1.20, -.30), (L-.35, -.05), (L, 0), (L, -.14),
           (L-.06, -.30), (L-.28, -.34), (L-.02, -.43),
           (L-.10, -.58), (L-.40, -.60), (L-.20, -.70),
           (L-.35, -.83), (L-.70, -.80), (L-.60, -.94),
           (L-.83, -1.04), (1.15, -.92), (.35, -.70), (0, -.28)]
    a = np.radians(ang)
    return Polygon(*[[px + side*(x*np.cos(a)-y*t/1.04*np.sin(a)),
                       py + x*np.sin(a)*vscale+y*t/1.04*np.cos(a), 0] for x,y in loc],
                   **kw).round_corners(.045)


def hands(w, th, L, ty=TY, cx=0.0, outline=False, vscale=1.22):
    g = VGroup()
    for side in (1,-1):
        g.add(bar(cx+side*w/2, ty+TT, L, th, side,
                  t=1.1 if outline else TT, vscale=vscale,
                  stroke_color=TEXT if outline else BLUE, stroke_width=3,
                  fill_color=BLUE, fill_opacity=0 if outline else .5))
    return g


def hand_labels(w, L, ty=TY, cx=0):
    return VGroup(T("hand / fold",28,BLUE).move_to([cx-3.4,ty+2.5,0]),
                  T("hand / fold",28,BLUE).move_to([cx+3.4,ty+2.5,0]),
                  T("thumb edge",26,YELLOW).move_to([cx,ty-.65,0]))


def book(w, ty=TY, cx=0.0):
    return Rectangle(width=w, height=TT, stroke_color=VIOLET, stroke_width=4,
                     fill_color=VIOLET, fill_opacity=0.6).move_to([cx, ty + TT / 2, 0])


def tbl_line(x0=-6.4, x1=6.4, ty=TY):
    return Line([x0, ty, 0], [x1, ty, 0], color=GREY, stroke_width=3)


# ---------------------------------------------------------------- cross-section made of the same arms
def xsec(m, th, L=4.0, y0=-1.5, S=6.3):
    g = VGroup()
    g.add(Line([-m / 2, y0, 0], [m / 2, y0, 0], color=VIOLET, stroke_width=20))
    for s in (1, -1):
        a = np.radians(th)
        tip = np.array([s * (m / 2 + L * np.cos(a)), y0 + L * np.sin(a), 0])
        g.add(Line([s * m / 2, y0, 0], tip, color=BLUE, stroke_width=20))
        g.add(Line(tip, [s * S, y0, 0], color=ORANGE, stroke_width=12))
    return g


def hinge_dots(m, y0=-1.5):
    return VGroup(*[Dot([s * m / 2, y0, 0], radius=0.13, color=YELLOW) for s in (1, -1)])


# ---------------------------------------------------------------- top-view embryo
def hwf(u):
    return (0.58 + 0.42 * (u + 1) / 2) * np.sqrt(max(0.0, 1 - abs(u) ** 6))


def plate_pts(cx, cy, W, H, f0, f1, u0=-1.0, u1=1.0, n=40):
    us = np.linspace(u0, u1, n)
    right = [[cx + f1 * W * hwf(u), cy + u * H / 2, 0] for u in us]
    left = [[cx + f0 * W * hwf(u), cy + u * H / 2, 0] for u in us[::-1]]
    return right + left


def embryo(cx, cy, sc):
    skin = Ellipse(width=5.2 * sc, height=4.3 * sc, stroke_color=ORANGE, stroke_width=4,
                   fill_color=ORANGE, fill_opacity=0.10).move_to([cx, cy, 0])
    plate = Polygon(*plate_pts(cx, cy, 1.25 * sc, 3.5 * sc, -1, 1), stroke_color=BLUE, stroke_width=4,
                    fill_color=BLUE, fill_opacity=0.35)
    return VGroup(skin, plate)


def tint(cx, cy, sc, kind):
    W, H = 1.25 * sc, 3.5 * sc
    kw = dict(stroke_width=0, fill_color=GOLD, fill_opacity=0.65)
    if kind == "mid":
        return VGroup(Polygon(*plate_pts(cx, cy, W, H, -0.3, 0.3, -0.9, 0.9), **kw))
    return VGroup(Polygon(*plate_pts(cx, cy, W, H, 0.62, 1.0, -0.9, 0.9), **kw),
                  Polygon(*plate_pts(cx, cy, W, H, -1.0, -0.62, -0.9, 0.9), **kw))


def folds(cx, cy, sc, f):
    W, H = 1.25 * sc, 3.5 * sc
    col = GREEN if f < 0.05 else YELLOW
    g = VGroup()
    for s in (1, -1):
        m = VMobject(color=col, stroke_width=7)
        m.set_points_as_corners([[cx + s * f * W * hwf(u), cy + u * H / 2, 0] for u in np.linspace(-0.85, 0.85, 24)])
        g.add(m)
    return g


def gapx(cx, cy, sc, f):
    W = 1.25 * sc
    h = f * W * hwf(0.15)
    return darr([cx - h, cy + 0.15 * 3.5 * sc / 2, 0], [cx + h, cy + 0.15 * 3.5 * sc / 2, 0], RED, 5)


# ---------------------------------------------------------------- results table
XS = [-4.5, -1.5, 1.5, 4.5]
HEAD = ["Where blocked", "Plate width", "Folds rise", "Tube closes"]
ROWS = [[("midline", VIOLET), ("stays wide", RED), ("yes", GREEN), ("no", RED)],
        [("sides", BLUE), ("not reported", GREY), ("yes", GREEN), ("yes (normal)", GREEN)]]
TCY, RH = 2.35, 0.72


def table_frame():
    box = Rectangle(width=12.0, height=3 * RH, stroke_color=GREY, stroke_width=2).move_to([0, TCY - RH, 0])
    ls = VGroup(*[Line([x, TCY + RH / 2, 0], [x, TCY - 2.5 * RH, 0], color=GREY, stroke_width=2) for x in (-3, 0, 3)],
                *[Line([-6, TCY - RH / 2 - i * RH, 0], [6, TCY - RH / 2 - i * RH, 0], color=GREY, stroke_width=2)
                  for i in range(2)])
    heads = VGroup(*[T(h, 26, TEXT).move_to([XS[i], TCY, 0]) for i, h in enumerate(HEAD)])
    return VGroup(box, ls, heads)


def tcell(r, c):
    txt, col = ROWS[r][c]
    return T(txt, 28, col).move_to([XS[c], TCY - (r + 1) * RH, 0])


EX = 3.0
EY = -1.45
ESC = 0.82


def emb_pair():
    L = embryo(-EX, EY, ESC)
    R = embryo(EX, EY, ESC)
    return L, R


def emb_labels():
    return VGroup(T("midline option", 28, GOLD).move_to([-EX, -3.5, 0]),
                  T("sides option", 28, GOLD).move_to([EX, -3.5, 0]))


class S00Title(TitleCard):
    LESSON = "Neurulation and neural tube defects"
    TITLE = "Where in the Plate?"


# ================================================================ s01
class S01Q(SpokenScene):
    def construct(self):
        M_ = ValueTracker(2.4)
        TH = ValueTracker(78)
        xs = always_redraw(lambda: xsec(M_.get_value(), TH.get_value()))
        self.play(FadeIn(xs), run_time=0.5)
        self.at("the width")
        arrow = darr([-1.2, -2.2, 0], [1.2, -2.2, 0], VIOLET, 5)
        q = T("?", 64, TEXT).move_to([2.2, -2.25, 0])
        self.play(GrowFromCenter(arrow), FadeIn(q), run_time=0.6)
        self.at("midline")
        ml = T("midline", 28, VIOLET).move_to([0, -0.85, 0])
        self.play(FadeIn(ml), run_time=0.4)
        self.at("the folds")
        fl = VGroup(T("fold", 28, BLUE).move_to([-1.95, 3.05, 0]), T("fold", 28, BLUE).move_to([1.95, 3.05, 0]))
        self.play(FadeIn(fl), run_time=0.4)
        self.at("they can meet")
        ar = VGroup(parr([-1.65, 2.45, 0], [-0.45, 2.45, 0]), parr([1.65, 2.45, 0], [0.45, 2.45, 0]))
        self.play(*[GrowArrow(a) for a in ar], run_time=0.6)
        self.at("a simple cartoon")
        self.play(FadeIn(T("a simple cartoon", 26, TEXT).move_to([0, -3.3, 0])), run_time=0.4)
        self.finish()


# ================================================================ s02
class S02Hands(SpokenScene):
    def construct(self):
        th=ValueTracker(0)
        hd=always_redraw(lambda: hands(0,th.get_value(),4.3))
        self.add(tbl_line(),hd,hand_labels(0,4.3))
        self.at("thumbs touching")
        self.play(FadeIn(Dot([0,TY+TT,0],color=YELLOW)),run_time=.3)
        self.at("roll each up")
        self.play(th.animate.set_value(90),run_time=1.6)
        self.at("the top edges meet")
        self.play(FadeIn(T("top edges meet",30,GREEN).move_to([3.6,2.3,0])),run_time=.4)
        self.at("however broad")
        self.play(FadeIn(hands(0,90,4.3,outline=True)),run_time=.5)
        self.wait(3.0)
        self.finish()


class S04Book(SpokenScene):
    def construct(self):
        w,L=2.1,4.1
        th=ValueTracker(0)
        hd=always_redraw(lambda:hands(w,th.get_value(),L))
        self.add(tbl_line(),hd,T("hand / fold",28,BLUE).move_to([-4,0,0]),
                 T("hand / fold",28,BLUE).move_to([4,0,0]))
        self.at("a book")
        self.play(FadeIn(book(w)),FadeIn(T("book",28,VIOLET).move_to([0,-3.25,0])),run_time=.4)
        self.at("upright")
        self.play(th.animate.set_value(90),run_time=.9)
        self.at("by the book's width")
        self.play(GrowFromCenter(darr([-w/2,2.9,0],[w/2,2.9,0],VIOLET)),
                  FadeIn(T("top edges: gap = book width",28,TEXT).move_to([0,3.45,0])),run_time=.4)
        self.wait(3.0)
        self.finish()


class S05Broad(SpokenScene):
    def construct(self):
        w,L=2.1,4.1
        th=ValueTracker(90)
        hd=always_redraw(lambda:hands(w,th.get_value(),L))
        self.add(tbl_line(),book(w),hd,hands(w,90,L,outline=True))
        top=T("broader hands: still apart",30,TEXT).move_to([0,3.3,0])
        bl=T("book",28,VIOLET).move_to([0,-3.12,0])
        self.add(top,bl,T("thumb edges",26,YELLOW).move_to([4.2,-1.7,0]),
                 Line([2.8,-1.7,0],[1.05,TY+TT,0],color=YELLOW,stroke_width=2))
        self.at("tip them past upright")
        top.become(T("tip inward to close the gap",30,GREEN).move_to([0,3.3,0]))
        self.play(FadeOut(self.mobjects[3]),th.animate.set_value(np.degrees(np.arccos(-w/(2*L)))),run_time=1.0)
        self.at("the book is the midline")
        self.play(Transform(bl,T("midline",30,VIOLET).move_to([0,-3.12,0])),
                  FadeIn(T("neural fold",28,BLUE).move_to([-3.7,.6,0])),
                  FadeIn(T("neural fold",28,BLUE).move_to([3.7,.6,0])),
                  FadeIn(T("A cartoon: the real midline creases at a hinge.",26,TEXT).move_to([0,-3.65,0])),run_time=.4)
        self.wait(3.2)
        self.finish()




# ================================================================ s06 / s07 shared rearrangement
def ce_cells(R, cw, ch, px, py, col=BLUE):
    cells = []
    xs = [-1.5 * px, -0.5 * px, 0.5 * px, 1.5 * px]
    for r in range(R):
        y = ((R - 1) / 2 - r) * py
        for c in range(4):
            cells.append(RoundedRectangle(corner_radius=0.1, width=cw, height=ch, stroke_color=col, stroke_width=3,
                                          fill_color=col, fill_opacity=0.35).move_to([xs[c], y, 0]))
    return cells


def ce_targets(R, px, py):
    """Target centres: row r, column c goes to slot k = 2r + (c mod 2) of its half-column."""
    out = []
    for r in range(R):
        for c in range(4):
            k = 2 * r + (c % 2)
            x = (-0.5 if c < 2 else 0.5) * px
            y = ((2 * R - 1) / 2 - k) * py
            out.append(np.array([x, y, 0]))
    return out


class S06Inter(SpokenScene):
    def construct(self):
        R, cw, ch, px, py = 2, 1.3, 1.0, 1.5, 1.15
        cells = ce_cells(R, cw, ch, px, py)
        grp = VGroup(*cells)
        tg = ce_targets(R, px, py)
        w0 = darr([-3.0, 2.8, 0], [3.0, 2.8, 0], VIOLET, 5)
        wl = T("midline width", 26, VIOLET).move_to([0, 3.35, 0])
        self.play(FadeIn(grp), GrowFromCenter(w0), FadeIn(wl), run_time=0.8)
        self.at("cells crawl")
        movers = [cells[i] for i in range(8) if i % 4 in (0, 3)]
        self.play(*[m.animate.set_fill(YELLOW, 0.5).set_stroke(YELLOW) for m in movers], run_time=0.3)
        ups = [(cells[i], np.array([cells[i].get_center()[0], tg[i][1], 0])) for i in range(8)]
        self.play(*[c.animate.move_to(p) for c, p in ups], run_time=0.7)
        w1 = darr([-1.5, 2.8, 0], [1.5, 2.8, 0], VIOLET, 5)
        self.play(*[c.animate.move_to(tg[i]) for i, c in enumerate(cells)], Transform(w0, w1), run_time=0.9)
        self.play(*[m.animate.set_fill(BLUE, 0.35).set_stroke(BLUE) for m in movers], run_time=0.3)
        self.at("this is intercalation")
        self.play(FadeIn(T("intercalation", 34, YELLOW).move_to([0, -3.2, 0])), run_time=0.5)
        self.finish()


class S07Ce(SpokenScene):
    def construct(self):
        # A persistent before panel holds 40 x 50 for the entire scene.
        cells=ce_cells(5,.70,.70,.80,.80)
        before=VGroup(*cells).move_to([-3.4,0,0])
        after=before.copy().move_to([2.5,0,0])
        self.add(before,T("40 across × 50 long",30,TEXT).move_to([-3.4,2.6,0]),
                 T("2,000 cells",30,TEXT).move_to([-3.4,-2.6,0]),
                 T("each square = 100 cells",26,TEXT).move_to([-3.4,-3.25,0]),
                 T("idealized: no cell division",26,TEXT).move_to([3.1,-3.25,0]))
        self.at("rearranged")
        self.play(TransformFromCopy(before,after),run_time=.4)
        self.at("narrower across")
        tg=ce_targets(5,.8,.48)
        self.play(*[c.animate.move_to(p+np.array([2.5,0,0])).stretch_to_fit_width(.70).stretch_to_fit_height(.39)
                    for c,p in zip(after,tg)],
                  FadeIn(T("converge →",28,YELLOW).move_to([-.25,0,0])),
                  GrowArrow(parr([1.15,0,0],[1.65,0,0],YELLOW,4)),
                  GrowArrow(parr([3.8,0,0],[3.35,0,0],YELLOW,4)),run_time=.6)
        self.at("longer along")
        self.play(GrowFromCenter(darr([4, -2.5,0],[4,2.5,0],YELLOW)),
                  FadeIn(T("extend",28,YELLOW).move_to([5.2,0,0])),
                  FadeIn(T("20 across × 100 long",30,TEXT).move_to([2.8,2.95,0])),
                  FadeIn(T("same 2,000 cells",28,TEXT).move_to([2.8,-2.8,0])),run_time=.5)
        self.at("convergent extension")
        self.play(FadeIn(T("convergent extension",34,YELLOW).move_to([0,3.55,0])),run_time=.4)
        self.wait(3.0)
        self.finish()




# ================================================================ s09 wing
def wing_pts(n=80):
    out = []
    for t in np.linspace(0, TAU, n, endpoint=False):
        out.append([5.2 * np.cos(t), 2.3 * np.sin(t) * (0.8 - 0.3 * np.cos(t)) - 0.2, 0])
    return out


def wing_hairs():
    hs = []
    for x in np.linspace(-4.3, 3.9, 9):
        for y in np.linspace(-1.5, 1.3, 5):
            half = 2.3 * (0.8 - 0.3 * np.cos(np.arccos(np.clip(x / 5.2, -1, 1)))) * np.sqrt(max(0, 1 - (x / 5.2) ** 2))
            if abs(y + 0.2) < half * 0.8:
                hs.append(Line([x-.22,y-.08,0],[x+.25,y+.08,0],color=TEAL,stroke_width=4))
    return hs


class S09Wing(SpokenScene):
    def construct(self):
        wing = Polygon(*wing_pts(), stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.12)
        wl = T("fly wing", 28, GREY).move_to([0, 3.2, 0])
        hs = wing_hairs()
        tipl=T("toward the tip →",28,TEXT).move_to([3.8,-2.65,0])
        self.add(wing,wl,*hs,tipl)
        self.at("in mutant flies")
        ml = T("frizzled or Van Gogh mutant", 28, RED).move_to([0, 3.2, 0])
        self.play(ReplacementTransform(wl, ml), FadeOut(tipl), run_time=0.5)
        self.at("the hairs swirl")
        anims = []
        for h in hs:
            c = h.get_center()
            a = 1.8 * np.sin(1.3 * c[0]) + 1.6 * np.cos(1.7 * c[1])
            anims.append(Rotate(h, a, about_point=c))
        self.play(LaggedStart(*anims, lag_ratio=0.03), run_time=1.6)
        self.wait(3.0)
        self.finish()


# ================================================================ s10
SPOS = [(-1.7, 1.2), (1.6, 1.5), (-1.5, -1.4), (1.5, -1.0), (0.2, 1.9), (-0.3, -1.9), (1.9, 0.3), (-1.9, 0.2)]


class S10Sides(SpokenScene):
    def construct(self):
        cell=RegularPolygon(6,radius=2.5,start_angle=PI/2,stroke_color=BLUE,
                            stroke_width=5,fill_color=BLUE,fill_opacity=.22)
        left=[Circle(radius=.17,stroke_color=PINK,stroke_width=4).move_to([x*.9,y*.9,0]) for x,y in SPOS[4:]]
        right=[Dot([x*.9,y*.9,0],radius=.17,color=TEAL) for x,y in SPOS[:4]]
        self.add(cell,T("one wing cell",30,TEXT).move_to([0,-3.1,0]))
        self.at("frizzled and disheveled")
        self.add(*right,chip("Frizzled",TEAL,28).move_to([4.6,.8,0]))
        self.at("disheveled gather")
        self.play(FadeIn(chip("Dishevelled",TEAL,28).move_to([4.6,-.5,0])),
                  *[d.animate.move_to([2.05,1.35-i*.9,0]) for i,d in enumerate(right)],run_time=.65)
        self.at("van gogh")
        self.add(*left,chip("Van Gogh",PINK,28).move_to([-4.6,.8,0]))
        self.at("prickle gather")
        self.play(FadeIn(chip("Prickle",PINK,28).move_to([-4.6,-.5,0])),
                  *[d.animate.move_to([-2.05,1.35-i*.9,0]) for i,d in enumerate(left)],run_time=.65)
        self.wait(3.0)
        self.finish()


# ================================================================ s11
class S11Pcp(SpokenScene):
    def construct(self):
        cells=VGroup(*ce_cells(7,.8,.62,.9,.73))
        self.add(cells,T("neural plate, top view",28,TEXT).move_to([0,-3.15,0]))
        self.at("planar cell polarity")
        self.play(FadeIn(T("planar cell polarity (PCP)",34,TEAL).move_to([0,3.25,0])),run_time=.4)
        self.at("a sense of direction")
        self.play(*[GrowFromCenter(darr(c.get_center()+LEFT*.28,c.get_center()+RIGHT*.28,TEAL,3)) for c in cells],
                  FadeIn(T("← across →",28,TEAL).move_to([0,2.75,0])),
                  GrowFromCenter(darr([3,-2.5,0],[3,2.5,0],GREY)),
                  FadeIn(T("along",28,TEXT).move_to([4.1,0,0])),run_time=.8)
        self.wait(3.0)
        self.finish()




# ================================================================ s12 / s13 / s14 frog
def early_cells(cx=0,cy=0,r=2.5):
    # Small bounded blastomeres clipped to the spherical embryo silhouette.
    cells=VGroup()
    for row in range(6):
        top=r-row*r/3; bottom=top-r/3
        ys=np.linspace(bottom,top,18)
        for col in range(6):
            f0=-1+col/3; f1=f0+1/3
            pts=[[cx+f1*np.sqrt(max(0,r*r-y*y)),cy+y,0] for y in ys]
            pts += [[cx+f0*np.sqrt(max(0,r*r-y*y)),cy+y,0] for y in ys[::-1]]
            cells.add(Polygon(*pts,stroke_color=TEXT,stroke_width=2,
                              fill_color=BLUE,fill_opacity=.28 if row<3 else .12))
    return cells


class S12Frog(SpokenScene):
    def construct(self):
        e=early_cells()
        self.add(e,T("Xenopus laevis: frog embryo",30,TEXT).move_to([0,-3.2,0]))
        self.at("john wallingford")
        self.play(FadeIn(T("Wallingford and Harland, 2002",32,TEXT).move_to([0,3.3,0])),run_time=.4)
        self.at("where in the frog plate")
        self.play(Indicate(e[9],color=YELLOW),run_time=.8)
        self.finish()


class S13Map(SpokenScene):
    def construct(self):
        ball=early_cells(-3.6,0,2.35)
        e=embryo(3.5,0,1.25)
        self.add(ball,e,T("early embryo",28,TEXT).move_to([-3.5,-2.95,0]),
                 T("neural plate",28,BLUE).move_to([3.5,-3,0]))
        self.at("mapped")
        self.play(GrowArrow(parr([-.9,0,0],[.8,0,0],TEXT)),
                  FadeIn(T("fate map",28,TEXT).move_to([0,.65,0])),run_time=.4)
        self.at("an injection")
        needle=parr([-1.1,2.5,0],ball[10].get_center(),YELLOW)
        self.play(GrowArrow(needle),ball[10].animate.set_fill(YELLOW,.8),
                  FadeIn(T("one injected cell",28,YELLOW).move_to([-3.6,2.85,0])),run_time=.5)
        self.at("one part of the plate")
        lit=Polygon(*plate_pts(3.5,0,1.25*1.25,3.5*1.25,-.25,.25,-.9,.9),
                    fill_color=YELLOW,fill_opacity=.8,stroke_width=0)
        self.play(FadeIn(lit),FadeOut(needle),run_time=.5)
        self.wait(3.0)
        self.finish()




class S14Design(SpokenScene):
    def construct(self):
        self.add(embryo(-3.4,0,1.25))
        self.at("disheveled")
        self.play(FadeIn(chip("Dishevelled blocked here",GOLD,30).move_to([0,3.2,0])),run_time=.4)
        self.at("the midline")
        self.play(FadeIn(tint(-3.4,0,1.25,"mid")),
                  FadeIn(T("blocked at midline",28,GOLD).move_to([-3.4,-3.1,0])),run_time=.4)
        self.at("in others")
        self.play(FadeIn(embryo(3.4,0,1.25)),run_time=.4)
        self.at("the sides")
        self.play(FadeIn(tint(3.4,0,1.25,"side")),
                  FadeIn(T("blocked at sides",28,GOLD).move_to([3.4,-3.1,0])),run_time=.4)
        self.wait(3.0)
        self.finish()




# ================================================================ s15 / s16
class S15Predict(SpokenScene):
    def construct(self):
        self.add(predict_frame())
        self.at("those blocked at the midline")
        self.play(Indicate(self.mobjects[0][0],color=GOLD,scale_factor=1.03),run_time=.5)
        self.at("those blocked at the sides")
        self.play(Indicate(self.mobjects[0][1],color=GOLD,scale_factor=1.03),run_time=.5)
        self.finish()




def predict_frame():
    eL, eR = emb_pair()
    gL, gR = VGroup(eL, tint(-EX, EY, ESC, "mid")), VGroup(eR, tint(EX, EY, ESC, "side"))
    return VGroup(gL, gR, emb_labels(), table_frame(),
                  T("Predict: which embryo stays open?", 34, TEXT).move_to([0, 3.25, 0]))


class S16Pause(NarratedScene):
    def construct(self):
        frame=predict_frame()
        frame[-1].move_to([0,3.5,0])
        self.add(frame)
        cue=T("pause and think: 5",28,YELLOW).move_to([0,2.95,0])
        self.add(cue)
        for n in range(5,0,-1):
            cue.become(T(f"pause and think: {n}",28,YELLOW).move_to([0,2.95,0]))
            self.wait(1)
        self.finish()


# ================================================================ s17 / s18 / s19
def result_frame(row1=False, row2=False, left_end=False, right_end=False):
    eL, eR = emb_pair()
    mob = VGroup(VGroup(eL, tint(-EX, EY, ESC, "mid")), VGroup(eR, tint(EX, EY, ESC, "side")),
                 table_frame(),T("Predict: which embryo stays open?",34,TEXT).move_to([0,3.25,0]))
    if row1:
        mob.add(*[tcell(0, c) for c in range(4)])
    if row2:
        mob.add(*[tcell(1, c) for c in range(4)])
    if left_end:
        mob.add(folds(-EX, EY, ESC, 0.6), gapx(-EX, EY, ESC, 0.6),
                T("open", 26, RED).move_to([-EX, -3.5, 0]))
    if right_end:
        mob.add(folds(EX, EY, ESC, 0.0), T("closed", 26, GREEN).move_to([EX, -3.5, 0]))
    return mob


class S17Rev1(SpokenScene):
    def construct(self):
        self.add(result_frame())
        self.wait(0.1)
        self.at("blocked at the midline")
        self.play(FadeIn(tcell(0, 0)), Indicate(VGroup(*self.mobjects[0][0]), color=RED, scale_factor=1.05), run_time=0.7)
        self.at("the plate stayed wide")
        wide = darr([-EX - 0.9, EY + 0.26, 0], [-EX + 0.9, EY + 0.26, 0], RED, 5)
        self.play(GrowFromCenter(wide), FadeIn(tcell(0, 1)), run_time=0.6)
        self.at("the folds rose")
        F = ValueTracker(1.0)
        fl = always_redraw(lambda: folds(-EX, EY, ESC, F.get_value()))
        self.play(FadeOut(wide), FadeIn(fl), FadeIn(tcell(0, 2)), run_time=0.5)
        self.at("moved inward")
        self.play(F.animate.set_value(0.6), run_time=1.0)
        self.at("the tube stayed open", lead=0)
        self.play(FadeIn(gapx(-EX, EY, ESC, 0.6)), FadeIn(T("open", 26, RED).move_to([-EX, -3.5, 0])),
                  FadeIn(tcell(0, 3)), run_time=0.6)
        self.finish()


class S18Rev2(SpokenScene):
    def construct(self):
        self.add(result_frame(row1=True, left_end=True))
        self.wait(0.1)
        self.at("blocked at the sides", lead=0)
        self.play(FadeIn(tcell(1, 0)), FadeIn(tcell(1,1)), run_time=0.4)
        self.at("where the folds")
        F = ValueTracker(1.0)
        fl = always_redraw(lambda: folds(EX, EY, ESC, F.get_value()))
        self.play(FadeIn(fl), FadeIn(tcell(1, 2)), run_time=0.4)
        self.at("form and fuse")
        self.play(F.animate.set_value(0.0), run_time=1.2)
        self.at("closure was normal")
        self.play(FadeIn(T("closed", 26, GREEN).move_to([EX, -3.5, 0])), FadeIn(tcell(1, 3)), run_time=0.6)
        self.finish()


class S19Beat(NarratedScene):
    def construct(self):
        self.add(result_frame(True, True, True, True))
        self.play(Indicate(tcell(0,3),color=RED,scale_factor=1.12),
                  Indicate(tcell(1,3),color=GREEN,scale_factor=1.12),run_time=1.4)
        self.finish()


# ================================================================ s20
class S20Mean(SpokenScene):
    def construct(self):
        th=ValueTracker(0);cx,ty,w,L=-3.4,-2.65,1.2,2.25
        hd=always_redraw(lambda:hands(w,th.get_value(),L,ty=ty,cx=cx,vscale=2.2))
        self.add(tbl_line(-6.4,-.4,ty),book(w,ty,cx),hd,
                 embryo(3.3,0,1.15),tint(3.3,0,1.15,"mid"),folds(3.3,0,1.15,.6),gapx(3.3,0,1.15,.6),
                 T("book = midline",28,VIOLET).move_to([-3.5,-3.15,0]),
                 T("hands =\nfolds",24,BLUE).move_to([-5.8,1.2,0]),
                 T("top edges stay apart",28,RED).move_to([-3.5,3.4,0]))
        self.at("the hands rose")
        self.play(th.animate.set_value(90),run_time=1.2)
        self.at("dishevelled is needed")
        self.play(GrowArrow(parr([-.9,-1,0],[2.9,-1,0],VIOLET)),
                  FadeIn(T("In these experiments, Dishevelled is needed at the midline.",28,TEAL).move_to([0,-3.5,0])),run_time=.4)
        self.wait(3.0)
        self.finish()




# ================================================================ s22 / s23 / s24 / s25 / s26 mouse
def mouse():
    # One opaque outline joins the pointed snout, ears, back, belly and feet.
    outline=[[-4.9,-.1,0],[-4.35,.35,0],[-4.1,.65,0],
             [-4.55,1.05,0],[-4.25,1.45,0],[-3.75,1.4,0],[-3.5,.65,0],
             [-3.15,1.2,0],[-2.65,1.25,0],[-2.45,.9,0],[-2.65,.65,0],
             [-1.7,1.45,0],[-.2,1.6,0],[1.15,1,0],[1.5,.05,0],
             [1.05,-.8,0],[.8,-1.1,0],[1.05,-1.3,0],[.2,-1.3,0],
             [-.15,-.95,0],[-1.7,-1.05,0],[-2.35,-.8,0],
             [-2.8,-1.15,0],[-3.45,-1.15,0],[-3.15,-.8,0],
             [-3.5,-.45,0],[-4.15,-.4,0],[-4.9,-.1,0]]
    body=VMobject(stroke_color=TEXT,stroke_width=4,fill_color="#363C49",fill_opacity=1)
    body.set_points_smoothly(outline)
    tail=VMobject(color=TEXT,stroke_width=7).set_points_smoothly(
        [[1.45,.05,0],[2,-.6,0],[3,-.8,0],[4,-.3,0],
         [4,1.1,0],[3,1.3,0],[2.7,.5,0],[3.5,.1,0]])
    ears=VGroup(*[Arc(radius=r,start_angle=-.4,angle=3.4,color=PINK,stroke_width=3)
                   .move_to([x,y,0]) for x,y,r in [(-4.08,1.14,.24),(-2.88,1.0,.20)]])
    whisk=VGroup(*[Line([-4.65,-.1,0],[-5.25,y,0],color=TEXT,stroke_width=2)
                  for y in (-.55,-.15,.25)])
    return VGroup(tail,body,ears,whisk,Dot([-4.05,.35,0],color=TEXT,radius=.09),
                  Dot([-4.9,-.1,0],color=PINK,radius=.10))


class S22Mouse(SpokenScene):
    def construct(self):
        m=mouse().scale(1.15).stretch(1.25,1).shift(DOWN*.1)
        self.add(m,T("mouse",34,TEXT).move_to([0,3.2,0]),
                 T("one copy",28,TEXT).move_to([-.8,-.35,0]),
                 T("looped / kinked tail",28,TEXT).move_to([3.7,-1.8,0]))
        self.at("the loop")
        self.play(Transform(self.mobjects[1],T("loop-tail mouse",34,TEXT).move_to([0,3.2,0])),run_time=.4)
        self.at("vangle two",lead=0)
        self.play(FadeIn(chip("Vangl2",TEAL,30).move_to([-.8,.5,0])),run_time=.4)
        self.at("a relative of")
        self.play(FadeIn(T("relative of Van Gogh (fly)",30,PINK).move_to([0,-2.8,0])),run_time=.4)
        self.wait(3.0)
        self.finish()


# Mouse top views: head at top; boundaries are schematic, not a body-length scale.
PCY,PH=-.25,5.8
MBY=.95
C1Y=.25

def mouse_plate(cx,short=False):
    pl=Polygon(*plate_pts(cx,PCY,1.05,PH,-1,1),stroke_color=BLUE,stroke_width=4,fill_color=BLUE,fill_opacity=.3)
    st=Polygon(*plate_pts(cx,PCY,1.05,PH,-.15,.15,.12 if short else -.94,.94),
               fill_color=VIOLET,fill_opacity=.95,stroke_width=0)
    return VGroup(pl,st)


def mouse_pair(title,short=True):
    return VGroup(mouse_plate(-3.4,False),mouse_plate(1.2,short),
        T("normal",28,GREEN).move_to([-3.4,2.95,0]),
        T("loop-tail: two copies",28,TEXT).move_to([1.6,2.95,0]),
        T(title,30,TEXT).move_to([0,3.55,0]),
        T("head ↑",26,TEXT).move_to([-5.4,2.1,0]),
        T("tail end",26,TEXT).move_to([-5.35,-2.85,0]))


class S23Lp(SpokenScene):
    def construct(self):
        pair=mouse_pair("loop-tail mouse: two copies",False)
        # This is a closure map. Save the labelled-midline evidence for s24.
        pair[0].remove(pair[0][1])
        pair[1].remove(pair[1][1])
        self.add(pair,folds(-3.4,PCY,1.3,0))
        self.at("open from the midbrain")
        op=Polygon(*plate_pts(1.2,PCY,1.05,PH,-1,1,-1,.41),
                   stroke_color=RED,fill_color=RED,fill_opacity=.5)
        line=DashedLine([-.1,MBY,0],[3,MBY,0],color=TEXT)
        self.play(FadeIn(op),Create(line),
                  FadeIn(T("midbrain",28,TEXT).move_to([4.2,MBY,0])),run_time=.4)
        self.at("down the spine")
        self.play(FadeIn(T("open:\ncraniorachischisis",28,RED).move_to([4.3,-.8,0])),
                  GrowArrow(parr([2.6,.6,0],[2.6,-2.9,0],RED)),run_time=.4)
        self.wait(3.2)
        self.finish()


class S24Copp(SpokenScene):
    def construct(self):
        pair=mouse_pair("loop-tail embryo, two copies, before neurulation")
        # Tracer is revealed when named; normal extends all the way to the tail end.
        normal_st=pair[0][1]; short_st=pair[1][1]
        pair[0].remove(normal_st);pair[1].remove(short_st)
        self.add(pair)
        self.at("andrew")
        self.play(FadeIn(T("Copp laboratory, 2007",30,TEXT).move_to([0,-3.55,0])),run_time=.4)
        self.at("that midline")
        self.play(Create(normal_st),Create(short_st),
                  FadeIn(T("labelled\nmidline",28,VIOLET).move_to([3.15,1.35,0])),run_time=.6)
        self.at("it had failed to extend")
        stop=PCY+.12*PH/2
        self.play(Create(DashedLine([1.2,stop,0],[1.2,-2.8,0],color=RED,stroke_width=5)),
                  FadeIn(T("where it\nshould reach",28,RED).move_to([3.3,-2.6,0])),
                  FadeIn(Dot([1.2,stop,0],radius=.08,color=RED)),
                  FadeIn(T("stops short",28,RED).move_to([3.3,stop,0])),run_time=.5)
        self.wait(3.0)
        self.finish()


def closure_frame(zip_end=1):
    pair=mouse_pair("Closure 1: hindbrain–spinal boundary")
    # The first zipper starts at this boundary, below the midbrain.
    y=C1Y
    pair.add(DashedLine([-4.65,y,0],[2.6,y,0],color=TEXT,stroke_width=2),
             T("hindbrain",26,TEXT).move_to([4.6,.7,0]),
             T("spinal cord",26,TEXT).move_to([4.6,-.2,0]),
             T("Closure 1",28,RED).move_to([4.6,-1.2,0]),
             parr([3.3,-1.1,0],[1.5,y,0],RED),
             Line([.95,y-.25,0],[1.45,y+.25,0],color=RED,stroke_width=7),
             Line([.95,y+.25,0],[1.45,y-.25,0],color=RED,stroke_width=7),
             Line([-3.4,y+1.7*zip_end,0],[-3.4,y-2.8*zip_end,0],color=GREEN,stroke_width=9))
    return pair


class S25C1(SpokenScene):
    def construct(self):
        z=ValueTracker(.08)
        self.add(always_redraw(lambda:closure_frame(z.get_value())))
        self.at("never happened")
        self.play(z.animate.set_value(.65),run_time=1.2)
        self.finish()


class S26Beat(NarratedScene):
    def construct(self):
        z=ValueTracker(.65)
        self.add(always_redraw(lambda:closure_frame(z.get_value())))
        self.play(z.animate.set_value(1),run_time=1.5)
        self.play(Indicate(VGroup(Line([.95,C1Y-.25,0],[1.45,C1Y+.25,0],color=RED,stroke_width=7),
                                 Line([.95,C1Y+.25,0],[1.45,C1Y-.25,0],color=RED,stroke_width=7)),
                           color=RED,scale_factor=1.3),run_time=.5)
        self.finish()




# ================================================================ s27
class S27Not(SpokenScene):
    def construct(self):
        y=-2.6;L=5.2
        m=ValueTracker(3.0);th=ValueTracker(30)
        xs=always_redraw(lambda:xsec(m.get_value(),th.get_value(),L=L,y0=y))
        self.add(xs,T("narrowing is not the whole job",32,TEXT).move_to([0,3.4,0]),
                 T("midline",28,VIOLET).move_to([0,-3.1,0]))
        self.at("starts early")
        self.play(m.animate.set_value(2.4),run_time=.6)
        self.at("overlaps folding")
        self.play(m.animate.set_value(1.8),th.animate.set_value(65),run_time=.8)
        self.at("the plate must still bend")
        self.play(FadeIn(hinge_dots(1.8,y)),
                  FadeIn(T("hinge points",28,YELLOW).move_to([0,-3.55,0])),th.animate.set_value(85),run_time=.7)
        self.at("fold tips must stick")
        meet=np.degrees(np.arccos(-1.8/(2*L)))
        self.play(th.animate.set_value(meet),
                  FadeIn(T("tips must stick",28,GREEN).move_to([3.4,2.5,0])),run_time=.7)
        self.play(FadeIn(Dot([0,y+L*np.sin(np.radians(meet)),0],radius=.14,color=GREEN)),
                  FadeIn(T("adhere",28,GREEN).move_to([-1.3,2.7,0])),run_time=.3)
        self.wait(3.0)
        self.finish()


class S28Take(SpokenScene):
    def construct(self):
        m=ValueTracker(3.4);th=ValueTracker(65);L=3.7;y=-1.2
        xs=always_redraw(lambda:xsec(m.get_value(),th.get_value(),L=L,y0=y))
        self.add(xs,VGroup(T("The midline must be narrow enough",40,TEXT),
                        T("for the folds to close.",40,TEXT)).arrange(DOWN,buff=.12)
                 .move_to([0,3.12,0]))
        self.at("the midline")
        self.play(m.animate.set_value(1.3),run_time=.8)
        self.at("for the folds")
        self.play(th.animate.set_value(np.degrees(np.arccos(-1.3/(2*L)))),run_time=.8)
        self.at("frog")
        self.play(FadeIn(T("Frog: Dishevelled at the midline",30,TEAL).move_to([0,-2.5,0])),run_time=.4)
        self.at("mouse")
        self.play(FadeIn(T("Mouse: Vangl2",30,TEAL).move_to([0,-3.15,0])),run_time=.4)
        self.finish()




class S29End(EndCard):
    LINE = "The midline must be narrow enough for the folds to close."

    def construct(self):
        self.add(VGroup(T("The midline must be narrow enough",48,TEXT),
                        T("for the folds to close.",48,TEXT)).arrange(DOWN,buff=.16)
                 .move_to([0,1.5,0]),
                 T("Frog: Dishevelled at the midline",32,TEAL).move_to([0,-.6,0]),
                 T("Mouse: Vangl2",32,TEAL).move_to([0,-1.5,0]),
                 T("biochemistrypedia.com",28,TEXT).move_to([0,-2.8,0]))
        self.finish()
