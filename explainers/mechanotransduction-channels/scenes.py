"""Chapter 1 fix round.
COLOR MAP: BLUE Piezo; GREY membrane/unknown; YELLOW applied force;
GREEN computed current/earned claims; RED knockdown; GOLD pore evidence.
Cartoons only, no molecular structures. Current: I=-A exp(-(t-5)/tau)
for t>=5 ms during a held stimulus. Normalized illustrative amplitude;
Piezo2 tau=7.3 ms, Piezo1 illustrative tau=16 ms. No release notch.
"""
import numpy as np
from bp_style import *


def heading(s):
    return T(s,36,font=TITLE_FONT).move_to([0,3.1,0])


def cell(dent=0):
    ts=np.linspace(0,TAU,241)
    points=[]
    for t in ts:
        displacement=dent*np.exp(-((t-PI)/.26)**2)
        points.append([-3+2.4*np.cos(t)+displacement,-.35+2.4*np.sin(t),0])
    return VMobject(color=GREY,stroke_width=5,fill_color=GREY,fill_opacity=.10).set_points_as_corners(points).close_path()


def probe(pressed=False):
    g=Polygon([-6.65,.15,0],[-5.45,-.35,0],[-6.65,-.85,0],color=YELLOW,fill_color=YELLOW,fill_opacity=.2)
    if pressed:g.shift(RIGHT*.5)
    return g


def pipette():
    return Polygon([-.6,-.35,0],[.35,.95,0],[.65,.55,0],color=TEXT,fill_color=GREY,fill_opacity=.2)


def trace(cx=3.25,cy=-.35,width=5,height=4.8,tau=16,amp=1):
    ax=Axes(x_range=[0,80,20],y_range=[-1.1,.1,.5],x_length=width,y_length=height,
        axis_config={'include_tip':False,'include_ticks':False,'color':GREY,'stroke_width':2})
    ax.move_to([cx,cy,0])
    ts=np.r_[np.linspace(0,4.999,15),5,np.linspace(5.001,80,240)]
    ys=np.where(ts>=5,-amp*np.exp(-(ts-5)/tau),0)
    curve=VMobject(color=GREEN,stroke_width=5).set_points_as_corners([ax.c2p(t,y) for t,y in zip(ts,ys)])
    # Scale bars sit below the data, never on the baseline or decay.
    y=ax.c2p(0,-1.1)[1]-.24
    scale=Line([ax.c2p(45,0)[0],y,0],[ax.c2p(65,0)[0],y,0],color=TEXT,stroke_width=3)
    labels=VGroup(T('inward current ↓',26,GREEN).move_to([cx,cy+height/2+.4,0]),
        scale,T('20 ms',26).next_to(scale,DOWN,buff=.12),
        T('time →',26,GREY).move_to([cx-width/2+.65,y-.37,0]))
    return VGroup(ax,curve,labels)


def poke(scene,c,p,tr):
    scene.play(Transform(c,cell(.5)),Transform(p,probe(True)),run_time=.25)
    scene.play(Create(tr[1]),run_time=.65,rate_func=linear)


def compare(reduced=True):
    a=trace(-3.15,.65,5.2,3.3)
    b=trace(3.15,.65,5.2,3.3,amp=.12)
    labels=VGroup(T('control',30,GREEN).move_to([-3.15,3.15,0]),
        T('Fam38A knockdown',30,RED).move_to([3.15,3.15,0]),
        T('sharply reduced',28,RED).move_to([3.15,-2.6,0]))
    if not reduced: labels[2].set_opacity(0)
    return VGroup(a,b,labels)


def questions():
    return VGroup(T('What have you shown?',36).move_to([0,-2.6,0]),T('What have you not?',36).move_to([0,-3.25,0]))


def claims(done=0,experiments=True):
    result=VGroup()
    for i,(title,ex) in enumerate(zip(['Necessity','Sufficiency','Pore identity'],['knockdown','expression','no experiment yet'])):
        x=(i-1)*4.15; col=GREEN if i<done else GREY
        box=RoundedRectangle(width=3.85,height=2.45,corner_radius=.18,color=col,fill_color=col,fill_opacity=.09).move_to([x,1.1,0])
        titlemob=T(title,30,col).move_to([x,1.9,0])
        mark=(VMobject(color=col,stroke_width=7).set_points_as_corners([[-.25,0,0],[-.06,-.2,0],[.3,.25,0]]) if i<done else T('unresolved',26,col)).move_to([x,1.05,0])
        sub=T(ex,26,GREY).move_to([x,.2,0])
        if i==2 and done==3:sub=T('purified protein',26,GOLD).move_to(sub)
        result.add(VGroup(box,titlemob,mark,sub))
    return result.shift(DOWN*.9)


def trimer(long=False):
    # Three single-piece cartoon subunits, with separate lining domains.
    g=VGroup()
    for angle in [90,210,330]:
        t=angle*DEGREES; d=np.array([np.cos(t),np.sin(t),0])
        length=3.4 if long else 1.65
        blade=RoundedRectangle(width=1.05,height=length,corner_radius=.35,color=BLUE,fill_color=BLUE,fill_opacity=.3)
        blade.rotate(t-PI/2).move_to(d*(.55+length/2))
        lining=Circle(.29,color=GOLD,fill_color=GOLD,fill_opacity=.7).move_to(d*.48)
        g.add(VGroup(blade,lining))
    g.add(Circle(.23,color=GREEN,stroke_width=6,fill_color=BG,fill_opacity=1))
    return g


class S00Title(TitleCard):
    LESSON='Piezo Channels and the Physics of Force'
    TITLE='Which Protein Carries the Poke?'
    def construct(self):
        g=VGroup(T('BIOCHEMISTRYPEDIA',26,TEAL),T(self.LESSON,28,GREY),T(self.TITLE,42,font=TITLE_FONT),Line(LEFT*1.2,RIGHT*1.2,color=GOLD)).arrange(DOWN,buff=.45)
        self.play(FadeIn(g),run_time=.6);self.finish()


class S01Question(SpokenScene):
    def construct(self):
        c,p,tr=cell(),probe(),trace();self.add(c,p,tr[0],tr[2])
        self.at('cell');poke(self,c,p,tr)
        self.at('nobody knew')
        self.play(FadeIn(T('?',64,BLUE).move_to([-3,2.7,0])),run_time=.3)
        self.at('How would you')
        self.play(FadeIn(T('Which protein\ncarries the poke?',28,font=TITLE_FONT).move_to([-3,-3.3,0])),run_time=.4)
        self.finish()


class S02Setup(SpokenScene):
    def construct(self):
        c,p,tr=cell(),probe(),trace();self.add(c,p,tr[0],tr[2])
        self.at('a cultured mouse')
        label=VGroup(T('mouse neuroblastoma line',28,GREY),T('Neuro2A',36,BLUE)).arrange(DOWN,buff=.2).move_to([-3,-3.3,0])
        self.play(FadeIn(label),FadeIn(T('2010',32).move_to([5.5,3.1,0])),run_time=.4)
        self.at('a reliable current');poke(self,c,p,tr);self.finish()


class S03Rig(SpokenScene):
    def construct(self):
        c,p,tr=cell(),probe(),trace();self.add(c,p,tr[0],tr[2])
        self.at('separate glass probe')
        self.play(FadeIn(T('glass probe',28,YELLOW).move_to([-4.9,2.9,0])),run_time=.3)
        self.at('pressed on the');poke(self,c,p,tr)
        self.at('A patch pipette')
        lab=T('patch pipette:\nwhole-cell current',28).move_to([-3,-3.3,0])
        leader=Line([-1.35,-2.95,0],[-.1,.1,0],color=GREY)
        self.play(Create(pipette()),FadeIn(lab),Create(leader),run_time=.4)
        self.at('recorded the whole')
        self.remove(tr[1]);self.play(Transform(c,cell()),Transform(p,probe()),run_time=.2)
        poke(self,c,p,tr);self.finish()


class S04Screen(SpokenScene):
    def construct(self):
        tiles=VGroup(*[chip('—',BLUE,30) for _ in range(6)]).arrange(RIGHT,buff=.6).move_to([0,2.55,0])
        tr=trace(0,-.35,10.8,3.5);tr[2][0].move_to([3,1.8,0]);self.add(tiles,tr,heading('Candidate genes'))
        self.at('one at a time')
        tag=chip('siRNA',RED,28).move_to([tiles[0].get_x(),1.5,0])
        self.play(FadeIn(tag),tiles[0].animate.set_opacity(.25),run_time=.3)
        self.remove(tr[1]);self.play(Create(tr[1]),run_time=.65)
        self.at('Then they asked')
        self.play(Transform(tiles[0],chip('—',BLUE,30).move_to(tiles[0])),tiles[1].animate.set_opacity(.25),tag.animate.move_to([tiles[1].get_x(),1.5,0]),run_time=.2)
        self.remove(tr[1]);self.play(Create(tr[1]),run_time=.35)
        self.at('which loss reduced')
        self.play(Transform(tiles[1],chip('—',BLUE,30).move_to(tiles[1])),tiles[2].animate.set_opacity(.25),tag.animate.move_to([tiles[2].get_x(),1.5,0]),run_time=.35)
        self.remove(tr[1]);self.play(Create(tr[1]),run_time=.65);self.finish()


class S05Hit(SpokenScene):
    def construct(self):
        panels=compare();self.add(panels)
        tile=chip('Fam38A',BLUE,30).move_to([0,-2.9,0]);self.add(tile)
        self.at('One candidate stood');self.play(Indicate(tile,color=YELLOW),run_time=.6)
        self.at('Knocking down');self.play(Indicate(panels[1][1],color=RED,scale_factor=1.06),run_time=.6)
        self.at('sharply reduced');self.play(Indicate(panels[2][2],color=RED),run_time=.5);self.finish()


class S06Predict(SpokenScene):
    def construct(self):
        self.add(compare(reduced=False).scale(.8).shift(UP*.65));q=questions().shift(UP*.35)
        self.add(T('pause and answer',32,TEAL).move_to([0,-1.4,0]))
        self.at('What have you shown');self.play(FadeIn(q[0]),run_time=.3)
        self.at('And what have');self.play(FadeIn(q[1]),run_time=.3);self.finish()


class S07Pause(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(compare(reduced=False).scale(.8).shift(UP*.65),questions().shift(UP*.35))
        cue=T('pause and answer',32,TEAL).move_to([0,-1.4,0]);self.add(cue)
        track=Rectangle(width=5.6,height=.16,stroke_color=TEAL,stroke_width=2).move_to([0,-1.8,0]);self.add(track)
        bar=Rectangle(width=.01,height=.12,stroke_width=0,fill_color=TEAL,fill_opacity=1).move_to([-2.79,-1.8,0]);self.add(bar)
        self.play(bar.animate.stretch_to_fit_width(5.56).move_to([0,-1.8,0]),run_time=5,rate_func=linear)


class S08Reveal(SpokenScene):
    def construct(self):
        self.add(compare(reduced=False))
        self.at('the gene is required');self.play(FadeIn(T('✓  required here (Neuro2A)',34,GREEN).move_to([0,-2.6,0])),run_time=.4)
        self.at('You have not');self.play(FadeIn(T('□  is the channel: not yet shown',32,GREY).move_to([0,-3.25,0])),run_time=.4);self.finish()


class S09Subunit(SpokenScene):
    def construct(self):
        membrane=VGroup(Line([-6,-.3,0],[.15,-.3,0],color=GREY,stroke_width=10),Line([2.65,-.3,0],[6,-.3,0],color=GREY,stroke_width=10))
        pore=VGroup(*[RoundedRectangle(width=.9,height=3.4,corner_radius=.2,color=GREY,fill_color=GREY,fill_opacity=.4).move_to([x,-.3,0]) for x in [.4,2.4]])
        accessory=RoundedRectangle(width=1.4,height=2.3,corner_radius=.2,color=BLUE,fill_color=BLUE,fill_opacity=.3).move_to([-2,-.3,0])
        accessory.move_to([-.85,-.3,0])
        arrow=Arrow([1.4,1.7,0],[1.4,-2.15,0],color=GOLD,buff=0,stroke_width=8)
        labels=VGroup(T('Piezo: possible\naccessory subunit',34,BLUE).move_to([-3.65,-2.9,0]),
            T('unknown channel',34).move_to([2.8,2.3,0]),
            T('conducting pore',34,GOLD).move_to([3,-2.9,0]))
        leaders=VGroup(Line([-2.8,-2.15,0],[-1.1,-1.4,0],color=BLUE),Line([2.3,1.95,0],[2.4,1.4,0],color=GREY))
        self.add(membrane,pore,accessory,arrow,labels,leaders,heading('A required protein…'))
        self.at('could be an');self.play(Indicate(accessory,scale_factor=1.03),run_time=.6)
        self.at('The real pore');self.play(Indicate(pore,scale_factor=1.03),run_time=.4)
        self.at('made of something');self.play(Indicate(arrow,color=GOLD,scale_factor=1.03),run_time=.6);self.finish()


class S10Express(SpokenScene):
    def construct(self):
        c,p,tr=cell(),probe(),trace();self.add(c,tr[0],tr[2],T('host cell',32,GREY).move_to([-3,-3.1,0]))
        gene=chip('gene',BLUE,28).move_to([-5.4,2.6,0])
        self.at('put the gene');self.play(FadeIn(gene),run_time=.2);self.play(gene.animate.move_to([-3,-.35,0]),run_time=.65)
        self.at('The renamed gene');self.play(FadeIn(heading('Fam38A renamed Piezo1')),FadeIn(T('introduced gene',28,BLUE).move_to([-3,-3.65,0])),run_time=.4)
        self.at('gave those cells');self.play(FadeIn(p),run_time=.3)
        self.at('mechanically activated currents');poke(self,c,p,tr);self.finish()


class S11Piezo2(SpokenScene):
    def construct(self):
        a=trace(-3.15,-.05,5.2,4.6);self.add(a,T('Piezo1',34,BLUE).move_to([-3.15,3.3,0]))
        self.at('a related gene');b=trace(3.15,-.05,5.2,4.6,tau=7.3)
        self.play(FadeIn(b[0]),FadeIn(b[2]),FadeIn(T('Piezo2',34,BLUE).move_to([3.15,3.3,0])),run_time=.3)
        self.play(Create(b[1]),run_time=.6)
        self.at('had different kinetics');self.play(FadeIn(T('kinetics differ · shared time scale',30).move_to([0,-3.6,0])),run_time=.4);self.finish()


class S12Cation(SpokenScene):
    def construct(self):
        tr=trace(3.25,.1,5,4.1,tau=7.3);self.add(tr,T('Piezo2',32,BLUE).move_to([3.25,3.2,0]))
        gate=VGroup(*[RoundedRectangle(width=.9,height=4.2,corner_radius=.2,color=BLUE,fill_color=BLUE,fill_opacity=.3).move_to([x,-.15,0]) for x in [-5,-1]])
        self.add(gate,T('schematic channel',30,BLUE).move_to([-3,-2.65,0]))
        ions=VGroup(*[chip(label,GREEN,30) for label in ['Na+','K+','Ca2+']])
        for i,ion in enumerate(ions):
            phase=i/3
            def flow(m,dt,phase=phase):
                m.move_to([-3,2.1-4.25*((self.elapsed()*.24+phase)%1),0])
            ion.add_updater(flow);flow(ion,0)
        self.add(ions)
        self.at('non selective cation')
        self.play(FadeIn(T('non-selective cation conductance',32,GREEN).move_to([0,-3.3,0])),run_time=.3)
        self.at('its current inactivated');self.play(Indicate(tr[1],scale_factor=1.03),run_time=.6);self.finish()


class S13Inactivation(SpokenScene):
    def construct(self):
        tr=trace(0,.65,10.8,3.25,tau=7.3);self.add(tr)
        self.at('Inactivation means');title=heading('Inactivation').shift(UP*.4);self.play(FadeIn(title),run_time=.3)
        self.at('the current decays');self.play(Indicate(tr[1],scale_factor=1.02),run_time=.5)
        self.at('while the stimulus')
        ax=tr[0];xs=[0,5,5,80];ys=[-2.75,-2.75,-2.1,-2.1]
        step=VMobject(color=YELLOW,stroke_width=5).set_points_as_corners([[ax.c2p(x,0)[0],y,0] for x,y in zip(xs,ys)])
        self.play(Create(step),FadeIn(T('probe held →',28,YELLOW).move_to([0,-3.3,0])),run_time=.5)
        self.at('Keep that word');self.play(Create(Underline(title,color=YELLOW)),run_time=.4);self.finish()


class S14Logic(SpokenScene):
    def construct(self):
        panels=claims();self.add(panels,heading('Three separate claims'))
        self.at('Silencing showed');target=claims(1)[0];self.play(FadeOut(panels[0]),run_time=.2);self.play(FadeIn(target),run_time=.3)
        self.at('Expression showed');target=claims(2)[1];self.play(FadeOut(panels[1]),run_time=.2);self.play(FadeIn(target),run_time=.3)
        self.at('Neither showed');self.play(Indicate(panels[2],scale_factor=1.03),FadeIn(T('2010: 2 of 3',36,GREEN).move_to([0,-2,0])),run_time=.6);self.finish()


class S15Authors(SpokenScene):
    def construct(self):
        self.add(claims(2).shift(UP*.75),heading('Three separate claims'))
        page=RoundedRectangle(width=10.3,height=2.55,corner_radius=.12,color=GREY).move_to([0,-1.95,0])
        title=T('2010 paper · schematic summary',28,GREY).move_to([0,-1.05,0])
        text=T('Possibly non-conducting subunits\nof some other channel',32).move_to([0,-2.1,0])
        self.add(page,title)
        self.at('They kept open')
        highlight=Rectangle(width=9.6,height=1.35,color=YELLOW,fill_color=YELLOW,fill_opacity=.12).move_to(text)
        self.play(FadeIn(highlight),FadeIn(text),run_time=.4);self.finish()


class S16Three(SpokenScene):
    def construct(self):
        panels=claims(2);self.add(panels,heading('Three separate claims'))
        self.at('three separate claims');self.play(Indicate(panels,scale_factor=1.015),run_time=.5)
        self.at('Each needs its own');self.play(FadeIn(T('Each claim needs its own experiment',32).move_to([0,-1.7,0])),run_time=.4)
        self.at('paper earned');self.play(FadeIn(chip('2010: 2 of 3',GREEN,36).move_to([0,-2.65,0])),run_time=.4);self.finish()


class S17Later(SpokenScene):
    def construct(self):
        panels=claims(2);self.add(panels,heading('Three separate claims').shift(UP*.3))
        self.at('earned the third');target=claims(3);target[2].set_color(GOLD)
        self.play(FadeOut(panels),FadeIn(target),run_time=.45)
        panels=target
        self.at('In 2012')
        earned=VGroup(chip('✓ Necessity',GREEN,26),chip('✓ Sufficiency',GREEN,26),chip('✓ Pore identity',GOLD,26)).arrange(RIGHT,buff=.5).move_to([0,2.2,0])
        self.play(FadeOut(panels),FadeIn(earned),run_time=.4)
        self.add(T('2012 · no cell\npurified protein',30,GOLD).move_to([-3.35,.75,0]))
        lip=Arc(radius=1.7,start_angle=PI/2+.28,angle=TAU-.56,arc_center=[3.2,-1.1,0],color=TEXT,stroke_width=10)
        block=RoundedRectangle(width=.94,height=.85,corner_radius=.1,color=BLUE,fill_color=BLUE,fill_opacity=.6).move_to([3.2,.55,0])
        self.at('purified');self.play(Create(lip),FadeIn(block),FadeIn(T('Piezo1',30,BLUE).move_to([5.25,.5,0])),Create(Line([4.5,.5,0],[3.7,.55,0],color=BLUE)),run_time=.4)
        self.at('formed ion channels');self.play(Indicate(block,color=GREEN),run_time=.4)
        self.at('artificial bilayers')
        membrane=VGroup(Line([-6,-1.1,0],[-3.85,-1.1,0],color=TEXT,stroke_width=10),Line([-2.85,-1.1,0],[-.7,-1.1,0],color=TEXT,stroke_width=10),RoundedRectangle(width=1,height=1.5,corner_radius=.1,color=BLUE,fill_color=BLUE,fill_opacity=.6).move_to([-3.35,-1.1,0]))
        self.play(FadeIn(membrane),FadeIn(T('Piezo1',30,BLUE).move_to([-3.35,-.1,0])),FadeIn(T('artificial bilayer',32,TEXT).move_to([-3.35,-3.3,0])),run_time=.35)
        self.at('and liposomes');self.play(FadeIn(T('liposome',32,TEXT).move_to([3.2,-3.3,0])),run_time=.3);self.finish()


class S18Pore(SpokenScene):
    def construct(self):
        model=trimer().scale(1.25).move_to([-1.7,-.35,0]);self.add(model,heading('Top view · schematic'))
        model[-1].add_updater(lambda m,dt: m.set_stroke(width=5+2*np.sin(self.elapsed()*2)**2))
        self.at('Structures then');self.play(Indicate(model[-1],color=GREEN),run_time=.5)
        self.at('carboxy terminal domains')
        label=T('Carboxy-terminal\ndomains',32,GOLD).move_to([3.6,1.2,0])
        leader=VGroup(*[Line([1.6,1.1,0],part[1].get_center(),color=GOLD,stroke_width=2) for part in model[:3]])
        self.play(FadeIn(label),Create(leader),*[part[1].animate.set_fill(GOLD,opacity=1) for part in model[:3]],run_time=.5)
        self.at('line a central')
        porelabel=T('central ion pore',30,GREEN).move_to([3.6,-1.2,0])
        self.play(FadeIn(porelabel),Create(Line([1.65,-1.2,0],model[-1].get_right(),color=GREEN)),run_time=.4)
        pulse=Circle(.29,color=GREEN,stroke_width=4).move_to(model[-1])
        pulse.add_updater(lambda m,dt: m.set_stroke(opacity=.45+.5*np.sin(self.elapsed()*2)**2))
        self.add(pulse);self.finish()


class S19Turn(SpokenScene):
    def construct(self):
        model=trimer().scale(1.25).move_to([-1.7,-.35,0]);self.add(model,heading('Top view · schematic'))
        model[-1].add_updater(lambda m,dt: m.set_stroke(width=5+2*np.sin(self.elapsed()*2)**2))
        self.at('protein is the channel');self.play(FadeIn(T('Piezo is the channel',32,BLUE).move_to([3.5,.1,0])),run_time=.35)
        self.at('a stranger question');self.play(*[FadeOut(m) for m in list(self.mobjects) if m is not model],run_time=.35)
        self.at('Why build so much');target=trimer(True).scale(.84).move_to([0,.65,0])
        target[-1].scale(1.7)
        for part in target[:3]: part[1].scale(1.35)
        self.play(Transform(model,target),run_time=1.1)
        self.at('around one central');self.play(FadeIn(T('Why so much protein\naround one central pore?',34,font=TITLE_FONT).move_to([0,-2.85,0])),run_time=.4);self.finish()


class S20Takeaway(SpokenScene):
    def construct(self):
        self.add(claims(3).shift(UP*.8),heading('Three separate claims'))
        self.at('Required')
        self.add(T('Inactivation',40,YELLOW,font=TITLE_FONT).move_to([0,-2.45,0]),
            T('Human PIEZO2 variants change inactivation',30,TEAL).move_to([0,-3.25,0]))
        self.play(FadeIn(T('Required, sufficient, and the pore itself.',32).move_to([0,-.95,0])),run_time=.3)
        self.at('Three claims');self.play(FadeIn(T('Three claims, three experiments.',36).move_to([0,-1.65,0])),run_time=.3)
        self.at('three experiments');self.finish()


class S21End(EndCard):
    LINE='Required, sufficient, and the pore itself. Three claims, three experiments.'
    def construct(self):
        self.add(T('Required, sufficient, and the pore itself.',36,font=TITLE_FONT).move_to([0,.65,0]),T('Three claims, three experiments.',38,font=TITLE_FONT).move_to([0,-.25,0]),T('biochemistrypedia.com',26,TEAL).move_to([0,-1.5,0]))
        self.finish()
