"""Revised chapter 3: signed causal model and explicitly qualitative schematics.
COLOR MAP: GREEN excitation / indirect route; RED inhibition / direct route / brake;
GOLD dopamine / SNc; BLUE neural populations; YELLOW movement / crossing / focus;
GREY anatomy / notes; TEXT statements. Shared with scenes.old.py.
No measured amplitudes, firing rates, recovery times or calcium kinetics are supplied
by the lesson. All traces below are computed from explicit illustrative equations:
a sigmoid interpolates the lesson's categorical observations; an oscillator represents
movement. These are schematic demonstrations, never fitted or experimental data.
"""
from bp_style import *
import numpy as np

EXC, INH, MOD, POP, HI = GREEN, RED, GOLD, BLUE, YELLOW
LOW, MID, HIGH = .07, .30, .66
SIGN = {'stn_gpi': 1, 'gpi_t': -1, 't_c': 1}


def node(text, xy, color=POP, level=MID, w=2.9, h=.95, size=30):
    box=RoundedRectangle(width=w,height=h,corner_radius=.12,
        stroke_color=color,stroke_width=3,fill_color=color,fill_opacity=level).move_to([*xy,0])
    return VGroup(box,T(text,size).move_to(box))


def link(p,q,sign=1,width=6):
    # scenes.old.py: pointed excitation versus a terminal bar for inhibition.
    p,q=np.array(p,float),np.array(q,float)
    u=(q-p)/np.linalg.norm(q-p)
    if sign<0:
        n=np.array([-u[1],u[0],0])
        return VGroup(Line(p,q,color=INH,stroke_width=width),
            Line(q-n*.22,q+n*.22,color=INH,stroke_width=width+2))
    return Arrow(p,q,buff=0,color=EXC,stroke_width=width,max_tip_length_to_length_ratio=.22)


def heading(text):
    return T(text,34,font=TITLE_FONT).move_to([0,3.15,0])


def cross_at(x,y,r=.22):
    return VGroup(Line([x-r,y-r,0],[x+r,y+r,0]),
                  Line([x-r,y+r,0],[x+r,y-r,0])).set_color(INH).set_stroke(width=7)


def foot(lifted=False):
    y=-1.03 if lifted else -1.48
    return Polygon([-1.75,y+.65,0],[-1.3,y+.65,0],[-1.3,y+.22,0],
        [-.65,y+.18,0],[-.5,y,0],[-1.75,y,0],color=INH,
        fill_color=INH,fill_opacity=.65,stroke_width=3)


def column():
    stn=node('STN',(-3.5,2.15),level=HIGH,w=3.2,h=1.1,size=36)
    gpi=node('GPi · brake',(-3.5,0),color=INH,level=HIGH,w=3.2,h=1.1)
    thal=node('Thalamus',(-3.5,-2.35),level=LOW,w=3.2,h=1.1)
    a=link([-3.5,1.58,0],[-3.5,.58,0],SIGN['stn_gpi'])
    b=link([-3.5,-.58,0],[-3.5,-1.75,0],SIGN['gpi_t'])
    plus=chip('+1',EXC,28).move_to([-4.35,1.1,0])
    minus=chip('−1',INH,28).move_to([-4.35,-1.15,0])
    boot=foot()
    pedal=Line([-1.8,-1.58,0],[-.4,-1.58,0],color=GREY,stroke_width=7)
    leader=Line([-1.8,-1.58,0],[-3.28,-1.58,0],color=INH,stroke_width=3)
    return stn,gpi,thal,a,b,plus,minus,VGroup(boot,pedal,leader)


def monkey():
    # Consistent adult primate silhouette, frontal view; no human substitute.
    head=Ellipse(width=1.3,height=1.5).move_to([0,1.95,0])
    ears=VGroup(Ellipse(width=.3,height=.48).move_to([-.76,1.95,0]),
                Ellipse(width=.3,height=.48).move_to([.76,1.95,0]))
    muzzle=Ellipse(width=.72,height=.45).move_to([0,1.55,0])
    brow=Line([-.4,2.12,0],[.4,2.12,0])
    trunk=Ellipse(width=1.55,height=2.3).move_to([0,-.1,0])
    arms=VGroup(VMobject().set_points_as_corners([[-.65,.6,0],[-1,.0,0],[-1.15,-1.65,0],[-.95,-1.85,0]]),
        VMobject().set_points_as_corners([[.65,.6,0],[1,.0,0],[1.15,-1.65,0],[.95,-1.85,0]]))
    legs=VGroup(VMobject().set_points_as_corners([[-.45,-1.05,0],[-.7,-2.05,0],[-.65,-2.85,0],[-1,-2.85,0]]),
        VMobject().set_points_as_corners([[.45,-1.05,0],[.7,-2.05,0],[.65,-2.85,0],[1,-2.85,0]]))
    tail=ArcBetweenPoints([.65,-.75,0],[1.7,-2.2,0],angle=-1.4)
    return VGroup(head,ears,muzzle,brow,trunk,arms,legs,tail).set_color(GREY).set_stroke(width=4)


def animal_panel():
    animal=monkey().shift(LEFT*4.2)
    sides=VGroup(T('R',28,HI).move_to([-5.65,.9,0]),T('L',28,HI).move_to([-2.7,.9,0]))
    tag=T('Parkinsonian monkey',27,GREY).move_to([-4.1,-3.25,0])
    # Enlarged cutaway: label and lesion are inside the brain, linked to the head.
    brain=VGroup(Ellipse(width=2.7,height=3.0).move_to([.55,1.2,0]),
        Ellipse(width=2.7,height=3.0).move_to([3.35,1.2,0])).set_color(GREY).set_stroke(width=3)
    leader=VGroup(Line([-3.5,2.3,0],[-1.1,2.85,0],color=GREY),
        Line([-1.1,2.85,0],[.55,2.55,0],color=GREY),
        Line([-1.1,2.85,0],[3.35,2.55,0],color=GREY))
    labels=VGroup(T('Right brain',26,GREY).move_to([.55,3.05,0]),
                  T('Left brain',26,HI).move_to([3.35,3.05,0]))
    stn=node('Left STN',(3.35,1.85),w=2.15,h=.7,size=26)
    stn[1].shift(LEFT*.24)
    snc=node('SNc',(3.35,.55),MOD,w=1.8,h=.7,size=28)
    lesion=cross_at(4.12,1.85,.23)
    return VGroup(animal,sides,tag,brain,leader,labels),stn,snc,lesion


def lesion_question():
    base,stn,snc,lesion=animal_panel()
    snc.set_opacity(.25)
    q1=T('Which way should movement change?',30).move_to([1.8,-1.45,0])
    q2=T('Which side of the body?',30).move_to([1.8,-2.35,0])
    return base,stn,snc,lesion,q1,q2


def prediction():
    return chip('Prediction: movement improves, on the right side',HI,27).move_to([0,-3.35,0])


def body_loop():
    # The original monkey beside a large frontal brain inset, with a separate stem.
    body=monkey().scale(.92).shift(LEFT*4.5)
    hemis=VGroup(Ellipse(width=3.2,height=4.8).move_to([-.4,.65,0]),
        Ellipse(width=4.4,height=4.8).move_to([3.5,.65,0])).set_color(GREY).set_stroke(width=3)
    stem=RoundedRectangle(width=.65,height=1.05,corner_radius=.15,
        color=GREY,stroke_width=3).move_to([1.25,-2.15,0])
    inset=VGroup(hemis,stem,
        Line([.2,-1.5,0],[.925,-1.7,0],color=GREY),
        Line([2.35,-1.5,0],[1.575,-1.7,0],color=GREY),
        Line([-3.9,2.15,0],[-1.5,2.15,0],color=GREY))
    labels=VGroup(T("Monkey's right",26,GREY).move_to([-.15,3.4,0]),
        T("Monkey's left",26,HI).move_to([3.5,3.4,0]),
        T('R',28,HI).move_to([-5.9,.8,0]),T('L',28,HI).move_to([-3.05,.8,0]))
    ctx=node('Cortex',(3.5,2.2),w=1.95,h=.65,size=26)
    stn=node('STN',(4.3,-.6),w=1.2,h=.65,size=26)
    gpi=node('GPi',(4.5,.65),INH,w=1.4,h=.65,size=26)
    thal=node('Thalamus',(2.45,.65),w=1.8,h=.65,size=26)
    routes=VGroup(link([4.3,-.24,0],[4.5,.29,0]),
        link([3.77,.65,0],[3.38,.65,0],-1),
        link([2.45,1.01,0],[2.9,1.84,0]))
    return body,inset,labels,VGroup(ctx,stn,gpi,thal),routes


def sigmoid(t,centre=0,width=.25):
    return 1/(1+np.exp(-(t-centre)/width))


def curve(fun,start,end,color,steps=240):
    ts=np.linspace(start,end,steps)
    return VMobject(color=color,stroke_width=5).set_points_as_corners([fun(t) for t in ts])


def raster(x,y,n,color=HI):
    # Qualitative density from the signed model; no numeric rate scale.
    return VGroup(*[Line([x+i*.17,y-.16,0],[x+i*.17,y+.16,0],color=color,stroke_width=3)
        for i in range(n)])


class S00Title(TitleCard):
    LESSON='Descending Control and the Basal Ganglia'
    TITLE='The Test: Silence the STN'
    def construct(self):
        g=VGroup(T('BIOCHEMISTRYPEDIA',26,TEAL),T(self.LESSON,28,GREY),
            T(self.TITLE,48,font=TITLE_FONT),Line(LEFT,RIGHT,color=GOLD,stroke_width=4)).arrange(DOWN,buff=.45)
        self.play(FadeIn(g),run_time=.6); self.finish()


class S01Question(SpokenScene):
    def construct(self):
        c=column(); self.add(*c)
        tag=T('Dopamine lost',28,MOD).move_to([-3.5,3.2,0])
        self.at('dopamine loss'); self.play(FadeIn(tag),run_time=.4)
        self.at('overactive')
        self.play(Circumscribe(c[0],color=HI,fade_out=True),c[0][0].animate.set_fill(HI,.65),run_time=.65)
        self.at('what happens')
        q=VGroup(T('What happens',38),T('when you silence',34),T('the STN?',44,HI)).arrange(DOWN,buff=.25).move_to([2.9,.7,0])
        self.play(FadeIn(q),run_time=.45); self.finish()


class S02Monkey(SpokenScene):
    def construct(self):
        base,stn,snc,lesion=animal_panel(); self.add(base,stn,snc)
        self.at('Picture a monkey'); self.play(Indicate(base[0],scale_factor=1.02),run_time=.5)
        self.at('with MPTP')
        toxin=chip('MPTP',HI,28).move_to([.45,-.9,0])
        action=Arrow([1.2,-.6,0],[2.45,.3,0],color=HI,buff=0,stroke_width=5)
        self.play(FadeIn(toxin),Create(action),run_time=.6)
        self.at('kills dopamine neurons'); self.play(snc.animate.set_opacity(.2),run_time=.65)
        self.at('substantia nigra')
        lab=T('Substantia nigra\ndopamine neurons lost',28,MOD).move_to([2.0,-2.25,0])
        self.play(FadeIn(lab),run_time=.4); self.finish()


class S03Q(SpokenScene):
    def construct(self):
        base,stn,snc,lesion,q1,q2=lesion_question(); self.add(base,stn,snc)
        self.at('Now lesion'); self.play(Create(lesion),stn[0].animate.set_fill(opacity=LOW),run_time=.5)
        self.at('Which way'); self.play(FadeIn(q1),run_time=.4)
        self.at('And on which'); self.play(FadeIn(q2),run_time=.4); self.finish()


class S04Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        base,stn,snc,lesion,q1,q2=lesion_question(); stn[0].set_fill(opacity=LOW)
        self.add(base,stn,snc,lesion,q1,q2)
        cue=T('Predict: which way? which side?',27,HI).move_to([1.7,-3.25,0])
        self.add(cue)
        for _ in range(5):
            self.play(lesion.animate.set_color(HI).scale(1.2),run_time=.45)
            self.play(lesion.animate.set_color(INH).scale(1/1.2),run_time=.55)


class S05Sign(SpokenScene):
    def construct(self):
        c=column(); self.add(*c[:3],c[7],heading('Count the sign'))
        self.at('Start with the sign'); self.wait(.2)
        self.at('STN excites'); self.play(Create(c[3]),FadeIn(c[5]),run_time=.5)
        self.at('inhibits the thalamus'); self.play(Create(c[4]),FadeIn(c[6]),run_time=.5)
        self.at('one inhibition')
        eq=VGroup(M('+1 × −1 = −1',36),T('1 inhibition · odd',34,INH),
            T('Opposite direction',32)).arrange(DOWN,buff=.5).move_to([2.8,.4,0])
        self.play(TransformFromCopy(c[5],eq[0]),FadeIn(eq[1:]),run_time=.55); self.finish()


class S06Sign2(SpokenScene):
    def construct(self):
        c=column(); self.add(*c,heading('Count the sign'))
        # Raster density follows the model sign propagation: −STN -> −GPi -> +thalamus.
        ticks=[raster(-1.3,y,n,col) for y,n,col in [(2.15,10,HI),(0,10,INH),(-2.35,2,POP)]]
        self.add(*ticks)
        self.at('activity falls')
        tag=T('STN ↓ · silenced',30,HI).move_to([3.6,2.15,0])
        g=T('GPi ↓',34,INH).move_to([3.6,0,0])
        self.play(FadeOut(ticks[0]),Transform(ticks[1],raster(-1.3,0,3,INH)),
            c[0][0].animate.set_fill(opacity=LOW),c[1][0].animate.set_fill(opacity=LOW),FadeIn(tag),FadeIn(g),run_time=.55)
        self.at('thalamus rises')
        t=T('Thalamus ↑',34,POP).move_to([3.6,-2.35,0])
        self.play(Transform(ticks[2],raster(-1.3,-2.35,9,POP)),c[2][0].animate.set_fill(opacity=HIGH),FadeIn(t),run_time=.55)
        self.at('brake lifts'); self.play(Transform(c[7][0],foot(True)),run_time=.5)
        self.at('toward movement'); self.play(FadeIn(T('Toward movement',30,EXC).move_to([3.6,-3.3,0])),run_time=.3)
        self.finish()


class S07Side(SpokenScene):
    def construct(self):
        body,brain,labels,nodes,routes=body_loop(); self.add(body,brain,labels,nodes)
        self.at('Now the side'); self.wait(.2)
        self.at('In the classic model')
        self.play(FadeIn(T('Classic model',28,GREY).move_to([-.15,.6,0])),run_time=.4)
        self.at('left loop returns')
        self.play(Create(routes),run_time=.5)
        self.play(Indicate(VGroup(nodes,routes),color=HI,scale_factor=1.03),run_time=.8); self.finish()


class S08Side2(SpokenScene):
    def construct(self):
        body,brain,labels,nodes,routes=body_loop(); self.add(body,brain,labels,nodes,routes)
        self.add(T('Classic model',28,GREY).move_to([-.15,.6,0]))
        # Start within cortex, descend between loop boxes, cross in the drawn stem.
        command=VMobject(color=HI,stroke_width=6).set_points_as_corners([
            [3.5,2.2,0],[3.5,1.5,0],[1.25,1.5,0],[1.25,-1.7,0],
            [1.45,-1.85,0],[1.05,-2.45,0],[1.05,-2.8,0]])
        marker=VGroup(Line([1.05,-1.85,0],[1.45,-2.45,0]),
            Line([1.45,-1.85,0],[1.05,-2.45,0])).set_color(HI).set_stroke(width=5)
        note=T('1 crossing\nPyramidal decussation',26,HI,line_spacing=1.3).move_to([4.35,-2.45,0])
        leader=Line([2.2,-2.3,0],[1.62,-2.15,0],color=HI)
        self.at('commands then cross'); self.play(Create(command),run_time=.9)
        self.at('pyramidal decussation'); self.play(Create(marker),Create(leader),FadeIn(note),run_time=.5)
        self.at('right side')
        branches=VGroup(VMobject(color=HI,stroke_width=5).set_points_as_corners([
                [1.05,-2.8,0],[-2.4,-2.8,0],[-2.4,-.25,0],[-5.4,-.25,0]]),
            VMobject(color=HI,stroke_width=5).set_points_as_corners([
                [-2.4,-2.8,0],[-5.1,-2.8,0],[-5.1,-2.62,0]]),
            body[5][0].copy().set_color(HI),body[6][0].copy().set_color(HI))
        self.play(Create(branches),labels[0].animate.set_color(HI),
            FadeIn(prediction()),run_time=.5); self.finish()


class S09Test(SpokenScene):
    def construct(self):
        base,stn,snc,lesion=animal_panel(); snc.set_opacity(.2)
        tag=chip('MPTP',HI,27).move_to([-4.2,-1.25,0]); tag[0].set_fill(BG,1)
        self.add(base,stn,snc,tag)
        self.at('In 1990')
        cite=VGroup(T('Bergman, Wichmann and DeLong',28),T('Science · 1990',28,GREY)).arrange(DOWN,buff=.25).move_to([1.8,-1.8,0])
        self.play(FadeIn(cite),run_time=.5)
        self.at('did this experiment'); self.play(Create(lesion),stn[0].animate.set_fill(opacity=LOW),run_time=.5)
        self.at('treated with MPTP'); self.play(Indicate(tag,scale_factor=1.08),run_time=.5); self.finish()


class S10Result(SpokenScene):
    def construct(self):
        self.add(heading('Schematic: signs improved'))
        axes=VGroup(Line([-5.1,-2.25,0],[5.8,-2.25,0],color=GREY),
            Line([-5.1,-2.25,0],[-5.1,2.5,0],color=GREY))
        ylabel=T('Right arm movement',28).rotate(PI/2).move_to([-5.85,.2,0])
        marker=DashedLine([-.3,-2.2,0],[-.3,2,0],color=HI)
        lesion=T('Left STN lesion',27,HI).move_to([-.3,2.45,0])
        labels=VGroup(T('Before',28,GREY).move_to([-2.8,-2.7,0]),T('After',28,GREY).move_to([2.8,-2.7,0]),
            T('Time',28).move_to([.2,-3.3,0]))
        self.add(axes,ylabel,marker,lesion,labels)
        # Analytic oscillator: low amplitude before; graded partial increase
        # afterwards. Only the direction is constrained by the lesson, no data implied.
        def motion(x):
            t=max(0.,x+.3)
            # Smooth partial recovery across four oscillations (about five x units).
            u=min(1.,t/5.2); ramp=u*u*(3-2*u)
            amp=.18+.48*ramp
            phase=2*PI*.78*(x+4.9)
            return [x,-.15+amp*np.sin(phase),0]
        before=curve(motion,-4.9,-.3,HI); after=curve(motion,-.3,5.6,HI)
        self.add(before)
        self.at('signs improved'); self.play(Create(after),run_time=1)
        self.at('opposite the lesion')
        self.play(FadeIn(T('Right side improved',29,EXC).move_to([3.15,1.65,0])),run_time=.4); self.finish()


class S11Target(SpokenScene):
    def construct(self):
        pred=prediction(); self.add(pred)
        # Retain a substantive anatomical target from the start of the confirmation.
        brain=VGroup(Ellipse(width=4.1,height=5.15).move_to([-2.15,.4,0]),
            Ellipse(width=4.1,height=5.15).move_to([2.15,.4,0])).set_color(GREY)
        stn=VGroup(Ellipse(width=.65,height=.42,color=POP,fill_color=POP,fill_opacity=.2,stroke_width=3).move_to([2.15,.1,0]),
            T('STN',30).move_to([2.15,-.65,0]))
        self.add(T('STN target · schematic',26,GREY).move_to([0,3.6,0]),
            T('Right brain',26,GREY).move_to([-2.15,3.2,0]),
            T('Left brain',26,HI).move_to([2.15,3.2,0]))
        target=VGroup(brain,stn)
        self.add(target)
        self.at('prediction held')
        check=VGroup(Line([5.15,-3.3,0],[5.4,-3.55,0]),Line([5.4,-3.55,0],[5.95,-3.1,0])).set_color(EXC).set_stroke(width=7)
        self.play(Create(check),run_time=.5)
        self.at('This work helped'); self.wait(.2)
        self.at('a target')
        rings=VGroup(Circle(.43,color=HI),Circle(.62,color=HI)).move_to([2.15,.15,0])
        self.play(Create(rings),run_time=.5)
        self.at('deep brain stimulation')
        electrode=VGroup(RoundedRectangle(width=.26,height=2.7,corner_radius=.05,color=GREY,fill_color=GREY,fill_opacity=.85),
            Rectangle(width=.32,height=.38,color=HI,fill_color=HI,fill_opacity=1).shift(DOWN*1.3)).move_to([2.15,1.55,0])
        label=T('Deep brain\nstimulation',29).move_to([5.2,1.9,0])
        leader=Line([4.02,1.9,0],[2.37,1.9,0],color=GREY)
        self.play(FadeIn(electrode,shift=DOWN*.6),FadeIn(label),Create(leader),
            FadeOut(pred),FadeOut(check),run_time=.55); self.finish()


class S12Limit(SpokenScene):
    def construct(self):
        self.add(heading('A limit of the count'))
        panels=VGroup(); traces=[]
        for x,name,col,shift,width in [(-3.05,'Direct',INH,-.12,.20),(3.05,'Indirect',EXC,.12,.29)]:
            axes=VGroup(Line([x-2.15,-1.9,0],[x+2.5,-1.9,0],color=GREY),
                Line([x-2.15,-1.9,0],[x-2.15,2,0],color=GREY))
            onset=DashedLine([x,-1.85,0],[x,1.65,0],color=HI)
            labs=VGroup(T(name,32,col).move_to([x,2.45,0]),T('Action onset',26,HI).move_to([x,-2.35,0]),
                T('Time',26).move_to([x,-2.9,0]))
            panels.add(VGroup(axes,onset,labs))
            # Different sigmoid widths/centres illustrate 'around onset', not kinetics.
            traces.append(curve(lambda t,x=x,shift=shift,width=width:
                [x+t,-1.15+2.3*sigmoid(t,shift,width),0],-1.95,2.3,col))
        plot=VGroup(panels,T('Activity (schematic)',26).rotate(PI/2).move_to([-6.1,.1,0]),
            T('Qualitative · after Cui and colleagues, 2013',26,GREY).move_to([0,-3.5,0]))
        intro=VGroup(RoundedRectangle(width=10.8,height=5.6,corner_radius=.25,color=GREY),
            M('?',110,HI).move_to([0,.7,0]),T('Where does the count stop?',36).move_to([0,-1.2,0]))
        self.add(intro)
        self.at('count has a hard limit'); self.wait(.2)
        self.at('In mice'); self.play(FadeOut(intro),FadeIn(plot),*[Create(t) for t in traces],run_time=.65)
        self.at('both pathways become active'); self.play(*[Indicate(t,scale_factor=1.015) for t in traces],run_time=.5)
        self.at('around the start'); self.play(*[Indicate(p[1],scale_factor=1,color=HI) for p in panels],run_time=.5)
        self.finish()


class S13Limit2(SpokenScene):
    def construct(self):
        gpi=node('GPi',(0,0),INH,w=3.2,h=2.0,size=38)
        gpi[1].move_to([0,-.4,0])
        direct=T('Direct',34,INH).move_to([0,2.9,0])
        indirect=T('Indirect',34,EXC).move_to([0,-2.85,0])
        down=link([0,2.5,0],[0,1.12,0],-1,width=7)
        up=link([0,-2.45,0],[0,-1.12,0],1,width=7)
        minus=chip('−1',INH,30).move_to([-1.05,1.85,0]); plus=chip('+1',EXC,30).move_to([1.05,-1.85,0])
        self.add(gpi,direct,indirect,down,up,minus,plus)
        self.at('pull in opposite directions'); self.play(Indicate(down,scale_factor=1),Indicate(up,scale_factor=1),run_time=.55)
        self.at('counting cannot say')
        q=M('?',55,HI).move_to([0,.38,0]); note=T('Opposite signs\nThe count makes no call',26,line_spacing=1.5).move_to([4.1,0,0])
        self.play(FadeIn(q),FadeIn(note),run_time=.5)
        self.at('how strong each')
        self.play(down.animate.set_stroke(width=15),run_time=.45)
        self.wait(1.0)
        self.play(down.animate.set_stroke(width=7),up.animate.set_stroke(width=15),run_time=.45)
        self.wait(1.0)
        self.play(up.animate.set_stroke(width=7),run_time=.3); self.finish()


class S14Tremor(SpokenScene):
    def construct(self):
        self.add(heading('Open questions'))
        cards=[]
        for x,label,sub in [(-3.15,'Rest tremor','The count gives no account'),
            (3.15,'How deep brain\nstimulation works','Mechanism unresolved')]:
            box=RoundedRectangle(width=5.8,height=5.65,corner_radius=.2,color=GREY,stroke_width=3).move_to([x,-.25,0])
            card=VGroup(box,M('?',76,HI).move_to([x,1.35,0]),T(label,30).move_to([x,-.15,0]),
                T(sub,26,GREY).move_to([x,-2.05,0]))
            cards.append(card)
        self.add(cards[0])
        self.at('no account of rest'); self.play(cards[0][0].animate.set_stroke(HI,width=5),run_time=.45)
        self.at('how deep brain stimulation'); self.play(FadeIn(cards[1]),run_time=.5)
        self.at('still unresolved'); self.play(cards[1][0].animate.set_stroke(HI,width=5),run_time=.4); self.finish()


class S15Takeaway(SpokenScene):
    def construct(self):
        side=VGroup(RoundedRectangle(width=11.7,height=2.5,corner_radius=.2,color=HI),
            T('SIDE',28,HI).move_to([-4.7,.55,0]),T('1 crossing: opposite side',38).move_to([.1,-.25,0])).move_to([0,1.55,0])
        sign=VGroup(RoundedRectangle(width=11.7,height=2.5,corner_radius=.2,color=INH),
            T('SIGN',28,INH).move_to([-4.7,.55,0]),T('1 inhibition (odd):',36).move_to([.1,.05,0]),
            T('opposite direction',38).move_to([.1,-.65,0])).move_to([0,-1.55,0])
        self.add(side)
        self.at('Count crossings'); self.play(Indicate(side,scale_factor=1.015),run_time=.45)
        self.at('inhibitions for sign'); self.play(FadeIn(sign),run_time=.45)
        self.at('then check'); self.play(Circumscribe(VGroup(side,sign),color=TEXT,fade_out=True),run_time=.65); self.finish()


class S16End(EndCard):
    LINE='Count crossings for side, inhibitions for sign. Then check against the data.'
    def construct(self):
        # The review explicitly requests this complete rule (13 whitespace words).
        line=T('Count crossings for side,\ninhibitions for sign.\nThen check against the data.',40,font=TITLE_FONT,line_spacing=1.25)
        sub=T('biochemistrypedia.com',26,TEAL).next_to(line,DOWN,buff=.65)
        self.play(FadeIn(line),FadeIn(sub),run_time=.6); self.finish()
