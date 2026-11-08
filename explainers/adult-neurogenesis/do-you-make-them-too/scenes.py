"""Do You Make Them Too?  (chapter 3 of 'Two Places the Adult Brain Still Makes Neurons')

COLOR MAP (one color per concept, shared with scenes.old.py and the other chapters)
  ORANGE = carbon-14 (the air curve, the level written into DNA, averaged readings)
  BLUE   = neurons, the neuron-identity fact (NeuN, neuron protein)
  YELLOW = the birth record (BrdU, the birth-year marker) and the questions
  PURPLE = the hippocampus (dentate gyrus outline, the hippocampus reading)
  GREEN  = young neurons seen by a stain (DCX, marked cells)
  GREY   = structure, axes, cards, other things
  RED    = a lost marker / a mismatch / crossed out
  TEXT   = the rule and plain labels
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"


# ---------------------------------------------------------------- helpers
def level(y):
    if y < 1955:
        return 1.0
    if y <= 1963:
        return 1.0 + 0.9 * ((y - 1955) / 8.0) ** 1.6
    return 1.9 - 0.6 * (y - 1963) / 52.0   # schematic: a plain declining line


def make_axes(center, w, h):
    ax = Axes(x_range=[1935, 2015, 10], y_range=[0.0, 2.2, 0.5], x_length=w, y_length=h,
              axis_config={"include_tip": False, "include_numbers": False, "include_ticks": False,
                           "stroke_color": GREY, "stroke_width": 3})
    ax.move_to([center[0], center[1], 0])
    return ax


def curve_pieces(ax):
    a = ax.plot(level, x_range=[1935, 1955], color=ORANGE, stroke_width=7)
    b = ax.plot(level, x_range=[1955, 1963], color=ORANGE, stroke_width=7)
    c = ax.plot(level, x_range=[1963, 2015], color=ORANGE, stroke_width=7)
    return a, b, c


def cell(r=0.8, color=BLUE, nuc=0.4):
    body = Circle(radius=r, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.22)
    n = Circle(radius=r * nuc, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.5)
    return VGroup(body, n)


def dna_bar(frac, w=1.8, h=0.3):
    out = RoundedRectangle(corner_radius=0.08, width=w, height=h, stroke_color=GREY, stroke_width=3,
                           fill_color=BG, fill_opacity=1)
    fill = Rectangle(width=max(0.001, (w - 0.1) * frac), height=h - 0.1, stroke_width=0,
                     fill_color=ORANGE, fill_opacity=0.95)
    fill.move_to(out.get_left() + RIGHT * (0.05 + fill.width / 2))
    return VGroup(out, fill)


def arrow(a, b, color=GREY, w=6):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=0.25,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def dg_arc(r=1.9, color=PURPLE, n=14, dot_r=0.13, dot_color=BLUE):
    """Dentate gyrus as a thick C-shaped arc with neurons (dots). Returns (group, dots)."""
    arc = Arc(radius=r, start_angle=-0.2 * PI, angle=1.4 * PI, stroke_color=color, stroke_width=30)
    arc.set_stroke(opacity=0.4)
    dots = VGroup()
    for k in range(n):
        t = (k + 0.5) / n
        ang = -0.2 * PI + 1.4 * PI * t
        p = arc.get_arc_center() + r * np.array([np.cos(ang), np.sin(ang), 0])
        dots.add(Dot(p, radius=dot_r, color=dot_color))
    return VGroup(arc, dots), dots


def old_brain_outline():
    return VGroup(Ellipse(width=8.4, height=4.6, color=GREY, stroke_width=4,
                          fill_color=GREY, fill_opacity=0.12),
                  Ellipse(width=1.35, height=1.0, color=GREY, fill_color=GREY,
                          fill_opacity=0.12).move_to([-4.4, -0.3, 0]),
                  Ellipse(width=1.6, height=1.3, color=GREY, fill_color=GREY,
                          fill_opacity=0.12).move_to([3.5, -1.35, 0]))


def person(color=GREY):
    head = Circle(radius=0.34, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.25)
    body = RoundedRectangle(width=1.1, height=1.1, corner_radius=0.5, stroke_color=color, stroke_width=4,
                            fill_color=color, fill_opacity=0.25)
    body.next_to(head, DOWN, buff=0.1)
    return VGroup(head, body)


def syringe(color=YELLOW):
    barrel = Rectangle(width=1.8, height=0.6, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.2)
    needle = Line(barrel.get_left(), barrel.get_left() + LEFT * 0.9, color=color, stroke_width=4)
    rod = Line(barrel.get_right(), barrel.get_right() + RIGHT * 0.6, color=color, stroke_width=4)
    thumb = Line(rod.get_end() + UP * 0.3, rod.get_end() + DOWN * 0.3, color=color, stroke_width=6)
    return VGroup(barrel, needle, rod, thumb)


def tick(color, s=0.22):
    return VGroup(Line([-s, 0, 0], [-s * 0.3, -s * 0.8, 0], color=color, stroke_width=7),
                  Line([-s * 0.3, -s * 0.8, 0], [s * 1.2, s * 0.9, 0], color=color, stroke_width=7))


def crossmark(color=RED, s=0.2):
    return VGroup(Line([-s, -s, 0], [s, s, 0], color=color, stroke_width=7),
                  Line([-s, s, 0], [s, -s, 0], color=color, stroke_width=7))


def fitw(m, w):
    if m.width > w:
        m.scale(w / m.width)
    return m


# All plot traces use level(), the shared reference's schematic equation.
# DNA is a labelled level gauge, never a molecular structure.
def label(text, x, y, size=28, color=TEXT):
    return T(text, size, color).move_to([x,y,0])


def brain_outline():
    pts=[[-4,-.6,0],[-4.3,.2,0],[-3.8,1.3,0],[-2.9,2,0],[-1.5,2.5,0],
         [0,2.6,0],[1.5,2.3,0],[2.8,1.6,0],[3.7,.6,0],[3.9,-.5,0],
         [3.3,-1.3,0],[2,-1.6,0],[1,-1.3,0],[.3,-1.5,0],[-1,-1.4,0],[-2.6,-1.4,0],[-4,-.6,0]]
    outline=VMobject(stroke_color=GREY,stroke_width=5,fill_color=GREY,fill_opacity=.13).set_points_smoothly(pts)
    folds=VGroup()
    for x,y in [(-2.7,.5),(-1.4,1.2),(.1,1.3),(1.6,.7)]:
        folds.add(VMobject(stroke_color=GREY,stroke_width=3).set_points_smoothly([[x-.4,y+.6,0],[x,y+.2,0],[x-.2,y-.4,0],[x+.3,y-.7,0]]))
    cerebellum=Ellipse(width=2,height=1.3,color=GREY,fill_color=GREY,fill_opacity=.2).move_to([2.6,-1.65,0])
    stem=Polygon([1,-1.4,0],[1.6,-1.4,0],[1.8,-2.5,0],[1.2,-2.5,0],color=GREY,fill_color=GREY,fill_opacity=.2)
    return VGroup(outline,folds,cerebellum,stem)


def hippocampus():
    return VMobject(stroke_color=PURPLE,stroke_width=24).set_points_smoothly(
        [[1.9,-.2,0],[1.2,-.9,0],[0,-1.1,0],[-.8,-.7,0],[-1,-.1,0],[-.6,.15,0],[-.25,-.1,0]])


class Plot:
    def __init__(self):
        self.ax=make_axes([-1.25,-.15],9.7,5.55)
        self.a,self.b,self.c=curve_pieces(self.ax)
        self.curve=VGroup(self.a,self.b,self.c)
        self.ylab=label('carbon-14 in DNA (relative)',-1.6,3.35,30,ORANGE)
        self.ticks=VGroup()
        for yr in [1950,1963,2000]:
            pt=self.ax.c2p(yr,0)
            self.ticks.add(Line(pt+DOWN*.08,pt+UP*.08,color=GREY),T(str(yr),26,GREY).move_to(pt+DOWN*.4))
        for val in [1,2]:
            pt=self.ax.c2p(1935,val)
            self.ticks.add(T(str(val),26,GREY).move_to(pt+LEFT*.35))
        self.m63=DashedLine(self.ax.c2p(1963,0),self.ax.c2p(1963,level(1963)),color=GREY)
        self.pt=self.ax.c2p(1975,level(1975))
        self.byear=DashedLine(self.ax.c2p(1975,0),self.pt,color=YELLOW,stroke_width=4)
        self.bl=label('born 1970s',.1,-3.5,26,YELLOW)
        self.hdot_pos=self.ax.c2p(1975,level(1975)-.5)
        self.schematic=label('schematic',4.9,-3.4,26,GREY)
    def base(self): return [self.ax,self.curve,self.ylab,self.ticks,self.m63,self.schematic]
    def birth(self): return [self.byear,self.bl]
    def hip_dot(self): return Dot(self.hdot_pos,radius=.16,color=PURPLE)
    def hip_chip(self):
        ch=bchip('hippocampus',PURPLE,28).move_to([3.1,-.4,0])
        return ch,Line(ch.get_left(),self.hdot_pos,buff=.15,color=PURPLE)
    def gap(self):
        return (DoubleArrow(self.pt+DOWN*.1,self.hdot_pos+UP*.13,buff=0,color=RED,tip_length=.14),
                label('no match',.15,.75,26,RED))


def add_plot_base(scene,P): scene.add(*P.base())


def pause_marker(scene): scene.add(label('pause and think',4.7,-2.65,26,YELLOW))


COLX=[-4.4,-1.2,1.8,4.6]; ROWY=[1.05,-.15,-1.35]
def table():
    frame=RoundedRectangle(width=12.7,height=5.3,corner_radius=.15,color=GREY).move_to([0,.4,0])
    heads=VGroup(*[label(t,x,2.3,26,c) for t,x,c in [('Birth record',-1.2,YELLOW),('Neuron identity',1.8,BLUE),('Same cells',4.6,TEXT)]],Line([-6.3,1.7,0],[6.3,1.7,0],color=GREY))
    rows=[]
    for i,n in enumerate(['BrdU in patients','carbon-14','DCX staining']):
        y=ROWY[i]; parts=[label(n,-4.4,y,26)]
        parts.extend([tick(YELLOW).move_to([-1.2,y,0]) if i<2 else crossmark().move_to([-1.2,y,0]),
                      tick(BLUE).move_to([1.8,y,0]) if i<2 else label('debated',1.8,y,26,GREEN),
                      tick(TEXT).move_to([4.6,y,0]) if i==0 else label('pooled nuclei' if i==1 else '—',4.6,y,26,GREY)])
        rows.append(VGroup(*parts))
    return frame,heads,rows


def s13_table_static(scene):
    f,h,r=table(); scene.add(f,h,*r); return f,h,r


class S00Title(TitleCard):
    LESSON='Two Places the Adult Brain Still Makes Neurons'
    TITLE='Do You Make Them Too?'
    def construct(self):
        self.add(label('BIOCHEMISTRYPEDIA',0,1.7,28,TEAL),label('ADULT NEUROGENESIS: RODENTS AND PEOPLE',0,.8,26,GREY))
        self.play(FadeIn(T(self.TITLE,48,font=TITLE_FONT).move_to([0,-.4,0])),run_time=.6)
        self.finish()


class S01Q(SpokenScene):
    def construct(self):
        human=brain_outline().scale(.85).move_to([0,.25,0])
        hip=hippocampus().scale(.85).shift(UP*.5)
        # Smooth rodent cerebrum and conspicuous anterior olfactory bulbs.
        rodent=VGroup(Ellipse(width=5.5,height=3.1,color=GREY,fill_color=GREY,fill_opacity=.13),
                      Ellipse(width=1.15,height=.8,color=GREY,fill_color=GREY,fill_opacity=.2).move_to([-3,.35,0]),
                      Ellipse(width=1.15,height=.8,color=GREY,fill_color=GREY,fill_opacity=.2).move_to([-3,-.35,0]),
                      Ellipse(width=1.4,height=1.5,color=GREY,fill_color=GREY,fill_opacity=.2).move_to([2.6,-.4,0]),
                      Line([2.7,-1,0],[3.2,-1.7,0],color=GREY,stroke_width=12)).shift(UP*.4)
        head=label('Adult rodents: new neurons',0,3.2,36,BLUE)
        species=label('rodent brain',-4.6,-2.9,28,GREY)
        hl=label('hippocampus',-3.9,-1.9,28,PURPLE)
        leader=Line(hl.get_right(),hip.get_left(),buff=.15,color=PURPLE)
        self.add(rodent,head,species)
        self.at('do adult humans')
        self.play(ReplacementTransform(rodent,human),FadeIn(hip),FadeIn(hl),Create(leader),
                  Transform(head,label('Adult humans?',0,3.2,40,YELLOW)),
                  Transform(species,label('human brain',-4.6,-2.9,28,GREY)),run_time=.45)
        self.finish()


def clinical_group(patient=False):
    p=person().scale(2.7).move_to([3.1,.1,0])
    syr=syringe().scale(1.65).move_to([-3.2,.4,0])
    g=VGroup(p,syr,label('BrdU',-3.2,1.6,40,YELLOW),label('patients with cancer' if patient else 'healthy people',3.1,-2.8,30))
    if patient:
        g.add(Rectangle(width=1.2,height=.35,color=TEXT,fill_color=TEXT,fill_opacity=.8).move_to([3.1,-.7,0]),label('hospital',3.1,2.7,28,BLUE))
    return g


class S02Brdu(SpokenScene):
    def construct(self):
        g=clinical_group(); self.add(g)
        self.at('cannot be given')
        self.play(Create(crossmark(RED,1.2).move_to(g[1])),run_time=.4)
        self.finish()


class S03Pat(SpokenScene):
    def construct(self):
        g=clinical_group(True); g[1].scale(.78).move_to([-4,.4,0]); self.add(g,label('1990s',0,3.3,36,YELLOW))
        chart=RoundedRectangle(width=1.8,height=2.3,corner_radius=.1,color=GREY).move_to([-.1,0,0])
        lines=VGroup(*[Line([-.7,.65-.45*k,0],[.5,.65-.45*k,0],color=GREY) for k in range(4)])
        self.at('cancer patients'); self.play(FadeIn(chart),FadeIn(lines),FadeIn(label('clinical\nrecords',-.1,-2,28)),run_time=.4)
        self.at('received it'); self.play(g[1].animate.shift(RIGHT*.35),run_time=.4)
        self.finish()


class S04Pat2(SpokenScene):
    def construct(self):
        dg,_=dg_arc(2.7,n=16); dg.move_to([-1,0,0])
        dl=label('dentate gyrus (human, after death)',0,3.2,30,PURPLE)
        self.add(dg,dl)
        self.at('cells with both')
        c=cell(2.3,GREY,.58).move_to([-2.7,-.1,0])
        self.play(FadeOut(dg),FadeIn(c),run_time=.35)
        br=Circle(radius=1.12,color=YELLOW,fill_color=YELLOW,fill_opacity=.5).move_to(c[1])
        self.play(FadeIn(br),FadeIn(label('BrdU',-2.7,2.5,30,YELLOW)),run_time=.35)
        self.at('a neuron protein')
        neu=Circle(radius=1.12,color=BLUE,fill_color=BLUE,fill_opacity=.45).move_to(c[1]).shift(RIGHT*.25)
        self.play(FadeIn(neu),FadeIn(label('BrdU + NeuN',-2.7,-.1,28)),run_time=.35)
        facts=VGroup(label('Birth record',3.5,.9,32,YELLOW),label('Neuron identity',3.5,-.6,32,BLUE),tick(YELLOW).move_to([5.6,.9,0]),tick(BLUE).move_to([5.6,-.6,0]))
        self.at('both facts'); self.play(FadeIn(facts),run_time=.3)
        self.add(label('one human cell',-2.7,-3,28))
        self.finish()


class S05Bomb(SpokenScene):
    def construct(self):
        P=Plot(); P.ylab=label('carbon-14 in air (relative)',-1.6,3.35,30,ORANGE)
        self.add(P.ax,P.ticks,P.ylab,P.schematic,label('Bomb tests',4.9,2.2,32,ORANGE))
        self.play(Create(P.a),run_time=.7)
        self.at('the 1950s'); self.add(label('1950s–\nearly 1960s',4.9,1.1,28))
        self.play(Create(P.b),run_time=1.5)
        self.at('sharply raised'); self.play(Create(P.m63),FadeIn(label('sharply\nraised',4.9,-.7,32,ORANGE)),run_time=.5)
        self.finish()


class S06Keep(SpokenScene):
    def construct(self):
        # A smaller chart here leaves the right half for the actual uptake mechanism.
        P=Plot(); P.ax=make_axes([-3.5,-.65],5.4,3.7)
        P.a,P.b,P.c=curve_pieces(P.ax)
        self.add(P.ax,P.a,P.b,label('carbon-14 (relative)',-3.5,1.55,26,ORANGE))
        for yr in [1950,1963,2000]: self.add(label(str(yr),P.ax.c2p(yr,0)[0],-3.35 if yr==1963 else -2.9,26,GREY))
        for val in [1,2]: self.add(label(str(val),-6.55,P.ax.c2p(1935,val)[1],26,GREY))
        self.add(label('schematic',-1.4,-3.35,26,GREY))
        self.play(Create(P.c),run_time=.5)
        chain=VGroup(*[bchip(t,ORANGE,28).move_to([x,2.8,0]) for t,x in [('air CO2',-4.8),('plant',-1.6),('food',1.3)]])
        a1=arrow([-3.6,2.8,0],[-2.4,2.8,0],ORANGE); a2=arrow([-.8,2.8,0],[.55,2.8,0],ORANGE)
        c=cell(2.15,GREY,.68).move_to([3.7,-.2,0]); name=label('dividing cell',4.25,2.3,30)
        gauge=dna_bar(level(1975)/2,3.1,.7).move_to([3.7,-.15,0])
        self.add(chain,a1,a2,c,name)
        self.at('ends up')
        tracer=Dot([-4.8,2.8,0],radius=.13,color=ORANGE)
        path=VMobject().set_points_as_corners([[-4.8,2.8,0],[-1.6,2.8,0],[1.3,2.8,0],[2.7,1,0],[3.7,-.15,0]])
        self.add(tracer)
        self.play(MoveAlongPath(tracer,path),GrowArrow(arrow([1.8,2.4,0],[2.7,1,0],ORANGE)),FadeIn(gauge),run_time=.9)
        self.play(c[1].animate.set_color(ORANGE),run_time=.2)
        self.remove(tracer)
        self.add(label('DNA: relative level',3.7,.75,28,ORANGE),label('0',2.15,-.95,26,GREY),label('2',5.25,-.95,26,GREY))
        self.at('dividing cells')
        pt=P.ax.c2p(1975,level(1975)); dot=Dot(pt,radius=.12,color=ORANGE)
        self.play(FadeIn(dot),Create(DashedLine(pt,gauge.get_left(),color=ORANGE)),Create(DashedLine(P.ax.c2p(1975,0),pt,color=YELLOW)),FadeIn(label('1975',pt[0],-2.9,26,YELLOW)),run_time=.5)
        self.at("a neuron's dna"); self.play(c.animate.set_color(BLUE),Transform(name,label('neuron',4.25,2.3,30,BLUE)),run_time=.4)
        self.at('last division'); self.play(FadeIn(label('last division:\nlevel frozen',3.7,-2.75,30,YELLOW)),run_time=.3)
        self.finish()


def cortex_readings(P):
    dot=Dot(P.pt,radius=.14,color=BLUE); ring=Circle(radius=.27,color=BLUE).move_to(P.pt)
    ch=label('back of cortex',2.6,.1,28,BLUE); ch2=label('olfactory bulb',2.6,-1.1,28,BLUE)
    l1=Line(ch.get_left(),P.pt,buff=.15,color=BLUE); l2=Line(ch2.get_left(),P.pt,buff=.3,color=BLUE)
    return VGroup(dot,ch,l1),VGroup(ring,ch2,l2,label('(unlike rodents)',3,-1.8,26,GREY))


class S07Cortex(SpokenScene):
    def construct(self):
        P=Plot(); add_plot_base(self,P); self.add(*P.birth())
        a,b=cortex_readings(P)
        self.at('back of the cortex'); self.play(FadeIn(a),run_time=.35)
        self.at("match the person's own"); self.add(label('match birth year',4.4,2.5,28,YELLOW))
        self.at('so were',lead=.4); self.play(FadeIn(b),run_time=.25)
        # The next scene also carries these readings through its opening.
        self.finish()


def s08_static(scene,P,questions=True):
    add_plot_base(scene,P); scene.add(*P.birth(),P.hip_dot(),*P.hip_chip(),*P.gap())
    if questions: scene.add(label('What can you\nconclude?',4.9,1.8,28,YELLOW),label('…and what not?',4.9,.85,26,YELLOW))


class S08Pred(SpokenScene):
    def construct(self):
        P=Plot(); add_plot_base(self,P); self.add(*P.birth()); a,b=cortex_readings(P); self.add(a,b)
        self.at('hippocampal neurons'); self.play(FadeOut(a),FadeOut(b),FadeIn(P.hip_dot()),FadeIn(P.hip_chip()[0]),Create(P.hip_chip()[1]),run_time=.4)
        self.at('do not match'); self.play(*[FadeIn(m) for m in P.gap()],run_time=.3)
        self.at('what can you conclude'); self.add(label('What can you\nconclude?',4.9,1.8,28,YELLOW))
        self.at('and what not'); self.add(label('…and what not?',4.9,.85,26,YELLOW)); self.finish()


class S09Pause(NarratedScene):
    def construct(self):
        s08_static(self,Plot()); pause_marker(self); self.finish()


def tube_parts():
    tube=VGroup(Line([-4,1.4,0],[-4,-1.6,0],color=GREY,stroke_width=6),Line([-2,1.4,0],[-2,-1.6,0],color=GREY,stroke_width=6),Arc(radius=1,start_angle=PI,angle=PI,arc_center=[-3,-1.6,0],color=GREY,stroke_width=6))
    return tube


def model_result(scene):
    liquid=Rectangle(width=1.85,height=1.7,stroke_width=0,fill_color=ORANGE,fill_opacity=.8).move_to([-3,-1,0])
    scene.add(liquid,arrow([-1.8,-.7,0],[.3,-.7,0],ORANGE),dna_bar(.65,3.4,.6).move_to([2.8,-.7,0]),label('one averaged reading',2.8,-1.6,30,ORANGE),label('how many?     when?',2.5,1.4,34,YELLOW),label('Needs a model',2.5,2.65,38,YELLOW))


class S10Rev1(SpokenScene):
    def construct(self):
        P=Plot(); s08_static(self,P,False)
        self.at('beyond measurement error')
        eb=VGroup(Line(P.hdot_pos+UP*.28,P.hdot_pos+DOWN*.28,color=TEXT,stroke_width=6),*[Line(P.hdot_pos+UP*y+LEFT*.2,P.hdot_pos+UP*y+RIGHT*.2,color=TEXT,stroke_width=6) for y in [-.28,.28]])
        self.play(Create(eb),run_time=.3)
        self.add(label('measurement error',-2,-1.3,26),Line([-2,-1.05,0],P.hdot_pos+DOWN*.3,color=GREY))
        self.at('points to neurons'); self.add(label('lower = younger,\nmade after birth',4.8,-1.1,26,BLUE))
        self.at('repair or stray')
        self.clear(); tube=tube_parts()
        self.add(tube,label('many nuclei',-3,3.2,30),
                 label('unless repair or\nstray nuclei explain it',2.8,1.2,30,GREY))
        colors=[BLUE,YELLOW,PURPLE,ORANGE,GREEN,RED,TEXT,TEAL]
        nuclei=VGroup(*[Circle(radius=.24,color=c,fill_color=c,fill_opacity=.95).move_to([-4.4+.4*k,2.3,0]) for k,c in enumerate(colors)])
        self.add(nuclei)
        # Begin at 4.64 s, while the repair/stray-nuclei caveat is spoken.
        self.play(LaggedStart(*[d.animate.move_to([-3+.3*((k%3)-1),-1.5+.45*(k//3),0]) for k,d in enumerate(nuclei)],lag_ratio=.16),run_time=2.8)
        self.at('but a sample')
        self.clear(); self.add(tube,label('many nuclei',-3,3.2,30)); model_result(self)
        self.at('how many'); self.play(Indicate(self.mobjects[-1],color=YELLOW),run_time=.4); self.finish()



class S11Beat(NarratedScene):
    def construct(self):
        self.add(tube_parts(),label('many nuclei',-3,3.2,30)); model_result(self); pause_marker(self); self.finish()


class S12Est(SpokenScene):
    def construct(self):
        dg,_=dg_arc(2.65,n=0); dg.move_to([-3.2,-.1,0]); self.add(dg,label('model estimate',0,3.2,32,GREY),label('daily flow (schematic)',-3.2,2.6,26,BLUE),label('one hippocampus',-3.2,-3.2,28,PURPLE))
        self.add(label('about 700',3.2,1.5,48),label('new neurons',3.2,.3,36,BLUE),label('per hippocampus',3.2,-.8,32,PURPLE),label('per day',3.2,-2,48,YELLOW))
        # A continuous stream fades inside the hippocampus; dots are not a total.
        self.add(arrow([-6.25,1.45,0],[-4.7,1.05,0],BLUE))
        self.at('about 700')
        stream=VGroup(*[Dot(radius=.14,color=BLUE) for _ in range(12)])
        clock=[0.0]
        def flow(group,dt):
            clock[0]+=dt
            for k,d in enumerate(group):
                age=clock[0]-k*.22
                if age<0:
                    d.set_opacity(0); continue
                u=(age%2.1)/2.1
                d.move_to([-6.1+3.65*u,1.15-1.9*u+.18*np.sin(k),0])
                d.set_opacity(min(1,u*8)*min(1,(1-u)*4))
        stream.add_updater(flow); self.add(stream)
        self.at('per day'); self.play(Indicate(self.mobjects[7],color=YELLOW),run_time=.4)
        self.finish(); stream.clear_updaters()



class S13Stain(SpokenScene):
    def construct(self):
        f,h,r=table(); self.add(f,h,r[0],r[1])
        self.at('young neurons'); self.add(r[2][0])
        self.at('a state'); self.play(Create(r[2][1]),FadeIn(label('a state, not a birth date',0,-2.8,32,RED)),run_time=.4)
        self.at('in people'); self.add(r[2][2]); self.at('only new neurons'); self.add(r[2][3]); self.finish()


def tissue(x,positive=False):
    # A broad C-shaped tissue section, with neutral nuclei and a DCX overlay.
    band=Arc(radius=1.9,start_angle=-.3*PI,angle=1.5*PI,stroke_color=PURPLE,stroke_width=75,stroke_opacity=.45).move_to([x,-.25,0])
    cells=VGroup()
    for k in range(30):
        ang=-.3*PI+1.5*PI*(k+.5)/30
        rad=1.9+(.15 if k%2 else -.15)
        pt=band.get_arc_center()+rad*np.array([np.cos(ang),np.sin(ang),0])
        d=Dot(pt,radius=.1,color=GREY)
        cells.add(d)
        if positive and k%2==0:
            cells.add(Dot(pt,radius=.16,color=GREEN))
    return VGroup(band,cells)


class S14Dis(SpokenScene):
    def construct(self):
        self.add(label('DCX staining in dentate gyrus',0,3.4,32,GREEN),tissue(-3.3),tissue(3.3),label('Sorrells 2018',-3.3,2.6,28),label('Moreno-Jimenez 2019',3.3,2.6,28))
        self.add(label('neurons, no DCX',-3.3,-2.45,28,GREY),label('neurons, no DCX',3.3,-2.45,28,GREY))
        baseline_right=self.mobjects[-1]
        self.at('one study found none'); self.add(label('no DCX in adults',-3.3,-3.1,30,RED))
        self.at('others found thousands'); self.remove(self.mobjects[2],baseline_right); self.add(tissue(3.3,True))
        self.add(label('thousands',3.3,-2.8,30,GREEN),label('adults up to old age',3.3,-3.4,26)); self.finish()


def young_dots(box):
    return VGroup(*[Dot(box.get_center()+[x,y,0],radius=.16,color=GREEN) for y in [-1.7,1.7] for x in [-2,-1,0,1,2]])


def prediction_parts():
    box=RoundedRectangle(width=6.2,height=5.2,corner_radius=.2,color=PURPLE,fill_color=PURPLE,fill_opacity=.08).move_to([2.7,-.1,0])
    inlet=VGroup(label('700 a day',-4.4,.7,38,BLUE),arrow([-3,.7,0],[-.6,.7,0],BLUE))
    q=VGroup(label('?',2.7,-.1,150,YELLOW),label('how many at once?',-3.8,-1.3,30,YELLOW),label('weeks or months',2.7,-3.15,30,GREY))
    return box,inlet,q


def s15_static(scene):
    b,i,q=prediction_parts(); scene.add(label('Pause and predict',0,3.3,36,YELLOW),b,i,young_dots(b),q)


class S15Pred2(SpokenScene):
    def construct(self):
        b,i,q=prediction_parts(); self.add(label('Pause and predict',0,3.3,36,YELLOW),b,i)
        self.at('arrive each day'); ds=young_dots(b); starts=VGroup(*[d.copy().set_color(BLUE).move_to([-1,1.9,0]) for d in ds]); self.add(starts)
        self.play(LaggedStart(*[Transform(a,d) for a,d in zip(starts,ds)],lag_ratio=.05),run_time=1)
        self.at('stays young'); self.play(starts.animate.set_color(GREEN),run_time=.35)
        self.at('for weeks or months'); self.add(q[2])
        self.at('how many marked'); self.play(FadeIn(q[0]),FadeIn(q[1]),run_time=.35); self.finish()


class S16Pause(NarratedScene):
    def construct(self):
        s15_static(self); self.add(label('pause and think',-4.3,-3.3,26,YELLOW)); self.finish()


class S17Rev3(SpokenScene):
    def construct(self):
        self.add(label('rate × time',0,3.35,40,YELLOW),label('durations assumed',1.4,2.65,34,YELLOW),label('toy numbers · steady rate assumed',0,-3.45,28,YELLOW))
        box=RoundedRectangle(width=3.25,height=3.65,corner_radius=.15,color=PURPLE).move_to([-4.85,-.75,0])
        self.add(label('human duration\nunknown',-4.85,2.65,28,YELLOW),box,label('700 a day',-4.8,1.8,30,BLUE),arrow([-4.8,1.35,0],[-4.8,1,0],BLUE),label('marked cells',-4.8,-2.9,26,GREEN))
        self.add(*[Dot([-5.85+1*i,.45-.95*j,0],radius=.22,color=GREEN) for i in range(3) for j in range(3)])
        base=-2.65; scale=4.45/126000; xs=[-1.5,1.4,4.5]; vals=[700*d for d in [21,90,180]]
        self.add(Line([-2.6,base,0],[5.8,base,0],color=GREY),label('marked cells per hippocampus',-2.95,-.4,26,GREEN).rotate(PI/2),Line([-2.65,base,0],[-2.65,1.8,0],color=GREY))
        bars=[]
        for x,v,name in zip(xs,vals,['3 weeks','3 months','6 months']):
            bar=Rectangle(width=1.55,height=v*scale,color=GREEN,fill_color=GREEN,fill_opacity=.45).move_to([x,base+v*scale/2,0]); bars.append(bar)
            self.add(label(name,x,-3,26,GREY))
        self.add(*[b.copy().set_fill(opacity=0).set_stroke(opacity=.25) for b in bars])
        self.at('even three weeks'); self.play(GrowFromEdge(bars[0],DOWN),run_time=.4)
        self.at('about 15'); self.add(label('about 15,000',xs[0],base+vals[0]*scale+.35,26,GREEN))
        self.at('across one hippocampus'); self.play(Indicate(box,color=PURPLE),run_time=.4)
        self.at('these are toy'); self.play(*[GrowFromEdge(b,DOWN) for b in bars[1:]],run_time=.5)
        for x,v,t in zip(xs[1:],vals[1:],['about 63,000','about 126,000']): self.add(label(t,x,base+v*scale+.3,26,GREEN))
        self.finish()


CARDXY=[(-3.25,1.45),(3.25,1.45),(-3.25,-1.65),(3.25,-1.65)]
def card(i):
    x,y=CARDXY[i]
    box=RoundedRectangle(width=6.15,height=2.85,corner_radius=.15,color=GREY,fill_color=GREY,fill_opacity=.08).move_to([x,y,0])
    titles=['lower rate','protein lost','short or unmarked state','stain missed cells']
    title=label(titles[i],x,y+.95,30)
    if i==0:
        icon=VGroup(Rectangle(width=.6,height=1,color=GREY,fill_color=GREY,fill_opacity=.6).move_to([x-1.5,y-.15,0]),Rectangle(width=.6,height=.25,color=BLUE,fill_color=BLUE,fill_opacity=.8).move_to([x+1.5,y-.525,0]),label('average',x-1.5,y-.95,26,GREY),label('these donors',x+1.4,y-.95,26,BLUE),label('rate',x,y-.1,28))
    elif i==1:
        icon=VGroup(label('protein',x-1.8,y-.1,26,GREEN),Dot([x-.8,y-.1,0],radius=.2,color=GREEN),arrow([x-.4,y-.1,0],[x+.7,y-.1,0]),Circle(radius=.2,color=RED).move_to([x+1.2,y-.1,0]),label('wait / long fixation',x,y-.95,26,GREY))
    elif i==2:
        icon=VGroup(Line([x-2.3,y-.4,0],[x+2.3,y-.4,0],color=GREY),Rectangle(width=.8,height=.5,color=GREEN,fill_color=GREEN,fill_opacity=.7).move_to([x-1.5,y-.1,0]),label('duration',x+1.3,y-.05,28,GREEN),label('human state',x,y-.95,26,GREY))
    else:
        dots=VGroup(*[Dot([x-1.9+.7*k,y-.1,0],radius=.17,color=BLUE) for k in range(6)])
        icon=VGroup(dots,Rectangle(width=1.1,height=.75,color=GREEN).move_to([x-.5,y-.1,0]),label('detection',x,y-.95,28,GREEN))
    return VGroup(box,title,icon)


def cards_static(scene,n,active=None):
    scene.add(label('A count of none needs an explanation',0,3.35,32))
    cs=[]
    for i in range(n):
        c=card(i)
        if active is not None and i!=active:
            c[1:].set_opacity(.4); c[0].set_stroke(opacity=.4)
        elif active is not None: c[0].set_stroke(YELLOW,width=4)
        scene.add(c); cs.append(c)
    return cs


class S18Why(SpokenScene):
    def construct(self):
        cs=cards_static(self,1,0)
        self.at('a far lower rate'); self.play(cs[0][2][1].animate.stretch(.6,1,about_edge=DOWN),run_time=.5); self.finish()


class S19Why2(SpokenScene):
    def construct(self):
        cs=cards_static(self,2,1)
        self.at('lost'); self.play(cs[1][2][1].animate.set_opacity(.15),run_time=.5)
        self.at('fixed'); self.play(Indicate(cs[1][2][-1],color=YELLOW),run_time=.5); self.finish()


class S20Why3(SpokenScene):
    def construct(self):
        cs=cards_static(self,3,2)
        self.at('short'); self.play(cs[2][2][1].animate.stretch(.5,0),run_time=.35)
        self.at('unmarked'); self.play(cs[2][2][1].animate.set_opacity(.1),run_time=.35); self.finish()


class S20bWhy4(SpokenScene):
    def construct(self):
        cs=cards_static(self,4,3)
        self.at('missed'); self.play(cs[3][2][1].animate.shift(RIGHT*1.5),run_time=.7); self.finish()


class S21Beat(NarratedScene):
    def construct(self): cards_static(self,4); self.add(label('pause and think',0,-3.55,26,YELLOW)); self.finish()


class S22Close(SpokenScene):
    def construct(self):
        f,h,r=s13_table_static(self); r[2].set_opacity(.3)
        self.add(label('carbon-14: pooled nuclei, needs a model',0,-2.65,28,GREY))
        self.at('birth record'); self.play(*[Create(RoundedRectangle(width=12.35,height=1.1,corner_radius=.1,color=YELLOW).move_to([0,ROWY[i],0])) for i in [0,1]],run_time=.35)
        self.at('points to some'); self.add(label('some new neurons',0,-3.35,36)); self.finish()


class S23Open(SpokenScene):
    def construct(self):
        dg,_=dg_arc(3,n=18); dg.move_to([0,0,0]); self.add(dg,label('how many?',-4.7,1.5,38,YELLOW))
        self.at('what they do'); self.add(label('what for?',4.8,1.5,38,YELLOW))
        self.at('still open'); self.add(label('still open',0,-.7,46,YELLOW)); self.finish()


class S24Take(SpokenScene):
    def construct(self):
        c=cell(2.0,BLUE,.48).move_to([0,-.65,0])
        self.add(c,label('Takeaway',0,3.2,38),label('birth record',-2.9,2.1,34,YELLOW),label('+',0,2.1,42),label('neuron identity',3.1,2.1,34,BLUE),label('in the same cells',0,-3.25,34))
        self.at('same cells'); self.play(Indicate(c,color=BLUE),run_time=.4)
        self.at('a birth record'); self.play(c[1].animate.set_color(YELLOW),run_time=.4)
        self.at('neuron identity'); self.play(c[0].animate.set_stroke(BLUE,width=10),run_time=.35); self.finish()


class S25End(EndCard):
    LINE='Ask whether the same cells carry\na birth record and neuron identity.'
    def construct(self):
        self.add(T(self.LINE,38,font=TITLE_FONT),label('biochemistrypedia.com',0,-1.7,28,TEAL)); self.finish()
