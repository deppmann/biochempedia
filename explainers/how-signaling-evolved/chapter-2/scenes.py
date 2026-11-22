"""Why Animal Pathways Rewire Cheaply — Lesson: How Signaling Evolved (Chapter 2)

COLOUR MAP (one colour per concept, used across the entire film):
- C_RECEPTOR = "#3FB8C0" (TEAL)   : animal receptor tyrosine kinases, animal cell/writer (TK)
- C_ALT      = "#E68A3E" (AMBER)  : bacterial sensor/responder & diverged sister receptor
- C_PHOS     = "#F5D547" (YELLOW) : phosphate marks (P) and ATP donor
- C_CORE     = "#F26B5B" (CORAL)  : shared downstream core kinases, targets, and PTP eraser
- C_READER   = "#B48AE8" (VIOLET) : modular SH2 reader domains, docking motifs, regulatory DNA
- C_MEMBRANE = "#8B93A1" (GREY)   : cell membranes, axes, neutral scaffolds

ONE PICTURE OF THE WORLD (carried from scene to scene):
A cross-section of the cell membrane (horizontal double-bar over a shaded cytoplasm) with
receptors spanning from outside into the cytoplasm below, gold phosphate marks attaching to
receptor tails, violet cup-shaped reader domains latching onto marks, and signals flowing down
into coral kinase cores/targets — zooming into the tail for modular moves, comparing across
cells/species, and returning to the multi-receptor hub network at the end.

WHAT CHANGES ON SCREEN (and what it is computed from) per spoken scene:
- s01_hook: 1 animal receptor duplicates geometrically into 4 (3 teal, 1 amber) along the
  membrane while continuous signal pulses travel along spline paths into the coral core,
  and a dashed probe gap with "?" opens toward a new pathway without a new enzyme.
- s02_bacterial_relay: Responder glides in while extracellular signal triggers the amber Sensor
  kinase; gold phosphate transfers from ATP to His and then onto Responder's Asp pocket; the
  Responder's hinge angle bends from 0 deg to 34 deg (computed polygon rotation) and moves onto
  the DNA bar, flipping Genes OFF -> ON and driving an activation wave along DNA.
- s03_predict_setup: Left (bacterial) — Responder receives Asp phosphate and decays following
  computed exponential exp(-3.5 * u) with a live stability bar dropping 100% -> 0% as the
  Responder unbends; Right (animal) — Tyr phosphate holds flat at 100% with Phosphatase waiting.
- s05_reveal_readers: Animal receptor grows from right-panel scale to center stage with Tyr-P;
  two violet SH2 cup modules glide from cytoplasm and latch onto two Tyr-P sites without
  removing them, launching computed signal pulses down two coral downstream kinase chains.
- s06_modular_moves: Violet SH2 cup detaches from its old protein and snaps onto a new coral
  effector to dock on Tyr-P and fire a new branch; then a zoomed tail segment mutates one
  grey neighbor bead to a violet specificity tab, reshaping the slot so a second SH2 locks on.
- s07_regulatory_and_counts: Regulatory DNA scan links switch to Receptor gene, driving receptor
  expression in Cell A; flipping the switch expresses the unchanged receptor in Cell B with
  different coral targets; computed genome bars and ValueTracker counter climb to >100 vs 1.
- s08_choanoflagellate: Choanoflagellate beats a computed sine-wave flagellum beside a human
  cell; computed bars grow to 128 (Monosiga) vs 90 (Human) TKs; a live Writer-Reader-Eraser
  cycle writes, reads, and erases P on a substrate while TGF-beta stays absent; then a
  cladogram branches from Common ancestor to Choanoflagellate and Animals.
- s09_network_payoff: Continuous signal pulses flow from 4 receptors into the shared coral hub
  and drive a live ValueTracker output meter (100%); blocking one teal receptor drops output
  to 75%, then rerouted pulses through the amber sister restore output to 90%.
"""

from bp_parts import *

# ---- Concept colours ----
C_RECEPTOR = TEAL       # "#3FB8C0"
C_ALT = "#E68A3E"       # amber (bacterial relay & diverged sister receptor)
C_PHOS = YELLOW         # "#F5D547" (gold phosphate & ATP)
C_CORE = "#F26B5B"      # coral (shared core kinases, targets, PTP eraser)
C_READER = "#B48AE8"    # violet (SH2 readers, docking motifs, regulatory DNA)
C_MEMBRANE = GREY       # "#8B93A1"
C_CYTO = "#1B263B"      # deep navy cell-interior fill (contrast > 5:1 for all colors)
DARK_INK = "#161B26"    # high-contrast dark label on bright gold P badge


# ======================================================================
# Shared visual builders (no duplicated geometry across scenes)
# ======================================================================

def pill(text, stroke_color=TEXT, text_color=TEXT, size=24, pad=0.22, fill_opacity=0.32):
    """Rounded label box with guaranteed high-contrast TEXT (never grey letters)."""
    lab = T(text, size=size, color=text_color)
    rect = RoundedRectangle(
        corner_radius=0.14,
        width=lab.width + 2 * pad,
        height=lab.height + 2 * pad,
        stroke_color=stroke_color,
        stroke_width=2.8,
        fill_color=stroke_color,
        fill_opacity=fill_opacity,
    )
    g = VGroup(rect, lab.move_to(rect))
    g.box, g.label = rect, lab
    return g


def make_membrane(x0=-5.9, x1=5.9, y=1.8, h=0.24, color=C_MEMBRANE, cyto_bottom=None):
    """Horizontal bilayer membrane built from Lines + Polygon (optional cytoplasm shading below)."""
    g = VGroup()
    if cyto_bottom is not None:
        cyto = Polygon(
            [x0, cyto_bottom, 0], [x1, cyto_bottom, 0],
            [x1, y - h / 2, 0], [x0, y - h / 2, 0],
            stroke_width=0, fill_color=C_CYTO, fill_opacity=0.90,
        )
        g.add(cyto)
    poly = Polygon(
        [x0, y - h / 2, 0], [x1, y - h / 2, 0],
        [x1, y + h / 2, 0], [x0, y + h / 2, 0],
        stroke_width=0, fill_color=color, fill_opacity=0.28,
    )
    top = Line([x0, y + h / 2, 0], [x1, y + h / 2, 0], color=color, stroke_width=4.0)
    bot = Line([x0, y - h / 2, 0], [x1, y - h / 2, 0], color=color, stroke_width=4.0)
    g.add(poly, top, bot)
    return g


def make_phos(pos=ORIGIN, radius=0.23, with_label=True):
    """Bright gold phosphate badge with crisp dark P."""
    dot = Circle(radius=radius, stroke_width=0, fill_color=C_PHOS, fill_opacity=1.0).move_to(pos)
    if not with_label:
        return VGroup(dot)
    lbl = T("P", size=24, color=DARK_INK, weight=BOLD).move_to(dot)
    return VGroup(dot, lbl)


def make_receptor(x, y_mem, color=C_RECEPTOR, scale=1.0, tail_len=1.60, site_offsets=()):
    """Transmembrane receptor: Y-cup ligand head above membrane, stalk, and cytoplasmic tail."""
    head = Polygon(
        [-0.38, 0.56, 0], [-0.15, 0.56, 0], [0.0, 0.30, 0],
        [0.15, 0.56, 0], [0.38, 0.56, 0], [0.20, 0.14, 0],
        [0.20, -0.18, 0], [-0.20, -0.18, 0], [-0.20, 0.14, 0],
        stroke_color=color, stroke_width=3.2, fill_color=color, fill_opacity=0.40,
    )
    tail = RoundedRectangle(
        corner_radius=0.09, width=0.32, height=tail_len,
        stroke_color=color, stroke_width=3.2, fill_color=color, fill_opacity=0.35,
    ).move_to([0.0, -0.18 - tail_len / 2, 0])
    parts = VGroup(head, tail)
    sites = VGroup()
    for dy in site_offsets:
        notch = Dot(radius=0.09, color=TEXT).move_to([0.16, -0.18 - dy, 0])
        sites.add(notch)
    parts.add(sites)
    parts.scale(scale)
    parts.shift([x, y_mem, 0])
    parts.head = head
    parts.tail = tail
    parts.sites = sites
    return parts


def make_sh2_cup(color=C_READER, w=1.28, h=0.76, facing=LEFT, text="SH2"):
    """Cup-shaped reader domain whose C-jaw physically grips a gold phosphate dot."""
    jaw_x = -w / 2 + 0.24
    jaw_y = min(0.24, h * 0.32)
    pts = [
        [-w / 2, h / 2, 0], [w / 2, h / 2, 0],
        [w / 2, -h / 2, 0], [-w / 2, -h / 2, 0],
        [-w / 2, -jaw_y, 0], [jaw_x, -jaw_y, 0],
        [jaw_x, jaw_y, 0], [-w / 2, jaw_y, 0],
    ]
    if facing is RIGHT:
        pts = [[-p[0], p[1], 0] for p in pts]
    body = Polygon(*pts, stroke_color=color, stroke_width=3.2, fill_color=color, fill_opacity=0.38)
    g = VGroup(body)
    if text:
        lbl = T(text, size=24, color=TEXT, weight=BOLD).move_to([0.14 if facing is LEFT else -0.14, 0, 0])
        g.add(lbl)
        g.lbl = lbl
    g.body = body
    return g


def make_core_hub(center, label="Shared core", radius_x=1.65, radius_y=0.76, color=C_CORE):
    """Coral downstream signaling hub."""
    ell = Ellipse(
        width=radius_x * 2, height=radius_y * 2,
        stroke_color=color, stroke_width=3.5, fill_color=color, fill_opacity=0.36,
    ).move_to(center)
    txt = T(label, size=28, color=TEXT, weight=BOLD).move_to(ell)
    return VGroup(ell, txt)


def make_pulse_stream(paths_fn, active_fn, color=C_PHOS, speed=0.85, radius=0.11, count=2):
    """Computed pulse dots that continuously traverse active segments (never crossing box labels)."""
    dots = VGroup()
    state = {"t": 0.0}
    max_n = 16
    for _ in range(max_n):
        d = Dot(radius=radius, color=color).set_opacity(0)
        dots.add(d)

    def update(mob, dt):
        state["t"] += dt
        paths = paths_fn()
        actives = active_fn()
        idx = 0
        for p_idx, (pts, on) in enumerate(zip(paths, actives)):
            if not on or len(pts) < 2:
                continue
            for k in range(count):
                if idx >= max_n:
                    break
                phase = (state["t"] * speed + k / count + 0.19 * p_idx) % 1.0
                segs = [np.linalg.norm(pts[i + 1] - pts[i]) for i in range(len(pts) - 1)]
                tot = sum(segs)
                target_d = phase * tot
                acc = 0.0
                pos = pts[-1]
                for i, sl in enumerate(segs):
                    if acc + sl >= target_d:
                        u = (target_d - acc) / max(sl, 1e-6)
                        pos = pts[i] * (1 - u) + pts[i + 1] * u
                        break
                    acc += sl
                mob[idx].move_to(pos).set_opacity(0.95)
                idx += 1
        for j in range(idx, max_n):
            mob[j].set_opacity(0.0)

    dots.add_updater(update)
    return dots


def stop_pulse_stream(scene, stream):
    """Cleanly stop and remove a pulse stream so zero stray dots remain."""
    stream.clear_updaters()
    for d in stream:
        d.set_opacity(0.0)
    scene.remove(stream)


def make_responder_shape(angle_deg=0.0, color=C_ALT):
    """Two-lobe bacterial responder with an Asp pocket on the left and hinged output arm below."""
    rad = np.deg2rad(angle_deg)
    recv = Polygon(
        [-0.54, 0.56, 0], [0.54, 0.56, 0],
        [0.54, -0.06, 0], [-0.54, -0.06, 0],
        [-0.54, 0.10, 0], [-0.24, 0.10, 0],
        [-0.24, 0.40, 0], [-0.54, 0.40, 0],
        stroke_color=color, stroke_width=3.2, fill_color=color, fill_opacity=0.40,
    )
    arm_pts = np.array([
        [-0.34, -0.06, 0], [0.34, -0.06, 0],
        [0.34, -0.88, 0], [-0.34, -0.88, 0],
    ])
    c, s = np.cos(rad), np.sin(rad)
    rot = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
    pivot = np.array([0.0, -0.06, 0.0])
    arm_pts = (arm_pts - pivot) @ rot.T + pivot
    arm = Polygon(*arm_pts, stroke_color=color, stroke_width=3.2, fill_color=color, fill_opacity=0.48)
    return VGroup(recv, arm)


def make_sensor_kinase(x=-2.2, y_mem=1.85, color=C_ALT):
    """Bacterial membrane sensor kinase with extracellular head, cytoplasmic stalk, and His notch."""
    head = RoundedRectangle(
        corner_radius=0.14, width=0.92, height=0.54,
        stroke_color=color, stroke_width=3.2, fill_color=color, fill_opacity=0.40,
    ).move_to([x, y_mem + 0.48, 0])
    pts = [
        [x - 0.36, y_mem + 0.22, 0],
        [x + 0.36, y_mem + 0.22, 0],
        [x + 0.36, 0.58, 0],
        [x + 0.10, 0.58, 0],
        [x + 0.10, 0.22, 0],
        [x + 0.36, 0.22, 0],
        [x + 0.36, -0.30, 0],
        [x + 0.62, -0.50, 0],
        [x + 0.62, -1.08, 0],
        [x - 0.62, -1.08, 0],
        [x - 0.62, -0.50, 0],
        [x - 0.36, -0.30, 0],
    ]
    body = Polygon(*pts, stroke_color=color, stroke_width=3.2, fill_color=color, fill_opacity=0.36)
    g = VGroup(head, body)
    g.his_pos = np.array([x + 0.54, 0.40, 0.0])
    g.fold_center = np.array([x, -0.78, 0.0])
    g.head_pos = np.array([x, y_mem + 0.48, 0.0])
    return g


def make_choanoflagellate(center=(-3.8, 0.25, 0), color=C_RECEPTOR):
    """Schematic collared choanoflagellate cell with microvilli collar."""
    cx, cy, _ = center
    body = Ellipse(width=1.95, height=2.45, stroke_color=color, stroke_width=3.5, fill_color=color, fill_opacity=0.36)
    body.move_to([cx, cy - 0.25, 0])
    collar = VGroup()
    for dx in np.linspace(-0.60, 0.60, 7):
        p0 = np.array([cx + dx * 0.65, cy + 0.80, 0])
        p1 = np.array([cx + dx * 1.20, cy + 1.66, 0])
        collar.add(Line(p0, p1, color=color, stroke_width=3.0))
    collar_rim = ArcBetweenPoints(
        [cx - 0.70, cy + 1.66, 0], [cx + 0.70, cy + 1.66, 0],
        angle=-0.4, color=color, stroke_width=3.0,
    )
    nuc = Circle(radius=0.32, color=TEXT, stroke_width=2.5, fill_color=TEXT, fill_opacity=0.22).move_to([cx, cy - 0.45, 0])
    g = VGroup(body, collar, collar_rim, nuc)
    g.flag_base = np.array([cx, cy + 0.90, 0])
    g.body = body
    return g


# ======================================================================
# Scene 00: Title Card
# ======================================================================
class S00Title(TitleCard):
    LESSON = "How Signaling Evolved"
    TITLE = "Why Animal Pathways Rewire Cheaply"


# ======================================================================
# Scene 01: Hook — Copied receptors over a shared core
# ======================================================================
class S01Hook(SpokenScene):
    def construct(self):
        y_mem = 1.65
        mem = make_membrane(-5.9, 5.9, y_mem, cyto_bottom=-2.85)
        mem_lbl = T("Animal cell membrane", size=28, color=TEXT, weight=BOLD).move_to([-1.8, y_mem + 1.02, 0])
        r0 = make_receptor(0.0, y_mem, color=C_RECEPTOR, scale=1.0, tail_len=1.30)
        core = make_core_hub([0.0, -1.65, 0], label="Shared core")
        tag = scope_tag("schematic")

        # Beat 1: "In the first film"
        self.at("In the first film")
        line0 = Line([0.0, y_mem - 1.48, 0], [0.0, -0.89, 0], color=C_RECEPTOR, stroke_width=3.5)
        self.add(mem, tag)
        self.play(FadeIn(mem_lbl), FadeIn(r0), FadeIn(core), Create(line0), run_time=0.8)

        # Beat 2: "duplication multiplied"
        self.at("duplication multiplied")
        r1 = make_receptor(-3.6, y_mem, color=C_RECEPTOR, scale=1.0, tail_len=1.30)
        r2 = make_receptor(-1.6, y_mem, color=C_RECEPTOR, scale=1.0, tail_len=1.30)
        r3 = make_receptor(0.4, y_mem, color=C_RECEPTOR, scale=1.0, tail_len=1.30)
        r4 = make_receptor(2.7, y_mem, color=C_ALT, scale=1.0, tail_len=1.30)
        w1 = Line([-3.6, y_mem - 1.48, 0], [-2.0, -1.00, 0], color=C_RECEPTOR, stroke_width=3.5)
        w2 = Line([-1.6, y_mem - 1.48, 0], [-1.3, -0.89, 0], color=C_RECEPTOR, stroke_width=3.5)
        w3 = Line([0.4, y_mem - 1.48, 0], [-0.7, -0.89, 0], color=C_RECEPTOR, stroke_width=3.5)

        p_stream = make_pulse_stream(
            lambda: [
                np.array([[-3.6, y_mem - 1.48, 0], [-2.0, -1.00, 0]]),
                np.array([[-1.6, y_mem - 1.48, 0], [-1.3, -0.89, 0]]),
                np.array([[0.4, y_mem - 1.48, 0], [-0.7, -0.89, 0]]),
            ],
            lambda: [True, True, True],
            color=C_PHOS, speed=0.9, count=2,
        )
        self.play(
            ReplacementTransform(r0, r1),
            FadeOut(line0),
            FadeIn(r2), FadeIn(r3), FadeIn(r4),
            core.animate.shift(LEFT * 1.1),
            Create(w1), Create(w2), Create(w3),
            run_time=1.4,
        )
        self.add(p_stream)

        # Beat 3: "How does a copied"
        self.at("How does a copied")
        copy_lbl = T("Copied receptor", size=28, color=C_ALT, weight=BOLD).move_to([3.3, y_mem + 1.02, 0])
        new_path = make_core_hub([3.5, -1.65, 0], label="New pathway", radius_x=1.65, radius_y=0.72, color=C_ALT)
        q_circ = Circle(radius=0.34, color=C_PHOS, stroke_width=3, fill_color=BG, fill_opacity=0.98).move_to([3.0, -0.25, 0])
        q_mark = T("?", size=30, color=C_PHOS, weight=BOLD).move_to(q_circ)
        gap_top = DashedLine([2.7, y_mem - 1.48, 0], [2.88, 0.14, 0], color=C_PHOS, stroke_width=3.5, dash_length=0.12)
        gap_bot = DashedLine([3.12, -0.64, 0], [3.35, -0.92, 0], color=C_PHOS, stroke_width=3.5, dash_length=0.12)
        self.play(FadeIn(copy_lbl), FadeIn(new_path), Create(gap_top), Create(gap_bot), FadeIn(q_circ), FadeIn(q_mark), run_time=1.0)

        # Beat 4: "without inventing a new"
        self.at("without inventing a new")
        no_x = T("×", size=34, color=RED, weight=BOLD)
        no_enz = pill("New enzyme", RED, size=24)
        no_badge = VGroup(no_x, no_enz).arrange(RIGHT, buff=0.15).move_to([4.85, 0.25, 0])
        self.play(FadeIn(no_badge), run_time=0.8)

        # Beat 5: "Start with a simpler"
        self.at("Start with a simpler")
        stop_pulse_stream(self, p_stream)
        world = VGroup(mem, mem_lbl, r1, r2, r3, r4, w1, w2, w3, core, copy_lbl, new_path, gap_top, gap_bot, q_circ, q_mark, no_badge)
        bact_mem = make_membrane(-5.9, 5.9, 1.85, cyto_bottom=-2.65)
        bact_lbl = T("Bacterial two-component relay", size=30, color=C_ALT, weight=BOLD).move_to([0, HEAD_Y, 0])
        bact_sensor = make_sensor_kinase(x=-2.2, y_mem=1.85, color=C_ALT)
        bact_grp = VGroup(bact_mem, bact_lbl, bact_sensor)
        self.play(FadeOut(world, run_time=0.5), FadeIn(bact_grp, run_time=0.7))
        self.finish()


# ======================================================================
# Scene 02: Bacterial Two-Component Relay
# ======================================================================
class S02BacterialRelay(SpokenScene):
    def construct(self):
        y_mem = 1.85
        mem = make_membrane(-5.8, 5.8, y_mem, cyto_bottom=-2.65)
        sensor = make_sensor_kinase(x=-2.2, y_mem=y_mem, color=C_ALT)
        sensor_lbl = T("Sensor kinase", size=28, color=C_ALT, weight=BOLD).move_to([-4.35, 1.25, 0])
        his_lbl = T("His", size=24, color=TEXT, weight=BOLD).move_to([-2.95, 0.88, 0])

        dna_line = VGroup(
            Line([-4.8, -2.08, 0], [5.0, -2.08, 0], color=C_MEMBRANE, stroke_width=4),
            Line([-4.8, -2.23, 0], [5.0, -2.23, 0], color=C_MEMBRANE, stroke_width=4),
        )
        dna_lbl = T("DNA", size=24, color=TEXT, weight=BOLD).move_to([-5.38, -2.15, 0])
        sw_box = pill("Genes: OFF", GREY, text_color=TEXT, size=24).move_to([3.3, -1.42, 0])
        sw_tick = Line([3.3, -1.78, 0], [3.3, -2.05, 0], color=GREY, stroke_width=3)

        head = T("Bacterial two-component relay", size=30, color=C_ALT, weight=BOLD).move_to([0, HEAD_Y, 0])
        tag = scope_tag("schematic")

        bend_t = ValueTracker(0.0)
        resp_pos = ValueTracker(4.5)
        resp_y = ValueTracker(0.05)
        resp = always_redraw(
            lambda: make_responder_shape(angle_deg=bend_t.get_value()).move_to([resp_pos.get_value(), resp_y.get_value(), 0])
        )
        resp_lbl = always_redraw(
            lambda: T("Responder", size=28, color=C_ALT, weight=BOLD).move_to([resp_pos.get_value() + 1.55, resp_y.get_value() + 0.88, 0])
        )
        asp_lbl = always_redraw(
            lambda: T("Asp", size=24, color=TEXT, weight=BOLD).move_to([resp_pos.get_value() + 0.96, resp_y.get_value() + 0.14, 0])
        )

        # Beat 1: "Many bacteria use" -> responder glides in, external stimulus descends to sensor
        self.at("Many bacteria use")
        self.add(mem, tag, head, sensor, sensor_lbl, his_lbl, dna_line, dna_lbl, sw_box, sw_tick, resp, resp_lbl, asp_lbl)
        ext_sig = Dot(radius=0.14, color=C_PHOS).move_to([-2.2, 2.80, 0])
        self.play(
            resp_pos.animate.set_value(1.85),
            FadeIn(ext_sig),
            run_time=2.2,
        )
        self.play(ext_sig.animate.move_to(sensor.head_pos + UP * 0.30), run_time=1.2)

        # Beat 2: "A membrane sensor kinase"
        self.at("A membrane sensor kinase")
        sig_ring = RoundedRectangle(
            corner_radius=0.18, width=1.14, height=0.74,
            stroke_color=C_PHOS, stroke_width=3.5,
        ).move_to(sensor.head_pos)
        self.play(FadeOut(ext_sig), Create(sig_ring), run_time=0.9)
        self.play(FadeOut(sig_ring), run_time=0.4)

        # Beat 3: "takes one phosphate" -> "its own histidine"
        self.at("takes one phosphate")
        atp_box = pill("ATP", C_PHOS, text_color=C_PHOS, size=26).move_to([-5.0, 0.38, 0])
        phos = make_phos(pos=[-4.10, 0.38, 0], radius=0.22)
        self.play(FadeIn(atp_box), FadeIn(phos), run_time=0.8)
        self.play(phos.animate.shift(RIGHT * 0.45), run_time=1.4)

        self.at("its own histidine")
        adp_box = pill("ADP", GREY, text_color=TEXT, size=24).move_to([-5.0, 0.38, 0])
        self.play(
            phos.animate.move_to(sensor.his_pos),
            swap(atp_box, adp_box, run_time=0.6),
            run_time=1.3,
        )
        self.play(FadeOut(adp_box), run_time=0.5)

        # Beat 4: "Its partner responder"
        self.at("Its partner responder")
        self.play(resp_pos.animate.set_value(-0.56), run_time=1.4)
        self.play(phos.animate.move_to([-1.24, 0.40, 0]), run_time=0.9)

        # Beat 5: "flipping its shape" / "switch genes on"
        self.at("flipping its shape")
        phos.add_updater(lambda m: m.move_to([resp_pos.get_value() - 0.68, resp_y.get_value() + 0.35, 0]))
        self.play(bend_t.animate.set_value(34.0), run_time=0.9)

        self.at("switch genes on")
        sw_on = pill("Genes: ON", GREEN, text_color=GREEN, size=24).move_to([3.3, -1.42, 0])
        sw_tick_on = Line([3.3, -1.78, 0], [3.3, -2.05, 0], color=GREEN, stroke_width=4)
        gene_wave = Line([-0.2, -2.15, 0], [3.3, -2.15, 0], color=GREEN, stroke_width=6)
        self.play(
            resp_pos.animate.set_value(0.25),
            resp_y.animate.set_value(-1.18),
            run_time=1.2,
        )
        phos.clear_updaters()
        self.play(
            swap(sw_box, sw_on, run_time=0.6),
            Transform(sw_tick, sw_tick_on),
            Create(gene_wave),
            run_time=1.1,
        )

        # Beat 6: "has a different fold"
        self.at("has a different fold")
        fold_ring = RoundedRectangle(
            corner_radius=0.15, width=1.46, height=0.86,
            stroke_color=TEXT, stroke_width=3,
        ).move_to(sensor.fold_center)
        fold_lbl = T("Different kinase fold", size=24, color=TEXT, weight=BOLD).move_to([-4.68, -0.78, 0])
        self.play(Create(fold_ring), FadeIn(fold_lbl), run_time=1.0)

        # Beat 7: "and animals lack"
        self.at("and animals lack")
        cap = caption("Different fold; absent in animals", size=28, color=TEXT)
        self.play(FadeIn(cap), run_time=0.5)
        self.finish()


# ======================================================================
# Scene 03 + Scene 04: Predict Setup & Predict Pause (shared backdrop)
# ======================================================================
def build_s03_panels(asp_level=0.0, tyr_level=1.0, decayed=True):
    """Build the split Bacterial vs Animal comparison panels for S03 end-state and S04Pause."""
    tp = TwoPanel(
        "Bacterial: Asp phosphate", "Animal: Tyr phosphate",
        colors=(C_ALT, C_RECEPTOR), top=3.25, bottom=-2.15, gap=0.4, width=12.8, size=30,
    )
    lx = -3.3
    resp = make_responder_shape(angle_deg=0.0 if decayed else 32.0, color=C_ALT).move_to([lx - 0.85, 0.30, 0])
    asp_txt = T("Asp", size=24, color=TEXT, weight=BOLD).move_to([lx - 1.55, 1.28, 0])
    p_left = make_phos([lx - 1.62, 0.56, 0], radius=0.20)
    p_left.set_opacity(max(0.0, asp_level))

    bar_bg_l = RoundedRectangle(corner_radius=0.06, width=0.48, height=2.1, stroke_color=GREY, stroke_width=2.5).move_to([lx + 1.75, 0.30, 0])
    h_l = max(0.02, 2.02 * asp_level)
    bar_fill_l = RoundedRectangle(
        corner_radius=0.04, width=0.40, height=h_l,
        stroke_width=0, fill_color=C_PHOS, fill_opacity=0.90 if asp_level > 0.05 else 0.0,
    ).move_to([lx + 1.75, 0.30 - 1.01 + h_l / 2, 0])
    meter_lbl_l = T("Bound P", size=24, color=TEXT).next_to(bar_bg_l, UP, buff=0.14)
    note_l = T("Sheds itself\n(sec–min)", size=24, color=C_ALT).move_to([lx - 0.55, -1.32, 0])

    rx = 3.3
    mem_r = make_membrane(rx - 2.6, rx + 1.05, 1.75, h=0.18)
    rec = make_receptor(rx - 0.9, 1.75, color=C_RECEPTOR, scale=0.95, tail_len=1.65, site_offsets=(0.95,))
    tyr_txt = T("Tyr", size=24, color=TEXT, weight=BOLD).move_to([rx - 1.68, 0.65, 0])
    p_right = make_phos([rx - 0.38, 0.65, 0], radius=0.22)

    bar_bg_r = RoundedRectangle(corner_radius=0.06, width=0.48, height=2.1, stroke_color=GREY, stroke_width=2.5).move_to([rx + 2.1, 0.30, 0])
    h_r = 2.02 * tyr_level
    bar_fill_r = RoundedRectangle(
        corner_radius=0.04, width=0.40, height=h_r,
        stroke_width=0, fill_color=C_PHOS, fill_opacity=0.92,
    ).move_to([rx + 2.1, 0.30 - 1.01 + h_r / 2, 0])
    meter_lbl_r = T("Bound P", size=24, color=TEXT).next_to(bar_bg_r, UP, buff=0.14)

    eraser = pill("Phosphatase", C_CORE, text_color=C_CORE, size=24).move_to([rx + 0.15, -0.60, 0])
    wait_lbl = T("waits until needed", size=24, color=C_CORE).move_to([rx + 0.15, -1.32, 0])

    left_grp = VGroup(resp, asp_txt, p_left, bar_bg_l, bar_fill_l, meter_lbl_l, note_l)
    right_grp = VGroup(mem_r, rec, tyr_txt, p_right, bar_bg_r, bar_fill_r, meter_lbl_r, eraser, wait_lbl)
    return tp, left_grp, right_grp


class S03PredictSetup(SpokenScene):
    def construct(self):
        tp = TwoPanel(
            "Bacterial: Asp phosphate", "Animal: Tyr phosphate",
            colors=(C_ALT, C_RECEPTOR), top=3.25, bottom=-2.15, gap=0.4, width=12.8, size=30,
        )
        lx, rx = -3.3, 3.3

        asp_t = ValueTracker(1.0)
        bend_t = ValueTracker(32.0)

        resp = always_redraw(lambda: make_responder_shape(angle_deg=bend_t.get_value(), color=C_ALT).move_to([lx - 0.85, 0.30, 0]))
        asp_txt = T("Asp", size=24, color=TEXT, weight=BOLD).move_to([lx - 1.55, 1.28, 0])
        p_left = always_redraw(lambda: make_phos([lx - 1.62, 0.56, 0], radius=0.20).set_opacity(max(0.0, asp_t.get_value())))

        bar_bg_l = RoundedRectangle(corner_radius=0.06, width=0.48, height=2.1, stroke_color=GREY, stroke_width=2.5).move_to([lx + 1.75, 0.30, 0])
        bar_fill_l = always_redraw(lambda: RoundedRectangle(
            corner_radius=0.04, width=0.40, height=max(0.02, 2.02 * asp_t.get_value()),
            stroke_width=0, fill_color=C_PHOS, fill_opacity=0.92 if asp_t.get_value() > 0.04 else 0.0,
        ).move_to([lx + 1.75, 0.30 - 1.01 + max(0.02, 2.02 * asp_t.get_value()) / 2, 0]))
        meter_lbl_l = T("Bound P", size=24, color=TEXT).next_to(bar_bg_l, UP, buff=0.14)

        # Beat 1: "Notice that mark" — ring highlights Asp phosphate while bound-P bar is full
        self.at("Notice that mark")
        self.add(tp, resp, asp_txt, p_left, bar_bg_l, bar_fill_l, meter_lbl_l)
        mark_ring = Circle(radius=0.34, color=C_PHOS, stroke_width=3.5).move_to([lx - 1.62, 0.56, 0])
        self.play(Create(mark_ring), run_time=1.0)
        self.play(FadeOut(mark_ring), run_time=0.8)

        # Beat 2: "is short" / "The responder itself"
        self.at("is short")
        note_l = T("Sheds itself\n(sec–min)", size=24, color=C_ALT).move_to([lx - 0.55, -1.32, 0])
        self.play(FadeIn(note_l), run_time=0.7)

        self.at("The responder itself")
        self.play(
            asp_t.animate(rate_func=lambda u: (1 - np.exp(-3.5 * u)) / (1 - np.exp(-3.5))).set_value(0.0),
            bend_t.animate.set_value(0.0),
            run_time=5.0,
        )

        # Beat 3: "It changes only"
        self.at("It changes only")
        only_badge = pill("1 responder only", C_ALT, text_color=C_ALT, size=24).move_to([lx - 0.85, 2.08, 0])
        self.play(FadeIn(only_badge), run_time=0.9)

        # Beat 4: "On an animal receptor"
        self.at("On an animal receptor")
        mem_r = make_membrane(rx - 2.6, rx + 1.05, 1.75, h=0.18)
        rec = make_receptor(rx - 0.9, 1.75, color=C_RECEPTOR, scale=0.95, tail_len=1.65, site_offsets=(0.95,))
        tyr_txt = T("Tyr", size=24, color=TEXT, weight=BOLD).move_to([rx - 1.68, 0.65, 0])
        bar_bg_r = RoundedRectangle(corner_radius=0.06, width=0.48, height=2.1, stroke_color=GREY, stroke_width=2.5).move_to([rx + 2.1, 0.30, 0])
        bar_fill_r = RoundedRectangle(
            corner_radius=0.04, width=0.40, height=2.02,
            stroke_width=0, fill_color=C_PHOS, fill_opacity=0.92,
        ).move_to([rx + 2.1, 0.30, 0])
        meter_lbl_r = T("Bound P", size=24, color=TEXT).next_to(bar_bg_r, UP, buff=0.14)
        self.play(FadeIn(mem_r), FadeIn(rec), FadeIn(tyr_txt), FadeIn(bar_bg_r), FadeIn(meter_lbl_r), run_time=1.0)

        # Beat 5: "on tyrosine stays" / "until a phosphatase"
        self.at("on tyrosine stays")
        p_right = make_phos([rx - 0.38, 0.65, 0], radius=0.22)
        self.play(FadeIn(p_right, scale=1.2), GrowFromEdge(bar_fill_r, DOWN), run_time=1.0)

        self.at("until a phosphatase")
        eraser = pill("Phosphatase", C_CORE, text_color=C_CORE, size=24).move_to([rx + 0.15, -0.60, 0])
        wait_lbl = T("waits until needed", size=24, color=C_CORE).move_to([rx + 0.15, -1.32, 0])
        self.play(FadeIn(eraser, shift=UP * 0.25), FadeIn(wait_lbl), run_time=1.4)
        self.play(Indicate(eraser, color=C_CORE, scale_factor=1.08), run_time=1.4)

        # Beat 6: "What new kind"
        self.at("What new kind")
        q = question_card("What new kind of connection does a lasting mark allow?", y=BOTTOM_Y + 0.15, max_w=10.2)
        self.play(FadeIn(q.question), run_time=1.4)
        self.finish()


class S04Pause(PredictPause):
    QUESTION = "What new kind of connection does a lasting mark allow?"
    SECONDS = 4.1

    def backdrop(self):
        tp, left_grp, right_grp = build_s03_panels(asp_level=0.0, tyr_level=1.0, decayed=True)
        only_badge = pill("1 responder only", C_ALT, text_color=C_ALT, size=24).move_to([-4.15, 2.08, 0])
        return VGroup(tp, left_grp, right_grp, only_badge)


# ======================================================================
# Scene 05: Reveal Readers — SH2 cups dock and launch branches
# ======================================================================
class S05RevealReaders(SpokenScene):
    def construct(self):
        y_mem = 2.00
        mem = make_membrane(-5.9, 5.9, y_mem, h=0.24, cyto_bottom=-2.85)
        rec_small = make_receptor(2.4, y_mem, color=C_RECEPTOR, scale=0.85, tail_len=1.65, site_offsets=(0.85,))
        rec = make_receptor(-3.2, y_mem, color=C_RECEPTOR, scale=1.25, tail_len=2.55, site_offsets=(0.85, 1.95))
        rec_lbl = T("Animal receptor", size=28, color=C_RECEPTOR, weight=BOLD).move_to([-3.2, HEAD_Y, 0])
        tyr1_lbl = T("Tyr", size=24, color=TEXT, weight=BOLD).move_to([-4.20, 0.72, 0])
        p1 = make_phos([-2.78, 0.72, 0], radius=0.24)
        tag = scope_tag("schematic")

        # Beat 1: "Because the mark" -> receptor expands from right-panel position to center stage
        self.at("Because the mark")
        self.add(mem, tag, rec_small)
        self.play(Transform(rec_small, rec), FadeIn(rec_lbl), FadeIn(tyr1_lbl), FadeIn(p1), run_time=1.8)

        # Beat 2: "docking tag"
        self.at("docking tag")
        dock_tag = pill("Docking tag", C_PHOS, text_color=C_PHOS, size=26).move_to([-0.15, 0.72, 0])
        self.play(FadeIn(dock_tag), run_time=1.0)

        # Beat 3: "Separate reader pieces" -> "bind the marked"
        self.at("Separate reader pieces")
        sh2_1 = make_sh2_cup(color=C_READER, facing=LEFT, text="SH2").move_to([3.8, 0.72, 0])
        sh2_lbl = T("Reader domain", size=26, color=C_READER, weight=BOLD).move_to([3.8, 1.52, 0])
        self.play(FadeOut(dock_tag), FadeIn(sh2_1), FadeIn(sh2_lbl), run_time=0.8)
        self.play(sh2_1.animate.move_to([1.2, 0.72, 0]), sh2_lbl.animate.move_to([1.2, 1.52, 0]), run_time=1.6)

        self.at("bind the marked")
        self.play(sh2_1.animate.move_to([-2.12, 0.72, 0]), sh2_lbl.animate.move_to([-0.35, 1.52, 0]), run_time=0.9)

        # Beat 4: "and recruit downstream"
        self.at("and recruit downstream")
        k1a = pill("Kinase 1A", C_CORE, text_color=TEXT, size=24).move_to([0.75, 0.72, 0])
        k1b = pill("Pathway 1", C_CORE, text_color=TEXT, size=24).move_to([4.15, 0.72, 0])
        arr1a = Arrow(sh2_1.get_right() + RIGHT * 0.08, k1a.get_left() + LEFT * 0.08, buff=0, color=C_CORE, stroke_width=3.5)
        arr1b = Arrow(k1a.get_right() + RIGHT * 0.08, k1b.get_left() + LEFT * 0.08, buff=0, color=C_CORE, stroke_width=3.5)

        b1_active = ValueTracker(1.0)
        b2_active = ValueTracker(0.0)
        stream = make_pulse_stream(
            lambda: [
                np.array([sh2_1.get_right() + RIGHT * 0.08, k1a.get_left() + LEFT * 0.08]),
                np.array([k1a.get_right() + RIGHT * 0.08, k1b.get_left() + LEFT * 0.08]),
                np.array([[-1.40, -0.68, 0], [-0.28, -0.68, 0]]),
                np.array([[1.78, -0.68, 0], [3.08, -0.68, 0]]),
            ],
            lambda: [b1_active.get_value() > 0.5, b1_active.get_value() > 0.5, b2_active.get_value() > 0.5, b2_active.get_value() > 0.5],
            color=C_PHOS, speed=0.95, count=2,
        )
        self.play(FadeIn(k1a), FadeIn(k1b), FadeIn(arr1a), FadeIn(arr1b), run_time=0.8)
        self.add(stream)

        # Beat 5: "One receptor can" -> "launch several branches"
        self.at("One receptor can")
        tyr2_lbl = T("Tyr", size=24, color=TEXT, weight=BOLD).move_to([-4.20, -0.68, 0])
        p2 = make_phos([-2.78, -0.68, 0], radius=0.24)
        self.play(FadeIn(tyr2_lbl), FadeIn(p2, scale=1.2), run_time=0.9)

        self.at("launch several branches")
        sh2_2 = make_sh2_cup(color=C_READER, facing=LEFT, text="SH2").move_to([1.2, -0.68, 0])
        k2a = pill("Kinase 2A", C_CORE, text_color=TEXT, size=24).move_to([0.75, -0.68, 0])
        k2b = pill("Pathway 2", C_CORE, text_color=TEXT, size=24).move_to([4.15, -0.68, 0])
        self.play(FadeIn(sh2_2), run_time=0.4)
        self.play(sh2_2.animate.move_to([-2.12, -0.68, 0]), run_time=0.7)
        arr2a = Arrow(sh2_2.get_right() + RIGHT * 0.08, k2a.get_left() + LEFT * 0.08, buff=0, color=C_CORE, stroke_width=3.5)
        arr2b = Arrow(k2a.get_right() + RIGHT * 0.08, k2b.get_left() + LEFT * 0.08, buff=0, color=C_CORE, stroke_width=3.5)
        b2_active.set_value(1.0)
        self.play(FadeIn(k2a), FadeIn(k2b), FadeIn(arr2a), FadeIn(arr2b), run_time=0.7)
        self.finish()


# ======================================================================
# Scene 06: Modular Moves (Move 1: swap domain; Move 2: mutate motif)
# ======================================================================
class S06ModularMoves(SpokenScene):
    def construct(self):
        y_mem = 2.00
        mem = make_membrane(-5.9, 5.9, y_mem, h=0.22, cyto_bottom=-2.85)
        rec = make_receptor(-4.3, y_mem, color=C_RECEPTOR, scale=1.2, tail_len=2.5, site_offsets=(0.85,))
        p1 = make_phos([-3.88, 0.72, 0], radius=0.23)
        tyr_lbl = T("Tyr", size=24, color=TEXT, weight=BOLD).move_to([-5.18, 0.72, 0])

        head = T("Modular parts make rewiring cheap", size=30, color=TEXT, weight=BOLD).move_to([-0.2, HEAD_Y, 0])
        tag = scope_tag("schematic")

        sh2 = make_sh2_cup(color=C_READER, facing=LEFT, text="SH2").move_to([-3.22, 0.72, 0])
        old_eff = pill("Old protein", GREY, text_color=TEXT, size=24).move_to([0.45, 0.72, 0])
        new_eff = pill("New effector", C_CORE, text_color=TEXT, size=24).move_to([2.6, -0.95, 0])
        link_old = Line(sh2.get_right() + RIGHT * 0.06, old_eff.get_left() + LEFT * 0.06, color=C_READER, stroke_width=3.5)

        # Beat 1: "Modular parts make" -> bring in parts dynamically so frame 0..4s is alive
        self.at("Modular parts make")
        self.add(mem, tag, rec, tyr_lbl, p1, head)
        self.play(FadeIn(sh2), FadeIn(old_eff), Create(link_old), run_time=1.4)
        self.play(sh2.animate.shift(RIGHT * 0.35), link_old.animate.put_start_and_end_on([-2.22, 0.72, 0], old_eff.get_left() + LEFT * 0.06), run_time=1.4)

        # Beat 2: "A domain is"
        self.at("A domain is")
        dom_badge = T("Domain: works on its own", size=26, color=C_READER, weight=BOLD).move_to([-1.2, -0.55, 0])
        self.play(FadeOut(link_old), run_time=0.25)
        self.play(
            sh2.animate.move_to([-1.80, 0.72, 0]),
            FadeIn(dom_badge),
            run_time=0.95,
        )

        # Beat 3: "First, moving"
        self.at("First, moving")
        step1 = T("1. Move an SH2 domain", size=30, color=C_READER, weight=BOLD).move_to([-0.2, HEAD_Y, 0])
        self.play(swap(head, step1, run_time=0.5), FadeOut(dom_badge), FadeIn(new_eff), FadeOut(old_eff), run_time=0.9)
        self.play(sh2.animate.next_to(new_eff, LEFT, buff=0.16), run_time=1.0)

        # Beat 4: "builds a new link"
        self.at("builds a new link")
        hybrid = VGroup(sh2, new_eff)
        dx_d = -3.22 - sh2.get_center()[0]
        dy_d = 0.72 - sh2.get_center()[1]
        self.play(hybrid.animate.shift([dx_d, dy_d, 0]), run_time=1.0)
        out_box = pill("New pathway", C_CORE, text_color=TEXT, size=24).move_to([3.55, 0.72, 0])
        out_arr = Arrow(new_eff.get_right() + RIGHT * 0.08, out_box.get_left() + LEFT * 0.08, buff=0, color=C_CORE, stroke_width=3.5)
        pulse_flag = ValueTracker(1.0)
        p_stream = make_pulse_stream(
            lambda: [np.array([new_eff.get_right() + RIGHT * 0.08, out_box.get_left() + LEFT * 0.08])],
            lambda: [pulse_flag.get_value() > 0.5],
            color=C_PHOS, speed=1.0, count=2,
        )
        self.play(FadeIn(out_box), FadeIn(out_arr), run_time=0.6)
        self.add(p_stream)

        # Beat 5: "Second, mutating"
        self.at("Second, mutating")
        stop_pulse_stream(self, p_stream)
        step2 = T("2. Mutate 1–2 amino acids beside Tyr", size=30, color=C_READER, weight=BOLD).move_to([-0.2, HEAD_Y, 0])
        old_scene = VGroup(mem, rec, tyr_lbl, p1, hybrid, out_box, out_arr)

        tail_bar = RoundedRectangle(
            corner_radius=0.14, width=6.6, height=0.98,
            stroke_color=C_RECEPTOR, stroke_width=3, fill_color=C_RECEPTOR, fill_opacity=0.28,
        ).move_to([-1.4, 0.55, 0])
        tyr_bead = Circle(radius=0.42, stroke_color=C_RECEPTOR, stroke_width=3, fill_color=C_RECEPTOR, fill_opacity=0.45).move_to([-2.9, 0.55, 0])
        tyr_b_lbl = T("Tyr", size=24, color=TEXT, weight=BOLD).move_to(tyr_bead)
        p_zoom = make_phos([-2.9, 1.32, 0], radius=0.25)
        b1 = Circle(radius=0.32, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.32).move_to([-1.6, 0.55, 0])
        b1_lbl = T("X", size=24, color=TEXT).move_to(b1)
        b2 = Circle(radius=0.32, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.32).move_to([-0.3, 0.55, 0])
        b2_lbl = T("X", size=24, color=TEXT).move_to(b2)

        reader2 = Polygon(
            [-3.5, 2.75, 0], [1.1, 2.75, 0],
            [1.1, 1.68, 0], [0.08, 1.68, 0],
            [0.08, 2.02, 0], [-0.68, 2.02, 0],
            [-0.68, 1.68, 0], [-2.52, 1.68, 0],
            [-2.52, 2.02, 0], [-3.28, 2.02, 0],
            [-3.28, 1.68, 0], [-3.5, 1.68, 0],
            stroke_color=C_READER, stroke_width=3, fill_color=C_READER, fill_opacity=0.35,
        ).shift(RIGHT * 2.2)
        reader2_lbl = T("Different SH2 adaptor", size=24, color=TEXT, weight=BOLD).move_to([1.0, 2.38, 0])

        zoom_grp = VGroup(tail_bar, tyr_bead, tyr_b_lbl, p_zoom, b1, b1_lbl, b2, b2_lbl)
        self.play(FadeOut(old_scene), swap(step1, step2, run_time=0.5), run_time=0.6)
        self.play(FadeIn(zoom_grp), FadeIn(reader2), FadeIn(reader2_lbl), run_time=0.7)

        b2_mut = Circle(radius=0.34, stroke_color=C_READER, stroke_width=3.5, fill_color=C_READER, fill_opacity=0.52).move_to([-0.3, 0.55, 0])
        b2_mut_lbl = T("M", size=24, color=TEXT, weight=BOLD).move_to(b2_mut)
        b2_tab = RoundedRectangle(corner_radius=0.05, width=0.44, height=0.26, stroke_color=C_READER, stroke_width=3, fill_color=C_READER, fill_opacity=0.65).move_to([-0.3, 1.24, 0])
        site_lbl = T("New docking site", size=26, color=C_PHOS, weight=BOLD).move_to([-1.6, -0.42, 0])
        self.play(
            Transform(b2, b2_mut),
            swap(b2_lbl, b2_mut_lbl, run_time=0.4),
            FadeIn(b2_tab),
            FadeIn(site_lbl),
            run_time=1.0,
        )

        # Beat 6: "builds a new docking"
        self.at("builds a new docking")
        dx_r = -2.2
        dy_r = -0.35
        self.play(
            reader2.animate.shift([dx_r, dy_r, 0]),
            reader2_lbl.animate.shift([dx_r, dy_r, 0]),
            run_time=0.55,
        )
        new_link = pill("New link active", C_CORE, text_color=TEXT, size=24).move_to([3.85, 1.85, 0])
        arr_link = Arrow(reader2.get_right() + RIGHT * 0.1, new_link.get_left() + LEFT * 0.1, buff=0, color=C_CORE, stroke_width=3.5)
        self.play(FadeIn(new_link), FadeIn(arr_link), run_time=0.4)
        self.finish()


# ======================================================================
# Scene 07: Regulatory DNA & Genome Counts (Yeast 1 vs Human >100)
# ======================================================================
class S07RegulatoryAndCounts(SpokenScene):
    def construct(self):
        head = T("3. Change regulatory DNA", size=30, color=C_READER, weight=BOLD).move_to([-2.0, HEAD_Y, 0])
        tag = scope_tag("schematic")

        reg_sw = pill("Regulatory DNA", C_MEMBRANE, text_color=TEXT, size=24).move_to([-4.2, 2.35, 0])
        gene_box = pill("Receptor gene", C_RECEPTOR, text_color=TEXT, size=24).move_to([-0.4, 2.35, 0])
        dna_seg1 = Line([-5.95, 2.35, 0], reg_sw.get_left() + LEFT * 0.04, color=C_MEMBRANE, stroke_width=4)
        dna_seg2 = Line(reg_sw.get_right() + RIGHT * 0.04, gene_box.get_left() + LEFT * 0.04, color=C_MEMBRANE, stroke_width=4)
        dna_seg3 = Line(gene_box.get_right() + RIGHT * 0.04, [1.55, 2.35, 0], color=C_MEMBRANE, stroke_width=4)
        dna = VGroup(dna_seg1, dna_seg2, dna_seg3)

        cell_a = RoundedRectangle(corner_radius=0.35, width=3.2, height=3.25, stroke_color=C_MEMBRANE, stroke_width=3, fill_color=C_CYTO, fill_opacity=0.88).move_to([-4.2, -0.45, 0])
        cell_a_lbl = T("Cell A", size=26, color=TEXT, weight=BOLD).move_to([-4.2, -2.42, 0])
        rec_a = make_receptor(-4.2, 1.18, color=C_RECEPTOR, scale=0.82, tail_len=0.90)
        targ_a = pill("Target A", C_CORE, text_color=TEXT, size=24).move_to([-4.2, -1.25, 0])

        cell_b = RoundedRectangle(corner_radius=0.35, width=3.2, height=3.25, stroke_color=C_MEMBRANE, stroke_width=3, fill_color=C_CYTO, fill_opacity=0.88).move_to([-0.4, -0.45, 0])
        cell_b_lbl = T("Cell B (new tissue)", size=26, color=TEXT, weight=BOLD).move_to([-0.4, -2.42, 0])
        targ_b1 = pill("Target B1", C_CORE, text_color=TEXT, size=24, pad=0.14).move_to([-0.4, -0.70, 0])
        targ_b2 = pill("Target B2", C_CORE, text_color=TEXT, size=24, pad=0.14).move_to([-0.4, -1.52, 0])

        # Beat 1: "Third, regulatory" -> build DNA + cells + active scan highlight during 0..5s
        self.at("Third, regulatory")
        self.add(head, dna, reg_sw, gene_box, cell_a, cell_a_lbl, targ_a, tag)
        scan_arr = Arrow(reg_sw.get_right() + RIGHT * 0.08, gene_box.get_left() + LEFT * 0.08, buff=0, color=C_READER, stroke_width=5)
        scan_dot = Dot(radius=0.09, color=C_READER).move_to(scan_arr.get_start())
        self.play(FadeIn(cell_b), FadeIn(cell_b_lbl), FadeIn(targ_b1), FadeIn(targ_b2), GrowArrow(scan_arr), FadeIn(scan_dot), run_time=1.6)
        self.play(scan_dot.animate.move_to(scan_arr.get_end()), run_time=2.0)
        self.play(FadeOut(scan_arr), FadeOut(scan_dot), run_time=0.6)

        # Beat 2: "decides which cells"
        self.at("decides which cells")
        arr_a = Arrow(reg_sw.get_bottom() + DOWN * 0.08, [-4.2, 1.66, 0], buff=0, color=C_READER, stroke_width=3.5)
        self.play(FadeIn(arr_a), FadeIn(rec_a, shift=DOWN * 0.2), run_time=1.5)

        # Beat 3: "Changing it"
        self.at("Changing it")
        reg_sw_new = pill("Regulatory DNA", C_READER, text_color=TEXT, size=24).move_to([-4.2, 2.35, 0])
        arr_b = Arrow(gene_box.get_bottom() + DOWN * 0.08, [-1.15, 1.66, 0], buff=0, color=C_READER, stroke_width=3.5)
        self.play(Transform(reg_sw, reg_sw_new), FadeOut(arr_a), FadeIn(arr_b), run_time=1.3)

        # Beat 4: "into a new tissue"
        self.at("into a new tissue")
        rec_b = make_receptor(-1.15, 1.18, color=C_RECEPTOR, scale=0.82, tail_len=0.90)
        unchanged_lbl = T("Same\nreceptor", size=24, color=C_RECEPTOR, weight=BOLD).move_to([0.22, 0.15, 0])
        pulse_flag = ValueTracker(1.0)
        p_stream = make_pulse_stream(
            lambda: [
                np.array([[-4.2, 0.25, 0], [-4.2, -0.88, 0]]),
                np.array([[-1.15, 0.25, 0], [-0.85, targ_b1.get_top()[1] + 0.14, 0]]),
            ],
            lambda: [pulse_flag.get_value() > 0.5, pulse_flag.get_value() > 0.5],
            color=C_PHOS, speed=0.95, count=2,
        )
        self.play(FadeIn(rec_b, shift=DOWN * 0.2), FadeIn(unchanged_lbl), run_time=1.4)
        self.add(p_stream)

        # Beat 5: "Genome counts match"
        self.at("Genome counts match")
        plot = Plot(
            box=(2.3, 6.0, -1.6, 1.9), xr=(0, 3), yr=(0, 120),
            xticks=[], yticks=[(0, "0"), (50, "50"), (100, "100")],
            ylabel="SH2 proteins", color=GREY, size=24, label_size=26,
        )
        chart_title = T("Genome SH2 counts", size=28, color=TEXT, weight=BOLD).move_to([4.15, HEAD_Y, 0])
        self.play(FadeIn(chart_title), Create(plot), run_time=1.1)

        # Beat 6: "yeast has"
        self.at("yeast has")
        yeast_v = ValueTracker(0.0)
        human_v = ValueTracker(0.0)

        def bar_rect(x_center, val_t, col):
            v = max(0.5, val_t.get_value())
            p_bot = plot.pt(x_center, 0)
            p_top = plot.pt(x_center, v)
            h = max(0.06, p_top[1] - p_bot[1])
            return RoundedRectangle(
                corner_radius=0.04, width=0.9, height=h,
                stroke_width=0, fill_color=col, fill_opacity=0.88,
            ).move_to([p_bot[0], p_bot[1] + h / 2, 0])

        y_bar = always_redraw(lambda: bar_rect(0.9, yeast_v, C_ALT))
        h_bar = always_redraw(lambda: bar_rect(2.1, human_v, C_READER))
        y_xlbl = T("Yeast", size=24, color=C_ALT, weight=BOLD).move_to([plot.pt(0.9, 0)[0], -1.98, 0])
        h_xlbl = T("Human", size=24, color=C_READER, weight=BOLD).move_to([plot.pt(2.1, 0)[0], -1.98, 0])
        y_num = always_redraw(lambda: M(f"{int(round(yeast_v.get_value()))}", size=26, color=C_ALT).move_to([plot.pt(0.9, yeast_v.get_value())[0], plot.pt(0.9, yeast_v.get_value())[1] + 0.30, 0]))
        h_num = always_redraw(lambda: M(
            ">100" if human_v.get_value() >= 99.5 else f"{int(round(human_v.get_value()))}",
            size=26, color=C_READER,
        ).move_to([plot.pt(2.1, human_v.get_value())[0], plot.pt(2.1, human_v.get_value())[1] + 0.30, 0]))

        self.add(y_bar, y_num)
        self.play(FadeIn(y_xlbl), yeast_v.animate.set_value(1.0), run_time=0.9)

        # Beat 7: "while humans carry"
        self.at("while humans carry")
        self.add(h_bar, h_num)
        self.play(FadeIn(h_xlbl), human_v.animate.set_value(100.0), run_time=0.9)
        self.finish()


# ======================================================================
# Scene 08: Choanoflagellate — Toolkit predates animals
# ======================================================================
class S08Choanoflagellate(SpokenScene):
    def construct(self):
        tag = scope_tag("schematic")
        q_head = T("When did this tyrosine toolkit appear?", size=32, color=TEXT, weight=BOLD).move_to([0, HEAD_Y, 0])
        tl = Arrow([-4.5, 0.2, 0], [4.5, 0.2, 0], color=C_RECEPTOR, stroke_width=4.5)
        tl_past = T("Common ancestor (?)", size=26, color=C_PHOS).move_to([-3.2, -0.35, 0])
        tl_now = T("Animals today", size=26, color=C_RECEPTOR).move_to([3.2, -0.35, 0])

        # Beat 1: "When did this" — sweep timeline marker into the past
        self.at("When did this")
        self.add(q_head, tl_past, tl_now, tag)
        self.play(GrowArrow(tl), run_time=2.2)

        # Beat 2: "Look at"
        self.at("Look at")
        head2 = T("Closest living single-celled relative of animals", size=30, color=C_RECEPTOR, weight=BOLD).move_to([0, HEAD_Y, 0])
        choano = make_choanoflagellate(center=(-3.8, 0.45, 0), color=C_RECEPTOR)
        choano_lbl = T("Choanoflagellate\n(Monosiga brevicollis)", size=24, color=C_RECEPTOR, weight=BOLD).move_to([-3.8, -1.52, 0])

        phase_t = ValueTracker(0.0)
        def make_flagellum():
            base = choano.flag_base
            ys = np.linspace(0.0, 1.40, 28)
            xs = 0.28 * (ys / 1.40) * np.sin(7.0 * ys - phase_t.get_value())
            pts = [base + np.array([x, y, 0.0]) for x, y in zip(xs, ys)]
            m = VMobject(stroke_color=C_RECEPTOR, stroke_width=4.5)
            m.set_points_as_corners(pts)
            return m

        flag = always_redraw(make_flagellum)
        flag.add_updater(lambda m, dt: phase_t.increment_value(dt * 8.5))

        human_cell = RoundedRectangle(corner_radius=0.5, width=1.9, height=2.2, stroke_color=TEXT, stroke_width=3, fill_color=C_CYTO, fill_opacity=0.88).move_to([-0.8, 0.15, 0])
        human_lbl = T("Human cell", size=24, color=TEXT, weight=BOLD).move_to([-0.8, -1.52, 0])

        self.play(FadeOut(tl), FadeOut(tl_past), FadeOut(tl_now), swap(q_head, head2, run_time=0.5), run_time=0.5)
        self.play(FadeIn(choano), FadeIn(choano_lbl), FadeIn(human_cell), FadeIn(human_lbl), run_time=0.9)
        self.add(flag)

        plot = Plot(
            box=(1.5, 5.9, -0.3, 2.3), xr=(0, 3), yr=(0, 150),
            xticks=[], yticks=[(0, "0"), (100, "100")],
            ylabel="Tyrosine kinases", color=GREY, size=24, label_size=24,
        )
        m_v = ValueTracker(0.0)
        h_v = ValueTracker(0.0)

        def tk_bar(xc, vt, col):
            v = max(1.0, vt.get_value())
            pb = plot.pt(xc, 0)
            pt = plot.pt(xc, v)
            hh = max(0.05, pt[1] - pb[1])
            return RoundedRectangle(
                corner_radius=0.04, width=1.0, height=hh,
                stroke_width=0, fill_color=col, fill_opacity=0.88,
            ).move_to([pb[0], pb[1] + hh / 2, 0])

        m_bar = always_redraw(lambda: tk_bar(0.9, m_v, C_RECEPTOR))
        h_bar = always_redraw(lambda: tk_bar(2.1, h_v, TEXT))
        m_num = always_redraw(lambda: M(f"{int(round(m_v.get_value()))}", size=26, color=C_RECEPTOR).move_to([plot.pt(0.9, m_v.get_value())[0], plot.pt(0.9, m_v.get_value())[1] + 0.28, 0]))
        h_num = always_redraw(lambda: M(f"{int(round(h_v.get_value()))}", size=26, color=TEXT).move_to([plot.pt(2.1, h_v.get_value())[0], plot.pt(2.1, h_v.get_value())[1] + 0.28, 0]))
        m_xl = T("Monosiga", size=24, color=C_RECEPTOR, weight=BOLD).move_to([plot.pt(0.9, 0)[0], -0.65, 0])
        h_xl = T("Human", size=24, color=TEXT, weight=BOLD).move_to([plot.pt(2.1, 0)[0], -0.65, 0])

        self.play(Create(plot), FadeIn(m_xl), FadeIn(h_xl), run_time=0.6)

        # Beat 3: "It carries"
        self.at("It carries")
        self.add(m_bar, m_num)
        self.play(m_v.animate.set_value(128.0), run_time=0.8)

        self.at("to our")
        self.add(h_bar, h_num)
        self.play(h_v.animate.set_value(90.0), run_time=0.6)

        # Beat 4: "plus tyrosine phosphatases" — Writer -> P -> Reader -> Eraser above chips, label clear of P!
        self.at("plus tyrosine phosphatases")
        tk_chip = pill("Writer (TK)", C_RECEPTOR, text_color=TEXT, size=24).move_to([-4.6, -3.12, 0])
        sh_chip = pill("Reader (SH2)", C_READER, text_color=TEXT, size=24).move_to([-1.6, -3.12, 0])
        ptp_chip = pill("Eraser (PTP)", C_CORE, text_color=TEXT, size=24).move_to([1.5, -3.12, 0])
        sub_bar = RoundedRectangle(corner_radius=0.06, width=2.2, height=0.22, stroke_color=C_MEMBRANE, stroke_width=2.5, fill_color=C_MEMBRANE, fill_opacity=0.35).move_to([-1.4, -2.50, 0])
        sub_lbl = T("Substrate", size=24, color=TEXT).move_to([-3.4, -2.50, 0])
        cyc_p = make_phos([-4.5, -2.04, 0], radius=0.20)
        cyc_cup = make_sh2_cup(color=C_READER, w=0.95, h=0.46, facing=LEFT, text="")
        cyc_cup.move_to([0.55, -2.04, 0])
        self.play(FadeIn(tk_chip), FadeIn(sh_chip), FadeIn(ptp_chip), FadeIn(sub_bar), FadeIn(sub_lbl), run_time=0.8)
        self.play(FadeIn(cyc_p), run_time=0.4)
        self.play(cyc_p.animate.move_to([-0.75, -2.04, 0]), run_time=0.9)
        self.play(FadeIn(cyc_cup), run_time=0.3)
        self.play(cyc_cup.animate.move_to([-0.08, -2.04, 0]), run_time=0.8)

        # Beat 5: "Yet it lacks"
        self.at("Yet it lacks")
        no_tgf = pill("No TGF-beta", C_RECEPTOR, text_color=TEXT, size=24).move_to([2.82, -1.52, 0])
        self.play(FadeIn(no_tgf), FadeOut(cyc_cup), run_time=0.45)
        self.play(cyc_p.animate.move_to([1.5, -2.04, 0]), run_time=0.8)
        self.play(FadeOut(cyc_p), FadeOut(sub_bar), FadeOut(sub_lbl), run_time=0.5)

        # Beat 6: "Parts shared by" -> "so the kit predates"
        self.at("Parts shared by")
        flag.clear_updaters()
        self.remove(flag)
        head3 = T("Tyrosine toolkit predates animals", size=30, color=C_PHOS, weight=BOLD).move_to([0, HEAD_Y, 0])
        upper_old = VGroup(choano, choano_lbl, human_cell, human_lbl, plot, m_bar, h_bar, m_num, h_num, m_xl, h_xl, no_tgf, tk_chip, sh_chip, ptp_chip)
        self.play(FadeOut(upper_old), swap(head2, head3, run_time=0.5), run_time=0.5)

        root = pill("Common ancestor", C_PHOS, text_color=C_PHOS, size=26).move_to([0, -1.45, 0])
        br_l = Line([-0.7, -1.08, 0], [-3.2, 1.52, 0], color=C_RECEPTOR, stroke_width=4.5)
        br_r = Line([0.7, -1.08, 0], [3.2, 1.52, 0], color=TEXT, stroke_width=4.5)
        leaf_l = pill("Choanoflagellate", C_RECEPTOR, text_color=TEXT, size=26).move_to([-3.2, 1.95, 0])
        leaf_r = pill("Animals", TEXT, text_color=TEXT, size=26).move_to([3.2, 1.95, 0])
        kit_badge = pill("TK · SH2 · PTP", C_PHOS, text_color=C_PHOS, size=24).move_to([0.0, 0.35, 0])
        tgf_badge = pill("+ TGF-beta", C_CORE, text_color=TEXT, size=24).move_to([4.15, 0.35, 0])

        self.play(FadeIn(root), Create(br_l), Create(br_r), FadeIn(leaf_l), FadeIn(leaf_r), run_time=1.1)

        self.at("so the kit predates")
        self.play(FadeIn(kit_badge), FadeIn(tgf_badge), run_time=1.0)

        # Beat 7: "Its job in"
        self.at("Its job in")
        q_cell = pill("? Role in one cell:\nlargely unknown", C_RECEPTOR, text_color=TEXT, size=24).move_to([-4.35, 0.25, 0])
        self.play(FadeIn(q_cell), run_time=0.9)
        self.finish()


# ======================================================================
# Scene 09: Network Payoff — Robustness, Clinical Costs, 3 Tools
# ======================================================================
class S09NetworkPayoff(SpokenScene):
    def construct(self):
        y_mem = 2.05
        mem = make_membrane(-5.9, 3.0, y_mem, h=0.24, cyto_bottom=-2.45)
        xs = [-4.6, -2.5, -0.4, 1.7]
        r1 = make_receptor(xs[0], y_mem, color=C_RECEPTOR, scale=0.95, tail_len=1.30)
        r2 = make_receptor(xs[1], y_mem, color=C_RECEPTOR, scale=0.95, tail_len=1.30)
        r3 = make_receptor(xs[2], y_mem, color=C_RECEPTOR, scale=0.95, tail_len=1.30)
        r4 = make_receptor(xs[3], y_mem, color=C_ALT, scale=0.95, tail_len=1.30)
        r4_lbl = T("Sister", size=24, color=C_ALT, weight=BOLD).move_to([xs[3], y_mem + 0.88, 0])

        hub_c = np.array([-1.45, -1.0, 0.0])
        hub = make_core_hub(hub_c, label="Shared hub", radius_x=1.65, radius_y=0.72, color=C_CORE)

        wires = VGroup(
            Line([xs[0], y_mem - 1.42, 0], [hub_c[0] - 1.1, hub_c[1] + 0.58, 0], color=C_RECEPTOR, stroke_width=3.5),
            Line([xs[1], y_mem - 1.42, 0], [hub_c[0] - 0.35, hub_c[1] + 0.68, 0], color=C_RECEPTOR, stroke_width=3.5),
            Line([xs[2], y_mem - 1.42, 0], [hub_c[0] + 0.35, hub_c[1] + 0.68, 0], color=C_RECEPTOR, stroke_width=3.5),
            Line([xs[3], y_mem - 1.42, 0], [hub_c[0] + 1.1, hub_c[1] + 0.58, 0], color=C_ALT, stroke_width=3.5),
        )

        out_t = ValueTracker(1.0)
        out_bar_bg = RoundedRectangle(corner_radius=0.08, width=0.62, height=2.6, stroke_color=GREY, stroke_width=3).move_to([4.7, 0.25, 0])
        out_bar = always_redraw(lambda: RoundedRectangle(
            corner_radius=0.05, width=0.50, height=max(0.05, 2.48 * out_t.get_value()),
            stroke_width=0, fill_color=C_CORE, fill_opacity=0.90,
        ).move_to([4.7, 0.25 - 1.24 + max(0.05, 2.48 * out_t.get_value()) / 2, 0]))
        out_lbl = T("Output", size=28, color=TEXT, weight=BOLD).next_to(out_bar_bg, UP, buff=0.16)
        hub_arr = Arrow([hub_c[0] + 1.72, hub_c[1] + 0.15, 0], [4.25, 0.15, 0], buff=0, color=C_CORE, stroke_width=4)

        r_on = [ValueTracker(1.0), ValueTracker(1.0), ValueTracker(1.0), ValueTracker(1.0)]
        p_stream = make_pulse_stream(
            lambda: [
                np.array([[xs[0], y_mem - 1.42, 0], [hub_c[0] - 1.1, hub_c[1] + 0.58, 0]]),
                np.array([[xs[1], y_mem - 1.42, 0], [hub_c[0] - 0.35, hub_c[1] + 0.68, 0]]),
                np.array([[xs[2], y_mem - 1.42, 0], [hub_c[0] + 0.35, hub_c[1] + 0.68, 0]]),
                np.array([[xs[3], y_mem - 1.42, 0], [hub_c[0] + 1.1, hub_c[1] + 0.58, 0]]),
                np.array([[hub_c[0] + 1.72, hub_c[1] + 0.15, 0], [4.25, 0.15, 0]]),
            ],
            lambda: [r_on[0].get_value() > 0.5, r_on[1].get_value() > 0.5, r_on[2].get_value() > 0.5, r_on[3].get_value() > 0.5, True],
            color=C_PHOS, speed=0.95, radius=0.12, count=2,
        )
        tag = scope_tag("schematic")
        head = T("Shared hub network", size=30, color=TEXT, weight=BOLD).move_to([-1.45, HEAD_Y, 0])

        # Beat 1: "Rewiring copied receptors" — wire up receptors -> hub -> output cleanly over first ~3s
        self.at("Rewiring copied receptors")
        self.add(head, mem, r1, r2, r3, r4, r4_lbl, hub, out_bar_bg, out_bar, out_lbl, tag)
        self.play(Create(wires), FadeIn(hub_arr), run_time=1.8)
        self.add(p_stream)

        # Beat 2: "If one receptor fails"
        self.at("If one receptor fails")
        r_on[0].set_value(0.0)
        x_mark = T("×", size=44, color=RED, weight=BOLD).move_to([xs[0], y_mem + 0.88, 0])
        self.play(
            r1.animate.set_opacity(0.28),
            wires[0].animate.set_opacity(0.20),
            FadeIn(x_mark),
            out_t.animate.set_value(0.75),
            run_time=0.9,
        )

        # Beat 3: "sisters made in"
        self.at("sisters made in")
        self.play(
            wires[3].animate.set_stroke(width=6.5),
            r4.animate.scale(1.1),
            out_t.animate.set_value(0.90),
            run_time=1.3,
        )

        # Beat 4: "Hubs buy robustness"
        self.at("Hubs buy robustness")
        rob_chip = pill("Robustness", GREEN, text_color=GREEN, size=24).move_to([-4.6, -1.0, 0])
        self.play(FadeIn(rob_chip), run_time=0.7)

        # Beat 5: "bring clinical costs"
        self.at("bring clinical costs")
        cost_chip = pill("Clinical costs", RED, text_color=RED, size=24).move_to([-4.6, -1.8, 0])
        cost_ring = Ellipse(width=3.65, height=1.65, stroke_color=RED, stroke_width=3.5).move_to(hub_c)
        self.play(FadeIn(cost_chip), Create(cost_ring), run_time=0.7)

        # Beat 6: "Modular domains"
        self.at("Modular domains")
        tools = VGroup(
            pill("Domains", C_READER, text_color=TEXT, size=24),
            pill("Short motifs", C_READER, text_color=TEXT, size=24),
            pill("Regulatory DNA", C_READER, text_color=TEXT, size=24),
        ).arrange(RIGHT, buff=0.35).move_to([-0.8, -2.95, 0])
        self.play(FadeIn(tools[0]), run_time=0.6)
        self.play(FadeIn(tools[1]), run_time=0.6)
        self.play(FadeIn(tools[2]), run_time=0.6)
        self.finish()


# ======================================================================
# Scene 10: End Card
# ======================================================================
class S10End(EndCard):
    LINE = "Modular domains, short motifs, and regulatory DNA make new wiring cheap."
