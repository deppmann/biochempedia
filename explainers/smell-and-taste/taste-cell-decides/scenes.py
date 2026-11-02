"""Taste: The Cell Decides — review redraw.
COLOR MAP: BLUE smell/receptors; YELLOW ligands/ATP; GREEN response;
RED deletion/loss; TEAL shared PLCβ2; ORANGE sweet; PINK umami;
PURPLE bitter; TEXT labels/sour/salty; GREY inactive structure.
All traces come from the explicitly schematic stimulus/rate model below.
No molecular structures; final narration and word timings are unchanged.
"""
from bp_style import *
import numpy as np

ORANGE, PINK, PURPLE = '#F29E4C', '#E88FB4', '#B58CE8'
KINDS = ['sweet', 'umami', 'bitter']
COL = dict(sweet=ORANGE, umami=PINK, bitter=PURPLE, sour=TEXT, salty=TEXT)
XS = [-4.1, 0, 4.1]


class Indicate(Indicate):
    """Pulse outlines without painting chip backgrounds over their text."""
    def __init__(self,mobject,scale_factor=1.06,color=YELLOW,**kwargs):
        super().__init__(mobject,scale_factor=scale_factor,color=color,**kwargs)

    def create_target(self):
        target=self.mobject.copy().scale(self.scale_factor)
        for source,dest in zip(self.mobject.get_family(),target.get_family()):
            if isinstance(source,VMobject) and source.get_stroke_width()>0:
                dest.set_stroke(self.color,family=False)
        return target

# Keep synchronization logs among temporary render artifacts, not deliverables.
_BaseSpokenScene = SpokenScene
class SpokenScene(_BaseSpokenScene):
    def at(self, phrase, lead=.2, nth=0):
        target = self.t_of(phrase, nth) - lead
        rest = target - self.elapsed()
        with open('/tmp/taste-cell-fix-sync.log', 'a') as f:
            f.write(f'{os.environ.get("KX_SCENE_ID")} {phrase}: late={max(0,-rest):.2f}\n')
        if rest > .02: self.wait(rest)


def label(s, x=0, y=3.25, size=32, color=TEXT):
    return T(s, size, color).move_to([x,y,0])


def block(s, x, y, color=BLUE, size=26):
    g=chip(s,color,size,pad=.12)
    g[0].set_fill(BG,1)
    return g.move_to([x,y,0])


def cell(k,x=0,y=.15,h=4.5,active=False,name=True):
    # One silhouette, always the same aspect ratio, including the zoomed views.
    body=RoundedRectangle(width=h*.63,height=h,corner_radius=h*.15,
        stroke_color=COL[k],stroke_width=3.5,fill_color=COL[k],
        fill_opacity=.28 if active else .025).move_to([x,y,0])
    g=VGroup(body)
    if name:g.add(label(k.upper(),x,y-h/2-.34,26,COL[k]))
    return g


def cells(active=False):
    return VGroup(*[cell(k,x,active=active) for k,x in zip(KINDS,XS)])


def xmark(p,s=.32):
    p=np.array(p)
    return VGroup(*[Line(p+[-s,v*s,0],p+[s,-v*s,0],color=RED,stroke_width=5) for v in [-1,1]])


def receptors(k,x):
    names={'sweet':['T1R2','T1R3'],'umami':['T1R1','T1R3'],
           'bitter':['T2R A','T2R B','T2R C']}[k]
    return VGroup(*[block(n,x,1.45-i*.95) for i,n in enumerate(names)])


def chain(x,gloss=False):
    names=['PLCβ2','IP3R3','TRPM5','CALHM1/3']
    words=['enzyme','calcium release','ion channel','ATP exit']
    ys=[1.95,.65,-.65,-1.95] if gloss else [1.7,.65,-.4,-1.45]
    nodes=VGroup(*[block(n,x,y,TEAL if i==0 else GREY) for i,(n,y) in enumerate(zip(names,ys))])
    notes=VGroup(*[label(w,x,y-.49,22,TEXT) for w,y in zip(words,ys)]) if gloss else VGroup()
    links=VGroup(*[Arrow([x,y-(.76 if gloss else .34),0],[x,y-(1.0 if gloss else .73),0],buff=0,color=GREY,stroke_width=2,
        max_tip_length_to_length_ratio=.4) for y in ys[:-1]])
    return VGroup(nodes,links,notes)


def deleted(rescue=False):
    c=cells(); ch=VGroup(*[chain(x) for x in XS]); marks=VGroup()
    for i,x in enumerate(XS):
        if not(rescue and i==2):
            ch[i][0][0].set_opacity(.3);marks.add(xmark([x,1.7,0],.43))
    return c,ch,marks


def fibre(y=-3.15):
    return Line([-6.05,y,0],[6.05,y,0],color=GREY,stroke_width=10)


def branches(y=-3.15,active=None):
    return VGroup(*[Line([x,-2.88,0],[x,y,0],color=COL[k] if active is True or active==k else GREY,
                        stroke_opacity=1 if active is True or active==k else .35,stroke_width=6)
                    for k,x in zip(KINDS,XS)])


def signal_scene():
    c=VGroup(*[cell(k,x,.85,h=3.3) for k,x in zip(KINDS,XS)])
    f=fibre(-2.2)
    b=VGroup(*[Line([x,-1.55,0],[x,-2.2,0],color=GREY,stroke_width=6,stroke_opacity=.4) for x in XS])
    dots=VGroup(*[Dot([x,-1.6,0],radius=.13,color=YELLOW) for x in XS])
    # A visible common output blip gives the cell silhouettes content.
    for k,x,cg in zip(KINDS,XS,c):cg.add(trace(x-.75,.65,w=1.5,h=.45,color=YELLOW))
    return c,f,b,dots


def mouse(x,y=0,color=GREY,left=False,scale=1):
    body=Ellipse(width=1.5,height=.8,color=color,fill_color=color,fill_opacity=.2).move_to([x,y,0])
    head=Circle(radius=.35,color=color,fill_color=BG,fill_opacity=1).move_to([x+.72,y+.12,0])
    ear=Circle(radius=.19,color=color,fill_color=BG,fill_opacity=1).move_to([x+.55,y+.47,0])
    eye=Dot([x+.86,y+.22,0],radius=.04,color=TEXT)
    tail=ArcBetweenPoints([x-.73,y,0],[x-1.3,y+.5,0],angle=-.8,color=color)
    g=VGroup(body,tail,head,ear,eye).scale(scale,about_point=[x,y,0])
    if left:g.flip(UP,about_point=[x,y,0])
    return g


def bottle(x,y,txt,color=TEXT):
    b=RoundedRectangle(width=.85,height=1.1,corner_radius=.12,color=color,fill_color=color,fill_opacity=.15).move_to([x,y,0])
    # Spout is below the bottle; mice occupy a separate lower band.
    sp=Line([x,y-.55,0],[x,y-1.15,0],color=color,stroke_width=4)
    return VGroup(b,sp,label(txt,x,y+.85,26,color))


def buttons(texts,y=-2.55):
    xs=np.linspace(-4.1,4.1,len(texts)) if len(texts)>1 else [0]
    return VGroup(*[block(s,x,y,TEXT,30) for s,x in zip(texts,xs)])


def prediction():
    c,ch,m=deleted(True)
    # Move the continuous cell/chain diagram up; reserve a clear answer band.
    for a in c:
        a[0].stretch_to_fit_height(3.7).stretch_to_fit_width(3.7*.63).move_to([a[0].get_x(),.6,0])
        a[1].set_y(-1.6)
    for a in ch:
        for i,n in enumerate(a[0]):n.set_y(1.95-i*.85)
        a[1].set_opacity(0)
    for a in m:a.shift(UP*.25)
    diagram=VGroup(c,ch,m)
    return VGroup(label('Which responses come back?',size=36),diagram,
                  buttons(['Bitter only','All three','None'],y=-2.5))


def countdown(scene):
    bar=Line([-5.6,-3.15,0],[5.6,-3.15,0],color=TEAL,stroke_width=10)
    track=bar.copy().set_color(GREY).set_opacity(.25)
    scene.add(track,bar,label('Think it through',y=-3.65,size=24,color=TEAL))
    scene.play(bar.animate.put_start_and_end_on([-5.6,-3.15,0],[-5.59,-3.15,0]),run_time=5,rate_func=linear)


def choice_mouse(x,color=TEXT,left=True):
    # Both heads are midway between the two tubes, in a separate lower band.
    return mouse(x-.72,-.35,color,scale=1)


def choice_answers():
    return VGroup(*[block(t,x,-2.85,TEXT,38) for t,x in [('Avoid',-2.2),('Drink',2.2)]])


def choice(question=False):
    panels=VGroup()
    for x,title,col in [(-3.25,'T2R16 mouse',ORANGE),(3.25,'Normal mouse',TEXT)]:
        frame=RoundedRectangle(width=5.95,height=5.05,corner_radius=.2,color=GREY,stroke_opacity=.4).move_to([x,.45,0])
        panels.add(VGroup(frame,label(title,x,2.65,32,col),bottle(x-1.45,1.3,'ligand',YELLOW),
                          bottle(x+1.45,1.3,'water'),choice_mouse(x,col)))
    g=VGroup(panels)
    if question:
        g.add(label('Will it avoid or drink the ligand?',y=3.5,size=36),choice_answers())
    return g


# A deterministic schematic model, not measured experimental data.
# Ligand binding gates one fixed-rate output; identical effective activation
# by A and B gives exactly the same pulse train (and zero activation is flat).
def response(t,activation=1):
    return activation*sum(np.exp(-((t-p)/.025)**2) for p in np.arange(.18,.96,.18))


def trace(x,y,w=2.5,h=.55,activation=1,color=YELLOW):
    ts=np.linspace(0,1,501)
    return VMobject(color=color,stroke_width=3).set_points_as_corners(
        [[x+w*t,y+h*response(t,activation),0] for t in ts])


class S00Title(TitleCard):
    LESSON='Smell and Taste'
    TITLE='Taste: The Cell Decides'
    def construct(self):
        g=VGroup(T('BIOCHEMISTRYPEDIA',26,TEAL),T(self.LESSON.upper(),26,GREY),
                 T(self.TITLE,48,font=TITLE_FONT),Line(LEFT*1.2,RIGHT*1.2,color=GOLD,stroke_width=4)).arrange(DOWN,buff=.4)
        self.play(FadeIn(g),run_time=.7);self.finish()


class S01Question(SpokenScene):
    def construct(self):
        c,f,b,d=signal_scene()
        q=label('Same chemical signal: how does the brain tell them apart?',size=30)
        self.at('If three kinds');self.add(c,f,b,q)
        self.at('send the same');self.add(d,label('same signal',y=-2.85,size=30,color=YELLOW),label('nerve fibre',4.7,-2.85,26))
        self.play(*[a.animate.move_to([x,-2.2,0]) for a,x in zip(d,XS)],run_time=.8)
        self.at('how does the brain');self.play(Indicate(q,color=YELLOW,scale_factor=1.03),run_time=.6)
        self.finish()


class S02Type2(SpokenScene):
    def construct(self):
        bud=Ellipse(width=12.4,height=6.3,color=GREY).move_to([0,.05,0])
        # Labels sit within the bud, above its narrowing lower outline.
        c=VGroup(*[cell(k,x,.25,h=3.2) for k,x in zip(KINDS,[-3.7,0,3.7])])
        self.at('In the taste bud');self.add(bud,c,label('Taste bud',y=3.55,size=30))
        self.at('type 2 cells');self.play(*[a[0].animate.set_fill(COL[k],.28) for a,k in zip(c,KINDS)],run_time=.5)
        self.add(label('Type II taste cells',y=-2.4,size=32));self.finish()


class S03Receptors(SpokenScene):
    def construct(self):
        self.add(cells())
        self.at('Sweet and umami');self.play(FadeIn(receptors('sweet',XS[0])),FadeIn(receptors('umami',XS[1])),run_time=.6)
        self.at('carry');self.play(Indicate(self.mobjects[-1],color=BLUE,scale_factor=1.03),run_time=.35)
        self.at('Bitter cells carry');self.play(FadeIn(receptors('bitter',XS[2])),run_time=.6)
        self.add(label('many T2R types',XS[2],-1.55,26,BLUE));self.finish()


class S04Same(SpokenScene):
    def construct(self):
        self.add(cells(),label('After the receptor',size=32))
        self.at('After the receptor');chs=VGroup(*[chain(x) for x in XS]);self.play(FadeIn(chs),run_time=.7)
        self.at('all three use');self.play(FadeIn(label('Same chain in all three cells',y=-3.35,size=30)),run_time=.4);self.finish()


class S05Chain(SpokenScene):
    def construct(self):
        c=VGroup(*[cell(k,x,.15,h=5.5) for k,x in zip(KINDS,XS)]);ch=VGroup(*[chain(x,True) for x in XS]);self.add(c,ch)
        caption=label('Enzyme',color=TEAL)
        self.at('An enzyme');self.add(caption);self.play(*[Indicate(a[0][0],color=TEAL) for a in ch],run_time=.5)
        self.at('leads to a calcium rise');self.play(Transform(caption,label('Calcium rises',color=GREEN)),*[AnimationGroup(a[0][1][0].animate.set_stroke(GREEN),a[0][1][1].animate.set_color(GREEN)) for a in ch],run_time=.5)
        self.at('Calcium opens a channel');self.play(Transform(caption,label('Calcium opens a channel',color=GREEN)),*[AnimationGroup(a[0][2][0].animate.set_stroke(GREEN),a[0][2][1].animate.set_color(GREEN)) for a in ch],run_time=.5)
        self.at('the cell depolarizes');self.play(Transform(caption,label('Cell depolarizes',color=GREEN)),*[AnimationGroup(a[0][3][0].animate.set_stroke(GREEN),a[0][3][1].animate.set_color(GREEN)) for a in ch],*[a[0].animate.set_fill(COL[k],.28) for a,k in zip(c,KINDS)],run_time=.5)
        self.finish()


class S06Atp(SpokenScene):
    def construct(self):
        c=cell('sweet',0,.15,h=4.5,active=True)
        c[1].move_to([0,-2.5,0])
        # A real gap in the membrane, masked locally; channel sides frame the path.
        gap=Line([-.42,-2,0],[.42,-2,0],color=BG,stroke_width=12)
        gate=VGroup(Line([-.43,-1.75,0],[-.43,-2.25,0],color=GREEN,stroke_width=6),Line([.43,-1.75,0],[.43,-2.25,0],color=GREEN,stroke_width=6))
        channelname=label('CALHM1/3',3.4,-.65,28,GREEN)
        leader=Line([2.2,-.85,0],[.52,-1.9,0],color=GREY)
        f=Line([-5.8,-2.85,0],[5.8,-2.85,0],color=GREY,stroke_width=14)
        self.add(c,gap,gate,channelname,leader,f,label('Nerve fibre',3.8,-3.4,28))
        particles=VGroup(*[Dot([0,1.3-i*.5,0],radius=.14,color=YELLOW) for i in range(3)])
        tag=label('ATP',2.2,1.2,30,YELLOW)
        self.at('Then ATP flows');self.add(particles,tag)
        self.play(particles.animate.shift(DOWN*1.2),tag.animate.shift(DOWN*1.2),run_time=.8)
        self.at('through a channel');self.play(particles.animate.arrange(RIGHT,buff=0).move_to([0,-2.85,0]),tag.animate.move_to([1.3,-2.5,0]),run_time=.8)
        self.at('onto the nerve');self.play(f.animate.set_color(GREEN),run_time=.45);self.finish()


class S07Rule(SpokenScene):
    def construct(self):
        c,f,b,d=signal_scene();self.add(c,f,b,d,label('Same signal',size=32,color=YELLOW))
        self.at('So the signal');self.play(*[a.animate.move_to([x,-2.2,0]) for a,x in zip(d,XS)],run_time=.7)
        self.at('what differs');self.play(*[a.animate.set_color(COL[k]).set_opacity(1) for a,k in zip(b,KINDS)],run_time=.5)
        self.at('which cell the nerve');self.play(FadeIn(label('Which cell the nerve listens to',y=-3.1,size=44)),run_time=.4);self.finish()


class S08Knockout(SpokenScene):
    def construct(self):
        c=cells();ch=VGroup(*[chain(x) for x in XS]);self.add(c,ch,label('Zhang and colleagues, 2003',size=30),label('Whole-mouse deletion',y=-3.35,size=32))
        self.at('deleted');marks=VGroup(*[xmark([x,1.7,0],.43) for x in XS]);self.play(Create(marks),*[a[0][0].animate.set_opacity(.3) for a in ch],run_time=.7);self.finish()


class S09Lost(SpokenScene):
    def construct(self):
        self.add(label('PLCβ2 deletion',y=3.35,size=34),Line([.05,-3.5,0],[.05,2.7,0],color=GREY,stroke_opacity=.4))
        cs=VGroup(*[cell(k,x,1.55,h=2.25,active=True) for k,x in zip(KINDS,[-5.4,-3.55,-1.7])])
        self.add(cs)
        for x in [-5.4,-3.55,-1.7]:self.add(xmark([x,1.55,0],.27))
        self.add(label('Nerve response (schematic)',-3.5,-.25,26))
        traces=VGroup()
        for k,y in zip(KINDS,[-1.15,-2.1,-3.05]):
            self.add(label(k if k!='umami' else 'amino acid',-5.05,y+.23,26,COL[k]))
            self.add(Line([-3.9,y,0],[-.65,y,0],color=GREY,stroke_opacity=.4))
            traces.add(trace(-3.9,y,w=3.2,h=.5,activation=1,color=GREY))
        self.add(traces)
        for y in [-1.15,-2.1,-3.05]:
            self.add(trace(-3.9,y+.28,w=3.2,h=.35,color=TEXT).set_opacity(.4))
        self.add(label('Normal reference / deletion below',-3.3,-3.6,22))
        self.at('Nerve responses');self.play(*[a[0].animate.set_fill(opacity=.025) for a in cs],*[Transform(tr,trace(-3.9,y,w=3.2,h=.5,activation=0,color=GREY)) for tr,y in zip(traces,[-1.15,-2.1,-3.05])],run_time=.55)
        self.at('tested sweet');self.play(Indicate(cs[0][0],color=ORANGE,scale_factor=1.03),run_time=.3)
        self.at('amino acid');self.play(Indicate(cs[1][0],color=PINK,scale_factor=1.03),run_time=.3)
        self.at('and bitter');self.play(Indicate(cs[2][0],color=PURPLE,scale_factor=1.03),run_time=.3)
        self.at('were lost');self.play(Indicate(traces,color=RED,scale_factor=1.02),run_time=.5)
        self.at('In Lick tests')
        self.add(label('Licks at spout, relative to water',3.4,2.65,26),label('Schematic • WT: normal, KO: deletion',3.4,2.13,26,GREY))
        base=-1.7; unit=1.65
        self.add(Line([.85,base,0],[6.1,base,0],color=GREY),Line([.85,base,0],[.85,1.55,0],color=GREY))
        water=DashedLine([.85,base+unit,0],[6.1,base+unit,0],color=TEXT)
        self.add(water,label('water',5.65,base+unit+.25,26))
        def bars(center,vals,col):
            return VGroup(*[Rectangle(width=.62,height=unit*v,stroke_color=col,fill_color=col,fill_opacity=1 if i==0 else .35).move_to([center+(i-.5)*.85,base+unit*v/2,0]) for i,v in enumerate(vals)])
        for x in [2.25,4.85]:
            self.add(label('WT',x-.425,-2.05,26),label('KO',x+.425,-2.05,26))
        self.add(label('Sweet',2.25,-2.55,28,ORANGE),label('Bitter',4.85,-2.55,28,PURPLE))
        self.at('sweet preference was');self.play(GrowFromEdge(bars(2.25,[1.8,1.08],ORANGE),DOWN),run_time=.6)
        self.add(label('Strongly\nreduced',2.25,-3.15,26,ORANGE))
        self.at('bitter avoidance was lost');self.play(GrowFromEdge(bars(4.85,[.18,1],PURPLE),DOWN),run_time=.5)
        self.add(label('Avoidance\nlost',4.85,-3.15,26,PURPLE));self.finish();self.wait(1)


class S10Spared(SpokenScene):
    def construct(self):
        self.add(label('After whole-mouse deletion',size=32))
        for k,x in zip(KINDS,[-5.3,-3.35,-1.4]):
            c=cell(k,x,h=2.7);self.add(c,xmark([x,.4,0]),Line([x,-1.95,0],[x,-2.8,0],color=GREY,stroke_opacity=.3))
        right=VGroup(cell('sour',2,h=2.7),cell('salty',5,h=2.7))
        self.at('Sour and salty');self.add(right)
        self.at('responses remained');self.play(*[a[0].animate.set_fill(GREEN,.3) for a in right],run_time=.5)
        self.at('other routes');self.add(label('Other routes',3.5,-3.25,30,GREEN))
        self.play(*[GrowArrow(Arrow([x,1.1,0],[x,-.8,0],color=GREEN,stroke_width=6)) for x in [2,5]],run_time=.4);self.finish()


class S11Rescue(SpokenScene):
    def construct(self):
        c,ch,m=deleted();self.add(c,ch,m,label('Restore the enzyme in bitter cells only',size=30))
        self.at('only in cells');self.play(FadeOut(m[2]),ch[2][0][0].animate.set_opacity(1),run_time=.6);self.finish()


class S12Predict(SpokenScene):
    def construct(self):
        q=prediction();self.at('Which responses');self.add(q)
        self.at('Bitter only');self.play(Indicate(q[2][0],color=TEAL,scale_factor=1.04),run_time=.35)
        self.at('all three');self.play(Indicate(q[2][1],color=TEAL,scale_factor=1.04),run_time=.3)
        self.at('or none');self.play(Indicate(q[2][2],color=TEAL,scale_factor=1.04),run_time=.3);self.finish()


class S13Pause(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(prediction());countdown(self)


class S14Reveal(SpokenScene):
    def construct(self):
        # Continuous four-step chains beside a full-height behavioural comparison.
        cs=VGroup(*[cell(k,x,.6,h=3.3) for k,x in zip(KINDS,[-5.4,-3.2,-1.0])])
        ch=VGroup(*[chain(x).scale(.68).move_to([x,.6,0]) for x in [-5.4,-3.2,-1.0]])
        # Keep compact pathway text readable at the house minimum size.
        for pathway in ch:
            for node in pathway[0]:
                node[1].scale(22/(26*.68))
                node[0].stretch_to_fit_width(node[1].width+.18)
        for a in ch[:2]:a.set_opacity(.3)
        self.add(cs,ch,*[xmark(ch[i][0][0].get_center(),.27) for i in [0,1]],label('Bitter only',size=38))
        self.at('Bitter only');self.play(cs[2][0].animate.set_fill(PURPLE,.3),run_time=.4)
        outputs=VGroup()
        for i,x in enumerate([-5.4,-3.2,-1.0]):
            outputs.add(Line([x,-1.9,0],[x,-2.5,0],color=GREEN if i==2 else GREY,stroke_width=8,stroke_opacity=1 if i==2 else .25))
            outputs.add(trace(x-.65,-2.7,w=1.3,h=.5,activation=1 if i==2 else 0,color=GREEN if i==2 else GREY))
        self.at('in the nerve');self.play(Create(outputs),run_time=.35)
        self.at('in behavior')
        base=-1.7;unit=1.65
        self.add(label('Bitter licks relative to water',3.25,2.55,27),label('Schematic',3.25,2,24,GREY))
        self.add(Line([.7,base,0],[6,base,0],color=GREY),Line([.7,base,0],[.7,1.3,0],color=GREY))
        self.add(DashedLine([.7,base+unit,0],[6,base+unit,0],color=TEXT),label('water',5.5,.2,24))
        bars=VGroup()
        for x,v,t in [(1.65,.18,'Normal'),(3.35,1,'Deletion'),(5.05,.18,'Rescue')]:
            bars.add(Rectangle(width=.85,height=unit*v,color=PURPLE,fill_color=PURPLE,fill_opacity=.8).move_to([x,base+unit*v/2,0]))
            self.add(label(t,x,-2.08,24))
        self.play(GrowFromEdge(bars,DOWN),run_time=.55)
        self.add(label('Bitter avoidance returns',3.35,-2.8,29,GREEN))
        self.at('did not return');self.add(label('Sweet and amino-acid responses stay absent',y=-3.5,size=28));self.finish()


class S15Separate(SpokenScene):
    def construct(self):
        c,ch,m=deleted(True);self.add(c,ch,m,fibre(),branches(active='bitter'))
        c[2][0].set_fill(PURPLE,.28)
        self.add(label('Each cell is a separate line to the nerve',size=30))
        self.at('The shared enzyme');self.play(Indicate(ch[2][0][0],color=TEAL),run_time=.6)
        self.at('The lines are separate');self.play(Flash([4.1,-3.15,0],color=PURPLE,flash_radius=.3),run_time=.6);self.finish()


def sweet_wrong(inserted=False):
    c=cell('sweet',-2,.2,h=4.6)
    r=receptors('sweet',-2)
    foreign=block('T2R16',-2 if inserted else 3, -.75 if inserted else 1.5,BLUE,30)
    name=label('Human bitter receptor',3,2.4,28,BLUE)
    lead=Line([2,2.05,0],foreign.get_right()+[.08,0,0],color=BLUE) if inserted else Line([3,2.05,0],[3,1.85,0],color=BLUE)
    return VGroup(c,r,foreign,name,lead)


class S16Meaning(SpokenScene):
    def construct(self):
        g=sweet_wrong();self.add(g,label('Does the cell decide what a line means?',size=32))
        self.at('Does the cell');self.play(Indicate(g[0][0],color=ORANGE,scale_factor=1.02),run_time=.5)
        self.at('Put a receptor');self.play(g[2].animate.move_to([-2,-.75,0]),Transform(g[4],Line([2,2.05,0],[-.9,-.55,0],color=BLUE)),run_time=.8)
        self.add(label('Put a receptor in the wrong cell',2,-2.9,30));self.finish()


class S17Mueller(SpokenScene):
    def construct(self):
        g=sweet_wrong(True);self.add(g,label('Mueller and colleagues, 2005',size=32))
        self.at('Mueller and colleagues');self.play(Indicate(g[2],color=BLUE),run_time=.5)
        self.at('into the sweet cells');self.play(g[0][0].animate.set_fill(ORANGE,.2),run_time=.5)
        self.add(label('Human T2R16 in mouse sweet cells',2,-2.9,28));self.finish()


class S18Predict(SpokenScene):
    def construct(self):
        g=choice();self.add(g)
        self.at('Its ligand');self.play(Indicate(g[0][0][2],color=YELLOW),run_time=.6)
        self.at('normal mice ignore');self.add(label('Normal mice:\nignore the ligand',3.25,-1.5,24))
        self.play(Indicate(g[0][1][4],color=TEXT,scale_factor=1.03),run_time=.5)
        self.at('Will these mice');self.play(FadeIn(VGroup(label('Will it avoid or drink the ligand?',y=3.5,size=36),choice_answers())),run_time=.5);self.finish()


class S19Pause(Scene):
    def construct(self):
        self.camera.background_color=BG;g=choice(True);self.add(g,label('Normal mice:\nignore the ligand',3.25,-1.5,24))
        # The countdown is in its own slim lower band.
        bar=Line([-5.6,-3.55,0],[5.6,-3.55,0],color=TEAL,stroke_width=10)
        self.add(bar.copy().set_color(GREY).set_opacity(.3),bar)
        self.play(bar.animate.put_start_and_end_on([-5.6,-3.55,0],[-5.59,-3.55,0]),run_time=5,rate_func=linear)


def share_bar(x,y,fraction):
    w=5.0
    a=Rectangle(width=w*fraction,height=.35,color=YELLOW,fill_opacity=.85,fill_color=YELLOW).move_to([x-w/2+w*fraction/2,y,0])
    b=Rectangle(width=w*(1-fraction),height=.35,color=TEXT,fill_opacity=.3,fill_color=TEXT).move_to([x+w*fraction/2,y,0])
    return VGroup(a,b)


class S20Reveal(SpokenScene):
    def construct(self):
        g=choice();self.add(g)
        self.add(label('Share of licks at each spout • schematic',y=-2.55,size=26))
        self.add(VGroup(Dot(color=YELLOW),T('ligand',26),Dot(color=TEXT).set_opacity(.5),T('water',26)).arrange(RIGHT,buff=.2).move_to([0,-3.02,0]))
        self.at('They drink it');self.play(FadeIn(share_bar(-3.25,-1.65,.85)),run_time=.5)
        self.add(label('Mostly ligand',-3.25,-1.15,27,ORANGE))
        self.at('while normal mice');self.play(FadeIn(share_bar(3.25,-1.65,.5)),run_time=.6)
        self.add(label('About equal: no preference',3.25,-1.15,26))
        self.at('The receptor detects');self.play(Indicate(g[0][0][2],color=BLUE),run_time=.5)
        self.at('but the sweet cell');self.add(label('Sweet-cell activation drives attraction',y=3.45,size=30,color=ORANGE))
        self.play(FadeIn(label('Not a report of subjective sweetness',y=-3.5,size=28)),run_time=.5);self.finish()


class S21Labeled(SpokenScene):
    def construct(self):
        g=sweet_wrong(True);g[0][1].set_opacity(0)
        f=fibre();w=Line([-2,-2.1,0],[-2,-3.15,0],color=ORANGE,stroke_width=7)
        self.add(g,f,w,label('Whatever receptor is on it',size=32))
        self.at('each kind of cell');self.play(FadeIn(block('SWEET',1,-3.15,ORANGE,30)),f.animate.set_color(ORANGE),run_time=.5);self.finish()


class S22Pooling(SpokenScene):
    def construct(self):
        c=cell('bitter',-2.5,.2,h=4.6);r=receptors('bitter',-2.5)
        self.add(c,r,label('One cell, many receptors',size=34),label('One cell',-2.5,-3.25,28,PURPLE))
        a=block('A',-5.5,1.45,YELLOW,30);b=block('B',-5.5,.5,YELLOW,30)
        self.add(a,b,label('Compounds',-5.2,2.35,26,YELLOW))
        self.add(label('Spikes per second',3.5,2.4,28),label('Schematic • same activation',3.5,1.85,26,GREY))
        for x,txt in [(1.1,'with A'),(4,'with B')]:
            self.add(label(txt,x+1,-.85,28),Line([x,-.3,0],[x,1.2,0],color=GREY),Line([x,-.3,0],[x+2.1,-.3,0],color=GREY),label('time',x+1,-1.4,26,GREY))
        ta=trace(1.1,-.3,2.1,1.25);tb=trace(4,-.3,2.1,1.25)
        self.at('a bitter cell pools');self.play(a.animate.move_to([-2.5,1.45,0]),run_time=.65)
        self.play(FadeOut(a),Indicate(r[0],color=YELLOW),Create(ta),run_time=.6)
        self.at('By its rate alone');self.play(b.animate.move_to([-2.5,.5,0]),run_time=.65)
        self.play(FadeOut(b),Indicate(r[1],color=YELLOW),Create(tb),run_time=.6)
        self.at('that cell cannot say');self.play(FadeIn(label('Identical output for A and B',3.6,-2.45,28,color=YELLOW)),run_time=.4);self.finish()


class S23Trade(SpokenScene):
    def construct(self):
        self.add(label('Many smell lines',-3.5,3.3,30,BLUE),label('Bitter cells',3.1,3.3,30,PURPLE))
        sm=VGroup()
        for i,x in enumerate(np.linspace(-5.8,-1.2,5)):
            sm.add(VGroup(block('R'+str(i+1),x,2.25,BLUE,26),Line([x,1.8,0],[x,-1.65,0],color=BLUE,stroke_width=5)))
        bitter=VGroup()
        for x,mix in [(.8,['A','B']),(3.05,['A','C']),(5.3,['B','C'])]:
            c=cell('bitter',x,.1,h=3.3,name=False)
            chips=VGroup(*[block(n,x,1.2-i*.9,BLUE,26) for i,n in enumerate(mix)])
            bitter.add(VGroup(c,chips))
        self.add(sm,bitter)
        mixlabel=label('Different receptor mixes',3.1,-1.9,28)
        self.at('Not every bitter cell');self.play(FadeIn(mixlabel),*[Indicate(g[1],color=BLUE,scale_factor=1.04) for g in bitter],run_time=.7)
        self.at('may keep some distinctions');distinctions=label('May retain some distinctions',y=-2.35,size=32,color=TEXT);self.add(distinctions)
        self.play(*[Indicate(g[1],color=PURPLE,scale_factor=1.03) for g in bitter],run_time=.6)
        self.at('Still pooling fits');box=VGroup(RoundedRectangle(width=11.8,height=.85,corner_radius=.15,color=TEXT),T('Eat it, or reject it?',38)).move_to([0,-3.1,0])
        self.add(box)
        # Separate arrival points on the top edge keep every arrowhead distinct.
        arrows=VGroup()
        for x,dest in zip(np.linspace(-5.8,-1.2,5),np.linspace(-5.3,-.9,5)):
            arrows.add(Arrow([x,-1.65,0],[dest,box.get_top()[1]+.015,0],color=BLUE,buff=.05,stroke_width=2,tip_length=.16,max_tip_length_to_length_ratio=.2))
        for x,dest in zip([.8,3.05,5.3],[.8,3.05,5.3]):
            arrows.add(Arrow([x,-1.65,0],[dest,box.get_top()[1]+.015,0],color=PURPLE,buff=.05,stroke_width=2,tip_length=.16,max_tip_length_to_length_ratio=.2))
        # Clear the transition captions before the convergence paths pass through.
        self.play(FadeOut(mixlabel),FadeOut(distinctions),run_time=.2)
        self.play(Create(arrows),run_time=.8)
        self.at('Eat it or reject it');self.play(Indicate(box,color=YELLOW,scale_factor=1.04),run_time=.5);self.finish()


class S24Scope(SpokenScene):
    def construct(self):
        self.add(label('Keep the scope',size=38),RoundedRectangle(width=12,height=5.8,corner_radius=.25,color=GREY).move_to([0,-.15,0]),mouse(-3.95,.1,TEXT,scale=1.35))
        rows=VGroup(T('Mouse experiments',40),T('Periphery: taste cells\nand nerves',36),T('Some cells respond to\nmore than one quality',36,color=YELLOW)).arrange(DOWN,aligned_edge=LEFT,buff=.85)
        rows.move_to([1.6,-.15,0])
        self.at('Keep the scope')
        self.at('mouse experiments on the periphery');self.play(FadeIn(rows[0]),FadeIn(rows[1]),run_time=.6)
        self.at('Some taste cells');self.play(FadeIn(rows[2]),run_time=.6)
        self.at('more than one quality');self.play(Indicate(rows[2],color=YELLOW,scale_factor=1.03),run_time=.5);self.finish()


class S25Takeaway(SpokenScene):
    def construct(self):
        self.add(label('SMELL',-3.5,3.15,36,BLUE),label('TASTE',3.3,3.15,36),Line([0,-3.4,0],[0,3.4,0],color=GREY,stroke_opacity=.3))
        sm=VGroup(*[Line([x,-1.8,0],[x,2.05,0],color=BLUE if i not in [1,4] else GREY,stroke_width=8,stroke_opacity=1 if i not in [1,4] else .25) for i,x in enumerate(np.linspace(-5.6,-1.4,6))])
        tc=VGroup(*[cell(k,x,.25,h=3.1,active=False) for k,x in zip(KINDS,[1.1,3.15,5.2])])
        # Names remain readable outside each narrower cell.
        self.add(sm,tc,label('A pattern across many lines',-3.5,-2.65,28),label('Mainly which cell is active',3.3,-2.65,28))
        self.at('Smell reads a pattern');self.play(Indicate(sm,color=BLUE,scale_factor=1.02),run_time=.6)
        self.at('Taste reads mainly');self.play(tc[0][0].animate.set_fill(ORANGE,.4),run_time=.6);self.finish()


class S26End(EndCard):
    LINE='Smell reads patterns of lines; taste mainly reads the active cell.'
    def construct(self):
        g=VGroup(T('Smell reads patterns of lines;',40,font=TITLE_FONT),T('taste mainly reads the active cell.',40,font=TITLE_FONT),T('biochemistrypedia.com',30,TEAL)).arrange(DOWN,buff=.45)
        self.play(FadeIn(g),run_time=.7);self.finish()
