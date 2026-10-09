"""Christian Anfinsen: a scientist profile (Biochemistrypedia, protein-3d-structure lesson).

Narration is the lesson entry's `story`, verbatim. Everything on screen comes from that entry
(name, dates, contribution, story, quote). The portrait is an AI-generated engraving-style
illustration from The Molecule Hunters; it is captioned "illustration · AI-generated" whenever it is
on screen at a readable size.

COLOR MAP (one color per concept, whole video)
  GOLD   = time: Anfinsen's name/dates, timeline markers, the wait
  BLUE   = the amino acid sequence: the numbered residue tiles and their chain, "its own sequence"
  TEAL   = the enzyme and its native fold: ribonuclease, the folded block, "native fold"
  YELLOW = reagents and tools: urea, beta-mercaptoethanol, the denaturant, the viola
  GREEN  = activity and recovery: the activity gauge, "see what refolds"
  RED    = loss and harm: zero activity, random coil, "too loud", the Dirty War, disappeared scientists
  PLACE (lavender) = places and institutions: NIH, the lab, Argentina, Royal Swedish Academy
  GREY   = axes, de-emphasized things
No molecular structure is drawn: the protein is a chain of numbered residue tiles (folded block or
loose string), and the free-energy picture is a schematic curve (a plain function, no numbers).
"""
import math

import numpy as np
from bp_style import *  # noqa: F401,F403

HERE = Path(os.environ.get("KX_SCRIPT", __file__)).resolve().parent
PORTRAIT = str(HERE / "anfinsen_crop.png")   # full engraving, cropped from public/scientists/christian-anfinsen.png
NAME = "Christian Anfinsen"
DATES = "1916–1995"
CAPTION = "illustration · AI-generated"
PLACE = "#B39DDB"       # places and institutions

INSET_C = np.array([-4.6, 1.15, 0.0])
INSET_H = 3.2
PANEL_C = 1.95          # x center of the right panel (x from -2.4 to 6.3)


# ----------------------------------------------------------------------------- helpers
def portrait_pair(height):
    img = ImageMobject(PORTRAIT).set_height(height)
    frame = Rectangle(width=img.width, height=img.height, stroke_color=GOLD, stroke_width=3, fill_opacity=0)
    return img, frame


def caption_under(frame, size=22):
    return T(CAPTION, size=size, color=GREY, font=TITLE_FONT).next_to(frame, DOWN, buff=0.2)


def name_tag(frame):
    nm = fit(T(NAME, size=32, font=TITLE_FONT), max_w=3.5)
    dt = T(DATES, size=28, color=GOLD)
    g = VGroup(nm, dt).arrange(DOWN, buff=0.14)
    g.move_to([frame.get_center()[0], frame.get_center()[1] - INSET_H / 2 - 1.3, 0])
    return g


def inset_group():
    img, frame = portrait_pair(INSET_H)
    img.move_to(INSET_C)
    frame.move_to(INSET_C)
    cap = caption_under(frame)
    tag = name_tag(frame)
    rule = Line([-2.7, -3.2, 0], [-2.7, 3.2, 0], color=GREY, stroke_width=1.5).set_opacity(0.35)
    return img, frame, cap, tag, rule


def lab(lines, color=BLUE, size=28, pad=0.22, fill=0.16):
    if isinstance(lines, str):
        lines = [lines]
    txt = VGroup(*[T(l, size, color) for l in lines]).arrange(DOWN, buff=0.1)
    ref_h = len(lines) * T("Ag", size).height + (len(lines) - 1) * 0.1
    box = RoundedRectangle(corner_radius=0.14, width=txt.width + 2 * pad, height=max(txt.height, ref_h) + 2 * pad,
                           stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=fill)
    return VGroup(box, txt.move_to(box))


def pop(mob):
    return FadeIn(mob, shift=UP * 0.12)


def xmark(center, color=RED, r=0.2, w=8):
    return VGroup(Line([-r, -r, 0], [r, r, 0]), Line([-r, r, 0], [r, -r, 0])).set_color(color) \
        .set_stroke(width=w).move_to(center)


class ProfileScene(SpokenScene):
    def add_inset(self):
        img, frame, cap, tag, rule = inset_group()
        self.add(img, frame, cap, tag, rule)


# ---- the protein as a chain of numbered residue tiles (BLUE = the sequence) ---------------------
NRES = 8
TILE = 0.5


def tile(n):
    sq = RoundedRectangle(corner_radius=0.08, width=TILE, height=TILE, stroke_color=BLUE, stroke_width=3,
                          fill_color=ManimColor(BG).interpolate(ManimColor(BLUE), 0.22), fill_opacity=1)
    return VGroup(sq, M(str(n), 22, BLUE).move_to(sq)).set_z_index(3)


def folded_pos(cx, cy):
    """Snake of 2 rows x 4: residues 1-4 left to right, 5-8 right to left."""
    xs = [-0.9, -0.3, 0.3, 0.9]
    out = [(cx + x, cy + 0.3) for x in xs] + [(cx + x, cy - 0.3) for x in reversed(xs)]
    return [np.array([x, y, 0.0]) for x, y in out]


COIL_REL = [(-3.5, 0.35), (-2.7, -0.4), (-1.5, -0.1), (-1.0, 0.5), (0.2, 0.05), (1.0, -0.5), (2.2, -0.12), (3.4, 0.42)]


def coil_pos(cx, cy):
    return [np.array([cx + x, cy + y, 0.0]) for x, y in COIL_REL]


def make_chain(positions):
    tiles = [tile(i + 1).move_to(p) for i, p in enumerate(positions)]
    links = VGroup(*[
        always_redraw(lambda a=tiles[i], b=tiles[i + 1]: Line(
            a.get_center(), b.get_center(), color=BLUE, stroke_width=4,
            stroke_opacity=min(a[0].get_stroke_opacity(), b[0].get_stroke_opacity())).set_z_index(1))
        for i in range(NRES - 1)])
    return tiles, links


def blob(cx, cy):
    return RoundedRectangle(corner_radius=0.5, width=2.55, height=1.55, stroke_color=TEAL, stroke_width=3,
                            fill_color=TEAL, fill_opacity=0.12).move_to([cx, cy, 0]).set_z_index(0)


def move_to_positions(tiles, positions, lag=0.12):
    return LaggedStart(*[t.animate.move_to(p) for t, p in zip(tiles, positions)], lag_ratio=lag)


# ---- activity gauge ----------------------------------------------------------------------------
GAUGE_Y = -2.95
GX0, GW = 0.6, 4.0


def make_gauge(tr):
    label = T("activity", 28, GREEN).move_to([-2.2 + 0.5, GAUGE_Y, 0], aligned_edge=LEFT)
    label.move_to([-2.2 + label.width / 2, GAUGE_Y, 0])
    frame = Rectangle(width=GW, height=0.36, stroke_color=GREY, stroke_width=2.5, fill_opacity=0) \
        .move_to([GX0 + GW / 2, GAUGE_Y, 0])

    def fill():
        v = tr.get_value()
        wd = max(0.001, GW * v)
        return Rectangle(width=wd, height=0.36, stroke_width=0, fill_color=GREEN, fill_opacity=0.9) \
            .move_to([GX0 + wd / 2, GAUGE_Y, 0])

    def readout():
        v = tr.get_value()
        col = GREEN if v > 0.02 else RED
        m = M(f"{round(100 * v)}%", 30, col, weight=BOLD)
        return m.move_to([GX0 + GW + 0.25 + m.width / 2, GAUGE_Y, 0])

    return label, frame, always_redraw(fill), always_redraw(readout)


def reagent_chips():
    urea = lab("urea", YELLOW, 28).move_to([-1.1, 1.7, 0])
    bme = lab("beta-mercaptoethanol", YELLOW, 28).move_to([2.7, 1.7, 0])
    a1 = Arrow(urea.get_bottom() + DOWN * 0.05, [0.95, -0.05, 0], color=YELLOW, stroke_width=4, buff=0,
               max_tip_length_to_length_ratio=0.12)
    a2 = Arrow(bme.get_bottom() + DOWN * 0.05, [2.2, -0.05, 0], color=YELLOW, stroke_width=4, buff=0,
               max_tip_length_to_length_ratio=0.12)
    return urea, bme, a1, a2


def timeline_1960():
    ay = 2.8
    axis = Arrow([-2.2, ay, 0], [6.1, ay, 0], color=GREY, stroke_width=3, buff=0, max_tip_length_to_length_ratio=0.04)
    dot = Dot([-1.2, ay, 0], radius=0.12, color=GOLD)
    date = T("1960", 32, GOLD, weight=BOLD).next_to(dot, UP, buff=0.15)
    return axis, dot, date


# ----------------------------------------------------------------------------- s00 title
class S00Title(TitleCard):
    LESSON = "Scientist profile"
    TITLE = NAME

    def construct(self):
        img, frame = portrait_pair(4.7)
        grp = Group(img, frame)
        grp.move_to([-3.3, 0.35, 0])
        cap = caption_under(frame, size=24).shift(DOWN * 0.15)
        brand = T("BIOCHEMISTRYPEDIA", size=20, color=TEAL, weight=BOLD).set_opacity(0.9)
        lesson = T(self.LESSON.upper(), size=22, color=GREY)
        name = fit(T(self.TITLE, size=50, font=TITLE_FONT), max_w=5.7)
        dates = T(DATES, size=38, color=GOLD)
        rule = Line(LEFT * 1.2, RIGHT * 1.2, color=GOLD, stroke_width=4)
        txt = VGroup(brand, lesson, name, dates, rule).arrange(DOWN, buff=0.3).move_to([3.1, 0.2, 0])
        self.play(FadeIn(img), FadeIn(frame), FadeIn(cap), run_time=0.5)
        self.play(
            ScaleInPlace(grp, 1.07, run_time=2.0, rate_func=linear),
            Succession(
                FadeIn(VGroup(brand, lesson), shift=UP * 0.1, run_time=0.4),
                Write(name, run_time=0.7),
                FadeIn(dates, shift=UP * 0.1, run_time=0.4),
                GrowFromCenter(rule, run_time=0.3),
            ),
        )
        i_img, i_frame, i_cap, i_tag, i_rule = inset_group()
        self.play(
            FadeOut(txt), FadeOut(cap),
            img.animate.set_height(INSET_H).move_to(INSET_C), frame.animate.become(i_frame),
            run_time=0.7,
        )
        self.play(FadeIn(i_cap), FadeIn(i_tag), FadeIn(i_rule), run_time=0.25)
        self.finish()


# ----------------------------------------------------------------------------- s01 NIH, viola
class S01Nih(ProfileScene):
    def construct(self):
        self.add_inset()
        tall = lab("tall, Lincolnesque figure", TEXT, 30)
        nih = lab("NIH", PLACE, 30)
        row = VGroup(tall, nih).arrange(RIGHT, buff=0.4).move_to([PANEL_C, 1.9, 0])
        self.at("tall")
        self.play(pop(tall), run_time=0.5)
        self.at("NIH")
        self.play(pop(nih), run_time=0.45)

        viola = lab("viola", YELLOW, 32).move_to([4.6, -0.5, 0])
        self.at("viola")
        self.play(pop(viola), run_time=0.45)

        amp = ValueTracker(0.25)
        n = 17
        base_y = -0.5
        wx = -0.6

        def wave():
            a = amp.get_value()
            col = interpolate_color(ManimColor(GREY), ManimColor(RED), min(1.0, max(0.0, (a - 0.25) / 0.75)))
            bars = VGroup()
            for i in range(n):
                env = 0.35 + 0.65 * abs(math.sin(1.35 * i + 0.4))
                h = max(0.06, 1.9 * a * env)
                bars.add(Rectangle(width=0.13, height=h, stroke_width=0, fill_color=col, fill_opacity=0.95)
                         .move_to([wx - 1.75 + 0.22 * i + 1.75, base_y, 0]))
            return bars

        wv = always_redraw(wave)
        sci = T("the science", 30, GREY).move_to([wx + 1.75, base_y - 1.45, 0])
        sci.move_to([wx + 0.22 * (n - 1) / 2 + 0.0, base_y - 1.45, 0])
        self.at("science")
        self.add(wv)
        self.play(pop(sci), run_time=0.5)
        self.at("too loud", lead=0.3)
        self.play(amp.animate.set_value(1.0), sci.animate.set_color(RED), run_time=0.7)
        reach = Arrow([wx + 0.22 * (n - 1) + 0.45, base_y, 0], viola.get_left() + LEFT * 0.08, color=YELLOW,
                      stroke_width=4, buff=0, max_tip_length_to_length_ratio=0.3)
        self.play(GrowArrow(reach), run_time=0.4)
        self.finish()


# ----------------------------------------------------------------------------- s02 take it apart
class S02Unfold(ProfileScene):
    CX, CY = 2.0, -0.75

    def construct(self):
        self.add_inset()
        axis, dot, date = timeline_1960()
        self.at("In 1960", lead=0.0)
        self.play(Create(axis), FadeIn(dot, scale=2), FadeIn(date, shift=UP * 0.1), run_time=0.6)

        cx, cy = self.CX, self.CY
        tiles, links = make_chain(folded_pos(cx, cy))
        bl = blob(cx, cy)
        enz = lab("ribonuclease", TEAL, 30).move_to([cx, -2.05, 0])
        self.at("ribonucleus")
        self.add(links)
        self.play(FadeIn(bl), LaggedStart(*[FadeIn(t, shift=UP * 0.12) for t in tiles], lag_ratio=0.12),
                  pop(enz), run_time=1.3)

        urea, bme, a1, a2 = reagent_chips()
        self.at("urea")
        self.play(pop(urea), run_time=0.4)
        self.at("beta")
        self.play(pop(bme), run_time=0.45)
        self.play(GrowArrow(a1), GrowArrow(a2), run_time=0.5)

        note = VGroup(T("smells like rotten eggs", 24, GREY), T("crossed with skunk", 24, GREY)) \
            .arrange(DOWN, buff=0.08).move_to([4.7, 0.65, 0])
        self.at("smells like rotten eggs")
        self.play(pop(note), run_time=0.6)

        gv = ValueTracker(1.0)
        g_lab, g_frame, g_fill, g_read = make_gauge(gv)
        self.at("watched the enzyme", lead=0.1)
        self.play(FadeOut(note), FadeIn(g_lab), FadeIn(g_frame), run_time=0.4)
        self.add(g_fill, g_read)

        self.at("collapse", lead=0.1)
        self.play(FadeOut(bl), FadeOut(a1), FadeOut(a2), move_to_positions(tiles, coil_pos(cx, cy), 0.1),
                  Succession(Wait(0.4), gv.animate.set_value(0.0).set_rate_func(smooth)), run_time=1.5)

        rc = lab("random coil", RED, 30).move_to([cx, 0.55, 0])
        self.at("random coil")
        self.play(pop(rc), run_time=0.5)
        self.finish()


# ----------------------------------------------------------------------------- s03 wash away, refold
class S03Refold(ProfileScene):
    CX, CY = 2.0, -0.75

    def construct(self):
        self.add_inset()
        cx, cy = self.CX, self.CY
        # starting state = the end of s02: reagents on, enzyme a random coil, activity at zero
        axis, dot, date = timeline_1960()
        urea, bme, a1, a2 = reagent_chips()
        tiles, links = make_chain(coil_pos(cx, cy))
        enz = lab("ribonuclease", TEAL, 30).move_to([cx, -2.05, 0])
        rc = lab("random coil", RED, 30).move_to([cx, 0.55, 0])
        gv = ValueTracker(0.0)
        g_lab, g_frame, g_fill, g_read = make_gauge(gv)
        self.add(axis, dot, date, urea, bme, links, *tiles, enz, rc, g_lab, g_frame, g_fill, g_read)

        # washed away
        self.at("washed the chemicals away", lead=0.1)
        self.play(FadeOut(urea, shift=LEFT * 1.2), FadeOut(bme, shift=RIGHT * 1.6),
                  FadeOut(VGroup(axis, dot, date)), run_time=1.0)

        # waited: a clock hand goes round once
        clock_c = np.array([cx - 0.5, 1.7, 0.0])
        face = Circle(radius=0.5, color=GOLD, stroke_width=4).move_to(clock_c)
        tick = Dot(clock_c, radius=0.05, color=GOLD)
        ang = ValueTracker(0.0)

        def hand():
            a = math.radians(90 - ang.get_value())
            u = np.array([math.cos(a), math.sin(a), 0.0])
            return Line(clock_c, clock_c + 0.38 * u, color=GOLD, stroke_width=5)

        hnd = always_redraw(hand)
        wait_lab = T("waiting", 28, GOLD).next_to(face, RIGHT, buff=0.3)
        self.at("waited", lead=0.15)
        self.add(hnd)
        self.play(FadeIn(face), FadeIn(tick), FadeIn(wait_lab), ang.animate.set_value(360), run_time=1.0, rate_func=linear)

        # found its way back
        bl = blob(cx, cy)
        self.at("found its way back", lead=0.15)
        self.play(FadeOut(VGroup(face, tick, hnd, wait_lab)), FadeOut(rc), run_time=0.4)
        self.play(move_to_positions(tiles, folded_pos(cx, cy), 0.1), Succession(Wait(0.9), FadeIn(bl)),
                  Succession(Wait(1.0), gv.animate.set_value(1.0).set_rate_func(smooth)), run_time=2.0)

        # the molecular equivalent of an egg unscrambling itself
        eq = T("the molecular equivalent of", 26, GREY).move_to([PANEL_C - 0.3, 3.15, 0])
        egg = lab("an egg unscrambling itself", TEXT, 30).move_to([PANEL_C - 0.4, 2.4, 0])
        self.at("molecular equivalent", lead=0.1)
        self.play(FadeIn(eq, shift=UP * 0.1), run_time=0.5)
        self.at("egg", lead=0.1)
        self.play(pop(egg), run_time=0.5)
        arc = Arc(radius=0.34, start_angle=math.radians(40), angle=math.radians(280), color=GREEN, stroke_width=5) \
            .add_tip(tip_length=0.2)
        arc.move_to([egg.get_right()[0] + 0.55, 2.4, 0])
        self.at("unscrambling")
        self.play(Create(arc), run_time=0.6)

        # no template, no helper, no instructions
        names = ["no template", "no helper", "no instructions"]
        chips = [lab(n, RED, 26) for n in names]
        row = VGroup(*chips).arrange(RIGHT, buff=0.25).move_to([PANEL_C, 1.4, 0])
        for phrase, c in zip(["No template", "no helper", "no instructions"], chips):
            self.at(phrase, lead=0.15)
            self.play(pop(c), run_time=0.4)

        own = lab(["its own", "sequence"], BLUE, 30).move_to([5.15, cy, 0])
        own_ar = Arrow(own.get_left() + LEFT * 0.08, [cx + 1.36, cy, 0], color=BLUE, stroke_width=4, buff=0,
                       max_tip_length_to_length_ratio=0.35)
        self.at("its own")
        self.play(pop(own), GrowArrow(own_ar), run_time=0.35)
        self.play(*[Indicate(t, color=BLUE, scale_factor=1.15) for t in tiles], run_time=0.6)
        self.finish()


# ----------------------------------------------------------------------------- s04 Nobel lecture
class S04Nobel(ProfileScene):
    X0, X1 = -1.9, 3.3
    Y0, Y1 = -2.35, 0.7
    XD0, XD1 = 0.3, 9.7

    @staticmethod
    def f(x):
        """A schematic free-energy landscape: a funnel with bumps and one clearly lowest well."""
        return 0.05 * (x - 6.4) ** 2 + 0.3 * math.sin(2.3 * x + 0.4) - 1.1 * math.exp(-((x - 6.4) / 0.55) ** 2)

    def px(self, x):
        return self.X0 + (x - self.XD0) / (self.XD1 - self.XD0) * (self.X1 - self.X0)

    def py(self, x):
        xs = np.linspace(self.XD0, self.XD1, 800)
        ys = np.array([self.f(v) for v in xs])
        lo, hi = ys.min(), ys.max()
        return self.Y0 + 0.3 + (self.f(x) - lo) / (hi - lo) * (self.Y1 - 0.15 - self.Y0 - 0.3)

    def pt(self, x):
        return np.array([self.px(x), self.py(x), 0.0])

    def construct(self):
        self.add_inset()
        academy = lab("Royal Swedish Academy", PLACE, 28).move_to([PANEL_C - 0.9, 2.95, 0])
        year = lab("1972", GOLD, 28)
        nobel = lab("Nobel lecture", TEXT, 28)
        row = VGroup(year, nobel).arrange(RIGHT, buff=0.35).move_to([PANEL_C, 2.05, 0])
        row.align_to(academy, LEFT)
        self.at("Royal Swedish Academy")
        self.play(pop(academy), run_time=0.5)
        self.at("1972", lead=0.15)
        self.play(pop(year), run_time=0.4)
        self.at("Nobel lecture", lead=0.1)
        self.play(pop(nobel), run_time=0.4)

        # free-energy landscape (schematic: a plain function, no numbers)
        xa = Arrow([self.X0, self.Y0, 0], [self.X1 + 0.3, self.Y0, 0], color=GREY, stroke_width=3, buff=0,
                   max_tip_length_to_length_ratio=0.04)
        ya = Arrow([self.X0, self.Y0, 0], [self.X0, self.Y1 + 0.35, 0], color=GREY, stroke_width=3, buff=0,
                   max_tip_length_to_length_ratio=0.06)
        ylab = T("free energy", 26, TEXT).next_to(ya, RIGHT, buff=0.15).align_to(ya, UP)
        xlab = T("conformations", 26, GREY).move_to([(self.X0 + self.X1) / 2, self.Y0 - 0.4, 0])
        curve = ParametricFunction(lambda t: self.pt(t), t_range=[self.XD0, self.XD1, 0.02], color=TEAL, stroke_width=5)
        self.at("native fold", lead=1.0)
        self.play(Create(xa), Create(ya), FadeIn(ylab), FadeIn(xlab), Create(curve), run_time=0.7)

        xs = np.linspace(self.XD0, self.XD1, 2000)
        xmin = float(xs[np.argmin([self.f(x) for x in xs])])
        ball = Dot(self.pt(0.7), radius=0.14, color=TEXT).set_z_index(4)
        roll = ParametricFunction(lambda t: self.pt(t), t_range=[0.7, xmin, 0.02])
        self.add(ball)
        self.play(MoveAlongPath(ball, roll), run_time=1.0, rate_func=smooth)

        pmin = self.pt(xmin)
        nat = lab("native fold", TEAL, 28).move_to([pmin[0], -0.35, 0])
        pin = DashedLine(pmin + UP * 0.2, nat.get_bottom() + DOWN * 0.03, color=TEAL, stroke_width=3, dash_length=0.1)
        level = DashedLine([self.X0, pmin[1], 0], [self.X1 + 0.5, pmin[1], 0], color=GREY, stroke_width=2,
                           dash_length=0.12).set_opacity(0.8)
        low = VGroup(T("lowest", 26, TEAL), T("free-energy", 26, TEAL), T("state", 26, TEAL)) \
            .arrange(DOWN, buff=0.1).move_to([5.0, pmin[1] + 0.35, 0])
        self.at("lowest free energy state", lead=0.25)
        self.play(Create(level), pop(nat), Create(pin), run_time=0.7)
        self.play(FadeIn(low, shift=LEFT * 0.1), run_time=0.5)

        seq = T("the sequence can reach", 26, BLUE).move_to([(self.X0 + self.X1) / 2 + 0.2, self.Y0 - 0.4, 0])
        self.at("sequence can reach", lead=0.3)
        self.play(FadeOut(xlab), run_time=0.2)
        self.play(FadeIn(seq, shift=UP * 0.1), Indicate(ball, color=BLUE, scale_factor=1.6), run_time=0.7)

        env = DashedVMobject(RoundedRectangle(corner_radius=0.25, width=8.7, height=4.7, stroke_color=GREY,
                                              stroke_width=2.5).move_to([PANEL_C, -1.02, 0]), num_dashes=74)
        env_lab = T("in a given environment", 26, GREY).move_to([PANEL_C, -1.02 - 2.35, 0])
        env_lab_bg = Rectangle(width=env_lab.width + 0.3, height=env_lab.height + 0.1, stroke_width=0, fill_color=BG,
                               fill_opacity=1).move_to(env_lab)
        self.at("given environment", lead=0.5)
        self.play(Create(env), FadeIn(env_lab_bg), FadeIn(env_lab), run_time=0.8)
        self.finish()


# ----------------------------------------------------------------------------- s05 Argentina
class S05Argentina(ProfileScene):
    def construct(self):
        self.add_inset()
        ay = 2.8
        axis = Arrow([-2.2, ay, 0], [6.1, ay, 0], color=GREY, stroke_width=3, buff=0, max_tip_length_to_length_ratio=0.04)
        d1, d2 = Dot([-1.2, ay, 0], radius=0.12, color=GOLD), Dot([3.4, ay, 0], radius=0.12, color=GOLD)
        l1 = T("1972", 30, GOLD, weight=BOLD).next_to(d1, UP, buff=0.15)
        l2 = T("years later", 30, GOLD, weight=BOLD).next_to(d2, UP, buff=0.15)
        self.add(axis, d1, l1)
        self.at("Years later", lead=0.0)
        self.play(FadeIn(d2, scale=2), FadeIn(l2, shift=UP * 0.1), run_time=0.5)

        lab_chip = lab("the lab", PLACE, 30).move_to([-0.2, 1.5, 0])
        arg = lab("Argentina", PLACE, 30).move_to([4.2, 1.5, 0])
        self.at("left the lab")
        self.play(pop(lab_chip), run_time=0.4)
        fly = Arrow(lab_chip.get_right() + RIGHT * 0.1, arg.get_left() + LEFT * 0.1, color=GREY, stroke_width=4, buff=0,
                    max_tip_length_to_length_ratio=0.2)
        self.at("flew")
        self.play(GrowArrow(fly), run_time=0.5)
        self.at("Argentina", lead=0.1)
        self.play(pop(arg), run_time=0.4)

        war = lab("Dirty War", RED, 30).move_to([4.2, 0.35, 0])
        self.at("dirty war", lead=0.15)
        self.play(pop(war), run_time=0.45)

        mins = lab(["government", "ministers"], TEXT, 28).move_to([-0.6, -1.35, 0])
        sci = lab(["disappeared", "scientists"], RED, 28, fill=0.0).move_to([4.0, -1.35, 0])
        sci_box = DashedVMobject(sci[0], num_dashes=26)
        sci_box.set_color(RED)
        conf = T("confront", 26, GREY).move_to([-0.6, -0.3, 0])
        self.at("confront", lead=0.1)
        self.play(FadeIn(conf, shift=UP * 0.1), run_time=0.3)
        self.at("government ministers", lead=0.1)
        self.play(pop(mins), run_time=0.45)
        over = Arrow(mins.get_right() + RIGHT * 0.1, sci.get_left() + LEFT * 0.1, color=GREY, stroke_width=4, buff=0,
                     max_tip_length_to_length_ratio=0.25)
        over_lab = T("over", 26, GREY).next_to(over, UP, buff=0.1)
        self.at("over", lead=0.1)
        self.play(GrowArrow(over), FadeIn(over_lab), run_time=0.4)
        self.at("disappeared scientists", lead=0.1)
        self.play(Create(sci_box), FadeIn(sci[1]), run_time=0.7)

        # second sentence: the method
        stage = VGroup(axis, d1, l1, d2, l2, lab_chip, arg, fly, war, mins, sci_box, sci[1], conf, over, over_lab)
        same = lab("his method", GOLD, 30).move_to([-0.7, 2.95, 0])
        self.at("His method", lead=0.3)
        self.play(FadeOut(stage), run_time=0.5)
        self.play(pop(same), run_time=0.4)
        obs = T("the book observes", 26, GREY).move_to([2.7, 2.95, 0])
        self.at("book observes", lead=0.1)
        self.play(FadeIn(obs, shift=LEFT * 0.1), run_time=0.5)

        cx, cy = 2.0, 0.3
        enz = lab("ribonuclease", TEAL, 30).move_to([cx, -1.0, 0])
        tiles, links = make_chain(coil_pos(cx, cy))
        bl = blob(cx, cy)
        self.at("same one", lead=0.0)
        self.play(pop(enz), run_time=0.4)
        self.at("enzyme", lead=0.2)
        self.add(links)
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in tiles], lag_ratio=0.1), run_time=0.9)

        den = lab("denaturant", YELLOW, 30).move_to([cx, 2.12, 0])
        rem = Arrow(den.get_bottom() + DOWN * 0.05, [cx, 0.98, 0], color=YELLOW, stroke_width=4, buff=0,
                    max_tip_length_to_length_ratio=0.3)
        self.at("remove", lead=0.1)
        self.play(pop(den), GrowArrow(rem), run_time=0.5)
        self.at("and see", lead=0.15)
        self.play(FadeOut(VGroup(den, rem), shift=UP * 0.8), run_time=0.5)
        see = lab("see what refolds", GREEN, 32).move_to([cx, -2.1, 0])
        self.at("see what refolds", lead=0.0)
        self.play(move_to_positions(tiles, folded_pos(cx, cy), 0.08), pop(see), Succession(Wait(0.5), FadeIn(bl)),
                  run_time=0.95)
        self.finish()


# ----------------------------------------------------------------------------- s06 the quote
class S06Quote(ProfileScene):
    def construct(self):
        self.add_inset()
        lines = ["“The native conformation is", "determined by the totality of", "interatomic interactions and hence",
                 "by the amino acid sequence,", "in a given environment.”"]
        q = VGroup(*[T(l, 36, TEXT, font=TITLE_FONT) for l in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        fit(q, max_w=8.4)
        who = T("— Christian Anfinsen", 32, GOLD)
        g = VGroup(q, who).arrange(DOWN, aligned_edge=RIGHT, buff=0.5).move_to([PANEL_C, 0.0, 0])
        for ln in q:
            ln.set_opacity(0)
        who.set_opacity(0)
        self.add(g)
        self.wait(0.3)
        for ln in q:
            self.play(ln.animate.set_opacity(1.0), run_time=0.65)
        self.wait(0.4)
        self.play(who.animate.set_opacity(1.0), run_time=0.6)
        self.finish()


# ----------------------------------------------------------------------------- s07 end card
class S07End(EndCard):
    LINE = "Proved the amino acid sequence alone holds all folding information."

    def construct(self):
        a = T("Proved the amino acid sequence alone", size=42, font=TITLE_FONT)
        b = T("holds all folding information.", size=42, font=TITLE_FONT)
        line = VGroup(a, b).arrange(DOWN, buff=0.22)
        sub = T("biochemistrypedia.com", size=22, color=TEAL)
        g = VGroup(line, sub).arrange(DOWN, buff=0.5).move_to(ORIGIN)
        self.play(FadeIn(line, shift=UP * 0.15), run_time=self.beat(0.3))
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        self.finish()
