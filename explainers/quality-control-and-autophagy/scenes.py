"""Quality control and autophagy: count the flux, not the dots  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  BLUE   = autophagosome / making them (the tap)
  PURPLE = LC3-II (dots on membranes, bars on the blot plot)
  ORANGE = lysosome / destroying (the drain)
  RED    = block: bafilomycin, the plugged drain, the misleading reading
  YELLOW = flux (the difference between the two measurements)
  GREY   = cell outline, axes, cytoplasm, structure / ER
  TEAL   = folding helpers / UPR sensors
  GREEN  = folding success; green fluorescent reporter emission
  RED also denotes red fluorescent reporter emission when explicitly labelled
"""
import math
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


def pt(x, y):
    return np.array([x, y, 0.0])


def autop(center, r=0.3, color=BLUE):
    c = pt(*center[:2])
    return VGroup(Circle(radius=r, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.12).move_to(c),
                  Circle(radius=r * 0.6, stroke_color=color, stroke_width=3).move_to(c))


def ring_dots(center, r, n, color=PURPLE, dr=0.07, start=0.0, span=2 * PI):
    c = np.array(center, float)
    out = VGroup()
    for i in range(n):
        a = start + span * i / n
        out.add(Dot(c + r * np.array([math.cos(a), math.sin(a), 0]), radius=dr, color=color))
    return out


def lbl(text, color=GREY, size=24):
    return T(text, size, color)


# ---- the sink ---------------------------------------------------------------------------------
class Sink:
    """basin, tap pipe and drain pipe centred at (cx, cy). Water height is set with water(h)."""

    def __init__(self, cx, cy, hw=1.9, wall=1.3):
        self.cx, self.cy, self.hw, self.wall = cx, cy, hw, wall
        self.basin = VMobject(color=GREY, stroke_width=6).set_points_as_corners(
            [pt(cx - hw, cy + wall), pt(cx - hw, cy - wall), pt(cx + hw, cy - wall), pt(cx + hw, cy + wall)])
        self.tx = cx - 1.0
        self.dx = cx + 1.15
        self.tap = VGroup(Line(pt(self.tx, cy + 2.55), pt(self.tx, cy + 1.75), color=BLUE, stroke_width=9),
                          Line(pt(self.tx - 0.35, cy + 2.55), pt(self.tx + 0.35, cy + 2.55), color=BLUE, stroke_width=9))
        self.stream = VGroup(*[Circle(radius=0.07, stroke_width=0, fill_color=BLUE, fill_opacity=0.9)
                               .move_to(pt(self.tx, cy + 1.5 - 0.35 * k)) for k in range(3)])
        self.drain = VGroup(Line(pt(self.dx, cy - wall), pt(self.dx, cy - wall - 0.75), color=ORANGE, stroke_width=9),
                            Rectangle(width=0.5, height=0.12, stroke_width=0, fill_color=ORANGE, fill_opacity=1)
                            .move_to(pt(self.dx, cy - wall)))
        self.plug = Rectangle(width=0.62, height=0.2, stroke_width=0, fill_color=RED, fill_opacity=1) \
            .move_to(pt(self.dx, cy - wall + 0.1))

    def water(self, h, color=BLUE, op=0.35):
        r = Rectangle(width=2 * self.hw - 0.1, height=max(h, 0.02), stroke_width=0, fill_color=color, fill_opacity=op)
        return r.move_to(pt(self.cx, self.cy - self.wall + 0.05 + max(h, 0.02) / 2))


# ---- the blot plot -----------------------------------------------------------------------------
U = 0.9
BASE = -2.3
AX = -5.0
BW = 1.0


def bar(cx, v, strong):
    return Rectangle(width=BW, height=v * U, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE,
                     fill_opacity=0.85 if strong else 0.45).move_to(pt(cx, BASE + v * U / 2))


def seg(cx, v0, v1):
    return Rectangle(width=BW, height=(v1 - v0) * U, stroke_width=0, fill_color=YELLOW, fill_opacity=0.95) \
        .move_to(pt(cx, BASE + (v0 + v1) / 2 * U))


def vlab(cx, v):
    return M(f"{v:.1f}", 22, TEXT).move_to(pt(cx, BASE + v * U + 0.25))


def fluxlab(cx, v0, v1):
    return M(f"{v1:.1f} − {v0:.1f} = {v1 - v0:.1f}", 24, YELLOW).move_to(pt(cx, 2.55))


def axes():
    ax = VGroup(Line(pt(AX, BASE), pt(AX, BASE + 5 * U), color=GREY, stroke_width=3),
                Line(pt(AX, BASE), pt(5.6, BASE), color=GREY, stroke_width=3))
    for k in range(5):
        ax.add(Line(pt(AX - 0.08, BASE + k * U), pt(AX, BASE + k * U), color=GREY, stroke_width=3))
        ax.add(M(str(k), 22, GREY).move_to(pt(AX - 0.4, BASE + k * U)))
    ylab = T("LC3-II / actin", 22, GREY).rotate(PI / 2).move_to(pt(-6.0, BASE + 2 * U))
    ax.add(ylab)
    return ax


def legend():
    a = Square(0.22, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.45)
    ta = T("without bafilomycin", 22, TEXT)
    b = Square(0.22, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.8)
    tb = T("with bafilomycin", 22, TEXT)
    row1 = VGroup(a, ta).arrange(RIGHT, buff=0.15)
    row2 = VGroup(b, tb).arrange(RIGHT, buff=0.15)
    return VGroup(row1, row2).arrange(RIGHT, buff=0.8).move_to(pt(0.2, 3.2))


def glabel(cx, name):
    return T(name, 26, TEXT).move_to(pt(cx, BASE - 0.4))


class S00Title(TitleCard):
    LESSON = "Protein quality control and organelle turnover"
    TITLE = "Protein Quality Control and Organelle Turnover"


# Simple compartment and cargo schematics, never molecular structures.
def compartment():
    box = RoundedRectangle(width=5.0, height=4.5, corner_radius=0.35,
                           stroke_color=GREY, stroke_width=4, fill_color=GREY,
                           fill_opacity=0.05).move_to(pt(-3.4, 0))
    return VGroup(box, T("ER · folding compartment", 25, GREY).move_to(pt(-3.4, 2.65)))


def membrane_badge(text, color, size=24):
    badge = chip(text, color, size)
    backing = RoundedRectangle(width=badge.width, height=badge.height,
                               corner_radius=0.14, stroke_width=0,
                               fill_color=BG, fill_opacity=1)
    return VGroup(backing, badge)


def arrow(a, b, color=GREY):
    return Arrow(pt(*a), pt(*b), buff=0.08, color=color, stroke_width=4)


def cup(c, span, r=1.5):
    start = 3 * PI / 2 - span / 2
    return VGroup(*[Arc(radius=rad, start_angle=start, angle=span,
                       arc_center=c, color=BLUE, stroke_width=5)
                    for rad in (r, r * 0.72)])


def lyso(c, r=1.65):
    return VGroup(Circle(radius=r, stroke_color=ORANGE, stroke_width=5,
                         fill_color=ORANGE, fill_opacity=0.12).move_to(c),
                  T("acidic lysosome", 25, ORANGE).move_to(c + UP * (r + 0.45)))


class S01Puzzle(SpokenScene):
    def construct(self):
        er = compartment()
        protein = chip("new protein", GREY, 26).move_to(pt(-3.4, 0))
        self.at("a cell checks")
        self.play(FadeIn(er), FadeIn(protein), run_time=0.7)
        self.at("get help folding")
        good = chip("folded", GREEN, 26).move_to(pt(-3.4, 1.05))
        golgi = chip("Golgi", GREY, 28).move_to(pt(3.5, 1.5))
        path = arrow((-0.7, 1.5), (2.5, 1.5), GREEN)
        self.play(Transform(protein, good), FadeIn(golgi), GrowArrow(path), run_time=1)
        self.play(protein.animate.move_to(pt(1.0, 2.15)), run_time=0.7)
        self.at("a protein that keeps failing")
        bad = chip("persistent failure", RED, 25).move_to(pt(-3.4, -1.0))
        self.play(FadeIn(bad), run_time=0.6)
        self.at("held back")
        self.play(Indicate(bad, color=RED), run_time=0.6)
        proteasome = chip("proteasome", ORANGE, 28).move_to(pt(3.5, -1.5))
        route = arrow((-0.7, -1.5), (2.0, -1.5), ORANGE)
        cyt = T("cytosol", 25, GREY).move_to(pt(3.5, -2.4))
        self.at("then sent to the cytosolic")
        self.play(FadeIn(proteasome), FadeIn(cyt), GrowArrow(route),
                  bad.animate.move_to(pt(0.8, -0.6)), run_time=0.9)
        ub = chip("Ub", RED, 22).next_to(bad, UP, buff=0.15)
        self.play(FadeIn(ub), run_time=0.4)
        name = T("ER-associated degradation · ERAD", 27, ORANGE).move_to(pt(0, -3.15))
        self.at("associated degradation")
        self.play(FadeIn(name), VGroup(bad, ub).animate.move_to(pt(3.5, -0.5)), run_time=0.9)
        self.play(FadeOut(bad, scale=0.2), FadeOut(ub, scale=0.2), run_time=0.6)
        self.at("proteins misfold")
        bad2 = chip("misfolded", RED, 26).move_to(pt(-3.4, -1.0))
        self.play(FadeIn(bad2), run_time=0.5)
        self.at("destroy the failures")
        self.play(bad2.animate.move_to(proteasome), run_time=0.9)
        self.play(FadeOut(bad2, scale=0.2), run_time=0.5)
        self.at("folding help and disposal")
        self.play(Indicate(er, color=TEAL), Indicate(proteasome, color=ORANGE), run_time=1)
        self.finish()


class S01Folding(SpokenScene):
    def construct(self):
        er = compartment()
        # Release from a chaperone remains inside the ER lumen.
        er[0].stretch_to_fit_width(11.8).move_to(ORIGIN)
        p = chip("new chain", GREY, 26).move_to(pt(-3.6, 0))
        bip = chip("BiP", TEAL, 27).move_to(pt(-3.6, -1.6))
        self.at("helps a new chain")
        self.play(FadeIn(er), FadeIn(p), FadeIn(bip), run_time=0.6)
        self.play(bip.animate.next_to(p, DOWN, buff=0.1), run_time=0.6)
        lectin = chip("calnexin / calreticulin", TEAL, 25).move_to(pt(-3.4, -1.4))
        self.at("and calreticulin hold")
        self.play(ReplacementTransform(bip, lectin), p.animate.move_to(pt(-3.4, 0)), run_time=0.7)
        glc = chip("glucose", GREEN, 22).move_to(pt(-3.4, 0.85))
        self.at("with a glucose tag")
        self.play(FadeIn(glc), lectin.animate.next_to(p, DOWN, buff=0.1), run_time=0.6)
        released = T("released · still non-native", 24, RED).move_to(pt(2.8, 1.6))
        self.at("if a released protein")
        self.play(FadeOut(glc, shift=UP * 0.4), p.animate.move_to(pt(2.8, 0.4)),
                  FadeIn(released), run_time=0.8)
        uggt = chip("UGGT", TEAL, 26).move_to(pt(2.8, -1.0))
        self.at("UGGT adds")
        self.play(FadeIn(uggt), run_time=0.5)
        glc.move_to(pt(2.8, 1.05))
        self.at("glucose back")
        self.play(FadeIn(glc), run_time=0.4)
        self.at("for another round")
        self.play(VGroup(p, glc).animate.move_to(pt(-3.4, 0.3)),
                  FadeOut(released), FadeOut(uggt), run_time=0.9)
        self.at("persistent failures leave")
        bad = chip("persistent failure", RED, 25).move_to(pt(-3.4, 0))
        self.play(Transform(p, bad), FadeOut(glc), FadeOut(lectin),
                  Transform(er[0], compartment()[0]), run_time=0.6)
        route = T("ERAD", 30, ORANGE).move_to(pt(2.8, 2.7))
        self.play(FadeIn(route), run_time=0.4)
        ub = chip("Ub", RED, 22).next_to(p, UP, buff=0.15)
        self.at("ubiquitin tags the protein")
        self.play(FadeIn(ub), run_time=0.5)
        motor = chip("ATPase", TEAL, 26).move_to(pt(1.0, -1.2))
        self.at("pulls it out")
        self.play(FadeIn(motor), VGroup(p, ub).animate.move_to(pt(1.0, 0.2)), run_time=0.7)
        machine = chip("proteasome", ORANGE, 27).move_to(pt(4.2, 0.2))
        self.at("the proteasome destroys")
        self.play(FadeIn(machine), run_time=0.3)
        self.play(VGroup(p, ub).animate.move_to(machine), run_time=0.45)
        self.play(FadeOut(p, scale=0.2), FadeOut(ub, scale=0.2), run_time=0.35)
        self.finish()


class S02Route(SpokenScene):
    def construct(self):
        machine = chip("proteasome", ORANGE, 29).move_to(pt(2.8, 0))
        p = chip("single protein", GREY, 26).move_to(pt(-3.5, 0))
        self.at("the proteasome destroys")
        self.play(FadeIn(machine), FadeIn(p), run_time=0.5)
        self.play(p.animate.move_to(machine), run_time=0.8)
        self.play(FadeOut(p, scale=0.2), run_time=0.4)
        C = pt(-3.3, 0)
        cargo = VGroup(Ellipse(width=1.2, height=0.8, color=GREY,
                              fill_color=GREY, fill_opacity=0.3).move_to(C),
                       Dot(C + UP * 0.7, radius=0.12, color=GREY))
        cargo_label = T("organelle", 23, GREY).move_to(C + DOWN * 0.85)
        lys = lyso(pt(3.5, 0))
        self.at("for whole organelles")
        self.play(FadeOut(machine), FadeIn(cargo), FadeIn(cargo_label), FadeIn(lys), run_time=0.8)
        a = cup(C, 2.6)
        self.at("a membrane cup grows")
        self.play(Create(a), FadeOut(cargo_label), run_time=0.8)
        self.play(Transform(a, cup(C, 4.8)), run_time=1)
        self.at("closes into an autophagosome")
        self.play(Transform(a, cup(C, 2 * PI - 0.001)), run_time=0.8)
        lab = T("autophagosome", 26, BLUE).move_to(pt(-3.3, 2.1))
        self.play(FadeIn(lab), run_time=0.4)
        self.at("two membranes")
        self.play(Indicate(a[0], color=BLUE), Indicate(a[1], color=BLUE), run_time=0.6)
        self.at("it fuses with")
        self.play(VGroup(a, cargo).animate.move_to(pt(3.5, 0)), FadeOut(lab), run_time=1)
        self.play(FadeOut(a[0]), Indicate(lys[0], color=ORANGE), run_time=0.5)
        self.at("the inner membrane")
        self.play(FadeOut(a[1], scale=0.3), FadeOut(cargo, scale=0.3), run_time=1.3)
        blocks = VGroup(*[Dot(pt(3.5 + (i-1)*0.3, 0), radius=0.1, color=GREY) for i in range(3)])
        self.at("the building blocks return")
        self.play(FadeIn(blocks), run_time=0.3)
        self.play(*[d.animate.move_to(pt(-1.8, (i-1)*0.8)) for i,d in enumerate(blocks)], run_time=1.1)
        reuse = T("cytosol · reuse", 28, GREY).move_to(pt(-2.0, -1.8))
        self.play(FadeIn(reuse), run_time=0.5)
        self.finish()


class S03Stress(SpokenScene):
    def construct(self):
        er = RoundedRectangle(width=10.8, height=1.2, corner_radius=0.2,
                              stroke_color=GREY).move_to(pt(0, 2.2))
        load = VGroup(*[chip("unfolded", RED, 23).move_to(pt(x,2.2)) for x in (-3.6,0,3.6)])
        self.at("what if unfolded proteins")
        self.play(Create(er), FadeIn(load, lag_ratio=0.15), run_time=0.8)
        outcome = VGroup(T("protein synthesis ↓", 27, TEAL),
                         T("folding machinery ↑", 27, TEAL)).arrange(RIGHT, buff=1.2).move_to(pt(0,-2.1))
        self.at("slows protein synthesis")
        self.play(FadeIn(outcome[0]), run_time=0.7)
        self.at("makes more folding machinery")
        self.play(FadeIn(outcome[1]), run_time=0.7)
        sensors = VGroup(*[chip(n, TEAL, 30).move_to(pt(x,0.8))
                           for x,n in zip((-4.4,0,4),("IRE1","PERK","ATF6"))])
        self.at("three branches")
        self.play(FadeIn(sensors), run_time=0.7)
        # Keep each branch independent when ATF6 moves to its cleavage position.
        self.remove(sensors)
        self.add(*sensors)
        rna = VGroup(chip("XBP1", GREY, 27), chip("intron", RED, 24), chip("mRNA", GREY, 27)).arrange(RIGHT,buff=0.16).move_to(pt(-4.4,-0.5))
        self.at("IRE1 splices")
        self.play(FadeIn(rna), run_time=0.5)
        self.play(FadeOut(rna[1],shift=DOWN*0.5), rna[0].animate.shift(RIGHT*0.3), rna[2].animate.shift(LEFT*0.3),run_time=0.7)
        tr = T("most translation ↓",27,TEAL).move_to(pt(0,-0.5))
        self.at("slows most translation")
        self.play(FadeIn(tr),run_time=0.6)
        golgi = chip("Golgi",GREY,28).move_to(pt(4.5,-0.35))
        to_golgi = Arrow(sensors[2].get_bottom(), golgi.get_top(),
                         buff=0.12, color=TEAL, stroke_width=4)
        self.at("travels to the Golgi")
        self.play(FadeIn(golgi),GrowArrow(to_golgi),run_time=0.65)
        self.at("to be cut")
        fragment=chip("ATF6",TEAL,27).move_to(pt(4.5,-1.35))
        self.play(ReplacementTransform(sensors[2],fragment),FadeOut(to_golgi),run_time=0.5)
        death=VGroup(T("unresolved stress",25,RED).move_to(pt(-2,-3.1)),
                     arrow((-0.1,-3.1),(1.2,-3.1),RED),
                     T("can drive cell death",25,RED).move_to(pt(3.2,-3.1)))
        self.at("unresolved stress")
        self.play(FadeIn(death),run_time=0.7)
        self.finish()


class S04Selective(SpokenScene):
    def construct(self):
        cargo=chip("selected cargo",GREY,26).move_to(pt(-0.6,0.9))
        a=cup(pt(0,0),3.6,2.1)
        receptor=chip("receptor",TEAL,24).move_to(pt(0,-0.45))
        lc=membrane_badge("LC3",PURPLE,24).move_to(pt(1.6,-1.1))
        links=VGroup(arrow((-0.6,0.5),(0,-0.1),TEAL),arrow((0.7,-0.6),(1.3,-1.0),TEAL))
        self.at("autophagy can also choose")
        self.play(FadeIn(cargo),Create(a),run_time=0.7)
        self.at("receptors link particular cargo")
        self.play(FadeIn(receptor),Create(links),run_time=0.7)
        self.at("the LC3 family")
        self.play(FadeIn(lc),run_time=0.6)
        mito=VGroup(Ellipse(width=3.4,height=1.5,stroke_color=GREY,fill_color=GREY,fill_opacity=0.12),
                    T("mitochondrion",26,GREY)).move_to(pt(0,0))
        self.at("mitophagy removes mitochondria")
        self.play(FadeOut(cargo),FadeOut(a),FadeOut(receptor),FadeOut(lc),FadeOut(links),FadeIn(mito),run_time=0.7)
        example=T("Cultured-cell example",29,GREY).move_to(pt(0,3.0))
        dep=T("depolarized",26,RED).move_to(pt(0,1.15))
        self.at("in cultured cells")
        self.play(FadeIn(example),run_time=0.5)
        pink=chip("PINK1",TEAL,25).move_to(pt(-2.3,0.8))
        self.at("pink one builds up")
        self.play(FadeIn(pink),FadeIn(dep),run_time=0.6)
        park=chip("Parkin",TEAL,25).move_to(pt(4,0.7))
        self.at("and recruits parkin")
        self.play(FadeIn(park),run_time=0.3)
        self.play(park.animate.move_to(pt(2.3,0.8)),run_time=0.65)
        ub=VGroup(*[chip("Ub",RED,22).move_to(pt(x,-0.95)) for x in (-1,0,1)])
        self.at("parkin adds ubiquitin tags")
        self.play(FadeIn(ub),run_time=0.7)
        rec=chip("receptors",TEAL,25).move_to(pt(0,-3.1))
        self.at("receptors bind the tagged")
        self.play(FadeIn(rec),run_time=0.6)
        engulf=cup(pt(0,0),4.3,2.55)
        marker=chip("LC3",PURPLE,24).move_to(pt(2.8,-1.8))
        self.at("recruit the machinery")
        connect=VGroup(arrow((0,-2.7),(0,-1.3),TEAL),
                       arrow((1.0,-2.9),(2.4,-2.0),TEAL))
        # Sensor names have served their beat; clear the future membrane path.
        self.play(FadeOut(pink),FadeOut(park),Create(engulf),
                  FadeIn(marker),Create(connect),run_time=0.6)
        self.at("that engulfs it")
        self.play(Transform(engulf,cup(pt(0,0),2*PI-0.001,2.55)),run_time=0.75)
        self.finish()


class S03Block(SpokenScene):
    def construct(self):
        ves=VGroup(*[autop(pt(x,0),0.6) for x in (-2,0,2)])
        title=T("More autophagosomes?",34,BLUE).move_to(pt(0,2.7))
        made=T("increased formation",28,BLUE).move_to(pt(-3,-1.6))
        clear=T("impaired clearance",28,ORANGE).move_to(pt(3,-1.6))
        self.at("finally how do you measure")
        self.play(FadeIn(title),FadeIn(ves),run_time=0.6)
        self.at("more are made")
        self.play(FadeIn(made),ves.animate.shift(UP*0.3),run_time=0.5)
        self.at("fewer are destroyed")
        self.play(FadeIn(clear),run_time=0.5)
        # Schematic amounts: no invented numerical measurements.
        b0,b1=bar(-2.1,1.6,False),bar(2.1,3.6,True)
        labels=VGroup(T("without bafilomycin",25,TEXT).move_to(pt(-2.6,-2.8)),
                      T("with bafilomycin",25,TEXT).move_to(pt(2.6,-2.8)),
                      T("LC3-II · schematic comparison",30,PURPLE).move_to(pt(0,2.9)))
        self.at("compare")
        self.play(FadeOut(title),FadeOut(ves),FadeOut(made),FadeOut(clear),
                  FadeIn(labels),GrowFromEdge(b0,DOWN),GrowFromEdge(b1,DOWN),run_time=0.9)
        assumption=T("Assume a complete lysosomal block",26,RED).move_to(pt(0,2.05))
        self.at("assuming a complete lysosomal block")
        self.play(FadeIn(assumption),run_time=0.7)
        delta=seg(2.1,1.6,3.6)
        meaning=T("LC3-II otherwise degraded",27,YELLOW).move_to(pt(0,1.2))
        self.at("the difference reveals")
        self.play(FadeIn(delta),FadeIn(meaning),run_time=0.8)
        self.at("check cargo")
        cargo=chip("p62 · cargo measurement",TEAL,27).move_to(pt(0,1.6))
        self.play(*[FadeOut(m) for m in (labels,b0,b1,assumption,delta,meaning)],FadeIn(cargo),run_time=0.7)
        carrier=chip("LC3 · carrier",PURPLE,27).move_to(pt(0,2.8))
        self.at("marks the carrier")
        self.play(FadeIn(carrier),run_time=0.5)
        reporters=VGroup(T("Tandem red / green LC3 reporter",27,TEXT).move_to(pt(0,0.25)),
            T("lysosomal delivery",25,ORANGE).move_to(pt(-3.2,-2.25)),
            T("pre-fusion block",25,RED).move_to(pt(3.2,-2.25)))
        red=VGroup(Dot(pt(-3.2,-1.1),radius=0.22,color=RED),T("red only",24,TEXT).move_to(pt(-3.2,-2.9)))
        both=VGroup(Dot(pt(2.95,-1.1),radius=0.22,color=RED),Dot(pt(3.45,-1.1),radius=0.22,color=GREEN),
                    T("red + green",24,TEXT).move_to(pt(3.2,-2.9)))
        self.at("and fluorescent reporters")
        self.play(FadeIn(reporters),FadeIn(red),FadeIn(both),run_time=0.8)
        self.at("to judge turnover")
        self.play(Indicate(cargo,color=TEAL),Indicate(carrier,color=PURPLE),run_time=0.7)
        self.finish()


class S07End(EndCard):
    LINE = "Failed ER proteins go to the proteasome; whole organelles to the lysosome."
