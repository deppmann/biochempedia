"""Partners in energy: photosynthesis and respiration  (grade 7 Life Science explainer)

COLOR MAP (one color per concept, whole video)
  BLUE   = oxygen (the gas, the bars, the tub's water level)
  TEAL   = water
  PURPLE = carbon dioxide
  GOLD   = sugar (glucose) and the chemical energy in it
  GREEN  = photosynthesis / chloroplast / plants
  ORANGE = cellular respiration / mitochondria / energy the cell can use
  YELLOW = light (radiant energy) and daylight
  RED    = heat
  GREY   = cell outline, sensor, structure, notes
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"

CHL = np.array([-3.5, -0.1, 0.0])   # chloroplast centre
MIT = np.array([3.5, -0.1, 0.0])    # mitochondrion centre
CH_W, CH_H, MI_W, MI_H = 3.0, 1.9, 3.0, 1.7
TOPY, BOTY = 1.8, -2.2              # lanes for the matter chips


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=14)


def ell_y(c, w, h, x, up=True):
    """y on the ellipse outline at x (up=True: top edge)."""
    t = (x - c[0]) / (w / 2)
    t = max(-0.999, min(0.999, t))
    d = (h / 2) * np.sqrt(1 - t * t)
    return c[1] + d if up else c[1] - d


def cell_outline():
    box = RoundedRectangle(corner_radius=0.5, width=12.0, height=6.0, stroke_color=GREY, stroke_width=4,
                           fill_color=GREY, fill_opacity=0.05).move_to([0, -0.3, 0])
    lab = T("green leaf cell", 24, GREY).move_to([3.9, 3.15, 0])
    return VGroup(box, lab)


def chloroplast():
    shape = Ellipse(width=CH_W, height=CH_H, stroke_color=GREEN, stroke_width=4, fill_color=GREEN,
                    fill_opacity=0.22).move_to(CHL)
    name = T("chloroplast", 26, GREEN).move_to(CHL + UP * 0.12)
    sub = T("photosynthesis", 22, GREEN).move_to(CHL + DOWN * 0.38)
    return shape, name, sub


def mitochondrion():
    shape = Ellipse(width=MI_W, height=MI_H, stroke_color=ORANGE, stroke_width=4, fill_color=ORANGE,
                    fill_opacity=0.22).move_to(MIT)
    name = T("mitochondria", 26, ORANGE).move_to(MIT + UP * 0.12)
    sub = T("respiration", 22, ORANGE).move_to(MIT + DOWN * 0.38)
    return shape, name, sub


def c_sugar(x=-3.2, y=TOPY):
    return chip("sugar (glucose)", GOLD, size=22).move_to([x, y, 0])


def c_oxy(x=-0.7, y=TOPY):
    return chip("oxygen", BLUE, size=22).move_to([x, y, 0])


def c_co2(x=-4.5, y=BOTY):
    return chip("carbon dioxide", PURPLE, size=22).move_to([x, y, 0])


def c_h2o(x=-2.5, y=BOTY):
    return chip("water", TEAL, size=22).move_to([x, y, 0])


# chips sit by their right/left edges so the pair never touches
def photo_inputs():
    co2 = c_co2(); h2o = c_h2o()
    co2.move_to([-3.1 - co2.width / 2, BOTY, 0])
    h2o.move_to([-2.85 + h2o.width / 2, BOTY, 0])
    return co2, h2o


def photo_in_arrows(co2, h2o):
    x1 = co2.get_center()[0] + 0.5
    x2 = h2o.get_center()[0]
    a1 = arr([x1, co2.get_top()[1] + 0.03, 0], [x1, ell_y(CHL, CH_W, CH_H, x1, False) - 0.03, 0], PURPLE)
    a2 = arr([x2, h2o.get_top()[1] + 0.03, 0], [x2, ell_y(CHL, CH_W, CH_H, x2, False) - 0.03, 0], TEAL)
    return a1, a2


def photo_out_arrows(sug, oxy):
    x1 = sug.get_center()[0]
    x2 = oxy.get_center()[0] - 0.25
    a1 = arr([x1, ell_y(CHL, CH_W, CH_H, x1) + 0.03, 0], [x1, sug.get_bottom()[1] - 0.03, 0], GOLD)
    a2 = arr([-2.45, ell_y(CHL, CH_W, CH_H, -2.45) + 0.03, 0], [x2, oxy.get_bottom()[1] - 0.03, 0], BLUE)
    return a1, a2


def mit_top_chips():
    sug = c_sugar(2.5); oxy = c_oxy(4.9)
    return sug, oxy


def mit_in_arrows(sug, oxy):
    x1 = sug.get_center()[0] + 0.4
    x2 = oxy.get_center()[0] - 0.3
    a1 = arr([x1, sug.get_bottom()[1] - 0.03, 0], [x1, ell_y(MIT, MI_W, MI_H, x1) + 0.03, 0], GOLD)
    a2 = arr([x2, oxy.get_bottom()[1] - 0.03, 0], [x2, ell_y(MIT, MI_W, MI_H, x2) + 0.03, 0], BLUE)
    return a1, a2


def mit_bottom_chips():
    co2 = c_co2(); h2o = c_h2o()
    co2.move_to([1.0 + co2.width / 2, BOTY, 0])
    h2o.move_to([3.95 + h2o.width / 2, BOTY, 0])
    return co2, h2o


def mit_out_arrows(co2, h2o):
    x1 = co2.get_center()[0] + 0.5
    x2 = h2o.get_center()[0]
    a1 = arr([x1, ell_y(MIT, MI_W, MI_H, x1, False) - 0.03, 0], [x1, co2.get_top()[1] + 0.03, 0], PURPLE)
    a2 = arr([x2, ell_y(MIT, MI_W, MI_H, x2, False) - 0.03, 0], [x2, h2o.get_top()[1] + 0.03, 0], TEAL)
    return a1, a2


def light_arrow():
    return arr([-5.9, 2.85, 0], [-4.5, 0.62, 0], YELLOW, w=7, tip=0.25)


def tag(text, color, near, below=False):
    t = T(text, 22, color, weight=BOLD)
    t.next_to(near, DOWN if below else UP, buff=0.1)
    return t


def energy_label():
    return T("energy the\ncell can use", 24, ORANGE, line_spacing=0.8).move_to([0, -0.1, 0])


def heat_group():
    a = arr([5.05, -0.1, 0], [6.15, -0.1, 0], RED, w=6)
    l = T("heat", 24, RED).move_to([5.6, 0.45, 0])
    return a, l


# =============================================================================================
class S00Title(TitleCard):
    LESSON = "Photosynthesis and respiration"
    TITLE = "Two processes that need each other"


# =============================================================================================
class S01Creek(SpokenScene):
    def construct(self):
        # creek: water, surface, ground, sensor
        water = Rectangle(width=5.4, height=2.0, stroke_width=0, fill_color=TEAL, fill_opacity=0.28).move_to([-3.5, -0.85, 0])
        surf = FunctionGraph(lambda x: 0.07 * np.sin(3.2 * x), x_range=[-6.2, -0.8], color=TEAL, stroke_width=4).shift(UP * 0.15)
        ground = Line([-6.2, -1.85, 0], [-0.8, -1.85, 0], color=GREY, stroke_width=5)
        wlab = T("creek water", 24, TEAL).move_to([-5.0, -1.4, 0])
        creek = VGroup(water, surf, ground, wlab)
        stake = Line([-3.0, 1.4, 0], [-3.0, -0.95, 0], color=TEXT, stroke_width=6)
        body = RoundedRectangle(corner_radius=0.1, width=0.5, height=0.8, stroke_color=TEXT, stroke_width=4,
                                fill_color=TEXT, fill_opacity=0.25).move_to([-3.0, -1.0, 0])
        slab = T("sensor", 28, TEXT).move_to([-3.0, 1.8, 0])
        sensor = VGroup(stake, body)
        self.play(FadeIn(creek), run_time=0.8)
        self.at("sensor sits")
        self.play(Create(stake), FadeIn(body), FadeIn(slab, shift=DOWN * 0.1), run_time=0.8)
        self.at("checks the oxygen")
        every = T("every 15 minutes", 26, TEXT).move_to([-3.5, -2.35, 0])
        self.play(FadeIn(every), run_time=0.4)
        for _ in range(2):
            ring = Circle(radius=0.3, stroke_color=BLUE, stroke_width=4).move_to(body)
            self.play(ring.animate.scale(3.2).set_stroke(opacity=0), run_time=0.9)
            self.remove(ring)
        # bars
        base = Line([1.0, -1.85, 0], [6.0, -1.85, 0], color=GREY, stroke_width=5)
        ttl = T("oxygen in the water", 26, BLUE).move_to([3.6, 2.4, 0])
        note = T("sketch, not to scale", 22, GREY).move_to([3.6, -3.05, 0])
        self.at("far more oxygen")
        b1 = Rectangle(width=1.3, height=3.4, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.45)
        b1.move_to([2.4, -1.85 + 1.7, 0])
        l1 = T("6 p.m.", 26, TEXT).move_to([2.4, -2.3, 0])
        self.play(FadeIn(base), FadeIn(ttl), FadeIn(note), run_time=0.4)
        self.play(GrowFromEdge(b1, DOWN), FadeIn(l1), run_time=0.9)
        self.at("early morning")
        b2 = Rectangle(width=1.3, height=1.2, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.45)
        b2.move_to([4.7, -1.85 + 0.6, 0])
        l2 = T("early morning", 26, TEXT).move_to([4.7, -2.3, 0])
        self.play(GrowFromEdge(b2, DOWN), FadeIn(l2), run_time=0.7)
        self.at("go up and down")
        q = T("?", 80, TEXT, weight=BOLD).move_to([3.55, 0.55, 0])
        self.play(FadeIn(q, scale=0.6), Indicate(b1, color=BLUE, scale_factor=1.06), run_time=0.6)
        self.play(Indicate(b2, color=BLUE, scale_factor=1.12), run_time=0.6)
        # the plant question
        self.at("plants make their own food")
        c1 = chip("plants make their own food", GREEN, size=24).move_to([-3.4, 0.9, 0])
        self.play(FadeOut(creek), FadeOut(sensor), FadeOut(slab), FadeOut(every), FadeIn(c1, shift=UP * 0.1), run_time=0.8)
        self.at("use oxygen too")
        c2 = chip("why do they use oxygen too?", BLUE, size=24).move_to([-3.4, -0.6, 0])
        self.play(FadeIn(c2, shift=UP * 0.1), run_time=0.6)
        self.play(Indicate(c2, color=BLUE, scale_factor=1.06), run_time=0.8)
        self.finish()


# =============================================================================================
class S02Photo(SpokenScene):
    def construct(self):
        cell = cell_outline()
        sh, nm, sub = chloroplast()
        self.play(Create(cell[0]), FadeIn(cell[1]), run_time=0.9)
        self.at("chloroplast, a green part")
        self.play(GrowFromCenter(sh), FadeIn(nm), run_time=0.8)
        self.at("takes in light")
        la = light_arrow()
        lab = T("light", 24, YELLOW).move_to([-5.0, 3.25, 0])
        self.play(GrowArrow(la), FadeIn(lab), run_time=0.7)
        self.at("photosynthesis happens")
        self.play(FadeIn(sub, shift=UP * 0.05), run_time=0.5)
        self.at("radiant energy")
        lab2 = T("radiant energy", 24, YELLOW).move_to([-4.8, 3.25, 0])
        self.play(ReplacementTransform(lab, lab2), run_time=0.5)
        self.at("It makes sugar")
        co2, h2o = photo_inputs()
        sug = c_sugar(); oxy = c_oxy()
        ai1, ai2 = photo_in_arrows(co2, h2o)
        ao1, ao2 = photo_out_arrows(sug, oxy)
        self.play(Indicate(VGroup(sh, nm, sub), color=GREEN, scale_factor=1.04), run_time=0.8)
        self.at("go in")
        self.play(FadeIn(co2, shift=UP * 0.2), FadeIn(h2o, shift=UP * 0.2), GrowArrow(ai1), GrowArrow(ai2), run_time=0.9)
        self.at("come out")
        self.play(GrowArrow(ao1), GrowArrow(ao2), FadeIn(sug, shift=UP * 0.2), FadeIn(oxy, shift=UP * 0.2), run_time=0.9)
        self.finish()


# =============================================================================================
class S03Resp(SpokenScene):
    def construct(self):
        cell = cell_outline()
        sh, nm, sub = chloroplast()
        la = light_arrow()
        lab = T("radiant energy", 24, YELLOW).move_to([-4.8, 3.25, 0])
        co2, h2o = photo_inputs(); sug = c_sugar(); oxy = c_oxy()
        ai1, ai2 = photo_in_arrows(co2, h2o); ao1, ao2 = photo_out_arrows(sug, oxy)
        self.add(cell, sh, nm, sub, la, lab, co2, h2o, ai1, ai2, sug, oxy, ao1, ao2)
        # inputs have been taken in
        self.play(FadeOut(co2), FadeOut(h2o), FadeOut(ai1), FadeOut(ai2), run_time=0.5)
        msh, mnm, msub = mitochondrion()
        self.at("same cell also has")
        self.play(GrowFromCenter(msh), FadeIn(mnm), run_time=0.8)
        self.at("found in almost all")
        note = T("almost all plant and animal cells", 22, GREY).move_to([3.5, -1.35, 0])
        self.play(FadeIn(note), run_time=0.5)
        self.at("cellular respiration happens")
        self.play(FadeOut(note), FadeIn(msub, shift=UP * 0.05), run_time=0.6)
        self.at("joins sugar with oxygen")
        s2, o2 = mit_top_chips()
        ia1, ia2 = mit_in_arrows(s2, o2)
        self.play(FadeOut(ao1), FadeOut(ao2), sug.animate.move_to(s2), oxy.animate.move_to(o2), run_time=1.0)
        self.play(GrowArrow(ia1), GrowArrow(ia2), run_time=0.5)
        self.at("releases energy")
        en = energy_label()
        ea = arr([2.0, -0.1, 0], [1.3, -0.1, 0], ORANGE, w=6)
        self.play(FadeOut(sug), FadeOut(oxy), FadeOut(ia1), FadeOut(ia2),
                  Indicate(VGroup(msh, mnm, msub), color=ORANGE, scale_factor=1.04), run_time=0.8)
        self.play(GrowArrow(ea), FadeIn(en), run_time=0.6)
        self.at("Carbon dioxide and water come out")
        bc, bw = mit_bottom_chips()
        ba1, ba2 = mit_out_arrows(bc, bw)
        self.play(GrowArrow(ba1), GrowArrow(ba2), FadeIn(bc, shift=DOWN * 0.2), FadeIn(bw, shift=DOWN * 0.2), run_time=0.9)
        self.at("some energy leaves as heat")
        ha, hl = heat_group()
        self.play(GrowArrow(ha), FadeIn(hl), run_time=0.7)
        self.finish()


# =============================================================================================
class S04Loop(SpokenScene):
    def construct(self):
        cell = cell_outline()
        sh, nm, sub = chloroplast(); msh, mnm, msub = mitochondrion()
        la = light_arrow(); lab = T("radiant energy", 24, YELLOW).move_to([-4.8, 3.25, 0])
        bc, bw = mit_bottom_chips(); ba1, ba2 = mit_out_arrows(bc, bw)
        en = energy_label(); ea = arr([2.0, -0.1, 0], [1.3, -0.1, 0], ORANGE, w=6)
        ha, hl = heat_group()
        self.add(cell, sh, nm, sub, msh, mnm, msub, la, lab, bc, bw, ba1, ba2, en, ea, ha, hl)
        self.play(FadeOut(en), FadeOut(ea), FadeOut(ha), FadeOut(hl), run_time=0.4)
        # definitions
        self.at("A reactant is")
        d1 = T("reactant: goes in", 26, TEXT, weight=BOLD).move_to([0, 0.5, 0])
        self.play(FadeIn(d1), run_time=0.5)
        self.at("A product is")
        d2 = T("product: comes out", 26, TEXT, weight=BOLD).move_to([0, -0.3, 0])
        self.play(FadeIn(d2), run_time=0.5)
        self.at("products of photosynthesis")
        sug = c_sugar(); oxy = c_oxy()
        ao1, ao2 = photo_out_arrows(sug, oxy)
        t1 = tag("product", GREEN, sug); t2 = tag("product", GREEN, oxy)
        self.play(FadeOut(d1), FadeOut(d2), GrowArrow(ao1), GrowArrow(ao2), FadeIn(sug), FadeIn(oxy),
                  FadeIn(t1), FadeIn(t2), run_time=0.8)
        self.at("reactants of respiration")
        s2, o2 = mit_top_chips()
        ia1, ia2 = mit_in_arrows(s2, o2)
        r1 = tag("reactant", ORANGE, s2); r2 = tag("reactant", ORANGE, o2)
        self.play(FadeOut(ao1), FadeOut(ao2), sug.animate.move_to(s2), oxy.animate.move_to(o2),
                  ReplacementTransform(t1, r1), ReplacementTransform(t2, r2), run_time=1.2)
        self.play(GrowArrow(ia1), GrowArrow(ia2), run_time=0.4)
        self.at("products of respiration")
        p1 = tag("product", ORANGE, bc, below=True); p2 = tag("product", ORANGE, bw, below=True)
        self.play(FadeIn(p1), FadeIn(p2), Indicate(bc, color=PURPLE, scale_factor=1.06),
                  Indicate(bw, color=TEAL, scale_factor=1.1), run_time=0.8)
        self.at("reactants of photosynthesis")
        co2, h2o = photo_inputs()
        ai1, ai2 = photo_in_arrows(co2, h2o)
        q1 = tag("reactant", GREEN, co2, below=True); q2 = tag("reactant", GREEN, h2o, below=True)
        self.play(FadeOut(ba1), FadeOut(ba2), FadeOut(ia1), FadeOut(ia2), FadeOut(sug), FadeOut(oxy),
                  FadeOut(r1), FadeOut(r2),
                  bc.animate.move_to(co2), bw.animate.move_to(h2o),
                  ReplacementTransform(p1, q1), ReplacementTransform(p2, q2), run_time=1.3)
        self.play(GrowArrow(ai1), GrowArrow(ai2), run_time=0.4)
        self.at("interdependent")
        word = T("interdependent", 30, TEXT, weight=BOLD).move_to([0, -0.05, 0])
        top = arr([-2.2, 0.85, 0], [2.2, 0.85, 0], GREEN, w=6)
        bot = arr([2.2, -0.95, 0], [-2.2, -0.95, 0], ORANGE, w=6)
        self.play(FadeIn(word), GrowArrow(top), GrowArrow(bot), run_time=0.8)
        self.at("The same matter is used again")
        again = T("the same matter is used again", 24, TEXT).move_to([0, -1.55, 0])
        self.play(FadeIn(again), Indicate(top, color=GREEN, scale_factor=1.05), run_time=0.6)
        self.play(Indicate(bot, color=ORANGE, scale_factor=1.05), run_time=0.6)
        self.finish()


# =============================================================================================
class S05Energy(SpokenScene):
    def construct(self):
        cell = cell_outline()
        sh, nm, sub = chloroplast(); msh, mnm, msub = mitochondrion()
        la = light_arrow(); lab = T("radiant energy", 24, YELLOW).move_to([-4.8, 3.25, 0])
        self.add(cell, sh, nm, sub, msh, mnm, msub, la, lab)
        self.at("Energy moves differently")
        ban = arr([-2.5, -2.55, 0], [2.5, -2.55, 0], TEXT, w=8, tip=0.3)
        bl = T("energy flows one way", 26, TEXT).move_to([0, -2.05, 0])
        self.play(GrowArrow(ban), FadeIn(bl), run_time=0.8)
        self.at("flows one way")
        self.play(Indicate(ban, color=TEXT, scale_factor=1.08), run_time=0.7)
        self.at("Light from the sun")
        self.play(Indicate(lab, color=YELLOW, scale_factor=1.1), Indicate(la, color=YELLOW, scale_factor=1.06), run_time=0.7)
        self.at("chemical energy in sugar")
        ch = chip("chemical energy in sugar", GOLD, size=24).move_to([0, 1.8, 0])
        a1 = arr([-2.75, 0.62, 0], [-2.0, 1.5, 0], GOLD)
        a2 = arr([2.0, 1.5, 0], [2.95, 0.65, 0], GOLD)
        self.play(GrowArrow(a1), FadeIn(ch), run_time=0.7)
        self.play(GrowArrow(a2), run_time=0.4)
        self.at("Respiration releases")
        en = energy_label(); ea = arr([2.0, -0.1, 0], [1.3, -0.1, 0], ORANGE, w=6)
        self.play(Indicate(VGroup(msh, mnm, msub), color=ORANGE, scale_factor=1.04), run_time=0.7)
        self.play(GrowArrow(ea), FadeIn(en), run_time=0.6)
        self.at("leaves as heat")
        ha, hl = heat_group()
        self.play(GrowArrow(ha), FadeIn(hl), run_time=0.6)
        self.at("changes form")
        self.play(Indicate(lab, color=YELLOW, scale_factor=1.1), run_time=0.5)
        self.play(Indicate(ch, color=GOLD, scale_factor=1.08), run_time=0.5)
        self.play(Indicate(en, color=ORANGE, scale_factor=1.1), run_time=0.5)
        self.finish()


# =============================================================================================
class S06Answer(SpokenScene):
    def construct(self):
        tank_c = np.array([-3.2, -0.6, 0])
        left, right, bot_y, top_y = -5.3, -1.1, -2.6, 1.4
        walls = VGroup(Line([left, top_y, 0], [left, bot_y, 0], color=GREY, stroke_width=7),
                       Line([left, bot_y, 0], [right, bot_y, 0], color=GREY, stroke_width=7),
                       Line([right, bot_y, 0], [right, top_y, 0], color=GREY, stroke_width=7))
        lv = ValueTracker(1.6)
        water = always_redraw(lambda: Rectangle(width=right - left - 0.1, height=max(0.05, lv.get_value()), stroke_width=0,
                                                fill_color=BLUE, fill_opacity=0.38)
                              .move_to([tank_c[0], bot_y + 0.05 + max(0.05, lv.get_value()) / 2, 0]))
        tlab = T("oxygen in the creek water (a model)", 22, BLUE).move_to([tank_c[0], -3.1, 0])
        self.at("creek as a tub")
        self.play(Create(walls), FadeIn(water), FadeIn(tlab), run_time=1.0)
        self.at("The tap is running")
        tap = arr([-3.2, 2.45, 0], [-3.2, 1.3, 0], GREY, w=5)
        tapl = T("tap", 26, GREY).move_to([-3.2, 2.85, 0])
        self.play(GrowArrow(tap), FadeIn(tapl), run_time=0.5)
        drain = arr([-1.1, -2.2, 0], [0.55, -2.2, 0], GREY, w=5)
        drl = T("drain", 26, GREY).move_to([1.5, -2.2, 0])
        self.at("drain is open")
        self.play(GrowArrow(drain), FadeIn(drl), run_time=0.5)
        self.at("Sunlight turns the tap on")
        sun = Circle(radius=0.42, stroke_color=YELLOW, stroke_width=4, fill_color=YELLOW, fill_opacity=0.6).move_to([3.0, 2.3, 0])
        sunl = T("daylight", 26, YELLOW).next_to(sun, RIGHT, buff=0.3)
        tap_on = arr([-3.2, 2.45, 0], [-3.2, 1.3, 0], GREEN, w=12, tip=0.3)
        self.play(FadeIn(sun), FadeIn(sunl), Transform(tap, tap_on), run_time=0.7)
        self.at("The tap is photosynthesis")
        tapl2 = T("photosynthesis adds oxygen", 26, GREEN).move_to([-3.2, 2.85, 0])
        self.play(ReplacementTransform(tapl, tapl2), run_time=0.5)
        self.at("The drain never closes")
        dr_on = arr([-1.1, -2.2, 0], [0.55, -2.2, 0], ORANGE, w=7)
        self.play(Transform(drain, dr_on), run_time=0.5)
        self.at("The drain is respiration")
        drl2 = T("respiration", 26, ORANGE).move_to([1.95, -2.2, 0])
        hedge = T("by nearly every living thing", 22, GREY).move_to([2.6, -2.75, 0])
        self.play(ReplacementTransform(drl, drl2), run_time=0.5)
        self.at("nearly every living thing")
        self.play(FadeIn(hedge), run_time=0.4)
        self.at("By day")
        self.play(lv.animate.set_value(3.0), run_time=2.0, rate_func=smooth)
        self.at("so oxygen climbs")
        up = arr([0.2, -0.7, 0], [0.2, 0.5, 0], BLUE, w=8, tip=0.3)
        upl = T("oxygen climbs", 26, BLUE).move_to([2.2, -0.1, 0])
        self.play(GrowArrow(up), FadeIn(upl), run_time=0.5)
        self.at("After dark")
        dark = Circle(radius=0.42, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.5).move_to([3.0, 2.3, 0])
        darkl = T("dark", 26, GREY).next_to(dark, RIGHT, buff=0.3)
        self.play(FadeOut(up), FadeOut(upl), ReplacementTransform(sun, dark), ReplacementTransform(sunl, darkl),
                  tap.animate.set_opacity(0.15), tapl2.animate.set_opacity(0.3), run_time=0.8)
        self.at("only the drain is open")
        self.play(lv.animate.set_value(0.8), run_time=1.3, rate_func=smooth)
        self.at("tends to fall")
        dn = arr([0.2, 0.5, 0], [0.2, -0.7, 0], BLUE, w=8, tip=0.3)
        dnl = T("oxygen tends to fall", 26, BLUE).move_to([2.0, -0.1, 0])
        self.play(GrowArrow(dn), FadeIn(dnl), run_time=0.5)
        self.at("Plants make new sugar only in light")
        c1 = chip("new sugar: only in light", GREEN, size=26).move_to([3.5, 1.2, 0])
        self.play(FadeOut(dn), FadeOut(dnl), FadeOut(dark), FadeOut(darkl), FadeIn(c1, shift=UP * 0.1), run_time=0.7)
        self.at("respire day and night")
        c2 = chip("respiration: day and night", ORANGE, size=26).move_to([3.5, -0.2, 0])
        self.play(FadeIn(c2, shift=UP * 0.1), run_time=0.7)
        self.finish()


# =============================================================================================
class S07End(EndCard):
    LINE = "Plants make sugar only in light, but respire day and night."
