"""One Cut, Two Destinations — PLC, IP3, DAG and Protein Kinase C.

COLOUR MAP (one colour per concept, carried across both films):
    PIP2             GOLD    (#D4A843)
    IP3              BLUE    (#58C4DD)
    DAG              ORANGE  (#F28C38)
    calcium          GREEN   (#83C167)
    PLC              WHITE   (#FFFFFF)
    conventional PKC TEAL    (#3FB8C0)
    Gq route         PURPLE  (#B185FF)
    RTK route        MAGENTA (#F062A2)

CARRIED WORLD:
    16:9 schematic cell cross-section: curved plasma-membrane bilayer across the upper third
    (outside above, watery cytosol below), and a curved ER sac across the lower third holding
    dense green calcium ions. Zoomed scenes keep the exact same orientation (outside up,
    cytosol down).

WHAT CHANGES IN EACH SCENE (computed / subject-driven, zero ambient filler):
    s00_hook        PIP2 cut flashes; bold inward and surface signal packets advance along diverging paths; camera/highlight traces the plasma membrane closely around the cell.
    s01_title       Standard TitleCard ("One Cut, Two Destinations", 2.0 s).
    s02_substrate   Camera zooms into the bilayer; PIP2 expands into charged head + two oily tails; tails flex inside core and head bobs into cytosol as named; PLC clamp glides steadily across cytosol to the cut junction.
    s03_predict     PLC clamp closes across the junction; bright cut flash separates BLUE IP3 head from ORANGE DAG tails at the same membrane patch; question card appears; test-focus alternates cleanly between IP3 and DAG.
    s04_pause       Standard PredictPause (4.5 s) holding the separated products and countdown ring.
    s05_destinations Question fades; camera pulls back to full cell; 3 phosphate badges mark IP3; IP3 diffuses along a computed curved cytosol path toward ER while DAG diffuses laterally along the inner leaflet.
    s06_two_routes  Left: GPCR activates Gq circle carrying PLC-beta from cytosol to left PIP2. Right: RTK dimerizes, displays P badges, docks PLC-gamma via SH2 (held idle with brake closed while kinase engages), kinase transfers P, brake swings open, PLC-gamma moves to right PIP2; both cut simultaneously releasing IP3 to ER and leaving DAG.
    s07_er_channel  Camera pans down from plasma membrane (DAG) following IP3 across cytosol to zoomed ER channel gate; IP3 binds socket and stays outside while ER Ca2+ ions circulate toward gate; gate opens and computed flow simulation (rng seed 7) drives dense ER Ca2+ dots out into cytosol.
    s08_experiment  Intact cell highlights sealed compartments, then plasma membrane opens 4 permeabilization gaps while internal store and grey mitochondrion stay sealed; added IP3 enters without hormone and releases a computed Ca2+ plume from the internal store only; final beat renames store to ER.
    s09_rule        Full cell + compact 8-colour legend; IP3 route + Ca2+ plume animate under "mobile branch"; DAG slides along membrane under "local branch"; both trace back to one PIP2 cut.
    s10_end         Standard EndCard ("One PIP2 cut sends IP3 away and leaves DAG at the membrane.").
"""
from bp_parts import *

# ---- Concept colour map ----
C_PIP2 = GOLD
C_IP3 = BLUE
C_DAG = "#F28C38"       # ORANGE, crisp high contrast on dark BG
C_CA = GREEN
C_PLC = WHITE
C_PKC = TEAL
C_GQ = "#B185FF"        # PURPLE, crisp high contrast on dark BG
C_RTK = "#F062A2"       # MAGENTA, crisp high contrast on dark BG
MEM_FILL = "#253042"
MEM_EDGE = "#7A8CA8"
ER_FILL = "#1B3338"
ER_EDGE = "#4E8E96"


# ---- Carried world builders ----
def membrane_y_inner(x):
    """Y coordinate of the inner leaflet surface in macro cell coordinates."""
    return 1.75 - 0.014 * (x ** 2)


def membrane_y_outer(x):
    """Y coordinate of the outer leaflet surface in macro cell coordinates."""
    return 2.30 - 0.014 * (x ** 2)


def build_plasma_membrane(x_min=-6.3, x_max=6.3, n=48):
    """Curved plasma-membrane bilayer polygon + crisp outer/inner leaflet lines."""
    xs = np.linspace(x_min, x_max, n)
    top_pts = [[x, membrane_y_outer(x), 0] for x in xs]
    bot_pts = [[x, membrane_y_inner(x), 0] for x in reversed(xs)]
    band = Polygon(*(top_pts + bot_pts), stroke_width=0, fill_color=MEM_FILL, fill_opacity=0.85)
    outer_line = VMobject().set_points_smoothly([np.array(p) for p in top_pts]).set_stroke(MEM_EDGE, 3.5)
    inner_line = VMobject().set_points_smoothly([np.array([x, membrane_y_inner(x), 0]) for x in xs]).set_stroke(MEM_EDGE, 3.5)
    mid_line = VMobject().set_points_smoothly(
        [np.array([x, 0.5 * (membrane_y_inner(x) + membrane_y_outer(x)), 0]) for x in xs]
    ).set_stroke(MEM_EDGE, 1.5, opacity=0.45)
    return VGroup(band, mid_line, outer_line, inner_line)


def build_er_sac(center_y=-1.95, rx=4.1, ry=0.88):
    """Curved ER lumen sac across the lower third."""
    pts = []
    for a in np.linspace(0, TAU, 40, endpoint=False):
        x = rx * np.cos(a)
        y = center_y + ry * np.sin(a) + 0.12 * np.cos(2 * a)
        pts.append([x, y, 0])
    sac = Polygon(*pts, stroke_color=ER_EDGE, stroke_width=3.5, fill_color=ER_FILL, fill_opacity=0.85)
    sac.round_corners(radius=0.25)
    return sac


def build_er_ca_dots(n=26, seed=7, center_y=-1.95, rx=3.5, ry=0.62):
    """Resting calcium dots inside the ER sac (computed from fixed integer seed)."""
    rng = np.random.default_rng(seed)
    dots = VGroup()
    for _ in range(n):
        while True:
            x = rng.uniform(-rx, rx)
            y = rng.uniform(-ry, ry)
            if (x / rx) ** 2 + (y / ry) ** 2 <= 0.85:
                break
        dots.add(Dot([x, center_y + y + 0.06, 0], radius=0.065, color=C_CA))
    return dots


def build_macro_pip2(x=0.0, scale=1.0):
    """Compact PIP2 lipid in the macro inner leaflet (two tail bars up in bilayer, head down in cytosol)."""
    y0 = membrane_y_inner(x)
    t1 = Line([x - 0.09 * scale, y0 + 0.04 * scale, 0], [x - 0.09 * scale, y0 + 0.44 * scale, 0],
              color=C_PIP2, stroke_width=5 * scale)
    t2 = Line([x + 0.09 * scale, y0 + 0.04 * scale, 0], [x + 0.09 * scale, y0 + 0.44 * scale, 0],
              color=C_PIP2, stroke_width=5 * scale)
    neck = Line([x, y0 - 0.08 * scale, 0], [x, y0 + 0.06 * scale, 0], color=C_PIP2, stroke_width=4 * scale)
    head = RoundedRectangle(corner_radius=0.10 * scale, width=0.44 * scale, height=0.30 * scale,
                            stroke_color=C_PIP2, stroke_width=3, fill_color=C_PIP2, fill_opacity=0.32)
    head.move_to([x, y0 - 0.24 * scale, 0])
    g = VGroup(t1, t2, neck, head)
    g.tails = VGroup(t1, t2)
    g.neck = neck
    g.head = head
    return g


def build_zoomed_bilayer(x_min=-6.5, x_max=6.5, y_in=0.65, y_mid=1.55, y_out=2.45):
    """Zoomed plasma-membrane bilayer (outer leaflet y_mid..y_out, inner leaflet y_in..y_mid)."""
    outer_band = Polygon(
        [x_min, y_out, 0], [x_max, y_out, 0], [x_max, y_mid, 0], [x_min, y_mid, 0],
        stroke_width=0, fill_color=MEM_FILL, fill_opacity=0.65,
    )
    inner_band = Polygon(
        [x_min, y_mid, 0], [x_max, y_mid, 0], [x_max, y_in, 0], [x_min, y_in, 0],
        stroke_width=0, fill_color="#2D3C52", fill_opacity=0.80,
    )
    l_out = Line([x_min, y_out, 0], [x_max, y_out, 0], color=MEM_EDGE, stroke_width=3.5)
    l_mid = DashedLine([x_min, y_mid, 0], [x_max, y_mid, 0], color=MEM_EDGE, stroke_width=2, dash_length=0.22).set_opacity(0.6)
    l_in = Line([x_min, y_in, 0], [x_max, y_in, 0], color=MEM_EDGE, stroke_width=3.5)
    return VGroup(outer_band, inner_band, l_out, l_mid, l_in)


def build_zoomed_pip2(cx=0.0, y_in=0.65, head_color=C_PIP2, tail_color=C_PIP2, gap=0.0):
    """Two-part PIP2 (or separated IP3 head + DAG tails) in zoomed bilayer."""
    t1 = Line([cx - 0.22, y_in + 0.06, 0], [cx - 0.22, y_in + 0.82, 0], color=tail_color, stroke_width=10)
    t2 = Line([cx + 0.22, y_in + 0.06, 0], [cx + 0.22, y_in + 0.82, 0], color=tail_color, stroke_width=10)
    glyc = RoundedRectangle(corner_radius=0.08, width=0.72, height=0.22,
                            stroke_color=tail_color, stroke_width=3, fill_color=tail_color, fill_opacity=0.35)
    glyc.move_to([cx, y_in + 0.02, 0])
    tails_grp = VGroup(t1, t2, glyc)

    head_y = y_in - 0.34 - gap
    stem = Line([cx, y_in - 0.09, 0], [cx, head_y + 0.26, 0], color=head_color, stroke_width=6) if gap < 0.05 else VGroup()
    head = RoundedRectangle(corner_radius=0.14, width=0.92, height=0.56,
                            stroke_color=head_color, stroke_width=3.5, fill_color=head_color, fill_opacity=0.28)
    head.move_to([cx, head_y, 0])
    head_grp = VGroup(stem, head)
    g = VGroup(tails_grp, head_grp)
    g.tails_grp = tails_grp
    g.head_grp = head_grp
    g.head_box = head
    return g


def build_plc_clamp(label_text="PLC", open_amt=0.18, width=1.45, jaw_dy=0.0):
    """Plain clamp-shaped PLC enzyme block (no molecular structure)."""
    body = RoundedRectangle(corner_radius=0.18, width=width, height=0.66,
                            stroke_color=C_PLC, stroke_width=3, fill_color=C_PLC, fill_opacity=0.15)
    jaw_top = RoundedRectangle(corner_radius=0.07, width=0.42, height=0.18,
                               stroke_color=C_PLC, stroke_width=2.5, fill_color=C_PLC, fill_opacity=0.22)
    jaw_bot = RoundedRectangle(corner_radius=0.07, width=0.42, height=0.18,
                               stroke_color=C_PLC, stroke_width=2.5, fill_color=C_PLC, fill_opacity=0.22)
    jaw_top.next_to(body, RIGHT, buff=-0.02).shift(UP * (open_amt + jaw_dy))
    jaw_bot.next_to(body, RIGHT, buff=-0.02).shift(DOWN * open_amt + UP * jaw_dy)
    lbl = T(label_text, size=26, color=C_PLC, weight=BOLD).move_to(body)
    g = VGroup(body, jaw_top, jaw_bot, lbl)
    g.body = body
    g.jaw_top = jaw_top
    g.jaw_bot = jaw_bot
    g.lbl = lbl
    return g


def build_ip3_token(text="IP3", scale=1.0):
    """Soluble BLUE IP3 token."""
    box = RoundedRectangle(corner_radius=0.14 * scale, width=0.98 * scale, height=0.54 * scale,
                           stroke_color=C_IP3, stroke_width=3, fill_color=C_IP3, fill_opacity=0.26)
    lbl = T(text, size=max(24, int(round(26 * scale))), color=C_IP3, weight=BOLD).move_to(box)
    return VGroup(box, lbl)


def build_dag_token(x=0.0, y_fn=membrane_y_inner, text="DAG", scale=1.0):
    """Membrane-retained ORANGE DAG block anchored in the inner leaflet with generous box padding."""
    y0 = y_fn(x)
    t1 = Line([x - 0.14 * scale, y0 + 0.04 * scale, 0], [x - 0.14 * scale, y0 + 0.42 * scale, 0],
              color=C_DAG, stroke_width=6 * scale)
    t2 = Line([x + 0.14 * scale, y0 + 0.04 * scale, 0], [x + 0.14 * scale, y0 + 0.42 * scale, 0],
              color=C_DAG, stroke_width=6 * scale)
    base = RoundedRectangle(corner_radius=0.10 * scale, width=1.08 * scale, height=0.52 * scale,
                            stroke_color=C_DAG, stroke_width=3, fill_color=C_DAG, fill_opacity=0.28)
    base.move_to([x, y0 - 0.28 * scale, 0])
    lbl = T(text, size=max(24, int(round(24 * scale))), color=C_DAG, weight=BOLD).move_to(base)
    return VGroup(t1, t2, base, lbl)


def make_p_badge(size=22, radius=0.22):
    """Phosphorylated tyrosine / protein phosphate badge with generous clearance."""
    c = Circle(radius=radius, color=C_PIP2, stroke_width=2.5, fill_color=BG, fill_opacity=0.96)
    t = T("P", size, C_PIP2, weight=BOLD).move_to(c)
    return VGroup(c, t)


# ====================================================================
# SCENE 0: HOOK
# ====================================================================
class S00Hook(SpokenScene):
    def construct(self):
        mem = build_plasma_membrane()
        er = build_er_sac(center_y=-1.95, rx=4.1, ry=0.88)
        ca_dots = build_er_ca_dots(n=24, seed=7, center_y=-1.95, rx=3.5, ry=0.60)
        pip2 = build_macro_pip2(x=0.0, scale=1.15)
        pip2_lbl = T("PIP2", 30, C_PIP2, weight=BOLD).next_to(pip2.head, DOWN, buff=0.27)
        mem_lbl = T("plasma membrane", 28, TEXT).move_to([-4.2, 2.55, 0])
        er_lbl = T("ER", 30, ER_EDGE, weight=BOLD).next_to(er, DOWN, buff=0.16)
        cyt_lbl = T("cytosol", 26, GREY).move_to([-4.8, 0.0, 0])
        tag = scope_tag("schematic")

        world = VGroup(mem, er, ca_dots, pip2, pip2_lbl, mem_lbl, er_lbl, cyt_lbl)
        self.add(world, tag)

        # Cut line + split flash at PIP2 junction
        cut_line = Line([-0.95, pip2.neck.get_center()[1], 0], [0.95, pip2.neck.get_center()[1], 0],
                        color=C_PLC, stroke_width=9)
        q_origin = T("?", 40, C_PLC, weight=BOLD).move_to([0.78, 1.35, 0])
        self.play(Create(cut_line), FadeIn(q_origin), pip2.head.animate.shift(DOWN * 0.16), run_time=1.3)
        self.play(FadeOut(cut_line), run_time=0.4)

        # Two diverging question packets + bold growing arrows
        self.at("send one signal inward")
        inward_p = ValueTracker(0.0)
        inward_start = pip2_lbl.get_bottom() + DOWN * 0.16
        inward_end = np.array([-0.15, -0.82, 0])
        inward_arrow = always_redraw(lambda: Arrow(
            inward_start,
            inward_start + (inward_end - inward_start) * max(inward_p.get_value(), 0.05),
            buff=0, color=C_IP3, stroke_width=7, max_tip_length_to_length_ratio=0.18,
        ))
        inward_pkt = RoundedRectangle(corner_radius=0.14, width=0.68, height=0.52,
                                      stroke_color=C_IP3, stroke_width=3, fill_color=C_IP3, fill_opacity=0.35)
        q_in = T("?", 32, C_IP3, weight=BOLD)
        inward_grp = VGroup(inward_pkt, q_in)
        inward_grp.add_updater(lambda m: m.move_to(inward_start + (inward_end - inward_start) * inward_p.get_value() + LEFT * 0.62))
        self.add(inward_arrow, inward_grp)
        self.play(FadeOut(q_origin, run_time=0.3), inward_p.animate.set_value(1.0), run_time=1.7)
        inward_grp.clear_updaters()

        self.at("while keeping another at the surface")
        surf_p = ValueTracker(0.0)
        surf_pts = [np.array([x, membrane_y_inner(x) - 0.16, 0]) for x in np.linspace(0.60, 4.35, 20)]

        def make_surf_arrow():
            k = max(2, int(round(surf_p.get_value() * (len(surf_pts) - 1))) + 1)
            curve = VMobject().set_points_smoothly(surf_pts[:k]).set_stroke(C_DAG, 7)
            p_prev, p_end = surf_pts[k - 2], surf_pts[k - 1]
            v = p_end - p_prev
            ang = np.arctan2(v[1], v[0])
            tip = Triangle(fill_color=C_DAG, fill_opacity=1.0, stroke_width=0).scale(0.15).rotate(ang - PI / 2).move_to(p_end)
            return VGroup(curve, tip)

        surf_arrow = always_redraw(make_surf_arrow)
        surf_pkt = RoundedRectangle(corner_radius=0.14, width=0.68, height=0.52,
                                    stroke_color=C_DAG, stroke_width=3, fill_color=C_DAG, fill_opacity=0.35)
        q_surf = T("?", 32, C_DAG, weight=BOLD)
        surf_grp = VGroup(surf_pkt, q_surf)
        surf_grp.add_updater(lambda m: m.move_to(
            surf_pts[min(len(surf_pts) - 1, int(surf_p.get_value() * (len(surf_pts) - 1)))] + DOWN * 0.48
        ))
        self.add(surf_arrow, surf_grp)
        self.play(surf_p.animate.set_value(1.0), run_time=2.5)
        surf_grp.clear_updaters()
        surf_grp.move_to(surf_pts[-1] + DOWN * 0.48)

        # Follow a single plasma membrane closely around one cell: zoom around center [0,0,0] so ER stays well inside frame
        self.at("Follow a single plasma membrane")
        trace_t = ValueTracker(-5.8)
        tracer = always_redraw(lambda: Dot([trace_t.get_value(), membrane_y_outer(trace_t.get_value()), 0],
                                           radius=0.15, color=C_PIP2))
        trace_trail = always_redraw(lambda: VMobject().set_points_smoothly(
            [np.array([x, 0.5 * (membrane_y_outer(x) + membrane_y_inner(x)), 0])
             for x in np.linspace(-5.8, max(-5.7, trace_t.get_value()), 28)]
        ).set_stroke(C_PIP2, 14, opacity=0.48))
        self.add(trace_trail, tracer)
        self.play(
            world.animate.scale(1.06, about_point=[0, 0.0, 0]),
            trace_t.animate.set_value(5.8),
            run_time=3.5, rate_func=smooth,
        )
        self.play(
            FadeOut(tracer),
            trace_trail.animate.set_stroke(opacity=0.18),
            world.animate.scale(1.0 / 1.06, about_point=[0, 0.0, 0]),
            run_time=1.0,
        )

        self.at("The answer depends on")
        inward_lbl = T("inward?", 28, C_IP3).next_to(inward_end, RIGHT, buff=0.30)
        surf_lbl = T("at surface?", 28, C_DAG).next_to(surf_grp, DOWN, buff=0.22)
        self.play(FadeIn(inward_lbl), FadeIn(surf_lbl), run_time=1.1)
        self.play(
            inward_grp.animate.shift(DOWN * 0.12),
            surf_grp.animate.shift(RIGHT * 0.16),
            run_time=2.2,
        )
        self.finish()


# ====================================================================
# SCENE 1: TITLE CARD
# ====================================================================
class S01Title(TitleCard):
    LESSON = "PLC, IP3, DAG and Protein Kinase C"
    TITLE = "One Cut, Two Destinations"


# ====================================================================
# SCENE 2: SUBSTRATE (PIP2 ZOOM)
# ====================================================================
def build_s02_world():
    """Zoomed bilayer + two-part PIP2 cartoon."""
    bilayer = build_zoomed_bilayer(y_in=0.55, y_mid=1.55, y_out=2.55)
    pip2 = build_zoomed_pip2(cx=0.0, y_in=0.55, head_color=C_PIP2, tail_color=C_PIP2, gap=0.0)
    out_lbl = T("outside cell", 26, GREY).move_to([-4.6, 3.05, 0])
    cyt_lbl = T("watery cytosol", 28, TEXT).move_to([-4.3, -2.55, 0])
    return bilayer, pip2, out_lbl, cyt_lbl


class S02Substrate(SpokenScene):
    def construct(self):
        macro_mem = build_plasma_membrane()
        macro_er = build_er_sac()
        macro_pip2 = build_macro_pip2(x=0.0, scale=1.15)
        self.add(macro_mem, macro_er, macro_pip2)

        bilayer, pip2, out_lbl, cyt_lbl = build_s02_world()
        pip2_lbl = T("PIP2", 34, C_PIP2, weight=BOLD).next_to(pip2.head_box, DOWN, buff=0.22)
        tag = scope_tag("schematic")
        self.add(tag)

        self.play(
            ReplacementTransform(macro_mem, bilayer),
            ReplacementTransform(macro_pip2, pip2),
            FadeOut(macro_er),
            run_time=1.6,
        )
        self.play(FadeIn(pip2_lbl), FadeIn(out_lbl), FadeIn(cyt_lbl), run_time=1.2)

        self.at("inner leaflet")
        in_band = Polygon(
            [-6.4, 1.53, 0], [6.4, 1.53, 0], [6.4, 0.57, 0], [-6.4, 0.57, 0],
            stroke_color=C_PIP2, stroke_width=3, fill_color=C_PIP2, fill_opacity=0.18,
        )
        in_lbl = T("inner leaflet", 28, C_PIP2).move_to([-4.4, 1.05, 0])
        self.play(FadeIn(in_band), FadeIn(in_lbl), run_time=1.4)
        self.play(FadeOut(in_band), run_time=1.4)

        self.at("Its oily tails")
        tails_lbl = T("oily tails", 30, C_PIP2).move_to([2.4, 1.10, 0])
        tails_brace = Brace(pip2.tails_grp, RIGHT, buff=0.25, color=C_PIP2)
        self.play(GrowFromCenter(tails_brace), FadeIn(tails_lbl), run_time=1.0)
        self.play(Rotate(pip2.tails_grp[0], 0.16, about_point=pip2.tails_grp[0].get_start()),
                  Rotate(pip2.tails_grp[1], -0.16, about_point=pip2.tails_grp[1].get_start()), run_time=0.7)
        self.play(Rotate(pip2.tails_grp[0], -0.16, about_point=pip2.tails_grp[0].get_start()),
                  Rotate(pip2.tails_grp[1], 0.16, about_point=pip2.tails_grp[1].get_start()), run_time=0.7)

        self.at("charged head")
        head_lbl = T("charged head", 30, C_PIP2).move_to([2.6, 0.02, 0])
        head_arrow = Arrow(head_lbl.get_left() + LEFT * 0.12, pip2.head_box.get_right() + RIGHT * 0.12,
                           buff=0, color=C_PIP2, stroke_width=3.5)
        self.play(FadeIn(head_lbl), Create(head_arrow), run_time=1.2)
        self.play(pip2.head_grp.animate.shift(DOWN * 0.20), pip2_lbl.animate.shift(DOWN * 0.20), run_time=1.2)
        self.play(pip2.head_grp.animate.shift(UP * 0.20), pip2_lbl.animate.shift(UP * 0.20), run_time=1.2)

        self.at("address label")
        role_addr = chip("address label", color=C_PIP2, size=26).move_to([3.7, -1.25, 0])
        self.play(FadeIn(role_addr), pip2.head_grp.animate.shift(DOWN * 0.12), pip2_lbl.animate.shift(DOWN * 0.12), run_time=1.1)

        self.at("stored signal")
        role_sig = chip("stored signal", color=C_PIP2, size=26).next_to(role_addr, DOWN, buff=0.25)
        self.play(FadeIn(role_sig), pip2.head_grp.animate.shift(UP * 0.12), pip2_lbl.animate.shift(UP * 0.12), run_time=1.2)

        self.at("Phospholipase C approaches")
        plc = build_plc_clamp("PLC", open_amt=0.18, jaw_dy=0.18).move_to([-5.6, -1.65, 0])
        self.play(FadeIn(plc), run_time=0.4)
        self.play(
            plc.animate.move_to([-1.35, -0.02, 0]),
            FadeOut(role_addr), FadeOut(role_sig),
            run_time=2.4,
        )
        self.finish()


# ====================================================================
# SCENE 3: PREDICT
# ====================================================================
QUESTION_TEXT = "Which product leaves?"
QUESTION_OPTS = ["phosphate-rich head (IP3)", "oily tails (DAG)"]


def build_s03_end_backdrop():
    """Shared picture for end of s03_predict and s04_pause."""
    bilayer = build_zoomed_bilayer(y_in=0.65, y_mid=1.60, y_out=2.55)
    pip2_cut = build_zoomed_pip2(cx=0.0, y_in=0.65, head_color=C_IP3, tail_color=C_DAG, gap=0.26)
    dag_lbl = T("DAG", 32, C_DAG, weight=BOLD).next_to(pip2_cut.tails_grp, RIGHT, buff=0.35)
    ip3_lbl = T("IP3", 32, C_IP3, weight=BOLD).next_to(pip2_cut.head_box, RIGHT, buff=0.35)
    patch_line = Line([-1.2, 0.65, 0], [1.2, 0.65, 0], color=C_PIP2, stroke_width=6)
    patch_lbl = T("same membrane patch", 26, TEXT).move_to([-3.5, 0.20, 0])
    return VGroup(bilayer, pip2_cut, dag_lbl, ip3_lbl, patch_line, patch_lbl)


class S03Predict(SpokenScene):
    def construct(self):
        bilayer = build_zoomed_bilayer(y_in=0.65, y_mid=1.60, y_out=2.55)
        pip2 = build_zoomed_pip2(cx=0.0, y_in=0.65, head_color=C_PIP2, tail_color=C_PIP2, gap=0.0)
        plc = build_plc_clamp("PLC", open_amt=0.18, jaw_dy=0.18).move_to([-1.35, 0.08, 0])
        out_lbl = T("outside cell", 26, GREY).move_to([-4.6, 3.05, 0])
        self.add(bilayer, pip2, plc, out_lbl)

        self.at("cuts between the head")
        self.play(
            plc.jaw_top.animate.shift(DOWN * 0.12),
            plc.jaw_bot.animate.shift(UP * 0.12),
            run_time=1.1,
        )
        cut_flash = Line([-0.95, 0.48, 0], [0.95, 0.48, 0], color=C_PLC, stroke_width=10)
        self.play(Create(cut_flash), run_time=0.7)

        pip2_cut = build_zoomed_pip2(cx=0.0, y_in=0.65, head_color=C_IP3, tail_color=C_DAG, gap=0.26)
        dag_lbl = T("DAG", 32, C_DAG, weight=BOLD).next_to(pip2_cut.tails_grp, RIGHT, buff=0.35)
        ip3_lbl = T("IP3", 32, C_IP3, weight=BOLD).next_to(pip2_cut.head_box, RIGHT, buff=0.35)
        self.play(
            FadeOut(cut_flash),
            ReplacementTransform(pip2, pip2_cut),
            FadeIn(dag_lbl),
            FadeIn(ip3_lbl),
            run_time=2.2,
        )

        self.at("Both products begin")
        patch_line = Line([-1.2, 0.65, 0], [1.2, 0.65, 0], color=C_PIP2, stroke_width=6)
        patch_lbl = T("same membrane patch", 26, TEXT).move_to([-3.5, 0.20, 0])
        # Fade PLC out completely BEFORE fading in patch_lbl so letters never overlap during motion
        self.play(FadeOut(plc, shift=LEFT * 1.4), FadeOut(out_lbl), run_time=1.1)
        self.play(Create(patch_line), FadeIn(patch_lbl), run_time=1.8)

        self.at("Which product can leave")
        q = question_card(QUESTION_TEXT, QUESTION_OPTS, y=-3.05)
        self.play(FadeIn(q.question), run_time=1.8)

        self.at("Choose the")
        self.play(FadeIn(q.chips), run_time=1.0)

        hl_ip3 = SurroundingRectangle(pip2_cut.head_box, color=C_IP3, buff=0.10, stroke_width=5)
        hl_dag = SurroundingRectangle(pip2_cut.tails_grp, color=C_DAG, buff=0.10, stroke_width=5)
        self.play(Create(hl_ip3), pip2_cut.head_grp.animate.shift(DOWN * 0.16), ip3_lbl.animate.shift(DOWN * 0.16), run_time=0.8)
        self.play(pip2_cut.head_grp.animate.shift(UP * 0.16), ip3_lbl.animate.shift(UP * 0.16), run_time=0.6)
        self.at("or the oily pair")
        self.play(FadeOut(hl_ip3, run_time=0.25), Create(hl_dag, run_time=0.5),
                  pip2_cut.tails_grp.animate.shift(RIGHT * 0.16), dag_lbl.animate.shift(RIGHT * 0.16))
        self.play(FadeOut(hl_dag), pip2_cut.tails_grp.animate.shift(LEFT * 0.16), dag_lbl.animate.shift(LEFT * 0.16), run_time=0.7)
        self.finish()


# ====================================================================
# SCENE 4: PREDICT PAUSE
# ====================================================================
class S04Pause(PredictPause):
    QUESTION = QUESTION_TEXT
    OPTIONS = QUESTION_OPTS
    SECONDS = 4.5

    def backdrop(self):
        return build_s03_end_backdrop()


# ====================================================================
# SCENE 5: TWO DESTINATIONS
# ====================================================================
class S05Destinations(SpokenScene):
    def construct(self):
        backdrop = build_s03_end_backdrop()
        q = question_card(QUESTION_TEXT, QUESTION_OPTS, y=-3.05)
        self.add(backdrop, q)

        mem = build_plasma_membrane()
        er = build_er_sac(center_y=-2.05, rx=4.1, ry=0.88)
        ca_dots = build_er_ca_dots(n=24, seed=7, center_y=-2.05, rx=3.5, ry=0.60)
        er_lbl = T("ER", 28, ER_EDGE, weight=BOLD).next_to(er, DOWN, buff=0.18)
        tag = scope_tag("schematic")

        ip3 = build_ip3_token("IP3", scale=0.95).move_to([0.0, 0.85, 0])
        dag = build_dag_token(x=0.0, scale=0.90)

        bilayer_b, pip2_cut_b, dag_lbl_b, ip3_lbl_b, patch_line_b, patch_lbl_b = backdrop
        self.play(
            FadeOut(q), FadeOut(dag_lbl_b), FadeOut(ip3_lbl_b), FadeOut(patch_line_b), FadeOut(patch_lbl_b),
            ReplacementTransform(bilayer_b, mem),
            ReplacementTransform(pip2_cut_b.head_grp, ip3),
            ReplacementTransform(pip2_cut_b.tails_grp, dag),
            FadeIn(er), FadeIn(ca_dots), FadeIn(er_lbl), FadeIn(tag),
            run_time=1.3,
        )

        self.at("three phosphates")
        p_badges = VGroup(*[make_p_badge(size=22, radius=0.21) for _ in range(3)])
        p_badges.arrange(RIGHT, buff=0.08).next_to(ip3, DOWN, buff=0.14)
        self.play(FadeIn(p_badges), run_time=0.9)

        self.at("dissolves in cytosol")
        t_val = ValueTracker(0.0)

        def ip3_pos(u):
            x = -1.75 * np.sin(u * PI * 0.58)
            y = 0.55 - 1.25 * (u ** 0.9)
            return np.array([x, y, 0])

        ip3_grp = VGroup(ip3, p_badges)
        ip3_grp.add_updater(lambda m: m.move_to(ip3_pos(t_val.get_value())))

        # Anchor trail from initial cut site [0, 1.15, 0] cleanly to ip3_grp top edge + UP*0.16 (never crosses IP3!)
        start_anchor = np.array([0.0, 1.15, 0])

        def make_trail():
            end_pt = ip3_grp.get_top() + UP * 0.16
            if np.linalg.norm(end_pt - start_anchor) < 0.25:
                return VGroup()
            return CurvedArrow(start_anchor, end_pt, angle=0.35, color=C_IP3, stroke_width=5, tip_length=0.18)

        ip3_trail = always_redraw(make_trail)
        sol_lbl = T("water-soluble", 28, C_IP3)
        # Put water-soluble cleanly on the LEFT of ip3_grp; moving branch goes ABOVE it
        sol_lbl.add_updater(lambda m: m.next_to(ip3_grp, LEFT, buff=0.28))

        self.add(ip3_trail, sol_lbl)
        self.play(t_val.animate.set_value(1.0), run_time=3.3, rate_func=smooth)
        ip3_grp.clear_updaters()
        sol_lbl.clear_updaters()
        sol_lbl.next_to(ip3_grp, LEFT, buff=0.28)

        self.at("DAG keeps two oily tails")
        dag_x = ValueTracker(0.0)
        dag.add_updater(lambda m: m.become(build_dag_token(x=dag_x.get_value(), scale=0.90)))
        mem_track = DashedLine([0.1, membrane_y_inner(0.1), 0], [2.9, membrane_y_inner(2.9), 0],
                               color=C_DAG, stroke_width=4)
        ret_lbl = T("membrane-retained", 28, C_DAG).move_to([3.55, 0.85, 0])
        self.play(Create(mem_track), FadeIn(ret_lbl), run_time=0.9)
        self.play(dag_x.animate.set_value(2.9), run_time=2.5, rate_func=smooth)
        self.play(dag_x.animate.set_value(2.1), run_time=1.3, rate_func=smooth)
        dag.clear_updaters()

        self.at("moving branch")
        mov_lbl = chip("moving branch", color=C_IP3, size=26).move_to([-3.9, -0.05, 0])
        self.play(FadeIn(mov_lbl), run_time=0.9)

        self.at("local membrane branch")
        loc_lbl = chip("local membrane branch", color=C_DAG, size=26).move_to([3.55, 0.12, 0])
        self.play(FadeIn(loc_lbl), run_time=1.1)

        self.at("two second messengers")
        summary = chip("two second messengers", color=C_PIP2, size=28).move_to([3.55, -0.82, 0])
        arr_l = Arrow(summary.get_left() + LEFT * 0.12, ip3_grp.get_right() + RIGHT * 0.20,
                      buff=0, color=C_IP3, stroke_width=3.5)
        arr_u = Arrow(summary.get_top() + UP * 0.10, loc_lbl.get_bottom() + DOWN * 0.10,
                      buff=0, color=C_DAG, stroke_width=3.5)
        self.play(FadeIn(summary), Create(arr_l), Create(arr_u), run_time=1.6)
        self.play(ip3_grp.animate.shift(DOWN * 0.08), run_time=1.2)
        self.finish()


# ====================================================================
# SCENE 6: TWO RECEPTOR ROUTES (GPCR->Gq->PLC-beta vs RTK->SH2->PLC-gamma)
# ====================================================================
class S06TwoRoutes(SpokenScene):
    def construct(self):
        mem = build_plasma_membrane()
        er = build_er_sac(center_y=-2.65, rx=4.1, ry=0.65)
        ca_dots = build_er_ca_dots(n=20, seed=7, center_y=-2.65, rx=3.4, ry=0.42)
        er_lbl = T("ER", 26, ER_EDGE, weight=BOLD).next_to(er, RIGHT, buff=0.25)
        tag = scope_tag("schematic")

        pip2_l = build_macro_pip2(x=-1.20, scale=1.05)
        pip2_r = build_macro_pip2(x=1.20, scale=1.05)
        pip2_l_lbl = T("PIP2", 26, C_PIP2, weight=BOLD).next_to(pip2_l.head, DOWN, buff=0.14)
        pip2_r_lbl = T("PIP2", 26, C_PIP2, weight=BOLD).next_to(pip2_r.head, DOWN, buff=0.14)
        div = DashedLine([0, 2.8, 0], [0, -1.7, 0], color=GREY, stroke_width=2).set_opacity(0.45)

        self.play(
            FadeIn(mem), FadeIn(er), FadeIn(ca_dots), FadeIn(er_lbl), FadeIn(tag),
            FadeIn(pip2_l), FadeIn(pip2_r), FadeIn(pip2_l_lbl), FadeIn(pip2_r_lbl), FadeIn(div),
            run_time=1.6,
        )
        # Highlight both PIP2 targets cleanly around both lipid & label
        ring_l = SurroundingRectangle(VGroup(pip2_l, pip2_l_lbl), color=C_PIP2, buff=0.10, stroke_width=3.5)
        ring_r = SurroundingRectangle(VGroup(pip2_r, pip2_r_lbl), color=C_PIP2, buff=0.10, stroke_width=3.5)
        self.play(Create(ring_l), Create(ring_r), run_time=1.2)
        self.play(FadeOut(ring_l), FadeOut(ring_r), run_time=0.8)

        # ---- LEFT: GPCR -> Gq -> PLC-beta ----
        self.at("G protein coupled receptor")
        gpcr_x = -5.1
        gpcr_y = 0.5 * (membrane_y_inner(gpcr_x) + membrane_y_outer(gpcr_x))
        helices = VGroup(*[
            RoundedRectangle(corner_radius=0.05, width=0.13, height=0.90,
                             stroke_color=C_GQ, stroke_width=2, fill_color=C_GQ, fill_opacity=0.45)
            for _ in range(7)
        ]).arrange(RIGHT, buff=0.04).move_to([gpcr_x, gpcr_y, 0])
        gpcr_lbl = T("GPCR", 26, C_GQ, weight=BOLD).next_to(helices, UP, buff=0.16)
        self.play(FadeIn(helices), FadeIn(gpcr_lbl), run_time=1.2)

        self.at("activates GQ")
        gq_circle = VGroup(
            Circle(radius=0.43, stroke_color=C_GQ, stroke_width=3, fill_color=C_GQ, fill_opacity=0.28),
            T("Gq", 26, C_GQ, weight=BOLD),
        )
        gq_circle[1].move_to(gq_circle[0])
        gq_circle.move_to([-4.9, 0.72, 0])
        self.play(FadeIn(gq_circle), gq_circle.animate.move_to([-4.25, 0.72, 0]), run_time=1.8)

        self.at("PLC beta")
        plc_b = build_plc_clamp("PLC-beta", open_amt=0.16, width=1.78, jaw_dy=0.15)
        plc_b.move_to([-3.3, -1.05, 0])
        self.play(FadeIn(plc_b), run_time=0.6)
        self.play(
            gq_circle.animate.move_to([-4.75, 0.75, 0]),
            plc_b.animate.move_to([-2.92, 0.85, 0]),
            run_time=1.8,
        )

        # ---- RIGHT: RTK dimer -> pY -> SH2 docks PLC-gamma (with closed brake) -> P jump -> brake open -> cut ----
        self.at("receptor tyrosine kinase")
        rtk_l = RoundedRectangle(corner_radius=0.08, width=0.26, height=1.35,
                                 stroke_color=C_RTK, stroke_width=2.5, fill_color=C_RTK, fill_opacity=0.35).move_to([4.25, 1.48, 0])
        rtk_r = RoundedRectangle(corner_radius=0.08, width=0.26, height=1.35,
                                 stroke_color=C_RTK, stroke_width=2.5, fill_color=C_RTK, fill_opacity=0.35).move_to([5.45, 1.48, 0])
        rtk_lbl = T("RTK", 26, C_RTK, weight=BOLD).move_to([4.85, 2.75, 0])
        self.play(FadeIn(rtk_l), FadeIn(rtk_r), FadeIn(rtk_lbl), run_time=0.8)
        self.play(rtk_l.animate.shift(RIGHT * 0.30), rtk_r.animate.shift(LEFT * 0.30), run_time=1.2)

        self.at("phosphorylated tyrosines")
        p_y1 = make_p_badge(size=22, radius=0.21).move_to([4.55, 0.45, 0])
        p_y2 = make_p_badge(size=22, radius=0.21).move_to([5.15, 0.45, 0])
        self.play(FadeIn(p_y1), FadeIn(p_y2), run_time=1.6)

        self.at("SH2 domains dock")
        plc_g_body = RoundedRectangle(corner_radius=0.16, width=2.15, height=0.68,
                                      stroke_color=C_PLC, stroke_width=3, fill_color=C_PLC, fill_opacity=0.15)
        plc_g_lbl = T("PLC-gamma", 24, C_PLC, weight=BOLD).move_to(plc_g_body)
        # Put SH2 label cleanly BETWEEN the two SH2 grips so it never extends past left or right edge
        sh2_1 = RoundedRectangle(corner_radius=0.06, width=0.40, height=0.24,
                                 stroke_color=C_RTK, stroke_width=2, fill_color=BG, fill_opacity=0.95)
        sh2_1.move_to(plc_g_body.get_top() + LEFT * 0.65 + UP * 0.18)
        sh2_2 = sh2_1.copy().move_to(plc_g_body.get_top() + RIGHT * 0.65 + UP * 0.18)
        sh2_tag = T("SH2", 22, C_RTK, weight=BOLD).move_to(plc_g_body.get_top() + UP * 0.18)
        brake = RoundedRectangle(corner_radius=0.06, width=0.24, height=0.58,
                                 stroke_color=GREY, stroke_width=2.5, fill_color=GREY, fill_opacity=0.75)
        brake.next_to(plc_g_body, LEFT, buff=0.10)
        brake_lbl = T("brake", 22, GREY, weight=BOLD).next_to(brake, LEFT, buff=0.10)
        plc_g = VGroup(plc_g_body, plc_g_lbl, sh2_1, sh2_2, sh2_tag, brake, brake_lbl).move_to([4.55, -1.55, 0])

        self.play(FadeIn(plc_g), run_time=0.8)
        self.play(plc_g.animate.shift(UP * 1.10), run_time=2.5)

        self.at("Docking places")
        dock_note = T("docked · brake closed", 24, GREY).move_to([4.45, -1.30, 0])
        # Route proximity arrow strictly to the LEFT of p_y1 so it never touches P
        prox_line = CurvedArrow(rtk_l.get_left() + DOWN * 0.25 + LEFT * 0.08,
                                plc_g_body.get_top() + LEFT * 0.88 + UP * 0.06,
                                angle=0.35, color=C_RTK, stroke_width=4, tip_length=0.16)
        self.play(FadeIn(dock_note), Create(prox_line), run_time=1.5)
        self.play(Indicate(p_y1, scale_factor=1.25), Indicate(p_y2, scale_factor=1.25),
                  Indicate(sh2_1, scale_factor=1.2), Indicate(sh2_2, scale_factor=1.2), run_time=1.6)
        # Active kinase engagement pulse while brake stays closed (prevents 9.5s freeze)
        kinase_glow = SurroundingRectangle(rtk_l, color=C_RTK, buff=0.08, stroke_width=4)
        self.play(Create(kinase_glow), run_time=1.4)
        self.play(FadeOut(kinase_glow), Indicate(plc_g_body, scale_factor=1.06, color=C_PLC), run_time=1.3)

        self.at("The kinase phosphorylates it")
        p_jump = make_p_badge(size=22, radius=0.21).move_to([4.00, 0.70, 0])
        self.play(FadeOut(dock_note, run_time=0.4), FadeOut(prox_line, run_time=0.4), FadeIn(p_jump, run_time=0.3))
        self.play(p_jump.animate.move_to(plc_g_body.get_bottom() + DOWN * 0.28), run_time=1.3)

        self.at("releases its internal")
        self.play(
            brake.animate.shift(DOWN * 0.55 + LEFT * 0.10).rotate(-PI / 3),
            FadeOut(brake_lbl, run_time=0.4),
            run_time=1.0,
        )
        plc_g_act = VGroup(plc_g_body, plc_g_lbl, sh2_1, sh2_2, sh2_tag, p_jump)
        self.play(
            FadeOut(brake, run_time=0.3),
            plc_g_act.animate.move_to([2.95, 0.72, 0]),
            run_time=1.2,
        )

        self.at("Both enzymes then make")
        flash_l = Line([-1.60, pip2_l.neck.get_center()[1], 0], [-0.80, pip2_l.neck.get_center()[1], 0], color=C_PLC, stroke_width=7)
        flash_r = Line([0.80, pip2_r.neck.get_center()[1], 0], [1.60, pip2_r.neck.get_center()[1], 0], color=C_PLC, stroke_width=7)
        self.play(Create(flash_l), Create(flash_r), run_time=0.7)

        self.at("producing IP3 and DAG")
        ip3_l = build_ip3_token("IP3", scale=0.88).move_to([-1.20, 1.00, 0])
        ip3_r = build_ip3_token("IP3", scale=0.88).move_to([1.20, 1.00, 0])
        dag_l = build_dag_token(x=-1.20, scale=0.85)
        dag_r = build_dag_token(x=1.20, scale=0.85)
        self.play(
            FadeOut(flash_l), FadeOut(flash_r),
            FadeOut(pip2_l_lbl), FadeOut(pip2_r_lbl),
            ReplacementTransform(pip2_l, dag_l),
            ReplacementTransform(pip2_r, dag_r),
            FadeIn(ip3_l), FadeIn(ip3_r),
            run_time=0.7,
        )
        self.play(
            ip3_l.animate.shift(DOWN * 2.15),
            ip3_r.animate.shift(DOWN * 2.15),
            run_time=2.2,
        )
        self.finish()


# ====================================================================
# SCENE 7: IP3 OPENS THE ER CALCIUM CHANNEL
# ====================================================================
class S07ErChannel(SpokenScene):
    def construct(self):
        top_mem = build_plasma_membrane(x_min=-3.8, x_max=3.8, n=28).shift(UP * 0.90)
        top_dag = build_dag_token(x=0.0, y_fn=lambda x: membrane_y_inner(x) + 0.90, scale=0.88)
        top_lbl = T("DAG stays at membrane", 24, C_DAG).next_to(top_dag, DOWN, buff=0.18)
        tag = scope_tag("schematic")

        er_y = -0.55
        er_lumen = Polygon(
            [-6.6, er_y, 0], [6.6, er_y, 0], [6.6, -3.55, 0], [-6.6, -3.55, 0],
            stroke_width=0, fill_color=ER_FILL, fill_opacity=0.85,
        )
        wall_l = Line([-6.6, er_y, 0], [-0.95, er_y, 0], color=ER_EDGE, stroke_width=5)
        wall_r = Line([0.95, er_y, 0], [6.6, er_y, 0], color=ER_EDGE, stroke_width=5)
        ch_l = RoundedRectangle(corner_radius=0.08, width=0.45, height=1.15,
                                stroke_color=ER_EDGE, stroke_width=3, fill_color=ER_FILL, fill_opacity=0.95).move_to([-0.85, er_y, 0])
        ch_r = RoundedRectangle(corner_radius=0.08, width=0.45, height=1.15,
                                stroke_color=ER_EDGE, stroke_width=3, fill_color=ER_FILL, fill_opacity=0.95).move_to([0.85, er_y, 0])
        gate_l = Rectangle(width=0.62, height=0.22, stroke_color=C_IP3, stroke_width=2.5, fill_color=ER_EDGE, fill_opacity=0.85)
        gate_l.move_to([-0.32, er_y, 0])
        gate_r = Rectangle(width=0.62, height=0.22, stroke_color=C_IP3, stroke_width=2.5, fill_color=ER_EDGE, fill_opacity=0.85)
        gate_r.move_to([0.32, er_y, 0])

        # Generous IP3 socket (1.18 x 0.70) so 0.88 x 0.49 IP3 sits cleanly inside with zero straddle/near
        socket = Polygon(
            [-2.16, er_y + 0.58, 0], [-2.16, er_y + 1.28, 0], [-0.98, er_y + 1.28, 0], [-0.98, er_y + 0.58, 0],
            stroke_color=C_IP3, stroke_width=3, fill_color=BG, fill_opacity=0.85,
        )
        socket_lbl = T("IP3 socket", 24, C_IP3).next_to(socket, LEFT, buff=0.24)
        rec_lbl = T("IP3 receptor", 30, TEXT, weight=BOLD).move_to([3.65, er_y + 1.05, 0])
        # Keep ER label at y=-2.15 relative to stage so even with initial DOWN*0.85 shift it stays at -3.00 inside frame
        er_lbl = T("ER lumen (calcium store)", 26, ER_EDGE, weight=BOLD).move_to([-3.8, -2.15, 0])
        er_lbl.set_z_index(20)

        rng = np.random.default_rng(7)
        ca_inside = []
        for i in range(34):
            x = rng.uniform(-5.6, 5.6)
            y = rng.uniform(-2.70, -0.95)
            if x < -1.0 and -2.45 < y < -1.85:
                y = rng.uniform(-1.70, -0.95)
            d = Dot([x, y, 0], radius=0.085, color=C_CA)
            d.flows = (i < 24)
            ca_inside.append(d)
        ca_sparse = VGroup(*[
            Dot([rng.uniform(-4.5, -2.5), rng.uniform(1.0, 1.8), 0], radius=0.075, color=C_CA),
            Dot([rng.uniform(2.2, 4.5), rng.uniform(1.0, 1.8), 0], radius=0.075, color=C_CA),
        ])
        ca_grp = VGroup(*ca_inside)

        stage = VGroup(er_lumen, wall_l, wall_r, ch_l, ch_r, gate_l, gate_r, socket, socket_lbl,
                       rec_lbl, er_lbl, ca_grp, ca_sparse, top_mem, top_dag, top_lbl)
        stage.shift(DOWN * 0.85)
        self.add(stage, tag)

        # Start IP3 cleanly in open cytosol BELOW top_mem & top_lbl (top_lbl bottom is at ~2.0-0.85=1.15)
        ip3 = build_ip3_token("IP3", scale=0.88).move_to([-3.0, 0.55, 0])
        self.at("follow IP3")
        self.play(FadeIn(ip3), run_time=0.8)

        self.at("crosses the cytosol")
        self.play(
            stage.animate.shift(UP * 0.85),
            ip3.animate.move_to([-1.57, 1.05, 0]),
            run_time=2.2, rate_func=smooth,
        )

        self.at("binds an IP3 receptor")
        # Drop straight down from [-1.57, 1.05] into socket center [-1.57, 0.38] without touching socket_lbl
        self.play(ip3.animate.move_to(socket.get_center()), run_time=1.5, rate_func=smooth)
        self.play(socket.animate.set_stroke(width=5), run_time=0.8)

        # ER calcium ions visibly gather toward the receptor pore
        ca_p_init = [d.get_center().copy() for d in ca_inside]
        ca_p_ready = [
            np.array([p[0] * 0.72, min(-0.88, p[1] + 0.45), 0])
            for p in ca_p_init
        ]
        prep_t = ValueTracker(0.0)
        ca_grp.add_updater(lambda m: [
            d.move_to(ca_p_init[i] + (ca_p_ready[i] - ca_p_init[i]) * prep_t.get_value())
            for i, d in enumerate(ca_inside)
        ])
        self.play(prep_t.animate.set_value(1.0), run_time=3.5, rate_func=smooth)
        ca_grp.clear_updaters()

        self.at("calcium channel")
        ch_lbl = T("calcium channel", 28, C_CA, weight=BOLD).move_to([3.65, er_y + 0.42, 0])
        self.play(
            FadeIn(ch_lbl),
            ch_l.animate.set_stroke(C_CA, 5),
            ch_r.animate.set_stroke(C_CA, 5),
            run_time=1.6,
        )

        self.at("IP3 does not carry calcium")
        no_carry = T("IP3 stays outside; opens route", 26, C_IP3).move_to([3.55, 1.15, 0])
        sock_ring = SurroundingRectangle(socket, color=C_IP3, buff=0.08, stroke_width=4)
        # Keep ER ions pressing smoothly upward near the pore while explaining IP3 doesn't carry Ca2+
        ca_p_press = [np.array([p[0] * 0.85, min(-0.82, p[1] + 0.25), 0]) for p in ca_p_ready]
        press_t = ValueTracker(0.0)
        ca_grp.add_updater(lambda m: [
            d.move_to(ca_p_ready[i] + (ca_p_press[i] - ca_p_ready[i]) * press_t.get_value())
            for i, d in enumerate(ca_inside)
        ])
        self.play(FadeIn(no_carry), Create(sock_ring), press_t.animate.set_value(1.0), run_time=2.0)
        ca_grp.clear_updaters()

        self.at("It opens")
        route_hint = Arrow([0.0, -2.25, 0], [0.0, er_y - 0.15, 0], buff=0, color=C_CA, stroke_width=7)
        self.play(FadeOut(no_carry), FadeOut(sock_ring), GrowArrow(route_hint), run_time=1.8)

        self.at("channel opens")
        self.play(
            FadeOut(route_hint, run_time=0.3),
            Rotate(gate_l, angle=-PI * 0.42, about_point=gate_l.get_left()),
            Rotate(gate_r, angle=PI * 0.42, about_point=gate_r.get_right()),
            run_time=1.1,
        )

        self.at("green calcium dots flow")
        flow_t = ValueTracker(0.0)
        start_pos = [d.get_center().copy() for d in ca_inside]
        targets = []
        for idx, d in enumerate(ca_inside):
            if d.flows:
                tx = rng.uniform(-1.90, 1.90)
                ty = rng.uniform(0.15, 1.65)
                targets.append(np.array([tx, ty, 0]))
            else:
                targets.append(start_pos[idx] + np.array([rng.uniform(-0.35, 0.35), rng.uniform(0.15, 0.45), 0]))

        def update_ca(mob):
            u = flow_t.get_value()
            for idx, d in enumerate(ca_inside):
                p0 = start_pos[idx]
                p1 = targets[idx]
                if not d.flows:
                    d.move_to(p0 + (p1 - p0) * u)
                else:
                    delay = (idx % 6) * 0.06
                    s = np.clip((u - delay) / (1.0 - delay), 0.0, 1.0)
                    pore = np.array([((idx % 5) - 2) * 0.09, er_y, 0])
                    if s < 0.45:
                        k = s / 0.45
                        d.move_to(p0 + (pore - p0) * k)
                    else:
                        k = (s - 0.45) / 0.55
                        d.move_to(pore + (p1 - pore) * k)

        ca_grp.add_updater(update_ca)
        self.play(flow_t.animate.set_value(1.0), run_time=3.5, rate_func=linear)
        ca_grp.clear_updaters()
        self.finish()


# ====================================================================
# SCENE 8: PERMEABILIZED CELL EXPERIMENT
# ====================================================================
class S08Experiment(SpokenScene):
    def construct(self):
        cell_full = RoundedRectangle(corner_radius=1.2, width=10.8, height=4.8,
                                     stroke_color=MEM_EDGE, stroke_width=4, fill_color=BG, fill_opacity=0.2)
        cell_full.move_to([0, -0.35, 0])
        cell_lbl = T("intact cell", 30, TEXT).move_to([-2.1, 2.60, 0])

        store_sac = RoundedRectangle(corner_radius=0.55, width=3.8, height=2.2,
                                     stroke_color=ER_EDGE, stroke_width=3.5, fill_color=ER_FILL, fill_opacity=0.88)
        store_sac.move_to([-2.4, -0.55, 0])
        store_lbl = T("internal store", 28, ER_EDGE, weight=BOLD).next_to(store_sac, DOWN, buff=0.20)

        rng = np.random.default_rng(7)
        store_ca = [
            Dot([rng.uniform(-3.9, -0.9), rng.uniform(-1.35, 0.25), 0], radius=0.075, color=C_CA)
            for _ in range(22)
        ]
        store_ca_grp = VGroup(*store_ca)

        mito = RoundedRectangle(corner_radius=0.75, width=3.3, height=1.8,
                                stroke_color=GREY, stroke_width=3.5, fill_color="#232832", fill_opacity=0.90)
        mito.move_to([2.4, -0.55, 0])
        mito_inner = VMobject().set_points_smoothly([
            np.array([1.2, -0.55, 0]), np.array([1.6, -0.15, 0]), np.array([2.0, -0.85, 0]),
            np.array([2.4, -0.15, 0]), np.array([2.8, -0.85, 0]), np.array([3.2, -0.25, 0]), np.array([3.6, -0.55, 0]),
        ]).set_stroke(GREY, 2.5, opacity=0.6)
        mito_ca = VGroup(*[
            Dot([rng.uniform(1.15, 3.65), rng.uniform(-1.15, 0.05), 0], radius=0.07, color=C_CA)
            for _ in range(10)
        ])
        mito_lbl = T("mitochondrion", 28, GREY, weight=BOLD).next_to(mito, DOWN, buff=0.20)
        tag = scope_tag("schematic")

        self.play(
            FadeIn(cell_full), FadeIn(cell_lbl), FadeIn(store_sac), FadeIn(store_lbl),
            FadeIn(store_ca_grp), FadeIn(mito), FadeIn(mito_inner), FadeIn(mito_ca), FadeIn(mito_lbl), FadeIn(tag),
            run_time=1.3,
        )
        test_q = chip("test: IP3 without hormone?", color=C_IP3, size=26).move_to([2.6, 2.60, 0])
        self.play(FadeIn(test_q), run_time=1.0)
        self.play(cell_full.animate.set_stroke(C_IP3, 5), run_time=1.5)
        self.play(cell_full.animate.set_stroke(MEM_EDGE, 4), run_time=1.3)

        self.at("cell surface leaky")
        segs = VGroup(
            Line([-5.4, 2.05, 0], [-2.4, 2.05, 0], color=MEM_EDGE, stroke_width=4),
            Line([-1.1, 2.05, 0], [1.4, 2.05, 0], color=MEM_EDGE, stroke_width=4),
            Line([2.3, 2.05, 0], [5.4, 2.05, 0], color=MEM_EDGE, stroke_width=4),
            Line([5.4, 2.05, 0], [5.4, -2.75, 0], color=MEM_EDGE, stroke_width=4),
            Line([5.4, -2.75, 0], [1.2, -2.75, 0], color=MEM_EDGE, stroke_width=4),
            Line([0.2, -2.75, 0], [-5.4, -2.75, 0], color=MEM_EDGE, stroke_width=4),
            Line([-5.4, -2.75, 0], [-5.4, 0.2, 0], color=MEM_EDGE, stroke_width=4),
            Line([-5.4, 1.0, 0], [-5.4, 2.05, 0], color=MEM_EDGE, stroke_width=4),
        )
        perm_lbl = T("permeabilized cell", 30, TEXT, weight=BOLD).move_to([-2.1, 2.60, 0])
        self.play(
            ReplacementTransform(cell_full, segs),
            swap(cell_lbl, perm_lbl, run_time=0.8),
            run_time=1.3,
        )

        self.at("internal stores stayed sealed")
        seal_s = SurroundingRectangle(store_sac, color=ER_EDGE, buff=0.06, stroke_width=5)
        seal_m = SurroundingRectangle(mito, color=GREY, buff=0.06, stroke_width=5)
        self.play(Create(seal_s), Create(seal_m), run_time=1.1)
        self.play(FadeOut(seal_s), FadeOut(seal_m), run_time=0.8)

        self.at("No outside hormone")
        no_horm = chip("no outside hormone", color=GREY, size=26).move_to([2.6, 2.60, 0])
        self.play(swap(test_q, no_horm, run_time=0.9), run_time=1.2)
        self.play(no_horm.animate.set_stroke(width=3.5), run_time=1.0)

        self.at("Added IP3")
        ip3 = build_ip3_token("IP3", scale=0.92).move_to([-1.75, 3.15, 0])
        self.play(FadeIn(ip3), run_time=0.5)
        self.play(ip3.animate.move_to([-1.75, 0.96, 0]), run_time=1.2)

        self.at("released calcium")
        rel_t = ValueTracker(0.0)
        ca_p0 = [d.get_center().copy() for d in store_ca]
        ca_p1 = []
        ca_p2 = []
        for idx, p in enumerate(ca_p0):
            if idx < 16:
                tx = rng.uniform(-4.5, -2.5) if idx % 2 == 0 else rng.uniform(-0.9, 0.7)
                ty = rng.uniform(0.75, 1.55)
                p_mid = np.array([tx, ty, 0])
                ca_p1.append(p_mid)
                ca_p2.append(np.array([np.clip(tx + rng.uniform(-0.55, 0.55), -4.8, 0.7),
                                       np.clip(ty + rng.uniform(0.15, 0.40), 0.75, 1.85), 0]))
            else:
                ca_p1.append(p)
                ca_p2.append(p)
        store_ca_grp.add_updater(lambda m: [
            d.move_to(ca_p0[i] + (ca_p1[i] - ca_p0[i]) * rel_t.get_value())
            for i, d in enumerate(store_ca)
        ])
        nonmito_lbl = T("unchanged", 24, GREY).move_to([2.4, 0.72, 0])
        self.play(rel_t.animate.set_value(1.0), FadeIn(nonmito_lbl), run_time=2.8, rate_func=smooth)
        store_ca_grp.clear_updaters()

        self.at("separation of cause")
        res_lbl = chip("IP3 sufficient for release", color=C_CA, size=26).move_to([0.0, -3.22, 0])
        diff_t = ValueTracker(0.0)
        store_ca_grp.add_updater(lambda m: [
            d.move_to(ca_p1[i] + (ca_p2[i] - ca_p1[i]) * diff_t.get_value())
            for i, d in enumerate(store_ca)
        ])
        self.play(FadeIn(res_lbl), diff_t.animate.set_value(1.0), run_time=4.8, rate_func=smooth)
        store_ca_grp.clear_updaters()

        self.at("identified the store as endoplasmic reticulum")
        er_final_lbl = T("ER (internal store)", 28, ER_EDGE, weight=BOLD).move_to(store_lbl)
        self.play(swap(store_lbl, er_final_lbl, run_time=1.0), run_time=1.8)
        self.finish()


# ====================================================================
# SCENE 9: RULE & LEGEND
# ====================================================================
def build_color_legend():
    """Compact 8-colour map legend for both films, docked cleanly on the right."""
    items = [
        ("PIP2", C_PIP2),
        ("IP3", C_IP3),
        ("DAG", C_DAG),
        ("Ca2+", C_CA),
        ("PLC", C_PLC),
        ("PKC", C_PKC),
        ("Gq", C_GQ),
        ("RTK", C_RTK),
    ]
    rows = VGroup()
    for name, col in items:
        sw = Square(side_length=0.22, stroke_width=0, fill_color=col, fill_opacity=1.0)
        tx = T(name, size=22, color=col, weight=BOLD)
        rows.add(VGroup(sw, tx).arrange(RIGHT, buff=0.14))
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    hdr = T("colour map", 22, GREY).next_to(rows, UP, buff=0.16, aligned_edge=LEFT)
    panel = RoundedRectangle(corner_radius=0.14, width=max(rows.width, hdr.width) + 0.44,
                             height=rows.height + hdr.height + 0.52,
                             stroke_color=GREY, stroke_width=2, fill_color=BG, fill_opacity=0.92)
    grp = VGroup(hdr, rows).move_to(panel)
    return VGroup(panel, grp).move_to([5.25, 0.35, 0])


class S09Rule(SpokenScene):
    def construct(self):
        cell_shift = LEFT * 1.15
        mem = build_plasma_membrane(x_min=-5.0, x_max=5.0, n=40).shift(cell_shift)
        er = build_er_sac(center_y=-1.75, rx=3.5, ry=0.72).shift(cell_shift)
        ca_dots = build_er_ca_dots(n=22, seed=7, center_y=-1.75, rx=2.9, ry=0.48).shift(cell_shift)
        er_lbl = T("ER", 28, ER_EDGE, weight=BOLD).next_to(er, LEFT, buff=0.20)
        pip2 = build_macro_pip2(x=0.0, scale=1.12).shift(cell_shift)
        pip2_lbl = T("PIP2 cut", 26, C_PIP2, weight=BOLD).next_to(pip2.head, LEFT, buff=0.24)
        legend = build_color_legend()
        tag = scope_tag("schematic")

        self.at("Return to the original cell")
        self.play(
            FadeIn(mem), FadeIn(er), FadeIn(ca_dots), FadeIn(er_lbl),
            FadeIn(pip2), FadeIn(pip2_lbl), FadeIn(legend), FadeIn(tag),
            run_time=1.8,
        )

        self.at("The moving branch is IP3")
        cut_x = cell_shift[0]
        ip3 = build_ip3_token("IP3", scale=0.90).move_to([cut_x, 0.92, 0])
        route_t = ValueTracker(0.0)
        start_pt = np.array([cut_x, 0.92, 0])
        end_pt = np.array([cut_x - 0.85, -0.58, 0])
        ip3.add_updater(lambda m: m.move_to(start_pt + (end_pt - start_pt) * route_t.get_value()))
        route_arrow = always_redraw(lambda: Arrow(
            start_pt + UP * 0.25,
            start_pt + (end_pt - start_pt) * max(route_t.get_value(), 0.05) + UP * 0.34,
            buff=0, color=C_IP3, stroke_width=6,
        ))
        mob_lbl = chip("mobile branch", color=C_IP3, size=26).move_to([cut_x - 3.05, 0.05, 0])
        self.add(route_arrow, ip3)
        self.play(FadeIn(mob_lbl), route_t.animate.set_value(1.0), run_time=2.0, rate_func=smooth)
        ip3.clear_updaters()

        plume_t = ValueTracker(0.0)
        plume_dots = [d for i, d in enumerate(ca_dots) if i % 2 == 0]
        p0s = [d.get_center().copy() for d in plume_dots]
        rng = np.random.default_rng(7)
        p1s = [np.array([cut_x + rng.uniform(-0.4, 0.9), rng.uniform(-0.35, 0.50), 0]) for _ in plume_dots]
        plume_grp = VGroup(*plume_dots)
        plume_grp.add_updater(lambda m: [d.move_to(p0s[i] + (p1s[i] - p0s[i]) * plume_t.get_value()) for i, d in enumerate(plume_dots)])
        self.play(plume_t.animate.set_value(1.0), run_time=2.5, rate_func=smooth)
        plume_grp.clear_updaters()

        self.at("The local branch is DAG")
        dag_x = ValueTracker(0.8)
        dag = build_dag_token(x=0.8, y_fn=membrane_y_inner, scale=0.90).shift(cell_shift)
        dag.add_updater(lambda m: m.become(build_dag_token(x=dag_x.get_value(), y_fn=membrane_y_inner, scale=0.90).shift(cell_shift)))
        loc_lbl = chip("local branch", color=C_DAG, size=26).move_to([cut_x + 2.35, 0.30, 0])
        self.add(dag)
        self.play(FadeIn(loc_lbl), dag_x.animate.set_value(2.45), run_time=3.2, rate_func=smooth)
        dag.clear_updaters()

        self.at("Keep this rule")
        origin_ring = Circle(radius=0.40, color=C_PIP2, stroke_width=5).move_to(pip2.neck.get_center())
        trace_back_ip3 = Arrow(ip3.get_top() + UP * 0.08, pip2.head.get_bottom() + DOWN * 0.10, buff=0, color=C_PIP2, stroke_width=5)
        self.play(Create(origin_ring), GrowArrow(trace_back_ip3), run_time=1.8)
        self.play(FadeOut(trace_back_ip3), run_time=0.6)

        self.at("sends IP3 away")
        rule1 = T("One PIP2 cut sends IP3 away", 26, C_IP3).move_to([cut_x, -3.12, 0])
        self.play(FadeIn(rule1), ip3.animate.shift(DOWN * 0.14), route_arrow.animate.set_stroke(width=8), run_time=1.6)

        self.at("It leaves DAG at the membrane")
        rule2 = T("One PIP2 cut sends IP3 away, leaves DAG at membrane", 24, TEXT).move_to([cut_x + 0.1, -3.12, 0])
        self.play(swap(rule1, rule2, run_time=0.9), dag.animate(run_time=1.8).shift(RIGHT * 0.30))
        self.finish()


# ====================================================================
# SCENE 10: END CARD
# ====================================================================
class S10End(EndCard):
    LINE = "One PIP2 cut sends IP3 away and leaves DAG at the membrane."
