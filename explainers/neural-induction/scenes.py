"""Chapter 1 — The Map and the Question.

COLOR MAP (shared with scenes.old.py):
GREY = uncommitted ectoderm, outlines, labels
ORANGE = epidermis / skin; BLUE = neural fate
YELLOW = BMP / BMP4; GREEN = organizer BMP antagonists
PURPLE = organizer / dorsal mesoderm; PINK = BMP receptor
RED = jammed receptor. FGF and neutral anatomy use GREY.
Geometric anatomical cartoons, not quantitative plots or molecular structures.
"""
import numpy as np
from bp_style import *

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
PINK = "#E58AC0"
# Exact audio alignment; avoid the pipeline log's misleading pre-wait timestamps.
class SpokenScene(SpokenScene):
    def at(self, phrase, lead=0.1, nth=0):
        remaining = self.t_of(phrase, nth) - lead - self.elapsed()
        if remaining > 0.02:
            self.wait(remaining)


# Cell and grid helpers retain the reference film's geometry and palette.
def cell(p, r=0.42, color=GREY):
    return Circle(radius=r, stroke_color=color, stroke_width=3,
                  fill_color=color, fill_opacity=0.28).move_to(p)

def paint(c, color):
    return c.animate.set_stroke(color).set_fill(color, 0.32)

def grid_pos(rows, cols, pitch, center=(0, 0)):
    return [np.array([center[0]+(j-(cols-1)/2)*pitch,
                      center[1]+((rows-1)/2-i)*pitch, 0])
            for i in range(rows) for j in range(cols)]

def label(s, x, y, size=30, color=TEXT):
    return T(s, size=max(30,size), color=TEXT if color == GREY else color).move_to([x,y,0])

def sheet(color=GREY, center=(0,0), flat=False):
    if flat:
        return VGroup(*[RoundedRectangle(width=1.12,height=0.68,corner_radius=0.12,
            stroke_color=color,fill_color=color,fill_opacity=0.28).move_to(p)
            for p in grid_pos(2,5,1.15,center)])
    return VGroup(*[cell(p,0.49,color) for p in grid_pos(2,5,1.0,center)])

def blastula(center=(0,0), scale=1, fluid=False):
    c=np.array([*center,0.])
    ring=VGroup(*[cell(c+2.65*scale*np.array([np.cos(a),np.sin(a),0]),0.34*scale)
                 for a in [PI/2+TAU*k/24 for k in range(24)]])
    for k in (21,22,23,0,1,2,3):
        ring[k].set_fill(ORANGE,0.38).set_stroke(ORANGE)
    for k in range(9,16):
        ring[k].set_fill(GREY,0.65)
    cavity=Circle(radius=2.29*scale,stroke_width=0,fill_color=BLUE,
                  fill_opacity=0.12 if fluid else 0).move_to(c)
    return VGroup(cavity,ring)

def cap_of(b):
    return VGroup(*[b[1][k] for k in (21,22,23,0,1,2,3)])

def pocket_shape(L=2.0):
    """The blastopore groove: a filled pocket folding inward from the lower-left surface."""
    ang=5*PI/4
    u=np.array([np.cos(ang),np.sin(ang),0])
    r=Polygon([-0.34,L/2,0],[0.34,L/2,0],[0.1,-L/2,0],[-0.1,-L/2,0],stroke_color=TEXT,stroke_width=4,
        fill_color=GREY,fill_opacity=0.55).round_corners(0.1).rotate(-PI/4)
    return r.move_to((2.9-L/2)*u)

def gastrula(L=2.0):
    b=blastula(fluid=True)
    b[1][9].set_opacity(0)   # the slit the pocket folds out of
    return VGroup(b,pocket_shape(L))

def host_ring(host):
    """Host embryo: only the animal and dorsal/ventral ectoderm is skin-coloured; the floor stays grey."""
    for k in list(range(16,24))+list(range(0,7)):
        host[1][k].set_stroke(ORANGE).set_fill(ORANGE,0.3)
    for k in range(7,16):
        host[1][k].set_stroke(GREY).set_fill(GREY,0.45)
    return host

def organized(L=2.0):
    g=gastrula(L)
    g[0][1][7].set_stroke(PURPLE).set_fill(PURPLE,0.6)
    return g

def skin_icon(center=(0,0), small=False):
    g=sheet(ORANGE,center,flat=True)
    if small: g.scale(0.58)
    return g

def neural_icon():
    # A schematic brain silhouette and cord; no molecular geometry.
    brain=VGroup(Ellipse(width=1.0,height=1.2,color=BLUE,fill_opacity=0.24),
                 Ellipse(width=1.0,height=1.2,color=BLUE,fill_opacity=0.24).shift(RIGHT*0.7))
    cord=RoundedRectangle(width=0.32,height=1.8,corner_radius=0.13,
        color=BLUE,fill_opacity=0.3).move_to([0.35,-1.3,0])
    return VGroup(brain,cord)

def dish_state(answer=False, question=False):
    dish=RoundedRectangle(width=8.1,height=3.35,corner_radius=0.45,
        color=GREY,fill_color=BLUE,fill_opacity=0.06).move_to([0,-0.25,0])
    cap=sheet(ORANGE if answer else GREY,(0,0),flat=answer)
    salt=label('salt solution',0,-2.2,30)
    head=label('animal-cap explant',0,2.7,30)
    g=VGroup(dish,cap,salt,head)
    if question: g.add(label('Alone, what does it become?',0,1.9,32))
    if answer:
        g.add(label('epidermis · the control',0,1.9,32,ORANGE),
              label('No organizer tissue attached',0,-3.05,26,GREY))
    return g

PUZ=['What holds an intact cap as skin?',
     'What does the organizer send?',
     'Beyond the cap: embryo, fly, chick?']

def prow(i,y,on=False):
    box=RoundedRectangle(width=11.8,height=1.7,corner_radius=0.2,color=GREY,fill_opacity=0.06).move_to([0,y,0])
    num=label(str(i+1),-5.2,y,40,TEAL)
    txt=label(PUZ[i],0.4,y,34)
    row=VGroup(box,num,txt)
    if not on: dim_row(row)
    return row

def dim_row(row):
    row[0].set_stroke(opacity=0.3); row[0].set_fill(opacity=0.02)
    row[1].set_opacity(0.4); row[2].set_opacity(0)

ROW_Y=[2.1,0.0,-2.1]

DC=np.array([-3.0,0.,0])
DS=1.15

def dial(high=False):
    center=DC
    nucleus=Arc(radius=2.85,start_angle=3*PI/4,angle=3*PI/2,color=GREY,stroke_width=3).move_arc_center_to(center)
    face=Arc(radius=2.25,start_angle=PI/4,angle=PI/2,color=TEXT,stroke_width=5).move_arc_center_to(center)
    ticks=VGroup(*[Line(center+2.12*np.array([np.cos(a),np.sin(a),0]),
                       center+2.38*np.array([np.cos(a),np.sin(a),0]),color=TEXT)
                   for a in np.linspace(PI/4,3*PI/4,9)])
    a=PI/4 if high else 3*PI/4
    needle=Arrow(center,center+2.0*np.array([np.cos(a),np.sin(a),0]),buff=0,color=YELLOW,stroke_width=7)
    g=VGroup(nucleus,face,needle,Dot(center,radius=0.12,color=YELLOW),
        label('low · neural',center[0]-1.55,2.68,30,BLUE),
        label('high · skin',center[0]+1.65,2.68,30,ORANGE),ticks,
        label('Smad1 activity',center[0],-0.7,30,YELLOW),
        label('(Smad1 shown)',center[0],-1.25,30),
        label('nucleus',center[0],-2.0,30))
    return g.scale(DS,about_point=center)

def scope(x=0,y=3.3):
    return label('early frog animal caps',x,y,32)

CELL=np.array([1.4,-1.75,0])

def decision(color=BLUE):
    # The dial feeds this decision cell; FGF joins it from below.
    return VGroup(cell(CELL,0.6,color),label('neural' if color==BLUE else 'skin',2.9,-1.75,32,color),
                  Arrow([DC[0]+np.sqrt((2.85*DS)**2-1.75**2)+0.03,-1.75,0],[0.74,-1.75,0],color=YELLOW,stroke_width=5,buff=0))

def fgf(dim=False):
    # Separate input joins the same decision cell from below; never the needle.
    return VGroup(label('FGF input',4.75,-2.85,30),
        Line([3.65,-2.85,0],[1.4,-2.85,0],color=TEXT,stroke_width=4),
        Arrow([1.4,-2.85,0],[1.4,-2.4,0],color=TEXT,stroke_width=4,buff=0,max_tip_length_to_length_ratio=0.5)).set_opacity(0.5 if dim else 1)

class S00Title(TitleCard):
    LESSON='Neural Induction: The Default Model'
    TITLE='The Map and the Question'
    def construct(self):
        self.add(label('BIOCHEMISTRYPEDIA',0,1.65,30,TEAL),
                 label(self.LESSON,0,0.8,32),
                 T(self.TITLE,size=50,font=TITLE_FONT).move_to([0,-0.3,0]),
                 Line([-1.3,-1.15,0],[1.3,-1.15,0],color=GOLD))
        self.finish()

class S01(SpokenScene):
    def construct(self):
        cells=sheet(center=(0,1.4)).scale(1.2)
        self.add(cells,label('ectoderm',0,2.8,36))
        self.at('can become')
        self.play(Create(VGroup(Arrow([-1,0.5,0],[-3,-0.5,0],color=TEXT),
                               Arrow([1,0.5,0],[3,-0.5,0],color=TEXT))),run_time=0.25)
        self.at('skin')
        self.play(FadeIn(skin_icon((-3.3,-1.35),True)),FadeIn(label('skin',-3.3,-2.8,34,ORANGE)),run_time=0.25)
        self.at('nervous system')
        self.play(FadeIn(neural_icon().scale(0.8).move_to([3.3,-1.65,0])),
                  FadeIn(label('nervous system',3.3,-3.15,34,BLUE)),run_time=0.3)
        self.at('What decides')
        self.play(Transform(cells, cells.copy().set_stroke(TEXT)),FadeIn(label('What decides?',0,-1.5,36)),run_time=0.3)
        self.finish()

class S02(SpokenScene):
    def construct(self):
        b=blastula(); self.add(b,label('animal pole\nectoderm',4.7,1.65,30),label('vegetal floor\nendoderm',4.7,-1.65,30),Line([3.35,1.8,0],[1.85,2.2,0],color=TEXT),Line([3.35,-1.8,0],[1.85,-2.2,0],color=TEXT))
        self.at('A blastula')
        self.play(FadeIn(label('frog blastula',0,3.3,34)),run_time=0.4)
        self.at('hollow ball')
        self.play(Indicate(b[1],color=TEXT,scale_factor=1.04),run_time=0.65)
        self.finish()

class S03(SpokenScene):
    def construct(self):
        b=blastula(); self.add(b,label('frog blastula',0,3.3,34))
        self.at('Inside is')
        self.play(b[0].animate.set_fill(BLUE,0.12),run_time=0.6)
        self.at('the blastocele')
        self.play(FadeIn(label('blastocoel',0,0,30,BLUE)),run_time=0.4)
        self.at('The roof')
        self.play(*[paint(c,TEXT) for c in cap_of(b)],run_time=0.6)
        self.at('animal cap')
        self.play(FadeIn(label('animal cap',4.35,2.75,30)),
            Create(Line([3.2,2.7,0],[0,2.98,0],color=TEXT)),run_time=0.4)
        self.finish()

class S04(SpokenScene):
    def construct(self):
        b=blastula(fluid=True); cap_of(b).set_color(TEXT)
        head=label('frog blastula',0,3.3,34)
        self.add(b,head)
        self.at('cap is ectoderm')
        ecto=label('ectoderm',-5.0,2.85,34)
        lead=Line([-3.85,2.7,0],[-1.95,2.15,0],color=TEXT)
        self.play(FadeIn(ecto),Create(lead),run_time=0.4)
        self.at('gives rise')
        self.play(b.animate.scale(0.75).shift(LEFT*3.5),head.animate.move_to([-3.5,3.45,0]),
                  ecto.animate.move_to([-3.5,2.88,0]),FadeOut(lead),run_time=0.4)
        lead2=Line([-3.5,2.66,0],[-3.5,2.36,0],color=TEXT)
        self.add(lead2)
        self.at('the skin')
        skin=skin_icon((3,1.1),True)
        self.play(FadeIn(skin),GrowArrow(Arrow([-1.8,1.4,0],[1.2,1.4,0],color=GREY)),run_time=0.45)
        self.play(FadeIn(label('skin',3,2.05,27,ORANGE)),run_time=0.2)
        self.at('the nervous system')
        neu=neural_icon().scale(0.75).move_to([3,-1.5,0])
        self.play(FadeIn(neu),GrowArrow(Arrow([-1.8,0.3,0],[1.7,-1.1,0],color=GREY)),run_time=0.4)
        self.play(FadeIn(label('nervous system',3,-3.05,27,BLUE)),run_time=0.2)
        self.finish()
        if self.elapsed()<8.2: self.wait(8.2-self.elapsed())

class S05(SpokenScene):
    def construct(self):
        skin=skin_icon((0,0)); self.add(skin,label('epidermis',0,2.6,40,ORANGE),label('outer layer of skin',0,-2.6,32))
        self.at('outer layer')
        self.play(skin.animate.scale(1.6),run_time=0.6)
        self.at('the epidermis')
        self.play(Create(Line([-4.5,1.55,0],[4.5,1.55,0],color=ORANGE,stroke_width=6)),run_time=0.45)
        self.at('Keep that word')
        self.play(Indicate(skin,color=ORANGE,scale_factor=1.03),run_time=0.6)
        self.finish()

class S06(SpokenScene):
    def construct(self):
        b=blastula(fluid=True); head=label('frog blastula',0,3.3,34); self.add(b,head)
        self.at('is the set')
        g=gastrula(0.8)
        self.play(b.animate.scale(0.62).shift(LEFT*3.8),head.animate.shift(LEFT*3.8),FadeIn(g.scale(0.9).shift(RIGHT*2.9)),
                  FadeIn(label('gastrulation',2.9,3.3,34)),run_time=0.55)
        self.at('cell movements')
        deeper=gastrula(1.4).scale(0.9).shift(RIGHT*2.9)
        self.play(Transform(g[1],deeper[1]),run_time=0.8)
        self.finish()

class S07(SpokenScene):
    def construct(self):
        g=gastrula(1.4); self.add(g,label('frog gastrula',0,3.3,34))
        self.at('at the blastopore')
        self.play(FadeIn(label('blastopore',-4.7,-2.95,32)),
            Create(Line([-3.5,-2.8,0],[-2.3,-2.25,0],color=TEXT)),run_time=0.4)
        self.at('where cells')
        arrows=VGroup(Arrow([-4.0,-0.9,0],[-2.8,-1.95,0],color=TEXT,stroke_width=6,buff=0),
                      Arrow([-0.1,-3.5,0],[-1.45,-2.9,0],color=TEXT,stroke_width=6,buff=0))
        self.play(GrowArrow(arrows[0]),GrowArrow(arrows[1]),Transform(g[1],gastrula(2.0)[1]),run_time=0.8)
        self.finish()

class S08(SpokenScene):
    def construct(self):
        g=gastrula(); self.add(g,label('frog gastrula',0,3.3,34))
        self.at("blastopore's dorsal lip")
        self.play(paint(g[0][1][7],PURPLE),FadeIn(label('dorsal lip',-4.6,0.3,32,PURPLE)),
                  Create(Line([-3.4,0.1,0],[-2.58,-0.68,0],color=PURPLE)),run_time=0.45)
        self.at('is the')
        self.play(FadeIn(label('organizer',-4.6,-0.4,34,PURPLE)),run_time=0.35)
        self.finish()

class S09(SpokenScene):
    def construct(self):
        g=organized(); self.add(g,label('frog gastrula',0,3.3,34))
        self.at('Dorsal is')
        self.play(FadeIn(label('dorsal · back',-4.65,2.5,30)),
            GrowArrow(Arrow([-3.5,2.1,0],[-2.45,1,0],color=TEXT,stroke_width=5,buff=0)),run_time=0.4)
        self.at('neural plate')
        plate=Arc(radius=3.07,start_angle=2.45,angle=0.65,color=BLUE,stroke_width=13)
        self.play(Create(plate),FadeIn(label('neural plate',-4.7,0.8,30,BLUE)),run_time=0.45)
        self.at('Ventral',lead=0.35)
        self.play(FadeIn(label('ventral · belly',4.65,-2.5,30)),
            GrowArrow(Arrow([3.5,-2.1,0],[2.45,-1.0,0],color=TEXT,stroke_width=5,buff=0)),run_time=0.3)
        self.finish()

def graft_stage():
    donor=organized().scale(0.7).move_to([-4.2,-0.4,0])
    host=host_ring(blastula(center=(2.2,-0.4),scale=0.9,fluid=True))
    graft=cell([4.5,-1.02,0],0.28,PURPLE)
    return VGroup(donor,host,graft)

class S10(SpokenScene):
    def construct(self):
        stage=graft_stage()
        tissue=stage[0][0][1][7]
        host=stage[1]
        ventral_tick=VGroup(Line([4.98,-0.4,0],[5.28,-0.4,0],color=TEXT,stroke_width=6),label('ventral',5.9,-0.4,26))
        site=label('graft site:\nventral side\nof host',2.0,-0.3,30)
        site_leader=Line([3.25,-0.75,0],[4.25,-0.98,0],color=TEXT)
        self.add(stage[0],host,label('donor',-4.2,2.85,34),label('host',2.2,2.85,34),
                 label('1920s · Hilde Mangold & Hans Spemann',0,3.5,32),
                 ventral_tick,site,site_leader)
        self.at('grafted an organizer')
        self.play(tissue.animate.move_to([0,1.2,0]),run_time=0.8)
        self.at('into another embryo')
        self.play(tissue.animate.move_to(stage[2]),run_time=0.8)
        self.finish()

def body(x,scale=1.0,color=TEXT):
    trunk=Polygon([-0.5,1.0,0],[0.5,1.0,0],[0.28,-1.0,0],[0.12,-1.85,0],[-0.12,-1.85,0],[-0.28,-1.0,0],
                  color=color,fill_opacity=0.08).round_corners(0.12)
    head=Circle(radius=0.42,color=color,fill_opacity=0.08).move_to([0,1.42,0])
    return VGroup(trunk,head).scale(scale).move_to([x,0,0])

class S11(SpokenScene):
    def construct(self):
        host=host_ring(blastula(scale=1.1,fluid=True))
        graft=cell([2.82,-0.76,0],0.33,PURPLE)
        axis1=body(-1.1,1.1)
        self.add(host,graft,axis1,label('host axis',-5.0,1.4,32),Line([-3.7,1.2,0],[-1.7,0.9,0],color=TEXT))
        self.at('a second body axis')
        axis2=body(1.1,1.1)
        self.play(Create(axis2),FadeIn(label('second axis',5.0,1.4,32)),
                  Create(Line([3.65,1.2,0],[1.65,0.9,0],color=TEXT)),run_time=0.55)
        self.at('change what nearby')
        near=VGroup(*[host[1][k] for k in (16,17,18,19)])
        self.play(*[paint(c,BLUE) for c in near],axis2.animate.set_color(BLUE),run_time=0.7)
        self.finish()

class S12(SpokenScene):
    def construct(self):
        org=chip('organizer',PURPLE,36).move_to([-3.7,0,0])
        cells=sheet(center=(2.2,0)).scale(1.15)
        self.add(org,cells,label('ectoderm',2.2,-1.6,34))
        self.at('the question was')
        self.play(FadeIn(label('A positive neural signal?',0,3.1,38)),run_time=0.3)
        self.at('positive signal')
        q=label('?',-3.7,1.5,76); self.play(FadeIn(q),run_time=0.3)
        self.at('organizer sends')
        self.play(q.animate.move_to([-0.5,1.6,0]),run_time=0.7)
        self.at('make ectoderm neural')
        self.play(q.animate.move_to([2.2,1.6,0]),run_time=0.6)
        self.finish()

class S13(SpokenScene):
    def construct(self):
        b=blastula(center=(-3.5,0),scale=0.78,fluid=True)
        dish=RoundedRectangle(width=5.1,height=2.6,corner_radius=0.35,
            color=GREY,fill_color=BLUE,fill_opacity=0.06).move_to([3.3,-0.4,0])
        head=label('animal-cap explant',3.3,2.2,30)
        salt=label('salt solution',3.3,-2.1,30)
        self.add(b,dish,head,salt)
        self.at('Cut out')
        cut=cap_of(b)
        self.play(cut.animate.shift(UP*0.65),run_time=0.6)
        self.at('culture it alone')
        cap=sheet(center=(3.3,-0.4)).scale(0.65)
        self.play(ReplacementTransform(cut,cap),run_time=0.7)
        self.at('salt solution')
        full=dish_state()
        self.play(FadeOut(b),FadeOut(head),FadeOut(salt),
                  ReplacementTransform(VGroup(dish,cap),VGroup(full[0],full[1])),
                  FadeIn(full[2]),FadeIn(full[3]),run_time=0.6)
        self.finish()

def choices():
    skin=skin_icon((-3.4,-3.05),True).scale(0.4)
    neural=neural_icon().scale(0.3).move_to([2.4,-3.05,0])
    return VGroup(skin,label('skin?',-1.8,-3.05,32,ORANGE),neural,label('neural?',4,-3.05,32,BLUE))

class S14(SpokenScene):
    def construct(self):
        self.add(dish_state())
        self.at('what should')
        self.play(FadeIn(label('Alone, what does it become?',0,1.9,32)),run_time=0.3)
        self.at('Make a guess')
        self.play(FadeIn(choices()),run_time=0.3)
        self.finish()

class S15Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(dish_state(question=True),choices(),label('Pause and decide',0,3.35,32,TEAL))
        timer=Line([-4.7,2.3,0],[4.7,2.3,0],color=TEAL,stroke_width=6)
        self.add(timer)
        self.play(timer.animate.stretch(0.01,0,about_point=[-4.7,2.3,0]),run_time=5,rate_func=linear)

class S16(SpokenScene):
    def construct(self):
        d=dish_state(question=True); self.add(d)
        self.at('It becomes')
        ans=dish_state(answer=True)
        self.play(FadeOut(d[4]),Transform(d[1],ans[1]),run_time=0.5)
        self.at('epidermis')
        self.play(FadeIn(ans[4]),run_time=0.4)
        self.at('No organizer tissue')
        self.play(FadeIn(ans[5]),run_time=0.4)
        self.finish()

class S17Beat(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(dish_state(answer=True)); self.wait(2.5)

class S18(SpokenScene):
    def construct(self):
        c=cell([-4.0,0.0,0],2.45)
        def dimer():
            return VGroup(RoundedRectangle(width=1.75,height=1.5,corner_radius=0.45,color=YELLOW,fill_opacity=0.35),
                RoundedRectangle(width=1.75,height=1.5,corner_radius=0.45,color=YELLOW,fill_opacity=0.35).shift(RIGHT*1.2))
        protein=dimer().move_to([-4.0,0.0,0])
        name=label('BMP',-4.0,1.15,40,YELLOW)
        self.add(c,protein,label('cell',-4.0,-2.0,34))
        self.at('BMPS')
        self.play(FadeIn(name),run_time=0.3)
        self.at('Bone Morphogenetic Proteins')
        full=label('bone morphogenetic\nproteins',3.4,2.65,36,YELLOW)
        self.play(FadeIn(full),run_time=0.4)
        self.at('are secreted signals')
        sec=label('secreted',-4.0,-1.15,36)
        sec.add_updater(lambda m: m.move_to([protein.get_center()[0],-1.15,0]))
        self.add(sec)
        self.play(protein.animate.move_to([3.0,0.0,0]),name.animate.move_to([3.0,1.2,0]),
                  run_time=1.3)
        sec.clear_updaters()
        self.at('of the')
        self.play(FadeIn(label('TGF-beta family',3.4,-2.45,34)),run_time=0.3)
        self.finish()

class S19(SpokenScene):
    def construct(self):
        c=RoundedRectangle(width=11.8,height=6.0,corner_radius=0.8,color=TEXT)
        n=Circle(radius=1.65,color=TEXT,fill_opacity=0.07).move_to([3.1,0,0])
        receptor=VGroup(Line([-5.9,0,0],[-4.7,0,0],color=PINK,stroke_width=10),
            Line([-5.9,-0.45,0],[-5.9,0.45,0],color=PINK,stroke_width=10))
        self.add(c,n,receptor,label('membrane',-4.4,3.35,30),label('receptor',-4.65,1,30,PINK),label('nucleus',3.1,-2.2,32))
        self.at('their signal')
        self.play(GrowArrow(Arrow([-4.5,0,0],[2.2,0,0],color=YELLOW,buff=0.1)),run_time=0.3)
        self.at('is carried')
        self.play(Indicate(receptor,scale_factor=1.05),run_time=0.3)
        for phrase,name,y in [('SMOD1','Smad1',0.9),('SMOD5','Smad5',0),('and SMOD8','Smad8',-0.9)]:
            self.at(phrase)
            carrier=chip(name,YELLOW,32).move_to([-3.4,0,0]).set_z_index(2)
            self.add(carrier)
            path=VMobject().set_points_as_corners([[-3.4,0,0],[0.9,0,0],[3.1,y,0]])
            self.play(MoveAlongPath(carrier,path),run_time=0.85,rate_func=smooth)
        self.finish()

def fly_icon():
    col=TEXT
    wings=VGroup(Ellipse(width=0.42,height=0.95,color=col,fill_opacity=0.12).rotate(0.6).move_to([-0.36,0.05,0]),
                 Ellipse(width=0.42,height=0.95,color=col,fill_opacity=0.12).rotate(-0.6).move_to([0.36,0.05,0]))
    legs=VGroup(*[Line([0,0.1+dy,0],[sx*(0.5+0.06*i),0.1+dy-0.18+0.14*i*0,0],color=col,stroke_width=3)
                  for sx in (-1,1) for i,dy in enumerate((0.12,0.0,-0.12))])
    abdomen=Ellipse(width=0.34,height=0.72,color=col,fill_opacity=0.3).move_to([0,-0.38,0])
    thorax=Ellipse(width=0.36,height=0.38,color=col,fill_opacity=0.3).move_to([0,0.08,0])
    head=Circle(radius=0.15,color=col,fill_opacity=0.3).move_to([0,0.4,0])
    eyes=VGroup(Dot([-0.1,0.44,0],radius=0.05,color=TEXT),Dot([0.1,0.44,0],radius=0.05,color=TEXT))
    return VGroup(legs,wings,abdomen,thorax,head,eyes).scale(1.35)

def chick_icon():
    col=TEXT
    body=Ellipse(width=1.05,height=0.85,color=col,fill_opacity=0.25).move_to([-0.1,-0.05,0])
    head=Circle(radius=0.3,color=col,fill_opacity=0.25).move_to([0.5,0.45,0])
    beak=Polygon([0.78,0.53,0],[1.08,0.43,0],[0.78,0.35,0],color=GOLD,fill_opacity=0.8)
    eye=Dot([0.58,0.52,0],radius=0.05,color=col)
    wing=Ellipse(width=0.55,height=0.3,color=col,fill_opacity=0.2).rotate(-0.4).move_to([-0.2,-0.02,0])
    tail=Polygon([-0.55,0.1,0],[-0.85,0.35,0],[-0.6,-0.1,0],color=col,fill_opacity=0.25)
    legs=VGroup(Line([-0.15,-0.46,0],[-0.15,-0.85,0],color=GOLD,stroke_width=4),
                Line([0.1,-0.46,0],[0.1,-0.85,0],color=GOLD,stroke_width=4),
                Line([-0.3,-0.85,0],[-0.05,-0.85,0],color=GOLD,stroke_width=4),
                Line([-0.05,-0.85,0],[0.2,-0.85,0],color=GOLD,stroke_width=4))
    return VGroup(legs,tail,body,wing,head,beak,eye).scale(1.0)

class S20(SpokenScene):
    def construct(self):
        rows=[prow(i,ROW_Y[i]) for i in range(3)]
        self.add(*rows)
        self.at('three puzzles')
        self.play(*[Indicate(r[0],color=TEAL,scale_factor=1.015) for r in rows],run_time=0.5)
        self.at('what holds an intact')
        self.play(rows[0][0].animate.set_stroke(opacity=1).set_fill(opacity=0.06),rows[0][1].animate.set_opacity(1),
                  rows[0][2].animate.set_opacity(1),run_time=0.5)
        self.finish()

class S21(SpokenScene):
    def construct(self):
        rows=[prow(i,ROW_Y[i],on=(i==0)) for i in range(3)]
        self.add(*rows)
        self.at('what does the organizer')
        self.play(rows[1][0].animate.set_stroke(opacity=1).set_fill(opacity=0.06),rows[1][1].animate.set_opacity(1),
                  rows[1][2].animate.set_opacity(1),run_time=0.5)
        self.finish()

class S22(SpokenScene):
    def construct(self):
        rows=[prow(i,ROW_Y[i],on=(i<2)) for i in range(3)]
        self.add(*rows)
        self.at('does the answer hold')
        self.play(rows[2][0].animate.set_stroke(opacity=1).set_fill(opacity=0.06),rows[2][1].animate.set_opacity(1),
                  rows[2][2].animate.set_opacity(1),run_time=0.4)
        self.at('In the whole embryo',lead=0.6)
        big=RoundedRectangle(width=11.8,height=3.7,corner_radius=0.2,color=GREY,fill_opacity=0.06).move_to([0,-1.55,0])
        self.play(rows[0].animate.scale(0.8).move_to([0,2.8,0]),rows[1].animate.scale(0.8).move_to([0,1.3,0]),
                  Transform(rows[2][0],big),rows[2][1].animate.move_to([-5.2,-0.15,0]),
                  rows[2][2].animate.move_to([0.4,-0.15,0]),run_time=0.5)
        embryo=blastula(scale=0.23).move_to([-3.8,-1.55,0])
        fly=fly_icon().move_to([0,-1.55,0]); chick=chick_icon().move_to([3.8,-1.55,0])
        self.play(FadeIn(embryo),FadeIn(label('frog embryo',-3.8,-2.85,30)),run_time=0.3)
        self.at('in a fly')
        self.play(FadeIn(fly),FadeIn(label('fly',0,-2.85,30)),run_time=0.3)
        self.at('in a chick')
        self.play(FadeIn(chick),FadeIn(label('chick',3.8,-2.85,30)),run_time=0.3)
        self.finish()
        if self.elapsed()<7.5: self.wait(7.5-self.elapsed())

RX=3.5   # right-hand column of the dial scenes

class S23(SpokenScene):
    def construct(self):
        d=dial(True); outcome=decision(ORANGE); sc=scope(RX)
        self.add(d,sc,outcome)
        self.at('idea to carry')
        self.play(Indicate(d[2],color=YELLOW,scale_factor=1.03),run_time=0.35)
        self.at('BMP says skin')
        self.play(FadeIn(label('BMP says skin;',RX,2.5,36,ORANGE)),run_time=0.35)
        self.at('In early frog animal caps')
        self.play(Indicate(sc,scale_factor=1.03),run_time=0.35)
        self.at('turn its signal down')
        self.play(Rotate(d[2],angle=PI/2,about_point=DC),
                  FadeIn(label('turn its signal down\nfar enough and',RX,1.45,34)),run_time=0.85)
        self.at('cells become neural')
        self.play(Transform(outcome,decision(BLUE)),FadeIn(label('competent cells\nbecome neural',RX,0.35,34,BLUE)),run_time=0.5)
        self.at('they can still respond')
        self.play(FadeIn(label('competent = can still respond',RX,-0.75,30)),run_time=0.35)
        self.at('other needed inputs')
        self.play(FadeIn(label('other inputs intact',RX,-3.45,30)),run_time=0.35)
        self.at('such as FGF')
        self.play(FadeIn(fgf()),run_time=0.35)
        self.finish()

class S24(SpokenScene):
    def construct(self):
        d=dial(); dec=decision()
        self.add(d,scope(RX),dec,fgf(True))
        self.at('effect comes down')
        self.play(FadeIn(label('the BMP side of the decision',RX,-0.85,28)),run_time=0.3)
        self.at('activity in the nucleus')
        self.play(Indicate(d[7],color=YELLOW,scale_factor=1.04),run_time=0.4)
        self.at('next chapters')
        self.play(FadeIn(label('Three ways to turn it down',RX,2.55,32)),run_time=0.3)
        self.at('three hands')
        R=2.85*DS
        levers=VGroup()
        for text,y,color in [('outside the cell',1.6,PURPLE),
                             ('at the membrane',0.8,PINK),
                             ('inside the cell',0.0,GREEN)]:
            rim=DC[0]+np.sqrt(R**2-y**2)
            lab=label(text,1.9,y,32,color); lab.align_to([1.9,0,0],LEFT)
            levers.add(VGroup(Arrow([1.7,y,0],[rim+0.04,y,0],color=color,stroke_width=7,buff=0,
                                    max_tip_length_to_length_ratio=0.3),lab))
        self.play(LaggedStart(*[Create(l) for l in levers],lag_ratio=0.3),run_time=0.8)
        self.finish()
        if self.elapsed()<10.4: self.wait(10.4-self.elapsed())

class S25End(EndCard):
    LINE='BMP says skin. Turn its signal down in\ncompetent frog caps, and cells go neural.'
    def construct(self):
        self.add(scope(),T(self.LINE,size=38,font=TITLE_FONT,line_spacing=1.3).move_to([0,0.3,0]),
                 label('biochemistrypedia.com',0,-1.8,30,TEAL))
        self.finish()
