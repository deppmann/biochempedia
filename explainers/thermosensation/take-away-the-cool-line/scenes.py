"""Take Away the Cool Line: reviewer fix round.
COLOR MAP: cyan BLUE = TRPM8 / cool input; orange = warm input;
yellow = temperature stimulus; green = report / lick; red = loss / false alarm;
grey = apparatus and uncertainty. No molecular structures.
All rasters are seeded realizations of the reference film's illustrative rate
model (not recordings); steps use T(t)=32+delta*H(t-4).
"""
import numpy as np
from statistics import NormalDist
from bp_style import *

WARM, COOL, STIM, REPORT, GONE = '#F29E4C', BLUE, YELLOW, GREEN, RED
_BaseSpoken = SpokenScene
class SpokenScene(_BaseSpoken):
    # Same word timing as bp_style, without writing a non-deliverable sync.log.
    def at(self, phrase, lead=.2, nth=0):
        rest=self.t_of(phrase,nth)-lead-self.elapsed()
        if rest>.02: self.wait(rest)

def label(s,x=0,y=0,color=TEXT,size=28):
    return T(s,size=size,color=color).move_to([x,y,0])
def heading(s): return label(s,y=3.08,size=32)
def cross(p,r=.3):
    p=np.array(p)
    return VGroup(*[Line(p+[-r,a*r,0],p+[r,-a*r,0],color=GONE,stroke_width=6) for a in [-1,1]])
def arrow(a,b,c=GREY): return Arrow(a,b,buff=.14,color=c,stroke_width=5)
def rate_warm(t): return .7+5.3*min(1,max(0,(t-4)/2.5))
def rate_cool(t): return 3.5-3.2*min(1,max(0,(t-4)/2.5))
def spikes(rate,seed):
    t=np.arange(0,10,.002); cum=np.cumsum([rate(x) for x in t])*.002
    targets=np.arange(int(cum[-1]))+.5+np.random.default_rng(seed).uniform(-.3,.3,int(cum[-1]))
    return t[np.searchsorted(cum,targets)]
COOL_T=spikes(rate_cool,5); WARM_T=spikes(rate_warm,3)
REST_T=spikes(lambda t:3.5,5)

def raster(y=.5,warm=False,empty=False,x0=-5.5,x1=5.5,h=2.0,rest=False):
    times=REST_T if rest else WARM_T if warm else COOL_T
    axis=Line([x0,y-h/2,0],[x1,y-h/2,0],color=GREY,stroke_width=2)
    ticks=VGroup(*[Line([x0+t/10*(x1-x0),y-h/2+.1,0],[x0+t/10*(x1-x0),y+h/2,0],color=WARM if warm else COOL,stroke_width=4) for t in ([] if empty else times)])
    return VGroup(axis,ticks)
def warming_bar(y=-1.1,x0=-5.5,x1=5.5):
    start=x0+.4*(x1-x0)
    return VGroup(Rectangle(width=x1-start,height=.26,stroke_width=0,fill_color=STIM,fill_opacity=.7).move_to([(start+x1)/2,y,0]),label('warming',(start+x1)/2,y-.5,STIM,26))
def mouse(x=-3,y=.3,scale=1):
    g=VGroup(Ellipse(width=2.3,height=1.2,color=GREY,fill_opacity=.22).move_to([x-.5,y,0]),Ellipse(width=1.1,height=.85,color=GREY,fill_opacity=.3).move_to([x+.8,y+.2,0]),Circle(.23,color=GREY,fill_opacity=.3).move_to([x+.65,y+.68,0]),Dot([x+1.05,y+.35,0],radius=.055,color=TEXT),Line([x+.1,y-.3,0],[x+.55,y-1,0],color=GREY,stroke_width=10),Line([x+.8,y+.6,0],[x+.8,y+1.35,0],color=GREY,stroke_width=5),Line([x+.35,y+1.35,0],[x+1.25,y+1.35,0],color=GREY,stroke_width=5),Line([x+1.45,y+.05,0],[x+2,y+.05,0],color=GREY,stroke_width=6))
    return g.scale(scale,about_point=[x,y,0])
def step(x0,x1,y,delta=1,color=STIM,gain=1.1):
    return VMobject(color=color,stroke_width=5).set_points_as_corners([[x0+t/10*(x1-x0),y+gain*d,0] for t,d in [(0,0),(4,0),(4,delta),(10,delta)]])

def fibre():
    ending=RoundedRectangle(width=3,height=1.5,corner_radius=.65,color=COOL,fill_color=COOL,fill_opacity=.18).move_to([-3.7,1.55,0])
    ch=chip('TRPM8',COOL,30).move_to([-3.7,1.55,0])
    body=VGroup(ending,Line([-2.2,1.55,0],[5.5,1.55,0],color=COOL,stroke_width=9),label('cool fibre',2.2,2.2,COOL,32))
    r=raster(-.45,h=1.65,rest=True)
    return VGroup(body,ch,r,label('resting firing · illustrative raster',0,-1.75,COOL,26))
def scanner(scene,y=-.45,h=1.65):
    scan=Line([-5.5,y-h/2,0],[-5.5,y+h/2,0],color=TEXT,stroke_opacity=.35)
    scan.add_updater(lambda m: m.set_x(-5.5+(scene.renderer.time*.9)%11))
    scene.add(scan)
    return scan

def tally(h=80,f=20):
    g=VGroup()
    for y,n,col,name in [(1.65,h,REPORT,'Hits'),(-.35,f,GONE,'False alarms')]:
        base=Rectangle(width=7.6,height=.7,color=GREY,fill_opacity=.08).move_to([1,y,0])
        fill=Rectangle(width=7.6*n/100,height=.7,stroke_width=0,fill_color=col,fill_opacity=.8).align_to(base,LEFT).set_y(y)
        g.add(VGroup(label(name,-4.7,y,col,30),base,fill,label(f'{n} / 100',1,y+.7,col,28),label('0',-2.8,y-.7,GREY,26),label('100',4.8,y-.7,GREY,26)))
    return g
def constructed(mouse_name):
    return VGroup(label(mouse_name,-4.7,2.65,size=28),label('constructed example, not published data',1.25,3.12,GREY,26))

# Fixed row geometry keeps continuation scenes aligned; all labels >=26 pt.
YS=[1.45,.45,-.55,-1.55,-2.55]
def table_row(i,result=True):
    data=[('Wild type','present','reports 1 °C step',REPORT),('TRPM8 loss','lost','no report · failed completely\nafter 10 days',GONE),('TRPV1 loss','—','reports 1 °C · blunted',REPORT),('TRPM2 loss','—','threshold 2 °C · blunted',REPORT),('Triple heat loss','—','reports · less sensitive',REPORT)]
    a,b,c,col=data[i]; y=YS[i]
    names=VGroup(label(a,-4.5,y,COOL if i==1 else GREY if i==0 else WARM,26),label(b,-1.55,y,GONE if i==1 else GREY,26))
    res=VGroup(*[T(line,size=26,color=col) for line in c.split('\n')]).arrange(DOWN,buff=.13).move_to([2.65,y,0])
    rule=Line([-6.15,y-.53,0],[6.15,y-.53,0],color=GREY,stroke_opacity=.3)
    return VGroup(names,res if result else VGroup(),rule)
def table(n=1):
    g=VGroup(heading('Reports warming in this task?'),label('Condition',-4.5,2.4,GREY,26),label('Cool firing',-1.55,2.4,GREY,26),label('Warming report',2.65,2.4,GREY,26))
    for i in range(n+1): g.add(table_row(i))
    return g

def inputs():
    a=chip('cool-line fall ↓',COOL,32,pad=.35).move_to([-3.9,1.6,0])
    b=chip('warm-line rise ↑',WARM,32,pad=.35).move_to([-3.9,-1.6,0])
    box=RoundedRectangle(width=4.6,height=5.25,corner_radius=.2,color=GREY).move_to([3,.0,0])
    return VGroup(a,b,box,arrow([-1.6,1.6,0],[.65,1,0],COOL),arrow([-1.6,-1.6,0],[.65,-1,0],WARM),label('How they combine',3,1.7,TEXT,30),label('?',3,-.1,TEXT,76))

def preparations():
    left=VGroup(RoundedRectangle(width=5.1,height=5.25,corner_radius=.2,color=GREY).move_to([-3.7,-.15,0]),label('Isolated skin',-3.7,2.8,size=30),label('32 °C Peltier',-3.7,1.8,STIM,28),Rectangle(width=2.1,height=.4,color=STIM,fill_opacity=.4).move_to([-3.7,1.1,0]),Rectangle(width=3.6,height=.28,color=GREY,fill_opacity=.5).move_to([-3.7,.65,0]),label('skin',-3.7,.12,GREY,26),raster(-1.1,x0=-5.8,x1=-1.6,h=.85,rest=True),label('resting cool firing',-3.7,-1.98,COOL,26),label('27 °C bath',-3.7,-2.5,STIM,28))
    right=VGroup(RoundedRectangle(width=5.1,height=5.25,corner_radius=.2,color=GREY).move_to([3.7,-.15,0]),label('Behaving mouse',3.7,2.8,size=30),mouse(3.4,.45,.95),Rectangle(width=1.4,height=.42,color=STIM,fill_opacity=.45).move_to([3.92,-.7,0]),label('32 °C plate',3.7,-1.45,STIM,28),label('during the task',3.7,-2.25,GREY,26))
    return VGroup(left,right)

class S00Title(TitleCard):
    LESSON='Hot, Warm, Cool and Cold'
    TITLE='Take Away the Cool Line'
    def construct(self):
        title=T(self.TITLE,size=46,font=TITLE_FONT)
        fit(title,max_w=11.8)
        g=VGroup(label('BIOCHEMISTRYPEDIA',color=TEAL,size=26),label(self.LESSON.upper(),color=GREY,size=26),title,Line(LEFT*1.3,RIGHT*1.3,color=GOLD,stroke_width=4)).arrange(DOWN,buff=.4)
        self.play(FadeIn(g),run_time=.5); self.finish()

class S01Q(SpokenScene):
    def construct(self):
        r=raster(.6,h=2.6,rest=True)
        title=heading('Cool fibre'); note=label('illustrative raster',-3.3,-1.35,GREY,26)
        self.add(title,r,note)
        bar=warming_bar(-.98)
        self.at('warming quiets'); self.play(Transform(r,raster(.6,h=2.6)),FadeIn(bar),run_time=.5)
        q=label('What happens to warmth',0,-2.25,STIM,36)
        self.at('what happens'); self.play(FadeIn(q),run_time=.3)
        self.at('line is gone'); self.play(FadeOut(r),FadeOut(bar),FadeOut(note),FadeOut(title),q.animate.set_y(.55),FadeIn(label('when the cool line is gone?',0,-.55,size=36)),run_time=.35); self.finish()

class S02Task(SpokenScene):
    def construct(self):
        # Enlarge the apparatus together, including the paw/plate contact.
        m=mouse(-3,.35,1.4); p=Rectangle(width=1.6,height=.6,color=STIM,fill_opacity=.3).move_to([-2.23,-1.25,0])
        apparatus=VGroup(m,p).scale(1.3).move_to([-3.2,.25,0])
        spout=m[-1].get_end(); paw=m[4].get_end(); mount=m[6].get_center()
        self.add(heading('The reporting task'),m,label('head-fixed',-3.8,2.7,GREY,26),Line([-3.3,2.45,0],mount,color=GREY),label('lick spout',.3,1.7,GREY,26),Line([.3,1.4,0],spout,color=GREY))
        self.at('small plate'); self.play(FadeIn(p),FadeIn(label('8 × 8 mm',-4.3,-2.45,GREY,28)),run_time=.35)
        self.at('32 degrees'); self.play(FadeIn(label('32 °C baseline',-3.1,-2.95,STIM,28)),run_time=.35)
        axes=VGroup(Line([1.6,-1.4,0],[5.7,-1.4,0],color=GREY),Line([1.6,-1.4,0],[1.6,.7,0],color=GREY),label('32 °C',2.15,-1.95,STIM,26),label('+1 °C',4.6,.45,STIM,28),label('time →',4,-2.8,GREY,26))
        self.at('It licks'); self.play(FadeIn(axes),Create(step(1.8,5.65,-1.05)),run_time=.45)
        lick=Line(spout+LEFT*.6,spout+LEFT*.08,color=REPORT,stroke_width=9)
        self.play(Create(lick),FadeIn(label('lick → report',3.7,1.25,REPORT,30)),run_time=.35); self.finish()

class S03Steps(SpokenScene):
    def construct(self):
        self.add(heading('Trained mice'),label('warming group',-3.35,2.2,STIM,30),step(-5.7,-.9,-.4,gain=1.9),label('32 °C',-4.8,-1.05,GREY,26),label('33 °C',-1.8,1.75,STIM,26),label('time →',-3.3,-2.1,GREY,26))
        self.at('reported'); self.play(FadeIn(label('1 °C reported',-3.3,-2.95,REPORT,32)),run_time=.3)
        self.at('warming step'); self.play(FadeIn(VGroup(label('separate cooling group',3.35,2.2,COOL,26),step(.9,5.7,.7,-.5,COOL,gain=1.9),label('32 °C',1.7,1.35,GREY,26),label('31.5 °C',4.8,-.85,COOL,26),label('time →',3.3,-2.1,GREY,26),label('0.5 °C reported',3.3,-2.95,REPORT,32))),run_time=.4); self.finish()

class S04Catch(SpokenScene):
    def construct(self):
        xs=[-4.65,-1.55,1.55,4.65]
        self.add(heading('Licking on every trial'))
        for i,x in enumerate(xs):
            self.add(step(x-1.1,x+1.1,.7,.6 if i%2==0 else 0),label('warming' if i%2==0 else 'no change',x,1.95,STIM if i%2==0 else GREY,26))
        count=label('Licks counted: 0',0,-1.65,REPORT,34)
        self.add(count,label('A tally alone cannot establish detection',0,-2.95,GREY,28))
        self.at('licked on every')
        for i,x in enumerate(xs):
            self.play(GrowFromCenter(Dot([x,-.25,0],radius=.16,color=REPORT)),Transform(count,label(f'Licks counted: {i+1}',0,-1.65,REPORT,34)),run_time=.25)
        self.at('score hits'); self.play(FadeIn(label('2 hits + 2 licks on flat trials',0,-2.35,REPORT,28)),run_time=.3)
        self.at('without detecting'); self.play(Indicate(count),run_time=.4); self.finish()

class S05Catch2(SpokenScene):
    def construct(self):
        self.add(heading('Warming trials and catch trials'),label('warming',-4.8,1.45,STIM,28))
        xs=[-2,1,4]
        for x in xs: self.add(step(x-.9,x+.9,1.1,.5),Dot([x,.5,0],radius=.13,color=REPORT))
        self.at('catch trials'); self.play(FadeIn(label('catch',-4.8,-1.05,GREY,28)),FadeIn(VGroup(*[step(x-.9,x+.9,-.9,0) for x in xs])),run_time=.4)
        self.at('no temperature change'); self.play(FadeIn(label('no temperature change',1,-.3,GREY,28)),run_time=.35)
        dots=VGroup(*[Dot([x,-1.5,0],radius=.15,color=GONE) for x in xs])
        self.at('A lick'); self.play(FadeIn(dots),FadeIn(VGroup(*[label('false alarm',x,-2.3,GONE,26) for x in xs])),run_time=.35)
        self.at('false alarm'); self.play(Indicate(dots,color=GONE,scale_factor=1.15),run_time=.4); self.finish()

class S06Dprime(SpokenScene):
    def construct(self):
        self.add(tally(),constructed('mouse A'))
        self.at('compares the two'); self.play(FadeIn(T('d′ = z(hit rate) − z(false-alarm rate)',size=26).move_to([0,-1.95,0])),run_time=.4)
        self.at('separates detection'); value=NormalDist().inv_cdf(.8)-NormalDist().inv_cdf(.2)
        self.play(FadeIn(label(f'd′ ≈ {value:.2f}',0,-2.95,REPORT,42)),run_time=.4); self.finish()
class S07Zero(SpokenScene):
    def construct(self):
        self.add(tally(80,80),constructed('mouse B'))
        self.at('near zero'); self.play(FadeIn(label('d′ ≈ 0',0,-1.95,GONE,42)),FadeIn(label('licking, not detecting',0,-2.95,GONE,30)),run_time=.4); self.finish()
class S08Beat(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(tally(80,80),constructed('mouse B'),label('d′ ≈ 0',0,-1.95,GONE,42),label('licking, not detecting',0,-2.95,GONE,30)); self.wait(2.5)
class S09Knock(SpokenScene):
    def construct(self):
        f=fibre(); self.add(f); scanner(self)
        self.at('the knockouts'); self.play(Indicate(f[1],color=COOL),run_time=.4)
        self.at('response to cooling'); self.play(ShowPassingFlash(f[0][1].copy().set_stroke(COOL,15)),FadeIn(label('cooling response',0,-2.9,COOL,34)),run_time=.6); self.finish()
class S10Predict(SpokenScene):
    def construct(self):
        f=fibre(); self.add(f); scanner(self)
        self.at('Remove it'); self.play(f[1].animate.set_opacity(.3),Create(cross([-5.6,1.55,0])),run_time=.35)
        self.at('resting firing'); self.play(FadeIn(label('Resting firing?',-3,-2.75,COOL,32)),run_time=.3)
        self.at('report warming'); self.play(FadeIn(label('Reports of warming?',2.9,-2.75,STIM,32)),run_time=.3); self.finish()
class S11Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; f=fibre(); f[1].set_opacity(.3)
        self.add(f,cross([-5.6,1.55,0]),label('Pause: predict',0,3.12,size=32),label('Resting firing?',-3,-2.75,COOL,32),label('Reports of warming?',2.9,-2.75,STIM,32)); scanner(self)
        bar=Line([-5.5,-3.4,0],[-5.49,-3.4,0],color=GREY,stroke_width=5); self.add(bar)
        self.play(Transform(bar,Line([-5.5,-3.4,0],[5.5,-3.4,0],color=GREY,stroke_width=5)),run_time=5,rate_func=linear)
class S12Reveal1(SpokenScene):
    def construct(self):
        r=raster(.45,h=2.7,rest=True)
        self.add(heading('Without TRPM8'),r,label('illustrative raster',-3.8,-2.35,GREY,26))
        self.at('lose their ongoing'); self.play(LaggedStart(*[FadeOut(t) for t in r[1]],lag_ratio=.015),FadeIn(label('ongoing firing lost',0,2.25,GONE,30)),run_time=.7)
        self.at('Warming',lead=0); self.play(FadeIn(warming_bar(-1.35)),run_time=.3)
        self.at('nothing left'); self.play(FadeIn(label('nothing left to silence',0,.4,GONE,36)),run_time=.3); self.finish()
class S13Reveal2(SpokenScene):
    def construct(self):
        t=table(1); result=t[-1][1]; t.remove(t[-1]); row=table_row(1,False)
        self.add(t,row,label('Failure alone does not identify the cause',0,-1.35,GREY,28))
        self.at('failed completely'); self.play(FadeIn(result),run_time=.35)
        self.at('even after'); self.play(FadeIn(label('• Mutants learned mechanical reports',0,-2.15,GREY,26)),FadeIn(label('• Wild type: TRPM8 antagonist reduced warm detection',0,-3.05,GREY,26)),run_time=.35); self.finish()
class S14Beat(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(table(1),label('Failure alone does not identify the cause',0,-1.35,GREY,28),label('• Mutants learned mechanical reports',0,-2.15,GREY,26),label('• Wild type: TRPM8 antagonist reduced warm detection',0,-3.05,GREY,26)); self.wait(3)
class S15Notheat(SpokenScene):
    def construct(self):
        r=raster(.3,h=2.2,rest=True)
        self.add(heading('TRPM8 supplies ongoing cool input'),r,label('illustrative raster',0,-1.25,GREY,26))
        self.at('Not because heat'); self.play(FadeIn(label('Not heat-gated here',0,2.15,COOL,30)),run_time=.35)
        self.at('Removing it removes'); self.play(FadeIn(label('Removing TRPM8 removes this source of firing',0,-3.05,COOL,28)),run_time=.4)
        self.at('whose fall'); self.play(Transform(r,raster(.3,h=2.2)),FadeIn(warming_bar(-1.85)),FadeIn(label('firing falls with warming',0,1.65,COOL,28)),run_time=.5); self.finish()
class S16Heat(SpokenScene):
    def construct(self):
        self.add(table(1))
        self.at('Mice without',lead=-.42); r2=table_row(2); self.play(FadeIn(r2),run_time=.4)
        self.at('or without',lead=-.84); r3=table_row(3); self.play(FadeIn(r3),run_time=.4)
        self.at('still detected warming'); self.play(Indicate(VGroup(r2[1],r3[1]),color=REPORT,scale_factor=1.04),run_time=.45); self.finish()
class S17Triple(SpokenScene):
    def construct(self):
        # Fixed rows leave a dedicated footer for the key and qualification.
        t=table(3); t[0].shift(UP*.37); self.add(t)
        row=table_row(4)
        self.at('three heat channels'); self.play(FadeIn(row),run_time=.4)
        key=label('Triple: TRPV1 / TRPA1 / TRPM3 · no threshold specified',0,-3.5,GREY,26)
        self.at('reduced sensitivity'); self.play(FadeIn(key),run_time=.35)
        self.at('loss blunts'); self.play(FadeIn(label('— = not reported here',0,2.9,GREY,26)),run_time=.35)
        self.at('loss abolished'); self.play(Create(RoundedRectangle(width=11.9,height=.88,corner_radius=.1,color=GONE).move_to([0,.45,0])),Transform(t[0],label('TRPM8 loss: no warming report in this task',0,3.45,GONE,28)),Transform(key,label('Cold report: abolished in this task',0,-3.5,GONE,28)),run_time=.4); self.finish()
class S18Sum(SpokenScene):
    def construct(self):
        ghost=raster(1.1,h=.9,rest=True); ghost[1].set_opacity(.16)
        self.add(heading('TRPM8-null skin'),ghost,label('cool fibre · firing lost',-3.3,1.95,COOL,28),label('faint ticks: wild-type reference',2.5,1.95,GREY,26),label('illustrative rasters',0,-3.25,GREY,26))
        self.at('still had'); self.play(FadeIn(raster(-.75,warm=True,h=1.15)),FadeIn(label('warm-excited fibre',-3.8,.15,WARM,28)),FadeIn(warming_bar(-1.65)),run_time=.5)
        claim=label('Proportions similar to wild type',0,-2.75,WARM,30)
        self.play(FadeIn(claim),run_time=.3)
        self.wait(2); self.finish()
class S19Sum2(SpokenScene):
    def construct(self):
        cool=VGroup(RoundedRectangle(width=4.1,height=1.7,corner_radius=.2,color=COOL,fill_opacity=.14),label('cool alarm',size=36)).move_to([-3.65,1.35,0])
        cool[1].set_color(COOL)
        warm=VGroup(RoundedRectangle(width=4.1,height=1.7,corner_radius=.2,color=WARM,fill_color=WARM,fill_opacity=.15),label('warm alarm',color=WARM,size=36)).move_to([-3.65,-1.35,0])
        out=RoundedRectangle(width=4.6,height=3.6,corner_radius=.2,color=GREY,fill_color=BG,fill_opacity=1).move_to([3.5,0,0])
        question=label('warming report?',3.5,0,GREY,30)
        self.add(heading('Discarded model: each line alone is enough'),cool,warm,out,arrow([-1.5,1.35,0],[1.1,.6,0],COOL),arrow([-1.5,-1.35,0],[1.1,-.6,0],WARM),question)
        self.at('remaining warm responses'); self.play(cool.animate.set_opacity(.23),Create(cross([-6.15,1.35,0],.28)),run_time=.4)
        warm[0].add_updater(lambda m: m.set_fill(WARM,opacity=.15+.35*(.5+.5*np.sin(self.renderer.time*5))))
        self.at('they did not')
        # Output stays dark: only its text changes.
        self.play(FadeOut(question),FadeIn(VGroup(label('no measurable',3.5,.4,GONE,30),label('warming report',3.5,-.4,GONE,30))),run_time=.35)
        self.wait(3); self.finish()
class S20Pattern(SpokenScene):
    def construct(self):
        g=inputs(); self.add(g[0],g[2],g[3],g[5],g[6])
        self.at('reduced cool input'); self.play(Indicate(g[0],color=COOL),run_time=.5)
        self.at('may also contribute'); self.play(FadeIn(g[1]),GrowArrow(g[4]),run_time=.5)
        self.at('not isolated'); self.play(FadeIn(label('Warm input: separate effect not isolated',0,-3.25,GREY,28)),run_time=.35); self.finish()
class S21Pattern2(SpokenScene):
    def construct(self):
        g=inputs(); self.add(g,heading('Two lines · one report'))
        self.at('two lines'); self.play(*[g[i].animate.set_opacity(.35) for i in [0,1,3,4]],g[-1].animate.set_opacity(.4),run_time=.4)
        self.at('not known'); self.play(FadeIn(label('The computation is unknown',0,-3.25,GREY,30)),g[-1].animate.set_opacity(1).scale(1.2),run_time=.35); self.finish()
class S22Beat(Scene):
    def construct(self):
        self.camera.background_color=BG; g=inputs()
        for i in [0,1,3,4]: g[i].set_opacity(.35)
        g[-1].scale(1.2)
        self.add(g,heading('Two lines · one report'),label('The computation is unknown',0,-3.25,GREY,30)); self.wait(2.5)
class S23Baseline(SpokenScene):
    def construct(self):
        p=preparations(); preview=p[1].copy().set_opacity(.3); preview[0].set_fill(opacity=0); self.add(p[0],preview)
        self.at('resting cool firing'); self.play(Indicate(p[0][-3],color=COOL,scale_factor=1.03),run_time=.4)
        self.at('behaving mouse'); self.play(FadeOut(preview),FadeIn(p[1]),run_time=.4); self.finish()
class S24Baseline2(SpokenScene):
    def construct(self):
        p=preparations(); self.add(p)
        self.at('the same'); self.play(Indicate(p[0][2],color=STIM),Indicate(p[1][-2],color=STIM),run_time=.5)
        bridge=VGroup(DashedLine([-1.15,-.15,0],[1.15,-.15,0],color=GREY),Rectangle(width=2,height=.5,stroke_width=0,fill_color=BG,fill_opacity=1).move_to([0,.35,0]),label('inferred',0,.35,GREY,26))
        self.at('Joining the two'); self.play(Create(bridge[0]),run_time=.4)
        self.at('an inference'); self.play(FadeIn(VGroup(*bridge[1:])),FadeIn(label('Isolated skin → behaving mouse: an inference',0,-3.35,GREY,28)),run_time=.35); self.finish()
class S25Other(SpokenScene):
    def construct(self):
        cells=VGroup(*[Circle(.4,color=GREY,fill_color=GREY,fill_opacity=.15).move_to([x,y,0]) for x,y in [(-1.8,1.1),(-.5,1.5),(.9,1.1),(1.8,.1),(.7,-1.1),(-.8,-1.2),(-2,-.2)]])
        gang=Ellipse(width=6.7,height=5.1,color=GREY).move_to([-.15,.15,0])
        self.add(heading('Trigeminal ganglion'),gang,cells,label('imaged warmth responses',0,-2.8,WARM,30),label('anaesthetized mice · acute drug block · 2016',0,-3.4,GREY,26))
        self.at('In mouthwarming'); stim=VGroup(Rectangle(width=.3,height=2,stroke_width=0,fill_color=STIM,fill_opacity=.8).move_to([-4.7,.2,0]),label('mouth',-5,2.05,STIM,26),label('warming',-5,1.55,STIM,26),arrow([-4.4,.2,0],[-3.55,.2,0],STIM))
        self.play(FadeIn(stim),cells[0].animate.set_fill(WARM,.9).set_stroke(WARM),run_time=.45)
        self.at('blocking',lead=0); self.play(FadeIn(VGroup(chip('TRPV1',GONE,28),label('blocker',0,-.75,GONE,28)).move_to([4.9,.2,0])),run_time=.45)
        self.at('removed the imaged'); self.play(cells[0].animate.set_fill(WARM,.02).set_stroke(GREY),run_time=.65); self.finish()
class S26Open(SpokenScene):
    def construct(self):
        beam=Line([-4.4,1.5,0],[4.4,1.5,0],color=GREY,stroke_width=6)
        stand=VGroup(Line([0,1.5,0],[0,-2.2,0],color=GREY,stroke_width=7),Line([-1.2,-2.2,0],[1.2,-2.2,0],color=GREY,stroke_width=7))
        pans=VGroup()
        for x in [-3.6,3.6]:
            pans.add(VGroup(Line([x,1.5,0],[x-2,-.3,0],color=GREY),Line([x,1.5,0],[x+2,-.3,0],color=GREY),RoundedRectangle(width=4.3,height=1.6,corner_radius=.25,color=GREY,fill_opacity=.08).move_to([x,-1.1,0])))
        self.add(heading('What supports gentle warmth?'),beam,stand,pans)
        self.at('warm fibers'); self.play(FadeIn(VGroup(label('TRPV1-positive',-3.6,-.75,WARM,28),label('warm fibres',-3.6,-1.4,WARM,30))),run_time=.4)
        self.at('cool fibers'); self.play(FadeIn(VGroup(label('TRPM8-dependent',3.6,-.75,COOL,26),label('cool input ↓',3.6,-1.4,COOL,30))),run_time=.4)
        self.at('not settled'); self.play(FadeIn(label('Not settled',0,-3.1,GREY,40)),run_time=.4); self.finish()
class S27Take(SpokenScene):
    def construct(self):
        self.add(raster(1.7,h=1.25,rest=True),label('cool fibre firing at rest',0,2.85,COOL,32),label('illustrative raster',0,.6,GREY,26))
        self.at('Keep the bath'); self.play(FadeIn(label('27 °C bath, resting',-3,-1.9,STIM,30)),FadeIn(label('32 °C baseline',3,-1.9,STIM,30)),run_time=.35)
        self.at('resting condition'); self.play(FadeIn(label('A resting condition',0,-.3,size=38)),run_time=.35)
        self.at('part of the stimulus'); self.play(FadeIn(label('is part of the stimulus.',0,-1.05,STIM,38)),FadeIn(label('Bath and local stimulator have different baselines',0,-3,GREY,26)),run_time=.35); self.finish()
class S28End(EndCard):
    LINE='A resting condition is part of the stimulus.'
