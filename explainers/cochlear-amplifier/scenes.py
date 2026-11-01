"""Cochlear amplifier: active cells, electrical readouts, emissions and feedback.

COLOR MAP (one colour per concept, whole film)
  BLUE   = the outer hair cell and prestin in its extended state (the subject)
  GREEN  = the contracted state and the capacitance it produces (the output we read)
  YELLOW = voltage and the stimulus impulse (the thing that moves)
  TEAL   = the sound that returns from the ear
  GREY   = structure, labels, things not measured
  RED    = crossed out / not shown by that measurement
"""
import numpy as np
from bp_style import *

VH, Z, KTE = -112.0, 0.70, 25.42


def occ(v, z=Z):
    return 1.0 / (1.0 + np.exp(-z * (v - VH) / KTE))


def nlc(v):
    f = occ(v)
    return 4 * f * (1 - f)


def mkaxes(w, h, xr, yr):
    return Axes(x_range=[xr[0], xr[1], 1], y_range=[yr[0], yr[1], 1], x_length=w, y_length=h, tips=False,
                axis_config={"color": GREY, "include_ticks": False, "stroke_width": 2.5})


def curve(ax, fn, xr, color, step=0.5, w=5):
    xs = np.arange(xr[0], xr[1] + 1e-9, step)
    pts = [ax.c2p(x, fn(x)) for x in xs]
    m = VMobject(color=color, stroke_width=w)
    m.set_points_as_corners(pts)
    return m


def bell_axes(w, h, cx, cy):
    ax = mkaxes(w, h, (-220, -20), (0, 1.15)).move_to([cx, cy, 0])
    return ax


def pulse(color=YELLOW, r=0.13):
    return Dot(radius=r, color=color)



def hair_cell(u, x=-3.0, bottom=-2.0):
    """Original rounded cell, anchored at its base as its length changes."""
    h = 4.1 - u.get_value()
    return RoundedRectangle(corner_radius=0.6, width=1.4, height=h,
        stroke_color=BLUE, stroke_width=4, fill_color=BLUE,
        fill_opacity=0.22).move_to([x, bottom + h / 2, 0])


def wave(x, y, amplitude=0.3, width=4.5, color=TEAL):
    m = VMobject(color=color, stroke_width=4)
    m.set_points_as_corners([[x+t, y+amplitude*np.sin(2*PI*t), 0]
                            for t in np.linspace(0, width, 160)])
    return m


def ear(y=0.5):
    mic = chip("microphone", GREY, size=24).move_to([-5.0, y, 0])
    canal = Rectangle(width=3.6, height=0.8, stroke_color=GREY,
        stroke_width=3, fill_color=GREY, fill_opacity=0.08).move_to([-1.9, y, 0])
    label = T("sealed ear canal", 22, GREY).next_to(canal, DOWN, buff=0.18)
    middle = chip("middle ear", GREY, size=24).move_to([1.4, y, 0])
    cochlea = chip("outer hair cells", BLUE, size=24).move_to([4.6, y, 0])
    return VGroup(mic, canal, label, middle, cochlea)


class S00Title(TitleCard):
    LESSON = "The Cochlear Amplifier and Otoacoustic Emissions"
    TITLE = "The cochlear amplifier"


class S01Gain(SpokenScene):
    def construct(self):
        benefits = VGroup(*[T(s, 27, TEXT) for s in
            ["detect weak sounds", "separate nearby frequencies", "handle a wide range of loudness"]])
        benefits.arrange(DOWN, buff=0.4).move_to([0, 0.7, 0])
        self.at("helps us hear")
        self.play(FadeIn(benefits[0]), run_time=0.5)
        self.at("separate nearby frequencies")
        self.play(FadeIn(benefits[1]), run_time=0.5)
        self.at("handle a wide")
        self.play(FadeIn(benefits[2]), run_time=0.5)
        active = chip("active process", GOLD, size=28).move_to([0, -1.7, 0])
        self.at("an active process")
        self.play(FadeIn(active), run_time=0.5)
        self.at("in mammals")
        self.play(FadeOut(benefits), FadeOut(active), run_time=0.4)
        u = ValueTracker(0)
        cell = always_redraw(lambda: hair_cell(u))
        label = T("outer hair cell", 26, BLUE).move_to([-3, 2.8, 0])
        vibration = wave(0.4, 0, 0.18, 5.3)
        energy = Arrow([-1.8, 0, 0], [0.1, 0, 0], color=YELLOW, buff=0.1)
        el = T("adds energy", 24, YELLOW).move_to([-0.7, 1.2, 0])
        self.play(FadeIn(cell), FadeIn(label), Create(vibration), run_time=0.6)
        self.at("add energy")
        self.play(GrowArrow(energy), FadeIn(el), run_time=0.5)
        self.play(u.animate.set_value(1), Transform(vibration, wave(0.4, 0, 0.65, 5.3)), run_time=0.8)
        self.play(u.animate.set_value(0), run_time=0.7)
        self.at("their motor")
        motor = chip("prestin · motor", BLUE, size=26).move_to([-3, -2.8, 0])
        self.play(FadeIn(motor), run_time=0.6)
        self.at("a microphone")
        self.play(*[FadeOut(m) for m in [cell,label,vibration,energy,el,motor]], run_time=0.4)
        e = ear()
        self.play(FadeIn(e), run_time=0.7)
        self.at("sends back out")
        sound = pulse(TEAL).move_to(e[4].get_left())
        self.play(FadeIn(sound), run_time=0.2)
        self.play(sound.animate.move_to(e[0].get_right()), run_time=1.0)
        self.play(FadeOut(sound), FadeIn(T("returning sound", 26, TEAL).move_to([0, 2, 0])), run_time=0.4)
        self.at("check outer hair")
        self.play(FadeIn(T("check outer hair cell function", 28, BLUE).move_to([0,-1.8,0])), run_time=0.5)
        self.finish()


class S02Fast(SpokenScene):
    def construct(self):
        u = ValueTracker(0)
        cell = always_redraw(lambda: hair_cell(u))
        label = T("outer hair cell", 26, BLUE).move_to([-3,2.8,0])
        self.at("how does the cell")
        self.play(FadeIn(cell), FadeIn(label), run_time=0.6)
        channel = chip("transduction channel", YELLOW, size=24).move_to([2.9,2.3,0])
        current = Arrow([1.5,1.65,0], [-2.1,1.65,0], color=YELLOW, buff=0.1)
        cl = T("current",24,YELLOW).move_to([0,2.1,0])
        self.at("current through")
        self.play(FadeIn(channel), GrowArrow(current), FadeIn(cl), run_time=0.6)
        voltage = chip("voltage → prestin", YELLOW, size=26).move_to([2.9,0.6,0])
        self.at("sets the voltage")
        self.play(FadeIn(voltage), run_time=0.5)
        self.at("shorten and lengthen")
        movement = T("somatic motility",26,BLUE).move_to([-3,-2.8,0])
        self.play(FadeIn(movement),u.animate.set_value(1),run_time=0.8)
        self.play(u.animate.set_value(0),run_time=0.8)
        direct = T("direct voltage response",24,YELLOW).move_to([2.9,-0.7,0])
        self.at("responds directly")
        self.play(FadeIn(direct),run_time=0.5)
        self.at("without burning")
        noatp = T("no ATP burned each cycle",24,GREY).move_to([2.9,-1.7,0])
        self.play(FadeIn(noatp),run_time=0.5)
        self.at("in a")
        self.play(*[FadeOut(m) for m in [cell,label,channel,current,cl,voltage,movement,direct,noatp]],run_time=0.5)
        head=T("Prestin knock-in mouse",32,BLUE).move_to([0,2.8,0])
        self.play(FadeIn(head),run_time=0.5)
        normal=VGroup(T("transduction: normal",28,TEXT),T("cell mechanics: normal",28,TEXT)).arrange(DOWN,buff=0.5).move_to([0,0.9,0])
        self.at("transduction and cell")
        self.play(FadeIn(normal),run_time=0.6)
        lost=chip("amplification lost",RED,size=30).move_to([0,-0.9,0])
        self.at("yet amplification")
        self.play(FadeIn(lost),run_time=0.5)
        self.at("motility is necessary")
        conclusion=T("cell-body motility is necessary",28,BLUE).move_to([0,-2.5,0])
        self.play(FadeIn(conclusion),run_time=0.6)
        self.finish()


class S03Bell(SpokenScene):
    def construct(self):
        title=T("Nonlinear capacitance",32,GREEN).move_to([0,3.1,0])
        self.at("one electrical signature")
        self.play(FadeIn(title),run_time=0.5)
        cell=RoundedRectangle(corner_radius=0.5,width=3.6,height=3.4,
            stroke_color=BLUE,stroke_width=4,fill_color=BLUE,fill_opacity=0.12).move_to([-4.2,0.4,0])
        cl=T("cell with prestin",24,BLUE).move_to(cell)
        pip=Line([-1.6,2.4,0],[-2.9,1.7,0],color=YELLOW,stroke_width=5)
        pl=T("voltage clamp",24,YELLOW).move_to([-4.2,2.55,0])
        pr=RoundedRectangle(corner_radius=0.15,width=0.8,height=1,
            stroke_color=BLUE,stroke_width=3,fill_color=BLUE,fill_opacity=0.3).move_to([-4.2,-1.3,0])
        self.at("voltage clamp")
        self.play(FadeIn(VGroup(cell,cl,pip,pl,pr)),run_time=0.6)
        ax=mkaxes(5.7,3.4,(0,5),(0,1.15)).move_to([3,0.3,0])
        xl=T("membrane voltage",24,YELLOW).next_to(ax,DOWN,buff=0.2)
        yl=T("capacitance",24,GREEN).next_to(ax,UP,buff=0.2)
        # Qualitative curve only: no fitted constants, numerical ticks or occupancy readout.
        bell=curve(ax,lambda v: np.exp(-((v-2.5)/1.2)**2),(0,5),GREEN,0.025,6)
        self.at("shows a")
        self.play(Create(ax),FadeIn(xl),FadeIn(yl),Create(bell),run_time=1.2)
        q=pulse(YELLOW).move_to(pr.get_center()+UP*0.28)
        readout=T("readout: charge movement",26,GREEN).move_to([0,-2.65,0])
        self.at("charge movement")
        self.play(FadeIn(q),FadeIn(readout),run_time=0.4)
        self.play(q.animate.shift(DOWN*0.56),run_time=0.6)
        self.play(q.animate.shift(UP*0.56),run_time=0.6)
        self.at("does not measure")
        limit=T("not a force or power measurement",26,RED).move_to([0,-3.35,0])
        self.play(FadeIn(limit),run_time=0.5)
        self.finish()


class S01Echo(SpokenScene):
    def construct(self):
        e=ear(1.1)
        title=T("Otoacoustic emissions",32,TEAL).move_to([0,3,0])
        self.at("returning sound")
        self.play(FadeIn(e),FadeIn(title),run_time=0.6)
        self.at("depend on the active")
        self.play(Indicate(e[4],color=BLUE),run_time=0.6)
        self.at("a microphone")
        d=pulse(TEAL).move_to(e[4].get_left())
        self.play(FadeIn(d),run_time=0.2)
        self.play(d.animate.move_to(e[0].get_right()),run_time=1.1)
        self.play(FadeOut(d),run_time=0.2)
        screen=T("newborn hearing screening",28,TEXT).move_to([0,-0.8,0])
        self.at("newborn hearing screening")
        self.play(FadeIn(screen),run_time=0.6)
        emission=chip("emission present",TEAL,size=26).move_to([-3.2,-2,0])
        self.at("a pass shows")
        self.play(FadeIn(emission),run_time=0.5)
        self.at("through the middle ear")
        self.play(Indicate(e[3],color=TEAL),run_time=0.5)
        caution=T("a pass does not prove intact hearing",28,RED).move_to([0,-3.2,0])
        self.at("does not prove")
        self.play(FadeIn(caution),run_time=0.5)
        self.at("in auditory neuropathy")
        neuro=T("auditory neuropathy",28,RED).move_to([0,-0.8,0])
        self.play(ReplacementTransform(screen,neuro),run_time=0.5)
        self.at("auditory brainstem response")
        response=VGroup(T("auditory nerve → brainstem",24,GREY),
            T("response absent / very abnormal",24,RED)).arrange(DOWN,buff=0.25).move_to([3.1,-2,0])
        self.play(FadeIn(response),run_time=0.6)
        self.at("different stages")
        self.play(Indicate(emission,color=TEAL),Indicate(response,color=RED),run_time=0.6)
        self.finish()


class S08Bundle(SpokenScene):
    def construct(self):
        head=T("Excised adult bullfrog sacculus",30,BLUE).move_to([0,3.1,0])
        base=Line([-5.5,-1.8,0],[-1.5,-1.8,0],color=GREY,stroke_width=5)
        bundle=VGroup(*[Line([-4.4+i*0.55,-1.8,0],[-4.4+i*0.55,-0.1+i*0.35,0],color=BLUE,stroke_width=8) for i in range(4)])
        bl=T("hair bundle",24,BLUE).move_to([-3.5,-2.4,0])
        self.at("in frogs")
        self.play(FadeIn(head),Create(base),Create(bundle),FadeIn(bl),run_time=0.7)
        self.at("a flexible probe")
        probe=VMobject(color=YELLOW,stroke_width=5).set_points_smoothly([[-0.7,2,0],[-1,1.4,0],[-2,0.9,0],[-2.75,0.8,0]])
        pl=T("flexible probe",24,YELLOW).move_to([-1.7,2.4,0])
        self.play(Create(probe),FadeIn(pl),run_time=0.5)
        target=bundle.copy()
        target.apply_function(lambda p: p+RIGHT*(p[1]+1.8)*0.25)
        self.play(Transform(bundle,target),probe.animate.shift(RIGHT*0.45),run_time=0.7)
        self.play(Transform(bundle,VGroup(*[Line([-4.4+i*0.55,-1.8,0],[-4.4+i*0.55,-0.1+i*0.35,0],color=BLUE,stroke_width=8) for i in range(4)])),probe.animate.shift(LEFT*0.45),run_time=0.7)
        balance=VGroup(T("energy dissipated through drag",24,TEXT),T(">",38,TEXT),T("energy supplied by probe",24,YELLOW)).arrange(DOWN,buff=0.3).move_to([3.1,0.8,0])
        self.at("dissipated more energy")
        self.play(FadeIn(balance),run_time=0.6)
        extra=chip("bundle supplies the difference",BLUE,size=24).move_to([3.1,-1.5,0])
        self.at("extra energy came")
        self.play(FadeIn(extra),Indicate(bundle,color=BLUE,scale_factor=1.0),run_time=0.6)
        self.at("a large movement alone")
        note=T("large motion alone ≠ added energy",26,RED).move_to([0,-3.2,0])
        self.play(FadeIn(note),run_time=0.6)
        self.at("a passive bundle")
        self.play(*[FadeOut(m) for m in [probe,pl,balance,extra]],run_time=0.4)
        passive=VGroup(T("passive bundle",27,GREY),T("probe can supply the motion",24,YELLOW)).arrange(DOWN,buff=0.35).move_to([2.8,0.5,0])
        self.play(FadeIn(passive),bundle.animate.set_color(GREY),run_time=0.5)
        self.play(bundle.animate.apply_function(lambda p: p+RIGHT*(p[1]+1.8)*0.35),run_time=0.7)
        self.play(bundle.animate.apply_function(lambda p: p-RIGHT*(p[1]+1.8)*0.35),run_time=0.7)
        self.at("does not show")
        limit=T("mammalian bundle contribution not established here",25,RED).move_to([0,-3.2,0])
        self.play(FadeOut(note),run_time=0.3)
        self.play(FadeIn(limit),run_time=0.3)
        self.finish()


class S09Feedback(SpokenScene):
    def construct(self):
        u=ValueTracker(0)
        cell=always_redraw(lambda: hair_cell(u,x=3.8))
        label=T("outer hair cell",26,BLUE).move_to([3.8,2.8,0])
        brain=chip("brain",GREY,size=28).move_to([-4.8,2.4,0])
        nerve=Arrow([-3.7,2.4,0],[2.9,1.3,0],buff=0.12,color=GREY,stroke_width=4)
        self.at("the brain")
        self.play(FadeIn(brain),FadeIn(cell),FadeIn(label),GrowArrow(nerve),run_time=0.6)
        self.play(u.animate.set_value(1),run_time=0.6)
        self.play(u.animate.set_value(0),run_time=0.6)
        eff=T("medial olivocochlear efferent",24,GREY).move_to([-1.6,3.2,0])
        ach=chip("acetylcholine",YELLOW,size=25).move_to([-1.3,0.5,0])
        self.at("efferents release")
        self.play(FadeIn(eff),FadeIn(ach),run_time=0.5)
        particle=pulse(YELLOW).move_to(ach.get_right())
        self.play(FadeIn(particle),run_time=0.2)
        self.play(particle.animate.move_to([3,0.5,0]),run_time=0.6)
        self.play(FadeOut(particle),run_time=0.2)
        calcium=chip("calcium entry",YELLOW,size=24).move_to([-3.7,-0.9,0])
        potassium=chip("potassium channels",YELLOW,size=24).move_to([0,-0.9,0])
        link=Arrow(calcium.get_right(),potassium.get_left(),buff=0.1,color=YELLOW)
        self.at("calcium entry")
        self.play(FadeIn(calcium),GrowArrow(link),FadeIn(potassium),run_time=0.6)
        self.at("shunts and hyperpolarizes")
        self.play(*[FadeOut(m) for m in [ach,calcium,potassium,link]],run_time=0.4)
        voltage=T("shunting + hyperpolarization",26,YELLOW).move_to([-2.6,0.1,0])
        self.play(FadeIn(voltage),run_time=0.6)
        self.at("suppressing their motility")
        self.play(u.animate.set_value(0.2),run_time=0.6)
        self.play(u.animate.set_value(0),run_time=0.6)
        suppressed=T("reduced motility",26,RED).move_to([3.8,-2.7,0])
        self.play(FadeIn(suppressed),run_time=0.4)
        self.at("this feedback regulates")
        regulation=T("feedback regulates amplification",29,GOLD).move_to([-1.4,-1.4,0])
        self.play(FadeIn(regulation),run_time=0.6)
        self.at("detect weak sounds")
        self.play(*[FadeOut(m) for m in [brain,nerve,eff,voltage,regulation]],run_time=0.4)
        benefits=VGroup(T("detect weak sounds",28,TEXT),T("separate nearby frequencies",28,TEXT)).arrange(DOWN,buff=0.45).move_to([-2,0.4,0])
        self.play(FadeIn(benefits),run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "Mammalian outer hair cells add energy to each sound cycle, via prestin."
