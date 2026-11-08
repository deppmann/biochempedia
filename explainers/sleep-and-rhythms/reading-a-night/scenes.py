"""Reading a Night — reviewer fix round.

COLOR MAP: pressure/N3/orexin ORANGE #F29E4C; clock/REM/levels PURPLE
#B58CD9; waking GREEN #83C167; inhibition RED #FC6255; recording TEXT;
SCN/interactive TEAL #3FB8C0; structure GREY #8B93A1.
All recordings are computed schematic signals, never patient data. Pressure
uses the lesson's 18 h / 4 h model and cosine thresholds. The hypnogram uses
all 960 lesson practice epochs, reordered to include late N3. No molecules.
"""
import numpy as np
from bp_style import *
PURPLE = '#B58CD9'
ORANGE = '#F29E4C'
MUTED = '#BDC4D0'


def heading(text, color=TEXT):
    return T(text, 34, color).move_to([0, 3.12, 0])


def lp(xs, ys, color=TEXT, width=3):
    return VMobject(color=color, stroke_width=width).set_points_as_corners(
        [np.array([x, y, 0]) for x, y in zip(xs, ys)])


def level(t, upper=True):
    return (.67 if upper else .17) + .12*np.cos(2*np.pi*(np.asarray(t)-17)/24)


def model(end=40, dt=.01):
    t = np.arange(7, end+dt/2, dt)
    s = np.zeros(len(t)); s[0] = .23
    asleep = np.zeros(len(t), bool); state = False
    for i in range(1, len(t)):
        if state and s[i-1] <= level(t[i-1], False): state = False
        elif not state and s[i-1] >= level(t[i-1]): state = True
        asleep[i] = state
        s[i] = s[i-1]*np.exp(-dt/4) if state else 1-(1-s[i-1])*np.exp(-dt/18)
    return t, s, asleep


def signal(kind, t):
    """Analytic schematic signals, seconds; EEG normalized except N3 epoch."""
    t = np.asarray(t)
    beta = .40*np.sin(2*np.pi*19*t)+.18*np.sin(2*np.pi*27*t+.7)
    if kind == 'alpha': return .75*np.sin(2*np.pi*10*t)
    if kind == 'theta': return .72*np.sin(2*np.pi*6*t)
    if kind == 'slow': return np.sin(2*np.pi*t)
    if kind == 'n2':
        return (.15*np.sin(2*np.pi*6*t) + .72*np.exp(-((t-.65)/.30)**2)*np.sin(2*np.pi*13*t)
                - .95*np.exp(-((t-1.55)/.10)**2)+.80*np.exp(-((t-1.80)/.20)**2))
    if kind == 'eog':
        # A cluster of sharp, oppositely directed eye deflections.
        centers = np.arange(.85, 2.65, .15)
        return sum((1 if i % 2 == 0 else -1)*(.8+.15*np.sin(i))*
                   np.maximum(0, 1-np.abs(t-c)/.065) for i,c in enumerate(centers))
    if kind == 'quiet': return .20*np.sin(2*np.pi*.7*t)+.08*np.sin(2*np.pi*1.7*t)
    if kind == 'emg': return .52*np.sin(2*np.pi*23*t)+.25*np.sin(2*np.pi*31*t)
    if kind == 'flat': return .025*np.sin(2*np.pi*23*t)
    return beta


def trace(kind, x, y, w, seconds=4, amp=.65, color=TEXT, width=2.2):
    t = np.linspace(0, seconds, max(900, int(seconds*120)))
    return lp(x+w*t/seconds, y+amp*signal(kind,t), color, width)


def pressure_plot(x=-4.8, y=-2.15, w=10.5, h=4.5):
    t = np.linspace(0, 6.5, 500)
    axes = VGroup(Line([x,y,0],[x+w,y,0],color=MUTED),
                  Line([x,y,0],[x,y+h,0],color=MUTED),
                  T('sleep pressure',28,ORANGE).rotate(PI/2).move_to([x-.65,y+h/2,0]),
                  T('sleep onset',26,MUTED).move_to([x+.8,y-.4,0]),
                  T('6.5 h asleep',26,MUTED).move_to([x+w-.9,y-.4,0]))
    return axes, lp(x+w*t/6.5, y+h*np.exp(-t/4), ORANGE, 6)


def epochs():
    seq=[('W',30)]
    # N3 totals 192; the 12-epoch fourth-cycle bout falls after 4 h.
    for n1,n3,rem,n2 in zip([18,10,8,6,6],[100,65,15,12,0],
                           [20,32,45,60,71],[42,73,100,114,103]):
        seq.extend([('N1',n1),('N2',n2//2),('N3',n3),('N2',n2-n2//2),('REM',rem)])
    seq.append(('W',30))
    # Merge adjacent N2 when N3 is absent: no stray joins or zero-length steps.
    out=[]
    for stage,count in seq:
        if not count: continue
        if out and out[-1][0]==stage: out[-1]=(stage,out[-1][1]+count)
        else: out.append((stage,count))
    return out


def hypno(question=False):
    x=-4.9; w=10.7
    ys={'W':1.8,'REM':1.10,'N1':.4,'N2':-.3,'N3':-1.0}
    if question: ys={'W':1.95,'REM':.85,'N1':-.25,'N2':-1.35,'N3':-2.45}
    bottom=-2.75 if question else -1.35
    top=2.30 if question else 2.05
    axes=VGroup(T('stage',28,MUTED).move_to([-5.55,2.72 if question else 2.5,0]))
    for k,v in ys.items():
        axes.add(T(k,28,MUTED).move_to([-5.55,v,0]),
                 Line([x,v,0],[x+w,v,0],color=GREY,stroke_width=.6).set_opacity(.3))
    axes.add(Line([x,bottom,0],[x+w,bottom,0],color=MUTED),
             DashedLine([x+w/2,bottom,0],[x+w/2,top,0],color=MUTED))
    for hour in range(9):
        xx=x+w*hour/8
        axes.add(Line([xx,bottom,0],[xx,bottom-.10,0],color=MUTED),
                 T(str(hour),26,MUTED).move_to([xx,bottom-.31,0]))
    axes.add(T('hours in bed',26,MUTED).move_to([.5,bottom-.70,0]))
    if question:
        axes.add(T('first half',28,MUTED).move_to([-2.25,2.50,0]),
                 T('second half',28,MUTED).move_to([3.1,2.50,0]))
    g=VGroup(); n3=VGroup(); rems=VGroup(); k=0; old=None
    for stage,count in epochs():
        a=x+w*k/960; b=x+w*(k+count)/960; yy=ys[stage]
        if old is not None: g.add(Line([a,old,0],[a,yy,0],color=MUTED,stroke_width=2))
        seg=Line([a,yy,0],[b,yy,0],color=ORANGE if stage=='N3' else PURPLE if stage=='REM' else TEXT,stroke_width=7)
        (n3 if stage=='N3' else rems if stage=='REM' else g).add(seg)
        k+=count; old=yy
    return axes,g,n3,rems


def question_frame():
    axes,*_=hypno(True)
    question=T('Where does most N3 fall?',38).move_to([-.65,3.17,0])
    ring=Circle(radius=.29,color=MUTED,stroke_width=3).move_to([5.65,3.14,0])
    return VGroup(axes,question,ring)


def tbar(a,b):
    a=np.array(a); b=np.array(b); d=(b-a)/np.linalg.norm(b-a)
    p=np.array([-d[1],d[0],0])*.20
    return VGroup(Line(a,b,color=RED,stroke_width=5),Line(b-p,b+p,color=RED,stroke_width=6))


def switch_boxes(sleep=False, neutral=False):
    left=chip('VLPO\nsleep-active neurons',ORANGE,30,pad=.35).move_to([-3.65,.25,0])
    right=chip('wake-promoting\ngroups',GREEN,30,pad=.35).move_to([3.65,.25,0])
    if not neutral:
        dim = right if sleep else left
        dim[0].set_stroke(opacity=.50).set_fill(opacity=.08)
        dim[1].set_color(MUTED).set_opacity(1)
    # Two separate box-to-box inhibitory connections with true flat heads.
    arrows=VGroup(tbar([left.get_right()[0],.65,0],[right.get_left()[0]-.08,.65,0]),
                  tbar([right.get_left()[0],-.15,0],[left.get_right()[0]+.08,-.15,0]))
    return VGroup(left,right,arrows)


def switch_panel(sleep=True):
    # Readable vertical companion for the model graph (not a shrunken seesaw).
    a=chip('VLPO\nsleep active',ORANGE,30,pad=.3).move_to([4.75,1.35,0])
    b=chip('wake\ngroups',GREEN,30,pad=.3).move_to([4.75,-.80,0])
    dim = b if sleep else a
    dim[0].set_stroke(opacity=.50).set_fill(opacity=.08)
    dim[1].set_color(MUTED).set_opacity(1)
    top=a.get_bottom()[1]; low=b.get_top()[1]
    return VGroup(a,b,tbar([4.45,top,0],[4.45,low+.03,0]),
                  tbar([5.05,low,0],[5.05,top-.03,0]),
                  T('bright = active',26,MUTED).move_to([4.65,2.50,0]))


def wall_switch(up=True):
    x=-.8
    plate=RoundedRectangle(width=3.4,height=5.4,corner_radius=.25,color=MUTED,
                           fill_color='#202631',fill_opacity=1).move_to([x,0,0])
    screws=VGroup(*[Circle(radius=.09,color=MUTED).move_to([x,y,0]) for y in [-2.38,2.38]])
    slot=RoundedRectangle(width=.62,height=2.7,corner_radius=.15,color=MUTED,
                          fill_color=BG,fill_opacity=1).move_to([x,0,0])
    base=Circle(radius=.34,color=MUTED,fill_color=GREY,fill_opacity=1).move_to([x,0,0])
    tip=np.array([x,1.15 if up else -1.15,0])
    lever=VGroup(Line([x,0,0],tip,color=GREEN if up else ORANGE,stroke_width=19),
                 Circle(radius=.29,color=TEXT,fill_color=TEXT,fill_opacity=1).move_to(tip))
    labels=VGroup(T('wake',32,GREEN).move_to([x,2,0]),T('sleep',32,ORANGE).move_to([x,-2,0]))
    # Palm, wrist, extended index finger, thumb and curled lower fingers.
    palm=RoundedRectangle(width=1.55,height=1.45,corner_radius=.35,color=ORANGE,
                          fill_color=ORANGE,fill_opacity=.48).move_to([3.25,.20,0])
    index=RoundedRectangle(width=3.65,height=.48,corner_radius=.23,color=ORANGE,
                           fill_color=ORANGE,fill_opacity=.6).move_to([1.28,.86,0])
    nail=Arc(radius=.18,start_angle=-PI/2,angle=PI,color=TEXT).move_to([-.30,.86,0])
    thumb=RoundedRectangle(width=1.15,height=.43,corner_radius=.2,color=ORANGE,
                           fill_color=ORANGE,fill_opacity=.6).rotate(-.6).move_to([2.65,-.42,0])
    fingers=VGroup(*[RoundedRectangle(width=.9,height=.31,corner_radius=.13,color=ORANGE,
                                     fill_color=ORANGE,fill_opacity=.6).move_to([3.12,yy,0]) for yy in [-.05,-.39]])
    wrist=Polygon([3.9,.65,0],[4.9,.65,0],[4.9,-.55,0],[3.9,-.55,0],
                  color=ORANGE,fill_color=ORANGE,fill_opacity=.48)
    hand=VGroup(wrist,palm,index,nail,thumb,fingers)
    return VGroup(plate,screws,slot,base,lever,labels,hand)


class S00Title(TitleCard):
    LESSON='Circadian Rhythms and Sleep'
    TITLE='Reading a Night'
    def construct(self):
        g=VGroup(T('BIOCHEMISTRYPEDIA',26,TEAL),T(self.LESSON,28,MUTED),
                 T(self.TITLE,54,font=TITLE_FONT),Line(LEFT*1.3,RIGHT*1.3,color=GOLD)).arrange(DOWN,buff=.4)
        self.add(g); self.finish()


class S01Q1(SpokenScene):
    def construct(self):
        axes,curve=pressure_plot(); dot=Dot(curve.get_start(),color=ORANGE,radius=.12)
        self.add(axes,curve,dot,heading('Pressure drains during sleep',ORANGE))
        self.at('Sleep pressure'); self.wait(.2)
        self.at('and it drains'); self.play(MoveAlongPath(dot,curve),run_time=1.15)
        self.at('a recording show',lead=.42)
        self.play(FadeIn(T('What does a recording show?',36).move_to([0,-3.20,0])),run_time=.3)
        self.wait(1.5)
        self.finish()


class S02Psg(SpokenScene):
    def construct(self):
        self.add(heading('30 s scoring windows · trace excerpts').shift(UP*.16))
        x=-4.5; w=10.2
        rows=VGroup()
        t=np.linspace(0,90,10800)
        # Each 30-s scoring window shows a representative 2-s excerpt,
        # explicitly labelled above, so real waveform detail stays resolvable.
        local=(t % 30)/15
        beta=signal('beta',local)*(.75+.20*np.sin(2*np.pi*.7*local))
        theta=signal('theta',local)
        eeg=np.where(t<30,beta,np.where(t<60,theta*.65,signal('n2',local)))
        eog=np.where(t<30,signal('quiet',local),np.where(t<60,.15*np.sin(2*np.pi*.25*local),.025*np.sin(2*np.pi*.3*local)))
        envelope=.18+.82*np.exp(-((local-.40)/.15)**2)+.65*np.exp(-((local-1.4)/.22)**2)
        emg=signal('emg',local)*envelope*np.where(t<30,1,np.where(t<60,.55,.30))
        for label,z,y in [('EEG',eeg,1.55),('EOG',eog,-.15),('EMG',emg,-1.85)]:
            rows.add(T(label,30).move_to([-5.55,y,0]),lp(x+w*t/90,y+.75*z,TEXT,1.3))
        self.add(rows)
        window=Rectangle(width=3.4,height=4.95,color=TEAL,fill_color=TEAL,fill_opacity=.08).move_to([-2.8,-.15,0])
        tag=chip('W',TEAL,28,pad=.12).move_to([-2.8,2.72,0])
        bracket=VGroup(Line([-4.5,-2.85,0],[-1.1,-2.85,0],color=TEAL),
                       T('30 s',28,TEAL).move_to([-2.8,-3.17,0]))
        self.add(window,tag,bracket)
        self.at('Sleep is read'); self.wait(.1)
        self.at('eye movements')
        self.play(Indicate(rows[2],color=TEAL),window.animate.shift(RIGHT*3.4),
                  bracket.animate.shift(RIGHT*3.4),tag.animate.shift(RIGHT*3.4),run_time=.35)
        self.play(Transform(tag,chip('N1',TEAL,28,pad=.12).move_to(tag)),run_time=.12)
        self.at('chin muscle'); self.play(Indicate(rows[4],color=TEAL),run_time=.35)
        self.at('The night')
        self.play(window.animate.shift(RIGHT*3.4),bracket.animate.shift(RIGHT*3.4),
                  tag.animate.shift(RIGHT*3.4),run_time=.35)
        self.play(Transform(tag,chip('N2',TEAL,28,pad=.12).move_to(tag)),run_time=.12)
        self.finish()


class S03Waves(SpokenScene):
    def construct(self):
        self.add(heading('Slower, larger waves · schematic'))
        panels=VGroup(*[RoundedRectangle(width=w,height=5.5,corner_radius=.15,color=c).move_to([x,-.1,0])
                       for x,w,c in [(-4.7,2.7,GREY),(-.15,6.1,GREY),(4.65,2.7,PURPLE)]])
        wake=VGroup(T('waking',30).move_to([-4.7,2.23,0]),
                    T('beta',26,MUTED).move_to([-4.7,1.63,0]),trace('beta',-5.8,.87,2.2,1,.65),
                    T('eyes closed',26,MUTED).move_to([-4.7,-.15,0]),T('alpha',26,MUTED).move_to([-4.7,-.65,0]),
                    trace('alpha',-5.8,-1.6,2.2,1,.75))
        nrem=VGroup(T('NREM deepening →',30,ORANGE).move_to([-.15,2.23,0]))
        for x,kind,label,amp in [(-2.95,'theta','N1',.55),(-.95,'n2','N2',.85),(1.05,'slow','N3',1.20)]:
            nrem.add(T(label,28,ORANGE).move_to([x+.82,1.58,0]),trace(kind,x,0,1.65,2,amp))
        nrem.add(T('theta',26,MUTED).move_to([-2.15,-1.08,0]),
                 T('spindle',26,MUTED).move_to([-.15,.98,0]),
                 Line([-.45,.76,0],[-.42,.40,0],color=MUTED),
                 T('K-complex',26,MUTED).move_to([-.10,-1.20,0]),
                 Line([.55,-.98,0],[.4,-.55,0],color=MUTED))
        rem=VGroup(T('REM',30,PURPLE).move_to([4.65,2.23,0]),trace('beta',3.55,.65,2.2,1,.7,color=PURPLE),
                   T('wake-like EEG',26,PURPLE).move_to([4.65,-.55,0]),T('see next →',26,MUTED).move_to([4.65,-1.25,0]))
        self.add(panels,wake,nrem,rem)
        neurons=VGroup(*[Dot([1.28+i*.39,-1.75,0],radius=.13,color=ORANGE) for i in range(4)])
        tag=T('active',26,ORANGE).move_to([1.88,-2.33,0])
        self.at('Slower larger'); self.wait(.1)
        self.at('cortical neurons'); self.play(FadeIn(neurons),run_time=.3)
        self.at('are active'); self.play(FadeIn(tag),neurons.animate.set_opacity(1),run_time=.25)
        self.at('then silent'); self.play(neurons.animate.set_opacity(.18),Transform(tag,T('silent',26,MUTED).move_to(tag)),run_time=.25)
        self.at('in step'); self.play(neurons.animate.set_opacity(1),Transform(tag,T('in step',26,ORANGE).move_to(tag)),run_time=.25)
        self.at('That happens'); self.play(Indicate(nrem,color=ORANGE,scale_factor=1.015),run_time=.45)
        self.finish()


class S04N3(SpokenScene):
    def construct(self):
        self.add(heading('N3 · deepest NREM',ORANGE))
        x=-5.1; w=10.4; y=.05; scale=.023
        t=np.linspace(0,30,7200)
        # Fifteen 2-Hz, 100-µV peak-to-peak waves in 7.5 s = 25% of epoch.
        rng=np.random.default_rng(43)
        background=np.interp(t,np.linspace(0,30,420),rng.normal(0,1.5,420))
        z=np.where(t<7.5,50*np.sin(2*np.pi*2*t),background)
        box=Rectangle(width=w,height=3.65,color=MUTED).move_to([x+w/2,y,0])
        wave=lp(x+w*t/30,y+scale*z,TEXT,2)
        highlight=Rectangle(width=w/4,height=3.65,color=ORANGE,fill_color=ORANGE,fill_opacity=.12).move_to([x+w/8,y,0])
        timebar=VGroup(Line([x,-2.1,0],[x+w,-2.1,0],color=MUTED),T('30 s epoch · frontal EEG schematic',28,MUTED).move_to([0,-2.5,0]))
        self.add(box,wave,timebar)
        ampbar=VGroup(Line([5.72,-.8625,0],[5.72,.8625,0],color=ORANGE),
                      Line([5.57,-.8625,0],[5.87,-.8625,0],color=ORANGE),
                      Line([5.57,.8625,0],[5.87,.8625,0],color=ORANGE),
                      T('75 µV',26,ORANGE).rotate(PI/2).move_to([6.14,0,0]))
        self.add(ampbar,T('0.5–2 Hz · peak-to-peak above 75 µV',30,ORANGE).move_to([0,2.38,0]))
        self.at('In stage'); self.wait(.1)
        self.at('large slow waves')
        self.play(FadeIn(highlight),run_time=.4)
        self.at('take up'); self.play(FadeIn(T('25% shown here · at least 20% required',30,ORANGE).move_to([0,-3.12,0])),run_time=.4)
        self.finish()


class S05Rem(SpokenScene):
    def construct(self):
        self.add(heading('Similar EEG; different eyes and muscle'))
        rows=[]
        for x,label,c in [(-4.9,'waking',GREEN),(1.75,'REM',PURPLE)]:
            self.add(T(label,32,c).move_to([x+1.95,2.48,0]))
            col=VGroup()
            for name,kind,y in [('EEG','beta',1.38),('EOG','quiet' if label=='waking' else 'eog',-.4),('EMG','emg' if label=='waking' else 'flat',-2.15)]:
                col.add(T(name,28,MUTED).move_to([x-.72,y,0]),trace(kind,x,y,3.9,4,.65,color=TEXT if label=='waking' else PURPLE,
                         width=4 if label=='REM' and name=='EMG' else 2.2))
            self.add(col); rows.append(col)
        self.at('In rem sleep'); self.wait(.1)
        self.at('The eyes',lead=.38)
        eyes=T('rapid eye movements',28,PURPLE).move_to([3.65,.45,0])
        self.play(FadeIn(eyes),Create(Line([3.65,.20,0],[3.55,-.07,0],color=PURPLE)),
                  Indicate(rows[1][3],color=PURPLE,scale_factor=1.03),run_time=.4)
        self.at('the muscles',lead=.38)
        self.play(FadeIn(T('muscle tone lowest',28,PURPLE).move_to([3.65,-3.03,0])),
                  Create(Line([3.65,-2.78,0],[3.65,-2.24,0],color=PURPLE)),run_time=.35)
        self.finish()


class S06Q2(SpokenScene):
    def construct(self):
        self.add(question_frame()); self.at('So where'); self.finish()


class S07Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(question_frame())
        fill=Arc(radius=.29,start_angle=PI/2,angle=-TAU+.001,color=TEAL,stroke_width=9).move_arc_center_to([5.65,3.14,0])
        self.play(Create(fill),run_time=5,rate_func=linear)


class S08Reveal(SpokenScene):
    def construct(self):
        axes,g,n3,rems=hypno()
        self.add(axes,T('schematic hypnogram, not data',28,MUTED).move_to([0,3.22,0]))
        # The explanatory pressure curve is already present when N3 is revealed.
        t=np.linspace(0,8,500)
        pressure=lp(-4.9+10.7*t/8,-3.33+1.45*np.exp(-t/4),ORANGE,5)
        # Lower pressure plot has its own baseline and high-contrast adjacent label.
        self.add(pressure,T('pressure',26,ORANGE).move_to([-5.52,-2.75,0]),
                 Line([-4.9,-3.33,0],[5.8,-3.33,0],color=GREY))
        self.at('Early'); self.play(Create(g),Create(n3),run_time=.55)
        bracket=VGroup(Line([-4.9,2.06,0],[.45,2.06,0],color=ORANGE),
                       Line([-4.9,1.96,0],[-4.9,2.16,0],color=ORANGE),
                       Line([.45,1.96,0],[.45,2.16,0],color=ORANGE),
                       T('most N3: first half',28,ORANGE).move_to([-2.2,2.55,0]))
        self.at('pressure is highest'); self.play(FadeIn(bracket),run_time=.4)
        self.at('REM sleep grows'); self.play(Create(rems),FadeIn(T('REM longer toward morning',27,PURPLE).move_to([3.5,2.55,0])),run_time=.6)
        self.at('with the clock'); self.finish()


class S09Switch1(SpokenScene):
    def construct(self):
        g=switch_boxes(neutral=True)
        self.add(g[0],g[1],heading('How does the brain flip?'),
                 T('VLPO (ventrolateral preoptic area)',28,MUTED).move_to([0,-2.38,0]))
        self.at('How does'); self.wait(.1)
        self.at('In one model'); self.play(FadeIn(T('one model · mutual inhibition',32,PURPLE).move_to([0,2.25,0])),run_time=.35)
        self.at('inhibit each other'); self.play(Create(g[2]),run_time=.5)
        self.add(T('flat end = inhibition',28,RED).move_to([0,-1.38,0]))
        self.finish()


class S10Switch2(SpokenScene):
    def construct(self):
        g=switch_boxes(True)
        self.add(g,heading('One model · a quick switch'),
                 T('bright = active · dim = inhibited',30,MUTED).move_to([0,-1.7,0]),
                 T('SLEEP',32,ORANGE).move_to([0,2.08,0]))
        state=self.mobjects[-1]
        self.at('Whichever side'); self.wait(.1)
        self.at('silences the other'); self.play(Indicate(g[2][0],color=RED),run_time=.35)
        self.at('flips quickly'); self.play(Transform(g,switch_boxes(False)),Transform(state,T('WAKE',32,GREEN).move_to(state)),run_time=.20)
        # Both states hold for >1.5 s; no second rapid flip obscures the comparison.
        self.finish()


class S11Switch3(SpokenScene):
    def construct(self):
        self.add(heading('A switch with a memory · one model'))
        t,s,asleep=model(); i=np.where(asleep)[0][0]
        hours=np.linspace(0,6.5,650)
        ss=s[i]*np.exp(-hours/4)
        x=-4.85; w=7.3; bottom=-2.65
        def yy(v): return bottom+5.1*np.asarray(v)/.8
        xs=x+w*hours/6.5
        axes=VGroup(Line([x,bottom,0],[x+w,bottom,0],color=MUTED),
                    Line([x,bottom,0],[x,2.50,0],color=MUTED),
                    T('sleep pressure',28,ORANGE).rotate(PI/2).move_to([-5.73,-.05,0]),
                    T('hours asleep',28,MUTED).move_to([-.95,-3.35,0]))
        for h in [0,2,4,6.5]:
            xx=x+w*h/6.5
            axes.add(Line([xx,bottom,0],[xx,bottom-.1,0],color=MUTED),
                     T(str(h).removesuffix('.0'),26,MUTED).move_to([xx,-2.98,0]))
        began=yy(ss[0]); finish=yy(ss[-1])
        hi=DashedLine([x,began,0],[x+w,began,0],color=PURPLE,stroke_width=3)
        lo=Line([x,finish,0],[x+w,finish,0],color=PURPLE,stroke_width=3)
        labels=VGroup(T('level where sleep began',27,PURPLE).move_to([-1.25,began+.36,0]),
                      Line([-1.25,began+.15,0],[-1.25,began,0],color=PURPLE),
                      T('level where waking can win',26,PURPLE).move_to([-.95,finish-.38,0]),
                      Line([-.95,finish-.15,0],[-.95,finish,0],color=PURPLE))
        panel=switch_panel(True)
        self.add(axes,hi,lo,labels,panel)
        dot=Dot([x,began,0],color=ORANGE,radius=.12); self.add(dot)
        self.at('Once sleep wins'); self.wait(.1)
        self.at('pressure must drain')
        curve=lp(xs,yy(ss),ORANGE,5)
        # End the pressure animation just as waking can win is spoken.
        self.play(Create(curve),MoveAlongPath(dot,curve),run_time=2.65)
        self.at('waking can win'); self.play(Transform(panel,switch_panel(False)),run_time=.2)
        self.at('That memory')
        gap=DoubleArrow([2.65,finish,0],[2.65,began,0],buff=0,color=PURPLE,stroke_width=4)
        self.play(GrowArrow(gap),FadeIn(T('gap',26,PURPLE).move_to([3.18,-.15,0])),run_time=.5)
        self.finish()


class S12Orexin1(SpokenScene):
    def construct(self):
        g=wall_switch(); self.add(*g[:6],g[6])
        label=T('orexin neurons',32,ORANGE).move_to([3.2,2.3,0])
        self.add(label,Line([3.2,1.96,0],[3.2,1.1,0],color=ORANGE))
        self.at('Orexin neurons'); self.wait(.1)
        self.at('thought to'); self.play(FadeIn(T('thought to hold wake',32,MUTED).move_to([0,3.18,0])),run_time=.3)
        self.at('like a finger'); self.play(g[6].animate.shift(UP*.15),run_time=.4)
        self.finish()


def person(slump=False):
    # Filled seated silhouette with arms, bent legs, and clearly open eyes.
    chair=VGroup(Line([-3.85,-.2,0],[-3.85,-2.4,0],color=GREY,stroke_width=10),
                 Line([-3.85,-1.0,0],[-1.6,-1.0,0],color=GREY,stroke_width=10))
    torso=RoundedRectangle(width=1.05,height=1.85,corner_radius=.3,color=TEXT,fill_color=TEXT,fill_opacity=.80).move_to([-2.9,.15,0])
    head=Circle(radius=.48,color=TEXT,fill_color='#2A303D',fill_opacity=1).move_to([-2.9,1.60,0])
    eyes=VGroup(*[Ellipse(width=.18,height=.12,color=TEXT,fill_color=TEXT,fill_opacity=1).move_to([xx,1.68,0]) for xx in [-3.08,-2.75]])
    pupils=VGroup(*[Dot([xx,1.68,0],radius=.04,color=GREEN) for xx in [-3.08,-2.75]])
    def limb(a,b,width):
        a=np.array([*a,0]); b=np.array([*b,0]); d=b-a
        return RoundedRectangle(width=width,height=np.linalg.norm(d)+width,
                                corner_radius=width/2-.01,color=TEXT,
                                fill_color=TEXT,fill_opacity=.85,stroke_width=1).rotate(
                                    -np.arctan2(d[0],d[1])).move_to((a+b)/2)
    arms=VGroup(limb([-3.34,.75],[-3.55,-.6],.25),
                limb([-2.45,.75],[-1.95,-.55],.25))
    legs=VGroup(limb([-2.9,-.75],[-1.55,-.95],.38),
                limb([-1.55,-.95],[-1.35,-2.3],.32),
                limb([-2.6,-.8],[-2,-1.12],.32),
                limb([-2,-1.12],[-1.95,-2.38],.28),
                Ellipse(width=.62,height=.25,color=TEXT,fill_color=TEXT,fill_opacity=.85).move_to([-1.15,-2.4,0]),
                Ellipse(width=.58,height=.25,color=TEXT,fill_color=TEXT,fill_opacity=.85).move_to([-1.78,-2.47,0]))
    upper=VGroup(torso,head,eyes,pupils,arms)
    if slump: upper.rotate(-.35,about_point=[-2.9,-.75,0]).shift(DOWN*.25)
    return VGroup(chair,legs,upper)


class S13Orexin2(SpokenScene):
    def construct(self):
        g=wall_switch(); self.add(g)
        caption=T('human type 1 · narcolepsy',32).move_to([0,3.18,0]); self.add(caption)
        self.at('In narcolepsy')
        # Loss begins immediately and finishes before "severely reduced".
        self.play(g[6].animate.shift(RIGHT*1.3+UP*.5).set_opacity(0),run_time=1.1)
        self.remove(g[6])
        self.at('these neurons')
        reduced=T('human type 1 · narcolepsy\norexin neurons severely reduced',28,ORANGE).move_to([0,3.15,0])
        self.play(Transform(caption,reduced),run_time=.25)
        # Two full up/down flickers, then a final drop, before the wake bar.
        for up in [False,True,False,True,False]:
            self.play(Transform(g[4],wall_switch(up)[4]),run_time=.20)
            self.wait(.14)
        self.at('waking becomes')
        self.play(FadeOut(g),run_time=.12)
        bar=Rectangle(width=11.2,height=1.7,color=GREEN,fill_color=GREEN,fill_opacity=.55).move_to([0,0,0])
        axis=VGroup(Line([-5.6,-1.15,0],[5.6,-1.15,0],color=MUTED),
                    T('hours · schematic',28,MUTED).move_to([0,-2.28,0]),
                    T('wake bouts break up',36,GREEN).move_to([0,1.85,0]))
        for hour in range(5):
            xx=-5.6+2.8*hour
            axis.add(Line([xx,-1.15,0],[xx,-1.3,0],color=MUTED),
                     T(str(hour),28,MUTED).move_to([xx,-1.65,0]))
        self.play(FadeIn(bar),FadeIn(axis),run_time=.10)
        bouts=VGroup(*[Rectangle(width=b-a,height=1.7,color=GREEN,fill_color=GREEN,fill_opacity=.6).move_to([(a+b)/2,0,0])
                       for a,b in [(-5.6,-3.9),(-3.25,-2.5),(-1.9,.55),(1.15,1.7),(2.3,3.7),(4.3,5.6)]])
        self.play(ReplacementTransform(bar,bouts),run_time=.25)
        self.at('Muscle tone')
        self.play(FadeOut(bouts),FadeOut(axis),FadeOut(caption),run_time=.15)
        def framed_person(slump=False):
            return person(slump).scale(1.25).move_to([-1.4,-.15,0])
        p=framed_person()
        labels=VGroup(T('muscle tone lost',32,ORANGE).move_to([3.75,.55,0]),
                      T('consciousness\npreserved',32,GREEN).move_to([3.75,-.55,0]))
        self.add(p,heading('Cataplexy'),labels)
        self.at('can also fail'); self.play(Transform(p,framed_person(True)),run_time=.45)
        self.at('stays conscious'); self.play(Indicate(p[2][2],color=GREEN,scale_factor=1.12),run_time=.3)
        self.finish()


class S14Take(SpokenScene):
    def construct(self):
        self.add(heading('Reading a night · three ideas'))
        ys=[1.65,-.35,-2.35]
        for yy in [2.6,.65,-1.35,-3.35]: self.add(Line([-5.8,yy,0],[5.8,yy,0],color=GREY,stroke_width=1))
        # Thumbnail one: the same exponential as the full-size pressure plot.
        t=np.linspace(0,6.5,200)
        thumb1=VGroup(lp(-5.55+2.1*t/6.5,1.05+1.25*np.exp(-t/4),ORANGE,5),
                      Line([-5.55,1.05,0],[-3.45,1.05,0],color=MUTED))
        thumb2=VGroup(*[Rectangle(width=w,height=.25,color=PURPLE,fill_color=PURPLE,fill_opacity=.8).move_to([xx,-.65,0])
                        for xx,w in [(-5.4,.23),(-4.85,.40),(-4.16,.65)]],
                      Circle(radius=.32,color=PURPLE).move_to([-4.65,.05,0]),
                      Line([-4.65,.05,0],[-4.65,.28,0],color=PURPLE),
                      Line([-4.65,.05,0],[-4.45,-.05,0],color=PURPLE))
        thumb3=VGroup(Line([-5.55,-1.85,0],[-3.45,-1.85,0],color=PURPLE,stroke_width=4),
                      Line([-5.55,-2.85,0],[-3.45,-2.85,0],color=PURPLE,stroke_width=4),
                      DoubleArrow([-4.5,-2.85,0],[-4.5,-1.85,0],buff=.05,color=ORANGE))
        texts=[T('Deep sleep mainly follows the pressure',32,ORANGE).move_to([1.08,ys[0],0]),
               T('REM grows with clock and time asleep',32,PURPLE).move_to([1.08,ys[1],0]),
               T('A switch with a memory\nmay explain the gap',32).move_to([.8,ys[2],0])]
        # Neutral thumbnails establish a full card before each claim is highlighted.
        thumbs=[thumb1,thumb2,thumb3]
        self.add(*[th.copy().fade(.65) for th in thumbs])
        self.at('Keep this'); self.wait(.1)
        for cue,thumb,label in zip(['Deep sleep','Rem grows','A switch'],thumbs,texts):
            self.at(cue); self.play(FadeIn(thumb),FadeIn(label),run_time=.4)
        self.at('keeps sleep'); self.finish()


class S15End(EndCard):
    LINE='Deep sleep mainly follows the pressure.'
    def construct(self):
        self.add(T(self.LINE,42,font=TITLE_FONT),
                 T('biochemistrypedia.com',26,TEAL).move_to([0,-.9,0]))
        self.finish()
