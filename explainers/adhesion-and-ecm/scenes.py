"""One Chain, Four Links — adhesion and ECM teaching film.

COLOR MAP
YELLOW calcium; BLUE cadherin; PURPLE integrin; TEAL adaptors;
GREEN actin; PINK keratin; ORANGE matrix; GOLD pull; GREY cell structure.
All diagrams are schematic labelled cartoons, never molecular structures.
"""

import numpy as np
from bp_style import *  # noqa: F401,F403


PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E87DB0"


def label(text, p, color=TEXT, size=28):
    return T(text, size=size, color=color).move_to(p)


def cell(cx, cy=0.55, w=2.7, h=3.75):
    body = RoundedRectangle(corner_radius=0.35, width=w, height=h,
                            stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.14).move_to([cx, cy, 0])
    nucleus = Ellipse(width=0.82, height=1.0, stroke_color=GREY, stroke_width=2,
                      fill_color=GREY, fill_opacity=0.28).move_to([cx, cy + 0.15, 0])
    return VGroup(body, nucleus)


def rope(y, amp=0.18, x0=-6.45, x1=6.45, phase=0.0, color=ORANGE, width=5):
    xs = np.linspace(x0, x1, 80)
    pts = [[x, y + amp * np.sin(1.55 * x + phase), 0] for x in xs]
    return VMobject(color=color, stroke_width=width).set_points_smoothly(pts)


def drifting_dots(points, color=YELLOW, radius=0.075, vx=0.07, vy=0.035,
                  bounds=(-6.5, 6.5, -3.5, 3.5)):
    """Small, continually moving particles for narrated fluid/gel holds."""
    group = VGroup(*[Dot(p, radius=radius, color=color) for p in points])
    xmin, xmax, ymin, ymax = bounds
    for i, dot in enumerate(group):
        dot.velocity = np.array([vx * (1 if i % 2 else -1), vy * (1 if i % 3 else -1), 0.0])

        def drift(m, dt, xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax):
            m.shift(m.velocity * dt)
            x, y = m.get_x(), m.get_y()
            if x < xmin: m.set_x(xmax)
            if x > xmax: m.set_x(xmin)
            if y < ymin: m.set_y(ymax)
            if y > ymax: m.set_y(ymin)
        dot.add_updater(drift)
    return group


def world(separated=False, with_label=True):
    shift = 0.38 if separated else 0.0
    xs = [-4.5 - shift, -1.5 - shift / 3, 1.5 + shift / 3, 4.5 + shift]
    cells = VGroup(*[cell(x, 0.55, 2.62 if not separated else 2.32,
                              3.75 if not separated else 3.32) for x in xs])
    basement = RoundedRectangle(corner_radius=0.08, width=12.9, height=0.26,
                                stroke_color=ORANGE, stroke_width=2.5,
                                fill_color=ORANGE, fill_opacity=0.28).move_to([0, -1.5, 0])
    ropes = VGroup(*[rope(y, 0.16, phase=i * 0.7, width=4)
                     for i, y in enumerate((-2.05, -2.55, -3.05, -3.45))])
    haze = Rectangle(width=13.0, height=2.15, stroke_width=0,
                     fill_color=ORANGE, fill_opacity=0.10).move_to([0, -2.55, 0])
    pts = [(-6 + i * 0.92, 2.72 + 0.14 * ((i * 7) % 3), 0) for i in range(14)]
    calcium = drifting_dots(pts, bounds=(-6.35, 6.35, 2.62, 3.05))
    lab = label("a sheet of epithelial cells", [-4.45, 3.55, 0], TEXT, 28)
    return VGroup(haze, ropes, basement, cells, calcium, *( [lab] if with_label else [] ))


def membrane(x, height=6.5):
    return RoundedRectangle(corner_radius=0.08, width=0.24, height=height,
                            stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.45).move_to([x, 0, 0])


def cad_arm(start, end, sag=0.0):
    p0, p1 = np.array(start, float), np.array(end, float)
    pts = []
    for i in range(5):
        u = i / 4
        p = p0 * (1-u) + p1 * u
        p[1] -= sag * np.sin(np.pi * u)
        pts.append(p)
    lines = VGroup(*[Line(pts[i], pts[i+1], color=BLUE, stroke_width=5) for i in range(4)])
    beads = VGroup(*[RoundedRectangle(corner_radius=0.05, width=0.25, height=0.25,
                                      stroke_color=BLUE, stroke_width=2,
                                      fill_color=BLUE, fill_opacity=0.5).move_to(p) for p in pts])
    return VGroup(lines, beads)


def calcium_joints(start, end):
    p0, p1 = np.array(start, float), np.array(end, float)
    return VGroup(*[Dot(p0 * (1-u) + p1 * u, radius=0.075, color=YELLOW)
                    for u in (0.125, 0.375, 0.625, 0.875)])


def arm_field(sag=0.0):
    arms, ca = VGroup(), VGroup()
    for y in (-1.65, 0, 1.65):
        arms.add(cad_arm([-1.9, y, 0], [-0.08, y, 0], sag),
                 cad_arm([1.9, y, 0], [0.08, y, 0], sag))
        ca.add(calcium_joints([-1.9, y, 0], [-0.08, y, 0]),
               calcium_joints([1.9, y, 0], [0.08, y, 0]))
    return arms, ca


def beaded_cable(a, b, color=GREEN, count=13):
    a, b = np.array(a, float), np.array(b, float)
    line = Line(a, b, color=color, stroke_width=5)
    beads = VGroup(*[Dot(a * (1-u) + b * u, radius=0.085, color=color)
                     for u in np.linspace(0, 1, count)])
    return VGroup(line, beads)


def adaptor(text, x, y=0):
    return chip(text, TEAL, size=28, pad=0.16).move_to([x, y, 0])


def chain_parts(y=0.35, show_labels=False):
    """Same landmarks for scenes 3–8: membrane x=±1.05, grip at x=0."""
    left_mem, right_mem = membrane(-1.05, 4.5), membrane(1.05, 4.5)
    # Keep the chain in one recognisable world: these broad, quiet cell interiors
    # make the intracellular/extracellular distinction readable without competing
    # with the coloured links.
    cell_fields = VGroup(
        Rectangle(width=5.25, height=5.55, stroke_width=0,
                  fill_color=GREY, fill_opacity=0.20).move_to([-3.68, 0, 0]),
        Rectangle(width=5.25, height=5.55, stroke_width=0,
                  fill_color=GREY, fill_opacity=0.20).move_to([3.68, 0, 0]),
    ).set_z_index(-2)
    larm = cad_arm([-1.05, y, 0], [-0.08, y, 0])
    rarm = cad_arm([1.05, y, 0], [0.08, y, 0])
    ca = VGroup(calcium_joints([-1.05, y, 0], [-0.08, y, 0]),
                calcium_joints([1.05, y, 0], [0.08, y, 0]))
    tails = VGroup(Line([-1.05, y, 0], [-1.55, y, 0], color=BLUE, stroke_width=5),
                   Line([1.05, y, 0], [1.55, y, 0], color=BLUE, stroke_width=5))
    lb, la = adaptor("β-catenin", -2.55, y), adaptor("α-catenin", -4.45, y)
    rb, ra = adaptor("β-catenin", 2.55, y), adaptor("α-catenin", 4.45, y)
    connectors = VGroup(Line([-1.55,y,0], lb.get_right(), color=TEAL, stroke_width=4),
                        Line(lb.get_left(), la.get_right(), color=TEAL, stroke_width=4),
                        Line([1.55,y,0], rb.get_left(), color=TEAL, stroke_width=4),
                        Line(rb.get_right(), ra.get_left(), color=TEAL, stroke_width=4))
    lcable = beaded_cable([-6.35,y,0], la.get_left(), GREEN, 12)
    rcable = beaded_cable(ra.get_right(), [6.35,y,0], GREEN, 12)
    labs = VGroup()
    if show_labels:
        labs.add(label("actin cable", [-5.15, 1.1, 0], GREEN),
                 label("cadherin", [0, 1.1, 0], BLUE))
    return dict(cell_fields=cell_fields, membranes=VGroup(left_mem,right_mem), arms=VGroup(larm,rarm), calcium=ca,
                tails=tails, adaptors=VGroup(lb,la,rb,ra), connectors=connectors,
                cables=VGroup(lcable,rcable), labels=labs)


def chain_group(d):
    return VGroup(d["cell_fields"], d["membranes"], d["arms"], d["calcium"], d["tails"],
                  d["adaptors"], d["connectors"], d["cables"], d["labels"])


def force_arrows(horizontal=True):
    if horizontal:
        return VGroup(Arrow([-5.55,2.25,0],[-6.55,2.25,0],buff=0,color=GOLD,stroke_width=8),
                      Arrow([5.55,2.25,0],[6.55,2.25,0],buff=0,color=GOLD,stroke_width=8))
    return VGroup(Arrow([0,3.1,0],[0,2.05,0],buff=0,color=GOLD,stroke_width=8),
                  Arrow([0,-3.1,0],[0,-2.05,0],buff=0,color=GOLD,stroke_width=8))


def tags(y=-1.25):
    texts = ("1 partner outside", "2 receptor", "3 adaptors", "4 cable")
    positions = ((2.2, y), (-.7, y), (-2.9, y), (-5.2, y))
    return VGroup(*[chip(t, TEXT, size=28, pad=0.13, fill_opacity=0.08).move_to([x, yy, 0])
                    for t, (x, yy) in zip(texts, positions)])


def integrin_world():
    membrane_bar = RoundedRectangle(corner_radius=0.08, width=12.8, height=0.28,
                                    stroke_color=GREY, stroke_width=3,
                                    fill_color=GREY, fill_opacity=0.42).move_to([0,0,0])
    haze = Rectangle(width=12.8, height=3.4, stroke_width=0, fill_color=ORANGE,
                     fill_opacity=0.13).move_to([0,-1.85,0])
    ropes = VGroup(*[rope(y, 0.14, phase=i*.8, width=4)
                     for i,y in enumerate((-1.35,-2.05,-2.75,-3.35))])
    alpha = RoundedRectangle(corner_radius=.22,width=.68,height=1.85,stroke_color=PURPLE,
                             stroke_width=4,fill_color=PURPLE,fill_opacity=.30).move_to([-.38,0,0])
    beta = alpha.copy().move_to([.38,0,0])
    al = label("α", alpha, TEXT, 30); bl = label("β", beta, TEXT, 30)
    strand = rope(-2.0, .22, -4.6, 4.6, .7, ORANGE, 5)
    rgd = chip("RGD", ORANGE, size=28, pad=.14).move_to([0,-1.3,0]); rgd[0].set_fill("#1d1812", 1); rgd.set_z_index(3)
    return dict(membrane=membrane_bar,haze=haze,ropes=ropes,
                integrin=VGroup(alpha,beta,al,bl),strand=strand,rgd=rgd)


class S00Hook(SpokenScene):
    def construct(self):
        intact = world(False)
        self.play(FadeIn(intact), run_time=.9)
        self.at("calcium away")
        separated = world(True)
        separated[4].shift(UP * 1.3).set_opacity(0)
        self.play(Transform(intact, separated), run_time=1.35)
        self.at("What was the calcium")
        question = label("What was calcium holding together?", [0,3.35,0], TEXT, 34)
        self.play(FadeOut(intact[-1]), FadeIn(question, shift=DOWN*.12), run_time=.45)
        self.at("Put it back")
        restored = world(False, with_label=False)
        self.play(FadeOut(question), Transform(intact, restored), run_time=1.45)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Adhesion and the extracellular matrix"
    TITLE = "One Chain, Four Links"

    def construct(self):
        w = world(False, with_label=False).set_opacity(.38)
        title = T(self.TITLE, size=56, font=TITLE_FONT)
        rule = Line(LEFT*1.3, RIGHT*1.3, color=GOLD, stroke_width=4)
        g = VGroup(title,rule).arrange(DOWN,buff=.3)
        self.add(w)
        self.play(FadeIn(g, shift=UP*.15), run_time=.65)
        self.wait(.75)
        self.play(FadeOut(g), run_time=.35)
        self.finish()


class S02Arms(SpokenScene):
    def construct(self):
        membranes = VGroup(membrane(-1.9), membrane(1.9))
        cell_fields = VGroup(
            Rectangle(width=4.35,height=7.0,stroke_width=0,fill_color=GREY,
                      fill_opacity=.20).move_to([-4.08,0,0]),
            Rectangle(width=4.35,height=7.0,stroke_width=0,fill_color=GREY,
                      fill_opacity=.20).move_to([4.08,0,0]),
        ).set_z_index(-2)
        arms, ca = arm_field()
        self.play(FadeIn(cell_fields),FadeIn(membranes),Create(arms),run_time=1.0)
        self.at("arms called")
        cad = label("cadherin", [-4.45,2.65,0], BLUE, 32)
        pointer = Arrow(cad.get_right(), [-1.15,1.65,0], buff=.15, color=BLUE)
        self.play(FadeIn(cad), GrowArrow(pointer), run_time=.5)
        self.at("Calcium sits")
        self.play(FadeIn(ca), run_time=.65)
        self.at("keeps it stiff")
        self.play(Indicate(arms, color=YELLOW, scale_factor=1.02), run_time=.65)
        self.at("grips the arm")
        flash = Dot([0,0,0], radius=.3, color=TEXT).set_opacity(.75)
        self.play(FadeIn(flash), arms.animate.set_stroke(width=7), run_time=.25)
        self.play(FadeOut(flash), arms.animate.set_stroke(width=5), run_time=.35)
        self.finish()


class S03Inside(SpokenScene):
    def construct(self):
        d = chain_parts(show_labels=False)
        base = VGroup(d["cell_fields"],d["membranes"],d["arms"],d["calcium"],d["tails"])
        self.play(FadeIn(base), run_time=.7)
        # The view follows the arm into the left cell before the narrator names
        # the intracellular pieces.
        self.play(base.animate.shift(RIGHT*.18),run_time=2.15,rate_func=smooth)
        self.at("Adaptor proteins")
        first=d["adaptors"][0]
        first.shift(UP*1.5+LEFT*.35)
        first.set_opacity(0)
        self.add(first)
        self.play(first.animate.set_opacity(1).shift(DOWN*1.5+RIGHT*.35),
                  Create(d["connectors"][0]),run_time=2.45)
        self.at("beta catenin")
        focus=Circle(radius=.82,color=TEAL,stroke_width=6,fill_color=TEAL,
                     fill_opacity=.14).move_to(d["adaptors"][0]).set_z_index(-1)
        self.play(FadeIn(focus),Indicate(d["adaptors"][0],color=TEAL),run_time=.4)
        self.at("alpha catenin")
        self.play(FadeIn(d["adaptors"][1]),Create(d["connectors"][1]),
                  focus.animate.move_to(d["adaptors"][1]),run_time=.55)
        self.play(Create(d["cables"][0]),focus.animate.move_to([-5.75,.35,0]),
                  run_time=2.35,rate_func=linear)
        self.at("filament of actin")
        actlab=label("actin cable",[-4.9,1.15,0],GREEN,30)
        self.play(FadeIn(actlab),focus.animate.set_color(GREEN).move_to([-4.9,.35,0]),run_time=.7)
        self.play(focus.animate.move_to([5.6,.35,0]),run_time=1.25,rate_func=linear)
        self.at("This grip")
        right=VGroup(d["adaptors"][2:],d["connectors"][2:],d["cables"][1])
        self.play(FadeIn(right),focus.animate.move_to([3.2,.35,0]),run_time=.6)
        self.at("adherence junction")
        bracket=Brace(VGroup(d["cables"],d["arms"]),DOWN,color=TEXT)
        jlab=label("adherens junction",[0,-3.2,0],TEXT,32)
        self.play(FadeOut(focus),GrowFromCenter(bracket),FadeIn(jlab),run_time=.55)
        self.finish()


class S04Chain(SpokenScene):
    def construct(self):
        d=chain_parts(show_labels=False); g=chain_group(d)
        self.add(g)
        self.at("simplest form")
        corner=label("simplest form",[-5.25,3.1,0],TEXT,28)
        self.play(FadeIn(corner),run_time=.35)
        self.at("four links")
        self.play(g.animate.shift(UP*.20),run_time=.5,rate_func=there_and_back)
        tg=tags(-2.85)
        cues=("partner outside","receptor in","adapters","cable inside")
        highlights=(d["arms"][1],d["arms"][0],d["adaptors"][:2],d["cables"][0])
        for cue,t,h in zip(cues,tg,highlights):
            self.at(cue)
            self.play(FadeIn(t,shift=UP*.08),Indicate(h,color=TEXT,scale_factor=1.03),run_time=.45)
        self.finish()


class S05Rule(SpokenScene):
    def construct(self):
        d=chain_parts(); g=chain_group(d); arrows=force_arrows()
        self.add(g)
        # A broad travelling load glow makes the continuous pull visible even
        # while the narration pauses between beats.
        load_glow=VGroup(d["cables"].copy(),d["connectors"].copy(),d["arms"].copy())
        load_glow.set_color(GOLD).set_stroke(width=11,opacity=.16).set_z_index(3)
        phase=ValueTracker(0)
        load_glow.add_updater(lambda m: m.set_opacity(.10+.20*(.5+.5*np.sin(phase.get_value()))))
        self.add(load_glow)
        self.at("pull on the sheet")
        self.play(GrowArrow(arrows[0]),GrowArrow(arrows[1]),g.animate.stretch(1.015,0),
                  phase.animate.set_value(PI),run_time=.6)
        self.play(g.animate.stretch(1.025,0),arrows.animate.scale(1.08),
                  phase.animate.set_value(3*PI),run_time=2.55,rate_func=there_and_back)
        self.at("pull runs")
        path=VMobject().set_points_as_corners([[-6.2,.35,0],[-3.55,.35,0],[-2.2,.35,0],
                                               [-1.05,.35,0],[0,.35,0],[1.05,.35,0],
                                               [2.2,.35,0],[3.55,.35,0],[6.2,.35,0]])
        pulse=VGroup(Dot([-6.2,.35,0],radius=.30,color=GOLD),
                     Circle(radius=.52,color=GOLD,stroke_width=5).move_to([-6.2,.35,0]))
        self.add(pulse)
        self.play(MoveAlongPath(pulse,path,rate_func=linear),phase.animate.set_value(5*PI),
                  g.animate(rate_func=there_and_back).stretch(1.018,0),run_time=2.1)
        pulse.move_to(path.get_start())
        self.play(MoveAlongPath(pulse,path,rate_func=linear),phase.animate.set_value(7*PI),
                  g.animate(rate_func=there_and_back).stretch(1.018,0),run_time=1.4)
        self.at("Break any one link")
        broken=d["connectors"][1]
        self.play(FadeOut(broken),pulse.animate.move_to([-2.4,.35,0]),phase.animate.set_value(8*PI),
                  d["cell_fields"][0].animate(rate_func=there_and_back).shift(LEFT*.16),
                  d["cell_fields"][1].animate(rate_func=there_and_back).shift(RIGHT*.16),run_time=.5)
        cut=label("one break cuts the path",[0,3.05,0],TEXT,34)
        self.at("path is cut")
        self.play(FadeIn(cut),Flash([-2.9,.35,0],color=RED),phase.animate.set_value(9*PI),run_time=.55)
        pulse.move_to(path.get_start())
        self.play(FadeIn(broken),MoveAlongPath(pulse,path),phase.animate.set_value(11*PI),run_time=1.25,rate_func=linear)
        self.finish()


def prediction_overlay():
    q=label("No calcium: which link fails first?",[0,3.15,0],TEXT,34)
    boxes=VGroup(
        RoundedRectangle(width=2.45,height=1.1,corner_radius=.12,color=BLUE,
                         fill_color=BLUE,fill_opacity=.11).move_to([0,.35,0]),
        RoundedRectangle(width=3.8,height=1.1,corner_radius=.12,color=TEAL,
                         fill_color=TEAL,fill_opacity=.11).move_to([-3.5,.35,0]),
        RoundedRectangle(width=1.3,height=1.1,corner_radius=.12,color=GREEN,
                         fill_color=GREEN,fill_opacity=.11).move_to([-6.05,.35,0]))
    labs=VGroup(label("arms outside",[0,-3.2,0],BLUE,28),
                label("adaptors",[-3.5,-3.2,0],TEAL,28),
                label("cable",[-6.05,-3.2,0],GREEN,28))
    return q,boxes,labs


class S06Predict(SpokenScene):
    def construct(self):
        d=chain_parts(); g=chain_group(d); arrows=force_arrows(); self.add(g,arrows)
        phase=ValueTracker(0)
        tension=VGroup(d["cables"].copy(),d["connectors"].copy(),d["arms"].copy())
        tension.set_color(GOLD).set_stroke(width=10,opacity=.12).set_z_index(2)
        tension.add_updater(lambda m: m.set_opacity(.08+.18*(.5+.5*np.sin(phase.get_value()))))
        self.add(tension)
        phase.add_updater(lambda m,dt: m.increment_value(dt*1.35))
        self.add(phase)
        self.at("take the calcium away")
        self.play(d["calcium"].animate.set_opacity(.32),run_time=.7)
        self.at("Which link gives")
        q,boxes,labs=prediction_overlay(); self.play(FadeIn(q),run_time=.4)
        highlights=(d["arms"],d["adaptors"],d["cables"])
        for cue,b,l,h in zip(("arms outside","adapters","cable"),boxes,labs,highlights):
            self.at(cue)
            self.play(Create(b),FadeIn(l),Indicate(h,color=b.get_color(),scale_factor=1.05),
                      run_time=.42)
        self.at("Choose one")
        options=VGroup(boxes,labs)
        self.play(options.animate.scale(1.015),arrows.animate.scale(1.04),
                  run_time=.65,rate_func=there_and_back)
        self.finish()


class S07Pause(Scene):
    def construct(self):
        d=chain_parts(); q,boxes,labs=prediction_overlay(); arrows=force_arrows()
        self.add(chain_group(d),q,boxes,labs,arrows)
        # Three short breaths are visibly distinct to the freeze detector while
        # keeping the scripted thinking pause gentle and uncluttered.
        options=VGroup(boxes,labs)
        for _ in range(3):
            self.play(options.animate.scale(1.015),arrows.animate.scale(1.04),
                      run_time=.55,rate_func=there_and_back)
            self.wait(.95)


class S08Reveal(SpokenScene):
    def construct(self):
        d=chain_parts(); q,boxes,labs=prediction_overlay(); arrows=force_arrows()
        self.add(chain_group(d),q,boxes,labs,arrows)
        self.at("Calcium leaves")
        self.play(d["calcium"].animate.shift(UP*2.2).set_opacity(0),FadeOut(q),FadeOut(labs),run_time=.9)
        self.at("arms go floppy")
        limp=VGroup(cad_arm([-1.05,.35,0],[-.14,.05,0],.42),cad_arm([1.05,.35,0],[.14,.05,0],.42))
        self.play(Transform(d["arms"],limp),run_time=.8)
        self.at("outer link lets go")
        self.play(d["arms"][0].animate.shift(LEFT*.32),d["arms"][1].animate.shift(RIGHT*.32),
                  boxes[0].animate.set_color(RED),run_time=.65)
        self.at("adapters and the cable")
        self.play(Indicate(VGroup(d["adaptors"],d["cables"]),color=TEXT,scale_factor=1.02),run_time=.7)
        self.at("no longer pass")
        stop=Dot([-1.22,.35,0],radius=.18,color=GOLD); self.add(stop)
        left_side=VGroup(d["cell_fields"][0],d["membranes"][0],d["cables"][0],
                         d["adaptors"][:2],d["connectors"][:2],d["tails"][0],d["arms"][0],boxes[1:])
        right_side=VGroup(d["cell_fields"][1],d["membranes"][1],d["cables"][1],
                          d["adaptors"][2:],d["connectors"][2:],d["tails"][1],d["arms"][1])
        self.play(stop.animate.move_to([-.45,.35,0]),left_side.animate.shift(LEFT*.16),
                  right_side.animate.shift(RIGHT*.16),run_time=.8)
        self.play(Flash([-.45,.35,0],color=RED),stop.animate.set_opacity(0),run_time=.55)
        self.at("sheet comes apart")
        old=Group(*list(self.mobjects))
        apart=world(True,with_label=False).scale(.72)
        self.add(apart)
        self.play(FadeOut(old),apart.animate.scale(1/.72),run_time=.75)
        self.play(Transform(apart,world(False,with_label=False)),run_time=1.15)
        self.finish()


class S09Floor(SpokenScene):
    def construct(self):
        iw=integrin_world()
        self.add(VGroup(iw["haze"],iw["ropes"],iw["membrane"]))
        self.at("at the matrix")
        ml=label("matrix",[-5.1,-.65,0],ORANGE,32); self.play(FadeIn(ml),run_time=.35)
        self.at("material cells")
        self.play(iw["ropes"].animate.shift(RIGHT*.24),run_time=.7,rate_func=there_and_back)
        self.at("receptor is an integrin")
        self.play(FadeIn(iw["integrin"],shift=DOWN*.45),run_time=.65)
        il=label("integrin",[2.15,.45,0],PURPLE,32); self.play(FadeIn(il),run_time=.3)
        self.at("alpha and beta")
        self.play(Indicate(iw["integrin"],color=PURPLE),
                  iw["ropes"].animate.shift(LEFT*.24),run_time=.55,rate_func=there_and_back)
        self.at("fibronctin")
        self.play(Create(iw["strand"]),run_time=.7)
        fl=label("fibronectin",[4.45,-.65,0],ORANGE,30); self.play(FadeIn(fl),run_time=.3)
        self.at("short tag")
        self.play(FadeIn(iw["rgd"]),run_time=.4)
        self.at("RgD")
        self.play(iw["integrin"].animate.stretch(1.1,1),iw["rgd"].animate.move_to([0,-1.03,0]),
                  Flash([0,-.9,0],color=TEXT),run_time=.65)
        self.finish()


class S10IntegrinChain(SpokenScene):
    def construct(self):
        iw=integrin_world(); base=VGroup(*iw.values()); self.add(base)
        actin=beaded_cable([-4.8,2.7,0],[4.8,2.7,0],GREEN,24)
        talin=chip("talin",TEAL,size=28,pad=.18).rotate(PI/2).move_to([0,1.35,0])
        self.at("talon ties")
        self.play(FadeIn(talin),Create(Line([0,.75,0],[0,.35,0],color=TEAL,stroke_width=5)),
                  iw["ropes"].animate(rate_func=there_and_back).shift(RIGHT*.28),run_time=.55)
        self.at("tail to actin")
        self.play(Create(actin),Create(Line([0,1.95,0],[0,2.7,0],color=TEAL,stroke_width=5)),
                  iw["ropes"].animate(rate_func=there_and_back).shift(LEFT*.28),run_time=.65)
        self.at("vinculin adds")
        vin=VGroup(chip("vinculin",TEAL,size=28,pad=.12).move_to([-1.55,1.55,0]),
                   chip("vinculin",TEAL,size=28,pad=.12).move_to([1.55,1.55,0]))
        ties=VGroup(Line(vin[0].get_top(),[-1.55,2.7,0],color=TEAL,stroke_width=4),
                    Line(vin[0].get_right(),[-.25,1.45,0],color=TEAL,stroke_width=4),
                    Line(vin[1].get_top(),[1.55,2.7,0],color=TEAL,stroke_width=4),
                    Line(vin[1].get_left(),[.25,1.45,0],color=TEAL,stroke_width=4))
        self.play(FadeIn(vin),run_time=.4)
        self.at("extra ties")
        self.play(Create(ties),actin.animate(rate_func=there_and_back).shift(UP*.18),run_time=.65)
        self.at("Notice the pattern")
        tg=VGroup(*[chip(t,TEXT,size=28,pad=.1,fill_opacity=.06).move_to(p) for t,p in zip(
            ("1 partner","2 receptor","3 adaptors","4 cable"),
            ((-4.7,-.65,0),(3.55,.65,0),(4.7,1.55,0),(4.75,3.35,0)))])
        self.play(FadeIn(tg),actin.animate(rate_func=there_and_back).shift(UP*.18),run_time=.7)
        self.at("receptor has changed")
        self.play(Indicate(iw["integrin"],color=PURPLE,scale_factor=1.10),run_time=.55)
        self.at("four links have not")
        self.play(Indicate(tg,color=TEXT,scale_factor=1.03),run_time=.6)
        self.at("cell tugs")
        pulse=Dot([0,2.7,0],radius=.17,color=GOLD)
        path=VMobject().set_points_as_corners([[0,2.7,0],[0,1.4,0],[0,0,0],[0,-1.05,0],[0,-2.0,0]])
        self.add(pulse)
        self.play(FadeOut(tg),actin.animate.stretch(.92,0),MoveAlongPath(pulse,path),
                  iw["strand"].animate.stretch(1.08,0),run_time=1.4)
        focal=label("focal adhesion (cultured cells)",[4.0,.85,0],TEXT,28)
        self.play(FadeIn(focal),run_time=.35)
        self.finish()


class S11Keratin(SpokenScene):
    def construct(self):
        cells=VGroup(cell(-2.0,.75,3.8,4.2),cell(2.0,.75,3.8,4.2))
        basement=RoundedRectangle(corner_radius=.08,width=12.6,height=.3,color=ORANGE,
                                  fill_color=ORANGE,fill_opacity=.25).move_to([0,-1.55,0])
        bm=label("basement membrane",[3.9,-2.15,0],ORANGE,30)
        self.play(FadeIn(cells),FadeIn(basement),FadeIn(bm),run_time=.8)
        self.at("Desmosomes")
        side=VGroup(Line([-1.05,.15,0],[1.05,.15,0],color=BLUE,stroke_width=8),
                    beaded_cable([-5.5,.15,0],[-1.05,.15,0],PINK,14),
                    beaded_cable([1.05,.15,0],[5.5,.15,0],PINK,14))
        dl=VGroup(label("desmosome",[0,3.5,0],TEXT,30),Line([0,3.25,0],[0,.4,0],color=TEXT,stroke_width=2).set_opacity(.6))
        self.play(FadeIn(side),FadeIn(dl),run_time=.7)
        self.at("Hemidesmosomes")
        hemi=VGroup(RoundedRectangle(width=.78,height=1.05,corner_radius=.16,color=PURPLE,
                                     fill_color=PURPLE,fill_opacity=.3).move_to([-2,-1.1,0]),
                    chip("adaptor",TEAL,size=28,pad=.12).move_to([-2,-.25,0]),
                    beaded_cable([-4.7,.55,0],[-2,.55,0],PINK,10),
                    Line([-2,.55,0],[-2,.04,0],color=TEAL,stroke_width=5),
                    Line([-2,-.46,0],[-2,-1.55,0],color=TEAL,stroke_width=5))
        hl=VGroup(label("hemidesmosome",[-5.0,-2.35,0],TEXT,28),Line([-3.7,-2.2,0],[-2.3,-1.75,0],color=TEXT,stroke_width=2).set_opacity(.6))
        self.play(FadeIn(hemi),FadeIn(hl),run_time=.75)
        self.at("thin matrix sheet")
        self.play(Indicate(basement,color=ORANGE,scale_factor=1.02),run_time=.5)
        self.at("both end on keratin")
        kl=label("keratin cable",[5.0,3.5,0],PINK,32)
        pink_cables=VGroup(side[1:],hemi[2])
        self.play(FadeIn(kl),Indicate(pink_cables,color=PINK,scale_factor=1.03),
                  pink_cables.animate(rate_func=there_and_back).shift(UP*.18),
                  cells.animate(rate_func=there_and_back).shift(UP*.24),run_time=.7)
        self.at("not on actin")
        act=label("actin",[5.2,-2.9,0],GREEN,28).set_opacity(.65)
        cross=Cross(act,stroke_color=TEXT,stroke_width=4)
        self.play(FadeIn(VGroup(act,cross)),pink_cables.animate(rate_func=there_and_back).shift(UP*.18),
                  cells.animate(rate_func=there_and_back).shift(UP*.24),run_time=.55)
        self.finish()


class S12Ropes(SpokenScene):
    def construct(self):
        waves=VGroup(*[rope(y,.28,phase=i*.8,width=7) for i,y in enumerate((-2,-1,0,1,2))])
        title=label("collagen ropes",[0,3.45,0],ORANGE,34)
        self.add(waves,title)
        self.at("collagen ropes")
        self.play(waves.animate.shift(RIGHT*.36),run_time=.45,rate_func=there_and_back)
        self.at("straighten under a pole")
        pulls=force_arrows(); straight=VGroup(*[Line([-6.2,y,0],[6.2,y,0],color=ORANGE,stroke_width=7)
                                               for y in (-2,-1,0,1,2)])
        self.play(FadeIn(pulls),Transform(waves,straight),run_time=1.1)
        self.at("resist it strongly")
        self.play(Indicate(waves,color=GOLD,scale_factor=1.01),run_time=.65)
        self.at("squeeze the tissue")
        inward=force_arrows(False); buckled=VGroup(*[rope(y,.45,phase=i*1.1,width=6)
                                                    for i,y in enumerate((-1.35,-.68,0,.68,1.35))])
        self.play(Transform(pulls,inward),Transform(waves,buckled),run_time=1.1)
        self.at("go slack")
        self.play(waves.animate.set_opacity(.62).stretch(.92,1),run_time=.6)
        self.at("poor at pushing")
        rule=label("strong in pulling, weak in squeezing",[0,-3.5,0],TEXT,32)
        self.play(FadeIn(rule),run_time=.5)
        self.finish()


class S13Gel(SpokenScene):
    def construct(self):
        ropes=VGroup(*[rope(y,.3,phase=i,width=4).set_opacity(.45) for i,y in enumerate((-2.4,2.4))])
        gel=RoundedRectangle(width=9.4,height=4.7,corner_radius=.65,stroke_color=ORANGE,stroke_width=3,
                             fill_color=ORANGE,fill_opacity=.16)
        title=label("proteoglycan gel",[0,3.45,0],ORANGE,34)
        self.play(FadeIn(VGroup(ropes,gel,title)),run_time=.75)
        self.at("long sugar chains")
        core=Line([-2.8,0,0],[2.8,0,0],color=ORANGE,stroke_width=8)
        bristles=VGroup(*[Line([x,0,0],[x,1.65 if i%2 else -1.65,0],color=ORANGE,stroke_width=4)
                          for i,x in enumerate(np.linspace(-2.5,2.5,11))])
        minus=VGroup(*[label("−",[x,1.05 if i%2 else -1.05,0],TEXT,30)
                       for i,x in enumerate(np.linspace(-2.5,2.5,11))])
        self.play(Create(core),Create(bristles),FadeIn(minus),run_time=.9)
        self.at("negative charges")
        self.play(Indicate(minus,color=TEXT,scale_factor=1.05),run_time=.55)
        self.at("draw in water")
        pts=[(-5.8+i*.7,(-1)**i*2.65,0) for i in range(17)]
        water=drifting_dots(pts,color=BLUE,radius=.09,vx=.10,vy=.06,bounds=(-4.4,4.4,-2.15,2.15))
        self.add(water)
        self.play(*[d.animate.move_to([(-3.7+i*.46),(-1)**i*(.35+(.18*(i%5))),0]) for i,d in enumerate(water)],
                  gel.animate.scale(1.08),run_time=1.1)
        self.at("Squeeze it")
        arrows=force_arrows(False); self.play(FadeIn(arrows),gel.animate.stretch(.82,1),
                                               bristles.animate.stretch(.75,1),run_time=.75)
        self.at("pushes back")
        self.play(arrows.animate.scale(.85),gel.animate.stretch(1.15,1),run_time=.75)
        schematic=label("schematic",[5.15,-3.05,0],TEXT,28); self.play(FadeIn(schematic),run_time=.25)
        self.finish()


class S14Return(SpokenScene):
    def construct(self):
        w=world(False,with_label=False); self.play(FadeIn(w),run_time=.75)
        web=VGroup()
        for x in (-3,-.0,3):
            web.add(Line([x,2.3,0],[x,-1.5,0],color=GREEN,stroke_width=5),
                    Line([x,-1.5,0],[x,-3.25,0],color=PURPLE,stroke_width=6))
        for x in (-3,0,3):
            web.add(Line([x-.38,.7,0],[x+.38,.7,0],color=BLUE,stroke_width=7))
        self.at("one web of chains")
        self.play(Create(web),run_time=1.1)
        self.at("many chains side by side")
        parallel=VGroup(*[Line([-1.0+i*.22,-.1,0],[-1.0+i*.22,-2.6,0],color=PURPLE,stroke_width=4)
                          for i in range(9)])
        self.play(FadeIn(parallel),run_time=.7)
        self.at("sharing the load")
        pulses=VGroup(*[Dot([-1.0+i*.22,-.1,0],radius=.09,color=GOLD) for i in range(9)])
        self.add(pulses)
        self.play(pulses.animate.shift(DOWN*2.35),run_time=1.0,rate_func=linear)
        self.at("One question is left")
        q=label("Does the pull change the links?",[0,3.3,0],TEXT,38)
        self.play(w.animate.set_opacity(.45),web.animate.set_opacity(.6),FadeOut(w[4]),FadeIn(q),run_time=.65)
        self.at("pull change the links")
        pulse=Dot([-5.4,.7,0],radius=.18,color=GOLD)
        self.add(pulse); self.play(pulse.animate.move_to([5.4,.7,0]),run_time=1.6,rate_func=linear)
        self.finish()


class S15End(EndCard):
    LINE = "Each grip is a chain, outside partner to inside cable."

