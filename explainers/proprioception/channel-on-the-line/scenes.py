"""The Channel on the Line — revision after the 21-item frame review.
COLOR MAP: YELLOW stretch/stimulus; BLUE spindle ending/nerve; PURPLE secondary
endings; GREEN Piezo2/current; ORANGE position estimate; RED deletion/deficit;
GREY structure/uncertainty. Abstract icons only, no molecular structures.
Current: exp(-t/5.6 ms). Ramp: clip((t-.5)/.5,0,1). Qualitative rasters
use explicitly generated event schedules, not purported experimental data.
"""
import numpy as np
from bp_style import *
PURPLE = '#B58CD9'
ORANGE = '#F29E4C'


def heading(s, color=TEXT):
    return T(s, 34, color, font=TITLE_FONT).move_to([0,3.12,0])


def label(s,x,y,color=TEXT,size=28):
    return T(s,size,color).move_to([x,y,0])


def arrow(a,b,color=GREY):
    return Arrow(a,b,buff=.13,color=color,stroke_width=5)


def channel(opened=False):
    # Three separated rounded blades terminate at a central abstract pore.
    blades=VGroup(*[RoundedRectangle(width=1.35,height=.45,corner_radius=.2,
        color=GREEN,fill_color=GREEN,fill_opacity=.3).shift(RIGHT*1.05)
        .rotate(a,about_point=ORIGIN) for a in (PI/2,7*PI/6,11*PI/6)])
    pore=Circle(radius=.32 if opened else .11,color=GREEN,fill_color=BG,
        fill_opacity=1,stroke_width=6)
    return VGroup(blades,pore,VectorizedPoint([0,-1.725,0]))


def membrane():
    # Gap keeps the pore visible and prevents blade / membrane intersections.
    return VGroup(*[Rectangle(width=3.7,height=.24,color=BLUE,fill_color=BLUE,
        fill_opacity=.4).move_to([x,-.1,0]) for x in (-3.65,3.65)])


def membrane_stage():
    return VGroup(membrane(),label('spindle sensory ending',0,-2.15,BLUE,32),
        label('membrane',4.2,.75,BLUE),Line([4.2,.45,0],[4.2,.05,0],color=BLUE))


def organ(x=0,y=0,tendon=False):
    shell=Ellipse(width=7.5,height=1.8,color=GREY,stroke_width=3,
        fill_color=GREY,fill_opacity=.07).move_to([x,y,0])
    fibers=VGroup(*[Line([x-3.4,y+d,0],[x+3.4,y+d,0],color=GREY,stroke_width=3)
        for d in (-.35,0,.35)])
    # Sensory terminal wraps the central intrafusal region, or branches among tendon strands.
    if not tendon:
        t=np.linspace(-1.25,1.25,260)
        wrap=VMobject(color=BLUE,stroke_width=6).set_points_as_corners(
            [[x+v,y+.68*np.sin(v*4*PI),0] for v in t])
    else:
        wrap=VGroup(*[VMobject(color=BLUE,stroke_width=5).set_points_as_corners(
            [[x-1.6,y+.75,0],[x-1,y+d,0],[x+.8,y+d,0],[x+1.5,y+d+.15,0]])
            for d in (-.48,0,.48)])
    nerve=Line([x,y+.65,0],[x+2.9,y+1,0],color=BLUE,stroke_width=5)
    return VGroup(shell,fibers,VGroup(wrap,nerve))


def raster(x,y,width=4.6,sparse=False,height=.75):
    ts=np.array([.25,.78]) if sparse else np.arange(.08,.96,.06)
    return VGroup(*[Line([x+width*t,y-height/2,0],[x+width*t,y+height/2,0],
        color=RED if sparse else BLUE,stroke_width=4) for t in ts])


def prediction(answer=False):
    title=heading('Predict: what happens to stretch-evoked firing?')
    labs=VGroup(label('control',-3,2.05,BLUE),label('Piezo2 deletion',3,2.05,RED))
    boxes=VGroup(*[Rectangle(width=5.4,height=2.15,color=GREY,stroke_width=2)
        .move_to([x,.45,0]) for x in (-3,3)])
    ctl=raster(-5.35,.55)
    result=raster(.65,.55,sparse=True) if answer else label('?',3,.5,TEXT,70)
    axes=VGroup(*[VGroup(Line([x-2.3,-.3,0],[x+2.3,-.3,0],color=GREY),
        label('time →',x,-.95,GREY,26)) for x in (-3,3)])
    note=label('schematic recordings',-3,-1.6,GREY,26)
    return VGroup(title,labs,boxes,ctl,result,axes,note)


def mouse():
    # Dorsal view: broad paws and bent, filled limbs make the splay readable.
    legs=VGroup()
    for x,y,dx,dy in [(-.9,.45,-.9,.85),(.8,.45,.85,.8),
            (-.9,-.45,-.9,-.85),(.8,-.45,.85,-.8)]:
        bx,by=x+dx*.55,y+dy*.35
        ex,ey=x+dx,y+dy
        limb=Polygon([x,y-.14,0],[bx,by-.14,0],[ex,ey-.14,0],
            [ex,ey+.14,0],[bx,by+.14,0],[x,y+.14,0],
            color=RED,fill_color=RED,fill_opacity=.8,stroke_width=2)
        paw=Ellipse(width=.52,height=.32,color=RED,fill_color=RED,
            fill_opacity=.8).move_to([ex,ey,0])
        legs.add(limb,paw)
    body=Ellipse(width=3.1,height=1.5,color=GREY,fill_color=GREY,fill_opacity=.5)
    head=Ellipse(width=1.2,height=1.05,color=GREY,fill_color=GREY,
        fill_opacity=.65).move_to([1.65,0,0])
    ears=VGroup(*[Circle(radius=.32,color=GREY,fill_color=BG,fill_opacity=1)
        .move_to([1.3,y,0]) for y in (.55,-.55)])
    nose=Dot([2.28,0,0],radius=.09,color=TEXT)
    eyes=VGroup(*[Dot([1.85,y,0],radius=.055,color=TEXT) for y in (.23,-.23)])
    tail=VMobject(color=GREY,stroke_width=6).set_points_smoothly(
        [[-1.5,0,0],[-2,.3,0],[-2.65,-.05,0],[-2.9,.45,0]])
    return VGroup(tail,legs,body,head,ears,nose,eyes)


def compact_recordings(g):
    g[1].move_to([0,2.3,0])
    for box in g[2]:
        box.stretch_to_fit_height(1.25).set_y(1.35)
    g[3].set_y(1.4);g[4].set_y(1.4)
    for axis in g[5]:
        axis[0].set_y(.85);axis[1].set_y(.42)
    return g


def reveal_scene():
    g=prediction(True)
    g[0].become(heading('Stretch-evoked firing: sharply reduced'))
    g.remove(g[6]);compact_recordings(g)
    return VGroup(g,label('Pvalb-Cre and HoxB8-Cre: sharply reduced',0,-.15,RED,27),
        mouse().scale_to_fit_height(2.9).move_to([0,-2.05,0]))


def decay(limit=25):
    ax=Axes(x_range=[0,limit,limit/5],y_range=[0,1,.25],x_length=10.5,y_length=4.5,
        axis_config={'color':GREY,'include_numbers':False},tips=False).move_to([.25,-.05,0])
    t=np.unique(np.r_[np.linspace(0,min(limit,40),500),np.linspace(0,limit,500)])
    curve=VMobject(color=GREEN,stroke_width=5).set_points_as_corners(
        [ax.c2p(v,np.exp(-v/5.6)) for v in t])
    ticks=[0,10,20] if limit==25 else [0,500,1000]
    labs=VGroup(label('fraction of peak current',-2.4,2.65,GREEN,26),
        label('time (ms)',0,-3.12,GREY,26),
        *[M(str(v),26,GREY).next_to(ax.c2p(0,v),LEFT,buff=.35) for v in (0,.5,1)],
        *[M(str(v),26,GREY).next_to(ax.c2p(v,0),DOWN,buff=.15) for v in ticks])
    return VGroup(ax,curve,labs)


def decay_notes():
    return VGroup(label('τ = 5.6 ms',2.8,1.8,GREEN,30),
        label('single-exponential assumption',2.2,1.05,GREY,26))


def drop_readout(ax):
    p=ax.c2p(20,np.exp(-20/5.6))
    return VGroup(DashedLine(ax.c2p(0,np.exp(-20/5.6)),p,color=YELLOW),
        Dot(p,color=GREEN,radius=.09),Line(p,p+UP*.9,color=GREEN),
        label('about 3% left at 20 ms',2.35,-.85,GREEN,32))


def holdplot():
    ax=Axes(x_range=[0,4,1],y_range=[0,1,1],x_length=10.3,y_length=2.2,
        tips=False,axis_config={'color':GREY,'include_numbers':False}).move_to([.15,1.05,0])
    curve=ax.plot(lambda t: np.clip((t-.5)/.5,0,1),x_range=[0,4,.01],
        color=YELLOW,stroke_width=5,use_smoothing=False)
    labs=VGroup(label('muscle length',-3.7,2.6,YELLOW),label('hold: seconds',3.1,2.6,YELLOW),
        *[M(str(t),26,GREY).next_to(ax.c2p(t,0),DOWN,buff=.12) for t in range(5)],
        label('sensory firing',-3.9,-.95,BLUE),label('time (s)',0,-2.55,GREY,26),
        label('Woo: stretch response measured during the hold',0,-3.18,TEXT,26))
    # Explicit schematic event model: 12 Hz during ramp; 6 Hz during held stretch.
    events=np.r_[np.arange(.5,1,1/12),np.arange(1,4,1/6)]
    spikes=VGroup(*[Line([ax.c2p(t,0)[0],-2.05,0],[ax.c2p(t,0)[0],-1.4,0],
        color=BLUE,stroke_width=3) for t in events])
    baseline=Line([ax.c2p(0,0)[0],-2.1,0],[ax.c2p(4,0)[0],-2.1,0],color=GREY)
    return VGroup(ax,curve,labs,spikes,baseline)


def options_title():
    return VGroup(heading('How could a held signal arise?'),
        label('Full pathway not settled',0,2.45,TEXT,28))


def optioncards(third=False):
    if third:
        return VGroup(*[chip(s,c,27).move_to([x,1.45,0]) for s,c,x in
            [('Cell body ≠ ending',GREY,-4.25),('Other channels?',GREY,0),('Ending machinery',BLUE,4.25)]])
    cards=VGroup(*[RoundedRectangle(width=5.55,height=4.85,corner_radius=.2,color=GREY,
        fill_color=GREY,fill_opacity=.04).move_to([x,-.55,0]) for x in (-3,3)])
    texts=VGroup(label('Cell body ≠ ending',-3,1.35,TEXT,30),label('Other channels may help',3,1.35,TEXT,28))
    cell=Circle(radius=.5,color=GREY,fill_color=GREY,fill_opacity=.3).move_to([-4.1,-.25,0])
    dish=VGroup(Ellipse(width=2.5,height=.42,color=GREY).move_to([-4.1,-.65,0]),
        VMobject(color=GREY,stroke_width=4).set_points_as_corners(
            [[-5.35,-.65,0],[-5.15,-1.3,0],[-3.05,-1.3,0],[-2.85,-.65,0]]))
    end=organ().scale(.43).move_to([-2.8,-2.05,0])
    icons=VGroup(cell,dish,end,label('dish',-4.1,.65,GREY,26),
        label('muscle ending',-2.8,-2.7,BLUE,26),arrow([-4.5,-1.5,0],[-3.6,-1.8,0]))
    other=VGroup(channel().scale(.55).move_to([2,-.5,0]),
        DashedVMobject(RoundedRectangle(width=1.5,height=1.65,color=GREY)).move_to([4.25,-.5,0]),
        label('?',4.25,-.5,TEXT,48),label('possible contribution',3,-2.25,GREY,28))
    return VGroup(cards,texts,icons,other)


class S00Title(TitleCard):
    LESSON="Proprioception: Sensing the Body's Own Position"
    TITLE='The Channel on the Line'
    def construct(self):
        g=VGroup(T('BIOCHEMISTRYPEDIA',26,TEAL),T('Proprioception:',28,GREY),
            T('Sensing the Body’s Own Position',28,GREY),T(self.TITLE,48,font=TITLE_FONT),
            Line(LEFT*1.3,RIGHT*1.3,color=GOLD)).arrange(DOWN,buff=.35)
        self.add(g);self.finish()


class S01Q(SpokenScene):
    def construct(self):
        stage=membrane_stage();q=label('?',0,-.1,GREEN,110)
        self.add(heading('What turns stretch into a signal?'),stage,q,
            arrow([-3,-1.2,0],[-5.6,-1.2,0],YELLOW),arrow([3,-1.2,0],[5.6,-1.2,0],YELLOW))
        self.at('what turns stretch');self.play(Indicate(q,scale_factor=1.2),run_time=.6)
        self.finish()


class S02Candidate(SpokenScene):
    def construct(self):
        stage=membrane_stage();ch=channel().scale(1.3).move_to([0,-.1,0])
        self.add(stage,ch,heading('A mechanically activated channel'),label('Piezo2',-2.9,1.8,GREEN,38))
        self.at('a mechanically activated');self.play(Indicate(ch),run_time=.5)
        self.at('force opens it')
        self.play(stage[0][0].animate.shift(LEFT*.45),stage[0][1].animate.shift(RIGHT*.45),
            Transform(ch,channel(True).scale(1.3).move_to([0,-.1,0])),
            GrowArrow(arrow([-2.7,-1.25,0],[-6,-1.25,0],YELLOW)),
            GrowArrow(arrow([2.7,-1.25,0],[6,-1.25,0],YELLOW)),run_time=.8)
        self.finish()


class S03Woo(SpokenScene):
    def construct(self):
        boxes=VGroup(*[RoundedRectangle(width=3.8,height=4.9,corner_radius=.2,
            color=GREY).move_to([x,-.2,0]) for x in (-4.15,0,4.15)])
        labels=VGroup(label('1  Where it is',-4.15,1.75,TEXT,29),
            label('2  What current\nit carries',0,1.65,TEXT,28),
            label('3  Does the\nending need it?',4.15,1.65,TEXT,28))
        icons=VGroup(organ().scale(.43).move_to([-4.15,-.6,0]),
            channel().scale(.7).move_to([0,-.6,0]),label('?',4.15,-.6,GREEN,86))
        self.add(heading('Woo and colleagues, 2015'),boxes,labels,icons)
        self.at('in three ways')
        self.play(LaggedStart(*[b.animate.set_color(GREEN) for b in boxes],lag_ratio=.4),run_time=1)
        self.finish()


class S04Where(SpokenScene):
    def construct(self):
        a=organ(0,1);b=organ(0,-1.55,True)
        self.add(heading('1  Where it is'),a,b,
            label('spindle',-4.7,2, TEXT,28),label('tendon organ',-4.65,-.5,TEXT,28),
            label('central intrafusal region',0,-.15,GREY,26))
        self.at('a reporter showed')
        self.play(a[2].animate.set_color(GREEN),b[2].animate.set_color(GREEN),run_time=.6)
        self.at('sensory endings')
        self.play(FadeIn(label('reporter signal: sensory endings',0,-3.1,GREEN,30)),
            Create(Line([3,-2.75,0],[1.1,-2.15,0],color=GREEN)),run_time=.4)
        self.finish()


class S05Current(SpokenScene):
    def construct(self):
        cell=Circle(radius=1.25,color=GREEN,fill_color=GREEN,fill_opacity=.1).move_to([-3.4,-.15,0])
        probe=Polygon([-5.7,1.55,0],[-5.7,1.15,0],[-4.65,.1,0],color=GREY,fill_opacity=.35)
        pip=VGroup(Line([-2.15,.2,0],[-1.4,1.3,0],color=GREY,stroke_width=4),
            Line([-2.1,0,0],[-1.15,1.15,0],color=GREY,stroke_width=4))
        ax=Axes(x_range=[0,25,5],y_range=[0,1,1],x_length=5.2,y_length=3.4,tips=False,
            axis_config={'color':GREY,'include_numbers':False}).move_to([3,-.4,0])
        # Piecewise stimulus onset followed by the same exponential decay model.
        def current(t):
            return 0 if t<2 else ((t-2) if t<3 else np.exp(-(t-3)/5.6))
        curve=ax.plot(current,x_range=[0,25,.025],color=GREEN,use_smoothing=False,stroke_width=5)
        self.add(heading('2  What current it carries'),cell,probe,pip,ax,
            label('probe indents',-4.6,2.1,TEXT,27),label('pipette records',-1.35,1.85,TEXT,27),
            label('current / peak',3,1.8,GREEN,27),label('time (ms)',3,-2.8,GREY,27),
            *[M(str(t),26,GREY).next_to(ax.c2p(t,0),DOWN,buff=.12) for t in (0,10,20)],
            *[M(str(v),26,GREY).next_to(ax.c2p(0,v),LEFT,buff=.35) for v in (0,1)],
            label('cell body',-3.4,-1.75,GREY,27),
            label('23 of 25 labelled neurons',-3.2,-2.65,GREEN,28))
        self.at('poked cell bodies')
        self.play(probe.animate.shift(RIGHT*.25),cell.animate.stretch(.88,0),Create(curve),run_time=1.1)
        self.at('gave rapidly')
        self.play(FadeIn(label('rapidly adapting',3.85,.65,GREEN,30)),run_time=.25)
        self.add(label('schematic current model',0,-3.4,GREY,26));self.finish()


class S06Cre(SpokenScene):
    def construct(self):
        drivers=VGroup(chip('Pvalb-Cre',RED,30),chip('HoxB8-Cre',RED,30)).arrange(RIGHT,buff=1).move_to([0,2.15,0])
        dna=VGroup(Line([-5,1,0],[-2.9,1,0],color=GREY,stroke_width=8),
            Line([2.9,1,0],[5,1,0],color=GREY,stroke_width=8))
        gene=VGroup(Rectangle(width=5,height=.65,color=GREEN,fill_color=GREEN,fill_opacity=.28),
            label('Piezo2 gene',0,0,GREEN,32)).move_to([0,1,0])
        sites=VGroup(*[Triangle(color=RED,fill_color=RED,fill_opacity=.8).scale(.22).rotate(-PI/2)
            .move_to([x,1,0]) for x in (-2.9,2.9)])
        site_labels=VGroup(label('target site',-4,1.65,RED,26),label('target site',4,1.65,RED,26))
        boundary=RoundedRectangle(width=11.5,height=5.4,corner_radius=.3,color=RED,
            fill_color=RED,fill_opacity=.04).move_to([0,0,0])
        cells=VGroup(chip('proprioceptors',BLUE,30).move_to([-2.8,-1.7,0]),
            chip('other cells',GREY,30).move_to([2.8,-1.7,0]))
        self.add(heading('3  Does the ending need it?'),dna,gene,sites,site_labels,boundary,
            label('driver-targeted cells',0,-.65,RED,30))
        self.at('they used');self.play(FadeIn(drivers),run_time=.3)
        self.at('to remove')
        # Lift the flanked segment clear of its locus, then fade the excised gene.
        self.play(gene.animate.shift(UP*.65),sites.animate.shift(UP*.65),run_time=.5)
        self.play(FadeOut(gene),FadeOut(sites),FadeOut(site_labels),
            Transform(dna,VGroup(Line([-5,1,0],[-.3,1,0],color=GREY,stroke_width=8),
                Line([.3,1,0],[5,1,0],color=GREY,stroke_width=8))),run_time=.4)
        self.at('including proprioceptors');self.play(FadeIn(cells[0]),run_time=.3)
        self.at('neither driver is');self.play(FadeIn(cells[1]),
            FadeIn(label('Neither driver is specific to proprioceptors',0,-3.05,RED,29)),run_time=.3)
        self.finish()


class S07Stretch(SpokenScene):
    def construct(self):
        muscle=Ellipse(width=4.7,height=1.8,color=GREY,fill_color=GREY,fill_opacity=.2).move_to([0,-1.2,0])
        fibers=VGroup(*[Line([-2.1,-1.2+d,0],[2.1,-1.2+d,0],color=GREY) for d in (-.4,0,.4)])
        tendons=VGroup(Line([-4.6,-1.2,0],[-2.35,-1.2,0],color=GREY,stroke_width=12),
            Line([2.35,-1.2,0],[4.6,-1.2,0],color=GREY,stroke_width=12))
        clamps=VGroup(*[Rectangle(width=.25,height=1.15,color=YELLOW).move_to([x,-1.2,0]) for x in (-4.6,4.6)])
        nerve=VMobject(color=BLUE,stroke_width=5).set_points_as_corners([[0,-.3,0],[0,.4,0],[4.8,.4,0]])
        electrode=Rectangle(width=.6,height=.65,color=TEXT).move_to([3.8,.4,0])
        # A continuous lead joins the recording baseline directly to the electrode.
        trace=VGroup(Line([3.8,.725,0],[3.8,1.15,0],color=BLUE),
            Line([.5,1.15,0],[5,1.15,0],color=BLUE))
        spikes=raster(.5,1.47,width=4.4,height=.64)
        self.add(heading('Isolated muscle → sensory nerve recording'),muscle,fibers,tendons,
            clamps,nerve,electrode,trace,label('electrode',4.5,-.25,TEXT,26),
            label('sensory nerve',-2,.4,BLUE,28),label('schematic spikes',2.8,2.15,BLUE,26))
        self.at('they stretched')
        self.play(muscle.animate.stretch_to_fit_width(7),fibers.animate.stretch_to_fit_width(6.4),
            clamps[0].animate.shift(LEFT*1.1),clamps[1].animate.shift(RIGHT*1.1),
            Transform(tendons,VGroup(Line([-5.7,-1.2,0],[-3.5,-1.2,0],color=GREY,stroke_width=12),
                Line([3.5,-1.2,0],[5.7,-1.2,0],color=GREY,stroke_width=12))),
            Create(spikes),GrowArrow(arrow([-3.5,-2.7,0],[-6,-2.7,0],YELLOW)),
            GrowArrow(arrow([3.5,-2.7,0],[6,-2.7,0],YELLOW)),run_time=1.2)
        self.at('recorded from');self.play(Indicate(electrode),run_time=.4);self.finish()


class S08Predict(SpokenScene):
    def construct(self):
        g=prediction();self.add(g)
        self.at('predict');self.play(Indicate(g[4]),run_time=.4)
        self.at('gone from these neurons');self.play(Indicate(g[1][1],color=RED),run_time=.5)
        self.add(label('Take a moment to predict',0,-2.75,TEXT,32));self.finish()


class S09Pause(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(prediction())
        # Preserve the silent five-second prediction hold with a gentle visible countdown.
        for n in range(5,0,-1):
            count=label('Think…  '+str(n),0,-2.75,TEXT,34);self.add(count);self.wait(1);self.remove(count)


class S10Reveal(SpokenScene):
    def construct(self):
        g=prediction();self.add(g)
        self.at('sharply reduced');self.play(Transform(g[4],raster(.65,.55,sparse=True)),
            Transform(g[0],heading('Stretch-evoked firing: sharply reduced')),run_time=.35)
        self.at('with either')
        target=compact_recordings(prediction(True))
        self.play(FadeOut(g[6]),*[Transform(g[i],target[i]) for i in range(1,6)],
            FadeIn(label('Pvalb-Cre and HoxB8-Cre: sharply reduced',0,-.15,RED,27)),run_time=.5)
        self.at('severely uncoordinated');self.play(FadeIn(mouse().scale_to_fit_height(2.9).move_to([0,-2.05,0])),run_time=.4)
        self.finish()


class S11Beat(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(reveal_scene());self.wait(2)


class S12Residue(SpokenScene):
    def construct(self):
        muscles=VGroup(*[Ellipse(width=1.3,height=4.7,color=GREY,fill_color=GREY,
            fill_opacity=.1) for _ in range(8)]).arrange(RIGHT,buff=.22).move_to([0,.15,0])
        fibers=VGroup(*[Line(m.get_center()+DOWN*1.9,m.get_center()+UP*1.9,color=GREY) for m in muscles])
        self.add(heading('Did every stretch response disappear?'),muscles,fibers)
        self.at('one of eight muscles');self.play(Transform(self.mobjects[0],heading('1 of 8 muscles per Cre line')),run_time=.25)
        self.at('some stretch response')
        faint=raster(muscles[0].get_x()-.5,.15,width=1,sparse=True,height=1.15).set_color(BLUE)
        self.remove(fibers[0])
        self.play(muscles[0].animate.set_color(BLUE).set_fill(BLUE,.2),FadeIn(faint),
            FadeIn(label('some stretch response remained',0,-2.7,BLUE,31)),
            run_time=.35)
        self.at('remained',lead=-.4)
        self.play(FadeIn(label('mostly atypical firing',0,-3.35,GREY,28)),run_time=.3);self.finish()


def remaining():
    box=RoundedRectangle(width=10.4,height=3.25,corner_radius=.7,color=BLUE,
        fill_color=BLUE,fill_opacity=.06).move_to([0,-.25,0])
    return VGroup(box,label('spindle sensory ending',0,1.75,BLUE,30),
        channel().scale(.7).move_to([-3,-.25,0]),channel().scale(.7).move_to([-.5,-.25,0]))


class S13Principal(SpokenScene):
    def construct(self):
        self.add(remaining(),heading('Possible incomplete deletion'))
        self.at('incomplete deletion');self.play(Indicate(self.mobjects[0][2]),run_time=.35)
        self.at('so it is called')
        principal=T('PRINCIPAL TRANSDUCER',39,GREEN,weight=BOLD).move_to([0,-2.75,0])
        self.add(principal)
        self.at('principal transducer');self.play(Indicate(principal,color=GREEN,scale_factor=1.02),run_time=.35);self.finish()


class S14Hedge(SpokenScene):
    def construct(self):
        self.add(remaining(),heading('Possible incomplete deletion'))
        q=VGroup(DashedVMobject(RoundedRectangle(width=1.8,height=2,color=GREY)),
            T('?',52,TEXT)).move_to([3,-.25,0])
        self.at('a second channel');self.play(FadeIn(q),run_time=.25)
        self.at('nor does it');self.play(FadeIn(label('A second channel remains an open possibility',0,-2.9,TEXT,30)),run_time=.25)
        self.finish()


class S15Rule(SpokenScene):
    def construct(self):
        card=VGroup(label('Limb position is an estimate built mainly',0,2.8,ORANGE,34),
            label('from spindle length signals',0,2.1,ORANGE,34))
        ch=channel().scale(.65).move_to([-4.9,-.4,0])
        ending=chip('spindle\nlength signal',BLUE,30).move_to([-1.65,-.4,0])
        nerve=VGroup(Line([.25,-.4,0],[2,-.4,0],color=BLUE,stroke_width=7),
            label('nerve',1.1,-1.2,BLUE,28))
        brain=chip('brain’s\nposition estimate',ORANGE,29).move_to([4.25,-.4,0])
        self.add(card,ch,ending,nerve,brain,label('Piezo2',-4.9,-2,GREEN,32),
            arrow([-3.8,-.4,0],[-3,-.4,0],BLUE),arrow([2,-.4,0],[2.65,-.4,0],BLUE))
        self.at('the principal channel');self.play(Indicate(ch),run_time=.4)
        self.at('it starts the signal')
        self.play(ShowPassingFlash(Line([-3.8,-.4,0],[2.5,-.4,0],color=YELLOW,stroke_width=7)),run_time=.8)
        self.at('the brain reads');self.play(Indicate(brain),run_time=.4);self.finish()


class S16Puzzle(SpokenScene):
    def construct(self):
        g=decay();self.add(g[0],g[2],heading('Cell body in culture'))
        self.at('now a puzzle');self.play(Create(g[1]),run_time=2.8)
        self.at('time constant');self.play(FadeIn(decay_notes()),run_time=.25);self.finish()


class S17Drop(SpokenScene):
    def construct(self):
        g=decay();readout=drop_readout(g[0]);self.add(g,heading('Cell body in culture'),decay_notes(),readout)
        self.at('assume one exponential');self.play(Indicate(g[1],scale_factor=1.01),run_time=.4)
        self.at('only about');self.play(Indicate(readout[1]),run_time=.4);self.finish()


class S18Zoom(SpokenScene):
    def construct(self):
        g=decay();notes=decay_notes();readout=drop_readout(g[0])
        self.add(g,heading('Cell body in culture'),notes,readout)
        self.at('zoom out');self.play(FadeOut(notes),FadeOut(readout),run_time=.2)
        # Recompute continuously as the maximum time expands, rather than morphing two curves.
        limit=ValueTracker(25)
        def zoom_curve():
            maximum=limit.get_value()
            t=np.unique(np.r_[np.linspace(0,min(maximum,40),500),np.linspace(0,maximum,500)])
            # Fixed plot rectangle: rescale each sample's x coordinate continuously.
            ax=g[0]
            return VMobject(color=GREEN,stroke_width=5).set_points_as_corners(
                [ax.c2p(v/maximum*25,np.exp(-v/5.6)) for v in t])
        dynamic=always_redraw(zoom_curve)
        self.remove(g[1]);self.add(dynamic)
        self.play(limit.animate.set_value(1000),Transform(g[2],decay(1000)[2]),run_time=1.6,rate_func=smooth)
        self.remove(dynamic);self.add(decay(1000)[1])
        self.at('the curve lies')
        p=g[0].c2p(17,0)
        self.play(FadeIn(label('effectively zero',2.4,-1.55,GREEN,32)),
            Create(Line([2.4,-1.85,0],[2.4,-2.25,0],color=GREEN)),run_time=.3);self.finish()


class S19Held(SpokenScene):
    def construct(self):
        g=holdplot();self.add(g,heading('Muscle stretch and sensory firing'))
        self.at('a spindle must report');self.play(Indicate(g[1],scale_factor=1.01),run_time=.6)
        self.at('is needed for');self.play(FadeIn(chip('Piezo2 needed for held response',GREEN,28).move_to([1.6,.85,0])),run_time=.25)
        self.finish()


class S20How(SpokenScene):
    def construct(self):
        self.add(heading('How can a fast channel support a held signal?'))
        for x,held in [(-3.5,False),(3.5,True)]:
            ax=Axes(x_range=[0,4 if held else 25,1 if held else 5],y_range=[0,1,1],
                x_length=4.65,y_length=3.7,tips=False,axis_config={'color':GREY,'include_numbers':False}).move_to([x,-.05,0])
            fn=(lambda t: np.clip((t-.5)/.5,0,1)) if held else (lambda t: np.exp(-t/5.6))
            curve=ax.plot(fn,x_range=[0,4 if held else 25,.02],use_smoothing=False,
                color=YELLOW if held else GREEN,stroke_width=5)
            self.add(ax,curve,label('stretch' if held else 'current',x,2.2,YELLOW if held else GREEN,29),
                label('time (seconds)' if held else 'time (ms)',x,-2.5,GREY,28),
                label('seconds of hold' if held else 'τ = 5.6 ms',x,-3.15,TEXT,30),
                *[M(str(t),26,GREY).next_to(ax.c2p(t,0),DOWN,buff=.12) for t in ([0,2,4] if held else [0,10,20])],
                *[M(str(v),26,GREY).next_to(ax.c2p(0,v),LEFT,buff=.35) for v in (0,1)])
        q=label('?',0,.15,TEXT,74);self.add(q)
        self.at('how does a channel');self.play(Indicate(q),run_time=.5);self.finish()


class S21Options(SpokenScene):
    def construct(self):
        cards=optioncards();self.add(options_title(),cards)
        self.at('a cell body');self.play(Indicate(cards[2][0]),run_time=.4)
        self.at('an ending in muscle');self.play(Indicate(cards[2][2]),run_time=.4)
        self.at('other channels may');self.play(Indicate(cards[3]),run_time=.5);self.finish()


class S22Options2(SpokenScene):
    def construct(self):
        cards=optioncards(True).set_y(1.8)
        xs=(-3,-.5)
        def bilayer(gaps=False):
            spans=[(-5.5,5.5)] if not gaps else [(-5.5,-3.3),(-2.7,-.8),(-.2,5.5)]
            return VGroup(*[Line([a,y,0],[b,y,0],color=BLUE,stroke_width=5)
                for y in (-.65,-.9) for a,b in spans])
        membrane=bilayer()
        outline=VMobject(color=BLUE,stroke_width=3).set_points_as_corners(
            [[-5.5,-.65,0],[-5.5,1.1,0],[5.5,1.1,0],[5.5,-.65,0]])
        ves=VGroup(*[Circle(radius=.62,color=GREY,fill_color=GREY,fill_opacity=.12)
            .move_to([x,.25,0]) for x in xs])
        dots=VGroup(*[Dot([x+dx,.25+dy,0],radius=.075,color=BLUE)
            for x in xs for dx,dy in [(-.2,0),(.2,0),(0,.22),(0,-.22)]])
        title=options_title()
        self.add(title,cards,outline,membrane,ves,dots,
            label('sensory ending',3.6,.8,BLUE,26),label('vesicles',2.6,.25,GREY,29),
            label('membrane',4.2,-1.3,BLUE,27),
            label('Supported contributor: Than and colleagues, 2021',0,-3.3,BLUE,27))
        self.at('the ending has');self.play(Indicate(cards[2]),run_time=.4)
        self.at('vesicle');self.play(Indicate(ves,color=GREY,scale_factor=1.06),run_time=.3)
        self.at('glutamate helps')
        self.play(ves.animate.shift(DOWN*.28),dots.animate.shift(DOWN*.28),run_time=.35)
        # Round fused vesicles retain their outlines, with a pore at the lower membrane.
        fused=VGroup(*[Arc(radius=.62,start_angle=-PI/2+.5,angle=TAU-1,
            color=GREY,stroke_width=4).shift([x,-.03,0]) for x in xs])
        pores=VGroup(*[Line([x+dx,-.57,0],[x+dx,-.9,0],color=GREY,stroke_width=4)
            for x in xs for dx in (-.3,.3)])
        self.play(Transform(ves,fused),Transform(membrane,bilayer(True)),FadeIn(pores),run_time=.4)
        crossing=VGroup(*[Dot([x+dx,-.88+dy,0],radius=.075,color=BLUE)
            for x in xs for dx,dy in [(-.12,0),(.12,0),(0,.18),(0,-.18)]])
        self.play(Transform(dots,crossing),run_time=.35)
        targets=VGroup(*[Dot([x+dx,-1.95+dy,0],radius=.075,color=BLUE)
            for x in xs for dx,dy in [(-.4,0),(.4,0),(0,.25),(0,-.25)]])
        self.play(Transform(dots,targets),FadeIn(label('glutamate release',3,-2,BLUE,30)),run_time=.6)
        self.at('the full pathway');self.play(Indicate(title[1]),run_time=.5);self.finish()


class S23Takeaway(SpokenScene):
    def construct(self):
        ch=channel().scale(1.45).move_to([-3.5,.1,0])
        question=label('Held signal:\nstill an open question',0,-2.5,TEXT,40)
        self.add(ch,label('Piezo2',2.1,1.35,GREEN,44),
            label('Principal transducer\non the stretch line',2.1,-.15,GREEN,36),question)
        self.at('the principal transducer');self.play(Indicate(ch),run_time=.4)
        self.at('how it supports');self.play(Indicate(question,color=TEXT,scale_factor=1.02),run_time=.4)
        self.finish()


class S24End(EndCard):
    LINE='Piezo2 is the principal transducer on the stretch line.'
    def construct(self):
        main=T(self.LINE,38,font=TITLE_FONT);fit(main,max_w=12)
        self.add(VGroup(main,T('Held signal: still open',38,TEXT),
            T('biochemistrypedia.com',26,TEAL)).arrange(DOWN,buff=.6));self.finish()
