# ==============================================================================
# Made All Day, Held Back Until Stress — scenes.py
# ==============================================================================
# COLOUR MAP (one colour per concept across the entire film):
#   TEAL   (#3FB8C0) : Stress responders & active outputs (p53, Nrf2, level gauge, activated genes)
#   GOLD   (#D4A843) : Restraints & shredder (MDM2 clamp, ubiquitin chain, proteasome ring, Keap1 catcher, ASK1/ER restraints)
#   RED    (#FC6255) : Stress triggers & signals (radiation break, ATM kinase, phosphate 'P' badges, electrophiles)
#   YELLOW (#F5D547) : Reactive cysteine sulfur knobs on Keap1 (electron-donor sites)
#   BLUE   (#58C4DD) : DNA / gene template & synthesis spout (nuclear DNA strands, inactive gene bars)
#   GREY   (#8B93A1) : Cell architecture & axes (plasma membrane, nuclear envelope, plot axes, schematic tag)
#   TEXT   (#E8EAF0) : Crisp labels & readouts (full opacity, >= 24 pt)
#
# CARRIED WORLD PICTURE:
#   A schematic cell cross-section (plasma membrane, dashed nucleus with DNA, left synthesis spout,
#   right spinning proteasome shredder ring, and—when quantified—a right-side ODE curve & level gauge).
#
# WHAT CHANGES IN EACH SPOKEN SCENE (and what computes it):
#   s01_hook         : Synthesis spout emits TEAL p53 blocks continuously; GOLD MDM2 clamps divert half
#                      to the spinning proteasome while a live 0 -> 20 min clock sweeps; slow BLUE gene
#                      bar creeps at bottom then fades, and one p53 releases on "let go".
#   s02_restraint    : Zoomed TEAL p53 docks onto BLUE DNA (gene lights TEAL), then GOLD MDM2 clamp
#                      slides over its gene-activation end, adds a chain of 4 GOLD ubiquitin beads,
#                      and delivers it into the spinning proteasome where it shreds into fading dots.
#   s03_turnover_math: Left cell runs constant 80/hr synthesis and 4/hr -> 1/hr shredder speed; right
#                      Plot + gauge + counter run the computed ODE dP/dt = 80 - k_d*P: flat at 20 for
#                      k_d = 4, then climbing smoothly along 80 - 60*exp(-(t-1.5)) toward 80 for k_d = 1.
#   s04_dna_break    : RED lightning snaps BLUE DNA; RED ATM lights up and fires 'P' badges onto GOLD
#                      MDM2 and TEAL p53; MDM2 opens and drifts off, gauge shoots from 20 -> 80 via
#                      80 - 60*exp(-k*t), and freed p53 lights up 'p21 (pause)' and 'DNA repair'.
#   s05_predict_q    : Synthesis spout runs while broken DNA + ATM show; then DNA break fades and varied
#                      RED chemical shapes cross the membrane and drift around a GOLD sensor block while
#                      question_card fades in at the bottom band.
#   s06_pause        : PredictPause holds the cell + drifting chemical shapes + question_card while
#                      the 4.5 s countdown ring empties.
#   s07_keap1_reveal : Electrophiles drift in cytosol while spout emits TEAL Nrf2 caught by GOLD Keap1
#                      and passed to spinning proteasome; YELLOW 'Cys' knobs emerge on Keap1 and varied
#                      RED electrophiles covalently bond to them with flashes regardless of shape.
#   s08_keap1_escape : Modified Keap1 pools fill with older Nrf2; fresh Nrf2 streams past them to the
#                      nucleus, lighting 'protective enzymes' TEAL and driving the right gauge 20 -> 80,
#                      while two bottom badges ('ASK1 + thioredoxin', 'ER sensors + BiP') lift restraints.
#   s09_closing      : TwoPanel side-by-side comparison: continuous synthesis streams in both mini-cells
#                      hold gauges at 20 until danger arrives, then left p53 frees from MDM2 via ATM
#                      phosphates and right Nrf2 bypasses modified Keap1; both gauges climb 20 -> 80.
# ==============================================================================

from bp_parts import *

# ------------------------------------------------------------------------------
# Shared carried-world geometry & builders
# ------------------------------------------------------------------------------

def _rounded_cell(x0, x1, y0, y1, nuc_center, nuc_rx, nuc_ry, with_break=False, dna_dy=0.18):
    """Build the schematic cell cross-section: plasma membrane, nucleus, and nuclear DNA."""
    w, h = x1 - x0, y1 - y0
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    outer = RoundedRectangle(
        corner_radius=0.55, width=w, height=h,
        stroke_color=GREY, stroke_width=4, fill_color=BLUE, fill_opacity=0.14,
    ).move_to([cx, cy, 0])
    inner = RoundedRectangle(
        corner_radius=0.48, width=w - 0.14, height=h - 0.14,
        stroke_color=GREY, stroke_width=1.5, stroke_opacity=0.55, fill_opacity=0.0,
    ).move_to([cx, cy, 0])

    nuc_base = Ellipse(width=2 * nuc_rx, height=2 * nuc_ry, stroke_color=GREY, stroke_width=2.5)
    nuc_env = DashedVMobject(nuc_base, num_dashes=28, dashed_ratio=0.58).move_to([nuc_center[0], nuc_center[1], 0])
    nuc_fill = Ellipse(
        width=2 * nuc_rx, height=2 * nuc_ry,
        stroke_width=0, fill_color=BLUE, fill_opacity=0.18,
    ).move_to([nuc_center[0], nuc_center[1], 0])

    dna_y = nuc_center[1] + dna_dy
    dna_w = min(2.6, 1.32 * nuc_rx)
    dna_x0 = nuc_center[0] - dna_w / 2
    dna_x1 = nuc_center[0] + dna_w / 2
    dna = VGroup()
    if not with_break:
        s1 = Line([dna_x0, dna_y + 0.10, 0], [dna_x1, dna_y + 0.10, 0], color=BLUE, stroke_width=4)
        s2 = Line([dna_x0, dna_y - 0.10, 0], [dna_x1, dna_y - 0.10, 0], color=BLUE, stroke_width=4)
        dna.add(s1, s2)
        for rx in np.linspace(dna_x0 + 0.18, dna_x1 - 0.18, 8):
            dna.add(Line([rx, dna_y - 0.10, 0], [rx, dna_y + 0.10, 0], color=BLUE, stroke_width=2.5))
    else:
        gap = 0.24
        mid = nuc_center[0]
        l1 = Line([dna_x0, dna_y + 0.10, 0], [mid - gap, dna_y + 0.16, 0], color=BLUE, stroke_width=4)
        l2 = Line([dna_x0, dna_y - 0.10, 0], [mid - gap, dna_y - 0.04, 0], color=BLUE, stroke_width=4)
        r1 = Line([mid + gap, dna_y + 0.16, 0], [dna_x1, dna_y + 0.10, 0], color=BLUE, stroke_width=4)
        r2 = Line([mid + gap, dna_y - 0.04, 0], [dna_x1, dna_y - 0.10, 0], color=BLUE, stroke_width=4)
        dna.add(l1, l2, r1, r2)
        for rx in np.linspace(dna_x0 + 0.18, mid - gap - 0.12, 3):
            dna.add(Line([rx, dna_y - 0.08, 0], [rx, dna_y + 0.12, 0], color=BLUE, stroke_width=2.5))
        for rx in np.linspace(mid + gap + 0.12, dna_x1 - 0.18, 3):
            dna.add(Line([rx, dna_y - 0.08, 0], [rx, dna_y + 0.12, 0], color=BLUE, stroke_width=2.5))

    g = VGroup(outer, inner, nuc_fill, nuc_env, dna)
    g.outer = outer
    g.nuc_env = nuc_env
    g.dna = dna
    g.nuc_center = np.array([nuc_center[0], nuc_center[1], 0.0])
    return g


def _synthesis_spout(pos, color=TEAL, scale=1.0):
    """Left-side synthesis nozzle from which responder blocks emerge."""
    p = np.array([pos[0], pos[1], 0.0])
    body = RoundedRectangle(
        corner_radius=0.14 * scale, width=0.92 * scale, height=0.60 * scale,
        stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.28,
    ).move_to(p)
    nozzle = Polygon(
        p + np.array([0.44, 0.21, 0]) * scale,
        p + np.array([0.72, 0.13, 0]) * scale,
        p + np.array([0.72, -0.13, 0]) * scale,
        p + np.array([0.44, -0.21, 0]) * scale,
        stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.38,
    )
    g = VGroup(body, nozzle)
    g.tip = p + np.array([0.82 * scale, 0.0, 0.0])
    return g


def _proteasome_ring(pos, radius=0.62):
    """Spinning GOLD proteasome shredder ring composed of segmented arcs."""
    c = np.array([pos[0], pos[1], 0.0])
    ring = VGroup()
    n_seg = 6
    for i in range(n_seg):
        a0 = i * TAU / n_seg + 0.08
        span = TAU / n_seg - 0.16
        arc = Arc(
            radius=radius, start_angle=a0, angle=span, arc_center=c,
            stroke_color=GOLD, stroke_width=10,
        )
        inner_arc = Arc(
            radius=radius * 0.68, start_angle=a0 + 0.06, angle=span - 0.12, arc_center=c,
            stroke_color=GOLD, stroke_width=4, stroke_opacity=0.75,
        )
        ring.add(arc, inner_arc)
    core = Circle(radius=radius * 0.45, stroke_width=0, fill_color=GOLD, fill_opacity=0.16).move_to(c)
    ring.add(core)
    ring.center_pt = c
    return ring


def _spin_ring(ring, speed_tracker):
    """Attach continuous angular rotation to a proteasome ring driven by a ValueTracker (rad/s)."""
    def _upd(mob, dt):
        mob.rotate(speed_tracker.get_value() * dt, about_point=mob.get_center())
    ring.add_updater(_upd)
    return ring


def _stream_block(pos=ORIGIN, scale=0.62):
    """Unlabelled TEAL responder block for continuous streams (Polygon tab avoids box heuristics)."""
    body = RoundedRectangle(
        corner_radius=0.10 * scale, width=0.58 * scale, height=0.36 * scale,
        stroke_color=TEAL, stroke_width=2.6, fill_color=TEAL, fill_opacity=0.48,
    )
    w_t, h_t = 0.20 * scale, 0.20 * scale
    act_end = Polygon(
        [0, h_t / 2, 0], [w_t, h_t / 2, 0], [w_t, -h_t / 2, 0], [0, -h_t / 2, 0],
        stroke_color=TEAL, stroke_width=2.4, fill_color=TEAL, fill_opacity=0.72,
    ).next_to(body, RIGHT, buff=0.0)
    g = VGroup(body, act_end)
    g.body = body
    g.act_end = act_end
    g.move_to(pos)
    return g


def _hero_block(label, pos=ORIGIN, font_size=26, scale=1.0):
    """Generously padded TEAL responder block with crisp internal label and Polygon active end."""
    txt = T(label, size=font_size, color=TEXT, weight=BOLD)
    w = max(1.18 * scale, txt.width + 0.56)
    h = max(0.62 * scale, txt.height + 0.34)
    body = RoundedRectangle(
        corner_radius=0.12, width=w, height=h,
        stroke_color=TEAL, stroke_width=3.0, fill_color=TEAL, fill_opacity=0.32,
    )
    w_t, h_t = 0.28 * scale, 0.30 * scale
    act_end = Polygon(
        [0, h_t / 2, 0], [w_t, h_t / 2, 0], [w_t, -h_t / 2, 0], [0, -h_t / 2, 0],
        stroke_color=TEAL, stroke_width=2.8, fill_color=TEAL, fill_opacity=0.65,
    ).next_to(body, RIGHT, buff=0.0)
    txt.move_to(body.get_center())
    g = VGroup(body, act_end, txt)
    g.body = body
    g.act_end = act_end
    g.label = txt
    g.move_to(pos)
    return g


def _mdm2_clamp(pos=ORIGIN, open_amt=0.0, scale=1.0):
    """GOLD C-shaped MDM2 clamp whose jaws open with open_amt (0=closed, 1=wide open)."""
    gap = 0.08 + 0.24 * open_amt
    top_jaw = RoundedRectangle(
        corner_radius=0.07, width=0.44 * scale, height=0.15 * scale,
        stroke_color=GOLD, stroke_width=2.6, fill_color=GOLD, fill_opacity=0.38,
    ).shift(UP * (0.14 + gap) * scale)
    bot_jaw = RoundedRectangle(
        corner_radius=0.07, width=0.44 * scale, height=0.15 * scale,
        stroke_color=GOLD, stroke_width=2.6, fill_color=GOLD, fill_opacity=0.38,
    ).shift(DOWN * (0.14 + gap) * scale)
    spine = RoundedRectangle(
        corner_radius=0.07, width=0.18 * scale, height=(0.44 + 2 * gap) * scale,
        stroke_color=GOLD, stroke_width=2.6, fill_color=GOLD, fill_opacity=0.48,
    ).shift(RIGHT * 0.17 * scale)
    g = VGroup(spine, top_jaw, bot_jaw).move_to(pos)
    return g


def _keap1_catcher(pos=ORIGIN, with_cys=False, scale=1.0):
    """GOLD Keap1 catcher cradle, optionally studded with 3 YELLOW sulfur-tipped Cys knobs."""
    cup = Polygon(
        [-0.36, 0.30, 0], [-0.14, 0.30, 0], [-0.14, -0.10, 0],
        [0.14, -0.10, 0], [0.14, 0.30, 0], [0.36, 0.30, 0],
        [0.36, -0.34, 0], [-0.36, -0.34, 0],
        stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.30,
    ).scale(scale)
    g = VGroup(cup)
    knobs = VGroup()
    if with_cys:
        offsets = [(-0.42, 0.12), (0.0, -0.42), (0.42, 0.12)]
        for ox, oy in offsets:
            stalk = Line(
                [ox * 0.72 * scale, oy * 0.72 * scale, 0],
                [ox * scale, oy * scale, 0],
                color=YELLOW, stroke_width=3.5,
            )
            tip = Dot([ox * scale, oy * scale, 0], radius=0.09 * scale, color=YELLOW, stroke_color=GOLD, stroke_width=1.5)
            knobs.add(VGroup(stalk, tip))
        g.add(knobs)
    g.cup = cup
    g.knobs = knobs
    g.move_to(pos)
    return g


def _electrophile_shape(kind, pos=ORIGIN, scale=0.22):
    """Varied RED geometric hazard shapes (no molecular structures)."""
    if kind % 4 == 0:
        m = Triangle(stroke_color=RED, stroke_width=2.5, fill_color=RED, fill_opacity=0.58)
    elif kind % 4 == 1:
        m = RegularPolygon(5, stroke_color=RED, stroke_width=2.5, fill_color=RED, fill_opacity=0.58)
    elif kind % 4 == 2:
        m = Square(stroke_color=RED, stroke_width=2.5, fill_color=RED, fill_opacity=0.58).rotate(PI / 4)
    else:
        m = Polygon([-1, -0.6, 0], [1, -0.2, 0], [0.3, 0.9, 0], [-0.8, 0.4, 0],
                    stroke_color=RED, stroke_width=2.5, fill_color=RED, fill_opacity=0.58)
    m.set_height(scale)
    m.move_to(pos)
    return m


def _phosphate_badge(pos=ORIGIN, scale=1.0):
    """Glowing RED 'P' phosphate badge with generous circle clearance (>= 22 pt)."""
    c = Circle(radius=0.25 * scale, stroke_color=RED, stroke_width=2.5, fill_color=RED, fill_opacity=0.45)
    txt = T("P", size=max(22, int(round(22 * scale))), color=TEXT, weight=BOLD).move_to(c)
    return VGroup(c, txt).move_to(pos)


def _level_gauge(tracker, x=5.3, y0=-1.6, y1=1.6, max_val=100.0, title="p53", unit="units", bar_w=0.68):
    """Vertical TEAL level gauge (0..max_val) + live numeric readout driven by one ValueTracker."""
    h = y1 - y0
    frame = RoundedRectangle(
        corner_radius=0.10, width=bar_w, height=h,
        stroke_color=GREY, stroke_width=3, fill_color=BG, fill_opacity=0.92,
    ).move_to([x, (y0 + y1) / 2, 0])

    def _bar():
        v = float(np.clip(tracker.get_value(), 1.0, max_val))
        bh = h * (v / max_val)
        return RoundedRectangle(
            corner_radius=0.06, width=bar_w - 0.10, height=max(0.06, bh - 0.06),
            stroke_width=0, fill_color=TEAL, fill_opacity=0.85,
        ).move_to([x, y0 + bh / 2, 0])

    bar = always_redraw(_bar)
    ticks = VGroup()
    for val in (0, 20, 80, 100):
        ty = y0 + h * (val / max_val)
        tk = Line([x - bar_w / 2 - 0.08, ty, 0], [x - bar_w / 2, ty, 0], color=GREY, stroke_width=2.5)
        tl = M(str(val), size=22, color=GREY).next_to(tk, LEFT, buff=0.08)
        ticks.add(tk, tl)

    num_y = y1 + 0.38
    ttl_y = y1 + 0.82
    ttl = T(title, size=26, color=TEAL).move_to([x, ttl_y, 0])
    fmt = "{:.0f} " + unit if unit else "{:.0f}"
    num = counter(fmt, tracker, at=[x, num_y, 0], size=26, color=TEXT)
    g = VGroup(frame, bar, ticks, ttl, num)
    g.frame = frame
    g.num = num
    g.ttl = ttl
    return g


def _start_stream(scene, spout_tip, shredder_pt, rng, shred_fraction=0.5, end_pt=None, spawn_period=0.55, pscale=0.62, use_clamp=True, arc_y=0.14, via_pt=None, curve_x=0.0):
    """Spawn a continuous deterministic stream of unlabelled TEAL blocks from the spout."""
    stream = VGroup()
    target_end = np.array([spout_tip[0] + 2.35, spout_tip[1] + 0.85, 0.0]) if end_pt is None else np.array(end_pt, dtype=float)
    via = None if via_pt is None else np.array(via_pt, dtype=float)
    state = {"active": True, "shred_fraction": shred_fraction, "t": 0.0, "spawn_i": 0, "particles": [], "end_pt": target_end, "curve_x": curve_x}
    scene.add(stream)

    def _upd(mob, dt):
        state["t"] += dt
        while state["active"] and state["t"] >= state["spawn_i"] * spawn_period:
            idx = state["spawn_i"]
            state["spawn_i"] += 1
            y_off = float(rng.uniform(-0.14, 0.14))
            blk = _stream_block(spout_tip + np.array([0.0, y_off, 0.0]), scale=pscale)
            sf = state["shred_fraction"]
            if sf >= 0.45:
                to_shred = (idx % 2 == 1)
            elif sf >= 0.20:
                to_shred = (idx % 4 == 3)
            else:
                to_shred = False
            clamp = _mdm2_clamp(blk.get_center() + RIGHT * (0.28 * pscale / 0.62), scale=pscale) if (use_clamp and to_shred and shredder_pt is not None) else None
            grp = VGroup(blk) if clamp is None else VGroup(blk, clamp)
            mob.add(grp)
            state["particles"].append({
                "grp": grp, "to_shred": to_shred, "age": 0.0, "y_off": y_off,
                "end_pt": state["end_pt"].copy(), "curve_x": state["curve_x"],
            })

        alive = []
        for p in state["particles"]:
            p["age"] += dt
            if p["to_shred"] and shredder_pt is not None:
                if via is not None:
                    frac = min(1.0, p["age"] / 2.8)
                    if frac < 0.50:
                        u = frac / 0.50
                        pos = spout_tip * (1 - u) + via * u
                    else:
                        u = (frac - 0.50) / 0.50
                        pos = via * (1 - u) + shredder_pt * u + UP * (0.28 * np.sin(u * PI))
                else:
                    frac = min(1.0, p["age"] / 2.4)
                    pos = spout_tip * (1 - frac) + shredder_pt * frac + UP * (arc_y * np.sin(frac * PI))
                p["grp"].move_to(pos)
                if frac > 0.78:
                    p["grp"].set_opacity(max(0.0, 1.0 - (frac - 0.78) / 0.22))
            else:
                frac = min(1.0, p["age"] / 2.8)
                dest = p["end_pt"] + np.array([0.0, p["y_off"], 0.0])
                pos = spout_tip * (1 - frac) + dest * frac + RIGHT * (p["curve_x"] * np.sin(frac * PI))
                p["grp"].move_to(pos)
                if frac > 0.78:
                    p["grp"].set_opacity(max(0.0, 1.0 - (frac - 0.78) / 0.22))
            if frac < 1.0:
                alive.append(p)
            else:
                mob.remove(p["grp"])
        state["particles"] = alive

    stream.add_updater(_upd)
    return stream, state


# ------------------------------------------------------------------------------
# s00_title: Standard TitleCard
# ------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Stress Signals: p38 and JNK, p53, Unfolded Proteins and Oxidants"
    TITLE = "Made All Day, Held Back Until Stress"


# ------------------------------------------------------------------------------
# s01_hook: Made all day, half shredded within ~20 min
# ------------------------------------------------------------------------------
class S01Hook(SpokenScene):
    def construct(self):
        rng = np.random.default_rng(7)
        cell = _rounded_cell(-5.8, 3.6, -2.15, 2.95, nuc_center=(-3.2, 1.65), nuc_rx=2.05, nuc_ry=0.98, dna_dy=0.25)
        nuc_lab = T("nucleus", size=24, color=BLUE).move_to([-3.95, 1.25, 0])
        spout = _synthesis_spout([-4.55, -0.55])
        spout_lab = T("p53 synthesis", size=26, color=TEAL).next_to(spout, DOWN, buff=0.20)
        shredder = _proteasome_ring([1.95, -0.70], radius=0.62)
        shred_lab = T("proteasome", size=26, color=GOLD).next_to(shredder, DOWN, buff=0.20)

        spin_spd = ValueTracker(2.0)
        _spin_ring(shredder, spin_spd)

        clock_c = np.array([5.15, 1.15, 0.0])
        t_min = ValueTracker(0.0)
        clock_bg = Circle(radius=0.88, color=GREY, stroke_width=4, fill_color=BG, fill_opacity=0.85).move_to(clock_c)
        clock_arc = always_redraw(lambda: AnnularSector(
            inner_radius=0.0, outer_radius=0.84,
            start_angle=PI / 2, angle=-max(0.002, PI * (t_min.get_value() / 20.0)),
            arc_center=clock_c, color=GOLD, fill_opacity=0.55,
        ))
        clock_hand = always_redraw(lambda: Line(
            clock_c,
            clock_c + 0.72 * np.array([
                np.sin(PI * (t_min.get_value() / 20.0)),
                np.cos(PI * (t_min.get_value() / 20.0)),
                0.0,
            ]),
            color=TEXT, stroke_width=4,
        ))
        clock_num = counter("{:.0f} min", t_min, at=clock_c + DOWN * 1.25, size=28, color=TEXT)
        batch_lab = always_redraw(lambda: M(
            f"shredded: {50 * min(1.0, t_min.get_value() / 20.0):.0f}%",
            size=24, color=GOLD,
        ).move_to(clock_c + DOWN * 1.72))

        self.play(
            FadeIn(cell), FadeIn(nuc_lab), FadeIn(spout), FadeIn(spout_lab),
            FadeIn(shredder), FadeIn(shred_lab),
            run_time=0.8,
        )
        self.add(scope_tag("schematic"))
        stream, st = _start_stream(
            self, spout.tip, shredder.center_pt, rng, shred_fraction=0.5,
            end_pt=[-1.8, -0.35, 0],
        )

        self.at("shred half")
        self.play(FadeIn(clock_bg), FadeIn(clock_num), FadeIn(batch_lab), run_time=0.4)
        self.add(clock_arc, clock_hand)
        self.play(t_min.animate.set_value(20.0), run_time=1.8, rate_func=linear)

        self.at("why make")
        q_badge = T("why destroy it?", size=28, color=GOLD).move_to([0.55, 2.20, 0])
        self.play(FadeIn(q_badge), run_time=0.5)

        self.at("cannot wait")
        self.play(FadeOut(q_badge), run_time=0.35)
        bar_bg = RoundedRectangle(
            corner_radius=0.08, width=6.2, height=0.34,
            stroke_color=BLUE, stroke_width=2.5, fill_color=BG, fill_opacity=0.9,
        ).move_to([-1.2, -3.08, 0])
        prog = ValueTracker(0.02)
        bar_fill = always_redraw(lambda: RoundedRectangle(
            corner_radius=0.06, width=max(0.08, 6.08 * prog.get_value()), height=0.22,
            stroke_width=0, fill_color=BLUE, fill_opacity=0.68,
        ).align_to(bar_bg.get_left() + RIGHT * 0.06, LEFT).set_y(bar_bg.get_center()[1]))
        bar_lab = T("new gene -> mRNA -> protein (slow)", size=24, color=TEXT).next_to(bar_bg, UP, buff=0.14)
        self.play(FadeIn(bar_bg), FadeIn(bar_lab), run_time=0.4)
        self.add(bar_fill)
        self.play(prog.animate.set_value(0.24), run_time=2.6, rate_func=linear)

        self.at("responder already exists")
        self.play(FadeOut(bar_bg), FadeOut(bar_fill), FadeOut(bar_lab), run_time=0.45)
        ready_p53 = _hero_block("p53", pos=[-0.95, 0.25, 0], font_size=26, scale=1.0)
        ready_clamp = _mdm2_clamp(ready_p53.act_end.get_center() + RIGHT * 0.26, open_amt=0.0, scale=1.0)
        self.play(FadeIn(ready_p53), FadeIn(ready_clamp), run_time=0.5)

        self.at("let go")
        st["shred_fraction"] = 0.0
        open_clamp = _mdm2_clamp(ready_clamp.get_center() + RIGHT * 0.65, open_amt=1.0, scale=1.0)
        self.play(
            Transform(ready_clamp, open_clamp),
            ready_p53.animate.move_to([-2.30, 1.32, 0]),
            run_time=0.9,
        )
        self.finish()


# ------------------------------------------------------------------------------
# s02_restraint: Zoomed p53 ends, MDM2 clamp + ubiquitin chain -> proteasome
# ------------------------------------------------------------------------------
class S02Restraint(SpokenScene):
    def construct(self):
        cell = _rounded_cell(-6.1, 6.1, -2.55, 3.25, nuc_center=(-2.6, 1.98), nuc_rx=3.15, nuc_ry=1.15, dna_dy=0.12)
        dna_lab = T("DNA", size=26, color=BLUE).move_to([-4.65, 2.10, 0])
        gene_bar = RoundedRectangle(
            corner_radius=0.08, width=1.65, height=0.32,
            stroke_color=BLUE, stroke_width=2.5, fill_color=BLUE, fill_opacity=0.24,
        ).move_to([-1.25, 2.10, 0])
        gene_lab = T("target gene", size=24, color=TEXT).next_to(gene_bar, UP, buff=0.14)

        p53_core = RoundedRectangle(
            corner_radius=0.14, width=1.95, height=0.92,
            stroke_color=TEAL, stroke_width=3.5, fill_color=TEAL, fill_opacity=0.30,
        )
        p53_dna_end = RoundedRectangle(
            corner_radius=0.10, width=0.65, height=0.72,
            stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.50,
        ).next_to(p53_core, LEFT, buff=-0.05)
        p53_act_end = RoundedRectangle(
            corner_radius=0.10, width=0.68, height=0.62,
            stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.68,
        ).next_to(p53_core, RIGHT, buff=-0.05)
        p53_txt = T("p53", size=30, color=TEXT, weight=BOLD).move_to(p53_core)
        p53 = VGroup(p53_core, p53_dna_end, p53_act_end, p53_txt).move_to([-1.5, -0.95, 0])

        end_dna_lab = T("DNA-binding end", size=24, color=TEAL).next_to(p53_dna_end, DOWN, buff=0.28).shift(LEFT * 0.55)
        end_act_lab = T("gene-activation end", size=24, color=TEAL).next_to(p53_act_end, DOWN, buff=0.28).shift(RIGHT * 0.65)

        shredder = _proteasome_ring([4.35, -0.95], radius=0.82)
        shred_lab = T("proteasome", size=26, color=GOLD).next_to(shredder, DOWN, buff=0.20)
        spin_spd = ValueTracker(2.0)
        _spin_ring(shredder, spin_spd)

        self.play(
            FadeIn(cell), FadeIn(dna_lab), FadeIn(gene_bar), FadeIn(gene_lab),
            FadeIn(p53), FadeIn(end_dna_lab), FadeIn(end_act_lab),
            FadeIn(shredder), FadeIn(shred_lab),
            run_time=1.0,
        )
        self.add(scope_tag("schematic"))

        self.at("binds dna")
        self.play(FadeOut(end_dna_lab), FadeOut(end_act_lab), run_time=0.4)
        self.play(p53.animate.move_to([-2.3, 1.42, 0]), run_time=0.9)
        gene_on = gene_bar.copy().set_fill(TEAL, opacity=0.75).set_stroke(TEAL)
        on_lab = T("gene ON", size=24, color=TEAL).next_to(gene_bar, UP, buff=0.14)
        self.play(Transform(gene_bar, gene_on), swap(gene_lab, on_lab, run_time=0.6), run_time=0.7)
        self.wait(0.6)

        self.at("a partner called")
        gene_off_lab = T("target gene", size=24, color=TEXT).next_to(gene_bar, UP, buff=0.14)
        gene_off = gene_bar.copy().set_fill(BLUE, opacity=0.24).set_stroke(BLUE)
        mdm2 = _mdm2_clamp([1.8, -0.95, 0], open_amt=0.4, scale=1.65)
        mdm2_lab = T("MDM2", size=28, color=GOLD).next_to(mdm2, UP, buff=0.22)
        self.play(
            p53.animate.move_to([-1.5, -0.95, 0]),
            Transform(gene_bar, gene_off),
            swap(on_lab, gene_off_lab, run_time=0.5),
            FadeIn(mdm2), FadeIn(mdm2_lab),
            run_time=1.0,
        )

        self.at("grips it")
        closed_mdm2 = _mdm2_clamp([p53.get_center()[0] + 1.48, p53.get_center()[1], 0], open_amt=0.0, scale=1.65)
        self.play(
            Transform(mdm2, closed_mdm2),
            mdm2_lab.animate.next_to(closed_mdm2, UP, buff=0.22),
            run_time=0.9,
        )
        covered_lab = T("active end covered", size=26, color=GOLD).next_to(closed_mdm2, DOWN, buff=0.24)
        self.play(FadeIn(covered_lab), run_time=0.6)

        self.at("tags it with ubiquitin")
        ub_chain = VGroup()
        for k in range(4):
            bead = Dot(radius=0.13, color=GOLD, stroke_color=TEXT, stroke_width=1.5)
            bead.move_to(p53.get_top() + UP * (0.24 + k * 0.27) + LEFT * 0.15)
            ub_chain.add(bead)
        ub_lab = T("ubiquitin", size=26, color=GOLD).next_to(ub_chain, LEFT, buff=0.22)
        self.play(
            LaggedStart(*[FadeIn(b, scale=1.3) for b in ub_chain], lag_ratio=0.18),
            FadeIn(ub_lab),
            FadeOut(covered_lab),
            run_time=1.2,
        )

        self.at("sending proteins")
        cargo = VGroup(p53_core, p53_dna_end, p53_act_end, mdm2, ub_chain)
        self.play(FadeOut(mdm2_lab), FadeOut(ub_lab), FadeOut(p53_txt), run_time=0.35)
        self.play(cargo.animate.scale(0.55).move_to(shredder.center_pt), run_time=1.2)
        rng = np.random.default_rng(11)
        dots = VGroup(*[
            Dot(
                shredder.center_pt + np.array([rng.uniform(-0.35, 0.35), rng.uniform(-0.35, 0.35), 0]),
                radius=0.06, color=TEAL,
            )
            for _ in range(12)
        ])
        self.play(FadeOut(cargo), FadeIn(dots), run_time=0.45)
        self.play(
            *[d.animate.shift(np.array([rng.uniform(-0.5, 0.5), rng.uniform(-0.5, 0.5), 0])).set_opacity(0.05) for d in dots],
            run_time=1.1,
        )
        self.finish()


# ------------------------------------------------------------------------------
# s03_turnover_math: Steady state = synthesis / destruction; 80/4=20 -> 80/1=80
# ------------------------------------------------------------------------------
class S03TurnoverMath(SpokenScene):
    def construct(self):
        rng = np.random.default_rng(19)
        cell = _rounded_cell(-6.2, -0.35, -2.35, 2.95, nuc_center=(-4.25, 1.75), nuc_rx=1.45, nuc_ry=0.72)
        nuc_lab = T("nucleus", size=24, color=BLUE).move_to([-4.25, 1.32, 0])
        spout = _synthesis_spout([-5.30, -0.45])
        spout_lab = T("synthesis", size=24, color=TEAL).move_to([-4.40, -1.38, 0])
        shredder = _proteasome_ring([-1.90, -0.80], radius=0.56)
        shred_lab = T("destruction", size=24, color=GOLD).next_to(shredder, DOWN, buff=0.22)
        spin_spd = ValueTracker(2.8)
        _spin_ring(shredder, spin_spd)

        formula = VGroup(
            T("level", size=28, color=TEAL),
            T("=", size=28, color=TEXT),
            T("synthesis", size=28, color=BLUE),
            T("÷", size=28, color=TEXT),
            T("destruction", size=28, color=GOLD),
        ).arrange(RIGHT, buff=0.14).move_to([3.0, 3.05, 0])

        def p_curve(t):
            if t <= 1.5:
                return 20.0
            return 80.0 - 60.0 * np.exp(-1.0 * (t - 1.5))

        P = Plot(
            box=(0.75, 4.35, -1.65, 1.55),
            xr=(0, 7.0), yr=(0, 100),
            xticks=[0, 2, 4, 6],
            yticks=[(0, "0"), (20, "20"), (80, "80"), (100, "100")],
            xlabel="time (hr)", ylabel="schematic units",
            size=22, label_size=24,
        )
        t_val = ValueTracker(0.0)
        p_val = ValueTracker(20.0)
        p_val.add_updater(lambda m: m.set_value(p_curve(t_val.get_value())))

        live = P.live_curve(p_curve, t_val, color=TEAL, width=5)
        dot = P.dot(lambda: t_val.get_value(), lambda: p_curve(t_val.get_value()), color=TEXT, ring=TEAL, radius=0.10)
        gauge = _level_gauge(p_val, x=5.55, y0=-1.65, y1=1.55, max_val=100.0, title="p53", unit="")

        self.play(
            FadeIn(cell), FadeIn(nuc_lab), FadeIn(spout), FadeIn(spout_lab),
            FadeIn(shredder), FadeIn(shred_lab),
            Create(P),
            run_time=1.0,
        )
        self.add(scope_tag("schematic units"), p_val)
        stream, st = _start_stream(self, spout.tip, shredder.center_pt, rng, shred_fraction=0.5)

        self.at("at balance")
        bal_lab = T("making = destroying", size=24, color=TEXT).move_to([-2.3, 0.72, 0])
        self.play(FadeIn(bal_lab), run_time=0.7)

        self.at("protein level equals")
        self.play(FadeOut(bal_lab), FadeIn(formula), run_time=0.9)

        eq_syn = M("80", size=30, color=BLUE).move_to([1.95, 2.38, 0])
        eq_div = M("÷", size=30, color=TEXT).next_to(eq_syn, RIGHT, buff=0.18)
        eq_kd = M("4", size=30, color=GOLD).next_to(eq_div, RIGHT, buff=0.18)
        eq_eq = M("=", size=30, color=TEXT).next_to(eq_kd, RIGHT, buff=0.18)
        eq_res = M("20", size=30, color=TEAL).next_to(eq_eq, RIGHT, buff=0.18)

        self.at("suppose synthesis adds")
        spout_lab_num = T("synthesis: 80 /hr", size=24, color=TEAL).move_to(spout_lab)
        self.play(FadeIn(eq_syn), swap(spout_lab, spout_lab_num, run_time=0.6), run_time=0.6)

        self.at("destruction constant is")
        shred_lab_num = T("destruction: 4 /hr", size=24, color=GOLD).move_to(shred_lab)
        self.play(FadeIn(eq_div), FadeIn(eq_kd), swap(shred_lab, shred_lab_num, run_time=0.6), run_time=0.6)

        self.at("leaves 20 units")
        self.play(FadeIn(eq_eq), FadeIn(eq_res), FadeIn(gauge), run_time=0.5)
        self.add(live, dot)
        self.play(t_val.animate.set_value(1.5), run_time=1.5, rate_func=linear)

        self.at("cut the constant")
        eq_kd_new = M("1", size=30, color=GOLD).move_to(eq_kd)
        eq_q = M("?", size=30, color=TEAL).move_to(eq_res)
        shred_lab_new = T("destruction: 1 /hr", size=24, color=GOLD).move_to(shred_lab_num)
        st["shred_fraction"] = 0.25
        ref80 = P.hline(80, None, TEAL)
        t_mid = 1.5 + 5.5 * (0.5 / 3.4)
        self.play(
            spin_spd.animate.set_value(0.7),
            swap(eq_kd, eq_kd_new, run_time=0.5),
            swap(eq_res, eq_q, run_time=0.5),
            swap(shred_lab_num, shred_lab_new, run_time=0.5),
            FadeIn(ref80),
            t_val.animate.set_value(t_mid),
            run_time=0.5,
            rate_func=linear,
        )
        self.play(t_val.animate.set_value(7.0), run_time=2.9, rate_func=linear)

        self.at("gives 80 units")
        eq_res_new = M("80", size=30, color=TEAL).move_to(eq_res)
        self.play(swap(eq_q, eq_res_new, run_time=0.4), run_time=0.4)
        self.finish()


# ------------------------------------------------------------------------------
# s04_dna_break: Radiation snaps DNA -> ATM -> P on MDM2 & p53 -> gauge 20->80
# ------------------------------------------------------------------------------
class S04DnaBreak(SpokenScene):
    def construct(self):
        rng = np.random.default_rng(23)
        cell = _rounded_cell(-6.0, 3.3, -2.25, 3.05, nuc_center=(-1.90, 1.84), nuc_rx=3.85, nuc_ry=1.12, with_break=False, dna_dy=0.36)
        cell_broken = _rounded_cell(-6.0, 3.3, -2.25, 3.05, nuc_center=(-1.90, 1.84), nuc_rx=3.85, nuc_ry=1.12, with_break=True, dna_dy=0.36)
        cell.dna.shift(LEFT * 1.40)
        cell_broken.dna.shift(LEFT * 1.40)

        # Lower stream lane (y = -1.10) well below hero p53 + MDM2
        spout = _synthesis_spout([-4.75, -1.10])
        spout_lab = T("p53 synthesis", size=24, color=TEAL).next_to(spout, DOWN, buff=0.18)
        shredder = _proteasome_ring([1.95, -1.10], radius=0.56)
        shred_lab = T("proteasome", size=24, color=GOLD).next_to(shredder, DOWN, buff=0.18)
        spin_spd = ValueTracker(2.4)
        _spin_ring(shredder, spin_spd)

        p_val = ValueTracker(20.0)
        gauge = _level_gauge(p_val, x=5.20, y0=-1.65, y1=1.65, max_val=100.0, title="p53", unit="units")

        # Hero complex sits cleanly in mid-cytosol above the lower stream lane
        p53 = _hero_block("p53", pos=[-1.65, -0.04, 0], font_size=24, scale=0.90)
        mdm2 = _mdm2_clamp(p53.act_end.get_center() + RIGHT * 0.30, open_amt=0.0, scale=1.08)
        mdm2_lab = T("MDM2", size=24, color=GOLD).next_to(mdm2, RIGHT, buff=0.22)

        self.play(
            FadeIn(cell), FadeIn(spout), FadeIn(spout_lab),
            FadeIn(shredder), FadeIn(shred_lab),
            FadeIn(gauge), FadeIn(p53), FadeIn(mdm2), FadeIn(mdm2_lab),
            run_time=0.8,
        )
        self.add(scope_tag("schematic"))
        stream, st = _start_stream(
            self, spout.tip, shredder.center_pt, rng, shred_fraction=0.5,
            end_pt=[-1.8, -1.00, 0], spawn_period=0.58, pscale=0.58,
        )

        bolt = Polygon(
            [-1.95, 2.85, 0], [-2.35, 2.38, 0], [-2.12, 2.38, 0],
            [-2.48, 1.98, 0], [-2.18, 2.26, 0], [-2.40, 2.26, 0],
            stroke_color=RED, stroke_width=3, fill_color=RED, fill_opacity=0.88,
        ).shift(LEFT * 0.95)
        rad_lab = T("radiation", size=26, color=RED).next_to(bolt, RIGHT, buff=0.18).align_to(bolt, UP)
        self.play(FadeIn(bolt), FadeIn(rad_lab), run_time=0.4)
        self.play(Transform(cell, cell_broken), run_time=0.55)
        self.play(FadeOut(bolt), FadeOut(rad_lab), run_time=0.35)

        self.at("that break activates")
        atm = boxed_label("ATM", color=RED, size=24).move_to([-3.70, 1.50, 0])
        self.play(FadeIn(atm, scale=1.12), run_time=0.75)

        self.at("adds phosphate tags")
        p_atm = _phosphate_badge(atm.get_right() + RIGHT * 0.35, scale=1.0)
        self.play(FadeIn(p_atm, scale=1.15), run_time=0.65)

        self.at("downstream kinases tag")
        p_on_p53 = _phosphate_badge(p53.body.get_left() + LEFT * 0.40, scale=1.0)
        p_on_mdm2 = _phosphate_badge([mdm2.get_center()[0] + 0.15, 0.56, 0], scale=0.88)
        p1 = _phosphate_badge([-3.55, 0.46, 0], scale=1.0)
        p2 = _phosphate_badge([-2.95, 0.46, 0], scale=0.88)
        self.play(FadeOut(p_atm), run_time=0.25)
        self.play(FadeIn(p1), FadeIn(p2), run_time=0.25)
        self.play(p1.animate.move_to(p_on_p53), p2.animate.move_to(p_on_mdm2), run_time=1.0)

        self.at("grip loosens")
        open_mdm2 = _mdm2_clamp(mdm2.get_center() + RIGHT * 1.15 + DOWN * 0.12, open_amt=1.0, scale=1.08)
        self.play(
            Transform(mdm2, open_mdm2),
            p2.animate.move_to([open_mdm2.get_center()[0] + 0.15, 0.68, 0]),
            mdm2_lab.animate.next_to(open_mdm2, RIGHT, buff=0.22),
            run_time=0.9,
        )

        self.at("destruction drops")
        st["shred_fraction"] = 0.1
        self.play(
            spin_spd.animate.set_value(0.65),
            p_val.animate.set_value(80.0),
            run_time=2.4,
            rate_func=lambda u: 1.0 - np.exp(-3.2 * u) / (1.0 - np.exp(-3.2)) if u < 1.0 else 1.0,
        )

        self.at("switching on genes")
        g_p21 = boxed_label("p21 (pause)", color=TEAL, size=22, pad=0.14).move_to([-0.30, 2.20, 0])
        g_rep = boxed_label("DNA repair", color=TEAL, size=22, pad=0.14).move_to([-0.30, 1.46, 0])
        self.play(
            FadeOut(p1),
            p53.animate.move_to([-2.25, 1.44, 0]),
            FadeIn(g_p21), FadeIn(g_rep),
            run_time=1.4,
        )
        self.finish()


# ------------------------------------------------------------------------------
# s05_predict_q: Diverse chemical threats cross membrane -> predict question
# ------------------------------------------------------------------------------
def _build_predict_world():
    """Shared backdrop builder for s05_predict_q end state and s06_pause."""
    cell = _rounded_cell(-5.9, 5.9, -2.05, 3.15, nuc_center=(-3.2, 1.95), nuc_rx=2.1, nuc_ry=0.88, with_break=False)
    nuc_lab = T("nucleus", size=24, color=BLUE).move_to([-3.2, 1.45, 0])
    catcher = _keap1_catcher([0.45, 0.05, 0], with_cys=False, scale=1.55)
    catcher_lab = T("one sensor ?", size=26, color=GOLD).next_to(catcher, DOWN, buff=0.22)
    threats_lab = T("diverse chemical threats", size=28, color=RED).move_to([3.55, 2.45, 0])

    rng = np.random.default_rng(31)
    shapes = VGroup()
    pts = [
        [3.1, 1.55], [4.2, 1.35], [2.4, 0.85], [3.6, 0.55],
        [4.7, 0.35], [2.8, -0.25], [4.0, -0.55], [2.2, -0.95],
        [3.4, -1.25], [4.8, -1.10], [1.65, 1.30], [1.75, 0.35],
    ]
    for i, (px, py) in enumerate(pts):
        s = _electrophile_shape(i, pos=[px, py, 0], scale=0.38 + 0.07 * (i % 3))
        s._base = np.array([px, py, 0.0])
        s._phase = float(rng.uniform(0, TAU))
        shapes.add(s)

    def _drift(mob, dt):
        for s in mob:
            s._phase += dt * 2.2
            s.move_to(s._base + np.array([0.16 * np.cos(s._phase), 0.16 * np.sin(s._phase * 1.3), 0.0]))
    shapes.add_updater(_drift)
    return VGroup(cell, nuc_lab, catcher, catcher_lab, threats_lab, shapes), shapes


class S05PredictQ(SpokenScene):
    def construct(self):
        rng = np.random.default_rng(37)
        cell = _rounded_cell(-5.9, 5.9, -2.05, 3.15, nuc_center=(-3.2, 1.95), nuc_rx=2.1, nuc_ry=0.88, with_break=True)
        nuc_lab = T("nucleus", size=24, color=BLUE).move_to([-3.2, 1.45, 0])
        atm = boxed_label("ATM", color=RED, size=26).move_to([-3.2, 0.50, 0])
        spout = _synthesis_spout([-4.65, -1.15])
        shredder = _proteasome_ring([3.95, -1.15], radius=0.58)
        spin_spd = ValueTracker(2.2)
        _spin_ring(shredder, spin_spd)

        p53 = _hero_block("p53", pos=[-0.55, -0.32, 0], font_size=26, scale=1.0)
        mdm2 = _mdm2_clamp(p53.act_end.get_center() + RIGHT * 0.26, open_amt=0.0, scale=1.1)

        self.play(
            FadeIn(cell), FadeIn(nuc_lab), FadeIn(atm),
            FadeIn(spout), FadeIn(shredder), FadeIn(p53), FadeIn(mdm2),
            run_time=0.9,
        )
        self.add(scope_tag("schematic"))
        stream, st = _start_stream(
            self, spout.tip, shredder.center_pt, rng, shred_fraction=0.5,
            end_pt=[-0.8, -1.10, 0], spawn_period=0.45, pscale=0.78,
        )

        self.at("broken dna has")
        sensor_tag = T("dedicated kinase sensor", size=24, color=RED).next_to(atm, RIGHT, buff=0.25)
        p_tag = _phosphate_badge(p53.body.get_left() + LEFT * 0.42, scale=1.0)
        self.play(FadeIn(sensor_tag), FadeIn(p_tag), run_time=1.1)

        self.at("imagine dozens of")
        st["active"] = False
        world, shapes = _build_predict_world()
        cell_clean = world[0]
        catcher, catcher_lab, threats_lab = world[2], world[3], world[4]
        self.play(
            FadeOut(atm), FadeOut(sensor_tag), FadeOut(p53), FadeOut(mdm2), FadeOut(p_tag),
            FadeOut(spout), FadeOut(shredder), FadeOut(stream),
            Transform(cell, cell_clean),
            run_time=0.65,
        )
        self.play(FadeIn(catcher), FadeIn(catcher_lab), run_time=0.60)
        self.play(FadeIn(threats_lab), FadeIn(shapes, shift=LEFT * 1.4), run_time=1.2)

        self.at("how could one protein")
        q = question_card("How can one sensor detect dozens of differently shaped toxins?", max_w=10.4)
        self.play(FadeIn(q.question), run_time=1.0)

        self.at("pause and predict")
        self.finish()


# ------------------------------------------------------------------------------
# s06_pause: Silent 4.5s PredictPause holding the exact question & backdrop
# ------------------------------------------------------------------------------
class S06Pause(PredictPause):
    QUESTION = "How can one sensor detect dozens of differently shaped toxins?"
    SECONDS = 4.5

    def backdrop(self):
        world, _ = _build_predict_world()
        return world


# ------------------------------------------------------------------------------
# s07_keap1_reveal: Nrf2 + Keap1 with reactive Cys sulfur knobs attacked by electrophiles
# ------------------------------------------------------------------------------
class S07Keap1Reveal(SpokenScene):
    def construct(self):
        rng = np.random.default_rng(43)
        cell = _rounded_cell(-5.9, 5.9, -2.15, 3.05, nuc_center=(-3.2, 1.85), nuc_rx=2.0, nuc_ry=0.85)
        nuc_lab = T("nucleus", size=24, color=BLUE).move_to([-3.2, 1.35, 0])
        spout = _synthesis_spout([-4.65, -0.55])
        spout_lab = T("Nrf2 synthesis", size=24, color=TEAL).next_to(spout, DOWN, buff=0.20)
        shredder = _proteasome_ring([4.25, -0.85], radius=0.68)
        shred_lab = T("proteasome", size=24, color=GOLD).next_to(shredder, DOWN, buff=0.20)
        spin_spd = ValueTracker(2.2)
        _spin_ring(shredder, spin_spd)

        catcher = _keap1_catcher([0.55, -0.10, 0], with_cys=False, scale=1.55)
        catcher_lab = T("Keap1", size=28, color=GOLD).next_to(catcher, UP, buff=0.32)

        elec_pts = [[2.75, 1.65, 0], [4.05, 1.35, 0], [2.35, 0.90, 0], [3.55, 0.45, 0], [4.70, 1.45, 0]]
        elec_shapes = VGroup(*[
            _electrophile_shape(i, pt, scale=0.44) for i, pt in enumerate(elec_pts)
        ])
        for i, s in enumerate(elec_shapes):
            s._base = np.array(elec_pts[i], dtype=float)
            s._phase = float(i * 1.5)

        def _bob_elec(mob, dt):
            for s in mob:
                s._phase += dt * 2.4
                s.move_to(s._base + np.array([0.28 * np.cos(s._phase), 0.25 * np.sin(s._phase * 1.2), 0.0]))

        elec_shapes.add_updater(_bob_elec)
        elec_lab = T("electrophiles", size=28, color=RED).move_to([3.35, 2.55, 0])

        self.play(FadeIn(cell), FadeIn(nuc_lab), FadeIn(catcher), FadeIn(elec_shapes, shift=LEFT * 1.6), run_time=0.9)
        self.add(scope_tag("schematic"))

        self.at("chemical threats are")
        self.play(FadeIn(elec_lab), run_time=0.7)

        self.at("their responder")
        self.play(FadeIn(spout), FadeIn(spout_lab), FadeIn(shredder), FadeIn(shred_lab), run_time=0.6)
        stream, st = _start_stream(
            self, spout.tip, shredder.center_pt, rng, shred_fraction=0.5,
            end_pt=[-1.2, -0.30, 0], spawn_period=0.48, pscale=0.72,
            use_clamp=False, via_pt=[0.55, 0.15, 0],
        )
        nrf2_demo = _hero_block("Nrf2", pos=[-2.1, 0.45, 0], font_size=26, scale=0.95)
        self.play(FadeIn(nrf2_demo, shift=RIGHT * 0.5), run_time=0.8)

        self.at("a partner called")
        nrf2_pass = _stream_block(nrf2_demo.get_center(), scale=0.85)
        self.play(FadeIn(catcher_lab), ReplacementTransform(nrf2_demo, nrf2_pass), run_time=0.45)
        self.play(nrf2_pass.animate.move_to([0.55, 0.15, 0]), run_time=0.6)
        self.play(nrf2_pass.animate.scale(0.65).move_to(shredder.center_pt).set_opacity(0.0), run_time=0.7)
        self.remove(nrf2_pass)

        self.at("carries cysteines")
        catcher_cys = _keap1_catcher([0.55, -0.10, 0], with_cys=True, scale=1.55)
        cys_lab = T("Cys (sulfur)", size=26, color=YELLOW).next_to(catcher_cys, DOWN, buff=0.18)
        self.play(Transform(catcher, catcher_cys), FadeIn(cys_lab), run_time=1.0)

        self.at("react with them")
        elec_shapes.clear_updaters()
        st["shred_fraction"] = 0.0
        spin_spd.set_value(0.6)
        targets = [k[1].get_center() for k in catcher_cys.knobs]
        arc_path = VMobject().set_points_smoothly([
            elec_shapes[0].get_center(),
            np.array([0.55, 1.80, 0.0]),
            targets[0],
        ])
        flashes = VGroup(*[
            Circle(radius=0.26, stroke_color=YELLOW, stroke_width=4, fill_color=YELLOW, fill_opacity=0.55).move_to(pt)
            for pt in targets
        ])
        self.play(
            MoveAlongPath(elec_shapes[0], arc_path),
            elec_shapes[2].animate.move_to(targets[2]),
            elec_shapes[3].animate.move_to(targets[1]),
            FadeOut(elec_shapes[1]),
            FadeOut(elec_shapes[4]),
            FadeOut(elec_lab),
            run_time=0.95,
        )
        self.play(FadeIn(flashes, scale=1.3), run_time=0.35)
        self.play(FadeOut(flashes), run_time=0.35)

        self.at("reads electron hunger")
        cap = caption("Reads electron hunger, not shape.", size=28, color=TEXT)
        self.play(FadeIn(cap), run_time=0.7)
        self.finish()


# ------------------------------------------------------------------------------
# s08_keap1_escape: Full Keap1 pool, fresh Nrf2 escapes to nucleus -> protective enzymes
# ------------------------------------------------------------------------------
class S08Keap1Escape(SpokenScene):
    def construct(self):
        rng = np.random.default_rng(59)
        cell = _rounded_cell(-6.0, 3.4, -1.95, 3.05, nuc_center=(-2.35, 1.88), nuc_rx=3.05, nuc_ry=1.02, dna_dy=0.40)
        spout = _synthesis_spout([-4.75, -0.45])
        spout_lab = T("Nrf2 synthesis", size=24, color=TEAL).next_to(spout, DOWN, buff=0.18)
        shredder = _proteasome_ring([2.05, -0.62], radius=0.52)
        shred_lab = T("proteasome", size=24, color=GOLD).next_to(shredder, DOWN, buff=0.20)
        spin_spd = ValueTracker(0.55)
        _spin_ring(shredder, spin_spd)

        keap_top = _keap1_catcher([-0.45, -0.15, 0], with_cys=True, scale=1.08)
        old_nrf_1 = _stream_block(keap_top.get_center() + UP * 0.14, scale=0.65)
        el_1 = _electrophile_shape(0, keap_top.knobs[0][1].get_center(), scale=0.26)

        keap_bot = _keap1_catcher([0.95, -0.15, 0], with_cys=True, scale=1.08)
        old_nrf_2 = _stream_block(keap_bot.get_center() + UP * 0.14, scale=0.65)
        el_2 = _electrophile_shape(1, keap_bot.knobs[2][1].get_center(), scale=0.26)

        keap_pool_lab = T("Keap1 pool full", size=24, color=GOLD).move_to([0.15, -1.10, 0])

        p_val = ValueTracker(20.0)
        gauge = _level_gauge(p_val, x=5.20, y0=-1.55, y1=1.75, max_val=100.0, title="Nrf2", unit="units")

        self.play(
            FadeIn(cell), FadeIn(spout), FadeIn(spout_lab),
            FadeIn(shredder), FadeIn(shred_lab),
            FadeIn(keap_top), FadeIn(old_nrf_1), FadeIn(el_1),
            FadeIn(keap_bot), FadeIn(old_nrf_2), FadeIn(el_2),
            FadeIn(keap_pool_lab), FadeIn(gauge),
            run_time=1.0,
        )
        self.add(scope_tag("schematic"))

        # Initial stream stays in cytosol near spout until "with the catchers"
        stream, st = _start_stream(
            self, spout.tip, None, rng, shred_fraction=0.0,
            end_pt=[-2.35, -0.45, 0], spawn_period=0.72, pscale=0.65,
        )

        self.at("with the catchers")
        st["end_pt"] = np.array([-3.82, 1.25, 0.0])
        st["curve_x"] = 0.35
        enz_bar = boxed_label("protective enzymes", color=TEAL, size=24, pad=0.16).move_to([-1.80, 1.62, 0])
        self.play(
            FadeIn(enz_bar),
            p_val.animate.set_value(80.0),
            run_time=2.4,
        )

        self.at("other pathways reuse")
        self.at("holding intact kinases")

        def _mini_badge(text, pos):
            bg = RoundedRectangle(
                corner_radius=0.12, width=4.35, height=0.82,
                stroke_color=GREY, stroke_width=2, fill_color=BG, fill_opacity=0.92,
            ).move_to(pos)
            blk = RoundedRectangle(
                corner_radius=0.06, width=0.42, height=0.28,
                stroke_color=TEAL, stroke_width=2.5, fill_color=TEAL, fill_opacity=0.35,
            ).move_to([pos[0] - 1.65, pos[1] - 0.10, 0])
            rest = RoundedRectangle(
                corner_radius=0.06, width=0.44, height=0.16,
                stroke_color=GOLD, stroke_width=2.5, fill_color=GOLD, fill_opacity=0.45,
            ).move_to([pos[0] - 1.65, pos[1] + 0.08, 0])
            lab = T(text, size=24, color=TEXT).move_to([pos[0] + 0.32, pos[1], 0])
            g = VGroup(bg, blk, rest, lab)
            g.rest = rest
            return g

        b1 = _mini_badge("ASK1 + thioredoxin", [-3.75, -2.95, 0])
        b2 = _mini_badge("ER sensors + BiP", [1.15, -2.95, 0])
        self.play(FadeIn(b1), FadeIn(b2), run_time=0.8)
        self.at("until stress arrives")
        self.play(
            b1.rest.animate.shift(UP * 0.20 + LEFT * 0.15),
            b2.rest.animate.shift(UP * 0.20 + LEFT * 0.15),
            run_time=1.0,
        )
        self.finish()


# ------------------------------------------------------------------------------
# s09_closing: Side-by-side TwoPanel comparison, both responders freed & gauges high
# ------------------------------------------------------------------------------
class S09Closing(SpokenScene):
    def construct(self):
        rng = np.random.default_rng(71)
        tp = TwoPanel(
            "p53 + MDM2 (DNA break)",
            "Nrf2 + Keap1 (electrophiles)",
            colors=(TEAL, TEAL),
            top=3.05, bottom=-2.45, gap=0.45, width=12.6, size=28,
        )

        lc, lw, lh = tp.area("left")
        rc, rw, rh = tp.area("right")

        # Left panel: mini-cell + synthesis spout + ATM + p53 + closed MDM2 + gauge
        l_cell = _rounded_cell(
            lc[0] - 2.75, lc[0] + 1.00, lc[1] - 2.00, lc[1] + 2.00,
            nuc_center=(lc[0] - 0.72, lc[1] + 1.08), nuc_rx=1.62, nuc_ry=0.74,
            with_break=True, dna_dy=0.40,
        )
        l_spout = _synthesis_spout([lc[0] - 2.38, lc[1] - 1.15], scale=0.45)
        l_atm = boxed_label("ATM", color=RED, size=22, pad=0.14).move_to([lc[0] - 1.25, lc[1] - 0.05, 0])
        l_p53 = _hero_block("p53", pos=[lc[0] - 0.40, lc[1] - 0.80, 0], font_size=22, scale=0.72)
        l_mdm2 = _mdm2_clamp(l_p53.act_end.get_center() + RIGHT * 0.20, open_amt=0.0, scale=0.72)
        l_mdm2_lab = T("MDM2", size=22, color=GOLD).next_to(l_mdm2, DOWN, buff=0.18)
        l_gene = boxed_label("repair", color=TEAL, size=22, pad=0.14).move_to([lc[0] - 0.72, lc[1] + 0.92, 0])
        l_val = ValueTracker(20.0)
        l_gauge = _level_gauge(l_val, x=lc[0] + 2.20, y0=lc[1] - 1.45, y1=lc[1] + 1.05, max_val=100.0, title="p53", unit="", bar_w=0.58)

        # Right panel: mini-cell + synthesis spout + Keap1 gripping Nrf2 + gauge
        r_cell = _rounded_cell(
            rc[0] - 2.75, rc[0] + 1.00, rc[1] - 2.00, rc[1] + 2.00,
            nuc_center=(rc[0] - 0.72, rc[1] + 1.08), nuc_rx=1.62, nuc_ry=0.74,
            with_break=False, dna_dy=0.40,
        )
        r_spout = _synthesis_spout([rc[0] - 2.38, rc[1] - 1.15], scale=0.45)
        r_keap = _keap1_catcher([rc[0] + 0.08, rc[1] - 1.12, 0], with_cys=True, scale=0.75)
        r_keap_lab = T("Keap1", size=22, color=GOLD).next_to(r_keap, DOWN, buff=0.12)
        r_nrf = _hero_block("Nrf2", pos=[rc[0] + 0.08, rc[1] - 0.58, 0], font_size=22, scale=0.72)
        r_gene = boxed_label("enzymes", color=TEAL, size=22, pad=0.14).move_to([rc[0] - 0.72, rc[1] + 0.92, 0])
        r_val = ValueTracker(20.0)
        r_gauge = _level_gauge(r_val, x=rc[0] + 2.20, y0=rc[1] - 1.45, y1=rc[1] + 1.05, max_val=100.0, title="Nrf2", unit="", bar_w=0.58)

        self.play(
            FadeIn(tp),
            FadeIn(l_cell), FadeIn(l_atm), FadeIn(l_p53), FadeIn(l_mdm2), FadeIn(l_mdm2_lab), FadeIn(l_gauge), FadeIn(l_spout),
            FadeIn(r_cell), FadeIn(r_keap), FadeIn(r_keap_lab), FadeIn(r_nrf), FadeIn(r_gauge), FadeIn(r_spout),
            run_time=1.2,
        )
        self.add(scope_tag("schematic"))

        # Left synthesis streams moving forward right of spout tips
        _start_stream(self, l_spout.tip, None, rng, shred_fraction=0.0, end_pt=[lc[0] - 1.92, lc[1] + 0.25, 0], spawn_period=0.62, pscale=0.44)
        _start_stream(self, r_spout.tip, None, rng, shred_fraction=0.0, end_pt=[rc[0] - 1.75, rc[1] + 0.25, 0], spawn_period=0.62, pscale=0.44)

        self.at("building responders ahead")
        l_spout_lab = T("made ahead", size=22, color=TEAL).move_to([lc[0] - 1.48, lc[1] - 1.62, 0])
        r_spout_lab = T("made ahead", size=22, color=TEAL).move_to([rc[0] - 1.48, rc[1] - 1.62, 0])
        self.play(
            FadeIn(l_spout_lab), FadeIn(r_spout_lab),
            run_time=1.6,
        )

        self.at("lifting a ready restraint")
        cap = caption("Lift the restraint -> act right away.", size=28, color=TEXT)
        open_l_mdm2 = _mdm2_clamp(l_mdm2.get_center() + DOWN * 0.08, open_amt=0.9, scale=0.72)
        l_p_badge = _phosphate_badge(open_l_mdm2.get_center() + UP * 0.38 + RIGHT * 0.36, scale=0.96)
        r_el = _electrophile_shape(0, r_keap.knobs[0][1].get_center(), scale=0.22)
        self.play(
            FadeIn(l_p_badge),
            FadeIn(r_el),
            Transform(l_mdm2, open_l_mdm2),
            l_mdm2_lab.animate.next_to(open_l_mdm2, DOWN, buff=0.16),
            l_p53.animate.move_to([lc[0] + 0.22, lc[1] + 0.14, 0]),
            r_nrf.animate.move_to([rc[0] + 0.08, rc[1] + 0.20, 0]),
            FadeIn(l_gene), FadeIn(r_gene),
            l_val.animate.set_value(80.0),
            r_val.animate.set_value(80.0),
            FadeIn(cap),
            run_time=2.3,
        )
        self.finish()


# ------------------------------------------------------------------------------
# s10_end: Standard EndCard with exact take-home line
# ------------------------------------------------------------------------------
class S10End(EndCard):
    LINE = "Many stress pathways hold responders back until stress removes the restraint."
