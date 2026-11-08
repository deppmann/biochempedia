"""The carbon and water cycles  (grade 7 Life Science explainer)

COLOR MAP (one color per concept, whole video)
  PURPLE = carbon dioxide (and the Mauna Loa carbon dioxide sketch)
  GOLD   = carbon in living things: sugar (glucose), fat, protein; "the carbon" question
  TEAL   = water, water vapor
  GREEN  = photosynthesis, plants, living things
  ORANGE = respiration
  PINK   = decomposition and decomposers
  RED    = combustion, burning fossil fuels
  BROWN  = soil and ground
  BLUE   = ocean
  YELLOW = radiant energy
  GREY   = air box, structure, notes, volcano
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58FB4"
BROWN = "#A8825A"


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=14)


# ---------- the Mauna Loa sketch (an equation, not data) ----------
def hshape(t):
    u = t - 0.38
    return np.cos(2 * np.pi * u) + 0.35 * np.sin(4 * np.pi * u + 1.0)


T_PEAK, T_MIN = 0.405, 0.768   # fractions of a year where the sketch peaks / bottoms out


def sketch_val(t, slope):
    return slope * t + 0.9 * hshape(t % 1.0)


class Sketch:
    """Axes + curve in a screen box. years = number of years drawn; slope = climb per year."""

    def __init__(self, x0, x1, y0, y1, years, slope):
        self.x0, self.x1, self.y0, self.y1, self.years, self.slope = x0, x1, y0, y1, years, slope
        ts = np.linspace(0, years, 600)
        vs = [sketch_val(t, slope) for t in ts]
        self.vmin, self.vmax = min(vs) - 0.15, max(vs) + 0.15

    def p(self, t, val=None):
        v = sketch_val(t, self.slope) if val is None else val
        x = self.x0 + t / self.years * (self.x1 - self.x0)
        y = self.y0 + (v - self.vmin) / (self.vmax - self.vmin) * (self.y1 - self.y0)
        return np.array([x, y, 0.0])

    def axes(self):
        a = Line([self.x0, self.y0, 0], [self.x1 + 0.1, self.y0, 0], color=GREY, stroke_width=4)
        b = Line([self.x0, self.y0, 0], [self.x0, self.y1 + 0.1, 0], color=GREY, stroke_width=4)
        return VGroup(a, b)

    def curve(self, t0=0.0, t1=None, color=PURPLE, width=5):
        t1 = self.years if t1 is None else t1
        return ParametricFunction(lambda t: self.p(t), t_range=[t0, t1, 0.01], color=color, stroke_width=width)


# ---------- the oak ----------
GROUND_TOP, GROUND_BOT = -2.15, -3.1


def ground(x0=-6.2, x1=6.2):
    return Rectangle(width=x1 - x0, height=GROUND_TOP - GROUND_BOT, stroke_width=0, fill_color=BROWN,
                     fill_opacity=0.35).move_to([(x0 + x1) / 2, (GROUND_TOP + GROUND_BOT) / 2, 0])


def oak(cx=0.0):
    trunk = Rectangle(width=0.55, height=1.65, stroke_color=BROWN, stroke_width=4, fill_color=BROWN,
                      fill_opacity=0.5).move_to([cx, GROUND_TOP + 0.825, 0])
    crown = Ellipse(width=3.6, height=2.0, stroke_color=GREEN, stroke_width=4, fill_color=GREEN,
                    fill_opacity=0.28).move_to([cx, 0.3, 0])
    return trunk, crown


# ---------- the carbon boxes ----------
def cbox(label, color, cx, cy, w, h, size=26, label_dy=0.0, label_dx=0.0):
    box = RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_color=color, stroke_width=3.5,
                           fill_color=color, fill_opacity=0.10).move_to([cx, cy, 0])
    lab = T(label, size, color, weight=BOLD).move_to([cx + label_dx, cy + label_dy, 0])
    return VGroup(box, lab)


AIR_C, LIV_C, SOIL_C, OCE_C = (0, 2.65), (-4.0, -0.5), (0.2, -0.5), (-4.0, -2.85)


def air_box():
    return cbox("air", GREY, AIR_C[0], AIR_C[1], 10.4, 0.9, label_dx=-4.5)


def liv_box():
    return cbox("living things", GREEN, LIV_C[0], LIV_C[1], 4.5, 2.3, size=26, label_dy=0.75)


def soil_box():
    return cbox("soil", BROWN, SOIL_C[0], SOIL_C[1], 2.6, 1.0)


def ocean_box():
    return cbox("ocean", BLUE, OCE_C[0], OCE_C[1], 3.0, 0.8)


def fuel_chip():
    return chip("coal, oil, natural gas", RED, size=22).move_to([3.8, -2.8, 0])


PH_X, RS_X, DC_X, CB_X = -5.3, -1.95, 1.2, 4.6
AIR_BOT, LIV_TOP = 2.2, 0.65


def photo_arrow():
    return arr([PH_X, AIR_BOT, 0], [PH_X, LIV_TOP + 0.05, 0], GREEN, w=7, tip=0.25)


def resp_arrow():
    return arr([RS_X, LIV_TOP + 0.05, 0], [RS_X, AIR_BOT, 0], ORANGE, w=7, tip=0.25)


def decomp_arrow():
    return arr([DC_X, 0.05, 0], [DC_X, AIR_BOT, 0], PINK, w=7, tip=0.25)


def dead_arrow():
    return arr([-1.72, -0.5, 0], [-1.12, -0.5, 0], PINK, w=6, tip=0.2)


def comb_arrow():
    return arr([CB_X, -2.35, 0], [CB_X, AIR_BOT, 0], RED, w=9, tip=0.3)


def co2_chip(x, y, size=22):
    return chip("carbon dioxide", PURPLE, size=size).move_to([x, y, 0])


def water_chip(x, y, size=22):
    return chip("water", TEAL, size=size).move_to([x, y, 0])


def sugar_chip(x, y):
    return chip("sugar", GOLD, size=22, pad=0.14).move_to([x, y, 0])


# =============================================================================================
class S00Title(TitleCard):
    LESSON = "The carbon and water cycles"
    TITLE = "Carbon and water keep going around"


# =============================================================================================
class S01Question(SpokenScene):
    def construct(self):
        tri = Polygon([-5.0, -1.9, 0], [-1.2, -1.9, 0], [-3.1, 0.2, 0], stroke_color=GREY, stroke_width=5,
                      fill_color=GREY, fill_opacity=0.18)
        vlab = T("Mauna Loa, Hawaii", 26, TEXT).move_to([-3.1, -2.45, 0])
        dots = VGroup(*[Dot([-3.1 + dx, 0.55 + dy, 0], radius=0.07, color=PURPLE) for dx, dy in
                        [(-0.45, 0.1), (0.1, 0.3), (0.5, 0.0), (-0.1, -0.05), (0.8, 0.35), (-0.8, 0.4)]])
        air = T("air measured here", 24, PURPLE).move_to([-3.1, 1.25, 0])
        vol = VGroup(tri, vlab)
        sk = Sketch(0.9, 5.9, -2.4, 2.1, 8, 0.33)
        ax = sk.axes()
        ylab = T("carbon dioxide in the air", 22, PURPLE).rotate(PI / 2).move_to([0.4, -0.1, 0])
        xlab = T("years since 1958", 22, GREY).move_to([3.4, -2.8, 0])
        note = T("sketch of the pattern, not data", 22, GREY).move_to([3.4, 2.65, 0])
        self.at("Hawaiian volcano")
        self.play(FadeIn(vol), FadeIn(dots), FadeIn(air), run_time=0.8)
        self.at("since")
        self.play(FadeIn(ax), FadeIn(ylab), FadeIn(xlab), FadeIn(note), run_time=0.6)
        curve = sk.curve()
        self.play(Create(curve, rate_func=linear), run_time=3.2)
        yr = 3
        up = sk.curve(yr - 1 + T_MIN, yr + T_PEAK, color=WHITE, width=9)
        dn = sk.curve(yr + T_PEAK, yr + T_MIN, color=YELLOW, width=9)
        self.at("rises through winter")
        tag1 = T("winter and spring: rises", 26, WHITE, weight=BOLD).move_to([3.4, 3.1, 0])
        self.play(Create(up), FadeIn(tag1), run_time=0.7)
        self.at("falls through summer")
        tag2 = T("summer: falls", 26, YELLOW, weight=BOLD).move_to([3.4, 3.1, 0])
        self.play(ReplacementTransform(tag1, tag2), Create(dn), run_time=0.7)
        self.at("slowly climbs")
        a = sk.p(0.0, sketch_val(0.4, 0.33)); b = sk.p(8.0, sketch_val(8.4, 0.33))
        trend = DashedLine(a, b, color=TEXT, stroke_width=4, dash_length=0.18)
        tag3 = T("the whole record climbs", 26, TEXT, weight=BOLD).move_to([3.4, 3.1, 0])
        self.play(FadeOut(up), FadeOut(dn), ReplacementTransform(tag2, tag3), Create(trend), run_time=1.0)
        self.at("Why")
        why = T("Why?", 64, TEXT, weight=BOLD).move_to([-3.1, 2.55, 0])
        self.play(FadeIn(why, scale=0.7), run_time=0.5)
        gr = ground()
        trunk, crown = oak(0.0)
        self.at("In Virginia")
        self.play(*[FadeOut(m) for m in (vol, dots, air, ax, ylab, xlab, note, curve, trend, tag3, why)], run_time=0.7)
        vlab2 = T("Virginia", 28, TEXT, weight=BOLD).move_to([-5.0, 3.05, 0])
        self.play(FadeIn(gr), FadeIn(trunk), GrowFromCenter(crown), FadeIn(vlab2), run_time=0.9)
        self.at("pulls water")
        wa = arr([0.0, GROUND_TOP - 0.5, 0], [0.0, 0.1, 0], TEAL, w=9, tip=0.3)
        wl = T("water from the soil", 26, TEAL).move_to([-3.0, -1.5, 0])
        self.play(GrowArrow(wa), FadeIn(wl), run_time=1.0)
        self.at("invisible gas")
        vap = VGroup(*[arr([x, 1.45, 0], [x + 0.1, 2.3, 0], TEAL, w=5, tip=0.2) for x in (-1.0, 0.0, 1.0)])
        vl = T("water vapor: an invisible gas", 26, TEAL).move_to([2.9, 2.75, 0])
        self.play(LaggedStart(*[GrowArrow(v) for v in vap], lag_ratio=0.25), FadeIn(vl), run_time=1.2)
        self.at("go next")
        cq = chip("carbon: where next?", GOLD, size=26).move_to([-4.5, 0.6, 0])
        wq = chip("water: where next?", TEAL, size=26).move_to([4.4, 0.2, 0])
        self.play(FadeIn(cq, shift=UP * 0.1), FadeIn(wq, shift=UP * 0.1), run_time=0.7)
        self.play(Indicate(cq, color=GOLD, scale_factor=1.06), Indicate(wq, color=TEAL, scale_factor=1.06), run_time=0.8)
        self.finish()


# =============================================================================================
class S02Carbon(SpokenScene):
    def construct(self):
        liv = liv_box()
        self.at("Carbon is in")
        self.play(FadeIn(liv), run_time=0.8)
        self.at("sugar")
        chips = VGroup(chip("sugar", GOLD, size=22, pad=0.14), chip("fat", GOLD, size=22, pad=0.14),
                       chip("protein", GOLD, size=22, pad=0.14)).arrange(RIGHT, buff=0.2).move_to([LIV_C[0], -0.75, 0])
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in chips], lag_ratio=0.4), run_time=1.4)
        cl = T("carbon in every living thing", 22, GOLD).move_to([LIV_C[0], -1.28, 0])
        self.play(FadeIn(cl), run_time=0.5)
        air, soil, ocean = air_box(), soil_box(), ocean_box()
        self.at("among air")
        self.play(FadeIn(air), run_time=0.6)
        self.at("living things")
        self.play(Indicate(liv, color=GREEN, scale_factor=1.03), run_time=0.6)
        self.at("ocean")
        self.play(FadeIn(ocean), run_time=0.5)
        self.at("soil")
        self.play(FadeIn(soil), run_time=0.5)
        self.at("Photosynthesis takes")
        pa = photo_arrow()
        pl = T("photosynthesis", 24, GREEN, weight=BOLD).move_to([-3.5, 1.6, 0])
        co2 = co2_chip(-0.8, 2.65)
        self.play(FadeIn(co2, scale=0.8), run_time=0.5)
        self.play(GrowArrow(pa), FadeIn(pl), Indicate(co2, color=PURPLE, scale_factor=1.1), run_time=0.9)
        self.at("out of the air")
        self.play(Indicate(air, color=GREY, scale_factor=1.02), run_time=0.7)
        self.at("radiant energy")
        re = T("+ radiant energy", 22, YELLOW).move_to([-3.5, 1.2, 0])
        self.play(FadeIn(re), run_time=0.5)
        self.at("to make sugar")
        self.play(Indicate(chips[0], color=GOLD, scale_factor=1.2), run_time=0.8)
        self.at("called glucose")
        gl = T("sugar (glucose)", 22, GOLD).move_to([LIV_C[0], -1.28, 0])
        self.play(ReplacementTransform(cl, gl), run_time=0.6)
        self.at("carbon dioxide and water")
        e1 = T("carbon dioxide", 26, PURPLE); e2 = T("+ water", 26, TEAL); e3 = T("→ sugar (glucose)", 26, GOLD)
        eq = VGroup(e1, e2, e3).arrange(RIGHT, buff=0.3).move_to([2.3, -1.95, 0])
        self.play(LaggedStart(FadeIn(e1), FadeIn(e2), FadeIn(e3), lag_ratio=0.5), run_time=1.6)
        self.finish()




# =============================================================================================
def carbon_state():
    """Scene-2 end state (boxes + photosynthesis) for scene 3."""
    air, liv, soil, ocean = air_box(), liv_box(), soil_box(), ocean_box()
    pa = photo_arrow()
    pl = T("photosynthesis", 24, GREEN, weight=BOLD).move_to([-3.5, 1.6, 0])
    co2 = co2_chip(-0.8, 2.65)
    sug = sugar_chip(-3.2, -0.75)
    gl = T("sugar (glucose)", 22, GOLD).move_to([LIV_C[0], -1.28, 0])
    return air, liv, soil, ocean, pa, pl, co2, sug, gl


class S03Return(SpokenScene):
    def construct(self):
        air, liv, soil, ocean, pa, pl, co2, sug, gl = carbon_state()
        fat = chip("fat", GOLD, size=22, pad=0.14); prot = chip("protein", GOLD, size=22, pad=0.14)
        row = VGroup(sug, fat, prot).arrange(RIGHT, buff=0.2).move_to([LIV_C[0], -0.75, 0])
        self.add(air, liv, soil, ocean, pa, pl, co2, row, gl)
        self.at("Three processes")
        self.play(pa.animate.set_opacity(0.3), pl.animate.set_opacity(0.3), FadeOut(fat), FadeOut(prot),
                  FadeOut(gl), sug.animate.move_to([-3.1, -0.6, 0]), run_time=0.9)
        # respiration
        self.at("Respiration is")
        ra = resp_arrow()
        rl = T("respiration", 24, ORANGE, weight=BOLD).move_to([-0.55, 1.6, 0])
        self.play(GrowArrow(ra), FadeIn(rl), run_time=0.7)
        self.at("breaking down sugar")
        self.play(Indicate(sug, color=GOLD, scale_factor=1.2), run_time=0.8)
        self.at("releasing carbon dioxide")
        c2 = co2_chip(-1.0, 2.65)
        c1 = co2_chip(-4.0, 0.2).scale(0.001)
        self.play(Indicate(co2, color=PURPLE, scale_factor=1.12), run_time=0.7)
        self.at("and water")
        w = water_chip(1.9, 2.65)
        self.play(FadeIn(w, shift=UP * 0.2), run_time=0.6)
        self.at("Plants, animals")
        names = VGroup(T("plants", 24, GREEN), T("animals", 24, GREEN), T("decomposers", 24, GREEN)) \
            .arrange(DOWN, buff=0.12, aligned_edge=LEFT).move_to([-5.0, -0.7, 0])
        self.play(LaggedStart(*[FadeIn(n) for n in names], lag_ratio=0.45), run_time=1.3)
        self.at("day and night")
        dn = T("day and night", 24, ORANGE).move_to([-0.55, 1.15, 0])
        self.play(FadeIn(dn), run_time=0.5)
        # decomposition
        self.at("Decomposition is")
        self.play(pa.animate.set_opacity(0.0), pl.animate.set_opacity(0.0), ra.animate.set_opacity(0.4),
                  rl.animate.set_opacity(0.4), dn.animate.set_opacity(0.4), run_time=0.5)
        da = decomp_arrow()
        dl = T("decomposition", 24, PINK, weight=BOLD).move_to([3.0, 1.4, 0])
        self.play(GrowArrow(da), FadeIn(dl), run_time=0.7)
        self.at("bacteria and fungi")
        bf = T("bacteria and fungi", 22, PINK).move_to([2.95, 0.98, 0])
        self.play(FadeIn(bf), run_time=0.6)
        self.at("dead organisms")
        dd = dead_arrow()
        dlab = T("dead organisms", 22, PINK).move_to([0.2, -1.45, 0])
        self.play(GrowArrow(dd), FadeIn(dlab), run_time=0.7)
        self.at("air and soil")
        self.play(Indicate(air, color=GREY, scale_factor=1.02), Indicate(soil, color=BROWN, scale_factor=1.05), run_time=0.9)
        # combustion
        self.at("Combustion is burning")
        self.play(da.animate.set_opacity(0.4), dl.animate.set_opacity(0.4), bf.animate.set_opacity(0.4),
                  dd.animate.set_opacity(0.4), dlab.animate.set_opacity(0.4), run_time=0.4)
        fuel = fuel_chip()
        ca = comb_arrow()
        cl = T("combustion", 24, RED, weight=BOLD).move_to([3.3, -0.6, 0])
        self.play(FadeIn(fuel, shift=UP * 0.1), GrowArrow(ca), FadeIn(cl), run_time=0.9)
        self.at("coal, oil")
        self.play(Indicate(fuel, color=RED, scale_factor=1.06), run_time=0.7)
        self.at("releases carbon dioxide quickly")
        c3 = co2_chip(3.9, 2.65)
        self.play(FadeIn(c3, shift=UP * 0.2), Indicate(ca, color=RED, scale_factor=1.1), run_time=0.9)
        self.finish()


# =============================================================================================
def water_scene_base():
    gr = ground()
    trunk, crown = oak(0.0)
    return gr, trunk, crown


def cloud(cx, cy):
    parts = [Ellipse(width=2.4, height=0.9).move_to([cx, cy, 0]),
             Circle(radius=0.55).move_to([cx - 0.5, cy + 0.3, 0]),
             Circle(radius=0.7).move_to([cx + 0.35, cy + 0.35, 0])]
    g = Union(*parts)
    g.set_stroke(color=GREY, width=3).set_fill(color=GREY, opacity=0.25)
    return g


class S04Water(SpokenScene):
    def construct(self):
        gr, trunk, crown = water_scene_base()
        pond = Ellipse(width=2.8, height=0.55, stroke_color=TEAL, stroke_width=3, fill_color=TEAL,
                       fill_opacity=0.5).move_to([-4.5, GROUND_TOP, 0])
        stream = Rectangle(width=1.5, height=0.3, stroke_width=0, fill_color=TEAL, fill_opacity=0.5).move_to([5.45, GROUND_TOP - 0.1, 0])
        cl = cloud(2.6, 2.6)
        self.at("Water has")
        self.play(FadeIn(gr), FadeIn(trunk), FadeIn(crown), FadeIn(pond), FadeIn(stream), run_time=0.9)
        self.at("Evaporation is")
        ea = VGroup(*[arr([x, GROUND_TOP + 0.35, 0], [x + 0.1, 0.05, 0], TEAL, w=5, tip=0.2) for x in (-5.0, -4.5, -4.0)])
        el = T("evaporation", 24, TEAL, weight=BOLD).move_to([-4.5, 0.5, 0])
        self.play(LaggedStart(*[GrowArrow(a) for a in ea], lag_ratio=0.25), FadeIn(el), run_time=1.0)
        self.at("water vapor")
        vl = T("water vapor: a gas", 22, TEAL).move_to([-4.5, 0.9, 0])
        self.play(FadeIn(vl), run_time=0.5)
        self.at("Condensation is")
        ca = arr([-3.6, 2.0, 0], [1.2, 2.6, 0], TEAL, w=5, tip=0.2)
        cn = T("condensation", 24, TEAL, weight=BOLD).move_to([-3.9, 2.85, 0])
        self.play(GrowArrow(ca), FadeIn(cn), run_time=0.8)
        self.play(FadeIn(cl), run_time=0.5)
        self.at("form clouds")
        self.play(Indicate(cl, color=GREY, scale_factor=1.08), run_time=0.7)
        self.at("Precipitation is")
        rain = VGroup(*[Line([x, 1.9 - k * 0.1, 0], [x - 0.12, 1.45 - k * 0.1, 0], color=TEAL, stroke_width=5)
                        for k, x in enumerate((2.1, 2.5, 2.9, 3.3))])
        pa = arr([3.0, 1.2, 0], [3.0, GROUND_TOP + 0.1, 0], TEAL, w=5, tip=0.2)
        pl = T("precipitation", 24, TEAL, weight=BOLD).move_to([4.6, 0.3, 0])
        self.play(GrowArrow(pa), FadeIn(rain), FadeIn(pl), run_time=1.0)
        self.at("rain or snow")
        self.play(Indicate(pl, color=TEAL, scale_factor=1.06), run_time=0.6)
        self.at("Infiltration is")
        ia = arr([1.4, GROUND_TOP - 0.1, 0], [1.4, GROUND_BOT + 0.15, 0], TEAL, w=5, tip=0.2)
        il = T("infiltration", 24, TEAL, weight=BOLD).move_to([-0.1, -2.62, 0])
        self.play(GrowArrow(ia), FadeIn(il), run_time=0.9)
        self.at("Runoff is")
        ra = arr([3.9, GROUND_TOP + 0.15, 0], [5.4, GROUND_TOP + 0.15, 0], TEAL, w=5, tip=0.2)
        rl = T("runoff", 24, TEAL, weight=BOLD).move_to([4.7, GROUND_TOP + 0.6, 0])
        self.play(GrowArrow(ra), FadeIn(rl), run_time=0.9)
        self.at("into streams")
        sl = T("stream", 22, TEAL).move_to([5.45, GROUND_TOP - 0.6, 0])
        self.play(FadeIn(sl), run_time=0.5)
        self.at("Transpiration is")
        tv = VGroup(*[arr([x, 1.4, 0], [x + 0.05, 2.05, 0], TEAL, w=5, tip=0.2) for x in (-0.5, 0.0, 0.5)])
        tl = T("transpiration", 24, TEAL, weight=BOLD).move_to([-1.95, 1.75, 0])
        self.play(LaggedStart(*[GrowArrow(a) for a in tv], lag_ratio=0.25), FadeIn(tl), run_time=1.0)
        self.at("from their leaves")
        self.play(Indicate(crown, color=GREEN, scale_factor=1.04), run_time=0.8)
        self.finish()


# =============================================================================================
class S05Meet(SpokenScene):
    def construct(self):
        top_y, left, right = 0.8, -3.4, 3.4
        pts = [[-0.45, top_y, 0], [left, top_y, 0], [left, -2.4, 0], [right, -2.4, 0], [right, top_y, 0], [0.45, top_y, 0]]
        outline = VMobject(stroke_color=GREEN, stroke_width=5)
        outline.set_points_as_corners(pts)
        fill = Rectangle(width=right - left, height=top_y + 2.4, stroke_width=0, fill_color=GREEN,
                         fill_opacity=0.12).move_to([0, (top_y - 2.4) / 2, 0])
        lname = T("inside a leaf", 24, GREEN).move_to([0, -2.0, 0])
        leaf = VGroup(fill, outline, lname)
        self.at("meet inside")
        self.play(FadeIn(leaf), run_time=0.9)
        self.at("Photosynthesis uses")
        ph = chip("photosynthesis", GREEN, size=26).move_to([0, -0.8, 0])
        self.play(FadeIn(ph, scale=0.9), run_time=0.6)
        wc = chip("water cycle", TEAL, size=22).move_to([-5.3, -1.2, 0])
        wa = arr([-4.2, -1.2, 0], [left + 0.15, -1.2, 0], TEAL, w=8, tip=0.25)
        self.play(FadeIn(wc), GrowArrow(wa), run_time=0.8)
        self.at("and carbon dioxide")
        cc = chip("carbon cycle", PURPLE, size=22).move_to([0, 3.0, 0])
        ca = arr([0, 2.55, 0], [0, 0.0, 0], PURPLE, w=8, tip=0.25)
        cl = T("carbon dioxide", 24, PURPLE).move_to([-1.9, 1.75, 0])
        self.play(FadeIn(cc), GrowArrow(ca), FadeIn(cl), run_time=0.9)
        self.at("together")
        self.play(Indicate(ph, color=GREEN, scale_factor=1.1), run_time=0.8)
        # dry summer
        self.at("In a dry summer")
        dry = chip("dry summer", RED, size=24).move_to([4.7, 2.9, 0])
        wa_thin = arr([-4.2, -1.2, 0], [left + 0.15, -1.2, 0], TEAL, w=3, tip=0.15)
        self.play(FadeIn(dry, shift=DOWN * 0.1), Transform(wa, wa_thin), run_time=0.8)
        self.at("close the tiny openings")
        tl = T("tiny opening", 22, GREY).move_to([3.4, 1.55, 0])
        tp = arr([2.7, 1.4, 0], [0.6, top_y + 0.08, 0], GREY, w=3, tip=0.15)
        self.play(FadeIn(tl), GrowArrow(tp), run_time=0.6)
        b1 = Line([-0.45, top_y, 0], [-0.45, top_y, 0], color=GREEN, stroke_width=9)
        b2 = Line([0.45, top_y, 0], [0.45, top_y, 0], color=GREEN, stroke_width=9)
        self.add(b1, b2)
        self.play(b1.animate.put_start_and_end_on([-0.45, top_y, 0], [0.0, top_y, 0]),
                  b2.animate.put_start_and_end_on([0.45, top_y, 0], [0.0, top_y, 0]), run_time=1.2)
        self.at("saves water")
        sv = T("saves water", 24, TEAL).move_to([-5.0, -2.0, 0])
        self.play(FadeIn(sv), run_time=0.5)
        self.at("less carbon dioxide gets in")
        ca_small = arr([0, 2.55, 0], [0, 1.2, 0], PURPLE, w=3, tip=0.15)
        cl2 = T("less carbon dioxide in", 24, PURPLE).move_to([-2.2, 1.75, 0])
        self.play(Transform(ca, ca_small), ReplacementTransform(cl, cl2), run_time=1.0)
        self.at("A change in one cycle")
        both = T("change one cycle, the other can change", 28, TEXT, weight=BOLD).move_to([0, -3.1, 0])
        self.play(FadeIn(both), run_time=0.8)
        self.play(Indicate(wc, color=TEAL, scale_factor=1.1), Indicate(cc, color=PURPLE, scale_factor=1.1), run_time=0.9)
        self.finish()


# =============================================================================================
class S06Answer(SpokenScene):
    def construct(self):
        ecx, ecy, er = 0.0, 0.0, 2.7
        circ = Circle(radius=er, stroke_color=GREY, stroke_width=5, fill_color=GREY, fill_opacity=0.06).move_to([ecx, ecy, 0])
        eq = Line([ecx - er, ecy, 0], [ecx + er, ecy, 0], color=GREY, stroke_width=3)
        earth = VGroup(circ, eq)

        def en(dx, dy):
            return np.array([ecx + dx, ecy + dy, 0])
        nh = T("Northern Hemisphere", 24, TEXT, weight=BOLD).move_to(en(0, 1.9))
        dots = VGroup(*[Dot(en(dx, 1.35), radius=0.13, color=GREEN) for dx in (-1.2, -0.6, 0.0, 0.6, 1.2)])
        sdot = Dot(en(0.4, -1.2), radius=0.13, color=GREEN)
        pl = T("most land plants", 22, GREEN).move_to(en(0, 0.9))
        ml_dot = Dot(en(-1.0, 0.4), radius=0.14, color=PURPLE)
        ml_lab = T("Mauna Loa", 24, PURPLE, weight=BOLD).move_to(en(-1.0, -0.55))
        ml_line = Line(en(-1.0, -0.3), en(-1.0, 0.33), color=PURPLE, stroke_width=3)
        self.at("Back to the volcano")
        self.play(Create(circ), Create(eq), run_time=0.9)
        self.play(FadeIn(ml_dot), FadeIn(ml_lab), Create(ml_line), run_time=0.6)
        self.at("Most land plants")
        self.play(FadeIn(nh), run_time=0.5)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in list(dots) + [sdot]], lag_ratio=0.2), FadeIn(pl), run_time=1.0)
        # spring
        self.at("northern spring")
        spring = T("spring: leaves grow, photosynthesis speeds up", 26, GREEN, weight=BOLD).move_to([0, 3.35, 0])
        self.play(FadeIn(spring), *[d.animate.scale(1.7) for d in dots], run_time=1.0)
        # fall
        self.at("Each fall")
        fall = T("fall: photosynthesis slows, many leaves drop,\nbut respiration and decomposition keep going", 26, ORANGE, weight=BOLD,
                 line_spacing=0.8).move_to([0, -3.3, 0])
        self.play(FadeOut(spring), FadeIn(fall), *[d.animate.scale(1 / 1.7).set_color(BROWN) for d in dots], run_time=1.0)
        # mixes
        self.at("mixes")
        mix = VGroup(*[arr(en(4.0, y), en(-0.82, 0.4 + (y - 0.4) * 0.2), PURPLE, w=3, tip=0.15) for y in (1.0, 0.5, 0.0)])
        mixl = T("air mixes with air\nfrom across the north", 22, PURPLE, line_spacing=0.8).move_to(en(4.3, 1.6))
        self.play(FadeOut(fall), LaggedStart(*[GrowArrow(a) for a in mix], lag_ratio=0.2), FadeIn(mixl), run_time=1.2)
        # panel
        self.at("from across")
        eg = VGroup(earth, nh, dots, sdot, pl, ml_dot, ml_lab, ml_line)
        self.play(FadeOut(mixl), FadeOut(mix), eg.animate.scale(0.8).move_to([-3.7, 0.0, 0]), run_time=0.9)
        self.at("So carbon dioxide")
        sk = Sketch(1.2, 5.9, -2.2, 2.0, 1, 0.0)
        # one-year panel: make the value range symmetric
        ax = sk.axes()
        months = VGroup(*[T(m, 22, GREY).move_to([sk.p(i / 12 + 1 / 24)[0], -2.6, 0]) for i, m in enumerate("JFMAMJJASOND")])
        ttl = T("one year (sketch, not data)", 22, GREY).move_to([3.7, 2.55, 0])
        yl = T("carbon dioxide", 22, PURPLE).rotate(PI / 2).move_to([0.75, 0, 0])
        cv = sk.curve()
        self.play(FadeIn(ax), FadeIn(months), FadeIn(ttl), FadeIn(yl), Create(cv, rate_func=linear), run_time=0.9)
        self.at("falls each northern summer")
        dn = sk.curve(T_PEAK, T_MIN, color=YELLOW, width=9)
        dl = T("summer: falls", 26, YELLOW, weight=BOLD).move_to([4.95, 1.5, 0])
        self.play(Create(dn), FadeIn(dl), run_time=0.8)
        self.at("rises each winter")
        up1 = sk.curve(T_MIN, 1.0, color=WHITE, width=9)
        up2 = sk.curve(0.0, T_PEAK, color=WHITE, width=9)
        ul = T("winter: rises", 26, WHITE, weight=BOLD).move_to([3.7, -3.1, 0])
        self.play(Create(up1), Create(up2), FadeIn(ul), run_time=0.8)
        # climbing record
        self.at("Underneath")
        sk2 = Sketch(1.2, 5.9, -2.2, 2.0, 8, 0.33)
        ax2 = sk2.axes()
        cv2 = sk2.curve()
        a = sk2.p(0.0, sketch_val(0.4, 0.33)); b = sk2.p(8.0, sketch_val(8.4, 0.33))
        trend = DashedLine(a, b, color=TEXT, stroke_width=4, dash_length=0.18)
        ttl2 = T("many years (sketch, not data)", 22, GREY).move_to([3.7, 2.55, 0])
        self.play(*[FadeOut(m) for m in (ax, months, ttl, cv, dn, up1, up2, dl, ul)], FadeIn(ax2), FadeIn(ttl2), run_time=0.4)
        self.play(Create(cv2, rate_func=linear), Create(trend), run_time=0.9)
        self.at("the record climbs")
        tag = T("the record climbs", 26, TEXT, weight=BOLD).move_to([3.7, 3.05, 0])
        self.play(FadeIn(tag), run_time=0.5)
        self.at("burning fossil fuels")
        fl = chip("burning fossil fuels", RED, size=26).move_to([3.7, -3.05, 0])
        self.play(FadeIn(fl, shift=UP * 0.1), run_time=0.7)
        self.finish()


# =============================================================================================
class S07End(EndCard):
    LINE = "A change in one cycle changes the other."
