"""Chapter 2: Cutting One Route at a Time.
COLOR MAP (from scenes.old.py, shared across chapters):
YELLOW tone / intact passing axons; GOLD shock; BLUE freezing and its identified route;
ORANGE pressure rise and its identified route; TEAL amygdala;
PURPLE unnamed targets; RED damage; GREY controls, axes, unknowns;
PINK people; TEXT learned differences and claims.
All bars use the lesson's invented worked-problem data, NOT 1988 measurements.
Geometry adapts the reference nbox, arr and raw-score bar plotting helpers.
"""
from bp_style import *
import numpy as np

PURPLE = '#B58CD9'
ORANGE = '#F29E4C'
PINK = '#E58FB5'
# Raw values in freezing percent / pressure mmHg, from scenes.old.py.
DATA = {'paired': (60, 20), 'unpaired': (8, 3), 'lh': (57, 4),
        'pag': (9, 19), 'cea': (6, 3)}


def lines(text, size=28, color=TEXT):
    return VGroup(*[T(s, size, color) for s in text.split('\n')]).arrange(DOWN, buff=.12)


def nbox(text, color=BLUE, size=26, min_w=0, min_h=0):
    label = lines(text, size, color)
    back = RoundedRectangle(width=max(min_w, label.width+.5), height=max(min_h, label.height+.4),
                            corner_radius=.14, stroke_color=color, stroke_width=3,
                            fill_color=BG, fill_opacity=1)
    return VGroup(back, label.move_to(back))


def arr(a, b, color=GREY):
    return Arrow(a, b, buff=.08, color=color, stroke_width=5, tip_length=.2)


def heading(text, color=TEXT):
    return T(text, 30, color).move_to([0, 3.12, 0])


def chart_frame(title='Intact rats: paired'):
    g = VGroup(heading(title), T('Invented numbers · design of the 1988 study', 26, GREY).move_to([0, -3.64, 0]))
    for j, (name, top, ticks, col) in enumerate((('Freezing (% of tone)', 70, (0, 30, 60), BLUE),
                                                ('Pressure rise (mmHg)', 24, (0, 10, 20), ORANGE))):
        x = -5.65 + j*6.3
        g.add(T(name, 26, col).move_to([x+2.1, 2.35, 0]))
        g.add(Line([x,-2.25,0], [x,1.65,0], color=GREY),
              Line([x,-2.25,0], [x+4.8,-2.25,0], color=GREY))
        for v in ticks:
            g.add(M(str(v),26,GREY).move_to([x-.32,-2.25+v*3.9/top,0]))
    return g


def bar(j, slot, value, label, color=None):
    top = (70,24)[j]
    col = color or (BLUE,ORANGE)[j]
    x = -5.65+j*6.3 + (1.05,2.65,4.15)[slot]
    h = max(.02,value*3.9/top)
    b = Rectangle(width=.83,height=h,stroke_color=col,fill_color=col,fill_opacity=.65,stroke_width=2)
    b.move_to([x,-2.25+h/2,0])
    val = M(str(value),26,col).move_to([x,-2.25+h+.23,0])
    lab = lines(label,26,GREY).move_to([x,-3.1 if '\n' in label else -2.94,0])
    return VGroup(b,val,lab)


def pair(key, slot=0, label='paired'):
    return VGroup(*[bar(j,slot,v,label,GREY if key=='unpaired' else None) for j,v in enumerate(DATA[key])])


def baselines():
    g=VGroup()
    for j,v in enumerate(DATA['unpaired']):
        x=-5.65+j*6.3; y=-2.25+v*3.9/(70,24)[j]
        # Labels sit above the reference line, away from ticks and low bars.
        g.add(DashedLine([x,y,0],[x+4.9,y,0],dash_length=.18,color=TEXT,stroke_width=2),
              lines('baseline\n'+('8%' if j==0 else '+3 mmHg'),22).move_to([x+5.35,y+.62,0]))
    return g

def chart(scene, title, lesion=None, include_base=True):
    frame=chart_frame(title); p=pair('paired'); scene.add(frame,p)
    if include_base: scene.add(pair('unpaired',1,'unpaired'),baselines())
    if lesion:
        q=pair(lesion,2,'lesion'); scene.add(q); return q
    return None


def circuit(known=True):
    c=nbox('central\namygdala',TEAL,30,min_w=3.0,min_h=1.1).move_to([0,2.05,0])
    lh=nbox('lateral\nhypothalamus',ORANGE if known else PURPLE,26,min_w=3.5).move_to([-3.2,-.15,0])
    pg=nbox('caudal periaqueductal\ngray',BLUE if known else PURPLE,26,min_w=3.8).move_to([3.2,-.15,0])
    pr=nbox('pressure rise',ORANGE,28,min_w=3.5).move_to([-3.2,-2.35,0])
    fr=nbox('freezing',BLUE,28,min_w=3.8).move_to([3.2,-2.35,0])
    edges=VGroup(arr(c.get_bottom(),lh.get_top(),ORANGE if known else GREY),
                 arr(c.get_bottom(),pg.get_top(),BLUE if known else GREY),
                 arr(lh.get_bottom(),pr.get_top(),ORANGE if known else GREY),
                 arr(pg.get_bottom(),fr.get_top(),BLUE if known else GREY))
    return VGroup(c,lh,pg,pr,fr,edges)


def puzzle():
    c=nbox('central amygdala',TEAL,32,min_w=4).move_to([0,2,0])
    q=nbox('?',YELLOW,56,min_w=2,min_h=1.1).move_to([0,0,0])
    fr=nbox('freezing',BLUE,32,min_w=3.8).move_to([-3,-2.2,0])
    pr=nbox('pressure rise',ORANGE,32,min_w=3.8).move_to([3,-2.2,0])
    return VGroup(c,q,fr,pr,arr(c.get_bottom(),q.get_top()),
                  arr(q.get_bottom(),fr.get_top(),BLUE),arr(q.get_bottom(),pr.get_top(),ORANGE))


def brain_map(which):
    # Sagittal silhouette, with two named targets and no damage slash.
    outline=VMobject(color=GREY,stroke_width=3)
    outline.set_points_smoothly([[-2.45,-.12,0],[-2.55,.35,0],[-1.8,.85,0],
        [-.7,.95,0],[.5,.8,0],[1.5,.45,0],[1.95,.05,0],
        [2.35,-.3,0],[1.85,-.42,0],[1.05,-.1,0],[-.3,-.35,0],[-1.6,-.3,0],[-2.45,-.12,0]])
    lh=Dot([-1.0,-.08,0],radius=.12,color=RED if which=='lh' else PURPLE)
    pg=Dot([1.15,.08,0],radius=.12,color=RED if which=='pag' else PURPLE)
    left=lines('lateral hypothalamus\n(LH)',22,RED if which=='lh' else GREY).move_to([-1.25,-.94,0])
    right=lines('caudal periaqueductal\ngray (PAG)',22,RED if which=='pag' else GREY).move_to([1.5,.96,0])
    leaders=VGroup(Line(left.get_top()+UP*.05,lh.get_bottom(),color=RED if which=='lh' else GREY),
                   Line(right.get_bottom()+DOWN*.05,pg.get_top(),color=RED if which=='pag' else GREY))
    return VGroup(outline,lh,pg,left,right,leaders)


def prediction(which):
    # Keep the entire control chart visible, without an opaque covering card.
    background=VGroup(chart_frame(''),pair('paired'),pair('unpaired',1,'unpaired'),baselines()).set_opacity(.58)
    # Map occupies unused upper right; the question occupies unused upper left.
    brain=brain_map(which).move_to([3.45,1.95,0])
    question=lines('Do both responses need\nthese neurons?' if which=='lh' else 'Damage a different target',28,YELLOW).move_to([-3.0,1.65,0])
    ask=lines('Predict: what happens\nto freezing?' if which=='lh' else 'Predict both responses',28,YELLOW).move_to([-3.0,2.9,0])
    # Control bars remain lower in the frame, preserving their exact values.
    background.stretch(.67,1,about_point=[0,-3.4,0])
    # Compress vertical plot geometry, while preserving 26 pt lettering.
    for mob in background.get_family():
        if isinstance(mob, Text):
            mob.stretch(1/.67,1)
            if mob.text.startswith('baseline '): mob.shift(UP*.12)
            elif mob.text in ('paired','unpaired'): mob.shift(DOWN*.1)
    return VGroup(background,brain,question,ask)


def rat_icon(color=BLUE, moving=False):
    body=Polygon([-1.4,-.6,0],[-1.45,.05,0],[-1,.65,0],[.3,.7,0],[.9,.35,0],[1.5,.1,0],[1.6,-.2,0],[.8,-.45,0],[.55,-.65,0],color=color,fill_color=color,fill_opacity=.3)
    ear=Circle(radius=.22,color=color,fill_color=BG,fill_opacity=1).move_to([.65,.58,0])
    eye=Dot([1.03,.18,0],radius=.055,color=TEXT)
    feet=VGroup(Line([-.9,-.5,0],[-.65,-.72,0],color=color),Line([.4,-.55,0],[.9,-.72,0],color=color))
    tail=ArcBetweenPoints([-1.4,-.4,0],[-2.25,.5,0],angle=-PI/2,color=color,stroke_width=4)
    ground=Line([-2.4,-.78,0],[1.9,-.78,0],color=GREY)
    if moving:
        feet=VGroup(Line([-.9,-.5,0],[-1.35,-.72,0],color=color),
                    Line([.4,-.55,0],[1.15,-.72,0],color=color))
        motion=VGroup(*[Line([-2.8,y,0],[-2.3,y,0],color=color,stroke_width=4) for y in (.1,.4,.7)])
        return VGroup(body,ear,eye,feet,tail,ground,motion)
    return VGroup(body,ear,eye,feet,tail,ground)


def gauge_icon(impaired=False):
    rim=Arc(radius=1.35,start_angle=0,angle=PI,color=ORANGE,stroke_width=6)
    ticks=VGroup(*[Line([1.14*np.cos(a),1.14*np.sin(a),0],[1.34*np.cos(a),1.34*np.sin(a),0],color=ORANGE,stroke_width=3) for a in np.linspace(0,PI,9)])
    needle=Line([0,0,0],[-1.1,.18,0] if impaired else [.7,.9,0],color=ORANGE,stroke_width=6)
    return VGroup(rim,ticks,needle,Dot(ORIGIN,color=ORANGE))


def tissue(target='Caudal periaqueductal gray', dead=False):
    region=RoundedRectangle(width=10.6,height=5.25,corner_radius=.3,color=PURPLE,fill_color=PURPLE,fill_opacity=.08).move_to([0,-.1,0])
    cells=VGroup(*[Circle(radius=.6,color=PURPLE,fill_color=PURPLE,fill_opacity=.65).move_to([x,y,0]) for x,y in ((-3,1.05),(0,-.9),(3,1.05))])
    if dead: cells.set_opacity(.16)
    axons=VGroup(*[Line([-5.6,y,0],[5.6,y,0],color=YELLOW,stroke_width=6) for y in (-.05,.35)])
    title=heading(target,PURPLE)
    label=T('passing axons',28,YELLOW).move_to([3.4,-1.8,0])
    leader=arr([3.4,-1.5,0],[3.4,-.12,0],YELLOW)
    neurons=T('neurons (cell bodies)',28,PURPLE).move_to([-.4,2.3,0])
    nl=arr([-1.8,2.15,0],[-2.7,1.5,0],PURPLE)
    return VGroup(title,region,cells,axons,label,leader,neurons,nl)


def toxin():
    return T('ibotenic acid',28,RED).move_to([0,-3.25,0])


def countdown(scene,which):
    scene.camera.background_color=BG
    scene.add(prediction(which))
    ring=Circle(radius=.32,color=GREY).move_to([0,3.15,0])
    progress=Arc(radius=.32,start_angle=PI/2,angle=TAU,color=YELLOW).move_to(ring)
    scene.add(ring,progress)
    scene.play(Uncreate(progress),run_time=8,rate_func=linear)


class S00Title(TitleCard):
    LESSON='Emotion and Stress'
    TITLE='Cutting One Route at a Time'

class S01Question(SpokenScene):
    def construct(self):
        g=puzzle(); self.add(g,heading('Cutting one route at a time'))
        self.at('Freezing and')
        self.play(g[2][0].animate.set_fill(BLUE,opacity=.2),run_time=.35)
        self.at('pressure rise')
        self.play(g[3][0].animate.set_fill(ORANGE,opacity=.2),run_time=.35)
        self.at('Do they travel')
        self.play(Indicate(g[1],color=YELLOW),run_time=.6)
        self.finish()


class S02Ledoux(SpokenScene):
    def construct(self):
        self.add(heading('The experiment · in rats'))
        year=M('1988',70,GOLD).move_to([0,1.8,0]); self.add(year)
        lead=T('Joseph LeDoux and colleagues',40,PINK).move_to([0,.2,0])
        names=lines('Iwata · Cicchetti · Reis',34).move_to([0,-1,0])
        self.at('Joseph')
        self.play(FadeIn(lead),run_time=.4)
        self.at('and his colleagues')
        self.play(FadeIn(names),run_time=.4)
        self.at('in rats')
        self.play(FadeIn(nbox('Study of learned responses in rats',TEAL,30).move_to([0,-2.5,0])),run_time=.3)
        self.finish()


class S03Design(SpokenScene):
    def construct(self):
        self.add(heading('Damage before training'))
        labels=['Damage one target of the central amygdala','Recover: two weeks','Train: tone paired with a shock','Test: tone alone · next day']
        boxes=VGroup(*[nbox(s,GREY,28,min_w=11.6,min_h=.85).move_to([0,1.85-i*1.4,0]) for i,s in enumerate(labels)])
        boxes.set_opacity(.65)
        self.add(boxes)
        marker=Dot([-6.15,1.85,0],radius=.12,color=RED)
        self.at('First')
        self.play(boxes[0].animate.set_opacity(1),FadeIn(marker),run_time=.4)
        self.at('they damaged')
        self.play(boxes[0][0].animate.set_stroke(RED),run_time=.35)
        self.at('Two weeks later')
        self.play(boxes[1].animate.set_opacity(1),marker.animate.move_to([-6.15,.45,0]),run_time=.4)
        self.at('they trained')
        self.play(boxes[2].animate.set_opacity(1),marker.animate.move_to([-6.15,-.95,0]),run_time=.4)
        self.at('the next day')
        self.play(boxes[3].animate.set_opacity(1),marker.animate.move_to([-6.15,-2.35,0]),run_time=.4)
        self.wait(2)
        self.finish()

class S04Measures(SpokenScene):
    def construct(self):
        self.add(heading('Both responses in the same rats'))
        rat=rat_icon().scale(1.4).move_to([-3.2,.4,0])
        gauge=gauge_icon().scale(1.75).move_to([3.2,.4,0])
        self.add(rat,gauge,T('freezing',34,BLUE).move_to([-3.2,-2.25,0]),
                 lines('blood pressure\npressure rise',32,ORANGE).move_to([3.2,-2.25,0]))
        self.at('both responses')
        self.play(Indicate(rat),run_time=.4)
        self.at('the rise in')
        self.play(Rotate(gauge[2],angle=.25,about_point=gauge[2].get_start()),run_time=.4)
        self.wait(1.5)
        self.finish()


class S05Bars(SpokenScene):
    def construct(self):
        self.add(chart_frame('Paired: tone and shock together'))
        self.at('Picture two bars')
        p=pair('paired')
        self.play(*[GrowFromEdge(b[0],DOWN) for b in p],*[FadeIn(b[2]) for b in p],run_time=.65)
        self.at('show two tall bars')
        self.play(*[FadeIn(b[1]) for b in p],run_time=.35)
        self.finish()

class S06Floor(SpokenScene):
    def construct(self):
        chart(self,'Intact rats: paired and unpaired',include_base=False)
        definition=T('Unpaired: tone and shock never together',26,GREY).move_to([0,2.85,0])
        self.remove(self.mobjects[0][0]); self.add(definition)
        self.at('show two short bars')
        p=pair('unpaired',1,'unpaired')
        self.play(*[GrowFromEdge(b[0],DOWN) for b in p],*[FadeIn(VGroup(b[1],b[2])) for b in p],run_time=.5)
        self.at('our baseline')
        self.play(Create(baselines()),run_time=.4)
        self.finish()

class S07Learned(SpokenScene):
    def construct(self):
        self.add(heading('Estimate the learned part'),T('Invented numbers',26,GREY).move_to([0,-3.5,0]))
        for j,(lo,hi) in enumerate(zip(DATA['unpaired'],DATA['paired'])):
            x=-4.7+j*3.2; sc=4.6/(70,24)[j]; y=-2.4
            col=(BLUE,ORANGE)[j]
            self.add(T(('Freezing','Pressure rise')[j],28,col).move_to([x,2.55,0]))
            bottom=Rectangle(width=.8,height=lo*sc,color=GREY,fill_color=GREY,fill_opacity=.6).move_to([x,y+lo*sc/2,0])
            learned=Rectangle(width=.8,height=(hi-lo)*sc,color=col,fill_color=col,fill_opacity=.55).move_to([x,y+(hi+lo)*sc/2,0])
            self.add(bottom,learned,DashedLine([x-.6,y+lo*sc,0],[x+1.6,y+lo*sc,0],color=TEXT,dash_length=.18))
            self.add(lines('baseline\n'+('8%' if j==0 else '+3 mmHg'),26).move_to([x+.9,-2.8,0]),
                     arr([x+.8,-2.4,0],bottom.get_right(),GREY))
            brace=Brace(learned,RIGHT,buff=.12,color=col)
            self.add(brace,T('learned',26,col).rotate(PI/2).next_to(brace,RIGHT,buff=.12))
        a=lines('1. Baseline does not move',30).move_to([3,1.8,0])
        b=lines('2. Score = baseline\n+ learned',30).move_to([3,.25,0])
        self.at('we assume')
        self.play(FadeIn(a),run_time=.4)
        self.at('plus a learned part')
        self.play(FadeIn(b),run_time=.4)
        self.at('estimates the learned response')
        self.play(FadeIn(lines('Excess above baseline\n= estimated learned response',28,YELLOW).move_to([3,-1.7,0])),run_time=.4)
        self.finish()


class S08Predict1(SpokenScene):
    def construct(self):
        p=prediction('lh'); self.add(p)
        self.at('through these')
        self.play(Indicate(p[1],color=RED),run_time=.6)
        self.at('What should damage')
        self.play(Indicate(p[3],color=YELLOW),run_time=.5)
        self.finish()

class S09Pause(Scene):
    def construct(self):
        countdown(self,'lh')

class S10Reveal1(SpokenScene):
    def construct(self):
        self.add(prediction('lh'))
        self.at('both would fall')
        self.play(Indicate(self.mobjects[0][2]),run_time=.5)
        self.at('They do not')
        self.clear(); chart(self,'Damage: lateral hypothalamus')
        # Withhold freezing result until the next sentence/scene.
        self.at('pressure rise falls')
        p=bar(1,0,20,'paired')[0].copy(); self.add(p)
        result=bar(1,2,4,'lesion')
        self.play(Transform(p,result[0]),FadeIn(result[1]),FadeIn(result[2]),run_time=.7)
        self.finish()

class S11Reveal1b(SpokenScene):
    def construct(self):
        chart(self,'Damage: lateral hypothalamus'); self.add(bar(1,2,4,'lesion'))
        self.add(T('Separable contributions within a larger network',24,GREY).move_to([0,2.8,0]))
        f=bar(0,2,57,'lesion')
        self.at('Freezing stays')
        self.play(GrowFromEdge(f[0],DOWN),FadeIn(f[1]),FadeIn(f[2]),run_time=.6)
        self.at('So freezing')
        self.play(FadeIn(T('Mostly survives · almost all',22,BLUE).move_to([-3.1,1.65,0])),run_time=.4)
        self.at('but the pressure')
        self.play(FadeIn(lines('mostly lost\nalmost none',26,ORANGE).move_to([4.8,.1,0])),run_time=.4)
        self.finish()

class S12Predict2(SpokenScene):
    def construct(self):
        p=prediction('pag'); self.add(p)
        self.at('Now damage')
        self.play(Indicate(p[1],color=RED),run_time=.5)
        self.at('What do you expect')
        self.play(Indicate(p[3],color=YELLOW),run_time=.5)
        self.finish()

class S13Pause(Scene):
    def construct(self):
        countdown(self,'pag')

class S14Reveal2(SpokenScene):
    def construct(self):
        chart(self,'Damage: caudal periaqueductal gray')
        self.at('freezing drops')
        f=bar(0,0,60,'paired')[0].copy(); self.add(f)
        result=bar(0,2,9,'lesion')
        self.play(Transform(f,result[0]),FadeIn(result[1]),FadeIn(result[2]),run_time=.7)
        self.at('pressure rise survives')
        p=bar(1,2,19,'lesion')
        self.play(GrowFromEdge(p[0],DOWN),FadeIn(p[1]),FadeIn(p[2]),run_time=.55)
        self.finish()

class S15Double(SpokenScene):
    def construct(self):
        title=heading('Each lesion spares one response'); self.add(title)
        # Each measure has its own axis and units; both lesion patterns use that scale.
        self.add(chart_frame('')[1:])
        for j,(top,unit) in enumerate(((70,'% of tone'),(24,'mmHg'))):
            for slot,key,label in ((0,'lh','LH lesion'),(2,'pag','PAG lesion')):
                self.add(bar(j,slot,DATA[key][j],label))
        self.add(baselines())
        self.at('double dissociation')
        self.play(Transform(title,heading('Double dissociation')),run_time=.4)
        self.finish()


class S16Meaning(SpokenScene):
    def construct(self):
        old=puzzle(); self.add(old)
        self.at('different targets')
        g=circuit()
        self.play(ReplacementTransform(old,g),run_time=1)
        self.at('different responses')
        self.play(Indicate(g[3]),Indicate(g[4]),run_time=.5)
        self.add(T('Separable contributions · simplified model',26,GREY).move_to([0,-3.4,0]))
        self.finish()


class S17Cea(SpokenScene):
    def construct(self):
        chart(self,'Worked problem')
        footer=self.mobjects[0][1]
        footer.scale(22/26).move_to([0,-3.72,0])
        self.at('damage to the')
        self.remove(self.mobjects[0][0]); self.add(heading('Damage: central amygdala',RED))
        self.at('neither learned response')
        p=pair('cea',2,'lesion')
        for b in p: b[1].shift(UP*.35)
        self.play(*[GrowFromEdge(b[0],DOWN) for b in p],*[FadeIn(VGroup(b[1],b[2])) for b in p],run_time=.6)
        self.at('a shared source')
        self.play(FadeIn(T('No learned response above baseline',24).move_to([0,-3.35,0])),run_time=.4)
        self.finish()

class S18Method(SpokenScene):
    def construct(self):
        g=tissue(); self.add(g)
        self.at('caudal midbrain damage')
        self.play(g[1].animate.set_fill(PURPLE,opacity=.2),run_time=.4)
        self.at('used')
        self.play(FadeIn(toxin()),run_time=.4)
        self.at('kills cell bodies')
        lost=T('cell bodies lost',28,RED).move_to([-4.2,-1.55,0])
        self.play(g[2].animate.set_opacity(.16),FadeIn(lost),
                  FadeIn(arr(lost.get_top(),g[2][1].get_left(),RED)),run_time=.5)
        self.at('spares passing axons')
        self.play(g[3].animate.set_stroke(YELLOW,width=9),run_time=.4)
        self.finish()

class S19MethodB(SpokenScene):
    def construct(self):
        g=tissue(dead=True); self.add(g,toxin())
        self.at('freezing loss points')
        rat=rat_icon(moving=True).scale(.35).move_to([-3,-1.6,0])
        loss=T('freezing impaired',26,BLUE).move_to([-2.7,-2.4,0])
        self.play(g[1].animate.set_fill(BLUE,opacity=.22),FadeIn(rat),FadeIn(loss),
                  FadeIn(arr(loss.get_top(),rat.get_bottom(),BLUE)),run_time=.5)
        self.at('not to cut')
        self.play(Indicate(g[3],color=YELLOW),run_time=.4)
        self.at('The same toxin')
        self.clear(); h=tissue('Lateral hypothalamus'); self.add(h,toxin())
        self.play(h[1].animate.set_fill(ORANGE,opacity=.2),h[2].animate.set_opacity(.16),run_time=.4)
        self.at('impaired the pressure rise')
        # Replace lower labels with two attached measured outcomes.
        self.remove(h[4],h[5])
        gauge=gauge_icon(impaired=True).scale(.55).move_to([-3,-1.5,0])
        pressure=T('pressure rise impaired',26,ORANGE).move_to([-3,-2.4,0])
        self.play(FadeIn(gauge),FadeIn(pressure),FadeIn(arr(pressure.get_top(),gauge.get_bottom(),ORANGE)),run_time=.4)
        self.at('while sparing freezing')
        rat=rat_icon().scale(.38).move_to([3,-1.5,0])
        spared=T('freezing spared',26,BLUE).move_to([3,-2.4,0])
        self.play(FadeIn(rat),FadeIn(spared),FadeIn(arr(spared.get_top(),rat.get_bottom(),BLUE)),run_time=.4)
        self.finish()


class S20Takeaway(SpokenScene):
    def construct(self):
        self.add(heading('What this experiment supports'))
        card=nbox('Different targets contribute to\ndifferent measured responses,\nbelow one amygdala node.',TEAL,38,min_w=11,min_h=3.8)
        self.add(card,T('Separable contributions within a larger network',26,GREY).move_to([0,-2.15,0]))
        self.at('It says nothing yet')
        self.at('about a feeling')
        self.play(FadeIn(T('A feeling: not measured here',30,GREY).move_to([0,-2.8,0])),run_time=.3)
        self.wait(1.5)
        self.finish()


class S21End(EndCard):
    LINE='Different targets contribute to different responses, below one amygdala node.'

    def construct(self):
        self.add(lines('Different targets contribute to\ndifferent responses,\nbelow one amygdala node.',40).move_to([0,.4,0]),
                 T('biochemistrypedia.com',26,TEAL).move_to([0,-2.2,0]))
        self.finish()
