"""Reading the Slope.
COLOR MAP: BLUE retina/axons/EphA; ORANGE ephrin-A/posterior membrane;
GREY anatomy/anterior membrane; YELLOW questions; RED removed branches/limit;
GREEN toy endpoints. No molecular structures. All toy traces use L(x)=1+2x,
P=R*L(x), endpoint=(3/R-1)/2. Schematic gradients are explicitly labelled.
"""
import numpy as np
from bp_style import *
ORANGE = '#F29E4C'
PALE = '#C7CCD5'
BROWN = '#946A4C'

def label(s,x,y,size=26,color=TEXT):
    return T(s,size,color).move_to([x,y,0])
def heading(s): return label(s,0,3.22,32)
def line(a,b,color=BLUE,w=5): return Line(a,b,color=color,stroke_width=w)
def cell(x,y,color=BLUE,r=.12): return Dot([x,y,0],radius=r,color=color)
def ligand(x): return 1+2*x
def endpoint(r): return (3/r-1)/2

def gradient(x0,x1,y,h=.7):
    g=VGroup()
    for i in range(40):
        u=(i+.5)/40
        g.add(Rectangle(width=(x1-x0)/40+.004,height=h,stroke_width=0,
            fill_color=ORANGE,fill_opacity=.12+.78*(ligand(u)-1)/2).move_to([x0+(x1-x0)*u,y,0]))
    g.add(Rectangle(width=x1-x0,height=h,color=ORANGE,stroke_width=2).move_to([(x0+x1)/2,y,0]))
    return g

def carpet(cx=0,w=11,heated=False,single=None):
    g=VGroup(); h=4.6
    if single is not None:
        g.add(Rectangle(width=w,height=h,stroke_width=0,fill_color=ORANGE if single else PALE,
            fill_opacity=.38 if single else .65).move_to([cx,-.15,0]))
    else:
        for i in range(8):
            x=cx-w/2+(i+.5)*w/8; post=i%2
            g.add(Rectangle(width=w/8-.018,height=h,stroke_width=0,
                fill_color=(BROWN if heated else ORANGE) if post else PALE,
                fill_opacity=(.65 if heated else .32) if post else .65).move_to([x,-.15,0]))
            if heated and post:
                for y in np.arange(-2.2,1.9,.45):
                    g.add(line([x-w/18,y,0],[x+w/18,y+.3,0],ORANGE,2))
    g.add(RoundedRectangle(width=w+.12,height=h+.12,corner_radius=.16,color=GREY,stroke_width=2).move_to([cx,-.15,0]))
    return g

def lane_key(heated=False):
    g=VGroup()
    for x,col,text in [(-5.75,PALE,'anterior membrane'),(.25,BROWN if heated else ORANGE,'posterior membrane'+(' · heated' if heated else ''))]:
        swatch=Rectangle(width=.4,height=.4,stroke_width=0,fill_color=col,fill_opacity=.8).move_to([x,-3.1,0])
        g.add(swatch,T(text,26).next_to(swatch,RIGHT,buff=.24))
    return g

def retina(cx=0,w=11):
    return VGroup(Rectangle(width=w,height=.32,color=BLUE,fill_opacity=.85).move_to([cx,1.78,0]),label('retina',cx,2.44,26,BLUE))
def growth(cx=0,w=11,mode='poised'):
    g=VGroup(); pitch=w/8
    for i in range(4):
        # Neutral stubs straddle borders; temporal result alone occupies pale centers.
        x=cx-w/2+(2*i+(1 if mode=='poised' else .5))*pitch
        if mode=='poised':
            g.add(line([x,1.6,0],[x,1.05,0]))
        elif mode=='temporal':
            g.add(line([x,1.6,0],[x,-2.2,0]))
        else:
            g.add(line([x,1.6,0],[min(cx+w/2-.1,x+1.2*pitch),-2.2,0]))
            g.add(line([x+pitch,1.6,0],[x+pitch,-2.1,0],w=3))
    return g
Q1='Where will temporal axons grow?'
Q2='After heating: where will temporal axons grow?'
def assay_question(heated=False):
    return VGroup(carpet(heated=heated),retina(),growth(),lane_key(heated),heading(Q2 if heated else Q1))
def assay_panel(cx,kind):
    return VGroup(carpet(cx,5.5),retina(cx,5.5),growth(cx,5.5,'temporal' if kind=='Temporal' else 'both'),
                  label(kind,cx,3.15,30,BLUE),label('stays on pale lanes' if kind=='Temporal' else 'grows on both',cx,-3,26))

def repellent_frame(with_axon=True):
    g=VGroup(heading('Evidence points to a heat-sensitive repellent'),
        Rectangle(width=4,height=5.2,color=ORANGE,fill_color=ORANGE,fill_opacity=.3).move_to([2.9,-.25,0]),
        label('posterior membrane',2.9,-3.2,26,ORANGE),label('heat-sensitive',2.9,1.6,28,ORANGE),
        label('temporal axon',-3.6,-1.6,28,BLUE))
    if with_axon:
        g.add(line([-5.6,-.1,0],[-.2,-.1,0]),Arrow([.6,.7,0],[-1,.7,0],color=BLUE,buff=0),cell(-.2,-.1))
    return g

def papers(right=False,named=True):
    g=VGroup()
    for x,active in [(-3.15,not right),(3.15,right)]:
        g.add(Rectangle(width=5.65,height=5.6,color=ORANGE if active else GREY,stroke_width=3,
            fill_color=GREY,fill_opacity=.08).move_to([x,-.15,0]),label('Cell · 1995',x,2.1,32),
            line([x-2.35,1.55,0],[x+2.35,1.55,0],GREY,2))
    g.add(label('Drescher and colleagues',-3.15,.95,26),label('Posterior tectal membranes',-3.15,.25,26),
          label('Repellent purified',-3.15,-.45,30,ORANGE))
    if named: g.add(label('ephrin-A5',-3.15,-1.65,36,ORANGE))
    g.add(label('Cheng and colleagues',3.15,.95,26),label('Graded ligand in tectum',3.15,.25,26))
    if right:
        g.add(label('ephrin-A2',3.15,-.45,34,ORANGE),gradient(.9,5.4,-1.25,.55),label('Cloned 1994 · mapped 1995',3.15,-2.25,26))
    else: g.add(label('Second report',3.15,-1.6,28,GREY))
    return g

def slopes():
    source=VGroup(label('Retina · EphA',-4.6,3.15,30,BLUE),label('nasal · low',-4.6,2.3,28,BLUE),
        label('temporal · high',-4.6,-3.1,28,BLUE),Arrow([-5.7,1.8,0],[-5.7,-2.4,0],color=BLUE,buff=0))
    for i in range(40):
        u=(i+.5)/40
        source.add(Rectangle(width=.85,height=4.5/40+.004,stroke_width=0,fill_color=BLUE,
            fill_opacity=.15+.8*u).move_to([-4.6,1.9-4.5*u,0]))
    # Qualitative level axes: ticks low/high avoid presenting toy units as measurements.
    axes=Axes(x_range=[0,1,.5],y_range=[0,3,1],x_length=6.4,y_length=4.5,tips=False,
        axis_config={'color':GREY,'include_ticks':False}).move_to([2.35,-.05,0])
    target=VGroup(label('Tectum',2.3,3.15,30,ORANGE),label('ephrin-A level (schematic)',2.3,2.55,26,ORANGE),axes,
        axes.plot(ligand,x_range=[0,1],color=ORANGE,stroke_width=6),
        label('low',-1.55,-.75,26,ORANGE),label('high',-1.55,2.05,26,ORANGE),
        label('front',-.3,-2.8,28),label('back',5.3,-2.8,28),Arrow([.3,-2.8,0],[4.5,-2.8,0],color=ORANGE,buff=0))
    return VGroup(source,target)

X0,X1=-1.5,5.55
ROWS=[1.15,-.2,-1.55]
QT='Which reaches the limit first?'
# Preview stops just short of the computed threshold. R=3 approaches the front
# from outside the tectum; it cannot move into positive x below the limit.
PREVIEW=tuple(-.1+.9*(endpoint(r)+.1) for r in [1,2,3])
def toy_base():
    return VGroup(label('repulsion =',-4.7,2.55,26),label('EphA × ephrin-A',-4.7,2.12,26),
        label('limit = 3',-1.6,2.3,28,RED),
        gradient(X0,X1,-2.6,.55),label('front · x = 0',X0+.6,-3.08,26),label('back · x = 1',X1-.7,-3.08,26),
        label('Linear toy gradient: ephrin-A 1 → 3',2,-3.63,26,ORANGE))
def runners(xs=(0,0,0),checked=(),meter=False):
    g=VGroup()
    for r,y,u in zip([1,2,3],ROWS,xs):
        x=X0+(X1-X0)*u; v=r*ligand(u)
        g.add(label('EphA '+str(r),-4.8,y+.1,28,BLUE),
              line([X0,y,0],[X1,y,0],GREY,2),line([X0-.22,y,0],[x,y,0]),cell(x,y))
        # A real gauge, with its threshold tick outside the bar. Unchecked states
        # carry no numerical answer or text inside the meter.
        g.add(Rectangle(width=2.5,height=.30,color=GREY,fill_opacity=0).move_to([-4.8,y-.4,0]),
              line([-3.55,y-.65,0],[-3.55,y-.15,0],RED,3))
        if meter or r in checked:
            f=min(1,v/3)
            g.add(Rectangle(width=2.46*f,height=.24,stroke_width=0,fill_color=GREEN if r in checked else BLUE,fill_opacity=.8).move_to([-6.03+1.23*f,y-.4,0]))
        if r in checked:
            text='x = '+('0' if u==0 else '1' if u==1 else '0.25')+' · ligand '+f'{ligand(u):g}'
            # Endpoint labels stay inside the safe frame, beside their own track.
            tx=max(-.25,min(4.5,x))
            g.add(label(text,tx,y-.46,26,GREEN))
    return g
def toy_question(): return VGroup(toy_base(),runners(PREVIEW,meter=True),heading(QT))
def toy_result(): return VGroup(toy_base(),runners([endpoint(r) for r in [1,2,3]],(1,2,3)),heading('Toy endpoint rule · not a full mechanism'))

def branch_base():
    return VGroup(gradient(-5.6,5.6,-.25,4.9).fade(.82),label('tectum',-4.8,1.9,26,GREY),
        gradient(-5.6,5.6,-2.6,.65),label('front',-5.1,-3.25,28),label('back',5.1,-3.25,28))
def trunk(end=5.1): return line([-5.6,-.25,0],[end,-.25,0],w=12)
def branches():
    good=VGroup(); bad=VGroup()
    for x in [-1.65,-1.05,-.45,1.05,2.55,4.05]:
        group=good if x<0 else bad
        group.add(line([x,-.25,0],[x+.3,1.55,0]),line([x,-.25,0],[x+.2,-2,0]))
    return good,bad
def overshoot_mark():
    return VGroup(label('overshoot',2.65,.98,28,BLUE),line([.2,.48,0],[5.1,.48,0],BLUE,4),
                  line([.2,.48,0],[.2,.16,0],BLUE,4),line([5.1,.48,0],[5.1,.16,0],BLUE,4))
def zone_label():
    return VGroup(label('termination zone',-1.1,2.5,30,GREEN),
        line([-1.9,1.95,0],[-.05,1.95,0],GREEN,3),
        line([-1.9,1.95,0],[-1.9,1.6,0],GREEN,3),line([-.05,1.95,0],[-.05,1.6,0],GREEN,3))

def ordered_map():
    g=VGroup(heading('More receptor, less ligand.'),label('Toy model · comparison among axons comes next',0,2.5,26),
        label('Retina · EphA',-4.75,1.8,28,BLUE),label('Tectum · ephrin-A',2,1.8,28,ORANGE),
        label('nasal · low',-4.9,1.15,26,BLUE),label('temporal · high',-4.8,-3.1,26,BLUE),
        gradient(-1.3,5.6,-2.4,.4),label('front · low',-.9,-3.62,26,ORANGE),label('back · high',4.8,-3.62,26,ORANGE),
        label('axon receptor level',2.1,-3.18,24,BLUE),
        label('Circled: toy axons 1, 2, 3',2,1.16,24,BLUE))
    for i in range(30):
        u=(i+.5)/30
        g.add(Rectangle(width=.32,height=2.7/30+.004,stroke_width=0,fill_color=BLUE,
            fill_opacity=.15+.7*u).move_to([-3.65,.9-2.7*u,0]))
    # Keep the true target positions. Fan the labels out below the ligand bar;
    # leaders distinguish the crowded high-receptor endpoints without moving them.
    for r,y,lx in zip([1,1.5,2,2.5,3],np.linspace(.5,-1.65,5),[5.6,2.15,.425,-.8,-2.0]):
        x=-1.3+6.9*endpoint(r)
        g.add(cell(-3.65,y,r=.1),label(f'{r:g}',-4.2,y,26,BLUE),
            line([-3.45,y,0],[x,y,0],BLUE,3),line([x,y,0],[x,-2.08,0],BLUE,3),cell(x,-2.08,GREEN,.09),
            line([x,-2.62,0],[lx,-2.75,0],GREY,2),label(f'{r:g}',lx,-2.9,24,BLUE))
        if r in [1,2,3]:
            g.add(Circle(radius=.24,color=BLUE,stroke_width=2).move_to([-4.2,y,0]))
    return g

class S00Title(TitleCard):
    TITLE='Reading the Slope'
    LESSON="Topographic Maps: Sperry's Eye and Eph Gradients"
    def construct(self):
        self.add(label('BIOCHEMISTRYPEDIA',0,2.3,26,TEAL),label("Topographic Maps: Sperry's Eye",0,1.35,28,GREY),label('and Eph Gradients',0,.85,28,GREY))
        self.play(FadeIn(label(self.TITLE,0,-.2,52)),Create(line([-1.2,-1,0],[1.2,-1,0],GOLD)),run_time=.7); self.finish()
class S01Question(SpokenScene):
    def construct(self):
        target=VGroup(Rectangle(width=6,height=4.6,color=GREY,fill_color=GREY,fill_opacity=.14).move_to([2.4,-.2,0]),label('target',2.4,-3,30))
        self.add(heading('Reading the Slope'),target,line([-5.8,-.2,0],[-2,-.2,0]),cell(-2,-.2))
        self.at('the target itself'); self.play(Indicate(target[0],scale_factor=1.02),run_time=.5)
        self.at('Can we ask'); self.play(Create(Arrow([-2,-.2,0],[.5,-.2,0],color=BLUE,buff=0)),FadeIn(label('?',2.4,.2,72,YELLOW)),run_time=.7); self.finish()
class S02Carpet(SpokenScene):
    def construct(self):
        self.add(heading('Walter, Bonhoeffer and colleagues · 1987'),label('dish seen from above',0,-3.1,28),carpet().set_opacity(.25))
        self.at('In'); self.play(FadeIn(carpet()),run_time=1.1); self.finish()
class S03Lanes(SpokenScene):
    def construct(self):
        self.add(carpet(),heading('Alternating tectal membranes'))
        self.at('Membranes from'); self.play(FadeIn(lane_key()),run_time=.6)
        # Leaders directly attach both swatches to representative lanes.
        self.at('alternating narrow lanes'); self.play(Create(line([-5.75,-2.85,0],[-4.81,-2.1,0],PALE,2)),Create(line([.25,-2.85,0],[.69,-2.1,0],ORANGE,2)),run_time=.5); self.finish()
class S04Strip(SpokenScene):
    def construct(self):
        self.add(carpet(),lane_key()); self.at('A strip'); self.play(FadeIn(retina()),run_time=.6)
        self.at('each growing axon'); self.play(Create(growth()),run_time=.8); self.finish()
class S05Predict(SpokenScene):
    def construct(self):
        self.add(carpet(),retina(),lane_key(),growth()); self.at('Where will'); self.play(FadeIn(heading(Q1)),run_time=.4); self.finish()
class S06Pause(Scene):
    def construct(self): self.camera.background_color=BG; self.add(assay_question()); self.wait(5)
class S07Reveal(SpokenScene):
    def construct(self):
        a=VGroup(carpet(),retina(),lane_key(),growth()); self.add(a)
        self.at('Temporal axons'); self.play(Transform(a,assay_panel(0,'Temporal')),run_time=.7)
        self.at('Nasal axons'); right=assay_panel(3.25,'Nasal').shift(RIGHT*7)
        self.add(right); self.play(a.animate.shift(LEFT*3.25),right.animate.shift(LEFT*7),run_time=.55)
        # Preserve both results for a full four seconds after the second panel settles.
        self.wait(4.1); self.finish()
class S08Control(SpokenScene):
    def construct(self):
        self.add(heading('Both retinal types grow on either membrane alone'))
        self.at('On either membrane'); self.play(FadeIn(carpet(-3.2,5.5,single=False)),FadeIn(carpet(3.2,5.5,single=True)),
            FadeIn(label('anterior membrane only',-3.2,-3.1,26)),FadeIn(label('posterior membrane only',3.2,-3.1,26)),run_time=.5)
        self.at('both grew well'); self.play(Create(growth(-3.2,5.5,'both')),Create(growth(3.2,5.5,'both')),run_time=.8); self.finish()
class S09Predict(SpokenScene):
    def construct(self):
        c=carpet(); k=lane_key(); self.add(c,k,heading('Heat the posterior membranes first'))
        self.at('heat the back'); heat=VGroup(*[label('≈',x,2.55,42,ORANGE) for x in [-3.44,-.69,2.06,4.81]])
        self.play(FadeIn(heat),Transform(c,carpet(heated=True)),Transform(k,lane_key(True)),run_time=.8)
        self.at('What will'); self.remove(heat,*[m for m in self.mobjects if isinstance(m,Text) and m.get_center()[1]>3])
        self.play(FadeIn(retina()),FadeIn(growth()),FadeIn(heading(Q2)),run_time=.4); self.finish()
class S10Pause(Scene):
    def construct(self): self.camera.background_color=BG; self.add(assay_question(True)); self.wait(5)
class S11Reveal(SpokenScene):
    def construct(self):
        p=growth(); q=heading(Q2); self.add(carpet(heated=True),retina(),lane_key(True),p,q)
        self.at('The avoidance vanished'); self.play(Transform(q,heading('Avoidance vanished')),Transform(p,growth(mode='both')),run_time=.8)
        self.at('unheated front lanes'); self.play(Transform(q,heading('Pale anterior lanes were not heated')),run_time=.4); self.finish()
class S12Repellent(SpokenScene):
    def construct(self):
        g=repellent_frame(False); tip=VGroup(line([-5.6,-.1,0],[.7,-.1,0]),cell(.7,-.1)); self.add(g,tip)
        self.at('repellent at'); self.play(Transform(tip,VGroup(line([-5.6,-.1,0],[-.2,-.1,0]),cell(-.2,-.1))),
            Create(Arrow([.6,.7,0],[-1,.7,0],color=BLUE,buff=0)),run_time=.8); self.finish()
class S13Beat(Scene):
    def construct(self): self.camera.background_color=BG; self.add(repellent_frame()); self.wait(2)
class S141995(SpokenScene):
    def construct(self):
        self.add(papers(named=False)); self.at('one paper found'); self.play(Indicate(self.mobjects[0][0],color=ORANGE,scale_factor=1),run_time=.5)
        self.at('now called'); self.play(FadeIn(label('ephrin-A5',-3.15,-1.65,36,ORANGE)),run_time=.5); self.finish()
class S14b1995(SpokenScene):
    def construct(self):
        p=papers(); self.add(p); self.at('A second paper'); self.play(Transform(p,papers(True)),run_time=.65); self.finish()
class S15Slopes(SpokenScene):
    def construct(self):
        g=slopes(); g[0].fade(.65); self.add(g)
        self.at('rises from front'); self.play(ShowPassingFlash(g[1][3].copy().set_color(YELLOW),time_width=.8),run_time=1)
        self.at('Its receptor'); self.play(Transform(g[0],slopes()[0]),run_time=.6)
        self.at('opposite way'); self.play(Indicate(g[0][3],color=BLUE,scale_factor=1),run_time=.6); self.finish()
class S16Toy(SpokenScene):
    def construct(self):
        old=slopes(); b=toy_base(); self.add(old); self.at('Take toy numbers')
        self.play(FadeOut(old),FadeIn(b),FadeIn(runners()),FadeIn(heading('Toy numbers · not measured')),run_time=.6)
        self.at('Repulsion is'); self.play(Indicate(b[0],color=YELLOW,scale_factor=1),run_time=.5); self.finish()
class S17Meter(SpokenScene):
    def construct(self):
        b=toy_base(); t=ValueTracker(0)
        r=always_redraw(lambda: runners([-.10+(u+.10)*t.get_value() for u in PREVIEW],meter=True))
        self.add(b,r,heading('Toy numbers · not measured'))
        self.at('enters at the front'); self.play(t.animate.set_value(1),run_time=2.2,rate_func=linear)
        self.at('reaches the limit'); self.play(Indicate(b[2],color=RED,scale_factor=1.05),run_time=.6); self.finish()
class S18Predict(SpokenScene):
    def construct(self):
        self.add(toy_base(),runners(PREVIEW,meter=True)); self.at('Three axons'); self.wait(.2)
        self.at('which reaches'); self.play(FadeIn(heading(QT)),run_time=.4); self.finish()
class S19Pause(Scene):
    def construct(self): self.camera.background_color=BG; self.add(toy_question()); self.wait(5)
class S20Reveal(SpokenScene):
    def construct(self):
        r=runners(PREVIEW,meter=True); q=heading(QT); self.add(toy_base(),r,q)
        self.at('most receptor'); self.remove(q,r)
        q=heading('Toy endpoint rule · not a full mechanism'); r=runners([PREVIEW[0],PREVIEW[1],0],checked=(3,),meter=True); self.add(q,r); self.wait(.4)
        self.at('least ends'); t=ValueTracker(0)
        moving=always_redraw(lambda: runners([u+(endpoint(v)-u)*t.get_value() for v,u in zip([1,2,3],[PREVIEW[0],PREVIEW[1],0])],(3,),meter=True))
        self.remove(r); self.add(moving); self.play(t.animate.set_value(1),run_time=.9,rate_func=linear)
        self.remove(moving); self.add(runners([endpoint(v) for v in [1,2,3]],(1,2,3))); self.finish()
class S21Beat(Scene):
    def construct(self): self.camera.background_color=BG; self.add(toy_result()); self.wait(3)
class S22Overshoot(SpokenScene):
    def construct(self):
        t=trunk(-2); self.add(branch_base(),t,heading('Overshoot, then branches'))
        mark=overshoot_mark()
        self.at('first overshoot'); self.play(Transform(t,trunk()),run_time=.85)
        self.play(FadeIn(mark),run_time=.35)
        self.at('side branches',lead=0); good,bad=branches(); self.play(FadeOut(mark),Create(good),Create(bad),run_time=.7); self.finish()
class S23Branches(SpokenScene):
    def construct(self):
        t=trunk(); good,bad=branches(); self.add(branch_base(),t,good,bad,heading('Branch formation and survival'))
        doomed=line([-.15,-.25,0],[5.1,-.25,0],RED,12)
        self.at('keeps branches'); self.play(FadeIn(label('high ephrin-A',3.75,1.98,28,ORANGE)),bad.animate.set_color(RED),
            FadeIn(VGroup(line([1.8,2.7,0],[2.3,2.7,0],RED),label('branch removed',3.8,2.7,26))),run_time=.45)
        self.at('right zone'); self.play(Uncreate(bad),run_time=.9)
        self.at('overshooting part'); self.add(doomed); self.wait(1.1)
        self.at('later removed'); self.play(Uncreate(doomed),Transform(t,trunk(-.15)),run_time=1.1); self.finish()
class S24Stop(SpokenScene):
    def construct(self):
        good,_=branches(); self.add(branch_base(),trunk(-.15),good)
        self.at('where it keeps'); self.play(Indicate(good,color=BLUE,scale_factor=1.03),run_time=.6)
        self.at('its termination zone'); self.play(FadeIn(zone_label()),run_time=.5); self.finish()
class S25Takeaway(SpokenScene):
    def construct(self):
        g=ordered_map(); self.add(g); self.at('more receptor'); self.play(Indicate(g[0],scale_factor=1.02),run_time=.5)
        self.at('In the toy'); self.play(Indicate(g[1],color=YELLOW,scale_factor=1),run_time=.5); self.finish()
class S26End(EndCard):
    LINE='More receptor ends where there is less ligand.'
    def construct(self):
        g=VGroup(T(self.LINE,40,font=TITLE_FONT),T('biochemistrypedia.com',26,TEAL)).arrange(DOWN,buff=.5)
        fit(g,max_w=12.2); self.play(FadeIn(g),run_time=.65); self.finish()
