"""A Fly Turned Over. All shapes are anatomical schematics, not signal plots.
COLOR MAP: GREY outlines; YELLOW BMP/Dpp; GREEN Sog/Chordin/catchers;
BLUE neural; PURPLE mesoderm; TEXT axis labels. No molecular structures.
"""
import numpy as np
from bp_style import *
PURPLE = '#B58CD9'
config.background_color = BG
R=3.25
PR=2.55
CY=0
CAP=-3.6

def label(s,x=0,y=3.55,color=TEXT,size=28):
    return T(s,size,color).move_to([x,y,0])

def band(r,start,sweep,color,width=.42):
    return AnnularSector(inner_radius=r-width,outer_radius=r,start_angle=start*DEGREES,
                         angle=sweep*DEGREES,fill_color=color,fill_opacity=.9,stroke_width=0)

def shell(r):
    return Circle(radius=r,color=GREY,stroke_width=3,fill_color=GREY,fill_opacity=.08)

def stripes(r,color=GREEN,inner=0):
    return VGroup(band(r-inner,190,64,color,.48 if not inner else .25),
                  band(r-inner,286,64,color,.48 if not inner else .25))

def map_body(kind='fly',r=PR,dpp=True,sog=True,neural=True,meso=False):
    g=VGroup(shell(r))
    if dpp:g.add(band(r,35 if kind=='fly' else 215,110,YELLOW))
    if sog:g.add(stripes(r) if kind=='fly' else band(r,10,160,GREEN,.48))
    if neural:g.add(stripes(r,BLUE,.62) if kind=='fly' else band(r-.62,10,160,BLUE,.25))
    if meso:g.add(band(r,258,24,PURPLE))
    return g

def map_labels(kind='fly',r=PR,dpp=True,sog=True):
    g=VGroup(label('dorsal',0,r+.28,size=26),label('ventral',0,-r-.28,size=26))
    if dpp:g.add(label('Dpp' if kind=='fly' else 'BMP4',0,1.1 if kind=='fly' else -1.1,YELLOW))
    if sog:g.add(label('Sog' if kind=='fly' else 'Chordin',0,-1.1 if kind=='fly' else 1.1,GREEN))
    return g

def rotated_map(g,angle=PI,c=None,r=PR):
    # Body turns about its centre. Labels stay upright; the dorsal/ventral labels ride just outside
    # the circle and fade while they pass the sides, where they would cross the outline or the frame.
    c=g[0].get_center() if c is None else c
    g.rotate(angle,about_point=c)
    for i,t in enumerate(g[1]):
        t.rotate(-angle)
        if i<2:
            sg=1 if i==0 else -1
            u=sg*np.array([-np.sin(angle),np.cos(angle),0])
            t.move_to(c+u*(r+.12+t.width/2*abs(u[0])+t.height/2*abs(u[1])))
            t.set_opacity(float(1-np.clip((abs(u[0])-.4)/.3,0,1)))
    return g

def turn(g,angle=PI):
    start=g.copy()
    def update(m,a):
        m.become(rotated_map(start.copy(),angle*a))
    return UpdateFromAlphaFunc(g,update)

def one_map(kind='fly',x=-3.35,dpp=True,sog=True,neural=True,meso=False,flipped=False):
    g=VGroup(map_body(kind,PR,dpp,sog,neural,meso),map_labels(kind,PR,dpp,sog)).shift([x,CY,0])
    if flipped:rotated_map(g)
    return g

def pair(full=True,flipped=False):
    return VGroup(one_map(meso=True,flipped=flipped),
                  one_map('frog',3.35,sog=full,neural=full),
                  label('Fly',-3.35),label('Frog',3.35))

def nerve_label():
    # Leader approaches from inside the embryo, never through the green ectoderm.
    return VGroup(label('ventral nerve cord',0,-.35,BLUE,26),
                  Line([-.9,-.65,0],[-1.35,-1.98,0],color=BLUE))

def fly_stage(sog=True,neural=False,meso=False,question=False):
    g=VGroup(map_body('fly',R,True,sog,neural,meso),
             label('Fly · cross-section',0,3.7),
             label('dorsal',4.8,2.7,size=26),label('ventral',4.8,-2.7,size=26),
             label('Dpp',0,2.35,YELLOW))
    if sog:g.add(label('Sog',-4.6,-1.2,GREEN),Line([-4,-1.2,0],[-2.8,-1.2,0],color=GREEN))
    if neural:g.add(nerve_label())
    if meso:g.add(label('mesoderm',0,-3.65,PURPLE,26))
    if question:g.add(label('Where does the nerve cord form?',0,-3.65,size=28))
    return g

def turn_question():
    return VGroup(pair(),label('What happens if you turn the fly over?',0,CAP))

def chips_pair():
    # Early comparisons are cards, with no anatomical position implied.
    return VGroup(RoundedRectangle(width=5.6,height=5.8,color=GREY).shift(LEFT*3.35),
                  RoundedRectangle(width=5.6,height=5.8,color=GREY).shift(RIGHT*3.35),
                  label('Fly',-3.35),label('Frog',3.35))

def home_chips():
    return VGroup(chip('Sog',GREEN).move_to([-3.35,1.45,0]),
                  chip('Chordin',GREEN).move_to([3.35,1.45,0]))

class S00Title(TitleCard):
    LESSON='Neural Induction: The Default Model'
    TITLE='A Fly Turned Over'

class S01(SpokenScene):
    def construct(self):
        # Distinct outline silhouettes, explicitly schematic.
        fly=VGroup(Ellipse(width=1.35,height=3,color=TEXT),Circle(.5,color=TEXT).shift(UP*1.8))
        for s in [-1,1]:
            fly.add(Ellipse(width=1.5,height=2.5,color=TEXT).rotate(s*.45).shift([s*.95,.3,0]))
            for y in [-.8,0,.8]:fly.add(Line([s*.6,y,0],[s*1.7,y-.7,0],color=TEXT))
        fly.scale(1.25).shift(LEFT*3.35)
        frog=VGroup(Ellipse(width=2.3,height=2.7,color=TEXT),Ellipse(width=2.8,height=1.3,color=TEXT).shift(UP*1.3))
        for s in [-1,1]:
            frog.add(Circle(.25,color=TEXT).shift([s*.85,1.85,0]),
                     VMobject(color=TEXT).set_points_as_corners([[s*.8,-.6,0],[s*1.8,-1.3,0],[s*.9,-1.7,0],[s*2,-2,0]]))
        frog.scale(1.2).shift(RIGHT*3.35)
        self.at('a fruit fly');self.add(fly,label('fruit fly · schematic',-3.35,3.55))
        self.at('and a frog');self.play(FadeIn(frog),FadeIn(label('frog · schematic',3.35,3.55)),run_time=.5)
        self.at('do they build');self.play(FadeIn(label('Do they build a nervous system the same way?',0,-3.5)),run_time=.4)
        self.finish()

class S02(SpokenScene):
    def construct(self):
        self.add(shell(R).shift(LEFT*2.7),label('Fly · cross-section',-2.7,3.7))
        self.at('the fly has');self.add(label('The same pair',3.6,2.4))
        self.at('its gene');self.play(FadeIn(chip('dpp',YELLOW,32).move_to([3.6,1.2,0])),run_time=.4)
        self.play(FadeIn(label('decapentaplegic',3.6,.3,YELLOW,26)),run_time=.4)
        self.at('encodes a relative');self.play(FadeIn(label('BMP2/4 relative',3.6,-1,YELLOW)),run_time=.5)
        self.finish()

class S03(SpokenScene):
    def construct(self):
        self.add(shell(R).shift(LEFT*2.7),label('Fly · cross-section',-2.7,3.7),
                 chip('dpp',YELLOW).move_to([3.6,2.3,0]))
        self.at('and short gastrulation');self.play(FadeIn(chip('sog',GREEN,32).move_to([3.6,1,0])),run_time=.4)
        self.play(FadeIn(label('short gastrulation',3.6,.1,GREEN,26)),run_time=.4)
        self.at('encodes a relative');self.play(FadeIn(label('Chordin relative',3.6,-1.2,GREEN)),run_time=.4)
        self.finish()

class S04(SpokenScene):
    def construct(self):
        self.add(chips_pair())
        self.at('so dpp plays');self.play(FadeIn(chip('Dpp',YELLOW).move_to([-3.35,1,0])),FadeIn(chip('BMP4',YELLOW).move_to([3.35,1,0])),GrowArrow(DoubleArrow([-1.5,1,0],[1.5,1,0],color=YELLOW)),run_time=.5)
        self.at('sog plays');self.play(FadeIn(chip('Sog',GREEN).move_to([-3.35,-1,0])),FadeIn(chip('Chordin',GREEN).move_to([3.35,-1,0])),GrowArrow(DoubleArrow([-1.5,-1,0],[1.5,-1,0],color=GREEN)),run_time=.5)
        self.finish()

class S05(SpokenScene):
    def construct(self):
        self.add(chips_pair(),home_chips())
        self.at('in 1995');self.play(FadeIn(label('1995 · Holley and colleagues',0,-3.55)),run_time=.4)
        self.at('swapped the two');self.play(GrowArrow(Arrow([-2.3,1,0],[2.3,-1,0],color=GREEN)),GrowArrow(Arrow([2.3,1,0],[-2.3,-1,0],color=GREEN)),run_time=.7)
        self.finish()

class S06(SpokenScene):
    def construct(self):
        self.add(chips_pair(),home_chips())
        self.at('frog cordon');c=chip('Chordin',GREEN).move_to([3.35,1.45,0]);self.add(c)
        self.play(c.animate.move_to([-3.35,-1.15,0]),GrowArrow(Arrow([2.2,1,0],[-2.2,-.85,0],color=GREEN)),run_time=.7)
        self.at('works in the fly');self.play(FadeIn(label('✓ works',-3.35,-2.25,GREEN,30)),run_time=.25)
        self.at('and fly');s=chip('Sog',GREEN).move_to([-3.35,1.45,0]);self.add(s)
        self.play(s.animate.move_to([3.35,-1.15,0]),GrowArrow(Arrow([-2.2,1,0],[2.2,-.85,0],color=GREEN)),run_time=.65)
        self.at('works in the frog');self.play(FadeIn(label('✓ works',3.35,-2.25,GREEN,30)),run_time=.25)
        self.finish()

class S07(SpokenScene):
    def construct(self):
        self.add(fly_stage(sog=False));s=stripes(R);self.add(s,label('Sog',-4.6,-1.2,GREEN))
        t=chip('Tolloid',TEXT).move_to([-5.0,-3.0,0])
        self.at('was first named');self.play(FadeIn(t),run_time=.35)
        self.at('and it');self.play(t.animate.move_to([-3.95,-2.55,0]),run_time=.3)
        pieces=VGroup(band(R,190,27,GREEN,.48),band(R,227,27,GREEN,.48))
        cut=Line([-2.85,-1.85,0],[-2,-2.5,0],color=TEXT,stroke_width=5)
        self.play(ReplacementTransform(s[0],pieces),Create(cut),run_time=.3)
        self.play(pieces[0].animate.shift(LEFT*.15).set_opacity(.2),pieces[1].animate.shift(DOWN*.15).set_opacity(.2),FadeOut(cut),run_time=.35)
        self.finish()

class S08(SpokenScene):
    def construct(self):
        self.add(shell(R),label('Fly · cross-section',0,3.7),label('dorsal',4.8,2.7,size=26),label('ventral',4.8,-2.7,size=26))
        self.at('now the map');self.at('is made on');self.play(FadeIn(band(R,35,110,YELLOW)),run_time=.4)
        self.at('the dorsal side');self.play(FadeIn(label('Dpp',0,2.35,YELLOW)),run_time=.3);self.finish()

class S09(SpokenScene):
    def construct(self):
        self.add(fly_stage(sog=False));self.at('sog is made');self.play(FadeIn(stripes(R)),run_time=.6)
        self.at('broad lateral stripes');self.play(FadeIn(label('Sog',-4.6,-1.2,GREEN)),Create(Line([-4,-1.2,0],[-2.8,-1.2,0],color=GREEN)),run_time=.4);self.finish()

class S10(SpokenScene):
    def construct(self):
        self.add(fly_stage());self.at('where should');self.play(FadeIn(label('Where does the nerve cord form?',0,-3.65)),run_time=.4);self.finish()
class S11Pause(Scene):
    def construct(self):self.add(fly_stage(question=True));self.wait(5)
class S12(SpokenScene):
    def construct(self):
        self.add(fly_stage());self.at('ventrally');self.play(FadeIn(stripes(R,BLUE,.62)),run_time=.5)
        self.at('from that ectoderm');self.play(FadeIn(nerve_label()),run_time=.4)
        self.at('signaling low');self.play(FadeIn(label('Dpp signaling low',0,-3.65,GREEN)),run_time=.4);self.finish()
class S13Beat(Scene):
    def construct(self):self.add(fly_stage(neural=True),label('Dpp signaling low',0,-3.65,GREEN));self.wait(2.5)
class S14(SpokenScene):
    def construct(self):
        self.add(fly_stage(neural=True));self.at('the ventralmost fly');self.play(FadeIn(band(R,258,24,PURPLE)),run_time=.5)
        self.at('are mesoderm');self.play(FadeIn(label('mesoderm',0,-3.65,PURPLE,26)),run_time=.4);self.finish()
class S15(SpokenScene):
    def construct(self):
        old=fly_stage(neural=True,meso=True);self.add(old);self.at('in a vertebrate')
        p=pair(full=False);signal=p[1][0][1];word=p[1][1][-1];p[1][0].remove(signal);p[1][1].remove(word)
        self.play(ReplacementTransform(old,p),run_time=.7);self.at('signaling is high')
        self.play(FadeIn(signal),FadeIn(word),run_time=.4);self.finish()
class S16(SpokenScene):
    def construct(self):
        self.add(pair(full=False));self.at('comes from the')
        shield=band(PR,10,160,GREEN,.48).shift([3.35,CY,0]);self.play(FadeIn(shield),run_time=.35)
        self.at('dorsal organiser')
        # BMP rises from the ventral arc and is stopped by the Chordin bar.
        arrows=VGroup(*[Arrow([x,-1.7,0],[x,.45,0],color=YELLOW,buff=0,stroke_width=7) for x in [2.5,4.2]])
        stop=Line([1.95,.7,0],[4.75,.7,0],color=GREEN,stroke_width=12)
        self.play(FadeIn(label('Chordin',3.35,1.25,GREEN)),run_time=.3)
        self.play(*[GrowArrow(a) for a in arrows],run_time=.7);self.play(Create(stop),run_time=.3)
        self.at('the neural tube')
        self.play(FadeOut(arrows),FadeOut(stop),FadeIn(band(PR-.62,10,160,BLUE,.25).shift([3.35,CY,0])),FadeIn(label('neural tube',4.55,-.4,BLUE,26)),Create(Line([5.0,-.15,0],[5.1,.25,0],color=BLUE)),run_time=.6);self.finish()
class S17(SpokenScene):
    def construct(self):
        p=pair();self.add(p);self.at('in both animals')
        self.play(Indicate(p[0][0][3],color=BLUE,scale_factor=1.08),Indicate(p[1][0][3],color=BLUE,scale_factor=1.08),run_time=.8)
        self.at('nervous system forms');self.play(FadeIn(label('BMP low',-3.35,0,GREEN,26)),FadeIn(label('BMP low',3.35,0,GREEN,26)),run_time=.4)
        self.at('signal low');self.play(FadeIn(label('Neural tissue where BMP signaling is low',0,CAP,BLUE)),run_time=.35);self.finish()
class S18(SpokenScene):
    def construct(self):
        self.add(pair());self.at('what happens if');self.play(FadeIn(label('What happens if you turn the fly over?',0,CAP)),run_time=.4);self.finish()
class S19Pause(Scene):
    def construct(self):self.add(turn_question());self.wait(5)
class S20(SpokenScene):
    def construct(self):
        p=pair();self.add(p);self.at("it's bmp");self.play(turn(p[0]),run_time=2.4)
        self.at('the two maps');self.play(FadeIn(label('The two maps line up',0,CAP)),run_time=.4);self.finish()
class S21Beat(Scene):
    def construct(self):self.add(pair(flipped=True),label('The two maps line up',0,CAP));self.wait(2.5)

def ancestor():
    # No dorsal/ventral axis implied for the proposed ancestor.
    return VGroup(shell(R),band(R,-80,160,YELLOW,.7),band(R,100,160,GREEN,.7),
                  label('BMP',1.7,0,YELLOW),label('Chordin-like',-1.4,0,GREEN,26))
def ancestral_stage():
    return VGroup(ancestor(),label('De Robertis and Sasai · argued, 1996',0,3.65),label('Proposed common ancestor · orientation unspecified',0,-3.65,size=26))
def lineage(x,kind='fly',flip=False):
    g=VGroup(VGroup(shell(PR),band(PR,215,110,YELLOW),band(PR,10,160,GREEN,.48)),
             VGroup(label('dorsal',0,PR+.28,size=26),label('ventral',0,-PR-.28,size=26),
                    label('BMP',0,-1.1,YELLOW),label('antagonist',0,1.1,GREEN,26))).shift([x,CY,0])
    if flip:rotated_map(g)
    return g
class S22(SpokenScene):
    def construct(self):
        p=pair(flipped=True);self.add(p);self.at('in 1996')
        h=label('1996 · De Robertis and Sasai',0,CAP);self.play(FadeIn(h),run_time=.4)
        self.at('argued the common ancestor');self.play(FadeOut(p),FadeOut(h),FadeIn(ancestral_stage()),run_time=.7);self.finish()
class S23(SpokenScene):
    def construct(self):
        a=ancestral_stage();self.add(a);self.at('one lineage');l=lineage(-3.35);r=lineage(3.35)
        self.play(FadeOut(a),FadeIn(l),FadeIn(r),FadeIn(label('lineage 1',-3.35)),FadeIn(label('lineage 2',3.35)),run_time=.5)
        self.at('then inverted');self.play(turn(l),run_time=1.25);self.finish()
class S24(SpokenScene):
    def construct(self):
        l=lineage(-3.35,flip=True);r=lineage(3.35);tags=VGroup(label('lineage 1',-3.35),label('lineage 2',3.35))
        self.add(l,r,tags);self.at('on this view');self.play(turn(l),run_time=.8)
        self.at('one ancestral map');a=ancestral_stage();self.play(FadeOut(l),FadeOut(r),FadeOut(tags),FadeIn(a),run_time=.6)
        self.at('read from opposite sides');l=lineage(-3.35);r=lineage(3.35)
        self.play(FadeOut(a),FadeIn(l),FadeIn(r),FadeIn(tags),run_time=.35);self.play(turn(l),run_time=1.2);self.finish()

AR=2.3
AX=3.3
def anatomy(x,arth=True):
    # Schematic cross-section: cord on one side, gut dot, and a limb pair (arthropod) or notochord (vertebrate).
    sg=1 if arth else -1       # arthropod cord is ventral (bottom), vertebrate cord is dorsal (top)
    body=VGroup(shell(AR),Line([-1.1,-1.55*sg,0],[1.1,-1.55*sg,0],color=BLUE,stroke_width=9),
                Circle(.3,color=GREY,fill_color=GREY,fill_opacity=.5,stroke_width=2).shift([0,.5 if arth else -.7,0]))
    if arth:
        for a in [-125,-55]:
            u=np.array([np.cos(a*DEGREES),np.sin(a*DEGREES),0])
            body.add(Line(u*(AR-.05),u*(AR+.45),color=GREY,stroke_width=6))
        body.add(Line([-.9,1.7,0],[.9,1.7,0],color=GREY,stroke_width=3))
    else:
        body.add(Circle(.2,color=GREY,fill_color=GREY,fill_opacity=.5,stroke_width=2).shift([0,.15,0]))
    labs=VGroup(label('dorsal',0,AR+.3,size=26),label('ventral',0,-AR-.3,size=26),
                label('nerve cord',0,-.85 if arth else .85,BLUE,26))
    # dorsal/ventral labels sit outside the circle; the cord label inside it
    return VGroup(body,labs).shift([x,0,0])
def turn_anat(g,angle=PI):
    c=g[0][0].get_center();start=g.copy()
    def update(m,a):
        n=rotated_map(start.copy(),angle*a,c,AR);n[1][2].set_opacity(float(abs(np.cos(angle*a))**3));m.become(n)
    return UpdateFromAlphaFunc(g,update)
class S25(SpokenScene):
    def construct(self):
        a=anatomy(-AX);v=anatomy(AX,False);self.at('long before')
        self.add(a,v,label('arthropod · schematic',-AX,CAP,size=26),label('vertebrate · schematic',AX,CAP,size=26))
        self.at('in the 1820s');self.play(FadeIn(label('1820s · Geoffroy Saint-Hilaire',0,3.55)),run_time=.4)
        self.at('had proposed this inversion');self.play(turn_anat(a),run_time=2);self.finish()
class S26(SpokenScene):
    def construct(self):
        self.add(pair(flipped=True));self.at('the same contest')
        arrows=VGroup(*[Arrow([x,-.8,0],[x,.25,0],color=YELLOW,buff=0,stroke_width=6) for x in [-3.35,3.35]])
        self.play(*[GrowArrow(a) for a in arrows],run_time=.5)
        self.at('against its catcher');self.play(*[Create(Line([x-.5,.25,0],[x+.5,.25,0],color=GREEN,stroke_width=10)) for x in [-3.35,3.35]],run_time=.5)
        self.at('on opposite sides');self.play(FadeIn(label('Same BMP contest, on opposite sides of the body.',0,CAP)),run_time=.4);self.finish()
class S27End(EndCard):
    LINE='Same BMP contest, on opposite sides of the body.'
