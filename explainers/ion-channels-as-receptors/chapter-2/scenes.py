"""
Gates, Two Locks, and Plugs — Lesson: Ion Channels as Receptors (Chapter 2)

COLOUR MAP (one colour per concept for the entire film):
- BG (#0f1117): dark slate background
- CHAN_COL (#58C4DD / BLUE): channel protein walls, pore, and hinged gate
- MEMB_FILL (#243247) / MEMB_EDGE (#475569): schematic lipid bilayer membrane
- NA_COL (#F59E0B): Na+ ions (E_Na = +60 mV)
- K_COL (#3FB8C0 / TEAL): K+ ions (E_K = -90 mV)
- CA_COL (#A78BFA): Ca2+ ions (E_Ca = +125 mV)
- MG_COL (#84CC16): Mg2+ ions (voltage-dependent pore block)
- LIGAND_COL (#D4A843 / GOLD): chemical ligands & intracellular messengers
- VOLT_COL (#F5D547 / YELLOW): electric field, S4 positive charges (+), voltage cues
- HEAT_COL (#FB923C): physical stimulus (heat waves)
- PLUG_COL (#F43F5E): pore-blocking toxins and drugs (tetrodotoxin, ketamine)
- TEXT (#E8EAF0): primary labels, Vm gauge needle, and live Vm readout

ONE CARRIED WORLD:
Horizontal membrane bilayer (Outside above, Inside below) with channel pore(s)
in the main stage (x = -6.0..3.1) and a live computed Membrane Voltage (Vm) gauge
on the right (x = 4.65, -90 mV to +60 mV, rest -70 mV).

SCENE-BY-SCENE PLAN (what changes on screen and what it is computed from):
- s00_hook: Open channel conducts Na+ down its electrochemical gradient (Vm - E_Na),
  integrating Vm upward via RC membrane ODE; gate then closes, and Mg2+ lock + outer
  plug appear to block the pore.
- s01_title: Standard TitleCard ("Ion Channels as Receptors" / "Gates, Two Locks, and Plugs").
- s02_key_ligand: Highlights gated receptor and 3 keys; outer ligand docks into outer
  pocket, rotating gate angle (0->1) to drive computed Na+ influx and Vm rise; then inner
  messenger docks at inner pocket to open gate from below.
- s03_key_voltage: Depolarizing Vm shifts electric-field vectors and pushes 4 S4 (+) helices
  outward via Boltzmann gating curve, pulling the gate open so Na+ enters and drives Vm up.
- s04_feedback_and_physical: Na+ influx through Channel 1 raises Vm across threshold (-40 mV),
  snapping Channel 2 open in positive feedback; then single sensory channel receives computed
  sinusoidal heat waves that swing its gate open and drive cation influx.
- s05_nmda_setup: Resting membrane (-70 mV) with AMPA (left) and NMDA (right); reveals
  synaptic receptors, then glutamate and glycine/D-serine dock on NMDA, opening its gate
  while extracellular Mg2+ hovers at the pore mouth.
- s06_predict_q: Holds open-gated NMDA at -70 mV with negative inner charges and hovering Mg2+,
  revealing the predict question card in the bottom band.
- s07_predict_pause: PredictPause holds the exact S06 world and question with 4.5 s countdown.
- s08_predict_reveal: Negative inside pulls Mg2+ into the open NMDA pore (bouncing Na+/Ca2+);
  AMPA opens so Na+ influx depolarizes Vm above -35 mV, expelling Mg2+ so Na+ and Ca2+ pour in.
- s09_pore_blockers: Side-by-side Na+ channel (tetrodotoxin lodges in outer mouth, bouncing Na+
  and holding Vm at -70 mV) and NMDA receptor (opens briefly then ketamine enters deep inside
  the open pore, blocking Na+/Ca2+ flow and reducing channel open frequency).
- s10_closing: Single carried channel demonstrates sharp switching by the 3 gate keys (ligand,
  voltage, heat) and 2 pore blocks (Mg2+, toxin/drug), then opens clear for ion flow.
- s11_end: Standard EndCard with exact take-home line.
"""
from bp_parts import *

# ---- Concept Palette ----
CHAN_COL = BLUE        # "#58C4DD"
MEMB_FILL = "#243247"
MEMB_EDGE = "#475569"
NA_COL = "#F59E0B"     # Amber Na+
K_COL = TEAL           # "#3FB8C0" Teal K+
CA_COL = "#A78BFA"     # Violet Ca2+
MG_COL = "#84CC16"     # Lime-green Mg2+
LIGAND_COL = GOLD      # "#D4A843"
VOLT_COL = YELLOW      # "#F5D547"
HEAT_COL = "#FB923C"   # Warm orange heat waves
PLUG_COL = "#F43F5E"   # Coral-red TTX / ketamine

# ---- Physiological Model Constants (from lesson_for_context.mdx) ----
V_REST = -70.0
E_K = -90.0
E_NA = 60.0
E_CA = 125.0
V_THRESH = -40.0


def integrate_vm(vm, g_na=0.0, g_ca=0.0, g_k=0.0, dt=1 / 60, tau=0.35):
    """Single Euler step of passive membrane RC model toward weighted equilibrium potential."""
    g_leak = 1.0
    target = (
        g_leak * V_REST + g_na * E_NA + g_ca * E_CA + g_k * E_K
    ) / (g_leak + g_na + g_ca + g_k)
    return vm + (target - vm) * min(1.0, dt / tau)


def s4_boltzmann(vm, v_half=-42.0, k=7.0):
    """Fraction of S4 voltage sensors shifted outward as a function of membrane voltage."""
    return float(1.0 / (1.0 + np.exp(-(vm - v_half) / k)))


def plus_mark(center, size=0.14, color=VOLT_COL, stroke=3.0):
    """Crisp vector '+' mark (no small Text glyph)."""
    c = np.array(center, dtype=float)
    h = size / 2
    return VGroup(
        Line(c + LEFT * h, c + RIGHT * h, color=color, stroke_width=stroke),
        Line(c + DOWN * h, c + UP * h, color=color, stroke_width=stroke),
    )


def minus_mark(center, size=0.16, color=VOLT_COL, stroke=3.2):
    """Crisp vector '-' mark."""
    c = np.array(center, dtype=float)
    h = size / 2
    return Line(c + LEFT * h, c + RIGHT * h, color=color, stroke_width=stroke)


def build_bilayer(pore_xs=(-1.2,), pore_half_w=0.54, x_min=-6.15, x_max=3.15, y_mid=0.0, half_h=0.48):
    """Horizontal lipid bilayer with clean openings at each channel pore x."""
    xs = sorted(pore_xs)
    spans = []
    cur = x_min
    for px in xs:
        left_end = px - pore_half_w
        if left_end > cur + 0.05:
            spans.append((cur, left_end))
        cur = px + pore_half_w
    if x_max > cur + 0.05:
        spans.append((cur, x_max))

    segs = VGroup()
    for a, b in spans:
        w = b - a
        cx = (a + b) / 2
        upper = Rectangle(
            width=w, height=half_h,
            fill_color=MEMB_FILL, fill_opacity=0.95,
            stroke_color=MEMB_EDGE, stroke_width=2.2,
        ).move_to([cx, y_mid + half_h / 2, 0])
        lower = Rectangle(
            width=w, height=half_h,
            fill_color=MEMB_FILL, fill_opacity=0.95,
            stroke_color=MEMB_EDGE, stroke_width=2.2,
        ).move_to([cx, y_mid - half_h / 2, 0])
        segs.add(upper, lower)

    out_lbl = T("Outside", size=26, color=TEXT).move_to([-5.35, 2.65, 0])
    in_lbl = T("Inside", size=26, color=TEXT).move_to([-5.35, -2.50, 0])
    return VGroup(segs, out_lbl, in_lbl)


class VmGauge(VGroup):
    """Vertical membrane voltage gauge (-90 to +60 mV) driven by a single ValueTracker."""

    def __init__(self, tracker, x=4.65, y_bot=-1.95, y_top=1.95):
        super().__init__()
        self.tracker = tracker
        self.x = x
        self.y_bot = y_bot
        self.y_top = y_top

        bar = RoundedRectangle(
            corner_radius=0.08, width=0.30, height=y_top - y_bot,
            stroke_color=GREY, stroke_width=2.5, fill_color=MEMB_FILL, fill_opacity=0.85,
        ).move_to([x, (y_bot + y_top) / 2, 0])

        ticks = VGroup()
        tick_specs = [
            (60, "+60", NA_COL),
            (0, "0", TEXT),
            (-70, "-70", TEXT),
            (-90, "-90", K_COL),
        ]
        for v, lab_txt, col in tick_specs:
            yy = self.y_for(v)
            tk = Line([x + 0.15, yy, 0], [x + 0.29, yy, 0], color=col, stroke_width=2.5)
            lb = M(lab_txt, size=22, color=col).move_to([x + 0.37, yy, 0], aligned_edge=LEFT)
            ticks.add(tk, lb)

        unit_lbl = T("mV", size=22, color=TEXT).move_to([x + 0.42, y_top + 0.32, 0], aligned_edge=LEFT)
        readout = always_redraw(
            lambda: M(f"Vm = {tracker.get_value():+3.0f} mV", size=26, color=TEXT).move_to([x + 0.15, y_top + 0.80, 0])
        )

        def mk_needle():
            yy = self.y_for(np.clip(tracker.get_value(), -90, 60))
            tri = Polygon(
                [x - 0.17, yy, 0],
                [x - 0.41, yy + 0.13, 0],
                [x - 0.41, yy - 0.13, 0],
                color=TEXT, fill_color=TEXT, fill_opacity=1.0, stroke_width=1.5,
            )
            cross = Line([x - 0.15, yy, 0], [x + 0.15, yy, 0], color=TEXT, stroke_width=3.5)
            return VGroup(tri, cross)

        needle = always_redraw(mk_needle)
        self.add(bar, ticks, unit_lbl, readout, needle)

    def y_for(self, vm):
        frac = (vm - (-90.0)) / (60.0 - (-90.0))
        return self.y_bot + frac * (self.y_top - self.y_bot)


class ChannelBody(VGroup):
    """Carried schematic ion channel cross-section with animated hinged gate and optional modules."""

    def __init__(
        self,
        cx=-1.2,
        y_mid=0.0,
        wall_w=0.50,
        wall_h=2.45,
        pore_w=0.70,
        color=CHAN_COL,
        gate_tracker=None,
        s4_tracker=None,
        outer_pockets=0,
        inner_pocket=False,
        tall=False,
    ):
        super().__init__()
        self.cx = cx
        self.y_mid = y_mid
        self.pore_w = pore_w
        self.color = color
        self.gate_t = gate_tracker if gate_tracker is not None else ValueTracker(0.0)
        self.s4_t = s4_tracker

        h = wall_h * (1.24 if tall else 1.0)
        dx = pore_w / 2 + wall_w / 2

        left_wall = RoundedRectangle(
            corner_radius=0.14, width=wall_w, height=h,
            stroke_color=color, stroke_width=3.2, fill_color=color, fill_opacity=0.28,
        ).move_to([cx - dx, y_mid, 0])
        right_wall = RoundedRectangle(
            corner_radius=0.14, width=wall_w, height=h,
            stroke_color=color, stroke_width=3.2, fill_color=color, fill_opacity=0.28,
        ).move_to([cx + dx, y_mid, 0])

        self.left_wall = left_wall
        self.right_wall = right_wall
        self.add(left_wall, right_wall)

        # Hinged inner gate leaves (pivot at inner pore walls)
        gate_y = y_mid - h * 0.22
        leaf_len = pore_w / 2 + 0.03

        def mk_gate():
            op = float(np.clip(self.gate_t.get_value(), 0.0, 1.0))
            ang = op * (PI * 0.44)
            lp = np.array([cx - pore_w / 2, gate_y, 0.0])
            rp = np.array([cx + pore_w / 2, gate_y, 0.0])
            l_tip = lp + leaf_len * np.array([np.cos(-ang), np.sin(-ang), 0.0])
            r_tip = rp + leaf_len * np.array([-np.cos(-ang), np.sin(-ang), 0.0])
            g_col = TEAL if op > 0.55 else color
            return VGroup(
                Line(lp, l_tip, color=g_col, stroke_width=8.0),
                Line(rp, r_tip, color=g_col, stroke_width=8.0),
                Dot(lp, radius=0.06, color=TEXT),
                Dot(rp, radius=0.06, color=TEXT),
            )

        self.gate = always_redraw(mk_gate)
        self.add(self.gate)

        # Outer binding pockets (1 on left or 2 symmetric)
        self.outer_pocket_pts = []
        if outer_pockets >= 1:
            p1 = self._make_pocket(cx - dx - wall_w / 2 - 0.16, y_mid + h * 0.30, side=-1)
            self.add(p1)
            self.outer_pocket_pts.append(p1.get_center())
        if outer_pockets >= 2:
            p2 = self._make_pocket(cx + dx + wall_w / 2 + 0.16, y_mid + h * 0.30, side=1)
            self.add(p2)
            self.outer_pocket_pts.append(p2.get_center())

        self.inner_pocket_pt = None
        if inner_pocket:
            pi = self._make_pocket(cx - dx - wall_w / 2 - 0.16, y_mid - h * 0.30, side=-1)
            self.add(pi)
            self.inner_pocket_pt = pi.get_center()

        # Four S4 voltage sensors (2 left, 2 right)
        if self.s4_t is not None:
            offsets = [
                -dx - wall_w / 2 - 0.56, -dx - wall_w / 2 - 0.24,
                dx + wall_w / 2 + 0.24, dx + wall_w / 2 + 0.56,
            ]

            def mk_s4():
                shift = float(np.clip(self.s4_t.get_value(), 0.0, 1.0)) * 0.56
                grp = VGroup()
                for ox in offsets:
                    cy = y_mid - 0.26 + shift
                    bar = RoundedRectangle(
                        corner_radius=0.08, width=0.22, height=1.32,
                        stroke_color=VOLT_COL, stroke_width=2.5,
                        fill_color=VOLT_COL, fill_opacity=0.22,
                    ).move_to([cx + ox, cy, 0])
                    grp.add(bar)
                    for dy in (-0.36, 0.0, 0.36):
                        grp.add(plus_mark([cx + ox, cy + dy, 0], size=0.11, color=VOLT_COL, stroke=2.6))
                return grp

            self.s4 = always_redraw(mk_s4)
            self.add(self.s4)

    def _make_pocket(self, x, y, side=-1):
        """U-shaped cup pocket facing outward."""
        dx = 0.16 * side
        pts = [
            [x - dx, y + 0.20, 0],
            [x + dx, y + 0.20, 0],
            [x + dx, y - 0.20, 0],
            [x - dx, y - 0.20, 0],
        ]
        cup = VMobject(stroke_color=LIGAND_COL, stroke_width=3.5)
        cup.set_points_as_corners(pts)
        return cup


def make_ion_stream(
    cx=-1.2,
    n=18,
    color=NA_COL,
    seed=7,
    radius=0.105,
    y_top=2.05,
    y_bot=-1.65,
    spread_x=0.68,
    pore_x=0.18,
    wall_top=1.34,
    gate_fn=lambda: True,
    block_y_fn=lambda: None,
    speed_fn=lambda: 1.5,
    upward=False,
):
    """Deterministic ion ensemble that flows through open pores and bounces off closed/blocked barriers."""
    rng = np.random.default_rng(seed)
    dots = VGroup()
    state = []
    blk0 = block_y_fn()
    open0 = gate_fn()
    for _ in range(n):
        d = Dot(radius=radius, color=color, fill_opacity=0.96)
        if upward:
            y0 = rng.uniform(y_bot, -0.55)
            x0 = cx + rng.uniform(-pore_x if -wall_top < y0 < wall_top else -spread_x, pore_x if -wall_top < y0 < wall_top else spread_x)
        else:
            min_y0 = max(0.65, (blk0 + 0.05) if blk0 is not None else 0.65)
            if not open0 and blk0 is None:
                min_y0 = max(min_y0, 0.25)
            y0 = rng.uniform(min(min_y0, y_top - 0.05), y_top)
            lim_x = pore_x if -wall_top < y0 < wall_top else spread_x
            x0 = cx + rng.uniform(-lim_x, lim_x)
        d.move_to([x0, y0, 0])
        dots.add(d)
        state.append({
            "x": x0,
            "y": y0,
            "vx": rng.uniform(-0.35, 0.35),
            "vy": rng.uniform(0.85, 1.40),
        })

    def update(mob, dt):
        dt = min(dt, 0.05)
        is_open = gate_fn()
        blk_y = block_y_fn()
        spd = max(0.0, speed_fn())
        for d, st in zip(mob, state):
            x, y = st["x"], st["y"]
            if not upward:
                if is_open and blk_y is None:
                    # Force downward motion so previously bounced ions never fly upward
                    st["vy"] = abs(st["vy"])
                    target_x = cx + np.clip(x - cx, -pore_x, pore_x) * 0.72
                    x += (target_x - x) * min(1.0, 6.5 * dt)
                    next_y = y - st["vy"] * spd * dt
                    if next_y < wall_top and y >= -wall_top and abs(x - cx) > pore_x:
                        x += (target_x - x) * min(1.0, 10.0 * dt)
                        y = wall_top + 0.01 if abs(x - cx) > pore_x else next_y
                    else:
                        y = next_y
                    if y < y_bot:
                        y = y_top - rng.uniform(0.0, 0.20)
                        x = cx + rng.uniform(-spread_x, spread_x)
                else:
                    barrier = blk_y if blk_y is not None else 0.20
                    if y < -0.65:
                        # Already inside the cell below the gate: finish falling and wrap to top
                        y -= abs(st["vy"]) * spd * dt
                        if y < y_bot:
                            y = y_top - rng.uniform(0.0, 0.20)
                            x = cx + rng.uniform(-spread_x, spread_x)
                    elif blk_y is not None and y < blk_y:
                        # Barrier rose above an ion still inside the pore: push it above the barrier
                        y = blk_y + 0.04
                        st["vy"] = -abs(st["vy"])
                    else:
                        max_dx = pore_x if y < wall_top else spread_x
                        x += st["vx"] * dt
                        if abs(x - cx) > max_dx:
                            st["vx"] *= -1
                            x = cx + np.clip(x - cx, -max_dx, max_dx)
                        next_y = y - st["vy"] * 0.95 * dt
                        if next_y < wall_top and y >= wall_top and abs(x - cx) > pore_x:
                            # Bounce off the top of the channel walls
                            y = wall_top + 0.02
                            st["vy"] = -abs(st["vy"])
                        else:
                            y = next_y
                            if y <= barrier:
                                y = barrier + 0.04
                                st["vy"] = -abs(st["vy"])
                            elif y >= y_top:
                                y = y_top - 0.04
                                st["vy"] = abs(st["vy"])
                if -wall_top < y < wall_top:
                    x = cx + float(np.clip(x - cx, -pore_x, pore_x))
                y = float(np.clip(y, y_bot, y_top))
            else:
                if is_open and blk_y is None:
                    st["vy"] = abs(st["vy"])
                    target_x = cx + np.clip(x - cx, -pore_x, pore_x) * 0.72
                    x += (target_x - x) * min(1.0, 6.5 * dt)
                    y += st["vy"] * spd * dt
                    if y > y_top:
                        y = y_bot + rng.uniform(0.0, 0.20)
                        x = cx + rng.uniform(-spread_x, spread_x)
                else:
                    barrier = blk_y if blk_y is not None else -0.45
                    max_dx = pore_x if y > -wall_top else spread_x
                    x += st["vx"] * dt
                    if abs(x - cx) > max_dx:
                        st["vx"] *= -1
                        x = cx + np.clip(x - cx, -max_dx, max_dx)
                    y += st["vy"] * 0.85 * dt
                    if y >= barrier:
                        y = barrier - 0.04
                        st["vy"] = -abs(st["vy"])
                    elif y <= y_bot:
                        y = y_bot + 0.04
                        st["vy"] = abs(st["vy"])
                if -wall_top < y < wall_top:
                    x = cx + float(np.clip(x - cx, -pore_x, pore_x))
                y = float(np.clip(y, y_bot, y_top))
            st["x"], st["y"] = x, y
            d.move_to([x, y, 0])

    dots.add_updater(update)
    return dots


def ion_legend(items, top_left=(-6.05, 2.05)):
    """Compact vertical legend of ion dot + name at safe size 24, well above bilayer."""
    rows = VGroup()
    for label, col in items:
        dot = Dot(radius=0.105, color=col)
        txt = T(label, size=24, color=col)
        row = VGroup(dot, txt).arrange(RIGHT, buff=0.16)
        rows.add(row)
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    rows.move_to([top_left[0], top_left[1], 0.0], aligned_edge=UL)
    return rows


def heading(text, color=TEXT):
    """Top-band heading clear of the frame edge and Vm gauge."""
    return T(text, size=32, color=color, weight=BOLD).move_to([-1.2, HEAD_Y, 0])


# ==============================================================================
# SCENES
# ==============================================================================

class S00Hook(SpokenScene):
    def construct(self):
        vm = ValueTracker(V_REST)
        gate = ValueTracker(1.0)
        blocked = {"state": None}

        bilayer = build_bilayer(pore_xs=(-1.2,))
        ch = ChannelBody(cx=-1.2, gate_tracker=gate)
        gauge = VmGauge(vm)
        leg = ion_legend([("Na+", NA_COL), ("K+", K_COL), ("Mg2+", MG_COL)], top_left=(-6.05, 2.05))

        na_ions = make_ion_stream(
            cx=-1.2, n=18, color=NA_COL, seed=11,
            gate_fn=lambda: gate.get_value() > 0.5,
            block_y_fn=lambda: 1.15 if blocked["state"] == "plug" else (0.20 if blocked["state"] == "lock" else None),
            speed_fn=lambda: max(0.45, (E_NA - vm.get_value()) / 70.0) if gate.get_value() > 0.5 else 0.9,
        )
        k_dots = VGroup(*[
            Dot(radius=0.095, color=K_COL).move_to([p[0], p[1], 0])
            for p in np.column_stack([
                np.random.default_rng(3).uniform(-3.6, -2.1, 6),
                np.random.default_rng(4).uniform(-1.95, -0.80, 6),
            ])
        ])

        self.add(bilayer, ch, gauge, leg, na_ions, k_dots)

        self.at("open channel")
        vm_active = {"on": True}

        def drive_vm(mob, dt):
            if vm_active["on"] and gate.get_value() > 0.5 and blocked["state"] is None:
                vm.set_value(integrate_vm(vm.get_value(), g_na=2.4, dt=dt, tau=0.85))
            else:
                vm.set_value(integrate_vm(vm.get_value(), g_na=0.0, dt=dt, tau=0.55))

        driver = Mobject()
        driver.add_updater(drive_vm)
        self.add(driver)

        self.at("opens that gate")
        vm_active["on"] = False
        q_mark = T("?", size=42, color=LIGAND_COL, weight=BOLD).move_to([-2.75, 1.05, 0])
        self.play(gate.animate.set_value(0.0), FadeIn(q_mark, shift=DOWN * 0.1), run_time=0.55)

        self.at("second lock")
        self.play(gate.animate.set_value(1.0), FadeOut(q_mark), run_time=0.35)
        blocked["state"] = "lock"
        mg_lock = Circle(
            radius=0.20, color=MG_COL, fill_color=MG_COL, fill_opacity=0.92, stroke_width=2.5,
        ).move_to([-1.2, 1.35, 0])
        lock_lbl = T("second lock", size=24, color=MG_COL).move_to([0.95, 1.15, 0])
        self.play(mg_lock.animate.move_to([-1.2, 0.0, 0]), FadeIn(lock_lbl), run_time=0.45)

        self.at("plug")
        plug = RoundedRectangle(
            corner_radius=0.14, width=0.62, height=0.44,
            color=PLUG_COL, fill_color=PLUG_COL, fill_opacity=0.92, stroke_width=2.5,
        ).move_to([-1.2, 1.65, 0])
        plug_lbl = T("plug", size=24, color=PLUG_COL).move_to([0.95, 1.70, 0])
        blocked["state"] = "plug"
        self.play(
            plug.animate.move_to([-1.2, 1.02, 0]),
            FadeIn(plug_lbl),
            run_time=0.55,
        )
        self.finish()


class S01Title(TitleCard):
    LESSON = "Ion Channels as Receptors"
    TITLE = "Gates, Two Locks, and Plugs"


class S02KeyLigand(SpokenScene):
    def construct(self):
        vm = ValueTracker(V_REST)
        gate = ValueTracker(0.0)

        bilayer = build_bilayer(pore_xs=(-1.2,))
        ch = ChannelBody(cx=-1.2, gate_tracker=gate, outer_pockets=1, inner_pocket=True)
        gauge = VmGauge(vm)
        leg = ion_legend([("Na+", NA_COL)], top_left=(-6.05, 2.05))
        na_ions = make_ion_stream(
            cx=-1.2, n=18, color=NA_COL, seed=21,
            gate_fn=lambda: gate.get_value() > 0.5,
            speed_fn=lambda: max(0.45, (E_NA - vm.get_value()) / 75.0),
        )

        def drive_vm(mob, dt):
            g_na = 1.8 * gate.get_value()
            vm.set_value(integrate_vm(vm.get_value(), g_na=g_na, dt=dt, tau=0.8))

        driver = Mobject()
        driver.add_updater(drive_vm)
        self.add(bilayer, ch, gauge, leg, na_ions, driver)

        self.at("opening the gate")
        gate_lbl = T("gate", size=26, color=CHAN_COL).move_to([0.65, -0.82, 0])
        self.play(FadeIn(gate_lbl), run_time=0.45)

        self.at("makes a channel a receptor")
        rec_head = heading("Gated channel = receptor", color=CHAN_COL)
        self.play(FadeIn(rec_head), run_time=0.5)

        self.at("three main keys")
        keys_head = heading("Gates answer three keys", color=TEXT)
        self.play(swap(rec_head, keys_head), run_time=0.55)

        self.at("first key")
        head = heading("Key 1: Chemical ligand", color=LIGAND_COL)
        self.play(swap(keys_head, head), run_time=0.55)

        self.at("neurotransmitter docks")
        outer_lig = RoundedRectangle(
            corner_radius=0.12, width=0.44, height=0.32,
            color=LIGAND_COL, fill_color=LIGAND_COL, fill_opacity=0.92,
        ).move_to([-2.65, 1.65, 0])
        lig_lbl = T("neurotransmitter", size=24, color=LIGAND_COL).move_to([-3.10, 1.05, 0], aligned_edge=RIGHT)
        self.add(outer_lig)
        self.play(
            outer_lig.animate.move_to(ch.outer_pocket_pts[0]),
            FadeIn(lig_lbl),
            run_time=0.85,
        )

        self.at("twisting the gate open")
        self.play(gate.animate.set_value(1.0), run_time=0.7)

        self.at("messengers inside")
        self.play(
            gate.animate.set_value(0.0),
            FadeOut(outer_lig),
            FadeOut(lig_lbl),
            FadeOut(gate_lbl),
            run_time=0.5,
        )
        inner_msg = RoundedRectangle(
            corner_radius=0.12, width=0.44, height=0.32,
            color=LIGAND_COL, fill_color=LIGAND_COL, fill_opacity=0.92,
        ).move_to([-2.65, -1.75, 0])
        msg_lbl = T("inner messenger", size=24, color=LIGAND_COL).move_to([-3.10, -1.20, 0], aligned_edge=RIGHT)
        self.play(
            inner_msg.animate.move_to(ch.inner_pocket_pt),
            FadeIn(msg_lbl),
            run_time=0.8,
        )
        self.play(gate.animate.set_value(1.0), run_time=0.65)
        self.finish()


class S03KeyVoltage(SpokenScene):
    def construct(self):
        vm = ValueTracker(V_REST)
        s4_t = ValueTracker(0.0)
        gate = ValueTracker(0.0)

        bilayer = build_bilayer(pore_xs=(-1.2,), pore_half_w=0.95)
        ch = ChannelBody(cx=-1.2, gate_tracker=gate, s4_tracker=s4_t)
        gauge = VmGauge(vm)
        leg = ion_legend([("Na+", NA_COL)], top_left=(-6.05, 2.05))
        head = heading("Key 2: Membrane voltage", color=VOLT_COL)

        na_ions = make_ion_stream(
            cx=-1.2, n=18, color=NA_COL, seed=31, spread_x=0.52,
            gate_fn=lambda: gate.get_value() > 0.5,
            speed_fn=lambda: max(0.45, (E_NA - vm.get_value()) / 75.0),
        )

        self.add(bilayer, ch, gauge, leg, na_ions)

        self.at("second key")
        self.play(FadeIn(head), run_time=0.5)

        self.at("sodium")
        fam_lbl = T("Na+, K+, Ca2+ channels", size=24, color=CHAN_COL).move_to([0.65, 2.15, 0], aligned_edge=LEFT)
        self.play(FadeIn(fam_lbl), run_time=0.5)

        self.at("four voltage sensors")
        s4_lbl = T("4 voltage sensors (S4)", size=24, color=VOLT_COL).move_to([0.65, 1.55, 0], aligned_edge=LEFT)
        self.play(FadeOut(fam_lbl), FadeIn(s4_lbl), run_time=0.55)

        self.at("positive charges")
        pos_lbl = T("+ charges", size=24, color=VOLT_COL).move_to([0.65, 1.05, 0], aligned_edge=LEFT)
        self.play(FadeIn(pos_lbl), run_time=0.5)

        self.at("electric field")
        field_arrows = VGroup(
            Arrow([-3.2, 0.58, 0], [-3.2, -0.58, 0], color=VOLT_COL, stroke_width=4, buff=0.04),
            Arrow([0.8, 0.58, 0], [0.8, -0.58, 0], color=VOLT_COL, stroke_width=4, buff=0.04),
        )
        field_lbl = T("electric field", size=24, color=VOLT_COL).move_to([-4.65, 0.90, 0])
        self.play(FadeIn(field_arrows), FadeIn(field_lbl), run_time=0.6)

        self.at("Depolarize the cell")
        out_arrows = VGroup(
            Arrow([-3.2, -0.58, 0], [-3.2, 0.58, 0], color=VOLT_COL, stroke_width=4.5, buff=0.04),
            Arrow([0.8, -0.58, 0], [0.8, 0.58, 0], color=VOLT_COL, stroke_width=4.5, buff=0.04),
        )
        self.play(
            vm.animate.set_value(15.0),
            ReplacementTransform(field_arrows, out_arrows),
            run_time=0.95,
        )

        self.at("pushes S4 outward")
        self.play(s4_t.animate.set_value(1.0), run_time=0.8)

        self.at("pulling the gate open")
        self.play(gate.animate.set_value(1.0), run_time=0.55)

        def drive_vm(mob, dt):
            if gate.get_value() > 0.5:
                vm.set_value(integrate_vm(vm.get_value(), g_na=2.2, dt=dt, tau=0.9))

        driver = Mobject()
        driver.add_updater(drive_vm)
        self.add(driver)
        self.finish()


class S04FeedbackAndPhysical(SpokenScene):
    def construct(self):
        vm = ValueTracker(V_REST)
        g1 = ValueTracker(0.0)
        g2 = ValueTracker(0.0)
        s4_1 = ValueTracker(0.0)
        s4_2 = ValueTracker(0.0)

        bilayer = build_bilayer(pore_xs=(-3.0, 0.4), pore_half_w=0.95)
        ch1 = ChannelBody(cx=-3.0, gate_tracker=g1, s4_tracker=s4_1)
        ch2 = ChannelBody(cx=0.4, gate_tracker=g2, s4_tracker=s4_2)
        gauge = VmGauge(vm)
        head = heading("Positive feedback", color=NA_COL)
        leg = ion_legend([("Na+", NA_COL)], top_left=(-6.05, 2.05))

        na1 = make_ion_stream(
            cx=-3.0, n=14, color=NA_COL, seed=41, spread_x=0.56,
            gate_fn=lambda: g1.get_value() > 0.5,
            speed_fn=lambda: max(0.45, (E_NA - vm.get_value()) / 70.0),
        )
        na2 = make_ion_stream(
            cx=0.4, n=14, color=NA_COL, seed=42, spread_x=0.56,
            gate_fn=lambda: g2.get_value() > 0.5,
            speed_fn=lambda: max(0.45, (E_NA - vm.get_value()) / 70.0),
        )

        self.add(bilayer, ch1, ch2, gauge, head, leg, na1, na2)

        fb_active = {"on": False}

        def drive_fb(mob, dt):
            if not fb_active["on"]:
                return
            g_tot = 1.0 * g1.get_value() + 2.2 * g2.get_value()
            vm.set_value(integrate_vm(vm.get_value(), g_na=g_tot, dt=dt, tau=0.85))
            if vm.get_value() > V_THRESH and g2.get_value() < 0.99:
                s4_2.set_value(min(1.0, s4_2.get_value() + 2.5 * dt))
                g2.set_value(min(1.0, g2.get_value() + 2.5 * dt))

        driver = Mobject()
        driver.add_updater(drive_fb)
        self.add(driver)

        self.at("feedback")
        ch1_lbl = T("Na+ channel 1", size=22, color=CHAN_COL).move_to([-3.0, -2.05, 0])
        self.play(
            FadeIn(ch1_lbl),
            vm.animate.set_value(-55.0),
            s4_1.animate.set_value(0.75),
            g1.animate.set_value(1.0),
            run_time=0.65,
        )

        self.at("Entering sodium")
        fb_active["on"] = True

        self.at("nerve impulse")
        impulse_lbl = T("nerve impulse", size=26, color=NA_COL).move_to([-1.3, -2.05, 0])
        self.play(swap(ch1_lbl, impulse_lbl), run_time=0.45)

        self.at("third key")
        fb_active["on"] = False
        new_head = heading("Key 3: Physical stimulus", color=HEAT_COL)

        single_bilayer = build_bilayer(pore_xs=(-1.2,))
        g3 = ValueTracker(0.0)
        ch_sens = ChannelBody(cx=-1.2, gate_tracker=g3)
        sens_ions = make_ion_stream(
            cx=-1.2, n=16, color=NA_COL, seed=43,
            gate_fn=lambda: g3.get_value() > 0.5,
            speed_fn=lambda: max(0.45, (E_NA - vm.get_value()) / 75.0),
        )

        self.remove(bilayer)
        self.add(single_bilayer)
        self.play(
            FadeOut(ch1), FadeOut(ch2), FadeOut(na1), FadeOut(na2),
            FadeOut(impulse_lbl),
            FadeIn(ch_sens),
            vm.animate.set_value(V_REST),
            swap(head, new_head),
            run_time=0.85,
        )
        self.add(sens_ions)

        self.at("such as heat")
        phase = ValueTracker(0.0)
        heat_waves = always_redraw(
            lambda: VGroup(*[
                FunctionGraph(
                    lambda t, p=phase.get_value(): 0.14 * np.sin(5.0 * t + p),
                    x_range=[-0.8, 0.8],
                    color=HEAT_COL,
                    stroke_width=4.0,
                ).rotate(-PI / 2).move_to([ox, 1.45, 0])
                for ox in (-2.4, -0.05)
            ])
        )
        heat_lbl = T("heat", size=26, color=HEAT_COL).move_to([-3.25, 1.45, 0])
        phase_driver = Mobject()
        phase_driver.add_updater(lambda m, dt: phase.increment_value(4.5 * dt))
        self.add(heat_waves, phase_driver)
        self.play(FadeIn(heat_lbl), run_time=0.55)

        self.at("open a sensory")
        self.play(
            g3.animate.set_value(1.0),
            vm.animate.set_value(-20.0),
            run_time=1.0,
        )
        self.finish()


def build_nmda_world(gate_val=0.0, ampa_val=0.0, vm_val=V_REST, ligands_bound=False, show_names=True):
    """Shared world builder for S05, S06, S07 (PredictPause) and S08."""
    vm = ValueTracker(vm_val)
    g_ampa = ValueTracker(ampa_val)
    g_nmda = ValueTracker(gate_val)

    bilayer = build_bilayer(pore_xs=(-3.0, 0.4), pore_half_w=0.54)
    ampa = ChannelBody(cx=-3.0, wall_h=2.0, gate_tracker=g_ampa, outer_pockets=1)
    nmda = ChannelBody(cx=0.4, wall_h=2.1, gate_tracker=g_nmda, outer_pockets=2, tall=True)
    gauge = VmGauge(vm)
    leg = ion_legend([("Na+", NA_COL), ("Ca2+", CA_COL), ("Mg2+", MG_COL)], top_left=(-6.05, 2.05))

    ampa_lbl = T("AMPA receptor", size=24, color=CHAN_COL).move_to([-3.0, -2.15, 0])
    nmda_lbl = T("NMDA receptor", size=24, color=CHAN_COL).move_to([0.4, -2.15, 0])

    world = VGroup(bilayer, ampa, nmda, gauge, leg)
    if show_names:
        world.add(ampa_lbl, nmda_lbl)
    bound_mobs = VGroup()
    if ligands_bound:
        g_chip = RoundedRectangle(
            corner_radius=0.10, width=0.38, height=0.28,
            color=LIGAND_COL, fill_color=LIGAND_COL, fill_opacity=0.92,
        ).move_to(nmda.outer_pocket_pts[0])
        gly_chip = RoundedRectangle(
            corner_radius=0.10, width=0.38, height=0.28,
            color=LIGAND_COL, fill_color=LIGAND_COL, fill_opacity=0.92,
        ).move_to(nmda.outer_pocket_pts[1])
        gl_lbl = T("glutamate", size=22, color=LIGAND_COL).move_to([-0.98, 1.72, 0], aligned_edge=RIGHT)
        gy_lbl = T("glycine / D-serine", size=22, color=LIGAND_COL).move_to([1.55, 2.08, 0], aligned_edge=LEFT)
        bound_mobs.add(g_chip, gly_chip, gl_lbl, gy_lbl)
        world.add(bound_mobs)

    return world, vm, g_ampa, g_nmda, ampa, nmda, ampa_lbl, nmda_lbl, bound_mobs


class S05NmdaSetup(SpokenScene):
    def construct(self):
        world, vm, g_ampa, g_nmda, ampa, nmda, ampa_lbl, nmda_lbl, _ = build_nmda_world(
            gate_val=0.0, ampa_val=0.0, vm_val=V_REST, show_names=False
        )
        head = heading("Two events must coincide", color=TEXT)

        na_out = make_ion_stream(cx=-3.0, n=12, color=NA_COL, seed=51, spread_x=0.52, wall_top=1.12, gate_fn=lambda: False)
        ca_out = make_ion_stream(cx=0.4, n=12, color=CA_COL, seed=52, spread_x=0.48, wall_top=1.42, gate_fn=lambda: False)
        mg_dots = VGroup(*[
            Dot(radius=0.12, color=MG_COL).move_to([0.4 + dx, 1.55 + dy, 0])
            for dx, dy in [(-0.35, 0.2), (0.0, 0.45), (0.35, 0.15)]
        ])

        self.add(world, head, na_out, ca_out, mg_dots)

        self.at("at synapses")
        self.play(FadeIn(nmda_lbl), run_time=0.55)

        self.at("glutamate receptors")
        self.play(FadeIn(ampa_lbl), run_time=0.55)

        self.at("glutamate bound")
        glut = RoundedRectangle(
            corner_radius=0.10, width=0.38, height=0.28,
            color=LIGAND_COL, fill_color=LIGAND_COL, fill_opacity=0.92,
        ).move_to([-0.61, 2.25, 0])
        gl_lbl = T("glutamate", size=22, color=LIGAND_COL).move_to([-0.98, 1.72, 0], aligned_edge=RIGHT)
        self.play(glut.animate.move_to(nmda.outer_pocket_pts[0]), FadeIn(gl_lbl), run_time=0.7)

        self.at("plus glycine")
        gly = RoundedRectangle(
            corner_radius=0.10, width=0.38, height=0.28,
            color=LIGAND_COL, fill_color=LIGAND_COL, fill_opacity=0.92,
        ).move_to([1.41, 2.25, 0])
        gy_lbl = T("glycine / D-serine", size=22, color=LIGAND_COL).move_to([1.72, 1.72, 0], aligned_edge=LEFT)
        self.play(gly.animate.move_to(nmda.outer_pocket_pts[1]), FadeIn(gy_lbl), run_time=0.7)

        self.at("its gate opens")
        self.play(g_nmda.animate.set_value(1.0), run_time=0.6)

        self.at("yet magnesium ions")
        self.play(mg_dots[1].animate.move_to([0.4, 1.55, 0]), run_time=0.8)
        self.finish()


def build_predict_backdrop():
    """Exact world state shared between S06PredictQ and S07PredictPause."""
    world, vm, g_ampa, g_nmda, ampa, nmda, *_ = build_nmda_world(
        gate_val=1.0, ampa_val=0.0, vm_val=V_REST, ligands_bound=True
    )
    neg_signs = VGroup(*[
        minus_mark([x, -0.82, 0], size=0.16, color=VOLT_COL, stroke=3.2)
        for x in (-4.2, -1.5, 1.7, 2.5)
    ])
    mg_wait = VGroup(
        Dot(radius=0.13, color=MG_COL).move_to([0.4, 1.55, 0]),
        Dot(radius=0.11, color=MG_COL).move_to([0.05, 1.85, 0]),
    )
    ions_wait = VGroup(
        Dot(radius=0.10, color=NA_COL).move_to([-3.2, 1.65, 0]),
        Dot(radius=0.10, color=NA_COL).move_to([-2.7, 1.95, 0]),
        Dot(radius=0.10, color=NA_COL).move_to([0.15, 1.48, 0]),
        Dot(radius=0.10, color=CA_COL).move_to([0.65, 1.52, 0]),
        Dot(radius=0.10, color=CA_COL).move_to([0.40, 2.05, 0]),
    )
    return VGroup(world, neg_signs, mg_wait, ions_wait)


class S06PredictQ(SpokenScene):
    def construct(self):
        world, vm, g_ampa, g_nmda, ampa, nmda, *_ = build_nmda_world(
            gate_val=0.0, ampa_val=0.0, vm_val=V_REST, ligands_bound=True
        )
        neg_signs = VGroup(*[
            minus_mark([x, -0.82, 0], size=0.16, color=VOLT_COL, stroke=3.2)
            for x in (-4.2, -1.5, 1.7, 2.5)
        ])
        mg_hover = Dot(radius=0.13, color=MG_COL).move_to([0.4, 1.65, 0]).set_z_index(5)
        mg_far = Dot(radius=0.11, color=MG_COL).move_to([0.05, 1.85, 0]).set_z_index(5)
        na_hover = make_ion_stream(
            cx=0.4, n=10, color=NA_COL, seed=61, spread_x=0.85, wall_top=1.42,
            gate_fn=lambda: False, block_y_fn=lambda: 1.44,
        )
        ca_hover = make_ion_stream(
            cx=0.4, n=10, color=CA_COL, seed=62, spread_x=0.85, wall_top=1.42,
            gate_fn=lambda: False, block_y_fn=lambda: 1.48,
        )
        self.add(world, mg_hover, mg_far, na_hover, ca_hover)

        self.at("at rest")
        vm_hl = SurroundingRectangle(world[3][4], color=VOLT_COL, buff=0.08, stroke_width=3.0)
        self.play(Create(vm_hl), run_time=0.45)
        self.play(FadeOut(vm_hl), run_time=0.45)

        self.at("negative inside")
        self.play(FadeIn(neg_signs), run_time=0.6)

        self.at("glutamate opens")
        gate_hl = SurroundingRectangle(nmda.gate, color=TEAL, buff=0.10, stroke_width=2.5)
        self.play(g_nmda.animate.set_value(1.0), Create(gate_hl), run_time=0.7)
        self.play(FadeOut(gate_hl), run_time=0.4)

        self.at("Pause and predict")
        q = question_card("Predict: Why does almost no current flow?", y=BOTTOM_Y + 0.15, color=GOLD)
        self.play(FadeIn(q), run_time=0.55)

        self.at("almost no current flow")
        self.play(mg_hover.animate.move_to([0.4, 1.55, 0]), run_time=0.7)
        self.finish()


class S07PredictPause(PredictPause):
    QUESTION = "Predict: Why does almost no current flow?"
    SECONDS = 4.5

    def backdrop(self):
        return build_predict_backdrop()


class S08PredictReveal(SpokenScene):
    def construct(self):
        world, vm, g_ampa, g_nmda, ampa, nmda, *_ = build_nmda_world(
            gate_val=1.0, ampa_val=0.0, vm_val=V_REST, ligands_bound=True
        )
        neg_signs = VGroup(*[
            minus_mark([x, -0.82, 0], size=0.16, color=VOLT_COL, stroke=3.2)
            for x in (-4.2, -1.5, 1.7, 2.5)
        ])
        mg_cork = Dot(radius=0.15, color=MG_COL).move_to([0.4, 1.55, 0]).set_z_index(5)
        mg_blocked = {"in_pore": False}
        allow_flow = {"on": False}

        na_ampa = make_ion_stream(
            cx=-3.0, n=12, color=NA_COL, seed=81, spread_x=0.52, wall_top=1.12, y_bot=-1.60,
            gate_fn=lambda: g_ampa.get_value() > 0.5,
            speed_fn=lambda: max(0.45, (E_NA - vm.get_value()) / 75.0),
        )
        na_nmda = make_ion_stream(
            cx=0.4, n=10, color=NA_COL, seed=82, spread_x=0.48, wall_top=1.42, y_bot=-1.60,
            gate_fn=lambda: allow_flow["on"],
            block_y_fn=lambda: 0.35 if mg_blocked["in_pore"] else (None if allow_flow["on"] else 1.44),
            speed_fn=lambda: max(0.45, (E_NA - vm.get_value()) / 75.0),
        )
        ca_nmda = make_ion_stream(
            cx=0.4, n=10, color=CA_COL, seed=83, spread_x=0.48, wall_top=1.42, y_bot=-1.60,
            gate_fn=lambda: allow_flow["on"],
            block_y_fn=lambda: 0.35 if mg_blocked["in_pore"] else (None if allow_flow["on"] else 1.48),
            speed_fn=lambda: max(0.45, (E_CA - vm.get_value()) / 100.0),
        )

        self.add(world, neg_signs, mg_cork, na_ampa, na_nmda, ca_nmda)

        self.at("pulls it into the open pore")
        mg_blocked["in_pore"] = True
        blk_lbl = T("Mg2+ block", size=24, color=MG_COL).move_to([1.88, 0.72, 0], aligned_edge=LEFT)
        self.play(
            mg_cork.animate.move_to([0.4, 0.0, 0]),
            FadeIn(blk_lbl),
            run_time=0.65,
        )

        self.at("nearby glutamate receptors open")
        ampa_glut = RoundedRectangle(
            corner_radius=0.10, width=0.38, height=0.28,
            color=LIGAND_COL, fill_color=LIGAND_COL, fill_opacity=0.92,
        ).move_to([-4.5, 1.8, 0])
        self.play(ampa_glut.animate.move_to(ampa.outer_pocket_pts[0]), run_time=0.55)
        self.play(g_ampa.animate.set_value(1.0), run_time=0.5)

        vm_mode = {"state": "ampa"}

        def drive_vm(mob, dt):
            if vm_mode["state"] == "ampa":
                vm.set_value(integrate_vm(vm.get_value(), g_na=1.0, dt=dt, tau=1.1))
            elif vm_mode["state"] == "both":
                vm.set_value(integrate_vm(vm.get_value(), g_na=2.0, g_ca=1.2, dt=dt, tau=1.0))

        driver = Mobject()
        driver.add_updater(drive_vm)
        self.add(driver)

        self.at("pull weakens")
        self.play(neg_signs.animate.set_opacity(0.25), run_time=0.7)

        self.at("magnesium is driven back out")
        mg_blocked["in_pore"] = False
        allow_flow["on"] = True
        vm_mode["state"] = "both"
        expel_lbl = T("Mg2+ expelled", size=24, color=MG_COL).move_to([1.88, 0.72, 0], aligned_edge=LEFT)
        self.play(
            mg_cork.animate.move_to([0.4, 1.95, 0]),
            swap(blk_lbl, expel_lbl),
            run_time=0.85,
        )

        self.at("two events must coincide")
        c1 = T("1. Glutamate bound", size=24, color=LIGAND_COL).move_to([-3.3, 3.25, 0])
        c2 = T("2. Cell depolarized", size=24, color=VOLT_COL).move_to([0.3, 3.25, 0])
        self.play(FadeIn(c1), FadeIn(c2), run_time=0.6)
        self.finish()


class S09PoreBlockers(SpokenScene):
    def construct(self):
        vm = ValueTracker(V_REST)
        g_na = ValueTracker(1.0)
        g_nmda = ValueTracker(0.0)

        bilayer = build_bilayer(pore_xs=(-3.0, 0.4), pore_half_w=0.54)
        ch_na = ChannelBody(cx=-3.0, wall_h=2.0, gate_tracker=g_na)
        ch_nmda = ChannelBody(cx=0.4, wall_h=2.1, gate_tracker=g_nmda, outer_pockets=1, tall=True)
        gauge = VmGauge(vm)
        leg = ion_legend([("Na+", NA_COL), ("Ca2+", CA_COL)], top_left=(-6.05, 2.05))

        na_lbl = T("Na+ channel", size=24, color=CHAN_COL).move_to([-3.0, -2.15, 0])
        nmda_lbl = T("NMDA receptor", size=24, color=CHAN_COL).move_to([0.4, -2.15, 0])
        head = heading("Toxins and drugs plug the pore", color=PLUG_COL)

        ttx_in = {"blocked": False}
        ket_in = {"blocked": False}

        na_stream = make_ion_stream(
            cx=-3.0, n=14, color=NA_COL, seed=91, spread_x=0.52, wall_top=1.12, y_bot=-1.60,
            gate_fn=lambda: not ttx_in["blocked"] and g_na.get_value() > 0.5,
            block_y_fn=lambda: 1.25 if ttx_in["blocked"] else None,
            speed_fn=lambda: 1.0,
        )
        nmda_na = make_ion_stream(
            cx=0.4, n=9, color=NA_COL, seed=92, spread_x=0.46, wall_top=1.42, y_bot=-1.60,
            gate_fn=lambda: not ket_in["blocked"] and g_nmda.get_value() > 0.5,
            block_y_fn=lambda: 0.45 if ket_in["blocked"] else None,
            speed_fn=lambda: 1.0,
        )
        nmda_ca = make_ion_stream(
            cx=0.4, n=9, color=CA_COL, seed=93, spread_x=0.46, wall_top=1.42, y_bot=-1.60,
            gate_fn=lambda: not ket_in["blocked"] and g_nmda.get_value() > 0.5,
            block_y_fn=lambda: 0.45 if ket_in["blocked"] else None,
            speed_fn=lambda: 1.0,
        )

        # Hold Na+ gate closed at rest before stimulus until TTX lodges, so Vm=-70 mV is consistent
        g_na.set_value(0.0)
        self.add(bilayer, ch_na, ch_nmda, gauge, leg, na_lbl, nmda_lbl, head, na_stream, nmda_na, nmda_ca)

        self.at("Tetrodotoxin lodges")
        ttx = RoundedRectangle(
            corner_radius=0.14, width=0.58, height=0.42,
            color=PLUG_COL, fill_color=PLUG_COL, fill_opacity=0.92, stroke_width=2.5,
        ).move_to([-3.0, 1.95, 0])
        ttx_lbl = T("Tetrodotoxin", size=24, color=PLUG_COL).move_to([-4.05, 0.92, 0], aligned_edge=RIGHT)
        ttx_in["blocked"] = True
        self.play(ttx.animate.move_to([-3.0, 0.92, 0]), FadeIn(ttx_lbl), run_time=0.8)

        self.at("no impulse starts")
        no_imp = T("no impulse", size=24, color=PLUG_COL).move_to([-3.0, -2.70, 0])
        self.play(FadeIn(no_imp), run_time=0.5)

        self.at("Ketamine enters")
        # NMDA opens briefly to admit ketamine, then ketamine plugs from within
        self.play(g_nmda.animate.set_value(1.0), run_time=0.4)
        ket = RoundedRectangle(
            corner_radius=0.12, width=0.44, height=0.38,
            color=PLUG_COL, fill_color=PLUG_COL, fill_opacity=0.92, stroke_width=2.5,
        ).move_to([0.4, 2.05, 0])
        ket_lbl = T("Ketamine", size=24, color=PLUG_COL).move_to([1.45, 1.05, 0], aligned_edge=LEFT)
        ket_in["blocked"] = True
        self.play(ket.animate.move_to([0.4, 0.05, 0]), FadeIn(ket_lbl), run_time=0.85)

        self.at("open less often")
        less_lbl = T("opens less often", size=24, color=PLUG_COL).move_to([0.4, -2.70, 0])
        self.play(g_nmda.animate.set_value(0.0), FadeIn(less_lbl), run_time=0.8)
        self.finish()


class S10Closing(SpokenScene):
    def construct(self):
        vm = ValueTracker(V_REST)
        gate = ValueTracker(0.0)
        s4_t = ValueTracker(0.0)
        blocked = {"y": None}

        bilayer = build_bilayer(pore_xs=(-1.2,), pore_half_w=0.95)
        ch = ChannelBody(cx=-1.2, gate_tracker=gate, s4_tracker=s4_t, outer_pockets=0)
        outer_pocket_pt = np.array([-1.2 - 1.01, 0.735, 0.0])
        outer_pocket = ch._make_pocket(outer_pocket_pt[0], outer_pocket_pt[1], side=-1)
        gauge = VmGauge(vm)
        leg = ion_legend([("Na+", NA_COL), ("Ca2+", CA_COL), ("Mg2+", MG_COL)], top_left=(-6.05, 2.05))

        na_ions = make_ion_stream(
            cx=-1.2, n=14, color=NA_COL, seed=101, y_bot=-1.70,
            gate_fn=lambda: gate.get_value() > 0.5 and blocked["y"] is None,
            block_y_fn=lambda: blocked["y"],
            speed_fn=lambda: max(0.45, (E_NA - vm.get_value()) / 75.0),
        )
        ca_ions = make_ion_stream(
            cx=-1.2, n=8, color=CA_COL, seed=102, y_bot=-1.70,
            gate_fn=lambda: gate.get_value() > 0.5 and blocked["y"] is None,
            block_y_fn=lambda: blocked["y"],
            speed_fn=lambda: max(0.45, (E_CA - vm.get_value()) / 100.0),
        )

        gate_tag = T("1. Gate", size=26, color=CHAN_COL).move_to([0.75, -0.85, 0], aligned_edge=LEFT)
        block_tag = T("2. Pore block", size=26, color=PLUG_COL).move_to([0.75, 0.85, 0], aligned_edge=LEFT)
        self.add(bilayer, ch, gauge, leg, na_ions, ca_ions, gate_tag, block_tag)

        def drive_vm(mob, dt):
            if gate.get_value() > 0.5 and blocked["y"] is None:
                vm.set_value(integrate_vm(vm.get_value(), g_na=1.8, dt=dt, tau=0.8))
            else:
                vm.set_value(integrate_vm(vm.get_value(), g_na=0.0, dt=dt, tau=0.7))

        driver = Mobject()
        driver.add_updater(drive_vm)
        self.add(driver)

        self.at("sharp switches")
        self.play(gate.animate.set_value(1.0), run_time=0.55)
        self.play(gate.animate.set_value(0.0), run_time=0.55)

        self.at("Ligands")
        lig = RoundedRectangle(
            corner_radius=0.10, width=0.40, height=0.28,
            color=LIGAND_COL, fill_color=LIGAND_COL, fill_opacity=0.92,
        ).move_to(outer_pocket_pt)
        key_lbl = T("Ligand", size=26, color=LIGAND_COL).move_to([-1.2, 2.75, 0])
        self.play(FadeIn(outer_pocket), FadeIn(lig), FadeIn(key_lbl), gate.animate.set_value(1.0), run_time=0.55)

        self.at("voltage")
        v_lbl = T("Voltage (S4)", size=26, color=VOLT_COL).move_to([-1.2, 2.75, 0])
        self.play(
            Succession(
                AnimationGroup(FadeOut(lig), FadeOut(outer_pocket), run_time=0.18),
                s4_t.animate(run_time=0.40).set_value(1.0),
            ),
            swap(key_lbl, v_lbl, run_time=0.58),
        )

        self.at("physical stimuli")
        h_lbl = T("Physical (heat)", size=26, color=HEAT_COL).move_to([-1.2, 2.75, 0])
        phase = ValueTracker(0.0)
        heat_waves = always_redraw(
            lambda: VGroup(*[
                FunctionGraph(
                    lambda t, p=phase.get_value(): 0.12 * np.sin(5.0 * t + p),
                    x_range=[-0.6, 0.6],
                    color=HEAT_COL,
                    stroke_width=4.0,
                ).rotate(-PI / 2).move_to([ox, 1.50, 0])
                for ox in (-2.75, 0.35)
            ])
        )
        phase_driver = Mobject()
        phase_driver.add_updater(lambda m, dt: phase.increment_value(4.5 * dt))
        self.add(phase_driver)
        self.play(
            s4_t.animate.set_value(0.0),
            gate.animate.set_value(0.0),
            swap(v_lbl, h_lbl),
            FadeIn(heat_waves),
            run_time=0.55,
        )

        self.at("open the gate")
        self.play(gate.animate.set_value(1.0), run_time=0.55)

        self.at("sensitive magnesium")
        blocked["y"] = 0.35
        mg_plug = Dot(radius=0.14, color=MG_COL).move_to([-1.2, 0.0, 0])
        blk_lbl = T("Mg2+ block", size=24, color=MG_COL).move_to([0.75, 1.40, 0], aligned_edge=LEFT)
        self.play(FadeOut(h_lbl), FadeOut(heat_waves), FadeIn(mg_plug), FadeIn(blk_lbl), run_time=0.6)

        self.at("a toxin")
        tox_plug = RoundedRectangle(
            corner_radius=0.12, width=0.54, height=0.38,
            color=PLUG_COL, fill_color=PLUG_COL, fill_opacity=0.92,
        ).move_to([-1.2, 0.85, 0])
        tox_lbl = T("Toxin / drug", size=24, color=PLUG_COL).move_to([0.75, 1.40, 0], aligned_edge=LEFT)
        blocked["y"] = 1.15
        self.play(FadeOut(mg_plug), FadeIn(tox_plug), swap(blk_lbl, tox_lbl), run_time=0.65)

        self.at("Signals open the gate")
        blocked["y"] = None
        cap = caption("Signals open the gate, and pore blocks control whether ions pass.")
        self.play(
            FadeOut(tox_plug), FadeOut(tox_lbl),
            gate.animate.set_value(1.0),
            FadeIn(cap),
            run_time=0.75,
        )
        self.finish()


class S11End(EndCard):
    LINE = "Signals open the gate, and pore blocks control whether ions pass."
