"""Microglia and Complement Prune Synapses, chapter 2: A Tag and a Reader (Biochemistrypedia explainer)

COLOR MAP (one color per concept, shared by every chapter of this lesson)
  BLUE   = inputs from eye A (retinal terminals)
  ORANGE = inputs from eye B
  YELLOW = the complement tag (C1q, C3, C3b, iC3b) and its enzymes
  PURPLE = microglia / the eating cell
  TEAL   = complement receptor 3 on the eating cell (the reader)
  RED    = silenced eye, removal, knockout mice
  GREEN  = boosted (more active) eye
  PINK   = astrocytes (chapter 2 only)
  GOLD   = headers and cautions
  GREY   = outlines, neurons, targets, unknowns
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
PINK = "#E58FB8"
EYE_A, EYE_B = BLUE, ORANGE

SURF_Y = -1.1          # top edge of the target
C1X = -3.5             # centre of the C1q bunch
ENZ = (1.7, 1.2)       # where the C3-cutting enzyme sits
C3B = (1.7, -0.65)     # where C3b is stapled


# ------------------------------------------------------------------------------------------ helpers
def P(x, y):
    return np.array([x, y, 0.0])


def _unit(deg):
    return P(np.cos(np.radians(deg)), np.sin(np.radians(deg)))


def rcap(line):
    line.set_cap_style(CapStyleType.ROUND)
    return line


def bulb(c, color=BLUE, r=0.45, op=0.45):
    return Circle(radius=r, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=op).move_to(c)


def arr(a, b, color=GREY, w=5):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=0.22,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def process(a, b, w=18, op=0.55):
    return rcap(Line(a, b, color=PURPLE, stroke_width=w, stroke_opacity=op))


def branch(c, ang, ln, sx, w=13, op=0.55, bend=7):
    # Filled, tapered silhouettes start inside the soma; twigs share a junction.
    root = c + _unit(ang) * .62 * sx
    joint = c + _unit(ang + bend) * .62 * ln
    tip = c + _unit(ang + bend * 1.6) * ln
    side = _unit(ang + 90)
    trunk = Polygon(root + side * .09 * sx, joint + side * .055 * sx,
                    tip, joint - side * .055 * sx, root - side * .09 * sx,
                    stroke_width=0, fill_color=PURPLE, fill_opacity=op)
    twig_tip = joint + _unit(ang + 50) * .55 * sx
    twig = Polygon(joint + side * .08 * sx, twig_tip, joint - side * .08 * sx,
                   stroke_width=0, fill_color=PURPLE, fill_opacity=op)
    return VGroup(trunk, twig)


def microglia(c, sx=1.0, procs=((160, 1.5), (200, 1.5), (110, 1.3), (70, 1.3), (250, 1.3))):
    body = Ellipse(width=1.7 * sx, height=1.5 * sx, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE,
                   fill_opacity=0.3).move_to(c)
    return VGroup(*[branch(c, a, ln * sx, sx) for a, ln in procs], body)


def lines(text, size=26, color=TEXT, font=FONT, **kw):
    """centred multi-line text (Text left-aligns its lines)."""
    return VGroup(*[T(t, size, color, font=font, **kw) for t in text.split("\n")]).arrange(DOWN, buff=0.12)


def target():
    cap = RoundedRectangle(corner_radius=0.9, width=12, height=1.8, stroke_color=GREY, stroke_width=4,
                           fill_color=GREY, fill_opacity=0.25).move_to(P(0, -2.0))
    return cap


def target_label():
    return T("target", 26, GREY).move_to(P(0, -2.0))


# the three-step strip
STEP_TEXT = ["1  binds", "2  cut and stick", "3  read"]


def step_chip(i, lit):
    col = YELLOW if lit else GREY
    box = RoundedRectangle(corner_radius=0.14, width=3.8, height=0.72, stroke_color=col, stroke_width=3,
                           fill_color=col, fill_opacity=0.28 if lit else 0.05)
    lab = T(STEP_TEXT[i], 26, col if lit else GREY, weight=BOLD if lit else NORMAL).move_to(box)
    return VGroup(box, lab).move_to(P(-4.2 + 4.2 * i, 3.2))


def make_strip(lit=()):
    return [step_chip(i, i in lit) for i in range(3)]


# C1q: six tulip heads on stalks that meet in one stem
HEAD_DX = (-2.2, -1.32, -0.44, 0.44, 1.32, 2.2)
HEAD_R = 0.3


def c1q(cx=C1X, lift=0.0, label=True, xs=1.0):
    top, junc, hy = 2.0 + lift, 1.3 + lift, -0.8 + lift
    stem = rcap(Line(P(cx, top), P(cx, junc), color=YELLOW, stroke_width=9))
    stalks = VGroup()
    for dx in HEAD_DX:
        path = VMobject().set_points_smoothly([P(cx, junc), P(cx + dx * xs * .65, junc-.45),
                                               P(cx + dx * xs, hy+1.0), P(cx + dx * xs, hy+HEAD_R)])
        path.set_stroke(YELLOW, 6)
        stalks.add(path)
    heads = VGroup(*[Circle(radius=HEAD_R, stroke_color=YELLOW, stroke_width=4, fill_color=YELLOW, fill_opacity=0.75)
                     .move_to(P(cx + dx * xs, hy)) for dx in HEAD_DX])
    parts = [stem, stalks, heads]
    if label:
        parts.append(T("C1q", 32, YELLOW, weight=BOLD).move_to(P(cx + 1.0, top - 0.15)))
    g = VGroup(*parts)
    g.heads = heads
    return g


def tag_dots_line(y, x0, x1, n):
    return VGroup(*[Dot(radius=0.11, color=YELLOW).move_to(P(x0 + (x1 - x0) * k / (n - 1), y)) for k in range(n)])


def synapse(c, s=1.0, tags=False):
    """a retinal terminal (blue) against a relay neuron (grey)."""
    b = bulb(c + P(-1.05 * s, 0), EYE_A, 0.75 * s, 0.45)
    r = Circle(radius=1.45 * s, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.2)
    r.move_to(c + P(0.55 * s, 0))
    g = VGroup(b, r)
    g.bulb, g.relay = b, r
    return g


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Microglia and Complement Prune Synapses"
    TITLE = "A Tag and a Reader"


class S01Q(SpokenScene):
    def construct(self):
        bc = P(-3.6,-.3)
        bac = RoundedRectangle(width=5.2,height=3.5,corner_radius=1.3,color=GREY,fill_opacity=.2,fill_color=GREY).move_to(bc)
        sy = synapse(P(3.8,-.3),1.35)
        self.add(bac,sy,T("bacterium",30,GREY).move_to(P(-3.6,-2.8)),T("synapse",30,GREY).move_to(P(3.7,-2.8)),
                 T("?",70,GREY).move_to(P(-3.6,2.3)),T("?",70,GREY).move_to(P(3.8,2.5)))
        self.at("immune protein")
        ip=chip("immune protein",YELLOW,30).move_to(P(0,3.1))
        dot=Dot(P(-1.2,2.1),radius=.2,color=YELLOW)
        leader=Line(ip.get_bottom(),dot.get_top(),color=YELLOW)
        self.play(FadeIn(ip),FadeIn(dot),Create(leader),run_time=.45)
        self.at("mark something")
        tags=VGroup(*[Dot(bc+P(2.8*np.cos(a),1.95*np.sin(a)),radius=.15,color=YELLOW) for a in np.linspace(0,2*PI,14,endpoint=False)])
        self.play(Transform(dot,tags),Transform(leader,Line(ip.get_bottom(),bc+P(1.75,1.52),color=YELLOW)),run_time=.65)
        self.at("young brain")
        self.play(Indicate(sy,color=YELLOW,scale_factor=1.05),run_time=.7)
        self.finish()


class S02Blood(SpokenScene):
    def construct(self):
        strip=make_strip()
        tg=RoundedRectangle(width=7.4,height=4.1,corner_radius=.9,color=GREY,fill_color=GREY,fill_opacity=.25).move_to(P(-2.3,-.5))
        tl=T("target",30,GREY).move_to(P(-2.3,-.7))
        heading=T("in the blood",34,GREY).move_to(P(-2.3,2.2))
        eater=bulb(P(4.5,.1),PURPLE,1.5,.3)
        self.add(tg,tl,*strip,heading,eater)
        self.at("complement marks")
        self.play(Transform(heading,T("complement",34,YELLOW).move_to(P(-2.3,2.2))),run_time=.5)
        self.at("eating cells")
        el=T("eating cell",30,PURPLE).move_to(P(4.5,2.2))
        self.play(FadeIn(el),run_time=.5)
        self.at("three steps")
        self.play(Transform(tg,target()),Transform(tl,target_label()),FadeOut(eater),FadeOut(el),FadeOut(heading),run_time=.7)
        self.finish()


class S03Step1(SpokenScene):
    def construct(self):
        strip=make_strip(); cq=c1q(0,lift=.5,xs=1.4)
        self.add(target(),target_label(),*strip,cq)
        self.at("binds")
        self.play(cq.animate.shift(DOWN*.5),Transform(strip[0],step_chip(0,True)),run_time=.65)
        self.at("six tulips")
        lab=T("six heads",32,YELLOW).move_to(P(4.8,.5))
        self.play(FadeIn(lab),Create(Line(lab.get_bottom(),P(3.1,-.5),color=YELLOW)),run_time=.5)
        self.at("each head")
        self.play(LaggedStart(*[Indicate(h,color=TEXT,scale_factor=1.3) for h in cq.heads],lag_ratio=.12),run_time=1)
        self.finish()


def enzyme_unit():
    # The retained C4 and C2 pieces remain visible as the assembled enzyme.
    return VGroup(chip("C4 piece",YELLOW,26),chip("C2 piece",YELLOW,26)).arrange(RIGHT,buff=.04).move_to(P(*ENZ))


def cascade_base():
    return VGroup(target(),target_label(),*make_strip((0,1)),c1q(xs=.85),enzyme_unit(),
                  T("C3-cutting enzyme",28,YELLOW).move_to(P(1.7,2.15)))


def split_block(label, center, width=2.2, height=.8):
    """One labelled cartoon with a removable end, initially flush with its body."""
    body = Rectangle(width=width*.75, height=height, color=YELLOW,
                     fill_color=YELLOW, fill_opacity=.2).move_to(center+P(-width*.125,0))
    end = Rectangle(width=width*.25, height=height, color=YELLOW,
                    fill_color=YELLOW, fill_opacity=.5).move_to(center+P(width*.375,0))
    lab = T(label,32,YELLOW).move_to(body)
    return VGroup(body,lab), end


class S04Step2(SpokenScene):
    def construct(self):
        strip=make_strip((0,)); cq=c1q(0,xs=1.4)
        self.add(target(),target_label(),*strip,cq)
        self.play(Transform(cq,c1q(xs=.85)),run_time=.7)
        self.at("enzymes")
        ez=T("enzymes",28,YELLOW).move_to(P(-5.2,2.2))
        leader=Line(ez.get_right(),P(-3.5,1.7),color=YELLOW)
        stalk_enz=RoundedRectangle(width=.5,height=.55,corner_radius=.08,color=YELLOW,
                                  fill_color=YELLOW,fill_opacity=.6).move_to(P(-3.5,1.65))
        c4,e4=split_block("C4",P(.1,1.15)); c2,e2=split_block("C2",P(4.1,1.15))
        self.play(FadeIn(ez),Create(leader),FadeIn(stalk_enz),FadeIn(c4),FadeIn(e4),FadeIn(c2),FadeIn(e2),run_time=.5)
        self.at("cut two")
        cuts=VGroup(*[Line(e.get_left()+UP*.55,e.get_left()+DOWN*.55,color=TEXT,stroke_width=6) for e in (e4,e2)])
        self.play(Create(cuts),run_time=.25)
        self.play(e4.animate.shift(P(.5,.9)),e2.animate.shift(P(.5,.9)),FadeOut(cuts),run_time=.75)
        self.at("their pieces")
        # A physical docking rail joins the assembled pieces beside the C1q stalk.
        rail=Line(P(-3.25,1.65),P(-.45,1.2),color=YELLOW,stroke_width=7)
        unit=enzyme_unit()
        self.play(Transform(c4,unit[0]),Transform(c2,unit[1]),Create(rail),
                  FadeOut(e4),FadeOut(e2),run_time=.65)
        self.at("build an enzyme")
        self.play(FadeIn(T("C3-cutting enzyme",28,YELLOW).move_to(P(1.7,2.15))),
                  Transform(strip[1],step_chip(1,True)),run_time=.4)
        self.at("cuts C3")
        c3,end=split_block("C3",P(1.7,-.05))
        self.play(FadeIn(c3),FadeIn(end),GrowArrow(arr(P(1.7,.75),P(1.7,.4),YELLOW)),run_time=.4)
        self.finish()


class S05Stick(SpokenScene):
    def construct(self):
        big,small=split_block("C3",P(1.7,-.05))
        self.add(cascade_base(),big,small)
        self.at("splits in two")
        seam=small.get_left()
        cut=Line(seam+UP*.55,seam+DOWN*.55,color=TEXT,stroke_width=6)
        self.play(Create(cut),run_time=.2)
        # Separate the actual pieces of the original block, then name the small one.
        self.play(big.animate.shift(LEFT*.25),small.animate.shift(RIGHT*.6),FadeOut(cut),run_time=.4)
        sa=T("C3a",28,YELLOW).next_to(small,UP,buff=.15)
        self.play(FadeIn(sa),run_time=.2)
        self.play(VGroup(small,sa).animate.move_to(P(5,1.3)),run_time=.65)
        self.at("large piece")
        self.play(Indicate(big[0],color=YELLOW,scale_factor=1.04),run_time=.35)
        self.at("C3B")
        self.play(Transform(big[1],T("C3b",32,YELLOW).move_to(big[0])),run_time=.3)
        self.at("fix itself")
        self.play(big.animate.move_to(P(*C3B)),run_time=.7)
        self.at("nearby surface")
        staples=VGroup(*[VMobject().set_points_as_corners([P(C3B[0]+dx,-.8),P(C3B[0]+dx,-1.4),
                           P(C3B[0]+dx+.2,-1.4)]).set_stroke(YELLOW,7) for dx in (-.55,.55)])
        self.play(Create(staples),run_time=.4)
        self.finish()


class S06Step3(SpokenScene):
    def construct(self):
        strip=make_strip((0,1))
        self.add(target(),target_label(),*strip,c1q(xs=.85))
        tag,clip=split_block("C3b",P(*C3B),width=2.2)
        self.add(tag,clip)
        self.at("is trimmed")
        seam=clip.get_left()
        cut=Line(seam+UP*.5,seam+DOWN*.5,color=TEXT,stroke_width=6)
        self.play(Create(cut),run_time=.15)
        self.play(clip.animate.shift(P(.7,1.3)),FadeOut(cut),run_time=.45)
        self.at("IC3B")
        self.play(Transform(tag[1],T("iC3b",32,YELLOW).move_to(tag[0])),run_time=.35)
        self.at("receptor 3",lead=.5)
        body=bulb(P(4.65,.6),PURPLE,1.85,.3)
        proc=process(P(3.6,.6),P(3.05,.15),32)
        receptor=VGroup(Line(P(3.05,.15),P(3.05,-.3),color=TEAL,stroke_width=10),
                        Arc(radius=.5,start_angle=0,angle=-PI,arc_center=P(2.55,-.3),color=TEAL,stroke_width=10))
        rl=lines("CR3\ncomplement receptor 3",26,TEAL).move_to(P(4.6,-3.4))
        crlead=Line(rl.get_top(),P(3.05,-.5),color=TEAL)
        self.play(FadeIn(body),Create(proc),Create(receptor),FadeIn(rl),Create(crlead),FadeOut(clip),run_time=.6)
        self.at("eating cell")
        self.play(FadeIn(T("eating cell",30,PURPLE).move_to(P(4.65,1.85))),run_time=.3)
        self.at("binds it")
        self.play(receptor.animate.shift(P(-.85,0)),proc.animate.put_start_and_end_on(P(3.6,.6),P(2.2,.15)),
                  Transform(crlead,Line(rl.get_top(),P(2.2,-.5),color=TEAL)),Transform(strip[2],step_chip(2,True)),run_time=.45)
        self.at("promotes engulfment")
        wrap=Arc(radius=1.1,start_angle=-PI/2,angle=1.4*PI,arc_center=P(1.7,-.75),color=PURPLE,stroke_width=12)
        self.play(Create(wrap),FadeIn(T("promotes engulfment",30,PURPLE).move_to(P(-1,-3.3))),run_time=.65)
        self.finish()


def neuron(c,r=1):
    return VGroup(bulb(c,GREY,r,.2),*[Line(c+_unit(a)*r,c+_unit(a)*(r+.4),color=GREY,stroke_width=5) for a in (210,330)])


def astro(c):
    return VGroup(*[Line(c,c+_unit(a)*.8,color=PINK,stroke_width=8) for a in range(0,360,60)],bulb(c,PINK,.4,.4))


class S07Stevens(SpokenScene):
    def construct(self):
        dish=RoundedRectangle(width=12,height=5.6,corner_radius=.6,color=GREY,fill_color=GREY,fill_opacity=.06).move_to(P(0,-.3))
        ns=VGroup(*[neuron(P(x,.7),.9) for x in (-3.8,0,3.8)])
        self.add(dish,ns,T("Credit: Stevens, Barres laboratory, Stanford",28,TEXT).move_to(P(0,3.3)),
                 T("retinal ganglion cells",30,GREY).move_to(P(0,2.15)))
        self.at("astrocytes")
        aa=VGroup(*[astro(P(x,-1.55)) for x in (-2.5,2.5)])
        self.play(FadeIn(aa),FadeIn(T("astrocytes",30,PINK).move_to(P(0,-2.7))),run_time=.65)
        self.at("in a dish")
        self.play(Indicate(dish,color=TEXT,scale_factor=1.01),run_time=.5)
        self.at("raised their")
        tags=VGroup(*[lines("more\nC1q mRNA",26,YELLOW).move_to(P(x,.7)) for x in (-3.8,0,3.8)])
        self.play(FadeIn(tags),*[n[0].animate.set_stroke(YELLOW,5) for n in ns],run_time=.65)
        self.finish()


class S08Synapses(SpokenScene):
    def construct(self):
        self.add(T("young mouse visual thalamus · dLGN",32,GREY).move_to(P(0,3.3)))
        relay=neuron(P(0,-.15),1.6)
        b=bulb(P(-2.6,.6),EYE_A,.9); o=bulb(P(2.6,.6),EYE_B,.9)
        self.add(relay,b,o,lines("left-eye retinal\ninput",28,EYE_A).move_to(P(-4.7,1.9)),
                 lines("right-eye retinal\ninput",28,EYE_B).move_to(P(4.7,1.9)),T("relay neuron",30,GREY).move_to(P(0,-2.4)))
        c1=VGroup(*[Dot(P(x,.85),radius=.30,color=YELLOW) for x in (-1.7,1.7)])
        c3=VGroup(*[Circle(radius=.34,color=YELLOW,stroke_width=7).move_to(P(x,-.05)) for x in (-1.7,1.7)])
        lab1=VGroup(Dot(radius=.30,color=YELLOW),T("C1q",30,YELLOW)).arrange(RIGHT,buff=.2).move_to(P(-3,-3.1))
        lab3=VGroup(Circle(radius=.34,color=YELLOW,stroke_width=7),T("C3",30,YELLOW)).arrange(RIGHT,buff=.2).move_to(P(3,-3.1))
        self.add(c1,c3,lab1,lab3)
        self.at("developing synapses")
        self.play(*[m.animate.scale(1.08) for m in (c1,c3)],run_time=.55)
        self.finish()


class S09Caution(SpokenScene):
    def construct(self):
        nn=neuron(P(-4,.3),1.55)
        mg=microglia(P(4,.3),1.65,procs=((45,1.45),(125,1.45),(215,1.45),(305,1.45)))
        self.add(T("Caution",40,GOLD).move_to(P(0,3.3)),nn,mg,
                 T("neuron",30,GREY).move_to(P(-4,2.4)),T("microglia",30,PURPLE).move_to(P(4,2.4)))
        self.at("neurons can make")
        source=T("most brain C1q",28,YELLOW).move_to(P(4,-2.05))
        self.play(FadeIn(lines("can make C1q",28,YELLOW).move_to(P(-4,-2.05))),FadeIn(source),run_time=.45)
        self.at("most brain",lead=.65)
        self.play(Indicate(source,color=YELLOW,scale_factor=1.03),run_time=.4)
        self.at("which cell supplies")
        sy=synapse(P(0,-1.7),.7)
        q=T("?",86,GOLD).move_to(P(0,1.3))
        self.play(FadeIn(sy),FadeIn(q),run_time=.45)
        self.at("supplies it")
        self.play(Create(DashedLine(P(-3.1,-.5),P(-1.15,-1.7),color=YELLOW)),
                  Create(DashedLine(P(3.1,-.5),P(1.2,-1.7),color=YELLOW)),run_time=.45)
        self.at("not settled")
        self.play(FadeIn(T("not settled",40,GOLD).move_to(P(0,-3.2))),run_time=.45)
        self.finish()


# Identical territory coordinates and aspect ratio in every genotype comparison.
XS=(-4.3,0,4.3)

def territory_panel(cx,label,kind=None,cy=-.3,h=5.5,w=4):
    box=RoundedRectangle(width=w,height=h,corner_radius=.25,color=GREY,fill_color=GREY,fill_opacity=.05).move_to(P(cx,cy))
    title=T(label,26,RED if 'knockout' in label else TEXT).move_to(P(cx,cy+h/2-.45))
    g=VGroup(box,title)
    outline=RoundedRectangle(width=w-.5,height=h-1.7,corner_radius=.5,color=GREY).move_to(P(cx,cy-.05))
    g.add(outline)
    if kind:
        a,b=((0,.52),(.48,1)) if kind=='normal' else ((0,.68),(.32,1))
        for (lo,hi),col in ((a,EYE_A),(b,EYE_B)):
            g.add(Rectangle(width=(hi-lo)*(w-.6),height=h-1.9,color=col,fill_color=col,fill_opacity=.4).move_to(P(cx-(w-.6)/2+(lo+hi)/2*(w-.6),cy-.05)))
        overlap=(.04 if kind=='normal' else .36)*(w-.6)
        zone=Rectangle(width=overlap,height=h-1.9,color=TEXT,stroke_width=2,fill_color=TEXT,fill_opacity=.25).move_to(P(cx,cy-.05))
        g.add(zone,T("overlap",26,TEXT).move_to(P(cx,cy-h/2+.35)),Line(P(cx,cy-h/2+.65),P(cx,cy-(h-1.9)/2),color=TEXT))
    else:
        g.add(T("dLGN",30,GREY).move_to(P(cx,cy)))
    return g


def comparison(two=False):
    # Two panels are centred; same geometry persists when the third is added.
    xs=(-2.15,2.15) if two else XS
    labs=('normal','C1q knockout') if two else ('normal','C1q knockout','C3 knockout')
    return VGroup(*[territory_panel(x,lab,'normal' if i==0 else 'ko') for i,(x,lab) in enumerate(zip(xs,labs))])


def eye_legend():
    return VGroup(T("left eye",28,EYE_A),T("right eye",28,EYE_B),T("schematic",26,GREY)).arrange(RIGHT,buff=.7).move_to(P(0,3.25))


def predict_stage():
    return VGroup(T("Predict",40,GOLD).move_to(P(0,3.35)),
        T("complement helps remove losing inputs",30,YELLOW).move_to(P(0,2.4)),
        territory_panel(-3.2,'normal',cy=-.55,h=4.8,w=5.7),territory_panel(3.2,'C1q knockout',cy=-.55,h=4.8,w=5.7))


class S10Predict(SpokenScene):
    def construct(self):
        stage=predict_stage(); stage[1].set_opacity(0); self.add(stage)
        self.at("If complement helps")
        self.play(stage[1].animate.set_opacity(1),run_time=.45)
        self.at("look like",lead=0)
        self.play(FadeIn(T("?",100,RED).move_to(P(3.2,-1.5))),run_time=.3)
        self.finish()


class S11Pause(NarratedScene):
    def construct(self):
        self.add(predict_stage(),T("?",100,RED).move_to(P(3.2,-1.5)))
        prompt=T("Pause. Predict first.",30,GOLD).move_to(P(-3.2,-1.5)); self.add(prompt)
        count=T("5",30,GOLD).move_to(P(0,-3.35)); self.add(count)
        for n in (4,3,2,1):
            self.wait(.8)
            self.play(Transform(count,T(str(n),30,GOLD).move_to(count)),run_time=.2)
        self.finish()


class S12Overlap(SpokenScene):
    def construct(self):
        panels=comparison(True); self.add(eye_legend(),panels)
        self.at("failed to refine")
        self.play(Indicate(panels[1][1],color=RED,scale_factor=1.05),run_time=.5)
        self.at("overlapped more")
        self.play(Indicate(panels[1][5],color=YELLOW,scale_factor=1.05),run_time=.6)
        self.at("normal littermates")
        self.play(Indicate(panels[0][5],color=TEXT,scale_factor=1.05),run_time=.5)
        self.finish()


def relay_inputs(c,angs,r=1.1):
    return VGroup(*[VGroup(Line(c+_unit(a)*r,c+_unit(a)*(r+.55),color=EYE_A if i%2==0 else EYE_B,stroke_width=6),
                     bulb(c+_unit(a)*(r+.75),EYE_A if i%2==0 else EYE_B,.33)) for i,a in enumerate(angs)])


class S13Cells(SpokenScene):
    def construct(self):
        nc,kc=P(-3.2,-.25),P(3.2,-.25)
        n=neuron(nc,1.55); k=neuron(kc,1.55); few=relay_inputs(nc,(50,130),1.55)
        self.add(T("Single relay neurons · schematic",32,GREY).move_to(P(0,3.3)),
                 T("normal",30,TEXT).move_to(P(-3.2,2.6)),T("C1q knockout",30,RED).move_to(P(3.2,2.6)),n,few,
                 T("two inputs",28,TEXT).move_to(P(-3.2,-2.5)),k)
        self.at("Most knockout cells")
        many=relay_inputs(kc,(0,36,72,108,144,180),1.55)
        self.play(LaggedStart(*[FadeIn(m) for m in many],lag_ratio=.15),run_time=.8)
        self.at("still received")
        self.play(FadeIn(T("several inputs",28,TEXT).move_to(P(3.2,-2.5))),run_time=.3)
        self.at("normal cells")
        self.play(Indicate(few,color=TEXT,scale_factor=1.05),run_time=.5)
        self.finish()


class S14C3(SpokenScene):
    def construct(self):
        old=comparison(True); self.add(old,eye_legend())
        new=comparison()
        self.at("C3")
        self.play(Transform(old,VGroup(*new[:2])),FadeIn(new[2]),run_time=.55)
        self.at("similar overlap")
        self.play(Indicate(new[2][5],color=YELLOW,scale_factor=1.04),run_time=.5)
        self.finish()


class S15Beat(NarratedScene):
    def construct(self):
        self.add(eye_legend(),comparison()); self.finish()


def summary_panels():
    return VGroup(*[territory_panel(x,lab,'normal' if i==0 else 'ko',cy=-1.45,h=3.7) for i,(x,lab) in enumerate(zip(XS,('normal','C1q knockout','C3 knockout')))])


class S16Proves(SpokenScene):
    def construct(self):
        ps=summary_panels()
        self.add(T("What this shows",38,GOLD).move_to(P(0,3.3)),ps)
        self.at("complement is needed")
        cb=lines("complement is needed for\nnormal refinement in this circuit",36,TEXT).move_to(P(0,1.65))
        self.play(FadeIn(cb),run_time=.6)
        self.at("normal refinement")
        self.play(*[Indicate(p[5],color=YELLOW,scale_factor=1.03) for p in ps],run_time=.7)
        self.finish()


class S17Not(SpokenScene):
    def construct(self):
        self.add(T("What it does not show",38,RED).move_to(P(0,3.3)))
        cards=[]
        for x,col in zip(XS,(YELLOW,TEAL,PURPLE)):
            box=RoundedRectangle(width=4,height=5.5,corner_radius=.2,color=col,fill_color=col,fill_opacity=.06).move_to(P(x,-.2))
            q=T("?",100,col).move_to(P(x,.7)); self.add(box,q); cards.append((x,col))
        labels=[]
        for (x,col),label in zip(cards,("which synapse\ngot a tag","what\nread it","which cell carried\nthe input away")):
            lab=lines(label,28,TEXT).move_to(P(x,-1.6)); self.add(lab); labels.append(lab)
        for phrase,(x,col),label in zip(('which synapse','what read it','which cell'),cards,('which synapse\ngot a tag','what\nread it','which cell carried\nthe input away')):
            self.at(phrase)
            self.play(Indicate(labels[cards.index((x,col))],color=col,scale_factor=1.03),run_time=.35)
        self.finish()


class S18Take(SpokenScene):
    def construct(self):
        sy=synapse(P(-2.3,-.3),1.6)
        ring=DashedVMobject(Circle(radius=2,color=PURPLE,stroke_width=6).move_to(P(4,-.3)),num_dashes=24)
        self.add(sy,ring,T("?",110,PURPLE).move_to(P(4,-.3)))
        self.at("a tag")
        tags=VGroup(*[DashedVMobject(Circle(radius=.2,color=YELLOW,stroke_width=4).move_to(P(-3.9,y)),num_dashes=8) for y in (-.9,-.3,.3)])
        self.play(FadeIn(tags),FadeIn(T("a tag?",38,YELLOW).move_to(P(-3.7,2.8))),run_time=.5)
        self.at("catch the eater")
        self.play(FadeIn(T("the eater?",38,PURPLE).move_to(P(4,2.8))),Create(DashedLine(P(1.9,-.3),P(.6,-.3),color=PURPLE)),run_time=.6)
        self.finish()


class S19End(EndCard):
    LINE = "Knockouts point to a tag. Catch the eater in the act."

    def construct(self):
        line=lines("Knockouts point to a tag.\nCatch the eater in the act.",40,TEXT,font=TITLE_FONT).move_to(P(0,.4))
        self.add(line)
        self.play(FadeIn(T("biochemistrypedia.com",26,TEAL).move_to(P(0,-1))),run_time=.5)
        self.finish()
