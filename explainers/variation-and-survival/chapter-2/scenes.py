"""Reading selection in a population.

COLOR MAP (kept across the film)
  TEAL  = tuskless inherited variant
  GOLD  = tusked inherited variant
  RED   = ivory-poaching pressure / paths that stop
  GREEN = survival and evidence supporting selection
  ORANGE = crab egg mass
  GREY  = neutral structure, models, and limits

All percentage bars below are computed from the reported percentages in script.json.
Animal icons are schematic markers, never counts unless a group size is printed beside a bar.
"""
from bp_parts import *


TUSKLESS = TEAL
TUSKED = GOLD
PRESSURE = RED
SUPPORT = GREEN
EGGS = "#F29E4C"


# ---------------------------------------------------------------------------
# Shared lesson pictures. Every continuing scene calls these builders.
class FilmScene(SpokenScene):
    """Spoken scene over the chapter's slowly moving data-field texture."""
    def setup(self):
        super().setup()
        field = VGroup(*[
            Line([x, -3.6, 0], [x + .7, 3.6, 0], color=GREY, stroke_width=6)
            for x in np.linspace(-6.8, 6.1, 16)
        ]).set_opacity(.28).set_z_index(-40)
        for ln in field:
            # Deliberate background texture; text is drawn above it and remains high-contrast.
            ln.layout_ok = True

        def flow(mob, dt):
            for ln in mob:
                ln.shift(RIGHT * .38 * dt)
                if ln.get_left()[0] > 6.9:
                    ln.shift(LEFT * 13.7)
        field.add_updater(flow)
        self.add(field)


def readable(mob, size=24):
    """Restore readable type after a carried picture has been geometrically reduced."""
    def visit(m):
        if isinstance(m, Text) and m.font_size < size:
            m.font_size = size
        for child in m.submobjects:
            visit(child)
    visit(mob)
    return mob


def elephant(tuskless=False, scale=1.0, color=None, outline=False):
    """Simple side-view elephant silhouette used as a trait marker."""
    c = color or (TUSKLESS if tuskless else TUSKED)
    fill = 0.0 if outline else 0.28
    body = Ellipse(width=1.35, height=0.78, color=c, stroke_width=4,
                   fill_color=c, fill_opacity=fill)
    head = Circle(radius=0.34, color=c, stroke_width=4,
                  fill_color=c, fill_opacity=fill).move_to([0.73, -0.02, 0])
    ear = Circle(radius=0.17, color=c, stroke_width=3,
                 fill_color=c, fill_opacity=0.12 if outline else 0.38).move_to([0.55, 0.06, 0])
    trunk = VMobject(color=c, stroke_width=6)
    trunk.set_points_as_corners([[0.98, -0.08, 0], [1.05, -0.48, 0], [0.9, -0.64, 0]])
    legs = VGroup(*[Line([x, -0.32, 0], [x, -0.67, 0], color=c, stroke_width=7)
                    for x in (-0.42, 0.22)])
    tail = Line([-0.66, 0.05, 0], [-0.86, -0.28, 0], color=c, stroke_width=4)
    parts = [body, head, ear, trunk, legs, tail]
    if not tuskless:
        parts.append(ArcBetweenPoints([0.96, -0.18, 0], [1.25, -0.1, 0], angle=-0.8,
                                      color=TEXT, stroke_width=4))
    g = VGroup(*parts).scale(scale)
    g.tuskless = tuskless
    return g


def data_bar(label, pct, n, width=7.4, height=0.72, center=ORIGIN, show_counts=True):
    """Computed stacked bar: teal width=pct; gold width=1-pct."""
    teal = Rectangle(width=width * pct, height=height, stroke_width=0,
                     fill_color=TUSKLESS, fill_opacity=0.95)
    gold = Rectangle(width=width * (1 - pct), height=height, stroke_width=0,
                     fill_color=TUSKED, fill_opacity=0.95)
    teal.move_to([-width / 2 + teal.width / 2, 0, 0])
    gold.next_to(teal, RIGHT, buff=0)
    outline = Rectangle(width=width, height=height, color=TEXT, stroke_width=2)
    bar = VGroup(teal, gold, outline).move_to(center)
    title = T(label, 30, TEXT, weight=BOLD).next_to(bar, UP, buff=0.18).align_to(bar, LEFT)
    pctlab = M(f"{100*pct:.1f}% teal", 28, TUSKLESS).next_to(bar, DOWN, buff=0.16).align_to(bar, LEFT)
    if show_counts:
        count = T(f"n = {n}", 26, GREY).next_to(bar, DOWN, buff=0.16).align_to(bar, RIGHT)
        g = VGroup(bar, title, pctlab, count)
    else:
        g = VGroup(bar, title, pctlab)
    g.bar, g.teal, g.gold = bar, teal, gold
    return g


def two_bars():
    pre = data_bar("prewar", 0.185, 54, center=[0, 1.45, 0])
    surv = data_bar("war survivors", 0.509, 108, center=[0, -1.25, 0])
    return VGroup(pre, surv)


def three_bars(compact=False):
    w = 3.55 if compact else 3.8
    h = 0.68
    xs = (-4.25, 0, 4.25)
    specs = (("prewar", .185, 54), ("survivors", .509, 108), ("daughters", .33, 91))
    bars = VGroup(*[data_bar(k, p, n, width=w, height=h, center=[x, 0.35, 0])
                    for x, (k, p, n) in zip(xs, specs)])
    line = Line([-5.9, -1.1, 0], [5.9, -1.1, 0], color=GREY, stroke_width=3)
    ticks = VGroup(*[Line([x, -1.0, 0], [x, -1.2, 0], color=GREY, stroke_width=3) for x in xs])
    return VGroup(bars, line, ticks)


def selection_gate(label=True):
    """Two fixed passages: a narrow gold route and wider teal route."""
    top = Polygon([-1.1, 2.55, 0], [1.1, 2.55, 0], [0.72, 0.35, 0], [-0.72, 0.35, 0],
                  color=PRESSURE, fill_color=PRESSURE, fill_opacity=.18, stroke_width=4)
    bottom = Polygon([-0.72, -0.35, 0], [0.72, -0.35, 0], [1.1, -2.55, 0], [-1.1, -2.55, 0],
                     color=PRESSURE, fill_color=PRESSURE, fill_opacity=.18, stroke_width=4)
    teal_gap = Line([-0.62, 0, 0], [-0.16, 0, 0], color=TUSKLESS, stroke_width=12)
    gold_gap = Line([0.2, 0, 0], [0.38, 0, 0], color=TUSKED, stroke_width=12)
    g = VGroup(top, bottom, teal_gap, gold_gap)
    if label:
        lab = T("ivory poaching", 30, PRESSURE, weight=BOLD).move_to([0, 3.05, 0])
        g.add(lab)
    return g


def question_backdrop():
    bars = readable(two_bars().scale(.78).shift(LEFT * 3.0 + UP * .1))
    gold = elephant(False, .82, outline=True).move_to([3.2, .9, 0])
    teal = elephant(True, .82, outline=True).move_to([3.2, -.55, 0])
    pulse(gold, base=4, amp=1.1, speed=2.0)
    pulse(teal, base=4, amp=1.1, speed=2.0)
    opts = VGroup(T("changed individuals?", 28, TUSKED).move_to([3.3, 1.85, 0]),
                  T("different group shares?", 28, TUSKLESS).move_to([3.3, -1.55, 0]))
    return VGroup(bars, gold, teal, opts)


def crab(scale=.9):
    shell = Ellipse(width=2.1, height=1.25, color=BLUE, stroke_width=5,
                    fill_color=BLUE, fill_opacity=.22)
    eyes = VGroup(*[Dot([x, .65, 0], radius=.07, color=TEXT) for x in (-.38, .38)])
    claws = VGroup(Arc(radius=.48, start_angle=.2, angle=2.3, color=BLUE, stroke_width=6).shift(LEFT*1.2+UP*.1),
                   Arc(radius=.48, start_angle=.65, angle=2.3, color=BLUE, stroke_width=6).shift(RIGHT*1.2+UP*.1))
    legs = VGroup(*[Line([sx*.65, y, 0], [sx*1.35, y-.35, 0], color=BLUE, stroke_width=5)
                    for sx in (-1, 1) for y in (-.1, -.38)])
    return VGroup(shell, eyes, claws, legs).scale(scale)


def egg_mass(rows=7, cols=11):
    dots = VGroup(*[Dot(radius=.075, color=EGGS).move_to([(c-(cols-1)/2)*.19, (r-(rows-1)/2)*.17, 0])
                    for r in range(rows) for c in range(cols)])
    return dots


# ---------------------------------------------------------------------------
class S00Hook(FilmScene):
    def construct(self):
        # The carried teal/gold population field appears before its labels.
        markers = VGroup()
        for i in range(14):
            e = elephant(i in {2, 6, 10}, .43).move_to([-5.7 + (i % 7)*1.85, 1.6-(i//7)*2.15, 0])
            markers.add(e)
        self.play(LaggedStart(*[FadeIn(e, scale=.7) for e in markers], lag_ratio=.06), run_time=2.1)
        self.at("inherited variants")
        legend = VGroup(chip("tuskless inherited variant", TUSKLESS, 28),
                        chip("tusked inherited variant", TUSKED, 28)).arrange(RIGHT, buff=.7).move_to([0,-2.55,0])
        self.play(FadeIn(legend, shift=UP*.15), run_time=.9)
        self.at("How can data")
        q = fit_text("Selection — or chance?", 7.5, 44, GOLD, weight=BOLD).move_to([0, 3.05, 0])
        self.play(FadeIn(q, shift=DOWN*.2), run_time=.8)
        self.at("Return to the same")
        targets = [[-4.3, 1.25, 0], [0, 1.25, 0], [4.3, 1.25, 0]]
        groups = [VGroup(*markers[:5]), VGroup(*markers[5:10]), VGroup(*markers[10:])]
        for g, p in zip(groups, targets):
            self.play(g.animate.scale(.72).move_to(p), run_time=.55)
        empty = VGroup(*[Rectangle(width=3.4, height=1.2, color=GREY, stroke_width=3).move_to(p)
                         for p in targets])
        self.play(FadeOut(markers), FadeOut(legend), FadeIn(empty), run_time=1.1)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Variation and survival"
    TITLE = "Reading Selection in a Population"


class S02Groups(FilmScene):
    def construct(self):
        leg = VGroup(elephant(True, .55), T("tuskless females", 28, TUSKLESS),
                     elephant(False, .55), T("tusked females", 28, TUSKED)).arrange(RIGHT, buff=.28).move_to([0,3.25,0])
        self.at("Teal marks")
        self.play(FadeIn(leg), run_time=1.0)
        bars = two_bars()
        pre, surv = bars[0], bars[1]
        self.at("Historical film")
        self.play(FadeIn(pre[1], shift=DOWN*.1), GrowFromEdge(pre.bar, LEFT), run_time=1.5)
        self.play(FadeIn(VGroup(*pre[2:])), run_time=.7)
        self.at("Later sightings")
        self.play(FadeIn(surv[1], shift=DOWN*.1), GrowFromEdge(surv.bar, LEFT), run_time=1.5)
        self.play(FadeIn(VGroup(*surv[2:])), run_time=.7)
        self.at("reported group sizes")
        self.play(Indicate(pre.bar, color=TUSKLESS), Indicate(surv.bar, color=TUSKLESS), run_time=1.5)
        self.finish()


class S03Predict(FilmScene):
    def construct(self):
        bars = readable(two_bars().scale(.78).shift(LEFT*3 + UP*.1))
        self.add(bars)
        self.at("teal share is higher")
        self.play(Indicate(bars[1].teal, color=TUSKLESS), run_time=1.2)
        gold = elephant(False, .82).move_to([-3.0, 1.5, 0])
        teal = elephant(True, .82).move_to([-3.0, -1.1, 0])
        gold_o = elephant(False, .82, outline=True).move_to([3.2, .9, 0])
        teal_o = elephant(True, .82, outline=True).move_to([3.2, -.55, 0])
        self.at("What changed")
        self.play(TransformFromCopy(gold, gold_o), TransformFromCopy(teal, teal_o), run_time=1.3)
        a = T("changed individuals?", 28, TUSKED).next_to(gold_o, UP, buff=.22)
        b = T("different group shares?", 28, TUSKLESS).next_to(teal_o, DOWN, buff=.22)
        self.at("Did individual elephants")
        pulse(gold_o)
        self.play(FadeIn(a), run_time=.8)
        self.at("two groups contain")
        pulse(teal_o)
        self.play(FadeIn(b), run_time=.8)
        q = question_card("What changed: individuals or group shares?", y=-3.18, size=30)
        self.play(FadeIn(q), run_time=.7)
        self.finish()


class S04Pause(PredictPause):
    QUESTION = "What changed: individuals or group shares?"
    SECONDS = 4.5
    CARD = {"y": -3.18, "size": 30}

    def backdrop(self):
        return question_backdrop()


class S05GroupReveal(FilmScene):
    def construct(self):
        bars = readable(two_bars().scale(.64).shift(UP*2.0))
        self.add(bars)
        left_gold = elephant(False, .75).move_to([-5.3, -.25, 0])
        left_teal = elephant(True, .75).move_to([-5.3, -1.9, 0])
        right_gold = elephant(False, .75).move_to([5.2, -.25, 0])
        right_teal = elephant(True, .75).move_to([5.2, -1.9, 0])
        self.at("Track two")
        self.play(FadeIn(left_gold), FadeIn(left_teal), run_time=.7)
        gp = ArcBetweenPoints(left_gold.get_center(), right_gold.get_center(), angle=-.18)
        tp = ArcBetweenPoints(left_teal.get_center(), right_teal.get_center(), angle=.18)
        gp.set_stroke(TUSKED, 5); tp.set_stroke(TUSKLESS, 5)
        self.play(Create(gp), Create(tp), run_time=1.0)
        self.at("gold animal stays gold")
        self.play(TransformFromCopy(left_gold, right_gold), run_time=1.35)
        self.at("teal animal stays teal")
        self.play(TransformFromCopy(left_teal, right_teal), run_time=1.35)
        # Extra paths show unequal survival without claiming exact individual outcomes.
        gold_paths = VGroup(*[Line([-4.4+i*.65,.35,0],[-1.5+i*.35,.35,0],color=TUSKED,stroke_width=4) for i in range(5)])
        teal_paths = VGroup(*[Line([-4.4+i*.75,-2.75,0],[3.3+i*.45,-2.75,0],color=TUSKLESS,stroke_width=4) for i in range(4)])
        self.at("survivor group contains")
        self.play(LaggedStart(*[Create(x) for x in gold_paths], lag_ratio=.1),
                  LaggedStart(*[Create(x) for x in teal_paths], lag_ratio=.1), run_time=1.5)
        self.at("survived poaching more often")
        self.play(*[FadeOut(x, shift=RIGHT*.2) for x in gold_paths[:3]],
                  *[x.animate.set_color(SUPPORT) for x in teal_paths], run_time=1.4)
        self.finish()


class S06Pressure(FilmScene):
    def construct(self):
        gate = selection_gate()
        self.at("Ivory poaching")
        self.play(FadeIn(gate[:2], scale=.9), run_time=1.0)
        self.play(FadeIn(gate[4]), run_time=.6)
        teal = elephant(True, .7).move_to([-3.8, 1.2, 0])
        gold = elephant(False, .7).move_to([3.8, 1.2, 0])
        self.at("affected the variants differently")
        self.play(FadeIn(teal), FadeIn(gold), FadeIn(gate[2:4]), run_time=.8)
        self.play(teal.animate.move_to([-.4,.05,0]), gold.animate.move_to([.3,.05,0]), run_time=1.4)
        teal_out = elephant(True,.7).move_to([-3.8,-1.55,0])
        self.play(TransformFromCopy(teal, teal_out), run_time=1.0)
        self.at("killed more often")
        stop = Line([-.15,-.38,0],[.75,.38,0],color=PRESSURE,stroke_width=9)
        self.play(Create(stop), FadeOut(gold, scale=.6), run_time=.9)
        supported = chip("supported explanation", SUPPORT, 30).move_to([-3.7,-3.0,0])
        wrong = chip("elephants chose or transformed", GREY, 27).move_to([3.2,-3.0,0])
        strike = Line(wrong.get_left()+LEFT*.08, wrong.get_right()+RIGHT*.08, color=PRESSURE, stroke_width=7)
        strike.layout_ok = True
        self.at("data support")
        self.play(FadeIn(supported), FadeIn(wrong), run_time=.8)
        self.at("not a choice")
        self.play(Create(strike), run_time=.75)
        self.finish()


class S07ChanceModel(FilmScene):
    def construct(self):
        panels = TwoPanel("equal-survival simulation", "observed survivors", colors=(GREY, TUSKLESS))
        self.at("population crash")
        self.play(FadeIn(panels), run_time=1.0)
        # Schematic equal-survival outcome range (explicitly not a data distribution).
        axis = Line([-5.5,-1.5,0],[-.9,-1.5,0],color=GREY,stroke_width=5)
        rng = Rectangle(width=1.8,height=.65,color=GREY,fill_color=GREY,fill_opacity=.28).move_to([-3.7,-.25,0])
        base = Line([-5.5,-.25,0],[-.9,-.25,0],color=GREY,stroke_width=2)
        lab = T("usual chance range", 28, GREY).next_to(rng, UP, buff=.2)
        sim = chip("equal survival", GREY, 30).move_to([-3.2,1.45,0])
        self.at("modeled the crash")
        self.play(FadeIn(sim), GrowFromCenter(rng), FadeIn(lab), Create(axis), Create(base), run_time=1.4)
        real = data_bar("real group", .509, 108, width=4.5, center=[3.25,.65,0])
        self.at("observed rise")
        self.play(GrowFromEdge(real.bar, LEFT), FadeIn(VGroup(*real[1:])), run_time=1.3)
        obs = Line([4.25,-1.6,0],[4.25,-.55,0],color=TUSKLESS,stroke_width=8)
        ol = M("50.9%", 32, TUSKLESS).next_to(obs, DOWN, buff=.2)
        self.play(Create(obs), FadeIn(ol), run_time=.7)
        self.at("far beyond")
        self.play(Indicate(obs, color=TUSKLESS, scale_factor=1.2), run_time=1.3)
        self.add(scope_tag("simulation range schematic"))
        self.finish()


class S08Daughters(FilmScene):
    def construct(self):
        world = three_bars()
        bars, line, ticks = world
        self.at("Daughters born later")
        self.play(Create(line), Create(ticks), run_time=.8)
        for i, cue in enumerate(("Daughters born later", "kept tusklessness", "pre war share")):
            if i:
                self.at(cue)
            b = bars[i]
            self.play(FadeIn(b[1]), GrowFromEdge(b.bar, LEFT), FadeIn(VGroup(*b[2:])), run_time=1.0)
        fitlab = chip("fits inheritance + selection", SUPPORT, 28).move_to([-2.6,-2.25,0])
        self.at("pattern fits")
        self.play(FadeIn(fitlab), run_time=.7)
        trait = chip("visible trait", TUSKLESS, 28).move_to([3.3,-2.05,0])
        unknown = chip("exact allele unknown", GREY, 28).next_to(trait, DOWN, buff=.25)
        self.at("exact allele")
        self.play(FadeIn(trait), FadeIn(unknown), run_time=.9)
        self.at("every elephant")
        self.play(Indicate(unknown, color=GREY), run_time=1.1)
        self.finish()


class S10Surplus(FilmScene):
    def construct(self):
        head = T("more young than environments can support", 36, TEXT, weight=BOLD).move_to([0,3.25,0])
        self.at("widen the picture")
        self.play(FadeIn(head, shift=DOWN*.15), run_time=.8)
        c = crab(1.05).move_to([-4.5,.75,0])
        eggs = egg_mass().move_to([-4.5,-.65,0])
        self.at("female blue crab")
        self.play(FadeIn(c, scale=.8), run_time=.8)
        self.play(LaggedStart(*[FadeIn(d, scale=.4) for d in eggs], lag_ratio=.012), run_time=1.5)
        mom = elephant(True,1.2,color=GREY).move_to([4.25,.55,0])
        calf = elephant(True,.68,color=GREY).move_to([5.35,-.55,0])
        self.at("elephant mother")
        self.play(FadeIn(mom), FadeIn(calf), run_time=1.0)
        gate = Polygon([-1.1,1.75,0],[1.1,1.75,0],[.55,-.15,0],[1.1,-2.2,0],[-1.1,-2.2,0],[-.55,-.15,0],
                       color=GREY,fill_color=GREY,fill_opacity=.18,stroke_width=4)
        gl = T("environment",28,GREY).move_to([0,2.15,0])
        self.at("Most crab young die")
        self.play(FadeIn(gate), FadeIn(gl), run_time=.7)
        survivors = VGroup(*[eggs[i].copy() for i in (8, 34, 62)])
        self.play(FadeOut(eggs), survivors.animate.move_to([0,-.1,0]).scale(1.7), run_time=1.4)
        adults = VGroup(*[Dot(radius=.12,color=SUPPORT).move_to([-.35+i*.35,-2.55,0]) for i in range(3)])
        self.play(Transform(survivors, adults), run_time=1.0)
        self.finish()


class S11Range(FilmScene):
    def construct(self):
        c = crab(.8).move_to([-5.2,.6,0]); e = elephant(True,.9,color=GREY).move_to([5.2,.6,0])
        arrow = DoubleArrow([-5.0,-1.5,0],[5.0,-1.5,0],color=TEXT,stroke_width=5,tip_length=.25)
        self.at("endpoints on a range")
        self.play(FadeIn(c), FadeIn(e), GrowFromCenter(arrow), run_time=1.2)
        left = VGroup(T("many young",30,EGGS,weight=BOLD),T("less per young",26,TEXT)).arrange(DOWN,buff=.12).move_to([-4.5,-2.3,0])
        right = VGroup(T("fewer young",30,GREY,weight=BOLD),T("more care",26,TEXT)).arrange(DOWN,buff=.12).move_to([4.5,-2.3,0])
        self.at("many young")
        self.play(FadeIn(left), run_time=.7)
        self.at("fewer young")
        self.play(FadeIn(right), run_time=.7)
        mids = VGroup(Circle(.42,color=BLUE),Triangle(color=TUSKLESS).scale(.52),Square(.72,color=GOLD)).arrange(RIGHT,buff=1.0).move_to([0,.45,0])
        self.at("Many species")
        self.play(LaggedStart(*[FadeIn(x,shift=UP*.15) for x in mids],lag_ratio=.25), run_time=1.4)
        label = T("reproductive strategies",32,TEXT).next_to(arrow,UP,buff=.25)
        self.play(FadeIn(label), run_time=.6)
        self.add(scope_tag("schematic"))
        self.finish()


class S12Fitness(FilmScene):
    def construct(self):
        gate = selection_gate(label=False).scale(.8).shift(UP*.35)
        young = VGroup(*[elephant(i%2==0,.48).move_to([-5.4+i*1.35,2.1,0]) for i in range(9)])
        self.at("count offspring")
        self.play(FadeIn(young), FadeIn(gate), run_time=1.0)
        nextgen = VGroup(*[elephant(i%3!=0,.48).move_to([-2.8+i*1.4,-2.05,0]) for i in range(5)])
        self.at("survive and reproduce")
        self.play(LaggedStart(*[TransformFromCopy(young[i],nextgen[j]) for j,i in enumerate((0,2,4,6,8))],lag_ratio=.18),run_time=1.8)
        ng = T("offspring in the next generation",30,SUPPORT,weight=BOLD).move_to([0,-3.1,0])
        self.play(FadeIn(ng),run_time=.6)
        decoys = VGroup(*[chip(s,GREY,27) for s in ("strength","effort","need")]).arrange(RIGHT,buff=.35).move_to([0,3.15,0])
        self.at("Strength")
        self.play(FadeIn(decoys),run_time=.6)
        self.at("not the score")
        self.play(FadeOut(decoys,shift=UP*.5),run_time=.8)
        cond = chip("conditions",PRESSURE,30).move_to([4.7,.3,0])
        self.at("conditions decide")
        self.play(FadeIn(cond),Indicate(gate,color=PRESSURE),run_time=1.0)
        self.finish()


class S13Rule(FilmScene):
    def construct(self):
        specs = (("prewar  18.5%", .185), ("survivors  50.9%", .509), ("daughters  33.0%", .33))
        bars = VGroup()
        for y, (lab, pct) in zip((1.9, .35, -1.2), specs):
            b = data_bar(lab, pct, 0, width=3.9, height=.5, center=[-4.25, y, 0], show_counts=False)
            # In this compact evidence recap, keep one combined computed label per bar.
            b.remove(b[2])
            bars.add(b)
        gate = selection_gate(False).scale(.55).shift(RIGHT*3.8+UP*.25)
        self.at("inherited variations")
        self.play(FadeIn(bars),FadeIn(gate),run_time=1.2)
        rule = caption("Inherited variation + reproductive success → population change",size=30,color=GOLD,y=-3.15)
        self.at("populations change")
        self.play(FadeIn(rule),run_time=.8)
        labels = ("trait pattern","pressure","survival","daughters")
        strands = VGroup()
        for i,(lab,col) in enumerate(zip(labels,(TUSKLESS,PRESSURE,SUPPORT,TUSKLESS))):
            y=2.3-i*.75
            ln = Line([.2,y,0],[2.75,-1.95+(i-1.5)*.06,0],color=col,stroke_width=5)
            ln.layout_ok = True  # deliberate evidence strands converge beside the conclusion
            strand=VGroup(T(lab,27,col).move_to([0,y,0],aligned_edge=RIGHT), ln)
            strands.add(strand)
        self.at("trait pattern")
        self.play(LaggedStart(*[FadeIn(s,shift=RIGHT*.15) for s in strands],lag_ratio=.25),run_time=2.0)
        support=chip("selection supported",SUPPORT,31).move_to([4.45,-2.0,0])
        self.at("support that rule")
        self.play(FadeIn(support),*[s[1].animate.set_color(SUPPORT) for s in strands],run_time=1.0)
        self.finish()


class S14Limits(FilmScene):
    def construct(self):
        bars=readable(three_bars().scale(.72).shift(UP*.65), 22)
        self.at("before and after data")
        self.play(FadeIn(bars),run_time=1.0)
        frame=VGroup(Line([-6.1,2.75,0],[5.0,2.75,0],color=SUPPORT,stroke_width=4),
                     Line([-6.1,2.75,0],[-6.1,-2.25,0],color=SUPPORT,stroke_width=4),
                     Line([-6.1,-2.25,0],[3.9,-2.25,0],color=SUPPORT,stroke_width=4))
        evidence=T("evidence",30,SUPPORT,weight=BOLD).move_to([-5.15,3.15,0])
        self.at("selective pressure")
        self.play(Create(frame),FadeIn(evidence),run_time=1.3)
        items=VGroup(*[chip(x,c,25) for x,c in (("pressure",PRESSURE),("survival estimate",SUPPORT),("chance comparison",GREY),("later daughters",TUSKLESS))]).arrange(RIGHT,buff=.22).move_to([0,-1.65,0])
        self.play(LaggedStart(*[FadeIn(x) for x in items],lag_ratio=.18),run_time=1.4)
        gap=T("limits stay open",28,GREY).move_to([5.25,-2.25,0])
        self.at("keeping its limits")
        self.play(FadeIn(gap),run_time=.7)
        supported=chip("selection supported",SUPPORT,32).move_to([0,3.2,0])
        self.play(FadeIn(supported),run_time=.7)
        self.finish()


class S15Return(FilmScene):
    def construct(self):
        world=three_bars()
        bars,line,ticks=world
        self.at("population snapshots")
        self.play(Create(line),Create(ticks),LaggedStart(*[FadeIn(b,scale=.85) for b in bars],lag_ratio=.22),run_time=1.6)
        snaps=VGroup(*[Rectangle(width=4.0,height=3.25,color=GREY,stroke_width=3).move_to([x,.25,0]) for x in (-4.25,0,4.25)])
        self.play(Create(snaps),run_time=.9)
        filt=selection_gate(False).scale(.15).move_to([-2.1,-1.9,0])
        self.at("filter as a comparison")
        self.play(FadeIn(filt),run_time=.7)
        paths=VGroup(Arrow([-2.8,-2.0,0],[-1.4,-2.0,0],color=TUSKLESS,stroke_width=4,buff=0),
                     Arrow([-2.8,-1.75,0],[-1.8,-1.75,0],color=TUSKED,stroke_width=4,buff=0))
        self.play(Create(paths),run_time=.8)
        q=question_card("Who left the next generation?",y=-3.15,size=34,color=GOLD)
        self.at("Then ask")
        self.play(FadeIn(q,shift=UP*.15),run_time=.8)
        self.at("inherited differences")
        self.play(Indicate(bars,color=GOLD,scale_factor=1.03),run_time=1.2)
        self.finish()


class S16End(EndCard):
    LINE = "When inherited variations affect reproductive success,\npopulations change across generations."
