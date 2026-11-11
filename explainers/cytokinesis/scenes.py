"""The Band Before the Furrow — a single-world cytokinesis teaching film.

COLOR MAP
  BLUE    spindle microtubules and asters
  GREY    membrane/cortex and inactive RhoA
  AMBER   active RhoA and the active-RhoA band
  MAGENTA actin, formin, myosin II, and the contractile ring
  RED     blocked actin / eliminated answer
  TEXT    chromosomes, needle, questions
"""
import math
import numpy as np
from bp_style import *  # noqa: F401,F403

AMBER = "#F0B44D"
MAGENTA = "#E764A8"


def label(text, size=30, color=TEXT, **kw):
    return T(text, size=size, color=color, weight=MEDIUM, **kw)


def arrow(a, b, color=TEXT, width=5):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=width, tip_length=0.18)


def badge(n, p):
    c = Circle(0.24, color=TEXT, fill_color=TEXT, fill_opacity=1)
    return VGroup(c, T(str(n), 28, BG, weight=BOLD).move_to(c)).move_to(p)


def question_card(title="How does the surface know where to cut?", options=None):
    title_m = label(title, 31)
    rows = [title_m]
    if options:
        rows.append(VGroup(*[chip(x, color=GREY, size=28) for x in options]).arrange(RIGHT, buff=0.25))
    body = VGroup(*rows).arrange(DOWN, buff=0.15)
    box = RoundedRectangle(corner_radius=0.18, width=body.width + 0.5, height=body.height + 0.34,
                           color=TEXT, stroke_width=2, fill_color=BG, fill_opacity=0.93)
    return VGroup(box, body.move_to(box)).move_to([0, 3.18, 0])


def concept_key():
    return VGroup(Dot(radius=0.11, color=AMBER), label("active RhoA", 28, AMBER)).arrange(RIGHT, buff=0.13)


class CellRig:
    """Stable geometry for the film's one world; all changes are tracker driven."""

    def __init__(self, cx=-0.45, cy=-0.30, r=2.72, spindle_x=0, band_x=0,
                 dent_x=0, dent=0, band=0, ring=0, chrom_sep=1.05, daughters=0):
        V = ValueTracker
        self.cx, self.cy, self.r = cx, cy, r
        self.spindle_x = V(spindle_x)
        self.band_x = V(band_x)
        self.dent_x = V(dent_x)
        self.dent = V(dent)
        self.band_op = V(band)
        self.ring_op = V(ring)
        self.chrom_sep = V(chrom_sep)
        self.breathe = V(0)
        self.daughters = V(daughters)
        self.breathe.add_updater(lambda m, dt: m.increment_value(dt * 1.15))
        self.parts = Group(
            always_redraw(self._cell), always_redraw(self._off_dots), always_redraw(self._band),
            always_redraw(self._ring), always_redraw(self._spindle), always_redraw(self._chromosomes),
            self.breathe
        )

    def _surface_y(self, x):
        rr = self.r * (1 + 0.012 * math.sin(self.breathe.get_value()))
        base = math.sqrt(max(rr * rr - (x - self.cx) ** 2, 0.02))
        d = self.dent.get_value() * math.exp(-((x - (self.cx + self.dent_x.get_value())) / 0.48) ** 2)
        return max(0.12, base - d)

    def _cell(self):
        if self.daughters.get_value() > 0.01:
            q = self.daughters.get_value()
            breath = math.sin(self.breathe.get_value())
            rad = 2.0 + 0.14 * q + 0.022 * breath
            sep = 1.28 + 0.60 * q - 0.012 * breath
            left = Circle(rad, color=GREY, stroke_width=7, fill_color=GREY, fill_opacity=0.20).move_to([self.cx-sep, self.cy, 0])
            right = left.copy().move_to([self.cx+sep, self.cy, 0])
            bridge = Line([self.cx-sep+rad-0.12, self.cy, 0], [self.cx+sep-rad+0.12, self.cy, 0], color=GREY, stroke_width=12)
            return VGroup(left, right, bridge)
        xs = np.linspace(self.cx-self.r, self.cx+self.r, 150)
        ys = np.array([self._surface_y(x) for x in xs])
        pts = [np.array([x, self.cy+y, 0]) for x, y in zip(xs, ys)]
        pts += [np.array([x, self.cy-y, 0]) for x, y in zip(xs[::-1], ys[::-1])]
        return Polygon(*pts, color=GREY, stroke_width=7, fill_color=GREY, fill_opacity=0.20)

    def _off_dots(self):
        if self.daughters.get_value() > 0.01:
            return VGroup()
        out = VGroup()
        bx = self.cx + self.band_x.get_value()
        for x in np.linspace(self.cx-1.95, self.cx+1.95, 13):
            active = math.exp(-((x-bx)/0.47)**2) * self.band_op.get_value()
            col = interpolate_color(ManimColor(GREY), ManimColor(AMBER), active)
            for s in (-1, 1):
                out.add(Dot([x, self.cy+s*(self._surface_y(x)-0.16), 0], radius=0.065, color=col))
        return out

    def _arc(self, xc, half, color, width, opacity, inset=0.02):
        xs = np.linspace(max(self.cx-self.r+0.05, xc-half), min(self.cx+self.r-0.05, xc+half), 35)
        out = VGroup()
        for s in (-1, 1):
            m = VMobject().set_points_smoothly([np.array([x, self.cy+s*(self._surface_y(x)-inset), 0]) for x in xs])
            m.set_stroke(color, width=width, opacity=opacity)
            out.add(m)
        return out

    def _band(self):
        if self.daughters.get_value() > 0.01:
            return VGroup()
        return self._arc(self.cx+self.band_x.get_value(), 0.50, AMBER, 15, self.band_op.get_value(), 0.10)

    def _ring(self):
        if self.daughters.get_value() > 0.01:
            return VGroup()
        return self._arc(self.cx+self.dent_x.get_value(), 0.55, MAGENTA, 7, self.ring_op.get_value(), 0.27)

    def _spindle(self):
        sx = self.cx + self.spindle_x.get_value()
        if self.daughters.get_value() > 0.01:
            return VGroup(Line([self.cx-0.38, self.cy, 0], [self.cx+0.38, self.cy, 0], color=BLUE, stroke_width=7))
        poles = [np.array([sx-1.58, self.cy, 0]), np.array([sx+1.58, self.cy, 0])]
        g = VGroup()
        for y in (-0.28, -0.10, 0.10, 0.28):
            g.add(Line(poles[0], [sx-0.38, self.cy+y, 0], color=BLUE, stroke_width=4))
            g.add(Line([sx+0.38, self.cy+y, 0], poles[1], color=BLUE, stroke_width=4))
        for p in poles:
            g.add(Dot(p, radius=0.10, color=BLUE))
            for a in np.linspace(0, TAU, 12, endpoint=False):
                end = p + 0.68*np.array([math.cos(a), math.sin(a), 0])
                g.add(Line(p, end, color=BLUE, stroke_width=2.6, stroke_opacity=0.78))
        return g

    def _chromosomes(self):
        if self.daughters.get_value() > 0.01:
            return VGroup(
                self._cluster([self.cx-1.85, self.cy, 0], 0.78),
                self._cluster([self.cx+1.85, self.cy, 0], 0.78))
        sx = self.cx + self.spindle_x.get_value()
        sep = self.chrom_sep.get_value()
        return VGroup(self._cluster([sx-sep, self.cy, 0]), self._cluster([sx+sep, self.cy, 0]))

    @staticmethod
    def _cluster(p, scale=1):
        return VGroup(*[
            Line(np.array(p)+[-0.12, y-0.20, 0], np.array(p)+[0.12, y+0.20, 0], color=TEXT, stroke_width=5)
            for y in (-0.28, 0, 0.28)
        ]).scale(scale)


def add_rig(scene, rig):
    scene.add(rig.parts)


def ghost_option(n, text, y, kind):
    center = np.array([4.10, y, 0])
    cell = Ellipse(2.25, 1.28, color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.04)
    spindle = VGroup(Line([-0.62, 0, 0], [0.62, 0, 0], color=BLUE, stroke_width=4), Dot([-0.62,0,0], radius=.06,color=BLUE), Dot([.62,0,0], radius=.06,color=BLUE))
    action = VGroup()
    if kind == 1:
        action = VGroup(arrow([-0.72,.27,0],[-.12,.27,0],BLUE,3), arrow([.72,-.27,0],[.12,-.27,0],BLUE,3))
    elif kind == 2:
        action = Line([0,-.55,0],[0,.55,0],color=MAGENTA,stroke_width=9)
    else:
        action = VGroup(Line([0,-.58,0],[0,.58,0],color=AMBER,stroke_width=10), Line([.12,-.52,0],[.12,.52,0],color=MAGENTA,stroke_width=5))
    pic = VGroup(cell, spindle, action).move_to(center + DOWN*.12)
    txt = label(text, 28).next_to(pic, DOWN, buff=.10)
    return VGroup(badge(n, center+LEFT*1.45+UP*.23), pic, txt)


def options_column():
    return VGroup(ghost_option(1,"Spindle pulls surface",1.82,1), ghost_option(2,"Ring comes first",-.05,2), ghost_option(3,"Signal, then ring",-1.92,3))


def clock(pos=(5.55,2.65,0)):
    face = Circle(.34,color=TEXT,stroke_width=3)
    hand = Line(ORIGIN,UP*.24,color=TEXT,stroke_width=4)
    return VGroup(face, hand).move_to(pos)


def pathway(y=-3.40):
    a=chip("microtubules",BLUE,28); b=chip("RhoA band",AMBER,28); c=chip("furrow",GREY,28)
    g=VGroup(a,arrow(ORIGIN,RIGHT*.65,GREY),b,arrow(ORIGIN,RIGHT*.65,GREY),c).arrange(RIGHT,buff=.16).move_to([0,y,0])
    return g


class S00Hook(SpokenScene, TitleCard):
    LESSON = "Cytokinesis"
    TITLE = "The Band Before the Furrow"
    def construct(self):
        rig=CellRig(); add_rig(self,rig)
        name=label("sea urchin embryo cell",30).to_corner(UL,buff=.45)
        self.add(name)
        rig.breathe.add_updater(lambda m,dt: m.increment_value(dt*.55))
        self.play(rig.chrom_sep.animate.set_value(1.32),run_time=5.7,rate_func=linear)
        self.at("right between")
        mid=DashedLine([rig.cx,2.48,0],[rig.cx,-3.0,0],color=TEXT,dash_length=.15)
        self.play(Create(mid),run_time=.7); self.play(FadeOut(mid),run_time=.35)
        self.at("How does its surface")
        q=question_card()
        self.play(FadeIn(q,shift=DOWN*.12),run_time=.55)
        self.finish()


class S01Title(Scene):
    LESSON = "Cytokinesis"
    TITLE = "The Band Before the Furrow"
    def construct(self):
        rig=CellRig(chrom_sep=1.32); add_rig(self,rig)
        self.add(question_card())
        title=T(self.TITLE,50,font=TITLE_FONT).move_to([0,-2.62,0])
        rule=Line(LEFT*2,RIGHT*2,color=GOLD,stroke_width=4).next_to(title,DOWN,buff=.12)
        self.play(FadeIn(title,shift=UP*.12),GrowFromCenter(rule),rig.chrom_sep.animate.set_value(1.43),run_time=1.6)
        self.wait(.9)


class S02Inside(SpokenScene):
    def construct(self):
        rig=CellRig(chrom_sep=1.43); add_rig(self,rig)
        self.play(rig.breathe.animate.set_value(1),run_time=1.8,rate_func=there_and_back)
        surface=label("cell surface",30,GREY).move_to([4.45,1.65,0]); pointer=arrow([3.55,1.4,0],[2.15,1.75,0],GREY)
        self.play(FadeIn(surface),GrowArrow(pointer),run_time=.7)
        self.at("surface pinches in")
        fur=label("furrow",30,GREY).move_to([3.95,-1.9,0])
        self.play(rig.dent.animate.set_value(.48),FadeIn(fur),run_time=1.2)
        self.play(rig.dent.animate.set_value(0),FadeOut(fur),run_time=.75)
        self.at("sits deep inside")
        glow=SurroundingRectangle(rig.parts[4],color=BLUE,buff=.18,corner_radius=.25).set_stroke(opacity=.5,width=10)
        self.play(FadeOut(surface),FadeOut(pointer),FadeIn(glow),run_time=.7)
        self.at("It is the spindle")
        sp=label("spindle",30,BLUE).move_to([rig.cx,-1.25,0])
        self.play(FadeIn(sp),Indicate(rig.parts[4],color=BLUE),run_time=.9)
        self.at("star shaped aster")
        ast=label("aster",30,BLUE).move_to([-3.85,.95,0]); ap=arrow([-3.4,.75,0],[-2.25,.1,0],BLUE)
        self.play(FadeIn(ast),GrowArrow(ap),FadeOut(glow),rig.chrom_sep.animate.set_value(1.55),run_time=1.1)
        self.finish()


class S03Options(SpokenScene):
    def construct(self):
        rig=CellRig(cx=-3.55,r=1.55,chrom_sep=.66); add_rig(self,rig)
        head=label("Three possible answers",32).move_to([3.8,3.15,0]); self.play(FadeIn(head),run_time=.6)
        opts=options_column(); one,two,three=opts
        self.at("One")
        self.play(FadeIn(one,shift=LEFT*.25),run_time=1.0)
        self.play(Indicate(one[1],color=BLUE),run_time=1.5)
        self.at("Two")
        self.play(FadeIn(two,shift=LEFT*.25),run_time=1.0)
        self.play(Indicate(two[1],color=MAGENTA),run_time=1.5)
        self.at("Three")
        self.play(FadeIn(three,shift=LEFT*.25),run_time=1.0)
        self.at("signal marks the surface")
        self.play(Indicate(three[1],color=AMBER),run_time=1.7)
        self.play(Indicate(three[1],color=MAGENTA),run_time=1.6)
        self.finish()


class S04Switch(SpokenScene):
    def construct(self):
        rig=CellRig(cx=-3.55,r=1.55,chrom_sep=.66); add_rig(self,rig)
        opts=options_column()
        for option in opts:
            option[0].set_opacity(.22)
            option[1].set_opacity(.22)
            option[2].set_opacity(0)
        self.add(opts)
        panel=RoundedRectangle(width=5.2,height=3.7,corner_radius=.2,color=GREY,fill_color=BG,fill_opacity=.96).move_to([3.2,.35,0])
        rho=chip("RhoA",GREY,32).move_to([2.55,.45,0]); gdp=chip("GDP",GREY,28).move_to([4.45,.45,0]); off=label("OFF",28,GREY).move_to([3.5,-.45,0])
        self.play(FadeIn(panel),FadeIn(rho,shift=UP*.15),FadeIn(gdp),FadeIn(off),run_time=1.6)
        self.at("ROA is on")
        gtp=chip("GTP",AMBER,28).move_to(gdp); on=label("ON",28,AMBER).move_to(off)
        rho_on=chip("RhoA",AMBER,32).move_to(rho)
        self.play(Transform(rho,rho_on),Transform(gdp,gtp),Transform(off,on),run_time=1.0)
        self.at("off when it holds")
        self.play(Transform(rho,chip("RhoA",GREY,32).move_to(rho)),Transform(gdp,chip("GDP",GREY,28).move_to(gdp)),Transform(off,label("OFF",28,GREY).move_to(off)),run_time=.8)
        self.at("glowing probe")
        crescent=Arc(radius=.28,start_angle=-1.15,angle=2.3,color=GREEN,stroke_width=9)
        probe=VGroup(crescent,label("probe",28,GREEN).next_to(crescent,UP,buff=.10)).move_to([.65,1.6,0])
        self.play(FadeIn(probe),probe.animate.move_to([1.2,-1.1,0]),run_time=.9)
        self.play(Transform(rho,rho_on),Transform(gdp,gtp),Transform(off,on),probe.animate.move_to([2.55,1.45,0]),run_time=1.2)
        self.play(Indicate(rho,color=GREEN,scale_factor=1.12),run_time=1.0)
        self.finish()


class S05Watch(Scene):
    def construct(self):
        rig=CellRig(); add_rig(self,rig); c=clock(); self.add(c)
        self.play(rig.band_op.animate.set_value(1),Rotate(c[1],TAU,about_point=c[0].get_center()),run_time=3.5,rate_func=linear)


class S06Band(SpokenScene):
    def construct(self):
        rig=CellRig(band=1); add_rig(self,rig); c=clock(); self.add(c)
        self.play(Indicate(rig.parts[2],color=AMBER),run_time=1.7)
        self.at("shown here in amber")
        key=concept_key().move_to([4.75,2.0,0]); self.play(FadeIn(key),run_time=.65)
        self.at("One to four minutes later")
        line=Line([2.80,-2.92,0],[6.10,-2.92,0],color=GREY,stroke_width=5)
        bandtick=VGroup(Line([3.05,-3.16,0],[3.05,-2.68,0],color=AMBER,stroke_width=7),label("band",28,AMBER).move_to([3.05,-2.34,0]))
        gap=label("1–4 min",28).move_to([4.45,-3.35,0])
        furtick=VGroup(Line([5.85,-3.16,0],[5.85,-2.68,0],color=GREY,stroke_width=7),label("furrow",28,GREY).move_to([5.85,-2.34,0]))
        self.play(Create(line),FadeIn(bandtick),Rotate(c[1],TAU,about_point=c[0].get_center()),run_time=.9)
        self.play(FadeIn(gap),FadeIn(furtick),rig.dent.animate.set_value(.52),run_time=1.4)
        self.at("frog embryos")
        frog=VGroup(Ellipse(1.55,1.25,color=GREY,stroke_width=4),Line([0,-.56,0],[0,.56,0],color=AMBER,stroke_width=9),label("frog embryo",28).next_to(ORIGIN,DOWN,buff=.82)).move_to([4.65,-1.5,0])
        self.remove(line,bandtick,gap,furtick)
        self.play(FadeIn(frog),run_time=.7); self.play(Indicate(frog[1],color=AMBER),run_time=.8)
        self.at("mark comes before")
        self.remove(frog)
        order=VGroup(chip("band",AMBER,28),arrow(ORIGIN,RIGHT*.75,GREY),chip("furrow",GREY,28)).arrange(RIGHT,buff=.18).move_to([4.35,-2.85,0])
        self.play(FadeIn(order),run_time=.55)
        self.play(Indicate(order[0],color=AMBER),Indicate(order[2],color=GREY),run_time=1.0)
        self.finish()


class S07Actin(SpokenScene):
    def construct(self):
        rig=CellRig(); add_rig(self,rig); key=concept_key().move_to([4.75,2.65,0]); self.add(key)
        self.play(rig.ring_op.animate.set_value(.65),run_time=1.4)
        blocked=VGroup(label("actin blocked",30,RED),Line(LEFT*.9,RIGHT*.9,color=RED,stroke_width=8)).arrange(DOWN,buff=.12).move_to([4.35,.6,0])
        self.at("blocked actin assembly")
        self.play(FadeIn(blocked),Flash(rig.parts[3],color=RED),rig.ring_op.animate.set_value(0),run_time=1.1)
        self.at("amber band still formed")
        self.play(rig.band_op.animate.set_value(1),run_time=1.7)
        self.at("signal does not need")
        self.remove(blocked)
        self.play(Indicate(rig.parts[2],color=AMBER),run_time=1.2)
        self.at("Answer 2 is out")
        opt=ghost_option(2,"Ring comes first",-1.9,2); x=VGroup(Line(LEFT*.65+UP*.65,RIGHT*.65+DOWN*.65,color=RED,stroke_width=9),Line(LEFT*.65+DOWN*.65,RIGHT*.65+UP*.65,color=RED,stroke_width=9)).move_to(opt)
        self.play(FadeIn(opt),Create(x),run_time=.75); self.play(FadeOut(opt),FadeOut(x),run_time=.65)
        self.finish()


class S08Predict(SpokenScene):
    def construct(self):
        rig=CellRig(band=1,dent=.52); add_rig(self,rig); self.add(concept_key().move_to([4.75,2.65,0]))
        self.play(Indicate(rig.parts[0],color=GREY),run_time=1.3)
        self.at("blunt needle")
        needle=Line([-6.2,2.6,0],[-1.9,.65,0],color=TEXT,stroke_width=9).set_z_index(5)
        tip=Circle(.12,color=TEXT,fill_color=TEXT,fill_opacity=1).move_to(needle.get_end())
        self.play(Create(needle),FadeIn(tip),run_time=.75)
        self.play(rig.spindle_x.animate.set_value(1.05),rig.chrom_sep.animate.set_value(1.18),run_time=1.55)
        self.play(FadeOut(needle),FadeOut(tip),run_time=.45)
        self.at("What moves first")
        q=question_card("What moves first?",["furrow","amber band","nothing"])
        self.play(FadeIn(q,shift=DOWN*.1),run_time=.8)
        self.play(Indicate(q[1][1],color=TEXT),run_time=1.1)
        self.finish()


class S09Think(Scene):
    def construct(self):
        rig=CellRig(band=1,dent=.52,spindle_x=1.05,chrom_sep=1.18); add_rig(self,rig)
        q=question_card("What moves first?",["furrow","amber band","nothing"]); self.add(q)
        pulse=Dot([rig.cx-rig.r+.12,rig.cy,0],radius=.11,color=TEXT).set_opacity(.75)
        self.add(pulse)
        self.play(pulse.animate.move_to([rig.cx+rig.r-.12,rig.cy,0]),rig.breathe.animate.set_value(1),run_time=2.25,rate_func=linear)
        self.play(pulse.animate.move_to([rig.cx-rig.r+.12,rig.cy,0]),rig.breathe.animate.set_value(0),run_time=2.25,rate_func=linear)


class S10Reveal(SpokenScene):
    def construct(self):
        rig=CellRig(band=1,dent=.52,spindle_x=1.05,chrom_sep=1.18); add_rig(self,rig)
        q=question_card("What moves first?",["furrow","amber band","nothing"]); self.add(q)
        schem=label("schematic",28,GREY).to_corner(DR,buff=.45)
        self.play(FadeOut(q),FadeIn(schem),run_time=.65)
        self.at("active row A gathers")
        self.play(rig.band_op.animate.set_value(0),run_time=.8)
        rig.band_x.set_value(1.05)
        self.play(rig.band_op.animate.set_value(1),run_time=2.2)
        self.at("Only then")
        self.play(rig.dent.animate.set_value(0),run_time=.65); rig.dent_x.set_value(1.05)
        self.play(rig.dent.animate.set_value(.52),run_time=1.35)
        self.at("band leads")
        lead=VGroup(chip("band",AMBER,30),arrow(ORIGIN,RIGHT*.8,GREY),chip("furrow",GREY,30)).arrange(RIGHT,buff=.2).move_to([0,-3.43,0])
        self.play(FadeIn(lead),run_time=.75); self.play(Indicate(lead[0],color=AMBER),Indicate(lead[2],color=GREY),run_time=1.05)
        self.at("argues against")
        bad=ghost_option(1,"Spindle pulls surface",2.15,1).scale(.86).set_opacity(.65)
        self.play(FadeIn(bad),run_time=.5); self.play(FadeOut(bad),run_time=.7)
        self.at("answer three")
        good=ghost_option(3,"Signal, then ring",2.05,3).scale(.86)
        self.play(FadeIn(good),Indicate(good,color=AMBER),run_time=.9)
        self.finish()


class S11Idea(SpokenScene):
    def construct(self):
        rig=CellRig(spindle_x=1.05,band_x=1.05,dent_x=1.05,band=1,dent=.52,chrom_sep=1.18); add_rig(self,rig)
        rule=label("Microtubules place the RhoA band; the furrow follows.",34).move_to([0,3.15,0])
        self.play(FadeIn(rule),run_time=1.1)
        p=pathway(-3.43); self.at("anaphase microtubules")
        self.play(FadeIn(p[0]),run_time=.75)
        self.play(GrowArrow(p[1]),FadeIn(p[2]),run_time=.9)
        self.play(GrowArrow(p[3]),FadeIn(p[4]),run_time=.9)
        self.at("Move the microtubules")
        self.play(rig.spindle_x.animate.set_value(.25),run_time=1.3)
        self.at("band moves first")
        self.play(rig.band_op.animate.set_value(0),run_time=.35); rig.band_x.set_value(.25)
        self.play(rig.band_op.animate.set_value(1),run_time=.85)
        self.at("furrow follows")
        self.play(rig.dent.animate.set_value(0),run_time=.3); rig.dent_x.set_value(.25)
        self.play(rig.dent.animate.set_value(.52),run_time=.75)
        self.finish()


class S12Ring(SpokenScene):
    def construct(self):
        membrane=Arc(radius=3.55,start_angle=.32,angle=2.50,color=GREY,stroke_width=12).move_to([0,-2.35,0])
        shimmer=ValueTracker(0)
        shimmer.add_updater(lambda m,dt:m.increment_value(dt*2.1))
        band=always_redraw(lambda: Arc(radius=3.34,start_angle=.95,angle=1.25,color=AMBER,
                                        stroke_width=17+2.2*math.sin(shimmer.get_value())).move_to([0,-2.35,0]))
        particles=VGroup(*[Dot(radius=.12,color=AMBER) for _ in range(13)])
        def drift_particles(group):
            for i,dot in enumerate(group):
                a=.95+((i/13+.22*shimmer.get_value())%1)*1.25
                dot.move_to([3.34*math.cos(a),-2.35+3.34*math.sin(a),0])
        particles.add_updater(drift_particles)
        self.add(membrane,band,particles,shimmer)
        self.play(Indicate(band,color=AMBER),run_time=1.0)
        self.at("turns on formans")
        formin=chip("formin",MAGENTA,30).move_to([-2.75,.6,0]); myosin=chip("myosin II",MAGENTA,30).move_to([2.75,.6,0])
        self.play(FadeIn(formin),FadeIn(myosin),run_time=1.25)
        self.at("Formans build")
        self.remove(formin,myosin)
        f1=VGroup(Line([-2.3,.15,0],[1.5,-.75,0],color=MAGENTA,stroke_width=5),*[Dot([-2.3+i*.42,.15-i*.10,0],radius=.09,color=MAGENTA) for i in range(10)])
        f2=VGroup(Line([2.3,-.15,0],[-1.5,-1.05,0],color=MAGENTA,stroke_width=5),*[Dot([2.3-i*.42,-.15-i*.10,0],radius=.09,color=MAGENTA) for i in range(10)])
        self.play(Create(f1),Create(f2),run_time=2.25)
        self.at("Myosin 2")
        myosin=chip("myosin II",MAGENTA,30).move_to([2.75,.6,0]); self.add(myosin)
        motor=VGroup(Circle(.18,color=MAGENTA,fill_color=MAGENTA,fill_opacity=1),Line(LEFT*.45,RIGHT*.45,color=MAGENTA,stroke_width=7)).move_to([0,-.48,0])
        self.play(Transform(myosin,motor),run_time=.65)
        self.at("pulls those filaments")
        self.play(f1.animate.shift(RIGHT*.72),f2.animate.shift(LEFT*.72),run_time=1.8)
        self.at("result is a ring")
        self.remove(membrane,band,particles,formin,myosin,f1,f2)
        rig=CellRig(band=1,ring=0,dent=.25); add_rig(self,rig)
        self.play(rig.ring_op.animate.set_value(1),run_time=.75)
        self.at("drawstring")
        word=label("drawstring",30,MAGENTA).move_to([4.7,-2.15,0]); self.play(FadeIn(word),rig.dent.animate.set_value(.95),run_time=1.0)
        self.play(FadeOut(word),run_time=.35)
        self.finish()


class S13Close(Scene):
    def construct(self):
        rig=CellRig(band=1,ring=1,dent=.95); add_rig(self,rig)
        self.play(rig.dent.animate.set_value(2.45),run_time=1.65)
        self.play(rig.daughters.animate.set_value(1),rig.ring_op.animate.set_value(0),rig.band_op.animate.set_value(0),run_time=1.35)


class S14Return(SpokenScene):
    def construct(self):
        rig=CellRig(daughters=1); add_rig(self,rig)
        rig.breathe.add_updater(lambda m,dt:m.increment_value(dt*.32))
        bridge=label("bridge",30,GREY).move_to([0,1.55,0]); bp=arrow([0,1.22,0],[0,.12,0],GREY)
        self.play(FadeIn(bridge),GrowArrow(bp),run_time=1.5)
        self.at("separate job")
        self.play(Indicate(rig.parts[0],color=GREY),run_time=1.0)
        self.at("One question stays open")
        self.remove(bridge,bp)
        q=question_card("Microtubules inside, RhoA at membrane: how?")
        dots=DashedLine([0,.05,0],[2.15,1.35,0],color=BLUE,dash_length=.13); qm=label("?",40).move_to([1.18,.83,0])
        self.play(FadeIn(q),Create(dots),FadeIn(qm),run_time=1.3)
        self.play(Wiggle(qm),run_time=1.0)
        self.at("settled earlier")
        self.remove(q,dots,qm)
        flash=Line([0,-.33,0],[0,.33,0],color=AMBER,stroke_width=18).set_opacity(.75)
        self.play(FadeIn(flash),run_time=.3); self.play(FadeOut(flash),run_time=.35)
        p=pathway(); self.play(FadeIn(p[0]),run_time=.5); self.play(GrowArrow(p[1]),FadeIn(p[2]),run_time=.55); self.play(GrowArrow(p[3]),FadeIn(p[4]),run_time=.55)
        self.finish()


class S15End(EndCard):
    LINE = "Microtubules place the RhoA band; the furrow follows."
    def construct(self):
        rig=CellRig(cy=-1.85,daughters=1); rig.parts.set_opacity(.25); add_rig(self,rig)
        line=label(self.LINE,40).move_to([0,1.55,0]); sub=label("biochemistrypedia.com",28,TEAL).move_to([0,.72,0])
        self.play(FadeIn(line,shift=UP*.12),FadeIn(sub),run_time=1.0)
        bridge=Line([-.38,-1.85,0],[.38,-1.85,0],color=GREY,stroke_width=12).set_opacity(.5)
        self.play(Indicate(bridge,color=GREY),run_time=.8)
        self.finish()
