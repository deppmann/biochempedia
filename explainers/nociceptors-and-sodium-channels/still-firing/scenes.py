"""COLOR MAP: Nav1.7 orange; Nav1.8/current teal; Nav1.9 purple;
genetics yellow; drug/block red; residual green; control white; axes grey.
All response curves use I/Imax=1/(1+C/Kd). Spike illustrations use the
reference PCHIP model, not recorded data. Clinical estimates: lesson.mdx.
"""
from bp_style import *
from bp_style import SpokenScene as BaseSpokenScene
import numpy as np
from scipy.interpolate import PchipInterpolator
ORANGE='#F29E4C'
TEAL_C='#3FB8C0'
PURPLE='#B58CD9'
KD=.38

class SpokenScene(BaseSpokenScene):
    # Use real word onsets; do not modify the pipeline's sync.log.
    def at(self, phrase, lead=0, nth=0):
        rest=self.t_of(phrase,nth)-self.elapsed()-lead
        if rest>.02: self.wait(rest)

def lab(s,x=0,y=0,size=28,color=TEXT): return T(s,size,color).move_to([x,y,0])
def lines(ss,x=0,y=0,size=28,color=TEXT):
    return VGroup(*[T(s,size,color) for s in ss]).arrange(DOWN,buff=.18).move_to([x,y,0])
def head(s): return lab(s,0,3.12,32)
def box(s,x,y,color=GREY,size=28): return chip(s,color,size).move_to([x,y,0])
def arrow(a,b,color=GREY): return Arrow(a,b,buff=.08,color=color,stroke_width=3)
def frame(x=0,y=0,w=5.7,h=4.7): return RoundedRectangle(width=w,height=h,corner_radius=.15,color=GREY,stroke_width=2).move_to([x,y,0])
def frac(c,k=KD): return 1/(1+c/k)
def leader(text,x,y,point,color=TEXT,size=28):
    t=lab(text,x,y,size,color)
    return VGroup(t,Line(t.get_boundary_point(np.array(point)-t.get_center()),point,color=color,stroke_width=2))
def bracket(a,b,y,text,color=TEXT):
    return VGroup(Line([a,y,0],[b,y,0],color=color),Line([a,y-.12,0],[a,y+.12,0],color=color),Line([b,y-.12,0],[b,y+.12,0],color=color),lab(text,(a+b)/2,y+.38,28,color))
def person(x=0,y=0):
    return VGroup(Circle(.45,color=GREY).move_to([x,y+1.5,0]),RoundedRectangle(width=1.7,height=2.8,corner_radius=.3,color=GREY).move_to([x,y-.3,0]))
def curve_panel(small=False):
    ax=Axes(x_range=[-2,2,1],y_range=[0,1,.5],x_length=4.7 if small else 10.1,y_length=2.9 if small else 4.3,axis_config={'color':GREY,'include_tip':False,'stroke_width':2},tips=False).move_to([-3.3 if small else .3,.05 if small else -.25,0])
    ls=VGroup(*[lab(t,size=26).next_to(ax.c2p(x,0),DOWN,buff=.12) for x,t in [(-2,'.01'),(-1,'.1'),(0,'1'),(1,'10'),(2,'100')]],*[lab(str(v),size=26).next_to(ax.c2p(-2,v),LEFT,buff=.15) for v in [0,.5,1]])
    ax.y_axis.set_opacity(0)
    ls.add(Line(ax.c2p(-2,0),ax.c2p(-2,1),color=GREY,stroke_width=2))
    ls.add(lab('Concentration (nM, log scale)',-3.2 if small else .3,-3.15,26))
    if not small: ls.add(lab('Fraction of current remaining',-2.8,2.35,26,TEAL_C))
    cv=ax.plot(lambda z:frac(10**z),x_range=[-2,2,.015],color=TEAL_C,stroke_width=5,use_smoothing=False)
    return ax,ls,cv

def spike_fn(drug=False):
    pts=([(0,0),(.45,.02),(.62,.30),(.78,1),(.95,.74),(1.15,.46),(1.5,.40),(1.85,.02),(2.1,-.14),(2.6,0),(3,0)] if not drug else [(0,0),(.45,.02),(.62,.30),(.78,.68),(.95,.48),(1.15,.28),(1.5,.24),(1.85,0),(2.1,-.10),(2.6,0),(3,0)])
    return PchipInterpolator(*zip(*pts))
def train(x,y,w=5,h=2.1,n=5,drug=False,color=TEXT):
    t=np.linspace(0,15,1501); phase=np.mod(t,15/n)*3/(15/n)
    return VMobject(color=color,stroke_width=3).set_points_as_corners([[x-w/2+w*a/15,y+h*b,0] for a,b in zip(t,spike_fn(drug)(phase))])
def step(x,y,w=5):
    return VMobject(color=GREY,stroke_width=3).set_points_as_corners([[a,b,0] for a,b in [(x-w/2,y),(x-w/2+.3,y),(x-w/2+.3,y+.3),(x+w/2-.3,y+.3),(x+w/2-.3,y),(x+w/2,y)]])
def time_axis(x,y,w=5):
    return VGroup(Line([x-w/2,y,0],[x+w/2,y,0],color=GREY),lab('0',x-w/2,y-.25,26),lab('same time window',x,y-.3,26),lab('T',x+w/2,y-.25,26))
def prediction():
    ax,ls,cv=curve_panel(True); p=ax.c2p(1,frac(10))
    left=VGroup(ax,ls,cv,Dot(p,color=GREEN),lab('Recombinant current',-3.3,2.35,28,TEAL_C),bracket(p[0]-.15,p[0]+.15,p[1]+.25,'',GREEN),lines(['About 3.7% remains','at 10 nM'],-3.2,-2.35,26,GREEN))
    right=VGroup(frame(3.1,-.2,5.3,4.8),lines(['Predict:','silent, or still firing?'],3.1,1.25,30),box('Silent',3.1,-.3),box('Still firing',3.1,-1.4),lab('Pause the video to predict',3.1,-2.95,26,YELLOW))
    return left,right,head('What does a human neuron do?')

class S00Title(TitleCard):
    TITLE='Strong Nav1.8 Block, Still Firing'
    LESSON='Nociceptors and the Sodium Channels of Pain'
    def construct(self):
        self.add(lab('BIOCHEMISTRYPEDIA',0,2,28,TEAL_C),lines(['Strong Nav1.8 Block,','Still Firing'],0,.25,48),lab('Nociceptors and the Sodium Channels of Pain',0,-1.65,28))
        self.finish()
class S01Question(SpokenScene):
    def construct(self):
        ax=Axes(x_range=[0,3,1],y_range=[0,1,1],x_length=5,y_length=4.6,tips=False,axis_config={'include_ticks':False,'include_tip':False,'color':GREY}).move_to([-3.2,-.35,0])
        cv=ax.plot(lambda t:frac(10),x_range=[0,3,.02],color=TEAL_C,stroke_width=6)
        self.add(head('Does the neuron go quiet?'),ax,cv,lab('Few percent of current',-3.2,2.4,28,TEAL_C),train(3.2,-1.8,5.2,3.5,3),lab('Neuron firing?',3.2,2.4,30))
        self.at('Does the neuron'); self.play(Indicate(self.mobjects[-2],scale_factor=1.03),run_time=.6); self.finish()
class S02Obvious(SpokenScene):
    def construct(self):
        self.add(head('The obvious target'),box('human genetics',-3.6,2,YELLOW),arrow([-3.6,1.5,0],[-3.6,.7,0],YELLOW),box('Nav1.7',-3.6,0,ORANGE,40),arrow([-2.2,0,0],[4.4,0,0],ORANGE),lab('compound tested here',1,1,30),Line([4.5,-.8,0],[4.5,.8,0],color=RED,stroke_width=8))
        self.at('has not delivered'); self.play(FadeIn(lines(['This compound did not show','an effect in the trial'],1,-1.9,32,RED)),run_time=.4); self.finish()
class S03State(SpokenScene):
    def construct(self):
        self.add(head('PF-05089771 • same Nav1.7, two voltages'))
        def protocol(x,depol):
            pts=[[x-2,0,0],[x-1.5,0,0],[x-1.5,1.1 if depol else .15,0],[x+1.6,1.1 if depol else .15,0]]
            return VGroup(VMobject(color=ORANGE,stroke_width=5).set_points_as_corners(pts),lab('holding voltage',x,-.5,26),lab('Half-inactivated' if depol else 'Resting',x,1.65,30,ORANGE))
        left=protocol(-3.2,True); right=protocol(3.2,False)
        self.add(left,lab('Membrane voltage protocols (schematic)',0,2.4,26))
        self.at('far more potent'); self.play(FadeIn(box('11 nM',-3.2,-1.35,RED,32)),run_time=.4)
        self.at('than on resting ones'); self.play(Create(right),FadeIn(box('about 10 µM',3.2,-1.35,RED,32)),run_time=.65)
        self.add(lab('IC50 (log scale)',0,-1.35,26),Line([-4.8,-2,0],[4.8,-2,0],color=GREY),*[lab(t,x,-2.3,26) for x,t in [(-4.8,'10 nM'),(-1.6,'100 nM'),(1.6,'1 µM'),(4.8,'10 µM')]],Dot([-4.67,-2,0],color=RED),Dot([4.8,-2,0],color=RED))
        self.at('Nearly a thousand'); self.play(Create(bracket(-4.8,4.8,-3.35,'Nearly 1,000-fold',TEXT)),run_time=.65); self.finish()
class S05Notsel(SpokenScene):
    def construct(self):
        self.add(head('What changed?'),frame(-3.25,-.2),frame(3.25,-.2),lines(['Nav1.7','two holding voltages'],-3.25,.6,30,ORANGE))
        self.at('That is state dependence'); self.play(FadeIn(lab('State dependence',-3.25,-1.5,32)),run_time=.4)
        self.at('It is not selectivity'); self.play(FadeIn(lines(['Nav1.7 / Nav1.2','Selectivity across subtypes','is a different question'],3.25,0,28)),run_time=.5); self.finish()
class S06Margin(SpokenScene):
    def construct(self):
        self.add(head('A limited subtype margin'),lab('Relative concentration for block (log scale)',0,2.3,28),lab('Lower concentration = more potent',0,-3.05,28,ORANGE))
        ax=NumberLine(x_range=[0,2,1],length=10,include_tip=False,color=GREY).move_to([0,-.3,0])
        self.add(ax,*[lab(s,size=28).next_to(ax.n2p(v),DOWN,buff=.25) for v,s in [(0,'1×'),(1,'10×'),(2,'100×')]],Dot(ax.n2p(0),color=ORANGE,radius=.13),lab('Nav1.7',-5,1,32,ORANGE))
        self.at('only eleven'); p=ax.n2p(np.log10(11)); self.play(FadeIn(Dot(p,color=TEXT,radius=.13)),FadeIn(lab('Nav1.2',p[0],1,32)),Create(bracket(-5,p[0],-1.9,'11-fold',ORANGE)),run_time=.7); self.finish()
class S07Trial(SpokenScene):
    def construct(self):
        self.add(head('Painful diabetic neuropathy • week 4'),box('PF-05089771',-3,1.9,RED),box('Placebo',3,1.9),lab('135 participants',0,2.55,28))
        ax=NumberLine(x_range=[-1.2,.4,.2],length=10,include_numbers=False,include_tip=False,color=GREY).move_to([0,-.3,0]); p=ax.n2p
        self.add(ax,DashedLine(p(0)+DOWN*.55,p(0)+UP*.65,color=TEXT),lab('0',p(0)[0],-1.15,28),lab('Favours drug',-3.5,.6,28,ORANGE),lab('Favours placebo',3.5,.6,28),lines(['Difference in weekly average pain score','Drug minus placebo; lower = less pain'],0,-2.2,28),lab('Schematic estimate and uncertainty • ticks not to scale',0,-3.25,26,GREY))
        self.at('trial in painful'); self.play(Create(Line(p(-1),p(.17),color=ORANGE,stroke_width=8)),FadeIn(Dot(p(-.41),color=ORANGE,radius=.14)),run_time=.8); self.finish()
class S08Why(SpokenScene):
    def construct(self):
        self.add(head('Separate healthy-volunteer study'),lab('Proposed explanations',0,2.2,30),lab('?',0,.2,100,GREY))
        self.at('authors proposed'); self.play(FadeIn(box('insufficient dose',-3.6,.4,RED)),run_time=.4)
        self.at('and inadequate access'); self.play(FadeIn(lines(['inadequate access','to the central','nervous system'],3.6,.4,30,RED)),run_time=.5)
        self.at('Those are candidate causes'); self.play(FadeIn(lab('Candidates, not settled causes',0,-2.4,34)),run_time=.4); self.finish()
class S09Eight(SpokenScene):
    def construct(self):
        self.add(head('Nav1.8 • schematic channel'),Line([-6,-1.1,0],[6,-1.1,0],color=GREY,stroke_width=15),Line([-6,1,0],[6,1,0],color=GREY,stroke_width=15))
        walls=VGroup(*[Rectangle(width=.65,height=4.7,color=TEAL_C,fill_color=TEAL_C,fill_opacity=.55).move_to([x,-.2,0]) for x in [-.65,1.25]])
        vsd=Rectangle(width=1.1,height=2.1,color=TEAL_C,fill_color=TEAL_C,fill_opacity=.5).move_to([-2,-.1,0])
        self.add(walls,vsd,leader('Voltage-sensing domain 2',-3.4,-2.75,vsd.get_bottom(),TEAL_C,26),lab('Pore',.3,2.45,28,TEAL_C))
        self.at('binds a site away'); drug=box('suzetrigine',-4,1.9,RED); self.play(FadeIn(drug),GrowArrow(arrow([-3.5,1.55,0],[-2,.1,0],RED)),run_time=.6)
        self.add(lines(['Allosteric:','away from the pore'],4,-1.9,26,TEAL_C))
        self.at('stabilizes the closed state'); self.play(walls[0].animate.shift(RIGHT*.53),walls[1].animate.shift(LEFT*.53),Create(Line([.205,-.2,0],[.395,-.2,0],color=TEAL_C,stroke_width=6)),FadeIn(lab('Closed',3.9,.4,32,TEAL_C)),run_time=.8); self.finish()
class S10Panel(SpokenScene):
    def construct(self):
        self.add(head('Recombinant human subtype panel'),lab('At least 31,000-fold selectivity',0,2.4,30,TEAL_C),lab('Potency relative to Nav1.8 (log scale)',0,-3.3,28))
        ax=Axes(x_range=[0,6,1],y_range=[-5,0,1],x_length=10,y_length=4.2,tips=False,axis_config={'include_tip':False,'color':GREY}).move_to([.5,-.2,0])
        self.add(ax,*[lab(s,size=26).next_to(ax.c2p(0,v),LEFT,buff=.15) for v,s in [(0,'1'),(-2,'10⁻²'),(-4,'10⁻⁴'),(-5,'10⁻⁵')]])
        for i,(s,col) in enumerate([('1.2',GREY),('1.5',GREY),('1.7',ORANGE),('1.8',TEAL_C),('1.9',PURPLE)],1):
            top=0 if s=='1.8' else -np.log10(31000)
            self.add(Line(ax.c2p(i,-5),ax.c2p(i,top),color=col,stroke_width=24),lab(s,size=28,color=col).next_to(ax.c2p(i,-5),DOWN,buff=.15))
            if s!='1.8': self.add(Arrow(ax.c2p(i,top+.6),ax.c2p(i,top+.05),buff=0,color=col,max_tip_length_to_length_ratio=.4))
        self.add(lines(['Other subtypes:','↓ upper bounds'],-1.4,1.2,26)); self.finish()
class S11Notpatient(SpokenScene):
    def construct(self):
        self.add(head('Different levels of evidence'),frame(-3.5,-.2,5,5.1),lab('Recombinant cells',-3.5,2.1,30,TEAL_C))
        for x,y in [(-4.5,.5),(-2.5,.5),(-3.5,-1.1)]: self.add(RoundedRectangle(width=1.4,height=1.1,corner_radius=.3,color=TEAL_C).move_to([x,y,0]))
        self.add(person(3.5,-.35),lines(['Patient tissue','(not tested here)'],3.5,2.1,28))
        self.at('is not tissue selectivity'); self.play(FadeIn(lab('≠',0,0,68,RED)),run_time=.4); self.finish()
class S12Trials(SpokenScene):
    def construct(self):
        self.add(head('Two surgical trials'),box('Abdominoplasty',-3.2,2),box('Bunionectomy',3.2,2),lab('1,118 adults',-3.2,1.3,28),lab('1,073 adults',3.2,1.3,28))
        ax=Axes(x_range=[0,48,12],y_range=[0,5,1],x_length=10.3,y_length=2.5,tips=False,axis_config={'include_tip':False,'color':GREY,'include_ticks':False}).move_to([0,-.65,0])
        f=lambda t:1+2.4*(1-np.exp(-t/12))
        cv=ax.plot(f,x_range=[0,48,.3],color=TEAL_C,use_smoothing=False)
        self.add(ax,lab('0 h',-5.2,-2.3,26),lab('48 h',5.2,-2.3,26),lab('Pain-intensity difference',-2.7,.8,26,TEAL_C))
        self.at('summed each'); area=ax.get_area(cv,x_range=[0,48],color=TEAL_C,opacity=.25)
        self.play(FadeIn(area),Create(cv),*[FadeIn(Dot(ax.c2p(t,f(t)),color=TEXT,radius=.06)) for t in range(0,49,4)],run_time=.7)
        self.add(lines(['SPID48: sum of pain-intensity difference over 48 h','Shaded area summed • schematic ratings'],0,-2.95,26)); self.finish()
class S13Result(SpokenScene):
    def construct(self):
        self.add(head('Surgical trial outcomes'),lab('vs placebo',-.6,1.9,28),lines(['vs hydrocodone /','acetaminophen'],3.7,1.9,26),lab('Abdominoplasty',-4.3,.3,28),lab('Bunionectomy',-4.3,-1.5,28),Line([-6,1.15,0],[6,1.15,0],color=GREY),Line([-2.6,2.4,0],[-2.6,-2.2,0],color=GREY))
        self.at('beat placebo in both'); self.play(FadeIn(lines(['Superior','+48.4 point-hours'],-.5,.3,28,TEAL_C)),run_time=.35); self.play(FadeIn(lines(['Superior','+29.3 point-hours'],-.5,-1.5,28,TEAL_C)),run_time=.35)
        self.at('Neither trial demonstrated'); self.play(FadeIn(lines(['Superiority','not demonstrated'],3.8,.3,28)),run_time=.35); self.play(FadeIn(lines(['Superiority','not demonstrated'],3.8,-1.5,28)),run_time=.35); self.finish()
class S14Notequiv(SpokenScene):
    def construct(self):
        self.add(head('Not shown superior ≠ equivalent'),lab('Bunionectomy • prespecified comparator analysis',0,2.2,28))
        ax=NumberLine(x_range=[-10,40,10],length=10.5,include_tip=False,color=GREY).move_to([0,-.1,0]); p=ax.n2p
        self.add(ax,*[lab(str(v),size=26).next_to(p(v),DOWN,buff=.2) for v in [-10,0,10,20,30,40]],DashedLine(p(0)+DOWN*.5,p(0)+UP*.5),lab('Favours suzetrigine',-3.8,1,28,TEAL_C),lab('Favours opioid',3.5,1,28),lab('SPID48 difference (point-hours)',0,-1.6,28))
        self.at('ran the other way'); self.play(Create(Line(p(7.7),p(32.7),color=RED,stroke_width=8)),FadeIn(Dot(p(20.2),color=RED,radius=.13)),FadeIn(lab('20.2 point-hours; 95% CI 7.7 to 32.7',0,-2.7,30,RED)),run_time=.55); self.finish()
class S15Approval(SpokenScene):
    def construct(self):
        self.add(head('United States approval'),frame(-3.1,.1,5.1,4.1),lab('APPROVED',-3.1,-.1,42,TEAL_C),frame(3.1,.65,4.7,3),lab('JANUARY',3.1,1.55,30),lab('2025',3.1,.5,48),Line([1,.95,0],[5.2,.95,0],color=GREY))
        self.at('for moderate'); self.play(FadeIn(lines(['Moderate-to-severe acute pain','in adults'],0,-2.8,32)),run_time=.4); self.finish()
class S16Notcompare(SpokenScene):
    def construct(self):
        self.add(head('Different conditions, different endpoints'),frame(-3.5,-.1,5.2,4.8),frame(3.5,-.1,5.2,4.8),lines(['Nav1.7 blocker','Diabetic neuropathy'],-3.5,1.7,28,ORANGE),lines(['Nav1.8 blocker','Surgical pain'],3.5,1.7,28,TEAL_C))
        self.add(Line([-5.5,-.2,0],[-1.5,-.2,0],color=GREY),DashedLine([-2.7,-.8,0],[-2.7,.4,0],color=GREY),Line([-4.9,-.2,0],[-2.2,-.2,0],color=ORANGE,stroke_width=7),Dot([-3.8,-.2,0],color=ORANGE),lines(['Uncertainty crosses zero','Weekly average pain'],-3.5,-1.5,26),lines(['SPID48 vs placebo','Both intervals above zero'],3.5,-1.8,26,TEAL_C))
        # Same point-hour scale for the two surgical placebo comparisons.
        for y,lo,est,hi,name in [(.35,33.6,48.4,63.1,'Abdominoplasty'),(-.65,14,29.3,44.6,'Bunionectomy')]:
            px=lambda v:1.55+v/70*3.7
            self.add(Line([px(0),y,0],[px(70),y,0],color=GREY),Line([px(lo),y,0],[px(hi),y,0],color=TEAL_C,stroke_width=6),Dot([px(est),y,0],color=TEAL_C,radius=.08),lab(name,3.5,y+.36,26))
        self.at('not a comparison of targets'); self.play(FadeIn(lab('≠',0,0,64,RED)),FadeIn(lab('No direct comparison of targets',0,-3.05,30)),run_time=.4); self.finish()
class S17Fit(SpokenScene):
    def construct(self):
        ax,ls,cv=curve_panel(); self.add(head('Recombinant Nav1.8 • 37 °C'),ax,ls,lab('I(C) / Imax = 1 / (1 + C / Kd)',2.4,1.7,28,TEAL_C))
        self.at('Now the channel itself'); self.play(Create(cv),run_time=.8)
        p=ax.c2p(np.log10(KD),.5); q=ax.c2p(1,frac(10))
        self.at('model was fitted'); self.play(FadeIn(Dot(p,color=GREEN)),Create(DashedLine(ax.c2p(np.log10(KD),0),p,color=GREEN)),FadeIn(leader('Kd = 0.38 nM; 50%',2.5,.6,p,GREEN)),FadeIn(Dot(q,color=GREEN)),run_time=.6); self.finish()
class S18Temp(SpokenScene):
    def construct(self):
        ax,ls,cv=curve_panel(); self.add(head('37 °C versus 21 °C'),ax,ls,cv,lab('37 °C (body): 0.38 nM',2.9,2.1,28,TEAL_C))
        c2=ax.plot(lambda z:frac(10**z,.072),x_range=[-2,2,.015],color=TEXT,stroke_width=4,use_smoothing=False)
        p=ax.c2p(np.log10(.072),.5); q=ax.c2p(np.log10(KD),.5)
        self.at('The temperature'); self.play(Create(c2),FadeIn(lab('21 °C: 0.072 nM',3.3,1.35,28)),FadeIn(Dot(p,color=TEXT)),FadeIn(Dot(q,color=TEAL_C)),run_time=.7)
        self.at('by more than'); self.play(Create(VGroup(bracket(p[0],q[0],-.25,'',YELLOW),lab('5.28-fold',3.1,.45,30,YELLOW),Line([1.6,.45,0],[q[0],-.25,0],color=YELLOW))),run_time=.5); self.finish()
class S19Predict(SpokenScene):
    def construct(self):
        self.add(*prediction()); self.finish()
class S20Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(*prediction()); self.wait(5)
class S21Reveal(SpokenScene):
    def construct(self):
        self.add(head('Adult human sensory neurons • 37 °C'),lab('Control',-3.2,2.4,30),lab('10 nM suzetrigine',3.2,2.4,30,RED),step(-3.2,-2.15,5.5),step(3.2,-2.15,5.5),time_axis(-3.2,-1.25,5.5),time_axis(3.2,-1.25,5.5),lab('Injected current: same step',0,-2.65,26,GREY),lab('Typical, not universal • schematic model traces',0,-3.55,26))
        self.at('Generally it keeps firing'); self.play(Create(train(-3.2,-.6,5.5,2.2,5)),Create(train(3.2,-.6,5.5,2.2,3,True,RED)),run_time=.7)
        self.at('most tested neurons'); self.play(FadeIn(lab('Most tested neurons kept firing',0,-3.08,28,GREEN)),run_time=.4); self.finish()
class S22Shape(SpokenScene):
    def construct(self):
        ax=Axes(x_range=[0,3,1],y_range=[-.2,1,.2],x_length=10.1,y_length=4.5,tips=False,axis_config={'include_ticks':False,'include_tip':False,'color':GREY}).move_to([.4,-.2,0])
        c=ax.plot(spike_fn(),x_range=[0,3,.007],color=TEXT,stroke_width=5,use_smoothing=False); d=ax.plot(spike_fn(True),x_range=[0,3,.007],color=RED,stroke_width=5,use_smoothing=False)
        self.add(head('Spike shape • schematic model'),ax,c,lab('Membrane potential',-5.7,0,26).rotate(PI/2),lab('Time (arbitrary units)',.5,-3.15,26),leader('Control',2.8,1.8,ax.c2p(1.15,.46)),leader('Suzetrigine',3.7,.65,ax.c2p(1.5,.24),RED))
        self.at('The peak'); self.play(Create(d),run_time=.5)
        self.at('came down'); self.play(FadeIn(leader('Peak ↓',-2.7,2.25,ax.c2p(.78,.68),RED)),FadeIn(leader('Shoulder ↓',-.7,-1.2,ax.c2p(1.5,.24),RED)),run_time=.4)
        self.at('Threshold and the initial upstroke'); self.play(Create(Circle(.4,color=GREEN).move_to(ax.c2p(.55,.13))),FadeIn(lab('Threshold / initial upstroke largely spared',.3,-2.6,28,GREEN)),run_time=.45); self.finish()
class S23Reason1(SpokenScene):
    def construct(self):
        base=Rectangle(width=2.4,height=4.3,color=TEAL_C,fill_color=TEAL_C,fill_opacity=.55).move_to([-3.9,-.55,0]); rh=4.3*frac(10)
        residual=Rectangle(width=2.4,height=rh,color=GREEN,fill_color=GREEN,fill_opacity=1).move_to([-3.9,-2.7+rh/2,0])
        placeholder=lab('Residual, magnified',2.9,-1.2,28,GREEN)
        self.add(head('Reason 1 of 2 • a large starting current'),base,lines(['Large Nav1.8','control current'],-3.9,2.1,28,TEAL_C),frame(2.9,-.2,5.7,4.8),lines(['Near-complete block','can leave substantial current'],2.9,1.3,28),placeholder,lab('Schematic magnitude',-3.9,-3.05,26))
        self.at('current is very large'); self.play(Indicate(base,scale_factor=1.04),run_time=.6)
        self.at('block still leaves'); self.play(FadeIn(residual),base.animate.set_fill(opacity=.12),GrowArrow(arrow([-2.6,-2.5,0],[.5,-1,0],GREEN)),run_time=.5)
        self.at('nanoampere'); self.play(FadeOut(placeholder),FadeIn(Rectangle(width=3.4,height=.85,color=GREEN,fill_color=GREEN,fill_opacity=.6).move_to([2.9,-1.2,0])),FadeIn(lines(['Nanoampere-level','current remains'],2.9,.15,30,GREEN)),FadeIn(VGroup(lab('~3.7% at 10 nM (fit)',2.9,-2.05,26,GREEN),lab('Residual magnified',2.9,-3.05,26,GREEN))),run_time=.5); self.finish()
class S24Reason2(SpokenScene):
    def construct(self):
        self.add(head('Reason 2 of 2 • the initial spikes'),train(0,-.9,11.4,2.8,5),box('Nav1.8 blocker',3.3,2.3,RED,28),time_axis(0,-2.75,11.4),lab('Illustrative spike train • in these recordings',0,-3.5,26,GREY))
        self.at('And the other channel'); self.play(FadeIn(box('Nav1.7',-3.6,2.3,ORANGE,32)),run_time=.4)
        self.at('dominates the initial spikes'); self.play(Create(train(-3.42,-.9,4.56,2.8,2,color=ORANGE)),Create(bracket(-5.7,-1.14,-2.1,'Nav1.7-dominated',ORANGE)),run_time=.6); self.finish()
class S25Takeaway(SpokenScene):
    def construct(self):
        ax,ls,cv=curve_panel(True); mini=VGroup(ax,cv).scale(.6).move_to([-4.4,.1,0])
        self.add(head('Three separate measurements'),mini,train(0,-1,3.1,2.5,3),person(4.4,-.25),lab('Channel current',-4.4,-2.4,28,TEAL_C),lab('Neuron firing',0,-2.4,28),lab('Patient dose',4.4,-2.4,28),lab('≠',-2.2,0,60,RED),lab('≠',2.2,0,60,RED))
        self.at('certainly not a dose'); self.play(FadeIn(lab('A current calculation is not silence, nor a dose.',0,-3.25,30)),run_time=.4); self.finish()
class S26End(EndCard):
    LINE='A current calculation is not neuronal silence, nor a dose.'
    def construct(self):
        self.add(lines(['A current calculation is not','neuronal silence, nor a dose.'],0,.25,40),lab('biochemistrypedia.com',0,-1.5,28,TEAL_C)); self.finish()
