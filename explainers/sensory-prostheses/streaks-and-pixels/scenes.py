"""Streaks and Pixels — revised, word-timed schematic animation.
COLOR MAP: BLUE hardware/native resolution; YELLOW current/fields;
PURPLE ganglion cells/axons; TEAL bipolar cells; ORANGE zoom/amber optogenetic light;
NIR dim red invisible near-infrared; GREEN participant endpoints; RED events;
TEXT percepts/people; GREY structure. All anatomy/percept outlines are schematics.
Gaussian fields and analytic axon trajectories are computed, not data traces.
"""
import numpy as np
from bp_style import *
PURPLE='#B58CD9'
ORANGE='#F29E4C'
NIR='#D98994'
GREY='#B5BDC9'
PIXEL_MAR=100/288*60
PIXEL_LOG=np.log10(PIXEL_MAR)
# Keep rendering side effects outside the chapter's protected audio/script files.
class Timed(SpokenScene):
    def at(self,phrase,lead=.2,nth=0):
        rest=self.t_of(phrase,nth)-lead-self.elapsed()
        if rest>.02:self.wait(rest)

def label(s,x=0,y=3.1,color=TEXT,size=28):
    return T(s,size=size,color=color,line_spacing=1.15).move_to([x,y,0])
def contact(x,y,size=.36,color=BLUE):
    return Square(side_length=size,stroke_color=color,stroke_width=3,fill_color=color,fill_opacity=.4).move_to([x,y,0])
def arr(a,b,color=GREY):return Arrow(a,b,buff=.08,color=color,stroke_width=3,tip_length=.18)
def leader(a,b,color=GREY):return Line(a,b,color=color,stroke_width=2)
def goggles(x=-4.4,y=.5,color=BLUE):
    return VGroup(*[RoundedRectangle(width=1.05,height=.7,corner_radius=.18,color=color,fill_color=color,fill_opacity=.15).move_to([x+d,y,0]) for d in (-.65,.65)],Line([x-.12,y,0],[x+.12,y,0],color=color))
def dome(x=0,base=-1.5,amp=1.7,s=.42,extent=.8):
    xs=np.linspace(x-extent,x+extent,80)
    ys=base+amp*np.exp(-.5*((xs-x)/s)**2)
    return VMobject(stroke_color=YELLOW,stroke_width=3,fill_color=YELLOW,fill_opacity=.16).set_points_as_corners([[a,b,0] for a,b in zip(xs,ys)]+[[x+extent,base,0],[x-extent,base,0]])
def axon(y,start=0,color=PURPLE):
    t=np.linspace(start,1,100)
    return VMobject(stroke_color=color,stroke_width=4).set_points_as_corners(np.column_stack([-5.7+6.3*t,(1-t)**2*y+2*(1-t)*t*(y+1.1)+t*t*.25,np.zeros_like(t)]))
def retina(with_electrode=True,model=False):
    paths=VGroup(*[axon(y) for y in (-2.3,-1.15,0,1.15,2.3)])
    somas=VGroup(*[Circle(radius=.15,color=PURPLE,fill_opacity=.65).move_to([-5.7,y,0]) for y in (-2.3,-1.15,0,1.15,2.3)])
    disk=Circle(radius=.34,color=GREY,fill_opacity=.2).move_to([.9,.25,0])
    panel=RoundedRectangle(width=3.7,height=5,corner_radius=.15,color=GREY,fill_color=GREY,fill_opacity=.06).move_to([4.35,0,0])
    # Single line heading is kept separate from the inset boundary.
    head=label('Modelled visual locations' if model else 'What the person sees',4.15,2.95,TEXT,26)
    el=contact(-3.4,.55,2.1)
    g=VGroup(paths,somas,disk,label('Retina · schematic',-2.5,3.15,GREY,28),label('optic disk',.8,-.55,GREY,26),panel,head)
    if with_electrode:g.add(el)
    return g,paths,el

def streak(x=4.35,y=0,h=3.5,w=.72,wobble=True,color=TEXT):
    # Analytic irregular silhouette, explicitly schematic, not participant data.
    t=np.linspace(0,TAU,160)
    r=1+.12*np.sin(3*t)+.07*np.sin(7*t+.4) if wobble else np.ones_like(t)
    pts=np.column_stack([w/2*r*np.cos(t),h/2*r*np.sin(t),np.zeros_like(t)])
    return VMobject(stroke_color=color,stroke_width=4,fill_color=color,fill_opacity=.15).set_points_as_corners(pts).close_path().rotate(-.38).move_to([x,y,0])
def prediction1():
    g,p,e=retina();return VGroup(g,label('What does the person see when it fires?',0,-3.05,TEXT,30))
RECRUIT_COLORS=(YELLOW,GREEN,TEAL)
def recruited():
    # At x=-3.4 the footprint spans y=-.5 to 1.6: exactly these three paths.
    return VGroup(*[axon(y,( -3.4+5.7)/6.3,c) for y,c in zip((-1.15,0,1.15),RECRUIT_COLORS)])
def locations():return VGroup(*[Dot([4.35+.26*i,.66*i,0],radius=.16,color=c) for i,c in zip((-1,0,1),RECRUIT_COLORS)])
def brain_links():
    return VGroup(chip('Brain',TEXT,30).move_to([.5,-2.05,0]),arr([.9,-.95,0],[.5,-1.6,0]),arr([1.4,-2.05,0],[2.6,-1.6,0]))
def cross_section():
    tissue=Rectangle(width=8.3,height=4.4,color=GREY,fill_color=GREY,fill_opacity=.05).move_to([-1.8,.1,0])
    ax=VGroup(*[Line([-5.7,1.5+j*.2,0],[2.1,1.5+j*.2,0],color=PURPLE,stroke_width=3) for j in range(3)],*[Circle(radius=.19,color=PURPLE,fill_opacity=.5).move_to([x,1.5,0]) for x in (-4,-1.8,.4)])
    cells=VGroup(*[VGroup(Line([x,-1.5,0],[x,.8,0],color=TEAL,stroke_width=4),Circle(radius=.24,color=TEAL,fill_color=TEAL,fill_opacity=.6).move_to([x,-.1,0])) for x in (-4,-1.8,.4)])
    pixels=VGroup(*[contact(x,-2.25,.72) for x in (-4,-1.8,.4)])
    labs=VGroup(label('Retina',-5.1,2.65,GREY,28),label('Ganglion cells\n+ axon layer',4.4,1.7,PURPLE,26),leader([2.2,1.7,0],[3,1.7,0],PURPLE),label('Bipolar cells',4.35,-.1,TEAL,26),leader([.7,-.1,0],[3,-.1,0],TEAL),label('PRIMA · subretinal',-1.8,-2.95,BLUE,28))
    return VGroup(tissue,ax,cells,pixels,labs),pixels,cells

def sx(v):return -5.65+11.1*v/2.15
AXY=-1.05
def scale_axis(y=AXY):
    axis=Line([sx(0),y,0],[sx(2.15),y,0],color=GREY,stroke_width=4)
    ticks=VGroup(*[VGroup(Line([sx(v),y-.12,0],[sx(v),y+.12,0],color=GREY),label(f'{v:g}',sx(v),y-.45,TEXT,26)) for v in (0,.5,1,1.5,2)])
    return VGroup(axis,ticks,label('logMAR',-4.7,y-1,GREY,26))
def markers(data=False):
    x=sx(PIXEL_LOG)
    a=VGroup(arr([x,.2,0],[x,AXY,0],BLUE),label('Pixel estimate · 1.32',x,.65,BLUE,28),label('About 20/420',x,1.2,BLUE,28))
    b=VGroup(Line([x,AXY,0],[x,-2.1,0],color=TEXT,stroke_width=4),leader([x,-2.1,0],[0,-2.55,0]),label('PRIMAvera native mean · 1.32',0,-2.85,TEXT,28))
    return VGroup(a,b) if data else a

def prediction2():
    pixel=contact(-4,.65,2.4)
    field=dome(-4,-.4,1.8,.5,1.05)
    measure=VGroup(Line([-5.2,-.85,0],[-2.8,-.85,0],color=BLUE),label('100 µm',-4,-1.3,BLUE,30))
    # No spatial answer cue: scale and unknown belong to separate panels.
    divider=Line([-1.8,-2.8,0],[-1.8,2.6,0],color=GREY)
    axis=VGroup(Line([-.95,-1.5,0],[5.85,-1.5,0],color=GREY),*[VGroup(Line([-.95+6.8*v/2.15,-1.6,0],[-.95+6.8*v/2.15,-1.4,0],color=GREY),label(f'{v:g}',-.95+6.8*v/2.15,-1.95,TEXT,26)) for v in (0,.5,1,1.5,2)],label('logMAR',.1,-2.55,GREY,26))
    q=label('If the field stays within the pixel,\nwhat acuity could it give?',2.2,1.8,TEXT,28)
    blank=label('Your estimate:  ?',2.2,.35,TEAL,32)
    return VGroup(VGroup(divider,axis),pixel,field,measure,q,blank)

def opto():
    panel=RoundedRectangle(width=8.2,height=4.9,corner_radius=.2,color=ORANGE,fill_color=ORANGE,fill_opacity=.05).move_to([1.65,.25,0])
    cells=VGroup(*[VGroup(Circle(radius=.7,color=PURPLE,fill_color=PURPLE,fill_opacity=.15).move_to([x,.3,0]),Line([x,1,0],[x,1.8,0],color=PURPLE,stroke_width=4)) for x in (-.8,1.65,4.1)])
    pores=VGroup(*[VGroup(Line([x-.15,-.38,0],[x-.15,-.14,0],color=ORANGE,stroke_width=6),Line([x+.15,-.38,0],[x+.15,-.14,0],color=ORANGE,stroke_width=6)) for x in (-.8,1.65,4.1)])
    labels=VGroup(label('Ganglion cells',1.65,2.35,PURPLE,30),label('ChrimsonR, a light-gated channel',1.65,-1.45,ORANGE,28),leader([1.65,-1.1,0],[1.65,-.45,0],ORANGE))
    return VGroup(panel,cells,pores,labels,goggles(-4.4,.3,ORANGE))

class S00Title(TitleCard):
    LESSON='Restoring Senses: Implants, Prostheses and Optogenetic Vision'
    TITLE='Streaks and Pixels'
    def construct(self):
        self.add(label('BIOCHEMISTRYPEDIA',0,2.5,TEAL,28),label('Restoring Senses: Implants, Prostheses\nand Optogenetic Vision',0,1.2,GREY,28))
        self.play(FadeIn(label(self.TITLE,0,-.6,TEXT,54)),run_time=.7);self.finish()
class S01Q(Timed):
    def construct(self):
        grid=VGroup(*[contact(-5.2+i*1.02,-1.8+j*1.02,.63) for i in range(4) for j in range(4)])
        strip=RoundedRectangle(width=4.3,height=4.5,corner_radius=.3,color=PURPLE,fill_opacity=.08).move_to([-3.65,-.25,0])
        self.at('Put a grid');self.play(FadeIn(strip),FadeIn(grid),FadeIn(label('Electrodes on retina',-3.65,2.8,BLUE,30)),run_time=.5)
        self.at('Do you get')
        dots=VGroup(*[Dot([2.1+i*1.02,-1.8+j*1.02,0],radius=.24,color=TEXT) for i in range(4) for j in range(4)])
        self.play(FadeIn(dots),FadeIn(label('?',0,-.2,TEXT,110)),FadeIn(label('A grid of dots?',3.65,2.8,TEXT,30)),run_time=.5);self.finish()
class S02Argus(Timed):
    def construct(self):
        self.add(label('Argus II · epiretinal',0,3.15,BLUE,36),goggles(-4.35,.6).scale(1.35),contact(-4.35,1.65,.45),label('Camera',-4.35,2.3,BLUE,28))
        self.at('A camera drove')
        array=VGroup(*[contact(-.7+i*.61,-1.7+j*.61,.3) for i in range(10) for j in range(6)])
        tissue=RoundedRectangle(width=6.5,height=4.1,corner_radius=.4,color=PURPLE,fill_opacity=.08).move_to([2.05,-.15,0])
        self.play(FadeIn(tissue),FadeIn(array),GrowArrow(arr([-2.8,.5,0],[-1.5,.5,0],YELLOW)),FadeIn(label('da Cruz and colleagues, 2016',0,-3.15,GREY,28)),run_time=.6)
        self.at('inner surface');self.play(FadeIn(label('60 electrodes · inner retinal surface',1.6,-2.6,BLUE,28)),run_time=.4);self.finish()
class S03Anatomy(Timed):
    def construct(self):
        g,p,e=retina(False);self.add(g)
        self.at('But ganglion cell');self.play(Indicate(p,color=PURPLE),run_time=.8)
        self.at('toward the optic');self.play(LaggedStart(*[ShowPassingFlash(a.copy().set_color(YELLOW),time_width=.5) for a in p],lag_ratio=.1),run_time=1.3);self.finish()
class S04Predict(Timed):
    def construct(self):
        g,p,e=retina(False);self.add(g)
        cue=label('Predict',0,-3.05,TEAL,30);self.at('Predict');self.add(cue)
        self.at('Axons from elsewhere');e.shift(UP*1);self.play(FadeIn(e),e.animate.shift(DOWN),run_time=.7)
        self.at('What does the');self.play(ReplacementTransform(cue,prediction1()[1]),run_time=.4);self.finish()
class S05Pause(Scene):
    def construct(self):self.camera.background_color=BG;self.add(prediction1());self.wait(5)
class S06Reveal(Timed):
    def construct(self):
        g,p,e=retina();self.add(g)
        self.at('often not a dot');self.play(Indicate(e,color=YELLOW),run_time=.45)
        self.play(Create(streak()),FadeIn(label('Beyeler and colleagues, 2019 · four implant users',0,-3.3,GREY,28)),run_time=1.2)
        self.at('Four implant users');self.add(label('Participant-style drawing · schematic',0,-2.75,TEXT,26));self.finish()
class S07Why(Timed):
    def construct(self):
        g,p,e=retina(model=True);self.add(g)
        r=recruited();self.at('Each passing axon');self.play(Create(r),run_time=.7)
        self.at('carries signals');self.play(LaggedStart(*[ShowPassingFlash(a.copy(),time_width=.5) for a in r],lag_ratio=.1),FadeIn(brain_links()),run_time=1)
        self.at('a different part');self.play(FadeIn(locations()),run_time=.5)
        self.add(label('Matching colours: one axon → one location',-.5,-3.15,TEXT,28));self.finish()
class S08Streak(Timed):
    def construct(self):
        g,p,e=retina(model=True);r=recruited();dots=locations();self.add(g,r,dots,brain_links())
        self.at('Recruit cells along');self.play(Indicate(r,color=YELLOW),run_time=.7)
        self.at('a stretch of visual');self.play(Indicate(dots,color=YELLOW),run_time=.5)
        self.at('can produce a streak');self.play(ReplacementTransform(dots,streak()),run_time=.8)
        self.add(label('Axon-pathway model · can produce a streak',0,-3.15,GREY,28));self.finish()
class S09Model(Timed):
    def construct(self):
        self.add(label('Participant-style drawing',-3.2,3,TEXT,28),streak(-3.2,.3,4.8,1.05),label('Schematic comparison',0,-2.25,GREY,26))
        self.at('A model of');self.play(Create(streak(3.2,.3,4.5,.85,False,PURPLE)),FadeIn(label('Model shape',3.2,3,PURPLE,28)),run_time=.7)
        self.add(label('Similar elongated shape, not an exact match',0,-2.8,TEXT,28))
        self.at('It is a');self.add(label('Model-supported explanation · not a recording',0,-3.35,GREY,26));self.finish()
class S10Idea(Timed):
    def construct(self):
        g,p,e=retina();self.add(g,e,label('Electrode',-3.4,-2.25,BLUE,28),leader([-3.4,-1.95,0],[-3.4,-.65,0],BLUE))
        expected=DashedVMobject(Circle(radius=.28,color=BLUE).move_to([3.15,-1.6,0]))
        self.add(expected,label('Expected',3.5,-2.25,BLUE,26),label('Recruited',4.5,2.15,TEXT,26))
        self.at('The current reaches');self.play(Create(streak(4.65,.5,2.6)),run_time=.65)
        self.at('whose place on');self.play(GrowArrow(arr([3.35,-1.35,0],[4.4,-.15,0],YELLOW)),run_time=.5);self.finish()
class S11Fix(Timed):
    def construct(self):
        g,p,c=cross_section();self.add(g[0],g[1],g[2],g[4][0],g[4][1],g[4][2],label('Design arguments · not a controlled comparison',0,-3.45,GREY,26))
        e=contact(-1.8,2.45,.7);field=dome(-1.8,.8,1.7,1.4,2.4)
        tag=label('Epiretinal electrode',-.4,3.2,BLUE,28);self.add(e,field,tag)
        self.at('move the electrode');self.play(e.animate.move_to([-1.8,-2.25,0]),FadeOut(tag),Transform(field,dome(-1.8,-1.9,3.6,1.2,2)),FadeIn(g[4][5]),run_time=1)
        self.at('keep each field');self.play(Transform(field,dome(-1.8,-1.9,2,.4,.75)),run_time=.7)
        self.at('chip does both');self.play(FadeIn(p[0]),FadeIn(p[2]),FadeIn(g[4][3]),FadeIn(g[4][4]),run_time=.4)
        self.finish()
class S12Bipolar(Timed):
    def construct(self):
        g,p,c=cross_section();g[4][0].move_to([-5.6,2.65,0]);self.add(g)
        self.add(label('Near-infrared · invisible light',0,3.25,NIR,30))
        self.at('light powers its');beams=VGroup(*[arr([x-.8,2.8,0],[x,-1.7,0],NIR) for x in (-4,-1.8,.4)])
        self.play(FadeIn(beams),run_time=.4)
        self.at('Each pixel stimulates');fields=VGroup(*[dome(x,-1.9,3,.95,1.5) for x in (-4,-1.8,.4)])
        self.play(FadeIn(fields),*[Indicate(cell[1],color=YELLOW,scale_factor=1.5) for cell in c],run_time=.7)
        self.play(FadeOut(beams),run_time=.25)
        self.at('a local return');rings=VGroup(*[Ellipse(width=1.6,height=.3,color=BLUE,stroke_width=5).move_to([x,-1.9,0]) for x in (-4,-1.8,.4)])
        self.play(FadeIn(rings),Transform(fields,VGroup(*[dome(x,-1.9,2,.4,.75) for x in (-4,-1.8,.4)])),FadeIn(label('Local return\nelectrode',4.3,-1.8,BLUE,26)),Create(leader([1.2,-1.9,0],[3,-1.9,0],BLUE)),run_time=1);self.finish()
class S13Logmar(Timed):
    def construct(self):
        axis=scale_axis();axis[2].move_to([5.4,-1.85,0])
        self.add(axis,label('Visual acuity · logMAR',0,3.2,TEXT,36))
        # Relative optotype sizes demonstrate the tenfold angle ratio, not a test chart.
        self.add(label('E',sx(0),1.2,TEXT,26),label('E',sx(1),1.2,TEXT,260),label('Relative chart-symbol sizes · schematic',0,-3.25,GREY,26))
        self.at('0 is 2020');self.play(Create(leader([sx(0),-1.75,0],[sx(0),-2.1,0])),FadeIn(label('20/20',sx(0)+.1,-2.45,TEXT,28)),run_time=.4)
        self.at('1 is 20');self.play(Create(leader([sx(1),-1.75,0],[sx(1),-2.1,0])),FadeIn(label('20/200',sx(1),-2.45,TEXT,28)),run_time=.4)
        self.at('Higher is worse');self.play(GrowArrow(arr([sx(0),-2.95,0],[sx(2),-2.95,0])),FadeIn(label('Higher = worse',2.9,-2.5,GREY,28)),run_time=.5);self.finish()
class S14Predict2(Timed):
    def construct(self):
        g=prediction2();self.add(g[0],label('Predict',0,3.15,TEAL,32))
        self.at('Each pixel is');self.play(FadeIn(g[1]),FadeIn(g[3]),run_time=.5)
        self.at('If its field');self.play(FadeIn(g[2]),run_time=.5)
        self.at('what acuity could');self.play(FadeIn(g[4]),FadeIn(g[5]),run_time=.4);self.finish()
class S15Pause(Scene):
    def construct(self):self.camera.background_color=BG;self.add(prediction2(),label('Pause and predict',0,3.15,TEAL,32));self.wait(5)
class S16Reveal2(Timed):
    def construct(self):
        self.add(scale_axis(),label('Smallest detail = one pixel width',0,3.25,TEXT,30))
        pattern=VGroup(*[Square(side_length=.32,color=BLUE,fill_color=BLUE,fill_opacity=1 if i%2==0 else 0).move_to([-5.1+i*.32,2.45,0]) for i in range(6)])
        self.add(pattern,label('Alternating on / off',-.7,2.45,GREY,26))
        eq=[label('100 µm / (288 µm per degree)',-1.4,1.65,TEXT,28),label(f'= {100/288:.2f} degree = {PIXEL_MAR:.1f} arcmin',-1.4,.8,TEXT,28),label(f'log10({PIXEL_MAR:.1f}) = {PIXEL_LOG:.2f} logMAR',-1.4,-.05,TEXT,28)]
        self.at('The conversion is');self.play(FadeIn(eq[0]),run_time=.4);self.wait(1.3)
        self.play(FadeIn(eq[1]),run_time=.4);self.wait(1.3)
        self.play(FadeIn(eq[2]),run_time=.4);self.wait(1.3)
        self.at('The pixel limit')
        x=sx(PIXEL_LOG)
        mark=VGroup(arr([x,-2.55,0],[x,AXY,0],BLUE),label('1.32 · about 20/420',x,-3.05,BLUE,30))
        self.play(FadeIn(mark),run_time=.6);self.finish();self.wait(1)
class S17Data(Timed):
    def construct(self):
        self.add(scale_axis(),markers(),label('PRIMAvera · Holz and colleagues',0,3.2,TEXT,30),label('Native resolution · no zoom',0,2.45,GREY,28))
        self.at('own resolution was');self.play(FadeIn(markers(True)[1]),run_time=.6)
        self.add(label('Mean of the trial participants',0,-3.4,GREY,26),label('38 implanted · 32 assessed at 12 months',0,1.85,GREY,26));self.finish()
class S18Match(Timed):
    def construct(self):
        m=markers(True)
        conversion=VGroup(T('100 µm / (',size=30,color=BLUE),T('288',size=30,color=BLUE),T('µm per degree)',size=30,color=BLUE)).arrange(RIGHT,buff=.12).move_to([0,3.15,0])
        self.add(scale_axis(),m,conversion)
        # Uncalibrated schematic band: no numerical range is implied.
        band=Rectangle(width=.8,height=1.65,color=BLUE,stroke_width=0,fill_color=BLUE,fill_opacity=.2).move_to([sx(PIXEL_LOG),-.8,0])
        self.at('The measured mean');self.play(FadeIn(band),Flash([sx(PIXEL_LOG),AXY,0],color=YELLOW,flash_radius=.42),Indicate(m,color=YELLOW),run_time=.8)
        self.at('Eyes differ in size');self.add(label('Varies with eye length',2.7,2.35,GREY,28),leader(conversion[1].get_bottom()+DOWN*.1,[2.2,2.65,0]))
        self.at('treat it as agreement');self.add(label('Close to the estimate',-3.1,1.5,TEXT,28))
        self.at('not a precise');self.add(label('Eye length shifts this\nSchematic band',-3.2,.25,GREY,26),label('Mean shown without spread',0,-3.4,GREY,26));self.finish()
class S19ArgusLimit(Timed):
    def construct(self):
        self.add(scale_axis(),label('Argus II',0,3.15,BLUE,36))
        self.at('an ideal grid');self.add(label('575 µm / (288 µm per degree) ≈ 2°',0,2.65,BLUE,28))
        x=sx(np.log10(2400/20));xx=sx(np.log10(1260/20))
        self.at('would give about');self.play(FadeIn(VGroup(Dot([x,AXY,0],color=BLUE),leader([x,AXY,0],[x,-.75,0],BLUE),leader([x,.6,0],[x,.9,0],BLUE),leader([x,.9,0],[3.8,1.25,0],BLUE),label('Nominal static estimate\n20/2400',3.6,1.75,BLUE,28))),run_time=.5)
        self.at('Yet its best');self.play(FadeIn(VGroup(Dot([xx,AXY,0],color=TEXT),leader([xx,AXY,0],[xx,-2,0]),leader([xx,-2,0],[2.4,-2.4,0]),label('Best reported grating acuity · 20/1260',1.2,-2.75,TEXT,28))),run_time=.5)
        self.add(label('Humayun and colleagues, 2012',0,-3.35,GREY,28))
        self.at('So this is');self.add(Line([xx,-.5,0],[x,-.5,0],color=YELLOW),Line([xx,-.5,0],[xx,-.7,0],color=YELLOW),Line([x,-.5,0],[x,-.7,0],color=YELLOW),label('Finer than the estimate',xx-1.95,-.5,TEXT,24),label('Not a hard limit',(xx+x)/2,.1,GREY,26));self.finish()
class S20Zoom(Timed):
    def construct(self):
        self.add(label('Two cautions',0,3.2,TEXT,36),Line([-.6,-3.2,0],[-.6,2.5,0],color=GREY),label('1 · Zoom adds a magnifier',-3.65,2.45,ORANGE,28),label('2 · Benefit and serious events',3,2.45,TEXT,28))
        def image(x,y,step):return VGroup(*[Square(side_length=step*.9,color=BLUE,fill_color=BLUE,fill_opacity=.75 if (i+j)%3 else .1).move_to([x+(i-1.5)*step,y+(j-1.5)*step,0]) for i in range(4) for j in range(4)])
        small=image(-4.9,.4,.3);large=image(-2.7,.4,.65)
        lens=VGroup(Circle(radius=1.45,color=ORANGE).move_to([-2.7,.4,0]),Line([-1.7,-.65,0],[-1.1,-1.4,0],color=ORANGE,stroke_width=8))
        self.add(small,large,lens,label('Same 4 × 4 pixels',-3.6,-1.65,TEXT,28),label('Zoom · 1–12×',-3.6,-2.35,ORANGE,30))
        # Two report columns with actual denominators, not equal-height decorative bars.
        self.add(Line([-.1,1.75,0],[2.3,1.75,0],color=GREEN),Line([2.9,1.75,0],[5.3,1.75,0],color=RED),label('Benefit',1.1,1.15,GREEN,30),label('Serious device-\nor procedure-\nrelated events',4.1,.75,RED,26))
        self.at('serious device');self.add(label('26 / 32\nassessed met\nzoom-allowed\nendpoint',1.1,-.3,TEXT,26),label('26 events\nin 19 / 38\nimplanted',4.1,-.95,TEXT,26),label('Single-arm · open-label',2.6,-2.5,GREY,28));self.finish()
class S21Opto(Timed):
    def construct(self):
        g=opto();self.add(g[0],g[1],g[3],g[4],label('Optogenetics',0,3.25,ORANGE,36))
        self.at('express a light');self.play(FadeIn(g[2]),run_time=.5);self.finish()
class S22Goggles(Timed):
    def construct(self):
        g=opto();self.add(g,label('Optogenetics',0,3.25,ORANGE,36))
        beams=VGroup(*[arr([-3,.3,0],[x,.3,0],ORANGE).set_opacity(.5) for x in (-1.5,.95,3.4)])
        self.at('Goggles supply');self.add(beams)
        pulses=VGroup(*[Dot(radius=.09,color=ORANGE) for _ in range(3)])
        for i,d in enumerate(pulses):
            start=np.array([-3,.3,0]);end=np.array([(-1.5,.95,3.4)[i],.3,0])
            d.add_updater(lambda m,dt,a=start,b=end,k=i: m.move_to(a+(b-a)*((self.elapsed()*.7+k*.27)%1)))
        self.add(pulses)
        self.at('bright amber light');self.play(Indicate(g[2],color=ORANGE),run_time=.6)
        self.at('part of the encoding');self.add(label('Bright amber light + part of the encoding',0,-2.95,ORANGE,30));self.finish()

def cup(x,y):
    return VGroup(Rectangle(width=.55,height=.75,color=TEXT),Arc(radius=.23,start_angle=-PI/2,angle=PI,color=TEXT).move_to([.42,0,0])).move_to([x,y,0])
def hand(x,y):
    palm=RoundedRectangle(width=.62,height=.7,corner_radius=.15,color=TEXT,fill_color=TEXT,fill_opacity=.16)
    fingers=VGroup(*[Line([-.22+i*.14,.25,0],[-.22+i*.14,.7-(i%2)*.08,0],color=TEXT,stroke_width=5) for i in range(4)])
    thumb=Line([.28,.05,0],[.52,.3,0],color=TEXT,stroke_width=6)
    arm=Line([0,-.35,0],[-.4,-1.15,0],color=TEXT,stroke_width=12)
    return VGroup(palm,fingers,thumb,arm).move_to([x,y,0])
class S23Test(Timed):
    def construct(self):
        self.add(*[RoundedRectangle(width=5.8,height=5.3,corner_radius=.2,color=GREY).move_to([x,.3,0]) for x in (-3.2,3.2)])
        objects=VGroup(*[cup(x+j*.95,.5) for x in (-4.2,2.2) for j in range(3)])
        hl=hand(-4.8,-1.1);hr=hand(1.6,-1.1)
        self.add(objects,hl,hr,label('With goggles',-3.2,2.45,ORANGE,30),label('Same objects',3.2,2.45,GREY,28),label('Sahel and colleagues, 2021',0,-2.85,GREY,28),label('One patient · not normal vision',0,-3.4,GREY,28))
        self.at('one patient located');self.play(hl.animate.move_to([-4.1,-.55,0]),run_time=.6)
        self.at('counted and touched');self.play(FadeIn(VGroup(*[label(str(i+1),-4.2+i*.95,1.35,TEXT,28) for i in range(3)])),hl.animate.shift(RIGHT*1.45),run_time=.7)
        self.add(label('Located · counted · touched',-3.2,-1.95,TEXT,26))
        self.at('Without them');self.play(FadeIn(label('Without goggles',3.2,1.6,GREY,28)),run_time=.35)
        self.at('did not detect');self.add(label('No object detection\nNo reach',4.1,-1.65,TEXT,26));self.finish()
class S24Takeaway(Timed):
    def construct(self):
        # Full three-row structure is present from the beginning; each row brightens at its cue.
        icons=VGroup(streak(-3.9,1.95,1.25,.45),contact(-3.9,0,1.15),goggles(-3.9,-1.95,ORANGE))
        texts=VGroup(label('Wrong neurons\ncan distort percepts',1,1.95,TEXT,32),label('PRIMA mean acuity\nnear its pixel estimate',1,0,BLUE,32),label('Light pattern picks\nthe driven cells',1,-1.95,ORANGE,32))
        self.add(icons.copy().set_opacity(.18),texts.copy().set_opacity(.18),label('Not a controlled head-to-head comparison',0,-3.35,GREY,28))
        self.at('Where current reaches');self.play(FadeIn(icons[0]),FadeIn(texts[0]),run_time=.5)
        self.at("Prima's mean acuity");self.play(FadeIn(icons[1]),FadeIn(texts[1]),run_time=.5)
        self.at('With optogenetics');self.play(FadeIn(icons[2]),FadeIn(texts[2]),run_time=.5);self.finish()
class S25End(EndCard):
    LINE='Detail depends on which neurons each electrode or pixel reaches,\nnot just on how many there are.'
    def construct(self):
        self.add(label('Detail depends on which neurons',0,1.5,TEXT,38),label('each electrode or pixel reaches,',0,.55,TEXT,38),label('not just on how many there are.',0,-.65,TEXT,38),label('biochemistrypedia.com',0,-2.5,TEAL,28));self.finish()
