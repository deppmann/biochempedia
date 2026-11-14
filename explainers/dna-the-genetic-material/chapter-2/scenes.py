"""How One Strand Specifies Another — chapter 2.

COLOR MAP (continued from chapter 1)
  BLUE   = DNA / old parental strands
  GREEN  = newly built DNA / light-labelled strands
  GOLD   = questions and the protein accent inherited from chapter 1
  GREY   = schematic apparatus and de-emphasized marks
  TEXT   = base letters and primary labels

Every strand is a labelled block diagram, never a molecular structure.  The same
builders place the carried DNA and density apparatus identically from scene to scene.
"""
import numpy as np
from bp_parts import *  # noqa: F401,F403


# --------------------------------------------------------------------------- builders
BASES = {"A": BLUE, "T": BLUE, "G": BLUE, "C": BLUE}
COMP = {"A": "T", "T": "A", "G": "C", "C": "G"}
SEQ = "GATTAC"
NEW_SEQ = "CTAATG"


def arrow_rail(y, direction=1, color=BLUE, x0=-4.7, x1=4.7, width=12):
    """A thick schematic strand rail with a small, unambiguous direction tip."""
    a, b = ([x0, y, 0], [x1, y, 0]) if direction > 0 else ([x1, y, 0], [x0, y, 0])
    return Arrow(a, b, buff=0, color=color, stroke_width=width, tip_length=0.28,
                 max_tip_length_to_length_ratio=0.08)


def base_tile(letter, center, color=BLUE, outline=False, size=34):
    box = RoundedRectangle(corner_radius=0.12, width=1.05, height=0.78,
                           stroke_color=color, stroke_width=4,
                           fill_color=color, fill_opacity=0.08 if outline else 0.72)
    txt = M(letter, size, TEXT, weight=BOLD)
    return VGroup(box, txt).move_to(center)


def empty_cup(center, color=GREEN):
    """Three-sided receiving cup: a functional shape, not molecular geometry."""
    x, y, _ = center
    return VGroup(Line([x - .48, y + .35, 0], [x - .48, y - .35, 0]),
                  Line([x - .48, y - .35, 0], [x + .48, y - .35, 0]),
                  Line([x + .48, y - .35, 0], [x + .48, y + .35, 0])).set_stroke(color, 4)


def sequence_world(answer=False, question=False, loose=False):
    """The exact prediction frame, reused by s05, s06 and s07."""
    xs = np.linspace(-3.25, 3.25, 6)
    old_rail = arrow_rail(1.55, 1, BLUE, -4.45, 4.45)
    new_rail = arrow_rail(-1.15, -1, GREEN, -4.45, 4.45, 8).set_opacity(.75)
    old = VGroup(*[base_tile(ch, [x, .72, 0]) for x, ch in zip(xs, SEQ)])
    cups = VGroup(*[empty_cup([x, -.32, 0]) for x in xs])
    ends = VGroup(T("5'", 28, BLUE).move_to([-5.0, 1.55, 0]),
                  T("3'", 28, BLUE).move_to([5.0, 1.55, 0]),
                  T("3'", 28, GREEN).move_to([-5.0, -1.15, 0]),
                  T("5'", 28, GREEN).move_to([5.0, -1.15, 0]))
    g = VGroup(old_rail, new_rail, old, cups, ends)
    g.old_rail, g.new_rail, g.old, g.cups, g.ends = old_rail, new_rail, old, cups, ends
    if answer:
        ans = VGroup(*[base_tile(ch, [x, -.32, 0], GREEN, True) for x, ch in zip(xs, NEW_SEQ)])
        g.add(ans)
        g.answer = ans
    if loose:
        drifting = VGroup(base_tile("C", [-5.75, .1, 0], GREEN, True, 32).scale(.72),
                          base_tile("T", [5.75, .15, 0], GREEN, True, 32).scale(.72),
                          base_tile("A", [-5.55, -1.65, 0], GREEN, True, 32).scale(.72),
                          base_tile("G", [5.55, -1.7, 0], GREEN, True, 32).scale(.72))
        for i, b in enumerate(drifting):
            bob(b, amp=.09, speed=1.4 + .12 * i, seed=i)
        g.add(drifting)
        g.loose = drifting
    if question:
        q = question_card("Which blocks fill the empty rail?", y=-3.12, size=32)
        g.add(q)
        g.question = q
    g.add(scope_tag("schematic"))
    return g


def duplex(old_seq=SEQ, new_seq=NEW_SEQ, center=ORIGIN, scale=.72):
    """A compact old-blue/new-green daughter duplex."""
    xs = np.linspace(-2.45, 2.45, 6)
    top = arrow_rail(.9, 1, BLUE, -3.25, 3.25, 10)
    bot = arrow_rail(-.9, -1, GREEN, -3.25, 3.25, 7)
    if scale >= .9:
        old = VGroup(*[base_tile(c, [x, .28, 0], BLUE, False, 32).scale(.78) for x, c in zip(xs, old_seq)])
        new = VGroup(*[base_tile(c, [x, -.28, 0], GREEN, True, 32).scale(.78) for x, c in zip(xs, new_seq)])
    else:
        # Overview cartoons keep the block count and strand colours, without unreadably tiny letters.
        old = VGroup(*[RoundedRectangle(corner_radius=.1, width=.7, height=.42,
                                        stroke_color=BLUE, stroke_width=3, fill_color=BLUE,
                                        fill_opacity=.72).move_to([x, .28, 0]) for x in xs])
        new = VGroup(*[RoundedRectangle(corner_radius=.1, width=.7, height=.42,
                                        stroke_color=GREEN, stroke_width=3, fill_color=GREEN,
                                        fill_opacity=.08).move_to([x, -.28, 0]) for x in xs])
    g = VGroup(top, bot, old, new).scale(scale).move_to(center)
    g.old, g.new, g.rails = old, new, VGroup(top, bot)
    return g


def strand_bar(color, y, x=0, width=2.1, label=None):
    r = RoundedRectangle(corner_radius=.13, width=width, height=.38,
                         stroke_color=color, stroke_width=4,
                         fill_color=color, fill_opacity=.72 if color == BLUE else .12).move_to([x, y, 0])
    if label:
        return VGroup(r, T(label, 24, color).next_to(r, RIGHT, buff=.16))
    return r


def density_tube(x, title, bands=(), bars=()):
    """Fixed schematic density tube. band levels: heavy=-1, hybrid=0, light=1."""
    top, bottom, h = 1.55, -2.2, 3.75
    body = RoundedRectangle(corner_radius=.5, width=2.35, height=h,
                            stroke_color=GREY, stroke_width=4,
                            fill_color=GREY, fill_opacity=.05).move_to([x, (top + bottom) / 2, 0])
    lab = fit_text(title, max_w=2.7, size=28, min_size=24, max_lines=2).move_to([x, 2.55, 0])
    level = {-1: bottom + .55, 0: (top + bottom) / 2, 1: top - .55}
    band_mobs = VGroup()
    for lev, color, frac in bands:
        band_mobs.add(RoundedRectangle(corner_radius=.08, width=1.55 * frac, height=.22,
                                       stroke_width=0, fill_color=color, fill_opacity=.95).move_to([x, level[lev], 0]))
    bar_mobs = VGroup()
    for i, (a, b) in enumerate(bars):
        yy = 1.5 - i * .52
        bar_mobs.add(strand_bar(a, yy, x - .53, .85), strand_bar(b, yy, x + .53, .85))
    g = VGroup(body, lab, band_mobs, bar_mobs)
    g.body, g.label, g.bands, g.bars = body, lab, band_mobs, bar_mobs
    return g


def three_tubes():
    a = density_tube(-4.35, "before transfer", [(-1, BLUE, 1)], [(BLUE, BLUE)])
    b = density_tube(0, "generation 1", [(0, TEAL, 1)], [(BLUE, GREEN)])
    c = density_tube(4.35, "generation 2", [(0, TEAL, .5), (1, GREEN, .5)], [(BLUE, GREEN), (GREEN, GREEN)])
    return VGroup(a, b, c)


def composition_bars(vals=(34, 34, 16, 16)):
    base_y, max_h = -2.25, 4.55
    xs = [-4.5, -1.5, 1.5, 4.5]
    cols = [BLUE, BLUE, TEAL, TEAL]
    bars, labels, nums = VGroup(), VGroup(), VGroup()
    for x, ch, v, col in zip(xs, "ATGC", vals, cols):
        h = max_h * v / 40
        bars.add(RoundedRectangle(corner_radius=.12, width=1.55, height=h,
                                  stroke_color=col, stroke_width=3, fill_color=col,
                                  fill_opacity=.72).move_to([x, base_y + h / 2, 0]))
        labels.add(M(ch, 42, TEXT, weight=BOLD).move_to([x, base_y - .48, 0]))
        nums.add(M(f"{v}%", 28, col).next_to(bars[-1], UP, buff=.14))
    g = VGroup(bars, labels, nums)
    g.bars, g.labels, g.nums = bars, labels, nums
    return g


def add_slow_sway(mob, angle=.018, speed=.8):
    """Visible but quiet continuous movement during narrated holds."""
    mob._sway_t, mob._sway_angle = 0.0, 0.0
    center = mob.get_center().copy()
    def update(m, dt):
        m._sway_t += dt
        target = angle * np.sin(speed * m._sway_t)
        m.rotate(target - m._sway_angle, about_point=center)
        m._sway_angle = target
    mob.add_updater(update)
    return mob


def diagram_field():
    """A quiet full-frame drafting field with continuously moving scan marks.

    It is scenery rather than a biological claim: the low-contrast blue board unifies the chapter,
    while the moving marks keep long spoken holds visually alive.
    """
    board = RoundedRectangle(corner_radius=.24, width=12.45, height=6.45,
                             stroke_width=0, fill_color=TEXT, fill_opacity=.119).set_z_index(-30)
    scans = VGroup()
    for i in range(12):
        x = -6.0 + i * 1.05
        mark = Line([x, -2.9, 0], [x, 2.9, 0], color=BLUE, stroke_width=8).set_opacity(.18)
        mark.set_z_index(-29)
        mark._field_speed = 1.35
        def drift(m, dt):
            m.shift(RIGHT * m._field_speed * dt)
            if m.get_x() > 6.15:
                m.shift(LEFT * 12.6)
        mark.add_updater(drift)
        scans.add(mark)
    return VGroup(board, scans)


class Film(SpokenScene):
    """Spoken scene on the chapter's shared, continuously moving diagram field."""
    def setup(self):
        super().setup()
        self.add(diagram_field())


class FilmPause(NarratedScene):
    def setup(self):
        super().setup()
        self.add(diagram_field())


# --------------------------------------------------------------------------- scenes
class S01Hook(Film):
    def construct(self):
        paths = VGroup(*[Arrow([-6.7, y, 0], [-3.8, .4 * y, 0], buff=0, color=BLUE,
                                  stroke_width=7, tip_length=.22) for y in (2.1, .7, -.7, -2.1)])
        self.at("first film traced")
        self.play(LaggedStart(*[GrowArrow(p) for p in paths], lag_ratio=.14), run_time=1.7)
        d = duplex(center=[1.35, -.15, 0], scale=1.02)
        self.play(ReplacementTransform(paths, d), run_time=1.5)
        add_slow_sway(d.rails)
        q = T("How can DNA make a copy?", 40, GOLD, font=TITLE_FONT).move_to([0, 3.05, 0])
        self.at("How can DNA")
        self.play(Write(q), run_time=1.0)
        shape = T("shape", 30, GREY).move_to([-3.0, -2.55, 0])
        rule = T("matching rule", 34, GREEN, weight=BOLD).move_to([2.0, -2.55, 0])
        self.at("not the helix")
        self.play(FadeIn(shape), run_time=.6)
        self.at("matching rule")
        self.play(shape.animate.set_opacity(.25), FadeIn(rule, shift=UP * .15), run_time=.9)
        self.at("labelled blocks")
        self.play(LaggedStart(*[Indicate(b, color=GREEN, scale_factor=1.05) for b in d.new], lag_ratio=.1), run_time=1.7)
        self.finish()


class S02Title(TitleCard):
    LESSON = "DNA Is the Genetic Material"
    TITLE = "How One Strand Specifies Another"

    def construct(self):
        rails = VGroup(arrow_rail(.75, 1, BLUE, -6.0, 6.0, 10),
                       arrow_rail(-.75, -1, BLUE, -6.0, 6.0, 10)).set_opacity(.22)
        add_slow_sway(rails, .025, .9)
        lesson = T(self.LESSON.upper(), 22, GREY)
        title = T(self.TITLE, 50, font=TITLE_FONT)
        fit(title, max_w=11.5)
        rule = Line(LEFT * 1.2, RIGHT * 1.2, color=GOLD, stroke_width=4)
        card = VGroup(lesson, title, rule).arrange(DOWN, buff=.34)
        self.add(rails)
        self.play(FadeIn(card), run_time=.55)
        self.wait(.9)
        self.play(FadeOut(card), rails.animate.set_opacity(.75), run_time=.55)
        self.finish()


class S03Composition(Film):
    def construct(self):
        blocks = VGroup(*[base_tile(c, [(i - 1.5) * 2.3, 2.35, 0], BLUE if c in "AT" else TEAL)
                          for i, c in enumerate("ATGC")])
        self.at("Start with base composition")
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN * .2) for b in blocks], lag_ratio=.15), run_time=1.2)
        bars1 = composition_bars()
        self.play(LaggedStart(*[ReplacementTransform(blocks[i], bars1.bars[i]) for i in range(4)], lag_ratio=.12),
                  FadeIn(bars1.labels), FadeIn(bars1.nums), run_time=1.8)
        eq1 = T("A matches T", 30, BLUE).move_to([-2.7, 3.25, 0])
        eq2 = T("G matches C", 30, TEAL).move_to([2.7, 3.25, 0])
        self.at("adenine lies close")
        self.play(FadeIn(eq1), Indicate(VGroup(bars1.bars[0], bars1.bars[1]), color=BLUE), run_time=1.0)
        self.at("guanine lies close")
        self.play(FadeIn(eq2), Indicate(VGroup(bars1.bars[2], bars1.bars[3]), color=TEAL), run_time=1.0)
        bars2 = composition_bars((22, 22, 28, 28))
        tag1 = scope_tag("sample 1 · schematic")
        self.add(tag1)
        self.at("different samples")
        self.play(*[ReplacementTransform(bars1.bars[i], bars2.bars[i]) for i in range(4)],
                  *[ReplacementTransform(bars1.nums[i], bars2.nums[i]) for i in range(4)],
                  run_time=2.2)
        tag2 = scope_tag("sample 2 · schematic")
        self.play(swap(tag1, tag2, .6))
        self.finish()


class S04Pairing(Film):
    def construct(self):
        top = arrow_rail(1.7, 1, BLUE, -5.5, 5.5)
        bottom = arrow_rail(-1.7, -1, BLUE, -5.5, 5.5)
        self.at("Place two blue rails")
        self.play(GrowArrow(top), GrowArrow(bottom), run_time=1.4)
        pairs = [("A", "T"), ("G", "C"), ("T", "A"), ("C", "G")]
        xs = [-4.1, -1.35, 1.35, 4.1]
        upper = VGroup(*[base_tile(a, [x, .6, 0]) for x, (a, _) in zip(xs, pairs)])
        cups = VGroup(*[empty_cup([x, -.55, 0], BLUE) for x in xs])
        self.play(FadeIn(upper), FadeIn(cups), run_time=.9)
        lower = VGroup(*[base_tile(b, [x, -.55, 0], BLUE, True) for x, (_, b) in zip(xs, pairs)])
        starts = [[-6.0, -.4, 0], [-5.7, -1.0, 0], [5.7, -.4, 0], [6.0, -1.0, 0]]
        for tile, p in zip(lower, starts): tile.move_to(p)
        self.at("adenine pairs")
        self.play(lower[0].animate.move_to(cups[0]), lower[2].animate.move_to(cups[2]), run_time=1.2)
        self.at("guanine pairs")
        self.play(lower[1].animate.move_to(cups[1]), lower[3].animate.move_to(cups[3]), run_time=1.2)
        totals = VGroup(T("A = T", 34, BLUE), T("G = C", 34, TEAL)).arrange(RIGHT, buff=1.5).move_to([0, 2.75, 0])
        self.at("explain the whole")
        self.play(FadeIn(totals), run_time=.8)
        self.at("rails are schematic")
        self.play(FadeIn(scope_tag("schematic · labelled blocks")), run_time=.6)
        self.finish()


class S05Predict(Film):
    def construct(self):
        closed = duplex(center=ORIGIN, scale=1.0)
        self.at("Now unzip")
        self.play(FadeIn(closed), run_time=.7)
        world = sequence_world()
        self.play(ReplacementTransform(closed, VGroup(world.old_rail, world.new_rail, world.old, world.cups, world.ends)), run_time=1.8)
        oldlab = T("old · blue", 28, BLUE).move_to([-4.9, 2.55, 0])
        newlab = T("new · green outline", 28, GREEN).move_to([3.9, -2.05, 0])
        self.at("old blocks remain blue")
        self.play(FadeIn(oldlab), run_time=.6)
        self.at("green outlines")
        self.play(FadeIn(newlab), run_time=.6)
        self.at("Predict the new partner")
        self.play(LaggedStart(*[Indicate(b, color=GOLD, scale_factor=1.05) for b in world.old], lag_ratio=.12), run_time=1.5)
        self.at("adenine selects thymine")
        self.play(Indicate(world.old[1], color=GREEN), Indicate(world.cups[1], color=GREEN), run_time=.8)
        self.at("guanine selects cytosine")
        self.play(Indicate(world.old[0], color=GREEN), Indicate(world.cups[0], color=GREEN), run_time=.8)
        q = question_card("Which blocks fill the empty rail?", y=-3.12, size=32)
        self.at("Which blocks fill")
        self.play(FadeOut(oldlab), FadeOut(newlab), FadeIn(q), FadeIn(scope_tag("schematic")), run_time=.7)
        add_slow_sway(world.old_rail, .012, 1.1)
        self.finish()


class S06Pause(FilmPause):
    def construct(self):
        world = sequence_world(question=True, loose=True)
        self.add(world)
        self.play(world.loose.animate.shift(UP * .12), rate_func=there_and_back, run_time=2.25)
        self.play(world.loose.animate.shift(DOWN * .12), rate_func=there_and_back, run_time=2.25)
        self.finish()


class S07Reveal(Film):
    def construct(self):
        world = sequence_world()
        self.add(world)
        xs = np.linspace(-3.25, 3.25, 6)
        answer = VGroup(*[base_tile(ch, [x, -3.0, 0], GREEN, True) for x, ch in zip(xs, NEW_SEQ)])
        self.at("Each position admits")
        self.play(LaggedStart(*[answer[i].animate.move_to(world.cups[i]) for i in range(6)], lag_ratio=.18), run_time=2.2)
        result = T("3'-CTAATG-5'", 34, GREEN, weight=BOLD).move_to([0, -2.25, 0])
        self.at("specified by the first")
        self.play(FadeIn(result), run_time=.7)
        direction = CurvedArrow([4.6, -1.35, 0], [-4.6, -1.35, 0], angle=-.35, color=GREEN, stroke_width=5)
        self.at("Reverse the reading direction")
        self.play(Create(direction), run_time=1.0)
        one = VGroup(world.old_rail, world.new_rail, world.old, world.cups, world.ends, answer)
        d1 = duplex(center=[-3.25, 0, 0], scale=.72)
        d2 = duplex(center=[3.25, 0, 0], scale=.72)
        d1.new.set_opacity(0)
        d2.new.set_opacity(0)
        self.at("both old rails separate")
        self.play(FadeOut(result), FadeOut(direction), FadeOut(one), FadeIn(d1), FadeIn(d2), run_time=1.1)
        self.at("each can guide")
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN * .15) for b in VGroup(*d1.new, *d2.new)], lag_ratio=.06), run_time=1.6)
        cap = caption("one duplex → two matching duplexes", color=GREEN)
        self.at("One duplex can")
        self.play(FadeIn(cap), d1.animate.shift(LEFT * .2), d2.animate.shift(RIGHT * .2), run_time=1.0)
        self.finish()


class S08Prediction(Film):
    def construct(self):
        d1 = duplex(center=[-3.2, 1.55, 0], scale=.62)
        d2 = duplex(center=[3.2, 1.55, 0], scale=.62)
        self.at("copying proposal")
        self.play(FadeIn(d1), FadeIn(d2), run_time=.9)
        proposal = T("proposal", 32, GOLD).move_to([0, 3.1, 0])
        self.play(FadeIn(proposal), run_time=.5)
        old_badge = chip("old · heavy", BLUE, 28).move_to([-3.2, -.25, 0])
        new_badge = chip("new · light", GREEN, 28).move_to([3.2, -.25, 0])
        self.at("one old strand")
        self.play(FadeIn(old_badge), Indicate(VGroup(d1.old, d2.old), color=BLUE), run_time=.9)
        self.at("one new strand")
        self.play(FadeIn(new_badge), Indicate(VGroup(d1.new, d2.new), color=GREEN), run_time=.9)
        tubes = VGroup(density_tube(-3.2, "daughter 1", [(0, TEAL, 1)], [(BLUE, GREEN)]),
                       density_tube(3.2, "daughter 2", [(0, TEAL, 1)], [(BLUE, GREEN)])).scale(.68).shift(DOWN * 1.18)
        for tube in tubes:
            tube.label.scale(1 / .68)
        self.at("Give old strands")
        self.play(FadeOut(proposal), FadeOut(old_badge), FadeOut(new_badge), run_time=.45)
        self.play(FadeOut(d1), FadeOut(d2), FadeIn(tubes), run_time=.7)
        self.at("combined density")
        self.play(Indicate(VGroup(tubes[0].bands, tubes[1].bands), color=GOLD), run_time=1.4)
        self.play(FadeIn(scope_tag("strand bars + bands · schematic")), run_time=.5)
        self.finish()


class S09Bands(Film):
    def construct(self):
        tubes = three_tubes()
        # begin with empty apparatus, then reveal the data pattern in narration order
        for t in tubes:
            t.bands.set_opacity(0)
            t.bars.set_opacity(0)
        self.play(FadeIn(tubes), run_time=.9)
        self.at("Before transfer")
        self.play(tubes[0].bands.animate.set_opacity(1), tubes[0].bars.animate.set_opacity(1), run_time=1.2)
        self.at("After one generation")
        self.play(tubes[1].bars.animate.set_opacity(1), run_time=.8)
        self.at("one hybrid band")
        self.play(tubes[1].bands.animate.set_opacity(1), run_time=1.0)
        self.at("After another generation")
        self.play(tubes[2].bars.animate.set_opacity(1), run_time=1.0)
        self.at("half the duplexes")
        self.play(tubes[2].bands.animate.set_opacity(1), run_time=1.2)
        levels = VGroup(T("light", 24, GREEN).move_to([6.15, .98, 0]),
                        T("hybrid", 24, TEAL).move_to([6.15, -.33, 0]),
                        T("heavy", 24, BLUE).move_to([6.15, -1.65, 0]))
        self.play(FadeIn(levels), FadeIn(scope_tag("band positions · schematic")), run_time=.7)
        self.finish()


class S10Alternatives(Film):
    def construct(self):
        observed = VGroup(density_tube(-1.35, "generation 1", [(0, TEAL, 1)]),
                          density_tube(1.35, "generation 2", [(0, TEAL, .5), (1, GREEN, .5)])).scale(.9)
        observed.shift(RIGHT * 2.0)
        self.add(observed)
        alt1 = density_tube(-4.75, "parental together", [(-1, BLUE, .55), (1, GREEN, .55)]).scale(.78)
        alt1.label.scale(1 / .78)
        self.at("parental strands stayed")
        self.play(FadeIn(alt1, shift=RIGHT * .2), run_time=.9)
        alt2 = density_tube(-4.75, "material dispersed", [(-.0, TEAL, 1)]).scale(.78)
        alt2.label.scale(1 / .78)
        shift_arrow = Arrow([-4.75, -1.15, 0], [-4.75, .35, 0], color=TEAL, stroke_width=5, tip_length=.2)
        self.at("old material dispersed")
        self.play(ReplacementTransform(alt1, alt2), run_time=.8)
        self.at("shift gradually")
        self.play(GrowArrow(shift_arrow), run_time=1.0)
        self.at("observed hybrid band")
        self.play(FadeOut(alt2), FadeOut(shift_arrow), Indicate(observed[0].bands, color=GOLD), run_time=1.0)
        self.at("hybrid and light bands")
        self.play(Indicate(observed[1].bands, color=GOLD), run_time=1.0)
        daughters = VGroup(VGroup(strand_bar(BLUE, 1.15, -5.15, 1.25), strand_bar(GREEN, .75, -5.15, 1.25)),
                           VGroup(strand_bar(BLUE, -.25, -5.15, 1.25), strand_bar(GREEN, -.65, -5.15, 1.25)))
        self.at("matched strand retention")
        self.play(FadeIn(daughters), run_time=.8)
        cap = caption("the band pattern is the test", color=GOLD)
        self.at("pattern, not exact density")
        self.play(FadeIn(cap), FadeIn(scope_tag("schematic")), run_time=.8)
        self.finish()


class S11Conclusion(Film):
    def construct(self):
        panels = TwoPanel("base totals", "copying rule", colors=(BLUE, GREEN), top=2.9, bottom=-1.8, width=12.0)
        self.at("Pairing does two jobs")
        self.play(FadeIn(panels), run_time=.8)
        left = VGroup(T("A = T", 40, BLUE, weight=BOLD),
                      T("G = C", 40, TEAL, weight=BOLD)).arrange(DOWN, buff=.65)
        panels.put(left, "left")
        right = VGroup(duplex(center=[0, .75, 0], scale=.48), duplex(center=[0, -.75, 0], scale=.48))
        panels.put(right, "right")
        self.at("complementary bases match")
        self.play(FadeIn(left), run_time=1.0)
        self.at("each old strand specify")
        self.play(FadeIn(right), run_time=1.1)
        connector = Arrow([-1.1, .55, 0], [1.1, .55, 0], color=GOLD, stroke_width=5, tip_length=.22)
        self.play(GrowArrow(connector), run_time=.7)
        inset_body = RoundedRectangle(corner_radius=.18, width=1.5, height=.72,
                                      stroke_color=GREY, stroke_width=3).move_to([0, -2.4, 0])
        inset_bands = VGroup(Line([-.5, -2.54, 0], [.05, -2.54, 0], color=TEAL, stroke_width=8),
                             Line([.18, -2.26, 0], [.73, -2.26, 0], color=GREEN, stroke_width=8))
        inset_label = T("density pattern", 24, TEAL).next_to(inset_body, LEFT, buff=.22)
        inset = VGroup(inset_body, inset_bands, inset_label)
        self.at("density bands test")
        self.play(FadeIn(inset), run_time=.8)
        limit = T("not every enzyme step", 28, GREY).move_to([0, -2.4, 0])
        self.at("do not test every")
        self.play(FadeOut(inset), FadeIn(limit), run_time=.7)
        rule = caption("structure supplied a rule", color=BLUE, y=-2.4)
        test = caption("experiment tested its consequence", color=GREEN, y=-2.95)
        self.at("Structure supplied")
        self.play(FadeOut(limit), FadeIn(rule), run_time=.7)
        self.at("Experiment tested")
        self.play(FadeIn(test), Indicate(connector, color=GOLD), run_time=.8)
        self.finish()


class S12End(EndCard):
    LINE = "Complementary pairing lets each DNA strand specify a new partner."
