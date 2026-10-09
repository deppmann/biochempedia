"""Fat, two carbons at a time: the three stages of fatty acid degradation (Biochemistrypedia fatty-acid-degradation explainer)

Four narrated slide clips, one arc: fat is released and unpacked in three stages (s01) -> an activated
fatty acid cannot cross the inner mitochondrial membrane without carnitine (s02) -> the chemistry happens
at the beta carbon, and every round hands out acetyl-CoA, NADH and FADH2 (s03) -> the energy ledger for
palmitate: -2 up front, +28 from the spiral, +80 from the acetyl-CoA, 106 net (s04).

COLOR MAP (one color per concept, whole video)
  BLUE   = the fatty acid / acyl group / the fatty-acid chain (the fuel)
  GREY   = glycerol, membranes, neutral labels, glucose label text
  GREEN  = acetyl-CoA (two-carbon product) and the ATP it earns through the citric acid cycle
  ORANGE = coenzyme A (the CoA tag)
  YELLOW = carnitine (the passport)
  PURPLE = enzymes (lipase, CPT I, CPT II, translocase)
  PINK   = reduced carriers NADH and FADH2 (and the ATP they earn)
  RED    = ATP spent (activation cost)
  GOLD   = one highlight at a time (the beta carbon, the checkpoint, the 106 total)
  TEXT   = glucose bars (neutral, the comparison)
No molecular structures are drawn: carbons are numbered tiles, enzymes and carriers are labelled chips, the
membranes are bands, and the ledger is a bar computed from the slide's own arithmetic (1.5 ATP per FADH2,
2.5 per NADH, 8 GTP + 24 NADH + 8 FADH2 from eight acetyl-CoA).
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

config.disable_caching = True

PURPLE = "#B58CE0"
ORANGE = "#E8903A"
PINK = "#E26AA8"
CARBON_LABELS = None


def tile(label="", color=BLUE, size=0.5, fs=22, fill=0.16, filled=False, stroke=3):
    sq = RoundedRectangle(corner_radius=0.08, width=size, height=size, stroke_color=color, stroke_width=stroke,
                          fill_color=color, fill_opacity=0.9 if filled else fill)
    if label:
        return VGroup(sq, M(label, fs, BG if filled else color).move_to(sq))
    return VGroup(sq)


def enz(text, size=24, w=None):
    """Enzyme chip: opaque dark purple so things can pass 'through' it (it sits above them)."""
    lab = T(text, size, PURPLE)
    box = RoundedRectangle(corner_radius=0.14, width=w or lab.width + 0.44, height=lab.height + 0.34,
                           stroke_color=PURPLE, stroke_width=2.5, fill_color="#2a2140", fill_opacity=1)
    g = VGroup(box, lab.move_to(box))
    g.set_z_index(5)
    return g


def acyl_coa(size=24):
    return VGroup(chip("acyl", BLUE, size=size, pad=0.14), chip("CoA", ORANGE, size=size, pad=0.14)).arrange(RIGHT, buff=0)


def acyl_carn(size=24):
    return VGroup(chip("acyl", BLUE, size=size, pad=0.14), chip("carnitine", YELLOW, size=size, pad=0.14)).arrange(RIGHT, buff=0)


def band(y, x0, x1, gap=None, h=0.3):
    """Membrane band from x0 to x1 (optionally with a gap [gx, gw] where an enzyme sits)."""
    def rect(a, b):
        return Rectangle(width=b - a, height=h, stroke_color=GREY, stroke_width=2, fill_color=GREY,
                         fill_opacity=0.32).move_to([(a + b) / 2, y, 0])
    if gap is None:
        return VGroup(rect(x0, x1))
    gx, gw = gap
    return VGroup(rect(x0, gx - gw / 2), rect(gx + gw / 2, x1))


def num(n):
    return str(n).replace("-", "−")


# =====================================================================================================
class S00Title(TitleCard):
    LESSON = "Fatty acid degradation"
    TITLE = "Fat, two carbons at a time"


# =====================================================================================================
class S01Stages(SpokenScene):
    """Three stages as a journey: adipocyte (release) -> blood -> mitochondrion (activate + import, degrade)."""

    def construct(self):
        A = np.array([-4.5, -0.2, 0.0])
        adip = Circle(radius=1.65, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.08).move_to(A)
        adip_lab = T("adipose tissue", 24, GREY).next_to(adip, DOWN, buff=0.22)

        # triacylglycerol: grey glycerol backbone + three blue fatty-acid bars (schematic blocks)
        back = RoundedRectangle(corner_radius=0.06, width=0.2, height=1.0, stroke_width=0, fill_color=GREY, fill_opacity=0.95)
        bars = VGroup(*[RoundedRectangle(corner_radius=0.06, width=1.0, height=0.2, stroke_width=0, fill_color=BLUE, fill_opacity=0.95)
                        for _ in range(3)])
        for i, b in enumerate(bars):
            b.move_to([0.6, 0.4 - 0.4 * i, 0])
        tag = VGroup(back, bars).move_to(A + np.array([0, 0.1, 0]))
        tag_lab = T("triacylglycerol", 24, GREY).move_to(A + np.array([0, -0.9, 0]))

        lipase = chip("lipase", PURPLE, size=26, pad=0.16).move_to(A + np.array([0, 1.0, 0]))

        # stage badges
        def badge(n, text, x):
            c = Circle(radius=0.27, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=1)
            nn = T(str(n), 26, BG, weight=BOLD).move_to(c)
            lab = T(text, 26, TEXT)
            g = VGroup(VGroup(c, nn), lab).arrange(RIGHT, buff=0.18)
            g.move_to([x, 2.85, 0])
            return g
        b1, b2, b3 = badge(1, "Release", -4.5), badge(2, "Activate + import", 0.7), badge(3, "Degrade", 4.5)

        # blood pipe
        pipe = VGroup(Line([-2.75, 0.4, 0], [1.9, 0.4, 0], color=GREY, stroke_width=3),
                      Line([-2.75, -0.6, 0], [1.9, -0.6, 0], color=GREY, stroke_width=3))
        blood = T("blood", 24, GREY).move_to([-0.4, -1.05, 0])

        # mitochondrion (schematic compartments)
        MC = np.array([4.2, -0.3, 0.0])
        mito = RoundedRectangle(corner_radius=0.6, width=4.0, height=4.0, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.06).move_to(MC)
        inner = RoundedRectangle(corner_radius=0.45, width=3.4, height=3.2, stroke_color=GREY, stroke_width=2,
                                 fill_opacity=0).move_to(MC)
        mito_lab = T("mitochondrion", 24, GREY).move_to(MC + np.array([0, 2.3, 0]))
        matrix_lab = T("matrix", 24, GREY).move_to(MC + np.array([0, 1.25, 0]))

        # pieces after hydrolysis
        gly = chip("glycerol", GREY, size=24, pad=0.14)
        fas = [chip("FA", BLUE, size=26, pad=0.14) for _ in range(3)]

        # ---------------------------------------------------------------- stage 1
        self.at("Before a fat can fuel anything")
        self.play(FadeIn(adip), FadeIn(adip_lab), FadeIn(tag), FadeIn(tag_lab), run_time=1.0)
        self.at("unpacked in three deliberate stages")
        self.play(Indicate(tag, color=BLUE, scale_factor=1.12), run_time=1.0)
        self.at("First,")
        self.play(FadeIn(b1, shift=DOWN * 0.15), run_time=0.6)
        self.at("hydrolyzed by lipase")
        self.play(FadeIn(lipase, shift=DOWN * 0.1), run_time=0.6)
        self.at("splitting each molecule")
        gly.move_to(A + np.array([-0.55, 0.2, 0]))
        for i, f in enumerate(fas):
            f.move_to(A + np.array([0.75, 0.65 - 0.6 * i, 0]))
        self.play(FadeOut(tag_lab), ReplacementTransform(back, gly),
                  *[ReplacementTransform(bars[i], fas[i]) for i in range(3)], FadeOut(lipase), run_time=1.5)
        pieces_cap = T("3 fatty acids + glycerol", 24, TEXT).move_to([-4.5, 1.95, 0])
        self.play(FadeIn(pieces_cap), run_time=0.5)
        self.at("which travel out into the blood")
        self.play(FadeOut(pieces_cap), Create(pipe), FadeIn(blood), run_time=0.8)
        tx = {0: -1.95, 1: -0.6, 2: 0.4, 3: 1.4}
        anims = [gly.animate.move_to([tx[0], -0.1, 0])]
        for i, f in enumerate(fas):
            anims.append(f.animate.move_to([tx[i + 1], -0.1, 0]))
        self.play(*anims, run_time=2.0)
        # ---------------------------------------------------------------- stage 2
        self.at("Second,")
        self.play(FadeIn(b2, shift=DOWN * 0.15), FadeIn(mito), FadeIn(inner), FadeIn(mito_lab), FadeIn(matrix_lab),
                  FadeOut(gly), FadeOut(fas[0]), FadeOut(fas[1]), FadeOut(pipe), FadeOut(blood), run_time=1.0)
        fa = fas[2]
        self.play(fa.animate.move_to([1.0, -0.1, 0]), run_time=0.6)
        self.at("activated")
        coa = chip("CoA", ORANGE, size=26, pad=0.14).next_to(fa, RIGHT, buff=0)
        self.play(FadeIn(coa, shift=LEFT * 0.2), run_time=0.6)
        grp = VGroup(fa, coa)
        self.at("shuttled across")
        self.play(grp.animate.move_to(MC + np.array([0, 0.65, 0])), run_time=1.6)
        # ---------------------------------------------------------------- stage 3
        self.at("Third,")
        self.play(FadeIn(b3, shift=DOWN * 0.15), run_time=0.6)
        self.at("dismantled")
        pairs = VGroup(*[VGroup(tile("", GREEN, 0.34, filled=True), tile("", GREEN, 0.34, filled=True)).arrange(RIGHT, buff=0.04)
                         for _ in range(3)]).arrange(RIGHT, buff=0.45).move_to(MC + np.array([0, 0.65, 0]))
        self.play(ReplacementTransform(grp, pairs), run_time=1.1)
        self.at("acetyl CoA units")
        acet_lab = T("acetyl-CoA", 24, GREEN).move_to(MC + np.array([0, 0.0, 0]))
        self.play(FadeIn(acet_lab), run_time=0.5)
        self.at("citric acid cycle")
        cyc = VGroup(Circle(radius=0.3, stroke_color=GREEN, stroke_width=4),
                     Triangle(color=GREEN, fill_opacity=1, stroke_width=0).scale(0.11).rotate(-PI / 2 - 0.4).move_to([0.3, 0.02, 0]))
        cyc.move_to(MC + np.array([-1.05, -0.85, 0]))
        cyc_lab = T("citric acid cycle", 22, GREEN).next_to(cyc, RIGHT, buff=0.2)
        self.play(FadeIn(cyc), FadeIn(cyc_lab), run_time=0.6)
        self.play(cyc.animate.rotate(-TAU), run_time=1.6, rate_func=linear)
        # roadmap recap
        self.at("Release,")
        self.play(Indicate(b1[0][0], color=GOLD, scale_factor=1.4), run_time=0.8)
        self.at("activation and import")
        self.play(Indicate(b2[0][0], color=GOLD, scale_factor=1.4), run_time=0.8)
        self.at("then degradation")
        self.play(Indicate(b3[0][0], color=GOLD, scale_factor=1.4), run_time=0.8)
        self.at("Everything that follows")
        self.play(*[Indicate(b[0], color=GOLD, scale_factor=1.12) for b in (b1, b2, b3)], run_time=1.2)
        self.finish()


# =====================================================================================================
class S02Shuttle(SpokenScene):
    """Carnitine passport: a cross-section of the two mitochondrial membranes."""

    def construct(self):
        X0, X1 = -3.4, 6.3
        Y_OUT, Y_IN = 1.1, -0.9
        G_CPT1, G_TR, G_CPT2 = -1.5, 0.9, 3.0
        outer = band(Y_OUT, X0, X1, gap=(G_CPT1, 1.5))
        inner = band(Y_IN, X0, X1, gap=(G_TR, 2.1))
        lab_cyt = T("cytosol", 24, GREY).move_to([-6.2 + 0.55, 2.35, 0])
        lab_out = T("outer\nmembrane", 22, GREY, line_spacing=0.6).move_to([-6.2 + 0.7, Y_OUT, 0])
        lab_ims = T("intermembrane\nspace", 22, GREY, line_spacing=0.6).move_to([-6.2 + 0.95, 0.1, 0])
        lab_inn = T("inner\nmembrane", 22, GREY, line_spacing=0.6).move_to([-6.2 + 0.7, Y_IN, 0])
        lab_mat = T("matrix", 24, GREY).move_to([-6.2 + 0.55, -2.4, 0])

        cpt1 = enz("CPT I").move_to([G_CPT1, Y_OUT, 0])
        tr = enz("translocase", 22).move_to([G_TR, Y_IN, 0])
        cpt2 = enz("CPT II").move_to([G_CPT2, Y_IN - 0.15, 0])
        cpt2.shift(DOWN * (cpt2.get_top()[1] - (Y_IN - 0.15)))  # hangs on the matrix face of the inner membrane

        def step_label(text):
            return T(text, 26, TEXT).move_to([1.6, 3.15, 0])

        # ---------------- the wall
        ac = acyl_coa().move_to([-1.2, 1.5, 0])
        inner_only = band(Y_IN, X0, X1)
        self.at("Activated fatty acids")
        self.play(FadeIn(ac, shift=DOWN * 0.1), run_time=0.6)
        self.at("face a wall")
        self.play(FadeIn(inner_only), FadeIn(lab_inn), FadeIn(lab_mat), run_time=0.8)
        self.at("Coenzyme A cannot cross")
        self.play(ac.animate.move_to([-1.2, -0.45, 0]), run_time=1.4)
        cross = VGroup(Line([-0.2, -0.2, 0], [0.2, 0.2, 0]), Line([-0.2, 0.2, 0], [0.2, -0.2, 0])).set_color(RED).set_stroke(width=7)
        cross.move_to([-1.2 + 1.35, -0.62, 0])
        self.play(FadeIn(cross, scale=1.5), ac.animate.shift(UP * 0.12), run_time=0.4)
        self.play(ac.animate.shift(RIGHT * 0.12), rate_func=there_and_back, run_time=0.3)
        # ---------------- passport
        self.at("needs a different passport")
        self.play(FadeOut(cross), FadeOut(ac[1]), Indicate(ac[0], color=BLUE, scale_factor=1.15), run_time=0.7)
        pp = chip("passport", YELLOW, size=24, pad=0.14, fill_opacity=0.0).next_to(ac[0], RIGHT, buff=0.15)
        self.at("passport")
        self.play(FadeIn(pp, shift=LEFT * 0.15), run_time=0.6)
        self.at("carnitine")
        carn_intro = chip("carnitine", YELLOW, size=24, pad=0.14).move_to(pp)
        self.play(FadeOut(pp), FadeIn(carn_intro), run_time=0.6)
        ac = VGroup(ac[0])
        self.wait(0.6)
        # ---------------- step 1: activation
        self.at("In step one")
        st = step_label("1  ·  activate in the cytosol")
        self.play(FadeOut(ac), FadeOut(carn_intro), FadeIn(st), FadeIn(outer), FadeIn(lab_cyt), FadeIn(lab_out), FadeIn(lab_ims),
                  run_time=0.9)
        fa = chip("fatty acid", BLUE, size=24, pad=0.14).move_to([-2.0, 2.2, 0])
        coa = chip("CoA", ORANGE, size=24, pad=0.14).move_to([-0.2, 2.2, 0])
        self.at("the fatty acid is activated")
        self.play(FadeIn(fa), FadeIn(coa), run_time=0.6)
        self.at("activated to acyl CoA")
        atp = T("ATP → AMP + PPi", 22, RED).move_to([-1.3, 1.6, 0])
        ac1 = acyl_coa().move_to([-1.3, 2.2, 0])
        self.play(ReplacementTransform(fa, ac1[0]), ReplacementTransform(coa, ac1[1]), FadeIn(atp), run_time=1.1)
        # ---------------- step 2: CPT I
        self.at("Then carnitine")
        st2 = step_label("2  ·  CPT I swaps CoA for carnitine")
        carn = chip("carnitine", YELLOW, size=24, pad=0.14).move_to([2.4, 2.2, 0])
        self.play(FadeOut(st), FadeIn(st2), FadeOut(atp), FadeIn(carn), FadeIn(cpt1), ac1.animate.move_to([G_CPT1, 2.0, 0]), run_time=1.3)
        st = st2
        self.at("swaps CoA for carnitine")
        self.play(ac1[1].animate.move_to([-3.3, 2.75, 0]), carn.animate.move_to([G_CPT1 + 0.9, 2.0, 0]), run_time=0.7)
        prod = acyl_carn().move_to([G_CPT1, 2.0, 0])
        self.play(ReplacementTransform(VGroup(ac1[0], carn), prod), run_time=0.5)
        self.at("acyl carnitine,")
        self.play(prod.animate.move_to([G_CPT1, 0.15, 0]), run_time=1.1)
        # ---------------- step 3: translocase
        self.at("which the translocase")
        st3 = step_label("3  ·  translocase carries it across")
        self.play(FadeOut(st), FadeIn(st3), FadeIn(tr), run_time=0.6)
        st = st3
        self.play(prod.animate.move_to([G_TR, 0.15, 0]), run_time=0.6)
        self.at("ferries")
        self.play(prod.animate.move_to([G_TR, -1.85, 0]), run_time=1.5)
        # ---------------- step 4: CPT II
        self.at("On the matrix side")
        st4 = step_label("4  ·  CPT II swaps back inside")
        self.play(FadeOut(st), FadeIn(st4), FadeIn(cpt2), FadeOut(ac1[1]), prod.animate.move_to([G_CPT2, -2.75, 0]), run_time=1.2)
        st = st4
        self.at("reverses the swap")
        coa2 = chip("CoA", ORANGE, size=24, pad=0.14).move_to([6.0 - 0.2, -2.75, 0])
        self.play(FadeIn(coa2), run_time=0.4)
        self.at("handing the acyl group back")
        # acyl-carnitine -> acyl-CoA + carnitine: carnitine steps aside, a fresh CoA takes its place
        carn_free = prod[1]
        self.play(carn_free.animate.move_to([G_CPT2 - 1.6, -2.2, 0]), run_time=0.6)
        self.play(coa2.animate.next_to(prod[0], RIGHT, buff=0), run_time=0.6)
        new_ac = VGroup(prod[0], coa2)
        self.at("beta oxidation can begin")
        arrow = Arrow(new_ac.get_right() + RIGHT * 0.15, new_ac.get_right() + RIGHT * 0.8, buff=0, color=TEXT, stroke_width=5, max_tip_length_to_length_ratio=0.5)
        boxl = T("β-oxidation", 24, TEXT).next_to(arrow, RIGHT, buff=0.12)
        self.play(GrowArrow(arrow), FadeIn(boxl), run_time=0.8)
        self.at("Carnitine itself is recycled")
        self.play(carn_free.animate.move_to([G_TR, -1.85, 0]), run_time=0.7)
        self.play(carn_free.animate.move_to([G_TR, 0.15, 0]), run_time=0.9)
        self.play(carn_free.animate.move_to([2.4, 2.2, 0]), run_time=1.0)
        # ---------------- checkpoint
        self.at("This shuttle is also the key")
        ring = SurroundingRectangle(cpt1, color=GOLD, buff=0.1, corner_radius=0.18, stroke_width=4)
        ck = T("regulatory checkpoint", 26, GOLD).move_to([G_CPT1 + 0.2, 2.6, 0])
        self.play(Create(ring), FadeOut(carn_free), FadeOut(st), FadeIn(ck), run_time=0.9)
        self.at("controlling fatty acid entry")
        ent = T("controls fatty acid entry", 24, GOLD).next_to(ck, DOWN, buff=0.12)
        self.play(FadeIn(ent), run_time=0.6)
        self.finish()


# =====================================================================================================
class S03Beta(SpokenScene):
    """Number the carbons, find the beta carbon, then one round's outputs."""

    def construct(self):
        title = T("β-oxidation", 52, font=TITLE_FONT).move_to([0, 3.0, 0])
        TY = 0.2
        xs = [-4.5, -2.8, -1.1]
        tl = [tile("", BLUE, 1.0, fill=0.18).move_to([x, TY, 0]) for x in xs]
        rest = RoundedRectangle(corner_radius=0.14, width=4.6, height=0.7, stroke_color=BLUE, stroke_width=3,
                                fill_color=BLUE, fill_opacity=0.18).move_to([2.9, TY, 0])
        rest_lab = T("rest of the chain", 24, BLUE).move_to(rest)
        carb_lab = T("carboxyl\ncarbon", 24, TEXT, line_spacing=0.6).move_to([xs[0], TY - 1.05, 0])
        alpha_lab = T("α carbon", 26, TEXT).move_to([xs[1], TY - 1.05, 0])
        beta_lab = T("β carbon", 26, GOLD).move_to([xs[2], TY - 1.05, 0])

        def nlab(n, i, color):
            return M(str(n), 32, color).move_to(tl[i])

        self.at("The name beta")
        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.8)
        self.at("where the chemistry happens")
        self.play(Indicate(title[0][0], color=GOLD, scale_factor=1.5), run_time=1.0)
        self.at("Number the carbon", lead=0.1)
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in tl], FadeIn(rest), FadeIn(rest_lab), lag_ratio=0.2), run_time=0.9)
        self.at("starting from the carboxyl")
        self.play(tl[0][0].animate.set_stroke(TEXT).set_fill(TEXT, 0.2), FadeIn(carb_lab), run_time=0.7)
        n1 = nlab(1, 0, TEXT)
        self.at("as carbon 1", lead=0.0)
        self.play(FadeIn(n1, scale=1.3), run_time=0.5)
        self.at("Carbon 2 is the alpha")
        n2 = nlab(2, 1, TEXT)
        self.play(tl[1][0].animate.set_stroke(TEXT).set_fill(TEXT, 0.2), FadeIn(n2, scale=1.3), FadeIn(alpha_lab), run_time=0.8)
        self.at("and carbon 3")
        n3 = nlab(3, 2, GOLD)
        self.play(tl[2][0].animate.set_stroke(GOLD).set_fill(GOLD, 0.25), FadeIn(n3, scale=1.3), FadeIn(beta_lab), run_time=0.8)
        self.at("attack and oxidize")
        halo = SurroundingRectangle(tl[2], color=GOLD, buff=0.14, corner_radius=0.18, stroke_width=5)
        self.play(Create(halo), run_time=0.7)
        self.at("converting it to a keto group", lead=0.1)
        keto = chip("keto group", GOLD, size=26, pad=0.16).move_to([xs[2], TY + 1.4, 0])
        stub = Line(keto.get_bottom(), tl[2].get_top() + UP * 0.14, color=GOLD, stroke_width=4)
        self.play(FadeIn(keto, shift=DOWN * 0.15), Create(stub), tl[2][0].animate.set_fill(GOLD, 0.9), n3.animate.set_color(BG), run_time=1.0)
        self.at("so the chain can be cleaved there", lead=0.0)
        cut = DashedLine([xs[1] + 0.85, TY + 0.75, 0], [xs[1] + 0.85, TY - 0.75, 0], color=GOLD, stroke_width=4)
        self.play(Create(cut), run_time=0.5)
        left = VGroup(tl[0], tl[1], n1, n2, carb_lab, alpha_lab)
        right = VGroup(tl[2], n3, rest, rest_lab, beta_lab, keto, stub, halo)
        gone = T("2 carbons leave", 24, GREEN).move_to([-3.65, TY + 1.4, 0])
        self.play(tl[0][0].animate.set_stroke(GREEN).set_fill(GREEN, 0.3), tl[1][0].animate.set_stroke(GREEN).set_fill(GREEN, 0.3),
                  FadeIn(gone), run_time=0.5)
        self.play(left.animate.shift(LEFT * 0.55), right.animate.shift(RIGHT * 0.55), run_time=0.8)
        # ----------------- delta notation
        self.at("The delta notation")
        self.play(*[FadeOut(m) for m in [left, right, cut, gone]], FadeOut(title), run_time=0.7)
        sub = T("delta notation: a companion convention", 28, GREY).move_to([0, 2.7, 0])
        row = VGroup(*[tile("", BLUE, 1.0, fill=0.18) for _ in range(4)]).arrange(RIGHT, buff=0.6).move_to([-0.5, 0.5, 0])
        rowN = VGroup(*[M(str(i + 1), 32, BLUE).move_to(row[i]) for i in range(4)])
        restn = T("···", 40, BLUE).next_to(row, RIGHT, buff=0.3)
        self.play(FadeIn(sub), FadeIn(row), FadeIn(rowN), FadeIn(restn), run_time=0.9)
        self.at("Delta N marks the first carbon")
        dn = M("Δⁿ", 44, GOLD).move_to([-3.3, 2.0, 0])
        dn_t = T("= first carbon of a double bond", 28, TEXT).next_to(dn, RIGHT, buff=0.25)
        self.play(FadeIn(dn), FadeIn(dn_t), run_time=0.8)
        self.at("delta 2 means a double bond between", lead=0.3)
        d2 = M("Δ²", 44, GOLD).move_to(dn)
        d2_t = T("= double bond between C2 and C3", 28, TEXT).next_to(d2, RIGHT, buff=0.25)
        x_a, x_b = row[1].get_left()[0] + 0.05, row[2].get_right()[0] - 0.05
        yb = row.get_bottom()[1] - 0.3
        br = VMobject(stroke_color=GOLD, stroke_width=5).set_points_as_corners(
            [[x_a, yb + 0.2, 0], [x_a, yb, 0], [x_b, yb, 0], [x_b, yb + 0.2, 0]])
        self.play(Transform(dn, d2), Transform(dn_t, d2_t), run_time=0.7)
        self.play(Create(br), row[1][0].animate.set_stroke(GOLD), row[2][0].animate.set_stroke(GOLD), run_time=0.9)
        # ----------------- one round's outputs
        self.at("Each round of oxidation", lead=0.25)
        self.play(*[FadeOut(m) for m in [sub, row, rowN, restn, dn, dn_t, br]], run_time=0.5)
        inp = chip("acyl-CoA", BLUE, size=28).move_to([-5.5, 0.4, 0])
        box = RoundedRectangle(corner_radius=0.2, width=2.2, height=1.6, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.1).move_to([-2.1, 0.4, 0])
        box_t = T("one round", 28, TEXT).move_to(box)
        a_in = Arrow(inp.get_right(), box.get_left(), buff=0.12, color=TEXT, stroke_width=5)
        self.play(FadeIn(inp), FadeIn(box), FadeIn(box_t), GrowArrow(a_in), run_time=0.7)
        outs_x, ys = 1.3, [1.9, 0.75, -0.4, -1.55]
        short = chip("acyl-CoA", BLUE, size=26).move_to([outs_x, ys[0], 0])
        short_t = T("2 carbons shorter", 24, GREY).next_to(short, RIGHT, buff=0.2)
        acet = chip("acetyl-CoA", GREEN, size=26).move_to([outs_x, ys[1], 0])
        nadh = chip("NADH", PINK, size=26).move_to([outs_x, ys[2], 0])
        fadh = chip("FADH₂", PINK, size=26).move_to([outs_x, ys[3], 0])

        def arr(c):
            return Arrow(box.get_right(), c.get_left(), buff=0.12, color=c[0].get_stroke_color(), stroke_width=4)
        self.at("generates")
        self.play(FadeIn(short, shift=RIGHT * 0.2), GrowArrow(arr(short)), FadeIn(short_t), run_time=0.7)
        self.at("acetyl CoA, along")
        self.play(FadeIn(acet, shift=RIGHT * 0.2), GrowArrow(arr(acet)), run_time=0.7)
        self.at("NADH")
        self.play(FadeIn(nadh, shift=RIGHT * 0.2), GrowArrow(arr(nadh)), run_time=0.6)
        self.at("FADH2")
        self.play(FadeIn(fadh, shift=RIGHT * 0.2), GrowArrow(arr(fadh)), run_time=0.6)
        loop = CurvedArrow([outs_x + 0.3, ys[0] + 0.4, 0], [-5.5, 1.0, 0], angle=PI / 6, color=BLUE, stroke_width=4)
        self.play(Create(loop), run_time=0.8)
        self.at("the energy currency")
        cur = T("the energy currency", 24, PINK).next_to(VGroup(nadh, fadh), RIGHT, buff=0.3)
        br2 = Brace(VGroup(nadh, fadh), direction=RIGHT, color=PINK, buff=0.1)
        cur.next_to(br2, RIGHT, buff=0.1)
        self.play(GrowFromCenter(br2), FadeIn(cur), Indicate(nadh, color=PINK), Indicate(fadh, color=PINK), run_time=1.0)
        self.finish()


# =====================================================================================================
class S04Ledger(SpokenScene):
    """Palmitate's ATP ledger as a bar: -2, +28, +80 -> 106; then per-carbon vs glucose."""

    def construct(self):
        # --------------------------- strip of 16 carbons
        PITCH = 0.5
        x_first = -5.75
        tiles = VGroup(*[tile("", BLUE, 0.42, fill=0.25, stroke=2).move_to([x_first + PITCH * i, 2.9, 0]) for i in range(16)])
        head = T("palmitate, 16 carbons", 26, BLUE).move_to([4.2, 2.9, 0])

        # --------------------------- ledger geometry
        X0 = -6.0
        S = 0.1   # units per ATP: -10 .. 110 -> 12 wide
        xv = lambda v: X0 + (v + 10) * S
        BY = -0.75
        axis = Line([xv(-10), BY - 0.45, 0], [xv(110), BY - 0.45, 0], color=GREY, stroke_width=2)
        ticks = VGroup(*[Line([xv(v), BY - 0.45, 0], [xv(v), BY - 0.55, 0], color=GREY, stroke_width=2) for v in (0, 50, 100)])
        tick_l = VGroup(*[M(str(v), 22, GREY).move_to([xv(v), BY - 0.82, 0]) for v in (0, 50, 100)])
        axis_t = T("ATP", 22, GREY).move_to([xv(110) - 0.2, BY - 0.82, 0])
        scaffold = VGroup(axis, ticks, tick_l, axis_t)

        a = ValueTracker(0)   # activation 0..1 -> -2
        p = ValueTracker(0)   # beta-oxidation carriers 0..1 -> +28 (7 FADH2 x1.5 + 7 NADH x2.5)
        g = ValueTracker(0)   # acetyl-CoA via citric acid cycle + oxphos 0..1 -> +80

        def total():
            return -2 * a.get_value() + 28 * p.get_value() + 80 * g.get_value()

        def seg(v0, v1, color):
            lo, hi = min(v0, v1), max(v0, v1)
            if hi - lo < 1e-3:
                return VMobject()
            return Rectangle(width=(hi - lo) * S, height=0.5, stroke_width=0, fill_color=color, fill_opacity=0.95
                             ).move_to([xv((lo + hi) / 2), BY, 0])

        red_seg = always_redraw(lambda: seg(0, -2 * a.get_value(), RED))
        pink_seg = always_redraw(lambda: seg(-2, -2 + 28 * p.get_value(), PINK))
        green_seg = always_redraw(lambda: seg(26, 26 + 80 * g.get_value(), GREEN))
        track = Rectangle(width=120 * S, height=0.5, stroke_color=GREY, stroke_width=1.5, fill_opacity=0).move_to([xv(50), BY, 0])
        zero = Line([xv(0), BY + 0.4, 0], [xv(0), BY - 0.4, 0], color=TEXT, stroke_width=2)

        tot_lab = T("running total", 24, GREY).move_to([-4.6, 0.55, 0])
        tot = always_redraw(lambda: M(f"{num(round(total()))} ATP", 40, TEXT).next_to(tot_lab, RIGHT, buff=0.3))
        cap_red = T("activation  −2", 24, RED).move_to([xv(-2) + 1.0, BY + 0.55, 0])
        cap_pink = T("7 FADH₂ + 7 NADH  +28", 24, PINK).move_to([xv(12), BY - 1.7, 0])
        cap_green = T("8 acetyl-CoA: cycle + oxphos  +80", 24, GREEN).move_to([xv(66) + 0.6, BY - 1.7, 0])

        # --------------------------- tallies
        cnt = {k: ValueTracker(0) for k in ("f", "n", "a")}
        fch = chip("FADH₂", PINK, size=26).move_to([-4.6, 1.5, 0])
        nch = chip("NADH", PINK, size=26).move_to([-1.2, 1.5, 0])
        ach = chip("acetyl-CoA", GREEN, size=26).move_to([2.2, 1.5, 0])
        fv = always_redraw(lambda: M(f"× {int(round(cnt['f'].get_value()))}", 30, PINK).next_to(fch, RIGHT, buff=0.2))
        nv = always_redraw(lambda: M(f"× {int(round(cnt['n'].get_value()))}", 30, PINK).next_to(nch, RIGHT, buff=0.2))
        av = always_redraw(lambda: M(f"× {int(round(cnt['a'].get_value()))}", 30, GREEN).next_to(ach, RIGHT, buff=0.2))

        # --------------------------- narration
        self.at("Let's tally")
        self.add(red_seg, pink_seg, green_seg)
        self.play(FadeIn(scaffold), Create(track), FadeIn(zero), run_time=0.9)
        self.at("palmitate,")
        self.play(FadeIn(head), run_time=0.6)
        self.at("16 carbon", lead=0.0)
        self.play(LaggedStart(*[FadeIn(t, scale=0.6) for t in tiles], lag_ratio=0.08), run_time=1.6)
        self.at("Activation costs")
        self.play(FadeIn(tot_lab), run_time=0.4)
        self.add(tot)
        self.play(FadeIn(cap_red), a.animate.set_value(1), run_time=1.3)
        self.at("minus 2")
        self.play(Indicate(tot, color=RED, scale_factor=1.15), run_time=0.8)

        # seven rounds peel two carbons off the carboxyl end each
        pairs = [VGroup(tiles[2 * i], tiles[2 * i + 1]) for i in range(8)]
        self.at("Seven rounds")
        self.play(FadeIn(fch), FadeIn(nch), FadeIn(ach), FadeIn(fv), FadeIn(nv), FadeIn(av), run_time=0.6)

        def peel(i, dur):
            anims = [pairs[i].animate.shift(DOWN * 0.55).set_stroke(GREEN).set_fill(GREEN, 0.9)]
            anims += [cnt["a"].animate.set_value(i + 1)]
            self.play(*anims, run_time=dur)

        self.at("of beta oxidation", lead=0.0)
        peel(0, 0.7)
        self.at("yield 1 FADH2", lead=0.0)
        self.play(cnt["f"].animate.set_value(1), Indicate(fch, color=PINK), run_time=0.6)
        self.at("and 1 NADH", lead=0.0)
        self.play(cnt["n"].animate.set_value(1), Indicate(nch, color=PINK), run_time=0.6)
        self.at("those seven rounds", lead=1.2)
        for i in range(1, 6):
            self.play(pairs[i].animate.shift(DOWN * 0.55).set_stroke(GREEN).set_fill(GREEN, 0.9),
                      cnt["a"].animate.set_value(i + 1), cnt["f"].animate.set_value(i + 1), cnt["n"].animate.set_value(i + 1),
                      run_time=0.4)
        # round 7 splits the last four carbons into TWO acetyl-CoA: 7 rounds, 8 acetyl-CoA
        self.at("produce eight")
        self.play(VGroup(pairs[6], pairs[7]).animate.shift(DOWN * 0.55).set_stroke(GREEN).set_fill(GREEN, 0.9),
                  cnt["a"].animate.set_value(8), cnt["f"].animate.set_value(7), cnt["n"].animate.set_value(7),
                  Indicate(ach, color=GREEN), run_time=0.8)
        # citric acid cycle -> oxphos
        self.at("Feed all eight")
        cyc = chip("citric acid cycle", GREEN, size=26).move_to([4.3, 0.35, 0])
        self.play(FadeIn(cyc, shift=DOWN * 0.15), run_time=0.7)
        self.at("run the reduced carriers")
        ox = chip("oxidative phosphorylation", PINK, size=24).move_to([3.7, 0.35, 0])
        self.play(Transform(cyc, ox), FadeIn(cap_pink), p.animate.set_value(1), run_time=1.0)
        self.at("oxidative phosphorylation")
        self.play(FadeIn(cap_green), g.animate.set_value(1), run_time=2.0)
        self.at("books close")
        self.play(Indicate(tot, color=GOLD, scale_factor=1.15), run_time=1.0)
        self.at("roughly 106")
        box = SurroundingRectangle(VGroup(tot_lab, tot), color=GOLD, buff=0.18, corner_radius=0.16, stroke_width=4)
        self.play(Create(box), tot.animate.set_color(GOLD), run_time=0.8)
        self.wait(0.6)

        # --------------------------- comparison with glucose
        self.at("Compare that to glucose", lead=0.4)
        for m in (red_seg, pink_seg, green_seg, tot, fv, nv, av):
            m.clear_updaters()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

        BX0, BY1, BY2 = -5.8, 0.75, -0.65
        head2 = T("ATP per molecule", 32, TEXT).move_to([0, 2.7, 0])
        scale_m = 0.085
        pal_bar = Rectangle(width=106 * scale_m, height=0.7, stroke_width=0, fill_color=BLUE, fill_opacity=0.95
                            ).move_to([BX0 + 106 * scale_m / 2, BY1, 0])
        glc_bar = Rectangle(width=32 * scale_m, height=0.7, stroke_width=0, fill_color=TEXT, fill_opacity=0.95
                            ).move_to([BX0 + 32 * scale_m / 2, BY2, 0])
        pal_name = T("palmitate (16 carbons)", 26, BLUE).move_to([BX0, BY1 + 0.7, 0]).align_to(BX0 * RIGHT, LEFT)
        glc_name = T("glucose (6 carbons)", 26, GREY).move_to([BX0, BY2 + 0.7, 0]).align_to(BX0 * RIGHT, LEFT)
        pal_val = M("106 ATP", 30, BLUE).next_to(pal_bar, RIGHT, buff=0.2)
        glc_val = M("32 ATP", 30, TEXT).next_to(glc_bar, RIGHT, buff=0.2)
        self.play(FadeIn(head2), FadeIn(pal_name), FadeIn(glc_name), FadeIn(pal_bar), FadeIn(pal_val), run_time=0.8)
        self.at("which nets around")
        self.play(GrowFromEdge(glc_bar, LEFT), run_time=1.0)
        self.play(FadeIn(glc_val), run_time=0.4)
        self.at("Per carbon")
        head3 = T("ATP per carbon", 32, TEXT).move_to([0, 2.7, 0])
        sc = 1.25
        pal2 = Rectangle(width=6.625 * sc, height=0.7, stroke_width=0, fill_color=BLUE, fill_opacity=0.95
                         ).move_to([BX0 + 6.625 * sc / 2, BY1, 0])
        glc2 = Rectangle(width=5.33 * sc, height=0.7, stroke_width=0, fill_color=TEXT, fill_opacity=0.95
                         ).move_to([BX0 + 5.33 * sc / 2, BY2, 0])
        pal_val2 = M("106 ÷ 16 = 6.6", 28, BLUE).next_to(pal2, RIGHT, buff=0.2)
        glc_val2 = M("32 ÷ 6 = 5.3", 28, TEXT).next_to(glc2, RIGHT, buff=0.2)
        self.play(Transform(head2, head3), Transform(pal_bar, pal2), Transform(glc_bar, glc2),
                  Transform(pal_val, pal_val2), Transform(glc_val, glc_val2), run_time=1.6)
        self.at("about 25")
        xa, xb = glc2.get_right()[0], pal2.get_right()[0]
        guide = DashedLine([xa, BY2 + 0.4, 0], [xa, BY1 + 0.55, 0], color=GOLD, stroke_width=3)
        dbl = DoubleArrow([xa, BY1 + 0.55, 0], [xb, BY1 + 0.55, 0], buff=0, color=GOLD, stroke_width=4, tip_length=0.18)
        more = T("about 25% more", 28, GOLD).next_to(dbl, UP, buff=0.12)
        # move palmitate name away from arrow (name sits above bar-left, arrow above bar-right)
        self.play(Create(guide), GrowFromCenter(dbl), FadeIn(more), run_time=1.0)
        self.at("That density")
        self.play(Indicate(VGroup(pal_bar, pal_val), color=BLUE, scale_factor=1.02), run_time=1.0)
        self.at("stores long")
        store = T("long-term energy store: fat", 30, BLUE).move_to([0, -2.2, 0])
        self.play(FadeIn(store), run_time=0.6)
        self.at("rather than carbohydrate")
        self.play(glc_bar.animate.set_opacity(0.3), glc_val.animate.set_opacity(0.3), glc_name.animate.set_opacity(0.4), run_time=0.8)
        self.finish()


# =====================================================================================================
class S05End(EndCard):
    LINE = "Palmitate nets about 106 ATP after the activation cost."
