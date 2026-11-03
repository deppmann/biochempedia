"""The Lock — chapter 4.
COLOR MAP (shared with scenes.old.py): BLUE = unchosen / different receptor gene;
RED = repression / unknown; GREEN = chosen gene / stable endpoint;
TEAL = enhancer hubs; ORANGE = receptor RNA / protein;
PURPLE = stress relay / feedback; GOLD = permanent lineage mark;
GREY = compartments / outlines. All geometry is schematic, not molecular.
The only data plot uses the narrated relative ratio: control=1, Adcy3-null≈2.
"""
import os
import numpy as np
from bp_style import *
PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


def head(s, color=TEXT):
    return T(s, 34, color).move_to([0, 3.15, 0])


def box(s, color=BLUE, w=2.5, h=1.0):
    label = T(s, 30, color)
    w = max(w, label.width + .45)
    return VGroup(RoundedRectangle(width=w, height=h, corner_radius=.14,
        stroke_color=color, fill_color=color, fill_opacity=.14), label)


def tile(color=BLUE, s=.8, op=.35):
    return RoundedRectangle(width=s,height=s,corner_radius=.08,color=color,
        fill_color=color,fill_opacity=op,stroke_width=3)


def arr(a,b,color=GREY,w=5):
    return Arrow(a,b,buff=.12,color=color,stroke_width=w,tip_length=.24,
        max_tip_length_to_length_ratio=.3)


def inhibit(a,b):
    a,b=np.array(a),np.array(b)
    d=(b-a)/np.linalg.norm(b-a); perp=np.array([-d[1],d[0],0])*.22
    return VGroup(Line(a,b,color=PURPLE,stroke_width=5),Line(b-perp,b+perp,color=PURPLE,stroke_width=6))


def padlock(opened=False):
    body=RoundedRectangle(width=2.3,height=1.8,corner_radius=.18,color=PURPLE,
        fill_color=PURPLE,fill_opacity=.22).shift(DOWN*.55)
    top=VGroup(Arc(radius=.72,start_angle=0,angle=PI,color=PURPLE,stroke_width=8),
        Line([-.72,0,0],[-.72,-.6,0],color=PURPLE,stroke_width=8),
        Line([.72,0,0],[.72,-.6,0],color=PURPLE,stroke_width=8)).shift(UP*.55)
    if opened: top.rotate(-.5,about_point=[-.72,-.05,0]).shift(UP*.35)
    hole=VGroup(Dot([0,-.35,0],radius=.12,color=BG),Line([0,-.35,0],[0,-.8,0],color=BG,stroke_width=7))
    return VGroup(body,top,hole)


def key():
    return VGroup(Circle(radius=.38,color=YELLOW,stroke_width=7).shift(LEFT*.8),
        Line([-.42,0,0],[1.1,0,0],color=YELLOW,stroke_width=7),
        Line([.7,0,0],[.7,-.35,0],color=YELLOW,stroke_width=7),
        Line([1.1,0,0],[1.1,-.35,0],color=YELLOW,stroke_width=7))


def alarm(on=True):
    c=PURPLE if on else GREY
    return VGroup(Triangle(color=c,fill_color=c,fill_opacity=.18).scale(.8),T("!",42,c))


def neuron(marked=False,different=False):
    outline=Circle(radius=2.1,color=GOLD if marked else GREY,stroke_width=7 if marked else 3,fill_color=GREY,fill_opacity=.05)
    stem=Line([0,-2.1,0],[0,-2.7,0],color=GREY,stroke_width=5)
    receptor=box("different receptor" if different else "MOR28",BLUE if different else GREEN,w=3.7)
    return VGroup(outline,stem,receptor)


def winner():
    nuc=Ellipse(width=11.8,height=5.0,color=GREY,fill_color=GREY,fill_opacity=.04).shift(DOWN*.25)
    hub=Circle(radius=1.2,color=TEAL,fill_color=TEAL,fill_opacity=.07).move_to([-3,.15,0])
    gene=tile(GREEN,1,.65).move_to(hub)
    rivals=VGroup(*[tile(BLUE,.85,.08).move_to([x,.2,0]) for x in [.1,2.1,4.1]])
    labels=VGroup(T("neuron",30,GREY).move_to([-4.2,-3,0]),T("hub",30,TEAL).move_to([-3,1.75,0]),
        T("winning gene",30,GREEN).move_to([-3,-1.4,0]),T("dimmed rival genes",30,GREY).move_to([2.1,-1.4,0]))
    return VGroup(nuc,hub,gene,rivals,labels)


def deletion(deleted=True):
    bar=VGroup(Rectangle(width=1.8,height=.85,color=GREEN).move_to([-4,1,0]),
        Rectangle(width=1.8,height=.85,color=GREEN).move_to([1.6,1,0]))
    coding=box("coding sequence",GREEN,w=3.8,h=.85).move_to([-1.2,1,0])
    if deleted: coding.shift(DOWN*1.7).fade(.6)
    slot=box("receptor protein: —",GREY,w=4.7).move_to([-2,-2,0])
    return VGroup(bar,coding,slot,T("?",110,PURPLE).move_to([4,-.8,0]),
        head("What will the neuron do?"),T("chosen gene",30,GREEN).move_to([-1.2,2,0]))


def second_choice():
    old=box("chosen gene",GREEN,w=3.4).move_to([-3.8,1,0]).fade(.6)
    no=T("no receptor protein",28,GREY).move_to([-3.8,-.3,0])
    lock=padlock(True).move_to([0,-.2,0])
    second=box("second gene",GREEN,w=3.3).move_to([3.8,1,0])
    protein=box("receptor protein",ORANGE,w=3.7).move_to([3.8,-1.6,0])
    return VGroup(old,no,lock,second,protein,arr(second.get_bottom(),protein.get_top(),ORANGE),
        head("Choose again",GREEN),arr(old.get_right(),lock.get_left()),arr(lock.get_right(),second.get_left()))


def snapshot():
    n=neuron().move_to([1.6,-.1,0])
    frame=Rectangle(width=5.2,height=5.2,color=GREY).move_to([1.6,-.1,0])
    ghost=box("earlier receptor?",GREY,w=3.8).move_to([-4,.3,0]).fade(.5)
    dotted=DashedVMobject(ghost[0],num_dashes=30); ghost[0].become(dotted)
    return VGroup(n,frame,head("How could you tell it had switched?"),ghost,T("?",86,PURPLE).move_to([-4,-1.5,0]))


def traced(different=False):
    return VGroup(neuron(True,different).move_to([0,-.1,0]),head("Permanent lineage mark",GOLD))


def er():
    chamber=RoundedRectangle(width=10.8,height=4.3,corner_radius=.45,color=GREY,fill_color=GREY,fill_opacity=.06).move_to([0,-.1,0])
    label=T("endoplasmic reticulum",32,GREY).move_to([0,2.6,0])
    proteins=VGroup(*[box("receptor",ORANGE,w=2.5,h=.9).move_to([x,y,0]) for x,y in [(-3,1),(0,.8),(3,1),(-1.7,-.8),(1.7,-.8)]])
    return VGroup(chamber,label,proteins,T("receptor protein piles up",30,ORANGE).move_to([0,-2.9,0]))


def order_chain(h=3.8):
    nodes=VGroup(*[box(s,PURPLE,w=2.45,h=h).move_to([x,.25,0]) for s,x in zip(["PERK","eIF2-alpha","ATF5","Adcy3"],[-4.8,-1.55,1.7,4.8])])
    arrows=VGroup(*[arr(nodes[i].get_right(),nodes[i+1].get_left(),PURPLE) for i in range(3)])
    return VGroup(nodes,arrows)


class S00Title(TitleCard):
    TITLE="The Lock"
    LESSON="One Receptor per Neuron: How Olfactory Neurons Choose"
    def construct(self):
        lesson=VGroup(T("One Receptor per Neuron:",30,GREY),T("How Olfactory Neurons Choose",30,GREY)).arrange(DOWN,buff=.18)
        g=VGroup(T("BIOCHEMISTRYPEDIA",26,TEAL),lesson,T(self.TITLE,64,font=TITLE_FONT),Line(LEFT*1.5,RIGHT*1.5,color=GOLD)).arrange(DOWN,buff=.5)
        self.play(FadeIn(g),run_time=.5); self.finish()

class S01(SpokenScene):
    def construct(self):
        w=winner(); self.add(w)
        self.at("one gene has"); self.play(Indicate(w[2],color=GREEN),run_time=.6)
        self.at("what keeps")
        self.play(FadeIn(VGroup(T("?",56,PURPLE),T("stable",32,PURPLE)).arrange(DOWN,buff=.1).move_to([0,2.9,0])),run_time=.4)
        self.finish()

class S02(SpokenScene):
    def construct(self):
        hubs=VGroup(*[VGroup(Circle(radius=1.55,color=TEAL,fill_color=TEAL,fill_opacity=.1),tile(GREEN,1,.6),T("hub",30,TEAL).shift(UP*2)).move_to([x,.1,0]) for x in [-4.1,0,4.1]])
        self.add(hubs,T("competing receptor genes",32,GREEN).move_to([0,-2.6,0]))
        self.at("competition helps"); self.play(hubs[0].animate.fade(.8),hubs[2].animate.fade(.8),hubs[1][1].animate.scale(1.3),run_time=1)
        self.at("holding the choice"); self.play(FadeIn(head("Holding the choice?",PURPLE)),run_time=.4); self.finish()

class S03(SpokenScene):
    def construct(self):
        g=box("winning gene",GREEN,w=3.8).move_to([-3.7,1.6,0]); lock=padlock(True).scale(1.35).move_to([3.6,0,0])
        self.add(g,lock)
        self.at("part of the answer"); self.play(Indicate(lock,color=PURPLE),run_time=.5)
        self.at("in the model"); self.play(FadeIn(head("Model",GREY)),run_time=.3)
        protein=box("receptor protein",ORANGE,w=4.1).move_to([-3.7,-1.5,0])
        self.at("the receptor"); self.play(FadeIn(protein),GrowArrow(arr(g.get_bottom(),protein.get_top(),ORANGE)),run_time=.5)
        self.at("closes it"); self.play(GrowArrow(arr(protein.get_right(),[3.6,-.7,0],PURPLE)),Transform(lock,padlock().scale(1.35).move_to(lock)),run_time=.8); self.finish()

class S04(SpokenScene):
    def construct(self):
        d=deletion(False); self.add(d[0],d[1],d[4],d[5])
        self.at("cannot make")
        self.play(d[1].animate.shift(DOWN*1.7).fade(.6),FadeIn(d[2]),FadeIn(d[3]),run_time=.7); self.finish()

class S05Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(deletion()); self.wait(5)

class S06(SpokenScene):
    def construct(self):
        c=second_choice(); self.add(c[0],c[1],c[2],T("Model",30,GREY).move_to([0,3.15,0]))
        self.at("choose again"); self.play(GrowArrow(c[7]),run_time=.4)
        self.at("express a second"); self.play(FadeIn(c[3]),FadeIn(c[4]),GrowArrow(c[5]),GrowArrow(c[8]),run_time=.7); self.finish()

class S07Beat(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(second_choice()); self.wait(2.5)

class S08(SpokenScene):
    def construct(self):
        self.add(head("Early working transgene",GREEN))
        genes=VGroup(*[tile(BLUE,1,.08).set_stroke(GREY).move_to([x,-2.1,0]) for x in [-3,0,3]])
        self.add(genes,T("own receptor genes",30,GREY).move_to([0,-3.1,0]))
        tg=box("transgene",GREEN,w=3).move_to([-4.2,1.2,0]); prot=box("receptor protein",ORANGE,w=4).move_to([.1,1.2,0]); lock=padlock(True).scale(.9).move_to([4.6,.7,0])
        self.at("given a working"); self.play(FadeIn(tg),run_time=.35)
        self.at("transgene"); self.play(FadeIn(prot),GrowArrow(arr(tg.get_right(),prot.get_left(),ORANGE)),FadeIn(lock),run_time=.5)
        self.at("early rarely"); self.play(Transform(lock,padlock().scale(.9).move_to(lock)),FadeIn(T("early → own genes stay dark",30,GREY).move_to([0,-.8,0])),run_time=.6); self.finish()

class S09(SpokenScene):
    def construct(self):
        p=box("receptor protein",ORANGE,w=4.5,h=2).move_to([-3.6,0,0]); lock=padlock().scale(1.5).move_to([3.3,0,0]); self.add(p,lock)
        self.at("depends on"); self.play(GrowArrow(arr(p.get_right(),lock.get_left(),PURPLE)),FadeIn(head("The lock depends on receptor protein",PURPLE)),run_time=.5); self.finish()

class S10(SpokenScene):
    def construct(self):
        title=T("Unfolded protein response",42,PURPLE).move_to([0,2,0]); self.add(title,alarm().scale(1.4).move_to([0,-.2,0]))
        self.at("dalton"); self.play(FadeIn(T("Dalton, Lyons and Lomvardas, 2013",30,GREY).move_to([0,-2.6,0])),run_time=.4)
        self.at("unfolded protein response"); self.play(Indicate(title,color=PURPLE),run_time=.6); self.finish()

class S11(SpokenScene):
    def construct(self):
        e=er(); self.add(e[0],e[1],e[2][0])
        self.at("misfolded protein"); self.play(LaggedStart(*[FadeIn(p,shift=DOWN*.3) for p in e[2][1:]],lag_ratio=.15),FadeIn(e[3]),run_time=1); self.finish()

class S12(SpokenScene):
    def construct(self):
        e=er().scale(.68).move_to([-2,-.35,0])
        e[1].become(T("endoplasmic reticulum",30,GREY).move_to([-2,1.6,0]))
        e[3].become(T("receptor protein piles up",28,ORANGE).move_to([-2,-2.2,0]))
        for protein in e[2]:
            protein[1].become(T("receptor",26,ORANGE).move_to(protein))
        a=alarm().scale(1.3).move_to([4,.1,0]); self.add(e)
        self.at("is the alarm"); self.play(FadeIn(a),FadeIn(head("1  Alarm",PURPLE)),run_time=.4)
        link=arr(e[0].get_right(),a.get_left(),PURPLE)
        self.at("expression engages"); self.play(GrowArrow(link),FadeIn(T("?",52,GOLD).move_to([1.8,1,0])),FadeIn(T("how receptors trigger it is not shown",30,GOLD).move_to([0,-3,0])),run_time=.7); self.finish()

class S13(SpokenScene):
    def construct(self):
        perk=box("PERK",PURPLE,w=3.6,h=1.2).move_to([-3.9,1.4,0])
        eif=box("eIF2-alpha",PURPLE,w=3.8,h=1.2).move_to([3.3,1.4,0])
        link=arr(perk.get_right(),eif.get_left(),PURPLE,w=7)
        self.add(perk,eif,link,head("2  Relay",PURPLE))
        p=chip("phosphate",PURPLE,30).move_to([-.7,1.4,0])
        rows=VGroup()
        for y,label in [(-.65,"most messages: slowed"),(-2.35,"a few: favoured")]:
            line=Line([-4.8,y,0],[4.8,y,0],color=GREY,stroke_width=4)
            rib=Ellipse(width=1.5,height=.7,color=PURPLE,fill_color=PURPLE,fill_opacity=.3).move_to([-2.2,y,0])
            rows.add(VGroup(line,rib,T(label,30).move_to([0,y-.7,0])))
        # Tracks are visible from the opening, directly below the relay.
        rows.set_opacity(.45)
        self.add(rows,T("mRNA",28,GREY).move_to([-5.3,-.05,0]),T("ribosome",28,PURPLE).move_to([-2.2,-.05,0]))
        self.at("phosphorylation of"); self.play(FadeIn(p),run_time=.2)
        self.play(p.animate.move_to([.1,1.4,0]),run_time=.3)
        self.play(p.animate.move_to([.1,2.55,0]),run_time=.3)
        self.play(p.animate.move_to([3.3,2.55,0]),run_time=.3)
        self.at("slows most translation"); self.play(rows[0].animate.set_opacity(1),run_time=.3)
        self.play(rows[0][1].animate.shift(RIGHT*.25).fade(.6),run_time=.5)
        self.at("but favors"); self.play(rows[1].animate.set_opacity(1),run_time=.3); self.play(rows[1][1].animate.shift(RIGHT*4),run_time=.7)
        self.finish()

class S14(SpokenScene):
    def construct(self):
        line=Line([-5,0,0],[4,0,0],color=GREY,stroke_width=5); rib=Ellipse(width=2.8,height=1.8,color=PURPLE,fill_color=PURPLE,fill_opacity=.3).move_to([-2.6,0,0])
        rl=T("ribosome",32,PURPLE).move_to([-2.6,-1.6,0])
        self.add(line,rib,rl,head("2  Relay",PURPLE),T("mRNA",32,GREY).move_to([-4.5,.8,0]))
        self.at("one favored message"); self.play(rib.animate.shift(RIGHT*2),rl.animate.shift(RIGHT*2),run_time=.7)
        atf=box("ATF5",PURPLE,w=3,h=1.3).move_to([3,1.9,0])
        self.at("the transcription factor"); self.play(GrowArrow(arr(rib.get_top(),atf.get_left(),PURPLE)),FadeIn(atf,shift=UP*.6),run_time=.7); self.finish()

class S15(SpokenScene):
    def construct(self):
        nuc=Ellipse(width=7.4,height=4.7,color=GREY,fill_color=GREY,fill_opacity=.04).move_to([-1.8,-.3,0])
        gene=box("Adcy3 gene",GREY,w=3.5).move_to([-1.6,-.5,0]); atf=box("ATF5",PURPLE,w=2.3).move_to([-5,2.4,0])
        self.add(nuc,gene,atf,head("3  Order",PURPLE),T("nucleus",30,GREY).move_to([-2,-3,0]))
        self.at("turns on the gene"); self.play(atf.animate.move_to([-1.6,1.2,0]),run_time=.4)
        self.play(GrowArrow(arr([-1.6,.7,0],gene.get_top(),PURPLE)),Transform(gene,box("Adcy3 gene",GREEN,w=3.5).move_to(gene)),run_time=.4)
        rna=box("Adcy3 mRNA",ORANGE,w=3.5).move_to([3.7,-.4,0]); product=box("Adcy3",PURPLE,w=2.7).move_to([3.7,-2.1,0])
        self.at("for"); self.play(GrowArrow(arr(gene.get_right(),rna.get_left(),ORANGE)),FadeIn(rna),run_time=.3)
        self.play(FadeIn(product),GrowArrow(arr(rna.get_bottom(),product.get_top(),PURPLE)),FadeIn(T("adenylyl cyclase 3",28,PURPLE).move_to([3.7,-3.1,0])),run_time=.4); self.finish()

class S16(SpokenScene):
    def construct(self):
        gene=box("Adcy3 gene",GREEN,w=3.6).move_to([-3.7,1.2,0]); k=key().scale(1.3).move_to([3.4,-.2,0]); kl=T("Lsd1: candidate key",30,YELLOW).move_to([3.2,-1.7,0]); self.add(gene,k,head("4  Two effects",PURPLE),kl)
        protein=box("Adcy3",PURPLE,w=3.3).move_to([-3.7,-1.2,0])
        self.at("the cyclase helps"); self.play(FadeIn(protein),GrowArrow(arr(gene.get_bottom(),protein.get_top(),PURPLE)),run_time=.4)
        self.at("turn down"); self.play(Create(inhibit(protein.get_right(),[1.7,-.6,0])),k.animate.fade(.6),Transform(kl,T("Lsd1 turned down",30,YELLOW).move_to(kl)),FadeIn(T("helps turn down",30,PURPLE).move_to([0,-2.8,0])),run_time=.7); self.finish()

class S17(SpokenScene):
    def construct(self):
        cyclase=box("Adcy3",PURPLE,w=3.3).move_to([-3.7,-1.2,0]); k=key().scale(1.3).move_to([3.4,-.2,0]).fade(.6)
        a=alarm().scale(1.25).move_to([-3.7,1.2,0]); self.add(cyclase,k,a,head("4  Two effects",PURPLE),inhibit(cyclase.get_right(),[1.7,-.6,0]),T("helps",30,PURPLE).move_to([0,-1.4,0]),T("Lsd1 turned down",30,YELLOW).move_to([3.2,-1.7,0]))
        self.at("later escapes become unlikely"); self.play(FadeIn(T("later escapes unlikely",30,GREY).move_to([2.3,-2.8,0])),run_time=.4)
        self.at("relieves the stress"); self.play(Create(inhibit(cyclase.get_top(),[-3.7,.05,0])),run_time=.35)
        self.at("alarm switches itself off"); self.play(Transform(a,alarm(False).scale(.85).move_to(a).fade(.55)),run_time=1.5)
        self.add(Circle(radius=1.1,color=GREY).move_to(a)); self.finish(); self.wait(1.2)

class S18(SpokenScene):
    def construct(self):
        w=winner(); w[4].remove(w[4][0]); self.add(w)
        sleeves=VGroup(*[RoundedRectangle(width=1.2,height=1.2,corner_radius=.15,color=GREY).move_to(g) for g in w[3]])
        k=key().scale(.7).move_to([-3.4,-3.1,0]).fade(.6)
        self.add(sleeves,k,T("Lsd1 down",28,YELLOW).move_to([-.9,-3.1,0]))
        self.at("earlier silence"); self.play(FadeIn(head("Earlier silence (chromatin)",GREY)),run_time=.4)
        rna=chip("RNA",ORANGE,30).move_to([1.8,1.6,0])
        self.at("the rna step"); self.play(FadeIn(rna),GrowArrow(arr(w[2].get_right(),rna.get_left(),ORANGE)),run_time=.35)
        links=VGroup(*[arr(rna.get_bottom()+RIGHT*dx,g.get_top(),ORANGE,w=4) for dx,g in zip([-.7,0,.7],w[3])])
        self.at("quiets rivals"); self.play(*[GrowArrow(a) for a in links],*[g.animate.fade(.75) for g in w[3]],run_time=.7); self.finish(); self.wait(1.2)

class S19(SpokenScene):
    def construct(self):
        nodes=VGroup(*[box(name,PURPLE,w=width,h=1.3).move_to([x,.25,0])
            for name,width,x in [("PERK",2.3,-4.2),("eIF2-alpha",2.8,-.8),("ATF5",2.1,2.5),("Adcy3",2.1,5.5)]])
        links=VGroup(*[arr(nodes[i].get_right(),nodes[i+1].get_left(),PURPLE,w=8) for i in range(3)])
        self.add(nodes,links,head("Ordered by mutant experiments",GREY))
        stub=DashedLine([-6.65,.25,0],nodes[0].get_left()+LEFT*.12,color=PURPLE,stroke_width=6)
        stub.add_tip(tip_length=.2)
        self.at("they do not show"); self.play(Create(stub),FadeIn(T("?",46,GOLD).move_to([-6.05,.8,0])),FadeIn(T("Receptor → PERK trigger unresolved",30,GOLD).move_to([.6,-2.3,0])),run_time=.5); self.finish()

class S20(SpokenScene):
    def construct(self):
        cilium=RoundedRectangle(width=3,height=4.7,corner_radius=.7,color=GREY).move_to([-3.6,-.3,0]); cyclase=box("Adcy3",PURPLE,w=2.3).move_to([-3.6,-1.2,0])
        odors=VGroup(*[Dot([x,y,0],radius=.16,color=YELLOW) for x,y in [(-4.3,2.4),(-3.5,2.7),(-2.7,2.4)]])
        clabel=T("cilium",30,GREY).move_to([-3.6,-3,0])
        olabel=T("odour molecules",30,YELLOW).move_to([-3.6,3.2,0])
        panel=VGroup(cilium,cyclase,clabel,odors,olabel).shift(RIGHT*3.6)
        self.add(cilium,cyclase,clabel)
        self.at("carries odor signals"); self.play(FadeIn(odors),FadeIn(olabel),run_time=.35); self.play(odors.animate.shift(DOWN*.8),run_time=.5)
        lock=padlock().move_to([3.6,-.6,0]); p=box("receptor protein",ORANGE,w=4).move_to([3.6,2,0])
        cue=VGroup(T("no odour needed",30,GREY).move_to([3.6,-3.25,0]),
            DashedLine([1.2,-2.85,0],[6,-2.85,0],color=GREY,stroke_width=3))
        self.at("but in this model"); self.play(panel.animate.shift(LEFT*3.6),FadeIn(lock),FadeIn(p),FadeIn(cue),FadeIn(T("Model",30,GREY).move_to([3.6,-2.3,0])),run_time=.55)
        self.at("receptor protein sets"); self.play(GrowArrow(arr(p.get_bottom(),lock.get_top(),PURPLE)),run_time=.4)
        self.finish()

class S21(SpokenScene):
    def construct(self):
        s=snapshot(); self.add(s)
        self.at("only once"); self.play(Indicate(s[1]),run_time=.5)
        self.at("how could you tell"); self.play(Indicate(s[4],color=PURPLE),run_time=.5); self.finish()

class S22Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(snapshot()); self.wait(5)

class S23(SpokenScene):
    def construct(self):
        n=neuron().move_to([3.1,-.3,0]); locus=box("MOR28 locus active",GREEN,w=4.5).move_to([-3.6,1.4,0]); self.add(n,locus,head("Leave a permanent mark",GOLD))
        recomb=box("recombinase",GOLD,w=3.7).move_to([-3.6,-.7,0])
        self.at("a recombinase"); self.play(FadeIn(recomb),GrowArrow(arr(locus.get_bottom(),recomb.get_top(),GOLD)),run_time=.5)
        self.at("marks the neuron"); link=arr(recomb.get_right(),n[0].get_left(),GOLD); self.play(GrowArrow(link),run_time=.3)
        stamp=box("MARK",GOLD,w=2.7).move_to([-3.6,-2.25,0]); self.play(stamp.animate.move_to([3.1,1,0]),run_time=.45)
        self.play(n[0].animate.set_stroke(GOLD,width=7),FadeOut(stamp),run_time=.4); self.finish()

class S24Beat(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(traced()); self.wait(2.5)

class S25(SpokenScene):
    def construct(self):
        n=traced(); self.add(n)
        self.at("now expresses a different receptor"); self.play(Transform(n[0][2],box("different receptor",BLUE,w=3.9).move_to(n[0][2])),FadeIn(T("switched",40,BLUE).move_to([0,-3.2,0])),run_time=.55)
        self.at("has switched"); self.finish()

class S26(SpokenScene):
    def construct(self):
        self.add(head("Postnatal day 2",GREY))
        zero=-2.05; unit=1.85
        self.add(Line([-3.5,zero,0],[5.3,zero,0],color=GREY),Line([-3.5,zero,0],[-3.5,2.1,0],color=GREY))
        for v in [0,1,2]:
            y=zero+unit*v
            self.add(T(str(v),28,GREY).move_to([-3.9,y,0]),Line([-3.6,y,0],[-3.4,y,0],color=GREY))
        self.add(DashedLine([-3.5,zero+unit,0],[5.3,zero+unit,0],color=GREY),T("MOR28 lineage ratio\nsingly / doubly labelled",28,GREY).rotate(PI/2).move_to([-5.65,0,0]))
        bars=VGroup(*[Rectangle(width=1.65,height=unit*v,color=c,fill_color=c,fill_opacity=.7).move_to([x,zero+unit*v/2,0]) for x,v,c in [(-1.4,1,BLUE),(2.2,2,PURPLE)]])
        self.add(bars[0],T("control",30,BLUE).move_to([-1.4,-2.55,0]),T("Adcy3-null",30,PURPLE).move_to([2.2,-2.55,0]),T("control normalized to 1",28,GREY).move_to([.2,2.5,0]))
        self.add(T("singly labelled = switched; doubly labelled = held",28,GREY).move_to([0,-3.35,0]))
        self.at("the ratio of"); self.play(GrowFromEdge(bars[1],DOWN),run_time=.6)
        bracket=VGroup(Line([3.4,zero+unit,0],[3.4,zero+2*unit,0],color=PURPLE),Line([3.2,zero+unit,0],[3.6,zero+unit,0],color=PURPLE),Line([3.2,zero+2*unit,0],[3.6,zero+2*unit,0],color=PURPLE))
        self.at("about twice the control"); self.play(Create(bracket),FadeIn(T("2 vs 1\n(≈2×)",28,PURPLE).move_to([4.85,.7,0])),run_time=.4)
        self.finish()

class S27(SpokenScene):
    def construct(self):
        self.add(head("Less stable choice",PURPLE))
        rows=VGroup()
        for y,label in [(1.6,"normal"),(-.1,"slowed?"),(-1.8,"lost?")]:
            line=Arrow([-2.6,y,0],[5.1,y,0],buff=0,color=GREY,stroke_width=4)
            rows.add(VGroup(line,T(label,32,PURPLE if label!="normal" else GREY).move_to([-4.2,y,0])))
        normal=VGroup(Line([-.6,1.4,0],[-.6,1.8,0],color=GREY,stroke_width=6),T("step",28,GREY).move_to([-.6,2.15,0])); self.add(rows,normal,T("time →",28,GREY).move_to([4.6,-2.5,0]))
        self.at("was the cyclase"); late=VGroup(Line([3.4,-.3,0],[3.4,.1,0],color=PURPLE,stroke_width=6),T("step",28,PURPLE).move_to([3.4,.45,0])); self.play(FadeIn(late,shift=RIGHT),run_time=.5)
        self.at("or lost"); self.play(FadeIn(T("no step appears",30,GREY).move_to([1.2,-1.25,0])),FadeIn(T("?",60,GOLD).move_to([5.8,-.6,0])),run_time=.4)
        self.at("this ratio alone"); self.play(FadeIn(T("This ratio alone cannot tell",32,GREY).move_to([0,-3.2,0])),run_time=.4); self.finish()

class S28(SpokenScene):
    def construct(self):
        lock=padlock(True).scale(1.2).move_to([3.7,.1,0]); rna=box("RNA competition",ORANGE,w=4.5,h=2.4).move_to([-3.3,.1,0])
        self.add(lock,rna,head("Mechanism unresolved",GOLD),T("+",60,GREY).move_to([0,.1,0]),T("may still limit expression",32,GREY).move_to([0,-2.9,0]))
        self.at("a lock need not"); self.play(GrowArrow(arr([4.6,1.5,0],[5.8,2.1,0],PURPLE)),run_time=.5)
        self.at("such as the rna competition"); self.play(Indicate(rna,color=ORANGE),run_time=.5); self.finish()

class S30(SpokenScene):
    def construct(self):
        protein=box("receptor protein",ORANGE,w=4).move_to([-3.7,2.7,0])
        c=order_chain(h=2.3); c[0].set_y(.4); c[1].set_y(.4)
        trigger=DashedLine(protein.get_bottom(),c[0][0].get_top(),color=PURPLE,stroke_width=5)
        question=T("?",42,GOLD).move_to([-5.45,1.85,0])
        # The relay is already laid out as context; activate each link on the words.
        active=c.copy()
        c.fade(.7)
        self.add(protein,c,trigger,question)
        self.at("sets off"); self.play(Transform(c[0][0],active[0][0]),run_time=.25)
        self.at("a stress relay")
        for i in range(3): self.play(Transform(c[1][i],active[1][i]),Transform(c[0][i+1],active[0][i+1]),run_time=.25)
        k=key().move_to([.3,-1.9,0]).fade(.6); lab=T("Lsd1 down",30,YELLOW).move_to([.3,-2.7,0])
        self.at("turns down the key"); self.play(FadeIn(k),FadeIn(lab),Create(inhibit(c[0][3].get_bottom(),[1.65,-1.9,0])),run_time=.4)
        lock=padlock().scale(.8).move_to([-4.7,-2.1,0])
        self.at("helps lock in the winner"); self.play(FadeIn(lock),GrowArrow(arr(k.get_left(),lock.get_right(),PURPLE)),FadeIn(T("helps stabilize the choice",30,GREEN).move_to([1.5,-3.25,0])),run_time=.5); self.finish(); self.wait(1)

class S31End(EndCard):
    LINE="Receptor protein sets off a stress relay that turns down the key and helps lock in the winner."
    def construct(self):
        lines=VGroup(*[T(s,36,font=TITLE_FONT) for s in ["Receptor protein sets off a stress relay", "that turns down the key", "and helps lock in the winner."]]).arrange(DOWN,buff=.3)
        self.add(lines,T("biochemistrypedia.com",28,TEAL).move_to([0,-2.3,0])); self.finish()
