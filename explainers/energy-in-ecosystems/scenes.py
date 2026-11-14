"""Why Energy Pyramids Narrow — Chesapeake Bay teaching film.

COLOR MAP (one concept, one colour throughout)
  GOLD  energy moving through food
  GREEN producer tissue / phytoplankton
  TEAL  consumers / new consumer tissue
  BLUE  decomposers and material moving to them
  RED   dispersed heat
  GREY  habitat and supporting structure
"""
from types import SimpleNamespace

from bp_parts import *


# --------------------------------------------------------------------------- shared drawing helpers
def _safe(mob):
    """Habitat strokes deliberately sit behind labels and never carry meaning as text."""
    mob.layout_ok = True
    return mob


def _fish(center, scale=1.0, color=TEAL):
    body = Ellipse(width=2.05 * scale, height=0.82 * scale, color=color,
                   fill_color=color, fill_opacity=0.2, stroke_width=4)
    tail = Polygon(LEFT * 1.0 * scale, LEFT * 1.65 * scale + UP * 0.55 * scale,
                   LEFT * 1.65 * scale + DOWN * 0.55 * scale,
                   color=color, fill_color=color, fill_opacity=0.18, stroke_width=4)
    eye = Dot(RIGHT * 0.62 * scale + UP * 0.12 * scale, radius=0.065 * scale, color=TEXT)
    return VGroup(tail, body, eye).move_to(center)


def _osprey(center, scale=1.0):
    wings = VMobject(color=TEAL, stroke_width=6)
    wings.set_points_smoothly([LEFT * 1.25 * scale + DOWN * 0.18 * scale,
                               LEFT * 0.52 * scale + UP * 0.28 * scale,
                               ORIGIN,
                               RIGHT * 0.52 * scale + UP * 0.28 * scale,
                               RIGHT * 1.25 * scale + DOWN * 0.18 * scale])
    body = Ellipse(width=0.38 * scale, height=0.9 * scale, color=TEAL,
                   fill_color=TEAL, fill_opacity=0.25, stroke_width=4)
    head = Circle(radius=0.18 * scale, color=TEXT, fill_color=TEXT, fill_opacity=0.13,
                  stroke_width=3).shift(UP * 0.47 * scale)
    return VGroup(wings, body, head).move_to(center)


def _phytoplankton(center):
    pts = [(-0.55, 0.16), (-0.22, -0.2), (0.08, 0.2), (0.42, -0.13), (0.61, 0.22),
           (-0.48, -0.34), (0.22, -0.38)]
    return VGroup(*[Circle(radius=0.12, color=GREEN, fill_color=GREEN, fill_opacity=0.45,
                           stroke_width=3).move_to([center[0] + x, center[1] + y, 0]) for x, y in pts])


def _zooplankton(center, scale=1.0):
    body = Ellipse(width=1.15 * scale, height=0.72 * scale, color=TEAL,
                   fill_color=TEAL, fill_opacity=0.2, stroke_width=4)
    legs = VGroup(*[Line([x * scale, -0.22 * scale, 0],
                         [(x + 0.12) * scale, -0.58 * scale, 0], color=TEAL, stroke_width=3)
                    for x in (-0.35, -0.1, 0.15, 0.4)])
    return VGroup(body, legs).move_to(center)


def _arrow(a, b, color=GOLD, width=7, buff=0.2):
    return Arrow(a, b, buff=buff, color=color, stroke_width=width, tip_length=0.22,
                 max_tip_length_to_length_ratio=0.25, max_stroke_width_to_length_ratio=10)


def bay_world(with_bass=False, dim=1.0):
    """The carried Bay cross-section; every Bay scene rebuilds this exact geometry."""
    sky = _safe(Rectangle(width=14.2, height=2.45, stroke_width=0,
                          fill_color="#18212E", fill_opacity=0.72 * dim).move_to([0, 2.78, 0]))
    water = _safe(Rectangle(width=14.2, height=4.55, stroke_width=0,
                            fill_color="#153246", fill_opacity=0.55 * dim).move_to([0, -0.7, 0]))
    bottom = _safe(Polygon([-7.1, -2.65, 0], [7.1, -2.42, 0], [7.1, -4, 0], [-7.1, -4, 0],
                           stroke_width=0, fill_color="#29343B", fill_opacity=0.9 * dim))
    surface = _safe(Line([-7.1, 1.55, 0], [7.1, 1.55, 0], color=BLUE,
                         stroke_width=3, stroke_opacity=0.55 * dim))
    ripples = _safe(VGroup(*[Line([-6.5 + i * 2.25, 1.42 - 0.08 * (i % 2), 0],
                                      [-5.2 + i * 2.25, 1.42 - 0.08 * (i % 2), 0],
                                      color=BLUE, stroke_width=2, stroke_opacity=0.35 * dim)
                                  for i in range(6)]))
    sun = Circle(radius=0.5, color=GOLD, fill_color=GOLD, fill_opacity=0.32 * dim,
                 stroke_width=5).move_to([-5.4, 2.75, 0])
    rays = VGroup(*[Line(sun.get_center() + 0.62 * rotate_vector(RIGHT, a),
                         sun.get_center() + 0.92 * rotate_vector(RIGHT, a), color=GOLD,
                         stroke_width=3, stroke_opacity=0.8 * dim) for a in np.linspace(0, TAU, 8, endpoint=False)])
    phy = _phytoplankton([-4.15, -0.52, 0])
    zoo = _zooplankton([-1.45, -0.43, 0], 0.9)
    men = _fish([1.55, -0.24, 0], 0.92)
    osp = _osprey([4.35, 2.48, 0], 0.88)
    dead = VGroup(*[Polygon([-0.16, 0.08, 0], [0.12, 0.14, 0], [0.2, -0.1, 0],
                            [-0.1, -0.16, 0], color=BLUE, fill_color=BLUE, fill_opacity=0.25,
                            stroke_width=2).shift([-0.8 + 0.45 * i, -2.56 - 0.08 * (i % 2), 0]) for i in range(4)])
    decomp = VGroup(*[Dot([-1.18 + 0.28 * (i % 4), -3.02 + 0.2 * (i // 4), 0],
                                radius=0.075, color=BLUE) for i in range(8)])
    bass = _fish([4.2, -1.78, 0], 1.1, color=TEAL) if with_bass else VGroup()
    group = VGroup(sky, water, bottom, surface, ripples, sun, rays, phy, zoo, men, osp, dead, decomp, bass)
    if dim != 1.0:
        for m in (sun, rays, phy, zoo, men, osp, dead, decomp, bass):
            m.set_opacity(dim)
    return SimpleNamespace(group=group, sky=sky, water=water, bottom=bottom, surface=surface,
                           ripples=ripples, sun=sun, phy=phy, zoo=zoo, men=men, osp=osp,
                           dead=dead, decomp=decomp, bass=bass)


def animate_bay(world):
    bob(world.phy, amp=0.06, speed=1.1, seed=1)
    bob(world.zoo, amp=0.08, speed=1.35, seed=2)
    bob(world.men, amp=0.07, speed=1.0, seed=3)
    bob(world.osp, amp=0.05, speed=1.4, seed=4)
    if len(world.bass):
        bob(world.bass, amp=0.055, speed=0.9, seed=5)
    world.ripples.add_updater(lambda m, dt: m.shift(RIGHT * 0.045 * dt)
                              if m.get_right()[0] < 7.0 else m.shift(LEFT * 0.5))
    pulse(world.decomp, base=2.5, amp=1.2, speed=2.1)


def bay_links(world, web=False):
    links = {
        "sun_phy": _arrow(world.sun.get_bottom() + DOWN * 0.05, world.phy.get_top(), width=9),
        "phy_zoo": _arrow(world.phy.get_right(), world.zoo.get_left(), width=7),
        "zoo_men": _arrow(world.zoo.get_right(), world.men.get_left(), width=7),
        "men_osp": _arrow(world.men.get_top() + RIGHT * 0.35, world.osp.get_bottom() + LEFT * 0.35, width=6),
    }
    if web:
        links["phy_men"] = CurvedArrow(world.phy.get_top() + RIGHT * 0.35,
                                        world.men.get_bottom() + LEFT * 0.25, angle=0.42,
                                        color=GOLD, stroke_width=6, tip_length=0.2)
        links["men_bass"] = _arrow(world.men.get_bottom() + RIGHT * 0.35,
                                    world.bass.get_left() + UP * 0.1, width=6)
    return links


def _moving_dot(path, color=GOLD, radius=0.1):
    return Dot(path.get_start(), radius=radius, color=color)


def diagram_stage():
    """A consistent magnified-water field: fuller ink and a detectable slow current."""
    plate = RoundedRectangle(width=12.55, height=6.55, corner_radius=0.22, stroke_color="#3A6072",
                             stroke_width=2, fill_color="#20384A", fill_opacity=1.0).set_z_index(-12)
    currents = VGroup(*[Line([-5.7 + (i % 4) * 3.0, -2.7 + (i // 4) * 1.05, 0],
                                  [-4.35 + (i % 4) * 3.0, -2.7 + (i // 4) * 1.05, 0],
                                  color=BLUE, stroke_width=8, stroke_opacity=0.35)
                             for i in range(24)]).set_z_index(-11)
    currents._flow_t = 0.0

    def flow(mob, dt):
        mob._flow_t += dt
        mob.shift(RIGHT * 0.58 * dt)
        for line in mob:
            if line.get_left()[0] > 6.0:
                line.shift(LEFT * 11.8)

    currents.add_updater(flow)
    plate.layout_ok = True
    currents.layout_ok = True
    return VGroup(plate, currents)


def feeding_split(kind="menhaden", labels=False, question=False):
    """One fixed feeding-step geometry, reused by split, predict, pause, reveal and rule."""
    body = (_fish([0.1, 0.15, 0], 1.65) if kind == "menhaden"
            else _zooplankton([0.1, 0.1, 0], 2.0))
    incoming = _arrow([-6.0, 0.42, 0], [-1.55, 0.3, 0], width=18, buff=0)
    scraps = VGroup(*[Polygon([-0.13, 0.1, 0], [0.12, 0.12, 0], [0.16, -0.09, 0],
                              [-0.1, -0.13, 0], color=BLUE, fill_color=BLUE, fill_opacity=0.35,
                              stroke_width=2).move_to([-3.8 + 0.42 * i, -0.55 - 0.28 * i, 0]) for i in range(3)])
    waste = Dot([1.0, -0.35, 0], radius=0.16, color=BLUE)
    waste_path = CurvedArrow([0.9, -0.25, 0], [3.65, -2.2, 0], angle=0.25,
                             color=BLUE, stroke_width=6, tip_length=0.2)
    heat = VGroup(*[ArcBetweenPoints([0.15 + 0.48 * i, 0.55, 0],
                                     [0.75 + 0.58 * i, 2.28 + 0.12 * i, 0], angle=(-1) ** i * 0.28,
                                     color=RED, stroke_width=7) for i in range(3)])
    tissue = RoundedRectangle(width=2.0, height=0.62, corner_radius=0.2, color=GOLD,
                              fill_color=TEAL, fill_opacity=0.38, stroke_width=7).move_to([0.35, 0.13, 0])
    onward = _arrow([1.4, 0.2, 0], [5.45, 0.2, 0], width=8, buff=0)
    decomp = VGroup(*[Dot([3.45 + 0.28 * (i % 4), -2.55 + 0.22 * (i // 4), 0],
                                radius=0.085, color=BLUE) for i in range(8)])
    osprey = _osprey([5.35, 1.32, 0], 0.72)
    labs = {}
    if labels:
        labs = {
            "uneaten": T("uneaten", 28, BLUE).move_to([-3.55, -1.72, 0]),
            "heat": T("heat", 30, RED).move_to([2.7, 2.48, 0]),
            "undigested": T("undigested", 28, BLUE).move_to([4.75, -1.0, 0]),
            "tissue": T("new tissue", 30, TEAL, weight=BOLD).move_to([0.35, -1.42, 0]),
        }
    q = fit_text("Which branch can feed the osprey?", max_w=8.5, size=36, color=GOLD).move_to([0, 3.28, 0]) if question else VGroup()
    group = VGroup(body, incoming, scraps, heat, waste, waste_path, tissue, onward, decomp, osprey,
                   *labs.values(), q)
    return SimpleNamespace(group=group, body=body, incoming=incoming, scraps=scraps, heat=heat,
                           waste=waste, waste_path=waste_path, tissue=tissue, onward=onward,
                           decomp=decomp, osprey=osprey, labels=labs, question=q)


def animate_split(split):
    pulse(split.incoming, base=18, amp=2.5, speed=2.0)
    pulse(split.heat, base=7, amp=1.6, speed=2.3)
    pulse(split.tissue, base=7, amp=1.7, speed=2.6)
    pulse(split.decomp, base=2.5, amp=1.2, speed=2.0)
    bob(split.scraps, amp=0.06, speed=1.2, seed=2)


# --------------------------------------------------------------------------- scenes
class S00Hook(SpokenScene, TitleCard):
    LESSON = "Energy in Ecosystems"
    TITLE = "Why Energy Pyramids Narrow"

    def construct(self):
        w = bay_world()
        animate_bay(w)
        self.at("Why does far less")
        self.play(FadeIn(w.group), run_time=1.1)
        links = bay_links(w)
        qs = VGroup(*[T("?", 42, GOLD, weight=BOLD).move_to(p) for p in
                      ([-2.78, 0.45, 0], [0.0, 0.45, 0], [3.28, 1.18, 0])])
        self.play(FadeIn(qs, shift=UP * 0.12), run_time=1.0)
        self.at("Watch a gold band")
        self.play(GrowArrow(links["sun_phy"]), run_time=2.1)
        self.at("It enters green")
        dot = _moving_dot(links["sun_phy"])
        self.play(MoveAlongPath(dot, links["sun_phy"]), Indicate(w.phy, color=GREEN), run_time=2.3)
        self.at("Then teal zooplankton")
        self.play(FadeOut(qs), LaggedStart(*[GrowArrow(links[k]) for k in ("phy_zoo", "zoo_men", "men_osp")],
                                          lag_ratio=0.35), run_time=3.7)
        self.at("The band will change")
        pulses = [_moving_dot(links[k]) for k in ("phy_zoo", "zoo_men", "men_osp")]
        self.play(*[MoveAlongPath(d, links[k]) for d, k in zip(pulses, ("phy_zoo", "zoo_men", "men_osp"))],
                  run_time=1.5)
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        w = bay_world(dim=0.3)
        animate_bay(w)
        w.group.layout_ok = True  # deliberate dim moving backdrop behind the title
        title = fit_text("Why Energy Pyramids Narrow", max_w=11.2, size=52,
                         min_size=40, font=TITLE_FONT).move_to([0, 0.3, 0])
        rule = Line([-1.8, -0.25, 0], [1.8, -0.25, 0], color=GOLD, stroke_width=5)
        self.add(w.group)
        self.play(Write(title), GrowFromCenter(rule), run_time=0.8)
        corner = T("WHY ENERGY PYRAMIDS NARROW", 24, GOLD).move_to([0, 3.25, 0])
        self.play(ReplacementTransform(title, corner), FadeOut(rule), run_time=0.7)
        self.finish()


class S02Roles(SpokenScene):
    def construct(self):
        w = bay_world()
        animate_bay(w)
        corner = T("WHY ENERGY PYRAMIDS NARROW", 24, GOLD).move_to([0, 3.25, 0])
        self.add(w.group, corner)
        self.at("Phytoplankton are producers")
        producer = T("producer", 30, GREEN, weight=BOLD).next_to(w.phy, DOWN, buff=0.3)
        self.play(w.phy.animate.scale(1.35), FadeIn(producer, shift=UP * 0.1), run_time=1.4)
        self.at("Animals are consumers")
        brace_line = Line([-2.1, 0.75, 0], [5.05, 0.75, 0], color=TEAL, stroke_width=4)
        consumers = T("consumers", 30, TEAL, weight=BOLD).move_to([1.48, 1.12, 0])
        self.play(Create(brace_line), FadeIn(consumers), run_time=1.4)
        self.at("Blue decomposers")
        dl = T("decomposers", 28, BLUE).move_to([-0.1, -3.28, 0])
        self.play(FadeIn(dl), Indicate(w.decomp, color=BLUE, scale_factor=1.4), run_time=1.2)
        self.at("Gold arrows")
        links = bay_links(w)
        arrows = VGroup(links["phy_zoo"], links["zoo_men"], links["men_osp"])
        self.play(FadeOut(brace_line), FadeOut(consumers), LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.25),
                  run_time=2.3)
        self.at("Those arrows follow energy")
        dots = [_moving_dot(a, radius=0.09) for a in arrows]
        self.play(*[MoveAlongPath(d, a) for d, a in zip(dots, arrows)], run_time=2.0)
        self.finish()


class S03Split(SpokenScene):
    def construct(self):
        s = feeding_split("zooplankton")
        self.add(diagram_stage(), s.body, scope_tag("schematic"))
        self.at("When zooplankton feed")
        self.play(GrowArrow(s.incoming), run_time=2.0)
        self.at("Cellular respiration")
        self.play(LaggedStart(*[Create(h) for h in s.heat], lag_ratio=0.22), run_time=2.2)
        heat_l = T("heat", 30, RED).move_to([2.7, 2.48, 0])
        self.play(FadeIn(heat_l), run_time=0.7)
        self.at("Uneaten pieces")
        self.play(FadeIn(s.scraps), Create(s.waste_path), FadeIn(s.waste), FadeIn(s.decomp), run_time=2.2)
        waste_l = T("uneaten + undigested", 28, BLUE)
        waste_l.move_to([6.05 - waste_l.width / 2, -0.8, 0])  # inside the panel, clear of the waste arrow
        self.play(FadeIn(waste_l), run_time=0.7)
        self.at("Only the tissue branch")
        self.play(FadeIn(s.tissue), run_time=1.5)
        tissue_l = T("new tissue", 30, TEAL, weight=BOLD).move_to([0.35, -1.42, 0])
        self.play(FadeIn(tissue_l), run_time=0.7)
        animate_split(s)
        self.at("That branch is available")
        men = _fish([5.15, 1.05, 0], 0.72)
        self.play(GrowArrow(s.onward), FadeIn(men, shift=LEFT * 0.25), run_time=1.7)
        self.finish()


class S04Predict(SpokenScene):
    def construct(self):
        s = feeding_split("menhaden", question=False)
        self.add(diagram_stage())
        self.at("Now follow the same split")
        self.play(FadeIn(s.body), GrowArrow(s.incoming), run_time=2.1)
        self.at("Which outgoing branch")
        q = question_card("Which branch can feed the osprey?", y=3.25, max_w=9.5, size=36)
        self.play(FadeIn(q.question, shift=DOWN * 0.1), run_time=1.2)
        self.at("Watch all branches form")
        self.play(LaggedStart(FadeIn(s.scraps), FadeIn(s.heat),
                              AnimationGroup(FadeIn(s.waste), Create(s.waste_path)),
                              FadeIn(s.tissue), lag_ratio=0.25), run_time=2.3)
        animate_split(s)
        self.at("Choose before the labels")
        self.play(Indicate(VGroup(s.heat, s.waste_path, s.tissue), color=GOLD, scale_factor=1.025), run_time=1.0)
        self.finish()


class S05Pause(PredictPause):
    QUESTION = "Which branch can feed the osprey?"
    SECONDS = 4.5
    CARD = {"y": 3.25, "max_w": 9.5, "size": 36}
    RING_AT = (6.0, -3.15, 0)

    def backdrop(self):
        s = feeding_split("menhaden")
        animate_split(s)
        return VGroup(diagram_stage(), s.body, s.incoming, s.scraps, s.heat, s.waste, s.waste_path, s.tissue)


class S06Reveal(SpokenScene):
    def construct(self):
        s = feeding_split("menhaden")
        animate_split(s)
        self.add(diagram_stage(), s.body, s.incoming, s.scraps, s.heat, s.waste, s.waste_path, s.tissue)
        self.at("The branch stored as")
        tissue_l = T("new tissue", 30, TEAL, weight=BOLD).move_to([0.35, -1.42, 0])
        self.play(FadeIn(tissue_l), GrowArrow(s.onward), FadeIn(s.osprey, shift=LEFT * 0.2), run_time=2.2)
        self.at("Heat has dispersed")
        heat_l = T("heat", 30, RED).move_to([-1.55, 2.45, 0])
        self.play(FadeIn(heat_l), s.heat.animate.set_opacity(0.28).scale(1.18), run_time=1.7)
        self.at("Uneat or undigested")
        waste_l = T("to decomposers", 28, BLUE)
        waste_l.move_to([5.95 - waste_l.width / 2, -1.0, 0])
        self.play(FadeIn(s.decomp), FadeIn(waste_l), MoveAlongPath(s.waste.copy(), s.waste_path), run_time=2.0)
        self.at("It does not become")
        self.play(s.waste_path.animate.set_opacity(0.35), s.scraps.animate.set_opacity(0.35), run_time=1.3)
        self.at("The gold band reaching")
        outline = s.onward.copy().set_stroke(GOLD, width=13)
        pulse(outline, base=11, amp=2.5, speed=3.0)
        self.play(Create(outline), Indicate(s.osprey, color=GOLD), run_time=1.6)
        self.finish()


class S07Measure(SpokenScene):
    def construct(self):
        self.add(diagram_stage())
        panels = TwoPanel("energy at this level", "energy at next level", colors=(GOLD, GOLD))
        in_band = RoundedRectangle(width=4.4, height=0.72, corner_radius=0.16, color=GOLD,
                                   fill_color=GOLD, fill_opacity=0.28, stroke_width=5)
        out_band = RoundedRectangle(width=1.55, height=0.72, corner_radius=0.16, color=GOLD,
                                    fill_color=GOLD, fill_opacity=0.28, stroke_width=5)
        panels.put(in_band, "left")
        panels.put(out_band, "right")
        self.at("Ecologists compare levels")
        self.play(FadeIn(panels), FadeIn(in_band), FadeIn(out_band), run_time=2.1)
        self.at("It is the percentage")
        pct = ValueTracker(0.02)
        gauge = dial(pct, center=[0, 0.35, 0], radius=1.45, label="transfer efficiency",
                     color=GOLD, size=34)
        self.play(FadeOut(panels), FadeOut(in_band), FadeOut(out_band), FadeIn(gauge), run_time=1.2)
        self.play(pct.animate.set_value(0.1), run_time=1.5)
        self.at("The measurements must match")
        locks = VGroup(*[chip(t, TEAL, 26) for t in ("same measure", "same area", "same time")])
        locks.arrange(RIGHT, buff=0.4).move_to([0, -2.0, 0])
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.12) for c in locks], lag_ratio=0.28), run_time=2.0)
        self.at("A familiar percentage")
        ten = T("10% model", 38, GOLD, weight=BOLD).move_to([0, 2.75, 0])
        self.play(FadeIn(ten, scale=0.9), run_time=1.2)
        self.at("Real feeding steps")
        slider_line = Line([-2.1, -2.6, 0], [2.1, -2.6, 0], color=GREY, stroke_width=4)
        ticks = VGroup(*[Line([-2.1 + i * 1.4, -2.71, 0], [-2.1 + i * 1.4, -2.49, 0],
                                  color=GREY, stroke_width=3) for i in range(4)])
        nums = VGroup(*[T(str(v), 24, GREY).move_to([-2.1 + i * 1.4, -2.97, 0])
                        for i, v in enumerate((5, 10, 15, 20))])
        slider = VGroup(slider_line, ticks, nums)
        slider_label = T("model slider (%)", 26, GREY).next_to(slider, UP, buff=0.18)
        dot = Dot([-0.7, -2.6, 0], radius=0.11, color=GOLD)
        self.play(FadeOut(locks), FadeIn(slider), FadeIn(slider_label), FadeIn(dot), run_time=1.1)
        self.play(dot.animate.move_to([1.54, -2.6, 0]), run_time=0.8, rate_func=there_and_back)
        self.add(scope_tag("schematic"))
        self.finish()


class S08Pyramid(SpokenScene):
    def construct(self):
        self.add(diagram_stage())
        ratio = 0.10
        energies = [ratio ** i for i in range(4)]
        widths = [10.4 * e for e in energies]
        ys = [-2.05, -0.72, 0.61, 1.94]
        bars = VGroup(*[RoundedRectangle(width=max(w, 0.08), height=0.83, corner_radius=0.08,
                                         color=GOLD, fill_color=GOLD, fill_opacity=0.25,
                                         stroke_width=5).move_to([0, y, 0]) for w, y in zip(widths, ys)])
        names = ["producers", "primary consumers", "secondary consumers", "top consumers"]
        label_ys = [-2.82, ys[1], ys[2], ys[3]]
        labels = VGroup(*[T(n, 28, GREEN if i == 0 else TEAL) for i, n in enumerate(names)])
        for l, ly in zip(labels, label_ys):  # right edge kept inside the panel (edge at x = 6.27)
            l.move_to([5.95 - l.width / 2, ly, 0])
        heading = T("10% model", 34, GOLD, weight=BOLD).move_to([0, 3.32, 0])
        self.at("Stack those matching measurements")
        self.play(FadeIn(heading), LaggedStart(*[GrowFromCenter(b) for b in bars], lag_ratio=0.22), run_time=2.7)
        self.play(LaggedStart(*[FadeIn(l) for l in labels], lag_ratio=0.18), run_time=1.0)
        self.at("The result is an energy pyramid")
        self.play(Indicate(bars, color=GOLD, scale_factor=1.02), run_time=1.2)
        self.at("Each bar is narrower")
        tracer = Dot(bars[0].get_right(), radius=0.11, color=TEXT)
        self.play(MoveAlongPath(tracer, VMobject().set_points_as_corners([bars[i].get_right() for i in range(4)])),
                  run_time=2.4)
        self.at("The shape tracks energy flow")
        energy_label = T("energy flow", 30, GOLD).move_to([-4.9, 2.8, 0])
        self.play(FadeIn(energy_label), bars.animate.set_fill(opacity=0.42), run_time=1.5)
        self.at("Many small producers")
        producers = VGroup(*[Dot([-4.85 + 0.28 * (i % 5), -2.68 + 0.28 * (i // 5), 0],
                                     radius=0.075, color=GREEN) for i in range(10)])
        predator = _osprey([-4.2, 1.8, 0], 0.7)
        self.play(LaggedStart(*[FadeIn(p) for p in producers], lag_ratio=0.06), FadeIn(predator), run_time=1.8)
        self.finish()


class S09Web(SpokenScene):
    def construct(self):
        w = bay_world(with_bass=True)
        animate_bay(w)
        self.at("A real food web")
        self.play(FadeIn(w.group), run_time=1.5)
        links = bay_links(w, web=True)
        self.at("Menhaden eat phytoplankton")
        self.play(Create(links["phy_men"]), GrowArrow(links["phy_zoo"]),
                  GrowArrow(links["zoo_men"]), run_time=2.1)
        self.at("Striped bass")
        bass_l = T("striped bass", 28, TEAL).next_to(w.bass, DOWN, buff=0.18)
        self.play(GrowArrow(links["men_bass"]), FadeIn(bass_l), run_time=1.5)
        self.at("An osprey's trophic level")
        self.play(GrowArrow(links["men_osp"]), run_time=1.0)
        path1 = [links["phy_men"], links["men_osp"]]
        self.play(*[MoveAlongPath(_moving_dot(a), a) for a in path1], run_time=1.7)
        path2 = [links["phy_zoo"], links["zoo_men"], links["men_osp"]]
        self.play(Succession(*[MoveAlongPath(_moving_dot(a), a, run_time=0.7) for a in path2]), run_time=2.1)
        self.at("The same accounting")
        self.play(LaggedStart(*[Indicate(a, color=GOLD, scale_factor=1.02) for a in links.values()], lag_ratio=0.12),
                  run_time=1.5)
        self.at("Follow arrows from")
        dots = [_moving_dot(a, radius=0.08) for a in links.values()]
        self.play(*[MoveAlongPath(d, a) for d, a in zip(dots, links.values())], run_time=1.4)
        self.finish()


class S10Return(SpokenScene):
    def construct(self):
        w = bay_world()
        animate_bay(w)
        links = bay_links(w)
        self.add(w.group)
        self.at("Return to the osprey")
        self.play(Indicate(w.osp, color=GOLD, scale_factor=1.15), run_time=1.2)
        self.at("Its food energy began")
        self.play(LaggedStart(*[GrowArrow(links[k]) for k in ("sun_phy", "phy_zoo", "zoo_men", "men_osp")],
                              lag_ratio=0.22), run_time=2.4)
        pulse_dot = Dot(links["sun_phy"].get_start(), radius=0.13, color=GOLD)
        self.play(Succession(*[MoveAlongPath(pulse_dot, links[k], run_time=0.52)
                               for k in ("sun_phy", "phy_zoo", "zoo_men", "men_osp")]), run_time=2.1)
        self.at("Along the path")
        heat = VGroup(*[ArcBetweenPoints(p, p + UP * 0.8 + RIGHT * 0.25, angle=0.25,
                                         color=RED, stroke_width=5) for p in
                       (w.phy.get_center(), w.zoo.get_center(), w.men.get_center())])
        scraps = VGroup(*[_arrow(p + DOWN * 0.2, w.decomp.get_center(), color=BLUE, width=4, buff=0.25)
                          for p in (w.phy.get_center(), w.zoo.get_center(), w.men.get_center())])
        self.play(LaggedStart(*[Create(h) for h in heat], lag_ratio=0.2),
                  LaggedStart(*[GrowArrow(a) for a in scraps], lag_ratio=0.2), run_time=2.4)
        pulse(heat, base=5, amp=1.3, speed=2.4)
        self.at("The energy was transformed")
        self.play(heat.animate.set_opacity(0.45).scale(1.12), Indicate(w.decomp, color=BLUE), run_time=1.5)
        self.at("But at each feeding step")
        self.play(FadeOut(scraps), FadeOut(heat),
                  *[a.animate.set_stroke(width=max(3, 10 - 2 * i))
                    for i, a in enumerate([links["phy_zoo"], links["zoo_men"], links["men_osp"]])],
                  run_time=1.6)
        self.at("only the tissue branch")
        self.play(LaggedStart(*[Indicate(links[k], color=GOLD, scale_factor=1.03)
                                for k in ("phy_zoo", "zoo_men", "men_osp")], lag_ratio=0.25), run_time=1.7)
        self.finish()


class S11Rule(SpokenScene):
    def construct(self):
        s = feeding_split("menhaden", labels=True)
        animate_split(s)
        branches = VGroup(s.heat, s.scraps, s.waste, s.waste_path, s.tissue, s.onward)
        self.add(diagram_stage(), s.body, s.incoming, branches, s.decomp, *s.labels.values(), scope_tag("schematic"))
        self.at("That is why energy pyramids")
        self.play(Indicate(VGroup(s.incoming, s.tissue, s.onward), color=GOLD, scale_factor=1.02), run_time=1.8)
        self.at("Use the rule")
        self.play(FadeOut(s.labels["uneaten"]), FadeOut(s.labels["heat"]),
                  FadeOut(s.labels["undigested"]), run_time=1.0)
        self.at("At each step")
        self.play(FadeOut(s.body), FadeOut(s.incoming), FadeOut(s.heat), FadeOut(s.scraps),
                  FadeOut(s.waste), FadeOut(s.waste_path), FadeOut(s.decomp), FadeOut(s.onward), run_time=1.4)
        self.at("only part becomes tissue")
        centered = s.tissue.copy().scale(1.45).move_to([0, 0.3, 0])
        centered_l = T("only part becomes new tissue", 34, TEAL, weight=BOLD).next_to(centered, DOWN, buff=0.48)
        self.play(ReplacementTransform(s.tissue, centered),
                  ReplacementTransform(s.labels["tissue"], centered_l), run_time=1.5)
        pulse(centered, base=8, amp=2, speed=2.5)
        self.play(Indicate(centered, color=GOLD, scale_factor=1.08), run_time=1.2)
        self.finish()


class S12End(EndCard):
    LINE = "At each step, only part becomes tissue the next level can eat."
