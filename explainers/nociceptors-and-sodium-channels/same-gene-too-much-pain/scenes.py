"""Chapter 3: The Same Gene, Too Much Pain.
COLOR MAP: YELLOW SCN9A; ORANGE Nav1.7 variants; TEXT wild type;
RED loss / painful extremities; GREY membranes / axes; TEAL evidence cues.
All channels are mechanical schematics, not molecular structures.
Curves use Boltzmann activation and first-order exponential relaxation;
parameters and relative times are illustrative, never measured fits.
"""
import importlib.util
from pathlib import Path
import numpy as np
from bp_style import *
_spec=importlib.util.spec_from_file_location('reference',Path(__file__).resolve().parent.parent/'scenes.old.py')
ref=importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ref)
ORANGE=ref.ORANGE
arr=ref.arr


def lines(ss,color=TEXT,size=28,buff=.16):
    return VGroup(*[T(s,size,color) for s in ss]).arrange(DOWN,buff=buff)


def heading(s):
    return T(s,34,font=TITLE_FONT).move_to([0,3.12,0])


def gate(x=0,y=0,opened=False,scale=1,color=ORANGE,state=None):
    """A labelled mechanical gate: horizontal shut bar, lifted open bar,
    or red block for inactivation. No inferred molecular geometry."""
    state=state or ('open' if opened else 'closed')
    band=VGroup(*[Rectangle(width=1.05,height=.55,color=GREY,fill_opacity=.22).move_to([s*.99,0,0]) for s in [-1,1]])
    walls=VGroup(*[RoundedRectangle(width=.24,height=1.65,corner_radius=.08,color=color,fill_opacity=.6).move_to([s*.52,0,0]) for s in [-1,1]])
    if state=='closed':
        door=Line([-.4,0,0],[.4,0,0],color=color,stroke_width=9)
    else:
        # An open pore has no offset door stub beside its left wall.
        door=Line([-.4,0,0],[.4,0,0],color=color,stroke_width=9).set_opacity(0)
    plug=RoundedRectangle(width=.72,height=.33,corner_radius=.08,color=RED,fill_opacity=1).move_to([0,-.35,0])
    if state!='inactivated': plug.set_opacity(0)
    flow=arr([0,.65,0],[0,-.65,0],color,w=3,tip=.12)
    if state!='open': flow.set_opacity(0)
    return VGroup(band,walls,door,plug,flow).scale(scale).move_to([x,y,0])


def legend():
    return T('schematic: bar = closed   gap + arrow = open   red block = inactivated',26,GREY).move_to([0,-3.22,0])


def channel(x=0,y=0,opened=False,scale=1.7):
    return VGroup(gate(x,y,opened,scale),T('Nav1.7',30,ORANGE).move_to([x,y-1.65,0]))


def person(color=GREY):
    head=Circle(.34,color=color).move_to([0,2.1,0])
    torso=RoundedRectangle(width=1.15,height=1.9,corner_radius=.25,color=color).move_to([0,.65,0])
    arms=VGroup(*[Line([s*.58,1.35,0],[s*1.3,-.25,0],color=color,stroke_width=9) for s in [-1,1]])
    legs=VGroup(*[Line([s*.3,-.3,0],[s*.45,-2,0],color=color,stroke_width=10) for s in [-1,1]])
    ends=VGroup(*[Ellipse(width=w,height=h,color=GREY,fill_opacity=.15).move_to([x,y,0]) for x,y,w,h in [(-1.3,-.3,.38,.6),(1.3,-.3,.38,.6),(-.55,-2.1,.65,.32),(.55,-2.1,.65,.32)]])
    return VGroup(head,torso,arms,legs,ends)


def family(x,color):
    nodes=VGroup(Square(.65),Circle(.325),Circle(.325),Square(.65))
    for n,p in zip(nodes,[[-.95,1.6,0],[.95,1.6,0],[-.95,-1.6,0],[.95,-1.6,0]]):
        n.move_to(p).set_color(color).set_fill(color,.7)
    joins=VGroup(Line([-.62,1.6,0],[.62,1.6,0]),Line([0,1.6,0],[0,-.6,0]),Line([-.95,-.6,0],[.95,-.6,0]),*[Line([s*.95,-.6,0],[s*.95,-1.27,0]) for s in [-1,1]])
    joins.set_color(GREY)
    return VGroup(joins,nodes).move_to([x,-.15,0])


def question():
    c=channel(-3.5,-.25,scale=1.75)
    slots=VGroup(*[VGroup(RoundedRectangle(width=4.8,height=1.28,corner_radius=.12,color=GREY),T(s,30)) for s in ['opening','closing','inactivating']]).arrange(DOWN,buff=.35).move_to([2.7,-.25,0])
    return VGroup(lines(['What could the channel do wrong','to cause too much pain?'],TEXT,32).move_to([0,2.72,0]),c,slots,legend())


def three_results():
    cards=VGroup()
    for x,title,result in zip([-4.2,0,4.2],['opening','closing','inactivating'],['opens too easily','closes too slowly','fails to inactivate']):
        cards.add(VGroup(RoundedRectangle(width=3.95,height=5.65,corner_radius=.16,color=GREY).move_to([x,0,0]),T(title,30).move_to([x,2.25,0]),gate(x,.95,True,1.15),T(result,26,ORANGE).move_to([x,-2.25,0])))
    return cards


def rig():
    cell=Circle(1.12,color=GREY,fill_opacity=.12).move_to([2,-.65,0])
    pip=VGroup(Line([2.45,.2,0],[3.35,1.55,0],color=TEXT,stroke_width=4),Line([2.65,.25,0],[3.55,1.55,0],color=TEXT,stroke_width=4))
    box=RoundedRectangle(width=1.9,height=1,corner_radius=.1,color=GREY).move_to([5,1.55,0])
    return VGroup(cell,pip,box,Line([3.55,1.55,0],[4.05,1.55,0],color=GREY),T('cell',28).move_to([2,-2.05,0]),T('pipette',28).move_to([2.7,2.15,0]),T('amplifier',28).move_to([5,2.5,0]),T('patch-clamp recording',28,GREY).move_to([3.4,-2.8,0]))


def activation(v,variant=False):
    return 1/(1+np.exp(((-42 if variant else -28)-v)/6))


def transient(t):
    return (1-np.exp(-t/.07))*np.exp(-t/.45)

# Equal peak heights: normalize each model by its computed maximum.
_grid=np.linspace(0,5,10001)
_peak=float(np.max(transient(_grid)))
_ppeak=float(np.max((1-np.exp(-_grid/.07))*(.25+.75*np.exp(-_grid/.45))))

def persistent(t):
    return (1-np.exp(-t/.07))*(.25+.75*np.exp(-t/.45))/_ppeak


def graph(kind='activation',slow=1.65):
    act=kind=='activation'
    ax=Axes(x_range=[-100,20,20] if act else [0,5,1],y_range=[0,1, .5],x_length=10.25 if act else 9.5,y_length=4.55,tips=False,axis_config={'color':GREY,'include_tip':False,'include_ticks':False}).move_to([.5 if act else .1,-.05,0])
    ylabel=lines(['fraction of','channels open'] if act else ['inward current','magnitude','(relative units)'],TEXT,26).rotate(PI/2).move_to([-6.12,0,0])
    labels=VGroup(ylabel,T('voltage (mV)' if act else 'time (relative units)',28).move_to([.5 if act else .1,-2.98,0]),T('illustrative kinetics • not measured fits',26,GREY).move_to([0,-3.5,0]))
    for yy in [0,1]: labels.add(T(str(yy),26,GREY).next_to(ax.c2p(-100 if act else 0,yy),LEFT,buff=.15))
    for xx in ([-100,-60,-20,20] if act else [0,1,2,3,4,5]): labels.add(T(str(xx),26,GREY).next_to(ax.c2p(xx,0),DOWN,buff=.13))
    if act: f=lambda v:activation(v); g=lambda v:activation(v,True)
    elif kind=='tail': f=lambda t:np.exp(-t/.45); g=lambda t:np.exp(-t/slow)
    else: f=lambda t:transient(t)/_peak; g=persistent
    xr=[-100,20,.2] if act else [0,5,.01]
    a=ax.plot(f,x_range=xr,color=TEXT,stroke_width=5,use_smoothing=False)
    b=ax.plot(g,x_range=xr,color=ORANGE,stroke_width=5,use_smoothing=False)
    # Labels sit beside the curves, with short leaders to resolve close tails.
    if act:
        wt=T('wild type',27,TEXT).move_to([3.4,1.1,0])
        var=T('variant',27,ORANGE).move_to([-.6,2.5,0])
        key=VGroup(wt,var,Line(wt.get_top(),ax.c2p(-16,f(-16)),color=TEXT),Line(var.get_bottom(),ax.c2p(-33,g(-33)),color=ORANGE))
    else:
        wt=T('wild type',27,TEXT).move_to(ax.c2p(5,0)+RIGHT*1.0+UP*.18)
        var=T('variant',27,ORANGE).move_to(ax.c2p(5,g(5))+RIGHT*1.0+UP*(.8 if kind=='tail' else .25))
        key=VGroup(wt,var,DashedLine(wt.get_left()+LEFT*.08,ax.c2p(5,f(5)),color=TEXT,stroke_width=1.5,dash_length=.06),DashedLine(var.get_left()+LEFT*.08,ax.c2p(5,g(5)),color=ORANGE,stroke_width=1.5,dash_length=.06))
    return ax,labels,a,b,key


def voltage_step(tail=False):
    """Illustrative voltage-clamp protocol, separate from the current traces."""
    box=RoundedRectangle(width=4.9,height=1.15,corner_radius=.1,color=GREY,stroke_opacity=.6).move_to([1.6,1.3,0])
    lab=T('voltage step',24,GREY).move_to([1.6,1.64,0])
    low,high=.99,1.28
    points=([[-.55,high,0],[.25,high,0],[.25,low,0],[3.55,low,0]] if tail else
            [[-.55,low,0],[.25,low,0],[.25,high,0],[3.55,high,0]])
    step=VMobject(color=TEAL,stroke_width=3).set_points_as_corners(points)
    note=T('returns negative' if tail else 'held depolarized',23,TEAL).move_to([1.6,.5,0])
    return VGroup(box,lab,step,note)


def hypothetical_train():
    dt=.003
    tt=np.arange(0,9,dt); v=0.; spikes=[]
    for t in tt:
        drive=1.3 if .9 <= t <= 7.1 else 0
        v += dt*(drive-v)/.9
        if v>=1:
            spikes.append(t); v=0.
    yy=np.zeros_like(tt)
    for t in spikes:
        # Fixed analytic spike and afterpotential, triggered by threshold events.
        yy += np.exp(-((tt-t)/.09)**2)-.12*np.exp(-((tt-t-.24)/.14)**2)
    return tt, yy


def region(ax,f,g,start,end,color=ORANGE,opacity=.25):
    xs=np.linspace(start,end,160)
    return Polygon(*[ax.c2p(x,f(x)) for x in xs],*[ax.c2p(x,g(x)) for x in xs[::-1]],stroke_width=0,fill_color=color,fill_opacity=opacity)


class S00Title(TitleCard):
    LESSON='Nociceptors and the Sodium Channels of Pain'
    TITLE='The Same Gene, Too Much Pain'
    def construct(self):
        card=VGroup(T('BIOCHEMISTRYPEDIA',26,TEAL),T(self.LESSON,26,GREY),T(self.TITLE,48,font=TITLE_FONT),Line(LEFT*1.5,RIGHT*1.5,color=GOLD)).arrange(DOWN,buff=.42)
        self.play(FadeIn(card),run_time=.5); self.finish()


class S01Question(SpokenScene):
    def construct(self):
        gene=chip('SCN9A',YELLOW,44).move_to([0,2.65,0])
        left=chip('no pain',RED,40).move_to([-3.7,-.55,0]); right=chip('burning pain',ORANGE,40).move_to([3.7,-.55,0])
        self.add(gene,left,right,arr(gene.get_bottom(),left.get_top(),YELLOW),arr(gene.get_bottom(),right.get_top(),YELLOW))
        self.at('Losing this channel'); self.play(Indicate(left,color=RED),run_time=.5)
        self.at('How could changing'); self.play(FadeIn(lines(['How could changing the same gene','cause too much pain?'],TEXT,34).move_to([0,-2.5,0])),Indicate(right,color=ORANGE),run_time=.6); self.finish()


class S02OtherWay(SpokenScene):
    def construct(self):
        self.add(chip('SCN9A',YELLOW,32).move_to([0,3.05,0]))
        for x,title,color in [(-3.2,'no measurable current',RED),(3.2,'conducting current',ORANGE)]:
            self.add(RoundedRectangle(width=5.9,height=5.7,corner_radius=.15,color=GREY).move_to([x,-.25,0]),T(title,28,color).move_to([x,2.1,0]),gate(x,.8,x>0,.8,color),T('schematic',26,GREY).move_to([x,-2.7,0]))
            ax=Axes(x_range=[0,5,1],y_range=[0,1,1],x_length=4.45,y_length=1.6,tips=False,axis_config={'include_ticks':False,'color':GREY}).move_to([x,-1.2,0])
            f=(lambda t:0) if x<0 else (lambda t:transient(t)/_peak)
            tr=ax.plot(f,x_range=[0,5,.015],color=color,use_smoothing=False,stroke_width=5)
            self.add(ax,tr,T('time',26,GREY).move_to([x,-2.3,0]))
        self.add(T('current (same relative scale)',26).move_to([0,-3.55,0]))
        self.at('Variants in the same'); self.wait(.2)
        self.at('These ones alter gating'); self.play(Indicate(self.mobjects[8],color=ORANGE),run_time=.5); self.finish()


class S03Phenotype(SpokenScene):
    def construct(self):
        p=person().scale(1.15).move_to([-2.9,-.3,0]); self.add(p,heading('Primary erythermalgia'))
        label=lines(['burning pain,','hands and feet'],RED,36).move_to([2.8,0,0])
        self.at('burning pain'); self.play(p[-1].animate.set_color(RED).set_fill(RED,.8),FadeIn(label),GrowArrow(arr([1,-.6,0],p[-1][1].get_right(),RED)),run_time=.6); self.finish()


class S04Intact(SpokenScene):
    def construct(self):
        g=gate(-.8,-.25,False,2.6)
        sensor=RoundedRectangle(width=.65,height=1.25,corner_radius=.12,color=YELLOW,fill_opacity=.3).move_to([1.25,.85,0])
        q=T('?',42,YELLOW).move_to(sensor)
        self.add(g,sensor,heading('An intact channel in the membrane'),T('Nav1.7',32,ORANGE).move_to([-.8,2.2,0]),T('gate',28,ORANGE).move_to([3.9,-1.3,0]),arr([3.2,-1.3,0],[.3,-.25,0],ORANGE),T('membrane',28,GREY).move_to([-4.6,-1.2,0]),legend())
        self.at('The channel protein'); self.play(Indicate(g,color=ORANGE),run_time=.5)
        self.at('Something about its gating'); self.play(FadeIn(q),FadeIn(T('voltage sensor',30,YELLOW).move_to([3.9,1.4,0])),GrowArrow(arr([2.6,1.4,0],[1.65,1,0],YELLOW)),run_time=.5); self.finish()


class S05Predict(SpokenScene):
    def construct(self):
        q=question(); self.add(q)
        self.at('In gating terms'); self.play(Indicate(q[2],color=YELLOW,scale_factor=1.02),run_time=.6); self.finish()


class S06Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        q=question(); q[1][1].set_opacity(.45); q[3].set_opacity(0)
        self.add(q,T('pause and predict',30,YELLOW).move_to([0,-3.22,0])); self.wait(5)


class S07ThreeWays(SpokenScene):
    def construct(self):
        cards=three_results()
        cards[0][2].become(gate(-4.2,.95,False,1.15))
        for c in cards: c[3].set_opacity(0)
        # Fill each panel from the start with the setup for its upcoming change.
        normal=gate(-.85,-.85,True,.45,color=TEXT)
        variant=gate(.85,-.85,True,.45)
        comparison=VGroup(normal,variant,T('normal',26).move_to([-.85,-1.55,0]),T('variant',26,ORANGE).move_to([.85,-1.55,0]))
        stimulus=T('small depolarization',26,GREY).move_to([-4.2,-.7,0])
        pulse=VMobject(color=GREY,stroke_width=3).set_points_as_corners([[-5.45,-1.45,0],[-4.85,-1.45,0],[-4.85,-1.1,0],[-3.55,-1.1,0],[-3.55,-1.45,0],[-2.95,-1.45,0]])
        ax=Axes(x_range=[0,5,1],y_range=[0,1,1],x_length=3,y_length=1.25,tips=False,axis_config={'include_ticks':False,'color':GREY}).move_to([4.2,-.85,0])
        baseline=ax.plot(lambda t:0,x_range=[0,5,.02],color=GREY,use_smoothing=False)
        self.add(cards,legend(),comparison,stimulus,pulse,ax,baseline,T('current',26,GREY).move_to([4.2,-.22,0]))
        self.at('Open too easily'); self.play(Transform(cards[0][2],gate(-4.2,.95,True,1.15)),cards[0][3].animate.set_opacity(1),pulse.animate.set_color(ORANGE),run_time=.5)
        self.at('close too slowly')
        # After stimulus removal, normal has closed but variant remains open.
        self.play(Transform(normal,gate(-.85,-.85,False,.45,color=TEXT)),cards[1][3].animate.set_opacity(1),FadeIn(T('stimulus ended',26).move_to([0,-.22,0])),run_time=.55)
        self.at('fail to inactivate')
        tr=ax.plot(persistent,x_range=[0,5,.02],color=ORANGE,use_smoothing=False)
        self.play(FadeOut(baseline),Create(tr),cards[2][3].animate.set_opacity(1),run_time=.45); self.finish()


class S08Allthree(SpokenScene):
    def construct(self):
        cards=three_results()
        for c in cards:
            c[0].become(RoundedRectangle(width=3.95,height=4.65,corner_radius=.16,color=GREY).move_to([c[0].get_x(),.3,0]))
            c[1].move_to([c[1].get_x(),2.2,0])
            c[2].scale(.98/1.15).move_to([c[2].get_x(),1.15,0])
            c[3].move_to([c[3].get_x(),-1.65,0])
        self.add(cards,chip('SCN9A',YELLOW,30).move_to([0,3.3,0]))
        self.add(T('small depolarization',26,GREY).move_to([-4.2,-.65,0]))
        self.add(gate(-.85,-.55,False,.4,color=TEXT),gate(.85,-.55,True,.4),T('stimulus ended',26).move_to([0,.15,0]),T('normal',26).move_to([-.85,-1.13,0]),T('variant',26,ORANGE).move_to([.85,-1.13,0]))
        ax=Axes(x_range=[0,5,1],y_range=[0,1,1],x_length=3,y_length=1.05,tips=False,axis_config={'include_ticks':False,'color':GREY}).move_to([4.2,-.6,0])
        self.add(ax,ax.plot(persistent,x_range=[0,5,.02],color=ORANGE,use_smoothing=False))
        for x,ss in [(-4.2,['erythermalgia','variants','in vitro']),(0,['erythermalgia','variants','in vitro']),(4.2,['paroxysmal extreme','pain disorder variants','in vitro'])]:
            self.add(lines(ss,YELLOW,26,buff=.1).move_to([x,-2.85,0]))
        self.at('All three have been'); self.play(Indicate(cards,color=YELLOW,scale_factor=1.01),run_time=.6); self.finish()


class S09Yang(SpokenScene):
    def construct(self):
        fam=family(-3.1,ORANGE).scale(1.18)
        lone=person(ORANGE).scale(1.03).move_to([3.3,-.3,0])
        self.add(fam,lone,heading('SCN9A missense variants'),T('family • schematic pedigree',28).move_to([-3.1,-2.98,0]),T('sporadic patient',30).move_to([3.3,-2.98,0]),T('Yang and colleagues, 2004',26,GREY).move_to([0,-3.5,0]))
        self.at('in a family'); self.play(Indicate(fam,color=ORANGE),run_time=.5)
        self.at('and in a sporadic'); self.play(Indicate(lone,color=ORANGE),run_time=.5); self.finish()


class S10Rig(SpokenScene):
    def construct(self):
        cs=VGroup(chip('I848T',ORANGE,34),chip('L858H',ORANGE,34)).arrange(DOWN,buff=.45).move_to([-3.65,-.2,0])
        self.add(rig(),lines(['variants from','Yang et al.'],YELLOW,32).move_to([-3.65,2,0]),cs,arr([-2.1,0,0],[.5,0,0],YELLOW),T('two tested next',26,ORANGE).move_to([-3.65,-2.1,0]))
        self.at('Take each variant'); self.play(Indicate(cs,color=ORANGE),run_time=.7); self.finish()


class S11Temp(SpokenScene):
    def construct(self):
        r=rig().scale(.8).move_to([3,-.1,0])
        for label in r:
            if isinstance(label,Text): label.scale(1.25)
        self.add(r)
        x=-4.1
        bulb=Circle(.47,color=TEXT,fill_color=ORANGE,fill_opacity=.8).move_to([x,-1.8,0])
        stem=RoundedRectangle(width=.4,height=4.2,corner_radius=.18,color=TEXT).move_to([x,.55,0])
        fluid=Rectangle(width=.22,height=2.55,stroke_width=0,fill_color=ORANGE,fill_opacity=1).move_to([x,-.52,0])
        self.add(stem,fluid,bulb,T('temperature',30).move_to([-3.4,3.1,0]))
        for yy,txt in [(.75,'21 °C'),(2.25,'37 °C • body')]:
            self.add(Line([x+.3,yy,0],[x+.65,yy,0],color=TEXT),T(txt,28).next_to([x+.8,yy,0],RIGHT,buff=.1))
        self.at('about room temperature'); self.play(Indicate(fluid,color=ORANGE),run_time=.5)
        self.at('kinetics are slower'); self.play(FadeIn(lines(['kinetics slower than at body temperature'],TEXT,28).move_to([0,-3.1,0])),run_time=.4); self.finish()


class S12Cummins(SpokenScene):
    def construct(self):
        cs=VGroup(chip('I848T',ORANGE,32),chip('L858H',ORANGE,32),chip('wild type',TEXT,32)).arrange(DOWN,buff=.5).move_to([-3.6,.2,0])
        self.add(rig(),cs,heading('HEK293 cells • about 21 °C'))
        self.at('Two of those variants')
        for c in cs[:2]:
            arrow=arr(c.get_right(),[.7,-.6,0],ORANGE)
            self.play(GrowArrow(arrow),Indicate(c,color=ORANGE),run_time=.55); self.play(FadeOut(arrow),run_time=.15)
        self.at('compared with wild type'); self.play(GrowArrow(arr(cs[2].get_right(),[.7,-.6,0],TEXT)),Indicate(cs[2],color=TEXT),run_time=.65); self.finish()


class S13Shift(SpokenScene):
    def construct(self):
        ax,labels,a,b,key=graph(); self.add(ax,labels,a,key,heading('Activation shifts left'))
        self.at('Activation was shifted'); self.play(Create(b),run_time=.65)
        self.at('more negative voltages'); self.play(GrowArrow(arr(ax.c2p(-25,.52),ax.c2p(-43,.52),ORANGE)),run_time=.45)
        rest=DashedLine(ax.c2p(-65,0),ax.c2p(-65,1),color=YELLOW)
        zone=region(ax,lambda v:activation(v,True),lambda v:activation(v),-65,-42)
        label=lines(['resting voltage','−65 mV'],YELLOW,26).move_to([-4.15,1.4,0])
        self.at('The channel opened'); self.play(Create(rest),FadeIn(zone),FadeIn(label),run_time=.5)
        self.add(T('variant opens earlier',27,ORANGE).move_to([-3.55,-.1,0]),arr([-2,-.4,0],ax.c2p(-52,activation(-52,True)),ORANGE)); self.finish()


class S14Deact(SpokenScene):
    def construct(self):
        ax,labels,a,b,key=graph('tail',slow=.85); self.add(ax,labels,a,b,key,heading('Deactivation slows'))
        self.add(voltage_step(tail=True))
        self.at('Deactivation was slowed'); final=graph('tail'); self.play(Transform(b,final[3]),Transform(key,final[4]),run_time=.8)
        self.at('Once open'); self.play(Indicate(b,color=ORANGE,scale_factor=1.015),run_time=.6); self.finish()


class S15Meaning(SpokenScene):
    def construct(self):
        self.add(RoundedRectangle(width=5.3,height=5.7,corner_radius=.15,color=GREY).move_to([-3.65,.25,0]),RoundedRectangle(width=6.1,height=5.7,corner_radius=.15,color=GREY).move_to([2.7,.25,0]))
        c=gate(-3.65,.25,True,1.55)
        self.add(c,lines(['Nav1.7','nociceptor membrane'],ORANGE,28).move_to([-3.65,2.3,0]),T('hypothetical firing',30).move_to([2.7,2.55,0]))
        ax=Axes(x_range=[0,9,3],y_range=[-.2,1.1,.5],x_length=4.55,y_length=2.9,tips=False,axis_config={'include_ticks':False,'color':GREY}).move_to([3,.2,0])
        self.add(ax,T('membrane voltage',26).rotate(PI/2).move_to([.0,.3,0]),T('time',26).move_to([3,-1.45,0]))
        x0,xon,xoff,xend=[ax.c2p(t,0)[0] for t in [0,.9,7.1,9]]
        strip=RoundedRectangle(width=5.45,height=.9,corner_radius=.08,color=GREY,stroke_opacity=.5).move_to([2.7,-2.1,0])
        step=VMobject(color=TEXT,stroke_width=4).set_points_as_corners([[x0,-2.35,0],[xon,-2.35,0],[xon,-2.13,0],[xoff,-2.13,0],[xoff,-2.35,0],[xend,-2.35,0]])
        current=T('stimulus current',24,GREY).move_to([2.7,-1.87,0])
        # Show the stimulus before drawing any part of the hypothetical spike train.
        self.add(strip,current,step)
        self.at('A channel that opens'); self.play(Indicate(c,color=ORANGE),run_time=.5)
        self.at('closes too late'); self.play(Indicate(step,color=YELLOW,scale_factor=1.0),FadeIn(T('small stimulus',26).move_to([-3.65,-1.8,0])),GrowArrow(arr([-2.2,-1.8,0],[.5,-2.1,0],TEXT)),run_time=.5)
        xx,yy=hypothetical_train(); tr=ax.plot_line_graph(xx,yy,line_color=TEXT,add_vertex_dots=False)['line_graph']; tr=DashedVMobject(tr,num_dashes=60)
        self.at('should make its neuron'); self.play(Create(tr),run_time=.7)
        self.at('That is an expectation'); self.play(FadeIn(lines(['expectation from a cell line','not recorded here'],TEXT,28).move_to([0,-3.15,0])),run_time=.5); self.finish()


class S16Pepd(SpokenScene):
    def construct(self):
        ax,labels,a,b,key=graph('persistent')
        self.add(ax,labels,a,b,key,heading('Paroxysmal extreme pain disorder'),voltage_step())
        self.at('is impaired'); self.play(Indicate(b,color=ORANGE,scale_factor=1.015),run_time=.65); self.finish()


class S17Persistent(SpokenScene):
    def construct(self):
        ax,labels,a,b,key=graph('persistent'); self.add(ax,labels,a,b,key,heading('Paroxysmal extreme pain disorder'),voltage_step())
        # A tapered opacity ramp avoids an artificial rectangular left boundary.
        shades=VGroup()
        for i,(lo,hi) in enumerate(zip(np.linspace(1.35,5,50)[:-1],np.linspace(1.35,5,50)[1:])):
            shades.add(region(ax,persistent,lambda t:0,lo,hi,opacity=.28*min(1,(i+1)/10)))
        self.at('What is left behind'); self.play(FadeIn(shades),run_time=.5)
        self.at('persistent sodium current'); self.play(FadeIn(T('persistent sodium current',28,ORANGE).move_to([1.4,0,0])),GrowArrow(arr([1.8,-.25,0],ax.c2p(3.7,.16),ORANGE)),run_time=.5)
        self.at('three mutant channels'); self.play(Transform(labels[2],T('three mutants • in vitro • illustrative kinetics',26,ORANGE).move_to([0,-3.5,0])),run_time=.4); self.finish()


class S18Sum(SpokenScene):
    def construct(self):
        self.add(chip('SCN9A',YELLOW,32).move_to([0,3.1,0]))
        xs=[-4.35,0,4.35]
        for x,t in zip(xs,['variant type','channel effect','phenotype']): self.add(T(t,30,GREY).move_to([x,2.1,0]))
        rows=[(['loss-of-function','variants'],['no current'],['pain loss']),(['I848T / L858H'],['opens too easily /','closes too slowly'],['primary','erythermalgia']),(['paroxysmal extreme','pain disorder variants'],['fails to inactivate'],['paroxysmal extreme','pain disorder'])]
        for i,row in enumerate(rows):
            y=.85-i*1.65
            self.add(Line([-6.25,y+.72,0],[6.25,y+.72,0],color=GREY,stroke_opacity=.4))
            for x,ss in zip(xs,row): self.add(lines(ss,RED if i==0 else ORANGE,27,buff=.12).move_to([x,y,0]))
        self.at('Same gene'); self.wait(.2); self.finish()


class S19Onegene(SpokenScene):
    def construct(self):
        gene=chip('SCN9A',YELLOW,38).move_to([0,3,0]); self.add(gene)
        families=[]
        for x,color,label in [(-3.4,RED,'pain loss'),(3.4,ORANGE,'burning pain')]:
            fam=family(x,color).scale(1.15); families.append(fam)
            self.add(fam,VGroup(Line(gene.get_bottom(),[x,2.45,0],color=YELLOW,stroke_width=5),arr([x,2.45,0],[x,1.69,0],YELLOW)),T(label,36,color).move_to([x,-2.85,0]))
        self.at('remove pain'); self.play(Indicate(families[0],color=RED,scale_factor=1.015),run_time=.4)
        self.at('and cause it'); self.play(Indicate(families[1],color=ORANGE,scale_factor=1.015),run_time=.4); self.finish()


class S20Cellline(SpokenScene):
    def construct(self):
        self.add(heading('Different levels of evidence'),Line([0,-3.1,0],[0,2.55,0],color=GREY))
        # Connected side walls, bottom and rim form one culture dish.
        dish=VGroup(Ellipse(width=2.7,height=.65,color=TEXT),Line([-1.35,0,0],[-1.35,-.75,0],color=TEXT),Line([1.35,0,0],[1.35,-.75,0],color=TEXT),ArcBetweenPoints([-1.35,-.75,0],[1.35,-.75,0],angle=PI/5,color=TEXT)).move_to([-4.6,.1,0])
        ax=Axes(x_range=[0,5,1],y_range=[0,1,1],x_length=2.1,y_length=2,tips=False,axis_config={'include_ticks':False,'color':GREY}).move_to([-1.65,.3,0]); tr=ax.plot(persistent,x_range=[0,5,.02],color=ORANGE,use_smoothing=False)
        human=person().scale(.8).move_to([3.4,.25,0])
        self.add(dish,ax,tr,human,lines(['cultured cells,','channel recordings'],TEXT,30).move_to([-3.35,-2.45,0]),lines(['people,','reported pain'],ORANGE,30).move_to([3.4,-2.45,0]))
        self.at('These gating measurements'); self.play(Indicate(tr,color=ORANGE),run_time=.5)
        self.at('The pain syndromes'); self.play(Indicate(human,color=ORANGE),run_time=.5); self.finish()


class S21Through(SpokenScene):
    def construct(self):
        panels=VGroup()
        for x,label in zip([-4.5,0,4.5],['channel','neuron','behaviour']):
            panels.add(VGroup(RoundedRectangle(width=3.5,height=6,corner_radius=.18,color=YELLOW if x==0 else GREY).move_to([x,0,0]),T(label,31).move_to([x,2.4,0])))
        pore=gate(-4.5,0,True,1.05)
        soma=Circle(.65,color=TEXT).move_to([0,.3,0])
        neur=VGroup(soma,Line([0,-.35,0],[0,-2,0],color=TEXT),Line([-.5,.65,0],[-1.2,1.5,0],color=TEXT),Line([.5,.65,0],[1.2,1.5,0],color=TEXT))
        human=person().scale(.8).move_to([4.5,-.2,0])
        self.add(panels,pore,neur,human,arr([-2.7,0,0],[-1.8,0,0]),arr([1.8,0,0],[2.7,0,0]))
        self.at('pass through the neuron'); self.play(Indicate(panels[1][0],color=YELLOW,scale_factor=1.02),run_time=.6); self.finish()


class S22Direction(SpokenScene):
    def construct(self):
        self.add(heading('What the channel does'))
        for yy,ss,color in [(1.65,['no current'],RED),(.25,['opens too easily / closes too slowly'],ORANGE),(-1.15,['fails to inactivate'],ORANGE)]:
            self.add(RoundedRectangle(width=10.8,height=1.15,corner_radius=.14,color=color).move_to([0,yy,0]),lines(ss,color,31).move_to([0,yy,0]))
        collector=VGroup(Line([-5.4,1.65,0],[-6,1.65,0]),Line([-5.4,.25,0],[-6,.25,0]),Line([-5.4,-1.15,0],[-6,-1.15,0]),Line([-6,1.65,0],[-6,-2.7,0]),arr([-6,-2.7,0],[3.1,-2.7,0],GREY))
        box=chip('behaviour',TEXT,32).move_to([4.3,-2.7,0])
        self.at('What the neuron does'); self.play(FadeIn(collector),FadeIn(box),FadeIn(T('depends on the neuron',30,TEXT).move_to([-1.5,-3.35,0])),run_time=.6); self.finish()


class S23Takeaway(SpokenScene):
    def construct(self):
        first=lines(['A variant list','is not a mechanism.'],TEXT,42).move_to([0,1.5,0])
        divider=Line([-4.5,0,0],[4.5,0,0],color=GOLD,stroke_opacity=.3)
        self.add(first,divider)
        self.at('The gating step'); self.play(FadeIn(lines(['The gating step is where','the mechanism starts.'],YELLOW,40).move_to([0,-1.55,0])),divider.animate.set_stroke(opacity=1),run_time=.6); self.finish()


class S24End(EndCard):
    LINE='The gating step is where the mechanism starts.'
