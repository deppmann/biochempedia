"""Microbes: partner or pathogen?  (Biochemistrypedia high school Biology explainer)

COLOR MAP (one colour per concept, whole film)
  GREEN  = a helpful or quiet microbe (bacteria in nodules, decomposers, gut bacteria, E. coli in the gut)
  RED    = harm (pathogen, a strain causing illness)
  PURPLE = virus
  BLUE   = nitrogen and nutrients (nitrogen gas, ammonium, usable nitrogen, nitrogen and phosphorus in water)
  YELLOW = energy-rich food from the plant
  ORANGE = enzymes
  BROWN  = dead matter (fallen leaves, dead algae)
  PINK   = the pink inside of an active nodule
  WHITE  = the ocean alga and the "blocked" bar (neutral)
  GREY   = structure, outlines, fiber, de-emphasised
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
BROWN = "#A67C52"
PINK = "#F28DB2"


def bchip(text, color=BLUE, size=28, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def dot(color=GREEN, r=0.14, at=ORIGIN):
    return Circle(radius=r, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=0.85).move_to(at)


def scatter(n, cx, cy, w, h, seed=1, gap=0.42):
    rng = np.random.default_rng(seed)
    pts = []
    tries = 0
    while len(pts) < n and tries < 5000:
        tries += 1
        p = np.array([cx + (rng.random() - 0.5) * w, cy + (rng.random() - 0.5) * h, 0])
        if all(np.linalg.norm(p - q) > gap for q in pts):
            pts.append(p)
    return pts


def leaf_pile(cx, cy, scale=1.0, seed=3):
    rng = np.random.default_rng(seed)
    g = VGroup()
    for i in range(9):
        x = cx + (rng.random() - 0.5) * 2.0 * scale
        y = cy + (rng.random() - 0.5) * 0.9 * scale
        e = Ellipse(width=0.95 * scale, height=0.4 * scale, stroke_color=BROWN, stroke_width=2,
                    fill_color=BROWN, fill_opacity=0.55).rotate(rng.random() * PI).move_to([x, y, 0])
        g.add(e)
    return g


class S00Title(TitleCard):
    LESSON = "Microbes in Bodies and Ecosystems"
    TITLE = "Microbes: Partner or Pathogen?"


# ---------------------------------------------------------------------------------------------
class S01Bumps(SpokenScene):
    def construct(self):
        root = RoundedRectangle(corner_radius=0.12, width=11.0, height=0.34, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.4).move_to([0, 2.2, 0])
        root_l = T("soybean root", 30, GREY).move_to([-4.2, 2.95, 0])
        nod_pos = [-3.6, 0.0, 3.6]
        nods = VGroup(*[Circle(radius=0.7, stroke_color=GREY, stroke_width=3, fill_color=BROWN, fill_opacity=0.45)
                        .move_to([x, 1.4, 0]) for x in nod_pos])
        self.at("Dig up a soybean plant")
        self.play(FadeIn(root, shift=UP * 0.2), FadeIn(root_l), run_time=0.7)
        self.at("small round bumps")
        self.play(LaggedStart(*[GrowFromCenter(n) for n in nods], lag_ratio=0.25), run_time=0.9)
        nlab = T("bumps", 28, TEXT).move_to([3.6, 0.45, 0])
        self.play(FadeIn(nlab), run_time=0.4)

        self.at("Cut one open")
        mid = nods[1]
        center = np.array([0.0, -0.7, 0.0])
        up = Sector(radius=1.55, angle=PI, start_angle=0, arc_center=center, stroke_color=GREY, stroke_width=3,
                    fill_color=BROWN, fill_opacity=0.45)
        low = Sector(radius=1.55, angle=PI, start_angle=PI, arc_center=center, stroke_color=GREY, stroke_width=3,
                     fill_color=BROWN, fill_opacity=0.45)
        whole = Circle(radius=1.55, stroke_color=GREY, stroke_width=3, fill_color=BROWN, fill_opacity=0.45).move_to(center)
        self.play(FadeOut(nods[0]), FadeOut(nods[2]), FadeOut(nlab),
                  ReplacementTransform(mid, whole), run_time=0.8)
        cut = Line([-1.9, -0.7, 0], [1.9, -0.7, 0], color=TEXT, stroke_width=4)
        self.play(Create(cut), run_time=0.4)
        self.remove(whole)
        self.add(up, low)
        self.play(up.animate.shift(UP * 0.12), low.animate.shift(DOWN * 0.12), FadeOut(cut), run_time=0.5)
        self.at("pink inside")
        pink_l = T("often pink inside\nwhen active", 28, PINK).move_to([4.7, -0.7, 0])
        pa = arr([3.1, -0.7, 0], [1.9, -0.7, 0], PINK)
        self.play(up.animate.set_fill(PINK, 0.6), low.animate.set_fill(PINK, 0.6), FadeIn(pink_l), GrowArrow(pa), run_time=0.7)
        self.at("packed with bacteria")
        pts = scatter(16, 0.0, -0.7, 2.3, 2.0, seed=4, gap=0.4)
        pts = [p for p in pts if np.linalg.norm(p - center) < 1.25 and abs(p[1] - center[1]) > 0.2][:12]
        dots = VGroup(*[dot(GREEN, 0.14, p + (UP * 0.12 if p[1] > center[1] else DOWN * 0.12)) for p in pts])
        bl = T("bacteria", 30, GREEN).move_to([-4.3, -0.7, 0])
        ba = arr([-3.2, -0.7, 0], [-1.7, -0.7, 0], GREEN)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.06), FadeIn(bl), GrowArrow(ba), run_time=1.0)

        self.at("next to the word germs")
        allg = VGroup(root, root_l, up, low, dots, bl, ba, pa, pink_l)
        self.play(FadeOut(allg), run_time=0.6)
        germ = bchip("germs", RED, 40).move_to([-3.3, -0.4, 0])
        part = bchip("partners", GREEN, 40).move_to([3.3, -0.4, 0])
        q = T("?", 64, TEXT, weight=BOLD).move_to([0, -0.4, 0])
        self.play(FadeIn(germ, shift=RIGHT * 0.3), FadeIn(q), run_time=0.6)
        self.play(FadeIn(part, shift=LEFT * 0.3), run_time=0.5)
        self.at("always harmful")
        qt = T("Are bacteria and viruses always harmful?", 38, TEXT, font=TITLE_FONT)
        fit(qt, max_w=12.0)
        qt.move_to([0, 2.0, 0])
        self.play(Write(qt), run_time=1.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Fixation(SpokenScene):
    def construct(self):
        living = bchip("living things", GREY, 28).move_to([-4.2, 2.6, 0])
        prot = bchip("proteins and DNA", BLUE, 28).move_to([3.4, 2.6, 0])
        use = arr([-2.6, 2.6, 0], [1.6, 2.6, 0], GREY)
        use_l = T("use nitrogen to build", 24, GREY).move_to([-0.5, 3.15, 0])
        self.at("Living things use")
        self.play(FadeIn(living, shift=RIGHT * 0.2), run_time=0.5)
        self.at("build proteins")
        self.play(GrowArrow(use), FadeIn(use_l), FadeIn(prot, shift=LEFT * 0.2), run_time=0.8)

        gas = bchip("nitrogen gas", BLUE, 30).move_to([-4.6, -0.3, 0])
        air = T("in the air", 24, GREY).next_to(gas, DOWN, buff=0.2)
        self.at("mostly nitrogen gas")
        self.play(FadeIn(gas, scale=0.9), FadeIn(air), run_time=0.6)

        pa = bchip("plants and animals", GREY, 28).move_to([4.2, -0.3, 0])
        line = DashedLine([-2.9, -0.3, 0], [2.0, -0.3, 0], color=GREY, stroke_width=4)
        block = VGroup(Line([0, -0.6, 0], [0, 0.0, 0], color=TEXT, stroke_width=7))
        block.move_to([-0.2, -0.3, 0])
        self.at("cannot use it")
        self.play(Create(line), FadeIn(pa), run_time=0.6)
        self.play(FadeIn(block, scale=0.6), run_time=0.3)
        no = T("cannot use it in that form", 24, GREY).move_to([-0.2, -1.0, 0])
        self.play(FadeIn(no), run_time=0.3)

        self.at("Nitrogen fixation")
        bact = bchip("bacteria", GREEN, 30).move_to([0, -0.3, 0])
        usable = bchip("usable nitrogen", BLUE, 30).move_to([4.2, -0.3, 0])
        a1 = arr([-3.0, -0.3, 0], [-1.35, -0.3, 0], GREEN)
        a2 = arr([1.35, -0.3, 0], [2.65, -0.3, 0], GREEN)
        self.play(FadeOut(VGroup(line, block, no)), ReplacementTransform(pa, usable), FadeIn(bact, scale=0.9),
                  GrowArrow(a1), GrowArrow(a2), run_time=1.0)
        fix = T("nitrogen fixation", 40, TEXT, weight=BOLD).move_to([0, -2.4, 0])
        self.play(Write(fix), run_time=0.8)
        self.at("form living things can use")
        up_a = arr([4.2, 0.2, 0], [3.9, 2.05, 0], BLUE)
        self.play(GrowArrow(up_a), Indicate(usable, color=BLUE, scale_factor=1.08), run_time=0.9)
        self.at("Only some bacteria")
        only = T("only some bacteria and archaea can do this", 26, GREEN).move_to([0, -3.3, 0])
        self.play(FadeIn(only, shift=UP * 0.1), Indicate(bact, color=GREEN, scale_factor=1.12), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Nodule(SpokenScene):
    def construct(self):
        c = np.array([-1.3, -0.3, 0.0])
        root = RoundedRectangle(corner_radius=0.12, width=8.0, height=0.34, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.4).move_to([-1.4, 1.45, 0])
        root_l = T("root", 28, GREY).move_to([-5.0, 2.2, 0])
        nod = Circle(radius=1.6, stroke_color=GREY, stroke_width=3, fill_color=PINK, fill_opacity=0.35).move_to(c)
        pts = [p for p in scatter(20, c[0], c[1], 2.4, 2.4, seed=7, gap=0.5) if np.linalg.norm(p - c) < 1.25][:10]
        dots = VGroup(*[dot(GREEN, 0.15, p) for p in pts])
        nod_l = T("nodule", 30, TEXT).move_to([c[0], -2.45, 0])
        self.at("inside a nodule")
        self.play(GrowFromCenter(nod), LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.08), run_time=1.0)
        self.play(FadeIn(nod_l), run_time=0.3)
        self.at("small swelling on a root")
        self.play(FadeIn(root, shift=DOWN * 0.15), FadeIn(root_l), run_time=0.7)

        gas = bchip("nitrogen gas", BLUE, 28).move_to([-5.45, -0.3, 0])
        ain = arr([-4.2, -0.3, 0], [-2.95, -0.3, 0], BLUE)
        self.at("turn nitrogen gas")
        self.play(FadeIn(gas, shift=RIGHT * 0.2), GrowArrow(ain), run_time=0.7)
        aout = arr([0.45, 0.5, 0], [4.7, 0.5, 0], BLUE)
        amm = T("ammonium", 28, BLUE).move_to([2.55, 0.95, 0])
        self.at("into ammonium")
        self.play(GrowArrow(aout), FadeIn(amm), run_time=0.7)
        plant = bchip("plant", GREY, 28).move_to([5.55, 0.5, 0])
        self.at("plant uses it")
        self.play(FadeIn(plant, shift=LEFT * 0.2), run_time=0.5)

        fin = arr([4.7, -0.9, 0], [0.45, -0.9, 0], YELLOW)
        food = T("energy-rich food", 28, YELLOW).move_to([2.55, -1.4, 0])
        photo = T("made by photosynthesis", 22, GREY).move_to([2.55, -1.85, 0])
        self.at("sends the bacteria")
        self.play(GrowArrow(fin), FadeIn(food), run_time=0.7)
        self.at("from photosynthesis")
        self.play(FadeIn(photo), run_time=0.4)
        self.at("both species benefit")
        self.play(Indicate(aout, color=BLUE), Indicate(fin, color=YELLOW), run_time=1.0)
        self.at("mutualism")
        mut = T("mutualism: both benefit", 38, TEXT, weight=BOLD).move_to([0.6, -3.15, 0])
        self.play(Write(mut), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Decay(SpokenScene):
    def construct(self):
        pile = leaf_pile(-4.6, -0.9)
        pile_l = T("fallen leaves", 28, BROWN).move_to([-4.6, -2.35, 0])
        self.at("stream full of fallen leaves")
        self.play(LaggedStart(*[FadeIn(e, shift=DOWN * 0.3) for e in pile], lag_ratio=0.1), FadeIn(pile_l), run_time=1.0)

        dec = bchip("decomposer", GREEN, 30).move_to([-4.6, 2.9, 0])
        dsub = T("dead plants, animals, wastes", 22, BROWN).move_to([-4.6, -2.85, 0])
        d_a = arr([-4.6, 2.35, 0], [-4.6, 0.3, 0], GREEN)
        self.at("A decomposer")
        self.play(FadeIn(dec, shift=DOWN * 0.2), run_time=0.5)
        self.at("breaks down dead plants")
        self.play(GrowArrow(d_a), FadeIn(dsub), run_time=0.8)

        bac = bchip("bacteria", GREEN, 24).move_to([-6.0, 1.45, 0])
        fun = bchip("fungi", GREEN, 24).move_to([-3.3, 1.45, 0])
        self.at("Bacteria and fungi")
        self.play(FadeOut(d_a), FadeIn(bac, shift=UP * 0.2), FadeIn(fun, shift=UP * 0.2), run_time=0.7)

        enz = bchip("enzymes", ORANGE, 28).move_to([-0.8, 1.7, 0])
        large = VGroup(RoundedRectangle(corner_radius=0.1, width=3.0, height=1.0, stroke_color=BROWN, stroke_width=3,
                                        fill_color=BROWN, fill_opacity=0.5),
                       T("large molecules", 24, TEXT)).move_to([-0.8, -0.9, 0])
        large[1].move_to(large[0])
        e_a = arr([-0.8, 1.15, 0], [-0.8, -0.3, 0], ORANGE)
        p_a = arr([-3.2, -0.9, 0], [-2.45, -0.9, 0], GREY)
        self.at("release enzymes")
        self.play(FadeIn(enz, shift=DOWN * 0.2), FadeIn(large), GrowArrow(p_a), GrowArrow(e_a), run_time=0.9)
        small = VGroup(*[Square(0.45, stroke_color=BROWN, stroke_width=3, fill_color=BROWN, fill_opacity=0.5)
                         .move_to([2.1 + 0.62 * k, -0.9, 0]) for k in range(3)])
        small_l = T("smaller molecules", 24, TEXT).move_to([2.7, -1.6, 0])
        s_a = arr([0.8, -0.9, 0], [1.6, -0.9, 0], ORANGE)
        self.at("into smaller ones")
        self.play(GrowArrow(s_a), ReplacementTransform(large[0].copy(), small), FadeIn(small_l), run_time=0.9)

        nut = bchip("nutrients", BLUE, 28).move_to([5.0, 0.5, 0])
        sw = bchip("soil or water", GREY, 26).move_to([5.0, -2.6, 0])
        n_a = arr([4.1, -0.9, 0], [4.6, -0.1, 0], BLUE)
        n_b = arr([5.0, 0.0, 0], [5.0, -2.0, 0], BLUE)
        self.at("The nutrients return")
        self.play(FadeIn(nut), GrowArrow(n_a), run_time=0.5)
        self.play(GrowArrow(n_b), FadeIn(sw), run_time=0.6)

        self.at("Without decomposers")
        keep = VGroup(pile, pile_l)
        gone = VGroup(dec, dsub, bac, fun, enz, large, e_a, p_a, s_a, small, small_l, nut, sw, n_a, n_b)
        self.play(FadeOut(gone), run_time=0.6)
        self.play(keep.animate.scale(1.5).move_to([0, 0.1, 0]), run_time=0.7)
        self.at("pile up")
        piled = leaf_pile(0.0, 0.6, scale=1.8, seed=9)
        self.play(LaggedStart(*[FadeIn(e, shift=DOWN * 0.3) for e in piled], lag_ratio=0.08), run_time=0.8)
        self.at("stay locked inside")
        lock = bchip("nutrients stay locked inside", BLUE, 30).move_to([0, -2.5, 0])
        self.play(FadeIn(lock, shift=UP * 0.2), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Gut(SpokenScene):
    def construct(self):
        box = RoundedRectangle(corner_radius=0.5, width=8.0, height=3.6, stroke_color=GREY, stroke_width=4)\
            .move_to([0.8, -0.3, 0])
        box_l = T("your gut", 28, GREY).move_to([0.8, 1.85, 0])
        pts = scatter(34, 0.8, -0.3, 7.0, 2.8, seed=11, gap=0.5)
        dots = VGroup(*[dot(GREEN, 0.14, p) for p in pts])
        self.at("Your gut holds")
        self.play(Create(box), FadeIn(box_l), run_time=0.6)
        self.at("trillions of bacteria")
        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.03), run_time=1.0)
        micro = bchip("microbiome", GREEN, 32).move_to([0.8, 2.85, 0])
        self.at("microbiome")
        self.play(FadeOut(box_l), FadeIn(micro, shift=DOWN * 0.15), run_time=0.5)

        fiber = bchip("fiber", GREY, 28).move_to([-5.7, -0.3, 0])
        f_a = arr([-4.85, -0.3, 0], [-3.1, -0.3, 0], GREY)
        self.at("break down fiber")
        self.play(FadeIn(fiber, shift=RIGHT * 0.2), GrowArrow(f_a), run_time=0.7)
        self.play(LaggedStart(*[Indicate(d, color=GREEN, scale_factor=1.6) for d in dots[::2]], lag_ratio=0.04), run_time=0.8)
        self.at("fermentation")
        ferm = T("fermentation", 34, TEXT, weight=BOLD).move_to([0.8, -2.8, 0])
        self.play(Write(ferm), run_time=0.7)
        self.at("without oxygen")
        ox = T("works without oxygen", 26, GREY).move_to([0.8, -3.3, 0])
        self.play(FadeIn(ox), run_time=0.4)

        # --- pathogen and host
        self.at("A pathogen")
        self.play(FadeOut(VGroup(box, dots, micro, fiber, f_a, ferm, ox)), run_time=0.6)
        path = bchip("pathogen", RED, 34).move_to([-3.9, 0.4, 0])
        host = bchip("host", GREY, 34).move_to([3.9, 0.4, 0])
        cd = arr([-2.4, 0.4, 0], [2.7, 0.4, 0], RED)
        cd_l = T("causes disease", 28, RED).move_to([0.15, 0.95, 0])
        self.play(FadeIn(path, shift=RIGHT * 0.2), run_time=0.5)
        self.at("causes disease")
        self.play(GrowArrow(cd), FadeIn(cd_l), run_time=0.6)
        self.at("its host")
        self.play(FadeIn(host, shift=LEFT * 0.2), run_time=0.5)
        self.at("lives in or on")
        hl = T("the living thing it lives in or on", 26, GREY).move_to([3.0, -0.7, 0])
        self.play(FadeIn(hl), run_time=0.5)

        # --- E. coli
        self.at("Most strains")
        self.play(FadeOut(VGroup(path, host, cd, cd_l, hl)), run_time=0.6)
        gb = RoundedRectangle(corner_radius=0.4, width=5.2, height=3.2, stroke_color=GREY, stroke_width=4).move_to([-3.4, 0.0, 0])
        gb_l = T("large intestine", 26, GREY).move_to([-3.4, 1.85, 0])
        ec = dot(GREEN, 0.2, [-3.4, -0.1, 0])
        ec_l = T("E. coli", 28, GREEN).move_to([-3.4, -0.9, 0])
        self.play(Create(gb), FadeIn(gb_l), GrowFromCenter(ec), FadeIn(ec_l), run_time=0.8)
        self.at("quietly")
        q = T("quiet", 28, GREEN).move_to([-3.4, 0.75, 0])
        self.play(FadeIn(q), run_time=0.4)
        self.at("Other strains")
        strain = dot(RED, 0.2, [0.2, 0.0, 0])
        s_l = T("other E. coli strains", 26, RED).move_to([1.0, 0.9, 0])
        self.play(FadeIn(strain), FadeOut(q), run_time=0.3)
        self.play(strain.animate.move_to([1.0, 0.0, 0]), FadeIn(s_l), run_time=0.5)
        self.at("cause illness")
        ill = T("illness", 32, RED, weight=BOLD).move_to([1.0, -0.8, 0])
        self.play(FadeIn(ill, shift=UP * 0.1), Indicate(strain, color=RED, scale_factor=1.5), run_time=0.8)
        self.at("food or water")
        fb = RoundedRectangle(corner_radius=0.4, width=4.0, height=3.2, stroke_color=GREY, stroke_width=4).move_to([4.2, 0.0, 0])
        fb_l = T("food or water", 26, GREY).move_to([4.2, 1.85, 0])
        self.play(Create(fb), FadeIn(fb_l), strain.animate.move_to([4.2, 0.0, 0]), FadeOut(s_l),
                  ill.animate.move_to([4.2, -0.9, 0]), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        self.at("Viruses matter too")
        vir = bchip("virus", PURPLE, 36).move_to([-3.5, 0.4, 0])
        self.play(FadeIn(vir, scale=0.9), run_time=0.5)
        self.at("bacteriophage")
        phage = bchip("bacteriophage", PURPLE, 36).move_to([-3.5, 0.4, 0])
        self.play(ReplacementTransform(vir, phage), run_time=0.6)
        self.at("infects bacteria")
        bdots = VGroup(*[dot(GREEN, 0.18, p) for p in scatter(5, 3.7, 0.4, 1.8, 1.4, seed=2, gap=0.55)])
        bl = T("bacteria", 30, GREEN).move_to([3.7, -0.9, 0])
        ia = arr([-1.5, 0.4, 0], [2.4, 0.4, 0], PURPLE)
        dl = T("a virus that infects bacteria", 26, GREY).move_to([0, -1.9, 0])
        self.play(GrowArrow(ia), LaggedStart(*[GrowFromCenter(d) for d in bdots], lag_ratio=0.1), FadeIn(bl), FadeIn(dl), run_time=0.9)

        self.at("lab model ecosystem")
        self.play(FadeOut(VGroup(phage, ia, bdots, bl, dl)), run_time=0.6)
        water = RoundedRectangle(corner_radius=0.2, width=11.6, height=1.8, stroke_color=BLUE, stroke_width=3,
                                 fill_color=BLUE, fill_opacity=0.08).move_to([0, -1.8, 0])
        wl = T("water", 24, BLUE).move_to([-5.2, -1.15, 0])
        self.play(Create(water), FadeIn(wl), run_time=0.6)
        self.at("a virus infected")
        v = bchip("virus", PURPLE, 26).move_to([-4.2, 1.2, 0])
        self.play(FadeIn(v, shift=RIGHT * 0.2), run_time=0.5)
        self.at("ocean alga")
        alga = Circle(radius=0.85, stroke_color=TEXT, stroke_width=4, fill_color=TEXT, fill_opacity=0.25).move_to([0, 1.2, 0])
        al = T("ocean alga", 28, TEXT).next_to(alga, UP, buff=0.2)
        va = arr([-3.3, 1.2, 0], [-0.95, 1.2, 0], PURPLE)
        self.play(GrowFromCenter(alga), FadeIn(al), GrowArrow(va), run_time=0.7)
        self.at("Bacteria then")
        dead = T("dead algae", 28, BROWN).move_to([0, 2.45, 0])
        self.play(alga.animate.set_stroke(BROWN).set_fill(BROWN, 0.5), ReplacementTransform(al, dead), FadeOut(VGroup(v, va)), run_time=0.7)
        bs = VGroup(*[dot(GREEN, 0.15, [x, y, 0]) for x, y in [(-1.2, 1.7), (1.2, 1.7), (-1.3, 0.7), (1.3, 0.7)]])
        self.at("broke down")
        self.play(LaggedStart(*[GrowFromCenter(b) for b in bs], lag_ratio=0.1), alga.animate.scale(0.5).set_fill(BROWN, 0.2), run_time=1.0)
        n = bchip("nitrogen", BLUE, 28).move_to([-1.9, -1.85, 0])
        p = bchip("phosphorus", BLUE, 28).move_to([1.9, -1.85, 0])
        self.at("nitrogen and phosphorus")
        self.play(FadeIn(n, shift=DOWN * 0.3), FadeIn(p, shift=DOWN * 0.3), run_time=0.8)
        self.at("other living things")
        ol = T("for other living things to use", 26, BLUE).move_to([0, -3.2, 0])
        self.play(FadeIn(ol), run_time=0.5)

        self.at("always harmful")
        self.play(FadeOut(VGroup(water, wl, alga, dead, bs, n, p, ol)), run_time=0.6)
        qt = T("Are bacteria and viruses always harmful?", 38, TEXT, font=TITLE_FONT)
        fit(qt, max_w=12.0)
        qt.move_to([0, 2.5, 0])
        self.play(Write(qt), run_time=1.0)
        self.at("Now")
        no = T("No.", 80, TEXT, weight=BOLD, font=TITLE_FONT).move_to([0, 0.9, 0])
        self.play(FadeIn(no, scale=0.8), run_time=0.4)
        self.at("which microbe")
        c1 = bchip("which microbe it is", GREEN, 34).move_to([-3.3, -1.0, 0])
        self.play(FadeIn(c1, shift=UP * 0.2), run_time=0.5)
        self.at("where it lives")
        c2 = bchip("where it lives", BLUE, 34).move_to([3.3, -1.0, 0])
        plus = T("and", 30, GREY).move_to([0, -1.0, 0])
        self.play(FadeIn(plus), FadeIn(c2, shift=UP * 0.2), run_time=0.5)
        self.finish()


class S07End(EndCard):
    LINE = "Helps or harms depends on which microbe, and where it lives."
