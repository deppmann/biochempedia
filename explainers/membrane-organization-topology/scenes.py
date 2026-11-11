"""Which Side Is Outside? — membrane topology as one carried visual world.

COLOR MAP
  GREY   membranes and neutral structure
  GOLD   cytosol and the cytosol-facing membrane edge
  TEAL   route lumens and outside
  BLUE   the membrane-spanning protein
  YELLOW the N terminus
  GREEN  the C terminus
  ORANGE sugar
  RED    a forbidden membrane crossing
"""
import math
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
CYTO = GOLD
LUMEN = TEAL
MEM = GREY


def P(x, y):
    return np.array([x, y, 0.0])


def double_line(x0, x1, y, gap=0.16, color=MEM, width=6):
    return VGroup(Line(P(x0, y - gap / 2), P(x1, y - gap / 2), color=color, stroke_width=width),
                  Line(P(x0, y + gap / 2), P(x1, y + gap / 2), color=color, stroke_width=width))


def moving_specks(seed=1, count=72, area=(-6.5, 6.5, -3.45, 2.2)):
    """One visual object: a continuously drifting cytosol field."""
    rng = np.random.RandomState(seed)
    x0, x1, y0, y1 = area
    dots = VGroup()
    for _ in range(count):
        d = Dot(P(rng.uniform(x0, x1), rng.uniform(y0, y1)), radius=rng.uniform(.045, .085), color=CYTO)
        d.set_opacity(rng.uniform(.24, .52))
        d.v = P(rng.uniform(-.18, .20), rng.uniform(.11, .24))

        def drift(m, dt, x0=x0, x1=x1, y0=y0, y1=y1):
            m.shift(m.v * dt)
            if m.get_y() > y1: m.shift(DOWN * (y1 - y0))
            if m.get_x() > x1: m.shift(LEFT * (x1 - x0))
            if m.get_x() < x0: m.shift(RIGHT * (x1 - x0))
        d.add_updater(drift)
        dots.add(d)
    return dots


def schematic_tag():
    return T("schematic", 28, GREY).to_corner(DR, buff=.26)


def protein(pos=P(0, 0), scale=1.0, sugar=True, vertical=True):
    """N points into teal, C into gold.  The membrane is horizontal."""
    if vertical:
        bar = RoundedRectangle(width=.34 * scale, height=1.48 * scale, corner_radius=.12,
                               stroke_width=0, fill_color=BLUE, fill_opacity=1).move_to(pos)
        npos, cpos = pos + UP * .93 * scale, pos + DOWN * .93 * scale
    else:
        bar = RoundedRectangle(width=1.48 * scale, height=.34 * scale, corner_radius=.12,
                               stroke_width=0, fill_color=BLUE, fill_opacity=1).move_to(pos)
        npos, cpos = pos + LEFT * .93 * scale, pos + RIGHT * .93 * scale
    def terminal(letter, center, color):
        circ = Circle(radius=.29 * scale, stroke_width=0, fill_color=color, fill_opacity=1).move_to(center)
        lab = T(letter, max(22, int(27 * scale)), BG, weight=BOLD).move_to(circ)
        return VGroup(circ, lab)
    n, c = terminal("N", npos, YELLOW), terminal("C", cpos, GREEN)
    g = VGroup(bar, n, c)
    g.bar, g.N, g.C = bar, n, c
    if sugar:
        stem = Line(npos + RIGHT * .18 * scale, npos + P(.52, .42) * scale,
                    color=ORANGE, stroke_width=max(3, 5 * scale))
        if scale >= .70:
            flag = RoundedRectangle(width=1.05 * scale, height=.48 * scale, corner_radius=.08,
                                    stroke_color=ORANGE, stroke_width=2, fill_color=ORANGE,
                                    fill_opacity=.22).move_to(npos + P(.86, .50) * scale)
            label = T("sugar", 28, ORANGE).move_to(flag)
            g.sugar = VGroup(stem, flag, label)
        else:
            flag = Square(side_length=.28 * scale, stroke_width=0, fill_color=ORANGE,
                          fill_opacity=1).move_to(npos + P(.58, .46) * scale)
            g.sugar = VGroup(stem, flag)
        g.add(g.sugar)
    return g


def whole_world(seed=2, proteins=False):
    """Stable whole-cell layout reused without lateral drift."""
    outside = Rectangle(width=13.3, height=1.18, stroke_width=0, fill_color=LUMEN,
                        fill_opacity=.20).move_to(P(0, 3.05))
    cyt = Rectangle(width=13.3, height=5.9, stroke_width=0, fill_color=CYTO,
                    fill_opacity=.075).move_to(P(0, -.45))
    pm = double_line(-6.6, 6.6, 2.43, .16)
    er = RoundedRectangle(width=4.15, height=2.05, corner_radius=.65, stroke_color=MEM,
                          stroke_width=7, fill_color=LUMEN, fill_opacity=.18).move_to(P(-3.75, .25))
    er2 = er.copy().scale(.88)
    erwall = VGroup(er, er2)
    golgi = VGroup()
    for i, (w, y) in enumerate([(3.05, .82), (2.75, .19), (2.42, -.44)]):
        sac = RoundedRectangle(width=w, height=.43, corner_radius=.20, stroke_color=MEM,
                               stroke_width=5, fill_color=LUMEN, fill_opacity=.20).move_to(P(1.50, y))
        golgi.add(sac)
    endo = Circle(radius=.72, stroke_color=MEM, stroke_width=6, fill_color=LUMEN,
                  fill_opacity=.20).move_to(P(4.35, -.90))
    labels = VGroup(T("outside", 28, LUMEN).move_to(P(-5.45, 3.05)),
                    T("ER lumen", 28, LUMEN).move_to(P(-4.5, .85)),
                    T("Golgi", 28, LUMEN).move_to(P(1.5, 1.42)),
                    T("cytosol", 28, CYTO).move_to(P(-.25, -2.75)))
    motes = moving_specks(seed)
    world = VGroup(cyt, outside, motes, pm, erwall, golgi, endo, labels)
    world.outside, world.cyt, world.pm, world.er, world.golgi, world.endo = outside, cyt, pm, erwall, golgi, endo
    world.motes, world.labels = motes, labels
    if proteins:
        ves = Circle(radius=.52, stroke_color=MEM, stroke_width=4, fill_color=LUMEN,
                     fill_opacity=.18).move_to(P(3.15, 1.30))
        ps = VGroup(protein(P(-3.72, -.74), .62), protein(P(1.5, -.67), .55),
                    protein(P(3.15, .78), .52), protein(P(4.4, 2.43), .62),
                    protein(P(4.35, -1.60), .50))
        world.proteins = ps
        world.add(ves, ps)
    return world


def local_membrane(y=0, top_teal=True, seed=5):
    teal_y, gold_y = (1.85, -1.85) if top_teal else (-1.85, 1.85)
    teal = Rectangle(width=13.3, height=3.65, stroke_width=0, fill_color=LUMEN,
                     fill_opacity=.18).move_to(P(0, teal_y))
    gold = Rectangle(width=13.3, height=3.65, stroke_width=0, fill_color=CYTO,
                     fill_opacity=.075).move_to(P(0, gold_y))
    wall = double_line(-6.5, 6.5, y, .20)
    motes_area = (-6.5, 6.5, -3.5, -.15) if top_teal else (-6.5, 6.5, .15, 3.5)
    return VGroup(gold, teal, moving_specks(seed, area=motes_area), wall)


def sac(center=P(0, -1.0), radius=1.25, with_protein=False):
    fill = Circle(radius=radius, stroke_width=0, fill_color=LUMEN, fill_opacity=.20).move_to(center)
    outer = Circle(radius=radius, stroke_color=MEM, stroke_width=8).move_to(center)
    inner = Circle(radius=radius-.15, stroke_color=MEM, stroke_width=4).move_to(center)
    g = VGroup(fill, outer, inner)
    g.fill = fill
    if with_protein:
        # At the bottom wall, N points up into the teal lumen and C out to gold.
        p = protein(center + DOWN * radius, .62)
        g.prot = p
        g.add(p)
    return g


def question_card():
    q = T("Contents?  Which face meets cytosol?", 31, TEXT)
    box = RoundedRectangle(width=q.width + .55, height=q.height + .42, corner_radius=.15,
                           stroke_color=TEXT, stroke_width=2, fill_color=BG, fill_opacity=.92)
    return VGroup(box, q).move_to(P(2.35, 2.72))


def pulse(m, color=None, scale=1.15):
    return Indicate(m, color=color or m.get_color(), scale_factor=scale)


class S00Hook(SpokenScene, TitleCard):
    LESSON = "Membrane organization and topology"
    TITLE = "Which Side Is Outside?"

    def construct(self):
        # First class is a TitleCard subclass, but the spoken hook leads with the promised picture.
        w = whole_world(10)
        tag = schematic_tag()
        p = protein(P(-3.72, -.74), .72, sugar=False)
        self.add(w, tag, p)
        self.at("sugar added")
        ps = protein(P(-3.72, -.74), .72).sugar
        self.play(GrowFromPoint(ps, p.N.get_center()), run_time=.65)
        self.at("inside its ER")
        self.play(w.er.animate.set_stroke(width=9), run_time=.65)
        self.at("outside the cell")
        ghost = protein(P(4.4, 2.43), .72).sugar.set_opacity(.48).shift(DOWN*.5)
        self.play(FadeIn(ghost, scale=.7), run_time=.45)
        route = DashedLine(ps.get_center(), ghost.get_center(), color=ORANGE, stroke_width=5)
        self.play(Create(route), run_time=1.15)
        self.at("across a membrane")
        x = T("×", 68, RED, weight=BOLD).move_to(P(-1.25, 2.43))
        mark = T("?", 74, TEXT, weight=BOLD).next_to(ghost, LEFT, buff=.35)
        self.play(GrowFromCenter(x), FadeIn(mark, shift=UP*.25), run_time=.55)
        self.play(route.animate.set_opacity(.25), rate_func=there_and_back, run_time=.7)
        self.finish()


class S01Title(Scene):
    def construct(self):
        w = whole_world(11)
        title = T("Which Side Is Outside?", 54, TEXT, font=TITLE_FONT)
        rule = Line(LEFT*1.25, RIGHT*1.25, color=GOLD, stroke_width=4).next_to(title, DOWN, buff=.3)
        plate = RoundedRectangle(width=title.width+.8, height=title.height+1.0,
                                 corner_radius=.18, stroke_width=0,
                                 fill_color=BG, fill_opacity=.86).move_to(VGroup(title, rule))
        self.add(w)
        self.play(FadeIn(plate), FadeIn(title, shift=UP*.15), GrowFromCenter(rule), run_time=.65)
        self.wait(.85)
        self.play(FadeOut(VGroup(plate, title, rule)), run_time=.45)


class S02Faces(SpokenScene):
    def construct(self):
        bg = local_membrane(seed=12)
        self.add(bg, schematic_tag())
        heads_top = VGroup(*[Dot(P(x, .12), radius=.09, color=MEM) for x in np.linspace(-6.2, 6.2, 25)])
        heads_bot = VGroup(*[Dot(P(x, -.12), radius=.09, color=MEM) for x in np.linspace(-6.2, 6.2, 25)])
        tails = VGroup(*[Line(P(x, .02), P(x, -.02), color=MEM, stroke_width=3) for x in np.linspace(-6.2, 6.2, 25)])
        self.add(heads_top, heads_bot, tails)
        self.at("two sheets")
        self.play(LaggedStart(pulse(heads_top, LUMEN, 1.08), pulse(heads_bot, CYTO, 1.08), lag_ratio=.45), run_time=1.1)
        self.at("two faces")
        arrows = VGroup(Arrow(P(-5.5,.55), P(5.5,.55), color=LUMEN, buff=0),
                        Arrow(P(5.5,-.55), P(-5.5,-.55), color=CYTO, buff=0))
        self.play(*[GrowArrow(a) for a in arrows], run_time=.9)
        self.at("touches the cytosol")
        cyt = T("cytosol", 38, CYTO).move_to(P(-4.8, -2.25))
        self.play(FadeIn(cyt, shift=UP*.2), bg[0].animate.set_fill(opacity=.12), run_time=.8)
        flow = VGroup(*[ArcBetweenPoints(P(-4.7, y), P(2.8, y), angle=.12,
                                         color=CYTO, stroke_width=8).set_opacity(.42)
                        for y in (-1.25, -1.75, -2.25)])
        self.play(Create(flow), run_time=.8)
        self.play(flow.animate.shift(RIGHT*1.6), run_time=1.35)
        self.play(FadeOut(flow), run_time=.35)
        self.at("outside of the cell")
        outside = T("outside", 38, LUMEN).move_to(P(3.9, 2.25))
        self.play(FadeIn(outside), run_time=.55)
        self.at("or a lumen")
        lumen = T("lumen", 38, LUMEN).move_to(outside)
        self.play(Transform(outside, lumen), bg[1].animate.set_fill(opacity=.26), run_time=.75)
        self.finish()


class S03Color(SpokenScene):
    def construct(self):
        w = whole_world(13)
        self.add(w, schematic_tag())
        self.at("is gold")
        # Keep the colour cue local: a bounded swatch marks open cytosol without tinting
        # the organelles, their labels, or the full frame.
        cyt_region = RoundedRectangle(width=7.4, height=1.18, corner_radius=.24,
                                      stroke_color=CYTO, stroke_width=4,
                                      fill_color=CYTO, fill_opacity=.10).move_to(P(-.25, -2.55))
        brush = Rectangle(width=.42, height=.96, fill_color=CYTO,
                          fill_opacity=.24, stroke_width=0).move_to(P(-3.65, -2.55))
        self.play(Create(cyt_region), brush.animate.move_to(P(3.15, -2.55)), run_time=1.15)
        self.play(FadeOut(brush), cyt_region.animate.set_fill(opacity=.05), run_time=.25)
        self.at("is teal")
        self.play(LaggedStart(pulse(w.er, LUMEN, 1.03), pulse(w.golgi, LUMEN, 1.05),
                              pulse(w.endo, LUMEN, 1.08), pulse(w.outside, LUMEN, 1.02), lag_ratio=.25), run_time=1.65)
        self.at("one gold face")
        gold_edge = Line(P(-6.4, 2.22), P(6.4, 2.22), color=CYTO, stroke_width=7)
        self.play(Create(gold_edge), run_time=.65)
        self.at("one teal face")
        teal_edge = Line(P(-6.4, 2.62), P(6.4, 2.62), color=LUMEN, stroke_width=7)
        self.play(Create(teal_edge), run_time=.65)
        self.play(Succession(gold_edge.animate.set_opacity(.35), gold_edge.animate.set_opacity(1)),
                  Succession(teal_edge.animate.set_opacity(.35), teal_edge.animate.set_opacity(1)), run_time=1.2)
        self.finish()


class S04PredictQ(SpokenScene):
    def construct(self):
        bg = local_membrane(y=2.15, top_teal=True, seed=14)
        self.add(bg, schematic_tag())
        pocket = Circle(radius=1.28, stroke_color=MEM, stroke_width=8, fill_color=LUMEN,
                        fill_opacity=.20).move_to(P(-2.1, .45))
        self.at("dimples inward")
        self.play(ReplacementTransform(bg[3].copy(), pocket), run_time=1.15)
        self.at("pinches off")
        self.play(pocket.animate.shift(DOWN*.55), run_time=.65)
        veil = Circle(radius=1.16, fill_color=GREY, fill_opacity=.42, stroke_width=0).move_to(pocket)
        qm = T("?", 62, TEXT).move_to(veil)
        self.play(FadeIn(VGroup(veil, qm)), run_time=.35)
        self.at("Predict")
        card = question_card()
        self.play(FadeIn(card, shift=LEFT*.4), run_time=.55)
        self.play(VGroup(pocket, veil, qm).animate.shift(UP*.12), rate_func=there_and_back, run_time=1.1)
        self.finish()


class S05PredictPause(Scene):
    def construct(self):
        bg = local_membrane(y=2.15, top_teal=True, seed=15)
        s = sac(P(-2.1, -.10))
        veil = Circle(radius=1.12, fill_color=GREY, fill_opacity=.42, stroke_width=0).move_to(s)
        q = T("?", 62, TEXT).move_to(s)
        card = question_card()
        self.add(bg, s, veil, q, card, schematic_tag())
        self.play(VGroup(s, veil, q).animate.shift(UP*.14), rate_func=there_and_back, run_time=2.15)
        self.play(VGroup(s, veil, q).animate.shift(DOWN*.10), rate_func=there_and_back, run_time=2.15)
        self.wait(.2)


class S06PredictA(SpokenScene):
    def construct(self):
        bg = local_membrane(y=2.15, top_teal=True, seed=16)
        s = sac(P(-2.1, -.10))
        veil = Circle(radius=1.12, fill_color=GREY, fill_opacity=.42, stroke_width=0).move_to(s)
        q = T("?", 62, TEXT).move_to(s)
        card = question_card()
        self.add(bg, s, veil, q, card, schematic_tag())
        self.at("outside fluid")
        self.play(FadeOut(VGroup(card, veil, q)), s.fill.animate.set_fill(opacity=.34), run_time=.75)
        self.at("gold face")
        edge = Circle(radius=1.34, color=CYTO, stroke_width=8).move_to(s)
        self.play(Create(edge), run_time=.65)
        self.at("Nothing crossed")
        mini = s.copy().scale(.54).move_to(P(3.45, -.25))
        arrow = Arrow(s.get_right()+RIGHT*.25, mini.get_left()-RIGHT*.25, color=TEXT, buff=0)
        self.play(FadeIn(mini), GrowArrow(arrow), run_time=.65)
        x = T("×", 58, RED, weight=BOLD).move_to(P(.65, 1.1))
        self.play(GrowFromCenter(x), run_time=.4)
        self.at("changed shape")
        oval = mini.copy().stretch(1.35, 0).stretch(.75, 1)
        self.play(Transform(mini, oval), run_time=.75)
        self.play(Transform(mini, s.copy().scale(.54).move_to(P(3.45, -.25))), run_time=.75)
        self.finish()


class S07Rule(SpokenScene):
    def construct(self):
        w = whole_world(17)
        self.add(w, schematic_tag())
        route = T("route lumens", 38, LUMEN)
        eq = M("=", 42, TEXT)
        out = T("outside", 38, LUMEN)
        banner = VGroup(route, eq, out).arrange(RIGHT, buff=.32).move_to(P(0, 3.05))
        self.at("Here is the rule")
        self.play(Write(route), run_time=.7)
        self.at("lumens count as outside")
        self.play(FadeIn(eq), Write(out), run_time=.8)
        dot = Dot(P(5.2, 3.05), radius=.16, color=LUMEN)
        self.add(dot)
        self.at("budding and fusing")
        path = VMobject(color=LUMEN, stroke_width=6).set_points_smoothly([P(5.2,3.05), P(4.9,1.8), P(4.35,-.9)])
        self.play(MoveAlongPath(dot, path), run_time=1.2)
        rev = VMobject(color=LUMEN, stroke_width=6).set_points_smoothly([P(-3.75,.3), P(1.5,.2), P(4.4,2.8)])
        dot2 = Dot(P(-3.75,.3), radius=.16, color=LUMEN)
        self.add(dot2)
        self.play(MoveAlongPath(dot2, rev), Create(rev.copy().set_stroke(opacity=.4)), run_time=1.5)
        self.at("without crossing")
        self.play(pulse(VGroup(dot, dot2), LUMEN, 1.5), run_time=.65)
        self.finish()


class S08Set(SpokenScene):
    def construct(self):
        bg = local_membrane(seed=18)
        trans = RoundedRectangle(width=1.15, height=.72, corner_radius=.16, stroke_color=MEM,
                                 stroke_width=4, fill_color=MEM, fill_opacity=.34).move_to(P(0,0))
        tl = T("translocon", 32, TEXT).move_to(P(3.05, .95))
        tl_leader = Line(tl.get_corner(DL) + P(.08, .03), trans.get_corner(UR),
                         color=TEXT, stroke_width=2)
        rib = chip("ribosome", CYTO, 30).move_to(P(0,-2.35))
        self.add(bg, schematic_tag(), trans, tl_leader, tl, rib)
        self.at("direction")
        arrow = CurvedArrow(P(-2.2,-1.2), P(-.45,.85), angle=-.5, color=YELLOW)
        self.play(Create(arrow), run_time=.7)
        self.at("set once")
        once = chip("set once", YELLOW, 36).move_to(P(3.9, 2.4))
        self.play(FadeIn(once, scale=.7), run_time=.5)
        self.at("chain is made")
        chain = VMobject(color=BLUE, stroke_width=12).set_points_smoothly([P(0,-1.95),P(-.2,-1.0),P(.05,-.25)])
        self.play(Create(chain), run_time=.8)
        self.at("channel called the translocon")
        self.play(pulse(VGroup(trans, tl), TEXT, 1.08), run_time=.55)
        self.at("threads one end")
        n = VGroup(Circle(radius=.3, fill_color=YELLOW, fill_opacity=1, stroke_width=0), T("N",25,BG,weight=BOLD)).move_to(P(.05,-.15))
        self.add(n)
        self.play(n.animate.move_to(P(.05,1.15)), chain.animate.set_points_smoothly([P(0,-1.95),P(-.2,-1),P(.05,.65)]), run_time=.85)
        bar = RoundedRectangle(width=.34, height=1.35, corner_radius=.1, fill_color=BLUE, fill_opacity=1, stroke_width=0).move_to(P(1.2,0))
        self.play(FadeIn(bar), run_time=.45)
        self.finish()


class S09Type1(SpokenScene):
    def construct(self):
        bg = local_membrane(seed=19)
        p = protein(P(0,0), 1.15, sugar=False)
        self.add(bg, schematic_tag(), p.bar, p.N)
        self.at("N terminus")
        self.play(pulse(p.N, YELLOW, 1.25), bg[1].animate.set_fill(opacity=.28), run_time=.7)
        self.at("C terminus")
        self.play(FadeIn(p.C, shift=UP*.3), pulse(p.C, GREEN, 1.2),
                  bg[0].animate.set_fill(opacity=.14), run_time=.8)
        self.at("type I")
        typ = chip("type I", BLUE, 36).move_to(P(3.6,-2.15))
        self.play(FadeIn(typ, shift=LEFT*.3), run_time=.55)
        self.at("an enzyme adds")
        enzyme = chip("sugar-adding enzyme", LUMEN, 34).move_to(P(-4.1,2.35))
        self.play(FadeIn(enzyme), enzyme.animate.move_to(P(-2.7,2.15)), run_time=.8)
        self.at("the sugar")
        sug = protein(P(0,0), 1.15).sugar
        self.play(GrowFromPoint(sug, p.N.get_center()), run_time=.65)
        self.play(pulse(sug, ORANGE, 1.2), run_time=.55)
        self.finish()


class S09bWatch(Scene):
    def construct(self):
        w = whole_world(20)
        p = protein(P(-3.72,-.74), .65)
        bud = Arc(radius=.62, start_angle=25*DEGREES, angle=130*DEGREES, arc_center=P(-2.95,-.95), color=MEM, stroke_width=7)
        self.add(w, p, schematic_tag())
        self.play(Create(bud), p.animate.shift(P(.3,.22)), run_time=1.7)
        self.play(bud.animate.scale(1.08), rate_func=there_and_back, run_time=.8)


class S10Golgi(SpokenScene):
    def construct(self):
        w = whole_world(21)
        p = protein(P(-3.72,-.74), .62)
        v = sac(P(-2.85,-.95), .68, with_protein=False)
        self.add(w, p, schematic_tag())
        self.at("vesicle buds")
        self.play(FadeIn(v), p.animate.move_to(P(-2.85,-1.63)), run_time=.75)
        vp = VGroup(v,p)
        self.at("fuses with the Golgi")
        self.play(vp.animate.move_to(P(.25,-.45)), run_time=1.25)
        self.play(FadeOut(v), p.animate.move_to(P(1.50,-.67)), run_time=.75)
        self.at("lumen joins first")
        erglow = w.er.copy().set_stroke(LUMEN, 9)
        self.play(FadeIn(erglow), run_time=.5)
        self.at("then the Golgi lumen")
        self.play(ReplacementTransform(erglow, w.golgi.copy().set_stroke(LUMEN, 8)), run_time=.75)
        self.at("never leaves teal")
        trail = VMobject(color=LUMEN, stroke_width=8).set_points_smoothly([P(-3.72,-.6),P(-1.5,-1.0),P(1.5,-.45)])
        self.play(Create(trail), pulse(p.sugar, ORANGE, 1.25), run_time=.85)
        self.finish()


class S10bWatch(Scene):
    def construct(self):
        w = whole_world(22)
        v = sac(P(2.45,1.15), .62, with_protein=True)
        self.add(w, schematic_tag())
        self.play(FadeIn(v, scale=.7), run_time=.55)
        self.play(v.animate.move_to(P(3.25,1.72)), run_time=1.4)


class S11Surface(SpokenScene):
    def construct(self):
        w = whole_world(23)
        v = sac(P(3.25,1.55), .68, with_protein=True)
        self.add(w, v, schematic_tag())
        self.at("fuses with the plasma membrane")
        self.play(v.animate.move_to(P(4.4,1.82)), run_time=.85)
        self.at("opens to the outside")
        pfinal = protein(P(4.4,2.43), .65)
        self.play(FadeOut(v), FadeIn(pfinal), w.outside.animate.set_fill(opacity=.30), run_time=.8)
        self.at("sugar now faces")
        ghost = pfinal.sugar.copy().set_opacity(.28).shift(LEFT*1.0)
        qm = T("?", 55, TEXT).next_to(ghost, LEFT, buff=.2)
        self.play(FadeIn(VGroup(ghost,qm)), run_time=.4)
        self.play(Transform(ghost, pfinal.sugar.copy()), FadeOut(qm), pulse(pfinal.sugar, ORANGE, 1.3), run_time=.75)
        self.at("inside a lumen")
        trail = VMobject(color=LUMEN, stroke_width=8).set_points_smoothly([P(-3.75,.2),P(1.5,.2),P(3.2,1.5),P(4.4,3.0)])
        self.play(Create(trail), run_time=1.05)
        self.play(trail.animate.set_opacity(.25), rate_func=there_and_back, run_time=.8)
        self.finish()


class S12Back(SpokenScene):
    def construct(self):
        w = whole_world(24)
        p = protein(P(4.4,2.43), .62)
        self.add(w, p, schematic_tag())
        s = sac(P(4.4,1.72), .72)
        self.play(GrowFromPoint(s, P(4.4,2.43)), p.animate.shift(DOWN*.10), run_time=1.15)
        self.at("bring the protein back in")
        self.play(s.animate.move_to(P(4.4,1.55)), p.animate.move_to(P(4.4,2.18)), run_time=.8)
        self.play(s.animate.move_to(P(4.35,-.90)), p.animate.move_to(P(4.35,-1.62)), run_time=1.05)
        self.at("endosome lumen")
        self.play(pulse(w.endo, LUMEN, 1.15), pulse(p.sugar, ORANGE, 1.2), run_time=.7)
        self.at("At no step")
        self.play(FadeOut(w.labels[3]), run_time=.25)
        mini = VGroup()
        xs = [-4.5,-1.5,1.5,4.5]
        names = ["ER","Golgi","surface","endosome"]
        for x,nm in zip(xs,names):
            box = RoundedRectangle(width=2.35,height=.95,corner_radius=.12,stroke_color=GREY,stroke_width=2)
            c = Circle(radius=.13,fill_color=GREEN,fill_opacity=1,stroke_width=0).move_to(box.get_bottom()+UP*.22)
            lab = T(nm,24,TEXT).move_to(box.get_top()+DOWN*.28)
            mini.add(VGroup(box,c,lab).move_to(P(x,-2.92)))
        self.play(LaggedStart(*[FadeIn(m) for m in mini], lag_ratio=.18), run_time=1.1)
        underline = Line(P(-5.65,-3.5),P(4.9,-3.5),color=CYTO,stroke_width=7)
        self.play(Create(underline), run_time=.75)
        self.finish()


class S12bWatch(Scene):
    def construct(self):
        w = whole_world(25)
        self.add(w, schematic_tag())
        ves = Circle(radius=.50, stroke_color=MEM, stroke_width=4, fill_color=LUMEN,
                     fill_opacity=.18).move_to(P(3.1,1.3))
        ps = VGroup(protein(P(-3.72,-.74),.58), protein(P(1.5,-.67),.52),
                    protein(P(3.1,.80),.48), protein(P(4.4,2.43),.58), protein(P(4.35,-1.6),.48))
        self.add(ves)
        self.play(LaggedStart(*[FadeIn(p, scale=.7) for p in ps], lag_ratio=.18), run_time=1.8)
        self.play(ps.animate.set_opacity(.72), rate_func=there_and_back, run_time=.2)


class S13Return(SpokenScene):
    def construct(self):
        w = whole_world(26, proteins=True)
        self.add(w, schematic_tag())
        self.at("once")
        self.play(pulse(w.proteins[0], YELLOW, 1.25), run_time=.65)
        self.at("at the ER")
        self.play(pulse(w.er, LUMEN, 1.06), run_time=.55)
        self.at("from lumen to lumen")
        route = VMobject(color=LUMEN, stroke_width=10).set_points_smoothly([P(-3.75,.2),P(1.5,.2),P(3.2,1.5),P(4.4,3.0),P(4.35,-.9)])
        self.play(Create(route), run_time=1.3)
        self.at("Secretory and endocytic lumens")
        self.play(LaggedStart(pulse(w.er,LUMEN,1.03), pulse(w.golgi,LUMEN,1.05),
                              pulse(w.outside,LUMEN,1.02), pulse(w.endo,LUMEN,1.08), lag_ratio=.22), run_time=1.5)
        self.at("Traffic never flips")
        locks = VGroup(*[T("↕", 34, TEXT).next_to(p, LEFT, buff=.08) for p in w.proteins])
        self.play(LaggedStart(*[FadeIn(x) for x in locks], lag_ratio=.12), run_time=.85)
        self.play(w.proteins.animate.set_opacity(.62), rate_func=there_and_back, run_time=1.0)
        self.finish()


class S14End(EndCard):
    LINE = "Lumens count as outside; traffic never flips proteins."
