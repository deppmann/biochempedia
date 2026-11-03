"""Chapter 1, reviewed redraw.
COLOR MAP: YELLOW stimuli; BLUE channels / channel time constant;
PURPLE (#B58CD9) cascade enzymes / molecular gain; ORANGE (#F29E4C)
behavioural latency; TEAL electrical excitation; GREEN current / output;
GREY cells / membranes / axes; TEXT labels; RED exclusion.
Hair current: a=1-exp(-t/tau), tau=50 us (lesson teaching model).
Rod: illustrative three-stage low-pass cascade impulse response,
r(t)=(t/tp)^3 exp(3*(1-t/tp)), tp=100 ms. The lesson supplies only
the approximate peak time, not a waveform: all rod plots say schematic.
Voltage is -r(t), normalized (no invented mV data).
"""
import numpy as np
from bp_style import *
from importlib.util import spec_from_file_location, module_from_spec
_spec=spec_from_file_location('reference_film',Path(__file__).with_name('scenes.old.py'))
_ref=module_from_spec(_spec); _spec.loader.exec_module(_ref)
mapper,trace,span,bchip,arrow=_ref.mapper,_ref.trace,_ref.span,_ref.bchip,_ref.arrow
PURPLE='#B58CD9'
ORANGE='#F29E4C'


def label(s,x=0,y=3.1,size=30,color=TEXT):
    return T(s,size,color).move_to([x,y,0])


def response(t):
    z=np.asarray(t)/.1
    return z**3*np.exp(3*(1-z))


def rod(x=0,y=0,height=5.6):
    body=RoundedRectangle(width=1.65,height=height,corner_radius=.5,color=GREY,fill_opacity=.12).move_to([x,y,0])
    discs=VGroup(*[Line([x-.62,y+d,0],[x+.62,y+d,0],color=GREY,stroke_width=4) for d in np.linspace(-height/2+.5,height/2-.5,11)])
    return VGroup(body,discs)


def channel(x,y,opened=False):
    walls=VGroup(*[RoundedRectangle(width=.18,height=.7,corner_radius=.04,color=BLUE,fill_opacity=.5).move_to([x+d,y,0]) for d in (-.28,.28)])
    gate=Rectangle(width=.48,height=.22,color=BLUE,fill_opacity=1,stroke_width=0).move_to([x,y,0])
    if opened: gate.set_opacity(0)
    g=VGroup(walls,gate); g.gate=gate
    return g


def bundle(x=-2.8,base=-.4,tilt=0,scale=1,rows=1):
    # Each stereocilium rotates about its own fixed base, never the cell centre.
    xs=[-.85,0,.85]; hs=[2,2.7,3.4]
    offsets=[0] if rows==1 else [-.34,.34]
    vec=np.array([np.sin(tilt),np.cos(tilt),0])
    stems,links,pores=VGroup(),VGroup(),VGroup()
    for offset in offsets:
        bases=[np.array([x+a*scale+offset,base,0]) for a in xs]
        tops=[b+h*scale*vec for b,h in zip(bases,hs)]
        stems.add(*[Line(b,t,color=TEXT,stroke_width=(13 if rows==1 else 8)*scale) for b,t in zip(bases,tops)])
        links.add(*[Line(tops[i],bases[i+1]+(hs[i]+.28)*scale*vec,color=YELLOW,stroke_width=4) for i in range(2)])
        pores.add(*[channel(*tops[i][:2],opened=False).scale(.8,about_point=tops[i]) for i in range(2)])
    body=RoundedRectangle(width=3*scale,height=2.1*scale,corner_radius=.3,color=GREY,fill_opacity=.12).move_to([x,base-1.05*scale,0])
    return VGroup(body,stems,links,pores)


def ladder(x=-3.3,spacing=2.45):
    nodes=VGroup(*[bchip(s,c,30).move_to([x,y,0]) for s,c,y in [('rhodopsin',BLUE,spacing),('transducin',PURPLE,0),('PDE6',PURPLE,-spacing)]])
    links=VGroup(*[arrow(a.get_bottom(),b.get_top(),PURPLE) for a,b in zip(nodes,nodes[1:])])
    return VGroup(nodes,links)


def prediction():
    return VGroup(ladder(),label('What does slowness buy?',1.7,2.7,32),label('?',2,.5,100,PURPLE),label('Pause and predict',2,-1.4,34,TEAL),label('Think through the ladder',2,-2.5,28))


def log_plot():
    xx=lambda t:-5.2+10.4*(np.log10(t)+5)/5
    mp=lambda t,v:np.array([xx(t),-1.65+3.5*v,0])
    axes=VGroup(Line([-5.2,-1.65,0],[5.2,-1.65,0],color=GREY),Line([-5.2,-1.65,0],[-5.2,2.1,0],color=GREY))
    ticks=VGroup(*[VGroup(Line([xx(t),-1.8,0],[xx(t),-1.5,0],color=GREY),label(s,xx(t),-2.15,28)) for t,s in [(1e-5,'10 μs'),(1e-4,'100 μs'),(.001,'1 ms'),(.01,'10 ms'),(.1,'100 ms'),(1,'1 s')]])
    curves=VGroup(trace(lambda t:1-np.exp(-t/50e-6),1e-5,250e-6,mp,BLUE),trace(response,1e-5,1,mp,GREEN,n=1000))
    marks=VGroup(Dot(mp(50e-6,1-np.exp(-1)),color=BLUE),Dot(mp(.1,1),color=GREEN),span(xx(50e-6),xx(.1),-2.65,PURPLE))
    tags=VGroup(label('Hair channel',-3.25,2.45,28,BLUE),label('Rod (schematic)',3.15,2.45,28,GREEN))
    return VGroup(axes,ticks,curves,marks,tags)


def table(compact=False):
    # The same column boundary is carried into the rod/cone caveat.
    ys=(.95,-.7) if compact else (.55,-1.85)
    height=1.65 if compact else 2.4
    boxes=VGroup(*[Rectangle(width=4.7,height=height,color=GREY).move_to([x,y,0]) for y in ys for x in (-1.25,3.45)])
    rowlabels=VGroup(*[label(txt,0,y,32,c).align_to([-3.85,y,0],RIGHT) for txt,y,c in [('Stimulus\ngates the\npore',ys[0],BLUE),('Enzymes\nin between',ys[1],PURPLE)]])
    q1=label('Q1: stimulus → pore',-6.4,sum(ys)/2,32,BLUE).rotate(PI/2)
    headers=VGroup(label('Q2: how does the signal leave?',.8,3.35,32,TEAL),label('Own axon\nPrimary',-1.25,2.35 if not compact else 2.25,32,TEAL),label('Separate afferent\nSecondary',3.45,2.35 if not compact else 2.25,32,TEAL),*rowlabels,q1)
    items=VGroup(label('TRPV1 nerve ending\nInsect olfactory\nneuron',-1.25,ys[0],32),label('Hair cell',3.45,ys[0],36),label('Vertebrate\nolfactory neuron',-1.25,ys[1],32),label('Type II taste cell',3.45,ys[1],32))
    return VGroup(boxes,headers,items)


class S00Title(TitleCard):
    LESSON='Five Ways to Turn a Stimulus into a Current'
    TITLE='Nothing in Between, or Enzymes in Between'
    def construct(self):
        self.add(label(self.LESSON,0,2.7,28))
        self.play(FadeIn(T('Nothing in Between,\nor Enzymes in Between',44,font=TITLE_FONT)),run_time=.6)
        self.finish()


class S01Q(SpokenScene):
    def construct(self):
        h=bundle(-2.3,-.6,scale=.9); r=rod(2.3,-.3,5.2)
        self.add(h,r,label('Why accept being slow?',0,3.35,34),label('?',0,2,76,YELLOW))
        self.at('a hair cell',lead=.4); self.play(FadeIn(label('Hair cell',-2.3,-3.25,36)),run_time=.2)
        self.at('a rod hold',lead=.4); self.play(FadeIn(label('Rod',2.3,-3.25,36)),run_time=.2)
        self.finish()


class S02Q1(SpokenScene):
    def construct(self):
        xs=[-4.8,-1.6,1.6,4.8]
        self.add(label('Question 1',0,3.2,34,BLUE))
        for x,s in zip(xs,['force','odorant','heat','light']):
            self.add(label(s,x,2.3,32,YELLOW),arrow([x,1.9,0],[x,1.1,0],YELLOW),label('?',x,.3,48),channel(x,-1.3).scale(1.8),Line([x-1.35,-1.3,0],[x-.7,-1.3,0],color=GREY,stroke_width=7),Line([x+.7,-1.3,0],[x+1.35,-1.3,0],color=GREY,stroke_width=7))
        self.add(label('Ion channels',0,-2.45,30,BLUE))
        self.at('what sits between'); self.play(FadeIn(label('What sits between stimulus and pore?',0,-3.2,32)),run_time=.3)
        self.finish()


class S03Hair(SpokenScene):
    def construct(self):
        h=bundle(-2.6,-.75,scale=1.05); self.add(h,label('Hair cell',0,3.4,34))
        self.at('no enzyme'); self.play(FadeIn(label('No enzyme\nin between',3,1.9,34,BLUE)),run_time=.3)
        self.at('bending the bundle')
        push=Arrow([-5.8,2.65,0],[-1,2.65,0],color=YELLOW,buff=0,stroke_width=5)
        self.play(GrowArrow(push),Transform(h,bundle(-2.6,-.75,.23,1.05)),run_time=.65)
        self.at('pulls on tip links')
        self.play(Indicate(h[2],color=YELLOW),FadeIn(label('Direct mechanical link',3,.5,32,BLUE)),Create(arrow([.7,.5,0],h[2][1].get_center(),BLUE)),run_time=.5)
        self.at('opens transduction channels')
        ions=VGroup(*[arrow(p.get_center()+UP*.75,p.get_center()+DOWN*.7,GREEN) for p in h[3]])
        self.play(*[p.gate.animate.set_opacity(0) for p in h[3]],Create(ions),FadeIn(label('Ions enter',-4.9,.6,34,GREEN)),run_time=.4)
        self.play(*[Flash(p,color=BLUE,flash_radius=.5) for p in h[3]],run_time=.35)
        self.finish()


class S04Hairfast(SpokenScene):
    def construct(self):
        mp=mapper(-4.9,-2.1,10,4.3,250,1)
        self.add(label('Turtle hair cells'),label('Transducer current',-2.8,2.55,30,BLUE),Line(mp(0,0),mp(250,0),color=GREY),Line(mp(0,0),mp(0,1.05),color=GREY))
        for t in [0,100,250]: self.add(Line(mp(t,-.03),mp(t,.03),color=GREY),label(f'{t} μs',mp(t,0)[0],-2.55,28))
        self.at('these channels can activate'); self.play(Create(trace(lambda t:1-np.exp(-t/50),0,250,mp,BLUE)),run_time=.8)
        self.at('a time constant')
        pt=mp(50,1-np.exp(-1)); self.play(FadeIn(Dot(pt,color=BLUE)),Create(DashedLine(mp(50,0),pt,color=BLUE)),FadeIn(label('63% of final',-.5,.5,30,BLUE)),run_time=.4)
        self.at('as short as'); self.play(FadeIn(label('Time constant as short as about 50 μs',0,-3.25,32,BLUE)),run_time=.3)
        self.finish()


class S05Rod(SpokenScene):
    def construct(self):
        r=rod(-4.4,0); l=ladder(.4)
        self.add(r,l,label('Rod: enzymes in between'),label('Rod disc\nmembranes',-4.4,-3.15,28),Line([-3.55,1.5,0],[-1,2.45,0],color=GREY))
        self.at('light activates')
        ph=Dot([-5.7,3,0],radius=.2,color=YELLOW); self.add(ph)
        self.play(ph.animate.move_to([-4.4,1.5,0]),run_time=.45)
        self.at('rhodopsin'); self.play(Indicate(l[0][0],color=YELLOW,scale_factor=1.03),run_time=.4)
        self.at('then transducin'); self.play(Indicate(l[0][1],color=PURPLE),run_time=.4)
        self.at('then pde6'); self.play(Indicate(l[0][2],color=PURPLE),run_time=.4)
        self.finish()


class S06Rod2(SpokenScene):
    def construct(self):
        r=rod(-3.8,0,5.8).stretch_to_fit_width(3.6); enzyme=bchip('PDE6',PURPLE,34).move_to([.3,2,0])
        # Pores interrupt the right membrane; cGMP stays on the cytoplasmic side.
        ps=VGroup(*[channel(-2.1,y,True).rotate(PI/2) for y in (1.6,0,-1.6)])
        masks=VGroup(*[Rectangle(width=.32,height=.9,stroke_width=0,fill_color=BG,fill_opacity=1).move_to(p) for p in ps])
        cg=VGroup(*[bchip('cGMP',PURPLE,32).move_to([-4.15,y,0]) for y in (1.6,0,-1.6)])
        breakdown=arrow(enzyme.get_left(),cg[0].get_right(),PURPLE)
        flows=VGroup(*[arrow([-1,y,0],[-2.55,y,0],GREEN) for y in (1.6,0,-1.6)])
        entry=label('Positive charge enters',2.8,-1.3,32,GREEN)
        state=label('CNG channels open',1.2,.75,32,BLUE)
        pore_label=arrow([-1,.75,0],[-2,.3,0],BLUE)
        self.add(r,masks,ps,enzyme,cg,flows,entry,state,pore_label,breakdown,label('Rod outer segment',0,3.4,34))
        self.at('breaks down'); self.play(Indicate(enzyme),Indicate(breakdown),LaggedStart(*[FadeOut(c) for c in cg],lag_ratio=.2),run_time=.65)
        self.at('channels close')
        self.play(*[p.gate.animate.set_opacity(1) for p in ps],FadeOut(flows),Transform(state,label('Channels close',1.2,.75,34,BLUE)),Transform(entry,label('Less positive\ncharge enters',2.8,-1.3,34,GREEN)),run_time=.5)
        self.at('less positive charge'); self.play(Indicate(entry,scale_factor=1.03),run_time=.3)
        self.at('the rod hyperpolarizes')
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.2)
        mp=mapper(-4.9,1.8,10,3.9,.25,1)
        # negative normalized voltage: plotted down from baseline
        vm=lambda t,v:mp(t,v)
        axes=VGroup(Line(mp(0,0),mp(.25,0),color=GREY),Line(mp(0,0),mp(0,-1.1),color=GREY))
        # mapper's positive height is upward; negative v goes down.
        self.add(label('0',-5.4,1.8,28),label('−1',-5.4,-2.1,28),label('Rod hyperpolarizes — schematic',0,3.1,32,TEAL),axes,label('Membrane voltage\n(relative change)',-3,2.45,28,TEAL),label('Time after photon (ms)',0,-3.2,28))
        for t in [0,.1,.2]:self.add(label(str(int(t*1000)),mp(t,0)[0],-2.7,28),Line(mp(t,-1.13),mp(t,-1.17),color=GREY))
        self.play(Create(trace(lambda t:-response(t),0,.25,vm,TEAL)),run_time=.8)
        self.finish()


class S07Rodslow(SpokenScene):
    def construct(self):
        mp=mapper(-4.9,-2.15,10,4.1,.25,1)
        self.add(label('Mouse rod, near body temperature',0,3.2,32),label('Response (relative) • schematic',-1.8,2.6,28,GREEN),Line(mp(0,0),mp(.25,0),color=GREY),Line(mp(0,0),mp(0,1.05),color=GREY),label('Time after photon (ms)',0,-3.2,28))
        for t in [0,.05,.1,.2]:self.add(Line(mp(t,-.03),mp(t,.03),color=GREY),label(str(int(t*1000)),mp(t,0)[0],-2.65,28))
        self.at('response to a single photon'); self.play(Create(trace(response,0,.25,mp,GREEN)),run_time=1)
        self.at('a tenth of a second');self.play(Create(DashedLine(mp(.1,0),mp(.1,1),color=GREEN)),FadeIn(label('~100 ms or more\nto peak',3.5,1.7,30,GREEN)),run_time=.4)
        self.finish()


class S08Axis(SpokenScene):
    def construct(self):
        self.add(log_plot(),label('One logarithmic time axis',0,3.25,32))
        self.at('more than three orders');self.play(FadeIn(label('More than 3 orders of magnitude',0,-3.25,32,PURPLE)),run_time=.4)
        self.finish()


class S09Caution(SpokenScene):
    def construct(self):
        self.add(log_plot(),label('Different kinds of timing number',0,3.25,32))
        self.at('a channel time constant');self.play(FadeIn(label('Channel time\nconstant',-1.6,.25,28,BLUE)),Create(arrow([-2.8,.4,0],[-3.746,.56,0],BLUE)),run_time=.35)
        self.at('and the other');self.play(FadeIn(label('Whole-cell\ntime to peak',.6,1.15,28,GREEN)),Create(arrow([1.8,1.5,0],[3.12,1.85,0],GREEN)),run_time=.35)
        self.at('read the gap');self.play(FadeIn(label('A picture of scale, not a measured cost',0,-3.25,32)),run_time=.35)
        self.finish()


class S10Predict(SpokenScene):
    def construct(self):
        p=prediction();self.add(p)
        self.at('predict');self.play(Indicate(p[1],color=TEAL),run_time=.4)
        self.finish()


class S11Pause(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(prediction());bar=Line([.1,-3.2,0],[4,-3.2,0],color=TEAL,stroke_width=5);self.play(Create(bar),run_time=5,rate_func=linear)


class S12Reveal(SpokenScene):
    def construct(self):
        l=ladder();ph=Dot([-3.3,3.35,0],radius=.22,color=YELLOW)
        tokens=VGroup(*[bchip('cGMP',PURPLE,32).move_to([x,y,0]) for y in (1.5,.5,-.5) for x in (.6,2.5,4.4)])
        v=ValueTracker(0)
        count=always_redraw(lambda:label(f'{int(v.get_value()):,}',2.5,-1.7,58,PURPLE))
        turnover=arrow(l[0][2].get_right(),[-.35,.5,0],PURPLE)
        self.add(l,ph,tokens,count,turnover,label('Gain',2.5,3.1,38,PURPLE))
        self.at('enzymes keep working');self.play(Indicate(ph,color=YELLOW),Indicate(l[0][2],color=PURPLE),run_time=.7)
        # Repeat turnovers throughout the explanation; chips are representative, not one-to-one.
        self.play(Indicate(l[0][2]),Indicate(turnover),v.animate.set_value(800),LaggedStart(*[FadeOut(t) for t in tokens[:4]],lag_ratio=.2),run_time=1.5)
        self.at('in mouse rods');self.play(FadeIn(label('Mouse rod',2.5,2.35,30)),v.animate.set_value(1200),FadeOut(tokens[4]),Indicate(turnover),run_time=.5)
        self.at('one absorbed photon');self.play(v.animate.set_value(1600),FadeOut(tokens[5:7]),Indicate(l[0][2]),Indicate(turnover),run_time=.6)
        self.at('removes about');self.play(v.animate.set_value(2000),FadeOut(tokens[7:]),Indicate(l[0][2]),Indicate(turnover),run_time=1)
        self.play(FadeIn(label('about 2,000 cGMP per photon',2,-2.6,30,PURPLE)),FadeIn(label('Arshavsky and Burns 2014',2,-3.25,34)),run_time=.3)
        self.finish()


class S13Reveal2(SpokenScene):
    def construct(self):
        gain=bchip('Gain',PURPLE,34).move_to([-3.6,1.7,0]); target=bchip('Single photon\nsignalled',GREEN,36).move_to([3,0,0])
        noise=bchip('Low dark noise',PURPLE,30).move_to([-3.6,0,0]); rep=bchip('Reproducible\nresponse',PURPLE,30).move_to([-3.6,-1.9,0])
        q1=bchip('?',PURPLE,34).move_to([-3.6,0,0]);q2=bchip('?',PURPLE,34).move_to([-3.6,-1.9,0]);self.add(label('Gain is one reason',0,3.15,36),gain,target,arrow(gain.get_right(),target.get_left(),PURPLE),q1,q2)
        self.at('a rod can signal');self.play(Indicate(target,color=GREEN),run_time=.5)
        self.at('low dark noise');self.play(ReplacementTransform(q1,noise),GrowArrow(arrow(noise.get_right(),target.get_left(),PURPLE)),run_time=.4)
        self.at('a reproducible response');self.play(ReplacementTransform(q2,rep),GrowArrow(arrow(rep.get_right(),target.get_left(),PURPLE)),run_time=.4)
        self.finish()


class S14Cost(SpokenScene):
    def construct(self):
        h=bundle(-3.5,-.8,scale=1,rows=2);l=ladder(3,2.05)
        self.add(h,l,Line([0,-3.5,0],[0,3.5,0],color=GREY),label('Hair cell: force on\nthe channel complex',-3.4,3.2,32,BLUE),label('Rod: molecules must meet,\nenzymes must turn over',3.3,3.2,32,PURPLE))
        self.at('no enzyme cascade');self.play(FadeIn(label('One deflection: many channels\nNo enzyme cascade',-3.5,-3.35,32,BLUE)),run_time=.3)
        self.at('force acts');self.play(Transform(h,bundle(-3.5,-.8,.22,1,rows=2)),GrowArrow(Arrow([-6,2.3,0],[-2.1,2.3,0],color=YELLOW,buff=0,stroke_width=5)),run_time=.5)
        self.at('the channel complex itself')
        ions=VGroup(*[arrow(p.get_center()+UP*.6,p.get_center()+DOWN*.55,GREEN) for p in h[3]])
        self.play(*[p.gate.animate.set_opacity(0) for p in h[3]],Create(ions),run_time=.25)
        self.play(*[p.gate.animate.set_opacity(1) for p in h[3]],FadeOut(ions),run_time=.2)
        self.play(*[p.gate.animate.set_opacity(0) for p in h[3]],FadeIn(ions),run_time=.25)
        self.at("the rod's price");self.play(Indicate(l[1],color=PURPLE),run_time=.4)
        self.at('molecules must meet')
        clocks=[]
        for y in (2.15,0,-2.15):
            face=Circle(radius=.28,color=TEXT).move_to([5.6,y,0]);hand=Line(face.get_center(),face.get_center()+UP*.2,color=TEXT);clocks.append(VGroup(face,hand))
        self.add(clocks[0]);self.play(Rotate(clocks[0][1],TAU,about_point=clocks[0][0].get_center()),Indicate(l[0][0]),run_time=.6)
        self.at('enzymes must turn over')
        for i in (1,2):
            self.add(clocks[i]);self.play(Rotate(clocks[i][1],TAU,about_point=clocks[i][0].get_center()),Indicate(l[0][i]),run_time=.4)
        self.at('before any channel changes');self.play(FadeIn(label('Step times depend on\nthe cell and conditions',3.3,-3.15,32)),run_time=.3)
        self.finish()


class S15Idea(SpokenScene):
    def construct(self):
        self.add(label('What sits between the stimulus and the pore\nsets what a sensory cell can do.',0,2.8,34))
        left=VGroup(bchip('No enzyme',BLUE,34),T('No enzyme cascade\nbefore the current',30),T('Can be fast',34,BLUE)).arrange(DOWN,buff=.7).move_to([-3.3,-.3,0])
        right=VGroup(bchip('Enzymes',PURPLE,34),T('e.g. about 2,000 cGMP\nper photon (mouse rod)',30),T('Usually slower',34,PURPLE)).arrange(DOWN,buff=.7).move_to([3.3,-.3,0])
        self.add(left,right,label('A tendency, not a law',0,-3.2,32,TEAL))
        self.at('the one idea');self.play(Indicate(left[0]),Indicate(right[0]),run_time=.5)
        self.finish()


class S16Q2(SpokenScene):
    def construct(self):
        soma=Ellipse(width=2,height=2.1,color=GREY,fill_opacity=.15).move_to([-1.5,-.5,0])
        dend=Line([-2.4,0,0],[-4.1,1.5,0],color=GREY,stroke_width=9)
        cilia=VGroup(*[Line([-4.1,1.5,0],[-5.5,y,0],color=GREY,stroke_width=5) for y in (.5,1.2,1.9,2.6)])
        axon=Line([-.5,-.5,0],[4.5,-.5,0],color=GREY,stroke_width=9)
        self.add(soma,dend,cilia,axon,label('Q2: how does the signal leave the cell?',0,3.2,32),label('Olfactory neuron',-2,-2,32),bchip('Bulb',GREY,30).move_to([5.2,-.5,0]))
        self.at('an olfactory neuron');self.play(FadeIn(label('Primary sensory neuron',0,-2.8,32,TEAL)),run_time=.3)
        self.at('carries it on');p=Dot([-.5,-.5,0],color=TEAL,radius=.18);self.add(p)
        self.play(p.animate.move_to([4.5,-.5,0]),FadeIn(label('Its own axon',2,.4,30,TEAL)),run_time=.7)
        self.finish()


class S17Secondary(SpokenScene):
    def construct(self):
        h=bundle(-3.35,-.6,scale=.98)
        taste=RoundedRectangle(width=2.94,height=4.7,corner_radius=.5,color=GREY,fill_opacity=.12).move_to([3.2,-.1,0])
        micro=VGroup(*[Line([x,2.25,0],[x,2.8,0],color=TEXT,stroke_width=9) for x in (2.65,3.2,3.75)])
        # Separate paths and arrowheads make ownership visible without crossings.
        hairf=VGroup(Line([-3.35,-2.66,0],[-3.35,-3.1,0],color=TEAL,stroke_width=5),arrow([-3.35,-3.1,0],[-.5,-3.1,0],TEAL))
        tastef=arrow([3.2,-2.5,0],[3.2,-3.55,0],TEAL)
        self.add(h,taste,micro,label('Secondary receptor cells',0,3.4,34,TEAL),label('Hair cell',-3.35,-1.65,32),label('Type II\ntaste cell',3.2,-.1,32))
        self.at('hands it to');self.play(Create(hairf),GrowArrow(tastef),run_time=.35)
        self.at('a separate afferent');self.play(FadeIn(label('Separate afferent fibres',-.1,-3.65,32,TEAL)),run_time=.4)
        self.finish()


class S18Table(SpokenScene):
    def construct(self):
        t=table();self.add(t[1])
        self.at('together the two questions');self.play(LaggedStart(*[Create(b) for b in t[0]],lag_ratio=.12),run_time=.7)
        self.at('five examples fill it');self.play(LaggedStart(*[FadeIn(e) for e in t[2]],lag_ratio=.12),run_time=.7)
        self.finish()


class S19Rods(SpokenScene):
    def construct(self):
        t=table(compact=True);self.add(t[0],t[1],t[2][0],t[2][1])
        self.add(label('Vertebrate\nolfactory neuron',-1.5,-.7,32),label('Type II\ntaste cell',3.9,-.7,32))
        self.at('rods and cones')
        icon=rod(1.1,-.8,2.6).scale(.4)
        self.play(FadeIn(icon),run_time=.25)
        self.at('do not fit neatly')
        self.play(FadeIn(label('Rods / cones: column disputed',1.1,-2.1,34,YELLOW)),FadeIn(label('?',1.8,-.75,54,YELLOW)),run_time=.3)
        self.at('they synapse inside');self.play(FadeIn(label('Synapse inside the retina',0,-2.75,32,TEAL)),run_time=.3)
        self.at('send no axon');self.play(FadeIn(label('No axon to the brain',0,-3.4,32)),run_time=.3)
        self.finish()


class S20Take(SpokenScene):
    def construct(self):
        first=bchip('1. What sits between\nstimulus and pore?',BLUE,38).move_to([0,1,0])
        second=bchip('2. How does the signal\nleave the cell?',TEAL,38).move_to([0,-1.8,0])
        q1=bchip('1. ?',BLUE,48).move_to([0,1,0]);q2=bchip('2. ?',TEAL,48).move_to([0,-1.8,0])
        for c in (first,second,q1,q2):
            for box in c[:2]:box.stretch_to_fit_width(10).stretch_to_fit_height(2.15)
        self.add(label('Ask two questions of every sensory cell',0,3.1,34),q1,q2)
        self.at('what sits between');self.remove(q1[2]);self.play(FadeIn(first[2]),run_time=.3)
        self.at('and how does');self.remove(q2[2]);self.play(FadeIn(second[2]),run_time=.3)
        self.finish()


class S21End(EndCard):
    LINE='Ask two questions of every sensory cell.'
    def construct(self):
        self.add(T(self.LINE,40,font=TITLE_FONT),label('biochemistrypedia.com',0,-1.2,30,TEAL));self.finish()
