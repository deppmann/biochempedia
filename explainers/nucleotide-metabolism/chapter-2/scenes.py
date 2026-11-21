"""Almost Right — STEMhop Nucleotide Metabolism Chapter 2.

COLOUR MAP (one colour per concept, whole film):
- GREEN   (#83C167): finished nucleotide (tokens, nucleotide pool, d-tagged deoxy tokens)
- YELLOW  (#F5D547): free purine base (capsule tokens)
- BLUE    (#58C4DD): enzymes and enzymatic gateways (HGPRT, ribonucleotide reductase, thymidylate synthase, DHFR)
- PURPLE  (#B589E6): PRPP and the de novo build door
- ORANGE  (#F2994A): ATP coins (s00 recap only)
- RED     (#FC6255): enzyme blocks, stall marks, broken X, DNA crack
- TEAL    (#3FB8C0): antimetabolite drugs / counterfeits (look-alike, methotrexate, 5-FU/FdUMP, 6-MP)
- MAGENTA (#E86BC5): folate carrier ring (THF / DHF) and carried one-carbon dot / two-ring-carbons arrow
- WHITE   (#E8EAF0): DNA double-stranded ladder, rungs, copying fork, and primary labels

THE WORLD (carried across all scenes):
- Left: round GREEN purine nucleotide pool with two rim doors — PURPLE build (PRPP) and BLUE recycle (HGPRT).
- Centre: BLUE ribonucleotide reductase gateway arch turning GREEN nucleotides into GREEN-outlined 'd' deoxy tokens.
- Right: tall WHITE schematic DNA ladder (~65% frame height) with an active copying fork sliding down it.
- Lower centre: MAGENTA folate loop connecting BLUE DHFR (left) and BLUE thymidylate synthase (right), feeding dTMP up to the DNA fork and two ring carbons up-left to the PURPLE build door.
- Bottom right: 'schematic' tag throughout.

WHAT CHANGES IN EACH SPOKEN SCENE (and what drives it):
- s00_link_and_question: YELLOW bases cycle out and back through HGPRT while ORANGE ATP coins fade at build; DNA ladder lights up as fork accelerates and GREEN tokens stream from pool; MAGENTA folate and TEAL look-alike rings float in; stream thins and fork slows as question appears.
- s02_gateway: BLUE gateway enlarges into ribonucleotide reductase arch; GREEN tokens pass through and become 'd'-tagged deoxy tokens; faint salvage side path joins stream; arch and DNA fork accelerate and decelerate together (coupled flow tracker).
- s03_thymidylate: World shifts up/dims while folate loop expands to lower half; 'dUMP' drops from arch to thymidylate synthase; MAGENTA ring delivers carbon dot onto token, which swaps to 'dTMP' and enters DNA fork as a rung; empty ring dims to 'DHF'.
- s04_folate_loop: 'DHF' travels to DHFR, brightens to 'THF' and picks up carbon dot; continuous folate loop turns (phase tracker); MAGENTA arrow grows to PURPLE build door carrying two carbon dots; both dTMP and purine-carbon outflows pulse together.
- s05_idea: Full world returns turning; DHFR enlarges with lock notch; MAGENTA ring slots through while TEAL look-alike jams notch and flickers RED stall before drifting out; fork accelerates with thicker token stream ('fastest demand').
- s06_predict: TEAL 'methotrexate' locks into DHFR notch under RED X; loop slows with DHF rings creeping; question marks appear on both dTMP and build outflows alongside top question card.
- s08_answer: Question card dissolves and both '?' turn to RED X; DHF rings stack behind jammed DHFR while THF side empties; purine-carbon arrow fades to dotted outline and dTMP stream dries up; DNA fork stalls at a missing 'T' rung ('no dTMP').
- s09_fluorouracil: Methotrexate block clears and loop restarts; TEAL '5-fluorouracil' capsule gains nucleotide outline to 'FdUMP' and locks onto thymidylate synthase under RED X; real dUMP tokens queue; fork stalls at missing 'T' rung while DHFR and purine arrow stay open.
- s10_mercaptopurine: 5-FU block clears; camera focuses on enlarged pool at left; TEAL '6-mercaptopurine' enters via turning HGPRT lock and becomes 'counterfeit' nucleotide; RED bar shuts PURPLE build door; counterfeit passes arch into DNA ladder as TEAL rung, cracking ladder ('leukemia cell').
- s11_close: Full world resumes unblocked; three TEAL ghosts appear sequentially at DHFR, thymidylate synthase, and HGPRT; white road lights from pool through arch to fork as fork accelerates; smaller 'normal dividing tissue' ladder appears at far right and dips slightly with ghost flicker.
"""
from bp_parts import *

# ---- Concept palette additions (core BG, BLUE, YELLOW, GREEN, RED, GREY, TEXT, TEAL, GOLD from bp_parts)
PURPLE = "#B589E6"
ORANGE = "#F2994A"
MAGENTA = "#E86BC5"

# ---- Canonical world coordinates (full view)
POOL_POS = np.array([-4.55, 1.38, 0.0])
POOL_R = 1.10
RECYCLE_POS = POOL_POS + POOL_R * np.array([np.cos(-3 * PI / 4), np.sin(-3 * PI / 4), 0.0])
BUILD_POS = POOL_POS + POOL_R * np.array([np.cos(-PI / 4), np.sin(-PI / 4), 0.0])
ARCH_POS = np.array([-0.25, 1.38, 0.0])
DNA_X = 4.65
DNA_TOP = 2.45
DNA_BOT = -2.35

# Folate loop: ellipse sits strictly between DHFR (left) and TS (right) with clear margin
LOOP_POS = np.array([-0.40, -1.45, 0.0])
LOOP_RX = 1.35
LOOP_RY = 0.64
DHFR_POS = np.array([-2.78, -1.45, 0.0])
TS_POS = np.array([2.25, -1.45, 0.0])


# ---- Reusable token / icon builders
def make_nuc_token(radius=0.16, color=GREEN, deoxy=False):
    """Finished nucleotide (solid circle) or deoxy nucleotide (outlined with 'd')."""
    if not deoxy:
        return Circle(radius=radius, color=color, fill_color=color, fill_opacity=0.90, stroke_width=2.8)
    ring = Circle(radius=radius, color=color, fill_color=BG, fill_opacity=0.96, stroke_width=3.5)
    d_txt = T("d", size=22, color=color, weight=BOLD).move_to(ring)
    d_txt.layout_ok = True
    return VGroup(ring, d_txt)


def make_base_token(color=YELLOW, w=0.38, h=0.20):
    """Free purine/pyrimidine base as a schematic capsule (never a chemical ring)."""
    return RoundedRectangle(corner_radius=h / 2, width=w, height=h, color=color,
                            fill_color=color, fill_opacity=0.90, stroke_width=2.8)


def make_atp_coin():
    """Small ORANGE ATP coin (recap only in s00)."""
    c = Circle(radius=0.38, color=ORANGE, fill_color=ORANGE, fill_opacity=0.28, stroke_width=3.2)
    t = T("ATP", size=22, color=ORANGE, weight=BOLD).move_to(c)
    return VGroup(c, t)


def make_folate_ring(radius=0.22, loaded=True, dim=False):
    """Plain geometric MAGENTA ring representing the folate carrier (+ optional carbon dot)."""
    op = 0.55 if dim else 1.0
    col = MAGENTA
    ring = Circle(radius=radius, color=col, stroke_width=6.0 if not dim else 4.2,
                  fill_color=col, fill_opacity=0.18 if not dim else 0.06).set_stroke(opacity=op)
    g = VGroup(ring)
    if loaded:
        dot = Dot(ring.get_top(), radius=0.085, color=col, fill_opacity=1.0)
        g.add(dot)
        g.dot = dot
    else:
        g.dot = None
    g.ring = ring
    return g


def make_drug_ring(radius=0.20, color=TEAL, opacity=1.0):
    """Plain TEAL ring of the same outline as folate."""
    return Circle(radius=radius, color=color, stroke_width=5.5, fill_color=color, fill_opacity=0.18 * opacity).set_stroke(opacity=opacity)


def make_red_x(center, size=0.42):
    """Crisp RED X block mark."""
    d = size / 2
    l1 = Line(center + np.array([-d, -d, 0]), center + np.array([d, d, 0]), color=RED, stroke_width=6.5)
    l2 = Line(center + np.array([-d, d, 0]), center + np.array([d, -d, 0]), color=RED, stroke_width=6.5)
    return VGroup(l1, l2)


def make_enzyme_chip(text, center, color=BLUE, size=26, notch_side=None, w=None, h=None):
    """Enzyme chip with optional schematic lock pocket cleanly OUTSIDE box border."""
    lab = T(text, size=size, color=color)
    pad_x, pad_y = 0.26, 0.18
    bw = max(w or 0, lab.width + 2 * pad_x)
    bh = max(h or 0, lab.height + 2 * pad_y)
    box = RoundedRectangle(corner_radius=0.14, width=bw, height=bh,
                           stroke_color=color, stroke_width=3.5, fill_color=color, fill_opacity=0.22).move_to(center)
    lab.move_to(box.get_center())
    g = VGroup(box, lab)
    g.box = box
    g.label = lab
    if notch_side == "left":
        # Outward pocket cleanly clear of box border (never straddles box!)
        pocket_center = box.get_left() + LEFT * 0.26
        notch = Arc(radius=0.21, start_angle=-PI / 2, angle=PI, arc_center=pocket_center,
                    color=color, stroke_width=4.0, fill_color=BG, fill_opacity=0.95)
        g.add(notch)
        g.notch = notch
        g.dock_pt = pocket_center
    elif notch_side == "right":
        pocket_center = box.get_right() + RIGHT * 0.26
        notch = Arc(radius=0.21, start_angle=PI / 2, angle=PI, arc_center=pocket_center,
                    color=color, stroke_width=4.0, fill_color=BG, fill_opacity=0.95)
        g.add(notch)
        g.notch = notch
        g.dock_pt = pocket_center
    else:
        g.notch = None
        g.dock_pt = center
    return g


def make_arch(center=ARCH_POS, scale=1.18, opacity=1.0):
    """BLUE ribonucleotide reductase gateway arch."""
    w = 1.18 * scale
    outer = Arc(radius=w / 2, start_angle=0, angle=PI, arc_center=center + DOWN * 0.15 * scale,
                color=BLUE, stroke_width=8 * scale).set_stroke(opacity=opacity)
    pillar_l = Line(center + np.array([-w / 2, -0.55 * scale, 0]),
                    center + np.array([-w / 2, -0.15 * scale, 0]), color=BLUE, stroke_width=8 * scale).set_stroke(opacity=opacity)
    pillar_r = Line(center + np.array([w / 2, -0.55 * scale, 0]),
                    center + np.array([w / 2, -0.15 * scale, 0]), color=BLUE, stroke_width=8 * scale).set_stroke(opacity=opacity)
    base = Line(center + np.array([-w / 2 - 0.15 * scale, -0.55 * scale, 0]),
                center + np.array([w / 2 + 0.15 * scale, -0.55 * scale, 0]), color=BLUE, stroke_width=4.5 * scale).set_stroke(opacity=opacity)
    glow = RoundedRectangle(corner_radius=0.22 * scale, width=w * 0.92, height=0.98 * scale,
                            stroke_width=0, fill_color=BLUE, fill_opacity=0.20 * opacity).move_to(center)
    return VGroup(glow, outer, pillar_l, pillar_r, base)


def make_pool(center=POOL_POS, radius=POOL_R, opacity=1.0, seed=7):
    """Round GREEN purine nucleotide pool with PURPLE build door and BLUE recycle door."""
    rng = np.random.default_rng(seed)
    circle = Circle(radius=radius, color=GREEN, stroke_width=5.5,
                    fill_color=GREEN, fill_opacity=0.20 * opacity).set_stroke(opacity=opacity).move_to(center)
    ang_rec = -3 * PI / 4
    ang_bld = -PI / 4
    rec_pt = center + radius * np.array([np.cos(ang_rec), np.sin(ang_rec), 0.0])
    bld_pt = center + radius * np.array([np.cos(ang_bld), np.sin(ang_bld), 0.0])
    rec_door = RoundedRectangle(corner_radius=0.06, width=0.40, height=0.20,
                                color=BLUE, fill_color=BLUE, fill_opacity=0.90 * opacity, stroke_width=2.5).move_to(rec_pt).rotate(ang_rec + PI / 2)
    bld_door = RoundedRectangle(corner_radius=0.06, width=0.40, height=0.20,
                                color=PURPLE, fill_color=PURPLE, fill_opacity=0.90 * opacity, stroke_width=2.5).move_to(bld_pt).rotate(ang_bld + PI / 2)
    inner_tokens = VGroup()
    for _ in range(10):
        r_t = rng.uniform(0.16, radius * 0.68)
        a_t = rng.uniform(0, TAU)
        tok = Circle(radius=0.13, color=GREEN, fill_color=GREEN, fill_opacity=0.82 * opacity, stroke_width=1.8)
        tok.move_to(center + r_t * np.array([np.cos(a_t), np.sin(a_t), 0.0]))
        tok._orbit_r = r_t
        tok._orbit_a = a_t
        tok._orbit_w = rng.uniform(0.45, 0.85) * (1 if rng.random() > 0.5 else -1)
        inner_tokens.add(tok)
    g = VGroup(circle, inner_tokens, rec_door, bld_door)
    g.circle = circle
    g.rec_door = rec_door
    g.bld_door = bld_door
    g.inner_tokens = inner_tokens
    g.center_pt = center
    return g


def animate_pool_tokens(pool, speed_mult=1.0):
    """Attach continuous orbital motion to nucleotides inside the pool."""
    c = pool.center_pt

    def upd(mob, dt):
        for tok in mob:
            tok._orbit_a += tok._orbit_w * speed_mult * dt
            tok.move_to(c + tok._orbit_r * np.array([np.cos(tok._orbit_a), np.sin(tok._orbit_a), 0.0]))

    pool.inner_tokens.add_updater(upd)
    return pool


def build_dna_ladder(x=DNA_X, y_top=DNA_TOP, y_bot=DNA_BOT, width=0.94, fork_tracker=None,
                     opacity=1.0, missing_t_y=None, teal_rung_y=None):
    """Computed schematic DNA ladder with active copying fork."""
    n_rungs = 13
    ys = np.linspace(y_top - 0.18, y_bot + 0.18, n_rungs)

    def mk():
        fy = fork_tracker.get_value() if fork_tracker is not None else (y_top + y_bot) / 2
        g = VGroup()
        if y_top - fy > 0.15:
            copied_bg = Rectangle(width=width, height=y_top - fy, stroke_width=0,
                                  fill_color=TEXT, fill_opacity=0.07 * opacity).move_to([x, (y_top + fy) / 2, 0])
            g.add(copied_bg)
        l_pts, r_pts = [], []
        for y in np.linspace(y_top, y_bot, 28):
            spread = 0.0 if y >= fy else 0.20 * min(1.0, (fy - y) / 0.75)
            l_pts.append([x - width / 2 - spread, y, 0.0])
            r_pts.append([x + width / 2 + spread, y, 0.0])
        rail_l = VMobject(color=TEXT, stroke_width=6.0, stroke_opacity=opacity).set_points_as_corners(l_pts)
        rail_r = VMobject(color=TEXT, stroke_width=6.0, stroke_opacity=opacity).set_points_as_corners(r_pts)
        g.add(rail_l, rail_r)
        for y in ys:
            if y >= fy:
                if missing_t_y is not None and abs(y - missing_t_y) < 0.20:
                    stub_l = Line([x - width / 2, y, 0], [x - width / 2 + 0.20, y, 0], color=RED, stroke_width=5.0, stroke_opacity=opacity)
                    stub_r = Line([x + width / 2 - 0.20, y, 0], [x + width / 2, y, 0], color=RED, stroke_width=5.0, stroke_opacity=opacity)
                    g.add(stub_l, stub_r)
                elif teal_rung_y is not None and abs(y - teal_rung_y) < 0.20:
                    rung = Line([x - width / 2, y, 0], [x + width / 2, y, 0], color=TEAL, stroke_width=7.0, stroke_opacity=opacity)
                    g.add(rung)
                else:
                    rung = Line([x - width / 2, y, 0], [x + width / 2, y, 0], color=TEXT, stroke_width=5.0, stroke_opacity=opacity)
                    g.add(rung)
            else:
                spread = 0.20 * min(1.0, (fy - y) / 0.75)
                stub_l = Line([x - width / 2 - spread, y, 0], [x - width / 2 - spread + 0.20, y, 0],
                              color=TEXT, stroke_width=4.0, stroke_opacity=0.65 * opacity)
                stub_r = Line([x + width / 2 + spread - 0.20, y, 0], [x + width / 2 + spread, y, 0],
                              color=TEXT, stroke_width=4.0, stroke_opacity=0.65 * opacity)
                g.add(stub_l, stub_r)
        fork_bar = Polygon(
            [x - width / 2 - 0.16, fy + 0.08, 0],
            [x + width / 2 + 0.16, fy + 0.08, 0],
            [x, fy - 0.22, 0],
            color=GOLD, stroke_width=3.5, fill_color=GOLD, fill_opacity=0.35 * opacity
        ).set_stroke(opacity=opacity)
        g.add(fork_bar)
        return g

    return always_redraw(mk) if fork_tracker is not None else mk()


def loop_point(center, rx, ry, theta):
    """Point on the folate ellipse parameterized by angle theta."""
    return center + np.array([rx * np.cos(theta), ry * np.sin(theta), 0.0])


def make_folate_track(center=LOOP_POS, rx=LOOP_RX, ry=LOOP_RY, opacity=1.0):
    """MAGENTA folate loop ellipse + directional arrowheads at top and bottom."""
    ell = Ellipse(width=2 * rx, height=2 * ry, color=MAGENTA, stroke_width=5.5).set_stroke(opacity=0.80 * opacity).move_to(center)
    top_arr = Triangle(color=MAGENTA, fill_color=MAGENTA, fill_opacity=0.90 * opacity, stroke_width=1).scale(0.13).rotate(-PI / 2).move_to(center + UP * ry)
    bot_arr = Triangle(color=MAGENTA, fill_color=MAGENTA, fill_opacity=0.90 * opacity, stroke_width=1).scale(0.13).rotate(PI / 2).move_to(center + DOWN * ry)
    return VGroup(ell, top_arr, bot_arr)


def make_token_stream(pts_fn, n_tokens, phase_tracker, deoxy=False, color=GREEN, radius=0.14):
    """Computed token stream moving smoothly along pts_fn(u) for u in [0, 1]."""
    def mk():
        g = VGroup()
        p0 = phase_tracker.get_value()
        for k in range(n_tokens):
            u = (p0 + k / n_tokens) % 1.0
            pos = pts_fn(u)
            if deoxy and u > 0.52:
                tok = Circle(radius=radius, color=color, fill_color=BG, fill_opacity=0.96, stroke_width=3.4).move_to(pos)
                d_t = T("d", size=22, color=color, weight=BOLD).move_to(tok)
                d_t.layout_ok = True
                g.add(tok, d_t)
            else:
                g.add(Circle(radius=radius, color=color, fill_color=color, fill_opacity=0.90, stroke_width=2.2).move_to(pos))
        return g

    return always_redraw(mk)


def stream_path_pt(u, pool_pos=POOL_POS, pool_r=POOL_R, arch_pos=ARCH_POS, dna_x=DNA_X, fork_y_fn=lambda: 0.3):
    """Piecewise smooth path: pool -> arch -> bend right near DNA -> fork (clears TS!)."""
    p_start = pool_pos + RIGHT * pool_r
    p_arch = arch_pos + DOWN * 0.05
    p_bend = np.array([dna_x - 0.95, arch_pos[1] - 0.05, 0.0])
    p_end = np.array([dna_x - 0.62, fork_y_fn(), 0.0])
    if u <= 0.45:
        a = u / 0.45
        return (1 - a) * p_start + a * p_arch
    if u <= 0.80:
        a = (u - 0.45) / 0.35
        return (1 - a) * p_arch + a * p_bend
    a = (u - 0.80) / 0.20
    return (1 - a) * p_bend + a * p_end


# ==============================================================================
# SCENES
# ==============================================================================

class S00LinkAndQuestion(SpokenScene):
    def construct(self):
        pool = make_pool(opacity=1.0)
        animate_pool_tokens(pool, speed_mult=1.0)
        pool_lbl = T("pool", size=28, color=GREEN).move_to(POOL_POS + UP * (POOL_R + 0.32))
        hgprt = make_enzyme_chip("HGPRT", RECYCLE_POS + np.array([-0.22, -0.95, 0]), color=BLUE, size=24)
        prpp = make_enzyme_chip("PRPP", BUILD_POS + np.array([0.38, -0.95, 0]), color=PURPLE, size=24)
        rec_lbl = T("recycle", size=24, color=BLUE).next_to(hgprt, DOWN, buff=0.18)
        bld_lbl = T("build", size=24, color=PURPLE).next_to(prpp, DOWN, buff=0.18)

        arch_dim = make_arch(ARCH_POS, opacity=0.35)
        fork_y = ValueTracker(1.2)
        dna_dim = build_dna_ladder(fork_tracker=fork_y, opacity=0.35)
        dna_lbl = T("DNA", size=28, color=TEXT).set_opacity(0.62).move_to([DNA_X, DNA_TOP + 0.35, 0])

        stag = scope_tag("schematic")
        self.add(pool, pool_lbl, hgprt, prpp, rec_lbl, bld_lbl, arch_dim, dna_dim, dna_lbl, stag, fork_y)

        # Beat 1 (0.0s): YELLOW bases loop strictly OUTSIDE HGPRT into BLUE recycle door
        base_phase = ValueTracker(0.0)
        base_phase.add_updater(lambda m, dt: m.increment_value(0.32 * dt))
        self.add(base_phase)

        def make_bases():
            g = VGroup()
            p = base_phase.get_value()
            lx = hgprt.get_left()[0] - 0.34
            ty = hgprt.get_top()[1] + 0.26
            pts = [
                POOL_POS + LEFT * POOL_R,
                np.array([lx, 0.70, 0]),
                np.array([lx, ty, 0]),
                np.array([hgprt.get_center()[0] + 0.15, ty, 0]),
                RECYCLE_POS,
            ]
            for k in range(3):
                u = (p + k / 3.0) % 1.0
                idx = min(3, int(u * 4))
                frac = u * 4 - idx
                pos = (1 - frac) * pts[idx] + frac * pts[idx + 1]
                g.add(make_base_token(YELLOW).move_to(pos))
            return g

        bases = always_redraw(make_bases)
        atp_coins = VGroup(
            make_atp_coin().move_to(BUILD_POS + np.array([0.88, 0.68, 0])),
            make_atp_coin().move_to(BUILD_POS + np.array([1.95, 0.30, 0])),
            make_atp_coin().move_to(BUILD_POS + np.array([1.20, -0.18, 0])),
        )
        self.add(bases, atp_coins)

        self.at("building them is costly")
        self.play(FadeOut(atp_coins, run_time=1.0))

        # Beat 2 (6.02s): Dividing cell -> light up DNA ladder & arch; fork speeds up; GREEN tokens stream
        self.at("A dividing cell")
        arch_bright = make_arch(ARCH_POS, opacity=1.0)
        dna_bright = build_dna_ladder(fork_tracker=fork_y, opacity=1.0)
        stream_phase = ValueTracker(0.0)
        stream_speed = ValueTracker(0.35)
        stream_count = [7]
        stream_phase.add_updater(lambda m, dt: m.increment_value(stream_speed.get_value() * dt))
        fork_speed = ValueTracker(-0.28)
        fork_y.add_updater(lambda m, dt: m.set_value(1.65 if m.get_value() < -1.75 else m.get_value() + fork_speed.get_value() * dt))
        self.add(stream_phase, stream_speed, fork_speed)

        def mk_stream():
            g = VGroup()
            p0 = stream_phase.get_value()
            n = stream_count[0]
            for k in range(n):
                u = (p0 + k / n) % 1.0
                pos = stream_path_pt(u, fork_y_fn=lambda: fork_y.get_value())
                g.add(Circle(radius=0.14, color=GREEN, fill_color=GREEN, fill_opacity=0.92, stroke_width=2.2).move_to(pos))
            return g

        stream = always_redraw(mk_stream)
        self.play(
            ReplacementTransform(arch_dim, arch_bright),
            FadeOut(dna_dim),
            FadeIn(dna_bright),
            dna_lbl.animate.set_opacity(1.0),
            FadeIn(stream),
            run_time=1.0
        )
        self.play(fork_speed.animate.set_value(-0.52), stream_speed.animate.set_value(0.58), run_time=1.2)

        # Beat 3 (12.56s): Folate & TEAL look-alike rings float in
        self.at("shaped almost like")
        folate = make_folate_ring(radius=0.34, loaded=True).move_to([-0.85, -1.45, 0])
        fol_lbl = T("folate", size=26, color=MAGENTA).next_to(folate, DOWN, buff=0.18)
        lookalike = make_drug_ring(radius=0.34, color=TEAL).move_to([0.90, -1.45, 0])
        look_lbl = T("look-alike", size=26, color=TEAL).next_to(lookalike, DOWN, buff=0.18)
        self.play(FadeIn(folate, shift=UP * 0.25), FadeIn(fol_lbl, shift=UP * 0.25), run_time=0.8)
        self.play(FadeIn(lookalike, shift=UP * 0.25), FadeIn(look_lbl, shift=UP * 0.25), run_time=0.8)

        # Beat 4 (15.94s): Question -> stream thins, fork slows, large white question across top
        self.at("How can a vitamin")
        stream_count[0] = 3
        q_txt = T("A fake vitamin stops copying?", size=38, color=TEXT, weight=BOLD).move_to([0.0, 3.22, 0])
        self.play(
            fork_speed.animate.set_value(-0.14),
            stream_speed.animate.set_value(0.18),
            FadeIn(q_txt, shift=DOWN * 0.15),
            run_time=1.0
        )
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        pool = make_pool(opacity=1.0)
        animate_pool_tokens(pool, speed_mult=1.0)
        pool_lbl = T("pool", size=28, color=GREEN).move_to(POOL_POS + UP * (POOL_R + 0.32))
        hgprt = make_enzyme_chip("HGPRT", RECYCLE_POS + np.array([-0.22, -0.95, 0]), color=BLUE, size=24)
        prpp = make_enzyme_chip("PRPP", BUILD_POS + np.array([0.38, -0.95, 0]), color=PURPLE, size=24)
        rec_lbl = T("recycle", size=24, color=BLUE).next_to(hgprt, DOWN, buff=0.18)
        bld_lbl = T("build", size=24, color=PURPLE).next_to(prpp, DOWN, buff=0.18)
        arch = make_arch(ARCH_POS, opacity=1.0)
        fork_y = ValueTracker(0.5)
        fork_y.add_updater(lambda m, dt: m.set_value(1.65 if m.get_value() < -1.75 else m.get_value() - 0.32 * dt))
        dna = build_dna_ladder(fork_tracker=fork_y, opacity=1.0)
        dna_lbl = T("DNA", size=28, color=TEXT).move_to([DNA_X, DNA_TOP + 0.35, 0])
        stream_phase = ValueTracker(0.2)
        stream_phase.add_updater(lambda m, dt: m.increment_value(0.38 * dt))
        stream = make_token_stream(lambda u: stream_path_pt(u, fork_y_fn=lambda: fork_y.get_value()),
                                   6, stream_phase, deoxy=False)

        folate = make_folate_ring(radius=0.34, loaded=True).move_to([-0.85, -1.45, 0])
        fol_lbl = T("folate", size=26, color=MAGENTA).next_to(folate, DOWN, buff=0.18)
        lookalike = make_drug_ring(radius=0.34, color=TEAL).move_to([0.90, -1.45, 0])
        look_lbl = T("look-alike", size=26, color=TEAL).next_to(lookalike, DOWN, buff=0.18)
        q_txt = T("A fake vitamin stops copying?", size=38, color=TEXT, weight=BOLD).move_to([0.0, 3.22, 0])

        self.add(pool, pool_lbl, hgprt, prpp, rec_lbl, bld_lbl, arch, dna, dna_lbl, stream,
                 folate, fol_lbl, lookalike, look_lbl, q_txt, scope_tag("schematic"),
                 fork_y, stream_phase)

        title = T("Almost Right", size=50, font=TITLE_FONT, color=TEXT).move_to([0.0, 3.22, 0])
        rule = Line(LEFT * 1.3, RIGHT * 1.3, color=GOLD, stroke_width=4).next_to(title, DOWN, buff=0.12)
        self.play(
            FadeOut(q_txt, run_time=0.25),
            VGroup(lookalike, look_lbl).animate.shift(LEFT * 2.5 + DOWN * 2.4).set_opacity(0.0),
            FadeOut(VGroup(folate, fol_lbl), run_time=0.45),
            run_time=0.45
        )
        self.play(FadeIn(title, run_time=0.35), GrowFromCenter(rule, run_time=0.35))
        self.wait(0.85)
        self.play(FadeOut(title), FadeOut(rule), run_time=0.35)
        self.finish()


class S02Gateway(SpokenScene):
    def construct(self):
        pool = make_pool(opacity=1.0)
        animate_pool_tokens(pool, speed_mult=1.0)
        pool_lbl = T("pool", size=28, color=GREEN).move_to(POOL_POS + UP * (POOL_R + 0.32))
        hgprt = make_enzyme_chip("HGPRT", RECYCLE_POS + np.array([-0.22, -0.95, 0]), color=BLUE, size=24)
        prpp = make_enzyme_chip("PRPP", BUILD_POS + np.array([0.38, -0.95, 0]), color=PURPLE, size=24)
        rec_lbl = T("recycle", size=24, color=BLUE).next_to(hgprt, DOWN, buff=0.18)
        bld_lbl = T("build", size=24, color=PURPLE).next_to(prpp, DOWN, buff=0.18)

        arch = make_arch(ARCH_POS, scale=1.0)
        fork_y = ValueTracker(1.2)
        fork_speed = ValueTracker(-0.30)
        fork_y.add_updater(lambda m, dt: m.set_value(1.65 if m.get_value() < -1.75 else m.get_value() + fork_speed.get_value() * dt))
        dna = build_dna_ladder(fork_tracker=fork_y, opacity=1.0)
        dna_lbl = T("DNA", size=28, color=TEXT).move_to([DNA_X, DNA_TOP + 0.35, 0])

        stream_phase = ValueTracker(0.0)
        stream_speed = ValueTracker(0.34)
        stream_phase.add_updater(lambda m, dt: m.increment_value(stream_speed.get_value() * dt))
        stream_deoxy = [False]
        stream_count = [6]

        def mk_stream():
            g = VGroup()
            p0 = stream_phase.get_value()
            n = stream_count[0]
            for k in range(n):
                u = (p0 + k / n) % 1.0
                pos = stream_path_pt(u, fork_y_fn=lambda: fork_y.get_value())
                if stream_deoxy[0] and u > 0.48:
                    tok = Circle(radius=0.15, color=GREEN, fill_color=BG, fill_opacity=0.96, stroke_width=3.5).move_to(pos)
                    d_t = T("d", size=22, color=GREEN, weight=BOLD).move_to(tok)
                    d_t.layout_ok = True
                    g.add(tok, d_t)
                else:
                    g.add(Circle(radius=0.14, color=GREEN, fill_color=GREEN, fill_opacity=0.90, stroke_width=2.2).move_to(pos))
            return g

        stream = always_redraw(mk_stream)
        self.add(pool, pool_lbl, hgprt, prpp, rec_lbl, bld_lbl, arch, dna, dna_lbl, stream,
                 scope_tag("schematic"), fork_y, fork_speed, stream_phase, stream_speed)

        # Beat 1 (0.0s): Gateway grows to large arch; deoxy tokens emerge
        self.at("But DNA needs")
        big_arch = make_arch(ARCH_POS, scale=1.45)
        arch_lbl = T("ribonucleotide\nreductase", size=26, color=BLUE).move_to(ARCH_POS + UP * 1.55)
        stream_deoxy[0] = True
        deoxy_lbl = T("deoxy", size=26, color=GREEN).move_to([1.85, 2.05, 0])
        self.play(ReplacementTransform(arch, big_arch), FadeIn(arch_lbl), run_time=1.0)
        self.play(FadeIn(deoxy_lbl), run_time=0.6)

        # Beat 2 (5.5s): Most new ones -> faint unlabelled side path joins deoxy stream
        self.at("most new ones")
        side_path = DashedLine([1.30, 0.15, 0], [1.95, 1.02, 0], color=GREY, stroke_width=3.5, dash_length=0.14)
        side_tip = Triangle(color=GREY, fill_color=GREY, fill_opacity=0.85, stroke_width=1).scale(0.09).rotate(-0.6).move_to([1.95, 1.02, 0])
        self.play(FadeIn(VGroup(side_path, side_tip)), run_time=0.8)

        # Beat 3 (13.0s): Tied tightly to cell division -> arch & fork pulse/accelerate together then slow
        self.at("Its activity")
        stream_count[0] = 9
        self.play(
            big_arch.animate.scale(1.12),
            fork_speed.animate.set_value(-0.62),
            stream_speed.animate.set_value(0.65),
            run_time=1.0
        )
        stream_count[0] = 3
        self.play(
            big_arch.animate.scale(1 / 1.12),
            fork_speed.animate.set_value(-0.16),
            stream_speed.animate.set_value(0.20),
            run_time=1.0
        )
        stream_count[0] = 6
        self.play(fork_speed.animate.set_value(-0.32), stream_speed.animate.set_value(0.35), run_time=0.5)
        self.finish()


class S03Thymidylate(SpokenScene):
    def construct(self):
        up_pool_pos = np.array([-4.45, 2.38, 0])
        up_pool = make_pool(center=up_pool_pos, radius=0.78, opacity=0.38)
        animate_pool_tokens(up_pool, speed_mult=0.7)
        up_pool_lbl = T("pool", size=24, color=GREEN).set_opacity(0.68).next_to(up_pool.circle, UP, buff=0.12)
        up_arch_pos = np.array([-0.45, 2.38, 0])
        up_arch = make_arch(center=up_arch_pos, scale=1.0, opacity=0.45)
        up_arch_lbl = T("ribonucleotide reductase", size=24, color=BLUE).set_opacity(0.68).move_to([-0.45, 3.25, 0])

        fork_y = ValueTracker(1.75)
        fork_y.add_updater(lambda m, dt: m.set_value(1.90 if m.get_value() < 0.85 else m.get_value() - 0.14 * dt))
        up_dna_x = 4.65
        up_dna = build_dna_ladder(x=up_dna_x, y_top=3.05, y_bot=0.50, width=0.78, fork_tracker=fork_y, opacity=0.48)
        up_dna_lbl = T("DNA", size=24, color=TEXT).set_opacity(0.68).move_to([up_dna_x, 3.32, 0])

        lo_center = np.array([-0.25, -1.18, 0.0])
        lo_rx, lo_ry = 2.00, 1.05
        track = make_folate_track(center=lo_center, rx=lo_rx, ry=lo_ry, opacity=1.0)
        ts_pos = lo_center + RIGHT * (lo_rx + 1.32)
        ts_chip = make_enzyme_chip("thymidylate\nsynthase", ts_pos, color=BLUE, size=26)

        up_phase = ValueTracker(0.0)
        up_phase.add_updater(lambda m, dt: m.increment_value(0.28 * dt))
        up_stream = make_token_stream(
            lambda u: stream_path_pt(u, up_pool_pos, 0.78, up_arch_pos, up_dna_x, lambda: 2.30),
            4, up_phase, deoxy=True, radius=0.12
        )
        up_stream.set_opacity(0.45)

        self.add(up_pool, up_pool_lbl, up_arch, up_arch_lbl, up_dna, up_dna_lbl, up_stream,
                 track, ts_chip, scope_tag("schematic"), fork_y, up_phase)

        # Beat 1 (3.18s): dUMP enters cleanly RIGHT of arch, drops above TS; MAGENTA ring arrives above TS
        self.at("Thymidylate synthase")
        dump_tok = make_nuc_token(radius=0.18, color=GREEN, deoxy=True).move_to([1.95, 1.65, 0])
        dump_lbl = T("dUMP", size=26, color=GREEN).next_to(dump_tok, LEFT, buff=0.26)
        dump_grp = VGroup(dump_tok, dump_lbl)

        fol = make_folate_ring(radius=0.28, loaded=True).move_to(loop_point(lo_center, lo_rx, lo_ry, 2.3))
        self.play(FadeIn(dump_grp), FadeIn(fol), run_time=0.3)

        ts_in_tok = ts_pos + np.array([-0.65, 1.05, 0])
        fol_in = ts_pos + np.array([0.45, 1.05, 0])
        self.play(
            dump_tok.animate.move_to(ts_in_tok),
            dump_lbl.animate.next_to(ts_in_tok, LEFT, buff=0.26),
            MoveAlongPath(fol, ArcBetweenPoints(fol.get_center(), fol_in, angle=-0.25)),
            run_time=0.6
        )

        # Beat 2 (4.06s): adds a carbon -> dot hops from ring onto token
        self.at("adds a carbon")
        c_dot = fol.dot
        fol.remove(c_dot)
        self.add(c_dot)
        target_dot_pt = dump_tok.get_top() + UP * 0.05
        self.play(c_dot.animate.move_to(target_dot_pt), run_time=0.8)

        # Beat 3 (8.66s): makes thymidylate dTMP -> relabels to dTMP and rises cleanly left of DNA fork, becomes rung
        self.at("That makes thymidylate")
        dtmp_lbl = T("dTMP", size=26, color=MAGENTA).move_to(dump_lbl)
        self.play(swap(dump_lbl, dtmp_lbl, run_time=0.55))
        dtmp_grp = VGroup(dump_tok, c_dot, dtmp_lbl)
        fork_target = np.array([up_dna_x - 1.25, fork_y.get_value(), 0.0])
        self.play(dtmp_grp.animate.move_to(fork_target), run_time=1.3)
        new_rung = Line([up_dna_x - 0.39, fork_y.get_value(), 0], [up_dna_x + 0.39, fork_y.get_value(), 0],
                        color=MAGENTA, stroke_width=6.5)
        self.play(FadeOut(dtmp_grp, run_time=0.25), FadeIn(new_rung, run_time=0.25))
        self.play(FadeOut(new_rung, run_time=0.4))

        # Beat 4 (11.66s): leaves the folate as DHF -> ring dims slightly and moves to bottom leg, labelled DHF
        self.at("leaves the folate")
        dhf_pt = loop_point(lo_center, lo_rx, lo_ry, -0.75)
        self.play(
            MoveAlongPath(fol, ArcBetweenPoints(fol.get_center(), dhf_pt, angle=2.4)),
            run_time=1.0
        )
        dhf_lbl = T("DHF", size=26, color=MAGENTA).next_to(fol, DOWN, buff=0.22)
        self.play(
            fol.ring.animate.set_stroke(opacity=0.55, width=4.2).set_fill(opacity=0.06),
            FadeIn(dhf_lbl),
            run_time=0.4
        )
        self.finish()


class S04FolateLoop(SpokenScene):
    def construct(self):
        up_pool_pos = np.array([-4.45, 2.38, 0])
        up_pool = make_pool(center=up_pool_pos, radius=0.78, opacity=0.58)
        animate_pool_tokens(up_pool, speed_mult=0.8)
        up_pool_lbl = T("pool", size=24, color=GREEN).set_opacity(0.85).next_to(up_pool.circle, UP, buff=0.12)
        bld_lbl = T("build", size=24, color=PURPLE).move_to(up_pool.bld_door.get_center() + np.array([0.82, -0.05, 0]))
        up_arch = make_arch(center=np.array([-0.45, 2.38, 0]), scale=1.0, opacity=0.45)

        fork_y = ValueTracker(2.2)
        fork_y.add_updater(lambda m, dt: m.set_value(2.8 if m.get_value() < 0.85 else m.get_value() - 0.18 * dt))
        up_dna_x = 4.65
        up_dna = build_dna_ladder(x=up_dna_x, y_top=3.05, y_bot=0.50, width=0.78, fork_tracker=fork_y, opacity=0.58)
        up_dna_lbl = T("DNA", size=24, color=TEXT).set_opacity(0.85).move_to([up_dna_x, 3.32, 0])

        lo_center = np.array([-0.25, -1.18, 0.0])
        lo_rx, lo_ry = 2.00, 1.05
        track = make_folate_track(center=lo_center, rx=lo_rx, ry=lo_ry, opacity=1.0)
        ts_pos = lo_center + RIGHT * (lo_rx + 1.38)
        dhfr_pos = lo_center + LEFT * (lo_rx + 1.05)
        ts_chip = make_enzyme_chip("thymidylate\nsynthase", ts_pos, color=BLUE, size=26)
        dhfr_chip = make_enzyme_chip("DHFR", dhfr_pos, color=BLUE, size=26)

        dhf_pos_0 = loop_point(lo_center, lo_rx, lo_ry, -0.75)
        fol = make_folate_ring(radius=0.28, loaded=False, dim=True).move_to(dhf_pos_0)
        ring_lbl = T("DHF", size=26, color=MAGENTA).next_to(fol, DOWN, buff=0.22)

        self.add(up_pool, up_pool_lbl, bld_lbl, up_arch, up_dna, up_dna_lbl,
                 track, ts_chip, dhfr_chip, fol, ring_lbl, scope_tag("schematic"), fork_y)

        # Beat 1 (0.0s): DHF travels round bottom of loop to DHFR
        self.at("Dihydrofolate reductase")
        theta = ValueTracker(-0.75)
        fol.add_updater(lambda m: m.move_to(loop_point(lo_center, lo_rx, lo_ry, theta.get_value())))
        ring_lbl.add_updater(lambda m: m.next_to(fol, DOWN, buff=0.22))
        self.add(theta)
        self.play(theta.animate.set_value(-PI + 0.25), run_time=2.4, rate_func=linear)

        # Beat 2 (3.38s): turns it back into THF -> brightens, relabels to THF, picks up fresh dot
        self.at("turns it back")
        fol.clear_updaters()
        ring_lbl.clear_updaters()
        thf_pos = loop_point(lo_center, lo_rx, lo_ry, PI - 0.35)
        thf_ring = make_folate_ring(radius=0.28, loaded=True, dim=False).move_to(thf_pos)
        thf_lbl = T("THF", size=26, color=MAGENTA).next_to(thf_ring, UP, buff=0.22)
        self.play(
            ReplacementTransform(fol, thf_ring),
            swap(ring_lbl, thf_lbl, run_time=0.55),
            run_time=0.85
        )

        # Beat 3 (7.12s): Continuous loop turns
        self.at("carry another carbon")
        self.remove(thf_ring, thf_lbl)
        loop_phase = ValueTracker(0.0)
        loop_phase.add_updater(lambda m, dt: m.increment_value(0.55 * dt))
        self.add(loop_phase)

        def mk_loop_rings():
            g = VGroup()
            p0 = loop_phase.get_value()
            for k in range(3):
                ang = (PI - 0.35 - (p0 + k / 3.0) * TAU) % TAU
                pos = loop_point(lo_center, lo_rx, lo_ry, ang)
                is_top = 0.15 < ang < PI - 0.15
                g.add(make_folate_ring(radius=0.24, loaded=is_top, dim=not is_top).move_to(pos))
            return g

        loop_rings = always_redraw(mk_loop_rings)
        thf_tag = T("THF", size=24, color=MAGENTA).move_to(lo_center + UP * (lo_ry + 0.45))
        dhf_tag = T("DHF", size=24, color=MAGENTA).move_to(lo_center + DOWN * (lo_ry + 0.45))

        dtmp_phase = ValueTracker(0.0)
        dtmp_phase.add_updater(lambda m, dt: m.increment_value(0.38 * dt))
        self.add(dtmp_phase)

        def mk_dtmp_out():
            g = VGroup()
            p0 = dtmp_phase.get_value()
            start = ts_pos + UP * 0.60
            end = np.array([up_dna_x - 0.60, fork_y.get_value(), 0.0])
            for k in range(2):
                u = (p0 + k * 0.5) % 1.0
                pos = (1 - u) * start + u * end
                tok = Circle(radius=0.13, color=GREEN, fill_color=BG, fill_opacity=0.96, stroke_width=3.0).move_to(pos)
                dot = Dot(tok.get_top() + UP * 0.04, radius=0.055, color=MAGENTA)
                g.add(tok, dot)
            return g

        dtmp_out = always_redraw(mk_dtmp_out)
        self.add(loop_rings, dtmp_out)
        self.play(FadeIn(thf_tag), FadeIn(dhf_tag), run_time=0.5)

        # Beat 4 (10.96s): two carbons of the purine ring -> MAGENTA arrow grows to PURPLE build door carrying 2 dots
        self.at("two carbons of the purine")
        arrow_start = lo_center + np.array([-1.35, lo_ry * 0.82, 0])
        arrow_end = up_pool.bld_door.get_center() + DOWN * 0.22
        pur_arrow = CurvedArrow(arrow_start, arrow_end, angle=-0.22, color=MAGENTA, stroke_width=5, tip_length=0.22)
        pur_dots_phase = ValueTracker(0.0)
        pur_dots_phase.add_updater(lambda m, dt: m.increment_value(0.45 * dt))
        self.add(pur_dots_phase)

        def mk_pur_dots():
            g = VGroup()
            p0 = pur_dots_phase.get_value()
            for k in range(2):
                u = (p0 + k * 0.5) % 1.0
                g.add(Dot(pur_arrow.point_from_proportion(u), radius=0.085, color=MAGENTA))
            return g

        pur_dots = always_redraw(mk_pur_dots)
        two_c_lbl = T("two ring\ncarbons", size=24, color=MAGENTA).move_to([-3.55, 0.10, 0])
        self.play(Create(pur_arrow), FadeIn(two_c_lbl), run_time=1.0)
        self.add(pur_dots)

        # Beat 5 (14.98s): feeds both -> pulse dTMP path and purine-carbon arrow together
        self.at("feeds both")
        dtmp_line = Line(ts_pos + UP * 0.60, [up_dna_x - 0.60, fork_y.get_value(), 0], color=MAGENTA, stroke_width=5)
        self.play(
            ShowPassingFlash(pur_arrow.copy().set_stroke(color=GOLD, width=8), time_width=0.6),
            ShowPassingFlash(dtmp_line.set_stroke(color=GOLD, width=8), time_width=0.6),
            run_time=1.3
        )
        self.finish()


# ---- Helper to build the full world for s05..s09 & s11
def build_full_world(dhfr_notch=True, loop_speed=0.45, fork_speed_val=-0.28, dtmp_active=True,
                     pur_active=True, pool_speed=0.9, missing_t_y=None, teal_rung_y=None,
                     dna_x=DNA_X, ts_pos=TS_POS, loop_pos=LOOP_POS, loop_rx=LOOP_RX, dhfr_pos=DHFR_POS):
    pool = make_pool(opacity=1.0)
    animate_pool_tokens(pool, speed_mult=pool_speed)
    pool_lbl = T("pool", size=24, color=GREEN).move_to(POOL_POS + UP * (POOL_R + 0.28))
    hgprt = make_enzyme_chip("HGPRT", RECYCLE_POS + np.array([-0.22, -0.95, 0]), color=BLUE, size=24)
    prpp = make_enzyme_chip("PRPP", BUILD_POS + np.array([0.38, -0.95, 0]), color=PURPLE, size=24)
    arch = make_arch(ARCH_POS, scale=1.18, opacity=1.0)
    arch_lbl = T("ribonucleotide reductase", size=24, color=BLUE).move_to(ARCH_POS + UP * 1.25)

    fork_y = ValueTracker(0.95)
    fork_spd = ValueTracker(fork_speed_val)
    fork_y.add_updater(lambda m, dt: m.set_value(1.75 if m.get_value() < -0.55 else m.get_value() + fork_spd.get_value() * dt))
    dna = build_dna_ladder(x=dna_x, fork_tracker=fork_y, opacity=1.0, missing_t_y=missing_t_y, teal_rung_y=teal_rung_y)
    dna_lbl = T("DNA", size=26, color=TEXT).move_to([dna_x, DNA_TOP + 0.35, 0])

    # Folate loop cleanly between DHFR and TS
    track = make_folate_track(center=loop_pos, rx=loop_rx, ry=LOOP_RY, opacity=1.0)
    dhfr = make_enzyme_chip("DHFR", dhfr_pos, color=BLUE, size=24, notch_side="left" if dhfr_notch else None)
    ts = make_enzyme_chip("thymidylate\nsynthase", ts_pos, color=BLUE, size=24)

    loop_phase = ValueTracker(0.0)
    loop_spd = ValueTracker(loop_speed)
    loop_phase.add_updater(lambda m, dt: m.increment_value(loop_spd.get_value() * dt))

    def mk_rings():
        g = VGroup()
        p0 = loop_phase.get_value()
        for k in range(3):
            ang = (PI - 0.35 - (p0 + k / 3.0) * TAU) % TAU
            pos = loop_point(loop_pos, loop_rx, LOOP_RY, ang)
            is_top = 0.15 < ang < PI - 0.15
            g.add(make_folate_ring(radius=0.19, loaded=is_top, dim=not is_top).move_to(pos))
        return g

    loop_rings = always_redraw(mk_rings)

    # Stream pool -> arch -> bend right -> fork (never crosses TS!)
    stream_phase = ValueTracker(0.0)
    stream_spd = ValueTracker(0.35)
    stream_phase.add_updater(lambda m, dt: m.increment_value(stream_spd.get_value() * dt))
    stream_count = [6]

    def mk_stream():
        g = VGroup()
        p0 = stream_phase.get_value()
        n = stream_count[0]
        for k in range(n):
            u = (p0 + k / n) % 1.0
            pos = stream_path_pt(u, dna_x=dna_x, fork_y_fn=lambda: fork_y.get_value())
            if u > 0.48:
                tok = Circle(radius=0.13, color=GREEN, fill_color=BG, fill_opacity=0.96, stroke_width=3.0).move_to(pos)
                dt_ = T("d", size=22, color=GREEN, weight=BOLD).move_to(tok)
                dt_.layout_ok = True
                g.add(tok, dt_)
            else:
                g.add(Circle(radius=0.13, color=GREEN, fill_color=GREEN, fill_opacity=0.90, stroke_width=2.2).move_to(pos))
        return g

    stream = always_redraw(mk_stream)

    # Purine-carbon MAGENTA arrow from THF side to PURPLE build door
    pur_arrow = CurvedArrow(loop_pos + np.array([-0.75, LOOP_RY * 0.92, 0]),
                            BUILD_POS + np.array([0.24, -0.05, 0]),
                            angle=-0.20, color=MAGENTA, stroke_width=4.5, tip_length=0.20)
    pur_active_flag = [pur_active]
    pur_phase = ValueTracker(0.0)
    pur_phase.add_updater(lambda m, dt: m.increment_value(0.45 * dt))

    def mk_pur_dots():
        if not pur_active_flag[0]:
            return VGroup()
        g = VGroup()
        p0 = pur_phase.get_value()
        for k in range(2):
            u = (p0 + k * 0.5) % 1.0
            g.add(Dot(pur_arrow.point_from_proportion(u), radius=0.075, color=MAGENTA))
        return g

    pur_dots = always_redraw(mk_pur_dots)

    # dTMP path from above TS up to fork
    dtmp_active_flag = [dtmp_active]
    dtmp_phase = ValueTracker(0.0)
    dtmp_phase.add_updater(lambda m, dt: m.increment_value(0.36 * dt))

    def mk_dtmp():
        if not dtmp_active_flag[0]:
            return VGroup()
        g = VGroup()
        p0 = dtmp_phase.get_value()
        for k in range(2):
            u = (p0 + k * 0.5) % 1.0
            start = ts_pos + UP * 0.65
            end = np.array([dna_x - 0.65, fork_y.get_value(), 0.0])
            pos = (1 - u) * start + u * end
            tok = Circle(radius=0.12, color=GREEN, fill_color=BG, fill_opacity=0.96, stroke_width=3.0).move_to(pos)
            dot = Dot(tok.get_top() + UP * 0.04, radius=0.05, color=MAGENTA)
            g.add(tok, dot)
        return g

    dtmp_stream = always_redraw(mk_dtmp)

    world = VGroup(pool, pool_lbl, hgprt, prpp, arch, arch_lbl, dna, dna_lbl,
                   track, pur_arrow, dhfr, ts, stream, loop_rings, pur_dots, dtmp_stream)
    trackers = [fork_y, fork_spd, loop_phase, loop_spd, stream_phase, stream_spd, pur_phase, dtmp_phase]
    return dict(
        world=world, trackers=trackers, pool=pool, hgprt=hgprt, prpp=prpp, arch=arch, dna=dna, dna_lbl=dna_lbl,
        track=track, dhfr=dhfr, ts=ts, loop_rings=loop_rings, stream=stream,
        pur_arrow=pur_arrow, pur_dots=pur_dots, dtmp_stream=dtmp_stream,
        fork_y=fork_y, fork_spd=fork_spd, loop_spd=loop_spd, stream_spd=stream_spd,
        stream_count=stream_count, pur_active=pur_active_flag, dtmp_active=dtmp_active_flag,
    )


class S05Idea(SpokenScene):
    def construct(self):
        w = build_full_world(dhfr_notch=True, loop_speed=0.45)
        self.add(w["world"], scope_tag("schematic"), *w["trackers"])

        # Beat 1 (0.0s): Pull back to full world turning; text at top 'shape decides what fits'
        self.at("Here is the rule")
        rule_txt = T("shape decides what fits", size=34, color=TEXT, weight=BOLD).move_to([0.0, 3.22, 0])
        self.play(FadeIn(rule_txt), run_time=0.8)

        # Beat 2 (2.52s): DHFR enlarges with outward notch; MAGENTA ring slots in and slides on
        self.at("An enzyme accepts")
        dhfr_big = make_enzyme_chip("DHFR", DHFR_POS, color=BLUE, size=26, notch_side="left", w=1.45, h=0.84)
        fol_test = make_folate_ring(radius=0.19, loaded=False).move_to(DHFR_POS + LEFT * 1.85)
        self.play(ReplacementTransform(w["dhfr"], dhfr_big), FadeIn(fol_test), run_time=0.7)
        notch_pt = dhfr_big.dock_pt + LEFT * 0.24
        self.play(fol_test.animate.move_to(notch_pt), run_time=0.6)
        self.play(fol_test.animate.move_to(DHFR_POS + UP * 0.90 + RIGHT * 0.7).set_opacity(0.0), run_time=0.6)
        self.remove(fol_test)

        # Beat 3 (6.1s): TEAL look-alike ring drifts back, fits outward notch and STAYS; RED stall mark over notch
        self.at("A counterfeit that fits")
        teal_ring = make_drug_ring(radius=0.19, color=TEAL).move_to(DHFR_POS + LEFT * 2.1 + DOWN * 0.5)
        stall_mark = make_red_x(notch_pt, size=0.42)
        self.play(teal_ring.animate.move_to(notch_pt), run_time=1.0)
        w["loop_spd"].set_value(0.10)
        self.play(FadeIn(stall_mark), run_time=0.25)
        self.play(FadeOut(stall_mark), run_time=0.25)
        self.play(FadeIn(stall_mark), run_time=0.25)

        # Beat 4 (9.78s): 'antimetabolite' appears in TEAL beneath DHFR
        self.at("is a medicine")
        anti_lbl = T("antimetabolite", size=26, color=TEAL, weight=BOLD).move_to(DHFR_POS + DOWN * 1.25)
        self.play(FadeIn(anti_lbl), run_time=0.7)

        # Beat 5 (13.64s): Preview TEAL ring drifts out, stall lifts; fork speeds up & stream thickens; 'fastest demand'
        self.at("The dividing cell")
        w["stream_count"][0] = 9
        fast_lbl = T("fastest demand", size=24, color=GOLD).move_to([DNA_X, DNA_BOT - 0.42, 0])
        self.play(
            FadeOut(stall_mark),
            teal_ring.animate.shift(LEFT * 1.6).set_opacity(0.0),
            w["loop_spd"].animate.set_value(0.45),
            w["fork_spd"].animate.set_value(-0.55),
            w["stream_spd"].animate.set_value(0.60),
            FadeIn(fast_lbl),
            run_time=1.0
        )
        self.remove(teal_ring)
        self.finish()


class S06Predict(SpokenScene):
    def construct(self):
        w = build_full_world(dhfr_notch=True, loop_speed=0.45)
        self.add(w["world"], scope_tag("schematic"), *w["trackers"])

        # Beat 1 (0.0s): TEAL ring labelled 'methotrexate' glides into outward DHFR notch
        self.at("Methotrexate mimics")
        notch_pt = w["dhfr"].dock_pt + LEFT * 0.24
        mtx = make_drug_ring(radius=0.19, color=TEAL).move_to(DHFR_POS + LEFT * 2.0)
        mtx_lbl = T("methotrexate", size=24, color=TEAL).next_to(mtx, LEFT, buff=0.16)
        self.add(mtx, mtx_lbl)
        self.play(
            mtx.animate.move_to(notch_pt),
            mtx_lbl.animate.next_to(notch_pt, LEFT, buff=0.28),
            run_time=1.3
        )

        # Beat 2 (2.22s): RED X appears on DHFR lock notch and stays; loop slows down
        self.at("jams DHFR")
        red_x = make_red_x(notch_pt, size=0.42)
        self.play(
            FadeIn(red_x),
            w["loop_spd"].animate.set_value(0.10),
            run_time=0.8
        )

        # Beat 3 (7.42s): What runs short -> white ? in clear space beside dTMP path and MAGENTA build arrow
        self.at("What runs short")
        q1 = T("?", size=34, color=TEXT, weight=BOLD).move_to([2.25, 0.25, 0])
        q2 = T("?", size=34, color=TEXT, weight=BOLD).move_to([-1.65, 0.25, 0])
        qcard = question_card("Thymidylate, purines, or both?", y=3.20, color=TEXT, size=32)
        self.play(FadeIn(q1), FadeIn(q2), FadeIn(qcard), run_time=0.9)
        self.finish()


class S07Pause(PredictPause):
    QUESTION = "Thymidylate, purines, or both?"
    CARD = {"y": 3.20, "color": TEXT, "size": 32}
    RING_AT = (5.95, -2.35, 0)
    SECONDS = 4.5

    def backdrop(self):
        w = build_full_world(dhfr_notch=True, loop_speed=0.10, fork_speed_val=-0.18)
        notch_pt = w["dhfr"].dock_pt + LEFT * 0.24
        mtx = make_drug_ring(radius=0.19, color=TEAL).move_to(notch_pt)
        mtx_lbl = T("methotrexate", size=24, color=TEAL).next_to(notch_pt, LEFT, buff=0.28)
        red_x = make_red_x(notch_pt, size=0.42)
        q1 = T("?", size=34, color=TEXT, weight=BOLD).move_to([2.25, 0.25, 0])
        q2 = T("?", size=34, color=TEXT, weight=BOLD).move_to([-1.65, 0.25, 0])
        return Group(w["world"], mtx, mtx_lbl, red_x, q1, q2, scope_tag("schematic"), *w["trackers"])


class S08Answer(SpokenScene):
    def construct(self):
        w = build_full_world(dhfr_notch=True, loop_speed=0.10, fork_speed_val=-0.18)
        notch_pt = w["dhfr"].dock_pt + LEFT * 0.24
        mtx = make_drug_ring(radius=0.19, color=TEAL).move_to(notch_pt)
        mtx_lbl = T("methotrexate", size=24, color=TEAL).next_to(notch_pt, LEFT, buff=0.28)
        red_x = make_red_x(notch_pt, size=0.42)
        q1 = T("?", size=34, color=TEXT, weight=BOLD).move_to([2.25, 0.25, 0])
        q2 = T("?", size=34, color=TEXT, weight=BOLD).move_to([-1.65, 0.25, 0])
        qcard = question_card("Thymidylate, purines, or both?", y=3.20, color=TEXT, size=32)

        self.add(w["world"], mtx, mtx_lbl, red_x, q1, q2, qcard, scope_tag("schematic"), *w["trackers"])

        # Beat 1 (0.0s): Question card dissolves; both ? turn into RED marks
        self.at("Both")
        rx1 = make_red_x(q1.get_center(), size=0.40)
        rx2 = make_red_x(q2.get_center(), size=0.40)
        self.play(FadeOut(qcard), ReplacementTransform(q1, rx1), ReplacementTransform(q2, rx2), run_time=0.8)

        # Beat 2 (2.08s): DHF rings pile up beside jammed DHFR; THF side empties, no MAGENTA dots move
        self.at("With DHFR jammed")
        w["loop_spd"].set_value(0.0)
        w["loop_rings"].clear_updaters()
        pile_positions = [
            LOOP_POS + np.array([-0.90, -0.82, 0]),
            LOOP_POS + np.array([-0.45, -0.85, 0]),
            LOOP_POS + np.array([0.00, -0.85, 0]),
        ]
        dhf_pile = VGroup(*[make_folate_ring(radius=0.19, loaded=False, dim=True).move_to(p) for p in pile_positions])
        self.play(FadeOut(w["loop_rings"]), FadeIn(dhf_pile), run_time=1.0)

        # Beat 3 (7.04s): Both thymidylate and purine starved -> MAGENTA arrow fades to dotted outline; dTMP path runs dry
        self.at("Thymidylate and the purine")
        w["pur_active"][0] = False
        w["dtmp_active"][0] = False
        dotted_pur = DashedVMobject(w["pur_arrow"], num_dashes=10, dashed_ratio=0.45).set_stroke(opacity=0.40)
        self.play(ReplacementTransform(w["pur_arrow"], dotted_pur), run_time=1.0)

        # Beat 4 (12.24s): Cell runs short of dTMP -> fork stops below missing 'T' rung; tag 'no dTMP' in clear spot
        self.at("The cell runs short")
        gap_y = 0.25
        self.play(w["fork_y"].animate.set_value(gap_y - 0.18), run_time=0.9)
        w["fork_spd"].set_value(0.0)
        w["fork_y"].clear_updaters()
        stalled_dna = build_dna_ladder(fork_tracker=w["fork_y"], opacity=1.0, missing_t_y=gap_y)
        no_dtmp_lbl = T("no dTMP", size=24, color=RED, weight=BOLD).move_to([DNA_X + 1.25, gap_y, 0])
        t_miss = T("T", size=22, color=RED, weight=BOLD).move_to([DNA_X, gap_y, 0])
        t_miss.layout_ok = True
        self.play(FadeOut(w["dna"]), FadeIn(stalled_dna), FadeIn(no_dtmp_lbl), FadeIn(t_miss), run_time=0.7)
        self.finish()


class S09Fluorouracil(SpokenScene):
    def construct(self):
        w = build_full_world(dhfr_notch=True, loop_speed=0.45, fork_speed_val=-0.28)
        self.add(w["world"], scope_tag("schematic"), *w["trackers"])

        # Beat 1 (1.36s): 5-fluorouracil mimics uracil -> TEAL base token enters below loop
        self.at("mimics uracil")
        fu_tok = make_base_token(TEAL, w=0.42, h=0.22).move_to([0.2, -2.85, 0])
        fu_lbl = T("5-fluorouracil", size=24, color=TEAL).next_to(fu_tok, RIGHT, buff=0.16)
        self.play(FadeIn(fu_tok), FadeIn(fu_lbl), run_time=0.7)

        # Beat 2 (3.56s): Inside the cell it becomes FdUMP -> gains nucleotide outline & relabels
        self.at("Inside the cell")
        fdump_tok = make_nuc_token(radius=0.17, color=TEAL, deoxy=True).move_to(TS_POS + np.array([-0.40, -0.95, 0]))
        fdump_lbl = T("FdUMP", size=24, color=TEAL).next_to(fdump_tok, DOWN, buff=0.22)
        self.play(
            ReplacementTransform(fu_tok, fdump_tok),
            swap(fu_lbl, fdump_lbl, run_time=0.55),
            run_time=0.95
        )

        # Beat 3 (6.46s): traps thymidylate synthase -> lodges neatly below TS chip; RED X at bottom-right edge of TS
        self.at("which traps")
        ts_dock = TS_POS + np.array([0.0, -0.82, 0])
        red_x = make_red_x(w["ts"].get_bottom() + DOWN * 0.20 + RIGHT * 0.55, size=0.42)
        self.play(
            fdump_tok.animate.move_to(ts_dock),
            fdump_lbl.animate.next_to(ts_dock, DOWN, buff=0.22),
            FadeIn(red_x),
            run_time=0.9
        )
        w["dtmp_active"][0] = False

        # Beat 4 (9.76s): A different lock, same shortage -> real dUMP queue cleanly ABOVE TS chip; fork stops at missing T rung
        self.at("A different lock")
        queue = VGroup(*[
            make_nuc_token(radius=0.14, color=GREEN, deoxy=True).move_to(TS_POS + np.array([-0.36 + 0.36 * k, 0.78, 0]))
            for k in range(3)
        ])
        dump_q_lbl = T("dUMP", size=24, color=GREEN).next_to(queue, UP, buff=0.18)
        gap_y = 0.25
        self.play(FadeIn(queue), FadeIn(dump_q_lbl), w["fork_y"].animate.set_value(gap_y - 0.18), run_time=0.9)
        w["fork_spd"].set_value(0.0)
        w["fork_y"].clear_updaters()
        stalled_dna = build_dna_ladder(fork_tracker=w["fork_y"], opacity=1.0, missing_t_y=gap_y)
        no_dtmp_lbl = T("no dTMP", size=24, color=RED, weight=BOLD).move_to([DNA_X + 1.25, gap_y, 0])
        t_miss = T("T", size=22, color=RED, weight=BOLD).move_to([DNA_X, gap_y, 0])
        t_miss.layout_ok = True
        self.play(FadeOut(w["dna"]), FadeIn(stalled_dna), FadeIn(no_dtmp_lbl), FadeIn(t_miss), run_time=0.6)
        self.finish()


class S10Mercaptopurine(SpokenScene):
    def construct(self):
        p_center = np.array([-3.20, 0.55, 0.0])
        p_r = 1.45
        pool = make_pool(center=p_center, radius=p_r, opacity=1.0)
        animate_pool_tokens(pool, speed_mult=1.0)
        pool_lbl = T("pool", size=28, color=GREEN).move_to(p_center + UP * (p_r + 0.35))

        hgprt_pos = p_center + np.array([-1.15, -1.65, 0])
        prpp_pos = p_center + np.array([1.25, -1.65, 0])
        hgprt = make_enzyme_chip("HGPRT", hgprt_pos, color=BLUE, size=26, notch_side="left")
        prpp = make_enzyme_chip("PRPP", prpp_pos, color=PURPLE, size=26)
        rec_lbl = T("recycle", size=24, color=BLUE).next_to(hgprt, DOWN, buff=0.18)
        bld_lbl = T("build", size=24, color=PURPLE).next_to(prpp, DOWN, buff=0.18)

        arch_pos = np.array([1.05, 0.55, 0.0])
        arch = make_arch(center=arch_pos, scale=1.22, opacity=1.0)
        arch_lbl = T("ribonucleotide\nreductase", size=24, color=BLUE).move_to(arch_pos + UP * 1.32)

        dna_x = 4.65
        fork_y = ValueTracker(0.95)
        fork_spd = ValueTracker(-0.26)
        fork_y.add_updater(lambda m, dt: m.set_value(1.65 if m.get_value() < -0.55 else m.get_value() + fork_spd.get_value() * dt))
        dna = build_dna_ladder(x=dna_x, y_top=2.35, y_bot=-2.15, width=0.90, fork_tracker=fork_y, opacity=1.0)
        dna_lbl = T("DNA", size=26, color=TEXT).move_to([dna_x, 2.75, 0])

        s_phase = ValueTracker(0.0)
        s_phase.add_updater(lambda m, dt: m.increment_value(0.35 * dt))
        stream = make_token_stream(
            lambda u: stream_path_pt(u, p_center, p_r, arch_pos, dna_x, lambda: fork_y.get_value()),
            5, s_phase, deoxy=True, radius=0.14
        )

        # Yellow bases recycling strictly OUTSIDE HGPRT box
        yb_phase = ValueTracker(0.0)
        yb_phase.add_updater(lambda m, dt: m.increment_value(0.28 * dt))
        def mk_yb():
            g = VGroup()
            p0 = yb_phase.get_value()
            lx = hgprt.get_left()[0] - 0.55
            ty = hgprt.get_top()[1] + 0.26
            pts = [
                p_center + LEFT * p_r,
                np.array([lx, -0.25, 0]),
                np.array([lx, ty, 0]),
                np.array([hgprt.get_center()[0] + 0.20, ty, 0]),
                pool.rec_door.get_center(),
            ]
            for k in range(2):
                u = (p0 + k * 0.5) % 1.0
                idx = min(3, int(u * 4))
                frac = u * 4 - idx
                pos = (1 - frac) * pts[idx] + frac * pts[idx + 1]
                g.add(make_base_token(YELLOW).move_to(pos))
            return g
        ybases = always_redraw(mk_yb)

        self.add(pool, pool_lbl, hgprt, prpp, rec_lbl, bld_lbl, arch, arch_lbl, dna, dna_lbl,
                 stream, ybases, scope_tag("schematic"), fork_y, fork_spd, s_phase, yb_phase)

        # Beat 1 (1.78s): 6-mercaptopurine enters from left among yellow bases
        self.at("a fake purine")
        mp_tok = make_base_token(TEAL, w=0.40, h=0.22).move_to([-5.65, 0.95, 0])
        mp_lbl = T("6-mercaptopurine", size=24, color=TEAL).move_to([-4.95, 2.95, 0])
        mp_arrow = Arrow(mp_lbl.get_bottom() + DOWN * 0.06, mp_tok.get_top() + UP * 0.08, color=TEAL, stroke_width=3.5, buff=0.04)
        self.play(FadeIn(mp_tok), FadeIn(mp_lbl), FadeIn(mp_arrow), run_time=0.75)

        # Beat 2 (2.96s): enters through recycle door -> HGPRT accepts it (lock turns)
        self.at("enters through the recycle")
        notch_pt = hgprt.dock_pt + LEFT * 0.24
        self.play(FadeOut(mp_arrow, run_time=0.25), FadeOut(mp_lbl, run_time=0.25))
        self.play(mp_tok.animate.move_to(notch_pt), run_time=0.85)
        self.play(Rotate(hgprt.notch, angle=PI / 3), run_time=0.45)
        self.play(mp_tok.animate.move_to(p_center + np.array([0.0, -0.55, 0])), Rotate(hgprt.notch, angle=-PI / 3), run_time=0.9)

        # Beat 3 (9.08s): turns into counterfeit nucleotides -> label cleanly OUTSIDE pool in dark area!
        self.at("turns it into counterfeit")
        cf_tok = make_nuc_token(radius=0.17, color=TEAL, deoxy=True).move_to(mp_tok)
        cf_lbl = T("counterfeit", size=26, color=TEAL, weight=BOLD).move_to([-1.55, 2.45, 0])
        cf_ptr = Line(cf_lbl.get_bottom() + DOWN * 0.08, cf_tok.get_top() + UP * 0.14, color=TEAL, stroke_width=3.0)
        self.play(ReplacementTransform(mp_tok, cf_tok), FadeIn(cf_lbl), Create(cf_ptr), run_time=0.9)

        # Beat 4 (12.56s): shut down purine building -> RED bar closes across PURPLE build door
        self.at("shut down purine")
        red_bar = Line(pool.bld_door.get_center() + np.array([-0.45, 0.25, 0]),
                       pool.bld_door.get_center() + np.array([0.45, -0.25, 0]), color=RED, stroke_width=7.5)
        red_bar2 = Line(pool.bld_door.get_center() + np.array([-0.45, -0.25, 0]),
                        pool.bld_door.get_center() + np.array([0.45, 0.25, 0]), color=RED, stroke_width=7.5)
        self.play(FadeIn(VGroup(red_bar, red_bar2)), run_time=0.7)

        # Beat 5 (15.24s): built into DNA -> counterfeit travels through arch to fork & becomes TEAL rung
        self.at("Once built into")
        self.play(FadeOut(cf_lbl), FadeOut(cf_ptr), cf_tok.animate.move_to(arch_pos), run_time=0.8)
        target_y = fork_y.get_value()
        self.play(cf_tok.animate.move_to([dna_x - 0.60, target_y, 0]), run_time=0.7)
        teal_y = target_y + 0.14
        cracked_dna = build_dna_ladder(x=dna_x, y_top=2.35, y_bot=-2.15, width=0.90,
                                       fork_tracker=fork_y, opacity=1.0, teal_rung_y=teal_y)
        self.play(FadeOut(cf_tok), FadeOut(dna), FadeIn(cracked_dna), run_time=0.5)

        # Beat 6 (17.94s): damage leukemia cells -> RED crack on ladder + tag 'leukemia cell' cleanly below DNA ladder
        self.at("the leukemia cells")
        crack = VMobject(color=RED, stroke_width=6.0).set_points_as_corners([
            [dna_x - 0.55, teal_y + 0.35, 0],
            [dna_x - 0.15, teal_y + 0.15, 0],
            [dna_x + 0.22, teal_y - 0.05, 0],
            [dna_x - 0.10, teal_y - 0.25, 0],
            [dna_x + 0.55, teal_y - 0.42, 0],
        ])
        leuk_lbl = T("leukemia cell", size=26, color=RED, weight=BOLD).move_to([dna_x, -2.55, 0])
        self.play(Create(crack), FadeIn(leuk_lbl), run_time=0.8)
        self.finish()


class S11Close(SpokenScene):
    def construct(self):
        # Compact right side slightly so both main ladder (x=3.85) and small normal tissue ladder (x=5.65) have plenty of room
        s11_loop_pos = np.array([-0.80, -1.45, 0.0])
        s11_loop_rx = 1.15
        s11_dhfr_pos = np.array([-2.95, -1.45, 0.0])
        s11_ts_pos = np.array([1.75, -1.45, 0.0])
        s11_dna_x = 3.85
        w = build_full_world(dhfr_notch=True, loop_speed=0.45, fork_speed_val=-0.28,
                             dna_x=s11_dna_x, ts_pos=s11_ts_pos,
                             loop_pos=s11_loop_pos, loop_rx=s11_loop_rx, dhfr_pos=s11_dhfr_pos)
        self.add(w["world"], scope_tag("schematic"), *w["trackers"])

        # Beat 1 (1.62s): three TEAL ghosts appear at their locks in turn: DHFR, TS, HGPRT
        self.at("almost right")
        g_dhfr = make_drug_ring(radius=0.19, color=TEAL, opacity=0.78).move_to(w["dhfr"].dock_pt + LEFT * 0.24)
        g_ts = make_nuc_token(radius=0.15, color=TEAL, deoxy=True).set_opacity(0.78).move_to(s11_ts_pos + DOWN * 0.80)
        g_hgprt = make_base_token(TEAL, w=0.36, h=0.20).set_opacity(0.78).move_to(w["hgprt"].get_left() + LEFT * 0.28)
        self.play(FadeIn(g_dhfr), run_time=0.4)
        self.play(FadeIn(g_ts), run_time=0.4)
        self.play(FadeIn(g_hgprt), run_time=0.4)

        # Beat 2 (4.9s): road to DNA -> white glowing path lights from pool through arch to fork (above TS!)
        self.at("road to DNA")
        road = Line(POOL_POS + RIGHT * POOL_R, np.array([s11_dna_x - 0.55, 1.38, 0]), color=TEXT, stroke_width=7).set_opacity(0.35)
        road.set_z_index(-1)
        self.play(Create(road), run_time=0.9)

        # Beat 3 (8.28s): dividing cell needs that road most -> fork speeds up and stream thickens
        self.at("needs that road most")
        w["stream_count"][0] = 9
        self.play(w["fork_spd"].animate.set_value(-0.52), w["stream_spd"].animate.set_value(0.58), run_time=0.8)

        # Beat 4 (10.94s): normal tissues -> smaller WHITE ladder at far right labelled 'normal dividing tissue'
        self.at("normal tissues")
        n_x = 5.65
        n_fork_y = ValueTracker(0.2)
        n_fork_spd = ValueTracker(-0.15)
        n_fork_y.add_updater(lambda m, dt: m.set_value(0.75 if m.get_value() < -1.15 else m.get_value() + n_fork_spd.get_value() * dt))
        self.add(n_fork_y, n_fork_spd)
        n_dna = build_dna_ladder(x=n_x, y_top=1.05, y_bot=-1.40, width=0.52, fork_tracker=n_fork_y, opacity=0.92)
        n_lbl = fit_text("normal dividing tissue", max_w=1.65, size=22, color=TEXT).move_to([n_x, 1.85, 0])
        n_stream_phase = ValueTracker(0.0)
        n_stream_spd = ValueTracker(0.30)
        n_stream_op = ValueTracker(0.85)
        n_stream_phase.add_updater(lambda m, dt: m.increment_value(n_stream_spd.get_value() * dt))
        self.add(n_stream_phase, n_stream_spd, n_stream_op)

        def mk_n_stream():
            g = VGroup()
            p0 = n_stream_phase.get_value()
            op = n_stream_op.get_value()
            start = np.array([s11_dna_x + 0.60, 0.45, 0.0])
            end = np.array([n_x - 0.38, n_fork_y.get_value(), 0.0])
            for k in range(2):
                u = (p0 + k * 0.5) % 1.0
                pos = (1 - u) * start + u * end
                tok = Circle(radius=0.10, color=GREEN, fill_color=BG, fill_opacity=0.95 * op, stroke_width=2.4).set_stroke(opacity=op).move_to(pos)
                g.add(tok)
            return g

        n_stream = always_redraw(mk_n_stream)
        self.play(FadeIn(n_dna), FadeIn(n_lbl), FadeIn(n_stream), run_time=0.6)
        self.play(
            g_dhfr.animate.set_stroke(opacity=1.0),
            n_fork_spd.animate.set_value(-0.08),
            n_stream_spd.animate.set_value(0.14),
            n_stream_op.animate.set_value(0.45),
            w["fork_spd"].animate.set_value(-0.28),
            run_time=0.6
        )
        self.finish()


class S12End(EndCard):
    LINE = "Counterfeits jam the nucleotide supply;\ncells dividing fastest are hit hardest."
