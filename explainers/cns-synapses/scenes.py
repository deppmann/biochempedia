"""Synapses in the brain: sufficient in a dish is not required in the animal  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = neuroligin (the protein on the kidney cell, the dendrite-side partner)
  BLUE   = neurexin (the axon-side partner, and the soluble neurexin that caps neuroligin)
  TEAL   = synaptic vesicles
  GREEN  = working / normal / function and maturation
  RED    = blocked / impaired / died
  GREY   = cells, axon, de-emphasized outlines
  GOLD   = the rule to keep (used once, in the last scene)
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

# ---------------------------------------------------------------------------------------------
# geometry of the dish: an axon (top bar) crossing kidney cells (bottom blobs)
# ---------------------------------------------------------------------------------------------
AX_Y, AX_H = 1.05, 0.7
CELL_TOP, CELL_H = 0.1, 2.9
CELL_Y = CELL_TOP - CELL_H / 2
XS = [1.3, 2.5, 3.7, 4.9]                   # stub positions over the neuroligin cell (centred on x = 3.1)
LEFT_K = range(0, 6)
RIGHT_K = range(6, 12)
SC = [(-5.6 + 1.018 * k, AX_Y + (0.13 if k % 2 == 0 else -0.13)) for k in range(12)]   # scattered vesicles
SC3 = [(0.7, 1.05), (1.9, 0.93), (3.1, 1.17), (4.3, 0.93), (5.5, 1.05), (2.5, 1.2)]
CL = [(2.8, 0.92), (3.1, 0.92), (3.4, 0.92), (2.8, 1.18), (3.1, 1.18), (3.4, 1.18)]   # clustered vesicles


def cell(x, w=5.4):
    return RoundedRectangle(corner_radius=0.45, width=w, height=CELL_H, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.22).move_to([x, CELL_Y, 0])


def axon(x0=-6.3, x1=6.3):
    return RoundedRectangle(corner_radius=0.3, width=x1 - x0, height=AX_H, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.12).move_to([(x0 + x1) / 2, AX_Y, 0])


def stub(x, color, yc, dx=0.0):
    return RoundedRectangle(corner_radius=0.07, width=0.3, height=0.3, stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=0.85).move_to([x + dx, yc, 0])


def stub_row(color, yc, xs=XS, dx=0.0):
    return VGroup(*[stub(x, color, yc, dx) for x in xs])


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def vdot(p):
    return Dot([p[0], p[1], 0], radius=0.12, color=TEAL)


def dashed_box(x, y, w=5.4, h=CELL_H, color=GREY):
    return DashedVMobject(RoundedRectangle(corner_radius=0.45, width=w, height=h, stroke_color=color, stroke_width=3),
                          num_dashes=60).move_to([x, y, 0])


def neuro_state():
    """cell + yellow stubs for the neuroligin cell at x = 3.1 and its labels."""
    c = cell(3.1)
    cl = T("kidney cell", 26, GREY).move_to([3.1, -2.3, 0])
    st = stub_row(YELLOW, 0.25)
    nl = T("neuroligin", 28, YELLOW).move_to([3.1, -0.8, 0])
    return c, cl, st, nl


# Additional conceptual colours: PURPLE = NMDA / glycine receptors;
# ORANGE = AMPA receptors; PINK = GABA-A receptors; WHITE = astrocyte signals.
PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#D98CB3"

_house_chip = chip


def chip(*args, **kwargs):
    """Keep membrane lines behind labels, with the original tinted chip above."""
    g = _house_chip(*args, **kwargs)
    back = RoundedRectangle(corner_radius=.14, width=g.width, height=g.height,
                            stroke_width=0, fill_color=BG, fill_opacity=1).move_to(g)
    return VGroup(back, g)


def membrane(y, x0=-5.8, x1=5.8):
    return RoundedRectangle(corner_radius=0.1, width=x1-x0, height=0.22,
                            stroke_color=GREY, fill_color=GREY, fill_opacity=0.25).move_to([(x0+x1)/2, y, 0])


def receptor(x, y, color=ORANGE):
    # A schematic channel with an open cup; no molecular geometry.
    return VGroup(Line([x-.22,y+.3,0], [x-.22,y-.3,0], color=color, stroke_width=6),
                  Line([x+.22,y+.3,0], [x+.22,y-.3,0], color=color, stroke_width=6),
                  Line([x-.22,y-.3,0], [x+.22,y-.3,0], color=color, stroke_width=6))


def scaffold(x, y, w=2.2):
    return RoundedRectangle(corner_radius=.12, width=w, height=.3, stroke_color=GREY,
                            fill_color=GREY, fill_opacity=.5).move_to([x,y,0])


def heading(s):
    return fit(T(s, 32, TEXT, font=TITLE_FONT), max_w=12.6).move_to([0,3.1,0])


def terminal(x, y=1.1, w=3.0):
    a = axon(-w/2,w/2).move_to([x,y,0])
    ds = VGroup(*[vdot((x+dx,y+dy)) for dx,dy in [(-.3,.1),(0,.1),(.3,.1),(0,-.15)]])
    return VGroup(a, ds)


def bridge(x, upper=.75, lower=.25):
    return VGroup(stub(x,BLUE,upper),stub(x,YELLOW,lower),
                  Line([x,lower+.15,0],[x,upper-.15,0],color=GREY,stroke_width=3))


def trace(x, y, sign=1, color=GREEN, w=3.8):
    # Qualitative response sketch, intentionally no numerical axes or scale.
    return VMobject(color=color,stroke_width=4).set_points_as_corners(
        [[x,y,0],[x+w*.25,y,0],[x+w*.32,y+sign*.65,0],
         [x+w*.55,y+sign*.3,0],[x+w*.8,y,0],[x+w,y,0]])


class S00Title(TitleCard):
    LESSON = "Synapses in the brain"
    TITLE = "Building a Working Synapse"


class S01Assembly(SpokenScene):
    def construct(self):
        h = heading("Two sides, one aligned contact")
        pre = terminal(0,1.5,5)
        mem = membrane(-.2,-3.5,3.5)
        recs = VGroup(*[receptor(x,-.2,ORANGE) for x in [-.65,0,.65]])
        labels = VGroup(T("release apparatus",26,TEAL).move_to([0,2.35,0]),
                        T("receptors",26,ORANGE).move_to([0,-1.1,0]))
        self.at("a working synapse")
        self.play(FadeIn(h),FadeIn(pre),run_time=.6)
        self.at("lined up with")
        self.play(Create(mem),FadeIn(recs,shift=UP*.3),FadeIn(labels),run_time=.7)
        br = VGroup(bridge(-1.6,1,.15),bridge(1.6,1,.15))
        self.at("adhesion proteins")
        self.play(FadeIn(br),run_time=.6)
        self.at("organize both sides")
        self.play(Indicate(pre,color=BLUE),Indicate(recs,color=YELLOW),run_time=.7)
        self.at("each contact")
        self.play(FadeOut(VGroup(h,pre,mem,recs,labels,br)),run_time=.4)
        dend = membrane(-.3)
        dl = T("one dendrite",26,GREY).move_to([0,-2.65,0])
        left,right = terminal(-3,1.3),terminal(3,1.3)
        r1 = VGroup(*[receptor(x,-.3,ORANGE) for x in [-3.5,-3,-2.5]])
        r2 = VGroup(*[receptor(x,-.3,PINK) for x in [2.5,3,3.5]])
        names = VGroup(T("glutamate",28,ORANGE).move_to([-3,2.2,0]),
                       T("GABA",28,PINK).move_to([3,2.2,0]))
        self.play(Create(dend),FadeIn(left),FadeIn(right),FadeIn(dl),run_time=.7)
        self.at("glutamate and gaba")
        self.play(FadeIn(names),run_time=.6)
        bs = VGroup(bridge(-4,.8,.2),bridge(4,.8,.2))
        self.at("each with its own receptors")
        self.play(FadeIn(r1),FadeIn(r2),FadeIn(bs),run_time=.6)
        scs=VGroup(scaffold(-3,-1.05),scaffold(3,-1.05))
        scl=T("scaffolds",25,GREY).move_to([0,-1.65,0])
        self.at("scaffolds gather")
        self.play(FadeIn(scs,shift=UP*.2),FadeIn(scl),run_time=.6)
        astro=chip("astrocyte signals",TEXT,26).move_to([0,3.15,0])
        sig=VGroup(arr([-1.2,2.9,0],[-1.6,1.5,0],TEXT),arr([1.2,2.9,0],[1.6,1.5,0],TEXT))
        self.at("astrocytes add signals")
        self.play(FadeIn(astro),GrowArrow(sig[0]),GrowArrow(sig[1]),run_time=.7)
        self.finish()


class S01Kidney(SpokenScene):
    def construct(self):
        c,cl,st,nl=neuro_state()
        ax=axon()
        ns=stub_row(BLUE,.55)
        nxl=T("neurexin · axon",26,BLUE).move_to([3.1,1.9,0])
        h=heading("Culture experiment 1 · induce the sending side")
        self.at("sits on the axon")
        self.play(FadeIn(h),FadeIn(ax),FadeIn(ns),FadeIn(nxl),run_time=.6)
        self.at("its partner")
        self.play(FadeIn(st),FadeIn(nl),run_time=.6)
        self.at("a kidney cell")
        self.play(FadeIn(c),FadeIn(cl),run_time=.6)
        dots=VGroup(*[vdot(p) for p in SC3])
        self.at("axons touching it")
        self.play(FadeIn(dots),run_time=.4)
        self.at("gather vesicles")
        self.play(*[d.animate.move_to([*p,0]) for d,p in zip(dots,CL)],run_time=.65)
        self.at("release and retrieve")
        self.play(*[d.animate.shift(DOWN*.4) for d in dots[:3]],run_time=.4)
        self.play(*[d.animate.shift(UP*.4) for d in dots[:3]],run_time=.4)
        c0=cell(-3.1)
        c0l=T("control cell",26,GREY).move_to([-3.1,-2.3,0])
        no=T("no induced cluster",24,GREY).move_to([-3.1,-.8,0])
        scatter=VGroup(*[vdot(p) for p in SC[:5]])
        self.at("control cells")
        self.play(FadeIn(c0),FadeIn(c0l),FadeIn(no),FadeIn(scatter),run_time=.6)
        self.at("on a non")
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.4)
        h2=heading("Culture experiment 2 · induce the receiving side")
        c2=cell(0,w=6)
        c2l=T("non-neuronal cell",26,GREY).move_to([0,-2.3,0])
        nx=stub_row(BLUE,.25,xs=[-1.5,-.5,.5,1.5])
        nxl2=T("neurexin",28,BLUE).move_to([0,-.8,0])
        den=axon(-5.5,5.5)
        denl=T("contacting dendrite",26,GREY).move_to([0,1.95,0])
        self.play(FadeIn(h2),FadeIn(c2),FadeIn(c2l),FadeIn(nx),FadeIn(nxl2),FadeIn(den),FadeIn(denl),run_time=.6)
        clusters=VGroup(*[stub(x,PURPLE,1.1) for x in [-4,-2,2,4]])
        pl=T("postsynaptic proteins",26,PURPLE).move_to([0,2.55,0])
        self.at("cluster postsynaptic proteins")
        self.play(FadeIn(clusters),FadeIn(pl),run_time=.4)
        self.play(*[m.animate.move_to([x,1.1,0]) for m,x in zip(clusters,[-.6,-.2,.2,.6])],run_time=.7)
        self.at("organization runs both ways")
        self.play(Indicate(clusters,color=PURPLE),Indicate(nx,color=BLUE),run_time=.7)
        self.finish()


class S02Scaffold(SpokenScene):
    def construct(self):
        h=heading("The receiving side · excitatory contact")
        mem=membrane(.9)
        nl=chip("neuroligin",YELLOW,26).move_to([-4,.9,0])
        nm=chip("NMDA",PURPLE,26).move_to([-.8,.9,0])
        psd=chip("PSD-95",GREY,28).move_to([-2.4,-1.5,0])
        tails=VGroup(Line([-4,.5,0],[-4,-1.1,0],color=YELLOW),
                     Line([-.8,.5,0],[-.8,-1.1,0],color=PURPLE),
                     Line([-4,-1.1,0],[-.8,-1.1,0],color=GREY))
        self.at("on the receiving side")
        self.play(FadeIn(h),Create(mem),FadeIn(psd),run_time=.6)
        self.at("holds neuralgene")
        self.play(FadeIn(nl),FadeIn(nm),Create(tails),run_time=.7)
        am=chip("AMPA",ORANGE,26).move_to([4,-2,0])
        star=chip("stargazin",TEXT,24).move_to([4,-2.8,0])
        self.at("receptors reach this scaffold")
        self.play(FadeIn(am),FadeIn(star),run_time=.7)
        delivery=T("surface delivery",24,TEXT).move_to([3.8,2.05,0])
        self.at("brings them to the cell surface")
        self.play(am.animate.move_to([4,.9,0]),star.animate.move_to([4,-.1,0]),FadeIn(delivery),run_time=.9)
        tail=VGroup(Line([4,-.45,0],[4,-1.5,0],color=TEXT),Line([4,-1.5,0],psd.get_right(),color=TEXT))
        anchor=T("synaptic anchoring",24,TEXT).move_to([3.8,-2.4,0])
        self.at("its tail binds")
        self.play(Create(tail),FadeOut(delivery),FadeIn(anchor),run_time=.7)
        self.at("in stargazer cerebellar granule cells")
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.4)
        h2=heading("Stargazer · cerebellar granule cells")
        inset=RoundedRectangle(width=11.6,height=3.7,corner_radius=.2,stroke_color=GREY)
        nm_label=chip("NMDA response",PURPLE,28).move_to([-3,1,0])
        am_label=chip("AMPA response",ORANGE,28).move_to([3,1,0])
        yes=trace(-4.9,-.5,1,PURPLE)
        neutral=Line([1.1,-.5,0],[4.9,-.5,0],color=GREY,stroke_width=3)
        self.play(FadeIn(h2),Create(inset),FadeIn(nm_label),FadeIn(am_label),run_time=.6)
        self.at("keep nmdi responses")
        self.play(Create(yes),run_time=.6)
        no=T("absent",26,RED).move_to([3,-1.2,0])
        self.at("but lack mpa responses")
        self.play(Create(neutral),FadeIn(no),run_time=.6)
        self.at("inhibitory synapses")
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.4)
        hi=heading("The receiving side · inhibitory contact")
        mi=membrane(1)
        gly=chip("glycine receptors",PURPLE,26).move_to([-3,1,0])
        gab=chip("many GABA-A receptors",PINK,26).move_to([2.6,1,0])
        # An irregular filled patch, a schematic scaffold cluster.
        geo=Polygon([-4,-.8,0],[-2,-.5,0],[-.3,-.9,0],[2,-.55,0],[4,-.9,0],
                    [3.7,-1.4,0],[1,-1.25,0],[-1.5,-1.5,0],[-4,-1.3,0],
                    color=GREY,fill_opacity=.4)
        geol=T("gephyrin scaffold",28,GREY).move_to([0,-2.2,0])
        t=VGroup(Line([-3,.55,0],[-3,-.8,0],color=PURPLE),Line([2.6,.55,0],[2.6,-.8,0],color=PINK))
        self.play(FadeIn(hi),Create(mi),FadeIn(geo),FadeIn(geol),run_time=.6)
        self.at("anchor glycine receptors")
        self.play(FadeIn(gly),Create(t[0]),run_time=.6)
        self.at("and many gaba")
        self.play(FadeIn(gab),Create(t[1]),run_time=.6)
        self.finish()


class S03Astrocytes(SpokenScene):
    def construct(self):
        h=heading("Purified rat retinal ganglion cells")
        prep=T("culture experiment · glia-conditioned medium",25,GREY).move_to([0,2.4,0])
        cells=VGroup(*[Circle(.5,color=GREY,fill_opacity=.2).move_to([x,.4,0]) for x in [-3,3]])
        link=arr([-2.4,.4,0],[2.4,.4,0],GREY)
        activity=chip("little synaptic activity",GREY,27).move_to([0,-1,0])
        survival=chip("survival unchanged",TEXT,26).move_to([0,-2.3,0])
        self.at("astrocyte signals")
        self.play(FadeIn(h),run_time=.5)
        self.at("purified retinal ganglion cells")
        self.play(FadeIn(cells),run_time=.6)
        self.at("barely communicated")
        self.play(GrowArrow(link),FadeIn(activity),run_time=.6)
        med=chip("glial signals",TEXT,26).move_to([0,1.5,0])
        self.at("glial signals were added")
        self.play(FadeIn(med,shift=DOWN*.4),run_time=.7)
        self.at("conditioned medium increased transmission")
        active=chip("increased transmission",GREEN,27).move_to(activity)
        self.play(FadeIn(prep),ReplacementTransform(activity,active),link.animate.set_color(GREEN),run_time=.6)
        self.at("without increasing survival")
        self.play(FadeIn(survival),run_time=.5)
        self.at("induce synapses")
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.4)
        h2=heading("Separate factor experiments")
        factor=chip("thrombospondins",TEXT,28).move_to([0,2.1,0])
        pre=terminal(-2.6,.7,4)
        post=membrane(-.7,-4.6,-.6)
        structure=T("normal structure",26,GREEN).move_to([-2.6,-1.6,0])
        release=T("transmitter release",26,TEAL).move_to([-2.6,-2.4,0])
        response=chip("AMPA response",ORANGE,26).move_to([3,1,0])
        flat=Line([1.2,-.2,0],[4.8,-.2,0],color=GREY,stroke_width=4)
        absent=T("absent",27,RED).move_to([3,-1,0])
        self.play(FadeIn(h2),FadeIn(factor),FadeIn(pre),Create(post),run_time=.6)
        self.at("look normal")
        self.play(FadeIn(structure),run_time=.4)
        self.at("release transmitter")
        self.play(FadeIn(release),pre[1][0].animate.shift(DOWN*.8),run_time=.6)
        self.at("yet have no")
        self.play(FadeIn(response),Create(flat),FadeIn(absent),run_time=.6)
        gly=chip("glypicans 4 and 6",TEXT,28).move_to(factor)
        self.at("other astrocyte factors")
        self.play(ReplacementTransform(factor,gly),FadeOut(flat),FadeOut(absent),
                  FadeOut(structure),FadeOut(release),run_time=.6)
        receptors=VGroup(receptor(-3.1,-1.7),receptor(-2.1,-1.7))
        self.at("recruit mpa receptors")
        self.play(FadeIn(receptors),run_time=.4)
        self.play(receptors.animate.shift(UP),run_time=.6)
        response_trace=trace(1.2,-.2,1,ORANGE,3.6)
        responds=T("responds",27,GREEN).move_to([3,-1.4,0])
        self.at("make such synapses respond")
        self.play(Create(response_trace),FadeIn(responds),run_time=.7)
        self.finish()


# Original bar helper retained for the house drawing vocabulary.
def bar(x, h, color, base=-1.9, w=1.1):
    r=Rectangle(width=w,height=h,stroke_color=color,stroke_width=3,fill_color=color,fill_opacity=.45)
    return r.move_to([x,base+h/2,0])


class S05Knockout(SpokenScene):
    def construct(self):
        h=heading("Sufficiency in culture · requirement in the animal")
        self.at("now distinguish")
        self.play(FadeIn(h),run_time=.6)
        c=cell(-3.3,w=4.8)
        ax=axon(-5.7,-.9)
        st=stub_row(YELLOW,.25,xs=[-4.2,-3.3,-2.4])
        nl=T("neuroligin",26,YELLOW).move_to([-3.3,-.7,0])
        cl=T("kidney cell · culture",24,GREY).move_to([-3.3,-2.25,0])
        ds=VGroup(*[vdot((p[0]-6.4,p[1])) for p in CL])
        dish=VGroup(c,ax,st,nl,cl,ds)
        self.play(FadeIn(c),FadeIn(ax),FadeIn(cl),run_time=.7)
        self.at("sufficient to induce terminals")
        self.play(FadeIn(st),FadeIn(nl),FadeIn(ds),run_time=.7)
        ko=VGroup(T("Mice · brainstem",28,TEXT),T("neuroligins 1, 2 and 3 deleted",24,YELLOW)).arrange(DOWN,buff=.25).move_to([3.2,2,0])
        self.at("yet mice lacking")
        self.play(FadeIn(ko),run_time=.6)
        num=chip("synapse counts: normal",GREEN,25).move_to([3.2,.4,0])
        fn=chip("transmission: impaired",RED,25).move_to([3.2,-1,0])
        self.at("normal synapse numbers")
        self.play(FadeIn(num),run_time=.6)
        self.at("with impaired transmission")
        self.play(FadeIn(fn),run_time=.6)
        tests=T("tests induction",26,TEXT).move_to([-3.3,-3.1,0])
        self.at("the assay tests induction")
        self.play(FadeIn(tests),Indicate(ds,color=TEAL),run_time=.6)
        self.at("the deletion separates")
        self.play(Indicate(num,color=GREEN,scale_factor=1.05),Indicate(fn,color=RED,scale_factor=1.05),run_time=.7)
        self.at("normal counts do not mean")
        self.play(FadeOut(tests),run_time=.3)
        rule=T("Sufficient in a dish ≠ required in the animal",28,GOLD).move_to([0,-3.1,0])
        self.play(FadeIn(rule),run_time=.6)
        self.finish()


class S06Maturation(SpokenScene):
    def construct(self):
        h=heading("A synapse keeps changing")
        scope=T("Rodent hippocampal and cortical neurons",26,GREY).move_to([0,2.4,0])
        stage=chip("immature",TEXT,27).move_to([-3.3,1.3,0])
        chlor=chip("internal chloride: high",TEXT,26).move_to([-3.3,0,0])
        gaba=chip("GABA-A response",PINK,26).move_to([3,1.3,0])
        base=Line([.8,-.7,0],[5.2,-.7,0],color=GREY)
        tr=trace(.8,-.7,1,PINK,4.4)
        dep=T("depolarizing",28,PINK).move_to([3,-1.5,0])
        note=T("qualitative response traces",22,GREY).move_to([0,-3.25,0])
        self.at("finally a synapse")
        self.play(FadeIn(h),run_time=.5)
        self.at("in immature")
        self.play(FadeIn(scope),FadeIn(stage),run_time=.6)
        self.at("high internal chloride")
        self.play(FadeIn(chlor),FadeIn(gaba),Create(base),FadeIn(note),run_time=.6)
        self.at("makes gaba depolarize")
        self.play(Create(tr),FadeIn(dep),run_time=.6)
        kcc=chip("KCC2 ↑",TEXT,28).move_to([-3.3,1.3,0])
        low=chip("internal chloride: low",TEXT,26).move_to(chlor)
        self.at("as kcc2 rises")
        self.play(ReplacementTransform(stage,kcc),FadeOut(tr),FadeOut(dep),run_time=.6)
        self.at("internal chloride falls")
        self.play(ReplacementTransform(chlor,low),run_time=.6)
        hyper=T("hyperpolarizing",28,PINK).move_to([3,-2.05,0])
        tr2=trace(.8,-.7,-1,PINK,4.4)
        self.at("gaba hyperpolarizes")
        self.play(Create(tr2),FadeIn(hyper),run_time=.6)
        self.at("depolarizing does not always")
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.4)
        h2=heading("Depolarizing does not always mean exciting")
        inset=T("Shunting current · schematic",26,GREY).move_to([0,2.15,0])
        mem=membrane(.2,-5.4,5.4)
        chan=receptor(0,.2,PINK)
        lab=T("GABA-A channel",26,PINK).move_to([0,1.3,0])
        incoming=arr([-4,-1.6,0],[-.4,-1.6,0],TEXT)
        il=T("input current",24,TEXT).move_to([-3,-2.4,0])
        shunt=arr([0,-1.6,0],[0,.8,0],PINK)
        sl=T("current shunted",25,PINK).move_to([3,1,0])
        result=chip("can still inhibit",GREEN,28).move_to([3,-1.6,0])
        self.play(FadeIn(h2),FadeIn(inset),Create(mem),FadeIn(chan),FadeIn(lab),run_time=.6)
        self.at("can still inhibit")
        self.play(GrowArrow(incoming),FadeIn(il),FadeIn(result),run_time=.6)
        self.at("by shunting current")
        self.play(GrowArrow(shunt),FadeIn(sl),run_time=.7)
        self.finish()


class S07End(EndCard):
    LINE = "A working synapse needs release machinery lined up with the right receptors."
