"""Chapter 1: A Cell Cannot Name a Molecule.

COLOR MAP: SMELL's five hues = distinct smell receptor lines; BLUE = smell labels; YELLOW = inputs;
GREEN = activity; RED = no distinction; GREY = structure/rest;
ORANGE = sweet; PURPLE = bitter; PINK = umami; TEXT = sour and labels.
All meters are explicitly schematic examples, not experimental traces.
"""
import numpy as np
from bp_style import *
from bp_style import SpokenScene as BaseSpokenScene

ORANGE, PINK, PURPLE = '#F29E4C', '#E88FB4', '#B58CE8'
SMELL = [BLUE, '#F3C969', '#74D7AC', '#C6A0EF', '#EF9EAE']
CCOL = {'sweet': ORANGE, 'bitter': PURPLE, 'umami': PINK, 'sour': TEXT}


class SpokenScene(BaseSpokenScene):
    # Same word alignment as the pipeline; avoid creating an unrequested sync.log.
    def at(self, phrase, lead=.2, nth=0):
        rest = self.t_of(phrase, nth) - lead - self.elapsed()
        if rest > .02:
            self.wait(rest)


def heading(text, color=TEXT):
    return T(text, 32, color).move_to([0, 3.15, 0])


def receptor_cell(x=0, y=-.85, color=BLUE, width=3.35, height=3.35):
    return RoundedRectangle(width=width, height=height, corner_radius=.48,
                            stroke_color=color, stroke_width=4,
                            fill_color=color, fill_opacity=.14).move_to([x,y,0])


def meter(x=0, y=1.65, value=.02, width=2.5, height=1.4):
    edge = Rectangle(width=width, height=height, color=GREY, stroke_width=3).move_to([x,y,0])
    fill = Rectangle(width=width-.14, height=max(.018, (height-.14)*value),
                     stroke_width=0, fill_color=GREEN, fill_opacity=.9)
    fill.move_to([x, y-height/2+.07+fill.height/2, 0])
    return VGroup(edge,fill)


def level(m, value):
    return meter(m[0].get_x(), m[0].get_y(), value, m[0].width, m[0].height)[1]


def one_cell(value=.02):
    c = receptor_cell()
    label = T('receptor cell', 28, BLUE).move_to(c)
    wire = Arrow([0,.83,0], [0,.94,0], buff=0, color=GREY, stroke_width=4)
    return VGroup(c,label,wire,meter(value=value))


def equal_readings(question=True):
    g=VGroup()
    for x, name, conc in [(-3,'X','low concentration'),(3,'Y','higher concentration')]:
        c=receptor_cell(x,-.65,width=3.25,height=3.3)
        g.add(c,T('same cell',28,BLUE).move_to(c),meter(x,1.8,.62),
              T(name,30,YELLOW).move_to([x,2.85,0]),
              T(conc,26,YELLOW).move_to([x,-2.75,0]))
    if question:
        g.add(T('Can this cell tell which molecule it met?',34).move_to([0,3.5,0]))
    return g


def nose(x=-3.5,y=0,scale=1):
    # Side-view mouse face with a projecting snout, dark nose and whiskers.
    face=Polygon([-1.35,-1.05,0],[-1.35,.85,0],[-.75,1.3,0],[.05,.85,0],
                 [.65,.35,0],[1.35,.05,0],[1.4,-.55,0],[.5,-.95,0],
                 color=BLUE,fill_color=BLUE,fill_opacity=.12)
    ear=Ellipse(width=.65,height=.9,color=BLUE,fill_color=BG,fill_opacity=1).move_to([-.85,1.1,0])
    eye=Dot([-.15,.4,0],radius=.09,color=TEXT)
    tip=Ellipse(width=.48,height=.6,color=BLUE,fill_color=BLUE,fill_opacity=.8).move_to([1.22,-.25,0])
    nostril=Dot([1.28,-.17,0],radius=.07,color=BG)
    whisk=VGroup(*[Line([.75,-.5,0],[1.7,z,0],color=GREY,stroke_width=2) for z in [-.2,-.65,-1.0]])
    return VGroup(face,ear,eye,tip,nostril,whisk).scale(scale).move_to([x,y,0])


def tongue(x=3.5,y=0):
    shape=Ellipse(width=3.5,height=3.1,color=PURPLE,
                           fill_color=PURPLE,fill_opacity=.17).move_to([x,y,0])
    groove=Line([x,y+1.1,0],[x,y-1.05,0],color=PURPLE,stroke_width=2)
    return VGroup(shape,groove)


def pattern(values,x=0,y=0,width=7.8,height=4,labels=True,colors=None):
    g=VGroup(); step=width/len(values)
    for i,v in enumerate(values):
        xx=x-width/2+step*(i+.5)
        m=meter(xx,y,v,width=step*.6,height=height)
        if colors:
            m[1].set_fill(colors[i])
        g.add(m)
    if labels:
        g.add(VGroup(*[T(f'line {i+1}',26).move_to([x-width/2+step*(i+.5),y-height/2-.4,0]) for i in range(len(values))]))
    return g


def split_smell(readout=True):
    title=T('SMELL',32,BLUE).move_to([-3.45,3.15,0])
    bulb=RoundedRectangle(width=5.55,height=1.05,corner_radius=.3,color=GREY,fill_color=GREY,
                          fill_opacity=.07).move_to([-3.45,1.8,0])
    epi=RoundedRectangle(width=5.55,height=1.1,corner_radius=.15,color=GREY,
                         fill_color=GREY,fill_opacity=.08).move_to([-3.45,-2.05,0])
    lines=VGroup()
    for i,col in enumerate(SMELL):
        x=-5.55+i*1.03
        gl=Circle(.22,color=col,fill_color=col,fill_opacity=.45).move_to([x,1.8,0])
        cells=VGroup(*[receptor_cell(x+dx,-2.05+dy,col,.24,.65) for dx,dy in [(-.28,-.12),(0,.15),(.28,-.05)]])
        wires=VGroup(*[Line(c.get_top(),[x,1.55,0],color=col,stroke_width=2.5) for c in cells])
        lines.add(VGroup(wires,cells,gl))
    many=T('…',32,BLUE).move_to([-.95,-2.05,0])
    caption=T('about 1,000 separate lines',26,BLUE).move_to([-3.45,2.55,0])
    read=pattern([.3,.8,.5,.65,.4],-3.45,-3.0,5.0,.65,False,SMELL)
    readlabel=T('pattern across lines',26,GREEN).move_to([-3.45,-3.6,0])
    diagram=VGroup(bulb,epi,lines,many)
    return VGroup(title,diagram,caption,VGroup(read,readlabel) if readout else VGroup())


def taste_outline():
    return VGroup(T('TASTE',32,GREY).move_to([3.45,3.15,0]),
                  RoundedRectangle(width=5.6,height=5.65,corner_radius=.3,color=GREY,
                                   stroke_opacity=.3).move_to([3.45,-.15,0]))


def bitter_panel(ghosts=True):
    title=T('TASTE',32).move_to([3.45,3.15,0])
    cell=receptor_cell(3.35,.55,PURPLE,3.05,2.8)
    recs=VGroup()
    positions=[(2.3+i*.52,1.64) for i in range(5)]+[(2.3+i*.52,-.54) for i in range(5)]+[(2.15,.55),(4.55,.55)]
    for i,(x,y) in enumerate(positions):
        if i%3==0:
            r=Rectangle(width=.23,height=.34,color=PURPLE,fill_color=PURPLE,fill_opacity=.7)
        elif i%3==1:
            r=RoundedRectangle(width=.33,height=.22,corner_radius=.08,color=PURPLE,fill_color=PURPLE,fill_opacity=.7)
        else:
            r=Polygon([-.14,-.16,0],[.14,-.16,0],[.18,.1,0],[0,.2,0],[-.18,.1,0],color=PURPLE,fill_color=PURPLE,fill_opacity=.7)
        recs.add(r.move_to([x,y,0]))
    name=T('bitter cell',28,PURPLE).move_to([3.35,.55,0])
    rl=T('different receptors',26,PURPLE).move_to([3.35,2.48,0])
    leader=Line([3.35,2.22,0],[3.35,1.87,0],color=PURPLE)
    wire=Arrow([3.35,-.85,0],[3.35,-1.65,0],color=PURPLE,buff=0,stroke_width=5)
    nerve=T('to the nerve',26,PURPLE).move_to([5.2,-1.18,0])
    small=VGroup()
    if ghosts:
        for x,k in [(2,'sweet'),(3.4,'umami'),(4.8,'sour')]:
            c=receptor_cell(x,-2.55,CCOL[k],.75,1.0).set_opacity(.65)
            small.add(c,T(k,26,CCOL[k]).move_to([x,-3.3,0]))
    return VGroup(title,cell,recs,name,VGroup(rl,leader),wire,nerve,small)


class S00Title(TitleCard):
    TITLE='A Cell Cannot Name a Molecule'
    LESSON='Smell and Taste'
    def construct(self):
        self.add(T('BIOCHEMISTRYPEDIA',26,TEAL).move_to([0,1.65,0]),
                 T(self.LESSON.upper(),28,TEXT).move_to([0,.85,0]))
        title=VGroup(T('A Cell Cannot',48,font=TITLE_FONT),T('Name a Molecule',48,font=TITLE_FONT)).arrange(DOWN,buff=.2).move_to([0,-.55,0])
        self.play(FadeIn(title),run_time=.5)
        self.add(Line([-1.1,-2.05,0],[1.1,-2.05,0],color=GOLD,stroke_width=4))
        self.finish()


class S01Genes(SpokenScene):
    def construct(self):
        n=nose(-3.55,-.2,1.4)
        self.add(n,T('mouse nose',28,BLUE).move_to([-3.55,-2.35,0]))
        dots=VGroup(*[Dot([.1+(i%5)*1.12,1.25-(i//5)*1.05,0],radius=.17,color=SMELL[i%5]) for i in range(20)])
        self.at('has about')
        self.play(FadeIn(dots),FadeIn(heading('about 1,000 odorant-receptor genes',BLUE)),run_time=.5)
        self.add(T('receptor types',28,BLUE).move_to([2.35,-2.65,0]),
                 Arrow([-1.25,-.1,0],[-.3,-.1,0],buff=0,color=BLUE))
        self.at('It reads')
        odor=chip('odour',YELLOW,28).move_to([-3.55,2.1,0])
        self.play(FadeIn(odor),run_time=.25)
        self.play(odor.animate.move_to([-2.65,.15,0]).set_opacity(0),run_time=.4)
        self.at('a pattern across')
        active={0,2,5,8,11,13,19}
        self.play(*[d.animate.set_opacity(1 if i in active else .2).scale(1.35 if i in active else 1) for i,d in enumerate(dots)],
                  FadeIn(T('pattern across receptors',28,GREEN).move_to([1.65,2.3,0])),run_time=.5)
        self.finish()


class S02Question(SpokenScene):
    def construct(self):
        self.add(nose(-3.45,.15,1.15),T('mouse nose',28,BLUE).move_to([-3.45,-1.7,0]),
                 T('about 1,000',30,BLUE).move_to([-3.45,2.35,0]))
        tg=tongue(3.45,.15)
        shapes=VGroup(*[Rectangle(width=.23,height=.2+(i%3)*.06,color=PURPLE,fill_color=PURPLE,fill_opacity=.65).move_to([[2.45,2.95,3.95,4.45][i%4],.85-(i//4)*.65,0]) for i in range(12)])
        self.at('It also has')
        self.play(FadeIn(tg),FadeIn(shapes),FadeIn(T('tongue',28,PURPLE).move_to([3.45,-1.7,0])),run_time=.4)
        self.at('dozens of')
        self.play(FadeIn(T('dozens of bitter-receptor genes',28,PURPLE).move_to([0,3.25,0])),
                  FadeIn(T('dozens',30,PURPLE).move_to([3.45,2.35,0])),run_time=.4)
        self.at('Yet bitter')
        self.play(Create(Arrow([3.45,-1.98,0],[3.45,-2.48,0],buff=0,color=PURPLE)),
                  FadeIn(T('BITTER',32,PURPLE).move_to([3.45,-2.85,0])),
                  FadeIn(T('Why the difference?',38).move_to([-2.6,-2.8,0])),run_time=.3)
        self.at('Why the difference')
        self.play(Indicate(self.mobjects[-1],scale_factor=1.03),run_time=.3)
        self.finish()


class S03Cell(SpokenScene):
    def construct(self):
        g=one_cell(); self.add(g[0])
        self.at('one receptor cell')
        self.play(FadeIn(g[1]),run_time=.35)
        self.at('Its output')
        self.play(Create(g[2]),FadeIn(g[3]),run_time=.35)
        self.at('its activity')
        self.play(FadeIn(heading('activity',GREEN)),run_time=.3)
        self.add(T('at rest',26,GREY).move_to([2.5,1.65,0]))
        self.finish()


class S04Two(SpokenScene):
    def construct(self):
        g=one_cell(); self.add(g,heading('invented example',TEXT))
        x=VGroup(chip('X',YELLOW,30),
                 *[Square(.12,color=YELLOW,fill_color=YELLOW,fill_opacity=.45).move_to([dx,.43,0]) for dx in [-.4,.4]]).move_to([-4.5,.1,0])
        y=VGroup(Circle(.4,color=YELLOW,fill_color=YELLOW,fill_opacity=.45),T('Y',30,YELLOW),
                 *[Dot([dx,dy,0],radius=.065,color=YELLOW) for dx,dy in [(-.48,-.4),(-.5,.4),(0,.55),(.5,.4),(.48,-.4),(0,-.55)]]).move_to([4.5,.1,0])
        lx=T('low concentration',26,YELLOW).move_to([-4.35,-1.15,0])
        ly=T('higher\nconcentration',26,YELLOW).move_to([4.45,-1.15,0])
        self.at('Two different molecules')
        self.play(FadeIn(x),FadeIn(lx),run_time=.25)
        self.at('arrive')
        xl=Line([-3.3,-.95,0],[-1.65,-.18,0],color=YELLOW,stroke_width=2)
        self.play(x.animate.move_to([-1.15,.15,0]),Create(xl),run_time=.4)
        self.play(Transform(g[3][1],level(g[3],.62)),run_time=.3)
        ghost=meter(-4.35,1.65,.62,1.9,1.4)
        ghostlabel=T('X response',26,GREEN).move_to([-4.35,2.65,0])
        self.at('each at a concentration')
        self.play(FadeIn(ghost),FadeIn(ghostlabel),FadeOut(x),FadeOut(lx),FadeOut(xl),
                  Transform(g[3][1],level(g[3],.02)),FadeIn(y),FadeIn(ly),run_time=.25)
        yl=Line([3.3,-.95,0],[1.7,-.18,0],color=YELLOW,stroke_width=2)
        self.play(y.animate.move_to([1.15,.15,0]),Create(yl),run_time=.45)
        self.at('activates it equally')
        self.play(Transform(g[3][1],level(g[3],.62)),run_time=.35)
        self.play(FadeIn(T('same response',30,GREEN).move_to([0,-3.12,0])),run_time=.2)
        self.finish()


class S05Predict(SpokenScene):
    def construct(self):
        g=equal_readings(); self.add(*g[:-1])
        self.at('Can this cell')
        self.play(FadeIn(g[-1]),run_time=.25)
        self.finish()


class S06Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(equal_readings())
        self.wait(5)


class S07Reveal(SpokenScene):
    def construct(self):
        old=equal_readings(); self.add(*old)
        # Clear all labels and both cells before the central cell appears.
        leftovers=VGroup(*[m for i,m in enumerate(old) if i not in (2,7)])
        self.play(FadeOut(leftovers),run_time=.3)
        self.play(old[2].animate.move_to([0,1.65,0]),old[7].animate.move_to([0,1.65,0]).set_opacity(0),run_time=.5)
        self.remove(old[2],old[7])
        fresh=one_cell(.62); self.add(fresh[3])
        self.at('a receptor cell')
        self.play(FadeIn(VGroup(*fresh[:3])),run_time=.35)
        self.at('reports how strongly')
        first=T('A cell reports how strongly it is active,',28).move_to([0,3.3,0])
        self.play(FadeIn(first),run_time=.3)
        self.at('not which molecule',lead=.35)
        self.play(FadeIn(T('not which molecule activated it.',30).move_to([0,-3.15,0])),run_time=.25)
        self.finish()


class S08Vision(SpokenScene):
    def construct(self):
        cone=Polygon([-.75,-2.35,0],[.75,-2.35,0],[.42,1.4,0],[-.42,1.4,0],
                     color=GREY,fill_color=GREY,fill_opacity=.2)
        m=meter(3.8,.1,.02,2.2,3.4)
        self.add(cone,T('cone',30).move_to([0,-2.8,0]),m,
                 T('response',28,GREEN).move_to([3.8,2.28,0]))
        self.at('Vision calls this')
        self.play(FadeIn(heading('univariance')),run_time=.3)
        self.at('a dim light')
        beam=Arrow([-5.5,.9,0],[-.65,.65,0],buff=0,color=GREEN,stroke_width=3)
        lab=T('dim light,\nnear peak',28,GREEN).move_to([-3.6,1.9,0])
        self.play(Create(beam),FadeIn(lab),run_time=.25)
        self.play(Transform(m[1],level(m,.62)),run_time=.3)
        mark_y=level(m,.62).get_top()[1]
        mark=DashedLine([2.55,mark_y,0],[5.05,mark_y,0],color=TEXT,stroke_width=2)
        self.add(mark)
        self.at('a brighter one')
        self.play(FadeOut(beam),FadeOut(lab),Transform(m[1],level(m,.02)),run_time=.15)
        beam2=Arrow([-5.5,.9,0],[-.65,.65,0],buff=0,color=RED,stroke_width=13)
        lab2=T('brighter light,\nfar from peak',28,RED).move_to([-3.6,1.9,0])
        self.play(Create(beam2),FadeIn(lab2),run_time=.2)
        self.play(Transform(m[1],level(m,.62)),run_time=.3)
        self.play(FadeIn(T('same response',28,GREEN).move_to([3.8,-2.35,0])),run_time=.2)
        self.finish()


class S09Line(SpokenScene):
    def construct(self):
        def route(cx,col):
            cells=VGroup(*[receptor_cell(cx+dx,-1.05,col,1.0,3.3) for dx in [-1.2,0,1.2]])
            wires=VGroup(*[Line(c.get_top(),[cx,.95,0],color=col,stroke_width=3) for c in cells])
            channel=Arrow([cx,.95,0],[cx,1.32,0],color=col,buff=0,stroke_width=6)
            brain=chip('brain',GREY,28).move_to([cx,1.65,0])
            return VGroup(cells,wires,channel,brain)
        a=route(-3.2,BLUE); b=route(3.2,PURPLE)
        self.add(a[0])
        self.at('To tell molecules apart')
        h=heading('concentration can vary',YELLOW)
        self.play(FadeIn(h),run_time=.3)
        self.at('more than one line')
        self.play(FadeIn(b[0]),run_time=.4)
        self.at('A line is')
        start=T('A line =',28).move_to([0,3.15,0])
        self.play(ReplacementTransform(h,start),run_time=.3)
        self.at('a set of cells')
        definition=T('A line = a set of cells whose activity\nreaches the brain as one channel.',28,line_spacing=1.1).move_to([0,3.15,0])
        self.play(ReplacementTransform(start,definition),Indicate(a[0],scale_factor=1.03),run_time=.3)
        self.at('activity reaches the brain')
        self.play(Create(a[1]),Create(a[2]),FadeIn(a[3]),run_time=.55)
        self.at('as one channel')
        self.play(Create(b[1]),Create(b[2]),FadeIn(b[3]),
                  FadeIn(T('line 1',28,BLUE).move_to([-3.2,-3,0])),
                  FadeIn(T('line 2',28,PURPLE).move_to([3.2,-3,0])),run_time=.5)
        self.finish()


class S10SmellLine(SpokenScene):
    def construct(self):
        epi=RoundedRectangle(width=11.4,height=1.25,corner_radius=.15,color=GREY,
                             fill_color=GREY,fill_opacity=.15).move_to([0,-1.95,0])
        bulb=RoundedRectangle(width=9.8,height=1.9,corner_radius=.7,color=GREY,
                              fill_color=GREY,fill_opacity=.08).move_to([0,1.25,0])
        xs=[-4.8,-3.25,-1.8,-.4,1.15,2.75,4.4]
        neurons=VGroup(*[receptor_cell(x,-1.95+dy,BLUE,.38,.75) for x,dy in zip(xs,[.1,-.15,.2,0,-.2,.15,-.1])])
        others=VGroup(*[receptor_cell(x,-1.95,PURPLE,.38,.75) for x in [-4.05,-2.55,.4,3.55]])
        gl=VGroup(*[Circle(.4,color=BLUE,fill_color=BLUE,fill_opacity=.4).move_to([x,1.25,0]) for x in [-2.2,2.2]])
        wires=VGroup(*[Line(c.get_top(),gl[0 if i < 4 else 1].get_bottom(),color=BLUE,stroke_width=2.5) for i,c in enumerate(neurons)])
        self.add(epi,neurons,others,bulb,heading('one smell line',BLUE),
                 T('olfactory bulb',28).move_to([0,2.45,0]),
                 T('nose epithelium',28).move_to([-4.15,-3.15,0]))
        self.at('neurons with one receptor')
        self.play(FadeIn(T('same receptor',28,BLUE).move_to([0,-2.95,0])),
                  FadeIn(T('other receptors',26,PURPLE).move_to([4.05,-3.15,0])),run_time=.3)
        self.at('the glomeruli')
        self.play(FadeIn(gl),FadeIn(T('glomeruli',28,BLUE).move_to([0,1.25,0])),
                  FadeIn(T('about two per bulb',26,BLUE).move_to([0,.65,0])),run_time=.3)
        self.at('they converge on')
        self.play(Create(wires),run_time=.6)
        self.finish()


class S11TasteLine(SpokenScene):
    def construct(self):
        bud=RoundedRectangle(width=11.8,height=5.35,corner_radius=1.1,color=GREY,stroke_opacity=.5).move_to([0,-.3,0])
        cells=VGroup(*[receptor_cell(x,-.35,CCOL[k],2.15,3.65) for x,k in zip([-4.25,-1.42,1.42,4.25],CCOL)])
        self.add(bud,cells,heading('one kind of receptor cell = one line'),
                 T('taste bud',28).move_to([0,-3.35,0]))
        self.at('the sweet cells')
        self.play(FadeIn(T('sweet',28,ORANGE).move_to(cells[0])),run_time=.25)
        self.at('the bitter cells')
        self.play(FadeIn(T('bitter',28,PURPLE).move_to(cells[1])),run_time=.25)
        self.at('and so on')
        self.play(FadeIn(T('umami',28,PINK).move_to(cells[2])),FadeIn(T('sour',28).move_to(cells[3])),run_time=.25)
        self.finish()


class S12Pattern(SpokenScene):
    def construct(self):
        values=[.3,.8,.5,.65]
        dots=VGroup(*[Dot([x,0,0],radius=.3,color=GREEN) for x in [-3,-1,1,3]])
        labels=VGroup(*[T(f'line {i+1}',28).move_to([x,-2.6,0]) for i,x in enumerate([-3,-1,1,3])])
        on=T('which lines are on',28).move_to([0,-3.25,0])
        self.add(dots,labels,on,heading('PATTERN',GREEN))
        self.at('relative strength of activity')
        bars=pattern(values,width=8,height=4.25,y=.05,labels=False)
        self.play(ReplacementTransform(dots,bars),Transform(on,T('relative strength across lines',28).move_to(on)),run_time=.55)
        self.at('not just which lines')
        self.play(FadeIn(T('all four are on; their strengths differ',28).move_to([0,2.65,0])),run_time=.3)
        self.finish()


class S13Rule(SpokenScene):
    def construct(self):
        rule=T('A chemical sense can tell two stimuli apart only if\nthey produce different patterns of activity\nacross its separate lines.',26,line_spacing=1.05).move_to([0,2.85,0])
        box=SurroundingRectangle(rule,color=GOLD,buff=.18)
        vals=[[.3,.8,.5,.65],[.3,.8,.5,.65],[.3,.8,.5,.65],[.7,.3,.8,.4]]
        bars=VGroup(*[pattern(v,x=x,y=-.45,width=2.35,height=3.4,labels=False) for x,v in zip([-4.6,-1.65,1.65,4.6],vals)])
        names=VGroup(*[T(f'stimulus {i+1}',26).move_to([x,1.55,0]) for i,x in enumerate([-4.6,-1.65,1.65,4.6])])
        self.add(bars,names)
        self.at('The rule')
        self.play(FadeIn(rule),Create(box),run_time=.35)
        self.at('can tell two stimuli apart')
        self.play(FadeIn(T('no distinction\nin this model',28,RED).move_to([-3.125,-2.95,0])),run_time=.3)
        self.at('only if their patterns')
        self.play(FadeIn(T('can differ in principle;\ntest behaviour',26,GREEN).move_to([3.125,-2.95,0])),run_time=.3)
        self.at('separate lines differ')
        self.play(Indicate(bars[3],scale_factor=1.02),run_time=.35)
        self.finish()


class S14Smell(SpokenScene):
    def construct(self):
        sm=split_smell(); self.add(*sm[:3],taste_outline())
        self.at('Smell keeps')
        self.play(LaggedStart(*[Indicate(line,scale_factor=1.02) for line in sm[1][2]],lag_ratio=.08),run_time=.6)
        self.at('So an')
        self.play(FadeIn(sm[3]),run_time=.5)
        self.at('a pattern across')
        self.play(Indicate(sm[3][0],scale_factor=1.02),run_time=.4)
        self.finish()


class S15Bitter(SpokenScene):
    def construct(self):
        self.add(split_smell()); outline=taste_outline(); self.add(outline)
        bp=bitter_panel()
        self.at('Taste pools its receptors')
        self.play(FadeOut(outline),FadeIn(VGroup(*bp[:5])),run_time=.45)
        self.at('a few kinds of cell')
        self.play(FadeIn(bp[7]),run_time=.4)
        self.at('So a taste')
        self.play(Create(bp[5]),FadeIn(bp[6]),run_time=.4)
        self.at('which kind of cell is active')
        self.play(bp[1].animate.set_fill(PURPLE,.4),Indicate(bp[5],scale_factor=1.02),run_time=.4)
        self.finish()


class S16Labeled(SpokenScene):
    def construct(self):
        self.add(split_smell())
        bp=bitter_panel(False); self.add(bp)
        tag=chip('BITTER',PURPLE,28).move_to([3.35,-1.75,0])
        self.at('A line whose activity')
        self.play(bp[1].animate.set_fill(PURPLE,.4),Indicate(bp[5],scale_factor=1.01),run_time=.3)
        self.at('always means one quality')
        self.play(FadeIn(tag),FadeIn(T('in mice',26).move_to([3.35,-2.4,0])),run_time=.3)
        self.at('whatever turned it on')
        self.play(bp[1].animate.set_fill(PURPLE,.14),run_time=.15)
        # Two distinct receptor cartoons activate the same cell and output.
        self.play(bp[2][0].animate.set_fill(YELLOW,1),bp[1].animate.set_fill(PURPLE,.4),
                  bp[5].animate.set_color(GREEN),run_time=.25)
        self.play(bp[2][0].animate.set_fill(PURPLE,.7),bp[1].animate.set_fill(PURPLE,.14),bp[5].animate.set_color(PURPLE),run_time=.15)
        self.play(bp[2][2].animate.set_fill(YELLOW,1),bp[1].animate.set_fill(PURPLE,.4),bp[5].animate.set_color(GREEN),run_time=.25)
        self.at('is called a labeled line')
        self.play(FadeIn(T('labeled line',30,PURPLE).move_to([3.35,-3.15,0])),run_time=.3)
        self.finish()


class S17Scope(SpokenScene):
    def construct(self):
        self.add(RoundedRectangle(width=11.2,height=5.5,corner_radius=.3,color=GREY),heading('Scope of the rule'))
        per=T('periphery',38,BLUE).move_to([0,1.45,0])
        self.at('Keep the scope')
        self.play(FadeIn(per),run_time=.3)
        self.at('about the periphery')
        self.play(Indicate(per,scale_factor=1.02),run_time=.25)
        self.at('mostly in mice')
        self.play(FadeIn(T('mostly mice',38).move_to([0,0,0])),run_time=.25)
        self.at('ignores spike timing',lead=.35)
        self.play(FadeIn(T('spike timing left out',36).move_to([0,-1.55,0])),run_time=.15)
        self.finish()


class S18Takeaway(SpokenScene):
    def construct(self):
        sm=split_smell(); bp=bitter_panel(False)
        self.add(sm[0],sm[1],sm[3],VGroup(*bp[:7]))
        # Keep the takeaway labels above the bars and directly below each output.
        sm[1].stretch_to_fit_height(4.4).move_to([-3.45,.2,0])
        bp[5].put_start_and_end_on([3.35,-.85,0],[3.35,-2.1,0])
        self.remove(sm[3]); sm[3][0].shift(DOWN*.2)
        msg=T('Gene count alone does not set the number of lines.',28).move_to([0,-3.25,0])
        self.at('Gene count alone')
        self.play(FadeIn(msg),run_time=.3)
        self.at('What matters is whether',lead=.4)
        self.play(FadeOut(msg),run_time=.15)
        self.play(FadeIn(sm[3][0]),FadeIn(T('separate lines',30,TEXT).move_to([-3.45,-2.55,0])),
                  FadeIn(T('pooled into a few cells',30,TEXT).move_to([3.35,-2.55,0])),run_time=.2)
        self.at('receptor identity')
        self.play(Indicate(sm[1][2],scale_factor=1.015),run_time=.4)
        self.at('kept separate')
        self.play(Indicate(sm[1][2],scale_factor=1.015),run_time=.3)
        self.at('or pooled')
        self.play(bp[1].animate.set_fill(PURPLE,.4),run_time=.3)
        self.finish()


class S19End(EndCard):
    LINE='Smell keeps receptor lines separate; taste pools them into a few.'
    def construct(self):
        lines=VGroup(T('Smell keeps receptor lines separate;',36,BLUE,font=TITLE_FONT),
                     T('taste pools them into a few.',36,PURPLE,font=TITLE_FONT)).arrange(DOWN,buff=.25).move_to([0,.4,0])
        self.play(FadeIn(lines),run_time=.4)
        self.play(FadeIn(T('biochemistrypedia.com',28,TEXT).move_to([0,-1.25,0])),run_time=.3)
        self.finish()
