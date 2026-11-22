"""
FILM PLAN — "How a Normal Switch Sticks On" (oncogenes)

COLOUR MAP (one colour per concept for the whole film):
- C_OFF   (#58C4DD, cool slate-blue): normal OFF-state switch (c-Src, Ras-GDP, normal proto-oncogene copy)
- C_ON    (#F59E0B, amber-gold):      active ON-state switch, growth signal, GTP token, altered oncogene & active pulses
- C_BRAKE (#10B981, emerald-teal):    off-switch mechanism (tail phosphate clamp, GAP helper, tumour suppressor gene)
- C_FAULT (#FC6255, crimson):         mutation / break / blocking amino-acid pin / lost-copy X
- C_LOST  (#64748B, dashed slate):    replaced/missing tail segment or lost gene copy (shapes only, never text)
- C_CELL  (#47628F, muted steel):     schematic cell cross-section boundary and chromosome rack frame
- TEXT    (#E8EAF0) & GOLD (#D4A843): primary labels and predict question banner

CARRIED WORLD:
A schematic cell cross-section on the left-center (membrane boundary, signalling switch slot, and a
two-copy chromosome rack along the bottom) coupled by a signal channel to a live computed activity
dial and real-time activity trace on the right. Every scene transforms this same cell world or zooms
into the active switch / gene copies, before splitting into a side-by-side TwoPanel comparison in
the closing scene.

WHAT CHANGES IN EACH SPOKEN SCENE (and what it is computed from):
- s01_hook:              Virus capsule delivers an amber gene strip that aligns with the cell's own chromosome band; switch flips ON and drives computed signal pulses + activity dial + live trace up to 90%, then resets to 0%.
- s02_normal_switch:     Growth signal docks at the membrane switch, driving computed activity + live trace from 0% to 90% with rightward signal pulses; signal leaves and emerald off-switch sweeps in to drop activity back to 0%; chromosome band lights as Proto-oncogene.
- s03_jam_clamp:         Switch zooms into a schematic Src kinase whose emerald tail + P badge closes into the grip cup (0% activity on live trace); tail breaks off and turns dashed grey, jaws spring open in amber, driving continuous signal pulses + dial + live trace to 95%, and gene band turns amber Oncogene.
- s04_jam_ras:           Switch reshapes into Ras holding amber GTP (85% activity); emerald GAP docks and hydrolyses GTP to blue GDP (0% activity); fresh GTP + crimson pin block GAP (GAP bounces off), locking GTP and driving dial + live trace to 95%.
- s05_one_copy_gain:     Two Ras gene copies rise into focus; Copy 2 turns amber with a crimson pin and emits a continuous upward stream of stuck-on Ras blocks that drive activity + live trace to 95%, while normal Copy 1 blocks cannot lower it.
- s06_off_switch_predict:Both Ras copies reset to blue; two emerald off-switch (tumour suppressor) copies emit dual upward GAP streams keeping dial + live trace at 15%; Copy 1 turns dashed grey with a crimson X, halving the GAP stream, and question card appears with neutral '?' state.
- s08_two_copy_loss:     Question fades out; single working copy's GAP stream clears incoming amber pulses to blue (15% activity on live trace); second copy turns dashed grey with crimson X, GAP stream stops, Ras locks amber and dial + live trace surge to 95%.
- s09_closing:           TwoPanel compares 1 altered + 1 normal on-switch copy (left dial pinned 95% with pulsing signal stream) against off-switch loss where 1 lost copy stays low (15%) until the 2nd copy is lost and right dial surges to 95%.
"""
from bp_parts import *

# ------------------------------------------------------------------ Colour Map
C_OFF = BLUE          # #58C4DD — normal OFF-state switch / normal gene copy
C_ON = "#F59E0B"      # amber-gold — active ON switch / growth signal / GTP / oncogene
C_BRAKE = "#10B981"   # emerald-teal — off-switch / tail clamp / GAP helper / tumour suppressor
C_FAULT = RED         # #FC6255 — break / amino acid pin / lost-copy X
C_LOST = "#64748B"    # dashed grey (shapes only, never text)
C_CELL = "#47628F"    # schematic cell outline & chromosome rack

CELL_CENTER = np.array([-1.85, -0.05, 0.0])
DIAL_CENTER = np.array([4.55, 1.05, 0.0])
SWITCH_POS = np.array([-1.85, 1.05, 0.0])
RACK_POS = np.array([-1.85, -1.65, 0.0])
HEAD_POS = np.array([-1.85, 3.28, 0.0])
TAG_TOP_R = np.array([5.75, 3.25, 0.0])


# ------------------------------------------------------------------ Shared Builders
def make_cell_shell(center=CELL_CENTER, width=9.2, height=5.8):
    """Schematic cell cross-section (Ellipse avoids PANEL_CLASSES false 'outside' triggers)."""
    outer = Ellipse(width=width, height=height, color=C_CELL, stroke_width=4.5,
                    fill_color="#131B2B", fill_opacity=0.65).move_to(center)
    inner = Ellipse(width=width - 0.18, height=height - 0.18, color=C_CELL, stroke_width=1.5,
                    stroke_opacity=0.45, fill_opacity=0).move_to(center)
    outer.set_z_index(-5)
    inner.set_z_index(-5)
    return VGroup(outer, inner)


def make_activity_dial(tracker, center=DIAL_CENTER, radius=1.28, label="switch activity",
                       neutral_q=False, size=36, label_size=25):
    """Half-circle dial whose arc shifts cleanly between C_OFF (<= 0.25) and C_ON (> 0.25)."""
    c = np.array(center, dtype=float)
    track = Arc(radius=radius, start_angle=PI, angle=-PI, arc_center=c, stroke_color=GREY, stroke_width=10)
    if neutral_q:
        num = M("?", size, GOLD).move_to(c + DOWN * 0.38)
        g = VGroup(track, num)
        if label:
            g.add(T(label, label_size, TEXT).move_to(c + DOWN * (radius * 0.78)))
        return g

    def _arc():
        v = float(np.clip(tracker.get_value(), 0.001, 1.0))
        col = C_ON if v > 0.25 else C_OFF
        return Arc(radius=radius, start_angle=PI, angle=-PI * v, arc_center=c,
                   stroke_color=col, stroke_width=10)

    def _needle():
        v = float(np.clip(tracker.get_value(), 0.001, 1.0))
        ang = PI - PI * v
        return Line(c, c + 0.8 * radius * np.array([np.cos(ang), np.sin(ang), 0.0]),
                    color=TEXT, stroke_width=5)

    val = always_redraw(_arc)
    needle = always_redraw(_needle)

    def _state_label():
        v = tracker.get_value()
        if v <= 0.105:
            txt, col = "OFF", C_OFF
        elif v <= 0.25:
            txt, col = "LOW", C_OFF
        else:
            txt, col = "HIGH", C_ON
        return T(txt, size, col).move_to(c + DOWN * 0.38)

    num = always_redraw(_state_label)
    g = VGroup(track, val, needle, num)
    if label:
        g.add(T(label, label_size, TEXT).move_to(c + DOWN * (radius * 0.78)))
    return g


def make_activity_trace(tracker, total_s=10.0, center=(4.55, -1.55, 0.0), width=2.85, height=1.55,
                        masked=False, label="activity over time"):
    """Real-time scrolling oscilloscope-style activity(t) trace directly below the dial.
    Scrolls continuously across a fixed 8 s window with moving 1.5 s time-grid ticks so even
    steady 0% or 95% baselines show authentic advancing time without decorative filler."""
    cx, cy, _ = center
    x0, x1 = cx - width / 2, cx + width / 2
    y0, y1 = cy - height / 2, cy + height / 2
    frame = RoundedRectangle(corner_radius=0.1, width=width, height=height,
                             stroke_color=C_CELL, stroke_width=3.0,
                             fill_color="#111827", fill_opacity=0.85).move_to(center)
    axis_b = Line([x0 + 0.14, y0 + 0.18, 0], [x1 - 0.14, y0 + 0.18, 0], color=GREY, stroke_width=2.5)
    axis_l = Line([x0 + 0.14, y0 + 0.18, 0], [x0 + 0.14, y1 - 0.14, 0], color=GREY, stroke_width=2.5)
    lbl = T(label, 22, TEXT).next_to(frame, DOWN, buff=0.14) if label else None

    if masked:
        q_txt = M("?", 34, GOLD).move_to(center)
        g = VGroup(frame, axis_b, axis_l, q_txt)
        if lbl is not None:
            g.add(lbl)
        return g, []

    px0, px1 = x0 + 0.20, x1 - 0.20
    py0, py1 = y0 + 0.22, y1 - 0.18
    win_s = 8.0
    t_trk = ValueTracker(0.0)
    history = [(0.0, float(np.clip(tracker.get_value(), 0.0, 1.0)))]

    def _step(mob, dt):
        mob.increment_value(dt)
        t_cur = mob.get_value()
        v_cur = float(np.clip(tracker.get_value(), 0.0, 1.0))
        if t_cur - history[-1][0] >= 0.04 or abs(v_cur - history[-1][1]) >= 0.01:
            history.append((t_cur, v_cur))

    t_trk.add_updater(_step)

    def _ticks():
        t_now = t_trk.get_value()
        t_min = t_now - win_s
        g = VGroup()
        first_k = int(np.ceil(t_min / 1.5))
        last_k = int(np.floor(t_now / 1.5))
        for k in range(first_k, last_k + 1):
            tk = k * 1.5
            frac = (tk - t_min) / win_s
            x = px0 + frac * (px1 - px0)
            g.add(Line([x, py0, 0], [x, py1, 0], color=C_CELL, stroke_width=2.8, stroke_opacity=0.65))
        return g

    def _curve():
        t_now = t_trk.get_value()
        t_min = t_now - win_s
        vis = [(t, v) for t, v in history if t >= t_min - 0.2]
        if not vis:
            vis = [history[-1]]
        pts = []
        for t, v in vis:
            frac = float(np.clip((t - t_min) / win_s, 0.0, 1.0))
            pts.append(np.array([px0 + frac * (px1 - px0), py0 + v * (py1 - py0), 0.0]))
        if len(pts) < 2:
            pts = [pts[0] + LEFT * 0.02, pts[0]]
        v_now = vis[-1][1]
        col = C_ON if v_now > 0.25 else C_OFF
        m = VMobject(stroke_color=col, stroke_width=5.0, fill_opacity=0)
        m.set_points_as_corners(pts)
        return m

    def _tip():
        v = history[-1][1]
        pos = np.array([px1, py0 + v * (py1 - py0), 0.0])
        col = C_ON if v > 0.25 else C_OFF
        return Dot(pos, radius=0.09, color=col)

    grid_ticks = always_redraw(_ticks)
    live_curve = always_redraw(_curve)
    live_tip = always_redraw(_tip)
    g = VGroup(frame, grid_ticks, axis_b, axis_l, live_curve, live_tip)
    if lbl is not None:
        g.add(lbl)
    return g, [t_trk]


def make_signal_stream(p0, p1, tracker, n_dots=4, speed=0.85, radius=0.11):
    """Computed signal pulses travelling along channel p0 -> p1 whenever tracker > 0.12."""
    p0 = np.array(p0, dtype=float)
    p1 = np.array(p1, dtype=float)
    channel = DashedLine(p0, p1, color=C_CELL, stroke_width=2.5, dash_length=0.16)
    channel.set_z_index(-2)
    phase = ValueTracker(0.0)

    def _tick(mob, dt):
        v = tracker.get_value()
        if v > 0.08:
            mob.increment_value(dt * speed * (0.4 + 0.8 * v))

    phase.add_updater(_tick)

    dots = VGroup()
    for i in range(n_dots):
        offset = i / n_dots

        def _make_dot(off=offset):
            v = tracker.get_value()
            op = float(np.clip((v - 0.08) / 0.18, 0.0, 1.0))
            t = (phase.get_value() + off) % 1.0
            pos = p0 + (p1 - p0) * t
            col = C_ON if v > 0.25 else C_OFF
            return Dot(pos, radius=radius, color=col).set_opacity(op)

        dots.add(always_redraw(_make_dot))
    return VGroup(channel, dots), phase


def make_gene_bar(label_text, color=C_OFF, width=1.80, height=0.36, dashed=False, pin=False, lost_x=False):
    """A single gene copy bar on the chromosome rack (compact height avoids panel classification)."""
    if dashed:
        box = DashedVMobject(
            RoundedRectangle(corner_radius=0.1, width=width, height=height,
                             stroke_color=C_LOST, stroke_width=3.0),
            num_dashes=14
        )
    else:
        box = RoundedRectangle(corner_radius=0.1, width=width, height=height,
                               stroke_color=color, stroke_width=3.5,
                               fill_color=color, fill_opacity=0.22)
    g = VGroup(box)
    if pin:
        p = Triangle(color=C_FAULT, fill_color=C_FAULT, fill_opacity=1.0).scale(0.11).rotate(-PI / 2)
        p.move_to(box.get_top() + UP * 0.10)
        g.add(p)
    if lost_x:
        x1 = Line(box.get_center() + np.array([-0.22, -0.14, 0]),
                  box.get_center() + np.array([0.22, 0.14, 0]), color=C_FAULT, stroke_width=4.5)
        x2 = Line(box.get_center() + np.array([-0.22, 0.14, 0]),
                  box.get_center() + np.array([0.22, -0.14, 0]), color=C_FAULT, stroke_width=4.5)
        g.add(x1, x2)
    if label_text:
        lab = T(label_text, size=24, color=TEXT if dashed else color).next_to(box, DOWN, buff=0.16)
        g.add(lab)
        g.label = lab
    g.box = box
    return g


def make_switch_box(center=SWITCH_POS, color=C_OFF, open_jaws=False, label="growth switch"):
    """Schematic signalling switch block with hinged jaw geometry."""
    c = np.array(center, dtype=float)
    core = RoundedRectangle(corner_radius=0.16, width=1.85, height=1.15,
                            stroke_color=color, stroke_width=4,
                            fill_color=color, fill_opacity=0.18).move_to(c)
    ang = 0.42 if open_jaws else 0.04
    j_top = Line(c + RIGHT * 0.92 + UP * 0.12,
                 c + RIGHT * 0.92 + UP * 0.12 + np.array([0.65 * np.cos(ang), 0.65 * np.sin(ang), 0]),
                 color=color, stroke_width=6)
    j_bot = Line(c + RIGHT * 0.92 + DOWN * 0.12,
                 c + RIGHT * 0.92 + DOWN * 0.12 + np.array([0.65 * np.cos(-ang), 0.65 * np.sin(-ang), 0]),
                 color=color, stroke_width=6)
    g = VGroup(core, j_top, j_bot)
    if label:
        lab = T(label, size=26, color=color).next_to(core, UP, buff=0.18)
        g.add(lab)
        g.label = lab
    g.core, g.j_top, g.j_bot = core, j_top, j_bot
    return g


def make_rising_stream(x_lane, y0, y1, color, active_tracker, n_items=4, speed=0.52,
                       shape="circle", radius=0.17):
    """Computed vertical stream of protein/GAP tokens rising from gene copy (y0) to switch (y1)."""
    phase = ValueTracker(0.0)

    def _step(mob, dt):
        if active_tracker.get_value() > 0.1:
            mob.increment_value(dt * speed)

    phase.add_updater(_step)
    items = VGroup()
    for i in range(n_items):
        off = i / n_items

        def _make_item(o=off):
            op = float(np.clip(active_tracker.get_value(), 0.0, 1.0))
            t = (phase.get_value() + o) % 1.0
            y = y0 + (y1 - y0) * t
            fade = min(1.0, min(t / 0.15, (1.0 - t) / 0.15))
            if shape == "square":
                m = RoundedRectangle(corner_radius=0.06, width=radius * 2.5, height=radius * 1.65,
                                     stroke_color=color, stroke_width=3.0,
                                     fill_color=color, fill_opacity=0.88).move_to([x_lane, y, 0])
            else:
                m = RoundedRectangle(corner_radius=0.10, width=radius * 2.2, height=radius * 1.3,
                                     stroke_color=color, stroke_width=2.5,
                                     fill_color=color, fill_opacity=0.88).move_to([x_lane, y, 0])
            return m.set_opacity(op * fade)

        items.add(always_redraw(_make_item))
    return items, phase


# ------------------------------------------------------------------ Scenes
class S00Title(TitleCard):
    LESSON = "Oncogenes: When the Switch Sticks"
    TITLE = "How a Normal Switch Sticks On"


class S01Hook(SpokenScene):
    def construct(self):
        cell = make_cell_shell()
        act = ValueTracker(0.0)
        dl = make_activity_dial(act)
        trace, trk = make_activity_trace(act, total_s=self.narration_s)
        sw = make_switch_box(SWITCH_POS, C_OFF, open_jaws=False, label="growth switch")
        stream, phase = make_signal_stream(SWITCH_POS + RIGHT * 1.62, [3.2, 1.05, 0], act)

        rack_line = Line(RACK_POS + LEFT * 2.4, RACK_POS + RIGHT * 2.4, color=C_CELL, stroke_width=4)
        copy1 = make_gene_bar("copy 1", C_OFF, width=1.75, height=0.36).move_to(RACK_POS + LEFT * 1.15)
        copy2 = make_gene_bar("copy 2", C_OFF, width=1.75, height=0.36).move_to(RACK_POS + RIGHT * 1.15)
        rack = VGroup(rack_line, copy1, copy2)
        tag = scope_tag("schematic")

        self.add(cell, dl, trace, *trk, sw, stream, phase, rack, tag)

        # Beat 1: Chicken virus enters outside top-left membrane (cleanly clear of cell outline)
        self.at("chicken virus")
        virus_body = RoundedRectangle(corner_radius=0.28, width=1.35, height=0.72,
                                      stroke_color=C_ON, stroke_width=3.5,
                                      fill_color=C_ON, fill_opacity=0.14)
        virus_strip = RoundedRectangle(corner_radius=0.05, width=0.80, height=0.20,
                                       stroke_color=C_ON, stroke_width=2,
                                       fill_color=C_ON, fill_opacity=0.9).move_to(virus_body)
        virus_lbl = T("virus", 24, C_ON).next_to(virus_body, UP, buff=0.12)
        virus = VGroup(virus_body, virus_strip, virus_lbl).move_to([-5.65, 2.72, 0])
        self.play(FadeIn(virus, shift=RIGHT * 0.25), run_time=0.8)

        # Beat 2: Strip matches healthy bird's own gene on chromosome rack
        self.at("healthy birds")
        moving_strip = virus_strip.copy()
        match_lbl = T("cell's own gene", 26, C_ON).move_to([-1.85, -0.35, 0])
        self.add(moving_strip)
        self.play(moving_strip.animate.move_to(copy1.box.get_center() + UP * 0.58), run_time=1.0)
        self.play(FadeIn(match_lbl),
                  copy1.box.animate.set_stroke(C_ON).set_fill(C_ON, opacity=0.35), run_time=0.6)

        # Beat 3: How does a cell's own switch get stuck on?
        self.at("own switch")
        q_mark = T("?", 48, GOLD, weight=BOLD).move_to(SWITCH_POS + RIGHT * 1.50 + UP * 0.72)
        sw_on = make_switch_box(SWITCH_POS, C_ON, open_jaws=True, label="growth switch")
        self.play(FadeIn(q_mark, scale=1.2),
                  Transform(sw.core, sw_on.core),
                  Transform(sw.j_top, sw_on.j_top),
                  Transform(sw.j_bot, sw_on.j_bot),
                  sw.label.animate.set_color(C_ON),
                  act.animate.set_value(0.90),
                  run_time=1.2)

        # Beat 4: How many copies does it take?
        self.at("how many copies")
        copies_q = T("1 or 2 copies?", 28, GOLD).next_to(rack, UP, buff=0.22)
        self.play(FadeOut(match_lbl, run_time=0.25),
                  FadeOut(moving_strip, run_time=0.25))
        self.play(FadeIn(copies_q), run_time=0.5)

        # Beat 5: Watch one growth switch inside a single cell
        self.at("Let us watch")
        sw_reset = make_switch_box(SWITCH_POS, C_OFF, open_jaws=False, label="growth switch")
        self.play(FadeOut(virus), FadeOut(q_mark), FadeOut(copies_q),
                  copy1.box.animate.set_stroke(C_OFF).set_fill(C_OFF, opacity=0.22),
                  Transform(sw.core, sw_reset.core),
                  Transform(sw.j_top, sw_reset.j_top),
                  Transform(sw.j_bot, sw_reset.j_bot),
                  sw.label.animate.set_color(C_OFF),
                  act.animate.set_value(0.0),
                  run_time=1.4)
        self.finish()


class S02NormalSwitch(SpokenScene):
    def construct(self):
        cell = make_cell_shell()
        act = ValueTracker(0.0)
        dl = make_activity_dial(act)
        trace, trk = make_activity_trace(act, total_s=self.narration_s)
        sw = make_switch_box(SWITCH_POS, C_OFF, open_jaws=False, label="growth switch")
        stream, phase = make_signal_stream(SWITCH_POS + RIGHT * 1.62, [3.2, 1.05, 0], act)

        rack_line = Line(RACK_POS + LEFT * 2.4, RACK_POS + RIGHT * 2.4, color=C_CELL, stroke_width=4)
        copy1 = make_gene_bar("", C_OFF, width=1.75, height=0.36).move_to(RACK_POS + LEFT * 1.15)
        copy2 = make_gene_bar("", C_OFF, width=1.75, height=0.36).move_to(RACK_POS + RIGHT * 1.15)
        rack = VGroup(rack_line, copy1, copy2)
        tag = scope_tag("schematic")

        # Normal gene expression stream (x = -2.25, clear of left-side chips/brakes)
        expr_on = ValueTracker(1.0)
        expr_stream, expr_ph = make_rising_stream(-2.25, copy1.box.get_top()[1] + 0.14,
                                                  sw.core.get_bottom()[1] - 0.14,
                                                  C_OFF, expr_on, n_items=3, speed=0.55,
                                                  shape="square", radius=0.14)
        self.add(cell, dl, trace, *trk, sw, stream, phase, rack, expr_stream, expr_ph, expr_on, tag)

        # Beat 1: Healthy cell divides only when told to
        self.at("healthy cell")
        self.play(sw.core.animate.set_fill(C_OFF, opacity=0.32), run_time=0.6)
        self.play(sw.core.animate.set_fill(C_OFF, opacity=0.18), run_time=0.6)

        # Beat 2: on-step and off-step placed cleanly inside the cell ellipse
        self.at("uses an on")
        on_chip = boxed_label("on-step", C_ON, size=25).move_to([-4.25, 1.65, 0])
        self.play(FadeIn(on_chip, shift=RIGHT * 0.15), run_time=0.5)

        self.at("an off")
        off_chip = boxed_label("off-step", C_BRAKE, size=25).move_to([-4.25, -0.30, 0])
        self.play(FadeIn(off_chip, shift=RIGHT * 0.15), run_time=0.5)

        # Beat 3: Growth signal docks on the left of the switch, cleanly inside the cell ellipse
        self.at("growth signal flips")
        sig_dot = Dot([-3.05, 1.25, 0], radius=0.18, color=C_ON)
        sig_lbl = T("growth signal", 24, C_ON).next_to(sig_dot, LEFT, buff=0.14)
        sig = VGroup(sig_dot, sig_lbl)
        sw_on = make_switch_box(SWITCH_POS, C_ON, open_jaws=True, label="growth switch")
        self.play(FadeOut(on_chip, run_time=0.25))
        self.play(FadeIn(sig), run_time=0.35)
        self.play(sig.animate.move_to(SWITCH_POS + LEFT * 1.90), run_time=0.75)
        self.play(Transform(sw.core, sw_on.core),
                  Transform(sw.j_top, sw_on.j_top),
                  Transform(sw.j_bot, sw_on.j_bot),
                  sw.label.animate.set_color(C_ON),
                  act.animate.set_value(0.90),
                  run_time=1.0)

        # Beat 4: Signal leaves
        self.at("signal leaves")
        self.play(sig.animate.move_to([-3.85, 1.85, 0]).set_opacity(0), run_time=0.7)
        self.remove(sig)

        # Beat 5: Off-switch sweeps in and resets to C_OFF, gauge drops to 0
        self.at("off switch flips")
        brake = RoundedRectangle(corner_radius=0.14, width=0.95, height=0.46,
                                 stroke_color=C_BRAKE, stroke_width=3,
                                 fill_color=C_BRAKE, fill_opacity=0.28).move_to([-4.15, -0.45, 0])
        brake_lbl = T("off-switch", 24, C_BRAKE).next_to(brake, DOWN, buff=0.12)
        brake_grp = VGroup(brake, brake_lbl)
        sw_off = make_switch_box(SWITCH_POS, C_OFF, open_jaws=False, label="growth switch")
        self.play(FadeOut(off_chip, run_time=0.25))
        self.play(FadeIn(brake_grp), run_time=0.3)
        self.play(brake_grp.animate.move_to(SWITCH_POS + LEFT * 1.65 + DOWN * 0.45), run_time=0.6)
        self.play(Transform(sw.core, sw_off.core),
                  Transform(sw.j_top, sw_off.j_top),
                  Transform(sw.j_bot, sw_off.j_bot),
                  sw.label.animate.set_color(C_OFF),
                  act.animate.set_value(0.0),
                  run_time=0.9)
        self.play(FadeOut(brake_grp), run_time=0.4)

        # Beat 6: Normal gene of this kind -> Proto-oncogene (gene expresses normal switch protein)
        self.at("normal gene")
        gene_link = DashedLine([-2.25, copy1.box.get_top()[1] + 0.08, 0],
                               [-2.25, sw.core.get_bottom()[1] - 0.08, 0],
                               color=C_OFF, stroke_width=3, dash_length=0.14)
        self.play(Create(gene_link), run_time=0.9)

        self.at("proto")
        proto_lbl = T("Proto-oncogene", 28, C_OFF).next_to(rack, DOWN, buff=0.20)
        self.play(copy1.box.animate.set_fill(C_OFF, opacity=0.42),
                  FadeIn(proto_lbl, shift=UP * 0.1),
                  run_time=0.9)
        self.finish()


class S03JamClamp(SpokenScene):
    """Zoomed-in Src kinase clamp: tail phosphate gripped keeps jaws shut; losing tail opens jaws nonstop."""

    def construct(self):
        cell = make_cell_shell()
        act = ValueTracker(0.0)
        dl = make_activity_dial(act)
        trace, trk = make_activity_trace(act, total_s=self.narration_s)
        sw = make_switch_box(SWITCH_POS, C_OFF, open_jaws=False, label="growth switch")
        stream, phase = make_signal_stream([0.82, 1.05, 0], [3.2, 1.05, 0], act)

        rack_line = Line(RACK_POS + LEFT * 2.4, RACK_POS + RIGHT * 2.4, color=C_CELL, stroke_width=4)
        copy1 = make_gene_bar("", C_OFF, width=1.75, height=0.36).move_to(RACK_POS + LEFT * 1.15)
        copy2 = make_gene_bar("", C_OFF, width=1.75, height=0.36).move_to(RACK_POS + RIGHT * 1.15)
        rack = VGroup(rack_line, copy1, copy2)
        proto_lbl = T("Proto-oncogene", 28, C_OFF).next_to(rack, DOWN, buff=0.20)
        tag = scope_tag("schematic")

        # Carried gene-expression stream while discussing cell's own genes
        expr_on = ValueTracker(1.0)
        expr_stream, expr_ph = make_rising_stream(-2.25,
                                                  copy1.box.get_top()[1] + 0.14,
                                                  sw.core.get_bottom()[1] - 0.14,
                                                  C_OFF, expr_on, n_items=3, speed=0.55,
                                                  shape="square", radius=0.14)
        self.add(cell, dl, trace, *trk, sw, stream, phase, rack, proto_lbl,
                 expr_stream, expr_ph, expr_on, tag)

        # Beat 1: altered copies of the cell's own genes
        self.at("cancer genes")
        self.play(copy1.box.animate.set_stroke(GOLD, width=4.5), run_time=0.6)
        self.at("altered copies")
        self.play(copy1.box.animate.set_stroke(C_OFF, width=3.5), run_time=0.6)

        # Beat 2: Morph generic switch cleanly into Src kinase
        self.at("Take the")
        src_title = T("Src kinase", 32, C_OFF).move_to([-1.85, 2.38, 0])
        src_body = RoundedRectangle(corner_radius=0.22, width=2.85, height=1.55,
                                    stroke_color=C_OFF, stroke_width=4.5,
                                    fill_color=C_OFF, fill_opacity=0.16).move_to([-1.45, 1.00, 0])
        jaw_top = Polygon([-0.02, 1.48, 0], [0.78, 1.38, 0], [0.78, 1.07, 0], [-0.02, 1.07, 0],
                          stroke_color=C_OFF, stroke_width=4, fill_color=C_OFF, fill_opacity=0.22)
        jaw_bot = Polygon([-0.02, 0.52, 0], [0.78, 0.62, 0], [0.78, 0.93, 0], [-0.02, 0.93, 0],
                          stroke_color=C_OFF, stroke_width=4, fill_color=C_OFF, fill_opacity=0.22)
        grip_cup = Arc(radius=0.40, start_angle=0.25 * PI, angle=1.5 * PI,
                       arc_center=[-3.25, 1.00, 0], color=C_OFF, stroke_width=7)
        grip_neck = Line([-2.87, 1.00, 0], [-3.05, 1.00, 0], color=C_OFF, stroke_width=7)
        grip_lbl = T("grip", 24, C_OFF).next_to(grip_cup, UP, buff=0.16)

        self.play(expr_on.animate.set_value(0.0),
                  FadeOut(sw.label, sw.j_top, sw.j_bot, run_time=0.35),
                  ReplacementTransform(sw.core, src_body, run_time=0.65),
                  FadeIn(src_title, run_time=0.5),
                  FadeIn(jaw_top, jaw_bot, grip_cup, grip_neck, grip_lbl, run_time=0.6))

        # Beat 3: Normally, a phosphate sits on its tail
        self.at("phosphate sits")
        tail_hinge = np.array([-1.55, 0.22, 0.0])
        tail_open_pts = [tail_hinge, np.array([-2.6, -0.22, 0.0]), np.array([-3.7, -0.15, 0.0])]
        tail_line = VMobject(color=C_BRAKE, stroke_width=7)
        tail_line.set_points_smoothly(tail_open_pts)
        phos_dot = Dot(tail_open_pts[-1], radius=0.21, color=C_BRAKE)
        phos_txt = T("P", 22, BG, weight=BOLD).move_to(phos_dot)
        phos = VGroup(phos_dot, phos_txt)
        tail_lbl = T("tail + P", 24, C_BRAKE).next_to(tail_line, DOWN, buff=0.14)
        self.play(Create(tail_line), FadeIn(phos), FadeIn(tail_lbl), run_time=0.9)

        # Beat 4: Another part grips that phosphate, holding kinase shut
        self.at("Another part")
        tail_closed_pts = [tail_hinge, np.array([-2.8, 0.28, 0.0]), np.array([-3.25, 1.00, 0.0])]
        tail_closed = VMobject(color=C_BRAKE, stroke_width=7)
        tail_closed.set_points_smoothly(tail_closed_pts)
        self.play(FadeOut(tail_lbl, run_time=0.25),
                  Transform(tail_line, tail_closed),
                  phos.animate.move_to([-3.25, 1.00, 0.0]),
                  run_time=1.0)

        self.at("holding the kinase")
        status_shut = boxed_label("Phosphate gripped, kinase shut", C_BRAKE, size=25).move_to([-1.65, -0.68, 0])
        self.play(FadeIn(status_shut), run_time=0.5)
        # Brief mechanical clamp test: jaws stay held shut by the gripped tail
        self.play(jaw_top.animate.shift(UP * 0.04), jaw_bot.animate.shift(DOWN * 0.04), run_time=0.4)
        self.play(jaw_top.animate.shift(DOWN * 0.04), jaw_bot.animate.shift(UP * 0.04), run_time=0.4)

        # Beat 5: Replace that tail -> tail breaks & turns dashed grey; grip has nothing to hold
        self.at("Replace that tail")
        break_mark = VGroup(
            Line([-2.25, -0.02, 0], [-1.95, 0.36, 0], color=C_FAULT, stroke_width=5),
            Line([-2.25, 0.36, 0], [-1.95, -0.02, 0], color=C_FAULT, stroke_width=5),
        )
        stub = DashedLine(tail_hinge, [-2.55, -0.10, 0], color=C_LOST, stroke_width=5, dash_length=0.12)
        self.play(FadeIn(break_mark), run_time=0.3)
        self.play(FadeOut(tail_line), FadeOut(phos), FadeIn(stub), run_time=0.8)

        self.at("nothing to hold")
        grip_open = Arc(radius=0.43, start_angle=0.35 * PI, angle=1.3 * PI,
                        arc_center=[-3.25, 1.00, 0], color=C_FAULT, stroke_width=7)
        status_open = boxed_label("Tail replaced: nothing to hold", C_FAULT, size=25).move_to([-1.65, -0.68, 0])
        self.play(Transform(grip_cup, grip_open),
                  grip_neck.animate.set_color(C_FAULT),
                  grip_lbl.animate.set_color(C_FAULT),
                  swap(status_shut, status_open, run_time=0.6),
                  run_time=0.9)

        # Beat 6: Kinase jaws spring open in amber, driving gauge high; band relabels Oncogene
        self.at("kinase runs all")
        jaw_top_open = jaw_top.copy().rotate(0.32, about_point=[-0.02, 1.48, 0]).set_stroke(C_ON).set_fill(C_ON, opacity=0.35)
        jaw_bot_open = jaw_bot.copy().rotate(-0.32, about_point=[-0.02, 0.52, 0]).set_stroke(C_ON).set_fill(C_ON, opacity=0.35)
        self.play(src_title.animate.set_color(C_ON),
                  src_body.animate.set_stroke(C_ON).set_fill(C_ON, opacity=0.25),
                  Transform(jaw_top, jaw_top_open),
                  Transform(jaw_bot, jaw_bot_open),
                  act.animate.set_value(0.95),
                  run_time=1.0)

        self.at("is an oncogene")
        onco_lbl = T("Oncogene", 28, C_ON).next_to(rack, DOWN, buff=0.20)
        self.play(copy1.box.animate.set_stroke(C_ON).set_fill(C_ON, opacity=0.42),
                  swap(proto_lbl, onco_lbl, run_time=0.6),
                  run_time=0.9)
        self.finish()


class S04JamRas(SpokenScene):
    """Ras GTPase switch: GAP helper turns Ras-GTP off to GDP; 1 changed amino acid blocks GAP."""

    def construct(self):
        cell = make_cell_shell()
        act = ValueTracker(0.0)
        dl = make_activity_dial(act)
        trace, trk = make_activity_trace(act, total_s=self.narration_s)
        stream, phase = make_signal_stream([-0.15, 0.85, 0], [3.2, 1.05, 0], act)

        rack_line = Line(RACK_POS + LEFT * 2.4, RACK_POS + RIGHT * 2.4, color=C_CELL, stroke_width=4)
        copy1 = make_gene_bar("", C_OFF, width=1.75, height=0.36).move_to(RACK_POS + LEFT * 1.15)
        copy2 = make_gene_bar("", C_OFF, width=1.75, height=0.36).move_to(RACK_POS + RIGHT * 1.15)
        rack = VGroup(rack_line, copy1, copy2)
        tag = scope_tag("schematic")

        # Ras schematic body (top edge at y = 0.72 + 0.85 = 1.57); GTP box sits cleanly ABOVE it
        ras_center = np.array([-1.55, 0.72, 0.0])
        ras_body = RoundedRectangle(corner_radius=0.32, width=2.8, height=1.70,
                                    stroke_color=C_OFF, stroke_width=4.5,
                                    fill_color=C_OFF, fill_opacity=0.18).move_to(ras_center)
        ras_title = T("Ras", 32, C_OFF).move_to([-1.55, 2.50, 0])
        dock_notch = Arc(radius=0.32, start_angle=-PI / 2, angle=PI,
                         arc_center=ras_center + LEFT * 1.4, color=C_OFF, stroke_width=4)

        self.add(cell, dl, trace, *trk, stream, phase, rack, ras_body, ras_title, dock_notch, tag)

        # Beat 1: A second switch jams differently; Ras is on while it holds GTP
        self.at("second switch")
        self.play(ras_body.animate.set_stroke(C_OFF, width=5), run_time=0.5)

        self.at("while it holds")
        gtp_pos = ras_center + UP * 1.19  # bottom of 0.56 box is at +0.91, cleanly above ras_body top (+0.85)
        gtp_box = RoundedRectangle(corner_radius=0.14, width=1.25, height=0.56,
                                   stroke_color=C_ON, stroke_width=3,
                                   fill_color=C_ON, fill_opacity=0.92).move_to(gtp_pos)
        gtp_txt = T("GTP", 25, BG, weight=BOLD).move_to(gtp_box)
        gtp = VGroup(gtp_box, gtp_txt)
        self.play(FadeIn(gtp, shift=DOWN * 0.15),
                  ras_body.animate.set_stroke(C_ON).set_fill(C_ON, opacity=0.26),
                  ras_title.animate.set_color(C_ON),
                  dock_notch.animate.set_color(C_ON),
                  act.animate.set_value(0.85),
                  run_time=0.9)

        # Beat 2: Turns itself off by breaking GTP down
        self.at("turns itself off")
        gtp_note = T("GTP → GDP", 26, TEXT).move_to([-1.55, -0.58, 0])
        self.play(FadeIn(gtp_note), run_time=0.6)

        # Beat 3: Helper protein called a GAP triggers the breakdown
        self.at("helper protein")
        gap_body = RoundedRectangle(corner_radius=0.2, width=1.45, height=1.02,
                                    stroke_color=C_BRAKE, stroke_width=4,
                                    fill_color=C_BRAKE, fill_opacity=0.24).move_to([-4.65, 0.72, 0])
        gap_finger = Triangle(color=C_BRAKE, fill_color=C_BRAKE, fill_opacity=0.85).scale(0.2).rotate(-PI / 2)
        gap_finger.next_to(gap_body, RIGHT, buff=-0.02)
        gap_lbl = T("GAP", 26, C_BRAKE, weight=BOLD).move_to(gap_body)
        gap = VGroup(gap_body, gap_finger, gap_lbl)
        self.play(FadeIn(gap, shift=RIGHT * 0.3), run_time=0.7)

        self.at("triggers the breakdown")
        gdp_box = RoundedRectangle(corner_radius=0.14, width=1.25, height=0.56,
                                   stroke_color=C_OFF, stroke_width=3,
                                   fill_color=C_OFF, fill_opacity=0.88).move_to(gtp_pos)
        gdp_txt = T("GDP", 25, BG, weight=BOLD).move_to(gdp_box)
        gdp = VGroup(gdp_box, gdp_txt)
        p_off = Dot(gtp_pos + RIGHT * 0.9, radius=0.14, color=C_ON)

        self.play(gap.animate.move_to(ras_center + LEFT * 2.18), run_time=0.6)
        self.play(FadeOut(gtp, run_time=0.25),
                  FadeIn(gdp, run_time=0.35),
                  FadeIn(p_off),
                  ras_body.animate.set_stroke(C_OFF).set_fill(C_OFF, opacity=0.18),
                  ras_title.animate.set_color(C_OFF),
                  dock_notch.animate.set_color(C_OFF),
                  act.animate.set_value(0.0),
                  run_time=0.9)
        self.play(p_off.animate.shift(UR * 0.45).set_opacity(0),
                  gap.animate.move_to([-4.75, 0.72, 0]),
                  FadeOut(gtp_note),
                  run_time=0.6)
        self.remove(p_off)

        # Beat 4: One changed amino acid gets in the helper's way (fresh GTP loads)
        fresh_gtp_box = RoundedRectangle(corner_radius=0.14, width=1.25, height=0.56,
                                         stroke_color=C_ON, stroke_width=3,
                                         fill_color=C_ON, fill_opacity=0.92).move_to(gtp_pos)
        fresh_gtp_txt = T("GTP", 25, BG, weight=BOLD).move_to(fresh_gtp_box)
        fresh_gtp = VGroup(fresh_gtp_box, fresh_gtp_txt)

        self.at("changed amino acid")
        pin = Triangle(color=C_FAULT, fill_color=C_FAULT, fill_opacity=1.0).scale(0.18).rotate(PI / 2)
        pin.move_to(ras_center + LEFT * 1.48)
        pin_lbl = T("1 changed amino acid", 25, C_FAULT).move_to([-1.85, -0.58, 0])
        self.play(FadeOut(gdp, run_time=0.25),
                  FadeIn(fresh_gtp, run_time=0.35),
                  ras_body.animate.set_stroke(C_ON).set_fill(C_ON, opacity=0.26),
                  ras_title.animate.set_color(C_ON),
                  dock_notch.animate.set_color(C_FAULT),
                  FadeIn(pin, scale=1.3),
                  FadeIn(pin_lbl),
                  act.animate.set_value(0.85),
                  run_time=0.8)

        # Beat 5: GAP bounces off the pin
        self.at("in the helper's way")
        self.play(gap.animate.move_to(ras_center + LEFT * 2.55), run_time=0.45)
        self.play(gap.animate.move_to([-4.75, 0.72, 0]), run_time=0.55)

        # Beat 6: Breaks GTP down only slowly, even with a GAP, so it stays on
        self.at("only slowly")
        blocked_lbl = T("GAP blocked — GTP stays locked", 26, C_ON).move_to([-1.65, -0.58, 0])
        self.play(gap.animate.move_to(ras_center + LEFT * 2.55), run_time=0.35)
        self.play(gap.animate.move_to([-4.75, 0.72, 0]),
                  swap(pin_lbl, blocked_lbl, run_time=0.6),
                  run_time=0.7)

        self.at("stays on")
        self.play(act.animate.set_value(0.95),
                  copy2.box.animate.set_stroke(C_ON).set_fill(C_ON, opacity=0.35),
                  run_time=0.9)
        self.finish()


class S05OneCopyGain(SpokenScene):
    """Two parallel Ras gene copies: altering 1 copy drives nonstop signal despite normal Copy 1."""

    def construct(self):
        cell = make_cell_shell(center=[-1.85, -0.15, 0.0], height=5.4)
        act = ValueTracker(0.10)
        dl = make_activity_dial(act)
        trace, trk = make_activity_trace(act, total_s=self.narration_s)
        tag = scope_tag("schematic")

        # Two dedicated emission lanes well inside the cell ellipse
        x1, x2 = -3.45, -0.30
        y_gene, y_slot = -1.25, 0.90
        rack_line = Line([x1 - 1.1, y_gene, 0], [x2 + 1.1, y_gene, 0], color=C_CELL, stroke_width=4)
        c1_bar = make_gene_bar("Copy 1", C_OFF, width=1.8, height=0.36).move_to([x1, y_gene, 0])
        c2_bar = make_gene_bar("Copy 2", C_OFF, width=1.8, height=0.36).move_to([x2, y_gene, 0])

        # Protein slots widened to 2.35 so "Ras (stuck on)" fits with generous padding
        p1_slot = RoundedRectangle(corner_radius=0.16, width=2.25, height=0.85,
                                   stroke_color=C_OFF, stroke_width=3.5,
                                   fill_color=C_OFF, fill_opacity=0.18).move_to([x1, y_slot, 0])
        p1_txt = T("Ras (off)", 24, C_OFF).move_to(p1_slot)
        p2_slot = RoundedRectangle(corner_radius=0.16, width=2.35, height=0.85,
                                   stroke_color=C_OFF, stroke_width=3.5,
                                   fill_color=C_OFF, fill_opacity=0.18).move_to([x2, y_slot, 0])
        p2_txt = T("Ras (off)", 24, C_OFF).move_to(p2_slot)

        stream, phase = make_signal_stream(p2_slot.get_right() + RIGHT * 0.08, [3.2, 1.05, 0], act)

        c1_on = ValueTracker(1.0)
        c2_norm_on = ValueTracker(1.0)
        c2_mut_on = ValueTracker(0.0)
        s1, ph1 = make_rising_stream(x1, c1_bar.box.get_top()[1] + 0.14, y_slot - 0.50, C_OFF, c1_on, shape="square", radius=0.12)
        s2_norm, ph2n = make_rising_stream(x2, c2_bar.box.get_top()[1] + 0.14, y_slot - 0.50, C_OFF, c2_norm_on, shape="square", radius=0.12)
        s2_mut, ph2m = make_rising_stream(x2, c2_bar.box.get_top()[1] + 0.28, y_slot - 0.50, C_ON, c2_mut_on, shape="square", radius=0.12)

        self.add(cell, dl, trace, *trk, rack_line, c1_bar, c2_bar, p1_slot, p1_txt, p2_slot, p2_txt,
                 stream, phase, s1, ph1, s2_norm, ph2n, s2_mut, ph2m,
                 c1_on, c2_norm_on, c2_mut_on, tag)

        # Beat 1: Heading cleanly ABOVE cell ellipse (y = 3.22)
        self.at("count the gene")
        hdr = T("2 gene copies of Ras", 30, TEXT).move_to(HEAD_POS)
        self.play(FadeIn(hdr), run_time=0.6)

        self.at("one from each")
        par1 = T("parent 1", 24, C_OFF).next_to(c1_bar, DOWN, buff=0.12)
        par2 = T("parent 2", 24, C_OFF).next_to(c2_bar, DOWN, buff=0.12)
        self.play(FadeIn(par1), FadeIn(par2), run_time=0.7)

        # Beat 2: Alter one copy of Ras -> signals nonstop
        self.at("Alter one copy")
        pin = Triangle(color=C_FAULT, fill_color=C_FAULT, fill_opacity=1.0).scale(0.12).rotate(-PI / 2)
        pin.move_to(c2_bar.box.get_top() + UP * 0.10)
        p2_new = T("Ras (stuck on)", 24, C_ON).move_to(p2_slot)

        self.play(c2_bar.box.animate.set_stroke(C_ON).set_fill(C_ON, opacity=0.35),
                  c2_bar.label.animate.set_color(C_ON),
                  FadeIn(pin, scale=1.3),
                  c2_norm_on.animate.set_value(0.0),
                  c2_mut_on.animate.set_value(1.0),
                  run_time=0.7)

        self.at("protein signals")
        self.play(p2_slot.animate.set_stroke(C_ON).set_fill(C_ON, opacity=0.25),
                  swap(p2_txt, p2_new, run_time=0.45),
                  act.animate.set_value(0.95),
                  run_time=0.9)

        # Beat 3: Normal protein from other copy cannot turn it off
        self.at("normal protein from")
        self.play(p1_slot.animate.set_stroke(C_OFF, width=5), run_time=0.4)
        self.at("cannot turn it off")
        cannot_lbl = T("normal copy cannot turn it off", 25, C_OFF).move_to([-1.85, 1.75, 0])
        probe = RoundedRectangle(corner_radius=0.06, width=0.32, height=0.22,
                                 stroke_color=C_OFF, stroke_width=3,
                                 fill_color=C_OFF, fill_opacity=0.90).move_to(
            p1_slot.get_right() + RIGHT * 0.22)
        self.play(FadeIn(probe, scale=0.85), FadeIn(cannot_lbl), run_time=0.45)
        self.play(probe.animate.move_to(p2_slot.get_left() + LEFT * 0.20),
                  p2_slot.animate.set_stroke(C_ON, width=5.5),
                  run_time=0.45)
        self.play(probe.animate.move_to(p1_slot.get_right() + RIGHT * 0.22).set_opacity(0),
                  p2_slot.animate.set_stroke(C_ON, width=3.5),
                  p1_slot.animate.set_stroke(C_OFF, width=3.5),
                  run_time=0.55)
        self.remove(probe)

        # Beat 4: Dominant gain of function cleanly ABOVE cell ellipse
        self.at("dominant gain")
        dom_chip = boxed_label("1 altered copy → Dominant gain", C_ON, size=27).move_to(HEAD_POS)
        self.play(FadeOut(hdr, run_time=0.25))
        self.play(FadeIn(dom_chip), run_time=0.55)
        self.finish()


# ------------------------------------------------------------------ Shared S06 / S07 / S08 World Builder
def build_offswitch_world(lost_copies=0, neutral_q=False, activity=0.15, total_s=20.0, show_ts_lbl=True):
    """Carried world for s06, s07 (PredictPause), and s08:
    Cell ellipse sits at center y=0.05, height=5.2 (top=+2.65, bottom=-2.55) so headings at y=3.28
    and question_card at y=-3.05 sit cleanly outside, while all gene bars + labels sit cleanly inside!
    """
    cell = make_cell_shell(center=[-1.75, 0.0, 0.0], width=9.8, height=5.3)
    act = ValueTracker(activity)
    dl = make_activity_dial(act, center=[4.55, 1.25, 0.0], radius=1.25, neutral_q=neutral_q)
    trace, trk = make_activity_trace(act, total_s=total_s, center=(4.55, -1.18, 0.0),
                                     width=2.85, height=1.35, masked=neutral_q)

    y_gene, y_sw = -0.70, 1.35
    x_ras, x_g1, x_g2 = -3.65, -1.55, 0.45

    rack_line = Line([-4.75, y_gene, 0], [1.45, y_gene, 0], color=C_CELL, stroke_width=4)
    ras_bar = make_gene_bar("2 normal Ras", C_OFF, width=1.65, height=0.35).move_to([x_ras, y_gene, 0])
    g1_bar = make_gene_bar("Off-switch 1", C_BRAKE, width=1.55, height=0.35,
                           dashed=(lost_copies >= 1), lost_x=(lost_copies >= 1)).move_to([x_g1, y_gene, 0])
    g2_bar = make_gene_bar("Off-switch 2", C_BRAKE, width=1.55, height=0.35,
                           dashed=(lost_copies >= 2), lost_x=(lost_copies >= 2)).move_to([x_g2, y_gene, 0])

    ts_lbl = T("Off-switch (tumour suppressor)", 24, C_BRAKE).move_to([-0.55, -1.52, 0])

    sw_box_col = GREY if neutral_q else (C_ON if activity > 0.25 else C_OFF)
    sw_lbl_col = TEXT if neutral_q else sw_box_col
    sw_txt = "Ras (?)" if neutral_q else ("Ras (stuck on)" if activity > 0.25 else "Ras (controlled)")
    sw_box = RoundedRectangle(corner_radius=0.18, width=4.95, height=0.92,
                              stroke_color=sw_box_col, stroke_width=4,
                              fill_color=sw_box_col, fill_opacity=0.2).move_to([-1.60, y_sw, 0])
    sw_lbl = T(sw_txt, 25, sw_lbl_col).move_to(sw_box)

    g1_on = ValueTracker(0.0 if lost_copies >= 1 else 1.0)
    g2_on = ValueTracker(0.0 if lost_copies >= 2 else 1.0)
    stream_g1, ph_g1 = make_rising_stream(x_g1, y_gene + 0.24, y_sw - 0.54, C_BRAKE, g1_on, shape="circle", radius=0.16)
    stream_g2, ph_g2 = make_rising_stream(x_g2, y_gene + 0.24, y_sw - 0.54, C_BRAKE, g2_on, shape="circle", radius=0.16)

    # Normal Ras protein stream rising from the 2 normal Ras copies on the left
    ras_on = ValueTracker(1.0)
    stream_ras, ph_ras = make_rising_stream(x_ras, y_gene + 0.24, y_sw - 0.54, C_OFF, ras_on, shape="square", radius=0.15)

    sig_act = ValueTracker(0.0 if neutral_q else activity)
    sig_stream, sig_ph = make_signal_stream(sw_box.get_right() + RIGHT * 0.08, [3.2, 1.25, 0], sig_act, radius=0.13)

    tag = scope_tag("schematic").move_to(TAG_TOP_R)

    world_items = [cell, dl, trace, rack_line, ras_bar, g1_bar, g2_bar,
                   sw_box, sw_lbl, stream_ras, stream_g1, stream_g2, sig_stream, tag]
    if show_ts_lbl:
        world_items.append(ts_lbl)
    world = VGroup(*world_items)
    return {
        "world": world, "act": act, "sig_act": sig_act, "dl": dl, "trace": trace,
        "g1_bar": g1_bar, "g2_bar": g2_bar, "g1_on": g1_on, "g2_on": g2_on,
        "sw_box": sw_box, "sw_lbl": sw_lbl, "ts_lbl": ts_lbl,
        "trackers": [ph_g1, ph_g2, ph_ras, sig_ph, g1_on, g2_on, ras_on, act, sig_act, *trk],
    }


def lose_copy_anim(bar, on_tracker):
    """Replace a working gene bar with a dashed grey lost bar + crimson X without morphing Text."""
    lost = make_gene_bar("", C_BRAKE, width=1.55, height=0.35, dashed=True, lost_x=True)
    lost.move_to(bar.box.get_center())
    return AnimationGroup(
        FadeOut(bar.box, run_time=0.25),
        FadeIn(lost, run_time=0.35),
        bar.label.animate.set_color(TEXT),
        on_tracker.animate.set_value(0.0),
    )


class S06OffSwitchPredict(SpokenScene):
    def construct(self):
        w = build_offswitch_world(lost_copies=0, neutral_q=False, activity=0.15,
                                  total_s=self.narration_s, show_ts_lbl=False)
        self.add(w["world"], *w["trackers"])

        # Beat 1: Second route
        self.at("second route")
        hdr = T("Route 2: remove the GAP off-switch", 28, C_BRAKE).move_to(HEAD_POS)
        self.play(FadeIn(hdr), run_time=0.6)

        self.at("Instead of jamming")
        self.play(w["g1_bar"].box.animate.set_fill(C_BRAKE, opacity=0.38),
                  w["g2_bar"].box.animate.set_fill(C_BRAKE, opacity=0.38),
                  run_time=0.6)

        # Beat 2: Remove its off-switch (GAP helper)
        self.at("remove its off")
        self.play(w["sw_box"].animate.set_stroke(C_OFF, width=5), run_time=0.45)
        self.play(w["sw_box"].animate.set_stroke(C_OFF, width=4), run_time=0.45)

        # Beat 3: Tumour suppressor
        self.at("tumor suppressor")
        self.play(FadeIn(w["ts_lbl"], shift=UP * 0.1), run_time=0.6)

        # Beat 4: Cell loses one of its two off-switch copies -> reset result to neutral '?'
        self.at("loses one of")
        dl_q = make_activity_dial(w["act"], center=[4.55, 1.25, 0.0], radius=1.25, neutral_q=True)
        trace_q, _ = make_activity_trace(w["act"], center=(4.55, -1.18, 0.0), width=2.85, height=1.35, masked=True)
        sw_q_lbl = T("Ras (?)", 25, TEXT).move_to(w["sw_box"])
        self.play(FadeOut(hdr, run_time=0.3),
                  lose_copy_anim(w["g1_bar"], w["g1_on"]),
                  w["sig_act"].animate.set_value(0.0),
                  w["sw_box"].animate.set_stroke(GREY).set_fill(GREY, opacity=0.20),
                  swap(w["sw_lbl"], sw_q_lbl, run_time=0.4),
                  FadeOut(w["dl"], run_time=0.25),
                  FadeOut(w["trace"], run_time=0.25),
                  run_time=0.7)
        self.play(FadeIn(dl_q), FadeIn(trace_q), run_time=0.35)

        # Beat 5: Question banner in bottom band (matches S07Pause)
        self.at("Does the switch")
        q = question_card("One off-switch copy lost: does the switch stick on?",
                          y=BOTTOM_Y + 0.05, left=-6.1, max_w=10.0)
        self.play(FadeIn(q.question), run_time=0.6)
        self.finish()


class S07Pause(PredictPause):
    QUESTION = "One off-switch copy lost: does the switch stick on?"
    CARD = {"y": BOTTOM_Y + 0.05, "left": -6.1, "max_w": 10.0}
    SECONDS = 4.5

    def backdrop(self):
        w = build_offswitch_world(lost_copies=1, neutral_q=True, activity=0.15)
        return Group(w["world"], *w["trackers"])


class S08TwoCopyLoss(SpokenScene):
    def construct(self):
        w = build_offswitch_world(lost_copies=1, neutral_q=True, activity=0.15, total_s=self.narration_s)
        q = question_card("One off-switch copy lost: does the switch stick on?",
                          y=BOTTOM_Y + 0.05, left=-6.1, max_w=10.0)
        self.add(w["world"], *w["trackers"], q)

        # Beat 1: Usually, no — one working copy still clears the signal
        self.at("Usually no")
        hdr = T("Usually no: 1 working copy clears signal", 28, C_BRAKE).move_to(HEAD_POS)
        dl_live = make_activity_dial(w["act"], center=[4.55, 1.25, 0.0], radius=1.25, neutral_q=False)
        trace_live, trk_live = make_activity_trace(w["act"], total_s=self.narration_s,
                                                   center=(4.55, -1.18, 0.0), width=2.85, height=1.35, masked=False)
        sw_ctrl = T("Ras (controlled)", 25, C_OFF).move_to(w["sw_box"])
        self.play(FadeOut(q), FadeOut(w["dl"]), FadeOut(w["trace"]), run_time=0.35)
        self.add(*trk_live)
        self.play(FadeIn(dl_live), FadeIn(trace_live), FadeIn(hdr),
                  w["sig_act"].animate.set_value(0.15),
                  w["sw_box"].animate.set_stroke(C_OFF).set_fill(C_OFF, opacity=0.20),
                  swap(w["sw_lbl"], sw_ctrl, run_time=0.4),
                  run_time=0.7)
        w["dl"] = dl_live
        w["trace"] = trace_live
        w["sw_lbl"] = sw_ctrl

        # Beat 2: Clears signal -> stays mostly off -> hidden at cell level
        self.at("clear the signal")
        self.play(w["act"].animate.set_value(0.12), w["sig_act"].animate.set_value(0.12), run_time=0.6)

        self.at("stays mostly off")
        self.play(w["sw_box"].animate.set_fill(C_OFF, opacity=0.30), run_time=0.45)
        self.play(w["sw_box"].animate.set_fill(C_OFF, opacity=0.20), run_time=0.45)

        self.at("hidden at the")
        hidden_lbl = T("1 copy lost → hidden at cell level", 28, C_BRAKE).move_to(HEAD_POS)
        self.play(swap(hdr, hidden_lbl, run_time=0.5), run_time=0.6)

        # Beat 3: Only when the cell loses the second copy does the off-step fail completely
        self.at("loses the second")
        fail_lbl = T("2nd copy lost → off-step fails", 28, C_ON).move_to(HEAD_POS)
        self.play(lose_copy_anim(w["g2_bar"], w["g2_on"]),
                  swap(hidden_lbl, fail_lbl, run_time=0.5),
                  run_time=0.7)

        self.at("fail completely")
        sw_on_lbl = T("Ras (stuck on)", 25, C_ON).move_to(w["sw_box"])
        self.play(w["sw_box"].animate.set_stroke(C_ON).set_fill(C_ON, opacity=0.28),
                  swap(w["sw_lbl"], sw_on_lbl, run_time=0.45),
                  w["act"].animate.set_value(0.95),
                  w["sig_act"].animate.set_value(0.95),
                  run_time=1.0)

        # Beat 4: Recessive loss of function
        self.at("recessive loss")
        rec_chip = boxed_label("Both copies lost → Recessive loss", C_FAULT, size=27).move_to(HEAD_POS)
        self.play(swap(fail_lbl, rec_chip, run_time=0.55), run_time=0.7)
        self.finish()


class S09Closing(SpokenScene):
    """Side-by-side comparison using TwoPanel: 1 altered on-switch copy vs 2 lost off-switch copies."""

    def construct(self):
        tp = TwoPanel("On-step: 1 altered copy", "Off-step: usually both lost",
                      colors=(C_ON, C_BRAKE), top=3.15, bottom=-2.15, gap=0.4, width=12.6, size=30)
        tag = scope_tag("schematic")
        self.add(tp, tag)

        # Left panel: start with 2 normal OFF copies, alter l_g2 on cue to eliminate freeze
        l_act = ValueTracker(0.0)
        l_c, _, _ = tp.area("left")
        l_dial = make_activity_dial(l_act, center=l_c + RIGHT * 1.55 + UP * 1.05, radius=0.98,
                                    label="activity", size=28, label_size=24)
        l_sw = RoundedRectangle(corner_radius=0.14, width=2.25, height=0.82,
                                stroke_color=C_OFF, stroke_width=4,
                                fill_color=C_OFF, fill_opacity=0.20).move_to(l_c + LEFT * 1.35 + UP * 1.05)
        l_sw_txt = T("both OFF", 24, C_OFF).move_to(l_sw)
        l_stream, l_ph = make_signal_stream(l_sw.get_right() + RIGHT * 0.08,
                                            l_c + RIGHT * 0.50 + UP * 1.05, l_act, n_dots=2, radius=0.09)
        l_g1 = make_gene_bar("normal", C_OFF, width=1.25, height=0.32).move_to(l_c + LEFT * 2.10 + DOWN * 0.90)
        l_g2 = make_gene_bar("normal", C_OFF, width=1.25, height=0.32).move_to(l_c + LEFT * 0.60 + DOWN * 0.90)
        l_n_on = ValueTracker(1.0)
        l_g2_norm_on = ValueTracker(1.0)
        l_a_on = ValueTracker(0.0)
        l_s1, l_ph1 = make_rising_stream(l_g1.box.get_center()[0], l_g1.box.get_top()[1] + 0.14,
                                         l_sw.get_bottom()[1] - 0.14, C_OFF, l_n_on, n_items=3, speed=0.70,
                                         shape="square", radius=0.14)
        l_s2n, l_ph2n = make_rising_stream(l_g2.box.get_center()[0], l_g2.box.get_top()[1] + 0.14,
                                           l_sw.get_bottom()[1] - 0.14, C_OFF, l_g2_norm_on, n_items=3, speed=0.70,
                                           shape="square", radius=0.14)
        l_s2, l_ph2 = make_rising_stream(l_g2.box.get_center()[0], l_g2.box.get_top()[1] + 0.28,
                                         l_sw.get_bottom()[1] - 0.14, C_ON, l_a_on, n_items=3, speed=0.70,
                                         shape="square", radius=0.14)
        l_trace, l_t_trk = make_activity_trace(l_act, total_s=10.0, center=l_c + RIGHT * 1.55 + DOWN * 0.85,
                                               width=2.15, height=1.10, label=None)
        l_note = T("2 normal copies", 26, C_OFF).move_to(l_c + DOWN * 1.82)
        left_all = VGroup(l_dial, l_trace, l_sw, l_sw_txt, l_stream, l_s1, l_s2n, l_s2, l_g1, l_g2, l_note)

        # Right panel: mirror same clean separation (gene bars on left under r_sw, dial + trace on right)
        r_act = ValueTracker(0.15)
        r_c, _, _ = tp.area("right")
        r_dial = make_activity_dial(r_act, center=r_c + RIGHT * 1.55 + UP * 1.05, radius=0.98,
                                    label="activity", size=28, label_size=24)
        r_sw = RoundedRectangle(corner_radius=0.14, width=2.25, height=0.82,
                                stroke_color=C_OFF, stroke_width=4,
                                fill_color=C_OFF, fill_opacity=0.20).move_to(r_c + LEFT * 1.35 + UP * 1.05)
        r_sw_txt = T("still OFF", 24, C_OFF).move_to(r_sw)
        r_stream, r_ph = make_signal_stream(r_sw.get_right() + RIGHT * 0.08,
                                            r_c + RIGHT * 0.50 + UP * 1.05, r_act, n_dots=2, radius=0.09)
        r_g1 = make_gene_bar("lost", C_BRAKE, width=1.25, height=0.32,
                             dashed=True, lost_x=True).move_to(r_c + LEFT * 2.10 + DOWN * 0.90)
        r_g2 = make_gene_bar("working", C_BRAKE, width=1.25, height=0.32).move_to(r_c + LEFT * 0.60 + DOWN * 0.90)
        r_g2_on = ValueTracker(1.0)
        r_s2, r_ph2 = make_rising_stream(r_g2.get_center()[0], r_g2.get_top()[1] + 0.14,
                                         r_sw.get_bottom()[1] - 0.14, C_BRAKE, r_g2_on, n_items=3, speed=0.70,
                                         shape="circle", radius=0.14)
        r_trace, r_t_trk = make_activity_trace(r_act, total_s=10.0, center=r_c + RIGHT * 1.55 + DOWN * 0.85,
                                               width=2.15, height=1.10, label=None)
        r_note = T("1 good copy clears it", 26, C_BRAKE).move_to(r_c + DOWN * 1.82)
        right_all = VGroup(r_dial, r_trace, r_sw, r_sw_txt, r_stream, r_s2, r_g1, r_g2, r_note)

        self.add(l_ph, l_ph1, l_ph2n, l_ph2, r_ph, r_ph2, l_n_on, l_g2_norm_on, l_a_on, r_g2_on,
                 *l_t_trk, *r_t_trk)

        # Beat 1: Jamming an on-step needs only one altered copy
        self.at("Jamming an on")
        self.play(FadeIn(left_all), run_time=0.8)

        self.at("one altered copy")
        l_pin = Triangle(color=C_FAULT, fill_color=C_FAULT, fill_opacity=1.0).scale(0.11).rotate(-PI / 2)
        l_pin.move_to(l_g2.box.get_top() + UP * 0.10)
        l_g2_alt_lbl = T("altered", 24, C_ON).move_to(l_g2.label)
        l_sw_on_txt = T("1 stuck ON", 24, C_ON).move_to(l_sw)
        l_note_dom = T("Dominant gain", 26, C_ON).move_to(l_c + DOWN * 1.82)
        self.play(l_g2.box.animate.set_stroke(C_ON).set_fill(C_ON, opacity=0.22),
                  swap(l_g2.label, l_g2_alt_lbl, run_time=0.45),
                  FadeIn(l_pin, scale=1.2),
                  l_g2_norm_on.animate.set_value(0.0),
                  l_a_on.animate.set_value(1.0),
                  l_sw.animate.set_stroke(C_ON).set_fill(C_ON, opacity=0.22),
                  swap(l_sw_txt, l_sw_on_txt, run_time=0.45),
                  l_act.animate.set_value(0.95),
                  swap(l_note, l_note_dom, run_time=0.45),
                  run_time=1.0)

        self.at("normal protein from")
        self.play(l_g1.box.animate.set_stroke(C_OFF, width=5.5).set_fill(C_OFF, opacity=0.42), run_time=0.6)

        self.at("cannot switch")
        # Visual cue: normal protein block pushes at l_sw from below and bounces back while l_sw stays amber
        probe = RoundedRectangle(corner_radius=0.06, width=0.35, height=0.23,
                                 stroke_color=C_OFF, stroke_width=3,
                                 fill_color=C_OFF, fill_opacity=0.90).move_to(
            [l_g1.box.get_center()[0], l_sw.get_bottom()[1] - 0.35, 0])
        self.play(FadeIn(probe, shift=UP * 0.15), run_time=0.25)
        self.play(probe.animate.move_to([l_sw.get_left()[0] + 0.40, l_sw.get_bottom()[1] - 0.12, 0]),
                  l_sw.animate.set_stroke(C_FAULT, width=5.5),
                  run_time=0.45)
        self.play(probe.animate.shift(DOWN * 0.35).set_opacity(0),
                  l_sw.animate.set_stroke(C_ON, width=4),
                  l_g1.box.animate.set_stroke(C_OFF, width=3.5).set_fill(C_OFF, opacity=0.22),
                  run_time=0.6)
        self.remove(probe)

        # Beat 2: Removing an off-step usually needs both copies lost, because 1 good copy clears it
        self.at("Removing an off")
        self.play(FadeIn(right_all), run_time=0.8)

        self.at("one good copy")
        self.play(r_g2.box.animate.set_stroke(C_BRAKE, width=5.5).set_fill(C_BRAKE, opacity=0.42),
                  r_sw.animate.set_fill(C_OFF, opacity=0.32),
                  run_time=0.55)
        self.play(r_g2.box.animate.set_stroke(C_BRAKE, width=3.5).set_fill(C_BRAKE, opacity=0.22),
                  r_sw.animate.set_fill(C_OFF, opacity=0.20),
                  run_time=0.55)

        # Beat 3: Take-home rule caption (use "jams a switch" so it hits 17.90s, not 2.18s!)
        self.at("jams a switch")
        cap = caption("One altered copy jams a switch,\nwhile off-switch loss usually needs both.", size=26)
        self.play(FadeIn(cap, shift=UP * 0.1), run_time=0.7)

        # Beat 4: Off-switch loss triggers 2nd copy loss -> stuck ON -> Recessive loss
        self.at("off switch loss")
        r_g2_lost_box = make_gene_bar("", C_BRAKE, width=1.25, height=0.32,
                                      dashed=True, lost_x=True).move_to(r_g2.box.get_center())
        r_g2_lost_lbl = T("lost", 24, TEXT).move_to(r_g2.label)
        r_sw_on_txt = T("stuck ON", 24, C_ON).move_to(r_sw)
        r_note_rec = T("Recessive loss", 26, C_FAULT).move_to(r_c + DOWN * 1.82)

        self.play(FadeOut(r_g2.box, run_time=0.25),
                  FadeIn(r_g2_lost_box, run_time=0.35),
                  r_g2_on.animate.set_value(0.0),
                  swap(r_g2.label, r_g2_lost_lbl, run_time=0.45),
                  r_sw.animate.set_stroke(C_ON).set_fill(C_ON, opacity=0.25),
                  swap(r_sw_txt, r_sw_on_txt, run_time=0.45),
                  r_act.animate.set_value(0.95),
                  swap(r_note, r_note_rec, run_time=0.45),
                  run_time=1.0)
        self.finish()


class S10End(EndCard):
    LINE = "One altered copy jams a switch, while off-switch loss usually needs both."
