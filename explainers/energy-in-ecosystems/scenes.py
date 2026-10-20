"""Sunlight in, heat out: energy flows one way through the Bay  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  YELLOW = energy as it arrives and is stored (sunlight, chemical energy in food, the 10 percent rule)
  GREEN  = producer (phytoplankton)
  BLUE   = consumer (zooplankton, menhaden, osprey) and new body tissue
  ORANGE = decomposer
  RED    = heat
  GREY   = uneaten or undigested matter, structure, notes
  TEAL   = carbon (matter that cycles)
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
SUN, PRODUCER, CONSUMER, DECOMP, HEAT, UNEATEN, CARBON = YELLOW, GREEN, BLUE, ORANGE, RED, GREY, TEAL
CY = 0.9   # chain row y


def node(text, color, size=24):
    return chip(text, color, size=size)


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def chain_nodes():
    names = [("sunlight", SUN), ("phytoplankton", PRODUCER), ("zooplankton", CONSUMER),
             ("Atlantic menhaden", CONSUMER), ("osprey", CONSUMER)]
    mobs = [node(n, c) for n, c in names]
    g = VGroup(*mobs).arrange(RIGHT, buff=0.62).move_to([0, CY, 0])
    if g.width > SAFE_W:
        g.scale(SAFE_W / g.width).move_to([0, CY, 0])
    return {"sun": mobs[0], "phy": mobs[1], "zoo": mobs[2], "men": mobs[3], "osp": mobs[4]}


def link(a, b, color=GREY, w=5):
    return arr(a.get_right(), b.get_left(), color, w)


class S00Title(TitleCard):
    LESSON = "Energy in Ecosystems"
    TITLE = "Sunlight In, Heat Out"


# ---------------------------------------------------------------------------------------------
class S01Osprey(SpokenScene):
    def construct(self):
        n = chain_nodes()
        head = T("Chesapeake Bay", 28, GREY).to_edge(UP, buff=0.55)
        self.at("Along the Chesapeake")
        self.play(FadeIn(head), run_time=0.4)
        self.at("an osprey")
        self.play(FadeIn(n["osp"], shift=LEFT * 0.3), run_time=0.6)
        self.at("Menhaden filter")
        a_mo = link(n["men"], n["osp"], CONSUMER)
        self.play(FadeIn(n["men"], shift=LEFT * 0.3), GrowArrow(a_mo), run_time=0.7)
        self.at("tiny plankton")
        long_a = arr(n["phy"].get_right(), n["men"].get_left(), PRODUCER)
        self.play(FadeIn(n["phy"], shift=LEFT * 0.3), GrowArrow(long_a), run_time=0.7)
        self.at("from sunlight")
        a_sp = link(n["sun"], n["phy"], SUN)
        self.play(FadeIn(n["sun"], shift=RIGHT * 0.3), GrowArrow(a_sp), run_time=0.7)
        q1 = T("Where does the osprey's energy come from?", 40, TEXT).move_to([0, -1.3, 0])
        self.at("where does")
        self.play(FadeIn(q1, shift=UP * 0.2), run_time=0.7)
        q2 = T("Why is there less at each step?", 40, YELLOW).move_to([0, -2.5, 0])
        self.at("less of it")
        qm = VGroup(*[T("?", 44, YELLOW, weight=BOLD).next_to(a, UP, buff=0.12) for a in (a_sp, long_a, a_mo)])
        self.play(FadeIn(q2, shift=UP * 0.2), LaggedStart(*[FadeIn(q) for q in qm], lag_ratio=0.25), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Chain(SpokenScene):
    def construct(self):
        n = chain_nodes()
        a_sp = link(n["sun"], n["phy"], SUN)
        long_a = arr(n["phy"].get_right(), n["men"].get_left(), PRODUCER)
        a_mo = link(n["men"], n["osp"], CONSUMER)
        head = T("Chesapeake Bay", 28, GREY).to_edge(UP, buff=0.55)
        self.add(head, n["sun"], n["phy"], n["men"], n["osp"], a_sp, long_a, a_mo)

        def under(txt, mob, color, dy=0.85):
            return T(txt, 28, color).next_to(mob, DOWN, buff=0.3)

        self.at("A producer")
        l_prod = under("producer", n["phy"], PRODUCER)
        self.play(FadeIn(l_prod, shift=UP * 0.15), Indicate(n["sun"], color=SUN, scale_factor=1.1), run_time=0.7)
        self.at("phytoplankton")
        self.play(Indicate(n["phy"], color=PRODUCER, scale_factor=1.12), run_time=0.7)
        self.at("A consumer")
        l_c1 = under("consumer", n["men"], CONSUMER)
        l_c2 = under("consumer", n["osp"], CONSUMER)
        self.play(FadeIn(l_c1, shift=UP * 0.15), FadeIn(l_c2, shift=UP * 0.15), run_time=0.7)
        self.at("Zooplankton eat")
        arc = CurvedArrow(n["phy"].get_top() + UP * 0.02, n["men"].get_top() + UP * 0.02, angle=-1.1,
                          color=CONSUMER, stroke_width=5, tip_length=0.2)
        a1 = link(n["phy"], n["zoo"], CONSUMER)
        a2 = link(n["zoo"], n["men"], CONSUMER)
        l_c3 = under("consumer", n["zoo"], CONSUMER)
        self.play(FadeOut(long_a), FadeIn(n["zoo"], shift=DOWN * 0.3), FadeIn(l_c3), run_time=0.7)
        self.play(GrowArrow(a1), GrowArrow(a2), run_time=0.6)
        self.at("Menhaden eat both")
        self.play(Create(arc), run_time=0.8)
        self.play(Indicate(n["men"], color=CONSUMER, scale_factor=1.12), run_time=0.6)
        self.at("The osprey eats")
        self.play(Indicate(n["osp"], color=CONSUMER, scale_factor=1.12), Indicate(a_mo, color=TEXT), run_time=0.7)
        self.at("Each feeding step")
        cap = node("trophic level = one feeding step", GOLD, size=34).move_to([0, -1.6, 0])
        self.play(FadeIn(cap, shift=UP * 0.2), run_time=0.5)
        for a in (a1, a2, a_mo):
            self.play(Indicate(a, color=GOLD, scale_factor=1.3), run_time=0.45)
        self.at("Arrows point")
        cap2 = node("arrows point from food to eater", TEXT, size=34).move_to([0, -2.9, 0])
        self.play(FadeIn(cap2, shift=UP * 0.2), run_time=0.5)
        self.play(Indicate(a_sp, color=TEXT, scale_factor=1.3), Indicate(a1, color=TEXT, scale_factor=1.3), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Lost(SpokenScene):
    def construct(self):
        phy = node("phytoplankton cell", PRODUCER, size=28).move_to([-3.4, 2.85, 0])
        zoo = node("zooplankton", CONSUMER, size=28).move_to([3.0, 2.85, 0])
        eat = arr(phy.get_right(), zoo.get_left(), CONSUMER)
        eat_l = T("eaten by", 24, GREY).next_to(eat, UP, buff=0.08)
        self.at("When a zooplankton")
        self.play(FadeIn(phy), FadeIn(zoo), run_time=0.6)
        self.play(GrowArrow(eat), FadeIn(eat_l), run_time=0.5)
        X0, W, Y, H = -5.5, 11.0, 0.8, 0.95
        outline = Rectangle(width=W, height=H, stroke_color=TEXT, stroke_width=3, fill_opacity=0).move_to([X0 + W / 2, Y, 0])
        bar_l = T("energy in the eaten cell", 28, YELLOW).move_to([0, Y + 0.95, 0])
        self.at("most of that energy")
        note = T("sizes not to scale", 22, GREY).to_corner(DR, buff=0.5)
        self.play(Create(outline), FadeIn(bar_l, shift=DOWN * 0.1), FadeIn(note), run_time=0.8)

        def seg(x0, w, color):
            return Rectangle(width=w, height=H, stroke_width=0, fill_color=color, fill_opacity=0.55).move_to([x0 + w / 2, Y, 0])
        s_heat, s_un, s_new = seg(X0, 5.0, HEAT), seg(X0 + 5.0, 4.2, UNEATEN), seg(X0 + 9.2, 1.8, CONSUMER)
        cx = lambda s: s.get_center()[0]
        self.at("released as heat")
        l_heat = VGroup(T("heat", 30, HEAT, weight=BOLD), T("cellular respiration", 24, HEAT)).arrange(DOWN, buff=0.1).move_to([cx(s_heat), Y - 1.0, 0])
        self.play(FadeIn(s_heat), FadeIn(l_heat, shift=UP * 0.1), run_time=0.8)
        self.at("not eaten or not digested")
        l_un = T("uneaten or\nundigested matter", 26, UNEATEN, line_spacing=0.8).move_to([cx(s_un), Y - 1.05, 0])
        self.play(FadeIn(s_un), FadeIn(l_un, shift=UP * 0.1), run_time=0.8)
        self.at("decomposers")
        dec = node("decomposer", DECOMP, size=28).move_to([cx(s_un), -2.5, 0])
        dec_s = T("gets energy from dead matter", 22, DECOMP).next_to(dec, DOWN, buff=0.12)
        to_dec = arr([cx(s_un), -1.0, 0], dec.get_top(), UNEATEN)
        self.play(GrowArrow(to_dec), FadeIn(dec), run_time=0.6)
        self.play(FadeIn(dec_s), run_time=0.4)
        self.at("new body tissue")
        l_new = T("new body tissue", 28, CONSUMER, weight=BOLD).move_to([cx(s_new), Y - 1.0, 0])
        self.play(FadeIn(s_new), FadeIn(l_new, shift=UP * 0.1), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Tenth(SpokenScene):
    def construct(self):
        big = VGroup(T("rule of thumb", 30, GREY), T("about 10 percent", 66, YELLOW, weight=BOLD)).arrange(DOWN, buff=0.25).move_to([0, 0.3, 0])
        self.at("rule of thumb")
        self.play(FadeIn(big, shift=UP * 0.2), run_time=0.8)
        top = node("rule of thumb: about 10 percent passes on", YELLOW, size=26).move_to([0, 3.1, 0])
        head = VGroup(T("a model patch of bay, made-up numbers", 24, TEXT),
                      T("kJ per square meter per year", 24, GREY)).arrange(DOWN, buff=0.1).move_to([0, 2.25, 0])
        self.at("model patch")
        self.play(FadeOut(big), FadeIn(top, shift=DOWN * 0.2), run_time=0.9)
        self.play(FadeIn(head), run_time=0.5)
        rows = [("phytoplankton", PRODUCER, 100000, 1.35), ("zooplankton", CONSUMER, 10000, 0.3),
                ("menhaden", CONSUMER, 1000, -0.75), ("osprey", CONSUMER, 100, -1.8)]
        SC, CXB = 6.0 / 100000, -0.4
        objs = []
        for name, col, val, y in rows:
            nm = T(name, 26, col).move_to([-6.3, y, 0], aligned_edge=LEFT)
            nm.move_to([-6.3 + nm.width / 2, y, 0])
            guide = DashedLine([-6.3 + nm.width + 0.1, y, 0], [3.5, y, 0], color=GREY, stroke_width=1.5, stroke_opacity=0.5)
            w = max(val * SC, 0.04)
            bar = Rectangle(width=w, height=0.55, stroke_width=0, fill_color=col, fill_opacity=0.9).move_to([CXB, y, 0])
            vt = M(f"{val:,}", 30, TEXT)
            vt.move_to([3.7 + vt.width / 2, y, 0])
            objs.append((nm, guide, bar, vt, y))
        mult = []
        for i, y in enumerate([0.82, -0.22, -1.27]):
            mult.append(M("× 0.10", 24, YELLOW).move_to([1.2, y, 0]))
        def show(i, mi=None):
            nm, guide, bar, vt, y = objs[i]
            anims = [FadeIn(nm), FadeIn(guide), GrowFromCenter(bar) if i == 0 else FadeIn(bar), FadeIn(vt)]
            if mi is not None:
                anims.append(FadeIn(mult[mi], shift=DOWN * 0.1))
            self.play(*anims, run_time=0.7)
        self.at("Phytoplankton add")
        show(0)
        self.at("Zooplankton get")
        show(1, 0)
        self.at("Menhaden get")
        show(2, 1)
        self.at("osprey level")
        show(3, 2)
        thin = T("bars to scale: this one is too thin to see", 22, GREY).move_to([-0.4, -2.35, 0])
        self.play(FadeIn(thin), run_time=0.4)
        self.at("higher or lower")
        hl = T("real measurements: often higher or lower", 28, TEXT).move_to([0, -3.0, 0])
        self.play(FadeIn(hl, shift=UP * 0.1), run_time=0.6)
        self.at("average")
        avg = node("2026 synthesis: average about 6 percent", GOLD, size=26).move_to([0, -3.0, 0])
        self.play(FadeOut(hl), FadeOut(thin), FadeIn(avg, shift=UP * 0.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Flow(SpokenScene):
    def construct(self):
        lab_e = T("ENERGY", 26, YELLOW, weight=BOLD).move_to([-6.3, 3.2, 0], aligned_edge=LEFT)
        lab_e.move_to([-6.3 + lab_e.width / 2, 3.2, 0])
        divider = Line([-6.3, 0.1, 0], [6.3, 0.1, 0], color=GREY, stroke_width=1.5, stroke_opacity=0.5)
        lab_m = T("MATTER (carbon)", 26, CARBON, weight=BOLD)
        lab_m.move_to([-6.3 + lab_m.width / 2, -0.25, 0])
        self.play(FadeIn(lab_e), FadeIn(divider), FadeIn(lab_m), run_time=0.3)
        sun = node("sunlight", SUN).move_to([-5.2, 1.9, 0])
        food = node("chemical energy in food", SUN).move_to([-1.3, 1.9, 0])
        motion = node("motion", TEXT).move_to([4.4, 2.6, 0])
        heat = node("heat", HEAT).move_to([4.4, 1.2, 0])
        a1 = arr(sun.get_right(), food.get_left(), SUN)
        a2 = arr(food.get_right(), motion.get_left(), TEXT)
        a3 = arr(food.get_right(), heat.get_left(), HEAT)
        self.play(FadeIn(sun), run_time=0.4)
        self.at("Light becomes")
        self.play(GrowArrow(a1), FadeIn(food), run_time=0.8)
        self.at("Food energy becomes")
        self.play(GrowArrow(a2), GrowArrow(a3), FadeIn(motion), FadeIn(heat), run_time=0.9)
        self.at("No living thing")
        nox = VGroup(Line(UL * 0.2, DR * 0.2, color=RED, stroke_width=6), Line(UR * 0.2, DL * 0.2, color=RED, stroke_width=6))
        no_t = T("cannot build food again", 24, HEAT).move_to([4.4, 0.55, 0])
        nox.next_to(no_t, LEFT, buff=0.15)
        self.play(FadeIn(no_t), Create(nox), run_time=0.7)
        self.at("flows one way")
        in_l = T("in", 28, SUN, weight=BOLD).next_to(sun, DOWN, buff=0.2)
        out_l = T("out", 28, HEAT, weight=BOLD).next_to(heat, RIGHT, buff=0.2)
        self.play(FadeIn(in_l), Indicate(sun, color=SUN), run_time=0.5)
        self.play(FadeIn(out_l), Indicate(heat, color=HEAT), run_time=0.5)
        # matter
        dead = node("dead menhaden", UNEATEN).move_to([-3.8, -1.0, 0])
        dec = node("decomposers", DECOMP).move_to([-3.8, -2.9, 0])
        co2 = node("carbon dioxide", CARBON).move_to([3.8, -2.9, 0])
        phy = node("phytoplankton", PRODUCER).move_to([3.8, -1.0, 0])
        b1 = arr(dead.get_bottom(), dec.get_top(), CARBON)
        b2 = arr(dec.get_right(), co2.get_left(), CARBON)
        b3 = arr(co2.get_top(), phy.get_bottom(), CARBON)
        b4 = arr(phy.get_left(), dead.get_right(), CARBON)
        self.at("Matter behaves")
        mt = T("matter cycles", 34, CARBON, weight=BOLD).move_to([0, -1.95, 0])
        self.play(FadeIn(dead), FadeIn(mt), run_time=0.6)
        self.at("Decomposers release")
        self.play(GrowArrow(b1), FadeIn(dec), run_time=0.5)
        self.play(GrowArrow(b2), FadeIn(co2), run_time=0.6)
        self.at("phytoplankton can take")
        self.play(GrowArrow(b3), FadeIn(phy), run_time=0.6)
        thru = T("through the food chain", 22, GREY).move_to([0, -0.62, 0])
        self.play(GrowArrow(b4), FadeIn(thru), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Answer(SpokenScene):
    def construct(self):
        xs = [-4.4, -1.5, 1.6, 4.5]
        names = [("phytoplankton", PRODUCER), ("zooplankton", CONSUMER), ("menhaden", CONSUMER), ("osprey", CONSUMER)]
        ch = [node(t, c).move_to([x, 0.5, 0]) for (t, c), x in zip(names, xs)]
        sun = node("sunlight", SUN).move_to([-5.1, 2.9, 0])
        a_sun = arr(sun.get_bottom(), [-5.1, ch[0].get_top()[1], 0], SUN)
        links = [link(ch[i], ch[i + 1], YELLOW) for i in range(3)]
        bar = RoundedRectangle(corner_radius=0.14, width=12.4, height=0.7, stroke_color=DECOMP, stroke_width=2.5,
                               fill_color=DECOMP, fill_opacity=0.16).move_to([0, -2.3, 0])
        bar_l = T("decomposers", 26, DECOMP).move_to(bar)
        self.at("So where does")
        self.play(LaggedStart(*[FadeIn(c) for c in ch], lag_ratio=0.2), run_time=1.0)
        self.play(*[GrowArrow(a) for a in links], run_time=0.5)
        self.at("It began as sunlight")
        self.play(FadeIn(sun), GrowArrow(a_sun), run_time=0.8)
        self.play(Indicate(ch[0], color=PRODUCER, scale_factor=1.12), run_time=0.6)
        self.at("much of the energy is released as heat")
        heats = []
        for c in ch:
            a = arr([c.get_center()[0] + 0.6, c.get_top()[1], 0], [c.get_center()[0] + 0.6, c.get_top()[1] + 0.95, 0], HEAT, w=4)
            t = T("heat", 24, HEAT).next_to(a, UP, buff=0.05)
            heats.append(VGroup(a, t))
        self.play(LaggedStart(*[FadeIn(h, shift=UP * 0.15) for h in heats], lag_ratio=0.2), run_time=1.0)
        self.at("or left in uneaten")
        greys = [arr([c.get_center()[0] + 0.6, c.get_bottom()[1], 0], [c.get_center()[0] + 0.6, bar.get_top()[1], 0], UNEATEN, w=4) for c in ch]
        un_l = T("uneaten or undigested matter", 24, UNEATEN).move_to([0, -0.95, 0])
        un_l_back = Rectangle(width=un_l.width + 0.3, height=un_l.height + 0.16, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(un_l)
        self.play(FadeIn(bar), FadeIn(bar_l), *[GrowArrow(g) for g in greys], run_time=0.9)
        self.play(FadeIn(un_l_back), FadeIn(un_l), run_time=0.4)
        self.at("only a small share")
        pct = node("rule of thumb: about 10 percent passes upward", YELLOW, size=26).move_to([1.6, 2.9, 0])
        self.play(FadeIn(pct, shift=DOWN * 0.1), *[Indicate(a, color=YELLOW, scale_factor=1.3) for a in links], run_time=1.0)
        self.at("carbon can cycle")
        cxp = ch[0].get_center()[0] - 0.7
        s2 = arr([cxp, bar.get_top()[1], 0], [cxp, ch[0].get_bottom()[1], 0], CARBON)
        c_l = T("carbon", 24, CARBON)
        c_l.move_to([cxp - 0.15 - c_l.width / 2, -0.75, 0])
        self.play(GrowArrow(s2), FadeIn(c_l), run_time=0.8)
        self.at("but the energy will not")
        for h in heats:
            self.play(Indicate(h, color=HEAT, scale_factor=1.15), run_time=0.25)
        self.finish()


class S07End(EndCard):
    LINE = "Much of the carbon can cycle back, but the energy will not."
