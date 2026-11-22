"""
"Still Talking, Until Sealed Inside" — Chapter 2 of Endocytosis and Signaling Endosomes.

COLOUR MAP (one colour per concept across the whole film):
    MEMBRANE     = "#60A5FA"   slate-blue plasma & endosome lipid membrane
    RAB5         = "#38BDF8"   cyan Rab5 marker (early endosome)
    RAB7         = "#E879F9"   magenta-purple Rab7 marker (late endosome)
    RECEPTOR     = "#34D399"   emerald active receptor & active cytosolic tail signal
    SILENCED     = "#94A3B8"   muted slate-grey sealed/silenced receptor body (labels stay TEXT)
    LIGAND       = "#E2E8F0"   crisp pale ligand bound to receptor head
    PARTNER      = "#7DD3FC"   sky-blue cytosolic partner / MyD88 adaptor
    TRIF_COL     = "#A3E635"   bright lime-gold endosomal adaptor TRIF & interferon output
    UBIQUITIN    = "#FACC15"   gold-yellow ubiquitin sorting tag
    ESCRT        = "#F43F5E"   rose-red ESCRT membrane-bending clamps
    TUBULE       = "#2DD4BF"   mint-teal recycling tubules
    LUMEN_EARLY  = "#FBBF24"   soft amber early endosome lumen (pH 6-6.5)
    LUMEN_LATE   = "#F97316"   warm orange late endosome lumen (pH ~5.5)
    LYSO         = "#EF4444"   deep coral-red lysosome & pH 5 / 100x H+ state

CARRIED WORLD:
    Cross-section of the cell's outer plasma membrane above dark cytosol and a large
    Rab5-rimmed early endosome with a soft amber lumen, tracked as an internalized active
    receptor's cytosolic tail keeps signaling until ESCRT buds the membrane inward into
    an internal vesicle and seals the tail off from cytosolic partners.

WHAT CHANGES IN EACH SPOKEN SCENE (and what it is computed from):
    s01_hook: Active emerald receptor rides a descending vesicle path (parametric Bezier
        in tracker t) from plasma membrane into the Rab5 early endosome outer wall, then
        radiates computed expanding signal arcs into the cytosol.
    s02_topology_partners: Smooth transition onto the zoomed outer endosome wall; sky-blue
        partner docks along a computed arc beside the cytosolic tail and triggers signal
        arcs, then undocks as a lime-gold partner docks and sends a new signal.
    s03_tlr4_switch: TLR4 binds ligand at top plasma membrane, docks sky-blue MyD88,
        releases it, descends in a vesicle into the Rab5 endosome below, and docks
        lime-gold TRIF to drive expanding interferon-gene signal arcs.
    s04_ubiquitin_escrt: Active receptors drift toward the recycling tubule until gold
        ubiquitin tags fly in onto their tails one by one; rose-red ESCRT clamps glide
        onto the membrane and slide all three receptors along computed polar angles
        theta(t) into one dense top patch.
    s05_inward_bud: Coated-pit reference bends smoothly into cytosol (computed pit depth),
        while ESCRT drives a computed parametric inward omega-invagination depth(t) into
        the amber lumen, pinching off a sealed internal vesicle with the tail inside.
    s06_predict: Zoomed multivesicular endosome holds the internal vesicle drifting gently
        in the lumen while cytosolic partner blocks bounce off the outer membrane along
        computed collision trajectories; question card appears for the predict pause.
    s08_sealed_reveal: Question card clears; enclosed receptor dims to muted grey and
        partners drift away while the endosome reframes and two more internal vesicles
        bud inward into the lumen to fill the multivesicular endosome.
    s09_rab_conversion_acid: Cyan Rab5 badges detach as purple Rab7 badges dock; a live
        pH ValueTracker (6.5 -> 4.9) drives computed lumen colour interpolation, lysosome
        fusion + enzymatic vesicle breakdown once pH reaches ~5.5, and a growing Plot
        curve of relative [H+] = 10**(7 - pH).
    s10_met_escape: Early endosome carries mutant MET that loses its docking segment;
        gold ubiquitin beads repeatedly approach and bounce off, rose-red ESCRT clamps
        glide past without gripping, and mutant MET keeps radiating active signal arcs.
    s11_close: Receptor enters the endosome wall active; mild acid detaches a second
        ligand to dim its tail, while the bound outer-wall receptor keeps radiating active
        signal arcs opposite the silenced receptor sealed inside an internal vesicle.
"""
from bp_parts import *

# ------------------------------------------------------------------ Colour map
MEMBRANE = "#60A5FA"
RAB5 = "#38BDF8"
RAB7 = "#E879F9"
RECEPTOR = "#34D399"
SILENCED = "#94A3B8"
LIGAND = "#E2E8F0"
PARTNER = "#7DD3FC"
TRIF_COL = "#A3E635"
UBIQUITIN = "#FACC15"
ESCRT = "#F43F5E"
TUBULE = "#2DD4BF"
LUMEN_EARLY = "#FBBF24"
LUMEN_LATE = "#F97316"
LYSO = "#EF4444"


# ------------------------------------------------------------------ Helpers
def make_receptor(pos, tail_angle=PI / 2, scale=1.0, active=True, ligand=True,
                  notched=False, ub_count=0):
    """Build a schematic transmembrane receptor oriented along `tail_angle`.

    `tail_angle` points from the lumen/extracellular side toward the cytoplasmic tail tip.
    """
    col = RECEPTOR if active else SILENCED
    stem_len = 0.50 * scale
    tail_len = 0.68 * scale
    w = 0.11 * scale

    g = VGroup()
    head = Arc(radius=0.17 * scale, start_angle=-0.25 * PI, angle=1.5 * PI,
               color=col, stroke_width=4.5 * scale)
    head.rotate(-PI / 2)
    head.move_to([0, -stem_len * 0.55, 0])
    g.add(head)

    if ligand:
        lig = Dot(point=[0, -stem_len * 0.68, 0], radius=0.105 * scale,
                  color=LIGAND, stroke_color=col, stroke_width=2.0 * scale)
        g.add(lig)

    stem = RoundedRectangle(corner_radius=0.04 * scale, width=w, height=stem_len,
                            stroke_color=col, stroke_width=2.5 * scale,
                            fill_color=col, fill_opacity=0.85)
    stem.move_to([0, 0, 0])
    g.add(stem)

    tip_y = stem_len * 0.45 + tail_len
    gap_mark = None
    if not notched:
        tail = Line([0, stem_len * 0.45, 0], [0, tip_y, 0],
                    color=col, stroke_width=5.0 * scale)
        prong = Line([0, stem_len * 0.45 + 0.42 * tail_len, 0],
                     [0.17 * scale, stem_len * 0.45 + 0.56 * tail_len, 0],
                     color=col, stroke_width=4.0 * scale)
        tip = Dot([0, tip_y, 0], radius=0.09 * scale, color=col)
        g.add(tail, prong, tip)
    else:
        seg1 = Line([0, stem_len * 0.45, 0], [0, stem_len * 0.45 + 0.28 * tail_len, 0],
                    color=col, stroke_width=5.0 * scale)
        gap_mark = DashedLine([0, stem_len * 0.45 + 0.30 * tail_len, 0],
                              [0, stem_len * 0.45 + 0.62 * tail_len, 0],
                              color=UBIQUITIN, stroke_width=3.2 * scale, dash_length=0.07 * scale)
        seg2 = Line([0, stem_len * 0.45 + 0.64 * tail_len, 0],
                    [0, tip_y, 0],
                    color=col, stroke_width=5.0 * scale)
        tip = Dot([0, tip_y, 0], radius=0.09 * scale, color=col)
        g.add(seg1, gap_mark, seg2, tip)

    halo = None
    if active:
        halo = Circle(radius=0.21 * scale, color=RECEPTOR, stroke_width=2.5 * scale,
                      fill_color=RECEPTOR, fill_opacity=0.25)
        halo.move_to([0, tip_y, 0])
        g.add(halo)

    for k in range(ub_count):
        ub = Dot([0.16 * scale * (1 if k % 2 == 0 else -1),
                  stem_len * 0.45 + (0.35 + 0.25 * k) * tail_len, 0],
                 radius=0.09 * scale, color=UBIQUITIN, stroke_color=BG, stroke_width=1.5)
        g.add(ub)

    g.rotate(tail_angle - PI / 2, about_point=ORIGIN)
    g.move_to(pos)
    tip_offset = np.array([np.cos(tail_angle), np.sin(tail_angle), 0.0]) * (0.45 * stem_len + tail_len - 0.1 * scale)
    g.tail_tip = np.array(pos, dtype=float) + tip_offset
    g.tip_mob = tip
    g.halo_mob = halo
    g.gap_mob = gap_mark
    return g


def make_signal_arcs(origin_fn, angle=PI / 2, color=RECEPTOR, max_r=1.15,
                     spread=0.72 * PI, n_waves=4, speed=1.1, active_fn=None):
    """Computed expanding concentric signal arcs driven by scene elapsed time."""
    holder = VGroup()
    holder._t = 0.0

    def rebuild():
        if active_fn is not None and not active_fn():
            return VGroup()
        c = origin_fn() if callable(origin_fn) else np.array(origin_fn, dtype=float)
        ang = angle() if callable(angle) else angle
        grp = VGroup()
        for k in range(n_waves):
            frac = (holder._t * speed + k / n_waves) % 1.0
            r = 0.18 + frac * (max_r - 0.18)
            op = max(0.32, 0.95 * (1.0 - 0.50 * frac))
            sw = 7.0 * (1.0 - 0.30 * frac)
            arc = Arc(radius=r, start_angle=ang - spread / 2, angle=spread,
                      arc_center=c, stroke_color=color, stroke_width=sw,
                      stroke_opacity=op)
            grp.add(arc)
        return grp

    waves = always_redraw(rebuild)
    waves.layout_ok = True

    def tick(m, dt):
        holder._t += dt

    holder.add_updater(tick)
    return VGroup(holder, waves)


def make_rab_badges(center, rx, ry, angles, color=RAB5, r_offset=0.14):
    """Build Rab GTPase badges along the outer rim of an ellipse."""
    c = np.array(center, dtype=float)
    grp = VGroup()
    for a in angles:
        p = c + np.array([(rx + r_offset) * np.cos(a), (ry + r_offset) * np.sin(a), 0.0])
        pill = RoundedRectangle(corner_radius=0.07, width=0.28, height=0.16,
                                stroke_color=color, stroke_width=2.0,
                                fill_color=color, fill_opacity=0.88)
        pill.rotate(a + PI / 2).move_to(p)
        grp.add(pill)
    return grp


def make_endosome(center=(0.0, -0.45, 0.0), rx=2.25, ry=1.75, lumen_color=LUMEN_EARLY,
                  lumen_opacity=0.15, with_tubule=True, rab_color=RAB5, rab_angles=None):
    """Build the carried early/late endosome body with optional left recycling tubule."""
    c = np.array(center, dtype=float)
    g = VGroup()

    if with_tubule:
        tub_pts = [
            c + np.array([-rx * 0.92, 0.35, 0.0]),
            c + np.array([-rx - 0.55, 0.58, 0.0]),
            c + np.array([-rx - 1.15, 0.72, 0.0]),
            c + np.array([-rx - 1.35, 0.55, 0.0]),
            c + np.array([-rx - 1.12, 0.34, 0.0]),
            c + np.array([-rx - 0.52, 0.22, 0.0]),
            c + np.array([-rx * 0.95, -0.05, 0.0]),
        ]
        tub = VMobject(stroke_color=TUBULE, stroke_width=4.5,
                       fill_color=TUBULE, fill_opacity=0.18)
        tub.set_points_smoothly(tub_pts)
        g.add(tub)

    body = Ellipse(width=2 * rx, height=2 * ry, stroke_color=MEMBRANE, stroke_width=5.5,
                   fill_color=lumen_color, fill_opacity=lumen_opacity).move_to(c)
    inner_rim = Ellipse(width=2 * rx - 0.14, height=2 * ry - 0.14,
                        stroke_color=MEMBRANE, stroke_width=1.8,
                        stroke_opacity=0.45, fill_opacity=0.0).move_to(c)
    g.add(body, inner_rim)
    g.body = body

    if rab_angles is None:
        rab_angles = [0.15 * PI, 0.35 * PI, 0.68 * PI, 1.18 * PI, 1.45 * PI, 1.75 * PI]
    if rab_angles:
        rabs = make_rab_badges(c, rx, ry, rab_angles, color=rab_color)
        g.add(rabs)
        g.rabs = rabs
    return g


def make_plasma_membrane(y=2.55, x_span=11.6, pit_depth=0.0, pit_x=0.0):
    """Curved plasma membrane across the top of the frame with optional pit indent."""
    xs = np.linspace(-x_span / 2, x_span / 2, 160)
    arch = 0.22 * (1.0 - (xs / (x_span / 2)) ** 2)
    pit = pit_depth * np.exp(-((xs - pit_x) / 0.55) ** 2)
    ys = y + arch - pit
    pts_top = [np.array([x, yy + 0.07, 0.0]) for x, yy in zip(xs, ys)]
    pts_bot = [np.array([x, yy - 0.07, 0.0]) for x, yy in zip(xs, ys)]
    top_ln = VMobject(stroke_color=MEMBRANE, stroke_width=4.5).set_points_as_corners(pts_top)
    bot_ln = VMobject(stroke_color=MEMBRANE, stroke_width=2.5, stroke_opacity=0.6).set_points_as_corners(pts_bot)
    return VGroup(top_ln, bot_ln)


def make_partner_block(label_text=None, color=PARTNER, size=24, width=1.1, height=0.52):
    """Notched cytosolic partner/adaptor block that docks onto a receptor tail."""
    box = RoundedRectangle(corner_radius=0.12, width=width, height=height,
                           stroke_color=color, stroke_width=2.8,
                           fill_color=color, fill_opacity=0.22)
    if label_text:
        lbl = T(label_text, size=size, color=color)
        if lbl.width > width - 0.24:
            box = RoundedRectangle(corner_radius=0.12, width=lbl.width + 0.34, height=height,
                                   stroke_color=color, stroke_width=2.8,
                                   fill_color=color, fill_opacity=0.22)
        return VGroup(box, lbl.move_to(box))
    return box


def make_escrt_clamp(scale=1.0):
    """Rose-red C-shaped ESCRT clamp."""
    arc = Arc(radius=0.22 * scale, start_angle=-0.25 * PI, angle=1.5 * PI,
              stroke_color=ESCRT, stroke_width=6.0 * scale)
    jaw1 = Dot([0.22 * scale * np.cos(-0.25 * PI), 0.22 * scale * np.sin(-0.25 * PI), 0],
               radius=0.055 * scale, color=ESCRT)
    jaw2 = Dot([0.22 * scale * np.cos(1.25 * PI), 0.22 * scale * np.sin(1.25 * PI), 0],
               radius=0.055 * scale, color=ESCRT)
    return VGroup(arc, jaw1, jaw2)


def make_budding_endosome_curve(center, rx, ry, depth, bud_theta=PI / 2, bud_r=0.58):
    """Compute closed endosome wall + lumen polygon and bud bottom for depth in [0, 1]."""
    c = np.array(center, dtype=float)
    n = 240
    span = 0.26
    thetas_outer = np.linspace(bud_theta + span, bud_theta + TAU - span, n)
    pts_outer = np.column_stack([c[0] + rx * np.cos(thetas_outer),
                                 c[1] + ry * np.sin(thetas_outer),
                                 np.zeros(n)])

    n_out = np.array([np.cos(bud_theta), np.sin(bud_theta), 0.0])
    wall_anchor = c + np.array([rx * np.cos(bud_theta), ry * np.sin(bud_theta), 0.0])

    p_right = c + np.array([rx * np.cos(bud_theta - span), ry * np.sin(bud_theta - span), 0.0])
    p_left = c + np.array([rx * np.cos(bud_theta + span), ry * np.sin(bud_theta + span), 0.0])

    p1 = min(1.0, depth / 0.65)
    p2 = max(0.0, (depth - 0.65) / 0.35)
    drop = (0.15 + 0.95 * p1 + 0.25 * p2) * bud_r * 1.45
    bud_center = wall_anchor - n_out * drop

    neck_half_ang = max(0.05, 0.85 * (1.0 - 0.72 * p1) * (1.0 - 0.88 * p2))
    pocket_angles = np.linspace(bud_theta - neck_half_ang,
                                bud_theta - TAU + neck_half_ang, 48)
    r_eff = bud_r * (0.35 + 0.65 * p1)
    pocket_pts = np.array([
        bud_center + r_eff * np.array([np.cos(a), np.sin(a), 0.0])
        for a in pocket_angles
    ])

    def bez(a0, a1, m=14):
        s = np.linspace(0, 1, m)[:, None]
        mid_a = a0 + 0.5 * (a1 - a0)
        c1 = a0 + 0.35 * (a1 - a0) + n_out * 0.04
        c2 = mid_a - n_out * 0.05
        return ((1 - s) ** 3) * a0 + 3 * ((1 - s) ** 2) * s * c1 + 3 * (1 - s) * (s ** 2) * c2 + (s ** 3) * a1

    conn_r = bez(p_right, pocket_pts[0], 12)[:-1]
    conn_l = bez(pocket_pts[-1], p_left, 12)[1:]
    bud_patch = np.vstack([conn_r, pocket_pts, conn_l])

    flat_angles = np.linspace(bud_theta - span, bud_theta + span, len(bud_patch))
    flat_patch = np.array([
        c + np.array([rx * np.cos(a), ry * np.sin(a), 0.0])
        for a in flat_angles
    ])

    raw = float(np.clip(depth / 0.25, 0.0, 1.0))
    blend = raw * raw * (3.0 - 2.0 * raw)
    pts_patch = (1.0 - blend) * flat_patch + blend * bud_patch
    bud_bottom = (1.0 - blend) * wall_anchor + blend * (bud_center - n_out * r_eff)
    all_pts = np.vstack([pts_patch, pts_outer])
    return all_pts, bud_center, bud_bottom


def make_enzyme_wedge(color=LYSO, scale=0.20):
    """Simple geometric digestive enzyme icon (not a molecular structure)."""
    return AnnularSector(inner_radius=0.0, outer_radius=scale,
                         start_angle=0.2 * PI, angle=1.6 * PI,
                         color=color, fill_opacity=0.85, stroke_width=1.5)


def make_s06_backdrop(animated=False, show_partners=True):
    """Build the zoomed-in multivesicular endosome world shared by s06_predict, s07_pause, s08_sealed_reveal."""
    world = VGroup()

    endo_c = np.array([0.0, -0.25, 0.0])
    endo_rx, endo_ry = 3.15, 1.80
    outer_wall = Ellipse(width=2 * endo_rx, height=2 * endo_ry,
                         stroke_color=MEMBRANE, stroke_width=5.5,
                         fill_color=LUMEN_EARLY, fill_opacity=0.15).move_to(endo_c)
    inner_wall = Ellipse(width=2 * endo_rx - 0.14, height=2 * endo_ry - 0.14,
                         stroke_color=MEMBRANE, stroke_width=1.8,
                         stroke_opacity=0.4, fill_opacity=0.0).move_to(endo_c)
    rab_angles = [0.14 * PI, 0.34 * PI, 0.66 * PI, 0.86 * PI, 1.25 * PI, 1.75 * PI]
    rabs = make_rab_badges(endo_c, endo_rx, endo_ry, rab_angles, color=RAB5, r_offset=0.14)
    world.add(outer_wall, inner_wall, rabs)

    ilv_c = np.array([0.0, -0.22, 0.0])
    ilv_r = 0.85
    ilv_ring = Circle(radius=ilv_r, stroke_color=MEMBRANE, stroke_width=4.8,
                      fill_color=BG, fill_opacity=0.85).move_to(ilv_c)
    rec_pos = ilv_c + np.array([0.0, ilv_r, 0.0])
    rec = make_receptor(rec_pos, tail_angle=-PI / 2, scale=0.72, active=True, ligand=True)
    ilv_group = VGroup(ilv_ring, rec)
    if animated:
        bob(ilv_group, amp=0.06, speed=1.6, seed=1)

    world.add(ilv_group)
    world.ilv_group = ilv_group
    world.ilv_ring = ilv_ring
    world.rec = rec
    world.outer_wall = outer_wall

    if show_partners:
        p_defs = [
            (np.array([-1.65, 2.35, 0.0]), np.array([-1.35, 1.82, 0.0]), 0.0),
            (np.array([0.0, 2.52, 0.0]), np.array([0.0, 1.98, 0.0]), 1.1),
            (np.array([1.75, 2.30, 0.0]), np.array([1.40, 1.80, 0.0]), 2.2),
        ]
        partners = VGroup()
        for p_hi, p_lo, phase0 in p_defs:
            blk = make_partner_block(color=PARTNER, width=0.92, height=0.44)
            blk.move_to(p_hi)
            if animated:
                blk._ph = phase0

                def bounce(m, dt, hi=p_hi, lo=p_lo):
                    m._ph += dt * 2.1
                    s = 0.5 * (1.0 - np.cos(m._ph))
                    m.move_to(hi * (1.0 - s) + lo * s)

                blk.add_updater(bounce)
            partners.add(blk)
        world.add(partners)
        world.partners = partners
    else:
        world.partners = VGroup()

    return world


# ------------------------------------------------------------------ Scenes
class S00Title(TitleCard):
    LESSON = "Endocytosis and Signaling Endosomes"
    TITLE = "Still Talking, Until Sealed Inside"


class S01Hook(SpokenScene):
    def construct(self):
        pm = make_plasma_membrane(y=2.55, x_span=11.6, pit_depth=0.22, pit_x=0.0)
        pm_lbl = T("Plasma membrane", size=26, color=MEMBRANE).move_to([-4.2, 3.16, 0.0]).set_z_index(20)
        endo = make_endosome(center=(0.0, -0.80, 0.0), rx=2.4, ry=1.60,
                             lumen_color=LUMEN_EARLY, lumen_opacity=0.15, with_tubule=True)
        endo_lbl = T("Early endosome (Rab5)", size=28, color=RAB5).move_to([0.0, -2.98, 0.0]).set_z_index(20)
        cyto_lbl = T("Cytosol", size=26, color=TEXT).move_to([-4.7, 0.85, 0.0]).set_z_index(20)
        tag = scope_tag("schematic", color=TEXT).set_z_index(20)

        t_path = ValueTracker(0.0)

        def ves_pos():
            u = t_path.get_value()
            x = 0.55 * (3 * u ** 2 - 2 * u ** 3)
            y = 1.30 - 0.50 * u
            return np.array([x, y, 0.0])

        def build_traveler():
            u = t_path.get_value()
            p = ves_pos()
            if u < 0.96:
                ves = Circle(radius=0.46, stroke_color=MEMBRANE, stroke_width=4.5,
                             fill_color=LUMEN_EARLY, fill_opacity=0.15).move_to(p)
                rec = make_receptor(p + np.array([0.44, 0.0, 0.0]), tail_angle=0.0,
                                    scale=0.80, active=True, ligand=True)
                return VGroup(ves, rec)
            angle_wall = 0.42 * PI
            wall_p = np.array([0.0, -0.80, 0.0]) + np.array([2.4 * np.cos(angle_wall),
                                                               1.60 * np.sin(angle_wall), 0.0])
            return make_receptor(wall_p, tail_angle=angle_wall, scale=0.90,
                                 active=True, ligand=True)

        traveler = always_redraw(build_traveler)

        def tip_now():
            u = t_path.get_value()
            if u < 0.96:
                return ves_pos() + np.array([1.12, 0.0, 0.0])
            angle_wall = 0.42 * PI
            wall_p = np.array([0.0, -0.80, 0.0]) + np.array([2.4 * np.cos(angle_wall),
                                                               1.60 * np.sin(angle_wall), 0.0])
            return wall_p + np.array([np.cos(angle_wall), np.sin(angle_wall), 0.0]) * 0.82

        def angle_now():
            return 0.0 if t_path.get_value() < 0.96 else 0.42 * PI

        ripples = make_signal_arcs(tip_now, angle=angle_now, color=RECEPTOR, max_r=0.85)

        self.play(FadeIn(pm), FadeIn(endo), FadeIn(pm_lbl), FadeIn(endo_lbl),
                  FadeIn(cyto_lbl), FadeIn(tag), run_time=0.7)
        self.add(traveler, ripples)

        self.at("internalized receptors")
        self.play(t_path.animate.set_value(0.95), run_time=1.7, rate_func=smooth)

        self.at("early endosome")
        self.play(t_path.animate.set_value(1.0), run_time=0.8, rate_func=smooth)

        self.at("tails still facing")
        tail_lbl = T("Tail in cytosol", size=28, color=RECEPTOR).move_to([3.55, 0.95, 0.0]).set_z_index(20)
        arr = Arrow(tail_lbl.get_left() + LEFT * 0.1, [1.25, 1.35, 0.0],
                    buff=0.05, color=RECEPTOR, stroke_width=3.5, max_tip_length_to_length_ratio=0.18)
        self.play(FadeIn(tail_lbl), GrowArrow(arr), run_time=0.8)

        self.at("Can an active")
        q_box = boxed_label("Still signaling?", color=GOLD, size=30, pad=0.22).move_to([4.15, 1.92, 0.0]).set_z_index(20)
        self.play(FadeIn(q_box, shift=DOWN * 0.1), run_time=0.7)

        self.at("keep signaling")
        self.wait(0.6)

        self.at("what finally shuts")
        q_off = T("What shuts it off?", size=28, color=TEXT).move_to([4.35, -0.25, 0.0]).set_z_index(20)
        self.play(FadeIn(q_off), run_time=0.7)

        self.at("Surprisingly")
        ans = boxed_label("Still active inside", color=RECEPTOR, size=30, pad=0.22).move_to([4.15, 1.92, 0.0]).set_z_index(20)
        self.play(FadeOut(q_off, run_time=0.4), swap(q_box, ans, run_time=0.7))

        self.at("silence an active")
        self.finish()


class S02TopologyPartners(SpokenScene):
    def construct(self):
        endo_full = make_endosome(center=(0.0, -0.80, 0.0), rx=2.4, ry=1.60,
                                  lumen_color=LUMEN_EARLY, lumen_opacity=0.15, with_tubule=True)
        ang = 0.44 * PI
        wall_p0 = np.array([0.0, -0.80, 0.0]) + np.array([2.4 * np.cos(ang), 1.60 * np.sin(ang), 0.0])
        rec0 = make_receptor(wall_p0, tail_angle=ang, scale=0.90, active=True, ligand=True)
        world0 = VGroup(endo_full, rec0)
        tag = scope_tag("schematic", color=TEXT).set_z_index(20)

        # Zoomed compartment shifted left (right rim at x = -2.2 + 3.15 = +0.95) so right-side labels are totally clear
        wall_c = np.array([-2.20, -1.25, 0.0])
        wall_rx, wall_ry = 3.15, 1.80
        endo_zoom = make_endosome(center=wall_c, rx=wall_rx, ry=wall_ry,
                                  lumen_color=LUMEN_EARLY, lumen_opacity=0.16, with_tubule=False,
                                  rab_angles=[0.14 * PI, 0.32 * PI, 0.68 * PI, 1.15 * PI, 1.65 * PI])
        z_ang = 0.44 * PI
        z_pos = wall_c + np.array([wall_rx * np.cos(z_ang), wall_ry * np.sin(z_ang), 0.0])
        rec_z = make_receptor(z_pos, tail_angle=z_ang, scale=1.15, active=True, ligand=True)
        world_zoom = VGroup(endo_zoom, rec_z)

        tail_tip = rec_z.tip_mob.get_center()
        halo_right = rec_z.halo_mob.get_right()

        signal_mode = ["basal"]
        ripples_basal = make_signal_arcs(lambda: tail_tip, angle=z_ang, color=RECEPTOR, max_r=1.0,
                                         active_fn=lambda: signal_mode[0] == "basal")

        self.add(world0, tag)
        self.wait(0.25)

        self.at("way the membrane")
        self.play(ReplacementTransform(world0, world_zoom), run_time=1.5, rate_func=smooth)
        self.add(ripples_basal)

        cyto_lbl = T("Cytosol", size=30, color=TEXT).move_to([4.6, 2.85, 0.0]).set_z_index(20)
        lumen_lbl = T("Endosome lumen (pH 6–6.5)", size=26, color=LUMEN_EARLY).move_to([-2.20, -1.65, 0.0]).set_z_index(20)
        self.play(FadeIn(cyto_lbl), FadeIn(lumen_lbl), run_time=0.7)

        self.at("outer endosome membrane")
        tail_lbl = T("Tail in cytosol", size=30, color=RECEPTOR).move_to([-4.35, 2.25, 0.0]).set_z_index(20)
        tail_arr = Arrow(tail_lbl.get_right() + RIGHT * 0.12, tail_tip + LEFT * 0.30,
                         buff=0.05, color=RECEPTOR, stroke_width=3.5, max_tip_length_to_length_ratio=0.18)
        self.play(FadeIn(tail_lbl), GrowArrow(tail_arr), run_time=0.7)

        p1_block = make_partner_block("Partner", color=PARTNER, size=28, width=1.65, height=0.62)
        p1_start = np.array([4.85, 1.85, 0.0])
        p1_dock = tail_tip + np.array([1.25, 0.02, 0.0])
        p1_block.move_to(p1_start).set_z_index(15)

        p2_block = make_partner_block("New partner", color=TRIF_COL, size=28, width=2.15, height=0.62)
        p2_start = np.array([4.85, 0.35, 0.0])
        p2_dock = tail_tip + np.array([1.68, 0.02, 0.0])
        p2_block.move_to(p2_start).set_z_index(15)

        ripples_1 = make_signal_arcs(lambda: p1_block.get_top() + UP * 0.08, angle=PI / 2,
                                     color=PARTNER, max_r=1.05,
                                     active_fn=lambda: signal_mode[0] == "partner1")
        ripples_2 = make_signal_arcs(lambda: p2_block.get_top() + UP * 0.08, angle=PI / 2,
                                     color=TRIF_COL, max_r=1.05,
                                     active_fn=lambda: signal_mode[0] == "partner2")
        self.add(ripples_1, ripples_2)

        self.at("tail still touches")
        self.play(FadeIn(p1_block), run_time=0.5)

        self.at("cytosolic partner")
        signal_mode[0] = "none"
        dock_arc1 = ArcBetweenPoints(p1_start, p1_dock, angle=0.32)
        self.play(MoveAlongPath(p1_block, dock_arc1), run_time=0.95, rate_func=smooth)
        dock_link1 = Line(halo_right, p1_block.get_left() + LEFT * 0.02,
                          color=PARTNER, stroke_width=4.0)
        self.play(Create(dock_link1), run_time=0.25)
        signal_mode[0] = "partner1"

        self.at("keep sending")
        same_lbl = boxed_label("Same signal continues", color=PARTNER, size=28, pad=0.2).move_to([3.85, -1.65, 0.0]).set_z_index(20)
        self.play(FadeIn(same_lbl), run_time=0.7)

        self.at("switch partners")
        signal_mode[0] = "none"
        undock_arc = ArcBetweenPoints(p1_dock, np.array([4.85, 2.2, 0.0]), angle=-0.28)
        self.play(FadeOut(dock_link1), MoveAlongPath(p1_block, undock_arc), FadeOut(p1_block),
                  FadeIn(p2_block), run_time=0.75, rate_func=smooth)
        dock_arc2 = ArcBetweenPoints(p2_start, p2_dock, angle=-0.28)
        self.play(MoveAlongPath(p2_block, dock_arc2), run_time=0.65, rate_func=smooth)
        dock_link2 = Line(halo_right, p2_block.get_left() + LEFT * 0.02,
                          color=TRIF_COL, stroke_width=4.0)
        self.play(Create(dock_link2), run_time=0.2)
        signal_mode[0] = "partner2"

        self.at("leave the plasma")
        new_lbl = boxed_label("New partner, new signal", color=TRIF_COL, size=28, pad=0.2).move_to([3.85, -1.65, 0.0]).set_z_index(20)
        self.play(swap(same_lbl, new_lbl, run_time=0.7))
        self.finish()


class S03Tlr4Switch(SpokenScene):
    def construct(self):
        pm = make_plasma_membrane(y=2.45, x_span=11.6, pit_depth=0.0)
        pm_lbl = T("Plasma membrane", size=26, color=MEMBRANE).move_to([-4.2, 3.05, 0.0]).set_z_index(20)

        endo_c = np.array([-0.6, -1.75, 0.0])
        endo = make_endosome(center=endo_c, rx=2.6, ry=1.35,
                             lumen_color=LUMEN_EARLY, lumen_opacity=0.15, with_tubule=False)
        endo_lbl = T("Rab5 early endosome", size=26, color=RAB5).move_to([-0.6, -1.95, 0.0]).set_z_index(20)
        tag = scope_tag("schematic", color=TEXT).set_z_index(20)

        tlr4_top_pos = np.array([-0.6, 2.48, 0.0])
        tlr4_end_ang = 0.5 * PI
        tlr4_end_pos = endo_c + np.array([0.0, 1.35, 0.0])

        t_move = ValueTracker(0.0)

        def build_tlr4():
            u = t_move.get_value()
            if u < 0.05:
                return make_receptor(tlr4_top_pos, tail_angle=-PI / 2, scale=0.9, active=True, ligand=True)
            elif u < 0.95:
                u_ves = (u - 0.05) / 0.90
                ves_start = np.array([-0.6, 1.15, 0.0])
                p = ves_start * (1.0 - u_ves) + (tlr4_end_pos + UP * 0.25) * u_ves
                ves = Circle(radius=0.44, stroke_color=MEMBRANE, stroke_width=4.0,
                             fill_color=LUMEN_EARLY, fill_opacity=0.14).move_to(p)
                rec = make_receptor(p + UP * 0.42, tail_angle=PI / 2, scale=0.78, active=True, ligand=True)
                return VGroup(ves, rec)
            return make_receptor(tlr4_end_pos, tail_angle=tlr4_end_ang, scale=0.92, active=True, ligand=True)

        tlr4 = always_redraw(build_tlr4)
        tlr4_lbl = T("TLR4", size=28, color=RECEPTOR).move_to([-1.95, 2.15, 0.0]).set_z_index(20)

        myd88 = make_partner_block("MyD88", color=PARTNER, size=26, width=1.45, height=0.56)
        myd88_start = np.array([-4.4, 1.30, 0.0])
        myd88_dock = np.array([-1.55, 1.50, 0.0])
        myd88.move_to(myd88_start).set_z_index(15)

        trif = make_partner_block("TRIF", color=TRIF_COL, size=26, width=1.35, height=0.56)
        trif_start = np.array([3.6, 0.25, 0.0])
        trif_dock = np.array([0.48, 0.48, 0.0])
        trif.move_to(trif_start).set_z_index(15)

        ifn_box = boxed_label("Interferon genes", color=TRIF_COL, size=28, pad=0.22).move_to([4.25, 1.65, 0.0]).set_z_index(20)

        sig_mode = ["surface"]
        sig_surf = make_signal_arcs(lambda: tlr4_top_pos + DOWN * 0.85, angle=-PI / 2,
                                    color=RECEPTOR, max_r=1.30, active_fn=lambda: sig_mode[0] == "surface")
        sig_myd88 = make_signal_arcs(lambda: myd88.get_bottom() + DOWN * 0.06, angle=-PI / 2,
                                     color=PARTNER, max_r=1.30, active_fn=lambda: sig_mode[0] == "myd88")
        sig_trif = make_signal_arcs(lambda: trif.get_right() + RIGHT * 0.06, angle=0.22 * PI,
                                    color=TRIF_COL, max_r=0.78, active_fn=lambda: sig_mode[0] == "trif")

        self.play(FadeIn(pm), FadeIn(pm_lbl), FadeIn(endo), FadeIn(endo_lbl),
                  FadeIn(tlr4_lbl), FadeIn(tag), run_time=0.5)
        self.add(tlr4, sig_surf, sig_myd88, sig_trif)

        self.at("receptor 4")
        self.play(Indicate(tlr4_lbl, color=RECEPTOR, scale_factor=1.12), run_time=0.6)
        self.play(tlr4_lbl.animate.shift(LEFT * 0.15), run_time=1.0, rate_func=there_and_back)

        self.at("At the plasma")
        self.play(FadeIn(myd88), run_time=0.6)

        self.at("it binds a cytosolic")
        sig_mode[0] = "none"
        self.play(myd88.animate.move_to(myd88_dock), run_time=1.0, rate_func=smooth)

        self.at("my D88")
        sig_mode[0] = "myd88"
        self.play(Indicate(myd88, color=PARTNER, scale_factor=1.06), run_time=0.9)

        self.at("After endocytosis")
        sig_mode[0] = "none"
        self.play(FadeOut(myd88), run_time=0.35)
        self.play(tlr4_lbl.animate.move_to([-2.15, 0.25, 0.0]),
                  t_move.animate.set_value(0.92), run_time=0.9, rate_func=smooth)

        self.at("into an endosome")
        self.play(t_move.animate.set_value(1.0), run_time=0.6, rate_func=smooth)

        self.at("second adapter")
        self.play(FadeIn(trif), FadeIn(ifn_box), run_time=0.6)

        self.at("TRIF")
        self.play(trif.animate.move_to(trif_dock), run_time=0.65, rate_func=smooth)

        self.at("switches on interferon")
        sig_mode[0] = "trif"
        ifn_on = boxed_label("Interferon genes: ON", color=TRIF_COL, size=28, pad=0.22,
                             fill_opacity=0.35).move_to([4.25, 1.65, 0.0]).set_z_index(20)
        self.play(swap(ifn_box, ifn_on, run_time=0.65))
        self.finish()


class S04UbiquitinEscrt(SpokenScene):
    def construct(self):
        endo_c = np.array([0.3, -0.55, 0.0])
        rx, ry = 2.6, 1.85
        endo = make_endosome(center=endo_c, rx=rx, ry=ry,
                             lumen_color=LUMEN_EARLY, lumen_opacity=0.15, with_tubule=True,
                             rab_angles=[0.05 * PI, 0.35 * PI, 0.68 * PI, 1.18 * PI, 1.45 * PI, 1.75 * PI])
        tub_lbl = T("Recycling tubule", size=26, color=TUBULE).move_to([-4.45, 1.20, 0.0]).set_z_index(20)
        endo_lbl = T("Early endosome (Rab5)", size=28, color=RAB5).move_to([0.3, -2.98, 0.0]).set_z_index(20)
        tag = scope_tag("schematic", color=TEXT).set_z_index(20)

        gather = ValueTracker(0.0)
        ub_on = [0]
        escrt_on = [False]
        sig_active = [True]

        start_angs = np.array([0.82 * PI, 0.50 * PI, 0.18 * PI])
        patch_angs = np.array([0.58 * PI, 0.50 * PI, 0.42 * PI])
        tub_wall_pos = np.array([-2.85, 0.36, 0.0])

        def build_cargo():
            u = gather.get_value()
            if u < 0.0:
                angs = start_angs.copy()
            else:
                angs = start_angs * (1.0 - u) + patch_angs * u
            grp = VGroup()
            for idx, a in enumerate(angs):
                p = endo_c + np.array([rx * np.cos(a), ry * np.sin(a), 0.0])
                t_ang = a
                if u < 0.0 and idx == 0:
                    s = -u
                    p = p * (1.0 - s) + tub_wall_pos * s
                    t_ang = a * (1.0 - s) + (PI / 2) * s
                n_ub = 2 if ub_on[0] > idx else 0
                rec = make_receptor(p, tail_angle=t_ang, scale=0.86, active=True, ligand=True, ub_count=n_ub)
                grp.add(rec)
                if escrt_on[0]:
                    clamp = make_escrt_clamp(scale=0.9)
                    clamp_pos = p + np.array([np.cos(t_ang), np.sin(t_ang), 0.0]) * 0.52
                    clamp.rotate(t_ang + PI / 2).move_to(clamp_pos)
                    grp.add(clamp)
            return grp

        cargo = always_redraw(build_cargo)

        def top_tip():
            u = max(0.0, gather.get_value())
            a = start_angs[1] * (1.0 - u) + patch_angs[1] * u
            p = endo_c + np.array([rx * np.cos(a), ry * np.sin(a), 0.0])
            return p + np.array([np.cos(a), np.sin(a), 0.0]) * 0.80

        ripples_mid = make_signal_arcs(top_tip, angle=PI / 2, color=RECEPTOR, max_r=1.0,
                                       active_fn=lambda: sig_active[0])

        self.play(FadeIn(endo), FadeIn(tub_lbl), FadeIn(endo_lbl), FadeIn(tag), run_time=0.6)
        self.add(cargo, ripples_mid)

        # Continuous biological sequence: drift toward tubule -> ubiquitin beads fly in -> ESCRT binds -> gather
        self.play(gather.animate.set_value(-1.0), run_time=2.4, rate_func=smooth)
        self.at("leaves the recycling")
        self.play(gather.animate.set_value(0.0), run_time=1.8, rate_func=smooth)

        self.at("attaches a small")
        ub_lbl = T("Ubiquitin", size=28, color=UBIQUITIN).move_to([4.55, 2.25, 0.0]).set_z_index(20)
        self.play(FadeIn(ub_lbl), run_time=0.35)
        for idx, ang_i in enumerate((0.82 * PI, 0.50 * PI, 0.18 * PI)):
            target_p = endo_c + np.array([rx * np.cos(ang_i), ry * np.sin(ang_i), 0.0]) + np.array([np.cos(ang_i), np.sin(ang_i), 0.0]) * 0.52
            bead = Dot([4.1, 1.85, 0.0], radius=0.14, color=UBIQUITIN)
            self.play(bead.animate.move_to(target_p), run_time=0.45, rate_func=smooth)
            self.remove(bead)
            ub_on[0] = idx + 1

        self.at("ubiquitin")
        self.wait(0.3)

        self.at("protein complex")
        escrt_lbl = T("ESCRT", size=28, color=ESCRT).move_to([-4.05, 2.55, 0.0]).set_z_index(20)
        self.play(FadeIn(escrt_lbl), run_time=0.55)
        clamps_fly = VGroup(*[make_escrt_clamp(0.85).move_to([-2.4 + 0.9 * k, 2.8, 0.0]) for k in range(3)])
        targets_c = [
            endo_c + np.array([rx * np.cos(a), ry * np.sin(a), 0.0]) + np.array([np.cos(a), np.sin(a), 0.0]) * 0.52
            for a in start_angs
        ]
        self.play(FadeIn(clamps_fly), run_time=0.3)
        self.play(*[clamps_fly[k].animate.move_to(targets_c[k]) for k in range(3)], run_time=1.0, rate_func=smooth)
        self.remove(clamps_fly)
        escrt_on[0] = True
        sig_active[0] = False

        self.at("reads ubiquitin")
        arr_e = Arrow(escrt_lbl.get_right() + RIGHT * 0.1, [0.05, 2.05, 0.0],
                      buff=0.05, color=ESCRT, stroke_width=3.5, max_tip_length_to_length_ratio=0.18)
        self.play(GrowArrow(arr_e), run_time=0.55)

        self.at("gathers tagged receptors")
        patch_lbl = boxed_label("Gathered patch", color=ESCRT, size=28, pad=0.2).move_to([4.25, 1.35, 0.0]).set_z_index(20)
        self.play(
            gather.animate(run_time=1.4, rate_func=smooth).set_value(1.0),
            Succession(Wait(1.0), FadeIn(patch_lbl, run_time=0.4)),
        )
        self.finish()


class S05InwardBud(SpokenScene):
    def construct(self):
        endo_c = np.array([1.05, -0.60, 0.0])
        rx, ry = 2.65, 1.92
        bud_r = 0.65
        depth = ValueTracker(0.0)
        pit_depth = ValueTracker(0.0)

        rabs = make_rab_badges(endo_c, rx, ry,
                               [0.10 * PI, 0.28 * PI, 0.72 * PI, 1.15 * PI, 1.48 * PI, 1.82 * PI],
                               color=RAB5)
        endo_lbl = T("Early endosome", size=28, color=RAB5).move_to([1.05, -3.08, 0.0]).set_z_index(20)
        tag = scope_tag("schematic", color=TEXT).set_z_index(20)

        def build_mve():
            d = depth.get_value()
            grp = VGroup()
            if d < 0.96:
                pts, b_cen, bud_bottom = make_budding_endosome_curve(endo_c, rx, ry, d, bud_theta=PI / 2, bud_r=bud_r)
                wall = VMobject(stroke_color=MEMBRANE, stroke_width=5.5,
                                fill_color=LUMEN_EARLY, fill_opacity=0.15)
                wall.set_points_as_corners(np.vstack([pts, pts[:1]]))
                grp.add(wall)
                rec_pos = np.array([b_cen[0], bud_bottom[1], 0.0])
                rec = make_receptor(rec_pos, tail_angle=PI / 2, scale=0.80, active=True, ligand=True, ub_count=2)
                grp.add(rec)
                neck_y = endo_c[1] + ry + 0.15 - 0.15 * d
                c_l = make_escrt_clamp(0.85).rotate(0.1 * PI).move_to([b_cen[0] - 0.50, neck_y, 0.0])
                c_r = make_escrt_clamp(0.85).rotate(0.9 * PI).move_to([b_cen[0] + 0.50, neck_y, 0.0])
                grp.add(c_l, c_r)
            else:
                t_pinch = np.clip((d - 0.96) / 0.04, 0.0, 1.0)
                outer = Ellipse(width=2 * rx, height=2 * ry, stroke_color=MEMBRANE, stroke_width=5.5,
                                fill_color=LUMEN_EARLY, fill_opacity=0.15).move_to(endo_c)
                _, b_cen_096, _ = make_budding_endosome_curve(endo_c, rx, ry, 0.96, bud_theta=PI / 2, bud_r=bud_r)
                ilv_target = endo_c + np.array([0.0, 0.35, 0.0])
                ilv_pos = b_cen_096 * (1.0 - t_pinch) + ilv_target * t_pinch
                ilv = Circle(radius=bud_r, stroke_color=MEMBRANE, stroke_width=4.5,
                             fill_color=BG, fill_opacity=0.85).move_to(ilv_pos)
                rec = make_receptor(ilv_pos + np.array([0.0, -bud_r, 0.0]), tail_angle=PI / 2,
                                    scale=0.80, active=True, ligand=True, ub_count=2)
                neck_y = endo_c[1] + ry + 0.15 - 0.15 * d
                clamp_op = max(0.0, 1.0 - t_pinch)
                c_l = make_escrt_clamp(0.85).rotate(0.1 * PI).move_to([ilv_pos[0] - 0.50, neck_y, 0.0])
                c_r = make_escrt_clamp(0.85).rotate(0.9 * PI).move_to([ilv_pos[0] + 0.50, neck_y, 0.0])
                for cl in (c_l, c_r):
                    cl[0].set_stroke(opacity=clamp_op)
                    cl[1].set_fill(opacity=clamp_op)
                    cl[2].set_fill(opacity=clamp_op)
                grp.add(outer, ilv, rec, c_l, c_r)
            return grp

        mve_dyn = always_redraw(build_mve)
        self.add(rabs, mve_dyn, endo_lbl, tag)

        pit_box = RoundedRectangle(corner_radius=0.16, width=3.85, height=2.65,
                                   stroke_color=MEMBRANE, stroke_width=2.2,
                                   fill_color=BG, fill_opacity=0.92).move_to([-4.15, 1.75, 0.0])
        pit_title = T("Coated pit", size=26, color=MEMBRANE).move_to([-4.15, 2.78, 0.0]).set_z_index(20)
        pit_note = T("Into cytosol", size=24, color=PARTNER).move_to([-3.25, 0.95, 0.0]).set_z_index(20)

        def build_pit_dyn():
            pd = pit_depth.get_value()
            xs = np.linspace(-1.55, 1.55, 80)
            ys = -0.10 - pd * 0.72 * np.exp(-(xs / 0.45) ** 2)
            curve = VMobject(stroke_color=MEMBRANE, stroke_width=4.0).set_points_as_corners(
                [np.array([-4.45 + x, 2.25 + y, 0.0]) for x, y in zip(xs, ys)]
            )
            rec_y = 2.15 - pd * 0.72
            rec = make_receptor([-4.45, rec_y - 0.12, 0.0], tail_angle=-PI / 2, scale=0.56,
                                active=True, ligand=True)
            arr = Arrow([-4.45, 2.48, 0.0], [-4.45, 2.15 - pd * 0.35, 0.0],
                        buff=0.04, color=PARTNER, stroke_width=3.8)
            return VGroup(curve, rec, arr)

        pit_dyn = always_redraw(build_pit_dyn)

        self.at("bends the membrane")
        self.play(FadeIn(pit_box), FadeIn(pit_title), run_time=0.6)
        self.add(pit_dyn)

        self.at("Coated pits pulled")
        self.play(pit_depth.animate.set_value(0.95), run_time=2.5, rate_func=smooth)

        self.at("tails exposed")
        self.play(FadeIn(pit_note), run_time=0.7)
        self.play(Indicate(pit_note, color=PARTNER, scale_factor=1.08), run_time=0.8)

        self.at("pushes the tagged")
        bud_arr = Arrow([1.05, 2.95, 0.0], [1.05, 2.30, 0.0], buff=0.05, color=ESCRT, stroke_width=5.5)
        bud_lbl = T("Inward bud", size=28, color=ESCRT).move_to([2.65, 2.25, 0.0]).set_z_index(20)
        self.play(FadeIn(bud_lbl), GrowArrow(bud_arr), run_time=0.8)
        self.play(depth.animate.set_value(0.18), run_time=1.4, rate_func=smooth)

        self.at("inward into")
        self.play(depth.animate.set_value(0.88), run_time=2.6, rate_func=smooth)

        self.at("pinches off")
        self.play(depth.animate.set_value(1.0), FadeOut(bud_arr), FadeOut(bud_lbl), run_time=1.2, rate_func=smooth)

        self.at("multivesicular endosome")
        mve_lbl = T("Multivesicular endosome", size=28, color=RAB5).move_to([1.05, -3.08, 0.0]).set_z_index(20)
        self.play(swap(endo_lbl, mve_lbl, run_time=0.8))
        self.finish()


class S06Predict(SpokenScene):
    def construct(self):
        world = make_s06_backdrop(animated=True, show_partners=True)
        tag = scope_tag("schematic", color=TEXT).move_to([5.45, 3.30, 0.0]).set_z_index(20)
        self.add(world, tag)

        self.at("tail faces now")
        tail_lbl = fit_text("Tail inside\nvesicle", max_w=2.4, size=28, color=RECEPTOR).move_to([-4.90, 0.15, 0.0]).set_z_index(20)
        tail_arr = Arrow(tail_lbl.get_right() + RIGHT * 0.1, [-0.14, 0.05, 0.0],
                         buff=0.05, color=RECEPTOR, stroke_width=3.5, max_tip_length_to_length_ratio=0.14)
        self.play(FadeIn(tail_lbl), GrowArrow(tail_arr), run_time=0.7)

        self.at("sealed inside")
        two_lbl = fit_text("Two membranes\nseparate them", max_w=2.5, size=26, color=MEMBRANE).move_to([4.85, 0.15, 0.0]).set_z_index(20)
        self.play(FadeIn(two_lbl), run_time=0.7)

        self.at("before any lysosome")
        part_lbl = T("Cytosolic partners", size=26, color=PARTNER).move_to([-4.35, 2.35, 0.0]).set_z_index(20)
        self.play(FadeIn(part_lbl), run_time=0.6)

        self.at("Does its signal")
        q = question_card("Signal stops now, or only in the lysosome?", y=BOTTOM_Y + 0.15)
        self.play(FadeIn(q.question, shift=UP * 0.1), run_time=0.8)

        self.at("only after digestive")
        self.finish()


class S07Pause(PredictPause):
    QUESTION = "Signal stops now, or only in the lysosome?"
    SECONDS = 4.5

    def backdrop(self):
        world = make_s06_backdrop(animated=True, show_partners=True)
        tail_lbl = fit_text("Tail inside\nvesicle", max_w=2.4, size=28, color=RECEPTOR).move_to([-4.90, 0.15, 0.0]).set_z_index(20)
        tail_arr = Arrow(tail_lbl.get_right() + RIGHT * 0.1, [-0.14, 0.05, 0.0],
                         buff=0.05, color=RECEPTOR, stroke_width=3.5, max_tip_length_to_length_ratio=0.14)
        two_lbl = fit_text("Two membranes\nseparate them", max_w=2.5, size=26, color=MEMBRANE).move_to([4.85, 0.15, 0.0]).set_z_index(20)
        part_lbl = T("Cytosolic partners", size=26, color=PARTNER).move_to([-4.35, 2.35, 0.0]).set_z_index(20)
        tag = scope_tag("schematic", color=TEXT).move_to([5.45, 3.30, 0.0]).set_z_index(20)
        return VGroup(world, tail_lbl, tail_arr, two_lbl, part_lbl, tag)


class S08SealedReveal(SpokenScene):
    def construct(self):
        world = make_s06_backdrop(animated=False, show_partners=True)
        q = question_card("Signal stops now, or only in the lysosome?", y=BOTTOM_Y + 0.15)
        tail_lbl = fit_text("Tail inside\nvesicle", max_w=2.4, size=28, color=RECEPTOR).move_to([-4.90, 0.15, 0.0]).set_z_index(20)
        tail_arr = Arrow(tail_lbl.get_right() + RIGHT * 0.1, [-0.14, 0.05, 0.0],
                         buff=0.05, color=RECEPTOR, stroke_width=3.5, max_tip_length_to_length_ratio=0.14)
        part_lbl = T("Cytosolic partners", size=26, color=PARTNER).move_to([-4.35, 2.35, 0.0]).set_z_index(20)
        tag = scope_tag("schematic", color=TEXT).move_to([5.45, 3.30, 0.0]).set_z_index(20)
        self.add(world, q, tail_lbl, tail_arr, part_lbl, tag)

        self.at("stops right now")
        rec_dim = make_receptor(world.rec.get_center(), tail_angle=-PI / 2, scale=0.72, active=False, ligand=True)
        sealed_lbl = boxed_label("Tail sealed off", color=TEXT, size=26, pad=0.18).move_to([-4.95, 0.15, 0.0]).set_z_index(20)
        # Shorten arrow so it starts cleanly outside sealed_lbl's right edge
        new_arr = Arrow(sealed_lbl.get_right() + RIGHT * 0.12, [-0.14, 0.05, 0.0],
                        buff=0.05, color=TEXT, stroke_width=3.5, max_tip_length_to_length_ratio=0.14)
        self.play(FadeOut(q), Transform(world.rec, rec_dim), swap(tail_lbl, sealed_lbl, run_time=0.8),
                  Transform(tail_arr, new_arr), run_time=0.8)

        self.at("encloses the cytoplasmic")
        seal_ring = Circle(radius=0.98, stroke_color=TEXT, stroke_width=3.5, stroke_opacity=0.85).move_to(world.ilv_ring.get_center())
        self.play(Create(seal_ring), run_time=0.8)
        self.play(FadeOut(seal_ring), run_time=0.4)

        self.at("Cytosolic partners")
        self.play(world.partners.animate.shift(UP * 1.4).set_opacity(0.0), FadeOut(part_lbl),
                  run_time=1.3, rate_func=smooth)
        self.remove(world.partners)

        self.at("signaling ends")
        self.play(FadeOut(tail_arr), FadeOut(sealed_lbl),
                  world.animate.scale(0.84).move_to([0.0, 0.30, 0.0]), run_time=1.5, rate_func=smooth)

        c_full = world.outer_wall.get_center()
        ilv2_start = c_full + np.array([-1.55, 0.72, 0.0])
        ilv2_end = c_full + np.array([-1.32, 0.02, 0.0])
        ilv3_start = c_full + np.array([1.55, 0.72, 0.0])
        ilv3_end = c_full + np.array([1.32, 0.02, 0.0])

        def make_small_ilv(pos):
            r = 0.56
            ring = Circle(radius=r, stroke_color=MEMBRANE, stroke_width=4.0,
                          fill_color=BG, fill_opacity=0.85).move_to(pos)
            rc = make_receptor(pos + np.array([0.0, r, 0.0]), tail_angle=-PI / 2,
                               scale=0.52, active=False, ligand=True)
            return VGroup(ring, rc)

        ilv2 = make_small_ilv(ilv2_start).scale(0.28)
        ilv3 = make_small_ilv(ilv3_start).scale(0.28)
        mve_lbl = T("Multivesicular endosome", size=30, color=RAB5).move_to([0.0, -2.65, 0.0]).set_z_index(20)
        self.play(FadeIn(ilv2), FadeIn(ilv3), FadeIn(mve_lbl), run_time=0.6)

        self.at("places the whole")
        self.play(ilv2.animate.scale(1.0 / 0.28).move_to(ilv2_end),
                  ilv3.animate.scale(1.0 / 0.28).move_to(ilv3_end),
                  run_time=2.3, rate_func=smooth)
        self.finish()


class S09RabConversionAcid(SpokenScene):
    def construct(self):
        endo_c = np.array([-3.15, 0.35, 0.0])
        rx, ry = 2.40, 1.65
        pH_tracker = ValueTracker(6.5)

        def lumen_col():
            p = pH_tracker.get_value()
            if p >= 5.5:
                t = np.clip((6.5 - p) / 1.0, 0.0, 1.0)
                return interpolate_color(ManimColor(LUMEN_EARLY), ManimColor(LUMEN_LATE), t)
            t = np.clip((5.5 - p) / 0.6, 0.0, 1.0)
            return interpolate_color(ManimColor(LUMEN_LATE), ManimColor(LYSO), t)

        def build_endo_body():
            p = pH_tracker.get_value()
            op = 0.16 + 0.18 * np.clip((6.5 - p) / 1.5, 0.0, 1.0)
            return Ellipse(width=2 * rx, height=2 * ry, stroke_color=MEMBRANE, stroke_width=5.5,
                           fill_color=lumen_col(), fill_opacity=op).move_to(endo_c)

        endo_body = always_redraw(build_endo_body)

        ilv_offsets = [np.array([-1.05, 0.05, 0.0]), np.array([0.0, 0.42, 0.0]), np.array([1.05, -0.05, 0.0])]
        ilvs = VGroup()
        for off in ilv_offsets:
            p = endo_c + off
            ring = Circle(radius=0.48, stroke_color=MEMBRANE, stroke_width=3.8,
                          fill_color=BG, fill_opacity=0.85).move_to(p)
            rc = make_receptor(p + np.array([0.0, 0.48, 0.0]), tail_angle=-PI / 2,
                               scale=0.46, active=False, ligand=True)
            ilvs.add(VGroup(ring, rc))

        rab5_angs = [0.15 * PI, 0.40 * PI, 0.68 * PI, 1.15 * PI, 1.48 * PI, 1.82 * PI]
        rab5_badges = make_rab_badges(endo_c, rx, ry, rab5_angs, color=RAB5)
        rab7_angs = [0.22 * PI, 0.52 * PI, 0.82 * PI, 1.25 * PI, 1.60 * PI, 1.92 * PI]
        rab7_badges = make_rab_badges(endo_c, rx, ry, rab7_angs, color=RAB7)

        comp_lbl = T("Rab5 early endosome", size=28, color=RAB5).move_to([-3.15, 2.72, 0.0]).set_z_index(20)
        tag = scope_tag("schematic", color=TEXT).set_z_index(20)

        P = Plot(box=(1.1, 5.9, -1.60, 2.0), xr=(0.0, 2.2), yr=(0.0, 110.0),
                 xticks=[(0.0, "pH 7"), (1.0, "pH 6"), (2.0, "pH 5")],
                 yticks=[(25.0, "25×"), (50.0, "50×"), (100.0, "100×")],
                 xlabel="", ylabel="Relative [H⁺]", color=TEXT, size=24, label_size=26)
        rule_lbl = T("1 pH unit down = 10× H⁺", size=28, color=UBIQUITIN).move_to([3.45, 2.95, 0.0]).set_z_index(20)

        dp_tracker = ValueTracker(0.0)
        live_curve = P.live_curve(lambda d: 10.0 ** d, dp_tracker, color=LUMEN_LATE, width=5)
        live_dot = P.dot(lambda: dp_tracker.get_value(), lambda: 10.0 ** dp_tracker.get_value(),
                         color=TEXT, ring=LYSO, radius=0.11)
        ro = Readout([("pH", lambda: 7.0 - dp_tracker.get_value(), "{:4.1f}", TEXT),
                      ("H⁺", lambda: 10.0 ** dp_tracker.get_value(), "{:4.0f}×", LUMEN_LATE)],
                     at=[2.75, 1.35, 0.0], size=24, widest=[7.0, 100], color=MEMBRANE).set_z_index(20)

        lyso_c = np.array([-3.15, -2.05, 0.0])
        lyso_circle = Circle(radius=0.68, stroke_color=LYSO, stroke_width=4.8,
                             fill_color=LYSO, fill_opacity=0.25).move_to(lyso_c)
        rng = np.random.default_rng(7)
        enzymes = VGroup()
        for _ in range(5):
            ang_e = rng.uniform(0, TAU)
            rad_e = rng.uniform(0.12, 0.40)
            ez = make_enzyme_wedge(color=LYSO, scale=0.17).rotate(rng.uniform(0, TAU))
            ez.move_to(lyso_c + np.array([rad_e * np.cos(ang_e), rad_e * np.sin(ang_e), 0.0]))
            enzymes.add(ez)
        lyso_lbl = T("Lysosome (pH 4.5–5)", size=26, color=LYSO).move_to([-3.15, -3.08, 0.0]).set_z_index(20)
        lyso = VGroup(lyso_circle, enzymes)

        self.play(FadeIn(endo_body), FadeIn(ilvs), FadeIn(rab5_badges), FadeIn(comp_lbl), FadeIn(tag), run_time=0.7)

        self.at("cyan RAB 5")
        self.play(rab5_badges.animate.scale(1.18).set_opacity(0.0), run_time=1.0, rate_func=smooth)
        self.remove(rab5_badges)

        self.at("purple RAB 7")
        self.play(FadeIn(rab7_badges), run_time=0.9)

        self.at("RAB conversion")
        rab7_lbl = T("Rab7 late endosome", size=28, color=RAB7).move_to([-3.15, 2.72, 0.0]).set_z_index(20)
        self.play(swap(comp_lbl, rab7_lbl, run_time=0.75))

        self.at("grows more acid")
        tick_55 = T("late endosome ~5.5", size=24, color=LUMEN_LATE).move_to([4.15, -2.85, 0.0]).set_z_index(20)
        arr_55 = Arrow(tick_55.get_top() + UP * 0.05, P.pt(1.5, 0.0), buff=0.04,
                       color=LUMEN_LATE, stroke_width=3.2, max_tip_length_to_length_ratio=0.18)
        self.play(pH_tracker.animate.set_value(5.5), run_time=1.0, rate_func=smooth)

        self.at("fuses with a lysosome")
        self.play(FadeIn(lyso), FadeIn(lyso_lbl), run_time=0.5)
        self.play(lyso.animate.move_to(endo_c),
                  pH_tracker.animate.set_value(4.9), run_time=1.0, rate_func=smooth)
        endolyso_lbl = T("Endolysosome (pH ~5)", size=28, color=LYSO).move_to([-3.15, 2.72, 0.0]).set_z_index(20)
        self.play(FadeOut(lyso_circle), FadeOut(lyso_lbl),
                  swap(rab7_lbl, endolyso_lbl, run_time=1.2),
                  enzymes.animate.scale(1.3),
                  ilvs.animate.scale(0.18).set_opacity(0.0), run_time=1.2, rate_func=smooth)
        self.remove(ilvs, lyso_circle, lyso_lbl)
        enzymes.add_updater(lambda m, dt: m.rotate(0.75 * dt))

        self.at("Each pH unit")
        self.play(Create(P), FadeIn(rule_lbl), FadeIn(ro), run_time=1.0)
        self.add(live_curve, live_dot)

        self.at("7 to 6")
        self.play(dp_tracker.animate.set_value(1.0), run_time=1.0, rate_func=smooth)
        lbl_10 = T("pH 6 → 10×", size=24, color=LUMEN_EARLY).move_to(P.pt(1.0, 10.0) + UP * 0.65 + LEFT * 0.15).set_z_index(20)
        dot_10 = Dot(P.pt(1.0, 10.0), radius=0.08, color=LUMEN_EARLY)
        self.play(FadeIn(dot_10), FadeIn(lbl_10), run_time=0.45)

        self.at("7 to 5", lead=0.3)
        self.play(dp_tracker.animate.set_value(2.0), FadeIn(tick_55), GrowArrow(arr_55),
                  run_time=0.65, rate_func=smooth)
        lbl_100 = T("pH 5 → 100×", size=24, color=LYSO).move_to([5.05, 2.22, 0.0]).set_z_index(20)
        dot_100 = Dot(P.pt(2.0, 100.0), radius=0.09, color=LYSO)
        self.play(FadeIn(dot_100), FadeIn(lbl_100), run_time=0.35)
        self.finish()


class S10MetEscape(SpokenScene):
    def construct(self):
        endo_c = np.array([-0.5, -0.65, 0.0])
        rx, ry = 2.65, 1.85
        endo = make_endosome(center=endo_c, rx=rx, ry=ry,
                             lumen_color=LUMEN_EARLY, lumen_opacity=0.15, with_tubule=True)
        endo_lbl = T("Early endosome (Rab5)", size=28, color=RAB5).move_to([-0.5, -3.05, 0.0]).set_z_index(20)
        tag = scope_tag("schematic", color=TEXT).set_z_index(20)

        met_ang = 0.42 * PI
        met_pos = endo_c + np.array([rx * np.cos(met_ang), ry * np.sin(met_ang), 0.0])
        met_normal = make_receptor(met_pos, tail_angle=met_ang, scale=0.98, active=True, ligand=True, notched=False)
        met_mutant = make_receptor(met_pos, tail_angle=met_ang, scale=0.98, active=True, ligand=True, notched=True)
        met_lbl = T("MET", size=30, color=RECEPTOR).move_to([-3.75, 2.35, 0.0]).set_z_index(20)
        met_arr = Arrow(met_lbl.get_right() + RIGHT * 0.1, met_pos + np.array([-0.15, 0.65, 0.0]),
                        buff=0.05, color=RECEPTOR, stroke_width=3.5, max_tip_length_to_length_ratio=0.18)

        ripples = make_signal_arcs(lambda: met_pos + np.array([np.cos(met_ang), np.sin(met_ang), 0.0]) * 0.90,
                                   angle=met_ang, color=RECEPTOR, max_r=1.30)

        self.at("Break that sorting")
        self.play(FadeIn(endo), FadeIn(endo_lbl), FadeIn(met_normal), FadeIn(met_lbl),
                  GrowArrow(met_arr), FadeIn(tag), run_time=0.8)
        self.add(ripples)
        self.play(Indicate(met_normal, color=RECEPTOR, scale_factor=1.06), run_time=2.5)

        self.at("receptor MET")
        self.play(Indicate(met_lbl, color=RECEPTOR, scale_factor=1.1), run_time=0.65)

        self.at("loses a short")
        met_mut_lbl = T("MET (mutant)", size=30, color=RECEPTOR).move_to([-3.75, 2.35, 0.0]).set_z_index(20)
        new_met_arr = Arrow(met_mut_lbl.get_right() + RIGHT * 0.1, met_pos + np.array([-0.15, 0.65, 0.0]),
                            buff=0.05, color=RECEPTOR, stroke_width=3.5, max_tip_length_to_length_ratio=0.18)
        self.play(Transform(met_normal, met_mutant, run_time=0.85),
                  swap(met_lbl, met_mut_lbl, run_time=0.85),
                  Transform(met_arr, new_met_arr, run_time=0.35))

        self.at("docking site")
        gap_lbl = boxed_label("No ligase docking site", color=UBIQUITIN, size=26, pad=0.18).move_to([3.85, 2.35, 0.0]).set_z_index(20)
        gap_arr = Arrow(gap_lbl.get_left() + LEFT * 0.1, met_mutant.gap_mob.get_center() + RIGHT * 0.06,
                        buff=0.05, color=UBIQUITIN, stroke_width=3.5, max_tip_length_to_length_ratio=0.18)
        self.play(FadeIn(gap_lbl), GrowArrow(gap_arr), run_time=0.7)

        ub_note = T("Ubiquitin fails to bind", size=24, color=UBIQUITIN).move_to([4.15, 0.95, 0.0]).set_z_index(20)
        self.play(FadeIn(ub_note), run_time=0.4)
        for k in range(2):
            ub_beads = VGroup(*[
                Dot([3.4 + 0.30 * j, 1.25 + 0.14 * j, 0.0], radius=0.11, color=UBIQUITIN)
                for j in range(3)
            ])
            self.play(ub_beads.animate.shift(LEFT * 2.0), run_time=0.65, rate_func=smooth)
            self.play(ub_beads.animate.shift(UP * 0.7 + RIGHT * 1.1).set_opacity(0.0), run_time=0.45)
            self.remove(ub_beads)

        self.at("Left poorly tagged")
        self.play(FadeOut(ub_note), run_time=0.4)

        self.at("slips past escort")
        c1 = make_escrt_clamp(0.92).move_to([2.6, 1.50, 0.0])
        c2 = make_escrt_clamp(0.92).move_to([3.0, 1.18, 0.0])
        esc_lbl = T("ESCRT passes by", size=26, color=ESCRT).move_to([4.35, 0.15, 0.0]).set_z_index(20)
        self.play(FadeIn(c1), FadeIn(c2), FadeIn(esc_lbl), run_time=0.3)
        self.play(c1.animate.move_to([-2.5, 1.50, 0.0]), c2.animate.move_to([-2.9, 1.18, 0.0]),
                  run_time=0.85, rate_func=linear)
        self.play(FadeOut(c1), FadeOut(c2), run_time=0.25)

        self.at("keeps signaling")
        cont_lbl = boxed_label("Signal runs too long", color=RECEPTOR, size=28, pad=0.2).move_to([4.05, -1.65, 0.0]).set_z_index(20)
        self.play(FadeIn(cont_lbl), run_time=0.6)
        self.finish()


class S11Close(SpokenScene):
    def construct(self):
        endo_c = np.array([0.0, -0.45, 0.0])
        rx, ry = 2.85, 1.88
        endo = make_endosome(center=endo_c, rx=rx, ry=ry,
                             lumen_color=LUMEN_EARLY, lumen_opacity=0.16, with_tubule=False,
                             rab_angles=[0.15 * PI, 0.35 * PI, 0.68 * PI, 1.32 * PI, 1.48 * PI, 1.75 * PI])
        tag = scope_tag("schematic", color=TEXT).set_z_index(20)

        ang_l = 0.62 * PI
        pos_l = endo_c + np.array([rx * np.cos(ang_l), ry * np.sin(ang_l), 0.0])
        rec_l = make_receptor(pos_l, tail_angle=ang_l, scale=0.92, active=True, ligand=True)
        ripples_l = make_signal_arcs(lambda: pos_l + np.array([np.cos(ang_l), np.sin(ang_l), 0.0]) * 0.85,
                                     angle=ang_l, color=RECEPTOR, max_r=1.05)
        lbl_l = boxed_label("Active on outer wall", color=RECEPTOR, size=28, pad=0.2).move_to([-4.25, 2.75, 0.0]).set_z_index(20)

        ang_m = 1.18 * PI
        pos_m = endo_c + np.array([rx * np.cos(ang_m), ry * np.sin(ang_m), 0.0])
        rec_m_on = make_receptor(pos_m, tail_angle=ang_m, scale=0.80, active=True, ligand=True)
        rec_m_off = make_receptor(pos_m, tail_angle=ang_m, scale=0.80, active=False, ligand=False)
        freed_lig = Dot(pos_m + np.array([np.cos(ang_m), np.sin(ang_m), 0.0]) * -0.35,
                        radius=0.10, color=LIGAND, stroke_color=LUMEN_EARLY, stroke_width=2.0)

        ilv_c = endo_c + np.array([0.85, -0.05, 0.0])
        ilv_r = 0.82
        ilv_ring = Circle(radius=ilv_r, stroke_color=MEMBRANE, stroke_width=4.5,
                          fill_color=BG, fill_opacity=0.85).move_to(ilv_c)
        rec_r = make_receptor(ilv_c + np.array([0.0, ilv_r, 0.0]), tail_angle=-PI / 2,
                              scale=0.68, active=False, ligand=True)
        lbl_r = boxed_label("Silenced inside vesicle", color=TEXT, size=28, pad=0.2).move_to([3.95, 2.75, 0.0]).set_z_index(20)
        arr_r = Arrow(lbl_r.get_bottom() + DOWN * 0.08, ilv_c + np.array([0.45, 0.68, 0.0]),
                      buff=0.05, color=TEXT, stroke_width=3.2, max_tip_length_to_length_ratio=0.18)

        self.at("Endocytosis alone")
        self.play(FadeIn(endo), FadeIn(rec_l), FadeIn(lbl_l), FadeIn(tag), run_time=0.65)
        self.add(ripples_l)
        self.play(Indicate(rec_l, color=RECEPTOR, scale_factor=1.08), run_time=1.6)

        self.at("Mild acid")
        acid_lbl = T("Mild acid (pH 6–6.5): ligand lets go", size=26, color=LUMEN_EARLY).move_to([-2.3, -2.98, 0.0]).set_z_index(20)
        self.play(FadeIn(rec_m_on), FadeIn(acid_lbl), run_time=0.7)

        self.at("ligand lets go")
        self.play(Transform(rec_m_on, rec_m_off), FadeIn(freed_lig), run_time=0.6)
        self.play(freed_lig.animate.shift(RIGHT * 1.1 + UP * 0.30), run_time=1.2, rate_func=smooth)

        self.at("Otherwise")
        self.play(FadeOut(rec_m_on), FadeOut(freed_lig), FadeOut(acid_lbl), run_time=0.6)

        self.at("Active receptors")
        ilv_all = VGroup(ilv_ring, rec_r)
        self.play(GrowFromCenter(ilv_all), FadeIn(lbl_r), GrowArrow(arr_r), run_time=1.3)

        self.at("sealed inside internal")
        self.play(Indicate(lbl_r, color=TEXT, scale_factor=1.05), run_time=1.0)
        self.finish()


class S12End(EndCard):
    LINE = "Active receptors can signal from endosomes until sealed inside internal vesicles."
