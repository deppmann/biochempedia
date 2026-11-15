"""How Chemistry Becomes a Read — Sequencing and Genomes (12 scenes).

COLOUR MAP (one colour per concept, used across the entire film):
- BLUE  (#58C4DD): DNA template strand, template lanes, genomic reference paths
- GOLD  (#D4A843): Newly copied DNA strand, ordered reads, base tiles
- RED   (#FC6255): Permanent chain-terminating dideoxynucleotide (ddNTP) stop
- TEAL  (#3FB8C0): Reversible terminator pause block (removable dye + block)
- GREEN (#83C167): Detected signal (camera sweep, consensus base calls, ionic current trace)
- GREY  (#8B93A1): Uncertainty markers ('?'), reference guides, schematic tags
- TEXT  (#E8EAF0): Polymerase marker, starting primer block, primary labels, base letters

ONE PICTURE OF THE WORLD:
A continuous blue DNA template ribbon passing through a white polymerase marker while a gold
copy grows beside it. Every sequencing chemistry is shown as a direct operation on this same
template-copy-polymerase system: permanent stops creating a sorted length ladder (Sanger),
reversible pauses cycling across aligned clusters (short-read), single-molecule circling and
pore translocation (long-read), and the resulting reads as fragment evidence tested against
candidate positions and a branching genomic path.

WHAT CHANGES IN EACH SPOKEN SCENE (and what it is computed from):
- s01_hook:     Blue template (60-base sequence from np.random.default_rng(7)) scrolls left
                across the frame driven by a continuous ValueTracker step_t; the gold copy
                grows base-by-base beside it at the white polymerase clamp, revealing ordered
                complementary bases as step_t advances.
- s03_sanger:   The carried blue template fans into 4 parallel blue lanes starting from white
                primer blocks; bases extend step-by-step until red ddNTP stop blocks join at
                distinct positions [4, 2, 5, 3] (computed from rng(7)), halting each lane
                immediately while the remaining lanes continue extending.
- s04_ladder:   The 4 stopped copies glide vertically into sorted length order (shortest at
                bottom to longest at top: lengths 2, 3, 4, 5); red endpoints reveal base
                identities sequentially and flash bottom-to-top to feed base tiles into a 5'->3'
                gold read, then the antiparallel blue template complement pairs beside it and
                flips its direction arrow to show reverse complement.
- s05_predict:  Blue template drifts smoothly beneath the paused gold copy while one red stop
                transforms into a teal pause block; a green camera icon and grey '?' appear
                above and after it with the predict question card.
- s07_cycles:   The single gold copy duplicates into a 6-strand aligned cluster; a three-state
                ring (add, image, reset) rotates through cycles as a green camera frame sweeps
                paused teal blocks, teal blocks lift to expose free ends, and new base tiles
                accumulate in the cluster's read strip.
- s08_compare:  Split frame: left panel sorts the 4 red-ended Sanger copies once into a ladder;
                right panel cycles teal pauses across a cluster, zooms out to a 6x4 field of
                gold clusters flashing in unison, then focuses on one short fragment read
                inward from both ends.
- s09_long:     Short fragment becomes one long gold ribbon: first it circles past the white
                polymerase 3 full revolutions while green base calls stack into a consensus row;
                then it straightens and threads through a pore block while a live computed
                stepped ionic current curve (from base-specific levels + deterministic noise)
                draws in a Plot and decodes base-by-base into ordered green base tiles.
- s10_evidence: Full blue template returns above the 3 method outputs, which transform into 3
                labelled evidence cards (Sanger ladder, short-read pair, long read); each card's
                candidate alignment marker slides across multiple positions on the blue template
                under grey '?' markers without resolving placement.
- s11_rule:     The 3 evidence cards and their chemistry icons (stop, pause cycle, current trace)
                transform and merge into one large ordered gold read of base tiles; the read
                glides toward a branching blue genomic path and stops before the fork, probing
                both branches equally.
"""

from bp_parts import *

# ------------------------------------------------------------------ deterministic biology data
RNG = np.random.default_rng(7)
BASES = ["A", "C", "G", "T"]
COMPLEMENT = {"A": "T", "T": "A", "C": "G", "G": "C"}

TEMPLATE_60 = [str(b) for b in RNG.choice(BASES, size=60)]
SANGER_NEW = [str(b) for b in RNG.choice(BASES, size=4)]
SANGER_STOP_LENGTHS = [4, 2, 5, 3]
CYCLE_BASES = [str(b) for b in RNG.choice(BASES, size=3)]
LONG_BASES = [str(b) for b in RNG.choice(BASES, size=10)]

BASE_CURRENT = {"A": 0.78, "C": 0.42, "G": 0.62, "T": 0.24}
PORE_NOISE = RNG.normal(0.0, 0.022, size=240)


def nanopore_current(u):
    """Computed schematic ionic current (0..1) as strand position u in [0, 10] passes through pore."""
    u_clip = float(np.clip(u, 0.0, 9.999))
    idx = int(u_clip)
    frac = u_clip - idx
    cur = BASE_CURRENT[LONG_BASES[idx]]
    if idx + 1 < len(LONG_BASES) and frac > 0.75:
        nxt = BASE_CURRENT[LONG_BASES[idx + 1]]
        blend = 0.5 - 0.5 * np.cos(np.pi * (frac - 0.75) / 0.25)
        cur = (1.0 - blend) * cur + blend * nxt
    ni = min(len(PORE_NOISE) - 1, int(u_clip / 10.0 * len(PORE_NOISE)))
    return float(np.clip(cur + PORE_NOISE[ni], 0.08, 0.94))


# ------------------------------------------------------------------ shared visual helpers
def make_template_strip(n_slots=24, slot_w=1.05, height=0.82, y=0.65, seq=TEMPLATE_60, start_idx=0):
    """Build a thick blue DNA template ribbon with base letters."""
    total_w = n_slots * slot_w
    bar = RoundedRectangle(
        corner_radius=0.14, width=total_w, height=height,
        stroke_color=BLUE, stroke_width=3.5, fill_color=BLUE, fill_opacity=0.28,
    ).move_to([0, y, 0])
    ticks = VGroup()
    for i in range(n_slots):
        cx = -total_w / 2 + (i + 0.5) * slot_w
        notch = Line(
            [cx, y - height / 2, 0], [cx, y - height / 2 + 0.16, 0],
            color=BLUE, stroke_width=2.5,
        )
        b = T(seq[(start_idx + i) % len(seq)], size=24, color=TEXT).move_to([cx, y + 0.05, 0])
        ticks.add(notch, b)
    g = VGroup(bar, ticks)
    g.layout_ok = "edge"   # deliberate off-screen continuation per script
    return g


def make_polymerase_clamp(x=-0.5, y_top=1.22, y_bot=-0.92, width=1.18):
    """Open top-and-bottom white polymerase clamp framing 1 base position without slicing letters."""
    hw = width / 2
    top_bar = VMobject(stroke_color=TEXT, stroke_width=5).set_points_as_corners([
        [x - hw, y_top - 0.14, 0], [x - hw, y_top, 0], [x + hw, y_top, 0], [x + hw, y_top - 0.14, 0],
    ])
    bot_bar = VMobject(stroke_color=TEXT, stroke_width=5).set_points_as_corners([
        [x - hw, y_bot + 0.14, 0], [x - hw, y_bot, 0], [x + hw, y_bot, 0], [x + hw, y_bot + 0.14, 0],
    ])
    halo = Rectangle(
        width=width, height=y_top - y_bot - 0.06,
        stroke_width=0, fill_color=TEXT, fill_opacity=0.07,
    ).move_to([x, (y_top + y_bot) / 2, 0])
    return VGroup(halo, top_bar, bot_bar)


def make_block(width=0.95, height=0.68, color=GOLD, label=None, text_color=TEXT, size=24, fill_opacity=0.26):
    """A clean rectangular nucleotide or terminator block (no molecular structures)."""
    rect = RoundedRectangle(
        corner_radius=0.12, width=width, height=height,
        stroke_color=color, stroke_width=3.0, fill_color=color, fill_opacity=fill_opacity,
    )
    if label is None:
        return rect
    txt = T(label, size=size, color=text_color).move_to(rect)
    return VGroup(rect, txt)


def make_camera_icon(color=GREEN, width=1.1, height=0.76):
    """Geometric camera icon with an outer body and inner aperture ring."""
    body = RoundedRectangle(
        corner_radius=0.14, width=width, height=height,
        stroke_color=color, stroke_width=3.0, fill_color=color, fill_opacity=0.15,
    )
    bump = RoundedRectangle(
        corner_radius=0.06, width=0.38, height=0.18,
        stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.25,
    ).next_to(body, UP, buff=0.0)
    ring = Circle(radius=0.22, stroke_color=color, stroke_width=3.0, fill_color=BG, fill_opacity=0.7).move_to(body)
    iris = Circle(radius=0.10, stroke_color=color, stroke_width=2.0, fill_color=color, fill_opacity=0.45).move_to(body)
    g = VGroup(body, bump, ring, iris)
    g.iris = iris
    g.ring = ring
    return g


def build_predict_picture(drift_tracker=None, y_shift=0.25):
    """Carried world for S05Predict and S06Pause: template, aligned gold copy, teal pause, camera, '?'."""
    y_tpl = 0.65 + y_shift
    y_cpy = -0.45 + y_shift
    step_w = 1.05
    # Slots on make_template_strip(n_slots=20, slot_w=1.05): slot i center is -10.5 + (i + 0.5) * 1.05.
    # For i = 8, 9, 10 -> x = -1.575, -0.525, +0.525 (exact vertical pairing beneath template bases).
    slot_x = lambda i: -20 * step_w / 2 + (i + 0.5) * step_w
    dx = (drift_tracker.get_value() if drift_tracker is not None else 0.0)
    tpl = make_template_strip(n_slots=20, slot_w=step_w, height=0.76, y=y_tpl).shift(LEFT * dx)

    primer = make_block(1.30, 0.66, TEXT, "primer", TEXT, size=24, fill_opacity=0.15).move_to(
        [slot_x(7) - 0.16 - dx, y_cpy, 0]
    )
    b1 = make_block(0.88, 0.66, GOLD, COMPLEMENT[TEMPLATE_60[8]], TEXT, size=26).move_to([slot_x(8) - dx, y_cpy, 0])
    b2 = make_block(0.88, 0.66, GOLD, COMPLEMENT[TEMPLATE_60[9]], TEXT, size=26).move_to([slot_x(9) - dx, y_cpy, 0])
    b3 = make_block(0.88, 0.66, GOLD, COMPLEMENT[TEMPLATE_60[10]], TEXT, size=26).move_to([slot_x(10) - dx, y_cpy, 0])
    pause_blk = make_block(1.22, 0.66, TEAL, "pause", TEXT, size=24, fill_opacity=0.35).move_to([slot_x(11) + 0.04 - dx, y_cpy, 0])
    gold_copy = VGroup(primer, b1, b2, b3, pause_blk)

    cam = make_camera_icon(GREEN).move_to([pause_blk.get_center()[0], y_tpl + 1.35, 0])
    cam_lab = T("camera", size=26, color=GREEN).next_to(cam, UP, buff=0.14)
    q_mark = T("?", size=56, color=GREY, weight=BOLD).next_to(pause_blk, RIGHT, buff=0.50)
    next_slot = DashedVMobject(
        RoundedRectangle(corner_radius=0.12, width=0.88, height=0.66, stroke_color=GREY, stroke_width=2.5),
        num_dashes=14,
    ).move_to([slot_x(13) - dx, y_cpy, 0])

    tpl_lab = T("template", size=26, color=BLUE).move_to([-4.9, y_tpl + 0.72, 0])
    cpy_lab = T("copy", size=26, color=GOLD).move_to([-4.9, y_cpy - 0.72, 0])
    pause_lab = T("removable pause", size=26, color=TEAL).next_to(pause_blk, DOWN, buff=0.38)

    g = VGroup(tpl, gold_copy, cam, cam_lab, q_mark, next_slot, tpl_lab, cpy_lab, pause_lab)
    g.tpl = tpl
    g.gold_copy = gold_copy
    g.pause_blk = pause_blk
    g.cam = cam
    g.q_mark = q_mark
    g.next_slot = next_slot
    g.pause_lab = pause_lab
    return g


# ------------------------------------------------------------------ S01Hook
class S01Hook(SpokenScene):
    def construct(self):
        step_t = ValueTracker(0.0)
        slot_w = 1.05
        y_tpl = 0.72
        y_cpy = -0.42
        # Slot i=9 on n_slots=20, slot_w=1.05 is centered at -10.5 + 9.5*1.05 = -0.525
        poly_x = -0.525

        def _build_tpl():
            s = step_t.get_value()
            frac = s - int(s)
            base_idx = int(s)
            return make_template_strip(
                n_slots=20, slot_w=slot_w, height=0.82, y=y_tpl,
                seq=TEMPLATE_60, start_idx=base_idx,
            ).shift(LEFT * (frac * slot_w))

        tpl_ribbon = always_redraw(_build_tpl)
        poly = make_polymerase_clamp(x=poly_x, y_top=1.28, y_bot=-0.95, width=1.18)
        active_hl = always_redraw(
            lambda: RoundedRectangle(
                corner_radius=0.12,
                width=0.62 + 0.08 * abs(np.sin(PI * step_t.get_value())),
                height=0.66 + 0.08 * abs(np.sin(PI * step_t.get_value())),
                stroke_width=0,
                fill_color=GOLD,
                fill_opacity=0.14 + 0.22 * abs(np.sin(PI * step_t.get_value())),
            ).move_to([poly_x, y_tpl, 0])
        )

        def _build_copy():
            s = step_t.get_value()
            n_full = int(s) + 1
            frac = s - int(s)
            g = VGroup()
            visible = min(n_full, 8)
            for k in range(visible):
                seq_idx = n_full - 1 - k
                # Exact complementary alignment: k=0 at frac=0 pairs with template slot i=9 (start_idx + 9)
                base = COMPLEMENT[TEMPLATE_60[(seq_idx + 9) % len(TEMPLATE_60)]]
                bx = poly_x - (k + frac) * slot_w
                if bx < -6.8:
                    continue
                blk = make_block(0.86, 0.68, GOLD, base, TEXT, size=26, fill_opacity=0.28).move_to([bx, y_cpy, 0])
                g.add(blk)
            g.layout_ok = "edge"
            return g

        gold_copy = always_redraw(_build_copy)

        tpl_label = T("blue template", size=28, color=BLUE).move_to([-4.3, 2.05, 0])
        poly_label = T("polymerase (1 base)", size=28, color=TEXT).move_to([poly_x, 1.85, 0])
        copy_label = T("gold copy", size=28, color=GOLD).move_to([-4.3, -1.75, 0])
        read_label = T("ordered read", size=28, color=GOLD).move_to([3.2, -1.75, 0])
        tag = scope_tag("schematic")

        # Scroll cleanly at ~1.25 bases/s and pulse the active base slot inside polymerase
        sweep = always_redraw(
            lambda: Rectangle(
                width=1.6, height=0.82, stroke_width=0, fill_color=TEAL, fill_opacity=0.22,
            ).move_to([-9.0 + ((step_t.get_value() * 1.9) % 18.0), y_tpl, 0])
        )
        sweep.set_z_index(-1)
        self.add(sweep, tpl_ribbon, active_hl, poly, tag)
        self.play(
            FadeIn(tpl_label), FadeIn(poly_label),
            step_t.animate(rate_func=linear).set_value(2.2),
            run_time=1.8,
        )
        self.play(step_t.animate(rate_func=linear).set_value(7.0), run_time=3.9)

        self.at("Watch one")
        self.play(step_t.animate(rate_func=linear).set_value(10.8), run_time=3.1)

        self.at("gold copy")
        self.add(gold_copy)
        self.play(FadeIn(copy_label), step_t.animate(rate_func=linear).set_value(14.3), run_time=2.8)

        self.at("never sees")
        self.play(step_t.animate(rate_func=linear).set_value(18.8), run_time=3.6)

        self.at("turn local")
        self.play(FadeIn(read_label), step_t.animate(rate_func=linear).set_value(22.5), run_time=3.0)

        rem = max(0.2, self.narration_s - self.elapsed())
        self.play(step_t.animate(rate_func=linear).set_value(22.5 + 1.2 * rem), run_time=rem)
        self.finish()


# ------------------------------------------------------------------ S02Title
class S02Title(NarratedScene):
    def construct(self):
        step_t = ValueTracker(23.8)
        slot_w = 1.05
        y_tpl = -1.05
        y_cpy = -2.10
        poly_x = -0.525

        def _build_tpl():
            s = step_t.get_value()
            frac = s - int(s)
            base_idx = int(s)
            m = make_template_strip(
                n_slots=20, slot_w=slot_w, height=0.72, y=y_tpl,
                seq=TEMPLATE_60, start_idx=base_idx,
            ).shift(LEFT * (frac * slot_w))
            m.set_opacity(0.42)
            return m

        def _build_copy():
            s = step_t.get_value()
            n_full = int(s) + 1
            frac = s - int(s)
            g = VGroup()
            for k in range(8):
                seq_idx = n_full - 1 - k
                base = COMPLEMENT[TEMPLATE_60[(seq_idx + 9) % len(TEMPLATE_60)]]
                bx = poly_x - (k + frac) * slot_w
                if bx < -6.8:
                    continue
                blk = make_block(0.86, 0.62, GOLD, base, TEXT, size=24, fill_opacity=0.18).move_to([bx, y_cpy, 0])
                blk.set_opacity(0.45)
                g.add(blk)
            g.layout_ok = "edge"
            return g

        tpl = always_redraw(_build_tpl)
        cpy = always_redraw(_build_copy)
        poly = make_polymerase_clamp(x=poly_x, y_top=-0.55, y_bot=-2.58, width=1.18)
        poly[0].set_fill(opacity=0.04)
        poly[1].set_stroke(opacity=0.45)
        poly[2].set_stroke(opacity=0.45)
        self.add(tpl, cpy, poly)

        title = T("How Chemistry Becomes a Read", size=50, font=TITLE_FONT, color=TEXT).move_to([0, 1.45, 0])
        fit(title, max_w=11.5)
        rule = Line(LEFT * 2.2, RIGHT * 2.2, color=GOLD, stroke_width=4).next_to(title, DOWN, buff=0.25)

        self.play(
            FadeIn(title, shift=UP * 0.1), GrowFromCenter(rule),
            step_t.animate(rate_func=linear).set_value(24.3),
            run_time=0.35,
        )
        self.play(step_t.animate(rate_func=linear).set_value(25.9), run_time=1.3)
        self.play(
            FadeOut(title), FadeOut(rule),
            step_t.animate(rate_func=linear).set_value(26.4),
            run_time=0.35,
        )
        self.finish()


# ------------------------------------------------------------------ S03Sanger
class S03Sanger(SpokenScene):
    def construct(self):
        lane_ys = [2.15, 0.90, -0.35, -1.60]
        primer_w = 1.45
        slot_w = 1.05
        stop_w = 1.24
        gap = 0.12

        single_lane = RoundedRectangle(
            corner_radius=0.12, width=11.0, height=0.48,
            stroke_color=BLUE, stroke_width=3.0, fill_color=BLUE, fill_opacity=0.20,
        ).move_to([0.65, 0.3, 0])

        lanes = VGroup(*[
            RoundedRectangle(
                corner_radius=0.10, width=11.0, height=0.42,
                stroke_color=BLUE, stroke_width=2.5, fill_color=BLUE, fill_opacity=0.16,
            ).move_to([0.65, ly + 0.36, 0])
            for ly in lane_ys
        ])
        lane_labels = VGroup(*[
            T(f"copy {i + 1}", size=24, color=BLUE).next_to(lanes[i], LEFT, buff=0.18)
            for i in range(4)
        ])
        x_left = lanes[0].get_left()[0] + 0.25

        primers = VGroup(*[
            make_block(primer_w, 0.56, TEXT, "primer", TEXT, size=24, fill_opacity=0.14).move_to(
                [x_left + primer_w / 2, ly - 0.18, 0]
            )
            for ly in lane_ys
        ])
        tag = scope_tag("schematic")
        head = T("Sanger chain termination", size=32, color=TEXT).move_to([0, 3.35, 0])

        def block_pos(i, k, w=slot_w):
            # k = 1..4 position index
            x0 = x_left + primer_w + gap + (k - 1) * (slot_w + gap)
            return [x0 + w / 2, lane_ys[i] - 0.18, 0]

        self.add(single_lane, tag)
        self.at("makes many copies")
        self.play(
            ReplacementTransform(VGroup(single_lane), lanes),
            FadeIn(head),
            run_time=1.35,
        )
        self.at("starting primer")
        self.play(FadeIn(primers, shift=RIGHT * 0.2), FadeIn(lane_labels), run_time=1.35)

        # Brief primer highlight before "ordinary nucleotides" at 6.32s
        primer_hl = VGroup(*[SurroundingRectangle(p, color=GOLD, stroke_width=2.5, buff=0.05) for p in primers])
        self.play(Create(primer_hl), run_time=0.5)
        self.play(FadeOut(primer_hl), run_time=0.5)

        # Step 1: ordinary gold nucleotides join all 4 copies horizontally (zero straddle over blue lanes)
        self.at("ordinary nucleotides")
        step1_blocks = VGroup(*[
            make_block(slot_w, 0.56, GOLD, SANGER_NEW[0], TEXT, size=26).move_to(block_pos(i, 1))
            for i in range(4)
        ])
        self.play(LaggedStart(*[FadeIn(b, shift=LEFT * 0.28) for b in step1_blocks], lag_ratio=0.14), run_time=1.5)

        # Keep growing: position 2 adds ordinary gold blocks cleanly
        self.at("keep growing")
        step2_gold = VGroup(*[
            make_block(slot_w, 0.56, GOLD, SANGER_NEW[1], TEXT, size=26).move_to(block_pos(i, 2))
            for i in (0, 2, 3)
        ])
        self.play(LaggedStart(*[FadeIn(b, shift=LEFT * 0.28) for b in step2_gold], lag_ratio=0.18), run_time=1.7)

        # Beat: Occasionally, a red dideoxynucleotide joins the copy (lane 1 stops at pos 2)
        self.at("red dideoxynucleotide")
        stop_lane1 = make_block(stop_w, 0.56, RED, "ddNTP", TEXT, size=24, fill_opacity=0.34).move_to(block_pos(1, 2, w=stop_w))
        stop_ring1 = SurroundingRectangle(stop_lane1, color=RED, stroke_width=4, buff=0.06)
        self.play(FadeIn(stop_lane1, shift=LEFT * 1.6), Create(stop_ring1), run_time=1.3)
        # While lane 1 stops, remaining lanes keep visibly extending horizontally
        s0_g3 = make_block(slot_w, 0.56, GOLD, SANGER_NEW[2], TEXT, size=26).move_to(block_pos(0, 3))
        s2_g3 = make_block(slot_w, 0.56, GOLD, SANGER_NEW[2], TEXT, size=26).move_to(block_pos(2, 3))
        self.play(
            FadeOut(stop_ring1),
            FadeIn(s0_g3, shift=LEFT * 1.4),
            FadeIn(s2_g3, shift=LEFT * 1.4),
            run_time=1.4,
        )

        # Beat: It lacks the usable end needed for another addition
        self.at("lacks the usable")
        blocked_bar = Line(
            stop_lane1.get_corner(UR) + RIGHT * 0.08,
            stop_lane1.get_corner(DR) + RIGHT * 0.08,
            color=RED, stroke_width=7,
        )
        incoming = make_block(slot_w, 0.56, GOLD, SANGER_NEW[2], TEXT, size=26).move_to(
            [4.2, lane_ys[1] - 0.18, 0]
        )
        x_center = blocked_bar.get_center() + RIGHT * 0.42
        block_x = VGroup(
            Line(x_center + UL * 0.16, x_center + DR * 0.16, color=RED, stroke_width=5),
            Line(x_center + UR * 0.16, x_center + DL * 0.16, color=RED, stroke_width=5),
        )
        self.play(Create(blocked_bar), FadeIn(incoming, shift=LEFT * 1.0), run_time=0.75)
        self.play(incoming.animate.move_to([blocked_bar.get_center()[0] + 0.72, lane_ys[1] - 0.18, 0]), run_time=0.65)
        self.play(Create(block_x), stop_lane1[0].animate.set_stroke(GOLD, width=4.5), run_time=0.45)
        self.play(
            FadeOut(incoming, shift=RIGHT * 2.2),
            FadeOut(block_x),
            stop_lane1[0].animate.set_stroke(RED, width=2.5),
            run_time=0.75,
        )

        # Beat: That copy stops permanently, while other copies continue until other stop positions
        self.at("stops permanently")
        blocked_tag = T("no usable end", size=26, color=RED).next_to(blocked_bar, RIGHT, buff=0.22)
        halted_chip = T("stopped", size=26, color=RED).next_to(blocked_bar, RIGHT, buff=0.22)
        lane1_row_hl = SurroundingRectangle(
            VGroup(primers[1], step1_blocks[1], stop_lane1),
            color=RED, stroke_width=3.5, fill_color=RED, fill_opacity=0.08, buff=0.06,
        )
        s2_g4 = make_block(slot_w, 0.56, GOLD, SANGER_NEW[3], TEXT, size=26).move_to(block_pos(2, 4))
        s0_g3_hl = SurroundingRectangle(s2_g4, color=GOLD, stroke_width=3.5, buff=0.05)
        self.play(FadeIn(blocked_tag), FadeIn(lane1_row_hl), FadeIn(s2_g4, shift=LEFT * 1.4), Create(s0_g3_hl), run_time=0.95)
        self.play(swap(blocked_tag, halted_chip, run_time=0.55), FadeOut(s0_g3_hl), run_time=0.65)
        self.play(stop_lane1[0].animate.set_stroke(GOLD, width=4.5), run_time=0.35)
        self.play(stop_lane1[0].animate.set_stroke(RED, width=2.5), run_time=0.35)

        self.at("other positions")
        s3_stop = make_block(stop_w, 0.56, RED, "ddNTP", TEXT, size=24, fill_opacity=0.34).move_to(block_pos(3, 3, w=stop_w))
        s0_stop = make_block(stop_w, 0.56, RED, "ddNTP", TEXT, size=24, fill_opacity=0.34).move_to(block_pos(0, 4, w=stop_w))
        s2_stop = make_block(stop_w, 0.56, RED, "ddNTP", TEXT, size=24, fill_opacity=0.34).move_to(block_pos(2, 5, w=stop_w))
        for st in (s3_stop, s0_stop, s2_stop):
            st_ring = SurroundingRectangle(st, color=RED, stroke_width=4.0, buff=0.06)
            self.play(FadeIn(st, shift=LEFT * 1.8), Create(st_ring), run_time=0.55)
            self.play(FadeOut(st_ring), run_time=0.20)
        self.finish()


# ------------------------------------------------------------------ S04Ladder
class S04Ladder(SpokenScene):
    def construct(self):
        lane_ys = [2.15, 0.90, -0.35, -1.60]
        x_left = -5.95
        primer_w = 1.25
        slot_w = 0.86
        stop_w = 1.22
        gap = 0.08

        def make_stopped_copy(n_gold, y, end_label="ddNTP"):
            g = VGroup()
            p = make_block(primer_w, 0.58, TEXT, "primer", TEXT, size=24, fill_opacity=0.14).move_to(
                [x_left + primer_w / 2, y, 0]
            )
            g.add(p)
            prev = p
            for k in range(n_gold):
                blk = make_block(slot_w, 0.58, GOLD, SANGER_NEW[k], TEXT, size=26).next_to(prev, RIGHT, buff=gap)
                g.add(blk)
                prev = blk
            stop = make_block(stop_w, 0.58, RED, end_label, TEXT, size=24, fill_opacity=0.40).next_to(prev, RIGHT, buff=gap)
            g.add(stop)
            g.stop = stop
            return g

        copies = [make_stopped_copy(ng, ly) for ng, ly in zip([3, 1, 4, 2], lane_ys)]
        head = T("Length ladder", size=32, color=TEXT).move_to([-2.6, 3.3, 0])
        tag = scope_tag("schematic")
        self.add(*copies, head, tag)

        # Beat 1: sort from shortest (bottom) to longest (top) smoothly
        sorted_ys = [-1.75, -0.55, 0.65, 1.85]
        order = [copies[1], copies[3], copies[0], copies[2]]
        self.at("now sort")
        self.play(
            *[c.animate.set_y(sy) for c, sy in zip(order, sorted_ys)],
            run_time=2.2,
        )

        # Beat 2: Each red endpoint carries the identity of its last base (fade old label out first to prevent overlap)
        self.at("red endpoint")
        end_tiles = []
        for idx, c in enumerate(order):
            base = SANGER_NEW[idx]
            nt = make_block(0.88, 0.58, RED, base, TEXT, size=28, fill_opacity=0.36).move_to(c.stop.get_left() + RIGHT * 0.44)
            end_tiles.append(nt)
        for c, nt in zip(order, end_tiles):
            ring = SurroundingRectangle(c.stop, color=GOLD, stroke_width=3.5, buff=0.05)
            self.play(
                FadeOut(c.stop[1], run_time=0.22),
                Create(ring, run_time=0.30),
                run_time=0.40,
            )
            self.play(
                ReplacementTransform(c.stop[0], nt[0]),
                FadeIn(nt[1]),
                FadeOut(ring),
                run_time=0.60,
            )

        # Beat 3: Reading those endpoints in length order spells the newly made strand
        self.at("length order")
        read_col_x = 2.35
        new_head = T("new strand", size=28, color=GOLD).move_to([read_col_x, 3.05, 0])
        gold_tiles = [
            make_block(0.95, 0.62, GOLD, SANGER_NEW[idx], TEXT, size=28, fill_opacity=0.32).move_to(
                [read_col_x, sorted_ys[idx], 0]
            )
            for idx in range(4)
        ]
        arrow_up = Arrow([1.45, -2.1, 0], [1.45, 2.2, 0], color=GOLD, stroke_width=4, buff=0)
        new_5 = T("5'", size=24, color=GOLD).next_to(arrow_up.get_start(), DOWN, buff=0.12)
        new_3 = T("3'", size=24, color=GOLD).next_to(arrow_up.get_end(), UP, buff=0.12)
        self.play(FadeIn(new_head), GrowArrow(arrow_up), FadeIn(new_5), FadeIn(new_3), run_time=0.75)

        for idx in range(4):
            flash_ring = SurroundingRectangle(end_tiles[idx], color=GOLD, stroke_width=5, buff=0.06)
            fly_box = end_tiles[idx][0].copy()
            self.play(Create(flash_ring), run_time=0.22)
            self.play(
                ReplacementTransform(fly_box, gold_tiles[idx][0]),
                FadeIn(gold_tiles[idx][1]),
                FadeOut(flash_ring),
                run_time=0.52,
            )

        # Beat 4: Template runs in the opposite direction with explicit base-pair bridges
        self.at("template runs")
        tpl_col_x = 4.55
        tpl_head = T("template", size=28, color=BLUE).move_to([tpl_col_x, 3.05, 0])
        tpl_tiles = [
            make_block(0.95, 0.62, BLUE, COMPLEMENT[SANGER_NEW[idx]], TEXT, size=28, fill_opacity=0.28).move_to(
                [tpl_col_x, sorted_ys[idx], 0]
            )
            for idx in range(4)
        ]
        pair_links = VGroup(*[
            DashedLine([read_col_x + 0.52, sorted_ys[idx], 0], [tpl_col_x - 0.52, sorted_ys[idx], 0], color=GREY, stroke_width=2.5)
            for idx in range(4)
        ])
        tpl_arrow = Arrow([5.55, -2.1, 0], [5.55, 2.2, 0], color=BLUE, stroke_width=4, buff=0)
        self.play(
            FadeIn(tpl_head),
            LaggedStart(*[FadeIn(t, shift=LEFT * 0.25) for t in tpl_tiles], lag_ratio=0.1),
            Create(pair_links),
            GrowArrow(tpl_arrow),
            run_time=0.95,
        )

        self.at("opposite direction")
        tpl_arrow_down = Arrow([5.55, 2.2, 0], [5.55, -2.1, 0], color=BLUE, stroke_width=4, buff=0)
        tpl_5 = T("5'", size=24, color=BLUE).next_to(tpl_arrow_down.get_start(), UP, buff=0.12)
        tpl_3 = T("3'", size=24, color=BLUE).next_to(tpl_arrow_down.get_end(), DOWN, buff=0.12)
        self.play(ReplacementTransform(tpl_arrow, tpl_arrow_down), FadeIn(tpl_5), FadeIn(tpl_3), run_time=1.2)

        self.at("reversing the complement")
        rev_tag = T("reverse complement", size=26, color=BLUE).move_to([3.5, -2.95, 0])
        self.play(FadeIn(rev_tag), run_time=0.55)
        for idx in (3, 2, 1, 0):
            hl = SurroundingRectangle(VGroup(gold_tiles[idx], tpl_tiles[idx]), color=GOLD, stroke_width=3.5, buff=0.06)
            self.play(Create(hl), tpl_tiles[idx][0].animate.set_fill(BLUE, opacity=0.62), run_time=0.35)
            self.play(FadeOut(hl), tpl_tiles[idx][0].animate.set_fill(BLUE, opacity=0.28), run_time=0.30)

        self.finish()


# ------------------------------------------------------------------ S05Predict
class S05Predict(SpokenScene):
    def construct(self):
        y_shift = 0.25
        y_tpl = 0.65 + y_shift
        y_cpy = -0.45 + y_shift
        step_w = 1.05
        slot_x = lambda i: -20 * step_w / 2 + (i + 0.5) * step_w

        # Exact base-pair alignment beneath template slots 8, 9, 10
        tpl = make_template_strip(n_slots=20, slot_w=step_w, height=0.76, y=y_tpl)
        primer = make_block(1.30, 0.66, TEXT, "primer", TEXT, size=24, fill_opacity=0.15).move_to([slot_x(7) - 0.16, y_cpy, 0])
        b1 = make_block(0.88, 0.66, GOLD, COMPLEMENT[TEMPLATE_60[8]], TEXT, size=26).move_to([slot_x(8), y_cpy, 0])
        b2 = make_block(0.88, 0.66, GOLD, COMPLEMENT[TEMPLATE_60[9]], TEXT, size=26).move_to([slot_x(9), y_cpy, 0])
        b3 = make_block(0.88, 0.66, GOLD, COMPLEMENT[TEMPLATE_60[10]], TEXT, size=26).move_to([slot_x(10), y_cpy, 0])
        red_stop = make_block(1.22, 0.66, RED, "stop", TEXT, size=24, fill_opacity=0.35).move_to([slot_x(11) + 0.04, y_cpy, 0])
        teal_pause = make_block(1.22, 0.66, TEAL, "pause", TEXT, size=24, fill_opacity=0.35).move_to([slot_x(11) + 0.04, y_cpy, 0])

        poly = make_polymerase_clamp(x=slot_x(9), y_top=y_tpl + 0.55, y_bot=y_cpy - 0.55, width=1.12)
        tpl_lab = T("template", size=26, color=BLUE).move_to([-4.9, y_tpl + 0.72, 0])
        cpy_lab = T("copy", size=26, color=GOLD).move_to([-4.9, y_cpy - 0.72, 0])
        red_lab = T("permanent stop", size=26, color=RED).next_to(red_stop, DOWN, buff=0.38)
        teal_lab = T("removable pause", size=26, color=TEAL).next_to(teal_pause, DOWN, buff=0.38)
        tag = scope_tag("schematic").move_to([5.4, 3.3, 0])

        # Polymerase advances to the red stop during opening beat so the halt is visibly earned
        self.add(tpl, primer, b1, b2, poly, tpl_lab, cpy_lab, tag)
        self.play(
            poly.animate.move_to([slot_x(10), (y_tpl + y_cpy) / 2, 0]),
            FadeIn(b3, shift=LEFT * 0.25),
            run_time=1.1,
        )
        self.play(
            poly.animate.move_to([slot_x(11) + 0.04, (y_tpl + y_cpy) / 2, 0]),
            FadeIn(red_stop, shift=LEFT * 0.3),
            FadeIn(red_lab),
            run_time=1.2,
        )

        self.at("removable teal pause")
        self.play(FadeOut(red_stop[1], run_time=0.22), FadeOut(red_lab, run_time=0.25), run_time=0.3)
        self.play(
            ReplacementTransform(red_stop[0], teal_pause[0]),
            FadeIn(teal_pause[1]),
            FadeIn(teal_lab),
            run_time=0.9,
        )

        self.at("What must happen")
        cam = make_camera_icon(GREEN).move_to([teal_pause.get_center()[0], y_tpl + 1.35, 0])
        cam_lab = T("camera", size=26, color=GREEN).next_to(cam, UP, buff=0.14)
        q_mark = T("?", size=56, color=GREY, weight=BOLD).next_to(teal_pause, RIGHT, buff=0.50)
        next_slot = DashedVMobject(
            RoundedRectangle(corner_radius=0.12, width=0.88, height=0.66, stroke_color=GREY, stroke_width=2.5),
            num_dashes=14,
        ).move_to([slot_x(13), y_cpy, 0])
        qcard = question_card(
            "What must happen before polymerase can copy the next base?",
            y=-2.85, max_w=10.6,
        )
        cam_beam = Polygon(
            cam.get_bottom() + LEFT * 0.22,
            cam.get_bottom() + RIGHT * 0.22,
            [teal_pause.get_right()[0], y_tpl + 0.44, 0],
            [teal_pause.get_left()[0], y_tpl + 0.44, 0],
            color=GREEN, stroke_width=2, fill_color=GREEN, fill_opacity=0.26,
        )
        cand_tile = DashedVMobject(
            RoundedRectangle(corner_radius=0.12, width=0.88, height=0.66, stroke_color=GOLD, stroke_width=3.0),
            num_dashes=14,
        ).move_to([5.85, y_cpy, 0])
        self.play(
            FadeOut(poly),
            FadeIn(cam), FadeIn(cam_lab), FadeIn(q_mark), Create(next_slot), Create(cand_tile), FadeIn(qcard),
            run_time=1.3,
        )
        self.play(
            FadeIn(cam_beam), cam.iris.animate.scale(1.35),
            cand_tile.animate.set_x(4.70), next_slot.animate.set_stroke(GOLD, width=4.0),
            teal_pause[0].animate.set_stroke(TEAL, width=5.5),
            run_time=0.85,
        )
        rem = max(0.2, self.narration_s - self.elapsed())
        self.play(
            FadeOut(cam_beam), cam.iris.animate.scale(1 / 1.35),
            cand_tile.animate.set_x(5.85), next_slot.animate.set_stroke(GREY, width=2.5),
            teal_pause[0].animate.set_stroke(TEAL, width=3.0),
            run_time=rem,
        )
        self.finish()


# ------------------------------------------------------------------ S06Pause
class S06Pause(PredictPause):
    QUESTION = "What must happen before polymerase can copy the next base?"
    CARD = {"y": -2.85, "max_w": 10.6}
    SECONDS = 4.5

    def backdrop(self):
        pic = build_predict_picture(y_shift=0.25)
        tag = scope_tag("schematic").move_to([5.4, 3.3, 0])
        y_tpl = 0.90
        y_cpy = -0.20
        pulse(pic.pause_blk[0], base=3.2, amp=2.8, speed=3.8)
        bob(pic.q_mark, amp=0.10, speed=3.2)

        cam_beam = Polygon(
            pic.cam.get_bottom() + LEFT * 0.22,
            pic.cam.get_bottom() + RIGHT * 0.22,
            [pic.pause_blk.get_right()[0], y_tpl + 0.44, 0],
            [pic.pause_blk.get_left()[0], y_tpl + 0.44, 0],
            color=GREEN, stroke_width=2.5, fill_color=GREEN, fill_opacity=0.22,
        )
        cam_beam._t = 0.0
        def _beam_upd(mob, dt):
            mob._t += dt
            op = 0.05 + 0.30 * (0.5 + 0.5 * np.sin(3.6 * mob._t))
            mob.set_fill(opacity=op)
            mob.set_stroke(opacity=0.25 + op)
        cam_beam.add_updater(_beam_upd)

        cand_tile = DashedVMobject(
            RoundedRectangle(corner_radius=0.12, width=0.88, height=0.66, stroke_color=GOLD, stroke_width=3.5),
            num_dashes=14,
        ).move_to([5.25, y_cpy, 0])
        cand_tile._t = 0.0
        def _cand_upd(mob, dt):
            mob._t += dt
            mob.set_x(5.25 + 0.60 * np.cos(3.0 * mob._t))
        cand_tile.add_updater(_cand_upd)

        pic.next_slot._t = 0.0
        _c_grey = ManimColor(GREY)
        _c_gold = ManimColor(GOLD)
        def _slot_upd(mob, dt):
            mob._t += dt
            s = 0.5 + 0.5 * np.sin(3.0 * mob._t)
            mob.set_stroke(interpolate_color(_c_grey, _c_gold, s), width=2.5 + 2.5 * s)
        pic.next_slot.add_updater(_slot_upd)

        pic.cam._ap_t = 0.0
        def _ap(mob, dt):
            mob._ap_t += dt
            s = 1.0 + 0.38 * np.sin(3.6 * mob._ap_t)
            mob.iris.set_width(0.20 * s)
        pic.cam.add_updater(_ap)

        return VGroup(pic, cam_beam, cand_tile, tag)


# ------------------------------------------------------------------ S07Cycles
class S07Cycles(SpokenScene):
    def construct(self):
        n_strands = 6
        ys = np.linspace(2.05, -1.75, n_strands)
        x0 = -6.05
        primer_w = 1.24
        slot_w = 0.72
        gap = 0.08

        primers = VGroup(*[
            make_block(primer_w, 0.48, TEXT, "primer", TEXT, size=24, fill_opacity=0.14).move_to([x0 + primer_w / 2, y, 0])
            for y in ys
        ])
        cluster_label = T("cluster of identical copies", size=28, color=GOLD).move_to([-2.7, 3.1, 0])
        tag = scope_tag("schematic")

        def col_x(c):
            return x0 + primer_w + gap + (c + 0.5) * (slot_w + gap)

        col0 = VGroup(*[make_block(slot_w, 0.48, GOLD, CYCLE_BASES[0], TEXT, size=24).move_to([col_x(0), y, 0]) for y in ys])
        col1_pause = VGroup(*[make_block(slot_w, 0.48, TEAL, CYCLE_BASES[1], TEXT, size=24, fill_opacity=0.38).move_to([col_x(1), y, 0]) for y in ys])

        # Three-state ring on the right with clear spacing between ring dots and labels
        ring_c = np.array([3.85, 0.45, 0.0])
        ring_r = 1.42
        ring_circle = Circle(radius=ring_r, stroke_color=GREY, stroke_width=5).move_to(ring_c)
        angles = {"add": PI / 2, "image": -PI / 6, "reset": -5 * PI / 6}
        label_offsets = {
            "add": UP * 0.52,
            "image": np.array([0.85, -0.35, 0.0]),
            "reset": np.array([-0.85, -0.35, 0.0]),
        }
        state_nodes = {}
        state_labs = {}
        state_colors = {"add": GOLD, "image": GREEN, "reset": TEAL}
        for name, ang in angles.items():
            pos = ring_c + ring_r * np.array([np.cos(ang), np.sin(ang), 0.0])
            dot = Dot(pos, radius=0.17, color=state_colors[name])
            lab = T(name, size=28, color=state_colors[name]).move_to(pos + label_offsets[name])
            state_nodes[name] = dot
            state_labs[name] = lab

        pointer_angle = ValueTracker(angles["image"])
        pointer = always_redraw(lambda: Dot(
            ring_c + ring_r * np.array([np.cos(pointer_angle.get_value()), np.sin(pointer_angle.get_value()), 0.0]),
            radius=0.23, color=TEXT, stroke_color=GOLD, stroke_width=3,
        ))

        read_head = T("reported read:", size=26, color=GREEN).move_to([1.25, -2.95, 0])

        # Start with single copy and quickly fan into 6-strand cluster cleanly before "images the" at 0.8s
        self.add(primers[2], col0[2], col1_pause[2], tag)
        self.play(
            LaggedStart(*[FadeIn(primers[i]) for i in (0, 1, 3, 4, 5)], lag_ratio=0.04),
            LaggedStart(*[FadeIn(col0[i]) for i in (0, 1, 3, 4, 5)], lag_ratio=0.04),
            LaggedStart(*[FadeIn(col1_pause[i]) for i in (0, 1, 3, 4, 5)], lag_ratio=0.04),
            FadeIn(cluster_label),
            Create(ring_circle),
            *[FadeIn(m) for m in state_nodes.values()],
            *[FadeIn(m) for m in state_labs.values()],
            FadeIn(pointer), FadeIn(read_head),
            run_time=0.40,
        )

        # Beat 2: The machine images the colour while every copy in a cluster is paused (0.6s..5.5s)
        self.at("images the")
        scan_box = SurroundingRectangle(col1_pause, color=GREEN, stroke_width=5, fill_color=GREEN, fill_opacity=0.14, buff=0.08)
        call1 = make_block(0.68, 0.52, GREEN, CYCLE_BASES[1], TEXT, size=26, fill_opacity=0.35).move_to([3.05, -2.95, 0])
        self.play(Create(scan_box), run_time=1.2)
        self.play(col1_pause.animate.set_stroke(GREEN, width=4), run_time=1.0)
        self.play(FadeIn(call1, shift=DOWN * 0.25), run_time=1.2)
        self.play(FadeOut(scan_box), col1_pause.animate.set_stroke(TEAL, width=3), run_time=1.0)

        # Beat 3: Then it removes both the dye and the block
        self.at("removes both")
        self.play(pointer_angle.animate.set_value(angles["reset"]), run_time=0.9)
        col1_free = VGroup(*[make_block(slot_w, 0.48, GOLD, CYCLE_BASES[1], TEXT, size=24).move_to([col_x(1), y, 0]) for y in ys])
        caps = VGroup(*[
            RoundedRectangle(corner_radius=0.06, width=0.22, height=0.48, stroke_color=TEAL, stroke_width=2.5, fill_color=TEAL, fill_opacity=0.5).move_to(
                [col_x(1) + slot_w / 2 + 0.08, y, 0]
            )
            for y in ys
        ])
        self.play(ReplacementTransform(col1_pause, col1_free), FadeIn(caps), run_time=0.6)
        self.play(caps.animate.shift(UP * 0.5).set_opacity(0), run_time=1.2)
        self.remove(caps)

        # Beat 4: The free end can accept another nucleotide
        self.at("free end")
        free_note = T("free end", size=26, color=GOLD).move_to([col_x(2) + 0.35, 2.55, 0])
        self.play(pointer_angle.animate.set_value(angles["add"]), FadeIn(free_note), run_time=1.0)
        col2_pause = VGroup(*[make_block(slot_w, 0.48, TEAL, CYCLE_BASES[2], TEXT, size=24, fill_opacity=0.38).move_to([col_x(2), y, 0]) for y in ys])
        self.play(FadeIn(col2_pause, shift=LEFT * 0.35), run_time=1.3)
        self.play(FadeOut(free_note), run_time=0.4)

        # Beat 5: Repeating this add, image, and reset cycle
        self.at("Repeating this")
        self.play(pointer_angle.animate.set_value(angles["image"]), run_time=0.75)
        scan2 = SurroundingRectangle(col2_pause, color=GREEN, stroke_width=5, fill_color=GREEN, fill_opacity=0.14, buff=0.08)
        call2 = make_block(0.68, 0.52, GREEN, CYCLE_BASES[2], TEXT, size=26, fill_opacity=0.35).next_to(call1, RIGHT, buff=0.12)
        self.play(Create(scan2), run_time=0.55)
        self.play(FadeIn(call2, shift=DOWN * 0.2), FadeOut(scan2), run_time=0.75)

        self.play(pointer_angle.animate.set_value(angles["reset"]), run_time=0.75)
        col2_free = VGroup(*[make_block(slot_w, 0.48, GOLD, CYCLE_BASES[2], TEXT, size=24).move_to([col_x(2), y, 0]) for y in ys])
        self.play(ReplacementTransform(col2_pause, col2_free), run_time=0.5)
        self.play(pointer_angle.animate.set_value(angles["add"] - TAU), run_time=0.8)
        col3_pause = VGroup(*[make_block(slot_w, 0.48, TEAL, CYCLE_BASES[0], TEXT, size=24, fill_opacity=0.38).move_to([col_x(3), y, 0]) for y in ys])
        self.play(FadeIn(col3_pause, shift=LEFT * 0.3), run_time=0.7)

        self.play(pointer_angle.animate.set_value(angles["image"] - TAU), run_time=0.7)
        scan3 = SurroundingRectangle(col3_pause, color=GREEN, stroke_width=5, fill_color=GREEN, fill_opacity=0.14, buff=0.08)
        call3 = make_block(0.68, 0.52, GREEN, CYCLE_BASES[0], TEXT, size=26, fill_opacity=0.35).next_to(call2, RIGHT, buff=0.12)
        self.play(Create(scan3), run_time=0.5)
        self.play(FadeIn(call3, shift=DOWN * 0.2), FadeOut(scan3), run_time=0.65)
        self.finish()


# ------------------------------------------------------------------ S08Compare
class S08Compare(SpokenScene):
    def construct(self):
        tp = TwoPanel(
            "Sanger: permanent ladder",
            "Short-read: cyclic pauses",
            colors=(RED, TEAL),
            top=3.15, bottom=-2.55, gap=0.42, width=12.6, size=30,
        )
        tag = scope_tag("schematic")

        lx_c, lw, lh = tp.area("left")
        bar_x0 = lx_c[0] - 2.3
        unsorted_ys = [1.4, 0.5, -0.4, -1.3]
        lens = [3.0, 1.3, 4.0, 2.2]
        sanger_bars = []
        for l_len, uy in zip(lens, unsorted_ys):
            g_bar = Rectangle(width=l_len, height=0.42, stroke_color=GOLD, stroke_width=2.5, fill_color=GOLD, fill_opacity=0.28)
            g_bar.move_to([bar_x0 + l_len / 2, uy, 0])
            r_cap = Rectangle(width=0.45, height=0.42, stroke_color=RED, stroke_width=2.5, fill_color=RED, fill_opacity=0.5).next_to(g_bar, RIGHT, buff=0.04)
            sanger_bars.append(VGroup(g_bar, r_cap))

        rx_c, rw, rh = tp.area("right")
        cluster_strands = VGroup(*[
            Rectangle(width=2.1, height=0.26, stroke_color=GOLD, stroke_width=2.0, fill_color=GOLD, fill_opacity=0.28).move_to(
                [rx_c[0] - 0.35, 1.35 - i * 0.46, 0]
            )
            for i in range(5)
        ])
        cluster_tips = VGroup(*[
            Rectangle(width=0.35, height=0.26, stroke_color=TEAL, stroke_width=2.0, fill_color=TEAL, fill_opacity=0.48).next_to(s, RIGHT, buff=0.04)
            for s in cluster_strands
        ])

        # Start with everything visible inside both panels and animate both sides immediately
        self.add(tp, tag, cluster_strands, cluster_tips)
        self.play(
            LaggedStart(*[FadeIn(b, shift=RIGHT * 1.1) for b in sanger_bars], lag_ratio=0.18),
            run_time=1.8,
        )
        self.play(cluster_tips.animate.set_fill(GREEN, opacity=0.80), run_time=0.75)
        self.play(cluster_tips.animate.set_fill(TEAL, opacity=0.48), run_time=0.75)

        # Beat: Sanger reads a permanent ladder of fragment lengths
        self.at("permanent ladder")
        sorted_ys = [-1.3, -0.4, 0.5, 1.4]
        sorted_bars = [sanger_bars[1], sanger_bars[3], sanger_bars[0], sanger_bars[2]]
        left_note = T("sorts once", size=26, color=RED).move_to([lx_c[0], -2.05, 0])
        self.play(
            *[b.animate.set_y(sy) for b, sy in zip(sorted_bars, sorted_ys)],
            FadeIn(left_note),
            run_time=1.65,
        )
        # Sweep a single read-out flash up the sorted red caps
        for b in sorted_bars:
            self.play(b[1].animate.set_fill(RED, opacity=0.95).scale(1.12), run_time=0.20)
            self.play(b[1].animate.set_fill(RED, opacity=0.50).scale(1 / 1.12), run_time=0.14)
        # Keep right cluster pulsing gently until "temporary pauses" cue
        self.play(cluster_tips.animate.set_fill(GREEN, opacity=0.75), run_time=0.40)
        self.play(cluster_tips.animate.set_fill(TEAL, opacity=0.48), run_time=0.35)

        # Beat: Short-read sequencing follows temporary pauses through repeated cycles
        self.at("temporary pauses")
        right_note = T("cycles: add, image, reset", size=26, color=TEAL).move_to([rx_c[0], -2.05, 0])
        self.play(FadeIn(right_note), run_time=0.35)
        for _ in range(2):
            scan_col = SurroundingRectangle(cluster_tips, color=GREEN, stroke_width=3.5, fill_color=GREEN, fill_opacity=0.14, buff=0.06)
            self.play(Create(scan_col), cluster_tips.animate.set_fill(GREEN, opacity=0.85), run_time=0.35)
            new_seg = VGroup(*[
                Rectangle(width=0.24, height=0.26, stroke_color=GOLD, stroke_width=2.0, fill_color=GOLD, fill_opacity=0.35).move_to(t)
                for t in cluster_tips
            ])
            self.play(
                FadeOut(scan_col),
                cluster_tips.animate.shift(RIGHT * 0.28).set_fill(TEAL, opacity=0.48),
                FadeIn(new_seg),
                run_time=0.50,
            )
            cluster_strands.add(*new_seg)

        # Beat: Millions of clusters can work together
        self.at("Millions of clusters")
        field = VGroup()
        for r in range(4):
            for c in range(6):
                dot = Circle(
                    radius=0.20,
                    stroke_color=TEAL, stroke_width=2.5,
                    fill_color=GOLD, fill_opacity=0.45,
                ).move_to([rx_c[0] - 2.0 + c * 0.80, 1.35 - r * 0.65, 0])
                field.add(dot)
        field_note = T("many clusters in parallel", size=26, color=TEAL).move_to([rx_c[0], -2.05, 0])
        self.play(
            ReplacementTransform(VGroup(cluster_strands, cluster_tips), field),
            swap(right_note, field_note, run_time=0.7),
            run_time=1.3,
        )
        self.play(field.animate.set_fill(GREEN, opacity=0.85), run_time=0.45)
        self.play(field.animate.set_fill(TEAL, opacity=0.55), run_time=0.45)

        # Beat: both ends of each fragment can be read
        self.at("both ends")
        frag_y = 0.25
        frag_box = RoundedRectangle(
            corner_radius=0.10, width=4.6, height=0.55,
            stroke_color=BLUE, stroke_width=2.5, fill_color=BLUE, fill_opacity=0.18,
        ).move_to([rx_c[0], frag_y, 0])
        read_l = Arrow([rx_c[0] - 2.25, frag_y - 0.65, 0], [rx_c[0] - 1.05, frag_y - 0.65, 0], color=GOLD, stroke_width=6, buff=0)
        read_r = Arrow([rx_c[0] + 2.25, frag_y - 0.65, 0], [rx_c[0] + 1.05, frag_y - 0.65, 0], color=GOLD, stroke_width=6, buff=0)
        ends_note = T("both ends read inward", size=26, color=GOLD).move_to([rx_c[0], -2.05, 0])
        self.play(
            FadeOut(field), FadeIn(frag_box),
            swap(field_note, ends_note, run_time=0.6),
            run_time=1.0,
        )
        self.play(GrowArrow(read_l), GrowArrow(read_r), run_time=2.2)

        # Beat: Yet each reported stretch remains short
        self.at("remains short")
        gap_mark = DashedLine(
            [rx_c[0] - 0.9, frag_y - 0.65, 0], [rx_c[0] + 0.9, frag_y - 0.65, 0],
            color=GREY, stroke_width=3,
        )
        short_note = T("each reported stretch stays short", size=26, color=GOLD).move_to([rx_c[0], -2.05, 0])
        self.play(Create(gap_mark), swap(ends_note, short_note, run_time=0.7), run_time=1.6)
        self.finish()


# ------------------------------------------------------------------ S09Long
class S09Long(SpokenScene):
    def construct(self):
        tag = scope_tag("schematic")
        short_frag = RoundedRectangle(
            corner_radius=0.12, width=3.6, height=0.52,
            stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.25,
        ).move_to([0, 0.2, 0])
        long_ribbon = RoundedRectangle(
            corner_radius=0.14, width=9.6, height=0.52,
            stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.28,
        ).move_to([0, 0.2, 0])
        head = T("Long-read single molecules", size=32, color=TEXT).move_to([0, 3.3, 0])
        self.add(short_frag, tag)

        # Beat 1: transform short fragment into one long gold ribbon
        self.at("single molecules")
        self.play(ReplacementTransform(short_frag, long_ribbon), FadeIn(head), run_time=2.4)

        # Beat 2: polymerase circles the same template repeatedly, supporting a consensus
        self.at("polymerase circles")
        circ_c = np.array([-3.55, 0.15, 0.0])
        circ_r = 1.48
        loop = Circle(radius=circ_r, stroke_color=GOLD, stroke_width=8, fill_opacity=0.0).move_to(circ_c)
        # Put polymerase marker at the bottom of the circle so its label sits cleanly below with zero overlap
        poly = RoundedRectangle(
            corner_radius=0.18, width=0.92, height=0.82,
            stroke_color=TEXT, stroke_width=4.0, fill_color=TEXT, fill_opacity=0.08,
        ).move_to([circ_c[0], circ_c[1] - circ_r, 0])
        poly_lab = T("polymerase", size=24, color=TEXT).next_to(poly, DOWN, buff=0.22)

        theta = ValueTracker(-PI / 2)
        bead = always_redraw(lambda: Dot(
            circ_c + circ_r * np.array([np.cos(theta.get_value()), np.sin(theta.get_value()), 0.0]),
            radius=0.16, color=TEXT, stroke_color=GREEN, stroke_width=3,
        ))
        self.play(ReplacementTransform(long_ribbon, loop), FadeIn(poly), FadeIn(poly_lab), run_time=0.85)
        self.add(bead)

        pass_rows = VGroup()
        tile_x0 = 0.85
        for p_idx in range(3):
            py = 1.50 - p_idx * 0.82
            p_lab = T(f"pass {p_idx + 1}", size=24, color=TEXT).move_to([tile_x0 - 0.15, py, 0])
            tiles = VGroup(*[
                make_block(0.56, 0.50, GREEN, LONG_BASES[b_idx], TEXT, size=24, fill_opacity=0.28).move_to(
                    [tile_x0 + 0.88 + b_idx * 0.64, py, 0]
                )
                for b_idx in range(7)
            ])
            pass_rows.add(VGroup(p_lab, tiles))

        self.play(theta.animate(rate_func=linear).set_value(-PI / 2 + TAU), FadeIn(pass_rows[0]), run_time=1.00)

        self.at("repeated passes")
        self.play(theta.animate(rate_func=linear).set_value(-PI / 2 + 2 * TAU), FadeIn(pass_rows[1]), run_time=0.85)
        self.play(theta.animate(rate_func=linear).set_value(-PI / 2 + 3 * TAU), FadeIn(pass_rows[2]), run_time=0.75)

        self.at("consensus")
        cons_tiles = VGroup(*[
            make_block(0.56, 0.54, GREEN, LONG_BASES[b_idx], TEXT, size=24, fill_opacity=0.45).move_to(
                [tile_x0 + 0.88 + b_idx * 0.64, -1.25, 0]
            )
            for b_idx in range(7)
        ])
        cons_lab = T("consensus", size=26, color=GREEN).next_to(cons_tiles, LEFT, buff=0.25)
        self.play(FadeIn(cons_lab), FadeIn(cons_tiles, shift=DOWN * 0.3), run_time=1.05)

        # Beat 3: Clear Part A cleanly, then straighten marked strand through pore + Plot
        self.at("In the other")
        self.remove(bead)
        strand_bar = RoundedRectangle(
            corner_radius=0.10, width=6.6, height=0.36,
            stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.32,
        ).move_to([1.2, 2.28, 0])
        strand_ticks = VGroup(*[
            Line([1.2 - 3.0 + k * 0.6, 2.12, 0], [1.2 - 3.0 + k * 0.6, 2.44, 0], color=GOLD, stroke_width=2.0)
            for k in range(11)
        ])
        straight_strand = VGroup(strand_bar, strand_ticks)
        pore_top = RoundedRectangle(
            corner_radius=0.08, width=0.95, height=0.44,
            stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.30,
        ).move_to([-1.5, 2.75, 0])
        pore_bot = RoundedRectangle(
            corner_radius=0.08, width=0.95, height=0.44,
            stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.30,
        ).move_to([-1.5, 1.81, 0])
        pore_lab = T("pore", size=26, color=TEAL).next_to(pore_top, RIGHT, buff=0.22)

        self.play(
            FadeOut(poly), FadeOut(poly_lab), FadeOut(pass_rows), FadeOut(cons_lab), FadeOut(cons_tiles),
            ReplacementTransform(loop, straight_strand),
            FadeIn(pore_top), FadeIn(pore_bot), FadeIn(pore_lab),
            run_time=0.85,
        )

        P = Plot(
            box=(-5.1, 5.5, -1.60, 0.45),
            xr=(0, 10), yr=(0, 1.0),
            xticks=[], yticks=[(0.2, "low"), (0.8, "high")],
            xlabel="", ylabel="ionic current (schematic)",
            color=GREY, size=22, label_size=24,
        )
        u_t = ValueTracker(0.0)
        trace = P.live_curve(nanopore_current, u_t, color=GREEN, width=5)
        dot = P.dot(lambda: u_t.get_value(), lambda: nanopore_current(u_t.get_value()), color=TEXT, ring=GREEN)

        self.play(Create(P), run_time=0.65)

        self.at("through a pore")
        self.add(trace, dot)
        self.play(
            u_t.animate(rate_func=linear).set_value(5.0),
            straight_strand.animate(rate_func=linear).shift(LEFT * 1.4),
            run_time=3.2,
        )

        # Beat 4: Software converts moving signal into base tiles synced with u_t
        self.at("Software converts")
        sw_lab = T("software base call:", size=24, color=GREEN).move_to([-4.6, -2.50, 0])
        def _decoded():
            n = int(np.clip(u_t.get_value(), 0, 10))
            return VGroup(*[
                make_block(0.58, 0.54, GREEN, LONG_BASES[k], TEXT, size=24, fill_opacity=0.38).move_to(
                    [-2.2 + k * 0.72, -2.50, 0]
                )
                for k in range(n)
            ])
        decoded_live = always_redraw(_decoded)
        self.play(FadeIn(sw_lab), run_time=0.35)
        self.add(decoded_live)
        self.play(
            u_t.animate(rate_func=linear).set_value(10.0),
            straight_strand.animate(rate_func=linear).shift(LEFT * 1.3),
            run_time=3.6,
        )

        # Beat 5: Both approaches preserve longer-range context
        self.at("longer")
        ctx_lab = T("longer-range context preserved", size=28, color=GOLD).move_to([0.0, -3.28, 0])
        self.play(FadeIn(ctx_lab), run_time=1.0)
        self.finish()


# ------------------------------------------------------------------ S10Evidence
class S10Evidence(SpokenScene):
    def construct(self):
        tpl_y = 2.05
        # Keep template within safe bounds while spanning full width
        tpl_ribbon = RoundedRectangle(
            corner_radius=0.14, width=12.4, height=0.72,
            stroke_color=BLUE, stroke_width=3.5, fill_color=BLUE, fill_opacity=0.25,
        ).move_to([0, tpl_y, 0])
        tpl_ticks = VGroup(*[
            Line([-5.8 + k * 0.58, tpl_y - 0.36, 0], [-5.8 + k * 0.58, tpl_y - 0.20, 0], color=BLUE, stroke_width=2)
            for k in range(21)
        ])
        tpl_lab = T("chromosome template", size=28, color=BLUE).move_to([0, 2.95, 0])
        tag = scope_tag("schematic")

        mini_sanger = VGroup(*[
            Rectangle(width=0.7 + 0.45 * i, height=0.24, stroke_color=RED, stroke_width=2, fill_color=GOLD, fill_opacity=0.35).move_to(
                [-4.2, -0.55 - i * 0.34, 0]
            )
            for i in range(4)
        ])
        mini_short = VGroup(*[
            Rectangle(width=0.95, height=0.22, stroke_color=TEAL, stroke_width=2, fill_color=GOLD, fill_opacity=0.35).move_to(
                [0.0, -0.55 - i * 0.32, 0]
            )
            for i in range(4)
        ])
        mini_long = RoundedRectangle(
            corner_radius=0.08, width=3.2, height=0.38,
            stroke_color=GREEN, stroke_width=2.5, fill_color=GOLD, fill_opacity=0.38,
        ).move_to([4.2, -1.0, 0])

        self.add(tpl_ribbon, tpl_ticks, tpl_lab, mini_sanger, mini_short, mini_long, tag)
        self.play(
            mini_sanger.animate.shift(UP * 0.35),
            mini_short.animate.shift(UP * 0.35),
            mini_long.animate.shift(UP * 0.35).stretch(1.06, 0),
            run_time=1.8,
        )

        # Height 1.72 ensures box acts as a card panel (> th + 1.2) so layout_check never confuses title & subtitle
        def make_card(title, subtitle, color, x, y):
            box = RoundedRectangle(
                corner_radius=0.16, width=3.45, height=1.72,
                stroke_color=color, stroke_width=3, fill_color=BG, fill_opacity=0.92,
            ).move_to([x, y, 0])
            t1 = T(title, size=28, color=color).move_to([x, y + 0.32, 0])
            t2 = T(subtitle, size=24, color=TEXT).move_to([x, y - 0.32, 0])
            return VGroup(box, t1, t2)

        card_s = make_card("Sanger ladder", "read length, stops", RED, -4.2, -1.0)
        card_sr = make_card("Short reads", "cycles, short span", TEAL, 0.0, -1.0)
        card_lr = make_card("Long read", "longer context", GREEN, 4.2, -1.0)

        self.at("chemistry")
        self.play(
            ReplacementTransform(mini_sanger, card_s),
            ReplacementTransform(mini_short, card_sr),
            ReplacementTransform(mini_long, card_lr),
            run_time=1.8,
        )

        # Sequentially highlight cards + slide candidate fragment probes along chromosome template
        self.at("read length")
        probe_s = RoundedRectangle(corner_radius=0.06, width=1.15, height=0.22, stroke_color=RED, stroke_width=2.5, fill_color=RED, fill_opacity=0.45).move_to([-4.6, 1.38, 0])
        probe_sr = RoundedRectangle(corner_radius=0.06, width=0.85, height=0.22, stroke_color=TEAL, stroke_width=2.5, fill_color=TEAL, fill_opacity=0.45).move_to([-0.5, 1.05, 0])
        probe_lr = RoundedRectangle(corner_radius=0.06, width=2.45, height=0.22, stroke_color=GREEN, stroke_width=2.5, fill_color=GREEN, fill_opacity=0.45).move_to([3.8, 0.72, 0])
        shape_note = T("chemistry + fragments + software -> read evidence", size=28, color=TEXT).move_to([0, -2.8, 0])
        self.play(FadeIn(shape_note), FadeIn(probe_s), FadeIn(probe_sr), FadeIn(probe_lr), run_time=0.8)
        for card, col, probe, dx in (
            (card_s, RED, probe_s, 3.2),
            (card_sr, TEAL, probe_sr, 3.4),
            (card_lr, GREEN, probe_lr, -4.0),
        ):
            self.play(card[0].animate.set_stroke(TEXT, width=4.5), probe.animate.shift(RIGHT * dx), run_time=0.75)
            self.play(card[0].animate.set_stroke(col, width=3.0), run_time=0.35)

        # Beat: A read is still evidence from one fragment, not a chromosome
        self.at("one fragment")
        frag_note = T("evidence from one fragment, not a chromosome", size=28, color=GOLD).move_to([0, -2.8, 0])
        self.play(
            swap(shape_note, frag_note, run_time=0.75),
            probe_s.animate.move_to([2.6, 1.38, 0]),
            probe_sr.animate.move_to([-3.4, 1.05, 0]),
            run_time=1.3,
        )
        self.play(
            tpl_ribbon.animate.set_stroke(BLUE, width=5),
            probe_lr.animate.move_to([-2.4, 0.72, 0]),
            run_time=1.1,
        )
        self.play(tpl_ribbon.animate.set_stroke(BLUE, width=3.5), run_time=0.5)

        # Beat: Later analysis must decide where it belongs (candidate bars & '?' slide along template without resolving)
        self.at("Later analysis")
        q_s = T("?", size=38, color=GREY, weight=BOLD).next_to(probe_s, RIGHT, buff=0.34)
        q_sr = T("?", size=38, color=GREY, weight=BOLD).next_to(probe_sr, RIGHT, buff=0.34)
        q_lr = T("?", size=38, color=GREY, weight=BOLD).next_to(probe_lr, RIGHT, buff=0.34)
        qs = VGroup(q_s, q_sr, q_lr)

        self.play(
            FadeIn(qs),
            probe_s.animate.shift(LEFT * 3.8), q_s.animate.shift(LEFT * 3.8),
            probe_sr.animate.shift(RIGHT * 4.2), q_sr.animate.shift(RIGHT * 4.2),
            probe_lr.animate.shift(RIGHT * 4.6), q_lr.animate.shift(RIGHT * 4.6),
            run_time=2.2,
        )

        self.at("Genome results")
        fit_note = T("where does each read fit?", size=28, color=GOLD).move_to([0, -2.8, 0])
        self.play(
            swap(frag_note, fit_note, run_time=0.7),
            probe_s.animate.shift(RIGHT * 4.4), q_s.animate.shift(RIGHT * 4.4),
            probe_sr.animate.shift(LEFT * 3.6), q_sr.animate.shift(LEFT * 3.6),
            probe_lr.animate.shift(LEFT * 4.2), q_lr.animate.shift(LEFT * 4.2),
            run_time=2.4,
        )
        self.play(
            probe_s.animate.shift(LEFT * 2.2), q_s.animate.shift(LEFT * 2.2),
            probe_sr.animate.shift(RIGHT * 1.8), q_sr.animate.shift(RIGHT * 1.8),
            probe_lr.animate.shift(RIGHT * 2.0), q_lr.animate.shift(RIGHT * 2.0),
            run_time=1.8,
        )
        self.finish()


# ------------------------------------------------------------------ S11Rule
class S11Rule(SpokenScene):
    def construct(self):
        tag = scope_tag("schematic")

        def make_card(title, color, x, y):
            box = RoundedRectangle(
                corner_radius=0.14, width=3.3, height=1.05,
                stroke_color=color, stroke_width=3, fill_color=BG, fill_opacity=0.92,
            ).move_to([x, y, 0])
            t1 = T(title, size=26, color=color).move_to(box)
            return VGroup(box, t1)

        card_s = make_card("Sanger ladder", RED, -4.1, 1.9)
        card_sr = make_card("Short reads", TEAL, 0.0, 1.9)
        card_lr = make_card("Long read", GREEN, 4.1, 1.9)

        read_tiles = VGroup(*[
            make_block(0.76, 0.72, GOLD, LONG_BASES[k], TEXT, size=30, fill_opacity=0.35)
            for k in range(6)
        ]).arrange(RIGHT, buff=0.08).move_to([0.0, 0.0, 0])
        read_label = T("ordered base calls", size=28, color=GOLD).next_to(read_tiles, DOWN, buff=0.28)

        self.add(card_s, card_sr, card_lr, tag)

        # Beat 1: fade card labels out cleanly first (prevents text_overlap in motion), then merge boxes into read_tiles
        self.at("ordered base calls")
        self.play(FadeOut(card_s[1]), FadeOut(card_sr[1]), FadeOut(card_lr[1]), run_time=0.35)
        self.play(
            ReplacementTransform(VGroup(card_s[0], card_sr[0], card_lr[0]), read_tiles),
            FadeIn(read_label),
            run_time=1.25,
        )

        # Size boxes cleanly to text with boxed_label so text never overflows
        icon_stop = boxed_label("stop", RED, size=26, box=(2.75, 0.68), fill_opacity=0.35).move_to([-4.5, 1.4, 0])
        icon_pause = boxed_label("pause cycle", TEAL, size=26, box=(2.75, 0.68), fill_opacity=0.35).move_to([-4.5, 0.0, 0])
        icon_curr = boxed_label("current trace", GREEN, size=26, box=(2.75, 0.68), fill_opacity=0.35).move_to([-4.5, -1.4, 0])

        self.play(read_tiles.animate.move_to([1.35, 0.0, 0]), read_label.animate.move_to([1.35, -0.78, 0]), run_time=0.55)

        self.at("polymerase stop")
        self.play(FadeIn(icon_stop, shift=RIGHT * 0.2), run_time=0.8)
        self.at("colored pauses")
        self.play(FadeIn(icon_pause, shift=RIGHT * 0.2), run_time=0.8)
        self.at("changing current")
        self.play(FadeIn(icon_curr, shift=RIGHT * 0.2), run_time=0.8)

        self.at("ordered string")
        arr1 = Arrow(icon_stop.get_right() + RIGHT * 0.14, read_tiles.get_left() + LEFT * 0.16 + UP * 0.22, color=RED, stroke_width=3.5, buff=0)
        arr2 = Arrow(icon_pause.get_right() + RIGHT * 0.14, read_tiles.get_left() + LEFT * 0.16, color=TEAL, stroke_width=3.5, buff=0)
        arr3 = Arrow(icon_curr.get_right() + RIGHT * 0.14, read_tiles.get_left() + LEFT * 0.16 + DOWN * 0.22, color=GREEN, stroke_width=3.5, buff=0)
        self.play(GrowArrow(arr1), GrowArrow(arr2), GrowArrow(arr3), run_time=1.1)
        # Travelling data tokens along all three arrows while transitioning to "computer"
        dots = VGroup(
            Dot(arr1.get_start(), radius=0.09, color=RED),
            Dot(arr2.get_start(), radius=0.09, color=TEAL),
            Dot(arr3.get_start(), radius=0.09, color=GREEN),
        )
        self.add(dots)
        self.play(
            dots[0].animate.move_to(arr1.get_end()),
            dots[1].animate.move_to(arr2.get_end()),
            dots[2].animate.move_to(arr3.get_end()),
            run_time=1.2,
        )
        self.remove(dots)

        # Beat 3: The chemistry shapes what evidence reaches the computer
        self.at("computer")
        comp_box = SurroundingRectangle(VGroup(read_tiles, read_label), color=TEXT, stroke_width=2.5, buff=0.22)
        comp_lab = T("evidence to computer", size=26, color=TEXT).next_to(comp_box, UP, buff=0.18)
        self.play(Create(comp_box), FadeIn(comp_lab), run_time=0.95)
        self.play(
            comp_box.animate.set_stroke(GOLD, width=4.0),
            read_tiles.animate.scale(1.03),
            run_time=0.65,
        )
        self.play(
            comp_box.animate.set_stroke(TEXT, width=2.5),
            read_tiles.animate.scale(1 / 1.03),
            run_time=0.65,
        )

        # Beat 4: Fade chemistry boxes out BEFORE moving read_tiles left so tiles never slide over fading text
        self.at("every calculation")
        trunk_x0 = 1.45
        fork_x = 2.45
        trunk = Line([trunk_x0, 0.0, 0], [fork_x, 0.0, 0], color=BLUE, stroke_width=10)
        branch_up = Line([fork_x, 0.0, 0], [5.7, 1.55, 0], color=BLUE, stroke_width=10)
        branch_dn = Line([fork_x, 0.0, 0], [5.7, -1.55, 0], color=BLUE, stroke_width=10)
        q_up = T("?", size=38, color=GREY, weight=BOLD).move_to([4.3, 1.75, 0])
        q_dn = T("?", size=38, color=GREY, weight=BOLD).move_to([4.3, -1.75, 0])
        path_lab = T("one path or several?", size=28, color=BLUE).move_to([3.7, 2.75, 0])

        self.play(
            FadeOut(icon_stop), FadeOut(icon_pause), FadeOut(icon_curr),
            FadeOut(arr1), FadeOut(arr2), FadeOut(arr3),
            FadeOut(comp_box), FadeOut(comp_lab),
            run_time=0.45,
        )
        self.play(
            read_tiles.animate.scale(0.85).move_to([-3.8, 0.0, 0]),
            read_label.animate.move_to([-3.8, -0.78, 0]),
            Create(trunk), Create(branch_up), Create(branch_dn),
            FadeIn(q_up), FadeIn(q_dn), FadeIn(path_lab),
            run_time=1.8,
        )

        # Beat 5: Read glides toward branching blue path and stops BEFORE trunk_x0 (at x = -1.65 -> right edge +0.47)
        self.at("next question")
        self.play(
            read_tiles.animate.move_to([-1.65, 0.0, 0]),
            read_label.animate.move_to([-1.65, -0.78, 0]),
            run_time=1.8,
        )
        # Dashed lines start cleanly right of read_tiles (x = +0.62) and point toward both branches
        opt_up = DashedLine([0.62, 0.22, 0], [3.3, 1.05, 0], color=GOLD, stroke_width=3.5)
        opt_dn = DashedLine([0.62, -0.22, 0], [3.3, -1.05, 0], color=GOLD, stroke_width=3.5)
        self.play(Create(opt_up), Create(opt_dn), run_time=1.2)
        self.play(branch_up.animate.set_stroke(GOLD, width=12), run_time=0.5)
        self.play(branch_up.animate.set_stroke(BLUE, width=10), branch_dn.animate.set_stroke(GOLD, width=12), run_time=0.5)
        self.play(branch_dn.animate.set_stroke(BLUE, width=10), run_time=0.4)
        self.finish()


# ------------------------------------------------------------------ S12End
class S12End(EndCard):
    LINE = "Sequencing turns molecular events into ordered base calls."
