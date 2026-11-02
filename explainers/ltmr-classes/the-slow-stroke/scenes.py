"""Your Own Skin: The Slow Stroke — timed to the supplied Kokoro recording.

COLOR MAP (from ../scenes.old.py; CHAPTERS.md is kept read-only per TASK):
 BLUE = Aβ RA / fast myelinated comparison; YELLOW = Aδ / hair bend;
 ORANGE = mouse C-LTMR / human CT; TEAL = Aβ SA1 / steady press;
 PURPLE = terminal Schwann cells; GREEN = field-LTMR;
 RED = a rejected inference; GREY = skin, hair, PC, axes and neutral labels;
 GOLD = the rule to keep. Pleasantness is white, distinct from any neuron.

Plots: computed normalized regression SHAPES, never fabricated measured rates.
Löken et al. 2009, doi:10.1038/nn.2312, reports negative quadratic fits
with velocity peaks 2.1 cm/s (CT) and 2.8 cm/s (ratings), and monotonically
increasing Aβ firing. With x=log10(v), a quadratic's normalized shape is
1 - ((x-x_peak)/max_distance)**2. Aβ is a normalized increasing linear
comparison. The unknown amplitude/intercept are intentionally not displayed;
these are not digitizations or fitted coefficients from the experiment.
Spike monitors are computed from a leaky integrate-and-fire model, not real data.
"""
import importlib.util
from pathlib import Path
import numpy as np
from bp_style import *

# Reuse the pilot's anatomy and plotting helpers without changing its source.
_spec = importlib.util.spec_from_file_location('ltmr_pilot', Path(__file__).resolve().parent.parent / 'scenes.old.py')
_pilot = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_pilot)
ORANGE, PURPLE = _pilot.ORANGE, _pilot.PURPLE
trace, follicle, place, finger = _pilot.trace, _pilot.follicle, _pilot.place, _pilot.finger


def label(s, y=3.1, color=TEXT, size=32):
    return T(s, size=size, color=color).move_to([0, y, 0])


def arm(hairy=False):
    outline = RoundedRectangle(width=9.2, height=3.3, corner_radius=.7,
        color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=.08).move_to([-.9,-.3,0])
    palm = RoundedRectangle(width=1.5,height=2.7,corner_radius=.4,color=GREY,
        fill_color=BG,fill_opacity=1).move_to([4.0,-.3,0])
    fingers = VGroup(*[Line([4.5,y,0],[5.9+dx,y,0],color=GREY,stroke_width=8)
        for y,dx in ((.7,-.2),(.1,0),(-.5,-.1),(-1.1,-.4))])
    thumb = Line([3.7,.7,0],[4.4,1.6,0],color=GREY,stroke_width=9)
    hairs = VGroup(*[Line([x,1.35,0],[x+.15,1.7,0],color=GREY,stroke_width=3)
        for x in np.linspace(-4.5,2.6,8)]) if hairy else VGroup()
    return VGroup(outline,palm,fingers,thumb,hairs)

def brush(x=-3.4, y=2.1):
    block = RoundedRectangle(width=1.5, height=.4, corner_radius=.1, color=TEXT,
                             fill_color=TEXT, fill_opacity=.15)
    handle = Line([0, .2, 0], [0, .65, 0], color=TEXT, stroke_width=8)
    bristles = VGroup(*[Line([x, -.2, 0], [x + .07, -.75, 0], color=TEXT, stroke_width=2)
                        for x in np.linspace(-.65, .65, 10)])
    return VGroup(block, handle, bristles).shift([x, y, 0])


def spikes(x,y,width,color):
    # Leaky integrate-and-fire response to constant gentle input, arbitrary units.
    dt=.002; potential=0.; times=[]
    for t in np.arange(0,1,dt):
        potential += dt*(1.8-potential)/.07
        if potential >= 1:
            times.append(t); potential=0.
    points=[[x,y,0]]
    for t in times:
        z=x+t*width
        points.extend([[z-.025,y,0],[z,y+.48,0],[z+.035,y-.08,0],[z+.07,y,0]])
    points.append([x+width,y,0])
    return VMobject(color=color,stroke_width=3).set_points_as_corners(points)


def nerve():
    return Line([-4.6, -.25, 0], [3.7, -.25, 0], color=ORANGE, stroke_width=5)


def electrode(inserted=False):
    e = Line([-.2, 3.0, 0], [1.2, 1.25, 0], color=TEXT, stroke_width=3)
    if inserted:
        e.shift(DOWN * 1.5)
    return e


def question_frame():
    q = label('Which speed drives a CT afferent hardest?', 3.15, size=32)
    a = arm(hairy=True)
    b = brush(-3.4, 2.1)
    axis = Arrow([-5.4,-2.45,0],[5.4,-2.45,0],color=GREY,buff=0)
    ticks = VGroup()
    for v in (.1,.3,1,3,10,30):
        x = -5.4+10.8*(np.log10(v)+1)/(np.log10(30)+1)
        ticks.add(Line([x,-2.35,0],[x,-2.55,0],color=GREY),M(str(v),26,GREY).move_to([x,-2.9,0]))
    ticks.add(label('Brush speed (cm/s, log scale)',-3.4,GREY,26))
    return q,a,b,axis,ticks




LO, HI = np.log10(.1), np.log10(30)
def tuning(v, peak):
    xp = np.log10(peak)
    return 1 - ((np.log10(v) - xp) / max(xp - LO, HI - xp)) ** 2


def plot_base():
    ax = Axes(x_range=[LO,HI,1],y_range=[0,1.15,.5],x_length=10.1,
        y_length=4.2,tips=False,axis_config={'color':GREY,'include_ticks':False})
    ax.move_to([.55,.35,0])
    ax.y_axis.set_opacity(0)
    left_axis=Line(ax.c2p(LO,0),ax.c2p(LO,1.15),color=GREY,stroke_width=2)
    ticks = VGroup()
    for v in (.1,1,10,30):
        pos=ax.c2p(np.log10(v),0)
        ticks.add(Line(pos+UP*.07,pos+DOWN*.07,color=GREY),M(str(v),26,GREY).move_to(pos+DOWN*.35))
    for v in (0,.5,1):
        ticks.add(M(str(v),26,GREY).next_to(ax.c2p(LO,v),LEFT,buff=.18))
    ylabel=T('Firing rate (normalised)',26,GREY).rotate(PI/2).move_to([-6.1,.1,0])
    footer=label('Brush speed (cm/s, log scale)',-2.7,GREY,26)
    shape=label('Normalised fit shapes • separate scales',-3.12,TEXT,30)
    return ax,VGroup(ax,left_axis,ticks,ylabel,footer,shape)

def curve(ax, peak, color, start=LO, end=HI):
    return ax.plot(lambda x: tuning(10**x, peak), x_range=[start, end, .015],
                   color=color, stroke_width=5, use_smoothing=False)


def band(ax):
    x1, x2 = ax.c2p(0, 0), ax.c2p(1, 0)
    return Rectangle(width=x2[0]-x1[0], height=4.2, stroke_width=0,
                     fill_color=ORANGE, fill_opacity=.09).move_to([(x1[0]+x2[0])/2, ax.c2p(0,.575)[1], 0]).set_z_index(-1)


class S00Title(TitleCard):
    LESSON = 'The Low-Threshold Mechanoreceptors: One Touch, Several Signals'
    TITLE = 'Your Own Skin: The Slow Stroke'

    def construct(self):
        brand = label('BIOCHEMISTRYPEDIA', 2.4, TEAL, 22)
        lesson = T('The Low-Threshold Mechanoreceptors:\nOne Touch, Several Signals', 24, GREY,
                   line_spacing=1.2).move_to([0, 1.15, 0])
        title = T(self.TITLE, 44, font=TITLE_FONT).move_to([0, -.35, 0])
        rule = Line([-1.3, -1.35, 0], [1.3, -1.35, 0], color=GOLD, stroke_width=4)
        self.add(brand, lesson)
        self.play(FadeIn(title), GrowFromCenter(rule), run_time=.8)
        self.finish()


class S01Question(SpokenScene):
    def construct(self):
        a, b = arm(), brush()
        self.add(a)
        self.at('A soft brush')
        self.play(FadeIn(b), run_time=.45)
        self.at('strokes your forearm')
        self.play(b.animate.shift(RIGHT * 4.6), run_time=1.2, rate_func=linear)
        self.at('Does some')
        self.play(FadeIn(label('Does speed matter?', -2.7, size=38)), run_time=.5)
        self.finish()


class S02Method(SpokenScene):
    def construct(self):
        n = nerve().set_color(GREY)
        self.add(arm(), n, T('nerve', 30, GREY).move_to([-3.7, -.85, 0]))
        genetics = chip('mouse genetics', GREY, 30).move_to([0, 2.45, 0])
        self.at('Mouse genetics')
        self.play(FadeIn(genetics), run_time=.5)
        self.at('cannot be done')
        cross = Cross(genetics, stroke_color=RED, stroke_width=5)
        self.play(Create(cross), run_time=.4)
        self.at('So human touch')
        method = label('microneurography', 2.9, size=40)
        self.play(FadeOut(genetics), FadeOut(cross), FadeIn(method), run_time=.5)
        self.at('microneurography')
        e = Line([-.9, 1.7, 0], [1.1, -.25, 0], color=TEXT, stroke_width=5)
        contact = Dot([1.1, -.25, 0], radius=.10, color=TEXT)
        self.play(Create(e), FadeIn(contact), Indicate(method, color=TEXT), run_time=.6)
        self.finish()


class S03Electrode(SpokenScene):
    def construct(self):
        a=arm().stretch_to_fit_height(2.5).shift(UP*.5)
        n=nerve().shift(UP*.5)
        e=Line([-1.5,2.8,0],[.3,1.5,0],color=TEXT,stroke_width=4)
        self.add(a)
        self.at('A fine tungsten')
        self.play(Create(e),FadeIn(label('Tungsten electrode',3.25,size=30)),run_time=.5)
        self.at('goes through the skin')
        self.play(e.animate.shift(DOWN*1.25),Create(n),run_time=1)
        monitor=RoundedRectangle(width=10.4,height=1.9,corner_radius=.15,color=GREY).move_to([0,-2.35,0])
        wave=spikes(-4.7,-2.85,9.4,ORANGE)
        wire=VMobject(color=GREY).set_points_as_corners([[-1.5,1.55,0],[-5.7,1.55,0],[-5.7,-2,0],[-5.2,-2,0]])
        self.at('in a conscious')
        self.play(FadeIn(T('Conscious volunteer',28,GREY).move_to([3,2.25,0])),
            Create(monitor),Create(wire),FadeIn(T('one afferent • model trace',28,ORANGE).move_to([0,-1.85,0])),run_time=.4)
        self.play(Create(wave),run_time=.7,rate_func=linear)
        self.at('It records')
        self.play(Indicate(wave,color=TEXT),run_time=.3)
        self.play(wave.animate.shift(LEFT*.25),run_time=.8,rate_func=linear)
        self.finish()

class S04Classes(SpokenScene):
    def construct(self):
        a = arm().move_to([0, .5, 0])
        # These are identical model examples, not invented class-specific recordings.
        waves = VGroup(*[spikes(x, .15, 1.7, c).stretch(1.6, 1)
            for x, c in zip((-4.6, -2.5, -.4, 1.7), (BLUE, GREY, TEAL, GREY))])
        self.add(a, waves, T('Model firing traces', 28, GREY).move_to([-.4, 1.3, 0]))
        self.at('Recordings from the hand')
        self.play(FadeIn(label('Human hand • classes by firing', 3.05, size=32)), run_time=.6)
        cards = VGroup(*[chip(t, c, 32) for t, c in [('RA', BLUE), ('PC', GREY), ('SA I', TEAL), ('SA II', GREY)]]).arrange(RIGHT, buff=.65).move_to([0, -1.7, 0])
        for card, wave in zip(cards, waves):
            card.set_x(wave.get_center()[0])
        self.at('sorted human afferents')
        self.play(LaggedStart(*[FadeIn(c, shift=UP*.15) for c in cards], lag_ratio=.16), run_time=.8)
        self.at('by firing')
        self.play(FadeIn(label('Johansson and Vallbo, 1979', -3.35, GREY, 26)), run_time=.4)
        self.at('The ending')
        unknown = VGroup(T('?', 58, GREY), T('ending never seen', 28, GREY)).arrange(RIGHT, buff=.3).move_to([0, -2.6, 0])
        self.play(FadeIn(unknown), run_time=.6)
        self.finish()


class S05Ct(SpokenScene):
    def construct(self):
        a, n, b = arm(hairy=True), nerve(), brush()
        self.add(a, b)
        self.at('Hairy skin adds')
        self.play(FadeIn(label('Human hairy skin', 3.1)), run_time=.5)
        self.at('another class')
        self.play(Create(n), run_time=.7)
        self.at('unmyelinated afferents')
        self.play(FadeIn(label('slow • unmyelinated', -2.18, ORANGE, 30)), FadeIn(label('Vallbo and colleagues, 1999', -3.35, TEXT, 34)), run_time=.4)
        self.at('respond to gentle')
        burst = spikes(-4.4, -.25, 7.7, ORANGE).stretch(1.8, 1, about_point=[0, -.25, 0])
        self.play(b.animate.shift(RIGHT * 4.5), Create(burst),
            ShowPassingFlash(n.copy().set_stroke(TEXT, 8), time_width=.4),
            run_time=1.4, rate_func=linear)
        self.add(T('Model spike response', 28, ORANGE).move_to([-.6, -1.15, 0]))
        self.finish()


class S06Ct2(SpokenScene):
    def construct(self):
        def panel(x,name):
            box=RoundedRectangle(width=5.2,height=3.7,corner_radius=.3,color=GREY).move_to([x,.2,0])
            skin=Line([x-2,1.1,0],[x+2,1.1,0],color=GREY,stroke_width=4)
            tool=brush(x-1,1.85).scale(.7)
            wave=spikes(x-2,-.8,4,ORANGE)
            title=T(name,30,ORANGE).move_to([x,-2.2,0])
            return VGroup(box,skin,tool,wave,title)
        human=panel(-3.1,'Human CT afferent'); mouse=panel(3.1,'Mouse C-LTMR')
        self.add(human,mouse[:3])
        self.at('These are the')
        self.play(human[2].animate.shift(RIGHT*1.2),run_time=.7)
        self.at('physiologically similar')
        self.play(Create(mouse[3]),FadeIn(mouse[4]),FadeIn(label('Similar physiology',3.15,size=36)),run_time=.5)
        self.play(mouse[2].animate.shift(RIGHT*1.2),Indicate(human[3],color=TEXT),run_time=.7)
        self.add(label('Matching model responses • schematic',-3.15,GREY,26))
        self.finish()

class S07Predict(SpokenScene):
    def construct(self):
        q, a, b, axis, ends = question_frame()
        self.add(a)
        self.at('The brush strokes')
        self.play(FadeIn(b), Create(axis), FadeIn(ends), run_time=.5)
        self.at('from very slow')
        self.play(b.animate.shift(RIGHT * 1.3), run_time=.65, rate_func=linear)
        self.at('to fast')
        self.play(b.animate.shift(RIGHT * 4.5), run_time=.45, rate_func=linear)
        self.at('which speed')
        self.play(FadeIn(q), run_time=.5)
        # Restore the exact pause composition before holding the question.
        self.play(b.animate.move_to(question_frame()[2]), run_time=.45)
        self.finish()


class S08Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(*question_frame())
        wave = spikes(-4.7, -.2, 3.5, ORANGE).stretch(1.5, 1)
        self.add(wave, T('Model spikes', 28, ORANGE).move_to([-3, -.9, 0]))
        centre = np.array([1.2, -.25, 0])
        ring = Circle(radius=1.02, color=GREY, stroke_width=5).move_to(centre)
        remaining = ValueTracker(5)
        arc = always_redraw(lambda: Arc(radius=1.02, start_angle=PI/2,
            angle=TAU * max(.001, remaining.get_value()/5), color=GOLD,
            stroke_width=12).move_arc_center_to(centre))
        number = always_redraw(lambda: M(str(max(1, int(np.ceil(remaining.get_value())))),
            64, TEXT).move_to(centre))
        self.add(ring, arc, number)
        self.play(remaining.animate.set_value(0), run_time=5, rate_func=linear)

class S09Reveal(SpokenScene):
    def construct(self):
        ax,base=plot_base()
        fastest=chip('Not the fastest',TEXT,32).move_to([1.6,.2,0])
        title=label('CT firing',3.18,ORANGE,34)
        credit=T('Löken and colleagues, 2009',32,TEXT).move_to([1.3,-1.7,0])
        self.add(base,title,fastest)
        self.at('Not the fastest')
        self.play(Indicate(fastest,color=RED),run_time=.6)
        self.at('firing rises')
        self.play(FadeOut(fastest),Create(curve(ax,2.1,ORANGE)),run_time=1.6)
        self.at('It peaks')
        self.play(FadeIn(band(ax)),FadeIn(label('Peak about 1–10 cm/s',2.65,ORANGE,28)),run_time=.45)
        # Keep the source and model note below the plotting area on separate lines.
        credit.move_to([0,-3.57,0])
        self.play(FadeIn(credit),run_time=.3)
        self.finish()

class S10Pleasant(SpokenScene):
    def construct(self):
        ax,base=plot_base(); ct=curve(ax,2.1,ORANGE)
        title=label('CT firing',3.18,ORANGE,34)
        credit = T('Löken and colleagues, 2009', 32, TEXT).move_to([0, -3.57, 0])
        self.add(base,band(ax),ct,title,credit)
        # Ratings use their own normalised vertical scale; preserve quadratic shape.
        ratings=ax.plot(lambda x:.12+.64*tuning(10**x,2.8),x_range=[LO,HI,.015],color=TEXT,stroke_width=4,use_smoothing=False)
        pleasant=DashedVMobject(ratings,num_dashes=25)
        ratings_title = VGroup(T('CT firing', 34, ORANGE), T('/ Pleasantness', 34, TEXT)).arrange(RIGHT, buff=.25).move_to([0, 3.18, 0])
        tag=T('Pleasantness rating',28,TEXT).move_to([2.6,-.3,0])
        leader=Line(tag.get_left()+LEFT*.1,ax.c2p(np.log10(1),.12+.64*tuning(1,2.8)),color=TEXT,stroke_width=2)
        self.at('Pleasantness ratings')
        self.play(Create(pleasant),FadeIn(tag),Create(leader),Transform(title, ratings_title),run_time=.8)
        self.at('Fast myelinated')
        blue_title=VGroup(T('CT firing',34,ORANGE), T('/ Aβ firing',34,BLUE)).arrange(RIGHT,buff=.25).move_to([0,3.18,0])
        self.play(FadeOut(pleasant),FadeOut(tag),FadeOut(leader),Transform(title,blue_title),run_time=.4)
        ab=ax.plot(lambda x:.08+.92*(x-LO)/(HI-LO),x_range=[LO,HI,.015],color=BLUE,stroke_width=5,use_smoothing=False)
        self.at('Their firing')
        self.play(Create(ab),run_time=.9)
        self.finish()

def social_picture():
    a = arm(hairy=True)
    # Side-on hand: wrist, palm, thumb and joined finger pad touch the skin.
    # Lower contour is at y=1.35, exactly the forearm's upper surface.
    outline = VMobject(color=TEXT, stroke_width=4, fill_color=BG, fill_opacity=1)
    outline.set_points_as_corners([
        [-4.6, 2.75, 0], [-3.7, 2.75, 0], [-3.25, 2.2, 0],
        [-2.5, 2.05, 0], [-1.4, 1.85, 0], [-1.05, 1.6, 0],
        [-1.25, 1.35, 0], [-3.1, 1.35, 0], [-3.75, 1.65, 0],
        [-4.6, 2.1, 0], [-4.6, 2.75, 0]])
    thumb = VMobject(color=TEXT, stroke_width=3).set_points_as_corners([
        [-3.4, 1.95, 0], [-2.8, 1.55, 0], [-2.15, 1.55, 0]])
    fingers = VGroup(*[Line([x, 1.4, 0], [x+.15, 1.72, 0], color=TEXT,
        stroke_width=2) for x in (-1.6, -1.95)])
    contact = Line([-3.0, 1.35, 0], [-1.3, 1.35, 0], color=ORANGE, stroke_width=6)
    return a, VGroup(outline, thumb, fingers, contact)



class S11Reviews(SpokenScene):
    def construct(self):
        a, hand = social_picture()
        self.add(a, hand)
        self.at('Reviews conclude')
        self.play(hand.animate.shift(RIGHT * 1.1), FadeIn(label('Reviews, 2023', -3.35, GREY, 28)), run_time=1.1, rate_func=linear)
        self.at('support gentle')
        self.play(hand.animate.shift(RIGHT * 2.1), run_time=1.0, rate_func=linear)
        self.at('the social side')
        self.play(FadeIn(label('Affective touch', -2.65, ORANGE, 40)), run_time=.5)
        self.finish()


class S12Limit(SpokenScene):
    def construct(self):
        a,hand=social_picture()
        VGroup(a, hand).scale(.65).shift(UP*.8)
        ct=chip('CT input',ORANGE,32).move_to([-3,-1.4,0])
        affect=chip('Affective touch',TEXT,32).move_to([2.4,-1.4,0])
        arrow=Arrow(ct.get_right(),affect.get_left(),color=GREY,buff=.15)
        first=label('Not every affective touch relies on CTs',-2.9,ORANGE,30)
        self.add(a,hand,ct,affect,arrow)
        self.at('But not every')
        self.play(ct.animate.set_opacity(.25),arrow.animate.set_opacity(.25),FadeIn(first),run_time=.7)
        self.at('need not be pleasant')
        face=Circle(radius=1.8,color=TEXT).move_to([0,.4,0])
        eyes=VGroup(Dot([-.45,.75,0],color=TEXT),Dot([.45,.75,0],color=TEXT))
        mouth=Line([-.5,-.1,0],[.5,-.1,0],color=TEXT,stroke_width=5)
        second=label('Affective touch need not be pleasant',-2.65,GOLD,32)
        # Cut between limits: no caption stacking or empty transition frame.
        self.remove(a,hand,ct,affect,arrow,first)
        self.add(face,eyes,mouth,second)
        self.finish()

class S13Unknown(SpokenScene):
    def construct(self):
        human=VGroup(Line([3.4,.8,0],[3.4,2.25,0],color=GREY,stroke_width=8),
            Line([1.9,.8,0],[5,.8,0],color=GREY,stroke_width=4),
            T('?',76,GREY).move_to([3.4,-.6,0]),T('Human hair',30,GREY).move_to([3.4,-2.7,0]))
        mouse=VGroup(place(follicle(1,'awl',tails=True),-4.5,-.15),T('Mouse hair map',30,GREY).move_to([-4.5,-2.7,0]))
        self.add(human,mouse)
        self.at('The human')
        self.play(Indicate(human[2],color=ORANGE),run_time=.6)
        self.at('The mouse')
        self.play(mouse.animate.shift(RIGHT*1.6),run_time=.65)
        self.at('cannot be transplanted')
        self.play(mouse.animate.shift(LEFT*.15),run_time=.2)
        self.play(FadeIn(label('Human CT ending: unknown',3.25,ORANGE,34)),run_time=.4)
        self.finish()

def touch_icon(kind, color):
    base = Line([-.65,-.6,0],[.65,-.6,0],color=GREY,stroke_width=3)
    if kind == 'press':
        action = VGroup(finger(0,.35).stretch_to_fit_height(1.1),
                        Arrow([0,1.5,0],[0,.95,0],buff=0,color=color))
    elif kind in ('motion','slow stroke'):
        action = VGroup(brush(0,.6).scale(.6), Arrow([-.7,1.6,0],[.7,1.6,0],buff=0,color=color))
    elif kind == 'vibration':
        action = VGroup(finger(0,.35).stretch_to_fit_height(1.1).stretch_to_fit_width(.5),
                        DoubleArrow([.65,-.2,0],[.65,1.0,0],buff=0,color=color,tip_length=.15))
    else:
        action = VGroup(Line([0,-.6,0],[.45,1.1,0],color=GREY,stroke_width=6),
                        Arrow([-.6,.9,0],[.15,.9,0],buff=0,color=color))
    return VGroup(base,action)


class S14Takeaway(SpokenScene):
    def construct(self):
        specs = [('press',TEAL),('motion',BLUE),('vibration',GREY),('bent hair',YELLOW),('slow stroke',ORANGE)]
        icons, paths, labs = VGroup(), VGroup(), VGroup()
        for x, (name,col) in zip(np.linspace(-5,5,5),specs):
            icons.add(touch_icon(name,col).scale(1.15).shift([x,.15,0]))
            labs.add(T(name,26,col).move_to([x,-1.0,0]))
            paths.add(Line([x,-1.5,0],[x,-2.3,0],color=col,stroke_width=12))
        self.add(icons,labs)
        self.at('So the idea')
        self.play(FadeIn(label('One touch',3.1,GOLD,38)),run_time=.5)
        self.at('Each class is')
        self.play(LaggedStart(*[Create(p) for p in paths],lag_ratio=.15), run_time=1.1)
        self.at('its own part')
        self.play(*[p.animate.set_opacity(.5) for p in paths],run_time=.5)
        self.at('The nervous system')
        self.play(*[p.animate.set_color(TEXT).set_opacity(1) for p in paths],run_time=.5)
        self.play(*[Indicate(p,color=TEXT,scale_factor=1.2) for p in paths],run_time=.5)
        self.finish()


class S15End(EndCard):
    LINE = 'The nervous system reads the pattern.'

    def construct(self):
        line=T(self.LINE,40,font=TITLE_FONT)
        fit(line,max_w=11.8)
        url=T('biochemistrypedia.com',32,TEAL).move_to([0,-1.1,0])
        self.play(FadeIn(line),run_time=.6)
        self.play(FadeIn(url),run_time=.4)
        self.finish()
