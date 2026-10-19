"""Killing faster than microbes double: innate immunity as a race (Biochemistrypedia explainer)

Timed to the SPOKEN words (self.at cues). Everything drawn is a schematic block, circle or arrow;
the numbers are the lesson's illustrative worked problem (100 bacteria, doubling every 20 minutes,
constant rates, well-mixed wound), computed from N = N0 x [2 x (1 - k)]^n.

COLOR MAP (one color per concept, whole video)
  RED    = microbes: spores, bacteria, budding yeast, the no-defense line, "grows"
  BLUE   = defender cells: blood cells, phagocytes, macrophages, neutrophils, NK cells
  TEAL   = complement pieces (C3b, C3a, C5a, hole-making pieces)
  PURPLE = signals: interferon, mediators such as histamine
  ORANGE = lysosomes (digestive enzymes)
  GREY   = barriers, tissue, labels, axes
  GREEN  = cleared / killed / "shrinks" / the 75% line
  YELLOW = highlight, the 40% line
  GOLD   = the 50% threshold and the rule
  TEXT   = labels and equations
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CE0"
ORANGE = "#F2994A"
MIC, DEF, CMP, SIG, LYS, WALL, OK, HI, THR = RED, BLUE, TEAL, PURPLE, ORANGE, GREY, GREEN, YELLOW, GOLD


def arrow(a, b, color=TEXT, sw=6, tip=0.25, both=False):
    cls = DoubleArrow if both else Arrow
    return cls(np.array(a, dtype=float), np.array(b, dtype=float), buff=0, color=color, stroke_width=sw,
               max_tip_length_to_length_ratio=0.3, max_stroke_width_to_length_ratio=12, tip_length=tip)


def cell(x, y, r=0.5, color=DEF, op=0.25, sw=3):
    return Circle(radius=r, stroke_color=color, stroke_width=sw, fill_color=color, fill_opacity=op).move_to([x, y, 0])


def dot(x, y, r=0.15, color=MIC):
    return Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=1).move_to([x, y, 0])


def spore(x, y, ang=0.6, L=0.55):
    d = np.array([np.cos(ang), np.sin(ang), 0]) * L / 2
    c = np.array([x, y, 0.0])
    return Line(c - d, c + d, color=MIC, stroke_width=8)


def yeast(x, y):
    a = Circle(radius=0.28, stroke_color=MIC, stroke_width=3, fill_color=MIC, fill_opacity=0.35).move_to([x, y, 0])
    b = Circle(radius=0.15, stroke_color=MIC, stroke_width=3, fill_color=MIC, fill_opacity=0.35).move_to([x + 0.32, y + 0.18, 0])
    return VGroup(a, b)


class Sc(SpokenScene):
    def rt(self, f):
        return min(max(0.4, self.beat(f)), 1.1)


# ---------------------------------------------------------------- title / end
class S00Title(TitleCard):
    LESSON = "Innate Immunity"
    TITLE = "Killing Faster Than Microbes Double"


class S07End(EndCard):
    LINE = "In this model, defenses clear an infection only by killing over half per doubling time."


# ---------------------------------------------------------------- s01
class S01Flea(Sc):
    def construct(self):
        body = RoundedRectangle(corner_radius=0.5, width=9.0, height=4.2, stroke_color=TEXT, stroke_width=3,
                                fill_color=TEXT, fill_opacity=0.04).move_to([0, -0.2, 0])
        name = T("water flea, Daphnia", 34).move_to([0, 3.0, 0])
        self.play(Create(body), FadeIn(name), run_time=0.9)
        self.at("is transparent")
        tr = T("transparent: it can be watched alive", 26, WALL).move_to([0, -2.9, 0])
        self.play(FadeIn(tr, shift=UP * 0.1), body.animate.set_fill(TEXT, opacity=0.0), run_time=self.rt(0.05))
        self.at("its blood cells")
        c1, c2, c3 = cell(-3.2, -0.9), cell(0.2, 1.0), cell(3.6, -1.0)
        cl = T("blood cells", 28, DEF).move_to([-3.2, -1.75, 0])
        self.play(FadeIn(c1, scale=0.6), FadeIn(c2, scale=0.6), FadeIn(c3, scale=0.6), FadeIn(cl),
                  run_time=self.rt(0.05))
        self.at("invading yeast")
        s1, s2, s3 = spore(-1.8, 0.4, 0.5), spore(1.3, -0.8, 1.0), spore(2.8, 0.9, 0.3)
        sl = T("yeast spores", 28, MIC).move_to([1.3, -1.6, 0])
        self.play(FadeIn(s1, scale=0.5), FadeIn(s2, scale=0.5), FadeIn(s3, scale=0.5), FadeIn(sl),
                  run_time=self.rt(0.05))
        self.play(c1.animate.move_to([-2.2, 0.2, 0]), c2.animate.move_to([-1.2, 0.5, 0]),
                  c3.animate.move_to([2.5, 0.2, 0]), FadeOut(cl), run_time=0.6)
        self.play(s1.animate.move_to([-2.2, 0.2, 0]).scale(0.3), s2.animate.move_to([1.6, -0.5, 0]),
                  s3.animate.move_to(c3).scale(0.3), c2.animate.move_to([1.6, -0.5, 0]), FadeOut(sl), run_time=0.6)
        self.at("Where the cells destroyed")
        eaten = VGroup(s1, s3)
        self.play(FadeOut(eaten), FadeOut(s2), FadeOut(name), FadeOut(tr), run_time=0.4)
        grp = VGroup(body, c1, c2, c3)
        self.play(grp.animate.scale(0.68).move_to([-3.3, 0.3, 0]), run_time=self.rt(0.07))
        l1 = T("spores destroyed:\ninfection stops", 30, OK, line_spacing=0.8).move_to([-3.3, -1.75, 0])
        self.play(FadeIn(l1, shift=UP * 0.1), run_time=self.rt(0.04))
        self.at("Where spores grew")
        body2 = RoundedRectangle(corner_radius=0.3, width=6.12, height=2.86, stroke_color=TEXT, stroke_width=3,
                                 fill_color=TEXT, fill_opacity=0.0).move_to([3.4, 0.3, 0])
        ys = VGroup(*[yeast(3.4 + dx, 0.3 + dy) for dx, dy in
                      [(-2.0, 0.6), (-1.0, -0.7), (0.0, 0.7), (1.1, -0.6), (1.9, 0.5), (-0.6, 0.1), (0.7, 0.0)]])
        self.play(Create(body2), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(y, scale=0.5) for y in ys], lag_ratio=0.15), run_time=self.rt(0.1))
        l2 = T("budding yeast grows:\nthe flea dies", 30, MIC, line_spacing=0.8).move_to([3.4, -1.75, 0])
        self.play(FadeIn(l2, shift=UP * 0.1), run_time=self.rt(0.04))
        self.finish()


# ---------------------------------------------------------------- s02
class S02Walls(Sc):
    def construct(self):
        head = T("innate immunity", 44, TEXT).move_to([0, 2.7, 0])
        sub = T("ready before it meets a particular microbe", 30, WALL).move_to([0, 1.9, 0])
        self.play(FadeIn(head, shift=DOWN * 0.1), run_time=0.6)
        self.at("before an organism")
        self.play(FadeIn(sub), run_time=self.rt(0.05))
        self.at("In mammalian airways")
        self.play(FadeOut(head), FadeOut(sub), run_time=0.4)
        WX = -1.2
        top = Rectangle(width=0.5, height=2.5, stroke_width=0, fill_color=WALL, fill_opacity=0.9).move_to([WX, 1.55, 0])
        bot = Rectangle(width=0.5, height=2.5, stroke_width=0, fill_color=WALL, fill_opacity=0.9).move_to([WX, -1.55, 0])
        wall = VGroup(top, bot)
        wl = T("airway lining (mammal)", 26, WALL).move_to([WX, -3.25, 0])
        out = T("outside", 26, WALL).move_to([-4.6, 3.1, 0])
        inn = T("inside the body", 26, WALL).move_to([1.0, 3.1, 0])
        self.play(FadeIn(inn), GrowFromEdge(top, UP), GrowFromEdge(bot, DOWN), FadeIn(wl), FadeIn(out), run_time=0.7)
        self.at("mucus traps")
        mucus = Rectangle(width=1.2, height=5.6, stroke_width=0, fill_color=WALL, fill_opacity=0.25).move_to([WX - 0.85, 0, 0])
        ml = T("mucus", 26, WALL).move_to([WX - 0.85, 3.1, 0])
        mics = VGroup(*[dot(-4.0, y) for y in (1.6, 0.4, -1.1, 2.4)])
        self.play(FadeIn(mucus), FadeIn(ml), FadeIn(mics), run_time=0.5)
        self.play(*[m.animate.move_to([-2.1, m.get_y(), 0]) for m in mics], run_time=0.7)
        self.at("cilia carry")
        ticks = VGroup(*[Line([WX - 0.25, y, 0], [WX - 0.65, y + 0.12, 0], color=WALL, stroke_width=4)
                         for y in list(np.arange(-2.7, -0.4, 0.3)) + list(np.arange(0.6, 2.9, 0.3))])
        up = arrow([-3.2, -0.4, 0], [-3.2, 2.6, 0], color=TEXT)
        self.play(Create(ticks), GrowArrow(up), run_time=0.6)
        self.play(*[m.animate.shift(UP * 1.0).set_opacity(0.0) for m in mics if m.get_y() > 0],
                  *[m.animate.shift(UP * 1.0) for m in mics if m.get_y() <= 0], run_time=0.7)
        self.at("A microbe that gets through")
        m = dot(-2.1, 0.0, r=0.2)
        self.play(FadeIn(m, scale=0.5), run_time=0.2)
        self.play(m.animate.move_to([0.8, 0.0, 0]), run_time=0.9)
        ph = cell(3.6, 0.0, r=2.1, op=0.12)
        pl = T("phagocyte", 32, DEF).move_to([3.6, 2.65, 0])
        self.at("meets a phagocyte")
        self.play(FadeIn(ph, scale=0.8), FadeIn(pl), run_time=0.5)
        self.play(FadeOut(mucus), FadeOut(ticks), FadeOut(up), FadeOut(ml), FadeOut(out), FadeOut(wl),
                  FadeOut(wall), FadeOut(mics), FadeOut(inn), m.animate.move_to([3.0, 0.3, 0]), run_time=0.7)
        self.at("sits in a bubble")
        bub = Circle(radius=0.55, stroke_color=TEXT, stroke_width=3, fill_opacity=0).move_to(m)
        bl = T("phagosome", 26, TEXT).move_to([3.0, -0.65, 0])
        self.play(Create(bub), FadeIn(bl), run_time=self.rt(0.05))
        self.at("digestive enzymes")
        ly = VGroup(cell(4.8, 1.0, r=0.3, color=LYS, op=0.5), cell(4.8, -0.5, r=0.3, color=LYS, op=0.5))
        yl = T("lysosomes: sacs of digestive enzymes", 26, LYS).move_to([3.5, -2.65, 0])
        self.play(FadeIn(ly), FadeIn(yl), run_time=self.rt(0.05))
        self.at("fuse with it")
        self.play(*[l.animate.move_to(bub.get_center() + d) for l, d in zip(ly, [UP * 0.5 + RIGHT * 0.15, DOWN * 0.5 + RIGHT * 0.15])],
                  bub.animate.set_stroke(LYS).set_fill(LYS, opacity=0.2), run_time=self.rt(0.07))
        self.at("kill the microbe")
        self.play(m.animate.scale(0.2).set_opacity(0), run_time=self.rt(0.06))
        self.finish()


# ---------------------------------------------------------------- s03
class S03Three(Sc):
    def construct(self):
        mic = RoundedRectangle(corner_radius=0.6, width=4.4, height=2.4, stroke_color=MIC, stroke_width=4,
                               fill_color=MIC, fill_opacity=0.18).move_to([-2.4, -0.3, 0])
        ml = T("microbe", 30, MIC).move_to(mic)
        pl = T("in mammals", 30, WALL).move_to([0, 3.2, 0])
        self.play(FadeIn(pl), Create(mic), FadeIn(ml), run_time=0.8)
        self.at("Complement is a set")
        cl = T("complement: proteins in blood plasma", 30, CMP).move_to([0, 3.2, 0])
        c3 = chip("C3", CMP, size=34).move_to([-5.2, 1.8, 0])
        self.play(Transform(pl, cl), FadeIn(c3, scale=0.7), run_time=self.rt(0.06))
        self.at("is cut")
        c3b = chip("C3b", CMP, size=34).move_to([-4.4, 1.9, 0])
        c3a = chip("C3a", CMP, size=24, pad=0.12).move_to([-5.6, 2.7, 0])
        cut = Line([-5.2, 2.5, 0], [-5.2, 1.1, 0], color=TEXT, stroke_width=4)
        self.play(Create(cut), run_time=0.3)
        self.play(FadeOut(c3, scale=1.2), FadeIn(c3b), FadeIn(c3a), FadeOut(cut), run_time=self.rt(0.04))
        self.at("sticks to a microbe")
        tags = VGroup(*[chip("C3b", CMP, size=22, pad=0.1).move_to(p) for p in
                        ([0.2, 0.6, 0], [0.2, -0.3, 0], [0.2, -1.2, 0])])
        self.play(c3b.animate.move_to(tags[0]), run_time=self.rt(0.05))
        self.play(FadeIn(tags[1]), FadeIn(tags[2]), FadeOut(c3b), FadeIn(tags[0]), run_time=0.4)
        self.at("marks it for eating")
        ph = cell(5.0, -0.3, r=1.6, op=0.12)
        phl = T("phagocyte", 28, DEF).move_to([5.0, 1.75, 0])
        eat = T("marked for eating", 28, CMP).move_to([2.3, -2.4, 0])
        self.play(FadeIn(ph), FadeIn(phl), run_time=self.rt(0.04))
        self.play(ph.animate.move_to([2.3, -0.3, 0]), phl.animate.move_to([2.3, 1.75, 0]), FadeIn(eat),
                  run_time=0.8)
        self.at("drift away")
        c5a = chip("C5a", CMP, size=24, pad=0.12).move_to([-1.8, 0.95, 0])
        self.play(FadeIn(c5a, scale=0.7), c3a.animate.move_to([-3.2, 1.7, 0]), run_time=0.3)
        self.play(c3a.animate.move_to([-4.6, 2.5, 0]), c5a.animate.move_to([-2.2, 2.4, 0]), run_time=self.rt(0.05))
        infl = T("promote inflammation", 28, TEXT).move_to([-3.4, 3.2 - 0.0, 0])
        self.play(FadeOut(pl), FadeIn(infl), run_time=0.3)
        self.at("punch holes")
        hole = Rectangle(width=0.8, height=0.3, stroke_width=0, fill_color=BG, fill_opacity=1).move_to([-2.4, -1.5, 0])
        barrel = RoundedRectangle(corner_radius=0.1, width=1.1, height=0.55, stroke_color=CMP, stroke_width=4,
                                  fill_opacity=0).move_to([-2.4, -1.5, 0])
        hl = T("holes in susceptible microbes", 28, CMP).move_to([-2.4, -2.5, 0])
        self.play(FadeIn(hole), Create(barrel), FadeIn(hl), FadeOut(eat), run_time=self.rt(0.05))
        self.at("Interferons from")
        self.play(*[FadeOut(m) for m in [mic, ml, tags, ph, phl, c3a, c5a, infl, hole, barrel, hl]], run_time=0.5)
        # interferon (left half) and NK (right half)
        sep = DashedLine([0.2, -3.0, 0], [0.2, 3.0, 0], color=WALL, stroke_width=2)
        inf_c = cell(-5.0, 0.4, r=1.0, color=MIC, op=0.25)
        inf_l = T("virus-infected\ncell", 26, MIC, line_spacing=0.8).move_to([-5.0, -1.45, 0])
        nb_c = cell(-1.8, 0.4, r=1.0, color=DEF, op=0.12)
        nb_l = T("nearby cell", 26, DEF).move_to([-1.8, -1.45, 0])
        self.play(Create(sep), FadeIn(inf_c), FadeIn(inf_l), FadeIn(nb_c), FadeIn(nb_l), run_time=0.5)
        ifn = VGroup(*[dot(-3.9 + 0.1 * i, 0.4 + 0.2 * (i % 2 - 0.5), r=0.12, color=SIG) for i in range(3)])
        il = T("interferon", 28, SIG).move_to([-3.4, 1.9, 0])
        self.play(FadeIn(ifn), FadeIn(il), run_time=0.3)
        self.play(*[d.animate.shift(RIGHT * 1.0) for d in ifn], run_time=self.rt(0.05))
        av = T("antiviral state", 26, OK).move_to([-1.8, -2.3, 0])
        self.play(nb_c.animate.set_stroke(OK).set_fill(OK, opacity=0.25), FadeIn(av), run_time=self.rt(0.04))
        self.at("Natural killer cells")
        nk = cell(2.0, 0.4, r=1.0, color=DEF, op=0.3)
        nkl = T("natural\nkiller cell", 26, DEF, line_spacing=0.8).move_to([2.0, -1.45, 0])
        tg = cell(5.2, 0.4, r=1.0, color=MIC, op=0.25)
        tgl = T("infected or\nabnormal cell", 26, MIC, line_spacing=0.8).move_to([5.2, -1.45, 0])
        self.play(FadeIn(nk), FadeIn(nkl), FadeIn(tg), FadeIn(tgl), run_time=0.5)
        a = arrow([3.2, 0.4, 0], [4.0, 0.4, 0], color=DEF)
        self.play(GrowArrow(a), run_time=self.rt(0.05))
        self.play(tg.animate.set_stroke(opacity=0.35).set_fill(opacity=0.05), FadeOut(a), run_time=self.rt(0.05))
        self.finish()


# ---------------------------------------------------------------- s04
class S04Inflame(Sc):
    GX = -1.5

    def construct(self):
        tissue = Rectangle(width=12.4, height=4.6, stroke_color=WALL, stroke_width=2, fill_color=WALL,
                           fill_opacity=0.08).move_to([0, 0.95, 0])
        tl = T("tissue", 26, WALL).move_to([-5.7, 1.0, 0])
        gx = self.GX
        vtop_l = Line([-6.2, -1.4, 0], [gx - 0.3, -1.4, 0], color=WALL, stroke_width=6)
        vtop_r = Line([gx + 0.3, -1.4, 0], [6.2, -1.4, 0], color=WALL, stroke_width=6)
        vbot = Line([-6.2, -3.1, 0], [6.2, -3.1, 0], color=WALL, stroke_width=6)
        vl = T("small blood vessel", 26, WALL).move_to([4.2, -3.45, 0])
        self.play(FadeIn(tissue), Create(vtop_l), Create(vtop_r), Create(vbot), FadeIn(tl), FadeIn(vl), run_time=0.9)

        def lab(s, color=TEXT):
            return T(s, 36, color).move_to([-3.9, 2.6, 0])
        mac = cell(0.6, 1.8, r=0.6, op=0.3)
        bact = VGroup(*[dot(x, y, r=0.15) for x, y in [(4.1, 2.2), (4.6, 1.5), (4.0, 1.0), (4.9, 2.1)]])
        self.at("Resident cells such as")
        ml = T("macrophage", 24, DEF).move_to([0.6, 2.75, 0])
        self.play(FadeIn(mac, scale=0.7), FadeIn(ml), FadeIn(bact), run_time=0.6)
        s1 = lab("1  sensing")
        self.at("sense microbes")
        recs = VGroup(*[Line(mac.get_center() + 0.6 * np.array([np.cos(a), np.sin(a), 0]),
                             mac.get_center() + 0.9 * np.array([np.cos(a), np.sin(a), 0]), color=DEF, stroke_width=4)
                        for a in np.radians([0, 30, 60, 330, 300])])
        pr = T("pattern-recognition receptors", 24, DEF).move_to([1.5, 0.8, 0])
        self.play(FadeIn(s1), Create(recs), FadeIn(pr), run_time=0.7)
        self.at("Mediators such as")
        s2 = lab("2  leaky vessels")
        sig = VGroup(*[dot(x, -0.75, r=0.12, color=SIG) for x in (-4.4, -3.6, -2.8, -2.0)])
        mast = cell(-5.0, -0.75, r=0.3, color=SIG, op=0.4)
        mastl = T("mast cell", 24, SIG).move_to([-5.0, -0.2, 0])
        sl = T("histamine", 26, SIG).move_to([-3.2, -0.25, 0])
        self.play(Transform(s1, s2), FadeOut(pr), FadeIn(mast), FadeIn(mastl), FadeIn(sig), FadeIn(sl), run_time=0.7)
        self.at("widen small vessels")
        self.play(sig.animate.shift(DOWN * 0.45),
                  vtop_l.animate.put_start_and_end_on([-6.2, -1.4, 0], [gx - 1.2, -1.4, 0]),
                  vtop_r.animate.put_start_and_end_on([gx + 1.2, -1.4, 0], [6.2, -1.4, 0]),
                  run_time=0.9)
        self.at("Fluid and plasma proteins")
        s3 = lab("3  leak")
        fl = VGroup(*[dot(gx - 0.5 + 0.5 * i, -1.9, r=0.11, color=DEF) for i in range(3)])
        cp = chip("complement", CMP, size=22, pad=0.1).move_to([gx, -2.55, 0])
        self.play(Transform(s1, s3), FadeOut(sl), FadeOut(sig), FadeOut(mast), FadeOut(mastl), FadeIn(fl), FadeIn(cp), run_time=0.6)
        self.play(*[f.animate.move_to([gx + 0.6 + 0.35 * i, -0.5 - 0.3 * (i % 2)] + [0]) for i, f in enumerate(fl)],
                  cp.animate.move_to([-2.9, -0.6, 0]), run_time=1.0)
        self.at("Neutrophils squeeze")
        s4 = lab("4  recruitment")
        neu = VGroup(*[cell(x, -2.25, r=0.4) for x in (-4.4, -3.5)])
        nl = T("neutrophils", 24, DEF).move_to([-4.0, -3.45, 0])
        self.play(Transform(s1, s4), FadeIn(neu), FadeIn(nl), run_time=0.5)
        self.play(*[n.animate.move_to([gx + 0.0 * i, -1.4, 0]) for i, n in enumerate(neu)], run_time=0.7)
        self.play(neu[0].animate.move_to([3.3, 0.5, 0]), neu[1].animate.move_to([3.3, 1.8, 0]), FadeOut(nl),
                  run_time=1.2)
        nl2 = T("neutrophils", 24, DEF).move_to([4.9, 0.3, 0])
        self.play(FadeIn(nl2), run_time=0.3)
        self.at("monocytes follow")
        mono = VGroup(*[cell(x, -2.25, r=0.4, op=0.1) for x in (-0.6, 0.2)])
        mol = T("monocytes", 24, DEF).move_to([0.8, -3.45, 0])
        self.play(FadeIn(mono), FadeIn(mol), run_time=0.3)
        self.play(*[mo.animate.move_to([gx, -1.4, 0]) for mo in mono], run_time=0.5)
        self.play(mono[0].animate.move_to([2.3, -0.1, 0]), mono[1].animate.move_to([2.3, 1.0, 0]) , FadeOut(mol),
                  run_time=0.8)
        mol2 = T("monocytes", 24, DEF).move_to([2.3, -0.75, 0])
        self.play(FadeIn(mol2), run_time=0.3)
        self.at("Macrophages then clear")
        s5 = lab("5  repair")
        self.play(Transform(s1, s5), *[FadeOut(b, scale=0.3) for b in bact], run_time=0.8)
        self.at("tissue rebuilds")
        note = T("microbes and debris\ncleared; tissue rebuilds", 26, OK, line_spacing=0.8).move_to([-3.9, 1.5, 0])
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------- s05
def lg(v):
    return float(np.log10(v))


class S05Race(Sc):
    X0, X1, Y0, Y1 = -4.4, 3.0, -2.3, 2.3

    def P(self, n, val):
        return np.array([self.X0 + (self.X1 - self.X0) * n / 12, self.Y0 + (self.Y1 - self.Y0) * (lg(val) + 2) / 8, 0])

    def line(self, k, color):
        pts = [self.P(n, 100 * (2 * (1 - k)) ** n) for n in range(13)]
        return VMobject(stroke_color=color, stroke_width=6).set_points_as_corners(pts)

    def construct(self):
        top = T("illustrative numbers, not a measured infection", 28, WALL).move_to([0, 3.3, 0])
        self.play(FadeIn(top), run_time=0.5)
        self.at("illustrative")
        ax = VGroup(Line(self.P(0, 0.01), self.P(12, 0.01), color=WALL, stroke_width=3),
                    Line(self.P(0, 0.01), self.P(0, 1e6), color=WALL, stroke_width=3))
        yt = VGroup(*[VGroup(Line(self.P(0, v) + LEFT * 0.08, self.P(0, v) + RIGHT * 0.08, color=WALL, stroke_width=3),
                             T(s, 22, WALL).next_to(self.P(0, v), LEFT, buff=0.15))
                      for v, s in ((0.01, "0.01"), (1, "1"), (100, "100"), (1e4, "10,000"), (1e6, "1,000,000"))])
        xt = VGroup(*[T(str(h), 22, WALL).move_to(self.P(3 * h, 0.01) + DOWN * 0.35) for h in range(5)])
        xl = T("hours since the bacteria entered", 24, WALL).move_to([-0.8, -3.15, 0])
        yl = T("bacteria (log scale)", 24, WALL).move_to([-3.3, 2.75, 0])
        self.play(Create(ax), FadeIn(yt), FadeIn(xt), FadeIn(xl), FadeIn(yl), run_time=self.rt(0.08))
        self.at("bacteria enter a wound")
        start = Dot(self.P(0, 100), radius=0.12, color=TEXT)
        sl = T("start: 100", 24, TEXT).move_to(self.P(0, 100) + RIGHT * 1.0 + UP * 0.85)
        self.play(FadeIn(start, scale=0.5), FadeIn(sl), run_time=self.rt(0.04))
        self.at("no defense")
        l0 = self.line(0.0, MIC)
        e0 = VGroup(T("409,600", 28, MIC), T("no defense", 22, MIC)).arrange(DOWN, aligned_edge=LEFT, buff=0.05)
        e0.next_to(self.P(12, 409600), RIGHT, buff=0.2)
        self.play(Create(l0), run_time=self.rt(0.1))
        self.play(FadeIn(e0), run_time=0.3)
        self.at("each interval")
        l1 = self.line(0.75, OK)
        self.play(Create(l1), run_time=self.rt(0.1))
        self.at("infection is cleared")
        e1 = VGroup(T("about 0.024", 28, OK), T("75% killed", 22, OK)).arrange(DOWN, aligned_edge=LEFT, buff=0.05)
        e1.next_to(self.P(12, 100 * 0.5 ** 12), RIGHT, buff=0.2)
        m1 = T("multiplier 0.5", 24, OK).move_to(self.P(6, 100 * 0.5 ** 6) + LEFT * 0.1 + DOWN * 0.55)
        self.play(FadeIn(e1), FadeIn(m1), run_time=0.4)
        self.at("kill only")
        l2 = self.line(0.4, HI)
        self.play(Create(l2), run_time=self.rt(0.08))
        m2 = T("multiplier 1.2", 24, HI).move_to(self.P(8.5, 100 * 1.2 ** 8.5) + DOWN * 0.5)
        self.play(FadeIn(m2), run_time=0.3)
        self.at("still growing")
        e2 = VGroup(T("about 892", 28, HI), T("40% killed", 22, HI)).arrange(DOWN, aligned_edge=LEFT, buff=0.05)
        e2.next_to(self.P(12, 100 * 1.2 ** 12), RIGHT, buff=0.2)
        self.play(FadeIn(e2), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------- s06
class S06Rule(Sc):
    XA, XB, YA, YB = -4.2, 4.4, -1.6, 2.1     # k = 0..1 across, multiplier 0..2 up

    def Pt(self, k, m):
        return np.array([self.XA + (self.XB - self.XA) * k, self.YA + (self.YB - self.YA) * m / 2, 0])

    def construct(self):
        eq = M("N = N0 x [2 x (1 - k)]^n", 32, TEXT).move_to([0, 3.2, 0])
        self.play(FadeIn(eq, shift=DOWN * 0.1), run_time=0.6)
        self.at("constant rates")
        sub = T("k = fraction killed per doubling time", 24, WALL).move_to([0, 2.65, 0])
        self.play(FadeIn(sub), run_time=0.4)
        self.at("shrinks only if")
        P = self.Pt
        grow = Polygon(P(0, 1), P(1, 1), P(1, 2), P(0, 2), stroke_width=0, fill_color=MIC, fill_opacity=0.12)
        shr = Polygon(P(0, 0), P(1, 0), P(1, 1), P(0, 1), stroke_width=0, fill_color=OK, fill_opacity=0.12)
        ax = VGroup(Line(P(0, 0), P(1, 0), color=WALL, stroke_width=3), Line(P(0, 0), P(0, 2), color=WALL, stroke_width=3))
        xt = VGroup(*[T(f"{int(k * 100)}%", 22, WALL).move_to(P(k, 0) + DOWN * 0.3) for k in (0, 0.25, 0.5, 0.75, 1)])
        yt = VGroup(*[T(str(m), 22, WALL).next_to(P(0, m), LEFT, buff=0.15) for m in (0, 1, 2)])
        xl = T("fraction killed per doubling time", 24, WALL).move_to([0.1, -2.4, 0])
        yl = T("multiplier per interval", 24, WALL).rotate(PI / 2).move_to([-5.5, 0.25, 0])
        gl = T("grows", 30, MIC).move_to(P(0.82, 1.65))
        sl = T("shrinks", 30, OK).move_to(P(0.22, 0.4))
        self.play(FadeIn(grow), FadeIn(shr), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl),
                  FadeIn(gl), FadeIn(sl), run_time=self.rt(0.1))
        one = DashedLine(P(0, 1), P(1, 1), color=THR, stroke_width=4)
        curve = Line(P(0, 2), P(1, 0), color=TEXT, stroke_width=6)
        self.play(Create(curve), Create(one), run_time=self.rt(0.1))
        p40 = Dot(P(0.4, 1.2), radius=0.12, color=HI)
        p75 = Dot(P(0.75, 0.5), radius=0.12, color=OK)
        t40 = T("40%: 1.2", 24, HI).next_to(p40, UR, buff=0.1)
        t75 = T("75%: 0.5", 24, OK).next_to(p75, UR, buff=0.1)
        self.play(FadeIn(p40, scale=0.5), FadeIn(t40), FadeIn(p75, scale=0.5), FadeIn(t75), run_time=0.5)
        self.at("Keep one rule")
        v = DashedLine(P(0.5, 0), P(0.5, 1), color=THR, stroke_width=4)
        vt = T("50%", 28, THR).next_to(P(0.5, 0), DOWN, buff=0.12)
        vt.set_opacity(0)
        cross = Dot(P(0.5, 1), radius=0.14, color=THR)
        self.play(Create(v), FadeIn(cross, scale=0.4), xt[2].animate.set_color(THR), run_time=self.rt(0.08))
        self.at("kills more than half")
        rule = fit(T("in this model: kill more than half, each doubling time", 34, THR), max_w=12.0).move_to([0, -3.1, 0])
        self.play(FadeIn(rule, shift=UP * 0.1), run_time=self.rt(0.06))
        self.finish()
