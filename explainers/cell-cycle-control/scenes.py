"""Cell-cycle states and control logic: a kinase whose partner rises and falls  (Biochemistrypedia explainer, Cell Biology)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = CDK (CDK1 / Cdc2), the kinase
  ORANGE = cyclin, and the cyclin level
  YELLOW = the transferable activity (the unknown "copy now" signal, MPF)
  TEAL   = DNA copying
  GREEN  = on / active / matured / mitosis
  RED    = refuses / off / destroyed
  PURPLE = Wee1 and Cdc25
  PINK   = the hormone progesterone
  GOLD   = a phosphate badge
  GREY   = cells, nuclei, axes, interphase and resting states
"""
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58FB5"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def bar_t(a, b, color=RED, w=5):
    """inhibition: line ending in a T bar."""
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w),
                  Line(b + perp * 0.25, b - perp * 0.25, color=color, stroke_width=w + 1))


def bchip(text, color=BLUE, size=24, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def cross_mark(center, s=0.3, color=RED, w=7):
    c = np.array(center, float)
    return VGroup(Line(c + [-s, -s, 0], c + [s, s, 0], color=color, stroke_width=w),
                  Line(c + [-s, s, 0], c + [s, -s, 0], color=color, stroke_width=w))


def cell_shape(cx, cy, w, h, color=GREY, op=0.07):
    return RoundedRectangle(corner_radius=0.9, width=w, height=h, stroke_color=color, stroke_width=4,
                            fill_color=color, fill_opacity=op).move_to([cx, cy, 0])


def nucleus(cx, cy, r=0.62, color=GREY, fill=0.1):
    return Circle(radius=r, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=fill).move_to([cx, cy, 0])


def pbadge(size=0.22):
    c = Circle(radius=size, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=1)
    return VGroup(c, T("P", 24, BG, weight=BOLD).move_to(c))


def sawtooth(xs, ys, x0, x1, y0, y1, teeth_end, color=ORANGE, w=6, power=1.6, n=60, last_frac=1.0):
    """Polyline: level rises through each cycle and drops at each division. teeth_end = division times."""
    pts = []
    t_prev = 0.0
    for k, te in enumerate(teeth_end):
        frac_end = last_frac if k == len(teeth_end) - 1 else 1.0
        for i in range(n + 1):
            u = (i / n) * frac_end
            t = t_prev + u * (te - t_prev)
            lvl = 0.06 + 0.88 * (u ** power)
            pts.append([xs(t), ys(lvl), 0])
        if frac_end >= 1.0 and k < len(teeth_end) - 1:
            pts.append([xs(te), ys(0.06), 0])
        t_prev = te
    m = VMobject(stroke_color=color, stroke_width=w)
    m.set_points_as_corners(pts)
    return m


class Plot:
    """A bare plot frame: x from X0..X1 (screen), y from Y0..Y1 (screen); time 0..tmax; level 0..1."""

    def __init__(self, X0, X1, Y0, Y1, tmax, xlab="time", ylab="level"):
        self.X0, self.X1, self.Y0, self.Y1, self.tmax = X0, X1, Y0, Y1, tmax
        self.xaxis = Arrow([X0, Y0, 0], [X1, Y0, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.2)
        self.yaxis = Arrow([X0, Y0, 0], [X0, Y1, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.2)
        self.xl = T(xlab, 22, GREY).next_to(self.xaxis, DOWN, buff=0.1).align_to(self.xaxis, RIGHT)
        self.yl = T(ylab, 22, GREY).next_to(self.yaxis, UP, buff=0.12).align_to(self.yaxis, LEFT)
        self.group = VGroup(self.xaxis, self.yaxis, self.xl, self.yl)

    def xs(self, t):
        return self.X0 + (self.X1 - self.X0 - 0.3) * t / self.tmax

    def ys(self, v):
        return self.Y0 + (self.Y1 - self.Y0 - 0.3) * v


def until(scene, phrase, extra=0.0, floor=0.5, nth=0):
    """seconds from now until just before the narrator says `phrase` (for draws that should end on a cue)."""
    return max(floor, scene.t_of(phrase, nth) - 0.2 - scene.elapsed() + extra)


class S00Title(TitleCard):
    LESSON = "Cell-cycle states and control logic"
    TITLE = "The Cyclin-CDK Engine"


CDK_W, CDK_H = 3.0, 2.5
CYC_W = 1.9


def cdk_blob(label="CDK1"):
    """CDK: a blue body with a pocket (the catalytic site). A red bar blocks the pocket when it is off.
    VGroup(body, pocket, flap, lab) with those attributes."""
    body = RoundedRectangle(corner_radius=0.4, width=CDK_W, height=CDK_H, stroke_color=BLUE, stroke_width=4,
                            fill_color=BLUE, fill_opacity=0.28)
    pocket = RoundedRectangle(corner_radius=0.14, width=1.0, height=0.7, stroke_color=BLUE, stroke_width=3,
                              fill_color=BG, fill_opacity=1).move_to(body.get_top() + DOWN * 0.7 + LEFT * 0.6)
    flap = Rectangle(width=1.2, height=0.14, stroke_width=0, fill_color=RED, fill_opacity=1).move_to(pocket.get_center())
    lab = T(label, 32, BLUE, weight=BOLD).move_to(body.get_center() + DOWN * 0.45)
    g = VGroup(body, pocket, flap, lab)
    g.body, g.pocket, g.flap, g.lab = body, pocket, flap, lab
    return g


def cyclin_blob(label="cyclin B"):
    r = RoundedRectangle(corner_radius=0.35, width=CYC_W, height=CDK_H, stroke_color=ORANGE, stroke_width=4,
                         fill_color=ORANGE, fill_opacity=0.3)
    return VGroup(r, T(label, 26, ORANGE, weight=BOLD).move_to(r))


def set_off(cdk):
    return [cdk.flap.animate.set_opacity(1), cdk.pocket.animate.set_stroke(BLUE).set_fill(BG, 1)]


def set_on(cdk):
    return [cdk.flap.animate.set_opacity(0), cdk.pocket.animate.set_stroke(GREEN).set_fill(GREEN, 0.3)]


def ymap(nm):
    return -2.6 + nm * 0.115


# New schematic helpers use the original shapes and concept colours.
def complex_at(x=0, y=0, label="CDK1", cyclin="cyclin B"):
    c = cdk_blob(label).move_to([x, y, 0])
    b = cyclin_blob(cyclin).move_to([x + CDK_W / 2 + CYC_W / 2 + 0.06, y, 0])
    return c, b


def cycle_ring(center=ORIGIN, radius=2.15):
    arcs, labels = VGroup(), VGroup()
    # Clockwise order, starting at the top.
    for i, name in enumerate(("G1", "S", "G2", "M")):
        angle = PI / 2 - i * PI / 2
        arcs.add(Arc(radius=radius, start_angle=angle - 0.08,
                     angle=-PI / 2 + 0.16, arc_center=center,
                     color=GREY, stroke_width=6))
        theta = angle - PI / 4
        labels.add(T(name, 30, GREY, weight=BOLD).move_to(
            center + (radius - 0.55) * np.array([np.cos(theta), np.sin(theta), 0])))
    return VGroup(arcs, labels)


def radial_peak(theta, center=ORIGIN, radius=2.15):
    points = []
    for a in np.linspace(theta + 0.68, theta - 0.68, 70):
        r = radius + 0.8 * np.exp(-((a - theta) / 0.27) ** 2)
        points.append(center + r * np.array([np.cos(a), np.sin(a), 0]))
    curve = VMobject(stroke_color=ORANGE, stroke_width=7)
    return curve.set_points_as_corners(points)


def tag_badge():
    return VGroup(*[Circle(radius=0.11, color=GOLD, fill_opacity=1).move_to([0.19*i, 0, 0])
                    for i in range(3)])


def locked_cyclin():
    c = bchip("cyclin B", ORANGE, 28)
    lock = VGroup(RoundedRectangle(width=0.45, height=0.38, corner_radius=0.05,
                                   color=ORANGE, fill_color=BG, fill_opacity=1),
                  Arc(radius=0.16, start_angle=0, angle=PI, color=ORANGE).shift(UP*0.2))
    lock.next_to(c, UP, buff=0.12)
    return VGroup(c, lock)


class S01Engine(SpokenScene):
    def construct(self):
        yeast = VGroup(cell_shape(-3.4, 1, 2.0, 2.8), nucleus(-3.4, 1, 0.42),
                       T("yeast", 26, GREY).move_to([-3.4, -0.9, 0]))
        human = VGroup(cell_shape(3.4, 1, 2.8, 2.8), nucleus(3.4, 1, 0.5),
                       T("human cell", 26, GREY).move_to([3.4, -0.9, 0]))
        engine = bchip("one engine", YELLOW, 32).move_to([0, -2.3, 0])
        self.at("Every cell")
        self.play(FadeIn(yeast), FadeIn(human), run_time=0.6)
        self.at("one engine")
        links = VGroup(arr([-2.6, -0.4, 0], [-0.8, -1.9, 0], YELLOW),
                       arr([2.6, -0.4, 0], [0.8, -1.9, 0], YELLOW))
        self.play(FadeIn(engine), Create(links), run_time=0.5)
        self.at("The engine is")
        c, b = complex_at(-1.25, 0.9, "CDK", "cyclin")
        dock = b.get_center().copy()
        b.shift(RIGHT*2.0)
        self.play(FadeOut(yeast), FadeOut(human), FadeOut(links),
                  ReplacementTransform(engine, c), run_time=0.7)
        self.at("Alone it does")
        state = T("OFF", 30, RED, weight=BOLD).move_to([-1.25, 2.8, 0])
        self.play(FadeIn(state), Indicate(c.flap, color=RED), run_time=0.5)
        self.at("a partner protein")
        self.play(FadeIn(b), run_time=0.4)
        self.at("is bound")
        on = T("ON", 30, GREEN, weight=BOLD).move_to(state)
        self.play(b.animate.move_to(dock), *set_on(c), ReplacementTransform(state, on), run_time=0.6)
        self.at("The cell builds")
        p = Plot(-5.5, 5.7, -2.8, -0.8, 3, "time", "level")
        flat = Line([p.xs(0), p.ys(0.45), 0], [p.xs(3), p.ys(0.45), 0], color=BLUE, stroke_width=5)
        kl = T("CDK", 24, BLUE).move_to([5, -1.65, 0])
        cl = T("cyclin", 24, ORANGE).move_to([-3.4, -0.9, 0])
        trace = sawtooth(p.xs, p.ys, 0, 0, 0, 0, [1, 2, 3])
        self.play(FadeIn(p.group), Create(flat), FadeIn(kl), FadeIn(cl), run_time=0.5)
        self.play(Create(trace), run_time=1.6, rate_func=linear)
        self.at("the next step")
        step = bchip("next step", GREEN, 26).move_to([4.7, 1, 0])
        arrow = arr([2.25, 1, 0], [3.55, 1, 0], GREEN)
        self.play(FadeIn(step), GrowArrow(arrow), run_time=0.5)
        self.at("destroys the cyclin")
        # The intact cyclin becomes separated schematic fragments.
        bits = VGroup(*[Rectangle(width=0.42, height=0.55, color=ORANGE, fill_opacity=0.3)
                        .move_to(dock + [dx, dy, 0]) for dx, dy in ((-0.5, 0.7), (0.4, 0.4), (-0.2, -0.6))])
        self.play(ReplacementTransform(b, bits), FadeOut(step), FadeOut(arrow), run_time=0.5)
        self.at("the kinase switches off")
        off = T("OFF", 30, RED, weight=BOLD).move_to(on)
        self.play(FadeOut(bits, shift=DOWN*0.3), *set_off(c), ReplacementTransform(on, off), run_time=0.5)
        self.at("the cycle resets")
        self.play(Indicate(trace, color=ORANGE), run_time=0.6)
        self.finish()


class S02Pairs(SpokenScene):
    def construct(self):
        ring = cycle_ring()
        self.at("Different cyclins")
        self.play(Create(ring[0]), FadeIn(ring[1]), run_time=0.8)
        d = radial_peak(PI/4)
        e = radial_peak(0)
        b = radial_peak(3*PI/4)
        dl = T("cyclin D", 28, ORANGE).move_to([4.6, 1.9, 0])
        el = T("cyclin E", 28, ORANGE).move_to([4.6, -0.6, 0])
        bl = T("cyclin B + CDK1", 28, ORANGE).move_to([-4.35, 2.4, 0])
        self.at("Cyclin D works")
        self.play(Create(d), FadeIn(dl), Indicate(ring[1][0], color=ORANGE), run_time=0.7)
        self.at("cyclin E drives")
        self.play(d.animate.set_stroke(opacity=0.35), Create(e), FadeIn(el), run_time=0.6)
        self.at("into S")
        dot = Dot([2.15, 0, 0], color=GREEN, radius=0.13)
        self.play(MoveAlongPath(dot, Arc(radius=2.15, start_angle=0, angle=-PI/4)), run_time=0.6)
        self.at("and cyclin B")
        self.play(FadeOut(dot), e.animate.set_stroke(opacity=0.35), Create(b), FadeIn(bl), run_time=0.6)
        self.at("drives mitosis")
        self.play(Indicate(ring[1][3], color=GREEN), run_time=0.6)
        self.at("the usual pattern")
        tag = bchip("usual pattern", GREY, 28).move_to([0, -3.2, 0])
        self.play(FadeIn(tag), run_time=0.5)
        self.finish()


class S03Brakes(SpokenScene):
    def construct(self):
        c, b = complex_at(-0.9, -0.15)
        c.flap.set_opacity(0)
        c.pocket.set_stroke(GREEN).set_fill(GREEN, 0.3)
        wee = bchip("Wee1", PURPLE, 30).move_to([-4.5, 2.4, 0])
        c25 = bchip("Cdc25", PURPLE, 30).move_to([4.3, 2.4, 0])
        self.at("The engine has brakes")
        self.play(FadeIn(c), FadeIn(b), run_time=0.6)
        self.at("We1 puts")
        pb = pbadge(0.26).move_to([-3.5, 1.9, 0])
        self.play(FadeIn(wee), FadeIn(pb), run_time=0.4)
        self.play(pb.animate.move_to(c.body.get_top()+DOWN*0.1), *set_off(c), run_time=0.65)
        self.at("and CDC25")
        self.play(FadeIn(c25), pb.animate.move_to([3.5, 1.7, 0]), run_time=0.5)
        self.play(FadeOut(pb), *set_on(c), run_time=0.35)
        self.at("Inhibitor proteins")
        inhibitor = RoundedRectangle(width=5.5, height=2.95, corner_radius=0.5, color=RED,
                                      stroke_width=7).move_to(VGroup(c, b))
        il = T("inhibitor", 28, RED).move_to([0, -2.25, 0])
        self.play(Create(inhibitor), FadeIn(il), run_time=0.6)
        self.at("bind and block")
        self.play(*set_off(c), inhibitor.animate.set_fill(RED, 0.08), run_time=0.4)
        self.at("Active CDK1")
        self.play(FadeOut(inhibitor), FadeOut(il), *set_on(c), run_time=0.4)
        self.at("switches on its activator")
        aa = arr([1.4, 1.2, 0], [3.5, 2.1, 0], GREEN)
        self.play(GrowArrow(aa), c25[1].animate.set_stroke(GREEN), run_time=0.5)
        self.at("switches off its brake")
        ib = bar_t([-1.8, 1.2, 0], [-3.8, 2.1, 0], RED)
        self.play(Create(ib), wee[1].animate.set_stroke(RED), run_time=0.5)
        self.at("once mitosis starts")
        switch = VMobject(stroke_color=GREEN, stroke_width=7).set_points_as_corners(
            [[-3.1,-2.8,0],[-0.8,-2.8,0],[-0.8,-1.9,0],[2.7,-1.9,0]])
        label = T("mitosis", 28, GREEN).move_to([4.2,-1.9,0])
        self.play(Create(switch), FadeIn(label), run_time=0.7)
        self.finish()


class S04Checkpoints(SpokenScene):
    def construct(self):
        center = np.array([-3.5, 0, 0])
        ring = cycle_ring(center)
        gates = VGroup(*[Line([x,y-0.34,0],[x,y+0.34,0],color=RED,stroke_width=9)
                         for x,y in ((-1.35,0),(-3.5,-2.15),(-5.65,0))])
        self.at("Checkpoints decide")
        self.play(FadeIn(ring), Create(gates), run_time=0.8)
        self.at("In G1")
        title = T("G1: commit?", 32, GREY, weight=BOLD).move_to([2.9, 2.5, 0])
        self.play(FadeIn(title), Indicate(gates[0], color=RED), run_time=0.4)
        nutrients = bchip("nutrients", GREY, 28).move_to([2.9, 1.2, 0])
        growth = bchip("growth factors", GREY, 28).move_to([2.9, -0.1, 0])
        self.at("enough nutrients")
        self.play(FadeIn(nutrients), run_time=0.4)
        self.at("and growth factors")
        go = T("commit", 30, GREEN).move_to([2.9, -1.5, 0])
        self.play(FadeIn(growth), FadeIn(go), gates[0].animate.rotate(PI/2).set_color(GREEN), run_time=0.6)
        self.at("If DNA is damaged")
        newtitle = T("G2: wait", 32, RED, weight=BOLD).move_to(title)
        # Broken paired bars are a DNA-status icon, not a molecular structure.
        dna = VGroup(Line([1.2,1.1,0],[2.6,1.1,0],color=TEAL,stroke_width=8),
                     Line([3.0,1.1,0],[4.4,1.1,0],color=TEAL,stroke_width=8),
                     T("damaged / not fully copied", 24, TEAL).move_to([2.9,0.4,0]))
        self.play(ReplacementTransform(title,newtitle), FadeOut(nutrients), FadeOut(growth), FadeOut(go),
                  FadeIn(dna), run_time=0.5)
        self.at("checkpoint signals")
        brakes = VGroup(bchip("Wee1",PURPLE,28), bchip("Cdc25",PURPLE,28)).arrange(RIGHT,buff=0.5).move_to([2.9,-1,0])
        signal = arr([2.9,0.05,0],[2.9,-0.55,0],RED)
        self.play(FadeIn(brakes), Create(signal), run_time=0.5)
        self.at("the cell waits")
        wait_label = T("brakes stay on", 28, RED).move_to([2.9,-2.2,0])
        self.play(Indicate(gates[1],color=RED), FadeIn(wait_label), run_time=0.5)
        self.at("In mitosis")
        mt = T("M: attachment check",32,RED,weight=BOLD).move_to(newtitle)
        self.play(ReplacementTransform(newtitle,mt),FadeOut(dna),FadeOut(brakes),FadeOut(signal),FadeOut(wait_label),run_time=0.5)
        chromosome = VGroup(*[RoundedRectangle(width=0.18,height=1.0,corner_radius=0.08,
                          color=GREY,fill_opacity=0.35).move_to([x,0.8,0]) for x in (2.7,3.0)])
        spindle = Line([0.5,0.8,0],[2.0,0.8,0],color=GREY,stroke_width=4)
        apc = bchip("APC/C",GREY,28).move_to([2.9,-1.0,0])
        stop = bar_t([2.9,0.05,0],[2.9,-0.55,0],RED)
        self.at("holds back destruction")
        self.play(FadeIn(chromosome),Create(spindle),FadeIn(apc),Create(stop),run_time=0.6)
        self.at("every chromosome is attached")
        self.play(spindle.animate.put_start_and_end_on([0.5,0.8,0],[2.6,0.8,0]),
                  FadeOut(stop),gates[2].animate.rotate(PI/2).set_color(GREEN),run_time=0.65)
        self.finish()


class S05Destroy(SpokenScene):
    def construct(self):
        apc = bchip("APC/C",GREY,32).move_to([-4.6,1.8,0])
        direction = arr([-5.4,3,0],[5.4,3,0],GREY,4)
        self.at("Destruction makes")
        self.play(GrowArrow(direction),run_time=0.6)
        self.at("A ubiquitin ligase")
        self.play(FadeIn(apc),run_time=0.5)
        securin = bchip("securin",GREY,30).move_to([-0.5,1.8,0])
        sisters = VGroup(*[RoundedRectangle(width=0.26,height=1.6,corner_radius=0.1,
                         color=GREY,fill_opacity=0.3).move_to([x,-0.3,0]) for x in (-0.7,-0.3)])
        self.at("tags succurin")
        tag = tag_badge().move_to(apc.get_right()+RIGHT*0.4)
        self.play(FadeIn(securin),FadeIn(sisters),FadeIn(tag),run_time=0.4)
        self.play(tag.animate.move_to(securin.get_top()+UP*0.18),run_time=0.5)
        self.at("sister chromatids can separate")
        self.play(FadeOut(securin),FadeOut(tag),sisters[0].animate.shift(LEFT*1.2),
                  sisters[1].animate.shift(RIGHT*1.2),run_time=0.8)
        self.at("and then cyclin B")
        c,b=complex_at(1.9,0.2)
        VGroup(c,b).scale(0.85)
        c.flap.set_opacity(0)
        c.pocket.set_stroke(GREEN).set_fill(GREEN,0.3)
        self.play(FadeOut(sisters),FadeIn(c),FadeIn(b),run_time=0.45)
        tag2=tag_badge().move_to(apc.get_right()+RIGHT*0.4)
        self.play(FadeIn(tag2),run_time=0.2)
        self.play(tag2.animate.move_to(b.get_top()+UP*0.18),run_time=0.5)
        self.at("which ends mitosis")
        self.play(FadeOut(b,shift=DOWN*0.4),FadeOut(tag2),*set_off(c),run_time=0.7)
        self.at("A cyclin that")
        self.play(FadeOut(apc),FadeOut(c),FadeOut(direction),run_time=0.35)
        tube=RoundedRectangle(width=2.5,height=3.3,corner_radius=0.6,color=GREY,
                              fill_color=GREEN,fill_opacity=0.12).move_to([-3.9,0.1,0])
        tl=T("frog egg extract",26,GREY).move_to([-3.9,-2.05,0])
        locked=locked_cyclin().move_to([-3.9,0.3,0])
        p=Plot(-0.7,5.9,-1.5,1.8,3,"time","cyclin level")
        high=Line([p.xs(0),p.ys(0.8),0],[p.xs(3),p.ys(0.8),0],color=ORANGE,stroke_width=7)
        self.play(FadeIn(tube),FadeIn(tl),FadeIn(locked),FadeIn(p.group),run_time=0.5)
        self.at("holds a frog")
        state=T("held in mitosis",30,GREEN,weight=BOLD).move_to([2.7,2.65,0])
        self.play(Create(high),FadeIn(state),run_time=0.7)
        self.at("Making cyclin drives entry")
        entry=T("making cyclin → entry",28,ORANGE).move_to([0,-2.65,0])
        self.play(FadeIn(entry),run_time=0.5)
        self.at("Destroying it permits exit")
        exit=T("destroying cyclin → exit",28,RED).move_to([0,-3.3,0])
        self.play(FadeIn(exit),run_time=0.5)
        self.finish()


class S06Once(SpokenScene):
    def construct(self):
        question=T("Copy again?",40,YELLOW,font=TITLE_FONT).move_to([0,2.9,0])
        self.at("The engine explains")
        self.play(FadeIn(question),run_time=0.5)
        left,right=-2.6,2.6
        cl,cr=cell_shape(left,0,4.3,3.6),cell_shape(right,0,4.3,3.6)
        nl,nr=nucleus(left,0.15,0.72,TEAL,0.35),nucleus(right,0.15,0.72)
        ll=T("copying",28,TEAL).move_to([left,-1.15,0])
        lr=T("not started",28,GREY).move_to([right,-1.15,0])
        self.at("Fuse a cell")
        self.play(FadeIn(cl),FadeIn(cr),FadeIn(nl),FadeIn(nr),FadeIn(ll),run_time=0.6)
        self.at("has not started")
        self.play(FadeIn(lr),run_time=0.4)
        self.at("the second nucleus")
        merged=cell_shape(0,0,10,3.6)
        self.play(ReplacementTransform(VGroup(cl,cr),merged),run_time=0.5)
        self.at("starts early")
        lr2=T("copying early",28,TEAL).move_to(lr)
        self.play(nr.animate.set_stroke(TEAL).set_fill(TEAL,0.35),ReplacementTransform(lr,lr2),run_time=0.5)
        self.at("Fuse it with")
        # Reset the result along with the new case, before revealing refusal.
        cl2,cr2=cell_shape(left,0,4.3,3.6),cell_shape(right,0,4.3,3.6)
        lr3=T("finished",28,GREY).move_to(lr2)
        self.play(ReplacementTransform(merged,VGroup(cl2,cr2)),nr.animate.set_stroke(GREY).set_fill(GREY,0.1),
                  ReplacementTransform(lr2,lr3),run_time=0.5)
        self.at("has finished")
        stamp=bchip("copied",GREY,24).move_to([right,1.35,0])
        self.play(FadeIn(stamp),run_time=0.35)
        self.at("that nucleus refuses")
        merged2=cell_shape(0,0,10,3.6)
        refused=T("refuses",28,RED).move_to(lr3)
        refusal_cross = cross_mark(nr.get_center(),0.35)
        self.play(ReplacementTransform(VGroup(cl2,cr2),merged2),ReplacementTransform(lr3,refused),
                  FadeIn(refusal_cross),run_time=0.65)
        self.at("once per cycle")
        rule=T("once per cycle",32,TEAL,weight=BOLD).move_to([0,-2.8,0])
        mitosis=bchip("mitosis",GREEN,26).move_to([-1,2.5,0])
        self.play(FadeOut(question), run_time=0.2)
        self.play(FadeIn(rule),FadeIn(mitosis),run_time=0.3)
        self.play(mitosis.animate.move_to([right,2.5,0]),run_time=0.5)
        reset = T("reset",28,GREY).move_to(refused)
        self.play(FadeOut(stamp),FadeOut(mitosis),FadeOut(refusal_cross),
                  ReplacementTransform(refused,reset),run_time=0.3)
        self.finish()


class S07Found(SpokenScene):
    def construct(self):
        heading=T("Three lines of work",36,font=TITLE_FONT).move_to([0,3,0])
        self.at("Three lines of work")
        self.play(FadeIn(heading),run_time=0.5)
        specs=(("frog oocyte","MPF",YELLOW,-4.6),
               ("yeast mutants","cdc2",BLUE,0),
               ("sea urchin","cyclin",ORANGE,4.6))
        threads=[]
        for name,value,color,x in specs:
            source=T(name,26,GREY).move_to([x,1.9,0])
            result=bchip(value,color,32).move_to([x,0.75,0])
            threads.append(VGroup(source,result))
        self.at("Frog")
        self.play(FadeIn(threads[0][0]),run_time=0.4)
        self.at("an activity")
        self.play(FadeIn(threads[0][1]),run_time=0.4)
        self.at("Yeast mutants")
        self.play(FadeIn(threads[1]),run_time=0.6)
        self.at("Sea urchins")
        self.play(FadeIn(threads[2]),run_time=0.6)
        self.at("Then the lines met")
        lines=VGroup(*[arr([x,0.15,0],[0,-1.1,0],color,4) for _,_,color,x in specs])
        mpf=bchip("MPF",YELLOW,38).move_to([0,-1.9,0])
        self.play(Create(lines),FadeIn(mpf),run_time=0.6)
        self.at("MPF is Cdc2")
        c,b=complex_at(-1.25,-0.7,"Cdc2","cyclin B")
        self.play(FadeOut(heading),FadeOut(lines),*[FadeOut(t) for t in threads],
                  ReplacementTransform(mpf,c),run_time=0.65)
        self.at("now called")
        label=T("CDK1",32,BLUE,weight=BOLD).move_to(c.lab)
        self.play(Transform(c.lab,label),run_time=0.45)
        self.at("bound to cyclin B")
        dock=b.get_center().copy()
        b.shift(RIGHT*2)
        self.play(FadeIn(b),run_time=0.3)
        self.play(b.animate.move_to(dock),*set_on(c),run_time=0.65)
        name=T("MPF",36,YELLOW,weight=BOLD).move_to([0,2.1,0])
        self.play(FadeIn(name),run_time=0.3)
        self.finish()


class S08End(EndCard):
    LINE = "Making cyclin drives entry. Destroying it permits exit."
