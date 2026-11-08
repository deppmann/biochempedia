"""Three Families, One Gene — chapter 1.

COLOR MAP shared with scenes.old.py (CHAPTERS.md is outside the edit scope):
YELLOW=SCN9A; ORANGE (#F29E4C)=Nav1.7; TEAL (#3FB8C0)=Nav1.8;
PURPLE (#B58CD9)=Nav1.9; RED=loss/broken copies/blockers;
GREEN=measured remaining current; TEXT=control; GREY=structure/axes.
Pedigrees, geography, cells and sensory icons are labelled schematics.
The recording plot is computed from Cox et al. 2006 Fig.4's fitted I–V
relation (Vhalf=-28, k=4.9, Erev=64); scaled to the reported -373 pA/pF
at -15 mV. Mutant/background values are the reported -5/-3 pA/pF.
https://pmc.ncbi.nlm.nih.gov/articles/PMC7212082/ (Fig.4 and text).
A peak-current/voltage plot avoids inventing a time course or noise trace.
The background band is qualitative, NOT a published detection threshold.
"""
from bp_style import *
import numpy as np

ORANGE = '#F29E4C'
TEAL_C = '#3FB8C0'
PURPLE = '#B58CD9'

# Plotting/cartoon helpers adapted from scenes.old.py.
def arr(a,b,color=GREY):
    return Arrow(a,b,buff=.15,color=color,stroke_width=5,tip_length=.22)

def heading(s,color=TEXT):
    return T(s,32,color,font=TITLE_FONT).move_to([0,3.05,0])

def lines(*ss,color=TEXT,size=28):
    return VGroup(*[T(s,size,color) for s in ss]).arrange(DOWN,buff=.18)

def mem_bar(cx,cy,w,h=.3):
    return RoundedRectangle(width=w,height=h,corner_radius=.1,color=GREY,fill_opacity=.35).move_to([cx,cy,0])

def chan(s='Nav1.7',color=ORANGE,cx=0,cy=0,size=32):
    c=chip(s,color,size=size)
    back=RoundedRectangle(width=c.width,height=c.height,corner_radius=.14,stroke_width=0,fill_color=BG,fill_opacity=1)
    return VGroup(back,c).move_to([cx,cy,0])

def cross(m):
    return VGroup(Line(m.get_corner(UL),m.get_corner(DR),color=RED,stroke_width=6),
                  Line(m.get_corner(DL),m.get_corner(UR),color=RED,stroke_width=6))

def gate(cx=0,cy=0,color=ORANGE):
    return VGroup(mem_bar(cx-1.6,cy,2),mem_bar(cx+1.6,cy,2),
                  Line([cx-.55,cy-.8,0],[cx-.55,cy+.8,0],color=color,stroke_width=10),
                  Line([cx+.55,cy-.8,0],[cx+.55,cy+.8,0],color=color,stroke_width=10),
                  T('Nav1.7' if color==ORANGE else 'Nav1.8',38,color).move_to([cx,cy-1.4,0]))

def pedigree(n=1,affected=True):
    # Minimal inheritance diagram, not a transcription of an actual family.
    p1=Square(.5,color=GREY).move_to([-.8,.65,0])
    p2=Circle(.25,color=GREY).move_to([.8,.65,0])
    kids=VGroup(Square(.5,color=RED if affected else GREY,fill_opacity=.8 if affected else 0).move_to([-.6,-.85,0]),
                Circle(.25,color=RED if affected else GREY,fill_opacity=.8 if affected else 0).move_to([.6,-.85,0]))
    links=VGroup(Line([-.55,.7,0],[.55,.7,0],color=GREY),Line([-.55,.6,0],[.55,.6,0],color=GREY),
                 Line([0,.6,0],[0,-.25,0],color=GREY),Line([-.6,-.25,0],[.6,-.25,0],color=GREY),
                 Line([-.6,-.25,0],[-.6,-.6,0],color=GREY),Line([.6,-.25,0],[.6,-.6,0],color=GREY))
    return VGroup(p1,p2,kids,links,T(f'Family {n}',30,GREY).move_to([0,1.5,0]))

def families(y=.35,affected=True):
    return VGroup(*[pedigree(n,affected) for n in (1,2,3)]).arrange(RIGHT,buff=1.6).move_to([0,y,0])

def dish():
    return VGroup(Ellipse(width=3.5,height=1.1,color=GREY),
        ArcBetweenPoints([-1.75,0,0],[1.75,0,0],angle=PI/2,color=GREY).shift(DOWN*.25),
        *[Circle(.16,color=GREY,fill_opacity=.3).move_to(p) for p in [[-.8,0,0],[0,.15,0],[.7,-.1,0]]])

def rig():
    cell=Circle(.95,color=GREY,fill_color=GREY,fill_opacity=.12).move_to([-1,-.1,0])
    pip=Polygon([-.3,.55,0],[1.4,2,0],[1.7,1.65,0],[-.15,.4,0],color=TEXT,fill_color=BG,fill_opacity=1)
    wire=VGroup(Line([1.55,1.85,0],[2.7,1.85,0],color=GREY),Line([2.7,1.85,0],[2.7,.5,0],color=GREY))
    screen=RoundedRectangle(width=2.2,height=1.6,corner_radius=.1,color=GREY).move_to([3,.0,0])
    return VGroup(cell,pip,wire,screen)

def question_frame():
    fam=families(y=.5).scale(.62).move_to([-3.2,.4,0])
    rr=rig().scale(.7).move_to([3,.2,0])
    q=lines('What would you measure?',size=38).move_to([0,-2.3,0])
    return VGroup(heading('From gene to function'),fam,rr,q)

def allele_pair(broken=1):
    a=VGroup(*[RoundedRectangle(width=.4,height=.8,corner_radius=.1,color=RED if i<broken else YELLOW,
        fill_opacity=.6).shift(RIGHT*(i-.5)*.65) for i in range(2)])
    return a

def gene():
    return VGroup(RoundedRectangle(width=9.5,height=.6,corner_radius=.12,color=YELLOW,fill_opacity=.15),
                  *[Line([x,-.3,0],[x,.3,0],color=YELLOW,stroke_width=3) for x in [-4,-3,-2,-1,0,1,2,3,4]])

def stop_flags():
    # Relative positions only; no base-pair scale is implied.
    return VGroup(*[VGroup(Line([x,.3,0],[x,1.1,0],color=RED),chip('STOP',RED,22).move_to([x,1.3,0])) for x in [-2.7,0,2.7]])

def hand():
    # Labelled flat silhouette; no anatomy or molecular structure is implied.
    return Polygon([-1.5,-.5,0],[-.6,-.5,0],[-.6,.8,0],[-.35,1,0],[-.1,.8,0],[-.1,.15,0],
                   [.8,.15,0],[1.1,-.1,0],[1.1,-.8,0],[.6,-1.1,0],[-1.5,-1.1,0],color=TEXT,fill_opacity=.12)

def sensory_panels():
    h1=hand().move_to([-3.2,.4,0]); h2=hand().move_to([3.2,.4,0])
    hot=RoundedRectangle(width=3.4,height=.35,corner_radius=.1,color=RED,fill_opacity=.45).move_to([-3.2,-.85,0])
    brush=VGroup(Line([2.3,1.6,0],[4.4,1.6,0],color=GREY,stroke_width=12),
                 *[Line([x,1.6,0],[x,.8,0],color=GREY,stroke_width=3) for x in np.linspace(2.4,4.3,9)])
    return h1,h2,hot,brush

def label(s,x,y,size=30,color=TEXT):
    return T(s,size,color).move_to([x,y,0])

def family_stack(x=-3.4):
    return VGroup(*[pedigree(n).scale(.68).move_to([x,2.35-(n-1)*2.35,0]) for n in (1,2,3)])

def big_families():
    return families().scale(1.22).move_to([0,.35,0])

def recording_panel(cx,mutant=False):
    # Cox Fig.4 fitted relation, normalized: amplitude is deliberately schematic.
    ax=Axes(x_range=[-70,40,50],y_range=[-1.1,.15,.5],x_length=4.45,y_length=5.0,
        tips=False,axis_config={'color':GREY,'include_ticks':False}).move_to([cx,.35,0])
    ax.x_axis.set_opacity(0); ax.y_axis.set_opacity(0)
    ax.add(Line(ax.c2p(-70,-1.1),ax.c2p(40,-1.1),color=GREY),
        Line(ax.c2p(-70,-1.1),ax.c2p(-70,.15),color=GREY),
        Line(ax.c2p(-70,0),ax.c2p(40,0),color=GREY,stroke_width=1))
    def wt(v):
        raw=(v-64)/(1+np.exp((-28-v)/4.9))
        norm=(-15-64)/(1+np.exp((-28+15)/4.9))
        return raw/abs(norm)
    curve=ax.plot((lambda v:-5/373) if mutant else wt,x_range=[-70,40,1],
        color=RED if mutant else ORANGE,stroke_width=5,use_smoothing=False)
    band=Polygon(ax.c2p(-70,-.055),ax.c2p(40,-.055),ax.c2p(40,.025),ax.c2p(-70,.025),
        stroke_width=0,fill_color=GREY,fill_opacity=.35)
    band.add(DashedLine(ax.c2p(-70,-.055),ax.c2p(40,-.055),color=GREY),
        DashedLine(ax.c2p(-70,.025),ax.c2p(40,.025),color=GREY))
    labs=VGroup(label('Mutant' if mutant else 'Wild type',cx,3.25,34,RED if mutant else ORANGE),
        label('Voltage (mV)',cx,-2.85,26,GREY),
        T('−70',26,GREY).next_to(ax.c2p(-70,-1.1),DOWN,buff=.12),
        T('+40',26,GREY).next_to(ax.c2p(40,-1.1),DOWN,buff=.12),
        T('0 mV',26,GREY).next_to(ax.c2p(0,-1.1),DOWN,buff=.12),
        Line(ax.c2p(0,-1.1),ax.c2p(0,-1.04),color=GREY))
    return ax,curve,band,labs

def rig_labelled(x=0,y=0,small=False):
    rr=rig().move_to([x,y,0])
    # Labels are placed outside the silhouettes, with explicit leaders.
    labs=VGroup(T('cell',28).next_to(rr[0],DOWN,buff=.18),
        T('pipette',28).next_to(rr[1],UP,buff=.15),
        T('amplifier',28).next_to(rr[3],DOWN,buff=.18))
    return VGroup(rr,labs)

def question_frame():
    fam=family_stack(-4.7).move_to([-4.7,.25,0])
    rr=rig_labelled(2.1,.35).scale(1.13).move_to([2.1,.35,0])
    q=label('What would you measure?',1,-3.15,38)
    return VGroup(fam,rr,q)

def finger(x):
    # Open hand: four separate fingers, thumb, palm and wrist.
    pts=[[-.65,-1.4],[-.65,-.8],[-1.25,-.1],[-1.48,.35],[-1.35,.6],
         [-1.1,.55],[-.65,.05],[-.65,1.35],[-.5,1.55],[-.32,1.35],
         [-.32,.5],[-.2,.5],[-.2,1.95],[-.02,2.15],[.17,1.95],
         [.17,.55],[.3,.55],[.3,1.7],[.48,1.9],[.66,1.7],[.66,.4],
         [.78,.4],[.78,1.15],[.95,1.3],[1.12,1.15],[1.12,-.3],
         [.85,-.85],[.65,-1.05],[.65,-1.4]]
    return Polygon(*[[x+px,py-.2,0] for px,py in pts],color=TEXT,
                   fill_color=TEXT,fill_opacity=.24,stroke_width=4)


def tick(x,y):
    return VGroup(Line([x-.25,y,0],[x,y-.25,0],color=GREEN,stroke_width=7),
        Line([x,y-.25,0],[x+.5,y+.4,0],color=GREEN,stroke_width=7))

def puzzle():
    left=gate().scale(1.23).move_to([-3.1,.25,0])
    right=gate(color=TEAL_C).scale(1.23).move_to([3.1,.25,0])
    # Leave a visible central gap even before the channels drift apart.
    left[1].stretch_to_fit_width(1.7,about_edge=LEFT)
    right[0].stretch_to_fit_width(1.7,about_edge=RIGHT)
    gl=lines('Genetics nominated:','Nav1.7',size=30,color=YELLOW).move_to([-3.1,2.85,0])
    dl=lines('Drug that worked:','Nav1.8 blocker (2025)',size=30,color=TEAL_C).move_to([3.1,2.85,0])
    # Leader ends outside the protein and membrane; no pore-block claim.
    blocker=chip('blocker',RED,28).move_to([5.05,-1.65,0])
    leader=Line(blocker.get_top(),[5.55,.8,0],color=RED)
    return VGroup(left,right,gl,dl,blocker,leader,label('?',0,.4,64))

class S00Title(TitleCard):
    LESSON='Nociceptors and the Sodium Channels of Pain'
    TITLE='Three Families, One Gene'
    def construct(self):
        g=VGroup(T('BIOCHEMISTRYPEDIA',26,TEAL),T(self.LESSON,28,GREY),
            T(self.TITLE,52,font=TITLE_FONT),Line(LEFT*1.3,RIGHT*1.3,color=GOLD)).arrange(DOWN,buff=.4)
        self.add(g); self.finish()

class S01Question(SpokenScene):
    def construct(self):
        f=family_stack(-4.5); d=dish().scale(1.75).move_to([2.7,-.1,0])
        self.add(f,d,label('?',2.7,2.1,110,YELLOW))
        self.at('no screen')
        self.play(Indicate(d,scale_factor=1.03),run_time=.35)
        self.finish()

class S02Nociceptors(SpokenScene):
    def construct(self):
        skin=RoundedRectangle(width=1.45,height=5.3,corner_radius=.2,color=GREY,fill_opacity=.15).move_to([-5.35,0,0])
        cord=RoundedRectangle(width=1.5,height=5.3,corner_radius=.2,color=GREY,fill_opacity=.15).move_to([5.35,0,0])
        nerve=VGroup(Line([-4.85,-.3,0],[4.6,-.3,0],color=TEXT,stroke_width=14),
            *[Line([-4.85,-.3,0],[-5.8,y,0],color=TEXT,stroke_width=9) for y in [-1.8,.9,1.8]],
            Circle(.65,color=TEXT).move_to([1.4,1.4,0]),Line([1.4,-.3,0],[1.4,.75,0],color=TEXT,stroke_width=6))
        self.add(skin,cord,nerve,label('skin',-5.35,-3.05,28),label('spinal cord',5.25,-3.05,28))
        self.at('called nociceptors')
        self.play(FadeIn(heading('Nociceptor')),run_time=.3)
        self.at('Their spikes need')
        pulse=Dot([-4.65,-.3,0],radius=.18,color=YELLOW)
        self.play(FadeIn(pulse),FadeIn(label('spike',-4.0,.65,30,YELLOW)),run_time=.2)
        channels=VGroup(*[VGroup(Line([x,-.7,0],[x,.1,0],color=ORANGE if x==-4 else TEAL_C,stroke_width=10),
            Line([x+.25,-.7,0],[x+.25,.1,0],color=ORANGE if x==-4 else TEAL_C,stroke_width=10)) for x in [-4,-2,0,3]])
        self.at('sodium channels')
        self.play(FadeIn(channels),FadeIn(label('Sodium channels',-2.1,1.35,32,ORANGE)),
            FadeIn(label('Nav1.7',-3.4,-2.0,32,ORANGE)),FadeIn(label('Nav1.8',1.5,-2.0,32,TEAL_C)),
            Create(Line([-3.4,-1.65,0],[-3.9,-.8,0],color=ORANGE)),
            Create(Line([1.5,-1.65,0],[3.1,-.8,0],color=TEAL_C)),run_time=.25)
        self.play(pulse.animate.move_to([4.65,-.3,0]),run_time=.65)
        self.finish()

class S03Noscreen(SpokenScene):
    def construct(self):
        d=dish().scale(1.3).move_to([-3.3,0,0]); f=family_stack(3.3).scale(.9).move_to([3.3,-.25,0])
        self.add(d)
        self.at('not nominated')
        self.play(FadeIn(heading('Not found by a screen in a dish')),Create(cross(d)),run_time=.35)
        self.at('found in families')
        self.play(FadeIn(f),d.animate.set_opacity(.45),run_time=.35)
        self.finish()

class S04Families(SpokenScene):
    def construct(self):
        # Country outline from world.geo.json PAK (Natural Earth geometry).
        # https://raw.githubusercontent.com/johan/world.geo.json/master/countries/PAK.geo.json
        lonlat=[(75.158,37.133),(75.897,36.667),(76.193,35.898),(77.837,35.494),
            (76.872,34.654),(75.757,34.505),(74.240,34.749),(73.750,34.318),
            (74.104,33.441),(74.452,32.765),(75.259,32.271),(74.406,31.693),
            (74.421,30.980),(73.451,29.976),(72.824,28.962),(71.778,27.913),
            (70.616,27.989),(69.514,26.941),(70.169,26.492),(70.283,25.722),
            (70.845,25.215),(71.043,24.357),(68.843,24.359),(68.177,23.692),
            (67.444,23.945),(67.145,24.664),(66.373,25.425),(64.530,25.237),
            (62.906,25.218),(61.497,25.078),(61.874,26.240),(63.317,26.757),
            (63.234,27.217),(62.755,27.379),(62.728,28.260),(61.772,28.699),
            (61.369,29.303),(60.874,29.829),(62.550,29.319),(63.550,29.468),
            (64.148,29.341),(64.350,29.560),(65.047,29.472),(66.346,29.888),
            (66.381,30.739),(66.939,31.305),(67.683,31.303),(67.793,31.583),
            (68.557,31.713),(68.927,31.620),(69.318,31.901),(69.263,32.502),
            (69.687,33.105),(70.324,33.359),(69.931,34.020),(70.882,33.989),
            (71.157,34.349),(71.115,34.733),(71.613,35.153),(71.499,35.651),
            (71.262,36.074),(71.846,36.510),(72.920,36.720),(74.068,36.836),
            (74.576,37.021)]
        def map_point(lon,lat):
            return [(lon-69.35)*.85*.44-1.2,(lat-30.41)*.44,0]
        outline=Polygon(*[map_point(lon,lat) for lon,lat in lonlat],
            color=TEXT,fill_color=GREY,fill_opacity=.2)
        marker=Dot(map_point(73,35),radius=.17,color=YELLOW)
        name=lines('Northern','Pakistan',size=36,color=YELLOW).move_to([3.4,1.9,0])
        leader=Line(marker.get_right(),name.get_left(),color=YELLOW)
        self.add(outline,marker,name,leader)
        self.at('had members')
        f=big_families()
        self.play(FadeOut(outline),FadeOut(marker),FadeOut(name),FadeOut(leader),FadeIn(f,scale=.25),run_time=.3)
        self.add(label('Related parents (consanguineous families)',0,-2.65,30,GREY))
        self.at('never experienced pain')
        self.play(FadeIn(heading('Never experienced pain',RED)),run_time=.3)
        self.finish()

class S05Children(SpokenScene):
    def construct(self):
        f=big_families(); self.add(f)
        self.at('Six affected children')
        numbers=VGroup(*[T(str(2*i+j+1),30,RED).next_to(f[i][2][j],DOWN,buff=.25) for i in range(3) for j in range(2)])
        self.play(FadeIn(numbers),FadeIn(heading('6 affected children',RED)),run_time=.35)
        self.at('They were aged')
        self.play(FadeIn(label('Aged 4 to 14',0,-2.8,38)),run_time=.3)
        self.finish()

class S06Recessive(SpokenScene):
    def construct(self):
        p=Square(.8,color=TEXT).move_to([-3.2,1.6,0]); m=Circle(.4,color=TEXT).move_to([3.2,1.6,0])
        c=Square(.85,color=RED,fill_opacity=.7).move_to([0,-.55,0])
        links=VGroup(Line([-2.8,1.65,0],[2.8,1.65,0],color=GREY),Line([-2.8,1.55,0],[2.8,1.55,0],color=GREY),Line([0,1.55,0],[0,-.12,0],color=GREY))
        a=allele_pair().move_to([-3.2,.45,0]); b=allele_pair().move_to([3.2,.45,0]); cc=allele_pair(2).move_to([0,-1.6,0])
        self.add(p,m,links,c,heading('Recessive'))
        self.at('recessive')
        self.play(FadeIn(a),FadeIn(b),run_time=.25)
        for x in [-3.2,3.2]:
            self.add(lines('Carrier','one working copy','one broken copy',size=26).move_to([x,-1.1,0]))
        self.add(label('Yellow = working',-3.5,-2.05,28,YELLOW),label('Red = broken',3.5,-2.05,28,RED))
        self.at('Affected children carried')
        self.play(TransformFromCopy(a[0],cc[0]),TransformFromCopy(b[0],cc[1]),run_time=.4)
        self.at('two broken copies')
        self.play(FadeIn(label('Affected: two broken copies',0,-3.0,32,RED)),run_time=.25)
        self.finish()

class S07Gene(SpokenScene):
    def construct(self):
        chrom=VGroup(*[RoundedRectangle(width=.6,height=4.7,corner_radius=.25,color=YELLOW).shift(RIGHT*x) for x in [-.4,.4]])
        self.add(chrom,heading('Chromosome → gene',YELLOW))
        self.at('found three different')
        g=gene().move_to([0,-.8,0]); name=label('SCN9A gene',0,-1.75,36,YELLOW)
        self.play(ReplacementTransform(chrom,g),FadeIn(name),run_time=.45)
        self.at('homozygous nonsense mutations')
        flags=VGroup()
        for i,x in enumerate([-3.5,0,3.5]):
            flags.add(VGroup(Line([x,-.5,0],[x,.6,0],color=RED),chip('STOP',RED,28).move_to([x,.8,0]),
                lines(f'Family {i+1}','nonsense variant',size=26,color=RED).move_to([x,1.9,0])))
        self.play(FadeIn(flags),run_time=.35)
        self.add(label('Positions schematic; three different variants',0,-2.8,28,GREY))
        self.finish()

class S08Protein(SpokenScene):
    def construct(self):
        g=gene(); title=heading('SCN9A gene',YELLOW); self.add(g,title)
        self.at('That gene encodes')
        ch=gate(0,.1); ch[0].set_opacity(0); ch[1].set_opacity(0)
        # Two membrane layers with a gap occupied by the channel.
        membrane=VGroup(*[mem_bar(x,y,5.5,.18) for x in [-3.4,3.4] for y in [-.22,.42]])
        self.play(FadeOut(g),FadeIn(ch,scale=.5),FadeIn(membrane),FadeOut(title),FadeIn(heading('Sodium channel',ORANGE)),run_time=.35)
        self.at('a sodium channel')
        self.add(label('Terminal membrane in skin',0,2.0,30,GREY))
        self.at('concentrated in pain')
        self.play(FadeIn(lines('Concentrated in','pain-sensing neurons',size=34).move_to([0,-2.6,0])),run_time=.3)
        self.finish()

class S09Predict(SpokenScene):
    def construct(self):
        frame=question_frame(); self.add(frame[0])
        self.at('What measurement would')
        self.play(FadeIn(frame[1]),FadeIn(frame[2]),run_time=.35)
        self.finish()

class S10Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(question_frame())
        cue=label('Pause and decide',0,3.15,28,GREY); self.add(cue)
        self.wait(5)

class S11Linkage(SpokenScene):
    def construct(self):
        p=pedigree().scale(1.65).move_to([0,.1,0]); self.add(p)
        self.add(lines('Linkage: variant travels','with phenotype',size=32,color=YELLOW).move_to([0,3,0]))
        self.at('travels with the phenotype')
        check=tick(1.8,1.3); self.play(Create(check),run_time=.3)
        self.at('It cannot say')
        self.play(p.animate.shift(LEFT*3.3),check.animate.shift(LEFT*3.3),FadeIn(gate(3,.2)),FadeIn(label('?',3,2.1,64,ORANGE)),run_time=.4)
        self.finish()

class S12Nonsense(SpokenScene):
    def construct(self):
        g=gene().scale(.42).move_to([-3.8,1.0,0]); stop=chip('STOP',RED,28).move_to([-3.8,2.25,0])
        self.add(g,stop,label('Nonsense allele',-3.8,-.05,30,YELLOW))
        ch=gate(0,1).scale(.56); ch[-1].scale(1.4); q=label('?',0,2.65,60,ORANGE)
        self.at('not by itself proof')
        self.play(FadeIn(ch),FadeIn(q),run_time=.35)
        cell=Circle(1.25,color=TEXT,fill_color=GREY,fill_opacity=.12).move_to([4,1,0])
        self.at('Expressing mutant')
        self.play(FadeIn(cell),GrowArrow(arr([1.5,1,0],[2.7,1,0],YELLOW)),run_time=.35)
        self.add(label('Cell line',4,-.6,28),label('Nav1.7 ?',4,1,30,ORANGE),
            label('Heterologous cDNA assay',0,3.45,32))
        self.at("the construct's functional output")
        self.play(FadeIn(label('1  Functional current tested',0,-1.45,32,ORANGE)),run_time=.3)
        self.at('without reproducing native')
        self.play(FadeIn(label('2  Native transcript processing not reproduced',0,-2.3,30)),run_time=.3)
        self.at('or measuring protein abundance')
        self.play(FadeIn(label('3  Patient-neuron protein abundance not measured',0,-3.15,30)),run_time=.3)
        self.finish()

class S13Reveal(SpokenScene):
    def construct(self):
        self.add(heading('HEK293 cells: wild type and mutant'))
        cells=VGroup()
        for x,name,col in [(-3.2,'Wild type',ORANGE),(3.2,'Mutant',RED)]:
            cell=Circle(1.55,color=TEXT,fill_color=GREY,fill_opacity=.12).move_to([x,-.15,0])
            pip=Polygon([x+.95,1.05,0],[x+2.15,2.1,0],[x+2.4,1.85,0],[x+1.1,.9,0],color=TEXT)
            amp=Rectangle(width=1.25,height=.65,color=GREY).move_to([x+1.8,-1.9,0])
            wire=VGroup(Line([x+2.3,1.95,0],[x+2.6,1.95,0],color=GREY),Line([x+2.6,1.95,0],[x+2.6,-1.9,0],color=GREY),Line([x+2.6,-1.9,0],amp.get_right(),color=GREY))
            sub=VGroup(*[Square(.28,color=GREY,fill_opacity=.4).move_to([x+dx,1.32,0]) for dx in [-.6,-.15]])
            pore=VGroup(*[Line([x+dx,.9,0],[x+dx,1.7,0],color=col,stroke_width=8) for dx in [-.9,-.7]])
            cells.add(VGroup(cell,pip,amp,wire,sub,pore,label(name,x,-.2,34,col),label('amplifier',x+1.8,-2.65,26),label('patch pipette',x+1.2,2.55,26)))
        self.add(cells)
        self.at('in cultured cells')
        self.play(Indicate(cells[0][0],scale_factor=1.02),Indicate(cells[1][0],scale_factor=1.02),run_time=.3)
        self.at('look for current')
        for x in [-3.2,3.2]:
            text=lines('Accessory','subunits',size=26,color=GREY).move_to([x-1.65,1.95,0])
            self.add(text,Line(text.get_bottom(),[x-.6,1.48,0],color=GREY))
        self.finish()

class S14Flat(SpokenScene):
    def construct(self):
        a,c,b,l=recording_panel(-3); aa,cc,bb,ll=recording_panel(3,True)
        yl=T('Peak current (pA/pF)',26,GREY).rotate(PI/2).move_to([-6.15,.4,0])
        self.add(a,aa,l,ll,yl,label('Amplitude + background band schematic',0,-3.55,26,GREY))
        self.at('The mutant constructs')
        self.play(Create(c),run_time=.4)
        self.at('no current above')
        self.play(FadeIn(bb),Create(cc),run_time=.4)
        self.at('the recording background')
        bg=lines('Recording background','(detection limit)',size=26,color=GREY).move_to([3,.75,0])
        self.play(FadeIn(bg),Create(Line(bg.get_top(),aa.c2p(15,-.015),color=GREY)),run_time=.25)
        self.at('That is no measurable')
        result=lines('No measurable','conduction',size=32,color=RED)
        # Place interpretation in the open lower region, clear of both axis captions.
        result.move_to([3,-.45,0]); self.play(FadeIn(result),run_time=.25)
        self.at('not a proven absence')
        self.play(FadeIn(lines('Not a proven','absence of protein',size=28).move_to([3,-1.5,0])),run_time=.25)
        self.finish()

class S15Agree(SpokenScene):
    def construct(self):
        p=pedigree().scale(1.55).move_to([-3.4,.2,0])
        a,c,b,l=recording_panel(3,True); plot=VGroup(a,b,c).scale(.7).move_to([3,.3,0])
        self.add(p,plot,heading('Genetics + recording agree'),label('=',0,.4,60),label('Loss of function',0,-2.7,40,RED))
        self.at('pointed the same way')
        self.play(Indicate(plot,scale_factor=1.025),run_time=.3)
        self.finish()

class S16Quiet(SpokenScene):
    def construct(self):
        f=finger(-3.2); self.add(heading('Loss of Nav1.7',ORANGE),f)
        # Large flame, separate from the hand, with a prominent red cross.
        flame=VMobject(color=RED,fill_color=RED,fill_opacity=.5,stroke_width=4)
        flame.set_points_smoothly([[-5.2,-.75,0],[-5.8,-.2,0],[-5.6,.55,0],
            [-5.25,1.3,0],[-5.1,.5,0],[-4.75,.85,0],[-4.6,-.1,0],[-5.2,-.75,0]])
        pin=VGroup(flame)
        self.add(pin)
        self.at('the painful world goes quiet')
        self.play(Create(cross(SurroundingRectangle(pin,buff=.14))),FadeIn(label('No pain',-3.2,-2.65,40,RED)),run_time=.3)
        self.at('while touch continues')
        pad=RoundedRectangle(width=2.5,height=.3,corner_radius=.12,color=TEXT,fill_opacity=.3).move_to([3.2,-1.8,0])
        self.play(FadeIn(finger(3.2)),FadeIn(pad),Create(tick(4.9,.2)),FadeIn(label('Touch continues',3.2,-2.65,40)),run_time=.4)
        self.finish()

class S17Hedge(SpokenScene):
    def construct(self):
        self.add(heading('Reported hot / cold discrimination',YELLOW))
        for x,name,col in [(-3,'Hot',RED),(3,'Cold',TEXT)]:
            cup=VGroup(Polygon([x-1.4,1.2,0],[x+1.4,1.2,0],[x+1,-1.5,0],[x-1,-1.5,0],color=col),
                Arc(radius=.7,start_angle=-PI/2,angle=PI,color=col).move_to([x+1.55,-.1,0]))
            self.add(VGroup(*[DashedVMobject(part,num_dashes=30) for part in cup]),label(name,x,-2.05,36,col))
        self.at('hot food from cold')
        steam=VGroup(*[Arrow([x,1.45,0],[x,2.4,0],color=RED,buff=.05) for x in [-3.6,-3,-2.4]])
        ice=VGroup(*[Square(.45,color=TEXT).rotate(.2).move_to([x,.3,0]) for x in [2.4,3,3.6]])
        self.play(FadeIn(steam),FadeIn(ice),run_time=.3)
        self.at('not rigorously assessed')
        self.play(FadeIn(lines('Could tell hot from cold;','not rigorously assessed',size=32,color=YELLOW).move_to([0,-3.05,0])),run_time=.25)
        self.finish()

class S18Smell(SpokenScene):
    def construct(self):
        self.add(heading('Later work',YELLOW))
        # Continuous profile with bulbous tip and a separate nostril.
        nose=VMobject(color=TEXT,stroke_width=9).set_points_smoothly([[.1,2.4,0],[-.1,1.3,0],[-.7,.1,0],[-1.2,-.8,0],[-.9,-1.15,0],[.2,-1.25,0],[.7,-.9,0],[1,-1.4,0]])
        nostril=Ellipse(width=.52,height=.3,color=TEXT,fill_color=TEXT,fill_opacity=.7).move_to([.25,-.95,0])
        VGroup(nose,nostril).scale(1.25).shift(RIGHT*1.1+UP*.1)
        waves=VGroup(*[Arc(radius=r,start_angle=-.85,angle=1.7,color=TEXT,stroke_width=7).move_to([-2.2-i*.65,0,0]) for i,r in enumerate([.85,1.25,1.65])])
        self.add(nose,nostril)
        self.at('People with the same')
        self.play(Create(waves),run_time=.35)
        self.at('also cannot smell')
        self.play(Create(cross(waves)),FadeIn(label('No smell (anosmia)',0,-2.75,42,RED)),run_time=.35)
        self.finish()

class S19Target(SpokenScene):
    def construct(self):
        ch=gate(-3.2,.25); self.add(ch)
        target=VGroup(*[Circle(r,color=ORANGE).move_to([3.1,.3,0]) for r in [1.7,1.1,.45]])
        self.at('a major target')
        self.play(FadeIn(target),GrowArrow(arr([-.4,.3,0],[3.1,.3,0],ORANGE)),run_time=.4)
        self.at('for analgesic drug development')
        self.play(FadeIn(lines('Analgesic drug','development',size=36).move_to([3.1,-2.5,0])),run_time=.3)
        self.finish()

class S20Standard(SpokenScene):
    def construct(self):
        self.add(heading('The standard set in 2006'))
        genechip=chip('Human pain gene',YELLOW,40).move_to([0,1.4,0])
        measure=chip('Channel measurement',ORANGE,40).move_to([0,-1.5,0])
        bracket=VGroup(Line(genechip.get_left(),[-5,1.4,0],color=TEXT),Line([-5,1.4,0],[-5,-1.5,0],color=TEXT),Line([-5,-1.5,0],measure.get_left(),color=TEXT))
        self.add(genechip,measure,bracket,label('attached',-3.7,-.15,30))
        self.at('with a channel measurement attached')
        self.play(Indicate(bracket,scale_factor=1.02),run_time=.35)
        self.finish()

class S21Direction(SpokenScene):
    def construct(self):
        p=pedigree().scale(1.6).move_to([0,0,0]); box=SurroundingRectangle(p,buff=.3,color=GREY)
        self.add(p,box)
        g=chip('SCN9A',YELLOW,40).move_to([2.8,1.5,0]); loss=lines('Direction:','loss of function',size=36,color=RED).move_to([2.8,-1.6,0])
        self.at('both the gene')
        self.play(p.animate.shift(LEFT*3.7),box.animate.shift(LEFT*3.7),FadeIn(g),run_time=.35)
        self.add(arr(box.get_right(),g.get_left(),YELLOW))
        self.at('and the direction')
        self.play(GrowArrow(arr(box.get_right(),loss.get_left(),RED)),FadeIn(loss),run_time=.35)
        self.finish()

class S22Puzzle(SpokenScene):
    def construct(self):
        g=puzzle(); self.add(g[0],g[2],g[6])
        self.at('The blocker that reached patients')
        self.play(FadeIn(g[1]),FadeIn(g[3]),run_time=.35)
        self.at('blocks a different channel')
        self.play(FadeIn(g[4]),Create(g[5]),run_time=.35)
        self.finish()

class S23Hold(SpokenScene):
    def construct(self):
        g=puzzle(); self.add(g)
        self.at('Hold that gap')
        gap=DoubleArrow([-1.1,-1.7,0],[1.1,-1.7,0],buff=0,color=YELLOW,stroke_width=5)
        self.add(gap)
        wider=DoubleArrow([-2.2,-1.7,0],[2.2,-1.7,0],buff=0,color=YELLOW,stroke_width=5)
        self.play(Transform(gap,wider),g[0].animate.shift(LEFT*.35),
            g[2].animate.shift(LEFT*.35),g[1].animate.shift(RIGHT*.35),
            g[3].animate.shift(RIGHT*.35),Indicate(g[6],scale_factor=1.15),run_time=.6)
        self.at('Genetics nominated')
        self.play(Indicate(g[0],scale_factor=1.02),run_time=.3)
        self.at('the drug that worked')
        self.play(Indicate(g[1],scale_factor=1.02),FadeIn(lines('Nociceptors and the','Sodium Channels of Pain',size=32).move_to([0,-2.85,0])),run_time=.35)
        self.finish()

class S24Takeaway(SpokenScene):
    def construct(self):
        p=pedigree().scale(1.45).move_to([-3.8,.25,0]); p[-1].scale(.65); self.add(p)
        self.add(label('Genetics nominates',0,3.05,40,YELLOW))
        self.at('Only a recording')
        self.play(FadeIn(rig_labelled(2.2,.2)),run_time=.35)
        self.add(lines('Only a recording shows','whether the channel conducts',size=38,color=ORANGE).move_to([0,-2.9,0]))
        self.finish()

class S25End(EndCard):
    LINE='Genetics nominates a channel; recording shows whether it conducts.'
    def construct(self):
        self.add(lines('Genetics nominates a channel;','recording shows whether it conducts.',size=40).move_to([0,.3,0]),
            label('biochemistrypedia.com',0,-1.5,28,TEAL))
        self.finish()
