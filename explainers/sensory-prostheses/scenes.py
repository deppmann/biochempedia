"""Sensory prostheses: a contact is not a channel  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = implant hardware: cochlear contacts, retinal electrodes, native implant resolution
  YELLOW = electric current and its fields (a model sketch, not a measurement)
  TEAL   = a channel (a band of frequency information)
  PURPLE = ganglion cells and their axons of passage
  GREEN  = a participant who met the endpoint
  ORANGE = zoom (implant plus a magnifier)
  RED    = serious events, and the "is not" sign
  TEXT   = what the person perceives (percepts), people in general
  GREY   = outlines, unassessed people, labels
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def contact(x, y, size=0.36, color=BLUE):
    return Square(side_length=size, stroke_color=color, stroke_width=3, fill_color=color,
                  fill_opacity=0.55).move_to([x, y, 0])


def poly(points, color, fill=0.0, w=3, fill_color=None):
    m = VMobject()
    m.set_points_as_corners([np.array([x, y, 0.0]) for x, y in points])
    m.set_stroke(color, w)
    m.set_fill(fill_color or color, fill)
    return m


def bell(c, base, amp, s, x0, x1, n=60):
    xs = np.linspace(x0, x1, n)
    return xs, base + amp * np.exp(-0.5 * ((xs - c) / s) ** 2)


class S00Title(TitleCard):
    LESSON = "Restoring senses: implants and prostheses"
    TITLE = "Which Neurons Get the Message"


# Additional schematics use the old contact, arrow and opaque-chip helpers.
def cell(x, y, color=PURPLE):
    soma = Circle(radius=0.22, color=color, fill_color=color, fill_opacity=0.5).move_to([x, y, 0])
    return VGroup(soma, Line([x + .22, y, 0], [x + 1.0, y, 0], color=color, stroke_width=3))


def goggles(x=0, y=0):
    lenses = VGroup(*[RoundedRectangle(width=1.0, height=.65, corner_radius=.18,
                        color=BLUE, fill_color=BLUE, fill_opacity=.15).move_to([x+d, y, 0]) for d in (-.65, .65)])
    return VGroup(lenses, Line([x-.15,y,0],[x+.15,y,0],color=BLUE))


def gripper(x, y):
    return VGroup(poly([(x-1.1,y+1.1),(x-.4,y+.4),(x,y)], BLUE, w=9),
                  poly([(x-.45,y-.55),(x-.45,y),(x+.45,y),(x+.45,y-.55)], BLUE, w=5))


class S01Question(SpokenScene):
    def construct(self):
        hair = VGroup(*[VGroup(Line([x,-.2,0],[x,.8,0],color=GREY,stroke_width=5),
                    Line([x-.18,.95,0],[x+.18,.55,0],color=RED),
                    Line([x-.18,.55,0],[x+.18,.95,0],color=RED)) for x in (-.7,0,.7)])
        hairs = VGroup(hair, T('damaged hair cells',26,GREY).move_to([0,-.8,0]))
        neurons = VGroup(*[cell(3.5,y) for y in (-.5,.5,1.5)])
        nl = T('surviving auditory\nneurons',26,PURPLE).move_to([4.2,-1.6,0])
        implant = bchip('cochlear\nimplant',BLUE,30).move_to([-4.6,.7,0])
        self.at('A cochlear implant')
        self.play(FadeIn(implant),FadeIn(hairs),FadeIn(neurons),FadeIn(nl),run_time=.7)
        bypass = poly([(-3.1,.7),(-2.5,2.2),(2.7,2.2),(3.3,1.5)],YELLOW,w=5)
        self.at('bypasses damaged')
        self.play(Create(bypass),run_time=.7)
        self.at('stimulates surviving')
        self.play(Indicate(neurons,color=YELLOW),run_time=.7)
        benefit = bchip('useful hearing',TEXT,32).move_to([0,-2.6,0])
        self.at('useful hearing')
        self.play(FadeIn(benefit),run_time=.6)
        speech = bchip('supports speech understanding',TEXT,30).move_to([0,-2.6,0])
        self.at('support speech understanding')
        self.play(ReplacementTransform(benefit,speech),run_time=.6)
        self.at('frequency map')
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.5)
        bar = RoundedRectangle(width=10.8,height=.8,corner_radius=.2,color=GREY,fill_opacity=.2).move_to([0,.5,0])
        contacts = VGroup(*[contact(x,.5,.55) for x in (-4.5,-2.7,-.9,.9,2.7,4.5)])
        heading = T('cochlear place map · schematic',30,GREY).move_to([0,2.8,0])
        self.play(FadeIn(bar),FadeIn(contacts),FadeIn(heading),run_time=.6)
        hi=T('basal contacts\nhigher frequency',30,TEAL).move_to([-3.7,-1.3,0])
        lo=T('apical contacts\nlower frequency',30,TEAL).move_to([3.7,-1.3,0])
        self.at('Higher frequencies')
        self.play(FadeIn(hi),Indicate(contacts[:3],color=TEAL),run_time=.7)
        self.at('lower ones')
        self.play(FadeIn(lo),Indicate(contacts[3:],color=TEAL),run_time=.7)
        q=T('Which neurons get which information?',34,TEXT).move_to([0,-3,0])
        self.at('Which neurons')
        self.play(FadeIn(q),run_time=.7)
        self.finish()


class S02Overlap(SpokenScene):
    def construct(self):
        xs=(-2,0,2)
        bar=RoundedRectangle(width=7,height=.7,corner_radius=.2,color=GREY).move_to([0,-1,0])
        cs=VGroup(*[contact(x,-1,.6) for x in xs])
        hard=T('contact = hardware',30,BLUE).move_to([0,-2,0])
        self.at('A contact')
        self.play(FadeIn(bar),FadeIn(cs),FadeIn(hard),run_time=.6)
        band=Rectangle(width=1.4,height=1.7,color=TEAL,fill_color=TEAL,fill_opacity=.15).move_to([0,1,0])
        bl=T('channel = a band of frequency information',28,TEAL).move_to([0,3.1,0])
        self.at('A channel')
        self.play(FadeIn(band),FadeIn(bl),run_time=.6)
        fields=VGroup()
        for x in xs:
            gx,gy=bell(x,-.65,2.9,1.3,x-2.2,x+2.2)
            pts=list(zip(gx,gy))+[(x+2.2,-.65),(x-2.2,-.65)]
            fields.add(poly(pts,YELLOW,.16,w=3))
        ns=VGroup(*[cell(x,1.2) for x in (-2.5,-.7,1.1)])
        self.at('Neighboring contacts')
        self.play(FadeOut(band),FadeOut(bl),FadeIn(fields),FadeIn(ns),run_time=.8)
        interaction=T('overlapping electric fields · schematic',28,YELLOW).move_to([0,3.1,0])
        self.at('overlapping electric fields')
        self.play(FadeIn(interaction),Indicate(ns,color=YELLOW),run_time=.8)
        self.at('So more contacts')
        neq=T('more contacts ≠ as many independent channels',28,TEXT).move_to([0,-3,0])
        self.play(FadeIn(neq),run_time=.6)
        self.at('which surviving neurons')
        self.play(ReplacementTransform(interaction,T('which neurons receive the signal?',30,PURPLE).move_to([0,3.1,0])),
                  Indicate(ns,color=YELLOW),run_time=.7)
        self.at('the pattern it carries')
        self.play(LaggedStart(*[Indicate(c,color=YELLOW) for c in cs],lag_ratio=.3),run_time=1.2)
        self.at('Electrode count alone')
        self.play(Indicate(neq,color=RED),run_time=.7)
        self.finish()


class S03Streak(SpokenScene):
    def construct(self):
        head=T('retina · schematic surface view',26,GREY).move_to([-3.2,3,0])
        panel=RoundedRectangle(width=3.8,height=4.4,corner_radius=.15,color=GREY,fill_color=GREY,fill_opacity=.12).move_to([4.3,.2,0])
        plab=T('percept drawing',26,TEXT).move_to([4.3,2.9,0])
        disk=Circle(radius=.45,color=GREY,fill_opacity=.3).move_to([.8,.2,0])
        dl=T('optic disk',24,GREY).move_to([.7,-.8,0])
        axons=VGroup(*[Line([-5.6,y,0],[.35,.2+(y-.2)*.15,0],color=PURPLE,stroke_width=3) for y in (1.7,1,.3,-.4,-1.1)])
        cells=VGroup(*[Circle(radius=.14,color=PURPLE,fill_color=PURPLE,fill_opacity=.7).move_to([-5.7,y,0]) for y in (1.7,1,.3,-.4,-1.1)])
        anatomy=VGroup(axons,cells,disk,dl)
        el=contact(-3.4,.3,.65)
        el_label=T('inner-surface electrode\nover ganglion-cell axons',24,BLUE).move_to([-3.2,-2.1,0])
        self.at('In the retina')
        self.play(FadeIn(head),FadeIn(panel),FadeIn(plab),run_time=.6)
        self.at('An electrode')
        self.play(FadeIn(anatomy),FadeIn(el),FadeIn(el_label),run_time=.8)
        dot=Circle(radius=.22,color=TEXT,fill_color=TEXT,fill_opacity=1).move_to([4.3,.6,0])
        expected=T('tempting expectation:\none dot',24,TEXT).move_to([4.3,-1.2,0])
        self.play(FadeIn(dot),FadeIn(expected),run_time=.6)
        self.at('elongated or distorted')
        streak=Ellipse(width=.6,height=2,color=TEXT,fill_color=TEXT,fill_opacity=1).rotate(-.4).move_to([4.3,.7,0])
        reported=T('reported:\nelongated / distorted',24,TEXT).move_to([4.3,-1.25,0])
        self.play(ReplacementTransform(dot,streak),ReplacementTransform(expected,reported),run_time=.8)
        self.at('An axon pathway model')
        model=T('model-supported explanation',28,PURPLE).move_to([0,-3.1,0])
        self.play(FadeIn(model),run_time=.6)
        self.play(LaggedStart(*[Indicate(a,color=YELLOW) for a in axons[1:4]],lag_ratio=.15),run_time=1.2)
        self.at('not a direct recording')
        self.play(ReplacementTransform(model,T('model-supported explanation · not recorded activity',25,GREY).move_to([0,-3.1,0])),run_time=.6)
        self.at('One electrode')
        self.play(ReplacementTransform(head,T('one electrode ≠ one pixel',28,TEXT).move_to([-3.2,3,0])),run_time=.7)
        self.finish()


class S04RetinalRoutes(SpokenScene):
    def construct(self):
        title=T('After photoreceptor loss: limited vision',32,TEXT).move_to([0,3.1,0])
        self.at('Retinal implants')
        self.play(FadeIn(title),run_time=.6)
        # The subretinal pixels are physically below the remaining network.
        pixels=VGroup(*[contact(x,-1.7,.55) for x in (-1,0,1)])
        pixel_label=T('PRIMA · subretinal photovoltaic pixels',26,BLUE).move_to([0,-2.6,0])
        retina=Line([-2.1,-1,0],[2.1,-1,0],color=GREY,stroke_width=5)
        bipolar=VGroup(*[VGroup(Line([x,-.7,0],[x,.4,0],color=PURPLE,stroke_width=3),
                       Circle(radius=.16,color=PURPLE,fill_opacity=.6).move_to([x,-.2,0])) for x in (-1,0,1)])
        network=VGroup(*[cell(x,1) for x in (-1,0,1)])
        labels=VGroup(T('bipolar cells',26,PURPLE).move_to([4,-.2,0]),T('remaining retinal\nnetwork',26,PURPLE).move_to([4,1.4,0]))
        self.at('In the PRIMA design')
        self.play(FadeIn(pixels),FadeIn(pixel_label),Create(retina),FadeIn(bipolar),FadeIn(network),FadeIn(labels),run_time=.7)
        camera=bchip('camera image\nprojected as NIR light',BLUE,24).move_to([-4.3,1,0])
        beam=arr([-3.3,.2,0],[-1.5,-1.6,0],ORANGE)
        self.at('projected near')
        self.play(FadeIn(camera),GrowArrow(beam),run_time=.7)
        current=VGroup(*[arr([x,-1.35,0],[x,-.5,0],YELLOW,w=3) for x in (-1,0,1)])
        self.at('current that stimulates')
        self.play(FadeOut(beam),FadeIn(current),Indicate(bipolar,color=YELLOW),run_time=.8)
        self.at('The signal then passes')
        self.play(FadeOut(camera),FadeOut(current),Indicate(network,color=YELLOW),run_time=.8)
        self.at('Early participants')
        self.play(*[FadeOut(m) for m in list(self.mobjects) if m is not title],run_time=.5)
        benefit=bchip('early participants\noptimal chip placement\nprosthetic acuity',TEXT,30).move_to([-3.1,.3,0])
        self.play(FadeIn(benefit),run_time=.6)
        risk=bchip('later trial\nserious device- or\nprocedure-related events',RED,28).move_to([3.2,.3,0])
        self.at('Later trial benefits')
        self.play(FadeIn(risk),run_time=.7)
        self.finish()


class S05Optogenetics(SpokenScene):
    def construct(self):
        cells=VGroup(*[cell(x,0) for x in (-1.8,0,1.8)])
        label=T('surviving retinal ganglion cells',28,PURPLE).move_to([0,-1.2,0])
        self.at('Optogenetics changes')
        self.play(FadeIn(cells),FadeIn(label),run_time=.6)
        vector=bchip('viral vector',BLUE,28).move_to([-4.6,2.1,0])
        self.at('A viral vector')
        self.play(FadeIn(vector),run_time=.5)
        badges=VGroup(*[Circle(radius=.1,color=ORANGE,fill_color=ORANGE,fill_opacity=1).move_to([x-.12,.16,0]) for x in (-1.8,0,1.8)])
        protein=T('light-sensitive protein',28,ORANGE).move_to([1.8,2.1,0])
        self.at('express a light')
        self.play(FadeIn(badges),FadeIn(protein),run_time=.7)
        scope=T('one adult · retinitis pigmentosa',28,GREY).move_to([0,3.2,0])
        self.at('In one adult')
        self.play(FadeOut(vector),FadeIn(scope),run_time=.6)
        gs=goggles(-4.3,0)
        light=VGroup(*[arr([-3.1,y,0],[-2,y,0],ORANGE,w=4) for y in (-.3,0,.3)])
        self.at('light from engineered goggles')
        self.play(FadeIn(gs),FadeIn(light),FadeOut(protein),run_time=.7)
        self.play(Indicate(badges,color=ORANGE),run_time=.6)
        self.at('With the treated eye')
        self.play(*[FadeOut(m) for m in list(self.mobjects) if m is not scope],run_time=.5)
        gs=goggles(0,1.3)
        state=T('treated eye + goggles',30,BLUE).move_to([0,2.3,0])
        objects=VGroup(Circle(radius=.3,color=TEXT),Square(side_length=.6,color=TEXT),Triangle(color=TEXT).scale(.35)).arrange(RIGHT,buff=1).move_to([0,-.5,0])
        self.play(FadeIn(gs),FadeIn(state),FadeIn(objects),run_time=.6)
        tasks=T('located · counted · touched objects',30,TEXT).move_to([0,-2,0])
        self.at('located counted and touched')
        self.play(FadeIn(tasks),Indicate(objects,color=ORANGE),run_time=.7)
        self.at('Without the goggles')
        neutral=T('treated eye · without goggles',30,GREY).move_to([0,2.3,0])
        self.play(FadeOut(tasks),FadeOut(gs),FadeOut(objects),ReplacementTransform(state,neutral),run_time=.5)
        failure=T('did not detect objects',34,TEXT).move_to([0,-.1,0])
        self.at('did not detect objects')
        self.play(FadeIn(failure),run_time=.6)
        self.at('This was partial')
        limitation=T('partial, goggle-dependent function\nin one person',30,ORANGE).move_to([0,-2.3,0])
        self.play(FadeIn(limitation),run_time=.7)
        self.finish()


class S06Touch(SpokenScene):
    def construct(self):
        title=T('Peripheral nerve interface · people with amputations',28,GREY).move_to([0,3.1,0])
        nerve=VGroup(*[Line([-5.6,y,0],[-2.4,y,0],color=PURPLE,stroke_width=4) for y in (.4,.7,1)])
        electrode=contact(-4,.7,.6)
        lab=T('residual peripheral nerve',26,PURPLE).move_to([-3.9,1.9,0])
        cortex=bchip('sensory cortex',PURPLE,28).move_to([3.6,.7,0])
        self.at('Touch can be written')
        self.play(FadeIn(title),FadeIn(nerve),FadeIn(electrode),FadeIn(lab),run_time=.6)
        self.at('or into sensory cortex')
        self.play(FadeIn(cortex),run_time=.6)
        self.at('Nerve stimulation')
        self.play(FadeOut(cortex),Indicate(electrode,color=YELLOW),run_time=.6)
        percept=bchip('phantom-hand\ntouch percept',TEXT,28).move_to([3.5,1,0])
        link=arr([-2.2,.7,0],[1.6,.7,0],YELLOW)
        self.at('phantom hand touch')
        self.play(GrowArrow(link),FadeIn(percept),run_time=.6)
        arm=gripper(0,-1.7)
        obj=Ellipse(width=.6,height=.9,color=TEXT).move_to([0,-2.3,0])
        objlabel=T('delicate object',24,TEXT).move_to([3,-2.3,0])
        self.at('handle delicate objects')
        self.play(FadeIn(arm),FadeIn(obj),FadeIn(objlabel),run_time=.6)
        self.play(arm.animate.shift(DOWN*.22),run_time=.6)
        self.at('In one man')
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.5)
        scope=T('separate example · one man with spinal cord injury',28,GREY).move_to([0,3.1,0])
        motor=bchip('motor cortex',PURPLE,28).move_to([-3.8,1.5,0])
        sensory=bchip('sensory cortex',PURPLE,28).move_to([-3.8,-1.2,0])
        arm=gripper(3.6,.3)
        arm_label=T('robotic arm',28,BLUE).move_to([3.5,2,0])
        self.play(FadeIn(scope),run_time=.6)
        self.at('motor cortex signals')
        drive=arr([-2,1.5,0],[2.4,.8,0],YELLOW)
        self.play(FadeIn(motor),FadeIn(arm),FadeIn(arm_label),GrowArrow(drive),run_time=.7)
        self.play(arm.animate.shift(DOWN*.4),run_time=.7)
        feedback=arr([3,-.6,0],[-2,-1.2,0],YELLOW)
        self.at('Stimulation of sensory cortex')
        self.play(FadeIn(sensory),GrowArrow(feedback),run_time=.7)
        self.at('supplied touch feedback')
        fb=T('touch feedback',26,YELLOW).move_to([.8,-1.7,0])
        self.play(FadeIn(fb),Indicate(sensory,color=YELLOW),run_time=.6)
        self.at('shortened his task time')
        result=T('shorter task time · one participant',30,TEXT).move_to([0,-3,0])
        self.play(FadeIn(result),run_time=.6)
        self.at('not a population effect')
        self.play(Indicate(scope,color=TEXT),run_time=.6)
        self.finish()


class S06Rule(SpokenScene):
    def construct(self):
        # Recall the four routes without suggesting a comparison of efficacy.
        cochlea=VGroup(*[contact(x,1.6,.4) for x in (-5.2,-4.6,-4)])
        retina=VGroup(cell(-1.7,1.6),contact(-1.4,.8,.35))
        gs=goggles(1.6,1.6)
        arm=gripper(5,1.3)
        recall=VGroup(cochlea,retina,gs,arm)
        labels=VGroup(*[T(t,24,c).move_to([x,2.9,0]) for t,x,c in [('place map',-4.6,TEAL),('retinal targets',-1.3,PURPLE),('goggles',1.6,BLUE),('arm + feedback',4.9,BLUE)]])
        self.at('The design rule')
        self.play(FadeIn(recall),FadeIn(labels),run_time=.7)
        code=bchip('task-relevant features\nof the natural neural code',TEAL,30).move_to([0,-.6,0])
        connections=VGroup(*[arr([x,.5,0],[x*.35,-.05,0],GREY,w=3) for x in (-4.6,-1.3,1.6,4.9)])
        self.at('features of the natural neural code')
        self.play(FadeIn(code),FadeIn(connections),run_time=.7)
        tests=T('test perception  →  test behaviour',32,TEXT).move_to([0,-2.3,0])
        self.at('then test perception')
        self.play(FadeIn(tests),run_time=.6)
        self.at('Biomimicry')
        self.play(FadeOut(connections),FadeOut(recall),FadeOut(labels),run_time=.4)
        strategy=T('Biomimicry: evidence-backed strategy',32,TEXT).move_to([0,2.2,0])
        self.play(FadeIn(strategy),run_time=.6)
        self.at('It is not a proven law')
        caveat=T('more exact copying ≠ guaranteed improvement',28,GREY).move_to([0,.8,0])
        self.play(FadeIn(caveat),run_time=.7)
        self.finish()


class S07End(EndCard):
    LINE = "Which neurons get which information? Test the percept. Test the behaviour."
