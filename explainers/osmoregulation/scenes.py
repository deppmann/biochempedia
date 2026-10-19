"""When kidneys cannot clear the salt: the cormorant salt gland  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  BLUE   = water / seawater
  YELLOW = salt (sodium chloride)
  ORANGE = the kidney route (kidneys, urine, cloacal fluid)
  GREEN  = the nasal salt gland route (glands, nasal fluid)
  RED    = the problem, the unknown, what was not shown
  GREY   = outlines, axes, de-emphasized
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def box(w, h, color, x, y, op=0.2, sw=3):
    return RoundedRectangle(corner_radius=0.12, width=w, height=h, stroke_color=color, stroke_width=sw,
                            fill_color=color, fill_opacity=op).move_to([x, y, 0])


def lines(txt, size=24, color=GREY, **kw):
    return VGroup(*[T(s, size, color, **kw) for s in txt.split("\n")]).arrange(DOWN, buff=0.08)


def bird(cx, cy, w, h, label="cormorant"):
    b = box(w, h, GREY, cx, cy, op=0.08, sw=3)
    l = T(label, 24, GREY).next_to(b, UP, buff=0.12)
    return VGroup(b, l)


def vial(x, y, color, w=0.8, h=1.1):
    v = box(w, h, color, x, y, op=0.3, sw=3)
    return v


class S00Title(TitleCard):
    LESSON = "Osmoregulation and nitrogenous waste"
    TITLE = "When Kidneys Cannot Clear the Salt"


# ---------------------------------------------------------------------------------------------
class S01Sea(SpokenScene):
    def construct(self):
        sea = Rectangle(width=12.2, height=1.0, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.25).move_to([0, -2.9, 0])
        sea_l = T("seawater: near 1,000 mOsm/kg (approximate)", 28, BLUE).move_to(sea)
        self.at("A seabird")
        bd = bird(-2.4, 0.35, 6.0, 3.4, "seabird")
        self.play(FadeIn(bd), FadeIn(sea), run_time=0.7)
        self.at("seawater")
        sea_tmp = T("seawater", 28, BLUE).move_to(sea)
        self.play(FadeIn(sea_tmp), run_time=0.5)
        salt_in = arr([-2.4, -2.4, 0], [-2.4, -1.45, 0], YELLOW)
        salt_l = chip("salt", YELLOW, 28).move_to([-4.2, -1.9, 0])
        self.at("heavy load of salt")
        self.play(GrowArrow(salt_in), FadeIn(salt_l, shift=UP * 0.1), run_time=0.7)
        self.at("an approximate figure")
        self.play(ReplacementTransform(sea_tmp, sea_l), run_time=0.8)
        osm = lines("osmolality: dissolved particles\nper kilogram of water", 24, GREY).move_to([3.0, -1.9, 0])
        self.at("That counts dissolved particles")
        self.play(FadeIn(osm, shift=UP * 0.1), run_time=0.7)
        kid = chip("kidneys", ORANGE, 30).move_to([-3.6, 0.35, 0])
        urine = arr([-2.5, 0.35, 0], [1.2, 0.35, 0], ORANGE)
        urine_l = lines("urine, not as salty\nas the sea", 26, ORANGE).move_to([3.9, 0.35, 0])
        self.at("Bird kidneys cannot make urine")
        self.play(FadeIn(kid), run_time=0.5)
        self.play(GrowArrow(urine), FadeIn(urine_l), run_time=0.9)
        q = chip("?", RED, 44, pad=0.3).move_to([1.9, 2.0, 0])
        qa = arr([0.3, 1.4, 0], [1.3, 1.95, 0], RED)
        ql = lines("where does the\nextra salt go?", 30, RED).move_to([4.4, 2.0, 0])
        self.at("where does the extra salt go")
        self.play(GrowArrow(qa), FadeIn(q, scale=0.8), FadeIn(ql), run_time=0.9)
        self.play(Indicate(q, color=RED, scale_factor=1.15), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Kidney(SpokenScene):
    def construct(self):
        head = T("kidney route alone", 34, ORANGE, font=TITLE_FONT).to_edge(UP, buff=0.5)
        gulp = box(2.8, 1.0, BLUE, -4.4, 2.1, op=0.3)
        gl = T("seawater gulp", 26, BLUE).move_to(gulp)
        kid = chip("kidneys", ORANGE, 30).move_to([0, 2.1, 0])
        urine = box(2.8, 1.0, ORANGE, 4.4, 2.1, op=0.2)
        ul = T("urine", 26, ORANGE).move_to(urine)
        a1 = arr([-2.95, 2.1, 0], [-1.2, 2.1, 0], GREY)
        a2 = arr([1.2, 2.1, 0], [2.95, 2.1, 0], GREY)
        fw = lines("fresh water is scarce at sea", 32, BLUE).move_to([0, 0.3, 0])
        fw2 = lines("fresh water\nis scarce at sea", 26, BLUE).move_to([4.7, -0.5, 0])
        self.at("Marine birds such as cormorants")
        self.at("feed at sea")
        self.play(FadeIn(fw, shift=UP * 0.1), run_time=0.7)
        self.at("kidney route alone")
        self.play(ReplacementTransform(fw, fw2), FadeIn(head), FadeIn(gulp), FadeIn(gl), FadeIn(kid), FadeIn(urine), FadeIn(ul), GrowArrow(a1), GrowArrow(a2), run_time=1.1)
        base = -3.0
        b1 = Rectangle(width=2.0, height=1.8, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.35).move_to([-3.2, base + 0.9, 0])
        b2 = Rectangle(width=2.0, height=3.2, stroke_color=RED, stroke_width=3, fill_color=RED, fill_opacity=0.3).move_to([0.6, base + 1.6, 0])
        l1 = T("water drunk", 26, BLUE).next_to(b1, DOWN, buff=0.12)
        l2 = T("water needed", 26, RED).next_to(b2, DOWN, buff=0.12)
        ax = Line([-5.0, base, 0], [2.6, base, 0], color=GREY, stroke_width=3)
        note = T("idealised, not to scale", 24, GREY).move_to([4.5, -3.0, 0])
        self.at("would need more water than it drank")
        self.play(Create(ax), GrowFromEdge(b1, DOWN), FadeIn(l1), run_time=0.8)
        self.play(GrowFromEdge(b2, DOWN), FadeIn(l2), FadeIn(note), run_time=1.0)
        self.at("short of water")
        self.play(Indicate(b2, color=RED, scale_factor=1.05), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
def experiment(scene, show_labels=True):
    """returns dict of mobjects for the two-route bird block."""
    bd = bird(-0.9, 0.2, 4.2, 3.2, "double-crested cormorant")
    gl = chip("nasal salt glands", GREEN, 24).move_to([-0.9, 0.95, 0])
    kd = chip("kidneys", ORANGE, 24).move_to([-0.9, -0.75, 0])
    return bd, gl, kd


class S03Test(SpokenScene):
    def construct(self):
        who = T("1958: Schmidt-Nielsen, Jørgensen, Osaki", 28, GREY).to_edge(UP, buff=0.5)
        bd = bird(-1.6, 0.2, 5.0, 3.6, "double-crested cormorant")
        kd = chip("kidneys", ORANGE, 28).move_to([-1.6, -0.8, 0])
        q = chip("another route?", RED, 28).move_to([-1.6, 0.9, 0])
        flask = chip("salt load", YELLOW, 28).move_to([-5.2, 0.2, 0])
        fl2 = lines("by mouth\nor infusion", 24, YELLOW).next_to(flask, DOWN, buff=0.15)
        fa = arr([-4.2, 0.2, 0], [-4.15 + 0.0, 0.2, 0], YELLOW)
        fa = arr([-4.25, 0.2, 0], [-4.05, 0.2, 0], YELLOW)
        self.at("In 1958")
        self.play(FadeIn(who), run_time=0.6)
        self.at("tested whether another route")
        self.play(FadeIn(bd), FadeIn(kd), run_time=0.7)
        self.play(FadeIn(q, shift=DOWN * 0.1), run_time=0.6)
        self.at("a load of salt")
        self.play(FadeIn(flask), FadeIn(fl2), run_time=0.8)
        self.at("collected two fluids")
        v2 = vial(3.4, -0.9, ORANGE)
        a2 = arr([-0.8, -0.8, 0], [2.85, -0.9, 0], ORANGE)
        l2 = lines("cloacal fluid\n(urine + feces)", 24, ORANGE).move_to([5.2, -0.9, 0])
        self.at("urine mixed with feces")
        self.play(GrowArrow(a2), FadeIn(v2), FadeIn(l2), run_time=0.9)
        v1 = vial(3.4, 1.4, GREEN)
        l1 = lines("clear fluid\ndripping from\nthe beak", 24, GREEN).move_to([5.2, 1.4, 0])
        self.at("clear fluid that dripped")
        self.play(FadeIn(v1), FadeIn(l1), run_time=0.7)
        gl = chip("nasal salt glands", GREEN, 28).move_to([-1.6, 0.9, 0])
        a1 = arr([-0.1, 0.95, 0], [2.85, 1.4, 0], GREEN)
        self.at("Paired nasal salt glands")
        self.play(ReplacementTransform(q, gl), GrowArrow(a1), run_time=0.9)
        self.play(Indicate(gl, color=GREEN, scale_factor=1.1), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Result(SpokenScene):
    def construct(self):
        head = T("after the salt load, in double-crested cormorants", 26, GREY).to_edge(UP, buff=0.45)
        base = -2.3
        sc = 3.6 / 700.0
        ax = Line([-6.0, base, 0], [-0.4, base, 0], color=GREY, stroke_width=3)
        yl = T("mmol/L", 24, GREY).move_to([-3.2, base - 0.45, 0])
        bn = Rectangle(width=1.5, height=500 * sc, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.35).move_to([-4.6, base + 250 * sc, 0])
        band = Rectangle(width=1.5, height=100 * sc, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.12).move_to([-4.6, base + 550 * sc, 0])
        bs = Rectangle(width=1.5, height=470 * sc, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.35).move_to([-2.0, base + 235 * sc, 0])
        nl = lines("nasal fluid\nNaCl 500-600", 24, GREEN).next_to(band, UP, buff=0.12)
        sl = lines("seawater\nsodium about 470", 24, BLUE).next_to(bs, UP, buff=0.12)
        self.at("would carry the load")
        self.play(FadeIn(head), run_time=0.6)
        self.at("It did not")
        self.wait(0.2)
        self.at("the nasal fluid held")
        self.play(Create(ax), FadeIn(yl), GrowFromEdge(bn, DOWN), run_time=0.9)
        self.at("of sodium chloride")
        self.play(FadeIn(band), FadeIn(nl), run_time=0.8)
        self.at("similar to seawater")
        self.play(GrowFromEdge(bs, DOWN), FadeIn(sl), run_time=0.9)
        # right chart: relative salt output
        ax2 = Line([0.6, base, 0], [6.0, base, 0], color=GREY, stroke_width=3)
        g = Rectangle(width=1.5, height=3.1, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.35).move_to([2.0, base + 1.55, 0])
        c = Rectangle(width=1.5, height=0.31, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE, fill_opacity=0.35).move_to([4.6, base + 0.15, 0])
        gl_ = lines("nasal glands", 22, GREEN).next_to(g, DOWN, buff=0.12)
        cl_ = lines("cloaca", 22, ORANGE).next_to(c, DOWN, buff=0.12)
        ttl = lines("total salt output: amount,\nnot concentration\n(relative lengths)", 24, GREY).move_to([3.3, 1.9, 0])
        ten = T("about ten times", 26, YELLOW).next_to(g, RIGHT, buff=0.3).shift(UP * 0.2)
        self.at("times as much")
        self.play(Create(ax2), GrowFromEdge(g, DOWN), FadeIn(gl_), run_time=0.8)
        self.play(GrowFromEdge(c, DOWN), FadeIn(cl_), FadeIn(ttl), FadeIn(ten), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Water(SpokenScene):
    def construct(self):
        head = T("in this sketch: idealised, not to scale", 24, GREY).to_edge(UP, buff=0.5)
        gulp = box(2.4, 2.6, BLUE, -5.0, 0.2, op=0.3)
        gs = chip("salt", YELLOW, 26).move_to(gulp)
        gl = lines("a gulp of\nseawater", 24, BLUE).next_to(gulp, DOWN, buff=0.15)
        gland = chip("nasal salt gland", GREEN, 24).move_to([-1.5, 0.2, 0])
        a1 = arr([-3.7, 0.2, 0], [-3.05, 0.2, 0], GREY)
        a2 = arr([-0.1, 0.2, 0], [0.7, 0.2, 0], GREY)
        # stacked outputs equal to gulp height 2.6
        out = box(2.4, 1.5, GREEN, 2.0, 0.75, op=0.2)
        os_ = chip("same salt", YELLOW, 24).move_to(out)
        kept = box(2.4, 1.1, BLUE, 2.0, -0.55, op=0.35)
        ol = lines("gland fluid:\nmore concentrated", 22, GREEN).move_to([4.95, 0.8, 0])
        kl = lines("water the\nbird keeps", 22, BLUE).move_to([4.95, -0.55, 0])
        self.at("A gland that excretes salt")
        self.play(FadeIn(head), FadeIn(gland), run_time=0.6)
        self.at("than seawater")
        self.play(FadeIn(gulp), FadeIn(gl), run_time=0.8)
        self.at("a gulp of seawater")
        self.play(FadeIn(gs), Indicate(gulp, color=BLUE, scale_factor=1.05), run_time=0.8)
        self.at("in less water than the gulp held")
        self.play(GrowArrow(a1), run_time=0.4)
        self.play(GrowArrow(a2), run_time=0.3)
        self.play(FadeIn(out), FadeIn(os_), FadeIn(ol), run_time=0.9)
        self.at("It keeps the difference")
        self.play(FadeIn(kept), FadeIn(kl), run_time=0.9)
        self.play(Indicate(kept, color=BLUE, scale_factor=1.06), run_time=0.8)
        self.at("Gulls reach even higher")
        gnote = T("gulls reach higher values still", 26, GREEN).move_to([0.0, -2.7, 0])
        self.play(FadeIn(gnote, shift=UP * 0.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        bd = bird(-3.8, 0.2, 4.2, 3.6, "cormorant")
        gl = chip("nasal salt glands", GREEN, 24).move_to([-3.8, 0.95, 0])
        kd = chip("kidneys", ORANGE, 24).move_to([-3.8, -0.8, 0])
        g_out = arr([-2.4, 0.95, 0], [-1.5, 0.95, 0], GREEN)
        k_out = arr([-3.05, -0.8, 0], [-1.5, -0.8, 0], ORANGE)
        self.at("What did the experiment show")
        self.play(FadeIn(bd), FadeIn(gl), FadeIn(kd), GrowArrow(k_out), run_time=0.9)
        r1 = lines("ruled in:\na route besides the kidneys", 24, GREEN).move_to([2.4, 1.9, 0])
        ok = chip("salt load excreted", GREEN, 24).move_to([2.4, 0.95, 0])
        self.at("It ruled in a route")
        self.play(GrowArrow(g_out), FadeIn(r1), FadeIn(ok), Indicate(gl, color=GREEN, scale_factor=1.1), run_time=1.1)
        n1 = chip("? how the gland concentrates salt", RED, 24).move_to([2.4, -0.15, 0])
        self.at("It did not show how")
        self.play(FadeIn(n1, shift=LEFT * 0.2), run_time=0.7)
        n2 = chip("? every bird has active glands", RED, 24).move_to([2.4, -1.1, 0])
        self.at("every bird")
        self.play(FadeIn(n2, shift=LEFT * 0.2), run_time=0.7)
        rep = chip("marine reptiles: salt glands too", GREY, 24).move_to([2.4, -2.1, 0])
        rep2 = T("sea turtles, marine iguana", 22, GREY).next_to(rep, DOWN, buff=0.12)
        self.at("Sea turtles")
        self.play(FadeIn(rep), FadeIn(rep2), run_time=0.7)
        self.at("In cormorants")
        self.play(Indicate(gl, color=GREEN, scale_factor=1.12), Indicate(g_out, color=GREEN), run_time=0.9)
        self.finish()


class S07End(EndCard):
    LINE = "In cormorants, salt can leave by a route besides the kidneys."
