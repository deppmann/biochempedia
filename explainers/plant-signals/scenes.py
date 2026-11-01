"""Plant Signals Steer Growth  (Biochemistrypedia explainer, Organismal Biology)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = light (lamp rays, the lit side)
  ORANGE = the signal that moves: auxin, or "something passes down"
  GREEN  = living plant tissue (seedlings, coleoptiles, flanks)
  BLUE   = light receptor / flowering signal FT
  GREY   = ground, the opaque cap, outlines, notes
  TEAL   = other hormone signals / mobile defence signal
  PURPLE = the PIN carrier in the cell membrane
  RED    = the question, and a blocked signal
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
Z0, Z1 = 0.12, 0.62          # the zone below the tip where the bend forms


# ---------------------------------------------------------------------------------------------
# helpers: a stem is a band along a centre line whose heading turns inside the bend zone
# ---------------------------------------------------------------------------------------------
def _heading(s, bend, z0=Z0, z1=Z1):
    u = np.clip((s - z0) / (z1 - z0), 0, 1)
    return bend * (u * u * (3 - 2 * u))


def centre(base, h, bend, n=40, z0=Z0, z1=Z1):
    """centre line points, headings, from base up to the tip. bend > 0 leans LEFT (toward a lamp at left)."""
    pts, ths = [np.array(base, float)], [0.0]
    ds = h / n
    for i in range(1, n + 1):
        s = (i - 0.5) / n
        th = _heading(s, bend, z0, z1)
        d = np.array([-np.sin(th), np.cos(th), 0])
        pts.append(pts[-1] + d * ds)
        ths.append(_heading(i / n, bend, z0, z1))
    return pts, ths


def pose(base, h, bend, s, n=40, z0=Z0, z1=Z1):
    pts, ths = centre(base, h, bend, n, z0, z1)
    i = int(round(s * n))
    return pts[i], ths[i]


def band(base, h, bend, a, b, s0=0.0, s1=1.0, n=40, color=GREEN, op=0.28, sw=3, z0=Z0, z1=Z1):
    """polygon of the stem between lateral offsets a..b (left negative) and arc fractions s0..s1."""
    pts, ths = centre(base, h, bend, n, z0, z1)
    i0, i1 = int(round(s0 * n)), int(round(s1 * n))
    L, R = [], []
    for i in range(i0, i1 + 1):
        nx = np.array([np.cos(ths[i]), np.sin(ths[i]), 0])      # points to the right of the heading
        L.append(pts[i] + nx * a)
        R.append(pts[i] + nx * b)
    poly = Polygon(*(L + R[::-1]), stroke_color=color, stroke_width=sw, fill_color=color, fill_opacity=op)
    return poly


def stem(base, h, bend, w=0.56, **kw):
    return band(base, h, bend, -w / 2, w / 2, **kw)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def rays(x, y, n=3, gap=0.62, length=0.8):
    return VGroup(*[arr([x, y + (i - (n - 1) / 2) * gap, 0], [x + length, y + (i - (n - 1) / 2) * gap, 0], YELLOW, w=5, tip=0.2)
                    for i in range(n)])


def ground(x, y, w=2.2):
    return Rectangle(width=w, height=0.18, stroke_color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=0.4).move_to([x, y - 0.09, 0])


def label(txt, x, y, size=24, color=GREY, **kw):
    return T(txt, size, color, **kw).move_to([x, y, 0])


def rot_to(mob, th):
    return mob.rotate(th, about_point=mob.get_center())


def at_pose(mob, p, th):
    mob.move_to(p)
    mob.rotate(th, about_point=p)
    return mob


# Additional schematics retain the original band-and-blob drawing language.
def dots(points, color=ORANGE):
    return VGroup(*[Dot(p, radius=0.11, color=color) for p in points])


def horizontal(x, y, bend=0, h=3.8, w=0.65):
    return stem([0, 0, 0], h, bend, w=w).rotate(-PI / 2, about_point=ORIGIN).shift([x, y, 0])


def comparison():
    root = horizontal(-5.6, 0.25, -0.65)
    shoot = horizontal(1.4, 0.25, 0.65)
    return VGroup(root, shoot,
        label('ROOT', -3.4, 2.5, 30, GREEN), label('SHOOT', 3.4, 2.5, 30, GREEN),
        label('lower side: less elongation', -3.4, -2.2, 24, ORANGE),
        label('lower side: more elongation', 3.4, -2.2, 24, ORANGE),
        dots([[x, -0.06, 0] for x in (-5.25, -4.8, -4.35, 1.75, 2.2, 2.65)]))


def plant():
    stalk = stem([0, -2.3, 0], 4.4, 0, w=0.25)
    leaves = VGroup(*[Ellipse(width=1.8, height=0.65, color=GREEN, fill_opacity=0.28)
        .rotate(a).move_to([x, y, 0]) for x, y, a in [(-0.8, -0.6, -0.35), (0.8, 0.5, 0.35)]])
    return VGroup(stalk, leaves)


def seed(x, y):
    return Ellipse(width=1.4, height=0.9, color=GREEN, fill_opacity=0.3).rotate(0.3).move_to([x, y, 0])


def cell(x=0, y=0, w=3.2, h=2.8):
    return RoundedRectangle(width=w, height=h, corner_radius=0.2, color=GREEN,
        stroke_width=3, fill_color=GREEN, fill_opacity=0.12).move_to([x, y, 0])


def carrier(x, y):
    return RoundedRectangle(width=0.28, height=0.75, corner_radius=0.1, color=PURPLE,
        fill_opacity=0.7).move_to([x, y, 0])


class S00Title(TitleCard):
    LESSON = 'Plant hormones and responses'
    TITLE = 'Plant Signals Steer Growth'

    def construct(self):
        title = T(self.TITLE, 46, TEXT, font=TITLE_FONT).move_to([0, 2.55, 0])
        light = VGroup(Circle(radius=0.25, color=YELLOW, fill_opacity=0.8).move_to([-5.8, 0, 0]), rays(-5.3, 0))
        shoot = stem([-3.4, -1.9, 0], 3.0, 0, w=0.45)
        gravity = VGroup(horizontal(1.3, 0, 0, h=2.8, w=0.4), horizontal(1.3, -0.7, 0, h=2.8, w=0.4))
        self.add(title, light, shoot, gravity)
        self.play(Transform(shoot, stem([-3.4, -1.9, 0], 3.0, 0.6, w=0.45)),
                  Transform(gravity, VGroup(horizontal(1.3, 0, 0.6, h=2.8, w=0.4), horizontal(1.3, -0.7, -0.6, h=2.8, w=0.4))), run_time=1.4)
        self.finish()


class S01Bend(SpokenScene):
    def construct(self):
        bx, by, h = -0.4, -2.1, 3.9
        left = band([bx, by, 0], h, 0, -0.65, 0)
        right = band([bx, by, 0], h, 0, 0, 0.65)
        lamp = VGroup(Circle(radius=0.35, color=YELLOW, fill_opacity=0.8).move_to([-5.7, 0.7, 0]),
                      rays(-5.1, 0.7, length=1.5), label('lamp', -5.7, 1.5, 26, YELLOW))
        name = label('oat seedling', bx, -2.85, 28)
        self.at('Light an oat')
        self.add(left, right, lamp, name)
        self.at('bends toward the lamp')
        self.play(Transform(left, band([bx, by, 0], h, 0.45, -0.65, 0)),
                  Transform(right, band([bx, by, 0], h, 0.45, 0, 0.65)), run_time=0.8)
        flank_poses = [pose([bx, by, 0], h, 0.45, f) for f in (0.3, 0.45, 0.6, 0.75)]
        signal = dots([p - 0.3 * np.array([np.cos(th), np.sin(th), 0]) for p, th in flank_poses])
        aux = label('auxin', 3.2, 1.6, 30, ORANGE)
        self.at('a plant hormone')
        self.play(FadeIn(signal), FadeIn(aux), run_time=0.4)
        self.at('moves toward the shaded flank')
        self.play(*[d.animate.move_to(p + 0.42 * np.array([np.cos(th), np.sin(th), 0])) for d, (p, th) in zip(signal, flank_poses)], run_time=0.8)
        faster = VGroup(arr([1, -1.7, 0], [1, 0.6, 0], GREEN),
                        label('shaded side', 3.3, 0.1, 26), label('elongates faster', 3.3, -0.5, 26, GREEN))
        self.at('That side elongates faster')
        self.play(FadeIn(faster), right.animate.stretch(1.12, 1, about_point=[bx, by, 0]), run_time=0.7)
        self.at('so the chute bends')
        self.play(Transform(left, band([bx, by, 0], h, 0.7, -0.65, 0)),
                  Transform(right, band([bx, by, 0], h, 0.7, 0, 0.65)), FadeOut(signal), run_time=0.9)
        self.at('Gravity also redirects')
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.35)
        organs = VGroup(horizontal(-5.6, 0.2), horizontal(1.4, 0.2))
        names = VGroup(label('SHOOT', -3.4, 2.6, 30, GREEN), label('ROOT', 3.4, 2.6, 30, GREEN))
        self.play(FadeIn(organs), FadeIn(names), run_time=0.5)
        lower = dots([[x, -0.1, 0] for x in (-5.2, -4.7, -4.2, 1.8, 2.3, 2.8)])
        self.at('It collects on the lower side')
        self.play(FadeIn(lower), run_time=0.5)
        self.at('making a chute curve up')
        self.play(Transform(organs[0], horizontal(-5.6, 0.2, 0.65)), run_time=0.7)
        self.at('and a root curve down')
        self.play(Transform(organs[1], horizontal(1.4, 0.2, -0.65)), run_time=0.7)
        chain = VGroup(T('Auxin redistribution', 26, ORANGE), T('→  unequal elongation  →', 26, GREEN), T('bending', 26, GREEN)).arrange(RIGHT, buff=0.25).move_to([0, -2.8, 0])
        self.at('by moving a chemical signal')
        self.play(FadeIn(chain), run_time=0.6)
        self.at('Unequal growth on opposite sides')
        self.play(Indicate(organs, color=GREEN), run_time=0.8)
        self.finish()


class S05Sideways(SpokenScene):
    def construct(self):
        shoot = stem([-3.8, -2, 0], 3.8, 0.5, w=0.6)
        title = label('Arabidopsis hypocotyl', 0, 3.1, 32, TEXT)
        sub = label('stem below the seed leaves', 0, 2.5, 24)
        c = cell(1, 0, 3.6, 3)
        pins = VGroup(carrier(0.4, -1.5).rotate(PI/2), carrier(1.6, -1.5).rotate(PI/2))
        self.at('How does auxin change direction')
        self.add(shoot)
        self.at('In Arabidopsis hypocotyls')
        self.play(shoot.animate.scale(0.75).move_to([-4.6, 0, 0]), FadeIn(title), FadeIn(sub), FadeIn(c), run_time=0.8)
        self.at('a carrier called')
        pl = label('PIN3: auxin export', 1, -2.2, 26, PURPLE)
        self.play(FadeIn(pins), FadeIn(pl), run_time=0.5)
        self.at('one face of a cell')
        self.play(Indicate(pins, color=PURPLE), run_time=0.6)
        self.at('Repositioning them steers auxin')
        flow = arr([1.7, 0, 0], [4.6, 0, 0], ORANGE)
        ds = dots([[0, 0, 0], [0.5, 0, 0], [1, 0, 0]])
        shaded = label('toward shaded flank', 4.5, -1.3, 24, ORANGE)
        self.play(Transform(pins, VGroup(carrier(2.8, -0.6), carrier(2.8, 0.6))), FadeIn(ds), run_time=0.65)
        self.play(GrowArrow(flow), ds.animate.shift(RIGHT * 2.5), FadeIn(shaded), run_time=0.8)
        self.at('A blue light receptor')
        receptor = chip('phototropin', BLUE, 26).move_to([0, 1.85, 0])
        receptor_leader = Line([-0.8, 1.55, 0], [-0.8, 1.05, 0], color=BLUE, stroke_width=3)
        light = rays(-6.2, 1.5, n=2, gap=0.5, length=1)
        self.play(FadeIn(receptor), Create(receptor_leader), FadeIn(light), run_time=0.5)
        self.at('detects the light')
        faster = label('shaded side elongates faster', -2.5, -3.1, 26, GREEN)
        self.play(Indicate(receptor, color=BLUE), Transform(shoot, stem([-4.6, -1.45, 0], 2.9, 0.75, w=0.45)), FadeIn(faster), run_time=0.7)
        self.finish()


class S08Gravity(SpokenScene):
    def construct(self):
        seedling = VGroup(stem([0, 0, 0], 2.1, 0, w=0.4), stem([0, 0, 0], 2.1, 0, w=0.3).rotate(PI, about_point=ORIGIN))
        self.at('Now lay a seedling')
        self.add(seedling)
        self.play(Rotate(seedling, -PI/2), run_time=0.8)
        self.at('In Arabidopsis root cap cells')
        self.play(FadeOut(seedling), run_time=0.3)
        c = cell(-2.5, 0, 3, 2.6)
        title = label('Arabidopsis root-cap cell', -2.5, 2.4, 28, TEXT)
        pin = carrier(-1, 0)
        pl = label('PIN3', -4.6, -1.9, 26, PURPLE)
        self.play(FadeIn(c), FadeIn(title), FadeIn(pin), FadeIn(pl), run_time=0.5)
        self.at('relocates to the new lower face')
        self.play(pin.animate.rotate(PI/2).move_to([-2.5, -1.3, 0]), run_time=0.8)
        self.at('redirecting oxen downward')
        flow = arr([-2.5, -0.2, 0], [-2.5, -2.9, 0], ORANGE)
        ds = dots([[-2.5, y, 0] for y in (0.8, 0.3, -0.2)])
        self.play(FadeIn(ds), GrowArrow(flow), ds.animate.shift(DOWN * 0.6), run_time=0.6)
        self.at('Extra oxen slows elongation')
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.3)
        comp = comparison()
        # Begin straight: the different growth rates produce the bends on cue.
        comp[0].become(horizontal(-5.6, 0.25)); comp[1].become(horizontal(1.4, 0.25))
        comp[5].set_opacity(0)
        self.play(FadeIn(comp), run_time=0.5)
        upper = RoundedRectangle(width=3.2, height=0.32, corner_radius=0.07, color=GREEN, fill_opacity=0.25).move_to([-3.8, 1.3, 0])
        lower = upper.copy().stretch(0.7, 0, about_edge=LEFT).shift(DOWN * 0.55).set_color(ORANGE)
        root_tags = VGroup(label('upper', -6.05, 1.3, 22, GREEN), label('lower', -6.05, 0.75, 22, ORANGE))
        self.play(FadeIn(VGroup(upper, lower)), FadeIn(root_tags), run_time=0.4)
        self.at('The upper side grows faster')
        self.play(upper.animate.stretch(1.2, 0, about_edge=LEFT), run_time=0.6)
        self.at('so the root curves down')
        self.play(Transform(comp[0], horizontal(-5.6, 0.25, -0.65)), FadeOut(upper), FadeOut(lower), FadeOut(root_tags), run_time=0.75)
        self.at('In the shoot')
        self.play(comp[5].animate.set_opacity(1), run_time=0.4)
        upper2 = RoundedRectangle(width=2.3, height=0.32, corner_radius=0.07, color=GREEN, fill_opacity=0.25).move_to([3.1, 1.7, 0])
        lower2 = upper2.copy().shift(DOWN * 0.55).set_color(ORANGE)
        shoot_tags = VGroup(label('upper', 1.25, 1.7, 22, GREEN), label('lower', 1.25, 1.15, 22, ORANGE))
        self.at('speeds elongation on the lower side')
        self.play(FadeIn(upper2), FadeIn(lower2), FadeIn(shoot_tags), run_time=0.3)
        self.play(lower2.animate.stretch(1.5, 0, about_edge=LEFT), run_time=0.6)
        self.at('so the shoot curves up')
        self.play(Transform(comp[1], horizontal(1.4, 0.25, 0.65)), FadeOut(upper2), FadeOut(lower2), FadeOut(shoot_tags), run_time=0.7)
        self.finish()


class S09Hormones(SpokenScene):
    def construct(self):
        self.at('The same hormone')
        comp = comparison(); self.add(comp)
        self.at('Plant cells make hormones')
        self.play(FadeOut(comp), run_time=0.4)
        p = plant().move_to([0, -0.1, 0])
        buds = VGroup(Dot([-0.25, -0.5, 0], radius=0.17, color=GREEN), Dot([0.25, 0.5, 0], radius=0.17, color=GREEN))
        title = label('Growing shoot tip regulates side buds', 0, 3.1, 30, TEXT)
        tip_label = label('growing shoot tip', 2.1, 2.1, 24, GREEN)
        tip_leader = Line([0.2, 2.1, 0], [0.65, 2.1, 0], color=GREEN, stroke_width=2)
        self.play(FadeIn(p), FadeIn(buds), FadeIn(title), FadeIn(tip_label), Create(tip_leader), run_time=0.6)
        aux = chip('auxin', ORANGE, 26).move_to([-1.4, 1.7, 0])
        self.at('helps the growing shoot tip')
        self.play(FadeIn(aux), run_time=0.5)
        self.at('suppress side buds')
        regulation = VGroup(arr([0, 2.1, 0], [0.25, 0.5, 0], ORANGE), label('side buds suppressed', 2.3, -0.7, 24, GREY),
                            Line([0.45, -0.65, 0], [-0.05, -0.5, 0], color=GREY, stroke_width=2))
        self.play(FadeIn(regulation), buds.animate.set_opacity(0.3), run_time=0.6)
        self.at('together with')
        partners = VGroup(chip('cytokinins', TEAL, 26), chip('strigolactones', TEAL, 26)).arrange(DOWN, buff=0.4).move_to([-4.1, -0.6, 0])
        links = VGroup(arr(partners[0].get_right(), [0.1, 0.5, 0], TEAL),
                       arr(partners[1].get_right(), [-0.4, -0.5, 0], TEAL))
        self.play(FadeIn(partners), *[GrowArrow(link) for link in links], run_time=0.6)
        self.at('Other hormones control other transitions')
        side_bud_frame = list(self.mobjects)
        tomato = VGroup(Circle(radius=1, color=GREEN, fill_opacity=0.65).move_to([0, -0.2, 0]),
                        Line([-0.25, 0.8, 0], [0, 1.2, 0], color=GREEN, stroke_width=6))
        eth = chip('ethylene', TEAL, 30).move_to([-4, 0, 0])
        head = label('Tomato ripening', 0, 3, 34, TEXT)
        status = label('little ethylene', 0, 1.9, 28, TEAL)
        self.at('Ethylene promotes fruit ripening')
        self.play(*[FadeOut(m) for m in side_bud_frame], FadeIn(tomato), FadeIn(eth), FadeIn(head), FadeIn(status), run_time=0.7)
        self.at('Tomatoes engineered to make little ethylene')
        result = label('fails to ripen normally', 0, -2.1, 28, GREY)
        self.play(FadeIn(result), eth.animate.set_opacity(0.25), run_time=0.6)
        self.at('Supplied ethylene restored ripening')
        arrow = arr([-2.5, 0, 0], [-1.2, 0, 0], TEAL)
        self.play(Transform(eth, chip('ethylene', TEAL, 30).move_to([-4, 0, 0])), GrowArrow(arrow), Transform(status, label('supplied ethylene', 0, 1.9, 28, TEAL)),
                  Transform(result, label('ripening restored', 0, -2.1, 28, GREEN)), tomato[0].animate.set_color(RED), run_time=1.1)
        self.finish()


class S10Flowering(SpokenScene):
    def construct(self):
        context = label('Arabidopsis · long-day plant', 0, 3.15, 30, TEXT)
        p = plant().shift(RIGHT * 2.6)
        dial = Circle(radius=1.1, color=GREY).move_to([-4.3, 0.8, 0])
        day = Arc(radius=1.1, start_angle=-PI/2, angle=1.5*PI, color=YELLOW, stroke_width=12).move_arc_center_to([-4.3, 0.8, 0])
        hand = Line([-4.3, 0.8, 0], [-4.3, 1.65, 0], color=TEXT, stroke_width=4)
        clock = VGroup(dial, day, hand, label('daily clock + light', -4.3, -0.9, 24, YELLOW))
        self.at('Light also helps time flowering')
        self.add(context, p)
        self.at('a daily clock')
        self.play(FadeIn(clock), run_time=0.6)
        co = chip('CONSTANS', YELLOW, 26).move_to([-0.4, 1.6, 0])
        evening = label('evening light: stable protein', -2.9, 2.3, 24, YELLOW)
        self.at('evening light stabilizes the protein')
        self.play(Rotate(hand, -2.5, about_point=[-4.3, 0.8, 0]), FadeIn(co), FadeIn(evening), run_time=0.8)
        gene = chip('FT gene ON', BLUE, 26).move_to([-0.4, -0.15, 0])
        phloem = label('leaf phloem', -0.4, -1.05, 24, GREY)
        path = arr([-0.4, 1.15, 0], [-0.4, 0.35, 0], BLUE)
        self.at('promotes the gene')
        self.play(GrowArrow(path), FadeIn(gene), FadeIn(phloem), run_time=0.7)
        ft = chip('FT', BLUE, 24).move_to([1.7, -0.6, 0])
        route = VMobject(color=BLUE, stroke_width=5).set_points_as_corners([[1.7,-0.6,0],[2.6,-0.3,0],[2.6,2.1,0]])
        self.at('protein travels to the shoot apex')
        self.play(FadeIn(ft), Create(route), run_time=0.4)
        self.play(MoveAlongPath(ft, route), run_time=1.0)
        self.at('where flowers form')
        flower = VGroup(*[Ellipse(width=0.55, height=0.25, color=TEXT, fill_opacity=0.8).rotate(a).shift([np.cos(a)*0.28,np.sin(a)*0.28,0]) for a in np.arange(0,TAU,TAU/5)], Dot(ORIGIN, radius=0.1, color=YELLOW)).move_to([2.6,2.1,0])
        self.play(FadeOut(ft), FadeIn(flower), run_time=0.6)
        self.at('Leaves read the timing')
        takeaway = label('leaf timing → mobile FT → shoot apex', 0, -3.1, 28, BLUE)
        self.play(FadeIn(takeaway), run_time=0.6)
        self.finish()


class S11Seeds(SpokenScene):
    def construct(self):
        head = label('Opposing effects on seed growth', 0, 3.1, 32, TEXT)
        dormant, growing = seed(-3.4, -0.3), seed(3.4, -0.3)
        self.at('Hormones also have opposing effects')
        self.add(head, dormant, growing)
        aba = chip('abscisic acid', TEAL, 28).move_to([-3.4, 1.7, 0])
        ga = chip('gibberellins', TEAL, 28).move_to([3.4, 1.7, 0])
        hold = VGroup(arr([-0.5, -0.3, 0], [-2.5, -0.3, 0], TEAL), label('dormancy maintained', -3.4, -2.6, 26, TEAL))
        self.at('acid maintains seed dormancy')
        self.play(FadeIn(aba), FadeIn(hold), run_time=0.6)
        arrest = label('arrested growth', -3.4, -1.55, 24)
        self.at('a state of arrested growth')
        self.play(FadeIn(arrest), run_time=0.4)
        sprout = VGroup(stem([3.4,0,0], 1.1, 0.4, w=0.18), stem([3.4,-0.5,0], 1.0, 0.3, w=0.14).rotate(PI, about_point=[3.4,-0.5,0]))
        go = VGroup(arr([0.5,-0.3,0],[2.5,-0.3,0],TEAL), label('germination promoted',3.4,-2.6,26,TEAL))
        self.at('Gibberellins promote germination')
        self.play(FadeIn(ga), FadeIn(go), Create(sprout), run_time=0.9)
        self.at('Their effects point in opposite directions')
        self.play(Indicate(hold, color=TEAL), Indicate(go, color=TEAL), run_time=0.8)
        self.finish()


class S12Defence(SpokenScene):
    def construct(self):
        leaf = Ellipse(width=3.5, height=1.4, color=GREEN, fill_opacity=0.25).move_to([0,-0.5,0])
        insect = VGroup(Ellipse(width=0.7,height=0.4,color=GREY,fill_opacity=0.8),
                         *[Line([x,-0.1,0],[x-0.12,-0.35,0],color=GREY) for x in (-0.2,0,0.2)]).move_to([0,0.35,0])
        ja = chip('jasmonates', TEAL, 30).move_to([-3.8,1.8,0])
        defense = label('defence against plant-eating animals', 0,-2.3,28,TEAL)
        self.at('Hormones spread defense signals')
        self.add(leaf)
        self.at('signal defense against')
        self.play(FadeIn(insect), FadeIn(ja), FadeIn(defense), run_time=0.7)
        self.at('Salicylic acid helps systemic acquired resistance')
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.4)
        p = plant().scale(1.1)
        title = label('Systemic acquired resistance',0,3.1,32,TEXT)
        infected = Dot([-0.85,-0.65,0],radius=0.25,color=RED)
        infection = label('infection here',-3.8,-1.3,26,RED)
        self.play(FadeIn(p), FadeIn(title), run_time=0.5)
        self.at('Infection in one part')
        self.play(FadeIn(infected), FadeIn(infection), run_time=0.5)
        moving = Dot([-0.85,-0.65,0],radius=0.13,color=TEAL)
        route = VMobject(color=TEAL,stroke_width=4).set_points_as_corners([[-0.85,-0.65,0],[0,-0.3,0],[0,0.6,0],[0.85,0.6,0]])
        protected = label('distant leaf: more resistant',3.8,1.7,24,GREEN)
        self.at('other parts more resistant')
        self.play(Create(route), FadeIn(moving), run_time=0.4)
        self.play(MoveAlongPath(moving,route), FadeIn(protected), run_time=0.7)
        self.at('In tobacco')
        tobacco = label('TOBACCO',-4.6,2.4,28,TEXT)
        self.play(FadeIn(tobacco), run_time=0.4)
        sa = VGroup(chip('salicylic acid',TEAL,26), T('needed in protected leaves',24,TEAL)).arrange(DOWN,buff=0.2).move_to([3.8,-0.2,0])
        self.at('needed in the distant protected leaves')
        self.play(FadeIn(sa), run_time=0.6)
        self.at('but is not itself the traveling signal')
        mobile = label('mobile signal: identity unassigned',0,-2.9,26,TEAL)
        self.play(FadeIn(mobile), Indicate(moving,color=TEAL), run_time=0.7)
        self.at('is a tendency')
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.4)
        context = VGroup(T('A tendency, not a rule',38,TEXT,font=TITLE_FONT),
            chip('attacker',GREY,30), chip('plant',GREEN,30)).arrange(DOWN,buff=0.6)
        self.play(FadeIn(context), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "Plants steer growth by moving auxin, so one flank grows faster."
    def construct(self):
        line = T(self.LINE,32,TEXT,font=TITLE_FONT).move_to([0,2.7,0])
        recap = VGroup(*[chip(t,c,24) for t,c in [('Auxin → bending',ORANGE),('Hormones interact',TEAL),('Leaf → FT → apex',BLUE),('Dormancy ↔ germination',GREEN),('Defence: context',TEAL)]])
        recap[:3].arrange(RIGHT,buff=0.4).move_to([0,0.7,0])
        recap[3:].arrange(RIGHT,buff=0.6).move_to([0,-0.9,0])
        self.add(line)
        self.play(LaggedStart(*[FadeIn(m) for m in recap],lag_ratio=0.12),run_time=1.3)
        self.add(label('biochemistrypedia.com',0,-2.7,22,TEAL))
        self.finish()
