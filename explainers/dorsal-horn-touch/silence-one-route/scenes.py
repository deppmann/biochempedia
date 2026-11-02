"""COLOR MAP: BLUE direct afferent; ORANGE indirect/PSDC; PURPLE gracile
neuron; GREEN active spinal synapses; YELLOW light/spikes; GREY anatomy/block.
Waves are sin(2*pi*f*t), with phase-zero timing marks. Response bars and
threshold positions are qualitative diagrams, never experimental traces.
"""
import numpy as np
from bp_style import *
PURPLE = '#B58CD9'
ORANGE = '#F29E4C'


def label(s, x=0, y=3.3, size=30, color=TEXT):
    return T(s, size, color, line_spacing=.8).move_to([x,y,0])


def poly(pts, color, w=6, opacity=1):
    return VMobject().set_points_as_corners([np.array([*p,0.]) for p in pts]).set_stroke(color,w,opacity=opacity).set_fill(opacity=0)


def send(scene, pts, run=1):
    d=Dot(radius=.13,color=YELLOW)
    scene.add(d)
    scene.play(MoveAlongPath(d,poly(pts,YELLOW)),run_time=run,rate_func=linear)
    scene.remove(d)


def switch(x,y,col):
    return VGroup(Circle(radius=.36,color=col,fill_color=BG,fill_opacity=1).move_to([x,y,0]),Line([x-.24,y-.16,0],[x+.24,y+.18,0],color=col,stroke_width=5))


def circuit(anatomy=True):
    # Identical direct ascent and spinal detour in the opening and both switches.
    cord=RoundedRectangle(width=5.7,height=2.1,corner_radius=.2,color=GREY,fill_opacity=.04).move_to([-.4,-1.8,0])
    brain=RoundedRectangle(width=5.7,height=1.7,corner_radius=.2,color=PURPLE,fill_opacity=.08).move_to([.5,1.65,0])
    trunk=poly([[-5.5,-2.3],[-3,-2.3],[-3,1.65]],BLUE,8)
    terminal=poly([[-3,1.65],[1.3,1.65]],BLUE,8)
    ends=VGroup(*[Dot([x,1.65,0],radius=.1,color=BLUE) for x in [.65,.95,1.25]])
    branch=poly([[-3,-1.7],[-1.5,-1.7]],BLUE,7)
    syn=VGroup(*[Dot([x,-1.7,0],radius=.12,color=GREEN) for x in [-1.35,-1.0]])
    ps=Circle(radius=.34,color=ORANGE,fill_opacity=.2).move_to([-.4,-1.7,0])
    indirect=poly([[0,-1.7],[3.4,-1.7],[3.4,.85],[2.2,1.35]],ORANGE,8)
    n=Circle(radius=.5,color=PURPLE,fill_opacity=.25).move_to([1.85,1.65,0])
    labs=VGroup(label('Direct',-3.85,.3,28,BLUE),label('Indirect',4.4,-.1,28,ORANGE),label('gracile\nneuron',4.9,1.7,27,PURPLE))
    labs.add(Line([2.42,1.8,0],[3.95,1.8,0],color=PURPLE,stroke_width=2))
    if anatomy:
        labs.add(label('lumbar cord',-.4,-3.2,27,GREY),label('gracile nucleus',-.4,2.78,27,PURPLE),label('PSDC',-.4,-2.4,27,ORANGE))
    else:
        cord.set_opacity(0); brain.set_opacity(0)
    return VGroup(cord,brain,trunk,terminal,ends,branch,syn,ps,indirect,n,labs)


def paw(center=(0,0), color=GREY):
    x,y=center
    base=Ellipse(width=3.3,height=2.3,color=color,fill_opacity=.07).move_to([x,y,0])
    toes=VGroup(*[Ellipse(width=.57,height=.85,color=color,fill_opacity=.07).move_to([x+dx,y+1.1+dy,0]) for dx,dy in [(-1.15,-.18),(-.4,.12),(.4,.12),(1.15,-.18)]])
    return VGroup(base,toes)


ROWS=['Vibration','Gentle\ndisplacement','Sustained\npress']
ANS=[['Precise timing,\nhigh frequencies','Adds at 10 Hz'],['Contributes','Contributes'],['Almost no sustained\nfiring alone','Sustained firing']]
XS=[-.1,4.0]
YS=[1.15,-1.0,-2.4]


def cell(s,r,c):
    return label(s,XS[c],YS[r],26,BLUE if c==0 else ORANGE)


def table(filled=(), prompt=False, band=False):
    g=VGroup(label('What does each route carry?',size=32))
    for c,col in enumerate([BLUE,ORANGE]):
        g.add(RoundedRectangle(width=3.85,height=5.8,corner_radius=.15,color=col,fill_color=col,fill_opacity=.07).move_to([XS[c],-.2,0]),label(['Direct','Indirect'][c],XS[c],2.25,30,col))
    cells={}
    for r,y in enumerate(YS):
        g.add(label(ROWS[r],-4.5,y,28))
        for c in range(2):
            cells[r,c]=cell(ANS[r][c] if r in filled else '?',r,c)
            g.add(cells[r,c])
    if band:
        # Reserve a separate caption band, with a clear gap below the table.
        for mob in list(g)[1:]:
            mob.stretch(.82, 1, about_point=[0,2.7,0])
        for r in range(3):
            for k in range(2):
                cells[r,k].become(label(ANS[r][k] if r in filled else '?',XS[k],2.7+(YS[r]-2.7)*.82,28,[BLUE,ORANGE][k]))
    if prompt:
        for k in [1,3]:
            g[k].stretch_to_fit_height(6.0).move_to([XS[(k-1)//2],-.2,0])
        for r,y in enumerate([1.15,-.65,-2.35]):
            g[5+3*r].become(label(ROWS[r],-4.5,y,30))
            for k in range(2):
                cells[r,k].become(label('?',XS[k],y,36,[BLUE,ORANGE][k]))
        for y in [.25,-1.55]:
            g.add(Line([-5.9,y,0],[5.9,y,0],color=GREY,stroke_width=2).set_opacity(.35))
        g.add(label('Predict · which route would you choose?',0,-3.55,34,TEAL))
    return g,cells


def wave(c,slow=False):
    # Two windows: 60 ms at 100 Hz versus 300 ms at 10 Hz; illustrative models.
    f,dur=(10,.3) if slow else (100,.06)
    left=XS[c]-1.5
    wave=poly([[left+3*t/dur,.35+.18*np.sin(2*np.pi*f*t)] for t in np.linspace(0,dur,601)],[BLUE,ORANGE][c],3)
    ticks=VGroup(*[Line([left+3*t/dur,-.05,0],[left+3*t/dur,.15,0],color=[BLUE,ORANGE][c],stroke_width=3) for t in np.arange(0,dur+1e-8,1/f)])
    return VGroup(wave,ticks)


def vibration():
    g,c=table((0,))
    c[0,0].move_to([XS[0],1.3,0]); c[0,1].move_to([XS[1],1.3,0])
    return VGroup(g,wave(0),wave(1,True),label('Model: 100 Hz',XS[0],-.33,26,BLUE),label('10 Hz',XS[1],-.33,26,ORANGE))


def threshold(done=False):
    g=VGroup(label('Onset threshold raised',size=34))
    axis=Arrow([-5.3,-.65,0],[5.3,-.65,0],buff=0,color=GREY)
    g.add(axis,label('Applied force (mN)',0,-1.6,30))
    for x,s in [(-5,'1'),(5,'300')]:
        g.add(Line([x,-.8,0],[x,-.5,0],color=GREY),label(s,x,-1.07,28))
    ghost=DashedVMobject(Arrow([-2.5,1.65,0],[-2.5,-.5,0],buff=0,color=GREY,stroke_width=5),num_dashes=15)
    mark=Arrow([-2.5,1.65,0],[-2.5,-.5,0],buff=0,color=ORANGE,stroke_width=7)
    g.add(ghost,label('Control',-2.5,2.1,30,GREY),mark,label('Schematic shift · threshold values not quantified',0,-2.4,26,GREY))
    if done:
        mark.shift(RIGHT*5)
        g.add(label('After block',2.5,2.1,30,ORANGE),label('Indirect input also supports onset',0,-3.1,29,ORANGE),label('Not just a late add-on',0,.7,30))
    return g,mark


def field(col):
    return Ellipse(width=1.85,height=1.35,color=col,stroke_width=7,fill_color=col,fill_opacity=.17).move_to([0,-.65,0])


def registered():
    p=paw((0,-.65)).scale(1.65,about_point=[0,-.65,0])
    b=field(BLUE); o=DashedVMobject(field(ORANGE).set_fill(opacity=0),num_dashes=22)
    return VGroup(p,b,o,label('Highly aligned receptive fields',size=34))


def reports():
    p=paw((0,-1.9)).scale(1.05,about_point=[0,-1.9,0])
    patch=field(BLUE).scale(.7).move_to([0,-1.9,0]); patch2=DashedVMobject(field(ORANGE).scale(.7).move_to([0,-1.9,0]),num_dashes=16)
    n=Circle(radius=.6,color=PURPLE,fill_opacity=.22).move_to([0,1.9,0])
    a=poly([[-.5,-1.5],[-2.6,.2],[-.5,1.6]],BLUE,8); b=poly([[.5,-1.5],[2.6,.2],[.5,1.6]],ORANGE,8)
    return VGroup(p,patch,patch2,n,a,b,label('Two reports · one spot · one neuron',size=32),label('Direct',-3.45,.3,29,BLUE),label('Indirect',3.55,.3,29,ORANGE),label('gracile neuron',0,2.8,28,PURPLE))


class S00Title(TitleCard):
    TITLE='Silence One Route'
    LESSON='Where Touch Is First Processed: Dorsal Horn and Dorsal Column Nuclei'
    def construct(self):
        self.add(label('BIOCHEMISTRYPEDIA',y=2.7,size=26,color=TEAL))
        self.add(label('Where Touch Is First Processed\nDorsal Horn and Dorsal Column Nuclei',y=1.25,size=26,color=GREY))
        self.play(FadeIn(label(self.TITLE,y=-.3,size=52)),Create(Line([-1.5,-1.2,0],[1.5,-1.2,0],color=GOLD)),run_time=.7)
        self.finish()


class S01Question(SpokenScene):
    def construct(self):
        c=circuit(False); self.add(c,label('What does each route carry?',size=36))
        self.at('feed one'); self.play(Indicate(c[9],scale_factor=1.2),run_time=.5)
        self.at('How can you'); self.play(Indicate(VGroup(c[3],c[8]),scale_factor=1.03),run_time=.7)
        self.finish()


class S02Logic(SpokenScene):
    def construct(self):
        c=circuit(False); self.add(c,label('What does each route carry?',size=36))
        s1=switch(-3,.75,BLUE); s2=switch(3.4,-.7,ORANGE)
        self.at('Take'); self.play(FadeIn(s1),FadeIn(s2),run_time=.4)
        self.at('away at a time'); self.play(c[3].animate.set_stroke(opacity=.2),c[4].animate.set_opacity(.2),Rotate(s1[1],angle=-.8),run_time=.5)
        self.at('watch what'); self.play(FadeIn(label('Remove one route, compare',0,-3.3,32)),run_time=.4)
        self.finish()


class S03Record(SpokenScene):
    def construct(self):
        stem=RoundedRectangle(width=8.5,height=5.35,corner_radius=.7,color=GREY,fill_opacity=.06).move_to([0,-.2,0])
        nucleus=RoundedRectangle(width=5.4,height=3.5,corner_radius=.4,color=PURPLE,fill_opacity=.12).move_to([-.7,-.35,0])
        n=Circle(radius=.35,color=PURPLE,fill_opacity=.4).move_to([-.6,-.5,0])
        elec=VGroup(Line([3,2,0],[-.6,.35,0],color=GREY,stroke_width=10),Line([-.6,.35,0],[-.6,-.45,0],color=TEXT,stroke_width=4)).shift(UP*.6)
        self.add(stem,nucleus,n,label('Turecek, Lehnert and Ginty · Nature 2022',size=29),label('gracile nucleus',-.7,-1.55,30,PURPLE),label('Schematic brainstem',0,-2.6,26,GREY),label('Adult mice · urethane anaesthesia',0,-3.35,28))
        self.at('recorded single'); self.play(FadeIn(elec),run_time=.3)
        self.at('in the hindlimb'); self.play(elec.animate.shift(DOWN*.6),run_time=1.25)
        self.finish()


class S04Vpl(SpokenScene):
    def construct(self):
        start=np.array([-4.4,-2.0,0]); end=np.array([4.9,2.0,0]); mid=(start+end)/2
        soma=Circle(radius=1.0,color=PURPLE,fill_opacity=.25).move_to(start+LEFT*.65)
        ax=Line(start,end,color=TEXT,stroke_width=15)
        title=label('Testing a thalamic projection',size=34)
        self.add(soma,ax,title,label('Recorded gracile neuron',-3.9,-3.35,29,PURPLE),label('Thalamus (VPL)',4.5,2.8,30))
        self.at('stimulating their axons'); self.play(Flash(end,color=YELLOW,flash_radius=.6),run_time=.45)
        self.at('spikes backward'); send(self,[end[:2],start[:2]],.75)
        self.at('checked with')
        # Two colours remain visible side by side at the collision for sampling.
        offset=np.array([-.10,.23,0])
        up=Dot(start,radius=.23,color=BLUE); back=Dot(end,radius=.23,color=YELLOW)
        self.add(up,back,label('Spontaneous spike →',-2.5,1.4,30,BLUE),label('← Backward spike',2.8,-1.45,30,YELLOW))
        self.play(up.animate.move_to(mid+offset),back.animate.move_to(mid-offset),run_time=.7,rate_func=linear)
        meeting=Circle(radius=.58,color=RED,stroke_width=4).move_to(mid)
        collision=label('Spikes meet',.25,-.95,30,RED)
        self.add(meeting,collision)
        self.wait(3.1)
        self.play(FadeOut(up),FadeOut(back),FadeOut(collision),FadeOut(meeting),run_time=.4)
        ghost=DashedVMobject(Circle(radius=.3,color=GREY).move_to(start),num_dashes=10)
        self.add(ghost,DashedLine(mid,start,color=YELLOW,dash_length=.15).set_opacity(.4),label('Collision test · spikes cancel',0,2.5,32,YELLOW),label('Expected return: absent',.2,-2.65,30),DashedLine(start+DOWN*.3,[.2,-2.25,0],color=GREY))
        self.play(Transform(title,label('Projects to the thalamus',size=34)),run_time=.3)
        self.wait(3.1)
        self.finish()


class S05Switch1(SpokenScene):
    def construct(self):
        c=circuit()
        c[10][5].become(label('gracile nucleus',-.5,1.1,27,PURPLE))
        self.add(c,label('ACR1 silencing at the gracile nucleus',size=31,color=BLUE),label('Light-gated\nchloride channel',-4.9,2.45,27,YELLOW))
        light=Polygon([.7,2.95,0],[1.1,2.95,0],[1.32,1.55,0],[.53,1.55,0],fill_color=YELLOW,fill_opacity=.4,stroke_width=0)
        self.at('Light on the'); self.play(FadeIn(light),run_time=.5)
        self.at('silences'); self.play(c[3].animate.set_stroke(opacity=.18),c[4].animate.set_opacity(.18),run_time=.65)
        self.add(label('Branches in the lumbar\ncord stay active',.1,-.25,26,GREEN),Line([-1.3,-.65,0],[-1.3,-1.45,0],color=GREEN,stroke_width=2))
        self.play(Indicate(c[6],color=GREEN,scale_factor=1.6),run_time=.65)
        self.at('chloride channel'); self.play(Indicate(light,scale_factor=1.05),run_time=.4)
        self.finish()


class S06Switch2(SpokenScene):
    def construct(self):
        c=circuit(); self.add(c,label('Block spinal synapses in the lumbar cord',size=31,color=ORANGE))
        drop=VGroup(Circle(radius=.22,color=GREY,fill_opacity=1),Triangle(color=GREY,fill_opacity=1).scale(.2).shift(UP*.2)).move_to([-1.9,.2,0])
        druglabel=label('Glutamate receptor\nantagonists',.6,.1,26,GREY)
        leader=Line([-.9,-.1,0],[-1.65,.15,0],color=GREY)
        self.at('Drugs on the'); self.add(drop,druglabel,leader); self.play(drop.animate.move_to([-.9,-1.65,0]),leader.animate.put_start_and_end_on([-.4,-.55,0],[-1.1,-1.35,0]),run_time=.65)
        self.at('block its spinal'); self.play(FadeOut(drop),c[6].animate.set_color(GREY),c[7].animate.set_color(GREY),run_time=.35)
        self.play(c[8].animate.set_stroke(color=GREY,opacity=.3),run_time=.4)
        self.at('direct branches'); c[10][0].become(label('Direct axons\nstill conduct',-4.8,.4,27,BLUE)); send(self,[[-5.5,-2.3],[-3,-2.3],[-3,1.65],[1.3,1.65]],1.5)
        self.at('keep conducting'); send(self,[[-3,-1.7],[-3,1.65],[1.3,1.65]],.8)
        self.finish()


class S07Stimuli(SpokenScene):
    def construct(self):
        self.add(label('Three stimuli on the hindpaw',size=34))
        xs=[-4.25,0,4.25]
        paws=[paw((x,-.7)) for x in xs]; self.add(*paws)
        probes=[Rectangle(width=.22 if k<2 else .7,height=1.4,color=GREY,fill_opacity=.8).move_to([x,1.65,0]) for k,x in enumerate(xs)]
        self.at('a vibration'); self.add(probes[0],label('Vibration',xs[0],-2.4,28,BLUE))
        self.play(probes[0].animate.shift(DOWN*.4),run_time=.2)
        for _ in range(3): self.play(probes[0].animate.shift(UP*.22),rate_func=there_and_back,run_time=.22)
        self.at('a gentle displacement'); self.add(probes[1],label('Gentle\ndisplacement',0,-2.4,28))
        self.play(probes[1].animate.shift(DOWN*.4),run_time=.3); self.play(probes[1].animate.shift(RIGHT*.3),paws[1][0].animate.shift(RIGHT*.1),run_time=.55)
        self.at('a sustained press'); self.add(probes[2],label('Sustained press',xs[2],-2.4,28,ORANGE))
        self.play(probes[2].animate.shift(DOWN*.5),paws[2][0].animate.stretch(.9,1),run_time=.6)
        self.add(label('Blunt 1-mm probe · 1 to 300 mN',0,-3.3,28,GREY))
        self.finish()


class S08Question(SpokenScene):
    def construct(self):
        g,c=table(prompt=True); self.add(g)
        self.at('carries vibration'); self.play(Indicate(VGroup(c[0,0],c[0,1])),run_time=.5)
        self.at('sustained press'); self.play(Indicate(VGroup(c[2,0],c[2,1])),run_time=.5)
        self.at('gentle displacement'); self.play(Indicate(VGroup(c[1,0],c[1,1])),run_time=.5)
        self.finish()


class S09Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(table(prompt=True)[0]); self.wait(5)


class S10Vib(SpokenScene):
    def construct(self):
        g,c=table(); self.add(g)
        self.at('direct input'); self.play(Transform(c[0,0],label(ANS[0][0],XS[0],1.3,26,BLUE)),run_time=.4)
        self.at('high temporal precision'); self.play(Create(wave(0)),FadeIn(label('Model: 100 Hz',XS[0],-.33,26,BLUE)),run_time=.65)
        self.at('indirect route'); self.play(Transform(c[0,1],label(ANS[0][1],XS[1],1.3,26,ORANGE)),Create(wave(1,True)),FadeIn(label('10 Hz',XS[1],-.33,26,ORANGE)),run_time=.5)
        self.finish()


class S11Beat(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(vibration()); self.wait(2)


class S12Press(SpokenScene):
    def construct(self):
        self.add(label('Sustained press',size=36,color=ORANGE),label('Different units · schematic responses',0,2.6,27,GREY))
        boxes=VGroup(*[RoundedRectangle(width=5.5,height=5.45,corner_radius=.2,color=GREY,fill_opacity=.04).move_to([x,-.45,0]) for x in [-3,3]])
        self.add(boxes,label('Control unit',-3,1.65,32),label('Lumbar synapses\nblocked',3,1.6,29))
        self.add(Arrow([-5.15,-1.2,0],[5.15,-1.2,0],buff=0,color=GREY),label('Shared time →',-3,-1.65,28,GREY))
        for x in [-3,3]:
            self.add(Line([x-1.7,-2.25,0],[x+1.7,-2.25,0],color=TEXT,stroke_width=5),label('Press held',x,-2.65,28))
        firing=Rectangle(width=3.4,height=.95,color=ORANGE,fill_opacity=.7).move_to([-3,.05,0])
        self.at('Now the press'); self.play(GrowFromEdge(firing,LEFT),FadeIn(label('Sustained firing',-3,.75,28,ORANGE)),run_time=.5)
        self.at('almost eliminated'); self.play(Create(Line([1.3,.05,0],[4.7,.05,0],color=GREY,stroke_width=4)),FadeIn(label('Almost silent',3,.75,28,GREY)),run_time=.5)
        self.play(FadeIn(label('Direct alone: almost no sustained firing',0,-3.6,28,BLUE)),run_time=.4)
        self.finish()


class S13Threshold(SpokenScene):
    def construct(self):
        g,m=threshold(); self.add(g)
        self.at('raised the force'); self.play(m.animate.shift(RIGHT*5),FadeIn(label('After block',2.5,2.1,30,ORANGE)),run_time=1)
        self.at('indirect route'); self.play(FadeIn(label('Indirect input also supports onset',0,-3.1,29,ORANGE)),run_time=.4)
        self.at('not just a late'); self.play(FadeIn(label('Not just a late add-on',0,.7,30)),run_time=.4)
        self.finish()


class S14Beat(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(threshold(True)[0]); self.wait(2)


class S15Gentle(SpokenScene):
    def construct(self):
        g,c=table((0,2),band=True); self.add(g)
        self.at('used both'); self.play(*[Transform(c[1,k],label('Contributes',XS[k],2.7+(YS[1]-2.7)*.82,28,[BLUE,ORANGE][k])) for k in range(2)],run_time=.5)
        slogan=label('Direct = vibration; indirect = light touch',0,-2.95,34)
        self.at('So direct'); self.play(FadeIn(slogan),run_time=.4)
        self.at('too simple',lead=-.65); self.play(Create(Line(slogan.get_left()+LEFT*.1,slogan.get_right()+RIGHT*.1,color=RED,stroke_width=4)),run_time=.4)
        self.wait(3.1)
        self.finish()


class S16Aligned(SpokenScene):
    def construct(self):
        # Both outlines have exactly the same points and registration throughout.
        g=registered(); goldpaw=g[0].copy(); gold=field(ORANGE)
        title=label('Map each input on the same neuron',size=34)
        legend=VGroup(Line([-2.7,-3.3,0],[-2,-3.3,0],color=BLUE,stroke_width=6),label('Direct field',-.75,-3.3,27,BLUE))
        self.add(g[0],g[1],title,legend)
        self.at('direct and indirect'); self.play(FadeOut(g[0]),FadeOut(g[1]),FadeOut(legend),FadeIn(goldpaw),FadeIn(gold),run_time=.5)
        goldlegend=VGroup(Line([-2.7,-3.3,0],[-2,-3.3,0],color=ORANGE,stroke_width=6),label('Indirect field',-.65,-3.3,27,ORANGE)); self.add(goldlegend)
        self.at('highly aligned'); self.play(FadeIn(g[0]),FadeIn(g[1]),FadeOut(goldpaw),FadeOut(gold),FadeIn(g[2]),Transform(title,g[3]),FadeOut(goldlegend),run_time=.65)
        self.add(label('Blue: direct · Gold: indirect',0,-3.3,27))
        self.wait(2.6)
        self.finish()


class S17Meaning(SpokenScene):
    def construct(self):
        r=reports(); self.add(r[0],r[1],r[2],r[3],r[6],r[9])
        self.at('two reports'); self.play(Create(r[4]),FadeIn(r[7]),run_time=.55); self.play(Create(r[5]),FadeIn(r[8]),run_time=.55)
        self.at('meeting on one'); self.play(Indicate(r[3],color=PURPLE,scale_factor=1.2),run_time=.5)
        self.finish()


class S18Beat(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(reports()); self.wait(3)


class S19Caveat(SpokenScene):
    def construct(self):
        conclusion=label('High-force conclusion rests\non the lumbar drug',0,-1.45,36,ORANGE).set_opacity(.55)
        validation=label('Validated only to about 20–30 mN',0,.1,34)
        self.add(label('One limit',size=36),RoundedRectangle(width=11.2,height=4.7,corner_radius=.2,color=GREY,fill_opacity=.04).move_to([0,-.2,0]),chip('ACR1 light silencing',BLUE,34).move_to([0,1.45,0]),validation,conclusion)
        self.at('validated only'); self.play(Indicate(validation,scale_factor=1.03),run_time=.4)
        self.at('So the'); self.play(conclusion.animate.set_opacity(1),run_time=.4)
        self.finish()


class S20Caveat2(SpokenScene):
    def construct(self):
        box=RoundedRectangle(width=11.4,height=4.7,corner_radius=.3,color=GREY,fill_opacity=.06).move_to([0,-.5,0])
        cells=VGroup(*[Circle(radius=.65,color=col,fill_opacity=.35).move_to([x,-.7,0]) for x,col in [(-3.5,ORANGE),(0,GREEN),(3.5,RED)]])
        drop=VGroup(Circle(radius=.35,color=TEXT,fill_opacity=.85),Triangle(color=TEXT,fill_opacity=.85).scale(.32).shift(UP*.3)).move_to([0,2.0,0])
        self.add(box,cells,label('Not PSDC-specific',size=36),label('Lumbar cord',0,-3.3,28,GREY),label('PSDC',-3.5,-1.9,30,ORANGE),label('Other spinal neurons',1.7,-1.9,30),drop)
        self.at('that drug'); self.play(drop.animate.move_to([0,.35,0]),run_time=.45)
        self.at('not specific'); self.play(cells.animate.set_color(GREY).set_fill(GREY,opacity=.5),FadeOut(drop),run_time=.6)
        self.finish()


class S21Pain(SpokenScene):
    def construct(self):
        self.add(label('Strong firing alone does not establish pain',size=31),label('Awake control trials · head-fixed',0,2.6,29))
        body=Ellipse(width=5.3,height=2.2,color=GREY,fill_opacity=.2).move_to([-.5,-.05,0])
        head=Ellipse(width=1.85,height=1.4,color=GREY,fill_opacity=.2).move_to([2.7,.35,0])
        ear=Circle(radius=.38,color=GREY,fill_opacity=.15).move_to([2.1,1.05,0]); eye=Dot([3,.6,0],radius=.07,color=TEXT)
        nose=poly([[3.45,.65],[3.95,.2],[3.4,-.1]],GREY,5)
        tail=VMobject().set_points_smoothly([[-3,.0,0],[-3.7,-.5,0],[-4.8,-.6,0],[-5.7,-.25,0]]).set_stroke(GREY,7)
        thigh=Ellipse(width=1.3,height=1.6,color=GREY,fill_color=BG,fill_opacity=1).move_to([-2.2,-.55,0])
        leg=poly([[-2.4,-1],[-2.7,-1.6],[-1.65,-1.6]],GREY,9)
        front=poly([[1.4,-.6],[1.2,-1.6],[2,-1.6]],GREY,8)
        platform=Rectangle(width=11.7,height=.15,color=GREY,fill_opacity=.15).move_to([0,-1.85,0])
        fixation=poly([[2.9,1.0],[4.8,1.0],[4.8,-1.7]],GREY,7)
        probe=VGroup(Rectangle(width=.48,height=1.5,color=TEXT,fill_opacity=.65),Line([-.5,-.75,0],[.5,-.75,0],color=TEXT,stroke_width=6)).move_to([-2.25,1.55,0])
        self.add(body,head,ear,eye,nose,tail,thigh,leg,front,platform,fixation,probe,label('Blunt probe',-4.55,1.85,27),Line([-3.5,1.7,0],[-2.6,1.5,0],color=GREY),label('Paw stays still',-2.4,-2.55,28))
        self.at('strong firing'); self.play(probe.animate.shift(DOWN*.65),run_time=.6)
        self.at('the high force'); self.play(Indicate(probe,color=TEXT,scale_factor=1.03),run_time=.45)
        self.at('evoked no'); self.play(FadeIn(label('No withdrawal or pain-related behaviour',0,-3.35,29)),run_time=.4)
        self.finish()


class S22Takeaway(SpokenScene):
    def construct(self):
        g,c=table((0,1,2),band=True); g.shift(LEFT*g.get_center()[0]); self.add(g)
        band=label('Fast timing → direct',0,-2.95,34,BLUE)
        def highlight(r,k):
            return SurroundingRectangle(c[r,k],color=[BLUE,ORANGE][k],buff=.12,stroke_width=4,fill_color=[BLUE,ORANGE][k],fill_opacity=.15)
        h=highlight(0,0)
        self.at('fast timing'); self.play(FadeIn(h),FadeIn(band),run_time=.4)
        self.at('Sustained pressure'); band.become(label('Sustained pressure → indirect',0,-2.95,34,ORANGE)); self.play(Transform(h,highlight(2,1)),run_time=.4)
        self.at('Gentle touch'); band.become(label('Gentle touch → both',0,-2.95,34,TEAL)); self.play(Transform(h,SurroundingRectangle(VGroup(c[1,0],c[1,1]),color=TEAL,buff=.15,fill_color=TEAL,fill_opacity=.12)),run_time=.4)
        self.at('both report'); band.become(label('Both report the same skin',0,-2.95,34)); self.play(FadeOut(h),run_time=.4)
        self.finish()


class S23End(EndCard):
    LINE='Fast timing rides the direct route; sustained pressure rides the indirect one. Both report the same skin.'
    def construct(self):
        self.add(label('Fast timing rides the direct route;',y=1.5,size=35,color=BLUE),label('sustained pressure rides the indirect one.',y=.5,size=35,color=ORANGE),label('Both report the same skin.',y=-1,size=38),label('biochemistrypedia.com',y=-2.7,size=27,color=TEAL))
        self.finish()
