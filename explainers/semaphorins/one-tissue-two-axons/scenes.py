"""One Tissue, Two Axons, One Receptor.

COLOR MAP (from ../scenes.old.py; shared across the series):
TEAL growth cones/axons; YELLOW Sema3A; BLUE neuropilin;
PURPLE plexin/inner domain; ORANGE small GTPase/integrin adhesion;
GOLD GTP badge; GREEN response; RED blocked/off/lost;
GREY membranes/structure/unknown. Assay identity exception required by
script.visual: pain fibres RED, muscle afferents BLUE.

Assay rays are calculated, not drawn freehand: radial length interpolates
between the script's illustrative near/far values with (1+cos(theta))/2.
These are explanatory schematics, not experimental measurements.
Fan, membrane, receptor and cue geometry adapted from scenes.old.py.
"""
import numpy as np
from bp_style import *
from bp_style import SpokenScene as BaseSpokenScene


class SpokenScene(BaseSpokenScene):
    """Use the actual word onset, with no anticipatory offset."""
    def at(self, phrase, lead=0, nth=0):
        target = self.t_of(phrase, nth)
        if target > self.elapsed():
            self.wait(target - self.elapsed(), frozen_frame=False)
        # Record the time AFTER waiting, rather than the pre-wait diagnostic.
        with open("/tmp/one-tissue-cues.tsv", "a") as f:
            f.write(f"{type(self).__name__}\t{phrase}\t{target:.3f}\t{self.elapsed():.3f}\n")


PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


def rr(w, h, color, op=.18, sw=3, r=.18):
    return RoundedRectangle(width=w, height=h, corner_radius=min(r,w/2.2,h/2.2),
        color=color, stroke_width=sw, fill_color=color, fill_opacity=op)


def header(text, color=TEXT):
    return T(text, 30, color).move_to([0,3.15,0])


def semag(x, y, w=1.8, h=.65):
    e=Ellipse(width=w,height=h,color=YELLOW,fill_color=YELLOW,fill_opacity=.85).move_to([x,y,0])
    return VGroup(e,T("Sema3A",26,BG).move_to(e))


def mem_bar(y=0,x0=-5.8,x1=5.8):
    return rr(x1-x0,.25,GREY,.3).move_to([(x0+x1)/2,y,0])


def fan(a0=-.85,a1=.85,r=2,c=(-2,0,0)):
    c=np.array(c,float)
    pts=[c+np.array([0,.22,0])]
    pts += [c+r*np.array([np.cos(a),np.sin(a),0]) for a in np.linspace(a1,a0,13)]
    pts += [c+np.array([0,-.22,0])]
    return Polygon(*pts,color=TEAL,fill_color=TEAL,fill_opacity=.22,stroke_width=4)


def growth(c=(-2,0,0),r=2):
    c=np.array(c,float)
    shaft=Line(c+LEFT*1.1,c,color=TEAL,stroke_width=20,stroke_opacity=.4)
    f=fan(r=r,c=c)
    hairs=VGroup(*[Line(c+r*np.array([np.cos(a),np.sin(a),0]),
            c+(r+.35)*np.array([np.cos(a),np.sin(a),0]),color=TEAL,stroke_width=3)
            for a in np.linspace(-.8,.8,7)])
    return VGroup(shaft,f,hairs)


def dish(x=0,y=0,medium=None,cells=False):
    frame=rr(5.9,3.9,GREY,.06).move_to([x,y,0])
    gang=Circle(radius=.4,color=TEAL,fill_color=TEAL,fill_opacity=.45).move_to([x-.75,y,0])
    cord=rr(.65,1.45,YELLOW,.24).move_to([x+1.9,y,0])
    if cells:
        cord=VGroup(*[Circle(radius=.18,color=YELLOW,fill_color=YELLOW,fill_opacity=.4)
                     .move_to([x+1.8+dx,y+dy,0]) for dx,dy in [(0,0),(.3,.4),(.3,-.4)]])
    label=T("Sema3A cells" if cells else "ventral cord",26,YELLOW).move_to([x+1.6,y-1.42,0])
    drg=T("DRG",26,BG).move_to(gang)
    g=VGroup(frame,gang,cord,drg,label)
    if medium: g.add(T(medium,28,RED if medium=="NGF" else BLUE).move_to([x,y+2.45,0]))
    return g


def halo(x,ratio,color,y=0):
    # Script data: far=600; near=150 (NGF) or 540 (NT-3).
    # Length units are micrometres; these are made-up mean lengths.
    g=VGroup()
    c=np.array([x-.75,y,0])
    for a in np.linspace(0,2*np.pi,28,endpoint=False):
        length=1.25*(1-(1-ratio)*(1+np.cos(a))/2)
        d=np.array([np.cos(a),np.sin(a),0])
        g.add(Line(c+.42*d,c+(.42+length)*d,color=color,stroke_width=5))
    return g


def assays(ngf=False,nt3=False,cells=False):
    g=VGroup(dish(-3.15,medium="NGF",cells=cells),dish(3.15,medium="NT-3",cells=cells))
    if ngf:g.add(halo(-3.15,.25,RED))
    if nt3:g.add(halo(3.15,.9,BLUE))
    return g


def assay_question():
    return T("Where will the axons grow?",32).move_to([0,-2.8,0])


def receptor(kind,x,cut=False,ym=0):
    color=BLUE if kind=="neuropilin" else PURPLE
    if kind=="neuropilin":
        # Open cup: cue enters the mitt. No molecular structure is implied.
        body=Polygon([x-.9,ym+1.8,0],[x-.9,ym+.8,0],[x,ym+.35,0],
                     [x+.9,ym+.8,0],[x+.9,ym+1.8,0],
                     color=color,fill_color=color,fill_opacity=.12)
        # Hide the top closing segment to make the mitt visibly open.
        body.set_stroke(width=0)
        edge=VMobject(color=color,stroke_width=5).set_points_as_corners([
            [x-.9,ym+1.8,0],[x-.9,ym+.8,0],[x,ym+.35,0],[x+.9,ym+.8,0],[x+.9,ym+1.8,0]])
        body=VGroup(body,edge)
        label=T(kind,26,color).move_to([x,ym+1.05,0])
    else:
        body=rr(1.8,1.5,color).move_to([x,ym+1.05,0])
        label=T(kind,28,color).move_to(body)
    neck=Line([x,ym+.35,0],[x,ym-.15,0],color=color,stroke_width=10)
    length=.3 if kind=="neuropilin" else 1.9
    tail=rr(.32,length,color,.5,r=.06).move_to([x,ym-.15-length/2,0])
    if cut:tail.set_opacity(0)
    return VGroup(body,label,neck,tail)


def receptor_stage(plex=True,cutn=False,cutp=False):
    mem=mem_bar(-.2)
    n=receptor("neuropilin",-1.7,cutn,ym=-.2).scale(1.35,about_point=[-1.7,-.2,0])
    p=receptor("plexin",1.1,cutp,ym=-.2).scale(1.35,about_point=[1.1,-.2,0])
    cue=semag(-1.7,2.08,2,.7)
    labels=VGroup(T("outside",28).move_to([-4.8,1.8,0]),
                  T("inside the cell",28).move_to([-4.5,-1.8,0]))
    g=VGroup(mem,n,cue,labels)
    if plex:g.add(p)
    return g,n,p,cue


def pause_cue(scene,y=-3.3):
    lab=T("Pause and predict",28,GOLD).move_to([0,y+.55,0])
    bar=Rectangle(width=6,height=.12,fill_color=GOLD,fill_opacity=1,stroke_width=0).move_to([0,y,0])
    scene.add(lab,bar)
    scene.play(bar.animate.stretch(.01,0,about_edge=LEFT),run_time=5,rate_func=linear)


def assay_large(medium,ratio=None):
    color=RED if medium=="NGF" else BLUE
    d=dish().scale(1.48,about_point=ORIGIN).shift(LEFT*1.3)
    d[0].stretch_to_fit_height(5.9).stretch_to_fit_width(9.25)
    d[4].become(T("ventral cord",28,YELLOW).move_to([1.5,1.6,0]))
    # Transform rays in the same coordinate system as the enlarged explant.
    h=halo(0,ratio or 1,color).scale(1.48,about_point=ORIGIN).shift(LEFT*1.3)
    tags=VGroup(T(medium,36,color).move_to([-1.3,3.4,0]),
       T("far",28).move_to([-4.6,-2.65,0]),
       T("near (faces cord)",28).move_to([0,-2.65,0]),
       Line([-5.3,-2.3,0],[-3.9,-2.3,0],color=TEXT),
       Line([-1.3,-2.3,0],[1.3,-2.3,0],color=TEXT))
    ruler=VGroup(Line([-.1,2.1,0],[1.75,2.1,0],color=TEXT,stroke_width=5),
        T("600 micrometres",26).move_to([.8,2.6,0]))
    return VGroup(d,tags,ruler),h


def assay_stats(near,ratio,color):
    return VGroup(T("Mean axon length",26).move_to([4.95,2.3,0]),
       T("micrometres\n(made up)",26).move_to([4.8,1.5,0]),
       T(f"near  {near}",30,color).move_to([4.8,.55,0]),
       T("far    600",30,color).move_to([4.8,-.05,0]),
       T("near / far",28).move_to([4.8,-.7,0]),
       M(str(ratio),48,color).move_to([4.8,-1.4,0]))


def halo_ring(ratio,color):
    pts=[]
    c=np.array([-2.41,0,0])
    for a in np.linspace(0,2*np.pi,90):
        length=1.25*(1-(1-ratio)*(1+np.cos(a))/2)
        pts.append(c+1.48*(.42+length+.08)*np.array([np.cos(a),np.sin(a),0]))
    ring=VMobject(color=color,stroke_width=2).set_points_as_corners(pts)
    lab=T("halo",30,color).move_to([-2.4,-3.35,0])
    leader=Line(lab.get_top(),min(pts,key=lambda v:v[1]),color=color)
    return VGroup(ring,lab,leader)


def neuron_rows(second=False,answer="?"):
    title=header("Neurons • other work")
    intact=T("Other receptor parts intact",28,GREY).move_to([0,2.5,0])
    box=rr(11.7,2.0,BLUE,.07).move_to([0,1.0,0])
    row=VGroup(T("Neuropilin: no inner tail",30,BLUE).move_to([-.6,1.45,0]),
        T("binds: yes",28).move_to([3.6,1.45,0]),
        T("growth cones still collapse",32,GREEN).move_to([1,.55,0]),
        fan(-.4,.4,1.5,(-5,.85,0)))
    g=VGroup(title,intact,box,row)
    if second:
        box2=rr(11.7,2.15,PURPLE,.07).move_to([0,-1.35,0])
        row2=VGroup(T("Extra plexin: tail cut",30,PURPLE).move_to([-.7,-.75,0]),
             T("Own normal plexin present",28,TEXT).move_to([-.7,-1.4,0]),
             T("binding: expected",28,TEXT).move_to([-.7,-2.05,0]))
        stub=receptor("plexin",-4.8,cut=True,ym=-2.05).scale(.7,about_point=[-4.8,-2.05,0])
        stub[1].scale(1/.7)
        row2.add(stub)
        ans=T(answer,60 if answer=="?" else 30,RED if answer!="?" else TEXT).move_to([3.3,-1.55,0])
        g.add(box2,row2,ans)
    return g


def mechanism(joined=True):
    stage,n,p,cue=receptor_stage(cutp=True)
    # Keep a visible gap between the extra plexin and neuropilin cup.
    if joined:p.shift(RIGHT*.08)
    own=receptor("plexin",4.6,ym=-.2).scale(1.2,about_point=[4.6,-.2,0]).set_opacity(.28)
    extra=T("extra plexin,\ninner part cut off",28,PURPLE).move_to([1.18,-1.5,0])
    normal=T("the cell's\nown plexin",28,PURPLE).move_to([4.6,-3,0])
    wire=Line([1.18,-.5,0],[1.18,-.95,0],color=GREY,stroke_width=6)
    no=T("no signal",30,GREY).move_to([1.18,-2.65,0])
    return VGroup(stage,own,extra,normal,wire,no),p


def comparison():
    g=VGroup(header("Same tissue, two answers"))
    for x,ratio,col,med in [(-3.15,.25,RED,"NGF"),(3.15,.9,BLUE,"NT-3")]:
        g.add(dish(x,medium=med),halo(x,ratio,col),
            T(f"near / far = {ratio}",34,col).move_to([x,-2.8,0]))
    return g


class S00Title(TitleCard):
    LESSON="Semaphorins and Repulsion"
    TITLE="One Tissue, Two Axons, One Receptor"

    def construct(self):
        brand=T("BIOCHEMISTRYPEDIA",22,TEAL)
        lesson=T(self.LESSON.upper(),22,GREY)
        title=T("One Tissue, Two Axons,\nOne Receptor",48,font=TITLE_FONT)
        rule=Line(LEFT*1.2,RIGHT*1.2,color=GOLD,stroke_width=4)
        group=VGroup(brand,lesson,title,rule).arrange(DOWN,buff=.35)
        self.play(FadeIn(group),run_time=.6)
        self.finish()


class S01Question(SpokenScene):
    def construct(self):
        outline=Ellipse(width=5.8,height=6.1,color=GREY,fill_color=GREY,fill_opacity=.08)
        region=Ellipse(width=4.6,height=2.5,color=YELLOW,fill_color=YELLOW,fill_opacity=.13).move_to([0,-1.2,0])
        self.add(outline,T("dorsal",28).move_to([0,3.35,0]),T("ventral",28).move_to([0,-3.35,0]))
        self.at("is made")
        self.play(FadeIn(region),run_time=.4)
        self.at("ventral cord")
        self.play(FadeIn(T("Sema3A",30,YELLOW).move_to([0,-1.5,0])),run_time=.4)
        pain=VMobject(color=RED,stroke_width=10).set_points_as_corners([[-6,1,0],[-2.6,1,0],[-1.4,.35,0]])
        muscle=VMobject(color=BLUE,stroke_width=10).set_points_as_corners([[6,1,0],[2.6,1,0],[.65,-.8,0]])
        self.at("Pain fibers")
        self.play(Create(pain),FadeIn(T("pain fibres",30,RED).move_to([-4.4,1.7,0])),run_time=.45)
        self.play(Create(Line([-1.65,.05,0],[-1.15,.65,0],color=RED,stroke_width=7)),run_time=.2)
        self.at("muscle afferents")
        self.play(Create(muscle),FadeIn(T("muscle afferents",28,BLUE).move_to([4.3,1.7,0])),run_time=.55)
        self.at("Is the difference")
        self.play(FadeIn(T("Cue or axon?",40).move_to([0,2.1,0])),run_time=.4)
        self.finish()

class S02Setup(SpokenScene):
    def construct(self):
        d=dish().scale(1.5,about_point=ORIGIN)
        self.at("Here is the test")
        self.play(FadeIn(d[0]),run_time=.5)
        self.at("a dorsal root")
        self.play(FadeIn(d[1]),run_time=.45)
        self.play(FadeIn(d[3]),FadeIn(T("dorsal root ganglion",28,TEAL).move_to([0,-3.35,0])),run_time=.3)
        self.at("collagen gel")
        self.play(FadeIn(header("Collagen gel",GREY)),run_time=.4)
        self.at("beside a piece")
        self.play(FadeIn(d[2]),run_time=.5)
        self.at("ventral cord")
        self.play(FadeIn(d[4]),run_time=.4)
        self.finish()


class S03Media(SpokenScene):
    def construct(self):
        d=dish().scale(1.5,about_point=ORIGIN); pair=assays()
        self.add(d,header("Collagen gel",GREY))
        self.at("nerve growth factor")
        self.play(d.animate.scale(2/3,about_point=ORIGIN).shift(LEFT*3.15),FadeIn(pair[0][-1]),run_time=.75)
        self.at("and once")
        self.play(FadeIn(pair[1]),run_time=.75)
        self.at("The medium")
        self.play(FadeIn(T("Medium largely decides which neurons grow",28).move_to([0,-3.35,0])),run_time=.5)
        self.finish()


class S04Q(SpokenScene):
    def construct(self):
        self.add(assays())
        self.at("Where will the axons")
        self.play(FadeIn(assay_question()),run_time=.5)
        self.finish()


class S05Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(assays(),assay_question().shift(UP*.5))
        for x in [-3.15,3.15]:
            self.add(DoubleArrow([x-2,.8,0],[x+.6,.8,0],color=TEXT),
                T("far    ?    near",28).move_to([x,1.4,0]))
        pause_cue(self)

class S06RevealNgf(SpokenScene):
    def construct(self):
        d,h=assay_large("NGF",.25);self.add(d)
        far=VGroup(*[m for i,m in enumerate(h) if np.cos(i*2*np.pi/28)<0])
        near=VGroup(*[m for i,m in enumerate(h) if np.cos(i*2*np.pi/28)>=0])
        self.at("the pain fibers")
        self.play(Create(far),run_time=.7)
        self.at("They grow poorly")
        self.play(Create(near),run_time=.7)
        self.at("The ring of axons")
        self.play(FadeIn(halo_ring(.25,RED)),FadeIn(assay_stats(150,.25,RED)),run_time=.5)
        self.at("is lopsided")
        self.play(Indicate(h),run_time=.4)
        self.finish()

class S07RevealNt3(SpokenScene):
    def construct(self):
        d,h=assay_large("NT-3",.9);self.add(d)
        self.add(T("Comparison: NGF\nnear / far = 0.25",26,RED).move_to([4.98,-2.85,0]))
        self.at("the muscle afferents")
        self.play(Create(h),run_time=.7)
        self.at("Their halo")
        self.play(FadeIn(halo_ring(.9,BLUE)),FadeIn(assay_stats(540,.9,BLUE)),run_time=.5)
        self.finish()

class S08Beat(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(comparison());self.wait(2)

class S09Same(SpokenScene):
    def construct(self):
        self.add(T("Same two halos • two sources",36).move_to([0,3.15,0]),
            T("ventral cord",28,YELLOW).move_to([-3.4,2.65,0]),
            T("NGF",30,RED).move_to([0,1.1,0]),
            T("NT-3",30,BLUE).move_to([0,-1.6,0]))
        def mini(x,y,ratio,col,cells=False):
            d=dish(cells=cells)
            d.remove(d[3],d[4])
            h=halo(0,ratio,col)
            pair=VGroup(d,h).scale(.72,about_point=ORIGIN).shift([x,y,0])
            d[0].stretch_to_fit_height(2.5)
            return d,h
        for y,ratio,col in [(1.1,.25,RED),(-1.6,.9,BLUE)]:
            d,h=mini(-3.4,y,ratio,col);self.add(d,h)
        self.at("Messersmith")
        self.play(FadeIn(T("Messersmith and colleagues • 1995 • rat explants",32,TEXT).move_to([0,-3.35,0])),run_time=.3)
        self.at("Cells secreting")
        ds=VGroup();hs=VGroup()
        for y,ratio,col in [(1.1,.25,RED),(-1.6,.9,BLUE)]:
            d,h=mini(3.4,y,ratio,col,True);ds.add(d);hs.add(h)
        self.play(FadeIn(ds),FadeIn(T("Sema3A cells",28,YELLOW).move_to([3.4,2.65,0])),run_time=.35)
        self.at("did the same")
        self.play(Create(hs),run_time=.6)
        self.wait(3.2)
        self.finish()

class S10Neuropilin(SpokenScene):
    def construct(self):
        gc=growth((-2,0,0),2.6);self.add(gc)
        self.at("a growth cone")
        self.play(FadeIn(header("How does a growth cone hear Sema3A?")),run_time=.5)
        stage,n,p,s=receptor_stage(False)
        stage.remove(s)
        n[1].set_opacity(0)
        self.at("Two groups found")
        self.play(FadeOut(gc),FadeIn(stage),run_time=.7)
        self.play(FadeIn(s.copy().move_to([3.8,2.2,0])),run_time=.4)
        loose=self.mobjects[-1]
        self.at("It was neuropilin")
        self.play(loose.animate.move_to(s),n[1].animate.set_opacity(1),run_time=.7)
        self.play(FadeIn(T("neuropilin • 1997 • two groups",26,BLUE).move_to([0,-2.9,0])),run_time=.4)
        self.finish()


class S11Tail(SpokenScene):
    def construct(self):
        stage,n,p,s=receptor_stage(False);self.add(stage)
        self.at("tightly")
        self.play(Indicate(s,scale_factor=1.08),run_time=.4)
        self.at("its tail inside")
        pointer=Arrow([.5,-1.2,0],n[3].get_right(),buff=.15,color=BLUE)
        self.play(GrowArrow(pointer),FadeIn(T("short inner tail\nabout 40 amino acids",30,BLUE).move_to([2.9,-1.25,0])),run_time=.45)
        self.at("with nothing like")
        self.play(FadeIn(T("no enzyme-like part",30).move_to([2.9,-2.35,0])),run_time=.4)
        self.at("Where is the wire")
        self.play(FadeIn(T("Where is the wire?",38).move_to([0,-3.25,0])),run_time=.4)
        self.finish()

class S12Plexin(SpokenScene):
    def construct(self):
        stage,n,p,s=receptor_stage(False);self.add(stage)
        self.at("pointed to the")
        self.play(FadeIn(p[:3]),FadeIn(T("plexins • 1999",30,PURPLE).move_to([3.8,2.8,0])),run_time=.5)
        self.at("a large part")
        self.play(GrowFromEdge(p[3],UP),FadeIn(T("about 40 amino acids",26,BLUE).move_to([-1.7,-1.05,0])),run_time=.5)
        self.at("inside the cell")
        self.play(FadeIn(T("large inner\ndomain",30,PURPLE).move_to([3.8,-1.9,0])),run_time=.4)
        self.finish()

class S13Table(SpokenScene):
    def construct(self):
        self.add(header("Engineered cells + Sema3A"))
        cols=[-4,.0,3.55]
        self.add(*[T(t,30).move_to([x,2.25,0]) for t,x in zip(["Cells carry","Binds?","Responds?"],cols)])
        vals=[("Neither","no","no"),("Neuropilin-1 alone","yes","no"),("Plexin-A1 alone","little or none","no"),("Both","yes, tighter","yes, cells round up")]
        rows=[]
        for y,v in zip([1.15,-.05,-1.25,-2.45],vals):
            icon=Ellipse(width=.85,height=.35,color=TEAL,fill_color=TEAL,fill_opacity=.3).move_to([5.75,y,0])
            row=VGroup(*[T(t,28,GREEN if j==2 and v[0]=="Both" else TEXT).move_to([x,y,0]) for j,(t,x) in enumerate(zip(v,cols))],icon)
            rows.append(row)
        self.add(rows[0])
        self.at("neuropilin alone")
        self.play(FadeIn(rows[1][:2]),run_time=.35)
        self.at("does not respond")
        self.play(FadeIn(rows[1][2:]),FadeIn(rows[2]),run_time=.4)
        self.at("With plexin as well")
        self.play(FadeIn(rows[3][0]),run_time=.35)
        self.at("binding is tighter")
        self.play(FadeIn(rows[3][1]),run_time=.35)
        self.at("Now the cells")
        self.add(rows[3][3])
        self.play(FadeIn(rows[3][2]),Transform(rows[3][3],Circle(radius=.38,color=TEAL,fill_color=TEAL,fill_opacity=.5).move_to([5.75,-2.45,0])),run_time=.7)
        self.wait(3)
        self.finish()

class S14Tailless(SpokenScene):
    def construct(self):
        self.add(header("Neurons • separate experiment"))
        n=receptor("neuropilin",-4.5,cut=True,ym=.2).scale(.9,about_point=[-4.5,.2,0])
        p=receptor("plexin",-2.2,ym=.2).scale(.9,about_point=[-2.2,.2,0]).set_opacity(.3)
        n[1].scale(1/.9);p[1].scale(1/.9)
        cue=semag(-4.5,2.05,1.65,.6)
        self.add(mem_bar(.2,-5.9,-.9),n,p,cue,
            T("neuropilin: tail removed",28,BLUE).move_to([-3.5,-2.1,0]),
            T("other receptor parts intact",26).move_to([-3.4,-2.7,0]))
        gc=growth((.6,-.1,0),2.8);self.add(gc)
        self.add(T("growth cone",30,TEAL).move_to([3,-2.65,0]))
        self.at("which keep their")
        self.play(Indicate(p),run_time=.5)
        self.at("with no inner tail")
        self.play(Indicate(n[2]),run_time=.5)
        self.at("still let growth")
        self.play(Transform(gc[1],fan(-.4,.4,2.3,(.6,-.1,0))),FadeOut(gc[2]),run_time=.8)
        self.play(FadeIn(T("still collapses",34,GREEN).move_to([3,-1.65,0])),run_time=.35)
        self.wait(3)
        self.finish()

class S15Q(SpokenScene):
    def construct(self):
        first=neuron_rows();full=neuron_rows(True)
        self.add(first)
        self.at("sensory neurons")
        self.play(FadeIn(full[4]),run_time=.4)
        self.at("with its inner part")
        self.play(FadeIn(full[5][0]),run_time=.5)
        self.at("They still have")
        self.play(FadeIn(full[5][1:]),run_time=.5)
        self.at("What happens")
        self.play(FadeIn(full[6]),FadeIn(T("What happens?",30).move_to([0,-3.05,0])),run_time=.5)
        self.finish()


class S16Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(neuron_rows(True))
        pause_cue(self)

class S17Reveal(SpokenScene):
    def construct(self):
        rows=neuron_rows(True);self.add(rows)
        self.at("is blocked")
        self.play(Transform(rows[6],T("response\nblocked",32,RED).move_to([3.7,-1.4,0])),run_time=.5)
        self.at("The broken plexin")
        self.play(Indicate(rows[5][0],color=PURPLE),run_time=.5)
        stage,p=mechanism(False)
        stage[-1].set_opacity(0)
        self.at("One likely idea")
        self.play(FadeOut(rows),FadeIn(stage),FadeIn(header("Possible mechanism",YELLOW)),run_time=.45)
        self.at("It joins neuropilin")
        self.play(p.animate.shift(RIGHT*.08),run_time=.55)
        self.at("that cannot signal")
        self.play(stage[-1].animate.set_opacity(1),run_time=.4)
        self.finish()

class S18Dn(SpokenScene):
    def construct(self):
        stage,p=mechanism();heading=header("Possible mechanism",YELLOW);self.add(stage,heading)
        self.at("this way")
        dn=T("Dominant negative",34,RED).move_to([0,3.2,0])
        self.play(Transform(heading,dn),run_time=.35)
        self.wait(2.1)
        self.at("So")
        normal,n,p,cue=receptor_stage()
        self.play(FadeOut(stage),FadeIn(normal),Transform(heading,header("The receptor pair")),run_time=.3)
        self.at("neuropilin catches")
        self.play(FadeIn(T("catches",34,BLUE).move_to([-1.7,-3.15,0])),run_time=.3)
        self.at("plexin signals")
        self.play(Indicate(p[3]),FadeIn(T("signals",34,PURPLE).move_to([1.1,-3.15,0])),run_time=.4)
        self.wait(3)
        self.finish()

class S19Inside(SpokenScene):
    def construct(self):
        cone=rr(12.6,6.4,TEAL,.06,r=1.0).move_to([0,.25,0])
        shaft=Line([-6.7,.25,0],[-6.3,.25,0],color=TEAL,stroke_width=18)
        self.add(shaft)
        self.add(cone,T("inside the growth cone",28,TEAL).move_to([-3,2.6,0]))
        plex=chip("plexin inner domain",PURPLE,30).move_to([0,2,0]);self.add(plex)
        # Membrane-embedded receptor cartoon connects the inner domain to the rim.
        self.add(rr(1.4,.5,PURPLE).move_to([0,3.25,0]),Line([0,3,0],[0,2.4,0],color=PURPLE,stroke_width=10))
        switch=chip("Ras-family GTPase",ORANGE,28).move_to([-3,.9,0])
        off=T("OFF",30,RED).move_to([-3,.05,0])
        self.at("switches off")
        self.play(FadeIn(switch),GrowArrow(Arrow(plex.get_left(),switch.get_top(),buff=.12,color=PURPLE)),FadeIn(off),run_time=.55)
        substrate=Line([-5.4,-2.25,0],[-.8,-2.25,0],color=GREY,stroke_width=6)
        feet=VGroup(*[VGroup(Line([x,-1.25,0],[x,-2.25,0],color=ORANGE,stroke_width=7),Line([x-.2,-2.25,0],[x+.2,-2.25,0],color=ORANGE,stroke_width=7)) for x in [-4.4,-3.1,-1.8]])
        self.at("integrins grip")
        self.play(FadeIn(substrate),FadeIn(feet),FadeIn(T("integrin grip",28,ORANGE).move_to([-3,-.45,0])),run_time=.4)
        self.play(feet.animate.shift(UP*.75),run_time=.65)
        effect=chip("other effectors",PURPLE,28).move_to([3,.9,0])
        self.at("Other plexin pathways")
        self.play(FadeIn(effect),GrowArrow(Arrow(plex.get_right(),effect.get_top(),buff=.12,color=PURPLE)),run_time=.45)
        mesh=VGroup(*[Line([1.3,y,0],[4.8,y+.7,0],color=TEAL,stroke_width=6) for y in [-1.65,-1.3,-.95]],*[Line([x,-1.8,0],[x+.5,-.5,0],color=TEAL,stroke_width=6) for x in [1.5,2.2,2.9,3.6]])
        rods=VGroup(*[Line([1.6,y,0],[4.6,y,0],color=BLUE,stroke_width=12) for y in [-1.95,-2.2]])
        self.at("actin and microtubules")
        self.play(Create(mesh),FadeIn(T("actin mesh",26,TEAL).move_to([3,-.25,0])),run_time=.35)
        self.at("and microtubules")
        self.play(Create(rods),FadeIn(T("microtubule rods",26,BLUE).move_to([3.65,-2.55,0])),run_time=.4)
        self.at("Together")
        self.play(mesh.animate.set_opacity(.45),rods.animate.stretch(.55,0).set_opacity(.8),run_time=.6)
        result=chip("Grip and actin lost",RED,30).move_to([0,-1.95,0])
        self.at("loses grip and actin")
        self.play(GrowArrow(Arrow([-1.8,-1.4,0],[-.65,-1.6,0],buff=.02,color=RED)),GrowArrow(Arrow([1.3,-1.7,0],[.65,-1.6,0],buff=.02,color=RED)),FadeIn(result),cone.animate.stretch(.86,0).stretch(.94,1),shaft.animate.put_start_and_end_on([-6.7,.25,0],[-5.418,.25,0]),run_time=.6)
        self.wait(3)
        self.finish()

class S20Layout(SpokenScene):
    def construct(self):
        left=growth((-5.1,.15,0),3.1);right=growth((1.1,.15,0),3.1)
        context=T("Typical outcomes • Sema3A-sensitive growth cones",28).move_to([0,-3.4,0])
        self.add(left,right,T("gradient from one side",30).move_to([-3.2,3,0]),T("strong dose all round",30).move_to([3.2,3,0]),context)
        # Deterministic graded density, with a direction arrow.
        gradient=VGroup(*[Dot([x,y,0],radius=.06,color=YELLOW) for j,x in enumerate([-2.4,-1.9,-1.4,-.9]) for y in np.linspace(.8,2.25,j+2)])
        arrow=Arrow([-.8,2.6,0],[-2.7,2.6,0],buff=.05,color=YELLOW)
        self.at("a gradient from")
        near_edge=Polygon([-3.1,1.9,0],[-2.55,1.1,0],[-2.9,.85,0],[-3.4,1.65,0],color=RED,fill_color=RED,fill_opacity=.35).scale(3.1/2.8,about_point=[-5.1,0,0]).shift(UP*.15)
        self.play(FadeIn(gradient),GrowArrow(arrow),FadeIn(near_edge),run_time=.4)
        self.at("turns it away")
        self.play(left.animate.rotate(-.45,about_point=[-5.1,.15,0]).shift(UP*.65),near_edge.animate.rotate(-.45,about_point=[-5.1,.15,0]).shift(UP*.65),FadeIn(T("near edge loosens → turn",28,TEAL).move_to([-3.2,-2.85,0])),run_time=.6)
        around=VGroup(*[Dot([3.1+2.25*np.cos(a),2.25*np.sin(a),0],radius=.07,color=YELLOW) for a in np.linspace(-np.pi,np.pi,26,endpoint=False) if 2.25*np.sin(a)>-.55])
        self.at("a strong dose")
        self.play(FadeIn(around),right[1].animate.set_stroke(RED).set_fill(RED,opacity=.15),run_time=.45)
        self.at("can fold the fan")
        self.play(Transform(right[1],fan(-.3,.3,2.0,(1.1,.15,0))),FadeOut(right[2]),FadeIn(T("whole rim loosens",28,RED).move_to([3.1,-1.55,0])),run_time=.6)
        self.at("preparations that support")
        self.play(FadeIn(T("possible collapse",30,TEAL).move_to([3.1,-2.85,0])),Transform(context,T("Dose, exposure and cell state matter too",28).move_to([0,-3.4,0])),run_time=.4)
        self.wait(3)
        self.finish()

class S21Takeaway(SpokenScene):
    def construct(self):
        stage,n,p,cue=receptor_stage();stage.shift(UP*.4);self.add(stage,header("The working receptor for Sema3A"))
        self.at("and plexin")
        self.play(p.animate.shift(LEFT*.37),run_time=.55)
        self.at("No pair")
        self.play(FadeIn(T("No pair, no answer\nin these experiments.",36).move_to([0,-3.15,0])),run_time=.4)
        self.wait(3)
        self.finish()

class S22End(EndCard):
    LINE="For Sema3A, no neuropilin-plexin pair, no answer."

    def construct(self):
        self.add(T("For Sema3A,",40,font=TITLE_FONT).move_to([0,1,0]),T("no neuropilin-plexin pair,\nno answer.",44,font=TITLE_FONT).move_to([0,-.3,0]),T("biochemistrypedia.com",26,TEAL).move_to([0,-2.2,0]))
        self.finish()