"""One Rise, One Fall — one cell and its schematic record.
COLOR MAP: BLUE CDK; ORANGE cyclin; GREEN active pairs/activity/rise;
RED destruction/APC/damage/fall; PURPLE Wee1/Cdc25; GOLD inhibitory phosphate;
TEAL DNA/origins/licences; PINK securin; GREY cell/nucleus/chromosomes/cohesin.
All protein drawings are abstract functional symbols, never molecular structures.
"""
from bp_style import *

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
PINK = "#E58FB5"
C = np.array([-3.25, -0.2, 0.])
X0, X1, Y0, Y1 = 0.6, 6.1, -1.8, 1.7


def label(s, p, color=TEXT, size=30, width=12.5):
    return fit(T(s, size=size, color=color), max_w=width).move_to(p)


def chip(text, color=BLUE, size=26, pad=.12):
    lab = T(text, size=size, color=color)
    box = RoundedRectangle(corner_radius=.12, width=lab.width+2*pad, height=lab.height+2*pad,
        stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=.18)
    back = box.copy().set_fill(BG, 1).set_stroke(width=0)
    g = VGroup(back, box, lab.move_to(box))
    g.set_z_index(6)
    return g


def tag(s, p, color, size=28):
    lab = label(s, p, color, size=size)
    back = Rectangle(width=lab.width+.16, height=lab.height+.14, stroke_width=0,
        fill_color=BG, fill_opacity=1).move_to(lab)
    g = VGroup(back, lab)
    g.set_z_index(5)
    return g


def protein(cyclin=True, active=False, badge=False, name=False):
    body = RoundedRectangle(width=1.05, height=.62, corner_radius=.17,
        stroke_color=GREEN if active else BLUE, stroke_width=5,
        fill_color=BLUE, fill_opacity=.24)
    notch = Line([-.25,.1,0],[.25,.1,0],color=BG,stroke_width=9)
    g = VGroup(body, notch)
    if name: g.add(T("CDK",28,BLUE).move_to(body))
    if cyclin:
        cap = RoundedRectangle(width=.75,height=.28,corner_radius=.1,
            color=ORANGE,fill_opacity=.9).move_to([0,.43,0])
        g.add(cap)
    if badge: g.add(phosphate().move_to([.48,.4,0]))
    return g


def phosphate():
    return VGroup(Circle(radius=.22,color=GOLD,fill_opacity=1), T("P",28,BG))


def cyclin():
    return RoundedRectangle(width=.7,height=.35,corner_radius=.12,
        color=ORANGE,fill_opacity=.85)


def tube():
    return RoundedRectangle(width=4.9,height=5.0,corner_radius=.9,
        color=GREY,stroke_width=4,fill_color=GREY,fill_opacity=.07).move_to(C)


def rod():
    return RoundedRectangle(width=5.1,height=3.8,corner_radius=1.65,
        color=GREY,stroke_width=4,fill_color=GREY,fill_opacity=.07).move_to(C)


def trace(points, color):
    m=VMobject(color=color,stroke_width=6)
    m.set_points_as_corners([[X0+(X1-X0)*x,Y0+(Y1-Y0)*y,0] for x,y in points])
    return m


ORANGE_CYCLE=[(0,.04),(.78,.92),(.88,.98),(.89,.04),(1,.14)]
GREEN_CYCLE=[(0,.02),(.67,.02),(.69,.9),(.88,.9),(.89,.02),(1,.02)]
LOW=[(0,.02),(.67,.02)]
RAMP=[(0,.04),(.67,.79)]


class World(SpokenScene):
    def world(self, phase="", cellname="", paired=False, badges=False, active=False,
              chart="normal", dna=False, shape="cell", question=""):
        self.clock=ValueTracker(0)
        self.clock.add_updater(lambda m,dt:m.increment_value(dt))
        self.add(self.clock)
        self.cell=Circle(radius=2.55,color=GREY,stroke_width=4,
            fill_color=GREY,fill_opacity=.055).move_to(C)
        if shape=="tube": self.cell=tube()
        if shape=="rod": self.cell=rod()
        base=self.cell.copy()
        self.cell.add_updater(lambda m: m.become(base.copy().scale(1+.018*np.sin(self.clock.get_value()*.85))))
        self.nuc=Circle(radius=1.15,color=GREY,stroke_width=3,fill_opacity=.04).move_to(C+UP*.35)
        self.cellname=label(cellname,[-3.25,2.64,0],width=6.1)
        self.phase=label(phase,[-6.2,2.08,0],GREEN)
        self.head=label(question,[0,3.35,0],size=37)
        self.axes=VGroup(Line([X0,Y0,0],[X1+.15,Y0,0],color=GREY),
                         Line([X0,Y0,0],[X0,Y1,0],color=GREY),
                         label("time →",[5.25,-2.2,0]),
                         label("schematic",[4.9,2.12,0],size=28))
        self.legend=VGroup(label("cyclin",[1.4,2.65,0],ORANGE),
                           label("CDK activity",[4.65,2.65,0],GREEN))
        self.o=trace(ORANGE_CYCLE,ORANGE)
        self.g=trace(GREEN_CYCLE,GREEN)
        if chart=="low": self.o=trace(RAMP,ORANGE); self.g=trace(LOW,GREEN)
        if chart=="orange":
            self.g.set_opacity(0); self.legend[1].set_opacity(0)
        if chart=="locked":
            self.o=trace([(0,.04),(.68,.95),(1,.95)],ORANGE)
            self.g=trace([(0,.02),(.5,.02),(.52,.9),(1,.9)],GREEN)
        self.pos=ValueTracker(.05)
        self.scrub=always_redraw(lambda:Line([X0+self.pos.get_value()*(X1-X0),Y0,0],
            [X0+self.pos.get_value()*(X1-X0),Y1,0],color=TEXT,stroke_width=2))
        self.add(self.cell,self.nuc,self.axes,self.legend,self.o,self.g,self.scrub,
                 self.cellname,self.phase,self.head)
        self.pairs=VGroup()
        positions=[[-4.55,-1.25,0],[-3.1,-1.4,0],[-1.75,-1.05,0]]
        if paired:
            for i,p in enumerate(positions):
                m=protein(active=active,badge=badges).move_to(p)
                origin=m.get_center().copy()
                m.add_updater(lambda m,i=i,origin=origin:m.move_to(origin+UP*.085*np.sin(self.clock.get_value()*.85+i*1.7)))
                self.pairs.add(m)
            self.add(self.pairs)
        self.note=VGroup()
        if dna: self.dna_setup()
        # A broad, faint rotating highlight makes the living boundary move visibly.
        self.halo=Arc(radius=2.55,start_angle=.3,angle=1.1,color=TEXT,stroke_width=7).move_arc_center_to(C)
        if shape=="cell":
            self.halo.add_updater(lambda m,dt:m.rotate(dt*.16,about_point=C))
            self.add(self.halo)

    def cue(self,phrase,*anims,d=.75):
        self.at(phrase)
        if anims: self.play(*anims,run_time=d)

    def heading(self,s,color=TEXT):
        new=label(s,[0,3.35,0],color,size=37)
        old=self.head;self.head=new
        if not old.has_points() and not old.submobjects: return FadeIn(new)
        return FadeTransform(old,new)

    def caption(self,s,color=TEXT):
        # Below the record, clear of axis and cell. Explicit line breaks keep size >=28.
        target=VGroup(*[label(t,[3.4,-2.7-i*.48,0],color,size=28,width=5.9)
                        for i,t in enumerate(s.split('\n'))])
        if len(self.note)==0:
            self.note=target; return FadeIn(self.note)
        old=self.note
        self.note=target
        return FadeTransform(old,target)

    def phase_to(self,s):
        new=label(s,[-6.2,2.08,0],GREEN)
        old=self.phase;self.phase=new
        if not old.has_points() and not old.submobjects: return FadeIn(new)
        return FadeTransform(old,new)

    def trace_to_scrubber(self,points):
        # A rising record is drawn only as the scrubber reaches each moment.
        def draw(m):
            u=self.pos.get_value(); pts=[]
            for a,b in zip(points,points[1:]):
                if a[0] <= u: pts.append(a)
                if a[0] <= u < b[0]:
                    f=(u-a[0])/(b[0]-a[0]);pts.append((u,a[1]+f*(b[1]-a[1])));break
            if u>=points[-1][0]:pts.append(points[-1])
            if len(pts)<2:pts=[points[0],(points[0][0]+.001,points[0][1])]
            m.become(trace(pts,ORANGE))
        self.o.add_updater(draw)

    def move_record(self,p,d=1):
        self.play(self.pos.animate.set_value(p),run_time=d,rate_func=linear)

    def set_pairs(self,active=False,badges=False):
        anim=[]
        for m in self.pairs:
            m.clear_updaters()
            anim.append(Transform(m,protein(active=active,badge=badges).move_to(m)))
        return anim

    def destroy(self,group):
        # Red fragments depart from the actual target, rather than a detached icon.
        fragments=VGroup()
        for m in group:
            for k in range(4):
                fragments.add(Square(side_length=.13,color=RED,fill_opacity=1).move_to(m.get_center()+[.12*k,0,0]))
        self.play(group.animate.set_color(RED),run_time=.22)
        self.play(FadeOut(group),FadeIn(fragments),run_time=.22)
        self.play(*[f.animate.shift([(.25 if i%2 else -.25),.4+(i%3)*.2,0]).set_opacity(0)
                    for i,f in enumerate(fragments)],run_time=.6)
        self.remove(fragments)

    def divide(self):
        self.cell.clear_updaters()
        two=VGroup(*[Ellipse(width=2.4,height=4.5,color=GREY,stroke_width=4,
            fill_color=GREY,fill_opacity=.055).move_to(C+[x,0,0]) for x in [-1.2,1.2]])
        self.play(Transform(self.cell,two),self.nuc.animate.scale(.65),run_time=.65)
        self.play(Transform(self.cell,Circle(radius=2.55,color=GREY,stroke_width=4,
            fill_color=GREY,fill_opacity=.055).move_to(C)),self.nuc.animate.scale(1/.65),run_time=.65)

    def dna_setup(self,licensed=False,copies=1):
        self.strand=VGroup(*[Line([-4.8,.1+j*.3,0],[-1.7,.1+j*.3,0],color=TEAL,stroke_width=5)
                            for j in range(copies)])
        self.origins=VGroup(*[Dot([-4.5+i*.82,.1,0],radius=.08,color=TEAL) for i in range(4)])
        self.rings=VGroup(*[Circle(radius=.2,color=TEAL,stroke_width=4).move_to(d) for d in self.origins])
        self.add(self.strand,self.origins)
        if licensed:self.add(self.rings)

    def license_bands(self):
        self.bands=VGroup(DashedLine([X0,Y0+.4,0],[X1,Y0+.4,0],color=TEAL),
            DashedLine([X0,Y0+1.45,0],[X1,Y0+1.45,0],color=TEAL),
            tag("license",[5.25,Y0+.4,0],TEAL),
            tag("fire",[5.5,Y0+1.45,0],TEAL))
        self.add(self.bands)

    def fire(self):
        bubbles=VGroup(*[Ellipse(width=.4,height=.38,color=TEAL,fill_opacity=.15).move_to(d) for d in self.origins])
        self.play(ReplacementTransform(self.rings,bubbles),run_time=.6)
        self.play(*[b.animate.stretch(2.1,0) for b in bubbles],run_time=1.3)
        new=Line([-4.8,.45,0],[-1.7,.45,0],color=TEAL,stroke_width=5)
        self.play(FadeOut(bubbles),Create(new),run_time=.6)
        self.strand.add(new)

    def chromosomes(self):
        self.chrom=VGroup()
        for x in [-3.9,-2.6]:
            a=Line([x-.2,.9,0],[x+.2,-.2,0],color=GREY,stroke_width=9)
            b=Line([x+.2,.9,0],[x-.2,-.2,0],color=GREY,stroke_width=9)
            self.chrom.add(VGroup(a,b))
        return self.chrom


class S00Hook(World):
    def construct(self):
        self.world(cellname="sea-urchin egg",chart="orange")
        self.remove(self.legend[1])
        self.pos.set_value(0)
        self.trace_to_scrubber([(0,.04),(.23,.95),(.24,.04),(.47,.95),(.48,.04)])
        supply=VGroup(*[cyclin().move_to([-4.5+i*1.15,-1.2,0]) for i in range(3)])
        self.add(supply)
        self.cue("every time",self.heading("Why destroy it every time?"),self.pos.animate.set_value(.23),d=1.0)
        self.at("it destroys")
        self.destroy(supply); self.divide(); self.move_record(.24,.4)
        self.cue("then it builds",FadeIn(supply.set_color(ORANGE)),self.pos.animate.set_value(.47),d=1.4)
        self.at("why would a cell")
        self.destroy(supply); self.divide(); self.move_record(.48,.4)
        self.finish()


class S01Title(TitleCard,World):
    TITLE="One Rise, One Fall"
    LESSON="Cyclin-CDK Control of the Cell Cycle"
    def construct(self):
        self.world(cellname="sea-urchin egg",chart="orange",question=self.TITLE)
        self.pos.set_value(.48)
        self.trace_to_scrubber([(0,.04),(.23,.95),(.24,.04),(.47,.95),(.48,.04),(.72,.95)])
        cap=cyclin().move_to([-3.25,-1.2,0]);self.add(cap)
        self.play(self.pos.animate.set_value(.56),run_time=2,rate_func=linear)


class S02Record(World):
    def construct(self):
        self.world(cellname="sea-urchin egg",chart="orange")
        self.legend[1].set_opacity(0)
        self.pos.set_value(.59)
        self.trace_to_scrubber([(0,.04),(.28,.95),(.29,.04),(.58,.95),(.59,.04),(.88,.95),(.89,.04)])
        supply=VGroup(*[cyclin().move_to([-4.5+i*1.15,-1.3,0]) for i in range(3)])
        self.add(supply)
        self.cue("at woods hole",self.caption("Hunt and colleagues\n1982 to 1983"))
        self.cue("the protein climbed",self.pos.animate.set_value(.88),d=3)
        self.cue("they named it cyclin",Indicate(self.legend[0],color=ORANGE),self.heading("Cyclin rises, then disappears"))
        source=Dot([-4.8,.3,0],radius=.14,color=GREY)
        self.cue("make it all",FadeIn(source))
        for m in supply:
            self.play(TransformFromCopy(source,m),run_time=.4)
        self.at("it is destroyed");self.destroy(supply);self.move_record(.89,.5);self.divide()
        self.finish()


class S03Engine(World):
    def construct(self):
        self.world(cellname="sea-urchin egg",chart="orange")
        self.pairs=VGroup(*[protein(cyclin=False,name=True).move_to([-4.6+i*1.4,-1.2,0]) for i in range(3)])
        self.add(self.pairs)
        self.cue("a kinase",self.heading("Cyclin + CDK"),self.caption("CDK alone: inactive",BLUE))
        cap=cyclin().move_to([-3.2,.7,0]);self.add(cap)
        self.cue("needed to switch it on",cap.animate.move_to(self.pairs[1].get_center()+UP*.43),d=.8)
        self.play(self.pairs[1][0].animate.set_stroke(GREEN,width=6),self.pos.animate.set_value(.6),run_time=.8)
        self.cue("from yeast to human",FadeTransform(self.cellname,label("any eukaryotic cell",[-3.25,2.64,0],width=6.1)))
        self.finish()


class S04Snap(World):
    def construct(self):
        self.world(paired=True,chart="low",phase="G1",cellname="frog embryo's first cycle")
        self.cue("the kinase's activity",self.caption("Two traces, different timing"),self.heading("Activity can snap"))
        self.cue("does not follow",Transform(self.o,trace(RAMP,ORANGE)),self.pos.animate.set_value(.3),self.phase_to("S"))
        self.cue("stays low",self.pos.animate.set_value(.67),self.phase_to("G2"),d=2)
        self.cue("snap up",Transform(self.g,trace(GREEN_CYCLE[:4],GREEN)),*self.set_pairs(active=True),self.pos.animate.set_value(.8),self.phase_to("M"),d=.7)
        self.cue("and crash",Transform(self.o,trace(ORANGE_CYCLE,ORANGE)),Transform(self.g,trace(GREEN_CYCLE,GREEN)),self.pos.animate.set_value(.95),*self.set_pairs(),d=.7)
        caps=VGroup(*[m[2] for m in self.pairs]);self.destroy(caps)
        self.finish()


class S05Puzzle(World):
    def construct(self):
        self.world(paired=True,chart="low",phase="G2",question="Why wait, then jump?")
        self.pos.set_value(.66)
        band=Rectangle(width=3.5,height=3.3,color=ORANGE,fill_opacity=.08,stroke_width=0).move_to([2.4,-.05,0]).set_z_index(-1)
        self.cue("cyclin climbs",FadeIn(band),self.caption("Cyclin rises\nActivity waits"))
        self.cue("so why",Indicate(self.g,color=GREEN))
        self.finish()


class S06Think(World):
    def construct(self):
        self.world(paired=True,chart="low",phase="G2",question="Why wait, then jump?")
        self.pos.set_value(.66)
        self.add(Rectangle(width=3.5,height=3.3,color=ORANGE,fill_opacity=.08,stroke_width=0).move_to([2.4,-.05,0]).set_z_index(-1))
        self.finish()


class S07Brake(World):
    def construct(self):
        self.world(paired=True,chart="low",phase="G2")
        self.wee=chip("Wee1",PURPLE).move_to([-3.25,1.65,0])
        self.cue("a pair can be built",self.heading("Built, but held off"))
        self.cue("the mitotic pair",self.caption("CDK1 + cyclin B"))
        self.cue("adds an inhibitory phosphate",FadeIn(self.wee),self.caption("Inhibitory phosphate",GOLD))
        for m in self.pairs:
            p=phosphate().move_to(m.get_center()+[.48,.4,0])
            self.play(self.wee.animate.move_to(m.get_center()+UP*1.1),TransformFromCopy(self.wee,p),run_time=.55)
            m.add(p)
        self.cue("inactive pairs pile up",self.pos.animate.set_value(.67),self.caption("Loaded and waiting",GOLD))
        self.finish()


class S08Release(World):
    def construct(self):
        self.world(paired=True,badges=True,chart="low",phase="G2")
        wee=chip("Wee1",PURPLE).move_to([-4.05,1.65,0])
        cdc=chip("Cdc25",PURPLE).move_to([-2.65,1.65,0]);self.add(wee)
        self.cue("a phosphatase",FadeIn(cdc),self.heading("Release becomes a cascade"))
        self.pairs[0].clear_updaters()
        self.cue("takes the phosphate off",self.pairs[0][-1].animate.shift(UP*.7).set_opacity(0),self.pairs[0][0].animate.set_stroke(GREEN,width=6))
        a=Arrow([-3.9,-.5,0],[-2.7,1.3,0],color=GREEN,buff=.1)
        b=VGroup(Line([-3.9,-.5,0],[-4.1,1.2,0],color=GREEN),Line([-4.35,1.2,0],[-3.85,1.2,0],color=GREEN))
        self.cue("it boosts",GrowArrow(a),Indicate(cdc,color=GREEN))
        self.cue("and slows",Create(b),wee.animate.set_opacity(.32))
        self.cue("each active pair",FadeOut(a),FadeOut(b))
        self.cue("it snaps",*self.set_pairs(active=True),Transform(self.g,trace(GREEN_CYCLE[:4],GREEN)),self.pos.animate.set_value(.8),self.phase_to("M"),d=.65)
        self.play(FadeOut(self.nuc),FadeIn(self.chromosomes()),run_time=.7)
        self.finish()


class S09Checkpoint(World):
    def construct(self):
        self.world(paired=True,active=True,phase="M")
        self.cue("checkpoints pull",self.phase_to("G2"),*self.set_pairs(badges=True),Transform(self.g,trace(LOW,GREEN)),Transform(self.o,trace(RAMP,ORANGE)),self.pos.animate.set_value(.65),self.heading("A checkpoint holds the brake"))
        self.dna_setup()
        damage=VGroup(Line([-3.4,-.05,0],[-3.15,.25,0],color=RED,stroke_width=6),Line([-3.4,.25,0],[-3.15,-.05,0],color=RED,stroke_width=6))
        cdc=chip("Cdc25",PURPLE).move_to([-2.65,1.65,0])
        sensor=label("sensor kinases",[-3.25,2.64,0],RED,size=28)
        bar=VGroup(Line([-2.65,2.35,0],[-2.65,2.05,0],color=RED,stroke_width=4),Line([-2.95,2.05,0],[-2.35,2.05,0],color=RED,stroke_width=4))
        self.cue("dna is damaged",FadeIn(damage),FadeIn(cdc))
        self.cue("sensor kinases",FadeIn(sensor),Create(bar),cdc[1].animate.set_color(GREY),cdc[2].animate.set_color(GREY))
        self.cue("the cell waits",self.caption("wait",GOLD))
        self.play(FadeOut(damage),FadeOut(sensor),FadeOut(bar),self.pos.animate.set_value(.69),run_time=.8)
        self.finish()


class S10Idea(World):
    def construct(self):
        self.world(paired=True,chart="low",phase="G1")
        self.cue("the one idea",self.heading("One rise. One fall."),self.caption("Rises and falls\nonce per cycle"))
        self.cue("the rise carries",self.pos.animate.set_value(.3),self.phase_to("S"))
        self.dna_setup()
        copied=self.strand.copy().shift(UP*.35)
        self.play(TransformFromCopy(self.strand,copied),run_time=1.0)
        self.play(self.pos.animate.set_value(.8),self.phase_to("M"),*self.set_pairs(active=True),Transform(self.g,trace(GREEN_CYCLE[:4],GREEN)),run_time=1)
        self.play(FadeOut(self.nuc),FadeOut(self.strand),FadeOut(self.origins),FadeOut(copied),FadeIn(self.chromosomes()),run_time=.6)
        self.cue("destroying cyclin",self.heading("Destruction brings the fall",RED),Transform(self.g,trace(GREEN_CYCLE,GREEN)),Transform(self.o,trace(ORANGE_CYCLE,ORANGE)),self.pos.animate.set_value(.95))
        self.destroy(VGroup(*[m[2] for m in self.pairs]))
        self.play(*[m[0].animate.set_stroke(BLUE) for m in self.pairs],run_time=.3)
        self.cue("copies the genome once",self.caption("Genome copies: 1",TEAL),FadeOut(self.chrom),FadeIn(self.nuc),FadeIn(self.strand),FadeIn(copied))
        self.finish()


class Spindle(World):
    def setup_spindle(self):
        self.world(paired=True,active=True,phase="M")
        self.pos.set_value(.82);self.remove(self.nuc)
        self.add(self.chromosomes())
        self.spindle=VGroup(*[Line([x,.35,0],[cx,.35,0],color=GREY,stroke_width=2)
            for x,cx in [(-5.2,-3.9),(-1.3,-2.6)]])
        self.coh=VGroup(*[Circle(radius=.22,color=GREY,stroke_width=4).move_to([x,.35,0]) for x in [-3.9,-2.6]])
        self.sec=chip("securin",PINK).move_to([-4.0,1.55,0])
        self.apc=chip("APC",RED).move_to([-2.5,1.55,0])
        self.tether=Line([-2.5,1.88,0],[-2.5,2.2,0],color=TEXT,stroke_width=3)
        self.add(self.spindle,self.coh,self.sec,self.apc,self.tether)


class S11SpindleHold(Spindle):
    def construct(self):
        self.setup_spindle();self.spindle[1].set_opacity(0)
        self.cue("now the fall",self.heading("Wait before anaphase"))
        self.cue("one enzyme",Indicate(self.apc,color=RED))
        self.cue("until every chromosome",Indicate(self.chrom[1],color=TEXT),self.caption("cohesin holds sisters"))
        self.cue("a checkpoint holds",Indicate(self.tether),self.caption("APC held back",RED))
        self.cue("the cell waits",self.spindle[1].animate.set_opacity(1),self.tether.animate.set_opacity(.4))
        self.finish()


class S12ApcTags(Spindle):
    def construct(self):
        self.setup_spindle()
        self.cue("checkpoint falls silent",FadeOut(self.tether),self.heading("APC tags two targets"))
        tags=VGroup(*[Square(side_length=.2,color=RED,fill_opacity=1).move_to(p)
                     for p in [self.sec.get_right(),self.pairs[1].get_center()+UP*.45]])
        self.cue("tags two proteins",TransformFromCopy(self.apc,tags[0]),TransformFromCopy(self.apc,tags[1]))
        self.at("securin goes");self.destroy(VGroup(self.sec,tags[0]))
        self.play(*[Transform(r,Arc(radius=.22,angle=PI,color=GREY).move_to(r)) for r in self.coh],
            *[ch[0].animate.shift(LEFT*.6) for ch in self.chrom],*[ch[1].animate.shift(RIGHT*.6) for ch in self.chrom],run_time=.8)
        self.at("cyclin b goes");self.destroy(VGroup(*[m[2] for m in self.pairs],tags[1]))
        self.play(*[m[0].animate.set_stroke(BLUE) for m in self.pairs],self.pos.animate.set_value(.96),Transform(self.g,trace(GREEN_CYCLE,GREEN)),run_time=.8)
        self.cue("the cell leaves",FadeOut(self.chrom),FadeOut(self.coh),FadeOut(self.spindle),FadeOut(self.apc),FadeIn(self.nuc),self.phase_to("G1"))
        self.divide();self.finish()


class S13OneWay(World):
    def construct(self):
        self.world()
        self.remove(self.nuc)
        divider=Line([-3.25,-2,0],[-3.25,1.6,0],color=GREY)
        pair=protein().move_to([-4.45,-.2,0]);cap=cyclin().move_to([-2,-.2,0])
        badge=phosphate().move_to(pair.get_center()+[.48,.4,0])
        self.add(divider,pair,cap)
        self.cue("switch the kinase off",self.heading("Pause, or rebuild?"))
        self.cue("a phosphate can be removed",FadeIn(badge),self.caption("Pause: reversible",GOLD))
        self.play(badge.animate.shift(UP*.8).set_opacity(0),pair[0].animate.set_stroke(GREEN),run_time=.65)
        self.play(badge.animate.shift(DOWN*.8).set_opacity(1),pair[0].animate.set_stroke(BLUE),run_time=.65)
        self.at("a destroyed protein");self.destroy(VGroup(cap))
        self.play(FadeIn(label("pause",[-4.45,-1.4,0],GOLD)),run_time=.4)
        fresh=cyclin().move_to([-2,-.2,0])
        self.cue("must be made again",GrowFromCenter(fresh),self.caption("Made again",ORANGE),d=1.6)
        self.cue("run one way",FadeOut(divider),self.pos.animate.set_value(.98),self.heading("Destruction makes a transition one way"),d=.8)
        self.finish()


class S14Predict(World):
    def construct(self):
        self.world(paired=True)
        self.cell.clear_updaters();self.halo.clear_updaters()
        self.cue("frog egg extracts",Transform(self.cell,tube()),FadeOut(self.halo),FadeTransform(self.cellname,label("frog egg extract",[-3.25,2.64,0],width=6.1)))
        self.cue("cycle in a tube",self.pos.animate.set_value(.95),d=1)
        lock=VGroup(RoundedRectangle(width=.5,height=.4,corner_radius=.07,color=ORANGE,fill_opacity=.3),Arc(radius=.18,start_angle=0,angle=PI,color=ORANGE).shift(UP*.2)).move_to([-3.2,.8,0])
        lock.add(cyclin().move_to(lock.get_center()+DOWN*.5))
        self.cue("cannot be destroyed",FadeIn(lock),self.caption("Cannot be destroyed",ORANGE))
        self.cue("what happens",self.heading("What happens?"))
        self.finish()


class S15Think(World):
    def construct(self):
        self.world(paired=True,shape="tube",cellname="frog egg extract",question="What happens?",chart="low")
        self.pos.set_value(.67)
        lock=VGroup(RoundedRectangle(width=.5,height=.4,corner_radius=.07,color=ORANGE,fill_opacity=.3),Arc(radius=.18,start_angle=0,angle=PI,color=ORANGE).shift(UP*.2)).move_to([-3.2,.8,0])
        lock.add(cyclin().move_to(lock.get_center()+DOWN*.5))
        self.add(lock)
        mask=Rectangle(width=1.8,height=3.55,fill_color=BG,fill_opacity=.93,stroke_width=0).move_to([5.25,-.05,0])
        self.add(mask);self.finish()


class S16Answer(World):
    def construct(self):
        self.world(paired=True,shape="tube",cellname="frog egg extract",chart="low",phase="G2")
        lock=VGroup(RoundedRectangle(width=.5,height=.4,corner_radius=.07,color=ORANGE,fill_opacity=.3),Arc(radius=.18,start_angle=0,angle=PI,color=ORANGE).shift(UP*.2)).move_to([-3.2,.8,0]);lock.add(cyclin().move_to(lock.get_center()+DOWN*.5))
        self.add(lock)
        self.cue("went into mitosis",*self.set_pairs(active=True),self.phase_to("M"),Transform(self.g,trace([(0,.02),(.5,.02),(.52,.9),(1,.9)],GREEN)),Transform(self.o,trace([(0,.04),(.68,.95),(1,.95)],ORANGE)),self.pos.animate.set_value(.7))
        apc=chip("APC",RED).move_to([-3.25,1.7,0])
        self.cue("the kinase stayed active",FadeIn(apc),self.heading("Activity stays high"))
        self.play(apc.animate.shift(LEFT*.3),run_time=.4);self.play(apc.animate.shift(RIGHT*.3),run_time=.4)
        self.cue("did not come out",self.pos.animate.set_value(.98),self.caption("Mitosis: no exit",RED))
        self.cue("making cyclin drives entry",self.caption("Making cyclin → entry",GREEN))
        down=DashedLine([5.7,1.3,0],[5.7,-1.6,0],color=RED,stroke_width=5)
        self.cue("destroying it permits exit",Create(down),self.caption("Destruction permits exit",RED))
        self.cell.clear_updaters()
        self.play(Transform(self.cell,Circle(radius=2.55,color=GREY,stroke_width=4).move_to(C)),FadeOut(apc),FadeOut(lock),run_time=.65)
        self.finish()


class S17License(World):
    def construct(self):
        self.world(phase="G1",dna=True,chart="low")
        self.license_bands()
        self.cue("controls copying",self.heading("Low: license. Rising: fire."))
        self.cue("an origin",Indicate(self.origins,color=TEAL),self.caption("Origins of replication",TEAL))
        self.cue("must be licensed",LaggedStart(*[Create(r) for r in self.rings],lag_ratio=.2),self.caption("Licensed",TEAL),d=1.3)
        self.cue("activity is low",self.pos.animate.set_value(.25),Indicate(self.bands[0],color=TEAL))
        self.cue("firing needs",self.phase_to("S"),Transform(self.g,trace([(0,.02),(.25,.02),(.65,.65)],GREEN)),self.pos.animate.set_value(.65),self.caption("Firing uses the licence",TEAL))
        self.fire();self.finish()


class S18Once(World):
    def construct(self):
        self.world(phase="S",dna=True)
        self.license_bands();self.strand.add(Line([-4.8,.45,0],[-1.7,.45,0],color=TEAL,stroke_width=5));self.add(self.strand)
        self.pos.set_value(.7)
        ring=self.rings[1].copy().shift(DOWN*.6)
        block=Line([-4.05,-.25,0],[-3.3,-.25,0],color=RED,stroke_width=7)
        self.cue("blocks new licenses",FadeIn(ring),Create(block),self.heading("At most once per cycle"),self.caption("No new licence",RED))
        self.cue("helps block",self.caption("Yeast: blocks\nAnimals: helps block",TEXT))
        self.cue("at most once",ring.animate.shift(DOWN*.3).set_opacity(0),self.caption("Copies this cycle: 1",TEAL),self.phase_to("G2"))
        self.cue("wait for the fall",self.pos.animate.set_value(.95),self.phase_to("M"))
        self.cue("normally at mitosis",FadeOut(block),Create(self.rings),self.phase_to("G1"),self.caption("New licences after the fall",TEAL))
        self.finish()


class S19Test(World):
    def construct(self):
        self.world(dna=True,chart="low",phase="S")
        self.o.set_opacity(0);self.legend[0].set_opacity(0)
        self.license_bands();self.cell.clear_updaters();self.halo.clear_updaters()
        self.cue("fission yeast",Transform(self.cell,rod()),FadeOut(self.halo),FadeTransform(self.cellname,label("fission yeast",[-3.25,2.64,0],width=6.1)),self.heading("Copy again, without division"))
        self.cue("without their mitotic cyclin",self.caption("No mitotic cyclin",ORANGE))
        self.cue("activity falls",Transform(self.g,trace([(0,.02),(.2,.6),(.35,.6),(.4,.02)],GREEN)),self.pos.animate.set_value(.4),d=.8)
        self.play(TransformFromCopy(self.strand,self.strand.copy().shift(UP*.3)),run_time=.5)
        self.cue("with no mitosis",self.caption("No mitosis",RED))
        self.cue("origins are licensed",Create(self.rings),self.caption("Copies: 2",TEAL))
        self.cue("copy their dna again",Transform(self.g,trace([(0,.02),(.2,.6),(.35,.6),(.4,.02),(.55,.02),(.7,.6),(.8,.6),(.85,.02),(1,.6)],GREEN)),self.pos.animate.set_value(.98),d=1.2)
        self.fire()
        self.play(self.nuc.animate.scale(1.17),self.caption("Copies: 3\nNo division",TEAL),run_time=.7)
        self.finish()


class S20Return(World):
    def construct(self):
        self.world(paired=True,chart="low",phase="G1")
        self.license_bands()
        self.cue("why destroy cyclin",self.heading("Why destroy it every time?"))
        self.cue("must climb once",*self.set_pairs(active=True),self.phase_to("M"),Transform(self.g,trace(GREEN_CYCLE[:4],GREEN)),self.pos.animate.set_value(.8),self.caption("One rise",GREEN))
        self.cue("and fall once",Transform(self.g,trace(GREEN_CYCLE,GREEN)),Transform(self.o,trace(ORANGE_CYCLE,ORANGE)),self.pos.animate.set_value(.96),self.caption("One fall",RED))
        self.cue("destruction is what normally",self.heading("Destruction normally makes the fall one way"),d=.7)
        caps=VGroup(*[m[2] for m in self.pairs]);self.destroy(caps)
        self.cue("leaves mitosis",*[Transform(m,protein(cyclin=False).move_to(m)) for m in self.pairs],self.phase_to("G1"))
        self.dna_setup()
        self.cue("resets its origins",Create(self.rings),self.caption("Origins reset",TEAL))
        self.cue("copies its genome once",self.heading("One rise. One fall. One copy."),self.caption("Copies this cycle: 1",TEAL),TransformFromCopy(self.strand,self.strand.copy().shift(UP*.35)))
        self.finish()


class S21End(EndCard):
    LINE="Make cyclin to enter mitosis; destroy it to reset, once per cycle."
