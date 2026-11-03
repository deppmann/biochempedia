"""Take One Route Away: revised visual argument.
COLOR MAP: ORANGE Merkel cells; PURPLE afferent; BLUE Piezo2/current;
YELLOW spikes; GREEN matches prediction (and depolarizing light);
GOLD does not match / caution; RED silencing light only; GREY skin/control.
Down arrows denote reductions, independently of prediction-match colour.
All spike trains are explicit illustrative model realizations, not data.
Control: reference spike_times() renewal model. Perturbations use its
piecewise-linear event-count intensity, integrated against a rate multiplier.
Deletion multiplier exp(-(t-1.9)/2); silencing multiplier 0.1 in the hold;
Atoh1 multiplier 1/3 at onset, 1 until 4.2, then 0. No measured timing claimed.
"""
import numpy as np
from bp_style import *
PURPLE = '#B58CD9'
ORANGE = '#F29E4C'


def label(txt,x,y,size=28,color=TEXT):
    return T(txt,size,color).move_to([x,y,0])


def left(txt,x,y,size=26,color=TEXT):
    return T(txt,size,color).move_to([x,y,0],aligned_edge=LEFT)


def heading(txt): return label(txt,0,3.25,30)


def ticks(xs,y,h=.65,color=YELLOW,w=3):
    return VGroup(*[Line([x,y-h/2,0],[x,y+h/2,0],color=color,stroke_width=w) for x in xs])


def spike_times():
    # Unchanged control renewal generator from scenes.old.py.
    rng=np.random.default_rng(7)
    ts,t=[],.15
    for i in range(9):
        ts.append(t); t+=.11+.025*i
    t=ts[-1]+.55
    while t<8.8:
        ts.append(t); t+=float(rng.gamma(1.2,.5))+.12
    return np.array(ts)


def model(mode):
    control=spike_times()
    if mode=='control': return control
    if mode=='empty': return np.array([])
    if mode=='light':
        rng=np.random.default_rng(11)
        ts=np.cumsum(.4+rng.gamma(1.5,.3,12))-.2
        return ts[ts<9]
    # Integrate the control's event-count intensity with a specified multiplier.
    t=np.linspace(0,9,9001)
    count=np.interp(t,np.r_[0,control,9],np.r_[0,np.arange(1,len(control)+1),len(control)+.2])
    mult=np.ones_like(t)
    if mode=='silenced': mult[t>=1.9]=.1
    if mode=='deleted': mult[t>=1.9]=np.exp(-(t[t>=1.9]-1.9)/2)
    if mode=='short': mult=np.where(t<1.9,1/3,np.where(t<4.2,1,0))
    integrated=np.cumsum(np.r_[0,np.diff(count)]*mult)
    return np.interp(np.arange(1,int(integrated[-1])+1),integrated,t)


ROWS=[('Light depolarizes cells\nNo touch','fires without touch','',GREEN,GREEN),
      ('Light silences cells\nHeld press','not reported','↓ suppressed',GREY,GREEN),
      ('Epithelial Piezo2\ndeleted','similar','↓ reduced',GREEN,GREEN),
      ('Developmental Atoh1\ndeletion','↓ lower','↓ cut short',GOLD,GREEN),
      ('Tetanus toxin\nRelease blocked','↓ lower','↓ lower',GREY,GREY)]


def legend(y=-2.35):
    return VGroup(label('Green: matches prediction',-3.1,y,26,GREEN),label('Amber: does not',3.3,y,26,GOLD),label('↓ = lower firing • grey release row is not scored',0,y-.55,26,GREY))


def table(n=5,pending=None):
    g=VGroup()
    for txt,x in [('Manipulation',-6.1),('Onset',-.8),('Hold',1.8),('Source',4.35)]:
        g.add(left(txt,x,2.95,26,GREY))
    g.add(Line([-6.15,2.6,0],[6.45,2.6,0],color=GREY))
    for i in range(n):
        txt,a,b,ca,cb=ROWS[i]; y=2.12-i*.86
        g.add(left(txt,-6.1,y,26))
        if i!=pending:
            if i==0: g.add(left(a,-.8,y,26,GREEN))
            else: g.add(left(a,-.8,y,26,ca),left(b,1.8,y,26,cb))
        else: g.add(left('onset?',-.8,y,26,GOLD),left('hold?',1.8,y,26,GOLD))
        g.add(left('Hoffman\n2018' if i==4 else 'Maksimovic\n2014',4.35,y,26,GREY))
        g.add(Line([-6.15,y-.43,0],[6.45,y-.43,0],color=GREY,stroke_opacity=.45))
    return g


def strip(i,pending=False):
    txt,a,b,ca,cb=ROWS[i]
    g=VGroup(left(txt,-6.1,2.92,26),label('Onset',-.1,3.35,26,GREY),label('Hold',3,3.35,26,GREY))
    if i==0:
        if not pending: g.add(label(a,1.6,2.7,28,GREEN))
    else:
        g.add(label('onset?' if pending else a,-.1,2.7,26,GOLD if pending else ca),label('hold?' if pending else b,3,2.7,26,GOLD if pending else cb))
    g.add(left('Hoffman\n2018' if i==4 else 'Maksimovic\n2014',4.35,2.94,26,GREY),Line([-6.15,2.22,0],[6.15,2.22,0],color=GREY))
    if pending and i>0:
        for x in [-.1,3]:
            g.add(RoundedRectangle(width=2.35,height=.56,corner_radius=.08,color=GOLD).move_to([x,2.7,0]))
    return g


def raster(mode='control',control=False,light=False):
    fx=lambda t:-5.6+11*t/9
    y=-.55
    g=VGroup()
    # Shared phase boundaries on every touch raster.
    if not light:
        for lo,hi,title in [(0,1.9,'Onset'),(1.9,9,'Hold')]:
            x0,x1=fx(lo),fx(hi)
            g.add(Rectangle(width=x1-x0,height=2.65,stroke_width=0,fill_color=BLUE if lo==0 else GREY,fill_opacity=.10).move_to([(x0+x1)/2,y-.05,0]))
            g.add(Line([x0,y-1.55,0],[x1,y-1.55,0],color=GREY),label(title,(x0+x1)/2,y-1.95,28))
        g.add(DashedLine([fx(1.9),y-1.4,0],[fx(1.9),y+1.3,0],color=GREY))
    g.add(Line([fx(0),y+1.9,0],[fx(9),y+1.9,0],color=GREEN if light else GREY,stroke_width=7),label('light, no touch' if light else 'press held',-2.8,y+2.35,28,GREEN if light else GREY))
    if not light:
        g.add(Line([fx(9),y-1.4,0],[fx(9),y+2.2,0],color=TEXT,stroke_width=2),label('probe lifts',4.8,y+2.35,26))
    if control:
        g.add(Line([fx(0),y+.8,0],[fx(9),y+.8,0],color=GREY,stroke_opacity=.4),ticks([fx(t) for t in spike_times()],y+.8,.42,GREY,2),left('control',-6.15,y+1.35,26,GREY))
    g.add(Line([fx(0),y,0],[fx(9),y,0],color=GREY,stroke_width=2,stroke_opacity=.4))
    st=model(mode)
    tk=ticks([fx(t) for t in st],y)
    if mode=='silenced':
        for tick,t in zip(tk,st):
            if t<1.9: tick.set_color(GREY).set_opacity(.25)
        g.add(Line([fx(1.9),y+1.55,0],[fx(9),y+1.55,0],color=RED,stroke_width=7),label('light on: Merkel cells silenced',.6,y+1.02,26,RED))
    g.add(tk)
    g.trace=tk
    g.add(label('illustrative model • time →',0,-3.45,26,GREY))
    return g


def pair(cx=0,cy=0,s=1,fibre=1):
    body=RoundedRectangle(width=2*s,height=1.7*s,corner_radius=.5*s,color=ORANGE,fill_color=ORANGE,fill_opacity=.22).move_to([cx,cy,0])
    disc=RoundedRectangle(width=1.6*s,height=.22*s,corner_radius=.08,stroke_width=0,fill_color=PURPLE,fill_opacity=1).move_to([cx,cy-.98*s,0])
    line=Line(disc.get_bottom(),disc.get_bottom()+DOWN*fibre*s,color=PURPLE,stroke_width=7)
    g=VGroup(body,disc,line); g.body=body; g.disc=disc; g.line=line
    return g


def dome(missing=False,cy=-.35):
    sheet=RoundedRectangle(width=11.4,height=2.45,corner_radius=.6,color=GREY,fill_color=GREY,fill_opacity=.08).move_to([0,cy+.15,0])
    g=VGroup(sheet)
    # Continuous epidermal sheet; seams replace detached rounded cells.
    for x in [-4,-1.35,1.35,4]:
        g.add(Line([x,cy-1.07,0],[x,cy+1.37,0],color=GREY,stroke_width=2,stroke_opacity=.55))
    p=pair(0,cy,1.05,.8)
    p.body.stretch_to_fit_height(2.25).shift(UP*.22)
    if missing:
        slot=DashedVMobject(p.body,num_dashes=28).set_color(ORANGE)
        g.add(slot,p.disc,p.line)
    else: g.add(p)
    g.add(label('other epithelial cells',-3.5,cy+1.85,26,GREY),label('touch dome',4.7,cy+1.85,26,GREY))
    g.add(label('ending remains' if missing else 'recorded afferent • no opsin',2,cy-2.2,28,PURPLE),Line([1.1,cy-1.95,0],[.25,cy-1.1,0],color=PURPLE))
    g.p=p
    return g


def routes(compact=False):
    y=2.1 if not compact else 1.9
    a=chip("Ending's own Piezo2",BLUE,size=30).move_to([-3.4,y,0])
    b=chip('Merkel cell: its Piezo2,\nthen release at the synapse',ORANGE,size=28).move_to([3.3,y,0])
    if compact:
        a.scale(1.08); b.scale(1.08)
    ax=chip('one axon',PURPLE,size=34).move_to([0,-1.9 if not compact else -.35,0])
    aa=Arrow(a.get_bottom(),ax.get_top()+LEFT*.5,buff=.15,color=PURPLE,stroke_width=6)
    bb=Arrow(b.get_bottom(),ax.get_top()+RIGHT*.5,buff=.15,color=ORANGE,stroke_width=6)
    return VGroup(a,b,ax,aa,bb)


def prep():
    bath=RoundedRectangle(width=8.8,height=3.8,corner_radius=.5,color=BLUE,fill_color=BLUE,fill_opacity=.08).move_to([-1.7,.2,0])
    skin=RoundedRectangle(width=5.8,height=.85,corner_radius=.2,color=GREY,fill_color=GREY,fill_opacity=.3).move_to([-2,.4,0])
    nerve=Line([.9,.15,0],[5,.15,0],color=PURPLE,stroke_width=8)
    el=VGroup(Line([4.2,2.35,0],[4.2,.15,0],color=TEXT,stroke_width=4),Circle(.14,color=TEXT).move_to([4.2,.15,0]))
    labs=VGroup(label('skin',-3.5,.4,28),label('bath',-4.8,-1.1,28,BLUE),label('nerve',2,-.35,28,PURPLE),label('electrode',4.5,2.8,28))
    return VGroup(bath,skin,nerve,el,labs)


def deletion_panel():
    p=pair(-3.2,-.15,1.2,.7)
    ch=chip('Piezo2',GREY,size=28).move_to([-3.2,.1,0])
    ch[0].become(DashedVMobject(ch[0].copy(),num_dashes=16))
    deleted=label('deleted',-3.2,-.65,28,GREY)
    # Cross only the chip's left border, leaving its name readable.
    edge=ch.get_left()[0]
    slash=Line([edge-.12,-.2,0],[edge+.2,.4,0],color=GREY,stroke_width=4)
    end=VGroup(RoundedRectangle(width=3.5,height=.5,corner_radius=.2,color=PURPLE,fill_color=PURPLE,fill_opacity=.3).move_to([3.3,-.65,0]),Line([3.3,-.9,0],[3.3,-2,0],color=PURPLE,stroke_width=8))
    channel=chip('Piezo2',BLUE,size=28).move_to([3.3,-.25,0])
    g=VGroup(p,ch,deleted,slash,end,channel,label('Merkel cell',-3.2,-2.65,28,ORANGE),label('ending route ON',3.3,-2.65,28,BLUE))
    return g


def culture_panel():
    # Isolated cell: deliberately no afferent plate or nerve in this panel.
    dish=RoundedRectangle(width=5.5,height=3.65,corner_radius=.4,color=GREY).move_to([-3.25,-.2,0])
    cell=RoundedRectangle(width=1.9,height=1.45,corner_radius=.45,color=ORANGE,fill_color=ORANGE,fill_opacity=.22).move_to([-4.2,-.25,0])
    ch=chip('Piezo2',GREY,size=26).move_to([-4.2,-.25,0])
    ch[0].become(DashedVMobject(ch[0].copy(),num_dashes=16))
    g=VGroup(dish,cell,ch,label('cultured Merkel cell',-3.3,1.3,26,ORANGE),label('deleted',-4.2,-1.35,26,GREY),Line([ch.get_left()[0]-.12,-.55,0],[ch.get_left()[0]+.18,.05,0],color=GREY,stroke_width=4))
    press=Arrow([-4.2,1.0,0],[-4.2,.5,0],buff=.02,color=GREY)
    flat=Line([-2.8,-.2,0],[-1,-.2,0],color=BLUE,stroke_width=4)
    g.add(press,label('press',-5.25,.7,26),flat,label('no current',-1.9,-.8,26,BLUE))
    panel=RoundedRectangle(width=5.4,height=3.65,corner_radius=.4,color=PURPLE).move_to([3.2,-.2,0])
    ending=VGroup(Line([3.1,-1.0,0],[3.1,-.3,0],color=PURPLE,stroke_width=9),RoundedRectangle(width=2.7,height=.4,corner_radius=.14,color=PURPLE,fill_color=PURPLE,fill_opacity=.4).move_to([3.1,-.1,0]),chip('Piezo2',BLUE,size=28).move_to([3.1,.25,0]))
    g.add(panel,ending,label('separate: in the skin',3.2,1.3,26,PURPLE),label('ending route ON',3.2,-1.55,28,BLUE),label('Culture: Woo and colleagues, 2014',-3.25,-2.3,24,GREY))
    return g


Q2='What do you expect to lose?'
Q3='Predict what is left.'


def prediction(which):
    if which==2:
        p=dome(cy=-.1)
        p.remove(p[6],p[7])  # Leave room for the persistent manipulation label.
        # Light targets the Merkel cell; nerve remains unlit.
        beam=Arrow([0,1.38,0],[0,.9,0],buff=.05,color=RED,stroke_width=8)
        p.p.body.set_fill(RED,.28)
        g=VGroup(strip(1,True),p,beam,label('light: silences cells during a held press',0,1.7,28,RED),label(Q2,0,-3.25,32,GOLD))
    else:
        g=VGroup(strip(2,True),culture_panel(),label(Q3,0,-3.05,32,GOLD))
    return g


class S00Title(TitleCard):
    LESSON='Merkel Cells: Touch Receptors That Are Not Neurons'
    TITLE='Take One Route Away'
    def construct(self):
        g=VGroup(T('Merkel Cells:',26,GREY),T('Touch Receptors That Are Not Neurons',26,GREY),T(self.TITLE,48,font=TITLE_FONT),Line(LEFT*1.5,RIGHT*1.5,color=GOLD)).arrange(DOWN,buff=.35)
        self.play(FadeIn(g),run_time=.5); self.finish()


class S01Q(SpokenScene):
    def construct(self):
        self.add(routes())
        self.at('How can you tell')
        self.play(FadeIn(label('Which route makes which phase?',0,-3.05,34,GOLD)),run_time=.45)
        self.finish()


class S02Logic(SpokenScene):
    def construct(self):
        r=routes(True); self.add(r)
        cue=label('Remove the Merkel-cell route; read the phases',0,3.35,28,GOLD)
        self.at('Take one root away')
        self.play(r[1].animate.set_opacity(.2),r[4].animate.set_opacity(.12),FadeIn(cue),run_time=.5)
        self.at('watch which phase')
        fx=lambda t:-5.6+11*t/9
        rr=VGroup(ticks([fx(t) for t in spike_times()],-1.8,.5,GREY,2),label('control reference • illustrative model',0,-3.45,26,GREY))
        for lo,hi,title in [(0,1.9,'Onset'),(1.9,9,'Hold')]:
            x0,x1=fx(lo),fx(hi)
            rr.add(Rectangle(width=x1-x0,height=1.0,stroke_width=0,fill_color=BLUE if lo==0 else GREY,fill_opacity=.1).move_to([(x0+x1)/2,-1.8,0]),Line([x0,-2.45,0],[x1,-2.45,0],color=GREY),label(title,(x0+x1)/2,-2.9,28))
        rr.add(DashedLine([fx(1.9),-2.4,0],[fx(1.9),-1.25,0],color=GREY))
        self.play(FadeIn(rr),run_time=.5)
        self.finish()


class S03Prep(SpokenScene):
    def construct(self):
        p=prep(); self.add(p[1],p[4][0],heading('Ex vivo skin–nerve preparation'))
        self.at('kept alive in')
        self.play(FadeIn(p[0]),FadeIn(p[4][1]),run_time=.4)
        self.at('with its nerve')
        self.play(Create(p[2]),FadeIn(p[3]),FadeIn(p[4][2:]),run_time=.5)
        self.play(FadeIn(label('mouse touch domes',0,-2.75,30,GREY)),run_time=.35)
        self.finish()


class S04Record(SpokenScene):
    def construct(self):
        p=prep(); p.shift(UP*.5)
        # Use the lower margin for a larger bath; recording sits just below it.
        p[0].stretch_to_fit_height(3.65).move_to([-1.7,.6,0])
        self.add(p[0:3],p[4][0:3])
        self.at('An electrode records')
        self.play(FadeIn(p[3]),FadeIn(p[4][3]),run_time=.3)
        probe=Rectangle(width=.6,height=1.0,color=GREY,fill_color=GREY,fill_opacity=.6).move_to([-2,2.5,0])
        self.at('while a probe')
        self.play(FadeIn(probe),FadeIn(label('probe',-.65,2.6,28)),run_time=.25)
        # Bottom of the probe meets the top of the skin, then indents it.
        contact_y=p[1].get_top()[1]+probe.height/2
        self.play(probe.animate.set_y(contact_y),run_time=.25)
        self.at('presses the skin')
        self.play(probe.animate.shift(DOWN*.12),p[1].animate.stretch_to_fit_height(.73),FadeIn(label('press',-.6,1.55,28)),run_time=.25)
        # Same model and same onset boundary, in a separate recording panel.
        fx=lambda t:-5.6+11*t/9
        rec=VGroup(Line([-5.6,-2.05,0],[5.4,-2.05,0],color=GREY),ticks([fx(t) for t in spike_times()],-2.05),label('spikes from one afferent',0,-1.5,28,YELLOW))
        for lo,hi,title in [(0,1.9,'Onset'),(1.9,9,'Hold')]:
            rec.add(Rectangle(width=fx(hi)-fx(lo),height=1.05,stroke_width=0,fill_color=BLUE if lo==0 else GREY,fill_opacity=.1).move_to([(fx(lo)+fx(hi))/2,-2.05,0]),label(title,(fx(lo)+fx(hi))/2,-2.85,28))
        rec.add(DashedLine([fx(1.9),-2.6,0],[fx(1.9),-1.55,0],color=GREY),label('illustrative model • time →',0,-3.35,26,GREY))
        self.play(FadeIn(rec),run_time=.4)
        self.wait(.3)
        self.play(probe.animate.set_y(2.5),p[1].animate.stretch_to_fit_height(.85),run_time=.3)
        self.finish()


class S05Light(SpokenScene):
    def construct(self):
        d=dome(); self.add(d,heading('Light aimed at the touch dome'),label('Merkel cell',0,1.35,28,ORANGE))
        self.at('recorded afferent lacks')
        self.play(Indicate(d.p.disc,color=PURPLE),run_time=.5)
        self.at('Light aimed at')
        beam=Arrow([1.6,2.8,0],[.85,.65,0],buff=.1,color=GREEN,stroke_width=8)
        self.play(GrowArrow(beam),FadeIn(label('light',2.65,2.05,30,GREEN)),d.p.body.animate.set_fill(GREEN,.42),run_time=.6)
        self.at('plus controls')
        self.play(FadeIn(label('Controls support a Merkel-cell effect',0,-3.3,28,GOLD)),run_time=.4)
        self.finish()


class S06Test1(SpokenScene):
    def construct(self):
        self.add(strip(0,True)); p=pair(-2,-.3,1.4,.65); self.add(p,label('Merkel cell',-4.7,.8,28,ORANGE),left('afferent • no opsin',-1.35,-2.45,28,PURPLE),Line([-2,-2.45,0],[-1.5,-2.45,0],color=PURPLE))
        self.at('Light aimed at')
        beam=Arrow([-2,2,0],[-2,.9,0],buff=.04,color=GREEN,stroke_width=8)
        self.play(GrowArrow(beam),FadeIn(label('light',-.75,1.65,28,GREEN)),run_time=.4)
        self.at('depolarizes them')
        self.play(p.body.animate.set_fill(GREEN,.4),run_time=.4)
        self.at('with no touch')
        self.play(FadeIn(chip('NO TOUCH',GREY,size=32).move_to([3,.2,0])),run_time=.4)
        self.finish()


class S07Rev1(SpokenScene):
    def construct(self):
        t=strip(0,True); rr=raster('light',light=True); self.add(t,*[m for m in rr if m is not rr.trace])
        self.at('The afferent fires')
        self.play(Create(rr.trace),run_time=.7)
        self.at('is enough to')
        self.remove(t); self.add(strip(0))
        self.play(FadeIn(label('Merkel cell: sufficient to drive firing',0,-2.65,30,GREEN)),run_time=.4)
        self.finish()


class S08Test2(SpokenScene):
    def construct(self):
        p=prediction(2)
        neutral=p[1].copy(); neutral.p.body.set_fill(ORANGE,.22)
        self.add(strip(1,True),neutral)
        self.at('light silences')
        self.play(neutral.p.body.animate.set_fill(RED,.28),FadeIn(p[2]),FadeIn(p[3]),run_time=.5)
        self.at('What do you expect')
        self.play(FadeIn(p[4]),Indicate(self.mobjects[0][-1],color=GOLD),run_time=.5)
        self.finish()


class S09Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(prediction(2)); self.wait(5)


class S10Rev2(SpokenScene):
    def construct(self):
        t=strip(1,True); self.add(t)
        rr=raster('silenced'); rr[-1].set_opacity(0)
        self.add(*[m for m in rr if m is not rr.trace])
        self.at('sustained firing is suppressed')
        self.play(Create(rr.trace),run_time=.65)
        self.remove(t); self.add(strip(1))
        self.at('The hold needs')
        self.play(FadeIn(label('sustained firing: median tenfold lower (3 afferents)',0,-2.95,26,GREEN)),run_time=.35)
        self.play(FadeIn(label('Green: matches prediction • Amber: does not',0,-3.45,24,GREY)),run_time=.3)
        self.finish()


class S11Test3(SpokenScene):
    def construct(self):
        p=deletion_panel(); self.add(strip(2,True),p[0],p[1],p[4],p[5],p[6],p[7])
        self.at("from the skin's epithelium")
        self.play(FadeIn(p[2]),Create(p[3]),run_time=.45)
        self.at('but not from')
        self.play(Indicate(p[5],color=BLUE),run_time=.5)
        self.finish()


class S12Q3(SpokenScene):
    def construct(self):
        self.add(strip(2,True)); p=culture_panel(); self.add(p[:6],p[10:])
        self.at('lose their touch')
        self.play(FadeIn(p[6:10]),run_time=.5)
        self.at('The ending keeps')
        self.play(Indicate(p[11][2],color=BLUE),run_time=.5)
        self.at('Predict what is left')
        self.play(FadeIn(label(Q3,0,-3.05,32,GOLD)),run_time=.45)
        self.finish()


class S13Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(prediction(3)); self.wait(5)


class S14Rev3(SpokenScene):
    def construct(self):
        t=strip(2,True); rr=raster('deleted',control=True); self.add(t,*[m for m in rr if m is not rr.trace])
        onset=VGroup(*[tick for tick,v in zip(rr.trace,model('deleted')) if v<1.9])
        hold=VGroup(*[tick for tick,v in zip(rr.trace,model('deleted')) if v>=1.9])
        self.at('The onset stays')
        self.play(Create(onset),run_time=.6)
        self.at('The hold loses')
        self.play(Create(hold),run_time=.75)
        self.remove(t); self.add(strip(2))
        self.at('cleanest split')
        self.play(FadeIn(label('Normal sustained firing lost',0,-2.95,28,GREEN)),run_time=.35)
        self.finish()


class S15Limit(SpokenScene):
    def construct(self):
        d=dome(); self.add(d,heading('One limit'),label('Merkel cell',0,1.35,28,ORANGE))
        self.at('This deletion covers')
        key=label('Epithelial driver: ALL skin epithelium',0,2.5,30,BLUE)
        self.play(FadeIn(key),d[0].animate.set_fill(BLUE,.22),*[m.animate.set_fill(BLUE,.25) for m in d[1:5]],d.p.body.animate.set_fill(BLUE,.25),run_time=.7)
        self.at('not only the')
        self.play(FadeIn(label('not restricted to Merkel cells',0,-3.25,30,GOLD)),run_time=.4)
        self.finish()


class S16Test4(SpokenScene):
    def construct(self):
        self.add(strip(3,True)); d=dome(); self.add(d)
        self.at('Remove the')
        slot=DashedVMobject(d.p.body.copy(),num_dashes=28).set_color(ORANGE)
        self.play(FadeOut(d.p.body),Create(slot),FadeOut(d[-2]),FadeIn(label('ending remains',2,-2.55,28,PURPLE)),FadeIn(label('no Merkel cells',0,1.9,28,ORANGE)),run_time=.6)
        self.at('during development')
        self.play(FadeIn(label('(Atoh1 deleted during development)',0,-3.25,28,ORANGE)),run_time=.4)
        self.finish()


class S17Rev4a(SpokenScene):
    def construct(self):
        self.add(strip(3,True)); rr=raster('empty'); self.add(rr)
        self.at('still respond to touch')
        short=raster('short'); self.play(Create(short.trace),run_time=.6)
        self.at('before the press ends')
        fx=lambda t:-5.6+11*t/9
        last=float(model('short')[-1]); x0=fx(last)+.08; x1=fx(9)
        br=VGroup(Line([x0,.05,0],[x1,.05,0],color=GOLD),Line([x0,-.1,0],[x0,.2,0],color=GOLD),Line([x1,-.1,0],[x1,.2,0],color=GOLD),label('response stops here → silence',(x0+x1)/2,.52,27,GOLD))
        self.play(Create(br),run_time=.4)
        self.at('That is called')
        self.play(FadeIn(label('intermediately adapting',1.7,-1.65,28,GOLD)),run_time=.45)
        self.finish()


class S18Rev4b(SpokenScene):
    def construct(self):
        t=strip(3,True); self.add(t)
        base=-2.3; scale=3.75/238
        axes=VGroup(Line([-4.6,base,0],[4.9,base,0],color=GREY),Line([-4.6,base,0],[-4.6,1.65,0],color=GREY),label('peak firing (Hz)',-6,-.25,28).rotate(PI/2))
        for v in [0,100,200]:
            y=base+v*scale
            axes.add(label(str(v),-5.15,y,26,GREY),Line([-4.7,y,0],[-4.5,y,0],color=GREY))
        def bar(v,x,c): return Rectangle(width=1.55,height=v*scale,stroke_width=0,fill_color=c,fill_opacity=.75).move_to([x,base+v*scale/2,0])
        a=bar(238,-2.2,GREY); b=bar(238,2.2,GOLD)
        self.add(axes,a,label('control',-2.2,-2.7,28,GREY),label('238',-2.2,1.7,28))
        self.at('the onset falls')
        self.remove(t); self.add(strip(3))
        self.at('Peak firing drops')
        self.add(b)
        self.play(Transform(b,bar(79,2.2,GOLD)),run_time=.7)
        self.play(FadeIn(label('79',2.2,-.7,28,GOLD)),FadeIn(label('no Merkel cells',2.2,-2.7,28,GOLD)),FadeIn(label('group means • 79 / 238 = 33%',0,-3.35,28,GREY)),run_time=.3)
        self.finish()


class S19Partly(SpokenScene):
    def construct(self):
        self.add(table(4))
        self.at('That row only')
        outline=RoundedRectangle(width=12.9,height=.84,corner_radius=.06,color=GOLD,stroke_width=2).move_to([.1,-.46,0])
        self.play(Create(outline),FadeIn(label('hold cut short: as predicted',-3,-1.55,26,GREEN)),FadeIn(label('onset also lower: not predicted',3,-1.55,26,GOLD)),run_time=.4)
        self.at('A developmental loss')
        self.play(FadeIn(label('Two possible explanations • mechanism unknown',0,-2.05,27,GOLD)),run_time=.4)
        self.at("the cell's own signal")
        cell=pair(-4.7,-2.95,.4,.25)
        signal=VGroup(cell,Arrow([-4.05,-2.95,0],[-3.2,-2.95,0],buff=.03,color=ORANGE),left('Cell’s own\nsignal',-2.95,-2.95,24,ORANGE))
        self.play(FadeIn(signal),run_time=.3)
        self.at('or a changed skin')
        skin=Polygon([1,-3.35,0],[1,-2.85,0],[1.5,-2.55,0],[2,-2.85,0],[2.6,-2.7,0],[2.6,-3.35,0],color=GREY,fill_color=GREY,fill_opacity=.2)
        self.play(FadeIn(VGroup(skin,left('Altered\nskin',3,-2.95,24,GREY))),run_time=.3)
        self.finish()


class S20Tetanus(SpokenScene):
    def construct(self):
        self.add(table(4))
        self.at('Blocking vesicle release')
        # Fifth row and explanatory line enter together; citation lives in row.
        five=table(5)
        self.play(*[FadeOut(m) for m in list(self.mobjects)],FadeIn(five),FadeIn(label('Release blocked: both phases lower',0,-2.15,30,GREY)),run_time=.4)
        self.at('also reduced both')
        self.play(Indicate(five[-4],color=GREY),run_time=.4)
        self.play(FadeIn(legend(-2.8)),run_time=.3)
        self.finish()


def both():
    g=VGroup()
    for x,title in [(-3.3,'Onset'),(3.3,'Hold')]:
        g.add(RoundedRectangle(width=5.8,height=4.25,corner_radius=.25,color=GREY).move_to([x,.05,0]),label(title,x,2.55,32))
        st=spike_times(); st=st[st<1.9] if x<0 else st[st>=1.9]
        lo,hi=(0,1.9) if x<0 else (1.9,9)
        # Same time scale: onset appears as a burst, hold as a sustained irregular train.
        xx=[x-2.3+.8*(t-lo) for t in st] if x<0 else [x-2.3+4.6*(t-lo)/(hi-lo) for t in st]
        g.add(ticks(xx,1.45,.5),label('ending route',x-1.45,-1.65,26,PURPLE),label('Merkel route',x+1.4,-1.65,26,ORANGE))
        for dx,c in [(-1.45,PURPLE),(1.4,ORANGE)]:
            g.add(Arrow([x+dx,-1.25,0],[x+dx,.7,0],buff=.07,color=c,stroke_width=4))
        # Distinct release arrow reaches each phase with equal graphical weight.
        g.add(Arrow([x,-.8,0],[x,.7,0],buff=.06,color=TEAL,stroke_width=4),label('release',x,-.95,26,TEAL))
    g.add(label('Release (probably Merkel cell) may help BOTH',0,-2.65,28,TEAL),label('Mainly • contributions are not measured by arrow width',0,-3.3,26,GOLD))
    return g


class S21Both(SpokenScene):
    def construct(self):
        b=both(); self.add(b,heading('Release may help both phases'))
        self.at('probably from Merkel cells')
        self.play(Indicate(b[-2],color=TEAL),run_time=.45)
        self.at('may help with')
        self.play(Indicate(b[7],color=TEAL),run_time=.45)
        self.finish()


class S22Beat(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(both(),heading('Release may help both phases')); self.wait(4)


class S23Take(SpokenScene):
    def construct(self):
        self.add(table(5))
        self.at('That is why')
        self.play(FadeIn(label('MAINLY • not an exclusive split',0,-2.0,30,GOLD)),run_time=.4)
        self.at('In mouse')
        self.play(FadeIn(label('In mouse touch domes',0,-2.6,28,GREY)),run_time=.35)
        self.at('the ending mainly')
        ending=label('Ending: mainly feels the change',0,-3.25,28,PURPLE)
        self.play(FadeIn(ending),run_time=.35)
        self.at('cell mainly holds')
        hold=label('Merkel cell: mainly holds the press',0,-3.25,28,ORANGE)
        self.play(FadeOut(ending),run_time=.15)
        self.play(FadeIn(hold),run_time=.25)
        self.at('Neither acts alone')
        self.clear()
        self.add(table(5),label('MAINLY • not an exclusive split',0,-2.0,30,GOLD),label('In mouse touch domes',0,-2.6,28,GREY))
        self.play(FadeIn(label('Neither acts alone.',0,-3.25,32,GOLD)),run_time=.3)
        self.finish()


class S24End(EndCard):
    LINE='In mouse touch domes the ending mainly feels the change, the Merkel cell mainly holds the press; neither acts alone.'
    def construct(self):
        g=VGroup(T('In mouse touch domes',30,GREY),T('The ending mainly feels the change.',34,font=TITLE_FONT),T('The Merkel cell mainly holds the press.',34,font=TITLE_FONT),T('Neither acts alone.',36,GOLD,font=TITLE_FONT)).arrange(DOWN,buff=.5)
        self.play(FadeIn(g),run_time=.5); self.finish()
