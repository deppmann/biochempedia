"""Chapter 5: Turning It Up or Down.

COLOR MAP: YELLOW glutamate; BLUE AMPA; PURPLE NMDA; ORANGE Mg2+;
PINK depolarization; TEAL Ca2+; GREEN LTP/CaMKII/insertion;
RED LTD/phosphatases/removal; TEXT stimulus/APV; GOLD questions/tags;
GREY membrane and baseline. Pale labels use TEXT for readable contrast.

All curves are computed. Calcium: normalized difference of exponentials
(fast rise/decay) or a sigmoid-window plateau (prolonged signal).
Pathway sensitivity: Hill functions with an earlier phosphatase response.
These are ordinal illustrations of the lesson, NOT fitted calcium kinetics,
affinity measurements, or an established calcium threshold. The response
experiment interpolates the lesson's 100 -> 75% example; its extended hold
illustrates the narrative's more-than-one-hour persistence. Receptor bars use
relative response proportional to illustrated receptor count, same stimulus.
"""
import numpy as np
from bp_style import *

PURPLE = '#B58CD9'
ORANGE = '#F29E4C'
PINK = '#E58FC0'


def label(s, x=0, y=3.1, color=TEXT, size=30):
    return T(s, size, color).move_to([x,y,0])


def ampa(x,y,k=1.,tagged=False):
    blocks=VGroup(*[RoundedRectangle(corner_radius=.05*k,width=.20*k,
        height=.58*k,stroke_color=BLUE,stroke_width=3,fill_color=BLUE,
        fill_opacity=.8).move_to([x+s*.15*k,y,0]) for s in (-1,1)])
    if tagged:
        halo=RoundedRectangle(width=.72*k,height=.85*k,corner_radius=.15*k,
            stroke_color=GOLD,stroke_width=7,stroke_opacity=.32).move_to([x,y,0])
        badge=Dot([x,y+.43*k,0],radius=.08*k,color=GOLD)
        return VGroup(blocks,halo,badge)
    return blocks


def spine(n=4,cx=0,width=9.0,height=5.3,top=1.85,k=1.6):
    body=RoundedRectangle(width=width,height=height,corner_radius=1.3,
        stroke_color=GREY,stroke_width=4,fill_color=GREY,fill_opacity=.08
        ).move_to([cx,top-height/2,0])
    mem=Line([cx-width*.43,top,0],[cx+width*.43,top,0],color=GREY,stroke_width=9)
    slots=np.linspace(cx-width*.32,cx+width*.32,4)
    use=slots[[0,3]] if n==2 else slots
    receptors=VGroup(*[ampa(x,top,k) for x in use])
    return VGroup(body,mem),receptors


def axes(x=-5.2,y=-2.35,w=10.6,h=4.8):
    return Axes(x_range=[0,1,1],y_range=[0,1,1],x_length=w,y_length=h,
        tips=False,axis_config={'include_ticks':False,'color':GREY,'stroke_width':3}
        ).move_to([x+w/2,y+h/2,0])


def series(ax,xs,ys,color=TEAL,opacity=1):
    ts=np.linspace(xs[0],xs[-1],300)
    return ax.plot_line_graph(ts,np.interp(ts,xs,ys),add_vertex_dots=False,
        line_color=color,stroke_width=5).set_stroke(opacity=opacity)


def calcium(ax,low=False,fallen=False):
    t=np.linspace(0,1,350)
    if fallen:
        y=np.full_like(t,.035)
    elif low:
        sigmoid=lambda z: 1/(1+np.exp(-z))
        y=.035+.29*(sigmoid((t-.15)/.02)-sigmoid((t-.84)/.025))
    else:
        u=np.maximum(t-.12,0)
        pulse=np.exp(-u/.09)-np.exp(-u/.018)
        y=.035+.89*pulse/max(pulse)
    return ax.plot_line_graph(t,y,add_vertex_dots=False,line_color=TEAL,stroke_width=5)


def ca_stage(low=False,fallen=False):
    ax=axes(-5.15,-2.35,7.35,4.9)
    labs=VGroup(label('spine Ca²⁺',-4.25,3.12,TEAL,30),
        label('time',1.6,-2.85,TEXT,28),label('qualitative model',-2.2,-3.35,TEXT,26))
    kin=chip('CaMKII',GREY if low else GREEN,34,fill_opacity=.15 if low else .4).move_to([4.35,.05,0])
    return ax,calcium(ax,low,fallen),labs,kin


def ticks(cx=0,y=0,n=7,gap=1.3,height=.7):
    return VGroup(*[Line([x,y,0],[x,y+height,0],color=TEXT,stroke_width=4)
        for x in (np.arange(n)-(n-1)/2)*gap+cx])


def experiment(question=False,apv=False):
    ax=axes(-4.65,-2.15,10.1,4.55)
    labs=VGroup(label('response (% of baseline)',-2.8,2.95,TEXT,30),
        label('before',-4.0,-2.62,TEXT,26),label('more than 1 h',4.25,-2.62,TEXT,26),
        label('time',.6,-2.62,TEXT,26))
    for v in (75,100):
        pt=ax.c2p(0,v/125)
        labs.add(label(str(v),-5.22,pt[1],TEXT,26),Line(pt+LEFT*.12,pt+RIGHT*.12,color=GREY))
    pre=series(ax,[0,.22],[.8,.8],GREY)
    drug=chip('APV · NMDA blocker',TEXT,28).move_to([1.3,3.1,0]) if apv else VGroup()
    if apv:
        labs[0].move_to([-3.4,3.1,0]).scale(.87)
    q=label('Does LTD develop?',0,-3.25,GOLD,34) if question else VGroup()
    mark=label('?',1.3,0,GOLD,76) if question else VGroup()
    train=ticks(-2.38,-2.12,5,.18,.36)
    train.add(label('slow train',-2.38,-1.4,TEXT,26))
    return ax,labs,pre,drug,q,mark,train


def bath():
    return Rectangle(width=9.9,height=4.35,stroke_width=0,fill_color=PURPLE,
        fill_opacity=.12).move_to([.4,.12,0])


def pit_at(cx=0,top=1.85,radius=1.45):
    # Shared open invagination, then a pinched-off vesicle in both removal scenes.
    pts=[[cx-radius,top,0]]
    pts += [[cx+radius*np.cos(t),top-radius*np.sin(t),0]
            for t in np.linspace(np.pi,0,70)]
    return VMobject(color=GREY,stroke_width=6).set_points_as_corners(pts)


class S00Title(TitleCard):
    LESSON='Synaptic Plasticity'
    TITLE='Turning It Up or Down'


class S01Question(SpokenScene):
    def construct(self):
        b,r=spine(width=8.1)
        self.add(b,r)
        self.at('turned up')
        self.play(GrowArrow(Arrow([-5.1,-1.8,0],[-5.1,1.7,0],color=GREEN,stroke_width=14)),run_time=.5)
        self.at('turned down')
        self.play(GrowArrow(Arrow([5.1,1.7,0],[5.1,-1.8,0],color=RED,stroke_width=14)),run_time=.5)
        self.at('what decides')
        self.play(FadeIn(label('What decides the direction?',0,3.1,GOLD,36)),run_time=.5)
        self.finish()


class S02Up(SpokenScene):
    def construct(self):
        ax,c,l,k=ca_stage()
        dim=chip('CaMKII',GREY,34,fill_opacity=.12).move_to(k)
        self.add(ax,l,dim)
        self.at('start with up')
        self.play(FadeIn(label('UP',4.35,2.8,GREEN,38)),run_time=.4)
        self.at('the large')
        self.play(Create(c),FadeIn(label('large, fast',-.9,2.45,TEAL,30)),run_time=1.7)
        self.at('recruits a kinase')
        ar=Arrow(ax.c2p(.16,.90),dim.get_left(),color=TEAL,buff=.2,stroke_width=5)
        self.play(GrowArrow(ar),Transform(dim,k),run_time=.9)
        self.finish()


class S03Persist(SpokenScene):
    def construct(self):
        ax,c,l,k=ca_stage()
        self.add(ax,c,l,k,label('UP',4.35,2.8,GREEN,38),label('large, fast',-.9,2.45,TEAL,30))
        self.at('stay active')
        self.play(FadeIn(label('stays active',4.35,-1.0,GREEN,30)),run_time=.4)
        self.at('after calcium falls')
        self.play(Transform(c,calcium(ax,fallen=True)),run_time=1.25)
        self.at('can leave a change')
        self.play(Indicate(k,color=GREEN,scale_factor=1.08),run_time=.7)
        self.finish()


class S04Insert(SpokenScene):
    def construct(self):
        b,r=spine(2,top=1.65,height=4.55)
        slots=np.linspace(-2.88,2.88,4)
        tagged=VGroup(ampa(slots[1],-.9,1.6,True),ampa(slots[2],-1.8,1.6,True))
        card=label('Hayashi, Malinow and colleagues · 2000',0,3.2,TEXT,30)
        self.add(b,r,card,label('tagged receptor',0,-3.35,GOLD,28),tagged)
        self.at('expression includes')
        self.play(tagged[0].animate.set_y(1.65),run_time=2.5)
        self.at('in 2000')
        self.play(tagged[1].animate.set_y(1.65),run_time=2.0)
        self.at('saw')
        self.play(FadeIn(label('saw tagged receptors move into synapses',0,2.55,TEXT,28)),run_time=.5)
        self.at('tagged ampa receptors')
        self.play(Indicate(tagged,color=GOLD,scale_factor=1.06),run_time=.6)
        self.finish()


class S05Bigger(SpokenScene):
    def construct(self):
        b,r=spine(2,cx=-3.55,width=4.25,height=4.7,top=1.7,k=1.25)
        slots=np.linspace(-3.55-4.25*.32,-3.55+4.25*.32,4)
        more=VGroup(ampa(slots[1],1.7,1.25),ampa(slots[2],1.7,1.25))
        ax=axes(.9,-2.6,4.8,4.85)
        # Same-stimulus toy response, R proportional to displayed receptor count.
        def bar(x,n,col):
            height=4.85*(n/4)*.8
            return Rectangle(width=.95,height=height,color=col,fill_opacity=.65).move_to([x,-2.6+height/2,0])
        before=bar(2.05,2,GREY); after=bar(4.45,4,GREEN)
        puff=lambda: VGroup(*[Dot([x,2.65,0],radius=.11,color=YELLOW) for x in [-4.35,-3.55,-2.75]])
        p=puff()
        state=label('before',-3.55,-2.3,TEXT,28)
        self.add(state,b,r,ax,label('EPSP (relative)',3.3,3.05,TEXT,30),
            label('same glutamate',-3.55,3.2,YELLOW,29),label('before',2.05,-3.05,TEXT,27),
            label('after',4.45,-3.05,TEXT,27),label('same stimulus',3.3,-3.55,TEXT,26),p)
        for v in (0,1,2):
            pt=ax.c2p(0,v*.4)
            self.add(label(str(v),.48,pt[1],TEXT,26),Line(pt+LEFT*.1,pt+RIGHT*.1,color=GREY))
        self.at('more ampa receptors')
        self.play(p.animate.shift(DOWN*.65),GrowFromEdge(before,DOWN),run_time=.7)
        self.at('mean')
        self.play(FadeIn(more),FadeOut(p),Transform(state,label('after',-3.55,-2.3,TEXT,28)),run_time=.45)
        self.at('a bigger response')
        p=puff(); self.add(p)
        self.play(p.animate.shift(DOWN*.65),GrowFromEdge(after,DOWN),run_time=.8)
        self.finish()


class S06Protein(SpokenScene):
    def construct(self):
        b,r=spine(4,top=1.65,height=4.7)
        self.add(b,r,label('UP = long-term potentiation (LTP)',0,3.2,GREEN,32))
        # Unequal, rounded subunits clasp a short mRNA strand (schematic only).
        large=VMobject(color=PURPLE,fill_color=PURPLE,fill_opacity=.85,stroke_width=3)
        large.set_points_smoothly([[-3.05,-.95,0],[-3.0,-.25,0],[-2.45,.15,0],
            [-1.65,.22,0],[-.95,-.18,0],[-.8,-.85,0],[-1.3,-1.05,0],
            [-1.85,-.88,0],[-2.4,-1.05,0],[-3.05,-.95,0]]).close_path()
        small=VMobject(color=PURPLE,fill_color=PURPLE,fill_opacity=.6,stroke_width=3)
        small.set_points_smoothly([[-2.85,-1.25,0],[-2.3,-1.12,0],[-1.65,-1.18,0],
            [-1.1,-1.25,0],[-1.3,-1.72,0],[-2.05,-1.85,0],
            [-2.7,-1.65,0],[-2.85,-1.25,0]]).close_path()
        mrna=VMobject(color=GOLD,stroke_width=5).set_points_smoothly(
            [[-3.65,-1.28,0],[-3.2,-1.12,0],[-2.6,-1.12,0],
             [-1.6,-1.12,0],[-.9,-1.12,0],[-.45,-1.28,0]])
        rib=VGroup(large,small,mrna,label('mRNA',-3.45,-1.8,GOLD,22))
        self.at('lasts many hours')
        self.play(FadeIn(label('lasting hours, new proteins',0,2.55,TEXT,28)),run_time=.5)
        self.at('often needs')
        self.play(FadeIn(rib),FadeIn(label('ribosome',-1.8,-2.25,TEXT,29)),run_time=.6)
        self.at('new protein synthesis')
        protein=chip('new protein',TEXT,30).move_to([2.1,-.9,0])
        self.play(GrowArrow(Arrow([-.45,-.9,0],[.7,-.9,0],color=TEXT)),FadeIn(protein),run_time=.6)
        self.finish()


class S07Down(SpokenScene):
    def construct(self):
        self.add(label('DOWN · Dudek and Bear · 1992',0,3.2,TEXT,34),
            label('900 pulses',-2.6,2.3,TEXT,34),label('1–3 per second (Hz)',2.35,2.3,TEXT,32),
            label('long, slow train · time →',0,-3.45,TEXT,30))
        base=Line([-5.6,-2.15,0],[5.6,-2.15,0],color=GREY,stroke_width=4)
        tr=ticks(0,-2.15,19,.6,3.85)
        # Axis break means the widely separated example pulses span a long train.
        gap=VGroup(Line([-.35,-2.35,0],[-.15,-1.95,0],color=GOLD,stroke_width=6),
            Line([-.05,-2.35,0],[.15,-1.95,0],color=GOLD,stroke_width=6))
        counter=ValueTracker(0)
        number=T('0',36,TEXT).move_to([0,-2.85,0])
        number.add_updater(lambda m:m.become(T(str(round(counter.get_value())),36,TEXT).move_to([0,-2.85,0])))
        self.add(base,gap,number,label('/ 900',1.45,-2.85,TEXT,30))
        self.at('now')
        self.play(LaggedStart(*[Create(t) for t in tr[:7]],lag_ratio=.22),counter.animate.set_value(300),run_time=3)
        self.at('the same input')
        self.play(LaggedStart(*[Create(t) for t in tr[7:13]],lag_ratio=.3),counter.animate.set_value(600),run_time=2.6)
        self.at('it was')
        self.play(LaggedStart(*[Create(t) for t in tr[13:]],lag_ratio=.3),counter.animate.set_value(900),run_time=2.2)
        number.clear_updaters()
        self.finish()


class S08Ltd(SpokenScene):
    def construct(self):
        ax,l,p,_,_,_,tr=experiment()
        self.add(ax,l,p,tr)
        down=series(ax,[.22,.26,1],[.8,.6,.6],RED)
        other=series(ax,[.22,1],[.8,.8],TEXT)
        self.at('the response fell')
        self.play(Create(down),FadeIn(label('conditioned input',3.3,-.35,RED,28)),run_time=1.3)
        self.at('stayed down')
        self.play(Create(other),FadeIn(label('other input',3.3,1.95,TEXT,28)),run_time=.7)
        self.at('this is')
        self.play(FadeIn(label('long-term depression (LTD)',0,-3.3,RED,32)),run_time=.6)
        self.finish()


class S09Predict(SpokenScene):
    def construct(self):
        ax,l,p,d,q,m,tr=experiment(True,True)
        self.add(ax,l,p)
        self.at('now repeat')
        self.play(LaggedStart(*[Create(t) for t in tr[:5]],lag_ratio=.15),FadeIn(tr[5]),run_time=.7)
        self.at('blocker')
        wash=bath()
        drop=Dot([5.1,3.0,0],radius=.18,color=PURPLE)
        self.play(FadeIn(d,shift=RIGHT*1.4),FadeIn(drop),run_time=.4)
        self.play(drop.animate.shift(DOWN*1.65),FadeIn(wash,shift=LEFT*1.2),run_time=.65)
        self.remove(drop)
        self.at('does ltd develop')
        self.play(FadeIn(q),FadeIn(m),run_time=.5)
        self.finish()


class S10Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(*experiment(True,True),bath())
        self.wait(5)


class S11Reveal(SpokenScene):
    def construct(self):
        ax,l,p,d,q,m,tr=experiment(True,True)
        self.add(ax,l,p,d,q,m,tr,bath())
        self.at('now')  # Transcript token for spoken "No".
        flat=series(ax,[.22,1],[.8,.8],TEXT)
        self.play(FadeOut(q),FadeOut(m),Create(flat),run_time=.7)
        self.at('prevented it')
        self.play(FadeIn(label('LTD blocked by APV',0,-3.25,RED,32)),run_time=.5)
        self.at('the same receptor')
        old=Group(*self.mobjects)
        panels=VGroup(label('Same NMDA receptor · APV blocks both',0,3.25,TEXT,32))
        for x,name,col,ys in [(-3.2,'LTP',GREEN,[.38,.38,.86,.86]),(3.2,'LTD',RED,[.72,.72,.25,.25])]:
            a=axes(x-2.25,-2.3,4.5,4.7)
            expected=series(a,[0,.25,.3,1],ys,col,opacity=.6)
            actual=series(a,[0,1],[ys[0],ys[0]],TEXT)
            # Labels occupy clear spaces, with leaders pointing to the exact trace.
            ey=2.13 if name=='LTP' else -.65
            ay=-1.15 if name=='LTP' else .25
            lx=x-.25 if name=='LTP' else x+.55
            panels.add(a,expected,actual,label('synaptic response',x,2.68,TEXT,26),
                label('time',x+1.85,-2.75,TEXT,26),label(name+' blocked',x,-3.35,col,30),
                label('without APV',lx,ey,col,27),label('with APV',lx,ay,TEXT,27))
            panels.add(Line([lx,ey-.22,0],a.c2p(.85,ys[-1]),color=col,stroke_width=2),
                Line([lx,ay+.22,0],a.c2p(.85,ys[0]),color=TEXT,stroke_width=2))
        self.play(FadeOut(old),FadeIn(panels),run_time=.7)
        self.finish()


class S12Model(SpokenScene):
    def construct(self):
        # A large physical slider: one calcium wire, two attributes of its signal.
        rail=RoundedRectangle(width=7.2,height=4.1,corner_radius=.45,
            color=GREY,fill_color=GREY,fill_opacity=.14).move_to([1,0,0])
        track=Line([-1.75,0,0],[3.75,0,0],color=GREY,stroke_width=13)
        knob=RoundedRectangle(width=.85,height=3.45,corner_radius=.2,
            color=TEXT,fill_color=BG,fill_opacity=1).move_to([-1.75,0,0])
        wire=Line([-5.6,0,0],[-2.6,0,0],color=TEAL,stroke_width=8)
        self.add(rail,track,knob,wire,label('Ca²⁺',-4.7,1.05,TEAL,36),
            label('amount',-4.35,-.85,TEAL,30),label('+ time course',-4.35,-1.5,TEAL,28),
            label('What decides the direction?',0,3.15,GOLD,36),
            label('DOWN',-1.75,-2.55,RED,34),label('UP',3.75,-2.55,GREEN,34))
        self.at('in the standard model')
        self.play(FadeIn(label('standard model',1,-3.15,TEXT,30)),knob.animate.set_x(1),run_time=1.1)
        self.at('how much calcium')
        self.play(knob.animate.set_x(-1.75),run_time=.7)
        self.at('and how fast')
        self.play(knob.animate.set_x(3.75),run_time=1.0)
        self.finish()


class S13Phos(SpokenScene):
    def construct(self):
        ax,c,l,k=ca_stage(True)
        ghost=calcium(ax).set_stroke(color=TEAL,opacity=.24)
        self.add(ax,l,ghost,label('large, fast',-.4,2.5,TEXT,28))
        self.at('a modest',lead=0)
        self.play(Create(c,rate_func=linear),
            FadeIn(label('modest, prolonged',-1.25,.3,TEAL,28)),run_time=2.35)
        ph=chip('phosphatases',RED,32,fill_opacity=.4).move_to([4.3,1.2,0])
        self.at('recruits protein phosphatases')
        ar=Arrow(ax.c2p(.75,.32),ph.get_left(),color=TEAL,buff=.2,stroke_width=5)
        self.play(GrowArrow(ar),FadeIn(ph),run_time=.8)
        self.at('rather than')
        k.move_to([4.3,-1.1,0])
        self.play(FadeIn(k),run_time=.5)
        self.finish()


class S14Reason(SpokenScene):
    def construct(self):
        ax=axes(-5.35,-2.35,10.9,4.95)
        self.add(ax,label('pathway response',-3.65,3.15,TEXT,30),
            label('Ca²⁺ / calmodulin signal →',0,-2.95,TEAL,30),
            label('qualitative model · no numerical thresholds',0,-3.5,TEXT,26))
        t=np.linspace(0,1,350)
        hill=lambda x,K,n: x**n/(K**n+x**n)
        # Different illustrative maxima keep the two responses visibly distinct.
        ph_response=lambda x: .88*hill(x,.20,3)
        ph=ax.plot_line_graph(t,ph_response(t),add_vertex_dots=False,line_color=RED,stroke_width=5)
        kin=ax.plot_line_graph(t,hill(t,.62,7),add_vertex_dots=False,line_color=GREEN,stroke_width=5)
        self.at("the model's")
        self.play(Create(ph),FadeIn(label('phosphatases',-3.65,2.16,RED,30)),
            Create(Line([-3.65,1.88,0],ax.c2p(.23,ph_response(.23)),color=RED,stroke_width=2)),run_time=1.3)
        self.at('than')
        self.play(Create(kin),FadeIn(label('CaMKII',3.75,-.9,GREEN,30)),
            Create(Line([3.75,-.62,0],ax.c2p(.72,hill(.72,.62,7)),color=GREEN,stroke_width=2)),
            FadeIn(label('CaMKII needs more',2.9,3.15,GREEN,28)),run_time=1.1)
        self.finish()


class S15Tip(SpokenScene):
    def construct(self):
        top=2.35; cx=3.5
        b,r=spine(4,cx=cx,width=4.6,height=5.85,top=top,k=1.6)
        ca_ax=axes(-5.5,-3.0,4.45,5.7)
        trace=calcium(ca_ax,True)
        small=label('small, long Ca²⁺ signal',1.1,3.4,TEAL,34)
        self.add(b,r,ca_ax,trace,small,label('spine Ca²⁺',-4.6,3.12,TEAL,28),label('time',-1.5,-3.4,TEXT,28))
        pit=pit_at(cx,top,1.33)
        split=VGroup(Line([cx-1.98,top,0],[cx-1.33,top,0],color=GREY,stroke_width=9),
            Line([cx+1.33,top,0],[cx+1.98,top,0],color=GREY,stroke_width=9))
        self.at('a small')
        # Begin the slow invagination during "small, long"; detached by "removing".
        self.play(Transform(b[1],split),Create(pit),r[1].animate.move_to([cx-.48,top-1.33,0]),
            r[2].animate.move_to([cx+.48,top-1.33,0]),run_time=.9)
        ves=Circle(radius=1.12,color=GREY,stroke_width=5).move_to([cx,-1.0,0])
        self.play(Transform(pit,ves),r[1].animate.move_to([cx-.48,-1.0,0]),
            r[2].animate.move_to([cx+.48,-1.0,0]),run_time=.7)
        self.play(Transform(b[1],Line([cx-1.98,top,0],[cx+1.98,top,0],color=GREY,stroke_width=9)),run_time=.1)
        self.at('removing receptors')
        self.at('a large')
        self.play(FadeOut(small),FadeOut(trace),FadeOut(pit),FadeOut(r[1]),FadeOut(r[2]),run_time=.15)
        large=label('large, fast Ca²⁺ signal',1.1,3.4,TEAL,34)
        trace=calcium(ca_ax)
        self.play(FadeIn(large),Create(trace),run_time=.85)
        self.at('inserting them')
        targets=np.linspace(cx-4.6*.32,cx+4.6*.32,4)
        incoming=VGroup(ampa(targets[1],-1.0,1.6),ampa(targets[2],-1.0,1.6))
        self.add(incoming)
        self.play(*[receptor.animate.set_y(top) for receptor in incoming],run_time=1.1)
        self.wait(.8)
        self.finish()


class S16Mulkey(SpokenScene):
    def construct(self):
        ph=chip('phosphatases',RED,36,fill_opacity=.3).move_to([-3.5,-1.3,0])
        out=chip('LTD induction',RED,36).move_to([3.5,-1.3,0])
        ar=Arrow(ph.get_right(),out.get_left(),color=RED,buff=.18,stroke_width=6)
        self.add(ph,ar,out,label('Mulkey, Herron and Malenka · 1993',0,3.15,TEXT,32),
            label('rat CA1',0,2.5,TEXT,30))
        drugs=VGroup(label('inhibitor',0,1.45,TEXT,34),
            label('okadaic acid · calyculin A',0,.75,TEXT,29),
            label('or microcystin LR',0,.15,TEXT,29))
        box=SurroundingRectangle(drugs,buff=.24,color=TEXT,corner_radius=.15)
        self.add(drugs,box)
        self.at('phosphatase inhibitors')
        self.play(Indicate(box,color=TEXT,scale_factor=1.03),run_time=.7)
        self.at('blocked')
        stem=DashedLine([0,-.3,0],[0,-1.3,0],color=TEXT,stroke_width=5)
        block=DashedLine([-.5,-1.3,0],[.5,-1.3,0],color=TEXT,stroke_width=8)
        self.play(Create(stem),Create(block),ar.animate.set_opacity(.3),
            FadeIn(label('blocked or reduced',0,-2.8,TEXT,34)),run_time=.7)
        self.finish()


class S17Endo(SpokenScene):
    def construct(self):
        b,r=spine(4,top=1.65,height=4.9)
        self.add(b,r,label('LTD',0,3.15,RED,38))
        self.at('removing ampa receptors')
        pit=pit_at(0,1.65,1.45)
        split=VGroup(Line([-3.87,1.65,0],[-1.45,1.65,0],color=GREY,stroke_width=9),
            Line([1.45,1.65,0],[3.87,1.65,0],color=GREY,stroke_width=9))
        self.play(Create(pit),Transform(b[1],split),r[1].animate.move_to([-.55,.2,0]),
            r[2].animate.move_to([.55,.2,0]),run_time=1.6)
        self.at('by endocytosis')
        ves=Circle(radius=1.15,color=GREY,stroke_width=6).move_to([0,-1.1,0])
        self.play(Transform(pit,ves),r[1].animate.move_to([-.55,-1.1,0]),
            r[2].animate.move_to([.55,-1.1,0]),run_time=1.1)
        self.play(Transform(b[1],Line([-3.87,1.65,0],[3.87,1.65,0],color=GREY,stroke_width=9)),run_time=.2)
        self.finish()


class S18Hedge(SpokenScene):
    def construct(self):
        ax=Arrow([-5.5,-.3,0],[5.5,-.3,0],color=TEAL,buff=0,stroke_width=7)
        band=VGroup(*[DashedLine([x,-1.4,0],[x,2.3,0],color=GOLD,dash_length=.16)
            .set_opacity(.15+.38*(1-abs(x)/1.1)) for x in np.linspace(-1,1,15)])
        self.add(ax,label('Ca²⁺: how much, and how fast →',0,-2.1,TEAL,32),
            label('LTD',-4.3,1.4,RED,40),label('LTP',4.3,1.4,GREEN,40),label('a model',0,3.2,TEXT,36))
        self.at('this calcium rule')
        self.play(Indicate(ax,color=TEAL,scale_factor=1.02),run_time=.65)
        self.at('no single calcium threshold')
        self.play(FadeIn(band),FadeIn(label('no single threshold established',0,-2.85,GOLD,32)),run_time=.7)
        self.play(band.animate.shift(LEFT*.55),run_time=1.7,rate_func=smooth)
        self.play(band.animate.shift(RIGHT*1.0),run_time=1.7,rate_func=smooth)
        self.at('whether ltd needs')
        old=Group(*self.mobjects)
        self.play(FadeOut(old),FadeIn(label('Does LTD need ion flow?',0,1.7,TEXT,42)),run_time=.6)
        receptor=chip('NMDA receptor',PURPLE,36).move_to([0,0,0])
        arrow=Arrow([0,-.5,0],[0,-1.85,0],color=TEAL,stroke_width=8)
        self.play(FadeIn(receptor),GrowArrow(arrow),FadeIn(label('Ca²⁺ ?',1.4,-1.2,TEAL,34)),run_time=.65)
        self.at('still debated')
        self.play(FadeIn(label('Debated.',0,-2.8,GOLD,42)),run_time=.5)
        self.finish()


class S19Takeaway(SpokenScene):
    def construct(self):
        self.add(label('standard model',0,3.5,TEXT,32))
        left=axes(-5.5,-2.1,4.7,5.15); right=axes(.8,-2.1,4.7,5.15)
        self.add(left,right,calcium(left),calcium(right,True),
            label('spine Ca²⁺',-4.35,3.4,TEAL,27),label('spine Ca²⁺',3.9,3.4,TEAL,27),
            label('time',-1.2,-2.3,TEXT,26),label('time',5.1,-2.3,TEXT,26),
            label('large, fast',-3.0,1.9,TEAL,29),label('modest, prolonged',3.15,.5,TEAL,28))
        self.at('a synapse turns up or down')
        for x,name,col in [(-3.2,'UP',GREEN),(3.2,'DOWN',RED)]:
            self.play(GrowArrow(Arrow([x,-2.35,0],[x,-2.85,0],color=col,buff=0,stroke_width=5)),
                FadeIn(label(name,x,-3.15,col,36)),FadeIn(label('(a model)',x,-3.65,TEXT,26)),run_time=.38)
        self.at('how much calcium')
        self.play(Indicate(left,color=TEAL,scale_factor=1.02),run_time=.5)
        self.at('and how fast')
        self.play(Indicate(right,color=TEAL,scale_factor=1.02),run_time=.5)
        self.finish()


class S20End(EndCard):
    LINE="In the standard model, calcium’s amount and timing set the direction."

    def construct(self):
        # Two lines keep the full takeaway readable without shrinking the font.
        line=VGroup(T('In the standard model,',38,font=TITLE_FONT),
            T('calcium’s amount and timing set the direction.',38,font=TITLE_FONT)).arrange(DOWN,buff=.25)
        sub=T('biochemistrypedia.com',26,TEAL).next_to(line,DOWN,buff=.6)
        self.play(FadeIn(line),run_time=.6)
        self.play(FadeIn(sub),run_time=.35)
        self.finish()
