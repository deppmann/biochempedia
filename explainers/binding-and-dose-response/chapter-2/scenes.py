"""Blockers and the Shape of a Shift — Chapter 2 of Binding: Affinity, Occupancy and Dose-Response.

COLOUR MAP (one colour per concept, carried across all 13 scenes):
  BLUE   (#58C4DD) : receptors (20-receptor strip, 6-receptor zoom, mu-opioid receptors)
  GREY   (#8B93A1) : cell membrane, plot axes/ticks, ghosted baseline curve, equilibrium scope tag
  GREEN  (#83C167) : agonist (morphine) tokens, unblocked baseline curve, downstream response/signalling bar
  GOLD   (#D4A843) : competitive blocker (naloxone), parallel-shifted curves, dose-ratio brackets, Schild points & slope-1 line
  PURPLE (#B18CEB) : non-competitive blocker & its schematic lowered curve
  RED    (#FC6255) : irreversible blocker, covalent lock badge, irreversible lowered curve
  ORANGE (#FF862F) : Schild assumption-failure warning (non-unit slope, non-equilibrium / agonist removal)
  TEAL   (#3FB8C0) : Schild assumption-failure warning (high-dose bend, binds elsewhere / second receptor), UI accents
  TEXT   (#E8EAF0) : unknown blocker (WHITE) & its single shifted curve, primary labels, question cards

CARRIED WORLD:
  A row of BLUE U-shaped receptor pockets embedded in a GREY cell membrane above a live GREEN
  response bar, paired with a computed log-dose response Plot under the sharp 5% receptor-reserve
  model (1 of 20 receptors occupied = 100% response, EC50 = Kd/39). Scenes zoom in on 6 pockets
  (s02), expand the Plot (s03-s07), split into the Schild Plot (s08-s09), return to the carried
  receptors + Plot + running clock (s10), and pull back to the full world with an unknown-amplifier
  cover (s11).

WHAT CHANGES IN EACH SPOKEN SCENE AND WHAT IT IS COMPUTED FROM:
  s00_link_and_question : Morphine and naloxone tokens move along non-colliding RNG trajectories;
                          naloxone enters BLUE pockets, dropping agonist occupancy from 1/20 to 0/20
                          and driving the GREEN response bar from 100% to 0% as baseline ghosts GREY.
  s02_competitive       : 6 zoomed pockets run stochastic competitive binding/unbinding (Markov RNG);
                          GREEN agonist bounces off GOLD-occupied sites, then floods in by mass action
                          to refill the GREEN response bar to 100%.
  s03_parallel_shift    : Dose-ratio tracker dr animates from 1 to 11, sliding the GOLD curve right by
                          log10(11)=1.04 log units; horizontal guide sweeps 20%-80% showing constant gap;
                          dose sweep fills receptor strip and GREEN response bar to 100%.
  s04_insurmountable    : PURPLE tokens latch side pockets and clamp the downstream GREEN gauge at 45%
                          while schematic PURPLE curve flattens low; RED tokens then lock main pockets.
  s05_predict_question  : WHITE unknown tokens drift above receptors while curve slides right by 2-fold
                          (dr=2, +0.301 log units) to 100% ceiling; question + empty marker set.
  s07_reveal            : Dose-removal tracker steps 50% (Kd/19, 100%) -> 90% (Kd/3, 100%) -> 98% (40% max)
                          in RED alongside competitive dr=2, 11, 101 (100% max) in GOLD.
  s08_schild_plot       : Left Plot dose-ratio brackets (dr=2, 11, 101) morph into computed Schild points
                          (0,0), (1,1), (2,2) as log(dr-1) vs log[B], connected by slope-1 GOLD line.
  s09_assumptions       : Schematic RED line (slope 0.55) and PURPLE curve (bends at high dose) draw over
                          dimmed slope-1 line; narrow-range bracket highlights where bending curve hugs slope 1.
  s10_naloxone_scope    : Non-colliding morphine/naloxone tokens compete at mu-opioid receptors while dr
                          slides 1 -> 11 (GREEN -> GOLD), dropping response at fixed dose and driving the
                          GREEN bar down; clock hand runs continuously for clinical time-dependence.
  s11_handoff           : Dose dot sweeps diverging GOLD competitive and RED irreversible curves; frosted
                          cover slides over the downstream gauge beside two parallel shifted curves and '?'.
"""
import numpy as np
from bp_parts import *

PURPLE = "#B18CEB"
RESERVE = 0.05  # 5% receptor reserve: 1 of 20 receptors occupied = 100% response


# ------------------------------------------------------------------ computed pharmacology model
def occupancy(log_dose, dr=1.0):
    """Fractional receptor occupancy [A]/Kd / (dr + [A]/Kd) for log10([A]/Kd) and dose ratio dr."""
    r = 10.0 ** log_dose
    return r / (dr + r)


def response_pct(log_dose, dr=1.0, surviving=1.0):
    """Sharp 5% reserve response (%): proportional up to 5% of original pool occupied, capped at 100%."""
    occ = occupancy(log_dose, dr=dr)
    return 100.0 * min(1.0, surviving * occ / RESERVE)


def noncomp_schematic(log_dose, cap=45.0):
    """Schematic insurmountable non-competitive response clamped at `cap` %."""
    return min(cap, response_pct(log_dose, dr=1.0, surviving=1.0))


def log_dose_for_response(pct, dr=1.0, surviving=1.0):
    """Inverse of response_pct for 0 < pct < 100 * min(1, surviving/RESERVE)."""
    occ = (pct / 100.0) * RESERVE / surviving
    r = dr * occ / max(1e-9, 1.0 - occ)
    return float(np.log10(max(1e-9, r)))


# ------------------------------------------------------------------ shared visual builders
def make_receptor(center, width=0.44, height=0.40, has_side=False, stroke_w=4.2):
    """Geometric U-shaped receptor pocket (no molecular structure). Optional side notch on right."""
    cx, cy, _ = np.array(center, dtype=float)
    hw, hh = width / 2, height / 2
    pts = [
        [cx - hw, cy + hh, 0],
        [cx - hw, cy - hh + 0.07, 0],
        [cx - hw + 0.07, cy - hh, 0],
        [cx + hw - 0.07, cy - hh, 0],
        [cx + hw, cy - hh + 0.07, 0],
        [cx + hw, cy + hh, 0],
    ]
    cup = VMobject(color=BLUE, stroke_width=stroke_w, fill_color=BLUE, fill_opacity=0.28)
    cup.set_points_as_corners(pts)
    g = VGroup(cup)
    g.cup = cup
    g.pocket_pt = np.array([cx, cy + 0.02, 0.0])
    if has_side:
        sx = cx + hw
        sy = cy - 0.02
        s_pts = [
            [sx, sy + 0.12, 0],
            [sx + 0.17, sy + 0.12, 0],
            [sx + 0.17, sy - 0.12, 0],
            [sx, sy - 0.12, 0],
        ]
        side = VMobject(color=BLUE, stroke_width=stroke_w * 0.85, fill_color=BLUE, fill_opacity=0.28)
        side.set_points_as_corners(s_pts)
        g.add(side)
        g.side_cup = side
        g.side_pt = np.array([sx + 0.09, sy, 0.0])
    return g


def make_membrane(x0, x1, y, stroke_w=5.5):
    """Cell membrane bilayer bar in GREY."""
    bilayer = Rectangle(width=x1 - x0, height=0.16, stroke_width=0, fill_color=GREY, fill_opacity=0.48)
    bilayer.move_to([(x0 + x1) / 2, y - 0.08, 0])
    top = Line([x0, y, 0], [x1, y, 0], color=GREY, stroke_width=stroke_w)
    bot = Line([x0, y - 0.16, 0], [x1, y - 0.16, 0], color=GREY, stroke_width=stroke_w * 0.65).set_opacity(0.85)
    return VGroup(bilayer, top, bot)


def make_receptor_row(n=20, x0=-5.9, x1=5.9, y=2.20, cup_w=0.40, cup_h=0.36, has_side=False, stroke_w=3.8):
    """Row of `n` BLUE receptor cups seated on a GREY membrane."""
    xs = np.linspace(x0 + 0.35, x1 - 0.35, n)
    cups = VGroup(*[make_receptor([x, y, 0], width=cup_w, height=cup_h, has_side=has_side, stroke_w=stroke_w) for x in xs])
    mem = make_membrane(x0, x1, y - cup_h / 2 - 0.04)
    g = VGroup(mem, cups)
    g.mem = mem
    g.cups = cups
    return g


def make_token(kind, radius=0.14):
    """Geometric ligand token: circle for agonist, rounded pill/triangle for blockers."""
    if kind == "agonist":
        return Circle(radius=radius, color=GREEN, fill_color=GREEN, fill_opacity=0.95,
                      stroke_color=TEXT, stroke_width=1.6)
    if kind == "competitive":
        return RoundedRectangle(width=radius * 2.15, height=radius * 1.7, corner_radius=0.05,
                                color=GOLD, fill_color=GOLD, fill_opacity=0.95,
                                stroke_color=TEXT, stroke_width=1.6)
    if kind == "noncompetitive":
        return RegularPolygon(3, radius=radius * 1.3, color=PURPLE, fill_color=PURPLE, fill_opacity=0.95,
                              stroke_color=TEXT, stroke_width=1.6)
    if kind == "irreversible":
        return RoundedRectangle(width=radius * 2.15, height=radius * 1.7, corner_radius=0.05,
                                color=RED, fill_color=RED, fill_opacity=0.95,
                                stroke_color=TEXT, stroke_width=1.6)
    return RoundedRectangle(width=radius * 2.15, height=radius * 1.7, corner_radius=0.05,
                            color=TEXT, fill_color=TEXT, fill_opacity=0.90,
                            stroke_color=GREY, stroke_width=1.6)


def make_lock_badge(center, scale=1.0):
    """Small geometric padlock icon for covalent irreversible binding."""
    c = np.array(center, dtype=float)
    shackle = Arc(radius=0.07 * scale, start_angle=0, angle=PI, color=TEXT, stroke_width=2.5 * scale)
    shackle.move_to(c + UP * 0.06 * scale)
    body = RoundedRectangle(width=0.18 * scale, height=0.14 * scale, corner_radius=0.02 * scale,
                            color=RED, fill_color=RED, fill_opacity=1.0, stroke_color=TEXT, stroke_width=1.8 * scale)
    body.move_to(c + DOWN * 0.03 * scale)
    return VGroup(shackle, body)


def make_response_bar(x0, x1, y, height=0.38, tracker=None, color=GREEN, title="response", show_pct=True):
    """Horizontal response bar strictly inside its frame + live % readout on the right."""
    if tracker is None:
        tracker = ValueTracker(100.0)
    w = x1 - x0
    outer = RoundedRectangle(corner_radius=0.08, width=w, height=height,
                             stroke_color=GREY, stroke_width=2.8, fill_color=BG, fill_opacity=0.95)
    outer.move_to([(x0 + x1) / 2, y, 0])
    inner_max = w - 0.10
    inner_h = height - 0.10
    left_edge = x0 + 0.05

    def _fill():
        frac = float(np.clip(tracker.get_value() / 100.0, 0.0, 1.0))
        fw = max(0.02, frac * inner_max)
        r = RoundedRectangle(corner_radius=0.04, width=fw, height=inner_h,
                             stroke_width=0, fill_color=color, fill_opacity=0.90 if frac > 0.01 else 0.0)
        r.move_to([left_edge + fw / 2, y, 0])
        return r

    fill = always_redraw(_fill)
    g = VGroup(outer, fill)
    if title:
        lbl = T(title, 28, color).next_to(outer, LEFT, buff=0.22)
        g.add(lbl)
        g.label = lbl
    if show_pct:
        pct = always_redraw(lambda: M(f"{tracker.get_value():3.0f}%", 28, TEXT).move_to([x1 + 0.65, y, 0]))
        g.add(pct)
        g.pct = pct
    g.outer = outer
    g.tracker = tracker
    return g


def make_dose_plot(box=(-5.4, 3.6, -2.6, 0.9), xlabel="log([agonist] / Kd)", ylabel="response (%)",
                   label_size=26, tick_size=24):
    """Standard log-dose vs response Plot using the lesson's log10([A]/Kd) scale."""
    xticks = [(-3, "10⁻³"), (-2, "10⁻²"), (-1, "10⁻¹"), (0, "1"), (1, "10"), (2, "10²")]
    yticks = [(0, "0%"), (50, "50%"), (100, "100%")]
    P = Plot(box=box, xr=(-3.4, 2.5), yr=(0, 112), xticks=xticks, yticks=yticks,
             xlabel=xlabel, ylabel=ylabel, color=GREY, size=tick_size, label_size=label_size, stroke=4.5)
    # Subtle 50% and 100% ceiling reference lines inside the plot
    for y_ref in (50, 100):
        g = DashedLine(P.pt(P.xr[0], y_ref), P.pt(P.xr[1], y_ref), color=GREY, stroke_width=1.5, dash_length=0.16)
        g.set_opacity(0.28).set_z_index(-1)
        g.layout_ok = "covered"
        P.add(g)
    return P


def make_schild_plot(box=(0.4, 5.8, -2.1, 2.2), label_size=28, tick_size=24):
    """Computed Schild plot: log(dose ratio - 1) vs log([blocker] / KB)."""
    ticks = [(0, "0"), (1, "1"), (2, "2")]
    P = Plot(box=box, xr=(-0.5, 2.5), yr=(-0.5, 2.5), xticks=ticks, yticks=ticks,
             xlabel="log [blocker]", ylabel="log(dose ratio − 1)",
             color=GREY, size=tick_size, label_size=label_size, stroke=4.5)
    for k in (0, 1, 2):
        h = DashedLine(P.pt(-0.5, k), P.pt(2.5, k), color=GREY, stroke_width=1.4, dash_length=0.14).set_opacity(0.25).set_z_index(-1)
        v = DashedLine(P.pt(k, -0.5), P.pt(k, 2.5), color=GREY, stroke_width=1.4, dash_length=0.14).set_opacity(0.25).set_z_index(-1)
        h.layout_ok = "covered"
        v.layout_ok = "covered"
        P.add(h, v)
    return P


def make_solution_trajectories(n_green, n_gold, bounds, seed=7, min_sep=0.45):
    """Precompute smooth non-colliding random-walk paths for GREEN and GOLD tokens in solution."""
    rng = np.random.default_rng(seed)
    x0, x1, y0, y1 = bounds
    n_tot = n_green + n_gold
    pos = np.zeros((n_tot, 2))
    for i in range(n_tot):
        for _ in range(80):
            p = np.array([rng.uniform(x0, x1), rng.uniform(y0, y1)])
            if all(np.linalg.norm(p - pos[j]) >= min_sep for j in range(i)):
                pos[i] = p
                break
        else:
            pos[i] = np.array([rng.uniform(x0, x1), rng.uniform(y0, y1)])
    vel = rng.uniform(-0.70, 0.70, size=(n_tot, 2))
    dt = 0.05
    steps = 650
    traj = np.zeros((steps, n_tot, 2))
    for s in range(steps):
        traj[s] = pos
        vel += rng.normal(0.0, 0.09, size=(n_tot, 2))
        speeds = np.linalg.norm(vel, axis=1, keepdims=True)
        vel = np.where(speeds > 0.90, vel * (0.90 / np.maximum(speeds, 1e-6)), vel)
        for i in range(n_green):
            for j in range(n_green, n_tot):
                diff = pos[i] - pos[j]
                dist = np.linalg.norm(diff)
                if dist < min_sep and dist > 1e-6:
                    push = (diff / dist) * (min_sep - dist) * 0.65
                    pos[i] += push
                    pos[j] -= push
                    vel[i] += (diff / dist) * 0.25
                    vel[j] -= (diff / dist) * 0.25
        pos = pos + vel * dt
        for k in range(n_tot):
            if pos[k, 0] < x0:
                pos[k, 0] = x0
                vel[k, 0] = abs(vel[k, 0])
            elif pos[k, 0] > x1:
                pos[k, 0] = x1
                vel[k, 0] = -abs(vel[k, 0])
            if pos[k, 1] < y0:
                pos[k, 1] = y0
                vel[k, 1] = abs(vel[k, 1])
            elif pos[k, 1] > y1:
                pos[k, 1] = y1
                vel[k, 1] = -abs(vel[k, 1])
    return traj, dt


def sample_traj(traj, dt, t):
    idx = (t / dt) % (len(traj) - 1)
    i0 = int(idx)
    a = idx - i0
    return traj[i0] * (1.0 - a) + traj[i0 + 1] * a


def drift_until(scene, tracker, phrase, lead=0.2, nth=0):
    """Advance simulation `tracker` continuously until `phrase` is spoken."""
    target = scene.t_of(phrase, nth=nth) - lead
    rest = target - scene.elapsed()
    if rest > 0.04:
        scene.play(tracker.animate(run_time=rest, rate_func=linear).set_value(tracker.get_value() + rest))


def drift_to_end(scene, tracker):
    """Advance simulation `tracker` cleanly right up to narration end, then finish."""
    rest = scene.narration_s - scene.elapsed()
    if rest > 0.04:
        scene.play(tracker.animate(run_time=rest, rate_func=linear).set_value(tracker.get_value() + rest))
    scene.finish()


def time_left_before(scene, phrase, lead=0.2, nth=0, min_t=0.2):
    """Seconds remaining before `phrase` minus `lead`, clamped below at `min_t`."""
    return max(min_t, scene.t_of(phrase, nth=nth) - lead - scene.elapsed())


def build_predict_backdrop():
    """Shared backdrop for s05_predict_question (end) and s06_predict_pause (question across top)."""
    row = make_receptor_row(20, x0=-5.9, x1=5.9, y=1.95, cup_w=0.38, cup_h=0.32, stroke_w=3.4)
    xs = [-2.5, -0.4, 1.7, 3.8]
    whites = VGroup(*[make_token("unknown", 0.14).move_to([x, 2.48, 0]) for x in xs])
    w_lbl = T("unknown blocker", 28, TEXT).move_to([-4.65, 2.48, 0])
    P = make_dose_plot(box=(-5.2, 3.8, -2.65, 0.72), label_size=26, tick_size=24)
    base_c = P.curve(lambda x: response_pct(x, dr=1.0), color=GREY, width=5.0, opacity=0.75)
    shift_c = P.curve(lambda x: response_pct(x, dr=2.0), color=TEXT, width=6.8)
    base_tag = T("baseline", 26, GREY).move_to([-4.45, -0.85, 0])
    shift_tag = T("with blocker (100% max)", 26, TEXT).move_to([1.9, -0.35, 0])
    choice_box = RoundedRectangle(corner_radius=0.10, width=1.6, height=0.54,
                                  stroke_color=GOLD, stroke_width=3.0, fill_color=BG, fill_opacity=0.92)
    choice_box.move_to([5.2, 3.22, 0])
    q_mark = T("?", 30, GOLD).move_to(choice_box)
    choice = VGroup(choice_box, q_mark)
    return VGroup(row, whites, w_lbl, P, base_c, shift_c, base_tag, shift_tag, choice), choice


# ------------------------------------------------------------------ scenes
def _separate_green_from_gold(green_pts, gold_pts, bounds, min_sep=0.46, min_gg=0.34):
    """Push free GREEN token positions away from GOLD (>= min_sep) and other GREEN (>= min_gg) in solution."""
    x0, x1, y0, y1 = bounds
    out = [np.array(p, dtype=float) for p in green_pts]
    for i in range(len(out)):
        for _ in range(4):
            others = [(q, min_sep) for q in gold_pts] + [(out[j], min_gg) for j in range(i)]
            for q, req in others:
                diff = out[i][:2] - np.array(q[:2], dtype=float)
                dist = float(np.linalg.norm(diff))
                if dist < req:
                    if dist > 1e-4:
                        push = (diff / dist) * (req - dist + 0.02)
                    else:
                        push = np.array([req, 0.0])
                    cand = out[i][:2] + push
                    cand[1] = float(np.clip(cand[1], y0, y1))
                    dx_cur = cand[0] - float(q[0])
                    dy_cur = cand[1] - float(q[1])
                    if np.hypot(dx_cur, dy_cur) < req:
                        need_dx = float(np.sqrt(max(0.0, (req + 0.02) ** 2 - dy_cur ** 2)))
                        sign = 1.0 if (dx_cur >= 0 and float(q[0]) + need_dx <= x1) or float(q[0]) - need_dx < x0 else -1.0
                        cand[0] = float(q[0]) + sign * need_dx
                    cand[0] = float(np.clip(cand[0], x0, x1))
                    out[i][:2] = cand
    return out


class S00LinkAndQuestion(SpokenScene):
    def construct(self):
        row = make_receptor_row(20, x0=-5.9, x1=5.9, y=2.15, cup_w=0.38, cup_h=0.34, stroke_w=3.5)
        resp = ValueTracker(100.0)
        bar = make_response_bar(-3.5, 2.7, 1.38, height=0.36, tracker=resp, color=GREEN, title="response")
        P = make_dose_plot(box=(-5.1, 3.6, -2.70, 0.52), label_size=24, tick_size=22)
        curve_col = ValueTracker(0.0)  # 0 = GREEN, 1 = GREY ghost
        curve = always_redraw(lambda: P.curve(
            lambda x: response_pct(x, dr=1.0),
            color=interpolate_color(ManimColor(GREEN), ManimColor(GREY), curve_col.get_value()),
            width=7.0 - 2.0 * curve_col.get_value(),
            opacity=1.0 - 0.30 * curve_col.get_value(),
        ))
        schem = T("schematic", 24, GREY).move_to([5.65, 1.38, 0])

        bound_ag = make_token("agonist", 0.13).move_to(row.cups[9].pocket_pt)
        reserve_tag = T("1 / 20 occupied (5% reserve)", 28, GREEN).move_to([-2.0, 3.40, 0])

        # Non-colliding morphine (GREEN) & naloxone (GOLD) tokens strictly below labels (y in 2.52..2.94)
        sol_bounds = (-5.5, 5.5, 2.52, 2.94)
        sim_t = ValueTracker(0.0)
        traj, dt = make_solution_trajectories(4, 7, sol_bounds, seed=7, min_sep=0.55)
        morph_free = [make_token("agonist", 0.13) for _ in range(4)]
        nalox_free = [make_token("competitive", 0.13) for _ in range(7)]

        block_p = ValueTracker(0.0)
        target_idxs = [2, 5, 7, 9, 12, 14, 17]
        bind_state = {"t0": None, "starts": None, "order": list(range(7))}

        def _update_tokens():
            t = sim_t.get_value()
            pts = sample_traj(traj, dt, t)
            bp = block_p.get_value()
            gold_pts = []
            for k, idx in enumerate(target_idxs):
                if bp <= 0.01 or bind_state["starts"] is None:
                    p = np.array([pts[4 + k, 0], pts[4 + k, 1], 0.0])
                else:
                    tok_i = bind_state["order"][k]
                    s = bind_state["starts"][tok_i]
                    dest = row.cups[idx].pocket_pt
                    # Delay slot 9 entry until bound morphine lifts completely clear
                    u = max(0.0, (bp - 0.35) / 0.65) if idx == 9 else bp
                    p = np.array([s[0], s[1], 0.0]) * (1.0 - u) + dest * u
                gold_pts.append(p)

            ag_u = min(1.0, bp * 2.8)
            ag_dest = np.array([row.cups[9].pocket_pt[0] - 0.55, 2.75, 0.0])
            ag_pos = row.cups[9].pocket_pt * (1.0 - ag_u) + ag_dest * ag_u

            free_pts = [np.array([pts[i, 0], pts[i, 1], 0.0]) for i in range(4)]
            if ag_u >= 0.4:
                sep = _separate_green_from_gold(free_pts + [ag_pos], gold_pts, sol_bounds, min_sep=0.46)
                free_pts, ag_pos = sep[:4], sep[4]
            else:
                free_pts = _separate_green_from_gold(free_pts, gold_pts, sol_bounds, min_sep=0.46)

            g = VGroup()
            for i in range(4):
                g.add(morph_free[i].copy().move_to(free_pts[i]))
            g.add(bound_ag.copy().move_to(ag_pos))
            for k in range(7):
                tok_i = bind_state["order"][k] if (bp > 0.01 and bind_state["starts"] is not None) else k
                g.add(nalox_free[tok_i].copy().move_to(gold_pts[k]))
            return g

        tokens = always_redraw(_update_tokens)
        morph_lbl = T("morphine", 28, GREEN).move_to([-4.8, 3.40, 0])
        nalox_lbl = T("naloxone", 28, GOLD).move_to([4.8, 3.40, 0])

        self.add(row, bar, P, curve, schem, tokens, reserve_tag)
        drift_until(self, sim_t, "Naloxone")
        self.play(FadeOut(reserve_tag, run_time=0.3),
                  FadeIn(morph_lbl, run_time=0.35),
                  FadeIn(nalox_lbl, run_time=0.35))
        t0 = sim_t.get_value()
        pts0 = sample_traj(traj, dt, t0)
        bind_state["t0"] = t0
        bind_state["starts"] = [pts0[4 + k].copy() for k in range(7)]
        bind_state["order"] = list(np.argsort(pts0[4:, 0]))
        self.play(
            sim_t.animate(run_time=3.2, rate_func=linear).set_value(sim_t.get_value() + 3.2),
            block_p.animate(run_time=3.2, rate_func=smooth).set_value(1.0),
            resp.animate(run_time=3.2, rate_func=smooth).set_value(0.0),
            curve_col.animate(run_time=3.2, rate_func=smooth).set_value(1.0),
        )
        drift_until(self, sim_t, "How does")
        q_mark = T("?", 90, GOLD, weight=BOLD).move_to(P.pt(-0.4, 58))
        q_label = T("how does the curve shift?", 28, GOLD).move_to([4.6, -1.0, 0])
        self.play(FadeIn(q_mark, shift=UP * 0.2), FadeIn(q_label, shift=UP * 0.15), run_time=0.65)
        drift_to_end(self, sim_t)


class S01Title(TitleCard):
    LESSON = "Binding: Affinity, Occupancy and Dose–Response"
    TITLE = "Blockers and the Shape of a Shift"


class S02Competitive(SpokenScene):
    def construct(self):
        xs = np.linspace(-5.0, 5.0, 6)
        cups = VGroup(*[make_receptor([x, 0.25, 0], width=1.18, height=1.05, stroke_w=5.0) for x in xs])
        mem = make_membrane(-6.0, 6.0, -0.35, stroke_w=6.0)
        resp = ValueTracker(0.0)
        bar = make_response_bar(-3.8, 3.8, -2.35, height=0.54, tracker=resp, color=GREEN, title="response")
        schem = scope_tag("schematic")

        lbl_rec = T("receptor", 28, BLUE).move_to([-4.0, -0.82, 0])
        lbl_blk = T("competitive blocker", 28, GOLD).move_to([-3.6, 3.35, 0])
        lbl_ag = T("agonist", 28, GREEN).move_to([4.6, 3.35, 0])
        lbl_same = T("same site", 28, GOLD).move_to([1.8, -1.10, 0])

        sim_t = ValueTracker(0.0)
        rng = np.random.default_rng(11)
        sol_traj, dt = make_solution_trajectories(12, 8, (-5.5, 5.5, 1.25, 2.70), seed=11, min_sep=0.52)
        flood_offsets = rng.uniform([-5.5, 1.18], [5.5, 2.72], size=(18, 2))
        flood_p = ValueTracker(0.0)

        def _pocket_states(t):
            if t < 4.5:
                return ["gold" if ((t + i * 0.75) % 2.6) < 1.6 else "empty" for i in range(6)]
            if t < 11.4:
                out = []
                for i in range(6):
                    if i == 2:
                        out.append("gold")
                    else:
                        out.append("gold" if ((t + i * 0.9) % 2.8) < 1.7 else "empty")
                return out
            if t < 14.3:
                return ["green" if (i == 2 and t > 12.62) else ("gold" if i in (0, 3, 5) else "empty") for i in range(6)]
            order = [2, 1, 4, 0, 3, 5]
            n_green = int(np.clip(1 + (t - 14.4) / 0.42, 1, 6))
            green_set = set(order[:n_green])
            return ["green" if i in green_set else "gold" for i in range(6)]

        def _draw_scene():
            t = sim_t.get_value()
            pts = sample_traj(sol_traj, dt, t)
            states = _pocket_states(t)
            fp = flood_p.get_value()
            g = VGroup()
            for j in range(8):
                p = pts[12 + j]
                tk = make_token("competitive", 0.25).move_to([p[0], p[1] + fp * 0.15, 0])
                if fp > 0.05:
                    tk.set_opacity(max(0.25, 1.0 - 0.7 * fp))
                g.add(tk)
            if t >= 9.6:
                vis_n = 3 if t < 14.3 else 12
                for i in range(vis_n):
                    if i == 0 and 9.8 <= t < 12.2:
                        px, py, _ = cups[2].pocket_pt
                        if t < 11.0:
                            u = (t - 9.8) / 1.2
                            dy = 1.5 * abs(np.cos(u * PI)) + 0.55
                            tk = make_token("agonist", 0.26).move_to([px, py + dy, 0])
                        else:
                            u = min(1.0, (t - 11.0) / 1.0)
                            tk = make_token("agonist", 0.26).move_to([px + 0.5 * (1 - u), py + 0.7 * (1 - 0.5 * u), 0])
                    else:
                        p = pts[i]
                        tk = make_token("agonist", 0.25).move_to([p[0], p[1], 0])
                    g.add(tk)
            if fp > 0.03:
                for m in range(18):
                    q = flood_offsets[m]
                    tk = make_token("agonist", 0.23).move_to([q[0], q[1] + 0.12 * np.sin(t * 2 + m), 0])
                    tk.set_opacity(min(0.92, fp))
                    g.add(tk)
            for i, st in enumerate(states):
                pt = cups[i].pocket_pt
                if st == "gold":
                    g.add(make_token("competitive", 0.28).move_to(pt))
                elif st == "green":
                    g.add(make_token("agonist", 0.28).move_to(pt))
                    if resp.get_value() > 0.5:
                        arr = Arrow([pt[0], -0.55, 0], [pt[0], -1.72, 0], buff=0.05, color=GREEN, stroke_width=4.5,
                                    max_tip_length_to_length_ratio=0.28)
                        g.add(arr)
            return g

        dyn = always_redraw(_draw_scene)
        self.add(mem, cups, bar, schem, dyn, lbl_rec, lbl_blk)
        drift_until(self, sim_t, "It binds reversibly")
        drift_until(self, sim_t, "One receptor holds")
        self.play(FadeIn(lbl_ag, run_time=0.35), FadeIn(lbl_same, run_time=0.35))
        drift_until(self, sim_t, "never both")
        d1 = max(0.3, self.t_of("Add enough agonist") - 0.2 - self.elapsed())
        self.play(sim_t.animate(run_time=d1 * 0.45, rate_func=linear).set_value(12.6))
        self.play(
            sim_t.animate(run_time=d1 * 0.55, rate_func=linear).set_value(14.2),
            resp.animate(run_time=d1 * 0.55, rate_func=smooth).set_value(17.0),
        )
        d_flood = max(0.4, min(1.9, self.narration_s - self.elapsed() - 0.8))
        self.play(
            FadeOut(lbl_same, run_time=0.25),
            sim_t.animate(run_time=d_flood, rate_func=linear).set_value(16.7),
            flood_p.animate(run_time=d_flood, rate_func=smooth).set_value(1.0),
            resp.animate(run_time=d_flood, rate_func=smooth).set_value(100.0),
        )
        drift_to_end(self, sim_t)


class S03ParallelShift(SpokenScene):
    def construct(self):
        row = make_receptor_row(20, x0=-5.9, x1=5.9, y=2.95, cup_w=0.34, cup_h=0.28, stroke_w=3.2)
        resp = ValueTracker(0.0)
        bar = make_response_bar(-3.0, 3.8, 2.25, height=0.32, tracker=resp, color=GREEN, title="tissue response")
        P = make_dose_plot(box=(-5.2, 4.8, -2.55, 1.42), label_size=26, tick_size=24)
        base_c = P.curve(lambda x: response_pct(x, dr=1.0), color=GREY, width=5.5, opacity=0.75)

        dr_t = ValueTracker(1.0)
        gold_c = always_redraw(lambda: P.curve(lambda x: response_pct(x, dr=dr_t.get_value()),
                                               color=GOLD, width=7.0))

        dose_x = ValueTracker(-2.5)
        bound_ags = always_redraw(lambda: VGroup(*[
            make_token("agonist", 0.11).move_to(row.cups[i].pocket_pt)
            for i in range(int(round(20 * occupancy(dose_x.get_value(), dr=11.0))))
        ]))

        tick_x = ValueTracker(-2.0)
        step_dot = always_redraw(lambda: Dot(P.pt(tick_x.get_value(), 6.0), radius=0.11, color=GOLD, stroke_color=TEXT, stroke_width=2))
        step_lbl = always_redraw(lambda: T("×10", 26, GOLD).next_to(P.pt(tick_x.get_value(), 6.0), UP, buff=0.18))

        self.add(row, bar, P, base_c)

        self.at("multiplies the dose")
        self.add(step_dot, step_lbl)
        d_step = time_left_before(self, "The curve slides right") / 3.0
        for nx in (-1.0, 0.0, 1.0):
            self.play(tick_x.animate.set_value(nx), run_time=max(0.4, d_step * 0.85))
        self.play(FadeOut(step_dot), FadeOut(step_lbl), run_time=0.25)

        self.at("The curve slides right")
        self.add(gold_c)
        d_slide = time_left_before(self, "At every response level")
        self.play(dr_t.animate(run_time=max(0.8, d_slide - 0.45), rate_func=smooth).set_value(11.0))
        lbl_par = T("parallel shift", 28, GOLD).move_to([2.4, 1.76, 0])
        self.play(FadeIn(lbl_par, shift=UP * 0.1), run_time=0.35)

        self.at("At every response level")
        lvl = ValueTracker(20.0)

        def _guide():
            y = lvl.get_value()
            x_a = log_dose_for_response(y, dr=1.0)
            x_b = log_dose_for_response(y, dr=11.0)
            p0 = P.pt(P.xr[0], y)
            pa = P.pt(x_a, y)
            pb = P.pt(x_b, y)
            dash = DashedLine(p0, pb, color=GREY, stroke_width=2.8, dash_length=0.12)
            tick_a = Line(pa + DOWN * 0.14, pa + UP * 0.14, color=GOLD, stroke_width=4.0)
            tick_b = Line(pb + DOWN * 0.14, pb + UP * 0.14, color=GOLD, stroke_width=4.0)
            span = Line(pa, pb, color=GOLD, stroke_width=4.5)
            return VGroup(dash, span, tick_a, tick_b)

        guide = always_redraw(_guide)
        self.add(guide)
        d_sweep = time_left_before(self, "That factor is")
        self.play(lvl.animate(run_time=d_sweep * 0.55, rate_func=smooth).set_value(82.0))
        self.play(lvl.animate(run_time=d_sweep * 0.45, rate_func=smooth).set_value(50.0))

        self.at("That factor is")
        pb_50 = P.pt(log_dose_for_response(50.0, dr=11.0), 50.0)
        lbl_dr = T("dose ratio = 11×", 28, GOLD).next_to(pb_50, RIGHT, buff=0.34).shift(UP * 0.28)
        self.play(FadeIn(lbl_dr, shift=RIGHT * 0.1), run_time=0.45)

        self.at("Enough agonist still")
        bar.add_updater(lambda m: resp.set_value(response_pct(dose_x.get_value(), dr=11.0)))
        dose_dot = always_redraw(lambda: Dot(P.pt(dose_x.get_value(), response_pct(dose_x.get_value(), dr=11.0)),
                                             radius=0.14, color=GOLD, stroke_color=TEXT, stroke_width=2.5))
        self.add(dose_dot, bound_ags)
        d_avail = max(1.2, self.narration_s - self.elapsed() - 0.5)
        d_reach = min(2.0, d_avail * 0.55)
        d_plateau = max(0.5, d_avail - d_reach - 0.35)
        self.play(dose_x.animate(run_time=d_reach, rate_func=smooth).set_value(-0.22))
        lbl_max = T("same maximum", 28, GOLD).move_to([4.6, 1.38, 0])
        self.play(
            dose_x.animate(run_time=d_plateau, rate_func=smooth).set_value(1.3),
            FadeIn(lbl_max, shift=UP * 0.1, run_time=0.35),
        )
        self.finish()


class S04Insurmountable(SpokenScene):
    def construct(self):
        xs = np.linspace(-5.4, 0.6, 6)
        cups = VGroup(*[make_receptor([x, 2.38, 0], width=0.68, height=0.56, has_side=True, stroke_w=3.8) for x in xs])
        mem = make_membrane(-6.0, 1.4, 2.02, stroke_w=5.0)

        resp = ValueTracker(0.0)
        gauge = make_response_bar(2.6, 5.7, 2.38, height=0.48, tracker=resp, color=GREEN, title="")
        gauge_lbl = T("downstream response", 26, GREEN).move_to([4.15, 3.05, 0])
        pathway_arrow = Arrow([1.5, 2.38, 0], [2.45, 2.38, 0], buff=0.05, color=GREEN, stroke_width=4.5,
                              max_tip_length_to_length_ratio=0.28)

        P = make_dose_plot(box=(-5.4, 3.2, -2.55, 1.18), label_size=26, tick_size=24)
        base_c = P.curve(lambda x: response_pct(x, dr=1.0), color=GREY, width=5.0, opacity=0.75)
        schem = scope_tag("schematic")

        # Carried world visible at t=0; immediately preview insurmountable ceiling and blocker tokens
        self.add(mem, cups, pathway_arrow, gauge, gauge_lbl, P, base_c, schem)
        purp_tokens = VGroup(*[make_token("noncompetitive", 0.14).move_to(c.side_pt + RIGHT * 0.35 + UP * 0.65) for c in cups])
        ceil_line = DashedLine(P.pt(-3.4, 45.0), P.pt(2.5, 45.0), color=PURPLE, stroke_width=3.2, dash_length=0.14)
        ceil_line.layout_ok = "covered"
        ceil_arr = Arrow(P.pt(1.5, 96.0), P.pt(1.5, 47.0), buff=0.05, color=PURPLE, stroke_width=4.0,
                         max_tip_length_to_length_ratio=0.18)
        lbl_insurm = T("lower ceiling", 24, PURPLE).next_to(ceil_arr, LEFT, buff=0.18)
        d_intro = time_left_before(self, "non competitive blocker")
        self.play(FadeIn(purp_tokens, shift=DOWN * 0.1, run_time=0.45),
                  Create(ceil_line, run_time=max(0.8, d_intro * 0.40)))
        self.play(GrowArrow(ceil_arr, run_time=max(0.5, d_intro * 0.25)),
                  FadeIn(lbl_insurm, run_time=0.4),
                  *[t.animate(run_time=max(0.6, d_intro * 0.35)).move_to(c.side_pt + RIGHT * 0.35 + UP * 0.35)
                    for t, c in zip(purp_tokens, cups)])

        # Beat 1: PURPLE non-competitive blocker
        self.at("non competitive blocker")
        lbl_nc = T("non-competitive blocker", 28, PURPLE).move_to([-2.7, 3.42, 0])
        clamp = RoundedRectangle(corner_radius=0.08, width=0.24, height=0.70, color=PURPLE,
                                 fill_color=PURPLE, fill_opacity=0.88, stroke_color=TEXT, stroke_width=2.0)
        clamp_dest = np.array([2.6 + 0.45 * (5.7 - 2.6), 2.38, 0.0])
        clamp.move_to(clamp_dest + DOWN * 0.58)
        d_nc = time_left_before(self, "Even with every")
        self.play(FadeOut(lbl_insurm, run_time=0.25),
                  FadeOut(ceil_arr, run_time=0.25),
                  FadeIn(lbl_nc, run_time=0.35),
                  *[t.animate(run_time=max(0.8, d_nc * 0.55)).move_to(c.side_pt) for t, c in zip(purp_tokens, cups)])
        self.play(clamp.animate(run_time=max(0.6, d_nc * 0.45)).move_to(clamp_dest))

        self.at("Even with every")
        ag_tokens = VGroup(*[make_token("agonist", 0.16).move_to(c.pocket_pt + UP * 0.48) for c in cups])
        d_ag = time_left_before(self, "the response hits")
        self.play(*[a.animate(run_time=max(0.6, d_ag)).move_to(c.pocket_pt) for a, c in zip(ag_tokens, cups)])

        self.at("the response hits")
        dx = ValueTracker(-3.2)
        purp_live = P.live_curve(lambda x: noncomp_schematic(x, cap=45.0), dx, color=PURPLE, width=7.0)
        purp_dot = P.dot(lambda: dx.get_value(), lambda: noncomp_schematic(dx.get_value(), cap=45.0),
                         color=PURPLE, ring=TEXT, radius=0.12)
        purp_upd = lambda m: resp.set_value(noncomp_schematic(dx.get_value(), cap=45.0))
        gauge.add_updater(purp_upd)
        self.add(purp_live, purp_dot)
        d_purp = time_left_before(self, "An irreversible blocker")
        self.play(dx.animate(run_time=min(1.05, max(0.8, d_purp - 0.6)), rate_func=smooth).set_value(2.2))
        lbl_low = T("lower maximum", 28, PURPLE).move_to([4.8, -0.35, 0])
        self.play(FadeIn(lbl_low, shift=UP * 0.1), run_time=0.35)

        # Beat 2: Clear PURPLE cleanly, introduce RED irreversible blocker with covalent lock on 5 of 6 cups
        self.at("An irreversible blocker")
        gauge.remove_updater(purp_upd)
        self.play(FadeOut(purp_tokens), FadeOut(ag_tokens), FadeOut(clamp), FadeOut(lbl_nc),
                  FadeOut(purp_live), FadeOut(purp_dot), FadeOut(lbl_low), FadeOut(ceil_line),
                  resp.animate.set_value(0.0), run_time=0.55)

        lbl_irr = T("irreversible blocker", 28, RED).move_to([-2.7, 3.42, 0])
        red_tokens = VGroup(*[make_token("irreversible", 0.16).move_to(c.pocket_pt + UP * 0.48) for c in cups[:5]])
        locks = VGroup(*[make_lock_badge(c.pocket_pt + DOWN * 0.24, scale=0.95) for c in cups[:5]])
        d_irr = time_left_before(self, "cannot be washed")
        self.play(FadeIn(lbl_irr, run_time=0.35),
                  *[r.animate(run_time=min(1.6, d_irr * 0.55)).move_to(c.pocket_pt) for r, c in zip(red_tokens, cups[:5])])
        self.play(FadeIn(locks, run_time=0.4))
        lbl_cov = T("covalent bond", 26, RED).move_to([0.2, 1.62, 0])
        self.play(FadeIn(lbl_cov, run_time=0.35))

        self.at("cannot be washed")
        bounce_ags = VGroup(*[make_token("agonist", 0.15).move_to(c.pocket_pt + UP * 0.52) for c in cups[:4]])
        surv_ag = make_token("agonist", 0.16).move_to(cups[5].pocket_pt + UP * 0.52)
        dx_r = ValueTracker(-3.2)
        red_live = P.live_curve(lambda x: response_pct(x, dr=1.0, surviving=0.02), dx_r, color=RED, width=7.0)
        red_dot = P.dot(lambda: dx_r.get_value(), lambda: response_pct(dx_r.get_value(), dr=1.0, surviving=0.02),
                        color=RED, ring=TEXT, radius=0.12)
        red_upd = lambda m: resp.set_value(response_pct(dx_r.get_value(), dr=1.0, surviving=0.02))
        gauge.add_updater(red_upd)
        self.add(red_live, red_dot)
        d_red = min(1.05, max(0.8, self.narration_s - self.elapsed() - 0.5))
        self.play(
            *[a.animate(run_time=min(0.95, d_red * 0.9), rate_func=there_and_back).shift(DOWN * 0.32) for a in bounce_ags],
            surv_ag.animate(run_time=min(0.85, d_red * 0.75), rate_func=smooth).move_to(cups[5].pocket_pt),
            dx_r.animate(run_time=d_red, rate_func=smooth).set_value(2.2),
        )
        lbl_low_r = T("lower maximum", 28, RED).move_to([4.8, -0.85, 0])
        self.play(FadeOut(bounce_ags, run_time=0.25), FadeIn(lbl_low_r, run_time=0.3))
        self.finish()


class S05PredictQuestion(SpokenScene):
    def construct(self):
        row = make_receptor_row(20, x0=-5.9, x1=5.9, y=1.95, cup_w=0.38, cup_h=0.32, stroke_w=3.4)
        P = make_dose_plot(box=(-5.2, 3.8, -2.65, 0.72), label_size=26, tick_size=24)
        base_c = P.curve(lambda x: response_pct(x, dr=1.0), color=GREY, width=5.0, opacity=0.75)
        base_tag = T("baseline", 26, GREY).move_to([-4.45, -0.85, 0])

        xs = [-2.5, -0.4, 1.7, 3.8]
        drift_t = ValueTracker(0.0)
        whites = always_redraw(lambda: VGroup(*[
            make_token("unknown", 0.14).move_to([
                x + 0.24 * np.sin(drift_t.get_value() * 1.4 + i),
                2.48 + 0.06 * np.cos(drift_t.get_value() * 1.8 + i),
                0
            ]) for i, x in enumerate(xs)
        ]))
        w_lbl = T("unknown blocker", 28, TEXT).move_to([-4.65, 2.48, 0])

        dr_t = ValueTracker(1.0)
        white_c = always_redraw(lambda: P.curve(lambda x: response_pct(x, dr=dr_t.get_value()),
                                                color=TEXT, width=6.8))

        self.add(row, whites, w_lbl, P, base_c, base_tag)
        drift_until(self, drift_t, "The agonist curve")

        self.add(white_c)
        self.play(
            dr_t.animate(run_time=2.4, rate_func=smooth).set_value(2.0),
            drift_t.animate(run_time=2.4, rate_func=linear).set_value(drift_t.get_value() + 2.4),
        )
        dot_x = ValueTracker(-1.3)
        w_dot = always_redraw(lambda: Dot(P.pt(dot_x.get_value(), response_pct(dot_x.get_value(), dr=2.0)),
                                          radius=0.13, color=TEXT, stroke_color=TEAL, stroke_width=2.5))
        self.add(w_dot)
        self.play(
            dot_x.animate(run_time=1.8, rate_func=smooth).set_value(0.2),
            drift_t.animate(run_time=1.8, rate_func=linear).set_value(drift_t.get_value() + 1.8),
        )
        shift_tag = T("with blocker (100% max)", 26, TEXT).move_to([1.9, -0.35, 0])
        self.play(FadeOut(w_dot, run_time=0.25), FadeIn(shift_tag, run_time=0.35))

        drift_until(self, drift_t, "Does that single")
        q = T("One parallel shift = competitive blocker?", 30, GOLD).move_to([-1.1, 3.22, 0])
        choice_box = RoundedRectangle(corner_radius=0.10, width=1.6, height=0.54,
                                      stroke_color=GOLD, stroke_width=3.0, fill_color=BG, fill_opacity=0.92)
        choice_box.move_to([5.2, 3.22, 0])
        q_mark = T("?", 30, GOLD).move_to(choice_box)
        self.play(FadeIn(q), FadeIn(choice_box), FadeIn(q_mark), run_time=0.55)

        rest = max(0.2, self.narration_s - self.elapsed())
        next_pi = np.ceil((drift_t.get_value() + rest) / TAU) * TAU
        self.play(drift_t.animate(run_time=rest, rate_func=linear).set_value(next_pi))
        self.finish()


class S06PredictPause(PredictPause):
    QUESTION = "One parallel shift = competitive blocker?"
    CARD = {"y": 3.22, "max_w": 9.2, "size": 30}
    RING_AT = (5.9, -3.05, 0)
    SECONDS = 4.5

    def backdrop(self):
        bg, _ = build_predict_backdrop()
        return bg


class S07Reveal(SpokenScene):
    def construct(self):
        bg, choice = build_predict_backdrop()
        row = bg[0]
        whites = bg[1]
        w_lbl = bg[2]
        P = bg[3]
        white_c = bg[5]
        shift_tag = bg[7]
        self.add(bg)

        # Immediately replace '?' choice marker with 'Not from one dose'
        not_lbl = boxed_label("Not from one dose", RED, size=26).move_to([4.6, 3.22, 0])
        self.play(swap(choice, not_lbl, run_time=0.6))

        self.at("a small irreversible")
        # Swap out hovering unknown tokens/label as irreversible RED locks take over receptors
        rem_lbl = T("50% receptors locked", 26, RED).move_to([-4.2, 2.65, 0])
        locks_50 = VGroup(*[make_token("irreversible", 0.12).move_to(row.cups[i].pocket_pt) for i in range(0, 20, 2)])
        dx_r1 = ValueTracker(-3.2)
        red_50 = P.live_curve(lambda x: response_pct(x, dr=1.0, surviving=0.5), dx_r1, color=RED, width=6.0)
        self.add(red_50)
        d_r1 = time_left_before(self, "Only higher doses")
        self.play(
            FadeOut(whites, run_time=0.3),
            swap(w_lbl, rem_lbl, run_time=0.35),
            FadeIn(locks_50, run_time=0.45),
            dx_r1.animate(run_time=max(0.8, d_r1 - 0.5), rate_func=smooth).set_value(2.2),
        )

        self.at("Only higher doses")
        self.play(FadeOut(white_c), FadeOut(shift_tag), run_time=0.25)

        gold_2 = P.curve(lambda x: response_pct(x, dr=2.0), color=GOLD, width=5.5)
        gold_11 = P.curve(lambda x: response_pct(x, dr=11.0), color=GOLD, width=5.5)
        dx_g101 = ValueTracker(-1.0)
        gold_101 = P.live_curve(lambda x: response_pct(x, dr=101.0), dx_g101, color=GOLD, width=6.5)

        locks_90 = VGroup(*[make_token("irreversible", 0.12).move_to(row.cups[i].pocket_pt)
                            for i in range(20) if i % 2 == 1 and i < 16])
        rem_lbl_90 = T("90% receptors locked", 26, RED).move_to([-4.2, 2.65, 0])
        dx_r2 = ValueTracker(-2.5)
        red_90 = P.live_curve(lambda x: response_pct(x, dr=1.0, surviving=0.1), dx_r2, color=RED, width=6.0)

        self.add(red_90, gold_101)
        d_sep = time_left_before(self, "To name the")
        self.play(
            Create(gold_2, run_time=0.5),
            Create(gold_11, run_time=0.6),
            swap(rem_lbl, rem_lbl_90, run_time=0.32),
            FadeIn(locks_90, run_time=0.45),
            dx_r2.animate(run_time=max(0.8, d_sep - 0.3), rate_func=smooth).set_value(2.2),
            dx_g101.animate(run_time=max(0.8, d_sep - 0.3), rate_func=smooth).set_value(2.2),
        )

        self.at("To name the")
        locks_98 = VGroup(*[make_token("irreversible", 0.12).move_to(row.cups[i].pocket_pt) for i in (17, 19)])
        rem_lbl_98 = T(">95% receptors locked", 26, RED).move_to([-4.2, 2.65, 0])
        dx_r3 = ValueTracker(-2.0)
        red_98 = P.live_curve(lambda x: response_pct(x, dr=1.0, surviving=0.02), dx_r3, color=RED, width=6.8)
        self.add(red_98)
        d_fin = max(0.8, self.narration_s - self.elapsed() - 0.6)
        self.play(
            swap(rem_lbl_90, rem_lbl_98, run_time=0.32),
            FadeIn(locks_98, run_time=0.4),
            dx_r3.animate(run_time=min(2.2, d_fin), rate_func=smooth).set_value(2.4),
        )

        lbl_comp = T("competitive: same ceiling", 26, GOLD).move_to([4.15, 0.92, 0])
        lbl_irr = T("irreversible: ceiling drops", 26, RED).move_to([4.15, -0.82, 0])
        self.play(FadeIn(lbl_comp, shift=UP * 0.1), FadeIn(lbl_irr, shift=UP * 0.1), run_time=0.45)
        self.finish()


class S08SchildPlot(SpokenScene):
    def construct(self):
        P_left = make_dose_plot(box=(-5.7, -1.1, -2.05, 2.20), xlabel="log dose", ylabel="response (%)",
                                label_size=26, tick_size=22)
        base_c = P_left.curve(lambda x: response_pct(x, dr=1.0), color=GREY, width=5.5, opacity=0.80)
        c2 = P_left.curve(lambda x: response_pct(x, dr=2.0), color=GOLD, width=6.5)
        c11 = P_left.curve(lambda x: response_pct(x, dr=11.0), color=GOLD, width=6.5)
        c101 = P_left.curve(lambda x: response_pct(x, dr=101.0), color=GOLD, width=6.5)

        P_schild = make_schild_plot(box=(0.45, 5.95, -2.05, 2.20), label_size=28, tick_size=24)
        self.add(P_left, base_c, c2, c11, c101, P_schild)

        self.at("made rising blocker")
        b_step = ValueTracker(-0.2)
        # Shaded vertical sweep band across Schild x-axis (visible motion across full plot height)
        b_band = always_redraw(lambda: Rectangle(
            width=0.55,
            height=P_schild.pt(0, 2.5)[1] - P_schild.pt(0, -0.5)[1],
            stroke_width=0, fill_color=GOLD, fill_opacity=0.16,
        ).move_to([P_schild.pt(b_step.get_value(), 1.0)[0], P_schild.pt(0, 1.0)[1], 0]).set_z_index(-1))
        b_dot = always_redraw(lambda: Dot(P_schild.pt(b_step.get_value(), -0.15), radius=0.15, color=GOLD,
                                          stroke_color=TEXT, stroke_width=2.2))
        b_bar = always_redraw(lambda: Line(P_schild.pt(-0.2, -0.15), P_schild.pt(b_step.get_value(), -0.15),
                                           color=GOLD, stroke_width=6.0))
        self.add(b_band, b_bar, b_dot)
        d_b = time_left_before(self, "Raise the blocker")
        self.play(b_step.animate(run_time=max(0.8, d_b - 0.3), rate_func=smooth).set_value(2.0))
        self.play(FadeOut(b_dot), FadeOut(b_bar), FadeOut(b_band), run_time=0.25)

        self.at("Raise the blocker")
        ten_lbl = T("×10 blocker per step", 28, GOLD).move_to([3.5, 3.22, 0])
        # Illuminate curves 11 and 101 sequentially with moving tracer dots + step arcs
        hi_x = ValueTracker(-2.5)
        hi_11 = P_left.dot(lambda: hi_x.get_value(), lambda: response_pct(hi_x.get_value(), dr=11.0),
                           color=GOLD, ring=TEXT, radius=0.14)
        hi_101 = P_left.dot(lambda: hi_x.get_value(), lambda: response_pct(hi_x.get_value(), dr=101.0),
                            color=GOLD, ring=TEXT, radius=0.14)
        arc1 = CurvedArrow(P_schild.pt(0.05, -0.15), P_schild.pt(0.95, -0.15), angle=0.5, color=GOLD, stroke_width=4.5)
        arc2 = CurvedArrow(P_schild.pt(1.05, -0.15), P_schild.pt(1.95, -0.15), angle=0.5, color=GOLD, stroke_width=4.5)
        d_raise = time_left_before(self, "Simple competition")
        self.add(hi_11)
        self.play(FadeIn(ten_lbl, shift=UP * 0.1), Create(arc1),
                  hi_x.animate(run_time=max(0.5, d_raise * 0.45)).set_value(1.2))
        self.remove(hi_11)
        hi_x.set_value(-1.5)
        self.add(hi_101)
        self.play(Create(arc2), hi_x.animate(run_time=max(0.5, d_raise * 0.45)).set_value(1.8))
        self.remove(hi_101)

        self.at("Simple competition")
        self.play(FadeOut(arc1), FadeOut(arc2), run_time=0.25)
        # Sweep horizontal shaded guide band up through y=15, 50, 78 while growing each bracket
        band_y = ValueTracker(0.0)
        h_band = always_redraw(lambda: Rectangle(
            width=P_left.pt(P_left.xr[1], 0)[0] - P_left.pt(P_left.xr[0], 0)[0],
            height=0.30,
            stroke_width=0, fill_color=GOLD, fill_opacity=0.14,
        ).move_to([(P_left.pt(P_left.xr[0], 0)[0] + P_left.pt(P_left.xr[1], 0)[0]) / 2,
                   P_left.pt(0, band_y.get_value())[1], 0]).set_z_index(-1))
        self.add(h_band)
        brackets = []
        guides = []
        bracket_specs = ((14, 2.0, "2", 0.20), (50, 11.0, "11", 0.10), (78, 101.0, "101", 0.10))
        for y_lvl, dr, lbl_txt, lb_buff in bracket_specs:
            p0 = P_left.pt(P_left.xr[0], y_lvl)
            xa = P_left.pt(log_dose_for_response(y_lvl, dr=1.0), y_lvl)
            xb = P_left.pt(log_dose_for_response(y_lvl, dr=dr), y_lvl)
            gd = DashedLine(p0, xa, color=GREY, stroke_width=2.8, dash_length=0.10)
            br = VGroup(
                Line(xa, xb, color=GOLD, stroke_width=6.0),
                Line(xa + DOWN * 0.10, xa + UP * 0.10, color=GOLD, stroke_width=4.0),
                Line(xb + DOWN * 0.10, xb + UP * 0.10, color=GOLD, stroke_width=4.0),
                T(lbl_txt, 24, GOLD).next_to(xb, RIGHT, buff=lb_buff),
            )
            guides.append(gd)
            brackets.append((y_lvl, br))
        d_br = time_left_before(self, "Subtract 1")
        for gd, (y_lvl, br) in zip(guides, brackets):
            self.play(band_y.animate(run_time=max(0.5, d_br / 3.4 * 0.45)).set_value(y_lvl))
            self.play(Create(gd, run_time=0.3), GrowFromCenter(br, run_time=max(0.5, d_br / 3.4 * 0.55)))
        self.play(FadeOut(h_band, run_time=0.25))

        self.at("Subtract 1")
        pts = [P_schild.pt(k, k) for k in (0, 1, 2)]
        dots = [Dot(p, radius=0.16, color=GOLD, stroke_color=TEXT, stroke_width=2.4) for p in pts]
        drop_lines = [
            VGroup(
                DashedLine(P_schild.pt(k, -0.5), pts[k], color=GOLD, stroke_width=3.0, dash_length=0.10).set_opacity(0.75),
                DashedLine(P_schild.pt(-0.5, k), pts[k], color=GOLD, stroke_width=3.0, dash_length=0.10).set_opacity(0.75),
            )
            for k in (0, 1, 2)
        ]
        # Shaded projection squares for (1,1) and (2,2) to highlight coordinate growth cleanly
        proj_rects = [
            None,
            Polygon(P_schild.pt(0, 0), P_schild.pt(1, 0), P_schild.pt(1, 1), P_schild.pt(0, 1),
                    stroke_width=0, fill_color=GOLD, fill_opacity=0.09).set_z_index(-1),
            Polygon(P_schild.pt(0, 0), P_schild.pt(2, 0), P_schild.pt(2, 2), P_schild.pt(0, 2),
                    stroke_width=0, fill_color=GOLD, fill_opacity=0.07).set_z_index(-1),
        ]
        eq_labels = [
            T("2 − 1 = 1", 26, GOLD).next_to(pts[0], RIGHT, buff=0.24).shift(DOWN * 0.12),
            T("11 − 1 = 10", 26, GOLD).next_to(pts[1], UL, buff=0.18),
            T("101 − 1 = 100", 26, GOLD).next_to(pts[2], UL, buff=0.18),
        ]
        d_sub = time_left_before(self, "That leaves 1")
        for (_, br), d, dl, pr in zip(brackets, dots, drop_lines, proj_rects):
            anims = [ReplacementTransform(br[0].copy(), d, run_time=max(0.55, d_sub / 3.2 - 0.2)),
                     Create(dl, run_time=0.4)]
            if pr is not None:
                anims.append(FadeIn(pr, run_time=0.45))
            self.play(*anims)

        self.at("That leaves 1")
        d_lv = time_left_before(self, "As logs against")
        for lbl in eq_labels:
            self.play(FadeIn(lbl, shift=UP * 0.08), run_time=max(0.45, d_lv / 3.2))

        self.at("As logs against")
        sx = ValueTracker(-0.25)
        schild_line = P_schild.live_curve(lambda x: x, sx, x0=-0.25, color=GOLD, width=8.0)
        s_dot = P_schild.dot(lambda: sx.get_value(), lambda: sx.get_value(), color=GOLD, ring=TEXT, radius=0.15)
        self.add(schild_line, s_dot)
        d_line = max(0.8, self.narration_s - self.elapsed() - 0.9)
        self.play(sx.animate(run_time=d_line * 0.62, rate_func=smooth).set_value(2.25))
        self.play(FadeOut(s_dot, run_time=0.2))

        p11, p21, p22 = P_schild.pt(1, 1), P_schild.pt(2, 1), P_schild.pt(2, 2)
        tri_fill = Polygon(p11, p21, p22, stroke_width=0, fill_color=GOLD, fill_opacity=0.28)
        tri = VGroup(
            tri_fill,
            DashedLine(p11, p21, color=GOLD, stroke_width=4.5),
            DashedLine(p21, p22, color=GOLD, stroke_width=4.5),
        )
        slope_lbl = T("slope = 1", 28, GOLD).next_to(p21, DR, buff=0.16)
        self.play(FadeIn(tri), FadeIn(slope_lbl), run_time=max(0.5, d_line * 0.35))
        self.finish()


class S09Assumptions(SpokenScene):
    def construct(self):
        P = make_schild_plot(box=(-2.65, 2.85, -1.85, 2.45), label_size=28, tick_size=24)
        ref_line = P.curve(lambda x: x, x0=-0.3, x1=2.3, color=GOLD, width=5.5, opacity=0.45)
        ref_pts = VGroup(*[Dot(P.pt(k, k), radius=0.10, color=GOLD).set_opacity(0.45) for k in (0, 1, 2)])
        schem = scope_tag("schematic")

        self.add(P, ref_line, ref_pts, schem)

        self.at("A different slope")
        tx = ValueTracker(-0.3)
        slope_live = P.live_curve(lambda x: 0.55 * x + 0.25, tx, x0=-0.3, color=ORANGE, width=8.0)
        bend_fn = lambda x: x - 0.55 * max(0.0, x - 0.65) ** 2
        bend_live = P.live_curve(bend_fn, tx, x0=-0.3, color=TEAL, width=8.0)
        self.add(slope_live, bend_live)
        d_curves = time_left_before(self, "Equilibrium may not")
        self.play(tx.animate(run_time=max(1.0, d_curves - 0.5), rate_func=smooth).set_value(2.2))

        lbl_slp = T("slope not 1", 26, ORANGE).next_to(P.pt(2.2, 1.46), RIGHT, buff=0.18).shift(UP * 0.15)
        lbl_crv = T("curves at high dose", 26, TEAL).next_to(P.pt(2.2, bend_fn(2.2)), RIGHT, buff=0.18).shift(DOWN * 0.20)
        self.play(FadeIn(lbl_slp), FadeIn(lbl_crv), run_time=0.4)

        b1 = boxed_label("not at equilibrium", ORANGE, size=24).move_to([-5.05, 1.65, 0])
        b2 = boxed_label("agonist removed", ORANGE, size=24).move_to([-5.05, 0.30, 0])
        b3 = boxed_label("binds elsewhere", TEAL, size=24).move_to([4.95, 2.35, 0])
        b4 = boxed_label("second receptor", TEAL, size=24).move_to([4.95, -1.15, 0])

        self.at("Equilibrium may not")
        self.play(FadeIn(b1, shift=RIGHT * 0.12), run_time=0.65)
        self.at("the tissue may")
        self.play(FadeIn(b2, shift=RIGHT * 0.12), run_time=0.65)
        self.at("A blocker binding")
        self.play(FadeIn(b3, shift=LEFT * 0.12), run_time=0.65)
        self.at("a second receptor")
        self.play(FadeIn(b4, shift=LEFT * 0.12), run_time=0.65)

        self.at("Even slope 1")
        p_a, p_b = P.pt(-0.2, -0.2), P.pt(0.65, 0.65)
        win = RoundedRectangle(corner_radius=0.12, width=abs(p_b[0] - p_a[0]) + 0.35,
                               height=abs(p_b[1] - p_a[1]) + 0.35,
                               stroke_color=GOLD, stroke_width=4.0, fill_color=GOLD, fill_opacity=0.10)
        win.move_to((p_a + p_b) / 2)
        win.layout_ok = True
        inc_lbl = T("narrow range: inconclusive", 28, GOLD).move_to([0.0, -3.22, 0])
        d_inc = max(0.8, self.narration_s - self.elapsed() - 0.3)
        self.play(Create(win, run_time=min(1.2, d_inc * 0.6)), FadeIn(inc_lbl, shift=UP * 0.1, run_time=0.5))
        self.finish()


class S10NaloxoneScope(SpokenScene):
    def construct(self):
        row = make_receptor_row(20, x0=-5.9, x1=5.9, y=2.15, cup_w=0.38, cup_h=0.32, stroke_w=3.4)
        mu_lbl = T("mu-opioid receptor", 28, BLUE).move_to([-4.2, 3.40, 0])
        P = make_dose_plot(box=(-5.4, 2.2, -2.65, 0.85), label_size=26, tick_size=24)
        base_c = P.curve(lambda x: response_pct(x, dr=1.0), color=GREY, width=4.8, opacity=0.70)

        dr_t = ValueTracker(1.0)
        # Starts GREEN (unblocked morphine curve) and turns GOLD as naloxone shifts it right
        morph_c = always_redraw(lambda: P.curve(
            lambda x: response_pct(x, dr=dr_t.get_value()),
            color=interpolate_color(ManimColor(GREEN), ManimColor(GOLD),
                                    float(np.clip((dr_t.get_value() - 1.0) / 10.0, 0.0, 1.0))),
            width=7.0,
        ))
        fixed_x = -1.25
        vline = DashedLine(P.pt(fixed_x, 0), P.pt(fixed_x, 102), color=GREEN, stroke_width=3.0)
        sig_dot = P.dot(lambda: fixed_x, lambda: response_pct(fixed_x, dr=dr_t.get_value()),
                        color=GREEN, ring=TEXT, radius=0.14)

        sig_outer = RoundedRectangle(corner_radius=0.10, width=0.62, height=2.6,
                                     stroke_color=GREY, stroke_width=2.8, fill_color=BG, fill_opacity=0.95)
        sig_outer.move_to([3.4, -0.9, 0])
        sig_title = T("signalling", 28, GREEN).next_to(sig_outer, UP, buff=0.18)

        def _sig_fill():
            pct = response_pct(fixed_x, dr=dr_t.get_value()) / 100.0
            fh = max(0.03, pct * 2.46)
            r = RoundedRectangle(corner_radius=0.05, width=0.50, height=fh,
                                 stroke_width=0, fill_color=GREEN, fill_opacity=0.92)
            r.move_to([3.4, -0.9 - 1.23 + fh / 2, 0])
            return r

        sig_fill = always_redraw(_sig_fill)
        sig_num = always_redraw(lambda: M(f"{response_pct(fixed_x, dr=dr_t.get_value()):.0f}%", 28, TEXT)
                                .next_to(sig_outer, DOWN, buff=0.18))
        schem = scope_tag("schematic")

        # Non-colliding morphine/naloxone tokens strictly below mu_lbl (y in 2.52..2.94)
        sol_bounds = (-5.5, 5.5, 2.52, 2.94)
        sim_t = ValueTracker(0.0)
        traj, dt = make_solution_trajectories(6, 7, sol_bounds, seed=19, min_sep=0.55)
        morph_tk = [make_token("agonist", 0.13) for _ in range(6)]
        bound_morph = make_token("agonist", 0.13)
        nalox_tk = [make_token("competitive", 0.13) for _ in range(7)]
        comp_p = ValueTracker(0.0)
        bound_slots = [9]  # 1/20 occupied = 5% reserve = 100% response
        nalox_slots = [2, 4, 6, 9, 11, 15, 17]
        bind_state = {"t0": None, "starts": None, "order": list(range(7))}

        def _draw_tokens():
            t = sim_t.get_value()
            pts = sample_traj(traj, dt, t)
            cp = comp_p.get_value()
            gold_pts = []
            for j, slot in enumerate(nalox_slots):
                if cp <= 0.02 or bind_state["starts"] is None:
                    p = np.array([pts[6 + j, 0], pts[6 + j, 1], 0.0])
                else:
                    tok_j = bind_state["order"][j]
                    s = bind_state["starts"][tok_j]
                    dest = row.cups[slot].pocket_pt
                    u = max(0.0, (cp - 0.35) / 0.65) if slot == bound_slots[0] else cp
                    p = np.array([s[0], s[1], 0.0]) * (1.0 - u) + dest * u
                gold_pts.append(p)

            ag_u = min(1.0, cp * 2.8)
            ag_dest = np.array([row.cups[bound_slots[0]].pocket_pt[0] - 0.55, 2.75, 0.0])
            ag_pos = row.cups[bound_slots[0]].pocket_pt * (1.0 - ag_u) + ag_dest * ag_u

            free_pts = [np.array([pts[i, 0], pts[i, 1], 0.0]) for i in range(6)]
            if ag_u >= 0.4:
                sep = _separate_green_from_gold(free_pts + [ag_pos], gold_pts, sol_bounds, min_sep=0.46)
                free_pts, ag_pos = sep[:6], sep[6]
            else:
                free_pts = _separate_green_from_gold(free_pts, gold_pts, sol_bounds, min_sep=0.46)

            g = VGroup()
            g.add(bound_morph.copy().move_to(ag_pos))
            for i in range(6):
                g.add(morph_tk[i].copy().move_to(free_pts[i]))
            for j in range(7):
                tok_j = bind_state["order"][j] if (cp > 0.02 and bind_state["starts"] is not None) else j
                g.add(nalox_tk[tok_j].copy().move_to(gold_pts[j]))
            return g

        tokens = always_redraw(_draw_tokens)

        self.add(row, mu_lbl, P, base_c, morph_c, vline, sig_dot, sig_outer, sig_fill, sig_title, sig_num, schem, tokens)
        drift_until(self, sim_t, "naloxone fills")
        t0 = sim_t.get_value()
        pts0 = sample_traj(traj, dt, t0)
        bind_state["t0"] = t0
        bind_state["starts"] = [pts0[6 + j].copy() for j in range(7)]
        bind_state["order"] = list(np.argsort(pts0[6:, 0]))
        d_act = min(9.5, time_left_before(self, "Yet clinical reversal") - 1.5)
        self.play(
            sim_t.animate(run_time=d_act, rate_func=linear).set_value(sim_t.get_value() + d_act),
            comp_p.animate(run_time=d_act, rate_func=smooth).set_value(1.0),
            dr_t.animate(run_time=d_act, rate_func=smooth).set_value(11.0),
        )
        drift_until(self, sim_t, "Yet clinical reversal")

        clock_c = np.array([5.35, 0.25, 0.0])
        clock_rim = Circle(radius=0.46, color=GOLD, stroke_width=4.0).move_to(clock_c)
        clock_t = ValueTracker(0.0)
        clock_hand = always_redraw(lambda: Line(
            clock_c,
            clock_c + 0.35 * np.array([np.sin(clock_t.get_value()), np.cos(clock_t.get_value()), 0.0]),
            color=GOLD, stroke_width=4.0,
        ))
        clock_lbl = T("clinical reversal:\ntime-dependent", 24, GOLD).next_to(clock_rim, DOWN, buff=0.16)
        eq_tag = T("equilibrium ratio", 24, GREY).move_to([5.35, -1.65, 0])
        self.play(FadeIn(clock_rim), FadeIn(clock_lbl), FadeIn(eq_tag), run_time=0.55)
        self.add(clock_hand)

        rest = max(0.2, self.narration_s - self.elapsed())
        self.play(
            sim_t.animate(run_time=rest, rate_func=linear).set_value(sim_t.get_value() + rest),
            clock_t.animate(run_time=rest, rate_func=linear).set_value(TAU * 1.5),
        )
        self.finish()


class S11Handoff(SpokenScene):
    def construct(self):
        row = make_receptor_row(20, x0=-5.9, x1=5.9, y=2.65, cup_w=0.35, cup_h=0.28, stroke_w=3.2)
        P = make_dose_plot(box=(-5.4, 1.1, -2.55, 1.55), label_size=26, tick_size=22)
        base_c = P.curve(lambda x: response_pct(x, dr=1.0), color=GREY, width=5.0, opacity=0.70)
        g2 = P.curve(lambda x: response_pct(x, dr=2.0), color=GOLD, width=6.5)
        g11 = P.curve(lambda x: response_pct(x, dr=11.0), color=GOLD, width=6.5)
        g101 = P.curve(lambda x: response_pct(x, dr=101.0), color=GOLD, width=6.5)
        r_drop = P.curve(lambda x: response_pct(x, dr=1.0, surviving=0.02), color=RED, width=7.0)

        # Downstream GREEN amplifier gauge visible on lower right, covered at cue by frosted box
        amp_t = ValueTracker(0.0)
        amp_bar = make_response_bar(2.5, 5.7, -2.05, height=0.44, tracker=amp_t, color=GREEN, title="", show_pct=False)
        amp_lbl = T("downstream amplifier", 24, GREEN).move_to([4.1, -1.45, 0])

        P_s = make_schild_plot(box=(2.5, 5.8, -0.2, 1.55), label_size=22, tick_size=22)
        s_line = P_s.curve(lambda x: x, x0=-0.2, x1=2.2, color=GOLD, width=4.5).set_opacity(0.6)
        schild_group = VGroup(P_s, s_line).set_opacity(0.70)

        self.add(row, P, base_c, g2, g11, g101, r_drop, schild_group, amp_bar, amp_lbl)

        dx = ValueTracker(-3.0)
        g_dot = P.dot(lambda: dx.get_value(), lambda: response_pct(dx.get_value(), dr=11.0),
                      color=GOLD, ring=TEXT, radius=0.12)
        r_dot = P.dot(lambda: dx.get_value(), lambda: response_pct(dx.get_value(), dr=1.0, surviving=0.02),
                      color=RED, ring=TEXT, radius=0.12)
        self.add(g_dot, r_dot)
        d_sweep = time_left_before(self, "Next can two")
        self.play(
            dx.animate(run_time=max(1.0, d_sweep - 0.3), rate_func=smooth).set_value(2.0),
            amp_t.animate(run_time=max(1.0, d_sweep - 0.3), rate_func=smooth).set_value(100.0),
        )
        self.play(FadeOut(g_dot), FadeOut(r_dot), run_time=0.25)

        self.at("Next can two")
        frosted = RoundedRectangle(corner_radius=0.14, width=3.9, height=1.25,
                                   stroke_color=TEAL, stroke_width=3.0, fill_color=BG, fill_opacity=0.92)
        frosted.move_to([4.1, -1.90, 0])
        frost_lbl = T("unknown amplifier", 28, TEXT).move_to(frosted)
        q_next = T("?", 68, GOLD, weight=BOLD).move_to([4.1, 0.55, 0])
        self.play(FadeOut(g2), FadeOut(g101), FadeOut(r_drop), FadeOut(schild_group),
                  FadeOut(amp_lbl), FadeOut(amp_bar), run_time=0.35)
        self.play(FadeIn(frosted), FadeIn(frost_lbl), FadeIn(q_next, shift=UP * 0.2), run_time=0.55)
        self.finish()


class S12End(EndCard):
    LINE = "How a blocker shifts or lowers curves across doses reveals its mechanism."
