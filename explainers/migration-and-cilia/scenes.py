"""How Internal Motion Becomes Movement.

COLOR MAP
  TEAL    actin network / speckles
  YELLOW  polymer addition and dynein motion
  GREEN   visible output / edge advance
  BLUE    complete A-tubule
  PURPLE  incomplete B-tubule
  ORANGE  mechanical constraints: clutch, links, anchor
  MAGENTA motor control
  GREY    membrane, substrate, structure
  RED     released or cut constraint

All diagrams are explicitly schematic.  The crawling and axoneme machines keep
the same landmarks whenever the split workbench returns.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
MAGENTA = "#E65AA3"


class WorkbenchScene(SpokenScene):
    """Shared visual world: a broad, slowly moving schematic workbench."""
    def setup(self):
        super().setup()
        surface, rail = workbench_background()
        rail.phase = 0.0
        def move_rail(m, dt):
            m.phase += dt
            # Keep ambient motion below every readable label and diagram.
            m.move_to([0, -3.55 + .30*np.sin(1.20*m.phase), 0])
        rail.add_updater(move_rail)
        self.add(surface, rail)


def arrow(a, b, color=TEXT, width=6, tip=0.22):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=width,
                 tip_length=tip, max_tip_length_to_length_ratio=0.4)


def workbench_background():
    surface = RoundedRectangle(width=13.1, height=6.45, corner_radius=.24,
                               stroke_color=GREY, stroke_width=2,
                               fill_color=GREY, fill_opacity=.18).set_z_index(-20)
    rail = Line([-6.35, -3.47, 0], [6.35, -3.47, 0], color=TEAL,
                stroke_width=8).set_opacity(.23).set_z_index(-19)
    return VGroup(surface, rail)


def small_label(text="schematic", point=(0, 0, 0)):
    return T(text, 28, GREY).move_to(point)


def add_drift(scene, x0, x1, y, color=TEAL, speed=-0.85, count=12):
    """Visible speckles that drift during narration without changing the claim."""
    dots = VGroup(*[Dot([x0 + (x1-x0)*i/max(1, count-1), y + 0.14*np.sin(i), 0],
                        radius=0.10, color=color) for i in range(count)])
    def drift(m, dt):
        for d in m:
            d.shift(RIGHT * speed * dt)
            if speed < 0 and d.get_x() < x0:
                d.shift(RIGHT * (x1-x0))
            if speed > 0 and d.get_x() > x1:
                d.shift(LEFT * (x1-x0))
    dots.add_updater(drift)
    scene.add(dots)
    return dots


def crawler(center=(-3.45, -0.15, 0), scale=1.0, clutch=False, released=False):
    """The carried left-hand machine, always at the same workbench landmark."""
    cx, cy, _ = center
    substrate = Line([cx-2.6*scale, cy-1.25*scale, 0], [cx+2.6*scale, cy-1.25*scale, 0],
                     color=GREY, stroke_width=9)
    ticks = VGroup(*[Line([cx+x*scale, cy-1.38*scale, 0], [cx+x*scale, cy-1.12*scale, 0],
                              color=GREY, stroke_width=3) for x in np.linspace(-2.3, 2.3, 9)])
    membrane = Line([cx-2.5*scale, cy+1.15*scale, 0], [cx+2.25*scale, cy+1.15*scale, 0],
                    color=GREY, stroke_width=12)
    mesh = VGroup()
    for y in (-0.65, -0.15, 0.35, 0.8):
        mesh.add(Line([cx-2.25*scale, cy+y*scale, 0], [cx+1.75*scale, cy+(y+0.18)*scale, 0],
                      color=TEAL, stroke_width=7))
    for x in (-1.7, -0.8, 0.1, 1.0):
        mesh.add(Line([cx+x*scale, cy-0.72*scale, 0], [cx+(x+0.45)*scale, cy+0.92*scale, 0],
                      color=TEAL, stroke_width=4).set_opacity(0.75))
    additions = VGroup(*[Square(0.20*scale, stroke_width=0, fill_color=YELLOW, fill_opacity=1)
                         .move_to([cx+(1.86+0.21*i)*scale, cy+(0.48+0.20*i)*scale, 0]) for i in range(3)])
    edge = Line([cx+2.25*scale, cy+1.15*scale, 0], [cx+2.25*scale, cy-0.15*scale, 0],
                color=GREEN, stroke_width=13)
    g = VGroup(substrate, ticks, membrane, mesh, additions, edge)
    if clutch or released:
        parts = VGroup()
        for x in (-0.9, 0.2, 1.2):
            col = RED if released else ORANGE
            stem = Line([cx+x*scale, cy+0.35*scale, 0], [cx+x*scale, cy-1.15*scale, 0],
                        color=col, stroke_width=7)
            grip = VGroup(Line([cx+(x-.20)*scale, cy-1.02*scale, 0], [cx+x*scale, cy-1.22*scale, 0], color=col, stroke_width=5),
                          Line([cx+(x+.20)*scale, cy-1.02*scale, 0], [cx+x*scale, cy-1.22*scale, 0], color=col, stroke_width=5))
            parts.add(stem, grip)
        g.add(parts)
    return g


def doublet_cross(radius=0.36, rotation=0.0):
    """One doublet: a complete blue A circle fused to an incomplete purple B arc."""
    rb = radius * 0.78
    b_center = np.array([np.cos(rotation), np.sin(rotation), 0]) * radius * 1.35
    b = Arc(radius=rb, start_angle=rotation-2.0, angle=4.0,
            stroke_color=PURPLE, stroke_width=5).move_arc_center_to(b_center)
    a = Circle(radius=radius, color=BLUE, stroke_width=5, fill_color=BLUE, fill_opacity=0.20)
    return VGroup(b, a)


def ring_axoneme(center=(3.45, -0.15, 0), radius=1.65):
    cx, cy, _ = center
    outline = Circle(radius=radius+0.55, color=GREY, stroke_width=4,
                     fill_color=GREY, fill_opacity=0.04).move_to(center)
    ds = VGroup()
    for i in range(9):
        a = PI/2 + TAU*i/9
        d = doublet_cross(0.25, a-PI/2)
        d.shift(np.array([cx+radius*np.cos(a), cy+radius*np.sin(a), 0]) - d[1].get_center())
        ds.add(d)
    cp = VGroup(Circle(0.22, color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=.25),
                Circle(0.22, color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=.25))
    cp.arrange(RIGHT, buff=.09).move_to(center)
    return VGroup(outline, ds, cp)


def long_pair(origin=(1.1, -1.0, 0), length=5.0, offset=0.62, slide=0.0,
              curved=0.0, links=True, anchor=True):
    """Two neighboring doublets in side view; curvature is computed from circular arcs."""
    o = np.array(origin, float)
    def p(s, off):
        if abs(curved) < 1e-6:
            return o + [s, off, 0]
        return o + [np.sin(curved*s)/curved - off*np.sin(curved*s),
                    (1-np.cos(curved*s))/curved + off*np.cos(curved*s), 0]
    lo = ParametricFunction(lambda t: p(t, -offset/2), t_range=[0, length, .04], color=BLUE, stroke_width=22)
    hi = ParametricFunction(lambda t: p(t+slide, offset/2), t_range=[0, length, .04], color=PURPLE, stroke_width=22)
    g = VGroup(lo, hi)
    if links:
        for s in np.linspace(0.9, length-0.7, 4):
            g.add(Line(p(s, -offset/2), p(s, offset/2), color=ORANGE, stroke_width=5))
    if anchor:
        g.add(RoundedRectangle(width=.35, height=1.35, corner_radius=.08,
                               color=ORANGE, stroke_width=4, fill_color=ORANGE,
                               fill_opacity=.35).move_to(o+[-.12, 0, 0]))
    return g


def split_bench(clutch=True, links=True):
    divider = Line([0, -2.35, 0], [0, 2.85, 0], color=GREY, stroke_width=2).set_opacity(.55)
    left = crawler(clutch=clutch)
    right = long_pair(origin=(.7, -1.0, 0), length=5.3, links=links, curved=.10 if links else 0)
    return VGroup(divider, left, right)


class S00Hook(WorkbenchScene, TitleCard):
    LESSON = "Cell shape, migration and cilia"
    TITLE = "How Internal Motion Becomes Movement"

    def construct(self):
        bench = split_bench(clutch=False, links=False)
        schem = small_label(point=(0, -2.8, 0))
        q1 = T("?", 64, TEXT).move_to([-1.0, 1.25, 0])
        q2 = T("?", 64, TEXT).move_to([5.9, 1.25, 0])
        back = arrow([-2.2, 2.1, 0], [-4.7, 2.1, 0], TEAL)
        fwd = arrow([-4.6, 2.65, 0], [-2.0, 2.65, 0], GREEN)
        slide = arrow([1.3, 2.1, 0], [3.4, 2.1, 0], YELLOW)
        bend = CurvedArrow([4.0, 1.8, 0], [5.4, 2.65, 0], angle=-.6, color=GREEN, stroke_width=6)
        self.play(FadeIn(bench), FadeIn(schem), run_time=.8)
        add_drift(self, -5.5, -1.4, -.05)
        self.at("actin move backward")
        self.play(GrowArrow(back), GrowArrow(fwd), FadeIn(q1), run_time=1.4)
        self.at("microtubules slide lengthwise")
        self.play(GrowArrow(slide), Create(bend), FadeIn(q2), run_time=1.4)
        self.at("Both puzzles start")
        title = T(self.TITLE, 34, font=TITLE_FONT).move_to([0, 3.55, 0])
        self.play(FadeOut(q1), FadeOut(q2), FadeIn(title), run_time=1.0)
        self.finish()


class S01OneWorld(WorkbenchScene):
    def construct(self):
        bench = split_bench(clutch=True, links=True)
        title = T("How Internal Motion Becomes Movement", 36, font=TITLE_FONT).move_to([0, 3.55, 0])
        labels = VGroup(T("crawling edge", 30, TEAL).move_to([-3.45, 2.55, 0]),
                        T("motile axoneme", 30, BLUE).move_to([3.45, 2.55, 0]))
        self.play(FadeIn(bench), FadeIn(title), run_time=.8)
        add_drift(self, -5.5, -1.4, -.05)
        self.at("both machines")
        self.play(FadeIn(labels), title.animate.scale(.8).move_to([0, 3.55, 0]), run_time=.8)
        motors = VGroup(arrow([-4.8, 1.9, 0], [-2.6, 1.9, 0], YELLOW),
                        arrow([1.1, 1.8, 0], [3.2, 1.8, 0], YELLOW))
        self.at("polymers and motors")
        self.play(LaggedStart(*[GrowArrow(a) for a in motors], lag_ratio=.35), run_time=1.3)
        constraint = chip("constraint", ORANGE, 28).move_to([0, -2.75, 0])
        self.at("changes one constraint")
        self.play(FadeIn(constraint, shift=UP*.15), Indicate(bench[2][2:], color=ORANGE), run_time=1.2)
        self.at("what it leaves out")
        self.play(constraint.animate.set_color(MAGENTA), run_time=.8)
        self.finish()


class S02Polymerization(WorkbenchScene):
    def construct(self):
        c = crawler(center=(-.45, -.15, 0), scale=1.25)
        dim_ax = ring_axoneme((5.2, -.1, 0), .7).set_opacity(.18)
        self.play(FadeIn(c), FadeIn(dim_ax), run_time=.8)
        specks = add_drift(self, -3.4, 1.8, -.25, speed=-.15, count=9)
        lam = T("lamellipodium", 34, TEAL).move_to([-.45, 2.75, 0])
        self.at("thin actin")
        self.play(FadeIn(lam), Indicate(c[3], color=TEAL), run_time=1.0)
        blocks = VGroup(*[Square(.26, stroke_width=0, fill_color=YELLOW, fill_opacity=1)
                          .move_to([2.05+.28*i, .45+.25*i, 0]) for i in range(3)])
        self.at("Actin subunits extend")
        self.play(LaggedStart(*[FadeIn(b, shift=LEFT*.2) for b in blocks], lag_ratio=.25),
                  c[5].animate.shift(RIGHT*.3), run_time=2.0)
        ruler = T("substrate", 30, GREY).move_to([-.45, -2.45, 0])
        self.at("substrate is the surface")
        self.play(FadeIn(ruler), Indicate(c[0], color=GREY), run_time=1.0)
        out = arrow([-.2, 2.0, 0], [2.15, 2.0, 0], GREEN)
        self.at("edge moves forward")
        self.play(GrowArrow(out), c[5].animate.shift(RIGHT*.28), run_time=1.4)
        self.finish()


class S03Balance(WorkbenchScene):
    def construct(self):
        c = crawler(center=(-1.3, .55, 0), scale=.92)
        self.add(c)
        specks = add_drift(self, -3.35, .25, .45, speed=-.95, count=12)
        ruler = T("substrate frame", 28, GREY).move_to([-1.3, -1.28, 0])
        self.at("speckles reveal")
        self.play(FadeIn(ruler), Indicate(specks, color=TEAL), run_time=1.0)
        retro = arrow([-.2, -.25, 0], [-2.7, -.25, 0], TEAL)
        retro_l = T("retrograde flow", 30, TEAL).move_to([2.7, -.25, 0])
        self.at("retrograde flow")
        self.play(GrowArrow(retro), FadeIn(retro_l), run_time=1.0)
        base_y = -2.25
        poly = Rectangle(width=4.3, height=.42, color=YELLOW, fill_color=YELLOW, fill_opacity=.55).move_to([-1.7, base_y, 0])
        minus = T("−", 48, TEXT).move_to([.85, base_y, 0])
        flow = Rectangle(width=2.2, height=.42, color=TEAL, fill_color=TEAL, fill_opacity=.55).move_to([2.35, base_y, 0])
        self.at("polymerization adds")
        self.play(GrowFromEdge(poly, LEFT), run_time=1.1)
        self.at("retrograde flow subtracts")
        self.play(FadeIn(minus), GrowFromEdge(flow, RIGHT), run_time=1.1)
        eq = T("=", 44, TEXT).move_to([3.85, base_y, 0])
        edge = Rectangle(width=1.35, height=.42, color=GREEN, fill_color=GREEN, fill_opacity=.65).move_to([4.85, base_y, 0])
        cap = VGroup(T("polymerization", 28, YELLOW).move_to([-1.7, -2.78, 0]),
                     T("flow", 28, TEAL).move_to([2.35, -2.78, 0]),
                     T("edge speed", 28, GREEN).move_to([4.85, -2.78, 0]))
        self.play(FadeIn(eq), GrowFromEdge(edge, LEFT), FadeIn(cap), run_time=1.0)
        net = T("network frame", 28, TEAL).move_to([-1.3, 2.45, 0])
        self.at("Growth is measured")
        self.play(FadeIn(net), Indicate(c[3], color=TEAL), run_time=.9)
        self.at("edge and flow")
        self.play(Indicate(ruler, color=GREY), run_time=.9)
        self.finish()


class S04Clutch(WorkbenchScene):
    def construct(self):
        c = crawler(center=(0, .35, 0), scale=1.05)
        self.add(c)
        specks = add_drift(self, -2.45, 1.8, .15, speed=-.9, count=12)
        integrins = VGroup()
        for x in (-1.0, .2, 1.35):
            receptor = RoundedRectangle(width=.34, height=.75, corner_radius=.12, color=ORANGE,
                                        fill_color=ORANGE, fill_opacity=.35).move_to([x, .45, 0])
            linker = Line([x, .12, 0], [x-.35, -.55, 0], color=ORANGE, stroke_width=6)
            grip = Line([x-.3, -1.0, 0], [x+.3, -1.0, 0], color=ORANGE, stroke_width=8)
            integrins.add(VGroup(receptor, linker, grip))
        self.at("integrin is")
        self.play(LaggedStart(*[FadeIn(i, shift=UP*.2) for i in integrins], lag_ratio=.2), run_time=1.5)
        labs = VGroup(T("integrin", 28, ORANGE).move_to([-3.6, .65, 0]),
                      T("linker", 28, ORANGE).move_to([-3.6, -.05, 0]))
        self.at("linker proteins")
        self.play(FadeIn(labs), run_time=.8)
        clutch = chip("clutch", ORANGE, 32).move_to([4.55, .45, 0])
        self.at("like a clutch")
        self.play(FadeIn(clutch), Indicate(integrins, color=ORANGE), run_time=1.0)
        engine = arrow([-1.5, 2.4, 0], [1.4, 2.4, 0], YELLOW)
        eng_l = T("polymerization engine", 28, YELLOW).next_to(engine, UP, buff=.12)
        self.at("Polymerization is the engine")
        self.play(GrowArrow(engine), FadeIn(eng_l), run_time=1.2)
        self.at("adhesion transmits")
        self.play(integrins.animate.set_fill(ORANGE, .75), specks.animate.set_opacity(.75), run_time=1.2)
        specks.set_opacity(.72)
        edge = arrow([2.4, 1.55, 0], [5.5, 1.55, 0], GREEN)
        self.at("reduce backward slip")
        self.play(GrowArrow(edge), run_time=1.3)
        self.at("edge advance")
        self.play(c[5].animate.shift(RIGHT*.45), Indicate(edge, color=GREEN), run_time=1.0)
        self.finish()


class S05Axoneme(WorkbenchScene):
    def construct(self):
        shaft = ParametricFunction(lambda t: np.array([-5.3+1.1*np.sin(.35*t), -2.4+t, 0]),
                                   t_range=[0, 5.3, .04], color=GREY, stroke_width=22)
        # Begin with the projection already visible so narration never starts on an empty bench.
        shaft.set_opacity(.30)
        self.add(shaft)
        self.play(shaft.animate.set_opacity(1), run_time=1.2)
        def gentle_beat(m, dt):
            m.rotate(.025*np.cos(1.15*self.renderer.time)*dt,
                     about_point=np.array([-5.3, -2.4, 0]))
        shaft.add_updater(gentle_beat)
        cil = T("motile cilium", 34, TEXT).move_to([-1.7, 2.8, 0])
        self.at("hair -like projection")
        self.play(FadeIn(cil), shaft.animate.set_color(BLUE), run_time=1.0)
        ring = ring_axoneme((1.85, .15, 0), 1.7)
        ax = T("axoneme", 34, BLUE).move_to([1.85, 2.75, 0])
        self.at("axoneme is")
        self.play(FadeIn(ring[0]), FadeIn(ax), run_time=.8)
        self.at("classic 9")
        self.play(LaggedStart(*[FadeIn(d, scale=.6) for d in ring[1]], lag_ratio=.08), run_time=1.5)
        nine = M("9 + 2", 42, TEXT).move_to([5.25, 2.0, 0])
        self.at("nine doublets")
        self.play(FadeIn(ring[2]), FadeIn(nine), run_time=1.0)
        zoom = doublet_cross(.6, 0).move_to([5.1, -.85, 0])
        al = T("A: complete", 28, BLUE).move_to([5.0, -2.05, 0])
        bl = T("B: incomplete", 28, PURPLE).move_to([5.0, -2.58, 0])
        self.at("Each doublet")
        self.play(FadeIn(zoom, scale=.5), FadeIn(al), run_time=1.0)
        self.at("incomplete B tubule")
        self.play(FadeIn(bl), Indicate(zoom[0], color=PURPLE), run_time=.9)
        self.add(small_label(point=(0, -2.8, 0)))
        self.finish()


class S06Dynein(WorkbenchScene):
    def construct(self):
        pair = long_pair(origin=(-5.5, -.35, 0), length=10.1, links=False, anchor=False)
        base = T("base", 28, GREY).move_to([-5.4, -1.5, 0])
        tip = T("tip", 28, GREY).move_to([4.6, -1.5, 0])
        self.add(pair, base, tip)
        add_drift(self, -4.9, 4.2, -.05, color=YELLOW, speed=-1.05, count=13)
        arms = VGroup()
        for x in np.linspace(-4.2, 3.8, 6):
            arms.add(VGroup(Line([x, -.62, 0], [x+.35, -.03, 0], color=YELLOW, stroke_width=7),
                            Dot([x+.35, -.03, 0], .13, color=YELLOW)))
        self.at("motors slide")
        self.play(LaggedStart(*[FadeIn(a, shift=UP*.15) for a in arms], lag_ratio=.12), run_time=1.4)
        a_lab = T("anchored on A", 28, BLUE).move_to([-3.4, -2.4, 0])
        b_lab = T("grips B", 28, PURPLE).move_to([2.3, .95, 0])
        self.at("arms anchor")
        self.play(FadeIn(a_lab), run_time=.7)
        self.at("grip the neighbor")
        self.play(FadeIn(b_lab), Indicate(arms, color=YELLOW), run_time=.9)
        head = arrow([1.1, 2.0, 0], [-1.7, 2.0, 0], YELLOW)
        head_l = T("head → base", 30, YELLOW).next_to(head, UP, buff=.12)
        self.at("head steps")
        self.play(GrowArrow(head), FadeIn(head_l), run_time=1.2)
        motion = arrow([-.5, -2.30, 0], [2.7, -2.30, 0], GREEN)
        mot_l = T("neighbor → tip", 30, GREEN).next_to(motion, DOWN, buff=.12)
        self.at("Seen from the other side")
        self.play(GrowArrow(motion), FadeIn(mot_l), pair[1].animate.shift(RIGHT*.7), run_time=1.5)
        self.finish()


class S07Bending(WorkbenchScene):
    def construct(self):
        k = ValueTracker(0.0)
        slide = ValueTracker(0.0)
        linked = always_redraw(lambda: long_pair(origin=(-5.6, -1.25, 0), length=10.2,
                                                  slide=slide.get_value(), curved=k.get_value(), links=True))
        self.add(linked, small_label("simple schematic", (0, -2.8, 0)))
        self.at("two neighboring doublets")
        title = T("two neighboring doublets", 32, TEXT).move_to([0, 2.8, 0])
        self.play(FadeIn(title), run_time=.7)
        add_drift(self, -4.9, 4.2, -.9, color=YELLOW, speed=.9, count=12)
        free = T("free: pass one another", 30, YELLOW).move_to([0, 2.1, 0])
        self.at("Free doublets")
        self.play(FadeIn(free), slide.animate.set_value(.9), run_time=1.4)
        shear = chip("shear = lengthwise offset", YELLOW, 30).move_to([0, 1.35, 0])
        self.at("shear")
        self.play(FadeIn(shear), run_time=.8)
        self.at("links that resist sliding")
        resist = T("links resist sliding", 30, ORANGE).move_to([3.7, .65, 0])
        anchor = T("base anchor", 28, ORANGE).move_to([-4.65, .65, 0])
        self.play(FadeIn(resist), FadeIn(anchor), slide.animate.set_value(0), run_time=1.2)
        bend = T("sliding → bending", 36, GREEN).move_to([-2.1, 2.85, 0])
        self.at("turn sliding into bending")
        self.play(FadeOut(title), FadeOut(free), FadeOut(shear), k.animate.set_value(.085), FadeIn(bend), run_time=2.1)
        motors = VGroup(*[Dot([-3.8+1.45*i, -.7, 0], .11, color=YELLOW) for i in range(6)])
        self.at("motors stay unchanged")
        self.play(FadeIn(motors), Indicate(motors, color=YELLOW), run_time=1.0)
        self.finish()


class S08MotorControl(WorkbenchScene):
    def construct(self):
        ring = ring_axoneme((-2.2, -.1, 0), 1.75)
        base = RoundedRectangle(width=.45, height=4.8, corner_radius=.08, color=ORANGE,
                                fill_color=ORANGE, fill_opacity=.35).move_to([-4.5, -.1, 0])
        links = VGroup(*[Line([-3.6, -1.5+.75*i, 0], [-3.05, -1.5+.75*i, 0], color=ORANGE, stroke_width=5) for i in range(5)])
        self.add(ring, base, links)
        left_m = VGroup(*[Dot([-3.35, -1.35+.24*i, 0], .12, color=YELLOW) for i in range(12)])
        right_m = VGroup(*[Dot([-.95, -1.35+.24*i, 0], .12, color=YELLOW).set_opacity(.2) for i in range(12)])
        def active_step(m, dt):
            for d in m:
                d.shift(UP*.78*dt)
                if d.get_y() > 1.38:
                    d.shift(DOWN*2.76)
        left_m.add_updater(active_step)
        self.at("opposite sides")
        self.play(FadeIn(left_m), FadeIn(right_m), run_time=1.0)
        dial = Circle(.78, color=MAGENTA, stroke_width=5, fill_color=MAGENTA, fill_opacity=.12).move_to([3.65, .35, 0])
        needle = Line(dial.get_center(), dial.get_center()+UP*.62+LEFT*.2, color=MAGENTA, stroke_width=7)
        dl = T("which motors\nare active", 30, MAGENTA, line_spacing=.85).move_to([3.65, -1.05, 0])
        self.at("Motor control")
        self.play(Create(dial), GrowFromPoint(needle, dial.get_center()), FadeIn(dl), run_time=1.2)
        curve = CurvedArrow([-.2, 2.3, 0], [1.2, 1.1, 0], angle=-.55, color=GREEN, stroke_width=7)
        self.at("which side is more active")
        self.play(Indicate(left_m, color=YELLOW), Create(curve), run_time=1.2)
        self.at("constraint shapes")
        self.play(Indicate(VGroup(base, links), color=ORANGE), run_time=.9)
        self.at("regulation helps")
        self.play(Rotate(needle, PI/3, about_point=dial.get_center()), curve.animate.shift(DOWN*.25), run_time=1.1)
        self.finish()


def prediction_frame():
    bench = split_bench(clutch=True, links=True)
    q = T("What happens to edge advance and to the doublets?", 34, font=TITLE_FONT).move_to([0, 3.55, 0])
    unlock = VGroup(*[T("×", 40, RED).move_to([-4.3+i*1.1, -1.15, 0]) for i in range(3)])
    cuts = VGroup(*[T("×", 40, RED).move_to([1.6+i*1.15, -.9+.12*i, 0]) for i in range(4)])
    return VGroup(bench, q, unlock, cuts)


class S09Predict(WorkbenchScene):
    def construct(self):
        frame = prediction_frame()
        # Carry the split bench in immediately; no empty opening while the question begins.
        self.add(frame[0])
        add_drift(self, -5.5, -1.4, -.05, speed=-.08)
        self.at("motion generators")
        self.play(Indicate(frame[0][1][3], color=TEAL), Indicate(frame[0][2][0:2], color=YELLOW), run_time=.9)
        self.at("Release the crawling clutch")
        self.play(FadeIn(frame[2]), run_time=.8)
        self.at("cut the aximal links")
        self.play(FadeIn(frame[3]), run_time=.8)
        self.at("What happens")
        self.play(Write(frame[1]), run_time=1.2)
        self.finish()


class S10Pause(Scene):
    def construct(self):
        # Rebuild the preceding WorkbenchScene background exactly for the thinking pause.
        self.camera.background_color = BG
        background = workbench_background()
        pause_rail = background[1]
        pause_rail.phase = 0.0
        def move_pause_rail(m, dt):
            m.phase += dt
            m.move_to([0, -3.55 + .30*np.sin(1.20*m.phase), 0])
        pause_rail.add_updater(move_pause_rail)
        self.add(background)
        frame = prediction_frame()
        self.add(frame)
        # Tiny shimmer preserves the poised frame without revealing either answer.
        glow = VGroup(*[Dot([-4.8+i*.65, -.1+.08*np.sin(i), 0], .05, color=TEAL) for i in range(6)],
                      *[Dot([1.4+i*.72, -.35, 0], .05, color=YELLOW) for i in range(6)])
        glow.add_updater(lambda m, dt: m.set_opacity(.45+.25*np.sin(self.renderer.time*2.2)))
        self.add(glow)
        self.wait(4.5)


class S11Reveal(WorkbenchScene):
    def construct(self):
        divider = Line([0, -2.35, 0], [0, 2.85, 0], color=GREY, stroke_width=2)
        left = crawler(clutch=False, released=True)
        right = long_pair(origin=(.7, -1, 0), length=5.3, links=False, anchor=True)
        self.add(divider, left, right)
        specks = add_drift(self, -5.5, -1.4, -.05, speed=-1.1, count=13)
        self.at("more act")
        back = arrow([-2.1, 2.0, 0], [-5.15, 2.0, 0], TEAL)
        self.play(GrowArrow(back), run_time=1.2)
        short = arrow([-4.6, 2.65, 0], [-3.35, 2.65, 0], GREEN)
        self.at("edge advances less")
        self.play(GrowArrow(short), run_time=1.0)
        slide = arrow([1.2, 2.0, 0], [4.6, 2.0, 0], YELLOW)
        self.at("links cut")
        self.play(FadeIn(VGroup(*[T("×", 40, RED).move_to([1.7+i, -.55, 0]) for i in range(4)])), run_time=.7)
        self.at("doublets slide apart")
        self.play(GrowArrow(slide), right[1].animate.shift(RIGHT*.3), run_time=1.5)
        still = T("motors still work", 30, YELLOW).move_to([3.4, 2.75, 0])
        self.at("motors still work")
        self.play(FadeIn(still), Indicate(slide, color=YELLOW), run_time=.9)
        changed = chip("changed constraint → different output", ORANGE, 30).move_to([0, -2.6, 0])
        self.at("changed constraint")
        self.play(FadeIn(changed, shift=UP*.15), run_time=1.0)
        self.finish()


class S12Scope(WorkbenchScene):
    def construct(self):
        left = crawler(center=(-4.55, -.25, 0), scale=.64, clutch=True)
        right = long_pair(origin=(2.2, -1.15, 0), length=3.7, curved=.14, links=True)
        self.play(FadeIn(left), FadeIn(right), run_time=.8)
        add_drift(self, -6.0, -3.2, -.25, speed=-.13, count=6)
        head = T("shared logic ≠ every detail", 34, font=TITLE_FONT).move_to([0, 2.7, 0])
        self.at("share a logic")
        self.play(FadeIn(head), run_time=.8)
        internal = chip("internal motion", YELLOW, 30).move_to([-4.2, 1.75, 0])
        gate = chip("constraint", ORANGE, 30).move_to([0, 1.75, 0])
        dial = chip("motor control", MAGENTA, 30).move_to([0, .55, 0])
        output = chip("visible output", GREEN, 30).move_to([4.25, 1.75, 0])
        a1 = arrow(internal.get_right(), gate.get_left(), TEXT)
        a2 = arrow(gate.get_right(), output.get_left(), GREEN)
        self.at("Polymers and motors")
        self.play(FadeIn(internal), run_time=.8)
        self.at("internal relative motion")
        self.play(GrowArrow(a1), FadeIn(gate), run_time=1.0)
        self.at("mechanical constraint")
        self.play(Indicate(gate, color=ORANGE), run_time=.9)
        outcomes = VGroup(T("slips", 28, TEAL), T("advances", 28, GREEN),
                          T("slides apart", 28, YELLOW), T("bends", 28, BLUE)).arrange(RIGHT, buff=.55).move_to([0, -2.55, 0])
        self.at("motion slips")
        self.play(GrowArrow(a2), FadeIn(output), FadeIn(outcomes[0]), run_time=.9)
        self.at("advances")
        self.play(FadeIn(outcomes[1]), run_time=.5)
        self.at("slides apart")
        self.play(FadeIn(outcomes[2]), run_time=.5)
        self.at("bends")
        self.play(FadeIn(outcomes[3]), run_time=.5)
        self.at("constraints and motor control")
        self.play(FadeIn(dial), Indicate(VGroup(gate, dial), color=ORANGE), run_time=1.0)
        self.at("visible output")
        self.play(Indicate(output, color=GREEN), left.animate.shift(RIGHT*.12), right.animate.rotate(.035, about_point=[2.2,-1.15,0]), run_time=1.2)
        self.finish()


class S13End(EndCard):
    LINE = "Constraints and motor control shape internal motion into visible movement."
