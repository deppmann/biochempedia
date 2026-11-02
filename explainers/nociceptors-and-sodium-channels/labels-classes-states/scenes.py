"""Labels, Classes and States: revised visual explanations.
COLOR MAP: YELLOW molecular labels; TEXT conduction/control; TEAL functional
state/current; RED loss/lesion; GREY anatomy; GREEN measured current fraction.
Traces are computed, normalized illustrations, never presented as recordings.
"""
from bp_style import *
import numpy as np

TEAL_C = TEAL

def head(s):
    return T(s,34,font=TITLE_FONT).move_to([0,3.12,0])

def txt(s,x,y,size=28,col=TEXT):
    return T(s,size,col).move_to([x,y,0])

def cell(x,y,r=.5,color=YELLOW):
    return VGroup(Circle(r,color=color,fill_color=color,fill_opacity=.12).move_to([x,y,0]),Dot([x,y,0],radius=r*.22,color=color))

def arrow(a,b,col=GREY):
    return Arrow(a,b,buff=0,color=col,stroke_width=4,max_tip_length_to_length_ratio=.12)

def rulers():
    g=VGroup()
    for y,name,col in [(1.7,'molecular label',YELLOW),(-.2,'conduction class',TEXT),(-2.1,'functional state',TEAL_C)]:
        row=VGroup(txt(name,-3.95,y+.35,28,col),Line([-.9,y,0],[5.6,y,0],color=col,stroke_width=4))
        if y==1.7:
            for x,s in [(0,'CGRP'),(2.5,'Mrgprd'),(5,'CHRNA3')]:
                row.add(Line([x,y-.12,0],[x,y+.12,0],color=col),txt(s,x,y+.48,26,col))
        elif y==-.2:
            for x,s in [(-.7,'0.5'),(.6846,'5'),(2.2231,'10'),(5.3,'20 m/s')]:
                row.add(Line([x,y-.12,0],[x,y+.12,0],color=col),txt(s,x,y+.5,26,col))
        else:
            row.add(txt('silent',.1,y+.5,26,col),txt('responsive',4.4,y+.5,26,col))
            sw=RoundedRectangle(width=1.6,height=.55,corner_radius=.25,color=col,fill_color=BG,fill_opacity=1).move_to([2.2,y+.5,0])
            row.add(sw,Dot([1.75,y+.5,0],radius=.18,color=col))
        g.add(row)
    return g

def populations():
    outline=Ellipse(width=8.4,height=3.7,color=GREY).move_to([0,.45,0])
    left=VGroup(*[cell(x,y,.48) for x,y in [(-2.7,1.1),(-1.3,1.1),(-2,.0)]])
    right=VGroup(*[cell(x,y,.48) for x,y in [(1.3,1.1),(2.7,1.1),(2,0)]])
    labs=VGroup(txt('CGRP-positive',-3,-2,28,YELLOW),txt('peptidergic',-3,-2.5,28,YELLOW),txt('Mrgprd-positive',3,-2,28,YELLOW),txt('IB4 binding',3,-2.5,28,YELLOW),Line([-2,-1.3,0],[-3,-1.7,0],color=YELLOW),Line([2,-1.3,0],[3,-1.7,0],color=YELLOW))
    return VGroup(outline,left,right,labs,txt('dorsal root ganglion',0,2.65,28,GREY))

def follicle():
    hair=RoundedRectangle(width=.55,height=3.6,corner_radius=.2,color=GREY,fill_opacity=.2).move_to([-4,.1,0])
    skin=VGroup(Line([-6,1.1,0],[-4.4,1.1,0],color=GREY,stroke_width=8),Line([-3.6,1.1,0],[-2.1,1.1,0],color=GREY,stroke_width=8))
    wrap=VGroup(*[Arc(radius=.85,start_angle=.15,angle=5.8,color=YELLOW,stroke_width=5).stretch(.35,1).move_to([-4,y,0]) for y in [-1,-.35,.3]])
    axon=Line([-3.2,-1,0],[-2.2,-1.8,0],color=YELLOW,stroke_width=5)
    labels=VGroup(txt('hair follicle',-4,2.15,28,GREY),txt('circumferential',-4,-2.35,26,YELLOW),txt('ending',-4,-2.8,26,YELLOW),txt('axon',-1.9,-2.15,26,YELLOW))
    return VGroup(skin,hair,wrap,axon,labels)

def crossed_axes():
    # Crossed versions of the label and conduction rulers, fixed colors.
    g=VGroup(Line([-.7,-1.6,0],[5.8,-1.6,0],color=YELLOW,stroke_width=4),Line([.1,-1.8,0],[.1,1.9,0],color=TEXT,stroke_width=4))
    for y,s in [(-.9,'C'),(.85,'Aδ')]:
        g.add(Line([-.05,y,0],[.25,y,0],color=TEXT),txt(s,-.45,y,26))
    g.add(txt('conduction class',2.9,2.1,28),txt('molecular label',3,-2.5,28,YELLOW),txt('Calca',3.6,-2.05,28,YELLOW),Line([3.6,-1.45,0],[3.6,-1.75,0],color=YELLOW))
    g.add(DashedLine([.1,.85,0],[3.6,.85,0],color=GREY),DashedLine([3.6,-1.6,0],[3.6,.85,0],color=GREY),cell(3.6,.85,.23),txt('peptidergic',3.65,1.4,27,YELLOW))
    return g

# An explicit first-order illustrative response model: dI/dt=(drive-I)/tau,
# tau_on=.06, tau_off=.18, unit step indentation on [0.25,0.6].
# Normalized amplitudes are illustrative, not fitted physiology or recordings.
def current_trace(x,y,w,h,amplitude=0):
    ts=np.linspace(0,1,301)
    on=(ts>=.25)&(ts<.6)
    values=np.zeros_like(ts)
    for i in range(1,len(ts)):
        tau=.06 if on[i] else .18
        values[i]=values[i-1]+(float(on[i])-values[i-1])*(ts[i]-ts[i-1])/tau
    pts=[[x+w*t,y-h*amplitude*v,0] for t,v in zip(ts,values)]
    return VMobject(color=TEAL_C,stroke_width=4).set_points_as_corners(pts)

def culture(stage):
    # All conditions are spatially separate experiments, not a longitudinal cell.
    g=VGroup(head('CHRNA3-positive cultured somata'))
    for i,(x,name) in enumerate([(-4.3,'Untreated'),(0,'NGF 24 h'),(4.3,'NGF + PIEZO2 siRNA')]):
        card=RoundedRectangle(width=4.05,height=5.65,corner_radius=.14,color=TEAL_C if i==stage else GREY).move_to([x,-.25,0])
        soma=cell(x,.95,.65,GREY)
        probe=VGroup(Rectangle(width=.26,height=.9,color=TEXT,fill_color=TEXT,fill_opacity=1),Triangle(color=TEXT,fill_color=TEXT,fill_opacity=1).scale(.18).rotate(PI).shift(DOWN*.6)).rotate(-PI/2).move_to([x+1.15,.95,0])
        axis=VGroup(Line([x-1.3,-.5,0],[x+1.4,-.5,0],color=GREY),Line([x-1.3,-.4,0],[x-1.3,-1.8,0],color=GREY),txt('time (normalized)',x,-2.12,26),txt('0',x-1.55,-.5,26,GREY),txt('−1',x-1.6,-1.55,26,GREY),Line([x-1.4,-1.55,0],[x-1.2,-1.55,0],color=GREY),txt('1',x+1.35,-.17,26,GREY))
        curve=current_trace(x-1.3,-.5,2.7,1.05,1 if i==1 and stage>=1 else 0)
        note=['tiny response: 1 / 15','50 ng/ml NGF','no induced current'][i]
        row=VGroup(card,txt(name,x,2.25,26,TEAL_C if i==stage else TEXT),soma,probe,axis,curve,txt(note,x,-2.63,26,TEAL_C))
        # Keep future result unasserted; retain the three condition headings.
        if i>stage:
            row[2].set_opacity(.2); row[3].set_opacity(.2); row[4].set_opacity(.2); row[5].set_opacity(0); row[6].set_opacity(0)
        g.add(row)
    g.add(txt('Inward current ↓   •   normalized model illustration',0,-3.4,26,TEAL_C))
    return g

def hist_panel(x,name,after=False):
    box=RoundedRectangle(width=5.1,height=3.9,corner_radius=.1,color=GREY).move_to([x,.2,0])
    dots=VGroup(*[cell(x-1.7+(i%5)*.85,1.4-(i//5)*.8,.23,YELLOW) for i in range(20)])
    if after: dots.set_opacity(.05)
    return VGroup(box,txt(name,x,2.5,29),dots,txt('Mrgprd-positive somata',x,-2.25,26,YELLOW))

def matrix():
    g=VGroup(head('Functional dissociation in mice'))
    for x,s in [(1,'Mechanical'),(4.2,'Heat')]: g.add(txt(s,x,1.65,26))
    for y,s in [(.3,'Adult Mrgprd removal'),(-1.35,'TRPV1 central lesion')]: g.add(txt(s,-3.5,y,26,YELLOW))
    for x,y,s in [(1,.3,'threshold ↑'),(4.2,.3,'spared'),(1,-1.35,'unchanged'),(4.2,-1.35,'lost')]:
        box=RoundedRectangle(width=2.8,height=1.2,corner_radius=.1,color=GREY).move_to([x,y,0])
        g.add(VGroup(box,txt(s,x,y,26,RED if s in ['threshold ↑','lost'] else TEXT)))
    g.add(txt('Within the stimulus ranges tested',0,-2.8,27,GREY))
    return g

def timelines(reveal=False):
    g=VGroup(head('Same neurons. Different deletion times.'))
    for y,name,when in [(1.45,'Adult deletion',1.25),(-1.25,'Deletion from birth',-4.8)]:
        row=VGroup(txt(name,-3.5,y+.8,30,YELLOW),arrow([-4.8,y,0],[5.4,y,0]),txt('birth',-4.8,y-.45,26,GREY),txt('adult assay',4.5,y-.45,26,GREY),Line([when,y-.2,0],[when,y+.2,0],color=RED,stroke_width=6),txt('deletion',when,y+.45,26,RED))
        g.add(row)
    g.add(txt('mechanical threshold ↑',3.6,2.25,28),txt('threshold unchanged' if reveal else '?',3.4,-.45,30,TEAL_C))
    g.add(txt('No detectable mechanical deficit' if reveal else 'What happens after deletion from birth?',0,-2.95,30))
    return g

class S00Title(TitleCard):
    TITLE='Labels, Classes and States'
    LESSON='Nociceptors and the Sodium Channels of Pain'

class S01Question(SpokenScene):
    def construct(self):
        bins=VGroup()
        for x,name,col in [(-4.8,'Peptidergic',YELLOW),(-1.6,'Non-peptidergic',YELLOW),(1.6,'Aδ',TEXT),(4.8,'C',TEXT)]:
            b=RoundedRectangle(width=3,height=4.8,corner_radius=.15,color=col).move_to([x,-.1,0])
            bins.add(VGroup(b,txt(name,x,1.6,26,col),cell(x,.3,.6,col),cell(x,-1.3,.6,col)))
        self.add(head('What do the bins measure?'),bins)
        self.at('What are those'); self.play(ReplacementTransform(bins,rulers()),run_time=.8)
        self.finish()

class S02ThreeAxes(SpokenScene):
    def construct(self):
        r=rulers(); self.add(head('Three kinds of measurement'),r)
        for cue,i in [('molecular label',0),('conduction class',1),('functional state',2)]:
            self.at(cue); self.play(Circumscribe(r[i],color=[YELLOW,TEXT,TEAL_C][i]),run_time=.5)
        self.play(r[2][-1].animate.shift(RIGHT*.9),run_time=.4)
        self.finish()

class S03Label(SpokenScene):
    def construct(self):
        p=populations(); self.add(p)
        self.at('marks a population'); self.play(Circumscribe(p[1],color=YELLOW),run_time=.5)
        self.at('genetic access'); self.play(FadeIn(chip('gene marker → genetic access',YELLOW,28).move_to([0,-3.2,0])),run_time=.5)
        self.finish()

class S04Notfunction(SpokenScene):
    def construct(self):
        marker=VGroup(RoundedRectangle(width=3.8,height=3.1,corner_radius=.2,color=YELLOW,fill_color=YELLOW,fill_opacity=.12).move_to([-3.6,.45,0]),txt('CGRP',-3.6,.45,56,YELLOW),txt('a peptide marker',-3.6,-1.65,30,YELLOW))
        channel=VGroup(Line([1.6,.65,0],[3.1,.65,0],color=GREY,stroke_width=12),Line([4.1,.65,0],[5.6,.65,0],color=GREY,stroke_width=12),Line([3.1,-.95,0],[3.1,1.95,0],color=TEAL_C,stroke_width=10),Line([4.1,-.95,0],[4.1,1.95,0],color=TEAL_C,stroke_width=10))
        self.add(head('A marker does not specify a function'),marker,channel,txt('TRPV1: a heat channel',3.6,-1.65,28,TEAL_C),txt('Molecular label ≠ measured function',0,-2.9,32))
        self.at('not functions'); self.play(FadeIn(txt('≠',0,.4,86,RED)),run_time=.4)
        self.finish()

class S05Class(SpokenScene):
    def construct(self):
        self.add(head('Conduction class = measured velocity'))
        axon=VGroup(Line([-5.9,-.4,0],[5.9,-.4,0],color=GREY,stroke_width=10),Line([-5.9,-1.15,0],[5.9,-1.15,0],color=GREY,stroke_width=10))
        self.add(axon,txt('axon',-5.1,-.8,30,GREY))
        # Gaussian travelling voltage profile; x(t)=x0+v*t, v=3.6 m/s.
        t=ValueTracker(0)
        spike=always_redraw(lambda: VMobject(color=TEXT,stroke_width=6).set_points_as_corners([[x,-.35+1.3*np.exp(-((x-(-5.3+3.6*t.get_value()))/.28)**2),0] for x in np.linspace(-5.9,5.9,450)]))
        watch=VGroup(Circle(.8,color=TEXT),Line([0,0,0],[0,.63,0],color=TEXT)).move_to([-3.8,1.9,0])
        read=always_redraw(lambda: txt(f'{t.get_value():.2f}',-1.55,1.9,40))
        self.add(spike,watch,read,txt('s',-.5,1.9,34),txt('3.6 m/s',2.9,1.9,48))
        scale=VGroup(Line([-5,-2.25,0],[5,-2.25,0],color=GREY,stroke_width=4),txt('C: slower comparison',-3.5,-2.9,30),txt('Aδ: study mean',2.5,-2.9,30))
        for v in [.5,2,3.6,5]:
            x=-5+2*v
            scale.add(Line([x,-2.05,0],[x,-2.45,0],color=TEXT,stroke_width=4),txt(f'{v:g}' + (' m/s' if v==5 else ''),x,-1.75,32))
        self.add(scale,txt('mean of six recordings • Ghitani et al.',0,-3.5,28,GREY))
        self.at('is a velocity'); self.play(t.animate.set_value(2.9),Rotate(watch[1],angle=-2*PI,about_point=watch[0].get_center()),run_time=1.7,rate_func=linear)
        self.finish()

class S06Cross(SpokenScene):
    def construct(self):
        f=follicle(); a=crossed_axes(); self.add(head('One neuron, two measurements'),f,a)
        self.at('circumferential'); self.play(Circumscribe(f[2],color=YELLOW),run_time=.5)
        self.at('carried a peptidergic'); self.play(Circumscribe(a[-1],color=YELLOW),run_time=.5)
        self.finish()

class S07Calca(SpokenScene):
    def construct(self):
        self.add(head('Aδ AND peptidergic'),follicle(),crossed_axes())
        self.at('Their label encodes'); self.play(FadeIn(chip('Calca → alpha-CGRP',YELLOW,28).move_to([2.8,-3.25,0])),run_time=.4)
        self.at('The axes cross'); self.play(Circumscribe(self.mobjects[2][-2],color=YELLOW),run_time=.5)
        self.finish()

class S08State(SpokenScene):
    def construct(self):
        c=culture(0); self.add(c)
        self.at('can change'); self.play(c[1][3].animate.shift(LEFT*.3),c[1][2][0].animate.stretch(.85,0),run_time=.5)
        self.at('were mechanically silent'); self.play(Circumscribe(c[1][6],color=TEAL_C),run_time=.5)
        self.finish()

class S09Ngf(SpokenScene):
    def construct(self):
        c=culture(0); self.add(c)
        self.at('After a day'); n=culture(1); n[2][5].set_opacity(0); self.play(Transform(c,n),run_time=.5)
        self.at('mechanically activated'); self.play(c[2][3].animate.shift(LEFT*.3),c[2][2][0].animate.stretch(.85,0),run_time=.4)
        self.at('currents appeared'); self.play(Transform(c[2][5],culture(1)[2][5]),run_time=.6)
        self.finish()

class S10Piezo(SpokenScene):
    def construct(self):
        c=culture(1); self.add(c)
        self.at('Knockdown of'); n=culture(2); n[3][5].set_opacity(0); n[3][6].set_opacity(0); self.play(Transform(c,n),run_time=.5)
        self.at('prevented them'); self.play(c[3][3].animate.shift(LEFT*.3),c[3][2][0].animate.stretch(.85,0),Create(culture(2)[3][5]),FadeIn(culture(2)[3][6]),run_time=.6)
        self.finish()

class S11Limit(SpokenScene):
    def construct(self):
        dish=VGroup(RoundedRectangle(width=4.6,height=2.0,corner_radius=.3,color=GREY).move_to([-3.4,-.85,0]),Ellipse(width=4.6,height=.55,color=GREY).move_to([-3.4,.15,0]),cell(-3.4,-.85,.6,GREY))
        skin=VGroup(Rectangle(width=4.8,height=1.3,color=GREY,fill_opacity=.12).move_to([3.3,.9,0]),Line([3.3,-1.5,0],[3.3,.9,0],color=YELLOW,stroke_width=5),*[Line([3.3,.2,0],[x,1.1,0],color=YELLOW,stroke_width=5) for x in [1.9,2.6,4,4.7]])
        self.add(head('The measurement was in the soma'),dish,skin,txt('culture dish',-3.4,-2.2,30),txt('intact skin ending',3.3,2.1,30))
        self.at('a dish'); self.play(Create(Circle(.85,color=TEAL_C).move_to([-3.4,-.85,0])),run_time=.4)
        self.at('Neither result'); self.play(skin.animate.set_opacity(.25),FadeIn(chip('CAUTION: ending not tested',RED,27).move_to([3,-2.2,0])),run_time=.5)
        self.finish()

class S12Ablate(SpokenScene):
    def construct(self):
        boundary=Ellipse(width=5.6,height=3.8,color=GREY).move_to([-3.5,-.1,0])
        cells=VGroup(*[cell(x,y,.35) for x,y in [(-5,0),(-4,1),(-3,0),(-2,1),(-4,-1),(-2,-1)]])
        panel=hist_panel(3.4,'Histology',False); panel.shift(DOWN*.15)
        toxin=VGroup(Rectangle(width=1.2,height=.5,color=RED,fill_opacity=.3),Line([.6,0,0],[1.6,0,0],color=RED,stroke_width=4)).move_to([-5.2,2.1,0])
        self.add(head('Adult mice • diphtheria toxin'),boundary,cells,panel,toxin,txt('dorsal root ganglion',-3.5,-2.45,27,GREY))
        self.at('Now remove'); self.play(toxin.animate.shift(RIGHT*1.6),run_time=.5)
        self.at('a whole'); dose=Dot([-3.2,1.9,0],color=RED,radius=.15); self.add(dose); self.play(dose.animate.move_to([-3.5,0,0]),run_time=.45); self.play(cells.animate.set_opacity(.03),FadeOut(dose),run_time=.4); self.play(panel[2].animate.set_opacity(.03),Transform(panel[1],txt('Histology: after toxin',3.4,2.35,28)),run_time=.5)
        self.at('test behavior'); self.play(FadeIn(txt('Then test withdrawal behaviour',0,-3.25,30)),run_time=.4)
        self.finish()

class S13Control(SpokenScene):
    def construct(self):
        before=hist_panel(-3.2,'Before toxin'); after=hist_panel(3.2,'After toxin',True)
        self.add(head('Histology verifies population removal'),before,after)
        self.at('eliminated'); self.play(FadeIn(txt('>98% eliminated',3.2,.2,36,RED)),run_time=.5)
        self.at('of the'); self.play(FadeIn(txt('More than 98% of Mrgprd-positive cell bodies eliminated',0,-3.15,28,RED)),run_time=.5)
        self.finish()

class S14Mech(SpokenScene):
    def construct(self):
        self.add(head('After adult Mrgprd ablation'),txt('Within the stimulus ranges tested',0,-3.25,28,GREY),txt('withdrawal threshold • arbitrary units',0,2.35,28),txt('Qualitative comparison; heights are schematic',0,-2.85,26,GREY))
        self.add(Line([-5.8,-1.9,0],[5.8,-1.9,0],color=GREY),Line([-5.8,-1.9,0],[-5.8,1.65,0],color=GREY))
        bars=[]
        for x,name in [(-3.8,'Mechanical'),(0,'Heat'),(3.8,'Cold')]:
            self.add(txt(name,x,-2.2,28),txt('before',x-.55,1.7,26,GREY),txt('after',x+.65,1.7,26,RED))
            b=Rectangle(width=.75,height=1.5,color=GREY,fill_color=GREY,fill_opacity=.6).move_to([x-.55,-1.15,0]); a=Rectangle(width=.75,height=1.5,color=RED,fill_color=RED,fill_opacity=.6).move_to([x+.65,-1.15,0]); self.add(b,a); bars.append(a)
        self.at('Mechanical withdrawal'); self.play(bars[0].animate.stretch_to_fit_height(2.9).move_to([-3.15,-.45,0]),run_time=.6)
        self.at('heat and cold'); self.play(Circumscribe(VGroup(bars[1],bars[2]),color=TEXT),run_time=.5)
        self.finish()

class S15Heat(SpokenScene):
    def construct(self):
        self.add(head('Lesion defined by TRPV1 expression'))
        skin=Rectangle(width=2.2,height=1.1,color=GREY,fill_opacity=.15).move_to([-4.8,1.35,0])
        path=VGroup(Line([-4.8,1.25,0],[-4.8,.1,0],color=YELLOW,stroke_width=5),Line([-4.8,.1,0],[2.8,.1,0],color=YELLOW,stroke_width=5),Line([2.8,.1,0],[4.8,1.35,0],color=YELLOW,stroke_width=5),Line([2.8,.1,0],[4.8,-.55,0],color=YELLOW,stroke_width=5))
        branches=VGroup(*[Line([-4.8,.55,0],[x,1.55,0],color=YELLOW,stroke_width=4) for x in [-5.5,-4.1]])
        self.add(skin,path,branches,cell(-.8,.1,.6,GREY),txt('skin: heat transduction',-4.5,2.35,26),txt('central: transmission',3.9,2.35,26),txt('resiniferatoxin • pharmacological lesion',0,-3.6,26,GREY))
        self.add(arrow([-5.1,2.05,0],[-5.1,1.65,0],RED))
        lesion=RoundedRectangle(width=.55,height=2.1,corner_radius=.1,color=RED,fill_color=RED,fill_opacity=.35).move_to([3.7,.6,0])
        self.at('central branches'); self.play(FadeIn(lesion),run_time=.5)
        bars=VGroup()
        for x,name in [(-2.7,'Heat response'),(2.3,'Mechanical threshold')]:
            bars.add(txt(name,x,-1.12,30))
            for dx in [-.6,.6]: bars.add(Rectangle(width=.85,height=1.25,color=GREY,fill_color=GREY,fill_opacity=.7).move_to([x+dx,-2.12,0]))
        # The after slot is empty from its very first frame, rather than briefly
        # showing the pre-lesion response or a faint pink remnant.
        bars[2].set_fill(opacity=0).set_stroke(RED,width=3)
        zero=txt('0',-2.1,-2.12,32,RED)
        self.add(bars,zero,txt('before / after • schematic',0,-3.0,26,GREY))
        self.at('Noxious heat'); self.play(Circumscribe(VGroup(bars[2],zero),color=RED),run_time=.5)
        self.at('baseline mechanical'); self.play(Circumscribe(VGroup(bars[4],bars[5]),color=TEXT),run_time=.5)
        self.finish()

class S16Dissoc(SpokenScene):
    def construct(self):
        g=matrix(); self.add(g)
        self.at('functional dissociation'); self.play(Circumscribe(VGroup(*g[5:9]),color=GREY),run_time=.6)
        self.finish()

class S17Nothuman(SpokenScene):
    def construct(self):
        m=matrix(); m.remove(m[-1])
        for j in [1,2]: m[j].set_y(2.0)
        for j in [3,5,6]: m[j].set_y(1.0)
        for j in [4,7,8]: m[j].set_y(-.35)
        self.add(m,txt('Within the stimulus ranges tested',0,-1.55,26,GREY))
        for cue,s,y in [('not evidence','Every fibre is unimodal',-2.45),('nor that mouse','Mouse withdrawal = human pain',-3.35)]:
            c=txt(s,0,y,29); self.at(cue); self.play(FadeIn(c),run_time=.3); self.play(Create(Line(c.get_left()+DOWN*.19,c.get_right()+DOWN*.10,color=RED,stroke_width=2,stroke_opacity=.4)),run_time=.3)
        self.finish()

class S18Predict(SpokenScene):
    def construct(self):
        g=timelines(); self.add(g)
        self.at('Adult removal'); self.play(Circumscribe(g[3],color=TEXT),run_time=.5)
        self.at('Predict what happens'); self.play(Circumscribe(g[4],color=TEAL_C),run_time=.5)
        self.finish()

class S19Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(timelines()); self.wait(5)

class S20Reveal(SpokenScene):
    def construct(self):
        g=timelines(); self.add(g)
        self.at('Nothing detectable'); n=timelines(True); self.play(Transform(g[4],n[4]),Transform(g[5],n[5]),run_time=.5)
        self.at('later assays'); self.play(Transform(g[5],txt('The authors read this as compensation',0,-2.95,29,GREY)),run_time=.5)
        self.finish()

class S21Dev(SpokenScene):
    def construct(self):
        g=timelines(True); g[5].become(txt('The authors read this as compensation',0,-2.95,29,GREY)); self.add(g)
        self.at('germline deletion'); self.play(Circumscribe(g[2],color=TEAL_C),run_time=.5)
        self.at('adult manipulation'); self.play(Circumscribe(g[1],color=TEXT),Transform(g[5],txt('A germline deletion tests development',0,-2.95,30,TEAL_C)),run_time=.5)
        self.finish()

class S23Takeaway(SpokenScene):
    def construct(self):
        self.add(head('Channels → neurons → withdrawal reflexes'))
        pore=VGroup(Line([-5.8,.9,0],[-4.9,.9,0],color=GREY,stroke_width=10),Line([-4.1,.9,0],[-3.2,.9,0],color=GREY,stroke_width=10),Line([-4.9,.2,0],[-4.9,1.7,0],color=TEAL_C,stroke_width=8),Line([-4.1,.2,0],[-4.1,1.7,0],color=TEAL_C,stroke_width=8),txt('Channel',-4.5,-.5,30))
        neuron=VGroup(cell(0,1,.75,GREY),Line([.75,1,0],[1.6,.3,0],color=GREY,stroke_width=5),*[Line([-.6,1,0],[-1.5,y,0],color=GREY,stroke_width=4) for y in [.2,1,1.8]],txt('Neuron',0,-.5,30))
        paw=VGroup(Line([3.6,1.9,0],[4.2,1,0],color=TEXT,stroke_width=9),Line([4.2,1,0],[4.8,.65,0],color=TEXT,stroke_width=9),Ellipse(width=1.1,height=.45,color=TEXT).move_to([4.9,.65,0]),Line([3.2,-.05,0],[5.9,-.05,0],color=GREY),arrow([5.7,.35,0],[5.7,1.3,0],TEAL_C),txt('Withdrawal reflex',4.5,-.5,28))
        for icon in [pore,neuron,paw]:
            icon.scale(1.18,about_point=icon.get_center()).shift(DOWN*.25)
        # Full explanatory silhouette from the first frame; highlight each level on cue.
        silhouettes=[m.copy().set_opacity(.25) for m in [pore,neuron,paw]]
        self.add(*silhouettes,txt('Mouse and cellular experiments',0,2.4,28,GREY))
        for i,(cue,obj) in enumerate([('channels',pore),('neurons',neuron),('and reflexes',paw)]):
            self.at(cue); self.play(FadeOut(silhouettes[i]),FadeIn(obj),run_time=.35)
            if cue=='and reflexes': self.play(VGroup(*obj[:3]).animate.shift(UP*.35),run_time=.4)
        self.at("The lesson's surgical",lead=0)
        report=VGroup(RoundedRectangle(width=11.6,height=1.15,corner_radius=.2,color=TEXT).move_to([0,-1.8,0]),txt('Patient’s own report • surgical trials',0,-1.8,32))
        self.play(FadeIn(report),run_time=.5)
        self.at('Keep those levels'); self.play(FadeIn(txt('Pain is what the whole nervous system makes of them.',0,-3.1,32,TEAL_C)),run_time=.5)
        self.finish()

class S24End(EndCard):
    LINE='A label is not a function; deletion carries its timing.'
    def construct(self):
        line=VGroup(T('A label is not a function.',44,font=TITLE_FONT),T('A deletion carries its timing.',44,font=TITLE_FONT)).arrange(DOWN,buff=.55)
        self.play(FadeIn(line),run_time=.6)
        self.add(txt('biochemistrypedia.com',0,-2.2,26,TEAL_C)); self.finish()
