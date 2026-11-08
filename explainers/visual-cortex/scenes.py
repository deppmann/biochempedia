"""Adding Up the Light — revised chapter 1.

COLOR MAP: BLUE recorded cell/spikes; YELLOW light outline; GREEN ON/plus;
RED OFF/minus; GREY structure; GOLD rule; PURPLE complex cells.
White is the bright interior of a light stimulus (yellow boundary).
Steady drive is the normalized area integral, with balanced centre/surround.
Rasters use a deterministic integrate-and-fire illustration: rate =
clip(4 + 17*drive, 0, 24) spikes per displayed interval. They are model
illustrations, not recordings. Off transient uses an explicitly separate
exponential change-response term, never the steady-light sum.
"""
import numpy as np
from bp_style import *

PURPLE = "#B58CD9"
P = np.array([-3.1, 0., 0.])
R = 3.0
RC = R/2


def head(s):
    return T(s, 30).move_to([0, 3.55, 0])


def drive(centre_light, ring_light):
    return (np.pi*RC**2*centre_light/(np.pi*RC**2)
            - np.pi*(R**2-RC**2)*ring_light/(np.pi*(R**2-RC**2)))


def spike_times(v=0, transient=False):
    # Integrate rate on a 1 ms grid; threshold crossings produce every tick.
    t=np.arange(0,1,.001)
    rate=np.full(t.shape,np.clip(4+17*v,0,24),dtype=float)
    if transient:
        rate += 95*np.exp(-t/.12)
    phase=np.cumsum(rate)*.001
    return t[np.flatnonzero(np.diff(np.floor(phase),prepend=0)>0)]


def ticks(v=0, x0=.6, x1=6., y=-1.8, h=.7, transient=False):
    return VGroup(*[Line([x0+(x1-x0)*t,y,0],[x0+(x1-x0)*t,y+h,0],
                        color=BLUE,stroke_width=3) for t in spike_times(v,transient)])


def raster(v=0,label="spontaneous firing",transient=False):
    g=VGroup(Line([.6,-1.8,0],[6,-1.8,0],color=GREY),
             ticks(v,transient=transient),
             T(label,28,BLUE).move_to([3.3,-2.3,0]),
             T("time →",26).move_to([4.9,-3.02,0]),
             T("spikes",26,BLUE).move_to([1.3,-3.02,0]))
    if not len(g[1]):
        g.add(T("no spikes",28,BLUE).move_to([3.3,-1.35,0]))
    return g


def field_icon(radius=R):
    return VGroup(Annulus(inner_radius=radius/2,outer_radius=radius,
                         color=RED,fill_opacity=.23,stroke_width=3),
                  Circle(radius=radius/2,color=GREEN,fill_opacity=.26,stroke_width=3).set_z_index(1),
                  T("+",44 if radius>1 else 28,GREEN),
                  T("−",40 if radius>1 else 26,RED).move_to([0,radius*.77,0]),
                  T("−",40 if radius>1 else 26,RED).move_to([0,-radius*.77,0]))


def field():
    f=field_icon().move_to(P)
    # Labels sit below the corresponding field, with clear leaders.
    f.add(T("centre (ON)",26,GREEN).move_to([-4.45,-3.45,0]),
          T("surround (OFF)",26,RED).move_to([-1.45,-3.45,0]),
          Line([-4.4,-3.15,0],[-3.65,-1.2,0],color=GREEN),
          Line([-1.45,-3.15,0],[-1.5,-2.1,0],color=RED))
    return f


def meter():
    return VGroup(Rectangle(width=.75,height=3.25,color=GREY).move_to([2.25,.8,0]),
                  Line([1.65,.8,0],[2.85,.8,0],color=WHITE,stroke_width=3),
                  T("0",28).move_to([3.15,.8,0]),
                  T("stimulus drive",28).move_to([3.15,2.85,0]),
                  T("steady",26).move_to([4.65,1.05,0]),
                  T("background",26).move_to([4.65,.5,0]))


def fill(v):
    # Keep matching geometry in every state: only the model bar changes height.
    # The near-zero label fades in place rather than morphing into a bar.
    h=max(.025,abs(v)*1.45)
    c=WHITE if abs(v)<.001 else (GREEN if v>0 else RED)
    return VGroup(Rectangle(width=.57,height=h,stroke_width=0,
                            fill_color=c,fill_opacity=.9)
                  .move_to([2.25,.8+np.sign(v)*h/2,0]),
                  T("≈ 0",28).move_to([1.0,.8,0]).set_opacity(1 if abs(v)<.001 else 0))


def light(mode):
    kw=dict(fill_color=WHITE,fill_opacity=.9,color=YELLOW,stroke_width=3)
    if mode=="spot": wash=Circle(radius=RC,**kw)
    elif mode=="ring": wash=Annulus(inner_radius=RC,outer_radius=R,**kw)
    else: wash=Circle(radius=R,**kw)
    wash.move_to(P).set_z_index(-1)
    signs=VGroup()
    if mode!="ring": signs.add(T("+",44,"#285220").move_to(P))
    if mode!="spot":
        signs.add(*[T("−",40,"#96251E").move_to(P+UP*y) for y in (R*.77,-R*.77)])
    signs.set_z_index(2)
    return VGroup(wash,signs)


def stage(v=0,mode=None,label="spontaneous firing"):
    g=VGroup(field(),meter(),fill(v),raster(v,label))
    if mode: g.add(light(mode))
    return g


def question():
    return head("Light over the whole patch?")


def rule_card(full=False):
    g=VGroup(T("Approximate rule",36,font=TITLE_FONT).move_to([0,3.25,0]),
             T("Add up the light",46).move_to([0,2.25,0]),
             chip("+  ON region",GREEN,38,pad=.4).move_to([-3, .95,0]),
             chip("−  OFF region",RED,38,pad=.4).move_to([3,.95,0]))
    if full:
        g.add(T("Bigger sum → stronger drive",34).move_to([0,-.3,0]),
              T("Near zero → spontaneous rate",32).move_to([0,-1.05,0]),
              T("Positive → can raise firing",30,GREEN).move_to([-3.05,-1.85,0]),
              T("Negative → lower firing",30,RED).move_to([3.05,-1.85,0]),
              T("Firing also depends on baseline,",30).move_to([0,-2.65,0]),
              T("threshold and saturation.",30).move_to([0,-3.3,0]))
    return g


class S00Title(TitleCard):
    LESSON="Visual Cortex"
    TITLE="Adding Up the Light"


class S01Question(SpokenScene):
    def construct(self):
        screen=Rectangle(width=5.5,height=5.8,color=GREY,fill_opacity=.12).move_to([-3.35,.15,0])
        spot=Circle(radius=.28,color=YELLOW,fill_color=WHITE,fill_opacity=1).move_to(screen)
        title=T("retina",34,BLUE).move_to([3.15,2.75,0])
        def row(v):
            return VGroup(Line([.5,-.6,0],[6,-.6,0],color=GREY),
                          ticks(v,x0=.5,x1=6,y=-.6,h=1.7),
                          T("spikes",28,BLUE).move_to([1.2,1.75,0]),
                          T("time →",28).move_to([4.95,-1.25,0]),
                          T("model illustration",26,GREY).move_to([3.2,-2.1,0]))
        dense=row(1)
        self.add(screen)
        self.at("spots of light")
        self.play(FadeIn(spot),FadeIn(dense),FadeIn(title),run_time=.35)
        self.at("in cat visual cortex")
        self.play(Transform(title,T("cat visual cortex",32,BLUE).move_to(title)),
                  Transform(dense,row(-.13)),run_time=.35)
        self.at("a bar at")
        bar=Rectangle(width=.38,height=4.5,color=YELLOW,fill_color=WHITE,fill_opacity=1).rotate(-PI/6).move_to(screen)
        self.play(Transform(spot,bar),run_time=.5)
        self.at("drove some cells hard")
        self.play(Transform(dense,row(1)),run_time=.4)
        self.at("why would")
        self.play(FadeIn(T("Why would a bar beat a spot?",32,font=TITLE_FONT).move_to([0,-3.25,0])),run_time=.35)
        self.finish()


class S02Field(SpokenScene):
    def construct(self):
        screen=Rectangle(width=5.25,height=5.6,color=GREY,fill_opacity=.1).move_to([-3.55,.1,0])
        eye=Circle(radius=2.55,color=GREY).move_to([3.5,.1,0])
        ret=Arc(radius=2.32,start_angle=-PI/2,angle=PI,color=BLUE,stroke_width=7).shift([3.5,.1,0])
        # A soma, dendrites and axon make this a drawn retinal neuron.
        soma=Circle(radius=.2,color=BLUE,fill_color=BLUE,fill_opacity=1).move_to([4.6,.25,0])
        dendrites=VGroup(*[Line(soma.get_left(),[3.7,y,0],color=BLUE,stroke_width=3)
                            for y in (-.35,.25,.85)])
        axon=VMobject(color=BLUE,stroke_width=4).set_points_as_corners([
            soma.get_right(),[5.35,.25,0],[5.35,-1.1,0],[4.9,-1.65,0]])
        cell=VGroup(soma,dendrites,axon)
        label=T("ganglion cell",28,BLUE).move_to([3.7,1.6,0])
        leader=Line(label.get_bottom(),soma.get_top(),color=BLUE,stroke_width=2)
        lens=Ellipse(width=.5,height=1.55,color=GREY).move_to([1.55,.1,0])
        patch=Circle(radius=1.25,color=YELLOW,fill_color=GREY,fill_opacity=.2).move_to([-3.55,.1,0])
        # Leave the patch through the screen's top edge, then travel above both
        # outlines and terminate at the eye edge, rather than crossing the cell.
        link=VMobject(color=BLUE,stroke_width=2).set_points_as_corners([
            patch.get_top(),[-3.55,3.15,0],[3.5,3.15,0],eye.get_top()])
        self.add(screen,patch,eye,lens,ret,cell,label,leader,
                 T("retina",30,BLUE).move_to([3.7,-2.95,0]))
        self.at("start in the retina")
        self.play(Indicate(ret,color=BLUE),run_time=.55)
        self.at("every visual neuron")
        self.play(Create(link),run_time=.55)
        self.at("one patch")
        self.play(FadeIn(T("receptive field",32).move_to([-3.55,-1.85,0])),run_time=.25)
        self.finish()


class S03Oncentre(SpokenScene):
    def construct(self):
        f=field()
        self.add(head("ON-centre ganglion cell"),Circle(radius=R,color=GREY).move_to(P),meter(),raster(),fill(0))
        self.at("take an")
        self.wait(.2)
        self.at("small round")
        self.play(FadeIn(f[1]),FadeIn(f[2]),run_time=.35)
        self.at("excites it")
        self.play(FadeIn(f[5]),Create(f[7]),run_time=.3)
        self.at("ring around it")
        self.play(FadeIn(f[0]),FadeIn(f[3]),FadeIn(f[4]),run_time=.35)
        self.at("the surround")
        self.play(FadeIn(f[6]),Create(f[8]),run_time=.3)
        self.finish()


class S04Spot(SpokenScene):
    def construct(self):
        g=stage()
        self.add(head("ON-centre ganglion cell"),g)
        spot=light("spot").shift(LEFT*.5)
        self.at("shine a small spot")
        self.play(FadeIn(spot),run_time=.35)
        self.at("just fills")
        self.play(spot.animate.shift(RIGHT*.5),run_time=.4)
        self.at("only on plus")
        self.play(Transform(g[2],fill(drive(1,0))),run_time=.35)
        self.at("cell fires faster")
        g[3].become(raster(drive(1,0),"faster firing"))
        self.wait(.4)
        self.finish()


class S05Predict(SpokenScene):
    def construct(self):
        g=stage(1,"spot","faster firing")
        hd=head("ON-centre ganglion cell")
        self.add(hd,g)
        self.at("now light")
        g[3].become(raster())
        self.play(FadeOut(g[4]),Transform(g[2],fill(0)),run_time=.4)
        self.at("whole patch")
        self.play(Transform(hd,question()),run_time=.35)
        self.at("what will")
        self.play(FadeIn(T("Pause and predict",26).move_to([4.8,-.3,0])),run_time=.25)
        self.finish()


class S06Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        centre=np.array([5.85,2.1,0])
        track=Circle(radius=.58,color=WHITE,stroke_width=3).move_to(centre)
        remaining=ValueTracker(1)
        ring=always_redraw(lambda: Arc(radius=.58,start_angle=PI/2,
            angle=TAU*max(.001,remaining.get_value()),color=YELLOW,stroke_width=9).move_arc_center_to(centre))
        self.add(question(),stage(),T("Pause and predict",26).move_to([4.8,-.3,0]),track,ring)
        self.play(remaining.animate.set_value(0),run_time=5,rate_func=linear)


class S07Reveal(SpokenScene):
    def construct(self):
        hd=question()
        self.add(hd,stage())
        self.at("very little")
        self.play(Transform(hd,head("Whole patch: almost no change")),FadeIn(light("whole")),run_time=.4)
        plus=Rectangle(width=.25,height=1.4,color=GREEN,fill_opacity=1).move_to([2.08,1.5,0])
        minus=Rectangle(width=.25,height=1.4,color=RED,fill_opacity=1).move_to([2.42,.1,0])
        self.at("adds plus")
        self.play(GrowFromEdge(plus,DOWN),run_time=.3)
        self.at("ring adds minus")
        self.play(GrowFromEdge(minus,UP),run_time=.3)
        self.at("largely cancel")
        self.play(Transform(plus,Line([1.9,.8,0],[2.25,.8,0],color=GREEN,stroke_width=5)),
                  Transform(minus,Line([2.25,.8,0],[2.6,.8,0],color=RED,stroke_width=5)),run_time=.55)
        self.finish()


class S08Ring(SpokenScene):
    def construct(self):
        g=stage(mode="whole")
        self.add(head("ON-centre ganglion cell"),g)
        self.at("light the ring alone")
        self.play(Transform(g[4],light("ring")),run_time=.5)
        self.at("sum goes negative")
        g[3].become(raster(drive(0,1),"below spontaneous rate"))
        self.play(Transform(g[2],fill(drive(0,1))),run_time=.6)
        self.at("firing drops")
        self.wait(.2)
        self.finish()


class S08bOffburst(SpokenScene):
    def construct(self):
        g=stage(-1,"ring","below spontaneous rate")
        self.add(head("ON-centre ganglion cell"),g)
        self.at("light goes off")
        self.play(FadeOut(g[4]),Transform(g[2],fill(0)),run_time=.4)
        self.at("brief burst")
        burst=raster(0,"burst → spontaneous firing",transient=True)
        burst.remove(burst[2])
        burst_label=VGroup(T("Light-off burst,",26,BLUE),
                           T("not part of the sum",26)).arrange(DOWN,aligned_edge=LEFT,buff=.1)
        burst_label.move_to([.65,-2.42,0],aligned_edge=LEFT)
        bracket=VGroup(Line([.65,-1.97,0],[2.2,-1.97,0],color=BLUE),
                       Line([.65,-1.97,0],[.65,-1.82,0],color=BLUE),
                       Line([2.2,-1.97,0],[2.2,-1.82,0],color=BLUE),burst_label)
        g[3].become(burst)
        self.play(FadeIn(bracket),run_time=.4)
        self.at("change in light")
        self.play(Indicate(bracket[0],color=BLUE),run_time=.4)
        self.at("sum alone")
        self.wait(.2)
        self.finish()


class S09Rule(SpokenScene):
    def construct(self):
        c=rule_card()
        # A large field is present until replaced by the two signed regions.
        f=field_icon(1.7).move_to([0,-1.65,0])
        self.add(c,f)
        self.at("here is the rule")
        self.wait(.2)
        self.at("add up the light")
        self.play(Indicate(f,color=YELLOW),run_time=.45)
        self.at("plus")
        self.play(Indicate(c[2],color=GREEN,scale_factor=1.04),run_time=.25)
        self.at("minus")
        self.play(Indicate(c[3],color=RED,scale_factor=1.04),run_time=.25)
        self.finish()


class S10Rule2(SpokenScene):
    def construct(self):
        self.add(rule_card())
        # Persistent state slots: no previous result disappears as a new one arrives.
        data=[("Bigger sum → stronger drive",TEXT,1),
              ("Near zero → spontaneous rate",TEXT,0),
              ("Positive sum → can raise firing",GREEN,1),
              ("Negative sum → lower firing",RED,-.15),
              ("Negative sum → down to zero firing",RED,-1)]
        slots=VGroup(*[T(s,32,c).move_to([-1.1,-.35-i*.72,0]) for i,(s,c,v) in enumerate(data)])
        self.add(slots.copy().set_opacity(.3))
        cues=("a bigger sum","a sum near zero","a positive sum","a negative sum","down to zero")
        # Mini rasters stay alongside their own stable text line.
        for i,(cue,(s,c,v)) in enumerate(zip(cues,data)):
            self.at(cue)
            slots[i].move_to([-1.1,-.35-i*.72,0])
            base=Line([4.1,slots[i].get_y()-.17,0],[6.2,slots[i].get_y()-.17,0],color=GREY)
            tk=ticks(v,x0=4.1,x1=6.2,y=slots[i].get_y()-.17,h=.35)
            self.play(FadeIn(slots[i]),FadeIn(base),FadeIn(tk),run_time=.18)
            if v==-1:
                self.add(T("no spikes",26,BLUE).move_to([5.15,slots[i].get_y()+.16,0]))
        self.wait(max(.1,12.2-self.elapsed()))
        self.finish()


class S11Card(NarratedScene):
    def construct(self):
        self.clear()
        # Rebuild a clean opaque card; no mini-raster from the prior scene.
        self.add(Rectangle(width=14.23,height=8.01,stroke_width=0,
                           fill_color=BG,fill_opacity=1),rule_card(full=True))
        self.finish()


MAP_POINTS=([-4.4,1.65,0],[-2.5,0,0],[-.5,-1.65,0])


class S12TwoHalves(SpokenScene):
    def construct(self):
        card=rule_card(full=True)
        self.add(card)
        self.at("where the patch sits")
        self.play(Transform(card,chip("Add up the light",GOLD,34,pad=.3,fill_opacity=.24).move_to([3.8,3.15,0])),run_time=.3)
        screen=Rectangle(width=8,height=5.9,color=GREY,fill_opacity=.1).move_to([-1.9,0,0])
        patches=VGroup(*[field_icon(.65).move_to(p) for p in MAP_POINTS])
        cells=VGroup(*[chip("cell",BLUE,28).move_to([5.2,p[1],0]) for p in MAP_POINTS])
        # Each horizontal link has a separate lane; none intersects another field.
        links=VGroup(*[Line(a.get_right(),b.get_left(),color=BLUE) for a,b in zip(patches,cells)])
        self.play(FadeIn(screen),FadeIn(patches),Create(links),FadeIn(cells),run_time=.4)
        self.at("which part of the world")
        self.play(FadeIn(T("where in the visual field",30).move_to([0,-3.3,0])),
                  FadeIn(Circle(radius=.78,color=YELLOW,stroke_width=4).move_to(MAP_POINTS[1])),run_time=.5)
        self.finish()


class S13Layout(SpokenScene):
    def construct(self):
        f=field_icon(.65).move_to(MAP_POINTS[1])
        self.add(f,chip("where",GREY,26).move_to([-5.4,3.1,0]))
        self.at("how plus and minus")
        self.play(f.animate.scale(2.6/.65).move_to([0,-.1,0]),run_time=.4)
        # The circular layout holds until 2.22 s, ~two seconds after scene start.
        self.at("which stimulus",lead=0)
        strips=VGroup(*[Rectangle(width=1.25,height=5.2,color=c,fill_opacity=.25).move_to([x,-.1,0])
                       for x,c in ((-1.25,RED),(0,GREEN),(1.25,RED))],
                      T("−",40,RED).move_to([-1.25,-.1,0]),T("+",44,GREEN).move_to([0,-.1,0]),
                      T("−",40,RED).move_to([1.25,-.1,0]))
        self.play(Transform(f,strips),FadeIn(head("which stimulus")),run_time=.5)
        self.at("reports best")
        bar=Rectangle(width=.7,height=3.5,color=YELLOW,fill_color=WHITE,fill_opacity=.75).move_to([0,-.1,0]).set_z_index(-1)
        self.play(FadeIn(bar),FadeIn(T("+",44,"#285220").move_to([0,-.1,0]).set_z_index(2)),run_time=.3)
        self.finish()


class S15Thalamus(SpokenScene):
    def construct(self):
        # Triangular group allows all three fields to be large without collisions.
        fields=VGroup(field_icon(1.55).move_to([-4.2,1.25,0]),
                      field_icon(1.55).move_to([-.85,1.25,0]),
                      field_icon(1.55).move_to([-2.5,-2.0,0]))
        v1=chip("V1  ?",BLUE,44,pad=.55).move_to([4.55,0,0])
        arrow=Arrow([1,0,0],[3.1,0,0],color=GREY,buff=0)
        self.add(head("LGN: thalamic relay"),fields,arrow,v1)
        self.at("cells of the thalamic relay")
        self.play(Circumscribe(fields[0],color=BLUE,buff=.08),run_time=.45)
        self.at("lateral geniculate nucleus")
        self.play(Transform(self.mobjects[0],head("Lateral geniculate nucleus (LGN)")),run_time=.35)
        self.at("fields of the same kind")
        self.play(Circumscribe(fields[1],color=BLUE,buff=.08),run_time=.45)
        self.finish()


class S16Scope(SpokenScene):
    def construct(self):
        self.add(head("Good first approximation"))
        icons=VGroup()
        for i,(name,x) in enumerate(zip(("retina","LGN","V1 simple cell"),(-4.3,0,4.3))):
            if i<2: shape=field_icon(1.6).move_to([x,.55,0])
            else:
                shape=VGroup(*[Rectangle(width=.95,height=3.2,color=c,fill_opacity=.25).move_to([x+dx,.55,0])
                               for dx,c in ((-.95,RED),(0,GREEN),(.95,RED))])
            icons.add(VGroup(shape,T(name,32).move_to([x,2.65,0])))
        self.add(icons.copy().set_opacity(.35))
        self.add(Line([-5.9,-1.35,0],[5.9,-1.35,0],color=GREY))
        self.at("good first approximation")
        self.wait(.2)
        self.at("many cells in the retina")
        self.play(FadeIn(icons[0]),run_time=.3)
        self.at("and thalamus")
        self.play(FadeIn(icons[1]),run_time=.3)
        self.at("simple cells in cortex")
        self.play(FadeIn(icons[2]),run_time=.3)
        cx=VGroup(*[Rectangle(width=.65,height=1.55,color=GREY,fill_opacity=.35).move_to([-4.35+dx,-2.45,0])
                    for dx in (-.8,0,.8)],
                  T("complex cell",34,TEXT).move_to([-.9,-2.2,0]),
                  T("beyond one sum",30,TEXT).move_to([3.25,-2.75,0]),
                  Line([1.9,-2.35,0],[1.9,-1.65,0],color=WHITE),
                  Polygon([1.9,-1.65,0],[2.8,-1.9,0],[1.9,-2.15,0],color=GREY,fill_opacity=.7))
        self.at("later we find",lead=.25)
        self.add(cx)
        self.wait(max(.1,self.narration_s+1.4-self.elapsed()))
        self.finish()


class S17Takeaway(SpokenScene):
    def construct(self):
        c=rule_card(full=True)
        self.at("keep the rule")
        self.play(FadeIn(c),run_time=.25)
        self.at("add up")
        self.play(Indicate(c[1],color=YELLOW,scale_factor=1.04),run_time=.4)
        self.at("plus on on regions")
        self.play(Indicate(c[2],color=GREEN,scale_factor=1.06),run_time=.4)
        self.at("minus on off regions")
        self.play(Indicate(c[3],color=RED,scale_factor=1.06),run_time=.4)
        self.finish()


class S18End(EndCard):
    LINE="Add up the light: plus on ON, minus on OFF."
