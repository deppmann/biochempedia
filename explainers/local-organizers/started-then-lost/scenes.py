"""Local organizers, chapter 3: Started, Then Lost  (Biochemistrypedia chaptered film)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole series; taken from scenes.old.py)
  SLATE  = forebrain tissue
  GREEN  = midbrain tissue (also territory kept)
  PURPLE = hindbrain tissue (rhombomere 1 = the cerebellum's source, and behind)
  TEAL   = Otx2 (not used in this chapter)
  PINK   = Gbx2 (not used in this chapter)
  YELLOW = FGF8 and the organizer / source
  ORANGE = Wnt1
  BLUE = Engrailed, Pax2/5 (boundary genes)
  RED    = repression, loss, removal, "lost"
  GREY   = tube outline, de-emphasized, "changed"
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
PINK = "#F08BB4"
ORANGE = "#F29E4C"
FORE, MID, HIND = "#7F9DB2", GREEN, PURPLE
OTX, GBX, FGF, WNT = TEAL, PINK, YELLOW, ORANGE
ENG = "#409CFF"

H = 1.9          # tube half-height
XL, XR = -6.0, 6.0
XI = 0.6         # the line (isthmus)
X_MID0, X_R1 = -2.4, 2.6
TY = 0.6         # vertical centre of the big tube in tube scenes


def prof(x):
    b = H * max(0.0, 1 - (abs(x) / 6.0) ** 4) ** 0.25
    return b * (1 - 0.30 * np.exp(-((x - XI) / 0.35) ** 2))


def poly(xa, xb, ty, color=None, op=0.25, stroke=0, sc=None, S=1.0, cx=0.0):
    xs = np.linspace(xa, xb, 60)
    top = [[cx + S * x, ty + S * prof(x), 0] for x in xs]
    bot = [[cx + S * x, ty - S * prof(x), 0] for x in xs[::-1]]
    p = Polygon(*(top + bot), stroke_width=stroke, stroke_color=sc or color or GREY)
    if color:
        p.set_fill(color, op)
    else:
        p.set_fill(opacity=0)
    return p


def dashed(m, n=36, ratio=0.55):
    return DashedVMobject(m, num_dashes=n, dashed_ratio=ratio)


def lost(xa, xb, ty, S=1.0, cx=0.0, color=RED, w=3, n=36):
    """Dashed outline of tissue that is gone."""
    return dashed(poly(xa, xb, ty, None, stroke=w, sc=color, S=S, cx=cx), n)


class TubeS:
    """Flat neural tube, front at left: forebrain | midbrain | the line | rhombomere 1 | hindbrain."""

    def __init__(self, ty=TY, S=1.0, cx=0.0, op=0.3):
        self.ty, self.S, self.cx = ty, S, cx
        kw = dict(S=S, cx=cx)
        self.fore = poly(XL, X_MID0, ty, FORE, op, **kw)
        self.mid = poly(X_MID0, XI, ty, MID, op, **kw)
        self.r1 = poly(XI, X_R1, ty, HIND, op, **kw)
        self.hind = poly(X_R1, XR, ty, HIND, op, **kw)
        self.out = poly(XL, XR, ty, None, stroke=4 if S >= 1 else 3, sc=GREY, **kw)
        self.body = VGroup(self.fore, self.mid, self.r1, self.hind, self.out)
        ly = ty + S * H + 0.38
        self.ly = ly
        self.l_fore = T("forebrain", 26, FORE).move_to([cx + S * -4.2, ly, 0])
        self.l_mid = T("midbrain", 26, MID).move_to([cx + S * -1.5, ly, 0])
        self.l_cere = T("cerebellum", 26, HIND).move_to([cx + S * 2.5, ly, 0])
        self.l_hind = T("hindbrain", 26, HIND).move_to([cx + S * 4.9, ly, 0])
        self.labels = VGroup(self.l_fore, self.l_mid, self.l_cere, self.l_hind)

    def X(self, x):
        return self.cx + self.S * x

    def line(self):
        return DashedLine([self.X(XI), self.ty - self.S * H - 0.1, 0], [self.X(XI), self.ty + self.S * H + 0.1, 0],
                          color=TEXT, stroke_width=3)


def source(x, y, r=0.26, g=0.55):
    glow = Circle(radius=g, stroke_width=0, fill_color=FGF, fill_opacity=0.25).move_to([x, y, 0])
    dot = Circle(radius=r, stroke_color=BG, stroke_width=2, fill_color=FGF, fill_opacity=1).move_to([x, y, 0])
    return VGroup(glow, dot)


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.05, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def cross(c, color=RED, s=0.5, w=7):
    p = c.get_center() if hasattr(c, "get_center") else np.array(c, float)
    return VGroup(Line(p + [-s, -s * 0.8, 0], p + [s, s * 0.8, 0], color=color, stroke_width=w),
                  Line(p + [-s, s * 0.8, 0], p + [s, -s * 0.8, 0], color=color, stroke_width=w))


def dashed_arrow(a, b, angle, color=GREY, w=4):
    a, b = np.array(a, float), np.array(b, float)
    arc = ArcBetweenPoints(a, b, angle=angle)
    d = DashedVMobject(arc.set_stroke(color, w), num_dashes=16, dashed_ratio=0.55)
    v = arc.get_end() - arc.point_from_proportion(0.95)
    v = v / np.linalg.norm(v)
    tip = Triangle(fill_color=color, fill_opacity=1, stroke_width=0).scale(0.16).rotate(angle_of_vector(v) - PI / 2)
    tip.move_to(b - v * 0.08)
    # Solid landing strokes bridge the terminal dash gaps to the chip edges.
    return VGroup(d,Line(a,arc.point_from_proportion(.045),color=color,stroke_width=w),
                  Line(arc.point_from_proportion(.955),b,color=color,stroke_width=w),tip)



def mouse(cx, cy, sc=1.0, color=GREY, sw=3):
    pts = [(-2.3, -0.2), (-1.95, 0.25), (-1.3, 0.6), (-0.3, 0.9), (0.8, 0.9), (1.6, 0.55), (1.95, -0.1), (1.55, -0.68),
           (0.5, -0.9), (-0.7, -0.85), (-1.6, -0.65), (-2.15, -0.5)]
    P = [np.array([x, y, 0.0]) * sc for x, y in pts]
    body = VMobject(stroke_color=color, stroke_width=sw, fill_color=color, fill_opacity=0.14)
    body.set_points_smoothly(P + [P[0]])
    tail = VMobject(stroke_color=color, stroke_width=sw, fill_opacity=0)
    tail.set_points_smoothly([np.array([x, y, 0.0]) * sc for x, y in [(1.95, -0.15), (2.55, -0.35), (3.0, 0.0), (3.3, 0.7)]])
    ear = Circle(radius=0.36 * sc, stroke_color=color, stroke_width=sw, fill_color=color, fill_opacity=0.14).move_to(np.array([-1.35, 0.78, 0]) * sc)
    eye = Dot(radius=0.07 * sc, color=color).move_to(np.array([-1.85, 0.12, 0]) * sc)
    nose = Dot(radius=0.06 * sc, color=color).move_to(np.array([-2.3, -0.2, 0]) * sc)
    g = VGroup(tail, body, ear, eye, nose)
    return g.move_to([cx, cy, 0])



def fish(cx, cy, color=GREY, sw=3):
    a, b = 2.3, 1.0
    body = Ellipse(width=2 * a, height=2 * b, stroke_color=color, stroke_width=sw, fill_color=color, fill_opacity=0.12)
    tail = Polygon([a - 0.2, 0, 0], [a + 1.1, 0.95, 0], [a + 1.1, -0.95, 0], stroke_color=color, stroke_width=sw,
                   fill_color=color, fill_opacity=0.12)
    eye = Dot([-a + 0.55, 0.28, 0], radius=0.11, color=color)
    stripes = VGroup()
    for yo in (-0.5, 0.0, 0.5):
        half = a * np.sqrt(1 - (yo / b) ** 2)
        stripes.add(Line([-0.2 * half, yo, 0], [0.96 * half, yo, 0], color=color, stroke_width=2.5))
    g = VGroup(tail, body, eye, stripes)
    return g.move_to([cx, cy, 0])



# Shared large time-course grid. Tissue is faint; expression is always blue.
TX = [-4.25, 0, 4.25]
RY = [1.05, -1.65]
TW, TH, MS = 3.95, 2.20, 0.30

def label(s, x, y, size=28, color=TEXT):
    return T(s, size, color).move_to([x,y,0])

def blank_tile(x,y,height=TH):
    return VGroup(RoundedRectangle(width=TW,height=height,corner_radius=.12,stroke_color=GREY,stroke_width=2).move_to([x,y,0]),
                  poly(XL,XR,y,None,stroke=2,sc=GREY,S=MS,cx=x))

def band_tile(x,y,op):
    return poly(-1.2,2.2,y,ENG,op,S=MS,cx=x)

def tissue_tile(x,y):
    return VGroup(poly(X_MID0,XI,y,MID,.14,S=MS,cx=x),poly(XI,X_R1,y,HIND,.14,S=MS,cx=x))

def gone_tile(x,y):
    return lost(X_MID0,X_R1,y,S=MS,cx=x,n=22)

class Panels:
    def __init__(self, rows, title="Engrailed"):
        self.tiles=[[blank_tile(x,y) for x in TX] for y in RY]
        self.labels=[label(t,-4.8,y+1.35,26,c) for (t,c),y in zip(rows,RY)]
        self.times=VGroup(*[label(t,x,2.95,28) for t,x in zip(["early","later","latest"],TX)])
        self.heading=label(title,-3.65,3.55,28,ENG)
        fit(self.heading,max_w=4.2)
        self.key=label("blue = Engrailed on",4,-3.62,24,ENG)
        self.tag=label("schematic, not data",-4.4,-3.62,24)
        self.axis=VGroup(arr([-.7,3.55,0],[1.1,3.55,0],TEXT,w=3),label("time",1.7,3.55,24))
        self.base=VGroup(self.heading,self.times,self.axis,*self.labels,*[t for row in self.tiles for t in row],self.key,self.tag)

def question_cards():
    # Fixed boxes and identical text styling give neither answer visual priority.
    cards=VGroup()
    for text,x in [("never on",-2.5),("on, then fade",2.5)]:
        box=RoundedRectangle(width=3.65,height=.62,corner_radius=.14,
                             stroke_color=ENG,stroke_width=2.5,fill_color=ENG,fill_opacity=.16)
        cards.add(VGroup(box,T(text,28,ENG)).move_to([x,-3.08,0]))
    return cards

def reveal_state():
    p=Panels([("wild type",TEXT),("mouse: Wnt1 null",WNT)])
    wt=[VGroup(tissue_tile(x,RY[0]),band_tile(x,RY[0],.95)) for x in TX]
    mu=[VGroup(tissue_tile(TX[0],RY[1]),band_tile(TX[0],RY[1],.95)),
        VGroup(tissue_tile(TX[1],RY[1]),band_tile(TX[1],RY[1],.35)),gone_tile(TX[2],RY[1])]
    return p,wt,mu

def signature():
    return VGroup(label("started,",-1.35,-3.15,40),label("then lost",1.5,-3.15,40,RED))

class S00Title(TitleCard):
    LESSON="Local Organizers: The Midbrain-Hindbrain Boundary"
    TITLE="Started, Then Lost"
    def construct(self):
        g=VGroup(T("BIOCHEMISTRYPEDIA",28,TEAL),T("LOCAL ORGANIZERS · CHAPTER 3",28),
                 T(self.TITLE,58,font=TITLE_FONT),Line(LEFT*2,RIGHT*2,color=GOLD,stroke_width=4)).arrange(DOWN,buff=.5).move_to(ORIGIN)
        self.play(FadeIn(g),run_time=.6)
        self.finish()

class S01Q(SpokenScene):
    def construct(self):
        tb=TubeS(); src=source(XI,TY)
        self.add(tb.body,tb.labels,tb.line(),src)
        self.at("what happens")
        self.play(FadeIn(label("take it away",0,-2.6,40)),run_time=.35)
        self.at("take it away")
        self.play(FadeOut(src),Create(cross([XI,TY,0],s=.5)),
                  FadeIn(VGroup(*[label("?",x,TY,68) for x in [-4,-1.4,2.2,4.7]])),run_time=.45)
        self.finish()

class S02Target(SpokenScene):
    def construct(self):
        segs=VGroup(*[Rectangle(width=1.65,height=.8,stroke_color=GREY,fill_color=GREY,fill_opacity=.3).move_to([x,2.1,0]) for x in [-3.6,-1.8,0,1.8,3.6]])
        self.add(segs,label("gene targeting in mouse",0,3.3,34))
        self.at("remove one gene")
        self.play(Create(cross(segs[2],s=.45)),FadeIn(label("one gene removed",0,1.22,28,RED)),run_time=.5)
        dish=Ellipse(width=4.8,height=1.7,stroke_color=TEXT,fill_color=GREY,fill_opacity=.12).move_to([-2.9,-1.5,0])
        cells=VGroup(*[Circle(radius=.18,stroke_color=TEXT,fill_color=TEXT,fill_opacity=.4).move_to([x,y,0]) for x,y in [(-4,-1.5),(-3.4,-1.8),(-2.8,-1.3),(-2,-1.5),(-3.6,-1.1),(-2.5,-1.9)]])
        self.at("the change is made")
        self.play(GrowArrow(arr([-2,1.4,0],[-2.8,-.45,0],TEXT)),FadeIn(dish),FadeIn(cells),run_time=.6)
        self.at("embryonic stem cells")
        # Complete the chain during the sentence, with a full-length arrow.
        self.play(FadeIn(label("embryonic stem cells",-2.9,-2.9,28)),
                  FadeIn(arr([-.4,-1.5,0],[1.35,-1.5,0],TEXT,w=6)),
                  FadeIn(mouse(3.6,-1.5,.75,color=TEXT)),FadeIn(label("mouse",3.6,-2.9,30)),run_time=.3)
        self.finish()

class S03Wnt(SpokenScene):
    def construct(self):
        tb=TubeS(); a=poly(-1.9,XI,TY,MID,.35); b=poly(XI,2,TY,HIND,.35)
        self.add(tb.fore,poly(X_MID0,-1.9,TY,MID,.35),a,b,poly(2,X_R1,TY,HIND,.35),tb.hind,tb.out,tb.labels,tb.line())
        ring=poly(-.35,.4,TY,WNT,.9,stroke=3,sc=WNT)
        wl=label("Wnt1 ring",-1.3,-2.1,30,WNT)
        self.at("is made")
        self.play(FadeIn(ring),FadeIn(wl),Create(Line([-.8,-1.85,0],[0,-1.05,0],color=WNT)),run_time=.5)
        self.at("mice lacking it")
        self.play(Create(cross(ring,s=.65)),ring.animate.set_fill(opacity=.15),FadeIn(label("McMahon and Bradley; Thomas and Capecchi, 1990",0,-3.35,26)),run_time=.5)
        self.at("lose most of")
        self.play(FadeOut(a),FadeIn(lost(-1.9,XI,TY,n=24)),run_time=.65)
        self.at("much of the cerebellum")
        self.play(FadeOut(b),FadeIn(lost(XI,2,TY,n=24)),run_time=.65)
        self.finish()

class S04Predict(SpokenScene):
    def construct(self):
        p=Panels([("wild type",TEXT),("mouse: Wnt1 null",WNT)])
        self.add(p.base)
        cards=question_cards()
        self.at("never come on")
        self.play(FadeIn(cards[0]),run_time=.3)
        self.at("or does it")
        self.play(FadeIn(cards[1]),run_time=.3)
        self.finish()

class S05Pause(NarratedScene):
    def construct(self):
        p=Panels([("wild type",TEXT),("mouse: Wnt1 null",WNT)])
        # Both alternatives stay at exactly the same brightness throughout the pause.
        p.heading.become(label("Engrailed · think",-3.65,3.55,28,ENG))
        ring=Circle(radius=.29,color=TEXT,stroke_width=3).move_to([0,-3.08,0])
        self.add(p.base,question_cards(),ring)
        for remaining in range(5,0,-1):
            digit=label(str(remaining),0,-3.08,24)
            self.add(digit)
            self.wait(1)
            self.remove(digit)
        self.finish()

class S06Rev(SpokenScene):
    def construct(self):
        p,wt,mu=reveal_state(); self.add(p.base)
        self.at("comes on")
        self.play(FadeIn(wt[0]),FadeIn(mu[0]),run_time=.45)
        self.at("then it is lost")
        self.play(FadeIn(wt[1]),FadeIn(mu[1]),run_time=.45)
        self.at("and the tissue disappears")
        self.play(FadeIn(wt[2]),FadeIn(mu[2]),run_time=.5)
        rule=label("Wnt1 keeps Engrailed on",0,-3.15,32)
        self.at("is needed")
        self.play(FadeIn(rule),run_time=.4)
        self.at("not to turn it on")
        self.play(Transform(rule,label("maintenance, rather than initiation",0,-3.15,30)),run_time=.35)
        self.finish()

class S07Sig(SpokenScene):
    def construct(self):
        p,wt,mu=reveal_state(); self.add(p.base,*wt,*mu)
        s=signature()
        self.at("started")
        self.play(FadeIn(s[0]),run_time=.3)
        self.at("then lost")
        self.play(FadeIn(s[1]),run_time=.3)
        self.finish()

class S08Beat(NarratedScene):
    def construct(self):
        p,wt,mu=reveal_state(); self.add(p.base,*wt,*mu,signature()); self.finish()

class S09Rescue(SpokenScene):
    def construct(self):
        tb=TubeS(ty=.55)
        tb.l_cere.become(label("anterior hindbrain",2.35,tb.ly,26,HIND))
        gm=lost(X_MID0,XI,.55); gr=lost(XI,X_R1,.55)
        tag=label("Wnt1 null",0,3.45,28,WNT)
        self.add(tb.fore,tb.hind,tb.out,tb.labels,gm,gr,tag)
        en=chip("Engrailed",ENG,32).move_to([2.25,-2.5,0])
        self.at("supplying engrailed")
        self.play(FadeIn(en),run_time=.45)
        self.at("in 1996")
        self.play(FadeIn(label("Danielian and McMahon, 1996",0,-3.45,26)),run_time=.35)
        self.at("made engrailed one")
        self.play(Transform(en,chip("Engrailed 1",ENG,32).move_to([2.25,-2.5,0])),run_time=.4)
        ctl=chip("Wnt1 control elements",WNT,28).move_to([-3.2,-2.5,0])
        self.at("own control elements")
        self.play(FadeIn(ctl),GrowArrow(arr(ctl.get_right(),en.get_left(),ENG)),run_time=.4)
        dom=poly(-.35,.4,.55,ENG,.95)
        travelling=dom.copy().scale(.2).next_to(en,UP,buff=.06)
        self.play(Transform(tag,label("Wnt1 null + En1 from Wnt1 control elements",0,3.45,28,WNT)),run_time=.3)
        self.at("in the mutants")
        self.add(travelling)
        # First move above the chip, then straight into the anterior Wnt1 domain.
        self.play(travelling.animate.move_to([.025,-1.55,0]),run_time=.3)
        self.play(Transform(travelling,dom),run_time=.5)
        domainlabel=label("Wnt1 domain",-1.5,-1.6,26,ENG)
        leader=Line([-.3,-1.6,0],[.03,-1.15,0],color=ENG)
        self.add(domainlabel,leader)
        self.at("early development")
        self.play(FadeOut(gm),FadeOut(gr),FadeIn(tb.mid),FadeIn(tb.r1),run_time=.75)
        self.bring_to_front(travelling)
        self.play(FadeOut(domainlabel),FadeOut(leader),FadeIn(label("early development restored · later stage not shown",0,-1.7,28)),run_time=.3)
        self.finish()

class S10Rescue2(SpokenScene):
    def construct(self):
        ys=[2.7,0,-2.7]
        cs=[chip("Wnt1",WNT,40).move_to([-1,y,0]) for y in ys[:1]]
        cs += [chip("Engrailed",ENG,40,pad=.35).move_to([-1,0,0]),chip("territory",MID,40,pad=.35).move_to([-1,-2.7,0])]
        icons=[]
        for y,k in zip(ys,[WNT,ENG,MID]):
            icons.append(VGroup(poly(XL,XR,y,None,stroke=3,sc=GREY,S=.31,cx=-4.8),poly(-1.2,2.2,y,k,.9,S=.31,cx=-4.8)))
        self.add(icons[0],cs[0],label("signal",3.35,2.7,32))
        self.at("keeps a")
        a=arr([-1,2.13,0],[-1,.65,0],TEXT,w=6)
        self.play(GrowArrow(a),FadeIn(label("keeps on",1,1.3,28)),FadeIn(icons[1]),FadeIn(cs[1]),FadeIn(label("transcription factor",3.35,0,30)),run_time=.55)
        self.at("the transcription")
        self.play(FadeIn(arr([-1,-.65,0],[-1,-2.05,0],TEXT,w=6)),
                  FadeIn(label("keeps",1,-1.35,28)),FadeIn(icons[2]),FadeIn(cs[2]),run_time=.3)
        self.finish()

class S11Fish(SpokenScene):
    def construct(self):
        fh=fish(0,1.3).scale(1.4).stretch_to_fit_height(3.3)
        self.add(fh,label("zebrafish",-4.8,3.35,30),label("acerebellar, Fgf8 mutant",2.5,3.35,30,FGF))
        xs=[-4.25,0,4.25]; y=-1.9
        tiles=[blank_tile(x,y,height=1.85) for x in xs]
        self.add(*tiles,label("boundary genes (e.g. Engrailed, Pax)",0,-.55,28,ENG),
                 *[label(t,x,-3.15,28) for t,x in zip(["early","later","latest"],xs)],label("schematic, not data",0,-3.65,26))
        self.at("same signature")
        early=band_tile(xs[0],y,.95); later=band_tile(xs[1],y,.35)
        self.play(FadeIn(early),FadeIn(later),run_time=.4)
        self.at("switch on")
        self.play(Indicate(early,color=ENG,scale_factor=1.08),run_time=.35)
        self.at("then fade")
        self.play(Indicate(later,color=ENG,scale_factor=1.08),run_time=.35)
        self.finish()

# Matched mouse rows; no invisible objects are reintroduced during a later shift.
class MouseRows:
    def __init__(self, final=False):
        self.rows=[]; self.base=VGroup()
        for idx,(y,caption) in enumerate([(1.65,"early regional Fgf8 deletion"),(-1.95,"milder Fgf8 reduction")]):
            s=.62
            fore=poly(XL,X_MID0,y,FORE,.35,S=s); hind=poly(X_R1,XR,y,HIND,.35,S=s)
            mf=poly(X_MID0,-1.2,y,MID,.5,S=s); mb=poly(-1.2,XI,y,MID,.5,S=s); cere=poly(XI,X_R1,y,HIND,.5,S=s)
            # Region boundaries are explicit and disappear with their respective tissue.
            normal=VGroup(mf,mb,cere)
            gl=VGroup(lost(X_MID0,XI,y,S=s,n=20),lost(XI,X_R1,y,S=s,n=16))
            mild=VGroup(lost(-1.2,XI,y,S=s,n=14),Ellipse(width=.75,height=1.2,fill_color=BG,fill_opacity=1,stroke_color=RED,stroke_width=3).move_to([s*1.5,y,0]))
            labs=VGroup(label("forebrain",-3.35,y+1.45,26,FORE),label("midbrain",-.9,y+1.45,26,MID),
                        label("cerebellum",1.35,y+1.45,26,HIND),label("hindbrain",3.35,y+1.45,26,HIND))
            self.base.add(fore,hind,poly(XL,XR,y,None,stroke=3,sc=GREY,S=s),labs,label(caption,0,y-1.5,28,FGF))
            self.rows.append(dict(mf=mf,mb=mb,cere=cere,normal=normal,gone=gl,mild=mild))
        if final:
            self.base.add(self.rows[0]["gone"],label("absent",-.5,1.65,28,RED),self.rows[1]["mf"],self.rows[1]["cere"],self.rows[1]["mild"])

class S12Mouse(SpokenScene):
    def construct(self):
        m=MouseRows(); a,b=m.rows
        self.add(m.base,a["gone"],b["normal"],label("absent",-.5,1.65,28,RED),label("mouse",0,3.6,32))
        self.at("lack")
        self.play(Indicate(a["gone"],color=RED,scale_factor=1.02),run_time=.4)
        self.at("milder reductions")
        self.play(Indicate(b["normal"],scale_factor=1.02),run_time=.35)
        self.at("spare part")
        self.play(FadeOut(b["mb"]),FadeIn(b["mild"]),run_time=.55)
        self.finish()

class S13Beat(NarratedScene):
    def construct(self):
        self.add(MouseRows(final=True).base,label("mouse",0,3.6,32)); self.finish()

class S14Loop(SpokenScene):
    def construct(self):
        p=Panels([("mouse: Wnt1 null",WNT),("zebrafish: acerebellar",FGF)],"boundary genes · Engrailed")
        self.add(p.base)
        for y in RY:
            self.add(tissue_tile(TX[0],y),band_tile(TX[0],y,.95),tissue_tile(TX[1],y),band_tile(TX[1],y,.35))
        self.at("does not fail")
        self.play(FadeIn(signature()[0]),run_time=.4)
        self.at("fails to last")
        self.play(FadeIn(signature()[1]),run_time=.4)
        self.finish()

class S15Loop2(SpokenScene):
    def construct(self):
        cf=chip("Fgf8",FGF,44,pad=.4).move_to([-3,2.2,0]); cw=chip("Wnt1",WNT,44,pad=.4).move_to([3,2.2,0])
        ce=chip("Engrailed and Pax",ENG,40,pad=.5).move_to([0,-.8,0])
        self.add(cf,cw,ce)
        af=dashed_arrow(cf.get_bottom(),ce.get_left()+UP*.2,PI/7,FGF)
        aw=arr(cw.get_bottom(),ce.get_right()+UP*.2,WNT,w=6)
        rescue=label("rescue, 1996",.9,.7,26,WNT)
        self.at("keep the program")
        self.play(FadeIn(af),GrowArrow(aw),FadeIn(rescue),run_time=.65)
        self.at("standard model")
        self.play(FadeIn(label("standard model: schematic, not a wiring diagram",0,-3.4,28)),run_time=.35)
        self.at("other experiments")
        self.play(FadeIn(label("dashed: from other experiments",0,-2.75,30)),run_time=.35)
        ra=dashed_arrow(ce.get_left(),cf.get_left(),-PI/1.8,TEXT)
        rb=dashed_arrow(ce.get_right(),cw.get_right(),PI/1.8,TEXT)
        self.at("the transcription factors")
        self.play(FadeIn(ra),FadeIn(rb),run_time=.7)
        self.at("remove a key part",lead=.45)
        self.play(FadeIn(cross(cw,s=.8)),cw.animate.set_opacity(.2),
                  *[m.animate.set_opacity(.15) for m in [cf,ce,af,aw,ra,rb,rescue]],run_time=.2)
        self.at("the rest fade")
        self.wait(.1)
        self.finish()

class S16Tests(SpokenScene):
    def construct(self):
        ys=[2.5,0,-2.5]; s=.59; cx=.95
        for y,t in zip(ys,["move it","add it","take it away"]):
            self.add(label(t,-5.1,y,30),poly(XL,X_MID0,y,FORE,.25,S=s,cx=cx),poly(X_MID0,XI,y,MID,.35,S=s,cx=cx),
                     poly(XI,XR,y,HIND,.3,S=s,cx=cx),poly(XL,XR,y,None,stroke=3,sc=GREY,S=s,cx=cx))
        px=cx+s*XI; fx=cx+s*-4.2
        sources=[source(fx,ys[0],r=.22,g=.42),source(px,ys[1],r=.22,g=.42),
                 source(fx,ys[1],r=.22,g=.42)]
        removed=cross([px,ys[2],0],s=.33)
        extra=poly(-5.5,-2.9,ys[1],MID,.75,S=s,cx=cx)
        move_arrow=arr([px,ys[0],0],[fx+.35,ys[0],0],FGF,w=4)
        self.add(*sources,removed,extra,move_arrow)
        self.bring_to_front(*sources,removed)
        self.at("move it")
        self.play(Indicate(sources[0],color=FGF,scale_factor=1.15),run_time=.3)
        self.at("add it")
        self.play(Indicate(sources[2],color=FGF,scale_factor=1.15),run_time=.3)
        self.at("take it away")
        self.play(Indicate(removed,color=RED,scale_factor=1.15),run_time=.3)
        self.finish()

class S17Take(SpokenScene):
    def construct(self):
        y=1.1
        tb=TubeS(ty=y,S=.85)
        self.add(tb.body,tb.labels,tb.line())
        band=poly(.2,1,y,FGF,.85,S=.85)
        self.at("a line becomes")
        sl=label("source",.5,-.85,28,FGF)
        self.play(FadeIn(band),FadeIn(sl),run_time=.5)
        def bar(end):
            return Rectangle(width=end+5.5,height=.42,stroke_color=FGF,fill_color=FGF,fill_opacity=.65).move_to([(-5.5+end)/2,-2,0])
        b=bar(-4.8)
        self.at("must stay on")
        self.add(label("source on, time",-3.9,-1.4,28,FGF),arr([-5.5,-2.5,0],[5.5,-2.5,0],TEXT,w=3),b)
        self.play(Transform(b,bar(3.8)),run_time=.65)
        self.at("for each part")
        self.play(Indicate(tb.mid,scale_factor=1.03),Indicate(tb.r1,scale_factor=1.03),run_time=.45)
        self.at("remove it too early")
        near_mid=poly(-1.2,XI,y,BG,1,S=.85); near_cere=poly(XI,1.8,y,BG,1,S=.85)
        ghosts=VGroup(lost(-1.2,XI,y,S=.85,n=16),lost(XI,1.8,y,S=.85,n=16))
        self.play(Transform(b,bar(-2.5)),FadeOut(band),FadeOut(sl),Create(cross([.5,y,0],s=.45)),run_time=.3)
        # Categorical timed-deletion inference: nearer structures may need longer.
        self.play(FadeIn(near_mid),FadeIn(near_cere),FadeIn(ghosts),run_time=.45)
        self.add(label("suggests: nearer the boundary may need longer exposure",0,-3.25,26))
        self.at("parts are lost")
        self.play(FadeIn(label("lost or changed",.2,-.85,30,RED)),run_time=.3)
        self.finish()

class S18End(EndCard):
    LINE="A line becomes a source; it must stay on long enough."
    def construct(self):
        g=VGroup(T("A line becomes a source.",44,font=TITLE_FONT),T("It must stay on long enough.",44,font=TITLE_FONT),
                 T("Remove it too early,",40),T("and parts are lost or changed.",40,color=RED),T("biochemistrypedia.com",26,color=TEAL)).arrange(DOWN,buff=.35)
        self.play(FadeIn(g),run_time=.5); self.finish()
