"""Neuron doctrine, chapter 1: A Touch Is Not a Fusion  (Biochemistrypedia chaptered film)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole series; taken from scenes.old.py and shared by chapters 2 and 3)
  BLUE   = neuron one (the branch and cell that comes in from the top)
  YELLOW = neuron two (the branch and cell that comes in from the bottom)
  RED    = the limit of the light microscope (blur disk, depth band)
  ORANGE = the reticular reading: the branches are joined, ONE outer membrane runs around the net
  GREEN  = the neuron-theory reading and the verdict: separate cells, each with its own membrane
  TEAL   = what passes across the contact (signals) and the specialised contact itself (synapse)
  GOLD   = the unknown contact / the membrane that decides (the question), used sparingly
  GREY   = tissue, undecided outlines, de-emphasised things

Geometry shared by every scene: a cell is a soma plus a branched process that ends in a rounded tip.
Cell A (BLUE) comes from the top, cell B (YELLOW) is the same drawing turned half a turn and comes
from the bottom; their tips meet at the centre of a panel.  Membranes are drawn as the coloured
outline around each tube; the cytoplasm is the dim fill.  In the fused net the fills are joined
(no outline between them) and ONE orange outline runs round the whole net.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"


def dim(c, k=0.42):
    return interpolate_color(ManimColor(BG), ManimColor(c), k)


# ---------------------------------------------------------------------------------------------
# drawing helpers
# ---------------------------------------------------------------------------------------------
def path(pts, color, w, z=0):
    m = VMobject()
    m.set_points_smoothly([np.array([x, y, 0.0]) for x, y in pts])
    m.set_stroke(color, w, opacity=1)
    m.set_fill(opacity=0)
    m.set_cap_style(CapStyleType.ROUND)
    m.set_z_index(z)
    return m


def lab(text, size=28, color=TEXT, at=None, left=None, max_w=SAFE_W, font=FONT, weight=NORMAL, **kw):
    t = T(text, size=size, color=color, font=font, weight=weight, **kw)
    fit(t, max_w=max_w)
    if at is not None:
        t.move_to([at[0], at[1], 0])
    if left is not None:
        t.move_to([left[0] + t.width / 2, left[1], 0])
    return t


# All contact drawings are schematic; only the s08 scale ruler is quantitative.
LC, RC, PY, PS = -3.4, 3.4, -0.1, 1.0
FRAME_Y = -0.35

# One closed contour per separate cell; the two tips share only the origin.
TOP = [(-.18,.18),(-.52,.68),(-1.0,1.05),(-1.8,.85),(-2.35,1.15),
       (-1.65,1.12),(-1.25,1.38),(-1.35,1.9),(-1.6,2.15),
       (-1.48,2.58),(-1.05,2.78),(-.62,2.58),(-.55,2.16),
       (-.85,1.9),(-.85,1.5),(-.35,1.75),(.55,2.0),(1.3,1.8),
       (.5,1.76),(-.25,1.45),(-.55,1.12),(-.25,.78),(.18,.18)]

def cell(sign, s, cx, cy, ocol, fcol):
    pts = TOP + [(.13,.05),(0,0),(-.13,.05)]
    shape = Polygon(*[[cx+sign*x*s,cy+sign*y*s,0] for x,y in pts],
                    stroke_color=ocol, stroke_width=3.5, fill_color=fcol, fill_opacity=1)
    return VGroup(shape)


def left_panel(ocol=GREEN):
    return VGroup(cell(1,1,LC,PY,ocol,dim(BLUE)),cell(-1,1,LC,PY,ocol,dim(YELLOW)))


def right_panel(ocol=ORANGE, fused=True):
    if not fused:
        return VGroup(cell(1,1,RC,PY,ocol,dim(BLUE)),cell(-1,1,RC,PY,ocol,dim(YELLOW)))
    # The waist joins the contours; there is no internal stroke or colour boundary.
    pts = TOP + [(-x,-y) for x,y in TOP]
    return VGroup(Polygon(*[[RC+x,PY+y,0] for x,y in pts],stroke_color=ocol,
                          stroke_width=3.5,fill_color=dim(GREY),fill_opacity=1))


def pair(cx,cy,kind,hh=2.75,w=1.8,gap=.14,ocol=None,mo=.1):
    if kind == 'fused':
        # A continuous hourglass: outer membrane runs around the open waist.
        ys=np.linspace(-hh+.35,hh-.35,70)
        widths=w/2*(.52+.48*(1-np.exp(-(ys/1.0)**2)))
        pts=[(cx-a,cy+y,0) for y,a in zip(ys,widths)]
        pts += [(cx+widths[-1]*np.cos(t),cy+hh-.35+.35*np.sin(t),0) for t in np.linspace(np.pi,0,20)]
        pts += [(cx+a,cy+y,0) for y,a in zip(ys[::-1],widths[::-1])]
        pts += [(cx+widths[0]*np.cos(t),cy-hh+.35+.35*np.sin(t),0) for t in np.linspace(0,-np.pi,20)]
        membrane=Polygon(*pts,stroke_color=ocol or ORANGE,stroke_width=5,fill_color=dim(GREY),fill_opacity=1)
        return VGroup(membrane)
    tubes=VGroup()
    for sign,col in [(1,BLUE),(-1,YELLOW)]:
        h=hh-gap/2
        tube=RoundedRectangle(width=w,height=h,corner_radius=.18,
                stroke_color=ocol or GREEN,stroke_width=5,fill_color=dim(col),fill_opacity=1)
        tube.move_to([cx,cy+sign*(gap/2+h/2),0]); tubes.add(tube)
    return tubes


def title_l(): return lab('neuron theory',32,GREEN,at=(LC,3.15))
def title_r(): return lab('reticular theory',32,ORANGE,at=(RC,3.15))
def divider(): return Line([0,2.85,0],[0,-3.0,0],color=GREY,stroke_width=2,stroke_opacity=.4)


def blur(cx,cy,r=1.6,op=.14):
    return VGroup(*[Circle(radius=r*f,stroke_width=0,fill_color=RED,fill_opacity=op)
                   .move_to([cx,cy,0]) for f in (1,.85,.7,.55)])


def smudge(cx,cy):
    # Identical schematic point-spread images for the two unresolved hypotheses.
    return VGroup(*[Ellipse(width=1.4+f,height=3.5+f,stroke_width=0,
                           fill_color=RED,fill_opacity=.09).move_to([cx,cy,0]) for f in (1,.7,.4,.1)])


def predict_state():
    head=lab('What does the light microscope show?',34,at=(0,3.25))
    tl=lab('neuron theory',32,GREEN,at=(LC,2.35))
    tr=lab('reticular theory',32,ORANGE,at=(RC,2.35))
    boxes=[RoundedRectangle(width=5.9,height=4.9,corner_radius=.18,stroke_color=GREY,
                            stroke_width=2).move_to([x,-.35,0]) for x in (LC,RC)]
    qs=VGroup(*[lab('?',100,GREY,at=(x,-.35)) for x in (LC,RC)])
    return head,tl,tr,*boxes,qs


def predict_footer():
    return lab('1890s  •  pause and predict',30,GOLD,at=(0,-3.35))


def captions():
    return VGroup(lab('two facing membranes',28,GREEN,at=(LC,-3.35)),
                  lab('a fused junction',28,ORANGE,at=(RC,-3.35)))


def result_state():
    _,tl,tr,fl,fr,_=predict_state()
    return VGroup(lab('One contact cannot decide it',34,GOLD,at=(0,3.25)),
                  tl,tr,fl,fr,smudge(LC,FRAME_Y),smudge(RC,FRAME_Y),captions(),
                  lab('light microscope image • limit about 200 nm',24,at=(0,2.82)))


def icon_cell():
    g=cell(1,1,0,0,BLUE,dim(BLUE,.6))
    g.scale_to_fit_width(3.1).move_to([-4.1,0,0])
    return g


def icon_embryo():
    # Curled vertebrate embryo, with a large head and neural tube down its back.
    contour=VMobject(stroke_color=TEXT,stroke_width=4,fill_color=dim(GREY),fill_opacity=1)
    contour.start_new_path([.6,-1.6,0])
    contour.add_cubic_bezier_curve_to([-.9,-1.9,0],[-1.35,-.6,0],[-1.1,.8,0])
    contour.add_cubic_bezier_curve_to([-1.15,2.35,0],[1.1,2.25,0],[1.05,.95,0])
    contour.add_cubic_bezier_curve_to([1,.35,0],[.15,.4,0],[.2,-.15,0])
    contour.add_cubic_bezier_curve_to([.15,-.7,0],[1,-.8,0],[.6,-1.6,0])
    tube=path([(-.3,1.35),(-.7,.7),(-.65,-.1),(-.3,-.9),(.35,-1.35)],TEAL,9)
    eye=Dot([.5,1.25,0],radius=.08,color=BG)
    label=lab('neural tube',26,TEAL,at=(0,-2.5))
    lead=Line([0,-2.15,0],[-.3,-.95,0],color=TEAL,stroke_width=2)
    body=VGroup(contour,tube,eye).scale_to_fit_height(3.1).move_to([0,.15,0])
    lead=Line([0,-2.15,0],[-.25,-1.1,0],color=TEAL,stroke_width=2)
    return VGroup(body,label,lead)


def icon_chain():
    cs=VGroup(*[Circle(radius=.53,stroke_color=GREEN,stroke_width=4,fill_color=dim(c),fill_opacity=1)
                .move_to([4.3,y,0]) for y,c in [(1.6,BLUE),(0,YELLOW),(-1.6,BLUE)]])
    ars=VGroup(*[Arrow([4.3,y+.23,0],[4.3,y-.23,0],buff=0,color=TEAL,stroke_width=6,
                      tip_length=.18) for y in (.8,-.8)])
    return VGroup(cs,ars).scale_to_fit_height(3.1).move_to([4.1,0,0])


def evidence_state():
    return VGroup(lab('Evidence from elsewhere',36,at=(0,3.2)),icon_cell(),icon_embryo(),icon_chain(),
                  lab('whole cells',30,BLUE,at=(-4.1,-3.25)),lab('embryos',30,at=(0,-3.25)),
                  lab('direction of signal',28,TEAL,at=(4.1,-3.25)))


def takeaway():
    t=Text('A touch is not a fusion.',font=TITLE_FONT,font_size=84,
           t2c={'touch':GREEN,'fusion':ORANGE})
    fit(t,max_w=12.2); t.move_to([0,.55,0])
    return t


class S(SpokenScene):
    pass


class S00Title(TitleCard):
    LESSON='Seeing neurons: Golgi, Cajal and the neuron doctrine'
    TITLE='A Touch Is Not a Fusion'


class S01Q(S):
    def construct(self):
        a=cell(1,1.05,0,.4,GREY,dim(BLUE)); b=cell(-1,1.05,0,-.4,GREY,dim(YELLOW))
        l=lab('separate cells?',36,GREEN,at=(-4.35,0),max_w=3.5)
        r=lab('one continuous\nnetwork?',36,ORANGE,at=(4.35,0),max_w=3.5)
        self.add(a,b)
        self.at('separate cells')
        self.play(FadeIn(l),a.animate.shift(DOWN*.2),b.animate.shift(UP*.2),run_time=.65)
        self.at('one continuous')
        self.play(FadeIn(r),a.animate.shift(DOWN*.2),b.animate.shift(UP*.2),run_time=.65)
        self.finish()


class S02Neuron(S):
    def construct(self):
        pl,pr=left_panel(),right_panel(fused=False).set_opacity(.22)
        tl,tr=title_l(),title_r().set_opacity(.3)
        self.add(pl,pr,tl,tr,divider())
        self.at('neuron theory')
        self.play(Indicate(tl,scale_factor=1.07),run_time=.4)
        self.at('separate cell')
        self.play(Indicate(pl[0],scale_factor=1,color=BLUE),Indicate(pl[1],scale_factor=1,color=YELLOW),run_time=.5)
        self.at('own membrane')
        label=lab('each cell has its own membrane',28,GREEN,at=(LC,-3.35))
        self.play(FadeIn(label),run_time=.3)
        self.finish()


class S03Ret(S):
    def construct(self):
        pl,pr=left_panel(),right_panel(fused=False).set_opacity(.22)
        tl,tr=title_l(),title_r().set_opacity(.3)
        self.add(pl,pr,tl,tr,divider())
        self.at('reticular theory')
        self.play(tr.animate.set_opacity(1),pr.animate.set_opacity(1),run_time=.45)
        self.at('branches fuse')
        self.play(Transform(pr,right_panel()),run_time=.65)
        self.at('one continuous net')
        self.play(FadeIn(lab('open bridge • one outer membrane',27,ORANGE,at=(RC,-3.35))),run_time=.4)
        self.finish()


class S04Spot(S):
    def construct(self):
        pl,pr=left_panel(),right_panel()
        self.add(pl,pr,title_l(),title_r(),divider())
        self.at('where two branches')
        rings=VGroup(*[Circle(radius=.45,color=TEAL,stroke_width=5).move_to([x,PY,0]) for x in (LC,RC)])
        self.play(Create(rings),run_time=.35)
        self.at('branches meet')
        c1=lab('open cytoplasmic bridge',28,ORANGE,at=(RC,-3.35))
        c2=lab('two membranes • gap enlarged',27,GREEN,at=(LC,-3.35))
        self.play(ReplacementTransform(pl,pair(LC,PY,'sep')),ReplacementTransform(pr,pair(RC,PY,'fused')),
                  FadeOut(rings),FadeIn(c1),FadeIn(c2),run_time=.65)
        self.at('one membrane run on')
        self.play(Indicate(c1,scale_factor=1.04),run_time=.4)
        self.at('two face each other')
        self.play(Indicate(c2,scale_factor=1.04),run_time=.4)
        self.finish()


class S05Idea(S):
    def construct(self):
        self.add(lab('THE ONE IDEA',32,GOLD,at=(0,2.05)),takeaway())
        self.at('touch is not')
        self.play(Indicate(self.mobjects[1],scale_factor=1.03),run_time=.5)
        self.finish()


class S06Idea2(S):
    def construct(self):
        tubes=pair(-3.25,.05,'sep',hh=3,w=3.1,gap=.18,ocol=GREY)
        title=lab('one cell or two?',40,at=(2.8,2.5))
        self.add(tubes,title,lab('contact enlarged',26,GREY,at=(-3.25,-3.3)))
        self.at('depends on the membrane')
        mem=VGroup(*[Line([-4.62,y,0],[-1.88,y,0],color=GOLD,stroke_width=8) for y in (-.04,.14)])
        leader=Line([-1.65,.05,0],[.15,.85,0],color=GOLD,stroke_width=3)
        text=lab('decided at the membrane',32,GOLD,at=(3.1,.85))
        self.play(Create(mem),Create(leader),FadeIn(text),run_time=.55)
        self.at('on that membrane')
        self.play(Indicate(mem,scale_factor=1,color=WHITE),run_time=.4)
        self.at('seeing it')
        lens=Circle(radius=.34,color=TEXT,stroke_width=4).move_to([.8,-.65,0])
        handle=Line([1.04,-.9,0],[1.3,-1.16,0],color=TEXT,stroke_width=5)
        imaging=lab('imaging the membrane',32,at=(3.65,-.75))
        self.play(Create(lens),Create(handle),FadeIn(imaging),run_time=.4)
        self.at('testing what crosses')
        arrow=Arrow([-3.25,.95,0],[-3.25,-.85,0],color=TEAL,buff=0,stroke_width=6)
        testing=lab('testing what crosses it',32,TEAL,at=(3.6,-2.1))
        self.play(GrowArrow(arrow),FadeIn(testing),run_time=.45)
        self.finish()


class S07Light(S):
    def construct(self):
        tubes=pair(-2.8,.05,'sep',hh=3,w=2.4,gap=.14,ocol=GREY)
        self.add(tubes,lab('light microscope limit',36,RED,at=(2.8,1.9)),
                 lab('contact enlarged',26,GREY,at=(-2.8,-3.3)))
        self.at('closer than')
        disk=DashedVMobject(Circle(radius=1.7,color=RED,stroke_width=4).move_to([-2.8,.05,0]),num_dashes=32)
        ar=DoubleArrow([-.7,-1.65,0],[-.7,1.75,0],buff=0,color=RED,tip_length=.2)
        self.play(Create(disk),GrowFromCenter(ar),FadeIn(lab('about 200 nm',40,RED,at=(2.8,.2))),run_time=.6)
        self.at('blur into one')
        self.play(FadeIn(blur(-2.8,.05)),run_time=.6)
        self.finish()


class S08Cleft(S):
    def construct(self):
        # Same enlarged scale: 4.6 units / 200 nm = .46 / 20 nm.
        self.add(pair(-3.7,0,'sep',hh=2.8,w=2.1,gap=.46),
                 lab('chemical synapse',32,GREEN,at=(-3.7,3.25)),
                 lab('enlarged • drawn to scale',26,GREY,at=(-3.7,-3.3)))
        ruler=DoubleArrow([6.1,-2.3,0],[6.1,2.3,0],buff=0,color=RED,tip_length=.18,stroke_width=4)
        ticks=VGroup(*[Line([5.9,-2.3+.46*i,0],[6.3,-2.3+.46*i,0],color=RED,stroke_width=2) for i in range(11)])
        disk=DashedVMobject(Circle(radius=2.3,color=RED,stroke_width=3).move_to([-3.7,0,0]),num_dashes=32)
        self.add(disk,ruler,ticks,lab('blur: about 200 nm',36,RED,at=(2.8,1.7)))
        self.at('is about')
        cleft=lab('cleft: about 20 nm',36,GREEN,at=(2.8,-.15))
        lead=Line([-2.6,0,0],[.45,-.15,0],color=GREEN,stroke_width=3)
        bracket=DoubleArrow([-2.4,-.23,0],[-2.4,.23,0],buff=0,color=GREEN,tip_length=.07,stroke_width=3)
        self.play(FadeIn(cleft),Create(lead),GrowFromCenter(bracket),run_time=.45)
        self.at('that is about')
        comparison=lab('about ten times narrower',32,at=(2.8,-1.5))
        self.play(FadeIn(comparison),FadeIn(lab('measured only in the 1950s\nelectron microscopy • 1955–56',27,GREY,at=(2.7,-2.85))),run_time=.55)
        self.finish()


class S09Depth(S):
    def construct(self):
        left=RoundedRectangle(width=5.65,height=5.8,corner_radius=.15,color=GREY,stroke_width=3).move_to([LC,-.05,0])
        right=left.copy().move_to([RC,-.05,0])
        ca=Circle(radius=.63,color=BLUE,stroke_width=6,fill_color=dim(BLUE),fill_opacity=1).move_to([LC,.65,0])
        cb=Circle(radius=.63,color=YELLOW,stroke_width=6,fill_color=dim(YELLOW),fill_opacity=1).move_to([LC,-.65,0])
        labels=VGroup(lab('thick section • side view',28,at=(LC,3.2)),lab('what you see',30,at=(RC,3.2)),
                      lab('section: 100 µm or more',27,at=(LC,-3.3)),lab('enlarged, not to scale',26,GREY,at=(RC,-3.3)))
        limit=VGroup(lab('depth limit',30,RED,at=(LC,-1.8)),lab('roughly 0.5 to 1 µm',28,RED,at=(LC,-2.25)))
        optics=lab('depending on the optics',26,RED,at=(LC,-2.65))
        band=Rectangle(width=5.55,height=1.45,color=RED,stroke_width=3,fill_color=RED,fill_opacity=.15).move_to([LC,1.8,0])
        la=Line([1.2,.55,0],[5.6,.55,0],color=BLUE,stroke_width=12)
        lb=Line([1.2,-.55,0],[5.6,-.55,0],color=YELLOW,stroke_width=12)
        self.add(left,right,ca,cb,labels,la,lb,limit,optics)
        self.at('two branches')
        self.play(ca.animate.set_fill(opacity=.9),cb.animate.set_fill(opacity=.9),run_time=.3)
        self.at('one above')
        self.add(band)
        self.play(band.animate.move_to([LC,.8,0]),run_time=.65)
        self.at('can look like')
        merged=VGroup(*[Line([1.2,0,0],[5.6,0,0],stroke_color=interpolate_color(ManimColor(BLUE),ManimColor(YELLOW),.5),
                            stroke_width=w,stroke_opacity=op) for w,op in [(40,.08),(30,.14),(20,.4),(12,.9)]])
        self.play(band.animate.move_to([LC,-.7,0]),ReplacementTransform(VGroup(la,lb),merged),
                  ca.animate.set_fill(opacity=.25),cb.animate.set_fill(opacity=.25),run_time=.75)
        self.play(FadeIn(lab('looks like one line',30,at=(RC,-1.6))),run_time=.25)
        self.finish()


class S10Predict(S):
    def construct(self):
        head,tl,tr,fl,fr,qs=predict_state()
        footer=predict_footer()
        self.add(head,tl,tr,fl,fr,qs,footer)
        self.at('under the best')
        self.play(Indicate(head,scale_factor=1.02,color=RED),run_time=.4)
        self.at('what does each')
        self.play(Indicate(footer,scale_factor=1.04),run_time=.5)
        self.finish()


class S11Pause(S):
    def construct(self):
        self.add(*predict_state(),lab('pause',30,GOLD,at=(-1.6,-3.3)),
                 lab('and predict',30,GOLD,at=(1.9,-3.3)))
        # A visible progress arc supplies the thinking cue without replacing the question.
        ring=Circle(radius=.4,color=GREY,stroke_width=4,stroke_opacity=.35).move_to([0,-3.3,0])
        self.add(ring)
        arc=Arc(radius=.4,start_angle=PI/2,angle=-TAU,color=GOLD,stroke_width=7).move_to(ring)
        self.play(Create(arc),run_time=5,rate_func=linear)
        self.finish()


class S12Reveal(S):
    def construct(self):
        head,tl,tr,fl,fr,qs=predict_state()
        footer=predict_footer()
        self.add(head,tl,tr,fl,fr,qs,footer)
        self.at('same thing')
        sl,sr=smudge(LC,FRAME_Y),smudge(RC,FRAME_Y)
        self.play(FadeOut(qs),FadeOut(footer),FadeIn(sl),FadeIn(sr),run_time=.5)
        cs=captions()
        self.at('two facing membranes')
        self.play(FadeIn(cs[0]),run_time=.35)
        self.at('a fused junction')
        self.play(FadeIn(cs[1]),run_time=.35)
        self.at('same smudge')
        self.play(Transform(head,lab('One contact cannot decide it',34,GOLD,at=(0,3.25))),
                  Indicate(sl,scale_factor=1.03),Indicate(sr,scale_factor=1.03),
                  FadeIn(lab('light microscope image • limit about 200 nm',24,at=(0,2.82))),run_time=.5)
        self.finish()


class S13Beat(S):
    def construct(self):
        self.add(result_state()); self.wait(3); self.finish()


class S14Elsewhere(S):
    def construct(self):
        state=evidence_state()
        self.add(state[0],*state[1:4].copy().set_opacity(.2))
        # The first icon is visible from the first spoken word; others are introduced in turn.
        self.add(state[1],state[4])
        self.at('whole cells')
        self.play(Indicate(state[1],scale_factor=1.04),run_time=.4)
        self.at('embryos')
        self.play(FadeIn(state[2]),FadeIn(state[5]),run_time=.45)
        self.at('the direction')
        self.play(FadeIn(state[3][0]),FadeIn(state[6]),run_time=.25)
        self.play(LaggedStart(*[GrowArrow(a) for a in state[3][1]],lag_ratio=.3),run_time=.6)
        self.finish()


class S15Answer(S):
    def construct(self):
        pl,pr=left_panel(),right_panel()
        tl,tr=title_l(),title_r()
        tl.shift(DOWN*.6);tr.shift(DOWN*.6)
        pl.scale(.83).shift(DOWN*.1);pr.scale(.83).shift(DOWN*.1)
        self.add(pl,pr,tl,tr,lab('Vertebrate nervous system',38,at=(0,3.3)))
        self.at('separate cells')
        note=lab('Electrical synapses: gap junctions\njoin some neurons while each\nremains a separate cell.',28,at=(3,-1.7),max_w=6.2)
        self.play(FadeOut(pr),tr.animate.set_opacity(.25),FadeIn(note),run_time=.5)
        self.at('pass signals')
        dot=Dot([LC-.6,.6,0],radius=.1,color=TEAL)
        self.add(dot)
        self.play(dot.animate.move_to([LC+.6,-.6,0]),run_time=.7)
        self.remove(dot)
        self.at('specialized contacts')
        ring=Circle(radius=.33,color=TEAL,stroke_width=5).move_to([LC,-.2,0])
        self.play(Create(ring),run_time=.35)
        self.at('called synapses')
        label=lab('synapse',36,TEAL,at=(-.7,-.4))
        leader=Line([-1.65,-.4,0],[LC+.38,-.2,0],color=TEAL,stroke_width=3)
        self.play(FadeIn(label),Create(leader),run_time=.4)
        self.finish()


class S16Why(S):
    def construct(self):
        head=lab('Development in vertebrates',38,at=(0,3.25))
        ys=[1.9,-.1,-2.1]
        sources=VGroup(*[Circle(radius=.65,color=GREEN,stroke_width=5,fill_color=dim(BLUE),fill_opacity=1).move_to([-5.35,y,0]) for y in ys])
        targets=VGroup(*[Circle(radius=.65,color=GREEN,stroke_width=5,fill_color=dim(YELLOW),fill_opacity=1).move_to([5.35,y,0]) for y in ys])
        self.add(head,sources,targets)
        # Distinct routes grow from the opening word, then reach different partner heights.
        routes=[ [(-4.7,1.9),(-3,2.5),(0,2.55),(2.4,2.35),(4.42,2.12)],
                 [(-4.7,-.1),(-3,-.8),(-.5,-.65),(2,.15),(4.42,.12)],
                 [(-4.7,-2.1),(-3,-1.3),(-.5,-1.45),(2.4,-2.5),(4.42,-2.28)] ]
        full=VGroup(*[path(pts,BLUE,10) for pts in routes])
        branches=VGroup(*[f.copy().pointwise_become_partial(f,0,.46) for f in full])
        self.play(*[Create(f) for f in branches],run_time=1.8)
        self.at('wire separate')
        self.play(*[Transform(b,f) for b,f in zip(branches,full)],run_time=1.0)
        self.at('right partners')
        rings=VGroup(*[Circle(radius=.12,color=TEAL,stroke_width=5).move_to([4.42,y,0]) for y in (2.12,.12,-2.28)])
        tag=lab('the right partners',30,TEAL,at=(0,-3.35))
        self.play(Create(rings),FadeIn(tag),run_time=.4)
        self.finish()


class S17Take(S):
    def construct(self):
        t=takeaway(); self.add(t)
        self.at('the difference')
        self.play(FadeIn(lab('The difference lies at the membrane.',38,at=(0,-.7),font=TITLE_FONT)),run_time=.45)
        self.finish()


class S18End(EndCard):
    LINE='A touch is not a fusion. The difference lies at the membrane.'

    def construct(self):
        # Carry the closing card across the cut, then settle into the unchanged end-card text.
        first=takeaway()
        second=lab('The difference lies at the membrane.',38,at=(0,-.7),font=TITLE_FONT)
        self.add(first,second)
        line=lab(self.LINE,40,font=TITLE_FONT,max_w=11.5)
        sub=lab('biochemistrypedia.com',22,TEAL)
        VGroup(line,sub).arrange(DOWN,buff=.4)
        self.wait(.5)
        self.remove(first,second)
        self.add(line)
        self.play(FadeIn(sub),run_time=.4)
        self.finish()
