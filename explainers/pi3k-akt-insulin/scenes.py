"""
COLOUR MAP (one colour per concept, carried across the whole film):
  BG          #0F1117  dark background
  TEXT        #E8EAF0  primary labels and text
  GREY        #8B93A1  bilayer leaflets, structural dividers, scope tag
  AMBER       #F59E0B  insulin hormone and transmembrane insulin receptor
  TEAL_IRS    #2DD4BF  IRS-1 docking protein
  SKY         #38BDF8  PI 3-kinase (regulatory + catalytic subunits)
  SLATE       #64748B  PIP2 inner-leaflet lipid tiles (label #94A3B8 on dark BG)
  PIP3_GOLD   #FACC15  PIP3 inner-leaflet lipid tiles (the membrane address)
  PHOS        #FEF08A  phosphate badges (P, 3-P)
  AKT_MUTED   #FB7185  folded, inactive Akt
  AKT_ACTIVE  #F43F5E  unfolded, doubly phosphorylated active Akt
  VIOLET      #A78BFA  PDK1 kinase
  LAVENDER    #C4B5FD  mTORC2 complex
  RED         #FC6255  drug blockade (X mark) and failed-activation status

WORLD CARRIED ACROSS SCENES:
  Schematic cross-section of a muscle cell edge: extracellular space above, plasma membrane
  bilayer across the upper-middle, cytosol below. The camera zooms onto the gold PIP3 patch
  for Akt docking and dual phosphorylation (s04, s05, s10) while keeping the upstream relay
  anchored at the left edge, and zooms back out to show the full relay (s06-s09).

WHAT CHANGES IN EACH SPOKEN SCENE (computed):
  s01_hook:           Seeded 2D random-walk trajectories of insulin orbs bounce elastically off
                      the outer leaflet while folded Akt executes a seeded 2D walk in the cytosol;
                      the inner-leaflet target patch highlights as the lipid address puzzle.
  s02_receptor_irs1:  Insulin docks into the receptor jaws, closing them; receptor tyrosines gain
                      2 P badges and sequentially stamp 3 P badges onto IRS-1's docking tail.
  s03_pi3k_pip3:      Two-block PI 3-kinase glides from cytosol, locks its notched SH2 pockets onto
                      IRS-1's P badges, pivots its regulatory block open 26 deg to expose the
                      catalytic site, and flips 5 slate PIP2 tiles one-by-one into gold PIP3 + 3-P
                      while an inset schematic ring-shaped head adds P at position 3 (PIP2 -> PIP3).
  s04_akt_docking:    Zoomed onto gold PIP3; folded Akt executes a cytosolic random walk, then rises
                      and locks its concave PH pocket cleanly onto the bottom of a gold PIP3 tile.
  s05_two_phosphates: Docked Akt's hinge swings open from 18 deg to 115 deg exposing Thr308; PDK1
                      rises to dock on an adjacent PIP3 and leans to stamp Thr308-P, mTORC2 docks
                      beside the tail to stamp Ser473-P, and Akt shifts to bright coral-red.
  s06_guiding_rule:   Computed signal-relay wave travels left-to-right across the active assembly
                      (receptor -> IRS-1 -> PI3K -> PIP3 -> Akt) while Thr308-P and Ser473-P fire.
  s07_predict_q:      Reset assembly with red X drug block snapping onto PI 3-kinase catalytic block;
                      PIP2 stays slate while folded Akt walks in the cytosol and question card enters.
  s09_predict_reveal: Receptor & IRS-1 stay phosphorylated, PIP2 remains slate (no PIP3), folded Akt
                      walks in the cytosol far from PDK1, and status label confirms Akt stays off.
  s10_closing:        Active assembly restored: Akt docks on PIP3, unfolds, gains Thr308-P (PDK1) and
                      Ser473-P (mTORC2) across the scene in sync with the 3-step safety lock.
"""

from bp_parts import *

# ------------------------------------------------------------------ Film Palette
AMBER = "#F59E0B"
TEAL_IRS = "#2DD4BF"
SKY = "#38BDF8"
SLATE = "#64748B"
SLATE_LBL = "#94A3B8"
PIP3_GOLD = "#FACC15"
PHOS = "#FEF08A"
AKT_MUTED = "#FB7185"
AKT_ACTIVE = "#F43F5E"
VIOLET = "#A78BFA"
LAVENDER = "#C4B5FD"


# ------------------------------------------------------------------ Computed Diffusion Helpers
def compute_walk(seed, start, bounds, n_steps=180, step_len=0.14, bounce_y=None):
    """Compute a deterministic 2D random walk inside bounds=(xmin, xmax, ymin, ymax).
    If bounce_y is given, trajectories reflect cleanly off that horizontal membrane boundary.
    """
    rng = np.random.default_rng(seed)
    xmin, xmax, ymin, ymax = bounds
    pts = [np.array([start[0], start[1], 0.0], dtype=float)]
    bounces = []
    angle = rng.uniform(0, TAU)
    for i in range(n_steps):
        angle += rng.normal(0.0, 0.72)
        dx = step_len * np.cos(angle)
        dy = step_len * np.sin(angle)
        nx = pts[-1][0] + dx
        ny = pts[-1][1] + dy
        if nx < xmin:
            nx = xmin + (xmin - nx)
            angle = np.pi - angle
        elif nx > xmax:
            nx = xmax - (nx - xmax)
            angle = np.pi - angle
        if ny < ymin:
            ny = ymin + (ymin - ny)
            angle = -angle
            if bounce_y == "bottom":
                bounces.append(i + 1)
        elif ny > ymax:
            ny = ymax - (ny - ymax)
            angle = -angle
            if bounce_y == "top":
                bounces.append(i + 1)
        pts.append(np.array([np.clip(nx, xmin, xmax), np.clip(ny, ymin, ymax), 0.0]))
    return np.array(pts), bounces


def eval_walk(pts, u):
    """Linearly interpolate a precomputed walk array at normalized progress u in [0, 1]."""
    u = float(np.clip(u, 0.0, 1.0))
    f = u * (len(pts) - 1)
    idx = int(np.floor(f))
    if idx >= len(pts) - 1:
        return pts[-1].copy()
    frac = f - idx
    return pts[idx] * (1.0 - frac) + pts[idx + 1] * frac


# ------------------------------------------------------------------ Shared World Geometry
def build_bilayer(y_in=0.90, y_out=1.80, x0=-6.1, x1=6.1):
    """Plasma membrane bilayer without Rectangle panels (avoids false panel-outside flags)."""
    band = Polygon(
        [x0, y_in, 0], [x1, y_in, 0], [x1, y_out, 0], [x0, y_out, 0],
        stroke_width=0, fill_color=SLATE, fill_opacity=0.22,
    )
    outer = Line([x0, y_out, 0], [x1, y_out, 0], color=GREY, stroke_width=4.0)
    inner = Line([x0, y_in, 0], [x1, y_in, 0], color=GREY, stroke_width=4.0)
    return VGroup(band, outer, inner)


def make_p_badge(text="P", radius=0.25, pill_w=0.70, pill_h=0.40):
    """Yellow-white phosphate badge with dark high-contrast text (font_size=22) and generous padding."""
    lbl = T(text, size=22, color=BG, weight=BOLD)
    if len(text) <= 1:
        bg = Circle(radius=radius, stroke_color=PHOS, stroke_width=2.0, fill_color=PHOS, fill_opacity=0.98)
    else:
        bg = RoundedRectangle(
            corner_radius=0.14, width=pill_w, height=pill_h,
            stroke_color=PHOS, stroke_width=2.0, fill_color=PHOS, fill_opacity=0.98,
        )
    lbl.move_to(bg.get_center())
    return VGroup(bg, lbl)


def make_insulin_orb(radius=0.23):
    """Warm amber insulin hormone orb."""
    return Circle(radius=radius, stroke_color=AMBER, stroke_width=2.5, fill_color=AMBER, fill_opacity=0.92)


def make_receptor(x=-4.65, y_in=0.90, y_out=1.80, scale=1.0, docked=False, active=False):
    """Transmembrane insulin receptor dimer spanning the bilayer with closing jaws and kinase stalks."""
    jaw_spread = 0.24 if docked else 0.44
    col = AMBER
    fill_op = 0.44 if active else 0.30
    sw = 3.5 if active else 2.6

    left_pts = [
        [-0.22 - jaw_spread, y_out + 0.90, 0],
        [-0.38 - jaw_spread * 0.4, y_out + 0.42, 0],
        [-0.30, y_out, 0],
        [-0.30, y_in - 1.32, 0],
        [-0.06, y_in - 1.32, 0],
        [-0.06, y_out + 0.24, 0],
        [-0.20, y_out + 0.50, 0],
    ]
    right_pts = [
        [0.22 + jaw_spread, y_out + 0.90, 0],
        [0.38 + jaw_spread * 0.4, y_out + 0.42, 0],
        [0.30, y_out, 0],
        [0.30, y_in - 1.32, 0],
        [0.06, y_in - 1.32, 0],
        [0.06, y_out + 0.24, 0],
        [0.20, y_out + 0.50, 0],
    ]
    left_sub = Polygon(*left_pts, stroke_color=col, stroke_width=sw, fill_color=col, fill_opacity=fill_op)
    right_sub = Polygon(*right_pts, stroke_color=col, stroke_width=sw, fill_color=col, fill_opacity=fill_op)

    stalk_l = Line([-0.30, y_in - 0.84, 0], [-0.58, y_in - 0.84, 0], color=col, stroke_width=2.6)
    stalk_r = Line([0.30, y_in - 1.08, 0], [0.58, y_in - 1.08, 0], color=col, stroke_width=2.6)

    g = VGroup(left_sub, right_sub, stalk_l, stalk_r)
    if scale != 1.0:
        g.scale(scale, about_point=[0, (y_in + y_out) / 2, 0])
    g.shift(RIGHT * x)

    g.jaw_center = np.array([x, y_out + 0.58 * scale, 0.0])
    g.p_spots = [
        g[2].get_end() + LEFT * 0.29,
        g[3].get_end() + RIGHT * 0.29,
    ]
    return g


def make_irs1(x=-2.95, y_in=0.90, scale=1.0, active=False):
    """Soft teal IRS-1 docking block anchored below the inner leaflet with 3 tyrosine stalks."""
    sw = 3.2 if active else 2.6
    body = RoundedRectangle(
        corner_radius=0.14, width=0.58, height=1.96,
        stroke_color=TEAL_IRS, stroke_width=sw, fill_color=TEAL_IRS, fill_opacity=0.38 if active else 0.26,
    )
    body.move_to([0, y_in - 1.12, 0])
    stalks = VGroup(*[
        Line([0.29, y_in - 0.44 - i * 0.64, 0], [0.58, y_in - 0.44 - i * 0.64, 0], color=TEAL_IRS, stroke_width=2.6)
        for i in range(3)
    ])
    g = VGroup(body, stalks)
    if scale != 1.0:
        g.scale(scale, about_point=[0, y_in, 0])
    g.shift(RIGHT * x)
    g.p_spots = [s.get_end() + RIGHT * 0.29 for s in g[1]]
    return g


def make_pi3k(pos=(-0.96, -0.5, 0), open_angle=0.0, scale=1.0, blocked=False):
    """Two-block sky-blue PI 3-kinase:
    - Regulatory block (smaller) with two notched SH2 cups on its left face
    - Catalytic block (larger) with an upward-facing active-site notch
    """
    reg_pts = [
        [-0.52, 0.44, 0],
        [0.05, 0.44, 0],
        [0.05, -0.44, 0],
        [-0.52, -0.44, 0],
        [-0.52, -0.30, 0],
        [-0.34, -0.25, 0],
        [-0.34, -0.09, 0],
        [-0.52, -0.04, 0],
        [-0.52, 0.06, 0],
        [-0.34, 0.11, 0],
        [-0.34, 0.27, 0],
        [-0.52, 0.32, 0],
    ]
    reg = Polygon(*reg_pts, stroke_color=SKY, stroke_width=2.6, fill_color=SKY, fill_opacity=0.38)

    cat_pts = [
        [0.08, 0.46, 0],
        [0.50, 0.46, 0],
        [0.54, 0.22, 0],
        [0.80, 0.22, 0],
        [0.84, 0.46, 0],
        [1.16, 0.46, 0],
        [1.16, -0.48, 0],
        [0.08, -0.48, 0],
    ]
    cat = Polygon(*cat_pts, stroke_color=SKY, stroke_width=2.8, fill_color=SKY, fill_opacity=0.44)
    if open_angle != 0.0:
        reg.rotate(-open_angle, about_point=np.array([0.06, 0.34, 0.0]))

    g = VGroup(reg, cat)
    if blocked:
        c = cat.get_center()
        x1 = Line(c + UL * 0.34, c + DR * 0.34, color=RED, stroke_width=6)
        x2 = Line(c + UR * 0.34, c + DL * 0.34, color=RED, stroke_width=6)
        g.add(VGroup(x1, x2))
    if scale != 1.0:
        g.scale(scale)
    g.move_to(pos)
    g.reg = reg
    g.cat = cat
    return g


def make_lipid_tile(x, y_in=0.90, gold=False, width=0.72, height=0.42):
    """One inner-leaflet phospholipid tile.
    The '3-P' badge sits cleanly ABOVE the short lipid tails inside the bilayer band
    so neither the tail lines nor the PH pockets below ever cross the '3-P' pill.
    """
    col = PIP3_GOLD if gold else SLATE
    fill_op = 0.50 if gold else 0.36
    # Short tails end cleanly BELOW the '3-P' badge (y_in + 0.22)
    tail1 = Line([x - 0.14, y_in + 0.02, 0], [x - 0.14, y_in + 0.22, 0], color=col, stroke_width=2.6)
    tail2 = Line([x + 0.14, y_in + 0.02, 0], [x + 0.14, y_in + 0.22, 0], color=col, stroke_width=2.6)
    head = RoundedRectangle(
        corner_radius=0.10, width=width, height=height,
        stroke_color=col, stroke_width=3.0 if gold else 2.4, fill_color=col, fill_opacity=fill_op,
    ).move_to([x, y_in - height / 2 - 0.02, 0])
    g = VGroup(tail1, tail2, head)
    if gold:
        # Placed at y_in + 0.50 (bottom at y_in + 0.30, clear of tail tips at y_in + 0.22)
        badge = make_p_badge("3-P").move_to([x, y_in + 0.50, 0])
        g.add(badge)
        g.badge = badge
    g.head = head
    return g


def make_akt(pos=(0.0, -1.5, 0), fold_deg=18.0, active=False, scale=1.0):
    """Articulated Akt with:
    - PH domain (upper block with concave semi-circular pocket facing UP toward PIP3)
    - Kinase lobe + activation loop (Thr308) hinged at right
    - C-terminal tail (Ser473) extending downward-right into the cytosol when unfolded
    """
    col = AKT_ACTIVE if active else AKT_MUTED
    sw = 3.5 if active else 2.6
    fill_op = 0.48 if active else 0.34

    ph_pts = [
        [-0.44, 0.42, 0],
        [-0.22, 0.42, 0],
        [-0.18, 0.18, 0],
        [0.0, 0.12, 0],
        [0.18, 0.18, 0],
        [0.22, 0.42, 0],
        [0.44, 0.42, 0],
        [0.44, -0.18, 0],
        [-0.44, -0.18, 0],
    ]
    ph = Polygon(*ph_pts, stroke_color=col, stroke_width=sw, fill_color=col, fill_opacity=fill_op)

    hinge = np.array([0.36, -0.14, 0.0])
    linker = Line(hinge, [0.22, -0.34, 0], color=col, stroke_width=5.0)
    kin = RoundedRectangle(
        corner_radius=0.18, width=0.96, height=0.64,
        stroke_color=col, stroke_width=sw, fill_color=col, fill_opacity=fill_op,
    ).move_to([-0.14, -0.60, 0])

    loop_arc = Arc(radius=0.16, start_angle=0, angle=PI, arc_center=[-0.16, -0.28, 0], color=col, stroke_width=3.0)
    loop_stalk = Line([-0.16, -0.12, 0], [-0.16, 0.10, 0], color=col, stroke_width=2.4)

    # Tail built so when kinase_grp swings +97 deg (fold_deg=115), tail extends RIGHT-DOWN into cytosol
    tail = VMobject(color=col, stroke_width=3.2)
    tail.set_points_smoothly([
        np.array([-0.14, -0.92, 0]),
        np.array([-0.20, -1.24, 0]),
        np.array([-0.04, -1.50, 0]),
    ])

    kinase_grp = VGroup(linker, kin, loop_arc, loop_stalk, tail)
    swing = (fold_deg - 18.0) * DEGREES
    if abs(swing) > 1e-4:
        kinase_grp.rotate(swing, about_point=hinge)

    g = VGroup(ph, kinase_grp)
    if scale != 1.0:
        g.scale(scale)
    g.move_to(pos)
    g.ph = ph
    g.kinase_grp = kinase_grp
    g.kin = kin
    g.loop_pt = loop_stalk.get_end()
    g.tail_pt = tail.get_end()
    return g


def make_pdk1(pos=(-1.8, 0.4, 0), lean=0.0, scale=1.0):
    """Violet PDK1 anchored by its own PH pocket on PIP3, with a kinase arm that leans toward Akt."""
    ph_pts = [
        [-0.36, 0.34, 0],
        [-0.18, 0.34, 0],
        [-0.14, 0.14, 0],
        [0.0, 0.08, 0],
        [0.14, 0.14, 0],
        [0.18, 0.34, 0],
        [0.36, 0.34, 0],
        [0.36, -0.14, 0],
        [-0.36, -0.14, 0],
    ]
    ph = Polygon(*ph_pts, stroke_color=VIOLET, stroke_width=2.6, fill_color=VIOLET, fill_opacity=0.42)
    linker = Line([0.10, -0.11, 0], [0.14, -0.28, 0], color=VIOLET, stroke_width=5.0)
    arm = RoundedRectangle(
        corner_radius=0.14, width=0.68, height=0.46,
        stroke_color=VIOLET, stroke_width=2.6, fill_color=VIOLET, fill_opacity=0.46,
    ).move_to([0.22, -0.46, 0])
    if lean != 0.0:
        for m in (linker, arm):
            m.rotate(lean, about_point=np.array([0.10, -0.16, 0]))
    g = VGroup(ph, linker, arm)
    if scale != 1.0:
        g.scale(scale)
    g.move_to(pos)
    g.ph = ph
    g.arm = arm
    return g


def make_mtorc2(pos=(4.9, -1.2, 0), scale=1.0):
    """Lavender mTORC2 complex docking beside Akt's C-terminal tail."""
    body = RoundedRectangle(
        corner_radius=0.22, width=1.24, height=0.70,
        stroke_color=LAVENDER, stroke_width=2.6, fill_color=LAVENDER, fill_opacity=0.40,
    )
    notch = Arc(radius=0.15, start_angle=PI / 2, angle=PI, arc_center=body.get_left() + RIGHT * 0.05,
                color=LAVENDER, stroke_width=2.8)
    g = VGroup(body, notch)
    if scale != 1.0:
        g.scale(scale)
    g.move_to(pos)
    return g


def akt_dock_pos_for_tile(tile, akt_scale=1.0):
    """Compute Akt center position so its PH cup cradles the bottom of `tile.head` cleanly."""
    probe = make_akt(pos=ORIGIN, fold_deg=18.0, scale=akt_scale)
    cup_top_offset = probe.ph.get_top()[1] - probe.get_center()[1]
    target_y = tile.head.get_bottom()[1] - cup_top_offset + 0.14 * akt_scale
    return np.array([tile.head.get_center()[0], target_y, 0.0])


def pdk1_dock_pos_for_tile(tile, pdk_scale=1.0):
    """Compute PDK1 center position so its PH cup cradles the bottom of `tile.head` cleanly."""
    probe = make_pdk1(pos=ORIGIN, lean=0.0, scale=pdk_scale)
    cup_top_offset = probe.ph.get_top()[1] - probe.get_center()[1]
    target_y = tile.head.get_bottom()[1] - cup_top_offset + 0.12 * pdk_scale
    return np.array([tile.head.get_center()[0], target_y, 0.0])


def build_overview_world(
    y_in=0.95, y_out=1.85,
    insulin_docked=True,
    rec_p=True,
    irs_p=True,
    pi3k_docked=True,
    pi3k_open=True,
    pi3k_blocked=False,
    n_pip3=5,
    akt_docked=False,
    akt_active=False,
    show_pdk1=False,
    show_mtorc2=False,
):
    """Build the full cell-edge assembly in consistent world coordinates."""
    bilayer = build_bilayer(y_in=y_in, y_out=y_out, x0=-6.1, x1=6.1)
    rec = make_receptor(x=-4.65, y_in=y_in, y_out=y_out, scale=0.94, docked=insulin_docked, active=rec_p)
    irs = make_irs1(x=-2.95, y_in=y_in, scale=0.94, active=irs_p)

    tile_xs = [0.70 + i * 0.90 for i in range(5)]
    tiles = VGroup(*[make_lipid_tile(tx, y_in=y_in, gold=(i < n_pip3), width=0.70, height=0.40) for i, tx in enumerate(tile_xs)])

    extras = VGroup()
    if insulin_docked:
        ins = make_insulin_orb(0.20).move_to(rec.jaw_center)
        extras.add(ins)
    if rec_p:
        for sp in rec.p_spots:
            extras.add(make_p_badge("P", radius=0.23).move_to(sp))
    if irs_p:
        for sp in irs.p_spots:
            extras.add(make_p_badge("P", radius=0.23).move_to(sp))

    if pi3k_docked:
        pi3k = make_pi3k(pos=(-0.92, y_in - 0.65, 0), open_angle=0.40 if pi3k_open else 0.0, scale=0.84, blocked=pi3k_blocked)
    else:
        pi3k = make_pi3k(pos=(0.3, -1.55, 0), open_angle=0.0, scale=0.84, blocked=pi3k_blocked)

    akt_p_badges = VGroup()
    if akt_docked:
        fold = 115.0 if akt_active else 18.0
        probe = make_akt(pos=ORIGIN, fold_deg=fold, scale=0.88)
        ph_offset = probe.ph.get_center() - probe.get_center()
        cup_top_offset = probe.ph.get_top()[1] - probe.get_center()[1]
        target_y = tiles[2].head.get_bottom()[1] - cup_top_offset + 0.14 * 0.88
        dpos = np.array([tiles[2].head.get_center()[0] - ph_offset[0], target_y, 0.0])
        akt = make_akt(pos=dpos, fold_deg=fold, active=akt_active, scale=0.88)
        if akt_active:
            p1 = make_p_badge("P", radius=0.23).next_to(akt.loop_pt, LEFT, buff=0.14)
            p2 = make_p_badge("P", radius=0.23).next_to(akt.tail_pt, RIGHT, buff=0.14)
            akt_p_badges.add(p1, p2)
    else:
        akt = make_akt(pos=(2.5, -1.55, 0), fold_deg=18.0, active=False, scale=0.88)

    pdk1 = VGroup()
    if show_pdk1:
        ppos = pdk1_dock_pos_for_tile(tiles[0], pdk_scale=0.80)
        if n_pip3 == 0:
            ppos = ppos + DOWN * 0.45
        pdk1 = make_pdk1(pos=ppos, lean=0.30 if akt_active else 0.0, scale=0.80)

    mtorc2 = make_mtorc2(pos=(4.95, -1.10, 0), scale=0.80) if show_mtorc2 else VGroup()

    world = VGroup(bilayer, tiles, rec, irs, pi3k, extras, pdk1, mtorc2, akt, akt_p_badges)
    world.bilayer = bilayer
    world.tiles = tiles
    world.rec = rec
    world.irs = irs
    world.pi3k = pi3k
    world.extras = extras
    world.akt = akt
    world.akt_p_badges = akt_p_badges
    world.pdk1 = pdk1
    world.mtorc2 = mtorc2
    world.tile_xs = tile_xs
    return world


# ================================================================== Scenes
class S00Title(TitleCard):
    LESSON = "PI 3-Kinase, Akt and Insulin"
    TITLE = "Writing a Membrane Address for Akt"


class S01Hook(SpokenScene):
    def construct(self):
        y_in, y_out = 0.90, 1.80
        bilayer = build_bilayer(y_in=y_in, y_out=y_out)
        rec = make_receptor(x=-4.65, y_in=y_in, y_out=y_out, scale=0.94, docked=False, active=False)
        tiles = VGroup(*[make_lipid_tile(0.70 + i * 0.90, y_in=y_in, gold=False, width=0.70, height=0.40) for i in range(5)])

        extra_lbl = T("extracellular space", size=26, color=GREY).move_to([-4.3, 3.28, 0])
        cyto_lbl = T("cytosol", size=26, color=GREY).move_to([-5.0, -3.05, 0])
        stag = scope_tag("schematic")

        # Insulin walks confined below y = 2.80 so they never cross top labels
        ins_walks = [
            compute_walk(7 + i, start=(-1.4 + i * 1.8, 2.38), bounds=(-2.8, 5.4, y_out + 0.30, 2.82), n_steps=180, step_len=0.15, bounce_y="bottom")[0]
            for i in range(4)
        ]
        akt_walk, _ = compute_walk(17, start=(1.4, -1.65), bounds=(-1.2, 4.2, -2.15, -1.05), n_steps=180, step_len=0.12)

        t_sim = ValueTracker(0.0)
        ins_orbs = VGroup(*[make_insulin_orb(0.22).move_to(ins_walks[i][0]) for i in range(4)])
        for i, orb in enumerate(ins_orbs):
            orb.add_updater(lambda m, idx=i: m.move_to(eval_walk(ins_walks[idx], t_sim.get_value())))

        akt = make_akt(pos=akt_walk[0], fold_deg=18.0, active=False, scale=0.92)
        akt_lbl = T("Akt (inactive)", size=28, color=AKT_MUTED).next_to(akt, DOWN, buff=0.22)
        akt.add_updater(lambda m: m.move_to(eval_walk(akt_walk, t_sim.get_value())))
        akt_lbl.add_updater(lambda m: m.next_to(akt, DOWN, buff=0.22))

        # Placed cleanly in the upper-center band (y = 3.28), clear of extra_lbl and ins_walks (ymax 2.82)
        ins_lbl = T("insulin", size=28, color=AMBER).move_to([0.4, 3.28, 0])

        self.add(bilayer, tiles, rec, extra_lbl, cyto_lbl, stag, ins_orbs, ins_lbl, akt, akt_lbl)

        self.at("never crosses")
        self.play(t_sim.animate.set_value(0.34), run_time=max(1.0, self.t_of("How does a hormone") - self.elapsed() - 0.25), rate_func=linear)

        self.at("How does a hormone")
        q_arrow = DashedLine([0.2, 2.05, 0], [0.8, -0.45, 0], color=TEXT, stroke_width=3.0, dash_length=0.14)
        q_mark = T("?", size=38, color=PIP3_GOLD, weight=BOLD).move_to([1.25, 0.15, 0])
        self.play(
            FadeIn(q_arrow), FadeIn(q_mark),
            t_sim.animate.set_value(0.68),
            run_time=max(1.0, self.t_of("writing a temporary lipid") - self.elapsed() - 0.25),
            rate_func=linear,
        )

        self.at("writing a temporary lipid")
        patch_box = DashedVMobject(
            RoundedRectangle(corner_radius=0.14, width=4.55, height=0.68, stroke_color=PIP3_GOLD, stroke_width=3.0)
            .move_to([2.50, y_in - 0.22, 0]),
            num_dashes=26,
        )
        addr_lbl = T("membrane address?", size=28, color=PIP3_GOLD).move_to([2.50, y_in - 0.92, 0])
        self.play(
            FadeOut(q_arrow), FadeOut(q_mark),
            t_sim.animate.set_value(0.72),
            run_time=0.4,
            rate_func=linear,
        )
        self.play(
            Create(patch_box), FadeIn(addr_lbl),
            t_sim.animate.set_value(0.90),
            run_time=1.9,
            rate_func=linear,
        )
        rest = max(0.2, self.narration_s + 0.35 - self.elapsed())
        self.play(t_sim.animate.set_value(1.0), run_time=rest, rate_func=linear)
        self.finish()


class S02ReceptorIrs1(SpokenScene):
    def construct(self):
        y_in, y_out = 0.95, 1.85
        bilayer = build_bilayer(y_in=y_in, y_out=y_out)
        rec = make_receptor(x=-4.65, y_in=y_in, y_out=y_out, scale=0.94, docked=False, active=False)
        irs = make_irs1(x=-2.95, y_in=y_in, scale=0.94, active=False)
        tiles = VGroup(*[make_lipid_tile(0.70 + i * 0.90, y_in=y_in, gold=False, width=0.70, height=0.40) for i in range(5)])

        extra_lbl = T("extracellular space", size=26, color=GREY).move_to([-4.3, 3.32, 0])
        cyto_lbl = T("cytosol", size=26, color=GREY).move_to([-5.0, -3.05, 0])
        stag = scope_tag("schematic")

        bg_walks = [
            compute_walk(21 + i, start=(0.8 + i * 2.1, 2.55), bounds=(-1.2, 5.4, y_out + 0.32, 3.15), n_steps=180, step_len=0.13, bounce_y="bottom")[0]
            for i in range(2)
        ]
        t_bg = ValueTracker(0.0)
        bg_orbs = VGroup(*[make_insulin_orb(0.21).move_to(bg_walks[i][0]) for i in range(2)])
        for i, orb in enumerate(bg_orbs):
            orb.add_updater(lambda m, idx=i: m.move_to(eval_walk(bg_walks[idx], t_bg.get_value())))

        dock_ins = make_insulin_orb(0.20).move_to([-2.45, 2.55, 0])
        ins_lbl = T("insulin", size=28, color=AMBER).next_to(dock_ins, RIGHT, buff=0.22)

        self.add(bilayer, tiles, rec, irs, extra_lbl, cyto_lbl, stag, bg_orbs, dock_ins, ins_lbl)

        self.at("Amber insulin docks")
        rec_docked = make_receptor(x=-4.65, y_in=y_in, y_out=y_out, scale=0.94, docked=True, active=False)
        self.play(
            dock_ins.animate.move_to(rec_docked.jaw_center),
            FadeOut(ins_lbl),
            Transform(rec, rec_docked),
            t_bg.animate.set_value(0.28),
            run_time=max(1.8, self.t_of("tyrosine kinase") - self.elapsed() - 0.25),
        )

        self.at("tyrosine kinase")
        rec_active = make_receptor(x=-4.65, y_in=y_in, y_out=y_out, scale=0.94, docked=True, active=True)
        rec_lbl = T("receptor\n(tyrosine kinase)", size=26, color=AMBER).move_to([-4.95, -1.95, 0])
        self.play(
            Transform(rec, rec_active),
            FadeIn(rec_lbl),
            t_bg.animate.set_value(0.46),
            run_time=max(1.4, self.t_of("own tyrosines") - self.elapsed() - 0.25),
        )

        self.at("own tyrosines")
        rec_badges = VGroup(*[make_p_badge("P", radius=0.23).move_to(sp) for sp in rec_active.p_spots])
        self.play(
            FadeIn(rec_badges[0], scale=0.7), FadeIn(rec_badges[1], scale=0.7),
            t_bg.animate.set_value(0.56),
            run_time=max(1.0, self.t_of("nearby docking protein") - self.elapsed() - 0.25),
        )

        self.at("nearby docking protein")
        irs_active = make_irs1(x=-2.95, y_in=y_in, scale=0.94, active=True)
        irs_lbl = T("IRS-1", size=28, color=TEAL_IRS).move_to([-2.70, -1.90, 0])
        self.play(
            Transform(irs, irs_active), FadeIn(irs_lbl),
            t_bg.animate.set_value(0.66),
            run_time=max(1.0, self.t_of("IRS1") - self.elapsed() - 0.25),
        )

        self.at("IRS1")
        irs_badges = VGroup(*[make_p_badge("P", radius=0.23).move_to(sp) for sp in irs_active.p_spots])
        for k, b in enumerate(irs_badges):
            spark = Dot(rec_active.p_spots[1], radius=0.09, color=PHOS)
            self.add(spark)
            self.play(
                spark.animate.move_to(irs_active.p_spots[k]),
                t_bg.animate.set_value(0.72 + 0.06 * k),
                run_time=0.65,
            )
            self.remove(spark)
            self.play(FadeIn(b, scale=0.7), run_time=0.55)

        self.at("busy landing pad")
        pad_lbl = T("landing pad", size=28, color=PHOS).move_to([-0.55, -0.75, 0])
        self.play(FadeIn(pad_lbl), t_bg.animate.set_value(0.95), run_time=1.3)
        rest = max(0.15, self.narration_s + 0.35 - self.elapsed())
        self.play(t_bg.animate.set_value(1.0), run_time=rest, rate_func=linear)
        self.finish()


class S03Pi3kPip3(SpokenScene):
    def construct(self):
        y_in, y_out = 0.95, 1.85
        w = build_overview_world(
            y_in=y_in, y_out=y_out,
            insulin_docked=True, rec_p=True, irs_p=True,
            pi3k_docked=False, pi3k_open=False, n_pip3=0,
        )
        rec_lbl = T("receptor", size=26, color=AMBER).move_to([-4.65, -1.90, 0])
        irs_lbl = T("IRS-1", size=28, color=TEAL_IRS).move_to([-2.95, -1.90, 0])
        pi3k_lbl = T("PI 3-kinase", size=28, color=SKY).next_to(w.pi3k, DOWN, buff=0.22)
        pip_lbl = T("PIP2", size=28, color=SLATE_LBL).move_to([2.80, y_in + 1.32, 0])
        stag = scope_tag("schematic")

        # Keep diffusing insulin orbs strictly in x in [-2.6, 1.4] so they never overlap PIP2/PIP3 on the right
        bg_walks = [
            compute_walk(31 + i, start=(-1.8 + i * 1.6, 2.55), bounds=(-2.8, 1.3, y_out + 0.32, 3.20), n_steps=200, step_len=0.14, bounce_y="bottom")[0]
            for i in range(2)
        ]
        t_bg = ValueTracker(0.0)
        bg_orbs = VGroup(*[make_insulin_orb(0.21).move_to(bg_walks[i][0]) for i in range(2)])
        for i, orb in enumerate(bg_orbs):
            orb.add_updater(lambda m, idx=i: m.move_to(eval_walk(bg_walks[idx], t_bg.get_value())))

        self.add(w.bilayer, w.tiles, w.rec, w.irs, w.extras, w.pi3k, rec_lbl, irs_lbl, pi3k_lbl, pip_lbl, stag, bg_orbs)

        self.at("kinase arrives")
        approach_pos = np.array([-0.75, y_in - 0.80, 0.0])
        self.play(
            w.pi3k.animate.move_to(approach_pos),
            pi3k_lbl.animate.move_to([-0.85, -1.90, 0]),
            t_bg.animate.set_value(0.16),
            run_time=max(1.5, self.t_of("regulatory subunit grips") - self.elapsed() - 0.25),
        )

        self.at("regulatory subunit grips")
        sh2_lbl = T("SH2 domains", size=26, color=SKY).move_to([-0.85, -2.50, 0])
        dock_pos = np.array([-0.92, y_in - 0.65, 0.0])
        self.play(
            w.pi3k.animate.move_to(dock_pos),
            FadeIn(sh2_lbl),
            t_bg.animate.set_value(0.32),
            run_time=3.2,
        )
        rem_pull = max(1.0, self.t_of("loosens its regulatory") - self.elapsed() - 0.25)
        self.play(
            w.pi3k.animate.shift(UP * 0.05),
            t_bg.animate.set_value(0.52),
            run_time=rem_pull,
            rate_func=linear,
        )

        self.at("loosens its regulatory")
        pi3k_open = make_pi3k(pos=w.pi3k.get_center(), open_angle=0.40, scale=0.84)
        self.play(
            Transform(w.pi3k, pi3k_open),
            FadeOut(sh2_lbl),
            t_bg.animate.set_value(0.64),
            run_time=max(1.6, self.t_of("catalytic subunit adds") - self.elapsed() - 0.25),
        )

        self.at("catalytic subunit adds")
        new_lbl = T("PIP2 -> PIP3", size=28, color=PIP3_GOLD).move_to([2.80, y_in + 1.32, 0])

        # Inset schematic of the lipid's ring-shaped head with positions 3, 4, 5 numbered
        inset_box = RoundedRectangle(
            corner_radius=0.16, width=5.20, height=2.76,
            stroke_color=GREY, stroke_width=2.2, fill_color=BG, fill_opacity=0.94,
        ).move_to([3.35, -1.35, 0])
        inset_tag = T("head ring\n(schematic)", size=24, color=TEXT, line_spacing=0.85).move_to([1.82, -0.52, 0])
        ring_c = np.array([3.50, -1.38, 0.0])
        head_ring = Circle(radius=0.40, stroke_color=SLATE_LBL, stroke_width=5.5, fill_color=SLATE, fill_opacity=0.28).move_to(ring_c)
        num3 = T("3", size=24, color=TEXT).move_to([2.82, -1.38, 0])
        num4 = T("4", size=24, color=TEXT).move_to([3.50, -0.74, 0])
        num5 = T("5", size=24, color=TEXT).move_to([4.18, -1.38, 0])
        p4_badge = make_p_badge("P", radius=0.21).move_to([3.50, -0.30, 0])
        p5_badge = make_p_badge("P", radius=0.21).move_to([4.76, -1.38, 0])
        p3_pos = np.array([2.24, -1.38, 0.0])
        p3_slot = DashedVMobject(
            Circle(radius=0.21, stroke_color=PIP3_GOLD, stroke_width=2.4),
            num_dashes=10,
        ).move_to(p3_pos)
        inset_lbl = T("PIP2 (P on 4, 5)", size=26, color=SLATE_LBL).move_to([3.35, -2.30, 0])
        inset_base = VGroup(inset_box, inset_tag, head_ring, num3, num4, num5, p4_badge, p5_badge, inset_lbl)

        self.play(
            swap(pip_lbl, new_lbl, run_time=0.6),
            FadeIn(inset_base),
            t_bg.animate.set_value(0.68),
        )
        pip_lbl = new_lbl

        def flip_tile(idx, bg_val):
            gold_tile = make_lipid_tile(w.tile_xs[idx], y_in=y_in, gold=True, width=0.70, height=0.40)
            spark = Dot(w.pi3k.cat.get_top(), radius=0.09, color=PHOS)
            self.add(spark)
            self.play(
                spark.animate.move_to(gold_tile.head.get_center()),
                t_bg.animate.set_value(bg_val),
                run_time=0.35,
            )
            self.remove(spark)
            self.play(Transform(w.tiles[idx], gold_tile), run_time=0.60)

        flip_tile(0, 0.71)

        self.at("position 3")
        self.play(Create(p3_slot), num3.animate.set_color(PIP3_GOLD), t_bg.animate.set_value(0.74), run_time=0.55)
        flip_tile(1, 0.77)
        flip_tile(2, 0.80)

        self.at("PIP2")
        flip_tile(3, 0.85)
        self.play(
            p4_badge.animate(rate_func=there_and_back).scale(1.16),
            p5_badge.animate(rate_func=there_and_back).scale(1.16),
            t_bg.animate.set_value(0.90),
            run_time=max(0.5, self.t_of("becomes gold") - self.elapsed() - 0.25),
        )

        self.at("becomes gold")
        p3_badge = make_p_badge("P", radius=0.21).move_to(p3_pos)
        head_ring_gold = Circle(radius=0.40, stroke_color=PIP3_GOLD, stroke_width=5.5, fill_color=PIP3_GOLD, fill_opacity=0.28).move_to(ring_c)
        inset_lbl_pip3 = T("PIP3 (P on 3, 4, 5)", size=26, color=PIP3_GOLD).move_to([3.35, -2.30, 0])
        gold_tile4 = make_lipid_tile(w.tile_xs[4], y_in=y_in, gold=True, width=0.70, height=0.40)
        self.play(
            Transform(w.tiles[4], gold_tile4),
            FadeOut(p3_slot),
            FadeIn(p3_badge, scale=0.6),
            Transform(head_ring, head_ring_gold),
            swap(inset_lbl, inset_lbl_pip3, run_time=0.7),
            t_bg.animate.set_value(0.95),
            run_time=0.95,
        )
        rest = max(0.4, self.narration_s + 0.35 - self.elapsed())
        self.play(
            w.tiles.animate.shift(UP * 0.04),
            t_bg.animate.set_value(1.0),
            run_time=rest,
            rate_func=there_and_back,
        )
        self.finish()


class S04AktDocking(SpokenScene):
    def construct(self):
        y_in, y_out = 1.45, 2.35
        bilayer = build_bilayer(y_in=y_in, y_out=y_out)

        rec = make_receptor(x=-5.35, y_in=y_in, y_out=y_out, scale=0.74, docked=True, active=True)
        rec_idle = make_receptor(x=-5.35, y_in=y_in, y_out=y_out, scale=0.74, docked=False, active=False)
        rec_active = make_receptor(x=-5.35, y_in=y_in, y_out=y_out, scale=0.74, docked=True, active=True)
        ins = make_insulin_orb(0.16).move_to(rec.jaw_center)
        irs = make_irs1(x=-4.10, y_in=y_in, scale=0.74, active=True)
        pi3k = make_pi3k(pos=(-2.80, y_in - 0.50, 0), open_angle=0.40, scale=0.70)
        pi3k_closed = make_pi3k(pos=(-2.80, y_in - 0.50, 0), open_angle=0.0, scale=0.70)
        pi3k_open = make_pi3k(pos=(-2.80, y_in - 0.50, 0), open_angle=0.40, scale=0.70)
        left_ctx = VGroup(rec, irs, pi3k)
        for grp in (left_ctx, ins, rec_idle, rec_active, pi3k_closed, pi3k_open):
            for m in grp.family_members_with_points():
                m.set_opacity(0.60)
        ctx_lbl = T("PI 3-kinase", size=24, color=SKY).move_to([-2.95, -0.55, 0])

        tile_xs = [-0.65, 0.80, 2.25, 3.70]
        tiles = VGroup(*[make_lipid_tile(tx, y_in=y_in, gold=True, width=1.00, height=0.52) for tx in tile_xs])
        tile_badges = VGroup(*[t.badge for t in tiles])
        for t, b in zip(tiles, tile_badges):
            t.remove(b)
        pip3_lbl = T("PIP3 (membrane address)", size=30, color=PIP3_GOLD).move_to([1.52, y_in + 1.30, 0])

        akt_walk, _ = compute_walk(41, start=(0.9, -1.65), bounds=(-1.0, 4.2, -2.15, -0.75), n_steps=180, step_len=0.12)
        t_walk = ValueTracker(0.0)
        akt = make_akt(pos=akt_walk[0], fold_deg=18.0, active=False, scale=1.10)
        akt_lbl = T("Akt (folded)", size=28, color=AKT_MUTED).next_to(akt, DOWN, buff=0.22)
        akt.add_updater(lambda m: m.move_to(eval_walk(akt_walk, t_walk.get_value())))
        akt_lbl.add_updater(lambda m: m.next_to(akt, DOWN, buff=0.22))

        stag = scope_tag("schematic")
        self.add(bilayer, left_ctx, ins, ctx_lbl, tiles, tile_badges, akt, akt_lbl, stag)

        self.at("gold lipid patch")
        self.play(FadeIn(pip3_lbl), t_walk.animate.set_value(0.14), run_time=0.8, rate_func=linear)
        self.play(
            t_walk.animate.set_value(0.24),
            run_time=max(0.5, self.t_of("Before insulin arrives") - self.elapsed() - 0.25),
            rate_func=linear,
        )

        self.at("Before insulin arrives")
        slate_tiles = VGroup(*[make_lipid_tile(tx, y_in=y_in, gold=False, width=1.00, height=0.52) for tx in tile_xs])
        self.play(
            FadeOut(ins),
            FadeOut(tile_badges),
            FadeOut(pip3_lbl),
            Transform(tiles, slate_tiles),
            Transform(rec, rec_idle),
            Transform(pi3k, pi3k_closed),
            t_walk.animate.set_value(0.32),
            run_time=0.8,
            rate_func=linear,
        )
        self.play(
            t_walk.animate.set_value(0.56),
            run_time=max(0.6, self.t_of("activation loop hidden") - self.elapsed() - 0.25),
            rate_func=linear,
        )

        self.at("activation loop hidden")
        hidden_lbl = T("loop hidden inside", size=26, color=TEXT).move_to([4.05, -1.20, 0])
        self.play(FadeIn(hidden_lbl), t_walk.animate.set_value(0.60), run_time=0.6, rate_func=linear)
        self.play(
            t_walk.animate.set_value(0.72),
            run_time=max(0.5, self.t_of("lipid binding") - self.elapsed() - 0.25),
            rate_func=linear,
        )

        self.at("lipid binding")
        self.play(FadeOut(hidden_lbl), t_walk.animate.set_value(0.76), run_time=0.5, rate_func=linear)
        ph_lbl = T("PH domain", size=28, color=AKT_MUTED).next_to(akt.ph, RIGHT, buff=0.42).shift(DOWN * 0.14)
        ph_leader = Line(
            akt.ph.get_right() + RIGHT * 0.05 + DOWN * 0.14,
            ph_lbl.get_left() + LEFT * 0.05,
            color=AKT_MUTED, stroke_width=2.5,
        )
        ph_lbl.add_updater(lambda m: m.next_to(akt.ph, RIGHT, buff=0.42).shift(DOWN * 0.14))
        ph_leader.add_updater(lambda m: m.put_start_and_end_on(
            akt.ph.get_right() + RIGHT * 0.05 + DOWN * 0.14,
            ph_lbl.get_left() + LEFT * 0.05,
        ))
        self.play(FadeIn(ph_lbl), FadeIn(ph_leader), t_walk.animate.set_value(0.80), run_time=0.6, rate_func=linear)
        self.play(
            t_walk.animate.set_value(0.91),
            run_time=max(0.5, self.t_of("When the gold patch") - self.elapsed() - 0.25),
            rate_func=linear,
        )

        self.at("When the gold patch")
        gold_tiles = VGroup(*[make_lipid_tile(tx, y_in=y_in, gold=True, width=1.00, height=0.52) for tx in tile_xs])
        new_badges = VGroup(*[t.badge for t in gold_tiles])
        for t, b in zip(gold_tiles, new_badges):
            t.remove(b)
        ins_restored = make_insulin_orb(0.16).move_to(rec_active.jaw_center)
        for m in ins_restored.family_members_with_points():
            m.set_opacity(0.60)
        self.play(
            FadeIn(ins_restored),
            Transform(rec, rec_active),
            Transform(pi3k, pi3k_open),
            Transform(tiles, gold_tiles),
            FadeIn(new_badges),
            t_walk.animate.set_value(0.96),
            run_time=0.85,
            rate_func=linear,
        )
        self.play(
            FadeIn(pip3_lbl),
            t_walk.animate.set_value(1.0),
            run_time=max(0.5, self.t_of("pocket grips it") - self.elapsed() - 0.25),
            rate_func=linear,
        )

        self.at("pocket grips it")
        akt.clear_updaters()
        akt_lbl.clear_updaters()
        target_akt_pos = akt_dock_pos_for_tile(tiles[1], akt_scale=1.10)
        self.play(
            akt.animate.move_to(target_akt_pos),
            akt_lbl.animate.move_to([tile_xs[1], -1.85, 0]),
            run_time=0.95,
        )
        ph_lbl.clear_updaters()
        ph_leader.clear_updaters()
        self.finish()


class S05TwoPhosphates(SpokenScene):
    def construct(self):
        y_in, y_out = 1.45, 2.35
        bilayer = build_bilayer(y_in=y_in, y_out=y_out)

        rec = make_receptor(x=-5.35, y_in=y_in, y_out=y_out, scale=0.74, docked=True, active=True)
        ins = make_insulin_orb(0.16).move_to(rec.jaw_center)
        irs = make_irs1(x=-4.10, y_in=y_in, scale=0.74, active=True)
        pi3k = make_pi3k(pos=(-2.80, y_in - 0.50, 0), open_angle=0.40, scale=0.70)
        left_ctx = VGroup(rec, ins, irs, pi3k)
        for m in left_ctx.family_members_with_points():
            m.set_opacity(0.60)

        tile_xs = [-0.65, 0.80, 2.25, 3.70]
        tiles = VGroup(*[make_lipid_tile(tx, y_in=y_in, gold=True, width=1.00, height=0.52) for tx in tile_xs])
        pip3_lbl = T("PIP3", size=28, color=PIP3_GOLD).move_to([1.52, y_in + 1.30, 0])

        akt_pos = akt_dock_pos_for_tile(tiles[1], akt_scale=1.10)
        akt = make_akt(pos=akt_pos, fold_deg=18.0, active=False, scale=1.10)
        akt_lbl = T("Akt", size=28, color=AKT_MUTED).move_to([tile_xs[1] + 0.10, -2.55, 0])

        # PDK1 begins lower in the cytosol and rises smoothly onto tile 0 during "second kinase"
        pdk_dock = pdk1_dock_pos_for_tile(tiles[0], pdk_scale=1.00)
        pdk1 = make_pdk1(pos=[-1.65, -1.65, 0], lean=0.0, scale=1.00)
        pdk1_lbl = T("PDK1", size=28, color=VIOLET).move_to([-2.75, -1.25, 0])

        stag = scope_tag("schematic")
        self.add(bilayer, left_ctx, tiles, pip3_lbl, akt, akt_lbl, pdk1, pdk1_lbl, stag)

        self.at("unfolds")
        akt_open_probe = make_akt(pos=ORIGIN, fold_deg=115.0, active=False, scale=1.10)
        akt_open_pos = akt.ph.get_center() - akt_open_probe.ph.get_center()
        akt_open = make_akt(pos=akt_open_pos, fold_deg=115.0, active=False, scale=1.10)
        thr_lbl = T("Thr308", size=26, color=TEXT).move_to([0.42, -0.88, 0])
        thr_leader = Line([0.52, -0.68, 0], akt_open.loop_pt + DOWN * 0.07, color=TEXT, stroke_width=2.4)
        self.play(
            Transform(akt, akt_open),
            FadeIn(thr_lbl),
            Create(thr_leader),
            run_time=max(2.6, self.t_of("second kinase") - self.elapsed() - 0.25),
        )

        self.at("second kinase")
        pdk_ph_target = np.array([-1.80, 0.24, 0.0])
        pdk_ph_lbl = T("PH domain", size=24, color=VIOLET).move_to(pdk_ph_target)
        pdk1_docked_probe = make_pdk1(pos=pdk_dock, lean=0.0, scale=1.00)
        pdk_ph_leader = Line(
            [-1.45, 0.40, 0],
            pdk1_docked_probe.ph.get_left() + LEFT * 0.05,
            color=VIOLET, stroke_width=2.4,
        )
        # Continuous upward docking of PDK1 onto tile 0 across ~6.5 s (eliminates freeze)
        t_dock = max(3.5, self.t_of("phosphorylates that loop") - self.elapsed() - 0.25)
        self.play(
            pdk1.animate.move_to(pdk_dock),
            pdk1_lbl.animate.move_to([-1.10, -0.75, 0]),
            run_time=t_dock - 0.9,
        )
        self.play(FadeIn(pdk_ph_lbl), Create(pdk_ph_leader), run_time=0.9)

        self.at("phosphorylates that loop")
        pdk1_lean = make_pdk1(pos=pdk_dock, lean=0.45, scale=1.00)
        p_thr = make_p_badge("P", radius=0.23).next_to(akt_open.loop_pt, LEFT, buff=0.14)
        self.play(Transform(pdk1, pdk1_lean), FadeOut(pdk_ph_lbl), FadeOut(pdk_ph_leader), run_time=0.9)
        self.play(FadeIn(p_thr, scale=0.7), run_time=1.0)

        self.at("Another kinase complex")
        mtorc2 = make_mtorc2(pos=[4.95, -1.85, 0], scale=1.00)
        mtor_lbl = T("mTORC2\n(a kinase)", size=24, color=LAVENDER, line_spacing=0.85).next_to(mtorc2, DOWN, buff=0.20)
        self.play(FadeIn(mtorc2, shift=LEFT * 0.35), FadeIn(mtor_lbl), run_time=0.9)

        ser_lbl = T("Ser473", size=26, color=TEXT).move_to([3.08, -0.80, 0])
        ser_leader = Line([3.02, -0.62, 0], akt_open.tail_pt + DOWN * 0.07, color=TEXT, stroke_width=2.4)
        p_ser = make_p_badge("P", radius=0.23).next_to(akt_open.tail_pt, RIGHT, buff=0.14)
        akt_active = make_akt(pos=akt_open.get_center(), fold_deg=115.0, active=True, scale=1.10)
        akt_active_lbl = T("Akt (active)", size=28, color=AKT_ACTIVE).move_to([tile_xs[1] + 0.10, -2.55, 0])
        akt_halo = Circle(radius=0.56, stroke_color=AKT_ACTIVE, stroke_width=4.0, fill_color=AKT_ACTIVE, fill_opacity=0.14)
        akt_halo.move_to(akt_active.kin.get_center())
        self.play(
            mtorc2.animate.move_to([4.35, 0.08, 0]),
            mtor_lbl.animate.move_to([4.72, -0.82, 0]),
            FadeIn(ser_lbl),
            Create(ser_leader),
            run_time=1.2,
        )
        self.play(
            FadeIn(p_ser, scale=0.7),
            Transform(akt, akt_active),
            FadeIn(akt_halo),
            swap(akt_lbl, akt_active_lbl, run_time=0.6),
            run_time=1.0,
        )
        rest = max(0.3, self.narration_s + 0.30 - self.elapsed())
        self.play(akt_halo.animate(rate_func=there_and_back).scale(1.12), run_time=rest)
        self.finish()


class S06GuidingRule(SpokenScene):
    def construct(self):
        y_in, y_out = 1.05, 1.90
        w = build_overview_world(
            y_in=y_in, y_out=y_out,
            insulin_docked=True, rec_p=True, irs_p=True,
            pi3k_docked=True, pi3k_open=True, n_pip3=5,
            akt_docked=True, akt_active=True, show_pdk1=True, show_mtorc2=True,
        )
        rec_lbl = T("receptor", size=24, color=AMBER).move_to([-4.65, -1.90, 0])
        irs_lbl = T("IRS-1", size=26, color=TEAL_IRS).move_to([-2.95, -1.90, 0])
        pi3k_lbl = T("PI 3-kinase", size=24, color=SKY).move_to([-0.85, -1.90, 0])
        pip_lbl = T("PIP3", size=28, color=PIP3_GOLD).move_to([2.50, y_in + 1.32, 0])
        akt_lbl = T("Akt (active)", size=26, color=AKT_ACTIVE).move_to([2.40, -2.25, 0])
        pdk_lbl = T("PDK1", size=24, color=VIOLET).move_to([0.70, -1.25, 0])
        mtor_lbl = T("mTORC2", size=24, color=LAVENDER).next_to(w.mtorc2, DOWN, buff=0.22)
        stag = scope_tag("schematic")

        # Keep extracellular insulin orbs strictly to the left-center (x in [-2.6, 1.2]) clear of "PIP3"
        bg_walks = [
            compute_walk(61 + i, start=(-1.6 + i * 1.4, 2.60), bounds=(-2.8, 1.2, y_out + 0.30, 3.22), n_steps=180, step_len=0.14, bounce_y="bottom")[0]
            for i in range(3)
        ]
        t_bg = ValueTracker(0.0)
        bg_orbs = VGroup(*[make_insulin_orb(0.19).move_to(bg_walks[i][0]) for i in range(3)])
        for i, orb in enumerate(bg_orbs):
            orb.add_updater(lambda m, idx=i: m.move_to(eval_walk(bg_walks[idx], t_bg.get_value())))

        self.add(w, rec_lbl, irs_lbl, pi3k_lbl, pip_lbl, akt_lbl, pdk_lbl, mtor_lbl, stag, bg_orbs)

        # Signal wave pulse routed cleanly via PH/kinase centers (clear of P badges and mTORC2 text)
        pulse_ring = Circle(radius=0.28, stroke_color=PHOS, stroke_width=4.5, fill_color=PHOS, fill_opacity=0.22)
        pulse_ring.move_to(w.pdk1.ph.get_center())
        self.add(pulse_ring)

        self.at("loop phosphate")
        self.play(
            pulse_ring.animate.move_to(w.akt.ph.get_center()),
            t_bg.animate.set_value(0.12),
            run_time=0.8,
        )
        self.play(
            pulse_ring.animate.move_to(w.akt.kin.get_center()).scale(1.2),
            t_bg.animate.set_value(0.22),
            run_time=max(0.8, self.t_of("tail phosphate") - self.elapsed() - 0.25),
        )

        self.at("tail phosphate")
        self.play(
            pulse_ring.animate.move_to(w.akt.kin.get_center() + DOWN * 0.45),
            t_bg.animate.set_value(0.32),
            run_time=0.7,
        )
        self.play(
            pulse_ring.animate.move_to(w.mtorc2.get_center()),
            t_bg.animate.set_value(0.44),
            run_time=max(0.8, self.t_of("Keep this rule") - self.elapsed() - 0.25),
        )

        self.at("Keep this rule")
        cap = caption("PIP3 recruits Akt to the membrane, where two phosphates activate it.", size=28, color=PIP3_GOLD)
        self.play(
            FadeIn(cap),
            pulse_ring.animate.move_to(w.tiles[0].head.get_center()).scale(1 / 1.2),
            t_bg.animate.set_value(0.56),
            run_time=max(1.2, self.t_of("PIP3 recruits") - self.elapsed() - 0.25),
        )

        self.at("PIP3 recruits")
        for tile in w.tiles:
            self.play(pulse_ring.animate.move_to(tile.head.get_center()), t_bg.animate.set_value(0.66), run_time=0.45, rate_func=linear)
        self.play(
            pulse_ring.animate.move_to(w.akt.ph.get_center()),
            t_bg.animate.set_value(0.75),
            run_time=0.7,
        )
        self.play(
            pulse_ring.animate.move_to(w.akt.kin.get_center()).scale(1.3),
            t_bg.animate.set_value(0.82),
            run_time=max(0.8, self.t_of("upstream steps write") - self.elapsed() - 0.25),
        )

        self.at("upstream steps write")
        relay_pts = [
            w.rec.jaw_center,
            w.irs.get_center(),
            w.pi3k.get_center(),
            w.tiles[2].head.get_center(),
            w.akt.ph.get_center(),
            w.akt.kin.get_center(),
        ]
        self.play(pulse_ring.animate.move_to(relay_pts[0]).scale(1 / 1.3), t_bg.animate.set_value(0.86), run_time=0.50)
        for k, pt in enumerate(relay_pts[1:], 1):
            self.play(pulse_ring.animate.move_to(pt), t_bg.animate.set_value(0.86 + 0.028 * k), run_time=0.60, rate_func=linear)
        self.finish()


class S07PredictQ(SpokenScene):
    def construct(self):
        y_in, y_out = 1.05, 1.90
        w = build_overview_world(
            y_in=y_in, y_out=y_out,
            insulin_docked=True, rec_p=True, irs_p=True,
            pi3k_docked=True, pi3k_open=False, pi3k_blocked=False,
            n_pip3=0, akt_docked=False, akt_active=False, show_pdk1=True,
        )
        rec_lbl = T("receptor", size=24, color=AMBER).move_to([-4.65, -1.90, 0])
        irs_lbl = T("IRS-1", size=26, color=TEAL_IRS).move_to([-2.95, -1.90, 0])
        pi3k_lbl = T("PI 3-kinase", size=24, color=SKY).move_to([-0.85, -1.90, 0])
        pip_lbl = T("lipid address?", size=26, color=PIP3_GOLD).move_to([2.50, y_in + 1.32, 0])
        pdk_lbl = T("PDK1", size=24, color=VIOLET).move_to([0.70, -1.25, 0])

        akt_walk, _ = compute_walk(73, start=(2.9, -0.85), bounds=(1.8, 4.1, -1.15, -0.40), n_steps=180, step_len=0.17)
        t_walk = ValueTracker(0.0)
        w.akt.move_to(akt_walk[0])
        akt_lbl = T("Akt", size=26, color=AKT_MUTED).next_to(w.akt, DOWN, buff=0.18)
        w.akt.add_updater(lambda m: m.move_to(eval_walk(akt_walk, t_walk.get_value())))
        akt_lbl.add_updater(lambda m: m.next_to(w.akt, DOWN, buff=0.18))

        stag = scope_tag("schematic")
        self.add(w, rec_lbl, irs_lbl, pi3k_lbl, pip_lbl, pdk_lbl, akt_lbl, stag)

        self.at("drug blocks")
        c = w.pi3k.cat.get_center()
        x_mark = VGroup(
            Line(c + UL * 0.30, c + DR * 0.30, color=RED, stroke_width=6),
            Line(c + UR * 0.30, c + DL * 0.30, color=RED, stroke_width=6),
        )
        drug_lbl = T("drug-blocked", size=24, color=RED).move_to([-0.85, -2.30, 0])
        self.play(
            Create(x_mark), FadeIn(drug_lbl),
            t_walk.animate.set_value(0.32),
            run_time=max(2.0, self.t_of("Insulin still binds") - self.elapsed() - 0.25),
            rate_func=linear,
        )

        self.at("Insulin still binds")
        self.play(
            w.extras.animate.scale(1.06),
            t_walk.animate.set_value(0.68),
            run_time=max(2.0, self.t_of("still gain its") - self.elapsed() - 0.25),
            rate_func=there_and_back,
        )

        self.at("still gain its")
        q = question_card("PI 3-kinase blocked + insulin: does Akt get phosphorylated?", y=BOTTOM_Y + 0.15, size=28, max_w=10.6)
        lipid_q = T("?", size=34, color=PIP3_GOLD, weight=BOLD).move_to([2.50, y_in + 0.48, 0])
        akt_q1 = T("P?", size=22, color=PHOS, weight=BOLD).next_to(w.akt.ph, RIGHT, buff=0.16)
        akt_q2 = T("P?", size=22, color=PHOS, weight=BOLD).next_to(w.akt.kin, RIGHT, buff=0.18).shift(DOWN * 0.10)
        akt_q1.add_updater(lambda m: m.next_to(w.akt.ph, RIGHT, buff=0.16))
        akt_q2.add_updater(lambda m: m.next_to(w.akt.kin, RIGHT, buff=0.18).shift(DOWN * 0.10))
        self.play(
            FadeIn(q.question), FadeIn(lipid_q), FadeIn(akt_q1), FadeIn(akt_q2),
            t_walk.animate.set_value(0.84),
            run_time=0.65,
            rate_func=linear,
        )
        self.play(
            t_walk.animate.set_value(1.0),
            run_time=max(0.5, self.narration_s + 0.30 - self.elapsed()),
            rate_func=linear,
        )
        self.finish()


class S08Pause(PredictPause):
    QUESTION = "PI 3-kinase blocked + insulin: does Akt get phosphorylated?"
    CARD = {"y": BOTTOM_Y + 0.15, "size": 28, "max_w": 10.6}
    SECONDS = 4.5

    def backdrop(self):
        y_in, y_out = 1.05, 1.90
        w = build_overview_world(
            y_in=y_in, y_out=y_out,
            insulin_docked=True, rec_p=True, irs_p=True,
            pi3k_docked=True, pi3k_open=False, pi3k_blocked=True,
            n_pip3=0, akt_docked=False, akt_active=False, show_pdk1=True,
        )
        akt_walk, _ = compute_walk(73, start=(2.9, -0.85), bounds=(1.8, 4.1, -1.15, -0.40), n_steps=180, step_len=0.17)
        w.akt.move_to(akt_walk[-1])
        rec_lbl = T("receptor", size=24, color=AMBER).move_to([-4.65, -1.90, 0])
        irs_lbl = T("IRS-1", size=26, color=TEAL_IRS).move_to([-2.95, -1.90, 0])
        pi3k_lbl = T("PI 3-kinase", size=24, color=SKY).move_to([-0.85, -1.90, 0])
        drug_lbl = T("drug-blocked", size=24, color=RED).move_to([-0.85, -2.30, 0])
        pip_lbl = T("lipid address?", size=26, color=PIP3_GOLD).move_to([2.50, y_in + 1.32, 0])
        lipid_q = T("?", size=34, color=PIP3_GOLD, weight=BOLD).move_to([2.50, y_in + 0.48, 0])
        pdk_lbl = T("PDK1", size=24, color=VIOLET).move_to([0.70, -1.25, 0])
        akt_lbl = T("Akt", size=26, color=AKT_MUTED).next_to(w.akt, DOWN, buff=0.18)
        akt_q1 = T("P?", size=22, color=PHOS, weight=BOLD).next_to(w.akt.ph, RIGHT, buff=0.16)
        akt_q2 = T("P?", size=22, color=PHOS, weight=BOLD).next_to(w.akt.kin, RIGHT, buff=0.18).shift(DOWN * 0.10)
        return VGroup(w, rec_lbl, irs_lbl, pi3k_lbl, drug_lbl, pip_lbl, lipid_q, pdk_lbl, akt_lbl, akt_q1, akt_q2)


class S09PredictReveal(SpokenScene):
    def construct(self):
        y_in, y_out = 1.05, 1.90
        w = build_overview_world(
            y_in=y_in, y_out=y_out,
            insulin_docked=True, rec_p=True, irs_p=True,
            pi3k_docked=True, pi3k_open=False, pi3k_blocked=True,
            n_pip3=0, akt_docked=False, akt_active=False, show_pdk1=True,
        )
        akt_walk, _ = compute_walk(91, start=(3.1, -1.30), bounds=(2.3, 5.1, -1.85, -0.55), n_steps=180, step_len=0.17)
        t_walk = ValueTracker(0.0)
        w.akt.move_to(akt_walk[0])

        rec_lbl = T("receptor", size=24, color=AMBER).move_to([-4.65, -1.90, 0])
        irs_lbl = T("IRS-1", size=26, color=TEAL_IRS).move_to([-2.95, -1.90, 0])
        pi3k_lbl = T("PI 3-kinase", size=24, color=SKY).move_to([-0.85, -1.90, 0])
        drug_lbl = T("drug-blocked", size=24, color=RED).move_to([-0.85, -2.30, 0])
        pip_lbl = T("PIP2", size=26, color=SLATE_LBL).move_to([2.50, y_in + 1.32, 0])
        pdk_lbl = T("PDK1", size=24, color=VIOLET).move_to([0.70, -1.25, 0])
        akt_lbl = T("Akt (folded)", size=26, color=AKT_MUTED).next_to(w.akt, DOWN, buff=0.18)

        w.akt.add_updater(lambda m: m.move_to(eval_walk(akt_walk, t_walk.get_value())))
        akt_lbl.add_updater(lambda m: m.next_to(w.akt, DOWN, buff=0.18))
        stag = scope_tag("schematic")

        self.add(w, rec_lbl, irs_lbl, pi3k_lbl, drug_lbl, pip_lbl, pdk_lbl, akt_lbl, stag)

        self.play(t_walk.animate.set_value(0.18), run_time=max(0.8, self.t_of("receptor and docking") - 0.25), rate_func=linear)

        self.at("receptor and docking")
        self.play(
            w.extras.animate.scale(1.06),
            t_walk.animate.set_value(0.36),
            run_time=max(1.5, self.t_of("no gold lipid") - self.elapsed() - 0.25),
            rate_func=there_and_back,
        )

        self.at("no gold lipid")
        no_pip3 = T("no PIP3", size=28, color=RED).move_to([2.50, y_in + 1.32, 0])
        self.play(swap(pip_lbl, no_pip3, run_time=0.8), t_walk.animate.set_value(0.55))
        rem1 = max(0.5, self.t_of("stays folded") - self.elapsed() - 0.25)
        self.play(t_walk.animate.set_value(0.65), run_time=rem1, rate_func=linear)

        self.at("stays folded")
        sep_line = DashedLine([1.35, 0.25, 0], [1.35, -2.10, 0], color=GREY, stroke_width=2.5, dash_length=0.14)
        self.play(
            Create(sep_line),
            t_walk.animate.set_value(0.86),
            run_time=max(1.5, self.t_of("Without the lipid") - self.elapsed() - 0.25),
            rate_func=linear,
        )

        self.at("Without the lipid")
        status = caption("No PIP3: Akt stays off", size=30, color=RED)
        self.play(FadeIn(status), t_walk.animate.set_value(1.0), run_time=max(1.2, self.narration_s + 0.35 - self.elapsed()), rate_func=linear)
        self.finish()


class S10Closing(SpokenScene):
    def construct(self):
        y_in, y_out = 1.45, 2.35
        bilayer = build_bilayer(y_in=y_in, y_out=y_out, x0=-6.1, x1=1.9)
        tile_xs = [-4.6, -3.15, -1.70, -0.25]
        tiles = VGroup(*[make_lipid_tile(tx, y_in=y_in, gold=True, width=0.96, height=0.50) for tx in tile_xs])
        pip3_lbl = T("PIP3", size=28, color=PIP3_GOLD).move_to([-2.42, y_in + 1.30, 0])

        akt_start = np.array([tile_xs[2], -1.65, 0.0])
        akt = make_akt(pos=akt_start, fold_deg=18.0, active=False, scale=1.04)
        pdk_dock = pdk1_dock_pos_for_tile(tiles[1], pdk_scale=0.94)
        pdk1 = make_pdk1(pos=[-3.85, -1.45, 0], lean=0.0, scale=0.94)
        pdk_lbl = T("PDK1", size=26, color=VIOLET).move_to([tile_xs[1] - 1.75, -0.75, 0])
        mtorc2 = make_mtorc2(pos=[1.45, -1.85, 0], scale=0.94)
        mtor_lbl = T("mTORC2", size=26, color=LAVENDER).next_to(mtorc2, DOWN, buff=0.20)

        lock_title = T("Safety lock", size=30, color=TEXT, weight=BOLD).move_to([4.30, 2.35, 0])
        row_texts = ["1. PIP3", "2. Thr308-P", "3. Ser473-P"]
        row_cols = [PIP3_GOLD, VIOLET, LAVENDER]
        rows = VGroup(*[T(rt, size=28, color=rc) for rt, rc in zip(row_texts, row_cols)]).arrange(DOWN, aligned_edge=LEFT, buff=0.55)
        rows.move_to([4.05, 0.45, 0])
        checks = VGroup(*[T("✓", size=30, color=rc, weight=BOLD).next_to(r, RIGHT, buff=0.25) for r, rc in zip(rows, row_cols)])

        stag = scope_tag("schematic")
        self.add(bilayer, tiles, pip3_lbl, akt, pdk1, pdk_lbl, mtorc2, mtor_lbl, lock_title, rows, stag)

        # Step 1 (0..2.3s): Akt rises and locks onto gold PIP3 -> check 1 ticks on
        self.at("membrane lipid")
        dock_pos = akt_dock_pos_for_tile(tiles[2], akt_scale=1.04)
        self.play(akt.animate.move_to(dock_pos), FadeIn(checks[0]), run_time=1.3)

        # Step 2 (2.3..7.7s): Akt unfolds; PDK1 docks & stamps Thr308-P -> check 2; mTORC2 docks & stamps Ser473-P -> check 3
        self.at("two separate kinases")
        akt_open_probe = make_akt(pos=ORIGIN, fold_deg=115.0, active=False, scale=1.04)
        akt_open_pos = akt.ph.get_center() - akt_open_probe.ph.get_center()
        akt_open = make_akt(pos=akt_open_pos, fold_deg=115.0, active=False, scale=1.04)
        pdk1_lean = make_pdk1(pos=pdk_dock, lean=0.45, scale=0.94)
        self.play(
            Transform(akt, akt_open),
            pdk1.animate.move_to(pdk_dock),
            pdk_lbl.animate.move_to([tile_xs[1] - 1.25, 0.25, 0]),
            run_time=2.0,
        )

        p_thr = make_p_badge("P", radius=0.22).next_to(akt_open.loop_pt, LEFT, buff=0.14)
        self.play(Transform(pdk1, pdk1_lean), FadeIn(p_thr, scale=0.7), FadeIn(checks[1]), run_time=1.6)

        p_ser = make_p_badge("P", radius=0.22).next_to(akt_open.tail_pt, RIGHT, buff=0.14)
        akt_active = make_akt(pos=akt_open.get_center(), fold_deg=115.0, active=True, scale=1.04)
        akt_lbl = T("Akt (active)", size=28, color=AKT_ACTIVE).move_to([tile_xs[2] + 0.15, -2.40, 0])
        self.play(
            mtorc2.animate.move_to([1.25, -1.00, 0]),
            mtor_lbl.animate.move_to([1.25, -1.75, 0]),
            FadeIn(p_ser, scale=0.7),
            Transform(akt, akt_active),
            FadeIn(checks[2]),
            FadeIn(akt_lbl),
            run_time=max(1.5, self.t_of("active receptors build") - self.elapsed() - 0.25),
        )

        # Step 3 (7.7..13.8s): Show active receptor building/sustaining gold PIP3 tiles & active Akt halo
        self.at("active receptors build")
        rec = make_receptor(x=-5.65, y_in=y_in, y_out=y_out, scale=0.60, docked=True, active=True)
        ins = make_insulin_orb(0.14).move_to(rec.jaw_center)
        rec_lbl = T("receptor", size=22, color=AMBER).move_to([-5.65, 0.25, 0])
        akt_halo = Circle(radius=0.58, stroke_color=AKT_ACTIVE, stroke_width=4.5, fill_color=AKT_ACTIVE, fill_opacity=0.16)
        akt_halo.move_to(akt_active.kin.get_center())
        ring = Circle(radius=0.30, stroke_color=PHOS, stroke_width=4.5, fill_color=PHOS, fill_opacity=0.24)
        ring.move_to(rec.jaw_center)
        self.play(FadeIn(rec), FadeIn(ins), FadeIn(rec_lbl), FadeIn(akt_halo), FadeIn(ring), run_time=0.9)
        for tile in tiles:
            self.play(
                ring.animate.move_to(tile.head.get_center()),
                tile.animate(rate_func=there_and_back).scale(1.14),
                run_time=0.85,
            )
        self.play(
            ring.animate.move_to(akt_active.kin.get_center()).scale(1.35),
            akt_halo.animate(rate_func=there_and_back).scale(1.18),
            run_time=max(1.0, self.t_of("Put together") - self.elapsed() - 0.25),
        )

        # Step 4 (13.8..19.1s): Highlight safety lock rows 1 -> 2 -> 3 & show closing caption
        self.at("Put together")
        cap = caption("Lipid docking + dual phosphorylation switch Akt on cleanly.", size=26, color=TEXT)
        self.play(FadeIn(cap), run_time=0.55)
        self.play(
            ring.animate.move_to(rows[0].get_left() + LEFT * 0.42).scale(0.65),
            tiles.animate(rate_func=there_and_back).scale(1.06),
            run_time=1.05,
        )
        self.play(
            ring.animate.move_to(rows[1].get_left() + LEFT * 0.42),
            p_thr.animate(rate_func=there_and_back).scale(1.22),
            run_time=1.2,
        )
        self.play(
            ring.animate.move_to(rows[2].get_left() + LEFT * 0.42),
            p_ser.animate(rate_func=there_and_back).scale(1.22),
            run_time=1.2,
        )
        rem_end = max(0.6, self.narration_s + 0.30 - self.elapsed())
        self.play(
            ring.animate.move_to(akt_active.kin.get_center()).scale(1.4),
            akt_halo.animate(rate_func=there_and_back).scale(1.16),
            run_time=rem_end,
        )
        self.finish()


class S11End(EndCard):
    LINE = "PIP3 recruits Akt to the membrane,\nwhere two phosphates activate it."
