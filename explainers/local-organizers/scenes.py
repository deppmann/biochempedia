"""Local organizers, chapter 1: Where the Line Falls  (Biochemistrypedia chaptered film)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, shared by all chapters; taken from scenes.old.py)
  SLATE #8295AD = Otx2 / midbrain roof
  SAGE  #A7BA91 = Gbx2 / cerebellum roof
  GOLD  #D4A843 = FGF8 / signaling source / bead
  CLAY  #C58B73 = Wnt1
  Neutral grey = anatomical regions before gene identity is introduced
  Hox code uses distinct lavender shades, only in the Hox scene
  TEXT (white) = line, labels; repression uses its source gene colour
  GREY   = tube outline, de-emphasized things
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
PINK = "#F08BB4"
ORANGE = "#F29E4C"
OTX, GBX, FGF, WNT = "#8295AD", "#A7BA91", "#D4A843", "#C58B73"
FORE, MID, HIND = GREY, OTX, GBX

# ---- geometry of the flat neural-tube strip (front at the left) ------------------------------
X0, X1 = -6.5, 6.5
X_FM = -2.4        # forebrain | midbrain
XI = 0.6           # the isthmus, where the line sits
X_R1 = 3.4         # end of rhombomere 1 (front of the hindbrain)
X_CORD = 4.8       # hindbrain | spinal cord
TY = 0.45          # strip centre line

_XS = np.linspace(X0, X1, 521)
_CT = [(-6.5, 0.0), (-6.3, 0.9), (-5.8, 1.55), (-4.8, 1.85), (-3.6, 1.8), (-2.8, 1.6), (-2.4, 1.4),
       (-1.8, 1.6), (-0.8, 1.75), (0.0, 1.45), (0.5, 0.95), (0.7, 0.8), (1.0, 0.95), (1.6, 1.25),
       (2.6, 1.3), (3.4, 1.15), (4.4, 0.7), (5.0, 0.55), (6.5, 0.55)]
_H = np.interp(_XS, [c[0] for c in _CT], [c[1] for c in _CT])
_K = 25
_H = np.convolve(np.pad(_H, (_K // 2, _K // 2), mode="edge"), np.ones(_K) / _K, mode="valid")


SY = 1.0


def setsy(v):
    """Vertical stretch of the strip (scenes without bottom text stretch it to fill the frame)."""
    global SY
    SY = v


def hh(x):
    return SY * float(np.interp(x, _XS, _H))


def poly(xa, xb, ty, color=None, op=0.25, stroke=0, sc=None, n=60):
    xs = np.linspace(xa, xb, n)
    top = [[x, ty + hh(x), 0] for x in xs]
    bot = [[x, ty - hh(x), 0] for x in xs[::-1]]
    p = Polygon(*(top + bot), stroke_width=stroke, stroke_color=sc or color or GREY)
    if color:
        p.set_fill(color, op)
    else:
        p.set_fill(opacity=0)
    return p


def outline(ty):
    return poly(X0, X1, ty, None, stroke=4, sc=GREY)


def sl(xa, xb, ty, color, op=0.8):
    """A narrow slice of the strip (a band across the tube)."""
    return poly(xa, xb, ty, color, op, n=8)


def roofline(xa, xb, ty, color, w=9, n=40):
    m = VMobject(stroke_color=color, stroke_width=w, fill_opacity=0)
    m.set_points_as_corners([[x, ty + hh(x) + 0.03, 0] for x in np.linspace(xa, xb, n)])
    return m


def stripes(xa, xb, ty, color, op=0.65, dx=0.2):
    g = VGroup()
    for i, x in enumerate(np.arange(xa, xb - 1e-6, dx)):
        if i % 2 == 0:
            g.add(poly(x, min(x + dx, xb), ty, color, op, n=6))
    return g


def dline(ty, x, color=TEXT, w=4):
    return DashedLine([x, ty - hh(x) - 0.12, 0], [x, ty + hh(x) + 0.12, 0], color=color, stroke_width=w,
                      dash_length=0.12)


def lab(text, x, y, color=TEXT, size=26, weight=NORMAL):
    return T(text, max(26, size), color, weight=weight).move_to([x, y, 0])


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.05, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def inhib(a, b, color=RED, w=6, tb=0.18):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w),
                  Line(b + perp * tb, b - perp * tb, color=color, stroke_width=w + 2))


def speaker(c, s=1.0, color=FGF):
    pts = [(-.28, -.14), (-.08, -.14), (.2, -.36), (.2, .36), (-.08, .14), (-.28, .14)]
    p = Polygon(*[[c[0] + x * s, c[1] + y * s, 0] for x, y in pts], stroke_color=BG, stroke_width=2)
    return p.set_fill(color, 1)


def waves(c, radii=(0.7, 1.1, 1.5), color=FGF):
    g = VGroup()
    for r in radii:
        g.add(Arc(radius=r, start_angle=-0.6, angle=1.2, arc_center=c, color=color, stroke_width=5))
        g.add(Arc(radius=r, start_angle=PI - 0.6, angle=1.2, arc_center=c, color=color, stroke_width=5))
    return g


def fence(c):
    g = VGroup()
    for i in range(5):
        g.add(Rectangle(width=0.16, height=0.9, stroke_width=0, fill_color=GREY, fill_opacity=1)
              .move_to([c[0] + (i - 2) * 0.3, c[1], 0]))
    for dy in (-0.2, 0.2):
        g.add(Rectangle(width=1.4, height=0.1, stroke_width=0, fill_color=GREY, fill_opacity=1)
              .move_to([c[0], c[1] + dy, 0]))
    return g


def reshape(mob, fn, span0, span1):
    """Morph a strip piece between two x-spans; every frame is rebuilt from the profile, so it never leaves the tube."""
    return UpdateFromAlphaFunc(
        mob, lambda m, al: m.become(fn(*[a + (b - a) * al for a, b in zip(span0, span1)])), run_time=1.3)


def clause(label, rest, y):
    a = T(label, 26, TEXT, weight=BOLD)
    b = T(rest, 26, TEXT)
    g = VGroup(a, b).arrange(RIGHT, buff=0.2)
    g.move_to([-6.3, y, 0], aligned_edge=LEFT)
    return g


CL_Y = [-2.5, -3.05, -3.6]
CLAUSES = [("Where:", "the line, where Otx2 meets Gbx2"),
           ("Which part:", "on the simplest reading: signal amount"),
           ("Which region:", "the repressor it carries")]


def tissue_fills(ty, op=0.28):
    return VGroup(poly(X0, X_FM, ty, FORE, op), poly(X_FM, XI, ty, MID, op),
                  poly(XI, X_R1, ty, HIND, op), poly(X_R1, X1, ty, GREY, 0.16))


def gene_fills(ty, a=XI, b=XI, op=0.40):
    return poly(X0, a, ty, OTX, op), poly(b, X_R1, ty, GBX, op)


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Local Organizers: The Midbrain-Hindbrain Boundary"
    TITLE = "Where the Line Falls"

    def construct(self):
        card=VGroup(lab("BIOCHEMISTRYPEDIA",0,2.2,OTX,26),
                    lab("LOCAL ORGANIZERS",0,1.4,TEXT,26),
                    lab("THE MIDBRAIN–HINDBRAIN BOUNDARY",0,.85,TEXT,26),
                    lab(self.TITLE,0,-.45,TEXT,50),
                    Line([-1.3,-1.35,0],[1.3,-1.35,0],color=FGF,stroke_width=4))
        self.play(FadeIn(card),run_time=.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
BEAD_X = X_FM - .4


def opening(complete=False):
    setsy(1.55)
    ty = 0.0
    out = outline(ty)
    # The ectopic lobe is the same silhouette as the normal midbrain,
    # reflected and compressed to remain wholly inside the forebrain.
    normal = poly(X_FM + .12, XI - .12, ty, OTX, .25, stroke=3, sc=OTX)
    ectopic = normal.copy().stretch_to_fit_width(2.3).flip(UP).move_to([-3.65, 0, 0])
    bead = Circle(.29, color=FGF, fill_opacity=1).move_to([BEAD_X, .2, 0])
    beadlabel = lab("bead", -3.45, 1.05, FGF)
    fgf = lab("FGF8", -3.45, 1.05, FGF)
    fb = lab("forebrain", -4.3, 3.15)
    realname = lab("midbrain", -1.0, 3.15, OTX)
    newname = lab("second midbrain", -4.35, 3.15, OTX)
    tag = lab("chick", 5.6, 3.2)
    # Same front-to-back axis in opposite directions, directly on each lobe.
    reverse = VGroup(arr([-2.8, -.8, 0], [-4.5, -.8, 0], OTX),
                     lab("front", -2.95, -1.35), lab("back", -4.5, -1.35))
    forward = VGroup(arr([-2.05, -.8, 0], [0, -.8, 0], OTX),
                     lab("front", -1.95, -1.35), lab("back", -.05, -1.35))
    question = lab("Who tells cells what to build?", 0, -3.2, TEXT, 38)
    qs = VGroup(lab("?", -4.25, .9, FGF, 48), lab("?", -1.3, .9, FGF, 48))
    return out, normal, ectopic, bead, beadlabel, fgf, fb, realname, newname, tag, reverse, forward, question, qs


class S01Q(SpokenScene):
    def construct(self):
        out, normal, ectopic, bead, bl, fgf, fb, rn, nn, tag, rev, fwd, q, qs = opening()
        self.add(out, tag)
        self.at("small bead")
        bead.move_to([BEAD_X, 3.1, 0]); bl.move_to([-1.9, 3.1, 0])
        self.play(FadeIn(bead), FadeIn(bl), run_time=.25)
        self.at("into the back")
        self.play(bead.animate.move_to([BEAD_X, .2, 0]), bl.animate.move_to([-3.45, 1.05, 0]), run_time=.65)
        self.at("forebrain")
        self.play(FadeIn(fb), run_time=.25)
        self.at("soaked in one")
        self.play(Indicate(bead, color=FGF), run_time=.5)
        self.at("fgf8")
        self.play(ReplacementTransform(bl, fgf), run_time=.25)
        self.at("second midbrain")
        self.play(GrowFromPoint(ectopic, bead.get_center()), FadeOut(fb), FadeIn(nn), FadeIn(normal), FadeIn(rn), run_time=.75)
        self.at("built")
        self.play(FadeIn(fwd), run_time=.25)
        self.at("back to")
        self.play(GrowFromCenter(rev), run_time=.45)
        self.at("who tells")
        self.play(FadeIn(q), FadeIn(qs), run_time=.5)
        self.finish()


class S02Beat(NarratedScene):
    def construct(self):
        out, normal, ectopic, bead, bl, fgf, fb, rn, nn, tag, rev, fwd, q, qs = opening()
        self.add(out, normal, ectopic, bead, fgf, rn, nn, tag, rev, fwd, q, qs)
        self.finish()




# ---------------------------------------------------------------------------------------------
class S03Hox(SpokenScene):
    def construct(self):
        # A magnified address strip gives r2 onward enough room to read.
        bounds = [-6.2, -1.5, .1, 1.1, 2.1, 3.1, 4.1, 5.1, 6.2]
        def box(a, b, col=GREY, op=.1):
            return Rectangle(width=b-a, height=5.9, stroke_color=GREY, stroke_width=2,
                             fill_color=col, fill_opacity=op).move_to([(a+b)/2, 0, 0])
        base = VGroup(*[box(a,b) for a,b in zip(bounds[:-1],bounds[1:])])
        def bracket(a,b,y,text):
            return VGroup(Line([a,y+.15,0],[a,y,0],color=GREY), Line([a,y,0],[b,y,0],color=GREY),
                          Line([b,y,0],[b,y+.15,0],color=GREY),lab(text,(a+b)/2,y-.42))
        regions=VGroup(bracket(-1.5,3.1,-3.1,"hindbrain"),bracket(3.3,6.2,-3.1,"spinal cord"))
        r1=lab("r1",-.7,.55)
        r1n=lab("no Hox",-.7,-.2, GREY)
        hoxcolors=["#8C76AC","#AE8BC7","#C6ACD8","#8C76AC","#AE8BC7","#C6ACD8"]
        coloured=VGroup(*[box(a,b,c,.65) for a,b,c in zip(bounds[2:-1],bounds[3:],hoxcolors)])
        top=VGroup(Line([.1,3.0,0],[6.2,3.0,0],color=TEXT),lab("Hox genes",3.15,3.5,TEXT,32))
        self.add(base,regions,r1,r1n,lab("forebrain + midbrain",-3.9,1.15,TEXT,28))
        self.at("hox genes")
        self.play(FadeIn(top), run_time=.35)
        self.at("the hindbrain")
        self.play(LaggedStart(*[FadeIn(b) for b in coloured[:3]],lag_ratio=.15),run_time=.65)
        self.at("spinal cord")
        self.play(LaggedStart(*[FadeIn(b) for b in coloured[3:]],lag_ratio=.15),run_time=.65)
        self.at("the midbrain and forebrain")
        self.play(FadeIn(lab("no Hox code",-3.9,-.25,TEXT,34)),run_time=.5)
        self.finish()




# ---------------------------------------------------------------------------------------------
class S04Parts(SpokenScene):
    def construct(self):
        setsy(1.25)
        ty = 0.35
        out = outline(ty)
        fore, mid, r1, rest = (poly(X0, X_FM, ty, GREY, 0.16), poly(X_FM, XI, ty, GREY, 0.16),
                               poly(XI, X_R1, ty, GREY, 0.16), poly(X_R1, X1, ty, GREY, 0.16))
        self.add(out, fore, mid, r1, rest)
        front = T("\u2190 front", 28, GREY).move_to([-5.3, ty - hh(-5.3) - 0.45, 0])
        l_fb = lab("forebrain", -4.4, ty + hh(-4.4) + 0.45, FORE, 28)
        l_mb = lab("midbrain", -1.9, ty + hh(-1.9) + 0.45, MID, 28)
        l_is = lab("isthmus", XI + 0.5, ty + hh(0.0) + 0.45, TEXT, 28)
        l_r1 = lab("rhombomere 1", 1.9, ty - hh(1.9) - 0.45, HIND, 28)
        l_cb = lab("cerebellum", 4.3, ty + hh(3.0) + 0.55, HIND, 28)
        self.at("front at")
        self.play(FadeIn(front), run_time=0.5)
        self.at("then midbrain", lead=0.9)
        self.play(fore.animate.set_fill(FORE, 0.3), FadeIn(l_fb), run_time=0.5)
        self.at("then midbrain")
        self.play(mid.animate.set_fill(MID, 0.3), FadeIn(l_mb), run_time=0.5)
        pinch = VGroup(arr([XI, ty + 1.6, 0], [XI, ty + 1.12, 0], GREY, 5, 0.15),
                       arr([XI, ty - 1.6, 0], [XI, ty - 1.12, 0], GREY, 5, 0.15))
        self.at("a narrowing")
        self.play(FadeIn(pinch), run_time=0.5)
        line = dline(ty, XI)
        lead = arr([XI + 0.4, ty + hh(0.0) + 0.2, 0], [XI + 0.05, ty + 1.2, 0], TEXT, 3, 0.12)
        self.at("isthmus")
        self.play(FadeOut(pinch), Create(line), FadeIn(l_is), FadeIn(lead), run_time=0.6)
        self.at("behind it")
        self.play(r1.animate.set_fill(HIND, 0.3), FadeIn(l_r1), run_time=0.5)
        roof = roofline(XI, X_R1, ty, HIND, 9)
        self.at("the roof of")
        self.play(Create(roof), run_time=0.8)
        a = arr([2.5, ty + 1.85, 0], [3.35, ty + 2.2, 0], HIND, 5, 0.18)
        self.at("gives rise")
        self.play(GrowArrow(a), run_time=0.5)
        self.at("cerebellum")
        self.play(FadeIn(l_cb), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Org(SpokenScene):
    def construct(self):
        setsy(1.25)
        ty = 0.35
        out = outline(ty)
        regs = VGroup(poly(X0, X_FM, ty, FORE, 0.22), poly(X_FM, XI, ty, MID, 0.22),
                      poly(XI, X_R1, ty, HIND, 0.22), poly(X_R1, X1, ty, GREY, 0.14))
        self.add(out, regs)
        sp = speaker([XI, ty, 0], 1.4)
        l_org = lab("local organizer", XI, -2.75, FGF, 30)
        lead = Line([XI, ty - 0.6, 0], [XI, -2.4, 0], color=FGF, stroke_width=3)
        wv = waves([XI, ty, 0], radii=(0.9, 1.45, 2.0))
        glow = poly(-1.5, 2.7, ty, FGF, 0.16)
        line = dline(ty, XI)
        l_is = lab("isthmus", XI + 0.5, ty + hh(0.0) + 0.45, TEXT, 28)
        lead2 = arr([XI + 0.4, ty + hh(0.0) + 0.2, 0], [XI + 0.05, ty + 1.2, 0], TEXT, 3, 0.12)
        self.at("local organizer")
        self.play(GrowFromCenter(sp), FadeIn(l_org), Create(lead), run_time=0.7)
        self.at("small signaling center")
        self.play(Indicate(sp, color=FGF, scale_factor=1.5), run_time=0.8)
        self.at("inside the tube")
        self.play(out.animate.set_stroke(TEXT, 6), run_time=0.4)
        self.play(out.animate.set_stroke(GREY, 4), run_time=0.4)
        self.at("it tells nearby cells")
        self.play(FadeIn(glow), LaggedStart(*[Create(w) for w in wv], lag_ratio=0.12), run_time=1.4)
        self.at("the best")
        self.play(Create(line), FadeIn(l_is), FadeIn(lead2), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Idea(SpokenScene):
    def construct(self):
        setsy(1.55)
        self.add(outline(0))
        title=lab("A line becomes a source.",0,3.3,TEXT,44)
        line=dline(0,XI)
        self.at("one idea")
        self.play(FadeIn(title),Create(line),run_time=.35)
        self.at("a line")
        self.play(Indicate(line,color=TEXT),run_time=.4)
        self.at("source")
        self.play(FadeIn(sl(XI,XI+.35,0,FGF)),Create(waves([XI,0,0],(.7,1.2,1.8),FGF)),run_time=.65)
        self.finish()




# ---------------------------------------------------------------------------------------------
def labels_in(ty, otx_x=-3.3, gbx_x=2.0):
    return lab("Otx2", otx_x, ty, TEXT, 28, BOLD), lab("Gbx2", gbx_x, ty, TEXT, 28, BOLD)


class S07Idea2(SpokenScene):
    def construct(self):
        setsy(1.55); ty=0
        out=outline(ty); o,g=gene_fills(ty)
        lo,lg=labels_in(ty); line=dline(ty,XI)
        band=sl(XI,XI+.35,ty,FGF,.9)
        src=lab("signaling source",1.0,3.15,FGF,30)
        lead=Line([XI,2.8,0],[XI,1.65,0],color=FGF)
        key=lab("FGF8",1.55,-2.5,FGF,28)
        lead8=Line([1.15,-2.2,0],[XI+.2,-1.15,0],color=FGF)
        self.add(out)
        self.at("where otx2")
        self.add(o); o.become(poly(X0,X0+.001,ty,OTX,.4))
        self.play(reshape(o,lambda a,b: poly(a,b,ty,OTX,.4),(X0,X0+.001),(X0,XI)),FadeIn(lo),run_time=.7)
        self.at("meets gbx2")
        self.add(g); g.become(poly(X_R1-.001,X_R1,ty,GBX,.4))
        self.play(reshape(g,lambda a,b: poly(a,b,ty,GBX,.4),(X_R1-.001,X_R1),(XI,X_R1)),FadeIn(lg),Create(line),run_time=.7)
        self.at("the boundary cells")
        self.play(FadeIn(clause("Where:","where Otx2 meets Gbx2",-3.25)),run_time=.35)
        self.at("become a signaling")
        self.play(FadeIn(band),FadeIn(src),Create(lead),run_time=.45)
        self.at("fgf8 is")
        self.play(FadeIn(key),Create(lead8),run_time=.4)
        self.finish()




# ---------------------------------------------------------------------------------------------
LAM = 2.0
STEP_EDGES = [0.8, 1.8, 3.2]          # distances from the line where the signal drops a step
STEP_OPS = [0.55, 0.38, 0.24, 0.12]   # opacity in each band


def sig(d):
    return float(np.exp(-d / LAM))


def step_op(d):
    for e, o in zip(STEP_EDGES, STEP_OPS):
        if d < e:
            return o
    return STEP_OPS[-1]


def roof_result():
    setsy(1.55); ty=0
    o,g=gene_fills(ty)
    lo,lg=labels_in(ty); lg.move_to([2.6,0,0])
    mid=roofline(X_FM,XI-.05,ty,OTX,10)
    cb=roofline(XI+.05,X_R1,ty,GBX,10)
    lm=lab("midbrain (tectum)",-1.5,3.2,OTX,30)
    lc=lab("cerebellum",3.2,2.7,GBX,30)
    leads=VGroup(Line([-1.5,2.95,0],[-1.3,ty+hh(-1.3),0],color=OTX),
                 Line([3.2,2.4,0],[2.6,ty+hh(2.6),0],color=GBX))
    return VGroup(outline(ty),o,g,lo,lg,dline(ty,XI),sl(XI,XI+.35,ty,FGF),mid,cb,lm,lc,leads)


class S08Idea3(SpokenScene):
    def construct(self):
        setsy(1.55); ty=0
        o,g=gene_fills(ty); lo,lg=labels_in(ty); lg.move_to([2.6,0,0])
        self.add(outline(ty),o,g,lo,lg,dline(ty,XI),sl(XI,XI+.35,ty,FGF))
        simple=lab("On the simplest reading",0,3.25,TEXT,30)
        part=lab("Which part: how much signal a cell gets",0,-3.6,TEXT,28)
        region=lab("Which region: the repressor it carries",0,-3.6,TEXT,28)
        grad=VGroup(*[poly(x,x+.15,ty,FGF,.55*sig(abs(x+.075-XI)),n=5) for x in np.arange(X0,X1-.01,.15)])
        key=VGroup(lab("less signal",-3.0,-3.0,FGF),lab("less signal",4.2,-3.0,FGF),
                   arr([XI-.15,-3.0,0],[-1.7,-3.0,0],FGF,3),
                   arr([XI+.15,-3.0,0],[2.9,-3.0,0],FGF,3))
        rings=waves([XI,ty,0],(.5,.85,1.2),FGF)
        self.at("on the simplest")
        self.play(FadeIn(simple),run_time=.35)
        self.at("how much signal")
        self.play(FadeIn(grad),Create(rings),FadeIn(key),FadeIn(part),run_time=.9)
        self.at("the repressor")
        self.play(FadeOut(part),run_time=.2)
        self.play(FadeIn(region),Indicate(lo,color=OTX),Indicate(lg,color=GBX),run_time=.5)
        self.at("in the roof")
        self.play(FadeOut(simple),FadeOut(key),FadeOut(rings),
                  *[slice.animate.set_fill(FGF,.16*sig(abs(x+.075-XI)))
                    for slice,x in zip(grad,np.arange(X0,X1-.01,.15))],run_time=.5)
        result=roof_result()
        self.at("midbrain in front")
        self.play(Create(result[7]),FadeIn(result[9]),Create(result[11][0]),run_time=.65)
        self.at("cerebellum behind")
        self.play(Create(result[8]),FadeIn(result[10]),Create(result[11][1]),run_time=.65)
        self.finish()


class S09Beat(NarratedScene):
    def construct(self):
        self.add(roof_result(),lab("Which region: the repressor it carries",0,-3.6,TEXT,28))
        self.finish()




# ---------------------------------------------------------------------------------------------
class S10Two(SpokenScene):
    def construct(self):
        setsy(1.55)
        ty = 0
        out = outline(ty)
        grey = poly(X0, X1, ty, GREY, 0.10)
        teal, pink = gene_fills(ty)
        l_o, l_g = labels_in(ty, -3.9, 2.4)
        line = dline(ty, XI)
        self.add(out, grey)
        self.at("the line")
        self.play(Create(line), run_time=0.6)
        self.at("otx2 is on")
        self.add(teal); teal.become(poly(X0,X0+.001,ty,OTX,.4))
        self.play(reshape(teal,lambda a,b: poly(a,b,ty,OTX,.4),(X0,X0+.001),(X0,XI)),FadeIn(l_o),run_time=.7)
        self.at("gbx2 is on")
        self.add(pink); pink.become(poly(X_R1-.001,X_R1,ty,GBX,.4))
        self.play(reshape(pink,lambda a,b: poly(a,b,ty,GBX,.4),(X_R1-.001,X_R1),(XI,X_R1)),FadeIn(l_g),run_time=.7)
        def route(points,col):
            path=VMobject(color=col,stroke_width=5).set_points_as_corners(points)
            end=np.array(points[-1]); cap=Line(end+LEFT*.2,end+RIGHT*.2,color=col,stroke_width=7)
            return VGroup(path,cap)
        i1=route([[-3.9,.45,0],[-3.9,3.25,0],[2.4,3.25,0],[2.4,1.15,0]],OTX)
        i2=route([[2.4,-.45,0],[2.4,-2.7,0],[-3.9,-2.7,0],[-3.9,-1.15,0]],GBX)
        self.at("each represses")
        self.play(Create(i1),FadeIn(lab("represses",-.6,2.85,OTX,28)),run_time=.6)
        self.at("the other")
        self.play(Create(i2),FadeIn(lab("represses",-.6,-3.2,GBX,28)),run_time=.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
NC = 10
CW = 1.08
YB = -2.6
BAR_MAX = 5.3
XA = np.arange(NC) - 4.5
_W = 1.6
A_O = 1 / (1 + np.exp(XA / _W))
A_G = 1 - A_O


def steady(n, K=0.5, steps=80):
    o, g = A_O.copy(), A_G.copy()
    for _ in range(steps):
        o, g = A_O / (1 + (g / K) ** n), A_G / (1 + (o / K) ** n)
    return o, g


def cell_x(i):
    return (i - 4.5) * CW


def bars(o, g):
    grp = VGroup()
    for i in range(NC):
        ho, hg = max(0.03, o[i] * BAR_MAX), max(0.03, g[i] * BAR_MAX)
        grp.add(Rectangle(width=0.42, height=ho, stroke_width=0, fill_color=OTX, fill_opacity=0.9)
                .move_to([cell_x(i) - 0.24, YB + ho / 2, 0]))
        grp.add(Rectangle(width=0.42, height=hg, stroke_width=0, fill_color=GBX, fill_opacity=0.9)
                .move_to([cell_x(i) + 0.24, YB + hg / 2, 0]))
    return grp


class S11Tip(SpokenScene):
    def construct(self):
        o0,g0=A_O.copy(),A_G.copy()
        os,gs=steady(8); ow,gw=steady(1)
        boxes=VGroup(*[Rectangle(width=1.02,height=5.6,stroke_color=GREY,stroke_width=1.5)
                       .move_to([cell_x(i),YB+2.8,0]) for i in range(NC)])
        b=bars(o0,g0)
        axes=VGroup(Line([-5.65,YB,0],[-5.65,3.0,0],color=GREY),
                     lab("amount of protein",-6.5,.3,TEXT,26).rotate(PI/2),
                     lab("cells along the tube, front to back",0,-3.25,TEXT,28),
                     *[VGroup(Line([-5.72,YB+v*BAR_MAX,0],[-5.58,YB+v*BAR_MAX,0],color=GREY),
                              lab(str(v),-5.98,YB+v*BAR_MAX,TEXT,26)) for v in (0,.5,1)],
                     *[lab(str(i+1),cell_x(i),-2.9,TEXT,26) for i in range(NC)])
        legend=VGroup(chip("Otx2",OTX,26).move_to([-4.4,3.4,0]),chip("Gbx2",GBX,26).move_to([4.4,3.4,0]))
        state=lab("overlapping edge",0,3.4,TEXT,28)
        self.add(boxes,b,axes,legend,state)
        hl=boxes[4].copy().set_stroke(TEXT,4)
        this=lab("this cell",-1.2,3.4,TEXT,26)
        self.at("a little more")
        self.play(FadeIn(hl),ReplacementTransform(state,this),run_time=.35)
        mo,mg=o0.copy(),g0.copy(); mo[4]=os[4]; mg[4]=gs[4]
        self.at("makes less")
        self.play(Transform(b,bars(mo,mg)),run_time=.65)
        hl2=boxes[5].copy().set_stroke(TEXT,4)
        neighbor=lab("its neighbour",1.25,3.4,TEXT,26)
        self.at("its neighbor")
        self.play(ReplacementTransform(hl,hl2),ReplacementTransform(this,neighbor),run_time=.35)
        mo[5]=os[5];mg[5]=gs[5]
        self.at("the opposite")
        self.play(Transform(b,bars(mo,mg)),run_time=.65)
        blurred=lab("blurred edge",0,3.4,TEXT,28)
        self.at("blurred edge")
        self.play(FadeOut(hl2),ReplacementTransform(neighbor,blurred),run_time=.25)
        sharp=lab("sharp edge",0,3.4,TEXT,28)
        self.at("can sharpen")
        self.play(Transform(b,bars(os,gs)),ReplacementTransform(blurred,sharp),run_time=.75)
        line=DashedLine([0,YB,0],[0,2.9,0],color=TEXT,stroke_width=4)
        self.at("the line sits")
        self.play(Create(line),run_time=.35)
        self.play(Indicate(line,color=FGF,scale_factor=1),run_time=.45)
        weak=lab("weaker, gradual repression: blurred edge",0,-3.62,TEXT,26)
        strong=lab("strong, switch-like repression: sharp edge",0,-3.62,TEXT,26)
        self.at("how sharp")
        self.play(Transform(b,bars(ow,gw)),FadeOut(line),FadeOut(sharp),FadeIn(weak),run_time=.65)
        self.at("and switch")
        self.play(Transform(b,bars(os,gs)),ReplacementTransform(weak,strong),FadeIn(line),run_time=.65)
        self.finish()




# ---------------------------------------------------------------------------------------------
FORCE_X = 2.2
BACK_X = -.35


def experiment(edge=XI):
    setsy(1.55); ty=0
    o,g=gene_fills(ty,edge,edge)
    lo=lab("Otx2",-3.5,0,TEXT,32)
    lg=lab("Gbx2",2.0 if edge < XI else (edge+.28+X_R1)/2,0,TEXT,26)
    if edge > XI:
        lg.scale_to_fit_width(min(lg.width, X_R1-edge-.46))
    line = dline(ty,edge) if edge == XI else Line([edge,-hh(edge),0],[edge,hh(edge),0],color=TEXT,stroke_width=4)
    return VGroup(outline(ty),o,g,lo,lg,line,sl(edge,edge+.28,ty,FGF,.95))


def move_stage(st, a, b):
    # Rebuild curved fills against the fixed tube at every frame. Interpolating
    # polygon vertices directly creates an incorrect bulging/striped roof.
    return [reshape(st[1],lambda x,y: poly(x,y,0,OTX,.4),(X0,a),(X0,b)),
            reshape(st[2],lambda x,y: poly(x,y,0,GBX,.4),(a,X_R1),(b,X_R1)),
            reshape(st[6],lambda x,y: sl(x,y,0,FGF,.95),(a,a+.28),(b,b+.28)),
            UpdateFromAlphaFunc(st[5],lambda m,t: m.become(Line(
                [a+(b-a)*t,-hh(a+(b-a)*t),0], [a+(b-a)*t,hh(a+(b-a)*t),0],
                color=TEXT,stroke_width=4))),
            Transform(st[4],experiment(b)[4])]


def forced():
    # Solid slate, with an outline: no unkeyed stripe pattern.
    return poly(XI,FORCE_X,0,OTX,.8,stroke=3,sc=OTX)


def predict_final():
    stage=experiment()
    # No signal band or prospective cerebellum result in a prediction.
    stage.remove(stage[6])
    stage[4].move_to([2.95,0,0])
    f=forced()
    tag=lab("forced Otx2",4.7,-2.5,TEXT,28)
    lead=arr([3.5,-2.2,0],[1.5,-.6,0],TEXT,3)
    q=lab("?",XI,2.0,FGF,48)
    return VGroup(stage,f,tag,lead,q,lab("Predict · mouse",-4.4,3.25,TEXT,32),
                  lab("Where does the line go?",0,-3.0,TEXT,30),
                  lab("What happens to the cerebellum?",0,-3.55,TEXT,30))


class S12Predict(SpokenScene):
    def construct(self):
        final=predict_final()
        self.add(final[0],final[5])
        self.at("force otx2")
        self.play(FadeIn(final[1]),FadeIn(final[2]),GrowArrow(final[3]),run_time=.6)
        self.at("where should")
        self.play(FadeIn(final[4]),FadeIn(final[6]),run_time=.35)
        self.at("what happens")
        self.play(FadeIn(final[7]),run_time=.35)
        self.finish()


class S13Pause(NarratedScene):
    def construct(self):
        self.add(predict_final())
        cue=lab("Think · 5",4.9,3.25,FGF,28)
        self.add(cue)
        for n in (4,3,2,1):
            self.wait(1)
            cue.become(lab("Think · "+str(n),4.9,3.25,FGF,28))
        self.finish()


def old_line():
    return VGroup(dline(0,XI,TEXT,3),lab("old line (dashed)",-.7,-2.9,TEXT,26),
                  Line([.4,-2.65,0],[XI,-1.35,0],color=GREY))


def result_back():
    st=experiment(FORCE_X)
    arc=roofline(FORCE_X,X_R1,0,GBX,10)
    return VGroup(st,old_line(),arc,lab("smaller cerebellum",3.9,2.75,GBX,28),
                  Line([3.5,2.45,0],[2.9,hh(2.9),0],color=GBX),
                  lab("new line",FORCE_X,-2.7,TEXT,28),
                  Line([FORCE_X,-2.4,0],[FORCE_X,-hh(FORCE_X),0],color=TEXT))


class S14R1(SpokenScene):
    def construct(self):
        st=experiment(); self.add(st,forced(),lab("mouse",5.6,3.25))
        arc=roofline(XI,X_R1,0,GBX,10)
        cb=lab("cerebellum",3.7,2.75,GBX,28)
        self.add(arc,cb)
        target=experiment(FORCE_X); ghost=old_line()
        self.at("the line moves")
        self.play(*move_stage(st,XI,FORCE_X),FadeIn(ghost),FadeIn(lab("new line",FORCE_X,-2.7,TEXT,28)),
                  Create(Line([FORCE_X,-2.4,0],[FORCE_X,-hh(FORCE_X),0],color=TEXT)),run_time=.8)
        self.at("with its band")
        self.play(Indicate(st[6],color=FGF,scale_factor=1),run_time=.5)
        self.at("cerebellum is")
        self.play(reshape(arc,lambda a,b: roofline(a,b,0,GBX,10),(XI,X_R1),(FORCE_X,X_R1)),
                  Transform(cb,lab("smaller cerebellum",3.9,2.75,GBX,28)),
                  Create(Line([3.5,2.45,0],[2.9,hh(2.9),0],color=GBX)),run_time=.8)
        self.at("broccoli")
        self.play(FadeIn(lab("Broccoli, Boncinelli and Wurst, 1999",0,-3.45,TEXT,28)),run_time=.4)
        self.finish()


def forward_result():
    return VGroup(experiment(BACK_X),old_line(),lab("line moves forward",-2.7,3.25,TEXT,32),
                  arr([XI,2.65,0],[BACK_X,2.65,0],TEXT),
                  lab("Millet and colleagues · Joyner laboratory · 1999",0,-3.35,TEXT,26))


class S15R2(SpokenScene):
    def construct(self):
        st=experiment(); self.add(st,lab("mouse",5.6,3.25))
        title=lab("the reverse",-3.8,3.25,TEXT,32)
        self.at("the reverse")
        self.play(FadeIn(title),run_time=.3)
        spreading=poly(BACK_X,XI,0,GBX,.8,stroke=3,sc=GBX)
        forced_tag=lab("forced Gbx2",-1.0,-3.15,GBX,28)
        forced_lead=arr([-.75,-2.85,0],[(BACK_X+XI)/2,-.5,0],GBX,3)
        self.at("gbx2")
        self.add(spreading); spreading.become(poly(XI-.001,XI,0,GBX,.8,stroke=3,sc=GBX))
        self.play(reshape(spreading,lambda a,b: poly(a,b,0,GBX,.8,stroke=3,sc=GBX),(XI-.001,XI),(BACK_X,XI)),
                  FadeIn(forced_tag),GrowArrow(forced_lead),run_time=.7)
        self.at("moved the line")
        self.remove(title)
        self.play(*move_stage(st,XI,BACK_X),FadeOut(spreading),FadeOut(forced_tag),FadeOut(forced_lead),FadeIn(old_line()),
                  FadeIn(lab("line moves forward",-2.7,3.25,TEXT,32)),
                  GrowArrow(arr([XI,2.65,0],[BACK_X,2.65,0],TEXT)),run_time=.8)
        self.play(FadeIn(lab("Millet and colleagues · Joyner laboratory · 1999",0,-3.35,TEXT,26)),run_time=.3)
        self.finish()


class S16Beat(NarratedScene):
    def construct(self):
        self.add(forward_result(),lab("mouse",5.6,3.25))
        self.finish()


class S17Move(SpokenScene):
    def construct(self):
        st=experiment(); self.add(st)
        title=lab("Move-it test",-3.9,3.25,TEXT,34)
        caption=lab("move the Otx2 edge",0,-3.25,TEXT,30)
        a=arr([XI,2.9,0],[FORCE_X,2.9,0],OTX)
        back=lab("back",3.05,2.65,OTX,28)
        self.at("move it")
        self.play(FadeIn(title),run_time=.3)
        self.at("change where")
        self.play(GrowArrow(a),FadeIn(caption),FadeIn(back),
                  reshape(st[1],lambda x,y: poly(x,y,0,OTX,.4),(X0,XI),(X0,FORCE_X)),
                  reshape(st[2],lambda x,y: poly(x,y,0,GBX,.4),(XI,X_R1),(FORCE_X,X_R1)),
                  Transform(st[4],experiment(FORCE_X)[4]),run_time=.65)
        self.at("see if the pattern")
        self.play(UpdateFromAlphaFunc(st[5],lambda m,t: m.become(Line([XI+(FORCE_X-XI)*t,-hh(XI+(FORCE_X-XI)*t),0],[XI+(FORCE_X-XI)*t,hh(XI+(FORCE_X-XI)*t),0],color=TEXT,stroke_width=4))),
                  reshape(st[6],lambda x,y: sl(x,y,0,FGF,.95),(XI,XI+.28),(FORCE_X,FORCE_X+.28)),run_time=.65)
        self.at("the line follows")
        self.play(*move_stage(st,FORCE_X,BACK_X),Transform(a,arr([FORCE_X,2.9,0],[BACK_X,2.9,0],OTX)),
                  ReplacementTransform(back,lab("forward",3.8,3.25,OTX,28)),
                  ReplacementTransform(caption,lab("the line follows the repressors",0,-3.25,FGF,32)),run_time=.9)
        self.finish()


class S18Bridge(SpokenScene):
    def construct(self):
        st=experiment(); st.remove(st[6]); st[4].move_to([3.0,0,0]); self.add(st)
        fe=fence([XI,0]).scale(.8)
        fence_tag=lab("old picture: a fence",-2.2,3.15,GREY,28)
        self.add(fe,fence_tag)
        bf=sl(XI,XI+.5,0,FGF,.9); bw=sl(XI-.5,XI,0,WNT,.9)
        lf=lab("FGF8 just behind the line",3.6,-2.9,FGF,28)
        lw=lab("Wnt1 just in front",.35,3.15,WNT,28)
        af=Line([1.9,-2.6,0],[XI+.25,-1.3,0],color=FGF)
        aw=Line([XI-.25,2.85,0],[XI-.25,hh(XI-.25)+.05,0],color=WNT)
        self.at("right at the line")
        self.play(Indicate(st[5],color=TEXT),run_time=.4)
        self.at("fgf8 just")
        self.play(FadeOut(fe),FadeOut(fence_tag),FadeIn(bf),FadeIn(lf),Create(af),run_time=.5)
        self.at("wnt1 just")
        self.play(FadeIn(bw),FadeIn(lw),Create(aw),run_time=.5)
        self.at("a fence")
        self.play(Indicate(bf,color=FGF,scale_factor=1),Indicate(bw,color=WNT,scale_factor=1),run_time=.6)
        self.finish()


class S19Take(SpokenScene):
    def construct(self):
        st=experiment(); st.remove(st[6]); self.add(st)
        tag=lab("Takeaway",0,3.25,TEXT,32)
        self.add(tag)
        self.at("two repressors")
        self.play(FadeIn(lab("Two repressors place the line.",0,-3.05,TEXT,32)),
                  Indicate(st[3],color=OTX),Indicate(st[4],color=GBX),run_time=.45)
        self.at("place the line")
        self.play(Indicate(st[5],color=FGF,scale_factor=1),run_time=.45)
        self.at("next")
        self.play(FadeIn(lab("Is that line a source?",0,-3.65,FGF,28)),run_time=.5)
        self.finish()




class S20End(EndCard):
    LINE = "Two repressors place the line. Next: is it a source?"

    def construct(self):
        rule=lab("Two repressors place the line.",0,1.0,TEXT,42)
        question=lab("Next: is it a source?",0,-.4,FGF,42)
        self.add(rule,question)
        self.play(FadeIn(lab("biochemistrypedia.com",0,-2,OTX,26)),run_time=.4)
        self.finish()
