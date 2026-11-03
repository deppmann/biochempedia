"""The Organizer's Catchers: schematic anatomy and protein cartoons, no structures.
COLOR MAP: GREY undecided ectoderm; ORANGE skin / non-neural; BLUE neural;
YELLOW BMP; GREEN catchers; PURPLE organizer / dorsal mesoderm; PINK receptor;
TEAL FGF; GOLD receptor-binding faces. No quantitative traces occur in this film.
"""
import numpy as np
from bp_style import *
ORANGE = '#F29E4C'
PURPLE = '#B58CD9'
PINK = '#E58AC0'
LIGHT = '#CED3DD'

def label(s, p, color=TEXT, size=28):
    return T(s, size=max(26,size), color=color, line_spacing=1.05).move_to(p)
def head(s):
    return label(s,[0,3.35,0],size=34)
def cell(p,r=.5,color=GREY):
    return Circle(radius=r,stroke_color=color,stroke_width=3,fill_color=color,fill_opacity=.3).move_to(p)
def paint(c,color):
    return c.animate.set_stroke(color).set_fill(color,.4)
def dot(p,r=.13,color=GREEN):
    return Dot(p,radius=r,color=color)
def grip(name,p,r=1):
    # Different open schematic grips, never molecular geometry.
    if name=='Chordin':
        body=VMobject(color=GREEN,stroke_width=11).set_points_as_corners([
            [r*.7,r*.75,0],[-r*.85,r*.75,0],[-r*.85,-r*.75,0],[r*.7,-r*.75,0]])
    elif name=='Follistatin':
        T_END=3.4*PI
        body=ParametricFunction(lambda t: np.array([r*(.5+.5*t/T_END)*np.cos(t),r*(.5+.5*t/T_END)*np.sin(t),0]),
            t_range=[0,T_END],color=GREEN,stroke_width=11)
    else:
        body=Arc(radius=r,start_angle=.25*PI,angle=1.5*PI,color=GREEN,stroke_width=11)
    return body.shift(np.array(p))
def catcher(name,p,r=1):
    return VGroup(grip(name,p,r),label(name,np.array(p)+[0,-r-.48,0],GREEN))
def dimer(p,name='BMP4',r=.46):
    p=np.array(p)
    return VGroup(VGroup(cell(p+[-r*.7,0,0],r,YELLOW),cell(p+[r*.7,0,0],r,YELLOW)),
                  label(name,p+[0,max(r+.7,1.5),0],YELLOW))
def embryo(p=(0,-.2,0),r=2.65,neural=False):
    shell=Circle(radius=r,stroke_color=LIGHT,stroke_width=6,fill_color=BG,fill_opacity=1)
    yolk=Sector(radius=r-.12,start_angle=PI,angle=PI,fill_color=ORANGE,fill_opacity=.24,stroke_width=0)
    plate=Arc(radius=r,start_angle=.58*PI,angle=.32*PI,stroke_width=19,stroke_color=BLUE if neural else GREY)
    org=Arc(radius=r,start_angle=.96*PI,angle=.13*PI,stroke_width=19,stroke_color=PURPLE)
    return VGroup(shell,yolk,plate,org).shift(np.array(p))
def groove(p=(0,-.2,0),r=2.65):
    return VMobject(color=PURPLE,stroke_width=8).set_points_smoothly([
        [-r,-.5,0],[-r+.55,-.7,0],[-r+.7,-.35,0]]).shift(np.array(p))
def gastrula():
    return VGroup(embryo(),groove())
def tissue(color=GREY):
    return VGroup(*[cell([x,y,0],.64,color) for y in [.68,-.68] for x in [-2.04,-.68,.68,2.04]])
def source_map(glow=True):
    R=1.8; cy=-.45; bx,gx=-4.0,4.0
    b=embryo([bx,cy,0],R); b[3].set_opacity(0)
    ring=VGroup(*[cell([bx+R*np.cos(a),cy+R*np.sin(a),0],.14,GREY) for a in np.linspace(0,2*PI,26,endpoint=False)])
    b.add(ring)
    g=embryo([gx,cy,0],R)
    gr=groove([gx,cy,0],R)
    source=Arc(radius=R,start_angle=.58*PI,angle=.32*PI,stroke_color=GREEN,stroke_width=23).shift([bx,cy,0])
    labels=VGroup(label('blastula',[bx,1.9,0]),label('gastrula',[gx,1.9,0]),
        label('blastocoel',[bx,.05,0],LIGHT),label('endoderm',[bx,-1.2,0],ORANGE),
        label('ectoderm',[bx,.75,0],LIGHT),label('organizer · dorsal lip',[gx,-2.65,0],PURPLE))
    axes=VGroup()
    for x in [bx,gx]:
        axes.add(Arrow([x-.15,-3.1,0],[x-1.85,-3.1,0],buff=0,color=LIGHT),
                 Arrow([x+.15,-3.1,0],[x+1.85,-3.1,0],buff=0,color=LIGHT),
                 label('dorsal',[x-1.1,-3.55,0],LIGHT),label('ventral',[x+1.1,-3.55,0],LIGHT))
    return VGroup(b,g,gr,labels,axes,source if glow else VGroup())
def source_tag():
    # Short tag above the blastula with a leader to the glowing dorsal animal cells.
    return VGroup(label('Chordin, Noggin',[-4.9,2.65,0],GREEN,28),
        Line([-5.0,2.38,0],[-5.33,1.0,0],color=GREEN,stroke_width=3))
def cap_stage(question=True,neural=False):
    dish=RoundedRectangle(width=10.7,height=4.7,corner_radius=.45,stroke_color=LIGHT,stroke_width=4).move_to([0,-.35,0])
    cap=tissue(BLUE if neural else GREY).move_to([.3,-.55,0])
    nog=VGroup(catcher('Noggin',[-3.8,.15,0],.7),
        grip('Noggin',[-1.5,1.35,0],.38),grip('Noggin',[1.2,1.35,0],.38),
        grip('Noggin',[3.8,.6,0],.38))
    q=label('What should the caps become?',[0,-3.25,0],size=32)
    return VGroup(head('1993 · Lamb and colleagues'),dish,cap,nog,q if question else VGroup())
def cap_answer():
    return VGroup(cap_stage(False,True),label('neural · no dorsal mesoderm',[0,-3.25,0],BLUE,32))
def strike(mob):
    # A single line below the letter centres leaves the names readable.
    return Line(mob.get_left()+DOWN*.02,mob.get_right()+DOWN*.02,color=RED,stroke_width=2.5)
def depleted_stage(question=True):
    e=embryo([-1.6,-.25,0],2.65,True)
    names=VGroup(*[chip(n,GREEN,28) for n in ['Chordin','Noggin','Follistatin']]).arrange(DOWN,buff=.35).move_to([4.2,.2,0])
    marks=VGroup(*[strike(n) for n in names])
    q=label('What happens to the neural plate?',[0,-3.4,0],size=30)
    species=label('Xenopus tropicalis',[3.6,2.25,0],LIGHT)
    return VGroup(head('2005 · Khokha and colleagues'),species,e,names,marks,q if question else VGroup())
def absent_plate(e):
    arc=Arc(radius=2.65,start_angle=.58*PI,angle=.32*PI).shift([-1.6,-.25,0])
    return VGroup(arc.copy().set_stroke(BG,20),
        DashedVMobject(arc.set_stroke(LIGHT,7),num_dashes=10))
def loss_labels():
    # Leader and bracket stop on the ectoderm, above the brown endoderm.
    return VGroup(label('neural plate: absent',[-4.5,2.35,0],LIGHT),
        Line([-4.3,2.05,0],[-3.4,1.65,0],color=LIGHT),
        label('dorsal structures lost',[-1.6,-3.35,0],LIGHT,30),
        label('BMP signaling\nstays high',[3.6,1.3,0],YELLOW,30),
        Line([1.2,.15,0],[1.2,1.7,0],color=YELLOW,stroke_width=4),
        Line([1.2,1.7,0],[.7,1.7,0],color=YELLOW),
        Line([1.2,.15,0],[.98,.15,0],color=YELLOW))
def lost_stage():
    e=embryo([-1.6,-.25,0],2.65); e[2].set_opacity(0)
    return VGroup(head('Without the three catchers'),e,absent_plate(e),loss_labels())
def membrane():
    bar=Line([-6,-1.75,0],[6,-1.75,0],color=LIGHT,stroke_width=8)
    rs=VGroup(*[RoundedRectangle(width=1.9,height=.7,corner_radius=.16,stroke_color=GREY,
         fill_color=GREY,fill_opacity=.3).move_to([x,-1.62,0]) for x in [-3.8,0,3.8]])
    return VGroup(bar,rs,label('outside',[-5.25,2.4,0],LIGHT),label('cell',[-5.45,-2.75,0],LIGHT))
def dial(p=(0,0,0),r=1.7,low=True):
    # Tick labels sit inside the face, under the arc, so the outline never crosses them.
    face=Circle(radius=r,color=LIGHT,stroke_width=5)
    arc=Arc(radius=r*.8,start_angle=.18*PI,angle=.64*PI,color=YELLOW,stroke_width=6)
    hand=Line(ORIGIN,[-r*.58,r*.47,0] if low else [r*.58,r*.47,0],color=YELLOW,stroke_width=8)
    return VGroup(face,arc,hand,label('Smad1',[0,-r*.42,0],YELLOW,32),
        label('low',[-r*.62,0,0],LIGHT,26),label('high',[r*.62,0,0],LIGHT,26)).shift(np.array(p))

class S00Title(TitleCard):
    LESSON='Neural Induction: The Default Model'
    TITLE="The Organizer's Catchers"

class S01(SpokenScene):
    def construct(self):
        e=gastrula().shift(LEFT*2.4)
        self.add(e,head("The Organizer's Catchers"),label('organizer',[-4.8,-3.2,0],PURPLE))
        self.at('makes skin')
        self.play(FadeIn(chip('BMP → skin',ORANGE,34).move_to([3.3,.7,0])),run_time=.4)
        self.at('what should')
        q=label('?',[-6.1,-.5,0],TEXT,190)
        self.play(FadeIn(q,scale=.6),run_time=.35)
        self.finish()

class S02(SpokenScene):
    def construct(self):
        e=embryo([4.0,-.25,0],2.35)
        self.add(e,head("The Organizer's Catchers"),label('organizer',[1.0,-1.65,0],PURPLE),
            Line([1.7,-1.38,0],[1.66,-.7,0],color=PURPLE))
        start=np.array([1.6,-.4,0])
        def slide(name,x,run):
            c=catcher(name,[x,.5,0],.8)
            target=c.get_center(); c.shift(start-target)
            self.play(FadeIn(c,run_time=.2),c.animate.move_to(target),run_time=run)
        self.at('Something that blocks')
        slide('Noggin',-5.4,1.1)
        self.at('It makes')
        slide('Chordin',-3.2,.8)
        self.at('such proteins')
        slide('Follistatin',-1.0,.8)
        self.finish()

class S03(SpokenScene):
    def construct(self):
        g=source_map(False); self.add(g,head('Before and during gastrulation'))
        self.at('are made early')
        glow=source_map()[5]; tag=source_tag()
        self.play(Create(glow),FadeIn(tag),run_time=.45)
        self.at('in dorsal animal cells')
        self.play(FadeIn(label('made in dorsal\nanimal cells',[0,.4,0],GREEN,28)),run_time=.4)
        self.finish()

class S04(SpokenScene):
    def construct(self):
        g=source_map(); self.add(g,head('Neural induction starts before gastrulation'),source_tag())
        # The timing note sits between the two maps, clear of the rings.
        note=label('BMP blockers\nalready made;\ngastrulation\nnot yet started',[0,.35,0],GREEN,26)
        self.add(note,Arrow([-1.3,-1.15,0],[1.3,-1.15,0],color=LIGHT,buff=0))
        self.at('neural induction starts')
        self.play(Indicate(g[5],color=GREEN,scale_factor=1.04),run_time=.5)
        self.finish()

class S05(SpokenScene):
    def construct(self):
        e=gastrula(); self.add(e,head('Gastrulation'),label('ectoderm',[3.9,1.4,0],LIGHT),
            Line([2.9,1.4,0],[2.25,1.1,0],color=LIGHT))
        mes=VGroup(*[cell([-2.6,-.7,0],.23,PURPLE) for _ in range(5)])
        self.at('the organizer and dorsal mesoderm')
        self.play(FadeIn(mes),run_time=.3)
        self.at('turn inward')
        ends=[[-1.85,.75,0],[-1.25,1.45,0],[-.5,1.85,0],[.35,1.85,0],[1.15,1.4,0]]
        paths=[VMobject().set_points_smoothly([[-2.6,-.7,0],[-1.95,-.65,0],[-2,.15,0],p]) for p in ends]
        self.play(LaggedStart(*[MoveAlongPath(m,p) for m,p in zip(mes,paths)],lag_ratio=.12),run_time=1.65)
        self.at('This is involution')
        a=CurvedArrow([-3.3,-.6,0],[-2.05,.25,0],angle=-PI*.65,color=PURPLE)
        self.play(Create(a),FadeIn(label('involution',[-4.5,.5,0],PURPLE,32)),run_time=.4)
        self.finish(); self.wait(1)

class S06(SpokenScene):
    def construct(self):
        e=gastrula(); mes=VGroup(*[cell(p,.23,PURPLE) for p in [[-1.85,.75,0],[-1.25,1.45,0],[-.5,1.85,0],[.35,1.85,0],[1.15,1.4,0]]])
        self.add(e,mes,head('Gastrulation'))
        self.at('secretes all three')
        ds=VGroup(*[dot(p) for p in [[-1.85,1,0],[-1.25,1.7,0],[-.5,2.1,0]]]); self.add(ds)
        self.play(ds.animate.shift(UP*.45),FadeIn(label('Noggin · Chordin · Follistatin',[0,-3.35,0],GREEN)),run_time=.7)
        self.at('becomes the neural plate')
        self.play(e[0][2].animate.set_color(BLUE),FadeIn(label('neural plate',[-4.4,2,0],BLUE)),
                  Create(Line([-3.1,2,0],[-1.4,2.05,0],color=BLUE)),run_time=.5)
        self.finish()

class S07(SpokenScene):
    def construct(self):
        c=cell([-3,-.25,0],2.3,PURPLE)
        n=catcher('Noggin',[-3,-.1,0],1)
        self.add(c,n,head('1992 · William Smith and Richard Harland'),label('organizer cell',[-3,-3.1,0],PURPLE))
        self.at('secreted protein')
        cap=label('Noggin: a secreted protein\nmade by the organizer cell',[3.4,1.7,0],LIGHT,30)
        self.play(FadeIn(cap),n.animate.shift(RIGHT*6.25),GrowArrow(Arrow([-.7,-.1,0],[1.7,-.1,0],color=GREEN,buff=0)),run_time=.9)
        self.finish()

class S08(SpokenScene):
    def construct(self):
        g=cap_stage(); self.add(g[0],g[1],g[2])
        self.at('added noggin protein')
        n=g[3]; n.shift(UP*2)
        self.add(n); self.play(n.animate.shift(DOWN*2),run_time=.65)
        self.at('What should the caps become')
        self.play(FadeIn(g[4]),run_time=.35)
        self.finish()
class S09Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(cap_stage()); self.wait(5)
class S10(SpokenScene):
    def construct(self):
        g=cap_stage(); self.add(g)
        self.at('neural tissue')
        self.play(FadeOut(g[4]),*[paint(c,BLUE) for c in g[2]],run_time=.4)
        self.at('without dorsal mesoderm')
        self.play(FadeIn(label('neural · no dorsal mesoderm',[0,-3.25,0],BLUE,32)),run_time=.35)
        self.at('acted on the ectoderm directly')
        self.play(Indicate(g[2],color=BLUE,scale_factor=1.04),run_time=.6)
        self.finish()
class S11Beat(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(cap_answer()); self.wait(2.5)

class S12(SpokenScene):
    def construct(self):
        self.add(head('Anterior · head end'))
        # Two large output panels keep the whole head from implying a neural fate.
        panels=VGroup(*[RoundedRectangle(width=5.2,height=5.8,corner_radius=.4,stroke_color=GREY,fill_color=GREY,fill_opacity=.06).move_to([x,-.25,0]) for x in [-3.1,3.1]])
        neutral_brain=RoundedRectangle(width=3.6,height=3.1,corner_radius=.8,color=GREY,fill_color=GREY,fill_opacity=.25).move_to([-3.1,-.2,0])
        neutral_gland=Ellipse(width=3.3,height=2.7,color=GREY,fill_color=GREY,fill_opacity=.25).move_to([3.1,-.2,0])
        self.add(panels,neutral_brain,neutral_gland)
        self.at('Forebrain is neural')
        brain=RoundedRectangle(width=3.6,height=3.1,corner_radius=.8,color=BLUE,fill_color=BLUE,fill_opacity=.45).move_to([-3.1,-.2,0])
        self.play(ReplacementTransform(neutral_brain,brain),FadeIn(label('forebrain',[-3.1,2,0],BLUE)),FadeIn(label('neural',[-3.1,-2.55,0],BLUE,32)),Create(Line([-3.1,1.7,0],[-3.1,1.35,0],color=BLUE)),run_time=.5)
        self.at('Cement gland')
        gland=Ellipse(width=3.3,height=2.7,color=ORANGE,fill_color=ORANGE,fill_opacity=.4).move_to([3.1,-.2,0])
        self.play(ReplacementTransform(neutral_gland,gland),FadeIn(label('cement gland',[3.1,2,0],ORANGE)),Create(Line([3.1,1.7,0],[3.1,1.15,0],color=ORANGE)),run_time=.4)
        self.at('is not')
        self.play(FadeIn(label('non-neural',[3.1,-2.55,0],ORANGE,32)),run_time=.3)
        self.finish(); self.wait(1)

class S13(SpokenScene):
    def construct(self):
        c=cell([-2.8,-.55,0],2.3,PURPLE); gene=chip('Chordin gene',LIGHT,32).move_to([-2.8,-.55,0])
        self.add(c,gene,head('1994 · Yoshiki Sasai and colleagues'),
            label('Eddy De Robertis laboratory',[0,2.55,0],LIGHT,30),label('organizer cell',[-2.8,-3.25,0],PURPLE))
        self.at('was cloned')
        self.play(gene.animate.set_color(GREEN),Flash(gene,color=GREEN,flash_radius=1.5),run_time=.6)
        self.at('and colleagues')
        n=catcher('Chordin',[-2.8,-.55,0],1)
        self.play(FadeIn(n),n.animate.shift(RIGHT*6),GrowArrow(Arrow([-.4,-.55,0],[1.6,-.55,0],color=GREEN,buff=0)),run_time=.8)
        self.finish()

class S14(SpokenScene):
    def construct(self):
        mem=membrane(); b=dimer([0,1.3,0]); self.add(mem,b,head('BMP4: free versus caught'))
        # Short free-ligand reference, then reset all receptors before the caught case.
        self.play(b.animate.shift(DOWN*2.1),mem[1][1].animate.set_fill(PINK,1).set_stroke(PINK),run_time=.65)
        self.at('Both')
        self.play(FadeOut(b),mem[1][1].animate.set_fill(GREY,.3).set_stroke(GREY),run_time=.25)
        bs=VGroup(dimer([-3,.5,0]),dimer([3,.5,0]))
        cs=VGroup(catcher('Noggin',[-3,.5,0]),catcher('Chordin',[3,.5,0]))
        self.add(bs)
        self.at('bind')
        self.play(Create(cs),run_time=.45)
        self.at('keep it off its receptors')
        self.play(FadeIn(label('receptors stay unlit',[0,-2.85,0],LIGHT,32)),
            Create(Line([-2.0,-2.7,0],[-3.4,-2.15,0],color=LIGHT)),
            Create(Line([2.0,-2.7,0],[3.4,-2.15,0],color=LIGHT)),run_time=.5)
        self.finish()

class S15(SpokenScene):
    def construct(self):
        c=catcher('Follistatin',[-3,.6,0],1.3)
        ligand=cell([-3,.6,0],.64,LIGHT)
        self.add(head('Follistatin'),ligand,label('activin',[-3,2.45,0],LIGHT,32))
        self.at('protein that binds')
        self.play(Create(c),FadeIn(label('binds activin best',[-3,-2.7,0],GREEN)),run_time=.5)
        self.at('also neuralizes caps')
        cap=tissue().move_to([3,-.2,0])
        self.add(cap)
        self.play(*[paint(x,BLUE) for x in cap],GrowArrow(Arrow([-.9,-.15,0],[.1,-.15,0],color=GREEN,buff=0)),
                  FadeIn(label('also neuralizes caps',[3,-2.05,0],BLUE)),run_time=.55)
        self.at('binds some')
        b=dimer([-.9,-1.0,0],'BMP',.3)[0]
        self.play(FadeIn(b),GrowArrow(Arrow([-1.15,-.78,0],[-1.98,-.36,0],color=GREEN,buff=0,stroke_width=5)),
                  FadeIn(label('also some BMPs',[-.9,-1.85,0],YELLOW)),run_time=.4)
        self.finish()

class S16(SpokenScene):
    def construct(self):
        mem=membrane(); self.add(mem,head('Follistatin: docking without signaling'))
        free=dimer([0,-.35,0],'BMP',1)
        self.add(free); mem[1][1].set_fill(PINK,1).set_stroke(PINK)
        self.at('can stay bound')
        self.play(FadeOut(free),mem[1][1].animate.set_fill(GREY,.3).set_stroke(GREY),run_time=.25)
        b=dimer([0,.35,0],'BMP',1); b[1].set_y(2.7)
        # An open upper grip stays entirely above the membrane and receptor.
        c=Arc(radius=1.9,start_angle=0,angle=PI,color=GREEN,stroke_width=14).shift([0,.35,0])
        name=label('Follistatin',[4,.35,0],GREEN,32)
        lead=Line([2,.35,0],[2.65,.35,0],color=GREEN)
        group=VGroup(b,c,name,lead); self.play(FadeIn(group),run_time=.4)
        self.at('docks on its receptor')
        # BMP's lower edge meets the receptor's upper face; the green grip stays outside.
        self.play(group.animate.shift(DOWN*.7),run_time=.6)
        self.at('does not signal')
        self.play(FadeIn(label('inactive',[0,-2.5,0],LIGHT,34)),run_time=.4)
        self.finish()

class S17(SpokenScene):
    def construct(self):
        mem=membrane(); self.add(mem,head('Catchers stay outside'))
        names=VGroup(*[catcher(n,[x,.55,0],.95) for n,x in zip(['Noggin','Chordin','Follistatin'],[-3.8,0,3.8])]); self.add(names)
        self.at('needs to enter a cell')
        self.play(Indicate(mem[0],color=LIGHT,scale_factor=1),run_time=.4)
        self.at('Each grabs')
        self.play(FadeIn(VGroup(*[dimer([x,.55,0],'BMP') for x in [-3.8,0,3.8]])),run_time=.45)
        self.finish()

class S18(SpokenScene):
    def construct(self):
        b=dimer([0,.1,0],'BMP-7',1.05)[0]
        self.add(b,head('Noggin clasping BMP-7 (schematic)'),label('BMP-7',[0,2.45,0],YELLOW),
            label('The lesson’s structure viewer shows the real structure.',[0,-3.35,0],LIGHT,26))
        self.at('Noggin clasps')
        arcs=VGroup(grip('Noggin',[-.75,.1,0],1.55),grip('Noggin',[.75,.1,0],1.55).rotate(PI,about_point=[.75,.1,0]))
        self.play(Create(arcs),FadeIn(label('Noggin dimer',[-4.5,-1.8,0],GREEN)),
                  Create(Line([-3.25,-1.65,0],[-1.85,-.9,0],color=GREEN)),run_time=.6)
        self.at('covers the faces')
        patches=VGroup(*[RoundedRectangle(width=.55,height=1.9,corner_radius=.14,color=GOLD,fill_color=GOLD,fill_opacity=1).move_to([x,.1,0]) for x in [-1.8,1.8]])
        self.play(FadeIn(patches),FadeIn(label('receptor-binding faces',[3.2,-2.5,0],GOLD)),
                  Create(Line([2.9,-2.2,0],[1.85,-.95,0],color=GOLD)),run_time=.5)
        self.finish()

class S19(SpokenScene):
    def construct(self):
        self.add(head('The shuttling model'),
            RoundedRectangle(width=12.1,height=1.05,corner_radius=.15,stroke_color=LIGHT,fill_color=GREY,fill_opacity=.15).move_to([0,-2.1,0]),
            Arrow([-5.8,-2.1,0],[5.8,-2.1,0],color=LIGHT,buff=0),
            label('organizer · dorsal',[-4,-3.05,0],PURPLE),label('ventral',[4.7,-3.05,0],LIGHT),
            label('ectoderm',[0,-3.05,0],LIGHT))
        CX,CY=-3.9,.55
        bmp=VGroup(cell([CX-.05-.7,CY,0],1.0,YELLOW),cell([CX-.05+.7,CY,0],1.0,YELLOW),label('BMP',[CX-.05,CY+1.45,0],YELLOW,30))
        c=VMobject(color=GREEN,stroke_width=11).set_points_as_corners([
            [CX+2.1,CY+1.9,0],[CX-2.2,CY+1.9,0],[CX-2.2,CY-1.9,0],[CX+2.1,CY-1.9,0]])
        start=label('Chordin made here',[CX,CY+2.3,0],GREEN)
        self.add(bmp,c,start)
        self.at('travels toward the ventral side')
        cl=label('Chordin',[CX,CY+2.3,0],GREEN)
        self.play(ReplacementTransform(start,cl),run_time=.3)
        grp=VGroup(bmp,c,cl)
        self.play(grp.animate.shift(RIGHT*6.5),run_time=1.5)
        self.at('proteases cut')
        cx=CX+6.5
        protease=chip('Tolloid',LIGHT,30).next_to([cx-2.2,CY,0],LEFT,buff=0)
        up=VMobject(color=GREEN,stroke_width=11).set_points_as_corners([
            [cx+2.1,CY+1.9,0],[cx-2.2,CY+1.9,0],[cx-2.2,CY+.07,0]])
        lo=VMobject(color=GREEN,stroke_width=11).set_points_as_corners([
            [cx-2.2,CY-.07,0],[cx-2.2,CY-1.9,0],[cx+2.1,CY-1.9,0]])
        self.play(FadeIn(protease),FadeOut(cl),ReplacementTransform(c,VGroup(up,lo)),run_time=.4)
        self.at('release the')
        self.play(up.animate.shift(UP*.45),lo.animate.shift(DOWN*.12),bmp.animate.shift(RIGHT*2.6),
            FadeIn(label('BMP released here',[CX+6.5+2.55-.05,-.95,0],YELLOW,26)),run_time=.7)
        self.finish()

class S20(SpokenScene):
    def construct(self):
        cap=tissue(); self.add(cap,head('From caps to the whole embryo'))
        self.play(ReplacementTransform(cap,embryo()),run_time=.65)
        self.at('Does the embryo need them')
        self.play(FadeIn(label('Does the embryo need them?',[0,-3.35,0],size=32)),run_time=.4)
        self.finish()

class S21(SpokenScene):
    def construct(self):
        g=depleted_stage(); self.add(g[0],g[1],g[2],g[3])
        self.at('depleted')
        self.play(Create(g[4]),g[3].animate.fade(.3),run_time=.5)
        self.at('What happens to the neural plate')
        self.play(FadeIn(g[5]),run_time=.4)
        self.finish()
class S22Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; g=depleted_stage(); g[3].fade(.3); self.add(g); self.wait(5)
class S23(SpokenScene):
    def construct(self):
        g=depleted_stage(); g[3].fade(.3); self.add(g)
        self.at('lost their dorsal structures')
        dashed=absent_plate(g[2]); labs=loss_labels()
        self.play(FadeOut(g[5]),FadeOut(g[3]),FadeOut(g[4]),FadeOut(g[1]),FadeOut(g[2][2]),
            FadeIn(dashed),FadeIn(labs[0]),Create(labs[1]),FadeIn(labs[2]),run_time=.6)
        self.at('With all three')
        self.play(FadeIn(VGroup(*labs[3:])),run_time=.4)
        self.finish()
class S24Beat(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(lost_stage()); self.wait(2.5)

class S25(SpokenScene):
    def construct(self):
        e=embryo([-2,-.25,0],2.65); self.add(e,head('Reversade and colleagues · reverse test'))
        bs=VGroup(*[chip(n,YELLOW,30) for n in ['BMP2','BMP4','BMP7']]).arrange(DOWN,buff=.3).move_to([4,.65,0])
        self.at('group removed')
        self.play(FadeIn(bs),run_time=.3)
        self.play(Create(VGroup(*[strike(b) for b in bs])),bs.animate.fade(.5),run_time=.4)
        self.at('organizer signals were blocked')
        self.play(e[3].animate.set_color(GREY),
            FadeIn(label('organizer signals blocked',[-2,-3.35,0],LIGHT)),
            Create(Line([-4,-3.05,0],[-4.6,-.65,0],color=LIGHT)),
            FadeIn(label('UV treatment or\nbeta-catenin knockdown',[3.8,-2.45,0],LIGHT,26)),run_time=.5)
        self.at('formed massive amounts of brain')
        brain=Ellipse(width=3.5,height=1.8,color=BLUE,fill_color=BLUE,fill_opacity=.45).move_to([-2,.85,0])
        ecto=Arc(radius=2.65,start_angle=0,angle=PI,color=BLUE,stroke_width=16).shift([-2,-.25,0])
        self.play(FadeIn(brain),FadeIn(ecto),e[2].animate.set_color(BLUE),
            FadeIn(label('brain',[-2,.85,0],'#FFFFFF',36)),run_time=.6)
        self.finish()

class S26(SpokenScene):
    def construct(self):
        d=dial([.3,.35,0],2.1,False); fg=chip('FGF',TEAL,36).move_to([-4.9,.4,0]); ne=chip('neural',BLUE,32).move_to([4.9,.1,0])
        self.add(d,fg,ne,head('FGF · a second input'),label('nucleus',[.3,-2.2,0],LIGHT))
        self.at('in addition to blocking')
        blockade=label('BMP blockade + early FGF',[0,-3.5,0],GREEN,30)
        self.play(FadeIn(blockade),run_time=.4)
        self.at('turn the dial down through')
        mk=chip('MAPK',TEAL,28).move_to([-3,2.15,0])
        self.play(FadeIn(mk),GrowArrow(Arrow(fg.get_top(),mk.get_left(),buff=.12,color=TEAL)),
            GrowArrow(Arrow(mk.get_right(),[-1.15,1.5,0],buff=.12,color=TEAL)),
            Transform(d[2],Line([.3,.35,0],[.3-.58*2.1,.35+.47*2.1,0],color=YELLOW,stroke_width=8)),run_time=.7)
        self.at('It also does more')
        bypass=VMobject(color=BLUE,stroke_width=6).set_points_as_corners([[-4.9,-.1,0],[-4.9,-2.7,0],[4.9,-2.7,0],[4.9,-.65,0]])
        tip=Arrow([4.9,-1.05,0],[4.9,-.5,0],buff=0,color=BLUE)
        self.play(Create(bypass),GrowArrow(tip),FadeIn(label('does more than lower BMP',[0,-3.1,0],BLUE,28)),
            FadeOut(blockade),run_time=.6)
        self.finish(); self.wait(1.5)

class S27(SpokenScene):
    def construct(self):
        self.add(head('Catchers plus a second input'))
        mem=Line([-6,.2,0],[6,.2,0],color=LIGHT,stroke_width=7)
        d=dial([-1.65,-1.7,0],1.35,True)
        nuc=Ellipse(width=4.3,height=3.2,color=LIGHT).move_to([-1.65,-1.7,0])
        cs=VGroup(*[catcher(n,[x,1.8,0],.8) for n,x in zip(['Noggin','Chordin','Follistatin'],[-4.4,-1.4,1.6])])
        bs=VGroup(*[dimer([x,1.8,0],'BMP',.24) for x in [-4.4,-1.4,1.6]])
        for b in bs: b[1].set_y(2.85)
        fg=chip('FGF',TEAL,32).move_to([4.5,1.9,0]); ne=chip('neural',BLUE,30).move_to([4.5,-1.8,0])
        fa=Arrow([4.5,1.35,0],[4.5,-1.2,0],color=TEAL,buff=0)
        hold=VGroup(Line([-2.9,.2,0],[-2.5,-.93,0],color=GREEN,stroke_width=5),
                    Line([-2.783,-1.03,0],[-2.217,-.83,0],color=GREEN,stroke_width=7))
        self.add(mem,nuc,d,cs,bs,fg,ne,fa,label('nucleus',[1.75,-2.9,0],LIGHT),
            Line([.95,-2.8,0],[.2,-2.6,0],color=LIGHT,stroke_width=3),
            label('cell membrane',[-5.2,-.35,0],LIGHT,26),
            label('second input',[4.5,-2.75,0],TEAL),hold)
        self.at('embryo needs the catchers')
        self.play(Indicate(cs,color=GREEN,scale_factor=1.03),run_time=.45)
        self.at('keep the dial down')
        self.play(Indicate(d[2],color=GREEN,scale_factor=1.05),Indicate(hold,color=GREEN,scale_factor=1.1),run_time=.4)
        self.at('adds a second input')
        self.play(Indicate(fa,color=TEAL,scale_factor=1.05),run_time=.4)
        self.finish()

class S28End(EndCard):
    LINE='The frog embryo needs the catchers to keep the dial down.\nFGF adds a second input.'
    def construct(self):
        # The fix brief explicitly requires the complete two-line takeaway.
        a=label('The frog embryo needs the catchers to keep the dial down.',[0,.6,0],size=34)
        b=label('FGF adds a second input.',[0,-.35,0],TEAL,38)
        self.add(a,b,label('biochemistrypedia.com',[0,-1.65,0],TEAL))
        self.finish()
