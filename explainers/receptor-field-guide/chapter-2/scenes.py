"""
Receptor Timing: Add Up the Waits — Animation scenes for "A Field Guide to Receptors".

COLOUR MAP (one colour per concept across the whole film):
    CYAN    (#58C4DD) : Ligand-gated muscle channel (nicotinic), its ion flow, its trace & wait bars
    TEAL    (#2EC4B6) : Seven-pass GPCR (heart muscarinic receptor)
    BLUE    (#6096FA) : GIRK potassium channel, its K+ efflux, its trace & wait bars
    PURPLE  (#B388FF) : Trimeric G protein and beta-gamma subunits
    GOLD    (#E5C158) : Extracellular water-soluble ligands (acetylcholine, kinase ligand) & phosphate tags
    AMBER   (#F79D3B) : Fat-soluble hormone (estradiol)
    ORANGE  (#FF6B35) : Single-pass kinase receptors and their wait bars
    CORAL   (#F4607E) : Nuclear receptor, newly made protein, and nuclear wait bars
    RED     (#FC6255) : GDP / off state
    GREEN   (#83C167) : GTP / active state / high-gain enzyme cascade
    GREY    (#8B93A1) : Plasma membrane, nuclear envelope, inactive baseline / low-gain comparison
    TEXT    (#E8EAF0) : DNA, new RNA, partner protein, headings, numbers, equations

CARRIED WORLD:
    A cross-section of a cell: extracellular space above a horizontal GREY plasma membrane,
    cytosol below, a GREY nuclear envelope arc at lower right, and a shared bottom schematic
    timeline. Scenes zoom into the relevant membrane patch or nucleus and pull back to compare
    all routes on the same timeline.

WHAT CHANGES PER SPOKEN SCENE (and what it is computed from):
    s00_link_and_question       : Three routes fire in sequence on the carried cell as ACh docks on
                                  CYAN and TEAL and estradiol crosses straight to CORAL; schematic
                                  timeline extends from < 1 ms to tens of ms to hours?.
    s02_sum_of_waits            : Zoomed CYAN muscle channel docks two GOLD ACh tokens, widens pore,
                                  streams computed ions downward, and builds 2 end-to-end schematic
                                  wait blocks (tens of us each -> < 1 ms).
    s03_gpcr_bottleneck         : Heart GPCR builds 4 schematic wait blocks (GDP exchange longest),
                                  then unaided G-protein clock sector & bar sweep continuously to 1 / 0.44 = 2.3 min.
    s04_predict_population      : 20 PURPLE G proteins (all GDP) sit under GOLD-bound TEAL; live speedup
                                  bar & rate bar compute 0.44 * 1000 = 440/min ~ 7.3/s and 1/7.3 ~ 140 ms,
                                  sweeping a preview bar to 140 ms (mean) beside a masked current plot.
    s06_reveal_and_guiding_idea : Clock runs 0..400 ms; 20 G proteins flip GDP->GTP at fixed-seed (seed 3)
                                  exponential times (rate 7.3/s) while Plot draws f(t) = 1 - exp(-7.3t),
                                  highlighting 10% (2/20) at ~14 ms, beta-gamma lag, and BLUE current rise.
    s07_slow_routes_single_pass : Two ORANGE single-pass stems pair on GOLD ligand binding (with a
                                  pre-paired rearrangement note), add GOLD phosphate dots, recruit
                                  a TEXT partner block, and extend an ORANGE seconds-to-minutes bar.
    s08_nuclear_paradox_solved  : AMBER estradiol crosses the membrane with no relay to CORAL on DNA;
                                  new RNA emerges at minutes, building CORAL new protein blocks as
                                  the CORAL bar stretches to tens of min to hours vs CYAN < 1 ms.
    s09_duration_off_steps      : Three stacked rows run ON up to ligand-clear at t = 0: CYAN shuts (~1 ms),
                                  PURPLE stays GTP-bound keeping BLUE open for seconds until GTP splits,
                                  CORAL new protein keeps gene program running after hormone leaves.
    s10_where_rule_stops        : Three limit panels: computed gain*t^2 curves, dots & output bars cross
                                  threshold sooner at high gain; independent potency and speed dials turn;
                                  AMBER touches a '?' surface marker above the slow nuclear route.
    s11_handoff                 : Wide carried cell lights up each route's slowest on and slowest off
                                  bars in sequence across all four architectures.
"""

from bp_parts import *  # noqa: F401,F403

CYAN = "#58C4DD"
TEAL = "#2EC4B6"
BLUE = "#6096FA"
PURPLE = "#B388FF"
GOLD = "#E5C158"
AMBER = "#F79D3B"
ORANGE = "#FF6B35"
CORAL = "#F4607E"

RATE_UNAIDED_MIN = 0.44
ACCEL = 1000.0
RATE_PER_MIN = RATE_UNAIDED_MIN * ACCEL
K_FIT = 7.3


# ------------------------------------------------------------------ shared builders
def make_membrane(y=1.3, x0=-6.2, x1=6.2, gap=0.14):
    """Double-line GREY plasma membrane representing the lipid bilayer."""
    top = Line([x0, y + gap / 2, 0], [x1, y + gap / 2, 0], color=GREY, stroke_width=4.2)
    bot = Line([x0, y - gap / 2, 0], [x1, y - gap / 2, 0], color=GREY, stroke_width=4.2)
    return VGroup(top, bot)


def make_nucleus_arc(center=(4.1, -2.0, 0), rx=2.2, ry=1.55):
    """Faint GREY nuclear envelope arc in the cytosol."""
    pts = [
        [center[0] + rx * np.cos(a), center[1] + ry * np.sin(a), 0.0]
        for a in np.linspace(0.12 * PI, 0.88 * PI, 48)
    ]
    outer = VMobject(color=GREY, stroke_width=4.2).set_points_as_corners(pts)
    pts2 = [
        [center[0] + (rx - 0.12) * np.cos(a), center[1] + (ry - 0.12) * np.sin(a), 0.0]
        for a in np.linspace(0.14 * PI, 0.86 * PI, 48)
    ]
    inner = VMobject(color=GREY, stroke_width=3.2).set_points_as_corners(pts2)
    return VGroup(outer, inner)


def make_nicotinic_channel(center=(-4.2, 1.3, 0), w=0.22, h=0.95, open_state=False):
    """Five CYAN subunits around a central pore."""
    cx, cy, _ = center
    spread = 0.34 if open_state else 0.18
    xs = [-2 * w - spread, -w - spread * 0.65, 0.0, w + spread * 0.65, 2 * w + spread]
    blocks = VGroup()
    for i, dx in enumerate(xs):
        op = 0.55 if i == 2 and open_state else (0.72 if i == 2 else 0.54)
        b = RoundedRectangle(
            corner_radius=0.06,
            width=w,
            height=h if i != 2 else h * (0.45 if open_state else 0.82),
            stroke_color=CYAN,
            stroke_width=3.2,
            fill_color=CYAN,
            fill_opacity=op,
        ).move_to([cx + dx, cy + (0.28 if i == 2 and open_state else 0.0), 0])
        blocks.add(b)
    return blocks


def make_gpcr(center=(0.0, 1.3, 0), n_helices=7, h=0.95, w=0.11, dx=0.17, active=False):
    """TEAL seven-bar transmembrane receptor."""
    cx, cy, _ = center
    bars = VGroup()
    for i in range(n_helices):
        x = cx + (i - (n_helices - 1) / 2) * dx
        tilt = 0.12 if (active and i >= 4) else 0.0
        b = RoundedRectangle(
            corner_radius=0.04,
            width=w,
            height=h,
            stroke_color=TEAL,
            stroke_width=2.8,
            fill_color=TEAL,
            fill_opacity=0.60 if active else 0.45,
        ).move_to([x + tilt, cy, 0])
        bars.add(b)
    return bars


def make_g_protein(center=(0.0, 0.25, 0), gtp=False, compact=False):
    """PURPLE G-protein body with a RED 'GDP' or GREEN 'GTP' badge."""
    w, h = (0.78, 0.44) if compact else (1.18, 0.62)
    body = RoundedRectangle(
        corner_radius=0.16,
        width=w,
        height=h,
        stroke_color=PURPLE,
        stroke_width=3.2,
        fill_color=PURPLE,
        fill_opacity=0.48,
    ).move_to(center)
    col = GREEN if gtp else RED
    txt = "GTP" if gtp else "GDP"
    badge = boxed_label(txt, color=col, size=24 if compact else 26, pad=0.11 if compact else 0.14, fill_opacity=0.30)
    badge.next_to(body, DOWN, buff=0.08)
    g = VGroup(body, badge)
    g.body = body
    g.badge = badge
    return g


def make_girk(center=(1.5, 1.3, 0), h=0.92, w=0.28, open_state=False):
    """BLUE potassium channel formed by two halves."""
    cx, cy, _ = center
    sep = 0.36 if open_state else 0.18
    left = RoundedRectangle(corner_radius=0.07, width=w, height=h, stroke_color=BLUE, stroke_width=3.2, fill_color=BLUE, fill_opacity=0.54)
    right = left.copy()
    left.move_to([cx - sep, cy, 0])
    right.move_to([cx + sep, cy, 0])
    return VGroup(left, right)


def make_ligand(color=GOLD, radius=0.14, label=None):
    """Circular ligand token (no molecular structure)."""
    dot = Dot(radius=radius, color=color, stroke_color=TEXT, stroke_width=2.0)
    if label:
        t = T(label, 24, color).next_to(dot, UP, buff=0.1)
        return VGroup(dot, t)
    return dot


def make_rtk_stem(x, y_mem=1.3, color=ORANGE, scale=1.0):
    """Single-pass kinase receptor stem crossing the membrane once with inner enzyme block."""
    stem = Line([x, y_mem + 0.65 * scale, 0], [x, y_mem - 0.85 * scale, 0], color=color, stroke_width=7.5 * scale)
    outer = RoundedRectangle(
        corner_radius=0.1,
        width=0.38 * scale,
        height=0.38 * scale,
        stroke_color=color,
        stroke_width=3.2,
        fill_color=color,
        fill_opacity=0.52,
    ).move_to([x, y_mem + 0.68 * scale, 0])
    kinase = RoundedRectangle(
        corner_radius=0.12,
        width=0.76 * scale,
        height=0.58 * scale,
        stroke_color=color,
        stroke_width=3.2,
        fill_color=color,
        fill_opacity=0.52,
    ).move_to([x, y_mem - 1.05 * scale, 0])
    g = VGroup(stem, outer, kinase)
    g.stem = stem
    g.outer = outer
    g.kinase = kinase
    return g


def make_nuclear_receptor(center=(4.1, -1.0, 0), occupied=False):
    """CORAL nuclear receptor."""
    return RoundedRectangle(
        corner_radius=0.14,
        width=1.18,
        height=0.60,
        stroke_color=CORAL,
        stroke_width=3.2,
        fill_color=CORAL,
        fill_opacity=0.56 if occupied else 0.40,
    ).move_to(center)


def make_timeline(y=-2.55, x0=-5.9, x1=4.8):
    """Shared schematic timeline along the bottom."""
    return Arrow([x0, y, 0], [x1, y, 0], color=GREY, stroke_width=4.2, buff=0, tip_length=0.22)


def make_ion_stream(x, y_top, y_bot, color=CYAN, direction=DOWN, n=6):
    """Animated updater stream of ions passing through an open channel."""
    dots = VGroup()
    span = abs(y_top - y_bot)
    for i in range(n):
        d = Dot(radius=0.09, color=color)
        d._phase = i / n
        y_init = y_top - d._phase * span if np.allclose(direction, DOWN) else y_bot + d._phase * span
        d.move_to([x + ((i % 3) - 1) * 0.08, y_init, 0])

        def step(m, dt, x=x, yt=y_top, yb=y_bot, dir_vec=direction, sp=span):
            m._phase = (m._phase + dt * 1.1) % 1.0
            y = yt - m._phase * sp if np.allclose(dir_vec, DOWN) else yb + m._phase * sp
            m.set_y(y)

        d.add_updater(step)
        dots.add(d)
    return dots


# ------------------------------------------------------------------ S00
class S00LinkAndQuestion(SpokenScene):
    def construct(self):
        mem = make_membrane(y=1.25)
        nuc = make_nucleus_arc(center=(4.15, -2.05, 0), rx=2.05, ry=1.45)
        timeline = make_timeline(y=-2.55, x0=-5.9, x1=4.5)
        tag = scope_tag("schematic")

        chan = make_nicotinic_channel(center=(-4.2, 1.25, 0), open_state=False)
        chan_lbl = T("muscle channel", 28, CYAN).move_to([-4.2, 2.9, 0])
        ach1 = make_ligand(GOLD, radius=0.14).move_to([-4.45, 2.35, 0])
        ach2 = make_ligand(GOLD, radius=0.14).move_to([-3.95, 2.35, 0])
        ach_lbl = T("ACh", 26, GOLD).move_to([-3.2, 2.35, 0])

        p_cyan = Plot(box=(-5.6, -2.9, -1.75, -0.25), xr=(0, 10), yr=(0, 1), color=GREY, stroke=3.0)
        cyan_t = ValueTracker(0.0)
        cyan_curve = p_cyan.live_curve(lambda x: 0.92 * np.exp(-((x - 1.2) / 0.55) ** 2), cyan_t, color=CYAN, width=6.5)

        gpcr = make_gpcr(center=(-0.65, 1.25, 0), active=False)
        gpcr_lbl = T("heart GPCR", 28, TEAL).move_to([-0.65, 2.9, 0])
        ach_c = make_ligand(GOLD, radius=0.14).move_to([-0.65, 2.35, 0])
        gprot = make_g_protein(center=(-0.45, 0.2, 0), gtp=False, compact=True)
        girk = make_girk(center=(1.25, 1.25, 0), open_state=False)

        p_blue = Plot(box=(-1.3, 1.5, -1.75, -0.25), xr=(0, 10), yr=(0, 1), color=GREY, stroke=3.0)
        blue_t = ValueTracker(0.0)
        blue_curve = p_blue.live_curve(lambda x: 0.0 if x < 3.0 else 0.85 * (1 - np.exp(-0.55 * (x - 3.0))), blue_t, color=BLUE, width=6.5)

        est_lbl = T("estradiol", 28, AMBER).move_to([4.15, 2.9, 0])
        est = make_ligand(AMBER, radius=0.20).move_to([4.15, 2.3, 0])
        nuc_rec = make_nuclear_receptor(center=(4.15, -1.15, 0), occupied=False)
        nr_lbl = T("nuclear receptor", 26, CORAL).next_to(nuc_rec, DOWN, buff=0.16)
        no_relay = T("no relay", 26, TEXT).move_to([4.15, 0.25, 0])

        bar_cyan = Line([-5.6, -2.55, 0], [-4.7, -2.55, 0], color=CYAN, stroke_width=15)
        lbl_cyan = M("< 1 ms", 26, CYAN).next_to(bar_cyan, DOWN, buff=0.16)
        bar_blue = Line([-2.3, -2.55, 0], [-0.2, -2.55, 0], color=BLUE, stroke_width=15)
        lbl_blue = M("tens of ms", 26, BLUE).next_to(bar_blue, DOWN, buff=0.16)
        bar_coral = Line([1.3, -2.55, 0], [4.1, -2.55, 0], color=CORAL, stroke_width=15)
        lbl_hours = M("hours?", 28, GOLD).next_to(bar_coral, DOWN, buff=0.16)
        q_mark = T("?", 46, GOLD, weight=BOLD).move_to([4.95, -2.55, 0])

        self.add(mem, nuc, timeline, tag, chan, chan_lbl, ach1, ach2, ach_lbl, p_cyan,
                 gpcr, gpcr_lbl, ach_c, gprot, girk, p_blue, est_lbl, est, nuc_rec, nr_lbl)

        # 0.00: "A muscle channel opens almost at once"
        self.at("A muscle channel")
        self.add(cyan_curve)
        chan_open = make_nicotinic_channel(center=(-4.2, 1.25, 0), open_state=True)
        self.play(
            ach1.animate.move_to([-4.52, 1.85, 0]),
            ach2.animate.move_to([-3.88, 1.85, 0]),
            Transform(chan, chan_open),
            run_time=0.8,
        )
        ions_c = make_ion_stream(-4.2, 1.9, 0.35, CYAN, DOWN, n=6)
        self.add(ions_c)
        self.play(
            cyan_t.animate.set_value(10.0),
            GrowFromEdge(bar_cyan, LEFT),
            FadeIn(lbl_cyan),
            run_time=1.8,
        )

        # 3.34: "a heart receptor waits on a G protein"
        self.at("A heart receptor")
        self.add(blue_curve)
        gpcr_act = make_gpcr(center=(-0.65, 1.25, 0), active=True)
        gprot_on = make_g_protein(center=(0.25, 0.2, 0), gtp=True, compact=True)
        girk_open = make_girk(center=(1.25, 1.25, 0), open_state=True)
        self.play(
            ach_c.animate.move_to([-0.65, 1.85, 0]),
            Transform(gpcr, gpcr_act),
            run_time=0.7,
        )
        self.play(
            gprot.body.animate.move_to(gprot_on.body),
            swap(gprot.badge, gprot_on.badge, run_time=0.4),
            run_time=0.7,
        )
        self.play(Transform(girk, girk_open), run_time=0.5)
        ions_b = make_ion_stream(1.25, 1.9, 0.35, BLUE, UP, n=6)
        self.add(ions_b)
        self.play(
            blue_t.animate.set_value(10.0),
            GrowFromEdge(bar_blue, LEFT),
            FadeIn(lbl_blue),
            run_time=1.3,
        )

        # 6.80: "Now watch estradiol, a fat-soluble hormone, slip through the membrane with no relay"
        self.at("Now watch estradiol")
        est_trail = DashedLine([4.15, 2.3, 0], [4.15, -0.85, 0], color=AMBER, stroke_width=3.5)
        self.play(est.animate.move_to([4.15, 1.25, 0]), Create(est_trail), run_time=2.2)
        self.at("slip through")
        nuc_rec_occ = make_nuclear_receptor(center=(4.15, -1.15, 0), occupied=True)
        self.play(est.animate.move_to([4.15, -1.15, 0]), run_time=2.0)
        self.play(FadeOut(est_trail), FadeIn(no_relay), Transform(nuc_rec, nuc_rec_occ), run_time=0.6)

        # 13.44: "Why can that route still take hours?"
        self.at("Why can that")
        self.play(
            GrowFromEdge(bar_coral, LEFT),
            FadeIn(lbl_hours),
            FadeIn(q_mark, scale=1.1),
            run_time=0.9,
        )
        self.finish()


# ------------------------------------------------------------------ S01
class S01Title(TitleCard):
    LESSON = "A Field Guide to Receptors"
    TITLE = "Receptor Timing: Add Up the Waits"


# ------------------------------------------------------------------ S02
class S02SumOfWaits(SpokenScene):
    def construct(self):
        mem = make_membrane(y=1.3)
        chan = make_nicotinic_channel(center=(0.0, 1.3, 0), w=0.46, h=1.95, open_state=False)
        ach1 = make_ligand(GOLD, radius=0.22).move_to([-0.68, 2.75, 0])
        ach2 = make_ligand(GOLD, radius=0.22).move_to([0.68, 2.75, 0])
        ach_lbl = T("acetylcholine", 28, GOLD).move_to([2.7, 2.45, 0])

        title = T("onset ≈ sum of waits", 34, TEXT).move_to([0.0, 3.25, 0])
        timeline = make_timeline(y=-2.05, x0=-5.4, x1=5.4)
        tag = scope_tag("schematic")

        b1 = RoundedRectangle(corner_radius=0.1, width=4.6, height=0.72, stroke_color=GOLD, stroke_width=3.5, fill_color=GOLD, fill_opacity=0.42)
        b1.move_to([-2.45, -1.45, 0])
        l1 = T("1. binding", 28, GOLD).move_to(b1)

        b2 = RoundedRectangle(corner_radius=0.1, width=4.6, height=0.72, stroke_color=CYAN, stroke_width=3.5, fill_color=CYAN, fill_opacity=0.42)
        b2.move_to([2.35, -1.45, 0])
        l2 = T("2. pore opening", 28, CYAN).move_to(b2)

        prog = ValueTracker(0.0)
        prog_bar = always_redraw(
            lambda: Line(
                [-4.75, -2.05, 0],
                [-4.75 + 9.4 * prog.get_value(), -2.05, 0],
                color=GOLD if prog.get_value() <= 0.5 else CYAN,
                stroke_width=15,
            )
            if prog.get_value() > 0.01
            else VGroup()
        )

        # Three sequential step blocks lighting up end-to-end (step 1 finishes before step 2 starts)
        step_specs = [("step 1", GOLD, -2.5), ("step 2", TEAL, 0.0), ("step 3", CYAN, 2.5)]
        seq_t = ValueTracker(0.0)
        seq_boxes = VGroup()
        seq_fills = VGroup()
        seq_labels = VGroup()
        for idx, (s_txt, s_col, sx) in enumerate(step_specs):
            box = RoundedRectangle(corner_radius=0.09, width=2.44, height=0.54, stroke_color=s_col, stroke_width=2.8).move_to([sx, -0.35, 0])
            lbl = T(s_txt, 24, TEXT).move_to(box)

            def _mk_fill(i=idx, b=box, c=s_col):
                frac = float(np.clip(seq_t.get_value() - i, 0.0, 1.0))
                if frac <= 0.01:
                    return VGroup()
                return (
                    Rectangle(width=2.40 * frac, height=0.50, stroke_width=0, fill_color=c, fill_opacity=0.45)
                    .align_to(b, LEFT)
                    .shift(RIGHT * 0.02)
                    .set_y(-0.35)
                )

            seq_boxes.add(box)
            seq_fills.add(always_redraw(_mk_fill))
            seq_labels.add(lbl)
        seq_brace = Brace(seq_boxes, DOWN, buff=0.14, color=TEXT)
        seq_sum_lbl = T("sum of waits", 26, GOLD).next_to(seq_brace, DOWN, buff=0.12)
        sum_t = ValueTracker(0.0)
        sum_bar = always_redraw(
            lambda: Line([-3.72, -1.75, 0], [-3.72 + 7.44 * sum_t.get_value(), -1.75, 0], color=GOLD, stroke_width=10)
            if sum_t.get_value() > 0.02
            else VGroup()
        )

        self.add(mem, chan, ach1, ach2, ach_lbl, timeline, tag)

        # 0.00: "Each step from binding to output must finish before the next starts."
        self.at("Each step")
        self.play(FadeIn(seq_boxes), FadeIn(seq_labels), run_time=0.5)
        self.add(seq_fills)
        self.play(
            seq_t.animate.set_value(3.0),
            ach1.animate.shift(DOWN * 0.25),
            ach2.animate.shift(DOWN * 0.25),
            run_time=4.4,
            rate_func=linear,
        )

        # 5.58: "Onset time is roughly the sum of those waits."
        self.at("Onset time")
        self.play(
            FadeIn(title, shift=DOWN * 0.12),
            GrowFromCenter(seq_brace),
            FadeIn(seq_sum_lbl),
            run_time=0.9,
        )
        self.add(sum_bar)
        self.play(sum_t.animate.set_value(1.0), run_time=1.9, rate_func=linear)

        # 9.14: "A muscle channel needs only binding and opening."
        self.at("A muscle channel")
        for f in seq_fills:
            f.clear_updaters()
        sum_bar.clear_updaters()
        chan_lbl = T("muscle channel", 28, CYAN).move_to([-3.65, 0.55, 0])
        self.play(
            FadeOut(seq_boxes),
            FadeOut(seq_fills),
            FadeOut(seq_labels),
            FadeOut(seq_brace),
            FadeOut(seq_sum_lbl),
            FadeOut(sum_bar),
            FadeIn(chan_lbl),
            run_time=0.7,
        )

        self.at("only binding")
        self.add(prog_bar)
        self.play(
            ach1.animate.move_to([-0.82, 2.38, 0]),
            ach2.animate.move_to([0.82, 2.38, 0]),
            FadeIn(b1),
            FadeIn(l1),
            prog.animate.set_value(0.5),
            run_time=1.1,
        )

        self.at("opening")
        chan_open = make_nicotinic_channel(center=(0.0, 1.3, 0), w=0.46, h=1.95, open_state=True)
        self.play(
            Transform(chan, chan_open),
            FadeIn(b2),
            FadeIn(l2),
            prog.animate.set_value(1.0),
            run_time=1.1,
        )
        ions = make_ion_stream(0.0, 2.3, -0.8, CYAN, DOWN, n=7)
        self.add(ions)

        # 13.36: "Each takes tens of microseconds, finishing well under a millisecond."
        self.at("Each takes tens")
        brace = Brace(VGroup(b1, b2), DOWN, buff=0.42, color=TEXT)
        lbl_us = M("tens of µs each", 30, TEXT).next_to(brace, DOWN, buff=0.14)
        self.play(GrowFromCenter(brace), FadeIn(lbl_us), run_time=0.8)

        self.at("finishing well under")
        lbl_ms = M("total < 1 ms", 32, CYAN).next_to(brace, DOWN, buff=0.14)
        self.play(swap(lbl_us, lbl_ms, run_time=0.35))
        self.finish()


# ------------------------------------------------------------------ S03
class S03GpcrBottleneck(SpokenScene):
    def construct(self):
        mem = make_membrane(y=1.55)
        gpcr = make_gpcr(center=(-3.8, 1.55, 0), h=1.25, w=0.15, dx=0.22, active=False)
        gpcr_lbl = T("muscarinic GPCR", 28, TEAL).move_to([-3.8, 3.05, 0])
        ach = make_ligand(GOLD, radius=0.18).move_to([-2.3, 2.55, 0])

        gprot = make_g_protein(center=(-0.6, 0.25, 0), gtp=False, compact=False)
        g_lbl = T("G protein", 28, PURPLE).next_to(gprot.body, UP, buff=0.18)

        girk = make_girk(center=(3.9, 1.55, 0), h=1.25, w=0.36, open_state=False)
        girk_lbl = T("K+ channel", 28, BLUE).move_to([3.9, 3.05, 0])

        timeline = make_timeline(y=-2.25, x0=-5.8, x1=5.6)
        tag = scope_tag("schematic")

        seg1 = boxed_label("1. bind", color=GOLD, size=24, box=(1.5, 0.56), fill_opacity=0.30).move_to([-4.95, -1.75, 0])
        seg2 = boxed_label("2. GDP exchange (slowest)", color=RED, size=24, box=(5.1, 0.56), fill_opacity=0.30).move_to([-1.45, -1.75, 0])
        seg3 = boxed_label("3. shift", color=PURPLE, size=24, box=(1.6, 0.56), fill_opacity=0.30).move_to([2.1, -1.75, 0])
        seg4 = boxed_label("4. open", color=BLUE, size=24, box=(1.55, 0.56), fill_opacity=0.30).move_to([3.9, -1.75, 0])

        self.add(mem, gpcr, gpcr_lbl, ach, gprot, g_lbl, girk, girk_lbl, timeline, tag)

        # 0.00: "The heart route has four steps"
        self.at("has four steps")
        gpcr_act = make_gpcr(center=(-3.8, 1.55, 0), h=1.25, w=0.15, dx=0.22, active=True)
        self.play(
            ach.animate.move_to([-3.8, 2.38, 0]),
            Transform(gpcr, gpcr_act),
            FadeIn(seg1),
            run_time=1.0,
        )

        # 2.26: "exchange, swapping GDP for GTP, is the slowest"
        self.at("exchange")
        gprot_gtp = make_g_protein(center=(-0.6, 0.25, 0), gtp=True, compact=False)
        self.play(FadeIn(seg2), run_time=0.9)
        self.play(swap(gprot.badge, gprot_gtp.badge, run_time=0.4), run_time=0.5)
        gprot.submobjects[1] = gprot_gtp.badge
        self.play(
            FadeIn(seg3),
            gprot.animate.shift(RIGHT * 2.5),
            g_lbl.animate.shift(RIGHT * 2.5),
            run_time=1.2,
        )
        girk_open = make_girk(center=(3.9, 1.55, 0), h=1.25, w=0.36, open_state=True)
        self.play(FadeIn(seg4), Transform(girk, girk_open), run_time=0.8)
        ions_k = make_ion_stream(3.9, 2.25, 0.75, BLUE, UP, n=6)
        self.add(ions_k)

        # 7.50: "Alone, a G protein releases GDP 0.44 times a minute."
        self.at("Alone")
        gprot_alone = make_g_protein(center=(-4.2, -0.25, 0), gtp=False, compact=False)
        unaided_lbl = T("unaided G protein\n(no receptor)", 28, PURPLE, line_spacing=0.85).move_to([-4.2, 0.72, 0])

        wait_t = ValueTracker(0.0)
        c_clock = np.array([-0.85, 0.05, 0.0])
        r_clock = 0.88
        clock_ring = Circle(radius=r_clock, color=GREY, stroke_width=8).move_to(c_clock)
        clock_sector = always_redraw(
            lambda: Sector(
                radius=r_clock - 0.05,
                start_angle=PI / 2,
                angle=-TAU * max(0.005, wait_t.get_value() / 2.5),
                arc_center=c_clock,
                color=RED,
                fill_opacity=0.42,
                stroke_width=0,
            )
        )
        clock_arc = always_redraw(
            lambda: Arc(
                radius=r_clock,
                start_angle=PI / 2,
                angle=-TAU * max(0.005, wait_t.get_value() / 2.5),
                arc_center=c_clock,
                color=RED,
                stroke_width=10,
            )
        )
        clock_hand = always_redraw(
            lambda: Line(
                c_clock,
                c_clock
                + 0.78 * r_clock * np.array([
                    np.cos(PI / 2 - TAU * (wait_t.get_value() / 2.5)),
                    np.sin(PI / 2 - TAU * (wait_t.get_value() / 2.5)),
                    0.0,
                ]),
                color=GOLD,
                stroke_width=6,
            )
        )

        calc = M("1 ÷ 0.44 ≈ 2.3 min", 34, TEXT).move_to([3.45, 0.85, 0])
        rate_lbl = M("GDP release = 0.44 / min", 28, RED).move_to([3.45, 0.20, 0])
        timer_readout = counter("mean wait = {:.1f} min", wait_t, at=[3.45, -0.45, 0], size=32, color=GOLD)

        bar_bg = Line([1.05, -1.02, 0], [5.85, -1.02, 0], color=GREY, stroke_width=12)
        bar_fill = always_redraw(
            lambda: Line(
                [1.05, -1.02, 0],
                [1.05 + 4.8 * (wait_t.get_value() / 2.5), -1.02, 0],
                color=RED,
                stroke_width=16,
            )
            if wait_t.get_value() > 0.02
            else VGroup()
        )

        ions_k.clear_updaters()
        self.play(
            FadeOut(ions_k),
            FadeOut(gprot),
            FadeOut(g_lbl),
            FadeOut(gpcr),
            FadeOut(gpcr_lbl),
            FadeOut(ach),
            FadeOut(girk),
            FadeOut(girk_lbl),
            seg1.animate.set_opacity(0.25),
            seg3.animate.set_opacity(0.25),
            seg4.animate.set_opacity(0.25),
            FadeIn(gprot_alone),
            FadeIn(unaided_lbl),
            FadeIn(clock_ring),
            FadeIn(rate_lbl),
            FadeIn(bar_bg),
            run_time=0.8,
        )
        self.add(clock_sector, clock_arc, clock_hand, timer_readout, bar_fill)
        self.play(wait_t.animate.set_value(1.35), run_time=5.0, rate_func=linear)

        # 13.68: "1 over 0.44 is a mean wait of about 2.3 minutes."
        self.at("1 over")
        self.play(FadeIn(calc), run_time=0.6)
        self.play(wait_t.animate.set_value(1.0 / RATE_UNAIDED_MIN), run_time=2.5, rate_func=linear)
        self.finish()


# ------------------------------------------------------------------ S04 & S05 & S06 shared layout
GPCR_XS = (-4.8, -2.1, 0.6, 3.1)
GRID_X0, GRID_DX = -5.4, 0.96
GRID_YS = (1.36, 0.88)


def build_population_backdrop():
    """Shared world at the end of s04_predict_population and throughout s05_predict_pause."""
    mem = make_membrane(y=2.12)
    receptors = VGroup()
    ligs = VGroup()
    for x in GPCR_XS:
        receptors.add(make_gpcr(center=(x, 2.12, 0), h=0.82, w=0.09, dx=0.13, active=True))
        ligs.add(make_ligand(GOLD, radius=0.12).move_to([x, 2.65, 0]))

    gprots = VGroup()
    for r in range(2):
        for c in range(10):
            gx = GRID_X0 + c * GRID_DX
            gy = GRID_YS[r]
            box = RoundedRectangle(
                corner_radius=0.09,
                width=0.84,
                height=0.36,
                stroke_color=PURPLE,
                stroke_width=2.6,
                fill_color=PURPLE,
                fill_opacity=0.38,
            ).move_to([gx, gy, 0])
            tag = M("GDP", 22, RED).move_to(box)
            gprots.add(VGroup(box, tag))

    c1 = M("0.44 × 1,000 = 440 / min ≈ 7.3 / s", 26, GOLD).move_to([-5.85, -0.05, 0], aligned_edge=LEFT)
    c2 = M("1 ÷ 7.3 ≈ 140 ms (mean)", 30, TEXT).move_to([-2.7, -0.72, 0])

    clock_x0, clock_x1, clock_y = -5.7, 0.7, -1.78
    clock_line = Line([clock_x0, clock_y, 0], [clock_x1, clock_y, 0], color=GREY, stroke_width=5)
    tick_0 = Line([clock_x0, clock_y - 0.14, 0], [clock_x0, clock_y + 0.14, 0], color=TEXT, stroke_width=3.5)
    lbl_0 = M("0 ms", 24, TEXT).next_to(tick_0, DOWN, buff=0.14)
    x_140 = clock_x0 + (140.0 / 400.0) * (clock_x1 - clock_x0)
    tick_140 = Line([x_140, clock_y - 0.16, 0], [x_140, clock_y + 0.16, 0], color=GOLD, stroke_width=5)
    lbl_140 = M("140 ms (mean)", 24, GOLD).next_to(tick_140, DOWN, buff=0.14)
    tick_400 = Line([clock_x1, clock_y - 0.14, 0], [clock_x1, clock_y + 0.14, 0], color=GREY, stroke_width=3.5)
    lbl_400 = M("400 ms", 24, GREY).next_to(tick_400, DOWN, buff=0.14)
    cursor = Triangle(color=CYAN, fill_color=CYAN, fill_opacity=1.0).scale(0.16).rotate(PI).move_to([clock_x0, clock_y + 0.25, 0])
    clock = VGroup(clock_line, tick_0, lbl_0, tick_140, lbl_140, tick_400, lbl_400, cursor)

    panel = RoundedRectangle(corner_radius=0.16, width=4.2, height=2.25, stroke_color=BLUE, stroke_width=3.2, fill_color=BG, fill_opacity=0.95)
    panel.move_to([3.85, -1.28, 0])
    p_title = T("K+ current", 28, BLUE).move_to([3.85, -0.48, 0])
    q_panel = T("?", 64, GOLD, weight=BOLD).move_to([3.85, -1.45, 0])
    masked = VGroup(panel, p_title, q_panel)

    return VGroup(mem, receptors, ligs, gprots, c1, c2, clock, masked)


class S04PredictPopulation(SpokenScene):
    def construct(self):
        bg = build_population_backdrop()
        mem, receptors, ligs, gprots, c1, c2, clock, masked = bg
        clock_x0, clock_x1, clock_y = -5.7, 0.7, -1.78
        x_140 = clock_x0 + (140.0 / 400.0) * (clock_x1 - clock_x0)

        for l in ligs:
            l.shift(UP * 0.22)
        accel_badge = boxed_label("receptor speeds GDP release × 1,000", color=GOLD, size=28, fill_opacity=0.26).move_to([0.0, 3.30, 0])

        self.add(mem, receptors, ligs, gprots[0], gprots[1], gprots[2])

        # 0.00: "Suppose the occupied receptor speeds release a thousandfold."
        self.at("Suppose the occupied")
        mult_v = ValueTracker(1.0)
        mult_bar_bg = RoundedRectangle(corner_radius=0.08, width=6.4, height=0.38, stroke_color=GREY, stroke_width=2.5).move_to([-2.5, -1.78, 0])
        mult_fill = always_redraw(
            lambda: Rectangle(
                width=max(0.05, 6.4 * (np.log10(mult_v.get_value()) / 3.0)),
                height=0.36,
                stroke_width=0,
                fill_color=GOLD,
                fill_opacity=0.68,
            ).align_to(mult_bar_bg, LEFT).set_y(-1.78)
        )
        mult_num = counter("× {:.0f}", mult_v, at=[-2.5, -1.25, 0], size=30, color=GOLD)

        self.play(
            *[l.animate.shift(DOWN * 0.22) for l in ligs],
            FadeIn(accel_badge),
            FadeIn(mult_bar_bg),
            run_time=1.3,
        )
        self.add(mult_fill, mult_num)
        self.play(mult_v.animate.set_value(1000.0), run_time=2.0, rate_func=linear)

        # 5.60: "0.44 times a thousand is 440 a minute, about 7.3 a second."
        self.at("0 44 times")
        c1_left = M("0.44 × 1,000 = 440 / min", 26, GOLD).move_to([-5.85, -0.05, 0], aligned_edge=LEFT)
        c1_right = M("≈ 7.3 / s", 26, GOLD).next_to(c1_left, RIGHT, buff=0.22)
        rate_v = ValueTracker(0.44)
        rate_meter = counter("rate = {:.1f} / min", rate_v, at=[3.85, -1.05, 0], size=30, color=GOLD)
        rate_bar_bg = RoundedRectangle(corner_radius=0.08, width=3.8, height=0.34, stroke_color=GREY, stroke_width=2.5).move_to([3.85, -1.65, 0])
        rate_bar_fill = always_redraw(
            lambda: Rectangle(
                width=max(0.05, 3.8 * (rate_v.get_value() / 440.0)),
                height=0.32,
                stroke_width=0,
                fill_color=GOLD,
                fill_opacity=0.65,
            ).align_to(rate_bar_bg, LEFT).set_y(-1.65)
        )
        self.play(FadeIn(c1_left), FadeIn(rate_meter), FadeIn(rate_bar_bg), run_time=0.7)
        self.add(rate_bar_fill)
        self.play(rate_v.animate.set_value(440.0), run_time=1.6, rate_func=linear)

        self.at("about 7")
        self.play(FadeIn(c1_right), run_time=0.8)

        # 13.06: "1 over 7.3 gives a mean wait near 140 milliseconds."
        self.at("1 over 7")
        self.play(
            FadeOut(mult_bar_bg),
            FadeOut(mult_fill),
            FadeOut(mult_num),
            FadeOut(rate_meter),
            FadeOut(rate_bar_bg),
            FadeOut(rate_bar_fill),
            FadeIn(c2),
            FadeIn(clock),
            run_time=1.3,
        )
        cursor = clock[-1]
        preview_bar = always_redraw(
            lambda: Line([clock_x0, clock_y, 0], [cursor.get_center()[0], clock_y, 0], color=CYAN, stroke_width=10)
            if cursor.get_center()[0] > clock_x0 + 0.05
            else Line([clock_x0, clock_y, 0], [clock_x0 + 0.01, clock_y, 0], color=CYAN, stroke_width=0, stroke_opacity=0)
        )
        self.add(preview_bar)
        self.play(cursor.animate.move_to([x_140, clock_y + 0.25, 0]), run_time=2.6, rate_func=there_and_back)
        self.remove(preview_bar)

        # 19.16: "But a cell holds many G proteins."
        self.at("But a cell")
        self.play(
            LaggedStart(*[FadeIn(g, shift=DOWN * 0.05) for g in gprots[3:]], lag_ratio=0.08),
            FadeIn(masked),
            run_time=2.4,
        )

        # 22.12: "Must it wait that long for current?"
        self.at("Must it wait")
        q = question_card("Must the cell wait 140 ms?", y=3.28, color=TEXT, size=34, max_w=10.2)
        q.question.move_to([-0.5, 3.28, 0])
        self.play(swap(accel_badge, q.question, run_time=0.5))
        self.finish()


# ------------------------------------------------------------------ S05
class S05PredictPause(PredictPause):
    QUESTION = "Must the cell wait 140 ms?"
    CARD = {"y": 3.28, "color": TEXT, "size": 34, "max_w": 10.2}
    RING_AT = (5.9, 3.28, 0)
    SECONDS = 4.5

    def backdrop(self):
        return build_population_backdrop()


# ------------------------------------------------------------------ S06
class S06RevealAndGuidingIdea(SpokenScene):
    def construct(self):
        bg = build_population_backdrop()
        mem, receptors, ligs, gprots, c1, c2, clock, masked = bg
        q_old = fit_text("Must the cell wait 140 ms?", max_w=10.2, size=34, color=TEXT, max_lines=2).move_to([-0.5, 3.28, 0])

        # Seed 3 gives exact 2/20 (10%) flipped by 14.4 ms: [9.1, 14.1, 15.1, ...]
        rng = np.random.default_rng(3)
        flip_ms = np.sort(rng.exponential(1000.0 / K_FIT, size=20))
        t_ms = ValueTracker(0.0)

        g_live = VGroup()
        for idx in range(20):
            r, c = divmod(idx, 10)
            gx, gy = GRID_X0 + c * GRID_DX, GRID_YS[r]
            ft = float(flip_ms[idx])

            def mk_g(gx=gx, gy=gy, ft=ft):
                on = t_ms.get_value() >= ft
                col = GREEN if on else RED
                lbl = "GTP" if on else "GDP"
                box = RoundedRectangle(
                    corner_radius=0.09,
                    width=0.84,
                    height=0.36,
                    stroke_color=PURPLE,
                    stroke_width=2.6,
                    fill_color=PURPLE,
                    fill_opacity=0.50 if on else 0.34,
                ).move_to([gx, gy, 0])
                tag = M(lbl, 22, col).move_to(box)
                return VGroup(box, tag)

            g_live.add(always_redraw(mk_g))

        plot = Plot(
            box=(-5.4, 0.75, -1.85, -0.15),
            xr=(0, 400),
            yr=(0, 1.0),
            xticks=[0, 140, 400],
            yticks=[(0, "0%"), (0.5, "50%"), (1.0, "100%")],
            xlabel="time (ms)",
            ylabel="fraction on",
            color=TEXT,
            size=24,
            label_size=26,
        )
        frac_fn = lambda ms: 1.0 - np.exp(-K_FIT * (ms / 1000.0))
        live_frac = plot.live_curve(frac_fn, t_ms, color=GREEN, width=6.5)
        dot_frac = always_redraw(
            lambda: Dot(plot.pt(t_ms.get_value(), frac_fn(t_ms.get_value())), radius=0.09, color=GREEN, stroke_color=TEXT, stroke_width=2.5)
            if t_ms.get_value() >= 6.0
            else VGroup()
        )
        formula = M("f(t) = 1 − e^(−7.3t)", 28, GREEN).move_to([-1.2, 0.2, 0])
        mean_line = DashedLine(plot.pt(140, 0), plot.pt(140, 1.0), color=GOLD, stroke_width=3.0)
        mean_lbl = M("mean 140 ms", 24, GOLD).move_to([-1.9, -2.95, 0])
        clock_num = counter("t = {:.0f} ms", t_ms, at=[-4.9, -2.95, 0], size=28, color=CYAN)

        p_curr = Plot(
            box=(2.2, 6.0, -1.85, -0.15),
            xr=(0, 400),
            yr=(0, 1.0),
            xticks=[0, 200, 400],
            yticks=[(0, "0"), (1, "max")],
            xlabel="ms",
            ylabel="K+ current",
            color=BLUE,
            size=24,
            label_size=26,
        )
        curr_fn = lambda ms: (1.0 - np.exp(-K_FIT * max(0.0, ms - 12.0) / 1000.0)) ** 2.2
        live_curr = p_curr.live_curve(curr_fn, t_ms, color=BLUE, width=6.5)

        self.add(mem, receptors, ligs, g_live, c1, c2, clock, masked, q_old)

        # 0.00: "No."
        self.at("Now")
        ans = fit_text("No: early fraction starts current", max_w=10.8, size=34, color=GREEN, max_lines=1).move_to([0.0, 3.28, 0])
        self.play(
            FadeOut(q_old),
            FadeOut(c1),
            FadeOut(c2),
            FadeOut(clock),
            FadeOut(masked),
            run_time=0.35,
        )
        self.play(
            FadeIn(ans),
            FadeIn(plot),
            FadeIn(mean_line),
            FadeIn(mean_lbl),
            FadeIn(clock_num),
            FadeIn(p_curr),
            run_time=0.5,
        )

        # 1.80: "The fraction on by time t is 1 minus e to the minus 7.3 t."
        self.at("the fraction on")
        self.add(live_frac, dot_frac, live_curr)
        self.play(FadeIn(formula), run_time=0.6)
        self.play(t_ms.animate.set_value(14.4), run_time=4.8, rate_func=linear)

        # 7.86: "That reaches 10 percent at about 14 milliseconds, and current can start."
        self.at("That reaches 10")
        pt14 = plot.pt(14.4, frac_fn(14.4))
        mark_14 = DashedLine(plot.pt(14.4, 0), pt14, color=GOLD, stroke_width=3)
        lbl_14 = M("10% on at ~14 ms", 26, GOLD).move_to([-1.25, -1.35, 0])
        arrow_14 = Arrow(lbl_14.get_left() + LEFT * 0.1, pt14 + RIGHT * 0.12, color=GOLD, stroke_width=3, buff=0.05)
        self.play(Create(mark_14), FadeIn(lbl_14), Create(arrow_14), run_time=0.9)

        self.at("current can start")
        self.play(t_ms.animate.set_value(95.0), run_time=2.0, rate_func=linear)

        # 13.90: "Channels need several G-protein pieces, a little extra delay."
        self.at("Channels need several")
        girk_ch = make_girk(center=(5.1, 2.12, 0), h=0.82, w=0.25, open_state=True)
        bg_pieces = VGroup(*[Dot(radius=0.1, color=PURPLE).move_to([4.7 + i * 0.26, 1.42, 0]) for i in range(4)])
        bg_lbl = T("4 βγ pieces\n(schematic)", 24, PURPLE, line_spacing=0.85).move_to([5.1, 0.88, 0])
        ions_k = make_ion_stream(5.1, 2.65, 1.65, BLUE, UP, n=6)
        self.play(FadeIn(girk_ch), FadeIn(bg_pieces), FadeIn(bg_lbl), run_time=0.7)
        self.add(ions_k)
        self.play(t_ms.animate.set_value(400.0), run_time=3.5, rate_func=linear)

        # 18.56: "So steps set when: waits add up, and the slowest sets the pace."
        self.at("So steps set")
        banner = boxed_label("Steps set when: waits add up, slowest sets the pace", color=GOLD, size=26, fill_opacity=0.26).move_to([-2.0, -2.95, 0])
        live_frac.clear_updaters()
        dot_frac.clear_updaters()
        self.play(
            FadeOut(plot),
            FadeOut(live_frac),
            FadeOut(dot_frac),
            FadeOut(formula),
            FadeOut(mean_line),
            FadeOut(mean_lbl),
            FadeOut(mark_14),
            FadeOut(lbl_14),
            FadeOut(arrow_14),
            FadeOut(clock_num),
            run_time=0.35,
        )
        self.play(FadeIn(banner), run_time=0.5)
        self.finish()


# ------------------------------------------------------------------ S07
class S07SlowRoutesSinglePass(SpokenScene):
    def construct(self):
        mem = make_membrane(y=1.25)
        stem_l = make_rtk_stem(-1.8, y_mem=1.25, color=ORANGE, scale=1.32)
        stem_r = make_rtk_stem(1.8, y_mem=1.25, color=ORANGE, scale=1.32)
        lig = make_ligand(GOLD, radius=0.22).move_to([0.0, 2.58, 0])

        head = T("Single-pass kinase receptors", 32, ORANGE).move_to([0.0, 3.25, 0])
        lbl_enz = T("phosphate-attaching\nenzyme", 26, ORANGE, line_spacing=0.85).move_to([-4.65, -0.05, 0])

        def _mk_arr_enz():
            return Arrow(
                lbl_enz.get_right() + RIGHT * 0.06,
                stem_l.kinase.get_left() + LEFT * 0.06,
                color=ORANGE,
                stroke_width=3.5,
                buff=0.06,
            )

        arr_enz = _mk_arr_enz()

        timeline = make_timeline(y=-2.45, x0=-5.8, x1=5.2)
        tag = scope_tag("schematic")

        bar_t = ValueTracker(0.0)
        bar_bg = RoundedRectangle(corner_radius=0.06, width=8.8, height=0.28, stroke_color=GREY, stroke_width=2).move_to([-1.4, -2.45, 0])
        bar_orange = always_redraw(
            lambda: Rectangle(width=max(0.04, 8.8 * bar_t.get_value()), height=0.26, stroke_width=0, fill_color=ORANGE, fill_opacity=0.85)
            .align_to(bar_bg, LEFT)
            .set_y(-2.45)
        )
        bar_lbl = M("seconds to minutes", 28, ORANGE).move_to([-1.4, -2.95, 0])

        self.add(mem, stem_l, stem_r, lig, timeline, bar_bg, tag)
        self.add(bar_orange)

        # 0.00: "Now slower designs."
        self.at("Now slower designs")
        self.play(FadeIn(head), bar_t.animate.set_value(0.18), run_time=2.2, rate_func=linear)

        # 2.74: "Single-pass kinase receptors cross the membrane once and carry a phosphate-attaching enzyme."
        self.at("Single pass kinase")
        once_lbl = T("crosses once", 28, TEXT).move_to([-4.3, 1.95, 0])
        self.play(FadeIn(once_lbl), FadeIn(lbl_enz), Create(arr_enz), run_time=1.0)
        arr_enz.add_updater(lambda m: m.become(_mk_arr_enz()))
        self.play(
            bar_t.animate.set_value(0.45),
            lig.animate.shift(DOWN * 0.25),
            stem_l.animate.shift(RIGHT * 0.45),
            stem_r.animate.shift(LEFT * 0.45),
            run_time=4.8,
            rate_func=linear,
        )

        # 9.96: "A ligand pairs chains, or rearranges a pair,"
        self.at("A ligand pairs")
        arr_enz.clear_updaters()
        self.play(
            FadeOut(lbl_enz),
            FadeOut(arr_enz),
            FadeOut(once_lbl),
            lig.animate.move_to([0.0, 2.1, 0]),
            stem_l.animate.shift(RIGHT * 0.85),
            stem_r.animate.shift(LEFT * 0.85),
            bar_t.animate.set_value(0.58),
            run_time=1.4,
        )

        self.at("rearranges a pair")
        rearr_lbl = T("pair or rearrange", 28, GOLD).move_to([-4.0, 2.1, 0])
        self.play(
            FadeIn(rearr_lbl),
            Rotate(stem_l.kinase, angle=0.14),
            Rotate(stem_r.kinase, angle=-0.14),
            run_time=1.0,
        )

        # 12.94: "so the enzymes tag each other and recruit partners."
        self.at("so the enzymes")
        p1_dot = Dot(radius=0.14, color=GOLD, stroke_color=TEXT, stroke_width=2.0).move_to([-0.85, -0.58, 0])
        p1_lbl = T("P", 26, GOLD).next_to(p1_dot, DOWN, buff=0.1)
        p2_dot = Dot(radius=0.14, color=GOLD, stroke_color=TEXT, stroke_width=2.0).move_to([0.85, -0.58, 0])
        p2_lbl = T("P", 26, GOLD).next_to(p2_dot, DOWN, buff=0.1)
        self.play(FadeIn(p1_dot), FadeIn(p1_lbl), FadeIn(p2_dot), FadeIn(p2_lbl), bar_t.animate.set_value(0.75), run_time=1.2)

        self.at("and recruit partners")
        partner = boxed_label("partner", color=TEXT, size=28, fill_opacity=0.28).move_to([3.2, -0.15, 0])
        arr_p = Arrow(partner.get_left() + LEFT * 0.1, [1.28, -0.15, 0], color=TEXT, stroke_width=3.5)
        self.play(FadeIn(partner), Create(arr_p), bar_t.animate.set_value(0.88), run_time=1.4)

        # 17.18: "Those steps take seconds to minutes."
        self.at("Those steps take")
        self.play(bar_t.animate.set_value(1.0), FadeIn(bar_lbl), run_time=1.8, rate_func=linear)
        self.finish()


# ------------------------------------------------------------------ S08
class S08NuclearParadoxSolved(SpokenScene):
    def construct(self):
        mem = make_membrane(y=2.35)
        nuc = make_nucleus_arc(center=(0.0, -1.75, 0), rx=5.7, ry=2.82)
        est = make_ligand(AMBER, radius=0.20).move_to([-3.2, 3.05, 0])
        est_lbl = T("estradiol", 28, AMBER).next_to(est, LEFT, buff=0.25)

        nuc_rec = make_nuclear_receptor(center=(-2.8, -0.55, 0), occupied=False)
        nr_lbl = T("nuclear receptor", 26, CORAL).move_to([-0.55, -0.55, 0])

        dna = VGroup(
            Line([-4.3, -1.2, 0], [4.5, -1.2, 0], color=TEXT, stroke_width=4.5),
            Line([-4.3, -1.36, 0], [4.5, -1.36, 0], color=TEXT, stroke_width=4.5),
        )
        dna_lbl = T("DNA", 28, TEXT).next_to(dna, LEFT, buff=0.2)

        timeline = make_timeline(y=-2.55, x0=-5.8, x1=5.4)
        cyan_bar = Line([-5.8, -2.55, 0], [-5.25, -2.55, 0], color=CYAN, stroke_width=15)
        cyan_lbl = M("channel < 1 ms", 24, CYAN).next_to(cyan_bar, DOWN, buff=0.14).align_to([-5.8, 0, 0], LEFT)
        tag = scope_tag("schematic")

        coral_t = ValueTracker(0.0)
        coral_bar = always_redraw(
            lambda: Line([-4.6, -2.55, 0], [-4.6 + 9.4 * coral_t.get_value(), -2.55, 0], color=CORAL, stroke_width=15)
            if coral_t.get_value() > 0.01
            else VGroup()
        )

        self.add(mem, nuc, est, est_lbl, nuc_rec, nr_lbl, dna, dna_lbl, timeline, cyan_bar, cyan_lbl, tag)
        self.add(coral_bar)

        # 0.00: "Now the puzzle."
        self.at("Now the puzzle")
        puzzle_lbl = T("Why does no relay still take hours?", 30, GOLD).move_to([1.6, 3.1, 0])
        self.play(FadeIn(puzzle_lbl), run_time=1.4)

        # 2.52: "Estradiol slips inside and binds its nuclear receptor, skipping every relay."
        self.at("Estradiol slips inside")
        self.play(
            FadeOut(est_lbl),
            est.animate.move_to([-3.2, 1.5, 0]),
            run_time=1.3,
        )
        no_relay = T("no relay", 28, TEXT).move_to([-1.6, 1.55, 0])
        self.play(
            est.animate.move_to([-2.8, -0.55, 0]),
            FadeIn(no_relay),
            run_time=1.6,
        )
        self.at("skipping every relay")
        nuc_occ = make_nuclear_receptor(center=(-2.8, -0.82, 0), occupied=True)
        self.play(
            FadeOut(nr_lbl),
            Transform(nuc_rec, nuc_occ),
            est.animate.move_to([-2.8, -0.82, 0]),
            run_time=1.0,
        )

        # 8.60: "But its output is new RNA within minutes,"
        self.at("But its output")
        rna_strips = VGroup(*[
            Line([-1.4 + i * 0.45, -1.2, 0], [-1.0 + i * 0.45, -0.6, 0], color=TEXT, stroke_width=6.0)
            for i in range(4)
        ])
        rna_lbl = T("new RNA\n(minutes)", 26, TEXT, line_spacing=0.85).move_to([-0.5, 0.02, 0])
        self.play(
            LaggedStart(*[Create(s) for s in rna_strips], lag_ratio=0.18),
            FadeIn(rna_lbl),
            coral_t.animate.set_value(0.35),
            run_time=2.5,
        )

        # 11.76: "then new protein over tens of minutes to hours."
        self.at("then new protein")
        prots = VGroup(*[
            RoundedRectangle(corner_radius=0.08, width=0.52, height=0.44, stroke_color=CORAL, stroke_width=3.2, fill_color=CORAL, fill_opacity=0.58)
            .move_to([1.65 + i * 0.65, -0.78, 0])
            for i in range(4)
        ])
        prot_lbl = T("new protein\n(tens of min–hours)", 26, CORAL, line_spacing=0.85).move_to([2.4, -0.1, 0])
        coral_lbl = M("tens of min to hours", 26, CORAL).move_to([0.2, -3.02, 0])
        self.play(
            LaggedStart(*[FadeIn(p, shift=UP * 0.12) for p in prots], lag_ratio=0.18),
            FadeIn(prot_lbl),
            coral_t.animate.set_value(1.0),
            FadeIn(coral_lbl),
            run_time=3.2,
            rate_func=linear,
        )

        # 15.68: "One slow step outweighs every skipped relay."
        self.at("One slow step")
        takeaway = T("one slow step > skipped relays", 30, GOLD).move_to([1.6, 3.1, 0])
        self.play(swap(puzzle_lbl, takeaway, run_time=0.5))
        self.finish()


# ------------------------------------------------------------------ S09
class S09DurationOffSteps(SpokenScene):
    def construct(self):
        head = T("Slowest off step sets duration", 34, TEXT).move_to([0.0, 3.2, 0])
        t0_line = DashedLine([-1.3, -2.6, 0], [-1.3, 2.75, 0], color=GREY, stroke_width=3.5)
        t0_lbl = T("ligand clears", 26, TEXT).next_to(t0_line, DOWN, buff=0.12)
        tag = scope_tag("schematic")

        mem1 = make_membrane(y=1.9, x0=-6.1, x1=-2.2, gap=0.1)
        chan1 = make_nicotinic_channel(center=(-4.2, 1.9, 0), w=0.18, h=0.72, open_state=True)
        ach1 = make_ligand(GOLD, radius=0.12).move_to([-4.2, 2.42, 0])
        r1_lbl = T("muscle channel", 26, CYAN).move_to([-4.2, 1.15, 0])

        mem2 = make_membrane(y=0.15, x0=-6.1, x1=-2.2, gap=0.1)
        gpcr2 = make_gpcr(center=(-5.1, 0.15, 0), h=0.7, w=0.09, dx=0.12, active=True)
        ach2 = make_ligand(GOLD, radius=0.12).move_to([-5.1, 0.65, 0])
        g2 = make_g_protein(center=(-3.9, -0.55, 0), gtp=True, compact=True)
        girk2 = make_girk(center=(-2.7, 0.15, 0), h=0.7, w=0.22, open_state=True)

        est3 = make_ligand(AMBER, radius=0.12).move_to([-5.3, -1.75, 0])
        nr3 = make_nuclear_receptor(center=(-4.5, -1.75, 0), occupied=True)
        prot3 = VGroup(*[
            RoundedRectangle(corner_radius=0.06, width=0.4, height=0.38, stroke_color=CORAL, stroke_width=2.8, fill_color=CORAL, fill_opacity=0.55)
            .move_to([-3.35 + i * 0.5, -1.75, 0])
            for i in range(2)
        ])
        r3_lbl = T("new protein", 26, CORAL).move_to([-3.1, -2.3, 0])

        # Pre-clear ON bars (left of ligand-clears line at x = -1.3) + post-clear OFF bars
        pre_t = ValueTracker(0.0)
        pre1 = always_redraw(lambda: Line([-2.0, 1.9, 0], [-2.0 + 0.7 * pre_t.get_value(), 1.9, 0], color=CYAN, stroke_width=16) if pre_t.get_value() > 0.02 else VGroup())
        pre2 = always_redraw(lambda: Line([-2.0, 0.0, 0], [-2.0 + 0.7 * pre_t.get_value(), 0.0, 0], color=BLUE, stroke_width=16) if pre_t.get_value() > 0.02 else VGroup())
        pre3 = always_redraw(lambda: Line([-2.0, -1.75, 0], [-2.0 + 0.7 * pre_t.get_value(), -1.75, 0], color=CORAL, stroke_width=16) if pre_t.get_value() > 0.02 else VGroup())

        b1_t = ValueTracker(0.0)
        b1 = always_redraw(lambda: Line([-1.3, 1.9, 0], [-1.3 + 0.65 * b1_t.get_value(), 1.9, 0], color=CYAN, stroke_width=18) if b1_t.get_value() > 0.02 else VGroup())
        b1_txt = M("~1 ms", 28, CYAN).move_to([-0.4, 1.9, 0], aligned_edge=LEFT)

        b2_t = ValueTracker(0.0)
        b2 = always_redraw(lambda: Line([-1.3, 0.0, 0], [-1.3 + 3.2 * b2_t.get_value(), 0.0, 0], color=BLUE, stroke_width=18) if b2_t.get_value() > 0.02 else VGroup())
        b2_txt = M("seconds (splits GTP)", 28, BLUE).move_to([2.15, 0.0, 0], aligned_edge=LEFT)

        b3_t = ValueTracker(0.0)
        b3 = always_redraw(lambda: Line([-1.3, -1.75, 0], [-1.3 + 6.7 * b3_t.get_value(), -1.75, 0], color=CORAL, stroke_width=18) if b3_t.get_value() > 0.02 else VGroup())
        b3_txt = T("outlasts the hormone", 28, CORAL).move_to([2.6, -2.25, 0])

        self.add(head, t0_line, t0_lbl, tag,
                 mem1, chan1, ach1, r1_lbl, pre1, b1,
                 mem2, gpcr2, ach2, g2, girk2, pre2, b2,
                 est3, nr3, prot3, r3_lbl, pre3, b3)

        # 0.00: "Duration follows the same rule."
        self.at("Duration follows")
        ions1 = make_ion_stream(-4.2, 2.35, 1.35, CYAN, DOWN, n=6)
        ions2 = make_ion_stream(-2.7, 0.55, -0.35, BLUE, UP, n=6)
        self.add(ions1, ions2)
        self.play(pre_t.animate.set_value(0.45), run_time=2.3, rate_func=linear)

        # 3.00: "Signals last until their slowest off-step finishes."
        self.at("Signals last until")
        rule_sub = T("each stays ON until its off step finishes", 28, GOLD).move_to([2.15, 2.55, 0])
        self.play(FadeIn(rule_sub), pre_t.animate.set_value(1.0), run_time=3.5, rate_func=linear)

        # 7.32: "Muscle current decays in about a millisecond once acetylcholine clears."
        self.at("Muscle current decays")
        chan1_closed = make_nicotinic_channel(center=(-4.2, 1.9, 0), w=0.18, h=0.72, open_state=False)
        ions1.clear_updaters()
        self.play(
            ach1.animate.shift(UP * 0.6).set_opacity(0),
            FadeOut(ions1),
            Transform(chan1, chan1_closed),
            b1_t.animate.set_value(1.0),
            FadeIn(b1_txt),
            run_time=2.2,
        )

        # 12.88: "G-proteins stay on for seconds until they split GTP."
        self.at("G proteins stay")
        gpcr2_idle = make_gpcr(center=(-5.1, 0.15, 0), h=0.7, w=0.09, dx=0.12, active=False)
        self.play(
            ach2.animate.shift(LEFT * 0.5 + UP * 0.25).set_opacity(0),
            Transform(gpcr2, gpcr2_idle),
            b2_t.animate.set_value(1.0),
            run_time=2.4,
            rate_func=linear,
        )
        g2_off = make_g_protein(center=(-3.9, -0.55, 0), gtp=False, compact=True)
        girk2_closed = make_girk(center=(-2.7, 0.15, 0), h=0.7, w=0.22, open_state=False)
        ions2.clear_updaters()
        self.play(
            swap(g2.badge, g2_off.badge, run_time=0.4),
            Transform(girk2, girk2_closed),
            FadeOut(ions2),
            FadeIn(b2_txt),
            run_time=1.0,
        )

        # 16.38: "New proteins can keep a gene program running after the hormone leaves."
        self.at("New proteins can")
        nr3_idle = make_nuclear_receptor(center=(-4.5, -1.75, 0), occupied=False)
        self.play(
            est3.animate.shift(LEFT * 0.5 + UP * 0.6).set_opacity(0),
            Transform(nr3, nr3_idle),
            b3_t.animate.set_value(1.0),
            FadeIn(b3_txt),
            run_time=4.8,
            rate_func=linear,
        )
        self.finish()


# ------------------------------------------------------------------ S10
class S10WhereRuleStops(SpokenScene):
    def construct(self):
        head = T("Where the rule stops", 34, TEXT).move_to([0.0, 3.25, 0])
        tag = scope_tag("schematic")

        p1 = RoundedRectangle(corner_radius=0.16, width=4.0, height=5.25, stroke_color=GREEN, stroke_width=3.0, fill_color=BG, fill_opacity=0.92).move_to([-4.2, -0.05, 0])
        p2 = RoundedRectangle(corner_radius=0.16, width=4.0, height=5.25, stroke_color=CYAN, stroke_width=3.0, fill_color=BG, fill_opacity=0.92).move_to([0.0, -0.05, 0])
        p3 = RoundedRectangle(corner_radius=0.16, width=4.0, height=5.25, stroke_color=AMBER, stroke_width=3.0, fill_color=BG, fill_opacity=0.92).move_to([4.2, -0.05, 0])

        t1 = T("1. high gain", 28, GREEN).move_to([-4.2, 2.2, 0])
        t2 = T("2. potency ≠ speed", 28, CYAN).move_to([0.0, 2.2, 0])
        t3 = T("3. rapid surface?", 28, AMBER).move_to([4.2, 2.2, 0])

        # Panel 1: high gain vs low gain quadratic curves + live output level bars
        rec1 = make_gpcr(center=(-4.5, 1.48, 0), h=0.48, w=0.07, dx=0.1, active=True)
        enzs = VGroup(*[
            RoundedRectangle(corner_radius=0.06, width=0.54, height=0.28, stroke_color=GREEN, stroke_width=2.5, fill_color=GREEN, fill_opacity=0.48)
            .move_to([-5.35 + i * 0.85, 0.82, 0])
            for i in range(3)
        ])
        fan_arrows = VGroup(*[Line([-4.5, 1.22, 0], e.get_top() + UP * 0.04, color=GREEN, stroke_width=2.5) for e in enzs])
        plot1 = Plot(box=(-5.5, -3.05, -1.62, 0.25), xr=(0, 3.0), yr=(0, 2.0), xticks=[0, 1, 2, 3], yticks=[(0, "0"), (1, "1")],
                     xlabel="time", color=TEXT, size=22, label_size=24)
        thresh_line = plot1.hline(1.0, label=None, color=GOLD, dashed=True)
        thresh_lbl = T("threshold", 22, GOLD).move_to([plot1.pt(1.88, 1.0)[0], plot1.pt(0, 1.0)[1] + 0.28, 0])
        t_g = ValueTracker(0.0)
        low_fn = lambda x: 0.14 * x ** 2
        high_fn = lambda x: 1.8 * x ** 2
        low_curve = plot1.live_curve(low_fn, t_g, color=GREY, width=6)
        high_curve = plot1.live_curve(high_fn, t_g, color=GREEN, width=8)
        low_dot = always_redraw(
            lambda: Dot(plot1.pt(t_g.get_value(), min(2.0, low_fn(t_g.get_value()))), radius=0.09, color=GREY, stroke_color=TEXT, stroke_width=2)
            if t_g.get_value() >= 0.25
            else VGroup()
        )
        high_dot = always_redraw(
            lambda: Dot(plot1.pt(min(1.05, t_g.get_value()), min(2.0, high_fn(min(1.05, t_g.get_value())))), radius=0.1, color=GREEN, stroke_color=TEXT, stroke_width=2)
            if t_g.get_value() >= 0.25
            else VGroup()
        )
        # Live output level bars beside plot1 so both low and high gain motion stay bold
        bar_h_bg = Rectangle(width=0.22, height=1.85, stroke_color=GREEN, stroke_width=2).move_to([-2.72, -0.68, 0])
        bar_l_bg = Rectangle(width=0.22, height=1.85, stroke_color=GREY, stroke_width=2).move_to([-2.42, -0.68, 0])
        bar_h_fill = always_redraw(
            lambda: Rectangle(
                width=0.2,
                height=max(0.03, 1.83 * min(1.0, high_fn(t_g.get_value()) / 2.0)),
                stroke_width=0,
                fill_color=GREEN,
                fill_opacity=0.8,
            ).align_to(bar_h_bg, DOWN).set_x(-2.72)
        )
        bar_l_fill = always_redraw(
            lambda: Rectangle(
                width=0.2,
                height=max(0.03, 1.83 * min(1.0, low_fn(t_g.get_value()) / 2.0)),
                stroke_width=0,
                fill_color=GREY,
                fill_opacity=0.8,
            ).align_to(bar_l_bg, DOWN).set_x(-2.42)
        )

        # Panel 2: Independent potency and speed dials
        pot_v = ValueTracker(0.15)
        spd_v = ValueTracker(0.85)
        d_pot = dial(pot_v, center=[0.0, 1.05, 0], radius=0.68, label="potency", color=GOLD, fmt="", size=28)
        d_pot.remove(d_pot[3])
        d_pot[3].shift(UP * 0.35)
        d_pot.add(T("low", 22, GREY).move_to([-1.12, 1.15, 0]), T("high", 22, GREY).move_to([1.12, 1.15, 0]))
        d_spd = dial(spd_v, center=[0.0, -1.18, 0], radius=0.68, label="speed", color=CYAN, fmt="", size=28)
        d_spd.remove(d_spd[3])
        d_spd[3].shift(UP * 0.35)
        d_spd.add(T("low", 22, GREY).move_to([-1.12, -1.08, 0]), T("high", 22, GREY).move_to([1.12, -1.08, 0]))

        # Panel 3: Carried membrane + slow nuclear route + AMBER touching surface '?' above membrane
        mem3 = make_membrane(y=0.9, x0=2.4, x1=6.0, gap=0.1)
        q_surf = boxed_label("?", color=GOLD, size=26, pad=0.12, fill_opacity=0.30).move_to([4.5, 1.38, 0])
        est3 = make_ligand(AMBER, radius=0.18).move_to([3.0, 1.68, 0])
        surf_lbl = T("reported rapid\nsurface actions", 24, AMBER, line_spacing=0.9).move_to([4.2, 0.15, 0])
        nr3 = make_nuclear_receptor(center=(4.2, -1.15, 0), occupied=True)
        nr3_lbl = T("slow nuclear route", 24, CORAL).next_to(nr3, DOWN, buff=0.16)

        self.add(head, tag, p1, t1)

        # 0.00: "This rule has limits."
        self.at("This rule has")
        self.play(
            FadeIn(rec1), FadeIn(enzs), Create(fan_arrows),
            FadeIn(plot1), FadeIn(thresh_line), FadeIn(thresh_lbl),
            FadeIn(bar_h_bg), FadeIn(bar_l_bg),
            run_time=1.3,
        )
        self.add(low_curve, high_curve, low_dot, high_dot, bar_h_fill, bar_l_fill)

        # 2.80: "High enzymatic gain can buy back speed..."
        self.at("High enzymatic gain")
        self.play(t_g.animate.set_value(3.0), run_time=6.4, rate_func=linear)

        # 10.26: "Potency, how much ligand a route needs, is separate from speed."
        self.at("Potency")
        self.play(FadeIn(p2), FadeIn(t2), FadeIn(d_pot), FadeIn(d_spd), run_time=0.8)
        self.play(pot_v.animate.set_value(0.92), spd_v.animate.set_value(0.18), run_time=3.5, rate_func=linear)

        # 15.00: "And estradiol has reported rapid surface actions."
        self.at("estradiol has reported")
        self.play(FadeIn(p3), FadeIn(t3), FadeIn(mem3), FadeIn(nr3), FadeIn(nr3_lbl), FadeIn(est3), FadeIn(q_surf), run_time=0.9)
        self.play(est3.animate.move_to([3.95, 1.38, 0]), FadeIn(surf_lbl), run_time=2.2)
        self.finish()


# ------------------------------------------------------------------ S11
class S11Handoff(SpokenScene):
    def construct(self):
        mem = make_membrane(y=1.45)
        nuc = make_nucleus_arc(center=(4.6, -0.5, 0), rx=1.45, ry=1.08)
        tag = scope_tag("schematic")
        head = T("slowest on and slowest off set when", 34, TEXT).move_to([0.0, 3.2, 0])

        chan = make_nicotinic_channel(center=(-4.6, 1.45, 0), open_state=True)
        gpcr = make_gpcr(center=(-2.0, 1.45, 0), active=True)
        gprot = make_g_protein(center=(-1.0, 0.55, 0), gtp=True, compact=True)
        rtk_l = make_rtk_stem(-0.5 + 1.55, y_mem=1.45, color=ORANGE, scale=0.85)
        rtk_r = make_rtk_stem(-0.5 + 2.15, y_mem=1.45, color=ORANGE, scale=0.85)
        nr = make_nuclear_receptor(center=(4.6, -0.18, 0), occupied=True).scale(0.85)

        lbls = VGroup(
            T("channel", 26, CYAN).move_to([-4.6, 2.55, 0]),
            T("GPCR", 26, TEAL).move_to([-1.5, 2.55, 0]),
            T("single-pass", 26, ORANGE).move_to([1.35, 2.55, 0]),
            T("nuclear", 26, CORAL).move_to([4.6, 2.55, 0]),
        )

        xs = [-4.6, -1.5, 1.35, 4.6]
        cols = [CYAN, BLUE, ORANGE, CORAL]
        on_w = [0.6, 1.4, 2.1, 2.7]
        off_w = [0.6, 1.7, 2.2, 2.8]
        on_txt = ["< 1 ms", "tens of ms", "sec–min", "min–hours"]
        off_txt = ["~1 ms", "seconds", "slow", "hours+"]

        on_lbl = T("slowest on", 28, GOLD).move_to([-5.2, -0.95, 0])
        off_lbl = T("slowest off", 28, GOLD).move_to([-5.2, -2.0, 0])

        on_bars = VGroup()
        off_bars = VGroup()
        for x, c, ow, fw, ot, ft in zip(xs, cols, on_w, off_w, on_txt, off_txt):
            ob = Line([x - ow / 2, -1.35, 0], [x + ow / 2, -1.35, 0], color=c, stroke_width=15)
            ol = M(ot, 24, c).next_to(ob, DOWN, buff=0.12)
            fb = Line([x - fw / 2, -2.4, 0], [x + fw / 2, -2.4, 0], color=c, stroke_width=15)
            fl = M(ft, 24, c).next_to(fb, DOWN, buff=0.12)
            on_bars.add(VGroup(ob, ol))
            off_bars.add(VGroup(fb, fl))

        self.add(mem, nuc, tag, head, chan, gpcr, gprot, rtk_l, rtk_r, nr, lbls)
        ions_c = make_ion_stream(-4.6, 1.95, 0.75, CYAN, DOWN, n=5)
        self.add(ions_c)

        # 0.00: "Design does more than count steps."
        self.at("Design does more")
        self.play(
            LaggedStart(*[GrowFromEdge(b[0], LEFT) for b in on_bars], lag_ratio=0.15),
            LaggedStart(*[FadeIn(b[1]) for b in on_bars], lag_ratio=0.15),
            run_time=2.1,
        )

        # 3.26: "The slowest waits, on and off, set when a signal starts and how long it lasts."
        self.at("The slowest")
        self.play(FadeIn(on_lbl), run_time=0.5)
        self.at("on and off")
        self.play(
            FadeIn(off_lbl),
            LaggedStart(*[GrowFromEdge(b[0], LEFT) for b in off_bars], lag_ratio=0.15),
            LaggedStart(*[FadeIn(b[1]) for b in off_bars], lag_ratio=0.15),
            run_time=2.1,
        )
        self.play(
            Indicate(on_bars[3][0], color=GOLD, scale_factor=1.08),
            Indicate(off_bars[3][0], color=GOLD, scale_factor=1.08),
            run_time=1.0,
        )
        self.finish()


# ------------------------------------------------------------------ S12
class S12End(EndCard):
    LINE = "Steps set when: slowest on and off steps set onset and duration."
