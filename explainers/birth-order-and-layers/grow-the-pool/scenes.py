"""Grow the Pool, Then Spend It — chapter 5.
COLOR MAP: PURPLE progenitors; neutral TEXT neuron counts; ORANGE earlier/deeper;
BLUE later/upper; YELLOW emphasis; TEAL interactive; GREY anatomy; RED prediction.
All traces use the lesson's two-outcome recurrence and simulator rising preset.
"""
import numpy as np
from bp_style import *
ORANGE, PURPLE, PINK = '#F29E4C', '#B58CD9', '#E58FB4'
QS=np.array([.1,.15,.2,.25,.3,.35,.4,.5,.65,.8,.8])
LESSON='Birth Order and Fate: Temporal Identity and the Inside-Out Cortex'

def model(qs=QS,start=1):
    pool,out=[],[]
    for q in qs:
        out.append(2*q*start);start=2*(1-q)*start;pool.append(start)
    return np.array(pool),np.array(out)

def nd(color,x,y,r=.18):
    return Circle(radius=r,color=color,fill_color=color,fill_opacity=.9).move_to([x,y,0])
def arr(a,b,color=GREY):
    return Arrow(a,b,buff=.12,color=color,stroke_width=3,tip_length=.18)
def heading(s):return T(s,32).move_to([0,3.32,0])
def card(s,y=3.36,color=TEXT,size=30):
    return chip(s,color,size,fill_opacity=.08).move_to([0,y,0])
def dots(n,color=PURPLE,x=-3,y=-1.55):
    cols=20;rows=int(np.ceil(n/cols))
    return VGroup(*[nd(color,x+(i%cols-9.5)*.205,y+(i//cols-(rows-1)/2)*.205,.073) for i in range(n)])
def poolbox(n):
    # Fixed density: box area and exact cell count both grow with the pool.
    h=.35+np.ceil(n/20)*.205
    box=RoundedRectangle(width=4.35,height=h,corner_radius=.12,color=PURPLE,fill_color=PURPLE,fill_opacity=.08).move_to([-3,-1.55,0])
    return VGroup(box,dots(n),T(f'{n} progenitors',28,PURPLE).move_to([-3,-3.05,0]))
def table(rows=0):
    xs=[-5.55,-4.15,-2.5,-.15,2.25,4.85]
    heads=['cycle','Q','progenitors\nat start','daughters','progenitors\nafter','neurons\nmade']
    g=VGroup(*[T(t,26,GREY).move_to([x,2.85,0]) for x,t in zip(xs,heads)])
    g.add(Line([-6.25,2.26,0],[6.25,2.26,0],color=GREY))
    vals=[];p=100
    for i,q in enumerate([.3,.5,.7]):
        a=round(2*(1-q)*p);o=round(2*q*p)
        vals.append(VGroup(*[M(str(v),28,PURPLE if j==4 else TEXT).move_to([x,1.85-i*.65,0]) for j,(x,v) in enumerate(zip(xs,[i+1,q,p,2*p,a,o]))]));p=a
    for r in vals[:rows]:g.add(r)
    return g,vals

def chart(qs=QS,lines=False,end=11,qrow=False):
    pool,out=model(qs)
    ax=Axes(x_range=[0,12,1],y_range=[0,24,5],x_length=11.4,y_length=4.25,tips=False,axis_config={'color':GREY,'include_ticks':False}).move_to([.15,.05,0])
    labels=VGroup(*[M(str(i),26).move_to(ax.c2p(i,0)+DOWN*.32) for i in range(1,12)])
    for v in [0,5,10,15,20]:
        labels.add(M(str(v),26,GREY).move_to(ax.c2p(0,v)+LEFT*.37),Line(ax.c2p(0,v),ax.c2p(12,v),color=GREY,stroke_width=.5,stroke_opacity=.25))
    labels.add(T('cycle',26,GREY).move_to([-6.05,-2.4,0]))
    legend=VGroup(T('pool after cycle',28,PURPLE).move_to([-3.8,2.6,0]),T('neurons made',28).move_to([.2,2.6,0]),T('starting pool = 1',26,GREY).move_to([4.1,2.6,0]))
    if lines:
        a=VMobject(color=PURPLE,stroke_width=5).set_points_as_corners([ax.c2p(i+1,v) for i,v in enumerate(pool[:end])])
        b=VMobject(color=TEXT,stroke_width=5).set_points_as_corners([ax.c2p(i+1,v) for i,v in enumerate(out[:end])])
    else:
        a=VGroup(*[Rectangle(width=.31,height=max(.005,v/24*4.25),stroke_width=0,fill_color=PURPLE,fill_opacity=.9).move_to(ax.c2p(i+1-.19,v/2)) for i,v in enumerate(pool[:end])])
        b=VGroup(*[Rectangle(width=.31,height=max(.005,v/24*4.25),stroke_width=0,fill_color=TEXT,fill_opacity=.9).move_to(ax.c2p(i+1+.19,v/2)) for i,v in enumerate(out[:end])])
    qr=VGroup()
    if qrow:
        qr.add(T('Q',26).move_to([-6.05,-2.98,0]))
        qr.add(*[M(f'{q:.2f}',22,YELLOW if i==8 else TEXT).move_to(ax.c2p(i+1,0)+DOWN*.9) for i,q in enumerate(qs)])
    return VGroup(ax,labels,legend,a,b,qr),ax

def cyclemark(ax):
    return VGroup(DashedLine(ax.c2p(8,0),ax.c2p(8,17.5),color=YELLOW),T('cycle 8: Q = 0.5 · pool stops growing',28,YELLOW).move_to([0,-3.5,0]))
def peak(ax,cycle=9,qs=QS,lines=False):
    pt=ax.c2p(cycle+(0 if lines else .19),model(qs)[1][cycle-1])
    lab=T(f'peak: cycle {cycle}',28,YELLOW).move_to([2.8,2.08,0])
    return VGroup(lab,arr(lab.get_bottom(),pt,YELLOW),nd(YELLOW,*pt[:2],.07))
def prediction():
    g,ax=chart(end=8)
    return VGroup(g,cyclemark(ax),card('Predict: is output highest at cycle 8?'))
def qplot(end=11,days=False):
    ax=Axes(x_range=[1,11,1],y_range=[0,1,.5],x_length=10.5,y_length=4.5,tips=False,axis_config={'color':GREY,'include_ticks':False}).move_to([.35,.15,0])
    ticks=VGroup(*[M(str(i),26).move_to(ax.c2p(i,0)+DOWN*.3) for i in range(1,12)])
    for v in [0,.5,1]:ticks.add(M(str(v),26,GREY).move_to(ax.c2p(1,v)+LEFT*.45))
    ticks.add(T('Q',30).move_to([-5.95,2.45,0]),T('cycle',26,GREY).move_to([-5.95,-2.4,0]))
    if days:
        # Interior day positions are an illustrative axis guide, not fitted timing data.
        for d,c in zip(range(11,18),[1,3.5,5.8,8,9,10,11]):
            ticks.add(T(f'E{d}',26,GREY).move_to(ax.c2p(c,0)+DOWN*.88))
    threshold=DashedLine(ax.c2p(1,.5),ax.c2p(11,.5),color=YELLOW)
    curve=VMobject(color=TEXT,stroke_width=5).set_points_as_corners([ax.c2p(i+1,QS[i]) for i in range(end)])
    note=T('Illustrative guide, including day spacing; not the published fitted curve.',26).move_to([0,-3.5,0]) if days else T('Illustrative Q sketch; not the published fitted curve.',26,GREY).move_to([0,-3.5,0])
    return VGroup(ax,ticks,threshold,curve,note),ax

def ecall(ax,c,q,label,x,y):
    t=chip(label,YELLOW,28).move_to([x,y,0]);pt=ax.c2p(c,q)
    return VGroup(t,arr(t.get_bottom(),pt,YELLOW),nd(YELLOW,*pt[:2],.08))

def anatomy():
    g=VGroup()
    for y,col,name in [(1.4,GREY,'subventricular zone'),(-.65,PURPLE,'ventricular zone')]:
        box=Rectangle(width=10.8,height=1.7,color=col,fill_color=col,fill_opacity=.12).move_to([0,y,0])
        cells=VGroup(*[nd(col,-4.7+i*.55,y-.35,.13) for i in range(18)])
        g.add(VGroup(box,cells,T(name,30,col if col==PURPLE else TEXT).move_to([0,y+.4,0])))
    g.add(T('ventricle',30).move_to([0,-2.45,0]),Line([-5.4,-1.65,0],[5.4,-1.65,0],color=PURPLE))
    return g

class S00Title(TitleCard):
    LESSON=LESSON
    TITLE='Grow the Pool, Then Spend It'
    def construct(self):
        g=VGroup(T('BIOCHEMISTRYPEDIA',26,TEAL),T('BIRTH ORDER AND FATE',28,GREY),fit(T(self.TITLE,54,font=TITLE_FONT),max_w=11.8),Line(LEFT*1.2,RIGHT*1.2,color=GOLD)).arrange(DOWN,buff=.4)
        self.play(FadeIn(g),run_time=.65);self.finish()

class S01Q(SpokenScene):
    def construct(self):
        p=VGroup(RoundedRectangle(width=4,height=4.5,color=PURPLE,fill_color=PURPLE,fill_opacity=.08).move_to([-3.6,0,0]),VGroup(*[nd(PURPLE,-4.8+i%5*.6,-1.5+i//5*.6,.19) for i in range(30)]),T('progenitor pool',30,PURPLE).move_to([-3.6,2.8,0]))
        self.add(p,arr([-1.3,0,0],[.6,0,0]),T('neurons',32).move_to([3.4,2.8,0]))
        self.at('a few early neurons');early=VGroup(*[nd(ORANGE,1.6+i*.7,1.3,.24) for i in range(3)])
        self.play(FadeIn(early,shift=RIGHT),FadeIn(T('early neurons',28,ORANGE).move_to([3.3,2,0])),run_time=.45)
        self.at('then many later ones');late=VGroup(*[nd(BLUE,1.5+i%6*.7,-1.8+i//6*.65,.24) for i in range(18)])
        self.play(LaggedStart(*[FadeIn(d,shift=RIGHT) for d in late],lag_ratio=.02),FadeIn(T('later neurons',28,BLUE).move_to([3.3,.4,0])),run_time=.65)
        self.at('ones');self.play(FadeIn(T('How does one pool do both?',32).move_to([0,-3.2,0])),run_time=.35);self.finish()

class S02Two(SpokenScene):
    def construct(self):
        a=nd(PURPLE,0,.8,1);lab=T('progenitor',32,PURPLE).move_to([0,2.6,0]);self.add(a,lab)
        self.at('every division gives');b=nd(PURPLE,-3,-.2,1);c=nd(PURPLE,3,-.2,1)
        self.play(ReplacementTransform(a,VGroup(b,c)),Transform(lab,T('one division → two daughters',32).move_to(lab)),run_time=.8)
        self.at('divides again');self.play(FadeIn(T('keeps dividing',32,PURPLE).move_to([-3,-2,0])),Indicate(b),run_time=.5)
        self.at('leaves the cycle');self.play(c.animate.set_color(TEXT),FadeIn(arr([4.1,-.2,0],[5.6,-.2,0],TEXT)),FadeIn(T('becomes a neuron',32).move_to([3,-2,0])),run_time=.5);self.finish()

class S03Pq(SpokenScene):
    def construct(self):
        self.add(heading('10 daughters: count the two outcomes'))
        staying=VGroup(*[nd(PURPLE,-5+i*.9,1.5,.28) for i in range(7)])
        leaving=VGroup(*[nd(TEXT,3+i*.9,1.5,.28) for i in range(3)])
        self.add(staying,leaving)
        self.at('keeps dividing');p=VGroup(T('P',64,PURPLE),T('proliferative fraction',28,PURPLE),M('7 / 10 = 0.7',30,PURPLE)).arrange(DOWN,buff=.22).move_to([-2.6,-.4,0]);self.play(FadeIn(p),run_time=.4)
        self.at('fraction that leaves');q=VGroup(T('Q',64),T('leaving fraction',28),M('3 / 10 = 0.3',30)).arrange(DOWN,buff=.22).move_to([3.8,-.4,0]);eq=M('P + Q = 1',52).move_to([0,-2.65,0]);self.play(FadeIn(q),FadeIn(eq),run_time=.4)
        self.at('Together they make');self.play(eq.animate.set_color(YELLOW),run_time=.3);self.finish()

class S04Rules(SpokenScene):
    def construct(self):
        self.add(heading('Two daughters per progenitor'))
        p=VGroup(nd(PURPLE,-5.3,1,.3),T('progenitors after',32,PURPLE).move_to([-1.5,1.7,0]),M('= 2 × P × progenitors before',32,PURPLE).move_to([.3,.7,0]))
        n=VGroup(nd(TEXT,-5.3,-1.8,.3),T('neurons made',32).move_to([-1.5,-1.1,0]),M('= 2 × Q × progenitors before',32).move_to([.3,-2.1,0]))
        self.add(T('Each daughter stays (P) or leaves (Q).',30).move_to([0,2.5,0]))
        self.at('pool after a cycle');self.play(FadeIn(p),run_time=.4);self.play(Create(Underline(p[2][3],color=PURPLE)),run_time=.2)
        self.at('The neurons');self.play(FadeIn(n),run_time=.4);self.play(Create(Underline(n[2][3],color=TEXT)),run_time=.4);self.finish()

class S05Walk(SpokenScene):
    def construct(self):
        t,_=table();self.add(t,poolbox(100))
        self.at('three cycles');self.play(FadeIn(T('three cycles\n1 → 2 → 3',32).move_to([3,-.7,0])),run_time=.4)
        self.at('with Q rising');self.play(FadeIn(T('Q rises: 0.3 → 0.5 → 0.7',28,YELLOW).move_to([3,-2,0])),run_time=.4)
        self.at('Assume no cells die');self.play(FadeIn(chip('no cell death',TEXT,28).move_to([3,-3,0])),run_time=.4);self.finish()

def worked(scene,row,before,after,out,c1,c2,c3):
    t,rs=table(row-1);p=poolbox(before);scene.add(t,p)
    scene.at(c1);scene.play(FadeIn(rs[row-1][:4]),run_time=.4)
    scene.at(c2);neurons=VGroup(T(f'{out} neurons made',30).move_to([3,-.55,0]),dots(out,TEXT,x=3,y=-2))
    scene.play(FadeIn(rs[row-1][5]),FadeIn(neurons),run_time=.45)
    scene.at(c3);scene.play(Transform(p,poolbox(after)),FadeIn(rs[row-1][4]),run_time=.5)
    scene.at('The pool' if row<3 else 'so the pool');delta=after-before
    scene.play(FadeIn(T(f'{delta:+d}' if delta else '0 · holds',28,YELLOW).move_to([-3,-3.55,0])),run_time=.3);scene.finish()
class S06Low(SpokenScene):
    def construct(self):worked(self,1,100,140,60,'When Q is','make','and')
class S07Half(SpokenScene):
    def construct(self):worked(self,2,140,140,140,'When Q is','make','of each')
class S08High(SpokenScene):
    def construct(self):worked(self,3,140,84,196,'When Q is','they make','Only')

class S09Tak(SpokenScene):
    def construct(self):
        a=anatomy();a[0][0].set_fill(opacity=.03).set_stroke(opacity=.3);a[0][1].set_opacity(.18);a[0][2].set_opacity(.3);self.add(a,heading('Mouse dorsomedial cortex'))
        pill=chip('ventricular epithelium',PURPLE,28).move_to([3.7,-2.42,0]);self.add(pill,Line([3.7,-2.05,0],[3.7,-1.7,0],color=PURPLE,stroke_width=3))
        credit=VGroup(*[T(t,30) for t in ['Takahashi','· Nowakowski','· Caviness','· 1996']]).arrange(RIGHT,buff=.15).move_to([0,-3.25,0]);self.add(credit)
        self.at('In');self.play(LaggedStart(*[Indicate(t,color=YELLOW,scale_factor=1.04) for t in [credit[3],credit[0],credit[1],credit[2]]],lag_ratio=.7),run_time=4.6)
        self.at('measured Q');self.play(Circumscribe(a[1],color=PURPLE),run_time=.6);self.finish()
class S10Cross(SpokenScene):
    def construct(self):
        g,ax=qplot(4,True);self.add(g,heading('Leaving fraction in the mouse cortex'))
        self.at('It crossed');h,_=qplot(8,True);self.play(Transform(g,h),run_time=.6)
        self.at('embryonic day');self.play(FadeIn(ecall(ax,8,.5,'E14 · cycle 8 · Q = 0.5',.3,2.65)),run_time=.35);self.finish()
class S11Late(SpokenScene):
    def construct(self):
        g,ax=qplot(8,True);e=ecall(ax,8,.5,'E14 · Q = 0.5',-.9,2.7);self.add(g,e)
        self.at('It rose');h,_=qplot(11,True);self.play(Transform(g,h),run_time=.7)
        self.at('embryonic day');self.play(FadeIn(ecall(ax,10,.8,'E16 · about 0.8',3.6,3.2)),run_time=.4)
        self.at('Their model spanned');self.play(FadeIn(T('eleven cell cycles',30).move_to([-2.5,1.4,0])),run_time=.4);self.finish()
class S12Vz(SpokenScene):
    def construct(self):
        a=anatomy();self.add(a,heading('Two progenitor zones above the ventricle'))
        self.at('ventricular zone');self.play(Circumscribe(a[1],color=PURPLE),FadeIn(T('modelled pool',28,PURPLE).move_to([0,-3.25,0])),run_time=.5)
        self.at('Intermediate progenitors');self.play(ReplacementTransform(a[0][1][8],VGroup(nd(GREY,-.48,.92,.13),nd(GREY,-.15,1.28,.13))),run_time=.5)
        self.at('add divisions');self.play(FadeIn(chip('extra divisions · outside this model',TEXT,28).move_to([0,2.7,0])),run_time=.4);self.finish()
class S13Predict(SpokenScene):
    def construct(self):
        g,ax=chart(end=8);self.add(g)
        self.at('Predict');self.play(FadeIn(card('Predict: is output highest at cycle 8?')),run_time=.3)
        self.at('pool stops growing');self.play(FadeIn(cyclemark(ax)),run_time=.4)
        self.at('Is that when');self.play(Indicate(g[4][7],color=YELLOW),run_time=.5);self.finish()
class S14Pause(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(prediction())
        # Prompt and countdown sit in the empty plot area to the right of cycle 8 (timer from 5 down to 1).
        prompt=chip('Your guess:\nYES or NO?',TEXT,30).move_to([4.95,.8,0]);self.add(prompt)
        v=ValueTracker(1.0)
        digit=always_redraw(lambda:M(str(max(1,int(np.ceil(v.get_value()*5-1e-6)))),80,YELLOW).move_to([4.95,-.45,0]))
        track=Rectangle(width=2.8,height=.2,stroke_color=GREY,stroke_width=2,fill_opacity=0).move_to([4.95,-1.5,0])
        bar=always_redraw(lambda:Rectangle(width=max(.01,2.8*v.get_value()),height=.2,stroke_width=0,fill_color=YELLOW,fill_opacity=.9).move_to([4.95-1.4+max(.01,2.8*v.get_value())/2,-1.5,0]))
        self.add(digit,track,bar)
        self.play(v.animate.set_value(0),run_time=5,rate_func=linear)
class S15Reveal(SpokenScene):
    def construct(self):
        t,rows=table(3);self.add(t)
        # ASR transcribes the opening No as Now; its audio onset is 0.0 s.
        self.add(T('No.',54,YELLOW).move_to([0,-.45,0]))
        self.at('look back at the table');outlines=VGroup(*[SurroundingRectangle(rows[i],color=YELLOW,buff=.14) for i in [1,2]])
        self.play(Create(outlines),run_time=.4)
        self.at('next cycle makes');self.play(FadeIn(M('140 → 196 neurons',36,YELLOW).move_to([2.8,-1.7,0])),run_time=.35)
        self.at('from the same pool');br=Brace(VGroup(rows[1][2],rows[2][2]),LEFT,color=PURPLE)
        self.play(GrowFromCenter(br),GrowArrow(arr([-3.2,-1.4,0],br.get_bottom(),PURPLE)),FadeIn(T('140 at start\nin both cycles',30,PURPLE).move_to([-3.2,-2,0])),FadeIn(T('same starting pool → more output',32).move_to([0,-3.25,0])),run_time=.35);self.finish()
class S16Why(SpokenScene):
    def construct(self):
        g,ax=chart(lines=True,end=8);title=heading('Sketch: Q 0.5 then 0.65');self.add(g,title)
        self.at('the pool shrinks slowly');h,_=chart(lines=True,end=9);self.play(Transform(g,h),run_time=.8)
        self.at('output rises one more cycle');h,_=chart(lines=True);self.play(Transform(g,h),FadeIn(peak(ax,lines=True)),run_time=.6)
        self.at('In general');self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.25)
        self.add(heading('When does output rise?'))
        eq=M('2 × (1 − Q now) × Q next > Q now',32).move_to([0,2.15,0]);self.add(eq)
        self.at('output rises only if');rise=VGroup(T('Worked table: Q 0.5 → 0.7',32,PURPLE),M('2 × 0.5 × 0.7 = 0.7 > 0.5',32),T('rises: 1.4 times as many neurons',30,YELLOW)).arrange(DOWN,buff=.23).move_to([0,.4,0]);self.play(FadeIn(rise),run_time=.4)
        self.at('times the next');self.play(Indicate(eq,scale_factor=1.02),run_time=.5)
        self.at('Later the shrinking pool wins');fall=VGroup(T('Q 0.7 → 0.8',32,PURPLE),M('2 × 0.3 × 0.8 = 0.48 < 0.7',32),T('falls: about 0.69 times as many',30)).arrange(DOWN,buff=.2).move_to([0,-1.7,0]);self.play(FadeIn(fall),run_time=.35)
        self.add(T('At fixed Q = 0.5, pool and output stay flat.',26,GREY).move_to([0,-3.35,0]));self.finish()
class S17Model(SpokenScene):
    def construct(self):
        g,ax=chart(qrow=True);self.add(g,heading('Illustrative sketch; not the published fitted curve'))
        self.at('output peaks');self.play(FadeIn(peak(ax)),g[4][8].animate.set_color(YELLOW),run_time=.4)
        self.at('the one after');self.play(FadeIn(cyclemark(ax)),run_time=.4);self.finish()

def changed():
    q=QS.copy();q[8]=.6;g,ax=chart(q,qrow=True)
    old=chart(qrow=True)[0][4][8].copy().set_fill(opacity=0).set_stroke(TEXT,width=2,opacity=.6)
    newpeak=peak(ax,10,q);newpeak[0].move_to([4.45,2.08,0]);newpeak[1].become(arr(newpeak[0].get_bottom(),ax.c2p(10.19,model(q)[1][9]),YELLOW))
    oldlabel=T('old peak: cycle 9',28,GREY).move_to([.15,2.08,0])
    oldmark=VGroup(oldlabel,arr(oldlabel.get_right(),ax.c2p(9.19,model()[1][8]),GREY))
    return VGroup(g,old,newpeak,heading('Cycle 9 Q: 0.65 → 0.60; new peak at cycle 10'),oldmark)
class S18Most(SpokenScene):
    def construct(self):
        g,ax=chart(qrow=True);self.add(g)
        self.at('About');share=model()[1][7:].sum()/model()[1].sum()
        br=BraceBetweenPoints(ax.c2p(7.65,22),ax.c2p(11.5,22),UP,color=YELLOW)
        title=heading(f'About 70 percent of all output ({share*100:.1f}%)')
        self.play(*[b.animate.set_color(YELLOW) for b in g[4][7:]],GrowFromCenter(br),FadeIn(title),run_time=.45)
        self.at('once Q has reached');qbox=SurroundingRectangle(g[5][8],color=YELLOW,buff=.07,stroke_width=2.5);self.play(g[5][8].animate.set_color(YELLOW),Create(qbox),run_time=.45)
        self.at('The exact peak');new=changed();self.play(Transform(g,new[0]),FadeOut(br),FadeOut(qbox),Transform(title,new[3]),FadeIn(new[1]),FadeIn(new[2]),FadeIn(new[4]),run_time=.65)
        self.at('how Q rises');self.play(Circumscribe(g[5][9],color=YELLOW),run_time=.45);self.finish()
class S19Hold(Scene):
    def construct(self):self.camera.background_color=BG;self.add(changed());self.wait(2.5)
class S20Spend(SpokenScene):
    def construct(self):
        # Continue with a complete chart: no redundant regrowth during the silent hold.
        g,ax=chart();self.add(g,heading('Build the pool, then spend much of it'))
        pool=model()[0];tops=[ax.c2p(i+1-.19,pool[i])+UP*.32 for i in range(11)]
        up=VMobject(color=PURPLE,stroke_width=6).set_points_as_corners(tops[:8]);dn=VMobject(color=YELLOW,stroke_width=6).set_points_as_corners(tops[7:])
        upl=T('builds its pool',28,PURPLE).move_to([-3.6,1.05,0]);dnl=T('spends much of it',28,YELLOW).move_to([.8,1.7,0])
        self.at('first builds');self.play(Create(up),FadeIn(upl),run_time=1.0,rate_func=linear)
        self.at('then spends');self.play(Create(dn),FadeIn(dnl),run_time=.8,rate_func=linear)
        self.at('Neurons spent later');bands=VGroup(T('earlier born · deeper layers',28,ORANGE).move_to([-3,-3.25,0]),T('later born · upper layers',28,BLUE).move_to([3,-3.25,0]),Line([-5,-2.85,0],[-.5,-2.85,0],color=ORANGE,stroke_width=5),Line([.5,-2.85,0],[5.4,-2.85,0],color=BLUE,stroke_width=5))
        self.play(FadeOut(VGroup(up,dn,upl,dnl)),FadeIn(bands),run_time=.45)
        self.at('The sketch stops');lab=T('progenitors still left',28,PURPLE).move_to([4.25,1.9,0]);pt=ax.c2p(10.81,model()[0][-1]);self.play(FadeIn(lab),GrowArrow(arr(lab.get_bottom(),pt,PURPLE)),Circumscribe(g[3][-1],color=PURPLE),run_time=.45)
        self.at('does not model');note=chip('End of neurogenesis is outside this sketch.\nEmptying this pool needs Q = 1; real progenitors also make glia.',TEXT,26).move_to([0,-3.22,0]);self.play(FadeOut(bands),FadeIn(note),run_time=.4);self.finish()
class S21Caveat(SpokenScene):
    def construct(self):
        g,ax=chart();label=heading('Counts, not identities. Not layer sizes.');self.add(g,label)
        self.at('model counts how many');self.play(Indicate(g[4],scale_factor=1.02),run_time=.6)
        self.at('not which identity');self.play(label.animate.set_color(YELLOW),run_time=.5)
        self.at('Do not read');self.play(FadeIn(chip('daughters leaving in each cycle',TEXT,28).move_to([0,-3.25,0])),run_time=.4);self.finish()
class S22Sim(SpokenScene):
    def construct(self):
        g,ax=chart();label=heading('Counts, not identities. Not layer sizes.');self.add(g,label)
        self.at('Try the simulation');self.play(Transform(label,heading('Simulation preview · find the largest output')),run_time=.4)
        self.at('below this film');controls=VGroup(chip('Q rising ✓',TEAL,26),chip('Q = 0.5',TEXT,26),chip('Reset',TEXT,26)).arrange(RIGHT,buff=.4).move_to([0,-3.2,0]);self.play(FadeIn(controls),run_time=.4)
        self.at('Find the cycle');slider=VGroup(T('cycle 9 Q',26).move_to([-3,1.55,0]),Line([-4.3,1,0],[-1.7,1,0],color=TEAL),nd(TEAL,-2.6,1,.14),M('0.65',26).move_to([-3,.5,0]));self.play(FadeIn(slider),run_time=.4);self.finish()
class S23Take(SpokenScene):
    def construct(self):
        g,ax=qplot();self.add(g,heading('The leaving fraction controls pool growth'))
        self.at('below one half');lo=Rectangle(width=10.5,height=2.25,stroke_width=0,fill_color=PURPLE,fill_opacity=.12).move_to(ax.c2p(6,.25));self.add(lo);a=chip('Q < 0.5: pool grows',PURPLE,30).move_to([2,-1.35,0]);self.play(FadeIn(a),run_time=.35)
        self.at('and above it');hi=Rectangle(width=10.5,height=2.25,stroke_width=0,fill_color=YELLOW,fill_opacity=.09).move_to(ax.c2p(6,.75));self.add(hi);b=chip('Q > 0.5: pool shrinks',YELLOW,30).move_to([-1,1.6,0]);self.play(FadeIn(b),run_time=.35)
        self.at('Output can keep rising');h,ax=chart(lines=True);self.play(*[FadeOut(m) for m in list(self.mobjects)],FadeIn(h),FadeIn(heading('Output can peak one cycle later')),FadeIn(cyclemark(ax)),run_time=.4)
        self.at('rising',lead=.1);pk=peak(ax,lines=True);self.play(FadeIn(pk),run_time=.35)
        self.at('a cycle after');br=Brace(Line(ax.c2p(8,0),ax.c2p(9,0)),DOWN,color=YELLOW,buff=.62);bl=T('one cycle later',28,YELLOW).next_to(br,RIGHT,buff=.2)
        self.play(GrowFromCenter(br),FadeIn(bl),run_time=.4);self.finish()
class S24End(EndCard):
    LINE='Output can keep rising a cycle after the pool stops growing.'
