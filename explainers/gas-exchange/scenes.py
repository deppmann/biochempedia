"""Gas Exchange and Breathing — timed to the supplied Kokoro narration.

COLOR MAP (retained from the original film)
  BLOOD = blood, purple
  TEAL = outside medium, water or air
  YELLOW = oxygen / its partial pressure (qualitative brightness)
  RED = limitation / carbon dioxide and its chemical signal
  GREY = structures, outlines and notes
  TEXT = generic labels
All gradients and volumes are qualitative, with no numerical scale.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403


BLOOD = "#B48CF0"


def arr(a, b, color=GREY, w=6, tip=0.25):
    return Arrow(a, b, buff=0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=14)


def bchip(text, color=BLOOD, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def sketch_note(y=-3.45, x=0):
    return T("in this sketch, not to scale", 22, GREY).move_to([x, y, 0])


def bar(x, base, h, w=0.9, color=YELLOW, op=0.5, stroke=None):
    return Rectangle(width=w, height=max(h, 0.02), stroke_color=stroke or color, stroke_width=3,
                     fill_color=color, fill_opacity=op).move_to([x, base + max(h, 0.02) / 2, 0])


def cell(x, y, v, edge, w=1.2, h=0.8):
    return Rectangle(width=w, height=h, stroke_color=edge, stroke_width=3, fill_color=YELLOW,
                     fill_opacity=0.12 + 0.78 * v).move_to([x, y, 0])


# Shared schematic pieces also recalled on the closing card.
def slab():
    return Rectangle(width=0.55, height=3.6, stroke_color=GREY, stroke_width=3,
                     fill_color=GREY, fill_opacity=0.3)


def pump():
    box = RoundedRectangle(width=2.2, height=1.5, corner_radius=0.3,
                           stroke_color=TEAL, fill_color=TEAL, fill_opacity=0.1)
    return VGroup(box, arr([-0.8, 0, 0], [0.8, 0, 0], TEAL))


def sensor():
    return VGroup(Circle(radius=0.5, color=RED),
                  Dot(radius=0.14, color=RED), arr([0.65, 0, 0], [1.4, 0, 0], GREY))


def heading(text):
    return T(text, 32, TEXT, font=TITLE_FONT).move_to([0, 3.15, 0])


def label(text, x, y, color=TEXT, size=24):
    return T(text, size, color).move_to([x, y, 0])


class S00Title(TitleCard):
    LESSON = "Large, thin, moist surfaces"
    TITLE = "Gas Exchange and Breathing"

    def construct(self):
        brand = T("BIOCHEMISTRYPEDIA", 22, TEAL, weight=BOLD)
        subtitle = T(self.LESSON, 24, GREY)
        title = T(self.TITLE, 48, font=TITLE_FONT)
        rule = Line(LEFT*1.2, RIGHT*1.2, color=GOLD, stroke_width=4)
        group = VGroup(brand, subtitle, title, rule).arrange(DOWN, buff=.32)
        self.play(FadeIn(brand), FadeIn(subtitle), run_time=self.beat(.25))
        self.play(Write(title), GrowFromCenter(rule), run_time=self.beat(.35))
        self.wait(self.beat(.2))
        self.play(FadeOut(group), run_time=self.beat(.2))
        self.finish()


class S01Question(SpokenScene):
    def construct(self):
        wall = slab()
        wet = Rectangle(width=0.14, height=3.6, color=TEAL, fill_opacity=0.5).next_to(wall, LEFT, buff=0)
        names = VGroup(label("air or water", -3.7, 2.35, TEAL), label("blood", 3.7, 2.35, BLOOD))
        oxygen = VGroup(label("oxygen: higher → lower", -3, 1.05, YELLOW),
                         arr([-4.6, 0.55, 0], [4.6, 0.55, 0], YELLOW, w=4))
        co2 = VGroup(label("CO₂: lower ← higher", 3, -1.25, RED),
                     arr([4.6, -0.65, 0], [-4.6, -0.65, 0], RED, w=4))
        self.at("Animals take in")
        self.play(FadeIn(wall), FadeIn(wet), FadeIn(names), run_time=0.5)
        self.at("oxygen and remove")
        self.play(FadeIn(oxygen), FadeIn(co2), run_time=0.7)
        self.at("higher partial pressure")
        self.play(ShowPassingFlash(oxygen[1].copy(), time_width=0.6),
                  ShowPassingFlash(co2[1].copy(), time_width=0.6), run_time=0.8)
        rate = label("more area → more transfer", 0, -2.65, TEXT, 28)
        self.at("More area")
        self.play(wall.animate.stretch_to_fit_height(4.6), wet.animate.stretch_to_fit_height(4.6),
                  FadeIn(rate), oxygen[1].animate.set_stroke(width=6), co2[1].animate.set_stroke(width=6), run_time=0.6)
        self.at("a steeper pressure difference")
        self.play(Transform(rate, label("steeper difference → more transfer", 0, -2.65, TEXT, 28)),
                  oxygen[1].animate.set_stroke(width=9), co2[1].animate.set_stroke(width=9), run_time=0.6)
        self.at("a thinner barrier")
        self.play(wall.animate.stretch_to_fit_width(0.2), wet.animate.shift(RIGHT * 0.175),
                  Transform(rate, label("thinner barrier → more transfer", 0, -2.65, TEXT, 28)), run_time=0.6)
        self.at("Breathing and blood flow")
        flows = VGroup(arr([-5.5, -1.8, 0], [-5.5, 1.6, 0], TEAL),
                       arr([5.5, 1.6, 0], [5.5, -1.8, 0], BLOOD))
        self.play(FadeIn(flows), Transform(rate, label("flows maintain the pressure differences", 0, -2.65, TEXT, 28)), run_time=0.7)
        self.finish()


class S02Fick(SpokenScene):
    def construct(self):
        title = heading("Fick’s law")
        numerator = T("k × area × partial-pressure difference", 28)
        denominator = T("thickness", 28, GREY).move_to([1, 0.5, 0])
        numerator.move_to([1, 1.6, 0])
        rule = Line([-4.1, 1.05, 0], [6.1, 1.05, 0], color=GREY)
        rate = label("rate =", -5.4, 1.05, TEXT, 28)
        equation = VGroup(numerator, denominator, rule, rate)
        self.at("This is")
        self.play(FadeIn(title), FadeIn(equation), run_time=0.7)
        self.play(Circumscribe(numerator, color=YELLOW), Circumscribe(denominator, color=GREY), run_time=0.8)
        share = VGroup(bchip("one gas’s contribution", YELLOW, 26).move_to([-2.8, -1.4, 0]),
                       label("of the total pressure", 2.6, -1.4, GREY, 26))
        self.at("Partial pressure is")
        self.play(FadeIn(share), run_time=0.6)
        self.at("Gases dissolve")
        self.play(FadeOut(equation), FadeOut(share), run_time=0.3)
        water = Rectangle(width=1.3, height=3.6, color=TEAL, fill_opacity=0.18).move_to([-0.9, -0.4, 0])
        cells = slab().stretch_to_fit_width(1.5).move_to([0.5, -0.4, 0])
        gas = bchip("gas", YELLOW, 26).move_to([-4.5, -0.4, 0])
        self.play(FadeIn(water), FadeIn(cells), FadeIn(gas),
                  FadeIn(label("water film", -1, 2, TEAL)), FadeIn(label("cells", 1, 2, GREY)), run_time=0.4)
        self.play(gas.animate.move_to([-0.9, -0.4, 0]), run_time=0.6)
        self.at("before crossing cells")
        dissolved = bchip("dissolved gas", YELLOW, 24).move_to([-2.7, -2.8, 0])
        self.play(FadeIn(dissolved), gas.animate.move_to([3.6, -0.4, 0]), run_time=0.7)
        self.at("must stay moist")
        self.play(Indicate(water, color=TEAL), run_time=0.6)
        self.finish()


class S04Mammal(SpokenScene):
    def construct(self):
        title = heading("Mammal: enlarge the chest")
        chest = RoundedRectangle(width=4.2, height=3.4, corner_radius=0.6, color=GREY).move_to([0, -0.3, 0])
        lung = RoundedRectangle(width=2.5, height=2.2, corner_radius=0.5, color=TEAL, fill_opacity=0.1).move_to([0, -0.3, 0])
        diaphragm = ArcBetweenPoints([-2.1, -2, 0], [2.1, -2, 0], angle=-0.8, color=GREY, stroke_width=7)
        dlabel = label("diaphragm", 0, -2.8, GREY)
        ribs = VGroup(*[Line([s*2.1, y, 0], [s*2.55, y-0.35, 0], color=GREY, stroke_width=6)
                        for s in [-1, 1] for y in [0.2, 0.9]])
        airway = Rectangle(width=0.5, height=1.1, color=GREY).move_to([0, 1.35, 0])
        self.at("Breathing renews")
        self.play(FadeIn(title), FadeIn(VGroup(chest, lung, diaphragm, dlabel, ribs, airway)), run_time=0.6)
        self.at("the diaphragm flattens")
        self.play(Transform(diaphragm, Line([-2.5, -2.3, 0], [2.5, -2.3, 0], color=GREY, stroke_width=7)), run_time=0.6)
        self.at("the ribs lift")
        self.play(ribs.animate.shift(UP*0.4 + RIGHT*0.05), run_time=0.45)
        self.at("The chest enlarges")
        self.play(chest.animate.stretch_to_fit_width(5).stretch_to_fit_height(4), lung.animate.scale(1.15), run_time=0.5)
        pressure = label("alveolar pressure < outside", 0, -3.25, TEXT, 26)
        self.at("pressure falls")
        self.play(FadeIn(pressure), run_time=0.4)
        inward = arr([0, 2.4, 0], [0, 0.3, 0], TEAL)
        self.at("air flows in")
        self.play(GrowArrow(inward), run_time=0.5)
        self.at("A frog instead")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.3)
        title = heading("Frog: mouth-floor pump")
        mouth = RoundedRectangle(width=3.4, height=1.5, corner_radius=0.2, color=GREY).move_to([-2, 0.1, 0])
        floor = Line([-3.7, -0.1, 0], [-0.3, -0.1, 0], color=TEAL, stroke_width=7)
        lung = RoundedRectangle(width=2.3, height=2.5, corner_radius=0.5, color=TEAL).move_to([3.6, 0, 0])
        nostril = Dot([-3.4, 0.85, 0], color=TEAL, radius=0.13)
        state = label("nostrils open", -2, 1.65, TEAL)
        self.play(FadeIn(VGroup(title, mouth, floor, lung, nostril, state)), FadeIn(label("lungs", 3.6, -1.8, TEAL)), run_time=0.3)
        intake = arr([-3.4, 2.2, 0], [-3.4, 0.9, 0], TEAL)
        self.play(floor.animate.shift(DOWN*0.8), GrowArrow(intake), run_time=0.5)
        self.at("raises its mouth floor")
        self.play(Transform(state, label("nostrils closed", -2, 1.65, GREY)), nostril.animate.set_color(GREY),
                  floor.animate.shift(UP*1.1), FadeOut(intake), run_time=0.5)
        self.at("push air into")
        self.play(GrowArrow(arr([-0.1, 0.2, 0], [2.3, 0.2, 0], TEAL)), run_time=0.5)
        self.at("Mammal air flows")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.25)
        tube = Rectangle(width=5, height=1.3, color=GREY).move_to([-1.5, 0, 0])
        sac = RoundedRectangle(width=2.6, height=2.6, corner_radius=0.5, color=TEAL).move_to([2.3, 0, 0])
        a = arr([-3.5, 0, 0], [2, 0, 0], TEAL)
        self.play(FadeIn(tube), FadeIn(sac), GrowArrow(a), run_time=0.5)
        self.at("out through the same")
        self.play(Transform(a, arr([2, 0, 0], [-3.5, 0, 0], TEAL)), run_time=0.5)
        self.at("This is tidal")
        self.play(FadeIn(heading("Tidal ventilation")), run_time=0.5)
        self.finish()


class S04Alveolar(SpokenScene):
    def construct(self):
        tube = Rectangle(width=5, height=1.3, color=GREY).move_to([-1.5, 0, 0])
        sac = RoundedRectangle(width=2.6, height=2.6, corner_radius=0.5, color=TEAL).move_to([2.3, 0, 0])
        stale = VGroup(*[Dot([2+dx, dy, 0], radius=0.13, color=GREY) for dx,dy in [(0,.5),(.7,.2),(.2,-.6)]])
        fresh = VGroup(*[Dot([-3+dx, dy, 0], radius=0.13, color=TEAL) for dx,dy in [(0,.3),(.5,-.3),(.8,0)]])
        self.at("Each breath")
        self.play(FadeIn(VGroup(tube,sac,stale,fresh)), FadeIn(heading("Each breath mixes with gas left behind")), run_time=0.6)
        self.play(fresh.animate.shift(RIGHT*5), run_time=0.8)
        self.at("windpipe and bronchi")
        dead = label("dead space: no exchange", -2, -1.5, GREY, 26)
        self.play(tube.animate.set_stroke(YELLOW, 5), FadeIn(dead), run_time=0.6)
        self.at("Alveolar ventilation is")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.3)
        eq = VGroup(T("alveolar ventilation = breathing frequency", 28),
                    T("× (tidal volume − dead space)", 28)).arrange(DOWN, buff=0.2).move_to([0,2,0])
        self.play(FadeIn(eq), run_time=0.7)
        self.at("after subtracting dead space")
        self.play(Circumscribe(eq[1], color=GREY), run_time=0.7)
        self.at("Equal total air movement")
        self.play(eq.animate.shift(UP*0.65), run_time=0.3)
        groups=[]
        for x,name,widths in [(-3.2,"deeper, slower",[2.7,2.7]),(3.2,"shallower, faster",[1.35]*4)]:
            breaths=VGroup()
            for w in widths:
                outer=Rectangle(width=w,height=.55,color=TEAL,fill_color=TEAL,fill_opacity=.45)
                wasted=Rectangle(width=.8,height=.55,color=GREY,fill_color=GREY,fill_opacity=1).align_to(outer,LEFT)
                breaths.add(VGroup(outer,wasted))
            breaths.arrange(DOWN,buff=.17).move_to([x,-.5,0])
            groups.append(VGroup(label(name,x,1.35,TEAL,26),breaths))
        self.play(*[FadeIn(g) for g in groups], FadeIn(label("equal minute ventilation",0,1.95,GREY)), run_time=0.6)
        self.at("different amounts of fresh air")
        self.play(FadeIn(label("more fresh gas reaches alveoli",-3.2,-2.45,TEAL,22)),
                  FadeIn(label("less fresh gas reaches alveoli",3.2,-2.45,TEAL,22)),
                  FadeIn(label("grey = dead space in each breath",0,-3.25,GREY,22)), run_time=0.6)
        self.finish()


class S03Surfaces(SpokenScene):
    def construct(self):
        head=heading("Diffusion across exchange surfaces")
        self.at("Animals use different surfaces")
        self.play(FadeIn(head), run_time=0.6)
        skin=RoundedRectangle(width=8,height=1.1,corner_radius=.45,color=GREY,fill_color=GREY,fill_opacity=.1)
        wet=Line([-4,.6,0],[4,.6,0],color=TEAL,stroke_width=8)
        flow=arr([-1,1.9,0],[-1,-.9,0],YELLOW)
        self.at("Earthworms exchange")
        self.play(FadeIn(VGroup(skin,wet)),GrowArrow(flow),FadeIn(label("earthworm: moist skin",0,-1.8,GREY,28)),run_time=.7)
        self.at("Insects have branching")
        self.play(*[FadeOut(m) for m in list(self.mobjects) if m is not head],run_time=.3)
        trunk=Line([-4.7,0,0],[-1.5,0,0],color=TEAL,stroke_width=9)
        branches=VGroup(*[Line([-1.5,0,0],[1.3,y,0],color=TEAL,stroke_width=6) for y in [-1.3,0,1.3]])
        tips=VGroup(*[Line([1.3,y,0],[3.3,y+dy,0],color=TEAL,stroke_width=3) for y in [-1.3,0,1.3] for dy in [-.3,.3]])
        spiracle=Circle(radius=.22,color=TEAL).move_to([-4.8,0,0])
        tissue=RoundedRectangle(width=1.5,height=4.2,corner_radius=.2,color=GREY).move_to([4.1,0,0])
        self.play(Create(VGroup(trunk,branches,tips,spiracle,tissue)),FadeIn(label("spiracle",-4.8,-1.5,TEAL)),
                  FadeIn(label("tracheae",0,-2.5,TEAL)),FadeIn(label("tissues",4.1,-2.5,GREY)),run_time=1)
        self.at("Water holds far less")
        self.play(*[FadeOut(m) for m in list(self.mobjects) if m is not head],run_time=.3)
        panels=VGroup()
        for x,name,opacity,work in [(-3,"water",.18,"more work to move"),(3,"air",.85,"less work to move")]:
            box=Rectangle(width=3.6,height=2.5,color=TEAL).move_to([x,.2,0])
            gas=Rectangle(width=2.8,height=1.5,color=YELLOW,fill_color=YELLOW,fill_opacity=opacity).move_to(box)
            panels.add(VGroup(box,gas,label(name,x,2,TEAL,28),label(work,x,-2,GREY)))
        self.play(FadeIn(panels),FadeIn(label("equal volumes • brighter = more oxygen",0,-3.1,YELLOW)),run_time=.8)
        self.at("takes more work")
        self.play(Indicate(panels[0][3],color=TEAL),run_time=.7)
        self.finish()


class S03Gill(SpokenScene):
    def construct(self):
        fil=Line([-4,-2,0],[-4,2,0],color=GREY,stroke_width=10)
        plates=VGroup(*[Rectangle(width=6,height=.3,color=GREY,fill_opacity=.15).move_to([-1,y,0]) for y in [-1.4,-.5,.5,1.4]])
        self.at("A trout's gills")
        self.play(FadeIn(heading("Gill filaments carry thin lamellae")),Create(fil),FadeIn(plates),run_time=.8)
        self.at("Inside each lamella")
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.3)
        outline=DashedVMobject(RoundedRectangle(width=11.4,height=4.7,corner_radius=.2,color=GREY),num_dashes=60)
        xs=np.linspace(-4.7,4.7,6)
        water=VGroup(*[cell(x,.85,v,TEAL,w=1.5) for x,v in zip(xs,np.linspace(1,.4,6))])
        blood=VGroup(*[cell(x,-.85,v,BLOOD,w=1.5) for x,v in zip(xs,np.linspace(.9,.3,6))])
        wa=arr([-5,1.8,0],[5,1.8,0],TEAL)
        ba=arr([5,-1.8,0],[-5,-1.8,0],BLOOD)
        self.play(FadeIn(outline),FadeIn(water),FadeIn(blood),GrowArrow(wa),
                  FadeIn(label("water",4.9,2.6,TEAL,22)),run_time=.6)
        self.at("blood runs opposite")
        self.play(GrowArrow(ba),FadeIn(label("blood",4.9,-2.6,BLOOD,22)),run_time=.6)
        self.at("This countercurrent exchange")
        self.play(FadeIn(heading("Countercurrent exchange")),run_time=.5)
        self.at("along its whole length")
        marks=VGroup(*[arr([x,.35,0],[x,-.35,0],YELLOW,w=3,tip=.14) for x in xs])
        self.play(FadeIn(marks),FadeIn(label("oxygen pressure: water > blood at every point",0,-2.9,YELLOW)),run_time=.6)
        self.at("Blood leaving can approach")
        self.play(Circumscribe(VGroup(water[0],blood[0]),color=YELLOW),run_time=.8)
        self.play(FadeIn(label("incoming water / outgoing blood",-2.8,2.55,TEXT,22)),
                  FadeIn(sketch_note()),run_time=.5)
        self.finish()


class S05Bird(SpokenScene):
    def construct(self):
        tube=Rectangle(width=7,height=1.3,color=GREY,fill_color=GREY,fill_opacity=.12).move_to([0,.5,0])
        title=heading("Bird: exchange in parabronchi")
        self.at("Bird lungs exchange")
        self.play(FadeIn(title),FadeIn(tube),run_time=.7)
        sacs=VGroup(*[RoundedRectangle(width=1.7,height=2.4,corner_radius=.5,color=TEAL,fill_opacity=.1).move_to([x,.5,0]) for x in [-4.7,4.7]])
        self.at("Air sacs act")
        self.play(FadeIn(sacs),FadeIn(label("air sacs: bellows",0,-2.6,TEAL,26)),run_time=.5)
        self.play(sacs.animate.stretch(1.2,1),run_time=.5)
        self.play(sacs.animate.stretch(1/1.2,1),run_time=.5)
        a=arr([-3.1,.5,0],[3.1,.5,0],TEAL)
        phase=label("breathing in",0,-1.2,TEAL,26)
        self.at("air flows the same way")
        self.play(GrowArrow(a),FadeIn(phase),run_time=.5)
        self.at("breathing in and out")
        self.play(sacs.animate.stretch(1.2,1),run_time=.5)
        self.play(Transform(phase,label("breathing out",0,-1.2,TEAL,26)),sacs.animate.stretch(1/1.2,1),
                  ShowPassingFlash(a.copy(),time_width=.6),run_time=.7)
        caps=VGroup(*[Rectangle(width=.3,height=2.8,color=BLOOD,fill_color=BLOOD,fill_opacity=.18).move_to([x,.5,0]) for x in [-2,0,2]])
        self.at("Capillaries cross")
        self.play(FadeIn(caps),Transform(phase,label("blood capillaries",0,-1.5,BLOOD,26)),run_time=.7)
        self.at("This is crosscurrent")
        self.play(Transform(title,heading("Crosscurrent exchange")),run_time=.6)
        self.finish()


class S06Control(SpokenScene):
    def construct(self):
        title=heading("What controls breathing?")
        self.at("What controls breathing")
        self.play(FadeIn(title),run_time=.6)
        co2=bchip("carbon dioxide",RED,28).move_to([-4.4,1,0])
        self.at("carbon dioxide sets")
        self.play(FadeIn(co2),FadeIn(label("main resting drive in humans",0,-2.7,GREY,26)),run_time=.7)
        brain=RoundedRectangle(width=4.1,height=2.8,corner_radius=.7,color=GREY).move_to([1.1,.6,0])
        fluid=label("brain extracellular fluid",1.1,2.4,GREY)
        self.at("It enters the brain")
        self.play(FadeIn(brain),FadeIn(fluid),co2.animate.move_to([1.1,1.3,0]),run_time=.7)
        ph=label("pH falls",1.1,.4,RED,30)
        self.at("lowers the fluid's")
        self.play(FadeIn(ph),run_time=.5)
        s=sensor().move_to([1.1,-.5,0])
        self.at("Central chemoreceptors")
        self.play(FadeIn(s),FadeIn(label("central chemoreceptors",1.1,-1.6,RED)),
                  FadeIn(label("sensors → breathing adjustment",0,-3.35,TEXT,24)),run_time=.6)
        self.at("The carotid bodies")
        self.play(*[FadeOut(m) for m in list(self.mobjects) if m is not title],run_time=.3)
        forks=VGroup()
        for x in [-3,3]:
            forks.add(VGroup(Line([x,-1.6,0],[x,0,0],color=BLOOD,stroke_width=10),
                              Line([x,0,0],[x-.8,1.3,0],color=BLOOD,stroke_width=8),
                              Line([x,0,0],[x+.8,1.3,0],color=BLOOD,stroke_width=8),
                              Dot([x+.28,.1,0],radius=.2,color=RED)))
        self.play(Create(forks),FadeIn(label("carotid bodies at artery forks",0,2.35,RED,26)),run_time=.7)
        self.at("mainly to low arterial oxygen")
        low=label("mainly low arterial oxygen",0,-2.35,YELLOW,28)
        self.play(FadeIn(low),run_time=.6)
        self.at("also to carbon dioxide")
        self.play(FadeIn(label("also carbon dioxide",0,-3.05,RED)),run_time=.5)
        self.play(FadeIn(label("sensors → breathing adjustment",0,1.55,TEXT,24)),run_time=.4)
        self.at("With carbon dioxide production unchanged")
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.3)
        self.play(FadeIn(heading("Carbon dioxide production unchanged")),run_time=.4)
        left=bchip("alveolar ventilation ↓",TEAL,28).move_to([-3.3,0,0])
        right=bchip("alveolar CO₂ pressure ↑",RED,28).move_to([3.3,0,0])
        self.at("less alveolar ventilation")
        self.play(FadeIn(left),run_time=.5)
        self.at("lets alveolar carbon dioxide")
        self.play(GrowArrow(arr([-.8,0,0],[.8,0,0],GREY)),FadeIn(right),run_time=.6)
        self.play(FadeIn(label("chemical sensors → breathing adjustment",0,-2.1,TEXT,26)),run_time=.6)
        self.finish()


class S06Alligator(SpokenScene):
    def construct(self):
        self.at("airflow also occurs")
        self.play(FadeIn(heading("Shared one-way airflow")),run_time=.5)
        columns=VGroup()
        for x,name in [(-4.2,"birds"),(0,"alligators"),(4.2,"some lizards")]:
            columns.add(VGroup(pump().move_to([x,.5,0]),label(name,x,1.9,TEXT,28)))
        self.play(FadeIn(columns),run_time=.7)
        self.at("Alligators have no")
        note=label("no air sacs",0,-1.3,GREY,28)
        self.play(FadeIn(note),Circumscribe(columns[1],color=TEAL),run_time=.7)
        self.at("So air sacs")
        self.play(FadeIn(label("Air sacs are not required for one-way flow.",0,-2.7,TEXT,30)),run_time=.7)
        self.finish()


class S07End(EndCard):
    LINE = "Gases cross large, thin surfaces by diffusion; breathing keeps gradients steep."
    def construct(self):
        title=heading(self.LINE)
        fit(title, max_w=12.5)
        icons=VGroup(slab().scale(.45),pump(),sensor()).arrange(RIGHT,buff=2.9).move_to([0,.4,0])
        names=VGroup(*[label(name,icon.get_x(),-1.35,TEXT,26) for name,icon in zip(
            ["diffusion","ventilation","chemical control"],icons)])
        self.play(FadeIn(title),FadeIn(icons),FadeIn(names),run_time=self.beat(.3))
        self.play(FadeIn(label("biochemistrypedia.com",0,-2.9,TEAL,22)),run_time=self.beat(.15))
        self.finish()
