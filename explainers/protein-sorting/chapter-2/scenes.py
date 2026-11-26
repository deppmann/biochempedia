"""How Do You Know It Went In? — Protein Sorting into Compartments, chapter 2.

Color map shared with chapter 1: GOLD = signal, TEAL = SRP, BLUE = readers
away from the ER, INDIGO = ER, ORANGE = mitochondrion, MAGENTA = peroxisome,
RED = cutting or blocked, GREY/WHITE = ribosome or chain. LIME = protease,
CYAN = detergent, GREEN = a result supported by the experiment.
"""

from importlib.util import module_from_spec, spec_from_file_location

from bp_parts import *
from bp_style import EndCard


_chapter_spec = spec_from_file_location("protein_sorting_chapter_one", Path(__file__).resolve().parent.parent / "scenes.py")
chapter_one = module_from_spec(_chapter_spec)
_chapter_spec.loader.exec_module(chapter_one)

GOLD = chapter_one.GOLD
INDIGO = chapter_one.INDIGO
ORANGE = chapter_one.ORANGE
MAGENTA = chapter_one.MAGENTA
LIME = "#B6E65C"
CYAN = "#72E4F5"
GLASS = "#A2B6D2"
LIQUID = "#263249"
GEL = "#242B3C"
LESSON_TITLE = "Protein Sorting into Compartments"
FILM_TITLE = "How Do You Know It Went In?"

TUBE_PROTECTED = (-4.31, -0.64, 0)
TUBE_EXPOSED = (-1.12, -0.33, 0)
ZOOM_PROTECTED = (-3.97, -0.27, 0)
ZOOM_EXPOSED = (-0.46, -0.30, 0)
TUBE_RIBOSOME = (-3.68, 1.18, 0)
RINGS = ((-5.36, 0.97, 0), (-1.46, 1.04, 0), (-2.62, -1.98, 0))
RING_RADII = (0.61, 0.61, 0.62)
CUTTER_START = ((-3.13, 1.91, 0), (-2.43, 1.91, 0), (-0.22, 0.52, 0))
CUTTER_ZOOM = ((-2.40, 1.99, 0), (-1.40, 1.5, 0), (-0.52, 0.72, 0))
CUTTER_AFTER = ((-2.65, 1.85, 0), (-1.61, 1.38, 0), (-0.55, 0.31, 0))
LANE_X = (1.91, 3.78, 5.65)
BAND_Y = 0.24
TRIMMED_Y = -0.36

LIGHT_AT = (-5.00, -0.55, 0)
GLOBIN_AT = (-0.96, -0.55, 0)
PREDICT_VESICLE = (-2.98, -0.54, 0)
PREDICT_RIBOSOMES = ((-5.00, 0.55, 0), (-0.96, 0.55, 0))
PREDICT_CUTTERS = ((-3.30, 2.12, 0), (-2.22, 2.09, 0), (-0.22, 1.94, 0))
QUESTION = "Which survives the protease?"
QUESTION_STYLE = dict(y=3.33, left=-5.13, color=TEXT, size=36)
WAIT_SECONDS = 4.5

CELL_PEROX = (-5.10, 0.75, 0)
CELL_MITO = (4.78, -0.10, 0)
ASSAY_INSET = (-5.12, 3.00, 0)
RULE_LEFT = 0.68
RULE_Y = (3.40, 2.88)
TEST_Y = 2.11


def point(x, y):
    return np.array([x, y, 0.0])


def label(words, x, y, color=TEXT, size=28, **kwargs):
    return T(words, size, color, **kwargs).move_to(point(x, y))


def film_scope():
    return scope_tag("schematic, not to scale", size=28, color=TEXT).set_z_index(20)


def folded_chain(center, radius=0.15, count=10):
    """The same white bead cartoon, folded into a staggered cluster."""
    chain = chapter_one.bead_chain(count, 0, r=radius)
    chain.arrange_in_grid(rows=3, buff=0.018)
    for i, bead in enumerate(chain):
        if i // 4 == 1:
            bead.shift(RIGHT * radius * 0.72)
    return chain.move_to(center)


def signal_chain(center, count=10, gold=3, radius=0.14, angle=0):
    return chapter_one.bead_chain(count, gold, r=radius).rotate(angle).move_to(center)


def lead_path(chain, vertices, spacing):
    """Put the gold leading end first, following the path back to the ribosome."""
    path = np.asarray(vertices, dtype=float)
    lengths = np.r_[0, np.cumsum(np.linalg.norm(np.diff(path, axis=0), axis=1))]
    for i, bead in enumerate(chain):
        distance = min(i * spacing, lengths[-1])
        bead.move_to([np.interp(distance, lengths, path[:, coord]) for coord in range(3)])
    return chain


def emerging_chain(ribosome, count, gold, radius, direction):
    mouth = ribosome[-1].get_center()
    positions = [mouth + direction * (2 * radius + 0.018) * index for index in range(count, 0, -1)]
    chain = signal_chain(ORIGIN, count=count, gold=gold, radius=radius)
    for bead, position in zip(chain, positions):
        bead.move_to(position)
    return chain


def grow_chain(chain, duration):
    return LaggedStart(*(GrowFromCenter(b) for b in reversed(chain)), lag_ratio=0.21, run_time=duration)


def translate_chain(ribosome, chain, duration):
    """Release beads from the mouth in order, beginning with the leading end."""
    mouth = ribosome[-1].get_center()
    return LaggedStart(*(FadeIn(bead, target_position=mouth) for bead in chain),
                       lag_ratio=0.23, run_time=duration)


def route(start, end, color=TEXT, tip=True):
    line = DashedLine(start, end, dash_length=0.14, dashed_ratio=0.62, color=color, stroke_width=3)
    if tip:
        line.add_tip(tip_length=0.20)
    return line


def specks(positions):
    return VGroup(*(Dot(point(x, y), radius=r, color=GLASS, fill_opacity=0.26)
                    for x, y, r in positions))


def hook_world():
    er = chapter_one.er_world()
    mito = chapter_one.mitochondrion(pos=(5.24, 0.12, 0))
    perox = chapter_one.peroxisome()
    ribosome = chapter_one.ribosome(scale=1.17)
    dust = specks([(-5.6, -1.4, .04), (-5.2, .45, .045), (-3.6, 2.75, .05),
                   (-2.1, -1.6, .055), (0.9, 1.83, .055), (2.4, -.8, .04),
                   (2.9, 1.55, .04), (4.25, -1.78, .05)])
    return VGroup(dust, er, mito, perox, ribosome)


def hook_cargo(threaded=False):
    chain = signal_chain(ORIGIN, count=12, gold=4, radius=0.142)
    if threaded:
        path = [(0.99, -2.88, 0), (0.95, -2.23, 0), (0.78, -1.65, 0),
                (0.13, -1.25, 0), (-0.61, -1.14, 0), (-1.35, -0.87, 0)]
    else:
        path = [(1.91, -0.89, 0), (1.04, -1.16, 0), (0.40, -1.11, 0),
                (-0.29, -0.97, 0), (-0.78, -1.04, 0), (-1.40, -0.83, 0)]
    return lead_path(chain, path, 0.30)


def hook_questions():
    return VGroup(label("?", 1.96, -2.83, size=48, weight=BOLD),
                  label("?", 3.41, .57, size=48, weight=BOLD))


def hook_signal_detail():
    """An enlarged view of the signal and the adjacent chain."""
    panel = RoundedRectangle(width=2.84, height=1.08, corner_radius=.19,
                             stroke_color=GOLD, stroke_width=2.5,
                             fill_color=GOLD, fill_opacity=.17).move_to(point(1.76, .57))
    signal = signal_chain((1.76, .57, 0), count=6, gold=4, radius=.174)
    return panel, signal


def tube_glass():
    """Open glass outline and a clipped-looking liquid silhouette."""
    liquid = VMobject(stroke_width=0, fill_color=LIQUID, fill_opacity=1)
    liquid.start_new_path(point(-6.30, 1.68))
    liquid.add_line_to(point(-6.30, -0.95))
    liquid.add_cubic_bezier_curve_to(point(-6.30, -2.37), point(-5.08, -3.18), point(-2.98, -3.18))
    liquid.add_cubic_bezier_curve_to(point(-0.86, -3.18), point(0.34, -2.37), point(0.34, -0.95))
    liquid.add_line_to(point(0.34, 1.68))
    liquid.close_path()
    wall = VMobject(stroke_color=GLASS, stroke_width=3.5)
    wall.start_new_path(point(-6.49, 2.64))
    wall.add_line_to(point(-6.49, -0.95))
    wall.add_cubic_bezier_curve_to(point(-6.49, -2.55), point(-5.22, -3.37), point(-2.98, -3.37))
    wall.add_cubic_bezier_curve_to(point(-0.75, -3.37), point(0.54, -2.55), point(0.54, -0.95))
    wall.add_line_to(point(0.54, 2.64))
    liquid_edge = Line(point(-6.30, 1.68), point(0.34, 1.68), color=GLASS, stroke_width=2, stroke_opacity=0.42)
    lips = VGroup(Line(point(-6.66, 2.64), point(-6.15, 2.64), color=GLASS, stroke_width=3.5),
                  Line(point(0.20, 2.64), point(0.69, 2.64), color=GLASS, stroke_width=3.5))
    dust = specks([(-5.9, -.1, .035), (-5.7, -1.54, .046), (-5.01, -2.2, .04),
                   (-3.9, -2.55, .055), (-3.1, .0, .045), (-2.75, -1.1, .04),
                   (-1.65, -1.43, .05), (-.82, .47, .036), (-.35, -1.2, .04)])
    return VGroup(liquid, wall, liquid_edge, lips, dust)


def vesicle(center, radius, bright=False):
    return Circle(radius=radius, stroke_color=INDIGO,
                  stroke_width=7 if bright else 4.0,
                  fill_color=INDIGO, fill_opacity=0.22).move_to(center)


def surrounding_rings():
    return VGroup(*(vesicle(p, r) for p, r in zip(RINGS, RING_RADII)))


def protection_subject(zoom=False, bright=False):
    center = ZOOM_PROTECTED if zoom else TUBE_PROTECTED
    return (vesicle(center, 2.29 if zoom else 0.82, bright=bright),
            folded_chain(center, radius=0.255 if zoom else 0.153))


def gel_panel(with_labels=True):
    """Fixed three-lane gel, rebuilt at identical coordinates for each assay."""
    body = RoundedRectangle(width=5.77, height=5.13, corner_radius=0.23,
                            stroke_color=GLASS, stroke_width=2.5,
                            fill_color=GEL, fill_opacity=1).move_to(point(3.78, -0.01))
    lanes = VGroup(*(RoundedRectangle(width=1.61, height=2.79, corner_radius=0.13,
                                    stroke_color=GLASS, stroke_opacity=0.43, stroke_width=2,
                                    fill_color=BG, fill_opacity=0.98).move_to(point(x, -0.72))
                     for x in LANE_X))
    parts = VGroup(body, lanes)
    if with_labels:
        heads = VGroup(label("no\nprotease", LANE_X[0], 1.83, line_spacing=.62),
                       label("+\nprotease", LANE_X[1], 1.83, line_spacing=.62),
                       label("+ protease\n+ detergent", LANE_X[2], 1.83, size=22, line_spacing=.62))
        parts.add(heads)
    return parts


def band(lane, y=BAND_Y):
    return RoundedRectangle(width=1.17, height=0.17, corner_radius=0.056,
                            stroke_width=0, fill_color=TEXT, fill_opacity=1).move_to(point(LANE_X[lane], y))


def missing_band():
    outline = RoundedRectangle(width=1.17, height=0.17, corner_radius=0.056).move_to(point(LANE_X[2], BAND_Y))
    return DashedVMobject(outline, num_dashes=14, dashed_ratio=0.45,
                          color=GLASS, stroke_width=2, stroke_opacity=0.56)


def cutter(center, facing=0, radius=0.24, gape=0.58):
    """A cartoon protease with a mouth pointing in its direction of travel."""
    head = Sector(radius=radius, start_angle=gape + facing,
                  angle=TAU - 2 * gape, arc_center=center, fill_color=LIME,
                  fill_opacity=1, stroke_width=0)
    eye_at = np.array(center) + radius * point(-0.12, 0.46)
    if facing < -0.7:
        eye_at += LEFT * radius * 0.14
    eye = Dot(eye_at, radius=radius * 0.15, color=BG)
    return VGroup(head, eye)


def cutter_set(positions, facings=(DOWN, DOWN, LEFT)):
    angles = (lambda direction: float(np.arctan2(direction[1], direction[0])))
    return VGroup(*(cutter(p, facing=angles(d)) for p, d in zip(positions, facings)))


def digest(scene, exposed, enzyme, end, duration=1.35, facing=-PI):
    """The enzyme closes on the exposed chain and leaves separated fragments."""
    center = exposed.get_center()
    pieces = [np.array([0.44 * np.cos(i * TAU / len(exposed)),
                        0.31 * np.sin(i * TAU / len(exposed)), 0]) for i in range(len(exposed))]
    scene.play(Transform(enzyme, cutter(end, facing=facing, gape=0.49)),
               run_time=duration * 0.42)
    scene.play(Transform(enzyme, cutter(end, facing=facing, gape=0.10)),
               *(bead.animate.shift(offset + (bead.get_center() - center) * 0.08)
                 for bead, offset in zip(exposed, pieces)), run_time=duration * 0.25)
    scene.play(FadeOut(exposed), Transform(enzyme, cutter(end, facing=facing)),
               run_time=duration * 0.33)


def prediction_rings():
    return VGroup(vesicle((-3.64, 1.30, 0), 0.49), vesicle((-2.26, 1.06, 0), 0.49))


def prediction_parts():
    """The still shared by the question, the silent pause and the first reveal frame."""
    return {
        "tube": tube_glass(),
        "gel": gel_panel(),
        "rings": prediction_rings(),
        "main": vesicle(PREDICT_VESICLE, 0.82),
        "light_ribo": chapter_one.ribosome(PREDICT_RIBOSOMES[0], scale=0.48),
        "globin_ribo": chapter_one.ribosome(PREDICT_RIBOSOMES[1], scale=0.48),
        "light": signal_chain(LIGHT_AT, radius=0.092, angle=PI),
        "globin": signal_chain(GLOBIN_AT, gold=0, radius=0.092),
        "cutters": cutter_set(PREDICT_CUTTERS),
        "light_label": label("light chain\n(secreted)", -4.76, -1.82, GOLD, size=24, line_spacing=0.65),
        "globin_label": label("globin\n(stays in cytosol)", -1.35, -1.82, size=24, line_spacing=0.65),
        "year": caption("Blobel and Dobberstein, 1975", size=26, y=-2.48).move_to(point(-2.98, -2.48)),
    }


def prediction_question(text=QUESTION, **style):
    question = question_card(text, **(style or QUESTION_STYLE))
    backing = SurroundingRectangle(question.question, buff=.17, corner_radius=.12,
                                    color=GLASS, stroke_width=2, fill_color=GLASS, fill_opacity=.19)
    return VGroup(backing, question)


def assembled_assay():
    """The just-completed assay beside the selected tube components for scene 8."""
    tube, gel = tube_glass(), gel_panel()
    rings = prediction_rings()
    main = vesicle(PREDICT_VESICLE, 0.82)
    inside = folded_chain(PREDICT_VESICLE, radius=0.126, count=7)
    bands = VGroup(band(0), band(1, TRIMMED_Y))
    return tube, gel, rings, main, inside, bands


def assay_inset():
    """Keep the actual tube, microsome and gel as the visual index to the first test."""
    tube = tube_glass()
    micro = vesicle(TUBE_PROTECTED, 0.82)
    cargo = folded_chain(TUBE_PROTECTED, radius=0.15)
    gel = gel_panel(with_labels=False)
    assay = VGroup(tube, micro, cargo, gel, band(0), band(1, TRIMMED_Y))
    assay.scale(0.212).move_to(ASSAY_INSET)
    return assay, micro


def cell_picture(with_ribosome=False):
    """The carried cytosol world from chapter one, with room for the assay inset."""
    er = chapter_one.er_world(opacity=0.3)
    er.remove(er[-1])
    # Use the same geometry and palette with the subdued ER below the current assay.
    er[0].set_fill(INDIGO, opacity=0.25)
    mito = chapter_one.mitochondrion(pos=CELL_MITO, scale=0.92)
    mito[0].set_fill(ORANGE, opacity=0.26)
    perox = chapter_one.peroxisome(pos=CELL_PEROX, scale=1.76)
    perox.set_fill(MAGENTA, opacity=0.27)
    dust = specks([(-6.22, -1.25, .05), (-5.0, -1.5, .04), (-3.8, 2.1, .04),
                   (-2.4, 1.48, .05), (-2.7, -1.58, .046), (0.8, -.79, .04),
                   (2.2, -1.79, .043), (5.6, -2.35, .04)])
    parts = VGroup(dust, er, mito, perox)
    if with_ribosome:
        parts.add(chapter_one.ribosome(pos=(-2.15, 0.14, 0), scale=0.77))
    return parts


def callout_rule(prompt, method, color, y):
    parts = VGroup(T(prompt, 28, TEXT, weight=BOLD), T(method, 28, color))
    return parts.arrange(RIGHT, buff=0.13).move_to(point(RULE_LEFT, y), aligned_edge=LEFT)


def test_rules():
    return VGroup(callout_rule("GOT IN?", "protection test", INDIGO, RULE_Y[0]),
                  callout_rule("WHAT SENT IT?", "move and delete", GOLD, RULE_Y[1]))


def test_tags():
    return VGroup(label("sufficient", 2.00, TEST_Y, GOLD, weight=BOLD),
                  label("necessary", 4.21, TEST_Y, GOLD, weight=BOLD))


def cell_index(scene, tests=0):
    assay, mini_vesicle = assay_inset()
    rules, tags = test_rules(), test_tags()
    scene.add(assay, rules, *tags[:tests], film_scope())
    return assay, mini_vesicle, rules, tags


def eraser(center):
    body = RoundedRectangle(width=0.74, height=0.43, corner_radius=0.10,
                            stroke_color=RED, stroke_width=3,
                            fill_color=RED, fill_opacity=0.78)
    end = Line(point(-0.15, -0.18), point(-0.15, 0.18), color=BG, stroke_width=3)
    return VGroup(body, end).rotate(-0.38).move_to(center)


def passenger(center, radius=0.20):
    return folded_chain(center, radius=radius, count=12)


def transfer_parts():
    ball = passenger((-3.03, -0.61, 0))
    signal = signal_chain((-2.02, 0.86, 0), count=3, radius=0.135)
    donor = signal_chain((-0.44, 0.86, 0), count=7, gold=0, radius=0.135)
    return ball, signal, donor


def target_compartment():
    outline = RoundedRectangle(width=2.86, height=2.31, corner_radius=0.39,
                               stroke_color=TEXT, stroke_width=3,
                               fill_color=GLASS, fill_opacity=0.15).move_to(point(1.29, -0.47))
    name = label("target", 1.29, 0.30)
    return outline, name


def finished_transfer():
    outline, name = target_compartment()
    ball = passenger((0.80, -0.91, 0))
    signal = signal_chain((1.95, -0.94, 0), count=3, radius=0.135)
    return VGroup(outline, name, ball, signal)


def dhfr_block(center):
    signal = signal_chain(ORIGIN, count=3, radius=0.135)
    protein = boxed_label("DHFR (mouse enzyme)", GREY, size=28, pad=.16, fill_opacity=0.22)
    return VGroup(protein, signal).arrange(RIGHT, buff=0.13).move_to(center)


def tail_tiles(center, variant="SKL"):
    tiles = VGroup(*(boxed_label(letter, GOLD, size=44, box=(1.10, 1.06),
                                 pad=.16, fill_opacity=.86) for letter in variant))
    for tile in tiles:
        tile.label.set_color(BG)
    return tiles.arrange(RIGHT, buff=.16).move_to(center)


def success(x, y):
    return label("✓ sufficient", x, y, GREEN, size=29, weight=BOLD)


class S00Link(TitleCard, SpokenScene):
    """The spoken opening precedes the script's two-second on-screen title."""

    LESSON = LESSON_TITLE
    TITLE = FILM_TITLE

    def construct(self):
        world = hook_world()
        cargo = hook_cargo()
        self.add(world, film_scope())
        self.at("in chapter 1")
        self.play(FadeIn(cargo[-1], scale=0.7), run_time=0.45)
        self.at("a stretch", lead=0.55)
        self.play(grow_chain(VGroup(*cargo[:-1]), 2.1))
        self.at("as an address")
        self.play(Indicate(VGroup(*cargo[:4]), color=GOLD, scale_factor=1.14), run_time=1.0)
        self.at("how do you know", lead=.42)
        self.play(Transform(cargo, hook_cargo(threaded=True)), run_time=1.58)
        questions = hook_questions()
        self.at("went inside", lead=0.08)
        self.play(GrowFromCenter(questions[0]), run_time=0.53)
        self.at("which stretch")
        panel, detail = hook_signal_detail()
        tip = VGroup(*cargo[:4])
        self.play(FadeIn(panel, shift=UP * .12),
                  TransformFromCopy(tip, VGroup(*detail[:4])), run_time=.82)
        self.play(FadeIn(VGroup(*detail[4:])), GrowFromCenter(questions[1]), run_time=.51)
        self.finish()


class S01Title(TitleCard):
    LESSON = LESSON_TITLE
    TITLE = FILM_TITLE

    def construct(self):
        previous = hook_world()
        lumen_name = previous[1][-1]
        previous[1].remove(lumen_name)
        carry = VGroup(previous, hook_cargo(threaded=True))
        questions = hook_questions()
        tube = tube_glass().set_z_index(-1)
        title = fit_text(self.TITLE, max_w=11.7, size=52, min_size=42, font=TITLE_FONT).move_to(point(-0.15, 3.22))
        rule = Line(point(-1.30, 2.78), point(1.00, 2.78), color=GOLD, stroke_width=3)
        detail = VGroup(*hook_signal_detail())
        self.add(carry, lumen_name, questions, detail, film_scope())
        # Clear the hook labels before the heading moves in and the cutaway shrinks.
        self.play(FadeOut(questions), FadeOut(lumen_name), FadeOut(detail), run_time=0.2)
        self.play(FadeIn(title), GrowFromCenter(rule),
                  carry.animate.scale(0.28).move_to(point(-2.98, -1.25)), run_time=0.65)
        self.play(FadeIn(tube), run_time=0.20)
        self.play(FadeOut(carry), run_time=0.47)
        self.play(FadeOut(title), FadeOut(rule), run_time=0.48)


class S02Tube(SpokenScene):
    def construct(self):
        tube, gel = tube_glass(), gel_panel()
        main, inside = protection_subject()
        rims = surrounding_rings()
        ribo = chapter_one.ribosome(TUBE_RIBOSOME, scale=0.54)
        self.add(tube, film_scope())
        self.at("start with")
        self.play(FadeIn(gel), run_time=0.85)
        self.play(FadeIn(ribo), run_time=0.65)
        self.at("make the protein", lead=0.55)
        emerging = emerging_chain(ribo, 10, 3, .103, point(.79, -.61))
        self.play(grow_chain(emerging, 1.55))
        self.at("that also holds")
        self.play(FadeIn(main), run_time=0.50)
        self.play(LaggedStart(*(FadeIn(ring) for ring in rims), lag_ratio=0.22), run_time=0.73)
        name = label("microsomes (ER vesicles)", -3.40, 2.28, INDIGO)
        pointer = Line(point(-5.14, 2.00), point(-5.31, 1.65), color=INDIGO, stroke_width=3)
        self.at("microsomes")
        self.play(FadeIn(name), Create(pointer), run_time=0.52)
        self.play(Transform(emerging, inside), run_time=0.81)
        second = emerging_chain(ribo, 10, 0, .093, point(.91, -.41))
        self.play(grow_chain(second, .93))
        self.play(Transform(second, folded_chain(TUBE_EXPOSED, radius=.13)),
                  FadeOut(name), FadeOut(pointer), run_time=.82)
        self.at("then add a protease")
        tip = Polygon(point(-3.18, 3.15), point(-2.53, 3.15), point(-2.69, 2.48),
                      point(-2.90, 2.26), point(-3.08, 2.48),
                      stroke_color=LIME, stroke_width=3, fill_color=LIME, fill_opacity=0.30)
        self.play(FadeIn(tip, shift=DOWN * 0.24), run_time=0.51)
        enzymes = cutter_set(((-2.87, 2.03, 0), (-2.68, 2.27, 0), (-2.36, 2.05, 0)))
        self.play(LaggedStart(*(GrowFromCenter(c) for c in enzymes), lag_ratio=0.21), run_time=0.56)
        name = label("protease", -4.42, 2.26, LIME)
        across = cutter((-0.22, 2.10, 0), facing=0)
        starts = cutter_set(CUTTER_START)
        self.play(FadeIn(name), FadeOut(tip, shift=UP * 0.22),
                  Transform(enzymes[0], starts[0]), Transform(enzymes[1], starts[1]),
                  Transform(enzymes[2], across), run_time=0.75)
        self.play(Transform(enzymes[2], starts[2]), run_time=0.67)
        self.play(FadeOut(name), run_time=0.38)
        self.finish()


class S03Shield(SpokenScene):
    def construct(self):
        tube, gel = tube_glass(), gel_panel()
        main, inside = protection_subject()
        rims = surrounding_rings()
        ribo = chapter_one.ribosome(TUBE_RIBOSOME, scale=0.54)
        outside = folded_chain(TUBE_EXPOSED, radius=0.13)
        enzymes = cutter_set(CUTTER_START)
        self.add(tube, rims, ribo, gel, main, inside, outside, enzymes, film_scope())
        self.at("the added protease")
        big_ring, big_cargo = protection_subject(zoom=True)
        self.play(FadeOut(rims, run_time=0.38), FadeOut(ribo, run_time=0.38),
                  Transform(main, big_ring, run_time=1.28), Transform(inside, big_cargo, run_time=1.28),
                  Transform(outside, folded_chain(ZOOM_EXPOSED, radius=0.157), run_time=1.28),
                  Transform(enzymes, cutter_set(CUTTER_ZOOM), run_time=1.28))
        self.at("cannot cross", lead=0.05)
        contact = (-2.30, 1.54, 0)
        self.play(Transform(enzymes[0], cutter(contact, facing=-2.30)), run_time=0.75)
        block = label("×", -1.66, 1.02, RED, size=44, weight=BOLD)
        self.play(GrowFromCenter(block), run_time=0.34)
        self.play(Transform(enzymes[0], cutter(CUTTER_AFTER[0], facing=2.50)),
                  run_time=0.93)
        self.at("an intact", lead=-1.0)
        stop = label("cannot cross intact microsome", -3.35, 2.92, TEXT)
        self.play(FadeOut(block), FadeIn(stop),
                  main.animate.set_stroke(width=7).set_fill(INDIGO, opacity=0.35), run_time=0.46)
        self.at("a chain outside")
        self.play(FadeOut(stop), Transform(enzymes[1], cutter(CUTTER_AFTER[1], facing=-0.95)),
                  run_time=0.76)
        self.at("chewed up", lead=0.48)
        digest(self, outside, enzymes[2], CUTTER_AFTER[2], duration=1.42, facing=-PI / 2)
        self.at("a chain inside")
        self.play(main.animate.set_stroke(width=8).set_fill(INDIGO, 0.30), run_time=1.00)
        self.at("is shielded")
        self.play(FadeIn(band(0), shift=DOWN * 0.22), run_time=0.61)
        self.at("band survives")
        self.play(FadeIn(band(1), shift=DOWN * 0.44), run_time=0.95)
        self.finish()


class S04Detergent(SpokenScene):
    def construct(self):
        tube, gel = tube_glass(), gel_panel()
        main, inside = protection_subject(zoom=True, bright=True)
        main.set_stroke(width=8).set_fill(INDIGO, 0.30)
        rims = surrounding_rings()
        enzymes = VGroup(cutter(CUTTER_AFTER[0], facing=2.50),
                         cutter(CUTTER_AFTER[1], facing=-0.95),
                         cutter(CUTTER_AFTER[2], facing=-PI / 2))
        self.add(tube, gel, band(0), band(1), main, inside, enzymes, film_scope())
        self.at("but maybe")
        small_ring, small_cargo = protection_subject()
        destinations = ((-3.13, 0.34, 0), (-2.46, 1.19, 0), (-0.74, 0.34, 0))
        self.play(Transform(main, small_ring), Transform(inside, small_cargo),
                  *(enzyme.animate.shift(np.subtract(end, start))
                    for enzyme, start, end in zip(enzymes, CUTTER_AFTER, destinations)), run_time=0.94)
        self.play(FadeIn(rims), run_time=0.44)
        self.at("resists protease")
        doubt = label("?", -4.28, 0.53, size=46, weight=BOLD)
        self.play(GrowFromCenter(doubt), run_time=0.62)
        self.play(Indicate(inside, color=TEXT, scale_factor=1.20), run_time=0.84)
        self.at("add a detergent")
        bubbles = VGroup(*(Circle(radius=r, color=CYAN, stroke_width=3, fill_color=CYAN, fill_opacity=0.13)
                           .move_to(point(x, y)) for x, y, r in
                           [(-4.54, -2.12, .25), (-3.18, -2.36, .17), (-2.04, -1.82, .29),
                            (-5.48, -1.92, .16), (-1.18, -1.54, .13), (-3.88, -1.82, .14)]))
        detergent = label("detergent", -4.88, -2.20, CYAN)
        self.play(FadeOut(doubt), FadeIn(bubbles, shift=UP * 0.42), run_time=0.5)
        self.play(FadeIn(detergent), bubbles.animate.shift(UP * 0.55), run_time=0.51)
        self.at("dissolves membranes")
        rings = [main, *rims]
        arcs = VGroup(*(Arc(radius=ring.width / 2, start_angle=i * TAU / 4 + .15,
                           angle=TAU / 4 - .31, arc_center=ring.get_center(),
                           stroke_color=INDIGO, stroke_width=4)
                        for ring in rings for i in range(4)))
        splash = [point(-4.51, -1.13), point(-2.78, -1.48), point(-1.39, .93),
                  point(-5.46, .46), point(-.74, -.40), point(-3.93, -.86)]
        self.play(*(bubble.animate.move_to(end) for bubble, end in zip(bubbles, splash)),
                  FadeOut(detergent), run_time=.59)
        self.play(FadeOut(VGroup(*rings)), FadeIn(arcs), run_time=.29)
        self.play(FadeOut(arcs), FadeOut(bubbles),
                  Transform(inside, folded_chain((-3.89, -0.63, 0), radius=0.153)),
                  run_time=0.59)
        digest(self, inside, enzymes[0], (-3.12, -0.56, 0), duration=1.23)
        self.at("band now vanishes", lead=0.07)
        self.play(Create(missing_band()), run_time=0.62)
        self.at("the membrane was")
        verdict = label("✓  membrane was the shield", -2.98, -1.58, GREEN, size=32, weight=BOLD)
        self.play(FadeIn(verdict, shift=UP * 0.14), run_time=0.84)
        self.finish()


class S05Predict(SpokenScene):
    def construct(self):
        p = prediction_parts()
        self.add(p["tube"], p["gel"], film_scope())
        self.at("in 1975")
        self.play(FadeIn(p["main"]), FadeIn(p["rings"]), run_time=0.88)
        self.play(FadeIn(p["year"]), run_time=0.78)
        self.at("tested an antibody", lead=0.72)
        self.play(FadeIn(p["light_ribo"]), run_time=0.49)
        light = emerging_chain(p["light_ribo"], 10, 3, .079, point(-.16, -.99))
        self.play(translate_chain(p["light_ribo"], light, 1.28))
        self.play(ReplacementTransform(light, p["light"]), run_time=.59)
        self.at("a secreted protein")
        self.play(FadeIn(p["light_label"]), run_time=0.63)
        self.at("globin which stays", lead=0.85)
        self.play(FadeIn(p["globin_ribo"]), run_time=0.46)
        globin = emerging_chain(p["globin_ribo"], 10, 0, .079, point(-.16, -.99))
        self.play(translate_chain(p["globin_ribo"], globin, .79))
        self.play(ReplacementTransform(globin, p["globin"]), run_time=.57)
        self.play(FadeIn(p["globin_label"]), run_time=0.47)
        self.at("was made the same way")
        self.play(Indicate(p["light_ribo"], color=GLASS, scale_factor=1.04),
                  Indicate(p["globin_ribo"], color=GLASS, scale_factor=1.04),
                  run_time=0.91)
        self.play(FadeIn(p["cutters"]), run_time=0.44)
        self.at("which survives", lead=.03)
        self.play(FadeIn(prediction_question(), shift=UP * .26), run_time=2.49, rate_func=linear)
        self.finish()


class S06Pause(PredictPause):
    QUESTION = QUESTION
    CARD = QUESTION_STYLE
    SECONDS = WAIT_SECONDS

    def backdrop(self):
        return VGroup(*prediction_parts().values(), film_scope())

    def construct(self):
        # Keep the question and comparison fully still during the supplied pause.
        self.add(self.backdrop(), prediction_question(self.QUESTION, **self.CARD))
        self.wait(self.SECONDS)


class S07Reveal(SpokenScene):
    def construct(self):
        p = prediction_parts()
        q = prediction_question()
        self.add(*p.values(), film_scope(), q)
        self.at("the light chain")
        self.play(FadeOut(q), FadeOut(p["year"]), FadeOut(p["light_label"]),
                  FadeOut(p["globin_label"]), FadeOut(p["globin_ribo"]), run_time=0.24)
        self.play(p["light_ribo"].animate.move_to(point(-4.35, .26)), run_time=0.48)
        threaded = lead_path(signal_chain(ORIGIN, radius=0.108),
                             [(-2.58, -0.86, 0), (-3.24, -0.59, 0), (-3.71, -0.44, 0),
                              (-4.00, -0.38, 0), (-4.50, -0.19, 0)], 0.218)
        self.play(Transform(p["light"], threaded), run_time=0.59)
        self.at("trimmed and protected", lead=0.06)
        gold_tip = VGroup(*p["light"][:3])
        rest = VGroup(*p["light"][3:])
        self.play(FadeOut(gold_tip, shift=DOWN * 0.22),
                  Transform(rest, folded_chain(PREDICT_VESICLE, radius=0.126, count=7)),
                  run_time=0.43)
        self.play(p["light_ribo"].animate.shift(UP * 0.37 + LEFT * 0.10),
                  Transform(p["cutters"], cutter_set(CUTTER_START)), run_time=0.58)
        high = band(0)
        low = band(1, TRIMMED_Y)
        trimmed = label("trimmed", LANE_X[1], -0.93, TEXT, size=22)
        self.play(FadeIn(high, shift=DOWN * 0.26), run_time=0.33)
        self.play(FadeIn(low, shift=DOWN * 0.65), run_time=0.45)
        self.play(FadeIn(trimmed), run_time=0.34)

        self.at("happened only when")
        saved_gel = VGroup(p["gel"], high, low, trimmed)
        later = TwoPanel("Vesicles added later", "", top=2.55, bottom=-2.56,
                         width=11.0, gap=0.50, size=28, colors=(RED, GREY))
        # Use the left half of the component for the separate reaction in the gel's place.
        stage = VGroup(later.left_frame, later.left_head).shift(RIGHT * 6.66)
        later_ribo = chapter_one.ribosome(pos=(3.05, 1.05, 0), scale=0.47)
        later_chain = emerging_chain(later_ribo, 9, 3, 0.13, RIGHT)
        late_ring = vesicle((2.65, -0.96, 0), 0.65)
        late_cutter = cutter((5.52, -0.60, 0), facing=2.16, radius=0.29)
        self.play(swap(saved_gel, stage, run_time=0.64))
        self.play(FadeIn(later_ribo), run_time=0.26)
        self.play(translate_chain(later_ribo, later_chain, 0.62))
        self.play(FadeOut(later_ribo), later_chain.animate.shift(DOWN * .62), run_time=0.40)
        self.at("while it was being made")
        self.play(FadeIn(late_ring, shift=RIGHT * 0.22), run_time=0.49)
        self.play(FadeIn(late_cutter, shift=LEFT * 0.34), run_time=0.32)
        digest(self, later_chain, late_cutter, (6.02, -0.24, 0), duration=0.85, facing=PI)
        self.play(swap(VGroup(stage, late_ring, late_cutter), saved_gel, run_time=0.50))

        self.at("was not protected", lead=0.32)
        digest(self, p["globin"], p["cutters"][2], (-0.26, -0.55, 0), duration=0.89)
        result = label("globin: not protected", -2.12, -1.85, RED, size=30, weight=BOLD)
        self.play(FadeIn(result), run_time=0.40)
        self.finish()


def species_icon(kind, center):
    """Animal silhouettes used only to identify the sources of the three parts."""
    color = GLASS
    body = Ellipse(width=0.63, height=0.34, color=color, fill_opacity=0.78, stroke_width=0)
    head = Circle(radius=0.18, color=color, fill_opacity=0.90, stroke_width=0).move_to(point(0.31, 0.13))
    if kind == "rabbit":
        features = VGroup(Ellipse(width=0.11, height=0.35, color=color, fill_opacity=0.94, stroke_width=0)
                          .rotate(a).move_to(point(x, 0.36)) for a, x in ((0.32, 0.24), (-0.02, 0.39)))
        features.add(Dot(point(-0.37, 0.10), radius=0.105, color=color))
    elif kind == "dog":
        features = VGroup(Ellipse(width=0.28, height=0.16, color=color, fill_opacity=0.90, stroke_width=0)
                          .move_to(point(0.46, 0.08)),
                          Ellipse(width=0.14, height=0.26, color=color, fill_opacity=0.86, stroke_width=0)
                          .rotate(-0.45).move_to(point(0.19, 0.24)),
                          Line(point(-0.26, 0.08), point(-0.45, 0.23), color=color, stroke_width=4))
    else:
        features = VGroup(Dot(point(0.22, 0.26), radius=0.105, color=color),
                          Dot(point(0.49, 0.08), radius=0.053, color=color),
                          ArcBetweenPoints(point(-0.30, -0.01), point(-0.62, 0.13),
                                           angle=-1.5, color=color, stroke_width=3))
    return VGroup(body, head, features).move_to(center)


def species_parts():
    tube = tube_glass()
    gel = gel_panel()
    ribo = chapter_one.ribosome(pos=(-4.75, 1.02, 0), scale=0.57)
    mem = vesicle((-3.39, -0.71, 0), 1.02).set_fill(INDIGO, .42)
    rna = VMobject(stroke_color=TEXT, stroke_width=4)
    rna.set_points_smoothly([point(-1.02, 1.05), point(-1.56, 0.91), point(-2.13, 1.08),
                             point(-2.68, 0.89), point(-3.25, 1.07), point(-3.88, 1.04)])
    return tube, gel, ribo, mem, rna


class S08Species(SpokenScene):
    def construct(self):
        tube, gel, rings, main, inside, bands = assembled_assay()
        _, _, ribo, mem, rna = species_parts()
        self.add(tube, gel, rings, main, inside, bands, film_scope())
        self.at("the parts came")
        self.play(FadeOut(rings), FadeOut(inside), FadeOut(main), run_time=0.76)

        positions = (-5.26, -3.09, -1.18)
        targets = (point(-4.91, 1.91), point(-3.34, 0.35), point(-1.29, 1.18))
        names = ("rabbit", "dog", "mouse")
        colors = (GLASS, INDIGO, TEXT)
        icons, labels, links = VGroup(), VGroup(), VGroup()
        for name, x, target, color in zip(names, positions, targets, colors):
            icon = species_icon(name, point(x, 2.80))
            icons.add(icon)
            labels.add(label(name, x, 3.40))
            links.add(Line(icon.get_bottom() + DOWN * .13, target,
                           color=color, stroke_width=2.5, stroke_opacity=0.55))

        self.at("rabbit ribosomes")
        self.play(FadeIn(ribo, shift=DOWN * .38), run_time=.56)
        self.play(FadeIn(icons[0], shift=DOWN * .14), FadeIn(labels[0]), Create(links[0]), run_time=.62)
        self.at("dog membranes")
        self.play(FadeIn(mem, shift=UP * .34), run_time=.49)
        self.play(FadeIn(icons[1], shift=DOWN * .14), FadeIn(labels[1]), Create(links[1]), run_time=.53)
        self.at("mouse messenger rna")
        self.play(Create(rna), run_time=.39)
        self.play(FadeIn(icons[2], shift=DOWN * .14), FadeIn(labels[2]), Create(links[2]), run_time=.59)

        self.at("still work together")
        self.play(links.animate.set_stroke(width=3.6, opacity=0.95), run_time=0.54)
        cargo = lead_path(signal_chain(ORIGIN, count=9, radius=0.117),
                          [(-3.37, -1.22, 0), (-3.52, -0.62, 0), (-3.65, -0.05, 0),
                           (-4.03, 0.32, 0), (-4.33, 0.57, 0)], 0.245)
        self.play(grow_chain(cargo, 1.38))
        self.play(FadeOut(icons), FadeOut(labels), FadeOut(links), run_time=0.40)

        self.at("ruled out a")
        special = label("special ribosome", -4.30, -1.95)
        self.play(FadeIn(special), run_time=0.56)
        self.at("special secretory ribosome")
        slash = Line(special.get_left() + LEFT * .10, special.get_right() + RIGHT * .10,
                     color=RED, stroke_width=5)
        slash.layout_ok = "covered"  # Strike through the explicitly rejected interpretation.
        self.play(Create(slash), run_time=0.56)
        self.play(FadeOut(special), FadeOut(slash), run_time=0.49)

        self.at("supported an address")
        address = label("address in the growing protein", -2.94, -2.23, GOLD, weight=BOLD)
        tip = VGroup(*cargo[:3])
        self.play(Indicate(tip, color=GOLD, scale_factor=1.18), run_time=0.71)
        self.play(FadeIn(address), run_time=0.64)
        self.finish()


class S09Idea(SpokenScene):
    def construct(self):
        tube, gel, ribo, mem, rna = species_parts()
        cargo = folded_chain(mem.get_center(), radius=0.15)
        surroundings = VGroup(tube, mem, cargo, gel_panel(with_labels=False), band(0), band(1, TRIMMED_Y))
        heads = gel[2]
        self.add(surroundings, heads, ribo, rna, film_scope())
        self.at("so here is")
        self.play(FadeOut(ribo), FadeOut(rna), Indicate(mem, color=INDIGO, scale_factor=1.07),
                  run_time=1.14)
        rules = test_rules()
        self.at("two kinds of test", lead=0.40)
        self.play(FadeIn(rules[0], shift=UP * 0.18), run_time=0.56)
        self.play(FadeIn(rules[1]), run_time=0.57)
        self.at("one shows the protein")
        inset, _ = assay_inset()
        self.play(FadeOut(heads), run_time=0.27)
        interim = surroundings.copy().scale(.67, about_point=point(-5.12, 1.0)).shift(DOWN * .27)
        self.play(Transform(surroundings, interim), run_time=.61)
        self.play(Transform(surroundings, inset), run_time=.79)
        self.at("what sent it", lead=0.52)
        cell = cell_picture(with_ribosome=True).set_z_index(-2)
        self.play(FadeIn(cell), Indicate(rules[1][1], color=GOLD, scale_factor=1.05), run_time=1.17)
        self.finish()


class S10Move(SpokenScene):
    def construct(self):
        cell = cell_picture(with_ribosome=True)
        self.add(cell)
        _, _, rules, tags = cell_index(self)
        ball, signal, donor = transfer_parts()
        self.at("to find the address")
        self.play(FadeOut(cell[-1]), run_time=0.56)
        self.play(FadeIn(ball, scale=0.84), run_time=0.73)
        self.play(FadeIn(donor), FadeIn(signal), run_time=0.71)
        self.at("move a stretch")
        destination = point(-1.90, -0.64)
        arrow = route(point(-2.02, 0.57), point(-1.89, -0.29), GOLD)
        self.play(Create(arrow), run_time=0.53)
        self.play(signal.animate.move_to(destination), FadeOut(donor), run_time=1.39)
        name = label("passenger (cytosolic)", -2.83, -1.46)
        self.play(FadeOut(arrow), FadeIn(name), run_time=0.54)
        self.at("if that passenger")
        outline, target_label = target_compartment()
        self.play(FadeIn(outline), run_time=0.48)
        self.play(FadeIn(target_label), FadeOut(name), run_time=0.43)
        arrow = route(point(-1.40, -0.98), point(0.54, -0.98))
        self.at("moves too", lead=0.15)
        self.play(Create(arrow), run_time=0.33)
        self.play(ball.animate.move_to(point(.80, -.91)), signal.animate.move_to(point(1.95, -.94)),
                  FadeOut(arrow), run_time=1.10)
        self.at("is sufficient", lead=-0.1)
        self.play(FadeIn(tags[0]), rules[1][1].animate.set_color(GOLD), run_time=0.63)
        self.finish()


class S11Delete(SpokenScene):
    def construct(self):
        self.add(cell_picture())
        _, _, _, tags = cell_index(self, tests=1)
        old_result = finished_transfer()
        protein = signal_chain((1.10, -0.12, 0), count=11, angle=PI, radius=0.133)
        self.add(old_result)
        self.at("or delete")
        self.play(FadeOut(old_result), run_time=0.26)
        self.play(FadeIn(protein), run_time=0.34)
        gold_tip = VGroup(*protein[:3])
        remaining = VGroup(*protein[3:])
        scrubber = eraser(point(2.68, 0.36))
        self.play(FadeIn(scrubber, shift=DOWN * 0.19), run_time=0.28)
        self.play(scrubber.animate.shift(LEFT * 0.73 + DOWN * 0.34),
                  LaggedStart(*(FadeOut(b) for b in gold_tip), lag_ratio=0.35), run_time=0.91)
        self.play(FadeOut(scrubber), run_time=0.32)
        self.at("if the protein")
        self.play(remaining.animate.move_to(point(-1.77, -0.80)).rotate(-PI * 0.10), run_time=1.36)
        stranded = label("stranded in cytosol", -1.76, -1.50, RED, size=30, weight=BOLD)
        self.play(FadeIn(stranded), run_time=0.58)
        self.at("is necessary")
        self.play(FadeIn(tags[1]), run_time=0.59)
        self.at("mouse enzyme", lead=0.53)
        cargo = dhfr_block(point(0.40, 0.64))
        description = label("sufficiency test", 0.02, 1.37, GOLD)
        self.play(FadeOut(stranded), FadeOut(remaining), FadeIn(cargo), run_time=0.75)
        self.play(FadeIn(description), Indicate(cargo[1], color=GOLD, scale_factor=1.17), run_time=0.78)
        self.finish()


def gate_membrane(left, right, bottom, top, gate_x, corner, width):
    """Open the membrane path exactly where the blue reader sits."""
    m = VMobject(stroke_color=ORANGE, stroke_width=width)
    m.start_new_path(point(gate_x + .37, top))
    m.add_line_to(point(right - corner, top))
    m.add_quadratic_bezier_curve_to(point(right, top), point(right, top - corner))
    m.add_line_to(point(right, bottom + corner))
    m.add_quadratic_bezier_curve_to(point(right, bottom), point(right - corner, bottom))
    m.add_line_to(point(left + corner, bottom))
    m.add_quadratic_bezier_curve_to(point(left, bottom), point(left, bottom + corner))
    m.add_line_to(point(left, top - corner))
    m.add_quadratic_bezier_curve_to(point(left, top), point(left + corner, top))
    m.add_line_to(point(gate_x - .37, top))
    return m


def reader_gate(x, y):
    return VGroup(*(RoundedRectangle(width=0.25, height=0.31, corner_radius=0.09,
                                     fill_color=BLUE, fill_opacity=0.75, stroke_color=BLUE, stroke_width=2)
                    .move_to(point(x + dx, y)) for dx in (-0.36, 0.36)))


def examples_mito():
    outer = gate_membrane(-6.23, -0.45, -2.50, 1.09, -3.63, .69, 5)
    inner = gate_membrane(-5.70, -1.00, -2.09, .48, -3.63, .57, 4)
    fill = RoundedRectangle(width=5.72, height=3.56, corner_radius=.69,
                            fill_color=ORANGE, fill_opacity=.25, stroke_width=0).move_to(point(-3.34, -.71))
    tom = reader_gate(-3.63, 1.09)
    tim = reader_gate(-3.63, 0.48)
    return VGroup(fill, outer, inner, tom, tim).shift(DOWN * .34)


class S12Examples(SpokenScene):
    def construct(self):
        cell_index(self)
        mito = examples_mito()
        self.at("yeast cytochrome", lead=0)
        self.play(FadeIn(mito), run_time=0.84)
        cargo = dhfr_block(point(-3.43, 1.85))
        self.play(FadeIn(cargo), run_time=0.75)
        precursor = label("COXIV precursor: first 53", -3.35, 1.21, GOLD)
        self.at("first 53")
        self.play(FadeIn(precursor), run_time=0.52)
        self.play(Indicate(cargo[1], color=GOLD, scale_factor=1.18), run_time=0.94)
        tom = label("TOM", -1.98, 0.47, BLUE)
        tim = label("TIM23", -1.97, -0.08, BLUE)
        matrix = label("matrix", -1.97, -1.57, ORANGE)
        self.at("carried mouse dhfr", lead=0.50)
        cargo_name = cargo[0].label
        self.play(FadeOut(precursor), FadeOut(cargo_name), FadeIn(tom), run_time=0.39)
        cargo[0].remove(cargo_name)
        unfolded = signal_chain((-3.63, 1.43, 0), count=10, radius=0.065, angle=PI / 2)
        self.play(FadeOut(cargo[0].box), ReplacementTransform(cargo[1], VGroup(*unfolded[:3])),
                  grow_chain(VGroup(*unfolded[3:]), .66), run_time=.66)
        self.play(unfolded.animate.shift(DOWN * 0.93), FadeIn(tim), run_time=0.91)
        self.at("into the matrix", lead=0.10)
        self.play(unfolded.animate.shift(DOWN * 1.39), run_time=0.95)
        self.play(FadeIn(matrix), FadeIn(success(-3.36, -3.19)), run_time=0.50)

        self.at("adding skl", lead=0.86)
        perox = chapter_one.peroxisome(pos=(4.86, -.56, 0), scale=2.42)
        perox.set_fill(MAGENTA, opacity=.28)
        enzyme = passenger((0.46, -.28, 0), radius=0.164)
        self.play(FadeIn(perox), FadeIn(enzyme), run_time=0.55)
        enzyme_label = label("bacterial enzyme", 1.25, .70)
        self.play(FadeIn(enzyme_label), run_time=0.39)
        skl = boxed_label("SKL", GOLD, size=28, pad=.11, fill_opacity=.18).move_to(point(1.67, -.28))
        self.play(FadeIn(skl, shift=LEFT * .28), run_time=0.74)
        self.at("carboxyl end", lead=0.68)
        reader = RoundedRectangle(width=.35, height=.38, corner_radius=.11,
                                  stroke_color=BLUE, fill_color=BLUE, fill_opacity=.64).move_to(point(2.57, .25))
        pex = place_label(T("PEX5", 28, BLUE), reader, dirs=(UP,), buff=.16)
        self.play(FadeOut(enzyme_label), FadeIn(reader), run_time=0.43)
        self.play(reader.animate.move_to(point(2.34, -.28)), FadeIn(pex), run_time=0.57)
        self.at("sent it into")
        self.play(enzyme.animate.shift(RIGHT * .80), skl.animate.shift(RIGHT * .80),
                  reader.animate.move_to(point(3.14, -.28)), FadeOut(pex), run_time=0.63)
        crossing = VGroup(*(Circle(radius=r, stroke_opacity=0, fill_color=MAGENTA, fill_opacity=opacity)
                            .move_to(point(3.25, -.28)) for r, opacity in ((.68, .12), (.47, .18), (.27, .25))))
        self.play(FadeOut(reader), FadeIn(crossing), run_time=0.30)
        self.play(enzyme.animate.move_to(point(4.45, -.27)), skl.animate.move_to(point(5.66, -.27)),
                  run_time=0.73)
        mammalian = caption("in mammalian cells").move_to(point(4.65, -2.67))
        self.play(FadeOut(crossing), FadeIn(mammalian), FadeIn(success(4.85, -1.34)), run_time=0.54)
        self.finish()


class S13Luciferase(SpokenScene):
    def construct(self):
        self.add(cell_picture())
        _, _, _, tags = cell_index(self, tests=2)
        ball = passenger((-1.61, -.33, 0))
        tail = signal_chain((-2.91, -.34, 0), count=3, radius=0.135)
        name = label("luciferase", -1.64, .78)
        self.at("now the other test")
        self.play(FadeIn(ball), FadeIn(tail), run_time=0.61)
        self.play(FadeIn(name), run_time=0.41)
        self.play(ball.animate.shift(LEFT * 1.04 + UP * .20),
                  tail.animate.shift(LEFT * 1.04 + UP * .20), run_time=0.76)
        self.at("deleting luciferase's", lead=0.28)
        self.play(ball.animate.move_to(point(-1.61, -.33)), tail.animate.move_to(point(-2.91, -.34)),
                  FadeOut(name), run_time=0.52)
        scrubber = eraser(point(-3.65, .03))
        self.play(FadeIn(scrubber, shift=RIGHT * .17), run_time=0.32)
        self.play(scrubber.animate.shift(RIGHT * 1.04 + DOWN * .28),
                  LaggedStart(*(FadeOut(b) for b in tail), lag_ratio=0.45), run_time=1.06)
        self.play(FadeOut(scrubber), run_time=0.25)
        self.at("no more than 12")
        length = label("tail signal: ≤12 amino acids", -1.30, 1.24, GOLD)
        self.play(FadeIn(length), run_time=0.60)
        reader = boxed_label("PEX5", BLUE, size=28, pad=.13).move_to(point(-2.90, .64))
        self.play(FadeIn(reader), run_time=0.55)
        self.at("left it in the cytosol")
        self.play(ball.animate.move_to(point(-3.10, -.68)), run_time=1.28)
        stranded = label("stays in cytosol", -2.63, -1.64, RED, size=30, weight=BOLD)
        self.play(FadeIn(stranded), run_time=0.63)
        self.at("a signal in that tail")
        self.play(Indicate(length, color=GOLD, scale_factor=1.07), run_time=0.68)
        self.at("is necessary")
        self.play(Indicate(tags[1], color=GOLD, scale_factor=1.10), run_time=0.82)
        self.finish()


class S14Cautions(SpokenScene):
    def construct(self):
        cell_index(self, tests=2)
        panels = TwoPanel("", "", top=1.66, bottom=-2.97, gap=.35, width=12.94)
        panels.left_frame.set_fill("#283440", opacity=1)
        panels.right_frame.set_fill("#302D39", opacity=1)
        self.at("two cautions")
        self.play(FadeIn(panels.left_frame), FadeIn(panels.right_frame), run_time=0.68)
        first = passenger((-4.82, .53, 0), radius=0.146)
        tag1 = signal_chain((-3.79, .51, 0), count=3, radius=0.11)
        other = RoundedRectangle(width=1.20, height=.83, corner_radius=.19,
                                 stroke_color=GREY, stroke_width=3,
                                 fill_color=GREY, fill_opacity=.37).move_to(point(-4.82, -.78))
        tag2 = signal_chain((-3.79, -.80, 0), count=3, radius=0.11)
        self.play(FadeIn(first), FadeIn(tag1), run_time=0.67)
        self.at("working for one passenger")
        self.play(GrowFromCenter(label("✓", -2.55, .52, GREEN, size=50, weight=BOLD)), run_time=0.65)
        self.play(FadeIn(other), FadeIn(tag2), run_time=0.85)
        self.at("every passenger", lead=0.31)
        self.play(GrowFromCenter(label("?", -2.55, -.78, size=50, weight=BOLD)), run_time=0.57)
        limit = label("One passenger ≠\nevery passenger", -3.24, -2.08, size=28, weight=BOLD)
        self.play(FadeIn(limit), run_time=0.58)

        self.at("and skl is picky")
        base = tail_tiles(point(3.20, .57))
        self.play(LaggedStart(*(FadeIn(tile, shift=UP * .16) for tile in base), lag_ratio=.31), run_time=1.01)
        self.play(Indicate(base, color=GOLD, scale_factor=1.07), run_time=0.75)
        self.at("in luciferase")
        summary = label("only a few swaps work", 3.22, -2.07, size=29, weight=BOLD)
        outcomes = VGroup()
        # X is an unspecified replacement. These marks illustrate selectivity, with no residue-level data.
        for i, site in enumerate((0, 1, 2, 0)):
            original, marker = base[site], "✓" if i == 1 else "×"
            altered = T("X", 44, GOLD).move_to(original)
            outcome_color = GREEN if i == 1 else RED
            result = boxed_label(marker, outcome_color, size=40, box=(.68, .66),
                                 pad=.12, fill_opacity=.76).move_to(point(1.78 + i * .94, -.80))
            result.label.set_color(BG)
            self.play(original.box.animate.set_fill(GOLD, opacity=.16),
                      swap(original.label, altered, run_time=.27), run_time=.31)
            self.play(FadeIn(result, shift=DOWN * .14), run_time=.31)
            outcomes.add(result)
            self.play(original.box.animate.set_fill(GOLD, opacity=.86),
                      swap(altered, original.label, run_time=.29), run_time=.31)
        self.at("kept it working")
        self.play(FadeIn(summary), Indicate(outcomes[1], color=GREEN, scale_factor=1.08),
                  run_time=.78)
        self.finish()


class S15Return(SpokenScene):
    def construct(self):
        cell = cell_picture()
        self.add(cell)
        inset, mini_vesicle, rules, tags = cell_index(self, tests=2)
        cargo = signal_chain((-0.40, -.25, 0), count=14, gold=3, radius=0.138)
        for bead in cargo[-3:]:
            bead.set_fill(GOLD)
        self.at("when a protein carries")
        self.play(grow_chain(cargo, 1.06))
        self.at("two signals", lead=.10)
        self.play(Indicate(VGroup(*cargo[:3]), color=GOLD, scale_factor=1.19),
                  Indicate(VGroup(*cargo[-3:]), color=GOLD, scale_factor=1.19), run_time=.73)
        self.at("only an experiment", lead=.46)
        left = route(point(-2.69, -.18), point(-3.93, .22), GOLD)
        right = route(point(1.91, -.24), point(2.94, -.15), GOLD)
        self.play(Create(left), Create(right), run_time=.68)
        questions = VGroup(label("?", -3.22, .64, size=48, weight=BOLD),
                           label("?", 2.46, .56, size=48, weight=BOLD))
        self.play(GrowFromCenter(questions[0]), GrowFromCenter(questions[1]), run_time=.42)
        self.play(FadeIn(label("test it", -.44, .68, size=32, weight=BOLD)), run_time=.55)
        self.at("protection shows")
        halo = Circle(radius=0.28, stroke_color=INDIGO, stroke_width=4).move_to(mini_vesicle)
        focus = SurroundingRectangle(inset, buff=.16, corner_radius=.16, stroke_width=0,
                                     fill_color=INDIGO, fill_opacity=.31).set_z_index(-1)
        self.play(FadeIn(focus), Create(halo), inset.animate.set_stroke(opacity=.96),
                  Indicate(rules[0][1], scale_factor=1.04, color=INDIGO), run_time=1.11)
        self.at("moving and deleting")
        focus_tests = SurroundingRectangle(VGroup(rules[1], tags), buff=.13, corner_radius=.14,
                                           stroke_width=0, fill_color=GOLD, fill_opacity=.23).set_z_index(-1)
        self.play(FadeOut(focus), FadeIn(focus_tests),
                  Indicate(rules[1][1], color=GOLD, scale_factor=1.05), run_time=.59)
        self.play(Indicate(tags[0], color=GOLD, scale_factor=1.12),
                  Indicate(tags[1], color=GOLD, scale_factor=1.12), run_time=.89)
        self.finish()


class S16End(EndCard):
    LINE = "Protection shows it got in; moving and deleting show what sent it."
