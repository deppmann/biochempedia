"""Same Cue, Opposite Answers — schematic, qualitative anatomy and turning assays.

COLOR MAP: TEAL neurons/growth cones; YELLOW Sema3A; BLUE neuropilin;
PURPLE plexin; ORANGE adhesion/GTPases; GOLD cGMP/guanylate cyclase;
GREEN response; RED blocked/lost; GREY anatomy. BLUE also denotes the
explicitly separate cAMP/netrin inset; RED pain / BLUE muscle in the callback.
No quantitative traces: the paths below depict anatomy and qualitative outcomes.
"""
from bp_style import *
import importlib.util
from pathlib import Path
import numpy as np

_spec = importlib.util.spec_from_file_location('sema_reference', Path(__file__).resolve().parent.parent / 'scenes.old.py')
_ref = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_ref)
fan, filopodia, path = _ref.fan, _ref.filopodia, _ref.path


def label(s, y=3.2, color=TEXT, size=32):
    return T(s, size, color).move_to([0, y, 0])


def plate(s, x, y, color=TEXT, size=28):
    t = T(s, size, color).move_to([x, y, 0])
    b = BackgroundRectangle(t, color=BG, fill_opacity=.96, buff=.12)
    return VGroup(b, t)


def cone(c=(-2, 0, 0), r=2.5, angle=0):
    g = VGroup(fan(-.85, .85, r, c), filopodia(-.85, .85, r, c))
    return g.rotate(angle, about_point=np.array(c))


def assay(state='neutral', raised=False, question=False):
    c = np.array({'neutral': [-2, 0, 0], 'away': [-1.8, -.35, 0],
                  'toward': [-1.8, .35, 0]}[state])
    angle = {'neutral': 0, 'away': -.36, 'toward': .36}[state]
    gc = cone(c, angle=angle)
    stem = path([[-5.1, 0, 0], [-3.1, 0, 0], c], width=22).set_opacity(.65)
    pip = Polygon([3.5, 2.45, 0], [5.8, 2.8, 0], [5.8, 3.2, 0],
                  color=GREY, fill_color=GREY, fill_opacity=.25)
    # Qualitative widening plume; density fades with distance from the tip.
    cloud = VGroup(*[Polygon([3.5,2.45,0], [3.5-.26*i,2.45-.04*i,0],
                             [3.5-.26*i,2.45-.28*i,0], stroke_width=0,
                             fill_color=YELLOW, fill_opacity=.035) for i in range(1,8)])
    source = VGroup(pip, cloud,
                   T('more Sema3A',28,YELLOW).move_to([4.5,1.95,0]),
                   T('less',28,YELLOW).move_to([3.0,-.65,0]))
    # Meter stays inside the growth cone as the entire receiving tip turns.
    meter = VGroup(T('cGMP',28,GOLD).move_to([-.45,.48,0]),
                   RoundedRectangle(width=1.35,height=.26,corner_radius=.06,color=GOLD).move_to([-.45,0,0]),
                   Rectangle(width=1.23 if raised else .20,height=.16,stroke_width=0,
                             fill_color=GOLD,fill_opacity=1).move_to([-.45 if raised else -.96,0,0]))
    meter.rotate(angle,about_point=np.array([-2,0,0])).shift(c-np.array([-2,0,0]))
    q = label('Away, ignore, or something else?',-3.25,size=34) if question else VGroup()
    return VGroup(stem,gc),source,meter,q


def outcome(which):
    if which == 'away':
        return plate('repulsion',1.95,-2.8,GREEN,32)
    return VGroup(plate('attraction',3.65,.45,GREEN,32),
                  Line([2.45,.6,0],[1.12,1.25,0],color=GREEN))


def repulsion_ghost():
    # A trajectory, rather than a second translucent growth cone.
    return DashedVMobject(path([[-3.1,0,0],[-1.8,-.35,0],[.55,-1.25,0]],
                              color=GREY,width=3),num_dashes=22).set_opacity(.6)


def revealed():
    a,s,m,_=assay('toward',True)
    ghost=repulsion_ghost()
    return VGroup(ghost,a,s,m,outcome('toward'),
                  label('The gradient did not change.\nThe reader did.',-3.15,size=30))


def cortex(axon=False,dendrite=False,enzyme=False):
    slab=Rectangle(width=11.7,height=5.6,color=GREY,stroke_width=2,
                   fill_color=GREY,fill_opacity=.035).move_to([0,-.1,0])
    surf=Line([-5.85,2.7,0],[5.85,2.7,0],color=GREY,stroke_width=5)
    pia=label('pial surface · outer surface of the brain',3.25,GREY,28)
    base=VGroup(slab,surf,pia)
    shading=VGroup(*[Rectangle(width=11.6,height=.48,stroke_width=0,fill_color=YELLOW,
                               fill_opacity=.24*(1-i/10)).move_to([0,2.44-i*.48,0]) for i in range(10)])
    cue=VGroup(shading,plate('Sema3A high',-4.15,2.13,YELLOW,28),
               plate('low',-4.75,-2.3,YELLOW,28),
               Arrow([-5.3,1.55,0],[-5.3,-1.8,0],color=YELLOW,buff=0,stroke_width=3))
    soma=Polygon([-.65,-.85,0],[.65,-.85,0],[0,.25,0],color=TEAL,
                 fill_color=TEAL,fill_opacity=.4)
    basal=VGroup(*[path([[x*.25,-.65,0],[x*.65,-.9,0],[x*1.25,-.65,0]],width=6) for x in [-1,1]])
    soma=VGroup(soma,basal)
    ax=VGroup(path([[0,-.85,0],[.06,-1.4,0],[-.12,-2.15,0],[0,-2.65,0]],width=9),
              Arrow([0,-2.2,0],[0,-2.72,0],color=TEAL,buff=0,stroke_width=6))
    dend=VGroup(Polygon([-.16,.12,0],[.16,.12,0],[.09,2.2,0],[-.09,2.2,0],
                       color=TEAL,fill_color=TEAL,fill_opacity=.7),
                *[path([[0,1.25,0],[x*.4,1.85,0],[x*.85,2.35,0]],width=6) for x in [-1,1]],
                Arrow([0,1.9,0],[0,2.45,0],color=TEAL,buff=0,stroke_width=6))
    axlab=VGroup(plate('axon · away',2.7,-1.5,TEAL,30),Line([1.25,-1.5,0],[-.03,-1.8,0],color=TEAL))
    dlab=VGroup(plate('apical dendrite · toward',3.2,.85,TEAL,28),Line([1.1,.85,0],[.2,1.1,0],color=TEAL))
    neuron=VGroup(soma,ax if axon else VGroup(),dend if dendrite else VGroup(),
                  axlab if axon else VGroup(),dlab if dendrite else VGroup())
    glow=VGroup(*[Line([0,.25,0],[0,2.22,0],color=GOLD,stroke_width=w).set_opacity(o)
                  for w,o in [(40,.09),(25,.19),(12,.8)]])
    enz=VGroup(glow,plate('soluble guanylate\ncyclase',-3.05,.65,GOLD,28),
               Line([-1.35,.7,0],[-.18,1.25,0],color=GOLD,stroke_width=3),
               VGroup(plate('little or none',2.3,-2.4,GREY,26),
                      Line([1.05,-2.4,0],[.18,-2.4,0],color=GREY)))
    return base,cue,neuron,enz


def rule_card(active=0):
    lines=['1  Receptor and its level','2  Internal state','3  Layout and dose']
    rows=VGroup()
    for i,s in enumerate(lines,1):
        box=RoundedRectangle(width=4.85,height=.78,corner_radius=.12,
                             color=GOLD if i==active else GREY,
                             fill_color=GOLD if i==active else BG,fill_opacity=.15 if i==active else 1)
        t=T(s,27,GOLD if i==active else TEXT)
        rows.add(VGroup(box,t).move_to([3.7,1.45-(i-1)*1.05,0]))
    return rows


def rule_block():
    return VGroup(T('The cue marks the place.',28,YELLOW),
                  T('The growth cone decides\nwhat it means.',28,TEXT)).arrange(DOWN,buff=.24).move_to([3.6,-2.45,0])


def spinal():
    # A large cord on the left reserves the right side for the persistent card.
    anatomy,cue,p,pl,m,ml=_ref.spinal()
    diagram=VGroup(anatomy,cue,p,m).scale(.86).move_to([-2.9,0,0])
    pl=plate('pain fibre',-4.55,1.65,RED,28)
    ml=plate('muscle afferent',-.65,1.65,BLUE,28)
    # Redraw routes so the stopping/entering distinction is explicit at the cue border.
    p.become(path([[-6.1,.8,0],[-4.8,.8,0],[-4.25,.2,0],[-4.25,-.15,0]],RED,9))
    m.become(path([[.25,.8,0],[-1,.8,0],[-1.6,.1,0],[-2,-1.0,0]],BLUE,9))
    # Replace scaled labels to preserve readable type.
    anatomy[2].become(T('dorsal',26,GREY).move_to([-2.9,2.55,0]))
    anatomy[3].become(T('ventral horn',26,GREY).move_to([-2.9,-2.85,0]))
    cue[0].become(RoundedRectangle(width=3.5,height=1.7,corner_radius=.12,color=YELLOW,
                                  fill_color=YELLOW,fill_opacity=.12).move_to([-2.9,-1,0]))
    cue[1].become(T('Sema3A',28,YELLOW).move_to([-3.25,-1.45,0]))
    return VGroup(anatomy,cue),VGroup(p,pl),VGroup(m,ml)


class S00Title(TitleCard):
    LESSON='Semaphorins and Repulsion'
    TITLE='Same Cue, Opposite Answers'
    def construct(self):
        self.add(label('BIOCHEMISTRYPEDIA',1.55,TEAL,26),
                 label(self.LESSON.upper(),.8,GREY,28),
                 label(self.TITLE,-.15,size=46),
                 Line([-1.2,-.95,0],[1.2,-.95,0],color=GOLD,stroke_width=4))
        self.finish()


class S01Question(SpokenScene):
    def construct(self):
        a,s,_,_=assay()
        self.add(a,s,label('Fixed, or set by the growth cone?',-3.25,size=34))
        self.at('Is repulsion')
        self.play(Indicate(s[2],scale_factor=1.04),run_time=.5)
        self.at('Or can the growth cone')
        self.play(Indicate(a[1],scale_factor=1.03,color=TEAL),run_time=.6)
        self.finish()


class S02Setup(SpokenScene):
    def construct(self):
        a,_,_,_=assay()
        dish=RoundedRectangle(width=12.3,height=5.3,corner_radius=.6,color=GREY).shift(UP*.1)
        soma=Circle(.48,color=TEAL,fill_color=TEAL,fill_opacity=.4).move_to([-5.1,0,0])
        self.add(dish,soma,a)
        self.at('and colleagues')
        text=label('Song, Poo and colleagues · 1998\nOne cultured Xenopus spinal neuron',-3.25,TEAL,27)
        self.play(FadeIn(text),run_time=.45)
        self.finish()


class S03Pipette(SpokenScene):
    def construct(self):
        a,s,_,_=assay()
        self.add(a)
        self.at('A fine pipette')
        self.play(FadeIn(s[0]),run_time=.6)
        self.at('a small gradient')
        self.play(FadeIn(s[1]),run_time=.65)
        self.at('beside one growth cone')
        self.play(FadeIn(s[2:]),run_time=.5)
        self.at('turned away')
        self.play(Transform(a,assay('away')[0]),FadeIn(outcome('away')),run_time=.85)
        self.finish()


class S04Q(SpokenScene):
    def construct(self):
        a,s,low,q=assay(question=True)
        self.add(a,s)
        self.at('Now raise')
        self.play(FadeIn(low),run_time=.45)
        self.at('inside the growth cone')
        self.play(Transform(low,assay(raised=True)[2]),run_time=1.15)
        self.at('Same pipette')
        self.play(Indicate(s[0],scale_factor=1.03),run_time=.4)
        self.at('same gradient')
        self.play(Indicate(s[1],scale_factor=1.03),run_time=.4)
        self.at('What happens')
        self.play(FadeIn(q),run_time=.45)
        self.finish()


class S05Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(*assay(raised=True,question=True))
        self.wait(5)


class S06Reveal(SpokenScene):
    def construct(self):
        a,s,m,q=assay(raised=True,question=True)
        self.add(a,s,m,q)
        self.at('turned toward')
        ghost=repulsion_ghost()
        target,_,tm,_=assay('toward',True)
        self.play(FadeOut(q),FadeIn(ghost),Transform(a,target),Transform(m,tm),run_time=.85)
        self.play(FadeIn(outcome('toward')),run_time=.35)
        self.at('The gradient did not change')
        caption=label('The gradient did not change.',-2.9,size=30)
        self.play(FadeIn(caption),run_time=.4)
        self.at('The reader did')
        self.play(FadeIn(label('The reader did.',-3.45,size=30)),run_time=.4)
        self.finish()


class S07Beat(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(revealed())
        self.wait(2)


class S08Cgmp(SpokenScene):
    def construct(self):
        enzyme=chip('guanylate\ncyclase',GOLD,34).move_to([-3.7,1.6,0])
        arrow=Arrow([-1.8,1.6,0],[1.2,1.6,0],color=GOLD,stroke_width=7)
        product=chip('cGMP',GOLD,44).move_to([3.3,1.6,0])
        rail=Line([-3.5,-1,0],[3.5,-1,0],color=GREY,stroke_width=12)
        knob=Dot([-3.5,-1,0],radius=.28,color=GOLD)
        states=VGroup(T('normal\naway',38).move_to([-3.5,-2.25,0]),
                      T('raised\ntoward',38).move_to([3.5,-2.25,0]))
        self.add(enzyme,arrow,product,rail,knob,states)
        self.at('a second messenger')
        self.play(FadeIn(label('cGMP · second messenger',3.15,GOLD,34)),run_time=.5)
        self.at('made by')
        self.play(Indicate(arrow,color=GOLD,scale_factor=1.03),
                  Indicate(product,color=GOLD,scale_factor=1.03),run_time=.6)
        self.at('Here')
        self.play(FadeIn(label('sets the sign here',-.05,size=36)),run_time=.4)
        self.at('sets the sign')
        self.play(knob.animate.move_to([3.5,-1,0]),run_time=1.0)
        self.play(Indicate(states[1],color=GOLD,scale_factor=1.04),run_time=.4)
        self.finish()


def netrin():
    dial=Arc(radius=1.55,start_angle=0,angle=PI,color=BLUE,arc_center=[-2.8,-.1,0])
    ticks=VGroup(*[Line(np.array([-2.8,-.1,0])+1.4*np.array([np.cos(a),np.sin(a),0]),
                       np.array([-2.8,-.1,0])+1.65*np.array([np.cos(a),np.sin(a),0]),color=BLUE)
                  for a in np.linspace(0,PI,7)])
    needle=Arrow([-2.8,-.1,0],[-4, .5,0],buff=0,color=BLUE,stroke_width=7)
    labs=VGroup(T('cAMP low\nrepel',30,BLUE).move_to([-4.8,-1.1,0]),
                T('high\nattract',30,BLUE).move_to([-.8,-1.1,0]))
    grad=VGroup(*[Rectangle(width=.55,height=3.5,stroke_width=0,fill_color=BLUE,
                            fill_opacity=.04+.055*i).move_to([1.5+i*.6,.25,0]) for i in range(7)])
    gl=VGroup(T('netrin',34,BLUE).move_to([3.3,2.65,0]),
              T('low',28,BLUE).move_to([1.5,-2,0]),T('high',28,BLUE).move_to([5.1,-2,0]),
              Arrow([1.5,-1.65,0],[5.1,-1.65,0],buff=0,color=BLUE))
    return VGroup(dial,ticks,needle,labs,grad,gl,
                  label('in some assays',-2.65,size=28),label('See netrin and DCC',-3.35,BLUE,30))


class S09Netrin(SpokenScene):
    def construct(self):
        g=netrin()
        self.add(g)
        self.at('with cyclic')
        self.play(Rotate(g[2],-2.2,about_point=np.array([-2.8,-.1,0])),run_time=1.1)
        self.finish()


class S10CortexQ(SpokenScene):
    def construct(self):
        b,c,n,_=cortex(True,True)
        # The switch recedes into already visible cortex; the entire neuron stays inside.
        n[3].set_opacity(0); n[4].set_opacity(0)
        VGroup(n[0],n[1],n[2]).stretch(1.04,1,about_point=np.array([0,-.1,0]))
        n.set_opacity(.43)
        # n.set_opacity affects descendants, so hide the premature response labels again.
        n[3].set_opacity(0); n[4].set_opacity(0)
        tissue=VGroup(b[0],b[1],n).scale(.87).shift(UP*.3)
        knob=Dot([-.6,.1,0],radius=.22,color=GOLD)
        switch=VGroup(Line([-.6,.1,0],[.6,.1,0],color=GREY,stroke_width=6),knob).move_to([3.8,0,0])
        self.add(tissue,b[2],switch,label('Does a living neuron use this switch?',-3.45,size=30))
        self.at('Look at the developing cortex')
        self.play(switch.animate.scale(.05).move_to([0,-.3,0]),
                  tissue.animate.scale(1.04),run_time=.8)
        self.play(FadeOut(switch),run_time=.2)
        self.finish()


class S11Cortex(SpokenScene):
    def construct(self):
        b,c,n,_=cortex()
        # A faint whole neuron gives scale before its directed growth is described.
        faint=cortex(True,True)[2].set_opacity(.12)
        faint[3].set_opacity(0); faint[4].set_opacity(0)
        self.add(b,faint,n)
        self.at('is high near')
        self.play(FadeIn(c),run_time=.65)
        self.at('the outer surface')
        self.play(Indicate(b[1],scale_factor=1.01),run_time=.5)
        self.at('It repels')
        target=cortex(True)[2]
        self.play(Create(target[1]),FadeIn(target[3]),run_time=1.25)
        self.finish()


class S12Dendrite(SpokenScene):
    def construct(self):
        b,c,n,_=cortex(True)
        self.add(b,c,n)
        self.at('the apical dendrite')
        target=cortex(True,True)[2]
        self.play(Create(target[2]),run_time=1.3)
        self.at('grows up')
        self.play(FadeIn(target[4]),run_time=.4)
        self.play(FadeIn(label('Polleux, Morrow and Ghosh · 2000',-3.4,GREY,26)),run_time=.3)
        self.finish()


class S13Enzyme(SpokenScene):
    def construct(self):
        b,c,n,e=cortex(True,True,True)
        # Fill the slab vertically while retaining the established labels.
        VGroup(n[0],n[1],n[2],e[0]).stretch(1.04,1,about_point=np.array([0,-.1,0]))
        self.add(b,c,n)
        self.at('Soluble guanylate cyclase')
        self.play(FadeIn(e[1]),Create(e[2]),run_time=.75)
        self.at('an enzyme that makes')
        # Product is attached to the dendritic enzyme by the same leader.
        product=plate('makes cGMP',-3.05,-.45,GOLD,28)
        self.play(FadeIn(product),run_time=.5)
        self.at('sits mainly')
        self.play(FadeIn(e[0]),FadeIn(e[3]),n[1].animate.set_color(GREY),run_time=.8)
        self.at('It is needed')
        self.play(FadeIn(label('needed for that attraction',-3.45,GOLD,30)),run_time=.35)
        self.at('needed for that attraction')
        self.play(n[2][-1].animate(rate_func=there_and_back).shift(UP*.28).set_color(GOLD),
                  run_time=1.15)
        self.finish()


class S14One(SpokenScene):
    def construct(self):
        b,c,n,e=cortex(True,True,True)
        n[1].set_color(GREY)
        self.add(b,c,n,e)
        self.add(label('One cue. One neuron. Two answers.',-3.4,size=32))
        self.at('one neuron')
        self.play(Indicate(n[0],scale_factor=1.08,color=TEAL),run_time=.4)
        self.at('two answers')
        self.play(Indicate(n[2][-1],color=GOLD),Indicate(n[1][-1],color=GREY),run_time=.5)
        self.at('where the enzyme is')
        self.play(Indicate(e[0],color=GOLD,scale_factor=1.08),run_time=.7)
        self.finish()


class S15Rule(SpokenScene):
    def construct(self):
        b,p,m=spinal()
        card=rule_card()
        self.add(b,p,m,card)
        block=rule_block()
        self.at('The cue marks the place')
        self.play(FadeIn(block[0]),run_time=.5)
        self.at('The growth cone decides')
        self.play(FadeIn(block[1]),run_time=.5)
        self.finish()


class S16Receptor(SpokenScene):
    def construct(self):
        b,p,m=spinal()
        self.add(b,p,m,rule_block())
        card=rule_card()
        self.add(card)
        self.at('The pain fiber')
        self.play(Indicate(p[0],scale_factor=1.03,color=RED),run_time=.6)
        self.at('the muscle afferent')
        self.play(Indicate(m[0],scale_factor=1.03,color=BLUE),run_time=.6)
        self.at('how strongly')
        self.play(Transform(card,rule_card(1)),
                  Transform(p[1],plate('pain fibre\nstrong · stops',-4.55,1.8,RED,28)),
                  Transform(m[1],plate('muscle afferent\nweak · enters',-.65,1.8,BLUE,28)),run_time=.5)
        self.finish()


class S17State(SpokenScene):
    def construct(self):
        # New summary composition: neuron left, same full-size card right.
        b,c,n,e=cortex(True,True,True)
        drawing=VGroup(b[0],b[1],c[0],n[0],n[1],n[2],e[0]).scale(.88).move_to([-3.1,0,0])
        # Narrow slab only; preserve full vertical neuron scale.
        b[0].stretch(.53,0); b[1].stretch(.53,0); c[0].stretch(.53,0)
        n[1].set_color(GREY)
        card=rule_card(1)
        self.add(drawing,card,rule_block(),
                 plate('dendrite · toward',-3.1,2.85,TEAL,28),
                 plate('axon · away',-3.1,-2.85,TEAL,28))
        self.at('The axon')
        self.play(Transform(card,rule_card(2)),run_time=.4)
        self.at('which way')
        self.play(Indicate(n[2],color=GOLD,scale_factor=1.06),Indicate(n[1],scale_factor=1.06),run_time=.7)
        self.finish()


class S18Layout(SpokenScene):
    def construct(self):
        # Card persists at right; two tall outcome panels fill the remaining stage.
        card=rule_card(2)
        # Card stays at the same position as in the preceding summaries.
        self.add(card)
        panels=VGroup(*[RoundedRectangle(width=3.45,height=5.8,corner_radius=.15,color=GREY)
                        .move_to([x,-.1,0]) for x in [-4.5,-.8]])
        left=cone([-5.8,.4,0],r=1.55)
        right=cone([-2.1,.4,0],r=1.55)
        self.add(panels,left,right,T('Repelled growth cones\nTypical outcomes',28).move_to([-2.65,3.3,0]))
        self.at('For a repelled growth cone')
        self.play(Transform(card,rule_card(3)),run_time=.5)
        self.at('a pipette gradient')
        pip=Polygon([-3.5,1.95,0],[-3.0,2.25,0],[-3.0,2.5,0],color=GREY)
        cloud=VGroup(*[Polygon([-3.5,1.95,0],[-3.5-.19*i,1.95,0],[-3.5-.19*i,1.95-.18*i,0],
                               stroke_width=0,fill_color=YELLOW,fill_opacity=.045) for i in range(1,7)])
        self.play(FadeIn(pip),FadeIn(cloud),FadeIn(plate('pipette gradient',-4.5,-2.6,YELLOW,26)),run_time=.5)
        self.at('gives a turn')
        self.play(Rotate(left,-.38,about_point=np.array([-5.8,.4,0])),
                  FadeIn(plate('turn',-4.5,-1.95,GREEN,30)),run_time=.65)
        self.at('A strong dose')
        bath=Rectangle(width=3.25,height=4.3,stroke_width=0,fill_color=YELLOW,fill_opacity=.13).move_to([-.8,.4,0])
        self.play(FadeIn(bath),FadeIn(plate('strong bath dose',-.8,-2.6,YELLOW,26)),run_time=.55)
        self.at('give a collapse')
        target=VGroup(fan(-.16,.16,1.5,[-2.1,.4,0]),filopodia(-.16,.16,1.5,[-2.1,.4,0],k=3))
        self.play(Transform(right,target),FadeIn(plate('collapse',-.8,-1.1,RED,30)),run_time=.65)
        self.at('where the preparation')
        self.play(FadeIn(plate('where the\npreparation\nsupports it',3.7,-2.15,TEXT,30)),
                  FadeIn(label('Collapse depends on the preparation.',-3.4,size=28)),run_time=.55)
        self.finish()


class S19Takeaway(SpokenScene):
    def construct(self):
        place=label('The place is in the cue.',2.1,YELLOW,44)
        meaning=label('The meaning is in the cell.',.75,TEAL,44)
        hear=chip('Can hear the cue',TEAL,38).move_to([-3.2,-1.75,0])
        sign=chip('State sets the sign',GOLD,38).move_to([3.1,-1.75,0])
        # Preview both conditions, then emphasize them before their explanation.
        self.add(place,meaning,Line([-4,-.3,0],[4,-.3,0],color=GREY),hear,sign)
        self.at('keep axons out')
        self.play(Indicate(place,scale_factor=1.04),run_time=.6)
        self.at('but only axons')
        self.play(Indicate(hear,scale_factor=1.04,color=TEAL),
                  Indicate(sign,scale_factor=1.04,color=GOLD),run_time=.4)
        self.at('and only in the sense')
        self.play(Indicate(sign,color=GOLD,scale_factor=1.04),run_time=.55)
        self.finish()


class S20End(EndCard):
    LINE='Only axons that can hear semaphorins respond as their state allows.'
    def construct(self):
        sentence=VGroup(T('Only axons that can hear semaphorins',38),
                        T('respond as their state allows.',38)).arrange(DOWN,buff=.16).move_to([0,.35,0])
        self.add(sentence,
                 label('biochemistrypedia.com',-1.15,TEAL,28))
        self.finish()
