"""Extinction and survival: who survives depends on variation that is already there  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  GREEN  = living / survives / sprouts / reproduces
  YELLOW = migrate (moves to a new place)
  RED    = die, the blight fungus, the new disease, the invasive species
  BLUE   = resistance (the bars in the sketches; heights are only a sketch, not data)
  ORANGE = pollution (harmful material added)
  TEAL   = climate change (the usual-weather range)
  GREY   = outlines, dead trunks, "extinct", places with no living members
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"


def dashed(mob, n=36):
    return DashedVMobject(mob, num_dashes=n)


def tree(x, y, s=1.0, c=GREEN):
    """schematic tree: trunk block + round canopy. y is the ground line."""
    trunk = Rectangle(width=0.26 * s, height=0.9 * s, stroke_width=0, fill_color=c, fill_opacity=0.55)
    trunk.move_to([x, y + 0.45 * s, 0])
    canopy = Circle(radius=0.62 * s, stroke_color=c, stroke_width=3, fill_color=c, fill_opacity=0.35)
    canopy.move_to([x, y + 0.9 * s + 0.5 * s, 0])
    g = VGroup(trunk, canopy)
    g.trunk, g.canopy = trunk, canopy
    return g


def kill(t):
    """animations: canopy gone, trunk grey."""
    return [t.canopy.animate.set_opacity(0), t.trunk.animate.set_fill(GREY, 0.7)]


def dot(x, y, r=0.22, c=TEXT):
    return Circle(radius=r, stroke_color=c, stroke_width=3, fill_color=c, fill_opacity=0.35).move_to([x, y, 0])


def bar(x, base, h, w=0.5):
    return Rectangle(width=w, height=h, stroke_color=BLUE, stroke_width=2.5, fill_color=BLUE,
                     fill_opacity=0.55).move_to([x, base + h / 2, 0])


def cross(x, y, s=0.2, c=RED):
    return VGroup(Line([x - s, y - s, 0], [x + s, y + s, 0], color=c, stroke_width=5),
                  Line([x - s, y + s, 0], [x + s, y - s, 0], color=c, stroke_width=5))


def sweep(x0, y0, y1, color=RED):
    return Rectangle(width=0.7, height=y1 - y0, stroke_width=0, fill_color=color,
                     fill_opacity=0.35).move_to([x0, (y0 + y1) / 2, 0])


class S00Title(TitleCard):
    LESSON = "Extinction and Survival"
    TITLE = "Who Survives Depends on Existing Variation"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    """a row of chestnuts; the fungus arrives; trunks grey; sprouts rise; the question."""

    def construct(self):
        head = T("American chestnut, Virginia's Blue Ridge", 32, font=TITLE_FONT).to_edge(UP, buff=0.45)
        xs = [-5.4 + 1.8 * i for i in range(7)]
        base = -0.9
        trees = [tree(x, base, 1.4) for x in xs]
        ground = Line([-6.3, base, 0], [6.3, base, 0], color=GREY, stroke_width=3)
        self.at("American chestnut trees were common")
        self.play(FadeIn(head), Create(ground), LaggedStart(*[GrowFromPoint(t, [t.get_center()[0], base, 0]) for t in trees],
                                                             lag_ratio=0.12), run_time=2.0)
        self.at("a fungus arrived")
        fungus = chip("fungus from Asia", RED, 28).move_to([-4.6, 2.5, 0])
        self.play(FadeIn(fungus, shift=RIGHT * 0.3), run_time=0.6)
        self.play(fungus.animate.move_to([4.6, 2.5, 0]), run_time=1.6)
        self.at("killed billions")
        killed = chip("about 1950: billions killed", RED, 28).move_to([0, 2.5, 0])
        self.play(FadeOut(fungus), FadeIn(killed), LaggedStart(*[AnimationGroup(*kill(t)) for t in trees], lag_ratio=0.1),
                  run_time=1.6)
        self.at("small sprouts still grow")
        sprouts = VGroup(*[VGroup(Line([x, base, 0], [x, base + 0.5, 0], color=GREEN, stroke_width=6),
                                  Circle(radius=0.13, stroke_width=0, fill_color=GREEN, fill_opacity=1).move_to([x, base + 0.62, 0]))
                           for x in xs])
        lbl = T("sprouts from old roots", 28, GREEN).move_to([0, -1.5, 0])
        self.play(LaggedStart(*[GrowFromPoint(s, [s.get_center()[0], base, 0]) for s in sprouts], lag_ratio=0.1),
                  FadeIn(lbl), run_time=1.4)
        self.at("Why do some species survive")
        q = VGroup(T("Why do some species survive big changes,", 34), T("while others disappear?", 34)).arrange(DOWN, buff=0.15)
        q.move_to([0, -2.6, 0])
        self.play(FadeIn(q, shift=UP * 0.15), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Fates(SpokenScene):
    """six members split into survive / migrate / die; then 'gone from one forest' vs 'extinct'."""

    def construct(self):
        box = RoundedRectangle(corner_radius=0.2, width=2.6, height=3.4, stroke_color=GREY, stroke_width=3).move_to([-4.6, 0, 0])
        pop_lbl = T("a population", 26, GREY).next_to(box, DOWN, buff=0.2)
        ys = [1.0, 0.0, -1.0]
        dots = [dot(-5.1 + 1.0 * c, y) for c in range(2) for y in ys]   # 6 dots, index = c*3 + r
        env = chip("environment changes", GREY, 26).move_to([-4.6, 2.55, 0])
        self.at("When an environment changes")
        self.play(Create(box), FadeIn(pop_lbl), LaggedStart(*[FadeIn(d, scale=0.6) for d in dots], lag_ratio=0.1),
                  FadeIn(env), run_time=1.4)
        self.at("do not share one fate")
        self.play(Indicate(VGroup(*dots), color=TEXT, scale_factor=1.05), run_time=0.8)

        lane_y = [1.9, 0.0, -1.9]
        c1 = chip("survive and reproduce", GREEN, 26).move_to([-0.4, lane_y[0] + 0.6, 0])
        c2 = chip("migrate", YELLOW, 26).move_to([-1.6, lane_y[1] + 0.6, 0])
        c3 = chip("die", RED, 26).move_to([-2.0, lane_y[2] + 0.6, 0])
        surv = [dots[0], dots[3]]
        mig = [dots[1], dots[4]]
        die = [dots[2], dots[5]]
        self.at("Some survive and reproduce")
        self.play(FadeIn(c1), *[d.animate.set_color(GREEN).set_fill(GREEN, 0.5) for d in surv], run_time=0.5)
        self.play(surv[0].animate.move_to([2.0, lane_y[0] - 0.3, 0]), surv[1].animate.move_to([2.8, lane_y[0] - 0.3, 0]),
                  run_time=0.9)
        kids = VGroup(dot(3.7, lane_y[0] - 0.3, 0.14, GREEN), dot(4.2, lane_y[0] - 0.3, 0.14, GREEN))
        self.play(FadeIn(kids, scale=0.5), run_time=0.5)
        self.at("Some migrate")
        newplace = dashed(Rectangle(width=2.6, height=1.3, stroke_color=YELLOW, stroke_width=3)).move_to([4.6, lane_y[1] - 0.3, 0])
        np_lbl = T("a new place", 24, YELLOW).next_to(newplace, DOWN, buff=0.12)
        self.play(FadeIn(c2), *[d.animate.set_color(YELLOW).set_fill(YELLOW, 0.5) for d in mig], Create(newplace), FadeIn(np_lbl),
                  run_time=0.7)
        self.at("move to a new place")
        self.play(mig[0].animate.move_to([4.0, lane_y[1] - 0.3, 0]), mig[1].animate.move_to([5.1, lane_y[1] - 0.3, 0]),
                  run_time=1.6)
        self.at("Some die")
        self.play(FadeIn(c3), *[d.animate.set_color(RED).set_fill(RED, 0.5).move_to([2.0 + 0.8 * i, lane_y[2] - 0.3, 0])
                                for i, d in enumerate(die)], run_time=0.6)
        xs_ = VGroup(*[cross(2.0 + 0.8 * i, lane_y[2] - 0.3, 0.2) for i in range(2)])
        self.play(Create(xs_), run_time=0.4)
        self.at("A species is extinct")
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)

        def grid(cx, filled):
            cells, items = VGroup(), VGroup()
            for i, (dx, dy) in enumerate([(-1.1, 0.8), (1.1, 0.8), (-1.1, -0.8), (1.1, -0.8)]):
                r = Rectangle(width=1.9, height=1.3, stroke_color=GREY, stroke_width=3).move_to([cx + dx, 0.55 + dy, 0])
                cells.add(r)
                if i in filled:
                    items.add(dot(cx + dx, 0.55 + dy, 0.28, GREEN))
            return cells, items

        cellsR, itemsR = grid(3.3, [])
        titleR = T("extinct", 34, GREY, weight=BOLD).move_to([3.3, 2.5, 0])
        capR = VGroup(T("no living members", 26), T("left anywhere", 26)).arrange(DOWN, buff=0.1).move_to([3.3, -1.75, 0])
        self.play(FadeIn(titleR), Create(cellsR), FadeIn(capR), run_time=1.0)
        self.at("Vanishing from one forest")
        cellsL, itemsL = grid(-3.3, [1, 2, 3])
        titleL = T("not extinct", 34, GREEN, weight=BOLD).move_to([-3.3, 2.5, 0])
        capL = VGroup(T("gone from one forest", 26), T("(top left box)", 26)).arrange(DOWN, buff=0.1).move_to([-3.3, -1.75, 0])
        self.play(FadeIn(titleL), Create(cellsL), FadeIn(itemsL), FadeIn(capL), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Four(SpokenScene):
    """four panels: habitat loss, pollution, climate change, invasive species."""

    def construct(self):
        pw, ph = 6.0, 3.15
        cx = [-3.15, 3.15]
        cy = [1.75, -1.75]

        def panel(ix, iy, title, color):
            r = RoundedRectangle(corner_radius=0.15, width=pw, height=ph, stroke_color=GREY, stroke_width=2.5).move_to([cx[ix], cy[iy], 0])
            t = T(title, 28, color, weight=BOLD).move_to([cx[ix], cy[iy] + ph / 2 - 0.4, 0])
            return r, t

        r1, t1 = panel(0, 0, "habitat loss", GREEN)
        hab_out = Rectangle(width=4.8, height=1.5, stroke_color=GREY, stroke_width=3).move_to([cx[0], cy[0] - 0.15, 0])
        hab = Rectangle(width=4.8, height=1.5, stroke_width=0, fill_color=GREEN, fill_opacity=0.4).move_to(hab_out)
        r2, t2 = panel(1, 0, "pollution", ORANGE)
        water = Rectangle(width=4.8, height=1.5, stroke_color=GREY, stroke_width=3).move_to([cx[1], cy[0] - 0.15, 0])
        wlabel = T("water", 24, GREY).move_to(water.get_bottom() + UP * 0.28)
        r3, t3 = panel(0, 1, "climate change", TEAL)
        axis = Line([cx[0] - 2.5, cy[1] - 0.7, 0], [cx[0] + 2.5, cy[1] - 0.7, 0], color=GREY, stroke_width=3)
        usual = Rectangle(width=1.8, height=0.6, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.4).move_to([cx[0] - 1.3, cy[1] - 0.2, 0])
        ulabel = T("usual weather", 24, TEAL).move_to([cx[0] - 1.3, cy[1] + 0.35, 0])
        r4, t4 = panel(1, 1, "invasive species", RED)
        region = Rectangle(width=4.8, height=1.3, stroke_color=GREY, stroke_width=3).move_to([cx[1], cy[1] - 0.05, 0])
        natives = VGroup(*[dot(cx[1] + dx, cy[1] - 0.05 + dy, 0.17, GREEN) for dx, dy in [(-1.5, 0.3), (-0.6, -0.3), (0.6, 0.3), (1.6, -0.25)]])

        self.at("Four changes")
        self.play(Create(r1), Create(r2), Create(r3), Create(r4), run_time=0.8)
        self.at("Habitat loss")
        self.play(FadeIn(t1), Create(hab_out), FadeIn(hab), run_time=0.7)
        self.at("destruction of the place")
        self.play(hab.animate.stretch_to_fit_width(1.6).align_to(hab_out, LEFT), run_time=1.6)
        self.at("Pollution")
        self.play(FadeIn(t2), Create(water), FadeIn(wlabel), run_time=0.7)
        self.at("harmful material added")
        drops = VGroup(*[Circle(radius=0.11, stroke_width=0, fill_color=ORANGE, fill_opacity=1).move_to([cx[1] - 1.8 + 0.9 * i, cy[0] + 0.85, 0]) for i in range(5)])
        self.play(FadeIn(drops), run_time=0.3)
        self.play(*[d.animate.shift(DOWN * (0.75 + 0.15 * (i % 3))) for i, d in enumerate(drops)], run_time=1.4)
        self.at("Climate change")
        self.play(FadeIn(t3), Create(axis), FadeIn(usual), FadeIn(ulabel), run_time=0.7)
        self.at("long shift")
        self.play(usual.animate.shift(RIGHT * 2.2), ulabel.animate.shift(RIGHT * 2.2), run_time=1.6)
        self.at("An invasive species")
        self.play(FadeIn(t4), Create(region), FadeIn(natives), run_time=0.7)
        self.at("brought to a new place")
        inv = dot(cx[1] - 2.8, cy[1] - 0.05, 0.17, RED)
        self.play(FadeIn(inv), run_time=0.3)
        self.play(inv.animate.move_to([cx[1] - 1.1, cy[1] + 0.05, 0]), run_time=1.0)
        self.at("spreads and causes harm")
        more = [dot(cx[1] - 1.1 + dx, cy[1] + dy, 0.17, RED) for dx, dy in [(0.8, -0.35), (1.6, 0.25), (2.4, -0.3)]]
        self.play(LaggedStart(*[FadeIn(m, scale=0.5) for m in more], lag_ratio=0.2),
                  *[n.animate.set_opacity(0.25) for n in natives], run_time=1.4)
        self.at("The chestnut blight fungus")
        tag = chip("chestnut blight fungus", RED, 24).move_to([cx[1], cy[1] - 1.15, 0])
        self.play(FadeIn(tag, shift=UP * 0.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Variation(SpokenScene):
    """eight members with different resistance bars; a disease; tall bars survive and pass the trait on."""

    def construct(self):
        base = -1.8
        xs = [-4.9 + 1.4 * i for i in range(8)]
        hs = [0.3, 1.7, 0.5, 0.9, 0.3, 2.0, 0.6, 0.4]
        members = [dot(x, 1.6, 0.3) for x in xs]
        bars = [bar(x, base, h) for x, h in zip(xs, hs)]
        floor = Line([-5.8, base, 0], [5.8, base, 0], color=GREY, stroke_width=3)
        top = T("genetic variation: inherited differences", 32).move_to([0, 3.0, 0])
        self.at("Genetic variation")
        self.play(FadeIn(top), LaggedStart(*[FadeIn(m, scale=0.6) for m in members], lag_ratio=0.08), Create(floor), run_time=1.2)
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.1), run_time=1.4)
        self.at("Resistance")
        rl = T("resistance: a taller bar holds off the disease better (a sketch)", 24, BLUE).move_to([0, -2.4, 0])
        self.play(FadeIn(rl), run_time=0.6)
        self.at("a new disease arrives")
        dis = chip("new disease", RED, 28).move_to([-5.2, 2.35, 0])
        band = sweep(-6.0, base - 0.1, 2.1)
        self.play(FadeIn(dis), FadeIn(band), run_time=0.5)
        self.play(dis.animate.move_to([5.2, 2.35, 0]), band.animate.move_to([6.0, (base + 2.1) / 2 - 0.05, 0]), run_time=1.6)
        self.play(FadeOut(band), run_time=0.2)
        self.at("more variation")
        res = [1, 5]
        self.play(*[Indicate(VGroup(members[i], bars[i]), color=GREEN, scale_factor=1.12) for i in res], run_time=1.0)
        self.at("Those members survive")
        gone = [i for i in range(8) if i not in res]
        self.play(*[FadeOut(VGroup(members[i], bars[i])) for i in gone],
                  *[members[i].animate.set_color(GREEN).set_fill(GREEN, 0.5) for i in res], FadeOut(dis), run_time=1.1)
        self.at("pass their traits")
        kids = VGroup()
        kh = {1: (1.55, 1.85), 5: (2.15, 1.85)}   # similar to the parent (1.7, 2.0), not identical
        for i in res:
            for dx, h in zip((-0.65, 0.65), kh[i]):
                kids.add(VGroup(dot(xs[i] + dx, 1.6, 0.17, GREEN), bar(xs[i] + dx, base, h, w=0.3)))
        kl = T("offspring", 26, GREEN).move_to([0, 0.35, 0])
        self.play(LaggedStart(*[FadeIn(k, scale=0.5) for k in kids], lag_ratio=0.15), FadeIn(kl), run_time=1.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Present(SpokenScene):
    """chestnuts with only short bars meet the fungus; then roots, sprouts, infection."""

    def construct(self):
        base = -1.6
        xs = [-4.9 + 1.4 * i for i in range(8)]
        trees = [tree(x, 0.2, 0.85) for x in xs]
        ground = Line([-6.3, 0.2, 0], [6.3, 0.2, 0], color=GREY, stroke_width=3)
        hs = [0.3, 0.45, 0.35, 0.4, 0.3, 0.45, 0.35, 0.95]
        bars = [bar(x, base, h) for x, h in zip(xs, hs)]
        floor = Line([-5.8, base, 0], [5.8, base, 0], color=GREY, stroke_width=3)
        head = T("American chestnut population", 32).move_to([0, 3.2, 0])
        self.at("Variation does not promise")
        self.play(FadeIn(head), Create(ground), LaggedStart(*[FadeIn(t, scale=0.7) for t in trees], lag_ratio=0.08), run_time=1.2)
        self.at("helpful trait usually has to be there")
        ht = T("helpful trait: usually has to be there already", 30, BLUE).move_to([0, 2.6, 0])
        self.play(FadeIn(ht, shift=UP * 0.1), run_time=0.8)
        self.at("very little resistance")
        rl = T("resistance (a sketch)", 26, BLUE).move_to([0, -2.15, 0])
        self.play(Create(floor), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.08), FadeIn(rl), run_time=1.3)
        self.at("this fungus")
        dis = chip("blight fungus", RED, 28).move_to([-5.2, -2.9, 0])
        band = sweep(-6.0, base - 0.1, 2.0)
        self.play(FadeIn(dis), FadeIn(band), run_time=0.4)
        self.play(dis.animate.move_to([5.2, -2.9, 0]), band.animate.move_to([6.0, (base + 2.0) / 2 - 0.05, 0]), run_time=1.1)
        self.at("almost all the big trees died")
        self.play(FadeOut(band), *[a for t in trees[:7] for a in kill(t)], run_time=1.0)
        self.at("The fungus can kill")
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)
        gy = -0.4
        gnd = Line([-6.0, gy, 0], [6.0, gy, 0], color=GREY, stroke_width=3)
        soil = T("soil", 26, GREY).move_to([-5.3, gy - 0.4, 0])
        t = tree(-1.5, gy, 1.6)
        roots = VGroup(*[Line([-1.5, gy, 0], [-1.5 + dx, gy - 1.4, 0], color=GREEN, stroke_width=6) for dx in (-1.2, -0.4, 0.4, 1.2)])
        gen = T("a typical tree", 26, GREY).move_to([-4.6, 1.8, 0])
        self.play(Create(gnd), FadeIn(soil), FadeIn(t), Create(roots), FadeIn(gen), run_time=0.9)
        fung = chip("fungus", RED, 26).move_to([-4.6, 1.2, 0])
        arrow_f = Arrow(fung.get_right(), [-1.8, 1.2, 0], buff=0.1, color=RED, stroke_width=5)
        self.play(FadeIn(fung), GrowArrow(arrow_f), run_time=0.4)
        self.play(*kill(t), run_time=0.8)
        self.at("The roots, safe in the soil")
        rl2 = T("roots, safe in the soil, often live", 26, GREEN).move_to([-1.5, gy - 1.95, 0])
        self.play(FadeIn(rl2), Indicate(roots, color=GREEN), run_time=0.8)
        self.at("send up new sprouts")
        spr = Line([0.8, gy - 0.5, 0], [0.8, gy + 1.5, 0], color=GREEN, stroke_width=8)
        leaf = Circle(radius=0.22, stroke_width=0, fill_color=GREEN, fill_opacity=1).move_to([0.8, gy + 1.65, 0])
        sp_lbl = T("new sprout", 26, GREEN).move_to([3.0, gy + 1.4, 0])
        self.play(Create(Line([-1.5, gy - 0.5, 0], [0.8, gy - 0.5, 0], color=GREEN, stroke_width=6)), run_time=0.4)
        self.play(GrowFromPoint(VGroup(spr, leaf), [0.8, gy - 0.5, 0]), FadeIn(sp_lbl), run_time=0.9)
        self.at("sprouts get infected")
        inf = Circle(radius=0.2, stroke_width=0, fill_color=RED, fill_opacity=0.9).move_to([0.8, gy + 0.75, 0])
        self.play(FadeIn(inf, scale=0.4), FadeOut(fung), FadeOut(arrow_f), run_time=0.6)
        self.at("die back")
        self.play(FadeOut(leaf), FadeOut(sp_lbl), FadeOut(inf), spr.animate.set_color(GREY), run_time=0.6)
        self.play(spr.animate.put_start_and_end_on([0.8, gy - 0.5, 0], [0.8, gy + 0.3, 0]), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Answer(SpokenScene):
    """a few survivors are not enough; the question answered in plain words."""

    def construct(self):
        sbox = RoundedRectangle(corner_radius=0.2, width=4.8, height=2.4, stroke_color=GREY, stroke_width=3).move_to([0, 0.4, 0])
        survivors = VGroup(*[dot(-1.3 + 1.3 * i, 0.4, 0.35, GREEN) for i in range(3)])
        sl = T("a few survivors", 34, GREEN).move_to([0, 2.1, 0])
        warn = T("not safe by themselves", 34, GREY).move_to([0, -1.3, 0])
        self.at("A few survivors")
        self.play(Create(sbox), FadeIn(survivors), FadeIn(sl), run_time=1.0)
        self.play(FadeIn(warn), run_time=0.6)
        self.at("So why do some species")
        self.play(FadeOut(sbox), FadeOut(survivors), FadeOut(sl), FadeOut(warn), run_time=0.5)
        q = VGroup(T("Why do some species survive big changes,", 32), T("while others disappear?", 32)).arrange(DOWN, buff=0.12).move_to([0, 2.8, 0])
        self.play(FadeIn(q), run_time=0.7)
        trait = chip("members already carry a helpful trait", BLUE, 24).move_to([-3.1, 1.0, 0])
        repro = chip("those members reproduce", GREEN, 24).move_to([-3.1, 0.0, 0])
        out1 = chip("more likely to survive", GREEN, 24).move_to([4.0, 0.5, 0])
        trait.align_to([-6.2, 0, 0], LEFT); repro.align_to([-6.2, 0, 0], LEFT)
        a1 = Arrow([0.4, 0.5, 0], [out1.get_left()[0] - 0.1, 0.5, 0], buff=0.05, color=GREEN, stroke_width=5)
        self.at("more likely to survive when")
        self.play(FadeIn(out1, shift=LEFT * 0.2), run_time=0.6)
        self.at("already carry a helpful trait")
        self.play(FadeIn(trait, shift=RIGHT * 0.2), run_time=0.6)
        self.at("those members reproduce")
        self.play(FadeIn(repro, shift=RIGHT * 0.2), run_time=0.6)
        self.play(GrowArrow(a1), run_time=0.5)
        self.at("If no member can survive")
        none = chip("no member can survive the change", RED, 24).move_to([-3.1, -1.9, 0])
        none.align_to([-6.2, 0, 0], LEFT)
        self.play(FadeIn(none, shift=RIGHT * 0.2), run_time=0.6)
        self.at("may become extinct")
        out2 = chip("species may become extinct", GREY, 24).move_to([4.0, -1.9, 0])
        a2 = Arrow([0.4, -1.9, 0], [out2.get_left()[0] - 0.1, -1.9, 0], buff=0.05, color=GREY, stroke_width=5)
        self.play(GrowArrow(a2), FadeIn(out2), run_time=0.7)
        self.finish()


class S07End(EndCard):
    LINE = "A helpful trait usually has to be there already."
