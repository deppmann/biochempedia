"""A Buffer That Breathes — Water, Weak Bonds, and the Generation of Order (Chapter 2)

COLOUR MAP (one colour per concept for the whole film):
    BLUE   (#58C4DD) : water (the cross-section glass outline and 140 drifting water dots)
    GREEN  (#83C167) : polar surface beads and ionic/weak-bond links on the folded protein ball
    YELLOW (#F5D547) : oily hydrophobic core blobs inside the folded protein ball
    GOLD   (#D4A843) : pH gauge window, pKa ticks/brackets, ratios, sealed lid, acid funnel, questions, ledger
    ORANGE (#FF862F) : protons (H+)
    WHITE  (#FFFFFF) : protonated form holding its proton (HA) in the grid; dissolved CO2 bar & bubbles (acid side)
    PURPLE (#9A72AC) : deprotonated form (A-) in the grid; bicarbonate (HCO3-) bar & kidney slices (base side)
    TEXT   (#E8EAF0) : primary neutral labels and real pH needle
    GREY   (#8B93A1) : gauge axes/ticks, ghost/dimmed pH needle from sealed case, schematic scope tag

ONE WORLD, CARRIED:
    Cross-section of a glass of water filled with 140 stratified-Brownian BLUE water dots, paired with
    the vertical blood pH gauge (scale 6.0 to 7.6, glowing 7.35..7.45 window, live needle at 7.40).
    From s05 onward, the glass holds the bicarbonate (PURPLE) and CO2 (WHITE) concentration bars,
    and from s08 onward, the open top connects through a tube to breathing lungs.

WHAT CHANGES IN EACH SPOKEN SCENE (and what it is computed from):
    s00_link_and_question : Folded ball breathes, GREEN ionic link snaps/slackens as an ORANGE proton binds/leaves
                            a '-' bead, ball shrinks to corner icon, blood pH gauge rises with needle trembling at 7.40.
    s02_pka               : 10x10 grid of 100 HA/A- discs and 'pH - pKa' slider step through -2 -> +2 -> 0;
                            deprotonated count = round(100 * 10**d / (1 + 10**d)) from Henderson-Hasselbalch.
    s03_tenfold           : Grid & slider step 0 -> +1 -> +2 (91% and 99% deprotonated, 10:1 and 100:1);
                            5.9 kJ/mol ledger row and pulsing weak-bond pair enter beside the grid.
    s04_flask_rule        : ORANGE protons rain onto the grid at 0 (buffered near 50:50) vs -2 (99:1, protons pile up),
                            then a GOLD lid clicks shut on the glass and a bracket marks [-1, +1].
    s05_blood             : Bicarbonate (PURPLE) and CO2 (WHITE) bars rise to 24 mM and 1.2 mM (20:1); full gauge
                            highlights pKa 6.1 and the 1.3-unit gap to 7.40.
    s06_sealed            : ORANGE acid pours into the sealed flask and converts slices of PURPLE bicarbonate into
                            WHITE CO2 bubbles; bars and needle begin shifting via 6.1 + log10(hco3 / co2).
    s07_sealed_result     : Computed sealed reaction completes: HCO3- -> 14 mM, CO2 -> 11.2 mM (bubbles press lid),
                            ratio -> 1.25:1, and pH needle drops along 6.1 + log10(hco3 / co2) to 6.20 and dims.
    s08_predict           : Reset to 24 and 1.2 mM (ghost needle kept at 6.2); lid lifts off and tube + breathing
                            lungs attach while CO2 bubbles exhale; question card asks where pH lands.
    s10_open_result       : Acid pours into open flask: HCO3- drops 24 -> 14 mM while WHITE CO2 bubbles exhale
                            through the lungs keeping CO2 = 1.2 mM (12:1), so pH lands at 7.17.
    s11_idea              : Open top flashes GOLD, steady train of CO2 bubbles exhales through lungs, and bracket
                            marks breathing's rescue between sealed (6.2) and open (7.17) needles.
    s12_better            : Other-buffer discs absorb protons, needle nudges up (schematic), then kidneys feed PURPLE
                            slices back into bicarbonate toward 24 mM as needle returns to 7.40.
    s13_stakes            : Folded ball returns; ghost needle drops past window, ORANGE protons neutralize '-' beads
                            and links go slack while heart trace stutters, then protons lift off and links recover.
    s14_return            : Whole system breathes together: CO2 bubble exhales through the lungs while charges
                            and weak-bond links on the folded ball glow and pulse steady.
"""
from bp_parts import *


# ------------------------------------------------------------------ shared helpers
def make_glass_and_water(x0, x1, y0, y1, n_dots=140, seed=7, meniscus=False):
    """Build the open-top glass outline (U-shape) and 140 stratified-Brownian BLUE water dots."""
    outline = VMobject(stroke_color=BLUE, stroke_width=3.8, fill_opacity=0)
    outline.set_points_as_corners([
        [x0, y1, 0],
        [x0, y0, 0],
        [x1, y0, 0],
        [x1, y1, 0],
    ])
    rng = np.random.default_rng(seed)
    cols, rows = 14, 10
    pad_x, pad_y = 0.25, 0.22
    w = (x1 - x0) - 2 * pad_x
    h = (y1 - y0) - 2 * pad_y
    dots = VGroup()
    for r in range(rows):
        for c in range(cols):
            hx = x0 + pad_x + (c + 0.5) * (w / cols)
            hy = y0 + pad_y + (r + 0.5) * (h / rows)
            px = hx + rng.uniform(-0.28, 0.28) * (w / cols)
            py = hy + rng.uniform(-0.28, 0.28) * (h / rows)
            d = Dot([px, py, 0], radius=0.048, color=BLUE, fill_opacity=0.65)
            d._home = np.array([hx, hy, 0.0])
            d._cell_rx = 0.42 * (w / cols)
            d._cell_ry = 0.42 * (h / rows)
            ang = rng.uniform(0, TAU)
            spd = rng.uniform(0.22, 0.42)
            d._vel = np.array([spd * np.cos(ang), spd * np.sin(ang), 0.0])
            d._phase = rng.uniform(0, TAU)
            dots.add(d)

    dots.set_z_index(-5)
    outline.set_z_index(1)

    def update_water(mob, dt):
        for k, d in enumerate(mob):
            d._phase += dt * (1.5 + 0.3 * (k % 5))
            vx = d._vel[0] + 0.16 * np.cos(d._phase + k)
            vy = d._vel[1] + 0.16 * np.sin(d._phase * 1.13 + k)
            nxt = d.get_center() + np.array([vx, vy, 0.0]) * dt
            dx = nxt[0] - d._home[0]
            dy = nxt[1] - d._home[1]
            if abs(dx) > d._cell_rx:
                d._vel[0] *= -1
                nxt[0] = d._home[0] + np.sign(dx) * d._cell_rx
            if abs(dy) > d._cell_ry:
                d._vel[1] *= -1
                nxt[1] = d._home[1] + np.sign(dy) * d._cell_ry
            d.move_to(nxt)

    dots.add_updater(update_water)
    items = [dots, outline]
    if meniscus:
        surf = Line([x0, y1 - 0.02, 0], [x1, y1 - 0.02, 0], color=BLUE, stroke_width=2.0, stroke_opacity=0.45)
        items.append(surf)
    return VGroup(*items), dots, outline


def make_folded_ball(center=(0.0, 0.0, 0.0), scale=1.0, seed=11, with_charges=False):
    """Build the protein ball: YELLOW hydrophobic blobs inside, GREEN polar beads + links outside."""
    rng = np.random.default_rng(seed)
    c = np.array(center, dtype=float)
    core = VGroup()
    for i in range(12):
        r = (0.35 + 0.55 * (i % 3) / 2.0) * scale
        th = i * TAU / 12.0 + rng.uniform(-0.2, 0.2)
        blob = Circle(
            radius=0.28 * scale * rng.uniform(0.85, 1.15),
            color=YELLOW,
            fill_color=YELLOW,
            fill_opacity=0.68,
            stroke_width=1.5,
        ).move_to(c + np.array([r * np.cos(th), r * np.sin(th), 0.0]))
        core.add(blob)

    shell = Circle(
        radius=1.35 * scale,
        color=GREEN,
        stroke_width=2.8,
        fill_color=GREEN,
        fill_opacity=0.08,
    ).move_to(c)

    beads = VGroup()
    n_beads = 12
    for i in range(n_beads):
        th = i * TAU / n_beads
        pos = c + np.array([1.35 * scale * np.cos(th), 1.35 * scale * np.sin(th), 0.0])
        b = Dot(pos, radius=0.14 * scale, color=GREEN, fill_opacity=0.95)
        beads.add(b)

    links = VGroup()
    pair_indices = [(0, 1), (2, 3), (4, 5), (7, 8), (10, 11)]
    for i, j in pair_indices:
        ln = Line(
            beads[i].get_center(),
            beads[j].get_center(),
            color=GREEN,
            stroke_width=3.0 * max(0.7, scale),
        )
        links.add(ln)

    charges = VGroup()
    if with_charges:
        for idx, sym in [(0, "+"), (1, "−"), (7, "+"), (8, "−")]:
            b = beads[idx]
            dir_v = b.get_center() - c
            norm = np.linalg.norm(dir_v) or 1.0
            out = dir_v / norm
            tag = T(sym, size=26, color=TEXT, weight=BOLD)
            tag.move_to(b.get_center() + out * (0.30 * scale))
            charges.add(tag)

    g = VGroup(shell, core, links, beads, charges)
    g.shell = shell
    g.core = core
    g.links = links
    g.beads = beads
    g.charges = charges
    return g


def make_ph_gauge(x=4.10, y0=-2.20, y1=2.60, compact=False, ph_tracker=None, tremble=True, dim_tracker=None):
    """Build the blood pH gauge (scale 6.0 to 7.6), glowing 7.35..7.45 window, and needle."""
    ph_min, ph_max = 6.0, 7.6
    y_of = lambda ph: y0 + (ph - ph_min) / (ph_max - ph_min) * (y1 - y0)

    spine = Line([x, y0, 0], [x, y1, 0], color=GOLD, stroke_width=4.0 if not compact else 3.0)
    ticks = VGroup()
    tick_labels = VGroup()
    tick_vals = [6.0, 6.8, 7.6] if compact else [6.0, 6.2, 6.4, 6.6, 6.8, 7.0, 7.2, 7.4, 7.6]
    for v in tick_vals:
        yv = y_of(v)
        tk = Line([x, yv, 0], [x - 0.14, yv, 0], color=GOLD, stroke_width=2.5)
        ticks.add(tk)
        lb = M(f"{v:.1f}", size=22, color=TEXT).next_to(tk, LEFT, buff=0.10)
        tick_labels.add(lb)

    yw0, yw1 = y_of(7.35), y_of(7.45)
    window_band = Rectangle(
        width=0.34,
        height=max(0.18, yw1 - yw0),
        color=GOLD,
        stroke_width=2.5,
        fill_color=GOLD,
        fill_opacity=0.40,
    ).move_to([x, (yw0 + yw1) / 2.0, 0])

    title = T("blood pH", size=26 if not compact else 24, color=GOLD).next_to([x, y1, 0], UP, buff=0.18)

    if ph_tracker is None:
        ph_tracker = ValueTracker(7.40)
    if dim_tracker is None:
        dim_tracker = ValueTracker(0.0)

    state = {"t": 0.0}

    def mk_needle():
        ph_val = ph_tracker.get_value()
        jitter = 0.012 * np.sin(state["t"] * 5.2) + 0.006 * np.sin(state["t"] * 11.7) if tremble else 0.0
        yv = y_of(np.clip(ph_val + jitter, ph_min, ph_max))
        ncol = interpolate_color(ManimColor(WHITE), ManimColor(GREY), np.clip(dim_tracker.get_value(), 0.0, 1.0))
        op = 1.0 - 0.25 * np.clip(dim_tracker.get_value(), 0.0, 1.0)
        tri = Polygon(
            [x + 0.04, yv, 0],
            [x + 0.28, yv + 0.10, 0],
            [x + 0.28, yv - 0.10, 0],
            color=ncol,
            fill_color=ncol,
            fill_opacity=op,
            stroke_width=1.0,
        )
        bar = Line([x - 0.14, yv, 0], [x + 0.36, yv, 0], color=ncol, stroke_width=4.0, stroke_opacity=op)
        return VGroup(bar, tri)

    needle = always_redraw(mk_needle)
    if tremble:
        def tick_t(mob, dt):
            state["t"] += dt
        spine.add_updater(tick_t)

    g = VGroup(spine, ticks, tick_labels, window_band, title, needle)
    g.y_of = y_of
    g.spine = spine
    g.window_band = window_band
    g.title = title
    g.needle = needle
    g.ph_tracker = ph_tracker
    g.dim_tracker = dim_tracker
    g.x_axis = x
    return g


def make_window_callouts(gauge):
    """Build 'the window' label and non-overlapping pointer line for the full gauge."""
    win_label = T("the window", size=26, color=GOLD).move_to([5.62, 2.66, 0])
    # Ends cleanly at (4.58, 2.40), well clear of 'the window' letters
    win_arrow = Line([4.58, 2.40, 0], [4.28, 2.08, 0], color=GOLD, stroke_width=2.5)
    return win_label, win_arrow


def make_live_ratio(hco3_tr, co2_tr, pos=(0.70, 0.75, 0)):
    """Build a live ratio tag computed from hco3_tr / co2_tr so ratio always matches the bars."""
    def fmt_ratio():
        r = max(hco3_tr.get_value(), 0.1) / max(co2_tr.get_value(), 0.1)
        if abs(r - 20.0) < 0.35:
            txt = "20 : 1"
        elif abs(r - 14.0 / 1.2) < 0.35:
            txt = "12 : 1"
        elif r >= 9.95:
            txt = f"{r:.0f} : 1"
        elif abs(r - 1.25) < 0.03:
            txt = "1.25 : 1"
        else:
            txt = f"{r:.1f} : 1"
        return T(txt, size=32, color=GOLD, weight=BOLD).move_to(pos)

    return always_redraw(fmt_ratio)


def make_ghost_needle(gauge, ph_val=6.20, label_text="sealed: 6.2"):
    """Build a dim GREY ghost needle at ph_val with an optional label beside it."""
    yv = gauge.y_of(ph_val)
    x = gauge.x_axis
    tri = Polygon(
        [x + 0.04, yv, 0],
        [x + 0.26, yv + 0.09, 0],
        [x + 0.26, yv - 0.09, 0],
        color=GREY,
        fill_color=GREY,
        fill_opacity=0.75,
        stroke_width=1.0,
    )
    bar = Line([x - 0.12, yv, 0], [x + 0.32, yv, 0], color=GREY, stroke_width=3.5)
    g = VGroup(bar, tri)
    if label_text:
        lab = T(label_text, size=24, color=GREY).move_to([x + 1.25, yv, 0])
        g.add(lab)
        g.label = lab
    return g


def make_ha_grid(center=(0.85, 0.45, 0.0), spacing=0.40, delta_tracker=None, seed=7):
    """Build the 10x10 grid of 100 HA/A- discs driven by Henderson-Hasselbalch on delta_tracker."""
    if delta_tracker is None:
        delta_tracker = ValueTracker(0.0)
    rng = np.random.default_rng(seed)
    flip_order = rng.permutation(100)
    rank = np.empty(100, dtype=int)
    for r, idx in enumerate(flip_order):
        rank[idx] = r

    cx, cy, _ = center
    x0 = cx - 4.5 * spacing
    y0 = cy + 4.5 * spacing

    def build_grid():
        d = delta_tracker.get_value()
        n_deprot = int(round(100.0 * (10.0 ** d) / (1.0 + 10.0 ** d)))
        g = VGroup()
        for idx in range(100):
            row, col = divmod(idx, 10)
            pos = np.array([x0 + col * spacing, y0 - row * spacing, 0.0])
            is_deprot = rank[idx] < n_deprot
            if is_deprot:
                disc = Dot(pos, radius=0.142, color=PURPLE, fill_opacity=0.92)
                g.add(disc)
            else:
                disc = Dot(pos, radius=0.142, color=WHITE, fill_opacity=0.92)
                proton = Dot(pos + np.array([0.085, 0.085, 0.0]), radius=0.055, color=ORANGE, fill_opacity=1.0)
                g.add(VGroup(disc, proton))
        return g

    grid = always_redraw(build_grid)
    grid.delta_tracker = delta_tracker
    grid.flip_order = flip_order
    grid.rank = rank
    grid.pos_of = lambda idx: np.array([x0 + (idx % 10) * spacing, y0 - (idx // 10) * spacing, 0.0])
    return grid


def make_ph_slider(center=(0.85, -1.94, 0.0), width=4.4, delta_tracker=None):
    """Build the horizontal 'pH - pKa' slider from -2 to +2 with a GOLD knob."""
    if delta_tracker is None:
        delta_tracker = ValueTracker(0.0)
    cx, cy, _ = center
    x_left, x_right = cx - width / 2.0, cx + width / 2.0
    x_of = lambda d: cx + (d / 2.0) * (width / 2.0)

    track = Line([x_left, cy, 0], [x_right, cy, 0], color=GREY, stroke_width=4.0)
    ticks = VGroup()
    tlabels = VGroup()
    for d in (-2, -1, 0, 1, 2):
        xd = x_of(d)
        tk = Line([xd, cy, 0], [xd, cy - 0.14, 0], color=GREY, stroke_width=3.0)
        ticks.add(tk)
        txt = f"{d:+d}" if d != 0 else "0"
        lb = M(txt, size=24, color=TEXT).next_to(tk, DOWN, buff=0.10)
        tlabels.add(lb)
    title = T("pH − pKa", size=28, color=GOLD).next_to([x_left, cy, 0], LEFT, buff=0.25)
    knob = always_redraw(
        lambda: Dot([x_of(np.clip(delta_tracker.get_value(), -2.0, 2.0)), cy, 0], radius=0.14, color=GOLD, stroke_color=WHITE, stroke_width=2.0)
    )
    g = VGroup(track, ticks, tlabels, title, knob)
    g.x_of = x_of
    g.y_line = cy
    g.knob = knob
    return g


BLOOD_GLASS = (-6.1, 2.7, -2.35, 1.45)
HCO3_X = -3.80
CO2_X = -1.70
BAR_W = 1.40
BAR_BASE_Y = -1.75
BAR_SCALE = 0.114


def make_blood_bars(hco3_tr, co2_tr, show_nums=True, show_bubbles=True, seed=19):
    """Build the bicarbonate (PURPLE) and CO2 (WHITE) vertical bars driven by ValueTrackers."""
    def mk_hco3():
        val = max(0.1, hco3_tr.get_value())
        h = val * BAR_SCALE
        return Rectangle(
            width=BAR_W,
            height=h,
            color=PURPLE,
            stroke_width=2.5,
            fill_color=PURPLE,
            fill_opacity=0.76,
        ).move_to([HCO3_X, BAR_BASE_Y + h / 2.0, 0])

    def mk_co2():
        val = max(0.1, co2_tr.get_value())
        h = val * BAR_SCALE
        return Rectangle(
            width=BAR_W,
            height=h,
            color=WHITE,
            stroke_width=2.5,
            fill_color=WHITE,
            fill_opacity=0.26,
        ).move_to([CO2_X, BAR_BASE_Y + h / 2.0, 0])

    hco3_bar = always_redraw(mk_hco3)
    co2_bar = always_redraw(mk_co2)
    base_line = Line([HCO3_X - 0.92, BAR_BASE_Y, 0], [CO2_X + 0.92, BAR_BASE_Y, 0], color=GREY, stroke_width=2.5)
    lab_hco3 = T("bicarbonate", size=26, color=PURPLE).move_to([HCO3_X, BAR_BASE_Y - 0.30, 0])
    lab_co2 = T("CO₂", size=26, color=WHITE).move_to([CO2_X, BAR_BASE_Y - 0.30, 0])

    g = VGroup(base_line, hco3_bar, co2_bar, lab_hco3, lab_co2)

    if show_nums:
        num_hco3 = always_redraw(
            lambda: M(f"{hco3_tr.get_value():.0f} mM", size=26, color=PURPLE).move_to(
                [HCO3_X, BAR_BASE_Y + max(0.1, hco3_tr.get_value()) * BAR_SCALE + 0.26, 0]
            )
        )
        num_co2 = always_redraw(
            lambda: M(f"{co2_tr.get_value():.1f} mM", size=26, color=WHITE).move_to(
                [CO2_X, BAR_BASE_Y + max(0.1, co2_tr.get_value()) * BAR_SCALE + 0.26, 0]
            )
        )
        g.add(num_hco3, num_co2)
        g.num_hco3, g.num_co2 = num_hco3, num_co2

    if show_bubbles:
        rng = np.random.default_rng(seed)
        bub_specs = [(rng.uniform(-0.45, 0.45), rng.uniform(0.0, 1.0), rng.uniform(0.35, 0.70)) for _ in range(8)]
        bub_t = {"t": 0.0}

        def mk_bubbles():
            h = max(0.12, co2_tr.get_value() * BAR_SCALE)
            out = VGroup()
            n_show = 2 if h < 0.20 else (5 if h < 0.60 else 8)
            for dx, ph, spd in bub_specs[:n_show]:
                frac = (ph + bub_t["t"] * spd) % 1.0
                yb = BAR_BASE_Y + 0.06 + frac * max(0.04, h - 0.12)
                c = Circle(radius=0.05, color=WHITE, stroke_width=2.0, fill_color=WHITE, fill_opacity=0.50)
                c.move_to([CO2_X + dx, yb, 0])
                out.add(c)
            return out

        bubbles = always_redraw(mk_bubbles)
        base_line.add_updater(lambda m, dt: bub_t.__setitem__("t", bub_t["t"] + dt))
        g.add(bubbles)
        g.bubbles = bubbles

    g.hco3_bar = hco3_bar
    g.co2_bar = co2_bar
    g.lab_hco3 = lab_hco3
    g.lab_co2 = lab_co2
    return g


def make_tube_and_lungs(breath_t=None, label=True):
    """Build the open tube above the CO2 bar leading to two rounded lung outlines that slowly breathe."""
    if breath_t is None:
        breath_t = {"t": 0.0}
    tx = CO2_X
    tube = VGroup(
        Line([tx - 0.18, 1.43, 0], [tx - 0.18, 2.08, 0], color=BLUE, stroke_width=3.2),
        Line([tx + 0.18, 1.43, 0], [tx + 0.18, 2.08, 0], color=BLUE, stroke_width=3.2),
    )

    def mk_lungs():
        s = 1.0 + 0.09 * np.sin(breath_t["t"] * 1.8)
        lobe_l = RoundedRectangle(
            corner_radius=0.35, width=0.85 * s, height=1.15 * s,
            color=TEXT, stroke_width=3.0, fill_color=BLUE, fill_opacity=0.12,
        ).move_to([tx - 0.56 * s, 2.65, 0])
        lobe_r = RoundedRectangle(
            corner_radius=0.35, width=0.85 * s, height=1.15 * s,
            color=TEXT, stroke_width=3.0, fill_color=BLUE, fill_opacity=0.12,
        ).move_to([tx + 0.56 * s, 2.65, 0])
        bridge = Line([tx - 0.18, 2.08, 0], [tx + 0.18, 2.08, 0], color=TEXT, stroke_width=2.5)
        return VGroup(lobe_l, lobe_r, bridge)

    lungs = always_redraw(mk_lungs)
    tube.add_updater(lambda m, dt: breath_t.__setitem__("t", breath_t["t"] + dt))
    g = VGroup(tube, lungs)
    if label:
        lab = T("breathing", size=28, color=TEXT).move_to([tx + 2.15, 2.65, 0])
        g.add(lab)
        g.label = lab
    g.tube = tube
    g.lungs = lungs
    g.breath_t = breath_t
    return g


def make_acid_funnel():
    """Build the GOLD acid funnel above the bicarbonate side with '+10 mM acid' label."""
    fx = HCO3_X
    funnel = Polygon(
        [fx - 0.50, 2.20, 0],
        [fx + 0.50, 2.20, 0],
        [fx + 0.14, 1.55, 0],
        [fx - 0.14, 1.55, 0],
        color=GOLD,
        stroke_width=3.0,
        fill_color=GOLD,
        fill_opacity=0.16,
    )
    lab = T("+10 mM acid", size=26, color=ORANGE).move_to([fx - 0.45, 2.60, 0])
    return VGroup(funnel, lab)


def make_sealed_lid(x0=-6.1, x1=2.7, y=1.45):
    """Build the GOLD lid across the top of the glass."""
    return RoundedRectangle(
        corner_radius=0.06,
        width=(x1 - x0) + 0.12,
        height=0.16,
        color=GOLD,
        stroke_width=2.5,
        fill_color=GOLD,
        fill_opacity=0.75,
    ).move_to([(x0 + x1) / 2.0, y + 0.08, 0])


# ------------------------------------------------------------------ scenes
class S00LinkAndQuestion(SpokenScene):
    def construct(self):
        glass_grp, water, outline = make_glass_and_water(-6.2, 6.2, -3.2, 3.0)
        ball = make_folded_ball(center=(0.0, 0.0, 0.0), scale=1.35, seed=11, with_charges=False)
        breath_state = {"t": 0.0}
        base_scale = {"s": 1.0}

        def breathe_ball(m, dt):
            breath_state["t"] += dt
            f = 1.0 + 0.025 * np.sin(breath_state["t"] * 2.1)
            m.core.scale(f / base_scale["s"])
            base_scale["s"] = f

        ball.add_updater(breathe_ball)
        self.add(glass_grp, ball)

        self.at("add up to a fold")
        flicker = VGroup(*[
            Line(ball.beads[i].get_center(), ball.beads[(i + 1) % 12].get_center(), color=GREEN, stroke_width=3.5)
            for i in (1, 3, 6, 9)
        ])
        self.play(FadeIn(flicker, run_time=0.45))
        self.play(FadeOut(flicker, run_time=0.45))

        self.at("need charges")
        b_pos = ball.beads[1]
        b_neg = ball.beads[2]
        p_out = b_pos.get_center() / np.linalg.norm(b_pos.get_center())
        n_out = b_neg.get_center() / np.linalg.norm(b_neg.get_center())
        plus_tag = T("+", size=30, color=TEXT, weight=BOLD).move_to(b_pos.get_center() + p_out * 0.34)
        minus_tag = T("−", size=30, color=TEXT, weight=BOLD).move_to(b_neg.get_center() + n_out * 0.34)
        ionic_link = Line(b_pos.get_center(), b_neg.get_center(), color=GREEN, stroke_width=5.5)
        self.play(FadeIn(plus_tag), FadeIn(minus_tag), GrowFromCenter(ionic_link), run_time=0.6)

        self.at("pH decides")
        proton = Dot(b_neg.get_center() + n_out * 1.4 + RIGHT * 0.8, radius=0.11, color=ORANGE, fill_opacity=1.0)
        slack_link = ArcBetweenPoints(b_pos.get_center(), b_neg.get_center(), angle=-0.8, color=GREY, stroke_width=2.5)
        self.play(FadeIn(proton), run_time=0.25)
        self.play(
            proton.animate.move_to(b_neg.get_center() + n_out * 0.22),
            FadeOut(minus_tag),
            Transform(ionic_link, slack_link),
            run_time=0.85,
        )
        taut_link = Line(b_pos.get_center(), b_neg.get_center(), color=GREEN, stroke_width=5.5)
        minus_back = T("−", size=30, color=TEXT, weight=BOLD).move_to(b_neg.get_center() + n_out * 0.34)
        self.play(
            proton.animate.shift(RIGHT * 1.3 + UP * 0.8).set_opacity(0.0),
            FadeIn(minus_back),
            Transform(ionic_link, taut_link),
            run_time=0.75,
        )
        self.remove(proton)

        self.at("Blood holds")
        ball.remove_updater(breathe_ball)
        self.play(FadeOut(plus_tag), FadeOut(minus_back), FadeOut(ionic_link), run_time=0.35)
        new_outline = VMobject(stroke_color=BLUE, stroke_width=3.8, fill_opacity=0)
        new_outline.set_points_as_corners([
            [-6.2, 2.65, 0],
            [-6.2, -3.2, 0],
            [3.0, -3.2, 0],
            [3.0, 2.65, 0],
        ])
        ph_tr = ValueTracker(7.40)
        gauge = make_ph_gauge(x=4.10, y0=-2.20, y1=2.60, compact=False, ph_tracker=ph_tr, tremble=True)
        win_label, win_arrow = make_window_callouts(gauge)

        self.play(
            ball.animate.scale(0.38).move_to([-4.8, 1.75, 0]),
            Transform(outline, new_outline),
            FadeIn(gauge),
            FadeIn(win_label),
            Create(win_arrow),
            *([self._remap_water_anim(water, -6.2, 3.0, -3.2, 2.65)]),
            run_time=1.1,
        )

        self.at("buffer is poor")
        poor_chip = chip("poor\nbuffer?", color=GOLD, size=24).move_to([5.50, 0.85, 0])
        self.play(FadeIn(poor_chip, shift=DOWN * 0.25), run_time=0.6)

        self.at("how does it hold")
        qmark = T("?", size=52, color=GOLD, weight=BOLD).move_to([4.92, 1.85, 0])
        self.play(FadeIn(qmark, scale=0.7), run_time=0.35)
        self.play(qmark.animate.scale(1.22), rate_func=there_and_back, run_time=0.55)
        self.finish()

    @staticmethod
    def _remap_water_anim(water, x0, x1, y0, y1):
        cols, rows = 14, 10
        pad_x, pad_y = 0.25, 0.22
        w = (x1 - x0) - 2 * pad_x
        h = (y1 - y0) - 2 * pad_y
        new_rx, new_ry = 0.42 * (w / cols), 0.42 * (h / rows)
        for k, d in enumerate(water):
            r, c = divmod(k, cols)
            d._old_home = d._home.copy()
            d._old_rx, d._old_ry = d._cell_rx, d._cell_ry
            d._new_home = np.array([x0 + pad_x + (c + 0.5) * (w / cols), y0 + pad_y + (r + 0.5) * (h / rows), 0.0])
            d._new_rx, d._new_ry = new_rx, new_ry
        state = {"a": 0.0}

        def remap(mob, alpha):
            da = alpha - state["a"]
            state["a"] = alpha
            for d in mob:
                d._home = d._old_home + alpha * (d._new_home - d._old_home)
                d._cell_rx = d._old_rx + alpha * (d._new_rx - d._old_rx)
                d._cell_ry = d._old_ry + alpha * (d._new_ry - d._old_ry)
                d.shift(da * (d._new_home - d._old_home))

        return UpdateFromAlphaFunc(water, remap)


class S01Title(NarratedScene):
    def construct(self):
        glass_grp, water, outline = make_glass_and_water(-6.2, 3.0, -3.2, 2.65)
        ball = make_folded_ball(center=(-4.8, 1.75, 0.0), scale=0.51, seed=11, with_charges=False)
        ph_tr = ValueTracker(7.40)
        gauge = make_ph_gauge(x=4.10, y0=-2.20, y1=2.60, compact=False, ph_tracker=ph_tr, tremble=True)
        win_label, win_arrow = make_window_callouts(gauge)
        poor_chip = chip("poor\nbuffer?", color=GOLD, size=24).move_to([5.50, 0.85, 0])
        qmark = T("?", size=52, color=GOLD, weight=BOLD).move_to([4.92, 1.85, 0])
        title = T("A Buffer That Breathes", size=44, color=GOLD, font=TITLE_FONT).move_to([-1.6, 3.12, 0])

        self.add(glass_grp, ball, gauge, win_label, win_arrow, poor_chip, qmark)
        self.play(
            FadeIn(title, shift=DOWN * 0.1),
            FadeOut(qmark),
            FadeOut(poor_chip),
            FadeOut(ball),
            run_time=0.9,
        )
        self.wait(1.1)


class S02Pka(SpokenScene):
    def construct(self):
        glass_grp, water, outline = make_glass_and_water(-6.2, 4.1, -3.1, 2.75)
        ph_tr = ValueTracker(7.40)
        gauge = make_ph_gauge(x=5.30, y0=-1.80, y1=1.80, compact=True, ph_tracker=ph_tr, tremble=True)

        delta_tr = ValueTracker(-2.0)
        grid = make_ha_grid(center=(0.85, 0.35, 0.0), spacing=0.40, delta_tracker=delta_tr, seed=7)
        slider = make_ph_slider(center=(0.85, -1.94, 0.0), width=4.4, delta_tracker=delta_tr)

        self.add(glass_grp, gauge)
        self.play(FadeIn(grid), FadeIn(slider), run_time=1.0)

        self.at("below its pka")
        self.play(slider.knob.animate.scale(1.2), rate_func=there_and_back, run_time=1.4)

        self.at("above")
        rng = np.random.default_rng(21)
        loose_protons = VGroup()
        for idx in grid.flip_order[1:19]:
            p = Dot(grid.pos_of(idx) + np.array([0.085, 0.085, 0]), radius=0.06, color=ORANGE)
            p._drift = np.array([rng.uniform(-0.8, 0.8), rng.uniform(0.5, 1.1), 0.0])
            loose_protons.add(p)
        self.play(
            delta_tr.animate.set_value(2.0),
            LaggedStart(*[p.animate.shift(p._drift).set_opacity(0.0) for p in loose_protons], lag_ratio=0.05),
            run_time=2.0,
        )
        self.remove(loose_protons)

        self.at("at the pka")
        half_label = T("at the pKa: 50%", size=28, color=GOLD).move_to([0.85, 2.64, 0])
        self.play(delta_tr.animate.set_value(0.0), run_time=1.0)
        self.play(FadeIn(half_label), run_time=0.4)
        self.finish()


class S03Tenfold(SpokenScene):
    def construct(self):
        glass_grp, water, outline = make_glass_and_water(-6.2, 4.1, -3.1, 2.75)
        ph_tr = ValueTracker(7.40)
        gauge = make_ph_gauge(x=5.30, y0=-1.80, y1=1.80, compact=True, ph_tracker=ph_tr, tremble=True)

        delta_tr = ValueTracker(0.0)
        grid = make_ha_grid(center=(0.85, 0.35, 0.0), spacing=0.40, delta_tracker=delta_tr, seed=7)
        slider = make_ph_slider(center=(0.85, -1.94, 0.0), width=4.4, delta_tracker=delta_tr)
        top_tag = T("at the pKa: 50%", size=28, color=GOLD).move_to([0.85, 2.64, 0])

        self.add(glass_grp, gauge, grid, slider, top_tag)

        self.at("shifts the ratio")
        tag_10 = T("10 : 1", size=30, color=GOLD, weight=BOLD).move_to([0.85, 2.64, 0])
        released = VGroup(*[
            Dot(grid.pos_of(idx) + np.array([0.085, 0.085, 0]), radius=0.055, color=ORANGE)
            for idx in grid.flip_order[50:66]
        ])
        self.play(
            delta_tr.animate.set_value(1.0),
            LaggedStart(*[p.animate.shift(UP * 0.7 + LEFT * 0.3).set_opacity(0.0) for p in released], lag_ratio=0.05),
            swap(top_tag, tag_10, run_time=1.0),
            run_time=2.8,
        )
        self.remove(released)

        self.at("about 91")
        self.play(tag_10.animate.scale(1.15), rate_func=there_and_back, run_time=1.5)

        self.at("two units")
        tag_100 = T("100 : 1", size=30, color=GOLD, weight=BOLD).move_to([0.85, 2.64, 0])
        self.play(
            delta_tr.animate.set_value(2.0),
            swap(tag_10, tag_100, run_time=0.8),
            run_time=2.2,
        )

        self.at("is worth about")
        ledger_row = boxed_label("1 pH unit ≈ 5.9 kJ/mol", color=GOLD, size=26).move_to([-3.65, 0.85, 0])
        b1 = Dot([-4.25, -0.20, 0], radius=0.14, color=GREEN)
        b2 = Dot([-3.05, -0.20, 0], radius=0.14, color=GREEN)
        bond_ln = Line(b1.get_center(), b2.get_center(), color=GREEN, stroke_width=4.0)
        bond_lab = T("one weak bond", size=28, color=GREEN).move_to([-3.65, -0.82, 0])
        bond_grp = VGroup(bond_ln, b1, b2, bond_lab)

        self.play(FadeIn(ledger_row, shift=RIGHT * 0.3), FadeIn(bond_grp), run_time=0.8)
        self.play(bond_ln.animate.set_stroke(width=8.0), rate_func=there_and_back, run_time=0.7)
        self.finish()


class S04FlaskRule(SpokenScene):
    def construct(self):
        glass_grp, water, outline = make_glass_and_water(-6.2, 4.1, -3.1, 2.75)
        ph_tr = ValueTracker(7.40)
        gauge = make_ph_gauge(x=5.30, y0=-1.80, y1=1.80, compact=True, ph_tracker=ph_tr, tremble=True)

        delta_tr = ValueTracker(2.0)
        grid = make_ha_grid(center=(0.85, 0.35, 0.0), spacing=0.40, delta_tracker=delta_tr, seed=7)
        slider = make_ph_slider(center=(0.85, -1.94, 0.0), width=4.4, delta_tracker=delta_tr)
        tag_100 = T("100 : 1", size=30, color=GOLD, weight=BOLD).move_to([0.85, 2.64, 0])
        ledger_row = boxed_label("1 pH unit ≈ 5.9 kJ/mol", color=GOLD, size=26).move_to([-3.65, 0.85, 0])
        b1 = Dot([-4.25, -0.20, 0], radius=0.14, color=GREEN)
        b2 = Dot([-3.05, -0.20, 0], radius=0.14, color=GREEN)
        bond_ln = Line(b1.get_center(), b2.get_center(), color=GREEN, stroke_width=4.0)
        bond_lab = T("one weak bond", size=28, color=GREEN).move_to([-3.65, -0.82, 0])
        bond_grp = VGroup(bond_ln, b1, b2, bond_lab)

        self.add(glass_grp, gauge, grid, slider, tag_100, ledger_row, bond_grp)
        self.play(
            FadeOut(ledger_row),
            FadeOut(bond_grp),
            FadeOut(tag_100),
            delta_tr.animate.set_value(0.0),
            run_time=1.4,
        )

        self.at("ready to absorb")
        rain1 = VGroup(*[
            Dot([0.85 + dx, 2.55, 0], radius=0.065, color=ORANGE)
            for dx in (-1.1, -0.35, 0.4, 1.15)
        ])
        self.play(FadeIn(rain1), run_time=0.25)
        self.play(
            rain1.animate.shift(DOWN * 2.0).set_opacity(0.0),
            delta_tr.animate.set_value(-0.08),
            run_time=1.4,
        )
        self.play(delta_tr.animate.set_value(0.0), run_time=0.8)
        self.remove(rain1)

        self.at("far away")
        self.play(delta_tr.animate.set_value(-2.0), run_time=1.0)
        rain2 = VGroup(*[
            Dot([-5.3 + k * 0.36, 2.55, 0], radius=0.065, color=ORANGE)
            for k in range(6)
        ])
        targets = [[-5.4 + k * 0.40, -2.55 + (k % 2) * 0.25, 0] for k in range(6)]
        self.play(FadeIn(rain2), run_time=0.25)
        self.play(*[p.animate.move_to(t) for p, t in zip(rain2, targets)], run_time=1.2)

        self.at("sealed flask")
        lid = make_sealed_lid(x0=-6.2, x1=4.1, y=2.75)
        lid_lab = T("sealed flask", size=28, color=GOLD).move_to([-1.0, 3.18, 0])
        x_m1, x_p1 = slider.x_of(-1), slider.x_of(1)
        br_y = -2.56
        bracket = VGroup(
            Line([x_m1, br_y + 0.12, 0], [x_m1, br_y, 0], color=GOLD, stroke_width=3.5),
            Line([x_m1, br_y, 0], [x_p1, br_y, 0], color=GOLD, stroke_width=3.5),
            Line([x_p1, br_y, 0], [x_p1, br_y + 0.12, 0], color=GOLD, stroke_width=3.5),
        )
        best_lab = T("works best", size=26, color=GOLD).move_to([0.85, -2.88, 0])
        self.play(
            FadeIn(lid, shift=DOWN * 0.25),
            FadeIn(lid_lab),
            Create(bracket),
            FadeIn(best_lab),
            run_time=1.0,
        )
        self.finish()


class S05Blood(SpokenScene):
    def construct(self):
        x0, x1, y0, y1 = BLOOD_GLASS
        glass_grp, water, outline = make_glass_and_water(x0, x1, y0, y1)
        lid = make_sealed_lid(x0=x0, x1=x1, y=y1)
        ph_tr = ValueTracker(7.40)
        gauge = make_ph_gauge(x=4.10, y0=-2.20, y1=2.60, compact=False, ph_tracker=ph_tr, tremble=True)
        win_label, win_arrow = make_window_callouts(gauge)

        hco3_tr = ValueTracker(0.5)
        co2_tr = ValueTracker(0.2)
        bars = make_blood_bars(hco3_tr, co2_tr, show_nums=False, show_bubbles=True)

        self.add(glass_grp, lid, gauge, win_label, win_arrow)
        self.play(FadeIn(bars), run_time=0.5)

        self.at("bicarbonate")
        self.play(hco3_tr.animate.set_value(24.0), run_time=1.1)
        self.at("carbon dioxide")
        self.play(co2_tr.animate.set_value(1.2), run_time=1.4)

        self.at("its effective")
        y_pka = gauge.y_of(6.1)
        pka_tick = Line([4.10, y_pka, 0], [4.38, y_pka, 0], color=GOLD, stroke_width=4.0)
        pka_lab = T("pKa 6.1", size=26, color=GOLD).move_to([5.35, y_pka, 0])
        self.play(Create(pka_tick), FadeIn(pka_lab), run_time=1.2)

        self.at("blood sits at")
        y_74 = gauge.y_of(7.4)
        bx = 4.55
        off_bracket = VGroup(
            Line([bx - 0.12, y_pka + 0.05, 0], [bx, y_pka + 0.05, 0], color=GOLD, stroke_width=3.0),
            Line([bx, y_pka + 0.05, 0], [bx, y_74 - 0.05, 0], color=GOLD, stroke_width=3.0),
            Line([bx - 0.12, y_74 - 0.05, 0], [bx, y_74 - 0.05, 0], color=GOLD, stroke_width=3.0),
        )
        off_lab = T("1.3 units", size=26, color=GOLD).move_to([5.45, (y_pka + y_74) / 2.0, 0])
        self.play(Create(off_bracket), FadeIn(off_lab), run_time=2.2)

        self.at("about twenty")
        ratio_tag = T("20 : 1", size=32, color=GOLD, weight=BOLD).move_to([0.70, 0.75, 0])
        self.play(FadeIn(ratio_tag), run_time=0.8)
        self.finish()


class S06Sealed(SpokenScene):
    def construct(self):
        x0, x1, y0, y1 = BLOOD_GLASS
        glass_grp, water, outline = make_glass_and_water(x0, x1, y0, y1)
        lid = make_sealed_lid(x0=x0, x1=x1, y=y1)

        hco3_tr = ValueTracker(24.0)
        co2_tr = ValueTracker(1.2)
        ph_tr = ValueTracker(7.40)
        ph_tr.add_updater(lambda m: m.set_value(6.1 + np.log10(max(hco3_tr.get_value(), 0.1) / max(co2_tr.get_value(), 0.1))))

        gauge = make_ph_gauge(x=4.10, y0=-2.20, y1=2.60, compact=False, ph_tracker=ph_tr, tremble=True)
        win_label, win_arrow = make_window_callouts(gauge)
        y_pka = gauge.y_of(6.1)
        pka_tick = Line([4.10, y_pka, 0], [4.38, y_pka, 0], color=GOLD, stroke_width=4.0)
        pka_lab = T("pKa 6.1", size=26, color=GOLD).move_to([5.35, y_pka, 0])

        bars = make_blood_bars(hco3_tr, co2_tr, show_nums=True, show_bubbles=True)
        bars.num_hco3.set_opacity(0.0)
        bars.num_co2.set_opacity(0.0)
        ratio_tag = make_live_ratio(hco3_tr, co2_tr, pos=(0.70, 0.75, 0))

        self.add(glass_grp, lid, gauge, win_label, win_arrow, pka_tick, pka_lab, bars, ratio_tag, ph_tr)

        self.at("24")
        bars.num_hco3.set_opacity(1.0)
        self.play(bars.num_hco3.animate.scale(1.15), rate_func=there_and_back, run_time=1.0)

        self.at("1")
        bars.num_co2.set_opacity(1.0)
        self.play(bars.num_co2.animate.scale(1.15), rate_func=there_and_back, run_time=1.2)

        self.at("seal the flask")
        funnel = make_acid_funnel()
        self.play(
            lid.animate.set_fill(opacity=1.0),
            FadeIn(funnel, shift=DOWN * 0.2),
            run_time=0.9,
        )

        self.at("add ten millimolar")
        acid_dots = VGroup(*[
            Dot([HCO3_X + dx, 2.10 + dy, 0], radius=0.065, color=ORANGE)
            for dx, dy in [(-0.25, 0.1), (0.0, 0.25), (0.22, 0.05), (-0.12, -0.05), (0.15, 0.22), (-0.30, 0.28)]
        ])
        self.play(FadeIn(acid_dots), run_time=0.25)
        self.play(
            *[d.animate.move_to([HCO3_X + (k - 2.5) * 0.18, BAR_BASE_Y + 2.6, 0]) for k, d in enumerate(acid_dots)],
            run_time=1.1,
        )

        self.at("turns one bicarbonate")
        convert_bubbles = VGroup(*[
            Circle(radius=0.065, color=WHITE, stroke_width=2.2, fill_color=WHITE, fill_opacity=0.55).move_to([HCO3_X, BAR_BASE_Y + 2.4, 0])
            for _ in range(4)
        ])
        self.play(
            FadeOut(acid_dots),
            LaggedStart(
                *[b.animate.move_to([CO2_X + (k - 1.5) * 0.18, BAR_BASE_Y + 0.45, 0]).set_opacity(0.0) for k, b in enumerate(convert_bubbles)],
                lag_ratio=0.18,
            ),
            hco3_tr.animate.set_value(21.5),
            co2_tr.animate.set_value(3.7),
            run_time=2.4,
        )
        self.remove(convert_bubbles)
        self.finish()


class S07SealedResult(SpokenScene):
    def construct(self):
        x0, x1, y0, y1 = BLOOD_GLASS
        glass_grp, water, outline = make_glass_and_water(x0, x1, y0, y1)
        lid = make_sealed_lid(x0=x0, x1=x1, y=y1)

        hco3_tr = ValueTracker(21.5)
        co2_tr = ValueTracker(3.7)
        ph_tr = ValueTracker(6.1 + np.log10(21.5 / 3.7))
        ph_tr.add_updater(lambda m: m.set_value(6.1 + np.log10(max(hco3_tr.get_value(), 0.1) / max(co2_tr.get_value(), 0.1))))
        dim_tr = ValueTracker(0.0)

        gauge = make_ph_gauge(x=4.10, y0=-2.20, y1=2.60, compact=False, ph_tracker=ph_tr, tremble=False, dim_tracker=dim_tr)
        win_label, win_arrow = make_window_callouts(gauge)
        y_pka = gauge.y_of(6.1)
        pka_tick = Line([4.10, y_pka, 0], [4.38, y_pka, 0], color=GOLD, stroke_width=4.0)
        pka_lab = T("pKa 6.1", size=26, color=GOLD).move_to([5.35, y_pka, 0])

        bars = make_blood_bars(hco3_tr, co2_tr, show_nums=True, show_bubbles=True)
        ratio_tag = make_live_ratio(hco3_tr, co2_tr, pos=(0.70, 0.75, 0))

        self.add(glass_grp, lid, gauge, win_label, win_arrow, pka_tick, pka_lab, bars, ratio_tag, ph_tr)

        self.at("bicarbonate falls")
        self.play(hco3_tr.animate.set_value(14.0), run_time=2.0)

        self.at("carbon dioxide piles up")
        lid_bubbles = VGroup(*[
            Circle(radius=0.06, color=WHITE, stroke_width=2.0, fill_color=WHITE, fill_opacity=0.5).move_to([CO2_X + dx, y1 - 0.12, 0])
            for dx in (-0.42, -0.14, 0.15, 0.40)
        ])
        self.play(co2_tr.animate.set_value(11.2), FadeIn(lid_bubbles), run_time=2.6)

        self.at("the ratio collapses")
        self.play(ratio_tag.animate.scale(1.18), rate_func=there_and_back, run_time=0.9)

        self.at("the ph drops")
        sealed_tag = T("sealed:\nabout 6.2", size=24, color=GREY).move_to([5.42, gauge.y_of(6.20) + 0.35, 0])
        self.play(dim_tr.animate.set_value(1.0), FadeIn(sealed_tag), run_time=0.9)
        self.finish()


class S08Predict(SpokenScene):
    def construct(self):
        x0, x1, y0, y1 = BLOOD_GLASS
        glass_grp, water, outline = make_glass_and_water(x0, x1, y0, y1, meniscus=True)
        lid = make_sealed_lid(x0=x0, x1=x1, y=y1)

        hco3_tr = ValueTracker(14.0)
        co2_tr = ValueTracker(11.2)
        ph_tr = ValueTracker(6.20)

        gauge = make_ph_gauge(x=4.10, y0=-2.20, y1=2.60, compact=False, ph_tracker=ph_tr, tremble=True)
        win_label, win_arrow = make_window_callouts(gauge)
        y_pka = gauge.y_of(6.1)
        pka_tick = Line([4.10, y_pka, 0], [4.38, y_pka, 0], color=GOLD, stroke_width=4.0)
        pka_lab = T("pKa 6.1", size=26, color=GOLD).move_to([5.35, y_pka, 0])

        ghost = make_ghost_needle(gauge, ph_val=6.20, label_text="sealed: 6.2")
        ghost.label.move_to([5.42, gauge.y_of(6.20) + 0.32, 0])

        bars = make_blood_bars(hco3_tr, co2_tr, show_nums=True, show_bubbles=True)
        ratio_tag = T("1.25 : 1", size=32, color=GOLD, weight=BOLD).move_to([0.70, 0.75, 0])

        self.add(glass_grp, lid, gauge, win_label, win_arrow, pka_tick, pka_lab, ghost, bars, ratio_tag)

        ratio_20 = T("20 : 1", size=32, color=GOLD, weight=BOLD).move_to([0.70, 0.75, 0])
        self.play(
            hco3_tr.animate.set_value(24.0),
            co2_tr.animate.set_value(1.2),
            ph_tr.animate.set_value(7.40),
            swap(ratio_tag, ratio_20, run_time=0.6),
            run_time=0.6,
        )

        self.at("open the flask")
        lungs_grp = make_tube_and_lungs(label=True)
        self.play(
            lid.animate.shift(UP * 0.6).set_opacity(0.0),
            FadeIn(lungs_grp),
            run_time=0.9,
        )
        self.remove(lid)

        self.at("breathing carries")
        exhale_bubs = VGroup(*[
            Circle(radius=0.065, color=WHITE, stroke_width=2.0, fill_color=WHITE, fill_opacity=0.7).move_to([CO2_X, -1.2, 0])
            for _ in range(4)
        ])
        self.play(
            LaggedStart(*[b.animate.move_to([CO2_X, 3.3, 0]).set_opacity(0.0) for b in exhale_bubs], lag_ratio=0.32),
            run_time=4.2,
        )
        self.remove(exhale_bubs)

        self.at("same acid")
        self.play(bars.num_co2.animate.scale(1.15), rate_func=there_and_back, run_time=0.8)

        self.at("where does the ph land")
        qcard = question_card("Open flask: where does pH land?", y=-3.05, size=32)
        qmark = T("?", size=48, color=GOLD, weight=BOLD).move_to([4.85, gauge.y_of(7.40) - 0.10, 0])
        self.play(FadeIn(qcard), FadeIn(qmark), run_time=0.7)
        self.finish()


class S09Think(PredictPause):
    QUESTION = "Open flask: where does pH land?"
    CARD = {"y": -3.05, "size": 32}
    RING_AT = (5.9, -3.05, 0)
    SECONDS = 4.5

    def backdrop(self):
        x0, x1, y0, y1 = BLOOD_GLASS
        glass_grp, _, _ = make_glass_and_water(x0, x1, y0, y1, meniscus=True)
        hco3_tr = ValueTracker(24.0)
        co2_tr = ValueTracker(1.2)
        ph_tr = ValueTracker(7.40)

        gauge = make_ph_gauge(x=4.10, y0=-2.20, y1=2.60, compact=False, ph_tracker=ph_tr, tremble=True)
        win_label, win_arrow = make_window_callouts(gauge)
        y_pka = gauge.y_of(6.1)
        pka_tick = Line([4.10, y_pka, 0], [4.38, y_pka, 0], color=GOLD, stroke_width=4.0)
        pka_lab = T("pKa 6.1", size=26, color=GOLD).move_to([5.35, y_pka, 0])

        ghost = make_ghost_needle(gauge, ph_val=6.20, label_text="sealed: 6.2")
        ghost.label.move_to([5.42, gauge.y_of(6.20) + 0.32, 0])

        bars = make_blood_bars(hco3_tr, co2_tr, show_nums=True, show_bubbles=True)
        ratio_tag = T("20 : 1", size=32, color=GOLD, weight=BOLD).move_to([0.70, 0.75, 0])
        lungs_grp = make_tube_and_lungs(label=True)
        qmark = T("?", size=48, color=GOLD, weight=BOLD).move_to([4.85, gauge.y_of(7.40) - 0.10, 0])

        return VGroup(glass_grp, gauge, win_label, win_arrow, pka_tick, pka_lab, ghost, bars, ratio_tag, lungs_grp, qmark)


class S10OpenResult(SpokenScene):
    def construct(self):
        x0, x1, y0, y1 = BLOOD_GLASS
        glass_grp, water, outline = make_glass_and_water(x0, x1, y0, y1, meniscus=True)
        hco3_tr = ValueTracker(24.0)
        co2_tr = ValueTracker(1.2)
        ph_tr = ValueTracker(7.40)
        ph_tr.add_updater(lambda m: m.set_value(6.1 + np.log10(max(hco3_tr.get_value(), 0.1) / max(co2_tr.get_value(), 0.1))))

        gauge = make_ph_gauge(x=4.10, y0=-2.20, y1=2.60, compact=False, ph_tracker=ph_tr, tremble=False)
        win_label, win_arrow = make_window_callouts(gauge)
        y_pka = gauge.y_of(6.1)
        pka_tick = Line([4.10, y_pka, 0], [4.38, y_pka, 0], color=GOLD, stroke_width=4.0)
        pka_lab = T("pKa 6.1", size=26, color=GOLD).move_to([5.35, y_pka, 0])

        ghost = make_ghost_needle(gauge, ph_val=6.20, label_text="sealed: 6.2")
        ghost.label.move_to([5.42, gauge.y_of(6.20) + 0.32, 0])

        bars = make_blood_bars(hco3_tr, co2_tr, show_nums=True, show_bubbles=True)
        ratio_tag = make_live_ratio(hco3_tr, co2_tr, pos=(0.70, 0.75, 0))
        lungs_grp = make_tube_and_lungs(label=True)
        funnel = make_acid_funnel()

        self.add(glass_grp, gauge, win_label, win_arrow, pka_tick, pka_lab, ghost, bars, ratio_tag, lungs_grp, ph_tr)

        acid_dots = VGroup(*[
            Dot([HCO3_X + dx, 2.10 + dy, 0], radius=0.065, color=ORANGE)
            for dx, dy in [(-0.22, 0.12), (0.02, 0.24), (0.20, 0.05), (-0.10, -0.05), (0.14, 0.20)]
        ])
        out_bubs = VGroup(*[
            Circle(radius=0.06, color=WHITE, stroke_width=2.0, fill_color=WHITE, fill_opacity=0.65).move_to([CO2_X, 1.30, 0])
            for _ in range(5)
        ])
        open_tag = T("open:\nabout 7.17", size=24, color=GOLD).move_to([5.45, gauge.y_of(7.17) - 0.12, 0])
        # First drop HCO3- to 14 and slide needle to 7.17, THEN reveal 'open: about 7.17'
        self.play(
            FadeIn(funnel),
            FadeIn(acid_dots),
            hco3_tr.animate.set_value(14.0),
            *[d.animate.move_to([HCO3_X, BAR_BASE_Y + 1.5, 0]).set_opacity(0.0) for d in acid_dots],
            LaggedStart(*[b.animate.move_to([CO2_X, 3.35, 0]).set_opacity(0.0) for b in out_bubs], lag_ratio=0.16),
            run_time=1.6,
        )
        self.remove(acid_dots, out_bubs)
        self.play(FadeIn(open_tag), FadeOut(funnel), run_time=0.5)

        self.at("bicarbonate falls")
        self.play(bars.num_hco3.animate.scale(1.18), rate_func=there_and_back, run_time=0.8)

        self.at("carbon dioxide stays put")
        self.play(bars.num_co2.animate.scale(1.18), rate_func=there_and_back, run_time=0.8)

        self.at("the ratio stays")
        self.play(ratio_tag.animate.scale(1.18), rate_func=there_and_back, run_time=0.8)

        self.at("never builds up")
        escape_path = Arrow([CO2_X, -0.95, 0], [CO2_X, 3.30, 0], color=GOLD, stroke_width=4.0, buff=0)
        self.play(Create(escape_path), run_time=1.0)
        self.play(FadeOut(escape_path), run_time=0.5)
        self.finish()


class S11Idea(SpokenScene):
    def construct(self):
        x0, x1, y0, y1 = BLOOD_GLASS
        glass_grp, water, outline = make_glass_and_water(x0, x1, y0, y1, meniscus=True)
        hco3_tr = ValueTracker(14.0)
        co2_tr = ValueTracker(1.2)
        ph_tr = ValueTracker(7.17)

        gauge = make_ph_gauge(x=4.10, y0=-2.20, y1=2.60, compact=False, ph_tracker=ph_tr, tremble=False)
        win_label, win_arrow = make_window_callouts(gauge)
        y_pka = gauge.y_of(6.1)
        pka_tick = Line([4.10, y_pka, 0], [4.38, y_pka, 0], color=GOLD, stroke_width=4.0)
        pka_lab = T("pKa 6.1", size=26, color=GOLD).move_to([5.35, y_pka, 0])

        ghost = make_ghost_needle(gauge, ph_val=6.20, label_text="sealed: 6.2")
        ghost.label.move_to([5.49, gauge.y_of(6.20) + 0.32, 0])
        open_tag = T("open:\nabout 7.17", size=24, color=GOLD).move_to([5.49, gauge.y_of(7.17) - 0.12, 0])

        y_62, y_717 = gauge.y_of(6.20), gauge.y_of(7.17)
        bx = 4.45
        rescue_br = VGroup(
            Line([bx - 0.12, y_62 + 0.05, 0], [bx, y_62 + 0.05, 0], color=GOLD, stroke_width=3.5),
            Line([bx, y_62 + 0.05, 0], [bx, y_717 - 0.05, 0], color=GOLD, stroke_width=3.5),
            Line([bx - 0.12, y_717 - 0.05, 0], [bx, y_717 - 0.05, 0], color=GOLD, stroke_width=3.5),
        )
        rescue_lab = T("breathing's\nrescue", size=26, color=GOLD).move_to([5.55, (y_62 + y_717) / 2.0, 0])

        bars = make_blood_bars(hco3_tr, co2_tr, show_nums=True, show_bubbles=True)
        ratio_tag = T("12 : 1", size=32, color=GOLD, weight=BOLD).move_to([0.70, 0.75, 0])
        lungs_grp = make_tube_and_lungs(label=True)

        train_t = {"t": 0.0}

        def mk_train():
            out = VGroup()
            for k in range(4):
                frac = (train_t["t"] * 0.55 + k * 0.25) % 1.0
                yb = 0.0 + frac * 3.1
                op = 0.85 * (1.0 - max(0.0, (frac - 0.75) / 0.25))
                out.add(Circle(radius=0.06, color=WHITE, stroke_width=2.0, fill_color=WHITE, fill_opacity=op).move_to([CO2_X, yb, 0]))
            return out

        bubble_train = always_redraw(mk_train)
        bubble_train.add_updater(lambda m, dt: train_t.__setitem__("t", train_t["t"] + dt))

        self.add(glass_grp, gauge, win_label, win_arrow, pka_tick, pka_lab, ghost, open_tag, bars, ratio_tag, lungs_grp, bubble_train)
        self.play(Create(rescue_br), FadeIn(rescue_lab), run_time=1.0)

        self.at("not sealed")
        open_rim = Line([x0, y1, 0], [x1, y1, 0], color=GOLD, stroke_width=6.0)
        self.play(FadeIn(open_rim), run_time=0.4)
        self.play(FadeOut(open_rim), run_time=0.6)

        self.at("carries the extra")
        self.play(lungs_grp.label.animate.scale(1.14), rate_func=there_and_back, run_time=0.8)
        self.finish()


class S12Better(SpokenScene):
    def construct(self):
        x0, x1, y0, y1 = BLOOD_GLASS
        glass_grp, water, outline = make_glass_and_water(x0, x1, y0, y1, meniscus=True)
        hco3_tr = ValueTracker(14.0)
        co2_tr = ValueTracker(1.2)
        ph_tr = ValueTracker(7.17)

        gauge = make_ph_gauge(x=4.10, y0=-2.20, y1=2.60, compact=False, ph_tracker=ph_tr, tremble=False)
        win_label, win_arrow = make_window_callouts(gauge)
        y_pka = gauge.y_of(6.1)
        pka_tick = Line([4.10, y_pka, 0], [4.38, y_pka, 0], color=GOLD, stroke_width=4.0)
        pka_lab = T("pKa 6.1", size=26, color=GOLD).move_to([5.35, y_pka, 0])
        ghost = make_ghost_needle(gauge, ph_val=6.20, label_text="sealed: 6.2")
        ghost.label.move_to([5.42, gauge.y_of(6.20) + 0.32, 0])

        bars = make_blood_bars(hco3_tr, co2_tr, show_nums=True, show_bubbles=True)
        ratio_tag = make_live_ratio(hco3_tr, co2_tr, pos=(0.70, 0.75, 0))
        lungs_grp = make_tube_and_lungs(label=True)
        stag = scope_tag("schematic")

        self.add(glass_grp, gauge, win_label, win_arrow, pka_tick, pka_lab, ghost, bars, ratio_tag, lungs_grp, stag)

        self.at("hemoglobin and other buffers")
        buf_positions = [(0.15, -0.35), (1.15, -0.15), (0.55, -1.05), (1.55, -0.95)]
        buf_discs = VGroup(*[
            Circle(radius=0.22, color=WHITE, stroke_width=2.5, fill_color=WHITE, fill_opacity=0.14).move_to([px, py, 0])
            for px, py in buf_positions
        ])
        buf_lab = T("other buffers", size=26, color=TEXT).move_to([0.85, -1.65, 0])
        protons = VGroup(*[
            Dot([px + 0.35, py + 0.65, 0], radius=0.06, color=ORANGE)
            for px, py in buf_positions[:3]
        ])
        self.play(FadeIn(buf_discs), FadeIn(buf_lab), FadeIn(protons), run_time=0.6)
        self.play(
            *[p.animate.move_to([px + 0.14, py + 0.14, 0]) for p, (px, py) in zip(protons, buf_positions[:3])],
            ph_tr.animate.set_value(7.24),
            run_time=1.3,
        )

        self.at("the kidneys")
        kidney_shape = RoundedRectangle(
            corner_radius=0.22, width=0.62, height=0.44,
            color=PURPLE, stroke_width=3.0, fill_color=PURPLE, fill_opacity=0.24,
        ).move_to([-5.32, -0.75, 0])
        kidney_lab = T("kidneys", size=24, color=PURPLE).move_to([-5.32, -1.28, 0])
        slices = VGroup(*[
            Rectangle(width=0.38, height=0.12, color=PURPLE, fill_color=PURPLE, fill_opacity=0.85).move_to([-5.32, -0.50, 0])
            for _ in range(3)
        ])

        self.play(FadeIn(kidney_shape), FadeIn(kidney_lab), FadeIn(slices), run_time=0.4)
        self.play(
            LaggedStart(*[s.animate.move_to([HCO3_X, BAR_BASE_Y + 2.0, 0]).set_opacity(0.0) for s in slices], lag_ratio=0.18),
            hco3_tr.animate.set_value(24.0),
            ph_tr.animate.set_value(7.40),
            FadeOut(ghost),
            run_time=1.8,
        )
        self.remove(slices)
        self.finish()


class S13Stakes(SpokenScene):
    def construct(self):
        x0, x1, y0, y1 = BLOOD_GLASS
        glass_grp, water, outline = make_glass_and_water(x0, x1, y0, y1, meniscus=True)
        hco3_tr = ValueTracker(24.0)
        co2_tr = ValueTracker(1.2)
        ph_tr = ValueTracker(7.40)

        gauge = make_ph_gauge(x=4.10, y0=-2.20, y1=2.60, compact=False, ph_tracker=ph_tr, tremble=True)
        win_label, win_arrow = make_window_callouts(gauge)
        y_pka = gauge.y_of(6.1)
        pka_tick = Line([4.10, y_pka, 0], [4.38, y_pka, 0], color=GOLD, stroke_width=4.0)
        pka_lab = T("pKa 6.1", size=26, color=GOLD).move_to([5.35, y_pka, 0])

        bars = make_blood_bars(hco3_tr, co2_tr, show_nums=True, show_bubbles=True)
        ratio_tag = T("20 : 1", size=32, color=GOLD, weight=BOLD).move_to([0.75, 0.95, 0])
        lungs_grp = make_tube_and_lungs(label=True)
        ball = make_folded_ball(center=(0.75, -0.55, 0.0), scale=0.82, seed=11, with_charges=True)
        stag = scope_tag("schematic")

        self.add(glass_grp, gauge, win_label, win_arrow, pka_tick, pka_lab, bars, ratio_tag, lungs_grp, ball, stag)

        self.at("cross much past")
        ghost_tr = ValueTracker(7.40)
        ghost_dyn = always_redraw(lambda: make_ghost_needle(gauge, ph_val=ghost_tr.get_value(), label_text=None))
        self.add(ghost_dyn)
        self.play(ghost_tr.animate.set_value(6.55), run_time=1.3)

        self.at("proteins change their charges")
        p1 = Dot(ball.beads[1].get_center() + UP * 0.8 + RIGHT * 0.4, radius=0.065, color=ORANGE)
        p2 = Dot(ball.beads[8].get_center() + DOWN * 0.8 + LEFT * 0.4, radius=0.065, color=ORANGE)
        slack0 = ArcBetweenPoints(ball.beads[0].get_center(), ball.beads[1].get_center(), angle=-0.7, color=GREY, stroke_width=2.5)
        slack3 = ArcBetweenPoints(ball.beads[7].get_center(), ball.beads[8].get_center(), angle=-0.7, color=GREY, stroke_width=2.5)
        self.play(FadeIn(p1), FadeIn(p2), run_time=0.2)
        self.play(
            p1.animate.move_to(ball.beads[1].get_center() + UP * 0.14),
            p2.animate.move_to(ball.beads[8].get_center() + DOWN * 0.14),
            FadeOut(ball.charges[1]),
            FadeOut(ball.charges[3]),
            Transform(ball.links[0], slack0),
            Transform(ball.links[3], slack3),
            ball.shell.animate.scale(1.08),
            run_time=1.1,
        )

        self.at("heart rhythm")
        ecg_pts = [
            [1.38, 2.55, 0], [1.62, 2.55, 0], [1.72, 2.90, 0], [1.82, 2.25, 0], [1.92, 2.55, 0],
            [2.18, 2.55, 0], [2.28, 2.85, 0], [2.38, 2.30, 0], [2.48, 2.55, 0],
            [2.82, 2.55, 0], [2.89, 2.66, 0], [2.97, 2.48, 0], [3.07, 2.55, 0], [3.25, 2.55, 0],
        ]
        ecg = VMobject(color=GOLD, stroke_width=3.5).set_points_as_corners(ecg_pts)
        self.play(Create(ecg), run_time=1.0)
        self.play(FadeOut(ecg), run_time=0.4)

        self.at("less than one ph unit")
        y_68, y_74 = gauge.y_of(6.80), gauge.y_of(7.40)
        bx = 4.55
        unit_br = VGroup(
            Line([bx - 0.12, y_68, 0], [bx, y_68, 0], color=GOLD, stroke_width=3.5),
            Line([bx, y_68, 0], [bx, y_74 - 0.05, 0], color=GOLD, stroke_width=3.5),
            Line([bx - 0.12, y_74 - 0.05, 0], [bx, y_74 - 0.05, 0], color=GOLD, stroke_width=3.5),
        )
        unit_lab = T("under 1\npH unit", size=26, color=GOLD).move_to([5.45, (y_68 + y_74) / 2.0, 0])
        self.play(Create(unit_br), FadeIn(unit_lab), run_time=0.9)

        taut0 = Line(ball.beads[0].get_center(), ball.beads[1].get_center(), color=GREEN, stroke_width=3.0)
        taut3 = Line(ball.beads[7].get_center(), ball.beads[8].get_center(), color=GREEN, stroke_width=3.0)
        self.play(
            FadeOut(ghost_dyn),
            FadeOut(p1),
            FadeOut(p2),
            FadeIn(ball.charges[1]),
            FadeIn(ball.charges[3]),
            Transform(ball.links[0], taut0),
            Transform(ball.links[3], taut3),
            ball.shell.animate.scale(1.0 / 1.08),
            run_time=1.0,
        )
        self.finish()


class S14Return(SpokenScene):
    def construct(self):
        x0, x1, y0, y1 = BLOOD_GLASS
        glass_grp, water, outline = make_glass_and_water(x0, x1, y0, y1, meniscus=True)
        hco3_tr = ValueTracker(24.0)
        co2_tr = ValueTracker(1.2)
        ph_tr = ValueTracker(7.40)

        gauge = make_ph_gauge(x=4.10, y0=-2.20, y1=2.60, compact=False, ph_tracker=ph_tr, tremble=True)
        win_label, win_arrow = make_window_callouts(gauge)
        y_pka = gauge.y_of(6.1)
        pka_tick = Line([4.10, y_pka, 0], [4.38, y_pka, 0], color=GOLD, stroke_width=4.0)
        pka_lab = T("pKa 6.1", size=26, color=GOLD).move_to([5.35, y_pka, 0])

        bars = make_blood_bars(hco3_tr, co2_tr, show_nums=True, show_bubbles=True)
        ratio_tag = T("20 : 1", size=32, color=GOLD, weight=BOLD).move_to([0.75, 0.95, 0])
        lungs_grp = make_tube_and_lungs(label=True)
        ball = make_folded_ball(center=(0.75, -0.55, 0.0), scale=0.82, seed=11, with_charges=True)

        self.add(glass_grp, gauge, win_label, win_arrow, pka_tick, pka_lab, bars, ratio_tag, lungs_grp, ball)

        self.play(pka_lab.animate.scale(1.12), rate_func=there_and_back, run_time=1.4)

        self.at("each breath")
        bub = Circle(radius=0.075, color=WHITE, stroke_width=2.5, fill_color=WHITE, fill_opacity=0.8).move_to([CO2_X, -1.35, 0])
        self.play(bub.animate.move_to([CO2_X, 3.35, 0]).set_opacity(0.0), run_time=1.8)
        self.remove(bub)

        self.at("steady the charges")
        self.play(
            ball.charges.animate.set_color(GOLD).scale(1.12),
            ball.links.animate.set_stroke(width=6.5),
            rate_func=there_and_back,
            run_time=1.2,
        )
        self.finish()


class S15End(EndCard):
    LINE = "Blood's buffer works far from its pKa because breathing removes CO₂."
