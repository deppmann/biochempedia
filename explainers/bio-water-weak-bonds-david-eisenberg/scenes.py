"""David Eisenberg: a scientist profile (Biochemistrypedia, water-weak-bonds lesson).

Narration is the lesson entry's `story`, verbatim. Everything on screen comes from that entry
(name, dates, contribution, story, quotes). The portrait is an AI-generated engraving-style
illustration from The Molecule Hunters; it is captioned "illustration · AI-generated" whenever it is
on screen at a readable size.

COLOR MAP (one color per concept, whole video)
  GOLD   = time and milestones: Eisenberg's name/dates, "the turn", "the rest of his career", "a century"
  TEAL   = Eisenberg himself and his ideas: young theorist, the hydrophobic moment, the steric zipper,
           the zipper's side chains, the adhesive segments
  ORANGE = anything hydrophobic: the hydrophobic interaction, non-polar residues, hydrophobic burial, the force
  BLUE   = water (the water band, water molecules)
  YELLOW = tools and data: myoglobin's coordinates, X-ray crystallography, "better numbers"
  RED    = what went wrong: too crude, the project failed, burial gone wrong, pathological clutter
  PLACE (lavender) = places: Princeton
  GREY   = axes, de-emphasised things (pure theory, polar residues, proteins as plain bars)
No molecular structure is drawn: residues are plain tiles, protein chains are bars, beta-sheets are
labelled slabs, side chains are rectangular "teeth", water molecules are dots, and the X-ray apparatus is a
generic source, beam, crystal square and detector plate. No equation or number is plotted because the
entry names none.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PORTRAIT = "/Users/deppmann/biochempedia/public/scientists/david-eisenberg.png"
CAPTION = "illustration · AI-generated"
NAME = "David Eisenberg"
DATES = "1939–"
PLACE = "#B39DDB"       # places
ORANGE = "#E8A15C"      # hydrophobic things

# left column (portrait inset + name), right panel (the story animates here)
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
    nm = T(NAME, size=32, font=TITLE_FONT)
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
    """Chip with one or more centered lines of text."""
    if isinstance(lines, str):
        lines = [lines]
    txt = VGroup(*[T(l, size, color) for l in lines]).arrange(DOWN, buff=0.1)
    ref_h = len(lines) * T("Ag", size).height + (len(lines) - 1) * 0.1
    box = RoundedRectangle(corner_radius=0.14, width=txt.width + 2 * pad, height=max(txt.height, ref_h) + 2 * pad,
                           stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=fill)
    return VGroup(box, txt.move_to(box))


def pop(mob):
    return FadeIn(mob, shift=UP * 0.12)


def strike(chip_, color=GREY):
    return Line(chip_.get_left() + RIGHT * 0.08, chip_.get_right() - RIGHT * 0.08, color=color, stroke_width=5)


def xmark(center, size=0.26, color=RED, width=8):
    return VGroup(Line([-size, -size, 0], [size, size, 0]), Line([-size, size, 0], [size, -size, 0])) \
        .set_color(color).set_stroke(width=width).move_to(center)


def residue(color=GREY, size=0.62):
    return RoundedRectangle(corner_radius=0.09, width=size, height=size, stroke_color=color, stroke_width=3,
                            fill_color=ManimColor(BG).interpolate(ManimColor(color), 0.22), fill_opacity=1)


def teeth(xs, y_base, up, color=TEAL, w=0.22, h=0.4):
    """Rectangular side-chain 'teeth' standing on y_base: pointing up if `up` else hanging down."""
    out = VGroup()
    for x in xs:
        r = Rectangle(width=w, height=h, stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.55)
        r.move_to([x, y_base + (h / 2 if up else -h / 2), 0])
        out.add(r)
    return out


class ProfileScene(SpokenScene):
    def add_inset(self):
        img, frame, cap, tag, rule = inset_group()
        self.add(img, frame, cap, tag, rule)


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
        name = T(self.TITLE, size=54, font=TITLE_FONT)
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


# ----------------------------------------------------------------------------- s01 Princeton: the failed project
class S01Princeton(ProfileScene):
    def construct(self):
        self.add_inset()
        princeton = lab("Princeton", PLACE, 30).move_to([-0.1, 2.7, 0])
        theorist = lab("young theorist", TEAL, 30).move_to([4.7, 2.7, 0])
        man = lab("the man", TEXT, 30).move_to([4.7, 1.3, 0])
        near = DashedLine(theorist.get_bottom() + DOWN * 0.05, man.get_top() + UP * 0.05, color=GREY,
                          stroke_width=3, dash_length=0.1)
        near_lab = T("near", 24, GREY).next_to(near, RIGHT, buff=0.2)
        inter = lab("hydrophobic interaction", ORANGE, 28).move_to([-0.05, 1.3, 0])
        named = Arrow(man.get_left() + LEFT * 0.05, inter.get_right() + RIGHT * 0.05, color=TEXT, stroke_width=4,
                      buff=0, max_tip_length_to_length_ratio=0.3)
        named_lab = T("named", 24, GREY).next_to(named, UP, buff=0.1)

        self.at("Princeton")
        self.play(pop(princeton), run_time=0.45)
        self.at("young theorist")
        self.play(pop(theorist), run_time=0.45)
        self.at("work near")
        self.play(Create(near), FadeIn(near_lab), pop(man), run_time=0.5)
        self.at("named the hydrophobic interaction")
        self.play(GrowArrow(named), FadeIn(named_lab), pop(inter), run_time=0.7)

        cost = lab("energetic cost", ORANGE, 28).move_to([4.8, -0.45, 0])
        coords = lab("myoglobin's coordinates", YELLOW, 26).move_to([-0.2, -0.45, 0])
        link = Arrow(coords.get_right() + RIGHT * 0.05, cost.get_left() + LEFT * 0.05, color=YELLOW, stroke_width=4,
                     buff=0, max_tip_length_to_length_ratio=0.3)
        self.at("compute its energetic cost")
        self.play(pop(cost), run_time=0.5)
        self.at("myoglobin's coordinates")
        self.play(pop(coords), GrowArrow(link), run_time=0.7)

        crude = T("too crude", 30, RED, weight=BOLD).next_to(coords, DOWN, buff=0.3)
        self.at("The coordinates were too crude")
        self.play(coords.animate.set_color(RED), FadeIn(crude, shift=UP * 0.1), run_time=0.5)
        self.play(Wiggle(coords, scale_value=1.05, rotation_angle=0.02 * TAU), run_time=0.7)

        x = xmark(link.get_center())
        stamp_t = T("project failed", 40, RED, weight=BOLD)
        stamp = VGroup(RoundedRectangle(corner_radius=0.14, width=stamp_t.width + 0.7, height=stamp_t.height + 0.5,
                                        stroke_color=RED, stroke_width=3.5, fill_color=RED, fill_opacity=0.12),
                       stamp_t)
        stamp_t.move_to(stamp[0])
        stamp.move_to([PANEL_C, -2.55, 0])
        self.at("The project failed")
        self.play(FadeIn(x, scale=1.5), cost.animate.set_opacity(0.35), run_time=0.35)
        self.play(FadeIn(stamp, scale=1.25), run_time=0.45)
        self.finish()


# ----------------------------------------------------------------------------- s02 better numbers, crystallography
class S02Crystallography(ProfileScene):
    def construct(self):
        self.add_inset()
        # phase 1: the mathematics needed better numbers
        needed = lab("what the mathematics needed", TEAL, 28).move_to([PANEL_C, 2.8, 0])
        nums = lab("the numbers", YELLOW, 30).move_to([-0.3, 1.2, 0])
        problem = T("the problem", 30, RED, weight=BOLD).next_to(nums, DOWN, buff=0.3)
        better = lab("better numbers", YELLOW, 30, fill=0.3).move_to([4.2, 1.2, 0])
        arrow = Arrow(nums.get_right() + RIGHT * 0.15, better.get_left() + LEFT * 0.15, color=YELLOW, stroke_width=4,
                      buff=0, max_tip_length_to_length_ratio=0.3)
        self.at("changed what he thought")
        self.play(pop(needed), run_time=0.6)
        link0 = DashedLine(needed.get_bottom() + DOWN * 0.05, nums.get_top() + UP * 0.05, color=GREY,
                           stroke_width=3, dash_length=0.1)
        self.at("mathematics needed")
        self.play(pop(nums), Create(link0), run_time=0.5)
        self.at("the numbers were the problem")
        self.play(nums.animate.set_color(RED), FadeIn(problem, shift=UP * 0.1), run_time=0.5)
        self.at("someone had to make")
        self.play(GrowArrow(arrow), run_time=0.5)
        self.at("better numbers")
        self.play(pop(better), run_time=0.5)

        # phase 2: X-ray crystallography replaces pure theory
        phase1 = VGroup(needed, nums, problem, better, arrow, link0)
        xr = lab("X-ray crystallography", YELLOW, 30).move_to([PANEL_C, 2.8, 0])
        ay = 1.15
        src = Rectangle(width=0.8, height=0.5, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW,
                        fill_opacity=0.3).move_to([-1.3, ay, 0])
        crystal_pos = np.array([1.3, ay, 0])
        beam = Line(src.get_right(), crystal_pos + LEFT * 0.28, color=YELLOW, stroke_width=6)
        crystal = Square(0.5, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.15) \
            .move_to(crystal_pos).rotate(PI / 4)
        det_x = 4.6
        detector = Line([det_x, ay - 1.0, 0], [det_x, ay + 1.0, 0], color=GREY, stroke_width=6)
        offs = [-0.8, -0.4, 0.0, 0.4, 0.8]
        rays = VGroup(*[Line(crystal_pos + RIGHT * 0.25, [det_x - 0.05, ay + o, 0], color=YELLOW, stroke_width=2.5)
                        .set_opacity(0.55) for o in offs])
        spots = VGroup(*[Dot([det_x, ay + o, 0], radius=0.1, color=YELLOW) for o in offs])
        self.at("He learned")
        self.play(FadeOut(phase1), run_time=0.4)
        self.at("X ray")
        self.play(pop(xr), FadeIn(src), Create(beam), FadeIn(crystal, scale=0.5), run_time=0.7)
        self.at("crystallography")
        self.play(Create(detector), LaggedStart(*[Create(r) for r in rays], lag_ratio=0.1),
                  LaggedStart(*[FadeIn(s, scale=2) for s in spots], lag_ratio=0.1), run_time=0.8)

        theory = lab("pure theory", GREY, 30).move_to([-0.3, -1.4, 0])
        craft = lab(["a craft that", "pins atoms down"], YELLOW, 28).move_to([3.7, -1.4, 0])
        swap = Arrow(theory.get_right() + RIGHT * 0.1, craft.get_left() + LEFT * 0.1, color=TEXT, stroke_width=4,
                     buff=0, max_tip_length_to_length_ratio=0.3)
        self.at("traded pure theory")
        self.play(pop(theory), run_time=0.45)
        self.at("for a craft")
        st = strike(theory)
        self.play(Create(st), theory.animate.set_opacity(0.55), GrowArrow(swap), pop(craft), run_time=0.6)
        rings = VGroup(*[Circle(radius=0.2, color=TEXT, stroke_width=3).move_to(s) for s in spots])
        self.at("pins atoms down")
        self.play(LaggedStart(*[Create(r) for r in rings], lag_ratio=0.15), run_time=0.8)

        # the force becomes a quantity
        force = lab("the force", ORANGE, 30).move_to([-0.3, -1.9, 0])
        arr2 = Arrow(force.get_right() + RIGHT * 0.1, [2.2, -1.9, 0], color=TEXT, stroke_width=4, buff=0,
                     max_tip_length_to_length_ratio=0.3)
        gauge = Rectangle(width=3.2, height=0.5, stroke_color=TEAL, stroke_width=3, fill_opacity=0) \
            .move_to([4.2, -1.9, 0])
        fillbar = Rectangle(width=2.2, height=0.5, stroke_width=0, fill_color=TEAL, fill_opacity=0.85) \
            .align_to(gauge, LEFT).align_to(gauge, DOWN)
        q_lab = T("a quantity", 30, TEAL, weight=BOLD).next_to(gauge, UP, buff=0.2)
        self.at("and only then")
        self.play(FadeOut(theory), FadeOut(swap), FadeOut(craft), FadeOut(st), FadeOut(rings),
                  run_time=0.4)
        self.at("turn the force")
        self.play(pop(force), run_time=0.4)
        self.at("into a quantity", lead=0.3)
        self.play(GrowArrow(arr2), Create(gauge), FadeIn(q_lab), run_time=0.5)
        self.play(GrowFromEdge(fillbar, LEFT), run_time=0.7)
        self.finish()


# ----------------------------------------------------------------------------- s03 the hydrophobic moment
class S03Moment(ProfileScene):
    def construct(self):
        self.add_inset()
        turn = lab("the turn", GOLD, 28).move_to([4.7, 2.85, 0])
        calc = lab("energetic calculations", TEAL, 28).move_to([0.5, 2.85, 0])
        self.at("I was able")
        self.play(pop(calc), run_time=0.5)

        # water above the protein
        water = Rectangle(width=8.0, height=0.5, stroke_width=0, fill_color=BLUE, fill_opacity=0.28) \
            .move_to([PANEL_C, 2.0, 0])
        water_lab = T("water", 26, BLUE).move_to(water)
        self.at("calculations")
        self.play(FadeIn(water), FadeIn(water_lab), run_time=0.6)

        # a protein: a row of plain residue tiles
        xs = [PANEL_C + (i - 4.5) * 0.74 for i in range(10)]
        tiles = [residue(GREY).move_to([x, 0.8, 0]) for x in xs]
        prot = T("a protein", 28, GREY).move_to([PANEL_C, 0.0, 0])
        self.at("protein")
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.12) for t in tiles], lag_ratio=0.08), FadeIn(prot), run_time=1.0)

        self.at("came up with the idea")
        self.play(FadeOut(prot), Flash(tiles[4].get_center() + UP * 0.1, color=TEAL, flash_radius=0.9,
                                       line_length=0.25), run_time=0.7)

        # non-polar residues face away from water; the arrow is the moment
        nonpolar = {1, 2, 5, 6, 9}
        moves, ups = [], []
        for i, t in enumerate(tiles):
            if i in nonpolar:
                moves.append(Transform(t, residue(ORANGE).move_to([xs[i], 0.1, 0])))
            else:
                moves.append(t.animate.shift(UP * 0.35))
        moment = Arrow([PANEL_C, -0.35, 0], [PANEL_C, -1.3, 0], color=TEAL, stroke_width=8, buff=0,
                       max_tip_length_to_length_ratio=0.3)
        m_lab = T("hydrophobic moment", 32, TEAL, weight=BOLD).move_to([PANEL_C, -1.75, 0])
        away = T("non-polar residues face away from water", 24, ORANGE).move_to([PANEL_C, -2.3, 0])
        self.at("hydrophobic moment")
        self.play(*moves, run_time=0.7)
        self.play(GrowArrow(moment), FadeIn(m_lab, shift=UP * 0.1), run_time=0.6)
        self.play(FadeIn(away), run_time=0.4)

        self.at("he said of the turn")
        self.play(pop(turn), run_time=0.45)
        self.play(Indicate(turn, color=GOLD, scale_factor=1.12), run_time=0.6)

        # related ideas -> the feeling of discoveries
        related = lab("related ideas", TEAL, 28).move_to([-0.1, -3.0, 0])
        disc = lab("discoveries", TEAL, 30, fill=0.3).move_to([4.5, -3.0, 0])
        link = Arrow(related.get_right() + RIGHT * 0.1, disc.get_left() + LEFT * 0.1, color=TEXT, stroke_width=4,
                     buff=0, max_tip_length_to_length_ratio=0.3)
        first = T("first time", 24, GOLD).next_to(link, UP, buff=0.12)
        self.at("This and related ideas")
        self.play(FadeOut(away), run_time=0.3)
        self.play(pop(related), run_time=0.45)
        self.at("for the first time")
        self.play(GrowArrow(link), FadeIn(first), run_time=0.5)
        self.at("make discoveries", lead=0.1)
        self.play(pop(disc), run_time=0.5)
        self.play(Flash(disc, color=GOLD, flash_radius=0.85, line_length=0.3), run_time=0.7)
        self.finish()


# ----------------------------------------------------------------------------- s04 hydrophobic burial gone wrong
class S04Burial(ProfileScene):
    def construct(self):
        self.add_inset()
        cx = 1.65
        career = Arrow([-2.2, 2.8, 0], [6.15, 2.8, 0], color=GOLD, stroke_width=3, buff=0,
                       max_tip_length_to_length_ratio=0.04)
        career_lab = T("the rest of his career", 28, GOLD, weight=BOLD).move_to([PANEL_C + 0.3, 3.18, 0])
        burial = lab("hydrophobic burial", ORANGE, 30).move_to([PANEL_C - 0.3, 2.05, 0])
        self.at("the rest of his career")
        self.play(Create(career), FadeIn(career_lab, shift=UP * 0.1), run_time=0.6)
        self.at("hydrophobic burial")
        self.play(pop(burial), run_time=0.5)
        wrong = T("goes wrong", 30, RED, weight=BOLD).next_to(burial, RIGHT, buff=0.3)
        self.at("go wrong")
        self.play(burial.animate.set_color(RED), FadeIn(wrong, shift=LEFT * 0.1), run_time=0.5)

        # two beta-sheets
        def slab(y):
            r = RoundedRectangle(corner_radius=0.12, width=5.2, height=0.6, stroke_color=TEXT, stroke_width=2.5,
                                 fill_color=TEXT, fill_opacity=0.12)
            return VGroup(r, T("beta-sheet", 24, TEXT).move_to(r)).move_to([cx, y, 0])

        DY = -0.3
        A, B = slab(1.15 + DY), slab(-1.55 + DY)
        rng = np.random.RandomState(7)
        x0s = rng.uniform(-0.5, 3.8, 16)
        y0s = rng.uniform(-1.1, 0.7, 16) + DY
        dots = VGroup(*[Dot([x, y, 0], radius=0.09, color=BLUE) for x, y in zip(x0s, y0s)])
        self.at("Two beta sheets")
        self.play(pop(A), pop(B), FadeIn(dots), run_time=0.8)

        # locked so tightly: sheets close in, water crowds
        # map the water band between sheets: stage 0 gap y in [-1.25, 0.85] -> stage 1 gap [-0.85, 0.5]
        s1y = [-0.8 + DY + (y - DY + 1.1) / 1.8 * 1.25 for y in y0s]
        self.at("locked so tightly")
        self.play(A.animate.move_to([cx, 0.8 + DY, 0]), B.animate.move_to([cx, -1.2 + DY, 0]),
                  *[d.animate.move_to([x, y, 0]) for d, x, y in zip(dots, x0s, s1y)], run_time=1.0)

        # squeezed out every water molecule
        outs = []
        for d, x, y in zip(dots, x0s, s1y):
            tx = -1.9 if x < cx else 5.5
            outs.append(d.animate.move_to([tx, -0.2 + DY + (y + 0.2 - DY) * 0.5, 0]).set_opacity(0))
        self.at("squeezed out")
        self.play(A.animate.move_to([cx, 0.5 + DY, 0]), B.animate.move_to([cx, -1.0 + DY, 0]), *outs, run_time=1.4)
        wlab = T("water molecules", 28, BLUE).move_to([cx, -2.8, 0])
        self.at("water molecule")
        self.play(FadeIn(wlab, shift=UP * 0.1), run_time=0.4)

        # side chains interlaced like a zipper's teeth
        pitch = 0.6
        txs = [cx - 2.1 + pitch * i for i in range(8)]
        a_teeth = teeth(txs, 0.2 + DY, up=False)
        b_teeth = teeth([x + pitch / 2 for x in txs], -0.7 + DY, up=True)
        sc = T("side chains", 26, TEAL, weight=BOLD).move_to([5.4, -0.25 + DY, 0])
        self.at("side chains")
        self.play(FadeOut(wlab), FadeIn(a_teeth), FadeIn(b_teeth), FadeIn(sc), run_time=0.6)
        self.at("interlaced")
        self.play(B.animate.shift(UP * 0.4), b_teeth.animate.shift(UP * 0.4), run_time=0.7)
        self.at("zipper's teeth")
        self.play(LaggedStart(*[Indicate(t, color=TEAL, scale_factor=1.25) for t in list(a_teeth) + list(b_teeth)],
                              lag_ratio=0.06), run_time=0.9)
        self.finish()


# ----------------------------------------------------------------------------- s05 the steric zipper
class S05Zipper(ProfileScene):
    def construct(self):
        self.add_inset()
        # mini zipper + name
        zx, zy, pitch = 0.2, 2.65, 0.4
        za = Rectangle(width=2.6, height=0.2, stroke_color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=0.25) \
            .move_to([zx, zy + 0.3, 0])
        zb = Rectangle(width=2.6, height=0.2, stroke_color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=0.25) \
            .move_to([zx, zy - 0.3, 0])
        txs = [zx - 1.0 + pitch * i for i in range(6)]
        ta = teeth(txs, zy + 0.2, up=False, w=0.16, h=0.32)
        tb = teeth([x + pitch / 2 for x in txs[:-1]], zy - 0.2, up=True, w=0.16, h=0.32)
        mini = VGroup(za, zb, ta, tb)
        name = T("steric zipper", 34, TEAL, weight=BOLD).move_to([3.7, zy, 0])
        self.at("steric zipper")
        self.play(FadeIn(mini), FadeIn(name, shift=LEFT * 0.1), run_time=0.7)

        # a century of pathological clutter
        century = lab("a century", GOLD, 28).move_to([PANEL_C, 1.5, 0])
        self.at("a century")
        self.play(pop(century), run_time=0.45)
        rng = np.random.RandomState(11)
        pieces, angs = VGroup(), []
        for k in range(16):
            w, h = rng.uniform(0.45, 1.0), rng.uniform(0.22, 0.5)
            col = RED if k % 2 == 0 else GREY
            r = RoundedRectangle(corner_radius=0.06, width=w, height=h, stroke_color=col, stroke_width=2.5,
                                 fill_color=col, fill_opacity=0.25)
            a = rng.uniform(-1.2, 1.2)
            r.rotate(a).move_to([rng.uniform(-1.6, 5.5), rng.uniform(-1.0, 0.9), 0])
            pieces.add(r)
        clutter = T("pathological clutter", 30, RED, weight=BOLD).move_to([PANEL_C, -1.9, 0])
        self.at("pathological clutter")
        self.play(LaggedStart(*[FadeIn(p, scale=0.6) for p in pieces], lag_ratio=0.05), FadeIn(clutter), run_time=1.0)

        # reduced to one line
        line_pieces = VGroup(*[Rectangle(width=0.47, height=0.07, stroke_width=0, fill_color=TEAL, fill_opacity=0.95)
                               .move_to([-1.5 + 0.45 * k, -0.1, 0]) for k in range(16)])
        one = T("one line", 30, TEAL, weight=BOLD).move_to([PANEL_C, 0.55, 0])
        self.at("to one line")
        self.play(*[Transform(p, q) for p, q in zip(pieces, line_pieces)], FadeOut(clutter), FadeOut(century),
                  FadeIn(one), run_time=1.0)

        # the line: adhesive segments are short
        self.at("We learned")
        self.play(FadeOut(pieces), FadeOut(one), run_time=0.5)
        bw, bh, segw = 4.4, 0.34, 0.8
        ys = [0.6, -0.2, -1.0]
        offs = [-1.2, 0.0, 1.2]
        bars, segs = VGroup(), VGroup()
        for y, o in zip(ys, offs):
            bar = Rectangle(width=bw, height=bh, stroke_color=GREY, stroke_width=2.5, fill_color=GREY, fill_opacity=0.18)
            bar.move_to([PANEL_C, y, 0])
            seg = Rectangle(width=segw, height=bh, stroke_color=TEAL, stroke_width=2.5, fill_color=TEAL,
                            fill_opacity=0.85).move_to([PANEL_C + o, y, 0])
            bars.add(VGroup(bar, seg))
            segs.add(seg)
        adh = T("adhesive segments", 30, TEAL, weight=BOLD).move_to([PANEL_C, -1.95, 0])
        self.at("adhesive segments")
        self.play(LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.2), FadeIn(adh, shift=UP * 0.1), run_time=0.8)
        prot_lab = T("proteins", 28, GREY).move_to([PANEL_C, 1.35, 0])
        self.at("the proteins")
        self.play(FadeIn(prot_lab), run_time=0.4)

        # they line up into a fiber
        fib_lab = T("fibers", 30, TEAL, weight=BOLD).move_to([PANEL_C, 1.45, 0])
        outline = DashedVMobject(Rectangle(width=1.15, height=2.1, stroke_color=TEAL, stroke_width=3,
                                           fill_opacity=0).move_to([PANEL_C, -0.2, 0]), num_dashes=36)
        self.at("form these fibers")
        self.play(*[bars[i].animate.shift(RIGHT * (-offs[i])) for i in range(3)], FadeOut(prot_lab), run_time=0.9)
        self.play(Create(outline), FadeIn(fib_lab), run_time=0.5)

        # just short segments
        brace = Brace(outline, DOWN, color=TEAL, buff=0.1)
        short = T("just short segments", 30, TEAL, weight=BOLD).next_to(brace, DOWN, buff=0.15)
        self.at("just short segments")
        self.play(FadeOut(adh), *[b[0].animate.set_opacity(0.35) for b in bars], run_time=0.4)
        self.play(GrowFromCenter(brace), FadeIn(short, shift=UP * 0.1), run_time=0.5)
        self.play(*[Indicate(s, color=TEAL, scale_factor=1.15) for s in segs], run_time=0.6)
        self.finish()


# ----------------------------------------------------------------------------- s06 the quote
class S06Quote(ProfileScene):
    def construct(self):
        self.add_inset()
        lines = ["“We learned that the adhesive", "segments of the proteins that", "form these fibers are just", "short segments.”"]
        q = VGroup(*[T(l, 38, TEXT, font=TITLE_FONT) for l in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        fit(q, max_w=8.4)
        who = T("— David Eisenberg", 32, GOLD)
        g = VGroup(q, who).arrange(DOWN, aligned_edge=RIGHT, buff=0.55).move_to([PANEL_C, 0.1, 0])
        for ln in q:
            ln.set_opacity(0)
        who.set_opacity(0)
        self.add(g)
        self.wait(0.4)
        for ln in q:
            self.play(ln.animate.set_opacity(1.0), run_time=0.8)
        self.wait(0.5)
        self.play(who.animate.set_opacity(1.0), run_time=0.6)
        self.finish()


# ----------------------------------------------------------------------------- s07 end card
class S07End(EndCard):
    LINE = "Coined the hydrophobic moment; mapped the steric zipper locking amyloid fibers."

    def construct(self):
        a = T("Coined the hydrophobic moment;", size=42, font=TITLE_FONT)
        b = T("mapped the steric zipper locking amyloid fibers.", size=42, font=TITLE_FONT)
        line = VGroup(a, b).arrange(DOWN, buff=0.22)
        sub = T("biochemistrypedia.com", size=22, color=TEAL)
        g = VGroup(line, sub).arrange(DOWN, buff=0.5).move_to(ORIGIN)
        self.play(FadeIn(line, shift=UP * 0.15), run_time=self.beat(0.3))
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        self.finish()
