"""Size Counts the Doublings  (chapter 1 of "When Building Goes Wrong: Microcephaly, Zika and Lissencephaly")

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, shared by every chapter of this lesson)
  BLUE   = progenitors (radial glia), their fibers, "too few made", the pool of progenitors
  YELLOW = neurons, "made but misplaced", the cortex ribbon
  RED    = what goes wrong: the cutoff tail, mutant / stalled, lost pool
  GREEN  = the normal X (chapters 2 and 3)
  ORANGE = spindle pole, and the ASPM gene
  TEAL   = microtubules (chapters 2 and 3)
  PURPLE = doublecortin (chapter 3)
  GOLD   = the switch from making progenitors to making neurons (a neurogenic division)
  GREY   = tissue outlines, ventricle, axes, labels, de-emphasized
  WHITE (TEXT) = nucleus, tape measure, the population curve, headlines
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def arr(a, b, color=GREY, w=4, tip=0.2):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=14)


def lab_right(text, color, x, y, tip, size=26):
    """text whose left edge sits at x, with an arrow from it to `tip`."""
    t = T(text, size, color)
    t.move_to([x + t.width / 2, y, 0])
    a = arr([x - 0.12, y, 0], tip, color)
    return VGroup(t, a)


def swap(scene, old, new, run_time=0.3):
    scene.play(ReplacementTransform(old, new), run_time=run_time)
    return new


def soma(x, y, r=0.26):
    body = Circle(radius=r, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.45)
    nuc = Dot(radius=r * 0.4, color=TEXT)
    return VGroup(body, nuc).move_to([x, y, 0])


# ---- the cortical wall (chapter 1 uses it in s02, s03, s12) -------------------------------------
WCX = -2.9
GOFF = [-2.2, -1.1, 0, 1.1, 2.2]

def wall():
    out = RoundedRectangle(corner_radius=0.15, width=5.8, height=6.4, stroke_color=GREY, stroke_width=3).move_to([WCX, 0, 0])
    bars = VGroup(*[Rectangle(width=5.6, height=0.16, stroke_width=0, fill_color=GREY, fill_opacity=0.7).move_to([WCX,y,0]) for y in (-2.95,2.95)])
    return VGroup(out, *bars)

def glia(off):
    x = WCX + off
    cell = Ellipse(width=0.48, height=0.7, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.4).move_to([x,-2.4,0])
    fib = Line([x,-2.05,0],[x,2.85,0],color=BLUE,stroke_width=3)
    return VGroup(fib,cell)

# Matched coronal schematics in the opening and return. Central lateral ventricles,
# a midline cleft, shallow folds in child 1, and a smooth thick ribbon in child 2.
L_BRAIN = dict(cx=-3.35, cy=0.20, w=4.4, h=4.3, rib=0.40)
R_BRAIN = dict(cx=3.35, cy=0.20, w=5.4, h=5.4, rib=0.95)

def brain_parts(cx,cy,w,h,rib):
    def contour(inset=0):
        pts=[]
        for t in np.linspace(0,2*PI,180):
            # A superior midline cleft and a flatter inferior coronal surface.
            x=(w/2-inset)*np.cos(t)
            y=(h/2-inset)*np.sin(t)
            if y>0: y-=0.48*np.exp(-(x/0.28)**2)
            else: y=max(y,-h*0.37+inset*0.7)
            if rib<0.5:
                y+=0.13*np.cos(12*t)*abs(np.cos(t))**2
            pts.append([cx+x,cy+y,0])
        ob=VMobject().set_points_smoothly(pts+[pts[0]])
        return ob
    outline=contour().set_stroke(GREY,4)
    ribbon=contour().set_stroke(width=0).set_fill(YELLOW,0.35)
    core=contour(rib).set_stroke(YELLOW,2).set_fill(BG,1)
    ventricles=VGroup()
    for sign in (-1,1):
        v=VMobject(color=GREY,stroke_width=3).set_points_smoothly([[cx+sign*x,cy+y,0] for x,y in [(0.16,0.1),(0.65,0.5),(0.9,0.3),(0.55,-0.15),(0.25,-0.42)]])
        ventricles.add(v)
    rings=VGroup(*[contour(rib*f).set_fill(opacity=0).set_stroke(YELLOW,2) for f in (0.27,0.53,0.78)]) if rib<0.5 else VGroup()
    return outline,ribbon,VGroup(core,ventricles),rings

def brain_pair():
    left=VGroup(*brain_parts(**L_BRAIN)); right=VGroup(*brain_parts(**R_BRAIN))
    labels=VGroup()
    for x,num,txt in [(-3.35,1,'small, layers in order'),(3.35,2,'thick, nearly smooth')]:
        labels.add(T(f'Child {num}',30,TEXT).move_to([x,-2.48,0]),T(txt,26,TEXT).move_to([x,-3.0,0]))
    return left,right,labels



# ---- the doubling tree (s04, s06) ----------------------------------------------------------------
TX0, TDX = -5.6, 1.5


def tpos(k, i, n=4):
    span = 2 ** (n - k)
    slot = i * span + (span - 1) / 2
    return np.array([TX0 + TDX * k, 3.0 - slot * 0.4, 0.0])


def build_tree(n=4):
    rad = [0.17, 0.17, 0.16, 0.15, 0.14]
    edges = [[]] + [[Line(tpos(k - 1, i // 2), tpos(k, i), color=GREY, stroke_width=2.5) for i in range(2 ** k)]
                    for k in range(1, n + 1)]
    dots = [[Dot(tpos(k, i), radius=rad[k], color=BLUE) for i in range(2 ** k)] for k in range(n + 1)]
    return dots, edges


# ---- the pool bar (s09, s10, s11) ----------------------------------------------------------------
BARX, BASE, BH, BW = -4.65, -2.9, 5.9, 2.6

def pool_bar(getf):
    outline=Rectangle(width=BW,height=BH,stroke_color=GREY,stroke_width=3).move_to([BARX,BASE+BH/2,0])
    def fill():
        h=max(0.01,BH*getf())
        return Rectangle(width=BW,height=h,stroke_width=0,fill_color=BLUE,fill_opacity=0.7).move_to([BARX,BASE+h/2,0])
    pct=always_redraw(lambda:T(f'{100*getf():.0f}%',44,BLUE,weight=BOLD).move_to([BARX,BASE+BH*getf()-0.45,0]))
    normal=T('normal = 100%',26,TEXT).move_to([BARX,3.4,0])
    under=T('relative pool',26,TEXT).move_to([BARX,-3.35,0])
    return outline,always_redraw(fill),pct,normal,under



# ---- the SD axis and head (s13, s14) -------------------------------------------------------------
AXX = -0.9


def ysd(sd):
    return 2.45 + 0.9 * sd


def sd_axis():
    line = Line([AXX, ysd(0), 0], [AXX, ysd(-6), 0], color=GREY, stroke_width=3)
    ticks = VGroup(*[Line([AXX - 0.1, ysd(-s), 0], [AXX + 0.1, ysd(-s), 0], color=GREY, stroke_width=3) for s in range(7)])
    return VGroup(line, ticks)


def head(cx=-3.3,cy=0):
    # Sagittal profile: occiput at left, brow/nose at right, neck inferiorly.
    pts=[[-0.65,-2.85],[-1.5,-2.15],[-2.2,-0.8],[-2.3,0.7],[-1.65,2.2],[-0.4,2.8],[1.0,2.55],[1.85,1.55],[1.95,0.85],[2.35,0.2],[1.98,0.02],[1.9,-0.7],[1.35,-1.3],[0.7,-1.6],[0.6,-2.85]]
    skull=VMobject(color=GREY,stroke_width=4).set_points_smoothly([[cx+x,cy+y,0] for x,y in pts])
    ear=Ellipse(width=0.45,height=0.7,color=GREY).move_to([cx+0.05,cy+0.05,0])
    eye=Line([cx+1.48,cy+0.8,0],[cx+1.77,cy+0.8,0],color=GREY,stroke_width=4)
    return VGroup(skull,ear,eye)

def tape(cx=-3.3,cy=0):
    # Visible near side of a circumferential band, above ear and eyebrow.
    pts=[[cx+x,cy+y,0] for x,y in [(-2.25,0.75),(-1.6,0.52),(-0.5,0.45),(0.6,0.55),(1.91,1.04)]]
    band=VMobject(color=TEXT,stroke_width=14).set_points_smoothly(pts)
    ticks=VGroup(*[Line([cx+x,cy+0.39,0],[cx+x,cy+0.58,0],color=BG,stroke_width=2) for x in np.arange(-1.4,0.7,0.3)])
    back_arc=VMobject(color=TEXT,stroke_width=7).set_points_smoothly(
        [[cx+x,cy+y,0] for x,y in [(-2.25,0.75),(-1.65,1.25),(-0.3,1.48),(1.15,1.35),(1.91,1.04)]])
    back=DashedVMobject(back_arc,num_dashes=12,dashed_ratio=0.7)
    return VGroup(back,band,ticks)



# ---- the bell (s15, s16) -------------------------------------------------------------------------
BASEY = -2.4
BELLH = 5.1


def sdx(sd):
    return 0.85 * sd + 3.2


def pdf(z):
    return np.exp(-z * z / 2) / np.sqrt(2 * np.pi)


def bell_curve(lo=-6.4, hi=3.2):
    pts = [[sdx(z), BASEY + BELLH * pdf(z) / 0.3989, 0] for z in np.linspace(lo, hi, 240)]
    c = VMobject(stroke_color=TEXT, stroke_width=4)
    c.set_points_as_corners(pts)
    return c


def bell_axis():
    line = Line([sdx(-6.4), BASEY, 0], [sdx(3.2), BASEY, 0], color=GREY, stroke_width=3)
    ticks = VGroup()
    labs = VGroup()
    for s in (-4, -2, 0, 2):
        ticks.add(Line([sdx(s), BASEY - 0.1, 0], [sdx(s), BASEY + 0.1, 0], color=GREY, stroke_width=3))
        txt = {0: "0 = mean"}.get(s, f"{s}".replace("-", "−"))
        labs.add(T(txt, 26, TEXT).move_to([sdx(s), BASEY - 0.42, 0]))
    cap = T("head size for age, in SD from the mean", 26, TEXT).move_to([sdx(-1), BASEY - 0.95, 0])
    return VGroup(line, ticks), labs, cap


# ---- icons for the closing cards ----------------------------------------------------------------
def mini_tree(x, y, color=BLUE):
    pts = [(0, 0)] + [(0.6, s * 0.35) for s in (-1, 1)] + [(1.2, s * 0.6 + t * 0.2) for s in (-1, 1) for t in (-1, 1)]
    par = [None, 0, 0, 1, 1, 2, 2]
    g = VGroup()
    for i, (px, py) in enumerate(pts):
        if par[i] is not None:
            qx, qy = pts[par[i]]
            g.add(Line([x + qx, y + qy, 0], [x + px, y + py, 0], color=GREY, stroke_width=2.5))
    for px, py in pts:
        g.add(Dot([x + px, y + py, 0], radius=0.11, color=color))
    return g


def mini_climb(x, y):
    fib = Line([x, y - 0.8, 0], [x, y + 0.8, 0], color=BLUE, stroke_width=3, stroke_opacity=0.8)
    n1 = Dot([x, y - 0.8, 0], radius=0.13, color=YELLOW)
    n2 = Dot([x, y + 0.35, 0], radius=0.13, color=YELLOW)
    ar = arr([x + 0.3, y - 0.5, 0], [x + 0.3, y + 0.5, 0], YELLOW, 3, 0.16)
    return VGroup(fib, n1, n2, ar)


# =============================================================================================
class S00Title(TitleCard):
    LESSON = "When Building Goes Wrong: Microcephaly, Zika and Lissencephaly"
    TITLE = "Size Counts the Doublings"
    def construct(self):
        title=T(self.TITLE,54,TEXT,font=TITLE_FONT).move_to([0,0.3,0])
        brand=T('BIOCHEMISTRYPEDIA',26,TEAL).move_to([0,2,0])
        lesson=VGroup(T('When Building Goes Wrong',28,TEXT),T('Microcephaly, Zika and Lissencephaly',26,TEXT)).arrange(DOWN,buff=0.2).move_to([0,-1.2,0])
        self.add(title,brand,lesson,Line([-2,-0.35,0],[2,-0.35,0],color=GOLD,stroke_width=4))
        self.finish()

class S01Q(SpokenScene):
    def construct(self):
        left,right,labels=brain_pair()
        # Complete silhouettes from frame one; reveal the cortical ribbons on cue.
        self.add(left[0],right[0],labels[0],labels[2])
        self.at('One is small')
        self.play(Indicate(left[0],color=TEXT,scale_factor=1.03),run_time=0.45)
        self.at('with its layers')
        self.play(FadeIn(VGroup(*left[1:])),FadeIn(labels[1]),run_time=0.65)
        self.at('thick and nearly smooth')
        self.play(FadeIn(VGroup(*right[1:])),FadeIn(labels[3]),run_time=0.65)
        self.at('Which step')
        q=T('Which step failed in each?',36,TEXT).move_to([0,3.5,0])
        self.play(FadeIn(q),run_time=0.35)
        self.finish()

class S02Jobs(SpokenScene):
    def construct(self):
        wl=wall(); gs=VGroup(*[glia(o) for o in GOFF])
        self.add(wl,T('outer surface',26,TEXT).move_to([-2.9,3.5,0]),T('ventricle',26,TEXT).move_to([-2.9,-3.5,0]))
        title=T('Job 1: make neurons',32,BLUE).move_to([3.2,3.15,0])
        self.at('radial glia')
        self.play(FadeIn(gs),FadeIn(title),run_time=0.4)
        lab=T('radial glia',28,BLUE).move_to([2.5,2.35,0]); self.add(lab)
        # Link this enlarged division to one particular ventricular glial cell.
        parent=Ellipse(width=0.85,height=1.25,color=BLUE,fill_color=BLUE,fill_opacity=0.45).move_to([3.2,0.6,0])
        self.at('divide')
        link=VMobject(color=BLUE,stroke_width=3).set_points_as_corners([[-0.4,-2.4,0],[0.3,-2.4,0],[0.3,0.6,0],[2.6,0.6,0]])
        inset_label=T('one glial cell dividing',26,BLUE).move_to([3.2,1.65,0])
        self.play(TransformFromCopy(gs[-1][1],parent),Create(link),FadeIn(inset_label),run_time=0.25)
        daughters=VGroup(*[parent.copy().move_to([x,0.6,0]) for x in (2.15,4.25)])
        self.at('more of themselves')
        self.play(ReplacementTransform(parent,daughters),FadeOut(link),FadeOut(inset_label),run_time=0.6)
        more=T('two progenitors',28,BLUE).move_to([3.2,-0.5,0]); self.add(more)
        self.at('and then neurons')
        neuron=soma(4.25,-1.7,0.43)
        retained=daughters[1].copy().move_to([2.15,-1.7,0])
        self.play(ReplacementTransform(daughters[1],VGroup(retained,neuron)),FadeOut(more),run_time=0.6)
        self.add(T('progenitor + neuron',28,YELLOW).move_to([3.2,-2.8,0]))
        self.finish()

class S03Move(SpokenScene):
    def construct(self):
        wl=wall(); gl=VGroup(*[glia(o) for o in GOFF]); n=soma(WCX,-1.6)
        self.add(wl,gl,n,T('Job 2: move them',32,YELLOW).move_to([3.2,2.8,0]))
        self.at('climbs a glial fiber')
        self.play(n.animate.move_to([WCX,2.3,0]),run_time=1.25)
        self.at('so too few')
        slot=Ellipse(width=0.55,height=0.8,color=BLUE,stroke_width=3).move_to([WCX+1.1,-2.4,0])
        self.play(FadeOut(gl[3]),FadeIn(slot),run_time=0.25)
        c1=chip('Too few made',BLUE,30).move_to([3.4,-1.9,0])
        link1=arr([1.4,-1.9,0],[WCX+1.1,-2.05,0],BLUE)
        self.play(FadeIn(c1),GrowArrow(link1),run_time=0.4)
        self.at('or they can stall')
        stalled=soma(WCX,-0.4); stalled[0].set_stroke(RED,5)
        c2=chip('Made but misplaced',YELLOW,28).move_to([3.4,0.4,0])
        self.play(FadeIn(stalled),FadeIn(c2),GrowArrow(arr([1.0,0.4,0],[WCX+0.35,-0.4,0],YELLOW)),run_time=0.5)
        self.finish()



class S04Double(SpokenScene):
    """the first job multiplies: a doubling tree and a counter."""

    def construct(self):
        dots, edges = build_tree()

        def counter(k):
            g = VGroup(T(f"round {k}", 30, GREY), M(str(2 ** k), 96, BLUE), T("progenitors in the pool", 26, BLUE))
            g.arrange(DOWN, buff=0.3).move_to([4.0, 0.2, 0])
            return g

        cnt = counter(0)
        self.play(FadeIn(dots[0][0], scale=0.3), FadeIn(cnt), run_time=0.6)

        def grow(k):
            return [Create(e) for e in edges[k]] + [FadeIn(d, scale=0.3) for d in dots[k]]

        self.at("each division")
        self.play(*grow(1), ReplacementTransform(cnt, (cnt1 := counter(1))), run_time=0.8)
        cnt = cnt1
        self.at("two progenitors")
        self.play(Indicate(VGroup(*dots[1]), color=TEXT, scale_factor=1.5), run_time=0.7)

        self.at("every round")
        self.play(*grow(2), ReplacementTransform(cnt, (cnt2 := counter(2))), run_time=0.6)
        cnt = cnt2
        self.at("doubles the pool")
        self.play(*grow(3), ReplacementTransform(cnt, (cnt3 := counter(3))), run_time=0.6)
        cnt = cnt3
        self.wait(0.3)
        self.play(*grow(4), ReplacementTransform(cnt, (cnt4 := counter(4))), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Table(SpokenScene):
    def construct(self):
        # log2 scale makes every round visible; every height is computed from 100*2**k.
        x0,y0=-4.95,-2.65
        bars=[]
        self.add(Line([x0-0.4,y0,0],[0.2,y0,0],color=GREY),Line([x0-0.4,y0,0],[x0-0.4,2.6,0],color=GREY))
        self.add(T('progenitors in the pool',28,BLUE).move_to([-3.1,3.3,0]),T('log₂ scale',26,TEXT).move_to([-3.1,2.75,0]),T('round',26,TEXT).move_to([-3,-3.4,0]))
        for j,k in enumerate((0,3,7)):
            yy=y0+0.6*(k+1)
            self.add(T(f'{100*2**k:,}',26,TEXT).move_to([-5.5,yy,0],aligned_edge=RIGHT))
        for k in range(8):
            x=x0+0.73*k; h=0.6*(k+1)
            bars.append(Rectangle(width=0.48,height=h,stroke_width=0,fill_color=BLUE,fill_opacity=0.75).move_to([x,y0+h/2,0]))
            self.add(T(str(k),26,TEXT).move_to([x,-3,0]))
        count=T('100',32,BLUE).move_to([-3.0,1.6,0]); self.add(count,bars[0])
        # The counter changes only as the matching bar grows.
        for k in range(1,8):
            nxt=T(f'{100*2**k:,}',32,BLUE).move_to([-3.0,1.6,0])
            self.play(GrowFromEdge(bars[k],DOWN),ReplacementTransform(count,nxt),run_time=0.13); count=nxt
        self.play(FadeOut(count),run_time=0.1)
        self.add(T('Switch timing → pool',30,TEXT).move_to([3.6,2.75,0]))
        def row(label,val,ratio,y,col):
            return VGroup(T(label,26,col).move_to([3.45,y,0]),T(f'{val:,}  ·  {ratio}',32,col).move_to([3.45,y-0.62,0]))
        self.add(row('normal: 7 rounds',12800,'1',1.8,TEXT))
        self.at('pool is halved')
        self.play(bars[6].animate.set_color(GOLD),FadeIn(row('switch 1 round early',6400,'one half',0.05,GOLD)),run_time=0.45)
        self.at('falls to a quarter')
        self.play(bars[5].animate.set_color(GOLD),FadeIn(row('switch 2 rounds early',3200,'one quarter',-1.7,GOLD)),run_time=0.45)
        self.finish()

class S06Real(SpokenScene):
    def construct(self):
        # Exactly ten parent divisions; one neurogenic outcome leaves 19/20 progenitors.
        title=T('10 divisions → normally 20 progenitors',32,BLUE).move_to([0,3.3,0])
        parents=VGroup(*[Dot([-5.6+i*1.24,2.25,0],radius=0.16,color=BLUE) for i in range(10)])
        self.add(title,parents)
        children=VGroup(); links=VGroup()
        for i,p in enumerate(parents):
            x=p.get_x()
            for dx in (-0.25,0.25):
                links.add(Line(p.get_center(),[x+dx,1.05,0],color=GREY,stroke_width=2))
                children.add(Dot([x+dx,1.05,0],radius=0.13,color=BLUE))
        self.at('one in ten chance')
        self.play(Create(links),FadeIn(children),run_time=0.5)
        stat=T('1 in 10 divisions',32,GOLD).move_to([-3.7,-0.1,0])
        self.add(stat)
        self.at('coming out neurogenic')
        chosen=children[11]; neuron=soma(chosen.get_x(),1.05,0.18)
        self.play(ReplacementTransform(chosen,neuron),links[10].animate.set_color(GOLD),links[11].animate.set_color(GOLD),run_time=0.4)
        self.add(T('19 progenitors / 20 normal',30,BLUE).move_to([2.8,-0.1,0]),T('on average: 1.9 per division',30,TEXT).move_to([0,-0.85,0]))
        self.at('for that round only')
        # Zoom the surviving sister: it is cyan and divides symmetrically next round.
        sister=children[10]
        zoom=Dot([-2.2,-1.95,0],radius=0.2,color=BLUE)
        self.play(TransformFromCopy(sister,zoom),run_time=0.25)
        offspring=VGroup(Dot([-0.5,-1.5,0],radius=0.2,color=BLUE),Dot([-0.5,-2.4,0],radius=0.2,color=BLUE))
        branches=VGroup(*[Line(zoom.get_center(),d.get_center(),color=BLUE) for d in offspring])
        self.play(Create(branches),FadeIn(offspring),run_time=0.35)
        self.add(T('next round: two progenitors',28,BLUE).move_to([3.1,-1.95,0]))
        self.add(T('illustrative model, one round at a time',26,TEXT).move_to([0,-2.95,0]),T('(a permanent switch would cost more)',26,TEXT).move_to([0,-3.45,0]))
        self.finish()



def pred_parts():
    title = T("Predict", 56, GOLD, weight=BOLD).move_to([0, 3.0, 0])
    l1 = fit(T("Each division: a 1 in 10 chance of coming out neurogenic,", 30, TEXT), max_w=12).move_to([0, 1.95, 0])
    l2 = T("for that round only.", 30, TEXT).move_to([0, 1.45, 0])
    l3 = T("Run 10 rounds.", 42, BLUE, weight=BOLD).move_to([0, 0.5, 0])
    q = T("How big is the pool, compared with normal?", 38, TEXT).move_to([0, -0.6, 0])
    ch = VGroup(*[chip(s, BLUE, 40).move_to([x, -2.1, 0]) for s, x in (("about 90%", -4.2), ("about 60%", 0), ("about 10%", 4.2))])
    return title, VGroup(l1, l2), l3, q, ch


class S07Pred(SpokenScene):
    def construct(self):
        title,ctx,l3,q,ch=pred_parts()
        self.add(title,ctx)
        self.at('run ten rounds')
        self.play(FadeIn(l3),run_time=0.3)
        self.at('How big is it')
        self.play(FadeIn(q),run_time=0.35)
        self.at('compared with normal')
        self.play(FadeIn(ch),run_time=0.35)
        self.finish()

class S08Pause(NarratedScene):
    def construct(self):
        self.add(*pred_parts())
        cue=T('Pause the video and decide',26,TEXT).move_to([0,-3.0,0]); self.add(cue)
        track=Line([-5.8,-3.5,0],[5.8,-3.5,0],color=GREY,stroke_width=5)
        progress=Line([-5.8,-3.5,0],[5.8,-3.5,0],color=GOLD,stroke_width=5)
        self.add(track); self.play(Create(progress),run_time=5,rate_func=linear); self.finish()

class S09Reveal(SpokenScene):
    def construct(self):
        f=ValueTracker(1)
        outline,fill,pct,normal,under=pool_bar(f.get_value)
        self.add(outline,fill,normal,under)
        # The spoken answer begins immediately. Show the causal arithmetic before
        # completing the bar's fall on the later 'falls five percent short' clause.
        answer=T('From divisions to the pool',34,TEXT).move_to([2.0,2.7,0])
        self.add(answer)
        a=T('0.9 × 2 + 0.1 × 1 = 1.9',34,BLUE).move_to([2,1.45,0])
        b=T('1.9 / 2 = 0.95 per round',34,BLUE).move_to([2,0.15,0])
        c=T('0.95¹⁰ ≈ 0.60',44,BLUE,weight=BOLD).move_to([2,-1.7,0])
        self.at('one progenitor short')
        self.play(FadeIn(a),run_time=0.45)
        self.at('each round falls')
        self.play(FadeIn(b),run_time=0.4)
        self.at('short of doubling')
        self.add(pct)
        self.play(f.animate.set_value(0.95**10),FadeIn(c),run_time=0.85)
        self.finish()

class S10Compound(SpokenScene):
    def construct(self):
        n=ValueTracker(10)
        self.add(*pool_bar(lambda:0.95**n.get_value()))
        counter=always_redraw(lambda:T(f'round {round(n.get_value())}',48,TEXT).move_to([2.1,2.4,0]))
        self.add(counter,T('illustrative, same one-in-ten fault',26,TEXT).move_to([2,3.3,0]))
        self.at('costs two fifths')
        lost=T('lost: two fifths at round 10',30,RED).move_to([2,0.7,0])
        self.play(FadeIn(lost),run_time=0.35)
        self.at('Small faults compound')
        self.play(FadeOut(lost),FadeIn(T('Small faults compound',38,RED,weight=BOLD).move_to([2,-1.3,0])),run_time=0.2)
        # Hold the narrated ten-round result while the conclusion lands.
        self.finish()

class S11Beat(NarratedScene):
    def construct(self):
        self.add(*pool_bar(lambda:0.95**10),T('round 10',48,TEXT).move_to([2.1,2.4,0]),T('illustrative, same one-in-ten fault',26,TEXT).move_to([2,3.3,0]),T('Small faults compound',38,RED,weight=BOLD).move_to([2,-1.3,0]))
        self.finish()

class S12Second(SpokenScene):
    def construct(self):
        n=soma(WCX,-1.6,0.35)
        self.add(wall(),VGroup(*[glia(o) for o in GOFF]),n,T('The second job',36,YELLOW).move_to([3.0,2.8,0]))
        self.at('does not multiply')
        self.play(n.animate.move_to([WCX,-0.05,0]),run_time=0.65)
        self.at('neuron that stalls')
        self.play(n[0].animate.set_stroke(RED,5),run_time=0.25)
        stalled_label=T('stalled neuron',28,RED).move_to([-3.25,0.7,0])
        backing=BackgroundRectangle(stalled_label,color=BG,fill_opacity=1,buff=0.14)
        self.add(backing,stalled_label)
        self.at('no descendants')
        ghosts=VGroup()
        for yy in (-1.4,1.2):
            ghosts.add(DashedLine([WCX+0.4,-0.05,0],[0.65,yy,0],color=GREY,stroke_width=3))
            ghosts.add(Circle(radius=0.38,color=GREY).move_to([1,yy,0]))
            ghosts.add(Line([0.72,yy-0.28,0],[1.28,yy+0.28,0],color=RED,stroke_width=4),Line([0.72,yy+0.28,0],[1.28,yy-0.28,0],color=RED,stroke_width=4))
        self.play(Create(ghosts),FadeIn(T('no descendants',34,TEXT).move_to([3.4,-0.05,0])),run_time=0.65)
        self.finish()



def sd_labels():
    labs = VGroup()
    for s in range(7):
        if s == 0:
            labs.add(T("0 (mean)", 26, TEXT).move_to([0.0, ysd(0), 0], aligned_edge=LEFT) if False else T("0 (mean)", 26, TEXT))
        elif s == 2:
            labs.add(T("−2 SD: WHO cutoff", 28, RED, weight=BOLD))
        else:
            labs.add(T(f"−{s}", 26, TEXT))
        labs[-1].move_to([AXX + 0.45 + labs[-1].width / 2, ysd(-s), 0])
    return labs


class S13Tape(SpokenScene):
    def construct(self):
        head_center=np.array([-2.8,0,0])
        hd=head(cx=-2.8).scale(1.1,about_point=head_center)
        ax=sd_axis().shift(RIGHT*2.8); labs=sd_labels().shift(RIGHT*2.8)
        self.add(hd,ax,labs,T('head size for age',28,TEXT).move_to([3.4,3.3,0]))
        self.at('a tape measure')
        tp=tape(cx=-2.8).scale(1.1,about_point=head_center)
        self.play(Create(tp),run_time=0.55)
        self.add(T('above eyebrows and ears',26,TEXT).move_to([-2.8,3.5,0]))
        self.at('The cutoff')
        self.play(Indicate(labs[2],color=TEXT,scale_factor=1.03),run_time=0.5)
        self.at('two standard deviations')
        dot=Dot([AXX+2.8,ysd(-2),0],radius=0.17,color=RED)
        self.play(FadeIn(dot),run_time=0.35)
        self.at('below the mean')
        ar=arr([AXX+2.3,ysd(0),0],[AXX+2.3,ysd(-2),0],RED)
        self.play(GrowArrow(ar),run_time=0.45)
        self.finish()

class S14Scale(SpokenScene):
    def construct(self):
        self.add(T('rough sphere model',34,TEXT).move_to([0,3.35,0]))
        foot=T('Mean head 34.5 cm; SD about 1.2 cm',26,TEXT).move_to([0,-3.3,0]);self.add(foot)
        # Side-by-side projected spheres: radii computed from the volume ratio.
        r=1.17; v=((34.5-2*1.2)/34.5)**3
        mean=Circle(radius=r,color=GREY,fill_color=GREY,fill_opacity=0.15).move_to([-4.8,0.9,0])
        cut=Circle(radius=r*v**(1/3),color=RED,fill_color=RED,fill_opacity=0.3).move_to([-1.9,0.9,0])
        self.add(mean,T('mean',28,TEXT).move_to([-4.8,2.5,0]))
        self.at('a head at the cutoff')
        self.play(FadeIn(cut),FadeIn(T('−2 SD',28,RED).move_to([-1.9,2.5,0])),run_time=0.5)
        self.at('about a fifth')
        self.play(FadeIn(T('volume 0.80',30,RED).move_to([-1.9,-0.7,0])),FadeIn(T('1.00',30,TEXT).move_to([-4.8,-0.7,0])),run_time=0.4)
        self.add(T('about a fifth smaller',28,RED).move_to([-3.35,-1.5,0]))
        hdr=VGroup(T('SD from\nmean',26,TEXT).move_to([0.5,2.1,0]),T('volume',26,TEXT).move_to([2.5,2.1,0]),T('model volume\nhalvings',26,TEXT).move_to([5.0,2.1,0]))
        rows=VGroup()
        # Values derive from the rough sphere model; rounded to lesson precision.
        for sd,txt,halving,y in [(-2,'0.80','about ⅓',0.95),(-3,'0.72','about ½',-0.1),(-6,'0.50','one',-1.15)]:
            rows.add(VGroup(T('about −6' if sd==-6 else f'−{abs(sd)}',28,TEXT).move_to([0.5,y,0]),M(txt,30,RED if sd==-2 else TEXT).move_to([2.5,y,0]),T(halving,28,TEXT).move_to([5.0,y,0])))
        self.at('That compares volumes')
        self.play(FadeIn(hdr),FadeIn(rows),run_time=0.6)
        self.at('It does not count')
        note=VGroup(T('Model volume halvings:',28,TEXT),T('not counted divisions',30,TEXT)).arrange(RIGHT,buff=0.3).move_to([0,-2.5,0])
        self.play(FadeIn(note),run_time=0.5)
        self.at('lost divisions')
        self.play(Indicate(note[1],color=RED,scale_factor=1.03),run_time=0.4)
        self.finish()



class S15Aspm(SpokenScene):
    def construct(self):
        # An off-scale arrow expresses a qualitative tail, with no -6 tick/value.
        ax,labs,cap=bell_axis()
        self.add(ax,labs,cap,bell_curve(),T('ASPM families',38,ORANGE).move_to([-3.7,2.8,0]),T('no newborn scale and no round count',26,TEXT).move_to([0,3.45,0]))
        self.at('mutations')
        self.add(T('often many SD below',32,ORANGE).move_to([-3.7,1.9,0]),T('the mean for age',28,ORANGE).move_to([-3.7,1.3,0]))
        self.at('far smaller heads')
        off=arr([sdx(-3),-1.0,0],[-6.3,-1.0,0],ORANGE,6,0.3)
        self.play(GrowArrow(off),run_time=1)
        self.at('below the mean')
        self.play(Indicate(labs[2],color=TEXT,scale_factor=1.08),run_time=0.4)
        self.finish()



class S16Base(SpokenScene):
    def construct(self):
        axl, labs, cap = bell_axis()
        curve = bell_curve()
        self.add(axl, labs, cap, T("share of children",26,TEXT).rotate(PI/2).move_to([-3.05,0.4,0]), Line([-2.5,BASEY,0],[-2.5,2.85,0],color=GREY))
        title = T("ideal bell-shaped reference population", 28, TEXT).move_to([1.6, 3.4, 0])
        self.play(Create(curve), FadeIn(title), run_time=1.2)

        self.at("about two babies")
        cut = DashedLine([sdx(-2), BASEY, 0], [sdx(-2), BASEY + 2.35, 0], color=RED, stroke_width=3)
        pts = [[sdx(z), BASEY + BELLH * pdf(z) / 0.3989, 0] for z in np.linspace(-6.4, -2, 120)]
        tail = Polygon(*([[sdx(-6.4), BASEY, 0]] + pts + [[sdx(-2), BASEY, 0]]), stroke_width=0, fill_color=RED, fill_opacity=0.6)
        cl = T("−2 SD cutoff", 30, TEXT).move_to([sdx(-2)-0.7, BASEY+2.4, 0])
        self.add(cl)
        self.play(Create(cut), FadeIn(tail), run_time=0.9)

        sp, x0, y0 = 0.27, -6.4, 3.0
        grid = VGroup(*[Dot([x0 + (i % 10) * sp, y0 - (i // 10) * sp, 0], radius=0.09, color=RED if i < 2 else GREY) for i in range(100)])
        g_lab = T("2 in 100", 40, RED, weight=BOLD).move_to([x0 + 1.2, y0 - 3.1, 0])
        self.at("fall below the cutoff")
        self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in grid], lag_ratio=0.01), run_time=1.0)
        self.play(FadeIn(g_lab), Indicate(grid[:2], color=RED, scale_factor=1.6), run_time=0.7)

        self.at("small head")
        h = VGroup(T("some of them", 30, TEXT), T("are healthy", 30, TEXT)).arrange(DOWN, buff=0.08).move_to([x0 + 1.2, y0 - 4.0, 0])
        self.play(FadeIn(h), run_time=0.6)
        self.at("not a diagnosis")
        self.play(Indicate(g_lab, color=TEXT, scale_factor=1.12), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
def idea_card():
    hd=T('The one idea',30,TEXT).move_to([0,3.1,0])
    a=VGroup(T('Size counts',44,BLUE,weight=BOLD).move_to([-2.3,1.7,0]),T('the doublings.',44,BLUE,weight=BOLD).move_to([-2.3,0.85,0]),mini_tree(2.4,1.25).scale(2.0,about_point=[2.4,1.25,0]))
    b=VGroup(T('Layering records',44,YELLOW,weight=BOLD).move_to([-2.3,-1.1,0]),T('the journey.',44,YELLOW,weight=BOLD).move_to([-2.3,-1.95,0]),mini_climb(3.4,-1.5).scale(1.5,about_point=[3.4,-1.5,0]))
    return hd,a,b

class S17Idea1(SpokenScene):
    def construct(self):
        hd,a,b=idea_card();self.add(hd)
        self.at('size counts the doublings')
        self.play(FadeIn(a),run_time=0.45)
        self.at('layering records')
        self.play(FadeIn(b),run_time=0.45)
        self.finish()

class S18Idea2(SpokenScene):
    def construct(self):
        left,right,labels=brain_pair();self.add(left,right,labels)
        # Tags at identical, safely inset positions, beside the matching outlines.
        t1=chip('production',BLUE,30).move_to([-3.35,3.35,0])
        t2=chip('migration',YELLOW,30).move_to([3.35,3.35,0])
        self.at('Small with orderly layers')
        self.play(Indicate(left[0],color=BLUE,scale_factor=1.02),run_time=0.4)
        self.at('points to production')
        self.play(FadeIn(t1),run_time=0.35)
        self.at('Near normal size')
        self.play(Indicate(right[0],color=YELLOW,scale_factor=1.02),run_time=0.4)
        self.at('points to migration')
        self.play(FadeIn(t2),run_time=0.35)
        self.finish()
        self.wait(1.2)  # Hold both diagnoses as hypotheses long enough to compare.

class S19Scope(SpokenScene):
    def construct(self):
        hd,a,b=idea_card()
        pair=VGroup(a,b).scale(0.85).shift(UP*0.9)
        self.add(pair,T('a first question, not a diagnosis',38,TEXT,weight=BOLD).move_to([0,-2.0,0]),VGroup(T('Making and placing neurons only.',30,TEXT),T('Zika and folding come later.',30,TEXT)).arrange(DOWN,buff=0.18).move_to([0,-3.05,0]))
        self.finish()
        self.wait(1.5)



class S20Take(SpokenScene):
    def construct(self):
        cards = VGroup()
        for x, col in ((-3.3, BLUE), (3.3, YELLOW)):
            cards.add(RoundedRectangle(corner_radius=0.2, width=5.8, height=4.3, stroke_color=col, stroke_width=3,
                                       fill_color=col, fill_opacity=0.08).move_to([x, -0.35, 0]))
        left = VGroup(mini_tree(-4.1, 0.5).scale(1.35, about_point=[-4.1, 0.5, 0]), T("Too few made", 40, BLUE, weight=BOLD).move_to([-3.3, -1.3, 0]),
                      T("job 1: make the neurons", 26, GREY).move_to([-3.3, -2.0, 0]))
        right = VGroup(mini_climb(2.9, 0.4).scale(1.5, about_point=[2.9, 0.4, 0]), T("Made but misplaced", 34, YELLOW, weight=BOLD).move_to([3.3, -1.3, 0]),
                       T("job 2: move them", 26, GREY).move_to([3.3, -2.0, 0]))
        self.add(cards)
        self.at("malformed")
        self.play(FadeIn(left), FadeIn(right), run_time=0.8)
        self.at("ask first")
        q = T("Which job failed?", 50, TEXT, weight=BOLD).move_to([0, 3.2, 0])
        self.play(FadeIn(q, shift=DOWN * 0.15), run_time=0.7)
        self.finish()


class S21End(EndCard):
    LINE = "When a cortex is built wrong, ask first which job failed."
    def construct(self):
        line=VGroup(T('When a cortex is built wrong,',44,TEXT,font=TITLE_FONT),T('ask first which job failed.',48,TEXT,font=TITLE_FONT)).arrange(DOWN,buff=0.35)
        self.add(line,T('biochemistrypedia.com',28,TEAL).move_to([0,-1.8,0]))
        self.finish()
