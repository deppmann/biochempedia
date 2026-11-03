"""Chapter 4. Tissue routes reuse the reference anatomical schematic, not data fits.
COLOR MAP (reference scenes.old.py): YELLOW netrin; BLUE growth cone/axon;
TEAL DCC; PURPLE UNC5; ORANGE cAMP (unused); PINK anti-DCC;
GREEN attraction; RED repulsion/block; GREY anatomy and outlines.
Qualitative outgrowth bars encode only low/high, with no invented measurements.
"""
import numpy as np
from bp_style import *
PURPLE = "#B58CD9"
PINK = "#E58BD0"
R = 1.0
DCC_A = [30,70,110]
UNC_A = [-30,-70,-110]
def smooth(points):
    m = VMobject()
    m.set_points_smoothly([np.array(p, float) for p in points])
    return m

def cups(center, angles, color, scale=1.0):
    out = VGroup()
    for deg in angles:
        phi = np.radians(deg)
        u = np.array([np.cos(phi), np.sin(phi), 0])
        c = center + (R * scale + 0.45 * scale) * u
        sw = 8 * max(scale, 0.6)
        out.add(Arc(radius=0.27 * scale, start_angle=phi + PI / 2, angle=PI, arc_center=c,
                    stroke_color=color, stroke_width=sw))
        out.add(Line(center + R * scale * u, center + (R + 0.18) * scale * u, color=color, stroke_width=sw * 0.8))
    return out

def caps(center, angles, scale=1.0):
    out = VGroup()
    for deg in angles:
        phi = np.radians(deg)
        u = np.array([np.cos(phi), np.sin(phi), 0])
        c = center + (R * scale + 0.45 * scale) * u
        out.add(Circle(radius=0.21 * scale, stroke_color=PINK, stroke_width=3, fill_color=PINK,
                       fill_opacity=0.95).move_to(c))
    return out

def body(center, scale=1.0):
    bg = Circle(radius=R * scale, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(center)
    disc = Circle(radius=R * scale, stroke_color=BLUE, stroke_width=5, fill_color=BLUE, fill_opacity=0.25)
    disc.move_to(center)
    fil = VGroup()
    for deg in [0, 150, 180, 210]:
        phi = np.radians(deg)
        u = np.array([np.cos(phi), np.sin(phi), 0])
        fil.add(Line(center + R * scale * u, center + (R + 0.3) * scale * u, color=BLUE, stroke_width=4))
    return VGroup(bg, disc, fil)

def run(self, mobs, path, t, rate=linear):
    """move a list of mobjects along a path while drawing the axon trail."""
    full = smooth(path).set_stroke(BLUE, 11).set_fill(opacity=0).set_z_index(-1)
    trail = full.copy()
    trail.pointwise_become_partial(full, 0, 0.001)
    self.add(trail)
    g = VGroup(*mobs)
    last = [np.array(path[0], float)]

    def step(m, a):
        a = max(a, 0.001)
        p = full.point_from_proportion(a)
        m.shift(p - last[0])
        last[0] = p
        trail.pointwise_become_partial(full, 0, a)

    self.play(UpdateFromAlphaFunc(g, step, rate_func=rate), run_time=t)
    return trail

def cord(center, scale=1.0, wrong=False, progenitor=True, floor=True):
    c = np.array(center, float)
    def pt(x, y):
        return c + np.array([x, y, 0]) * scale
    outline = Ellipse(width=4.6*scale, height=4.5*scale, color=GREY, stroke_width=3).move_to(c)
    mid = DashedLine(pt(0, 2.15), pt(0, -2.15), color=GREY, stroke_width=2)
    canal = Ellipse(width=.55*scale, height=1.5*scale, color=GREY, stroke_width=3).move_to(pt(0, .55))
    fp = RoundedRectangle(width=.65*scale, height=.28*scale, corner_radius=.06,
                          color=GREY, fill_color=GREY, fill_opacity=.3).move_to(pt(0, -2.05))
    progenitors = VGroup(*[Dot(pt(x, y), radius=.10*scale, color=GREY)
                           for x in [-.48, .48] for y in [.2, .65, 1.1]])
    deposits = VGroup(*[Dot(pt(x,y), radius=.075*scale, color=YELLOW)
                        for x,y in [(-2.02,.8),(-2.12,.25),(-2.0,-.4),(-1.7,-1.05),(-1.2,-1.62),(-.65,-1.9)]])
    fcue = VGroup(*[Dot(pt(x,-1.96), radius=.07*scale, color=YELLOW) for x in [-.2,0,.2]])
    points = [(-1.55,1.4),(-1.9,.55),(-1.7,-.65),(-.85,-1.8),(0,-2.05)]
    if wrong:
        points = [(-1.55,1.4),(-1.65,.6),(-.7,.1),(-.95,.8),(-.25,1.35)]
    route = smooth([pt(x,y) for x,y in points]).set_stroke(BLUE, 6)
    tip = body(pt(*points[-1]), .15*scale)
    soma = Dot(pt(-1.55,1.4), radius=.17*scale, color=BLUE)
    anatomy = VGroup(outline, mid, canal, fp, progenitors, soma)
    cues = VGroup()
    if progenitor:
        cues.add(deposits)
    if floor:
        cues.add(fcue)
    return VGroup(anatomy, cues, route, tip)

def explant(pos, color=BLUE):
    return RoundedRectangle(width=.8, height=.9, corner_radius=.2, color=color,
                            fill_color=color, fill_opacity=.25).move_to(pos)

def dish(cx):
    return RoundedRectangle(width=5.8, height=3.6, corner_radius=.3, color=GREY,
                            fill_color=GREY, fill_opacity=.04).move_to([cx,0,0])


def lab(text, x=0, y=3.15, color=TEXT, size=28):
    return T(text, size=size, color=color).move_to([x,y,0])


def cone(x, y=0, reader='d', scale=1):
    c = np.array([x,y,0.])
    g = VGroup(body(c,scale))
    if 'd' in reader: g.add(cups(c,DCC_A,TEAL,scale))
    if 'u' in reader: g.add(cups(c,UNC_A,PURPLE,scale))
    return g


# All tissue routes below are schematic anatomy, not quantitative traces.
def leader(a, b, color=TEXT):
    return Line([*a,0],[*b,0],color=color,stroke_width=2)


def map_full():
    m=cord([-2,-.15,0],1.35,progenitor=False,floor=False)
    labels=VGroup(lab('dorsal commissural neurons',-1.8,3.25,BLUE,26),
        lab('floor plate',2.9,-2.95,size=28),lab('ventricular zone',3.7,1.8,size=26),
        lab('central canal',3.7,.4,size=26),lab('pial surface',3.7,-1.15,size=26))
    lines=VGroup(leader((-3,2.95),(-4.09,1.74)),leader((1.6,-2.95),(-1.7,-2.92)),
        leader((2,1.8),(-1.35,1.2)),leader((2,.4),(-1.6,.4)),leader((2.4,-1.15),(1,-1.15)))
    return m,labels,lines


def assay(question=True):
    tissue=explant([-4,.1,0]).scale(2)
    paths=VGroup(*[smooth([[-3.2,y,0],[-1.9,y+.15,0],[-.6,y+.3,0],[.6,y+.2,0]]).set_stroke(BLUE,5)
        for y in [-.65,.1,.85]])
    tips=VGroup(*[cone(.6,y+.2,'d',.29) for y in [-.65,.1,.85]])
    ab=VGroup(*[caps(np.array([.6,y+.2,0]),DCC_A,.29) for y in [-.65,.1,.85]])
    source=VGroup(RoundedRectangle(width=1.3,height=2.5,corner_radius=.15,color=YELLOW,fill_color=YELLOW,fill_opacity=.16).move_to([4,.1,0]),
        *[Dot([4,y,0],radius=.12,color=YELLOW) for y in [-.6,.1,.8]],lab('netrin',4,1.9,YELLOW,28))
    base=VGroup(lab('3 · Test the receptor',size=32),tissue,paths,tips,source,
        lab('spinal explant',-4,-1.8,BLUE,26),lab('axon outgrowth',-.4,-1.8,BLUE,26),lab('DCC',1.1,1.7,TEAL,26))
    q=VGroup(lab('Predict',0,-2.65,GOLD,28),lab('What happens to the outgrowth?',0,-3.25,size=32))
    return base,ab,VGroup(lab('anti-DCC',-.5,2.5,PINK,28),leader((-.5,2.2),(.65,1.3),PINK)),q


def result():
    # Ordinal low/high encoding specified in FIXES.md. No measured magnitudes.
    xs=[-3.8,-1.1,1.6,4.3]; vals=[.5,3.8,.5,3.8]
    axis=VGroup(Line([-5,-2,0],[5.8,-2,0],color=TEXT),Arrow([-5,-2,0],[-5,2.7,0],buff=0,color=TEXT),
        lab('outgrowth (idealized)',-6.5,.3,size=26).rotate(PI/2),lab('low',-5.65,-1.6,size=26),
        lab('high',-5.65,1.8,size=26))
    bars=VGroup(*[Rectangle(width=1.15,height=h,stroke_width=0,fill_color=c,fill_opacity=.85).move_to([x,-2+h/2,0])
        for x,h,c in zip(xs,vals,[GREY,GREEN,PINK,GREEN])])
    labels=VGroup(*[lab(t,x,-2.8,c,26) for x,t,c in zip(xs,['no netrin','netrin','netrin +\nanti-DCC','netrin +\ncontrol antibody'],[TEXT,YELLOW,PINK,TEXT])])
    return VGroup(axis,bars,labels,lab('Outgrowth · qualitative',0,3.2,size=32),lab('selective block',1.6,-.8,PINK,26))


def inset():
    gel=RoundedRectangle(width=12,height=5.3,corner_radius=.25,color=GREY).move_to([0,-.2,0])
    tissue=explant([.1,-.5,0]).scale(2)
    anatomy=VGroup(Ellipse(width=2.2,height=1.2,color=GREY).move_to([-4.7,1.25,0]),
        Ellipse(width=1.5,height=1.2,color=GREY).move_to([-2.75,1.25,0]),
        lab('midbrain',-4.7,2.3,size=26),lab('hindbrain',-2.75,2.3,size=26),
        leader((-2.8,.55),(-.8,-.2)),lab('explant',.1,-1.8,BLUE,26))
    return VGroup(gel,tissue,anatomy,lab('gel culture',4.7,-2.35,size=26))


def turn_pair(readers=True):
    a=cone(-3.6,.3,'d' if readers else '',1.05)
    b=cone(3.6,.3,'u' if readers else '',1.05)
    source=VGroup(Dot([0,.3,0],radius=.28,color=YELLOW),lab('netrin',0,1.15,YELLOW,28))
    arrows=VGroup(Arrow([-2.2,-1.55,0],[-.5,-1.55,0],buff=0,color=GREEN,stroke_width=7),
        Arrow([3.7,-1.55,0],[5.7,-1.55,0],buff=0,color=RED,stroke_width=7),
        lab('toward netrin',-3,-2.2,GREEN,26),lab('away from netrin',4,-2.2,RED,26))
    labels=VGroup(lab('commissural',-3.6,2.5,BLUE,30),lab('trochlear',3.6,2.5,BLUE,30))
    return a,b,source,arrows,labels


class S00Title(TitleCard):
    TITLE='The Vertebrate Readers: DCC and UNC5'
    LESSON='Netrin and DCC: One Cue, Two Answers'
    def construct(self):
        self.add(lab('BIOCHEMISTRYPEDIA',0,2.25,TEAL,26),lab(self.LESSON,0,1.4,size=28))
        title=VGroup(T('The Vertebrate Readers:',size=42,font=TITLE_FONT),T('DCC and UNC5',size=42,font=TITLE_FONT)).arrange(DOWN,buff=.25).move_to([0,-.15,0])
        self.play(FadeIn(title),Create(Line([-1.4,-1.7,0],[1.4,-1.7,0],color=GOLD)),run_time=.6); self.finish()


class S01Question(SpokenScene):
    def construct(self):
        a=cone(-3,0,'du',1.3); b=cone(3,0,'du',1.3)
        self.add(lab('The Vertebrate Readers',size=34),a,b,lab('worm',-3,-2.2,size=30),lab('rat · same readers?',3,-2.2,size=30),
            lab('toward reader',-3,2.3,TEAL,26),lab('away reader',-3,-3,PURPLE,26),lab('?',3,2.3,GOLD,38))
        self.at('two readers'); self.play(Indicate(a[1:]),run_time=.4)
        self.at('Do vertebrate'); self.play(Indicate(b[1:]),run_time=.5); self.finish()


class S02Map(SpokenScene):
    def construct(self):
        m,l,p=map_full(); self.add(m[0],l,p)
        self.at('follow the commissural'); tip=body(m[2].get_start(),.18); self.add(tip)
        self.play(Create(m[2]),MoveAlongPath(tip,m[2]),run_time=1.7); self.finish()


class S03Dcc(SpokenScene):
    def construct(self):
        a,b=cone(-3,0,'d',1.25),cone(3,0,'d',1.25)
        self.add(a,b,lab('toward reader',-3,2.7,TEAL),lab('human protein',3,2.7,TEAL))
        self.at('toward reader'); self.play(FadeIn(lab('UNC-40',-3,-2.15,TEAL,32)),run_time=.4)
        self.at('resemble a human'); self.play(Create(leader((-1.2,.2),(1.2,.2),TEAL)),FadeIn(lab('similar protein',0,1,size=26)),run_time=.5)
        self.at('Its name is'); self.play(FadeIn(lab('DCC',3,-2.15,TEAL,32)),run_time=.4)
        self.at('deleted in'); self.play(FadeIn(lab('Deleted in Colorectal Cancer',0,-3.1,TEAL,30)),run_time=.4); self.finish()


class S04Cancer(SpokenScene):
    def construct(self):
        chrom=VGroup(*[Line([x,2,0],[x,.7,0],color=GREY,stroke_width=18) for x in [-3.6,-3]],
            *[Line([x,.5,0],[x,-2.5,0],color=GREY,stroke_width=18) for x in [-3.6,-3]],
            Line([-3.75,-1.35,0],[-2.85,-1.35,0],color=TEAL,stroke_width=16))
        colon=smooth([[2.9,-2,0],[2.9,-.9,0],[4.1,-.8,0],[4.1,1.7,0],[1,1.7,0],[1,-.7,0],[1.7,-.8,0]]).set_stroke(BLUE,28)
        self.add(chrom,colon,lab('DCC · chromosome 18',0,3.15,TEAL,32),lab('colon',2.6,-2.6,BLUE,28),
            lab('long arm (18q)',-3.3,-3.15,TEAL,28))
        self.at('first studied'); self.play(FadeIn(lab('often lost in colorectal tumours',1.6,2.5,size=28)),run_time=.4); self.finish()


class S051996(SpokenScene):
    def construct(self):
        xs=[-4.2,0,4.2]
        emb=cord([-4.2,.3,0],.72,progenitor=False,floor=False)[0]
        ex=VGroup(Circle(radius=1.6,color=GREY),explant([0,.3,0]).scale(1.6)).move_to([0,.3,0])
        cells=VGroup(Circle(radius=1.6,color=GREY).move_to([4.2,.3,0]),*[Circle(radius=.32,color=BLUE,fill_color=BLUE,fill_opacity=.25).move_to([4.2+dx,.3+dy,0]) for dx,dy in [(-.7,.4),(.5,.6),(.3,-.5)]])
        self.add(lab('1996 · Three tests of DCC',size=34),emb,ex,cells)
        for i,x in enumerate(xs):
            self.add(RoundedRectangle(width=3.3,height=1,corner_radius=.12,color=GREY).move_to([x,-2.75,0]),lab(str(i+1),x,-2.75,GOLD,32))
        for phrase,text,x in [('rat embryos','rat embryos',-4.2),('spinal explants','spinal explants',0),('cultured cells','cultured cells',4.2)]:
            self.at(phrase); self.play(FadeIn(lab(text,x,-1.65,size=26)),run_time=.35)
        self.at('three things'); self.play(Indicate(Group(*[m for m in self.mobjects if isinstance(m,RoundedRectangle)])),run_time=.4); self.finish()


class S06One(SpokenScene):
    def construct(self):
        m=cord([-1.8,-.2,0],1.3,progenitor=False,floor=False)
        self.add(m,lab('1 · DCC on commissural axons',size=32))
        self.at('is on commissural'); stain=m[2].copy().set_stroke(TEAL,18)
        self.play(Create(stain),FadeIn(lab('DCC present',-1.4,-1.1,TEAL,32)),
            Create(leader((-2.65,-1.1),(-3.65,-1.45),TEAL)),
            m[3].animate.set_color(TEAL),run_time=.65)
        self.add(Line([-3.8,-3.35,0],[-3.1,-3.35,0],color=TEAL,stroke_width=12),
            lab('DCC-positive axon',-.9,-3.35,TEAL,30)); self.finish()


class S07Two(SpokenScene):
    def construct(self):
        cells=VGroup(*[Circle(radius=1.2,color=BLUE,fill_color=BLUE,fill_opacity=.22).move_to([x,-.2,0]) for x in [-3,3]])
        rs=cups(np.array([-3,-.2,0]),DCC_A,TEAL,1.2)
        dots=VGroup(*[Dot([x,2.1,0],radius=.17,color=YELLOW) for x in [-3.6,-2.4,-1.3,2.3,3.5]])
        self.add(lab('2 · Netrin binds DCC-displaying cells',size=32),cells,rs,dots,lab('netrin-1',0,2.4,YELLOW,28),
            lab('DCC on surface',-3,-2.2,TEAL,28),lab('without DCC',3,-2.2,size=28),lab('cultured cells',0,-3.15,BLUE,28))
        self.at('binds cultured cells')
        targets=[[-3+1.74*np.cos(np.radians(a)),-.2+1.74*np.sin(np.radians(a)),0] for a in DCC_A]
        self.play(*[d.animate.move_to(p) for d,p in zip(dots[:3],targets)],run_time=.9); self.finish()


class S08Predict(SpokenScene):
    def construct(self):
        base,ab,al,q=assay(); self.add(base)
        self.at('an antibody'); self.play(FadeIn(ab),FadeIn(al),run_time=.45)
        self.at('What should happen'); self.play(FadeIn(q),run_time=.4); self.finish()


class S09Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(*assay()); self.wait(5)


class S10Reveal(SpokenScene):
    def construct(self):
        g=result(); self.add(g[0],g[2],g[3])
        self.at('The antibody'); self.play(FadeIn(g[1]),run_time=.6)
        self.at('selectively blocked'); self.play(FadeIn(g[4]),run_time=.4); self.finish()


class S11Beat(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(result()); self.wait(2.5)


class S12Worm(SpokenScene):
    def construct(self):
        a=cone(-3,1.1,'d',.65); b=cone(-3,-1.5,'',.65)
        self.add(lab('Worm · receptor acts in the moving cell',size=32),a,b,
            lab('normal · UNC-40',-3,2.4,TEAL,28),lab('UNC-40 mutant',-3,-2.7,size=28),
            Dot([4,1.1,0],radius=.25,color=YELLOW),Dot([4,-1.5,0],radius=.25,color=YELLOW),lab('UNC-6 (netrin)',4,2.3,YELLOW,28))
        self.at('worm work showed'); run(self,[a],[[-3,1.1,0],[-1.5,1.1,0],[.4,1.1,0]],1.1)
        self.at('in the moving cells'); self.play(FadeIn(lab('UNC-40 acts here',.4,-.1,TEAL,28)),FadeIn(lab('fails to migrate',.2,-2.7,RED,26)),run_time=.4); self.finish()


class S13Mouse(SpokenScene):
    def construct(self):
        a=cord([-3.2,0,0],1.15,progenitor=False,floor=False); b=cord([3.2,0,0],1.15,wrong=True,progenitor=False,floor=False)
        self.add(a,b,lab('Mouse · commissural axons',size=32),lab('normal',-3.2,-3.15,BLUE,28),
            lab('little / no netrin-1',3.2,-3.15,YELLOW,26),lab('floor plate',-1.6,-2.7,size=26),
            leader((-2.35,-2.55),(-3.1,-2.36)))
        self.at('had misrooted'); self.play(Indicate(b[2]),run_time=.9); self.finish()


class S14Commissures(SpokenScene):
    def construct(self):
        brains=VGroup()
        for x,label in [(-3.2,'normal forebrain'),(3.2,'netrin-1 mutant')]:
            lobes=VGroup(*[Ellipse(width=2.4,height=4.3,color=GREY).move_to([x+dx,.2,0]) for dx in [-1.25,1.25]])
            brains.add(lobes,lab(label,x,-2.6,size=28))
        normal=VGroup(*[Line([-4,y,0],[-2.4,y,0],color=BLUE,stroke_width=7) for y in [-.4,.2,.8]])
        # Separate stubs end well before the midline; no bundle spans the gap.
        absent=VGroup(*[Line([x1,y,0],[x2,y,0],color=BLUE,stroke_width=7)
            for y in [-.4,.2,.8] for x1,x2 in [(2.4,2.65),(3.75,4)]],
            Line([2.9,-.65,0],[3.5,1.05,0],color=RED,stroke_width=5),
            Line([2.9,1.05,0],[3.5,-.65,0],color=RED,stroke_width=5))
        self.add(brains,normal,absent,lab('Forebrain · crossing bundles',size=32))
        self.at('lacked several'); self.play(FadeIn(lab('missing crossings',3.2,-3.2,RED,28)),run_time=.4)
        self.at('Mice lacking'); self.play(FadeOut(Group(*self.mobjects)),run_time=.25)
        b=cord([0,0,0],1.25,wrong=True,progenitor=False,floor=False)
        self.add(b[0],lab('Dcc mutant',size=32))
        self.at('similar defects'); self.play(Create(b[2]),FadeIn(b[3]),run_time=.6); self.finish()


class S15Same(SpokenScene):
    def construct(self):
        a=cord([-3.2,0,0],1.12,wrong=True,progenitor=False,floor=False)
        b=cord([3.2,0,0],1.12,wrong=True,progenitor=False,floor=False)
        a[2].set_color(YELLOW); b[2].set_color(TEAL)
        b[2].become(smooth([np.array([3.2+x,y,0]) for x,y in
            [(-1.736,1.568),(-1.45,.55),(-.25,-.12),(-.5,.55),(.14,1.272)]]).set_stroke(TEAL,6))
        b[3].shift(RIGHT*.42+DOWN*.24)
        la=lab('no cue\n(netrin-1 mutant)',-3.2,-3,YELLOW,26); lb=lab('no reader\n(Dcc mutant)',3.2,-3,TEAL,26)
        self.add(a,b,la,lb,lab('Similar routing failure',size=32))
        self.at('commissural axons fail')
        self.play(FadeOut(la),FadeOut(lb),a.animate.shift(RIGHT*3.2),b.animate.shift(LEFT*3.2),run_time=.75)
        self.at('much the same way'); self.play(
            FadeIn(lab('no cue\n(netrin-1 mutant)',-3.7,.3,YELLOW,26)),
            Create(leader((-2.45,.3),(-1.75,.55),YELLOW)),
            FadeIn(lab('no reader\n(Dcc mutant)',1.85,.6,TEAL,26)),
            Create(leader((.75,.6),(-.45,.1),TEAL)),run_time=.35); self.finish()


class S16Trochlear(SpokenScene):
    def construct(self):
        self.add(inset(),lab('1995 · Trochlear repulsion',size=32))
        src=VGroup(RoundedRectangle(width=1.1,height=2,corner_radius=.1,color=YELLOW,fill_color=YELLOW,fill_opacity=.2).move_to([4.7,.25,0]),lab('netrin',4.7,1.65,YELLOW,28))
        self.at('Netrin'); self.play(FadeIn(src),run_time=.35)
        self.at('repelled trochlear')
        paths=VGroup(*[smooth([[-.6,-.5+dy,0],[-1.4,-.6+dy,0],[-2.4,-1.1+dy,0],[-4,-1.5+dy,0]]).set_stroke(BLUE,5) for dy in [-.3,0,.3]])
        tips=VGroup(*[body(p.get_start(),.15) for p in paths]); self.add(tips)
        self.play(*[Create(p) for p in paths],*[MoveAlongPath(t,p) for t,p in zip(tips,paths)],FadeIn(lab('trochlear motor axons',-3.6,-2.4,BLUE,26)),run_time=1.2); self.finish()


class S17Second(SpokenScene):
    def construct(self):
        a,b,src,ar,labels=turn_pair(False)
        self.add(lab('Same cue · opposite turns',size=34),src,labels,
            RoundedRectangle(width=5,height=4.8,corner_radius=.2,color=GREY).move_to([-3.6,-.15,0]),
            RoundedRectangle(width=5,height=4.8,corner_radius=.2,color=GREY).move_to([3.6,-.15,0]))
        unknown=VGroup(lab('?',-3.6,.3,GOLD,60),lab('?',3.6,.3,GOLD,60)); self.add(unknown)
        self.at('Different growth cones'); self.play(FadeOut(unknown),FadeIn(a),FadeIn(b),run_time=.45)
        self.at('same cue'); self.play(Indicate(src),run_time=.35)
        self.at('opposite turns'); self.play(FadeIn(ar),run_time=.4)
        self.at('different readers'); self.play(FadeIn(cups(np.array([-3.6,.3,0]),DCC_A,TEAL,1.05)),FadeIn(cups(np.array([3.6,.3,0]),UNC_A,PURPLE,1.05)),
            FadeIn(lab('DCC',-3.6,-3.1,TEAL,30)),FadeIn(lab('Unc5',3.6,-3.1,PURPLE,30)),run_time=.4); self.wait(2); self.finish()


class S18Caveat(SpokenScene):
    def construct(self):
        self.add(inset(),lab('Midbrain–hindbrain · netrin-1 mutant',size=30))
        points=[[-.6,-.5,0],[-1.4,-.65,0],[-2.4,-1.15,0],[-4,-1.5,0]]
        ghost=smooth(points).set_stroke(GREY,15,opacity=.45)
        self.add(ghost,lab('grey = normal route',3.7,.7,size=26))
        self.at('trochlear axons'); path=smooth(points).set_stroke(BLUE,5)
        self.play(Create(path),FadeIn(body(path.get_end(),.18)),run_time=.7)
        self.at('largely normal'); self.play(FadeIn(lab('near-normal route',-3.5,-2.35,BLUE,26)),run_time=.35)
        self.at('Other repellents'); self.play(FadeIn(chip('other repellents',RED,26).move_to([3.7,-.5,0])),FadeIn(lab('other repellents also guide them',0,-3.25,RED,28)),run_time=.35); self.finish()


class S19Fly(SpokenScene):
    def construct(self):
        ladder=VGroup(*[Line([x,-2.65,0],[x,2.4,0],color=GREY,stroke_width=6) for x in [-1.3,-.3]],*[Line([-1.3,y,0],[-.3,y,0],color=GREY) for y in [-2,-.8,.4,1.6]])
        c=cone(-.8,.3,'u',.85)
        unc5=lab('Unc5',-1.2,-1.2,PURPLE,28)
        self.add(ladder,c,unc5,lab('fly embryo nerve cord',-3.2,3.15,size=30),
            Dot([3.8,.3,0],radius=.3,color=YELLOW),lab('netrin',3.8,1.2,YELLOW,30),lab('midline',-.8,-3.15,size=26))
        self.at('a repulsive netrin')
        path=smooth([[-.8,.3,0],[-1.7,.1,0],[-2.8,-.65,0],[-4,-.8,0]]).set_stroke(BLUE,9).set_z_index(-1)
        self.play(Create(path),MoveAlongPath(c,path),unc5.animate.shift(LEFT*3.2+DOWN*1.1),
            GrowArrow(Arrow([2,-1.75,0],[.1,-1.75,0],buff=0,color=RED,stroke_width=7)),
            FadeIn(lab('away from netrin',2,-2.5,RED,28)),run_time=1.2)
        self.finish()


def range_row(y,long=False):
    x=0 if long else 2
    c=cone(x,y,'du' if long else 'u',.58)
    source=VGroup(Dot([5,y,0],radius=.24,color=YELLOW),lab('netrin',5,y+.72,YELLOW,26))
    bracket=VGroup(Line([x,y-1,0],[5,y-1,0],color=TEXT),*[Line([v,y-.9,0],[v,y-1.1,0],color=TEXT) for v in [x,5]])
    text=VGroup(lab('Unc5 + Frazzled' if long else 'Unc5 alone',-3.9,y+.5,PURPLE,28),lab('long range' if long else 'short range',-3.9,y-.2,size=28))
    arrow=Arrow([x-.75,y,0],[x-1.75,y,0],buff=0,color=RED,stroke_width=6)
    return VGroup(c,source,bracket,text,arrow)


class S20Range(SpokenScene):
    def construct(self):
        a,b=range_row(1.25),range_row(-1.4,True)
        self.add(lab('Fly · repulsion at two ranges',size=32),a[0],a[1],a[2],a[3],b[0][0],b[1],b[2],b[3][1],
            lab('Arrows: away from netrin · distances schematic',0,-3.25,size=26))
        self.at('short range repulsion'); self.play(GrowArrow(a[4]),run_time=.4)
        self.at('Long range repulsion'); self.play(Indicate(b[2]),run_time=.4)
        self.at('also needs frazzled'); self.play(FadeIn(b[0][1:]),FadeIn(b[3][0]),GrowArrow(b[4]),run_time=.5)
        self.at('family receptor'); self.play(Transform(self.mobjects[0],lab('Fly · teal Frazzled = DCC family',size=30)),run_time=.35); self.finish()


def rule():
    a,b=cone(-.6,1.3,'d',.68),cone(-.6,-1.4,'u',.68)
    labels=VGroup(lab('DCC: toward',-4,1.6,TEAL,28),lab('UNC5: adds\nrepulsion',-4,-1.3,PURPLE,28))
    src=VGroup(*[VGroup(Dot([4.7,y,0],radius=.25,color=YELLOW),lab('netrin',4.7,y+.7,YELLOW,26)) for y in [1.3,-1.4]])
    ar=VGroup(Arrow([.5,1.3,0],[3.5,1.3,0],color=GREEN,buff=0,stroke_width=7),Arrow([-1.5,-1.4,0],[-2.5,-1.4,0],color=RED,buff=0,stroke_width=7))
    words=VGroup(lab('toward netrin',2,2.15,GREEN,26),lab('away from netrin',1,-2.7,RED,26))
    return a,b,labels,src,ar,words


class S21Rule(SpokenScene):
    def construct(self):
        a,b,l,s,ar,w=rule(); self.add(a,b,l,s,lab('The receptor layer',size=34))
        self.at('DCC draws'); self.play(Indicate(a[1:]),Indicate(l[0]),run_time=.4)
        self.at('a growth cone in'); self.play(GrowArrow(ar[0]),FadeIn(w[0]),run_time=.4)
        self.at('UNC5 receptors'); self.play(Indicate(b[1:]),Indicate(l[1]),run_time=.4)
        self.at('add repulsion'); self.play(GrowArrow(ar[1]),FadeIn(w[1]),run_time=.4); self.finish()


class S22Scope(SpokenScene):
    def construct(self):
        prior=Group(*rule()); self.add(prior,lab('Starting point',0,3.15,GOLD,38))
        hub=VGroup(Dot([0,0,0],radius=.4,color=YELLOW),lab('netrin',0,-.85,YELLOW,32))
        c=cone(-3.8,1,'d',.7)
        d=VGroup(c,lab('DCC family',-3.8,-.6,TEAL,28),leader((-2.5,.7),(-.6,.1),TEAL))
        self.at('DCC family receptors'); self.play(FadeOut(prior),FadeIn(hub),FadeIn(d),run_time=.5)
        self.at('also take part'); self.play(FadeIn(cups(np.array([-3.8,1,0]),UNC_A,PURPLE,.7)),
            FadeIn(lab('can join repulsion',-3.8,-1.25,TEAL,28)),run_time=.45)
        extras=VGroup(chip('other receptors',GREY,28).move_to([3.5,2,0]),
            Square(side_length=.5,color=GREY).move_to([2.3,-1.5,0]),lab('partners',4,-1.5,size=28),
            cups(np.array([3.2,.2,0]),[90],GREY,.7),
            RoundedRectangle(width=.3,height=.65,corner_radius=.08,color=GREY).move_to([2,1.3,0]),
            leader((.6,.2),(2.9,1.45)),leader((.4,-.4),(2,-1.3)))
        self.at('other receptors and partners'); self.play(FadeIn(extras),run_time=.5); self.finish()


class S23Takeaway(SpokenScene):
    def construct(self):
        a,b,s,ar,l=turn_pair(); self.add(a,b,s,ar,l,lab('One shared cue',size=34))
        self.at('the cue is shared'); self.play(Indicate(s),run_time=.4)
        self.at('the receptors a'); self.play(FadeIn(lab('Different receptors, different first answer',0,-3.2,TEAL,30)),run_time=.5); self.finish()


class S24End(EndCard):
    LINE='One shared cue. The receptors a growth cone carries set the first answer.'
    def construct(self):
        lines=VGroup(T('One shared cue.',size=42,font=TITLE_FONT),T('The receptors a growth cone carries',size=36,font=TITLE_FONT),T('set the first answer.',size=40,font=TITLE_FONT)).arrange(DOWN,buff=.3)
        self.play(FadeIn(lines),run_time=.5); self.add(lab('biochemistrypedia.com',0,-2.1,TEAL,26)); self.finish()
