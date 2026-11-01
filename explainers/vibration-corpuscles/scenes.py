"""Vibration corpuscles: is the onion the filter?  (Biochemistrypedia Sensory Systems explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  INDIGO = outer core of the corpuscle (the onion layers, the capsule)
  TEAL   = inner core / lamellar cells (the cells that touch the terminal)
  YELLOW = the nerve ending (terminal) and its impulses (spikes); pale yellow = second afferent
  GREEN  = graded signal of the ending (generator potential, transduction current)
  ORANGE = the mechanical stimulus (press, tap, vibration)
  RED    = what is not shown / not supported
  GREY   = labels, axes, preparation tags
All traces are sketches ("in this sketch"); the only numbers on screen are the lesson's own.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
INDIGO = "#9B8CF2"
SKETCH = "in this sketch"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def corpuscle(n_outer=5):
    """A corpuscle drawn as labelled layers around a nerve ending (schematic, never to scale)."""
    outer = VGroup(*[Ellipse(width=4.0 - 0.42 * i, height=3.2 - 0.4 * i, stroke_color=INDIGO, stroke_width=3,
                             fill_color=INDIGO, fill_opacity=0.05) for i in range(n_outer)])
    inner = VGroup(Ellipse(width=1.9, height=1.3, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.08),
                   Ellipse(width=1.45, height=0.95, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.08))
    axon = Line(LEFT * 2.45, LEFT * 0.3, color=YELLOW, stroke_width=7)
    term = RoundedRectangle(corner_radius=0.13, width=0.9, height=0.26, stroke_color=YELLOW, stroke_width=3,
                            fill_color=YELLOW, fill_opacity=0.9).move_to(LEFT * 0.0)
    g = VGroup(outer, inner, axon, term)
    g.outer, g.inner, g.axon, g.term = outer, inner, axon, term
    return g


def place(g, x, y, s=0.85):
    g.scale(s).move_to([x, y, 0])
    return g


def spike(x, y, h=0.8, w=0.3, color=YELLOW, sw=5):
    pts = [[x - w, y, 0], [x - w / 3, y, 0], [x, y + h, 0], [x + w / 3, y - 0.12, 0], [x + w, y, 0]]
    m = VMobject(stroke_color=color, stroke_width=sw)
    m.set_points_as_corners(pts)
    return m


def poly(pts, color, sw=5):
    m = VMobject(stroke_color=color, stroke_width=sw)
    m.set_points_as_corners([[x, y, 0] for x, y in pts])
    return m


def tag(text, color=GREY, size=22):
    return T(text, size, color)


def fade_arrow(x, y_from, y_to, color=ORANGE, n=5, w=7):
    """a downward force arrow built from segments whose opacity falls off (force dissipated)."""
    ys = np.linspace(y_from, y_to, n + 1)
    segs = VGroup(*[Line([x, ys[i], 0], [x, ys[i + 1], 0], color=color, stroke_width=w,
                         stroke_opacity=max(0.1, 1 - 0.22 * i)) for i in range(n)])
    return segs


def press_arrow(x, y_from, y_to, color=ORANGE, w=8):
    return Arrow([x, y_from, 0], [x, y_to, 0], buff=0, color=color, stroke_width=w, tip_length=0.3,
                 max_tip_length_to_length_ratio=0.4)


def lead(a, b, color=GREY, w=2):
    return Line(a, b, color=color, stroke_width=w, stroke_opacity=0.8)


# Reused silhouettes and traces are schematics, not quantitative fits.
def wave(x0, x1, y, cycles=3, amp=0.25, color=ORANGE):
    return poly([(x, y + amp * np.sin(2 * np.pi * cycles * (x-x0)/(x1-x0)))
                 for x in np.linspace(x0, x1, 180)], color, 4)


def meissner():
    cells = VGroup(*[Ellipse(width=1.4, height=0.38, color=TEAL,
                             fill_color=TEAL, fill_opacity=0.13).move_to([0, y, 0])
                     for y in (-0.5, 0, 0.5)])
    nerve = poly([(-1.2,-0.7),(-0.45,-0.7),(-0.45,0.7),(0.2,0.7)], YELLOW)
    return VGroup(cells, nerve)


def mouse():
    body = Ellipse(width=1.3, height=0.65, color=GREY, fill_color=GREY, fill_opacity=0.25)
    head = Circle(radius=0.27, color=GREY).move_to([0.65,0.12,0])
    ear = Circle(radius=0.17, color=GREY).move_to([0.5,0.4,0])
    tail = ArcBetweenPoints([-0.65,0,0],[-1.3,0.3,0], angle=-0.7, color=GREY)
    feet = VGroup(*[Line([x,-0.2,0],[x+0.1,-0.45,0],color=GREY) for x in (-0.4,0.3)])
    return VGroup(body,head,ear,tail,feet)


def human():
    return VGroup(Circle(radius=0.22,color=GREY).move_to([0,0.65,0]),
                  poly([(0,0.4),(0,-0.2),(-0.35,-0.7)],GREY,4),
                  poly([(0,-0.2),(0.35,-0.7)],GREY,4),
                  poly([(-0.45,0.05),(0,0.25),(0.45,0.05)],GREY,4))


def monkey():
    head=Circle(radius=0.34,color=GREY,fill_color=GREY,fill_opacity=0.15)
    ears=VGroup(*[Circle(radius=0.16,color=GREY).move_to([x,0.05,0]) for x in (-0.42,0.42)])
    muzzle=Ellipse(width=0.4,height=0.25,color=GREY).move_to([0,-0.14,0])
    return VGroup(head,ears,muzzle)


def wrap_terminal(x=-2.8, y=0):
    top = Ellipse(width=3.8, height=0.9, color=TEAL, fill_color=TEAL, fill_opacity=0.15).move_to([x,y+1,0])
    bot = top.copy().move_to([x,y-1,0])
    term = RoundedRectangle(width=2.8,height=0.5,corner_radius=0.16,color=YELLOW,
                            fill_color=YELLOW,fill_opacity=0.3).move_to([x,y,0])
    axon = Line([x-2.6,y,0],[x-1.4,y,0],color=YELLOW,stroke_width=7)
    g = VGroup(top,bot,term,axon)
    g.top,g.bot,g.term,g.axon=top,bot,term,axon
    return g


def clear(scene):
    scene.play(*[FadeOut(m) for m in list(scene.mobjects)],run_time=0.4)


class S00Title(TitleCard):
    LESSON = "Meissner and Pacinian corpuscles"
    TITLE = "Is the Onion the Filter?"



class S01Two(SpokenScene):
    def construct(self):
        skin = RoundedRectangle(width=6,height=3.8,corner_radius=0.15,color=GREY,
                                fill_color=GREY,fill_opacity=0.07).move_to([-3.3,-0.3,0])
        finger = RoundedRectangle(width=2.1,height=0.65,corner_radius=0.3,color=ORANGE,
                                  fill_color=ORANGE,fill_opacity=0.2).move_to([-4.6,2.05,0])
        small = meissner().scale(0.65).move_to([-4.5,0.75,0])
        deep = place(corpuscle(),-2.7,-1.15,0.57)
        names = VGroup(T("Meissner",24,TEAL).move_to([-2.4,0.9,0]),
                       T("Pacinian",24,INDIGO).move_to([-4.9,-1.5,0]))
        self.at("Slide a fingertip")
        self.play(FadeIn(skin),FadeIn(finger),run_time=0.5)
        self.play(finger.animate.shift(RIGHT*1.2),run_time=0.8)
        self.at("buzzing phone")
        phone=RoundedRectangle(width=0.7,height=1.2,corner_radius=0.1,color=GREY).move_to([3.1,1.6,0])
        self.play(FadeIn(phone),Wiggle(finger,rotation_angle=0.04),run_time=0.6)
        self.at("Two kinds")
        self.play(FadeIn(small),FadeIn(deep),run_time=0.5)
        slow=wave(0.7,5.7,0.6,3)
        fast=wave(0.7,5.7,-0.7,12)
        self.at("report flutter")
        self.play(FadeIn(names[0]),Create(slow),Indicate(small,color=TEAL),run_time=0.8)
        self.at("report the fast")
        self.play(FadeIn(names[1]),Create(fast),Indicate(deep.inner,color=TEAL),run_time=0.8)
        self.at("Both fire")
        self.play(FadeOut(phone),FadeOut(slow),FadeOut(fast),run_time=0.3)
        press=poly([(0.7,1.6),(1.7,1.6),(1.7,2.1),(4.6,2.1),(4.6,1.6),(5.9,1.6)],ORANGE)
        trace=VGroup(Line([0.7,0,0],[5.9,0,0],color=GREY),spike(1.7,0),spike(4.6,0))
        labels=VGroup(T("steady press",24,ORANGE).move_to([3.2,2.65,0]),
                      tag(SKETCH).move_to([3.2,-1.1,0]))
        self.play(Create(press),Create(trace),FadeIn(labels),run_time=0.8)
        self.at("go quiet")
        quiet=T("quiet during the hold",24,GREY).move_to([3.2,-0.5,0])
        self.play(FadeIn(quiet),run_time=0.4)
        self.at("wrapped in cells")
        self.play(Indicate(deep.inner,color=TEAL),Indicate(small[0],color=TEAL),run_time=0.7)
        rule=T("two detectors of change",32,GOLD).move_to([0,-3.05,0])
        self.play(FadeIn(rule),run_time=0.5)
        self.finish()


class S02Flutter(SpokenScene):
    def construct(self):
        q=T("How do they split the work?",36,font=TITLE_FONT).move_to([0,2.8,0])
        self.at("How do we know")
        self.play(FadeIn(q),run_time=0.5)
        h=human().move_to([-5.5,1.1,0])
        study=T("1968 · Talbot, Mountcastle & colleagues",26,GREY).move_to([0,2.8,0])
        self.at("colleagues vibrated")
        self.play(ReplacementTransform(q,study),FadeIn(h),
                  FadeIn(T("human",22,GREY).move_to([-5.5,-0.5,0])),run_time=0.5)
        axis=Arrow([-4.5,-0.2,0],[6,-0.2,0],color=GREY,buff=0)
        xlabel=T("vibration frequency →",24,GREY).move_to([0,-0.75,0])
        # A schematic axis: the only numeric bands are those spoken in the narration.
        flutter=VGroup(Line([-4.1,0.45,0],[-0.8,0.45,0],color=ORANGE,stroke_width=14),
                       T("5–40 Hz · flutter",26,ORANGE).move_to([-2.45,1.05,0]))
        hum=VGroup(Line([0.7,0.45,0],[5.8,0.45,0],color=ORANGE,stroke_width=14),
                   T("~60–80 Hz upward · hum",26,ORANGE).move_to([3.3,1.05,0]))
        self.at("From about")
        self.play(Create(axis),FadeIn(xlabel),FadeIn(flutter),run_time=0.7)
        self.at("From around")
        self.play(FadeIn(hum),run_time=0.6)
        self.at("single nerve fibers")
        monkey_label=chip("monkey · nerve recording",GREY,24).move_to([0,-1.5,0])
        self.play(FadeIn(monkey_label),FadeIn(monkey().move_to([-5.3,-1.9,0])),run_time=0.5)
        a=VGroup(VGroup(Line([-4.4,-2.3,0],[-0.6,-2.3,0],color=GREY),*[spike(x,-2.3,h=0.45,w=0.14) for x in (-3.8,-2.5,-1.2)]),T("Meissner afferent",24,YELLOW).move_to([-2.5,-3.05,0]))
        b=VGroup(VGroup(Line([1,-2.3,0],[5.8,-2.3,0],color=GREY),*[spike(x,-2.3,h=0.45,w=0.1) for x in np.linspace(1.3,5.5,9)]),T("Pacinian afferent",24,YELLOW).move_to([3.4,-3.05,0]))
        self.at("Flutter matched")
        self.play(Create(a),run_time=0.7)
        self.at("The hum matched")
        self.play(Create(b),run_time=0.7)
        self.at("And in mice")
        clear(self)
        self.add(T("Sensitivity peaks differ by species",34,font=TITLE_FONT).move_to([0,2.8,0]))
        axes=VGroup(Arrow([-5,-2,0],[5.8,-2,0],color=GREY,buff=0),
                     T("frequency →",24,GREY).move_to([0,-2.65,0]),
                     tag("relative sensitivity · in this sketch").move_to([0,2,0]))
        c1=poly([(x,-2+2.4*np.exp(-((x+1.6)/1.2)**2)) for x in np.linspace(-5,5.5,140)],TEXT)
        c2=poly([(x,-2+2.4*np.exp(-((x-2.8)/1.2)**2)) for x in np.linspace(-5,5.5,140)],TEAL)
        icons=VGroup(human().scale(0.6).move_to([-1.6,1.1,0]),mouse().scale(0.6).move_to([2.8,1.1,0]),
                     T("human",24,TEXT).move_to([-3,0.8,0]),T("mouse",24,TEAL).move_to([4.4,0.8,0]))
        self.play(FadeIn(axes),Create(c1),FadeIn(icons),run_time=0.7)
        self.at("higher frequency")
        self.play(Create(c2),run_time=0.8)
        self.finish()


class S03Piezo(SpokenScene):
    def construct(self):
        head=T("Where force becomes current",36,font=TITLE_FONT).move_to([0,3,0])
        g=wrap_terminal(-1.5,0)
        self.at("Where does force")
        self.play(FadeIn(head),run_time=0.4)
        self.at("starts in the axon")
        self.play(FadeIn(g),FadeIn(chip("mouse",GREY,24).move_to([-5.5,2.7,0])),run_time=0.6)
        channels=VGroup(*[VGroup(Line([x-0.12,0.18,0],[x-0.12,0.55,0],color=GREEN,stroke_width=5),
                                  Line([x+0.12,0.18,0],[x+0.12,0.55,0],color=GREEN,stroke_width=5))
                           for x in (-2.3,-0.8)])
        name=T("Piezo2 · axon membrane",26,GREEN).move_to([2.9,1.7,0])
        self.at("A channel called")
        self.play(FadeIn(channels),FadeIn(name),run_time=0.6)
        links=VGroup(*[poly([(x,0.25),(x+0.25,0.55),(x+0.25,0.65)],YELLOW,3) for x in (-2.8,-1.4)])
        self.at("tiny protrusions")
        self.play(Create(links),run_time=0.6)
        self.at("tethered to the wrapping")
        self.play(Indicate(g.top,color=TEAL),run_time=0.5)
        # Reset the result whenever the deletion case changes.
        case=chip("axon Piezo2 absent",RED,24).move_to([2.8,-0.6,0])
        result=T("light touch almost lost",26,RED).move_to([2.8,-1.5,0])
        self.at("Without it")
        self.play(FadeIn(case),channels.animate.set_opacity(0.15),run_time=0.4)
        self.at("almost lost")
        self.play(FadeIn(result),run_time=0.4)
        case2=chip("wrapping-cell Piezo2 deleted",GREY,24).move_to([2.8,-0.6,0])
        self.at("Delete it from")
        self.play(ReplacementTransform(case,case2),FadeOut(result),channels.animate.set_opacity(1),run_time=0.4)
        result2=T("touch responses stay",26,GREEN).move_to([2.8,-1.5,0])
        self.at("touch responses stay")
        self.play(FadeIn(result2),run_time=0.4)
        self.at("A press stretches")
        force=press_arrow(-1.5,2.35,1.6)
        self.play(FadeOut(case2),FadeOut(result2),GrowArrow(force),g.term.animate.stretch(1.12,0),run_time=0.6)
        self.at("the channels open")
        self.play(*[c[0].animate.shift(LEFT*0.15) for c in channels],
                  *[c[1].animate.shift(RIGHT*0.15) for c in channels],run_time=0.4)
        current=Arrow([-0.8,0.85,0],[-0.8,-0.1,0],color=GREEN,buff=0)
        self.at("the current drives spikes")
        sp=VGroup(Line([1.2,-1.5,0],[5.8,-1.5,0],color=GREY),*[spike(x,-1.5) for x in (2,3,4)])
        self.play(GrowArrow(current),Create(sp),FadeIn(T("current → spikes",26,GREEN).move_to([3.2,-2.6,0])),run_time=0.7)
        self.finish()


class S04Cells(SpokenScene):
    def construct(self):
        g=wrap_terminal(-2.7,0)
        name=T("lamellar cells",28,TEAL).move_to([-2.7,-2.4,0])
        self.at("the wrapping cells")
        self.play(FadeIn(g),FadeIn(name),run_time=0.6)
        species=chip("duck",GREY,26).move_to([3.2,2.6,0])
        self.at("In duckbill corpuscles")
        self.play(FadeIn(species),run_time=0.4)
        force=press_arrow(-2.7,2.7,1.5)
        self.at("respond to force")
        self.play(GrowArrow(force),g.top.animate.set_fill(TEAL,0.5),run_time=0.5)
        self.at("depolarizing one")
        self.play(FadeOut(force),g.top.animate.set_fill(TEAL,0.85),run_time=0.5)
        sp=spike(2.8,0,h=1)
        base=Line([1.3,0,0],[5.5,0,0],color=GREY)
        self.at("nerve fiber fire")
        self.play(Create(base),Create(sp),run_time=0.5)
        self.at("In mice")
        self.play(ReplacementTransform(species,chip("mouse · Pacinian",GREY,26).move_to([3.2,2.6,0])),
                  FadeOut(sp),g.top.animate.set_fill(TEAL,0.15),run_time=0.4)
        self.at("on with light")
        light=VGroup(*[Line([-3.7+0.5*i,2.5,0],[-3.3+0.5*i,1.4,0],color=GOLD,stroke_width=4) for i in range(3)])
        self.play(Create(light),g.top.animate.set_fill(TEAL,0.85),run_time=0.5)
        self.at("drove the fiber")
        self.play(Create(sp),run_time=0.4)
        self.at("Switching them off")
        self.play(FadeOut(light),FadeOut(sp),FadeOut(base),g.top.animate.set_fill(TEAL,0.05),run_time=0.4)
        axis=Line([1.3,-2.2,0],[5.8,-2.2,0],color=GREY)
        bar=Rectangle(width=0.7,height=0.4,color=ORANGE,fill_color=ORANGE,fill_opacity=0.7).move_to([3.4,-2,0])
        lab=T("vibration threshold",26,ORANGE).move_to([3.4,0.9,0])
        self.play(Create(axis),FadeIn(bar),FadeIn(lab),run_time=0.4)
        self.at("five times harder")
        factor=T("~5×",30,ORANGE).move_to([4.6,-0.5,0])
        self.play(bar.animate.stretch(5,1,about_edge=DOWN),FadeIn(factor),run_time=0.7)
        self.at("How these cells signal")
        self.play(FadeOut(axis),FadeOut(bar),FadeOut(lab),FadeOut(factor),run_time=0.3)
        # The gap carries a question, rather than inventing a signaling route.
        question=T("?",24,GOLD).move_to([-2.7,0.4,0])
        unknown=T("cell → nerve: still unknown",28,GOLD).move_to([2.7,-1.7,0])
        self.play(FadeIn(question),FadeIn(unknown),run_time=0.5)
        self.finish()


class S05Brief(SpokenScene):
    def construct(self):
        c=place(corpuscle(),-3.7,-0.1,0.95)
        self.at("Why is the response")
        self.play(FadeIn(c),FadeIn(T("Why so brief?",36,font=TITLE_FONT).move_to([0,3,0])),run_time=0.6)
        self.at("the onion of layers")
        self.play(Indicate(c.outer,color=INDIGO),run_time=0.7)
        force=fade_arrow(-3.7,2.4,-0.1,n=6)
        self.at("soaks up slow presses")
        self.play(Create(force),FadeIn(T("classic mechanical filter",26,INDIGO).move_to([2.7,1.9,0])),run_time=0.7)
        self.at("stripped most layers")
        clear(self)
        self.add(c,chip("1965 · cat",GREY,24).move_to([-3.7,2.8,0]),tag(SKETCH).move_to([4.8,3,0]))
        self.play(*[FadeOut(e) for e in c.outer[1:]],c.outer[0].animate.set_stroke(opacity=0.3),run_time=0.8)
        x0,x1,a,b=-0.8,5.9,0.2,4.7
        potential=poly([(x,0.35+(0.9*np.exp(-(x-a)/6) if a<=x<b else 0)) for x in np.linspace(x0,x1,140)],GREEN)
        ref=poly([(x,0.35+(0.9*np.exp(-(x-a)/0.35) if x>=a else 0)) for x in np.linspace(x0,x1,140)],GREEN,2).set_opacity(0.4)
        labels=VGroup(T("generator potential",26,GREEN).move_to([2.7,1.8,0]),T("layers off",24,GREEN).move_to([3,-0.05,0]),
                      T("layers on",22,GREY).move_to([1,-0.4,0]))
        self.at("voltage then lasted longer")
        self.play(Create(ref),Create(potential),FadeIn(labels),run_time=0.8)
        caveat=T("mainly under intense compression",24,GREY).move_to([2.5,-0.8,0])
        self.at("mainly under intense compression")
        self.play(FadeIn(caveat),run_time=0.5)
        sp=VGroup(Line([x0,-2,0],[x1,-2,0],color=GREY),spike(a+0.2,-2))
        self.at("single spike")
        self.play(Create(sp),run_time=0.6)
        stages=VGroup(T("1  mechanics around the ending",24,INDIGO).move_to([-3.2,-3.1,0]),
                      T("2  spike-generating membrane",24,YELLOW).move_to([3.2,-3.1,0]))
        self.at("two stages")
        self.play(FadeIn(stages),run_time=0.6)
        self.at("In 2025")
        clear(self)
        d=place(corpuscle(),-3.7,-0.2,0.95)
        self.add(d,chip("duck, ex vivo",GREY,26).move_to([-3.7,2.8,0]),T("2025 · Herbst corpuscle",28,GREY).move_to([2.8,2.8,0]))
        self.at("removing the outer layers")
        self.play(*[FadeOut(e) for e in d.outer],run_time=0.7)
        self.at("fast current and tuning intact")
        cur=poly([(x,0.5-(1.5*np.exp(-(x-1.5)/0.25) if x>=1.5 else 0)) for x in np.linspace(0.4,5.8,150)],GREEN)
        self.play(Create(cur),FadeIn(T("fast current: stays",28,GREEN).move_to([3,1.5,0])),run_time=0.6)
        self.play(FadeIn(T("tuning: intact",28,TEXT).move_to([3,-1.6,0])),FadeIn(tag(SKETCH).move_to([3,-2.6,0])),run_time=0.5)
        self.finish()


class S06Meissner(SpokenScene):
    def construct(self):
        m=meissner().scale(1.9).move_to([-3.4,0.2,0])
        self.at("Mice nerve corpuscles")
        self.play(FadeIn(m),FadeIn(chip("mouse · Meissner",GREY,26).move_to([-3.4,2.8,0])),run_time=0.5)
        second=poly([(-5.6,-1.7),(-3.4,-1.7),(-3.4,1.3),(-2.7,1.3)],"#FFF1A6",4)
        self.at("two genetically different")
        self.play(Create(second),run_time=0.6)
        labels=VGroup(T("two distinct afferents",28,YELLOW).move_to([2.7,1.5,0]),
                      T("one more sensitive",28,TEXT).move_to([2.7,0.5,0]))
        self.at("one more sensitive")
        self.play(FadeIn(labels),Indicate(m[1],color=YELLOW),run_time=0.5)
        self.at("Mice that grew up")
        self.play(FadeOut(labels),run_time=0.3)
        title=T("touch threshold",28,ORANGE).move_to([2.9,1.9,0])
        bar=Rectangle(width=0.8,height=0.8,color=ORANGE,fill_color=ORANGE,fill_opacity=0.7).move_to([2.9,-1.8,0])
        baseline=Line([0.4,-2.2,0],[5.6,-2.2,0],color=GREY)
        label=T("without Meissner corpuscles",24,GREY).move_to([2.9,-2.8,0])
        self.play(FadeIn(title),FadeIn(bar),Create(baseline),FadeIn(label),run_time=0.4)
        self.at("twice the push")
        self.play(bar.animate.stretch(2,1,about_edge=DOWN),FadeIn(T("~2×",30,ORANGE).move_to([4.2,-1,0])),run_time=0.7)
        self.at("In freely moving mice")
        clear(self)
        branch=Line([-5.7,-0.8,0],[5.7,-0.8,0],color=GREY,stroke_width=12)
        animal=mouse().move_to([4.2,-0.3,0])
        heading=T("Pacinian neurons · freely moving mouse",30,font=TITLE_FONT).move_to([0,2.8,0])
        self.play(Create(branch),FadeIn(animal),FadeIn(heading),run_time=0.6)
        force=press_arrow(-4.8,1.1,-0.6)
        self.at("answered taps on a branch")
        self.play(GrowArrow(force),run_time=0.4)
        distance=VGroup(Line([-4.8,-1.7,0],[4.2,-1.7,0],color=GREY),T("2.5 m",28,GREY).move_to([-0.3,-2.2,0]))
        self.at("half meters away")
        self.play(FadeIn(distance),Create(wave(-4.5,3.4,-0.8,9,0.12)),
                  Create(VGroup(*[spike(x,0.8,h=0.6) for x in (3.5,4.2,4.9)])),run_time=0.7)
        self.at("Two detectors of change")
        clear(self)
        a=meissner().scale(1.25).move_to([-3.2,0,0])
        b=place(corpuscle(),3.2,0,0.8)
        names=VGroup(T("Meissner · flutter",28,TEAL).move_to([-3.2,2.1,0]),
                      T("Pacinian · vibration",28,INDIGO).move_to([3.2,2.1,0]),
                      T("two detectors of change",36,GOLD).move_to([0,3.1,0]))
        self.play(FadeIn(a),FadeIn(b),FadeIn(names),run_time=0.6)
        self.at("the cells that help")
        self.play(Indicate(a[0],color=TEAL),Indicate(b.inner,color=TEAL),
                  FadeIn(T("nerve ending + wrapping cells",30,TEXT).move_to([0,-2.8,0])),run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "In duck, without the outer core, the terminal still adapts fast."
