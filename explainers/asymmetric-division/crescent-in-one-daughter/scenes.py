"""Chapter 3: A Crescent in One Daughter.
COLOR MAP: YELLOW=Numb; TEAL=Notch on; RED=absence/block;
VIOLET=inner fate (neuron/sheath); ORANGE=outer fate (hair/socket);
GREY=membranes/unknown/Notch off; BLUE=DNA channel; TEXT=labels.
All drawings are schematic cells, never molecular structures.
"""
from bp_style import *
import numpy as np

ORANGE = '#F29E4C'
VIOLET = '#A98BE0'
LESSON = 'Asymmetric Division: Numb and the Neuroblast'


def label(text, color=TEXT, x=0, y=0, size=28):
    return T(text, size=size, color=color).move_to([x,y,0])


def head(text):
    return label(text, y=3.35, size=30)


def cell(c, r, color=GREY, op=.12):
    return Circle(radius=r, color=color, stroke_width=4,
                  fill_color=color, fill_opacity=op).move_to(c)


def crescent(c, r, span=PI, w=14):
    return Arc(radius=r, start_angle=PI-span/2, angle=span,
               arc_center=c, color=YELLOW, stroke_width=w)


def arr(a,b,color=GREY):
    return Arrow(a,b,buff=0,color=color,stroke_width=4,tip_length=.23)


def cross(m):
    return Line(m.get_corner(DL),m.get_corner(UR),color=RED,stroke_width=6)


MC=[0,.1]


def outline_pt(t,p=0):
    """Point on the dividing cell's outline; p is 0 (round, elongated) to 1 (pinched in two)."""
    a=3.5+.7*p; b=2.2-.15*p
    x=a*np.cos(t)
    y=b*np.sin(t)*(1-p*np.exp(-(x/.8)**2))
    return np.array([MC[0]+x,MC[1]+y,0])


def mother(p=0):
    return ParametricFunction(lambda t: outline_pt(t,p),t_range=[0,TAU,.05],color=GREY,
        stroke_width=4,fill_color=GREY,fill_opacity=.10)


def mother_crescent(p=0,span=1.25):
    return ParametricFunction(lambda t: outline_pt(t,p),t_range=[PI-span,PI+span,.04],
        color=YELLOW,stroke_width=14)


PLATE_Y=[-.95,-.32,.32,.95]


def spindle():
    g=VGroup()
    for sx in (-1,1):
        pole=np.array([sx*2.85,MC[1],0])
        for y in PLATE_Y:
            bow=.55*sx*(1 if y>0 else -1)*(0 if abs(y)<.5 else 1)
            end=np.array([0,MC[1]+y,0])
            g.add(ArcBetweenPoints(pole,end,angle=bow*.9,color=GREY,stroke_width=3,stroke_opacity=.7) if bow else
                  Line(pole,end,color=GREY,stroke_width=3,stroke_opacity=.7))
        g.add(Dot(pole,radius=.13,color=GREY))
    return g


def dividing():
    return VGroup(mother(),spindle())


def dna_plate(c=(0,.1),scale=1.0):
    rods=VGroup(*[RoundedRectangle(width=.2,height=.6,corner_radius=.09,color=BLUE,
        fill_color=BLUE,fill_opacity=1).rotate(r).move_to([c[0]+dx,c[1]+y,0])
        for y,r,dx in zip(PLATE_Y,[.18,-.15,.12,-.2],[.03,-.04,.02,-.03])])
    return rods.scale(scale,about_point=[c[0],c[1],0])


def pair():
    return VGroup(cell([-2.15,.25,0],2.05),cell([2.15,.25,0],2.05))


def pair_gold():
    p=pair(); p[0].set_stroke(YELLOW)
    return p


def pair_numb():
    return crescent([-2.15,.25,0],1.85)


def dna(c,scale=1):
    rods=VGroup(*[RoundedRectangle(width=.16,height=.7,corner_radius=.07,
        color=BLUE,fill_color=BLUE,fill_opacity=1).rotate(t).move_to(np.array(c)+[x,y,0])
        for x,y,t in [(-.45,.18,-.25),(.1,-.2,.2),(.45,.25,-.3)]])
    return rods.scale(scale,about_point=c)


def embryo():
    e=Ellipse(width=8.5,height=4.6,color=GREY,fill_color=GREY,fill_opacity=.1).move_to([0,-.25,0])
    marks=VGroup()
    for x in [-3,-2,-1,0,1,2,3]:
        h=2.3*np.sqrt(1-(x/4.25)**2)
        marks.add(ArcBetweenPoints([x,-.25+h-.12,0],[x,-.25-h+.12,0],angle=.16,color=GREY,stroke_opacity=.5))
    return VGroup(e,marks)


def neuron(x,y,scale=1):
    return VGroup(cell([x,y,0],.3,VIOLET),
        Line([x,y-.3,0],[x,y-.9,0],color=VIOLET,stroke_width=5),
        Line([x-.24,y+.17,0],[x-.55,y+.55,0],color=VIOLET,stroke_width=5),
        Line([x+.24,y+.17,0],[x+.55,y+.55,0],color=VIOLET,stroke_width=5)).scale(scale,about_point=[x,y,0])


def support(x,y,r=.65):
    return VGroup(cell([x,y,0],r,ORANGE,.24),Circle(radius=r*.45,color=ORANGE,stroke_width=3).move_to([x,y,0]))


def sheath(x,y,scale=1):
    return VGroup(Ellipse(width=.85,height=1.3,color=VIOLET,fill_color=VIOLET,fill_opacity=.2).move_to([x,y,0]),
        Line([x,y-.4,0],[x,y+.4,0],color=VIOLET,stroke_width=4)).scale(scale,about_point=[x,y,0])


def hair(x,y):
    return VGroup(cell([x,y,0],.52,ORANGE,.2),Line([x,y+.52,0],[x+.3,y+1.35,0],color=ORANGE,stroke_width=7))


ROOT=[0,2.05,0]
DAUGHTERS=[(-2.9,.25,0),(2.9,.25,0)]
LEAVES=[(-4.55,-1.8,0),(-1.45,-1.8,0),(1.45,-1.8,0),(4.55,-1.8,0)]


def tree_lines():
    g=VGroup(*[Line([0,1.43,0],[x,y+.72,0],color=GREY,stroke_width=3) for x,y,z in DAUGHTERS])
    for p,inds in zip(DAUGHTERS,[(0,1),(2,3)]):
        for i in inds:
            q=LEAVES[i]
            g.add(Line([p[0],p[1]-.72,0],[q[0],q[1]+.67,0],color=GREY,stroke_width=3))
    return g


def tree_nodes():
    return VGroup(cell(ROOT,.62),*[cell(p,.73) for p in DAUGHTERS],*[cell(p,.67) for p in LEAVES])


def tree_crescents():
    return VGroup(*[crescent(p,.61,w=10) for p in DAUGHTERS])


def loss_tag():
    n=chip('Numb',YELLOW,size=26).move_to([2.15,2.35,0])
    return VGroup(label('precursor, no Numb',GREY,-2.6,2.25,26),n,cross(n),
                  Line([1.4,2.05,0],[.65,2.05,0],color=YELLOW))


def lineage(gain=False,inner=False,result=False,question=False,absence=True):
    title='Give Numb to both' if gain else 'Remove Numb'
    g=VGroup(head(title),tree_lines(),cell(ROOT,.62))
    for p in DAUGHTERS:
        g.add(cell(p,.73,VIOLET if inner else GREY,.2))
    if gain:
        g.add(tree_crescents(),label('First division only · pulse ended',YELLOW,0,2.95,26))
    else:
        g.add(loss_tag())
    if result:
        if gain:
            for i,(x,y,z) in enumerate(LEAVES):
                g.add(neuron(x,y,1) if i%2==0 else sheath(x,y))
                g.add(label('neuron' if i%2==0 else 'sheath',VIOLET,x,-2.8,26))
        else:
            g.add(*[support(x,y) for x,y,z in LEAVES])
            g.add(label('4 outer support cells',ORANGE,0,-2.85,30))
            if absence: g.add(label('No neuron or sheath',GREY,0,-3.4,26))
    else:
        g.add(*[cell(p,.67).set_stroke(opacity=.4 if inner else 1) for p in LEAVES])
    if inner or (result and not gain):
        for x,y,z in DAUGHTERS:
            g.add(label('inner precursor' if gain else 'outer precursor',VIOLET if gain else ORANGE,x*1.24,1.45,26))
    if question: g.add(label('What forms now?' if gain else 'What cells form?',y=-3.25,size=32))
    return g


def no_bristle():
    # An explicitly negated anatomical sketch: ghost shaft and socket, both crossed out.
    shaft=Line([5.45,.1,0],[5.85,1.1,0],color=ORANGE,stroke_width=9,stroke_opacity=.55)
    socket=Ellipse(width=1.4,height=.55,color=ORANGE,stroke_width=6,stroke_opacity=.55).move_to([5.6,-.05,0])
    sketch=VGroup(shaft,socket)
    x1=Line(sketch.get_corner(UL),sketch.get_corner(DR),color=RED,stroke_width=8)
    x2=Line(sketch.get_corner(DL),sketch.get_corner(UR),color=RED,stroke_width=8)
    return VGroup(sketch,x1,x2,label('No bristle',GREY,5.6,-.85,26))


def takeaway():
    p=pair(); p[0].set_stroke(YELLOW); p[1].set_stroke(TEAL).set_fill(TEAL,.2)
    return VGroup(p,pair_numb(),label('Numb',YELLOW,-2.15,.25,34),
        label('Notch off',GREY,-2.15,-2.2,30),label('Notch on',TEAL,2.15,-2.2,30),
        label('Numb forms a crescent → enters one daughter',YELLOW,0,3.2,30),
        label('The Numb daughter does not hear Notch.',TEXT,0,-3.1,32))


class S00Title(TitleCard):
    TITLE='A Crescent in One Daughter'
    LESSON=LESSON
    def construct(self):
        self.add(label('BIOCHEMISTRYPEDIA',TEAL,0,2.15,26),label(self.LESSON,GREY,0,1.25,26))
        self.play(FadeIn(label(self.TITLE,size=48)),Create(Line([-1.2,-.85,0],[1.2,-.85,0],color=GOLD)),run_time=.7)
        self.finish()


class S01Question(SpokenScene):
    def construct(self):
        p=VGroup(cell([-2.35,.25,0],2.35),cell([2.35,.25,0],2.35,TEAL,.2))
        self.add(p)
        self.at('only one hears')
        self.play(FadeIn(label('Notch off',GREY,-2.35,.25,34)),FadeIn(label('Notch on',TEAL,2.35,.25,34)),run_time=.35)
        self.at('What makes the difference')
        self.play(FadeIn(label('What makes the difference?',y=-3,size=36)),run_time=.3)
        self.finish()


class S02Mutant(SpokenScene):
    def construct(self):
        self.add(embryo(),label('fly embryo',GREY,0,-3.1,30))
        self.at('In 1989')
        self.play(FadeIn(head('Uemura and colleagues · 1989')),run_time=.35)
        self.at('studied embryos')
        n=chip('numb',YELLOW,size=44).move_to([0,-.25,0])
        # Opaque backing keeps the segment lines out of the gene label.
        n[0].set_fill(BG,1)
        self.play(FadeIn(n),run_time=.3)
        self.at('lacking the gene')
        self.play(Create(cross(n)),run_time=.45)
        self.finish()


class S03Lab(SpokenScene):
    def construct(self):
        self.add(RoundedRectangle(width=11,height=4.5,corner_radius=.3,color=TEAL),
            label('The Jan laboratory',y=.8,size=46),label('Lily Jan',GREY,-2.6,-.7,36),
            label('Yuh Nung Jan',GREY,2.6,-.7,36))
        self.at('They worked')
        self.wait(.1)
        self.finish()


class S04Result(SpokenScene):
    def construct(self):
        self.add(head('numb mutant embryo · body-wall sense organs'))
        ns=VGroup(*[neuron(x,.1,2.45) for x in [-3.8,0,3.8]])
        self.add(ns)
        self.at('the sensory neurons')
        n=label('sensory neurons',VIOLET,0,-2.9,32)
        self.play(FadeIn(n),run_time=.3)
        self.at('transformed into')
        ss=VGroup(*[support(x,0,1.55) for x in [-3.8,0,3.8]])
        self.play(FadeOut(ns),FadeIn(ss),FadeOut(n),run_time=.8)
        self.play(FadeIn(label('support cells · same lineage',ORANGE,0,-2.9,32)),run_time=.25)
        self.finish()


class S05Gene(SpokenScene):
    def construct(self):
        gene=chip('numb',YELLOW,size=44).move_to([0,1.65,0])
        p=VGroup(cell([-2.8,-.85,0],1.25),cell([2.8,-.85,0],1.25))
        self.add(gene,p,arr([-.7,1.15,0],[-2.3,.5,0]),arr([.7,1.15,0],[2.3,.5,0]))
        self.at('chooses between')
        self.play(FadeIn(label('chooses between sister fates',y=-2.65,size=32)),run_time=.3)
        self.at('did not show how')
        self.play(FadeIn(label('How?',YELLOW,0,3,38)),run_time=.25)
        self.finish()


class S06Rhyu(SpokenScene):
    def construct(self):
        self.add(dividing(),head('Rhyu, Jan and Jan · 1994'))
        self.at('stained dividing precursors')
        self.play(FadeIn(label('dividing sensory organ precursor',GREY,0,-3.05,30)),run_time=.3)
        self.at('with an antibody')
        pill=chip('antibody to Numb',YELLOW,size=28).move_to([4.3,2.4,0])
        leader=Line([3.75,2.0,0],[3.05,1.2,0],color=YELLOW,stroke_width=3)
        self.play(FadeIn(pill),Create(leader),FadeIn(Dot([3.05,1.2,0],radius=.07,color=YELLOW)),run_time=.35)
        self.finish()


class S07Method(SpokenScene):
    def construct(self):
        self.add(head('Two imaging channels'),cell([-3,.5,0],2.1),cell([3,.5,0],2.1))
        self.at('an antibody marks')
        self.play(FadeIn(label('Numb antibody',YELLOW,-3,-1.95,30)),run_time=.3)
        self.at('a DNA dye')
        self.play(FadeIn(dna([3,.5,0],1.9)),FadeIn(label('DNA dye',BLUE,3,-1.95,30)),run_time=.4)
        self.at('stage of mitosis')
        self.play(FadeIn(label('condensed chromosomes',BLUE,3,-2.75,30)),run_time=.3)
        self.finish()


class S08Crescent(SpokenScene):
    def construct(self):
        self.add(dividing(),dna_plate(MC,1.0))
        self.at('Numb was at')
        edge=outline_pt(.55)
        self.play(FadeIn(label('membrane',GREY,5.2,2.1,30)),
            Create(Line(edge,[3.98,1.92,0],color=GREY,stroke_width=3)),run_time=.3)
        self.at('a crescent')
        self.play(Create(mother_crescent()),FadeIn(label('Numb',YELLOW,-5.2,.1,34)),
            Create(Line([-4.38,.1,0],[-3.85,.1,0],color=YELLOW,stroke_width=3)),run_time=.5)
        self.at('one half')
        self.play(FadeIn(label('One half of the cell',y=-3.05,size=30)),run_time=.3)
        self.finish()


class S09One(SpokenScene):
    def construct(self):
        pt=ValueTracker(0)
        m=always_redraw(lambda: mother(pt.get_value()))
        c=always_redraw(lambda: mother_crescent(pt.get_value(),1.25))
        sp=spindle(); d=dna_plate(MC,1.0)
        self.add(m,c,sp,d)
        self.at('When the cell divided')
        dl=d.copy(); dr=d.copy()
        self.remove(d); self.add(dl,dr)
        self.play(pt.animate.set_value(1),dl.animate.shift(LEFT*1.9),dr.animate.shift(RIGHT*1.9),
            FadeOut(sp,run_time=.9),run_time=2.5,rate_func=smooth)
        self.at('one daughter only')
        m.clear_updaters(); c.clear_updaters()
        p=pair_gold(); pn=pair_numb()
        self.play(FadeIn(p),FadeIn(pn),FadeOut(m),FadeOut(c),FadeOut(dl),FadeOut(dr),
            FadeIn(label('Numb',YELLOW,-2.15,.25,34)),run_time=.4)
        self.finish()
        self.wait(2)


INN=[-3.0,1.55,0]
OUT=[3.0,1.55,0]


def hair2(x,y,r):
    k=r/.75
    p0=np.array([x-.7*r,y+.7*r,0])
    return VGroup(cell([x,y,0],r,ORANGE,.2),Line(p0,p0+np.array([-.4*k,1.05*k,0]),color=ORANGE,stroke_width=8))


class S10Scheme(SpokenScene):
    def construct(self):
        pc=pair_gold(); cr=pair_numb(); nl=label('Numb',YELLOW,-2.15,.25,34)
        self.add(pc,cr,nl)
        inner=cell(INN,1.2,GREY,.12).set_stroke(YELLOW)
        outer=cell(OUT,1.2,GREY,.12)
        newcr=crescent(INN,1.05,w=12)
        newl=label('Numb',YELLOW,INN[0],INN[1],30)
        self.play(ReplacementTransform(pc[0],inner),ReplacementTransform(pc[1],outer),
            ReplacementTransform(cr,newcr),FadeOut(nl),FadeIn(newl),run_time=.7)
        self.at('that daughter')
        self.play(FadeIn(label('inner precursor',VIOLET,INN[0],3.25,28)),run_time=.3)
        self.at('Its sister')
        self.play(FadeIn(label('outer precursor',ORANGE,OUT[0],3.25,28)),
            outer.animate.set_stroke(ORANGE).set_fill(ORANGE,.12),run_time=.3)
        self.at('makes the hair')
        hs=hair2(OUT[0],OUT[1],.3); ss=support(OUT[0],OUT[1],.3)
        self.add(hs,ss)
        a1=arr([2.62,.62,0],[1.7,-.72,0],ORANGE); a2=arr([3.4,.62,0],[4.3,-.72,0],ORANGE)
        self.play(Transform(hs,hair2(1.3,-1.45,.75)),Transform(ss,support(4.7,-1.45,.75)),
            GrowArrow(a1),GrowArrow(a2),run_time=.8)
        self.play(FadeIn(label('hair cell',ORANGE,1.3,-2.7,28)),FadeIn(label('socket cell',ORANGE,4.7,-2.7,28)),run_time=.3)
        self.finish()


class S11Predict1(SpokenScene):
    def construct(self):
        self.add(head('Two tests'),tree_lines(),tree_nodes())
        self.at('remove num')
        self.remove(self.mobjects[0])
        self.play(FadeIn(head('Remove Numb')),FadeIn(loss_tag()),run_time=.4)
        self.at('What cells form')
        self.play(FadeIn(label('What cells form?',y=-3.25,size=32)),run_time=.3)
        self.finish()


def countdown(scene,gain=False):
    scene.camera.background_color=BG
    scene.add(lineage(gain=gain,question=True))
    center=[5.65,2.55,0]
    ring=Circle(radius=.58,color=GREY).move_to(center)
    scene.add(ring)
    for n in range(5,0,-1):
        number=label(str(n),TEXT,5.65,2.55,32)
        arc=Arc(radius=.58,start_angle=PI/2,angle=-TAU*n/5,arc_center=center,color=TEAL,stroke_width=7)
        scene.add(number,arc)
        scene.play(Uncreate(arc),run_time=1,rate_func=linear)
        scene.remove(number,arc)


class S12Pause(Scene):
    def construct(self): countdown(self)


class S13Reveal1(SpokenScene):
    def construct(self):
        p=lineage(question=True); self.add(p)
        self.at('four outer support cells')
        self.play(FadeOut(p),FadeIn(lineage(result=True,absence=False)),run_time=.6)
        self.at('no neuron or sheath')
        self.play(FadeIn(label('No neuron or sheath',GREY,0,-3.4,26)),run_time=.3)
        self.finish()


class S14Beat(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(lineage(result=True)); self.wait(2)


class S15Predict2(SpokenScene):
    def construct(self):
        self.add(head('Give Numb to both'),tree_lines(),tree_nodes())
        self.at('make extra')
        pulse=chip('extra Numb pulse',YELLOW,size=28).move_to([-3.5,2.6,0])
        arrow=arr([-1.9,2.6,0],[-.7,2.1,0],YELLOW)
        self.play(FadeIn(pulse),GrowArrow(arrow),run_time=.35)
        self.at('only during')
        root_signal=crescent(ROOT,.5,w=10)
        self.play(Create(root_signal),run_time=.35)
        self.at('both daughters inherit')
        self.play(ReplacementTransform(root_signal,tree_crescents()),FadeOut(pulse),FadeOut(arrow),run_time=.5)
        self.play(FadeIn(label('First division only · pulse ended',YELLOW,0,2.95,26)),run_time=.3)
        self.at('What forms now')
        self.play(FadeIn(label('What forms now?',y=-3.25,size=32)),run_time=.3)
        self.finish()


class S16Pause(Scene):
    def construct(self): countdown(self,True)


class S17Reveal2(SpokenScene):
    def construct(self):
        p=lineage(gain=True,question=True); self.add(p)
        self.at('Both daughters')
        self.play(FadeOut(p),FadeIn(lineage(gain=True,inner=True)),run_time=.6)
        self.finish()


class S18Reveal2b(SpokenScene):
    def construct(self):
        p=lineage(gain=True,inner=True); self.add(p)
        self.at('Each then divides')
        self.play(Indicate(p[1],color=VIOLET,scale_factor=1.01),run_time=.5)
        self.at('You get neurons')
        self.play(FadeOut(p),FadeIn(lineage(gain=True,inner=True,result=True)),run_time=.55)
        self.at('but no hair')
        self.play(FadeIn(label('No hair or socket',GREY,0,-3.45,28)),run_time=.3)
        self.at('So there is')
        self.play(FadeIn(no_bristle()),run_time=.4)
        self.finish()


class S19Beat(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(lineage(gain=True,inner=True,result=True),label('No hair or socket',GREY,0,-3.45,28),no_bristle()); self.wait(2)


class S20Logic(SpokenScene):
    def construct(self):
        centre=VGroup(cell([0,1.9,0],.9),label('Numb',YELLOW,0,2.08,30),label('present',GREY,0,1.68,26))
        self.add(head('Opposite changes'),centre,label('Loss of Numb',GREY,-4.4,2.55,32),
            label('Gain of Numb',YELLOW,4.4,2.55,32),label('first division only',YELLOW,4.4,2.05,26))
        rows=[-.4,-1.95]
        left=VGroup(*[support(x,y,.72) for y in rows for x in (-4.4,-2.8)])
        right=VGroup(neuron(2.8,-.1,1.0),sheath(4.4,-.4,1.1),neuron(2.8,-1.75,1.0),sheath(4.4,-1.95,1.1))
        self.at('loss and gain')
        self.play(GrowArrow(arr([-.75,1.35,0],[-2.4,.55,0],ORANGE)),
            GrowArrow(arr([.75,1.35,0],[2.4,.55,0],VIOLET)),
            FadeIn(left),FadeIn(right),
            FadeIn(label('loss pushes this way',ORANGE,-4.4,1.45,26)),
            FadeIn(label('gain pushes this way',VIOLET,4.4,1.45,26)),
            FadeIn(label('all outer',ORANGE,-3.6,-3.2,30)),FadeIn(label('all inner',VIOLET,3.6,-3.2,30)),run_time=.5)
        self.at('decides between')
        self.play(FadeIn(label('Two fates',TEXT,0,-.7,38)),
            FadeIn(chip('outer',ORANGE,size=28).move_to([-1.0,-1.8,0])),
            FadeIn(chip('inner',VIOLET,size=28).move_to([1.0,-1.8,0])),run_time=.35)
        self.finish()


class S21Branches(SpokenScene):
    def construct(self):
        root=cell([0,2.0,0],.62)
        fork=[0,.55,0]
        self.add(root,Line([0,1.38,0],fork,color=GREY),arr(fork,[-2.03,-1.07,0],VIOLET),
            arr(fork,[2.03,-1.07,0],ORANGE),cell([-3,-1.85,0],1.25,VIOLET,.2),
            cell([3,-1.85,0],1.25,ORANGE,.2),label('inner',VIOLET,-3,-1.85,34),label('outer',ORANGE,3,-1.85,34))
        self.at('Numb decides')
        tag=chip('Numb',YELLOW,size=30).move_to(fork)
        tag[0].set_fill(BG,1)
        self.play(FadeIn(tag),run_time=.3)
        self.at('two branches')
        self.play(FadeIn(head('Two branches')),run_time=.3)
        self.finish(); self.wait(1.5)


def notch_table():
    g=VGroup(head('The Notch map'),label('Division',GREY,-4.65,2.3,28),
        label('Notch off',GREY,-.85,2.3,30),label('Notch on',TEAL,3.6,2.3,30))
    for y,division,off,on in [(1.05,'SOP','inner precursor','outer precursor'),
        (-.8,'outer precursor','hair','socket'),(-2.65,'inner precursor','neuron','sheath')]:
        g.add(label(division,GREY,-4.65,y,26),chip(off,GREY,size=28).move_to([-.85,y,0]),
            chip(on,TEAL,size=28).move_to([3.6,y,0]))
    return g


class S22Lineup(SpokenScene):
    def construct(self):
        table=notch_table(); self.add(table)
        self.at('Numb goes into')
        target=table[5]
        badge=chip('Numb',YELLOW,size=26).move_to([-.85,.25,0])
        self.play(target[0].animate.set_stroke(YELLOW),FadeIn(badge),run_time=.4)
        self.at('That is the')
        self.play(Indicate(target,color=YELLOW,scale_factor=1.02),run_time=.4)
        self.finish()


class S23Open(SpokenScene):
    def construct(self):
        self.add(cell([0,-1.5,0],1.8),crescent([0,-1.5,0],1.6),label('Numb',YELLOW,0,-1.5,34))
        a=RoundedRectangle(width=5.5,height=2.35,corner_radius=.3,color=GREY).move_to([-3,1.6,0])
        b=a.copy().move_to([3,1.6,0])
        self.at('tell the cell')
        note=VGroup(a,Line([-1.4,.4,0],[-.8,0,0],color=GREY),
            Rectangle(width=1.1,height=1.25,color=TEXT).move_to([-4.6,1.6,0]),
            Line([-5,1.9,0],[-4.25,1.9,0],color=TEXT),arr([-4.95,1.45,0],[-4.3,1.45,0],TEXT),
            label('become X',TEXT,-2.4,1.7,30),label('Instruction?',GREY,-2.4,.95,28))
        self.play(FadeIn(note),run_time=.4)
        self.at('only stop')
        rec=RoundedRectangle(width=.7,height=1.7,corner_radius=.15,color=TEAL,fill_color=TEAL,
            fill_opacity=.4).move_to([1.6,1.55,0])
        receptor=VGroup(b,Line([1.4,.4,0],[.8,0,0],color=GREY),
            Line([.8,.95,0],[2.5,.95,0],color=GREY,stroke_width=6),rec,
            Line(rec.get_corner(UL),rec.get_corner(DR),color=RED,stroke_width=7),
            Line(rec.get_corner(DL),rec.get_corner(UR),color=RED,stroke_width=7),
            label('Block Notch?',TEAL,4.2,1.6,28))
        self.play(FadeIn(receptor),run_time=.4)
        self.finish()


class S24Takeaway(SpokenScene):
    def construct(self):
        self.add(takeaway())
        self.at('Numb forms a crescent')
        self.play(Indicate(self.mobjects[0][1],color=YELLOW,scale_factor=1.03),run_time=.45)
        self.at('goes into')
        self.play(Indicate(self.mobjects[0][0][0],color=YELLOW,scale_factor=1.02),run_time=.45)
        self.finish()


class S25End(EndCard):
    LINE='Numb forms a crescent; its daughter does not hear Notch.'
    def construct(self):
        self.add(takeaway()); self.finish()
