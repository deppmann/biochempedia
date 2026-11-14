"""What the Island's Counts Show — Predators and prey, chapter 2.

COLOR MAP (shared across the whole chapter)
  BROWN = moose / estimated moose counts
  GREY  = wolves / counted wolf counts
  GREEN = plant food
  GOLD  = questions, highlights, and the moose-per-wolf clue
  TEAL  = Lake Superior / survey action

The plotted points below are computed from the NPS winter-count values reproduced in
the lesson's chart. Missing 2021 and 2025 counts are shown only by dotted connectors.
"""
import numpy as np
from bp_parts import *  # noqa: F401,F403


BROWN = "#B06A32"
WOLF = GREY
MOOSE = BROWN
FOOD = GREEN
ORANGE = "#F28C45"


def layout_allowed(mob):
    """Mark a deliberate label-on-picture relationship for the layout checker."""
    for part in mob.get_family():
        part.layout_ok = True
    return mob


def breathe_fill(mob, base=0.20, amp=0.045, speed=1.15):
    """Slowly changing field light; large enough to keep a held data panel alive."""
    mob._fill_t = 0.0
    def update(m, dt):
        m._fill_t += dt
        m.set_fill(opacity=base + amp * np.sin(speed * m._fill_t))
    return mob.add_updater(update)


def graph_note(text, at, color=TEXT, size=28):
    note = T(text, size, color).move_to(at)
    note.add_background_rectangle(color=BG, opacity=0.88, buff=0.10)
    return layout_allowed(note)


# NPS winter counts, 1980–2026. Values are those encoded by the lesson's source chart.
YEARS_A = np.arange(1980, 2021)
MOOSE_A = np.array([665,650,700,900,810,1062.5,1025,1380,1652.5,1397.5,1215,1312.5,
                    1600,1880,1800,2400,1200,500,700,750,850,900,1000,900,750,540,
                    385,450,650,530,510,515,750,975,1050,1250,1300,1600,1500,2060,1875])
WOLVES_A = np.array([50,30,14,23,24,22,20,16,12,11,15,12,12,13,15,16,22,24,14,25,
                     29,19,17,19,29,30,30,21,23,24,19,16,9,8,9,3,2,2,2,15,14])
YEARS_B = np.array([2022, 2023, 2024])
MOOSE_B = np.array([1345, 967.5, 840])
WOLVES_B = np.array([28, 31, 30])
YEARS_C = np.array([2026])
MOOSE_C = np.array([524])
WOLVES_C = np.array([37])


def arrow(a, b, color=GREY, width=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=width, tip_length=tip,
                 max_tip_length_to_length_ratio=0.4)


def moose_icon(scale=1.0, color=MOOSE):
    """A labelled cartoon moose silhouette, matching chapter 1's simple flat shapes."""
    body = Ellipse(width=1.25, height=0.62, color=color, stroke_width=3,
                   fill_color=color, fill_opacity=0.28)
    head = Circle(radius=0.23, color=color, stroke_width=3,
                  fill_color=color, fill_opacity=0.28).move_to([0.72, 0.18, 0])
    legs = VGroup(*[Line([x, -0.22, 0], [x, -0.65, 0], color=color, stroke_width=4)
                    for x in (-0.42, 0.32)])
    antlers = VGroup(Line([0.75, 0.38, 0], [0.62, 0.68, 0], color=color, stroke_width=3),
                     Line([0.75, 0.38, 0], [0.92, 0.67, 0], color=color, stroke_width=3),
                     Line([0.62, 0.60, 0], [0.48, 0.73, 0], color=color, stroke_width=3),
                     Line([0.92, 0.60, 0], [1.04, 0.73, 0], color=color, stroke_width=3))
    return VGroup(body, head, legs, antlers).scale(scale)


def wolf_icon(scale=1.0, color=WOLF):
    body = Ellipse(width=1.18, height=0.55, color=color, stroke_width=3,
                   fill_color=color, fill_opacity=0.28)
    head = Polygon([0.52, 0.18, 0], [0.92, 0.42, 0], [0.83, 0.02, 0],
                   color=color, stroke_width=3, fill_color=color, fill_opacity=0.28)
    ear = Triangle(color=color, stroke_width=3, fill_color=color, fill_opacity=0.28).scale(0.14).move_to([0.75, 0.43, 0])
    legs = VGroup(*[Line([x, -0.2, 0], [x, -0.57, 0], color=color, stroke_width=4)
                    for x in (-0.38, 0.30)])
    tail = Line([-0.55, 0.12, 0], [-0.88, 0.48, 0], color=color, stroke_width=4)
    return VGroup(body, head, ear, legs, tail).scale(scale)


def plane_icon(scale=1.0):
    body = RoundedRectangle(width=2.0, height=0.34, corner_radius=0.16,
                            color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.12)
    wing = Polygon([-0.25, 0.05, 0], [0.55, 0.8, 0], [0.82, 0.78, 0],
                   [0.45, 0.02, 0], color=TEAL, fill_color=TEAL, fill_opacity=0.35)
    tail = Polygon([-0.82, 0.08, 0], [-0.66, 0.55, 0], [-0.42, 0.53, 0],
                   [-0.48, 0.02, 0], color=TEAL, fill_color=TEAL, fill_opacity=0.35)
    nose = Dot([1.03, 0, 0], radius=0.08, color=GOLD)
    return VGroup(body, wing, tail, nose).scale(scale)


def island_world(show_plane=False):
    """The carried island picture used by every survey scene at one scale and position."""
    lake = RoundedRectangle(width=12.0, height=5.2, corner_radius=0.2, stroke_color=TEAL,
                            stroke_width=2, fill_color=TEAL, fill_opacity=0.22).move_to([0, -0.25, 0])
    island = Ellipse(width=8.5, height=3.25, color=TEXT, stroke_width=3,
                     fill_color=TEXT, fill_opacity=0.22).rotate(-0.12).move_to([-0.8, -0.35, 0])
    layout_allowed(lake), layout_allowed(island)
    snow = VGroup(*[Line([-4.4 + i * 0.75, -0.9 + 0.13 * (i % 3), 0],
                              [-4.0 + i * 0.75, -0.9 + 0.13 * (i % 3), 0],
                              color=TEXT, stroke_width=2).set_opacity(0.35) for i in range(10)])
    label = T("Isle Royale", 32, TEXT, font=TITLE_FONT).move_to([-0.8, 1.55, 0])
    water = T("Lake Superior", 26, TEAL).move_to([-4.7, -2.65, 0])
    g = VGroup(lake, island, snow, label, water)
    if show_plane:
        g.add(plane_icon(0.78).move_to([-4.7, 2.45, 0]))
    return g


def ratio_box(value="—", color=TEXT):
    lab = T("moose per wolf", 24, GREY)
    val = M(str(value), 38, color)
    box = RoundedRectangle(width=3.25, height=1.02, corner_radius=0.14,
                           stroke_color=color, stroke_width=2.5, fill_color=BG, fill_opacity=0.96)
    VGroup(lab, val).arrange(DOWN, buff=0.04).move_to(box)
    return VGroup(box, lab, val).move_to([4.9, 3.15, 0])


def ratio_readout(tracker, color_fn=lambda: TEXT):
    box = RoundedRectangle(width=3.25, height=1.02, corner_radius=0.14,
                           stroke_color=GREY, stroke_width=2.5, fill_color=BG, fill_opacity=0.96).move_to([4.9, 3.15, 0])
    lab = T("moose per wolf", 24, GREY).move_to([4.9, 3.39, 0])
    val = always_redraw(lambda: M(f"{tracker.get_value():.0f}", 38, color_fn()).move_to([4.9, 2.98, 0]))
    return VGroup(box, lab, val)


class CountGraph(VGroup):
    """Two large panels sharing a year axis, computed directly from the lesson data."""
    def __init__(self, x0=-5.75, x1=5.75, top=(0.25, 2.55), bottom=(-2.45, -0.55), labels=True):
        super().__init__()
        self.x0, self.x1 = x0, x1
        self.mt0, self.mt1 = top
        self.wt0, self.wt1 = bottom
        axes = VGroup(
            Line([x0, self.mt0, 0], [x1, self.mt0, 0], color=GREY, stroke_width=2),
            Line([x0, self.mt0, 0], [x0, self.mt1, 0], color=GREY, stroke_width=2),
            Line([x0, self.wt0, 0], [x1, self.wt0, 0], color=GREY, stroke_width=2),
            Line([x0, self.wt0, 0], [x0, self.wt1, 0], color=GREY, stroke_width=2))
        grid = VGroup(*[Line([x0, y, 0], [x1, y, 0], color=GREY, stroke_width=1).set_opacity(0.25)
                        for y in ((self.mt0+self.mt1)/2, self.mt1, (self.wt0+self.wt1)/2, self.wt1)])
        ticks = VGroup()
        for year in (1980, 1990, 2000, 2010, 2020):
            x = self.x(year)
            ticks.add(Line([x, self.wt0, 0], [x, self.wt0-0.09, 0], color=GREY, stroke_width=2),
                      T(str(year), 22, GREY).next_to([x, self.wt0, 0], DOWN, buff=0.12))
        ylabels = VGroup(T("2,500", 22, GREY).next_to([x0, self.mt1, 0], LEFT, buff=0.12),
                         T("0", 22, GREY).next_to([x0, self.mt0, 0], LEFT, buff=0.12),
                         T("50", 22, GREY).next_to([x0, self.wt1, 0], LEFT, buff=0.12),
                         T("0", 22, GREY).next_to([x0, self.wt0, 0], LEFT, buff=0.12))
        self.axes_group = VGroup(axes, grid, ticks, ylabels)
        panels = VGroup(Rectangle(width=x1-x0, height=self.mt1-self.mt0, stroke_width=0,
                                  fill_color=MOOSE, fill_opacity=0.20).move_to([(x0+x1)/2,(self.mt0+self.mt1)/2,0]),
                        Rectangle(width=x1-x0, height=self.wt1-self.wt0, stroke_width=0,
                                  fill_color=WOLF, fill_opacity=0.20).move_to([(x0+x1)/2,(self.wt0+self.wt1)/2,0]))
        layout_allowed(panels)
        for panel in panels:
            breathe_fill(panel)
        self.add(panels, self.axes_group)
        if labels:
            self.headers = VGroup(T("moose (estimated)", 28, MOOSE, weight=BOLD).move_to([-3.9, 2.82, 0]),
                                  T("wolves (counted)", 28, WOLF, weight=BOLD).move_to([-3.9, -0.27, 0]))
            self.add(self.headers)

    def x(self, year):
        return self.x0 + (year - 1980) / 46 * (self.x1 - self.x0)

    def mp(self, year, value):
        return np.array([self.x(year), self.mt0 + value / 2500 * (self.mt1-self.mt0), 0])

    def wp(self, year, value):
        return np.array([self.x(year), self.wt0 + value / 50 * (self.wt1-self.wt0), 0])

    def line(self, years, values, kind, color, dashed=False, width=5):
        pts = [self.mp(y, v) if kind == "m" else self.wp(y, v) for y, v in zip(years, values)]
        if len(pts) == 1:
            return Dot(pts[0], radius=0.08, color=color)
        if dashed:
            m = DashedVMobject(VMobject().set_points_as_corners(pts).set_stroke(color, width), num_dashes=max(3, len(pts)*2))
        else:
            m = VMobject().set_points_as_corners(pts).set_stroke(color, width)
        return pulse(m, base=width, amp=1.25, speed=1.35)

    def data(self, through=2026):
        g = VGroup()
        mask = YEARS_A <= through
        if mask.any():
            g.add(self.line(YEARS_A[mask], MOOSE_A[mask], "m", MOOSE),
                  self.line(YEARS_A[mask], WOLVES_A[mask], "w", WOLF))
        if through >= 2022:
            mb = YEARS_B <= through
            g.add(self.line(np.array([2020, 2022]), np.array([MOOSE_A[-1], MOOSE_B[0]]), "m", MOOSE, True, 3),
                  self.line(np.array([2020, 2022]), np.array([WOLVES_A[-1], WOLVES_B[0]]), "w", WOLF, True, 3),
                  self.line(YEARS_B[mb], MOOSE_B[mb], "m", MOOSE),
                  self.line(YEARS_B[mb], WOLVES_B[mb], "w", WOLF))
        if through >= 2026:
            g.add(self.line(np.array([2024, 2026]), np.array([MOOSE_B[-1], MOOSE_C[0]]), "m", MOOSE, True, 3),
                  self.line(np.array([2024, 2026]), np.array([WOLVES_B[-1], WOLVES_C[0]]), "w", WOLF, True, 3),
                  Dot(self.mp(2026, MOOSE_C[0]), radius=0.08, color=MOOSE),
                  Dot(self.wp(2026, WOLVES_C[0]), radius=0.08, color=WOLF))
        return g

    def year_line(self, year, color=GOLD):
        return Line([self.x(year), self.wt0, 0], [self.x(year), self.mt1, 0], color=color, stroke_width=5).set_opacity(0.55)


def graph_world(through=2026, source=True):
    graph = CountGraph()
    data = graph.data(through)
    extra = VGroup()
    if source:
        src = T("NPS winter counts", 24, TEAL).move_to([-4.75, 3.38, 0])
        extra.add(src)
    return graph, data, extra


def family_world():
    """The carried 2016 family picture used unchanged in scenes 13 and 14."""
    wolves = VGroup(wolf_icon(1.55), wolf_icon(1.55)).arrange(RIGHT, buff=0.75).move_to([-3.4, -0.35, 0])
    tree = VGroup(
        Dot([2.2, 2.0, 0], radius=0.16, color=WOLF), Dot([4.0, 2.0, 0], radius=0.16, color=WOLF),
        Dot([3.1, 0.8, 0], radius=0.16, color=WOLF), Dot([2.3, -0.5, 0], radius=0.16, color=WOLF),
        Dot([3.9, -0.5, 0], radius=0.16, color=WOLF),
        Line([2.2,1.84,0],[3.1,0.96,0],color=WOLF), Line([4.0,1.84,0],[3.1,0.96,0],color=WOLF),
        Line([3.1,0.64,0],[2.3,-0.34,0],color=WOLF), Line([3.1,0.64,0],[3.9,-0.34,0],color=WOLF),
        ArcBetweenPoints([2.3,-0.65,0],[3.9,-0.65,0],angle=-PI,color=GOLD,stroke_width=4))
    return wolves, tree


def family_panel():
    panel = RoundedRectangle(width=12.2, height=5.7, corner_radius=0.22, stroke_color=WOLF,
                             stroke_width=2, fill_color=WOLF, fill_opacity=0.18).move_to([0,-0.15,0])
    return layout_allowed(breathe_fill(panel, base=0.18, amp=0.035, speed=0.9))


class S00Title(TitleCard):
    LESSON = "Predators and prey"
    TITLE = "What the Island's Counts Show"


class S01Question(SpokenScene):
    def construct(self):
        q = fit_text("Does the real island follow the rule?", max_w=8.2, size=44,
                     color=TEXT, font=TITLE_FONT).move_to([-1.55, 2.95, 0])
        self.play(Write(q), run_time=1.3)
        self.at("The first film used")
        island = island_world()
        prey = moose_icon(0.75).move_to([-2.4, -0.45, 0])
        wolves = VGroup(*[wolf_icon(0.42).move_to([x, y, 0]) for x,y in ((-0.2,0.25),(0.8,-0.4),(1.7,0.2))])
        loop = CurvedArrow([2.1,-0.7,0],[-2.0,-1.0,0],angle=-1.4,color=GOLD,stroke_width=5)
        tag = scope_tag("model (schematic)")
        counter_box = ratio_box("21", ORANGE)
        self.play(FadeIn(island), FadeIn(prey), FadeIn(wolves), Create(loop), FadeIn(tag), FadeIn(counter_box), run_time=1.6)
        self.at("wolves usually ran short")
        self.play(wolves.animate.set_opacity(0.35).shift(DOWN*0.18), counter_box[0].animate.set_stroke(ORANGE, width=5), run_time=1.4)
        self.at("Now we check")
        real = island_world(show_plane=True)
        real[-1].move_to([4.65, 1.85, 0])
        real_label = T("real winter counts", 34, TEAL, weight=BOLD).move_to([0, -3.1, 0])
        self.play(FadeOut(VGroup(island, prey, wolves, loop, tag, counter_box)), Transform(q, T("Now: the real island", 44, TEXT, font=TITLE_FONT).move_to(q)),
                  FadeIn(real), FadeIn(real_label), run_time=1.6)
        self.finish()


class S02Counting(SpokenScene):
    def construct(self):
        world = island_world(show_plane=True)
        ratio = ratio_box()
        self.play(FadeIn(world), FadeIn(ratio), run_time=1.0)
        self.at("where wolves hunt moose")
        wolf = wolf_icon(0.9).move_to([-1.4, -0.2, 0])
        moose = moose_icon(1.0).move_to([1.4, -0.1, 0])
        self.play(FadeIn(moose), FadeIn(wolf), run_time=1.1)
        self.at("Scientists survey")
        plane = world[-1]
        self.play(plane.animate.move_to([4.4, 2.35, 0]), run_time=1.7, rate_func=linear)
        self.at("Wolves are counted")
        tracks = VGroup(*[VGroup(Dot(radius=0.06,color=WOLF),Dot(radius=0.06,color=WOLF).shift(RIGHT*0.15)).move_to([-3+i*0.5,-1.4+0.12*(i%2),0]) for i in range(7)])
        tally = VGroup(T("wolves", 28, WOLF), M("|||| |||", 38, TEXT)).arrange(DOWN,buff=0.12)
        tally_box = SurroundingRectangle(tally, color=WOLF, buff=0.28, corner_radius=0.12)
        tally_group = VGroup(BackgroundRectangle(tally_box,color="#0b0d14",fill_opacity=0.95,buff=0.05),tally_box,tally).move_to([3.9,-1.45,0])
        self.play(FadeIn(tracks, lag_ratio=0.08), FadeIn(tally_group), plane.animate.move_to([-4.4,2.35,0]), run_time=1.7)
        self.at("close to every wolf")
        ring = SurroundingRectangle(wolf, color=GOLD, buff=0.22, corner_radius=0.15)
        note = T("counted from the air", 28, TEXT).next_to(tally_group, UP, buff=0.22)
        note = VGroup(BackgroundRectangle(note,color="#0b0d14",fill_opacity=0.95,buff=0.08),note)
        self.play(Create(ring), FadeIn(note), run_time=1.0)
        self.finish()


class S03Estimate(SpokenScene):
    def construct(self):
        world = island_world()
        ratio = ratio_box()
        herd = VGroup(*[moose_icon(0.28).move_to([-3.2+(i%6)*1.0,-1.25+(i//6)*0.75,0]) for i in range(18)])
        self.play(FadeIn(world), FadeIn(ratio), FadeIn(herd, lag_ratio=0.03), run_time=1.3)
        self.at("Scientists count them")
        grid = VGroup(*[Rectangle(width=1.25,height=0.72,color=TEAL,stroke_width=2).move_to([-3.4+c*1.25,-1.55+r*0.72,0]) for r in range(4) for c in range(6)])
        self.play(Create(grid), run_time=1.2)
        self.at("small squares of land")
        samples = VGroup(grid[2],grid[9],grid[16]).copy().set_fill(GOLD,opacity=0.25).set_stroke(GOLD,width=5)
        self.play(FadeIn(samples), Indicate(VGroup(herd[2],herd[9],herd[16]),color=MOOSE), run_time=1.2)
        self.at("estimate the whole island")
        result = chip("moose: estimated for the whole island", MOOSE, size=30).move_to([1.6,2.25,0])
        layout_allowed(result)
        arrw = arrow(samples.get_right(),result.get_bottom(),MOOSE)
        self.play(GrowArrow(arrw), FadeIn(result), run_time=1.4)
        self.at("moose numbers are estimates")
        self.play(Indicate(result,color=MOOSE,scale_factor=1.04), run_time=1.0)
        self.finish()


class S04Graph(SpokenScene):
    def construct(self):
        g,data,extra = graph_world()
        ratio = ratio_box()
        self.play(FadeIn(g[0]), Create(g.axes_group), FadeIn(g.headers), FadeIn(extra), FadeIn(ratio), run_time=1.2)
        self.at("The brown line")
        self.play(Create(VGroup(data[0],data[2],data[4],data[6],data[8])), run_time=1.8, rate_func=linear)
        self.at("The gray line")
        self.play(Create(VGroup(data[1],data[3],data[5],data[7],data[9])), run_time=1.8, rate_func=linear)
        self.at("Some winters have no count")
        gaps = T("2021 & 2025: no count",24,GOLD).move_to([3.75,-3.15,0])
        self.play(FadeIn(gaps), Indicate(VGroup(data[2],data[3],data[6],data[7]),color=GOLD), run_time=1.2)
        self.finish()


class S051995(SpokenScene):
    def construct(self):
        g,data,extra = graph_world()
        bar = g.year_line(1995)
        ratio = ratio_box("150", TEXT)
        self.add(g,data,extra,ratio)
        self.play(Create(bar), run_time=1.1)
        self.at("moose line is near")
        mdot = Dot(g.mp(1995,2400),radius=0.13,color=MOOSE)
        mlab = graph_note("1995: about 2,400 moose",[2.2,2.2,0],MOOSE)
        self.play(FadeIn(mdot), FadeIn(mlab), run_time=1.1)
        self.at("only 16 wolves")
        wdot = Dot(g.wp(1995,16),radius=0.13,color=TEXT)
        wlab = graph_note("16 wolves",[2.8,-1.2,0],WOLF)
        self.play(FadeIn(wdot), FadeIn(wlab), run_time=1.0)
        self.at("counter is high")
        self.play(Indicate(ratio,color=GOLD,scale_factor=1.03), run_time=1.0)
        self.at("plenty of moose")
        self.play(Flash(mdot,color=GOLD,line_length=0.25,num_lines=12), run_time=1.1)
        self.finish()


class S061997(SpokenScene):
    def construct(self):
        g,data,extra = graph_world()
        bar = g.year_line(1995)
        n = ValueTracker(150)
        color = lambda: ORANGE if n.get_value() < 60 else TEXT
        ratio = ratio_readout(n,color)
        self.add(g,data,extra,bar,ratio)
        self.play(bar.animate.shift(RIGHT*(g.x(1997)-g.x(1995))), run_time=1.2)
        self.at("moose had dropped")
        mdot = Dot(g.mp(1997,500),radius=0.13,color=MOOSE)
        mlab = graph_note("1997: about 500 moose",[2.45,0.75,0],MOOSE)
        self.play(FadeIn(mdot), FadeIn(mlab), run_time=1.1)
        self.at("wolves had risen")
        wdot = Dot(g.wp(1997,24),radius=0.13,color=TEXT)
        wlab = graph_note("24 wolves",[2.7,-1.15,0],WOLF)
        self.play(FadeIn(wdot), FadeIn(wlab), run_time=1.0)
        self.at("counter fell")
        self.play(n.animate.set_value(21), ratio[0].animate.set_stroke(ORANGE,width=4), run_time=1.6)
        self.at("few moose to hunt")
        self.play(Indicate(VGroup(mdot,wdot),color=ORANGE,scale_factor=1.05), run_time=1.0)
        self.finish()


class S07Cause(SpokenScene):
    def construct(self):
        g,data,extra = graph_world()
        ratio = ratio_box("21",ORANGE)
        self.add(g,data,extra,ratio,g.year_line(1997,ORANGE))
        card = chip("Why did moose fall?",GOLD,size=32).move_to([2.3,1.65,0])
        card = VGroup(BackgroundRectangle(card,color="#0b0d14",fill_opacity=0.96,buff=0.04),card)
        layout_allowed(card)
        self.play(FadeIn(card), run_time=0.9)
        self.at("counts alone do not say")
        answer = T("counts alone do not say",28,TEXT).move_to([2.3,0.85,0])
        answer = VGroup(BackgroundRectangle(answer,color="#0b0d14",fill_opacity=0.96,buff=0.08),answer)
        layout_allowed(answer)
        self.play(FadeIn(answer), run_time=1.0)
        self.at("Weather and food")
        weather = chip("weather ?",TEAL,size=28).move_to([1.35,-0.05,0])
        food = chip("food ?",FOOD,size=28).move_to([4.25,-0.05,0])
        weather = VGroup(BackgroundRectangle(weather,color="#0b0d14",fill_opacity=0.96,buff=0.04),weather); food = VGroup(BackgroundRectangle(food,color="#0b0d14",fill_opacity=0.96,buff=0.04),food)
        layout_allowed(weather), layout_allowed(food)
        self.play(FadeIn(weather), FadeIn(food), run_time=1.1)
        self.at("follow is the counter")
        self.play(Indicate(ratio,color=ORANGE,scale_factor=1.05), FadeOut(VGroup(card,answer,weather,food)), run_time=1.2)
        self.finish()


PREDICT_Q = "Only 21 moose for each wolf. What happens to the 24 wolves by next winter?"


def predict_backdrop():
    g,data,extra = graph_world(through=1997)
    return VGroup(g,data,extra,g.year_line(1997,ORANGE),ratio_box("21",ORANGE))


class S08Predict(SpokenScene):
    def construct(self):
        back = predict_backdrop()
        self.add(back)
        self.at("Only about 21")
        self.play(Indicate(back[-1],color=ORANGE,scale_factor=1.05),run_time=1.2)
        self.at("What happens to")
        q = question_card(PREDICT_Q,y=-3.2,size=28,max_w=10.7,left=-6.1)
        self.play(FadeIn(q),run_time=1.3)
        self.at("Pause and predict")
        self.play(back[-1][0].animate.set_stroke(ORANGE,width=5),run_time=1.0)
        self.finish()


class S09Pause(PredictPause):
    QUESTION = PREDICT_Q
    OPTIONS = ()
    CARD = {"y": -3.2, "size": 28, "max_w": 10.7, "left": -6.1}
    SECONDS = 5.0

    def backdrop(self):
        return predict_backdrop()


class S10Reveal(SpokenScene):
    def construct(self):
        g,old,extra = graph_world(through=1997)
        ratio = ratio_box("50",TEXT)
        self.add(g,old,extra,ratio,g.year_line(1997,ORANGE))
        self.at("only 14 wolves")
        wseg = g.line(np.array([1997,1998]),np.array([24,14]),"w",WOLF)
        wdot = Dot(g.wp(1998,14),radius=0.13,color=TEXT)
        wlab = T("1998: 14 wolves",30,WOLF).move_to([2.7,-1.3,0])
        self.play(Create(wseg),FadeIn(wdot),FadeIn(wlab),run_time=1.4)
        self.at("Hundreds of moose")
        mseg = g.line(np.array([1997,1998]),np.array([500,700]),"m",MOOSE)
        mdot = Dot(g.mp(1998,700),radius=0.13,color=MOOSE)
        mlab = T("1998: about 700 moose",28,MOOSE).move_to([2.6,0.85,0])
        ring = Circle(radius=0.28,color=GOLD,stroke_width=4).move_to(g.mp(1998,700))
        self.play(Create(mseg),FadeIn(mdot),FadeIn(mlab),Create(ring),run_time=1.3)
        self.at("fits the rule")
        tick = T("✓  fits the rule",34,GREEN,weight=BOLD).move_to([3.7,0.0,0])
        self.play(FadeIn(tick,shift=UP*0.15),run_time=1.1)
        self.finish()


class S11Limit(SpokenScene):
    def construct(self):
        tp = TwoPanel("fits the rule","proves the cause",colors=(GREEN,RED),top=2.7,bottom=-2.2)
        tp.left_frame.set_fill(GREEN,opacity=0.16)
        tp.right_frame.set_fill(RED,opacity=0.16)
        breathe_fill(tp.left_frame,base=0.16,amp=0.05)
        breathe_fill(tp.right_frame,base=0.16,amp=0.05,speed=0.95)
        self.play(FadeIn(tp),run_time=1.0)
        self.at("one run of counts")
        left = VGroup(T("✓",110,GREEN),T("1995 → 1998",32,TEXT)).arrange(DOWN,buff=0.25)
        tp.put(left,"left")
        self.play(FadeIn(left),run_time=1.1)
        self.at("cannot prove")
        right = VGroup(T("×",110,RED),T("other things changed too",28,TEXT)).arrange(DOWN,buff=0.25)
        tp.put(right,"right")
        self.play(FadeIn(right),run_time=1.2)
        cap = caption("Counts can fit a rule without proving its cause.",size=30,color=GOLD)
        self.play(FadeIn(cap),run_time=0.8)
        self.finish()


class S12Exception(SpokenScene):
    def construct(self):
        g,data,extra = graph_world()
        n = ValueTracker(21)
        ratio = ratio_readout(n,lambda: TEXT)
        bar = g.year_line(1997,ORANGE)
        self.add(g,data,extra,ratio,bar)
        self.play(bar.animate.shift(RIGHT*(g.x(2016)-g.x(1997))),run_time=1.4)
        self.at("counted only two wolves")
        wdot = Dot(g.wp(2016,2),radius=0.14,color=TEXT)
        wlab = graph_note("2016: 2 wolves",[1.9,-1.65,0],WOLF,30)
        flat = g.line(np.array([2016,2017,2018]),np.array([2,2,2]),"w",WOLF,width=8)
        self.play(FadeIn(wdot),FadeIn(wlab),Indicate(flat,color=TEXT),run_time=1.2)
        self.at("estimated 1")
        mdot = Dot(g.mp(2016,1300),radius=0.14,color=MOOSE)
        mlab = graph_note("about 1,300 moose",[2.3,1.45,0],MOOSE,30)
        self.play(FadeIn(mdot),FadeIn(mlab),run_time=1.2)
        self.at("counter shoots")
        self.play(n.animate.set_value(650),ratio[0].animate.set_stroke(GOLD,width=5),run_time=1.5)
        self.finish()


class S13Inbreeding(SpokenScene):
    def construct(self):
        wolves,tree = family_world()
        panel = family_panel()
        ratio = ratio_box("650",TEXT)
        pile = VGroup(*[moose_icon(0.25).move_to([-5.5+(i%5)*0.55,2.0+(i//5)*0.48,0]) for i in range(10)])
        self.play(FadeIn(panel),FadeIn(pile,lag_ratio=0.04),FadeIn(ratio),run_time=1.0)
        self.at("expect more wolves")
        ghost = VGroup(*[wolf_icon(0.35).move_to([-2+i*0.75,0.4,0]) for i in range(6)]).set_opacity(0.22)
        self.play(FadeIn(ghost),run_time=1.0)
        self.at("That did not happen")
        self.play(FadeOut(ghost),FadeIn(wolves),run_time=1.0)
        self.at("close relatives")
        self.play(FadeIn(tree),run_time=1.3)
        self.at("called inbreeding")
        lab = chip("inbreeding: mating between close relatives",GOLD,size=28).move_to([1.6,-2.35,0])
        self.play(FadeIn(lab),Indicate(tree,color=GOLD,scale_factor=1.02),run_time=1.1)
        self.add(scope_tag("schematic"))
        self.finish()


class S14Traits(SpokenScene):
    def construct(self):
        wolves,tree = family_world()
        panel = family_panel()
        ratio = ratio_box("650",TEXT)
        pile = VGroup(*[moose_icon(0.25).move_to([-5.5+(i%5)*0.55,2.0+(i//5)*0.48,0]) for i in range(10)])
        self.add(panel,wolves,tree,ratio,pile,scope_tag("schematic"))
        self.at("harmful inherited traits")
        warnings = VGroup(*[T("!",42,RED,weight=BOLD).move_to(w.get_top()+UP*0.2) for w in wolves])
        lab = chip("harmful inherited traits",RED,size=30).move_to([-2.9,-2.25,0])
        self.play(FadeIn(warnings,shift=DOWN*0.1),FadeIn(lab),run_time=1.2)
        self.at("health problems")
        self.play(wolves.animate.set_opacity(0.5).shift(DOWN*0.15),run_time=1.0)
        self.at("shortage of moose")
        foodlab = T("plenty of food",30,MOOSE,weight=BOLD).next_to(pile,DOWN,buff=0.2)
        self.play(FadeIn(foodlab),Indicate(pile,color=MOOSE,scale_factor=1.03),run_time=1.0)
        self.at("not what held")
        cap = caption("Food was not the limit here.",size=36,color=GOLD)
        self.play(FadeIn(cap),run_time=1.1)
        self.finish()


class S15People(SpokenScene):
    def construct(self):
        world = island_world()
        ratio = ratio_box("137",TEXT)
        self.play(FadeIn(world),FadeIn(ratio),run_time=0.9)
        self.at("2018 and 2019")
        crates = VGroup(*[RoundedRectangle(width=1.3,height=1.1,corner_radius=0.08,color=GOLD,fill_color=GOLD,fill_opacity=0.12) for _ in range(3)]).arrange(RIGHT,buff=0.45).move_to([-1.2,-0.45,0])
        self.play(FadeIn(crates,shift=RIGHT*0.2),run_time=1.1)
        self.at("Park Service brought")
        newcomers = VGroup(*[wolf_icon(0.42).move_to([-2.3+i*0.85,-1.45+0.18*(i%2),0]) for i in range(5)])
        self.play(FadeOut(crates),FadeIn(newcomers,lag_ratio=0.12,shift=RIGHT*0.2),run_time=1.3)
        self.at("19 new wolves")
        lab = chip("2018 and 2019: 19 new wolves brought in",WOLF,size=30).move_to([0,3.3,0])
        layout_allowed(lab)
        g,data,extra = graph_world(through=2019)
        self.play(FadeOut(VGroup(world,newcomers,ratio)),FadeIn(g),FadeIn(data),FadeIn(lab),run_time=0.9)
        self.finish()


class S16Rule(SpokenScene):
    def construct(self):
        g = CountGraph(labels=False)
        data = g.data()
        graph_group = VGroup(g[0], g.axes_group[0], g.axes_group[1], data).scale(0.58).move_to([-3.15,-0.15,0])
        graph_label = T("NPS winter counts",24,TEAL).move_to([-3.6,2.05,0])
        self.play(FadeIn(graph_group),FadeIn(graph_label),run_time=1.0)
        self.at("Few moose")
        food = chip("food availability",MOOSE,size=28).move_to([3.6,2.2,0])
        clue = T("moose per wolf is a rough clue",24,GREY).next_to(food,DOWN,buff=0.15)
        self.play(FadeIn(food),FadeIn(clue),run_time=1.1)
        self.at("weather")
        weather = chip("weather",TEAL,size=26).move_to([2.6,0.9,0])
        self.play(FadeIn(weather),run_time=0.6)
        self.at("ticks")
        ticks = chip("ticks",RED,size=26).move_to([4.7,0.9,0])
        self.play(FadeIn(ticks),run_time=0.5)
        self.at("disease")
        disease = chip("disease",RED,size=26).move_to([2.6,-0.15,0])
        self.play(FadeIn(disease),run_time=0.6)
        self.at("inbreeding")
        inbreed = chip("inbreeding",GOLD,size=26).move_to([4.7,-0.15,0])
        self.play(FadeIn(inbreed),run_time=0.6)
        self.at("people moving wolves")
        people = chip("people moving wolves",WOLF,size=26).move_to([3.65,-1.25,0])
        self.play(FadeIn(people),run_time=0.9)
        self.at("Food is one limit")
        final = caption("Food is one limit on wolves, not the only one.",size=34,color=GOLD)
        self.play(FadeIn(final),run_time=1.2)
        self.finish()


class S17End(EndCard):
    LINE = "Food is one limit on wolves, not the only one."
