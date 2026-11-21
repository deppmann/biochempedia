"""The Bean and the Red Cell — animated teaching film for STEMhop.

COLOUR MAP (one colour per concept, consistent across the whole film):
    YELLOW (#F5D547)   = glucose-6-phosphate (G6P) and sugars (ribose)
    ORANGE (#FF8C42)   = pentose phosphate pathway and its enzyme G6PD (the tap)
    PURPLE (#B388EB)   = NADPH
    TEAL   (#3FB8C0)   = glutathione (2 GSH / GSSG) and the antioxidant cycle
    RED    (#FC6255)   = reactive oxygen (8-pointed stars) and oxidative damage
    ROSE   (#E8A0A8)   = red blood cell outline and healthy hemoglobin dots
    OX_HB  (#8D4E45)   = oxidized / clumped hemoglobin (Heinz bodies)
    BEAN   (#9B8D4E)   = fava beans (olive-brown)
    TEXT   (#E8EAF0)   = white electron dots, labels, counters, questions
    GREY   (#8B93A1)   = spleen, infection, malaria parasite, neutral reference

ONE WORLD:
    A single cut-away mature red blood cell seen face-on (ROSE disc), with the ORANGE
    G6PD tap on its left wall feeding PURPLE NADPH dots to the TEAL glutathione cycle
    on its right half, surrounded by ROSE hemoglobin dots.

WHAT CHANGES IN EACH SCENE (computed / state-driven):
    s00_link_and_question : RED stars hit 2 GSH -> GSSG; PURPLE NADPH dots + G6P bars drive recharge; bean plate enters; crack flashes on cell outline.
    s01_title             : Standard TitleCard ("The Bean and the Red Cell").
    s02_red_cell          : Cell scales up; dashed nucleus & mitochondria flash and are crossed out; ribose shrinks; G6PD tap opens and NADPH + G6P stream starts.
    s03_cycle             : Glutathione loop grows; RED stars neutralized at peroxidase; NADPH hands off electrons at reductase; cycle & G6P flux accelerate.
    s04_idea              : Cell pulls back; ORANGE route traces tap -> NADPH -> cycle; cycle tilts toward tap; tap brightens to "G6PD: first step".
    s05_deficiency        : Tap dims & narrows; G6P chips queue; NADPH thins; cycle slows; counter counts to 400 million; X chromosome & XY highlight appear.
    s06_triggers          : Tap steps across 3 severity levels; fava beans, capsule, infection enter & emit bursts of RED stars that overwhelm the slowed cycle.
    s07_cascade           : NADPH drops; 2 GSH fades & cycle stalls; RED stars multiply; ROSE hemoglobin dots migrate into 3 RED-outlined Heinz body knots.
    s08_crisis            : Camera pulls back; 5 damaged cells drift in circulation; 2 burst scattering ROSE dots; 2 are pulled into the spleen; crisis title lands.
    s09_chain             : Main cell returns; 6-chip causal chain builds left-to-right while each matching cellular step updates live inside the cell.
    s10_predict           : Chain dims below; counter counts to 400 million; question "Why is it so common?" appears across the top.
    s11_pause             : PredictPause holding the weakened cell, dimmed chain, counter, and question for 4.5 s while the countdown ring empties.
    s12_malaria           : GREY parasite enters dim-tap cell and fails to thrive ("seems"); cell shifts left; trait & malaria regions slide into partial overlap.
    s13_balanced          : Overlap shapes transform into a rocking balance beam ("balanced polymorphism"); beam wobbles; fades to drug capsule + G6PD screen checklist.
    s14_twist             : Cell returns full size; solid RED arrow grows to bean ("exposed") and dashed arrow grows to parasite ("poorer home?").
    s15_close             : Healthy cycle turns at full speed; G6PD dims, oxidant burst arrives, NADPH thins, loop stalls, and hemoglobin knots form in order.
    s16_end               : Standard EndCard with the take-home line.
"""

from bp_parts import *

# ------------------------------------------------------------------ Film palette
SUGAR = YELLOW
PATHWAY = "#FF8C42"       # ORANGE: PPP & G6PD tap
NADPH_COL = "#B388EB"     # PURPLE: NADPH
GSH_COL = TEAL            # TEAL: glutathione cycle
OXIDANT = RED             # RED: reactive oxygen & damage
CELL_ROSE = "#E8A0A8"     # soft ROSE: RBC outline & healthy hemoglobin
OX_HB = "#8D4E45"         # dull brown-red: oxidized hemoglobin clumps
BEAN_COL = "#9B8D4E"      # olive-brown: fava beans
WHITE_DOT = TEXT


# ------------------------------------------------------------------ Geometry helpers
def oxidant_star(radius=0.18, color=OXIDANT):
    """8-pointed reactive-oxygen star."""
    pts = []
    for i in range(16):
        ang = i * TAU / 16
        r = radius if i % 2 == 0 else radius * 0.42
        pts.append([r * np.cos(ang), r * np.sin(ang), 0.0])
    return Polygon(*pts, stroke_color=color, stroke_width=2.0, fill_color=color, fill_opacity=0.92)


def nadph_dot(radius=0.13):
    """PURPLE NADPH circle carrying two small white electron dots."""
    core = Circle(radius=radius, color=NADPH_COL, stroke_width=1.6, fill_color=NADPH_COL, fill_opacity=0.95)
    e1 = Dot(radius=0.042, color=WHITE_DOT).shift(LEFT * radius * 0.36)
    e2 = Dot(radius=0.042, color=WHITE_DOT).shift(RIGHT * radius * 0.36)
    return VGroup(core, e1, e2)


def sugar_bar(n_carbons=6, color=SUGAR, unit=0.12, label=None):
    """Row of n_carbons square tiles (no rings/molecular structures)."""
    tiles = VGroup(*[
        Square(side_length=unit, stroke_color=color, stroke_width=1.8, fill_color=color, fill_opacity=0.80)
        for _ in range(n_carbons)
    ]).arrange(RIGHT, buff=0.025)
    if label:
        t = T(label, size=24, color=color).next_to(tiles, UP, buff=0.08)
        return VGroup(tiles, t)
    return tiles


def fava_plate(scale=1.0):
    """Three plain olive-brown beans on a pale rimmed plate (not green, no structures)."""
    plate = Ellipse(width=1.65, height=0.85, stroke_color=GREY, stroke_width=2.5, fill_color=GREY, fill_opacity=0.18)
    beans = VGroup()
    for pos, ang in [([-0.38, 0.08, 0], 0.25), ([0.15, 0.14, 0], -0.2), ([-0.08, -0.14, 0], 0.08)]:
        b = Ellipse(width=0.52, height=0.30, stroke_color="#C7B86B", stroke_width=2.0,
                    fill_color=BEAN_COL, fill_opacity=0.95).rotate(ang).move_to(pos)
        beans.add(b)
    return VGroup(plate, beans).scale(scale)


def drug_capsule(scale=1.0):
    """Plain white/grey two-tone capsule icon (no drug name)."""
    left = RoundedRectangle(corner_radius=0.18, width=0.58, height=0.36, stroke_color=TEXT, stroke_width=2.5,
                            fill_color=TEXT, fill_opacity=0.88).shift(LEFT * 0.24)
    right = RoundedRectangle(corner_radius=0.18, width=0.58, height=0.36, stroke_color=TEXT, stroke_width=2.5,
                             fill_color=GREY, fill_opacity=0.40).shift(RIGHT * 0.24)
    seam = Line([0, -0.18, 0], [0, 0.18, 0], color=BG, stroke_width=2.5)
    return VGroup(left, right, seam).scale(scale)


def infection_blob(scale=1.0):
    """Simple GREY irregular infection blob (not a molecular structure)."""
    pts = []
    for i in range(12):
        ang = i * TAU / 12
        r = 0.42 + (0.09 if i % 2 == 0 else -0.05)
        pts.append([r * np.cos(ang), r * np.sin(ang), 0.0])
    blob = Polygon(*pts, stroke_color=TEXT, stroke_width=2.0, fill_color=GREY, fill_opacity=0.60)
    blob.make_smooth()
    dots = VGroup(*[
        Dot(radius=0.05, color=TEXT).move_to(p)
        for p in ([-0.14, 0.1, 0], [0.16, 0.05, 0], [-0.02, -0.15, 0])
    ])
    return VGroup(blob, dots).scale(scale)


def parasite_oval(scale=1.0):
    """Simple cartoon oval with inner dot for Plasmodium falciparum."""
    outer = Ellipse(width=0.68, height=0.36, stroke_color=TEXT, stroke_width=2.2, fill_color=GREY, fill_opacity=0.60)
    inner = Dot(radius=0.07, color=TEXT).shift(LEFT * 0.1)
    return VGroup(outer, inner).scale(scale)


def person_icon(tag_text, color=TEXT, glow_color=None):
    """Simple human silhouette icon with chromosome tag (XY or XX)."""
    head = Circle(radius=0.18, stroke_color=color, stroke_width=2.5,
                  fill_color=glow_color or color, fill_opacity=0.42 if glow_color else 0.16)
    body = RoundedRectangle(corner_radius=0.14, width=0.46, height=0.68, stroke_color=color, stroke_width=2.5,
                            fill_color=glow_color or color, fill_opacity=0.42 if glow_color else 0.16)
    body.next_to(head, DOWN, buff=0.08)
    tag = T(tag_text, size=28, color=glow_color or color, weight=BOLD).next_to(body, DOWN, buff=0.14)
    return VGroup(head, body, tag)


def make_tap(pos, scale=1.0, strength=1.0):
    """ORANGE G6PD valve/tap sitting on the cell membrane wall."""
    pipe = RoundedRectangle(corner_radius=0.08, width=0.58 * scale, height=0.36 * scale,
                            stroke_color=PATHWAY, stroke_width=2.8, fill_color=PATHWAY,
                            fill_opacity=0.25 + 0.58 * strength).move_to(pos)
    stem = Line(pipe.get_top(), pipe.get_top() + UP * 0.18 * scale, color=PATHWAY, stroke_width=3.6 * scale)
    handle_w = (0.18 + 0.36 * strength) * scale
    handle = Line(stem.get_end() + LEFT * handle_w / 2, stem.get_end() + RIGHT * handle_w / 2,
                  color=PATHWAY, stroke_width=5.2 * scale)
    g = VGroup(pipe, stem, handle)
    g.set_opacity(0.48 + 0.52 * strength)
    g.pipe = pipe
    g.handle = handle
    return g


def tap_label_above(tap, text, color=PATHWAY, size=28):
    """Place tap label cleanly to the left and above the tap, strictly clear of the cell wall and G6P lane."""
    # Wrap at colon or space so it sits compactly in [-6.15, tap_left - 0.16]
    if ": " in text:
        wrapped = text.replace(": ", ":\n", 1)
    elif " " in text and len(text) > 8:
        wrapped = text.replace(" ", "\n", 1)
    else:
        wrapped = text
    lab = T(wrapped, size=size, color=color, line_spacing=0.88)
    target_x = tap.get_left()[0] - 0.16 - lab.width / 2
    min_x = -6.15 + lab.width / 2
    lab.move_to([max(target_x, min_x), tap.get_top()[1] + 0.35 + lab.height / 2, 0.0])
    return lab


def hb_positions(center, radius, seed=7, count=22):
    """Deterministic hemoglobin positions inside the left/upper/lower crescent (clear of loop & labels)."""
    rng = np.random.default_rng(seed)
    pts = []
    cx, cy = center[0], center[1]
    tries = 0
    while len(pts) < count and tries < 2500:
        tries += 1
        x = rng.uniform(-radius * 0.80, radius * 0.65)
        y = rng.uniform(-radius * 0.80, radius * 0.80)
        r2 = x * x + y * y
        if r2 > (radius * 0.80) ** 2 or r2 < (radius * 0.16) ** 2:
            continue
        # Keep clear of the right glutathione loop zone and enzyme labels
        if x > -0.54 * radius and abs(y) < 0.78 * radius:
            continue
        # Keep clear of the G6PD tap mouth
        if x < -0.58 * radius and abs(y) < 0.24 * radius:
            continue
        if any(np.hypot(x - px, y - py) < 0.28 * (radius / 2.45) for px, py in pts):
            continue
        pts.append((x, y))
    return [np.array([cx + x, cy + y, 0.0]) for x, y in pts]


class RedCellWorld:
    """Reusable cut-away red blood cell + G6PD tap + glutathione cycle + hemoglobin dots."""

    def __init__(self, center=(-1.15, -0.1, 0.0), radius=2.45, g6pd=1.0, show_loop=True,
                 show_tap=True, show_enzyme_labels=False, loop_scale=1.0, compact_loop=False, seed=7):
        self.center = np.array(center, dtype=float)
        self.radius = float(radius)
        self.s = self.radius / 2.45
        self.compact_loop = compact_loop

        # Cell body: biconcave disc with visible ROSE fill (0.16) + soft inner dimple shading (no hard wireframe ring)
        self.outer = Circle(radius=self.radius, stroke_color=CELL_ROSE, stroke_width=5.5,
                            fill_color=CELL_ROSE, fill_opacity=0.16).move_to(self.center)
        self.dimple = Circle(radius=self.radius * 0.54, stroke_width=0.0,
                             fill_color=CELL_ROSE, fill_opacity=0.08).move_to(self.center)
        self.dimple.layout_ok = True

        # Hemoglobin dots in the crescent
        self.hb_home = hb_positions(self.center, self.radius, seed=seed, count=22)
        self.hb_dots = VGroup(*[
            Circle(radius=0.105 * self.s, stroke_color=CELL_ROSE, stroke_width=1.2,
                   fill_color=CELL_ROSE, fill_opacity=0.88).move_to(p)
            for p in self.hb_home
        ])

        # G6PD tap on the left wall
        self.tap_pos = self.center + LEFT * self.radius
        self.tap = make_tap(self.tap_pos, scale=self.s, strength=g6pd)

        # Glutathione cycle in the right half of the cell
        lc = self.center + RIGHT * (0.65 * self.s)
        ls = self.s * loop_scale
        self.loop_center = lc
        if compact_loop:
            # Thumbnail mode (when cell is in left third): clean unlabelled TEAL cycle arcs, no tiny text
            self.gsh_chip = RoundedRectangle(corner_radius=0.10, width=0.52, height=0.28, stroke_color=GSH_COL,
                                             stroke_width=2.2, fill_color=GSH_COL, fill_opacity=0.22).move_to(lc + LEFT * 0.45)
            self.gssg_chip = RoundedRectangle(corner_radius=0.10, width=0.52, height=0.28, stroke_color=GSH_COL,
                                              stroke_width=2.2, fill_color=GSH_COL, fill_opacity=0.22).move_to(lc + RIGHT * 0.45)
            self.top_arc = CurvedArrow(self.gsh_chip.get_top() + UP * 0.08, self.gssg_chip.get_top() + UP * 0.08,
                                       angle=-0.85, color=GSH_COL, stroke_width=2.6, tip_length=0.14)
            self.bot_arc = CurvedArrow(self.gssg_chip.get_bottom() + DOWN * 0.08, self.gsh_chip.get_bottom() + DOWN * 0.08,
                                       angle=-0.85, color=GSH_COL, stroke_width=2.6, tip_length=0.14)
        else:
            sz = max(24, int(round(26 * ls)))
            self.gsh_chip = boxed_label("2 GSH", GSH_COL, size=sz, pad=0.15 * ls)
            self.gssg_chip = boxed_label("GSSG", GSH_COL, size=sz, pad=0.15 * ls)
            self.gsh_chip.move_to(lc + LEFT * (0.88 * ls))
            self.gssg_chip.move_to(lc + RIGHT * (0.86 * ls))
            top_start = self.gsh_chip.get_top() + UP * (0.14 * ls)
            top_end = self.gssg_chip.get_top() + UP * (0.14 * ls)
            bot_start = self.gssg_chip.get_bottom() + DOWN * (0.14 * ls)
            bot_end = self.gsh_chip.get_bottom() + DOWN * (0.14 * ls)
            self.top_arc = CurvedArrow(top_start, top_end, angle=-0.88, color=GSH_COL, stroke_width=3.6 * ls,
                                       tip_length=0.20 * ls)
            self.bot_arc = CurvedArrow(bot_start, bot_end, angle=-0.88, color=GSH_COL, stroke_width=3.6 * ls,
                                       tip_length=0.20 * ls)

        self.loop_group = VGroup(self.gsh_chip, self.gssg_chip, self.top_arc, self.bot_arc)
        self.perox_label = T("peroxidase", size=28, color=TEXT).next_to(self.top_arc, UP, buff=0.58 * ls)
        self.reduc_label = T("reductase", size=28, color=TEXT).next_to(self.bot_arc, DOWN, buff=0.34 * ls)

        self.root = VGroup(self.outer, self.dimple, self.hb_dots)
        if show_loop:
            self.root.add(self.loop_group)
        if show_enzyme_labels:
            self.root.add(self.perox_label, self.reduc_label)
        if show_tap:
            self.root.add(self.tap)

        self.top_arc.layout_ok = "near"
        self.bot_arc.layout_ok = "near"

    def nadph_path_point(self, alpha):
        """Smooth path from tap exit into the bottom glutathione reductase arc."""
        p0 = self.tap_pos + RIGHT * (0.34 * self.s)
        p1 = np.array([self.center[0] - 0.85 * self.s, self.center[1] - 0.55 * self.s, 0.0])
        p2 = self.bot_arc.point_from_proportion(0.5) + DOWN * (0.14 * self.s)
        t = float(np.clip(alpha, 0.0, 1.0))
        return (1 - t) ** 2 * p0 + 2 * (1 - t) * t * p1 + t ** 2 * p2

    def g6p_path_point(self, alpha):
        """Incoming G6P sugar path from left plasma into the G6PD tap."""
        p0 = self.tap_pos + LEFT * (2.2 * self.s)
        p1 = self.tap_pos + LEFT * (0.28 * self.s)
        t = float(np.clip(alpha, 0.0, 1.0))
        return (1 - t) * p0 + t * p1

    def attach_cycle_flow(self, rate_tracker, nadph_tracker=None, show_g6p=True, show_oxidants=False):
        """Attach computed cycle token, NADPH stream, G6P feed, and optional incoming peroxide stars."""
        phase = ValueTracker(0.0)
        n_phase = ValueTracker(0.0)
        g_phase = ValueTracker(0.0)
        ox_phase = ValueTracker(0.0)

        tok_top = Dot(radius=0.14 * self.s, color=GSH_COL, stroke_color=TEXT, stroke_width=2.0)
        tok_bot = Dot(radius=0.14 * self.s, color=GSH_COL, stroke_color=TEXT, stroke_width=2.0)
        ring_pulse = Circle(radius=0.22 * self.s, color=GSH_COL, stroke_color=GSH_COL, stroke_width=2.5, fill_opacity=0)

        def upd_top(m, dt):
            r = max(0.0, rate_tracker.get_value())
            phase.set_value((phase.get_value() + dt * 0.45 * r) % 1.0)
            m.move_to(self.top_arc.point_from_proportion(phase.get_value()))
            m.set_opacity(1.0 if r > 0.03 else 0.0)

        def upd_bot(m, dt):
            r = max(0.0, rate_tracker.get_value())
            p = (phase.get_value() + 0.5) % 1.0
            m.move_to(self.bot_arc.point_from_proportion(p))
            m.set_opacity(1.0 if r > 0.03 else 0.0)

        def upd_ring(m, dt):
            r = max(0.0, rate_tracker.get_value())
            m.move_to(self.top_arc.point_from_proportion(phase.get_value()))
            m.set_stroke(GSH_COL, opacity=0.75 if r > 0.03 else 0.0)
            m.set_fill(opacity=0.0)

        tok_top.add_updater(upd_top)
        tok_bot.add_updater(upd_bot)
        ring_pulse.add_updater(upd_ring)
        tok_top.set_z_index(1)
        tok_bot.set_z_index(1)
        ring_pulse.set_z_index(1)

        flow_grp = VGroup(tok_top, tok_bot, ring_pulse)

        # PURPLE NADPH + electron dots
        for k in range(4):
            nd = nadph_dot(radius=0.125 * self.s)
            nd.set_z_index(1)
            nd.layout_ok = True

            def make_n_upd(idx):
                def upd(m, dt):
                    nr = nadph_tracker.get_value() if nadph_tracker is not None else rate_tracker.get_value()
                    if idx == 0:
                        n_phase.set_value((n_phase.get_value() + dt * 0.48 * max(0.10, nr)) % 1.0)
                    if nr <= 0.01:
                        m.set_opacity(0.0)
                    elif nr < 0.20:
                        m.set_opacity(0.90 if idx == 0 else 0.0)
                    elif nr < 0.55:
                        m.set_opacity(0.95 if idx < 2 else 0.0)
                    else:
                        m.set_opacity(1.0)
                    u = (n_phase.get_value() + idx / 4.0) % 1.0
                    m.move_to(self.nadph_path_point(u))
                return upd

            nd.add_updater(make_n_upd(k))
            flow_grp.add(nd)

        # YELLOW G6P sugar bars entering tap
        if show_g6p:
            for k in range(2):
                bar = sugar_bar(6, color=SUGAR, unit=0.11 * self.s)
                bar.set_z_index(1)
                bar.layout_ok = True

                def make_g_upd(idx):
                    def upd(m, dt):
                        nr = nadph_tracker.get_value() if nadph_tracker is not None else rate_tracker.get_value()
                        if idx == 0:
                            g_phase.set_value((g_phase.get_value() + dt * 0.42 * max(0.12, nr)) % 1.0)
                        u = (g_phase.get_value() + idx * 0.5) % 1.0
                        m.move_to(self.g6p_path_point(u))
                        m.set_opacity(0.92 * (1.0 - 0.5 * u) if nr > 0.04 else 0.25)
                    return upd

                bar.add_updater(make_g_upd(k))
                flow_grp.add(bar)

        # Continuous incoming peroxide stars being neutralized at the top arrow (strictly above GSSG, below "peroxidase")
        if show_oxidants:
            for k in range(2):
                st = oxidant_star(0.19 * self.s)
                st.set_z_index(1)
                p_start = self.center + RIGHT * (3.1 * self.s) + UP * ((0.92 + 0.04 * k) * self.s)
                p_hit = self.top_arc.point_from_proportion(0.45) + UP * (0.14 * self.s)

                def make_o_upd(idx, a=p_start, b=p_hit):
                    def upd(m, dt):
                        r = max(0.0, rate_tracker.get_value())
                        if idx == 0:
                            ox_phase.set_value((ox_phase.get_value() + dt * 0.48 * max(0.15, r)) % 1.0)
                        if r < 0.05:
                            m.set_opacity(0.0)
                            return
                        u = (ox_phase.get_value() + idx * 0.5) % 1.0
                        m.move_to((1 - u) * a + u * b)
                        m.set_opacity(1.0 - (u - 0.78) / 0.22 if u > 0.78 else 1.0)
                    return upd

                st.add_updater(make_o_upd(k))
                flow_grp.add(st)

        return flow_grp


def make_chain_chips(y=-2.28):
    """Build the 6-chip causal chain across the bottom third at >= 24 pt (no downscaling)."""
    specs = [
        ("G6PD\ndown", PATHWAY),
        ("NADPH\ndown", NADPH_COL),
        ("GSH\ndown", GSH_COL),
        ("reactive\noxygen up", OXIDANT),
        ("Heinz\nbodies", OX_HB),
        ("cells\nlost", TEXT),
    ]
    chips = []
    for txt, col in specs:
        lab = T(txt, size=24, color=TEXT if col in (OX_HB, TEXT) else col, line_spacing=0.82)
        w = max(1.56, lab.width + 0.34)
        h = max(0.90, lab.height + 0.28)
        box = RoundedRectangle(corner_radius=0.14, width=w, height=h, stroke_color=col, stroke_width=2.6,
                               fill_color=col, fill_opacity=0.18)
        chips.append(VGroup(box, lab.move_to(box)))
    row = VGroup()
    arrows = []
    for i, c in enumerate(chips):
        row.add(c)
        if i < len(chips) - 1:
            arr = Arrow(ORIGIN, RIGHT * 0.28, buff=0, stroke_width=2.6, max_tip_length_to_length_ratio=0.38, color=GREY)
            arrows.append(arr)
            row.add(arr)
    row.arrange(RIGHT, buff=0.06).move_to([0.0, y, 0.0])
    return row, chips, arrows


# ------------------------------------------------------------------ Scenes
class S00LinkAndQuestion(SpokenScene):
    def construct(self):
        world = RedCellWorld(center=(-1.1, -0.25, 0.0), radius=2.45, g6pd=1.0, show_loop=True, show_tap=True)
        rate = ValueTracker(0.85)
        flow = world.attach_cycle_flow(rate, show_g6p=True, show_oxidants=False)
        tag = scope_tag("schematic")
        q_top = T("Why can beans destroy red cells?", size=38, color=TEXT).move_to([0.0, 3.22, 0.0])

        self.add(world.root, flow, tag)

        # Oxidant hit on 2 GSH -> GSSG
        self.at("glutathione")
        star = oxidant_star(0.20).move_to([2.8, 1.35, 0.0])
        self.play(FadeIn(star), run_time=0.25)

        self.at("oxidant hits")
        self.play(star.animate.move_to(world.gsh_chip.get_top() + UP * 0.20), run_time=0.55)
        puff = Circle(radius=0.22, stroke_color=GREY, stroke_width=2.5, fill_color=GREY, fill_opacity=0.4).move_to(star)
        self.play(ReplacementTransform(star, puff), run_time=0.25)
        self.play(FadeOut(puff), run_time=0.25)

        self.at("recharged it")
        e_hand = VGroup(Dot(radius=0.06, color=WHITE_DOT), Dot(radius=0.06, color=WHITE_DOT)).arrange(RIGHT, buff=0.08)
        e_hand.move_to(world.bot_arc.point_from_proportion(0.5))
        self.play(FadeIn(e_hand, scale=1.3), rate.animate.set_value(1.25), run_time=0.6)
        self.play(e_hand.animate.move_to(world.gsh_chip.get_bottom() + DOWN * 0.12).set_opacity(0.0), run_time=0.9)
        self.remove(e_hand)

        # Fava beans slide in on right
        self.at("fava beans")
        plate = fava_plate(scale=1.18).move_to([4.5, 0.0, 0.0])
        plate_lab = T("fava beans", size=28, color=TEXT).next_to(plate, DOWN, buff=0.25)
        beans_grp = VGroup(plate, plate_lab)
        self.play(FadeIn(beans_grp, shift=LEFT * 1.2), FadeIn(q_top, shift=DOWN * 0.15), run_time=0.7)

        # Teaser crack on cell outline
        self.at("destroy")
        p_top = world.outer.point_at_angle(2.1)
        p_mid1 = world.center + np.array([-1.5, 0.5, 0.0])
        p_mid2 = world.center + np.array([-1.7, -0.4, 0.0])
        p_bot = world.outer.point_at_angle(4.2)
        crack = VMobject(stroke_color=OXIDANT, stroke_width=4.8)
        crack.set_points_as_corners([p_top, p_mid1, p_mid2, p_bot])
        self.play(world.outer.animate.set_stroke(OXIDANT, width=7.0), Create(crack), run_time=0.45)
        self.play(world.outer.animate.set_stroke(CELL_ROSE, width=5.5), FadeOut(crack), run_time=0.55)
        self.finish()


class S01Title(TitleCard):
    LESSON = "The Pentose Phosphate Pathway: NADPH and Five-Carbon Sugars"
    TITLE = "The Bean and the Red Cell"


class S02RedCell(SpokenScene):
    def construct(self):
        world = RedCellWorld(center=(-0.6, -0.1, 0.0), radius=2.60, g6pd=1.0, show_loop=True, show_tap=False)
        world.gsh_chip[0].set_fill(GSH_COL, opacity=0.08).set_stroke(opacity=0.65)
        world.gssg_chip[0].set_fill(GSH_COL, opacity=0.08).set_stroke(opacity=0.65)
        world.top_arc.set_stroke(opacity=0.55)
        world.bot_arc.set_stroke(opacity=0.55)
        rate = ValueTracker(0.28)
        nadph_r = ValueTracker(0.0)
        flow = world.attach_cycle_flow(rate, nadph_tracker=nadph_r, show_g6p=False, show_oxidants=False)
        for m in flow[3:]:
            m.set_opacity(0.0)
        tag = scope_tag("schematic")
        self.add(world.outer, world.dimple, world.hb_dots, world.loop_group, flow, tag)

        # Ease in smoothly up to the "no nucleus" cue
        self.play(world.root.animate.scale(1.06), run_time=3.1)

        # No nucleus (upper-left open pocket, clear of 2 GSH and Hb dots)
        self.at("no nucleus")
        nuc_pos = world.center + np.array([-0.75, 1.35, 0.0])
        nuc = DashedVMobject(Circle(radius=0.52, color=GREY, stroke_width=3.5), num_dashes=16).move_to(nuc_pos)
        nuc_lab = T("nucleus", size=28, color=TEXT).next_to(nuc, RIGHT, buff=0.18)
        cross1 = VGroup(
            Line(nuc.get_corner(DL), nuc.get_corner(UR), color=OXIDANT, stroke_width=4.5),
            Line(nuc.get_corner(UL), nuc.get_corner(DR), color=OXIDANT, stroke_width=4.5),
        )
        cross1.layout_ok = True
        self.play(FadeIn(nuc), FadeIn(nuc_lab), run_time=0.35)
        self.play(Create(cross1), run_time=0.30)
        self.play(FadeOut(nuc), FadeOut(nuc_lab), FadeOut(cross1), run_time=0.35)

        # No mitochondria (lower open pocket below loop, clear of dimple, outer wall, and Hb dots)
        self.at("no mitochondria")
        m_pos = world.center + np.array([0.45, -1.25, 0.0])
        m1 = DashedVMobject(Ellipse(width=0.64, height=0.30, color=GREY, stroke_width=3.2), num_dashes=12).move_to(m_pos + LEFT * 0.38)
        m2 = DashedVMobject(Ellipse(width=0.64, height=0.30, color=GREY, stroke_width=3.2), num_dashes=12).move_to(m_pos + RIGHT * 0.38)
        mitos = VGroup(m1, m2)
        mito_lab = T("mitochondria", size=28, color=TEXT).next_to(mitos, DOWN, buff=0.14)
        cross2 = VGroup(
            Line(mitos.get_corner(DL), mitos.get_corner(UR), color=OXIDANT, stroke_width=4.5),
            Line(mitos.get_corner(UL), mitos.get_corner(DR), color=OXIDANT, stroke_width=4.5),
        )
        cross2.layout_ok = True
        self.play(FadeIn(mitos), FadeIn(mito_lab), run_time=0.35)
        self.play(Create(cross2), run_time=0.30)
        self.play(FadeOut(mitos), FadeOut(mito_lab), FadeOut(cross2), run_time=0.35)

        # Little ribose
        self.at("It needs little")
        rib = sugar_bar(5, color=SUGAR, unit=0.18, label="ribose").move_to(world.center + UP * 1.45 + RIGHT * 0.35)
        self.play(FadeIn(rib), run_time=0.45)
        self.play(rib.animate.scale(0.15).set_opacity(0.0), run_time=1.3)
        self.remove(rib)

        # NADPH stream & G6PD tap (restore loop cleanly without solid fill!)
        self.at("NADPH")
        self.remove(flow)
        flow_full = world.attach_cycle_flow(rate, show_g6p=True, show_oxidants=False)
        self.play(
            FadeIn(world.tap),
            rate.animate.set_value(0.95),
            world.gsh_chip[0].animate.set_fill(GSH_COL, opacity=0.16).set_stroke(opacity=1.0),
            world.gsh_chip[1].animate.set_opacity(1.0),
            world.gssg_chip[0].animate.set_fill(GSH_COL, opacity=0.16).set_stroke(opacity=1.0),
            world.gssg_chip[1].animate.set_opacity(1.0),
            world.top_arc.animate.set_stroke(opacity=1.0),
            world.bot_arc.animate.set_stroke(opacity=1.0),
            run_time=0.65,
        )
        self.add(flow_full)

        self.at("this pathway")
        tap_lab = tap_label_above(world.tap, "G6PD: the tap")
        self.play(FadeIn(tap_lab), run_time=0.5)
        self.finish()


class S03Cycle(SpokenScene):
    def construct(self):
        world = RedCellWorld(center=(-0.6, -0.1, 0.0), radius=2.65, g6pd=1.0, show_loop=True,
                             show_tap=True, loop_scale=1.18)
        tap_lab = tap_label_above(world.tap, "G6PD: the tap")
        rate = ValueTracker(0.55)
        flow = world.attach_cycle_flow(rate, show_g6p=True, show_oxidants=True)
        tag = scope_tag("schematic")
        self.add(world.root, tap_lab, flow, tag)

        self.at("glutathione peroxidase")
        self.play(FadeIn(world.perox_label, shift=DOWN * 0.1), run_time=0.45)

        self.at("neutralize peroxides")
        star = oxidant_star(0.22).move_to([3.8, 1.55, 0.0])
        self.play(FadeIn(star), run_time=0.25)
        self.play(star.animate.move_to(world.gsh_chip.get_top() + UP * 0.24), run_time=0.65)
        puff = Circle(radius=0.24, stroke_color=GREY, stroke_width=2.5, fill_color=GREY, fill_opacity=0.45).move_to(star)
        self.play(ReplacementTransform(star, puff), run_time=0.25)
        self.play(FadeOut(puff), run_time=0.30)

        self.at("Glutathione reductase")
        self.play(FadeIn(world.reduc_label, shift=UP * 0.1), run_time=0.45)

        self.at("NADPH")
        e_burst = VGroup(Dot(radius=0.055, color=WHITE_DOT), Dot(radius=0.055, color=WHITE_DOT)).arrange(RIGHT, buff=0.08)
        e_burst.move_to(world.bot_arc.point_from_proportion(0.5))
        self.play(FadeIn(e_burst, scale=1.4), run_time=0.25)

        self.at("restore it")
        self.play(e_burst.animate.move_to(world.gsh_chip.get_bottom() + DOWN * 0.12).set_opacity(0.0), run_time=0.6)
        self.remove(e_burst)

        self.at("turns")
        self.play(rate.animate.set_value(1.25), run_time=0.8)
        self.finish()


class S04Idea(SpokenScene):
    def construct(self):
        world = RedCellWorld(center=(-0.6, -0.25, 0.0), radius=2.45, g6pd=1.0, show_loop=True,
                             show_tap=True, show_enzyme_labels=True)
        tap_lab = tap_label_above(world.tap, "G6PD: the tap")
        rate = ValueTracker(1.1)
        flow = world.attach_cycle_flow(rate, show_g6p=True, show_oxidants=True)
        head = T("One enzyme carries the cycle", size=38, color=TEXT).move_to([0.0, 3.22, 0.0])
        tag = scope_tag("schematic")
        self.add(world.root, tap_lab, flow, head, tag)

        # Trace bright ORANGE line from tap -> NADPH path -> around 2 GSH -> top arc -> GSSG
        pts = [world.nadph_path_point(a) for a in np.linspace(0, 1, 20)]
        pts += [world.bot_arc.point_from_proportion(a) + DOWN * 0.05 for a in np.linspace(0.5, 1.0, 12)]
        pts += [
            world.gsh_chip.get_left() + LEFT * 0.22 + DOWN * 0.22,
            world.gsh_chip.get_left() + LEFT * 0.22 + UP * 0.22,
        ]
        pts += [world.top_arc.point_from_proportion(a) + UP * 0.08 for a in np.linspace(0.0, 1.0, 20)]
        route = VMobject(stroke_color=PATHWAY, stroke_width=5.5, stroke_opacity=0.85)
        route.set_points_as_corners(pts)
        self.play(Create(route), run_time=1.35)

        self.at("on one enzyme")
        pivot = world.gsh_chip.get_left()
        tilt_grp = VGroup(world.loop_group, world.perox_label, world.reduc_label, route)
        self.play(Rotate(tilt_grp, angle=0.14, about_point=pivot), run_time=0.55)
        self.play(Rotate(tilt_grp, angle=-0.14, about_point=pivot), run_time=0.55)

        self.at("It is G6PD")
        new_lab = tap_label_above(world.tap, "G6PD: first step", size=30).set_weight(BOLD)
        self.play(world.tap.animate.scale(1.18), swap(tap_lab, new_lab, run_time=0.65), run_time=0.65)

        self.at("first step")
        self.play(FadeOut(route), run_time=0.6)
        self.finish()


class S05Deficiency(SpokenScene):
    def construct(self):
        world = RedCellWorld(center=(-1.20, -0.1, 0.0), radius=2.40, g6pd=1.0, show_loop=True,
                             show_tap=True, show_enzyme_labels=True)
        tap_lab = tap_label_above(world.tap, "G6PD: first step")
        rate = ValueTracker(1.0)
        flow = world.attach_cycle_flow(rate, show_g6p=False, show_oxidants=False)
        tag = scope_tag("schematic")
        self.add(world.root, tap_lab, flow, tag)

        # Weaken the tap: dims to ~40%, handle narrows, G6P chips queue outside over 5.0s
        self.at("weakens that step")
        weak_tap = make_tap(world.tap_pos, scale=world.s, strength=0.28)
        q1 = sugar_bar(6, color=SUGAR, unit=0.11).move_to(world.tap_pos + LEFT * 0.85)
        q2 = sugar_bar(6, color=SUGAR, unit=0.11).move_to(world.tap_pos + LEFT * 1.75)
        q3 = sugar_bar(6, color=SUGAR, unit=0.11).move_to(world.tap_pos + LEFT * 1.95 + DOWN * 0.42)
        self.play(
            Transform(world.tap, weak_tap),
            rate.animate.set_value(0.35),
            FadeIn(q1), FadeIn(q2),
            run_time=1.5,
        )
        self.play(FadeIn(q3), q1.animate.shift(RIGHT * 0.30), q2.animate.shift(RIGHT * 0.25), run_time=1.6)
        self.play(q2.animate.shift(RIGHT * 0.15), q3.animate.shift(RIGHT * 0.45 + UP * 0.25), run_time=1.8)

        # Counter: ~400 million people
        self.at("400 million")
        pop = ValueTracker(0)
        pop_counter = counter("~{:.0f} million people", pop, at=[3.85, 2.25, 0.0], size=34, color=TEXT)
        self.add(pop_counter)
        self.play(pop.animate.set_value(400), run_time=1.3)

        # X chromosome + XY / XX figures
        self.at("X chromosome")
        x_glyph = T("X", size=54, color=TEXT, weight=BOLD).move_to([3.95, 2.25, 0.0])
        x_sub = T("gene on X", size=28, color=TEXT).next_to(x_glyph, DOWN, buff=0.16)
        x_grp = VGroup(x_glyph, x_sub)
        xy = person_icon("XY", color=TEXT).move_to([2.95, -0.35, 0.0])
        xx = person_icon("XX", color=TEXT).move_to([4.95, -0.35, 0.0])
        self.play(FadeOut(pop_counter), run_time=0.25)
        self.play(FadeIn(x_grp), FadeIn(xy), FadeIn(xx), run_time=0.65)

        self.at("males are affected")
        xy_glow = person_icon("XY", color=PATHWAY, glow_color=PATHWAY).move_to(xy)
        self.play(Transform(xy, xy_glow), run_time=0.6)
        self.finish()


class S06Triggers(SpokenScene):
    def construct(self):
        world = RedCellWorld(center=(-1.20, -0.1, 0.0), radius=2.40, g6pd=0.28, show_loop=True,
                             show_tap=True, show_enzyme_labels=True)
        tap_lab = tap_label_above(world.tap, "G6PD: weak tap")
        rate = ValueTracker(0.35)
        flow = world.attach_cycle_flow(rate, show_g6p=True, show_oxidants=False)
        tag = scope_tag("schematic")
        self.add(world.root, tap_lab, flow, tag)

        # Three severity levels (schematic, no numbers) reflected in both tap & flow
        self.at("differ in severity")
        for s_lvl, r_lvl in ((0.65, 0.75), (0.14, 0.16), (0.28, 0.32)):
            self.play(
                Transform(world.tap, make_tap(world.tap_pos, scale=world.s, strength=s_lvl)),
                rate.animate.set_value(r_lvl),
                run_time=0.72,
            )

        # Three triggers enter from right
        self.at("fava beans")
        beans = fava_plate(0.88).move_to([4.5, 2.15, 0.0])
        beans_l = T("fava beans", size=28, color=TEXT).next_to(beans, DOWN, buff=0.14)
        self.play(FadeIn(VGroup(beans, beans_l), shift=LEFT * 0.8), run_time=0.45)

        self.at("certain")
        pill = drug_capsule(0.95).move_to([4.5, 0.25, 0.0])
        pill_l = T("certain drugs", size=28, color=TEXT).next_to(pill, DOWN, buff=0.16)
        self.play(FadeIn(VGroup(pill, pill_l), shift=LEFT * 0.8), run_time=0.45)

        self.at("infection")
        inf = infection_blob(0.88).move_to([4.5, -1.55, 0.0])
        inf_l = T("infection", size=28, color=TEXT).next_to(inf, DOWN, buff=0.14)
        self.play(FadeIn(VGroup(inf, inf_l), shift=LEFT * 0.8), run_time=0.45)

        # Bursts of RED stars overwhelm the slowed loop
        self.at("pushes oxidative stress")
        burst_origins = [beans.get_left(), pill.get_left(), inf.get_left()]
        stars = VGroup(*[
            oxidant_star(0.17).move_to(burst_origins[k % 3] + UP * (0.16 * ((k % 3) - 1)))
            for k in range(6)
        ])
        self.play(FadeIn(stars), run_time=0.25)

        self.at("past what")
        targets = [
            world.center + np.array([-0.85, 1.35, 0.0]),
            world.center + np.array([-1.65, 0.85, 0.0]),
            world.center + np.array([-1.85, -0.95, 0.0]),
            world.center + np.array([-1.15, 1.60, 0.0]),
            world.center + np.array([-1.55, -1.45, 0.0]),
            world.center + np.array([-2.15, 0.45, 0.0]),
        ]
        self.play(*[s.animate.move_to(t) for s, t in zip(stars, targets)], run_time=1.4)
        self.finish()


class S07Cascade(SpokenScene):
    def construct(self):
        world = RedCellWorld(center=(-1.20, -0.1, 0.0), radius=2.40, g6pd=0.25, show_loop=True,
                             show_tap=True, show_enzyme_labels=True)
        tap_lab = tap_label_above(world.tap, "G6PD: weak tap")
        rate = ValueTracker(0.28)
        nadph_r = ValueTracker(0.28)
        flow = world.attach_cycle_flow(rate, nadph_tracker=nadph_r, show_g6p=True, show_oxidants=False)

        beans = fava_plate(0.65).move_to([4.8, 1.65, 0.0])
        pill = drug_capsule(0.75).move_to([4.8, 0.25, 0.0])
        inf = infection_blob(0.68).move_to([4.8, -1.15, 0.0])
        trig_l = T("triggers", size=28, color=TEXT).next_to(beans, UP, buff=0.22)
        tag = scope_tag("schematic")
        self.add(world.root, tap_lab, flow, beans, pill, inf, trig_l, tag)

        # Less NADPH
        self.at("Less NADPH")
        self.play(nadph_r.animate.set_value(0.10), run_time=0.8)

        # Less reduced glutathione -> 2 GSH dims, GSSG brightens, loop stalls
        self.at("less reduced glutathione")
        self.play(
            world.gsh_chip[0].animate.set_fill(GSH_COL, opacity=0.05).set_stroke(opacity=0.45),
            world.gssg_chip[0].animate.set_fill(GSH_COL, opacity=0.20).set_stroke(width=4.2),
            rate.animate.set_value(0.0),
            run_time=1.9,
        )

        # Reactive oxygen builds up inside cell
        self.at("Reactive oxygen")
        star_pts = [
            world.center + np.array([-1.45, 1.35, 0.0]),
            world.center + np.array([-1.95, 0.70, 0.0]),
            world.center + np.array([-1.75, -1.10, 0.0]),
            world.center + np.array([-1.05, 1.65, 0.0]),
            world.center + np.array([-2.15, -0.45, 0.0]),
            world.center + np.array([-1.25, -1.55, 0.0]),
            world.center + np.array([-1.75, 0.40, 0.0]),
            world.center + np.array([-1.75, -0.75, 0.0]),
        ]
        stars = VGroup(*[oxidant_star(0.16).move_to(p) for p in star_pts])
        self.play(LaggedStart(*[FadeIn(s, scale=1.2) for s in stars], lag_ratio=0.12), run_time=1.5)

        # Hemoglobin oxidizes
        self.at("Hemoglobin oxidizes")
        self.play(*[
            d.animate.set_fill(OX_HB, opacity=0.95).set_stroke(OXIDANT, width=1.8)
            for d in world.hb_dots
        ], run_time=1.0)

        # Clumps together into 3 RED-outlined Heinz body knots
        self.at("clumps together")
        knot_centers = [
            world.center + np.array([-1.65, 1.25, 0.0]),
            world.center + np.array([-1.75, -0.85, 0.0]),
            world.center + np.array([-1.25, -1.35, 0.0]),
        ]
        rng = np.random.default_rng(11)
        move_anims = []
        for idx, d in enumerate(world.hb_dots):
            kc = knot_centers[idx % 3]
            offset = np.array([rng.uniform(-0.14, 0.14), rng.uniform(-0.14, 0.14), 0.0])
            move_anims.append(d.animate.move_to(kc + offset))
        knots = VGroup(*[
            Circle(radius=0.30, stroke_color=OXIDANT, stroke_width=3.2, fill_color=OX_HB, fill_opacity=0.25).move_to(kc)
            for kc in knot_centers
        ])
        for k in knots:
            k.layout_ok = "near"
        self.play(*move_anims, FadeIn(knots), run_time=1.6)

        # Heinz bodies label
        self.at("Heinz bodies")
        hb_lab = T("Heinz bodies", size=28, color=OXIDANT, weight=BOLD).move_to([2.45, 2.45, 0.0])
        arrow_hb = CurvedArrow(
            hb_lab.get_left() + LEFT * 0.1,
            knot_centers[0] + UP * 0.24 + RIGHT * 0.24,
            angle=0.35,
            stroke_width=2.8,
            color=OXIDANT,
            tip_length=0.20,
        )
        self.play(FadeIn(hb_lab), Create(arrow_hb), run_time=0.6)
        self.finish()


def mini_damaged_cell(radius=0.72, seed=3):
    """Compact damaged RBC with ROSE outline and 3 RED-outlined Heinz body knots."""
    ring = Circle(radius=radius, stroke_color=CELL_ROSE, stroke_width=3.8, fill_color=CELL_ROSE, fill_opacity=0.16)
    rng = np.random.default_rng(seed)
    knots = VGroup()
    for ang in (0.7, 2.6, 4.4):
        pos = np.array([0.42 * radius * np.cos(ang), 0.42 * radius * np.sin(ang), 0.0])
        k = Circle(radius=0.14 * radius / 0.72, stroke_color=OXIDANT, stroke_width=2.4,
                   fill_color=OX_HB, fill_opacity=0.90).move_to(pos + rng.uniform(-0.04, 0.04, 3) * np.array([1, 1, 0]))
        knots.add(k)
    return VGroup(ring, knots)


class S08Crisis(SpokenScene):
    def construct(self):
        main_cell = mini_damaged_cell(0.95, seed=7).move_to([-1.8, 0.05, 0.0])
        c_burst1 = mini_damaged_cell(0.72, seed=1).move_to([-4.6, 1.55, 0.0])
        c_burst2 = mini_damaged_cell(0.72, seed=2).move_to([-0.2, -1.65, 0.0])
        c_spl1 = mini_damaged_cell(0.72, seed=4).move_to([0.9, 1.30, 0.0])
        c_spl2 = mini_damaged_cell(0.72, seed=5).move_to([1.6, -0.65, 0.0])

        spleen_box = RoundedRectangle(corner_radius=0.55, width=2.1, height=3.2, stroke_color=TEXT, stroke_width=2.5,
                                      fill_color=GREY, fill_opacity=0.42).move_to([4.85, -0.1, 0.0])
        spleen_lab = T("spleen", size=30, color=TEXT, weight=BOLD).move_to(spleen_box)
        spleen = VGroup(spleen_box, spleen_lab)
        tag = scope_tag("schematic")

        self.add(main_cell, c_burst1, c_burst2, c_spl1, c_spl2, spleen, tag)
        self.play(
            main_cell.animate.shift(RIGHT * 0.45),
            c_burst1.animate.shift(RIGHT * 0.7),
            c_burst2.animate.shift(RIGHT * 0.7),
            c_spl1.animate.shift(RIGHT * 0.5),
            c_spl2.animate.shift(RIGHT * 0.5),
            run_time=0.95,
        )

        # Two cells burst in circulation and scatter ROSE dots
        self.at("burst")
        rng = np.random.default_rng(19)
        scatter_dots = VGroup()
        scatter_anims = []
        for cb in (c_burst1, c_burst2):
            pos = cb.get_center()
            for a in np.linspace(0, TAU, 8, endpoint=False):
                d = Dot(radius=0.075, color=CELL_ROSE).move_to(pos)
                scatter_dots.add(d)
                scatter_anims.append(d.animate.shift(np.array([np.cos(a), np.sin(a), 0.0]) * rng.uniform(0.65, 1.15)))
        self.add(scatter_dots)
        self.play(
            FadeOut(c_burst1, scale=1.35),
            FadeOut(c_burst2, scale=1.35),
            *scatter_anims,
            main_cell.animate.shift(RIGHT * 0.35),
            run_time=1.0,
        )

        # Spleen pulls 2 damaged cells out
        self.at("the spleen")
        self.play(spleen_box.animate.set_fill(GREY, opacity=0.58), run_time=0.35)

        self.at("pulls them out")
        self.play(
            c_spl1.animate.move_to(spleen_box.get_left() + RIGHT * 0.4).scale(0.2).set_opacity(0.0),
            c_spl2.animate.move_to(spleen_box.get_left() + RIGHT * 0.4).scale(0.2).set_opacity(0.0),
            FadeOut(scatter_dots),
            main_cell.animate.shift(RIGHT * 0.35),
            run_time=1.3,
        )
        self.remove(c_spl1, c_spl2, scatter_dots)

        # Hemolytic crisis headline
        self.at("hemolytic crisis")
        head = T("hemolytic crisis", size=40, color=TEXT, weight=BOLD).move_to([0.0, 3.22, 0.0])
        self.play(FadeIn(head, shift=DOWN * 0.15), run_time=0.55)

        # Bean started it
        self.at("started it")
        bean_corner = fava_plate(0.75).move_to([-4.9, 1.75, 0.0])
        bean_note = T("fava beans", size=28, color=TEXT).next_to(bean_corner, DOWN, buff=0.14)
        trigger_arr = Arrow(bean_corner.get_right() + RIGHT * 0.1, main_cell.get_left() + LEFT * 0.12,
                            buff=0.05, color=OXIDANT, stroke_width=3.2)
        self.play(FadeIn(bean_corner), FadeIn(bean_note), Create(trigger_arr), run_time=0.6)
        self.finish()


class S09Chain(SpokenScene):
    def construct(self):
        world = RedCellWorld(center=(0.0, 1.00, 0.0), radius=2.12, g6pd=1.0, show_loop=True,
                             show_tap=True, show_enzyme_labels=False)
        rate = ValueTracker(1.0)
        nadph_r = ValueTracker(1.0)
        flow = world.attach_cycle_flow(rate, nadph_tracker=nadph_r, show_g6p=True, show_oxidants=False)
        row, chips, arrows = make_chain_chips(y=-2.22)
        tag = scope_tag("schematic")
        self.add(world.root, flow, tag)

        # 1. Weak G6PD
        self.at("Weak")
        weak_tap = make_tap(world.tap_pos, scale=world.s, strength=0.25)
        self.play(FadeIn(chips[0]), Transform(world.tap, weak_tap), run_time=0.6)

        # 2. Less NADPH
        self.at("Less NADPH")
        self.play(Create(arrows[0]), FadeIn(chips[1]), nadph_r.animate.set_value(0.12), run_time=0.65)

        # 3. Less reduced glutathione
        self.at("Less reduced glutathione")
        self.play(
            Create(arrows[1]),
            FadeIn(chips[2]),
            world.gsh_chip[0].animate.set_fill(GSH_COL, opacity=0.05).set_stroke(opacity=0.45),
            world.gsh_chip[1].animate.set_opacity(0.55),
            rate.animate.set_value(0.0),
            run_time=0.75,
        )

        # 4. More reactive oxygen
        self.at("More reactive oxygen")
        stars = VGroup(*[
            oxidant_star(0.14).move_to(world.center + p)
            for p in ([-1.2, 1.0, 0], [-1.55, 0.2, 0], [-1.3, -1.0, 0], [-0.9, 1.3, 0], [-1.5, -0.5, 0])
        ])
        self.play(Create(arrows[2]), FadeIn(chips[3]), FadeIn(stars, scale=1.2), run_time=0.75)

        # 5. Clumped hemoglobin
        self.at("Clumped hemoglobin")
        kcs = [world.center + np.array([-1.35, 1.0, 0]), world.center + np.array([-1.65, -0.7, 0]), world.center + np.array([-0.95, -1.1, 0])]
        rng = np.random.default_rng(23)
        clump_anims = [
            d.animate.move_to(kcs[i % 3] + np.array([rng.uniform(-0.11, 0.11), rng.uniform(-0.11, 0.11), 0.0])).set_fill(OX_HB, opacity=0.95)
            for i, d in enumerate(world.hb_dots)
        ]
        knots = VGroup(*[Circle(radius=0.24, stroke_color=OXIDANT, stroke_width=2.8, fill_color=OX_HB, fill_opacity=0.25).move_to(kc) for kc in kcs])
        for k in knots:
            k.layout_ok = "near"
        self.play(Create(arrows[3]), FadeIn(chips[4]), *clump_anims, FadeIn(knots), run_time=0.85)

        # 6. Lost cells
        self.at("Lost cells")
        crack = VMobject(stroke_color=OXIDANT, stroke_width=4.0)
        crack.set_points_as_corners([
            world.outer.point_at_angle(2.2),
            world.center + np.array([-1.3, 0.3, 0.0]),
            world.center + np.array([-1.4, -0.3, 0.0]),
            world.outer.point_at_angle(4.1),
        ])
        self.play(Create(arrows[4]), FadeIn(chips[5]), world.outer.animate.set_stroke(OXIDANT, width=5.5), Create(crack), run_time=0.7)
        self.finish()


def build_s10_world(dim_chain=True):
    """Exact shared state between S10Predict and S11Pause."""
    world = RedCellWorld(center=(-1.55, 0.70, 0.0), radius=1.95, g6pd=0.25, show_loop=True,
                         show_tap=True, show_enzyme_labels=False)
    world.gsh_chip[0].set_fill(GSH_COL, opacity=0.05).set_stroke(opacity=0.45)
    world.gsh_chip[1].set_opacity(0.55)
    row, chips, arrows = make_chain_chips(y=-2.22)
    if dim_chain:
        for c in chips:
            c[0].set_stroke(opacity=0.45).set_fill(opacity=0.08)
            c[1].set_opacity(0.90)
        for a in arrows:
            a.set_opacity(0.45)
    return world, row


class S10Predict(SpokenScene):
    def construct(self):
        world, row = build_s10_world(dim_chain=True)
        rate = ValueTracker(0.24)
        nadph_r = ValueTracker(0.18)
        flow = world.attach_cycle_flow(rate, nadph_tracker=nadph_r, show_g6p=True, show_oxidants=False)
        tag = scope_tag("schematic")
        self.add(world.root, flow, row, tag)

        self.at("400 million")
        pop = ValueTracker(0)
        pop_counter = counter("~{:.0f} million people", pop, at=[3.75, 1.25, 0.0], size=34, color=TEXT)
        self.add(pop_counter)
        self.play(pop.animate.set_value(400), run_time=1.3)

        self.at("What could keep")
        q_top = T("Why is it so common?", size=40, color=GOLD, weight=BOLD).move_to([0.0, 3.22, 0.0])
        self.play(FadeIn(q_top, shift=DOWN * 0.15), run_time=0.65)
        self.finish()


class S11Pause(PredictPause):
    QUESTION = "Why is it so common?"
    CARD = {"y": 3.22, "size": 40, "color": GOLD}
    RING_AT = (3.75, -0.25, 0)
    SECONDS = 4.5

    def construct(self):
        world, row = build_s10_world(dim_chain=True)
        pop = T("~400 million people", size=34, font=MONO, color=TEXT).move_to([3.75, 1.25, 0.0])
        q_top = T(self.QUESTION, size=40, color=GOLD, weight=BOLD).move_to([0.0, 3.22, 0.0])
        ring, run = countdown(self.SECONDS, center=self.RING_AT)
        self.add(world.root, row, pop, q_top, ring)
        self.play(run)
        self.finish()


class S12Malaria(SpokenScene):
    def construct(self):
        # Dissolve question card & dimmed chain from pause scene as malaria answer begins
        world_prev, row_prev = build_s10_world(dim_chain=True)
        q_prev = T("Why is it so common?", size=40, color=GOLD, weight=BOLD).move_to([0.0, 3.22, 0.0])

        world = RedCellWorld(center=(-1.65, -0.05, 0.0), radius=2.35, g6pd=0.25, show_loop=True, show_tap=True)
        world.gsh_chip[0].set_fill(GSH_COL, opacity=0.08).set_stroke(opacity=0.65)
        rate = ValueTracker(0.32)
        flow = world.attach_cycle_flow(rate, show_g6p=True, show_oxidants=False)
        tag = scope_tag("schematic")
        self.add(world_prev.root, row_prev, q_prev, tag)
        self.play(
            FadeOut(row_prev),
            FadeOut(q_prev),
            ReplacementTransform(world_prev.root, world.root),
            run_time=1.0,
        )
        self.add(flow)

        # Parasite drifts toward dim-tap cell
        self.at("protection against malaria")
        para = parasite_oval(1.15).move_to([3.9, 0.6, 0.0])
        para_lab = T("malaria parasite", size=28, color=TEXT).next_to(para, UP, buff=0.22)
        self.play(FadeIn(VGroup(para, para_lab), shift=LEFT * 0.7), run_time=0.65)

        # Slips inside cell, fails to thrive, fades out; "seems" tag
        self.at("poorer home")
        inner_spot = world.center + np.array([-1.05, 1.15, 0.0])
        self.play(FadeOut(para_lab), para.animate.move_to(inner_spot), run_time=1.0)
        seems = boxed_label("seems", TEXT, size=28, pad=0.14).move_to([2.4, 1.15, 0.0])
        self.play(para.animate.scale(0.55).set_opacity(0.22), FadeIn(seems), run_time=0.9)
        self.play(FadeOut(para), run_time=0.6)

        # Replace with clean thumbnail cell (no tiny font < 22) in left third, and overlap shapes at right
        self.at("Where the trait")
        self.remove(flow)
        mini_world = RedCellWorld(center=(-4.25, -0.05, 0.0), radius=1.45, g6pd=0.25,
                                  show_loop=True, show_tap=True, compact_loop=True)
        self.play(FadeOut(seems), ReplacementTransform(world.root, mini_world.root), run_time=0.9)

        r_trait = RoundedRectangle(corner_radius=0.85, width=3.3, height=3.1, stroke_color=PATHWAY,
                                   stroke_width=3.5, fill_color=PATHWAY, fill_opacity=0.22).move_to([0.3, 0.25, 0.0])
        r_mal = RoundedRectangle(corner_radius=0.85, width=3.3, height=3.1, stroke_color=GREY,
                                 stroke_width=3.5, fill_color=GREY, fill_opacity=0.24).move_to([4.1, -0.15, 0.0])
        r_trait.layout_ok = "near"
        r_mal.layout_ok = "near"
        l_trait = T("trait common", size=28, color=PATHWAY).next_to(r_trait, UP, buff=0.22)
        l_mal = T("malaria, historically", size=28, color=TEXT).next_to(r_mal, DOWN, buff=0.22)
        note = T("schematic, not a map", size=24, color=TEXT).move_to([2.2, -2.95, 0.0])
        self.play(FadeIn(r_trait), FadeIn(r_mal), FadeIn(l_trait), FadeIn(l_mal), FadeIn(note), run_time=0.7)

        self.at("overlaps")
        self.play(
            r_trait.animate.shift(RIGHT * 1.15),
            l_trait.animate.shift(RIGHT * 0.65),
            r_mal.animate.shift(LEFT * 1.15),
            l_mal.animate.shift(LEFT * 0.65),
            run_time=1.4,
        )
        self.finish()


class S13Balanced(SpokenScene):
    def construct(self):
        world = RedCellWorld(center=(-4.25, -0.05, 0.0), radius=1.45, g6pd=0.25,
                             show_loop=True, show_tap=True, compact_loop=True)
        r_trait = RoundedRectangle(corner_radius=0.85, width=3.3, height=3.1, stroke_color=PATHWAY,
                                   stroke_width=3.5, fill_color=PATHWAY, fill_opacity=0.22).move_to([1.45, 0.25, 0.0])
        r_mal = RoundedRectangle(corner_radius=0.85, width=3.3, height=3.1, stroke_color=GREY,
                                 stroke_width=3.5, fill_color=GREY, fill_opacity=0.24).move_to([2.95, -0.15, 0.0])
        overlap_grp = VGroup(r_trait, r_mal)
        tag = scope_tag("schematic")
        self.add(world.root, overlap_grp, tag)

        # Balance beam
        self.at("balanced polymorphism")
        pivot = np.array([2.2, -0.45, 0.0])
        fulcrum = Polygon(pivot, pivot + np.array([-0.38, -0.70, 0.0]), pivot + np.array([0.38, -0.70, 0.0]),
                          stroke_color=TEXT, stroke_width=2.5, fill_color=GREY, fill_opacity=0.40)
        tilt = ValueTracker(0.0)

        def mk_beam():
            ang = tilt.get_value()
            dx, dy = 2.05 * np.cos(ang), 2.05 * np.sin(ang)
            p_l = pivot + np.array([-dx, -dy, 0.0])
            p_r = pivot + np.array([dx, dy, 0.0])
            bar = Line(p_l, p_r, color=TEXT, stroke_width=5.0)
            pan_l = Line(p_l + LEFT * 0.72, p_l + RIGHT * 0.72, color=OXIDANT, stroke_width=4.0)
            pan_r = Line(p_r + LEFT * 0.72, p_r + RIGHT * 0.72, color=GSH_COL, stroke_width=4.0)
            b_icon = fava_plate(0.62).next_to(pan_l, UP, buff=0.08)
            p_icon = parasite_oval(0.70).next_to(pan_r, UP, buff=0.10)
            return VGroup(bar, pan_l, pan_r, b_icon, p_icon)

        beam = always_redraw(mk_beam)
        bal_head = T("balanced polymorphism", size=32, color=TEXT, weight=BOLD).move_to([2.2, 2.35, 0.0])
        lab_l = T("risk: hemolysis", size=26, color=OXIDANT).move_to([0.15, -1.65, 0.0])
        lab_r = T("some malaria\nprotection", size=26, color=GSH_COL, line_spacing=0.85).move_to([4.25, -1.70, 0.0])

        self.play(ReplacementTransform(overlap_grp, fulcrum), FadeIn(bal_head), FadeIn(lab_l), FadeIn(lab_r), run_time=0.5)
        self.add(beam)
        self.play(tilt.animate.set_value(0.18), run_time=0.55)
        self.play(tilt.animate.set_value(-0.14), run_time=0.55)
        self.play(tilt.animate.set_value(0.0), run_time=0.45)

        # Debated strength
        self.at("still differs")
        debated = boxed_label("debated strength", GOLD, size=28, pad=0.14).move_to([2.2, -2.55, 0.0])
        self.play(tilt.animate.set_value(0.11), FadeIn(debated), run_time=0.55)
        self.play(tilt.animate.set_value(-0.08), run_time=0.45)
        self.play(tilt.animate.set_value(0.0), run_time=0.45)

        # Doctors screen before oxidant drugs
        self.at("doctors screen")
        self.play(FadeOut(beam), FadeOut(fulcrum), FadeOut(bal_head), FadeOut(lab_l), FadeOut(lab_r), FadeOut(debated), run_time=0.55)
        self.remove(beam)

        pill = drug_capsule(1.1).move_to([1.2, 0.65, 0.0])
        pill_l = T("certain drugs", size=28, color=TEXT).next_to(pill, DOWN, buff=0.22)
        chk_box = RoundedRectangle(corner_radius=0.16, width=2.8, height=2.2, stroke_color=GSH_COL, stroke_width=3.0,
                                   fill_color=GSH_COL, fill_opacity=0.14).move_to([4.15, 0.35, 0.0])
        chk_title = T("G6PD screen\nfirst", size=28, color=TEXT, weight=BOLD, line_spacing=0.9).move_to(chk_box.get_center() + UP * 0.35)
        check_mark = VMobject(stroke_color=GSH_COL, stroke_width=5.0)
        c0 = chk_box.get_center() + DOWN * 0.55
        check_mark.set_points_as_corners([c0 + LEFT * 0.30 + UP * 0.05, c0 + LEFT * 0.08 + DOWN * 0.16, c0 + RIGHT * 0.34 + UP * 0.28])
        self.play(FadeIn(pill), FadeIn(pill_l), FadeIn(chk_box), FadeIn(chk_title), run_time=0.6)
        self.play(Create(check_mark), run_time=0.55)
        self.finish()


class S14Twist(SpokenScene):
    def construct(self):
        world = RedCellWorld(center=(-1.55, -0.05, 0.0), radius=2.30, g6pd=0.25, show_loop=True, show_tap=True)
        rate = ValueTracker(0.32)
        flow = world.attach_cycle_flow(rate, show_g6p=True, show_oxidants=False)
        tap_lab = tap_label_above(world.tap, "weak G6PD")
        tag = scope_tag("schematic")
        self.add(world.root, flow, tap_lab, tag)

        # Two arrows: solid RED to bean ("exposed"), dashed white to parasite ("poorer home?")
        self.at("cuts both ways")
        bean_pos = np.array([3.95, 1.55, 0.0])
        para_pos = np.array([3.95, -1.55, 0.0])
        beans = fava_plate(0.95).move_to(bean_pos)
        bean_lab = T("exposed", size=30, color=OXIDANT, weight=BOLD).next_to(beans, DOWN, buff=0.18)
        para = parasite_oval(1.10).move_to(para_pos)
        para_lab = T("poorer home?", size=30, color=TEXT, weight=BOLD).next_to(para, DOWN, buff=0.20)

        arr_top = Arrow(world.outer.get_right() + UP * 0.55 + RIGHT * 0.1, beans.get_left() + LEFT * 0.15,
                        buff=0.05, color=OXIDANT, stroke_width=3.8)
        bot_start = world.outer.get_right() + DOWN * 0.55 + RIGHT * 0.1
        bot_end = para.get_left() + LEFT * 0.25
        arr_bot_line = DashedVMobject(
            Line(bot_start, bot_end, color=TEXT, stroke_width=3.5),
            num_dashes=10,
        )
        bot_ang = angle_of_vector(bot_end - bot_start) - PI / 2
        arr_bot_tip = Triangle(color=TEXT, fill_color=TEXT, fill_opacity=1.0).scale(0.11).rotate(bot_ang).move_to(para.get_left() + LEFT * 0.18)

        self.play(
            Create(arr_top), FadeIn(beans), FadeIn(bean_lab),
            run_time=1.4,
        )
        self.play(
            Create(arr_bot_line), FadeIn(arr_bot_tip), FadeIn(para), FadeIn(para_lab),
            run_time=1.4,
        )

        self.at("exposed to a bean")
        star = oxidant_star(0.18).move_to(beans.get_left())
        self.play(FadeIn(star), run_time=0.2)
        self.play(star.animate.move_to(world.outer.get_right() + UP * 0.45), run_time=1.1)

        self.at("poorer home")
        self.play(para.animate.scale(0.75).set_opacity(0.45), FadeOut(star), run_time=1.1)
        self.finish()


class S15Close(SpokenScene):
    def construct(self):
        world = RedCellWorld(center=(-0.6, -0.05, 0.0), radius=2.55, g6pd=1.0, show_loop=True,
                             show_tap=True, show_enzyme_labels=True)
        tap_lab = tap_label_above(world.tap, "G6PD: the tap")
        rate = ValueTracker(1.1)
        nadph_r = ValueTracker(1.1)
        flow = world.attach_cycle_flow(rate, nadph_tracker=nadph_r, show_g6p=True, show_oxidants=True)
        tag = scope_tag("schematic")
        self.add(world.root, tap_lab, flow, tag)

        # Trace ORANGE route on "shield" (routed cleanly around 2 GSH)
        self.at("shield")
        pts = [world.nadph_path_point(a) for a in np.linspace(0, 1, 18)]
        pts += [world.bot_arc.point_from_proportion(a) for a in np.linspace(0.5, 1.0, 12)]
        pts += [
            world.gsh_chip.get_left() + LEFT * 0.18 + DOWN * 0.20,
            world.gsh_chip.get_left() + LEFT * 0.18 + UP * 0.20,
        ]
        pts += [world.top_arc.point_from_proportion(a) for a in np.linspace(0.0, 1.0, 18)]
        route = VMobject(stroke_color=PATHWAY, stroke_width=5.2, stroke_opacity=0.85).set_points_as_corners(pts)
        route.layout_ok = True
        self.play(Create(route), run_time=1.1)
        self.play(FadeOut(route), run_time=0.5)

        # Weaken G6PD
        self.at("Weaken G6PD")
        weak_tap = make_tap(world.tap_pos, scale=world.s, strength=0.22)
        new_lab = tap_label_above(world.tap, "G6PD: weak tap")
        self.play(Transform(world.tap, weak_tap), swap(tap_lab, new_lab, run_time=0.6), run_time=0.7)

        # Add an oxidant
        self.at("add an oxidant")
        burst = VGroup(*[
            oxidant_star(0.17).move_to([3.4, 0.85 - 0.58 * i, 0.0])
            for i in range(4)
        ])
        self.play(FadeIn(burst), run_time=0.25)

        # Whole chain gives way in order
        self.at("gives way")
        kcs = [
            world.center + np.array([-1.65, 1.25, 0.0]),
            world.center + np.array([-1.85, -0.85, 0.0]),
            world.center + np.array([-1.25, -1.40, 0.0]),
        ]
        rng = np.random.default_rng(31)
        clump_anims = [
            d.animate.move_to(kcs[i % 3] + np.array([rng.uniform(-0.13, 0.13), rng.uniform(-0.13, 0.13), 0.0])).set_fill(OX_HB, opacity=0.95)
            for i, d in enumerate(world.hb_dots)
        ]
        burst_targets = [
            world.center + np.array([-1.4, 1.1, 0.0]),
            world.center + np.array([-1.9, 0.4, 0.0]),
            world.center + np.array([-1.7, -0.9, 0.0]),
            world.center + np.array([-1.1, -1.3, 0.0]),
        ]
        self.play(
            nadph_r.animate.set_value(0.10),
            rate.animate.set_value(0.0),
            world.gsh_chip[0].animate.set_fill(GSH_COL, opacity=0.05).set_stroke(opacity=0.45),
            world.gsh_chip[1].animate.set_opacity(0.55),
            *[s.animate.move_to(t) for s, t in zip(burst, burst_targets)],
            *clump_anims,
            run_time=1.4,
        )
        self.finish()


class S16End(EndCard):
    LINE = "A red cell's antioxidant defense leans on NADPH, gated by G6PD."
