"""One Current, Three Factors — reviewed redraw.
COLOR MAP: BLUE candidate protein; GOLD mechanical channel highlight (s04 only);
TEAL partners (overridden to a distinct green-teal); PURPLE required factors;
YELLOW ions/current; PINK reachable residue; GREEN evidence; RED uncertainty;
GREY membrane/stereocilia; TEXT labels and force.
All plotted currents are calculated from I = N*i*P or binary/binomial open counts.
Logistic activation and latency are illustrative models, not measured kinetics.
"""
import numpy as np
from bp_style import *
TEAL = '#29C790'
PURPLE = '#B58CD9'
PINK = '#F2789F'
I_UNIT = -15.0


class Timed(SpokenScene):
    # Same word alignment as SpokenScene, without modifying the existing sync.log.
    def at(self, phrase, lead=.2, nth=0):
        rest = self.t_of(phrase, nth) - lead - self.elapsed()
        if rest > .02:
            self.wait(rest)


def txt(s, x=0, y=0, size=32, color=TEXT):
    return T(s, size, color).move_to([x, y, 0])


def equation(y=2.95, active=None):
    parts = [('N', -4.4), ('×', -2.85), ('i', -1.5), ('×', -.1),
             ('P_open', 1.8), ('→', 4.2), ('I', 5.5)]
    return VGroup(*[(M(s,44,YELLOW if active is None or s == active else TEXT).move_to([x,y,0])
                    if s == 'I' else txt(s,x,y,42,YELLOW if active is None or s == active else TEXT)) for s,x in parts])


def bundle(links=False, pushed=False):
    rods = VGroup(); tips = []
    for x, h in zip((-3, 0, 3), (2.6, 3.8, 5.0)):
        r = RoundedRectangle(width=.6, height=h, corner_radius=.18,
             color=GREY, fill_color=GREY, fill_opacity=.24, stroke_width=4)
        r.move_to([x, -2.7+h/2, 0])
        if pushed:
            r.rotate(-.18, about_point=np.array([x, -2.7, 0]))
        rods.add(r); tips.append(r.get_top())
    base = Rectangle(width=10.5, height=.4, color=GREY, fill_opacity=.22).move_to([0,-2.95,0])
    ls = VGroup(*[Line(tips[j], tips[j+1]+DOWN*(.35 if pushed else .9), color=TEXT, stroke_width=5)
                  for j in (0,1)]) if links else VGroup()
    return VGroup(rods, base, ls)


def gate(opened=True, color=BLUE):
    d = .64 if opened else .32
    return VGroup(*[RoundedRectangle(width=.48, height=1.65, corner_radius=.12,
       color=color, fill_color=color, fill_opacity=.55, stroke_width=4)
       .move_to([s*d,0,0]) for s in (-1,1)])


def linked_gate(opened=True):
    g = gate(opened)
    mem = VGroup(*[Line([s*1.0,0,0],[s*2.0,0,0],color=GREY,stroke_width=14) for s in (-1,1)])
    link = Line([-.64,.83,0],[.5,2.05,0], color=TEXT, stroke_width=5)
    return VGroup(mem,g,link)


def ion(x,y,blocked=False):
    shape = Square(side_length=.43,color=TEXT,fill_color=BG,fill_opacity=1) if blocked else Circle(radius=.22,color=YELLOW,fill_color=BG,fill_opacity=1)
    return VGroup(shape, T('+',30,TEXT if blocked else YELLOW).move_to(shape)).move_to([x,y,0])


def icon_row(n=10, open_indices=(), inactive=()):
    icons = VGroup()
    for j in range(n):
        g=linked_gate(j in open_indices).scale(.35)
        if j in inactive: g.set_opacity(.25)
        g.move_to([(j-(n-1)/2)*1.16,0,0]); icons.add(g)
    return icons


def trace(n=100,i=-15,p=.2,w=10,h=3.7,center=(0,0,0),seed=8,max_current=450,mean_label=True):
    rng=np.random.default_rng(seed)
    vals=rng.binomial(n,p,161)*i
    top=h/2
    pts=[[-w/2+w*k/160,top+np.clip(v,-max_current,0)/max_current*h,0] for k,v in enumerate(vals)]
    line=VMobject(color=YELLOW,stroke_width=2.5).set_points_as_corners(pts)
    zero=Line([-w/2,top,0],[w/2,top,0],color=GREY,stroke_width=2)
    axis=Line([-w/2,top,0],[-w/2,-h/2,0],color=GREY)
    mean_y=top+n*i*p/max_current*h
    mean=DashedLine([-w/2,mean_y,0],[w/2,mean_y,0],color=GREEN,stroke_width=7,dash_length=.18,dashed_ratio=.75).set_z_index(2)
    labels=VGroup(txt('0 pA',-w/2+.55,top+.3,30))
    if mean_label: labels.add(txt(f'mean −{abs(n*i*p):.0f} pA',w/2-1.6,mean_y+.36,28,GREEN))
    return VGroup(zero,axis,mean,line,labels).shift(np.array(center))


def single_event(x=0,y=0,w=5,h=2.6):
    # One binary opening, multiplied by unitary current. Downward is inward.
    ts=np.array([0,.3,.3,.7,.7,1.0])
    opened=np.array([0,0,1,1,0,0])
    vals=I_UNIT*opened
    path=VMobject(color=YELLOW,stroke_width=5).set_points_as_corners(
        [[x-w/2+t*w,y+v/15*h,0] for t,v in zip(ts,vals)])
    base=Line([x-w/2,y,0],[x+w/2,y,0],color=GREY)
    arrow=DoubleArrow([x+w*.34,y,0],[x+w*.34,y-h,0],buff=0,color=YELLOW)
    return VGroup(base,path,arrow,txt('i',x+w*.34+.4,y-h/2,42,YELLOW),
        txt('closed · 0 pA',x-w*.2,y+.4,30),txt('open',x,y-h-.4,30,YELLOW))


def prediction():
    title=txt('Which factor changed?',0,3.05,44)
    zero=Line([-5.7,1.6,0],[5.7,1.6,0],color=GREY)
    bars=VGroup()
    for x,n,cap in [(-3,-300,'average current now'),(3,-150,'after mutation')]:
        height=abs(n)/300*3.5
        bars.add(Rectangle(width=2.1,height=height,color=YELLOW,fill_color=YELLOW,fill_opacity=.4)
                 .move_to([x,1.6-height/2,0]))
        bars.add(txt(cap,x,2.15,30),txt(f'−{abs(n)} pA',x,1.6-height-.4,32,YELLOW))
    factors=VGroup(*[chip(s,YELLOW,32).move_to([x,-3.05,0]) for s,x in [('N ?',-3.6),('i ?',0),('P_open ?',3.6)]])
    return VGroup(title,zero,bars,factors,txt('0',-6.05,1.6,30),txt('inward ↓',0,-1.15,30,YELLOW))


def rule():
    return txt('A lost current cannot say\nwhich factor you removed.',0,1.2,50)


def factor_paths():
    factors=VGroup(*[txt(label,x,-.75,42,YELLOW) for label,x in [('N ↓',-4),('i ↓',0),('P_open ↓',4)]])
    result=txt('I lower',0,-2.9,44,YELLOW)
    arrows=VGroup(*[Arrow(f.get_bottom()+DOWN*.15,result.get_top()+np.array([dx,.12,0]),buff=0,color=YELLOW)
        for f,dx in zip(factors,(-.7,0,.7))])
    return VGroup(factors,arrows,result)


class S00Title(TitleCard):
    LESSON="The Hair Cell's Transduction Channel"
    TITLE='One Current, Three Factors'


class S01Q(Timed):
    def construct(self):
        b=bundle().scale(.88).move_to([.3,-.45,0]); self.add(b)
        # A generic gene badge, not a molecular structure.
        dna=VGroup(RoundedRectangle(width=2.15,height=1.15,corner_radius=.15,color=TEXT),
            Line([-.8,.2,0],[.8,.2,0],color=GREY,stroke_width=5),
            Rectangle(width=.55,height=.3,color=TEXT,fill_color=TEXT,fill_opacity=.6).move_to([0,.2,0]),
            txt('GENE',0,-.27,30))
        dna.move_to([-4.6,1.7,0])
        self.at('A gene'); self.play(FadeIn(dna),run_time=.35)
        pt=b[0][0].get_top()
        protein=RoundedRectangle(width=.75,height=.55,corner_radius=.2,color=BLUE,fill_color=BLUE,fill_opacity=.65).move_to(pt)
        name=txt('protein',-4.65,.25,34,BLUE)
        leader=Line(name.get_right()+RIGHT*.15,pt+LEFT*.5,color=BLUE)
        arrow=Arrow(dna.get_bottom(),name.get_top(),buff=.12,color=BLUE)
        self.at('its protein'); self.play(FadeIn(protein),FadeIn(name),Create(leader),GrowArrow(arrow),run_time=.4)
        self.at('Is that enough'); self.play(FadeIn(txt('Enough to call it the channel?',0,3.05,40)),run_time=.3)
        self.at('Start with'); self.play(Indicate(protein,color=YELLOW),run_time=.4); self.finish()


class S02Bundle(Timed):
    def construct(self):
        b=bundle(); self.add(b)
        self.at('A hair bundle'); self.play(Indicate(b[0],color=TEXT),run_time=.65)
        name=txt('stereocilia',-3.6,2.6,36)
        lead=Line(name.get_bottom()+DOWN*.15,b[0][1].get_top()+LEFT*.3,color=TEXT)
        self.at('stereocilia'); self.play(FadeIn(name),Create(lead),run_time=.4); self.finish()


class S03Links(Timed):
    def construct(self):
        b=bundle(); full=bundle(True); self.add(b)
        self.at('Tip links connect'); self.play(Create(full[2][0]),Create(full[2][1]),run_time=.7)
        name=txt('tip link',-3.7,2.55,36)
        target=full[2][0].get_center()
        self.at('each shorter'); self.play(FadeIn(name),Create(Line(name.get_bottom()+DOWN*.15,target,color=TEXT)),run_time=.4)
        self.at('to the side'); self.play(Indicate(full[2],color=YELLOW),run_time=.4); self.finish()


class S04Push(Timed):
    def construct(self):
        b=bundle(True); self.add(b)
        pos=b[0][0].get_top()
        ch=gate(False,GOLD).scale(1.05).move_to(pos+RIGHT*.67+DOWN*.86)
        self.add(ch)
        ar=Arrow([-1.2,-1.5,0],[1.2,-1.5,0],buff=0,color=TEXT)
        pushed=bundle(True,True)
        newpos=pushed[0][0].get_top()
        closed=gate(False,GOLD).scale(1.05).move_to(newpos+RIGHT*.67+DOWN*.86)
        pushed[2][0].put_start_and_end_on(closed[0].get_top(),pushed[2][0].get_end())
        self.at('Deflect the bundle'); self.play(GrowArrow(ar),Transform(b,pushed),Transform(ch,closed),run_time=.9)
        note=txt('thought to\nsit here',-4.8,.85,32,GOLD)
        leader=Line(note.get_bottom()+DOWN*.15,ch[0].get_left()+LEFT*.15,color=GOLD)
        self.at('The tip links'); self.play(FadeIn(note),Create(leader),Indicate(b[2],color=GOLD),run_time=.5)
        opened=gate(True,GOLD).scale(1.05).move_to(newpos+RIGHT*.67+DOWN*.86)
        link=Line(opened[0].get_top(),b[2][0].get_end(),color=TEXT,stroke_width=5)
        self.at('pull channels open'); self.play(Transform(ch,opened),Transform(b[2][0],link),run_time=.5)
        self.finish()

class S05In(Timed):
    def construct(self):
        stage=linked_gate().scale(1.15).move_to([-3.5,.05,0]); self.add(stage)
        self.add(txt('outside',-5.5,1.35,30),txt('inside',-5.5,-1.7,30))
        self.add(txt('Holding voltage negative · below reversal potential',0,3.12,32))
        self.add(txt('channel: thought at the lower end of a tip link',0,-3.35,30,BLUE))
        event=single_event(x=2.75,y=.9,w=5.1,h=2.05)
        # The trace is present from the outset; i is introduced only in s10.
        event.remove(event[2],event[3]); self.add(event)
        self.add(txt('tip link',-2,2.15,30),Line([-2.55,1.9,0],stage[2].get_center(),color=TEXT))
        cx=stage[1].get_x()
        ions=VGroup(*[ion(cx,y) for y in (-1.9,-.95,0,.95,1.9)])
        clock=ValueTracker(0)
        def flow(m):
            for j,c in enumerate(m): c.move_to([cx,2.0-((j*.85+clock.get_value()*1.7)%4.1),0])
        ions.add_updater(flow)
        self.at('With the cell'); self.play(Indicate(stage[0],color=TEXT),run_time=.3)
        self.at('cations flow in'); self.add(ions); clock.add_updater(lambda m,dt:m.increment_value(dt)); self.add(clock)
        self.at('current is inward'); self.play(Indicate(event[1]),FadeIn(txt('inward current',2.8,-2.1,34,YELLOW)),run_time=.5)
        self.at('This is the'); self.play(FadeIn(txt('Opened toward the tallest row',2.65,-2.7,30)),run_time=.3)
        self.finish()

class S06Fast(Timed):
    def construct(self):
        ax=Axes(x_range=[0,.5,.1],y_range=[0,1,.5],x_length=5.4,y_length=2.6,tips=False).move_to([-2.75,1.3,0])
        curve=ax.plot(lambda t:1/(1+np.exp(-(t-.17)/.03)),x_range=[0,.5,.002],color=YELLOW)
        ylabel=txt('Current magnitude',-6.05,1.35,27,YELLOW).rotate(PI/2)
        self.add(ax,ylabel,txt('Magnified rise · fraction of 1 ms',-2.65,3.2,32,YELLOW),
            txt('0',-5.45,-.3,26),txt('0.5 ms',-.05,-.3,26))
        self.at('The current rises'); self.play(Create(curve),run_time=.65)
        # Both latency bars use this one linear millisecond scale.
        x0=-5.5; unit=3.65
        axis=Line([x0,-3,0],[5.65,-3,0],color=GREY)
        ticks=VGroup(*[VGroup(Line([x0+k*unit,-2.9,0],[x0+k*unit,-3.1,0],color=TEXT),
            txt(f'{k} ms',x0+k*unit,-3.4,26)) for k in range(4)])
        rise=Line([x0,-1.1,0],[x0+.13*unit,-1.1,0],color=YELLOW,stroke_width=16)
        self.at('within a fraction'); self.play(Create(axis),FadeIn(ticks),Create(rise),
            FadeIn(txt('current rise',-3.5,-1.1,30,YELLOW)),run_time=.4)
        cascade=VGroup(Line([x0,-2.25,0],[x0+2.7*unit,-2.25,0],color=RED,stroke_width=16),
            txt('enzyme → messenger → channel',0,-1.75,30),txt('too slow',5.45,-2.25,28,RED))
        self.at('too fast for'); self.play(FadeIn(cascade),run_time=.4)
        comparison=txt('Illustrative latency comparison',3,2.7,28)
        self.at('second messengers'); self.add(comparison)
        mech=linked_gate().scale(.9).move_to([3.6,1.25,0])
        force=Arrow(mech[2].get_end()+UP*.65+RIGHT*.5,mech[2].get_end(),color=TEXT,buff=0)
        self.at('So force'); self.play(FadeOut(comparison),FadeIn(mech),GrowArrow(force),run_time=.4)
        self.at('open the channel directly'); self.play(FadeIn(txt('Direct gating (thought)',3.6,-.25,30,GREEN)),run_time=.35)
        self.finish()

class S07Curve(Timed):
    def construct(self):
        ax=Axes(x_range=[-3,3,1],y_range=[0,1,.5],x_length=10.2,y_length=4.5,tips=False,
                axis_config={'include_ticks':False}).move_to([.1,-.05,0])
        # Keep coordinate geometry intact; display a separate left-boundary y axis.
        display=VGroup(ax.x_axis,Line(ax.c2p(-3,0),ax.c2p(-3,1),color=GREY),
                       Line(ax.c2p(0,0),ax.c2p(0,0)+DOWN*.15,color=TEXT))
        curve=ax.plot(lambda x:1/(1+np.exp(-2*x)),x_range=[-3,3,.02],color=YELLOW)
        self.add(display,txt('Size of peak inward current',0,3.5,36,YELLOW),
                 txt('Bundle displacement → toward tallest row',0,-3.5,32),
                 txt('0 (no deflection)',.1,-2.9,30),
                 txt('0',-5.45,-2.3,30),txt('maximum',-5.4,2.25,30))
        self.at('Plot the size'); self.play(Indicate(display),run_time=.4)
        self.at('The S'); self.play(Create(curve),run_time=.65)
        cap=txt('Nearly all open: saturation',1.8,2.85,32,GREEN)
        self.at('saturates when'); self.play(FadeIn(cap),Create(Line(cap.get_bottom()+DOWN*.1,ax.c2p(2.2,.99)+UP*.1,color=GREEN)),run_time=.4); self.finish()


class S08Many(Timed):
    def construct(self):
        icons=icon_row(open_indices=(0,3,5,7)); icons.move_to([0,1.6,0])
        tr=trace(w=10,h=2.8,center=(0,-1.1,0),mean_label=False)
        self.add(icons,tr,txt('current from many channels',0,3.05,36,YELLOW))
        connector=Arrow([0,.9,0],[0,.45,0],buff=0,color=YELLOW)
        self.at('many channels'); self.play(GrowArrow(connector),Indicate(icons,color=YELLOW),run_time=.4)
        self.at('Three things'); self.play(FadeOut(Group(*self.mobjects)),FadeIn(equation()),run_time=.4)
        self.add(icon_row(open_indices=(0,3)).move_to([0,.7,0]),txt('Three factors set the ensemble current',0,-1.5,38)); self.finish()


class S09N(Timed):
    def construct(self):
        self.add(equation(active='N'))
        top=icon_row(5,open_indices=(0,2)).scale(1.3).move_to([-.7,1.1,0])
        bottom=icon_row(5,open_indices=(1,),inactive=(3,4)).scale(1.3).move_to([-.7,-1.2,0])
        self.add(top,bottom,txt('Before: all working',0,2.1,30),txt('After: 3 working',-1,-.2,30),
            txt('not working',4.7,-1.2,28),Line([3.65,-1.2,0],bottom[4].get_right()+RIGHT*.1,color=TEXT))
        cap=txt('N: number of working channels at tip links',0,-2.9,36,YELLOW)
        self.at('how many working'); self.play(Indicate(bottom[:3],color=YELLOW),FadeIn(cap),run_time=.45)
        self.at('Call that'); self.play(Indicate(cap),run_time=.35); self.finish()

class S10I(Timed):
    def construct(self):
        self.add(equation(active='i'),linked_gate().scale(1.2).move_to([-3.5,-.2,0]))
        event=single_event(2.55,.8,5.4,2.8); self.add(event)
        cap=txt('i: current through one open channel',0,-3.2,36,YELLOW)
        self.at('one open channel'); self.play(Indicate(self.mobjects[1],color=YELLOW),FadeIn(cap),run_time=.4)
        self.at('unitary current'); self.play(Indicate(event[1],color=YELLOW),run_time=.4)
        self.at('small i'); self.play(Indicate(cap),run_time=.35); self.finish()


class S11P(Timed):
    def construct(self):
        self.add(equation(active='P_open'))
        row=icon_row(5,open_indices=(2,)).scale(1.8).move_to([0,.2,0]); self.add(row)
        brace=Brace(row[2],DOWN,color=YELLOW)
        self.at('chance that each'); self.play(FadeIn(brace),FadeIn(txt('open',0,-1.55,34,YELLOW)),run_time=.4)
        self.at('open probability'); self.play(FadeIn(txt('P_open: chance a channel is open',0,-2.6,36,YELLOW)),run_time=.35)
        self.add(txt('Illustration: 1 in 5 open',0,-3.35,32)); self.finish()


class S12Eq(Timed):
    def construct(self):
        self.add(equation(),txt('Channels alike · fixed voltage and ions',0,3.6,30))
        nums=VGroup(*[txt(s,x,1.95,30) for s,x in [('N = 100',-4.3),('i = −15 pA',-.8),('P_open = 0.20',3.5)]])
        tr=trace(w=10.3,h=2.65,center=(0,-.35,0),max_current=600); self.add(nums,tr)
        self.at('For channels'); self.play(Indicate(nums),run_time=.4)
        self.at('multiply the three'); self.play(Indicate(self.mobjects[0],color=YELLOW),run_time=.4)
        self.at('That gives'); self.play(FadeIn(txt('100 × (−15 pA) × 0.20 = −300 pA',0,-2.55,34,YELLOW)),run_time=.35)
        self.at('whole bundle'); self.play(FadeIn(txt('Made-up ensemble: N and P_open are teaching assumptions',0,-3.35,30)),run_time=.35); self.finish()


class S13Predict(Timed):
    def construct(self):
        p=prediction(); self.add(p[0],p[1],p[2][0],p[2][1],p[2][2],p[4],p[5])
        self.at('Predict'); self.play(Indicate(p[0]),run_time=.35)
        self.at('A mutation'); self.play(FadeIn(VGroup(*list(p[2])[3:])),run_time=.4)
        self.at('Which of the'); self.play(FadeIn(p[3]),run_time=.35); self.finish()


class S14Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(prediction())
        cue=txt('Predict · 5',0,.4,32,GREEN); self.add(cue)
        for n in (5,4,3,2,1):
            cue.become(txt(f'Predict · {n}',0,.4,32,GREEN)); self.wait(1)


class S15Reveal(Timed):
    def construct(self):
        self.add(txt('The average alone cannot tell',0,3.2,40))
        cases=[(50,-15,.2,'N halved'),(100,-7.5,.2,'i halved'),(100,-15,.1,'P_open halved')]
        cards=[]
        for j,(n,i,p,name) in enumerate(cases):
            x=(j-1)*4.25
            # All panels share 0..−300 pA, and the same binomial model.
            panel=VGroup(RoundedRectangle(width=4.05,height=5.25,corner_radius=.15,color=GREY).move_to([x,0,0]),
                txt(name,x,2.12,32,YELLOW),trace(n,i,p,w=3.5,h=3.65,center=(x,-.3,0),seed=10+j,max_current=300,mean_label=False),
                txt('mean −150 pA',x,-2.32,30,GREEN))
            panel[2][4][0].shift(DOWN*.12)
            cards.append(panel)
        self.add(cards[0])
        self.at('From the average alone'); self.play(Indicate(cards[0][1]),run_time=.4)
        self.at('the channels'); self.play(Indicate(cards[0][2][3]),run_time=.35)
        self.at('the unitary current'); self.play(FadeIn(cards[1]),run_time=.35)
        self.at('the open probability'); self.play(FadeIn(cards[2]),run_time=.35)
        self.at('Each gives'); self.play(FadeIn(txt('Same mean −150 pA · the flicker can differ',0,-3.12,34,GREEN)),run_time=.35)
        self.add(txt('Shared scale: 0 to −300 pA · equal time windows',0,-3.65,30)); self.finish()


class S16Suspects(Timed):
    def construct(self):
        self.add(txt('Different required proteins',0,3.15,40,PURPLE))
        cards=VGroup()
        for name,x in [('trafficking\nfactor',-4.2),('anchor',0),('lipid-modifying\nenzyme',4.2)]:
            cards.add(chip(name,PURPLE,32).move_to([x,1.5,0]))
        self.at('trafficking factor'); self.play(FadeIn(cards[0]),run_time=.3)
        self.at('an anchor'); self.play(FadeIn(cards[1]),run_time=.3)
        self.at('enzyme'); self.play(FadeIn(cards[2]),run_time=.3)
        self.at('could all be needed',lead=.55); self.play(FadeIn(txt('Could all be needed',0,2.55,32,WHITE)),run_time=.2)
        self.at('Deleting'); self.play(*[c[0].animate.set_stroke(opacity=.4) for c in cards],run_time=.3)
        flats=VGroup(*[VGroup(Arrow([x,.7,0],[x,.15,0],color=GREY,buff=0),
            Line([x-1.65,-.25,0],[x+1.65,-.25,0],color=YELLOW,stroke_width=5),txt('0 pA',x,-.8,32,YELLOW)) for x in (-4.2,0,4.2)])
        self.at('silence the cell'); self.play(FadeIn(flats),FadeIn(txt('Each deletion would silence the cell',0,-1.45,30,RED)),run_time=.3)
        # Shared alternatives, not an assignment of suspects to factors.
        alternatives=VGroup()
        for j,parts in enumerate([['0','i','P_open'],['N','0','P_open'],['N','i','0']]):
            tokens=['I','=',parts[0],'×',parts[1],'×',parts[2]]
            row=VGroup(*[M(t,28,YELLOW) if t=='I' else T(t,28,RED if t=='0' else YELLOW) for t in tokens]).arrange(RIGHT,buff=.17)
            alternatives.add(row.move_to([0,-2.05-j*.55,0]))
        self.add(alternatives,txt('Alternative causes · current alone cannot decide',0,-3.65,27)); self.finish()


class S17Rule(Timed):
    def construct(self):
        r=rule(); paths=factor_paths(); self.add(equation(),r,paths)
        self.at('a lost current'); self.play(Indicate(r,color=RED),run_time=.4)
        self.at('which factor'); self.play(Indicate(paths[0],color=YELLOW),run_time=.35); self.finish()

class S18Pore(Timed):
    def construct(self):
        eq=equation(); r=rule(); paths=factor_paths(); self.add(eq,r,paths)
        stage=linked_gate().scale(1.5).move_to([-2.9,-.15,0])
        self.at('Evidence about permeation'); self.play(FadeOut(r),FadeOut(paths),FadeIn(stage),run_time=.35)
        self.at('speaks more directly'); self.play(FadeIn(txt('Permeation → pore',2.8,1.9,36,GREEN)),run_time=.3)
        cx=stage[1].get_x(); mouth=stage[1].get_top()[1]
        a=ion(cx,mouth+.55).scale(1.75)
        b=VGroup(RegularPolygon(n=6,radius=.43,color=TEXT,fill_color=BG,fill_opacity=1),T('−',32,TEXT)).move_to([cx-1.55,mouth+.55,0])
        sel=txt('selectivity',-5.25,-1.8,30,YELLOW)
        lead=Line(sel.get_top()+UP*.12,stage[1][0].get_left()+LEFT*.1,color=YELLOW)
        self.at('which ions pass'); self.play(FadeIn(a),FadeIn(b),FadeIn(sel),Create(lead),run_time=.25)
        self.play(a.animate.move_to([cx,stage[1].get_bottom()[1]-.55,0]),
            b.animate.move_to([cx,mouth+.42,0]),run_time=.9)
        stop=Line([cx-.45,mouth-.04,0],[cx+.45,mouth-.04,0],color=RED,stroke_width=6)
        self.add(stop,T('blocked',28,TEXT).next_to(b,RIGHT,buff=.22),T('passes',30,YELLOW).next_to(a,RIGHT,buff=.22))
        self.at('how much current'); self.play(FadeIn(single_event(3.1,.65,4.6,2.35)),run_time=.4)
        self.add(txt('one open channel',3.1,-2.6,32,YELLOW),txt('Illustrative ion discrimination',0,-3.45,30)); self.finish()

class S19Limit(Timed):
    def construct(self):
        stage=linked_gate().scale(1.55).move_to([3.5,-.15,0]); self.add(stage)
        self.add(txt('Evidence ladder',-3.35,3.05,40,GREEN))
        spine=Line([-5.75,-1.6,0],[-5.75,2.45,0],color=GREEN,stroke_width=5)
        self.add(spine)
        def rung(s,y,color=GREEN):
            return VGroup(Line([-5.75,y,0],[-5.25,y,0],color=color,stroke_width=5),txt(s,-2.8,y,34,color))
        self.add(rung('Permeation',2.05))
        badge=Square(side_length=.25,color=PINK,fill_color=PINK,fill_opacity=1).move_to([2.5,-.5,0])
        residue_leader=Line([-.8,.7,0],badge.get_left()+LEFT*.1,color=PINK)
        self.at('a residue reached'); self.play(FadeIn(rung('Reachable residue',.7,PINK)),FadeIn(badge),Create(residue_leader),run_time=.4)
        self.at('activity of the protein'); self.play(FadeIn(rung('Protein alone',-.65)),run_time=.4)
        partners=VGroup(*[RoundedRectangle(width=.7,height=1.05,corner_radius=.16,color=TEAL,fill_color=TEAL,fill_opacity=.6).move_to([x,-.5,0]) for x in (1.78,5.22)])
        self.at('But partners'); self.play(FadeOut(residue_leader),FadeIn(partners),FadeIn(txt('partners',3.5,2.65,34,TEAL)),
            Create(Line([2.7,2.35,0],partners[0].get_top()+UP*.1,color=TEAL)),
            Create(Line([4.3,2.35,0],partners[1].get_top()+UP*.1,color=TEAL)),run_time=.4)
        caveat=txt('Partners can change permeation too',0,-2.95,32,TEAL)
        self.at('change permeation too'); self.play(FadeIn(caveat),run_time=.35)
        self.at('several rungs together'); self.play(FadeOut(caveat),FadeIn(txt('Several rungs together',0,-3.05,46,GREEN)),run_time=.35); self.finish()


class S20Take(Timed):
    def construct(self):
        self.add(equation(),txt('Through every experiment',0,1.65,38))
        questions=VGroup(txt('Which factor did it test?',0,.1,52,YELLOW),txt('What did it rule out?',0,-1.85,52,GREEN))
        self.at('Carry one question'); self.play(FadeIn(questions),run_time=.8)
        self.at('which factor did'); self.play(Indicate(questions[0]),run_time=.4)
        self.at('what did it'); self.play(Indicate(questions[1]),run_time=.4); self.finish()


class S21End(EndCard):
    LINE='Which factor did it test,\nand what did it rule out?'

    def construct(self):
        self.add(txt(self.LINE,0,.3,48),txt('biochemistrypedia.com',0,-1.5,30,TEAL))
        self.finish()
