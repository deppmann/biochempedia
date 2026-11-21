"""Inside the Antenna: Cilia and Downstream Control (STEMhop: Hedgehog and the Primary Cilium, Chapter 2).

COLOUR MAP (one colour per concept, carried across the entire film):
- Hedgehog (Hh / Sonic hedgehog signal):  #F5A623 (warm gold)
- Patched (PTCH1 receptor / brake):      #E05A47 (coral-red)
- Smoothened (SMO switch):               #2AB7CA (teal; bright when ON, muted body when OFF)
- Primary cilium & microtubule core:     #A8DADC (pale cyan)
- Gli / Gli3 transcription factor:       #9B72CF (violet-lavender; full-length activator vs trimmed #B79CED-labelled repressor)
- Sterol tokens:                         #FFD166 (amber)
- Kinases (PKA/CK1/GSK3) & proteasome:   #7FA8E0 (slate-blue)
- Smoothened blocker (Cyclopamine/Vismo):#D81B60 / #FF5C93 (crisp magenta)
- Genes ON:                              #83C167 (green)
- Genes OFF:                             #E05A47 (coral-red)
- Labels / Neutral text:                 #E8EAF0 (TEXT)

ONE WORLD CARRIED:
A cross-section of a vertebrate cell with its plasma membrane, nucleus at the bottom, and the
pale-cyan primary cilium rising from the apical membrane. Downstream scenes zoom from this cell
out to the linear pathway chain and apply the exact same switch logic to the embryonic forebrain
and to basal cell carcinoma cells.

WHAT CHANGES IN EACH SPOKEN SCENE (and what drives it):
- s01_hook: Hedgehog docks onto Patched, turning it off so Smoothened activates and keeps Gli whole;
  then the camera zooms back as the primary cilium grows up from the cell surface and a magenta
  drug wedge locks onto Smoothened.
- s02_cilium_intro: The view pulls back to 70% frame height as the primary cilium rises, its
  parallel microtubule core extends from base to tip, and IFT motor shuttles continuously ride up
  and down the tracks (computed cyclic track positions).
- s03_off_in_cilium: Patched lines the ciliary membrane and deflects amber sterol particles away
  (deterministic trajectories from rng seed 7), Smoothened stays outside in the cell body, and
  full-length Gli3 is physically cleaved by kinases+proteasome into the shorter repressor that moves
  into the nucleus to switch Genes OFF.
- s04_on_in_cilium: Gold Hedgehog binds Patched, Patched slides out of the cilium and clears,
  Smoothened glides into the cilium and activates, and full-length Gli rides IFT tracks to the tip,
  escapes trimming, and enters the nucleus to switch Genes ON.
- s05_chain_logic: The cilium cross-section sits on the left while the horizontal switch chain
  builds across the top; a computed signal pulse travels left-to-right along the pathway track and
  halts abruptly at a downstream barrier.
- s06_embryo_predict: In the schematic forebrain below the chain, midline Sonic hedgehog waves
  split the single central eye field into left and right (computed separation tracker), then reset
  to one oval as the magenta Cyclopamine wedge snaps onto Smoothened while Hedgehog keeps arriving.
- s08_reveal: Midline Sonic hedgehog waves keep arriving at the undivided central eye field while
  an upstream signal pulse turns off Patched and halts at Cyclopamine-locked Smoothened, trimming
  Gli to Gli3R and switching Genes OFF; a call-out arrow traces the sheep defect to Smoothened.
- s09_tumour_vismodegib: Two side-by-side tumour cells compare Lost Patched (Patched disappears,
  Smoothened runs ON in the cilium sending signal waves until Vismodegib snaps on and flips Genes
  OFF) against Downstream fault (Vismodegib locks Smoothened OFF, yet a downstream Gli fault arrow
  keeps firing Genes ON).
- s10_synthesis: Returns to one centered cell where Patched exits, Smoothened enters, and Gli
  gathers at the tip, while the fly-cell note appears and a pulse along the compact chain shows
  downstream steps overriding upstream ones.
"""

import numpy as np
from bp_parts import *

# ---- Concept Palette ----
HH_COL = "#F5A623"       # warm gold: Hedgehog / Sonic hedgehog
PTCH_COL = "#E05A47"     # coral-red: Patched / Genes OFF
SMO_COL = "#2AB7CA"      # teal: Smoothened
SMO_DIM = "#134E57"      # muted dark teal fill when Smoothened is OFF
CILIUM_COL = "#A8DADC"   # pale cyan: primary cilium & microtubules
GLI_COL = "#9B72CF"      # violet-lavender: full-length Gli
GLI_REP_COL = "#B79CED"  # crisp lighter violet for repressor labels
STEROL_COL = "#FFD166"   # amber: sterol tokens
KINASE_COL = "#7FA8E0"   # slate-blue: kinases + proteasome
DRUG_COL = "#D81B60"     # magenta fill: Cyclopamine / Vismodegib
DRUG_EDGE = "#FF5C93"    # crisp magenta border/label
ON_COL = "#83C167"       # green: Genes ON


# ---- Reusable Schematic Builders ----

def build_patched(pos=ORIGIN, scale=1.0, active=True, missing=False):
    """Coral-red 12-pass transporter gate: two pillars forming a sterol-clearing channel."""
    h = 0.54 * scale
    if missing:
        l_box = DashedVMobject(RoundedRectangle(corner_radius=0.07 * scale, width=0.14 * scale, height=h,
                                                stroke_color=PTCH_COL, stroke_width=2.4), num_dashes=6)
        r_box = l_box.copy()
    else:
        op = 0.88 if active else 0.30
        sw = 2.6 if active else 1.8
        l_box = RoundedRectangle(corner_radius=0.07 * scale, width=0.15 * scale, height=h,
                                 stroke_color=PTCH_COL, stroke_width=sw, fill_color=PTCH_COL, fill_opacity=op)
        r_box = l_box.copy()
    l_box.move_to(LEFT * 0.11 * scale)
    r_box.move_to(RIGHT * 0.11 * scale)
    return VGroup(l_box, r_box).move_to(pos)


def build_smoothened(pos=ORIGIN, scale=1.0, on=False):
    """Teal receptor block with a side drug pocket notch; bright rim when ON, dark muted body when OFF."""
    w, h = 0.42 * scale, 0.54 * scale
    fill_c = SMO_COL if on else SMO_DIM
    fill_op = 0.90 if on else 0.78
    stroke_w = 3.8 if on else 2.4
    body = RoundedRectangle(corner_radius=0.10 * scale, width=w, height=h,
                            stroke_color=SMO_COL, stroke_width=stroke_w,
                            fill_color=fill_c, fill_opacity=fill_op)
    pocket = Polygon(
        [w * 0.5, h * 0.18, 0],
        [w * 0.14, 0, 0],
        [w * 0.5, -h * 0.18, 0],
        stroke_color=SMO_COL, stroke_width=1.8, fill_color=BG, fill_opacity=0.95,
    )
    g = VGroup(body, pocket)
    if on:
        glow = RoundedRectangle(corner_radius=0.14 * scale, width=w + 0.14 * scale, height=h + 0.14 * scale,
                                stroke_color=SMO_COL, stroke_width=2.2, stroke_opacity=0.72, fill_opacity=0)
        g.add(glow)
    return g.move_to(pos)


def build_hedgehog(pos=ORIGIN, scale=1.0):
    """Warm-gold Hedgehog ligand sphere with lipid anchor ticks."""
    r = 0.19 * scale
    core = Circle(radius=r, stroke_color=HH_COL, stroke_width=2.5, fill_color=HH_COL, fill_opacity=0.94)
    t1 = Line(LEFT * r, LEFT * (r + 0.12 * scale), color=STEROL_COL, stroke_width=2.8 * scale)
    t2 = Line(RIGHT * r, RIGHT * (r + 0.12 * scale), color=STEROL_COL, stroke_width=2.8 * scale)
    return VGroup(t1, t2, core).move_to(pos)


def build_drug_wedge(pos=ORIGIN, scale=1.0):
    """Crisp magenta triangular wedge shaped to snap into Smoothened's pocket."""
    wedge = Polygon(
        [0.0, 0.16 * scale, 0],
        [-0.36 * scale, 0.0, 0],
        [0.0, -0.16 * scale, 0],
        [0.14 * scale, -0.12 * scale, 0],
        [0.14 * scale, 0.12 * scale, 0],
        stroke_color=DRUG_EDGE, stroke_width=2.5, fill_color=DRUG_COL, fill_opacity=0.95,
    )
    return wedge.move_to(pos)


def build_gli_full(pos=ORIGIN, scale=1.0):
    """Full-length Gli: front DNA-binding segment + back activator segment."""
    front = RoundedRectangle(corner_radius=0.06 * scale, width=0.42 * scale, height=0.18 * scale,
                             stroke_color=GLI_COL, stroke_width=2.4, fill_color=GLI_COL, fill_opacity=0.90)
    back = RoundedRectangle(corner_radius=0.06 * scale, width=0.46 * scale, height=0.18 * scale,
                            stroke_color=GLI_COL, stroke_width=2.4, fill_color="#C7A9F0", fill_opacity=0.90)
    back.next_to(front, RIGHT, buff=0.03 * scale)
    g = VGroup(front, back).move_to(pos)
    g.front = front
    g.back = back
    return g


def build_gli_repressor(pos=ORIGIN, scale=1.0):
    """Trimmed Gli3 repressor: only the front DNA-binding segment remains."""
    return RoundedRectangle(corner_radius=0.06 * scale, width=0.42 * scale, height=0.18 * scale,
                            stroke_color=GLI_REP_COL, stroke_width=2.5, fill_color=GLI_COL, fill_opacity=0.85).move_to(pos)


def build_cilium_cell(cx=0.0, mem_y=-1.45, cil_h=4.35, cil_w=1.36, mem_half_w=5.5, nuc_h=1.85,
                      with_tracks=True, cilium_visible=True, pill_text="Genes OFF", pill_col=PTCH_COL,
                      pill_size=26, pill_pad=0.13, cyto_h=None, nuc_angle=-0.95):
    """Builds the vertebrate cell cross-section: plasma membrane, primary cilium finger, microtubule tracks,
    and nucleus dome at the bottom. Geometry ensures pill sits cleanly inside the nucleus with no straddle."""
    half_c = cil_w / 2.0
    r_tip = half_c
    tip_y = mem_y + cil_h - r_tip

    if cilium_visible:
        n_arc = 24
        arc_pts = [
            np.array([cx + r_tip * np.cos(a), tip_y + r_tip * np.sin(a), 0.0])
            for a in np.linspace(PI, 0, n_arc)
        ]
        pts = [
            np.array([cx - mem_half_w, mem_y, 0.0]),
            np.array([cx - half_c, mem_y, 0.0]),
            np.array([cx - half_c, tip_y, 0.0]),
            *arc_pts,
            np.array([cx + half_c, tip_y, 0.0]),
            np.array([cx + half_c, mem_y, 0.0]),
            np.array([cx + mem_half_w, mem_y, 0.0]),
        ]
        membrane = VMobject(stroke_color=CILIUM_COL, stroke_width=5.0, fill_opacity=0)
        membrane.set_points_as_corners(pts)
        cil_fill = Polygon(
            np.array([cx - half_c, mem_y, 0.0]),
            np.array([cx - half_c, tip_y, 0.0]),
            *arc_pts,
            np.array([cx + half_c, tip_y, 0.0]),
            np.array([cx + half_c, mem_y, 0.0]),
            stroke_width=0, fill_color="#1A3244", fill_opacity=0.72,
        )
    else:
        membrane = Line([cx - mem_half_w, mem_y, 0.0], [cx + mem_half_w, mem_y, 0.0],
                        color=CILIUM_COL, stroke_width=5.0)
        cil_fill = VGroup()

    ch = cyto_h if cyto_h is not None else max(1.0, nuc_h + 0.35)
    cyto_bg = Rectangle(width=2 * mem_half_w, height=ch,
                        stroke_width=0, fill_color="#1B2A45", fill_opacity=0.82)
    cyto_bg.move_to([cx, mem_y - ch / 2.0, 0.0])

    track_top = mem_y + cil_h - r_tip * 0.70
    track_bot = mem_y + 0.08
    if with_tracks and cilium_visible:
        t_left = Line([cx - 0.17 * cil_w, track_bot, 0.0], [cx - 0.17 * cil_w, track_top, 0.0],
                      color=CILIUM_COL, stroke_width=3.2, stroke_opacity=0.68)
        t_right = Line([cx + 0.17 * cil_w, track_bot, 0.0], [cx + 0.17 * cil_w, track_top, 0.0],
                       color=CILIUM_COL, stroke_width=3.2, stroke_opacity=0.68)
        basal = RoundedRectangle(corner_radius=0.05, width=cil_w * 0.65, height=0.18,
                                 stroke_color=CILIUM_COL, stroke_width=2.2, fill_color=CILIUM_COL, fill_opacity=0.28)
        basal.move_to([cx, mem_y - 0.08, 0.0])
        tracks = VGroup(t_left, t_right, basal)
    else:
        tracks = VGroup()

    nuc_w = min(mem_half_w * 1.56, 7.6)
    nuc_bot = mem_y - nuc_h
    nuc = ArcBetweenPoints([cx - nuc_w / 2, nuc_bot, 0.0], [cx + nuc_w / 2, nuc_bot, 0.0], angle=nuc_angle,
                           stroke_color="#7B99C7", stroke_width=3.8, fill_color="#23375A", fill_opacity=0.88)
    nuc_base = Line([cx - nuc_w / 2, nuc_bot, 0.0], [cx + nuc_w / 2, nuc_bot, 0.0],
                    stroke_color="#7B99C7", stroke_width=2.2)
    nucleus = VGroup(nuc, nuc_base)

    gene_y = nuc_bot + nuc.height * 0.39
    gene_pill = boxed_label(pill_text, pill_col, size=pill_size, pad=pill_pad, fill_opacity=0.20)
    gene_pill.move_to([cx, gene_y, 0.0])

    g = VGroup(cyto_bg, cil_fill, tracks, membrane, nucleus, gene_pill)
    g.cyto_bg = cyto_bg
    g.membrane = membrane
    g.cil_fill = cil_fill
    g.tracks = tracks
    g.nucleus = nucleus
    g.nuc_arc = nuc
    g.gene_pill = gene_pill
    g.cx = cx
    g.mem_y = mem_y
    g.cil_h = cil_h
    g.cil_w = cil_w
    g.track_bot = track_bot
    g.track_top = track_top
    g.gene_pos = np.array([cx, gene_y, 0.0])
    g.nuc_bot = nuc_bot
    return g


def make_ift_shuttles(cx, track_x_off, y_bot, y_top, phase_tracker, n_per_side=3, cargo_w=0.22, cargo_h=0.28):
    """Always-redraw IFT cargo shuttles riding smoothly up the left track and down the right track."""
    def mk():
        p = phase_tracker.get_value()
        shuttles = VGroup()
        span = max(0.4, y_top - y_bot)
        for i in range(n_per_side):
            u_up = (p + i / n_per_side) % 1.0
            y_u = y_bot + 0.16 + u_up * (span - 0.32)
            c_up = RoundedRectangle(corner_radius=0.05, width=cargo_w, height=cargo_h,
                                    stroke_color=TEXT, stroke_width=2.2, fill_color=CILIUM_COL, fill_opacity=0.96)
            c_up.move_to([cx - track_x_off, y_u, 0.0])

            u_dn = (p + 0.35 + i / n_per_side) % 1.0
            y_d = y_top - 0.16 - u_dn * (span - 0.32)
            c_dn = RoundedRectangle(corner_radius=0.05, width=cargo_w, height=cargo_h,
                                    stroke_color=TEXT, stroke_width=2.2, fill_color="#7EA8BE", fill_opacity=0.95)
            c_dn.move_to([cx + track_x_off, y_d, 0.0])
            shuttles.add(c_up, c_dn)
        return shuttles
    return always_redraw(mk)


def make_shh_waves(origin_pt, wave_t, color=HH_COL, max_r=1.42):
    """Always-redraw expanding Sonic hedgehog waves + diffusing gold signal tokens rising from midline source."""
    def mk():
        t = wave_t.get_value()
        arcs = VGroup()
        for k in range(3):
            u = (t + k / 3.0) % 1.0
            r = 0.25 + u * (max_r - 0.25)
            op = max(0.25, 1.0 - 0.70 * u)
            arcs.add(Arc(radius=r, start_angle=PI * 0.20, angle=PI * 0.60,
                         arc_center=origin_pt, color=color, stroke_width=4.8, stroke_opacity=op))
            # Diffusing gold signal particles riding the wavefront
            for ang in (PI * 0.38, PI * 0.62):
                pt = origin_pt + np.array([r * np.cos(ang), r * np.sin(ang), 0.0])
                arcs.add(Dot(pt, radius=0.065, color=color, fill_opacity=op))
        return arcs
    return always_redraw(mk)


def build_chain(top_y=2.65, left_x=-6.4, right_x=6.4, font_size=24, pad=0.12,
                ptch_text="Patched", ptch_off=False,
                smo_text="Smoothened (cilium)", smo_off=False,
                gli_text="Gli", gli_col=GLI_COL,
                genes_text="Genes", genes_col=ON_COL, show_genes=True,
                fixed_boxes=True):
    """Builds the horizontal pathway chain with fixed-width boxes so node swaps never collide."""
    if fixed_boxes:
        hh = boxed_label("Hedgehog", HH_COL, size=font_size, box=(1.50, 0.56), pad=pad, fill_opacity=0.20)
        ptch = boxed_label(ptch_text, PTCH_COL, size=font_size, box=(2.05, 0.56), pad=pad,
                           fill_opacity=0.06 if ptch_off else 0.20)
        smo = boxed_label(smo_text, SMO_COL, size=font_size, box=(2.70, 0.56), pad=pad,
                          fill_opacity=0.06 if smo_off else 0.22)
        gli = boxed_label(gli_text, gli_col, size=font_size, box=(1.35, 0.56), pad=pad, fill_opacity=0.20)
        nodes = [hh, ptch, smo, gli]
        if show_genes:
            genes = boxed_label(genes_text, genes_col, size=font_size, box=(1.85, 0.56), pad=pad, fill_opacity=0.20)
            nodes.append(genes)
        else:
            genes = None
    else:
        hh = boxed_label("Hedgehog", HH_COL, size=font_size, pad=pad, fill_opacity=0.20)
        ptch = boxed_label(ptch_text, PTCH_COL, size=font_size, pad=pad,
                           fill_opacity=0.06 if ptch_off else 0.20)
        smo = boxed_label(smo_text, SMO_COL, size=font_size, pad=pad,
                          fill_opacity=0.06 if smo_off else 0.22)
        gli = boxed_label(gli_text, gli_col, size=font_size, pad=pad, fill_opacity=0.20)
        nodes = [hh, ptch, smo, gli]
        if show_genes:
            genes = boxed_label(genes_text, genes_col, size=font_size, pad=pad, fill_opacity=0.20)
            nodes.append(genes)
        else:
            genes = None

    total_node_w = sum(m.width for m in nodes)
    span = right_x - left_x
    gap = max(0.24, (span - total_node_w) / max(1, len(nodes) - 1))
    cur_x = left_x
    for m in nodes:
        m.move_to([cur_x + m.width / 2, top_y, 0.0])
        cur_x += m.width + gap

    def inhib_bar(a, b, color):
        p0 = [a.get_right()[0] + 0.06, top_y, 0.0]
        p1 = [b.get_left()[0] - 0.08, top_y, 0.0]
        ln = Line(p0, p1, color=color, stroke_width=3.2)
        cap = Line(np.array(p1) + UP * 0.15, np.array(p1) + DOWN * 0.15, color=color, stroke_width=3.6)
        return VGroup(ln, cap)

    def arrow_link(a, b, color):
        p0 = [a.get_right()[0] + 0.06, top_y, 0.0]
        p1 = [b.get_left()[0] - 0.06, top_y, 0.0]
        return Arrow(p0, p1, buff=0, color=color, stroke_width=3.2, max_tip_length_to_length_ratio=0.40)

    c1 = inhib_bar(hh, ptch, HH_COL)
    c2 = inhib_bar(ptch, smo, PTCH_COL)
    c3 = arrow_link(smo, gli, SMO_COL)
    links = [c1, c2, c3]
    if show_genes:
        c4 = arrow_link(gli, genes, gli_col)
        links.append(c4)

    g = VGroup(*nodes, *links)
    g.hh, g.ptch, g.smo, g.gli, g.genes = hh, ptch, smo, gli, genes
    g.links = links
    g.nodes = nodes
    g.top_y = top_y
    return g


def build_forebrain(cx=-0.35, cy=-0.45, w=4.6, h=3.15):
    """Builds the schematic embryonic forebrain cross-section with a midline Shh source at the bottom."""
    pts = [
        [cx - w * 0.45, cy - h * 0.35, 0],
        [cx - w * 0.50, cy + h * 0.08, 0],
        [cx - w * 0.30, cy + h * 0.46, 0],
        [cx, cy + h * 0.38, 0],
        [cx + w * 0.30, cy + h * 0.46, 0],
        [cx + w * 0.50, cy + h * 0.08, 0],
        [cx + w * 0.45, cy - h * 0.35, 0],
        [cx, cy - h * 0.48, 0],
    ]
    arr_pts = [np.array(p) for p in pts]
    n = len(arr_pts)
    ext = arr_pts[-5:] + arr_pts + arr_pts[:6]
    tmp = VMobject()
    tmp.set_points_smoothly(ext)
    outline = VMobject(stroke_color=CILIUM_COL, stroke_width=4.5, fill_color="#1E2F4D", fill_opacity=0.86)
    outline.set_points(tmp.points[20:20 + 4 * n])

    midline = DashedLine([cx, cy - h * 0.34, 0], [cx, cy + h * 0.34, 0],
                         color=CILIUM_COL, stroke_width=2.2, dash_length=0.12).set_opacity(0.55)
    shh_src = Ellipse(width=0.90, height=0.36, stroke_color=HH_COL, stroke_width=2.5,
                      fill_color=HH_COL, fill_opacity=0.92).move_to([cx, cy - h * 0.36, 0])
    shh_lab = T("Sonic hedgehog (vertebrate Hh)", 24, HH_COL).next_to(outline, DOWN, buff=0.16)
    brain_lab = T("Embryo forebrain\n(schematic)", 26, CILIUM_COL, line_spacing=0.9).move_to([cx - w * 0.5 - 1.90, cy + 0.15, 0])

    g = VGroup(outline, midline, shh_src, shh_lab, brain_lab)
    g.outline = outline
    g.midline = midline
    g.shh_src = shh_src
    g.shh_lab = shh_lab
    g.brain_lab = brain_lab
    g.eye_y = cy + 0.25
    g.cx = cx
    return g


def live_eye_field(brain, sep_tracker):
    """Computed eye field driven by separation tracker (0 = one central oval, 1 = left & right ovals)."""
    def mk():
        s = float(np.clip(sep_tracker.get_value(), 0.0, 1.0))
        if s < 0.08:
            w = 1.78 * (1.0 - 0.12 * s)
            ov = Ellipse(width=w, height=0.76, stroke_color=TEXT, stroke_width=3.5,
                         fill_color="#DCE7F5", fill_opacity=0.88).move_to([brain.cx, brain.eye_y, 0])
            return VGroup(ov)
        dx = 0.98 * s
        w = 1.78 - 0.78 * s
        h = 0.76 - 0.08 * s
        left_ov = Ellipse(width=w, height=h, stroke_color=TEXT, stroke_width=3.5,
                          fill_color="#DCE7F5", fill_opacity=0.88).move_to([brain.cx - dx, brain.eye_y, 0])
        right_ov = left_ov.copy().move_to([brain.cx + dx, brain.eye_y, 0])
        return VGroup(left_ov, right_ov)
    return always_redraw(mk)


# ================================================================== SCENES

class S00Title(TitleCard):
    LESSON = "Hedgehog and the Primary Cilium"
    TITLE = "Inside the Antenna: Cilia and Downstream Control"


class S01Hook(SpokenScene):
    """Carried-over cell cross-section from Film 1; Patched off -> Smoothened keeps Gli whole;
    zooms back to reveal rising primary cilium and magenta drug wedge beside Smoothened."""
    def construct(self):
        mem = Line([-6.2, 0.75, 0], [6.2, 0.75, 0], color=CILIUM_COL, stroke_width=5.0)
        cyto = Rectangle(width=12.4, height=4.25, stroke_width=0, fill_color="#1B2A45", fill_opacity=0.82).move_to([0, -1.38, 0])
        nuc = ArcBetweenPoints([-4.4, -3.35, 0], [4.4, -3.35, 0], angle=-0.85,
                               stroke_color="#7B99C7", stroke_width=3.8, fill_color="#23375A", fill_opacity=0.88)
        nuc_base = Line([-4.4, -3.35, 0], [4.4, -3.35, 0], stroke_color="#7B99C7", stroke_width=2.2)

        ptch = build_patched([-2.2, 0.75, 0], scale=1.35, active=True)
        smo = build_smoothened([1.5, 0.75, 0], scale=1.35, on=False)
        hh = build_hedgehog([-2.2, 2.55, 0], scale=1.25)
        gli = build_gli_full([1.5, -0.65, 0], scale=1.25)

        l_hh = T("Hedgehog", 28, HH_COL).next_to(hh, RIGHT, buff=0.24)
        l_ptch = T("Patched", 28, PTCH_COL).move_to([-3.65, 1.32, 0])
        l_smo = T("Smoothened", 28, SMO_COL).move_to([3.05, 1.32, 0])
        l_gli = T("Gli (whole)", 28, GLI_COL).next_to(gli, RIGHT, buff=0.24)
        gene_pill = boxed_label("Genes ON", ON_COL, size=26, pad=0.13).move_to([0, -2.72, 0])

        geom_start = VGroup(cyto, mem, nuc, nuc_base, ptch, smo, gli)
        labels_start = VGroup(l_ptch, l_smo, l_gli, l_hh)
        self.add(geom_start, l_ptch, l_smo, l_gli)
        self.play(FadeIn(hh, shift=DOWN * 0.2), FadeIn(l_hh, run_time=0.25), run_time=0.55)
        self.play(hh.animate.shift(DOWN * 0.45), l_hh.animate.shift(DOWN * 0.45), run_time=1.1)

        self.at("turns off patched")
        ptch_off = build_patched([-2.2, 0.75, 0], scale=1.35, active=False)
        smo_on = build_smoothened([1.5, 0.75, 0], scale=1.35, on=True)
        self.play(
            hh.animate.move_to([-2.2, 1.30, 0]),
            l_hh.animate.next_to([-2.2, 1.30, 0], UP, buff=0.32),
            Transform(ptch, ptch_off),
            run_time=1.1,
        )
        self.play(
            Transform(smo, smo_on),
            gli.animate.move_to([-0.25, -1.35, 0]),
            l_gli.animate.move_to([1.35, -1.35, 0]),
            FadeIn(gene_pill, run_time=0.3),
            run_time=2.5,
        )

        self.at("in vertebrate cells")
        self.play(FadeOut(labels_start), FadeOut(gene_pill), FadeOut(hh), run_time=0.45)
        self.play(geom_start.animate.scale(0.62).move_to([0, -2.15, 0]), run_time=0.9)

        cil_target = build_cilium_cell(cx=0.0, mem_y=-1.45, cil_h=4.35, cil_w=1.32, mem_half_w=5.2, nuc_h=1.85)
        cil_target.remove(cil_target.gene_pill)
        self.play(
            FadeOut(geom_start, run_time=0.35),
            FadeIn(cil_target.cyto_bg, run_time=0.4),
            FadeIn(cil_target.nucleus, run_time=0.4),
            Create(cil_target.membrane, run_time=1.0),
            FadeIn(cil_target.cil_fill, run_time=0.8),
        )
        ptch_c = build_patched([-0.66, 0.55, 0], scale=0.92, active=False)
        smo_c = build_smoothened([0.66, 0.35, 0], scale=0.92, on=True)
        gli_c = build_gli_full([0.0, 2.05, 0], scale=0.92)
        q_switch = boxed_label("Switch sits here?", CILIUM_COL, size=28, pad=0.15).move_to([-3.35, 1.85, 0])
        arr_q = Arrow(q_switch.get_right() + RIGHT * 0.08, [-0.76, 1.45, 0], buff=0, color=CILIUM_COL, stroke_width=3)
        self.play(
            Create(cil_target.tracks),
            FadeIn(ptch_c), FadeIn(smo_c), FadeIn(gli_c),
            FadeIn(q_switch, run_time=0.25), GrowArrow(arr_q),
            run_time=1.3,
        )

        self.at("and why can one")
        drug = build_drug_wedge([3.2, 0.35, 0], scale=1.1)
        l_drug = T("Smoothened blocker", 28, DRUG_EDGE).move_to([3.45, 1.55, 0])
        self.play(FadeIn(drug), FadeIn(l_drug, run_time=0.25), run_time=0.5)
        self.play(drug.animate.move_to([0.96, 0.35, 0]), run_time=1.2)
        arr_d = Arrow(l_drug.get_bottom() + DOWN * 0.08, [1.26, 0.48, 0], buff=0, color=DRUG_EDGE, stroke_width=3)
        embryo_tag = boxed_label("Deforms embryo", HH_COL, size=26, pad=0.13).move_to([3.95, 0.25, 0])
        tumour_tag = boxed_label("Shrinks skin tumour", ON_COL, size=26, pad=0.13).move_to([3.95, -0.58, 0])
        smo_c_off = build_smoothened([0.66, 0.35, 0], scale=0.92, on=False)
        self.play(
            GrowArrow(arr_d), Transform(smo_c, smo_c_off),
            FadeIn(embryo_tag, shift=RIGHT * 0.12), FadeIn(tumour_tag, shift=RIGHT * 0.12),
            run_time=1.5,
        )
        self.finish()


class S02CiliumIntro(SpokenScene):
    """Primary cilium pulls back to 70% frame height; parallel microtubule core extends upward and
    IFT motor shuttles continuously travel up and down the tracks."""
    def construct(self):
        cell = build_cilium_cell(cx=0.0, mem_y=-1.65, cil_h=4.95, cil_w=1.55, mem_half_w=5.5, nuc_h=1.90,
                                 with_tracks=False)
        cell.remove(cell.gene_pill)
        nuc_lab = T("Nucleus", 26, "#A6C0E6").move_to([0.0, -2.92, 0])
        mem_lab = T("Plasma membrane", 28, CILIUM_COL).move_to([-3.65, -2.15, 0])

        self.add(cell.cyto_bg, cell.nucleus, nuc_lab)
        self.play(Create(cell.membrane), FadeIn(cell.cil_fill), run_time=3.1)
        self.play(FadeIn(mem_lab, run_time=0.25))

        t_left = Line([-0.26, -1.55, 0], [-0.26, 2.55, 0], color=CILIUM_COL, stroke_width=4.2, stroke_opacity=0.82)
        t_right = Line([0.26, -1.55, 0], [0.26, 2.55, 0], color=CILIUM_COL, stroke_width=4.2, stroke_opacity=0.82)
        basal = RoundedRectangle(corner_radius=0.06, width=0.98, height=0.22,
                                 stroke_color=CILIUM_COL, stroke_width=2.5, fill_color=CILIUM_COL, fill_opacity=0.30).move_to([0, -1.75, 0])
        self.play(FadeIn(basal), Create(t_left), Create(t_right), run_time=3.8)

        self.at("single primary")
        cil_lab = T("Primary cilium", 30, CILIUM_COL).move_to([-3.2, 1.90, 0])
        cil_arr = Arrow(cil_lab.get_right() + RIGHT * 0.1, [-0.88, 1.90, 0], buff=0, color=CILIUM_COL, stroke_width=3)
        self.play(FadeIn(cil_lab, run_time=0.25), GrowArrow(cil_arr), run_time=1.8)

        self.at("does not beat")
        sway_l = DashedVMobject(ArcBetweenPoints([-0.95, -1.1, 0], [-1.55, 2.4, 0], angle=0.28, color=PTCH_COL, stroke_width=2.5), num_dashes=8)
        sway_r = DashedVMobject(ArcBetweenPoints([0.95, -1.1, 0], [1.55, 2.4, 0], angle=-0.28, color=PTCH_COL, stroke_width=2.5), num_dashes=8)
        cross_x = VGroup(
            Line([-0.22, -0.22, 0], [0.22, 0.22, 0], color=PTCH_COL, stroke_width=4.5),
            Line([-0.22, 0.22, 0], [0.22, -0.22, 0], color=PTCH_COL, stroke_width=4.5),
        ).move_to([1.85, 1.45, 0])
        no_beat = T("Does not beat", 28, PTCH_COL).next_to(cross_x, RIGHT, buff=0.2)
        self.play(Create(sway_l), Create(sway_r), Create(cross_x), FadeIn(no_beat, run_time=0.25), run_time=1.4)
        self.wait(0.6)
        self.play(FadeOut(sway_l), FadeOut(sway_r), FadeOut(cross_x), FadeOut(no_beat), run_time=0.35)

        self.at("motor shuttles")
        phase = ValueTracker(0.0)
        shuttles = make_ift_shuttles(0.0, 0.26, -1.45, 2.50, phase, n_per_side=3, cargo_w=0.22, cargo_h=0.28)
        ift_lab = boxed_label("Intraflagellar\ntransport (schematic)", CILIUM_COL, size=25, pad=0.14).move_to([3.85, 1.85, 0])
        core_lab = T("Microtubule core", 28, TEXT).move_to([3.55, 0.35, 0])
        ift_arr = Arrow(ift_lab.get_left() + LEFT * 0.1, [0.42, 1.85, 0], buff=0, color=CILIUM_COL, stroke_width=3)
        core_arr = Arrow(core_lab.get_left() + LEFT * 0.1, [0.36, 0.35, 0], buff=0, color=TEXT, stroke_width=3)
        self.add(shuttles)
        self.play(FadeIn(ift_lab, run_time=0.25), GrowArrow(ift_arr),
                  FadeIn(core_lab, run_time=0.25), GrowArrow(core_arr),
                  phase.animate.set_value(1.0), run_time=1.3, rate_func=linear)
        self.play(phase.animate.set_value(5.8), run_time=5.7, rate_func=linear)
        self.finish()


def _cell_stage():
    """Shared cell geometry for s03, s04, s10."""
    return build_cilium_cell(cx=0.0, mem_y=-1.45, cil_h=4.35, cil_w=1.32, mem_half_w=5.5, nuc_h=1.90)


class S03OffInCilium(SpokenScene):
    """Without Hedgehog: Patched sits in ciliary membrane keeping sterol out; Smoothened waits
    outside; kinases+proteasome trim Gli3 to repressor which moves into nucleus -> Genes OFF."""
    def construct(self):
        cell = _cell_stage()
        phase = ValueTracker(0.0)
        shuttles = make_ift_shuttles(0.0, 0.22, -1.35, 2.25, phase, n_per_side=3, cargo_w=0.22, cargo_h=0.28)
        state_pill = boxed_label("No Hedgehog", PTCH_COL, size=28, pad=0.14).move_to([-4.6, 3.05, 0])
        self.add(cell, shuttles, state_pill, scope_tag("schematic", color=TEXT))

        comp_ring = RoundedRectangle(corner_radius=0.55, width=1.68, height=4.55,
                                     stroke_color=CILIUM_COL, stroke_width=3.5, stroke_opacity=0.88).move_to([0, 0.72, 0])
        self.play(Create(comp_ring), phase.animate.set_value(2.2), run_time=2.5, rate_func=linear)
        self.play(Uncreate(comp_ring), phase.animate.set_value(4.0), run_time=2.0, rate_func=linear)
        rest = max(0.3, self.t_of("patched sits") - 0.2 - self.elapsed())
        self.play(phase.animate.set_value(4.0 + rest * 0.9), run_time=rest, rate_func=linear)

        self.at("patched sits")
        ptch_l = build_patched([-0.66, 1.35, 0], scale=0.85, active=True)
        ptch_r = build_patched([0.66, 1.35, 0], scale=0.85, active=True)
        l_ptch = T("Patched", 28, PTCH_COL).move_to([-3.15, 2.15, 0])
        arr_ptch = Arrow(l_ptch.get_right() + RIGHT * 0.1, [-0.90, 1.52, 0], buff=0, color=PTCH_COL, stroke_width=3)

        sterol_pts = [
            [-1.35, 1.75, 0],
            [-1.62, 1.38, 0],
            [-1.28, 1.05, 0],
            [-1.58, 0.72, 0],
        ]
        sterols = VGroup(*[
            RegularPolygon(4, radius=0.12, stroke_color=STEROL_COL, stroke_width=2.2,
                           fill_color=STEROL_COL, fill_opacity=0.92).move_to(pt)
            for pt in sterol_pts
        ])
        l_sterol = T("Sterol kept out", 26, STEROL_COL).move_to([-3.65, 0.35, 0])

        self.play(FadeIn(ptch_l), FadeIn(ptch_r), FadeIn(l_ptch, run_time=0.25), GrowArrow(arr_ptch),
                  FadeIn(sterols), FadeIn(l_sterol, run_time=0.25),
                  phase.animate.set_value(7.3), run_time=1.3, rate_func=linear)
        self.play(
            *[s.animate.shift(LEFT * 0.45) for s in sterols],
            phase.animate.set_value(8.8),
            run_time=1.6, rate_func=linear,
        )

        self.at("outside in the cell body")
        smo_l = build_smoothened([-2.8, -1.45, 0], scale=0.9, on=False)
        smo_r = build_smoothened([2.8, -1.45, 0], scale=0.9, on=False)
        l_smo = T("Smoothened (outside, OFF)", 26, SMO_COL).move_to([3.65, -0.55, 0])
        arr_smo = Arrow(l_smo.get_bottom() + DOWN * 0.08, [2.85, -1.12, 0], buff=0, color=SMO_COL, stroke_width=3)
        self.play(FadeIn(smo_l), FadeIn(smo_r), FadeIn(l_smo, run_time=0.25), GrowArrow(arr_smo),
                  phase.animate.set_value(10.5), run_time=1.8, rate_func=linear)
        rest2 = max(0.2, self.t_of("trimming glee") - 0.2 - self.elapsed())
        if rest2 > 0.25:
            self.play(phase.animate.set_value(10.5 + rest2 * 0.9), run_time=rest2, rate_func=linear)

        self.at("trimming glee")
        trimmer = boxed_label("Kinases +\nproteasome", KINASE_COL, size=24, pad=0.12).move_to([4.05, -2.15, 0])
        gli3 = build_gli_full([0.0, -0.25, 0], scale=0.75)
        l_gli3 = T("Gli3", 26, GLI_COL).move_to([1.50, -1.84, 0])
        l_gli3_note = boxed_label("Gli3 = main repressor form", GLI_REP_COL, size=24, pad=0.12).move_to([3.75, 1.55, 0])
        path_gli3 = VMobject().set_points_as_corners([
            np.array([0.0, -0.25, 0]),
            np.array([0.0, -1.45, 0]),
            np.array([1.50, -2.18, 0]),
        ])
        self.play(FadeIn(trimmer, run_time=0.25), FadeIn(gli3),
                  phase.animate.set_value(12.2), run_time=1.0, rate_func=linear)
        self.play(
            MoveAlongPath(gli3, path_gli3),
            FadeIn(l_gli3, run_time=0.35),
            phase.animate.set_value(13.3), run_time=1.1, rate_func=linear,
        )
        self.at("glee iii")
        rep = build_gli_repressor([1.50, -2.18, 0], scale=0.85)
        l_rep = T("Gli3 repressor", 24, GLI_REP_COL).move_to([1.50, -1.84, 0])
        self.play(
            FadeIn(l_gli3_note, run_time=0.3),
            FadeOut(gli3.back, shift=RIGHT * 0.25),
            Transform(gli3.front, rep),
            swap(l_gli3, l_rep, run_time=0.45),
            phase.animate.set_value(15.0), run_time=1.6, rate_func=linear,
        )

        self.at("quiet cells")
        self.play(
            FadeOut(l_rep, run_time=0.35),
            gli3.front.animate.move_to([1.45, -2.88, 0]),
            phase.animate.set_value(16.2), run_time=1.3, rate_func=linear,
        )
        l_rep_nuc = T("Gli3 repressor", 24, GLI_REP_COL).move_to([1.50, -2.15, 0])
        self.play(
            FadeIn(l_rep_nuc, run_time=0.35),
            phase.animate.set_value(18.2), run_time=2.2, rate_func=linear,
        )
        self.finish()


class S04OnInCilium(SpokenScene):
    """When Hedgehog binds Patched, traffic reverses: Patched exits, Smoothened enters and
    switches ON, full-length Gli gathers at the tip, escapes trimming, and activates Genes ON."""
    def construct(self):
        cell = _cell_stage()
        phase = ValueTracker(0.0)
        shuttles = make_ift_shuttles(0.0, 0.22, -1.35, 2.25, phase, n_per_side=3, cargo_w=0.22, cargo_h=0.28)
        state_pill = boxed_label("No Hedgehog", PTCH_COL, size=28, pad=0.14).move_to([-4.6, 3.05, 0])

        ptch_l = build_patched([-0.66, 1.35, 0], scale=0.85, active=True)
        ptch_r = build_patched([0.66, 1.35, 0], scale=0.85, active=True)
        smo_l = build_smoothened([-2.8, -1.45, 0], scale=0.9, on=False)
        smo_r = build_smoothened([2.8, -1.45, 0], scale=0.9, on=False)
        trimmer = boxed_label("Kinases +\nproteasome", KINASE_COL, size=24, pad=0.12).move_to([4.05, -2.15, 0])

        self.add(cell, shuttles, state_pill, ptch_l, ptch_r, smo_l, smo_r, trimmer, scope_tag("schematic", color=TEXT))

        self.at("when hedgehog binds")
        hh_l = build_hedgehog([-2.0, 2.35, 0], scale=0.95)
        hh_r = build_hedgehog([2.0, 2.35, 0], scale=0.95)
        l_hh = T("Hedgehog", 28, HH_COL).move_to([-3.3, 2.35, 0])
        plus_pill = boxed_label("+ Hedgehog", HH_COL, size=28, pad=0.14).move_to([-4.6, 3.05, 0])
        self.play(FadeIn(hh_l), FadeIn(hh_r), FadeIn(l_hh, run_time=0.25), swap(state_pill, plus_pill, run_time=0.45),
                  phase.animate.set_value(1.1), run_time=1.2, rate_func=linear)
        self.play(
            hh_l.animate.move_to([-1.00, 1.45, 0]),
            hh_r.animate.move_to([1.00, 1.45, 0]),
            l_hh.animate.move_to([-2.4, 2.1, 0]),
            phase.animate.set_value(2.9), run_time=2.0, rate_func=linear,
        )

        self.at("patched exits")
        l_ptch_out = T("Patched exits", 26, PTCH_COL).move_to([-3.75, -0.45, 0])
        self.play(
            VGroup(ptch_l, hh_l).animate.move_to([-1.85, -1.45, 0]),
            VGroup(ptch_r, hh_r).animate.move_to([1.85, -1.45, 0]),
            FadeIn(l_ptch_out, run_time=0.25),
            phase.animate.set_value(4.5), run_time=1.8, rate_func=linear,
        )
        self.play(
            FadeOut(ptch_l), FadeOut(hh_l), FadeOut(ptch_r), FadeOut(hh_r), FadeOut(l_hh), FadeOut(l_ptch_out),
            phase.animate.set_value(5.3), run_time=0.8, rate_func=linear,
        )

        self.at("moves inside")
        smo_l_on = build_smoothened([-0.66, 1.05, 0], scale=0.85, on=True)
        smo_r_on = build_smoothened([0.66, 1.05, 0], scale=0.85, on=True)
        l_smo = T("Smoothened ON", 28, SMO_COL).move_to([-3.25, 1.05, 0])
        arr_smo = Arrow(l_smo.get_right() + RIGHT * 0.1, [-0.98, 1.05, 0], buff=0, color=SMO_COL, stroke_width=3)
        path_smo_l = VMobject().set_points_as_corners([
            np.array([-2.8, -1.45, 0]),
            np.array([-0.66, -1.45, 0]),
            np.array([-0.66, 1.05, 0]),
        ])
        path_smo_r = VMobject().set_points_as_corners([
            np.array([2.8, -1.45, 0]),
            np.array([0.66, -1.45, 0]),
            np.array([0.66, 1.05, 0]),
        ])
        self.play(
            MoveAlongPath(smo_l, path_smo_l),
            MoveAlongPath(smo_r, path_smo_r),
            FadeOut(trimmer),
            phase.animate.set_value(6.8), run_time=1.6, rate_func=linear,
        )
        self.play(
            Transform(smo_l, smo_l_on),
            Transform(smo_r, smo_r_on),
            FadeIn(l_smo, run_time=0.25), GrowArrow(arr_smo),
            phase.animate.set_value(8.1), run_time=1.4, rate_func=linear,
        )

        self.at("gather at the")
        gli_a = build_gli_full([-0.15, 0.25, 0], scale=0.65)
        gli_b = build_gli_full([0.15, 0.75, 0], scale=0.65)
        l_gli = T("Full-length Gli", 28, GLI_COL).move_to([-3.3, 2.35, 0])
        arr_gli = Arrow(l_gli.get_right() + RIGHT * 0.1, [-0.60, 2.55, 0], buff=0, color=GLI_COL, stroke_width=3)
        self.play(
            FadeIn(gli_a), FadeIn(gli_b),
            gli_a.animate.move_to([-0.08, 2.58, 0]),
            gli_b.animate.move_to([0.08, 2.32, 0]),
            FadeIn(l_gli, run_time=0.25), GrowArrow(arr_gli),
            phase.animate.set_value(10.1), run_time=2.2, rate_func=linear,
        )

        self.at("travel to the nucleus")
        genes_on = boxed_label("Genes ON", ON_COL, size=26, pad=0.13).move_to(cell.gene_pos)
        l_act = T("Activators", 26, ON_COL).move_to([2.45, -2.20, 0])
        path_gli_a = VMobject().set_points_as_corners([
            np.array([-0.08, 2.58, 0]),
            np.array([0.0, -1.45, 0]),
            np.array([0.0, -2.58, 0]),
            np.array([1.40, -2.85, 0]),
        ])
        path_gli_b = VMobject().set_points_as_corners([
            np.array([0.08, 2.32, 0]),
            np.array([0.0, -1.45, 0]),
            np.array([0.0, -2.58, 0]),
            np.array([-1.40, -2.85, 0]),
        ])
        self.play(
            FadeOut(l_gli, run_time=0.4),
            FadeOut(arr_gli, run_time=0.4),
            MoveAlongPath(gli_a, path_gli_a),
            MoveAlongPath(gli_b, path_gli_b),
            swap(cell.gene_pill, genes_on, run_time=0.45),
            FadeIn(l_act, run_time=0.25),
            phase.animate.set_value(12.4), run_time=2.5, rate_func=linear,
        )

        self.at("both sides")
        badge = boxed_label("Cilium needed for both forms", CILIUM_COL, size=28, pad=0.15).move_to([3.55, 2.95, 0])
        self.play(FadeIn(badge, run_time=0.3), phase.animate.set_value(15.5), run_time=3.4, rate_func=linear)
        self.finish()


class S05ChainLogic(SpokenScene):
    """Cilium cross-section sits on the left while the horizontal pathway chain builds across the top;
    a signal pulse travels left-to-right along a track below the chain and halts at a downstream barrier."""
    def construct(self):
        cell = build_cilium_cell(cx=-3.05, mem_y=-1.75, cil_h=2.95, cil_w=0.95, mem_half_w=2.95, nuc_h=1.45,
                                 pill_text="Genes ON", pill_col=ON_COL, pill_size=24, pill_pad=0.11, cyto_h=1.65)
        phase = ValueTracker(0.0)
        shuttles = make_ift_shuttles(-3.05, 0.16, -1.65, 0.85, phase, n_per_side=3, cargo_w=0.20, cargo_h=0.26)
        smo_l = build_smoothened([-3.52, -0.05, 0], scale=0.65, on=True)
        smo_r = build_smoothened([-2.58, -0.05, 0], scale=0.65, on=True)
        self.add(cell, shuttles, smo_l, smo_r, scope_tag("schematic", color=TEXT))

        chain = build_chain(top_y=2.55, left_x=-6.4, right_x=6.4, font_size=24, pad=0.12)
        cil_link = DashedLine(chain.smo.get_bottom() + DOWN * 0.06, [-3.05, 1.25, 0],
                              color=SMO_COL, stroke_width=2.5, dash_length=0.12)
        self.play(phase.animate.set_value(2.2), run_time=2.5, rate_func=linear)

        self.at("hedgehog turns off")
        self.play(FadeIn(chain.hh, run_time=0.25), Create(chain.links[0]), FadeIn(chain.ptch, run_time=0.25),
                  phase.animate.set_value(3.6), run_time=1.5, rate_func=linear)

        self.at("holds back")
        self.play(Create(chain.links[1]), FadeIn(chain.smo, run_time=0.25), Create(cil_link),
                  phase.animate.set_value(5.0), run_time=1.5, rate_func=linear)

        self.at("governs")
        self.play(Create(chain.links[2]), FadeIn(chain.gli, run_time=0.25), Create(chain.links[3]),
                  FadeIn(chain.genes, run_time=0.25), phase.animate.set_value(6.6), run_time=1.8, rate_func=linear)

        self.at("in a linear chain")
        xs = [n.get_center()[0] for n in chain.nodes]
        track_y = 1.92
        sig_track = Line([xs[0], track_y, 0], [xs[-1], track_y, 0], color=CILIUM_COL, stroke_width=2.5, stroke_opacity=0.55)
        ticks = VGroup(*[Line([x, track_y, 0], [x, chain.top_y - 0.34, 0], color=CILIUM_COL, stroke_width=2.0, stroke_opacity=0.55)
                         for x in xs])
        u = ValueTracker(0.0)
        p_dot = always_redraw(lambda: Dot([xs[0] + u.get_value() * (xs[-1] - xs[0]), track_y, 0],
                                          radius=0.15, color=HH_COL, stroke_color=TEXT, stroke_width=2.5))
        self.play(Create(sig_track), Create(ticks), run_time=0.4)
        self.add(p_dot)
        self.play(u.animate.set_value(1.0), phase.animate.set_value(8.4), run_time=2.0, rate_func=linear)
        self.remove(p_dot)

        self.at("a block or fault")
        bar_x = (chain.smo.get_right()[0] + chain.gli.get_left()[0]) / 2.0
        barrier = VGroup(
            Line([bar_x, track_y - 0.25, 0], [bar_x, track_y + 0.28, 0], color=DRUG_EDGE, stroke_width=6),
            boxed_label("Downstream block", DRUG_EDGE, size=24, pad=0.12).move_to([bar_x, 1.25, 0]),
        )
        u2 = ValueTracker(0.0)
        p_dot2 = always_redraw(lambda: Dot([xs[0] + u2.get_value() * (bar_x - xs[0] - 0.14), track_y, 0],
                                           radius=0.15, color=HH_COL, stroke_color=TEXT, stroke_width=2.5))
        rule_txt = boxed_label("Later block overrides upstream", DRUG_EDGE, size=28, pad=0.15).move_to([3.0, -0.45, 0])
        gli_blocked = boxed_label("Gli OFF", GLI_REP_COL, size=24, box=(1.35, 0.56), pad=0.12, fill_opacity=0.06).move_to(chain.gli.get_center())
        genes_off = boxed_label("Genes OFF", PTCH_COL, size=24, box=(1.85, 0.56), pad=0.12, fill_opacity=0.06).move_to(chain.genes.get_center())
        cell_genes_off = boxed_label("Genes OFF", PTCH_COL, size=24, pad=0.11).move_to(cell.gene_pos)
        self.play(FadeIn(barrier, run_time=0.3), run_time=0.5)
        self.add(p_dot2)
        self.play(
            u2.animate.set_value(1.0),
            FadeIn(rule_txt, run_time=0.3),
            phase.animate.set_value(10.6),
            run_time=2.4, rate_func=linear,
        )
        self.play(
            swap(chain.gli, gli_blocked, run_time=0.45),
            swap(chain.genes, genes_off, run_time=0.45),
            swap(cell.gene_pill, cell_genes_off, run_time=0.45),
            phase.animate.set_value(12.0),
            run_time=1.4, rate_func=linear,
        )
        self.finish()


def build_predict_backdrop():
    """Exact static state at end of s06_embryo_predict and throughout s07_pause."""
    chain = build_chain(top_y=2.68, left_x=-6.4, right_x=6.4, font_size=24, pad=0.12,
                        ptch_text="Patched OFF", ptch_off=True,
                        smo_text="Smoothened OFF", smo_off=True)
    wedge = build_drug_wedge(chain.smo.get_bottom() + DOWN * 0.16, scale=0.95).rotate(-PI / 2)
    cyc_lab = T("Cyclopamine", 24, DRUG_EDGE).next_to(wedge, DOWN, buff=0.08)

    brain = build_forebrain(cx=-0.35, cy=-0.45, w=4.6, h=3.15)
    eye = Ellipse(width=1.78, height=0.76, stroke_color=TEXT, stroke_width=3.5,
                  fill_color="#DCE7F5", fill_opacity=0.88).move_to([brain.cx, brain.eye_y, 0])
    waves = VGroup(*[
        Arc(radius=0.25 + 0.38 * k, start_angle=PI * 0.20, angle=PI * 0.60,
            arc_center=brain.shh_src.get_center(), color=HH_COL, stroke_width=4.8)
        for k in range(3)
    ])
    return VGroup(chain, wedge, cyc_lab, brain, eye, waves)


class S06EmbryoPredict(SpokenScene):
    """Forebrain starts with one central eye field; midline Shh switches Smoothened on to divide it;
    resets to one oval as Cyclopamine locks Smoothened off while Shh still arrives; asks question."""
    def construct(self):
        chain = build_chain(top_y=2.68, left_x=-6.4, right_x=6.4, font_size=24, pad=0.12)
        brain = build_forebrain(cx=-0.35, cy=-0.45, w=4.6, h=3.15)
        sep = ValueTracker(0.0)
        eye_live = live_eye_field(brain, sep)
        wave_t = ValueTracker(0.0)
        waves = make_shh_waves(brain.shh_src.get_center(), wave_t)

        self.add(chain)
        self.play(FadeIn(brain.outline), FadeIn(brain.brain_lab, run_time=0.25),
                  FadeIn(brain.shh_src), FadeIn(brain.shh_lab, run_time=0.25), run_time=2.5)

        self.at("the forebrain starts")
        self.play(FadeIn(eye_live), Create(brain.midline), run_time=2.0)

        self.at("sonic hedgehog")
        ptch_off = boxed_label("Patched OFF", PTCH_COL, size=24, box=(2.05, 0.56), pad=0.12, fill_opacity=0.06).move_to(chain.ptch.get_center())
        self.add(waves)
        self.play(
            wave_t.animate.set_value(0.5),
            swap(chain.ptch, ptch_off, run_time=0.5),
            run_time=0.5, rate_func=linear,
        )
        self.play(
            wave_t.animate.set_value(4.5),
            run_time=4.0, rate_func=linear,
        )

        self.at("to split")
        self.play(sep.animate.set_value(1.0), wave_t.animate.set_value(7.1), run_time=2.6, rate_func=linear)

        self.at("now predict")
        self.play(sep.animate.set_value(0.0), wave_t.animate.set_value(8.9), run_time=1.8, rate_func=linear)

        self.at("cyclopamine locks")
        smo_off = boxed_label("Smoothened OFF", SMO_COL, size=24, box=(2.70, 0.56), pad=0.12, fill_opacity=0.06).move_to(chain.smo.get_center())
        wedge = build_drug_wedge(smo_off.get_bottom() + DOWN * 0.58, scale=0.95).rotate(-PI / 2)
        cyc_lab = T("Cyclopamine", 24, DRUG_EDGE).next_to(wedge, DOWN, buff=0.08)
        self.play(
            FadeIn(wedge, run_time=0.3), FadeIn(cyc_lab, run_time=0.25),
            wedge.animate.move_to(smo_off.get_bottom() + DOWN * 0.16),
            cyc_lab.animate.next_to(smo_off.get_bottom() + DOWN * 0.16, DOWN, buff=0.20),
            swap(chain.smo, smo_off, run_time=0.45),
            wave_t.animate.set_value(10.7),
            run_time=1.8, rate_func=linear,
        )

        self.at("while sonic hedgehog")
        self.play(wave_t.animate.set_value(13.1), run_time=2.4, rate_func=linear)

        self.at("will the eye field")
        q = question_card("Smoothened locked off: divide or stay one?", left=-5.8, y=-2.95, size=30, max_w=10.5)
        self.play(FadeIn(q, run_time=0.3), wave_t.animate.set_value(15.6), run_time=2.5, rate_func=linear)
        self.finish()


class S07Pause(PredictPause):
    QUESTION = "Smoothened locked off: divide or stay one?"
    CARD = {"left": -5.8, "y": -2.95, "size": 30, "max_w": 10.5}
    RING_AT = (5.9, -3.0, 0)
    SECONDS = 4.5

    def backdrop(self):
        return build_predict_backdrop()


class S08Reveal(SpokenScene):
    """Eye field stays undivided; midline Shh waves continue arriving while upstream signal turns off
    Patched and halts at Cyclopamine-locked Smoothened; sheep defect points to Smoothened."""
    def construct(self):
        bd = build_predict_backdrop()
        chain, wedge, cyc_lab, brain, eye, static_waves = bd
        q = question_card("Smoothened locked off: divide or stay one?", left=-5.8, y=-2.95, size=30, max_w=10.5)
        wave_t = ValueTracker(0.0)
        live_waves = make_shh_waves(brain.shh_src.get_center(), wave_t)
        self.add(bd, q)
        self.remove(static_waves)
        self.add(live_waves)

        ans = boxed_label("Single eye field (undivided)", HH_COL, size=28, pad=0.14).move_to([-0.35, -3.0, 0])
        self.play(swap(q, ans, run_time=0.5), eye.animate.set_stroke(HH_COL, width=5.5),
                  wave_t.animate.set_value(2.0), run_time=1.8, rate_func=linear)
        self.play(wave_t.animate.set_value(4.5), run_time=2.4, rate_func=linear)

        self.at("turns off patched")
        xs = [n.get_center()[0] for n in chain.nodes]
        track_y = 2.15
        sig_track = Line([xs[0], track_y, 0], [xs[2] - 0.15, track_y, 0], color=CILIUM_COL, stroke_width=2.5, stroke_opacity=0.45)
        p_u = ValueTracker(0.0)
        p_beam = always_redraw(lambda: Line([xs[0], track_y, 0],
                                            [xs[0] + max(0.02, p_u.get_value()) * (xs[2] - 0.15 - xs[0]), track_y, 0],
                                            color=HH_COL, stroke_width=5.0))
        p_dot = always_redraw(lambda: Dot([xs[0] + p_u.get_value() * (xs[2] - 0.15 - xs[0]), track_y, 0],
                                          radius=0.14, color=HH_COL, stroke_color=TEXT, stroke_width=2.5))
        self.play(Create(sig_track), wave_t.animate.set_value(5.0), run_time=0.45, rate_func=linear)
        self.add(p_beam, p_dot)
        self.play(p_u.animate.set_value(0.55), wave_t.animate.set_value(8.5), run_time=3.3, rate_func=linear)

        self.at("locking smoothened off")
        self.play(p_u.animate.set_value(0.95), wave_t.animate.set_value(10.4), run_time=1.8, rate_func=linear)
        gli_r = boxed_label("Gli3R", GLI_REP_COL, size=24, box=(1.35, 0.56), pad=0.12).move_to(chain.gli.get_center())
        genes_off = boxed_label("Genes OFF", PTCH_COL, size=24, box=(1.85, 0.56), pad=0.12).move_to(chain.genes.get_center())
        self.play(swap(chain.gli, gli_r, run_time=0.45), swap(chain.genes, genes_off, run_time=0.45),
                  wave_t.animate.set_value(12.2), run_time=1.8, rate_func=linear)

        self.at("grazing corn")
        sheep_card = boxed_label("Sheep single-eye\ndefect", HH_COL, size=24, pad=0.12).move_to([4.15, 0.95, 0])
        w_corn = T("Corn lily", 24, HH_COL)
        w_cyc = T("→ cyclopamine", 24, DRUG_EDGE)
        w_smo = T("→ Smoothened", 24, SMO_COL)
        row1 = VGroup(w_corn, w_cyc).arrange(RIGHT, buff=0.14).move_to([4.15, -0.10, 0])
        w_smo.move_to([4.15, -0.55, 0])
        self.play(FadeIn(sheep_card, run_time=0.25), FadeIn(w_corn, run_time=0.3),
                  wave_t.animate.set_value(14.5), run_time=2.2, rate_func=linear)

        self.at("cyclopamine")
        self.play(FadeIn(w_cyc, run_time=0.3), wave_t.animate.set_value(16.0), run_time=1.5, rate_func=linear)

        self.at("to smoothened")
        drug_tag = T("Smoothened =\ndrug target", 25, DRUG_EDGE, line_spacing=0.9).move_to([4.15, -1.45, 0])
        target_arr = Arrow(sheep_card.get_top() + LEFT * 0.4 + UP * 0.06,
                           chain.smo.get_bottom() + RIGHT * 0.9 + DOWN * 0.08,
                           buff=0, color=DRUG_EDGE, stroke_width=3.8)
        self.play(FadeIn(w_smo, run_time=0.3), GrowArrow(target_arr), FadeIn(drug_tag, run_time=0.3),
                  wave_t.animate.set_value(18.2), run_time=2.2, rate_func=linear)
        self.finish()


class S09TumourVismodegib(SpokenScene):
    """Side-by-side tumour cells: Left (Lost Patched -> Vismodegib locks Smoothened OFF -> Genes OFF);
    Right (Downstream fault -> Vismodegib locks Smoothened OFF, yet Gli fault keeps Genes ON)."""
    def construct(self):
        tp = TwoPanel("Lost Patched", "Downstream fault", colors=(PTCH_COL, GLI_COL), top=3.15, bottom=-2.45)
        lc, _, _ = tp.area("left")
        rc, _, _ = tp.area("right")
        l_cell = build_cilium_cell(cx=lc[0], mem_y=-0.60, cil_h=2.42, cil_w=0.90, mem_half_w=2.45, nuc_h=1.70,
                                   pill_text="Genes OFF", pill_col=PTCH_COL, pill_size=22, pill_pad=0.11,
                                   cyto_h=1.80, nuc_angle=-1.52)
        r_cell = build_cilium_cell(cx=rc[0], mem_y=-0.60, cil_h=2.42, cil_w=0.90, mem_half_w=2.45, nuc_h=1.70,
                                   pill_text="Target genes", pill_col=TEXT, pill_size=22, pill_pad=0.11,
                                   cyto_h=1.80, nuc_angle=-1.52)
        l_phase = ValueTracker(0.0)
        r_phase = ValueTracker(0.2)
        l_shuttles = make_ift_shuttles(lc[0], 0.15, -0.52, 1.40, l_phase, n_per_side=2, cargo_w=0.20, cargo_h=0.26)
        r_shuttles = make_ift_shuttles(rc[0], 0.15, -0.52, 1.40, r_phase, n_per_side=2, cargo_w=0.20, cargo_h=0.26)
        l_ptch_init = build_patched([lc[0] - 0.45, 0.65, 0], scale=0.72, active=True)

        # Start immediately with framed panels (no black frame at t = 0)
        self.add(tp.left_frame, tp.left_head, tp.right_frame, tp.right_head)
        self.play(FadeIn(l_cell), FadeIn(r_cell), FadeIn(l_ptch_init), run_time=1.4)
        self.add(l_shuttles, r_shuttles)
        self.play(l_phase.animate.increment_value(2.4), r_phase.animate.increment_value(2.4),
                  run_time=2.5, rate_func=linear)

        l_ptch = build_patched([lc[0] - 0.45, 0.65, 0], scale=0.72, missing=True)
        l_ptch_lab = T("Patched lost", 24, PTCH_COL).move_to([lc[0] - 1.72, 1.25, 0])
        l_smo = build_smoothened([lc[0] + 0.45, 0.55, 0], scale=0.72, on=True)
        l_smo_lab = T("Smoothened\nON", 24, SMO_COL, line_spacing=0.85).move_to([lc[0] + 1.80, 1.32, 0])
        l_genes_on = boxed_label("Genes ON", ON_COL, size=22, pad=0.11).move_to(l_cell.gene_pos)

        self.at("lose patched")
        self.play(
            Transform(l_ptch_init, l_ptch), FadeIn(l_ptch_lab, run_time=0.25),
            FadeIn(l_smo), FadeIn(l_smo_lab, run_time=0.25),
            swap(l_cell.gene_pill, l_genes_on, run_time=0.45),
            l_phase.animate.increment_value(1.8), r_phase.animate.increment_value(1.8),
            run_time=1.8, rate_func=linear,
        )
        for _ in range(2):
            dot_run = Dot([lc[0] + 0.45, 0.55, 0], radius=0.13, color=SMO_COL, stroke_color=TEXT, stroke_width=2.0)
            self.add(dot_run)
            self.play(dot_run.animate.move_to([lc[0] + 0.45, -1.05, 0]),
                      l_phase.animate.increment_value(1.8), r_phase.animate.increment_value(1.8),
                      run_time=1.8, rate_func=linear)
            self.remove(dot_run)

        self.at("binds smoothened")
        vismo = build_drug_wedge([lc[0] + 2.0, 0.55, 0], scale=0.85)
        l_vismo = T("Vismodegib", 24, DRUG_EDGE).move_to([lc[0] + 1.82, -0.10, 0])
        self.play(FadeIn(vismo, run_time=0.25), FadeIn(l_vismo, run_time=0.25),
                  vismo.animate.move_to([lc[0] + 0.68, 0.55, 0]),
                  l_phase.animate.increment_value(1.8), r_phase.animate.increment_value(1.8),
                  run_time=1.8, rate_func=linear)

        l_smo_off = build_smoothened([lc[0] + 0.45, 0.55, 0], scale=0.72, on=False)
        l_smo_off_lab = T("Smoothened\nOFF", 24, SMO_COL, line_spacing=0.85).move_to([lc[0] + 1.80, 1.32, 0])
        self.play(Transform(l_smo, l_smo_off), swap(l_smo_lab, l_smo_off_lab, run_time=0.45),
                  l_phase.animate.increment_value(2.0), r_phase.animate.increment_value(2.0),
                  run_time=2.0, rate_func=linear)

        self.at("silences the")
        l_genes_off = boxed_label("Genes OFF", PTCH_COL, size=22, pad=0.11).move_to(l_cell.gene_pos)
        self.play(swap(l_genes_on, l_genes_off, run_time=0.45),
                  l_phase.animate.increment_value(2.0), r_phase.animate.increment_value(2.0),
                  run_time=2.0, rate_func=linear)

        self.at("but if a")
        r_smo = build_smoothened([rc[0] + 0.45, 0.55, 0], scale=0.72, on=False)
        r_vismo = build_drug_wedge([rc[0] + 0.68, 0.55, 0], scale=0.85)
        r_vismo_lab = T("Vismodegib", 24, DRUG_EDGE).move_to([rc[0] + 1.82, 0.98, 0])
        gli_fault = boxed_label("Gli fault", GLI_COL, size=22, pad=0.10).move_to([rc[0] - 1.50, -1.02, 0])
        bypass_arr = Arrow([rc[0] - 1.25, -1.28, 0], [rc[0] - 0.75, -1.60, 0],
                           buff=0, color=GLI_COL, stroke_width=4.5)
        r_genes_on = boxed_label("Genes ON", ON_COL, size=22, pad=0.11).move_to(r_cell.gene_pos)
        fail_lab = boxed_label("Fault below Smoothened: drug fails", DRUG_EDGE, size=24, pad=0.12).move_to([rc[0], -2.95, 0])
        self.play(FadeIn(r_smo), FadeIn(r_vismo), FadeIn(r_vismo_lab, run_time=0.25),
                  FadeIn(gli_fault, run_time=0.25), GrowArrow(bypass_arr),
                  swap(r_cell.gene_pill, r_genes_on, run_time=0.45),
                  l_phase.animate.increment_value(1.6), r_phase.animate.increment_value(1.6),
                  run_time=1.6, rate_func=linear)
        for idx in range(2):
            f_dot = Dot(bypass_arr.get_start(), radius=0.13, color=GLI_COL, stroke_color=TEXT, stroke_width=2.0)
            self.add(f_dot)
            anims = [
                f_dot.animate.move_to(bypass_arr.get_end()),
                l_phase.animate.increment_value(1.0), r_phase.animate.increment_value(1.0),
            ]
            if idx == 1:
                anims.append(FadeIn(fail_lab, run_time=0.3))
            self.play(*anims, run_time=1.0, rate_func=linear)
            self.remove(f_dot)
        self.finish()


class S10Synthesis(SpokenScene):
    """Returns to one centered vertebrate cell with primary cilium (~70% height), Patched exiting and
    Smoothened entering beside the compact pathway chain, fly-cell note, and final rule."""
    def construct(self):
        cell = build_cilium_cell(cx=-2.35, mem_y=-1.45, cil_h=4.55, cil_w=1.35, mem_half_w=3.25, nuc_h=1.80)
        phase = ValueTracker(0.0)
        shuttles = make_ift_shuttles(-2.35, 0.23, -1.35, 2.40, phase, n_per_side=3, cargo_w=0.22, cargo_h=0.28)

        ptch = build_patched([-3.02, 1.4, 0], scale=0.85, active=True)
        smo = build_smoothened([-0.7, -1.45, 0], scale=0.85, on=False)
        gli = build_gli_full([-2.35, 0.5, 0], scale=0.72)

        self.add(cell, shuttles, ptch, smo, gli, scope_tag("schematic", color=TEXT))
        self.play(phase.animate.set_value(3.8), run_time=3.8, rate_func=linear)

        self.at("gathers patched")
        smo_on = build_smoothened([-1.68, 1.1, 0], scale=0.85, on=True)
        genes_on = boxed_label("Genes ON", ON_COL, size=26, pad=0.13).move_to(cell.gene_pos)
        hub_lab = T("Primary\ncilium hub", 28, CILIUM_COL, line_spacing=0.9).move_to([-4.65, 2.05, 0])
        path_ptch = VMobject().set_points_as_corners([
            np.array([-3.02, 1.4, 0]),
            np.array([-3.02, -1.45, 0]),
            np.array([-4.15, -1.45, 0]),
        ])
        path_smo = VMobject().set_points_as_corners([
            np.array([-0.7, -1.45, 0]),
            np.array([-1.68, -1.45, 0]),
            np.array([-1.68, 1.1, 0]),
        ])
        self.play(
            MoveAlongPath(ptch, path_ptch),
            MoveAlongPath(smo, path_smo),
            gli.animate.move_to([-2.35, 2.52, 0]),
            FadeIn(hub_lab, run_time=0.25),
            phase.animate.set_value(6.6),
            run_time=2.8, rate_func=linear,
        )
        self.play(
            ptch.animate.set_opacity(0.35),
            Transform(smo, smo_on),
            swap(cell.gene_pill, genes_on, run_time=0.45),
            phase.animate.set_value(8.4),
            run_time=1.8, rate_func=linear,
        )

        self.at("most fly cells")
        fly_note = boxed_label("Most fly cells lack a cilium", CILIUM_COL, size=26, pad=0.14).move_to([3.45, -1.65, 0])
        self.play(FadeIn(fly_note, run_time=0.25), phase.animate.set_value(10.8), run_time=2.4, rate_func=linear)

        self.at("along that chain")
        chain = build_chain(top_y=1.95, left_x=-0.65, right_x=6.05, font_size=24, pad=0.10,
                            smo_text="Smoothened", show_genes=False, fixed_boxes=False)
        self.play(FadeIn(chain, run_time=0.3), phase.animate.set_value(12.6), run_time=1.8, rate_func=linear)

        xs = [n.get_center()[0] for n in chain.nodes]
        track_y = 1.38
        sig_track = Line([xs[0], track_y, 0], [xs[3], track_y, 0], color=CILIUM_COL, stroke_width=2.5, stroke_opacity=0.45)
        bar_x = (chain.smo.get_right()[0] + chain.gli.get_left()[0]) / 2.0
        barrier = Line([bar_x, track_y - 0.22, 0], [bar_x, chain.top_y + 0.24, 0], color=DRUG_EDGE, stroke_width=6)
        block_tag = T("Block", 22, DRUG_EDGE).next_to(barrier, DOWN, buff=0.08)
        u = ValueTracker(0.0)
        p_dot = always_redraw(lambda: Dot([xs[0] + u.get_value() * (bar_x - xs[0] - 0.14), track_y, 0],
                                          radius=0.12, color=HH_COL, stroke_color=TEXT, stroke_width=2.5))
        gli_off = boxed_label("Gli OFF", GLI_REP_COL, size=24, pad=0.10, fill_opacity=0.06).move_to(chain.gli.get_center()).align_to(chain.gli, LEFT)
        self.add(sig_track, p_dot)
        self.play(FadeIn(barrier, run_time=0.3), FadeIn(block_tag, run_time=0.3), phase.animate.set_value(13.0), run_time=0.4, rate_func=linear)
        self.play(u.animate.set_value(1.0), phase.animate.set_value(15.2), run_time=2.2, rate_func=linear)
        self.play(
            swap(chain.gli, gli_off, run_time=0.45),
            chain.links[2].animate.set_opacity(0.35),
            phase.animate.set_value(15.8), run_time=0.6, rate_func=linear,
        )

        self.at("houses the switch")
        ring = RoundedRectangle(corner_radius=0.75, width=2.15, height=4.95,
                                stroke_color=CILIUM_COL, stroke_width=3.5).move_to([-2.35, 0.72, 0])
        rule_box = boxed_label("Downstream steps decide", DRUG_EDGE, size=28, pad=0.15).move_to([3.0, 0.05, 0])
        self.play(Create(ring), FadeIn(rule_box, run_time=0.3), phase.animate.set_value(19.3), run_time=3.5, rate_func=linear)
        self.finish()


class S11End(EndCard):
    LINE = "In vertebrates the cilium houses the switch, and downstream steps decide."
