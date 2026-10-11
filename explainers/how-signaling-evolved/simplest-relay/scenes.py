"""Two proteins, one phosphate: the bacterial two-component relay  (section film, how-signaling-evolved)

COLOR MAP (one color per concept, whole video)
  BLUE   = sensor kinase (bacterial)
  PURPLE = responder (bacterial)
  GOLD   = a phosphate (the "P" badge, and the bars that show how long it lasts)
  YELLOW = the signal
  GREEN  = switched ON
  ORANGE = animal pathway proteins (target protein, receptor, kinases)
  RED    = phosphatase / removal / "no reader"
  TEAL   = the SH2 reading domain and the protein that carries it
  PINK   = the gene (output)
  GREY   = membrane, ATP, labels, de-emphasised
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58BB5"


def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def pbadge(size=0.24):
    c = Circle(radius=size, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=1)
    return VGroup(c, T("P", 24, BG, weight=BOLD).move_to(c))


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def membrane_h(y, x0=-6.3, x1=6.3, h=0.32):
    return RoundedRectangle(corner_radius=0.1, width=x1 - x0, height=h, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.35).move_to([(x0 + x1) / 2, y, 0])


def slot(color, s=0.5):
    return Square(s, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.55)


def dome(color=TEAL, r=0.5, dashed=False):
    a = Arc(radius=r, start_angle=0, angle=PI, color=color, stroke_width=8)
    l1 = Line(a.get_start(), a.get_start() + DOWN * 0.18, color=color, stroke_width=8)
    l2 = Line(a.get_end(), a.get_end() + DOWN * 0.18, color=color, stroke_width=8)
    g = VGroup(a, l1, l2)
    if dashed:
        g.set_opacity(0.7)
    return g


def toggle(on=False, scale=1.0):
    c = GREEN if on else GREY
    body = RoundedRectangle(corner_radius=0.5, width=2.0, height=1.0, stroke_color=c, stroke_width=5,
                            fill_color=c, fill_opacity=0.25)
    knob = Circle(radius=0.36, stroke_width=0, fill_color=TEXT, fill_opacity=1)
    knob.move_to(body.get_center() + RIGHT * (0.5 if on else -0.5))
    g = VGroup(body, knob)
    g.body, g.knob = body, knob
    g.scale(scale)
    return g


def flip_on(sw):
    off = sw.body.width * 0.25
    return [sw.knob.animate.move_to(sw.body.get_center() + RIGHT * off),
            sw.body.animate.set_stroke(GREEN).set_fill(GREEN, 0.25)]


# fixed geometry shared by scenes 1 and 2
MEM_Y = 1.1
SLOT_DY = -1.5          # slot sits this far below the membrane line


def sensor_parts(x):
    body = RoundedRectangle(corner_radius=0.25, width=1.3, height=2.4, stroke_color=BLUE, stroke_width=4,
                            fill_color=BLUE, fill_opacity=0.28).move_to([x, MEM_Y, 0])
    hs = slot(BLUE).move_to([x, MEM_Y + SLOT_DY, 0])
    hl = T("histidine", 24, BLUE).next_to(hs, LEFT, buff=0.2)
    lbl = T("sensor kinase", 28, BLUE).move_to([x + 3.0, 2.2, 0])
    return body, hs, hl, lbl


def membrane_scene_base():
    mem = membrane_h(MEM_Y)
    out_l = T("outside", 24, GREY).move_to([-5.5, MEM_Y + 0.6, 0])
    in_l = T("inside", 24, GREY).move_to([-5.5, MEM_Y - 0.6, 0])
    return mem, out_l, in_l


class S00Title(TitleCard):
    LESSON = "How signaling evolved"
    TITLE = "Two Proteins, One Phosphate"


# ---------------------------------------------------------------------------------------------
class S01Sensor(SpokenScene):
    def construct(self):
        head = T("A two-component system", 34, font=TITLE_FONT).to_edge(UP, buff=0.4)
        mem, out_l, in_l = membrane_scene_base()
        body, hs, hl, lbl = sensor_parts(0)
        usually = T("usually set in the membrane", 22, GREY).move_to([3.0, 1.7, 0])
        self.play(FadeIn(head), FadeIn(mem), FadeIn(out_l), FadeIn(in_l), run_time=0.8)

        self.at("bacterium senses")
        self.play(FadeIn(body, scale=0.9), run_time=0.7)
        self.at("is a sensor kinase")
        self.play(FadeIn(lbl), run_time=0.5)
        self.at("usually set in")
        self.play(FadeIn(usually), Indicate(mem, color=GREY, scale_factor=1.05), run_time=0.8)

        sig = Circle(radius=0.3, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.9)
        sig.move_to([-4.6, 2.3, 0])
        sig_l = T("signal", 26, YELLOW).next_to(sig, UP, buff=0.15)
        self.at("detects its signal")
        self.play(FadeIn(sig), FadeIn(sig_l), run_time=0.4)
        self.play(sig.animate.move_to([-1.15, 1.9, 0]), sig_l.animate.move_to([-2.2, 2.45, 0]), run_time=0.7)
        self.play(Indicate(body, color=YELLOW, scale_factor=1.04), run_time=0.5)

        atp = bchip("ATP", GREY, 28).move_to([-3.2, -2.4, 0])
        pb = pbadge().move_to(atp.get_right() + RIGHT * 0.05)
        self.at("end phosphate")
        self.play(FadeIn(atp, shift=UP * 0.2), run_time=0.5)
        self.play(FadeIn(pb, scale=0.6), run_time=0.3)

        self.at("puts that phosphate")
        self.play(FadeIn(hs), FadeIn(hl), run_time=0.4)
        self.play(pb.animate.move_to(hs.get_center()), run_time=0.9)
        self.play(Indicate(hs, color=GOLD, scale_factor=1.15), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Responder(SpokenScene):
    def construct(self):
        head = T("A two-component system", 34, font=TITLE_FONT).to_edge(UP, buff=0.4)
        mem, out_l, in_l = membrane_scene_base()
        body, hs, hl, lbl = sensor_parts(0)
        pb = pbadge().move_to(hs.get_center())
        sensor = VGroup(body, hs, hl, lbl, pb)
        self.add(head, mem, out_l, in_l, sensor)

        self.at("is the responder")
        self.play(sensor.animate.shift(LEFT * 4.0), run_time=0.8)
        rcx, rcy = -0.2, -1.7
        rbody = RoundedRectangle(corner_radius=0.25, width=2.4, height=1.5, stroke_color=PURPLE, stroke_width=4,
                                 fill_color=PURPLE, fill_opacity=0.28).move_to([rcx, rcy, 0])
        rlab = T("responder", 28, PURPLE).move_to(rbody)
        asp = slot(PURPLE).move_to([rcx - 1.45, rcy, 0])
        asp_l = T("aspartate", 24, PURPLE).next_to(asp, LEFT, buff=0.2)
        self.play(FadeIn(rbody, shift=UP * 0.2), FadeIn(rlab), FadeIn(asp), FadeIn(asp_l), run_time=0.8)

        self.at("moves that phosphate")
        self.play(pb.animate.move_to(asp.get_center()), run_time=1.1)
        self.play(Indicate(asp, color=GOLD, scale_factor=1.15), run_time=0.4)

        self.at("change in shape")
        new_body = RoundedRectangle(corner_radius=0.25, width=2.0, height=1.9, stroke_color=PURPLE, stroke_width=4,
                                    fill_color=PURPLE, fill_opacity=0.28).move_to([rcx + 0.2, rcy, 0])
        shp = T("shape changes", 22, GREY).move_to([rcx + 0.2, rcy + 1.35, 0])
        self.play(Transform(rbody, new_body), rlab.animate.shift(RIGHT * 0.2), asp.animate.shift(RIGHT * 0.4),
                  pb.animate.shift(RIGHT * 0.4), FadeIn(shp), run_time=0.8)
        self.at("switches it on")
        on = T("ON", 30, GREEN, weight=BOLD).move_to([rcx + 0.2, rcy + 1.35, 0])
        self.play(ReplacementTransform(shp, on), rlab.animate.set_color(GREEN),
                  rbody.animate.set_stroke(GREEN).set_fill(GREEN, 0.28), run_time=0.5)

        self.at("Most responders")
        most = T("most responders: transcription factors", 22, GREY).move_to([2.6, rcy - 1.55, 0])
        self.play(FadeIn(most), run_time=0.6)
        sw = toggle(False, 0.7).move_to([4.9, rcy, 0])
        gl = T("gene switch", 26, PINK).next_to(sw, UP, buff=0.3)
        a = arr([rcx + 1.35, rcy, 0], [3.8, rcy, 0], GREEN)
        self.at("transcription factors")
        self.play(GrowArrow(a), FadeIn(sw), run_time=0.7)
        self.at("gene switch")
        self.play(FadeIn(gl), run_time=0.4)
        self.at("one phosphate")
        self.play(*flip_on(sw), sw.body.animate.set_stroke(GREEN), run_time=0.5)
        self.play(Indicate(pb, color=GOLD, scale_factor=1.4), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Stays(SpokenScene):
    def construct(self):
        # lane 1: bacterial responder; lane 2: animal protein
        c1 = bchip("responder", PURPLE, 26).move_to([-4.7, 2.1, 0])
        n1 = T("on aspartate", 24, GREY).next_to(c1, DOWN, buff=0.25)
        c2 = bchip("animal protein", ORANGE, 26).move_to([-4.7, -1.2, 0])
        n2 = T("on serine, threonine\nor tyrosine", 22, GREY).next_to(c2, DOWN, buff=0.25)
        sep = DashedLine([-6.3, 0.2, 0], [6.3, 0.2, 0], color=GREY, stroke_width=2).set_opacity(0.6)

        self.at("Set this beside")
        self.play(FadeIn(c1), FadeIn(c2), FadeIn(sep), run_time=0.8)

        self.at("phosphate on")
        p1 = pbadge().move_to(c1.get_corner(UR) + [0.05, 0.05, 0])
        self.play(FadeIn(n1), FadeIn(p1, scale=0.6), run_time=0.6)

        # lifetimes of the aspartate phosphate (not to scale)
        x0 = -2.4
        bar_a = Line([x0, 2.55, 0], [x0 + 1.2, 2.55, 0], color=GOLD, stroke_width=14)
        bar_b = Line([x0, 1.65, 0], [x0 + 6.4, 1.65, 0], color=GOLD, stroke_width=14)
        la = T("CheY: seconds", 24, GOLD).next_to(bar_a, RIGHT, buff=0.3)
        lb = T("other responders: minutes or more", 24, GOLD).move_to([x0 + 3.2, 1.1, 0])
        ns = T("not to scale", 22, GREY).move_to([5.2, 2.55, 0])
        self.at("labile")
        lab = T("labile", 28, GOLD, weight=BOLD).move_to([1.6, 2.55, 0])
        self.play(FadeIn(lab, scale=0.8), run_time=0.4)

        self.at("How long it lasts")
        self.play(FadeOut(lab), run_time=0.2)
        self.play(Create(bar_a), run_time=0.5)
        self.play(Create(bar_b), FadeIn(ns), run_time=0.9)
        self.at("seconds for")
        self.play(FadeIn(la), run_time=0.4)
        self.at("minutes or more")
        self.play(FadeIn(lb), run_time=0.4)
        for bar in (bar_a, bar_b):
            drop = pbadge(0.2).move_to(bar.get_end())
            self.play(FadeIn(drop, scale=0.5), run_time=0.15)
            self.play(drop.animate.shift(DOWN * 0.4).set_opacity(0), run_time=0.4)
            self.remove(drop)

        # lane 2
        self.at("serine, threonine or tyrosine")
        p2 = pbadge().move_to(c2.get_corner(UR) + [0.05, 0.05, 0])
        self.play(FadeIn(n2), FadeIn(p2, scale=0.6), run_time=0.5)
        bar_c = Line([x0, -1.2, 0], [x0 + 5.8, -1.2, 0], color=GOLD, stroke_width=14)
        lc = T("stays", 26, GOLD).move_to([x0 + 2.9, -1.8, 0])
        self.at("stays until")
        self.play(Create(bar_c), FadeIn(lc), run_time=1.3)
        ph = bchip("phosphatase", RED, 26).move_to([5.0, -3.0, 0])
        self.at("a phosphatase")
        self.play(FadeIn(ph), run_time=0.3)
        self.play(ph.animate.move_to([5.0, -1.2, 0]), run_time=0.7)
        end_b = pbadge(0.2).move_to(bar_c.get_end())
        self.at("removes it")
        self.play(FadeIn(end_b, scale=0.5), run_time=0.2)
        self.play(end_b.animate.shift(UP * 0.5).set_opacity(0), p2.animate.shift(UP * 0.5).set_opacity(0), run_time=0.6)
        self.remove(end_b)

        self.at("off separately from on")
        on_t = T("on", 28, GREEN, weight=BOLD).move_to([x0 + 0.1, -0.6, 0])
        off_t = T("off", 28, RED, weight=BOLD).move_to([5.0, -0.55, 0])
        self.play(FadeIn(on_t), FadeIn(off_t), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Reader(SpokenScene):
    def construct(self):
        # ---- beat A: a mark that stays can be read; the bacterial phosphate is not read ----
        LX, RX = -3.4, 3.4
        CY = -1.2
        ap = bchip("animal protein", ORANGE, 30).move_to([LX, CY, 0])
        yt = ap.get_top()[1]
        apb = pbadge(0.3).move_to([LX, yt + 0.38, 0])
        apl = T("phosphotyrosine", 26, GOLD).next_to(ap, DOWN, buff=0.3)

        self.at("Because that mark stays")
        self.play(FadeIn(ap), FadeIn(apb, scale=0.6), FadeIn(apl), run_time=0.8)

        R = 0.7
        base = yt + 0.18
        dm = dome(TEAL, r=R)
        dm.move_to([LX, base + (R - 0.18) / 2, 0])
        pchip = bchip("another protein", TEAL, 30)
        pchip.move_to([LX, base + R + 0.1 + pchip.height / 2, 0])
        sh2 = T("SH2 domain", 26, TEAL).move_to([LX + 2.2, base + 0.35, 0])
        partner = VGroup(dm, pchip, sh2).shift(UP * 1.8)
        self.at("another protein can")
        self.play(FadeIn(partner, shift=DOWN * 0.3), run_time=0.7)
        self.at("domain reads")
        self.play(partner.animate.shift(DOWN * 1.8), run_time=0.9)
        self.play(Indicate(apb, color=GOLD, scale_factor=1.3), run_time=0.4)

        self.at("In the bacterial relay")
        rp = bchip("responder", PURPLE, 30).move_to([RX, CY, 0])
        rpb = pbadge(0.3).move_to([RX, yt + 0.38, 0])
        rpl = T("phosphate on aspartate", 24, GOLD).next_to(rp, DOWN, buff=0.3)
        self.play(FadeIn(rp), FadeIn(rpb, scale=0.6), FadeIn(rpl), run_time=0.8)
        self.at("changes the responder")
        rp_new = bchip("responder", GREEN, 30).move_to(rp)
        self.play(Transform(rp, rp_new), run_time=0.7)
        nd = dome(RED, r=R, dashed=True).move_to([RX, base + 0.6 + (R - 0.18) / 2, 0])
        c0 = nd.get_center()
        cross = VGroup(Line(c0 + [-0.5, 0.45, 0], c0 + [0.5, -0.35, 0], color=RED, stroke_width=8),
                       Line(c0 + [-0.5, -0.35, 0], c0 + [0.5, 0.45, 0], color=RED, stroke_width=8))
        nrl = T("no separate reader", 26, RED).move_to([RX, base + 0.6 + R + 0.5, 0])
        self.at("no separate domain")
        self.play(FadeIn(nd), Create(cross), FadeIn(nrl), run_time=0.8)

        # ---- beat B: one partner versus several pathways ----
        self.at("Most sensor kinases")
        gone = Group(*self.mobjects)
        self.play(FadeOut(gone), run_time=0.5)

        sen = bchip("sensor kinase", BLUE, 26).move_to([-4.5, 2.0, 0])
        main = bchip("partner", PURPLE, 26).move_to([0.2, 2.0, 0])
        o1 = bchip("responder", PURPLE, 24).move_to([4.4, 2.9, 0]).set_opacity(0.4)
        o2 = bchip("responder", PURPLE, 24).move_to([4.4, 1.1, 0]).set_opacity(0.4)
        self.play(FadeIn(sen), run_time=0.4)
        self.at("to one partner")
        a_main = arr(sen.get_right(), main.get_left(), GOLD, w=7)
        self.play(FadeIn(main), GrowArrow(a_main), run_time=0.7)
        self.at("largely ignore")
        d1 = DashedLine(sen.get_right() + UP * 0.1, o1.get_left(), color=GREY, stroke_width=2.5).set_opacity(0.6)
        d2 = DashedLine(sen.get_right() + DOWN * 0.1, o2.get_left(), color=GREY, stroke_width=2.5).set_opacity(0.6)
        ign = T("largely ignored", 22, GREY).move_to([4.4, 2.0, 0])
        self.play(FadeIn(o1), FadeIn(o2), Create(d1), Create(d2), FadeIn(ign), run_time=0.8)

        sep = DashedLine([-6.3, 0.35, 0], [6.3, 0.35, 0], color=GREY, stroke_width=2).set_opacity(0.6)
        rec = bchip("receptor", ORANGE, 26).move_to([-4.7, -1.4, 0])
        self.at("An animal receptor")
        self.play(FadeIn(sep), FadeIn(rec), run_time=0.6)
        rows = []
        ys = [-0.35, -1.4, -2.45]
        self.at("several pathways")
        for y in ys:
            ks = [bchip("kinase", ORANGE, 22, pad=0.16).move_to([x, y, 0]) for x in (-1.8, 1.5, 4.8)]
            arrs = [arr(rec.get_right(), ks[0].get_left(), ORANGE, w=4, tip=0.18)]
            arrs += [arr(ks[i].get_right(), ks[i + 1].get_left(), ORANGE, w=4, tip=0.18) for i in range(2)]
            rows.append((ks, arrs))
        self.play(*[AnimationGroup(FadeIn(ks[0]), GrowArrow(ar[0])) for ks, ar in rows], run_time=0.8)
        self.at("tiers of kinases")
        self.play(*[AnimationGroup(GrowArrow(ar[1]), FadeIn(ks[1]), GrowArrow(ar[2]), FadeIn(ks[2]),
                                   lag_ratio=0.5) for ks, ar in rows], run_time=1.1)
        idl = T("idealised: the numbers are for illustration", 22, GREY).move_to([0, -3.2, 0])
        self.play(FadeIn(idl), run_time=0.4)
        self.finish()


class S05End(EndCard):
    LINE = "A sensor, a gene switch, and one phosphate passed between them."
