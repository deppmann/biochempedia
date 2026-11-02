"""Chapter 2: word-aligned calibration film.

COLOR MAP (inherited from scenes.old.py; CHAPTERS.md is read-only for this task):
GREY = probe, sites, structure, de-emphasised things; BLUE = neuron / neuron count;
TEAL = recorded signal / addressed channels; YELLOW = inferred unit / rate;
ORANGE = mouse A; PINK = mouse B; PURPLE = session;
RED = wrong count / false alarm; GREEN = correct animal-level count.
Chapter extensions: GREEN also denotes fluorescence (as specified in the script),
YELLOW detection estimates; TEAL electrical ground truth and photon collection.

Reference reuse: neuron(), bchip() reproduce the reference's cartoon and opaque chip.
The old film contains no calcium model. Traces below implement the lesson's slow
exponential transient and Poisson photon-noise model (Going deeper), with invented
illustrative events, tau=.5 s, fractional amplitude=.18. They are not measured data.
Gauge ranges are the numbers supplied by the reviewed chapter, not fitted curves.
"""
import numpy as np
from bp_style import *

PURPLE = '#B58CD9'
ORANGE = '#F29E4C'
PINK = '#E58FB5'


def pos(x=0, y=0):
    return np.array([x, y, 0.])


def label(text, x=0, y=0, size=30, color=TEXT):
    return T(text, size=size, color=color).move_to(pos(x,y))


def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=.14, width=c[0].width, height=c[0].height,
        stroke_width=0, fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def neuron(color=BLUE, r=.34, nd=3):
    soma = Circle(radius=r, stroke_color=color, stroke_width=4,
                  fill_color=color, fill_opacity=.35)
    lines=[]
    for k in range(nd):
        ang=2*PI*k/nd+PI/6
        d=np.array([np.cos(ang),np.sin(ang),0])
        lines.append(Line(d*r,d*(r+.36),color=color,stroke_width=4))
    g=VGroup(soma,*lines)
    g.soma=soma
    return g


def path(xs,ys,color=GREEN,width=4):
    m=VMobject(stroke_color=color,stroke_width=width)
    m.set_points_as_corners([pos(x,y) for x,y in zip(xs,ys)])
    return m


def response(t, events):
    return sum(.18*np.exp(-np.maximum(t-e,0)/.5)*(t>=e) for e in events) if events else np.zeros_like(t)


def trace(x=-5.4,y=-1.8,w=10.8,events=(1.0,),photons=None,seed=7,scale=7, duration=4):
    t=np.linspace(0,duration,401)
    f=response(t,events)
    if photons is not None:
        f=np.random.default_rng(seed).poisson(photons*(1+f))/photons-1
    return path(x+w*t/duration,y+scale*f)


# Exact audio lengths: the shared helper adds a 0.4 s tail to EVERY scene.
# Keep word cues, but avoid that accumulating drift and workspace sync-log writes.
_BaseSpokenScene = SpokenScene
class SpokenScene(_BaseSpokenScene):
    def at(self, phrase, lead=.12, nth=0):
        rest=self.t_of(phrase,nth)-lead-self.elapsed()
        if rest>.001: self.wait(rest)
    def finish(self):
        rest=self.narration_s-self.elapsed()
        if rest>.001: self.wait(rest)


def record(x=-4.9,w=9.8,flat=False):
    axes=VGroup(
        Line(pos(x,1.9),pos(x+w,1.9),color=GREY),
        Line(pos(x,-2.2),pos(x+w,-2.2),color=GREY),
        Line(pos(x,-2.2),pos(x,.4),color=GREY),
        label('spikes',x-.65,2.5,26,TEAL),
        label('light',x-.65,-.2,26,GREEN),
        label('time →',x+w-.6,-2.8,26,GREY),
        label('illustrative record',0,3.25,26,GREY))
    ev=(.65,1.8,3.)
    ticks=VGroup(*[Line(pos(x+w*e/4,1.9),pos(x+w*e/4,2.65),color=TEAL,stroke_width=5) for e in ev])
    t=np.linspace(0,4,801)
    # A weak middle light response is below shot noise, although its spike is real.
    amps=(.18,.001,.18) if not flat else (.0003,.0003,.0003)
    f=sum(a*np.exp(-np.maximum(t-e,0)/.5)*(t>=e) for a,e in zip(amps,ev))
    n=3200 if not flat else 4000000
    f=np.random.default_rng(7).poisson(n*(1+f))/n-1
    glow=path(x+w*t/4,-2.2+10*f)
    return axes,ticks,glow


def link_record(ticks,glow):
    links=VGroup(); marks=VGroup()
    for i,t in enumerate(ticks):
        # Locate the model's first sample at/after this event, not an invented endpoint.
        pts=np.array(glow.get_anchors()); pt=pts[np.argmin(abs(pts[:,0]-t.get_x()))]
        links.add(DashedLine(pos(t.get_x(),1.88),pt,color=GREY,dash_length=.12))
        if i==1:
            marks.add(label('no bump',t.get_x()+.85,-.8,26,GREY))
        else:
            marks.add(label('✓',t.get_x()+.38,pt[1]+.12,30,YELLOW))
    return links,marks


def pipette_cell():
    # Closed tapered glass: narrow tip touches, never crosses, the soma membrane.
    cell=neuron(r=1.95).move_to(pos(-2,-.45))
    tip=cell.soma.get_right()
    glass=Polygon(tip+pos(0,.07),pos(7.3,2.7),pos(7.3,1.4),tip-pos(0,.07),
                  color=GREY,fill_color=GREY,fill_opacity=.12,stroke_width=4)
    return cell,glass


def objective():
    return VGroup(Polygon(pos(-3.1,3.4),pos(-.9,3.4),pos(-1.3,2.15),pos(-2.7,2.15),
                         color=GREY,fill_opacity=.25),
                  Line(pos(-2.7,2.15),pos(-1.3,2.15),color=TEAL,stroke_width=5),
                  Polygon(pos(-2.7,2.1),pos(-1.3,2.1),pos(-.9,.6),pos(-3.1,.6),
                          stroke_width=0,fill_color=TEAL,fill_opacity=.09),
                  label('microscope',1,3.0,28,GREY))


def gauge(x=0,title='Detection',lo=0,hi=None,reading='',bottom=-2.25,height=5):
    hi=lo if hi is None else hi
    frame=RoundedRectangle(width=1.25,height=height,corner_radius=.1,color=GREY).move_to(pos(x,bottom+height/2))
    fill=Rectangle(width=1.1,height=max(.01,height*lo),stroke_width=0,fill_color=YELLOW,fill_opacity=.82).move_to(pos(x,bottom+max(.01,height*lo)/2))
    band=Rectangle(width=1.1,height=max(.01,height*(hi-lo)),stroke_width=0,fill_color=YELLOW,fill_opacity=.3).move_to(pos(x,bottom+height*lo+max(.01,height*(hi-lo))/2))
    marks=VGroup(label('100%',x+1.2,bottom+height,26,GREY),label('0',x+1,bottom,26,GREY))
    return VGroup(frame,fill,band,marks,label(title,x,bottom+height+.5,28),label(reading,x,bottom-.6,36,YELLOW))


def comparisons(wide=False,blind=False):
    xs=(-4.4,0) if blind else (-3.5,3.5)
    a=gauge(xs[0],'Chen',.99,reading='99%')
    b=gauge(xs[1],'Huang: tuned',.16 if wide else .4,.43 if wide else .8,
            reading='~16–43%' if wide else '~40–80%')
    return VGroup(a,b,label('1% false positives',0,-3.45,26,RED))


def mosaic():
    frame=RoundedRectangle(width=11.6,height=4.9,corner_radius=.1,color=GREY).move_to(pos(0,.65))
    # 200 cells, with the target replacing rather than overprinting one neighbour.
    center=pos(-.275,.65)
    coords=[pos(-5.225+c*.55,-1.375+r*.45) for r in range(10) for c in range(20)]
    coords=sorted(coords,key=lambda p:np.linalg.norm(p-center))
    cells=VGroup(*[Dot(p,radius=.05,color=BLUE) for p in coords[1:]])
    target=Dot(coords[0],radius=.115,color=GREEN)
    return VGroup(frame,cells,target)


QUESTION='What happens to single-spike detection?\nWhy?'
def question_frame():
    m=mosaic().stretch(.88,1).move_to(pos(0,-1.35))
    ring=Circle(radius=.32,color=GREEN,stroke_width=4).move_to(m[2])
    q=VGroup(label('What happens to single-spike detection?',size=34),label('Why?',size=34)).arrange(DOWN,buff=.2).move_to(pos(0,3.1))
    return VGroup(m,ring,q)


def window_row():
    windows=VGroup()
    for i in range(4):
        x=-4.5+i*3
        rect=RoundedRectangle(width=2.7,height=5.35,corner_radius=.12,color=GREY).move_to(pos(x,.15))
        top=Line(pos(x-1.15,1.65),pos(x+1.15,1.65),color=TEAL)
        # A spurious optical transient is present from the beginning, surrounded
        # by the same shot noise as its neighbours; no electrical tick accompanies it.
        bottom=trace(x=x-1.15,y=-1.25,w=2.3,events=(1.0,) if i==2 else (),
                     photons=900,seed=i+10,scale=8)
        windows.add(VGroup(rect,top,bottom))
    return windows


class S00Title(TitleCard):
    LESSON='Recording Many Neurons: Imaging, Arrays and Atlases'
    TITLE='The Answer Key: How Many Spikes Is a Flash?'
    def construct(self):
        self.add(label('BIOCHEMISTRYPEDIA',0,2.8,26,TEAL),
                 label('Recording Many Neurons:\nImaging, Arrays and Atlases',0,1.6,28,GREY))
        self.play(FadeIn(label('The Answer Key:\nHow Many Spikes Is a Flash?',0,-.4,44)),
                  Create(Line(pos(-1.4,-2.3),pos(1.4,-2.3),color=GOLD,stroke_width=4)),run_time=.7)
        self.wait(max(0,self.narration_s-self.elapsed()))


class S01N(SpokenScene):
    def construct(self):
        n=neuron(r=1.05).move_to(pos(0,1.7))
        ax=VGroup(Line(pos(-4.9,-2.2),pos(5.5,-2.2),color=GREY),
                  Line(pos(-4.9,-2.2),pos(-4.9,.1),color=GREY),
                  label('ΔF/F0',-5.6,.1,26,GREEN),label('time →',4.9,-2.65,26,GREY))
        self.add(n,ax)
        glow=trace(x=-4.9,w=10.4,y=-2.2,events=(.65,),scale=9)
        self.at('flashes brighter')
        # Draw baseline first, then the model's rise at the flash, followed by decay.
        early=glow.copy().pointwise_become_partial(glow,0,.16)
        rest=glow.copy().pointwise_become_partial(glow,.16,1)
        self.add(early)
        self.play(n.soma.animate.set_fill(GREEN,.95).set_stroke(GREEN),Create(rest),run_time=1.1,rate_func=linear)
        self.play(n.soma.animate.set_fill(GREEN,.3),run_time=.4)
        self.at('How many spikes')
        self.play(FadeIn(label('How many spikes did it fire?',0,-3.25,34)),run_time=.3)
        self.finish()


class S02N(SpokenScene):
    def construct(self):
        ax=VGroup(Line(pos(-4.7,-2.5),pos(5.5,-2.5),color=GREY),
                  Line(pos(-4.7,-2.5),pos(-4.7,-.3),color=GREY),
                  label('light\nΔF/F0',-5.6,-1.25,26,GREEN),label('time →',4.9,-3.05,26,GREY))
        self.add(ax,trace(x=-4.7,w=10.2,y=-2.5,scale=9))
        pages=VGroup(RoundedRectangle(width=11.4,height=2.9,corner_radius=.15,color=GREY).move_to(pos(0,1.95)),
                     Line(pos(0,.5),pos(0,3.4),color=GREY))
        self.at('To translate')
        self.play(Create(pages),run_time=.55)
        self.at('record both at once')
        self.play(FadeIn(label('light',-2.65,1.9,40,GREEN)),FadeIn(label('spikes',2.65,1.9,40,TEAL)),run_time=.4)
        self.at('Then ask whether')
        self.play(FadeIn(label('Does this calibration fit?',0,-3.45,32,YELLOW)),run_time=.4)
        self.finish()


class S03N(SpokenScene):
    def construct(self):
        cell,glass=pipette_cell(); self.add(cell)
        self.at('fine glass pipette')
        glass.shift(RIGHT*1.4); self.play(FadeIn(glass),run_time=.35)
        self.at('presses against')
        self.play(glass.animate.shift(LEFT*1.4),run_time=.65)
        self.at('without breaking in')
        self.play(Indicate(cell.soma,scale_factor=1.02,color=BLUE),run_time=.5)
        self.at('each spike electrically')
        tip=cell.soma.get_right()
        pulses=VGroup(*[Dot(tip,radius=.11,color=TEAL) for _ in range(3)])
        end=pos(6.4,1.8)
        pipette_label=label('electrical spikes',3.7,-.35,30,TEAL)
        leader=Line(pos(3.7,-.05),pos(3.7,.9),color=TEAL,stroke_width=3)
        self.play(FadeIn(pipette_label),Create(leader),run_time=.25)
        self.play(LaggedStart(*[Succession(FadeIn(p,run_time=.05),
                  p.animate(run_time=.65,rate_func=linear).move_to(end),
                  FadeOut(p,run_time=.1)) for p in pulses],lag_ratio=.35),run_time=1.4)
        self.finish()


class S04N(SpokenScene):
    def construct(self):
        cell,glass=pipette_cell();self.add(cell,glass)
        self.at('This is a')
        self.play(FadeIn(label('cell-attached recording',0,-2.95,34,TEAL)),run_time=.4)
        self.at('the microscope')
        self.play(FadeIn(objective()),run_time=.45)
        self.at('same cells glow')
        tip=cell.soma.get_right(); blip=Dot(tip,color=TEAL,radius=.12)
        self.add(blip)
        self.play(cell.soma.animate.set_fill(GREEN,.9).set_stroke(GREEN),
                  blip.animate.move_to(pos(5.9,1.8)),run_time=.35)
        self.play(cell.soma.animate.set_fill(GREEN,.3),FadeOut(blip),run_time=.4)
        self.finish()


class S05N(SpokenScene):
    def construct(self):
        axes,ticks,glow=record()
        self.add(axes,glow.copy().set_stroke(opacity=.22))
        self.at('spike ticks')
        self.play(Create(ticks),run_time=.5)
        self.at('the glow runs')
        self.play(Create(glow),run_time=.75,rate_func=linear)
        self.finish()


class S06N(SpokenScene):
    def construct(self):
        axes,ticks,glow=record();self.add(axes,ticks,glow)
        self.at('the answer key')
        self.play(axes[-1].animate.become(label('spikes = answer key',0,3.25,30,TEAL)),run_time=.35)
        links,marks=link_record(ticks,glow)
        self.at('how often')
        self.play(Create(links),FadeIn(marks),run_time=.65)
        self.finish()


class S07N(SpokenScene):
    def construct(self):
        axes,ticks,glow=record(x=-4.9,w=7.5)
        links,marks=link_record(ticks,glow)
        axes[-1].become(label('illustrative record',-1,3.25,26,GREY))
        g=gauge(4.6,'Detection rate',0,reading='0 of 3')
        self.add(axes,ticks,glow,links,marks,g)
        self.at('fraction of')
        # Each lit segment contains the computed bump and its matching answer-key tick.
        pts=np.array(glow.get_anchors())
        pairs=[]
        for i in (0,2):
            x=ticks[i].get_x(); use=pts[(pts[:,0]>=x)&(pts[:,0]<x+1)]
            pairs.append(VGroup(ticks[i].copy(),path(use[:,0],use[:,1],YELLOW,6),links[i].copy()).set_color(YELLOW))
        self.play(Create(pairs[0]),Transform(g,gauge(4.6,'Detection rate',1/3,reading='1 of 3')),run_time=.5)
        self.at('isolated single spikes')
        self.play(ticks[1].animate.set_color(GREY),marks[1].animate.become(label('missed',ticks[1].get_x()+.85,-.8,26,GREY)),run_time=.3)
        self.at('the light reveals')
        self.play(Create(pairs[1]),Transform(g,gauge(4.6,'Detection rate',2/3,reading='2 of 3')),run_time=.45)
        self.finish()


class S08N(SpokenScene):
    def construct(self):
        windows=window_row(); self.add(windows,label('spike-free test windows',0,3.35,32,TEAL))
        self.add(label('spikes',-5,2.35,26,TEAL),label('light',-5,.3,26,GREEN))
        self.at('fraction of')
        self.play(LaggedStart(*[Indicate(w[0],scale_factor=1.01) for w in windows],lag_ratio=.12),run_time=.65)
        self.at('light reports')
        self.play(windows[2][0].animate.set_stroke(RED,width=5),Indicate(windows[2][2],color=RED,scale_factor=1),run_time=.5)
        self.at('spike anyway')
        self.play(FadeIn(label('false positive · per spike-free window',0,-3.1,30,RED)),run_time=.3)
        self.finish()


class S09N(SpokenScene):
    def construct(self):
        noise=np.random.default_rng(12).poisson(100,100); scores=(noise-100)/10
        # Actual signal-window scores and noise-window scores share the threshold.
        signal=np.random.default_rng(3).poisson(130,100); sigscores=(signal-100)/10
        dots=VGroup(*[Dot(pos(-5.6+(i%10)*.65,2.7-(i//10)*.48),radius=.105,
                         color=RED if scores[i]>2.4 else GREY) for i in range(100)])
        rail=Line(pos(-4.6,-2.8),pos(4.6,-2.8),color=GREY,stroke_width=4)
        notch=Line(pos(2.7,-3.03),pos(2.7,-2.57),color=RED,stroke_width=5)
        knob=Dot(pos(2.7,-2.8),radius=.16,color=YELLOW)
        det=ValueTracker(sum(sigscores>2.4))
        count=always_redraw(lambda:label(str(int(det.get_value())),4,1.3,58,YELLOW))
        bar=always_redraw(lambda:Rectangle(width=2.4,height=max(.02,2.4*det.get_value()/100),fill_color=YELLOW,fill_opacity=.75,stroke_width=0).move_to(pos(4,-1.8+max(.02,2.4*det.get_value()/100)/2)))
        self.add(dots,rail,notch,knob,count,bar,label('spike-free windows',-2.6,3.4,30),
                 label('detections',4,2.8,30,YELLOW),label('illustrative scores',-2.6,-2.2,26,GREY),
                 label('lower threshold',-4.5,-3.4,26,GREY),label('higher threshold',4.5,-3.4,26,GREY),
                 label('1%',2.7,-2.25,26,RED))
        self.at('find more spikes')
        more=label('more detections',3.7,2.05,26,YELLOW)
        self.play(knob.animate.move_to(pos(-2.8,-2.8)),det.animate.set_value(sum(sigscores>.8)),FadeIn(more),run_time=.65)
        self.at('more false alarms')
        self.play(*[d.animate.set_color(RED if s>.8 else GREY) for d,s in zip(dots,scores)],run_time=.55)
        self.at('fix the false alarms')
        # Empirical top-one threshold: exactly one of the 100 spike-free scores exceeds it.
        threshold=(sorted(scores)[-1]+sorted(scores)[-2])/2
        self.play(knob.animate.move_to(pos(2.7,-2.8)),det.animate.set_value(sum(sigscores>threshold)),
                  *[d.animate.set_color(RED if s>threshold else GREY) for d,s in zip(dots,scores)],FadeOut(more),run_time=.55)
        self.at('at one')
        self.play(Transform(knob,Square(.3,color=YELLOW,fill_opacity=1).move_to(pos(2.7,-2.8))),run_time=.25)
        self.finish()


def condition_icons():
    mouse=VGroup(Ellipse(width=2.5,height=1.15,color=BLUE,fill_opacity=.25),
                 Circle(radius=.35,color=BLUE,fill_opacity=.2).move_to(pos(.8,.45)),
                 Arc(radius=.75,start_angle=-PI/2,angle=-PI,color=BLUE).shift(LEFT*1.2),
                 label('Zzz',.1,1,32,TEXT)).move_to(pos(-4.35,1.5))
    # Cartoon viral particle: an envelope with surface projections, no molecular detail.
    virus=VGroup(Circle(radius=.75,color=BLUE,fill_opacity=.22))
    for angle in np.linspace(0,TAU,12,endpoint=False):
        direction=pos(np.cos(angle),np.sin(angle))
        virus.add(Line(.75*direction,1.02*direction,color=BLUE,stroke_width=4),
                  Circle(radius=.09,color=BLUE,fill_opacity=1).move_to(1.02*direction))
    virus.add(label('virus',0,-1.45,28,BLUE))
    virus.move_to(pos(-4.35,-1.55))
    return mouse,virus


class S10N(SpokenScene):
    def construct(self):
        cell=neuron(r=2.4).move_to(pos(1.65,.15))
        lens=Circle(radius=2.75,color=GREY,stroke_width=6).move_to(pos(1.65,.15))
        handle=Line(pos(3.6,-1.8),pos(5,-3.2),color=GREY,stroke_width=10)
        mouse,virus=condition_icons();self.add(cell)
        self.at('best case')
        self.play(FadeIn(label('Best case',1.65,3.35,38)),FadeIn(mouse),run_time=.4)
        # The narration does not name mouse or virus; reveal on the study/conditions cues.
        self.at('and colleagues')
        self.play(FadeIn(virus),FadeIn(label('Chen and colleagues · 2013',0,-3.55,28,GREY)),run_time=.4)
        self.at('magnified view',lead=.65)
        self.play(Create(lens),Create(handle),cell.soma.animate.set_fill(GREEN,.3).set_stroke(GREEN),run_time=.65)
        self.finish()


class S11N(SpokenScene):
    def construct(self):
        def study_gauge(value=0,reading=''):
            g=gauge(0,'Single-spike detection',value,reading=reading,bottom=-1.2,height=4.2)
            for part in g[:3]: part.stretch(1.3,0)
            g[3].shift(RIGHT*.3)
            return g
        g=study_gauge()
        self.add(g,label('GCaMP6s',-3.8,1.3,38,GREEN),label('Chen · 2013',-3.8,2.5,28,GREY))
        conditions=VGroup(*[label(line,size=28) for line in
            ('Lightly anesthetized mice','Virus · high magnification','Nine cells')]).arrange(DOWN,buff=.22).move_to(pos(0,-2.8))
        self.add(conditions)
        self.at('revealed nearly every')
        self.play(Transform(g,study_gauge(.99,'99 ± 0.2%')),
                  FadeIn(label('1% false positives',3.8,1.3,28,RED)),run_time=.6)
        self.finish()


class S12N(SpokenScene):
    def construct(self):
        m=mosaic();cell=neuron(r=2).move_to(m[2]);self.add(cell)
        self.at('widen the field')
        # Surrounding cells move inward from the edge as the field zooms out.
        spread=m[1].copy().scale(2.8,about_point=m[2].get_center()).set_opacity(0)
        self.add(spread)
        self.play(cell.animate.scale(.25,about_point=m[2].get_center()),Transform(spread,m[1]),Create(m[0]),run_time=1.7)
        self.at('tiny part')
        self.play(ReplacementTransform(cell,m[2]),FadeIn(label('hundreds of cells',0,-2.7,34,BLUE)),run_time=.7)
        self.finish()


class S13N(SpokenScene):
    def construct(self):
        q=question_frame();m=mosaic();self.add(m)
        self.at('What happens')
        self.play(Transform(m,q[0]),Create(q[1]),FadeIn(q[2]),run_time=.45)
        self.finish()


class S14Pause(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(question_frame())
        center=pos(0,1.65)
        self.add(Circle(radius=.69,color=GREY,stroke_width=3).move_to(center))
        remaining=ValueTracker(1)
        arc=always_redraw(lambda:Arc(radius=.69,start_angle=PI/2,
            angle=-TAU*max(.00001,remaining.get_value()),color=TEAL,stroke_width=7)
            .move_arc_center_to(center))
        self.add(arc)
        self.play(remaining.animate.set_value(0),run_time=5,rate_func=linear)


class S15N(SpokenScene):
    def construct(self):
        # Hard cut clears the mosaic. Chen's 99% is the explicit reference.
        a=gauge(-3.5,'Chen',.99,reading='99%')
        b=gauge(3.5,'Huang',.99,reading='99%')
        self.add(a,b,label('1% false positives',0,-3.45,26,RED))
        self.at('It falls further')
        # Remove the old number before morphing the geometry; reveal the settled range.
        b[-1].set_opacity(0)
        target=gauge(3.5,'Huang',.4,.8,reading='~40–80%')
        target[-1].set_opacity(0)
        self.play(Transform(b,target),run_time=.8)
        self.play(b[-1].animate.set_opacity(1),run_time=.2)
        self.at('and colleagues')
        self.play(FadeIn(VGroup(label('Huang and colleagues',size=28,color=GREY),label('2021',size=28,color=GREY)).arrange(DOWN,buff=.25).move_to(pos(0,1.55))),run_time=.3)
        self.at('transgenic mice')
        self.play(FadeIn(label('transgenic mice',0,.2,28,BLUE)),run_time=.35)
        self.finish()


class S16N(SpokenScene):
    def construct(self):
        g=comparisons();self.add(g)
        heading=label('High magnification',0,1.1,28,GREY);self.add(heading)
        # The comparison gap branches to two separately attached condition tags.
        bracket=VGroup(Line(pos(-2.85,2.3),pos(-2,2.3),color=GREY),
                       Line(pos(-2,2.3),pos(-2,1.75),color=GREY),
                       Line(pos(-2,1.75),pos(2.7,1.75),color=GREY))
        title=label('Possible reasons',0,1.15,28,TEXT)
        left=bchip('weaker\nexpression',BLUE,28).move_to(pos(-1.35,-.5))
        right=bchip('more labelled\nneuropil',GREEN,28).move_to(pos(1.35,-1.7))
        self.at('authors proposed')
        self.play(FadeOut(heading),Create(bracket),FadeIn(title),run_time=.45)
        self.at('weaker expression')
        self.play(Create(Line(pos(-2,1.75),pos(-2,left.get_top()[1]+.12),color=BLUE)),FadeIn(left),run_time=.35)
        self.at('and more')
        self.play(Create(Line(pos(2.7,1.75),pos(2.7,right.get_top()[1]+.12),color=GREEN)),FadeIn(right),run_time=.4)
        self.finish()


class S17N(SpokenScene):
    def construct(self):
        g=comparisons(); self.add(g)
        self.at('made to mimic')
        self.play(FadeIn(label('Reduced pixels\nand frames',0,1.7,28,GREY)),
                  Transform(g[1],gauge(3.5,'Huang: tuned',.16,.43,reading='~16–43%')),run_time=.7)
        self.finish()


class S18N(SpokenScene):
    def construct(self):
        # Retain the wide-field result as a labelled ghost while returning to the
        # pre-reduction condition for the blind-inference comparison.
        g=comparisons(wide=False,blind=True)
        blind=gauge(4.4,'Blind inference',0,reading='')
        ghost=VGroup(DashedLine(pos(-.7,-2.25+5*.16),pos(.7,-2.25+5*.16),color=GREY),
                     DashedLine(pos(-.7,-2.25+5*.43),pos(.7,-2.25+5*.43),color=GREY))
        note=label('Wide-field\n~16–43%',-2.1,-.8,26,GREY)
        self.add(g,ghost,note,blind)
        self.at('without the answer key')
        self.play(FadeIn(label('no answer key',2.2,-1.1,26,GREY)),run_time=.3)
        self.at('often caught under')
        self.play(Transform(blind,gauge(4.4,'Blind inference',.08,reading='<10%')),run_time=.45)
        self.at('even before that')
        self.play(Transform(g[1],gauge(0,'Huang: tuned',.4,.8,reading='~40–80%')),
                  FadeIn(label('Before\nreduction',2.2,1.2,26,TEXT)),run_time=.45)
        self.bring_to_front(ghost)
        self.finish()


def field(x,wide=False):
    frame=Square(side_length=4.8,color=GREY).move_to(pos(x,.5))
    if wide:
        coords=[pos(x-2.1+c*.42,-1.6+r*.42) for r in range(11) for c in range(11)]
        coords=[p for p in coords if np.linalg.norm(p-pos(x,.5))>.08]
        cells=VGroup(*[Dot(p,radius=.045,color=BLUE) for p in coords])
        target=Dot(pos(x,.5),radius=.1,color=GREEN)
    else:
        cells=VGroup();target=neuron(GREEN,r=1).move_to(pos(x,.5))
    return VGroup(frame,cells,target)


def raster(x):
    points=[]
    for i,y in enumerate(np.linspace(2.8,-1.8,8)):
        ends=(x-2.25,x+2.25) if i%2==0 else (x+2.25,x-2.25)
        points.extend([pos(ends[0],y),pos(ends[1],y)])
    return VMobject().set_points_as_corners(points)


class S19N(SpokenScene):
    def construct(self):
        a=field(-3.35);b=field(3.35,True)
        self.add(a,b,label('small field',-3.35,3.4,30),label('wide field',3.35,3.4,30))
        photons=ValueTracker(0)
        ca=always_redraw(lambda:label(str(int(photons.get_value())), -3.35,-2.4,40,TEAL))
        cb=always_redraw(lambda:label(str(int(photons.get_value()/190)),3.35,-2.4,40,TEAL))
        self.add(ca,cb,label('photons, recorded cell',-3.35,-3,26,TEAL),
                 label('photons, recorded cell',3.35,-3,26,TEAL),label('Illustrative, not to scale · 1 second scan',0,-3.6,26,GREY))
        self.at('pointed to photons')
        self.play(a[2].animate.set_color(GREEN),run_time=.3)
        self.at('wider field spreads')
        s1=Dot(pos(-5.6,2.8),color=TEAL,radius=.1);s2=Dot(pos(1.1,2.8),color=TEAL,radius=.1)
        self.add(s1,s2)
        self.play(MoveAlongPath(s1,raster(-3.35)),MoveAlongPath(s2,raster(3.35)),
                  photons.animate.set_value(19000),run_time=2.5,rate_func=linear)
        self.finish()


class S20N(SpokenScene):
    def construct(self):
        ax=Axes(x_range=[0,4,1],y_range=[-.4,.5,.2],x_length=10.5,y_length=5.1,
                tips=False,axis_config={'color':GREY,'include_ticks':True}).move_to(pos(.4,-.25))
        n=ValueTracker(19000)
        t=np.linspace(0,4,401);expected=response(t,(1.3,))
        # Quantile coupling keeps a fixed random realization as photon budget falls.
        # Each state remains a Poisson sample, rather than an interpolated noise sketch.
        from scipy.stats import poisson
        u=np.random.default_rng(8).uniform(.001,.999,len(t))
        def plotted():
            photons=n.get_value();f=poisson.ppf(u,photons*(1+expected))/photons-1
            return VMobject(color=GREEN,stroke_width=3).set_points_as_corners([ax.c2p(ti,fi) for ti,fi in zip(t,f)])
        glow=always_redraw(plotted)
        counter=always_redraw(lambda:label(f'{int(n.get_value()):,} photons',3.9,3.3,30,TEAL))
        self.add(ax,glow,counter,label('ΔF/F0',-5.5,2.65,26,GREEN),label('time (s)',4.9,-3.25,26,GREY),
                 label('Illustrative simulation',-2.4,3.3,28,GREY))
        for val in (-.4,-.2,0,.2,.4):
            self.add(label(f'{val:g}',-5.35,ax.c2p(0,val)[1],26,GREY))
        marker=DashedLine(ax.c2p(1.3,.18),ax.c2p(2.7,.18),color=GREY)
        self.add(marker,label('one spike: +0.18',1.8,1.8,26,GREY))
        self.at('fewer photons',lead=0)
        self.play(n.animate.set_value(100),run_time=4.8,
                  rate_func=lambda a:(19000-19000*(100/19000)**a)/18900)
        self.finish()


class S21N(SpokenScene):
    def construct(self):
        self.add(label('Slow, isolated GCaMP6s transients',0,3.4,32,GREEN))
        self.add(RoundedRectangle(width=12,height=3.15,corner_radius=.15,color=GREY).move_to(pos(0,1.2)),
                 RoundedRectangle(width=12,height=2.65,corner_radius=.15,color=GREY).move_to(pos(0,-2)))
        rate=ValueTracker(158)
        fps=always_redraw(lambda:label(f'{int(rate.get_value())} frames/s',-3.5,2.15,38,TEAL))
        def ruler():
            steps=int(round(rate.get_value()/6))
            return VGroup(Line(pos(-5.5,.45),pos(-1.5,.45),color=GREY),
                *[Line(pos(x,.2),pos(x,.7),color=TEAL) for x in np.linspace(-5.5,-1.5,steps)])
        ticks=always_redraw(ruler)
        self.add(label('0',-5.5,-.05,26,GREY),label('0.16 s',-1.5,-.05,26,GREY))
        sampling_label=label('sampling in time',-3.5,1.15,26,GREY)
        self.add(fps,ticks,sampling_label,
                 label('equal photons / second',2.5,2.35,28,TEAL),label('signal / noise',2.5,1.65,28,TEAL))
        def meter(x,y,fraction):
            return VGroup(Rectangle(width=4.4,height=.55,color=GREY).move_to(pos(x,y)),
                          Rectangle(width=max(.01,4.2*fraction),height=.4,stroke_width=0,fill_color=TEAL,fill_opacity=.85)
                          .move_to(pos(x-2.1+max(.01,4.2*fraction)/2,y)),
                          label('0',x-2.1,y-.52,26,GREY),label('full',x+1.9,y-.52,26,GREY))
        self.add(meter(2.5,.75,1))
        photon=ValueTracker(19000)
        pc=always_redraw(lambda:label(f'{int(photon.get_value()):,} photons/s',-3.2,-1.8,34,TEAL))
        lowmeter=always_redraw(lambda:meter(2.5,-1.8,np.sqrt(photon.get_value()/19000)))
        self.add(pc,lowmeter)
        photon_note=label('Fewer photons → weaker signal / noise',0,-2.9,28,TEAL)
        timing_note=label('timing resolution still changes',-3.5,1.15,24,TEAL)
        self.at('slower frame rate')
        # The counter steps through the range while the first S/N meter holds full.
        self.play(rate.animate.set_value(30),
                  ReplacementTransform(sampling_label,timing_note),
                  run_time=1.6,rate_func=linear)
        self.at('Frame rate still')
        self.play(Indicate(ticks,color=TEAL,scale_factor=1.02),run_time=.4)
        self.at('limits spike timing')
        self.play(photon.animate.set_value(100),FadeIn(photon_note),run_time=.8,rate_func=linear)
        self.finish()


class S22N(SpokenScene):
    def construct(self):
        box=RoundedRectangle(width=12,height=6.4,corner_radius=.2,color=YELLOW,stroke_width=4)
        text=VGroup(*[label(line,size=72) for line in ('A calibration belongs','to its conditions,','not to the sensor.')]).arrange(DOWN,buff=.5)
        self.add(box,text)
        self.at('a calibration belongs')
        self.play(Indicate(box,color=YELLOW,scale_factor=1.01),run_time=.5)
        self.finish()


class S23N(SpokenScene):
    def construct(self):
        self.add(label('Was it calibrated at your…',0,3,38,YELLOW))
        rows=VGroup(*[RoundedRectangle(width=11.8,height=1.65,corner_radius=.12,color=GREY)
                       .move_to(pos(0,1.55-i*2)) for i in range(3)])
        self.add(rows)
        # Begin the first row during the opening question; check it on its spoken words.
        self.at('turning glow')
        first=label('field of view',0,1.55,40,BLUE)
        self.play(FadeIn(first),run_time=.4)
        self.at('field of view')
        self.play(FadeIn(label('✓',-4.8,1.55,42,BLUE)),run_time=.3)
        self.at('expression level')
        self.play(FadeIn(label('✓   expression level',0,-.45,40,BLUE)),run_time=.3)
        self.at('and cell')
        self.play(FadeIn(label('✓   cell type',0,-2.45,40,BLUE)),run_time=.3)
        self.finish()


class S24N(SpokenScene):
    def construct(self):
        axes,ticks,glow=record(flat=True)
        axes[-1].become(label('population imaging · illustrative record',0,3.25,28,GREY))
        self.add(axes,glow)
        self.at('flat trace')
        self.play(Indicate(glow,color=GREEN,scale_factor=1),run_time=.4)
        self.at('One or a few spikes')
        ticks.set_opacity(.35)
        self.play(FadeIn(ticks),run_time=.65)
        self.finish()


class S25End(EndCard):
    LINE='A calibration belongs to its conditions, not to the sensor.'
    def construct(self):
        self.add(label('A calibration belongs\nto its conditions,\nnot to the sensor.',0,.3,48),
                 label('biochemistrypedia.com',0,-2.7,26,TEAL))
        self.wait(self.narration_s)
