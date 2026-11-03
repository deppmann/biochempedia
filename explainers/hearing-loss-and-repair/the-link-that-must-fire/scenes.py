"""Chapter 2: word-aligned, explicitly schematic teaching animation.
COLOR MAP: BLUE inner hair cells, ribbon, vesicles, otoferlin, vector half A;
ORANGE vector half B; GREEN auditory nerve; WHITE calcium;
TEAL recordings; RED impaired release; YELLOW thresholds; GOLD restored function;
TEXT labels; GREY neutral structure. No molecular structures are drawn.
Models: C = fused-vesicle count * unit capacitance; I = g*p_open*driving_force.
Hill sensitivity comparison uses n=3.3, EC50=2.3 / 9.8 µM (prior draft's
Michalski 2017 Fig 7; https://elifesciences.org/articles/31013), normalized
to the same ceiling. Control is the heterozygous C2C/+ reference. S23 shows only the
sustained phase of C=C_fast+r*t, with r_treated/r_WT=.425 (35–50% midpoint).
All displayed plot amplitudes and time scales are schematic; the Hill
x axis is shown qualitatively from low to high calcium.
"""
import numpy as np
from bp_style import *
ORANGE = '#F29E4C'
PURPLE = '#B58CD9'

# Keep exact narration lengths, without accumulating the pipeline's 0.4 s tails.
# Avoid generating sync.log: the task permits only the named deliverables.
class TimedSpoken(SpokenScene):
    def at(self, phrase, lead=.2, nth=0):
        rest = self.t_of(phrase, nth) - lead - self.elapsed()
        if rest > .02:
            self.wait(rest)
    def finish(self):
        rest = self.narration_s - self.elapsed()
        if rest > 0:
            self.wait(rest)


def heading(s, color=TEXT):
    return T(s, 32, color, font=TITLE_FONT).move_to([0,3.15,0])


def label(s, x, y, color=TEXT, size=28):
    return T(s,size,color).move_to([x,y,0])


def arrow(a,b,color=TEXT):
    return Arrow(a,b,buff=.08,color=color,stroke_width=4,tip_length=.18)


def synapse():
    membrane=VGroup(Line([-5.7,-1.1,0],[5.7,-1.1,0],color=BLUE,stroke_width=6),
                    Line([-5.7,2.5,0],[-5.7,-1.1,0],color=BLUE),
                    Line([5.7,2.5,0],[5.7,-1.1,0],color=BLUE))
    rib=RoundedRectangle(width=.65,height=2.15,corner_radius=.13,color=BLUE,fill_opacity=.6).move_to([0,.55,0])
    ves=VGroup(*[Circle(radius=.24,color=BLUE,fill_opacity=.2).move_to([x,y,0])
        for x,y in [(-.85,1.55),(.85,1.55),(-.9,.5),(.9,.5),(-.65,-.65),(.65,-.65)]])
    channels=VGroup(*[Rectangle(width=.12,height=.6,color=WHITE,fill_opacity=.7).move_to([-1.6+d,-1.1,0]) for d in (-.16,.16)])
    nerve=RoundedRectangle(width=8.2,height=.75,corner_radius=.22,color=GREEN,fill_opacity=.18).move_to([0,-2.5,0])
    return VGroup(membrane,rib,ves,channels,nerve,
                  label('auditory nerve ending',0,-2.5,GREEN,28))


def fusion_question():
    # At the docking gap, with a short leader; no glyph sits on the membrane.
    return VGroup(label('?',1.65,-1.65,GOLD,38),Line([1.35,-1.45,0],[.65,-.99,0],color=GOLD))


def calcium():
    return VGroup(*[Dot([-1.6+d,-1.8,0],radius=.1,color=WHITE) for d in (-.14,.14)])


def cell(x=0,y=0,w=1,h=2):
    body=RoundedRectangle(width=w,height=h,corner_radius=.22,color=BLUE,fill_opacity=.08).move_to([x,y,0])
    hairs=VGroup(*[Line([x+d,y+h/2,0],[x+d,y+h/2+.3,0],color=BLUE,stroke_width=3) for d in (-w*.22,0,w*.22)])
    return VGroup(body,hairs)


def frame_axes(x,y,w=5.3,h=3.8):
    return Axes(x_range=[0,1,.5],y_range=[0,1,.5],x_length=w,y_length=h,
        axis_config={'color':TEXT,'include_ticks':False,'include_tip':False}).move_to([x,y,0])


def path(ax,xs,ys,color=TEAL):
    return VMobject(color=color,stroke_width=5).set_points_as_corners([ax.c2p(float(x),float(y)) for x,y in zip(xs,ys)])


def questions(reveal=False):
    a,b=frame_axes(-3.15,-.05),frame_axes(3.15,-.05)
    texts=VGroup(label('Calcium current',-3.15,2.25,TEAL),label('Capacitance',3.15,2.25,TEAL),
                 label('time →',-3.15,-2.25),label('time →',3.15,-2.25))
    qs=VGroup(label('?',-3.15,0,size=64),label('?',3.15,0,size=64))
    return VGroup(heading('After calcium enters: what should the recording show?'),a,b,texts,qs,
                  label('Pause and predict',0,-3.15,GOLD,30))


def suitcase(color=TEXT):
    box=RoundedRectangle(width=5,height=3.5,corner_radius=.2,color=color,stroke_width=4).move_to([0,-.15,0])
    handle=RoundedRectangle(width=1.25,height=.45,corner_radius=.1,color=color).move_to([0,1.83,0])
    return VGroup(box,handle)


def delivery():
    cs=VGroup(*[cell(-5.4+i*1.2,0,.85,3.6) for i in range(10)])
    marks=VGroup()
    for i in range(10):
        if i<7: marks.add(Rectangle(width=.23,height=1.7,color=BLUE,fill_opacity=.8).move_to([-5.56+i*1.2,-.3,0]))
        if i<5 or i in (7,8): marks.add(Rectangle(width=.23,height=1.7,color=ORANGE,fill_opacity=.8).move_to([-5.24+i*1.2,-.3,0]))
    legend=VGroup(chip('Half A',BLUE,28).move_to([-4.4,-2.55,0]),
                  chip('Half B',ORANGE,28).move_to([4.4,-2.55,0]))
    return VGroup(heading('Each vector: 70% · independent delivery'),cs,marks,legend,
                  label('Illustrative cells',0,-2.55),label('What fraction can make the protein?',0,-3.5,size=30))


class S00Title(TitleCard):
    LESSON='Hidden Hearing Loss, Gene Therapy and Regeneration'
    TITLE='The Link That Must Fire'
    def construct(self):
        self.add(label('BIOCHEMISTRYPEDIA',0,1.4,TEAL,28),
                 T(self.TITLE,48,font=TITLE_FONT).move_to([0,.2,0]),
                 Line([-1,-.7,0],[1,-.7,0],color=GOLD,stroke_width=4),
                 label('Otoferlin and the surviving hair cell',0,-1.5,size=30))
        self.wait(self.narration_s)


class S01(TimedSpoken):
    def construct(self):
        s=synapse(); self.add(s,heading('What turns the calcium signal into release?'),fusion_question())
        self.at('the calcium signal'); ca=calcium(); self.add(ca); self.play(ca.animate.shift(UP*1.6),run_time=.6)
        self.finish()


class S02(TimedSpoken):
    def construct(self):
        s=synapse(); self.add(s,heading('Inner hair cell'))
        self.at('depolarizes'); self.play(s[0].animate.set_stroke(GOLD),run_time=.4)
        self.at('calcium enters'); ca=calcium(); self.add(ca)
        self.play(s[3][0].animate.shift(LEFT*.12),s[3][1].animate.shift(RIGHT*.12),ca.animate.shift(UP*1.6),run_time=.6)
        self.add(label('calcium channels',-3.7,-.1,WHITE,26),Line([-2.5,-.3,0],[-1.8,-.9,0],color=WHITE))
        self.at('Something must turn'); self.play(FadeIn(label('Signal → ?',3,.7)),run_time=.4)
        self.at('vesicle fusion'); self.play(FadeIn(fusion_question()),run_time=.35)
        self.finish()


class S03(TimedSpoken):
    def construct(self):
        s=synapse(); self.add(s)
        self.at('The ribbon'); self.add(heading('Ribbon: supply, not trigger'),label('ribbon',3,1.6,BLUE),Line([2.1,1.5,0],[.4,1,0],color=BLUE))
        self.play(Indicate(s[1]),run_time=.5)
        self.at('larger resident pool')
        outer=VGroup(*[Circle(radius=.23,color=GOLD,fill_opacity=.18).move_to([x,y,0]) for x,y in [(-1.7,2),(-1.9,1),(-1.8,0),(1.7,2),(1.9,1),(1.8,0)]])
        self.play(FadeIn(outer),s[2].animate.set_color(GOLD),run_time=.65)
        self.add(label('resident',-3.8,1.15,GOLD,28),label('vesicle pool',-3.8,.55,GOLD,28),Line([-2.65,.3,0],[-2.05,.05,0],color=GOLD))
        self.finish()


class S04(TimedSpoken):
    def construct(self):
        gene=chip('OTOF gene',BLUE,36,pad=.35).move_to([-3.6,1.65,0]); self.add(gene,heading('A genetic clue'))
        self.at('Mutations in'); self.play(Create(Cross(gene[0],stroke_color=RED)),run_time=.4)
        self.at('cause deafness'); self.play(GrowArrow(arrow([-1.8,1.65,0],[1.7,1.65,0],RED)),FadeIn(label('Deafness',3.5,1.65,RED,36)),run_time=.5)
        p=VGroup(*[chip('C2',BLUE,34,pad=.35).move_to([-4.3+i*1.72,-.8,0]) for i in range(6)])
        self.at('and'); self.play(FadeIn(p),run_time=.45)
        self.at('carries'); self.add(label('Otoferlin · C2 domains',0,.3,BLUE,32))
        self.at('calcium'); self.play(FadeIn(label('C2 modules often bind calcium',0,-2.45,WHITE,32)),run_time=.45)
        self.finish()


class S05(TimedSpoken):
    def construct(self):
        c=cell(-2,-.3,4.3,4.9)
        self.add(c,heading('Roux and colleagues · 2006'),label('inner hair cell',-2,-3.15,BLUE),label('Otof-null mice',3,-1.3,RED,32))
        self.at('recorded from')
        pip=Polygon([5.3,2.4,0],[4.8,2.9,0],[.2,.4,0],color=TEXT,fill_opacity=.25)
        self.play(Create(pip),run_time=.65); self.add(label('recording pipette',3.8,1, size=26))
        self.finish()


class S06(TimedSpoken):
    def construct(self):
        ax=frame_axes(2,-.15,7.3,4.5)
        c=cell(-4.3,-.1,3.2,4.2); mem=Line([-5.7,-1.7,0],[-2.9,-1.7,0],color=BLUE,stroke_width=6)
        ves=VGroup(*[Circle(radius=.25,color=BLUE,fill_opacity=.2).move_to([-5.2+i*.85,-.7,0]) for i in range(3)])
        head=heading('Control: fusion increases capacitance')
        self.add(ax,c,mem,ves,head,label('Capacitance (relative)',2,2.55,TEAL),label('time →',5.15,-2.9,size=26),label('control cell',-4.3,2.5,BLUE,26))
        pulse=Line(ax.c2p(.18,0)+DOWN*.28,ax.c2p(.78,0)+DOWN*.28,color=WHITE,stroke_width=6)
        self.at('tracks how much'); self.add(pulse,label('depolarization',2,-3.35,WHITE,26)); self.remove(head); self.add(heading('Fused membrane → higher capacitance',TEAL))
        # C(t) is computed directly from the count of the three fusion events.
        steps=[.2,.45,.7]
        for i,t in enumerate(steps):
            xs=[0]+[z for e in steps[:i+1] for z in (e,e)]+[min(1,t+.22)]
            ys=[0]+[z for n in range(i+1) for z in (n*.25,(n+1)*.25)]+[(i+1)*.25]
            trace=path(ax,xs,ys)
            if i: self.remove(previous)
            self.play(Create(trace),ves[i].animate.move_to([-5.2+i*.85,-1.7,0]).set_opacity(0),run_time=.45)
            previous=trace
            self.add(Arc(radius=.25,start_angle=0,angle=PI,color=BLUE).move_to([-5.2+i*.85,-1.7,0]))
        self.finish()


class S07(TimedSpoken):
    def construct(self):
        q=questions(); self.add(q[0],q[1],q[2],q[3])
        self.at('after calcium enters'); self.play(Indicate(q[1],color=TEAL),run_time=.4)
        self.at('at fusion itself'); self.play(Indicate(q[2],color=TEAL),run_time=.4)
        self.at('what should'); self.play(FadeIn(q[4]),FadeIn(q[5]),run_time=.4); self.finish()


class S08Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(questions()); self.wait(5)


class S09(TimedSpoken):
    def construct(self):
        q=questions(); self.add(q[1],q[2],q[3],heading('Otof-null · at the age recorded'))
        self.at('Calcium current')
        xs=np.linspace(0,1,301); current=.8-.6*((xs>=.2)&(xs<=.75))
        self.play(Create(path(q[1],xs,current)),run_time=.6)
        self.add(label('inward calcium\ncurrent',-3.15,-.45,TEAL,26))
        self.at('ribbon morphogenesis'); rib=VGroup(synapse()[1],synapse()[2]).scale(.36).move_to([-1.9,-3.05,0])
        self.play(FadeIn(rib),FadeIn(label('ribbon intact',-4.2,-3.05,BLUE,26)),run_time=.4)
        self.add(Line([-3.05,-3.05,0],[-2.45,-3.05,0],color=BLUE))
        self.at('were preserved'); self.add(label('Preserved',-3.15,1.35,TEAL,28))
        self.at('Release was'); self.play(Create(path(q[2],[0,1],[.04,.04],RED)),FadeIn(label('release almost abolished',3.15,-2.7,RED,26)),run_time=.6)
        self.finish()


class S10(TimedSpoken):
    def construct(self):
        self.add(heading('A proposed sensing role'))
        box=DashedVMobject(RoundedRectangle(width=9.5,height=3.8,corner_radius=.2,color=BLUE),num_dashes=55).move_to([0,-.1,0])
        may=T('may',64,GOLD,slant=ITALIC).move_to([0,-.7,0])
        self.add(box,label('Otoferlin: sensor?',0,.65,BLUE,42),may)
        self.at('The word'); self.play(Indicate(may,color=GOLD),run_time=.7); self.finish()


class S11(TimedSpoken):
    def construct(self):
        a=RoundedRectangle(width=5.3,height=4.6,corner_radius=.2,color=BLUE).move_to([-3.1,-.15,0]); b=a.copy().set_color(TEXT).move_to([3.1,-.15,0]); self.add(a,heading('What does a knockout establish?'))
        self.at('is needed'); self.play(FadeIn(label('Needed',-3.1,-.15,BLUE,42)),run_time=.4)
        self.at('It does not'); self.play(Create(b),run_time=.4)
        self.at('is the sensor'); self.play(FadeIn(label('Is the sensor?',3.1,.5,size=32)),FadeIn(label('Not yet shown',3.1,-.8,RED,30)),run_time=.4); self.finish()


class S12(TimedSpoken):
    def construct(self):
        self.add(heading('Michalski and colleagues · 2017'))
        p=VGroup(*[chip('C2C' if i==2 else 'C2',BLUE,34,pad=.5).move_to([-3.8+(i%3)*3.8,.9-(i//3)*2.3,0]) for i in range(6)])
        # Three ions visibly TOUCH the top boundary of the tested domain.
        top=p[2][0].get_top()[1]
        ions=VGroup(*[Dot([3.8+d,top+.09,0],radius=.11,color=WHITE) for d in (-.5,0,.5)])
        self.add(p,ions,label('calcium bound',3.8,2.2,WHITE,26))
        self.at('A change'); self.play(p[2][0].animate.set_stroke(RED,width=5),run_time=.4)
        self.at('domain'); self.add(label('C2C changed',3.8,-.12,RED,30))
        self.at('reduced'); self.play(ions[0].animate.shift(UP*.6+LEFT*.4).set_opacity(0),ions[2].animate.shift(UP*.6+RIGHT*.4).set_opacity(0),run_time=.6)
        self.at('calcium binding'); self.add(label('Fewer calcium ions bound',0,-3.25,WHITE,28)); self.finish()


class S13(TimedSpoken):
    def construct(self):
        ax=Axes(x_range=[0,60,20],y_range=[0,1,.5],x_length=10.1,y_length=4.3,axis_config={'color':TEXT,'include_tip':False,'include_ticks':False}).move_to([-.4,.05,0])
        self.add(ax,heading('Calcium sensitivity of release'),label('low → high calcium',-.4,-2.95,size=28),label('Normalized release',-3.8,2.6,TEAL,26))
        for v in [.5,1]: self.add(label(str(v),*ax.c2p(0,v)[:2]+np.array([-.35,0]),size=26))
        xs=np.linspace(0,60,601)
        def hill(k): return xs**3.3/(k**3.3+xs**3.3)
        # Label each curve alongside its OWN point with a short leader, away from the ceiling.
        self.at('The calcium sensitivity'); self.play(Create(path(ax,xs,hill(2.3),BLUE)),run_time=.5)
        cl=label('Control',-4.2,.8,BLUE,28); self.add(cl,Line(cl.get_top()+UP*.1,ax.c2p(5,5**3.3/(2.3**3.3+5**3.3)),color=BLUE))
        self.at('release fell'); self.play(Create(path(ax,xs,hill(9.8),RED)),run_time=.5)
        kl=label('C2C knock-in',1.3,.75,RED,28); self.add(kl,Line(kl.get_top()+UP*.1,ax.c2p(30,30**3.3/(9.8**3.3+30**3.3)),color=RED))
        self.at('the only sensor'); box=DashedVMobject(RoundedRectangle(width=3.7,height=.8,corner_radius=.1,color=TEXT),num_dashes=28).move_to([3.6,-.85,0]); self.play(Create(box),FadeIn(label('another sensor?',3.6,-.85,size=26)),run_time=.4)
        self.add(label('Schematic Hill curves · right shift = less sensitivity',0,-3.5,size=26)); self.finish()


class S14(TimedSpoken):
    def construct(self):
        c=cell(0,-.15,11.5,4.9)
        ribs=VGroup(*[VGroup(RoundedRectangle(width=.45,height=1.1,corner_radius=.1,color=BLUE,fill_opacity=.3).move_to([x,-.7,0]),
            VGroup(*[Circle(radius=.19,color=BLUE).move_to([x+d,y,0]) for d,y in ((-.6,-.45),(-.6,-.9),(.6,-.45),(.6,-.9))])) for x in (-3.6,0,3.6)])
        ribs.set_opacity(.45); ribs[0].set_opacity(.16)
        self.add(c,ribs,heading('A living treatment target'),label('inner hair cell present',0,1.65,BLUE,32),
                 label('some ribbons already lost',-3.2,.45,size=26),
                 label('vesicles stuck · no fusion',2.5,.45,RED,26),
                 label('Release almost absent',0,-3.2,RED,32))
        # Vesicles remain clustered well above the basal membrane; no fusion.
        self.at('release almost nothing'); self.play(Indicate(ribs[1:],color=RED),run_time=.55); self.finish()


class S15(TimedSpoken):
    def construct(self):
        cs=VGroup(*[cell(x,-.65,1.5,3.5) for x in (-2.8,0,2.8)])
        self.add(cs,heading('Outer hair cells'))
        self.at('still amplify')
        # Separate endpoints and holds make the somatic motion plainly visible.
        for _ in range(2):
            self.play(*[c.animate.stretch(.72,1,about_edge=DOWN) for c in cs],run_time=.3)
            self.wait(.1)
            self.play(*[c.animate.stretch(1/.72,1,about_edge=DOWN) for c in cs],run_time=.3)
            self.wait(.1)
        self.at('early in life'); self.add(label('At least early in life',0,-3.15,size=28))
        self.at('own faint sounds')
        waves=VGroup(*[Arc(radius=r,start_angle=-PI/3,angle=2*PI/3,color=TEAL,arc_center=[4.1,.3,0]) for r in (.5,.85,1.2)])
        self.play(Create(waves),FadeIn(label('otoacoustic emissions present',0,2.5,TEAL,28)),run_time=.6)
        self.finish()


class S16(TimedSpoken):
    def construct(self):
        s=suitcase(); self.add(s,heading('The vector has a capacity limit'))
        self.at('A conventional'); self.play(FadeIn(label('AAV vector',0,-.15,size=40)),run_time=.4)
        self.at('carries about'); self.add(label('About 4.7–5 kb capacity',0,-2.85,size=32)); self.finish()


class S17(TimedSpoken):
    def construct(self):
        s=suitcase(); self.add(s,heading('OTOF is too large for one vector'),label('AAV · 4.7–5 kb capacity',0,-2.85,size=30))
        # Six-unit bar against five-unit internal width; left edges aligned.
        bar=Rectangle(width=6,height=.8,color=BLUE,fill_opacity=.6).move_to([.5,-.15,0])
        self.at('coding sequence'); self.play(GrowFromEdge(bar,LEFT),run_time=.5)
        self.at('is about'); self.add(label('OTOF: about 6 kb',0,1,BLUE,32))
        self.at('before a promoter'); self.add(label('Before adding a promoter',0,-1.3,size=28)); self.finish()


class S18(TimedSpoken):
    def construct(self):
        halves=VGroup(*[Rectangle(width=2.7,height=.65,color=c,fill_opacity=.65).move_to([x,1,0]) for x,c in ((-1.35,BLUE),(1.35,ORANGE))])
        self.add(halves,heading('Al-Moyed and colleagues · 2019'))
        self.at('split it'); self.play(halves[0].animate.move_to([-3.3,2.55,0]),halves[1].animate.move_to([3.3,2.55,0]),run_time=.4)
        bags=VGroup(*[suitcase(c).scale(.7).move_to([x,1,0]) for x,c in ((-3.3,BLUE),(3.3,ORANGE))])
        self.at('two vectors'); self.play(FadeIn(bags),run_time=.2)
        self.play(halves[0].animate.move_to([-3.3,.7,0]),halves[1].animate.move_to([3.3,.7,0]),run_time=.35)
        self.add(label('Half A',-3.3,1.6,BLUE,28),label('Half B',3.3,1.6,ORANGE,28))
        self.at('A cell receiving both'); target=cell(0,-1.9,10.4,1.7)
        opened=[]
        for bag,col in zip(bags,(BLUE,ORANGE)):
            b=bag[0]; l,r,t,bt=b.get_left()[0],b.get_right()[0],b.get_top()[1],b.get_bottom()[1]
            opened.append(VMobject(color=col,stroke_width=4).set_points_as_corners([[l,t,0],[l,bt,0],[r,bt,0],[r,t,0]]))
        self.play(FadeIn(target),ReplacementTransform(bags[0][0],opened[0]),ReplacementTransform(bags[1][0],opened[1]),bags[0][1].animate.shift(UP*.25),bags[1][1].animate.shift(UP*.25),run_time=.25)
        self.play(halves[0].animate.move_to([-1.5,-1.9,0]),halves[1].animate.move_to([1.5,-1.9,0]),run_time=.6)
        self.add(label('one cell receiving both',0,-3.3,BLUE,28))
        self.at('rebuild'); self.play(halves[0].animate.move_to([-1.35,-1.9,0]).set_color(GOLD).set_fill(GOLD,opacity=.16),halves[1].animate.move_to([1.35,-1.9,0]).set_color(GOLD).set_fill(GOLD,opacity=.16),run_time=.4)
        self.remove(halves)
        joined=Rectangle(width=5.4,height=.65,color=GOLD,fill_opacity=.16).move_to([0,-1.9,0])
        self.add(joined,label('full gene',0,-1.9,GOLD,28)); self.finish()


class S19(TimedSpoken):
    def construct(self):
        d=delivery(); self.add(*d[:5])
        self.at('what fraction'); self.play(FadeIn(d[5]),run_time=.4); self.finish()


class S20Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(delivery()); self.wait(5)


class S21(TimedSpoken):
    def construct(self):
        d=delivery(); self.add(*d[:5])
        self.at('About half'); self.play(*[d[1][i][0].animate.set_fill(GOLD,opacity=.6).set_stroke(GOLD) for i in range(5)],run_time=.4)
        self.at('needs both halves'); self.add(label('0.7 × 0.7 = 0.49 · both → can make protein',0,-3.5,GOLD,28)); self.finish()


class S22(TimedSpoken):
    def construct(self):
        cs=VGroup(*[cell(-4.75+i*1.9,-.1,1.3,4.2) for i in range(6)])
        self.add(cs,heading('Real mice · separate experimental evidence'))
        self.wait(2.5)
        self.play(*[cs[i][0].animate.set_fill(GOLD,opacity=.6) for i in range(3)],
                  FadeIn(label('Full-length otoferlin · up to 50%',0,-3,GOLD,32)),run_time=.4)
        self.finish()


class S23(TimedSpoken):
    def construct(self):
        head=heading('Fast release restored in transduced cells')
        ax=frame_axes(-.6,-.4,9.7,3.8)
        self.add(head,ax,label('Capacitance (relative)',-3,2.15,TEAL,28))
        initial_time=label('time during stimulation →',-.6,-2.75,size=28)
        self.add(initial_time)
        self.at('Fast release')
        # A normalized restored fast pool, with no WT amplitude comparison.
        fast=path(ax,[0,.18,.18,1],[.1,.1,.65,.65],GOLD)
        fast_label=label('Fast release returns',2.7,.8,GOLD,30)
        self.play(Create(fast),FadeIn(fast_label),run_time=.6)
        self.at('Vesicle replenishment')
        self.play(FadeOut(fast),FadeOut(fast_label),FadeOut(initial_time),
                  Transform(head,heading('Sustained phase · replenishment remains partial')),run_time=.25)
        self.add(label('time after fast release →',-.6,-2.75,size=28))
        t=np.linspace(0,1,201); wt=.1+.8*t; treated=.1+.8*.425*t
        self.play(Create(path(ax,t,wt,TEXT)),Create(path(ax,t,treated,GOLD)),
                  FadeIn(label('Wild type',4.7,1.5,TEXT,28)),FadeIn(label('Treated',4.7,-.3,GOLD,28)),run_time=.6)
        self.add(label('Replenishment: 35–50% of wild type',0,-3.4,GOLD,30),label('Slope comparison · normalized model',0,2.6,size=26)); self.finish()


class S24(TimedSpoken):
    def construct(self):
        self.add(heading('Click thresholds · treated mice'))
        # Quantified scale ONLY for the reported treated range; WT and deafness
        # have no measured values here, so keep them off the numerical axis.
        ax=NumberLine(x_range=[20,80,20],length=4.6,include_numbers=False,include_tip=False,color=TEXT).rotate(PI/2).move_to([-3.7,.1,0])
        self.add(ax,label('dB SPL',-5.25,1.65,size=28),label('untreated: deaf',2.8,2.35,RED,32),
                 label('no response / off scale',2.8,1.75,RED,26),
                 label('wild type: lower',2.8,-1.9,TEXT,30),label('(range not specified)',2.8,-2.5,size=26),
                 label('Partial rescue, not normal hearing',0,-3.35,GOLD,32))
        self.add(arrow([-.2,2.05,0],[-.2,2.75,0],RED),
                 DashedLine([-3.7,2.65,0],[.15,2.65,0],color=RED),
                 arrow([2.8,-.75,0],[2.8,-1.45,0],TEXT))
        for v in [20,40,60,80]: self.add(label(str(v),-4.45,ax.n2p(v)[1],size=28))
        self.at('Treated mice'); lo,hi=ax.n2p(40)[1],ax.n2p(60)[1]
        band=Rectangle(width=3,height=hi-lo,color=YELLOW,fill_opacity=.22).move_to([-2,(lo+hi)/2,0])
        self.play(FadeIn(band),run_time=.4)
        self.at('click thresholds'); self.add(label('40–60',-2,(lo+hi)/2,YELLOW,34),label('treated',1.3,.1,YELLOW,30))
        self.finish()


class S25(TimedSpoken):
    def construct(self):
        c=cell(0,-.25,11.9,5.15)
        left=chip('Calcium signal',WHITE,28,pad=.35).move_to([-3.7,-.5,0]); right=chip('Release',PURPLE,30,pad=.35).move_to([4,-.5,0])
        mid=DashedVMobject(RoundedRectangle(width=3.4,height=1.6,corner_radius=.15,color=RED),num_dashes=28).move_to([.2,-.5,0])
        missing=label('missing step',.2,-.5,RED,28)
        self.add(c,left,right,mid,missing,heading('Repair in a surviving inner hair cell'),
                 arrow([-2,-.5,0],[-1.6,-.5,0]),arrow([2,-.5,0],[2.8,-.5,0]))
        self.at('Replacing a missing link')
        restored=VGroup(RoundedRectangle(width=3.4,height=1.6,corner_radius=.15,color=GOLD,fill_opacity=.15).move_to([.2,-.5,0]),
                        label('otoferlin-',.2,-.2,GOLD,28),label('dependent step',.2,-.8,GOLD,28))
        self.wait(.65)
        self.play(FadeOut(mid),FadeOut(missing),FadeIn(restored),run_time=.4)
        self.at('can work'); self.add(label('needed for release',.2,-1.9,GOLD,28))
        self.at('are still alive'); self.play(FadeIn(label('The cells are still alive',0,1.35,BLUE,34)),run_time=.35); self.finish()


class S26End(EndCard):
    LINE='Replacing a missing link can work in surviving cells.'
    def construct(self):
        self.add(T('Replacing a missing link can work',40,font=TITLE_FONT).move_to([0,.55,0]),
                 T('in surviving cells.',40,font=TITLE_FONT).move_to([0,-.3,0]),
                 label('biochemistrypedia.com',0,-1.5,TEAL,28))
        self.wait(self.narration_s)
