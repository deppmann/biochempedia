"""What the Cell Waits For — one cell, one checkpoint, one irreversible cut.
COLOR MAP: BLUE sisters/tension; ORANGE kinetochores/anaphase A;
TEAL cohesin; YELLOW poles/pulls/anaphase B; GREY spindle/envelopes;
RED empty/wait/errors; PURPLE APC/tags; GOLD securin; GREEN separase/GO;
PINK Aurora B. Cohesin belts are schematic cartoons, never molecular structures.
"""
from bp_style import *

ORANGE = '#F29E4C'
PURPLE = '#B58CD9'
PINK = '#E58AB0'


def label(words, x=0, y=3.12, color=TEXT, size=34, width=12.5):
    text = fit(T(words, size, color), max_w=width).move_to([x, y, 0])
    back = Rectangle(width=text.width+.16, height=text.height+.10, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(text)
    return VGroup(back,text).set_z_index(20)


def arrow(a, b, color=YELLOW):
    return Arrow(a, b, buff=0, color=color, stroke_width=6, tip_length=.2)


def sway(m, amplitude=.07, speed=1.25, axis=UP, phase=0):
    m._clock = phase
    def update(obj, dt):
        old = obj._clock
        obj._clock += dt * speed
        obj.shift(axis * amplitude * (np.sin(obj._clock) - np.sin(old)))
    m.add_updater(update)
    return m


class Pair(VGroup):
    def __init__(self, x=0, y=0, scale=1, arms=False):
        super().__init__()
        self.L = VGroup(RoundedRectangle(width=.29, height=1.45, corner_radius=.13,
            color=BLUE, fill_color=BLUE, fill_opacity=.68, stroke_width=3).shift(LEFT*.23),
            Dot([-.43, 0, 0], radius=.115, color=ORANGE))
        self.R = VGroup(self.L[0].copy().shift(RIGHT*.46), Dot([.43,0,0], radius=.115,color=ORANGE))
        self.kL, self.kR = self.L[1], self.R[1]
        self.rings = VGroup(*[Ellipse(width=.86,height=.28,color=TEAL,stroke_width=4).shift(UP*t) for t in [-.14,.14]])
        self.arms = VGroup(*[Ellipse(width=.86,height=.28,color=TEAL,stroke_width=4).shift(UP*t) for t in [-.52,.52]]) if arms else VGroup()
        self.add(self.L,self.R,self.rings,self.arms)
        self.scale(scale).move_to([x,y,0])
        self.set_z_index(4)

    def free(self, yes=True):
        self.kR.set_color(RED if yes else ORANGE)
        self.kR.clear_updaters()
        if yes:
            self.kR._t=0
            def pulse(m,dt):
                m._t+=dt
                m.set_opacity(.65+.35*(.5+.5*np.sin(m._t*4)))
            self.kR.add_updater(pulse)


def fibre(pole, kin, phase=0):
    g=VGroup(Line(pole.get_center(),kin.get_center(),color=GREY,stroke_width=2.8),
             Dot(radius=.045,color=TEXT))
    g._t=phase
    g.strength=1.0
    def live(m,dt):
        m._t+=dt
        a,b=pole.get_center(),kin.get_center()
        m[0].put_start_and_end_on(a,b).set_stroke(width=2.8+.7*np.sin(m._t*2),opacity=m.strength)
        m[1].move_to(a+(b-a)*((m._t*.33)%1)).set_opacity(.7*m.strength)
    g.add_updater(live)
    return g.set_z_index(0)


class Panel(VGroup):
    def __init__(self, count=1, human=False, go=False):
        super().__init__()
        self.clamp = VGroup(Line([2.9,2.48,0],[2.9,3.02,0],color=PURPLE,stroke_width=7),
            Line([2.9,3.02,0],[3.3,3.02,0],color=PURPLE,stroke_width=7),
            Line([2.9,2.48,0],[3.3,2.48,0],color=PURPLE,stroke_width=7))
        if go:
            self.clamp[1].rotate(.6,about_point=[2.9,3.02,0])
            self.clamp[2].rotate(-.6,about_point=[2.9,2.48,0])
        scene_number=int(os.environ.get('KX_SCENE_ID','s00').split('_')[0][1:])
        self.name=label('APC' if scene_number>=11 else 'anaphase brake',4.6,3.3,PURPLE,28,3.7)
        self.lamp=chip('GO' if go else 'WAIT',GREEN if go else RED,30).move_to([4.65,2.48,0])
        self.counter=label(f'attached: {92-count} of 92' if human else f'empty kinetochores: {count}',4.35,1.72,TEXT,28,4.6)
        back=RoundedRectangle(width=4.75,height=2.1,corner_radius=.16,stroke_width=0,fill_color=BG,fill_opacity=.96).move_to([4.3,2.55,0])
        self.add(back,self.clamp,self.name,self.lamp,self.counter)
        self.set_z_index(15)
        self.lamp._t=0
        def pulse(m,dt):
            m._t+=dt
            m[0].set_fill(opacity=.2+.2*(.5+.5*np.sin(m._t*3)))
        self.lamp.add_updater(pulse)

    def change(self, scene, count, human=False, go=False):
        dest=label(f'attached: {92-count} of 92' if human else f'empty kinetochores: {count}',4.35,1.72,TEXT,28,4.6)
        lamp=chip('GO' if go else 'WAIT',GREEN if go else RED,30).move_to([4.65,2.48,0])
        scene.play(Transform(self.counter,dest),Transform(self.lamp,lamp),run_time=.45)
        if go:
            scene.play(self.clamp[1].animate.rotate(.6,about_point=[2.9,3.02,0]),
                       self.clamp[2].animate.rotate(-.6,about_point=[2.9,2.48,0]),run_time=.35)


class World:
    def __init__(self, scene, state='bi', count=1, human=False, go=False, arms=False):
        self.scene=scene
        self.cell=Ellipse(width=12.8,height=5.65,color=GREY,stroke_width=3,
            fill_color=GREY,fill_opacity=.055).move_to([0,-.55,0]).set_z_index(-5)
        self.pl=Dot([-5.75,-.55,0],radius=.19,color=YELLOW)
        self.pr=Dot([5.75,-.55,0],radius=.19,color=YELLOW)
        self.panel=Panel(count,human,go)
        self.hero=Pair(0,.35,arms=arms)
        self.other=Pair(0,-1.65)
        self.stuck=Pair(-3.2,-.55)
        self.stuck.free(count>0)
        if state in ('syn','empty'):
            self.hero.shift(LEFT*1.3)
            self.hero.kR.move_to(self.hero.R[0].get_left())
        if state=='empty': self.hero.free()
        if state=='dead':
            self.stuck.kR.set_color(GREY)
        self.pairs=VGroup(self.stuck,self.hero,self.other)
        if human:
            self.pairs=VGroup()
            # Exactly 46 duplicated chromosomes, hence exactly 92 kinetochores.
            for i in range(46):
                row,col=divmod(i,8)
                p=Pair(-2.85+col*.80,1.0-row*.72,scale=.35)
                self.pairs.add(p)
            self.hero=self.pairs[19]
            self.other=self.pairs[28]
            self.stuck=self.pairs[0]
            self.hero.free(count>0)
        for i,p in enumerate(self.pairs): sway(p,amplitude=.06 if not human else .035,phase=i*.7)
        self.fibres=VGroup()
        self.links={}
        for i,p in enumerate(self.pairs):
            a=fibre(self.pl,p.kL,i*.31)
            if p is self.stuck and not human: b=None
            elif p is self.hero and state=='empty': b=None
            elif p is self.hero and human and count: b=None
            else: b=fibre(self.pl if p is self.hero and state=='syn' else self.pr,p.kR,i*.31+.5)
            self.fibres.add(a)
            if b is not None: self.fibres.add(b)
            self.links[id(p)]=[a,b]
        # Searching spindle tips extend and retract behind the carried chromosomes.
        self.search=VGroup()
        for i in range(6):
            ray=Line(ORIGIN,RIGHT,color=GREY,stroke_width=2,stroke_opacity=.5)
            ray._t=i*.8
            def probe(m,dt,i=i):
                m._t+=dt
                start=(self.pl if i%2==0 else self.pr).get_center()
                end=start+np.array([(1 if i%2==0 else -1)*(2+.9*np.sin(m._t*1.7)),(i//2-1)*.8,0])
                m.put_start_and_end_on(start,end)
            ray.add_updater(probe)
            self.search.add(ray)
        self.wave=VGroup()
        if count:
            source=self.hero if human or state=='empty' else self.stuck
            self.add_wave(source)
        scene.add(self.cell,self.search,self.fibres,self.pl,self.pr,self.pairs,self.panel,self.wave)

    def add_wave(self, source):
        for i in range(3):
            d=Dot(radius=.075,color=RED).set_z_index(10)
            d._t=i/3
            def wave(m,dt):
                m._t=(m._t+dt*.42)%1
                a=source.kR.get_center(); b=np.array([3.,2.5,0])
                m.move_to(a+(b-a)*m._t).set_opacity(.9*np.sin(np.pi*m._t))
            d.add_updater(wave)
            self.wave.add(d)

    def detach(self,p):
        link=self.links[id(p)][1]
        p.free()
        if link is not None:
            link.clear_updaters()
            self.scene.play(link.animate.scale(.05,about_point=self.pl.get_center()).set_opacity(0),run_time=.55)
            self.scene.remove(link)
        self.links[id(p)][1]=None

    def catch(self,p,go=False,human=False,count=1):
        p.free(False)
        p.kR.move_to(p.R[0].get_right())
        link=fibre(self.pr,p.kR)
        self.links[id(p)][1]=link
        self.fibres.add(link)
        self.scene.play(Create(link),run_time=.55)
        self.scene.play(FadeOut(self.wave),run_time=.2)
        self.wave.clear_updaters()
        self.wave=VGroup()
        if count: self.add_wave(self.stuck); self.scene.add(self.wave)
        self.panel.change(self.scene,count,human,go)

    def focus(self,p,arms=False,animate=True):
        others=VGroup(*[q for q in self.pairs if q is not p])
        p.clear_updaters(recursive=False)
        # The other chromosomes stay visible in a quiet context inset, never behind the hero.
        for q in others:
            for f in self.links[id(q)]:
                if f is not None: f.strength=.15
        scale=4.56/p.height
        if animate:
            self.scene.play(others.animate.scale(.4).move_to([-4.15,.85,0]).set_opacity(.4),
                self.cell.animate.set_stroke(opacity=.4),p.animate.scale(scale).move_to([-.6,-.45,0]),run_time=.8)
        else:
            others.scale(.4).move_to([-4.15,.85,0]).set_opacity(.4)
            self.cell.set_stroke(opacity=.4)
            p.scale(scale).move_to([-.6,-.45,0])
        sway(p,amplitude=.065)
        return p


def heading(scene, text, color=TEXT):
    t=label(text,-1.8,3.12,color,36,7.8)
    scene.play(FadeIn(t,shift=DOWN*.08),run_time=.35)
    return t


def tension(p, y=-3.02):
    g=VGroup()
    def redraw(m):
        a,b=p.kL.get_x(),p.kR.get_x()
        m.become(VGroup(Line([a,y,0],[b,y,0],color=BLUE,stroke_width=4),
            Line([a,y-.12,0],[a,y+.12,0],color=BLUE,stroke_width=4),
            Line([b,y-.12,0],[b,y+.12,0],color=BLUE,stroke_width=4)))
    g.add_updater(redraw)
    return g


def pulls(p,same=False):
    y=p.get_y()+.5
    return VGroup(arrow([p.kL.get_x()-.2,y,0],[p.kL.get_x()-1.3,y,0]),
        arrow([p.kR.get_x()+(.2 if not same else -.2),y+.55,0],
              [p.kR.get_x()+(1.3 if not same else -1.3),y+.55,0]))


def cloud(p):
    c=Ellipse(width=.55,height=.8,color=PINK,fill_color=PINK,fill_opacity=.4,stroke_width=0).move_to((p.kL.get_center()+p.kR.get_center())/2)
    sway(c,.12,1.5,RIGHT)
    return c.set_z_index(6)


def scissors():
    return VGroup(Line([-.25,-.2,0],[.25,.2,0],color=GREEN,stroke_width=6),
                  Line([-.25,.2,0],[.25,-.2,0],color=GREEN,stroke_width=6))


class S00Hook(SpokenScene):
    def construct(self):
        w=World(self)
        self.at('this cell')
        self.play(Indicate(w.pairs,color=BLUE,scale_factor=1.04),run_time=.6)
        self.at('each daughter')
        self.play(Indicate(w.hero.rings,color=TEAL),run_time=.6)
        self.at('but one chromosome')
        self.play(Flash(w.stuck.kR,color=RED,flash_radius=.35),run_time=.7)
        self.at('the whole cell waits')
        self.play(Indicate(w.panel.lamp,color=RED),run_time=.65)
        self.at('what is it waiting for')
        heading(self,'What is it waiting for?')
        self.finish()


class S01Title(TitleCard):
    TITLE='What the Cell Waits For'
    LESSON='Mitosis and Chromosome Segregation'
    def construct(self):
        w=World(self)
        title=label(self.TITLE,-1.5,3.12,TEXT,40,9)
        self.add(title)
        self.wait(max(.1,self.narration_s-.07))


class S02Parts(SpokenScene):
    def construct(self):
        w=World(self,arms=True)
        self.at('look closer')
        p=w.focus(w.hero)
        w.fibres.clear_updaters();w.search.clear_updaters()
        self.play(FadeOut(w.fibres),FadeOut(w.search),run_time=.4)
        self.at('2 sister chromatids')
        t=heading(self,'sister chromatids',BLUE)
        self.play(Indicate(VGroup(p.L,p.R),color=BLUE,scale_factor=1.03),run_time=.6)
        self.at('held by cohesin rings')
        self.play(Transform(t,label('cohesin',-1.8,3.12,TEAL,36,8.5)),Indicate(VGroup(p.rings,p.arms),color=TEAL),run_time=.7)
        self.at('each sister carries')
        labs=VGroup(label('kinetochore',-3.7,-.6,ORANGE,28,3),label('kinetochore',2.9,-.6,ORANGE,28,3))
        self.play(FadeIn(labs),Indicate(VGroup(p.kL,p.kR),color=ORANGE),run_time=.7)
        self.at('the 2 face opposite ways')
        self.play(FadeOut(labs),run_time=.2)
        self.play(GrowArrow(arrow(p.kL.get_center()+LEFT*.2,p.kL.get_center()+LEFT*1.0,ORANGE)),
                  GrowArrow(arrow(p.kR.get_center()+RIGHT*.2,p.kR.get_center()+RIGHT*1.,ORANGE)),run_time=.6)
        self.finish()


class S03Grip(SpokenScene):
    def construct(self):
        w=World(self,arms=True)
        p=w.focus(w.hero,animate=False)
        self.at('reach the kinetochores')
        self.play(w.fibres.animate.set_opacity(.25),run_time=.4)
        self.at('the goal is')
        h=heading(self,'biorientation',BLUE)
        self.play(w.fibres.animate.set_opacity(.5),run_time=.5)
        self.at('each sister gripped')
        a=pulls(p)
        self.play(FadeIn(a),run_time=.5)
        self.at('but both sisters')
        self.play(FadeOut(a),w.links[id(p)][1].animate.set_opacity(0),run_time=.3)
        w.links[id(p)][1].clear_updaters()
        self.remove(w.links[id(p)][1])
        b=fibre(w.pl,p.kR)
        w.fibres.add(b);self.add(b)
        self.play(p.kR.animate.move_to(p.R[0].get_left()),run_time=.3)
        self.play(p.animate.shift(LEFT*.65),Transform(h,label('same pole',-1.8,3.12,RED,36,8.5)),run_time=.8)
        self.at('that is')
        self.play(Transform(h,label('syntelic · error',-1.8,3.12,RED,36,8.5)),run_time=.5)
        self.finish()


class S04Rope(SpokenScene):
    def construct(self):
        w=World(self,'syn',arms=True)
        self.at('how can a cell')
        p=w.focus(w.other)
        self.at('sense force')
        a=pulls(p);self.play(FadeIn(a),run_time=.5)
        self.at('think of the pair')
        rope=DashedLine(p.kL.get_center(),p.kR.get_center(),color=TEXT,stroke_width=7,dash_length=.12)
        self.play(Create(rope),run_time=.4)
        h=heading(self,'rope picture',TEXT)
        self.at('pulled from opposite ends')
        self.play(FadeOut(rope),p.L.animate.shift(LEFT*.35),p.R.animate.shift(RIGHT*.35),p.rings.animate.stretch(1.3,0),run_time=1)
        self.at('it goes taut')
        b=tension(p);self.add(b)
        self.play(Transform(h,label('tension (schematic)',-1.8,3.12,BLUE,36,8.5)),run_time=.5)
        self.finish()


def syntelic_scene(scene,question=False):
    w=World(scene,'syn',arms=True);p=w.focus(w.hero,animate=False)
    a=pulls(p,True);scene.add(a,tension(p))
    if question: scene.add(label('Is it under tension?',-1.8,3.12,TEXT,36,8.5))
    return w,p,a


class S05Predict(SpokenScene):
    def construct(self):
        w=World(self,'syn',arms=True)
        self.at('now go back')
        p=w.focus(w.hero)
        self.at('both sisters are pulled')
        self.play(FadeIn(pulls(p,True)),p.animate.shift(LEFT*.2),run_time=.7)
        self.add(tension(p))
        self.at('is it under tension')
        heading(self,'Is it under tension?')
        self.finish()


class S06Hold(NarratedScene):
    def construct(self):
        syntelic_scene(self,True)
        self.wait(max(.1,self.narration_s-self.elapsed()-.07))


class S07Answer(SpokenScene):
    def construct(self):
        w,p,a=syntelic_scene(self)
        self.at('in the rope picture')
        h=heading(self,'little tension · rope picture',BLUE)
        rope=DashedLine(p.kL.get_center(),p.kR.get_center(),color=TEXT,stroke_width=5)
        self.play(Create(rope),run_time=.4)
        self.at('pulls drag the pair')
        self.play(p.animate.shift(LEFT*.3),rope.animate.shift(LEFT*.3),a.animate.shift(LEFT*.3),run_time=1)
        self.at('some load from other forces')
        self.play(FadeOut(rope),Transform(h,label('other forces can add load',-1.8,3.12,TEXT,34,8.5)),
            GrowArrow(arrow([-2,-2.8,0],[-2,-1.9,0],GREY)),run_time=.6)
        self.at('let go and try again')
        self.play(Wiggle(w.links[id(p)][1],scale_value=1.02,rotation_angle=.04),run_time=.7)
        self.finish()


class S08Aurora(SpokenScene):
    def construct(self):
        w=World(self,'syn',arms=True);p=w.focus(w.hero,animate=False)
        c=cloud(p);self.add(c)
        self.at('a kinase called')
        heading(self,'Aurora B',PINK)
        self.at('it phosphorylates')
        marks=VGroup(*[Dot(radius=.09,color=PINK).move_to(p.rings.get_center()) for _ in range(4)])
        self.add(marks)
        self.play(*[d.animate.move_to((p.kL if i%2==0 else p.kR).get_center()+UP*(i//2-.5)*.22) for i,d in enumerate(marks)],run_time=.8)
        self.at('weakening their grip')
        self.play(Wiggle(w.links[id(p)][1],rotation_angle=.04),run_time=.65)
        self.at('slack grips tend')
        w.detach(p);w.add_wave(p)
        w.panel.change(self,2)
        self.play(p.arms[0].animate.shift(DOWN*.7).set_opacity(0),p.arms[1].animate.shift(UP*.7).set_opacity(0),run_time=1)
        self.finish()


class S09Force(SpokenScene):
    def construct(self):
        w=World(self,'empty',2);p=w.focus(w.hero,animate=False);c=cloud(p);self.add(c)
        self.at('under tension')
        w.catch(p,count=1)
        self.play(p.L.animate.shift(LEFT*.25),p.R.animate.shift(RIGHT*.25),c.animate.set_opacity(.15),run_time=.7)
        self.add(tension(p));h=heading(self,'tension (schematic)',BLUE)
        self.at('force also steadies')
        self.play(w.links[id(p)][0][0].animate.set_stroke(width=5),w.links[id(p)][1][0].animate.set_stroke(width=5),run_time=.6)
        self.at('so taut grips tend to stay')
        self.play(Transform(h,label('taut grips tend to stay',-1.8,3.12,BLUE,34,8.5)),run_time=.5)
        self.finish()


class S10Idea(SpokenScene):
    def construct(self):
        w=World(self)
        self.at('here is the whole rule')
        self.at('keep what is pulled')
        h=heading(self,'Keep the taut',BLUE)
        self.play(Indicate(VGroup(w.hero,w.other),color=BLUE,scale_factor=1.04),run_time=.5)
        self.at('remake what is not')
        h2=label('Remake the slack',-3.25,2.5,PINK,30,5.8)
        self.play(FadeIn(h2),Wiggle(w.links[id(w.stuck)][0],rotation_angle=.04),run_time=.5)
        self.at('and cut only when')
        h3=label('Cut only when none is empty',-2.4,-3.43,RED,30,8.6)
        self.play(FadeIn(h3),Indicate(w.panel.lamp,color=RED),run_time=.6)
        self.finish()


class S11Empty(SpokenScene):
    def construct(self):
        w=World(self)
        self.at('turning over a wrong grip')
        self.play(Wiggle(w.links[id(w.hero)][1],rotation_angle=.03),run_time=.5)
        self.at('leave its kinetochore empty')
        w.detach(w.hero)
        w.panel.change(self,2)
        w.catch(w.hero,count=1)
        self.at('empty means without enough')
        p=w.focus(w.stuck)
        side=Line([-5,p.kR.get_y(),0],[1,p.kR.get_y(),0],color=GREY,stroke_width=3)
        self.play(Create(side),run_time=.5)
        heading(self,'empty: no end-on grip',RED)
        self.at('an empty kinetochore sends')
        self.play(Flash(p.kR,color=RED,flash_radius=.5),run_time=.6)
        self.at('it holds back')
        self.play(Transform(w.panel.name,label('APC',4.6,3.3,PURPLE,30,3.7)),run_time=.4)
        self.add(label('anaphase-promoting complex',0,-3.4,PURPLE,30,11))
        self.finish()


class S12Laser(SpokenScene):
    def construct(self):
        w=World(self)
        self.at('while even 1 is empty')
        self.play(Indicate(w.panel.lamp,color=RED),run_time=.5)
        self.at('in a stuck rat kangaroo cell')
        heading(self,'PtK1 cell · 1995',TEXT)
        self.at('destroyed that 1 empty kinetochore')
        laser=Line([-4.5,2.1,0],w.stuck.kR.get_center(),color=TEXT,stroke_width=4)
        self.play(Create(laser),run_time=.35)
        self.play(Flash(w.stuck.kR,color=TEXT),run_time=.4)
        w.stuck.kR.clear_updaters();w.stuck.kR.set_color(GREY)
        self.play(FadeOut(laser),FadeOut(w.wave),run_time=.25)
        self.add(label('destroyed',-3.2,-1.7,GREY,28,3))
        w.panel.change(self,0)
        self.at('about 20 minutes later')
        clock=Circle(radius=.35,color=TEXT).move_to([1.3,2.6,0])
        hand=Line(clock.get_center(),clock.get_center()+UP*.28,color=TEXT)
        self.add(clock,hand,label('about 20 min later',0,-3.43,TEXT,32))
        self.play(Rotate(hand,-TAU,about_point=clock.get_center()),run_time=1.2)
        self.at('anaphase began')
        w.panel.change(self,0,go=True)
        self.finish()


class S13Meaning(SpokenScene):
    def construct(self):
        w=World(self,'dead',0,go=True)
        self.at('the damaged chromosome')
        mid=DashedLine([0,-2.9,0],[0,2.1,0],color=TEXT,stroke_width=2)
        self.play(Create(mid),run_time=.5)
        h=heading(self,'middle',TEXT)
        self.at('never reached the middle')
        gap=DoubleArrow([-2.6,-2.7,0],[-.1,-2.7,0],color=GREY,buff=0)
        self.play(GrowArrow(gap),run_time=.6)
        self.at('not waiting for alignment')
        self.play(Transform(h,label('alignment is not the signal',-1.8,3.12,TEXT,34,8.5)),run_time=.5)
        self.at('in or near')
        halo=Circle(radius=.4,color=RED,stroke_width=4).move_to(w.stuck.kR)
        self.play(Create(halo),Transform(h,label('signal source: in or near',-1.8,3.12,RED,32,8.5)),run_time=.6)
        self.finish()


class S14Predict(SpokenScene):
    def construct(self):
        w=World(self,human=True)
        self.at('a human cell')
        h=heading(self,'human cell · schematic')
        self.at('92 kinetochores')
        self.play(Indicate(w.pairs,color=BLUE,scale_factor=1.02),run_time=.5)
        self.at('91 are attached')
        self.play(Indicate(w.panel.counter,color=BLUE),run_time=.5)
        self.at('1 is empty')
        self.play(Flash(w.hero.kR,color=RED,flash_radius=.3),run_time=.6)
        self.at('does the cell go')
        self.play(Transform(h,label('Does the cell go?',-1.8,3.12,TEXT,36,8.5)),run_time=.4)
        self.finish()


class S15Hold(NarratedScene):
    def construct(self):
        World(self,human=True)
        self.add(label('Does the cell go?',-1.8,3.12,TEXT,36,8.5))
        self.wait(max(.1,self.narration_s-.07))


class S16Answer(SpokenScene):
    def construct(self):
        w=World(self,human=True)
        self.at('now')
        h=heading(self,'WAIT',RED)
        self.at('1 in 92')
        bar=VGroup(*[Rectangle(width=.075,height=.16,color=BLUE if i<91 else RED,
            fill_color=BLUE if i<91 else RED,fill_opacity=1,stroke_width=0).move_to([-4.4+i*.080,-3.2,0]) for i in range(92)])
        self.play(FadeIn(bar),run_time=.6)
        self.add(label('about 1.1%',4.8,-3.2,RED,30,3))
        self.at('a majority vote')
        vote=label('majority vote',-1.8,2.4,TEXT,30,8)
        cross=Line(vote.get_left()+LEFT*.1,vote.get_right()+RIGHT*.1,color=RED,stroke_width=5)
        self.play(FadeIn(vote),Create(cross),run_time=.5)
        self.at('the checkpoint works')
        self.play(FadeOut(vote),FadeOut(cross),run_time=.3)
        self.at('any empty kinetochore')
        self.play(Indicate(w.panel.lamp,color=RED),run_time=.5)
        # The answer lands before the last attachment turns off its signal.
        self.wait(.6)
        w.catch(w.hero,human=True,count=0)
        self.finish()


def enzymes(scene,p):
    sep=chip('separase',GREEN,30).move_to([2.8,-1.9,0])
    sep[0].set_opacity(.4)
    sec=chip('securin',GOLD,30).move_to([2.8,-1.05,0])
    inactive=label('inactive',2.8,-2.65,RED,28,3)
    scene.add(sep,sec,inactive)
    return sep,sec,inactive


class S17Cut(SpokenScene):
    def construct(self):
        w=World(self,human=True,count=0)
        p=w.focus(w.hero,animate=False)
        sep,sec,status=enzymes(self,p)
        self.at('when none is empty')
        w.panel.change(self,0,human=True,go=True)
        self.at('comes off')
        apc=chip('APC',PURPLE,30).move_to([3.0,2.2,0]);self.add(apc)
        self.play(apc.animate.move_to([1.8,-.15,0]),run_time=.7)
        self.at('it tags securin')
        tags=VGroup(*[Square(side_length=.15,color=PURPLE,fill_color=PURPLE,fill_opacity=1).move_to(apc) for _ in range(3)])
        self.add(tags)
        self.play(*[t.animate.move_to([2.45+i*.32,-.88,0]) for i,t in enumerate(tags)],run_time=.65)
        self.at('securin had kept')
        self.play(Indicate(VGroup(sec,sep),color=GOLD,scale_factor=1.04),run_time=.6)
        self.at('now separase is free')
        fragments=VGroup(*[Square(side_length=.13,color=GOLD,fill_color=GOLD,fill_opacity=1).move_to(sec.get_center()+RIGHT*(i-2)*.2) for i in range(5)])
        self.remove(sec);self.add(fragments)
        self.play(*[f.animate.shift([.35*(i-2),.6,0]).set_opacity(0) for i,f in enumerate(fragments)],FadeOut(tags),
            sep.animate.set_opacity(1),Transform(status,label('active',2.8,-2.5,GREEN,28,3)),run_time=.8)
        self.finish()


def cut_focus(scene,animate=True):
    w=World(scene,count=0,human=True,go=True)
    p=w.focus(w.hero,animate=animate)
    sep=scissors().move_to([2,-1.5,0]);scene.add(sep)
    return w,p,sep


def open_rings(scene,p,sep):
    # A visible gap is cut in a schematic belt, not an atomistic protein drawing.
    pieces=VGroup()
    for ring in p.rings:
        c=ring.get_center();a=ring.width/2;b=ring.height/2
        arc=ParametricFunction(lambda t,c=c,a=a,b=b:c+np.array([a*np.cos(t),b*np.sin(t),0]),
            t_range=[.45,TAU-.45],color=TEAL,stroke_width=5).set_z_index(6)
        scene.play(sep.animate.move_to(c+RIGHT*a),run_time=.3)
        scene.play(ReplacementTransform(ring.copy(),arc),ring.animate.set_opacity(0),run_time=.35)
        pieces.add(arc)
    return pieces


class S18Ring(SpokenScene):
    def construct(self):
        self.at('separase is a protease')
        w,p,sep=cut_focus(self)
        h=heading(self,'separase',GREEN)
        self.at('it cuts 1 subunit')
        self.play(Transform(h,label('one subunit',-1.8,3.12,TEAL,36,8.5)),sep.animate.move_to(p.rings[0].get_right()),run_time=.35)
        self.at('and the ring opens')
        pieces=open_rings(self,p,sep)
        self.at('in vertebrates')
        ghost=VGroup(*[Ellipse(width=p.rings.width,height=.3,color=TEAL,stroke_opacity=.4).move_to(p.get_center()+UP*y) for y in [-1.5,1.5]])
        self.play(FadeIn(ghost),run_time=.35)
        self.at('mainly at the centromere')
        self.play(FadeOut(ghost),Transform(h,label('mainly centromere',-1.8,3.12,TEAL,36,8.5)),run_time=.6)
        self.finish()


class S19Oneway(SpokenScene):
    def construct(self):
        w,p,sep=cut_focus(self,animate=False)
        self.remove(sep)
        for r in p.rings:r.set_opacity(0)
        halves=VGroup(Arc(radius=1.3,start_angle=.3,angle=PI-.6,color=TEAL,stroke_width=6).stretch(.3,1).move_to([-.6,-.15,0]),
            Arc(radius=1.3,start_angle=PI+.3,angle=PI-.6,color=TEAL,stroke_width=6).stretch(.3,1).move_to([-.6,-.8,0]))
        self.add(halves)
        self.at('a cut ring cannot be rejoined')
        h=heading(self,'cannot be rejoined',RED)
        back=DashedLine([1,-.1,0],[1,-.8,0],color=TEXT)
        cross=VGroup(Line([.7,-.7,0],[1.3,-.2,0],color=RED,stroke_width=5),Line([.7,-.2,0],[1.3,-.7,0],color=RED,stroke_width=5))
        self.play(Create(back),Create(cross),halves[0].animate.shift(UP*.15),halves[1].animate.shift(DOWN*.15),run_time=.6)
        self.at('in a normal cycle')
        forward=arrow([-4,-3.05,0],[3.7,-3.05,0],TEXT)
        self.play(GrowArrow(forward),run_time=.5)
        self.at('only as dna is copied')
        tag=label('next S phase: new sisters',-.5,-2.5,TEXT,30,9)
        self.play(FadeIn(tag),p.L.animate.shift(LEFT*.4),p.R.animate.shift(RIGHT*.4),run_time=.65)
        self.finish()


def split_all(scene,w,lag=False,run_time=1.5,near=False):
    anim=[]
    for i,p in enumerate(w.pairs):
        p.clear_updaters()
        anim.extend([p.rings.animate.set_opacity(0),p.L.animate.move_to([(-1.5 if near else -4.1)+(i%4)*.22,p.L.get_y(),0])])
        if not (lag and p is w.hero): anim.append(p.R.animate.move_to([(1.0 if near else 3.5)+(i%4)*.22,p.R.get_y(),0]))
    scene.play(*anim,run_time=run_time)


def nuclei(scene):
    g=VGroup(*[Ellipse(width=2.9,height=4.5,color=GREY,stroke_width=3,fill_color=GREY,fill_opacity=.08).move_to([x,-.65,0]) for x in [-3.8,3.8]])
    scene.play(Create(g),run_time=.8)
    return g


class S20Move(SpokenScene):
    def construct(self):
        w=World(self,human=True,count=0,go=True)
        self.at('the sisters part')
        split_all(self,w,near=True)
        self.at('in anaphase a')
        h=heading(self,'anaphase A · schematic',ORANGE)
        brackets=VGroup(Line([-5.7,-2.95,0],[-1.1,-2.95,0],color=ORANGE,stroke_width=5),Line([1.1,-2.95,0],[5.7,-2.95,0],color=ORANGE,stroke_width=5))
        self.add(brackets)
        self.at('each moves toward its pole')
        self.play(brackets[0].animate.put_start_and_end_on([-5.7,-2.95,0],[-3.7,-2.95,0]),
            brackets[1].animate.put_start_and_end_on([3.7,-2.95,0],[5.7,-2.95,0]),
            *[p.L.animate.shift(LEFT*2.6) for p in w.pairs],
            *[p.R.animate.shift(RIGHT*2.5) for p in w.pairs],run_time=.8)
        self.at('in anaphase b')
        self.play(FadeOut(brackets),Transform(h,label('anaphase B · schematic',-1.8,3.12,YELLOW,34,8.5)),run_time=.35)
        b=DoubleArrow([-5.7,-3.0,0],[5.7,-3.,0],color=YELLOW,buff=0);self.add(b)
        self.at('the poles themselves move apart')
        self.play(w.pl.animate.shift(LEFT*.35),w.pr.animate.shift(RIGHT*.35),b.animate.stretch(1.06,0),run_time=.8)
        self.finish()


class S21Blind(SpokenScene):
    def construct(self):
        w=World(self,human=True,count=0,go=True)
        originals=[p.copy() for p in w.pairs]
        for i,p in enumerate(w.pairs):
            p.clear_updaters();p.rings.set_opacity(0)
            p.L.move_to([-4.1+(i%4)*.22,p.L.get_y(),0])
            p.R.move_to([3.5+(i%4)*.22,p.R.get_y(),0])
        w.pl.shift(LEFT*.35);w.pr.shift(RIGHT*.35)
        self.at('1 error slips through')
        h=heading(self,'rewind')
        self.play(*[Transform(p,old) for p,old in zip(w.pairs,originals)],
            w.pl.animate.shift(RIGHT*.35),w.pr.animate.shift(LEFT*.35),run_time=.9)
        for i,p in enumerate(w.pairs):sway(p,amplitude=.035,phase=i*.7)
        self.at('sometimes 1 kinetochore')
        p=w.focus(w.hero)
        extra=fibre(w.pl,p.kR);self.add(extra)
        self.at('gripped from both poles')
        self.play(Indicate(p.kR,color=ORANGE,scale_factor=1.3),run_time=.6)
        self.play(Transform(h,label('merotelic',-1.8,3.12,RED,36,8.5)),run_time=.4)
        self.at('it is attached')
        self.play(Transform(w.panel.counter,label('empty kinetochores: 0',4.35,1.72,TEXT,28,4.6)),run_time=.4)
        self.at('the pair is partly under tension')
        self.add(tension(p));self.add(label('partial tension · schematic',0,-3.4,BLUE,30,11))
        c=cloud(p);self.add(c)
        self.at('can miss it')
        self.play(c.animate.set_opacity(.15),run_time=.5)
        self.finish()


class S22Lag(SpokenScene):
    def construct(self):
        w=World(self,human=True,count=0,go=True)
        original=[p.copy() for p in w.pairs]
        w.focus(w.hero,animate=False)
        extra=fibre(w.pl,w.hero.kR);self.add(extra)
        self.at('anaphase can start')
        self.play(*[Transform(p,old) for p,old in zip(w.pairs,original)],run_time=.8)
        for f in w.fibres:f.strength=1.0
        split_all(self,w,True)
        self.at('that kinetochore is pulled')
        a=VGroup(arrow(w.hero.kR.get_center()+LEFT*.2,w.hero.kR.get_center()+LEFT*1.3),
            arrow(w.hero.kR.get_center()+RIGHT*.2,w.hero.kR.get_center()+RIGHT*1.3))
        self.play(FadeIn(a),run_time=.5)
        self.at('its chromatid can lag')
        heading(self,'can lag',RED)
        self.play(w.hero.R.animate.scale(2.4),run_time=.5)
        nuclei(self)
        self.finish()


class S23Fate(SpokenScene):
    def construct(self):
        w=World(self,human=True,count=0,go=True)
        # Rebuild the preceding scene's final positions without replaying its action.
        for i,p in enumerate(w.pairs):
            p.clear_updaters();p.rings.set_opacity(0)
            p.L.move_to([-4.1+(i%4)*.22,p.L.get_y(),0])
            if p is not w.hero:p.R.move_to([3.5+(i%4)*.22,p.R.get_y(),0])
        w.hero.R.scale(2.4)
        n=VGroup(*[Ellipse(width=2.9,height=4.5,color=GREY,stroke_width=3,fill_color=GREY,fill_opacity=.08).move_to([x,-.65,0]) for x in [-3.8,3.8]])
        self.add(n)
        self.at('in 2 human cell lines')
        h=heading(self,'two human cell lines')
        self.at('most lagging chromosomes')
        late=w.hero.R
        late.set_opacity(.8)
        alternate=late.copy().set_opacity(.45);self.add(alternate)
        self.play(late.animate.move_to([3.4,-.6,0]),run_time=.9)
        self.play(Transform(h,label('most rejoin',-1.8,3.12,BLUE,36,8.5)),run_time=.4)
        self.at('a minority ended up')
        self.add(label('alternative outcomes',0,-3.4,TEXT,30,11))
        small=Ellipse(width=1.05,height=1.5,color=GREY,stroke_width=3).move_to(alternate)
        self.play(Create(small),run_time=.7)
        self.at('small separate nucleus')
        self.add(label('micronucleus',0,1.3,RED,30,5))
        self.finish()


class S24Return(SpokenScene):
    def construct(self):
        w=World(self,'syn')
        self.at('the checkpoint never reads')
        h=heading(self,'attached ≠ error-free',TEXT)
        self.at('tension sorts the grips')
        w.detach(w.hero)
        w.panel.change(self,2)
        self.at('taught ones tend to stay')
        self.play(Indicate(w.other,color=BLUE,scale_factor=1.12),run_time=.6)
        self.at('slack ones are remade')
        c=cloud(w.hero);self.add(c)
        w.catch(w.hero,count=1)
        self.play(FadeOut(c),run_time=.2)
        self.at('it just waits until')
        w.catch(w.stuck,count=0,go=True)
        self.at('then 1 cut')
        sep=scissors().move_to(w.hero.rings)
        self.add(sep)
        self.play(Wiggle(sep),w.hero.rings.animate.set_opacity(0),run_time=.5)
        self.play(FadeOut(sep),run_time=.15)
        split_all(self,w,run_time=1.0)
        self.at('part for good')
        nuclei(self)
        self.finish()


class S25End(EndCard):
    LINE='Keep taut grips, remake slack ones, cut when none is empty.'
