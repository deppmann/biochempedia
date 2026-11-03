"""Chapter 2: The Light Response That Survived the Block.
COLOR MAP shared with scenes.old.py and the chapter series:
YELLOW = light, clock/pupil outputs, questions; BLUE = rods/cones and bipolar relay;
GREEN = ipRGC and melanopsin; PURPLE = brain targets; RED = blocked/lost;
GREY = outlines/de-emphasis; TEXT = labels.
Only scenes.py and requested output artifacts are edited; CHAPTERS.md is read-only
under the task's final edit restriction, so the shared map is recorded here.

Response plots are computed by interpolation of an ordinal encoding of the lesson's
signature-response table (lesson.mdx, 'The signature response'): fast onset,
partial adaptation, sustained; slow onset, slight adaptation, slow offset.
They have no numerical time/voltage calibration and are labelled schematic examples,
not recordings or fitted kinetics. No experimental amplitude or time constant is claimed.
Spectrum: Govardovskii A1 alpha-band template, peak parameter 484 nm from the lesson.
Template equation source: https://link.springer.com/article/10.1007/s00359-010-0568-7
Primary template: https://doi.org/10.1017/S0952523800174036
"""
import numpy as np
from bp_style import *
PURPLE = "#B58CD9"

def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def cell(cx, cy, w, h, color, fill=0.22, dashed=False):
    e = Ellipse(width=w, height=h, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=fill)
    if dashed:
        e = DashedVMobject(e, num_dashes=24)
        e.set_fill(color, fill)
    return e.move_to([cx, cy, 0])


def cross(center, s=0.35, color=RED, w=7):
    c = np.array(center, float)
    return VGroup(Line(c + [-s, -s, 0], c + [s, s, 0], color=color, stroke_width=w),
                  Line(c + [-s, s, 0], c + [s, -s, 0], color=color, stroke_width=w))


def light_arrow(x, ytop, ybot):
    return arr([x, ytop, 0], [x, ybot, 0], YELLOW, w=6)


def clock_icon(cx, cy, r=0.55):
    """A clock: ring and two hands. .h2 is the hand that turns; .c is the centre."""
    c = np.array([cx, cy, 0.0])
    ring = Circle(radius=r, stroke_color=YELLOW, stroke_width=4).move_to(c)
    h1 = Line(c, c + [0, r * 0.7, 0], color=YELLOW, stroke_width=4)
    h2 = Line(c, c + [r * 0.62 * np.cos(PI / 6), r * 0.62 * np.sin(PI / 6), 0], color=YELLOW, stroke_width=4)
    g = VGroup(ring, h1, h2)
    g.h2, g.c, g.r = h2, c, r
    return g


def dim_anims(g, o=0.3):
    """Animations that fade a flat group toward opacity o without turning its fill on."""
    return [m.animate.set_stroke(opacity=o).set_fill(opacity=m.get_fill_opacity() * o) for m in g.submobjects]


def dim_static(g, o=0.3):
    for m in g.submobjects:
        m.set_stroke(opacity=o)
        m.set_fill(opacity=m.get_fill_opacity() * o)
    return g


def eye_icon(cx, cy, w=1.5):
    """A pupil icon: eye outline, iris, dark pupil. .pup is the pupil."""
    c = [cx, cy, 0]
    eye = Ellipse(width=w, height=w * 0.57, stroke_color=YELLOW, stroke_width=4).move_to(c)
    iris = Circle(radius=w * 0.24, stroke_width=0, fill_color=GREY, fill_opacity=0.6).move_to(c)
    pup = Circle(radius=w * 0.16, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(c)
    g = VGroup(eye, iris, pup)
    g.pup = pup
    return g



def label(s, x=0, y=3, size=30, color=TEXT):
    return T(s, max(size,26), color).move_to([x,y,0])


def neuron(x=2.6, y=0, w=3.8, h=2.7):
    return VGroup(cell(x,y,w,h,GREEN,fill=.12), label('ganglion cell',x,y,26,GREEN))


def relay():
    rc=VGroup(cell(-4.7,0,2.5,4.7,BLUE),label('rods and\ncones',-4.7,0,28,BLUE))
    bp=VGroup(cell(-.7,0,2,4.7,BLUE),label('bipolar\ncell',-.7,0,28,BLUE))
    gc=VGroup(cell(3.65,0,3,4.7,GREEN),label('ganglion\ncell',3.65,0,28,GREEN))
    links=VGroup(arr([-3.4,0,0],[-1.75,0,0],BLUE),arr([.4,0,0],[2.1,0,0],BLUE))
    cuts=VGroup(*[VGroup(*[DashedVMobject(line,num_dashes=6) for line in cross([x,0,0],.33)]) for x in [-2.6,1.25]])
    return rc,bp,gc,links,cuts


def clouds():
    return VGroup(*[Ellipse(width=1.1,height=2.5,color=RED,fill_color=RED,fill_opacity=.13).move_to([x,0,0]) for x in [-2.6,1.25]])


def dish():
    rim=Ellipse(width=9.6,height=5.4,color=GREY,stroke_width=4)
    retina=Ellipse(width=8.6,height=4.7,color=GREEN,fill_color=GREEN,fill_opacity=.10)
    cells=VGroup(*[cell(x,y,.9,.7,GREY,fill=.2) for x,y in [(-2.7,0),(-1.4,1.2),(.4,1),(2.5,0),(.7,-1.2),(-1.6,-1.2)]])
    return VGroup(rim,retina,cells)


def pipette(point=(.4,1,0)):
    p=np.array(point)
    return Polygon(p,p+[1.5,1.5,0],p+[2.1,1.5,0],color=GREY,fill_color=GREY,fill_opacity=.15,stroke_width=3)

# Ordinal data from the lesson table: baseline/onset/held/offset/recovery.
# Piecewise interpolation avoids implying a measured kinetic fit.
RELAY_T=np.array([0,1,1.12,1.3,1.8,2.8,4.8,6,6.12,6.4,9])
RELAY_Y=np.array([0,0,.85,1,.8,.6,.57,.55,.25,0,0])
OWN_T=np.array([0,1,1.4,2,2.8,3.8,4.8,6,6.8,7.8,9])
OWN_Y=np.array([0,0,.03,.28,.63,.88,.93,.86,.65,.39,.18])

def value(t,own=True):
    return np.interp(t,OWN_T if own else RELAY_T,OWN_Y if own else RELAY_Y)


def trace(y,own=True,start=0,end=9,amp=1.2,x0=-5.1,width=10.2,noise=False):
    ts=np.linspace(start,end,max(2,int((end-start)*65)))
    ys=np.array([value(t,own) for t in ts])
    if noise:
        # Deterministic illustrative baseline noise, not physiological measurements.
        ys += .012*np.sin(ts*83)+.009*np.sin(ts*137)
    pts=[[x0+width*t/9,y+amp*v,0] for t,v in zip(ts,ys)]
    return VMobject(color=GREEN if own else BLUE,stroke_width=5).set_points_as_corners(pts)


X0=-4.6
WIDTH=10.1
TOP=.75
BOTTOM=-1.9
AMP=1.95

def wave(y,own=True,start=0,end=9,amp=AMP):
    return trace(y,own,start,end,amp,X0,WIDTH)


def lightbar(y=-2.5):
    on=X0+WIDTH/9; off=X0+WIDTH*6/9
    return VGroup(Line([X0,y,0],[5.5,y,0],color=GREY,stroke_width=3),
      Line([on,y,0],[off,y,0],color=YELLOW,stroke_width=10),
      label('on',on,y-.36,26,YELLOW),label('off',off,y-.36,26,YELLOW),
      label('time →',5,y-.36,26))


def lamp(x,y,bright=False):
    g=VGroup(Circle(radius=.15,color=YELLOW,fill_color=YELLOW,fill_opacity=1 if bright else .18).move_to([x,y,0]))
    for a in np.linspace(0,TAU,8,endpoint=False):
        v=np.array([np.cos(a),np.sin(a),0])
        g.add(Line(np.array([x,y,0])+v*.24,np.array([x,y,0])+v*(.44 if bright else .31),color=YELLOW,stroke_opacity=1 if bright else .35))
    return g


def comparison():
    axes=VGroup(Line([X0,2.9,0],[X0,-2.05,0],color=GREY),
       *[DashedLine([X0,y,0],[5.5,y,0],color=GREY,stroke_opacity=.5) for y in [TOP,BOTTOM]],
       label('response (a.u.)',-6,0,26).rotate(PI/2),
       label('0',-4.95,TOP,26),label('0',-4.95,BOTTOM,26))
    names=VGroup(label('rods / cones relay',-2.3,3.18,28,BLUE),label('melanopsin',-3,.25,28,GREEN))
    return VGroup(axes,names,lightbar(),label('Schematic example • amplitudes arbitrary',0,-3.42,26))


def prediction():
    return VGroup(label('Relay only, after the block?',0,3.15,32,YELLOW),
      Line([X0,-1.6,0],[X0,2.6,0],color=GREY),
      Line([X0,-1.6,0],[5.5,-1.6,0],color=GREY),
      label('membrane voltage (a.u.)',-5.9,.45,26).rotate(PI/2),lightbar(-2.15),
      label('What should the recording show?',0,-3.2,28),
      label('0',-4.95,-1.15,26))


def meter(x=2.9):
    box=RoundedRectangle(width=4.6,height=4.9,corner_radius=.25,color=GREEN,fill_color=GREEN,fill_opacity=.08).move_to([x,0,0])
    ticks=VGroup(*[Line([x-1.6+i*.4,1.4,0],[x-1.6+i*.4,1.7,0],color=GREY) for i in range(9)])
    needle=Line([x,-1.5,0],[x+.45,1.3,0],color=YELLOW,stroke_width=6)
    return VGroup(box,ticks,needle)

def spectrum(w):
    x=484/np.asarray(w)
    a=.8795+.0459*np.exp(-((484-300)**2)/11940)
    return 1/(np.exp(69.7*(a-x))+np.exp(28*(.922-x))+np.exp(-14.9*(1.104-x))+.674)


class S00Title(TitleCard):
    LESSON='Melanopsin Cells: Light for the Clock and the Pupil'
    TITLE='The Light Response That Survived the Block'

    def construct(self):
        # Wrapped at readable sizes rather than shrinking the house title.
        self.add(label('BIOCHEMISTRYPEDIA',0,2.7,22,TEAL),
          label('Melanopsin Cells: Light for the Clock and the Pupil',0,1.65,24,GREY),
          T('The Light Response\nThat Survived the Block',font=TITLE_FONT,size=46,line_spacing=1.1),
          Line([-1.2,-1.7,0],[1.2,-1.7,0],color=GOLD,stroke_width=4))
        self.finish()


class S01Q(SpokenScene):
    def construct(self):
        rc,bp,gc,links,cuts=relay()
        self.add(rc,bp,gc,links,label('Whose response is it?',0,-3.1,36,YELLOW))
        self.at('Cut a ganglion cell')
        self.play(ReplacementTransform(links,VGroup(*[DashedVMobject(a) for a in links])),Create(cuts),run_time=.6)
        self.at('If it still responds')
        self.play(GrowArrow(light_arrow(3.65,3.35,2.45)),FadeIn(label('light',5.2,3,28,YELLOW)),gc[0].animate.set_fill(GREEN,.4),run_time=.65)
        self.at('whose response is it')
        self.play(Indicate(self.mobjects[4],color=YELLOW),run_time=.5)
        self.finish()


class S02Logic1(SpokenScene):
    def construct(self):
        rc,bp,gc,links,cuts=relay(); self.add(rc,bp,gc)
        self.at('Here is the logic')
        self.at('Rods and cones reach')
        self.play(Create(links),run_time=.6)
        self.at('through synapses')
        syn=label('synapses',0,-3,30,BLUE)
        self.play(FadeIn(syn),run_time=.4)
        self.at('Block those synapses')
        self.play(ReplacementTransform(links,VGroup(*[DashedVMobject(a.copy().set_color(GREY)) for a in links])),FadeIn(clouds()),Create(cuts),FadeOut(syn),run_time=.4)
        self.play(FadeIn(label('drug block',0,-3,30,RED)),run_time=.25)
        self.finish()


class S03Logic2(SpokenScene):
    def construct(self):
        rc,bp,gc,links,cuts=relay()
        self.add(rc,bp,gc,VGroup(*[DashedVMobject(a.set_color(GREY)) for a in links]),cuts,dim_static(clouds(),.65),label('drug block',0,-3.1,30,RED))
        self.at('If a ganglion cell')
        self.play(GrowArrow(light_arrow(3.65,3.35,2.45)),run_time=.4)
        self.at('still responds')
        self.play(gc[0].animate.set_fill(GREEN,.4),run_time=.4)
        self.at('block is verified')
        self.play(FadeIn(label('verified',0,3.1,30,RED)),run_time=.4)
        self.at('most likely its own')
        self.play(FadeOut(self.mobjects[6]),FadeIn(label('Still responds → most likely its own response',0,-3.1,28,GREEN)),run_time=.45)
        self.finish()


class S04Who(SpokenScene):
    def construct(self):
        self.add(dish(),label('Isolated, flat-mounted adult rat retina',0,-3.15,28,GREEN))
        self.at('In')
        self.play(FadeIn(label('Berson, Dunn and Takao • 2002',0,3.15,32)),run_time=.5)
        self.at('did this')
        self.finish()


class S05Label(SpokenScene):
    def construct(self):
        d=dish().scale(.9).shift(LEFT*1.15)
        scn=chip('clock\n(SCN)',PURPLE,size=30).move_to([4.9,0,0])
        self.add(d,scn)
        self.at('First')
        dye=Dot([4.1,0,0],radius=.14,color=YELLOW)
        self.play(FadeIn(dye),run_time=.3)
        self.at('from the')
        for i in [2,3,4]:
            end=d[2][i].get_center(); path=Line([4.1,0,0],end,color=GREEN,stroke_width=3)
            self.play(Create(path),MoveAlongPath(dye,Line([4.1,0,0],end)),run_time=.35,rate_func=linear)
            self.play(d[2][i].animate.set_color(GREEN).set_fill(GREEN,.7),run_time=.12)
            dye.move_to([4.1,0,0])
        self.remove(dye)
        self.at('That told them')
        self.play(FadeIn(label('labelled cells project to the clock',0,-3.15,30)),run_time=.45)
        self.finish()


class S06Record(SpokenScene):
    def construct(self):
        d=dish()
        for i in [2,3,4]: d[2][i].set_color(GREEN).set_fill(GREEN,.7)
        self.add(d,label('labelled cell',-.7,.2,26,GREEN),Line([0,.45,0],[.2,.7,0],color=GREEN))
        self.at('Then they recorded')
        self.play(Create(pipette()),run_time=.6)
        self.at('while the blockers')
        # Flow covers the full dish width below all cell bodies.
        self.play(GrowArrow(arr([-5.7,-1.95,0],[5.7,-1.95,0],RED,w=8)),FadeIn(label('blocking drugs in the bath',0,-3.15,30)),run_time=.6)
        self.finish()


class S07Predict(SpokenScene):
    def construct(self):
        p=prediction(); self.add(*p[1:5],p[6])
        self.at('Predict')
        prompt=label('Predict',0,3.15,34,YELLOW); self.play(FadeIn(prompt),run_time=.35)
        self.at('Suppose the rod')
        self.play(FadeOut(prompt),FadeIn(p[0]),run_time=.4)
        self.at('What should the recording')
        self.play(FadeIn(p[5]),run_time=.4)
        self.finish()


class S08Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(prediction()); self.wait(5)


class S09Reveal(SpokenScene):
    def construct(self):
        p=prediction(); self.add(p)
        expected=label('predicted: relay only',3.1,-.65,28,GREY)
        heading=label('No light-evoked change?',0,3.15,32)
        flat=DashedLine([X0,-1.15,0],[5.5,-1.15,0],color=GREY,stroke_width=4)
        self.at('There should be')
        self.play(FadeOut(p[0]),FadeOut(p[5]),FadeIn(heading),Create(flat),FadeIn(expected),run_time=.6)
        self.at('But one remained')
        self.play(FadeOut(heading),Create(trace(-1.15,amp=3.65,x0=X0,width=WIDTH,noise=True)),FadeIn(label('Observed: a light response remains',0,3.15,32,GREEN)),run_time=1.35,rate_func=linear)
        self.at('still depolarized to light')
        self.play(FadeIn(label('Still depolarizes with synapses blocked',0,-3.2,28,GREEN)),run_time=.45)
        self.add(label('Schematic response',3.5,2.4,26))
        self.finish()


class S10Intrinsic(SpokenScene):
    def construct(self):
        gc=neuron(0,0,8.5,5.3); self.add(gc)
        self.at('So the response')
        self.play(GrowArrow(light_arrow(0,3.4,2.7)),run_time=.4)
        self.at('was intrinsic')
        self.play(gc[0].animate.set_fill(GREEN,.4),FadeIn(label('intrinsic',0,-3.15,38,GREEN)),run_time=.5)
        self.at('made within')
        self.play(FadeOut(gc[1]),FadeIn(label('made within the ganglion cell',0,0,30,TEXT)),run_time=.4)
        self.finish()


class S11Isolated(SpokenScene):
    def construct(self):
        d=dish(); c=cell(.4,1,.9,.7,GREEN,fill=.5); self.add(d,c)
        self.at('They also recorded')
        self.at('cell body removed')
        self.play(c.animate.shift(UP*.8),run_time=.35)
        self.play(FadeOut(d),c.animate.move_to([-.5,0,0]).stretch_to_fit_width(6).stretch_to_fit_height(4.8),run_time=.7)
        self.play(Create(pipette((1.5,1,0))),GrowArrow(light_arrow(-.5,3.3,2.5)),run_time=.4)
        self.at('a stronger test')
        self.play(FadeIn(label('stronger test: isolated cell body',0,-3.15,30,GREEN)),c.animate.set_fill(GREEN,.7),run_time=.4)
        self.at('no synapses left')
        stub=VGroup(Line([-4.7,0,0],[-3.65,0,0],color=BLUE),cross([-4.2,0,0],.3))
        self.play(Create(stub),FadeIn(label('no synapses\nattached',-4.55,-1.2,26)),run_time=.4)
        self.finish()


class S12Two(SpokenScene):
    def construct(self):
        c=neuron(0,0,8,5.2); self.add(c)
        self.at('So one cell'); self.play(Indicate(c[0],color=GREEN),run_time=.4)
        self.at('two kinds'); q=label('two kinds of light response',0,-3.15,32); self.play(FadeIn(q),run_time=.4)
        self.at('Put both on'); self.play(FadeOut(c),FadeOut(q),FadeIn(comparison()),run_time=.6)
        self.finish()


class S13Relay(SpokenScene):
    def construct(self):
        self.add(comparison())
        self.at('The relayed response'); self.play(Create(wave(TOP,False,end=1)),run_time=.3)
        self.at('usually starts fast'); self.play(Create(wave(TOP,False,start=1,end=2.8)),run_time=.6)
        self.at('works in dim light'); self.play(FadeIn(lamp(1.15,3.18)),FadeIn(label('dim light',3.25,3.18,26,BLUE)),run_time=.4)
        self.at('It can have both'); self.play(Create(wave(TOP,False,start=2.8)),run_time=.7)
        self.play(FadeIn(label('brief + lasting',3.4,2.35,26,BLUE)),run_time=.3)
        self.finish()


class S14Own(SpokenScene):
    def construct(self):
        self.add(comparison(),wave(TOP,False),lamp(1.15,3.18),label('dim light',3.25,3.18,26,BLUE))
        self.at("The cell's own response"); self.play(Create(wave(BOTTOM,end=1)),run_time=.3)
        self.at('usually slow to start'); self.play(Create(wave(BOTTOM,start=1,end=4.8)),run_time=.8)
        self.at('needs brighter light'); self.play(FadeIn(lamp(1.15,.3,True).scale(.65)),FadeIn(label('brighter light',3.5,.25,26,GREEN)),run_time=.4)
        self.at('It is often'); self.play(Create(wave(BOTTOM,start=4.8,end=6)),run_time=.5)
        self.at('though it adapts too'); self.play(FadeIn(label('sustained; also adapts',2.4,-1.15,26,GREEN)),run_time=.3)
        self.finish()


class S15Off(SpokenScene):
    def construct(self):
        c=comparison(); self.add(c,wave(TOP,False),wave(BOTTOM,end=6))
        self.at('When the light goes off'); self.play(Indicate(c[2][3],color=YELLOW),run_time=.4)
        self.at('it decays slowly'); self.play(Create(wave(BOTTOM,start=6)),run_time=.9)
        self.at('The cell stays depolarized')
        t=7.5; x=X0+WIDTH*t/9; y=BOTTOM+AMP*value(t)
        bracket=DoubleArrow([x,BOTTOM,0],[x,y,0],buff=0,color=GREEN,tip_length=.12)
        self.play(Create(bracket),FadeIn(label('still above\nbaseline',5,-.75,26,GREEN)),FadeIn(label('back to 0',4.3,1.2,26,BLUE)),run_time=.45)
        self.finish()


class S16Pipr(SpokenScene):
    def construct(self):
        eye=eye_icon(0,.1,8.7); wide=label('wide pupil',0,-3.15,30); self.add(eye,wide)
        beam=arr([-4.8,2.5,0],[-.2,.2,0],YELLOW,w=7)
        self.at('these cells drive')
        on=label('light on',-4.4,3.05,28,YELLOW)
        self.play(GrowArrow(beam),FadeIn(on),run_time=.35)
        self.play(eye.pup.animate.scale(.36),FadeOut(wide),run_time=.9)
        self.at('pupil response')
        self.play(FadeIn(label('Post-illumination pupil response',0,3.5,30)),run_time=.35)
        self.at('The pupil stays small')
        still=label('still small, seconds later',0,-3.15,30,YELLOW)
        self.play(FadeOut(beam),FadeOut(on),FadeIn(label('light off',-4.7,2.7,28)),FadeIn(still),run_time=.35)
        clock=clock_icon(5.5,0,.65); self.play(Create(clock),run_time=.25)
        self.at('after light goes off')
        self.play(Rotate(clock.h2,angle=-TAU,about_point=clock.c),run_time=3.4,rate_func=linear)
        self.play(FadeOut(still),run_time=.15)
        self.add(label('slow recovery',0,-3.15,30))
        self.play(eye.pup.animate.scale(1/.36),run_time=2.1,rate_func=smooth)
        self.finish()


class S17Why(SpokenScene):
    def construct(self):
        self.add(wave(-1.8,amp=2.4),Line([X0,-1.8,0],[5.5,-1.8,0],color=GREY),lightbar(-2.55),label('response',-5.3,-.2,26).rotate(PI/2))
        plateau=wave(-1.8,start=3.8,end=6,amp=2.4)
        self.at('Why would slow'); self.play(Indicate(plateau,color=YELLOW,scale_factor=1),run_time=.6)
        self.at('The clock and the pupil')
        self.play(Create(clock_icon(-3.2,2.1,1)),FadeIn(eye_icon(3.2,2.1,3.6)),GrowArrow(arr([.4,.5,0],[-2.3,1.4,0],YELLOW)),GrowArrow(arr([.8,.5,0],[2.3,1.1,0],YELLOW)),run_time=.6)
        self.at('how bright it is'); self.play(FadeIn(label('steady level = how bright',.5,-1.25,30,YELLOW)),run_time=.4)
        self.finish()


class S18Meter(SpokenScene):
    def construct(self):
        camera=VGroup(
            RoundedRectangle(width=2.1,height=3.7,corner_radius=.2,color=GREY),
            Circle(radius=.73,color=GREY)).move_to([-5.1,0,0])
        lens=Polygon([-4.05,-.65,0],[-3.45,-1,0],[-3.45,1,0],[-4.05,.65,0],color=GREY)
        stage=Rectangle(width=2.2,height=4.4,color=GREY).move_to([-1.8,0,0])
        view=VGroup(*[DashedLine([-3.45,0,0],[-2.9,y,0],color=GREY,stroke_opacity=.65) for y in [-2.2,2.2]])
        obj=Line([-2.45,-1.4,0],[-2.45,1.4,0],color=TEXT,stroke_width=9)
        box=Rectangle(width=.55,height=3.2,color=YELLOW).move_to([-2.45,0,0])
        self.add(camera,lens,view,stage,obj,box,label('camera tracks changes',-3.4,3.15,27))
        self.at('A camera must follow'); self.play(obj.animate.shift(RIGHT*1.25),box.animate.shift(RIGHT*1.25),run_time=1.3,rate_func=linear)
        self.at('A light meter'); m=meter(); self.play(FadeIn(m),FadeIn(label('light meter',2.9,3.15,30,GREEN)),run_time=.4)
        self.at('a steady reading')
        # The scene flickers in the camera's field while the meter needle holds.
        pulse=Rectangle(width=2.1,height=4.3,fill_color=YELLOW,fill_opacity=.38,stroke_width=0).move_to([-1.8,0,0])
        self.add(pulse); self.bring_to_front(obj,box)
        self.play(FadeOut(pulse),FadeIn(label('steady reading',2.9,-3.15,28,YELLOW)),run_time=.8)
        self.finish()


class S19M1(SpokenScene):
    def construct(self):
        self.add(meter(0),label('light meter',0,3.15,32,GREEN))
        self.at('The cells that serve'); self.play(Create(clock_icon(-4.5,.7,1.1)),FadeIn(eye_icon(4.5,.7,3.3)),run_time=.5)
        self.at('are mostly a type')
        self.play(FadeIn(cell(-4.5,-1.8,1.5,1.4,GREEN,.4)),FadeIn(label('mostly M1 cells',0,-2.85,30,GREEN)),run_time=.4)
        self.at('They report how bright'); reading=label('how bright the world is',0,-3.5,28,YELLOW); self.play(FadeIn(reading),run_time=.3)
        self.at('not what is in it'); self.play(FadeOut(reading),FadeIn(label('how bright, not what is in it',0,-3.5,28,YELLOW)),run_time=.25)
        self.wait(1.5); self.finish()


class S20Spectrum(SpokenScene):
    def construct(self):
        axes=Axes(x_range=[380,650,50],y_range=[0,1.05,.5],x_length=9.8,y_length=4.5,tips=False,axis_config={'color':GREY,'include_ticks':False}).move_to([.35,.15,0])
        self.add(axes,label('Rat ganglion cells',0,3.3,32),label('relative sensitivity',-5.9,.2,26).rotate(PI/2),label('wavelength (nm)',0,-3.1,28))
        for w in [400,500,600]: self.add(label(str(w),axes.c2p(w,0)[0],-2.5,26))
        for v in [0,.5,1]:
            pos=axes.c2p(380,v); self.add(label(str(v),pos[0]-.4,pos[1],26),Line(pos+LEFT*.1,pos+RIGHT*.1,color=GREY))
        self.add(label('Illustrative pigment curve, peak 484 nm',0,2.8,26,GREEN),label('Not the measured points',2.9,1.95,26))
        self.at('The rat response'); self.play(Create(axes.plot(lambda w:float(spectrum(w)),x_range=[380,650],color=GREEN,stroke_width=5,use_smoothing=False)),run_time=1.2)
        self.at('that peaks near'); point=axes.c2p(484,float(spectrum(484)))
        # A vertical marker cannot cross the curve or the explanatory labels.
        self.play(FadeIn(Dot(point,color=YELLOW)),Create(DashedLine(point,axes.c2p(484,0),color=YELLOW,stroke_width=3)),run_time=.3)
        self.add(label('≈484 nm',point[0],point[1]+.32,28,YELLOW))
        self.at('That is a rat estimate'); self.play(FadeIn(label('rat estimate',3.3,.5,30)),run_time=.3)
        self.at('not a human one'); self.play(FadeIn(label('not a human estimate',3.4,0,28,YELLOW)),run_time=.3)
        self.finish()


class S21Hattar(SpokenScene):
    def construct(self):
        target=cell(-1.1,0,6,5,GREEN,.15)
        neighbours=VGroup(cell(4.1,1.2,2.1,2,GREY,.12),cell(4.1,-1.3,2.1,2,GREY,.12))
        self.add(target,neighbours,label('labelled rat cell',-1.1,0,30,TEXT),label('unstained\nneighbours',4.1,-2.8,26))
        self.at('In the same volume'); self.play(FadeIn(label('Hattar and colleagues • 2002',0,3.2,32)),run_time=.4)
        self.at('showed that these rat cells'); self.play(target.animate.set_fill(GREEN,.65),run_time=.7)
        self.at('carried melanopsin')
        halo=Ellipse(width=6.3,height=5.3,color=GREEN,stroke_width=9).move_to([-1.1,0,0])
        self.play(Create(halo),FadeIn(label('melanopsin stain',-1.1,-3.2,30,GREEN)),run_time=.5)
        self.finish()


class S22Hattar2(SpokenScene):
    def construct(self):
        retina=cell(-4,0,3.5,5.5,GREEN,.12)
        cells=VGroup(*[cell(-4.1,y,.6,.55,GREEN,.5) for y in [-1.4,0,1.4]])
        scn=chip('clock\nSCN',PURPLE,size=38,pad=.5).move_to([4.8,0,0])
        self.add(retina,cells,scn,label('mouse retina',-4,-3.2,28,GREEN))
        self.at('and melanopsin')
        self.at('mouse axons')
        axons=VGroup(*[VMobject(color=GREEN,stroke_width=4).set_points_as_corners([c.get_right(),[-1.8,c.get_y(),0],[-1.2,0,0]]) for c in cells.submobjects])
        self.play(Create(axons,lag_ratio=0),GrowArrow(arr([-1.2,0,0],[3.65,0,0],GREEN,w=8)),FadeIn(label('melanopsin-marked axons',1.1,.4,28,GREEN)),run_time=.65)
        self.at('the SCN'); self.play(Indicate(scn,color=PURPLE),run_time=.4)
        self.finish()


class S23Take(SpokenScene):
    def construct(self):
        amp=2.9 / OWN_Y.max()
        self.add(wave(-1.6,amp=amp),Line([X0,-1.6,0],[5.5,-1.6,0],color=GREY),lightbar(-2.7),label('response',-5.5,.1,26).rotate(PI/2))
        self.at('A response')
        thumb=trace(0,amp=.95,x0=-5.3,width=2.8).shift(UP*2.35)
        self.play(Create(thumb),FadeIn(label('response',-3.9,3.55,28)),run_time=.25)
        self.at('a pigment')
        ws=np.linspace(380,650,100); pts=[[-1.4+2.8*(w-380)/270,2.35+.95*float(spectrum(w)),0] for w in ws]
        self.play(Create(VMobject(color=GREEN,stroke_width=5).set_points_as_corners(pts)),FadeIn(label('pigment',0,3.55,28)),run_time=.25)
        self.at('and a target'); self.play(FadeIn(chip('SCN',PURPLE,size=38,pad=.35).move_to([4.1,2.8,0])),FadeIn(label('target',4.1,3.55,28)),run_time=.25)
        self.at('one set of cells'); self.play(FadeIn(label('one set of cells',0,1.85,28)),run_time=.3)
        self.at('Their signature is slow')
        rise=wave(-1.6,start=1,end=3.8,amp=amp)
        slow=Brace(rise,direction=LEFT,buff=.12,color=GREEN)
        self.play(Create(slow),FadeIn(label('slow',-4.65,.15,30,GREEN)),run_time=.3)
        self.at('insensitive'); self.play(FadeIn(lamp(-2.4,-2.05,True)),FadeIn(label('insensitive: needs brighter light',1.1,-2.05,26,GREEN)),run_time=.3)
        self.at('and sustained')
        plateau=wave(-1.6,start=3.8,end=6,amp=amp).set_color(YELLOW).set_stroke(width=9)
        # Highlight the computed plateau itself; short end ticks anchor the bracket.
        ticks=VGroup(*[Line(plateau.point_from_proportion(p)+DOWN*.1,plateau.point_from_proportion(p)+UP*.1,color=YELLOW,stroke_width=4) for p in [0,1]])
        self.play(Create(plateau),Create(ticks),FadeIn(label('sustained',3.9,1.3,28,GREEN)),run_time=.3)
        self.wait(2); self.finish()


class S24End(EndCard):
    LINE='Their signature is slow, insensitive and sustained.'
