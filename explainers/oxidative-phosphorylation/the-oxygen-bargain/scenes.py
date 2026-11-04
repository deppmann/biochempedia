"""The Oxygen Bargain — a four-movement teaching film.

COLOR MAP (from the available parent scenes.py; scenes.old.py is absent):
YELLOW electrons/reduced carriers; BLUE protons/gradient; GREEN respiratory
pumps/chain; GREY non-pump II, oxidized carriers, membranes; TEAL ATP;
PURPLE donors; ORANGE oxygen; RED leaks/damage; GOLD title highlights.
Additional environmental pigments: RUST iron minerals, CYAN cyanobacteria,
AMBER archaeal host, PINK bacterial guest, VIOLET anaerobes.
The same map is documented here because TASK restricts edits to scenes.py.
No molecular structures: every chemical species is a labelled chip.
Landscapes and cell cartoons are illustration geometry, never data plots.
No invented deposit histogram or oxygen concentration curve is shown.
All energy ladders are explicitly ordinal schematics; no measured trace is invented.
"""
import numpy as np
from bp_style import *

ORANGE = "#F2A154"
PURPLE = "#B58CD9"
RUST = "#BA6144"
CYAN = "#48C9B0"
AMBER = "#E7B46B"
PINK = "#DB8DA7"
VIOLET = "#A18AB9"
UMBER = "#211A18"
LAB = "#170F1C"
WARM = "#231B29"


def Polyline(*points, **kwargs):
    return VMobject(**kwargs).set_points_as_corners([P3(p) for p in points])


def P3(p):
    return np.array([*p[:2], 0.0])


def arr(a, b, color=GREY, w=4):
    return Arrow(P3(a), P3(b), buff=0.08, color=color, stroke_width=w,
                 tip_length=0.16, max_tip_length_to_length_ratio=0.35)


def edot(p, r=0.105):
    return Dot(P3(p), radius=r, color=YELLOW)


def hdot(p, r=0.105):
    return Dot(P3(p), radius=r, color=BLUE)


def box(w, h, color, op=0.2, r=0.18, sw=3):
    return RoundedRectangle(width=w, height=h, corner_radius=r,
                            stroke_color=color, stroke_width=sw,
                            fill_color=color, fill_opacity=op)


def block(label, color, w=1.6, h=1.0, size=30):
    txt = T(label, max(26,size), color)
    b = box(max(w,txt.width+.5), max(h,txt.height+.4), color)
    return VGroup(b, txt.move_to(b))


# Wrap the shared chip helper: no molecular label below 26 pt.
_style_chip = chip
def chip(text, color=BLUE, size=28, pad=.22, fill_opacity=.16):
    return _style_chip(text,color,max(26,size),pad,fill_opacity)


def label(text, p=(0, 2.9), size=32, color=TEXT):
    t = T(text, size=max(26,size), color=color)
    # Text sizes stay >=22; long labels wrap explicitly, never shrink to fit.
    return t.move_to(P3(p))


def pigment(top, bottom):
    """Full-bleed background: 24 smoothly interpolated flat sky bands."""
    return VGroup(*[Rectangle(width=14.23, height=8/24 + .015,
        fill_color=interpolate_color(ManimColor(top), ManimColor(bottom), i/23),
        fill_opacity=1, stroke_width=0).move_to([0, 4-(i+.5)*8/24, 0]) for i in range(24)])


def glow(mob, color, n=3):
    halos = VGroup(*[mob.copy().set_fill(opacity=0).set_stroke(color,
        width=14+10*i, opacity=.025*(n-i)) for i in reversed(range(n))])
    return VGroup(halos, mob)


def landscape(clear=False, deep=False):
    sky = pigment("#16324B" if clear else "#302724", "#70ADBA" if clear else "#AB7647")
    sun = Circle(radius=.38, fill_color="#F0D69B", fill_opacity=.6, stroke_width=0).move_to([-4.7,2.3,0])
    sea = Rectangle(width=14.23, height=2.3, fill_color="#246A70" if clear else "#4B6157", fill_opacity=1, stroke_width=0).move_to([0,-.65,0])
    hills = Polygon([-7.12,-.3,0],[-7.12,.25,0],[-5.4,.6,0],[-4.5,.25,0],[-3.3,.9,0],[-2.6,.25,0],[1.2,-.3,0],fill_color="#343C3B",fill_opacity=1,stroke_width=0)
    land = Polygon([-7.12,-4,0],[-7.12,-1.4,0],[-4.5,-1.0,0],[-2.3,-1.6,0],[1.1,-1.3,0],[4,-.6,0],[7.12,-.85,0],[7.12,-4,0],fill_color="#222927" if clear else "#302D2B",fill_opacity=1,stroke_width=0)
    cone = Polygon([3,-1.1,0],[4.5,1.1,0],[4.8,.85,0],[5.1,1.1,0],[6.8,-1.1,0],fill_color="#222526",fill_opacity=1,stroke_width=0)
    plumes=VGroup(*[Ellipse(width=.75+.25*i,height=.4,fill_color=GREY,fill_opacity=.12,stroke_width=0).move_to([4.8-.12*i,1.25+.33*i,0]) for i in range(4)])
    mats=VGroup(*[Ellipse(width=1.4,height=.18,fill_color=CYAN,fill_opacity=.5,stroke_width=0).move_to([x,-1.3+.15*(i%2),0]) for i,x in enumerate([-4,-2.6,-1.1])]) if clear else VGroup()
    if deep:
        land=Rectangle(width=14.23,height=2.6,fill_color="#1C3034",fill_opacity=1,stroke_width=0).move_to([0,-2.7,0])
    texture=VGroup(*[Polygon([x-.26,y-.07,0],[x-.1,y+.13,0],[x+.3,y+.04,0],[x+.2,y-.12,0],fill_color="#57605A",fill_opacity=.32,stroke_width=0) for x,y in [(x,-2.1-.5*j+.13*np.sin(x)) for j in range(3) for x in np.arange(-6.2,6.4,.85)]])
    ripples=VGroup(*[Line([x,y,0],[x+.65,y,0],stroke_color=CYAN,stroke_opacity=.22,stroke_width=2) for x,y in [(-5,.05),(-3,-.45),(-1,-.7),(1,-.3),(2,-.85)]])
    return VGroup(sky,sun,sea,hills,cone,plumes,land,mats,texture,ripples)


def underwater():
    bg=pigment("#325F62","#17292E")
    floor=Polygon([-7.12,-4,0],[-7.12,-2.2,0],[-4,-2.5,0],[-1,-2.1,0],[3,-2.5,0],[7.12,-2.2,0],[7.12,-4,0],fill_color="#39353D",fill_opacity=1,stroke_width=0)
    return VGroup(bg,floor)


def cell(color=CYAN,w=4,h=2.4,membranes=False):
    outer=box(w,h,color,.15,r=min(.7,h/2-.01))
    inner=box(w-.25,h-.25,color,.04,r=min(.58,(h-.25)/2-.01))
    lines=VGroup()
    if membranes:
        for x in np.linspace(-w*.3,w*.3,4):
            lines.add(Polyline([x-.18,-h*.27,0],[x+.18,-h*.12,0],[x-.18,h*.05,0],[x+.18,h*.27,0],stroke_color=color,stroke_width=3))
    return VGroup(outer,inner,lines)


def microbes(color=VIOLET):
    return VGroup(*[cell(color,.55,.32).rotate((i%3-1)*.4).move_to([x,y,0]) for i,(x,y) in enumerate([(-4,-1.8),(-2.6,-2.4),(-1.1,-1.6),(.4,-2.3),(2,-1.6),(3.6,-2.2)])])


def mat():
    bg=underwater()
    # Nested half-ellipses make a literal layered cross-section, like an onion.
    mound=VGroup()
    for i in range(8):
        w=10-i*.95;h=3.6-i*.33
        dome=VMobject(stroke_color=CYAN,stroke_width=2,fill_color=CYAN if i%2 else "#245B59",fill_opacity=.7)
        pts=[[w/2*np.cos(a),-2.5+h*np.sin(a),0] for a in np.linspace(0,np.pi,64)]
        dome.set_points_as_corners(pts+[pts[0]])
        mound.add(dome)
    bubbles=VGroup(*[chip("O₂",ORANGE,26,pad=.13).move_to([x,y,0]) for x,y in [(-4,1.7),(0,2.1),(4,1.7)]])
    return VGroup(bg,mound,bubbles)


def bands():
    bg=pigment("#172F3A","#42382F")
    wall=VGroup(*[Polygon([-5.8,-2.4+.5*i,0],[-5.8,-1.93+.5*i,0],[5.6,-1.65+.5*i,0],[5.8,-2.12+.5*i,0],fill_color=RUST if i%2 else "#8A9294",fill_opacity=1,stroke_width=0) for i in range(10)])
    return VGroup(bg,wall)


def timeline():
    base=Line([-5.9,-1.8,0],[5.9,-1.8,0],color=GREY,stroke_width=5)
    ticks=VGroup()
    for age in [3.5,3,2.5,2,1.5,1]:
        x=tx(age)
        ticks.add(Line([x,-1.95,0],[x,-1.65,0],color=GREY),label(str(age),(x,-2.35),26,GREY))
    return VGroup(base,ticks,label("Billion years ago",(0,-3.1),28,GREY))


def tx(age):
    return -5.9+(3.5-age)/2.5*11.8


def goe_band():
    x1,x2=tx(2.4),tx(2.1)
    b=Rectangle(width=x2-x1,height=3.5,fill_color=BLUE,fill_opacity=.2,stroke_color=BLUE).move_to([(x1+x2)/2,-.05,0])
    return VGroup(b,label("Great Oxygenation Event",(-1,2.9),30,BLUE),label("2.4–2.1",((x1+x2)/2,-.6),26,BLUE),Line([(x1+x2)/2,2.5,0],[(x1+x2)/2,1.75,0],color=BLUE))


def host():
    body=Ellipse(width=6,height=4.7,fill_color=AMBER,fill_opacity=.1,stroke_color=AMBER,stroke_width=4)
    arms=VGroup(*[Polyline([-2.2,y,0],[-3.1,y+.35,0],[-3.7,y+.2,0],stroke_color=AMBER,stroke_width=5) for y in [-1.2,0,1.2]])
    return VGroup(body,arms)


def merged(nucleus=False):
    shell=VGroup(Ellipse(width=10.5,height=5.5,stroke_color=AMBER,stroke_width=4,fill_color=AMBER,fill_opacity=.12))
    guest=cell(PINK,2.5,1.45,True).move_to([1.65,-.45,0])
    g=VGroup(shell,guest)
    if nucleus:
        g.add(VGroup(Ellipse(width=2.1,height=1.9,stroke_color=PURPLE,fill_color=PURPLE,fill_opacity=.12),T("nucleus",24,PURPLE)).move_to([-1.8,.4,0]))
    return g


def chain(side=False):
    # Correct respiratory topology. II feeds Q from a separate branch.
    xs=[-4.8,-2.6,-.4,1.8,4.0]
    names=["I","Q","III","cyt c","IV"]
    cols=[GREEN,TEXT,GREEN,TEXT,GREEN]
    mem=Rectangle(width=12.4,height=3.4,stroke_width=0,fill_color=GREY,fill_opacity=.15).move_to([0,0,0])
    nodes=VGroup(*[block(n,c,1.35,2.4 if c==GREEN else 1.2,28).move_to([x,0,0]) for n,c,x in zip(names,cols,xs)])
    links=VGroup(*[arr((xs[i]+.7,0),(xs[i+1]-.7,0),YELLOW) for i in range(4)])
    g=VGroup(mem,nodes,links)
    if side:
        ii=block("II",GREY,1.25,.8,28).move_to([-2.6,-2,0])
        g.add(ii,arr((-2.6,-1.55),(-2.6,-.5),YELLOW),label("succinate",(-4.7,-1.65),26,PURPLE),arr((-3.8,-2),(-3.3,-2),YELLOW),label("no H⁺ pump",(-2.6,-3.05),28,GREY))
    return g


def stairs(blank=False):
    # Ordinal reaction-step diagram, not a fitted energy trace.
    pts=[(-5.05,1.9),(-2.6,.8),(0,-.35),(2.65,-1.5),(5.1,-2.6)]
    names=["O₂","?" if blank else "superoxide\nO₂•−","?" if blank else "peroxide\nH₂O₂","?" if blank else "•OH + H₂O","2 H₂O"]
    nodes=VGroup(*[block(n,ORANGE if i==0 else BLUE if i==4 else GREY if blank else RED,2.1,1.1,26).move_to(P3(p)) for i,(n,p) in enumerate(zip(names,pts))])
    links=VGroup(*[arr((pts[i][0]+.7,pts[i][1]-.62),(pts[i+1][0]-.7,pts[i+1][1]+.62),YELLOW) for i in range(4)])
    tags=VGroup(*[label(f"+{i} e⁻",(pts[i][0],pts[i][1]+.95),26,YELLOW) for i in range(1,4)])
    aura=Star(n=12,outer_radius=1,inner_radius=.78,color=RED,fill_opacity=0,stroke_width=2).stretch_to_fit_width(2.7).stretch_to_fit_height(1.55).move_to([2.65,-1.5,0])
    if blank: aura.set_opacity(0)
    return VGroup(label("Possible reduction intermediates",(0,3.25),32),nodes,links,tags,aura)


Q1="If cyanobacteria were releasing oxygen,\nwhy did the air not fill with it right away?"
Q2="If oxygen picks up electrons one at a time,\nwhat forms along the way?"


def question1():
    back=mat()
    back[2].shift(DOWN*1.1)
    panel=box(12.4,1.65,"#152D31",.96).move_to([0,2.4,0])
    return VGroup(back,panel,label(Q1,(0,2.4),30))


def question2():
    back=stairs(True)
    back[0].set_opacity(0)
    panel=box(12.2,1.0,LAB,.97).move_to([0,2.9,0])
    return VGroup(back,panel,label(Q2,(0,2.9),30))


def haze_dots():
    return VGroup(*[Dot([x,y,0],radius=.025+.012*(i%3),color=ORANGE,fill_opacity=.35) for i,(x,y) in enumerate(( (x,y) for y in np.arange(.5,3,.32) for x in np.arange(-6.5,6.6,.4)))])

def flakes(n=16):
    return VGroup(*[Polygon([-.17,-.1,0],[0,.16,0],[.22,-.03,0],fill_color=RUST,fill_opacity=.9,stroke_width=0).move_to([-4.8+(i%8)*1.35,1.2-(i//8)*.65,0]) for i in range(n)])

def mito(w=6,h=3.5):
    # Organelle outline and membrane folds, never molecular geometry.
    shell=Ellipse(width=w,height=h,stroke_color=PINK,stroke_width=4,fill_color=PINK,fill_opacity=.12)
    inner=Ellipse(width=w-.3,height=h-.3,stroke_color=PINK,stroke_width=2)
    folds=VGroup(*[Polyline([x,-h*.28,0],[x-.25,-.1,0],[x+.2,.2,0],[x,h*.28,0],stroke_color=PINK,stroke_width=3) for x in np.linspace(-w*.3,w*.3,5)])
    return VGroup(shell,inner,folds)

def later_zone():
    zones=VGroup()
    for i in range(30):
        a=2.1-i*1.1/30;b=a-1.1/30
        zones.add(Rectangle(width=tx(b)-tx(a)+.01,height=2.6,stroke_width=0,fill_color=AMBER,fill_opacity=.25*np.sin(np.pi*(i+.5)/30)).move_to([(tx(a)+tx(b))/2,-.2,0]))
    return VGroup(zones,label("Eukaryotes appear",(3.4,1.9),30,AMBER),label("timing uncertain",(3.4,1.25),26,AMBER))

def idea_card():
    first=label("Every way of living with oxygen",(0,.65),40)
    second=VGroup(T("is a way of handling its",40),T("electrons.",40,YELLOW)).arrange(RIGHT,buff=.18).move_to([0,-.2,0])
    words=VGroup(first,second[0],second[1])
    return words

def enzyme_row(name,reactant,product,y):
    enz=block(name,GREEN,4.8,1.65,28).move_to([0,y,0])
    left=chip(reactant,RED,28).move_to([-4.8,y,0]);right=chip(product,BLUE,28).move_to([4.8,y,0])
    return VGroup(left,arr((left.get_right()[0]+.05,y),(-2.5,y),YELLOW),enz,arr((2.5,y),(right.get_left()[0]-.05,y),YELLOW),right)

def stair_chain():
    pts=[(-4.8,1.8),(-2.5,.9),(-.2,0),(2.1,-.9),(4.4,-1.8)]
    nodes=VGroup(*[block(n,c,1.55,1.1,28).move_to(P3(p)) for n,c,p in zip(["I","Q","III","cyt c","IV"],[GREEN,TEXT,GREEN,TEXT,GREEN],pts)])
    links=VGroup(*[arr((pts[i][0]+.8,pts[i][1]-.2),(pts[i+1][0]-.8,pts[i+1][1]+.2),YELLOW) for i in range(4)])
    return VGroup(nodes,links)


class FilmScene(SpokenScene):
    def setup(self):
        super().setup()
        self.camera.background_color=LAB

    def at(self, phrase, lead=0, nth=0):
        # Reveal each new beat when its spoken words begin.
        return super().at(phrase, lead=lead, nth=nth)

    def finish(self):
        # Give each completed visual a readable hold, including late sentence-end cues.
        super().finish()
        self.wait(1.5)

    def show(self,*mobs,t=.65):
        self.play(*[FadeIn(m) for m in mobs],run_time=t)

    def clear(self,*mobs,t=.5):
        self.play(*[FadeOut(m) for m in (mobs or list(self.mobjects))],run_time=t)

    def heading(self,text,color=TEXT):
        m=label(text,(0,3.05),32,color)
        self.show(m)
        return m


class S00Title(TitleCard):
    LESSON="Oxidative Phosphorylation: The Electron-Transport Chain"
    TITLE="The Oxygen Bargain"
    def construct(self):
        self.add(pigment("#241C1A","#0C1824"))
        self.add(label(self.TITLE,(0,1.4),58),label("How oxygen arrived",(0,-.3),32),label("Why it is dangerous • How cells use it",(0,-1.1),30,GREY))
        rule=VGroup(*[Line([-5.5+i*.275,0,0],[-5.5+(i+1)*.275,0,0],stroke_width=6,color=interpolate_color(ManimColor(RUST),ManimColor(BLUE),i/39)) for i in range(40)]).shift(DOWN*2.1)
        self.play(Create(rule),run_time=1.3)
        oxygen=chip("O₂",ORANGE,32).move_to([-5.4,-2.1,0]);self.add(oxygen)
        self.play(oxygen.animate.move_to([5.4,-2.1,0]),run_time=2)
        self.finish()


class Movement(Scene):
    LINE=""
    TONE=UMBER
    def construct(self):
        self.add(pigment(self.TONE,"#0B1016"))
        title=T(self.LINE,size=40,font=TITLE_FONT)
        self.play(FadeIn(title,shift=UP*.12),run_time=.5)
        self.wait(.95)
        self.wait(.55)


class S01Card(Movement):
    LINE="I. A WORLD WITHOUT OXYGEN"


class S02Open(FilmScene):
    def construct(self):
        world=landscape()
        self.add(world)
        self.at("Picture Earth")
        self.play(world[5].animate.shift(UP*.18+LEFT*.15),run_time=1.3)
        self.at("billion years ago")
        self.show(label("~3 billion years ago",(-3.6,3),28,AMBER))
        self.at("almost no oxygen")
        self.show(chip("Almost no O₂ in the air",ORANGE,28).move_to([0,-2.9,0]))
        self.finish()


class S03Sky(FilmScene):
    def construct(self):
        self.add(landscape());haze=haze_dots();self.add(haze)
        self.at("may have been hazy")
        self.play(haze.animate.set_opacity(.7),run_time=.8)
        q=label("Methane haze?",(0,2.5),42,AMBER)
        self.at("perhaps tinted orange")
        self.show(q)
        self.at("Nobody saw it")
        self.play(haze.animate.shift(LEFT*.3),run_time=1)
        rock=Polygon([-1,-.3,0],[-.7,.4,0],[.4,.55,0],[1,-.25,0],[.3,-.6,0],fill_color=GREY,fill_opacity=.7,stroke_color=GREY).move_to([-3.7,-2.5,0])
        self.at("ancient rocks")
        self.show(rock,label("Evidence: ancient rocks",(1,-2.5),32))
        self.finish()


class S04Sea(FilmScene):
    def construct(self):
        self.add(underwater())
        irons=VGroup(*[chip("Fe²⁺",GREY,28).move_to([x,y,0]) for x,y in [(-4,1.1),(0,.5),(4,1.5),(-2,-1.3),(3,-1.3)]])
        self.at("oceans held dissolved iron")
        self.show(irons)
        self.at("ferrous form")
        self.play(irons[1].animate.scale(1.65),run_time=.7)
        e=edot((.9,.6),.14)
        self.at("take its electrons")
        self.show(e,label("One electron to give",(0,-2.9),30,YELLOW))
        self.at("stayed dissolved")
        self.play(irons.animate.shift(LEFT*.3),e.animate.shift(LEFT*.3),run_time=1.0)
        self.finish()


class S05Life(FilmScene):
    def construct(self):
        self.add(underwater(),microbes())
        icons=VGroup(cell(VIOLET,2.2,1.1).move_to([-4,0,0]),VGroup(*[Circle(radius=.45,stroke_color=VIOLET,fill_color=VIOLET,fill_opacity=.3).move_to([x,y,0]) for x,y in [(-.35,0),(.4,.1),(0,-.55)]]),cell(VIOLET,2.4,1.1).rotate(.2).move_to([4,0,0]))
        self.add(icons,label("A microbial world",(0,2.7),38,VIOLET))
        for cue,name,x in [("by fermenting","Fermentation",-4),("making methane","Methane makers",0),("reduced sulfate","Sulfate reducers?",4)]:
            self.at(cue);self.show(label(name,(x,1.25),28,VIOLET))
        ch4=chip("CH₄",TEXT,28).move_to([0,-1.5,0]);self.show(ch4,t=.3)
        self.play(ch4.animate.shift(UP*.6),run_time=.6)
        self.finish()


class S06Electrons(FilmScene):
    def construct(self):
        rows=VGroup()
        for y,n in zip([2,0,-2],["Fermentation","Methane makers","Sulfate reducers?"]):
            rows.add(VGroup(label(n,(-3.7,y+.65),28,VIOLET),block("donor",PURPLE,2,.95,28).move_to([-4,y-.25,0]),block("acceptor",TEXT,2,.95,28).move_to([.3,y-.25,0]),arr((-2.8,y-.25),(-.9,y-.25),YELLOW)))
        self.add(rows)
        self.at("moves electrons")
        es=VGroup(*[edot((-2.7,y-.25),.14) for y in [2,0,-2]]);self.add(es)
        self.play(*[e.animate.shift(RIGHT*1.8) for e in es],run_time=1.1);self.clear(es,t=.15)
        self.at("Oxygen")
        slot=DashedVMobject(RoundedRectangle(width=3,height=5.6,corner_radius=.3,color=ORANGE),num_dashes=35).move_to([5.5,0,0])
        self.show(slot,label("O₂",(4.6,.6),54,ORANGE),label("scarce",(4.6,-.6),34,ORANGE))
        self.finish()


class S07Land(FilmScene):
    def construct(self):
        world=landscape()
        self.add(world)
        self.at("no plants and no animals")
        self.show(label("Bare rock. Dark sand.",(0,-2.9),34,AMBER))
        self.at("crusted damp patches")
        crust=VGroup(*[Ellipse(width=1.5,height=.18,fill_color=VIOLET,fill_opacity=.85,stroke_width=0).move_to([x,-2,0]) for x in [-3,1]])
        self.show(crust,label("Microbial crusts?",(-2.5,-1.35),28,VIOLET),Line([-2.5,-1.6,0],[-3,-1.9,0],color=VIOLET))
        self.finish()


class S07bBeat(Scene):
    def construct(self):
        self.add(landscape(),label("Bare rock. Dark sand.",(0,-2.9),34,AMBER),label("Microbial crusts?",(-2.5,-1.35),28,VIOLET),Line([-2.5,-1.6,0],[-3,-1.9,0],color=VIOLET))
        self.add(*[Ellipse(width=1.5,height=.18,fill_color=VIOLET,fill_opacity=.85,stroke_width=0).move_to([x,-2,0]) for x in [-3,1]])
        self.wait(2)


class S08Card(Movement):
    LINE="II. THE OXYGEN ARRIVES"
    TONE="#123D3C"


class S09Cyano(FilmScene):
    def construct(self):
        c=glow(cell(CYAN,8.2,5.2,True),CYAN)
        self.add(pigment("#102F38","#154C4A"),c)
        self.at("Cyanobacteria learned")
        self.heading("Cyanobacteria",CYAN)
        water=chip("2 H₂O",BLUE,34).move_to([-5.3,0,0])
        self.at("out of water")
        self.show(water,t=.3)
        es=VGroup(*[edot((-3.4,-1.1+.7*i),.13) for i in range(4)]);self.add(es)
        self.play(es.animate.shift(RIGHT*5.5),run_time=.65)
        self.at("powered by sunlight")
        self.show(VGroup(*[arr((x,2.6),(x-.5,1.6),GOLD) for x in [-2,0,2]]))
        self.at("waste product")
        self.show(chip("O₂",ORANGE,36).move_to([5.2,0,0]),label("2 H₂O → O₂ + 4 H⁺ + 4 e⁻",(0,-3.15),32))
        self.finish()


class S09bWater(FilmScene):
    def construct(self):
        self.add(pigment("#102F38","#154C4A"))
        water=block("H₂O",BLUE,2.2,2,40).move_to([-4.9,.3,0])
        ps2=block("Photosystem II\nsplits water",CYAN,3.5,2.8,28).move_to([-.9,.3,0])
        ps1=block("Photosystem I\nboosts electrons",CYAN,3.5,2.8,28).move_to([3.6,.3,0])
        self.add(water,ps2[0],ps1[0])
        es=VGroup(edot((-5.2,.9),.13),edot((-4.7,.9),.13));self.add(es)
        self.at("Photosystem II")
        self.show(ps2[1],arr((-.9,3),(-.9,1.8),GOLD))
        self.at("splits it")
        self.play(es.animate.move_to([-.9,.9,0]),run_time=.6)
        self.show(chip("O₂",ORANGE,30).move_to([-.9,-1.8,0]))
        self.at("photosystem I")
        self.show(ps1[1],arr((3.6,3),(3.6,1.8),GOLD))
        self.at("boosts the electrons higher")
        self.play(es.animate.move_to([3.6,1.25,0]),run_time=.8)
        self.at("Plants later gained it")
        plant=cell(CYAN,2.6,1.1).move_to([-2.5,-2.9,0]);guest=cell(CYAN,.8,.45).move_to([-2.5,-2.9,0])
        self.show(plant,guest,label("Plants took in a cyanobacterium",(2,-2.9),28,CYAN))
        self.finish()


class S10Mat(FilmScene):
    def construct(self):
        m=mat()
        self.add(m)
        self.at("spread as glowing")
        self.play(m[1].animate.scale(1.1),run_time=1.2)
        self.at("Similar mats")
        self.play(m[2].animate.shift(UP*.8),run_time=1.2)
        self.at("layered mounds")
        self.clear(m[2])
        self.play(m[1].animate.scale(.92).shift(UP*.1),run_time=.4)
        self.at("called stromatolites")
        self.heading("Stromatolites",CYAN)
        self.at("today")
        self.show(label("Living examples in some bays and lakes",(0,-3),26))
        self.finish()


class S11Predict(FilmScene):
    def construct(self):
        self.add(question1()[0])
        self.at("Predict")
        q=question1()
        self.show(q[1],q[2])
        self.finish()


class S12Pause(Scene):
    def construct(self):
        self.add(question1())
        clock=Circle(radius=.38,color=GREY).move_to([5.9,-2.9,0]);hand=Line([5.9,-2.9,0],[5.9,-2.58,0],color=GREY)
        self.add(clock,hand)
        self.play(Rotate(hand,-2*PI,about_point=[5.9,-2.9,0]),run_time=5,rate_func=linear)


class S13Reveal(FilmScene):
    def construct(self):
        self.add(underwater())
        irons=VGroup(*[chip("Fe²⁺",GREY,38).move_to([x,y,0]) for x,y in [(-4,1.6),(-4,-.4),(4,1.6),(4,-.4)]])
        o=chip("O₂",ORANGE,48).move_to([0,.6,0]);self.add(irons,o)
        self.at("handed its electrons")
        es=VGroup(*[edot(i.get_center()+RIGHT*(1 if k<2 else -1),.17) for k,i in enumerate(irons)])
        self.add(es)
        self.play(*[e.animate.move_to([(-.6 if k<2 else .6),.2+(k%2)*.8,0]) for k,e in enumerate(es)],run_time=1)
        self.at("formed")
        self.play(*[Transform(m,chip("Fe³⁺",RUST,38).move_to(m)) for m in irons],FadeOut(es),FadeOut(o),run_time=.7)
        self.show(label("4 Fe²⁺ + O₂ + 10 H₂O → 4 Fe(OH)₃ + 8 H⁺",(0,-3.1),28))
        self.at("and sank")
        f=flakes();self.play(FadeOut(irons),FadeIn(f),run_time=.4)
        self.play(f.animate.shift(DOWN*2.4),FadeIn(Rectangle(width=11.6,height=.7,stroke_color=RUST,fill_color=RUST,fill_opacity=.6).move_to([0,-2.25,0])),run_time=1)
        self.finish()


class S14Bands(Scene):
    def construct(self):
        b=bands();f=flakes();self.add(b[0],f)
        self.play(f.animate.shift(DOWN*2.3),FadeIn(b[1]),run_time=1.3)
        bugs=VGroup(*[cell(VIOLET,.8,.4).move_to([x,-2.9,0]) for x in [-4.5,-3.4,-2.3]])
        self.add(label("Banded iron formation",(0,3.05),34),bugs,label("No oxygen needed?",(2.2,-3),28,VIOLET))
        self.wait(1.7)


class S15Bif(FilmScene):
    def construct(self):
        self.add(bands(),label("Banded iron formation",(0,3.05),34))
        self.at("iron and silica")
        cap=label("Iron minerals + silica",(0,-3.15),28)
        self.show(cap)
        self.at("without oxygen")
        self.show(VGroup(*[cell(VIOLET,.8,.4).move_to([x,-2.65,0]) for x in [-4.7,-3.6,-2.5]]),t=.35)
        self.play(Transform(cap,label("Some layers: microbes without O₂?",(0,-3.15),26,VIOLET)),run_time=.5)
        self.at("iron we mine today")
        truck=VGroup(Rectangle(width=.8,height=.3,fill_color=GOLD,fill_opacity=1,stroke_width=0),Circle(radius=.1,color=GREY).shift(DOWN*.2+LEFT*.24),Circle(radius=.1,color=GREY).shift(DOWN*.2+RIGHT*.24)).move_to([4.3,-2.6,0])
        self.show(truck)
        self.play(truck.animate.shift(LEFT*1.3),run_time=1)
        self.finish()


class S15bPeak(FilmScene):
    def construct(self):
        self.add(timeline())
        a,b=tx(2.6),tx(2.4)
        band=Rectangle(width=b-a,height=3.6,stroke_color=RUST,fill_color=RUST,fill_opacity=.4).move_to([(a+b)/2,0,0])
        self.add(band,label("Major iron-deposition interval",(0,3.05),34,RUST),label("~2.6–2.4 Ga • approximate",(0,2.35),28,RUST))
        self.add(label("Oxygen rises later →",(3.4,.6),28,BLUE),label("Timing and relative\nsize uncertain",(3.5,-.65),26,GREY))
        self.at("biggest pulse")
        self.play(Indicate(band,scale_factor=1.04),run_time=.8)
        self.finish()


class S16Sinks(FilmScene):
    def construct(self):
        self.add(pigment("#112A32","#122024"))
        incoming=chip("O₂",ORANGE,38).move_to([-5.1,0,0])
        iron=block("Dissolved iron",RUST,4.8,.85,26).move_to([.1,2.1,0])
        self.add(incoming,iron,arr((-4.3,.25),(-2.4,2),ORANGE))
        self.at("not the only sink")
        self.play(Indicate(iron),run_time=.6)
        self.at("Volcanic gases")
        v=block("Volcanic gases",GREY,4.8,.85,26).move_to([.1,.7,0]);self.show(v,arr((-4.3,.1),(-2.4,.7),ORANGE))
        self.at("methane")
        m=block("Methane",GREY,4.8,.85,26).move_to([.1,-.7,0]);self.show(m,arr((-4.3,-.1),(-2.4,-.7),ORANGE),t=.4)
        self.at("minerals on land")
        r=block("Minerals on land",GREY,4.8,.85,26).move_to([.1,-2.1,0]);self.show(r,arr((-4.3,-.25),(-2.4,-2),ORANGE),t=.5)
        self.show(block("Air:\na trickle",BLUE,2.4,3,30).move_to([4.7,0,0]))
        self.finish()


class S17Whiffs(FilmScene):
    def construct(self):
        self.add(timeline())
        segs=VGroup(*[Line([tx(a),.6,0],[tx(a-.05),.6,0],color=CYAN,stroke_width=15,stroke_opacity=min(1,(3.5-a)*2.7+.06)) for a in np.arange(3.5,1.5,-.055)])
        self.add(segs,label("Cyanobacterial ancestors",(0,3),34,CYAN),label("Start uncertain",(-4.8,-.15),26,CYAN))
        self.at("brief whiffs of oxygen")
        rock=Polygon([-1,-.4,0],[-.7,.4,0],[.6,.5,0],[1,-.4,0],fill_color=GREY,fill_opacity=.4,stroke_color=GREY).move_to([-1.8,-.9,0])
        puffs=VGroup(*[Ellipse(width=.6,height=.35,stroke_width=0,fill_color=BLUE,fill_opacity=.3).move_to([tx(a),-.3,0]) for a in [2.9,2.7,2.55]])
        self.show(rock,puffs,label("Rock hints: oxygen whiffs?",(2.4,-.8),28,BLUE))
        self.play(puffs.animate.set_opacity(.08).shift(UP*.25),run_time=.7)
        self.play(puffs.animate.set_opacity(.45),run_time=.6)
        self.finish()


class S18Goe(FilmScene):
    def construct(self):
        self.add(timeline())
        self.at("between about")
        band=goe_band()
        self.show(band[0])
        gauge=box(2.1,3.6,BLUE,.08).move_to([-4.5,.2,0])
        fill=Rectangle(width=1.8,height=.1,stroke_width=0,fill_color=BLUE,fill_opacity=.65).move_to([-4.5,-1.35,0])
        self.add(gauge,fill,label("relative O₂",(-4.5,2.65),30,BLUE),label("(schematic)",(-4.5,2.15),26,GREY),DashedLine([-5.55,1.5,0],[-3.45,1.5,0],color=GREY),label("today",(-2.6,1.5),26,GREY))
        self.at("oxygen rose")
        self.play(fill.animate.stretch_to_fit_height(1.3).move_to([-4.5,-.75,0]),run_time=.7)
        self.at("wavered")
        self.play(fill.animate.stretch_to_fit_height(.45).move_to([-4.5,-1.175,0]),run_time=.6)
        self.at("finally stayed")
        self.play(fill.animate.stretch_to_fit_height(.75).move_to([-4.5,-1.025,0]),run_time=.6)
        self.add(label("Levels uncertain",(3,1.1),28,GREY))
        self.at("Great Oxygenation Event")
        self.show(*band[1:],t=.4)
        self.finish()


class S19Sky(FilmScene):
    def construct(self):
        old=landscape(False,True);haze=haze_dots();self.add(old,haze)
        self.at("haze may have thinned")
        self.play(Transform(old,landscape(True,True)),haze.animate.set_opacity(.04).shift(UP*.7),run_time=3)
        self.at("far below today's level")
        self.show(label("O₂ still far below today",(0,2.9),32,ORANGE),label("Deep ocean: still anoxic",(0,-2.9),30,VIOLET))
        self.finish()


class S19bBeat(Scene):
    def construct(self):
        self.add(landscape(True,True),label("O₂ still far below today",(0,2.9),32,ORANGE),label("Deep ocean: still anoxic",(0,-2.8),30,VIOLET))
        self.wait(3)


class S20Dieoff(FilmScene):
    def construct(self):
        self.add(underwater(),microbes().shift(DOWN*1.2))
        evidence=box(10.7,2.6,GREY,.08).move_to([0,.1,0])
        divisions=VGroup(*[Line([x,-1.1,0],[x,1.3,0],color=GREY,stroke_opacity=.4) for x in [-3.5,-1.75,0,1.75,3.5]])
        lens=VGroup(Circle(radius=.7,color=TEXT),Line([.5,-.5,0],[1.25,-1.25,0],color=TEXT,stroke_width=6)).move_to([1,.4,0])
        self.add(evidence,divisions,lens,label("Mass die-off of anaerobes?",(0,2.8),38),label("Fossil evidence",(-3.5,-1.6),28,GREY))
        self.at("evidence is thin")
        self.play(lens.animate.shift(LEFT*2),run_time=1)
        self.show(label("Evidence is thin",(3,-1.6),30,GREY))
        self.at("Anaerobes clearly survived")
        self.clear(evidence,divisions,lens,*[m for m in self.mobjects if isinstance(m,Text)],t=.4)
        self.add(label("Anaerobes survived",(0,2.8),38,VIOLET))
        self.show(label("Mud • deep water • airless places",(0,.3),32,VIOLET))
        self.finish()


class S21Gut(FilmScene):
    def construct(self):
        # A thick serpentine lumen, drawn as an organ cartoon rather than a molecule.
        pts=[[-5,2,0],[-2,2,0],[2,2,0],[4.5,1,0],[2.5,0,0],[-2.5,0,0],[-4.5,-1,0],[-2.5,-2,0],[2.8,-2,0]]
        tube=VMobject(stroke_color=VIOLET,stroke_width=65,stroke_opacity=.35).set_points_smoothly(pts)
        cells=VGroup(*[cell(VIOLET,.7,.35).move_to([x,y,0]) for x,y in [(-3,2),(0,2),(2.7,1.8),(2,.1),(-1,0),(-2.5,-2),(.5,-2)]])
        self.add(tube,cells)
        self.at("thrive there still")
        self.play(cells.animate.shift(RIGHT*.25),run_time=.8)
        self.at("your own gut")
        self.heading("Still here: your gut",VIOLET)
        self.finish()


class S21bShadow(FilmScene):
    def construct(self):
        self.add(landscape(True,True),microbes())
        self.at("did not end")
        self.show(label("The old world of life survived",(0,2.9),36))
        self.at("into the shadows")
        self.show(label("Anaerobes in airless places",(0,-3.1),28,VIOLET))
        self.finish()


class S22Card(Movement):
    LINE="III. OXYGEN IS DANGEROUS"
    TONE="#431C28"


class S23Why(FilmScene):
    def construct(self):
        o=block("O₂",ORANGE,4.8,3.8,72)
        self.add(pigment("#251422","#0B121C"),o)
        self.at("pulls in four electrons")
        slots=VGroup(*[DashedVMobject(Circle(radius=.35,color=YELLOW),num_dashes=12).move_to([x,y,0]) for x,y in [(-3.3,0),(3.3,0),(0,2.6),(0,-2.6)]])
        self.show(slots)
        self.at("to become water")
        self.show(label("O₂ + 4 e⁻ + 4 H⁺ → 2 H₂O",(0,-3.35),32),t=.3)
        self.play(Indicate(o,scale_factor=1.03),run_time=.5)
        self.finish()


class S24Spin(FilmScene):
    def construct(self):
        o=block("O₂",ORANGE,4,3.8,68).move_to([2,0,0]);self.add(o)
        self.at("two unpaired electrons")
        self.show(label("↑     ↑",(2,2.45),48,YELLOW))
        ordinary=block("Ordinary\nmolecule",GREY,3.1,2,30).move_to([-4.2,.7,0])
        pair=VGroup(edot((-2.4,.5),.15),edot((-2.4,.9),.15))
        self.at("slow to react")
        self.show(ordinary,pair)
        self.play(pair.animate.shift(RIGHT*.8),run_time=.5)
        self.play(pair.animate.shift(LEFT*.8),run_time=.5)
        self.show(label("paired offer turned away",(-3.6,-1.1),26,GREY))
        self.at("one at a time")
        self.show(label("Spin rule: one electron at a time",(0,-3),34,YELLOW),t=.25)
        self.clear(ordinary,pair,*[m for m in self.mobjects if isinstance(m,Text) and 'paired' in m.text],t=.25)
        metal=chip("Metal ion",RUST,32).move_to([-4.2,0,0]);e=edot((-2.7,0),.18)
        self.add(metal,e);self.play(e.animate.move_to([.6,0,0]),run_time=.8)
        self.play(Indicate(metal,scale_factor=1.03),run_time=.4)
        self.finish()


class S25Predict(FilmScene):
    def construct(self):
        self.add(question2()[0])
        self.at("Predict")
        q=question2();self.show(q[1],q[2])
        self.finish()


class S26Pause(Scene):
    def construct(self):
        self.camera.background_color=LAB
        self.add(question2())
        self.wait(5)


class S27Ros(FilmScene):
    def construct(self):
        st=stairs(True);self.add(st);full=stairs()
        for phrase,i in [("makes superoxide",1),("make hydrogen peroxide",2),("make a hydroxyl radical",3)]:
            self.at(phrase)
            target=full[1][i];e=edot(target.get_center()+UP*1.4,.15);h=hdot(target.get_center()+LEFT*1.25,.13)
            self.add(e,h)
            self.play(e.animate.move_to(target.get_center()+UP*.65),h.animate.move_to(target.get_center()+LEFT*.75),Transform(st[1][i],target),run_time=.65)
            self.clear(e,h,t=.15)
        self.add(full[4])
        self.at("attacks almost anything")
        self.play(Flash(st[1][3],color=RED,flash_radius=.8),Indicate(st[1][3],color=RED,scale_factor=1.08),run_time=.8)
        self.finish()


class S27bBeat(Scene):
    def construct(self):
        self.camera.background_color=LAB;st=stairs();self.add(st)
        self.play(Indicate(st[4],color=RED,scale_factor=1.04),run_time=.6)
        self.wait(1.9)


class S28Damage(FilmScene):
    def construct(self):
        panels=VGroup(*[box(3.8,5.5,GREY,.04).move_to([x,-.3,0]) for x in [-4.2,0,4.2]])
        dna=VGroup(*[Rectangle(width=.38,height=.65,stroke_color=PURPLE,fill_color=PURPLE,fill_opacity=.65).move_to([-4.2,-1.65+.7*i,0]) for i in range(5)])
        protein=block("Protein",GREEN,2.5,2.4,30)
        lipids=VGroup(*[Rectangle(width=.34,height=1.6,stroke_color=GREY,fill_color=GREY,fill_opacity=.6).move_to([3.05+i*.45,-.2,0]) for i in range(6)])
        self.add(panels,dna,protein,lipids,label("DNA",(-4.2,2.1),30,PURPLE),label("Membrane",(4.2,1.8),28,GREY))
        self.at("reactive oxygen species")
        self.heading("Reactive oxygen species (ROS)",RED)
        self.at("break DNA")
        self.play(dna[3:].animate.shift(UP*.25+RIGHT*.35),FadeOut(dna[2]),Flash(dna[2],color=RED,flash_radius=.6),run_time=.7)
        self.at("damage proteins")
        self.play(protein[0].animate.set_color(RED).rotate(.2),run_time=.7)
        self.at("chain reactions")
        self.play(LaggedStart(*[l.animate.set_color(RED) for l in lipids],lag_ratio=.18),run_time=1.2)
        self.clear(lipids[2:4],t=.3)
        self.finish()


class S29Fenton(FilmScene):
    def construct(self):
        fe=block("Fe²⁺",GREY,3,2.7,56).move_to([-3.6,.3,0]);per=block("H₂O₂",RED,3.4,2.7,54).move_to([1,.3,0])
        callback=flakes(8).shift(DOWN*2.5);self.add(fe,per,callback,label("Iron amplifies the danger",(0,3),34,RUST))
        self.at("hands an electron")
        e=edot((-1.8,.3),.2);self.add(e);self.play(e.animate.move_to([.1,.3,0]),run_time=.8)
        self.at("releasing the hydroxyl radical")
        rad=chip("•OH",RED,48).move_to([4.7,.6,0])
        self.play(Transform(fe,block("Fe³⁺",RUST,3,2.7,56).move_to(fe)),Transform(per,block("OH⁻",GREY,3,2.7,48).move_to(per)),FadeOut(e),FadeIn(rad),FadeOut(callback),run_time=.7)
        self.play(Flash(rad,color=RED,flash_radius=.7),run_time=.5)
        self.add(label("Fe²⁺ + H₂O₂ → Fe³⁺ + OH⁻ + •OH",(0,-2.9),32))
        self.finish()


class S29bLock(FilmScene):
    def construct(self):
        # Ferritin is a protein shell cartoon; heme is a labelled chip, never a ring structure.
        shell=VGroup(Circle(radius=1.65,stroke_color=GREY,stroke_width=4),Ellipse(width=3.3,height=1.1,stroke_color=GREY),Ellipse(width=1.1,height=3.3,stroke_color=GREY),Circle(radius=.8,fill_color=RUST,fill_opacity=.7,stroke_color=RUST)).move_to([-3.8,0,0])
        heme=block("Heme\nbound iron",RUST,3.2,2.6,32).move_to([.4,0,0])
        partners=VGroup(*[VGroup(chip("partner",GREY,26).move_to([4.3,y,0]),chip("Fe",RUST,26).move_to([5.9,y,0]),Line([5.15,y,0],[5.45,y,0],color=GREY)) for y in [-1.2,0,1.2]])
        self.add(shell,heme,partners,label("Ferritin shell",(-3.8,2.3),30),label("mineral core",(-3.8,-2.3),28,RUST),label("Small labile pool",(4.7,2.3),28),label("Iron held by proteins and partners",(0,3.3),32))
        self.at("tightly bound")
        self.play(Indicate(shell,scale_factor=1.03),run_time=.7)
        self.at("stored inside proteins")
        self.show(label("Storage varies with cell and condition",(0,-3.2),28,GREY))
        self.finish()


class S30Idea(FilmScene):
    def construct(self):
        self.camera.background_color=BLACK;words=idea_card();e=edot((3.1,-1.8),.18)
        self.add(e)
        self.at("Here is the idea")
        self.show(label("The idea that ties this film together",(0,2.8),30),t=.4)
        self.at("Every way of living")
        self.show(words[0],t=.5)
        self.at("is a way of handling")
        self.show(words[1],t=.5)
        self.at("electrons")
        self.show(words[2],t=.25)
        self.play(MoveAlongPath(e,Ellipse(width=6.2,height=1.2).move_to([0,-1.8,0])),run_time=2)
        self.finish()


class S30bBeat(Scene):
    def construct(self):
        self.camera.background_color=BLACK;self.add(idea_card());e=edot((3.1,-1.8),.18);self.add(e)
        self.play(MoveAlongPath(e,Ellipse(width=6.2,height=1.2).move_to([0,-1.8,0])),run_time=3,rate_func=linear)


class S31Enzymes(FilmScene):
    def construct(self):
        first=enzyme_row("Superoxide\ndismutase","2 O₂•−\n+ 2 H⁺","H₂O₂ + O₂",1.35)
        second=enzyme_row("Catalase","2 H₂O₂","2 H₂O + O₂",-1.35)
        self.add(first[2],second[2])
        self.at("Superoxide dismutase")
        self.show(first[0],first[1],t=.35)
        self.play(Indicate(first[2],scale_factor=1.04),run_time=.6)
        self.at("hydrogen peroxide")
        self.show(first[3],first[4],t=.3)
        self.play(Indicate(first[4],color=BLUE,scale_factor=1.08),run_time=.7)
        self.at("Catalyase")
        self.show(second[0],second[1],t=.3)
        self.play(Indicate(second[2],scale_factor=1.04),run_time=.6)
        self.at("water and oxygen")
        self.show(second[3],second[4],t=.3)
        self.play(Indicate(second[4],color=BLUE,scale_factor=1.08),run_time=.7)
        self.show(label("Reactive oxygen → controlled products",(0,-3.05),28,GREEN),t=.8)
        self.finish()


class S32Respire(FilmScene):
    def construct(self):
        ch=stair_chain();self.add(cell(PINK,12.5,6.2),ch)
        self.at("put oxygen to work")
        self.show(chip("O₂",ORANGE,32).move_to([4.4,-.3,0]))
        self.at("They placed it")
        e=edot((-4.8,2.55),.16);self.add(e)
        self.play(Succession(*[e.animate.move_to([x,y+.7,0]) for x,y in [(-2.5,.9),(-.2,0),(2.1,-.9),(4.4,-1.8)]]),run_time=1.6)
        self.show(chip("O₂ → H₂O",BLUE,28).move_to([1.1,-2.35,0]))
        self.finish()


class S33Energy(FilmScene):
    def construct(self):
        # Ordinal ladder: only relative ranking is claimed, no numerical potential trace.
        axis=arr((-5.5,2.7),(-5.5,-2.7),GREY)
        self.add(axis,label("Electron energy",(-3.55,3.1),30,YELLOW),label("relative • schematic",(2.7,3.1),26,GREY),label("high",(-6.1,2.45),26),label("low",(-6.1,-2.5),26))
        rungs=VGroup()
        for name,y,c in [("Donor",1.8,PURPLE),("Sulfate",.85,TEXT),("Other acceptors",-.25,GREY),("O₂",-2.2,ORANGE)]:
            rungs.add(Line([-4.8,y,0],[-.6,y,0],color=c,stroke_width=4),label(name,(-2.8,y+.32),28,c))
        self.add(rungs,arr((.1,1.8),(.1,.85),YELLOW),label("small release",(2.3,1.3),30,YELLOW),arr((.1,.4),(.1,-2.2),YELLOW),label("large release",(2.6,-1.1),34,YELLOW))
        self.at("falls all the way")
        e=edot((-.25,1.8),.18);self.add(e)
        self.play(e.animate.move_to([-.25,-2.2,0]),run_time=1.2)
        self.at("much more energy")
        self.play(Flash(e,color=YELLOW,flash_radius=.65),run_time=.6)
        self.finish()


class S33bAtp(FilmScene):
    def construct(self):
        self.add(label("ATP per glucose",(-2.2,2.9),36,TEAL))
        for x,n in [(-3.3,2),(3.3,30)]:
            self.add(VGroup(*[Rectangle(width=1.8,height=.13,stroke_color=TEAL,fill_color=TEAL,fill_opacity=.7).move_to([x,-2.2+i*.145,0]) for i in range(n)]))
        a=label("2",(-3.3,-1.25),54,TEAL);b=label("about 30",(3.3,2.65),38,TEAL)
        self.add(label("Fermentation",(-3.3,-2.8),28),label("lactate or ethanol",(-3.3,-3.3),26,GREY),label("Aerobic respiration",(3.3,-2.8),28),label("~ estimate",(3.3,-3.3),26,GREY))
        self.at("yields")
        self.show(a,t=.25)
        self.play(Indicate(a),run_time=.6)
        self.at("around 30")
        self.show(b,t=.25)
        self.play(Indicate(b),run_time=.6)
        self.finish()


class S34Leak(FilmScene):
    def construct(self):
        ch=chain();ch[0].stretch_to_fit_height(3.8)
        self.add(ch,label("A small fraction of electrons leak",(0,3.1),32,RED))
        flowing=VGroup(*[edot((x,1.55),.13) for x in np.linspace(-5,3.8,9)]);self.add(flowing)
        self.at("chain is not perfect")
        self.play(flowing.animate.shift(RIGHT*.6),run_time=.8)
        self.at("slip off early")
        e1=edot((-4.8,.9),.16);e3=edot((-.4,.9),.16);self.add(e1,e3)
        self.play(e1.animate.move_to([-4.8,2.1,0]),e3.animate.move_to([-.4,2.1,0]),run_time=.65)
        self.at("complexes one and three")
        self.play(Flash(e1,color=RED),Flash(e3,color=RED),run_time=.5)
        self.at("making superoxide")
        self.clear(e1,e3,t=.15)
        self.show(chip("O₂•−",RED,30).move_to([-4.8,2.1,0]),chip("O₂•−",RED,30).move_to([-.4,2.1,0]),label("Most flow onward →",(1,-2.8),30,YELLOW))
        self.finish()


class S34bBeat(Scene):
    def construct(self):
        self.camera.background_color=LAB;ch=chain();ch[0].stretch_to_fit_height(3.8)
        self.add(ch,label("A small fraction of electrons leak",(0,3.1),32,RED),chip("O₂•−",RED,30).move_to([-4.8,2.1,0]),chip("O₂•−",RED,30).move_to([-.4,2.1,0]))
        self.wait(2)


class S35Card(Movement):
    LINE="IV. A CELL INSIDE A CELL"
    TONE="#39263F"


class S36Later(FilmScene):
    def construct(self):
        self.add(timeline(),goe_band())
        self.at("oldest widely accepted")
        self.show(later_zone(),t=.4)
        fossil=cell(AMBER,1.1,.9).move_to([tx(1.5),-.7,0])
        self.show(fossil,t=.4)
        self.at("more than one and a half")
        self.show(label("Fossils: >1.5 billion years",(3.6,2.55),26,AMBER),t=.4)
        self.finish()


class S37Host(FilmScene):
    def construct(self):
        self.add(pigment("#251C2A","#372D31"),host(),label("Archaeal host • Asgard relative",(0,3.1),32,AMBER))
        self.at("nucleus is still debated")
        nucleus=DashedVMobject(Circle(radius=1,color=PURPLE),num_dashes=20).move_to([.5,0,0])
        self.show(nucleus,label("?",(.5,0),60,PURPLE),label("Nucleus yet?",(0,-3.05),32,PURPLE))
        self.finish()


class S37bAsgard(FilmScene):
    def construct(self):
        self.add(underwater())
        vents=VGroup(*[Polygon([x-.5,-3.4,0],[x-.25,-.5+h,0],[x+.2,-.6+h,0],[x+.6,-3.4,0],fill_color=GREY,fill_opacity=.5,stroke_color=GREY) for x,h in [(-5.2,.5),(-4.3,-.2),(-3.5,.2)]])
        plumes=VGroup(*[Ellipse(width=.4+.13*i,height=.3,fill_color=GREY,fill_opacity=.15,stroke_width=0).move_to([-5.1-.1*i,.3+i*.35,0]) for i in range(7)])
        core=VGroup(*[Rectangle(width=1.4,height=.65,stroke_color=GREY,fill_color=c,fill_opacity=.8).move_to([-1.3,-1.8+.65*i,0]) for i,c in enumerate(["#3B3437","#5C5252","#75665E","#8B7C6F"])])
        self.add(vents,plumes,core)
        self.at("sediments")
        self.play(core.animate.shift(UP*.7),run_time=.8)
        genome=block("Asgard genome",AMBER,4.8,3,32).move_to([3,.3,0])
        stream=VGroup(*[Rectangle(width=.35,height=.22,fill_color=PURPLE,fill_opacity=.8,stroke_width=0).move_to([-.2+i*.45,1.2+.3*np.sin(i),0]) for i in range(6)])
        self.at("Their genomes")
        self.show(stream,genome)
        self.at("genes once thought unique")
        tiles=VGroup(*[Rectangle(width=.45,height=.4,fill_color=PURPLE,fill_opacity=1,stroke_color=PURPLE).move_to([1.7+i*.75,-.4,0]) for i in range(4)])
        self.show(tiles,label("Genes once thought unique\nto eukaryotes",(2.7,2.85),30,PURPLE))
        self.finish()


class S38Guest(FilmScene):
    def construct(self):
        self.add(pigment("#251C2A","#372D31"))
        guest=cell(PINK,9.2,5.1,True).shift(LEFT*.5)
        self.add(guest)
        self.at("The guest")
        self.at("alpha protobacteria")
        self.heading("Alphaproteobacterial relative",PINK)
        self.at("probably respire")
        little=chain().scale(.5).move_to([-.5,-.1,0])
        # Tiny chain uses unlabeled colored blocks; labels would fall below 22 pt.
        for node in little[1]: node[1].set_opacity(0)
        self.show(little)
        self.at("may have used oxygen")
        self.show(chip("O₂?",ORANGE,32).move_to([5.5,0,0]))
        self.finish()


class S39Engulf(FilmScene):
    def construct(self):
        self.add(pigment("#251C2A","#372D31"))
        h=Ellipse(width=6.2,height=4.8,stroke_color=AMBER,stroke_width=5,fill_color=AMBER,fill_opacity=.1).move_to([-2.6,0,0])
        g=cell(PINK,2.8,1.7,True).move_to([3.1,0,0]);g[0].set_fill(WARM,opacity=1);self.add(h,g,label("One proposed mechanism",(0,3.15),32,AMBER))
        self.at("came to enclose")
        arms=VGroup(VMobject(stroke_color=AMBER,stroke_width=5).set_points_smoothly([[-.6,2,0],[1.1,2.7,0],[4.3,2,0],[5,0.4,0]]),VMobject(stroke_color=AMBER,stroke_width=5).set_points_smoothly([[-.6,-2,0],[1.1,-2.7,0],[4.3,-2,0],[5,-.4,0]]))
        self.show(arms,t=.7)
        final=Ellipse(width=11.8,height=5.3,stroke_color=AMBER,stroke_width=5,fill_color=AMBER,fill_opacity=.1)
        self.play(Transform(h,final),g.animate.move_to([2.4,-.3,0]),FadeOut(arms),run_time=1.5)
        self.at("guests stayed")
        self.play(Indicate(g,color=PINK,scale_factor=1.08),run_time=.7)
        self.finish()


class S39bBeat(Scene):
    def construct(self):
        m=merged();m[0].stretch_to_fit_width(10).stretch_to_fit_height(5)
        self.add(pigment("#251C2A","#372D31"),m,label("One proposed mechanism",(0,3.05),30,AMBER))
        self.play(m[1].animate.scale(.7).shift(LEFT*.7),run_time=.8)
        second=m[1].copy().shift(RIGHT*1.7)
        self.play(FadeIn(second),run_time=.7)
        self.wait(1.5)


class S40Once(FilmScene):
    def construct(self):
        self.add(pigment("#251C2A","#372D31"))
        root=Dot([-5.8,0,0],radius=.15,color=PINK)
        bact=VGroup(*[Line([-5.8,0,0],[-3.3,y,0],color=PINK,stroke_width=3) for y in [-2,-1,0,1,2]])
        self.add(root,bact,label("Alphaproteobacteria",(-3.5,3.1),30,PINK))
        self.at("only once")
        node=Dot([-.3,0,0],radius=.2,color=PINK)
        self.show(Line([-3.3,0,0],[-.3,0,0],color=PINK,stroke_width=4),node,label("Mitochondria",(-.3,.6),30,PINK))
        self.at("Every mitochondrion today")
        branches=VGroup(*[VGroup(Line([-.3,0,0],[3.5,y,0],color=PINK,stroke_width=3),label(n,(4.8,y),30)) for n,y in zip(["Plants","Animals","Fungi","Protists"],[2.1,.7,-.7,-2.1])])
        self.show(branches,label("After Gray, Burger & Lang (1999)",(0,-3.2),26,GREY))
        self.finish()


class S40bClues(FilmScene):
    def construct(self):
        a=mito(5.4,4.3).move_to([-3.4,0,0]);b=cell(PINK,5.4,4.3).move_to([3.4,0,0])
        a[2][1:4].set_opacity(0)
        self.add(a,b,label("Mitochondrion",(-3.4,2.8),32,PINK),label("Bacterium",(3.4,2.8),32,PINK))
        self.at("two membranes")
        cap=label("✓ Two membranes",(0,-3.1),32);self.show(cap)
        self.at("their own DNA")
        self.show(chip("DNA",PURPLE,30).move_to([-3.4,1.05,0]),chip("DNA",PURPLE,30).move_to([3.4,1.05,0]))
        new_cap=label("✓ Their own DNA",(0,-3.1),32)
        self.play(Succession(FadeOut(cap),FadeIn(new_cap)),run_time=.35);cap=new_cap
        self.at("ribosomes")
        self.show(VGroup(*[Dot([x+dx,-1.2,0],radius=.16,color=GREEN) for x in [-3.4,3.4] for dx in [-.7,0,.7]]))
        new_cap=label("✓ Ribosomes of bacterial ancestry",(0,-3.1),30)
        self.play(Succession(FadeOut(cap),FadeIn(new_cap)),run_time=.35);cap=new_cap
        self.at("pinching in two")
        new_cap=label("✓ Division by pinching in two",(0,-3.1),30)
        self.play(a.animate.stretch(.7,0),b.animate.stretch(.7,0),Succession(FadeOut(cap),FadeIn(new_cap)),run_time=.8)
        self.show(VGroup(*[VGroup(arr((x+.95,2),(x+.95,.7),PINK),arr((x+.95,-2),(x+.95,-.7),PINK)) for x in [-3.4,3.4]]),t=.4)
        self.finish()


class S41Why(FilmScene):
    def construct(self):
        self.add(merged().scale(.8))
        self.at("Why did the partnership begin")
        self.heading("Why did it start?",AMBER)
        self.at("still debated")
        self.show(chip("Hydrogen?",TEXT,30).move_to([-3,-2.9,0]),chip("Oxygen?",ORANGE,30).move_to([3,-2.9,0]))
        self.finish()


class S42H2(FilmScene):
    def construct(self):
        h=cell(AMBER,5.3,5.0).move_to([-3.35,-.1,0]);b=cell(PINK,5.0,4.6,True).move_to([3.35,-.1,0])
        self.add(h,b)
        self.at("hydrogen hypothesis")
        self.heading("Hydrogen hypothesis",AMBER)
        self.at("host lived on hydrogen")
        self.show(label("Host",(-3.35,-3.05),30,AMBER))
        hydrogen=chip("H₂",TEXT,32).move_to([2,.4,0])
        self.at("bacterium gave off hydrogen")
        self.show(hydrogen)
        self.play(hydrogen.animate.move_to([-2,.4,0]),run_time=1)
        self.at("fed each other")
        self.show(arr((-1.1,-1.2),(1.1,-1.2),TEXT),arr((1.1,1.2),(-1.1,1.2),TEXT),label("Trading food",(2.7,-3.1),32))
        self.finish()


class S43O2(FilmScene):
    def construct(self):
        self.add(cell(AMBER,4.8,4.6).move_to([-3.2,0,0]),cell(PINK,4.4,3.8,True).move_to([2,0,0]))
        self.at("oxygen detoxification hypothesis")
        self.heading("Oxygen detoxification hypothesis",ORANGE)
        oxy=chip("O₂",ORANGE,32).move_to([5.4,1,0])
        self.at("oxygen harmed the host")
        self.show(oxy)
        self.at("bacterium consumed oxygen")
        self.play(oxy.animate.move_to([2,0,0]),run_time=.8)
        self.play(Flash(oxy,color=ORANGE,flash_radius=.7),run_time=.4)
        self.clear(oxy,t=.3)
        self.at("shielded its partner")
        shield=Ellipse(width=5.3,height=5.1,color=BLUE,stroke_width=4).move_to([-3.2,0,0])
        self.show(shield,label("Protected host",(-3.2,-2.8),30,BLUE))
        self.finish()


class S44Open(FilmScene):
    def construct(self):
        self.add(chip("Hydrogen?",TEXT,30).move_to([-4.5,2.7,0]),chip("Oxygen?",ORANGE,30).move_to([4.5,2.7,0]))
        scale=VGroup(Line([-2.5,2.1,0],[2.5,2.1,0],color=TEXT,stroke_width=5),Line([0,2.1,0],[0,.9,0],color=TEXT,stroke_width=4),Polygon([-.6,.8,0],[0,1.4,0],[.6,.8,0],color=GREY),*[Arc(radius=.65,start_angle=PI,angle=PI,color=TEXT).move_to([x,1.6,0]) for x in [-2.5,2.5]])
        flask=VMobject(stroke_color=GREY,stroke_width=4,fill_color=BLUE,fill_opacity=.07).set_points_as_corners([[-4.4,.5,0],[-4.4,-.1,0],[-5.7,-2.5,0],[-5.5,-2.8,0],[5.5,-2.8,0],[5.7,-2.5,0],[4.4,-.1,0],[4.4,.5,0]])
        arch=host().scale(.55).move_to([-2.9,-1.2,0]);partner=cell(PINK,3.5,2.2).move_to([3,-1.2,0])
        self.add(scale)
        self.at("neither is proven")
        self.show(label("Neither is proven",(0,3.45),30))
        self.at("first Asgard")
        self.show(flask,arch,partner,t=.5)
        self.at("gives hydrogen to partner microbes")
        h=chip("H₂",TEXT,30).move_to([-.6,-1.2,0]);self.add(h)
        self.play(h.animate.move_to([.6,-1.2,0]),run_time=1.2)
        self.at("reverse of the proposed host")
        self.show(label("Cultured Asgard gives H₂ to partners",(0,-3.1),28,AMBER))
        self.at("partnerships are real")
        self.show(label("Imachi et al. (2020)",(0,-3.65),26,GREY))
        self.finish()


class S45Stage(FilmScene):
    def construct(self):
        goe=goe_band();goe[1].move_to([-1,2.5,0]);goe[3].put_start_and_end_on([goe[3].get_x(),2.15,0],[goe[3].get_x(),1.75,0])
        self.add(timeline(),goe)
        x1,x2=tx(1.8),tx(1)
        self.add(Rectangle(width=x2-x1,height=2.4,stroke_width=0,fill_color=AMBER,fill_opacity=.15).move_to([(x1+x2)/2,-.1,0]),label("Eukaryote fossil record",(3.6,1.9),28,AMBER),label("timing uncertain",(3.6,1.25),26,AMBER))
        self.at("fossils appear long after")
        a,b=tx(2.1),tx(1.8)
        brace=VGroup(Line([a,-.8,0],[b,-.8,0],color=TEXT),Line([a,-.8,0],[a,-.5,0],color=TEXT),Line([b,-.8,0],[b,-.5,0],color=TEXT))
        self.show(brace,label("gap",((a+b)/2,-1.25),26))
        self.at("still debated")
        self.show(label("Did oxygen drive the merger?",(0,3.5),28),label("Still debated.",(0,-3.65),28))
        self.finish()


class S46Genes(FilmScene):
    def construct(self):
        self.add(pigment("#251C2A","#372D31"))
        shell=Ellipse(width=12,height=5.5,stroke_color=AMBER,fill_color=AMBER,fill_opacity=.08)
        nucleus=block("Nucleus",PURPLE,3.3,2.6,32).move_to([-3.5,.3,0]);m=mito(5.6,3.6).move_to([2.7,0,0])
        genes=VGroup(*[Rectangle(width=.4,height=.45,stroke_color=PURPLE,fill_color=PURPLE,fill_opacity=1).move_to([1.1+(i%5)*.65,-.45+(i//5)*.9,0]) for i in range(10)])
        self.add(shell,nucleus,m,genes)
        self.at("guess became an organelle")
        self.heading("From guest to organelle",PINK)
        self.at("genes were lost")
        self.clear(genes[:7],t=.8)
        self.at("others moved to the nucleus")
        self.play(genes[7:].animate.move_to([-3.5,-.4,0]),run_time=1.2)
        self.finish()


class S47Mtdna(FilmScene):
    def construct(self):
        self.add(pigment("#251C2A","#372D31"))
        m=mito(12,5.2);m[2].set_opacity(0);self.add(m)
        genome=chip("mtDNA",PURPLE,36).move_to([-3.6,.65,0]);self.add(genome)
        complexes=VGroup(*[block(n,GREEN,1.8,1.5,28).move_to([x,-1.25,0]) for n,x in [("I",-3.8),("III",-1.4),("IV",1),("ATP",3.6)]])
        synthase=VGroup(Line([3.6,-1,0],[3.6,-.3,0],color=TEAL,stroke_width=7),Ellipse(width=1.5,height=.6,color=TEAL,fill_color=TEAL,fill_opacity=.3).move_to([3.6,-.2,0]))
        for node in complexes: node[1].shift(DOWN*.38)
        self.add(complexes,synthase,label("ATP synthase",(3.6,.65),28,TEAL))
        self.at("thirteen proteins")
        tiles=VGroup(*[Rectangle(width=.32,height=.4,fill_color=GREEN,fill_opacity=1,stroke_color=GREEN).move_to([-2.9+.48*i,1.7,0]) for i in range(13)])
        self.show(tiles,label("Human mtDNA: about a dozen proteins",(0,3.2),32,PURPLE))
        self.at("respiration and")
        self.play(*[t.animate.move_to([[-3.8,-1.4,1,3.6][i//4]+(-.5+(i%4)*.33 if i<12 else 0),-.9,0]) for i,t in enumerate(tiles)],run_time=.9)
        self.show(label("Respiration and ATP synthesis",(0,-3.2),32,TEAL))
        self.finish()


def descendants():
    g=VGroup()
    for x,c,n in zip([-4.8,-1.6,1.6,4.8],[AMBER,CYAN,VIOLET,PINK],["Protist","Plant","Fungus","Animal"]):
        shape=cell(c,2.85,4.7)
        mitos=VGroup(*[cell(PINK,.55,.3,False).move_to([dx,dy,0]) for dx,dy in [(-.55,.65),(.55,.3),(-.2,-.7)]])
        g.add(VGroup(shape,mitos,label(n,(0,-2.8),28,c)).move_to([x,0,0]))
    return g


class S48Payoff(FilmScene):
    def construct(self):
        m=merged();self.add(m)
        self.at("One influential idea")
        head=self.heading("One influential idea",AMBER)
        self.at("many mitochondria")
        copies=VGroup(*[cell(PINK,.65,.36).move_to([x,y,0]) for x in np.linspace(-3.6,3.6,8) for y in [-1.4,-.5,.5,1.4]])
        self.clear(m[1],t=.2)
        self.show(copies)
        self.at("larger genomes")
        self.show(label("Energy for larger genomes",(0,-3.05),30,TEAL))
        self.at("more complex lives")
        self.clear(m,copies,*[o for o in self.mobjects if isinstance(o,Text) and o is not head],t=.3)
        self.show(descendants())
        self.finish()


class S48bBeat(Scene):
    def construct(self):
        self.camera.background_color=LAB
        self.add(descendants(),label("One influential idea",(0,3.05),32,AMBER))
        self.wait(2)


class S49Remind(FilmScene):
    def construct(self):
        panels=VGroup(*[box(3.8,5.4,GREY,.05).move_to([x,0,0]) for x in [-4.2,0,4.2]])
        rust=flakes(12).scale(.25).move_to([-4.2,.2,0]);rust.stretch_to_fit_height(2.7)
        for f in rust: f.stretch_to_fit_width(.3)
        ros=chip("O₂•−",RED,48);power=VGroup(block("IV",GREEN,2,2,38).move_to([4.2,.7,0]),chip("H₂O",BLUE,34).move_to([4.2,-1.3,0]),arr((4.2,-.4),(4.2,-.8),YELLOW))
        self.add(panels,rust,ros,power,label("Rust",(-4.2,-2.2),32,RUST),label("Poison",(0,-2.2),32,RED),label("Power",(4.2,-2.2),32,GREEN))
        self.at("Rust poison and power")
        self.play(rust.animate.shift(DOWN*.4),Flash(ros,color=RED,flash_radius=1),run_time=.9)
        self.at("handling oxygen's electrons")
        stream=VGroup(*[edot((x,2.1),.13) for x in np.linspace(-5.5,4.5,14)]);self.add(stream)
        self.play(stream.animate.shift(RIGHT*.7),run_time=1.4)
        self.finish()


class S50Bridge(FilmScene):
    def construct(self):
        ch=chain(True);ch[0].stretch_to_fit_height(2.7);self.add(ch)
        pumps=VGroup(*[VGroup(arr((x,.7),(x,2.5),BLUE),label("H⁺",(x+.5,1.9),28,BLUE)) for x in [-4.8,-.4,4]])
        self.add(pumps,arr((-5.9,-2.4),(-5.9,0),YELLOW),arr((-5.9,0),(-5.5,0),YELLOW))
        self.at("In this lesson")
        self.heading("Follow the electrons",YELLOW)
        donor=chip("NADH",PURPLE,30).move_to([-4.8,-2.8,0])
        self.show(donor)
        self.at("down the chain to oxygen")
        e=edot((-4.8,.3),.14);self.add(e)
        self.play(Succession(*[e.animate.move_to([x,.3,0]) for x in [-2.6,-.4,1.8,4]]),run_time=1.3)
        self.clear(e,t=.13)
        self.play(Indicate(pumps,scale_factor=1.02),run_time=.3)
        self.at("Watch complex four")
        self.clear(t=.2)
        grip=box(6.4,3.7,GREEN,.12,r=.7)
        oxygen=chip("O₂",ORANGE,42)
        self.show(grip,oxygen,label("Complex IV",(0,2.6),38,GREEN),label("Bound at the heme–copper site",(0,-2.7),26,GREY),t=.35)
        self.at("hold oxygen")
        gates=VGroup(Line([3.2,-1.2,0],[3.2,1.2,0],color=GREEN,stroke_width=9),Line([-3.2,-1.2,0],[-3.2,1.2,0],color=GREEN,stroke_width=9));self.show(gates,t=.4)
        self.at("until it is")
        electrons=VGroup(*[edot((-4.5,-.9+.6*i),.18) for i in range(4)])
        protons=VGroup(*[hdot((4.5,-.9+.6*i),.18) for i in range(4)])
        self.add(electrons,protons,label("4 e⁻",(-4.5,1.5),32,YELLOW),label("4 H⁺",(4.5,1.5),32,BLUE))
        self.play(electrons.animate.move_to([-1.6,0,0]),protons.animate.move_to([1.6,0,0]),run_time=.65)
        self.at("fully reduced to water")
        self.play(Transform(oxygen,chip("2 H₂O",BLUE,42)),FadeOut(electrons),FadeOut(protons),run_time=.6)
        self.play(oxygen.animate.move_to([4.8,0,0]),run_time=.7)
        self.finish()


class S51Close(FilmScene):
    def construct(self):
        self.add(pigment("#251C2A","#372D31"))
        membrane=chain();self.add(membrane)
        self.at("careful grip is the bargain")
        organelle=mito(12,6);self.play(membrane.animate.scale(.55),FadeIn(organelle),run_time=1)
        self.at("Every breath you take")
        group=VGroup(membrane,organelle)
        outer=Ellipse(width=12,height=6.3,stroke_color=AMBER,stroke_width=5,fill_color=AMBER,fill_opacity=.08)
        self.play(group.animate.scale(.45).shift(RIGHT*2),FadeIn(outer),run_time=1)
        whole=VGroup(group,outer)
        water=underwater();self.add(water);self.bring_to_front(whole)
        self.play(whole.animate.scale(.12).shift(DOWN*1.7),run_time=1.1)
        self.at("inherited from that ancient guest")
        self.play(FadeOut(whole),FadeOut(water),FadeIn(landscape(True)),run_time=1.5)
        self.finish()


class S52End(EndCard):
    LINE="Every way of living with oxygen is a way of handling its electrons."
    def construct(self):
        self.add(pigment("#143647","#08151F"))
        self.add(chip("O₂",ORANGE,44).move_to([-4.8,1.9,0]),arr((-3.5,1.9),(3.4,1.9),YELLOW),block("IV",GREEN,1.7,1.5,40).move_to([4.6,1.9,0]))
        self.add(label("Every way of living with oxygen",(0,-.1),36),label("is a way of handling its electrons.",(0,-1.1),36),label("biochemistrypedia.com",(0,-2.8),28,TEAL))
        self.wait(3)
