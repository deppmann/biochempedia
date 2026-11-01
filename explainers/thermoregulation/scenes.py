"""Heat in, heat out, and the controller. Timed to the new Kokoro narration.

COLOR MAP (retained throughout)
  ORANGE = heat made, flowing, lost, and plotted metabolic rate
  BLUE = surroundings, body outline, cold, and thick-fur comparison
  GREEN = thermoneutral zone / basal rate
  GOLD = controller / defended temperature
  RED = fever / cooling-alone caveat
  YELLOW = highlighted action
  GREY = axes, notes, insulation
  TEXT = labels
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F2994A"
HEAT, AIR, ZONE, SETP, UP_C, HI = ORANGE, BLUE, GREEN, GOLD, RED, YELLOW


def body(w=3.4, h=2.0, label=None, size=28, color=AIR):
    r = RoundedRectangle(corner_radius=0.25, width=w, height=h, stroke_color=color, stroke_width=3.5,
                         fill_color=color, fill_opacity=0.10)
    g = VGroup(r)
    if label:
        g.add(T(label, size, TEXT).move_to(r))
    return g


def arrow(a, b, color=HEAT, sw=7, tip=0.28, both=False):
    cls = DoubleArrow if both else Arrow
    return cls(np.array(a, dtype=float), np.array(b, dtype=float), buff=0, color=color, stroke_width=sw,
               max_tip_length_to_length_ratio=0.3, max_stroke_width_to_length_ratio=12, tip_length=tip)


def tag(text, x, y, size=22, color=GREY):
    return T(text, size, color).move_to([x, y, 0])


class Sc(SpokenScene):
    def rt(self, f):
        return min(max(0.4, self.beat(f)), 1.1)


def dial(x=0, y=0, radius=0.38):
    rim = Circle(radius=radius, color=SETP, stroke_width=4)
    needle = Line(ORIGIN, [radius * 0.65, radius * 0.4, 0], color=SETP, stroke_width=4)
    return VGroup(rim, needle).move_to([x, y, 0])


class S00Title(TitleCard):
    LESSON = "Metabolic Rate and Body Temperature"
    TITLE = "Heat In, Heat Out, and the Controller"


class S07End(EndCard):
    LINE = "A controller decides where the heat balance sits."


class S01Balance(Sc):
    def construct(self):
        bx = body(4.4, 3.0).move_to([0, 0.4, 0])
        name = tag("body", 0, 1.35, 32, TEXT)
        self.at("An animal's body")
        self.play(Create(bx[0]), FadeIn(name), run_time=0.7)
        met = chip("metabolism", HEAT, size=28).move_to([0, 0.35, 0])
        made = tag("heat made", 0, -0.45, 26, HEAT)
        self.at("Heat made by")
        self.play(FadeIn(met, scale=0.8), FadeIn(made), run_time=0.7)
        incoming = VGroup(arrow([-5.9, 0.4, 0], [-2.3, 0.4, 0]),
                          tag("heat gained", -4.2, 1.1, 28, HEAT),
                          tag("sun / rock", -4.2, -0.3, 26, AIR))
        self.at("plus heat gained")
        self.play(GrowArrow(incoming[0]), FadeIn(incoming[1:]), run_time=0.7)
        more = tag("air / water", -4.2, -0.9, 26, AIR)
        self.at("air or water")
        self.play(FadeIn(more), run_time=0.4)
        outgoing = VGroup(arrow([2.3, 0.4, 0], [5.9, 0.4, 0]),
                          tag("heat lost", 4.2, 1.1, 28, HEAT),
                          tag("surroundings", 4.2, -0.3, 26, AIR))
        self.at("against heat lost")
        self.play(GrowArrow(outgoing[0]), FadeIn(outgoing[1:]), run_time=0.7)
        ctrl = VGroup(dial(0, 2.7), tag("controller", 2.0, 2.7, 28, SETP))
        self.at("a controller adjusts")
        self.play(FadeIn(ctrl), run_time=0.4)
        self.play(Rotate(ctrl[0][1], angle=PI/3, about_point=ctrl[0][0].get_center()), run_time=0.4)
        self.at("how much heat they make")
        self.play(Indicate(met, color=HI), run_time=0.5)
        self.at("how much they lose")
        self.play(Indicate(outgoing[0], color=HI), run_time=0.5)
        self.at("what they do")
        self.play(Indicate(incoming[0], color=HI), run_time=0.5)
        ig = chip("desert iguana", AIR, size=28).move_to([-2.3, -2.4, 0])
        temp = M("near or above 37 °C", 30, HEAT).move_to([2.3, -2.4, 0])
        self.at("a desert iguana")
        self.play(FadeIn(ig), run_time=0.6)
        self.at("warmer than you are")
        self.play(FadeIn(temp, shift=UP*0.15), run_time=0.7)
        self.finish()


class S02Routes(Sc):
    def construct(self):
        bx = body(4.0, 2.0, "body", size=34).move_to([0, 0.4, 0])
        self.at("Heat moves by")
        self.play(Create(bx[0]), FadeIn(bx[1]), run_time=0.6)
        rad = VGroup(arrow([0, 1.55, 0], [0, 2.7, 0], both=True), tag("Radiation", 0, 3.15, 30, TEXT))
        con = VGroup(arrow([0, -0.75, 0], [0, -1.65, 0], both=True),
                     Rectangle(width=4, height=0.3, color=GREY, fill_opacity=0.3).move_to([0,-1.85,0]),
                     tag("Conduction", 0,-2.45,30,TEXT))
        cv = VGroup(arrow([2.15,0.4,0],[5.7,0.4,0],both=True),tag("Convection",4.1,1.1,30,TEXT),
                    tag("moving air / water",4.1,-0.25,22,AIR))
        ev = VGroup(arrow([-2.15,0.4,0],[-5.7,0.4,0]),tag("Evaporation",-4.1,1.1,30,TEXT),
                    tag("water → vapour",-4.1,-0.25,24,AIR))
        for cue, route in [("Radiation",rad),("Conduction",con),("Convection",cv),("And evaporation",ev)]:
            self.at(cue)
            self.play(FadeIn(route), run_time=0.7)
        self.at("The first three")
        self.play(Indicate(VGroup(rad[0],con[0],cv[0]),color=HI,scale_factor=1.04),run_time=0.8)
        cost = tag("out only • costs water",-4.1,-1.1,24,HEAT)
        self.at("Evaporation only removes")
        self.play(Indicate(ev[0],color=HI),FadeIn(cost),run_time=0.7)
        self.at("Animals adjust these routes")
        self.play(FadeOut(VGroup(rad,con,cv,ev,cost)),bx.animate.move_to([0,1.7,0]),run_time=0.7)
        knobs = []
        specs=[("fur and feathers","fur / feathers",-3.6,0.0),
               ("Blood flow","skin blood flow",0,0.0),
               ("Countercurrent exchange","countercurrent",3.6,0.0),
               ("sweating or panting","sweat / pant",-2,-2),
               ("and behavior","behaviour",2,-2)]
        for cue,label,x,y in specs:
            g=VGroup(dial(x,y+0.45,0.27),chip(label,AIR,size=24).move_to([x,y-0.3,0]))
            self.at(cue)
            self.play(FadeIn(g),run_time=0.35)
            knobs.append(g)
        self.finish()


class S03Loop(Sc):
    def construct(self):
        heading=tag("Mammalian temperature control",0,3.2,32,TEXT)
        self.at("What adjusts them")
        self.play(FadeIn(heading),run_time=0.5)
        skin=chip("skin sensors",AIR,size=28).move_to([-4.5,1.6,0])
        core=chip("core sensors",AIR,size=28).move_to([-4.5,-0.1,0])
        detail=tag("brain • spinal cord\nabdomen",-4.5,-1.0,22,GREY)
        ctrl=chip("preoptic area\nhypothalamus",SETP,size=26).move_to([0,0.8,0])
        a=arrow(skin.get_right(),ctrl.get_left()+UP*0.3,color=AIR,sw=5)
        b=arrow(core.get_right(),ctrl.get_left()+DOWN*0.3,color=AIR,sw=5)
        self.at("sensors in the skin")
        self.play(FadeIn(skin),run_time=0.6)
        self.at("and sensors in the brain")
        self.play(FadeIn(core),FadeIn(detail),run_time=0.6)
        self.at("A controller in")
        self.play(FadeIn(ctrl),GrowArrow(a),GrowArrow(b),run_time=0.8)
        cold=chip("cold response",AIR,size=28).move_to([4.4,1.7,0])
        warm=chip("warm response",HEAT,size=28).move_to([4.4,-0.4,0])
        out=arrow(ctrl.get_right(),cold.get_left(),color=SETP,sw=5)
        vessel=VGroup(Line([-0.4,-1.8,0],[-0.4,-2.7,0],color=HEAT,stroke_width=5),
                       Line([0.4,-1.8,0],[0.4,-2.7,0],color=HEAT,stroke_width=5))
        vl=tag("skin vessels",0,-3.15,24,GREY)
        self.at("In the cold")
        self.play(FadeIn(cold),GrowArrow(out),Create(vessel),FadeIn(vl),run_time=0.6)
        coldtext=tag("narrow vessels",4.4,0.85,24,AIR)
        heating=tag("shiver • brown fat",4.4,0.2,24,HEAT)
        self.at("narrows skin blood vessels")
        self.play(vessel[0].animate.shift(RIGHT*0.22),vessel[1].animate.shift(LEFT*0.22),FadeIn(coldtext),run_time=0.6)
        self.at("calls for shivering")
        self.play(FadeIn(heating),run_time=0.5)
        warmtext=tag("widen vessels",4.4,-1.25,24,HEAT)
        evaporate=tag("sweat / pant",4.4,-1.9,24,HEAT)
        out2=arrow(ctrl.get_right(),warm.get_left(),color=SETP,sw=5)
        self.at("In the warm")
        self.play(FadeOut(VGroup(cold,coldtext,heating,out)),FadeIn(warm),GrowArrow(out2),run_time=0.6)
        self.at("widens skin vessels")
        self.play(vessel[0].animate.shift(LEFT*0.45),vessel[1].animate.shift(RIGHT*0.45),FadeIn(warmtext),run_time=0.6)
        self.at("turns on sweating")
        self.play(FadeIn(evaporate),run_time=0.5)
        self.at("Skin sensors can")
        flat=VGroup(Line([-5.6,-2.5,0],[-3.4,-2.5,0],color=SETP,stroke_width=5),
                    tag("core temperature: unchanged",-3.8,-3.15,22,GREY))
        self.play(FadeOut(VGroup(warm,warmtext,evaporate,out2,vessel,vl)),FadeIn(flat),
                  Indicate(skin,color=HI),ShowPassingFlash(a.copy().set_color(HI),time_width=0.6),run_time=0.8)
        self.at("before the core")
        self.play(Indicate(flat[0],color=HI),Indicate(ctrl,color=SETP),run_time=0.7)
        self.finish()


class S04Sources(Sc):
    def construct(self):
        L,R=-3.4,3.4
        bl=body(5.2,2.8).move_to([L,-0.1,0])
        br=body(5.2,2.8).move_to([R,-0.1,0])
        self.at("Where the heat comes")
        self.play(Create(bl[0]),Create(br[0]),run_time=0.6)
        title=VGroup(tag("Endotherm",L,3.1,34,TEXT),tag("mammals and birds",L,2.5,26,GREY))
        self.at("Mammals and birds")
        self.play(FadeIn(title),run_time=0.6)
        met=chip("own metabolism",HEAT,size=30).move_to(bl)
        ins=RoundedRectangle(corner_radius=0.3,width=5.6,height=3.2,stroke_color=GREY,stroke_width=9).move_to(bl)
        self.at("their own metabolism")
        self.play(FadeIn(met,scale=0.8),Create(ins),run_time=0.7)
        title2=VGroup(tag("Ectotherm",R,3.1,34,TEXT),tag("desert iguana",R,2.5,26,GREY))
        ig=chip("iguana",AIR,size=26).move_to([2.2,0,0])
        self.at("Ectotherms like")
        self.play(FadeIn(title2),FadeIn(ig),run_time=0.6)
        sun=tag("sun",2.1,1.85,26,AIR)
        rock=tag("warm rock",2.1,-2.1,26,AIR)
        incoming=VGroup(arrow([2.1,1.55,0],[2.1,0.55,0]),arrow([2.1,-1.75,0],[2.1,-0.55,0]))
        self.at("from outside")
        self.play(FadeIn(sun),FadeIn(rock),GrowArrow(incoming[0]),GrowArrow(incoming[1]),run_time=0.6)
        shade=Rectangle(width=2.1,height=2.3,stroke_color=GREY,fill_color=GREY,fill_opacity=0.25).move_to([4.8,-0.1,0])
        sh=tag("shade",4.8,-1.85,26,GREY)
        self.at("moving between sun and shade")
        self.play(FadeIn(shade),FadeIn(sh),FadeOut(incoming),ig.animate.move_to([4.8,0,0]),run_time=0.9)
        note=tag("Ectotherm names the heat source",0,-3.1,30,HI)
        self.at("Ectotherm names")
        self.play(FadeIn(note),run_time=0.6)
        self.finish()


def zone_curve(L, B, s, U, su):
    def f(x):
        if x < L:
            return B + s * (L - x)
        if x <= U:
            return B
        return B + su * (x - U)
    return f


class S05Cost(Sc):
    def construct(self):
        note=tag("in this sketch • relative units",0,3.3,24,GREY)
        self.at("Keeping warm costs")
        self.play(FadeIn(note),run_time=0.5)
        ax=Axes(x_range=[0,10,1],y_range=[0,6,1],x_length=9.6,y_length=4.6,
                axis_config={"color":GREY,"include_ticks":False,"include_numbers":False,"stroke_width":3},tips=True).move_to([0.7,0.4,0])
        xl=tag("air temperature",0.7,-3.15,26,GREY)
        yl=T("resting metabolic rate",26,GREY).rotate(PI/2).next_to(ax.y_axis,LEFT,buff=0.3)
        self.at("resting metabolic rate")
        self.play(Create(ax),FadeIn(xl),FadeIn(yl),run_time=0.8)
        B,L,U=1.4,4.4,8.0
        f=zone_curve(L,B,0.75,U,1.2)
        flat=ax.plot(f,x_range=[L,U],color=ZONE,stroke_width=7)
        cold=ax.plot(f,x_range=[0.05,L],color=HEAT,stroke_width=7)
        hot=ax.plot(f,x_range=[U,9.4],color=HEAT,stroke_width=7)
        zl=T("thermoneutral zone",26,ZONE).move_to(ax.c2p(6.2,2.05))
        self.at("the line is flat")
        self.play(Create(flat),FadeIn(zl),run_time=0.7)
        basal=T("basal rate",24,ZONE).move_to(ax.c2p(6.2,0.8))
        self.at("at basal metabolic rate")
        self.play(FadeIn(basal),run_time=0.5)
        vl=DashedLine(ax.c2p(L,0),ax.c2p(L,B),color=GREY)
        vu=DashedLine(ax.c2p(U,0),ax.c2p(U,B),color=GREY)
        ll=T("lower critical\ntemperature",22,GREY).move_to(ax.c2p(L,0)+DOWN*0.55)
        ul=T("upper critical\ntemperature",22,GREY).move_to(ax.c2p(U,0)+DOWN*0.55)
        self.at("Below the lower critical")
        self.play(Create(cold),Create(vl),FadeIn(ll),Create(hot),Create(vu),FadeIn(ul),run_time=0.9)
        slope=T("steepness → conductance",26,HEAT).move_to(ax.c2p(4.7,4.9))
        self.at("The steepness of")
        self.play(Indicate(cold,color=HI,scale_factor=1.03),FadeIn(slope),run_time=0.8)
        f2=zone_curve(1.9,B,0.38,U,1.2)
        arc=ax.plot(f2,x_range=[0.05,L],color=AIR,stroke_width=7)
        label=T("thick fur • arctic",24,AIR).move_to(ax.c2p(2.0,0.65))
        tropical=T("tropical",24,HEAT).move_to(ax.c2p(1.5,4.7))
        self.at("arctic mammals")
        self.play(FadeOut(slope),Create(arc),FadeIn(label),FadeIn(tropical),run_time=0.8)
        colder=arrow(ax.c2p(4.1,2.5),ax.c2p(2.0,2.5),color=HI,sw=5)
        self.at("much colder air")
        self.play(GrowArrow(colder),run_time=0.7)
        self.finish()


class S06Setpoint(Sc):
    def construct(self):
        ax_x = -2.8
        scale = Arrow([ax_x, -3.1, 0], [ax_x, 3.2, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.25)
        sl = T("body temperature", 26, GREY).rotate(PI / 2).move_to([ax_x - 0.55, 0, 0])
        nts = T("not to scale", 24, GREY).move_to([ax_x + 1.8, -3.25, 0])
        line = Line([ax_x + 0.3, 0, 0], [ax_x + 3.8, 0, 0], color=SETP, stroke_width=9)
        lab = T("set point", 32, SETP).next_to(line, UP, buff=0.12).align_to(line, LEFT)
        grp = VGroup(line, lab)
        self.at("The controller can")
        self.play(Create(scale), FadeIn(sl), FadeIn(nts), Create(line), FadeIn(lab), run_time=0.8)
        self.at("In fever")
        f = chip("fever: raised", UP_C, size=32).move_to([4.2, 1.8, 0])
        self.play(grp.animate.shift(UP * 1.8), FadeIn(f, shift=UP * 0.1), run_time=self.rt(0.07))
        self.at("In torpor")
        t = chip("torpor: drops", AIR, size=32).move_to([4.2, -1.8, 0])
        self.play(grp.animate.shift(DOWN * 3.6), FadeOut(f), FadeIn(t, shift=DOWN * 0.1), run_time=self.rt(0.07))
        self.at("In hibernating black")
        left = VGroup(scale, sl, nts, grp, t)
        self.play(FadeOut(left), run_time=0.6)
        base_y, H = -2.7, 4.6
        b1 = Rectangle(width=2.0, height=H, stroke_color=ZONE, stroke_width=3, fill_color=ZONE, fill_opacity=0.45
                       ).move_to([-4.2, base_y + H / 2, 0])
        b1l = VGroup(T("basal rate", 26, ZONE), T("100%", 28, ZONE)).arrange(DOWN, buff=0.1).next_to(b1, DOWN, buff=0.15)
        b2 = Rectangle(width=2.0, height=H * 0.25, stroke_color=HEAT, stroke_width=3, fill_color=HEAT, fill_opacity=0.5
                       ).move_to([-1.5, base_y + H * 0.125, 0])
        b2l = VGroup(T("black bear", 26, HEAT), T("25%", 28, HEAT)).arrange(DOWN, buff=0.1).next_to(b2, DOWN, buff=0.15)
        hdr = T("hibernating black bear", 30, TEXT).move_to([-2.85, 3.3, 0])
        self.play(FadeIn(hdr), FadeIn(b1), FadeIn(b1l), run_time=0.6)
        self.at("metabolism fell to")
        self.play(FadeIn(b2), FadeIn(b2l), run_time=0.6)
        self.at("body temperature stayed")
        bt = VGroup(T("body temperature", 30, GOLD), T("30 to 36 °C", 30, GOLD)).arrange(DOWN, buff=0.12)
        bb = RoundedRectangle(corner_radius=0.14, width=bt.width + 0.5, height=bt.height + 0.4, stroke_color=GOLD,
                              stroke_width=2.5, fill_color=GOLD, fill_opacity=0.16)
        band = VGroup(bb, bt.move_to(bb)).move_to([3.5, 1.5, 0])
        self.play(FadeIn(band, shift=LEFT * 0.1), run_time=self.rt(0.05))
        self.at("Cooling alone does not")
        ncl = T("not explained by\ncooling alone", 32, UP_C, line_spacing=0.85).move_to([3.5, -0.9, 0])
        self.play(FadeIn(ncl, shift=UP * 0.1), run_time=self.rt(0.05))
        self.at("Keep one rule")
        everything = VGroup(b1, b1l, b2, b2l, hdr, band, ncl)
        self.play(FadeOut(everything), run_time=self.rt(0.04))
        equation = VGroup(chip("heat made + gained", HEAT, size=32),
                          T("=", 42, TEXT), chip("heat lost", HEAT, size=32)).arrange(RIGHT,buff=0.35).move_to([0,1,0])
        controller=VGroup(dial(0,-1),tag("controller",0,-2,30,SETP))
        self.at("Heat made and gained")
        self.play(FadeIn(equation),run_time=0.7)
        self.at("a controller decides")
        self.play(FadeIn(controller), run_time=0.4)
        self.play(Rotate(controller[0][1],angle=PI/3,about_point=controller[0][0].get_center()),run_time=0.4)
        self.finish()
