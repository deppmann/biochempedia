"""Word-synchronised, equation-driven chapter.
COLOR MAP: ORANGE terminal; YELLOW serotonin; TEAL SERT; PURPLE paroxetine /
bicuculline; BLUE receptor/control; GREEN diazepam (exclusive); GOLD emphasis;
GREY structure / unblocked clearance. No molecular structures.
"""
import numpy as np
from bp_style import *
ORANGE='#F29E4C'
PURPLE='#B58CD9'
KD=.08


def label(s,x,y,size=26,color=TEXT):
    return T(s,size=size,color=color).move_to([x,y,0])


def heading(s,color=TEXT):
    return label(s,0,3.35,30,color)


def grid(n=0,center=(-4.05,.5),spacing=.46,receptor=False):
    return VGroup(*[Circle(radius=.145,stroke_width=2,
        stroke_color=PURPLE if i<n else (BLUE if receptor else TEAL),
        fill_color=PURPLE,fill_opacity=int(i<n)).move_to(
        [center[0]+(i%10-4.5)*spacing,center[1]+(4.5-i//10)*spacing,0]) for i in range(100)])


def plot_frame(x=-5.35,y=-2.3,w=8,h=5.2,xmin=0,xmax=12,
               xlabel='time (baseline decay times)',ylabel='serotonin remaining',ticks=None,ys=None):
    def p(a,b):return np.array([x+w*(a-xmin)/(xmax-xmin),y+h*b,0])
    lines=VGroup(Line(p(xmin,0),p(xmax,0),color=GREY),Line(p(xmin,0),p(xmin,1),color=GREY))
    texts=VGroup(label(xlabel,x+w/2,y-.8,26,GREY),label(ylabel,x+w/2,y+h+.43,26,GREY))
    for v,s in (ys or [(0,'0'),(.5,'50%'),(1,'100%')]):texts.add(label(s,x-.57,y+h*v,26,GREY))
    for a,s in (ticks or []):
        texts.add(label(s,p(a,0)[0],y-.35,26,GREY))
        lines.add(Line(p(a,0),p(a,0)+DOWN*.08,color=GREY))
    return VGroup(lines,texts),p


def curve(p,fn,lo,hi,color,width=4):
    return ParametricFunction(lambda z:p(z,fn(z)),t_range=[lo,hi,(hi-lo)/500],color=color,stroke_width=width)


def move_response(scene,mob,p,start,end,color,extra=(),run_time=1):
    # Evaluate the binding equation on every animation frame, including shifts.
    value=ValueTracker(start)
    mob.add_updater(lambda m:m.become(response_curve(p,value.get_value(),color)))
    scene.add(mob)
    scene.play(value.animate.set_value(end),*extra,run_time=run_time)
    mob.clear_updaters()


def slider(name,x,y,color=PURPLE,width=3):
    line=Line([x-width/2,y,0],[x+width/2,y,0],color=GREY,stroke_width=4)
    knob=Dot([x-width/2,y,0],radius=.13,color=color)
    return VGroup(label(name,x,y+.48,26,color),line,knob),knob


def occupancy(n=0):
    g=grid(n)
    a,p=plot_frame(-.5,-2.05,6.5,4.6,-3,2,'','share filled',
        [(i,s) for i,s in zip(range(-3,3),['0.001','0.01','0.1','1','10','100'])])
    a[1][0].become(label('free paroxetine (nM; log scale)',2.75,3.45,26,GREY))
    c=curve(p,lambda z:10**z/(KD+10**z),-3,2,PURPLE)
    s,k=slider('concentration',-3.8,-2.75,width=4.2)
    k.move_to([-5.9+4.2*(np.log10(KD*n/(100-n))+3)/5 if n else -5.9,-2.75,0])
    return g,a,c,p,s,k


def occ_marker(p,f):
    z=np.log10(KD*f/(1-f))
    return VGroup(DashedLine(p(z,0),p(z,f),color=GOLD,stroke_width=2),Dot(p(z,f),color=GOLD,radius=.085))


def ratio(p,f1,f2,text):
    z1,z2=[np.log10(KD*f/(1-f)) for f in [f1,f2]]
    l,r=p(z1,0)[0],p(z2,0)[0]
    return VGroup(Line([l,-2.85,0],[r,-2.85,0],color=GOLD),
        Line([l,-2.72,0],[l,-2.98,0],color=GOLD),Line([r,-2.72,0],[r,-2.98,0],color=GOLD),
        label(text,(l+r)/2,-3.35,26,GOLD))


def occ_add(scene,n,marks=()):
    g,a,c,p,s,k=occupancy(n);scene.add(g,a,c,s)
    for f in marks:scene.add(occ_marker(p,f))
    return g,p,k


ASSUMPTIONS=['Transporter is the only way out','Far below saturation','Occupancy held fixed',
             'One-site equilibrium binding','Block follows the binding KD']

def assumptions(small=False):
    body=VGroup(*[T(s,size=22 if small else 29) for s in ASSUMPTIONS]).arrange(DOWN,buff=.18 if small else .43,aligned_edge=LEFT)
    box=SurroundingRectangle(body,buff=.23,color=TEAL,corner_radius=.1)
    return VGroup(box,body).move_to([4.4,2,0] if small else [1.4,0,0])


COLS=[GREY,TEAL,PURPLE,GOLD]

def decay_base(count=1):
    a,p=plot_frame(x=-5.45,w=7.1,h=5.25,ticks=[(0,'0'),(4,'4'),(8,'8'),(12,'12')])
    cs=VGroup();ls=VGroup()
    for i,(tau,col) in enumerate(zip([1,2,10,100][:count],COLS)):
        group=VGroup(curve(p,lambda t:np.exp(-t/tau),0,12,col))
        if tau<=12:
            group.add(DashedLine(p(tau,0),p(tau,np.exp(-1)),color=col,stroke_width=2))
        cs.add(group)
        text=['control: 1×','50% blocked: 2×','90% blocked: 10×','99% blocked: 100×'][i]
        ls.add(label(text,4.35,.3-i*.57,26,col))
    # A logarithmic time ruler keeps even the off-frame 100× time measurable.
    ls.add(label('37% time (log scale)',4.35,-2.15,22,GREY))
    ls.add(Line([2.75,-2.7,0],[6.1,-2.7,0],color=GREY))
    for tau,col in zip([1,2,10,100][:count],COLS):
        xx=2.75+3.35*np.log10(tau)/2
        ls.add(Line([xx,-2.55,0],[xx,-2.85,0],color=col),Dot([xx,-2.7,0],color=col,radius=.05),
               label(str(tau),xx,-3.5 if tau==2 else -3.12,26,col))
    if count==4:
        cs[-1].add(Arrow(p(11,.88),p(12,.88),buff=0,color=GOLD))
    return a,cs,ls,p


def receptor_base():
    a,p=plot_frame(-5.3,-2.35,7.6,5.25,-3,5,'GABA concentration (each tick tenfold)',
        'current (% of maximum)',list(zip(range(-3,6),['10⁻³','10⁻²','10⁻¹','1','10','10²','10³','10⁴','10⁵'])))
    a.add(DashedLine(p(-3,1),p(5,1),color=GREY,stroke_opacity=.4,stroke_width=2))
    return a,response_curve(p,0,BLUE),p


def response_curve(p,shift,color=PURPLE):
    return curve(p,lambda z:10**z/(10**shift+10**z),-3,5,color)


def curve_name(p,name,shift,y,color):
    anchor=p(shift+.3,10**.3/(1+10**.3))
    return VGroup(Line([2.8,y,0],[3.25,y,0],color=color,stroke_width=3),label(name,4.6,y,26,color))


def receptor_names(p,b=None,d=None):
    v=VGroup(curve_name(p,'control',0,2.45,BLUE))
    if b is not None:v.add(curve_name(p,'bicuculline',b,1.75,PURPLE))
    if d is not None:v.add(curve_name(p,'diazepam',d,1.05,GREEN))
    return v


def question_frame():
    a,c,p=receptor_base()
    s1,_=slider('bicuculline',4.5,.3,width=2.8)
    s2,_=slider('diazepam',4.5,-1.1,GREEN,width=2.8)
    q=label('What happens\nto each curve?',4.5,-3.05,36,GOLD)
    ring=Circle(radius=.37,color=GOLD).move_to([4.5,-2.05,0])
    return VGroup(a,c,receptor_names(p),s1,s2,q,ring,label('5 s',4.5,-2.05,22,GOLD))


class S00Title(TitleCard):
    TITLE='How Much a Drug Changes a Step'
    LESSON='Transmitter Systems and Drugs'
    def construct(self):
        self.add(label('BIOCHEMISTRYPEDIA',0,2.1,22,TEAL),label(self.LESSON,0,1.35,26,GREY))
        self.play(FadeIn(label('How Much a Drug\nChanges a Step',0,-.2,48)),run_time=.7)
        self.finish()


class S01(SpokenScene):
    def construct(self):
        g=grid(0,(-2.15,.1),.69);self.add(g)
        self.at('fills nine in ten')
        self.play(Transform(g,grid(90,(-2.15,.1),.69)),run_time=.8)
        self.at('looks nearly done')
        self.play(FadeIn(label('90 of 100\ntargets',4.05,1,42,PURPLE)),run_time=.4)
        self.at('Is it')
        self.play(FadeIn(label('Nearly done?',4.05,-.85,42,GOLD)),run_time=.4)
        self.finish()


class S02(SpokenScene):
    def construct(self):
        # A large terminal shares its lower membrane with the transporter.
        terminal=RoundedRectangle(width=11.8,height=4.5,corner_radius=.25,color=ORANGE,fill_color=ORANGE,fill_opacity=.08).move_to([0,1.2,0])
        tr=RoundedRectangle(width=1.7,height=2.1,corner_radius=.2,color=TEAL,fill_color=TEAL,fill_opacity=.3).move_to([-.6,-1.05,0])
        dot=Dot([-.6,-2.85,0],radius=.22,color=YELLOW)
        nextdot=Dot([-3.2,-2.85,0],radius=.22,color=YELLOW)
        serotonin=label('serotonin',1.15,-2.85,30,YELLOW)
        self.add(terminal,tr,dot,nextdot,serotonin,label('terminal',-3.6,2.6,34,ORANGE),label('SERT (the transporter)',-.6,.5,30,TEAL))
        self.at('Take paroxetine')
        self.play(dot.animate.move_to([-.6,1.7,0]),serotonin.animate.move_to([1.15,1.7,0]),run_time=.85)
        drug=Dot([4,-1.05,0],radius=.32,color=PURPLE)
        self.play(FadeIn(drug),FadeIn(label('paroxetine',4,.15,32,PURPLE)),run_time=.3)
        self.at('It blocks the transporter')
        self.play(drug.animate.move_to([-.6,-1.05,0]),run_time=.6)
        self.play(nextdot.animate.move_to([-.6,-2.5,0]),run_time=.4)
        self.at('clears serotonin')
        self.play(FadeIn(label('reuptake\nblocker',4,-1.65,32,PURPLE)),Create(Line([-1.1,-2.18,0],[-.1,-2.18,0],color=PURPLE,stroke_width=6)),run_time=.4)
        self.finish()


class S03(SpokenScene):
    def construct(self):
        g,a,c,p,s,k=occupancy(0);self.add(g,a,s)
        self.at("As the drug's concentration rises")
        tracker=ValueTracker(-3)
        moving=always_redraw(lambda:Dot(p(tracker.get_value(),10**tracker.get_value()/(KD+10**tracker.get_value())),color=GOLD,radius=.09))
        fill=always_redraw(lambda:grid(round(100*10**tracker.get_value()/(KD+10**tracker.get_value()))))
        trace=always_redraw(lambda:curve(p,lambda z:10**z/(KD+10**z),-3,max(-2.999,tracker.get_value()),PURPLE))
        self.remove(g);self.add(fill,moving,trace)
        self.at('the dots fill')
        self.play(tracker.animate.set_value(2),k.animate.move_to([-1.7,-2.75,0]),run_time=1.6,rate_func=linear)
        self.finish()


class S04(SpokenScene):
    def construct(self):
        g,a,c,p,s,k=occupancy(99)
        a[1].remove(a[1][7])  # Replace the nearby 0.1 tick with the measured KD tick.
        self.add(g,a,c,s)
        self.at('Half fill')
        self.play(Transform(g,grid(50)),Create(occ_marker(p,.5)),k.animate.set_x(-5.9+4.2*(np.log10(KD)+3)/5),run_time=.6)
        z=np.log10(KD)
        self.add(label('0.08',p(z,0)[0],-2.43,26,GOLD))
        self.at('That concentration')
        self.play(FadeIn(VGroup(label('KD = 0.08 nM',3.9,-.55,29,GOLD),Line(p(np.log10(KD),.5),[2.65,-.55,0],color=GOLD,stroke_width=1.5))),run_time=.35)
        self.at('dissociation constant')
        self.play(FadeIn(label('Free paroxetine • wild-type human SERT • HEK293 cell membranes',0,-3.5,22,GREY)),run_time=.35)
        self.finish()


class S05(SpokenScene):
    def construct(self):
        g,p,k=occ_add(self,50,[.5])
        self.at('nine in ten')
        self.play(Transform(g,grid(90)),Create(occ_marker(p,.9)),k.animate.set_x(-5.9+4.2*(np.log10(.72)+3)/5),run_time=.6)
        self.add(label('90%: 0.72 nM',1.1,1.6,28,GOLD))
        self.at('takes nine times')
        self.play(Create(ratio(p,.5,.9,'9× KD')),run_time=.4)
        self.finish()


class S06(SpokenScene):
    def construct(self):
        g,p,k=occ_add(self,90,[.5,.9])
        self.at('99 in 100')
        self.play(Transform(g,grid(99)),Create(occ_marker(p,.99)),k.animate.set_x(-5.9+4.2*(np.log10(7.92)+3)/5),run_time=.7)
        self.add(label('99%: 7.92 nM',1.1,1.6,28,GOLD))
        self.at('takes eleven times')
        self.play(Create(ratio(p,.9,.99,'11× 0.72 nM')),run_time=.4)
        self.finish()


class S07(SpokenScene):
    def construct(self):
        g,p,k=occ_add(self,99,[.5,.9,.99])
        self.at('The curve flattens')
        self.play(Create(curve(p,lambda z:10**z/(KD+10**z),np.log10(.72),2,GOLD,7)),run_time=.7)
        self.at('the last few sites')
        self.play(FadeIn(label('The last few percent cost the most.',0,-3.5,30,GOLD)),run_time=.4)
        self.finish()


class S08(SpokenScene):
    def construct(self):
        g=grid(90,(-4.8,0),.3);self.add(g,assumptions())
        self.at('Do those last few sites matter')
        self.play(Indicate(VGroup(*g[90:]),color=GOLD),run_time=.7)
        self.at('Build a simple model')
        self.play(Indicate(assumptions()[0],color=TEAL),run_time=.6)
        self.finish()


class S09(SpokenScene):
    def construct(self):
        a,c,l,p=decay_base(1);card=assumptions(True);self.add(a,c,l,card)
        self.at('far from busy')
        self.play(card[1][1].animate.set_color(TEAL),run_time=.5)
        self.at('Block half')
        _,cs,ls,_=decay_base(2)
        self.remove(l);self.add(ls)
        self.play(Create(cs[-1]),run_time=1)
        self.finish()


class S10(SpokenScene):
    def construct(self):
        a,c,l,p=decay_base(2);self.add(a,c,l,assumptions(True))
        self.at('Block')
        _,cs,ls,_=decay_base(3)
        self.remove(l);self.add(ls)
        self.play(Create(cs[-1]),run_time=1)
        self.finish()


class S11(SpokenScene):
    def construct(self):
        a,c,l,p=decay_base(3);self.add(a,c,l,assumptions(True))
        self.at('Block')
        _,cs,ls,_=decay_base(4)
        self.remove(l);self.add(ls)
        self.play(Create(cs[-1]),run_time=1)
        self.finish()


class S12(SpokenScene):
    def construct(self):
        # Substitute the free share into the reciprocal; labels share a baseline.
        filled=label('f = L / (K + L)',-3.15,1.2,42,PURPLE)
        free=label('1 − f = K / (K + L)',0,2.75,38,TEAL)
        stretch=VGroup(label('stretch =',1.35,1.2,42),
                       label('1',4.25,1.65,42),
                       Line([3.25,1.2,0],[5.25,1.2,0],color=TEXT),
                       label('1 − f',4.25,.75,42,TEAL))
        self.add(filled,free,label('f: share filled',-3.15,-.05,30,PURPLE))
        self.at('That stretch')
        self.play(FadeIn(stretch),FadeIn(label('1 − f: share still free',3.55,-.05,30,TEAL)),run_time=.4)
        self.at('the factor')
        bridge=VGroup(T('= (K + L) / K',size=42),T('= 1 + L/K',size=48,color=GOLD)).arrange(RIGHT,buff=.35).move_to([0,-1.25,0])
        self.play(FadeIn(bridge),run_time=.4)
        self.at('L is the free')
        self.play(FadeIn(label('L: free drug concentration',0,-2.35,32,PURPLE)),run_time=.4)
        self.at("K is the drug's")
        self.play(FadeIn(label('K: half-fill concentration',0,-3.2,32,TEAL)),run_time=.4)
        self.finish()


class S13(SpokenScene):
    def construct(self):
        left,p=plot_frame(-5.45,-2.3,4.8,4.85,0,12,'time (baseline decay times)','serotonin remaining',[(0,'0'),(4,'4'),(8,'8'),(12,'12')])
        right,q=plot_frame(1,-2.3,4.75,4.85,0,1,'share blocked','decay-time stretch',[(0,'0'),(.5,'50%'),(1,'100%')],[(0,'0'),(.5,'11×'),(1,'22×')])
        left[1][0].set_font_size(22)
        self.add(left,right,label('Illustrative: other routes = 5% of baseline; fixed, first-order',0,3.55,26))
        faint=VGroup();solid=VGroup()
        for f,col in zip([0,.5,.9,.99],COLS):
            tau=1/(1-f)
            faint.add(DashedVMobject(curve(p,lambda t:np.exp(-t/tau),0,12,'#C6CDD5',5),num_dashes=20,dashed_ratio=.55))
            solid.add(curve(p,lambda t:np.exp(-(.05+.95*(1-f))*t),0,12,col,3))
        self.add(faint)
        self.at('Real tissue')
        self.play(Create(solid),run_time=.65)
        fixed=curve(q,lambda f:1/(.05+.95*(1-f))/22,0,1,TEXT)
        only=curve(q,lambda f:1/(1-f)/22,0,1-1/22,GREY)
        asym=DashedLine(q(0,20/22),q(1,20/22),color=TEXT,stroke_width=2)
        self.play(Create(fixed),Create(only),Create(asym),run_time=.65)
        self.add(Arrow(q(1-1/21,21/22),q(1-1/22,1),buff=0,color=GREY),label('no limit',4.2,1.65,26,GREY),label('20× limit',2.35,1.65,26,TEXT))
        blocked=VGroup(T('share blocked:',size=22,color=GREY),*[T(t,size=22,color=col) for t,col in zip(['0% /','50% /','90% /','99%'],COLS)]).arrange(RIGHT,buff=.12).move_to([-3.05,-3.65,0])
        self.add(label('dashed: SERT only; solid: + routes',3.35,-3.65,22,GREY),blocked)
        self.at('They make all three numbers smaller')
        results=VGroup(*[label(t,3.15,.15-i*.6,26,col) for i,(t,col) in enumerate(zip(['50%: 2 → 1.9×','90%: 10 → 6.9×','99%: 100 → 16.8×'],COLS[1:]))])
        self.play(FadeIn(results),run_time=.4)
        self.at('limit the stretch most')
        self.play(Indicate(asym,color=TEXT),run_time=.5)
        self.finish()


class S14(SpokenScene):
    def construct(self):
        a,c,p=receptor_base();self.add(a)
        self.at('The same factor')
        self.play(Create(c),FadeIn(receptor_names(p)),run_time=.8)
        self.finish()


class S15(SpokenScene):
    def construct(self):
        a,c,p=receptor_base();self.add(a,c,receptor_names(p))
        b=c.copy()
        self.at('slides the curve right')
        move_response(self,b,p,0,1,PURPLE,[FadeIn(curve_name(p,'bicuculline',1,1.75,PURPLE))],.8)
        self.at('by that same factor')
        self.play(GrowArrow(Arrow(p(0,.5),p(1,.5),buff=0,color=GOLD)),FadeIn(label('1 + [B]/KB',.45,1.35,28,GOLD)),run_time=.4)
        self.at('still reach the top')
        self.play(FadeIn(label('same maximum',4.5,3.25,26,GOLD)),Indicate(a[2],color=GOLD),run_time=.5)
        self.finish()


class S16(SpokenScene):
    def construct(self):
        a,c,p=receptor_base();b=response_curve(p,1);names=receptor_names(p,b=1)
        self.add(a,c,b,names)
        self.at('Diazepam')
        self.play(FadeOut(b),FadeOut(names[1]),run_time=.4)
        d=c.copy();self.add(d)
        self.at('slides the curve to the left')
        move_response(self,d,p,0,-.8,GREEN,[FadeIn(curve_name(p,'diazepam',-.8,1.05,GREEN))],.9)
        self.finish()


class S17(SpokenScene):
    def construct(self):
        q=question_frame();self.add(*q[:3])
        self.at('Keep adding')
        self.play(FadeIn(q[3]),run_time=.4)
        self.at('then separately')
        self.play(FadeIn(q[4]),run_time=.4)
        self.at('What happens')
        self.play(FadeIn(q[5:]),run_time=.4)
        self.finish()


class S18Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        q=question_frame();self.add(q)
        self.play(Uncreate(q[6]),run_time=5,rate_func=linear)


class S19(SpokenScene):
    def construct(self):
        a,c,p=receptor_base();s,k=slider('bicuculline',4.5,-.7,width=2.8)
        b=response_curve(p,0);names=receptor_names(p,b=0)
        self.add(a,c,b,s,names,label('more drug →',4.5,-1.45,26,PURPLE))
        self.at('The antagonist keeps pushing')
        move_response(self,b,p,0,1,PURPLE,[k.animate.shift(RIGHT*1.3)],.9)
        self.at('for as long')
        move_response(self,b,p,1,2,PURPLE,[k.animate.shift(RIGHT*1.3)],.9)
        self.finish()


class S20(SpokenScene):
    def construct(self):
        a,c,p=receptor_base();s,k=slider('diazepam',4.5,-.7,GREEN,width=2.8)
        d=response_curve(p,0,GREEN);names=receptor_names(p,d=0)
        self.add(a,c,d,s,names,label('more drug →',4.5,-1.45,26,GREEN))
        self.at('The modulator stops')
        shift=-np.log10(1+9*9/10)
        move_response(self,d,p,0,shift,GREEN,[k.animate.shift(RIGHT*1.5)],.75)
        self.at('Once its own sites are full')
        old=shift;shift=-np.log10(1+9*999/1000)
        move_response(self,d,p,old,shift,GREEN,[k.animate.shift(RIGHT*.6)],.65)
        self.at('it can do no more')
        self.play(k.animate.shift(RIGHT*.6),run_time=.5)
        self.at('That is its ceiling')
        point=p(shift,.5)
        self.play(FadeIn(label('ceiling',point[0]-1.2,point[1]-.85,28,GREEN)),Create(Line(point,point+[-.4,-.55,0],color=GREEN)),run_time=.4)
        self.finish()


class S21(SpokenScene):
    def construct(self):
        self.add(label('1 + L/K',0,2.45,90,GOLD))
        self.at('This rule is for blockers')
        self.play(FadeIn(chip('competitive blockers',PURPLE,size=50,pad=.6).move_to([0,.25,0])),run_time=.5)
        self.at('not for agonists')
        tag=chip('agonist response',BLUE,size=46,pad=.55).move_to([.55,-2.35,0])
        no=Square(side_length=.65,color=RED).next_to(tag,LEFT,buff=.45)
        self.play(FadeIn(tag),Create(no),run_time=.25)
        self.play(Create(Cross(no,stroke_color=RED,stroke_width=5)),run_time=.35)
        self.finish()


class S22(SpokenScene):
    def construct(self):
        g=grid(1,(-2.8,.1),.53,receptor=True)
        outline=Rectangle(width=1.4,height=5,color=BLUE).move_to([3.3,.1,0])
        # Illustrative operational model, tau=10: E/Emax=10 f/(1+10 f).
        f=.01;value=10*f/(1+10*f)
        fill=Rectangle(width=1.35,height=5*value,stroke_width=0,fill_color=BLUE,fill_opacity=.7).align_to(outline,DOWN).set_x(3.3)
        title=heading('Agonist')
        self.add(g,outline,fill,title,label('illustrative; depends on the cell',0,-3.5,26,GREY))
        self.at('With spare receptors')
        self.play(Transform(title,heading('spare receptors',BLUE)),run_time=.3)
        self.at('filling a tenth of them')
        self.play(Transform(g,grid(10,(-2.8,.1),.53,receptor=True)),FadeIn(label('10% filled',-2.8,-2.9,28,PURPLE)),run_time=.5)
        self.at('can give about half')
        new=Rectangle(width=1.35,height=2.5,stroke_width=0,fill_color=BLUE,fill_opacity=.7).align_to(outline,DOWN).set_x(3.3)
        self.play(Transform(fill,new),FadeIn(label('~50%',5,0,30,BLUE)),FadeIn(label('response',3.3,-2.9,28,BLUE)),run_time=.6)
        self.finish()


class S23(SpokenScene):
    def construct(self):
        self.add(heading('The takeaway',GOLD))
        self.at('if the transporter is the only way out')
        self.play(FadeIn(label('If the transporter is\nthe only way out,',0,1.25,36,TEAL)),run_time=.5)
        self.at('the last few percent blocked')
        self.play(FadeIn(label('the last few percent blocked\nstretch the signal most.',0,-.7,38,GOLD)),run_time=.5)
        self.play(FadeIn(label('Next: a mechanism is not a cause.',0,-2.7,26,GREY)),run_time=.4)
        self.finish()


class S24End(EndCard):
    LINE='In this model, the last few percent blocked stretch the signal most.'
    def construct(self):
        self.add(label('If the transporter is the only way out,',0,1.5,30,TEAL),
                 label('the last few percent blocked\nstretch the signal most.',0,-.1,40,GOLD),
                 label('in this model',0,-1.65,28,GREY),label('biochemistrypedia.com',0,-2.65,22,TEAL))
        self.finish()
