"""The Nucleus Left Behind — revised, word-cued schematic animation.
COLOR MAP: BLUE progenitors/radial glia/too few; YELLOW neurons/wrong place;
RED mutation/failure; GREEN normal X; ORANGE centrosome; TEAL microtubules;
PURPLE doublecortin; PINK LIS1/nudF; INDIGO dynein; TEXT nuclei; GREY tissue.
All geometry is schematic, not measured anatomy. No molecular structures or data traces.
"""
import numpy as np
from bp_style import *

PURPLE, ORANGE, PINK, INDIGO = "#B58CD9", "#F29E4C", "#EE8CC4", "#7C8CFF"
LESSON_TITLE = "When Building Goes Wrong: Microcephaly, Zika and Lissencephaly"


def label(txt, x, y, color=TEXT, size=30):
    return T(txt, size, color).move_to([x, y, 0])


def arrow(a, b, color=TEXT):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=4, tip_length=0.19)


def leader(txt, x, y, tip, color=TEXT, side=LEFT):
    t = label(txt, x, y, color)
    start = t.get_left() if np.array_equal(side, LEFT) else t.get_right()
    return VGroup(arrow(start, tip, color), t)


def cross(x, y, r=0.22):
    return VGroup(Line([x-r, y-r, 0], [x+r, y+r, 0], color=RED, stroke_width=5),
                  Line([x-r, y+r, 0], [x+r, y-r, 0], color=RED, stroke_width=5))


def neuron(x, y, col=YELLOW, r=0.3):
    return VGroup(Circle(radius=r, color=col, stroke_width=4, fill_color=col, fill_opacity=0.4),
                  Dot(radius=r*0.43, color=TEXT)).move_to([x, y, 0])


def tissue(cx=-2.3, w=7.8):
    out = RoundedRectangle(width=w, height=6.1, corner_radius=0.15, color=GREY).move_to([cx, -0.1, 0])
    cortex = Rectangle(width=w-0.06, height=1.15, stroke_width=0, fill_color=GREY, fill_opacity=0.22).move_to([cx, 2.35, 0])
    vent = Line([cx-w/2+0.15, -2.8, 0], [cx+w/2-0.15, -2.8, 0], color=GREY, stroke_width=8)
    return VGroup(out, cortex, vent)


def brain(cx, cy, kind, s=1):
    """Nested opaque silhouettes make a rim and a separated heterotopic band."""
    th = np.linspace(0, 2*np.pi, 180, endpoint=False)
    def shape(rad, wob, fill, stroke=GREY):
        rr = rad*(1+wob*np.sin(14*th))
        pts = [[cx+2.55*s*r*np.cos(t), cy+2.8*s*r*np.sin(t), 0] for r,t in zip(rr,th)]
        return Polygon(*pts, stroke_color=stroke, stroke_width=2, fill_color=fill, fill_opacity=1)
    if kind == "smooth":
        return VGroup(shape(1, 0, "#A2AAB7"), shape(0.59, 0, "#252B38"))
    outer = shape(1, 0.035, "#A2AAB7")
    white = shape(0.84, 0.025, "#252B38")
    if kind == "band":
        return VGroup(outer, white, shape(0.66, 0, YELLOW, YELLOW), shape(0.50, 0, "#252B38"))
    return VGroup(outer, white)


def cortex_section(cx, kind, numbered=False):
    # Enlarged histological schematics: normal is a magnified reference, explicitly marked.
    n = 6 if kind == "normal" else 4
    w, h, top = 5.3, 4.7, 2.3
    g = VGroup()
    for i in range(n):
        xs = np.linspace(cx-w/2, cx+w/2, 90)
        def boundary(j):
            wave = 0.19*np.sin(3.4*(xs-cx)) if kind == "normal" else 0*xs
            return [[x, top-([0,0.75,2.15,3.2,4.7][j] if kind != "normal" else j*h/n)+v, 0] for x,v in zip(xs,wave)]
        band = Polygon(*(boundary(i)+boundary(i+1)[::-1]), stroke_color=BG, stroke_width=2,
                       fill_color=YELLOW, fill_opacity=0.50 if i%2==0 else 0.25)
        g.add(band)
        if numbered:
            g.add(label(str(i+1), cx-2.25, top-(i+0.5)*h/n, TEXT, 28))
    return g


def chromosome(x, deleted=False):
    st = dict(stroke_color=TEXT, fill_color=TEXT, fill_opacity=0.15, stroke_width=3)
    body = RoundedRectangle(width=1.1, height=4.8, corner_radius=0.45, **st).move_to([x,-0.35,0])
    band = Rectangle(width=1.06, height=0.28, stroke_width=0, fill_color=PINK, fill_opacity=1).move_to([x,1.45,0])
    if deleted:
        body = RoundedRectangle(width=1.1, height=3.9, corner_radius=0.43, **st).move_to([x,-0.8,0])
        band = DashedVMobject(RoundedRectangle(width=1.1, height=0.85, corner_radius=0.2, color=RED).move_to([x,1.6,0]), num_dashes=15)
    return VGroup(body,band)


def motor(x, y, phase=0, s=1.6):
    body = RoundedRectangle(width=1.65*s, height=0.65*s, corner_radius=0.18, color=INDIGO,
                            fill_color=INDIGO, fill_opacity=0.5).move_to([x,y+0.95*s,0])
    feet = [np.array([x+sg*0.4*s+0.16*s*np.sin(phase+idx*np.pi),y+max(0,np.cos(phase+idx*np.pi))*0.12*s,0])
            for idx,sg in enumerate([-1,1])]
    legs = VGroup(*[Line([x+sg*0.32*s,y+0.62*s,0],p,color=INDIGO,stroke_width=7)
                    for sg,p in zip([-1,1],feet)], *[Dot(p,radius=0.11*s,color=INDIGO) for p in feet])
    return VGroup(legs,body,label("dynein",x,y+0.95*s,TEXT,30))


def multi(x,y,r=0.3):
    g = VGroup()
    for a in np.linspace(0,2*np.pi,6,endpoint=False):
        g.add(Line([x+r*np.cos(a),y+r*np.sin(a),0],[x+(r+0.4)*np.cos(a),y+(r+0.4)*np.sin(a),0],color=YELLOW,stroke_width=4))
    g.add(neuron(x,y,r=r))
    return g


class S00Title(TitleCard):
    LESSON = LESSON_TITLE
    TITLE = "The Nucleus Left Behind"
    def construct(self):
        title = T(self.TITLE, 52, TEXT, font=TITLE_FONT)
        lesson = label("WHEN BUILDING GOES WRONG",0,1.4,GREY,28)
        brand = label("BIOCHEMISTRYPEDIA",0,-1.4,TEAL,28)
        rule = Line([-1,-0.75,0],[1,-0.75,0],color=GOLD,stroke_width=4)
        self.add(title,lesson,brand,rule)
        self.finish()


class S01Q(SpokenScene):
    def construct(self):
        a = brain(-3.3,0.15,"normal",0.95)
        b = brain(3.3,0.15,"smooth",0.95)
        self.add(a,b,label("normal, folded",-3.3,3.25),label("lissencephaly",3.3,3.25))
        self.at("neurons are made")
        ns = VGroup(*[neuron(x,-2.3,r=0.16) for x in [-4.4,-3.3,-2.2,2.2,3.3,4.4]])
        cap = label("neurons made",0,-3.25,YELLOW)
        self.play(FadeIn(ns),FadeIn(cap),run_time=0.35)
        self.at("never arrive")
        self.play(*[n.animate.move_to([n.get_x(),0.15+2.8*0.95*0.92*np.sqrt(1-((n.get_x()+3.3)/(2.55*0.95))**2),0]) for n in ns[:3]],*[n.animate.shift(UP*0.6) for n in ns[3:]],run_time=0.7)
        self.finish()


class S02Liss(SpokenScene):
    def construct(self):
        normal = cortex_section(-3.3,"normal",True)
        smooth = cortex_section(3.3,"liss")
        self.add(normal,smooth,label("normal: six layers",-3.3,3.25),label("lissencephaly",3.3,3.25),
                 label("magnified layer comparison",-3.3,-3.15,GREY,28))
        self.at("the cortex is thick")
        thick = label("thick, nearly smooth",3.3,-3.15,YELLOW)
        self.play(FadeIn(thick),run_time=0.35)
        self.at("with about four")
        depths = [0,0.75,2.15,3.2,4.7]
        nums = VGroup(*[label(str(i+1),1.05,2.3-(depths[i]+depths[i+1])/2,TEXT,30) for i in range(4)])
        self.play(FadeIn(nums),Transform(thick,label("about four crude layers",3.3,-3.15,YELLOW)),run_time=0.5)
        self.finish()


class S03Size(SpokenScene):
    def construct(self):
        # Constant extrusion depth: equal cross-sectional areas (6.4*1.4 == 1.6*5.6).
        st = dict(stroke_color=TEXT,fill_color=GREY,fill_opacity=0.45,stroke_width=3)
        base = -2.5
        sheet = Rectangle(width=6.4,height=1.4,**st).move_to([-3,base+0.7,0])
        block = Rectangle(width=1.6,height=5.6,**st).move_to([4.3,base+2.8,0])
        eq = label("=",1.65,-0.55,TEXT,64)
        self.add(sheet,block,eq,label("volume = area × thickness",0,3.5,TEXT,36),
                 label("same volume",1.65,-1.4,TEXT,28),label("large area, thin",-3,-3.0),
                 label("¼ area, 4× thick",4.3,-3.0),label("plausibility check only",0,-3.6,YELLOW,32))
        self.at("the head is")
        self.play(Indicate(eq,scale_factor=1.1),run_time=0.5)
        self.at("near normal")
        self.play(Indicate(sheet,scale_factor=1.02),Indicate(block,scale_factor=1.02),run_time=0.7)
        self.finish()


class S04Mdl(SpokenScene):
    def construct(self):
        normal, deleted = chromosome(-2),chromosome(2,True)
        self.add(normal,deleted,label("Miller-Dieker syndrome",0,3.25,RED,34),
                 label("normal copy",-2,-3.2,GREEN),label("deleted copy",2,-3.2,RED))
        self.at("a piece of")
        reg = leader("17p13.3\ndeleted",4.7,1.6,[2.6,1.6,0],RED)
        self.play(FadeIn(reg),run_time=0.5)
        self.at("one chromosome")
        self.play(FadeIn(label("chromosome 17",-4.65,-0.4,GREY,28)),run_time=0.35)
        self.at("including")
        lis = leader("LIS1",-4.65,1.45,[-2.6,1.45,0],PINK,RIGHT)
        self.play(FadeIn(lis),run_time=0.4)
        self.finish()


class S05Half(SpokenScene):
    def construct(self):
        self.add(chromosome(-4.9),chromosome(-2.5,True),label("normal copy",-4.9,-3.1,GREEN,28),
                 label("broken copy",-2.5,-3.1,RED,28),label("LIS1",-3.7,2.65,PINK,34))
        box = Rectangle(width=1.3,height=4.5,color=TEXT).move_to([1.1,-0.15,0])
        full = Rectangle(width=1.25,height=4.45,stroke_width=0,fill_color=PINK,fill_opacity=0.65).move_to(box)
        half = Rectangle(width=1.25,height=2.225,stroke_width=0,fill_color=PINK,fill_opacity=0.65).move_to([1.1,-1.2625,0])
        self.add(box,half,label("usual dose",3.45,2.1,TEXT,28),DashedLine([0.3,2.1,0],[2.3,2.1,0],color=TEXT))
        self.at("one copy")
        self.play(Indicate(half,scale_factor=1.03),run_time=0.6)
        self.at("still causes")
        result = chip("lissencephaly",RED,30).move_to([3.5,3.1,0])
        hap = VGroup(label("haploinsufficiency",2.5,-2.8,RED,32),label("half the usual dose is too little",2.5,-3.35,TEXT,28))
        hl = leader("half a dose",3.9,-1.1,[1.8,-1.1,0],PINK)
        self.play(FadeIn(result),FadeIn(hap),FadeIn(hl),run_time=0.4)
        self.at("half a dose")
        self.play(Indicate(half,scale_factor=1.03),run_time=0.35)
        self.at("too little")
        self.play(Indicate(hap,scale_factor=1.015),run_time=0.4)
        self.finish()


class S06Mould(SpokenScene):
    def construct(self):
        ys = [1.65,-0.3]
        rows = VGroup(*[RoundedRectangle(width=10.6,height=1.8,corner_radius=0.8,color=GREY,
                          fill_color=GREY,fill_opacity=0.12).move_to([0.9,y,0]) for y in ys])
        nx = np.linspace(-3.2,5,5)
        nuclei = [VGroup(*[Dot([x,y,0],radius=0.3,color=TEXT) for x in (nx if j==0 else [-3.15+i*0.7 for i in range(5)])]) for j,y in enumerate(ys)]
        self.add(rows,nuclei[0],label("mould filament",0,3.55,TEXT,34),label("normal",-5.3,1.65,GREY),label("nudF\nmutant",-5.3,-0.3,PINK))
        self.at("its relative of")
        self.play(FadeIn(nuclei[1]),FadeIn(label("nudF: 42% identical to human LIS1",0,2.95,PINK,30)),run_time=0.4)
        self.at("helps space nuclei")
        self.play(Indicate(nuclei[0],scale_factor=1.02),Indicate(nuclei[1],color=RED,scale_factor=1.08),run_time=0.8)
        self.at("as do parts of dynein")
        tube = Rectangle(width=10.6,height=0.26,color=TEAL,fill_color=TEAL,fill_opacity=0.6).move_to([0.9,-2.8,0])
        mot = motor(1.9,-2.67,s=1.05)
        track_label = label("microtubule",-2.3,-2.3,TEAL,30)
        link = DashedLine([-3.9,-1.2,0],[-3.9,-2.65,0],color=TEAL,stroke_width=3)
        caption = label("dynein: the motor",1.9,-3.4,INDIGO,32)
        self.play(FadeIn(tube),FadeIn(track_label),FadeIn(link),FadeIn(mot),FadeIn(caption),run_time=0.45)
        self.at("a microtubule motor")
        self.play(mot.animate.shift(RIGHT*1.6),run_time=0.65)
        self.finish()


class S07Dynein(SpokenScene):
    def construct(self):
        y=-1.55
        pos = ValueTracker(-2.7)
        phase = ValueTracker(0)
        dyn = always_redraw(lambda:motor(pos.get_value(),y,phase.get_value(),1.65))
        tube = Rectangle(width=12.1,height=0.28,color=TEAL,fill_color=TEAL,fill_opacity=0.65).move_to([0,y-0.14,0])
        self.add(tube,dyn,label("mammalian cell",0,3.25,TEXT,34),label("plus end",-5,-2.35,GREY),
                 label("minus end",5,-2.35,TEXT),label("microtubule",0,-2.35,TEAL),
                 arrow([-3,-3.15,0],[3,-3.15,0],INDIGO))
        def cofactors():
            x=pos.get_value()
            lis=chip("LIS1",PINK,30).move_to([x,1.2,0])
            n1=chip("NDE1",GREY,28).move_to([x-1.7,2.25,0])
            n2=chip("NDEL1",GREY,28).move_to([x+1.7,2.25,0])
            return VGroup(Line(lis.get_top(),n1.get_bottom(),color=GREY),Line(lis.get_top(),n2.get_bottom(),color=GREY),
                          Line(lis.get_bottom(),[x,0.55,0],color=PINK),lis,n1,n2)
        self.at("in mammalian cells")
        self.play(pos.animate.set_value(-1.8),phase.animate.set_value(2*np.pi),run_time=1.2,rate_func=linear)
        self.at("binds dynein")
        co=always_redraw(cofactors)
        self.add(co)
        self.at("helps it work")
        self.play(pos.animate.set_value(2.5),phase.animate.set_value(8*np.pi),run_time=1.1,rate_func=linear)
        self.finish()


class S08Steps(SpokenScene):
    def construct(self):
        x=0.0
        sy,ty,cy=ValueTracker(-2.1),ValueTracker(-1.4),ValueTracker(-1.4)
        fibre=Line([x-1.4,-3.2,0],[x-1.4,3.1,0],color=BLUE,stroke_width=8)
        proc=always_redraw(lambda:Rectangle(width=1.1,height=max(0.1,ty.get_value()-sy.get_value()),stroke_width=0,
                    fill_color=YELLOW,fill_opacity=0.35).move_to([x,(ty.get_value()+sy.get_value())/2,0]))
        soma=always_redraw(lambda:Ellipse(width=2.7,height=1.85,color=YELLOW,fill_color=YELLOW,fill_opacity=0.3).move_to([x,sy.get_value(),0]))
        nuc=always_redraw(lambda:Circle(radius=0.55,color=TEXT,fill_color=TEXT,fill_opacity=1).move_to([x,sy.get_value(),0]))
        cen=always_redraw(lambda:Dot([x,cy.get_value(),0],radius=0.21,color=ORANGE))
        self.add(fibre,proc,soma,nuc,cen,label("a migrating neuron",0,3.35,TEXT,34),
                 leader("radial glial\nfibre",-4.4,2.25,[x-1.45,2.25,0],BLUE,RIGHT),
                 always_redraw(lambda:leader("nucleus",-4.4,-1.9,[x-0.6,sy.get_value(),0],TEXT,RIGHT)))
        self.at("first")
        l1=leader("1  leading process\nextends",3.9,2.3,[x+0.6,2.3,0],YELLOW)
        self.play(FadeIn(l1),run_time=0.3)
        self.at("the leading process")
        self.play(ty.animate.set_value(2.6),run_time=1.1)
        self.at("and the centrosome")
        cl=leader("centrosome",3.9,0.8,[x+0.25,1.35,0],ORANGE)
        self.play(cy.animate.set_value(1.35),FadeIn(cl),run_time=1.0)
        # Long, thick tracks fan back from the centrosome to the nuclear surface.
        tracks=always_redraw(lambda:VGroup(*[Line([x+dx*0.2,cy.get_value(),0],[x+dx,sy.get_value()+0.55,0],color=TEAL,stroke_width=9) for dx in [-0.8,0.8]]))
        motors=always_redraw(lambda:VGroup(*[RoundedRectangle(width=0.52,height=0.36,corner_radius=0.08,color=INDIGO,
                     fill_color=INDIGO,fill_opacity=1).move_to([x+dx*0.6,(cy.get_value()+sy.get_value()+0.55)/2,0]) for dx in [-0.8,0.8]]))
        self.at("then dynein pulls")
        l2=leader("2  dynein pulls\nthe nucleus up",3.9,-1.7,[x+0.85,-0.1,0],INDIGO)
        self.play(FadeIn(tracks),FadeIn(motors),FadeIn(l2),run_time=0.4)
        self.at("up toward")
        self.play(sy.animate.set_value(0.45),run_time=0.95)
        self.finish()


# Three readable alternatives, without the unexplained fourth panel.
def prediction_board():
    cols=VGroup()
    names=["process fails?","nucleus fails?","earlier failure?"]
    for x,name in zip([-4.2,0,4.2],names):
        pan=RoundedRectangle(width=3.9,height=5.2,corner_radius=0.15,color=GREY).move_to([x,-0.2,0])
        title=label(name,x,1.85,TEXT,30)
        if x==4.2:
            cell=multi(x,-0.4,0.42)
            note=label("never starts\nmigration",x,-2.0,YELLOW,28)
        else:
            cell=neuron(x,-1.7,r=0.45)
            line=Line([x,-1.2,0],[x,0.9 if x==0 else -0.4,0],color=YELLOW,stroke_width=12)
            cell.add(line,Dot([x,0.9 if x==0 else -0.4,0],radius=0.16,color=ORANGE))
            note=label("no extension" if x<0 else "no nuclear travel",x,-2.45,YELLOW,28)
        cols.add(VGroup(pan,title,cell,note))
    return VGroup(cols,label("knock down LIS1",-3.2,3.25,PINK,32),label("embryonic rat cortex",3.2,3.25,TEXT,30),
                  label("Pause and predict",0,-3.35,TEXT,30))


def countdown(scene):
    # The question diagram stays fixed; only a small clock at the edge changes.
    clock=label("5",6.25,-3.35,YELLOW,32)
    scene.add(clock)
    for n in range(5,0,-1):
        clock.become(label(str(n),6.25,-3.35,YELLOW,32))
        scene.wait(1)
    scene.finish()


class S09Pred(SpokenScene):
    def construct(self):
        g=prediction_board()
        self.add(g[0],g[3])
        self.at("knock down")
        self.play(FadeIn(g[1]),run_time=0.35)
        self.at("embryonic rat cortex")
        self.play(FadeIn(g[2]),run_time=0.35)
        self.at("does the process")
        self.play(Indicate(g[0][0][0],color=YELLOW,scale_factor=1.015),run_time=0.45)
        self.at("the nucleus")
        self.play(Indicate(g[0][1][0],color=YELLOW,scale_factor=1.015),run_time=0.45)
        self.at("or something earlier")
        self.play(Indicate(g[0][2][0],color=YELLOW,scale_factor=1.015),run_time=0.45)
        self.finish()


class S10Pause(NarratedScene):
    def construct(self):
        self.add(prediction_board())
        countdown(self)


def reveal_state(grown=True):
    left=tissue(-3.25,5.8)
    right=tissue(3.25,5.8)
    cells=VGroup(*[multi(x,y) for x,y in [(-5,-1.95),(-3.25,-1.95),(-1.5,-1.95),(-4.25,-0.35),(-2.3,-0.35)]])
    soma=neuron(3.25,-2.1,r=0.48)
    proc=Line([3.25,-1.6,0],[3.25,2.2 if grown else -0.8,0],color=YELLOW,stroke_width=14)
    labs=VGroup(label("most: multipolar",-3.25,3.25,YELLOW,32),label("few: bipolar",3.25,3.25,YELLOW,32),
                label("near the ventricle",-3.25,1.05,TEXT,28),
                label("Tsai and colleagues, 2005 · embryonic rats",0,-3.55,GREY,28))
    return VGroup(left,right,cells,proc,soma,labs)


class S11Reveal(SpokenScene):
    def construct(self):
        g=reveal_state(False)
        self.add(g)
        self.at("in the few")
        self.play(Indicate(g[4],scale_factor=1.12),run_time=0.4)
        self.at("process kept growing")
        grown=Line([3.25,-1.6,0],[3.25,2.2,0],color=YELLOW,stroke_width=14)
        pl=leader("keeps\ngrowing",4.95,0.65,[3.4,0.65,0],YELLOW)
        self.play(Transform(g[3],grown),FadeIn(pl),run_time=0.9)
        self.at("but the nucleus")
        nl=leader("nucleus\nstays low",1.35,-2.1,[2.7,-2.1,0],TEXT,RIGHT)
        self.play(FadeIn(nl),Indicate(g[4],color=RED,scale_factor=1.12),run_time=0.6)
        self.finish()


class S12Beat(NarratedScene):
    def construct(self):
        self.add(reveal_state(),leader("keeps\ngrowing",4.95,0.65,[3.4,0.65,0],YELLOW),
                 leader("nucleus\nstays low",1.35,-2.1,[2.7,-2.1,0],TEXT,RIGHT))
        self.finish()


class S13Prog(SpokenScene):
    def construct(self):
        pan=tissue(-2.4,7.6)
        cells=VGroup()
        for x in [-5.3,-3.9,-2.5,-1.1,0.3]:
            cells.add(VGroup(Line([x,-1.45,0],[x,-0.8,0],color=BLUE,stroke_width=4),
                            Ellipse(width=0.8,height=1.0,color=BLUE,fill_color=BLUE,fill_opacity=0.3).move_to([x,-1.9,0]),
                            Dot([x,-1.9,0],radius=0.19,color=TEXT)))
        self.add(pan,cells,label("LIS1 knockdown",-2.4,3.3,PINK,34),label("ventricle",-2.4,-3.4,GREY,30),
                 VGroup(label("progenitor nuclei",-2.4,-0.3,TEXT,30),arrow([-2.5,-0.6,0],[-2.5,-1.65,0],TEXT)))
        self.at("blocked progenitor")
        blocked=VGroup(*[cross(x,-2.65,0.15) for x in [-5.3,-3.9,-2.5,-1.1,0.3]])
        caption=label("progenitor divisions\nblocked",-2.4,1.25,RED,32)
        self.play(FadeIn(blocked),FadeIn(caption),run_time=0.5)
        # Compact sorting board: explicit definitions; LIS1 bridges its shared boundary.
        a=Rectangle(width=2.3,height=4.4,color=YELLOW).move_to([2.65,0.1,0])
        b=Rectangle(width=2.3,height=4.4,color=BLUE).move_to([4.95,0.1,0])
        defs=VGroup(label("wrong place",2.65,1.75,YELLOW,27),label("failed\nmigration",2.65,0.7,TEXT,28),
                    label("too few",4.95,1.75,BLUE,28),label("fewer\nneurons\nmade",4.95,0.7,TEXT,27))
        self.at("so lis1")
        small=chip("LIS1",PINK,32).move_to([2.65,-1.1,0])
        self.play(FadeIn(VGroup(a,b,defs,small)),run_time=0.45)
        self.at("one foot in")
        bridge=chip("LIS1",PINK,36,pad=0.45).move_to([3.8,-1.1,0])
        bridge[0].set_fill(BG,opacity=1)
        small.set_z_index(3)
        self.play(Transform(small,bridge),run_time=0.6)
        self.wait(3.0)
        self.finish()


class S14Dcx(SpokenScene):
    def construct(self):
        xchr=VGroup(RoundedRectangle(width=0.9,height=4.4,corner_radius=0.4,color=TEXT).move_to([-5.2,0.6,0]),
                    Rectangle(width=0.85,height=0.22,stroke_width=0,fill_color=PURPLE,fill_opacity=1).move_to([-5.2,1.9,0]))
        self.add(xchr,label("X",-5.2,-2.2,TEXT,34),leader("DCX",-3.5,1.9,[-4.7,1.9,0],PURPLE))
        blob=Ellipse(width=2.4,height=1.4,color=PURPLE,fill_color=PURPLE,fill_opacity=0.5).move_to([1,1.9,0])
        self.at("makes double cortin")
        self.play(FadeIn(blob),FadeIn(label("doublecortin",1,3.2,PURPLE,36)),run_time=0.45)
        self.at("not a motor")
        no=label("not a motor",3.8,1.8,TEXT,32)
        self.play(FadeIn(no),run_time=0.35)
        tube=RoundedRectangle(width=9.8,height=0.6,corner_radius=0.2,color=TEAL,fill_color=TEAL,fill_opacity=0.35).move_to([0.8,-0.5,0])
        self.at("it binds microtubules")
        blobs=VGroup(*[Ellipse(width=0.9,height=0.65,color=PURPLE,fill_color=PURPLE,fill_opacity=0.6).move_to([x,-0.06,0]) for x in [-3,-1.1,0.8,2.7,4.6]])
        bind=label("binds microtubules",0.8,-1.65,PURPLE,32)
        self.play(FadeIn(tube),ReplacementTransform(blob,blobs),FadeIn(bind),run_time=0.6)
        self.at("steady the tracks")
        braces=VGroup(*[Line([x,-0.2,0],[x,-0.8,0],color=PURPLE,stroke_width=8) for x in [-3,-1.1,0.8,2.7,4.6]])
        self.play(tube.animate.set_stroke(width=8),FadeIn(braces),FadeIn(label("thought mainly to steady the tracks",0.8,-3.1,TEXT,30)),run_time=0.5)
        self.finish()


def puzzle_heads():
    return VGroup(brain(-3.25,-0.05,"smooth",0.97),brain(3.25,-0.05,"band",0.97),
                  label("boy · thick, smooth",-3.25,-3.25,TEXT,30),label("mother · second band",3.25,-3.25,YELLOW,30))


class S15Hook(SpokenScene):
    def construct(self):
        # Unknown insides are filled only as each phenotype is named.
        outlines=VGroup(*[Ellipse(width=4.95,height=5.43,color=GREY).move_to([x,-0.05,0]) for x in [-3.25,3.25]])
        qs=VGroup(*[label("?",x,0,TEXT,80) for x in [-3.25,3.25]])
        c1,c2=label("boy",-3.25,-3.25),label("mother",3.25,-3.25)
        self.add(outlines,qs,c1,c2)
        self.at("share a mutation")
        self.play(FadeIn(label("same doublecortin mutation",0,3.35,PURPLE,34)),run_time=0.4)
        heads=puzzle_heads()
        self.at("he has a smooth brain")
        self.play(FadeOut(outlines[0]),FadeOut(qs[0]),FadeIn(heads[0]),run_time=0.5)
        self.play(Transform(c1,heads[2]),run_time=0.2)
        self.at("she has a second band")
        self.play(FadeOut(outlines[1]),FadeOut(qs[1]),FadeIn(heads[1]),run_time=0.45)
        band=leader("band",3.25,0.05,[4.68,0.05,0],YELLOW,RIGHT)
        self.play(FadeIn(band),Transform(c2,heads[3]),run_time=0.25)
        self.wait(2.6)
        self.finish()


class S16Xi(SpokenScene):
    def construct(self):
        male=VGroup(Circle(radius=1.7,color=GREY),label("X",0,0,TEXT,100)).move_to([-4.3,0,0])
        cells,active,silent=VGroup(),[],[]
        for i,(x,y) in enumerate([(0,1.35),(2.7,1.35),(5.4,1.35),(0,-1.25),(2.7,-1.25),(5.4,-1.25)]):
            circ=Circle(radius=1.05,color=GREY,fill_color=GREY,fill_opacity=0.09).move_to([x,y,0])
            a=label("X",x-0.38,y,TEXT,48)
            b=label("X",x+0.38,y,TEXT,48)
            active.append(a if i%2 else b)
            silent.append(b if i%2 else a)
            cells.add(VGroup(circ,a,b))
        self.add(male,label("male: one X",-4.3,2.65,TEXT,32),label("female cells: two Xs",2.7,3.25,TEXT,32))
        self.at("each of a female's cells")
        self.add(cells)
        self.at("silences one",lead=0.35)
        strikes=VGroup(*[Line(s.get_corner(DL),s.get_corner(UR),color=TEXT,stroke_width=5) for s in silent])
        xi=label("X inactivation, at random",2.5,-3.15,TEXT,32)
        self.play(*[s.animate.set_color("#454C59") for s in silent],FadeIn(strikes),FadeIn(xi),run_time=0.3)
        self.finish()


def second_question():
    return VGroup(puzzle_heads(),label("Explain both brains",0,3.35,TEXT,36),
                  label("Pause and predict",0,-3.6,TEXT,28))


class S17Pred2(SpokenScene):
    def construct(self):
        g=second_question()
        self.add(g[0])
        self.at("explain both brains")
        self.play(FadeIn(g[1]),FadeIn(g[2]),run_time=0.4)
        self.finish()


class S18Pause(NarratedScene):
    def construct(self):
        self.add(second_question())
        countdown(self)


# Cortex tanks use the full left 60%, with a large anatomical result on the right.
CX=-2.3
XS=np.linspace(-5.5,0.9,8)
PATTERN=[GREEN,RED,RED,GREEN,RED,GREEN,GREEN,RED]


def tank_labels(tag):
    return VGroup(label(tag,CX,3.4,TEXT,32),label("cortex",CX,2.65,TEXT,28),label("ventricle",CX,-3.45,GREY,28))


class S19Boy(SpokenScene):
    def construct(self):
        cells=[neuron(x,-2.25,RED) for x in XS]
        xmut=label("X",4.15,2.25,TEXT,64)
        self.add(tissue(),tank_labels("BOY · human schematic"),label("one X, no choice",4.15,3.15,TEXT,30),xmut)
        self.at("carries the mutation")
        self.play(xmut.animate.set_color(RED),FadeIn(label("severe loss of function,\nin every cell",4.1,0.8,RED,29)),run_time=0.4)
        self.at("so no neuron")
        self.play(*[FadeIn(n) for n in cells],run_time=0.4)
        self.at("makes working double cortin")
        rise=[0.7,1.1,0.8,1.3,0.6,1.1,4.35,0.8]
        self.play(*[n.animate.shift(UP*r) for n,r in zip(cells,rise)],run_time=1.3)
        self.at("most stall")
        self.play(FadeIn(label("most neurons stall",CX,0.5,RED,32)),run_time=0.4)
        self.at("the cortex is smooth")
        b=brain(4.15,-1.45,"smooth",0.62)
        self.play(FadeIn(b),run_time=0.5)
        self.play(FadeIn(label("smooth cortex",4.15,-3.5,TEXT,28)),run_time=0.2)
        self.wait(2.6)
        self.finish()


class S20Mom(SpokenScene):
    def construct(self):
        cells=[neuron(x,-2.25,c) for x,c in zip(XS,PATTERN)]
        greens=[i for i,c in enumerate(PATTERN) if c==GREEN]
        reds=[i for i,c in enumerate(PATTERN) if c==RED]
        head=brain(4.15,-1.35,"normal",0.65)
        self.add(tissue(),*cells,tank_labels("MOTHER · human schematic"),head,
                 label("normal X active",4.15,2.65,GREEN,30),label("mutant X active",4.15,1.9,RED,30))
        self.at("a mosaic")
        self.wait(0.4)
        self.at("neurons with the normal")
        self.play(*[Indicate(cells[i],scale_factor=1.15) for i in greens],run_time=0.4)
        self.at("arrive")
        self.play(*[cells[i].animate.move_to([x,1.95,0]) for i,x in zip(greens,np.linspace(-5.2,0.6,len(greens)))],run_time=0.65)
        self.at("those with the mutant")
        self.play(*[Indicate(cells[i],scale_factor=1.15) for i in reds],run_time=0.4)
        self.at("stall partway")
        self.play(*[cells[i].animate.move_to([XS[i],-0.3,0]) for i in reds],run_time=0.65)
        self.at("gather into a band")
        band=RoundedRectangle(width=7.2,height=1.0,corner_radius=0.1,color=RED,fill_color=RED,fill_opacity=0.12).move_to([CX,-0.3,0])
        self.play(FadeIn(band),Transform(head,brain(4.15,-1.35,"band",0.65)),
                  FadeIn(label("second band",4.15,-3.55,YELLOW,30)),*[cells[i].animate.move_to([x,-0.3,0]) for i,x in zip(reds,np.linspace(-5.2,0.6,len(reds)))],run_time=0.6)
        self.at("beneath the cortex")
        self.play(FadeIn(label("second band / heterotopia",CX,0.65,YELLOW,30)),run_time=0.35)
        self.finish()


def rat_state():
    ns={}
    silenced=[1,2,4,7]
    normal=[0,3,5,6]
    for i,x in enumerate(XS):
        ns[i]=neuron(x,-0.3 if i in silenced else 1.95,RED if i in silenced else YELLOW)
    band=RoundedRectangle(width=7.2,height=1,corner_radius=0.1,color=RED,fill_color=RED,fill_opacity=0.12).move_to([CX,-0.3,0])
    return VGroup(tissue(),tank_labels("RAT · embryonic cortex"),band,*ns.values()),ns,normal,silenced


class S21Rat(SpokenScene):
    def construct(self):
        cells=[neuron(x,-2.25,RED if i in [1,2,4,7] else YELLOW) for i,x in enumerate(XS)]
        self.add(tissue(),*cells,tank_labels("RAT · embryonic cortex"),label("RAT EXPERIMENT",4.2,2.6,TEAL,32),
                 label("doublecortin\nsilenced",4.2,1.2,RED,32))
        self.at("stalled")
        self.play(*[n.animate.move_to([XS[i],-0.3 if i in [1,2,4,7] else 1.95,0]) for i,n in enumerate(cells)],run_time=0.6)
        self.at("formed such a band")
        band=RoundedRectangle(width=7.2,height=1,corner_radius=0.1,color=RED,fill_color=RED,fill_opacity=0.12).move_to([CX,-0.3,0])
        self.add(label("band beneath\ncortex",4.2,-0.7,YELLOW,34))
        self.play(FadeIn(band),run_time=0.45)
        self.finish()


class S22Caveat(SpokenScene):
    def construct(self):
        g,ns,normal,silenced=rat_state()
        # Keep the rat result legible while reserving half the screen for the key caveat.
        g.scale(0.8,about_point=[CX,0,0]).shift(LEFT*1.35)
        self.add(g,label("some neighbours\ndisturbed too",3.3,2.65,YELLOW,36))
        self.at("some neighbors")
        self.play(*[ns[i].animate.shift(DOWN*0.8) for i in normal[:3]],run_time=0.8)
        self.at("the sorting")
        box=RoundedRectangle(width=6.6,height=4.6,corner_radius=0.2,color=TEXT).move_to([3.3,-0.6,0])
        heading=label("HUMAN TISSUE",3.3,1.1,TEXT,32)
        incomplete=label("human evidence\nremains incomplete",3.3,-2.05,TEXT,34)
        self.play(FadeIn(box),FadeIn(heading),FadeIn(incomplete),run_time=0.35)
        self.at("not been traced")
        claim=label("not traced\nneuron by neuron",3.3,-0.45,TEXT,44)
        self.add(claim)
        self.finish()


def takeaway_diagrams():
    # Generation counts are computed, rather than a decorative hand-drawn tree.
    tree=VGroup()
    for gen in range(4):
        n=2**gen
        ys=np.linspace(-1.8,1.6,n) if n>1 else [-0.1]
        x=-5.9+gen*1.65
        for j,y in enumerate(ys):
            if gen:
                prevn=2**(gen-1)
                py=np.linspace(-1.8,1.6,prevn)[j//2] if prevn>1 else -0.1
                tree.add(Line([x-1.65,py,0],[x,y,0],color=BLUE,stroke_width=3))
            tree.add(Dot([x,y,0],radius=0.13,color=BLUE))
    layers=VGroup(*[Rectangle(width=4.5,height=0.6,stroke_color=BG,stroke_width=2,fill_color=YELLOW,
                    fill_opacity=0.45 if i%2==0 else 0.23).move_to([3.35,1.6-i*0.6,0]) for i in range(6)])
    return tree,layers


class S23Take(SpokenScene):
    def construct(self):
        tree,layers=takeaway_diagrams()
        # Fully populated from the first frame; the named concept is highlighted on its cue.
        self.add(tree,layers,label("size",-3.35,2.8,BLUE,38),label("layering",3.35,2.8,YELLOW,38))
        self.at("size counts")
        self.play(Indicate(tree,scale_factor=1.025),FadeIn(label("counts the doublings",-3.35,-2.85,TEXT,32)),run_time=0.5)
        self.at("layering records")
        self.play(Indicate(layers,scale_factor=1.025),run_time=0.3)
        self.at("the journey")
        runner=neuron(3.35,-2.45,r=0.18)
        self.add(runner)
        path=arrow([3.35,-2.2,0],[3.35,1.55,0],YELLOW)
        self.play(GrowArrow(path),runner.animate.move_to([3.35,1.55,0]),FadeIn(label("records the journey",3.35,-2.85,TEXT,32)),run_time=0.7)
        self.wait(2.6)
        self.finish()


class S24End(EndCard):
    LINE = "Size counts the doublings. Layering records the journey."
    def construct(self):
        line=T("Size counts the doublings.\nLayering records the journey.",42,TEXT,font=TITLE_FONT,line_spacing=1.2)
        self.add(line,label("biochemistrypedia.com",0,-1.6,TEAL,28))
        self.finish()
