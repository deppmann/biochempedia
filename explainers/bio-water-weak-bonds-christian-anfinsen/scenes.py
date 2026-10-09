"""Christian Anfinsen: a scientist profile (Biochemistrypedia, water-weak-bonds lesson).

Narration is the lesson entry's `story`, verbatim. Everything on screen comes from that entry
(name, dates, contribution, story, quote). The portrait is an AI-generated engraving-style
illustration from The Molecule Hunters; it is captioned "illustration · AI-generated" whenever it is
on screen at a readable size.

COLOR MAP (one color per concept, whole video)
  GOLD   = time and names: dates, the life timeline, the title "Thermodynamic Hypothesis", "his method"
  BLUE   = the amino acid sequence: numbered residue tiles and their chain
  TEAL   = water / environment: the water box, "a given environment"
  YELLOW = the denaturant: urea
  GREEN  = the native shape: the folded block, "one shape", "see what refolds"
  ORANGE = the interactions: hydrogen bonds, hydrophobic burial, water contacts, "totality of interactions"
  ROSE   = later life: philosophical structure, Orthodox Judaism, human rights
  RED    = unfolded, and what the refolding did not need (no template, no instructions)
  PLACE (lavender) = institutions: the Royal Swedish Academy of Sciences
  GREY   = axes, connectors, de-emphasized things
No molecular structure is drawn: the protein is a chain of numbered residue tiles (folded block or
loose string), the interactions are labelled chips, and the quote is a stack of labelled chips.
"""
import math

import numpy as np
from bp_style import *  # noqa: F401,F403

HERE = Path(os.environ.get("KX_SCRIPT", __file__)).resolve().parent
PORTRAIT = str(HERE / "anfinsen_crop.png")   # cropped + upscaled from public/scientists/christian-anfinsen.png
NAME = "Christian Anfinsen"
DATES = "1916–1995"
CAPTION = "illustration · AI-generated"
PLACE = "#B39DDB"       # institutions
ORANGE = "#E8915A"      # the interactions
ROSE = "#E58FB4"        # later life

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


def arrow(a, b, color=GREY, w=4, ratio=0.3):
    return Arrow(a, b, color=color, stroke_width=w, buff=0, max_tip_length_to_length_ratio=ratio)


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


def coil_pos(cx, cy, s=0.8):
    return [np.array([cx + s * x, cy + s * y, 0.0]) for x, y in COIL_REL]


def make_chain(positions):
    tiles = [tile(i + 1).move_to(p) for i, p in enumerate(positions)]
    links = VGroup(*[
        always_redraw(lambda a=tiles[i], b=tiles[i + 1]: Line(
            a.get_center(), b.get_center(), color=BLUE, stroke_width=4,
            stroke_opacity=min(a[0].get_stroke_opacity(), b[0].get_stroke_opacity())).set_z_index(1))
        for i in range(NRES - 1)])
    return tiles, links


def blob(cx, cy):
    """The native fold: a green block behind the folded chain."""
    return RoundedRectangle(corner_radius=0.5, width=2.55, height=1.55, stroke_color=GREEN, stroke_width=3,
                            fill_color=GREEN, fill_opacity=0.12).move_to([cx, cy, 0]).set_z_index(0)


def move_to_positions(tiles, positions, lag=0.12):
    return LaggedStart(*[t.animate.move_to(p) for t, p in zip(tiles, positions)], lag_ratio=lag)


def snake_icon(cx, cy, s=0.42):
    """A tiny copy of the folded protein (blob + dots on the snake path)."""
    b = blob(cx, cy).scale(s)
    c = np.array([cx, cy, 0.0])
    pts = [c + (p - c) * s for p in folded_pos(cx, cy)]
    path = VMobject(color=BLUE, stroke_width=3).set_points_as_corners(pts)
    dots = VGroup(*[Dot(p, radius=0.045, color=BLUE) for p in pts])
    return VGroup(b, path, dots)


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


# ----------------------------------------------------------------------------- s01 unfold, wash, refold
class S01Refold(ProfileScene):
    CX, CY = 1.1, -0.55
    BOX_C = np.array([1.95, -0.8, 0.0])

    def construct(self):
        self.add_inset()
        cx, cy = self.CX, self.CY

        # "His central insight was almost mystical in its plainness."
        top = lab("his central insight", GOLD, 32).move_to([PANEL_C, 2.95, 0])
        mystic = T("almost mystical", 30, GREY).move_to([0.2, 1.8, 0])
        plain = T("in its plainness", 30, TEXT).move_to([3.9, 1.8, 0])
        under = Line(plain.get_corner(DL) + DOWN * 0.08, plain.get_corner(DR) + DOWN * 0.08, color=GOLD, stroke_width=4)
        self.at("central insight", lead=0.0)
        self.play(pop(top), run_time=0.5)
        self.at("almost mystical")
        self.play(FadeIn(mystic, shift=UP * 0.1), run_time=0.5)
        self.at("in its plainness")
        self.play(FadeIn(plain, shift=UP * 0.1), run_time=0.4)
        self.play(Create(under), run_time=0.5)

        # the water box appears just ahead of "Drop a protein into water"
        box = RoundedRectangle(corner_radius=0.3, width=8.3, height=3.5, stroke_color=TEAL, stroke_width=2,
                               fill_color=TEAL, fill_opacity=0.10).move_to(self.BOX_C).set_z_index(-1)
        water = T("water", 30, TEAL).move_to([-1.5, 0.55, 0])
        tiles, links = make_chain(folded_pos(cx, 1.95))
        bl = blob(cx, 1.95)
        prot = T("protein", 30, BLUE).move_to([cx + 2.4, 1.95, 0])

        self.at("Drop", lead=0.7)
        self.play(FadeOut(VGroup(top, mystic, plain, under)), run_time=0.3)
        self.add(links)
        self.play(FadeIn(bl), LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in tiles], lag_ratio=0.1),
                  FadeIn(prot), run_time=0.6)
        self.at("into water", lead=0.2)
        dy = DOWN * (1.95 - cy)
        self.play(FadeIn(box), *[t.animate.shift(dy) for t in tiles], bl.animate.shift(dy), FadeOut(prot, shift=dy),
                  FadeIn(water), run_time=0.7)

        # unfold it with urea
        urea = lab("urea", YELLOW, 30).move_to([3.1, 1.95, 0])
        den = T("denaturant", 28, YELLOW).next_to(urea, RIGHT, buff=0.25)
        a_urea = arrow(urea.get_bottom() + DOWN * 0.05, [2.6, -0.1, 0], YELLOW, 4, 0.2)
        unf = lab("unfolded", RED, 28).move_to([cx, 0.5, 0])
        self.at("unfold", lead=0.1)
        self.play(pop(urea), GrowArrow(a_urea), run_time=0.5)
        self.at("urea", lead=0.3)
        self.play(FadeOut(bl), move_to_positions(tiles, coil_pos(cx, cy), 0.08),
                  Succession(Wait(0.55), pop(unf)), run_time=0.9)

        # wash the denaturant away
        flows = VGroup(arrow([-1.6, -1.75, 0], [4.2, -1.75, 0], TEAL, 4, 0.1), arrow([-1.6, -2.2, 0], [4.2, -2.2, 0], TEAL, 4, 0.1))
        flows.set_opacity(0.8)
        self.at("wash")
        self.play(Create(flows), run_time=0.5)
        self.at("denaturant", lead=0.3)
        self.play(FadeIn(den, shift=UP * 0.1), run_time=0.3)
        self.at("away", lead=0.2)
        self.play(FadeOut(VGroup(urea, den, a_urea), shift=RIGHT * 2.0), FadeOut(flows), run_time=0.7)

        # and the chain finds its way back to exactly one shape
        bl2 = blob(cx, cy)
        one = lab("exactly one shape", GREEN, 28).move_to([cx, -2.0, 0])
        self.at("finds its way", lead=0.3)
        self.play(FadeOut(unf), move_to_positions(tiles, folded_pos(cx, cy), 0.08), Succession(Wait(0.7), FadeIn(bl2)),
                  run_time=1.3)
        self.at("exactly one shape", lead=0.1)
        self.play(pop(one), run_time=0.5)

        # every time
        ys = [0.4, -0.35, -1.1]
        minis = [snake_icon(4.9, y) for y in ys]
        every = T("every time", 28, GREY).move_to([4.9, -2.0, 0])
        self.at("every time", lead=0.1)
        self.play(LaggedStart(*[FadeIn(m, scale=0.8) for m in minis], lag_ratio=0.3), FadeIn(every), run_time=1.0)

        # no template, no instructions
        c1 = lab("no template", RED, 28).move_to([0.5, 1.9, 0])
        c2 = lab("no instructions", RED, 28).move_to([4.2, 1.9, 0])
        self.at("no template", lead=0.15)
        self.play(pop(c1), run_time=0.4)
        self.at("no instructions", lead=0.15)
        self.play(pop(c2), run_time=0.4)
        self.finish()


# ----------------------------------------------------------------------------- s02 sequence + interactions
class S02Forces(ProfileScene):
    def construct(self):
        self.add_inset()
        scx, scy = -0.6, 0.3
        tiles, links = make_chain(folded_pos(scx, scy))
        bl = blob(scx, scy)
        shape = T("the shape", 30, GREEN).move_to([scx, -0.85, 0])
        self.add(links)
        self.at("The shape", lead=0.0)
        self.play(FadeIn(bl), LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in tiles], lag_ratio=0.08),
                  FadeIn(shape), run_time=0.9)

        # written in the sequence
        up = arrow([scx, 1.2, 0], [scx, 2.3, 0], GREY, 4, 0.3)
        written = T("written in", 28, GREY).move_to([scx + 1.2, 1.75, 0])
        seq_tiles = VGroup(*[tile(i + 1).move_to([PANEL_C + (i - 3.5) * 0.62, 2.75, 0]) for i in range(NRES)])
        seq_links = VGroup(*[Line(seq_tiles[i].get_center(), seq_tiles[i + 1].get_center(), color=BLUE, stroke_width=4)
                             .set_z_index(1) for i in range(NRES - 1)])
        seq_lab = T("sequence", 30, BLUE).move_to([5.45, 2.75, 0])
        self.at("written in")
        self.play(GrowArrow(up), FadeIn(written), run_time=0.5)
        self.at("sequence", lead=0.1)
        self.play(FadeIn(seq_links), LaggedStart(*[FadeIn(t, shift=DOWN * 0.1) for t in seq_tiles], lag_ratio=0.08),
                  FadeIn(seq_lab), run_time=0.9)

        # selected by the summed push-and-pull of three interactions
        self.at("selected")
        self.play(Indicate(bl, color=GREEN, scale_factor=1.06), run_time=0.6)
        head = T("Σ  push-and-pull", 30, ORANGE, weight=BOLD).move_to([4.3, 1.55, 0])
        self.at("summed push", lead=0.1)
        self.play(FadeIn(head, shift=UP * 0.1), run_time=0.5)
        names = ["hydrogen bonds", "hydrophobic burial", "water contacts"]
        cues = ["hydrogen bonds", "hydrophobic burial", "contacts with the surrounding water"]
        left = 2.5
        stage = [up, written, seq_tiles, seq_links, seq_lab, head]
        for i, (nm, cue) in enumerate(zip(names, cues)):
            c = lab(nm, ORANGE, 28)
            y = 0.8 - 0.85 * i
            c.move_to([left + c.width / 2, y, 0])
            ar = arrow([left - 0.1, y, 0], [1.0, 0.3 + (y - 0.3) * 0.5, 0], ORANGE, 4, 0.2)
            self.at(cue, lead=0.1)
            self.play(pop(c), GrowArrow(ar), run_time=0.5)
            stage += [c, ar]

        # named it the Thermodynamic Hypothesis
        self.at("He named it", lead=0.0)
        self.play(*[FadeOut(m) for m in stage], run_time=0.5)
        t1 = T("Thermodynamic", 46, TEXT, font=TITLE_FONT)
        t2 = T("Hypothesis", 46, TEXT, font=TITLE_FONT)
        title = VGroup(t1, t2).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.4, 0.55, 0])
        rule = Line(title.get_corner(DL) + DOWN * 0.2, title.get_corner(DR) + DOWN * 0.2, color=GOLD, stroke_width=4)
        self.at("thermodynamic", lead=0.1)
        self.play(Write(t1), run_time=0.7)
        self.play(Write(t2), GrowFromEdge(rule, LEFT), run_time=0.7)
        self.finish()


# ----------------------------------------------------------------------------- s03 Nobel lecture
class S03Nobel(ProfileScene):
    def construct(self):
        self.add_inset()
        academy = lab("Royal Swedish Academy of Sciences", PLACE, 28).move_to([PANEL_C, 3.05, 0])
        year = lab("1972", GOLD, 28)
        nobel = lab("Nobel lecture", TEXT, 28)
        one = lab("one sentence", TEXT, 28)
        row = VGroup(year, nobel, one).arrange(RIGHT, buff=0.3).move_to([PANEL_C, 2.2, 0])
        self.at("Royal Swedish", lead=0.1)
        self.play(pop(academy), run_time=0.5)
        self.at("1972", lead=0.1)
        self.play(pop(year), run_time=0.4)
        self.at("Nobel lecture", lead=0.1)
        self.play(pop(nobel), run_time=0.4)
        self.at("one sentence", lead=0.5)
        self.play(pop(one), run_time=0.4)

        xc = PANEL_C - 0.3
        conf = lab("native conformation", GREEN, 28).move_to([xc, 0.95, 0])
        inter = lab("totality of interatomic interactions", ORANGE, 28).move_to([xc, -0.35, 0])
        seq = lab("amino acid sequence", BLUE, 28).move_to([xc, -1.65, 0])
        a1 = arrow(inter.get_top() + UP * 0.03, conf.get_bottom() + DOWN * 0.03, GREY, 4, 0.5)
        a2 = arrow(seq.get_top() + UP * 0.03, inter.get_bottom() + DOWN * 0.03, GREY, 4, 0.5)
        l1 = T("determined by", 24, GREY).next_to(a1, RIGHT, buff=0.2)
        l2 = T("hence by", 24, GREY).next_to(a2, RIGHT, buff=0.2)

        self.at("native", lead=0.1)
        self.play(pop(conf), run_time=0.5)
        self.at("determined by", lead=0.1)
        self.play(GrowArrow(a1), FadeIn(l1), run_time=0.4)
        self.at("totality", lead=0.1)
        self.play(pop(inter), run_time=0.5)
        self.at("hence", lead=0.1)
        self.play(GrowArrow(a2), FadeIn(l2), run_time=0.4)
        self.at("amino acid sequence", lead=0.1)
        self.play(pop(seq), run_time=0.5)

        env = DashedVMobject(RoundedRectangle(corner_radius=0.25, width=8.6, height=4.0, stroke_color=TEAL,
                                              stroke_width=2.5).move_to([PANEL_C, -0.4, 0]), num_dashes=70)
        env_lab = T("in a given environment", 26, TEAL).move_to([PANEL_C, -0.4 - 2.0, 0])
        env_bg = Rectangle(width=env_lab.width + 0.3, height=env_lab.height + 0.1, stroke_width=0, fill_color=BG,
                           fill_opacity=1).move_to(env_lab)
        self.at("in a given", lead=0.1)
        self.play(Create(env), FadeIn(env_bg), FadeIn(env_lab), run_time=0.9)
        self.finish()


# ----------------------------------------------------------------------------- s04 later in life, the method
class S04Later(ProfileScene):
    def construct(self):
        self.add_inset()
        ay = 2.7
        axis = arrow([-2.2, ay, 0], [6.1, ay, 0], GREY, 3, 0.04)
        d0, d1, d2 = (Dot([x, ay, 0], radius=0.11, color=GOLD) for x in (-1.5, 5.5, 4.0))
        y0 = T("1916", 26, GOLD).move_to([-1.5, ay - 0.45, 0])
        y1 = T("1995", 26, GOLD).move_to([5.5, ay - 0.45, 0])
        later = T("later in life", 30, GOLD, weight=BOLD).move_to([4.0, ay + 0.5, 0])
        self.add(axis, d0, d1, y0, y1)
        self.at("Later in life", lead=0.0)
        self.play(FadeIn(d2, scale=2), FadeIn(later, shift=UP * 0.1), run_time=0.5)

        x0 = 1.2
        r1 = VGroup(T("went looking for", 26, GREY), lab("philosophical structure", ROSE, 28))
        r2 = VGroup(T("converting to", 26, GREY), lab("Orthodox Judaism", ROSE, 28))
        r3 = VGroup(T("fierce advocate for", 26, GREY), lab("human rights", ROSE, 28))
        rows = []
        for r, y in zip((r1, r2, r3), (1.35, 0.35, -0.65)):
            r[1].move_to([x0 + r[1].width / 2, y, 0])
            r[0].move_to([x0 - 0.3 - r[0].width / 2, y, 0])
            rows.append(r)
        self.at("philosophical", lead=0.5)
        self.play(FadeIn(r1[0], shift=RIGHT * 0.1), pop(r1[1]), run_time=0.5)
        self.at("converting", lead=0.1)
        self.play(FadeIn(r2[0], shift=RIGHT * 0.1), run_time=0.3)
        self.at("Orthodox Judaism", lead=0.1)
        self.play(pop(r2[1]), run_time=0.45)
        self.at("fierce advocate", lead=0.1)
        self.play(FadeIn(r3[0], shift=RIGHT * 0.1), run_time=0.3)
        self.at("human rights", lead=0.1)
        self.play(pop(r3[1]), run_time=0.45)

        # colleagues: the method never changed
        stage = VGroup(axis, d0, d1, d2, y0, y1, later, *[m for r in rows for m in r])
        meth = lab("his method never changed", TEXT, 30).move_to([3.4, 2.7, 0])
        said = T("Colleagues said", 26, GREY).next_to(meth, LEFT, buff=0.25)
        self.at("Colleagues said", lead=0.2)
        self.play(FadeOut(stage), FadeIn(said, shift=UP * 0.1), pop(meth), run_time=0.6)

        cx, cy = PANEL_C, -0.4
        tiles, links = make_chain(coil_pos(cx, cy))
        den = lab("denaturant", YELLOW, 30).move_to([cx, 1.3, 0])
        a_den = arrow(den.get_bottom() + DOWN * 0.05, [cx, 0.25, 0], YELLOW, 4, 0.3)
        self.at("never changed", lead=0.1)
        self.add(links)
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in tiles], lag_ratio=0.1), pop(den),
                  GrowArrow(a_den), run_time=0.9)

        self.at("remove", lead=0.1)
        self.play(FadeOut(VGroup(den, a_den), shift=UP * 1.0), run_time=0.8)
        bl = blob(cx, cy)
        see = lab("see what refolds", GREEN, 32).move_to([cx, -1.95, 0])
        self.at("see what refolds", lead=0.1)
        self.play(move_to_positions(tiles, folded_pos(cx, cy), 0.08), pop(see), run_time=1.0)
        self.play(FadeIn(bl), run_time=0.3)
        self.finish()


# ----------------------------------------------------------------------------- s05 the quote
class S05Quote(ProfileScene):
    def construct(self):
        self.add_inset()
        lines = ["“The native conformation is", "determined by the totality of", "interatomic interactions and hence",
                 "by the amino acid sequence,", "in a given environment.”"]
        # one Text block so the leading is even, then split into per-line glyph groups for the build
        full = T("\n".join(lines), 36, TEXT, font=TITLE_FONT, line_spacing=0.8)
        q, k = VGroup(), 0
        for l in lines:
            n = len(l.replace(" ", ""))
            q.add(VGroup(*full.submobjects[k:k + n]))
            k += n
        assert k == len(full.submobjects)
        fit(q, max_w=8.4)
        who = T("— Christian Anfinsen, 1972 Nobel lecture", 28, GOLD)
        g = VGroup(q, who).arrange(DOWN, aligned_edge=RIGHT, buff=0.5).move_to([PANEL_C, 0.0, 0])
        for ln in q:
            ln.set_opacity(0)
        who.set_opacity(0)
        self.add(g)
        self.wait(0.3)
        for ln in q:
            self.play(ln.animate.set_opacity(1.0), run_time=0.6)
        self.wait(0.3)
        self.play(who.animate.set_opacity(1.0), run_time=0.6)
        self.finish()


# ----------------------------------------------------------------------------- s06 end card
class S06End(EndCard):
    LINE = "Proved an amino-acid sequence alone encodes a protein's folded shape."

    def construct(self):
        a = T("Proved an amino-acid sequence alone", size=42, font=TITLE_FONT)
        b = T("encodes a protein's folded shape.", size=42, font=TITLE_FONT)
        line = VGroup(a, b).arrange(DOWN, buff=0.22)
        sub = T("biochemistrypedia.com", size=22, color=TEAL)
        g = VGroup(line, sub).arrange(DOWN, buff=0.5).move_to(ORIGIN)
        self.play(FadeIn(line, shift=UP * 0.15), run_time=self.beat(0.3))
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        self.finish()
