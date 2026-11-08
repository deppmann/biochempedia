"""Choosing a Partner, chapter 1: Same Means Stick.

COLOR MAP: YELLOW Sidekick-1; BLUE Sidekick-2; PURPLE Dscam;
PINK DscamL; ORANGE bipolar cells; TEAL amacrine cells / gradient;
GREEN adhesion / ganglion cells; RED wrong partners / missing protein;
GREY neutral anatomy; TEXT explanations. All proteins are schematic chips.
"""
import numpy as np
from bp_style import *

PURPLE = '#A78BFA'
PINK = '#FF8CBA'
ORANGE = '#F29E4C'
BX0, BX1 = -6.0, 6.0
BH = 1.2
BY = [2.4, 1.2, 0, -1.2, -2.4]
TOPY, BOTY, CR = 3.0, -3.0, .29


def label(text, x=0, y=3.55, color=TEXT, size=30):
    return T(text, size, color).move_to([x, y, 0])


def plate(m):
    bg = Rectangle(width=m.width+.25, height=m.height+.12,
                   fill_color=BG, fill_opacity=1, stroke_width=0).move_to(m)
    return VGroup(bg, m)


def band(i, color=GREY, op=.09):
    return Rectangle(width=12, height=BH, stroke_color=color, stroke_width=1.5,
                     fill_color=color, fill_opacity=op).move_to([0, BY[i], 0])


def stack(colored=False):
    cols = [TEAL, YELLOW, PURPLE, BLUE, PINK] if colored else [GREY]*5
    return VGroup(*[band(i, c) for i, c in enumerate(cols)])


def lab(name, color, i):
    return plate(label(name, -4.65, BY[i], color, 28))


def cell(x, color=TEXT, y=TOPY):
    return Circle(CR, stroke_color=color, stroke_width=4,
                  fill_color=color, fill_opacity=.28).move_to([x, y, 0])


def proc(x, indices, color=TEXT, w=.65, up=False, soma_y=None):
    start = (BOTY+CR if up else TOPY-CR) if soma_y is None else soma_y
    ys = [BY[i]+(.12 if not up else -.12) for i in indices]
    stem = Line([x,start,0], [x,ys[-1],0], color=color, stroke_width=5)
    arbor = VGroup(*[Line([x-w,y,0],[x+w,y,0],color=color,stroke_width=6) for y in ys])
    ticks = VGroup(*[Line([x+dx,y,0],[x+dx,y+(.22 if up else -.22),0],color=color,stroke_width=4)
                      for y in ys for dx in np.linspace(-w*.8,w*.8,4)])
    return VGroup(stem, arbor, ticks)


def cross(x,y,s=.4):
    return VGroup(*[Line([x-s,y+q*s,0],[x+s,y-q*s,0], color=RED,stroke_width=8) for q in [-1,1]])


def arrow(a,b,color=TEXT):
    return Arrow(a,b,buff=.05,color=color,stroke_width=5,tip_length=.18)


def recolor(c,p,col):
    return [c.animate.set_stroke(col).set_fill(col,.3), p.animate.set_color(col)]


class S00Title(TitleCard):
    LESSON = 'Choosing a Partner: Layers, Self-Avoidance and Smell'
    TITLE = 'Same Means Stick'
    def construct(self):
        self.add(label('BIOCHEMISTRYPEDIA', y=2.65, color=TEAL, size=28),
                 label('Choosing a Partner', y=1.5, size=36),
                 T(self.TITLE, font=TITLE_FONT, size=68).move_to([0,0,0]),
                 Line([-2,-1,0],[2,-1,0],color=GOLD,stroke_width=5),
                 label('Layers, Self-Avoidance and Smell',y=-2.15,size=30))
        self.finish()


class S01Q(SpokenScene):
    def construct(self):
        bs=stack(True)
        q=label('Which thin layer should a branch stop in?',size=38)
        cs=VGroup(*[cell(x) for x in [-2.4,.6,3.6]])
        ps=[proc(x,[i]) for x,i in zip([-2.4,.6,3.6],[1,3,4])]
        self.add(bs,q,cs,label('retina cross-section',y=-3.55,size=28))
        self.at('growing branch')
        self.play(*[Create(p) for p in ps],run_time=1.1)
        self.at('which thin layer')
        self.play(*[FadeIn(label('?',x+.95,BY[i],size=42)) for x,i in zip([-2.4,.6,3.6],[1,3,4])],run_time=.4)
        self.finish()


class S02Gradient(SpokenScene):
    def construct(self):
        strips=VGroup(*[Rectangle(width=11.5,height=.29,stroke_width=0,fill_color=TEAL,
                       fill_opacity=.04+.5*k/19).move_to([0,2.6-.29*k,0]) for k in range(20)])
        cs=VGroup(*[cell(x) for x in [-2.5,0,2.5]])
        ps=VGroup(*[Line([x,TOPY-CR,0],[x,-.5,0],color=TEXT,stroke_width=5) for x in [-2.5,0,2.5]])
        head=label('a gradient brings axons near a target',color=TEAL,size=32)
        self.add(strips,cs,head)
        self.at('bring an axon')
        self.play(Create(ps),run_time=.7)
        region=Rectangle(width=8.8,height=1.0,color=TEXT,stroke_width=3).move_to([0,-.5,0])
        self.at('near its target')
        self.play(Create(region),run_time=.35)
        self.at('but a thin layer')
        bs=stack()
        mini=bs.copy().scale(.16).move_to(region)
        self.play(FadeOut(strips),FadeOut(cs),FadeOut(ps),FadeIn(mini),run_time=.2)
        self.play(ReplacementTransform(mini,bs),FadeOut(region),
                  Transform(head,label('a thin layer is a discrete choice',size=36)),run_time=.5)
        self.at('either the right')
        self.play(bs[1].animate.set_stroke(YELLOW,width=5).set_fill(YELLOW,.35),
                  FadeIn(lab('right layer',YELLOW,1)),run_time=.3)
        self.finish()


class S03Discrete(SpokenScene):
    def construct(self):
        bs=stack(True)
        self.add(bs,label('discrete choices',size=40))
        tags=VGroup(*[RoundedRectangle(width=.6,height=.45,corner_radius=.08,
                     color=c,fill_color=c,fill_opacity=.6).move_to([-4.9,BY[i],0])
                     for i,c in enumerate([TEAL,YELLOW,PURPLE,BLUE,PINK])])
        self.at('discrete labels')
        self.play(FadeIn(tags),FadeIn(label('discrete labels',y=-3.55,size=36)),run_time=.3)
        self.finish()


# Shared anatomy: separate horizontal territories keep arbors legible.
def anatomy():
    xs=[-3.1,0,3.1]; colors=[ORANGE,TEAL,GREEN]
    cs=VGroup(cell(xs[0],colors[0]),cell(xs[1],colors[1]),cell(xs[2],colors[2],BOTY))
    ps=VGroup(proc(xs[0],[1],colors[0],w=1.0),proc(xs[1],[1,3],colors[1],w=1.0),
              proc(xs[2],[3],colors[2],w=1.0,up=True))
    names=VGroup(label('bipolar',xs[0],3.55,colors[0],28),
                 label('amacrine',xs[1],3.55,colors[1],28),
                 label('retinal ganglion',xs[2],-3.55,colors[2],28))
    return cs,ps,names


class S04Ipl(SpokenScene):
    def construct(self):
        blk=Rectangle(width=12,height=6.0,color=GREY,fill_color=GREY,fill_opacity=.09)
        cs,ps,names=anatomy()
        self.add(blk,cs,ps,names,plate(label('inner plexiform layer',0,-2.5,size=30)))
        self.at('three kinds of cell')
        self.play(*[Indicate(c,color=col,scale_factor=1.15) for c,col in zip(cs,[ORANGE,TEAL,GREEN])],run_time=.5)
        self.at('make synapses')
        # All three coloured arbors meet in one common IPL band.
        green=proc(3.1,[2],GREEN,w=1.9,up=True)
        green[0].put_start_and_end_on([3.1,BOTY+CR,0],[3.1,.12,0])
        green[1:].shift(UP*.24)
        target=VGroup(proc(-3.1,[2],ORANGE,w=1.9),
                      proc(0,[2],TEAL,w=1.2),green)
        self.play(Transform(ps,target),run_time=.4)
        contacts=VGroup(*[Circle(.17,color=GOLD,stroke_width=5).move_to([x,.12,0])
                         for x in [-1.2,1.2]])
        self.play(FadeIn(contacts),run_time=.15)
        self.finish()


class S05Subl(SpokenScene):
    def construct(self):
        bs=stack(True);cs,ps,names=anatomy()
        self.add(bs,cs,ps,names)
        self.at('divided into thinner')
        self.play(Indicate(bs,color=TEXT,scale_factor=1.02),run_time=.5)
        self.at('each cell type')
        self.play(*[Indicate(p[1],color=c,scale_factor=1.1) for p,c in zip(ps,[ORANGE,TEAL,GREEN])],run_time=.7)
        # A distinct wrong-band example stays in the bipolar cell's territory.
        ghost=VGroup(DashedLine([-3.1,BY[1],0],[-3.1,BY[4]+.12,0],color=ORANGE,stroke_width=4),
                     DashedLine([-4.1,BY[4]+.12,0],[-2.1,BY[4]+.12,0],color=ORANGE,stroke_width=4))
        partner=Line([-2.1,BY[4]+.12,0],[-1.3,BY[4]+.12,0],color=PINK,stroke_width=7)
        self.at('one or a few')
        self.play(Create(ghost),Create(partner),FadeIn(cross(-2.1,BY[4]+.12)),
                  FadeIn(plate(label('wrong band: wrong partners',-2.7,-3.55,RED,28))),run_time=.6)
        self.finish()


def groups(colored=True):
    xs=[-2.8,-1.5,1.5,2.8]
    cols=[YELLOW,YELLOW,BLUE,BLUE] if colored else [TEXT]*4
    cs=VGroup(*[cell(x,c) for x,c in zip(xs,cols)])
    ps=VGroup(*[proc(x,[1 if i<2 else 3],c,w=.5) for i,(x,c) in enumerate(zip(xs,cols))])
    return cs,ps


class S06Sdk(SpokenScene):
    def construct(self):
        cs,ps=groups(False)
        self.add(stack(),cs,ps,label('chick retina',y=-3.55,size=30))
        self.at('two related proteins')
        self.play(FadeIn(label('two related cell-surface proteins',y=3.55,size=28)),run_time=.3)
        self.at('sidekick1')
        self.play(FadeIn(lab('Sidekick-1',YELLOW,1)),*[a for c,p in zip(cs[:2],ps[:2]) for a in recolor(c,p,YELLOW)],run_time=.35)
        self.at('sidekick2')
        self.play(FadeIn(lab('Sidekick-2',BLUE,3)),*[a for c,p in zip(cs[2:],ps[2:]) for a in recolor(c,p,BLUE)],run_time=.35)
        self.finish()


class S07Groups(SpokenScene):
    def construct(self):
        bs=stack();cs,ps=groups()
        self.add(bs,cs,ps,lab('Sidekick-1',YELLOW,1),lab('Sidekick-2',BLUE,3),label('chick retina',y=3.55))
        self.at('largely separate groups')
        self.play(Indicate(cs[:2],color=YELLOW),Indicate(cs[2:],color=BLUE),run_time=.7)
        self.at('end in different')
        self.play(bs[1].animate.set_stroke(YELLOW).set_fill(YELLOW,.2),
                  bs[3].animate.set_stroke(BLUE).set_fill(BLUE,.2),run_time=.6)
        self.finish()


# Schematic membrane-bound receptors: labelled blocks, never molecular structures.
def facing_membranes(gap):
    return VGroup(*[RoundedRectangle(width=11,height=.65,corner_radius=.18,color=GREY,
                fill_color=GREY,fill_opacity=.25).move_to([0,s*gap,0]) for s in [1,-1]])


def receptor(x,y,col,down=True):
    d=-1 if down else 1
    stem=Line([x,y,0],[x,y+d*1.3,0],color=col,stroke_width=8)
    head=RoundedRectangle(width=.8,height=.42,corner_radius=.12,color=col,
                          fill_color=col,fill_opacity=.6).move_to([x,y+d*1.4,0])
    return VGroup(stem,head)


class S08Homo(SpokenScene):
    def construct(self):
        mem=facing_membranes(2.35)
        r1=receptor(-1.5,2.03,YELLOW);r2=receptor(-1.5,-2.03,YELLOW,False)
        blue=receptor(3,-2.03,BLUE,False)
        self.add(mem,r1,r2,blue,label('homophilic binding',size=42),
                 label('Sidekick-1',-2.8,-3.2,YELLOW,30),label('Sidekick-2',3,-3.2,BLUE,30),
                 label('cell membrane',3.4,2.9,GREY,28))
        self.at('binds its own kind')
        self.play(mem[0].animate.shift(DOWN*.4),mem[1].animate.shift(UP*.4),
                  r1.animate.shift(DOWN*.4),r2.animate.shift(UP*.4),blue.animate.shift(UP*.4),run_time=.7)
        lock=RoundedRectangle(width=1.2,height=.8,corner_radius=.15,color=GREEN,stroke_width=6).move_to([-1.5,0,0])
        self.play(Create(lock),run_time=.25)
        self.at('which is called')
        self.play(blue.animate.shift(LEFT*1.5),run_time=.6)
        self.add(label('match → hold',-2.2,-2.65,GREEN,30), label('no matching contact',2.7,-2.65,BLUE,28))
        self.finish()


class S09Stick(SpokenScene):
    def construct(self):
        # Reuse the preceding membrane/receptor close-up, now on cell processes.
        mem=facing_membranes(2.25).set_stroke(YELLOW).set_fill(YELLOW,.18)
        r1=receptor(-1.5,1.93,YELLOW)
        r2=receptor(-1.5,-1.93,YELLOW,False)
        upper=VGroup(mem[0],r1)
        lower=VGroup(mem[1],r2)
        # Continuations and small branches identify the membranes as processes.
        branches=VGroup(*[Line([x,y,0],[x+.5,y+d*.55,0],color=YELLOW,stroke_width=5)
                         for x,y,d in [(-4.7,2.575,1),(4.4,2.575,1),(-4.7,-2.575,-1)]])
        upper.add(*branches[:2]);lower.add(branches[2])
        blue_mem=RoundedRectangle(width=2.8,height=.5,corner_radius=.18,color=BLUE,
                                 fill_color=BLUE,fill_opacity=.25).move_to([3.5,-1,0])
        blue_rec=receptor(3.5,-.75,BLUE,False).scale(.45,about_point=[3.5,-.75,0])
        passing=VGroup(blue_mem,blue_rec,label('Sidekick-2',3.5,.25,BLUE,28))
        self.add(upper,lower,passing,
                 label('Sidekick-1',0,3.55,YELLOW,34),
                 label('Sidekick-1',0,-3.55,YELLOW,34),
                 plate(label('cell processes',3.5,2.25,GREY,28)))
        self.at('sidekick 1')
        self.play(upper.animate.shift(DOWN*.32),lower.animate.shift(UP*.32),run_time=.5)
        lock=RoundedRectangle(width=1.2,height=.85,corner_radius=.15,color=GREEN,
                              fill_color=GREEN,fill_opacity=.18,stroke_width=7).move_to([-1.5,0,0])
        self.at('sticks to')
        self.play(FadeIn(lock),passing.animate.shift(LEFT*1.5),run_time=.3)
        self.add(label('hold together',-4,0,GREEN,30),
                 label('no contact',3.7,.8,BLUE,28))
        self.finish()


NX=3.7

def mis_state(added=False,shifted=False):
    bs=stack();bs[1].set_stroke(YELLOW).set_fill(YELLOW,.18);bs[3].set_stroke(BLUE).set_fill(BLUE,.15)
    cs=VGroup(cell(-2.3,YELLOW),cell(.6,BLUE),cell(NX,YELLOW if added else TEXT))
    ps=VGroup(proc(-2.3,[1],YELLOW),proc(.6,[3],BLUE),proc(NX,[4],YELLOW if added else TEXT))
    if shifted:
        # Shift in distribution: a new branch approaches the matching band;
        # some of the old arbor remains. No travel through an unrelated band.
        ps[2]=VGroup(proc(NX,[4],YELLOW).set_opacity(.35),proc(NX,[1],YELLOW,w=.9))
    return VGroup(bs,cs,ps,lab('Sidekick-1',YELLOW,1),lab('Sidekick-2',BLUE,3))


def prediction():
    return VGroup(label('Predict',-4.7,3.55,GOLD,36),label('+ Sidekick-1',NX,3.55,YELLOW,28),
                  label('Where should their processes end?',y=-3.55,size=34),label('?',5.1,BY[4],size=44))


class S10Mark(SpokenScene):
    def construct(self):
        d=mis_state()
        self.add(d,label('Marks the band, or helps choose it?',y=-3.55,size=36),label('What does the label do?',size=36))
        self.at('mark the band')
        self.play(Indicate(d[0][1],color=YELLOW),run_time=.6)
        self.at('help choose it')
        self.play(Indicate(d[2][2],color=TEXT),run_time=.6)
        self.finish()


class S11Predict(SpokenScene):
    def construct(self):
        d=mis_state();bits=prediction()
        no=label('no Sidekick',NX,3.55,TEXT,28)
        self.add(d,bits[0],no)
        self.at('make neurons produce')
        self.play(Indicate(d[1][2],color=TEXT),run_time=.4)
        self.at('a sidekick')
        self.play(ReplacementTransform(no,bits[1]),*recolor(d[1][2],d[2][2],YELLOW),run_time=.5)
        self.at('where should')
        self.add(bits[2],bits[3])
        self.finish()


class S12Pause(NarratedScene):
    def construct(self):
        self.add(mis_state(True),prediction())
        n=label('Think: 5',0,3.55,GOLD,28)
        self.add(n)
        for i in range(5,0,-1):
            n.become(label(f'Think: {i}',0,3.55,GOLD,28))
            self.wait(1)
        self.finish()


class S13Reveal(SpokenScene):
    def construct(self):
        d=mis_state(True)
        self.add(d,label('misexpression: + Sidekick-1',y=3.55,size=32),
                 label('Yamagata, Weiner and Sanes, 2002',y=-3.55,size=28))
        old=d[2][2]
        ghost=proc(NX,[4],GREY).set_opacity(.5)
        self.add(ghost)
        self.at('shifted toward')
        # Crossfade distributions; do not animate an arbor crossing the blue band.
        new=proc(NX,[1],YELLOW,w=.9)
        self.play(old.animate.set_opacity(.35),FadeIn(new),run_time=.65)
        self.add(plate(label('shift toward the matching band',0,-2.65,YELLOW,28)))
        self.at('already concentrated')
        self.play(Indicate(d[0][1],color=YELLOW,scale_factor=1.02),run_time=.6)
        self.finish()


def moved():
    return VGroup(mis_state(True,True),label('+ Sidekick-1',NX,3.55,YELLOW,28),
                  label('add the label → shift the arbor',y=-3.55,size=36))


class S14Moved(SpokenScene):
    def construct(self):
        d=moved();self.add(d)
        self.at('adding the label')
        self.play(Indicate(d[1],color=YELLOW),run_time=.4)
        self.at('shifted the arbor')
        self.play(Indicate(d[0][2][2][1][1],color=YELLOW),run_time=.4)
        self.finish()


class S15Beat(NarratedScene):
    def construct(self):
        self.add(moved());self.finish()


# Four independent mini-panels avoid asserting an anatomical layer order.
def family_panel(x,y,name,col):
    box=RoundedRectangle(width=5.6,height=2.6,corner_radius=.16,color=GREY,stroke_width=1.5).move_to([x,y,0])
    zone=Rectangle(width=4.8,height=.55,color=col,fill_color=col,fill_opacity=.18).move_to([x,y-.55,0])
    c=cell(x,col,y+.25)
    stem=Line([x,y-.04,0],[x,y-.55,0],color=col,stroke_width=5)
    arb=Line([x-1.2,y-.55,0],[x+1.2,y-.55,0],color=col,stroke_width=6)
    return VGroup(box,zone,c,stem,arb,label(name,x,y+.95,col,30))


class S16Four(SpokenScene):
    def construct(self):
        a=family_panel(-3,1.55,'Sidekick-1',YELLOW);b=family_panel(3,1.55,'Sidekick-2',BLUE)
        c=family_panel(-3,-1.3,'Dscam',PURPLE);d=family_panel(3,-1.3,'DscamL',PINK)
        self.add(a,b,label('schematic groups; no anatomical layer order',y=-3.55,size=28))
        self.at('yamagata')
        self.add(label('Yamagata and Sanes, 2008',y=3.55,size=28))
        self.at('added')
        self.play(FadeIn(c),run_time=.35)
        # Transcript joins the second protein's spelling; cue its plain conjunction.
        self.at('and dscam')
        self.play(FadeIn(d),run_time=.35)
        self.at('making four labels')
        self.play(Indicate(VGroup(a[5],b[5],c[5],d[5]),color=TEXT,scale_factor=1.03),run_time=.5)
        self.finish()


class S17Scope(SpokenScene):
    def construct(self):
        bs=stack();bs[1].set_stroke(YELLOW).set_fill(YELLOW,.2)
        c=cell(.4);p=proc(.4,[1],YELLOW,w=1.2)
        pull=arrow([2.8,2.4,0],[1.1,BY[1]+.12,0],YELLOW)
        self.add(bs,c,lab('Sidekick-1',YELLOW,1),label('one part of how layers form',size=34),
                 label('not an address book',y=-3.55,size=32))
        self.at('a choice')
        self.add(plate(label('a bias',3.8,2.4,YELLOW,38)))
        self.play(Create(p),Create(pull),run_time=.5)
        self.at('one part')
        cues=VGroup(arrow([-3.5,2.4,0],[-.9,BY[1]+.12,0],TEAL),
                    plate(label('other cues',-3.8,2.4,TEAL,28)))
        self.play(FadeIn(cues),run_time=.4)
        self.finish()


class S18Mouse(SpokenScene):
    def construct(self):
        bs=stack()
        self.add(bs,label('mouse retina',-4.7,3.55,size=28),
                 label('still reach the right sublaminae',y=-3.55,size=34))
        ca=cell(-1.8,RED);cb=cell(2.5,RED)
        # Neutral outlines establish the normal target before either arbor arrives.
        targets=VGroup(*[DashedVMobject(Rectangle(width=2.8,height=BH*.8,color=TEXT,
                              stroke_width=3).move_to([x,BY[i],0]),num_dashes=24)
                        for x,i in [(-1.8,2),(2.5,0)]])
        self.add(targets,plate(label('normal band',-4.5,BY[2],size=28)),
                 plate(label('normal band',4.8,BY[0],size=28)))
        self.at('cells lacking')
        self.add(ca,cb,label('no DSCAM',-1.8,3.55,RED,28),label('no DSCAML1',2.5,3.55,RED,28))
        pa=proc(-1.8,[2],TEXT,w=1.1);pb=proc(2.5,[0],TEXT,w=1.1)
        self.at('still reach')
        self.play(Create(pa),Create(pb),run_time=.55)
        self.finish()


# Idea card: one consistent font size; future lines are absent until spoken.
def idea_lines():
    return [label('A match says only: we are the same.',y=2.95,size=32),
            label('The cell decides what same means.',y=2.2,size=32),
            label('A shared sticky label draws like processes together.',y=1.45,size=32)]


def match_picture(joined=False):
    cs=VGroup(*[Circle(1.25,color=GREY,fill_color=GREY,fill_opacity=.2).move_to([x,-.8,0]) for x in [-4.7,4.7]])
    r=.3 if joined else 1.4
    arms=VGroup(Line([-3.45,-.8,0],[-r,-.8,0],color=TEXT,stroke_width=9),
                Line([3.45,-.8,0],[r,-.8,0],color=TEXT,stroke_width=9))
    heads=VGroup(*[RoundedRectangle(width=.6,height=.8,corner_radius=.1,color=TEXT,fill_color=TEXT,
                  fill_opacity=.35).move_to([x,-.8,0]) for x in [-r,r]])
    return VGroup(cs,arms,heads)


class S19Idea2(SpokenScene):
    def construct(self):
        lines=idea_lines();pic=match_picture()
        self.add(lines[0],pic,label('the idea to carry through this lesson',y=-3.55,color=GOLD,size=30))
        self.at('match between identical')
        self.play(Transform(pic,match_picture(True)),run_time=.8)
        self.at('we are the same')
        self.play(Indicate(pic[2],color=TEXT,scale_factor=1.1),run_time=.5)
        self.finish()


class S20Idea3(SpokenScene):
    def construct(self):
        lines=idea_lines();pic=match_picture(True)
        self.add(lines[0],pic)
        self.at('the cell decides')
        self.add(lines[1])
        self.play(Indicate(pic[0],color=TEXT),run_time=.5)
        self.finish()


def convergence(spread=True,by=-2.15,cy=.65):
    xs=[-3.8,0,3.8]; ends=[-4.4,0,4.4] if spread else [-.9,0,.9]
    cs=VGroup(*[cell(x,YELLOW,cy) for x in xs])
    ps=VGroup()
    for x,end in zip(xs,ends):
        stem=Line([x,cy-CR,0],[end,by,0],color=YELLOW,stroke_width=5)
        arb=Line([end-1.0,by,0],[end+1.0,by,0],color=YELLOW,stroke_width=7)
        ps.add(VGroup(stem,arb))
    zone=Rectangle(width=12,height=.85,color=YELLOW,fill_color=YELLOW,fill_opacity=.13).move_to([0,by,0])
    return VGroup(zone,cs,ps)


class S21Idea4(SpokenScene):
    def construct(self):
        ls=idea_lines();pic=convergence()
        self.add(ls[0],ls[1],pic)
        self.at('shares a sticky label')
        self.add(label('shared sticky label',y=-3.55,color=YELLOW,size=30))
        self.at('their processes')
        self.add(ls[2])
        self.at('drawn together')
        self.play(Transform(pic,convergence(False)),run_time=.85)
        self.finish()


class S22Next(SpokenScene):
    def construct(self):
        sm=label('same means',-2.7,.6,size=54)
        st=label('stick',2,.6,size=54)
        ring=Ellipse(width=st.width+.7,height=st.height+.7,color=GOLD,stroke_width=5).move_to(st)
        self.add(sm)
        self.at('stick')
        self.add(st,ring,label('retreat',y=-1.5,color=GREY,size=40),
                 label('(the next lesson)',y=-2.4,color=GREY,size=28))
        self.finish()


TAKE='In chick retina, shared sticky labels help\nlike processes settle in matching sublaminae,\nalongside other cues.'


class S23Take(SpokenScene):
    def construct(self):
        pic=convergence(True,by=.5,cy=2.25)
        self.add(pic,label('Takeaway',y=3.55,color=GOLD,size=36))
        # The full scoped claim is readable before the narration ends.
        text=T(TAKE,size=32,line_spacing=1.25).move_to([0,-2,0])
        self.at('in chick retina')
        self.add(text)
        self.at('like processes')
        self.play(Transform(pic,convergence(False,by=.5,cy=2.25)),run_time=.8)
        self.finish()


class S24End(EndCard):
    LINE=TAKE
    def construct(self):
        line=T(self.LINE,font=TITLE_FONT,size=38,line_spacing=1.5).move_to([0,.5,0])
        self.add(line,label('biochemistrypedia.com',y=-2.6,color=TEAL,size=28),
                 Line([-2,2.5,0],[2,2.5,0],color=GOLD,stroke_width=4))
        self.finish()
