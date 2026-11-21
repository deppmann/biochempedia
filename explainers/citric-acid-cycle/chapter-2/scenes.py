"""The Roundabout Has Exits — Citric Acid Cycle, Chapter 2.

COLOUR MAP (one colour per concept for the entire film):
- BLUE   (#58C4DD): oxaloacetate (4C platform), station, pool blocks, pool gauge
- YELLOW (#F5D547): acetyl group (2C incoming fuel), acetyl-CoA, feedforward signal
- GOLD   (#D4A843): high-energy electrons (orbiting electron dots / pairs)
- TEAL   (#3FB8C0): NADH electron carriers and electron transport chain (ETC)
- GREEN  (#83C167): ATP energy token and ON switch
- ORANGE (#FF8C42): biosynthetic exits and building sites (fatty acids, amino acids, heme, glucose)
- RED    (#FC6255): oxygen consumed bar (Krebs) and OFF switch
- PURPLE (#C084FC): pyruvate
- PINK   (#F472B6): glutamine (dividing cells)
- GREY   (#8B93A1): CO2 block, road track, structural outlines
- TEXT   (#E8EAF0): labels, guiding catalyst loop, '?'

ONE WORLD:
One schematic metabolic roundabout centred at (-0.9, 0.25) with radius 1.82:
bottom blue station (oxaloacetate · 4C), left incoming acetyl-CoA lane, bottom-left
anaplerosis on-ramp with pyruvate carboxylase machine, four outward orange exit ramps
(citrate -> fatty acids, alpha-ketoglutarate -> amino acids, succinyl-CoA -> heme,
oxaloacetate -> glucose), right-side teal carrier lane to the electron transport chain,
and vertical oxaloacetate pool gauge beside the blue station.

WHAT CHANGES PER SCENE:
- s00_hook: Yellow 2C cart with gold electron dots merges from left, turns clockwise around
  the roundabout loading a teal carrier to the ETC and returning the blue 4C block to the
  station; green ATP drops into a bottom-left machine stamping a fresh 4C block; '?' rises.
- s01_title: Same moving roundabout, cart, and bottom-left machine turn behind a 2s title
  overlay as '?' fades out.
- s02_exits: Four orange exit ramps grow sequentially from citrate, alpha-ketoglutarate,
  succinyl-CoA, and oxaloacetate, each peeling an orange block into its building site.
- s03_drain: Computed pool ValueTracker falls from 1.0 to 0.25, station stack thins 4 -> 1,
  road speed slows proportionally, yellow carts queue at citrate synthase, and ETC trickle thins.
- s04_krebs: Three blue 4C blocks drop into the station, pool rises 0.25 -> 0.90, road speeds up,
  queued carts merge, two computed/schematic bars grow (pinch alone vs oxygen used), and one
  blue block completes rapid turns carrying fresh yellow carts.
- s05_guiding: White catalyst ring draws around the roundabout and cracks open at each of the
  four active exits; an empty dashed anaplerosis on-ramp outline appears at bottom-left.
- s06_refill: Pyruvate carboxylase rolls onto the on-ramp; purple pyruvate, grey CO2, and green
  ATP enter to stamp blue 4C blocks up the ramp into the station while the pool gauge climbs.
- s07_predict: Refill machine switches to OFF; yellow carts drift slowly at the entrance; top
  prompt "What switches the refill on?" and "?" answer box appear.
- s08_think: PredictPause holds the question and "?" box for 4.5s with countdown ring while
  carts drift slowly, road turns gently, and "?" breathes once at ~2s.
- s09_feedforward: Answer box fills with yellow acetyl-CoA; yellow feedforward arrow flips
  switch to ON; machine restarts and speeds up in step with arriving carts as pool climbs.
- s10_hub: Pink glutamine on-ramp joins at alpha-ketoglutarate; balanced traffic flows through
  exits, both refills, and brightened ETC lane while the pool gauge settles and holds steady.
- s11_return: Full composition pulls back; blue 4C block locks a turn into the station, gold pairs
  flow to ETC, four orange exits pulse together, and anaplerosis ramp sends a 4C block up.
- s12_end: Standard EndCard with exact take-home line.
"""

import numpy as np
from bp_parts import *  # noqa: F401,F403

# Concept colours beyond bp_style defaults
ORANGE = "#FF8C42"
PURPLE = "#C084FC"
PINK = "#F472B6"

# Shared roundabout geometry
RC = np.array([-0.9, 0.25, 0.0])
R_ROAD = 1.82
R_IN = 1.60
R_OUT = 2.04

STATION_C = np.array([-0.9, -1.58, 0.0])
MERGE_ANGLE = -145.0 * DEGREES       # lower-left merge point on the ring
MERGE_PT = RC + R_ROAD * np.array([np.cos(MERGE_ANGLE), np.sin(MERGE_ANGLE), 0.0])

# Ramp anchor angles (clockwise from bottom = -90 deg)
ANG_CITRATE = 142.0 * DEGREES
ANG_AKG = 74.0 * DEGREES
ANG_SUCC = -10.0 * DEGREES
ANG_OAA = -62.0 * DEGREES
ANG_ETC = 24.0 * DEGREES
ANG_GLUT = 112.0 * DEGREES

PC_POS = np.array([-4.15, -2.44, 0.0])
GAUGE_POS = np.array([1.75, -1.12, 0.0])


def road_pt(angle_rad, r=R_ROAD):
    return RC + r * np.array([np.cos(angle_rad), np.sin(angle_rad), 0.0])


def make_block(color, w=0.38, h=0.24, opacity=0.88):
    return RoundedRectangle(
        corner_radius=0.06,
        width=w,
        height=h,
        stroke_color=color,
        stroke_width=2.5,
        fill_color=color,
        fill_opacity=opacity,
    )


def make_electron_pair(center=ORIGIN, radius=0.055):
    d1 = Dot(radius=radius, color=GOLD).shift(LEFT * 0.07)
    d2 = Dot(radius=radius, color=GOLD).shift(RIGHT * 0.07)
    return VGroup(d1, d2).move_to(center)


class RoundaboutWorld:
    """Shared schematic world builder so carried objects match across scenes."""

    def __init__(self, speed=0.85, pool_level=0.85, stack_count=4, show_etc="full", start_phase=-90.0 * DEGREES):
        self.speed = ValueTracker(speed)
        self.pool = ValueTracker(pool_level)
        self.phase = ValueTracker(start_phase)
        self.root = VGroup()

        # 1. Road track
        self.annulus = Annulus(
            inner_radius=R_IN,
            outer_radius=R_OUT,
            fill_color=GREY,
            fill_opacity=0.22,
            stroke_width=0,
        ).move_to(RC)
        self.outer_ring = Circle(radius=R_OUT, color=GREY, stroke_width=3).move_to(RC)
        self.inner_ring = Circle(radius=R_IN, color=GREY, stroke_width=3).move_to(RC)
        self.dash_ring = DashedVMobject(
            Circle(radius=R_ROAD, color=GREY, stroke_width=2).move_to(RC),
            num_dashes=32,
        ).set_opacity(0.45)

        # Visible clockwise platform capsules orbiting on the road (driven by phase)
        self.road_markers = VGroup()
        self.n_markers = 6
        for i in range(self.n_markers):
            cap = RoundedRectangle(
                corner_radius=0.07,
                width=0.46,
                height=0.22,
                stroke_color=BLUE,
                stroke_width=2.5,
                fill_color=BLUE,
                fill_opacity=0.82,
            )
            e_dot = make_electron_pair(ORIGIN, radius=0.048).shift(RIGHT * 0.08)
            unit = VGroup(cap, e_dot)
            unit._last_ang = 0.0
            self.road_markers.add(unit)

        def _spin_markers(mob, dt):
            self.phase.increment_value(-self.speed.get_value() * dt)
            ph = self.phase.get_value()
            for idx, m in enumerate(mob):
                ang = ph + idx * TAU / self.n_markers
                m.move_to(road_pt(ang, R_ROAD))
                tangent_ang = ang - PI / 2.0
                m.rotate(tangent_ang - m._last_ang)
                m._last_ang = tangent_ang

        self.road_markers.add_updater(_spin_markers)

        # 2. Blue station at bottom
        self.station_box = RoundedRectangle(
            corner_radius=0.14,
            width=2.15,
            height=0.66,
            stroke_color=BLUE,
            stroke_width=3.5,
            fill_color=BLUE,
            fill_opacity=0.14,
        ).move_to(STATION_C)
        self.station_label = T("oxaloacetate · 4C", size=24, color=BLUE).move_to([-0.9, -2.26, 0])

        self.stack_blocks = VGroup()
        self.set_stack(stack_count)

        # 3. Left acetyl-CoA entrance lane (horizontal at y = MERGE_PT[1])
        self.ent_y = MERGE_PT[1]
        self.ent_start = np.array([-6.05, self.ent_y, 0.0])
        self.ent_end = MERGE_PT.copy()
        self.ent_lane = VGroup(
            Line(self.ent_start + UP * 0.20, self.ent_end + UP * 0.20, color=GREY, stroke_width=2.5),
            Line(self.ent_start + DOWN * 0.20, self.ent_end + DOWN * 0.20, color=GREY, stroke_width=2.5),
            DashedLine(self.ent_start, self.ent_end, color=YELLOW, stroke_width=2, dash_length=0.18).set_opacity(0.5),
        )
        self.acetyl_label = T("acetyl group · 2C", size=24, color=YELLOW).move_to([-4.85, self.ent_y + 0.48, 0])

        # 4. Right-side ETC carrier lane & block
        self.etc_start = road_pt(ANG_ETC, R_OUT)
        self.etc_block = RoundedRectangle(
            corner_radius=0.14,
            width=1.85,
            height=1.40,
            stroke_color=TEAL,
            stroke_width=3,
            fill_color=TEAL,
            fill_opacity=0.16,
        ).move_to([5.35, self.etc_start[1], 0.0])
        self.etc_label = fit_text("electron\ntransport\nchain", max_w=1.55, size=24, color=TEAL, max_lines=3).move_to(
            self.etc_block
        )
        self.etc_lane = Line(
            self.etc_start,
            np.array([self.etc_block.get_left()[0], self.etc_start[1], 0.0]),
            color=TEAL,
            stroke_width=5,
        )
        self.etc_strip = RoundedRectangle(
            corner_radius=0.08,
            width=0.28,
            height=2.10,
            stroke_color=TEAL,
            stroke_width=2,
            fill_color=TEAL,
            fill_opacity=0.20,
        ).move_to([6.10, 0.90, 0.0])
        self.etc_thin_lane = Line(
            self.etc_start,
            np.array([self.etc_strip.get_left()[0], self.etc_start[1], 0.0]),
            color=TEAL,
            stroke_width=2.5,
        ).set_opacity(0.45)

        self.etc_full_grp = VGroup(self.etc_lane, self.etc_block, self.etc_label)
        self.etc_dim_grp = VGroup(self.etc_thin_lane, self.etc_strip)

        # 5. Corner schematic tag (full opacity, TEXT color per TASK.md)
        self.schematic_tag = scope_tag("schematic", size=24, color=TEXT)

        self.root.add(
            self.annulus,
            self.outer_ring,
            self.inner_ring,
            self.dash_ring,
            self.ent_lane,
            self.station_box,
            self.stack_blocks,
            self.road_markers,
            self.station_label,
            self.acetyl_label,
            self.schematic_tag,
        )
        if show_etc == "full":
            self.root.add(self.etc_full_grp)
        elif show_etc == "dim":
            self.root.add(self.etc_dim_grp)

    def set_stack(self, count):
        self.stack_blocks.submobjects.clear()
        xs = np.linspace(-1.55, -0.25, 4)
        for i in range(max(0, min(4, count))):
            b = make_block(BLUE, w=0.34, h=0.36, opacity=0.90).move_to([xs[i], STATION_C[1], 0.0])
            self.stack_blocks.add(b)

    def build_exits(self, outlines_only=False):
        """Four orange exit ramps and building sites."""
        specs = [
            (
                "fatty acids",
                road_pt(ANG_CITRATE, R_OUT),
                np.array([-4.05, 2.25, 0.0]),
                np.array([-4.95, 2.35, 0.0]),
            ),
            (
                "amino acids",
                road_pt(ANG_AKG, R_OUT),
                np.array([2.40, 2.40, 0.0]),
                np.array([3.50, 2.42, 0.0]),
            ),
            (
                "heme",
                road_pt(ANG_SUCC, R_OUT),
                np.array([3.10, -0.08, 0.0]),
                np.array([3.90, -0.08, 0.0]),
            ),
            (
                "glucose",
                np.array([0.18, STATION_C[1] - 0.14, 0.0]),
                np.array([2.10, -2.75, 0.0]),
                np.array([2.95, -2.85, 0.0]),
            ),
        ]
        ramps = []
        for name, p0, p1, box_c in specs:
            line = Line(p0, p1, color=ORANGE, stroke_width=4)
            if outlines_only:
                tmp = boxed_label(name, color=ORANGE, size=24, pad=0.18)
                box = RoundedRectangle(
                    corner_radius=0.14,
                    width=tmp.box.width,
                    height=tmp.box.height,
                    stroke_color=ORANGE,
                    stroke_width=2,
                    stroke_opacity=0.35,
                    fill_color=ORANGE,
                    fill_opacity=0.05,
                ).move_to(box_c)
                line.set_stroke(opacity=0.35)
                end_pt = np.array([box.get_right()[0] if name == "fatty acids" else box.get_left()[0], box_c[1], 0.0])
            else:
                box = boxed_label(name, color=ORANGE, size=24, pad=0.18)
                box.move_to(box_c)
                end_pt = np.array([box.get_right()[0] if name == "fatty acids" else box.get_left()[0], box_c[1], 0.0])
            line.put_start_and_end_on(p0, end_pt)
            # Stop trickle blocks 0.30 units before box edge so they never straddle the box
            vec = end_pt - p0
            p_stop = end_pt - 0.32 * vec / max(np.linalg.norm(vec), 1e-6)
            ramps.append({"name": name, "p0": p0, "p1": p_stop, "end_pt": end_pt, "line": line, "box": box, "grp": VGroup(line, box)})
        self.exits = ramps
        return ramps

    def start_exit_trickle(self, ramps, rate=0.38):
        """Continuously move small orange blocks along each active exit ramp (stopping short of box)."""
        trickle = VGroup()
        for idx, r in enumerate(ramps):
            blk = make_block(ORANGE, w=0.24, h=0.16, opacity=0.92)
            blk._t = (idx * 0.25) % 1.0
            blk._p0, blk._p1 = r["p0"], r["p1"]

            def _move(m, dt, sp=rate):
                m._t = (m._t + sp * dt) % 1.0
                m.move_to((1.0 - m._t) * m._p0 + m._t * m._p1)

            blk.add_updater(_move)
            trickle.add(blk)
        self.exit_trickle = trickle
        return trickle

    def build_pool_gauge(self, wobble=False):
        """Vertical schematic gauge beside the blue station, driven by self.pool."""
        w, h = 0.36, 1.48
        frame = RoundedRectangle(
            corner_radius=0.08,
            width=w,
            height=h,
            stroke_color=BLUE,
            stroke_width=2.5,
            fill_color=BG,
            fill_opacity=0.85,
        ).move_to(GAUGE_POS)
        bot_y = frame.get_bottom()[1] + 0.05
        max_h = h - 0.10
        clock = ValueTracker(0.0)

        def _mk_fill():
            lvl = float(np.clip(self.pool.get_value(), 0.06, 0.98))
            if wobble:
                lvl = float(np.clip(lvl + 0.04 * np.sin(3.5 * clock.get_value()), 0.06, 0.98))
            fh = max(0.08, lvl * max_h)
            r = Rectangle(
                width=w - 0.10,
                height=fh,
                stroke_width=0,
                fill_color=BLUE,
                fill_opacity=0.82,
            )
            r.move_to([GAUGE_POS[0], bot_y + fh / 2.0, 0.0])
            return r

        fill = always_redraw(_mk_fill)
        if wobble:
            frame.add_updater(lambda m, dt: clock.increment_value(dt))
        lab = T("oxaloacetate\npool", size=24, color=BLUE, line_spacing=0.85).next_to(frame, RIGHT, buff=0.18)
        self.gauge = VGroup(frame, fill, lab)
        self.gauge_frame = frame
        self.gauge_label = lab
        return self.gauge

    def build_onramp(self, labelled=True, dashed=False):
        """Bottom-left anaplerosis on-ramp from PC machine into the blue station."""
        p0 = PC_POS + RIGHT * 1.05
        p1 = np.array([self.station_box.get_left()[0], STATION_C[1] - 0.05, 0.0])
        if dashed:
            line = DashedLine(p0, p1, color=BLUE, stroke_width=3.5, dash_length=0.18)
        else:
            line = Line(p0, p1, color=BLUE, stroke_width=4)
        self.onramp_p0, self.onramp_p1 = p0, p1
        self.onramp_line = line
        grp = VGroup(line)
        if labelled:
            self.onramp_label = T("anaplerosis · refill", size=24, color=BLUE).move_to([-4.15, -3.24, 0.0])
            grp.add(self.onramp_label)
        return grp

    def build_pc_machine(self, label_text="pyruvate\ncarboxylase", switch=None):
        """Side refill machine box at PC_POS."""
        box = RoundedRectangle(
            corner_radius=0.14,
            width=2.10,
            height=0.86,
            stroke_color=BLUE,
            stroke_width=3,
            fill_color=BG,
            fill_opacity=0.92,
        ).move_to(PC_POS)
        if label_text:
            lbl = T(label_text, size=24, color=TEXT, line_spacing=0.82).move_to(box)
        else:
            lbl = T("+ 4C", size=24, color=BLUE).move_to(box)
        grp = VGroup(box, lbl)
        # Place switch badge cleanly above top-left of pc_box, clear of onramp line on right
        sw_pos = np.array([box.get_left()[0] + 0.45, box.get_top()[1] + 0.36, 0.0])
        if switch == "OFF":
            sw = boxed_label("OFF", color=RED, size=22, pad=0.14).move_to(sw_pos)
            grp.add(sw)
            self.pc_switch = sw
        elif switch == "ON":
            sw = boxed_label("ON", color=GREEN, size=22, pad=0.14).move_to(sw_pos)
            grp.add(sw)
            self.pc_switch = sw
        self.pc_sw_pos = sw_pos
        self.pc_box = box
        self.pc_grp = grp
        return grp


def build_queuing_carts(n=3, start_x=-3.2, spacing=0.72, y=MERGE_PT[1]):
    carts = VGroup()
    for i in range(n):
        c = make_block(YELLOW, w=0.38, h=0.26, opacity=0.92).move_to([start_x - i * spacing, y, 0.0])
        carts.add(c)
    return carts


# --------------------------------------------------------------------------- scenes
class S00Hook(SpokenScene):
    def construct(self):
        W = RoundaboutWorld(speed=0.75, pool_level=0.85, stack_count=1, show_etc="full")
        self.add(W.root)

        cart = make_block(YELLOW, w=0.40, h=0.26, opacity=0.95).move_to([-4.95, W.ent_y, 0.0])
        e_pair = make_electron_pair(cart.get_center(), radius=0.055)
        e_theta = ValueTracker(0.0)
        e_pair.add_updater(
            lambda m, dt: (
                e_theta.increment_value(4.5 * dt),
                m.move_to(
                    cart.get_center()
                    + np.array([0.30 * np.cos(e_theta.get_value()), 0.22 * np.sin(e_theta.get_value()), 0.0])
                ),
            )
        )
        blue_turn = make_block(BLUE, w=0.38, h=0.26, opacity=0.92)
        turn_ang = ValueTracker(-145.0 * DEGREES)
        blue_turn.add_updater(lambda m: m.move_to(road_pt(turn_ang.get_value(), R_ROAD)))
        self.add(cart, e_pair)

        self.play(cart.animate.move_to(MERGE_PT), run_time=1.3, rate_func=linear)
        self.add(blue_turn)
        cart.add_updater(lambda m: m.move_to(road_pt(turn_ang.get_value(), R_ROAD - 0.14)))

        self.play(turn_ang.animate.set_value(-310.0 * DEGREES), run_time=1.7, rate_func=linear)

        carrier = make_block(TEAL, w=0.34, h=0.22, opacity=0.92).move_to(W.etc_start)
        carrier_dots = make_electron_pair(carrier.get_center(), radius=0.05)
        carrier_grp = VGroup(carrier, carrier_dots)
        self.add(carrier_grp)

        self.play(
            turn_ang.animate.set_value(-450.0 * DEGREES),
            carrier_grp.animate.move_to([W.etc_block.get_left()[0] - 0.25, W.etc_start[1], 0.0]),
            run_time=1.5,
            rate_func=linear,
        )
        cart.clear_updaters()
        e_pair.clear_updaters()
        blue_turn.clear_updaters()
        self.play(
            FadeOut(cart, run_time=0.3),
            FadeOut(e_pair, run_time=0.3),
            FadeOut(carrier_grp, run_time=0.3),
            blue_turn.animate.move_to(STATION_C + RIGHT * 0.45),
            run_time=0.5,
        )

        self.at("reusable platform")
        pulse_ring = SurroundingRectangle(W.station_box, corner_radius=0.16, color=BLUE, stroke_width=4, buff=0.08)
        self.play(FadeIn(pulse_ring), run_time=0.35)
        self.play(FadeOut(pulse_ring), run_time=0.45)

        self.at("here is a puzzle")
        onramp = W.build_onramp(labelled=False, dashed=False)
        pc_mach = W.build_pc_machine(label_text="", switch=None)
        self.play(Create(onramp), FadeIn(pc_mach, shift=UP * 0.15), run_time=0.8)

        self.at("spend")
        atp = boxed_label("ATP", color=GREEN, size=24, pad=0.14).move_to(PC_POS + UP * 0.92)
        self.play(FadeIn(atp, shift=DOWN * 0.1), run_time=0.35)
        self.play(FadeOut(atp, shift=DOWN * 0.4), run_time=0.55)

        fresh_4c = make_block(BLUE, w=0.36, h=0.24, opacity=0.95).move_to(PC_POS + RIGHT * 1.48 + UP * 0.22)
        qmark = T("?", size=64, color=TEXT, weight=BOLD).move_to(RC + DOWN * 0.35)
        self.play(FadeIn(fresh_4c, shift=RIGHT * 0.2), FadeIn(qmark, shift=UP * 0.25), run_time=0.75)

        next_cart = make_block(YELLOW, w=0.38, h=0.26, opacity=0.90).move_to([-5.6, W.ent_y, 0.0])
        self.add(next_cart)
        self.play(next_cart.animate.move_to([-3.8, W.ent_y, 0.0]), run_time=1.0, rate_func=linear)
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        W = RoundaboutWorld(speed=0.75, pool_level=0.85, stack_count=2, show_etc="full")
        onramp = W.build_onramp(labelled=False, dashed=False)
        pc_mach = W.build_pc_machine(label_text="", switch=None)
        fresh_4c = make_block(BLUE, w=0.36, h=0.24, opacity=0.95).move_to(PC_POS + RIGHT * 1.48 + UP * 0.22)
        qmark = T("?", size=64, color=TEXT, weight=BOLD).move_to(RC + DOWN * 0.35)
        cart = make_block(YELLOW, w=0.38, h=0.26, opacity=0.90).move_to([-3.8, W.ent_y, 0.0])
        cart.add_updater(lambda m, dt: m.shift(RIGHT * 0.45 * dt))

        self.add(W.root, onramp, pc_mach, fresh_4c, qmark, cart)

        # Compact high-contrast card clear of acetyl label (x < -3.5) and ETC block (x > 4.4)
        card = RoundedRectangle(
            corner_radius=0.22,
            width=7.1,
            height=3.05,
            stroke_color=GOLD,
            stroke_width=3,
            fill_color=BG,
            fill_opacity=0.94,
        ).move_to([0.35, 0.30, 0.0]).set_z_index(20)
        lesson = T("THE CITRIC ACID CYCLE:\nHARVESTING ELECTRONS", size=22, color=TEAL, line_spacing=0.9).set_z_index(21)
        title = T("THE ROUNDABOUT\nHAS EXITS", size=40, font=TITLE_FONT, color=TEXT, line_spacing=0.90).set_z_index(21)
        rule = Line(LEFT * 1.4, RIGHT * 1.4, color=GOLD, stroke_width=4).set_z_index(21)
        txt_grp = VGroup(lesson, title, rule).arrange(DOWN, buff=0.18).move_to(card).set_z_index(21)

        self.play(FadeOut(qmark, run_time=0.4), FadeIn(card), FadeIn(txt_grp), run_time=0.55)
        self.finish()


class S02Exits(SpokenScene):
    def construct(self):
        W = RoundaboutWorld(speed=0.95, pool_level=0.85, stack_count=4, show_etc="dim")
        W.root.remove(W.acetyl_label)
        ramps = W.build_exits(outlines_only=False)

        # Ongoing breakdown traffic: yellow acetyl carts entering & teal carriers flowing right
        ent_flow = make_block(YELLOW, w=0.38, h=0.24, opacity=0.92)
        ent_flow._t = 0.0
        ent_end = MERGE_PT - RIGHT * 0.25
        ent_flow.add_updater(
            lambda m, dt: (
                setattr(m, "_t", (m._t + 0.45 * dt) % 1.0),
                m.move_to((1 - m._t) * W.ent_start + m._t * ent_end),
            )
        )
        etc_end = np.array([W.etc_strip.get_left()[0] - 0.24, W.etc_start[1], 0.0])
        etc_flow = VGroup(make_block(TEAL, w=0.30, h=0.20, opacity=0.72), make_electron_pair(ORIGIN, radius=0.045))
        etc_flow._t = 0.3
        etc_flow.add_updater(
            lambda m, dt: (
                setattr(m, "_t", (m._t + 0.36 * dt) % 1.0),
                m.move_to((1 - m._t) * W.etc_start + m._t * etc_end),
            )
        )
        self.add(W.root, ent_flow, etc_flow)

        self.at("is amphibolic")
        amph_bg = RoundedRectangle(
            corner_radius=0.14,
            width=2.75,
            height=1.15,
            stroke_width=0,
            fill_color=BG,
            fill_opacity=0.88,
        ).move_to(RC)
        amph_lbl = T("amphibolic:\nbreakdown +\nbuilding", size=24, color=TEXT, line_spacing=0.85).move_to(RC)
        self.play(FadeIn(amph_bg), FadeIn(amph_lbl), run_time=0.65)

        trickle_grp = VGroup()
        self.add(trickle_grp)

        def _launch_ramp(idx, seg_text=None, seg_pos=None):
            r = ramps[idx]
            anims = [Create(r["line"]), FadeIn(r["box"])]
            if seg_text is not None:
                seg_lbl = T(seg_text, size=24, color=ORANGE).move_to(seg_pos)
                anims.append(FadeIn(seg_lbl))
            self.play(*anims, run_time=0.75)
            peel = make_block(ORANGE, w=0.28, h=0.18, opacity=0.95).move_to(r["p0"])
            self.play(peel.animate.move_to(r["p1"]), run_time=0.75, rate_func=linear)
            self.remove(peel)
            blk = make_block(ORANGE, w=0.24, h=0.16, opacity=0.90)
            blk._t = 0.0
            blk._p0, blk._p1 = r["p0"], r["p1"]
            blk.add_updater(lambda m, dt: (setattr(m, "_t", (m._t + 0.38 * dt) % 1.0), m.move_to((1 - m._t) * m._p0 + m._t * m._p1)))
            trickle_grp.add(blk)

        self.at("Citrate leaves")
        _launch_ramp(0, "citrate", [-3.45, 1.08, 0.0])

        self.at("Alpha")
        _launch_ramp(1, "α-ketoglutarate", [-1.65, 2.65, 0.0])

        self.at("builds heme")
        _launch_ramp(2, "succinyl-CoA", [2.35, 0.45, 0.0])

        self.at("itself feeds")
        _launch_ramp(3)

        self.finish()


class S03Drain(SpokenScene):
    def construct(self):
        W = RoundaboutWorld(speed=0.80, pool_level=1.0, stack_count=4, show_etc="dim")
        ramps = W.build_exits(outlines_only=False)
        for r in ramps:
            self.add(r["grp"])
        trickle = W.start_exit_trickle(ramps, rate=0.38)
        gauge = W.build_pool_gauge(wobble=False)
        self.add(W.root, trickle)

        self.play(FadeIn(gauge, shift=UP * 0.2), run_time=0.8)

        self.at("pool shrinks")
        self.play(
            W.pool.animate.set_value(0.75),
            W.speed.animate.set_value(0.60),
            run_time=1.8,
            rate_func=linear,
        )
        W.set_stack(3)

        self.at("Citrate synthase")
        gate_bar = Line(
            MERGE_PT + UP * 0.26 + LEFT * 0.12,
            MERGE_PT + DOWN * 0.26 + RIGHT * 0.12,
            color=YELLOW,
            stroke_width=5,
        )
        # Position cleanly left of outer ring (x < -2.94) and well above acetyl label (y = -0.32)
        gate_lbl = T("citrate synthase", size=24, color=TEXT).move_to([-4.55, 0.28, 0.0])
        carts = build_queuing_carts(n=3, start_x=-3.05, spacing=0.62, y=W.ent_y)
        self.play(
            Create(gate_bar),
            FadeIn(gate_lbl),
            FadeIn(carts, shift=RIGHT * 0.25),
            W.pool.animate.set_value(0.50),
            W.speed.animate.set_value(0.40),
            run_time=2.2,
            rate_func=linear,
        )
        W.set_stack(2)

        self.at("fewer acetyl groups")
        lead_cart = carts[0]
        self.play(
            lead_cart.animate.move_to(MERGE_PT),
            carts[1:].animate.shift(RIGHT * 0.62),
            W.pool.animate.set_value(0.25),
            W.speed.animate.set_value(0.22),
            run_time=2.4,
            rate_func=linear,
        )
        W.set_stack(1)
        lead_cart.add_updater(lambda m, dt: m.move_to(road_pt(W.phase.get_value() - 145 * DEGREES, R_ROAD - 0.12)))

        self.at("fewer loaded carriers")
        nadh = VGroup(make_block(TEAL, w=0.30, h=0.20, opacity=0.80), make_electron_pair(ORIGIN, radius=0.045))
        nadh.move_to(W.etc_start)
        self.add(nadh)
        self.play(
            nadh.animate.move_to(np.array([W.etc_strip.get_left()[0] - 0.25, W.etc_start[1], 0.0])),
            run_time=2.2,
            rate_func=linear,
        )
        self.finish()


class S04Krebs(SpokenScene):
    def construct(self):
        W = RoundaboutWorld(speed=0.24, pool_level=0.25, stack_count=1, show_etc="dim")
        # Exits faded to outlines only (no low-opacity text)
        ramps = W.build_exits(outlines_only=True)
        for r in ramps:
            self.add(r["grp"])
        gauge = W.build_pool_gauge(wobble=False)
        gate_bar = Line(
            MERGE_PT + UP * 0.26 + LEFT * 0.12,
            MERGE_PT + DOWN * 0.26 + RIGHT * 0.12,
            color=YELLOW,
            stroke_width=5,
        )
        carts = build_queuing_carts(n=3, start_x=-3.05, spacing=0.62, y=W.ent_y)
        self.add(W.root, gauge, gate_bar, carts)

        self.at("A pinch")
        pinch = VGroup(
            make_block(BLUE, w=0.32, h=0.28, opacity=0.95).shift(LEFT * 0.38),
            make_block(BLUE, w=0.32, h=0.28, opacity=0.95),
            make_block(BLUE, w=0.32, h=0.28, opacity=0.95).shift(RIGHT * 0.38),
        ).move_to([-0.9, 0.45, 0.0])
        self.play(FadeIn(pinch, shift=DOWN * 0.2), run_time=0.45)
        self.play(
            pinch.animate.move_to(STATION_C),
            W.pool.animate.set_value(0.90),
            W.speed.animate.set_value(1.35),
            run_time=1.35,
        )
        self.remove(pinch)
        W.set_stack(4)

        self.play(
            FadeOut(carts[0], shift=RIGHT * 0.4),
            carts[1].animate.move_to(MERGE_PT + LEFT * 0.55),
            carts[2].animate.move_to(MERGE_PT + LEFT * 1.15),
            run_time=0.9,
            rate_func=linear,
        )

        self.at("more oxygen")
        # Rapid carrier flow to the chain showing heightened oxygen consumption
        etc_end = np.array([W.etc_strip.get_left()[0] - 0.24, W.etc_start[1], 0.0])
        o2_flow = VGroup(make_block(TEAL, w=0.32, h=0.22, opacity=0.85), make_electron_pair(ORIGIN, radius=0.05))
        o2_flow._t = 0.0
        o2_flow.add_updater(
            lambda m, dt: (
                setattr(m, "_t", (m._t + 0.68 * dt) % 1.0),
                m.move_to((1 - m._t) * W.etc_start + m._t * etc_end),
            )
        )
        self.add(o2_flow)

        base_y = -2.05
        bar_pinch = Rectangle(width=0.62, height=0.04, fill_color=BLUE, fill_opacity=0.85, stroke_color=BLUE, stroke_width=2)
        bar_pinch.move_to([4.35, base_y + 0.02, 0.0])
        bar_o2 = Rectangle(width=0.62, height=0.04, fill_color=RED, fill_opacity=0.85, stroke_color=RED, stroke_width=2)
        bar_o2.move_to([5.55, base_y + 0.02, 0.0])
        lbl_pinch = T("pinch\nalone", size=24, color=BLUE, line_spacing=0.85).move_to([4.35, base_y - 0.52, 0.0])
        lbl_o2 = T("oxygen\nused", size=24, color=RED, line_spacing=0.85).move_to([5.55, base_y - 0.52, 0.0])
        bar_base = Line([3.85, base_y, 0.0], [6.05, base_y, 0.0], color=GREY, stroke_width=2.5)
        self.add(bar_base, bar_pinch, bar_o2)
        self.play(
            bar_pinch.animate.stretch_to_fit_height(0.45, about_edge=DOWN),
            bar_o2.animate.stretch_to_fit_height(2.40, about_edge=DOWN),
            FadeIn(lbl_pinch),
            FadeIn(lbl_o2),
            run_time=1.8,
        )

        self.at("carried many acetyl groups")
        # Highlight one road capsule so it tracks 3 rapid laps cleanly with no overlap
        runner_ring = always_redraw(
            lambda: Circle(radius=0.30, color=GOLD, stroke_width=3.5).move_to(W.road_markers[0].get_center())
        )
        self.add(runner_ring)
        W.speed.set_value(TAU / 1.35)
        for _ in range(3):
            fresh_y = make_block(YELLOW, w=0.34, h=0.22, opacity=0.92).move_to([-3.6, W.ent_y, 0.0])
            self.add(fresh_y)
            self.play(
                FadeOut(fresh_y, shift=RIGHT * 0.9),
                run_time=1.35,
                rate_func=linear,
            )
        self.remove(runner_ring)
        self.finish()


class S05Guiding(SpokenScene):
    def construct(self):
        W = RoundaboutWorld(speed=0.55, pool_level=0.28, stack_count=1, show_etc="dim")
        ramps = W.build_exits(outlines_only=False)
        for r in ramps:
            self.add(r["grp"])
        trickle = W.start_exit_trickle(ramps, rate=0.38)
        gauge = W.build_pool_gauge(wobble=True)
        self.add(W.root, trickle, gauge)

        self.at("behaves as a catalyst")
        full_loop = Circle(radius=R_OUT + 0.08, color=TEXT, stroke_width=5).move_to(RC)
        self.play(Create(full_loop), run_time=1.4)

        exit_angles = sorted([ANG_CITRATE, ANG_AKG, ANG_SUCC, ANG_OAA])
        gap = 18.0 * DEGREES
        arcs = VGroup()
        for i in range(len(exit_angles)):
            a0 = exit_angles[i] + gap / 2
            a1 = (exit_angles[(i + 1) % len(exit_angles)] if i + 1 < len(exit_angles) else exit_angles[0] + TAU) - gap / 2
            arcs.add(
                Arc(
                    radius=R_OUT + 0.08,
                    start_angle=a0,
                    angle=a1 - a0,
                    arc_center=RC,
                    color=TEXT,
                    stroke_width=5,
                )
            )
        self.remove(full_loop)
        self.add(arcs)
        self.play(arcs.animate.set_stroke(opacity=0.85), run_time=0.5)

        self.at("must be put back")
        onramp = W.build_onramp(labelled=False, dashed=True)
        self.play(Create(onramp), run_time=1.0)

        self.at("has a name")
        ana_lbl = T("anaplerosis · refill", size=24, color=BLUE).move_to([-4.15, -3.24, 0.0])
        self.play(FadeIn(ana_lbl, shift=UP * 0.15), run_time=0.75)
        self.finish()


class S06Refill(SpokenScene):
    def construct(self):
        W = RoundaboutWorld(speed=0.60, pool_level=0.28, stack_count=1, show_etc="dim")
        ramps = W.build_exits(outlines_only=False)
        for r in ramps:
            self.add(r["grp"])
        trickle = W.start_exit_trickle(ramps, rate=0.34)
        gauge = W.build_pool_gauge(wobble=False)
        onramp = W.build_onramp(labelled=True, dashed=False)
        self.add(W.root, trickle, gauge, onramp)

        self.at("pyruvate carboxylase")
        pc_mach = W.build_pc_machine(label_text="pyruvate\ncarboxylase", switch=None)
        pc_mach.shift(LEFT * 0.85)
        self.play(pc_mach.animate.shift(RIGHT * 0.85), run_time=0.85)

        self.at("adds carbon dioxide")
        pyr = boxed_label("pyruvate", color=PURPLE, size=24, pad=0.14).move_to([-5.45, -1.55, 0.0])
        co2 = boxed_label("CO2", color=GREY, size=24, pad=0.14).move_to([-5.95, -2.50, 0.0])
        self.play(FadeIn(pyr, shift=RIGHT * 0.12), FadeIn(co2, shift=RIGHT * 0.12), run_time=0.55)
        # Fade out cleanly into left/top of PC box without overlapping PC box
        self.play(FadeOut(pyr, shift=DOWN * 0.15), FadeOut(co2, shift=RIGHT * 0.15), run_time=0.65)

        self.at("The reaction uses")
        atp = boxed_label("ATP", color=GREEN, size=24, pad=0.14).move_to(PC_POS + UP * 0.92)
        self.play(FadeIn(atp, shift=DOWN * 0.1), run_time=0.35)
        self.play(FadeOut(atp, shift=DOWN * 0.35), run_time=0.55)

        for step, target_pool in enumerate((0.56, 0.85)):
            blk = make_block(BLUE, w=0.34, h=0.22, opacity=0.95).move_to(W.onramp_p0)
            self.add(blk)
            self.play(
                blk.animate.move_to(W.onramp_p1),
                W.pool.animate.set_value(target_pool),
                W.speed.animate.set_value(0.75 + 0.1 * step),
                run_time=1.1,
                rate_func=linear,
            )
            self.remove(blk)
            W.set_stack(2 + step * 2)

        self.at("opening puzzle")
        qmark = T("?", size=52, color=TEXT, weight=BOLD).move_to(PC_POS + UP * 0.92)
        self.play(FadeIn(qmark, shift=UP * 0.1), run_time=0.4)
        self.play(FadeOut(qmark), run_time=0.5)
        self.finish()


def _predict_backdrop():
    """Shared world builder for S07Predict and S08Think (PredictPause)."""
    W = RoundaboutWorld(speed=0.55, pool_level=0.55, stack_count=2, show_etc="dim")
    ramps = W.build_exits(outlines_only=False)
    for r in ramps:
        W.root.add(r["grp"])
    gauge = W.build_pool_gauge(wobble=False)
    onramp = W.build_onramp(labelled=True, dashed=False)
    pc_mach = W.build_pc_machine(label_text="pyruvate\ncarboxylase", switch="OFF")

    carts = build_queuing_carts(n=3, start_x=-3.2, spacing=0.88, y=W.ent_y)

    def _drift_carts(mob, dt):
        for c in mob:
            c.shift(RIGHT * 0.24 * dt)
            if c.get_center()[0] > MERGE_PT[0] - 0.15:
                c.move_to([-5.85, W.ent_y, 0.0])

    carts.add_updater(_drift_carts)
    W.root.add(gauge, onramp, pc_mach, carts)
    return W, pc_mach, carts


class S07Predict(SpokenScene):
    def construct(self):
        W, pc_mach, carts = _predict_backdrop()
        # Keep switch out until cue (never use set_opacity(1.0) on boxed_label)
        pc_mach.remove(W.pc_switch)
        self.add(W.root)

        self.at("needs an on")
        pc_mach.add(W.pc_switch)
        self.play(FadeIn(W.pc_switch), run_time=0.55)

        self.at("which molecule")
        q = question_card(
            "What switches the refill on?",
            y=3.18,
            color=GOLD,
            size=30,
            left=-6.0,
            max_w=5.5,
        )
        ans_box = RoundedRectangle(
            corner_radius=0.14,
            width=2.15,
            height=0.66,
            stroke_color=GOLD,
            stroke_width=3,
            fill_color=BG,
            fill_opacity=0.92,
        ).move_to([1.15, 3.18, 0.0])
        ans_q = T("?", size=34, color=TEXT, weight=BOLD).move_to(ans_box)
        self.play(FadeIn(q.question), FadeIn(ans_box), FadeIn(ans_q), run_time=0.8)
        self.finish()


class S08Think(PredictPause):
    QUESTION = "What switches the refill on?"
    CARD = {"y": 3.18, "left": -6.0, "size": 30, "max_w": 5.5, "color": GOLD}
    RING_AT = (6.0, 3.15, 0)
    SECONDS = 4.5

    def backdrop(self):
        W, _, _ = _predict_backdrop()
        ans_box = RoundedRectangle(
            corner_radius=0.14,
            width=2.15,
            height=0.66,
            stroke_color=GOLD,
            stroke_width=3,
            fill_color=BG,
            fill_opacity=0.92,
        ).move_to([1.15, 3.18, 0.0])
        ans_q = T("?", size=34, color=TEXT, weight=BOLD).move_to(ans_box)
        clock = ValueTracker(0.0)

        def _breathe(m, dt):
            clock.increment_value(dt)
            t = clock.get_value()
            s = 1.0 + 0.18 * np.exp(-((t - 2.1) / 0.45) ** 2)
            m.set_height(0.42 * s)

        ans_q.add_updater(_breathe)
        return VGroup(W.root, ans_box, ans_q)


class S09Feedforward(SpokenScene):
    def construct(self):
        W, pc_mach, carts = _predict_backdrop()
        q = question_card("What switches the refill on?", y=3.18, color=GOLD, size=30, left=-6.0, max_w=5.5)
        ans_box = RoundedRectangle(
            corner_radius=0.14,
            width=2.15,
            height=0.66,
            stroke_color=GOLD,
            stroke_width=3,
            fill_color=BG,
            fill_opacity=0.92,
        ).move_to([1.15, 3.18, 0.0])
        ans_q = T("?", size=34, color=TEXT, weight=BOLD).move_to(ans_box)
        self.add(W.root, q.question, ans_box, ans_q)

        self.at("Acetyl CoA")
        ans_tag = T("acetyl-CoA", size=26, color=YELLOW, weight=BOLD).move_to(ans_box)
        self.play(swap(ans_q, ans_tag, run_time=0.6), ans_box.animate.set_stroke(YELLOW))

        self.at("switches pyruvate carboxylase")
        sw_pos = W.pc_sw_pos
        ff_arrow = Arrow(
            np.array([sw_pos[0], W.ent_y - 0.25, 0.0]),
            np.array([sw_pos[0], W.pc_switch.get_top()[1] + 0.08, 0.0]),
            color=YELLOW,
            stroke_width=4,
            buff=0.04,
            max_tip_length_to_length_ratio=0.22,
        )
        on_sw = boxed_label("ON", color=GREEN, size=22, pad=0.14).move_to(sw_pos)
        self.play(GrowArrow(ff_arrow), run_time=0.65)
        self.play(swap(W.pc_switch, on_sw, run_time=0.5))

        refill_blk = make_block(BLUE, w=0.34, h=0.22, opacity=0.95).move_to(W.onramp_p0)
        self.add(refill_blk)
        self.play(refill_blk.animate.move_to(W.onramp_p1), W.pool.animate.set_value(0.72), run_time=0.95, rate_func=linear)
        self.remove(refill_blk)
        W.set_stack(3)

        self.at("feedforward control")
        ff_lbl = T("feedforward", size=24, color=YELLOW).next_to(ff_arrow, RIGHT, buff=0.14)
        self.play(FadeIn(ff_lbl, shift=RIGHT * 0.1), run_time=0.55)

        self.at("fuel is arriving")
        W.speed.set_value(1.10)
        for _ in range(2):
            b = make_block(BLUE, w=0.34, h=0.22, opacity=0.95).move_to(W.onramp_p0)
            self.add(b)
            self.play(
                b.animate.move_to(W.onramp_p1),
                W.pool.animate.set_value(0.85),
                run_time=0.65,
                rate_func=linear,
            )
            self.remove(b)
        W.set_stack(4)
        self.finish()


class S10Hub(SpokenScene):
    def construct(self):
        W = RoundaboutWorld(speed=0.85, pool_level=0.75, stack_count=4, show_etc="dim")
        ramps = W.build_exits(outlines_only=False)
        for r in ramps:
            self.add(r["grp"])
        trickle = W.start_exit_trickle(ramps, rate=0.38)
        gauge = W.build_pool_gauge(wobble=False)
        onramp = W.build_onramp(labelled=True, dashed=False)
        pc_mach = W.build_pc_machine(label_text="pyruvate\ncarboxylase", switch="ON")

        pc_flow = make_block(BLUE, w=0.28, h=0.18, opacity=0.92)
        pc_flow._t = 0.0
        pc_flow.add_updater(
            lambda m, dt: (
                setattr(m, "_t", (m._t + 0.55 * dt) % 1.0),
                m.move_to((1 - m._t) * W.onramp_p0 + m._t * W.onramp_p1),
            )
        )
        self.add(W.root, trickle, gauge, onramp, pc_mach, pc_flow)

        self.at("glutamine is a major source")
        glut_start = np.array([-2.65, 2.95, 0.0])
        glut_end = road_pt(ANG_GLUT, R_OUT)
        glut_line = Line(glut_start, glut_end, color=PINK, stroke_width=4)
        glut_lbl = T("glutamine · dividing cells", size=24, color=PINK).move_to([-4.45, 3.24, 0.0])
        glut_tag = T("schematic", size=22, color=TEXT).move_to([-1.25, 2.75, 0.0])
        self.play(Create(glut_line), FadeIn(glut_lbl), FadeIn(glut_tag), run_time=0.85)

        pink_stop = glut_end - 0.16 * (glut_end - glut_start) / np.linalg.norm(glut_end - glut_start)
        pink_flow = make_block(PINK, w=0.26, h=0.18, opacity=0.92)
        pink_flow._t = 0.0
        pink_flow.add_updater(
            lambda m, dt: (
                setattr(m, "_t", (m._t + 0.55 * dt) % 1.0),
                m.move_to((1 - m._t) * glut_start + m._t * pink_stop),
            )
        )
        self.add(pink_flow)

        self.at("busy hub")
        # Swap dim ETC strip for full ETC lane & block via FadeOut/FadeIn (never set_opacity(1.0))
        self.play(FadeOut(W.etc_dim_grp, run_time=0.3), FadeIn(W.etc_full_grp, run_time=0.6))

        etc_end = np.array([W.etc_block.get_left()[0] - 0.24, W.etc_start[1], 0.0])
        nadh_flow = VGroup(make_block(TEAL, w=0.30, h=0.20, opacity=0.92), make_electron_pair(ORIGIN, radius=0.045))
        nadh_flow._t = 0.0
        nadh_flow.add_updater(
            lambda m, dt: (
                setattr(m, "_t", (m._t + 0.48 * dt) % 1.0),
                m.move_to((1 - m._t) * W.etc_start + m._t * etc_end),
            )
        )
        self.add(nadh_flow)

        self.at("holds steady")
        level_y = gauge[0].get_bottom()[1] + 0.05 + 0.85 * (gauge[0].height - 0.10)
        level_line = Line(
            [GAUGE_POS[0] - 0.28, level_y, 0.0],
            [GAUGE_POS[0] + 0.28, level_y, 0.0],
            color=GOLD,
            stroke_width=3.5,
        )
        self.play(W.pool.animate.set_value(0.85), Create(level_line), run_time=0.7)
        self.finish()


class S11Return(SpokenScene):
    def construct(self):
        W = RoundaboutWorld(speed=0.80, pool_level=0.85, stack_count=4, show_etc="full", start_phase=-75.0 * DEGREES)
        ramps = W.build_exits(outlines_only=False)
        for r in ramps:
            self.add(r["grp"])
        trickle = W.start_exit_trickle(ramps, rate=0.38)
        gauge = W.build_pool_gauge(wobble=False)
        onramp = W.build_onramp(labelled=True, dashed=False)
        pc_mach = W.build_pc_machine(label_text="pyruvate\ncarboxylase", switch="ON")
        self.add(W.root, trickle, gauge, onramp, pc_mach)

        self.at("platform is reusable")
        # Highlight capsule #0 for one full clockwise turn, then lock a fresh block into station
        W.speed.set_value(TAU / 3.4)
        re_ring = always_redraw(
            lambda: Circle(radius=0.30, color=TEXT, stroke_width=3).move_to(W.road_markers[0].get_center())
        )
        self.add(re_ring)
        self.wait(3.4)
        self.remove(re_ring)
        W.speed.set_value(0.80)
        lock_pulse = SurroundingRectangle(W.station_box, corner_radius=0.16, color=TEXT, stroke_width=3.5, buff=0.06)
        self.play(FadeIn(lock_pulse), run_time=0.25)
        self.play(FadeOut(lock_pulse), run_time=0.30)

        self.at("loads electron carriers")
        etc_end = np.array([W.etc_block.get_left()[0] - 0.24, W.etc_start[1], 0.0])
        pair1 = make_electron_pair(W.etc_start, radius=0.065)
        pair2 = make_electron_pair(W.etc_start, radius=0.065)
        self.add(pair1)
        self.play(pair1.animate.move_to(etc_end), run_time=1.0, rate_func=linear)
        self.remove(pair1)
        self.add(pair2)
        self.play(pair2.animate.move_to(etc_end), run_time=0.9, rate_func=linear)
        self.remove(pair2)

        self.at("supplies builders")
        self.play(
            *[r["box"].box.animate.set_stroke(GOLD, width=4) for r in ramps],
            *[r["line"].animate.set_stroke(GOLD, width=6) for r in ramps],
            run_time=0.6,
        )
        self.play(
            *[r["box"].box.animate.set_stroke(ORANGE, width=2.5) for r in ramps],
            *[r["line"].animate.set_stroke(ORANGE, width=4) for r in ramps],
            run_time=0.7,
        )

        self.at("anaplerosis must give back")
        give_blk = make_block(BLUE, w=0.34, h=0.22, opacity=0.95).move_to(W.onramp_p0)
        self.add(give_blk)
        self.play(
            W.onramp_line.animate.set_stroke(GOLD, width=6),
            give_blk.animate.move_to(W.onramp_p1),
            run_time=1.0,
            rate_func=linear,
        )
        self.play(W.onramp_line.animate.set_stroke(BLUE, width=4), FadeOut(give_blk), run_time=0.45)
        self.finish()


class S12End(EndCard):
    LINE = "Oxaloacetate stays reusable only if what builders take gets refilled."
