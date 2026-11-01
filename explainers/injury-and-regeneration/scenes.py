"""Injury and regeneration  (Biochemistrypedia explainer, Developmental Neuroscience)

COLOR MAP (one color per concept, whole video)
  BLUE   = the neuron: cell body, axon, stump
  TEAL   = NMNAT2 (the short-lived supply) and the Wlds protein that stands in for it
  ORANGE = NMN
  GREEN  = NAD+ and ATP (the axon's energy)
  RED    = SARM1 and the cut/destruction
  YELLOW = calcium
  PURPLE = calpain
  GOLD   = growth cones and the program bracket
  SAGE   = repair glia (Schwann cells and astrocytes)
  GREY   = labels, outlines, de-emphasized
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def inhib(a, b, color=RED, w=5):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    b = b - d * 0.08
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w),
                  Line(b + perp * 0.26, b - perp * 0.26, color=color, stroke_width=w + 1))


def dim(c, o=0.3):
    return [c[1].animate.set_stroke(opacity=o).set_fill(opacity=0.16 * o), c[2].animate.set_opacity(o)]


def undim(c):
    return [c[1].animate.set_stroke(opacity=1).set_fill(opacity=0.16), c[2].animate.set_opacity(1)]


def tube(x0, x1, y, h=0.4, color=BLUE, op=0.3):
    return RoundedRectangle(corner_radius=h / 2, width=x1 - x0, height=h, stroke_color=color, stroke_width=3.5,
                            fill_color=color, fill_opacity=op).move_to([(x0 + x1) / 2, y, 0])


def beads(x0, x1, y, h=0.4, n=7, color=BLUE, op=0.3):
    pitch = (x1 - x0) / n
    g = VGroup()
    for i in range(n):
        w = pitch * 0.62
        g.add(RoundedRectangle(corner_radius=min(h, w) / 2, width=w, height=h * 0.9, stroke_color=color, stroke_width=3.5,
                               fill_color=color, fill_opacity=op).move_to([x0 + pitch * (i + 0.5), y + (0.05 if i % 2 else -0.05), 0]))
    return g


def neuron(y, xs=-5.4, xe=6.0, xc=-0.8, h=0.4, r=0.65):
    prox = tube(xs, xc, y, h)
    dist = tube(xc, xe, y, h)
    soma = Circle(radius=r, stroke_color=BLUE, stroke_width=4, fill_color=BG, fill_opacity=1).move_to([xs, y, 0])
    soma_f = Circle(radius=r, stroke_width=0, fill_color=BLUE, fill_opacity=0.3).move_to([xs, y, 0])
    nuc = Circle(radius=r * 0.36, stroke_color=GREY, stroke_width=2.5, fill_color=GREY, fill_opacity=0.35).move_to([xs, y, 0])
    n = VGroup(prox, dist, soma, soma_f, nuc)
    n.prox, n.dist, n.soma, n.nuc, n.y, n.xc, n.xe = prox, dist, VGroup(soma, soma_f), nuc, y, xc, xe
    return n


def cutmark(x, y, h=0.9):
    return VGroup(*[Line([x + dx - 0.12, y - h / 2, 0], [x + dx + 0.12, y + h / 2, 0], color=TEXT, stroke_width=5)
                    for dx in (-0.2, 0.2)])


def do_cut(n, gap=0.18):
    """animations that open a gap in the axon."""
    return [n.prox.animate.shift(LEFT * gap), n.dist.animate.shift(RIGHT * gap)]


def padlock(color=RED, opened=False, scale=1.0):
    body = RoundedRectangle(corner_radius=0.18, width=1.5, height=1.1, stroke_color=color, stroke_width=4,
                            fill_color=color, fill_opacity=0.3)
    sh = Arc(radius=0.46, start_angle=0, angle=PI, stroke_color=color, stroke_width=7).move_to(body.get_top() + UP * 0.38)
    if opened:
        sh.rotate(-0.55, about_point=sh.get_corner(DR)).shift(UP * 0.05)
    g = VGroup(sh, body)
    g.body, g.sh = body, sh
    g.scale(scale)
    return g


def gauge(w, h, color):
    return RoundedRectangle(corner_radius=0.08, width=w, height=h, stroke_color=color, stroke_width=3)


SAGE = "#9BB99B"


def cone(x, y, color=GOLD):
    # A broad, fingered growth tip; a schematic cell shape, not a molecule.
    return Polygon([-0.45, -0.16, 0], [0.03, -0.37, 0], [0.48, -0.33, 0],
                   [0.25, -0.10, 0], [0.58, 0, 0], [0.25, 0.10, 0],
                   [0.48, 0.33, 0], [0.03, 0.37, 0], [-0.45, 0.16, 0],
                   stroke_color=color, fill_color=color, fill_opacity=0.45,
                   stroke_width=3).shift([x, y, 0])


def glia(x, y, color=SAGE):
    return Ellipse(width=1.25, height=0.55, color=color, fill_opacity=0.25,
                   stroke_width=3).move_to([x, y, 0])


def target(x, y):
    body = RoundedRectangle(width=0.85, height=1.55, corner_radius=0.35,
                            color=GREY, fill_opacity=0.2)
    lines = VGroup(*[Line([-0.25, z, 0], [0.25, z, 0], color=GREY)
                    for z in (-0.42, 0, 0.42)])
    return VGroup(body, lines).move_to([x, y, 0])


def heading(text):
    return T(text, 32, TEXT).move_to([0, 3.1, 0])


class S00Title(TitleCard):
    LESSON = "Injury and regeneration"
    TITLE = "Why the Spinal Cord Does Not Regrow"


class S01Contrast(SpokenScene):
    def construct(self):
        divider = Line([0, -2.8, 0], [0, 2.6, 0], color=GREY, stroke_opacity=0.35)
        left = T("Nerve in the arm", 30).move_to([-3.4, 2.8, 0])
        right = T("Spinal cord", 30).move_to([3.4, 2.8, 0])
        a = neuron(0.7, xs=-5.8, xe=-0.8, xc=-4.0, r=0.45)
        b = neuron(0.7, xs=1.1, xe=6.0, xc=2.9, r=0.45)
        guide = VGroup(*[glia(x, 0.18) for x in (-3.5, -2.25, -1.0)],
                       *[glia(x, 1.22) for x in (-3.5, -2.25, -1.0)])
        tip = cone(-4.05, 0.7)
        self.at("Cut a nerve")
        self.play(FadeIn(left), FadeIn(a), Create(divider), run_time=0.5)
        cm = cutmark(-4, 0.7)
        self.play(*do_cut(a), FadeIn(cm), run_time=0.4)
        self.at("can grow back")
        self.play(FadeOut(a.dist), FadeIn(guide), FadeIn(tip), run_time=0.4)
        grown = tube(-4.2, -1.0, 0.7)
        self.play(GrowFromEdge(grown, LEFT), FadeOut(cm), tip.animate.move_to([-1.0, 0.7, 0]), run_time=1.1)
        self.at("your spinal cord")
        self.play(FadeIn(right), FadeIn(b), run_time=0.5)
        self.play(*do_cut(b), FadeIn(cutmark(2.9, 0.7)), run_time=0.4)
        self.at("mostly do not")
        self.play(b.prox.animate.set_stroke(width=7), b.dist.animate.set_opacity(0.25), run_time=0.6)
        block = bchip("surroundings block", RED, 26).move_to([3.4, -0.9, 0])
        low = bchip("growth program turned down", BLUE, 24).move_to([3.4, -2.0, 0])
        self.at("Two things hold")
        self.play(Indicate(b.prox, color=BLUE), run_time=0.7)
        self.at("The tissue around")
        self.play(FadeIn(block), run_time=0.6)
        self.at("growth program down")
        self.play(FadeIn(low), run_time=0.6)
        ready = T("ready to grow", 26, BLUE).move_to([-3.4, -0.9, 0])
        help_ = T("cells help", 26, SAGE).move_to([-3.4, -2.0, 0])
        self.at("ready to grow")
        self.play(FadeIn(ready), Indicate(a.soma, color=BLUE), run_time=0.7)
        self.at("the cells around")
        self.play(FadeIn(help_), Indicate(guide, color=SAGE, scale_factor=1.03), run_time=0.7)
        self.finish()


class S02Test(SpokenScene):
    def construct(self):
        q = heading("Surroundings and the neuron: two tests")
        self.at("How do we know")
        self.play(FadeIn(q), run_time=0.5)
        # Schematic brainstem and cord with a curved peripheral graft between them.
        med = RoundedRectangle(width=1.7, height=2.1, corner_radius=0.55,
                               color=BLUE, fill_opacity=0.18).move_to([-4.6, 0.4, 0])
        cord = tube(2.8, 6.0, 0.4, 1.5, BLUE, 0.18)
        labels = VGroup(T("medulla", 26, BLUE).move_to([-4.6, -1.2, 0]),
                        T("spinal cord", 26, BLUE).move_to([4.4, -1.2, 0]),
                        T("rat", 26, GREY).move_to([-5.7, 2.3, 0]))
        path = CubicBezier([-4.0, 0.4, 0], [-1.7, 2.0, 0], [1.0, 2.0, 0], [3.5, 0.4, 0])
        bridge = path.copy().set_stroke(SAGE, width=35, opacity=0.35)
        bl = T("peripheral nerve graft", 26, SAGE).move_to([0, 2.25, 0])
        self.at("In rats")
        self.play(FadeIn(med), FadeIn(cord), FadeIn(labels), run_time=0.5)
        self.at("a peripheral nerve graft")
        self.play(Create(bridge), FadeIn(bl), run_time=0.8)
        ax = path.copy().set_stroke(BLUE, width=6)
        tip = cone(-4, 0.4)
        dist = T("about 30 mm", 28, GOLD).move_to([0, -0.5, 0])
        self.at("central axons grow")
        self.add(tip)
        self.play(Create(ax), MoveAlongPath(tip, path), FadeIn(dist), run_time=2.0)
        stop = T("stops in central tissue", 26, RED).move_to([2.9, -2.3, 0])
        self.at("central tissue again")
        self.play(FadeIn(stop), Indicate(tip, color=RED), run_time=0.7)
        self.at("In mice")
        self.play(*[FadeOut(m) for m in list(self.mobjects) if m is not q], run_time=0.45)
        eye = Circle(radius=1.1, color=BLUE, fill_opacity=0.12).move_to([-4.8, 0, 0])
        retinal = Dot([-4.15, 0, 0], radius=0.22, color=BLUE)
        nerve = tube(-4.0, 5.8, 0, 0.65)
        crush = cutmark(0.8, 0, 1.2)
        pten = bchip("PTEN", GREY, 30).move_to([-4.8, 1.75, 0])
        el = VGroup(T("mouse eye", 26, BLUE).move_to([-4.8, -1.7, 0]),
                    T("crushed optic nerve", 26, GREY).move_to([2.2, -1.2, 0]))
        self.play(FadeIn(eye), FadeIn(nerve), FadeIn(retinal), FadeIn(crush), FadeIn(el), run_time=0.5)
        self.at("deleting a gene")
        cross = Cross(stroke_color=RED, stroke_width=5).scale(0.2).next_to(pten, RIGHT, buff=0.2)
        self.play(FadeIn(pten), Create(cross), run_time=0.6)
        self.at("many axons regrow")
        growth = VGroup(*[Line([-4.0, y, 0], [4.7, y, 0], color=BLUE, stroke_width=3)
                          for y in (-0.17, 0, 0.17)])
        gc = cone(-3.7, 0)
        self.add(gc)
        self.play(GrowFromEdge(growth, LEFT), gc.animate.move_to([4.7, 0, 0]), run_time=2.1)
        self.finish()


class S03TwoParts(SpokenScene):
    def construct(self):
        n = neuron(1.0, xc=-0.8)
        cm = cutmark(-0.8, 1.0)
        self.at("A cut splits")
        self.play(FadeIn(n), run_time=0.4)
        self.play(*do_cut(n), Create(cm), run_time=0.5)
        cell = T("joined to the cell body", 26, BLUE).move_to([-3.5, 2.4, 0])
        tip = cone(-1.5, 1.0)
        self.at("The part joined")
        self.play(FadeIn(cell), run_time=0.4)
        self.at("can grow a new tip")
        self.play(FadeIn(tip, scale=0.3), run_time=0.7)
        dl = T("part beyond the cut", 26, BLUE).move_to([3.0, 2.4, 0])
        self.at("The part beyond")
        self.play(FadeIn(dl), run_time=0.4)
        # The narrated time delay is represented by the clock label, not real-time waiting.
        self.at("falls to pieces")
        bd = beads(-0.62, 6.18, 1.0, n=7)
        self.play(ReplacementTransform(n.dist, bd), run_time=0.7)
        time = T("about 1½ days", 26, GREY).move_to([3.0, 0.0, 0])
        self.at("a day and a half")
        self.play(FadeIn(time), run_time=0.4)
        nb = neuron(-1.8, xc=-0.8)
        gene = bchip("Sarm1 deleted", RED, 26).move_to([-3.5, -0.6, 0])
        self.at("In mice that lack")
        self.play(FadeIn(nb), FadeIn(gene), run_time=0.6)
        self.play(*do_cut(nb), Create(cutmark(-0.8, -1.8)), run_time=0.4)
        self.at("stay whole for weeks")
        weeks = T("weeks: stump stays whole", 26, BLUE).move_to([2.8, -2.8, 0])
        self.play(FadeIn(weeks), Indicate(nb.dist, color=BLUE, scale_factor=1.04), run_time=0.7)
        self.finish()


class S04Program(SpokenScene):
    def construct(self):
        n = neuron(1.1, xc=-0.8, h=0.65)
        head = bchip("NMNAT2", TEAL, 30).move_to([-3.8, 2.8, 0])
        note = T("short-lived supply", 26, TEAL).move_to([1.2, 2.8, 0])
        packets = VGroup(*[Dot([-4.7, 1.1, 0], radius=0.14, color=TEAL) for _ in range(3)])
        self.at("An enzyme called")
        self.play(FadeIn(n), FadeIn(head), run_time=0.5)
        self.at("short")
        self.play(FadeIn(note), run_time=0.4)
        self.at("must keep sending it")
        self.add(packets)
        self.play(*[p.animate.move_to([x, 1.1, 0]) for p, x in zip(packets, (1.8, 3.3, 4.8))], run_time=1.3)
        self.at("A cut stops")
        self.play(*do_cut(n), Create(cutmark(-0.8, 1.1)), FadeOut(packets), run_time=0.6)
        late = Dot([-4.7, 1.1, 0], radius=0.14, color=TEAL)
        self.add(late)
        self.play(late.animate.move_to([-1.2, 1.1, 0]), run_time=0.7)
        self.play(Indicate(late, color=RED), run_time=0.3)
        self.at("Its raw material")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.4)
        # Enlarge the local sequence in the stump.
        bar = Rectangle(width=0.9, height=0.3, color=ORANGE, fill_opacity=0.5).move_to([-4.6, -1.6, 0])
        label = T("NMN", 28, ORANGE).move_to([-4.6, -2.25, 0])
        lock = padlock(RED).move_to([-0.6, 0.8, 0])
        sl = T("SARM1", 30, RED).move_to([-0.6, -0.65, 0])
        model = T("leading model", 24, GREY).move_to([-2.2, 2.8, 0])
        self.play(FadeIn(bar), FadeIn(label), run_time=0.4)
        self.at("builds up")
        tall = Rectangle(width=0.9, height=2.8, color=ORANGE, fill_opacity=0.5).move_to([-4.6, -0.35, 0])
        self.play(Transform(bar, tall), run_time=0.65)
        self.at("in the leading model")
        self.play(FadeIn(model), FadeIn(lock), FadeIn(sl), run_time=0.4)
        self.at("switches")
        opened = padlock(RED, opened=True).move_to(lock)
        self.play(Transform(lock, opened), GrowArrow(arr([-3.8, 0.3, 0], [-1.8, 0.3, 0], ORANGE)), run_time=0.7)
        nad = bchip("NAD+", GREEN, 30).move_to([3.8, 0.8, 0])
        self.at("cleaves")
        slash = Line([3.0, 0.3, 0], [4.6, 1.3, 0], color=RED, stroke_width=6)
        self.play(FadeIn(nad), Create(slash), run_time=0.55)
        self.at("Energy")
        energy = T("energy falls", 26, GREEN).move_to([3.8, -0.65, 0])
        self.play(FadeIn(energy), nad.animate.set_opacity(0.25), run_time=0.6)
        self.at("calcium rises")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.3)
        tb = tube(-5.8, 5.8, -0.2, 1.1)
        scaffold = VGroup(*[Line([-5.6, y, 0], [5.6, y, 0], color=GREY, stroke_width=3) for y in (-0.45, 0.05)])
        ca = VGroup(*[Dot([x, y, 0], radius=0.10, color=YELLOW)
                      for x, y in ((-4.8,-0.1),(-3,-0.4),(-1,0.1),(1,-0.3),(3,0.05),(5,-0.4))])
        cal = T("calcium rises", 28, YELLOW).move_to([-3.6, 2.5, 0])
        cp = bchip("calpain", PURPLE, 28).move_to([2.6, 0.7, 0])
        self.play(FadeIn(tb), FadeIn(scaffold), FadeIn(ca), FadeIn(cal), run_time=0.4)
        self.at("and calcanes")
        self.play(FadeIn(cp, shift=DOWN * 0.2), run_time=0.4)
        self.at("cut the axon apart")
        cuts = VGroup(*[Line([x, -0.85, 0], [x, 0.45, 0], color=PURPLE, stroke_width=5) for x in (-2, 0, 2)])
        self.play(Create(cuts), run_time=0.25)
        self.play(ReplacementTransform(tb, beads(-5.8, 5.8, -0.2, 1.0, 7)),
                  FadeOut(scaffold), FadeOut(cuts), FadeOut(ca), FadeOut(cp), run_time=0.55)
        self.finish()


class S05Schwann(SpokenScene):
    def construct(self):
        title = heading("Peripheral nerve: cells help regrowth")
        ax = tube(-5.7, -3.7, -0.4, 0.45)
        cells = VGroup(*[glia(x, y, GREY) for x, y in ((-2.5,0.3),(0,-1.1),(2.5,0.4))])
        debris = beads(-2.8, 3.7, -0.4, 0.5, 4, GREY)
        scl = T("Schwann cells", 28, SAGE).move_to([-3.8, 1.8, 0])
        self.at("In a nerve")
        self.play(FadeIn(title), FadeIn(ax), FadeIn(cells), FadeIn(debris), run_time=0.5)
        self.at("Schwann cells")
        self.play(FadeIn(scl), run_time=0.4)
        self.at("turn into repair cells")
        repair = T("repair Schwann cells", 28, SAGE).move_to(scl)
        self.play(cells.animate.set_color(SAGE), ReplacementTransform(scl, repair), run_time=0.8)
        self.at("help clear")
        self.play(debris[0].animate.scale(0.05).move_to(cells[0]), run_time=0.6)
        self.remove(debris[0])
        vessel = tube(0.3, 5.8, 2.0, 0.5, RED, 0.15)
        blood = T("blood", 24, RED).move_to([5.2, 2.7, 0])
        macrophage = Circle(radius=0.47, color=GREY, fill_opacity=0.35).move_to([2.3, 2.0, 0])
        ml = T("macrophage", 26, GREY).move_to([2.3, 1.0, 0])
        self.at("call in macrophages")
        self.play(FadeIn(vessel), FadeIn(blood), FadeIn(macrophage), FadeIn(ml), run_time=0.4)
        self.play(macrophage.animate.move_to([2.3, -0.4, 0]), FadeOut(ml),
                  *[d.animate.scale(0.05).move_to([2.3, -0.4, 0]) for d in list(debris)[1:]], run_time=0.8)
        self.at("line up into tubes")
        guide = VGroup(*[glia(x,y) for x in (-2.5,0,2.5) for y in (-1.0,0.2)])
        self.play(ReplacementTransform(cells, guide), FadeOut(debris), FadeOut(macrophage),
                  FadeOut(vessel), FadeOut(blood), run_time=0.7)
        muscle = target(5.5, -0.4)
        tl = T("muscle", 26, GREY).move_to([5.5, -1.7, 0])
        tip = cone(-3.7, -0.4)
        growth = tube(-3.7, 5.0, -0.4, 0.45)
        self.at("guide the regrowing axon")
        self.play(FadeIn(tip), FadeIn(muscle), FadeIn(tl), run_time=0.4)
        self.play(GrowFromEdge(growth, LEFT), tip.animate.move_to([4.95, -0.4, 0]), run_time=1.5)
        rate = T("around 1 mm / day", 30, GOLD).move_to([0, -2.5, 0])
        self.at("often at around")
        self.play(FadeIn(rate), run_time=0.6)
        self.finish()


class S06Cord(SpokenScene):
    def construct(self):
        title = heading("Central tissue: several barriers")
        ax = tube(-6.0, -2.8, 0, 0.45)
        tip = cone(-2.8, 0)
        debris = beads(-1.5, 4.5, -1.1, 0.45, 4, GREY)
        dl = T("myelin debris lingers", 26, GREY).move_to([2.2, -2.2, 0])
        self.at("In the spinal cord")
        self.play(FadeIn(title), FadeIn(ax), FadeIn(tip), FadeIn(debris), run_time=0.5)
        self.at("debris clears slowly")
        self.play(FadeIn(dl), run_time=0.6)
        nogo = bchip("Nogo", GREY, 28).move_to([0, 1.3, 0])
        self.at("such as NOGO")
        self.play(FadeIn(nogo), run_time=0.4)
        self.play(nogo.animate.move_to([-1.8, 0.55, 0]), run_time=0.45)
        self.at("collapse growth cones")
        blunt = Ellipse(width=0.25, height=0.45, color=BLUE, fill_opacity=0.4).move_to([-2.8,0,0])
        self.play(Transform(tip, blunt), run_time=0.6)
        self.at("removing them alone")
        small = T("removal alone: little regrowth", 26, GREY).move_to([0, 2.2, 0])
        self.play(FadeOut(nogo), FadeIn(small), run_time=0.6)
        self.at("The lesion also fills")
        self.play(FadeOut(small), FadeOut(dl), FadeOut(debris), run_time=0.4)
        lesion = Circle(radius=1.7, color=RED, fill_opacity=0.12, stroke_opacity=0.3).move_to([1.3,0,0])
        blocks = VGroup(*[Dot([x,y,0], radius=0.12, color=RED) for x,y in
                         ((0.3,-0.7),(0.5,0.5),(1.1,0.9),(1.8,-0.6),(2.2,0.5),(1.3,-0.1))])
        bl = T("growth-blocking molecules", 26, RED).move_to([1.3,-2.6,0])
        self.play(FadeIn(lesion), FadeIn(blocks), FadeIn(bl), run_time=0.7)
        border = VGroup(*[glia(1.3+1.85*np.cos(a), 1.85*np.sin(a)).rotate(a+PI/2)
                         for a in np.linspace(0,TAU,7,endpoint=False)])
        al = T("astrocyte border", 26, SAGE).move_to([4.7,2.2,0])
        self.at("Astrocytes form a border")
        self.play(FadeIn(border), FadeIn(al), run_time=0.7)
        self.at("limits the spread")
        damage = Circle(radius=0.5, color=RED, fill_opacity=0.28).move_to([1.3,0,0])
        self.play(GrowFromCenter(damage), run_time=0.4)
        self.play(damage.animate.scale(3.0), border.animate.set_stroke(width=5), run_time=0.8)
        self.at("change the scar")
        rule = T("Change the scar; keep its protective border", 28, SAGE).move_to([0,-3.3,0])
        self.play(FadeIn(rule), run_time=0.7)
        self.finish()


class S07Fix(SpokenScene):
    def construct(self):
        divider = Line([0,-1.8,0],[0,2.5,0],color=GREY,stroke_opacity=0.4)
        labels = VGroup(T("Preserve",32,BLUE).move_to([-3.4,2.8,0]),
                        T("Regrow and reconnect",30,GOLD).move_to([3.4,2.8,0]))
        a = neuron(0.4,xs=-5.8,xe=-0.7,xc=-3.8,r=0.45)
        b = neuron(0.4,xs=1,xe=5.1,xc=2.3,r=0.45)
        muscle = target(5.9,0.4)
        self.at("there are two problems")
        self.play(FadeIn(labels),Create(divider),FadeIn(a),run_time=0.5)
        self.play(*do_cut(a,0.28),Create(cutmark(-3.8,0.4)),run_time=0.4)
        blocker = bchip("SARM1 blocked",RED,26).move_to([-3.4,1.7,0])
        self.at("Blocking")
        self.play(FadeIn(blocker),run_time=0.6)
        self.at("keep axons from breaking")
        self.play(Indicate(a.dist,color=BLUE,scale_factor=1.03),run_time=0.7)
        gap = T("whole stump, gap remains",24,GREY).move_to([-3.4,-0.9,0])
        self.at("cannot rejoin")
        self.play(FadeIn(gap),run_time=0.6)
        self.at("Function returns only")
        self.add(b.prox,b.soma,b.nuc)
        self.play(FadeIn(muscle),run_time=0.5)
        gc = cone(2.3,0.4)
        growth = tube(2.3,5.45,0.4)
        self.at("the attached part regrows")
        self.add(gc)
        self.play(GrowFromEdge(growth,LEFT),gc.animate.move_to([5.35,0.4,0]),run_time=1.3)
        contact = Dot([5.45,0.4,0],radius=0.17,color=GOLD)
        right = T("contact with the right target",24,GREY).move_to([3.4,-0.9,0])
        self.at("connects with the right target")
        self.play(FadeOut(gc),FadeIn(contact),FadeIn(right),run_time=0.7)
        rod = bchip("rodents: partly",GREY,28).move_to([-3.1,-2.5,0])
        human = bchip("people: not yet",GREY,28).move_to([3.1,-2.5,0])
        self.at("In rodents")
        self.play(FadeIn(rod),run_time=0.6)
        self.at("None yet restores")
        self.play(FadeIn(human),run_time=0.6)
        self.finish()


class S08End(EndCard):
    LINE = "Central axons mostly don't regrow: blocking tissue and a turned-down growth program."
