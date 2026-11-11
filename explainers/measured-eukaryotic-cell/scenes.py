"""Amount over Volume — measured eukaryotic cell explainer.

COLOR MAP
  RED    Whi5, the proposed division brake
  GREEN  Start and commitment
  ORANGE RNA, protein, cytoplasm, and volume
  PURPLE genome
  BLUE   membrane and surface
  YELLOW concentration gauge, equations, and questions
"""
import math
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"

CELL_C = np.array([-2.45, -0.15, 0.0])
CELL_R = 2.25
GAUGE_C = np.array([4.55, -0.20, 0.0])
PAIR_CENTERS = (np.array([-4.15, -0.45, 0.0]), np.array([1.35, -0.45, 0.0]))
PAIR_GAUGES = (np.array([-1.75, -0.45, 0.0]), np.array([4.55, -0.45, 0.0]))


def tag(text, color=GREY, pos=(5.05, 3.35, 0), size=22):
    return T(text, size, color).move_to(pos)


def genome(center=CELL_C, scale=1.0):
    return RoundedRectangle(corner_radius=.12, width=.72 * scale, height=.5 * scale,
                            stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE,
                            fill_opacity=.55).move_to(np.array(center) + [-.5, .25, 0])


def cell_body(center=CELL_C, r=CELL_R, opacity=.20, width=7):
    return Circle(r, stroke_color=BLUE, stroke_width=width, fill_color=ORANGE,
                  fill_opacity=opacity).move_to(center)


DOT_POS = [(-.55, .56), (-.08, .7), (.44, .52), (-.72, .08), (-.18, .2),
           (.35, .08), (.68, -.22), (-.48, -.42), (.02, -.55), (.48, -.58)]


def content_dots(center=CELL_C, r=CELL_R, color=ORANGE, n=18, radius=.065, spread=.76):
    # Deterministic sunflower distribution: even visual density with no random claims.
    c = np.array(center, float); out = VGroup()
    for k in range(n):
        rr = spread * r * math.sqrt((k + .5) / n)
        a = k * math.pi * (3 - math.sqrt(5))
        out.add(Dot(c + [rr * math.cos(a), rr * math.sin(a), 0], radius=radius, color=color))
    out.add_updater(lambda m, dt, pivot=c: m.rotate(.40 * dt, about_point=pivot))
    return out


def fixed_dots(center=CELL_C, r=CELL_R, color=RED):
    c = np.array(center, float)
    out = VGroup(*[Dot(c + [x * r, y * r, 0], radius=.105, color=color) for x, y in DOT_POS])
    out.add_updater(lambda m, dt, pivot=c: m.rotate(.32 * dt, about_point=pivot))
    return out


def gauge(center=GAUGE_C, level=.75, color=YELLOW, label=None, start=False, narrow=False):
    c = np.array(center, float); w = .72 if narrow else 1.0; h = 4.25
    outline = RoundedRectangle(corner_radius=.12, width=w, height=h, stroke_color=GREY,
                               stroke_width=3, fill_opacity=0).move_to(c)
    ih = max(.05, (h - .18) * level)
    fill = Rectangle(width=w - .18, height=ih, stroke_width=0, fill_color=color,
                     fill_opacity=.72).move_to(c).align_to(outline, DOWN).shift(UP * .09)
    parts = VGroup(outline, fill)
    parts.outline, parts.fill = outline, fill
    if start:
        y = c[1] - h / 2 + .4 * h
        line = DashedLine([c[0] - w * .72, y, 0], [c[0] + w * .72, y, 0], color=GREEN,
                          stroke_width=4, dash_length=.12)
        lab = T("Start", 28, GREEN).next_to(line, RIGHT, buff=.12)
        parts.add(line, lab); parts.start_line = line
    if label:
        lab = T(label, 28, color).next_to(outline, UP, buff=.18)
        parts.add(lab)
    return parts


def readout(text, center=CELL_C, color=TEXT, size=28):
    return M(text, size, color).move_to([center[0], -3.25, 0])


def lock_icon(pos=(1.1, -.2, 0), open_lock=False):
    p = np.array(pos, float)
    box = RoundedRectangle(corner_radius=.08, width=.55, height=.46, color=RED,
                           fill_color=RED, fill_opacity=.25).move_to(p + [0, -.16, 0])
    arc = Arc(radius=.22, start_angle=0, angle=PI, color=RED, stroke_width=5)
    arc.move_to(p + ([.13, .16, 0] if open_lock else [0, .12, 0]))
    if open_lock: arc.rotate(-.45)
    return VGroup(box, arc)


def divide_arrow(pos=(1.15, -.1, 0)):
    a = Arrow(np.array(pos) + [0, -.55, 0], np.array(pos) + [0, .5, 0], buff=0,
              color=GREEN, stroke_width=6, tip_length=.22)
    return VGroup(a, T("divide", 28, GREEN).next_to(a, RIGHT, buff=.12))


def world(r=CELL_R, orange_n=18, gauge_level=0, gauge_color=YELLOW):
    b = cell_body(CELL_C, r)
    d = content_dots(CELL_C, r, ORANGE, orange_n)
    g = genome(CELL_C)
    q = gauge(GAUGE_C, max(gauge_level, .01), gauge_color)
    if gauge_level <= 0: q.fill.set_opacity(0)
    return VGroup(b, d, g, q)


def pair_world(question=True, radii=(1.35, 1.7), levels=(.9, .5)):
    all_m = VGroup()
    for c, gc, r, lev, vol in zip(PAIR_CENTERS, PAIR_GAUGES, radii, levels, ("20 fL", "40 fL")):
        b = cell_body(c, r); ds = fixed_dots(c, r)
        gg = gauge(gc, lev, RED, start=True, narrow=True)
        ro = M(vol, 28, TEXT).next_to(b, DOWN, buff=.18)
        all_m.add(VGroup(b, ds, gg, ro))
    if question:
        all_m.add(T("Which must grow more?", 40, YELLOW, font=TITLE_FONT).move_to([0, 3.25, 0]))
    return all_m


class S00Hook(SpokenScene):
    def construct(self):
        r = ValueTracker(1.7)
        body = always_redraw(lambda: cell_body(CELL_C, r.get_value()))
        contents = content_dots(CELL_C, 1.7, ORANGE, 16).set_opacity(.75)
        gen = genome(CELL_C)
        empty = gauge(GAUGE_C, .01); empty.fill.set_opacity(0)
        self.play(Create(body), FadeIn(contents), FadeIn(gen), Create(empty.outline), run_time=.9)
        bud = Circle(.08, stroke_color=BLUE, stroke_width=6, fill_color=ORANGE,
                     fill_opacity=.13).move_to(CELL_C + [1.72, .15, 0])
        self.play(r.animate.set_value(2.0), bud.animate.scale(6).shift(RIGHT * .25), run_time=1.3)
        self.at("no ruler")
        q = T("?", 92, YELLOW, weight=BOLD).move_to([1.15, 1.75, 0])
        self.play(FadeIn(q, shift=UP * .35), run_time=.45)
        self.play(bud.animate.scale(.65).shift(RIGHT * 3.8), r.animate.set_value(1.8), run_time=1.0)
        self.at("big enough to divide")
        self.play(r.animate.set_value(2.25), run_time=.75)
        self.at("too big")
        self.play(r.animate.set_value(2.52), body.animate.set_stroke(width=12), rate_func=there_and_back,
                  run_time=.7)
        self.play(Indicate(body, color=BLUE, scale_factor=1.02), run_time=.45)
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        w = world(r=2.35); w[1].set_opacity(.65)
        title = T("Amount over Volume", 48, TEXT, font=TITLE_FONT).move_to([0, 3.2, 0])
        self.add(w)
        self.play(FadeIn(title, shift=DOWN * .15), w[0].animate.scale(1.035), run_time=.65)
        self.wait(.75)
        self.play(FadeOut(title), run_time=.35)
        self.finish()


class S02Gauge(SpokenScene):
    def construct(self):
        r0 = 1.8; body = cell_body(CELL_C, r0); gen = genome(CELL_C)
        orange = content_dots(CELL_C, r0, ORANGE, 18).set_opacity(.10)
        reds = fixed_dots(CELL_C, r0)
        empty = gauge(GAUGE_C, .01); empty.fill.set_opacity(0)
        self.add(body, gen, orange, empty)
        self.at("concentration")
        ratio = T("amount ÷ volume", 42, YELLOW).move_to([0.45, 3.18, 0])
        self.play(Write(ratio), run_time=.8)
        self.at("divided by the room")
        self.play(Indicate(body, color=ORANGE, scale_factor=1.04), run_time=.8)
        self.at("gauge on the right")
        full = gauge(GAUGE_C, .92, YELLOW, "amount ÷ volume")
        self.play(Transform(empty, full), run_time=.8)
        self.at("ten red dots")
        count = M("10 dots", 30, RED).move_to([-2.45, -3.25, 0])
        self.play(FadeIn(reds), FadeIn(count), orange.animate.set_opacity(.03), run_time=.65)
        self.at("number stays the same")
        self.play(Indicate(VGroup(reds, count), color=RED, scale_factor=1.03), run_time=.55)
        self.at("room grows")
        body2 = cell_body(CELL_C, r0 * 2 ** (1 / 3)); reds2 = fixed_dots(CELL_C, r0 * 2 ** (1 / 3))
        half = gauge(GAUGE_C, .46, YELLOW, "amount ÷ volume")
        vol = M("volume  1 → 2", 28, TEXT).move_to([-2.45, -3.25, 0])
        self.play(Transform(body, body2), Transform(reds, reds2), Transform(empty, half),
                  Transform(count, vol), run_time=1.2)
        self.at("concentration falls")
        self.play(Indicate(empty.fill, color=YELLOW, scale_factor=1.02), FadeIn(tag("computed")), run_time=.55)
        self.finish()


class S03Brake(SpokenScene):
    def construct(self):
        body = cell_body(CELL_C, 1.75); reds = fixed_dots(CELL_C, 1.75); gen = genome(CELL_C)
        gg = gauge(GAUGE_C, .88, RED, "Whi5 ÷ volume")
        self.add(body, reds, gen, gg)
        newborn_w = body.width
        body.add_updater(lambda m: m.set_width(newborn_w * (1 + .04 * math.sin(self.renderer.time * 1.8))))
        self.at("leading model")
        model = tag("a leading model", YELLOW)
        self.play(FadeIn(model), run_time=.45)
        self.at("newborn daughter")
        body.clear_updaters()
        self.play(body.animate.scale(.92), reds.animate.scale(.92), run_time=.65)
        self.at("same dose")
        lab = T("Whi5: the brake", 34, RED).move_to([-2.45, 2.65, 0])
        self.play(FadeIn(lab), Indicate(reds, color=RED, scale_factor=1.08), run_time=.75)
        self.at("holds back start")
        start_g = gauge(GAUGE_C, .88, RED, "Whi5 ÷ volume", start=True)
        arrow = divide_arrow(); lock = lock_icon()
        self.play(Transform(gg, start_g), FadeIn(arrow), FadeIn(lock), run_time=.8)
        self.at("commits to dividing")
        self.play(Indicate(lock, color=RED, scale_factor=1.12), run_time=.55)
        self.finish()


class S04Commit(SpokenScene):
    def construct(self):
        body = cell_body(CELL_C, 1.75); reds = fixed_dots(CELL_C, 1.75); gen = genome(CELL_C)
        gg = gauge(GAUGE_C, .82, RED, "Whi5 ÷ volume", start=True)
        arrow = divide_arrow(); lock = lock_icon(); model = tag("computed, invented numbers", YELLOW)
        ro = M("30 fL   3.3 per fL", 27, TEXT).move_to([-1.55, -3.25, 0])
        self.add(body, reds, gen, gg, arrow, lock, model, ro)
        self.at("cell grows")
        self.play(Transform(body, cell_body(CELL_C, 2.08)), Transform(reds, fixed_dots(CELL_C, 2.08)),
                  Transform(gg, gauge(GAUGE_C, .4, RED, "Whi5 ÷ volume", start=True)),
                  Transform(ro, M("50 fL   2.0 per fL", 27, TEXT).move_to(ro)), run_time=2.3)
        self.at("green line")
        self.play(Indicate(gg, color=GREEN, scale_factor=1.02), run_time=.55)
        self.at("brake gives way")
        bud = Circle(.18, color=GREEN, stroke_width=6, fill_color=ORANGE, fill_opacity=.13).move_to(CELL_C + [2.08, .2, 0])
        self.play(Transform(lock, lock_icon(open_lock=True)), FadeIn(bud), body.animate.set_stroke(GREEN), run_time=.7)
        self.finish()


class S05Predict(SpokenScene):
    def construct(self):
        pair = pair_world(question=False)
        self.at("two newborns")
        self.play(FadeIn(pair, lag_ratio=.08), run_time=1.0)
        same = T("same dose", 30, RED).move_to([-1.1, -3.35, 0])
        self.at("same red dose")
        self.play(FadeIn(same), run_time=.5)
        self.at("Which must grow more")
        q = T("Which must grow more?", 42, YELLOW, font=TITLE_FONT).move_to([0, 3.25, 0])
        self.play(FadeIn(q, shift=DOWN * .2), run_time=.55)
        self.at("Pause and decide")
        self.play(Indicate(q, color=YELLOW, scale_factor=1.04), run_time=.6)
        self.finish()


class S06Think(Scene):
    def construct(self):
        p = pair_world(question=True)
        self.add(p)
        # Deliberate prediction pause: only the particles gently jitter.
        self.play(*[d.animate.shift([.035 * (-1) ** i, .025 * (-1) ** (i // 2), 0])
                    for i, d in enumerate([*p[0][1], *p[1][1]])], run_time=2.2, rate_func=there_and_back)
        self.wait(2.3)


class S07Reveal(SpokenScene):
    def construct(self):
        pair = pair_world(question=True); self.add(pair)
        self.at("small one")
        ans = T("The small one", 40, YELLOW, font=TITLE_FONT).move_to([0, 3.25, 0])
        self.play(Transform(pair[-1], ans), Indicate(pair[0][0], color=YELLOW, scale_factor=1.08), run_time=.7)
        self.at("dots start crowded")
        self.play(Indicate(pair[0][1], color=RED, scale_factor=1.12), run_time=.7)
        self.at("gauge starts higher")
        self.play(Indicate(pair[0][2], color=RED, scale_factor=1.03), run_time=.6)
        self.at("must grow more")
        left_done = VGroup(cell_body(PAIR_CENTERS[0], 1.84), fixed_dots(PAIR_CENTERS[0], 1.84),
                           gauge(PAIR_GAUGES[0], .4, RED, start=True, narrow=True),
                           M("50 fL  +30 fL", 28, TEXT).move_to([-4.15, -2.75, 0]))
        right_done = VGroup(cell_body(PAIR_CENTERS[1], 1.84), fixed_dots(PAIR_CENTERS[1], 1.84),
                            gauge(PAIR_GAUGES[1], .4, RED, start=True, narrow=True),
                            M("50 fL  +10 fL", 28, TEXT).move_to([1.35, -2.75, 0]))
        self.play(Transform(pair[1], right_done), run_time=.8)
        self.play(Transform(pair[0], left_done), run_time=1.5)
        self.at("same dose")
        bracket = Line([-4.15, -3.18, 0], [1.35, -3.18, 0], color=RED, stroke_width=4)
        sl = T("same dose at birth", 28, RED).next_to(bracket, DOWN, buff=.08)
        self.play(Create(bracket), FadeIn(sl), run_time=.55)
        self.at("simple model")
        self.play(Transform(pair[-1], T("simple model: same size", 34, YELLOW).move_to(pair[-1])), run_time=.6)
        self.at("Real cells are noisier")
        band = Rectangle(width=.68, height=.45, stroke_width=0, fill_color=GREEN, fill_opacity=.20).move_to(PAIR_GAUGES[1] + [0, -.2, 0])
        real = T("real: a range", 28, GREEN).move_to([0, 2.55, 0])
        self.play(FadeIn(band), FadeIn(real), FadeOut(bracket), FadeOut(sl), run_time=.7)
        self.at("part of the gap")
        self.play(pair[0][0].animate.scale(.96), run_time=.7)
        self.finish()


class S08Hold(NarratedScene):
    def construct(self):
        p = pair_world(question=False, radii=(1.84, 1.84), levels=(.4, .4)); self.add(p)
        buds = VGroup(*[Circle(.12, color=GREEN, stroke_width=5, fill_color=ORANGE, fill_opacity=.13)
                        .move_to(c) for c in [(-2.27, -.25, 0), (3.23, -.25, 0)]])
        self.play(GrowFromCenter(buds), Indicate(VGroup(p[0][2], p[1][2]), color=GREEN), run_time=1.5)
        self.finish()


class S09Idea(SpokenScene):
    def construct(self):
        body = cell_body(CELL_C, 1.8); reds = fixed_dots(CELL_C, 1.8)
        gg = gauge(GAUGE_C, .78, RED); gen = genome(CELL_C)
        self.add(body, reds, gg, gen)
        self.at("one idea")
        title = T("amount ÷ volume", 46, YELLOW, font=TITLE_FONT).move_to([0, 3.15, 0])
        self.play(FadeIn(title, shift=UP * .2), run_time=.7)
        self.at("cell grows")
        self.play(Transform(body, cell_body(CELL_C, 2.25)), Transform(reds, fixed_dots(CELL_C, 2.25)),
                  Transform(gg, gauge(GAUGE_C, .4, RED)), run_time=1.6)
        self.at("does not keep pace")
        rule = T("not keeping pace  →  diluted", 34, YELLOW).move_to([.6, -3.3, 0])
        self.play(Write(rule), Indicate(gg.fill, color=YELLOW), run_time=.8)
        self.finish()


class S10KeepPace(SpokenScene):
    def construct(self):
        body = cell_body(CELL_C, 1.75); red = fixed_dots(CELL_C, 1.75); gen = genome(CELL_C)
        redg = gauge([4.0, -.2, 0], .72, RED); self.add(body, red, gen, redg)
        newborn_w = body.width
        body.add_updater(lambda m: m.set_width(newborn_w * (1 + .035 * math.sin(self.renderer.time * 1.8))))
        self.at("dilution is a danger")
        self.play(red.animate.set_opacity(.08), redg.animate.set_opacity(.25), run_time=.6)
        self.at("RNA and protein")
        orange = content_dots(CELL_C, 1.75, ORANGE, 16)
        lab = T("RNA and protein", 34, ORANGE).move_to([-2.45, 2.55, 0])
        self.play(FadeIn(orange), FadeIn(lab), run_time=.7)
        self.at("cells work")
        self.play(Indicate(orange, color=ORANGE, scale_factor=1.05), run_time=.55)
        self.at("make them roughly")
        body.clear_updaters()
        larger = content_dots(CELL_C, 1.75 * 2 ** (1 / 3), ORANGE, 32)
        orange_g = gauge([5.25, -.2, 0], .68, ORANGE, "RNA/protein ÷ volume", narrow=True)
        self.play(FadeIn(orange_g), Transform(body, cell_body(CELL_C, 1.75 * 2 ** (1 / 3))),
                  Transform(orange, larger), run_time=2.0)
        self.at("in step with their volume")
        ro = M("30 → 60 fL", 28, TEXT).move_to([-2.45, -3.25, 0])
        self.play(FadeIn(ro), Indicate(orange_g.fill, color=ORANGE), FadeIn(tag("computed")), run_time=.65)
        self.finish()


class S11NoSignal(SpokenScene):
    def construct(self):
        # Both curves are computed over V=25..75: red=100/V, orange=2.
        ax = Axes(x_range=[25, 75, 25], y_range=[0, 4.5, 1], x_length=8.2, y_length=4.0,
                  axis_config={"color": GREY, "stroke_width": 3, "include_ticks": False}, tips=False).move_to([-.8, -.65, 0])
        xl = T("cell volume", 30, TEXT).next_to(ax, DOWN, buff=.18)
        yl = T("amount ÷ volume", 30, TEXT).rotate(PI/2).next_to(ax, LEFT, buff=.2)
        redc = ax.plot(lambda v: 100 / v, x_range=[25, 75], color=RED, stroke_width=7)
        orangec = ax.plot(lambda v: 2, x_range=[25, 75], color=ORANGE, stroke_width=7)
        start = DashedLine(ax.c2p(25, 1.6), ax.c2p(75, 1.6), color=GREEN, stroke_width=3)
        cell_c = np.array([4.45, 2.55, 0.0])
        cell = cell_body(cell_c, .72)
        dots = content_dots(cell_c, .72, ORANGE, 10, radius=.045)
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(cell), FadeIn(dots), run_time=.7)
        self.at("gauge stays flat")
        self.play(Create(orangec), run_time=.8)
        self.at("total amount grows")
        counter = M("total: 50 → 150", 28, ORANGE).move_to([1.55, 2.85, 0])
        grown_cell = cell_body(cell_c, .92)
        grown_dots = content_dots(cell_c, .92, ORANGE, 18, radius=.045)
        self.play(FadeIn(counter), Transform(cell, grown_cell), Transform(dots, grown_dots), run_time=.75)
        self.at("concentration does not")
        self.play(Indicate(orangec, color=ORANGE, scale_factor=1.02), run_time=.55)
        self.at("cannot be the ruler")
        labs = VGroup(T("ruler", 28, RED).move_to([4.0, -1.55, 0]),
                      T("flat: no size signal", 28, ORANGE).move_to([2.3, -.15, 0]))
        self.play(Create(redc), Create(start), FadeIn(labs), FadeIn(tag("computed", pos=(-4.85, 3.35, 0))), run_time=1.0)
        self.finish()


class S12Genome(SpokenScene):
    def construct(self):
        body = cell_body(CELL_C, 1.45); orange = content_dots(CELL_C, 1.45, ORANGE, 18); gen = genome(CELL_C)
        gg = gauge(GAUGE_C, .68, ORANGE); self.add(body, orange, gen, gg)
        newborn_w = body.width
        body.add_updater(lambda m: m.set_width(newborn_w * (1 + .035 * math.sin(self.renderer.time * 1.8))))
        self.at("fall behind")
        self.play(Indicate(gen, color=PURPLE, scale_factor=1.1), run_time=.55)
        self.at("purple block")
        gl = T("genome: one copy, held", 32, PURPLE).move_to([2.5, 3.05, 0])
        self.play(FadeIn(gl), gen.animate.set_stroke(width=6), run_time=.65)
        self.at("grow without dividing")
        cross = VGroup(divide_arrow([1.1, .1, 0]), Cross(divide_arrow([1.1, .1, 0]), stroke_color=RED, stroke_width=6))
        held = T("held: no division", 28, RED).move_to([1.25, -1.3, 0])
        self.play(FadeIn(cross), FadeIn(held), run_time=.65)
        self.at("kept one copy")
        self.play(Indicate(gen, color=PURPLE, scale_factor=1.15), run_time=.55)
        self.at("swelled many times over")
        body.clear_updaters()
        big_r = 1.45 * (600 / 65) ** (1 / 3)
        spread = content_dots(CELL_C, big_r, ORANGE, 18)
        ro = M("about 65 → 600 fL", 28, TEXT).move_to([0, -3.35, 0])
        self.play(Transform(body, cell_body(CELL_C, big_r)), Transform(orange, spread), FadeIn(ro),
                  FadeOut(cross), FadeOut(held), run_time=2.3)
        self.finish()


class S13Diluted(SpokenScene):
    def construct(self):
        r = 3.0; body = cell_body(CELL_C, r); orange = content_dots(CELL_C, r, ORANGE, 18); gen = genome(CELL_C)
        gg = gauge(GAUGE_C, .62, ORANGE); note = tag("schematic, no measured values", GREY, (4.7, -3.35, 0))
        self.add(body, orange, gen, gg, note)
        self.at("synthesis fell behind")
        self.play(Transform(body, cell_body(CELL_C, 3.25)), Transform(orange, content_dots(CELL_C, 3.25, ORANGE, 20)),
                  Transform(gg, gauge(GAUGE_C, .42, ORANGE)), run_time=1.4)
        swollen_w = body.width
        body.add_updater(lambda m: m.set_width(swollen_w * (1 + .025 * math.sin(self.renderer.time * 1.9))))
        self.at("was diluted")
        dl = T("diluted", 40, ORANGE).move_to([4.45, 2.55, 0])
        self.play(FadeIn(dl), run_time=.55)
        self.at("orange dots thinned out")
        self.play(Indicate(orange, color=ORANGE, scale_factor=1.03), run_time=.6)
        self.at("copied from the DNA")
        strands = VGroup(*[Arrow(gen.get_right() + [0, y, 0], gen.get_right() + [1.25, y + .15, 0],
                                 buff=0, color=ORANGE, stroke_width=3, tip_length=.14) for y in (-.18, 0, .18)])
        self.play(LaggedStart(*[GrowArrow(a) for a in strands], lag_ratio=.25), run_time=1.1)
        self.at("one genome copy")
        ring = Circle(.65, color=PURPLE, stroke_width=4).move_to(gen)
        limit = T("a limit?", 30, PURPLE).next_to(ring, UP, buff=.12)
        self.play(Create(ring), FadeIn(limit), run_time=.65)
        self.at("a limit")
        self.play(Indicate(ring, color=PURPLE, scale_factor=1.12), run_time=.55)
        self.finish()


class S14Hold(NarratedScene):
    def construct(self):
        body = cell_body(CELL_C, 3.05); dots = content_dots(CELL_C, 3.05, ORANGE, 20); gen = genome(CELL_C)
        self.add(body, dots, gen)
        self.play(Transform(body, cell_body(CELL_C, CELL_R)), Transform(dots, content_dots(CELL_C, CELL_R, ORANGE, 18)),
                  run_time=2.2)
        self.finish()


def inward_arrows(center=CELL_C, r=CELL_R, n=12, length=.55, color=BLUE):
    c = np.array(center, float); out = VGroup()
    for k in range(n):
        a = 2 * PI * k / n + .1; d = np.array([math.cos(a), math.sin(a), 0])
        out.add(Arrow(c + d * (r + length), c + d * (r + .08), buff=0, color=color,
                      stroke_width=4, tip_length=.16))
    return out


class S15Surface(SpokenScene):
    def construct(self):
        body = cell_body(CELL_C, CELL_R); dots = content_dots(CELL_C, CELL_R, ORANGE, 18); gen = genome(CELL_C)
        self.add(body, dots, gen)
        self.at("second is the surface")
        surf = T("surface: supply", 34, BLUE).move_to([2.8, 2.75, 0])
        self.play(body.animate.set_stroke(width=12), FadeIn(surf), run_time=.75)
        self.at("crosses its membrane")
        arrows = inward_arrows(); self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=.07), run_time=1.4)
        self.at("blue rim")
        self.play(Indicate(body, color=BLUE, scale_factor=1.02), run_time=.55)
        self.at("throughout its volume")
        demand = T("volume: demand", 34, ORANGE).move_to([2.8, -2.75, 0])
        self.play(FadeIn(demand), dots.animate.set_opacity(1), body.animate.set_fill(ORANGE, opacity=.24), run_time=.8)
        self.finish()


def sphere(center, r):
    c = np.array(center, float)
    base = Circle(r, stroke_color=BLUE, stroke_width=6, fill_color=ORANGE, fill_opacity=.22).move_to(c)
    shade = Arc(radius=r * .78, start_angle=-PI/2, angle=PI, color=BLUE, stroke_width=2).move_to(c).set_opacity(.4)
    hi = Ellipse(width=r * .85, height=r * .28, color=TEXT, stroke_width=2).move_to(c + [-.2*r, .35*r, 0]).set_opacity(.25)
    return VGroup(base, shade, hi)


def surface_marks(center, r, n, color=BLUE):
    c = np.array(center, float); out = VGroup()
    for k in range(n):
        a = 2 * PI * k / n
        p = c + [r * math.cos(a), r * math.sin(a), 0]
        q = c + [(r-.18) * math.cos(a), (r-.18) * math.sin(a), 0]
        out.add(Line(p, q, color=color, stroke_width=4))
    return out


class S16Double(SpokenScene):
    def construct(self):
        c1, c2 = np.array([-3.7, .65, 0]), np.array([1.65, .65, 0])
        small = sphere(c1, 1.0); sm = surface_marks(c1, 1.0, 12)
        self.add(small)
        self.at("Take a sphere")
        self.play(Create(sm), FadeIn(M("5 µm", 28, BLUE).next_to(small, DOWN)),
                  Indicate(small, color=BLUE, scale_factor=1.03), run_time=.7)
        self.at("simplest shape")
        case = T("sphere: simplest case", 28, YELLOW).move_to([0, 3.35, 0])
        self.play(FadeIn(case), run_time=.45)
        self.at("double its radius")
        big = sphere(c2, 2.0); bm = surface_marks(c2, 2.0, 48)
        bl = M("10 µm", 28, BLUE).next_to(big, DOWN, buff=.12)
        self.play(GrowFromCenter(big), LaggedStart(*[Create(x) for x in bm], lag_ratio=.015), FadeIn(bl), run_time=1.4)
        self.at("area rises four times")
        area = VGroup(Rectangle(width=2.3, height=.38, color=BLUE, fill_color=BLUE, fill_opacity=.55),
                      T("area × 4", 28, BLUE)).arrange(RIGHT, buff=.22).move_to([-3.0, -2.65, 0])
        self.play(GrowFromEdge(area[0], LEFT), FadeIn(area[1]), run_time=.65)
        self.at("volume 8")
        vol = VGroup(Rectangle(width=4.6, height=.38, color=ORANGE, fill_color=ORANGE, fill_opacity=.55),
                     T("volume × 8", 28, ORANGE)).arrange(RIGHT, buff=.22).move_to([1.75, -3.25, 0])
        self.play(GrowFromEdge(vol[0], LEFT), FadeIn(vol[1]), run_time=.65)
        self.at("half as much membrane")
        sectors = VGroup(*[Line(c2, c2 + 1.9*np.array([math.cos(a), math.sin(a), 0]), color=ORANGE,
                                  stroke_width=2).set_opacity(.25) for a in np.linspace(-PI/2, PI/2, 7)])
        half = T("membrane per volume: ½", 34, YELLOW).move_to([0, -2.3, 0])
        calc = M("area ÷ volume: 0.6 → 0.3 per µm", 24, YELLOW).next_to(half, DOWN, buff=.16)
        self.play(FadeOut(area), FadeOut(vol), run_time=.25)
        self.play(Create(sectors), FadeIn(half), FadeIn(calc), FadeIn(tag("computed, sphere")), run_time=.7)
        self.finish()


class S17Hold(NarratedScene):
    def construct(self):
        c1, c2 = np.array([-3.7, .4, 0]), np.array([1.65, .4, 0])
        s = sphere(c1, 1.0); b = sphere(c2, 2.0); sm = surface_marks(c1, 1, 12); bm = surface_marks(c2, 2, 48)
        half = T("membrane per volume: ½", 36, YELLOW).move_to([0, -2.75, 0])
        self.add(s, b, sm, bm, half)
        self.play(LaggedStart(*[Indicate(x, color=BLUE, scale_factor=1.05) for x in [sm, bm]], lag_ratio=.25),
                  b.animate.set_fill(ORANGE, opacity=.32), run_time=1.7, rate_func=there_and_back)
        self.finish()


def mini_gauge(x, color, level, label, extra=None):
    box = RoundedRectangle(corner_radius=.08, width=2.55, height=2.05, color=GREY, stroke_width=2).move_to([x, -1.8, 0])
    bar = Rectangle(width=.38, height=1.25*level, stroke_width=0, fill_color=color, fill_opacity=.75)
    bar.move_to(box).align_to(box, DOWN).shift(UP*.2 + LEFT*.62)
    lab = T(label, 28, color).move_to([x, -.52, 0])
    g = VGroup(box, bar, lab)
    if extra is not None: g.add(extra)
    return g


class S18Return(SpokenScene):
    def construct(self):
        body = cell_body([0, 1.65, 0], 1.2); dots = content_dots([0, 1.65, 0], 1.2, ORANGE, 12)
        self.add(body, dots)
        self.at("four jobs")
        gs = VGroup(mini_gauge(-4.8, RED, .85, "proposed ruler"),
                    mini_gauge(-1.6, ORANGE, .58, "kept steady"),
                    mini_gauge(1.6, ORANGE, .42, "genome: a cost", genome([2.05, -1.65, 0], .55)),
                    mini_gauge(4.8, BLUE, .38, "surface: a cost"))
        self.play(LaggedStart(*[FadeIn(g, shift=UP*.15) for g in gs], lag_ratio=.12), run_time=1.1)
        self.at("diluted brake")
        self.play(gs[0][1].animate.stretch(.5, 1).align_to(gs[0][0], DOWN).shift(UP*.2),
                  body.animate.scale(1.06), run_time=.7)
        self.at("may tell yeast its size")
        line = Line([-5.5, -1.75, 0], [-4.1, -1.75, 0], color=GREEN, stroke_width=4)
        self.play(Create(line), run_time=.45)
        self.at("keep pace")
        self.play(Indicate(gs[1][1], color=ORANGE, scale_factor=1.04), body.animate.scale(1.05), run_time=.6)
        self.at("stay steady")
        self.play(gs[1][1].animate.shift(UP*.05), run_time=.45, rate_func=there_and_back)
        self.at("single genome")
        self.play(Indicate(gs[2][-1], color=PURPLE, scale_factor=1.2),
                  gs[2][1].animate.stretch(.65, 1).align_to(gs[2][0], DOWN).shift(UP*.2),
                  body.animate.scale(1.04), run_time=.65)
        self.at("sphere's surface")
        self.play(gs[3][1].animate.stretch(.55, 1).align_to(gs[3][0], DOWN).shift(UP*.2),
                  body.animate.scale(1.03), run_time=.65)
        self.at("costs of being big")
        bud = Circle(.12, color=BLUE, stroke_width=5, fill_color=ORANGE, fill_opacity=.15).move_to([1.2, 1.7, 0])
        self.play(Transform(body, cell_body([-.7, 1.65, 0], 1.45)), Transform(dots, content_dots([-.7, 1.65, 0], 1.45, ORANGE, 12)),
                  bud.animate.scale(6).shift(RIGHT*.65), run_time=.9)
        self.finish()


class S19End(EndCard):
    LINE = "Growth dilutes what does not keep pace: a proposed ruler, two costs."
