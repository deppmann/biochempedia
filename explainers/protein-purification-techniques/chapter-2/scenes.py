"""
COLOUR MAP (one colour per concept for the entire film):
- GOLD   (#D4A843): target protein (tube tokens, bead chain, gel band, peptides, MS peaks, matching card)
- GREY   (#8B93A1): non-target / contaminant proteins and unmatched database cards (shapes only; text uses TEXT)
- TEAL   (#3FB8C0): gel ladder, size ruler, purity/stain-limit threshold, step cards
- RED    (#FC6255): discarded material (selective loss), blind-spot / same-mass highlight
- BLUE   (#58C4DD): electrophoresis terminals (+/-), trypsin scissors, flight-tube & MS scan controls
- PURPLE (#B189FF): antibodies (Y-shaped probes)
- GREEN  (#83C167): confirmed validation checkmark
- TEXT   (#E8EAF0): all general labels, titles, and outlines at full opacity

ONE WORLD, CARRIED ALL FILM:
At far left (x ~ -5.20), the small purified sample vessel (gold-rich target tokens + 2 grey tokens) and
the growing vertical stack of three proving cards ('1 · size', '2 · which protein?', '3 · sequence').
To its right (x = -1.65 to +6.15, filling ~75% of frame height), the PROVING PANEL that transforms from
an SDS-PAGE gel -> western blot membrane -> MALDI-TOF flight tube & mass list -> Edman sequencer ->
tandem MS fragmenter -> Sanger vs MS comparison -> back to the opening gel with all three answers linked.
A full-opacity 'schematic' scope tag sits at bottom right throughout.

WHAT CHANGES IN EACH SPOKEN SCENE (and what it is computed from):
- s00_link_and_question: Discard stream leaves the vessel; a drop falls into the sample well and migrates
  exponentially down the gel into one sharp GOLD band; question and '?' appear beside the band.
- s02_gel: Three coiled protein blobs (sizes 13, 9, 6) uncoil into straight bead chains, acquire uniform-
  spacing negative-charge strokes (proportional to length), and migrate down at computed v ~ 1/log(N) speeds.
- s03_ladder: Five TEAL marker bands migrate down the ladder lane at computed 1/log(size) speeds; a horizontal
  TEAL ruler slides from the GOLD band to interpolate size; card '1 · size' pins at left.
- s04_limit: A zoom window opens on the GOLD band revealing a co-migrating GREY chain of identical length;
  window closes; a faint GREY trace (12% opacity) sits under a computed 'stain limit' threshold bar meter.
- s05_idea: Tags 'size' and blank name tag attach to the GOLD band; 'purity' and 'identity' split above the
  panel; cards '2 · which protein?' and '3 · sequence' slide into the stack at left.
- s06_western: Mixture bands transfer horizontally band-for-band from gel to pale membrane; PURPLE Y-shaped
  antibodies probe across the membrane, deflect off GREY bands, clamp and light up only the GOLD band.
- s07_mass: Membrane transforms into the MALDI-TOF flight tube; BLUE scissors cut the 18-bead GOLD chain into
  6 peptides (lengths 2..7); a laser flash launches them rightward at computed velocities v ~ 1/sqrt(m_i).
- s08_predict: Remaining peptides arrive at the detector in sqrt(m_i) order, raising 6 GOLD sticks on the
  mass axis; sticks compress into a 6-tick mass list beside the empty name tag and question card.
- s10_answer: Seven computed database digest cards (seed 7) fan out; the GOLD mass list scans down them,
  dimming mismatches until all 6 ticks align on card #5, merging into 6 fingerprint arcs and 'match found'.
- s11_sequence: Edman degradation clips N-terminal residues one by one into a reader box; compounding 0.98^n
  phase lag across 4 chains blurs the read; two staggered cuts yield clean overlapping peptide reads.
- s12_tandem: One 6-residue peptide fragments into a staircase of 6..1 beads; peaks rise at cumulative residue
  masses and BLUE gap brackets spell the sequence left-to-right, flagging equal-mass 'L or I?' in RED.
- s13_sanger: Left panel fills 21 + 30 = 51 insulin beads one by one while a 'years' counter ticks 0 to 12;
  right panel runs a single MS scan line across 14 computed peaks to 'one run'.
- s14_return: Returns to the opening gel world, briefly re-opens the hidden-chain window on the GOLD band,
  and links all three cards (with antibody, mass-list, and sequence icons) to 'size' and 'identity'.
"""

from bp_parts import *

PURPLE = "#B189FF"

# Consistent coordinates for the carried world (safe frame: x in [-6.3, 6.3], y in [-3.4, 3.4])
VESSEL_X = -5.20
VESSEL_Y = -1.05
VESSEL_W = 1.75
VESSEL_H = 2.65

CARDS_X = -5.20
CARDS_Y = [2.65, 2.02, 1.39]
CARD_BOX = (2.05, 0.46)

# Gel slab positioned to leave clean left margin for ladder words (-3.0..-1.8)
# and clean right margin (+4.25..+6.30) for side meters/name tags
GEL_X0 = -1.65
GEL_X1 = 4.25
GEL_Y0 = -2.28
GEL_Y1 = 2.12
LADDER_X = -0.45
SAMPLE_X = 2.45
DIVIDER_X = 0.85
BAND_Y = -0.65

CARD_LABELS = [
    ("1 · size", TEAL),
    ("2 · which protein?", GOLD),
    ("3 · sequence", BLUE),
]


def build_scope():
    return scope_tag("schematic", size=24, color=TEXT)


def build_vessel(seed=7):
    """Build the purified sample vessel at left with fixed-seed GOLD target & 2 GREY tokens."""
    rng = np.random.default_rng(seed)
    body = RoundedRectangle(
        corner_radius=0.22,
        width=VESSEL_W,
        height=VESSEL_H,
        stroke_color=TEXT,
        stroke_width=3,
        fill_color=BG,
        fill_opacity=0.95,
    ).move_to([VESSEL_X, VESSEL_Y, 0])

    liq_h = VESSEL_H * 0.72
    liq = RoundedRectangle(
        corner_radius=0.16,
        width=VESSEL_W - 0.14,
        height=liq_h,
        stroke_width=0,
        fill_color=TEAL,
        fill_opacity=0.20,
    ).move_to([VESSEL_X, VESSEL_Y - (VESSEL_H - liq_h) / 2 + 0.08, 0])

    tokens = VGroup()
    xs = rng.uniform(VESSEL_X - 0.62, VESSEL_X + 0.62, 18)
    ys = rng.uniform(VESSEL_Y - 1.05, VESSEL_Y + 0.42, 18)
    for i in range(18):
        col = GREY if i in (3, 12) else GOLD
        r = 0.09 if col == GOLD else 0.08
        tokens.add(Dot([xs[i], ys[i], 0], radius=r, color=col))

    label = T("purified tube", size=24, color=TEXT).next_to(body, DOWN, buff=0.16)
    g = VGroup(body, liq, tokens, label)
    g.body, g.liq, g.tokens, g.label = body, liq, tokens, label
    return g


def build_cards(count=3, active=None, checked=()):
    """Build 1..3 pinned method cards in the fixed top-left stack."""
    cards = VGroup()
    for i in range(count):
        txt, col = CARD_LABELS[i]
        is_active = (active == i)
        c = boxed_label(
            txt,
            color=col,
            size=24,
            box=CARD_BOX,
            pad=0.12,
            stroke=4.0 if is_active else 2.2,
            fill_opacity=0.28 if is_active else 0.14,
        ).move_to([CARDS_X, CARDS_Y[i], 0])
        if i in checked:
            tick = check_mark(color=GREEN).scale(0.85).next_to(c, RIGHT, buff=0.10)
            c.add(tick)
        cards.add(c)
    return cards


def check_mark(color=GREEN):
    p1 = np.array([-0.11, 0.0, 0.0])
    p2 = np.array([-0.02, -0.09, 0.0])
    p3 = np.array([0.14, 0.11, 0.0])
    return VMobject(stroke_color=color, stroke_width=4.5).set_points_as_corners([p1, p2, p3])


def build_gel_panel(show_terminals=False, ladder_label=True, sample_label=True):
    """Build the upright SDS-PAGE gel slab inside the main panel region."""
    slab = RoundedRectangle(
        corner_radius=0.18,
        width=GEL_X1 - GEL_X0,
        height=GEL_Y1 - GEL_Y0,
        stroke_color=TEAL,
        stroke_width=3.0,
        fill_color=TEAL,
        fill_opacity=0.15,
    ).move_to([(GEL_X0 + GEL_X1) / 2, (GEL_Y0 + GEL_Y1) / 2, 0])

    well_y = 1.76
    well_w = 1.85
    well_h = 0.24
    ladder_well = Rectangle(
        width=well_w, height=well_h, stroke_color=GREY, stroke_width=2.2, fill_color=BG, fill_opacity=0.85
    ).move_to([LADDER_X, well_y, 0])
    sample_well = Rectangle(
        width=well_w + 0.45, height=well_h, stroke_color=GREY, stroke_width=2.2, fill_color=BG, fill_opacity=0.85
    ).move_to([SAMPLE_X, well_y, 0])

    divider = DashedLine(
        [DIVIDER_X, GEL_Y0 + 0.15, 0],
        [DIVIDER_X, GEL_Y1 - 0.15, 0],
        color=GREY,
        stroke_width=1.8,
        dash_length=0.12,
    ).set_opacity(0.55)

    g = VGroup(slab, divider, ladder_well, sample_well)
    if ladder_label:
        lbl_l = T("ladder", size=24, color=TEXT).next_to(slab, UP, buff=0.14)
        lbl_l.set_x(LADDER_X)
        g.add(lbl_l)
        g.ladder_label = lbl_l
    if sample_label:
        lbl_s = T("sample", size=24, color=TEXT).next_to(slab, UP, buff=0.14)
        lbl_s.set_x(SAMPLE_X)
        g.add(lbl_s)
        g.sample_label = lbl_s
    if show_terminals:
        neg = T("−", size=34, color=BLUE, weight=BOLD).next_to(slab, RIGHT, buff=0.18).set_y(GEL_Y1 - 0.25)
        pos = T("+", size=34, color=BLUE, weight=BOLD).next_to(slab, RIGHT, buff=0.18).set_y(GEL_Y0 + 0.25)
        g.add(neg, pos)
        g.neg, g.pos = neg, pos

    g.slab = slab
    g.ladder_well = ladder_well
    g.sample_well = sample_well
    g.divider = divider
    return g


def build_gel_band(x, y, width=1.80, height=0.18, color=GOLD, opacity=1.0):
    return RoundedRectangle(
        corner_radius=0.05,
        width=width,
        height=height,
        stroke_width=0,
        fill_color=color,
        fill_opacity=opacity,
    ).move_to([x, y, 0])


def build_ladder_bands():
    """Five computed marker bands from large (top) to small (bottom), tagged with size words."""
    sizes = [120.0, 75.0, 48.0, 30.0, 18.0]
    words = ["very large", "large", "medium", "small", "very small"]
    logs = [np.log(s) for s in sizes]
    lo, hi = min(logs), max(logs)
    bands = VGroup()
    tags = VGroup()
    for s, w, lg in zip(sizes, words, logs):
        frac = (hi - lg) / (hi - lo)
        y = 1.25 - frac * 3.05
        b = build_gel_band(LADDER_X, y, width=1.60, height=0.16, color=TEAL, opacity=0.95)
        t = T(w, size=24, color=TEAL).move_to([GEL_X0 - 0.16, y, 0], aligned_edge=RIGHT)
        bands.add(b)
        tags.add(t)
    return bands, tags


def build_bead_chain(n_beads, center, step=0.18, radius=0.075, color=GOLD, vertical=False, coiled=False, seed=0):
    """Build a straight or coiled bead chain (no molecular structures)."""
    g = VGroup()
    if coiled:
        pts = []
        for i in range(n_beads):
            ang = i * 1.15 + seed * 0.7
            r = 0.08 + 0.024 * i
            pts.append(np.array([center[0] + r * np.cos(ang), center[1] + 0.55 * r * np.sin(ang), 0.0]))
    else:
        span = (n_beads - 1) * step
        axis = DOWN if vertical else RIGHT
        start = np.array(center, dtype=float) - axis * (span / 2.0)
        pts = [start + axis * (i * step) for i in range(n_beads)]
    if len(pts) >= 2:
        backbone = VMobject(stroke_color=color, stroke_width=3.2).set_points_as_corners(pts)
        g.add(backbone)
    for p in pts:
        g.add(Dot(p, radius=radius, color=color))
    return g


def build_antibody_y(color=PURPLE, scale=0.35):
    """Build a simple Y-shaped antibody cartoon (no molecular detail)."""
    stem = Line([0, -0.5, 0], [0, 0.05, 0], color=color, stroke_width=5)
    arm_l = Line([0, 0.05, 0], [-0.42, 0.52, 0], color=color, stroke_width=5)
    arm_r = Line([0, 0.05, 0], [0.42, 0.52, 0], color=color, stroke_width=5)
    return VGroup(stem, arm_l, arm_r).scale(scale)


def build_scissors(color=BLUE, scale=0.34):
    """Simple geometric scissors icon."""
    b1 = Line([-0.4, -0.35, 0], [0.45, 0.35, 0], color=color, stroke_width=4.5)
    b2 = Line([-0.4, 0.35, 0], [0.45, -0.35, 0], color=color, stroke_width=4.5)
    r1 = Circle(radius=0.14, color=color, stroke_width=3.5).move_to([-0.5, -0.4, 0])
    r2 = Circle(radius=0.14, color=color, stroke_width=3.5).move_to([-0.5, 0.4, 0])
    return VGroup(b1, b2, r1, r2).scale(scale)


def build_name_tag(text="name: _____", color=GOLD, at=(5.35, BAND_Y, 0)):
    return boxed_label(text, color=color, size=24, pad=0.14, stroke=2.5, fill_opacity=0.18).move_to(at)


def build_flight_tube(title_text="MALDI-TOF", y0=0.20, y1=2.15):
    """Horizontal flight tube from x=-3.1 to +5.7."""
    x0, x1 = -3.10, 5.70
    tube = RoundedRectangle(
        corner_radius=0.16,
        width=x1 - x0,
        height=y1 - y0,
        stroke_color=BLUE,
        stroke_width=3.0,
        fill_color=BLUE,
        fill_opacity=0.14,
    ).move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0])
    plate_l = Line([x0 + 0.25, y0 + 0.15, 0], [x0 + 0.25, y1 - 0.15, 0], color=TEXT, stroke_width=4.5)
    plate_r = Line([x1 - 0.25, y0 + 0.15, 0], [x1 - 0.25, y1 - 0.15, 0], color=GOLD, stroke_width=5.5)
    lbl_laser = T("laser", size=24, color=BLUE).next_to(tube, DOWN, buff=0.14).set_x(x0 + 0.45)
    lbl_det = T("detector", size=24, color=GOLD).next_to(tube, DOWN, buff=0.14).set_x(x1 - 0.55)
    lbl_title = T(title_text, size=30, color=TEXT).move_to([(x0 + x1) / 2, y1 + 0.38, 0])
    g = VGroup(tube, plate_l, plate_r, lbl_laser, lbl_det, lbl_title)
    g.tube, g.plate_l, g.plate_r = tube, plate_l, plate_r
    g.lbl_laser, g.lbl_det, g.lbl_title = lbl_laser, lbl_det, lbl_title
    g.x_start, g.x_end = x0 + 0.55, x1 - 0.45
    return g


# ------------------------------------------------------------------ scenes

class S00LinkAndQuestion(SpokenScene):
    def construct(self):
        vessel = build_vessel()
        gel = build_gel_panel()
        scope = build_scope()
        self.add(vessel, gel, scope)

        # Gentle thermal mixing of proteins inside the purified tube during opening
        rng = np.random.default_rng(101)
        deltas = rng.uniform(-0.12, 0.12, (len(vessel.tokens), 2))
        self.play(
            *[t.animate.shift([dx, dy, 0]) for t, (dx, dy) in zip(vessel.tokens, deltas)],
            run_time=1.0,
        )

        self.at("selective loss")
        discard = VGroup(*[Dot([VESSEL_X + 0.8 + 0.20 * i, VESSEL_Y + 0.9 - 0.12 * i, 0], radius=0.08, color=RED) for i in range(5)])
        sa_tag = boxed_label("30,000 units/mg", color=TEAL, size=24, pad=0.14).next_to(vessel.body, UP, buff=0.18)
        self.play(
            FadeIn(sa_tag, shift=UP * 0.1),
            FadeIn(discard, shift=RIGHT * 0.3),
            run_time=1.5,
        )
        self.play(
            discard.animate.shift(RIGHT * 0.7 + DOWN * 0.4).set_opacity(0),
            FadeOut(sa_tag),
            run_time=1.8,
        )
        self.remove(discard)

        self.at("run a sample")
        drop = Dot([VESSEL_X + 0.2, VESSEL_Y + 0.6, 0], radius=0.13, color=GOLD)
        well_pt = np.array([SAMPLE_X, 1.76, 0.0])
        arc_path = ArcBetweenPoints(drop.get_center(), well_pt, angle=-0.8)
        self.play(MoveAlongPath(drop, arc_path), run_time=1.2)
        streak = build_gel_band(SAMPLE_X, 1.70, width=1.80, height=0.45, color=GOLD, opacity=0.75)
        self.remove(drop)
        self.play(streak.animate.stretch_to_fit_height(0.18).move_to([SAMPLE_X, BAND_Y, 0]), run_time=1.5)

        self.at("one clean band")
        band = build_gel_band(SAMPLE_X, BAND_Y, width=1.80, height=0.18, color=GOLD, opacity=1.0)
        self.remove(streak)
        self.add(band)
        glow = RoundedRectangle(
            corner_radius=0.08, width=2.05, height=0.34, stroke_color=GOLD, stroke_width=3.5, fill_opacity=0
        ).move_to(band)
        self.play(Create(glow), run_time=1.0)
        self.play(FadeOut(glow), run_time=0.8)

        self.at("is it one protein")
        q_mark = T("?", size=56, color=GOLD, weight=BOLD).next_to(band, RIGHT, buff=0.35)
        q_head = T("One band. Which protein?", size=34, color=TEXT).move_to([1.3, 3.22, 0])
        band_box = RoundedRectangle(corner_radius=0.08, width=2.20, height=0.50, stroke_color=GOLD, stroke_width=3.2, fill_color=GOLD, fill_opacity=0.14).move_to(band)
        self.play(FadeIn(q_mark, scale=1.15), FadeIn(q_head, shift=DOWN * 0.1), Create(band_box), run_time=1.3)

        self.at("which protein")
        self.play(FadeOut(band_box), q_mark.animate.scale(1.14), run_time=1.2)
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        vessel = build_vessel()
        gel = build_gel_panel()
        band = build_gel_band(SAMPLE_X, BAND_Y, width=1.80, height=0.18, color=GOLD, opacity=1.0)
        scope = build_scope()
        q_mark = T("?", size=56, color=GOLD, weight=BOLD).next_to(band, RIGHT, buff=0.35)
        q_head = T("One band. Which protein?", size=34, color=TEXT).move_to([1.3, 3.22, 0])
        self.add(vessel, gel, band, scope, q_mark, q_head)

        title = T("One Band, Three Questions", size=46, font=TITLE_FONT, color=TEXT).move_to([1.3, 3.30, 0])
        fit(title, max_w=9.0)
        rule = Line(LEFT * 1.4, RIGHT * 1.4, color=GOLD, stroke_width=4).next_to(title, DOWN, buff=0.08)
        self.play(
            FadeOut(q_mark),
            swap(q_head, VGroup(title, rule), run_time=0.85),
            run_time=0.9,
        )
        self.finish()


class S02Gel(SpokenScene):
    def construct(self):
        vessel = build_vessel()
        gel = build_gel_panel(show_terminals=False)
        band_open = build_gel_band(SAMPLE_X, BAND_Y, width=1.80, height=0.18, color=GOLD, opacity=1.0)
        scope = build_scope()
        title = T("One Band, Three Questions", size=46, font=TITLE_FONT, color=TEXT).move_to([1.3, 3.30, 0])
        fit(title, max_w=9.0)
        rule = Line(LEFT * 1.4, RIGHT * 1.4, color=GOLD, stroke_width=4).next_to(title, DOWN, buff=0.08)
        sds_title = T("SDS-PAGE", size=34, color=TEXT).move_to([1.3, 3.22, 0])
        self.add(vessel, gel, band_open, scope, title, rule)

        # Rewind opening band to sample well while 3 folded proteins load from the tube
        specs = [
            (13, GREY, 10, 1.55),
            (9, GOLD, 20, 1.15),
            (6, GREY, 30, 0.78),
        ]
        coiled = VGroup(*[
            build_bead_chain(n, [SAMPLE_X - 0.72 + 0.72 * i, 1.76, 0], step=0.10, radius=0.065, color=c, vertical=False, coiled=True, seed=sd)
            for i, (n, c, sd, _) in enumerate(specs)
        ])
        self.play(
            swap(VGroup(title, rule), sds_title, run_time=0.7),
            band_open.animate.move_to([SAMPLE_X, 1.76, 0]).set_opacity(0.0),
            FadeIn(coiled, shift=DOWN * 0.3),
            run_time=2.2,
        )
        self.remove(band_open)

        self.at("unfolds")
        uncoiled_ys = [1.55, 1.15, 0.75]
        uncoiled = VGroup(*[
            build_bead_chain(n, [SAMPLE_X, uy, 0], step=0.155, radius=0.088, color=c, vertical=False, coiled=False)
            for (n, c, _, _), uy in zip(specs, uncoiled_ys)
        ])
        self.play(*[Transform(a, b) for a, b in zip(coiled, uncoiled)], run_time=1.8)

        self.at("coats it with negative")
        minus_strokes = VGroup()
        sheaths = VGroup()
        for chain, (n, _, _, _), uy in zip(coiled, specs, uncoiled_ys):
            sh = RoundedRectangle(corner_radius=0.10, width=chain.width + 0.20, height=0.26, stroke_color=BLUE, stroke_width=2.2, fill_color=BLUE, fill_opacity=0.18).move_to(chain)
            sheaths.add(sh)
            lx = chain.get_left()[0]
            rx = chain.get_right()[0]
            count = max(3, n // 2)
            for k in range(count):
                xx = lx + (k + 0.5) * (rx - lx) / count
                s = Line([xx - 0.06, uy + 0.16, 0], [xx + 0.06, uy + 0.16, 0], color=BLUE, stroke_width=4.0)
                minus_strokes.add(s)

        neg_term = T("−", size=34, color=BLUE, weight=BOLD).next_to(gel.slab, RIGHT, buff=0.18).set_y(GEL_Y1 - 0.25)
        pos_term = T("+", size=34, color=BLUE, weight=BOLD).next_to(gel.slab, RIGHT, buff=0.18).set_y(GEL_Y0 + 0.25)
        self.play(FadeIn(sheaths, lag_ratio=0.1), FadeIn(minus_strokes, lag_ratio=0.06), FadeIn(neg_term), FadeIn(pos_term), run_time=2.2)

        self.at("sort by size")
        targets_y = [0.65, BAND_Y, -1.68]
        chain_with_charges = VGroup()
        idx = 0
        for chain, sh, (n, _, _, _) in zip(coiled, sheaths, specs):
            cnt = max(3, n // 2)
            grp = VGroup(sh, chain, *minus_strokes[idx:idx + cnt])
            idx += cnt
            chain_with_charges.add(grp)

        self.play(
            *[grp.animate.set_y(ty) for grp, ty in zip(chain_with_charges, targets_y)],
            run_time=2.2,
        )

        self.at("small ones")
        demo_bands = VGroup(
            build_gel_band(SAMPLE_X, targets_y[0], width=1.80, height=0.16, color=GREY, opacity=0.75),
            build_gel_band(SAMPLE_X, BAND_Y, width=1.80, height=0.18, color=GOLD, opacity=1.0),
            build_gel_band(SAMPLE_X, targets_y[2], width=1.80, height=0.16, color=GREY, opacity=0.75),
        )
        fast_lbl = T("small runs\nfastest", size=24, color=TEXT, line_spacing=0.85).next_to(gel.slab, RIGHT, buff=0.22).set_y(targets_y[2] + 0.55)
        self.play(FadeOut(chain_with_charges), FadeIn(demo_bands), FadeIn(fast_lbl), run_time=0.9)
        self.play(
            FadeOut(demo_bands[0]),
            FadeOut(demo_bands[2]),
            FadeOut(fast_lbl),
            run_time=0.9,
        )
        self.finish()


class S03Ladder(SpokenScene):
    def construct(self):
        vessel = build_vessel()
        gel = build_gel_panel(show_terminals=True)
        band = build_gel_band(SAMPLE_X, BAND_Y, width=1.80, height=0.18, color=GOLD, opacity=1.0)
        sds_title = T("SDS-PAGE", size=34, color=TEXT).move_to([1.3, 3.22, 0])
        scope = build_scope()
        self.add(vessel, gel, band, sds_title, scope)

        ladder_bands, ladder_tags = build_ladder_bands()
        start_bands = VGroup(*[build_gel_band(LADDER_X, 1.74, width=1.60, height=0.12, color=TEAL, opacity=0.9) for _ in ladder_bands])
        self.add(start_bands)
        self.play(
            *[sb.animate.move_to(tb.get_center()).stretch_to_fit_height(0.16) for sb, tb in zip(start_bands, ladder_bands)],
            run_time=3.2,
        )

        self.at("runs in the next lane")
        # Reveal size words while highlighting the ladder bands top-to-bottom
        lad_hl = RoundedRectangle(corner_radius=0.08, width=1.80, height=0.30, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.22).move_to(ladder_bands[0])
        self.play(FadeIn(ladder_tags, lag_ratio=0.18), FadeIn(lad_hl), run_time=1.2)
        self.play(lad_hl.animate.move_to(ladder_bands[-1]), run_time=1.0)
        self.play(FadeOut(lad_hl), run_time=0.4)

        self.at("read the band")
        ruler = DashedLine(
            [SAMPLE_X - 0.94, BAND_Y, 0],
            [LADDER_X + 0.85, BAND_Y, 0],
            color=TEAL,
            stroke_width=4.5,
            dash_length=0.14,
        )
        arrow_tip = Triangle(color=TEAL, fill_opacity=1).scale(0.13).rotate(PI / 2).move_to([LADDER_X + 0.90, BAND_Y, 0])
        self.play(Create(ruler), FadeIn(arrow_tip), run_time=1.6)

        self.at("estimate")
        est_tag = boxed_label("estimated size", color=TEAL, size=24, pad=0.14, fill_opacity=0.26).move_to([SAMPLE_X, BAND_Y + 0.65, 0])
        br_pair = RoundedRectangle(corner_radius=0.10, width=1.82, height=1.18, stroke_color=TEAL, stroke_width=2.5, fill_color=TEAL, fill_opacity=0.10).move_to([LADDER_X, BAND_Y, 0])
        self.play(FadeIn(est_tag, shift=UP * 0.08), Create(br_pair), run_time=1.8)

        self.at("first answer")
        card1 = build_cards(count=1, active=0)
        self.play(FadeIn(card1, shift=RIGHT * 0.5), run_time=1.5)
        self.finish()


class S04Limit(SpokenScene):
    def construct(self):
        vessel = build_vessel()
        cards = build_cards(count=1, active=0)
        gel = build_gel_panel(show_terminals=False)
        band = build_gel_band(SAMPLE_X, BAND_Y, width=1.80, height=0.18, color=GOLD, opacity=1.0)
        ladder_bands, ladder_tags = build_ladder_bands()
        sds_title = T("SDS-PAGE", size=34, color=TEXT).move_to([1.3, 3.22, 0])
        scope = build_scope()
        self.add(vessel, cards, gel, band, ladder_bands, ladder_tags, sds_title, scope)

        clean_box = RoundedRectangle(
            corner_radius=0.10, width=2.15, height=3.55, stroke_color=TEAL, stroke_width=3.2, fill_color=TEAL, fill_opacity=0.12
        ).move_to([SAMPLE_X, -0.25, 0])
        clean_lbl = T("clean lane", size=24, color=TEAL).next_to(gel.slab, RIGHT, buff=0.22).set_y(0.75)
        self.play(Create(clean_box), FadeIn(clean_lbl), run_time=2.2)

        self.at("but not enough")
        win = RoundedRectangle(
            corner_radius=0.16, width=3.9, height=2.55, stroke_color=GOLD, stroke_width=3.2, fill_color=BG, fill_opacity=0.97
        ).move_to([2.15, -0.35, 0])
        gold_chains = VGroup(
            build_bead_chain(9, [2.15, 0.28, 0], step=0.24, radius=0.072, color=GOLD),
            build_bead_chain(9, [2.15, -0.10, 0], step=0.24, radius=0.072, color=GOLD),
            build_bead_chain(9, [2.15, -0.48, 0], step=0.24, radius=0.072, color=GOLD),
        )
        self.play(FadeOut(clean_box), FadeOut(clean_lbl), FadeIn(win, scale=0.6), FadeIn(gold_chains), run_time=1.8)

        self.at("two proteins of the same size")
        grey_chain = build_bead_chain(9, [2.15, -0.88, 0], step=0.24, radius=0.068, color=GREY)
        same_lbl = T("same size", size=26, color=TEXT).move_to([2.15, -1.28, 0])
        self.play(FadeIn(grey_chain, shift=DOWN * 0.2), FadeIn(same_lbl), run_time=1.4)
        self.wait(0.8)
        self.play(FadeOut(win), FadeOut(gold_chains), FadeOut(grey_chain), FadeOut(same_lbl), run_time=0.9)

        self.at("a contaminant can hide")
        smudge = build_gel_band(SAMPLE_X, -1.55, width=1.80, height=0.16, color=GREY, opacity=0.12)
        meter_frame = Rectangle(width=1.05, height=2.8, stroke_color=TEXT, stroke_width=2.2, fill_color=BG, fill_opacity=0.9).move_to([5.30, -0.3, 0])
        gold_bar = Rectangle(width=0.30, height=2.2, stroke_width=0, fill_color=GOLD, fill_opacity=0.9).move_to([5.07, -0.60, 0])
        grey_bar = Rectangle(width=0.30, height=0.72, stroke_width=0, fill_color=GREY, fill_opacity=0.75).move_to([5.53, -1.34, 0])
        thresh_y = -0.25
        thresh = DashedLine([4.70, thresh_y, 0], [5.90, thresh_y, 0], color=TEAL, stroke_width=3.5, dash_length=0.10)
        limit_lbl = T("stain limit", size=24, color=TEAL).next_to(meter_frame, UP, buff=0.14)
        self.play(FadeIn(smudge), FadeIn(meter_frame), FadeIn(gold_bar), FadeIn(grey_bar), Create(thresh), FadeIn(limit_lbl), run_time=1.8)
        self.finish()


class S05Idea(SpokenScene):
    def construct(self):
        vessel = build_vessel()
        cards1 = build_cards(count=1, active=0)
        gel = build_gel_panel(show_terminals=False)
        band = build_gel_band(SAMPLE_X, BAND_Y, width=1.80, height=0.18, color=GOLD, opacity=1.0)
        ladder_bands, ladder_tags = build_ladder_bands()
        sds_title = T("SDS-PAGE", size=34, color=TEXT).move_to([1.3, 3.22, 0])
        scope = build_scope()
        self.add(vessel, cards1, gel, band, ladder_bands, ladder_tags, sds_title, scope)

        panel_grp = VGroup(gel, band, ladder_bands, ladder_tags)
        self.play(panel_grp.animate.shift(UP * 0.14), run_time=1.1)
        self.play(panel_grp.animate.shift(DOWN * 0.14), run_time=1.0)

        self.at("a band gives a size")
        # Place 'size' tag cleanly above the band inside sample lane (clear of divider)
        size_tag = boxed_label("size", color=TEAL, size=26, pad=0.14, fill_opacity=0.22).move_to([SAMPLE_X, BAND_Y + 0.72, 0])
        size_line = Line(size_tag.get_bottom() + DOWN * 0.04, band.get_top() + UP * 0.04, color=TEAL, stroke_width=3.2)
        self.play(FadeIn(size_tag), Create(size_line), run_time=0.9)

        self.at("not a name")
        # Place 'name: _____' cleanly in right margin (x=5.35, clear of GEL_X1=4.25)
        name_tag = build_name_tag("name: _____", color=GOLD, at=[5.35, BAND_Y, 0])
        name_line = Line(band.get_right() + RIGHT * 0.06, name_tag.get_left() + LEFT * 0.06, color=GOLD, stroke_width=3.2)
        self.play(FadeIn(name_tag), Create(name_line), run_time=1.0)

        self.at("purity and identity")
        purity_lbl = T("purity", size=32, color=TEAL, weight=BOLD).move_to([-0.25, 3.22, 0])
        identity_lbl = T("identity", size=32, color=GOLD, weight=BOLD).move_to([4.65, 3.22, 0])
        arr_p = Arrow([purity_lbl.get_bottom()[0], 2.92, 0], [SAMPLE_X - 0.85, 2.22, 0], color=TEAL, stroke_width=3.5, buff=0)
        arr_i = Arrow([identity_lbl.get_bottom()[0], 2.92, 0], [name_tag.get_top()[0], name_tag.get_top()[1] + 0.12, 0], color=GOLD, stroke_width=3.5, buff=0)
        self.play(FadeOut(sds_title), run_time=0.35)
        self.play(FadeIn(purity_lbl), FadeIn(identity_lbl), Create(arr_p), Create(arr_i), run_time=1.5)

        self.at("antibodies")
        card2 = build_cards(count=2, active=1)[1]
        self.play(FadeIn(card2, shift=RIGHT * 0.25), run_time=1.1)

        self.at("sequence")
        card3 = build_cards(count=3, active=1)[2]
        self.play(FadeIn(card3, shift=RIGHT * 0.25), run_time=1.2)
        self.finish()


class S06Western(SpokenScene):
    def construct(self):
        vessel = build_vessel()
        cards = build_cards(count=3, active=1)
        scope = build_scope()
        gel_box = RoundedRectangle(
            corner_radius=0.14, width=2.55, height=4.35, stroke_color=TEAL, stroke_width=2.8, fill_color=TEAL, fill_opacity=0.15
        ).move_to([-1.85, -0.05, 0])
        gel_lbl = T("gel", size=26, color=TEXT).next_to(gel_box, UP, buff=0.14)

        band_ys = [1.45, 0.75, 0.10, BAND_Y, -1.45]
        gel_bands = VGroup()
        for y in band_ys:
            col = GOLD if y == BAND_Y else GREY
            gel_bands.add(build_gel_band(-1.85, y, width=1.75, height=0.16, color=col, opacity=0.95))

        # Place name tag cleanly in right margin away from membrane label
        name_tag = build_name_tag("name: _____", color=GOLD, at=[4.95, 0.25, 0])
        self.add(vessel, cards, gel_box, gel_lbl, gel_bands, name_tag, scope)

        self.at("copy the gel onto a membrane")
        mem_box = RoundedRectangle(
            corner_radius=0.14, width=2.55, height=4.35, stroke_color=TEXT, stroke_width=2.8, fill_color=TEXT, fill_opacity=0.12
        ).move_to([1.65, -0.05, 0])
        mem_lbl = T("membrane", size=26, color=TEXT).next_to(mem_box, UP, buff=0.14)
        title = T("western blot", size=34, color=TEXT).move_to([-0.10, 3.22, 0])
        self.play(FadeIn(mem_box, shift=RIGHT * 0.3), FadeIn(mem_lbl), FadeIn(title), run_time=1.3)

        self.at("band for band")
        mem_bands = VGroup()
        ghost_lines = VGroup()
        for gb, y in zip(gel_bands, band_ys):
            col = GOLD if y == BAND_Y else GREY
            mb = build_gel_band(1.65, y, width=1.75, height=0.16, color=col, opacity=0.95)
            ln = DashedLine([gb.get_right()[0] + 0.08, y, 0], [mb.get_left()[0] - 0.08, y, 0], color=GREY, stroke_width=2.4, dash_length=0.10)
            mem_bands.add(mb)
            ghost_lines.add(ln)
        self.play(Create(ghost_lines), FadeIn(mem_bands, shift=RIGHT * 0.4), run_time=1.5)

        self.at("probe it with an antibody")
        ab1 = build_antibody_y(PURPLE, scale=0.42).move_to([3.5, 1.45, 0])
        ab2 = build_antibody_y(PURPLE, scale=0.42).move_to([3.5, 0.10, 0])
        ab3 = build_antibody_y(PURPLE, scale=0.42).move_to([3.5, BAND_Y + 0.18, 0])
        ab_lbl = T("antibody", size=24, color=PURPLE).next_to(ab1, RIGHT, buff=0.16)
        self.play(FadeIn(ab1), FadeIn(ab2), FadeIn(ab3), FadeIn(ab_lbl), run_time=0.7)
        self.play(
            ab1.animate.move_to([2.35, 1.45, 0]),
            ab2.animate.move_to([2.35, 0.10, 0]),
            ab3.animate.move_to([1.65, BAND_Y + 0.25, 0]).rotate(-0.15),
            FadeOut(ab_lbl),
            run_time=0.95,
        )

        self.at("only the matching band lights up")
        glow = RoundedRectangle(
            corner_radius=0.08, width=2.05, height=0.38, stroke_color=GOLD, stroke_width=4.5, fill_color=GOLD, fill_opacity=0.32
        ).move_to(mem_bands[3])
        self.play(
            FadeOut(ab1, shift=RIGHT * 0.6),
            FadeOut(ab2, shift=RIGHT * 0.6),
            *[mem_bands[i].animate.set_opacity(0.18) for i in (0, 1, 2, 4)],
            FadeIn(glow),
            run_time=1.9,
        )

        self.at("validated antibody")
        tick = check_mark(color=GREEN).next_to(name_tag, LEFT, buff=0.16)
        sup_lbl = T("supports\nidentity", size=24, color=GOLD, line_spacing=0.85).next_to(name_tag, DOWN, buff=0.20)
        self.play(Create(tick), FadeIn(sup_lbl), name_tag[0].animate.set_fill(GOLD, opacity=0.32), run_time=1.8)
        self.finish()


class S07Mass(SpokenScene):
    def construct(self):
        vessel = build_vessel()
        cards = build_cards(count=3, active=1)
        scope = build_scope()
        tube = build_flight_tube("MALDI-TOF", y0=-0.15, y1=1.95)
        self.add(vessel, cards, scope)

        mem_rect = RoundedRectangle(corner_radius=0.14, width=2.55, height=4.35, stroke_color=TEXT, stroke_width=2.8, fill_color=TEXT, fill_opacity=0.12).move_to([1.3, 0.2, 0])
        self.add(mem_rect)
        self.play(Transform(mem_rect, tube.tube), FadeIn(tube.plate_l), FadeIn(tube.plate_r), FadeIn(tube.lbl_laser), FadeIn(tube.lbl_det), FadeIn(tube.lbl_title), run_time=1.3)
        self.remove(mem_rect)
        self.add(tube)

        whole_chain = build_bead_chain(18, [0.85, 0.90, 0], step=0.25, radius=0.09, color=GOLD)
        self.play(FadeIn(whole_chain, lag_ratio=0.05), run_time=1.0)

        self.at("trypsin cuts")
        cut_scissors = VGroup(*[build_scissors(BLUE, scale=0.40).move_to([-0.95 + 0.72 * i, 1.45, 0]) for i in range(5)])
        self.play(FadeIn(cut_scissors, lag_ratio=0.15), run_time=1.0)
        self.play(cut_scissors.animate.shift(DOWN * 0.55), run_time=0.8)
        masses = [2.0, 3.0, 4.0, 5.0, 6.0, 7.0]
        peptides = VGroup()
        y_lanes = np.linspace(1.62, 0.16, 6)
        for m, yl in zip(masses, y_lanes):
            seg = build_bead_chain(int(m), [-1.65, yl, 0], step=0.17, radius=0.082, color=GOLD)
            bar = RoundedRectangle(corner_radius=0.06, width=seg.width + 0.16, height=0.22, stroke_width=0, fill_color=GOLD, fill_opacity=0.28).move_to(seg)
            peptides.add(VGroup(bar, seg))
        pep_lbl = T("peptides", size=26, color=GOLD).next_to(peptides, RIGHT, buff=0.45)
        self.play(FadeOut(whole_chain), FadeOut(cut_scissors), FadeIn(peptides, lag_ratio=0.12), FadeIn(pep_lbl), run_time=1.8)

        self.at("a laser launches")
        flash = Star(n=8, outer_radius=0.34, inner_radius=0.14, color=GOLD, fill_opacity=0.92).move_to([-2.46, 0.90, 0])
        beam = Line([-2.82, 0.90, 0], [-2.25, 0.90, 0], color=BLUE, stroke_width=7)
        self.play(FadeOut(pep_lbl), FadeIn(flash, scale=0.6), Create(beam), run_time=0.8)
        self.play(FadeOut(flash), FadeOut(beam), *[p.animate.set_x(-1.85) for p in peptides], run_time=1.1)

        self.at("most carry one charge")
        plus_marks = VGroup()
        for p in peptides:
            pm = T("+", size=24, color=BLUE, weight=BOLD).next_to(p, RIGHT, buff=0.06)
            plus_marks.add(pm)
        self.play(FadeIn(plus_marks), run_time=0.7)
        grp = VGroup(*[VGroup(p, pm) for p, pm in zip(peptides, plus_marks)])
        self.play(*[g.animate.shift(RIGHT * 1.1) for g in grp], run_time=0.9)

        self.at("heavier ones arrive later")
        x_now = [p.get_center()[0] for p in peptides]
        dx_light = 4.65 - x_now[0]
        self.play(
            *[g.animate.shift(RIGHT * (dx_light * np.sqrt(2.0 / m))) for g, m in zip(grp, masses)],
            run_time=2.6,
            rate_func=linear,
        )
        self.finish()


class S08Predict(SpokenScene):
    def construct(self):
        vessel = build_vessel()
        cards = build_cards(count=3, active=1)
        scope = build_scope()
        tube = build_flight_tube("MALDI-TOF", y0=0.25, y1=2.10)
        self.add(vessel, cards, tube, scope)

        masses = [2.0, 3.0, 4.0, 5.0, 6.0, 7.0]
        y_lanes = np.linspace(1.70, 0.55, 6)
        dx_light = 4.65 - (-0.75)
        peptides = VGroup()
        for m, yl in zip(masses, y_lanes):
            x_cur = -0.75 + dx_light * np.sqrt(2.0 / m)
            peptides.add(build_bead_chain(int(m), [x_cur, yl, 0], step=0.16, radius=0.075, color=GOLD))
        self.add(peptides)

        axis_y = -1.65
        axis = Line([-2.8, axis_y, 0], [5.4, axis_y, 0], color=GREY, stroke_width=3)
        axis_lbl = T("mass", size=24, color=TEXT).next_to(axis, RIGHT, buff=0.16)
        self.add(axis, axis_lbl)

        peak_xs = [-2.5 + ((m - 1.5) / 6.0) * 7.5 for m in masses]
        peak_hs = [0.78, 0.95, 0.65, 1.05, 0.84, 0.72]
        sticks = VGroup(*[Line([px, axis_y, 0], [px, axis_y + ph, 0], color=GOLD, stroke_width=5)
                          for px, ph in zip(peak_xs, peak_hs)])

        self.play(Create(sticks[0]), run_time=0.5)
        for i in range(1, 6):
            rem = 4.85 - peptides[i].get_center()[0]
            self.play(
                peptides[i].animate.shift(RIGHT * max(0.05, rem)),
                Create(sticks[i]),
                run_time=0.65,
            )

        self.at("but you never read")
        # Place 'no amino acid letters' cleanly INSIDE the vacated flight tube (clear of borders & mass list!)
        no_seq = boxed_label("no amino acid letters", color=RED, size=24, pad=0.12).move_to([1.15, 1.15, 0])
        list_box = RoundedRectangle(corner_radius=0.14, width=3.4, height=1.15, stroke_color=GOLD, stroke_width=2.8, fill_color=BG, fill_opacity=0.92).move_to([-0.8, -1.45, 0])
        list_ticks = VGroup(*[Line([-2.2 + 0.52 * k, -1.78, 0], [-2.2 + 0.52 * k, -1.12, 0], color=GOLD, stroke_width=5) for k in range(6)])
        list_lbl = T("mass list", size=24, color=GOLD).next_to(list_box, UP, buff=0.12)
        self.play(
            FadeIn(no_seq),
            FadeOut(sticks),
            FadeOut(axis),
            FadeOut(axis_lbl),
            FadeIn(list_box),
            FadeIn(list_ticks),
            FadeIn(list_lbl),
            run_time=1.8,
        )

        self.at("can a list of masses")
        name_tag = build_name_tag("name: _____", color=GOLD, at=[3.35, -1.45, 0])
        q_mark = T("?", size=52, color=GOLD, weight=BOLD).next_to(name_tag, RIGHT, buff=0.25)
        q_card = question_card("Can masses name it?", y=-3.10, size=34, max_w=8.5)
        self.play(FadeOut(no_seq), FadeIn(name_tag), FadeIn(q_mark), FadeIn(q_card), run_time=1.8)
        self.finish()


class S09Think(PredictPause):
    QUESTION = "Can masses name it?"
    CARD = {"y": -3.10, "size": 34, "max_w": 8.5}
    RING_AT = (6.0, -2.25, 0)
    SECONDS = 4.5

    def backdrop(self):
        vessel = build_vessel()
        cards = build_cards(count=3, active=1)
        scope = build_scope()
        tube = build_flight_tube("MALDI-TOF", y0=0.25, y1=2.10)
        masses = [2.0, 3.0, 4.0, 5.0, 6.0, 7.0]
        y_lanes = np.linspace(1.70, 0.55, 6)
        peptides = VGroup(*[build_bead_chain(int(m), [4.85, yl, 0], step=0.16, radius=0.075, color=GOLD)
                            for m, yl in zip(masses, y_lanes)])
        list_box = RoundedRectangle(corner_radius=0.14, width=3.4, height=1.15, stroke_color=GOLD, stroke_width=2.8, fill_color=BG, fill_opacity=0.92).move_to([-0.8, -1.45, 0])
        list_ticks = VGroup(*[Line([-2.2 + 0.52 * k, -1.78, 0], [-2.2 + 0.52 * k, -1.12, 0], color=GOLD, stroke_width=5) for k in range(6)])
        list_lbl = T("mass list", size=24, color=GOLD).next_to(list_box, UP, buff=0.12)
        name_tag = build_name_tag("name: _____", color=GOLD, at=[3.35, -1.45, 0])
        q_mark = T("?", size=52, color=GOLD, weight=BOLD).next_to(name_tag, RIGHT, buff=0.25)
        return VGroup(vessel, cards, scope, tube, peptides, list_box, list_ticks, list_lbl, name_tag, q_mark)


class S10Answer(SpokenScene):
    def construct(self):
        vessel = build_vessel()
        cards = build_cards(count=3, active=1)
        scope = build_scope()

        q_old = question_card("Can masses name it?", y=-3.10, size=34, max_w=8.5)
        q_new = question_card("Yes, if the protein is known.", y=-3.10, size=34, max_w=8.5)

        target_fracs = [0.10, 0.24, 0.42, 0.58, 0.76, 0.90]
        probe_w = 2.75
        probe_x = -1.90
        probe_box = RoundedRectangle(corner_radius=0.12, width=probe_w, height=0.60, stroke_color=GOLD, stroke_width=3, fill_color=BG, fill_opacity=0.95).move_to([probe_x, 2.05, 0])
        probe_ticks = VGroup(*[
            Line([probe_x - probe_w / 2 + 0.22 + f * (probe_w - 0.44), 1.82, 0],
                 [probe_x - probe_w / 2 + 0.22 + f * (probe_w - 0.44), 2.28, 0],
                 color=GOLD, stroke_width=5)
            for f in target_fracs
        ])
        probe_lbl = T("mass list", size=24, color=GOLD).next_to(probe_box, UP, buff=0.12)
        probe = VGroup(probe_box, probe_ticks)

        # Place name tag cleanly on the left (-2.35, -0.85) so sliding probe at x=0.60 never overlaps it!
        name_tag = build_name_tag("name: _____", color=GOLD, at=[-2.35, -0.85, 0])
        self.add(vessel, cards, scope, q_old, probe, probe_lbl, name_tag)

        self.play(swap(q_old, q_new, run_time=0.8), run_time=0.9)

        self.at("a computer predicts")
        rng = np.random.default_rng(7)
        db_cards = VGroup()
        card_ys = np.linspace(2.25, -1.55, 6)
        db_x = 3.85
        for idx, cy in enumerate(card_ys):
            fracs = target_fracs if idx == 4 else sorted(rng.uniform(0.08, 0.92, 6))
            box = RoundedRectangle(corner_radius=0.10, width=probe_w, height=0.56, stroke_color=GREY, stroke_width=2.2, fill_color=BG, fill_opacity=0.92).move_to([db_x, cy, 0])
            ticks = VGroup(*[
                Line([db_x - probe_w / 2 + 0.22 + f * (probe_w - 0.44), cy - 0.18, 0],
                     [db_x - probe_w / 2 + 0.22 + f * (probe_w - 0.44), cy + 0.18, 0],
                     color=GREY, stroke_width=4)
                for f in fracs
            ])
            db_cards.add(VGroup(box, ticks))

        db_hdr = T("database digests", size=26, color=TEXT).next_to(db_cards[0], UP, buff=0.16)
        self.play(FadeIn(db_hdr), FadeIn(db_cards, lag_ratio=0.12), run_time=2.0)

        self.at("few proteins give the same set")
        # Slide probe cleanly along x = 0.65 (clear of name_tag at -2.35 and db_cards at +3.85!)
        self.play(FadeOut(probe_lbl), probe.animate.move_to([0.65, card_ys[0], 0]), run_time=0.55)
        for idx in range(5):
            if idx > 0:
                self.play(probe.animate.set_y(card_ys[idx]), run_time=0.38)
            if idx < 4:
                self.play(db_cards[idx].animate.set_opacity(0.25), run_time=0.25)
            else:
                self.play(
                    db_cards[4][0].animate.set_stroke(GOLD, width=4),
                    *[t.animate.set_color(GOLD) for t in db_cards[4][1]],
                    db_cards[5].animate.set_opacity(0.25),
                    run_time=0.65,
                )

        self.at("works like a fingerprint")
        fp_center = np.array([-2.35, 0.75, 0])
        arcs = VGroup(*[
            Arc(radius=0.16 + 0.10 * k, start_angle=-0.4, angle=PI * 1.25, arc_center=fp_center, color=GOLD, stroke_width=4)
            for k in range(6)
        ])
        match_tag = build_name_tag("match found", color=GOLD, at=[-2.35, -0.85, 0])
        tick2 = check_mark(color=GREEN).scale(0.85).next_to(cards[1], RIGHT, buff=0.10)
        self.play(FadeIn(arcs, lag_ratio=0.1), swap(name_tag, match_tag, run_time=0.7), Create(tick2), run_time=1.5)
        self.finish()


class S11Sequence(SpokenScene):
    def construct(self):
        vessel = build_vessel()
        cards = build_cards(count=3, active=2, checked=(1,))
        scope = build_scope()
        title = T("Edman degradation", size=34, color=TEXT).move_to([1.3, 3.22, 0])
        panel = RoundedRectangle(corner_radius=0.18, width=8.8, height=5.0, stroke_color=BLUE, stroke_width=2.8, fill_color=BLUE, fill_opacity=0.14).move_to([1.35, 0.05, 0])
        self.add(vessel, cards, scope, title)

        chain_x = -1.75
        letters = ["M", "A", "L", "G", "K", "V", "T", "R", "S", "E", "D", "F"]
        beads = VGroup(*[
            Dot([chain_x, 1.55 - 0.30 * i, 0], radius=0.135, color=GOLD)
            for i in range(len(letters))
        ])
        n_lbl = T("start (N-terminus)", size=24, color=GOLD).next_to(beads[0], UP, buff=0.18).shift(RIGHT * 0.5)
        reader_box = RoundedRectangle(corner_radius=0.12, width=2.8, height=1.20, stroke_color=BLUE, stroke_width=3, fill_color=BG, fill_opacity=0.95).move_to([2.4, 1.45, 0])
        reader_lbl = T("reader", size=24, color=BLUE).next_to(reader_box, UP, buff=0.12)
        self.play(FadeIn(panel), FadeIn(beads, lag_ratio=0.06), FadeIn(n_lbl), FadeIn(reader_box), FadeIn(reader_lbl), run_time=2.6)

        self.at("clips the first residue")
        read_letters = VGroup()
        for idx in range(3):
            b = beads[idx]
            clip_bar = Line([chain_x - 0.35, b.get_y(), 0], [chain_x + 0.35, b.get_y(), 0], color=BLUE, stroke_width=4.5)
            big_l = T(letters[idx], size=36, color=GOLD, weight=BOLD).move_to(reader_box.get_center())
            self.play(Create(clip_bar), run_time=0.25)
            self.play(FadeOut(clip_bar), b.animate.move_to(reader_box.get_center()), run_time=0.55)
            lt = T(letters[idx], size=34, color=GOLD, weight=BOLD).move_to([1.35 + 0.70 * idx, 0.20, 0])
            read_letters.add(lt)
            self.play(FadeOut(b), FadeIn(big_l), reader_box.animate.set_fill(BLUE, opacity=0.28), run_time=0.35)
            self.play(ReplacementTransform(big_l, lt), reader_box.animate.set_fill(BG, opacity=0.95), run_time=0.45)

        self.at("each cycle")
        self.play(FadeOut(beads[3:]), FadeOut(n_lbl), FadeOut(read_letters), run_time=0.5)
        multi = VGroup(*[
            VGroup(*[Dot([-2.1 + 0.45 * c, 1.45 - 0.28 * r, 0], radius=0.11, color=GOLD) for r in range(7)])
            for c in range(4)
        ])
        self.play(FadeIn(multi), run_time=0.6)
        cyc = ValueTracker(1)
        cyc_read = counter("cycle {:.0f}: 0.98^n in step", cyc, at=[2.5, -0.35, 0], size=24, color=TEXT)
        blur_read = T("M / A / L ?", size=28, color=RED).move_to(reader_box.get_center())
        self.add(cyc_read)
        self.play(
            multi[1].animate.shift(DOWN * 0.28),
            multi[2].animate.shift(DOWN * 0.56),
            multi[3].animate.shift(DOWN * 0.28),
            cyc.animate.set_value(50),
            FadeIn(blur_read),
            run_time=2.8,
        )

        self.at("so long proteins are cut")
        self.play(FadeOut(multi), FadeOut(cyc_read), FadeOut(blur_read), FadeOut(reader_box), FadeOut(reader_lbl), run_time=0.6)
        top_chain = build_bead_chain(12, [0.4, 1.40, 0], step=0.32, radius=0.10, color=GOLD)
        bot_chain = build_bead_chain(12, [0.4, 0.75, 0], step=0.32, radius=0.10, color=GOLD)
        sc1 = build_scissors(BLUE, scale=0.34).move_to([-0.24, 1.72, 0])
        sc2 = build_scissors(BLUE, scale=0.34).move_to([1.04, 1.72, 0])
        sc3 = build_scissors(BLUE, scale=0.34).move_to([0.40, 0.35, 0])
        self.play(FadeIn(top_chain), FadeIn(bot_chain), FadeIn(sc1), FadeIn(sc2), FadeIn(sc3), run_time=1.0)

        self.at("overlapping peptides")
        self.play(FadeOut(sc1), FadeOut(sc2), FadeOut(sc3), run_time=0.3)
        p1 = T("M-A-L-G", size=28, color=GOLD).move_to([-1.1, -0.50, 0])
        p2 = T("L-G-K-V-T-R", size=28, color=GOLD).move_to([0.5, -1.10, 0])
        p3 = T("T-R-S-E-D-F", size=28, color=GOLD).move_to([2.4, -1.70, 0])
        ov_lbl = T("overlapping reads", size=26, color=TEXT).move_to([1.3, 2.22, 0])
        self.play(FadeIn(ov_lbl), FadeIn(p1), FadeIn(p2), FadeIn(p3), run_time=1.5)
        self.finish()


class S12Tandem(SpokenScene):
    def construct(self):
        vessel = build_vessel()
        cards = build_cards(count=3, active=2, checked=(1,))
        scope = build_scope()
        tube = build_flight_tube("tandem MS", y0=0.45, y1=2.25)
        self.add(vessel, cards, scope)

        pep = build_bead_chain(6, [-2.1, 1.35, 0], step=0.34, radius=0.11, color=GOLD)
        self.play(FadeIn(tube), FadeIn(pep), run_time=1.1)
        self.play(pep.animate.move_to([1.4, 1.35, 0]), run_time=2.5)

        self.at("one peptide breaks")
        flash = Rectangle(width=4.2, height=1.5, stroke_width=0, fill_color=BLUE, fill_opacity=0.25).move_to([1.3, 1.35, 0])
        stair = VGroup(*[
            build_bead_chain(6 - k, [-1.2 + (6 - k) * 0.16, 2.00 - k * 0.25, 0], step=0.30, radius=0.082, color=GOLD)
            for k in range(6)
        ])
        self.play(FadeIn(flash), run_time=0.5)
        self.play(FadeOut(flash), FadeOut(pep), FadeIn(stair, lag_ratio=0.18), run_time=2.5)
        self.play(stair.animate.shift(RIGHT * 1.4), run_time=1.4)

        self.at("each gap between peaks")
        res_letters = ["M", "A", "L", "G", "K", "I"]
        res_masses = [131.0, 71.0, 113.0, 57.0, 128.0, 113.0]
        cum = np.concatenate([[0.0], np.cumsum(res_masses)])
        ax_y = -2.05
        xs = -2.5 + (cum / cum[-1]) * 7.6
        axis = Line([-2.7, ax_y, 0], [5.4, ax_y, 0], color=GREY, stroke_width=3)
        ax_lbl = T("mass", size=24, color=TEXT).next_to(axis, RIGHT, buff=0.14)
        peaks = VGroup(*[Line([x, ax_y, 0], [x, ax_y + 1.05, 0], color=GOLD, stroke_width=5) for x in xs])
        self.play(Create(axis), FadeIn(ax_lbl), Create(peaks, lag_ratio=0.15), run_time=1.6)

        brackets = VGroup()
        gap_letters = VGroup()
        for i, let in enumerate(res_letters):
            x0, x1 = xs[i], xs[i + 1]
            y_b = ax_y + 1.22
            br = VGroup(
                Line([x0 + 0.04, y_b - 0.08, 0], [x0 + 0.04, y_b, 0], color=BLUE, stroke_width=3.2),
                Line([x0 + 0.04, y_b, 0], [x1 - 0.04, y_b, 0], color=BLUE, stroke_width=3.5),
                Line([x1 - 0.04, y_b - 0.08, 0], [x1 - 0.04, y_b, 0], color=BLUE, stroke_width=3.2),
            )
            lt = T(let, size=26, color=TEXT, weight=BOLD).next_to(br, UP, buff=0.10)
            brackets.add(br)
            gap_letters.add(lt)
        self.play(
            *[AnimationGroup(Create(b), FadeIn(l)) for b, l in zip(brackets, gap_letters)],
            lag_ratio=0.25,
            run_time=2.8,
        )

        self.at("weigh the same")
        same_lbl = T("same mass", size=26, color=RED).move_to([1.3, -0.15, 0])
        l_or_i_1 = T("L or I?", size=24, color=RED, weight=BOLD).move_to(gap_letters[2])
        l_or_i_2 = T("L or I?", size=24, color=RED, weight=BOLD).move_to(gap_letters[5])
        eq_link = DashedLine(
            [brackets[2].get_top()[0], -0.42, 0],
            [brackets[5].get_top()[0], -0.42, 0],
            color=RED,
            stroke_width=2.8,
            dash_length=0.12,
        )
        self.play(
            brackets[2].animate.set_color(RED),
            brackets[5].animate.set_color(RED),
            swap(gap_letters[2], l_or_i_1, run_time=0.6),
            swap(gap_letters[5], l_or_i_2, run_time=0.6),
            FadeIn(same_lbl),
            Create(eq_link),
            run_time=2.6,
        )
        self.finish()


class S13Sanger(SpokenScene):
    def construct(self):
        vessel = build_vessel()
        cards = build_cards(count=3, active=2, checked=(1,))
        scope = build_scope()
        self.add(vessel, cards, scope)

        left_frame = RoundedRectangle(corner_radius=0.16, width=4.4, height=4.9, stroke_color=GOLD, stroke_width=2.8, fill_color=GOLD, fill_opacity=0.08).move_to([-1.15, 0.05, 0])
        right_frame = RoundedRectangle(corner_radius=0.16, width=4.4, height=4.9, stroke_color=TEAL, stroke_width=2.8, fill_color=TEAL, fill_opacity=0.08).move_to([3.65, 0.05, 0])
        left_head = T("Sanger, insulin", size=28, color=GOLD).move_to([-1.15, 2.15, 0])
        right_head = T("mass spectrometry", size=28, color=TEAL).move_to([3.65, 2.15, 0])
        self.add(left_frame, right_frame, left_head, right_head)

        yrs = ValueTracker(0.0)
        yr_counter = counter("{:.0f} years", yrs, at=[-1.15, -1.85, 0], size=32, color=GOLD)
        beads_51 = VGroup()
        for r, cnt, y_pos in [(0, 11, 1.30), (1, 10, 0.90), (2, 10, 0.25), (3, 10, -0.15), (4, 10, -0.55)]:
            for c in range(cnt):
                bx = -2.85 + c * 0.34
                beads_51.add(Dot([bx, y_pos, 0], radius=0.09, color=GOLD))
        bridge1 = Line([-2.17, 0.90, 0], [-2.17, 0.25, 0], color=TEXT, stroke_width=2)
        bridge2 = Line([-0.47, 0.90, 0], [-0.47, -0.55, 0], color=TEXT, stroke_width=2)
        self.add(yr_counter)

        self.play(
            FadeIn(beads_51, lag_ratio=0.08),
            yrs.animate(rate_func=linear).set_value(12.0),
            run_time=5.2,
        )
        self.play(Create(bridge1), Create(bridge2), run_time=0.5)

        self.at("Today, mass spectrometry")
        rng = np.random.default_rng(7)
        ax_y = -0.85
        r_axis = Line([1.85, ax_y, 0], [5.45, ax_y, 0], color=GREY, stroke_width=2.5)
        pk_xs = np.linspace(2.05, 5.25, 14)
        pk_hs = rng.uniform(0.45, 1.95, 14)
        r_peaks = VGroup(*[Line([x, ax_y, 0], [x, ax_y + h, 0], color=TEAL, stroke_width=4) for x, h in zip(pk_xs, pk_hs)])
        scan = Line([1.85, ax_y, 0], [1.85, 1.40, 0], color=GOLD, stroke_width=3.5)
        self.add(r_axis, scan)
        self.play(
            scan.animate.set_x(5.45),
            Create(r_peaks, lag_ratio=0.08),
            run_time=3.0,
            rate_func=linear,
        )

        self.at("single run")
        one_run = boxed_label("one run", color=TEAL, size=28, pad=0.16).move_to([3.65, -1.85, 0])
        self.play(FadeOut(scan), FadeIn(one_run), run_time=0.8)
        self.finish()


class S14Return(SpokenScene):
    def construct(self):
        vessel = build_vessel()
        cards = build_cards(count=3, active=None)
        gel = build_gel_panel(show_terminals=False)
        band = build_gel_band(SAMPLE_X, BAND_Y, width=1.80, height=0.18, color=GOLD, opacity=1.0)
        ladder_bands, ladder_tags = build_ladder_bands()
        # Place 'identity' tag cleanly in right margin (x=5.35, clear of GEL_X1=4.25)
        name_tag = build_name_tag("identity", color=GOLD, at=[5.35, BAND_Y, 0])
        name_line = Line(band.get_right() + RIGHT * 0.06, name_tag.get_left() + LEFT * 0.06, color=GOLD, stroke_width=3.2)
        scope = build_scope()
        self.add(vessel, cards, gel, band, ladder_bands, ladder_tags, name_tag, name_line, scope)

        self.at("opens the question")
        win = RoundedRectangle(corner_radius=0.16, width=3.2, height=1.6, stroke_color=GOLD, stroke_width=3, fill_color=BG, fill_opacity=0.96).move_to([SAMPLE_X, BAND_Y, 0])
        g_chain = build_bead_chain(8, [SAMPLE_X, BAND_Y + 0.30, 0], step=0.22, radius=0.06, color=GOLD)
        k_chain = build_bead_chain(8, [SAMPLE_X, BAND_Y - 0.30, 0], step=0.22, radius=0.06, color=GREY)
        self.play(FadeIn(win, scale=0.7), FadeIn(g_chain), FadeIn(k_chain), run_time=1.3)

        self.at("does not close it")
        self.play(FadeOut(win, scale=0.7), FadeOut(g_chain), FadeOut(k_chain), run_time=1.4)

        self.at("size comes from the gel")
        l1 = Line(cards[0].get_right() + RIGHT * 0.08, [GEL_X0 - 0.08, 1.78, 0], color=TEAL, stroke_width=4.0)
        lad_hl = RoundedRectangle(corner_radius=0.10, width=1.85, height=3.55, stroke_color=TEAL, stroke_width=3.0, fill_color=TEAL, fill_opacity=0.14).move_to([LADDER_X, -0.25, 0])
        self.play(Create(l1), Create(lad_hl), run_time=1.6)

        self.at("antibodies")
        ab_icon = build_antibody_y(PURPLE, scale=0.30).next_to(cards[1], RIGHT, buff=0.10)
        self.play(FadeOut(lad_hl), FadeIn(ab_icon, shift=LEFT * 0.2), run_time=0.9)

        self.at("masses")
        ticks_icon = VGroup(*[Line([0, -0.11, 0], [0, 0.11, 0], color=GOLD, stroke_width=3).shift(RIGHT * 0.10 * i) for i in range(4)])
        ticks_icon.next_to(ab_icon, RIGHT, buff=0.10)
        self.play(FadeIn(ticks_icon, shift=LEFT * 0.15), run_time=0.55)

        self.at("or sequence")
        seq_icon = T("M-A-L", size=24, color=BLUE).move_to([CARDS_X, 0.92, 0])
        route = VMobject(stroke_color=GOLD, stroke_width=3.2).set_points_as_corners([
            [CARDS_X + 0.55, 0.92, 0],
            [-3.90, 0.92, 0],
            [-3.90, -2.85, 0],
            [5.35, -2.85, 0],
            [5.35, BAND_Y - 0.34, 0],
        ])
        self.play(FadeIn(seq_icon, shift=UP * 0.1), Create(route), run_time=0.75)
        self.finish()


class S15End(EndCard):
    LINE = "A band shows size; antibodies, masses or sequence name the protein."
