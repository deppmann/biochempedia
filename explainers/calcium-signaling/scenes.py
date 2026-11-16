"""How a Cell Makes a Calcium Signal (calcium-signaling)

COLOUR MAP:
  CA_COLOR     = TEAL     (#3FB8C0)  calcium ions (Ca2+)
  ER_COLOR     = #A47CE0             endoplasmic reticulum (ER) store
  CHAN_COLOR   = GOLD     (#D4A843)  channels (ON mechanisms)
  PUMP_COLOR   = #F47868             pumps and exchanger (coral, OFF mechanisms)
  BUF_COLOR    = #5C9EFF             cytosolic calcium buffers (blue, OFF mechanisms)
  SENS_COLOR   = GREEN    (#83C167)  cytosolic sensor proteins
  ACTIVE_COLOR = #FF9F43             active protein output (orange)
  TRACE_COLOR  = WHITE    (#FFFFFF)  schematic free-calcium traces
  MEMB_COLOR   = GREY     (#8B93A1)  plasma membrane & neutral walls
  CAMP_COLOR   = YELLOW   (#F5D547)  cyclic AMP comparison (S01 only)

CARRIED WORLD:
  A full-frame cell cross-section (extracellular band at top, double plasma membrane,
  large cytosol holding green sensor proteins and blue buffers, purple ER store at lower
  left) paired on the right with a schematic FREE Ca2+ gauge or live Plot trace.

WHAT CHANGES IN EACH SPOKEN SCENE (computed from seeded walks & compartment flux):
  s01_hook:     A Ca2+ ion enters and leaves a dashed MAKE/DESTROY box unchanged while cAMP
                appears, signals, and fades; the Ca2+ moves to a cell-shaped ? holding a protein.
  s03_gradient: Seeded ions crowd outside and inside the purple ER while rotating coral pumps
                carry cytosolic ions away and the FREE gauge holds low.
  s04_channel:  Zoomed gold channel doors separate, seeded Ca2+ ions pour down the gradient into
                the cytosol, the computed white schematic trace rises, and a sensor gains a teal ring.
  s05_predict:  Split TwoPanel pits a closed gold channel against a coral pump while one teal ion
                shuttles between them above flat schematic traces and a question card.
  s07_reveal:   Left gold channel opens and trace rises; trace resets and right coral pump expels
                ions as trace falls; headings swap to ON and OFF (pump, exchanger, buffer).
  s08_balance:  Opposing channel and pump fluxes compete in the full cell; entry outruns removal to
                raise the computed trace, then channels close and buffers + pumps restore baseline.
  s09_store:    Plasma-membrane and ER gold channels open sequentially for different durations,
                launching two localized teal plumes near distinct sensors and two computed trace pulses.
  s10_close:    Plumes settle back into the carried cell, then one full computed pulse (fast rise on
                channel opening, recovery via off machinery) restores the resting distribution.
"""
from bp_parts import *

# ---------------------------------------------------------------------------
# Film Colour Map
# ---------------------------------------------------------------------------
CA_COLOR = TEAL          # #3FB8C0
ER_COLOR = "#A47CE0"     # purple ER store
CHAN_COLOR = GOLD        # #D4A843
PUMP_COLOR = "#F47868"   # coral pumps & exchanger
BUF_COLOR = "#5C9EFF"    # blue buffers
SENS_COLOR = GREEN       # #83C167
ACTIVE_COLOR = "#FF9F43" # orange active output
TRACE_COLOR = WHITE      # schematic free-Ca2+ trace
MEMB_COLOR = GREY        # #8B93A1
CAMP_COLOR = YELLOW      # #F5D547


# ---------------------------------------------------------------------------
# Shared Geometric Builders & Deterministic Simulation Helpers
# ---------------------------------------------------------------------------
def make_ca_dot(pos=ORIGIN, radius=0.105, color=CA_COLOR, glow=False):
    """A calcium ion dot; optional white inner highlight for featured tracked ions."""
    d = Dot(pos, radius=radius, color=color, fill_opacity=0.95)
    if glow:
        ring = Circle(radius=radius + 0.055, color=WHITE, stroke_width=2.5).move_to(pos)
        return VGroup(d, ring)
    return d


def make_sensor_cup(pos=ORIGIN, angle=0.0, scale=1.0, active=False, teal_ring=False):
    """A cytosolic sensor protein drawn as an open C-shaped cup (no molecular structure)."""
    r = 0.42 * scale
    col = ACTIVE_COLOR if active else SENS_COLOR
    arc = Arc(radius=r, start_angle=0.55, angle=TAU - 1.1, stroke_color=col, stroke_width=8 * scale)
    fill = Circle(radius=r * 0.88, stroke_width=0, fill_color=col, fill_opacity=0.25)
    g = VGroup(fill, arc).rotate(angle).move_to(pos)
    if teal_ring:
        ring = Circle(radius=r + 0.11 * scale, stroke_color=CA_COLOR, stroke_width=4.0 * scale).move_to(pos)
        g.add(ring)
    return g


def make_buffer_cup(pos=ORIGIN, angle=PI / 2, scale=1.0):
    """A blue cytosolic buffer cup that catches free calcium ions."""
    r = 0.27 * scale
    arc = Arc(radius=r, start_angle=0.7, angle=TAU - 1.4, stroke_color=BUF_COLOR, stroke_width=6 * scale)
    fill = Circle(radius=r * 0.85, stroke_width=0, fill_color=BUF_COLOR, fill_opacity=0.25)
    return VGroup(fill, arc).rotate(angle).move_to(pos)


def make_channel(center, width=1.1, height=0.56, open_frac=0.0):
    """A gold membrane channel with two doors that separate horizontally."""
    cx, cy, _ = np.array(center, dtype=float)
    door_w = width * 0.42
    gap = 0.04 + 0.48 * open_frac
    left_x = cx - gap / 2 - door_w / 2
    right_x = cx + gap / 2 + door_w / 2
    d_l = RoundedRectangle(
        corner_radius=0.08, width=door_w, height=height,
        stroke_color=CHAN_COLOR, stroke_width=3.0, fill_color=CHAN_COLOR, fill_opacity=0.38
    ).move_to([left_x, cy, 0])
    d_r = RoundedRectangle(
        corner_radius=0.08, width=door_w, height=height,
        stroke_color=CHAN_COLOR, stroke_width=3.0, fill_color=CHAN_COLOR, fill_opacity=0.38
    ).move_to([right_x, cy, 0])
    return VGroup(d_l, d_r)


def live_channel(center, open_tracker, width=1.1, height=0.56):
    """A gold channel driven continuously by open_tracker in [0, 1]."""
    return always_redraw(lambda: make_channel(center, width=width, height=height, open_frac=open_tracker.get_value()))


def make_pump(center, radius=0.32, phase=0.0):
    """A coral membrane pump rendered as a rotating two-blade transporter wheel."""
    c = np.array(center, dtype=float)
    ring = Circle(radius=radius, stroke_color=PUMP_COLOR, stroke_width=4.0, fill_color=PUMP_COLOR, fill_opacity=0.25).move_to(c)
    bar1 = Line(c + LEFT * radius * 0.82, c + RIGHT * radius * 0.82, stroke_color=PUMP_COLOR, stroke_width=4.0)
    bar2 = Line(c + DOWN * radius * 0.82, c + UP * radius * 0.82, stroke_color=PUMP_COLOR, stroke_width=4.0)
    cross = VGroup(bar1, bar2).rotate(phase, about_point=c)
    return VGroup(ring, cross)


def add_pump_spin(pump_group, speed_fn):
    """Continuously rotate the inner cross of a coral pump around its ring's live center."""
    ring, cross = pump_group[0], pump_group[1]

    def u(mob, dt):
        c = ring.get_center()
        mob.move_to(c)
        mob.rotate(speed_fn() * dt, about_point=c)

    cross.add_updater(u)
    return pump_group


def add_confined_drift(dots, box, seed=7, speed=0.45):
    """Seeded thermal walk confining every dot strictly inside box=(x0, x1, y0, y1)."""
    rng = np.random.default_rng(seed)
    x0, x1, y0, y1 = box
    angles = rng.uniform(0, TAU, len(dots))
    vels = np.column_stack([np.cos(angles), np.sin(angles), np.zeros(len(dots))]) * speed
    for i, d in enumerate(dots):
        v = vels[i].copy()

        def step(mob, dt, v=v):
            p = mob.get_center() + v * dt
            if p[0] < x0:
                p[0] = x0
                v[0] = abs(v[0])
            elif p[0] > x1:
                p[0] = x1
                v[0] = -abs(v[0])
            if p[1] < y0:
                p[1] = y0
                v[1] = abs(v[1])
            elif p[1] > y1:
                p[1] = y1
                v[1] = -abs(v[1])
            mob.move_to(p)

        d.add_updater(step)
    return dots


def seed_positions(box, n, seed=7):
    """Generate n deterministic positions inside (x0, x1, y0, y1)."""
    rng = np.random.default_rng(seed)
    x0, x1, y0, y1 = box
    xs = rng.uniform(x0, x1, n)
    ys = rng.uniform(y0, y1, n)
    return [np.array([x, y, 0.0]) for x, y in zip(xs, ys)]


def make_cell_shell(x0=-6.1, x1=1.85, y_bot=-2.7, y_memb=1.85, y_top=3.2):
    """Build the carried cell cross-section shell (extracellular tint, cell body, plasma membrane, ER store).

    Leaves clear label zones so drifting ions never pass through compartment text, and stops at x1=1.85
    to leave ample clearance before the right-hand Plot axis labels.
    """
    w = x1 - x0
    cx = (x0 + x1) / 2

    # Extracellular region (tinted subtly teal, cleanly above membrane)
    ext_h = y_top - (y_memb + 0.08)
    ext_bg = Rectangle(
        width=w, height=ext_h, stroke_width=0,
        fill_color=CA_COLOR, fill_opacity=0.18
    ).move_to([cx, y_memb + 0.08 + ext_h / 2, 0])

    # Cytosol interior box cleanly below membrane
    cyto_h = (y_memb - 0.08) - y_bot
    cyto_bg = RoundedRectangle(
        corner_radius=0.22, width=w, height=cyto_h,
        stroke_color=MEMB_COLOR, stroke_width=5.0,
        fill_color="#1A2538", fill_opacity=0.92
    ).move_to([cx, y_bot + cyto_h / 2, 0])

    # Plasma membrane double-line highlight along y_memb
    pm_top = Line([x0, y_memb + 0.08, 0], [x1, y_memb + 0.08, 0], color=MEMB_COLOR, stroke_width=4.0)
    pm_bot = Line([x0, y_memb - 0.08, 0], [x1, y_memb - 0.08, 0], color=MEMB_COLOR, stroke_width=4.0)

    # Purple ER store in lower-left of cytosol
    er_x0, er_x1 = x0 + 0.40, x1 - 1.75
    er_y0, er_y1 = y_bot + 0.25, -0.25
    er_box = RoundedRectangle(
        corner_radius=0.30, width=er_x1 - er_x0, height=er_y1 - er_y0,
        stroke_color=ER_COLOR, stroke_width=4.5,
        fill_color=ER_COLOR, fill_opacity=0.28
    ).move_to([(er_x0 + er_x1) / 2, (er_y0 + er_y1) / 2, 0])

    # Compartment labels placed in ion-free corners
    lbl_out = T("outside", 26, TEXT).move_to([x0 + 0.22, y_top - 0.28, 0], aligned_edge=LEFT)
    lbl_cyto = T("cytosol", 26, TEXT).move_to([x0 + 0.22, y_memb - 0.44, 0], aligned_edge=LEFT)
    lbl_er = T("ER store", 26, ER_COLOR).move_to([er_x0 + 0.22, er_y0 + 0.28, 0], aligned_edge=LEFT)

    shell = VGroup(ext_bg, cyto_bg, pm_top, pm_bot, er_box, lbl_out, lbl_cyto, lbl_er)
    shell.ext_box = (x0 + 1.85, x1 - 0.25, y_memb + 0.25, y_top - 0.18)
    shell.er_box = (er_x0 + 1.95, er_x1 - 0.25, er_y0 + 0.22, er_y1 - 0.35)
    shell.pm_y = y_memb
    shell.er_top_y = er_y1
    shell.pm_chan_x = x0 + 2.35
    shell.pm_pump_x = x1 - 1.35
    shell.er_chan_x = er_x0 + 1.95
    shell.er_pump_x = er_x1 - 1.05
    shell.er_box_mob = er_box
    return shell


def make_free_gauge(level_tracker, center=(4.55, 0.25, 0), height=4.4, width=1.15):
    """A tall vertical FREE Ca2+ bar gauge driven by level_tracker in [0, 1]."""
    c = np.array(center, dtype=float)
    frame = RoundedRectangle(
        corner_radius=0.18, width=width, height=height,
        stroke_color=MEMB_COLOR, stroke_width=3.5, fill_color="#141B29", fill_opacity=0.95
    ).move_to(c)
    title = T("FREE", 28, TEXT).next_to(frame, UP, buff=0.22)
    sub = T("Ca²⁺", 26, CA_COLOR).next_to(frame, DOWN, buff=0.20)
    bot_y = c[1] - height / 2 + 0.12
    max_h = height - 0.24

    def mk_bar():
        f = float(np.clip(level_tracker.get_value(), 0.05, 1.0))
        bh = f * max_h
        return RoundedRectangle(
            corner_radius=0.10, width=width - 0.24, height=bh,
            stroke_width=0, fill_color=CA_COLOR, fill_opacity=0.92
        ).move_to([c[0], bot_y + bh / 2, 0])

    bar = always_redraw(mk_bar)
    low_lbl = T("low", 24, TEXT).next_to([c[0] - width / 2, bot_y + 0.18, 0], LEFT, buff=0.18)
    high_lbl = T("high", 24, TEXT).next_to([c[0] - width / 2, bot_y + max_h - 0.18, 0], LEFT, buff=0.18)
    return VGroup(frame, bar, title, sub, low_lbl, high_lbl)


def make_trace_plot(box=(3.15, 6.2, -1.7, 2.2), xr=(0, 10), yr=(0, 1.0), ylabel="FREE Ca²⁺"):
    """Schematic time-course plot in the right-hand zone."""
    return Plot(
        box=box, xr=xr, yr=yr,
        xticks=[], yticks=[(0.1, "low"), (0.9, "high")],
        xlabel="time", ylabel=ylabel, color=MEMB_COLOR, size=24, label_size=26, stroke=3.5
    )


def build_predict_stage():
    """Shared TwoPanel picture used by S05Predict, S06Pause, and the start of S07Reveal."""
    tp = TwoPanel("open channel", "speed pump", colors=(CHAN_COLOR, PUMP_COLOR), top=3.25, bottom=-2.05, gap=0.45, width=12.6, size=30)

    # Left panel: closed gold channel in membrane + outside Ca2+ + cytosolic sensor + flat trace
    lc, _, _ = tp.area("left")
    lx = lc[0]
    l_memb = Line([lx - 2.6, 1.05, 0], [lx + 2.6, 1.05, 0], color=MEMB_COLOR, stroke_width=5)
    l_ext = Rectangle(width=5.2, height=0.95, stroke_width=0, fill_color=CA_COLOR, fill_opacity=0.16).move_to([lx, 1.55, 0])
    l_chan = make_channel([lx, 1.05, 0], width=1.1, height=0.52, open_frac=0.0)
    l_sens = make_sensor_cup([lx - 1.75, 0.35, 0], angle=-0.3, scale=0.76)
    l_dots = VGroup(*[make_ca_dot(p, radius=0.09) for p in seed_positions((lx - 2.3, lx + 2.3, 1.24, 1.90), 14, seed=11)])
    add_confined_drift(l_dots, (lx - 2.3, lx + 2.3, 1.24, 1.90), seed=11, speed=0.35)

    l_plot = Plot(box=(lx - 1.85, lx + 2.25, -1.85, -0.78), xr=(0, 6), yr=(0, 1),
                  xticks=[], yticks=[], xlabel="", ylabel="FREE", color=MEMB_COLOR, size=22, label_size=24, stroke=2.5)
    l_q = T("?", 34, TEXT).move_to([lx + 0.2, -1.28, 0])
    l_base = l_plot.curve(lambda t: 0.12, color=TRACE_COLOR, width=4)

    # Right panel: coral pump in membrane + outside Ca2+ + cytosolic sensor + flat trace
    rc, _, _ = tp.area("right")
    rx = rc[0]
    r_memb = Line([rx - 2.6, 1.05, 0], [rx + 2.6, 1.05, 0], color=MEMB_COLOR, stroke_width=5)
    r_ext = Rectangle(width=5.2, height=0.95, stroke_width=0, fill_color=CA_COLOR, fill_opacity=0.16).move_to([rx, 1.55, 0])
    r_pump = make_pump([rx, 1.05, 0], radius=0.34)
    add_pump_spin(r_pump, lambda: 0.8)
    r_sens = make_sensor_cup([rx + 1.75, 0.35, 0], angle=PI + 0.3, scale=0.76)
    r_dots = VGroup(*[make_ca_dot(p, radius=0.09) for p in seed_positions((rx - 2.3, rx + 2.3, 1.24, 1.90), 14, seed=12)])
    add_confined_drift(r_dots, (rx - 2.3, rx + 2.3, 1.24, 1.90), seed=12, speed=0.35)

    r_plot = Plot(box=(rx - 1.85, rx + 2.25, -1.85, -0.78), xr=(0, 6), yr=(0, 1),
                  xticks=[], yticks=[], xlabel="", ylabel="FREE", color=MEMB_COLOR, size=22, label_size=24, stroke=2.5)
    r_q = T("?", 34, TEXT).move_to([rx + 0.2, -1.28, 0])
    r_base = r_plot.curve(lambda t: 0.12, color=TRACE_COLOR, width=4)

    stage = VGroup(
        tp,
        l_ext, l_memb, l_dots, l_chan, l_sens, l_plot, l_base, l_q,
        r_ext, r_memb, r_dots, r_pump, r_sens, r_plot, r_base, r_q,
    )
    stage.tp = tp
    stage.lx, stage.rx = lx, rx
    stage.l_chan, stage.l_sens, stage.l_plot, stage.l_base, stage.l_q, stage.l_dots = l_chan, l_sens, l_plot, l_base, l_q, l_dots
    stage.r_pump, stage.r_sens, stage.r_plot, stage.r_base, stage.r_q, stage.r_dots = r_pump, r_sens, r_plot, r_base, r_q, r_dots
    return stage


# ---------------------------------------------------------------------------
# Scenes
# ---------------------------------------------------------------------------
class S01Hook(SpokenScene):
    def construct(self):
        # Left: dashed MAKE / DESTROY box; Right: cell-shaped question mark (present cleanly)
        make_box = DashedVMobject(
            RoundedRectangle(corner_radius=0.22, width=4.0, height=3.3, stroke_color=MEMB_COLOR, stroke_width=4.0),
            num_dashes=28
        ).move_to([-3.65, -0.1, 0])
        make_lbl = T("MAKE / DESTROY", 26, TEXT).next_to(make_box, UP, buff=0.22)

        # Large teal Ca2+ sphere with label cleanly inside so it never grazes outlines
        ca_circle = Dot([-5.8, -0.1, 0], radius=0.48, color=CA_COLOR, fill_opacity=0.96)
        ca_ring = Circle(radius=0.53, color=WHITE, stroke_width=2.5).move_to(ca_circle)
        ca_lbl = T("Ca²⁺", 26, BG, weight=BOLD).move_to(ca_circle)
        ca_group = VGroup(ca_circle, ca_ring, ca_lbl)

        # Cell-shaped question mark on the right
        cell_outline = RoundedRectangle(
            corner_radius=1.1, width=4.8, height=5.0,
            stroke_color=MEMB_COLOR, stroke_width=5.0,
            fill_color="#1A2538", fill_opacity=0.88
        ).move_to([3.3, -0.1, 0])
        q_mark = T("?", 120, GOLD).move_to(cell_outline.get_center() + UP * 0.25)

        self.play(FadeIn(make_box), FadeIn(make_lbl), FadeIn(ca_group), run_time=0.8)
        self.play(ca_group.animate.move_to(make_box.get_center()), run_time=1.3)

        self.at("cannot make")
        # Move Ca2+ straight through the dashed box unchanged, then cross out MAKE / DESTROY
        self.play(ca_group.animate.move_to([-0.8, -0.1, 0]), run_time=1.0)
        cross1 = Line(make_box.get_corner(DL) + UR * 0.35, make_box.get_corner(UR) + DL * 0.35, color=PUMP_COLOR, stroke_width=6)
        cross2 = Line(make_box.get_corner(UL) + DR * 0.35, make_box.get_corner(DR) + UL * 0.35, color=PUMP_COLOR, stroke_width=6)
        cross = VGroup(cross1, cross2)
        self.play(Create(cross), run_time=0.55)

        self.at("cyclic amp")
        # Beside it, cyclic AMP appears, sends a signal arrow, then disappears
        camp = chip("cyclic AMP", CAMP_COLOR, size=28).move_to([3.3, 1.5, 0])
        camp_arrow = Arrow([3.3, 1.0, 0], [3.3, -0.2, 0], color=CAMP_COLOR, stroke_width=5, buff=0.05)
        self.play(FadeIn(camp, scale=0.85), run_time=0.7)
        self.play(GrowArrow(camp_arrow), run_time=0.6)

        self.at("then disappear")
        self.play(FadeOut(camp), FadeOut(camp_arrow), run_time=0.7)

        self.at("calcium atoms remain")
        # Cell-shaped ? enters cleanly while Ca2+ traces an active arc in the center
        self.play(FadeIn(cell_outline), FadeIn(q_mark), run_time=0.7)
        ca_base = ca_group.get_center().copy()
        ca_group._t = 0.0

        def ca_arc(m, dt):
            m._t += dt
            m.move_to(ca_base + np.array([0.32 * np.sin(1.8 * m._t), 0.25 * np.cos(1.8 * m._t), 0]))

        ca_group.add_updater(ca_arc)
        self.wait(2.4)

        self.at("the puzzle")
        ca_group.remove_updater(ca_arc)
        self.play(ca_group.animate.move_to([0.25, -0.1, 0]), run_time=1.3)

        self.at("how to change")
        protein = make_sensor_cup([3.65, -1.35, 0], angle=0.3, scale=1.05)
        prot_lbl = T("protein", 28, SENS_COLOR).next_to(protein, LEFT, buff=0.22)
        self.play(
            q_mark.animate.scale(0.68).move_to([3.3, 1.2, 0]),
            FadeIn(protein), FadeIn(prot_lbl),
            run_time=0.8
        )
        self.play(ca_group.animate.move_to([0.32, 0.35, 0]), run_time=1.1)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Calcium: The Messenger Kept at Arm's Length"
    TITLE = "How a Cell Makes a Calcium Signal"


class S03Gradient(SpokenScene):
    def construct(self):
        cell = make_cell_shell()
        free_val = ValueTracker(0.08)
        gauge = make_free_gauge(free_val)
        tag = scope_tag("schematic")

        # Coral pumps present from start, slowly rotating to maintain low cytosolic resting Ca2+
        pm_pump = make_pump([cell.pm_pump_x, cell.pm_y, 0], radius=0.33)
        er_pump = make_pump([cell.er_pump_x, cell.er_top_y, 0], radius=0.33)
        pump_rate = ValueTracker(0.9)
        add_pump_spin(pm_pump, lambda: pump_rate.get_value())
        add_pump_spin(er_pump, lambda: pump_rate.get_value())

        cyto_dots = VGroup(
            make_ca_dot([-3.9, 0.55, 0], radius=0.115),
            make_ca_dot([-0.4, 0.25, 0], radius=0.115),
        )
        add_confined_drift(cyto_dots, (-4.3, -0.1, 0.1, 0.95), seed=31, speed=0.65)

        self.play(FadeIn(cell), FadeIn(gauge), FadeIn(tag), FadeIn(pm_pump), FadeIn(er_pump), FadeIn(cyto_dots), run_time=1.0)

        self.at("crowded outside")
        out_dots = VGroup(*[make_ca_dot(p, radius=0.105) for p in seed_positions(cell.ext_box, 26, seed=32)])
        add_confined_drift(out_dots, cell.ext_box, seed=32, speed=0.42)
        self.play(FadeIn(out_dots), run_time=0.9)

        self.at("inside the endoplasmic")
        er_dots = VGroup(*[make_ca_dot(p, radius=0.105) for p in seed_positions(cell.er_box, 24, seed=33)])
        add_confined_drift(er_dots, cell.er_box, seed=33, speed=0.40)
        self.play(FadeIn(er_dots), run_time=1.0)

        self.at("coral pumps")
        pump_lbl = T("pumps", 26, PUMP_COLOR).move_to([cell.pm_pump_x - 0.95, cell.pm_y - 0.52, 0])
        pump_rate.set_value(2.0)
        carry_pm = make_ca_dot([cell.pm_pump_x, cell.pm_y - 0.55, 0], radius=0.105, glow=True)
        carry_er = make_ca_dot([cell.er_pump_x, cell.er_top_y + 0.55, 0], radius=0.105, glow=True)
        self.play(FadeIn(pump_lbl), FadeIn(carry_pm), FadeIn(carry_er), run_time=0.6)
        self.play(
            carry_pm.animate.move_to([cell.pm_pump_x, cell.pm_y + 0.65, 0]),
            carry_er.animate.move_to([cell.er_pump_x, cell.er_top_y - 0.65, 0]),
            free_val.animate.set_value(0.06),
            run_time=2.5
        )
        self.play(FadeOut(carry_pm), FadeOut(carry_er), run_time=0.5)

        self.at("stored potential")
        arr_pm = Arrow([cell.pm_chan_x, cell.pm_y + 0.68, 0], [cell.pm_chan_x, cell.pm_y + 0.14, 0], color=CHAN_COLOR, stroke_width=5, buff=0)
        arr_er = Arrow([cell.er_chan_x, cell.er_top_y - 0.68, 0], [cell.er_chan_x, cell.er_top_y - 0.14, 0], color=CHAN_COLOR, stroke_width=5, buff=0)
        self.play(GrowArrow(arr_pm), GrowArrow(arr_er), run_time=0.9)

        self.at("cytosolic proteins")
        sens1 = make_sensor_cup([0.95, 0.15, 0], angle=0.4, scale=0.9)
        sens2 = make_sensor_cup([-1.55, 0.25, 0], angle=-0.6, scale=0.85)
        sens_lbl = T("cytosolic proteins", 26, SENS_COLOR).move_to([-0.25, 0.88, 0])
        self.play(FadeIn(sens1), FadeIn(sens2), FadeIn(sens_lbl), run_time=0.9)
        self.finish()


class S04Channel(SpokenScene):
    def construct(self):
        # Zoomed plasma membrane on the left; schematic white trace on the right
        ext_bg = Rectangle(width=7.4, height=1.65, stroke_width=0, fill_color=CA_COLOR, fill_opacity=0.18).move_to([-2.35, 2.38, 0])
        cyto_bg = RoundedRectangle(
            corner_radius=0.25, width=7.4, height=4.25,
            stroke_color=MEMB_COLOR, stroke_width=5, fill_color="#1A2538", fill_opacity=0.92
        ).move_to([-2.35, -0.72, 0])
        pm_top = Line([-6.05, 1.56, 0], [1.35, 1.56, 0], color=MEMB_COLOR, stroke_width=4.5)
        pm_bot = Line([-6.05, 1.40, 0], [1.35, 1.40, 0], color=MEMB_COLOR, stroke_width=4.5)
        out_lbl = T("outside", 26, TEXT).move_to([-5.8, 2.9, 0], aligned_edge=LEFT)
        cyto_lbl = T("cytosol", 26, TEXT).move_to([-5.8, 0.95, 0], aligned_edge=LEFT)

        open_t = ValueTracker(0.0)
        chan_pos = [-2.55, 1.48, 0]
        chan = live_channel(chan_pos, open_t, width=1.6, height=0.72)
        # Channel label placed cleanly inside upper-right cytosol clear of ions, doors, and sensor
        chan_lbl = T("channel", 28, CHAN_COLOR).move_to([-0.35, 0.85, 0])

        # Crowded outside ions (confined clear of "outside" label)
        out_dots = VGroup(*[make_ca_dot(p, radius=0.105) for p in seed_positions((-4.3, 1.1, 1.75, 3.05), 26, seed=41)])
        add_confined_drift(out_dots, (-4.3, 1.1, 1.75, 3.05), seed=41, speed=0.42)

        # Nearby green sensor blob and label kept cleanly clear of flow region
        sensor = make_sensor_cup([-0.55, -0.95, 0], angle=2.3, scale=1.2)
        sensor_lbl = T("protein", 28, SENS_COLOR).next_to(sensor, DOWN, buff=0.22)

        # Right-side computed white schematic trace (Plot)
        P = make_trace_plot(box=(2.85, 6.15, -1.7, 2.2), xr=(0, 12), yr=(0, 1.0))
        sim_t = ValueTracker(0.0)
        t_open = 4.2
        trace_fn = lambda t: 0.08 if t < t_open else 0.08 + 0.80 * (1.0 - np.exp(-(t - t_open) / 2.2))
        live_tr = P.live_curve(trace_fn, sim_t, color=TRACE_COLOR, width=6)
        dot_tr = P.dot(lambda: sim_t.get_value(), lambda: trace_fn(sim_t.get_value()), color=CA_COLOR, ring=WHITE)
        tag = scope_tag("schematic")

        self.play(
            FadeIn(ext_bg), FadeIn(cyto_bg), FadeIn(pm_top), FadeIn(pm_bot),
            FadeIn(out_lbl), FadeIn(cyto_lbl), FadeIn(out_dots),
            FadeIn(chan), FadeIn(chan_lbl), FadeIn(sensor), FadeIn(sensor_lbl),
            Create(P), FadeIn(tag),
            run_time=1.0
        )
        self.add(live_tr, dot_tr)
        self.play(sim_t.animate.set_value(2.2), run_time=2.2, rate_func=linear)

        self.at("opens a path")
        grad_arrow = Arrow([-2.55, 2.75, 0], [-2.55, 0.35, 0], color=CA_COLOR, stroke_width=5)
        self.play(GrowArrow(grad_arrow), sim_t.animate.set_value(4.1), run_time=1.9, rate_func=linear)

        self.at("gold channel doors")
        self.play(FadeOut(grad_arrow), open_t.animate.set_value(1.0), run_time=0.8)

        # Spawn streaming teal ions immediately and rise trace smoothly into the gauge beat
        flow_dots = VGroup()
        rng = np.random.default_rng(42)
        for i in range(15):
            d = make_ca_dot([-2.55 + rng.uniform(-0.20, 0.20), 1.95 + (i % 4) * 0.22, 0], radius=0.105)
            flow_dots.add(d)
        self.add(flow_dots)

        anims = []
        for i, d in enumerate(flow_dots):
            tx = rng.uniform(-5.4, -1.85)
            ty = rng.uniform(-2.25, 0.25)
            anims.append(d.animate.move_to([tx, ty, 0]))

        # Continuous rise from t=4.1 -> 9.6 across ~5.4s (bridges directly through "free calcium gauge")
        self.play(
            LaggedStart(*anims, lag_ratio=0.07),
            sim_t.animate.set_value(9.6),
            run_time=5.2,
            rate_func=linear
        )
        add_confined_drift(flow_dots, (-5.5, -1.85, -2.35, 0.35), seed=43, speed=0.45)

        self.at("a protein near")
        teal_outline = Circle(radius=0.42 * 1.2 + 0.13, stroke_color=CA_COLOR, stroke_width=5.0).move_to(sensor.get_center())
        dock_ion = make_ca_dot(sensor.get_center() + UP * 0.28 + LEFT * 0.20, radius=0.105, glow=True)
        self.play(
            Create(teal_outline), FadeIn(dock_ion),
            sim_t.animate.set_value(12.0),
            run_time=2.4, rate_func=linear
        )
        self.finish()


class S05Predict(SpokenScene):
    def construct(self):
        stage = build_predict_stage()
        self.play(FadeIn(stage), run_time=1.0)

        self.at("opening a channel")
        self.play(stage.tp.left_frame.animate.set_stroke(width=6), run_time=0.6)
        self.play(stage.tp.left_frame.animate.set_stroke(width=2.5), run_time=0.4)

        self.at("speeding a pump")
        self.play(stage.tp.right_frame.animate.set_stroke(width=6), run_time=0.6)
        self.play(stage.tp.right_frame.animate.set_stroke(width=2.5), run_time=0.4)

        self.at("follow one teal")
        probe = make_ca_dot([0.0, 0.72, 0], radius=0.16, glow=True)
        self.play(FadeIn(probe, scale=0.6), run_time=0.6)

        probe._t = 0.0

        def shuttle(m, dt):
            m._t += dt
            m.move_to([1.35 * np.sin(1.4 * m._t), 0.72 + 0.10 * np.cos(2.8 * m._t), 0])

        probe.add_updater(shuttle)

        self.at("towards cytosolic proteins")
        q = question_card("Which raises free cytosolic calcium immediately?", y=-2.85, max_w=10.2)
        self.play(FadeIn(q.question), run_time=0.9)

        self.at("which direction")
        self.finish()


class S06Pause(PredictPause):
    QUESTION = "Which raises free cytosolic calcium immediately?"
    OPTIONS = ()
    CARD = {"y": -2.85, "max_w": 10.2}
    SECONDS = 4.5

    def backdrop(self):
        stage = build_predict_stage()
        probe = make_ca_dot([0.0, 0.72, 0], radius=0.16, glow=True)
        probe._t = 0.0

        def shuttle(m, dt):
            m._t += dt
            m.move_to([1.35 * np.sin(1.4 * m._t), 0.72 + 0.10 * np.cos(2.8 * m._t), 0])

        probe.add_updater(shuttle)
        return VGroup(stage, probe)


class S07Reveal(SpokenScene):
    def construct(self):
        stage = build_predict_stage()
        lx, rx = stage.lx, stage.rx
        self.add(stage)

        # Left channel opening + computed rising white trace
        l_open = ValueTracker(0.0)
        l_chan_live = live_channel([lx, 1.05, 0], l_open, width=1.1, height=0.52)
        self.remove(stage.l_chan, stage.l_q, stage.l_base)
        self.add(l_chan_live)

        lt = ValueTracker(0.0)
        l_fn = lambda t: 0.12 + 0.76 * (1.0 - np.exp(-t / 1.4))
        l_live = stage.l_plot.live_curve(l_fn, lt, color=TRACE_COLOR, width=5)
        l_dot = stage.l_plot.dot(lambda: lt.get_value(), lambda: l_fn(lt.get_value()), color=CA_COLOR, ring=WHITE, radius=0.09)
        self.add(l_live, l_dot)

        self.at("opening the channel")
        l_flow = VGroup(*[make_ca_dot([lx + dx, 1.35, 0], radius=0.09) for dx in (-0.18, -0.06, 0.06, 0.18, -0.12, 0.12)])
        self.add(l_flow)
        self.play(l_open.animate.set_value(1.0), run_time=0.55)
        self.play(
            lt.animate.set_value(6.0),
            *[d.animate.move_to([lx + (i - 2.5) * 0.45, 0.18 - (i % 2) * 0.25, 0]) for i, d in enumerate(l_flow)],
            run_time=2.8,
            rate_func=linear
        )

        self.at("speeding the pump")
        self.remove(stage.r_q, stage.r_base)
        r_cyto = VGroup(*[make_ca_dot([rx + (i - 2) * 0.42, 0.25 - (i % 2) * 0.24, 0], radius=0.09) for i in range(5)])
        rt = ValueTracker(0.0)
        r_fn = lambda t: 0.12 + 0.72 * np.exp(-t / 1.3)
        r_live = stage.r_plot.live_curve(r_fn, rt, color=TRACE_COLOR, width=5)
        r_dot = stage.r_plot.dot(lambda: rt.get_value(), lambda: r_fn(rt.get_value()), color=CA_COLOR, ring=WHITE, radius=0.09)
        self.add(r_cyto, r_live, r_dot)
        self.play(
            rt.animate.set_value(6.0),
            *[d.animate.move_to([rx + (i - 2) * 0.45, 1.55, 0]) for i, d in enumerate(r_cyto)],
            run_time=2.5,
            rate_func=linear
        )

        self.at("two functional teams")
        on_head = T("ON", 30, CHAN_COLOR, weight=BOLD).move_to(stage.tp.left_head)
        off_head = T("OFF", 30, PUMP_COLOR, weight=BOLD).move_to(stage.tp.right_head)
        self.play(
            swap(stage.tp.left_head, on_head),
            swap(stage.tp.right_head, off_head),
            run_time=0.8
        )

        self.at("channels are on")
        on_arr = Arrow([lx, 1.48, 0], [lx, 0.35, 0], color=CHAN_COLOR, stroke_width=5)
        on_lbl = T("into cytosol", 26, CHAN_COLOR).move_to([lx + 1.55, 0.48, 0])
        self.play(GrowArrow(on_arr), FadeIn(on_lbl), run_time=0.8)

        self.at("pumps exchangers")
        self.play(FadeOut(stage.r_sens), run_time=0.35)
        pump_lbl = T("pump", 24, PUMP_COLOR).move_to([rx - 1.45, 0.42, 0])
        exch_x = rx + 1.65
        exch_up = Arrow([exch_x - 0.16, 0.65, 0], [exch_x - 0.16, 1.50, 0], color=PUMP_COLOR, stroke_width=4.5, buff=0)
        exch_dn = Arrow([exch_x + 0.16, 1.50, 0], [exch_x + 0.16, 0.65, 0], color=MEMB_COLOR, stroke_width=3.5, buff=0)
        exch_lbl = T("exchanger", 24, PUMP_COLOR).move_to([exch_x, 0.35, 0])

        buf_cup = make_buffer_cup([rx - 0.15, -0.08, 0], angle=PI / 2, scale=0.95)
        buf_ion = make_ca_dot([rx - 0.15, -0.08, 0], radius=0.085)
        buf_lbl = T("buffer", 24, BUF_COLOR).next_to(buf_cup, RIGHT, buff=0.18)

        self.play(
            stage.r_pump.animate.move_to([rx - 1.45, 1.05, 0]),
            FadeIn(pump_lbl),
            GrowArrow(exch_up), GrowArrow(exch_dn), FadeIn(exch_lbl),
            FadeIn(buf_cup), FadeIn(buf_ion), FadeIn(buf_lbl),
            run_time=1.2
        )

        self.at("describe direction")
        dir_cap = caption("ON moves Ca²⁺ into cytosol; OFF removes Ca²⁺ from free pool.", size=28)
        tag = scope_tag("schematic")
        self.play(FadeIn(dir_cap), FadeIn(tag), run_time=0.9)
        self.finish()


class S08Balance(SpokenScene):
    def construct(self):
        cell = make_cell_shell()
        out_dots = VGroup(*[make_ca_dot(p, radius=0.10) for p in seed_positions(cell.ext_box, 24, seed=81)])
        er_dots = VGroup(*[make_ca_dot(p, radius=0.10) for p in seed_positions(cell.er_box, 22, seed=82)])
        add_confined_drift(out_dots, cell.ext_box, seed=81, speed=0.40)
        add_confined_drift(er_dots, cell.er_box, seed=82, speed=0.40)

        pm_open = ValueTracker(0.0)
        er_open = ValueTracker(0.0)
        pm_chan = live_channel([cell.pm_chan_x, cell.pm_y, 0], pm_open, width=1.0, height=0.5)
        er_chan = live_channel([cell.er_chan_x, cell.er_top_y, 0], er_open, width=1.0, height=0.5)

        pump_speed = ValueTracker(1.4)
        pm_pump = make_pump([cell.pm_pump_x, cell.pm_y, 0], radius=0.31)
        er_pump = make_pump([cell.er_pump_x, cell.er_top_y, 0], radius=0.31)
        add_pump_spin(pm_pump, lambda: pump_speed.get_value())
        add_pump_spin(er_pump, lambda: pump_speed.get_value())

        bufs = VGroup(
            make_buffer_cup([-0.9, 0.72, 0], angle=PI / 2),
            make_buffer_cup([0.2, 0.72, 0], angle=PI / 2),
            make_buffer_cup([1.15, 0.72, 0], angle=PI / 2),
        )
        sensor = make_sensor_cup([0.95, -0.95, 0], angle=2.4, scale=0.9)

        P = make_trace_plot(box=(3.15, 6.2, -1.7, 2.2), xr=(0, 22), yr=(0, 1.0))
        sim_t = ValueTracker(0.0)

        def balance_fn(t):
            if t < 5.0:
                return 0.08
            if t < 9.5:
                return 0.08 + 0.80 * (1.0 - np.exp(-(t - 5.0) / 1.8))
            peak = 0.08 + 0.80 * (1.0 - np.exp(-4.5 / 1.8))
            if t < 13.0:
                return peak - 0.10 * (t - 9.5) / 3.5
            mid = peak - 0.10
            if t < 16.0:
                return mid - 0.28 * (t - 13.0) / 3.0
            low_mid = mid - 0.28
            return 0.08 + (low_mid - 0.08) * np.exp(-(t - 16.0) / 2.2)

        live_tr = P.live_curve(balance_fn, sim_t, color=TRACE_COLOR, width=6)
        dot_tr = P.dot(lambda: sim_t.get_value(), lambda: balance_fn(sim_t.get_value()), color=CA_COLOR, ring=WHITE, radius=0.085)
        tag = scope_tag("schematic")

        self.play(
            FadeIn(cell), FadeIn(out_dots), FadeIn(er_dots),
            FadeIn(pm_chan), FadeIn(er_chan), FadeIn(pm_pump), FadeIn(er_pump),
            FadeIn(bufs), FadeIn(sensor),
            Create(P), FadeIn(tag),
            run_time=0.9
        )
        self.add(live_tr, dot_tr)

        self.at("moving calcium")
        self.play(sim_t.animate.set_value(5.0), run_time=3.0, rate_func=linear)

        self.at("during a rise")
        entry_arr = Arrow([cell.pm_chan_x, cell.pm_y + 0.45, 0], [cell.pm_chan_x, cell.pm_y - 0.75, 0], color=CHAN_COLOR, stroke_width=8, buff=0)
        entry_er_arr = Arrow([cell.er_chan_x, cell.er_top_y - 0.45, 0], [cell.er_chan_x, cell.er_top_y + 0.70, 0], color=CHAN_COLOR, stroke_width=8, buff=0)
        surge = VGroup(*[make_ca_dot([cell.pm_chan_x + (i % 3 - 1) * 0.2, 1.45, 0], radius=0.095) for i in range(9)])
        self.add(surge)
        rng = np.random.default_rng(83)
        self.play(
            pm_open.animate.set_value(1.0),
            er_open.animate.set_value(1.0),
            GrowArrow(entry_arr), GrowArrow(entry_er_arr),
            *[d.animate.move_to([rng.uniform(-4.1, 1.1), rng.uniform(0.05, 1.25), 0]) for d in surge],
            sim_t.animate.set_value(9.5),
            run_time=3.2, rate_func=linear
        )

        self.at("when channels close")
        self.play(
            pm_open.animate.set_value(0.0),
            er_open.animate.set_value(0.0),
            FadeOut(entry_arr), FadeOut(entry_er_arr),
            pump_speed.animate.set_value(2.8),
            sim_t.animate.set_value(13.0),
            run_time=3.2, rate_func=linear
        )

        self.at("buffers bind")
        buf_lbl = T("buffers", 24, BUF_COLOR).next_to(bufs[1], DOWN, buff=0.18)
        self.play(
            FadeIn(buf_lbl),
            surge[0].animate.move_to(bufs[0].get_center()),
            surge[1].animate.move_to(bufs[1].get_center()),
            surge[2].animate.move_to(bufs[2].get_center()),
            sim_t.animate.set_value(16.0),
            run_time=2.6, rate_func=linear
        )

        self.at("pumps return")
        self.play(
            *[d.animate.move_to([cell.pm_pump_x + (i - 4) * 0.14, cell.pm_y + 0.55, 0]) for i, d in enumerate(surge[3:6])],
            *[d.animate.move_to([cell.er_pump_x + (i - 7) * 0.14, cell.er_top_y - 0.55, 0]) for i, d in enumerate(surge[6:])],
            sim_t.animate.set_value(19.5),
            run_time=2.6, rate_func=linear
        )

        self.at("restoring the low")
        self.play(
            FadeOut(surge[3:]),
            pump_speed.animate.set_value(1.3),
            sim_t.animate.set_value(22.0),
            run_time=2.5, rate_func=linear
        )
        self.finish()


class S09Store(SpokenScene):
    def construct(self):
        cell = make_cell_shell()
        out_dots = VGroup(*[make_ca_dot(p, radius=0.10) for p in seed_positions(cell.ext_box, 24, seed=91)])
        er_dots = VGroup(*[make_ca_dot(p, radius=0.10) for p in seed_positions(cell.er_box, 22, seed=92)])
        add_confined_drift(out_dots, cell.ext_box, seed=91, speed=0.40)
        add_confined_drift(er_dots, cell.er_box, seed=92, speed=0.40)

        pm_open = ValueTracker(0.0)
        er_open = ValueTracker(0.0)
        pm_chan = live_channel([cell.pm_chan_x, cell.pm_y, 0], pm_open, width=1.0, height=0.5)
        er_chan = live_channel([cell.er_chan_x, cell.er_top_y, 0], er_open, width=1.0, height=0.5)

        # Two green sensors placed at distinct distances from the two channels
        sens_pm = make_sensor_cup([cell.pm_chan_x + 1.45, 1.08, 0], angle=2.8, scale=0.82)
        sens_er = make_sensor_cup([cell.er_chan_x + 1.55, 0.22, 0], angle=2.5, scale=0.82)
        sens_pm_lbl = T("sensor A", 24, SENS_COLOR).next_to(sens_pm, RIGHT, buff=0.18)
        sens_er_lbl = T("sensor B", 24, SENS_COLOR).next_to(sens_er, RIGHT, buff=0.18)

        P = make_trace_plot(box=(3.15, 6.2, -1.7, 2.2), xr=(0, 20), yr=(0, 1.0))
        sim_t = ValueTracker(0.0)

        def two_pulse_fn(t):
            p1 = 0.65 * np.exp(-((t - 9.2) / 1.1) ** 2) if 7.0 <= t <= 12.2 else 0.0
            if t < 12.5:
                p2 = 0.0
            elif t < 16.5:
                p2 = 0.78 * (1.0 - np.exp(-(t - 12.5) / 1.1))
            else:
                p2 = 0.78 * np.exp(-(t - 16.5) / 1.5)
            return float(np.clip(0.08 + p1 + p2, 0.08, 0.95))

        live_tr = P.live_curve(two_pulse_fn, sim_t, color=TRACE_COLOR, width=6)
        dot_tr = P.dot(lambda: sim_t.get_value(), lambda: two_pulse_fn(sim_t.get_value()), color=CA_COLOR, ring=WHITE, radius=0.085)
        tag = scope_tag("schematic")

        # Carry cell & axes straight in without a dark fade dip
        self.add(cell, out_dots, er_dots, pm_chan, er_chan, P, tag, live_tr, dot_tr)
        self.play(FadeIn(sens_pm), FadeIn(sens_er), FadeIn(sens_pm_lbl), FadeIn(sens_er_lbl), run_time=0.6)

        self.at("outside the cell")
        pm_ring = Circle(radius=0.50, stroke_color=CHAN_COLOR, stroke_width=4).move_to(pm_chan)
        self.play(Create(pm_ring), sim_t.animate.set_value(2.0), run_time=0.9)

        self.at("inside its store")
        er_ring = Circle(radius=0.50, stroke_color=CHAN_COLOR, stroke_width=4).move_to(er_chan)
        self.play(ReplacementTransform(pm_ring, er_ring), sim_t.animate.set_value(4.0), run_time=1.0)

        self.at("same measured")
        self.play(FadeOut(er_ring), sim_t.animate.set_value(7.2), run_time=3.2, rate_func=linear)

        self.at("which channel opens")
        # Plume 1: confined strictly inside cyto_bg (radius <= 0.72)
        plume1 = Circle(radius=0.20, stroke_width=0, fill_color=CA_COLOR, fill_opacity=0.35).move_to([cell.pm_chan_x + 0.25, 1.35, 0])
        p1_dots = VGroup(*[make_ca_dot([cell.pm_chan_x + (i - 2) * 0.15, 1.55, 0], radius=0.09) for i in range(5)])
        sens_pm_act = Circle(radius=0.44, stroke_color=ACTIVE_COLOR, stroke_width=5).move_to(sens_pm)
        self.add(plume1, p1_dots)
        self.play(
            pm_open.animate.set_value(1.0),
            plume1.animate.scale(3.6).move_to([cell.pm_chan_x + 0.50, 0.95, 0]),
            *[d.animate.move_to([cell.pm_chan_x + 0.35 + (i - 2) * 0.26, 1.05 - (i % 2) * 0.22, 0]) for i, d in enumerate(p1_dots)],
            Create(sens_pm_act),
            sim_t.animate.set_value(10.5),
            run_time=2.5, rate_func=linear
        )
        self.play(
            pm_open.animate.set_value(0.0),
            FadeOut(plume1), FadeOut(p1_dots), FadeOut(sens_pm_act),
            sim_t.animate.set_value(12.3),
            run_time=1.2, rate_func=linear
        )

        self.at("how long it stays open")
        plume2 = Circle(radius=0.20, stroke_width=0, fill_color=CA_COLOR, fill_opacity=0.35).move_to([cell.er_chan_x + 0.25, 0.10, 0])
        p2_dots = VGroup(*[make_ca_dot([cell.er_chan_x + (i - 3) * 0.14, -0.45, 0], radius=0.09) for i in range(7)])
        sens_er_act = Circle(radius=0.44, stroke_color=ACTIVE_COLOR, stroke_width=5).move_to(sens_er)
        self.add(plume2, p2_dots)
        self.play(
            er_open.animate.set_value(1.0),
            plume2.animate.scale(4.6).move_to([cell.er_chan_x + 0.70, 0.35, 0]),
            *[d.animate.move_to([cell.er_chan_x + 0.45 + (i - 3) * 0.24, 0.25 + (i % 2) * 0.24, 0]) for i, d in enumerate(p2_dots)],
            Create(sens_er_act),
            sim_t.animate.set_value(16.5),
            run_time=3.5, rate_func=linear
        )

        self.at("movement creates")
        self.play(
            er_open.animate.set_value(0.0),
            plume2.animate.set_opacity(0.18),
            sim_t.animate.set_value(20.0),
            run_time=3.0, rate_func=linear
        )
        self.finish()


class S10Close(SpokenScene):
    def construct(self):
        cell = make_cell_shell()
        out_dots = VGroup(*[make_ca_dot(p, radius=0.10) for p in seed_positions(cell.ext_box, 24, seed=101)])
        er_dots = VGroup(*[make_ca_dot(p, radius=0.10) for p in seed_positions(cell.er_box, 22, seed=102)])
        add_confined_drift(out_dots, cell.ext_box, seed=101, speed=0.40)
        add_confined_drift(er_dots, cell.er_box, seed=102, speed=0.40)

        pm_open = ValueTracker(0.0)
        er_open = ValueTracker(0.0)
        pm_chan = live_channel([cell.pm_chan_x, cell.pm_y, 0], pm_open, width=1.0, height=0.5)
        er_chan = live_channel([cell.er_chan_x, cell.er_top_y, 0], er_open, width=1.0, height=0.5)

        pump_speed = ValueTracker(1.5)
        pm_pump = make_pump([cell.pm_pump_x, cell.pm_y, 0], radius=0.31)
        er_pump = make_pump([cell.er_pump_x, cell.er_top_y, 0], radius=0.31)
        add_pump_spin(pm_pump, lambda: pump_speed.get_value())
        add_pump_spin(er_pump, lambda: pump_speed.get_value())

        # Well-separated sensors clear of ER pump
        sens_pm = make_sensor_cup([cell.pm_chan_x + 1.45, 1.25, 0], angle=2.8, scale=0.80)
        sens_er = make_sensor_cup([cell.er_chan_x + 1.25, 0.35, 0], angle=2.5, scale=0.80)
        buf1 = make_buffer_cup([0.4, 0.90, 0], angle=PI / 2)

        residual_plume = Circle(radius=0.9, stroke_width=0, fill_color=CA_COLOR, fill_opacity=0.22).move_to([cell.er_chan_x + 0.7, 0.35, 0])
        leftover_ions = VGroup(*[make_ca_dot([cell.er_chan_x + 0.3 + i * 0.28, 0.35, 0], radius=0.095) for i in range(4)])

        P = make_trace_plot(box=(3.15, 6.2, -1.7, 2.2), xr=(0, 20), yr=(0, 1.0))
        sim_t = ValueTracker(0.0)

        def single_pulse_fn(t):
            # Initial settle 0..4, quiet resting 4..6, fast pulse 6..11, smooth recovery 11..20
            if t < 4.0:
                return 0.08 + 0.32 * np.exp(-t / 1.1)
            if t < 6.0:
                return 0.08
            if t < 11.0:
                return 0.08 + 0.80 * (1.0 - np.exp(-(t - 6.0) / 1.3))
            peak = 0.08 + 0.80 * (1.0 - np.exp(-5.0 / 1.3))
            return 0.08 + (peak - 0.08) * np.exp(-(t - 11.0) / 2.2)

        live_tr = P.live_curve(single_pulse_fn, sim_t, color=TRACE_COLOR, width=6)
        dot_tr = P.dot(lambda: sim_t.get_value(), lambda: single_pulse_fn(sim_t.get_value()), color=CA_COLOR, ring=WHITE, radius=0.085)
        tag = scope_tag("schematic")

        self.add(cell, out_dots, er_dots, pm_chan, er_chan, pm_pump, er_pump, sens_pm, sens_er, buf1, residual_plume, leftover_ions, P, tag)
        self.add(live_tr, dot_tr)
        # Collapse residual plumes into the resting distribution while settling trace
        self.play(
            residual_plume.animate.scale(0.1).set_opacity(0.0),
            *[d.animate.move_to([cell.er_pump_x + (i - 1.5) * 0.14, cell.er_top_y - 0.55, 0]) for i, d in enumerate(leftover_ions)],
            sim_t.animate.set_value(4.5),
            run_time=4.0, rate_func=linear
        )
        self.remove(residual_plume, leftover_ions)

        self.at("controlled redistribution")
        self.play(sim_t.animate.set_value(6.0), run_time=2.0, rate_func=linear)

        self.at("makes opening fast")
        pulse_ions = VGroup(*[make_ca_dot([cell.pm_chan_x + (i - 3) * 0.14, 1.55, 0], radius=0.095) for i in range(7)])
        self.add(pulse_ions)
        sens_act1 = Circle(radius=0.42, stroke_color=ACTIVE_COLOR, stroke_width=5).move_to(sens_pm)
        sens_act2 = Circle(radius=0.42, stroke_color=ACTIVE_COLOR, stroke_width=5).move_to(sens_er)
        self.play(
            pm_open.animate.set_value(1.0),
            er_open.animate.set_value(1.0),
            *[d.animate.move_to([-4.6 + i * 0.52, 0.55 + (i % 2) * 0.35, 0]) for i, d in enumerate(pulse_ions)],
            Create(sens_act1), Create(sens_act2),
            sim_t.animate.set_value(11.0),
            run_time=2.1, rate_func=linear
        )

        self.at("the off machinery")
        self.play(
            pm_open.animate.set_value(0.0),
            er_open.animate.set_value(0.0),
            pump_speed.animate.set_value(2.8),
            pulse_ions[0].animate.move_to(buf1.get_center()),
            *[d.animate.move_to([cell.pm_pump_x + (i - 2) * 0.14, cell.pm_y + 0.55, 0]) for i, d in enumerate(pulse_ions[1:4])],
            *[d.animate.move_to([cell.er_pump_x + (i - 5) * 0.14, cell.er_top_y - 0.55, 0]) for i, d in enumerate(pulse_ions[4:])],
            FadeOut(sens_act1), FadeOut(sens_act2),
            sim_t.animate.set_value(15.5),
            run_time=3.5, rate_func=linear
        )

        self.at("turn calcium movement")
        self.play(
            FadeOut(pulse_ions),
            pump_speed.animate.set_value(1.3),
            sim_t.animate.set_value(20.0),
            run_time=4.5, rate_func=linear
        )
        self.finish()


class S11End(EndCard):
    LINE = "Calcium signals begin and end by moving calcium, not changing it."