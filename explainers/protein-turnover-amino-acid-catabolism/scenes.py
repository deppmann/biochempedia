"""Choose, Recycle, Split — Biochemistrypedia teaching film.

COLOR MAP (one meaning throughout)
  BLUE   carbon skeletons, proteins, and the main material stream
  YELLOW ubiquitin, ATP/energy, and nitrogen tokens
  GREEN  reuse, safe urea, and productive destinations
  RED    toxicity, danger, and rejected choices
  GREY   machinery, lanes, and de-emphasized structure

Everything is a schematic mechanical cartoon.  No molecular structures are drawn.
"""
import math

import numpy as np
from bp_style import *  # noqa: F401,F403


def pt(x, y):
    return np.array([x, y, 0.0])


def heading(text, size=38):
    return fit(T(text, size=size, font=TITLE_FONT), max_w=12.0).to_edge(UP, buff=0.32)


def arr(a, b, color=GREY, width=4, buff=0.08):
    return Arrow(a, b, buff=buff, color=color, stroke_width=width, tip_length=0.22)


def protein(label="one protein", n=7, scale=1.0):
    blocks = VGroup(*[
        RoundedRectangle(corner_radius=0.13, width=0.62, height=0.68,
                         stroke_color=BLUE, stroke_width=3,
                         fill_color=BLUE, fill_opacity=0.22)
        for _ in range(n)
    ]).arrange(RIGHT, buff=0.08)
    blocks.set_y(-0.82)
    blocks.scale(scale)
    lab = T(label, 28, BLUE, weight=BOLD).next_to(blocks, UP, buff=0.18)
    return VGroup(blocks, lab)


def badge(text="", radius=0.22):
    c = Circle(radius=radius, color=YELLOW, stroke_width=3,
               fill_color=YELLOW, fill_opacity=0.35)
    return VGroup(c, T(text, 22, YELLOW, weight=BOLD).move_to(c)) if text else c


def atp_token():
    return chip("ATP", YELLOW, 28, pad=0.16, fill_opacity=0.22)


def conveyor(y=-1.58, x1=-6.25, x2=6.25, color=GREY):
    top = Line(pt(x1, y + 0.23), pt(x2, y + 0.23), color=color, stroke_width=4)
    bot = Line(pt(x1, y - 0.23), pt(x2, y - 0.23), color=color, stroke_width=4)
    rollers = VGroup(*[
        VGroup(Circle(radius=0.17, color=color, stroke_width=2),
               Line(LEFT * 0.13, RIGHT * 0.13, color=color, stroke_width=2)).move_to(pt(x, y))
        for x in np.linspace(x1 + 0.3, x2 - 0.3, 16)
    ])
    return VGroup(top, bot, rollers)


def gate(x=1.9, y=-0.55, scale=1.0):
    posts = VGroup(
        RoundedRectangle(corner_radius=0.13, width=0.4, height=2.65,
                         stroke_color=GREY, fill_color=GREY, fill_opacity=0.14),
        RoundedRectangle(corner_radius=0.13, width=0.4, height=2.65,
                         stroke_color=GREY, fill_color=GREY, fill_opacity=0.14),
    )
    posts[0].move_to(pt(x - 0.8, y)); posts[1].move_to(pt(x + 0.8, y))
    bar = Line(pt(x - 0.62, y + 0.82), pt(x + 0.62, y - 0.35),
               color=YELLOW, stroke_width=9)
    geometry = VGroup(posts, bar).scale(scale, about_point=pt(x, y))
    label = T("sorting gate", 28, TEXT).next_to(geometry, UP, buff=.18)
    return VGroup(*geometry, label)


def proteasome(center=pt(2.9, -0.45), scale=1.0):
    cap = RoundedRectangle(corner_radius=0.35, width=2.0, height=1.25,
                           stroke_color=YELLOW, stroke_width=4,
                           fill_color=YELLOW, fill_opacity=0.12)
    core = RoundedRectangle(corner_radius=0.25, width=2.35, height=2.45,
                            stroke_color=BLUE, stroke_width=4,
                            fill_color=BLUE, fill_opacity=0.10)
    cap.move_to(UP * 1.38); core.move_to(DOWN * 0.48)
    geometry = VGroup(core, cap).scale(scale)
    cap_text = "regulatory cap" if scale >= .8 else "cap"
    lab1 = T(cap_text, 28, YELLOW).move_to(cap.get_center() + UP * .28 * scale)
    lab2 = T("core", 28, BLUE, weight=BOLD).move_to(core.get_center())
    gears = VGroup(*[
        Circle(radius=0.13 * scale, color=YELLOW, stroke_width=3)
        .move_to(pt((-0.35 + i * .35) * scale, .82 * scale))
        for i in range(3)
    ])
    return VGroup(geometry[0], geometry[1], lab1, lab2, gears).move_to(center)


def scope_label():
    return chip("adult · nitrogen balance", GREY, 28, pad=0.16).to_edge(UP, buff=0.68)


def factory_backdrop(scene):
    """The same large, quiet recycling-room shell behind every close view."""
    room = RoundedRectangle(corner_radius=.32, width=13.25, height=6.75,
                            stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=.045).move_to(DOWN*.08)
    beams = VGroup(*[
        Line(pt(x,-3.25), pt(x,3.15), color=GREY, stroke_width=2).set_opacity(.17)
        for x in [-5.2, -3.45, -1.72, 0, 1.72, 3.45, 5.2]
    ])
    grid = VGroup(*[
        Line(pt(-6.35,y), pt(6.35,y), color=GREY, stroke_width=2).set_opacity(.13)
        for y in [-2.25, -1.1, .05, 1.2, 2.35]
    ])
    floor = VGroup(*[
        Line(pt(-6.35,-2.95+i*.18),pt(6.35,-2.95+i*.18),color=GREY,stroke_width=2).set_opacity(.16)
        for i in range(3)
    ])
    # Solid machinery bays occupy a minority of the image, so the room reads as a
    # working place rather than an empty outline while the dark ground stays dominant.
    bays = VGroup(
        RoundedRectangle(corner_radius=.18,width=1.05,height=5.55,stroke_width=0,
                         fill_color=GREY,fill_opacity=.22).move_to(pt(-5.75,-.05)),
        RoundedRectangle(corner_radius=.18,width=1.05,height=5.55,stroke_width=0,
                         fill_color=GREY,fill_opacity=.22).move_to(pt(5.75,-.05)),
        RoundedRectangle(corner_radius=.12,width=10.35,height=.72,stroke_width=0,
                         fill_color=GREY,fill_opacity=.22).move_to(pt(0,-2.62)),
    )
    shell = VGroup(room, bays, beams, grid, floor).set_z_index(-8)
    scene.add(shell)
    return shell


def moving_dots(scene, a, b, color, n=6, speed=0.10, radius=0.08, z=-1):
    """Continuously moving material on a straight lane."""
    phase = ValueTracker(0)
    driver = Mobject()
    driver.add_updater(lambda m, dt: phase.increment_value(speed * dt))
    dots = VGroup(*[Dot(radius=radius, color=color) for _ in range(n)])
    av, bv = np.array(a), np.array(b)
    for i, d in enumerate(dots):
        d.add_updater(lambda m, i=i: m.move_to(av + (((phase.get_value() + i / n) % 1.0)) * (bv - av)))
    dots.set_z_index(z)
    scene.add(driver, dots)
    return Group(driver, dots)


class S00Hook(TitleCard):
    """The spoken hook doubles as the compact title card required for the opening scene."""
    LESSON = "Protein turnover and amino acid catabolism"
    TITLE = "Choose, Recycle, Split"
    _words = SpokenScene._words
    t_of = SpokenScene.t_of
    at = SpokenScene.at

    def construct(self):
        factory_backdrop(self)
        conv = conveyor()
        g = gate(2.65, -0.52)
        p = protein().move_to(pt(-3.3, -0.55))
        schematic = T("schematic", 24, GREY).to_corner(DR, buff=0.3)
        self.add(conv, schematic)
        moving_dots(self, pt(-6.1, -1.58), pt(6.1, -1.58), BLUE, 12, .08, .055)
        self.play(FadeIn(p, shift=RIGHT * .3), run_time=.7)
        self.at("dismantles roughly")
        counter = M("roughly 250 g/day", 40, TEXT).move_to(pt(-2.4, 2.45))
        self.play(FadeIn(counter, shift=UP * .15), p.animate.shift(RIGHT * .5), run_time=1.0)
        ghosts = VGroup(*[protein("", 5, .45).set_opacity(.22).move_to(pt(-5.2 + i * 1.2, .55)) for i in range(5)])
        self.play(LaggedStart(*[FadeIn(x, shift=RIGHT * .35) for x in ghosts], lag_ratio=.12), run_time=1.2)
        self.at("Why spend")
        self.play(Create(g), p.animate.move_to(pt(.05, -.55)), run_time=1.2)
        token = atp_token().move_to(pt(2.65, 1.45))
        q = T("?", 76, YELLOW, font=TITLE_FONT).move_to(pt(4.55, 1.35))
        self.play(FadeIn(token, scale=.7), FadeIn(q, shift=UP * .3), run_time=.8)
        self.play(MoveAlongPath(token, Arc(radius=1.0, start_angle=PI, angle=TAU).move_arc_center_to(pt(2.65, .4))), run_time=1.4)
        self.at("Follow one protein")
        title = T(self.TITLE, 48, TEXT, font=TITLE_FONT).to_edge(UP, buff=.28).shift(DOWN*.12)
        self.remove(counter, ghosts)
        self.play(Write(title), p.animate.shift(RIGHT * .55), run_time=1.1)
        self.at("selection matters")
        self.play(Indicate(g, color=YELLOW, scale_factor=1.03), run_time=.8)
        self.finish()


class S01Turnover(SpokenScene):
    def construct(self):
        factory_backdrop(self)
        conv, g = conveyor(), gate(2.65, -.52)
        p = protein().move_to(pt(-3.45, -.55))
        self.add(conv, g, p, T("schematic", 24, GREY).to_corner(DR, buff=.3))
        moving_dots(self, pt(-6.1, -1.58), pt(6.1, -1.58), BLUE, 12, .08, .055)
        self.at("different expiration dates")
        clocks = VGroup()
        for x, lab in zip([-3.8, -1.2, 1.0], ["minutes", "months", "lifetime"]):
            c = Circle(radius=.68, color=TEXT, stroke_width=3).move_to(pt(x, 1.55))
            hand = Line(c.get_center(), c.get_center() + UP * .46, color=YELLOW, stroke_width=4)
            grp = VGroup(c, hand, T(lab, 28, TEXT).next_to(c, DOWN, buff=.14))
            clocks.add(grp)
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN*.15) for c in clocks], lag_ratio=.2), p.animate.shift(RIGHT*.55), run_time=1.4)
        for i, rate in enumerate([2.2, .8, .25]):
            clocks[i][1].add_updater(lambda m, dt, r=rate: m.rotate(-r*dt, about_point=m.get_start()))
        self.at("Turnover removes")
        damaged = protein("damaged", 5, .75).move_to(pt(-2.9, -.45))
        damaged[0][2].shift(DOWN*.22).set_color(RED)
        self.play(FadeOut(clocks), Transform(p, damaged), run_time=.9)
        self.play(p.animate.move_to(pt(1.25, -.45)), run_time=1.0)
        self.at("changes signals")
        lamp = VGroup(Circle(radius=.38, color=GREEN, fill_color=GREEN, fill_opacity=.65), T("signal", 28, GREEN).next_to(ORIGIN, DOWN, buff=.52)).move_to(pt(-2.6, 1.25))
        self.play(FadeIn(lamp), run_time=.5)
        self.play(lamp[0].animate.set_fill(opacity=.05).set_stroke(GREY), run_time=.7)
        self.at("hydrolysis is downhill")
        ramp = Line(pt(-4.7, .35), pt(-1.15, -1.0), color=BLUE, stroke_width=7)
        rlab = T("peptide-bond hydrolysis", 28, BLUE).next_to(ramp, UP, buff=.2)
        self.play(FadeOut(lamp), Create(ramp), FadeIn(rlab), run_time=1.0)
        self.at("What is")
        tok = atp_token().move_to(pt(-3.0, 1.55)); q=T("?", 72, YELLOW).move_to(pt(4.65, 1.2))
        self.play(FadeIn(tok), FadeIn(q, shift=UP*.2), run_time=.7)
        self.play(tok.animate.shift(RIGHT*.45), rate_func=there_and_back, run_time=1.2)
        self.finish()


class S02Choose(SpokenScene):
    def construct(self):
        factory_backdrop(self)
        g = gate(3.9, -.45)
        p = protein().move_to(pt(-3.65, -.55))
        exits = VGroup(T("reuse", 28, GREEN).move_to(pt(4.9, 1.5)), T("burn", 28, RED).move_to(pt(5.05, -2.35)))
        self.add(g, p, exits, T("schematic", 24, GREY).to_corner(DR,buff=.3))
        self.at("Ubiquitin is")
        ub = badge().move_to(pt(-1.5, .25))
        self.play(FadeIn(ub, scale=.5), run_time=.45)
        ulab = T("ubiquitin", 28, YELLOW).next_to(ub, UP, buff=.18)
        self.play(FadeIn(ulab), run_time=.55)
        self.at("E1 spends")
        e1 = chip("E1 activation", BLUE, 28).move_to(pt(-3.0, 1.7)); atp=atp_token().next_to(e1, LEFT, buff=.3)
        self.play(FadeIn(e1), FadeIn(atp), run_time=.7)
        products = VGroup(chip("AMP", GREY, 28), chip("PPi", GREY, 28)).arrange(RIGHT,buff=.15).move_to(pt(-4.65,2.5))
        self.play(Transform(atp, products), ub.animate.set_fill(YELLOW, opacity=.8), run_time=.8)
        self.at("E2 carries")
        e2 = chip("E2 cart", BLUE, 28).move_to(pt(-1.4, 1.7))
        self.remove(ulab, e1, atp)
        self.play(FadeIn(e2), ub.animate.next_to(e2, DOWN, buff=.18), run_time=.8)
        self.play(VGroup(e2,ub).animate.shift(RIGHT*2.25), run_time=.9)
        self.at("E3 ligase recognizes")
        e3 = Arc(radius=.72,start_angle=-PI/2,angle=PI,color=BLUE,stroke_width=9).move_to(pt(1.75,.1))
        e3_lab = T("E3",28,BLUE,weight=BOLD).next_to(e3, RIGHT, buff=.32)
        notch = Triangle(color=BLUE, fill_color=BLUE, fill_opacity=.25).scale(.22).move_to(p[0].get_right()+LEFT*.5+UP*.36)
        self.play(FadeIn(notch), FadeIn(e3), FadeIn(e3_lab), run_time=.65)
        self.play(FadeOut(e3_lab), e3.animate.move_to(notch.get_center()+UP*.15),
                  ub.animate.move_to(notch.get_center()+UP*.48), run_time=.8)
        self.at("Hundreds of")
        fan = VGroup(*[
            Arc(radius=.28,start_angle=-PI/2,angle=PI,color=BLUE,stroke_width=5)
            .move_to(pt(-.4+i*.55,2.55)) for i in range(7)
        ])
        self.play(FadeIn(fan), FadeOut(e2), run_time=.7)
        self.at("classic lysine")
        chain = VGroup(*[badge("",.19).move_to(pt(.55+i*.43,.35+i*.16)) for i in range(4)], T("K48",26,YELLOW).move_to(pt(1.35,1.05)))
        self.play(FadeOut(ub), FadeOut(e3), FadeIn(chain), run_time=.7)
        self.at("toward the proteasome")
        pm = proteasome(pt(5.15,-.2),.65)
        self.play(FadeOut(fan), FadeOut(g), FadeOut(exits), FadeIn(pm),
                  p.animate.move_to(pt(2.25,-.55)), chain.animate.shift(RIGHT*1.35), run_time=1.1)
        self.finish()


def prediction_layout(scene, animate=True):
    pm=proteasome(pt(4.65,-.45),.82)
    p=protein("tagged protein",6,.8).move_to(pt(-2.9,-1.0))
    tags=VGroup(*[badge("",.15).move_to(pt(-1.95+i*.3,-.48+i*.1)) for i in range(4)])
    a=chip("cut bonds?", RED, 30).move_to(pt(-3.1,1.35))
    b=chip("something else?", YELLOW,30).move_to(pt(.55,1.35))
    q=T("Where does ATP energy go?",40,TEXT,font=TITLE_FONT).to_edge(UP,buff=.28)
    tok=atp_token().move_to(pt(-1.35,.35))
    conv=conveyor(-1.85)
    scene.add(conv, pm, p, tags, a, b, q, tok, T("schematic",24,GREY).to_corner(DR,buff=.3))
    moving_dots(scene,pt(-6.1,-1.85),pt(3.4,-1.85),BLUE,10,.07,.05)
    return pm,p,tags,a,b,q,tok


class S03Predict(SpokenScene):
    def construct(self):
        factory_backdrop(self)
        pm,p,tags,a,b,q,tok=prediction_layout(self)
        self.remove(a,b,q,tok)
        self.at("Predict where")
        self.play(FadeIn(q), p.animate.shift(RIGHT*.35), run_time=.6)
        self.at("peptide bond cutting")
        self.play(FadeIn(a,shift=UP*.15), p.animate.shift(RIGHT*.35), run_time=.7)
        self.at("something else")
        self.play(FadeIn(b,shift=UP*.15), FadeIn(tok), run_time=.7)
        self.play(tok.animate.move_to(a.get_bottom()+DOWN*.4), rate_func=there_and_back, run_time=1.2)
        self.at("Hold your answer")
        self.play(tok.animate.move_to(b.get_bottom()+DOWN*.4), p.animate.shift(RIGHT*.55), run_time=1.4)
        self.finish()


class S04Think(Scene):
    def construct(self):
        factory_backdrop(self)
        pm,p,tags,a,b,q,tok=prediction_layout(self)
        timer=Circle(radius=.48,color=YELLOW,stroke_opacity=.25).move_to(pt(2.55,1.25))
        arc=Arc(radius=.48,start_angle=PI/2,angle=-TAU,color=YELLOW,stroke_width=6).move_to(timer)
        self.add(timer)
        self.play(Create(arc), tok.animate.move_to(a.get_bottom()+DOWN*.4), p.animate.shift(RIGHT*.25), run_time=2.15, rate_func=linear)
        self.play(tok.animate.move_to(b.get_bottom()+DOWN*.4), p.animate.shift(RIGHT*.2), run_time=2.15, rate_func=linear)
        self.wait(.2)


class S05Answer(SpokenScene):
    def construct(self):
        factory_backdrop(self)
        pm=proteasome(pt(2.9,-.25),1.05)
        p=protein("tagged protein",7,.82).move_to(pt(-3.8,-.65))
        tags=VGroup(*[badge("",.16).move_to(pt(-2.85+i*.31,-.1+i*.1)) for i in range(4)])
        cut=chip("cut bonds?",RED,28).move_to(pt(-3.8,2.35)); tok=atp_token().move_to(pt(-1.55,1.55))
        ramp=Line(pt(-4.9,-2.65),pt(-2.2,-3.15),color=BLUE,stroke_width=6)
        self.add(pm,p,tags,cut,tok,ramp,T("hydrolysis: downhill",26,BLUE).next_to(ramp,UP,buff=.12),T("schematic",24,GREY).to_corner(DR,buff=.3))
        self.at("Not to cutting")
        cross=T("×",52,RED,weight=BOLD).next_to(cut,RIGHT,buff=.25)
        self.play(FadeIn(cross), tok.animate.shift(RIGHT*.15), run_time=.7)
        self.at("regulatory cap recognizes")
        self.play(FadeOut(cut),FadeOut(cross),p.animate.move_to(pt(-1.15,-.35)),tags.animate.shift(RIGHT*2.55),run_time=1.1)
        self.play(Indicate(pm[1],color=YELLOW,scale_factor=1.05),run_time=.55)
        self.at("uses a TP")
        self.play(tok.animate.move_to(pm[1].get_top()+UP*.4),run_time=.65)
        self.at("unfold and thread")
        strand=VGroup(*[RoundedRectangle(corner_radius=.1,width=.42,height=.48,stroke_color=BLUE,fill_color=BLUE,fill_opacity=.25).move_to(pt(-1.25+i*.48,-.2)) for i in range(7)])
        self.play(Transform(p[0],strand),FadeOut(p[1]),run_time=1.0)
        self.play(p[0].animate.shift(RIGHT*2.45),run_time=1.1)
        self.at("core cuts")
        peps=VGroup(*[chip("peptide",BLUE,28,pad=.12).move_to(pt(4.8,-1.35+i*.66)) for i in range(3)])
        self.play(FadeOut(p[0]),LaggedStart(*[FadeIn(x,shift=RIGHT*.3) for x in peps],lag_ratio=.25),run_time=1.1)
        no=chip("no ATP",GREEN,28).move_to(pt(4.9,1.4))
        self.play(FadeIn(no),run_time=.5)
        self.at("Dubiquitinases recover")
        arm=arr(pt(1.75,.75),pt(-.1,1.9),YELLOW,4)
        self.play(GrowArrow(arm),tags.animate.move_to(pt(-.4,2.0)),run_time=.9)
        self.at("Energy buys choice")
        choose=VGroup(Circle(radius=.7,color=YELLOW,stroke_width=7),T("choose",28,YELLOW)).move_to(pt(-2.3,.75))
        handle=VGroup(Circle(radius=.7,color=YELLOW,stroke_width=7),T("handle",28,YELLOW)).move_to(pt(-.55,.75))
        self.play(FadeOut(tags),FadeOut(arm),Transform(tok,choose),FadeIn(handle),run_time=.9)
        self.at("not favorable")
        self.play(Indicate(ramp,color=BLUE,scale_factor=1.03),run_time=.7)
        self.finish()


class S06Recycle(SpokenScene):
    def construct(self):
        factory_backdrop(self)
        pm=proteasome(pt(-4.8,.3),.68)
        pool=Circle(radius=1.55,color=BLUE,stroke_width=5,fill_color=BLUE,fill_opacity=.08).move_to(pt(-.5,-.25))
        plab=T("amino acids",36,BLUE,weight=BOLD).move_to(pool)
        reuse=Arc(radius=2.35,start_angle=-PI*.3,angle=PI*1.55,color=GREEN,stroke_width=8).move_arc_center_to(pt(.1,-.15)); reuse.add_tip(tip_length=.25)
        burn=arr(pt(1.0,-.85),pt(5.55,-2.2),RED,7)
        self.add(pm,scope_label(),T("schematic",24,GREY).to_corner(DR,buff=.3))
        self.at("Peptidases release")
        peps=VGroup(*[chip("peptide",BLUE,28,pad=.1).move_to(pt(-3.15,-.9+i*.7)) for i in range(3)])
        station=chip("peptidases",GREY,28).move_to(pt(-2.35,1.65))
        self.play(FadeIn(peps),FadeIn(station),run_time=.7)
        tiles=VGroup(*[RoundedRectangle(corner_radius=.08,width=.42,height=.42,stroke_color=BLUE,fill_color=BLUE,fill_opacity=.28).move_to(pt(-2.8+i*.5,-.25)) for i in range(7)])
        self.play(Transform(peps,tiles),run_time=.9)
        self.at("shared pool")
        self.play(Create(pool),FadeIn(plab),FadeOut(peps),run_time=1.0)
        pool.add_updater(lambda m,dt:m.rotate(.12*dt))
        pool_tiles=VGroup(*[Dot(radius=.10,color=BLUE).move_to(pool.point_at_angle(i*TAU/9)) for i in range(9)])
        pool_tiles.add_updater(lambda m,dt:m.rotate(.35*dt,about_point=pool.get_center()))
        self.add(pool_tiles)
        self.at("most return")
        self.play(Create(reuse),run_time=.9)
        moving_dots(self,pt(.2,1.8),pt(4.7,1.55),GREEN,7,.08,.09)
        newp=protein("new protein",6,.72).move_to(pt(4.6,1.75))
        self.play(FadeIn(newp,shift=RIGHT*.2),run_time=.8)
        self.at("surplus is burned")
        self.play(GrowArrow(burn),run_time=.8)
        moving_dots(self,pt(1.0,-.85),pt(5.55,-2.2),RED,4,.07,.09)
        self.at("cell selects proteins")
        g=gate(-5.45,-.35,.55)
        self.play(FadeOut(station),pm.animate.move_to(pt(-3.8,.15)),FadeIn(g),run_time=.7)
        self.play(Indicate(pm,color=YELLOW),run_time=.45)
        self.at("reuses most")
        self.play(Indicate(reuse,color=GREEN,scale_factor=1.02),run_time=.7)
        self.at("separates surplus")
        fork=T("Y",64,RED,weight=BOLD).rotate(PI).move_to(pt(4.95,-2.05))
        self.play(FadeIn(fork),run_time=.7)
        self.finish()


class S07Split(SpokenScene):
    def construct(self):
        factory_backdrop(self)
        aa=chip("burned amino acid",BLUE,34).move_to(pt(-4.6,.15))
        fork=VGroup(Line(pt(-2.55,.1),pt(-1.2,1.75),color=GREY,stroke_width=7),Line(pt(-2.55,.1),pt(-1.2,-1.75),color=GREY,stroke_width=7))
        n=chip("nitrogen",YELLOW,30).move_to(pt(-.25,1.75)); c=chip("carbon skeleton",BLUE,30).move_to(pt(-.1,-1.75))
        self.add(scope_label(),aa)
        self.at("poses two problems")
        self.play(Create(fork),aa.animate.move_to(pt(-3.05,.1)),run_time=1.0)
        self.at("Nitrogen can be toxic")
        self.play(FadeIn(n,shift=RIGHT*.25),run_time=.65)
        danger=VGroup(RoundedRectangle(corner_radius=.12,width=.55,height=2.0,color=RED),Rectangle(width=.34,height=1.45,stroke_width=0,fill_color=RED,fill_opacity=.65).align_to(ORIGIN,DOWN),T("danger",28,RED)).arrange(RIGHT,buff=.2).move_to(pt(2.05,1.55))
        self.play(FadeIn(danger),run_time=.6)
        self.at("carbon remains valuable")
        self.play(FadeIn(c,shift=RIGHT*.25),run_time=.65)
        value=VGroup(Circle(radius=.55,color=GREEN,stroke_width=5),T("value",28,GREEN)).move_to(pt(2.75,-1.65))
        self.play(FadeIn(value),run_time=.6)
        self.at("passes onto glutamate")
        carriers=VGroup(chip("glutamate",YELLOW,28),chip("alanine",YELLOW,28),chip("glutamine",YELLOW,28)).arrange(RIGHT,buff=.38).move_to(pt(2.35,1.2))
        self.play(FadeOut(danger),FadeOut(n),FadeIn(carriers[0]),run_time=.8)
        self.at("alanine or glutamine")
        blood=RoundedRectangle(corner_radius=.3,width=5.8,height=1.45,color=GREY,stroke_width=3).move_to(pt(3.0,1.2))
        bl=T("blood",28,GREY).next_to(blood,UP,buff=.12)
        carriers[1:].shift(RIGHT*.65)
        self.play(Create(blood),FadeIn(bl),FadeIn(carriers[1:]),carriers[0].animate.shift(RIGHT*.65),run_time=.8)
        self.play(carriers[0].animate.shift(RIGHT*.08),carriers[1].animate.shift(RIGHT*.1),carriers[2].animate.shift(RIGHT*.12),run_time=.8)
        self.at("carbon skeleton moves")
        hub=VGroup(Circle(radius=.8,color=BLUE,stroke_width=6),T("central\nmetabolism",28,BLUE,line_spacing=.8)).move_to(pt(4.75,-1.65))
        lane=arr(c.get_right(),hub.get_left(),BLUE,6)
        self.play(FadeOut(value),GrowArrow(lane),FadeIn(hub),run_time=.7)
        self.play(c.animate.move_to(hub.get_left()+LEFT*.5),run_time=.8)
        self.play(FadeOut(c),Indicate(hub,color=BLUE,scale_factor=1.05),run_time=.45)
        self.finish()


class S08Nitrogen(SpokenScene):
    def construct(self):
        factory_backdrop(self)
        blood=Line(pt(-6.1,2.4),pt(6.1,2.4),color=GREY,stroke_width=8)
        liver=RoundedRectangle(corner_radius=.55,width=8.3,height=5.2,color=GREY,stroke_width=4,fill_color=GREY,fill_opacity=.05).move_to(pt(.6,-.35))
        wheel=VGroup(Circle(radius=1.45,color=GREEN,stroke_width=8),T("urea cycle",32,GREEN,weight=BOLD)).move_to(pt(.4,-.35))
        stations=VGroup(*[Dot(wheel[0].point_at_angle(i*TAU/5),radius=.13,color=GREEN) for i in range(5)])
        stations.add_updater(lambda m,dt:m.rotate(-.22*dt,about_point=wheel.get_center()))
        wheel.add(stations)
        self.add(blood,T("blood",28,GREY).move_to(pt(-5.35,2.75)),liver,T("liver",32,TEXT).move_to(pt(-2.8,1.75)),T("schematic",24,GREY).to_corner(DR,buff=.3))
        self.at("packaged as urea")
        self.play(FadeIn(wheel,scale=.8),run_time=.8)
        self.at("comes from ammonium")
        amm=chip("ammonium",YELLOW,28).move_to(pt(-4.1,.65)); n1=badge("N",.27).next_to(amm,RIGHT,buff=.22)
        self.play(FadeIn(amm),FadeIn(n1),run_time=.7)
        self.at("other comes from aspartate")
        asp=chip("aspartate",YELLOW,28).move_to(pt(-4.1,-1.25)); n2=badge("N",.27).next_to(asp,RIGHT,buff=.22)
        self.play(FadeIn(asp),FadeIn(n2),run_time=.7)
        self.play(n1.animate.move_to(wheel.get_center()+UP*.65),n2.animate.move_to(wheel.get_center()+DOWN*.65),run_time=1.0)
        self.at("spends four")
        marks=VGroup(*[T("⚡",34,YELLOW).move_to(pt(2.65+i*.58,.65)) for i in range(4)])
        self.play(LaggedStart(*[FadeIn(x,scale=.6) for x in marks],lag_ratio=.18),run_time=.8)
        self.at("per urea")
        self.play(LaggedStart(*[FadeOut(x,shift=DOWN*.15) for x in marks],lag_ratio=.15),run_time=.8)
        urea=VGroup(RoundedRectangle(corner_radius=.45,width=1.65,height=.85,color=GREEN,fill_color=GREEN,fill_opacity=.18),T("urea",30,GREEN,weight=BOLD)).move_to(pt(3.5,-.55))
        self.play(FadeOut(n1),FadeOut(n2),FadeIn(urea),run_time=.6)
        self.at("dangerous load")
        gauge=VGroup(RoundedRectangle(corner_radius=.12,width=.55,height=2.2,color=RED),Rectangle(width=.34,height=1.55,stroke_width=0,fill_color=RED,fill_opacity=.7).align_to(ORIGIN,DOWN),T("danger",28,RED).next_to(ORIGIN,DOWN,buff=1.3)).move_to(pt(5.35,.35))
        chute=arr(pt(4.1,-1.0),pt(5.65,-2.45),GREEN,7)
        self.play(FadeIn(gauge),GrowArrow(chute),run_time=.7)
        self.at("excretible product")
        self.play(FadeOut(chute),urea.animate.move_to(pt(5.35,-2.15)),
                  gauge[1].animate.set_height(.25).align_to(gauge[0],DOWN),run_time=1.1)
        self.finish()


class S09Carbon(SpokenScene):
    def construct(self):
        factory_backdrop(self)
        hub=VGroup(Circle(radius=1.15,color=BLUE,stroke_width=7),T("central\nmetabolism",28,BLUE,line_spacing=.8)).move_to(pt(-4.55,-.2))
        door=RoundedRectangle(corner_radius=.18,width=1.05,height=2.25,color=BLUE,stroke_width=5).move_to(pt(-2.25,-.2))
        self.add(hub,door,T("schematic",24,GREY).to_corner(DR,buff=.3))
        self.at("seven metabolic doors")
        cards=VGroup(*[chip(str(i),BLUE,28,pad=.14).move_to(pt(-5.7+i*.62,2.45)) for i in range(1,8)])
        self.play(LaggedStart(*[FadeIn(c,shift=DOWN*.2) for c in cards],lag_ratio=.12),run_time=1.2)
        count=M("7",52,BLUE).move_to(pt(-2.25,1.65)); self.play(FadeIn(count),run_time=.4)
        self.at("Five can supply")
        five=VGroup(*[cards[i].copy() for i in range(5)]).arrange(RIGHT,buff=.12).scale(.85).move_to(pt(.65,1.85))
        self.play(FadeOut(cards),FadeIn(five),run_time=.7)
        oaa=chip("oxaloacetate",GREEN,28).move_to(pt(.7,.6)); glucose=chip("net glucose",GREEN,30).move_to(pt(4.85,.6))
        path=arr(oaa.get_right(),glucose.get_left(),GREEN,6)
        self.play(FadeIn(oaa),GrowArrow(path),FadeIn(glucose),run_time=1.0)
        self.at("acetyl coenzyme A")
        ac=chip("acetyl-CoA",YELLOW,28).move_to(pt(.0,-.85))
        self.play(FadeOut(five),FadeOut(count),FadeOut(door),FadeIn(ac),run_time=.6)
        self.at("acetoacetyl")
        aac=chip("acetoacetyl-CoA",YELLOW,28).move_to(pt(.0,-1.75)); self.play(FadeIn(aac),run_time=.6)
        ket=VGroup(chip("ketones",YELLOW,28),chip("fat storage",YELLOW,28)).arrange(DOWN,buff=.25).move_to(pt(4.75,-1.25))
        p1=arr(ac.get_right(),ket[0].get_left(),YELLOW,5); p2=arr(aac.get_right(),ket[1].get_left(),YELLOW,5)
        self.play(GrowArrow(p1),GrowArrow(p2),FadeIn(ket),run_time=.9)
        block=T("×",48,RED,weight=BOLD).next_to(glucose,UP,buff=.12); self.play(FadeIn(block),run_time=.45)
        self.at("Only leucine")
        ll=VGroup(chip("leucine",TEXT,28),chip("lysine",TEXT,28)).arrange(DOWN,buff=.18).move_to(pt(-2.2,-2.15))
        self.play(FadeIn(ll),run_time=.6)
        self.at("purely ketogenic")
        self.play(ll[0].animate.next_to(ac,LEFT,buff=.25),ll[1].animate.next_to(aac,LEFT,buff=.25),run_time=1.0)
        self.finish()


class S10Return(SpokenScene):
    def construct(self):
        factory_backdrop(self)
        g=gate(-4.9,.25,.7)
        pm=proteasome(pt(-2.6,.05),.55)
        pool=VGroup(Circle(radius=1.0,color=GREEN,stroke_width=7),T("reuse",28,GREEN,weight=BOLD)).move_to(pt(.0,.25))
        fork=VGroup(Line(pt(1.5,.2),pt(2.65,1.55),color=GREY,stroke_width=7),Line(pt(1.5,.2),pt(2.65,-1.55),color=GREY,stroke_width=7))
        urea=VGroup(Circle(radius=.75,color=YELLOW,stroke_width=6),T("urea",28,YELLOW)).move_to(pt(4.15,1.65))
        carbon=VGroup(Circle(radius=.75,color=BLUE,stroke_width=6),T("7 doors",28,BLUE)).move_to(pt(4.15,-1.65))
        title=heading("The recycling center's logic",42).shift(DOWN*.42)
        self.add(title,g,pm,pool,fork,urea,carbon,T("schematic",24,GREY).to_corner(DR,buff=.3))
        moving_dots(self,pt(-5.8,-2.65),pt(5.5,-2.65),BLUE,12,.07,.06)
        self.at("Select the protein")
        self.play(Indicate(g,color=YELLOW,scale_factor=1.06),run_time=.8)
        self.at("before dismantling")
        self.play(Indicate(pm,color=BLUE,scale_factor=1.08),run_time=.8)
        self.at("Reuse most")
        self.play(Indicate(pool,color=GREEN,scale_factor=1.1),run_time=.8)
        self.at("surplus is burned")
        self.play(Indicate(fork,color=RED,scale_factor=1.05),run_time=.7)
        self.at("cage its nitrogen")
        self.play(Indicate(urea,color=YELLOW,scale_factor=1.1),run_time=.7)
        self.at("keep its carbon")
        self.play(Indicate(carbon,color=BLUE,scale_factor=1.1),run_time=.7)
        self.at("Choose what dies")
        choose=VGroup(g.copy().scale(1.25),T("choose",34,YELLOW,weight=BOLD)).arrange(DOWN,buff=.25)
        recycle=VGroup(Circle(radius=.8,color=GREEN,stroke_width=8),T("recycle most",34,GREEN,weight=BOLD)).arrange(DOWN,buff=.25)
        split=VGroup(fork.copy().scale(.75),T("split surplus",34,BLUE,weight=BOLD)).arrange(DOWN,buff=.25)
        icons=VGroup(choose,recycle,split).arrange(RIGHT,buff=.75).move_to(pt(0,-.25)); fit(icons,12.0,5.0)
        old=VGroup(g,pm,pool,fork,urea,carbon,title)
        self.play(FadeOut(old),FadeIn(icons,shift=UP*.15),run_time=1.1)
        self.at("split surplus amino acids")
        self.play(Indicate(icons[2],color=BLUE,scale_factor=1.04),run_time=.8)
        self.finish()


class S11End(EndCard):
    LINE = "Choose what dies, recycle most, then split surplus amino acids by atom."

    def construct(self):
        factory_backdrop(self)
        hexm=hex_mascot(1.35).move_to(pt(0,1.6))
        line1=T("Choose what dies, recycle most,",38,TEXT,font=TITLE_FONT)
        line2=T("then split surplus amino acids by atom.",38,TEXT,font=TITLE_FONT)
        lines=VGroup(line1,line2).arrange(DOWN,buff=.16).move_to(pt(0,.15))
        choose=VGroup(Line(LEFT*.42,RIGHT*.42,color=YELLOW,stroke_width=7),T("choose",28,YELLOW)).arrange(DOWN,buff=.14)
        recycle=VGroup(Circle(radius=.38,color=GREEN,stroke_width=6),T("recycle",28,GREEN)).arrange(DOWN,buff=.14)
        split=VGroup(Line(LEFT*.38,RIGHT*.38+UP*.5,color=BLUE,stroke_width=6),Line(LEFT*.38,RIGHT*.38+DOWN*.5,color=BLUE,stroke_width=6),T("split",28,BLUE)).arrange(DOWN,buff=.12)
        icons=VGroup(choose,recycle,split).arrange(RIGHT,buff=1.25).move_to(pt(0,-1.7))
        sub=T("biochemistrypedia.com",28,TEAL).to_edge(DOWN,buff=.28)
        self.play(FadeIn(hexm,shift=UP*.15),FadeIn(lines,shift=UP*.12),run_time=.9)
        self.play(LaggedStart(*[FadeIn(x,shift=UP*.15) for x in icons],lag_ratio=.18),FadeIn(sub),run_time=.8)
        self.play(icons.animate.shift(UP*.08),rate_func=there_and_back,run_time=1.0)
        shoulder=hexm.arm.get_start()
        self.play(Rotate(hexm.arm,angle=-.5,about_point=shoulder),rate_func=there_and_back,run_time=.55)
        self.finish()

