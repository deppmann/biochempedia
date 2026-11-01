"""Sensory Systems: Five Ways to Turn a Stimulus into a Current

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one colour per concept, whole film)
  YELLOW = tissue latency (the 40 microsecond delay across the sheet of hair cells)
  BLUE   = channel (the transduction channel, CALHM channels) and channel time constant
  PURPLE = molecular gain
  ORANGE = behavioural latency
  TEAL   = the 3 ms depolarizing pulse
  GREEN  = activation fraction reached (gauges)
  RED    = crossed out: not this, does not identify
  GREY   = cells, membranes, axes, de-emphasized
  TEXT   = labels
  New narration: YELLOW also marks stimuli; TEAL electrical excitation;
  GREEN current/output; PURPLE cascade enzymes/gain. Original palette retained.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


def hair_cell(s=1.0, chan=True):
    """A simple hair cell: body, three stereocilia in a staircase, two tip links, a channel chip on each link."""
    body = RoundedRectangle(corner_radius=0.3 * s, width=1.5 * s, height=1.7 * s, stroke_color=GREY,
                            stroke_width=3, fill_color=GREY, fill_opacity=0.2)
    top = body.get_top()
    xs, hs = [-0.4, 0.0, 0.4], [0.7, 1.1, 1.5]
    cil = VGroup(*[Line(top + RIGHT * x * s, top + RIGHT * x * s + UP * h * s, color=TEXT, stroke_width=5)
                   for x, h in zip(xs, hs)])
    links = VGroup(*[Line(top + RIGHT * xs[i] * s + UP * hs[i] * s,
                          top + RIGHT * xs[i + 1] * s + UP * (hs[i] + 0.22) * s, color=GREY, stroke_width=3)
                     for i in range(2)])
    chans = VGroup(*[RoundedRectangle(corner_radius=0.04, width=max(0.16, 0.24 * s), height=max(0.12, 0.17 * s),
                                      stroke_color=BLUE, stroke_width=2, fill_color=BLUE, fill_opacity=0.9
                                      ).move_to(l.get_center()) for l in links]) if chan else VGroup()
    bundle = VGroup(cil, links, chans)
    g = VGroup(body, bundle)
    g.body, g.bundle, g.chans, g.base = body, bundle, chans, top
    return g


def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def mapper(ox, oy, w, h, xmax, ymax):
    return lambda t, v: np.array([ox + w * t / xmax, oy + h * v / ymax, 0.0])


def trace(f, t0, t1, mp, color, n=140, width=5, dashed=False):
    pts = [mp(t, f(t)) for t in np.linspace(t0, t1, n)]
    m = VMobject(stroke_color=color, stroke_width=width)
    m.set_points_as_corners(pts)
    return DashedVMobject(m, num_dashes=40) if dashed else m


def span(x0, x1, y, color, tick=0.12, w=4):
    """a horizontal bracket from x0 to x1 at height y, with end ticks"""
    return VGroup(Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=w),
                  Line([x0, y - tick, 0], [x0, y + tick, 0], color=color, stroke_width=w),
                  Line([x1, y - tick, 0], [x1, y + tick, 0], color=color, stroke_width=w))


def card(title, body, color, icon):
    box = RoundedRectangle(corner_radius=0.2, width=6.1, height=2.45, stroke_color=color, stroke_width=3,
                           fill_color=color, fill_opacity=0.08)
    icon.move_to(box.get_left() + RIGHT * 1.15)
    t = T(title, 27, color, weight=BOLD, line_spacing=0.9)
    b = T(body, 23, TEXT, line_spacing=0.9)
    txt = VGroup(t, b).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    txt.move_to(box.get_center() + RIGHT * 0.95)
    g = VGroup(box, icon, txt)
    g.box = box
    return g


# Shared schematic pore: two blue walls and a movable gate, never a molecular structure.
def pore(x, y, name):
    walls = VGroup(*[RoundedRectangle(width=.26, height=1.0, corner_radius=.06,
                    color=BLUE, fill_opacity=.35).move_to([x+d,y,0]) for d in (-.42,.42)])
    gate = Line([x-.3,y,0], [x+.3,y,0], color=BLUE, stroke_width=7)
    label = T(name, 22, BLUE).move_to([x,y-1.0,0])
    g = VGroup(walls, gate, label)
    g.gate = gate
    return g


def flow(x, y):
    return Arrow([x,y+.8,0], [x,y-.65,0], color=GREEN, buff=0, stroke_width=5)


def arrow(a, b, color=GREY):
    return Arrow(a, b, color=color, buff=.12, stroke_width=4, tip_length=.18)


def heading(text):
    return T(text, 34, font=TITLE_FONT).move_to([0,3.15,0])


def chain(names, colors, y=1.0, size=24):
    nodes = VGroup(*[bchip(n,c,size) for n,c in zip(names,colors)]).arrange(RIGHT,buff=.65)
    nodes.move_to([0,y,0])
    links = VGroup(*[arrow(a.get_right(),b.get_left()) for a,b in zip(nodes,nodes[1:])])
    return VGroup(nodes,links)


class S00Title(TitleCard):
    LESSON = "Sensory systems"
    TITLE = "Five Ways to Turn a Stimulus\ninto a Current"


class S01Current(SpokenScene):
    def construct(self):
        main = chain(["stimulus", "channel current", "electrical signal"], [YELLOW,BLUE,TEAL], 1.7, 28)
        self.at("every sensory cell")
        self.play(FadeIn(main[0][0]), run_time=.5)
        self.at("ion channel current")
        self.play(GrowArrow(main[1][0]), FadeIn(main[0][1]), run_time=.6)
        self.at("electrical signal")
        self.play(GrowArrow(main[1][1]), FadeIn(main[0][2]), run_time=.6)
        self.at("but the machinery")
        puzzle=bchip("What connects stimulus to current?",TEXT,30).move_to([0,-.1,0])
        self.play(FadeIn(puzzle), run_time=.5)
        self.at("some roots couple")
        self.play(FadeOut(puzzle), main.animate.shift(UP*.6), run_time=.4)
        direct=chain(["stimulus", "pore opens"],[YELLOW,BLUE],.55)
        self.play(FadeIn(direct), run_time=.6)
        self.at("others insert enzymes")
        enzymes=chain(["receptor", "enzymes", "pore"],[BLUE,PURPLE,BLUE],-.8)
        self.play(ReplacementTransform(direct,enzymes), run_time=.7)
        self.at("or add an output channel")
        output=chain(["detection", "excitation", "output channel"],[YELLOW,TEAL,BLUE],-2.2)
        self.play(FadeIn(output), run_time=.7)
        self.at("comparing those roots")
        self.play(Indicate(output[0][0],color=YELLOW),Indicate(output[0][2],color=BLUE),run_time=.8)
        self.finish()


class S02Routes(SpokenScene):
    def construct(self):
        titles=[T(n,26,TEXT).move_to([x,2.9,0]) for x,n in zip((-4.35,0,4.35),('Hair cell','Insect smell','Free nerve ending'))]
        separators=VGroup(*[Line([x,-2.9,0],[x,2.5,0],color=GREY,stroke_opacity=.3) for x in (-2.2,2.2)])
        cell=hair_cell(.95).move_to([-4.35,.2,0])
        self.at("in a hair cell")
        self.play(FadeIn(titles[0]),FadeIn(cell),Create(separators),run_time=.6)
        self.at("bundle movement")
        pull=arrow([-5.3,1.7,0],[-3.5,1.7,0],YELLOW)
        self.play(GrowArrow(pull),cell.bundle.animate.rotate(-.22,about_point=cell.body.get_top()),run_time=.6)
        self.at("opens transduction channels")
        cur=flow(-4.35,-.2)
        self.play(Indicate(cell.chans,color=BLUE),GrowArrow(cur),run_time=.5)
        self.at("insect odorant receptors")
        insect=pore(0,.2,"OR / Orco complex")
        ligand=Dot([-.9,1.65,0],radius=.15,color=YELLOW)
        odor=T('odorant',22,YELLOW).move_to([0,2.0,0])
        self.play(FadeIn(titles[1]),FadeIn(insect),FadeIn(ligand),FadeIn(odor),run_time=.5)
        self.at("ligand gated channels")
        self.play(ligand.animate.move_to([-.55,.65,0]),insect.gate.animate.shift(RIGHT*.85),GrowArrow(flow(0,.2)),run_time=.6)
        self.at("in a free nerve ending")
        trp=pore(4.35,.2,'TRPV1')
        nerve=Line([3.3,-1.65,0],[5.5,-1.65,0],color=GREY,stroke_width=7)
        self.play(FadeIn(titles[2]),FadeIn(trp),Create(nerve),run_time=.5)
        self.at("senses heat")
        heat=T('heat',28,YELLOW).move_to([4.35,1.8,0])
        self.play(FadeIn(heat),trp.gate.animate.shift(RIGHT*.85),GrowArrow(flow(4.35,.2)),run_time=.6)
        self.at("same protein")
        self.play(Indicate(trp[0],color=BLUE),run_time=.6)
        self.finish()


class S03Cascade(SpokenScene):
    def construct(self):
        h=heading('Enzymes between receptor and pore')
        generic=chain(['receptor','enzymes','pore'],[BLUE,PURPLE,BLUE],.6,30)
        self.at("a g protein")
        self.play(FadeIn(h),FadeIn(generic),run_time=.7)
        self.at("in a rod")
        rod=chain(['light','rhodopsin','transducin','PDE6'],[YELLOW,BLUE,PURPLE,PURPLE],1.4,24)
        rodname=T('Rod',28,TEXT).move_to([0,2.35,0])
        self.play(FadeOut(generic),FadeIn(rod),FadeIn(rodname),run_time=.7)
        self.at("falling cyclic gmp")
        cg=bchip('cGMP ↓',PURPLE,28).move_to([-3.6,-.35,0])
        channel=pore(0,-.4,'CNG channels')
        channel.gate.shift(RIGHT*.85)
        current=flow(0,-.4)
        self.play(FadeIn(cg),FadeIn(channel),GrowArrow(current),run_time=.4)
        self.at("closes channels")
        self.play(channel.gate.animate.shift(LEFT*.85),FadeOut(current),run_time=.5)
        self.at("hyperpolarizes the cell")
        result=bchip('hyperpolarization',TEAL,26).move_to([3.9,-.4,0])
        self.play(FadeIn(result),run_time=.5)
        rodview=VGroup(rod,rodname,cg,channel,result)
        self.at("in a vertebrate olfactory neuron")
        olf=chain(['receptor','Golf','adenylyl cyclase III'],[BLUE,PURPLE,PURPLE],1.4,24)
        olfname=T('Vertebrate olfactory neuron',28,TEXT).move_to([0,2.35,0])
        newchannel=pore(0,-.4,'CNG channels')
        self.play(FadeOut(rodview),run_time=.3)
        self.play(FadeIn(olf),FadeIn(olfname),FadeIn(newchannel),run_time=.3)
        self.at("rising cyclic amp")
        ca=bchip('cAMP ↑',PURPLE,28).move_to([-3.6,-.35,0])
        self.play(FadeIn(ca),run_time=.4)
        self.at("opens channels")
        self.play(newchannel.gate.animate.shift(RIGHT*.85),GrowArrow(flow(0,-.4)),run_time=.5)
        self.at("depolarizes the cell")
        dep=bchip('depolarization',TEAL,26).move_to([3.9,-.4,0])
        self.play(FadeIn(dep),run_time=.4)
        self.at("cascades can amplify")
        self.play(FadeOut(Group(*[m for m in self.mobjects if m is not h])),run_time=.4)
        gain=VGroup(bchip('input',PURPLE,28),bchip('larger output',PURPLE,38)).arrange(RIGHT,buff=2).move_to([0,.8,0])
        link=arrow(gain[0].get_right(),gain[1].get_left(),PURPLE)
        self.play(FadeIn(gain),GrowArrow(link),run_time=.6)
        self.at("but gain varies")
        varies=T('Gain varies',28,PURPLE).move_to([0,-.4,0])
        self.play(FadeIn(varies),run_time=.4)
        self.at("amplification takes time")
        time=bchip('takes time',GREY,28).move_to([-2.7,-2,0])
        self.play(FadeIn(time),run_time=.4)
        self.at("also amplify noise")
        noise=bchip('noise grows too',PURPLE,28).move_to([2.5,-2,0])
        self.play(FadeIn(noise),run_time=.5)
        self.finish()


class S06Rule(SpokenScene):
    def construct(self):
        h=heading('What identifies the pore?')
        speed=bchip('Speed alone = proof?',GREY,32).move_to([0,.7,0])
        self.at("how do we identify")
        self.play(FadeIn(h),FadeIn(speed),run_time=.6)
        self.at("speed alone is not proof")
        cross=Cross(speed,stroke_color=RED,stroke_width=6)
        self.play(Create(cross),run_time=.5)
        self.at("look for the right location")
        self.play(FadeOut(speed),FadeOut(cross),run_time=.3)
        specs=[('location',[-4.3,1.2,0]),('loss of native current',[0,1.2,0]),('altered permeation',[4.3,1.2,0]),('sufficiency',[-2.4,-.5,0]),('compatible kinetics',[2.4,-.5,0])]
        cards=[bchip(n,BLUE,24).move_to(p) for n,p in specs]
        self.play(FadeIn(cards[0]),run_time=.4)
        self.at("loss of the native current")
        self.play(FadeIn(cards[1]),run_time=.4)
        self.at("mutations that change permeation")
        self.play(FadeIn(cards[2]),run_time=.4)
        self.at("sensitivity in a new system")
        self.play(FadeIn(cards[3]),run_time=.4)
        self.at("kinetics must fit")
        self.play(FadeIn(cards[4]),run_time=.4)
        converge=VGroup(*[arrow(c.get_bottom(),[0,-2.15,0],BLUE) for c in cards[3:]])
        conclusion=T('Converging evidence',28,TEXT).move_to([0,-2.6,0])
        self.play(Create(converge),FadeIn(conclusion),run_time=.5)
        self.at("in mouse hair cells")
        self.play(FadeOut(VGroup(*cards,converge,conclusion)),run_time=.3)
        cell=hair_cell(.85,chan=False).move_to([-4.6,-.2,0])
        native=T('Mouse hair cells\nTmc1 / Tmc2 absent',24,GREY).move_to([-4.6,-2.55,0])
        status=bchip('native current absent',GREY,26).move_to([.5,1.55,0])
        self.play(FadeIn(cell),FadeIn(native),FadeIn(status),run_time=.5)
        self.at("restoring altered tmc1")
        restored=bchip('cysteine-substituted TMC1',BLUE,24).move_to([.7,.2,0])
        self.play(FadeIn(restored),run_time=.4)
        self.play(restored.animate.move_to([.7,.8,0]),ReplacementTransform(status,bchip('native current restored',GREEN,26).move_to([.5,1.8,0])),run_time=.4)
        self.at("chemically modifying it")
        reagent=bchip('modifying reagent',YELLOW,24).move_to([.7,-.7,0])
        self.play(FadeIn(reagent),run_time=.4)
        self.at("changed permeation rapidly")
        altered=bchip('rapid, irreversible\npermeation change',BLUE,28).move_to([2,-2.1,0])
        self.play(reagent.animate.shift(UP*.5),FadeIn(altered),run_time=.6)
        self.at("strengthening the poor argument")
        self.play(Indicate(altered,color=BLUE),run_time=.6)
        self.finish()


class S04Channel(SpokenScene):
    def construct(self):
        h=heading('Detection → excitation → output')
        cell=RoundedRectangle(width=6.2,height=3.8,corner_radius=.4,color=GREY,fill_opacity=.12).move_to([-1.6,-.15,0])
        # Leave an opening in the membrane for the output-channel schematic.
        cell.add(Line([1.5,-.95,0],[1.5,.85,0],color=BG,stroke_width=7))
        name=T('Mouse type II taste cell',26,GREY).move_to([-1.6,-2.65,0])
        detection=bchip('sweet / bitter / umami',YELLOW,24).move_to([-2,1.05,0])
        gpcr=bchip('GPCR pathway',BLUE,24).move_to([-3,-.3,0])
        exc=bchip('excitable',TEAL,26).move_to([-.5,-.3,0])
        p=pore(1.5,-.3,'CALHM1/3')
        VGroup(p[0],p.gate).rotate(PI/2,about_point=[1.5,-.3,0])
        p[2].move_to([2.8,-1.15,0])
        aff=bchip('gustatory\nafferent',GREY,26).move_to([5,-.3,0])
        self.at("now separate detection from output")
        self.play(FadeIn(h),FadeIn(cell),FadeIn(name),run_time=.6)
        self.at("mouse type 2 taste cells")
        self.play(FadeIn(detection),run_time=.5)
        self.at("protein coupled receptors")
        self.play(FadeIn(gpcr),GrowArrow(arrow(detection.get_bottom(),gpcr.get_top())),FadeIn(exc),run_time=.6)
        self.at("they release")
        atp=bchip('ATP',GREEN,24).move_to([1.5,-.3,0])
        self.play(FadeIn(p),FadeIn(aff),p.gate.animate.shift(UP*.75),run_time=.5)
        self.play(FadeIn(atp),run_time=.3)
        self.play(atp.animate.move_to([3.25,-.3,0]),run_time=.9)
        self.at("instead of vesicles")
        channelnote=T('channel-mediated release',24,BLUE).move_to([3.8,-2.1,0])
        self.play(FadeIn(channelnote),run_time=.4)
        self.at("deleting")
        deletion=bchip('Calhm3 deletion',RED,28).move_to([0,2.25,0])
        self.play(FadeIn(deletion),FadeOut(atp),FadeOut(channelnote),
                  p[0].animate.set_opacity(.25),p.gate.animate.shift(DOWN*.75).set_opacity(.25),run_time=.5)
        self.at("abolished taste evoked")
        noout=T('no taste-evoked\nATP release',26,RED).move_to([3.9,-2.1,0])
        block=Cross(Square(side_length=.58).move_to([1.5,-.3,0]),stroke_color=RED,stroke_width=5)
        self.play(FadeIn(noout),Create(block),run_time=.5)
        self.at("leaving the cells excitable")
        self.play(Indicate(exc[1:],color=TEAL,scale_factor=1.03),run_time=.7)
        self.at("the cell could respond")
        self.play(Indicate(gpcr[1:],color=BLUE,scale_factor=1.03),Indicate(exc[1:],color=TEAL,scale_factor=1.03),run_time=.6)
        self.at("could not send the message")
        self.play(Indicate(noout,color=RED),run_time=.6)
        self.finish()


class S05Architecture(SpokenScene):
    def construct(self):
        h=heading('Which cell carries the signal?')
        self.at("finally ask")
        self.play(FadeIn(h),run_time=.5)
        neuron=Circle(radius=.5,color=GREY,fill_opacity=.2).move_to([-4.9,1.35,0])
        axon=Line([-4.4,1.35,0],[3.4,1.35,0],color=GREY,stroke_width=7)
        bulb=bchip('bulb',GREY,26).move_to([4.7,1.35,0])
        primary=T('Primary: olfactory neuron',26,GREY).move_to([-2,2.35,0])
        self.at("an olfactory neuron")
        self.play(FadeIn(neuron),FadeIn(primary),run_time=.4)
        self.at("its own axon")
        self.play(Create(axon),FadeIn(bulb),run_time=.6)
        pulse=Dot([-4.9,1.35,0],color=TEAL,radius=.13)
        self.play(FadeIn(pulse),run_time=.2)
        self.play(pulse.animate.move_to([3.4,1.35,0]),run_time=.8)
        self.at("hair cells and type 2 taste cells")
        hair=hair_cell(.48).move_to([-4.9,-1.2,0])
        hairname=T('hair cell',24,GREY).next_to(hair,UP,buff=.2)
        taste=bchip('type II\ntaste cell',GREY,24).move_to([-2.7,-1.2,0])
        secondary=T('Secondary receptor cells',26,GREY).move_to([0,-3.05,0])
        aff=bchip('separate afferent',GREY,26).move_to([3.7,-1.2,0])
        self.play(FadeIn(hair),FadeIn(hairname),FadeIn(taste),FadeIn(secondary),run_time=.5)
        self.at("pass the message")
        paths=VGroup(
            Arrow(hair.body.get_bottom(),aff.get_bottom(),path_arc=.5,
                  color=TEAL,buff=.12,stroke_width=4,tip_length=.18),
            arrow(taste.get_right(),aff.get_left(),TEAL))
        self.play(Create(paths),FadeIn(aff),run_time=.7)
        self.at("this is cell architecture")
        self.play(Indicate(primary,color=TEXT),Indicate(secondary,color=TEXT),run_time=.6)
        self.at("it is a different question")
        self.play(FadeOut(Group(*[m for m in self.mobjects if m is not h])),run_time=.4)
        q1=bchip('How does the stimulus change current?',BLUE,28).move_to([0,.9,0])
        q2=bchip('Which cell carries the signal?',TEAL,28).move_to([0,-1.3,0])
        self.play(FadeIn(q1),FadeIn(q2),run_time=.6)
        self.finish()


class S07End(EndCard):
    LINE = "Five Ways to Turn a Stimulus\ninto a Current"
