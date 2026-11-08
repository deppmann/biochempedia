"""Opening the Package: qualitative experimental schematics; no invented data traces.
COLOR MAP: BLUE=sweet/identity; PURPLE=bitter; ORANGE=umami;
YELLOW=sodium/light/questions; GREEN=attraction/intact/accept;
RED=impaired/aversion/reject; GREY=structure/inactive; TEXT=labels.
Field positions and cell dots are schematic, not anatomical or measured data.
"""
from bp_style import *
from bp_style import SpokenScene as _SpokenScene
import numpy as np

PURPLE = '#B58CD9'
SWEET, BITTER, UMAMI, SODIUM = BLUE, PURPLE, '#F0A45B', YELLOW
MUTED = '#C7CDD8'


class SpokenScene(_SpokenScene):
    # Preserve word timing without writing an unrequested sync.log deliverable.
    def at(self, phrase, lead=.2, nth=0):
        rest = self.t_of(phrase, nth) - lead - self.elapsed()
        if rest > .02:
            self.wait(rest)


def label(s, x=0, y=0, size=28, color=TEXT):
    return T(s, size=size, color=color).move_to([x,y,0])


def header(s):
    return label(s, y=3.3, size=34)


def foot(s):
    return label(s, y=-3.35, size=26, color=MUTED)


def cross_at(p, r=.25):
    p=np.array(p)
    return VGroup(Line(p+[-r,-r,0],p+[r,r,0],color=RED,stroke_width=4),
                  Line(p+[-r,r,0],p+[r,-r,0],color=RED,stroke_width=4))


def mouse(x=0,y=0,scale=1):
    body=Ellipse(width=1.65,height=.85,color=MUTED,fill_opacity=.35)
    head=Circle(radius=.36,color=MUTED,fill_opacity=.45).move_to([.83,.16,0])
    ear=Circle(radius=.22,color=MUTED,fill_opacity=.6).move_to([.62,.49,0])
    eye=Dot([.98,.25,0],radius=.045,color=TEXT)
    nose=Dot([1.2,.1,0],radius=.06,color=TEXT)
    tail=VMobject(color=MUTED,stroke_width=4).set_points_smoothly([[-.78,0,0],[-1.2,-.2,0],[-1.65,.1,0]])
    return VGroup(body,head,ear,eye,nose,tail).scale(scale).move_to([x,y,0])


def cortex(fields=True):
    outline=Ellipse(width=10.5,height=4.8,color=MUTED,stroke_width=4,fill_opacity=.06).move_to([0,.1,0])
    patches=VGroup()
    for name,col,x,y in [('sweet',SWEET,-3,.7),('bitter',BITTER,-1,-.7),('umami',UMAMI,1,.7),('sodium',SODIUM,3,-.7)]:
        blob=Ellipse(width=1.85,height=1.25,color=col,fill_opacity=.3).move_to([x,y,0])
        patches.add(VGroup(blob,label(name,x,y,size=28,color=col)))
    return VGroup(outline,header('Insular cortex · schematic'),patches if fields else VGroup())


def light_field(x,y,col,name,lit=False):
    blob=Ellipse(width=2.1,height=1.0,color=col,fill_opacity=.65 if lit else .12).move_to([x,y,0])
    lamp=Line([x,y+1.65,0],[x,y+1.25,0],color=MUTED,stroke_width=10)
    beam=Polygon([x-.12,y+1.23,0],[x+.12,y+1.23,0],[x+.75,y+.5,0],[x-.75,y+.5,0],
                 color=YELLOW,fill_opacity=.8 if lit else 0,stroke_width=0)
    tag=label(name,x,y-.03,26,col)
    return VGroup(blob,lamp,beam,tag)


def trials(question=False):
    g=VGroup(header('Trained identity task'))
    for x,col,taste,answer,acol in [(-3,BITTER,'bitter','GO · respond',GREEN),(3,SWEET,'sweet','NO-GO · withhold',MUTED)]:
        box=RoundedRectangle(width=5.5,height=4.65,corner_radius=.2,color=col).move_to([x,.15,0])
        taste_m=chip(taste,col,size=34).move_to([x,1.5,0])
        arrow=Arrow([x,.85,0],[x,-.65,0],color=acol)
        result=label(answer,x,-1.3,30,acol)
        g.add(VGroup(box,taste_m,arrow,result))
    if question:
        g.add(label("Why set the task against the mouse's own preference?",y=-2.85,size=28,color=YELLOW))
    return g


def table(rows=3, rec='?', attraction='?', question=False):
    g=VGroup(header('Manipulation → two behavioural readouts'))
    g.add(label('Manipulation',-3.75,2.3,28),label('Trained recognition',.05,2.3,26),label('Attraction',4,2.3,28))
    labels=['Light on sweet field','Block either field','Silence amygdala']
    answers=[('—','Attraction'),('Impaired','—'),(rec,attraction)]
    colors=[(MUTED,GREEN),(RED,MUTED),(GREEN if rec!='?' else YELLOW,RED if attraction!='?' else YELLOW)]
    for i in range(rows):
        y=1.35-i*1.4
        row=VGroup(RoundedRectangle(width=12.1,height=1.25,corner_radius=.12,color=GREY,fill_opacity=.07).move_to([0,y,0]),
                   label(labels[i],-3.75,y,27),
                   label(answers[i][0],.05,y,32,colors[i][0]),
                   label(answers[i][1],4,y,32,colors[i][1]))
        if i==1:
            row[2].become(VGroup(label('Impaired → recovers',.05,y+.2,26,GREEN),label('on washout',.05,y-.25,26,MUTED)))
        if i==2:
            bundle=chip('package: identity + value',MUTED,size=26).move_to([.5,-2.65,0])
            # A sealed parcel: lid, folded flaps and a continuous gold tape seam.
            parcel=VGroup(Rectangle(width=1.35,height=.85,color=MUTED,fill_opacity=.12),
                          Line([-.675,.2,0],[.675,.2,0],color=MUTED),
                          Line([-.675,.425,0],[0,.2,0],color=MUTED),
                          Line([.675,.425,0],[0,.2,0],color=MUTED),
                          Line([0,.425,0],[0,-.425,0],color=GOLD,stroke_width=5)).move_to([-3.3,-2.65,0])
            row.add(VGroup(parcel,bundle))
        g.add(row)
    g.add(foot('What survives?' if question else 'in these mouse assays'))
    return g


def closed_package():
    box=RoundedRectangle(width=7.9,height=4.9,corner_radius=.15,color=MUTED,fill_opacity=.06).move_to([-.7,-.1,0])
    lid=Line([-4.65,2.35,0],[3.25,2.35,0],color=MUTED,stroke_width=7)
    name=label('package: identity + value',-.7,1.8,32)
    ident=chip('identity',BLUE,size=38).move_to([-.7,.55,0])
    value=VGroup(Arrow([-2,-.8,0],[.6,-.8,0],color=GREEN,stroke_width=7),label('value',-.7,-1.5,36,GREEN))
    return VGroup(box,lid,name,ident,value)


def projection():
    source=VGroup(Ellipse(width=4.5,height=4.75,color=MUTED,fill_opacity=.06).move_to([-3.7,0,0]),label('insular cortex',-3.7,2.65,28))
    s=chip('sweet field',SWEET,size=28).move_to([-3.7,1,0])
    b=chip('bitter field',BITTER,size=28).move_to([-3.7,-1,0])
    a=Ellipse(width=3.35,height=4.75,color=MUTED,fill_opacity=.1).move_to([3.7,0,0])
    dots=VGroup(Ellipse(width=1.6,height=1.25,color=SWEET,fill_opacity=.4).move_to([3.7,1,0]),Ellipse(width=1.6,height=1.25,color=BITTER,fill_opacity=.4).move_to([3.7,-1,0]))
    arrows=VGroup(Arrow(s.get_right(),dots[0].get_left(),color=SWEET,buff=.2),Arrow(b.get_right(),dots[1].get_left(),color=BITTER,buff=.2))
    return VGroup(source,s,b,a,dots,arrows,label('amygdala',3.7,2.65,28))


def salt_panel(x,depleted=False,drinking=False):
    box=RoundedRectangle(width=5.8,height=5.05,corner_radius=.2,color=GREY).move_to([x,-.05,0])
    name=label('Sodium depleted' if depleted else 'Normal',x,2.15,30,YELLOW if depleted else TEXT)
    bottle=VGroup(RoundedRectangle(width=.8,height=2.5,corner_radius=.12,color=SODIUM,fill_opacity=.18),
                 Line([-.4,-.8,0],[-.85,-1.05,0],color=MUTED,stroke_width=6)).move_to([x+1.65,.6,0])
    m=mouse(x-1.0 if depleted else x-.35,-.401125,1.15)
    if not depleted: m.flip(UP)
    if drinking: m.shift(RIGHT*.42075)
    action=label('drinks' if drinking else ('approaches' if depleted else 'turns away'),x,-1.5,28,GREEN if depleted else RED)
    # Qualitative before/after arrows on the same baseline, not numerical measurements.
    a=Arrow([x-1.9,-2,0],[x+1.9 if depleted else x-.75,-2,0],buff=0,color=GREEN,stroke_width=6)
    val=label('value · higher' if depleted else 'value · low',x,-2.85,27,GREEN)
    return VGroup(box,name,bottle,m,action,a,val)


def salt_comparison(drinking=True):
    return VGroup(header('Value changes with need'),salt_panel(-3.1),salt_panel(3.1,True,drinking),
                  label('salt',0,2.75,28,SODIUM),foot('behavioural assays · qualitative value comparison'))


class S00Title(TitleCard):
    LESSON='Taste from Tongue to Cortex'
    TITLE='Opening the Package'
    def construct(self):
        self.add(label('BIOCHEMISTRYPEDIA',y=1.7,size=26,color=TEAL),label(self.LESSON,y=.8,size=28,color=MUTED))
        self.play(FadeIn(label(self.TITLE,y=-.3,size=52)),Create(Line([-1.3,-1.2,0],[1.3,-1.2,0],color=GOLD)),run_time=.6)
        self.finish()


class S01Q(SpokenScene):
    def construct(self):
        c=cortex(False)
        p=VGroup(Ellipse(width=2.7,height=1.65,color=BLUE,fill_opacity=.3).move_to([-1,0,0]),label('taste field',-1,0,30,BLUE))
        q=label('Does a taste field in cortex do anything?',y=-2.85,size=32,color=YELLOW)
        self.add(c,p,q)
        self.at('can a mouse')
        self.play(Transform(q,label('Know the taste … but stop wanting it?',y=-2.85,size=32,color=YELLOW)),run_time=.35)
        self.finish()


class S02Fields(SpokenScene):
    def construct(self):
        c=cortex(); self.add(c[0],c[1],foot('anaesthetized mice · Chen and colleagues, 2011'))
        setup=label('Anaesthetized mice',y=.1,size=38,color=MUTED); self.add(setup)
        self.at('separate fields')
        self.play(Transform(setup,label('One reported map',y=-1.7,size=30,color=MUTED)),run_time=.2)
        # Each patch and its adjacent name arrive together on the named taste.
        for cue,p in zip(['sweet','bitter','umami','sodium'],c[2]):
            self.at(cue); self.play(FadeIn(p),run_time=.2)
        self.finish()


class S03Drive(SpokenScene):
    def construct(self):
        outline=Ellipse(width=10.8,height=4.45,color=MUTED,fill_opacity=.06).move_to([0,.3,0])
        s=light_field(-2.7,-.2,SWEET,'sweet field'); b=light_field(2.7,-.2,BITTER,'bitter field')
        self.add(header('Drive cortical taste fields'),outline,s,b,foot('awake mice · Peng and colleagues, 2015'))
        self.at('made the fields'); self.play(Indicate(s[1]),Indicate(b[1]),run_time=.4)
        self.at('respond to light')
        self.play(s[0].animate.set_fill(SWEET,opacity=.8),b[0].animate.set_fill(BITTER,opacity=.8),s[2].animate.set_fill(YELLOW,opacity=.8),b[2].animate.set_fill(YELLOW,opacity=.8),s[3].animate.set_color(BG),b[3].animate.set_color(BG),
                  FadeIn(VGroup(label('channelrhodopsin',y=-2.3,size=30,color=YELLOW),label('light-gated ion channel',y=-2.85,size=26,color=MUTED))),run_time=.4)
        self.finish()


class S04Value(SpokenScene):
    def construct(self):
        s=light_field(-3,1.2,SWEET,'sweet field'); b=light_field(3,1.2,BITTER,'bitter field')
        a=mouse(-4.5,-2.25,1.45); m=mouse(2.5,-.65,1.45).flip(UP)
        self.add(header('Value · approach or retreat'),s,b,a,m)
        self.at('light on the sweet')
        self.play(s[0].animate.set_fill(SWEET,opacity=.8),s[2].animate.set_fill(YELLOW,opacity=.85),s[3].animate.set_color(BG),run_time=.2)
        self.at('drove attraction')
        self.play(a.animate.move_to([-2.5,-.65,0]),FadeIn(label('approach',-3,-3.15,32,GREEN)),run_time=.75)
        self.at('light on the bitter')
        self.play(s[0].animate.set_fill(SWEET,opacity=.12),s[2].animate.set_fill(opacity=0),b[0].animate.set_fill(BITTER,opacity=.8),b[2].animate.set_fill(YELLOW,opacity=.85),s[3].animate.set_color(SWEET),b[3].animate.set_color(BG),FadeIn(label('retreat',3,-3.15,32,RED)),run_time=.2)
        self.at('drove aversion')
        self.play(m.animate.move_to([4.5,-2.25,0]),run_time=.75)
        self.finish()


class S05Task(SpokenScene):
    def construct(self):
        t=trials()
        # Readable previews avoid empty cards; each rule lights on its taste word.
        for card in t[1:]:
            card[2:].set_opacity(.45)
        self.add(t)
        self.at('bitter',lead=.1); self.play(t[1][2:].animate.set_opacity(1),run_time=.2)
        self.at('sweet',lead=.1); self.play(t[2][2:].animate.set_opacity(1),run_time=.2)
        self.finish()


class S06Q(SpokenScene):
    def construct(self):
        self.add(trials(True)); self.finish()


class S07Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(trials(True)); self.wait(3)


class S08Why(SpokenScene):
    def construct(self):
        t=trials(); self.add(t)
        self.at('cannot just follow')
        heart=label('♥',3,-2.75,42,SWEET)
        self.play(FadeIn(heart),Create(cross_at([3,-2.75,0],.35)),run_time=.3)
        self.at('learn a rule'); self.play(FadeIn(label('Loophole: a learned rule',-2.3,-2.75,28,YELLOW)),run_time=.3)
        self.at('respond to the unpleasant'); self.play(Indicate(t[1][3],color=YELLOW),run_time=.4)
        self.finish()


class S09Controls(SpokenScene):
    def construct(self):
        left=VGroup(RoundedRectangle(width=5.5,height=4.8,corner_radius=.2,color=SWEET).move_to([-3,.1,0]),chip('sweet',SWEET,size=34).move_to([-3,1.65,0]))
        right=VGroup(RoundedRectangle(width=5.5,height=4.8,corner_radius=.2,color=BITTER).move_to([3,.1,0]),chip('bitter',BITTER,size=34).move_to([3,1.65,0]))
        self.add(header('Control 1 · novel tastants'),left,right,label('Trained mice',y=-3,size=28,color=MUTED))
        self.at('new sweet'); self.play(FadeIn(label('new chemical',-3,.65,30,SWEET)),run_time=.25)
        self.at('bitter chemicals'); self.play(FadeIn(label('new chemical',3,.65,30,BITTER)),run_time=.25)
        self.at('similar accuracy')
        self.play(GrowArrow(Arrow([-3,.05,0],[-3,-1,0],color=GREEN)),GrowArrow(Arrow([3,.05,0],[3,-1,0],color=GREEN)),FadeIn(label('Similar accuracy',-3,-1.65,28,GREEN)),FadeIn(label('Similar accuracy',3,-1.65,28,GREEN)),run_time=.35)
        self.finish()


class S10Salt(SpokenScene):
    def construct(self):
        self.add(header('Control 2 · a taste the mouse likes'))
        bitter=chip('bitter',BITTER,size=38).move_to([-3,1.65,0]); salt=chip('low salt',SODIUM,size=38).move_to([3,1.65,0])
        self.add(bitter)
        self.at('low salt'); self.play(FadeIn(salt),run_time=.25)
        self.at('mice like'); self.play(FadeIn(label('attractive',3,.65,30,GREEN)),run_time=.25)
        self.at('shared the bitter answer')
        self.play(GrowArrow(Arrow([-3,.95,0],[-.85,-1.25,0],color=BITTER)),GrowArrow(Arrow([3,.2,0],[.85,-1.25,0],color=SODIUM)),FadeIn(chip('GO · respond',GREEN,size=38).move_to([0,-1.85,0])),FadeIn(foot('liking alone cannot solve this')),run_time=.45)
        self.finish()


class S11Block(SpokenScene):
    def construct(self):
        t=table(2); self.add(t)
        # The two icons make 'either field' explicit; only sweet is blocked in this example.
        s=VGroup(Dot([-4,-2.25,0],radius=.28,color=SWEET),label('sweet field',-4,-2.85,26,SWEET))
        b=VGroup(Dot([-1.4,-2.25,0],radius=.28,color=BITTER),label('bitter field',-1.4,-2.85,26,BITTER))
        status=label('normal',2.1,-2.4,30,GREEN)
        self.remove(t[-1]); self.add(s,b,status)
        t[5][2].become(label('Normal',.05,-.05,30,GREEN))
        self.at('blocking either field')
        x=cross_at([-4,-2.25,0],.37)
        self.play(Create(x),s[0].animate.set_opacity(.3),Transform(status,label('block one field',2.1,-2.4,28,RED)),run_time=.25)
        self.at('impaired recognition'); self.play(Transform(t[5][2],label('Impaired',.05,-.05,32,RED)),run_time=.25)
        self.at('recognition recovered')
        self.play(FadeOut(x),s[0].animate.set_opacity(1),Transform(status,label('washout → normal',2.1,-2.4,28,GREEN)),Transform(t[5][2],table(2)[5][2]),run_time=.4)
        self.finish()


class S12Dispute(SpokenScene):
    def construct(self):
        c=cortex(); self.add(c)
        rng=np.random.default_rng(17)
        # Reproducible scattered schematic cells; neither position nor radius is data.
        dots=VGroup(*[Dot([x+rng.uniform(-.55,.55),y+rng.uniform(-.35,.35),0],radius=rng.uniform(.10,.23),color=[SWEET,BITTER,UMAMI,SODIUM][i%4]) for i,(x,y) in enumerate(( (x,y) for y in [-1,.1,1.2] for x in [-3.2,-1.6,0,1.6,3.2]))])
        key=VGroup(*[VGroup(Square(side_length=.22,color=col,fill_opacity=1),label(name,size=26,color=col)).arrange(RIGHT,buff=.15) for name,col in [('sweet',SWEET),('bitter',BITTER),('umami',UMAMI),('sodium',SODIUM)]]).arrange(RIGHT,buff=.5).move_to([0,-3.45,0])
        self.at('alert licking mice'); self.play(FadeOut(c[2]),FadeIn(dots),run_time=.45)
        self.at('distributed responses')
        self.play(Indicate(dots,scale_factor=1.03),FadeIn(label('Map not settled',y=-2.55,size=30,color=YELLOW)),FadeIn(label('each dot = a cell · colour = preferred taste',y=-2.98,size=26,color=MUTED)),FadeIn(key),run_time=.4)
        self.add(label('alert, licking mice · 2021 · schematic',y=2.75,size=26,color=MUTED)); self.finish()


class S13Wang(SpokenScene):
    def construct(self):
        p=projection(); self.add(header('Cortex → amygdala'),p[0],p[1],p[2],p[3],p[6],foot('Wang and colleagues, 2018'))
        self.at('two fields'); self.play(FadeIn(p[4]),run_time=.3)
        self.at('different parts'); self.play(Create(p[5]),run_time=.4)
        self.finish()


class S14Silence(SpokenScene):
    def construct(self):
        p=projection(); self.add(header('Silence the amygdala'),p)
        self.at('silenced the amygdala')
        self.play(p[4].animate.set_color(GREY).set_opacity(.3),p[5].animate.set_color(GREY),p[3].animate.set_fill(GREY,opacity=.35),FadeIn(chip('silenced',RED,size=30).move_to([3.7,0,0])),run_time=.2)
        self.wait(2)
        self.play(FadeOut(Group(*self.mobjects)),FadeIn(table()),run_time=.25)
        # Closed package introduced before the later opening; a scope-bound metaphor.
        self.finish()


class S15Q(SpokenScene):
    def construct(self):
        t=table(question=True); self.add(t)
        self.at('what survives'); self.play(Indicate(t[-1],color=YELLOW),run_time=.25)
        self.at('recognizing the taste'); self.play(Indicate(t[6][2],color=YELLOW),run_time=.3)
        self.at('pull toward'); self.play(Indicate(t[6][3],color=YELLOW),run_time=.3)
        self.finish()


class S16Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(table(question=True)); self.wait(5)


class S17Reveal(SpokenScene):
    def construct(self):
        t=table(question=True); self.add(t)
        self.at('recognition stayed'); self.play(Transform(t[6][2],label('Intact',.05,-1.45,34,GREEN)),Transform(t[-1],foot('in these mouse assays')),run_time=.3)
        self.at('sweet and bitter correctly'); self.play(Indicate(t[6][2],color=GREEN),run_time=.35)
        self.at('was abolished'); self.play(Transform(t[6][3],label('Abolished',4,-1.45,34,RED)),run_time=.3)
        self.finish()


class S18Beat(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(table(rec='Intact',attraction='Abolished')); self.wait(3)


class S19Apart(SpokenScene):
    def construct(self):
        p=closed_package(); self.add(header('Opening the package'),p)
        self.at('pulled apart')
        self.play(p[1].animate.rotate(.07,about_point=[-4.65,2.35,0]),p[4].animate.shift(RIGHT*5.1),run_time=.5)
        self.at('in these assays'); self.play(FadeIn(foot('in these assays · with this silencing method')),run_time=.3)
        self.finish()


class S20Pattern(SpokenScene):
    def construct(self):
        self.add(header('A reusable experimental pattern'))
        boxes=VGroup(*[RoundedRectangle(width=11.2,height=1.2,corner_radius=.15,color=GREY,fill_opacity=.06).move_to([0,y,0]) for y in [1.95,.1,-1.75]])
        nums=VGroup(*[label(str(i+1),-5,y,30,YELLOW) for i,y in enumerate([1.95,.1,-1.75])])
        steps=VGroup(label('Intervene',y=1.95,size=32),label('Measure',y=.1,size=32),label('Compare',y=-1.75,size=32))
        self.add(boxes,nums,steps)
        self.at('manipulate one stage'); self.play(Transform(steps[0],label('Manipulate one stage',y=1.95,size=32)),run_time=.25)
        self.at('measure two')
        self.play(GrowArrow(Arrow([0,1.3,0],[0,.75,0],buff=0,color=MUTED)),Transform(steps[1],label('Measure two behaviours',y=.32,size=30)),FadeIn(label('recognition + attraction',y=-.12,size=30,color=MUTED)),run_time=.25)
        self.at('see which one moves')
        readouts=VGroup(label('recognition',-2,-2.02,30,BLUE),label('attraction',2,-2.02,30,GREEN))
        self.play(GrowArrow(Arrow([0,-.55,0],[0,-1.1,0],buff=0,color=MUTED)),Transform(steps[2],label('See which one moves',y=-1.48,size=30)),FadeIn(readouts),run_time=.25)
        self.play(readouts[1].animate.set_opacity(.45),run_time=.25)
        self.play(readouts[1].animate.set_opacity(1),run_time=.25)
        self.play(readouts[1].animate.set_opacity(.65),run_time=.25); self.finish()


class S21Need(SpokenScene):
    def construct(self):
        s=salt_comparison(False); self.add(s)
        self.at('changes with need'); self.play(s[1][3].animate.shift(LEFT*.45),run_time=.35)
        self.at('depleted animal'); self.play(Indicate(s[2][1],color=YELLOW),run_time=.3)
        self.at('drinks salt'); self.play(s[2][3].animate.shift(RIGHT*.42075),Transform(s[2][4],label('drinks',3.1,-1.5,28,GREEN)),run_time=.45)
        self.at('normally reject'); self.play(Indicate(s[1][4],color=RED),run_time=.35)
        self.finish()


class S22Same(SpokenScene):
    def construct(self):
        s=salt_comparison(); s[1][3].shift(LEFT*.45); self.add(s)
        self.at('salt is the same'); self.play(Indicate(s[3],color=SODIUM),run_time=.35)
        self.at('what changes'); self.play(Indicate(s[1][5],color=GREEN),Indicate(s[2][5],color=GREEN),run_time=.4)
        self.at('how much the animal'); self.play(Indicate(s[2][6],color=GREEN),run_time=.35)
        self.finish()


class S23Beat2(Scene):
    def construct(self):
        self.camera.background_color=BG; s=salt_comparison(); s[1][3].shift(LEFT*.45); self.add(s); self.wait(2)


class S24Scope(SpokenScene):
    def construct(self):
        card=RoundedRectangle(width=11.9,height=5.8,corner_radius=.2,color=GREY,fill_opacity=.07).move_to([0,-.1,0])
        self.add(header('Keep the scope'),card,label('Mouse assays',y=1.95,size=42,color=YELLOW))
        readouts=VGroup(chip('Recognition',BLUE,size=34).move_to([-2.6,-.1,0]),chip('Attraction',GREEN,size=34).move_to([2.6,-.1,0]),label('Two behavioural readouts',y=-1.65,size=32,color=MUTED))
        self.add(readouts)
        self.at('do not show')
        self.play(FadeOut(readouts),FadeIn(label('Value computed only',y=.65,size=42)),FadeIn(label('in the amygdala',y=-.15,size=42)),FadeIn(chip('?',YELLOW,size=40).move_to([5,-.15,0])),FadeIn(label('These assays do not show this.',y=-1.85,size=34,color=MUTED)),run_time=.4)
        self.finish()


class S25Brainstem(SpokenScene):
    def construct(self):
        fore=VGroup(Ellipse(width=4.25,height=1.45,color=GREY,fill_opacity=.08).move_to([-3.7,1.85,0]),label('forebrain disconnected',-3.7,1.85,26,MUTED))
        cut=DashedLine([-5.9,.8,0],[-1.5,.8,0],color=RED,stroke_width=4)
        stem=VGroup(RoundedRectangle(width=3.55,height=2.65,corner_radius=.35,color=YELLOW,fill_opacity=.15).move_to([-3.7,-.85,0]),label('brainstem',-3.7,-.85,34,YELLOW))
        accept=VGroup(Arrow([-1.8,-.3,0],[.4,-.1,0],color=GREEN),chip('accept',GREEN,size=34).move_to([1.65,-.1,0]))
        reject=VGroup(Arrow([-1.8,-1.2,0],[.4,-1.6,0],color=RED),chip('reject',RED,size=34).move_to([1.65,-1.6,0]))
        for output in [accept,reject]:
            output[0].set_opacity(.55)
            output[1][0].set_stroke(opacity=.55)
            output[1][1].set_opacity(.65)
        self.add(header('Decerebrate rats'),fore,cut,stem,accept,reject,foot('rats · taste-reactivity · Grill and Norgren, 1978'))
        self.at('brainstem circuits'); self.play(stem[0].animate.set_fill(YELLOW,opacity=.4),run_time=.3)
        self.at('innate acceptance'); self.play(accept[0].animate.set_opacity(1),accept[1][0].animate.set_stroke(opacity=1),accept[1][1].animate.set_opacity(1),run_time=.3)
        self.at('and rejection'); self.play(reject[0].animate.set_opacity(1),reject[1][0].animate.set_stroke(opacity=1),reject[1][1].animate.set_opacity(1),run_time=.3)
        self.at('learning shapes value')
        # Join the brainstem's behavioural outputs to value; learning is another input.
        outputs=VGroup(Line(accept[1].get_right(),[4.5,-.1,0],color=MUTED),Line(reject[1].get_right(),[4.5,-1.6,0],color=MUTED),Line([4.5,-1.6,0],[4.5,-.1,0],color=MUTED))
        self.play(Create(outputs),GrowArrow(Arrow([4.5,-.1,0],[4.5,1.6,0],buff=0,color=GREEN,stroke_width=6)),FadeIn(label('value',4.5,2.1,34,GREEN)),FadeIn(label('learning',.25,2.1,32,BLUE)),GrowArrow(Arrow([1.4,2.1,0],[3.55,2.1,0],buff=0,color=BLUE,stroke_width=6)),run_time=.45)
        self.finish()


class S26Take(SpokenScene):
    def construct(self):
        self.add(header('Two behavioural readouts'))
        before=VGroup(label('Before silencing',-3,2.2,30),chip('Recognition intact',GREEN,size=28).move_to([-3,1,0]),chip('Attraction present',GREEN,size=28).move_to([-3,-.1,0]))
        after=VGroup(label('Amygdala silenced',3,2.2,30),chip('Recognition intact',GREEN,size=28).move_to([3,1,0]),chip('Attraction abolished',RED,size=28).move_to([3,-.1,0]))
        self.add(before,after,Arrow([-.7,.5,0],[.7,.5,0],color=MUTED),label('in these mouse assays',y=-2.7,size=40,color=YELLOW))
        self.at('removed the attraction'); self.play(Indicate(after[2],color=RED),run_time=.35)
        self.at('spared trained recognition'); self.play(Indicate(after[1],color=GREEN),run_time=.35)
        self.finish()


class S27End(EndCard):
    LINE='In these mouse assays, silencing the amygdala removed attraction and spared trained recognition.'
    def construct(self):
        self.add(label('In these mouse assays,',y=1.35,size=36,color=YELLOW))
        statement=VGroup(T('silencing the amygdala removed attraction',size=36,font=TITLE_FONT),T('and spared trained recognition.',size=36,font=TITLE_FONT)).arrange(DOWN,buff=.3)
        self.play(FadeIn(statement),run_time=.4)
        self.play(FadeIn(label('biochemistrypedia.com',y=-1.6,size=26,color=TEAL)),run_time=.25); self.finish()
