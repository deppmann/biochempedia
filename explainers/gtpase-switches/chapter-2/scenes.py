"""GTPase switches, chapter 2: How the Timer Breaks.

COLOR MAP (copied from chapter 1's script.json)
  SLATE = GDP/off
  GOLD  = GTP/on
  TEAL  = GEF/loading action
  CLAY  = GAP/RGS/cutting action
  GREY  = membrane, axes, and de-emphasized context

All activity traces are explicitly labelled schematic.  The carried switch world is
built by switch_world() at one scale and in one position throughout the film.
"""
from bp_parts import *


SLATE = "#7D8796"
CLAY = "#C96F5B"
ON = GOLD
LOAD = TEAL
CUT = CLAY


def stage_panel():
    """A quiet, non-semantic canvas that gives the carried world visual weight."""
    panel = RoundedRectangle(
        corner_radius=0.22, width=13.0, height=6.45,
        stroke_color=GREY, stroke_width=7, stroke_opacity=0.32,
        fill_color=GREY, fill_opacity=0.10,
    ).move_to([0, -0.05, 0]).set_z_index(-5)
    panel._breath_t = 0.0

    def breathe(mob, dt):
        mob._breath_t += dt
        mob.set_fill(GREY, opacity=0.10 + 0.035 * np.sin(1.7 * mob._breath_t))

    return panel.add_updater(breathe)


def membrane():
    """The chapter-one membrane, rebuilt at the same coordinates in every scene."""
    return RoundedRectangle(
        corner_radius=0.12, width=12.0, height=0.48,
        stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.22,
    ).move_to([0, 2.35, 0])


def receptor(opacity=1.0):
    r = RoundedRectangle(
        corner_radius=0.16, width=0.9, height=1.35,
        stroke_color=LOAD, stroke_width=4, fill_color=LOAD, fill_opacity=0.18,
    ).move_to([-4.85, 1.85, 0])
    return r.set_opacity(opacity)


def switch_block(label="GTPase", color=ON, at=(-1.25, 0.65, 0), width=2.7):
    return boxed_label(label, color, size=32, box=(width, 1.25), pad=0.25).move_to(at)


def nucleotide(kind="GTP", at=(1.55, 0.65, 0), color=ON):
    """A labelled token with three plain tabs; it is a diagram, not a structure."""
    body = boxed_label(kind, color, size=30, box=(1.65, 0.9)).move_to(at)
    tabs = VGroup(*[
        RoundedRectangle(corner_radius=0.06, width=0.30, height=0.30,
                         stroke_color=color, stroke_width=2.5,
                         fill_color=color, fill_opacity=0.55)
        for _ in range(3)
    ]).arrange(RIGHT, buff=0.09).next_to(body, RIGHT, buff=0.16)
    g = VGroup(body, tabs)
    g.tabs = tabs
    return g


def activity_plot():
    return Plot(
        box=(-5.65, 5.25, -2.45, -1.05), xr=(0, 10), yr=(0, 1.15),
        xticks=(), yticks=(), xlabel="", ylabel="", color=GREY,
        size=24, label_size=28, stroke=3,
    )


def interval_fn(end=6.0, start=1.0):
    """Computed rectangular activity interval used by every schematic trace."""
    return lambda t: 0.08 if t < start else (1.0 if t <= end else 0.08)


def trace_picture(end=6.0, color=ON, live_to=None):
    p = activity_plot()
    curve = (p.curve(interval_fn(end), color=color, width=7)
             if live_to is None else p.live_curve(interval_fn(end), live_to, color=color, width=7))
    tag = T("schematic", 24, GREY).move_to([4.72, -2.83, 0])
    return VGroup(p, curve, tag), p, curve


def switch_world(label="GTPase", state="on", trace_end=6.0, live_to=None,
                 receptor_opacity=1.0, token_kind=None):
    """The one carried world: membrane, receptor, switch, token, and activity trace."""
    col = ON if state == "on" else SLATE
    token_kind = token_kind or ("GTP" if state == "on" else "GDP")
    tr, p, curve = trace_picture(trace_end, ON, live_to)
    g = VGroup(membrane(), receptor(receptor_opacity), switch_block(label, col),
               nucleotide(token_kind, color=col), tr)
    g.switch, g.token, g.trace, g.plot, g.curve = g[2], g[3], tr, p, curve
    panel = stage_panel()
    g.add(panel)
    bob(g[1], amp=0.11, speed=1.35)
    return g


def arrow_between(a, b, color, text=None, above=True):
    ar = Arrow(a, b, buff=0.12, color=color, stroke_width=6, tip_length=0.24)
    if text:
        lab = T(text, 28, color).next_to(ar, UP if above else DOWN, buff=0.16)
        return VGroup(ar, lab)
    return ar


def cut_mark(at=(2.55, 0.65, 0)):
    """A schematic cutting alignment: two chevrons, never an atom-level picture."""
    c = np.array(at, float)
    return VGroup(
        Line(c + [-0.35, 0.35, 0], c, color=CUT, stroke_width=7),
        Line(c, c + [-0.35, -0.35, 0], color=CUT, stroke_width=7),
    )


def choices_card():
    q = question_card(
        "What happens to the active interval?",
        ["longer", "shorter", "unchanged"],
        y=-3.25, size=30, chip_size=28,
    )
    q.chips.move_to([0, 3.2, 0])
    return q


class S00Hook(SpokenScene):
    def construct(self):
        t = ValueTracker(0.0)
        world = switch_world(live_to=t, trace_end=6.0)
        self.at("first film followed")
        self.play(FadeIn(VGroup(world[0], world[1], world.switch, world.token, world[-1])),
                  Create(world.plot), run_time=1.4)
        self.add(world.curve, world.trace[-1])
        self.play(t.animate.set_value(6.1), run_time=3.0, rate_func=linear)
        off = arrow_between([3.2, 0.65, 0], [4.05, 0.65, 0], CUT)
        cut_lab = T("cut", 28, CUT).move_to([3.65, 1.35, 0])
        slate = switch_block("GDP / off", SLATE, at=(5.25, 0.65, 0), width=2.05)
        self.at("cutting turned")
        self.play(GrowArrow(off), FadeIn(cut_lab), FadeIn(slate), run_time=1.2)
        self.at("what happens")
        self.play(FadeOut(slate), FadeOut(cut_lab), off.animate.shift(UP * 0.65), run_time=0.7)
        blocked = T("blocked", 30, CUT).move_to([4.92, 0.38, 0])
        fast = T("accelerated", 30, CUT).move_to([4.75, 1.85, 0])
        xmark = T("×", 42, CUT, weight=BOLD).move_to([4.25, 1.3, 0])
        chevs = VGroup(*[cut_mark((3.25 + i * 0.45, 0.0, 0)).scale(0.55) for i in range(3)])
        self.at("blocks the cut")
        self.play(FadeIn(blocked), FadeIn(xmark), run_time=0.8)
        self.at("speeds it up")
        self.play(FadeIn(fast), LaggedStart(*[FadeIn(c, shift=RIGHT * 0.15) for c in chevs], lag_ratio=0.18), run_time=1.2)
        self.at("same colors")
        self.play(Indicate(world.switch, color=ON), run_time=1.0)
        self.finish()


class S01Title(TitleCard):
    LESSON = "GTPase Switches: The Timer"
    TITLE = "How the Timer Breaks"

    def construct(self):
        t = ValueTracker(5.2)
        tr, p, curve = trace_picture(live_to=t)
        block = RoundedRectangle(corner_radius=0.16, width=2.8, height=1.15,
                                 stroke_color=ON, stroke_width=4,
                                 fill_color=ON, fill_opacity=0.22).move_to([0, 0.2, 0])
        backdrop = VGroup(block, p, curve, tr[-1]).set_opacity(0.32)
        title = T(self.TITLE, 56, TEXT, font=TITLE_FONT)
        lesson = T(self.LESSON.upper(), 22, GREY)
        rule = Line(LEFT * 1.25, RIGHT * 1.25, color=GOLD, stroke_width=4)
        card = VGroup(lesson, title, rule).arrange(DOWN, buff=0.30).move_to([0, 1.55, 0])
        lesson.shift(UP * 0.45)
        self.add(backdrop)
        pulse(block, base=3.5, amp=1.5, speed=4)
        self.play(FadeIn(card, shift=UP * 0.12), t.animate.set_value(8.5), run_time=1.45, rate_func=linear)
        self.play(FadeOut(card), t.animate.set_value(10), run_time=0.55, rate_func=linear)
        self.finish()


class S02Baseline(SpokenScene):
    def construct(self):
        t = ValueTracker(0.0)
        world = switch_world(state="off", live_to=t, trace_end=5.8)
        self.at("ordinary cycle")
        self.play(FadeIn(world), run_time=1.0)
        load = arrow_between([-4.25, 1.55, 0], [-2.45, 0.95, 0], LOAD)
        load_lab = T("loading", 28, LOAD).move_to([-3.45, 0.92, 0])
        self.at("teal loading event")
        self.play(GrowArrow(load), FadeIn(load_lab), run_time=0.8)
        gold = switch_block("GTPase", ON)
        gtp = nucleotide("GTP", color=ON)
        self.at("gold interval")
        self.play(Transform(world.switch, gold), Transform(world.token, gtp),
                  t.animate.set_value(3.0), run_time=2.2, rate_func=linear)
        cutter = cut_mark()
        self.at("intrinsic cutting")
        self.play(FadeIn(cutter, shift=LEFT * 0.2), t.animate.set_value(5.7), run_time=2.0, rate_func=linear)
        tab = world.token.tabs[-1]
        self.at("final phosphate")
        self.play(tab.animate.shift(DOWN * 0.9).set_opacity(0), run_time=1.0)
        slate = switch_block("GDP / off", SLATE)
        gdp = nucleotide("GDP", color=SLATE)
        gdp.tabs[-1].set_opacity(0)
        self.at("leaving GDP")
        self.play(Transform(world.switch, slate), Transform(world.token, gdp),
                  t.animate.set_value(8.8), run_time=2.0, rate_func=linear)
        neutral = caption("neutral reference", color=TEXT)
        self.at("neutral reference")
        self.play(FadeIn(neutral), FadeOut(load), FadeOut(load_lab), FadeOut(cutter), run_time=0.8)
        self.play(t.animate.set_value(10), run_time=1.0, rate_func=linear)
        self.finish()


class S03Analogue(SpokenScene):
    def construct(self):
        t = ValueTracker(0.0)
        world = switch_world(live_to=t, trace_end=10, token_kind="GTP analogue")
        self.at("replace GTP")
        self.play(FadeIn(world), run_time=1.0)
        lock = boxed_label("cannot cut", CUT, size=28, box=(2.2, 0.65)).next_to(world.token, UP, buff=0.25)
        self.at("cannot cut")
        self.play(FadeIn(lock), t.animate.set_value(2.5), run_time=1.8, rate_func=linear)
        load = arrow_between([-4.25, 1.55, 0], [-2.45, 0.95, 0], LOAD)
        load_lab = T("loading", 28, LOAD).move_to([-3.45, 0.82, 0])
        self.at("loading still")
        self.play(FadeIn(load), FadeIn(load_lab), t.animate.set_value(4.5), run_time=1.5, rate_func=linear)
        cutter = cut_mark((3.45, 0.65, 0))
        xmark = T("blocked", 28, CUT, weight=BOLD).move_to([4.2, -0.05, 0])
        self.at("off event fails")
        self.play(FadeIn(cutter), FadeIn(xmark), t.animate.set_value(7.2), run_time=2.0, rate_func=linear)
        self.at("after receptor input ends")
        self.play(world[1].animate.set_opacity(0.18), t.animate.set_value(10), run_time=2.4, rate_func=linear)
        self.finish()


class S04Toxin(SpokenScene):
    def construct(self):
        t = ValueTracker(0.0)
        world = switch_world(label="Gs alpha", live_to=t, trace_end=10)
        world.switch.shift(LEFT * 0.35)
        self.at("cholera toxin")
        self.play(FadeIn(world), run_time=0.9)
        toxin = boxed_label("cholera toxin", CUT, size=28).move_to([3.75, 1.75, 0])
        badge = T("blocked cut", 26, CUT).move_to([0.6, -0.48, 0])
        self.play(FadeIn(toxin, shift=DOWN * 0.2), t.animate.set_value(2), run_time=1.5, rate_func=linear)
        self.at("modification obstructs")
        self.play(toxin.animate.move_to([1.45, 1.72, 0]), FadeIn(badge),
                  t.animate.set_value(4), run_time=1.7, rate_func=linear)
        ac = ValueTracker(0.15)
        gauge = dial(ac, center=[4.45, 0.15, 0], radius=1.15, label="adenylyl cyclase", color=ON,
                     fmt="ON", scale=1, size=34)
        self.at("cyclase remains active")
        self.add(gauge)
        self.play(ac.animate.set_value(0.92),
                  t.animate.set_value(6.3), run_time=2.0, rate_func=linear)
        camps = VGroup(*[Dot(radius=0.11, color=TEAL) for _ in range(12)]).arrange_in_grid(3, 4, buff=0.18)
        camps.move_to([4.2, 2.15, 0])
        camp_lab = T("cyclic AMP", 28, TEAL).move_to([2.3, 3.05, 0])
        self.at("cyclic amp stays elevated")
        self.play(LaggedStart(*[FadeIn(d, shift=UP * 0.3) for d in camps], lag_ratio=0.07),
                  FadeIn(camp_lab), t.animate.set_value(8.3), run_time=2.2, rate_func=linear)
        self.at("timer stalls")
        self.play(Indicate(world.switch, color=ON), t.animate.set_value(10), run_time=1.7, rate_func=linear)
        self.finish()


class S05Predict(SpokenScene):
    def construct(self):
        t = ValueTracker(0.0)
        world = switch_world(label="G alpha", live_to=t, trace_end=7)
        self.at("add extra RGS")
        self.play(FadeIn(world), run_time=0.8)
        rgs = switch_block("RGS", CUT, at=(4.72, 0.65, 0), width=1.65)
        self.play(FadeIn(rgs, shift=LEFT * 0.6), t.animate.set_value(2.5), run_time=1.8, rate_func=linear)
        matched = T("all else matched", 28, GREY).move_to([4.1, 1.72, 0])
        self.at("all other parts")
        self.play(FadeIn(matched), t.animate.set_value(4.6), run_time=1.5, rate_func=linear)
        q = choices_card()
        self.at("should its active interval")
        self.play(FadeIn(q.question), t.animate.set_value(6.1), run_time=1.2, rate_func=linear)
        self.at("grow longer")
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.12) for c in q.chips], lag_ratio=0.22),
                  t.animate.set_value(7.4), run_time=2.3, rate_func=linear)
        self.finish()


class S06Pause(PredictPause):
    QUESTION = "What happens to the active interval?"
    OPTIONS = ["longer", "shorter", "unchanged"]
    SECONDS = 4.5

    def backdrop(self):
        world = switch_world(label="G alpha", trace_end=7.4)
        rgs = switch_block("RGS", CUT, at=(4.72, 0.65, 0), width=1.65)
        bob(rgs, amp=0.09, speed=1.8)
        return VGroup(world, rgs, T("all else matched", 28, GREY).move_to([4.1, 1.72, 0]))


class S07Reveal(SpokenScene):
    def construct(self):
        t = ValueTracker(0.0)
        world = switch_world(label="G alpha", live_to=t, trace_end=4.0)
        rgs = switch_block("RGS", CUT, at=(4.72, 0.65, 0), width=1.65)
        q = choices_card()
        self.add(world, rgs, q)
        shorter = q.chips[1]
        self.at("shorter")
        self.play(shorter[0].animate.set_fill(CUT, opacity=0.55).set_stroke(CUT, width=5), run_time=0.7)
        chevs = VGroup(*[cut_mark((2.65 + i * 0.42, 0.65, 0)).scale(0.55) for i in range(3)])
        self.at("accelerates cutting")
        self.play(FadeOut(q), LaggedStart(*[FadeIn(c, shift=RIGHT * 0.16) for c in chevs], lag_ratio=0.16),
                  t.animate.set_value(3.5), run_time=2.0, rate_func=linear)
        tab = world.token.tabs[-1]
        self.at("phosphate leaves sooner")
        self.play(tab.animate.shift(DOWN * 0.85).set_opacity(0), t.animate.set_value(5.0), run_time=1.4, rate_func=linear)
        slate = switch_block("GDP / off", SLATE)
        self.at("returns to slate")
        self.play(Transform(world.switch, slate), t.animate.set_value(7.0), run_time=1.7, rate_func=linear)
        family = T("Gi and Gq", 30, CUT, weight=BOLD).move_to([3.5, 1.65, 0])
        self.at("family boundary matters")
        self.play(FadeOut(chevs), FadeIn(family), t.animate.set_value(8.2), run_time=1.3, rate_func=linear)
        gs = switch_block("Gs", GREY, at=(3.6, 0.55, 0), width=1.5)
        note = T("not this RGS target", 28, GREY).next_to(gs, DOWN, buff=0.18)
        self.at("not have this effect")
        self.play(FadeOut(rgs), FadeIn(gs), FadeIn(note), t.animate.set_value(10), run_time=2.1, rate_func=linear)
        self.finish()


class S08G12v(SpokenScene):
    def construct(self):
        t = ValueTracker(0.0)
        world = switch_world(label="Ras G12V", live_to=t, trace_end=10)
        tether = Line([-1.25, 1.28, 0], [-1.25, 2.10, 0], color=GREY, stroke_width=5)
        self.at("G12 V")
        self.play(FadeIn(world), Create(tether), run_time=1.0)
        gap = switch_block("GAP", CUT, at=(4.75, 0.25, 0), width=1.65)
        self.at("gap may bind")
        self.play(FadeIn(gap, shift=LEFT * 0.7), t.animate.set_value(3.0), run_time=2.0, rate_func=linear)
        aligned = cut_mark((2.55, 0.95, 0))
        offset = cut_mark((2.95, 0.25, 0))
        self.at("arrangement fails")
        self.play(FadeIn(aligned), Transform(aligned, offset), t.animate.set_value(5.3), run_time=2.0, rate_func=linear)
        failure = boxed_label("catalytic failure", CUT, size=28).move_to([3.7, 1.65, 0])
        self.at("catalytic failure")
        self.play(FadeIn(failure), t.animate.set_value(7.4), run_time=1.7, rate_func=linear)
        present = T("GAP is present", 28, TEXT).move_to([3.65, -0.85, 0])
        self.at("not missing gap")
        self.play(FadeIn(present), Indicate(gap, color=CUT), t.animate.set_value(8.5), run_time=1.5, rate_func=linear)
        self.at("far longer")
        self.play(t.animate.set_value(10), Indicate(world.curve, color=ON), run_time=1.8, rate_func=linear)
        self.finish()


class S09Q61(SpokenScene):
    def construct(self):
        self.add(stage_panel())
        panels = TwoPanel("Ras G12V", "Ras Q61", colors=(ON, ON), top=3.0, bottom=-2.35)
        a = switch_block("G12V", ON, width=2.0)
        b = switch_block("Q61", ON, width=2.0)
        panels.put(a, "left"); panels.put(b, "right")
        a.shift(UP * 0.9); b.shift(UP * 0.9)
        bob(a, amp=0.08, speed=1.2)
        bob(b, amp=0.08, speed=1.2, seed=2)
        tr1 = Line([-5.2, -1.25, 0], [-1.2, -1.25, 0], color=ON, stroke_width=8)
        tr2 = Line([1.2, -1.25, 0], [5.2, -1.25, 0], color=ON, stroke_width=8)
        gap = switch_block("GAP", CUT, at=(-1.4, 0.45, 0), width=1.45).scale(0.8)
        self.at("Q61")
        self.play(FadeIn(panels), FadeIn(a), FadeIn(b), run_time=1.0)
        self.at("without gap")
        no_gap = T("without GAP", 28, GREY).move_to([3.2, -0.48, 0])
        self.play(FadeIn(gap), FadeIn(no_gap), Create(tr1), Create(tr2), run_time=2.0)
        long = T("abnormally long", 30, ON).move_to([0, -2.85, 0])
        self.at("both mutants")
        self.play(FadeIn(long), Indicate(tr1, color=ON), Indicate(tr2, color=ON), run_time=1.6)
        mis1 = cut_mark((-2.6, 0.05, 0)).scale(0.7)
        mis2 = VGroup(Line([2.35, 0.30, 0], [3.05, -0.05, 0], color=CUT, stroke_width=6),
                      Line([2.55, -0.25, 0], [3.15, 0.25, 0], color=CUT, stroke_width=6))
        self.at("damage the off")
        self.play(FadeIn(mis1), FadeIn(mis2), run_time=1.4)
        tags = VGroup(T("schematic", 24, GREY).move_to([-3.2, -1.75, 0]),
                      T("schematic", 24, GREY).move_to([3.2, -1.75, 0]))
        self.at("detailed defects differ")
        self.play(FadeIn(tags), mis1.animate.rotate(0.25), mis2.animate.rotate(-0.25), run_time=1.6)
        self.finish()


class S10S17n(SpokenScene):
    def construct(self):
        world = switch_world(label="Ras S17N", state="off", trace_end=1.2)
        world.token.set_opacity(0)
        self.at("dominant negative")
        self.play(FadeIn(world), run_time=1.0)
        gtp = nucleotide("GTP", at=(4.65, 0.65, 0), color=ON)
        dotted = DashedLine(gtp.get_left(), world.switch.get_right(), color=LOAD, stroke_width=5)
        self.at("binds GTP poorly")
        self.play(FadeIn(gtp), Create(dotted), run_time=1.5)
        self.play(gtp.animate.shift(LEFT * 0.65), run_time=0.8, rate_func=there_and_back)
        target = switch_block("target", GREY, at=(2.75, 1.35, 0), width=1.9)
        weak = T("no activation", 28, GREY).move_to([4.15, 3.0, 0])
        self.at("fails to activate")
        self.play(FadeIn(target), FadeIn(weak), run_time=1.3)
        side = T("loading side", 30, LOAD, weight=BOLD).move_to([-3.4, 3.05, 0])
        self.at("loading side")
        self.play(FadeIn(side), Indicate(dotted, color=LOAD), run_time=1.3)
        sos = switch_block("SOS", LOAD, at=(-3.55, 0.0, 0), width=1.6)
        may = T("may hold SOS", 28, LOAD).move_to([-3.55, -0.95, 0])
        self.at("may also hold")
        self.play(FadeIn(sos, shift=RIGHT * 0.5), FadeIn(may), run_time=1.5)
        normal = switch_block("normal Ras", GREY, at=(3.8, -0.6, 0), width=2.3)
        away = DashedLine(sos.get_right(), normal.get_left(), color=GREY, stroke_width=4)
        self.at("away from normal")
        self.play(FadeIn(normal), Create(away), sos.animate.shift(LEFT * 0.3), run_time=1.7)
        self.finish()


def big_cycle():
    off = switch_block("GDP / off", SLATE, at=(-3.65, 0.2, 0), width=2.5)
    on = switch_block("GTP / on", ON, at=(3.65, 0.2, 0), width=2.5)
    load = CurvedArrow(off.get_top(), on.get_top(), angle=-0.55, color=LOAD, stroke_width=6, tip_length=0.26)
    cut = CurvedArrow(on.get_bottom(), off.get_bottom(), angle=-0.55, color=CUT, stroke_width=6, tip_length=0.26)
    ll = T("loading", 32, LOAD).move_to([0, 1.85, 0])
    cl = T("cutting", 32, CUT).move_to([0, -1.55, 0])
    return VGroup(off, on, load, cut, ll, cl)


class S11Sort(SpokenScene):
    def construct(self):
        self.add(stage_panel())
        cyc = big_cycle()
        bob(cyc, amp=0.09, speed=1.15)
        self.at("changed arrow")
        self.play(FadeIn(cyc[:2]), Create(cyc[2]), Create(cyc[3]), FadeIn(cyc[4:]), run_time=1.5)
        obstruct = VGroup(*[
            boxed_label(x, CUT, size=26) for x in ("analogue", "toxin", "Ras G12V / Q61")
        ]).arrange(RIGHT, buff=0.25).move_to([0, -2.55, 0])
        self.at("analog toxin")
        self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.2) for x in obstruct], lag_ratio=0.18), run_time=1.7)
        block = T("blocked", 28, CUT, weight=BOLD).move_to([0, -0.25, 0])
        self.at("obstruct cutting")
        self.play(FadeIn(block), Indicate(cyc[3], color=CUT), run_time=1.2)
        rgs = boxed_label("RGS: faster", CUT, size=28).move_to([5.15, 1.55, 0])
        chevs = VGroup(*[cut_mark((1.4 - i * 0.45, -0.9, 0)).scale(0.45) for i in range(3)])
        self.at("extra RGS")
        self.play(FadeOut(block), FadeIn(rgs), LaggedStart(*[FadeIn(c) for c in chevs], lag_ratio=0.15), run_time=1.5)
        substrate = T("its substrates", 28, GREY).move_to([5.15, 2.2, 0])
        self.at("only for its substrates")
        self.play(FadeIn(substrate), run_time=1.0)
        s17 = boxed_label("Ras S17N", LOAD, size=28).move_to([0, 2.65, 0])
        self.at("impairs loading")
        self.play(FadeIn(s17), Indicate(cyc[2], color=LOAD), run_time=1.4)
        self.at("one cycle")
        self.play(Indicate(cyc, color=TEXT), run_time=1.2)
        self.finish()


class S12Scope(SpokenScene):
    def construct(self):
        self.add(stage_panel())
        rec = boxed_label("receptor", LOAD, size=30, box=(2.1, 1.0)).move_to([-5.0, 0.5, 0])
        gtp = boxed_label("GTPase", ON, size=30, box=(2.1, 1.0)).move_to([-1.7, 0.5, 0])
        target = boxed_label("target", TEXT, size=30, box=(2.1, 1.0)).move_to([1.7, 0.5, 0])
        mess = VGroup(*[Dot(radius=0.13, color=TEAL) for _ in range(10)]).arrange_in_grid(2, 5, buff=0.18).move_to([5.0, 0.5, 0])
        arrows = VGroup(
            arrow_between(rec.get_right(), gtp.get_left(), GREY),
            arrow_between(gtp.get_right(), target.get_left(), GREY),
            arrow_between(target.get_right(), mess.get_left(), GREY),
        )
        labels = VGroup(T("shutoff", 28, GREY).move_to([-3.35, 1.35, 0]),
                        T("target kinetics", 28, GREY).move_to([0, 1.35, 0]),
                        T("clearance", 28, GREY).move_to([3.35, 1.35, 0]))
        bob(mess, amp=0.10, speed=1.3)
        self.at("predicts direction")
        self.play(FadeIn(VGroup(rec, gtp, target, mess)), LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.2), run_time=1.6)
        exact = caption("direction, not exact response shape", color=TEXT)
        self.at("not the exact shape")
        self.play(FadeIn(exact), run_time=1.0)
        self.at("receptor shutoff")
        self.play(FadeIn(labels[0]), arrows[0].animate.set_color(LOAD), run_time=1.0)
        self.at("target kinetics")
        self.play(FadeIn(labels[1]), arrows[0].animate.set_color(GREY), arrows[1].animate.set_color(ON), run_time=1.0)
        self.at("messenger clearance")
        self.play(FadeIn(labels[2]), arrows[1].animate.set_color(GREY), arrows[2].animate.set_color(TEAL),
                  mess.animate.set_opacity(0.28), run_time=1.5)
        limit = boxed_label("keep the limit visible", GREY, size=28).move_to([0, 2.7, 0])
        self.at("limit visible")
        self.play(FadeIn(limit), arrows[2].animate.set_color(GREY), mess.animate.set_opacity(1), run_time=1.2)
        changed = arrows[1]
        self.at("locate the change step")
        self.play(changed.animate.set_color(CUT).set_stroke(width=9), run_time=1.2)
        self.at("judge the trace")
        self.play(Indicate(gtp, color=ON), run_time=1.0)
        self.finish()


class S13Close(SpokenScene):
    def construct(self):
        self.add(stage_panel())
        names = ["loading", "cutting", "clearance"]
        cols = [LOAD, CUT, TEAL]
        knobs = VGroup()
        trackers = []
        for x, name, col in zip((-4.2, 0, 4.2), names, cols):
            v = ValueTracker(0.5)
            trackers.append(v)
            knobs.add(dial(v, center=[x, 1.0, 0], radius=1.15, label=name, color=col,
                           fmt="", scale=1, size=28))
        bob(knobs, amp=0.10, speed=1.2)
        t = ValueTracker(0.0)
        trace, p, curve = trace_picture(end=6.0, live_to=t)
        self.at("lasting signal")
        self.add(knobs)
        self.play(FadeIn(p), FadeIn(trace[-1]), run_time=1.0)
        self.add(curve)
        self.play(t.animate.set_value(3.0), run_time=1.6, rate_func=linear)
        self.at("loading increased")
        self.play(trackers[0].animate.set_value(0.85), t.animate.set_value(4.5), run_time=1.2, rate_func=linear)
        self.at("cutting slowed")
        self.play(trackers[1].animate.set_value(0.15), knobs[1].animate.scale(1.15),
                  t.animate.set_value(6.3), run_time=1.5, rate_func=linear)
        self.at("clearance changed")
        self.play(trackers[2].animate.set_value(0.82), t.animate.set_value(7.5), run_time=1.3, rate_func=linear)
        rec = boxed_label("receptor", GREY, size=28).move_to([-4.2, 2.75, 0])
        self.at("prevents blaming")
        self.play(FadeIn(rec), knobs[0].animate.set_opacity(0.45), t.animate.set_value(8.4), run_time=1.2, rate_func=linear)
        rule = caption("the defect's position determines the prediction", color=TEXT)
        self.at("position of the defect")
        self.play(FadeIn(rule), knobs[1].animate.set_opacity(1).scale(1.08),
                  t.animate.set_value(10), run_time=1.7, rate_func=linear)
        self.finish()


class S14End(EndCard):
    LINE = "Block GTP cutting to prolong signaling; speed it to shorten signaling."
