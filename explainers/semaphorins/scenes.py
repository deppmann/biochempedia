"""Semaphorins and repulsion: neuropilin catches, plexin signals  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  TEAL   = the growth cone and its axon
  YELLOW = Sema3A / semaphorin cues
  BLUE   = neuropilin
  PURPLE = plexin (and its inner GAP part)
  ORANGE = small GTPase and integrin adhesion
  GOLD   = the GTP badge
  GREEN  = a response that happens
  RED    = a response that is blocked / switched off / lost
  GREY   = membranes, outlines, labels, the unknown
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


# ------------------------------------------------------------------------------------------
# helpers
# ------------------------------------------------------------------------------------------
def fan_pts(a0, a1, r, c, n=11):
    c = np.array(c, float)
    pts = [c + np.array([0, 0.28, 0])]
    for a in np.linspace(a1, a0, n):
        pts.append(c + r * np.array([np.cos(a), np.sin(a), 0]))
    pts.append(c + np.array([0, -0.28, 0]))
    return pts


def fan(a0, a1, r, c):
    return Polygon(*fan_pts(a0, a1, r, c), color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.25)


def filopodia(a0, a1, r, c, k=7):
    c = np.array(c, float)
    g = VGroup()
    for a in np.linspace(a0 + 0.05, a1 - 0.05, k):
        d = np.array([np.cos(a), np.sin(a), 0])
        g.add(Line(c + r * d, c + (r + 0.5) * d, color=TEAL, stroke_width=3))
    return g


def shaft(c, x0=-6.3):
    return Rectangle(width=c[0] - x0, height=0.56, stroke_width=0, fill_color=TEAL,
                     fill_opacity=0.25).move_to([(c[0] + x0) / 2, c[1], 0])


def dots(points, color=YELLOW, r=0.13):
    return VGroup(*[Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=0.95).move_to([p[0], p[1], 0]) for p in points])


def mem_bar(y, x0=-6.3, x1=6.3, h=0.34):
    return RoundedRectangle(corner_radius=0.1, width=x1 - x0, height=h, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.35).move_to([(x0 + x1) / 2, y, 0])


def rr(w, h, color, op=0.3, sw=3.5, r=0.18):
    return RoundedRectangle(corner_radius=min(r, w / 2.2, h / 2.2), width=w, height=h, stroke_color=color,
                            stroke_width=sw, fill_color=color, fill_opacity=op)


def sema(x, y, w=1.3, h=0.55):
    e = Ellipse(width=w, height=h, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.9)
    return e.move_to([x, y, 0])


def semag(x, y, w=1.3, h=0.55, size=24):
    e = sema(x, y, w, h)
    t = T("Sema3A", size, BG).move_to(e)
    return VGroup(e, t)


class Rec(VGroup):
    """A receptor drawn as shapes: body outside, neck through the membrane, tail inside.
    parts: body (with label), neck, tail."""

    def __init__(self, name, color, x, ym=0.0, s=1.0, body_h=1.7, tail_h=0.38, tail_w=0.26):
        super().__init__()
        bw = 1.6 * s
        bh = body_h * s
        self.body = rr(bw, bh, color).move_to([x, ym + 0.17 + bh / 2, 0])
        self.lab = T(name, int(round(22 * max(1.0, s))), color).move_to(self.body)
        self.neck = Rectangle(width=0.3 * s, height=0.34, stroke_width=0, fill_color=color, fill_opacity=0.9).move_to([x, ym, 0])
        th = tail_h * s
        self.tail = rr(tail_w * s, th, color, op=0.5, sw=3, r=0.06).move_to([x, ym - 0.17 - th / 2, 0])
        self.add(self.body, self.lab, self.neck, self.tail)
        self.x, self.ym, self.s, self.color = x, ym, s, color

    def top(self):
        return self.body.get_top()[1]


def lab(text, size=26, color=GREY, **kw):
    return T(text, size, color, **kw)


def qbox(w=1.1, h=1.1, color=GREY):
    box = DashedVMobject(RoundedRectangle(corner_radius=0.14, width=w, height=h, stroke_color=color, stroke_width=3.5), num_dashes=24)
    q = T("?", 44, color, weight=BOLD)
    return VGroup(box, q)


class S00Title(TitleCard):
    LESSON = "Semaphorins and Repulsion"
    TITLE = "Semaphorins: Keeping Axons on Course"


YM = -0.5
CS = 1.25


def complex_at(xn, xp, ym=YM, s=CS):
    n = Rec("neuropilin", BLUE, xn, ym, s=s)
    p = Rec("plexin", PURPLE, xp, ym, s=s, tail_h=1.3, tail_w=0.3)
    return n, p


def path(points, color=TEAL, width=6):
    return VMobject(color=color, stroke_width=width).set_points_smoothly([np.array(p, float) for p in points])


def growth(c=(-3, 0, 0), r=2.6):
    return VGroup(shaft(c), fan(-0.85, 0.85, r, c), filopodia(-0.85, 0.85, r, c))


def spinal():
    """Schematic cross-section, dorsal up; separate sensory routes."""
    outline = Ellipse(width=5.6, height=5.2, color=GREY, fill_color=GREY, fill_opacity=0.07).move_to([0, 0, 0])
    horns = Polygon(*[np.array([x, y, 0]) for x, y in
        [(-1.55, 1.9), (-.55, .55), (.55, .55), (1.55, 1.9), (1.1, .1),
         (1.65, -1.7), (.55, -.95), (-.55, -.95), (-1.65, -1.7), (-1.1, .1)]],
        color=GREY, fill_color=GREY, fill_opacity=.15)
    anatomy = VGroup(outline, horns, T("dorsal", 24, GREY).move_to([0, 2.95, 0]),
                     T("ventral horn", 24, GREY).move_to([0, -2.95, 0]))
    cue = VGroup(rr(3.8, 1.55, YELLOW, .12).move_to([0, -1.1, 0]),
                 T("Sema3A", 26, YELLOW).move_to([0, -1.4, 0]))
    pain = path([[-6, 1, 0], [-3, 1, 0], [-1.6, .3, 0], [-1.25, 1.35, 0]])
    pain_label = T("pain fibre", 26, TEAL).move_to([-4.6, 1.65, 0])
    muscle = path([[6, 1, 0], [3.1, 1, 0], [1.4, .2, 0], [.8, -.7, 0]], GREY)
    muscle_label = T("muscle-stretch\nfibre", 24, GREY).move_to([4.5, 1.85, 0])
    return anatomy, cue, pain, pain_label, muscle, muscle_label


class S01Collapse(SpokenScene):
    def construct(self):
        anatomy, cue, pain, pl, muscle, ml = spinal()
        self.add(anatomy)
        self.at("guide growing axons")
        approach = path([[-6, 1, 0], [-3, 1, 0], [-1.6, .3, 0]])
        self.play(Create(approach), run_time=1.2)
        self.at("by repelling")
        self.play(FadeIn(cue), Transform(approach, pain), run_time=1.2)
        self.at("Keeping axons out")
        self.play(Indicate(approach, color=TEAL), run_time=.7)
        self.at("In the spinal cord")
        self.play(FadeIn(pl), run_time=.5)
        self.at("while muscle stretch")
        self.play(Create(muscle), FadeIn(ml), run_time=1.1)
        shared = T("Sema3A: one of the cues", 24, YELLOW).move_to([0, -3.45, 0])
        self.at("Other cues probably")
        self.play(FadeIn(shared), run_time=.5)
        gc = growth()
        gl = T("growth cone", 28, TEAL).move_to([-2, -3.0, 0])
        self.at("A growth cone")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], FadeIn(gc), FadeIn(gl), run_time=.8)
        dish = T("dish assay", 28, GREY).move_to([0, 3.2, 0])
        dd = dots([(2.3, .8), (2.6, 0), (2.3, -.8)])
        dl = T("repellent", 26, YELLOW).move_to([3.5, 1.7, 0])
        self.at("In a dish")
        self.play(FadeIn(dish), FadeIn(dd), FadeIn(dl), run_time=.5)
        self.at("fold that fan")
        self.play(Transform(gc[1], fan(-.07, .07, 1.8, [-3, 0, 0])), FadeOut(gc[2]),
                  dd.animate.shift(LEFT), run_time=1.0)
        self.at("That is collapse")
        result = T("collapse", 30, RED).move_to([2, -1.6, 0])
        self.play(FadeIn(result), run_time=.4)
        self.finish()


class S02Neuropilin(SpokenScene):
    def construct(self):
        gc = growth()
        self.add(gc)
        mem = mem_bar(0)
        n = Rec("neuropilin", BLUE, 0, s=1.3)
        sg = semag(4.5, 2.95, 1.8, .7)
        self.at("How does the growth cone")
        self.play(FadeOut(gc), FadeIn(mem), FadeIn(n), run_time=.9)
        self.at("This secreted semaphorin")
        self.play(FadeIn(sg), run_time=.5)
        self.at("binds")
        self.play(sg.animate.move_to([0, n.top() + .4, 0]), run_time=.9)
        self.at("has only a short tail")
        tl = T("short tail", 28, BLUE).move_to([3.0, -.9, 0])
        ln = Line(n.tail.get_right(), [1.9, -.9, 0], color=BLUE)
        inside = T("inside the cell", 24, GREY).move_to([-4, -.9, 0])
        self.play(FadeIn(tl), Create(ln), FadeIn(inside), run_time=.6)
        self.at("nothing that looks")
        nl = T("no enzyme-like part", 26, GREY).move_to([3, -1.6, 0])
        self.play(FadeIn(nl), run_time=.4)
        self.at("must also pass it on")
        q = qbox(1.3, 1.1).move_to([0, -2.5, 0])
        wire = DashedLine(n.tail.get_bottom(), q.get_top(), color=GREY)
        self.play(Create(wire), FadeIn(q), run_time=.6)
        self.at("Where is the wire")
        question = T("Where is the wire?", 28).move_to([3.6, -2.7, 0])
        self.play(FadeIn(question), run_time=.5)
        self.finish()


class S03Plexin(SpokenScene):
    def construct(self):
        self.at("The answer is plexin")
        p = Rec("plexin", PURPLE, 0, tail_h=1.5)
        self.play(FadeIn(p), FadeIn(mem_bar(0)), run_time=.7)
        self.at("In engineered cells")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=.3)
        heading = T("engineered cells + Sema3A", 28, YELLOW).move_to([0, 3.2, 0])
        cells = VGroup(*[Ellipse(width=3.0, height=2.3, color=TEAL, fill_color=TEAL,
                                 fill_opacity=.12).move_to([x, .3, 0]) for x in (-3.5, 3.5)])
        labels = VGroup(T("neuropilin alone", 26, BLUE).move_to([-3.5, 2, 0]),
                        T("plexin alone", 26, PURPLE).move_to([3.5, 2, 0]))
        self.play(FadeIn(heading), FadeIn(cells), FadeIn(labels), run_time=.5)
        no = T("no shrinking", 28, RED).move_to([0, -1.8, 0])
        self.at("neither protein alone")
        self.play(FadeIn(no), run_time=.4)
        self.at("Together they did")
        both = T("neuropilin + plexin", 28).move_to([0, 2, 0])
        yes = T("cell shrinks", 28, GREEN).move_to([0, -1.8, 0])
        target = cells[0].copy().scale(.55).move_to([0, .3, 0])
        self.play(FadeOut(labels), FadeOut(no), FadeIn(both),
                  Transform(cells[0], target), Transform(cells[1], target), FadeIn(yes), run_time=.8)
        self.at("Most class 3")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=.3)
        # Two distinct routes; the first complex stays for the role labels.
        n, p = complex_at(-4.5, -2.0, ym=-.1, s=1)
        mem = mem_bar(-.1)
        s = semag(-3.25, 2.4, 4.5, .65)
        title = T("most secreted class 3", 24, YELLOW).move_to([-3.25, 3.2, 0])
        self.play(FadeIn(mem), FadeIn(n), FadeIn(p), FadeIn(s), FadeIn(title), run_time=.7)
        self.at("Membrane semaphorins")
        p2 = Rec("plexin", PURPLE, 3.4, ym=-.1, tail_h=1.3)
        uppermem = mem_bar(2.9, 1, 5.9, .18)
        cue = rr(2.7, .55, YELLOW, .6).move_to([3.4, 2.1, 0])
        name = T("semaphorin", 24, YELLOW).move_to(cue)
        title2 = T("membrane cue: direct", 24, YELLOW).move_to([3.4, 3.45, 0])
        stalk = Line([3.4, 2.375, 0], [3.4, 2.9, 0], color=YELLOW, stroke_width=5)
        self.play(FadeIn(p2), FadeIn(uppermem), FadeIn(stalk), FadeIn(cue), FadeIn(name), FadeIn(title2), run_time=.7)
        self.at("Neuropilin catches")
        a = T("catches", 28, BLUE).move_to([-4.5, -2.7, 0])
        self.play(FadeIn(a), Indicate(n.body), run_time=.5)
        self.at("Plexin signals")
        b = T("signals", 28, PURPLE).move_to([-2, -2.7, 0])
        b2 = b.copy().move_to([3.4, -2.7, 0])
        self.play(FadeIn(b), FadeIn(b2), Indicate(p.tail), Indicate(p2.tail), run_time=.5)
        self.finish()


class S04Split(SpokenScene):
    def construct(self):
        mem = mem_bar(YM, -6.3, 1.7)
        n, p = complex_at(-4.5, -2)
        bridge = semag(-3.25, n.top() + .37, 4.6, .7)
        gc = growth(c=(3.0, 0, 0), r=1.7)
        # Replace the shaft with a short right-hand axon.
        gc[0].become(shaft([3, 0, 0], x0=1.9))
        heading = T("deletion comparison", 28, GREY).move_to([0, 3.25, 0])
        self.add(mem, n, p, bridge, gc, heading)
        self.at("A neuropilin without its tail")
        case = T("neuropilin: tail removed", 26, BLUE).move_to([-3.25, -2.8, 0])
        self.play(FadeOut(n.tail), FadeIn(case), run_time=.5)
        self.at("still supported collapse")
        result = T("collapse still occurs", 26, GREEN).move_to([3.8, -2, 0])
        self.play(Transform(gc[1], fan(-.07, .07, 1.2, [3, 0, 0])), FadeOut(gc[2]), FadeIn(result), run_time=.7)
        self.at("A plexin stripped")
        case2 = T("plexin: inner part removed", 26, PURPLE).move_to(case)
        self.play(FadeOut(result), FadeOut(case), FadeIn(case2), FadeIn(n.tail),
                  Transform(gc[1], fan(-.85, .85, 1.7, [3, 0, 0])), FadeIn(gc[2]), FadeOut(p.tail), run_time=.6)
        self.at("blocked")
        blocked = T("response blocked", 26, RED).move_to([3.8, -2, 0])
        sensory = T("sensory neurons", 24, GREY).move_to([3.8, -2.8, 0])
        self.play(FadeIn(blocked), FadeIn(sensory), run_time=.5)
        self.at("So neuropilin catches")
        a = T("catches", 28, BLUE).move_to([-4.5, -2.8, 0])
        self.play(FadeOut(case2), FadeOut(blocked), FadeOut(sensory), FadeIn(p.tail), FadeIn(a), run_time=.5)
        self.at("Plexin signals")
        b = T("signals", 28, PURPLE).move_to([-2, -2.8, 0])
        self.play(FadeIn(b), run_time=.5)
        self.finish()


class S05Gap(SpokenScene):
    def construct(self):
        self.at("Inside the cell")
        mem = mem_bar(2.4)
        tail = rr(.4, 1.5, PURPLE).move_to([-4.5, 1.5, 0])
        pl = T("plexin", 28, PURPLE).move_to([-4.5, 3.1, 0])
        self.play(FadeIn(mem), FadeIn(tail), FadeIn(pl), run_time=.7)
        self.at("acts as a")
        gap = chip("GAP", PURPLE, 30).move_to([-4.5, .3, 0])
        self.play(FadeIn(gap), run_time=.5)
        self.at("It speeds")
        small = chip("small GTPase", ORANGE, 28).move_to([-1, .3, 0])
        badge = chip("GTP", GOLD, 24).move_to([-1, 1.6, 0])
        arrow = Arrow(gap.get_right(), small.get_left(), color=PURPLE, buff=.1)
        hydro = T("faster hydrolysis", 24, PURPLE).move_to([-3.1, -1, 0])
        self.play(FadeIn(small), FadeIn(badge), GrowArrow(arrow), FadeIn(hydro), run_time=.6)
        self.at("switches a small")
        off = chip("OFF", RED, 24).move_to(badge)
        self.play(ReplacementTransform(badge, off), small[0].animate.set_stroke(GREY), run_time=.7)
        self.at("This can lower")
        adhesion = chip("integrin adhesion", ORANGE, 26).move_to([-2.7, -2.3, 0])
        contacts = VGroup(*[Line([x, -2.8, 0], [x, -3.3, 0], color=ORANGE, stroke_width=5)
                            for x in (-3.5, -3, -2.5, -2)])
        self.play(FadeIn(adhesion), FadeIn(contacts), run_time=.4)
        self.play(contacts.animate.set_opacity(.2), run_time=.6)
        self.at("Plexin signaling also engages")
        rho = chip("Rho-family GTPases", PURPLE, 25).move_to([3.6, 1.1, 0])
        branch = Arrow([-.1, 2.4, 0], rho.get_top(), buff=.1, color=PURPLE)
        self.play(FadeIn(rho), GrowArrow(branch), run_time=.6)
        self.at("proteins that act")
        effectors = chip("effector proteins", PURPLE, 26).move_to([3.6, -.4, 0])
        a = Arrow(rho.get_bottom(), effectors.get_top(), buff=.08, color=PURPLE)
        self.play(FadeIn(effectors), GrowArrow(a), run_time=.5)
        self.at("actin and microtubules")
        cyto = T("actin + microtubules", 26, TEAL).move_to([3.6, -2.1, 0])
        b = Arrow(effectors.get_bottom(), cyto.get_top(), buff=.1, color=PURPLE)
        self.play(FadeIn(cyto), GrowArrow(b), run_time=.6)
        self.finish()


class S06Rule(SpokenScene):
    def construct(self):
        c = [-4, 0, 0]
        gc = growth(c, 2.7)
        head = T("local loss of\nactin and adhesion", 28, RED).move_to([3.3, 2, 0])
        # Schematic actin struts and adhesion contacts, not molecular structures.
        actin = VGroup(*[Line([-3.5, 0, 0], [-1.8, y, 0], color=TEAL, stroke_width=4)
                          for y in (-1.3, -.6, .6, 1.3)])
        adhesion = dots([(-1.6, -1.4), (-1, -.6), (-1, .6), (-1.6, 1.4)], ORANGE, .12)
        self.add(gc, actin, adhesion)
        self.at("The net result")
        self.play(FadeIn(head), run_time=.6)
        self.at("On one side")
        dd = dots([(-1, 2), (-.5, 1.5), (0, 1)])
        case = T("one side", 28, YELLOW).move_to([3.3, -.3, 0])
        self.play(FadeIn(dd), FadeIn(case), actin[2:].animate.set_opacity(.12),
                  adhesion[2:].animate.set_opacity(.12), run_time=.5)
        self.at("that means a turn")
        turned = fan(-1.05, .1, 2.7, c)
        self.play(Transform(gc[1], turned), FadeOut(gc[2]), FadeOut(actin), FadeOut(adhesion), run_time=.8)
        self.at("Everywhere at once")
        around = dots([(c[0] + 3.3 * np.cos(a), 3.3 * np.sin(a)) for a in np.linspace(-.85, .85, 5)])
        case2 = T("all around", 28, YELLOW).move_to(case)
        self.play(Transform(gc[1], fan(-.85, .85, 2.7, c)), FadeIn(gc[2]),
                  ReplacementTransform(dd, around), ReplacementTransform(case, case2),
                  FadeIn(actin.set_opacity(1)), FadeIn(adhesion.set_opacity(1)), run_time=.45)
        self.at("it means collapse")
        self.play(Transform(gc[1], fan(-.07, .07, 1.7, c)), FadeOut(gc[2]),
                  FadeOut(actin), FadeOut(adhesion), run_time=.7)
        self.at("This connects")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=.25)
        blocks = VGroup(chip("cue", YELLOW, 28), chip("receptor\ncomplex", PURPLE, 26),
                        chip("actin +\nadhesion loss", RED, 26), chip("turn", TEAL, 28))
        blocks.arrange(RIGHT, buff=.8).move_to([0, 0, 0])
        arrows = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=.08, color=GREY)
                             for a, b in zip(blocks, blocks[1:])])
        self.play(FadeIn(blocks), FadeIn(arrows), run_time=.7)
        self.finish()


class S08Context(SpokenScene):
    def construct(self):
        heading = T("the receiving cell matters", 30).move_to([0, 3.2, 0])
        self.at("The response also depends")
        self.play(FadeIn(heading), run_time=.6)
        self.at("In the developing cortex")
        surface = mem_bar(2.2)
        pia = T("pial surface", 24, GREY).move_to([-4.8, 2.9, 0])
        cue = VGroup(rr(6, .8, YELLOW, .16).move_to([0, 1.65, 0]),
                     T("Sema3A high near surface", 24, YELLOW).move_to([0, 1.65, 0]))
        soma = Polygon([-0.5, -.7, 0], [.5, -.7, 0], [0, .3, 0], color=TEAL,
                       fill_color=TEAL, fill_opacity=.25)
        name = T("developing cortical\npyramidal neuron", 24, TEAL).move_to([-3.7, -.5, 0])
        self.play(FadeOut(heading), FadeIn(surface), FadeIn(pia), FadeIn(cue), FadeIn(soma), FadeIn(name), run_time=.7)
        self.at("repels a pyramidal")
        axon = Arrow([0, -.7, 0], [0, -3.1, 0], color=TEAL, buff=.05, stroke_width=6)
        al = T("axon: away", 26, TEAL).move_to([2.5, -2.6, 0])
        self.play(GrowArrow(axon), FadeIn(al), run_time=.8)
        self.at("attracts its apical")
        dendrite = Arrow([0, .3, 0], [0, 1.1, 0], color=TEAL, buff=.03, stroke_width=7)
        dl = T("apical dendrite: toward", 24, TEAL).move_to([3.6, .6, 0])
        self.play(GrowArrow(dendrite), FadeIn(dl), run_time=.7)
        self.at("The same cue")
        self.play(Indicate(cue, scale_factor=1.03), run_time=.7)
        self.at("Keep the purpose in view")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=.4)
        anatomy, cue, pain, pl, muscle, ml = spinal()
        self.play(FadeIn(anatomy), FadeIn(cue), FadeIn(pl), FadeIn(ml), run_time=.6)
        self.at("signals help growing axons")
        self.play(Create(pain), Create(muscle), run_time=1.2)
        self.at("avoid the wrong territories")
        reminder = T("avoid inappropriate territories", 26, TEAL).move_to([0, -3.45, 0])
        self.play(FadeIn(reminder), run_time=.6)
        self.finish()


class S07End(EndCard):
    LINE = "Semaphorins steer axons by repelling growth cones from wrong territory."
