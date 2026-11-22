"""Pulled In, Sorted Back Out — Endocytosis and Signaling Endosomes

COLOUR MAP (one colour per concept for the whole film):
- MEMBRANE = "#60A5FA"   : plasma membrane bilayer, coated/bare vesicles, endosome & tubule walls
- RECEPTOR = "#2DD4BF"   : transmembrane receptors (ligand-binding head, stem, cytoplasmic tail) + turnover highlight
- LIGAND   = "#FDE68A"   : LDL / extracellular ligand particles
- ADAPTOR  = "#F59E0B"   : adaptor protein bridge & inner-leaflet membrane lipid patch
- CLATHRIN = "#FB923C"   : clathrin lattice triskelion units shaping the coated pit
- DYNAMIN  = "#A78BFA"   : dynamin helical collar & GTP -> GDP scission trigger
- RAB5     = "#38BDF8"   : Rab5 switch markers identifying the early endosome
- ACID     = "#FBBF24"   : proton pumps, H+ ions, and acidified pH 6-6.5 endosomal lumen
- RECYCLE  = "#5EEAD4"   : Rab4 / Rab4+Rab11 recycling tubules, recycling compartment, and return paths
- TEXT     = "#E8EAF0"   : primary labels and equations (from bp_style)
- GREY     = "#8B93A1"   : scope tags and plot axes/ticks only

ONE CARRIED WORLD:
A cellular cross-section with extracellular fluid above, the slate-blue plasma membrane bilayer
across the upper zone, and the cytosol below containing the Rab5 early endosome sorting station.
We zoom smoothly onto one coated pit for entry and scission (s03-s04), pull into the early
endosome for topology, acidification, and tubule geometry (s05-s09), and pull back out to show
the full plasma-membrane-to-endosome recycling loop (s10-s11).

WHAT CHANGES IN EACH SPOKEN SCENE (and what it is computed from):
- s01_hook: Continuous parametric pit dimpling, pinching, and downward drift of receptor-loaded vesicles computed from time t while membrane span holds fixed.
- s02_flux_math: Uptake vesicles bud at 3%/min above while a computed circular turnover ring (t / 33.3 min) fills to 100% (33 min) alongside 100% / 3%/min = 33 min, followed by upward return vesicles.
- s03_entry_adaptor: Zoomed-in receptor glides into the pit site and membrane curves continuously while clathrin triskelions form below a visible gap, then amber adaptors slide in to bridge lipid patch, tail sequence, and clathrin.
- s04_dynamin_cut: Pit neck radius and bulb depth follow a smooth parametric flask curve as dynamin rings wrap and constrict on GTP -> GDP, severing the neck and freeing the coated vesicle downward.
- s05_topology_rab5: Clathrin and adaptors peel away, the bare vesicle descends and merges smoothly into the Rab5 early endosome wall, Rab5 markers dock sequentially, and a traced arrow follows the outward cytosolic tail.
- s06_acid_and_shape: Proton pumps dock and push H+ inward driving a live pH tracker from 7.0 to 6.2 (lumen colour interpolated with pH), LDL particles detach and diffuse (fixed-seed RNG), and two rounded tubules grow via a length tracker.
- s07_tube_geometry: Left: freed LDL particles diffuse continuously inside the round endosome body; Right: a wide cylinder's radius shrinks from R to R/10 while computed S/V = 2/r climbs from 2 to 20 against sphere 3/R (~6.7x).
- s08_predict: Early endosome centers with continuously diffusing freed LDL inside the lumen, an untagged receptor drifts to the tubule junction, and two dashed choice arrows + question card appear.
- s10_recycle_reveal: Computed 1D random walks (fixed seed) carry untagged receptors along the membrane into the mint-teal tubules while freed LDL diffuses in the lumen; Rab4 fast tubule pinches straight to the surface while Rab4/Rab11 loops via a recycling compartment.
- s11_close: Three LDL receptors + ligands traverse the complete closed cycle (pit entry -> Rab5 endosome ligand release -> ~10 min recycling tubule back to surface) with a side branch to the Golgi.
"""
from bp_parts import *

# Concept colour map
MEMBRANE = "#60A5FA"
RECEPTOR = "#2DD4BF"
LIGAND = "#FDE68A"
ADAPTOR = "#F59E0B"
CLATHRIN = "#FB923C"
DYNAMIN = "#A78BFA"
RAB5 = "#38BDF8"
ACID = "#FBBF24"
RECYCLE = "#5EEAD4"

RNG_SEED = 7
TAIL = 0.4


# ------------------------------------------------------------------ shared geometry helpers
def _bilayer_curves(pts_2d, half_thick=0.10, color=MEMBRANE, stroke_w=4.0):
    """Build a crisp double-leaflet bilayer ribbon along an open 2D path."""
    pts = np.asarray(pts_2d, dtype=float)
    tang = np.zeros_like(pts)
    tang[1:-1] = pts[2:] - pts[:-2]
    tang[0] = pts[1] - pts[0]
    tang[-1] = pts[-1] - pts[-2]
    norms = np.maximum(np.linalg.norm(tang, axis=1, keepdims=True), 1e-6)
    tang = tang / norms
    perp = np.stack([-tang[:, 1], tang[:, 0]], axis=1)

    outer = pts + half_thick * perp
    inner = pts - half_thick * perp

    outer_3d = [np.array([p[0], p[1], 0.0]) for p in outer]
    inner_3d = [np.array([p[0], p[1], 0.0]) for p in inner]

    fill_pts = outer_3d + list(reversed(inner_3d))
    band = Polygon(*fill_pts, stroke_width=0, fill_color=color, fill_opacity=0.22)
    top_line = VMobject(stroke_color=color, stroke_width=stroke_w).set_points_as_corners(outer_3d)
    bot_line = VMobject(stroke_color=color, stroke_width=stroke_w).set_points_as_corners(inner_3d)
    return VGroup(band, top_line, bot_line)


def _pit_profile(xs, pit_x=0.0, depth=0.0, width=0.65):
    """Smooth Gaussian-dimple y-offset (negative downward) along horizontal membrane."""
    if depth <= 1e-4:
        return np.zeros_like(xs)
    return -depth * np.exp(-((xs - pit_x) / width) ** 2)


def make_receptor(pos=(0, 0, 0), normal_angle=PI / 2, scale=1.0, has_ligand=True, color=RECEPTOR, ligand_color=LIGAND):
    """Schematic transmembrane receptor: cup-shaped extracellular head, stem, cytoplasmic tail.

    `normal_angle` points outward (extracellular / lumen side); default PI/2 points UP.
    """
    g = VGroup()
    stem = Line(DOWN * 0.24 * scale, UP * 0.16 * scale, color=color, stroke_width=4.5 * scale)
    cup = Arc(radius=0.12 * scale, start_angle=PI, angle=PI, color=color, stroke_width=4.5 * scale).shift(UP * 0.25 * scale)
    tail = VMobject(stroke_color=color, stroke_width=4.0 * scale)
    tail.set_points_as_corners([
        DOWN * 0.24 * scale,
        DOWN * 0.36 * scale + RIGHT * 0.05 * scale,
        DOWN * 0.48 * scale - RIGHT * 0.03 * scale,
    ])
    g.add(stem, cup, tail)
    if has_ligand:
        lig = Dot(UP * 0.25 * scale, radius=0.095 * scale, color=ligand_color)
        g.add(lig)
        g.ligand = lig
    else:
        g.ligand = None
    g.tail = tail
    g.cup = cup
    g.rotate(normal_angle - PI / 2, about_point=ORIGIN)
    g.move_to(pos)
    return g


def make_vesicle(center, radius=0.38, n_receptors=2, has_ligand=True, coat_color=None, adaptor_color=None):
    """A closed circular vesicle bilayer with receptors pointing into its lumen and tails outward."""
    c = np.array(center, dtype=float)
    outer = Circle(radius=radius + 0.055, color=MEMBRANE, stroke_width=3.5, fill_color=MEMBRANE, fill_opacity=0.18).move_to(c)
    inner = Circle(radius=radius - 0.055, color=MEMBRANE, stroke_width=3.0, fill_color="#1B2538", fill_opacity=0.95).move_to(c)
    g = VGroup(outer, inner)
    for i in range(n_receptors):
        ang = -PI / 2 + (i - (n_receptors - 1) / 2) * 1.15
        pos = c + radius * np.array([np.cos(ang), np.sin(ang), 0.0])
        rec = make_receptor(pos=pos, normal_angle=ang + PI, scale=0.65, has_ligand=has_ligand)
        g.add(rec)
    if adaptor_color is not None:
        for i in range(6):
            ang = i * TAU / 6 + 0.2
            p = c + (radius + 0.16) * np.array([np.cos(ang), np.sin(ang), 0.0])
            blk = RoundedRectangle(corner_radius=0.04, width=0.18, height=0.10, color=adaptor_color,
                                   fill_color=adaptor_color, fill_opacity=0.88, stroke_width=1.5).rotate(ang + PI / 2).move_to(p)
            g.add(blk)
    if coat_color is not None:
        tri_scale = 0.23 * min(1.0, radius / 0.45)
        for i in range(6):
            ang = i * TAU / 6 + 0.5
            p = c + (radius * 1.45) * np.array([np.cos(ang), np.sin(ang), 0.0])
            tri = make_clathrin_triskelion(p, scale=tri_scale, angle=ang, color=coat_color)
            g.add(tri)
    return g


def make_clathrin_triskelion(center=(0, 0, 0), scale=0.32, angle=0.0, color=CLATHRIN):
    """Schematic three-legged geometric clathrin pinwheel (not a molecular structure)."""
    g = VGroup()
    for k in range(3):
        a = angle + k * TAU / 3
        p0 = np.array([0.0, 0.0, 0.0])
        p1 = 0.55 * scale * np.array([np.cos(a), np.sin(a), 0.0])
        p2 = 1.0 * scale * np.array([np.cos(a + 0.42), np.sin(a + 0.42), 0.0])
        leg = VMobject(stroke_color=color, stroke_width=4.0, fill_opacity=0).set_points_as_corners([p0, p1, p2])
        g.add(leg)
    hub = Dot(ORIGIN, radius=0.055 * scale / 0.32, color=color)
    g.add(hub)
    return g.move_to(center)


def make_adaptor_block(center=(0, 0, 0), angle=0.0, scale=1.0, color=ADAPTOR):
    """Schematic adaptor protein clamp bridging membrane lipid, receptor tail, and clathrin."""
    body = RoundedRectangle(corner_radius=0.08 * scale, width=0.44 * scale, height=0.22 * scale,
                            stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.85)
    grip_top = Line(LEFT * 0.14 * scale + UP * 0.11 * scale, LEFT * 0.14 * scale + UP * 0.22 * scale,
                    color=color, stroke_width=4.0)
    grip_bot = Line(DOWN * 0.11 * scale, DOWN * 0.22 * scale, color=color, stroke_width=4.0)
    g = VGroup(body, grip_top, grip_bot)
    g.rotate(angle, about_point=ORIGIN)
    return g.move_to(center)


def make_endosome_contour(center=(0, -0.8, 0), rx=2.2, ry=1.55, tube_left=0.0, tube_right=0.0):
    """Compute smooth, rounded-tip 2D perimeter points of an early endosome with optional tubules."""
    c = np.array(center[:2], dtype=float)
    ts = np.linspace(0, TAU, 360, endpoint=False)
    pts = np.stack([rx * np.cos(ts), ry * np.sin(ts)], axis=1)

    # Thin cylindrical rounded-cap tubules (w=0.20, span=0.16) keep inner leaflets non-crossing
    def add_tube(pts_arr, theta0, length):
        if length <= 1e-3:
            return pts_arr
        dtheta = np.angle(np.exp(1j * (ts - theta0)))
        span = 0.16
        idx = np.where(np.abs(dtheta) < span)[0]
        if len(idx) == 0:
            return pts_arr
        u = np.array([np.cos(theta0), np.sin(theta0)])
        v = np.array([-np.sin(theta0), np.cos(theta0)])
        p0 = np.array([rx * np.cos(theta0), ry * np.sin(theta0)])
        w = 0.20
        s = dtheta[idx] / span
        cap_s, shaft_s = 0.36, 0.84
        blend = float(np.clip(length / 0.35, 0.0, 1.0))
        shaft_len = max(0.0, length - w)
        out = pts_arr.copy()
        for k, sk in enumerate(s):
            a, sgn = abs(sk), (1.0 if sk >= 0 else -1.0)
            if a <= cap_s:
                phi = (sk / cap_s) * (PI / 2)
                pt_cyl = p0 + (shaft_len + w * np.cos(phi)) * u + (w * np.sin(phi)) * v
            elif a <= shaft_s:
                f = 1.0 - (a - cap_s) / (shaft_s - cap_s)
                pt_cyl = p0 + (f * shaft_len) * u + (sgn * w) * v
            else:
                f = 0.5 * (1.0 + np.cos(PI * (a - shaft_s) / (1.0 - shaft_s)))
                pt_base = p0 + sgn * w * v
                pt_cyl = pts_arr[idx[k]] + f * (pt_base - pts_arr[idx[k]])
            out[idx[k]] = pts_arr[idx[k]] + blend * (pt_cyl - pts_arr[idx[k]])
        return out

    pts = add_tube(pts, np.deg2rad(138), tube_left)
    pts = add_tube(pts, np.deg2rad(42), tube_right)
    return pts + c[None, :]


def make_endosome_shell(center=(0, -0.8, 0), rx=2.2, ry=1.55, tube_left=0.0, tube_right=0.0,
                        ph=7.0, stroke_w=3.8):
    """Build the early endosome bilayer + pH-tinted lumen from make_endosome_contour."""
    pts = make_endosome_contour(center, rx, ry, tube_left, tube_right)
    tang = np.roll(pts, -1, axis=0) - np.roll(pts, 1, axis=0)
    norms = np.maximum(np.linalg.norm(tang, axis=1, keepdims=True), 1e-6)
    tang /= norms
    perp = np.stack([tang[:, 1], -tang[:, 0]], axis=1)  # outward for CCW
    outer = pts + 0.065 * perp
    inner = pts - 0.065 * perp

    # pH 7.0 -> clear slate-blue lumen; pH 6.2 -> rich soft amber
    frac = float(np.clip((7.0 - ph) / 0.85, 0.0, 1.0))
    lumen_col = interpolate_color(ManimColor("#2E4463"), ManimColor(ACID), frac)
    lumen_op = 0.48 - 0.14 * frac

    inner_3d = [np.array([p[0], p[1], 0.0]) for p in inner]
    outer_3d = [np.array([p[0], p[1], 0.0]) for p in outer]
    lumen = Polygon(*inner_3d, stroke_width=0, fill_color=lumen_col, fill_opacity=lumen_op)
    outer_ring = VMobject(stroke_color=MEMBRANE, stroke_width=stroke_w).set_points_as_corners(outer_3d + [outer_3d[0]])
    inner_ring = VMobject(stroke_color=MEMBRANE, stroke_width=stroke_w * 0.85).set_points_as_corners(inner_3d + [inner_3d[0]])
    return VGroup(lumen, outer_ring, inner_ring), pts, perp


def make_rab5_dots(pts, perp, indices=(25, 80, 145, 210, 275, 325), color=RAB5):
    """Place Rab5 switch protein markers on the outer cytosolic rim of the endosome."""
    g = VGroup()
    for idx in indices:
        i = idx % len(pts)
        p = pts[i] + 0.19 * perp[i]
        d = Circle(radius=0.11, color=color, fill_color=color, fill_opacity=0.92, stroke_width=2).move_to([p[0], p[1], 0])
        g.add(d)
    return g


# ------------------------------------------------------------------ scenes
class S00Title(TitleCard):
    LESSON = "Endocytosis and Signaling Endosomes"
    TITLE = "Pulled In, Sorted Back Out"


class S01Hook(SpokenScene):
    def construct(self):
        t = ValueTracker(0.0)
        xs = np.linspace(-6.1, 6.1, 140)
        y_mem = 1.95

        static_locs = [-5.0, -3.7, 3.7, 5.0]
        static_recs = VGroup(*[make_receptor([x, y_mem, 0], scale=0.82, has_ligand=False) for x in static_locs])

        pit_xs = [-1.9, 0.0, 1.9]
        period = 4.2

        def sim_membrane():
            tau = t.get_value()
            ys = np.full_like(xs, y_mem)
            ves = VGroup()
            for idx, px in enumerate(pit_xs):
                phase = ((tau + idx * 1.4) % period) / period
                if phase < 0.40:
                    d = 0.95 * np.sin(PI * phase / 0.40)
                    ys += _pit_profile(xs, pit_x=px, depth=d, width=0.55)
                    ves.add(make_receptor([px, y_mem - d + 0.02, 0], normal_angle=PI / 2, scale=0.76, has_ligand=True))
                else:
                    heal = max(0.0, 1.0 - (phase - 0.40) / 0.16)
                    ys += _pit_profile(xs, pit_x=px, depth=0.38 * heal, width=0.45)
                    drop_frac = (phase - 0.40) / 0.60
                    vy = (y_mem - 0.95) - 3.95 * drop_frac
                    if vy > -3.2:
                        ves.add(make_vesicle([px, vy, 0], radius=0.38, n_receptors=2, has_ligand=True))
            pts = np.stack([xs, ys], axis=1)
            return VGroup(_bilayer_curves(pts, half_thick=0.10, color=MEMBRANE), ves)

        mem_group = always_redraw(sim_membrane)

        lbl_mem = T("Plasma membrane", size=30, color=TEXT).move_to([-3.9, 2.95, 0])
        lbl_cyto = T("Cytosol", size=30, color=TEXT).move_to([-4.9, -2.75, 0])
        q_banner = boxed_label("Where do they go?", color=GOLD, size=30).move_to([3.7, 2.95, 0])
        endo_chip = boxed_label("Endocytosis", color=MEMBRANE, size=30).move_to([4.0, -2.05, 0])
        tag = scope_tag("schematic")

        self.add(mem_group, static_recs, lbl_mem, lbl_cyto, tag)

        dt0 = max(0.5, self.t_of("Where do all") - 0.2 - self.elapsed())
        self.play(t.animate(run_time=dt0, rate_func=linear).set_value(dt0))

        self.at("Where do all")
        dt1 = max(0.6, self.t_of("Pulling plasma membrane") - 0.2 - self.elapsed())
        self.play(FadeIn(q_banner, shift=DOWN * 0.1, run_time=0.5),
                  t.animate(run_time=dt1, rate_func=linear).set_value(t.get_value() + dt1))

        self.at("Pulling plasma membrane")
        dt2 = max(0.5, self.t_of("called endocytosis") - 0.2 - self.elapsed())
        self.play(t.animate(run_time=dt2, rate_func=linear).set_value(t.get_value() + dt2))

        self.at("called endocytosis")
        rem = max(0.6, self.narration_s + TAIL - self.elapsed())
        self.play(FadeIn(endo_chip, shift=UP * 0.1, run_time=0.45),
                  t.animate(run_time=rem, rate_func=linear).set_value(t.get_value() + rem))
        self.finish()


class S02FluxMath(SpokenScene):
    def construct(self):
        t = ValueTracker(0.0)
        prog = ValueTracker(0.0)
        ret_prog = ValueTracker(0.0)

        xs = np.linspace(-6.1, 6.1, 140)
        y_mem = 2.35
        pit_xs = [-3.8, -1.6, 0.6]
        period = 3.8

        def sim_top():
            tau = t.get_value()
            ys = np.full_like(xs, y_mem)
            ves = VGroup()
            for idx, px in enumerate(pit_xs):
                phase = ((tau + idx * 1.26) % period) / period
                if phase < 0.45:
                    d = 0.65 * np.sin(PI * phase / 0.45)
                    ys += _pit_profile(xs, pit_x=px, depth=d, width=0.48)
                    ves.add(make_receptor([px, y_mem - d + 0.02, 0], scale=0.68, has_ligand=True))
                else:
                    drop = (phase - 0.45) / 0.55
                    vy = (y_mem - 0.72) - 1.15 * drop
                    if vy > 0.45:
                        ves.add(make_vesicle([px, vy, 0], radius=0.30, n_receptors=2, has_ligand=True))
            return VGroup(_bilayer_curves(np.stack([xs, ys], axis=1), half_thick=0.09, color=MEMBRANE), ves)

        mem_top = always_redraw(sim_top)
        lbl_mem = T("Plasma membrane", size=28, color=TEXT).move_to([-4.0, 3.05, 0])

        # Lower-left computed formula steps (strictly below y = -0.35, clear of top vesicles y > 0.45)
        step1 = M("uptake = 3% / min", size=30, color=ADAPTOR).move_to([-3.3, -0.55, 0])
        step2 = T("Total area ÷ uptake rate = turnover time", size=28, color=TEXT).move_to([-2.75, -1.35, 0])
        step3 = M("100% ÷ 3% / min", size=32, color=TEXT).move_to([-4.25, -2.20, 0])
        step4 = M("≈ 33 min", size=36, color=RECEPTOR).next_to(step3, RIGHT, buff=0.32)

        # Right lower panel: computed circular progress ring
        ring_c = np.array([3.65, -1.30, 0.0])
        ring_r = 1.25
        ring_bg = Circle(radius=ring_r, color=GREY, stroke_width=10).set_opacity(0.35).move_to(ring_c)
        ring_arc = always_redraw(lambda: Arc(
            radius=ring_r, start_angle=PI / 2, angle=-max(prog.get_value(), 0.002) * TAU,
            arc_center=ring_c, stroke_color=RECEPTOR, stroke_width=12
        ))
        ring_pct = always_redraw(lambda: M(f"{prog.get_value() * 100:.0f}%", size=34, color=TEXT).move_to(ring_c + UP * 0.22))
        ring_min = always_redraw(lambda: M(f"{prog.get_value() * 33.3:.0f} min", size=28, color=RECEPTOR).move_to(ring_c + DOWN * 0.28))

        # Return arrows beside (never piercing) rising return vesicles
        def return_flow():
            rp = ret_prog.get_value()
            if rp <= 0.001:
                return VGroup()
            g = VGroup()
            for x_arr, x_ves in ((2.0, 2.55), (4.5, 5.05)):
                g.add(Arrow([x_arr, 0.45, 0], [x_arr, y_mem - 0.35, 0], color=RECYCLE, stroke_width=5, buff=0))
                vy = 0.55 + rp * 1.20
                g.add(make_vesicle([x_ves, vy, 0], radius=0.25, n_receptors=1, has_ligand=False))
            return g

        ret_mob = always_redraw(return_flow)
        ret_lbl = T("Return", size=28, color=RECYCLE).move_to([3.55, 1.25, 0])
        tag = scope_tag("computed rate")

        self.add(mem_top, lbl_mem, ring_bg, ring_arc, ring_pct, ring_min, ret_mob, tag)

        dt0 = max(0.4, self.t_of("about 3") - 0.2 - self.elapsed())
        self.play(t.animate(run_time=dt0, rate_func=linear).set_value(dt0))

        self.at("about 3")
        dt1 = max(0.5, self.t_of("Total area divided") - 0.2 - self.elapsed())
        self.play(FadeIn(step1, shift=UP * 0.1, run_time=0.45),
                  t.animate(run_time=dt1, rate_func=linear).set_value(t.get_value() + dt1))

        self.at("Total area divided")
        dt2 = max(0.5, self.t_of("100") - 0.2 - self.elapsed())
        self.play(FadeIn(step2, shift=UP * 0.1, run_time=0.45),
                  t.animate(run_time=dt2, rate_func=linear).set_value(t.get_value() + dt2))

        self.at("100")
        dt3 = max(0.5, self.t_of("equals about 33") - 0.2 - self.elapsed())
        self.play(FadeIn(step3, shift=RIGHT * 0.12, run_time=0.45),
                  t.animate(run_time=dt3, rate_func=linear).set_value(t.get_value() + dt3))

        self.at("equals about 33")
        dt4 = max(1.0, self.t_of("Membrane must return") - 0.2 - self.elapsed())
        ring_dt = min(0.9, dt4)
        self.play(FadeIn(step4, shift=RIGHT * 0.1, run_time=0.45),
                  prog.animate(run_time=ring_dt, rate_func=smooth).set_value(1.0),
                  t.animate(run_time=ring_dt, rate_func=linear).set_value(t.get_value() + ring_dt))
        if dt4 - ring_dt > 0.05:
            rem4 = dt4 - ring_dt
            self.play(t.animate(run_time=rem4, rate_func=linear).set_value(t.get_value() + rem4))

        self.at("Membrane must return")
        rem = max(0.5, self.narration_s + TAIL - self.elapsed())
        self.play(FadeIn(ret_lbl, run_time=0.4),
                  ret_prog.animate(run_time=rem, rate_func=linear).set_value(1.0),
                  t.animate(run_time=rem, rate_func=linear).set_value(t.get_value() + rem))
        self.finish()


class S03EntryAdaptor(SpokenScene):
    def construct(self):
        depth = ValueTracker(0.0)
        rec_x = ValueTracker(-1.8)
        clath_in = ValueTracker(0.0)
        adap_in = ValueTracker(0.0)
        xs = np.linspace(-6.1, 6.1, 140)
        y_mem = 1.65

        def world():
            d = depth.get_value()
            rx = rec_x.get_value()
            ci = clath_in.get_value()
            ai = adap_in.get_value()
            ys = y_mem + _pit_profile(xs, pit_x=0.0, depth=d, width=1.65)
            bil = _bilayer_curves(np.stack([xs, ys], axis=1), half_thick=0.14, color=MEMBRANE, stroke_w=4.5)

            y0 = y_mem + _pit_profile(np.array([rx]), pit_x=0.0, depth=d, width=1.65)[0]
            rec = make_receptor([rx, y0, 0], normal_angle=PI / 2, scale=1.65, has_ligand=True)
            lip_xs = np.linspace(-1.05, -0.35, 25)
            lip_ys = y_mem + _pit_profile(lip_xs, pit_x=0.0, depth=d, width=1.65) - 0.16
            lipid_patch = VMobject(stroke_color=ADAPTOR, stroke_width=7).set_points_as_corners(
                [np.array([x, y, 0.0]) for x, y in zip(lip_xs, lip_ys)]
            )

            g = VGroup(bil, rec)
            if ai > 0.05:
                g.add(lipid_patch)

            # Clathrin lattice sits below adaptors (-1.10 offset)
            if ci > 0.01:
                clath_g = VGroup()
                for px in (-1.5, -0.75, 0.0, 0.75, 1.5):
                    cy = y_mem + _pit_profile(np.array([px]), pit_x=0.0, depth=d, width=1.65)[0] - 1.10 - (1.0 - ci) * 0.75
                    ang = px * 0.28
                    tri = make_clathrin_triskelion([px, cy, 0], scale=0.40, angle=ang, color=CLATHRIN)
                    for leg in tri[:3]:
                        leg.set_stroke(opacity=ci)
                    tri[3].set_fill(opacity=ci)
                    clath_g.add(tri)
                g.add(clath_g)

            # Adaptors sit cleanly in the bridge zone (-0.46 offset, gripping lipid, tail, and clathrin)
            if ai > 0.01:
                adap_g = VGroup()
                for px in (-0.38, 0.40):
                    target_y = y_mem + _pit_profile(np.array([px]), pit_x=0.0, depth=d, width=1.65)[0] - 0.46
                    start_y = target_y - 1.0
                    cy = start_y + ai * (target_y - start_y)
                    blk = make_adaptor_block([px, cy, 0], angle=-px * 0.15, scale=1.12, color=ADAPTOR)
                    blk.set_opacity(ai)
                    adap_g.add(blk)
                g.add(adap_g)
            return g

        scene_mob = always_redraw(world)
        lbl_mem = T("Plasma membrane", size=28, color=TEXT).move_to([-4.1, 2.75, 0])
        lbl_lig = T("Ligand", size=28, color=LIGAND).move_to([1.85, 2.45, 0])
        lbl_rec = T("Receptor tail", size=28, color=RECEPTOR).move_to([3.35, 0.45, 0])
        lbl_clath = T("Clathrin", size=30, color=CLATHRIN).move_to([3.55, -1.75, 0])
        lbl_gap = T("No direct contact", size=28, color=GOLD).move_to([-3.65, -0.25, 0])
        gap_bar = DashedLine([-0.9, 1.00, 0], [-0.9, 0.55, 0], color=GOLD, stroke_width=3.5)
        lbl_adap = T("Adaptor", size=30, color=ADAPTOR).move_to([-3.65, 0.15, 0])
        lbl_lipid = T("Membrane lipid", size=26, color=ADAPTOR).move_to([-3.65, -0.65, 0])
        lbl_motif = T("Tail sequence", size=26, color=RECEPTOR).move_to([3.35, -0.40, 0])
        tag = scope_tag("schematic")

        self.add(scene_mob, lbl_mem, lbl_lig, lbl_rec, tag)

        dt0 = max(0.5, self.t_of("at a coated pit") - 0.2 - self.elapsed())
        self.play(rec_x.animate(run_time=dt0, rate_func=smooth).set_value(0.0),
                  depth.animate(run_time=dt0, rate_func=smooth).set_value(0.25))

        self.at("at a coated pit")
        dt_pit = max(0.6, self.t_of("called clathrin") - 0.2 - self.elapsed())
        self.play(depth.animate(run_time=dt_pit, rate_func=smooth).set_value(0.55))

        self.at("called clathrin")
        dt_cl = max(0.6, self.t_of("touches neither membrane") - 0.2 - self.elapsed())
        self.play(clath_in.animate(run_time=min(1.2, dt_cl), rate_func=smooth).set_value(1.0),
                  FadeIn(lbl_clath, run_time=0.45))
        rem_cl = max(0.05, self.t_of("touches neither membrane") - 0.2 - self.elapsed())
        if rem_cl > 0.1:
            self.wait(rem_cl)

        self.at("touches neither membrane")
        dt_gap = max(0.6, self.t_of("Adaptor proteins bridge") - 0.2 - self.elapsed())
        self.play(FadeIn(lbl_gap, run_time=0.4), Create(gap_bar, run_time=min(1.6, dt_gap)))
        rem_gap = max(0.05, self.t_of("Adaptor proteins bridge") - 0.2 - self.elapsed())
        if rem_gap > 0.1:
            self.wait(rem_gap)

        self.at("Adaptor proteins bridge")
        self.play(FadeOut(lbl_gap, run_time=0.35), FadeOut(gap_bar, run_time=0.35))
        self.play(adap_in.animate(run_time=1.0, rate_func=smooth).set_value(1.0), FadeIn(lbl_adap, run_time=0.4))

        self.at("a membrane lipid")
        self.play(FadeIn(lbl_lipid, run_time=0.45))

        self.at("receptor tail sequence")
        self.play(FadeIn(lbl_motif, run_time=0.45))

        self.at("and clathrin")
        rem = max(0.4, self.narration_s + TAIL - self.elapsed())
        self.play(depth.animate(run_time=rem, rate_func=smooth).set_value(0.95))
        self.finish()


class S04DynaminCut(SpokenScene):
    def construct(self):
        neck_half = ValueTracker(1.25)
        bulb_cy = ValueTracker(0.55)
        collar_on = ValueTracker(0.0)
        collar_tight = ValueTracker(0.0)
        severed = ValueTracker(0.0)

        xs = np.linspace(-6.1, 6.1, 140)
        y_mem = 2.05

        def pit_flask():
            nw = neck_half.get_value()
            cy = bulb_cy.get_value()
            co = collar_on.get_value()
            ct = collar_tight.get_value()
            sev = severed.get_value()
            g = VGroup()

            if sev < 0.5:
                r_bulb = 1.05
                # Keep neck clearance >= 0.18 before cut so inner bilayer leaflets never cross
                nw_eff = max(nw, 0.22)
                theta_top = np.arcsin(np.clip(nw_eff / r_bulb, 0.20, 0.92))
                ang_s = np.linspace(PI / 2 + theta_top, 5 * PI / 2 - theta_top, 100)
                bulb_pts = np.stack([r_bulb * np.cos(ang_s), cy + r_bulb * np.sin(ang_s)], axis=1)

                left_flat = np.stack([np.linspace(-6.1, -nw_eff - 0.95, 25), np.full(25, y_mem)], axis=1)
                right_flat = np.stack([np.linspace(nw_eff + 0.95, 6.1, 25), np.full(25, y_mem)], axis=1)

                t_l = np.linspace(0, 1, 24)
                p0_l = np.array([-nw_eff - 0.95, y_mem])
                p3_l = bulb_pts[0]
                tang_b0 = np.array([-np.sin(ang_s[0]), np.cos(ang_s[0])])
                p1_l = p0_l + np.array([0.55, 0.0])
                p2_l = p3_l - 0.35 * tang_b0
                left_neck = ((1 - t_l[:, None]) ** 3) * p0_l + 3 * ((1 - t_l[:, None]) ** 2) * t_l[:, None] * p1_l + 3 * (1 - t_l[:, None]) * (t_l[:, None] ** 2) * p2_l + (t_l[:, None] ** 3) * p3_l

                p0_r = bulb_pts[-1]
                p3_r = np.array([nw_eff + 0.95, y_mem])
                tang_b1 = np.array([-np.sin(ang_s[-1]), np.cos(ang_s[-1])])
                p1_r = p0_r + 0.35 * tang_b1
                p2_r = p3_r - np.array([0.55, 0.0])
                right_neck = ((1 - t_l[:, None]) ** 3) * p0_r + 3 * ((1 - t_l[:, None]) ** 2) * t_l[:, None] * p1_r + 3 * (1 - t_l[:, None]) * (t_l[:, None] ** 2) * p2_r + (t_l[:, None] ** 3) * p3_r

                all_pts = np.vstack([left_flat, left_neck[1:-1], bulb_pts, right_neck[1:-1], right_flat])
                g.add(_bilayer_curves(all_pts, half_thick=0.095, color=MEMBRANE, stroke_w=4.0))

                g.add(make_receptor([0.0, cy - r_bulb, 0], normal_angle=PI / 2, scale=0.95, has_ligand=True))
                for ang in np.linspace(-1.05 * PI, 0.05 * PI, 5):
                    pa = np.array([0.0, cy, 0.0]) + (r_bulb + 0.22) * np.array([np.cos(ang), np.sin(ang), 0.0])
                    g.add(make_adaptor_block(pa, angle=ang + PI / 2, scale=0.75, color=ADAPTOR))
                    pc = np.array([0.0, cy, 0.0]) + (r_bulb + 0.50) * np.array([np.cos(ang), np.sin(ang), 0.0])
                    g.add(make_clathrin_triskelion(pc, scale=0.28, angle=ang, color=CLATHRIN))

                if co > 0.01:
                    neck_y = cy + r_bulb * np.cos(theta_top) + 0.25
                    ring_w = max(0.38, (2 * nw_eff + 0.42) * (1.0 - 0.30 * ct))
                    for k, dy in enumerate((-0.18, 0.0, 0.18)):
                        alpha = float(np.clip(co * 3.0 - k * 0.7, 0.0, 1.0))
                        if alpha > 0.02:
                            ring = RoundedRectangle(
                                corner_radius=0.07, width=ring_w, height=0.13,
                                stroke_color=DYNAMIN, stroke_width=3, fill_color=DYNAMIN, fill_opacity=0.88 * alpha
                            ).move_to([0.0, neck_y + dy, 0])
                            g.add(ring)
            else:
                flat_pts = np.stack([xs, np.full_like(xs, y_mem)], axis=1)
                g.add(_bilayer_curves(flat_pts, half_thick=0.095, color=MEMBRANE, stroke_w=4.0))
                g.add(make_vesicle([0.0, cy, 0], radius=1.0, n_receptors=2, has_ligand=True,
                                   coat_color=CLATHRIN, adaptor_color=ADAPTOR))
            return g

        flask_mob = always_redraw(pit_flask)
        lbl_mem = T("Plasma membrane", size=28, color=TEXT).move_to([-4.1, 2.85, 0])
        lbl_neck = T("Thin neck", size=28, color=MEMBRANE).move_to([2.65, 1.15, 0])
        lbl_dyn = T("Dynamin", size=30, color=DYNAMIN).move_to([-2.45, 1.05, 0])
        gtp_chip = boxed_label("GTP → GDP", color=DYNAMIN, size=30).move_to([3.45, 0.50, 0])
        lbl_ves = T("Coated vesicle", size=30, color=CLATHRIN).move_to([3.3, -1.65, 0])
        tag = scope_tag("schematic")

        self.add(flask_mob, lbl_mem, tag)

        dt_pre = max(0.8, self.t_of("a thin neck") - 0.2 - self.elapsed())
        self.play(
            neck_half.animate(run_time=dt_pre, rate_func=smooth).set_value(0.55),
            bulb_cy.animate(run_time=dt_pre, rate_func=smooth).set_value(-0.05),
        )

        self.at("a thin neck")
        dt_neck = max(0.8, self.t_of("called dynamin") - 0.2 - self.elapsed())
        self.play(
            neck_half.animate(run_time=dt_neck, rate_func=smooth).set_value(0.24),
            bulb_cy.animate(run_time=dt_neck, rate_func=smooth).set_value(-0.35),
            FadeIn(lbl_neck, run_time=0.4)
        )

        self.at("called dynamin")
        dt_wrap = max(1.2, self.t_of("Hydralizing GTP") - 0.2 - self.elapsed())
        self.play(collar_on.animate(run_time=dt_wrap, rate_func=linear).set_value(0.85),
                  FadeIn(lbl_dyn, run_time=0.45))

        self.at("Hydralizing GTP")
        dt_gtp = max(0.6, self.t_of("tightens the collar") - 0.2 - self.elapsed())
        self.play(FadeIn(gtp_chip, scale=1.06, run_time=0.35),
                  collar_on.animate(run_time=dt_gtp, rate_func=linear).set_value(1.0))

        self.at("tightens the collar")
        dt_cut = max(0.8, self.t_of("cutting the neck") - 0.2 - self.elapsed())
        self.play(collar_tight.animate(run_time=dt_cut, rate_func=smooth).set_value(1.0),
                  neck_half.animate(run_time=dt_cut, rate_func=smooth).set_value(0.22))

        self.at("cutting the neck")
        severed.set_value(1.0)
        rem = max(0.8, self.narration_s + TAIL - self.elapsed())
        self.play(FadeOut(lbl_neck, run_time=0.3), FadeOut(lbl_dyn, run_time=0.3), FadeOut(gtp_chip, run_time=0.3),
                  FadeIn(lbl_ves, run_time=0.4),
                  bulb_cy.animate(run_time=rem, rate_func=smooth).set_value(-1.65))
        self.finish()


class S05TopologyRab5(SpokenScene):
    def construct(self):
        ves_y = ValueTracker(2.35)
        coat_op = ValueTracker(1.0)
        rab5_prog = ValueTracker(0.0)   # 0 -> 1: Rab5 markers glide from cytosol to dock on rim
        merged = ValueTracker(0.0)
        endo_scale = ValueTracker(0.92) # grows smoothly to 1.04 upon vesicle fusion
        tail_glow = ValueTracker(0.0)   # highlights receptor orientation along membrane

        endo_c = (0.0, -0.70, 0)

        def dyn_world():
            sc = endo_scale.get_value()
            shell, pts, perp = make_endosome_shell(endo_c, rx=2.80 * sc, ry=1.75 * sc, ph=7.0)
            g = VGroup(shell)

            rec_idx = 305
            rec_p = np.array([pts[rec_idx, 0], pts[rec_idx, 1], 0.0])
            out_ang = np.arctan2(perp[rec_idx, 1], perp[rec_idx, 0])

            if merged.get_value() > 0.5:
                # 2 fused receptors on opposite sides to show consistent topology
                for r_i in (150, 305):
                    rp = np.array([pts[r_i, 0], pts[r_i, 1], 0.0])
                    oa = np.arctan2(perp[r_i, 1], perp[r_i, 0])
                    g.add(make_receptor(rp, normal_angle=oa + PI, scale=1.22, has_ligand=True))
                tg = tail_glow.get_value()
                if tg > 0.05:
                    ring = Circle(radius=0.35 + 0.12 * np.sin(tg * TAU), color=RECEPTOR, stroke_width=3.5).move_to(
                        rec_p + 0.35 * np.array([np.cos(out_ang), np.sin(out_ang), 0.0])
                    )
                    g.add(ring)
            else:
                vy = ves_y.get_value()
                co = coat_op.get_value()
                ves = make_vesicle([0.0, vy, 0], radius=0.54, n_receptors=2, has_ligand=True,
                                   coat_color=CLATHRIN if co > 0.05 else None,
                                   adaptor_color=ADAPTOR if co > 0.05 else None)
                if co > 0.05:
                    for m in ves[4:]:
                        m.set_opacity(co)
                if vy < 1.35:
                    ves.set_opacity(float(np.clip((vy - 0.75) / 0.60, 0.15, 1.0)))
                g.add(ves)

            rp_val = rab5_prog.get_value()
            if rp_val > 0.01:
                indices = (25, 85, 130, 205, 265, 330)
                for k, idx in enumerate(indices):
                    u = float(np.clip(rp_val * len(indices) - k, 0.0, 1.0))
                    if u > 0.02:
                        p_end = pts[idx] + 0.19 * perp[idx]
                        p_start = pts[idx] + 0.75 * perp[idx]
                        p = p_start + u * (p_end - p_start)
                        d = Circle(radius=0.11, color=RAB5, fill_color=RAB5, fill_opacity=0.92 * u, stroke_width=2).move_to([p[0], p[1], 0])
                        g.add(d)
            return g

        world_mob = always_redraw(dyn_world)

        lbl_endo = T("Rab5 early endosome", size=30, color=RAB5).move_to([-4.1, -2.90, 0])
        lbl_lumen = T("Ligand in lumen", size=28, color=LIGAND).move_to([0.0, -0.45, 0])
        lbl_tail = T("Tail in cytosol", size=30, color=RECEPTOR).move_to([4.35, -2.55, 0])

        _, pts_f, perp_f = make_endosome_shell(endo_c, rx=2.80 * 1.04, ry=1.75 * 1.04, ph=7.0)
        rec_p_f = np.array([pts_f[305, 0], pts_f[305, 1], 0.0])
        out_ang_f = np.arctan2(perp_f[305, 1], perp_f[305, 0])
        tail_tip = rec_p_f + 0.58 * np.array([np.cos(out_ang_f), np.sin(out_ang_f), 0.0])
        tail_arr = Arrow(lbl_tail.get_left() + LEFT * 0.14, tail_tip + RIGHT * 0.15 + DOWN * 0.08,
                         color=RECEPTOR, stroke_width=4.5, buff=0)
        # Route fold arc cleanly outside the right rim so it never crosses membrane or Rab5 dots
        fold_arc = CurvedArrow(np.array([0.8, 1.90, 0.0]), np.array([3.95, -0.55, 0.0]),
                               angle=-0.55, color=MEMBRANE, stroke_width=4.0)
        tag = scope_tag("schematic")

        self.add(world_mob, tag)

        dt_strip = max(0.8, self.t_of("bare vesicle fuses") - 0.2 - self.elapsed())
        self.play(coat_op.animate(run_time=dt_strip, rate_func=smooth).set_value(0.0),
                  ves_y.animate(run_time=dt_strip, rate_func=smooth).set_value(1.90))

        self.at("bare vesicle fuses")
        dt_fuse = max(1.0, self.t_of("called RAB5") - 0.2 - self.elapsed())
        self.play(ves_y.animate(run_time=dt_fuse * 0.65, rate_func=smooth).set_value(0.80))
        merged.set_value(1.0)
        self.play(endo_scale.animate(run_time=max(0.4, dt_fuse * 0.35), rate_func=smooth).set_value(1.04))

        self.at("called RAB5")
        dt_rab = max(1.2, self.t_of("Because the membrane folded") - 0.2 - self.elapsed())
        self.play(rab5_prog.animate(run_time=dt_rab, rate_func=linear).set_value(1.0),
                  FadeIn(lbl_endo, run_time=0.22))

        self.at("Because the membrane folded")
        dt_fold = max(0.8, self.t_of("the receptor's cytoplasmic tail") - 0.2 - self.elapsed())
        self.play(Create(fold_arc, run_time=dt_fold), FadeIn(lbl_lumen, run_time=0.25))

        self.at("the receptor's cytoplasmic tail")
        rem = max(0.8, self.narration_s + TAIL - self.elapsed())
        self.play(FadeOut(fold_arc, run_time=0.25), FadeIn(lbl_tail, run_time=0.25),
                  GrowArrow(tail_arr, run_time=0.6),
                  tail_glow.animate(run_time=rem, rate_func=linear).set_value(1.5))
        self.finish()


class S06AcidAndShape(SpokenScene):
    def construct(self):
        pump_in = ValueTracker(0.0)
        ph = ValueTracker(7.0)
        release = ValueTracker(0.0)
        tube_l = ValueTracker(0.0)
        drift_t = ValueTracker(0.0)
        h_alpha = ValueTracker(0.0)

        endo_c = (0.0, -0.55, 0)
        rng = np.random.default_rng(RNG_SEED)
        rec_angles = [-0.82 * PI, -0.62 * PI, -0.38 * PI, -0.18 * PI]
        drift_phases = rng.uniform(0, TAU, size=len(rec_angles))

        def live_endosome():
            tl = tube_l.get_value()
            p_val = ph.get_value()
            rel = release.get_value()
            dt = drift_t.get_value()
            pin = pump_in.get_value()
            ha = h_alpha.get_value()

            shell, pts, perp = make_endosome_shell(endo_c, rx=2.85, ry=1.80, tube_left=1.75 * tl, tube_right=1.75 * tl, ph=p_val)
            rabs = make_rab5_dots(pts, perp, indices=(25, 95, 165, 225, 270, 340))
            g = VGroup(shell, rabs)

            for idx in (60, 120):
                p = pts[idx] + (1.0 - pin) * 0.45 * perp[idx]
                ang = np.arctan2(perp[idx, 1], perp[idx, 0])
                pump = RoundedRectangle(corner_radius=0.06, width=0.38, height=0.24, color=ACID,
                                        fill_color=ACID, fill_opacity=0.88 * max(0.3, pin), stroke_width=2).rotate(ang + PI / 2).move_to([p[0], p[1], 0])
                g.add(pump)
                if ha > 0.05:
                    for wave in (0.0, 0.33, 0.66):
                        frac_d = (dt * 0.65 + wave) % 1.0
                        hp = pts[idx] - (0.50 + 1.25 * frac_d) * perp[idx]
                        h_lbl = M("H+", size=24, color=ACID).move_to([hp[0], hp[1], 0]).set_opacity(ha * (1.0 - 0.45 * frac_d))
                        g.add(h_lbl)

            for k, r_ang in enumerate(rec_angles):
                rx, ry = 2.85, 1.80
                # Gentle lateral membrane wobble before release keeps receptors alive
                ang_now = r_ang + 0.04 * np.sin(dt * 1.4 + k)
                wall_p = np.array([endo_c[0] + rx * np.cos(ang_now), endo_c[1] + ry * np.sin(ang_now), 0.0])
                out_a = np.arctan2(np.sin(ang_now) / ry, np.cos(ang_now) / rx)
                g.add(make_receptor(wall_p, normal_angle=out_a + PI, scale=0.92, has_ligand=False))
                bound_p = wall_p - 0.25 * np.array([np.cos(out_a), np.sin(out_a), 0.0])
                free_base = np.array([endo_c[0] + (k - 1.5) * 0.85, endo_c[1] + 0.15 * np.sin(k * 1.7), 0.0])
                free_p = free_base + np.array([
                    0.42 * np.sin(1.9 * dt + drift_phases[k]),
                    0.30 * np.cos(1.5 * dt + drift_phases[k]),
                    0.0
                ])
                lp = bound_p + rel * (free_p - bound_p)
                g.add(Dot(lp, radius=0.125, color=LIGAND))
            return g

        endo_mob = always_redraw(live_endosome)
        lbl_endo = T("Rab5 early endosome", size=28, color=RAB5).move_to([-3.95, -2.90, 0])
        ph_counter = always_redraw(lambda: M(f"pH {ph.get_value():.1f}", size=32, color=ACID).move_to([4.8, 2.75, 0]))
        ph_badge = boxed_label("pH 6–6.5", color=ACID, size=30).move_to([4.8, 2.75, 0])
        lbl_ldl = T("LDL freed", size=28, color=LIGAND).move_to([4.5, 0.85, 0])
        lbl_tubes = T("Thin tubules", size=28, color=MEMBRANE).move_to([-4.25, 2.35, 0])
        tag = scope_tag("schematic")

        self.add(endo_mob, lbl_endo, ph_counter, tag)

        dt0 = max(0.8, self.t_of("proton pumps acidify") - 0.2 - self.elapsed())
        self.play(pump_in.animate(run_time=dt0, rate_func=smooth).set_value(1.0),
                  drift_t.animate(run_time=dt0, rate_func=linear).set_value(dt0))

        self.at("proton pumps acidify")
        dt_acid = max(1.0, self.t_of("about pH 6") - 0.2 - self.elapsed())
        self.play(h_alpha.animate(run_time=0.25).set_value(1.0),
                  ph.animate(run_time=dt_acid, rate_func=smooth).set_value(6.5),
                  drift_t.animate(run_time=dt_acid, rate_func=linear).set_value(drift_t.get_value() + dt_acid))

        self.at("about pH 6")
        dt_ldl = max(1.0, self.t_of("including LDL") - 0.2 - self.elapsed())
        self.play(ph.animate(run_time=min(2.2, dt_ldl), rate_func=smooth).set_value(6.1),
                  drift_t.animate(run_time=dt_ldl, rate_func=linear).set_value(drift_t.get_value() + dt_ldl))
        self.remove(ph_counter)
        self.add(ph_badge)

        self.at("including LDL")
        dt_go = max(0.6, self.t_of("let go in that") - 0.2 - self.elapsed())
        self.play(h_alpha.animate(run_time=0.35).set_value(0.0),
                  drift_t.animate(run_time=dt_go, rate_func=linear).set_value(drift_t.get_value() + dt_go))

        self.at("let go in that")
        dt_rel = max(0.8, self.t_of("thin tubes sprout") - 0.2 - self.elapsed())
        self.play(FadeIn(lbl_ldl, run_time=0.25),
                  release.animate(run_time=min(1.4, dt_rel), rate_func=smooth).set_value(1.0),
                  drift_t.animate(run_time=dt_rel, rate_func=linear).set_value(drift_t.get_value() + dt_rel))

        self.at("thin tubes sprout")
        rem = max(0.6, self.narration_s + TAIL - self.elapsed())
        self.play(tube_l.animate(run_time=min(1.6, rem), rate_func=smooth).set_value(1.0),
                  FadeIn(lbl_tubes, run_time=0.22),
                  drift_t.animate(run_time=rem, rate_func=linear).set_value(drift_t.get_value() + rem))
        self.finish()


def build_endosome_and_ligands(center=(-3.2, -0.4, 0), rx=1.95, ry=1.35, tube_l=1.40, drift_t=0.0):
    """Helper for s07, s08, s09: acidified Rab5 early endosome with tubules + freed diffusing LDL."""
    shell, pts, perp = make_endosome_shell(center, rx=rx, ry=ry, tube_left=tube_l, tube_right=tube_l, ph=6.2)
    rabs = make_rab5_dots(pts, perp, indices=(70, 120, 175, 225, 290, 340))
    g = VGroup(shell, rabs)
    rng = np.random.default_rng(RNG_SEED)
    phases = rng.uniform(0, TAU, size=5)
    for k in range(5):
        base = np.array([
            center[0] + (k - 2) * 0.48,
            center[1] + 0.28 * np.sin(k * 1.9),
            0.0,
        ])
        pos = base + np.array([
            0.38 * np.sin(1.9 * drift_t + phases[k]),
            0.28 * np.cos(1.5 * drift_t + phases[k]),
            0.0,
        ])
        g.add(Dot(pos, radius=0.115, color=LIGAND))
    return g, pts, perp


class S07TubeGeometry(SpokenScene):
    def construct(self):
        drift_t = ValueTracker(0.0)
        r_ratio = ValueTracker(1.0)

        left_endo = always_redraw(lambda: build_endosome_and_ligands(
            center=(-3.35, -0.25, 0), rx=1.85, ry=1.30, tube_l=1.25, drift_t=drift_t.get_value()
        )[0])
        lbl_left = T("Early endosome (pH 6–6.5)", size=26, color=ACID).move_to([-3.35, -2.55, 0])

        panel = RoundedRectangle(corner_radius=0.18, width=6.1, height=5.9, stroke_color=GREY, stroke_width=2.2,
                                 fill_color=BG, fill_opacity=0.85).move_to([3.3, 0.15, 0])
        head = T("Surface ÷ volume", size=30, color=TEXT).move_to([3.3, 2.65, 0])

        # Sphere radius = 0.60 (diameter = 1.20)
        sph_c = np.array([1.75, 1.45, 0.0])
        sph = Circle(radius=0.60, color=MEMBRANE, stroke_width=3.5, fill_color=ACID, fill_opacity=0.22).move_to(sph_c)
        sph_lbl = T("Sphere: 3 / R", size=26, color=TEXT).move_to([4.42, 1.65, 0])
        sph_val = M("R = 1 → 3", size=26, color=ACID).move_to([4.42, 1.15, 0])

        # Wide horizontal cylinder (width=2.0, diameter=1.20 -> r = R, shrinking to height=0.12 -> r = R/10)
        tube_c = np.array([1.75, -0.15, 0.0])

        def live_tube():
            rr = r_ratio.get_value()
            h = max(0.12, 1.20 * rr)
            return RoundedRectangle(corner_radius=min(0.25, h / 2), width=2.0, height=h,
                                    stroke_color=MEMBRANE, stroke_width=3.5, fill_color=RECYCLE, fill_opacity=0.25).move_to(tube_c)

        tube_mob = always_redraw(live_tube)
        tube_lbl = T("Tube: 2 / r", size=26, color=TEXT).move_to([4.50, 0.15, 0])
        def _tube_live():
            rr = r_ratio.get_value()
            if rr <= 0.105:
                txt = "2 ÷ 0.1 = 20"
            else:
                r_d = round(rr, 2)
                q = 2.0 / r_d
                if abs(q - round(q)) < 1e-6:
                    txt = f"2 ÷ {r_d:.2f} = {q:.0f}"
                elif abs(q - round(q, 1)) < 1e-6:
                    txt = f"2 ÷ {r_d:.2f} = {q:.1f}"
                else:
                    txt = f"2 ÷ {r_d:.2f} ≈ {q:.1f}"
            return M(txt, size=26, color=RECYCLE).move_to([4.52, -0.38, 0])

        tube_live = always_redraw(_tube_live)

        ratio_box = boxed_label("r = R / 10  →  20 vs 3", color=TEXT, size=26).move_to([3.3, -1.35, 0])
        mult_box = boxed_label("≈ 6.7× membrane / fluid", color=RECEPTOR, size=28).move_to([3.3, -2.28, 0])
        body_note = T("Ligands stay in body", size=26, color=LIGAND).move_to([-3.35, 2.35, 0])
        tag = scope_tag("computed geometry")

        self.add(left_endo, lbl_left, panel, head, tag)

        # Continuous ligand drift from t=0 while introducing left endosome & right panel
        dt0 = max(0.8, self.t_of("3 over the radius") - 0.2 - self.elapsed())
        self.play(drift_t.animate(run_time=dt0, rate_func=linear).set_value(dt0))

        self.at("3 over the radius")
        dt1 = max(0.8, self.t_of("2 over the radius") - 0.2 - self.elapsed())
        self.play(FadeIn(sph, run_time=0.45), FadeIn(sph_lbl, run_time=0.45),
                  drift_t.animate(run_time=dt1, rate_func=linear).set_value(drift_t.get_value() + dt1))

        self.at("2 over the radius")
        dt2 = max(0.8, self.t_of("1 tenth") - 0.2 - self.elapsed())
        self.play(FadeIn(tube_mob, run_time=0.45), FadeIn(tube_lbl, run_time=0.45),
                  drift_t.animate(run_time=dt2, rate_func=linear).set_value(drift_t.get_value() + dt2))

        self.at("1 tenth")
        self.play(FadeIn(sph_val, run_time=0.35), FadeIn(tube_live, run_time=0.35),
                  drift_t.animate(run_time=0.35, rate_func=linear).set_value(drift_t.get_value() + 0.35))
        dt3 = max(0.8, self.t_of("is 20 against 3") - 0.2 - self.elapsed())
        self.play(r_ratio.animate(run_time=min(2.0, dt3), rate_func=smooth).set_value(0.1),
                  drift_t.animate(run_time=dt3, rate_func=linear).set_value(drift_t.get_value() + dt3))

        self.at("is 20 against 3")
        dt4 = max(0.8, self.t_of("nearly 7 times") - 0.2 - self.elapsed())
        self.play(FadeIn(ratio_box, run_time=0.45),
                  drift_t.animate(run_time=dt4, rate_func=linear).set_value(drift_t.get_value() + dt4))

        self.at("nearly 7 times")
        dt5 = max(0.8, self.t_of("freed ligands stay mostly") - 0.2 - self.elapsed())
        self.play(FadeIn(mult_box, run_time=0.45),
                  drift_t.animate(run_time=dt5, rate_func=linear).set_value(drift_t.get_value() + dt5))

        self.at("freed ligands stay mostly")
        rem = max(0.5, self.narration_s + TAIL - self.elapsed())
        self.play(FadeIn(body_note, run_time=0.45),
                  drift_t.animate(run_time=rem, rate_func=linear).set_value(drift_t.get_value() + rem))
        self.finish()


def predict_backdrop_group(drift_t=0.0):
    """Exact shared picture for end of s08_predict and all of s09_pause."""
    endo_c = (0.0, 0.25, 0)
    g, pts, perp = build_endosome_and_ligands(center=endo_c, rx=2.40, ry=1.50, tube_l=1.50, drift_t=drift_t)
    idx = 28
    rp = np.array([pts[idx, 0], pts[idx, 1], 0.0])
    out_a = np.arctan2(perp[idx, 1], perp[idx, 0])
    rec = make_receptor(rp, normal_angle=out_a + PI, scale=1.25, has_ligand=False)
    halo = Circle(radius=0.38, color=RECEPTOR, stroke_width=2.5, fill_opacity=0, stroke_opacity=0.75).move_to(rp)
    no_tag_lbl = boxed_label("No tag", color=RECEPTOR, size=28).move_to([4.15, 1.35, 0])
    arr_body = DashedVMobject(
        CurvedArrow(np.array([2.95, 0.65, 0.0]), np.array([2.58, -0.85, 0.0]), angle=-0.40, color=GOLD, stroke_width=4),
        num_dashes=7
    )
    arr_tube = DashedVMobject(
        Arrow(np.array([3.02, 1.70, 0.0]), np.array([3.42, 2.75, 0.0]), color=RECYCLE, stroke_width=4, buff=0),
        num_dashes=7
    )
    g.add(halo, rec, no_tag_lbl, arr_body, arr_tube)
    return g


class S08Predict(SpokenScene):
    def construct(self):
        drift_t = ValueTracker(0.0)
        rec_idx_t = ValueTracker(345.0)
        halo_op = ValueTracker(0.0)
        endo_c = (0.0, 0.25, 0)

        def live_scene():
            g, pts, perp = build_endosome_and_ligands(center=endo_c, rx=2.40, ry=1.50, tube_l=1.50, drift_t=drift_t.get_value())
            idx = int(round(rec_idx_t.get_value())) % len(pts)
            rp = np.array([pts[idx, 0], pts[idx, 1], 0.0])
            out_a = np.arctan2(perp[idx, 1], perp[idx, 0])
            rec = make_receptor(rp, normal_angle=out_a + PI, scale=1.25, has_ligand=False)
            ho = halo_op.get_value()
            if ho > 0.01:
                halo = Circle(radius=0.38, color=RECEPTOR, stroke_width=2.5, fill_opacity=0, stroke_opacity=0.75 * ho).move_to(rp)
                g.add(halo)
            g.add(rec)
            return g

        live_mob = always_redraw(live_scene)
        no_tag_lbl = boxed_label("No tag", color=RECEPTOR, size=28).move_to([4.15, 1.35, 0])
        arr_body = DashedVMobject(
            CurvedArrow(np.array([2.95, 0.65, 0.0]), np.array([2.58, -0.85, 0.0]), angle=-0.40, color=GOLD, stroke_width=4),
            num_dashes=7
        )
        arr_tube = DashedVMobject(
            Arrow(np.array([3.02, 1.70, 0.0]), np.array([3.42, 2.75, 0.0]), color=RECYCLE, stroke_width=4, buff=0),
            num_dashes=7
        )
        qcard = question_card("Round body or thin tube back out?")

        self.add(live_mob)

        dt0 = max(0.8, self.t_of("carries no tag") - 0.2 - self.elapsed())
        self.play(rec_idx_t.animate(run_time=dt0, rate_func=smooth).set_value(388.0),
                  drift_t.animate(run_time=dt0, rate_func=linear).set_value(dt0))

        self.at("carries no tag")
        dt1 = max(1.0, self.t_of("Does it stay") - 0.2 - self.elapsed())
        self.play(halo_op.animate(run_time=0.4).set_value(1.0), FadeIn(no_tag_lbl, run_time=0.4),
                  rec_idx_t.animate(run_time=dt1, rate_func=there_and_back).set_value(396.0),
                  drift_t.animate(run_time=dt1, rate_func=linear).set_value(drift_t.get_value() + dt1))

        self.at("Does it stay")
        rem = max(0.6, self.narration_s + TAIL - self.elapsed())
        self.play(FadeIn(arr_body, run_time=0.35), FadeIn(arr_tube, run_time=0.35), FadeIn(qcard, run_time=0.4),
                  drift_t.animate(run_time=rem, rate_func=linear).set_value(drift_t.get_value() + rem))
        self.finish()


class S09Pause(PredictPause):
    QUESTION = "Round body or thin tube back out?"
    SECONDS = 4.5

    def backdrop(self):
        return predict_backdrop_group(drift_t=0.0)


class S10RecycleReveal(SpokenScene):
    def construct(self):
        walk_t = ValueTracker(0.0)
        tube_grow = ValueTracker(0.0)
        fast_prog = ValueTracker(0.0)
        slow_prog = ValueTracker(0.0)

        xs = np.linspace(-6.1, 6.1, 120)
        y_mem = 2.65
        top_mem = _bilayer_curves(np.stack([xs, np.full_like(xs, y_mem)], axis=1), half_thick=0.10, color=MEMBRANE)
        lbl_mem = T("Plasma membrane", size=26, color=TEXT).move_to([-4.2, 3.25, 0])

        endo_c = (-1.35, -1.35, 0)
        rng = np.random.default_rng(RNG_SEED)
        lig_bases = [np.array([endo_c[0] + dx, endo_c[1] + dy, 0.0]) for dx, dy in
                     [(-0.75, 0.15), (-0.1, -0.35), (0.55, 0.25), (-0.25, 0.45), (0.35, -0.15)]]

        # True fixed-seed 1D random walks for 4 untagged receptors along endosome membrane into distinct positions on tubules
        n_steps = 180
        paths = []
        starts = [310, 330, 225, 200]
        targets = [(305, 398, +1), (315, 378, +1), (138, 230, -1), (152, 220, -1)]
        for cur, (lo, hi, bias) in zip(starts, targets):
            arr = np.zeros(n_steps, dtype=int)
            for s in range(n_steps):
                step = int(rng.choice([-1, bias, bias * 2]))
                cur = int(np.clip(cur + step, lo, hi))
                arr[s] = cur % 360
            paths.append(arr)

        def dynamic_world():
            wt = walk_t.get_value()
            tg = tube_grow.get_value()
            fp = fast_prog.get_value()
            sp = slow_prog.get_value()

            tl_len = 1.25 + 0.55 * tg
            shell, pts, perp = make_endosome_shell(endo_c, rx=2.25, ry=1.35, tube_left=tl_len, tube_right=tl_len + 0.05, ph=6.2)
            rabs = make_rab5_dots(pts, perp, indices=(58, 110, 175, 250, 295))
            g = VGroup(shell, rabs)

            # Freed ligands visibly diffusing inside round body
            for k, lb in enumerate(lig_bases):
                p = lb + np.array([0.36 * np.sin(wt * 1.9 + k * 1.3), 0.26 * np.cos(wt * 1.5 + k * 1.1), 0.0])
                g.add(Dot(p, radius=0.11, color=LIGAND))

            step_i = int(np.clip(wt / 11.7 * (n_steps - 1), 0, n_steps - 1))
            for arr in paths:
                i = int(arr[step_i])
                rp = np.array([pts[i, 0], pts[i, 1], 0.0])
                oa = np.arctan2(perp[i, 1], perp[i, 0])
                g.add(make_receptor(rp, normal_angle=oa + PI, scale=1.05, has_ligand=False))

            # Fast Rab4 path from left tubule tip to just below inner plasma membrane leaflet
            if fp > 0.01:
                p_start = np.array([pts[138, 0], pts[138, 1], 0.0]) + np.array([0.28, 0.22, 0.0])
                p_end = np.array([-0.65, y_mem - 0.58, 0.0])
                pos = p_start + fp * (p_end - p_start)
                tub = RoundedRectangle(corner_radius=0.16, width=0.42, height=0.92, stroke_color=RECYCLE,
                                       stroke_width=3.8, fill_color=RECYCLE, fill_opacity=0.26).move_to(pos)
                rec_f = make_receptor(pos + RIGHT * 0.21, normal_angle=PI, scale=0.82, has_ligand=False)
                g.add(tub, rec_f)

            # Slow Rab4 / Rab11 path: from right tubule tip into recycling compartment, then budding from top edge (y=0.76)
            if sp > 0.01:
                comp = RoundedRectangle(corner_radius=0.35, width=1.40, height=0.82, stroke_color=RECYCLE,
                                        stroke_width=3.2, fill_color=RECYCLE, fill_opacity=0.20).move_to([2.75, 0.35, 0])
                g.add(comp)
                if sp < 0.45:
                    u = sp / 0.45
                    p_tip_r = np.array([pts[42, 0], pts[42, 1], 0.0]) + np.array([0.14, -0.04, 0.0])
                    pos = p_tip_r + u * (np.array([2.75, 0.35, 0.0]) - p_tip_r)
                    alpha_s = float(np.clip(1.0 - max(0.0, u - 0.45) / 0.55, 0.0, 1.0))
                else:
                    u = (sp - 0.45) / 0.55
                    pos = np.array([2.75, 0.76 + 0.15, 0.0]) + u * (np.array([2.75, y_mem - 0.58, 0.0]) - np.array([2.75, 0.76 + 0.15, 0.0]))
                    alpha_s = float(np.clip(u / 0.25, 0.0, 1.0))
                if alpha_s > 0.02:
                    tub_s = RoundedRectangle(corner_radius=0.14, width=0.38, height=0.80, stroke_color=RECYCLE,
                                             stroke_width=3.8, fill_color=RECYCLE, fill_opacity=0.26 * alpha_s).move_to(pos)
                    tub_s.set_stroke(opacity=alpha_s)
                    rec_s = make_receptor(pos + LEFT * 0.19, normal_angle=0.0, scale=0.78, has_ligand=False)
                    rec_s.set_opacity(alpha_s)
                    g.add(tub_s, rec_s)
            return g

        world_mob = always_redraw(dynamic_world)
        arr_win = CurvedArrow([1.65, -0.95, 0], [2.25, 0.55, 0], angle=0.20, color=RECYCLE, stroke_width=5.5)
        lbl_fast = boxed_label("Rab4 (fast: minutes)", color=RECYCLE, size=26).move_to([-4.85, 2.18, 0])
        lbl_rec_comp = T("Recycling compartment", size=24, color=TEXT).move_to([4.48, -0.50, 0])
        lbl_slow = boxed_label("Rab4 / Rab11 (slow: tens of min)", color=RECYCLE, size=24).move_to([3.95, -1.75, 0])
        tag = scope_tag("schematic")

        self.add(top_mem, lbl_mem, world_mob, tag)
        dt0 = max(1.0, self.t_of("wandering receptor usually drifts") - 0.2 - self.elapsed())
        self.play(Create(arr_win, run_time=0.8),
                  tube_grow.animate(run_time=dt0, rate_func=smooth).set_value(0.65),
                  walk_t.animate(run_time=dt0, rate_func=linear).set_value(dt0))

        self.at("wandering receptor usually drifts")
        dt1 = max(1.0, self.t_of("Fast tubes marked") - 0.2 - self.elapsed())
        self.play(FadeOut(arr_win, run_time=0.3),
                  tube_grow.animate(run_time=dt1, rate_func=smooth).set_value(1.0),
                  walk_t.animate(run_time=dt1, rate_func=linear).set_value(walk_t.get_value() + dt1))

        self.at("Fast tubes marked")
        dt2 = max(1.2, self.t_of("A slower route") - 0.2 - self.elapsed())
        self.play(FadeIn(lbl_fast, run_time=0.22),
                  fast_prog.animate(run_time=min(3.2, dt2), rate_func=smooth).set_value(1.0),
                  walk_t.animate(run_time=dt2, rate_func=linear).set_value(walk_t.get_value() + dt2))

        self.at("A slower route")
        rem = max(0.8, self.narration_s + TAIL - self.elapsed())
        self.play(FadeIn(lbl_slow, run_time=0.22), FadeIn(lbl_rec_comp, run_time=0.22),
                  slow_prog.animate(run_time=rem, rate_func=smooth).set_value(1.0),
                  walk_t.animate(run_time=rem, rate_func=linear).set_value(walk_t.get_value() + rem))
        self.finish()


class S11Close(SpokenScene):
    def construct(self):
        cyc = ValueTracker(0.0)

        xs = np.linspace(-6.1, 6.1, 130)
        y_mem = 2.45
        ys = y_mem + _pit_profile(xs, pit_x=-2.7, depth=0.65, width=0.65)
        top_mem = _bilayer_curves(np.stack([xs, ys], axis=1), half_thick=0.10, color=MEMBRANE)
        lbl_mem = T("Plasma membrane", size=26, color=TEXT).move_to([0.0, 3.30, 0])

        endo_c = (0.0, -1.25, 0)
        shell, pts, perp = make_endosome_shell(endo_c, rx=2.45, ry=1.35, tube_left=1.15, tube_right=1.50, ph=6.2)
        rabs = make_rab5_dots(pts, perp, indices=(25, 100, 210, 290, 340))
        lbl_endo = T("Rab5 early endosome", size=26, color=RAB5).move_to([0.0, -3.22, 0])

        arr_in = CurvedArrow([-2.15, 1.72, 0], [-0.85, 0.65, 0], angle=-0.22, color=CLATHRIN, stroke_width=4.5)
        arr_out = CurvedArrow([2.05, 0.95, 0], [2.00, 2.00, 0], angle=0.22, color=RECYCLE, stroke_width=4.5)
        lbl_pit = T("Coated pit", size=26, color=CLATHRIN).move_to([-4.6, 1.05, 0])
        badge_10 = boxed_label("~10 min cycle", color=RECYCLE, size=28).move_to([4.85, 1.05, 0])

        golgi_box = RoundedRectangle(corner_radius=0.22, width=1.65, height=0.85, stroke_color=MEMBRANE,
                                     stroke_width=2.5, fill_color=MEMBRANE, fill_opacity=0.16).move_to([-4.75, -1.35, 0])
        golgi_lbl = T("Golgi", size=26, color=TEXT).move_to(golgi_box)
        arr_golgi = Arrow([-2.55, -1.35, 0], [-3.85, -1.35, 0], color=TEXT, stroke_width=3.5, buff=0)

        rng = np.random.default_rng(RNG_SEED)
        lig_bases = [np.array([dx, -1.30 + dy, 0.0]) for dx, dy in [(-0.75, 0.15), (0.0, -0.25), (0.70, 0.1)]]
        lig_phases = rng.uniform(0, TAU, size=3)

        def moving_cargo():
            ct = cyc.get_value()
            g = VGroup()
            for k, lb in enumerate(lig_bases):
                lp = lb + np.array([0.32 * np.sin(ct * 5.2 + lig_phases[k]), 0.22 * np.cos(ct * 4.2 + lig_phases[k]), 0.0])
                g.add(Dot(lp, radius=0.11, color=LIGAND))

            ves_end = np.array([pts[115, 0], pts[115, 1], 0.0]) + 0.30 * np.array([perp[115, 0], perp[115, 1], 0.0])
            tub_start = np.array([pts[42, 0], pts[42, 1], 0.0]) + np.array([0.12, 0.26, 0.0])

            for offset in (0.0, 0.5):
                u = (ct + offset) % 1.0
                if u < 0.30:
                    s = u / 0.30
                    pos = np.array([-2.7, 1.50, 0.0]) + s * (ves_end - np.array([-2.7, 1.50, 0.0]))
                    coat_op = float(np.clip(1.0 - (s - 0.45) / 0.35, 0.0, 1.0))
                    ves = make_vesicle(pos, radius=0.25, n_receptors=1, has_ligand=True,
                                       coat_color=CLATHRIN if coat_op > 0.02 else None)
                    if coat_op > 0.02:
                        for m in ves[3:]:
                            m.set_opacity(coat_op)
                    g.add(ves)
                elif u < 0.55:
                    # Receptor travels along upper endosome membrane rim (never floating in lumen!)
                    s = (u - 0.30) / 0.25
                    i = int(round(115 - s * 75)) % len(pts)
                    rp = np.array([pts[i, 0], pts[i, 1], 0.0])
                    oa = np.arctan2(perp[i, 1], perp[i, 0])
                    g.add(make_receptor(rp, normal_angle=oa + PI, scale=0.90, has_ligand=False))
                elif u < 0.85:
                    s = (u - 0.55) / 0.30
                    pos = tub_start + s * (np.array([2.75, y_mem - 0.52, 0.0]) - tub_start)
                    tub = RoundedRectangle(corner_radius=0.12, width=0.30, height=0.62, stroke_color=RECYCLE,
                                           stroke_width=3.2, fill_color=RECYCLE, fill_opacity=0.24).move_to(pos)
                    g.add(tub, make_receptor(pos + LEFT * 0.15, normal_angle=0.0, scale=0.68, has_ligand=False))
                else:
                    s = (u - 0.85) / 0.15
                    pos = np.array([2.75, y_mem, 0.0]) + s * (np.array([-2.7, y_mem, 0.0]) - np.array([2.75, y_mem, 0.0]))
                    g.add(make_receptor(pos, normal_angle=PI / 2, scale=0.90, has_ligand=True))
            return g

        cargo_mob = always_redraw(moving_cargo)
        tag = scope_tag("schematic")

        self.add(top_mem, lbl_mem, shell, rabs, lbl_endo, arr_in, arr_out, lbl_pit, cargo_mob, tag)

        dt0 = max(0.8, self.t_of("roughly every 10 minutes") - 0.2 - self.elapsed())
        self.play(cyc.animate(run_time=dt0, rate_func=linear).set_value(0.32))

        self.at("roughly every 10 minutes")
        dt1 = max(0.8, self.t_of("heads to the Golgi") - 0.2 - self.elapsed())
        self.play(FadeIn(badge_10, run_time=0.35), cyc.animate(run_time=dt1, rate_func=linear).set_value(0.70))

        self.at("heads to the Golgi")
        dt2 = max(0.8, self.t_of("Otherwise, early endosomes sort") - 0.2 - self.elapsed())
        self.play(FadeIn(golgi_box, run_time=0.35), FadeIn(golgi_lbl, run_time=0.35), GrowArrow(arr_golgi, run_time=0.45),
                  cyc.animate(run_time=dt2, rate_func=linear).set_value(1.08))

        self.at("Otherwise, early endosomes sort")
        rem = max(0.8, self.narration_s + TAIL - self.elapsed())
        self.play(cyc.animate(run_time=rem, rate_func=lambda x: 0.70 * x + 0.30 * (1 - (1 - x) ** 2)).set_value(1.75))
        self.finish()


class S12End(EndCard):
    LINE = "Early endosomes sort internalized receptors, returning untagged ones to the surface."
