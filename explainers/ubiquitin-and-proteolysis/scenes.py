"""Ubiquitin and regulated proteolysis: oxygen writes the destruction mark  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  TEAL   = HIF-1a, the protein that is made, tagged, destroyed or spared
  YELLOW = oxygen, the signal
  ENZ    = the prolyl hydroxylase, the enzyme that uses oxygen (a blue-violet)
  GOLD   = the mark: the degron, which for HIF-1a is a hydroxyl (the round "OH" badge)
  PURPLE = the tagging machinery: E1, E2, E3, and VHL with its cup that grips the mark
  PINK   = ubiquitin, the tag and its chain
  ORANGE = ARNT, the partner protein
  RED    = destruction (the proteasome, the drain, "destroyed")
  GREEN  = switched on (genes)
  GREY   = tank, DNA, other proteins, iron and 2-oxoglutarate, labels, anything absent or ruled out

No molecular structures: proteins are labelled chips, the mark is an "OH" badge (like a P badge), the
reading part of VHL and E3 is a cup that closes on the badge, the proteasome is a labelled barrel,
and the amount of HIF-1a is a tank with a level. The last plot is computed from dP/dt = s - kP:
flat when made and destroyed together, a straight rise once destruction stops (P = P0 + s t), and an
exponential fall back to the old level once it starts again.

Three framings, rebuilt where the story continues:
  TANK    (scenes 1 and 5)  the tank at the left, the rest of the frame for what acts on it.
  CLOSE-UP (scenes 2, 3, 4) the tagging machinery, the enzyme, the cup and the badge fill the frame.
  PLOT    (scene 6)         level against time, then the rule as a three-step chain.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
PINK = "#F08BB4"
ORANGE = "#F29E4C"
ENZ = "#6F8FFF"        # the prolyl hydroxylase (blue-violet, apart from the teal HIF-1a and the purple E3)

# the tank: walls at the left of the frame, a gap at the bottom for the drain
TK_X, TK_BOT, TK_TOP, TK_W = -4.3, -2.3, 1.5, 3.6
LVL_AIR, LVL_HIGH = 0.22, 0.92


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=26, pad=0.2, **kw):
    """chip with an opaque backing so lines drawn behind it do not show through. [back, box, label]"""
    c = chip(text, color, size=size, pad=pad, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def ghost_chip(text, size=22):
    """a dashed grey chip: something that is not part of the picture."""
    t = T(text, size, GREY)
    box = RoundedRectangle(corner_radius=0.14, width=t.width + 0.4, height=t.height + 0.32)
    return VGroup(DashedVMobject(box, num_dashes=max(18, int(box.width * 9))).set_color(GREY), t)


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def glow(*mobs, s=1.1, color=TEXT):
    """flash each mobject in place (one animation per mobject)."""
    return [Indicate(m, color=color, scale_factor=s) for m in mobs]


def pop(m, s=1.35):
    return m.animate(rate_func=there_and_back).scale(s)


def ohbadge(r=0.32):
    """the mark: a hydroxyl group, drawn like a phosphate badge."""
    c = Circle(radius=r, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=1)
    return VGroup(c, T("OH", 22, BG, weight=BOLD).move_to(c))


def o2dot(pos, r=0.3):
    pos = np.array([pos[0], pos[1], 0.0])
    c = Circle(radius=r, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.22).move_to(pos)
    return VGroup(c, T("O₂", 22, YELLOW).move_to(c))


def ubi(pos, r=0.17):
    """one ubiquitin."""
    return Circle(radius=r, stroke_width=0, fill_color=PINK, fill_opacity=1).move_to(pos)


def cup(center, opens, r_in=0.34, r_out=0.48, span=220, color=PURPLE):
    """the reading part of an E3: an arc that opens toward `opens` and closes on the mark."""
    phi = {"left": PI, "right": 0.0, "up": PI / 2, "down": -PI / 2}[opens]
    c = AnnularSector(inner_radius=r_in, outer_radius=r_out, angle=span * DEGREES,
                      start_angle=phi + PI - span * DEGREES / 2, color=color, fill_opacity=1, stroke_width=0)
    return c.shift(np.array(center, float))


def vhl_unit(cupc, size=32, label=True, r_in=0.42, r_out=0.58):
    """VHL: a chip with a cup on its left that opens toward the left. g.cp is the cup, g.body the chip."""
    cupc = np.array(cupc, float)
    cp = cup(cupc, "left", r_in, r_out, 220)
    body = bchip("VHL", PURPLE, size)
    body.next_to(cp, RIGHT, buff=-0.1)
    parts = [cp, body]
    if label:
        parts.append(T("part of an E3", 24, PURPLE).next_to(body, DOWN, buff=0.18))
    g = VGroup(*parts)
    g.cp, g.body = cp, body
    return g


def proteasome(center, w=3.6, h=1.2):
    body = RoundedRectangle(corner_radius=0.5, width=w, height=h, stroke_color=RED, stroke_width=5,
                            fill_color=RED, fill_opacity=0.14)
    rings = VGroup(*[Line([dx, -h / 2 + 0.1, 0], [dx, h / 2 - 0.1, 0], color=RED, stroke_width=3, stroke_opacity=0.6)
                     for dx in (-w * 0.2, 0.0, w * 0.2)])
    return VGroup(body, rings).move_to(center)


def crumble(center, n=9, color=TEAL, spread=1.1, seed=2):
    """a protein broken up: small dots that scatter and fade. Returns (dots, [animations])."""
    rng = np.random.RandomState(seed)
    c = np.array(center, float)
    dots = VGroup(*[Dot(c, radius=0.08, color=color) for _ in range(n)])
    moves = []
    for i, d in enumerate(dots):
        ang = TAU * i / n + rng.uniform(-0.3, 0.3)
        tgt = c + spread * rng.uniform(0.7, 1.3) * np.array([np.cos(ang), np.sin(ang) * 0.55, 0])
        moves.append(Succession(d.animate(run_time=0.7).move_to(tgt), FadeOut(d, run_time=0.4)))
    return dots, moves


def clock(center, r=0.45):
    center = np.array(center, float)
    face = Circle(radius=r, stroke_color=GREY, stroke_width=4).move_to(center)
    ticks = VGroup(*[Line(center + (r - 0.11) * v, center + r * v, color=GREY, stroke_width=4) for v in (UP, RIGHT, DOWN, LEFT)])
    hand = Line(center, center + UP * (r - 0.15), color=TEXT, stroke_width=5)
    pin = Dot(center, radius=0.05, color=TEXT)
    g = VGroup(face, ticks, hand, pin)
    g.hand, g.c = hand, center
    return g


# the tank ------------------------------------------------------------------------------------
def tank_walls():
    l, r = TK_X - TK_W / 2, TK_X + TK_W / 2
    a = VMobject().set_points_as_corners([[l, TK_TOP, 0], [l, TK_BOT, 0], [TK_X - 0.3, TK_BOT, 0]])
    b = VMobject().set_points_as_corners([[TK_X + 0.3, TK_BOT, 0], [r, TK_BOT, 0], [r, TK_TOP, 0]])
    return VGroup(a, b).set_stroke(GREY, 7).set_fill(opacity=0)


def tank_fill(f):
    """the standing amount of HIF-1a as a level, f from 0 to 1."""
    h = max(f, 0.001) * (TK_TOP - TK_BOT - 0.1)
    r = Rectangle(width=TK_W - 0.14, height=h, stroke_width=0, fill_color=TEAL, fill_opacity=0.55)
    return r.move_to([TK_X, TK_BOT + 0.03 + h / 2, 0])


def drops(n, top_y, bot_y, x, color=TEAL, rt=0.5, lag=0.35):
    """a stream of small dots falling from top_y to bot_y."""
    dots = [Dot([x + (0.14 if i % 2 else -0.14), top_y, 0], radius=0.1, color=color) for i in range(n)]
    anims = [Succession(FadeIn(d, run_time=0.05), d.animate(run_time=rt, rate_func=linear).move_to([d.get_center()[0], bot_y, 0]),
                        FadeOut(d, run_time=0.05)) for d in dots]
    return LaggedStart(*anims, lag_ratio=lag)


def tank_parts():
    """the chip, inflow arrow, drain arrow and labels that go with the tank. Returns a dict."""
    hif = bchip("HIF-1α", TEAL, 40).move_to([TK_X, 2.9, 0])
    inflow = arr([TK_X, 2.35, 0], [TK_X, TK_TOP + 0.1, 0], TEAL, w=7)
    made = T("made", 30, TEAL).next_to(inflow, RIGHT, buff=0.25)
    drain = arr([TK_X, TK_BOT - 0.05, 0], [TK_X, TK_BOT - 0.9, 0], RED, w=7)
    dest = T("destroyed", 30, RED).next_to(drain, RIGHT, buff=0.25)
    amount = T("amount\nin the cell", 26, GREY, line_spacing=0.8).move_to([TK_X + TK_W / 2 + 1.25, 0.55, 0])
    return dict(hif=hif, inflow=inflow, made=made, drain=drain, dest=dest, amount=amount)


class S00Title(TitleCard):
    LESSON = "Ubiquitin and Regulated Proteolysis as Signals"
    TITLE = "Oxygen writes the destruction mark"


# ---------------------------------------------------------------------------------------------
class S01Puzzle(SpokenScene):
    """a protein made and destroyed all the time: why? HIF-1a switches on the genes needed when oxygen is short. (TANK)"""

    def construct(self):
        walls = tank_walls()
        lvl = ValueTracker(0.0)
        fill = always_redraw(lambda: tank_fill(lvl.get_value()))
        self.add(fill)
        self.play(Create(walls), run_time=0.6)
        P = tank_parts()

        self.at("make a protein")
        self.play(FadeIn(P["hif"], shift=DOWN * 0.15), GrowArrow(P["inflow"]), FadeIn(P["made"]), FadeIn(P["amount"]), run_time=0.5)
        self.play(drops(7, 2.2, 0.4, TK_X), lvl.animate.set_value(0.32), run_time=2.0)

        o2s = VGroup(*[o2dot(p, 0.38) for p in [(2.6, 2.7), (3.8, 2.2), (5.0, 2.8), (5.5, 1.8), (3.7, 3.05)]])
        oxy = T("oxygen", 30, YELLOW).move_to([4.1, 1.35, 0])
        self.at("oxygen is around")
        self.play(LaggedStart(*[FadeIn(o, scale=0.6) for o in o2s], lag_ratio=0.15), FadeIn(oxy), run_time=0.9)

        self.at("destroy it")
        self.play(GrowArrow(P["drain"]), FadeIn(P["dest"]), drops(5, TK_BOT, TK_BOT - 0.9, TK_X, RED), lvl.animate.set_value(LVL_AIR), run_time=0.9)

        ck = clock([5.3, -0.1, 0], 0.6)
        mins = T("minutes", 28, GREY).move_to([5.3, -1.0, 0])
        self.at("within minutes")
        self.play(FadeIn(ck), FadeIn(mins), run_time=0.3)
        self.play(Rotate(ck.hand, -TAU / 5, about_point=ck.c), run_time=0.8)

        why = T("Why?", 80, TEXT, font=TITLE_FONT).move_to([2.5, 0.35, 0])
        self.at("Why build")
        self.play(Write(why), *glow(P["inflow"], s=1.15), *glow(P["drain"], s=1.15), run_time=1.0)
        self.at("throw it away")
        self.play(drops(4, 2.2, 0.4, TK_X), drops(4, TK_BOT, TK_BOT - 0.9, TK_X, RED), pop(why, 1.1), run_time=1.2)

        tf = T("a transcription factor", 30, TEAL).move_to([-0.7, 2.9, 0])
        self.at("transcription factor")
        self.play(FadeIn(tf, shift=RIGHT * 0.1), pop(P["hif"], 1.1), run_time=0.6)

        dna = Line([0.9, -2.25, 0], [6.2, -2.25, 0], color=GREY, stroke_width=7)
        gene = Rectangle(width=2.8, height=0.34, stroke_width=0, fill_color=GREY, fill_opacity=1).move_to([4.0, -2.25, 0])
        glab = T("genes", 30, GREY).move_to([4.0, -1.65, 0])
        sw = arr([-2.4, -0.5, 0], [2.35, -2.0, 0], GREY, w=6)
        swl = T("switches on genes", 28, GREY).move_to([-0.6, -1.75, 0])
        self.at("switches on the genes")
        self.play(Create(dna), FadeIn(gene), FadeIn(glab), GrowArrow(sw), FadeIn(swl), run_time=1.0)

        need = T("needed when oxygen runs short", 28, GREY).move_to([3.2, -2.9, 0])
        self.at("oxygen runs short")
        self.play(FadeIn(need, shift=UP * 0.1), *glow(gene, s=1.1), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Tag(SpokenScene):
    """ubiquitin passes E1 -> E2 -> E3; the E3 grips the target at its degron; the tagged protein goes to the proteasome. (CLOSE-UP)"""

    def construct(self):
        TX = 1.0
        tgt = bchip("target", GREY, 52).move_to([TX, -0.6, 0])
        self.at("destroys a protein")
        self.play(FadeIn(tgt, shift=UP * 0.15), run_time=0.5)

        ub = bchip("ubiquitin", PINK, 46).move_to([-4.3, 0.5, 0])
        small = T("a small protein", 30, GREY).next_to(ub, DOWN, buff=0.3)
        tagarr = arr(ub.get_right() + DOWN * 0.1, tgt.get_left() + UP * 0.2, PINK, w=6)
        tagl = T("tag", 32, PINK).next_to(tagarr, UP, buff=0.12)
        self.at("by tagging it")
        self.play(FadeIn(ub, shift=RIGHT * 0.15), GrowArrow(tagarr), FadeIn(tagl), run_time=0.7)
        self.at("a small protein")
        self.play(FadeIn(small), run_time=0.4)

        e1 = bchip("E1", PURPLE, 58).move_to([-4.9, 2.6, 0])
        e2 = bchip("E2", PURPLE, 58).move_to([-1.95, 2.6, 0])
        e3 = bchip("E3", PURPLE, 58).move_to([TX, 2.6, 0])
        c3 = cup([TX, 1.5, 0], "down", 0.4, 0.62, 220)
        e3g = VGroup(e3, c3)
        a12 = arr(e1.get_right(), e2.get_left(), PURPLE, w=6)
        a23 = arr(e2.get_right(), e3.get_left(), PURPLE, w=6)
        self.at("Three enzymes")
        self.play(FadeOut(tagarr), FadeOut(tagl), LaggedStart(FadeIn(e1, shift=DOWN * 0.2), FadeIn(e2, shift=DOWN * 0.2),
                                                           FadeIn(e3g, shift=DOWN * 0.2), lag_ratio=0.3), run_time=0.8)
        self.play(GrowArrow(a12), GrowArrow(a23), run_time=0.3)

        dot = ubi(ub.get_top() + UP * 0.05, 0.24)
        hop_y = e1.get_bottom()[1] - 0.3
        self.at("pass the")
        self.play(FadeIn(dot, scale=0.5), run_time=0.3)
        self.at("E1")
        self.play(dot.animate.move_to([e1.get_center()[0], hop_y, 0]), pop(e1, 1.12), run_time=0.7)
        self.at("E2")
        self.play(dot.animate.move_to([e2.get_center()[0], hop_y, 0]), pop(e2, 1.12), run_time=0.7)
        self.at("and E3")
        self.play(dot.animate.move_to([TX - 1.0, hop_y, 0]), pop(e3, 1.12), run_time=0.7)

        # the target rises into the E3's cup: the E3 binds it
        peg = RoundedRectangle(corner_radius=0.07, width=0.46, height=0.7, stroke_width=0, fill_color=GOLD, fill_opacity=1)
        peg.move_to(tgt.get_top() + UP * 0.35)
        rise = c3.get_center()[1] + 0.08 - peg.get_center()[1]
        tg = VGroup(tgt, peg)
        self.at("binds the target")
        self.play(GrowFromCenter(peg), run_time=0.3)
        self.play(tg.animate.shift(UP * rise), run_time=0.9)
        tag_pos = tgt.get_left() + LEFT * 0.35
        self.play(dot.animate.move_to(tag_pos), run_time=0.5)

        others = VGroup(ghost_chip("other protein", 28), ghost_chip("other protein", 28)).arrange(DOWN, buff=0.45).move_to([4.7, -0.25, 0])
        self.at("decides which")
        self.play(FadeIn(others), pop(e3, 1.1), run_time=0.8)

        deg = T("degron", 40, GOLD, weight=BOLD).move_to([TX + 3.2, 1.55, 0])
        dl = Line(deg.get_left() + LEFT * 0.05, peg.get_center() + RIGHT * 0.32, color=GOLD, stroke_width=3)
        self.at("reads")
        self.play(FadeIn(deg, shift=LEFT * 0.1), Create(dl), pop(peg, 1.5), run_time=0.8)
        self.at("a mark on")
        self.play(pop(peg, 1.6), run_time=0.5)
        self.at("tells the system")
        self.play(pop(peg, 1.8), run_time=0.6)

        PRC = np.array([0.0, -2.3, 0])
        pr = proteasome(PRC, w=4.8, h=1.6)
        prl = T("proteasome", 34, RED, weight=BOLD).move_to([4.5, -1.95, 0])
        prs = T("barrel-shaped\nprotease", 26, GREY).move_to([4.5, -2.8, 0])
        self.at("proteasome")
        self.play(FadeIn(pr, shift=UP * 0.2), FadeIn(prl), run_time=0.7)
        self.at("shaped protease")
        self.play(FadeIn(prs), run_time=0.4)

        dots, moves = crumble(PRC, 10, TEAL, 1.3)
        self.at("destroys the tagged")
        self.play(FadeOut(deg), FadeOut(dl), FadeOut(others), run_time=0.3)
        full = VGroup(tgt, peg, dot)
        self.play(full.animate.scale(0.5).move_to(PRC), run_time=0.9)
        self.add(dots)
        self.play(FadeOut(full, run_time=0.15), LaggedStart(*moves, lag_ratio=0.05), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Write(SpokenScene):
    """most proteins have no degron; a signal writes it. For HIF-1a the enzyme, with iron, 2-oxoglutarate and oxygen, hangs an OH on one proline. (CLOSE-UP)"""

    def construct(self):
        Y0, YI = -0.7, 2.15
        SITE = np.array([-0.4, Y0, 0])          # centre of the proline site (and of the OH that lands on it)
        CE = SITE + LEFT * 0.3                  # right edge of the protein chip
        gen = bchip("target", GREY, 54).next_to(CE, LEFT, buff=0)
        slot = DashedVMobject(Circle(radius=0.4), num_dashes=18).set_color(GOLD).move_to(SITE)
        nodeg = T("no degron yet", 32, GREY).move_to(SITE + DOWN * 1.15)
        self.at("Some proteins")
        self.play(FadeIn(gen, shift=UP * 0.15), run_time=0.5)
        self.play(Create(slot), FadeIn(nodeg), run_time=0.6)

        sig = bchip("signal", YELLOW, 42).move_to([-3.9, YI, 0])
        wr = arr(sig.get_bottom() + RIGHT * 0.6, SITE + UP * 0.45, YELLOW, w=6)
        self.at("A signal writes")
        self.play(FadeIn(sig, shift=DOWN * 0.15), GrowArrow(wr), run_time=0.7)

        hif = bchip("HIF-1α", TEAL, 54).next_to(CE, LEFT, buff=0)
        oxy = bchip("oxygen", YELLOW, 42).move_to([-3.9, YI, 0])
        self.at("the signal is")
        self.play(ReplacementTransform(gen, hif), ReplacementTransform(sig, oxy), FadeOut(wr), FadeOut(nodeg), run_time=0.8)

        phd = bchip("prolyl\nhydroxylase", ENZ, 38)
        phd.next_to(SITE + RIGHT * 0.4, RIGHT, buff=0.1)
        phd_final = phd.get_center().copy()
        phd.shift(RIGHT * 2.2)
        self.at("An enzyme called")
        self.play(FadeIn(phd, shift=LEFT * 0.2), run_time=0.6)
        self.play(phd.animate.move_to(phd_final), run_time=0.7)

        iron = bchip("iron", GREY, 40).move_to([-0.3, YI, 0])
        twox = bchip("2-oxoglutarate", GREY, 36).move_to([3.9, YI, 0])
        top = phd.get_top()
        a_iron = arr(iron.get_bottom(), top + LEFT * 0.7, GREY, w=6)
        a_twox = arr(twox.get_bottom() + LEFT * 0.4, top + RIGHT * 0.8, GREY, w=6)
        a_oxy = arr(oxy.get_bottom() + RIGHT * 0.7, top + LEFT * 1.3, YELLOW, w=6)
        self.at("needs iron")
        self.play(FadeIn(iron, shift=DOWN * 0.15), GrowArrow(a_iron), run_time=0.6)
        self.at("small molecule")
        self.play(FadeIn(twox, shift=DOWN * 0.15), GrowArrow(a_twox), run_time=0.6)
        self.at("one molecule of oxygen")
        self.play(GrowArrow(a_oxy), pop(oxy, 1.1), run_time=0.7)

        oh = ohbadge(0.4).move_to(SITE)
        self.at("adds a hydroxyl")
        self.play(FadeOut(slot), FadeIn(oh, scale=0.4), Flash(SITE, color=GOLD, line_length=0.35, flash_radius=0.55, num_lines=10), run_time=0.7)
        pro = T("one proline", 34, GREY).move_to(SITE + DOWN * 1.15)
        pl = Line(pro.get_top() + UP * 0.05, SITE + DOWN * 0.45, color=GREY, stroke_width=3)
        self.at("one proline")
        self.play(FadeIn(pro), Create(pl), run_time=0.5)

        degl = T("degron", 42, GOLD, weight=BOLD).move_to(SITE + DOWN * 1.15)
        self.at("That hydroxyl is")
        self.play(ReplacementTransform(pro, degl), pop(oh, 1.4), run_time=0.7)

        used = T("used up", 36, YELLOW).move_to([-3.9, YI, 0])
        self.at("the oxygen is used up")
        self.play(ReplacementTransform(oxy, used), FadeOut(a_oxy), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Read(SpokenScene):
    """VHL's cup closes on the OH badge; a plain proline cannot be gripped; the held HIF-1a gets a chain and goes to the proteasome. (CLOSE-UP)"""

    def construct(self):
        AY = 0.2
        R_B, R_IN, R_OUT = 0.55, 0.7, 0.98
        SA = np.array([-0.2, AY, 0])              # centre of the OH badge on the HIF-1a row
        hifA = bchip("HIF-1α", TEAL, 50).next_to(SA + LEFT * R_B, LEFT, buff=0)
        ohA = ohbadge(R_B).move_to(SA)
        vA = vhl_unit(SA + RIGHT * 2.8, size=54, r_in=R_IN, r_out=R_OUT)
        self.add(hifA, ohA, vA)
        self.at("part of an")
        self.play(pop(vA.body, 1.12), run_time=0.5)

        hyp = T("hydroxylated proline", 30, GOLD).move_to([SA[0], 3.05 - 1.65 + 1.65 - 1.65 + 0.0, 0])
        hyp.move_to([SA[0], AY + 1.5, 0])
        self.at("grips the hydroxylated")
        self.play(vA.animate.shift(LEFT * 2.8), FadeIn(hyp), run_time=0.9)

        # a short piece of HIF-1a, with the hydroxyl in place
        pieceA = bchip("HIF-1α piece", TEAL, 46).next_to(SA + LEFT * R_B, LEFT, buff=0)
        self.at("A short piece")
        self.play(ReplacementTransform(hifA, pieceA), run_time=0.5)
        grpA = VGroup(pieceA, ohA, vA, hyp)

        self.play(grpA.animate.shift(UP * 1.35), run_time=0.6)
        bound = T("bound tightly", 32, TEXT).move_to([4.75, AY + 1.35, 0])
        self.at("made with")
        self.play(pop(ohA, 1.4), run_time=0.5)
        self.at("bound")
        self.play(FadeIn(bound, shift=LEFT * 0.1), *glow(vA.cp, s=1.1), run_time=0.5)

        # the same piece with an ordinary proline
        BY = -1.55
        SB = np.array([-0.2, BY, 0])
        pieceB = bchip("HIF-1α piece", TEAL, 46).next_to(SB + LEFT * R_B, LEFT, buff=0)
        plain = Circle(radius=0.2, stroke_width=0, fill_color=GREY, fill_opacity=1).move_to(SB)
        plainl = T("ordinary proline", 30, GREY).move_to(SB + DOWN * 1.4)
        vB = vhl_unit(SB + RIGHT * 2.8, size=54, label=False, r_in=R_IN, r_out=R_OUT)
        self.at("The same piece")
        self.play(FadeIn(pieceB), FadeIn(plain), FadeIn(plainl), FadeIn(vB), run_time=0.6)
        self.at("did not")
        self.play(vB.animate.shift(LEFT * 2.0), run_time=0.4)
        self.play(Wiggle(vB, scale_value=1.0, rotation_angle=0.03 * TAU), run_time=0.3)
        nogrip = T("no grip", 36, RED).move_to([5.3, BY, 0])
        self.play(vB.animate.shift(RIGHT * 0.5), FadeIn(nogrip), run_time=0.3)

        sigl = T("the mark", 40, GOLD, weight=BOLD).move_to([SA[0], AY + 1.5 + 1.35, 0])
        self.at("the hydroxyl itself")
        self.play(ReplacementTransform(hyp, sigl), pop(ohA, 1.4), run_time=0.7)

        # held by VHL: a ubiquitin chain, then the proteasome
        self.at("Held by")
        whole = bchip("HIF-1α", TEAL, 46).next_to(pieceA[1].get_right() + 0 * RIGHT, LEFT, buff=0)
        whole.move_to(pieceA.get_right() + LEFT * (whole.width / 2))
        self.play(FadeOut(VGroup(pieceB, plain, plainl, vB, nogrip, bound, sigl)), ReplacementTransform(pieceA, whole), run_time=0.5)
        pieceA = whole
        chain = VGroup()
        cy = AY + 1.35 - 1.25
        for i in range(4):
            x = -5.2 + 0.72 * i
            if i:
                chain.add(Line([x - 0.72, cy, 0], [x, cy, 0], color=PINK, stroke_width=5))
            chain.add(ubi([x, cy, 0], 0.22))
        cl = T("ubiquitin chain", 32, PINK).move_to([-4.1, cy - 0.6, 0])
        self.at("gets a ubiquitin chain")
        self.play(LaggedStart(*[GrowFromCenter(m) for m in chain], lag_ratio=0.2), FadeIn(cl), run_time=1.1)

        PRC = np.array([-1.8, -2.4, 0])
        pr = proteasome(PRC, w=5.2, h=1.7)
        prl = T("proteasome", 36, RED, weight=BOLD).move_to([3.3, -2.4, 0])
        self.at("and the proteasome")
        self.play(FadeIn(pr, shift=UP * 0.2), FadeIn(prl), run_time=0.7)
        dots, moves = crumble(PRC, 10, TEAL, 1.3)
        self.at("destroys it")
        full = VGroup(pieceA, ohA, chain, cl)
        self.play(FadeOut(vA), full.animate.scale(0.5).move_to(PRC), run_time=0.9)
        self.add(dots)
        self.play(FadeOut(full, run_time=0.15), LaggedStart(*moves, lag_ratio=0.05), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Spared(SpokenScene):
    """oxygen falls: fewer OH marks, VHL has less to grip, HIF-1a is spared, the level climbs, HIF-1a pairs with ARNT and genes switch on. (CLOSE-UP, then TANK)"""

    def construct(self):
        # --- close-up: three copies, each marked and held; the enzyme and the oxygen at the left -------------
        rows = []
        for y in (2.2, 0.0, -2.2):
            c = bchip("HIF-1α", TEAL, 44).move_to([-0.2, y, 0])
            b = ohbadge(0.5).move_to(c.get_right() + RIGHT * 0.5)
            v = vhl_unit(b.get_center(), size=42, label=False, r_in=0.64, r_out=0.9)
            rows.append((c, b, v))
        o2s = VGroup(*[o2dot(p, 0.36) for p in [(-5.4, 0.6), (-4.3, 0.2), (-5.4, -0.3), (-4.3, -0.7), (-4.85, -1.3)]])
        oxy = T("oxygen", 30, YELLOW).move_to([-4.85, -2.1, 0])
        phd = bchip("prolyl\nhydroxylase", ENZ, 30).move_to([-4.6, 2.3, 0])
        grp = VGroup(*[m for r in rows for m in r], o2s, oxy, phd)
        self.add(grp)

        self.at("oxygen falls")
        down = arr([-3.0, 0.7, 0], [-3.0, -1.1, 0], YELLOW, w=6)
        self.play(LaggedStart(*[o.animate.scale(0.2).set_opacity(0) for o in o2s[1:]], lag_ratio=0.2), GrowArrow(down), run_time=1.1)
        self.at("less often")
        self.play(phd.animate.set_opacity(0.4), run_time=0.7)

        self.at("fewer prolines")
        self.play(LaggedStart(*[r[1].animate.scale(0.2).set_opacity(0) for r in rows[1:]], lag_ratio=0.25), run_time=1.0)
        self.at("has less to grip")
        self.play(*[r[2].animate.shift(RIGHT * 0.6).set_opacity(0.35) for r in rows[1:]], run_time=0.8)

        spared = T("spared", 44, TEAL, weight=BOLD).move_to([-0.2, -3.05, 0])
        self.at("is spared")
        self.play(FadeIn(spared, shift=UP * 0.1), *[pop(r[0], 1.15) for r in rows[1:]], run_time=0.9)

        # --- the tank returns; the spared copies pour into it ---------------------------------------------------
        walls = tank_walls()
        lvl = ValueTracker(LVL_AIR)
        fill = always_redraw(lambda: tank_fill(lvl.get_value()))
        P = tank_parts()
        P["drain"].set_opacity(0.3)
        P["dest"].set_opacity(0.3)
        amount = P.pop("amount")
        self.at("It builds up")
        gone = VGroup(rows[0][0], rows[0][1], rows[0][2], *[r[1] for r in rows[1:]], *[r[2] for r in rows[1:]], o2s, oxy, down, phd, spared)
        self.add(fill)
        self.play(FadeOut(gone), Create(walls), FadeIn(VGroup(*P.values())), run_time=0.5)
        flows = [Succession(r[0].animate(run_time=0.7).move_to([TK_X, TK_TOP - 0.5, 0]).scale(0.4), FadeOut(r[0], run_time=0.15)) for r in rows[1:]]
        self.play(LaggedStart(*flows, lag_ratio=0.3), lvl.animate(rate_func=linear).set_value(0.6), run_time=1.0)

        hp = bchip("HIF-1α", TEAL, 40).move_to([TK_X + 1.2, 1.2, 0])
        self.at("partner protein")
        self.play(hp.animate.move_to([1.4, 1.0, 0]), lvl.animate(rate_func=linear).set_value(LVL_HIGH), FadeIn(amount), run_time=0.8)
        arnt = bchip("ARNT", ORANGE, 40).move_to([5.0, 1.0, 0])
        self.at("called")
        self.play(FadeIn(arnt, shift=LEFT * 0.2), run_time=0.4)
        self.play(arnt.animate.next_to(hp, RIGHT, buff=0.04), run_time=0.5)
        self.at("Together")
        self.play(pop(VGroup(hp, arnt), 1.1), run_time=0.5)

        dna = Line([-0.4, -2.3, 0], [6.2, -2.3, 0], color=GREY, stroke_width=7)
        g1 = Rectangle(width=2.2, height=0.34, stroke_width=0, fill_color=GREY, fill_opacity=1).move_to([0.9, -2.3, 0])
        g2 = Rectangle(width=2.2, height=0.34, stroke_width=0, fill_color=GREY, fill_opacity=1).move_to([4.5, -2.3, 0])
        l1 = T("genes", 30, GREY).move_to([0.9, -1.65, 0])
        l2 = T("VEGF", 30, GREY).move_to([4.5, -1.65, 0])
        pair = VGroup(hp, arnt)
        k1 = arr([pair.get_center()[0] - 0.7, pair.get_bottom()[1] - 0.05, 0], [0.9, -1.2, 0], GREEN, w=6)
        k2 = arr([pair.get_center()[0] + 0.7, pair.get_bottom()[1] - 0.05, 0], [4.5, -1.2, 0], GREEN, w=6)
        self.at("switch on genes")
        self.play(Create(dna), FadeIn(g1), FadeIn(g2), FadeIn(l1), FadeIn(l2), run_time=0.6)
        self.play(GrowArrow(k1), GrowArrow(k2), g1.animate.set_fill(GREEN), g2.animate.set_fill(GREEN),
                  l1.animate.set_color(GREEN), l2.animate.set_color(GREEN), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    """made all the time, so a fall in oxygen only has to spare it; on demand would wait; it falls back within minutes; the rule. (PLOT)"""

    def construct(self):
        ax = Axes(x_range=[0, 12, 1], y_range=[0, 10, 1], x_length=11.4, y_length=4.7, tips=False,
                  axis_config={"include_ticks": False, "include_numbers": False, "color": GREY, "stroke_width": 5})
        ax.move_to([0.0, 0.6, 0])
        ylab = T("HIF-1α in the cell", 28, GREY).move_to([-4.2, 3.25, 0])
        tlab = T("time", 28, GREY).move_to(ax.c2p(11.3, 0.8))
        P0, PEAK, TF, TR, K = 1.6, 7.8, 2.0, 6.6, 1.0
        s = (PEAK - P0) / (TR - TF)

        def rise(x):
            return P0 + s * (x - TF)

        def fall(x):
            return P0 + (PEAK - P0) * np.exp(-K * (x - TR))

        def seg(f, a, b):
            return ax.plot(f, x_range=[a, b], use_smoothing=False, color=TEAL, stroke_width=8)

        flat, up, down = seg(lambda x: P0, 0, TF), seg(rise, TF, TR), seg(fall, TR, 10.6)
        self.add(ax, ylab, tlab)

        made = arr(ax.c2p(0.8, 5.2), ax.c2p(0.8, P0 + 0.35), TEAL, w=6)
        madel = T("made", 30, TEAL).next_to(made, UP, buff=0.1)
        self.at("So why make")
        self.play(Create(flat), run_time=0.6)
        self.play(GrowArrow(made), FadeIn(madel), run_time=0.4)
        self.at("just to destroy")
        d2 = arr(ax.c2p(1.5, P0 - 0.2), ax.c2p(1.5, 0.1), RED, w=6)
        d2l = T("destroyed", 30, RED).next_to(d2, RIGHT, buff=0.15)
        self.play(GrowArrow(d2), FadeIn(d2l), run_time=0.6)

        self.at("keeps making")
        self.play(*glow(made, s=1.2), pop(madel, 1.2), run_time=0.6)
        fall_line = DashedLine(ax.c2p(TF, 0), ax.c2p(TF, 9.3), color=YELLOW, stroke_width=4)
        fall_lab = T("oxygen falls", 28, YELLOW).move_to(ax.c2p(TF, 9.7) + RIGHT * 1.4)
        self.at("a fall in oxygen")
        self.play(Create(fall_line), FadeIn(fall_lab), FadeOut(made), FadeOut(madel), FadeOut(d2), FadeOut(d2l), run_time=0.7)
        self.at("only has to spare")
        self.play(Create(up), run_time=1.4, rate_func=linear)

        # the on-demand route: wait
        wait_y = 0.45
        wline = DashedLine(ax.c2p(TF, wait_y), ax.c2p(6.0, wait_y), color=GREY, stroke_width=5, dash_length=0.14)
        a = ax.c2p(TF, 0)[0]
        b = ax.c2p(6.0, 0)[0]
        by = ax.c2p(0, 0)[1] - 0.45
        bracket = VGroup(Line([a, by, 0], [b, by, 0]), Line([a, by, 0], [a, by + 0.15, 0]), Line([b, by, 0], [b + 0.5, by, 0]), Arrow([b, by, 0], [b + 0.7, by, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.2))
        bracket.set_color(GREY).set_stroke(width=4)
        bl = T("waiting for transcription and translation:\ntens of minutes to hours", 28, GREY, line_spacing=0.9).move_to([(a + b) / 2, by - 0.62, 0])
        ns = T("not to scale", 26, GREY).move_to([b + 2.2, by + 0.02, 0])
        self.at("Making it on demand")
        self.play(Create(wline), run_time=0.8)
        self.at("waiting for transcription")
        self.play(Create(bracket), FadeIn(bl), FadeIn(ns), run_time=0.7)
        self.at("tens of minutes")
        self.play(pop(bl, 1.05), run_time=0.6)

        ret_line = DashedLine(ax.c2p(TR, 0), ax.c2p(TR, 9.3), color=YELLOW, stroke_width=4)
        ret_lab = T("oxygen returns", 28, YELLOW).move_to(ax.c2p(TR, 9.7) + RIGHT * 1.65)
        self.at("when oxygen returns")
        self.play(FadeOut(VGroup(wline, bracket, bl, ns)), Create(ret_line), FadeIn(ret_lab), run_time=0.7)
        wm = T("within minutes", 34, TEAL, weight=BOLD).move_to([3.6, 1.0, 0])
        self.at("disappears within minutes")
        self.play(Create(down), FadeIn(wm), run_time=1.5, rate_func=linear)

        # the rule, as a chain that runs down the frame
        everything = VGroup(ax, ylab, tlab, flat, up, down, fall_line, fall_lab, ret_line, ret_lab, wm)
        sig = bchip("signal", YELLOW, 50).move_to([0, 2.7, 0])
        tgt = bchip("HIF-1α", TEAL, 50).move_to([-0.4, 0.2, 0])
        pr = proteasome([0, -2.5, 0], w=4.4, h=1.4)
        prl = T("destroyed", 36, RED, weight=BOLD).move_to([4.1, -2.5, 0])
        a1 = arr([0, 2.05, 0], [0, 0.95, 0], YELLOW, w=7)
        a2 = arr([0, -0.55, 0], [0, -1.7, 0], RED, w=7)
        mark = ohbadge(0.45).move_to(tgt.get_right() + RIGHT * 0.45)
        markl = T("destruction mark", 34, GOLD, weight=BOLD).next_to(mark, RIGHT, buff=0.3)
        self.at("Keep this rule")
        self.play(FadeOut(everything), run_time=0.4)
        self.play(FadeIn(sig, shift=DOWN * 0.15), FadeIn(tgt), run_time=0.4)
        self.at("a signal can write")
        self.play(GrowArrow(a1), run_time=0.5)
        self.at("the destruction mark")
        self.play(FadeIn(mark, scale=0.4), FadeIn(markl), Flash(mark.get_center(), color=GOLD, line_length=0.35, flash_radius=0.55, num_lines=10), run_time=0.7)
        self.play(GrowArrow(a2), FadeIn(pr), FadeIn(prl), run_time=0.6)
        oxy = bchip("oxygen", YELLOW, 50).move_to(sig.get_center())
        self.at("here oxygen writes")
        self.play(ReplacementTransform(sig, oxy), pop(mark, 1.4), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "A signal can write the destruction mark, and here oxygen writes it."
