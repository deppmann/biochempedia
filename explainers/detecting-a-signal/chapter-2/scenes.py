# COLOUR MAP (one colour per concept for the entire film):
#   SLATE (#8B93A1)  = bystander / normal kinases, ordinary ATP, downstream / parallel steps
#   GOLD  (#D4A843)  = target kinase X and its direct substrate
#   GREEN (#83C167)  = phosphate group (P / P*) and cell response meter
#   BLUE  (#58C4DD)  = bulky benzyl-ATP analog (cyan) and shared ATP-pocket highlight
#   RED   (#FC6255)  = chemical ATP-pocket inhibitor and blocked / crossed-out states
#   TEAL  (#3FB8C0)  = hormone signal and parallel bypass pathway
#   GENETIC (#B388EB)= genetic knockout / site mutant method
#
# CARRIED WORLD:
#   A schematic kinase panel (slate bystander kinases around gold Kinase X, all sharing a notched
#   ATP pocket) paired with an emerald cell-response meter. Scenes zoom into Kinase X's pocket
#   to show gatekeeper reshaping and back out to the panel + meter to test inhibitors, rescue,
#   and sufficiency vs necessity.
#
# WHAT CHANGES PER SPOKEN SCENE (and what drives it):
#   s01_hook:            Bystander proteins slide aside as scanner locks onto target P; 16-kinase grid expands while counter runs 1 -> 500; pocket trace sweeps notches; candidate arrows probe response.
#   s02_naive_fails:     Left & right panels build; cyan ATP* capsules enter all 4 kinases -> all 4 substrates light up green; removing X dims X and drops P sequentially down X -> K2 -> K3 -> Target.
#   s03_shokat:          Normal kinase & Kinase X build; narrow-cleft caliper highlights gatekeeper; Kinase X gatekeeper shrinks to Gly/Ala opening left recess; bulky cyan ATP analog glides down.
#   s04_shokat_transfer: Bulky analog rebounds off Normal kinase's gatekeeper while ordinary ATP transfers grey P; analog docks in Kinase X, transfers emerald P* to gold substrate, and benzyl-ADP lifts away.
#   s05_inhibitors:      Coral wedges plug X + 10 slate kinases while response meter drops 100% -> 0%; 2007 and 2008 panel-survey bars grow from lesson data as off-target markers light across the grid.
#   s06_asymmetry_rescue:Response meter stays 100% when plugged (ruled out) -> drains 100% -> 0% (ambiguous ?) -> X mutates to resistant pocket, wedge bounces off X while slate kinases stay plugged, meter refills 0% -> 100%.
#   s07_nec_suff_predict:Necessary test crosses X and drops meter 100% -> 0%; sufficient test turns Hormone OFF and X ON alone, raising meter 0% -> 100% with live signal packet moving X -> meter.
#   s09_reveal_close:    Hormone turns ON, X is crossed out, teal parallel pathway draws and carries signal to keep meter 100%; both method blind spots appear then converge with green checkmarks onto one causal claim.

from bp_parts import *

# ---------------------------------------------------------------------------
# Colour map
# ---------------------------------------------------------------------------
SLATE = GREY          # #8B93A1: bystander / normal kinases, ordinary ATP
TARGET = GOLD         # #D4A843: target kinase X and its direct substrate
PHOS = GREEN          # #83C167: phosphate (P / P*) and cell response meter
ANALOG = BLUE         # #58C4DD: bulky benzyl-ATP analog (cyan)
INHIB = RED           # #FC6255: chemical inhibitor and blocked / crossed-out states
HORMONE = TEAL        # #3FB8C0: hormone signal and parallel bypass
GENETIC = "#B388EB"   # violet: genetic knockout / site mutant method


# ---------------------------------------------------------------------------
# Reusable schematic builders
# ---------------------------------------------------------------------------
def make_small_kinase(label_text="", color=SLATE, w=1.35, h=0.98, resistant=False, fill_opacity=0.22):
    """Schematic kinase block with a top ATP-pocket notch (and optional steric bump for drug resistance)."""
    pw = w * 0.40
    pd = h * 0.30
    pts = [
        (-w / 2, h / 2),
        (-pw / 2, h / 2),
        (-pw / 2, h / 2 - pd),
        (pw / 2, h / 2 - pd),
        (pw / 2, h / 2),
        (w / 2, h / 2),
        (w / 2, -h / 2),
        (-w / 2, -h / 2),
    ]
    body = Polygon(*[[x, y, 0] for x, y in pts], stroke_color=color, stroke_width=3.2,
                   fill_color=color, fill_opacity=fill_opacity)
    g = VGroup(body)
    if resistant:
        bump = RoundedRectangle(corner_radius=0.05, width=pw * 0.40, height=pd * 0.62,
                                stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.78)
        bump.move_to([0.0, h / 2 - pd * 0.55, 0])
        g.add(bump)
        g.bump = bump
    if label_text:
        lab = T(label_text, size=24, color=TEXT if color == TARGET else color)
        lab.move_to([0.0, -h * 0.25, 0])
        g.add(lab)
        g.label = lab
    g.body = body
    g.pocket_top = np.array([0.0, h / 2, 0.0])
    g.pocket_mid = np.array([0.0, h / 2 - pd * 0.46, 0.0])
    return g


def make_wedge(w=0.42, h=0.26, color=INHIB):
    """Coral-red ATP-pocket inhibitor wedge sized to sit cleanly inside the pocket notch."""
    pts = [
        (-w * 0.60, h * 0.50),
        (w * 0.60, h * 0.50),
        (w * 0.42, -h * 0.45),
        (-w * 0.42, -h * 0.45),
    ]
    return Polygon(*[[x, y, 0] for x, y in pts], stroke_color=color, stroke_width=2.5,
                   fill_color=color, fill_opacity=0.85)


def make_cross(mob, color=INHIB, scale=0.85, stroke=6):
    """A crisp X cross-out over a mobject."""
    c = mob.get_center()
    dx = mob.width * 0.45 * scale
    dy = mob.height * 0.45 * scale
    l1 = Line(c + [-dx, -dy, 0], c + [dx, dy, 0], color=color, stroke_width=stroke)
    l2 = Line(c + [-dx, dy, 0], c + [dx, -dy, 0], color=color, stroke_width=stroke)
    g = VGroup(l1, l2)
    g.layout_ok = True
    return g


def make_phosphate(text="P", radius=0.21, color=PHOS, font_size=22):
    """Emerald phosphate dot with label inside."""
    dot = Circle(radius=radius, stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.90)
    lbl = T(text, size=font_size, color=BG, weight=BOLD).move_to(dot)
    lbl.layout_ok = True
    g = VGroup(dot, lbl)
    g.dot = dot
    return g


def make_pocket_kinase(label_text, color=SLATE, center=ORIGIN, open_pocket=False):
    """Large zoomed-in kinase block with wide ATP pocket and separate gatekeeper lobe on the left wall."""
    W, H = 3.8, 3.0
    pl, pr, pd = -1.25, 0.80, 1.35
    pts = [
        (-W / 2, H / 2),
        (pl, H / 2),
        (pl, H / 2 - pd),
        (pr, H / 2 - pd),
        (pr, H / 2),
        (W / 2, H / 2),
        (W / 2, -H / 2),
        (-W / 2, -H / 2),
    ]
    body = Polygon(*[[x, y, 0] for x, y in pts], stroke_color=color, stroke_width=4,
                   fill_color=color, fill_opacity=0.20)
    gk_w = 0.16 if open_pocket else 0.72
    gk_h = 0.34 if open_pocket else 0.88
    gk = RoundedRectangle(corner_radius=0.10, width=gk_w, height=gk_h,
                          stroke_color=SLATE, stroke_width=3, fill_color=SLATE, fill_opacity=0.72)
    gk.move_to([pl + gk_w / 2 + 0.03, H / 2 - pd * 0.52, 0])

    lab = T(label_text, size=28, color=TEXT if color == TARGET else color, weight=BOLD)
    lab.move_to([0.0, -H * 0.27, 0])

    g = VGroup(body, gk, lab).move_to(center)
    g.body = body
    g.gk = gk
    g.label = lab
    g.pocket_center = np.array([center[0] - 0.18, center[1] + H / 2 - pd * 0.45, 0.0])
    g.slot_x = center[0] + 0.15
    g.recess_x = center[0] - 0.60
    g.top_y = center[1] + H / 2
    return g


def make_bulky_analog(with_phos=True):
    """Schematic bulky benzyl-ATP analog: adenine core + left benzyl wing + optional emerald gamma P*."""
    core = RoundedRectangle(corner_radius=0.10, width=0.52, height=0.92,
                            stroke_color=ANALOG, stroke_width=3, fill_color=ANALOG, fill_opacity=0.35)
    wing = RoundedRectangle(corner_radius=0.10, width=0.46, height=0.44,
                            stroke_color=ANALOG, stroke_width=3, fill_color=ANALOG, fill_opacity=0.65)
    wing.next_to(core, LEFT, buff=0.0).shift(UP * 0.04)
    adenine_lbl = T("A", size=24, color=TEXT, weight=BOLD).move_to(core)
    adenine_lbl.layout_ok = True
    g = VGroup(core, wing, adenine_lbl)
    g.core = core
    g.wing = wing
    if with_phos:
        stem = Line(core.get_right(), core.get_right() + RIGHT * 0.22, color=ANALOG, stroke_width=4)
        p = make_phosphate("P*", radius=0.21, color=PHOS, font_size=22)
        p.next_to(stem, RIGHT, buff=0.03)
        g.add(stem, p)
        g.stem = stem
        g.phos = p
    return g


def make_ordinary_atp(phos_color=SLATE, phos_text="P", body_color=SLATE, body_label="ATP"):
    """Ordinary ATP (no benzyl wing)."""
    core = RoundedRectangle(corner_radius=0.10, width=0.70, height=0.74,
                            stroke_color=body_color, stroke_width=3, fill_color=body_color, fill_opacity=0.30)
    lbl = T(body_label, size=22, color=TEXT).move_to(core)
    p = make_phosphate(phos_text, radius=0.16, color=phos_color, font_size=22)
    p.next_to(core, UP, buff=0.06)
    g = VGroup(core, lbl, p)
    g.core = core
    g.phos = p
    return g


def build_kinase_panel(origin=(-2.9, 0.0, 0), x_idx=(1, 2), resistant=False):
    """4x4 schematic kinase grid (Kinase X at x_idx, 15 slate bystander kinases)."""
    grid = VGroup()
    kinases = []
    for r in range(4):
        for c in range(4):
            is_x = (r, c) == x_idx
            k = make_small_kinase(
                "X" if is_x else "",
                color=TARGET if is_x else SLATE,
                w=1.35, h=0.98,
                resistant=(is_x and resistant),
                fill_opacity=0.28 if is_x else 0.18,
            )
            kinases.append((r, c, is_x, k))
            grid.add(k)
    grid.arrange_in_grid(rows=4, cols=4, buff=(0.24, 0.32)).move_to(origin)
    x_mob = next(k for _, _, is_x, k in kinases if is_x)
    others = [k for _, _, is_x, k in kinases if not is_x]
    return grid, x_mob, others


def make_response_meter(tracker, center=(4.8, 0.2, 0), w=0.95, h=3.4):
    """Vertical emerald response meter driven by a 0..1 ValueTracker, with live % readout."""
    c = np.array(center, dtype=float)
    frame = RoundedRectangle(corner_radius=0.14, width=w, height=h,
                             stroke_color=SLATE, stroke_width=3, fill_color=BG, fill_opacity=0.95).move_to(c)
    bottom_y = c[1] - h / 2 + 0.08
    max_fill_h = h - 0.16

    def _fill():
        v = float(np.clip(tracker.get_value(), 0.0, 1.0))
        fh = max(0.06, v * max_fill_h)
        r = RoundedRectangle(corner_radius=0.08, width=w - 0.16, height=fh,
                             stroke_width=0, fill_color=PHOS, fill_opacity=0.88 if v > 0.05 else 0.15)
        r.move_to([c[0], bottom_y + fh / 2, 0])
        return r

    bar = always_redraw(_fill)
    title = T("cell\nresponse", size=24, color=PHOS, line_spacing=0.85).next_to(frame, UP, buff=0.16)
    readout = always_redraw(
        lambda: M(f"{tracker.get_value() * 100:.0f}%", size=28, color=PHOS if tracker.get_value() > 0.4 else INHIB)
        .next_to(frame, DOWN, buff=0.16)
    )
    return VGroup(frame, bar, title, readout)


def build_predict_world():
    """Shared builder for end of S07 and S08Pause."""
    hormone = boxed_label("No hormone", color=SLATE, size=28, box=(2.7, 1.15), fill_opacity=0.14).move_to([-4.6, 0.25, 0])
    kin_x = boxed_label("Always-active X", color=TARGET, size=28, box=(3.4, 1.35), fill_opacity=0.28).move_to([0.0, 0.25, 0])
    resp_t = ValueTracker(1.0)
    meter = make_response_meter(resp_t, center=[4.6, 0.25, 0], w=1.0, h=3.1)
    a1 = DashedLine(hormone.get_right() + RIGHT * 0.12, kin_x.get_left() + LEFT * 0.12,
                    color=SLATE, stroke_width=3, dash_length=0.14).set_opacity(0.45)
    a2 = Arrow(kin_x.get_right() + RIGHT * 0.12, meter[0].get_left() + LEFT * 0.12,
               buff=0, color=TARGET, stroke_width=5, max_tip_length_to_length_ratio=0.14)
    tag = scope_tag("schematic").move_to([5.65, 3.35, 0])
    return VGroup(hormone, kin_x, meter, a1, a2, tag), hormone, kin_x, meter, resp_t, a1, a2


# ---------------------------------------------------------------------------
# Scenes
# ---------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "How We Know: Detecting a Signal"
    TITLE = "Proving Which Kinase Did the Work"


class S01Hook(SpokenScene):
    def construct(self):
        target_box = RoundedRectangle(corner_radius=0.18, width=3.2, height=1.45,
                                      stroke_color=TARGET, stroke_width=4, fill_color=TARGET, fill_opacity=0.24)
        target_lbl = T("target protein", size=28, color=TARGET, weight=BOLD).move_to(target_box)
        p_dot = make_phosphate("P", radius=0.24, color=PHOS, font_size=24)
        # Keep P cleanly above target_box border (0.06+ clearance -> zero box_overlap)
        p_dot.move_to(target_box.get_top() + [0.95, 0.32, 0])
        target_grp = VGroup(target_box, target_lbl, p_dot).move_to([0.0, -0.1, 0])

        crowd = VGroup()
        crowd_pos = [(-4.3, 1.85), (-1.4, 2.05), (1.7, 2.05), (4.4, 1.75),
                     (-4.2, -1.85), (-1.2, -2.05), (1.8, -1.95), (4.3, -1.75)]
        for x, y in crowd_pos:
            b = RoundedRectangle(corner_radius=0.12, width=1.8, height=0.75,
                                 stroke_color=SLATE, stroke_width=2.5, fill_color=SLATE, fill_opacity=0.14).move_to([x, y, 0])
            crowd.add(b)

        scan_x = ValueTracker(-5.2)
        scanner = always_redraw(
            lambda: Line([scan_x.get_value(), -2.6, 0], [scan_x.get_value(), 2.6, 0], color=ANALOG, stroke_width=4)
        )
        scanner.layout_ok = True
        p_badge = place_label(T("1 phosphate found", size=28, color=PHOS), p_dot, avoid=[target_grp], dirs=(UP,))
        tag = scope_tag("schematic")

        # Start visible immediately (no dark opening frame)
        self.add(tag, crowd, target_box, target_lbl, scanner)
        self.play(scan_x.animate.set_value(5.2), FadeIn(p_dot), run_time=3.4, rate_func=linear)
        self.at("find one phosphate")
        self.play(FadeOut(scanner, run_time=0.4), crowd.animate.set_opacity(0.20), FadeIn(p_badge, run_time=0.5), run_time=1.0)
        self.play(crowd.animate.shift(LEFT * 0.8).set_opacity(0.0), run_time=2.4)
        self.remove(crowd)

        self.at("Finding that mark")
        target_full = VGroup(target_box, target_lbl, p_dot)
        self.play(
            FadeOut(p_badge, run_time=0.4),
            target_full.animate.scale(0.84).move_to([4.25, 0.25, 0]),
            run_time=1.1,
        )
        target_cap = T("phosphorylated target", size=24, color=TARGET).next_to(target_full, DOWN, buff=0.22)
        q_arrow = Arrow([1.75, 0.25, 0], target_full.get_left() + LEFT * 0.14,
                        buff=0, color=GOLD, stroke_width=4)
        q_mark = T("?", size=38, color=GOLD, weight=BOLD).next_to(q_arrow, UP, buff=0.12)
        self.play(FadeIn(target_cap), GrowArrow(q_arrow), FadeIn(q_mark), run_time=1.0)

        grid, x_mob, others = build_kinase_panel(origin=(-2.8, -0.35, 0), x_idx=(1, 2))
        n_track = ValueTracker(1)
        kin_counter = counter("~{:.0f} human kinases", n_track, at=[-2.8, 2.42, 0], size=30, color=TEXT, mono=False)
        self.add(kin_counter)
        self.play(
            LaggedStart(*[FadeIn(m, scale=0.88) for m in grid], lag_ratio=0.06),
            n_track.animate.set_value(500),
            run_time=1.5,
            rate_func=linear,
        )
        self.at("Roughly 500 human kinases")

        self.at("share a similar ATP pocket")
        pocket_hl = RoundedRectangle(corner_radius=0.06, width=0.60, height=0.38,
                                     stroke_color=ANALOG, stroke_width=4, fill_opacity=0)
        sample_kinases = [grid[0], grid[5], x_mob, grid[10], grid[14]]
        pocket_hl.move_to(sample_kinases[0].get_center() + sample_kinases[0].pocket_mid)
        pocket_lbl = T("similar ATP pocket", size=26, color=ANALOG).move_to([3.8, 1.85, 0])
        self.play(FadeIn(pocket_hl), FadeIn(pocket_lbl), run_time=0.5)
        for km in sample_kinases[1:]:
            self.play(pocket_hl.animate.move_to(km.get_center() + km.pocket_mid), run_time=0.65)

        self.at("How do you prove")
        self.play(FadeOut(pocket_hl, run_time=0.3), FadeOut(pocket_lbl, run_time=0.3), run_time=0.35)
        head_q = fit_text("Which kinase added it, and caused the response?", max_w=12.0, size=32, color=GOLD, weight=BOLD)
        head_q.move_to([0.0, HEAD_Y, 0])
        resp_box = boxed_label("cell response ?", color=PHOS, size=26, box=(2.9, 0.85), fill_opacity=0.16)
        resp_box.move_to([4.25, -2.15, 0])
        resp_arrow = Arrow(target_cap.get_bottom() + DOWN * 0.12, resp_box.get_top() + UP * 0.10,
                           buff=0, color=PHOS, stroke_width=4)
        self.play(FadeIn(head_q, shift=DOWN * 0.1), FadeIn(resp_box), GrowArrow(resp_arrow), run_time=1.2)
        # Keep arrow pulse / highlight on X -> target until end
        probe = Dot(q_arrow.get_start(), radius=0.10, color=GOLD)
        self.add(probe)
        self.play(probe.animate.move_to(q_arrow.get_end()), run_time=1.4, rate_func=linear)
        self.play(FadeOut(probe, run_time=0.3), run_time=0.3)
        self.finish()


class S02NaiveFails(SpokenScene):
    def construct(self):
        tp = TwoPanel("Test 1: ordinary radioactive ATP", "Test 2: remove kinase X",
                      colors=(SLATE, INHIB), top=3.15, bottom=-2.75, gap=0.4, width=12.8, size=30)
        tag = scope_tag("schematic")
        self.add(tag, tp)

        lx = tp.area("left")[0][0]
        names_l = [("X", TARGET), ("K2", SLATE), ("K3", SLATE), ("K4", SLATE)]
        kin_l = VGroup(*[make_small_kinase(n, color=c, w=1.22, h=0.92) for n, c in names_l])
        kin_l.arrange(RIGHT, buff=0.26).move_to([lx, 0.85, 0])

        subs_l = VGroup(*[
            boxed_label(s, color=c, size=24, box=(1.22, 0.72), fill_opacity=0.18)
            for s, c in [("S1", TARGET), ("S2", SLATE), ("S3", SLATE), ("S4", SLATE)]
        ]).arrange(RIGHT, buff=0.26).move_to([lx, -1.05, 0])

        arrows_l = VGroup(*[
            Arrow(k.get_bottom() + DOWN * 0.10, s.get_top() + UP * 0.10, buff=0, color=SLATE, stroke_width=3)
            for k, s in zip(kin_l, subs_l)
        ])

        rx = tp.area("right")[0][0]
        chain_specs = [("X", TARGET), ("K2", SLATE), ("K3", SLATE), ("Target", SLATE)]
        chain = VGroup(*[
            boxed_label(n, color=c, size=24, box=(1.15, 0.85), fill_opacity=0.20)
            for n, c in chain_specs
        ]).arrange(RIGHT, buff=0.36).move_to([rx, 0.45, 0])
        chain_arrows = VGroup(*[
            Arrow(chain[i].get_right() + RIGHT * 0.08, chain[i + 1].get_left() + LEFT * 0.08,
                  buff=0, color=SLATE, stroke_width=3.5)
            for i in range(3)
        ])
        chain_p = VGroup(*[
            make_phosphate("P", radius=0.19, color=PHOS, font_size=22).next_to(chain[i], UP, buff=0.16)
            for i in (1, 2, 3)
        ])

        # Build left & right panels smoothly across 0.0..4.5s (prevents early static freeze)
        self.play(LaggedStart(*[FadeIn(k, shift=DOWN * 0.1) for k in kin_l], lag_ratio=0.18), run_time=1.3)
        self.play(
            LaggedStart(*[GrowArrow(a) for a in arrows_l], lag_ratio=0.15),
            LaggedStart(*[FadeIn(s, shift=UP * 0.1) for s in subs_l], lag_ratio=0.15),
            run_time=1.3,
        )
        self.play(
            LaggedStart(*[FadeIn(c) for c in chain], lag_ratio=0.15),
            LaggedStart(*[GrowArrow(a) for a in chain_arrows], lag_ratio=0.15),
            LaggedStart(*[FadeIn(p, shift=DOWN * 0.1) for p in chain_p], lag_ratio=0.15),
            run_time=1.6,
        )

        # Beat 1: Add ordinary radioactive ATP
        self.at("Add ordinary radioactive")
        atp_caps = VGroup()
        for k in kin_l:
            cap = RoundedRectangle(corner_radius=0.07, width=0.38, height=0.28,
                                   stroke_color=SLATE, stroke_width=2.5, fill_color=SLATE, fill_opacity=0.65)
            p_dot = make_phosphate("P*", radius=0.18, color=PHOS, font_size=22)
            g = VGroup(cap, p_dot).arrange(RIGHT, buff=0.06).move_to([k.get_center()[0], 2.15, 0])
            atp_caps.add(g)
        self.play(FadeIn(atp_caps, shift=DOWN * 0.2), run_time=0.6)
        self.play(
            *[a.animate.move_to(k.get_center() + k.pocket_top + UP * 0.22) for a, k in zip(atp_caps, kin_l)],
            run_time=2.6,
            rate_func=linear,
        )

        # Beat 2: Every active kinase labels its substrates at once
        self.at("every active kinase labels")
        sub_p = VGroup(*[
            make_phosphate("P*", radius=0.19, color=PHOS, font_size=22).move_to(k.get_bottom() + [0.42, -0.26, 0])
            for k in kin_l
        ])
        self.play(
            FadeOut(atp_caps, run_time=0.4),
            *[p.animate.move_to(s.get_top() + [0.42, 0.26, 0]) for p, s in zip(sub_p, subs_l)],
            run_time=2.0,
            rate_func=linear,
        )
        left_res = boxed_label("all targets labelled", color=INHIB, size=24, box=(3.4, 0.65), fill_opacity=0.16)
        left_res.move_to([lx, -2.1, 0])
        self.play(
            *[s.box.animate.set_stroke(PHOS, width=3.5) for s in subs_l],
            FadeIn(left_res, run_time=0.5),
            run_time=1.0,
        )

        # Beat 3: Or remove kinase X from cells
        self.at("remove kinase X")
        x_cross = make_cross(chain[0], color=INHIB, scale=0.85, stroke=6)
        self.play(chain[0].animate.set_opacity(0.32), Create(x_cross), run_time=1.4)

        # Beat 4: Phosphorylation drops on direct targets and three steps downstream
        self.at("Phosphorylation drops")
        for idx, (p_mob, lbl_txt, dx) in enumerate([
            (chain_p[0], "direct:\nP drops", -1.45),
            (chain_p[1], "", 0.0),
            (chain_p[2], "3 steps down:\nP drops", 1.45),
        ]):
            # Dim each downstream kinase + arrow clearly as phosphorylation drops
            node = chain[idx + 1]
            anims = [
                p_mob.animate.shift(DOWN * 0.22).set_opacity(0.10),
                chain_arrows[idx].animate.set_color(INHIB).set_opacity(0.30),
                node.box.animate.set_stroke(INHIB, width=2.5).set_fill(INHIB, opacity=0.08),
            ]
            if lbl_txt:
                dt = fit_text(lbl_txt, max_w=2.3, size=22, color=INHIB).move_to([rx + dx, -0.75, 0])
                anims.append(FadeIn(dt, run_time=0.4))
            self.play(*anims, run_time=0.9)
            if idx == 0:
                self.at("and on proteins")
            elif idx == 1:
                self.at("three steps downstream")

        right_res = boxed_label("both look identical", color=INHIB, size=24, box=(3.4, 0.65), fill_opacity=0.16)
        right_res.move_to([rx, -2.1, 0])
        self.play(FadeIn(right_res, run_time=0.5), run_time=0.5)
        self.finish()


class S03Shokat(SpokenScene):
    def construct(self):
        head = T("Reshaping kinase X's ATP pocket", size=34, color=TEXT, weight=BOLD).move_to([0.0, HEAD_Y, 0])
        tag = scope_tag("schematic")
        self.add(tag, head)

        norm_k = make_pocket_kinase("Normal kinase", color=SLATE, center=[-2.5, -0.45, 0], open_pocket=False)
        kin_x = make_pocket_kinase("Kinase X", color=TARGET, center=[2.2, -0.45, 0], open_pocket=False)

        self.play(Create(norm_k.body), Create(kin_x.body), run_time=1.6)
        self.at("solved this by")
        self.play(
            FadeIn(norm_k.gk, shift=RIGHT * 0.4), FadeIn(norm_k.label, shift=UP * 0.15),
            FadeIn(kin_x.gk, shift=RIGHT * 0.4), FadeIn(kin_x.label, shift=UP * 0.15),
            run_time=1.8,
        )
        # Sweep focus across both pockets up to 6.28s
        self.play(
            norm_k.body.animate.set_fill(SLATE, opacity=0.34),
            kin_x.body.animate.set_fill(TARGET, opacity=0.34),
            run_time=1.1,
        )
        self.play(
            norm_k.body.animate.set_fill(SLATE, opacity=0.20),
            kin_x.body.animate.set_fill(TARGET, opacity=0.20),
            run_time=1.1,
        )

        # Highlight bulky gatekeeper in normal kinase and test ordinary ATP fit
        self.at("In a normal kinase")
        gk_lbl = T("bulky gatekeeper", size=26, color=TEXT).move_to([-4.55, 2.15, 0])
        gk_ptr = Arrow(gk_lbl.get_bottom() + DOWN * 0.06, norm_k.gk.get_top() + UP * 0.14,
                       buff=0, color=TEXT, stroke_width=3.5, max_tip_length_to_length_ratio=0.18)
        narrow_arrow = DoubleArrow(
            [norm_k.gk.get_right()[0] + 0.06, norm_k.pocket_center[1], 0],
            [norm_k.get_center()[0] + 0.80 - 0.06, norm_k.pocket_center[1], 0],
            buff=0, color=INHIB, stroke_width=3.5, tip_length=0.14,
        )
        narrow_lbl = T("narrow", size=24, color=INHIB).next_to(norm_k, DOWN, buff=0.22)
        self.play(
            norm_k.gk.animate.set_fill(INHIB, opacity=0.82).set_stroke(INHIB),
            norm_k.body.animate.set_fill(SLATE, opacity=0.30),
            FadeIn(gk_lbl, run_time=0.5), GrowArrow(gk_ptr),
            Create(narrow_arrow), FadeIn(narrow_lbl, run_time=0.5),
            run_time=1.8,
        )
        # Ordinary ATP enters and leaves the narrow cleft cleanly
        probe_atp = make_ordinary_atp().move_to([norm_k.slot_x, 2.25, 0])
        self.play(FadeOut(narrow_arrow, run_time=0.35), FadeIn(probe_atp, shift=DOWN * 0.3), run_time=0.7)
        self.play(probe_atp.animate.move_to([norm_k.slot_x, norm_k.pocket_center[1] - 0.10, 0]), run_time=1.6)
        self.play(probe_atp.animate.shift(UP * 1.4).set_opacity(0.0), norm_k.body.animate.set_fill(SLATE, opacity=0.20), run_time=1.3)
        self.remove(probe_atp)

        # Mutate gatekeeper in Kinase X to small Gly / Ala and illuminate open recess
        self.at("Mutate that gatekeeper")
        x_open_k = make_pocket_kinase("Kinase X", color=TARGET, center=[2.2, -0.45, 0], open_pocket=True)
        gly_lbl = T("Gly / Ala", size=26, color=TARGET).move_to([1.65, 2.05, 0])
        gly_ptr = Arrow(gly_lbl.get_bottom() + DOWN * 0.06, x_open_k.gk.get_top() + UP * 0.14,
                        buff=0, color=TARGET, stroke_width=3.5, max_tip_length_to_length_ratio=0.18)
        self.play(
            Transform(kin_x.gk, x_open_k.gk),
            kin_x.body.animate.set_fill(TARGET, opacity=0.32),
            FadeIn(gly_lbl, run_time=0.5), GrowArrow(gly_ptr),
            run_time=2.5,
        )

        self.at("opening a hole")
        hole_ring = DashedVMobject(
            RoundedRectangle(corner_radius=0.12, width=0.56, height=0.84, stroke_color=PHOS, stroke_width=4),
            num_dashes=14,
        ).move_to([kin_x.recess_x + 0.06, kin_x.pocket_center[1], 0])
        hole_glow = RoundedRectangle(corner_radius=0.12, width=0.56, height=0.84,
                                     stroke_width=0, fill_color=PHOS, fill_opacity=0.35).move_to(hole_ring)
        hole_lbl = T("open recess", size=24, color=PHOS).next_to(kin_x, DOWN, buff=0.22)
        self.play(Create(hole_ring), FadeIn(hole_glow), FadeIn(hole_lbl, run_time=0.5), run_time=1.4)
        self.play(FadeOut(hole_glow), kin_x.body.animate.set_fill(TARGET, opacity=0.20), run_time=0.9)

        # Supply bulky benzyl ATP analog cleanly below heading
        self.at("Now supply a")
        analog = make_bulky_analog(with_phos=True).move_to([-0.2, 2.25, 0])
        self.play(
            FadeOut(gk_lbl, run_time=0.4), FadeOut(gk_ptr, run_time=0.4),
            FadeOut(gly_lbl, run_time=0.4), FadeOut(gly_ptr, run_time=0.4),
            FadeIn(analog, shift=DOWN * 0.2),
            run_time=1.0,
        )
        self.play(analog.animate.move_to([-0.2, 1.75, 0]), run_time=1.4)
        benzyl_lbl = T("bulky benzyl\non adenine", size=24, color=ANALOG, line_spacing=0.85).next_to(analog.wing, LEFT, buff=0.25)
        self.play(FadeIn(benzyl_lbl, run_time=0.5), run_time=0.8)

        self.at("carrying a radioactive")
        gamma_lbl = T("gamma P*", size=24, color=PHOS).next_to(analog.phos, RIGHT, buff=0.22)
        self.play(FadeIn(gamma_lbl, run_time=0.5), analog.phos.animate.scale(1.18), run_time=1.0)
        self.play(analog.phos.animate.scale(1 / 1.18), run_time=0.8)
        self.finish()


class S04ShokatTransfer(SpokenScene):
    def construct(self):
        tag = scope_tag("schematic")
        self.add(tag)

        norm_k = make_pocket_kinase("Normal kinase", color=SLATE, center=[-2.5, -0.45, 0], open_pocket=False)
        norm_k.gk.set_fill(INHIB, opacity=0.75).set_stroke(INHIB)
        kin_x = make_pocket_kinase("Kinase X", color=TARGET, center=[2.2, -0.45, 0], open_pocket=True)

        norm_sub = boxed_label("other\nsubstrate", color=SLATE, size=24, box=(1.65, 1.2), fill_opacity=0.16)
        norm_sub.move_to([-5.40, 0.15, 0])
        x_sub = boxed_label("substrate", color=TARGET, size=26, box=(1.75, 1.2), fill_opacity=0.24)
        x_sub.move_to([5.35, 0.15, 0])

        analog = make_bulky_analog(with_phos=True).move_to([-0.2, 1.75, 0])
        self.add(norm_k, kin_x, norm_sub, x_sub, analog)

        # Smooth lead-in motion before cue
        self.play(analog.animate.move_to([-1.2, 1.85, 0]), run_time=1.3)

        # Beat 1: Bulky benzyl fits normal pockets poorly (collision + bounce)
        self.at("fits normal pockets poorly")
        target_try = np.array([norm_k.slot_x - 0.45, norm_k.top_y + 0.12, 0.0])
        self.play(analog.animate.move_to(target_try), run_time=0.8)
        clash = make_cross(norm_k.gk, color=TEXT, scale=0.75, stroke=6)
        clash_lbl = T("steric clash!", size=26, color=INHIB, weight=BOLD).next_to(norm_k, UP, buff=0.95)
        self.play(analog.animate.shift(DOWN * 0.25), FadeIn(clash), FadeIn(clash_lbl), run_time=0.35)
        self.play(analog.animate.move_to([-0.1, 2.05, 0]), FadeOut(clash), FadeOut(clash_lbl), run_time=0.9)

        # Beat 2: Ordinary ATP fits normal kinase silently (transfers left without crossing label)
        self.at("other kinases keep using")
        ord_atp = make_ordinary_atp().move_to([norm_k.slot_x, 2.35, 0])
        self.play(FadeIn(ord_atp, shift=DOWN * 0.2), run_time=0.6)
        self.play(ord_atp.animate.move_to([norm_k.slot_x, norm_k.pocket_center[1] - 0.10, 0]), run_time=1.3)
        grey_p = ord_atp.phos.copy()
        self.add(grey_p)
        silent_lbl = T("silent:\nunlabelled P", size=22, color=SLATE, line_spacing=0.85).move_to([-5.48, -1.25, 0])
        # Move grey_p cleanly left onto other substrate top (0.28 above box top -> zero overlap)
        self.play(
            grey_p.animate.move_to(norm_sub.get_top() + UP * 0.28),
            FadeOut(ord_atp, run_time=0.4),
            FadeIn(silent_lbl, run_time=0.5),
            run_time=1.4,
        )

        # Beat 3: Only engineered Kinase X accepts the bulky analog
        self.at("Only engineered")
        dock_pos = np.array([kin_x.get_center()[0] - 0.135, kin_x.pocket_center[1] + 0.18, 0.0])
        self.play(analog.animate.move_to([dock_pos[0], 2.05, 0]), run_time=1.4)
        self.play(analog.animate.move_to(dock_pos), run_time=1.8)
        fit_lbl = T("fits enlarged pocket", size=24, color=ANALOG).next_to(kin_x, DOWN, buff=0.22)
        self.play(FadeIn(fit_lbl), run_time=1.0)

        # Beat 4: Transfers radioactive phosphate to direct substrates
        self.at("transfers its radioactive phosphate")
        transferred_p = make_phosphate("P*", radius=0.25, color=PHOS, font_size=22).move_to(analog.phos.get_center())
        self.add(transferred_p)
        analog.phos.set_opacity(0)
        analog.stem.set_opacity(0)
        cand_lbl = T("direct\nsubstrate\ncandidate", size=24, color=PHOS, weight=BOLD, line_spacing=0.82)
        cand_lbl.move_to([5.35, -1.28, 0])
        # Keep transferred_p 0.12 clear above x_sub's top border even during 1.18x pulse
        self.play(
            transferred_p.animate.move_to(x_sub.get_top() + UP * 0.38),
            x_sub.box.animate.set_stroke(PHOS, width=4),
            FadeIn(cand_lbl),
            run_time=2.2,
        )

        # Beat 5: Bulky group stays behind on adenine; only the phosphate moves
        self.at("The bulky group stays")
        benzyl_adp = VGroup(analog.core, analog.wing, analog[2])
        stay_lbl = T("benzyl stays on adenine", size=26, color=ANALOG).move_to([0.0, 3.15, 0])
        self.play(FadeIn(stay_lbl), benzyl_adp.animate.move_to([1.6, 1.95, 0]), run_time=1.5)
        self.at("only the phosphate moves")
        self.play(
            benzyl_adp.animate.shift(LEFT * 1.4).set_opacity(0.30),
            transferred_p.animate.scale(1.18),
            run_time=1.2,
        )
        self.play(transferred_p.animate.scale(1 / 1.18), run_time=0.5)
        self.finish()


class S05Inhibitors(SpokenScene):
    def construct(self):
        head = T("Chemical ATP-pocket inhibitors", size=32, color=TEXT, weight=BOLD).move_to([-1.2, HEAD_Y, 0])
        tag = scope_tag("schematic")
        grid, x_mob, others = build_kinase_panel(origin=(-2.9, -0.1, 0), x_idx=(1, 2))
        resp_t = ValueTracker(1.0)
        meter = make_response_meter(resp_t, center=[5.15, 1.05, 0], w=0.95, h=2.15)

        # Visible immediately at t=0, build rows 2-4 + meter cleanly up to 4.8s
        self.add(tag, head, grid[:4], x_mob)
        self.play(LaggedStart(*[FadeIn(k, shift=UP * 0.15) for k in grid[4:] if k is not x_mob], lag_ratio=0.09), run_time=2.5)
        self.play(FadeIn(meter, shift=LEFT * 0.2), run_time=1.6)

        # Beat 1: Inhibitor plugs ATP pockets
        self.at("Labs often add")
        plugged_targets = [x_mob] + others[:10]
        wedges = VGroup()
        for km in plugged_targets:
            w = make_wedge(color=INHIB).move_to(km.get_center() + km.pocket_top + UP * 0.12)
            wedges.add(w)
        inh_lbl = T("ATP-pocket inhibitor", size=26, color=INHIB).move_to([2.35, 1.85, 0])
        self.play(FadeIn(inh_lbl), FadeIn(wedges, shift=DOWN * 0.1), run_time=0.7)
        self.play(
            LaggedStart(*[w.animate.move_to(km.get_center() + km.pocket_mid + UP * 0.08) for w, km in zip(wedges, plugged_targets)], lag_ratio=0.06),
            LaggedStart(*[km.body.animate.set_fill(opacity=0.08).set_stroke(opacity=0.45) for km in plugged_targets], lag_ratio=0.06),
            x_mob.label.animate.set_opacity(0.45),
            resp_t.animate.set_value(0.0),
            run_time=3.6,
        )

        # Beat 2: Selectivity is hard across hundreds of kinases
        self.at("hundreds of kinases share")
        off_lbl = T("hits X + off-targets", size=26, color=INHIB).move_to([2.35, 1.15, 0])
        pocket_hl = RoundedRectangle(corner_radius=0.06, width=0.62, height=0.38,
                                     stroke_color=ANALOG, stroke_width=4.5, fill_opacity=0)
        pocket_hl.move_to(x_mob.get_center() + x_mob.pocket_mid)
        self.play(
            FadeIn(off_lbl, run_time=0.45),
            FadeIn(pocket_hl, run_time=0.45),
            x_mob.body.animate.set_stroke(INHIB, width=3.5).set_fill(INHIB, opacity=0.22),
            run_time=0.5,
        )
        for idx, km in enumerate(others[:10]):
            self.play(
                pocket_hl.animate.move_to(km.get_center() + km.pocket_mid),
                km.body.animate.set_stroke(INHIB, width=3.5).set_fill(INHIB, opacity=0.22),
                Indicate(wedges[idx + 1], color=INHIB, scale_factor=1.28),
                run_time=0.48,
            )
        self.play(
            pocket_hl.animate.move_to(x_mob.get_center() + x_mob.pocket_mid),
            Indicate(wedges[0], color=INHIB, scale_factor=1.28),
            FadeOut(pocket_hl, run_time=0.45),
            run_time=0.55,
        )

        # Beat 3: Published panel surveys (computed proportion bars from lesson numbers)
        self.at("Large panel surveys")
        survey_title = T("Published panel surveys", size=26, color=TEXT, weight=BOLD).move_to([3.25, -0.78, 0])
        scale_lbl = T("kinases screened per survey", size=22, color=ANALOG).move_to([3.25, -1.14, 0])
        bar_w = 3.8
        bar_left_x = 3.25 - bar_w / 2
        f1_track = ValueTracker(0.0)
        f2_track = ValueTracker(0.0)

        lbl_2007 = T("2007: 65 inhibitors vs 70–80 kinases", size=22, color=TEXT).move_to([3.25, -1.56, 0])
        bar_base1 = Line([bar_left_x, -1.78, 0], [bar_left_x, -2.06, 0], color=SLATE, stroke_width=2.5)
        bar1 = always_redraw(lambda: RoundedRectangle(
            corner_radius=0.05, width=max(0.08, bar_w * (75.0 / 317.0) * f1_track.get_value()), height=0.24,
            stroke_width=0, fill_color=ANALOG, fill_opacity=0.88,
        ).align_to([bar_left_x, 0, 0], LEFT).set_y(-1.92))

        lbl_2008 = T("2008: 38 inhibitors vs 317 kinases", size=22, color=TEXT).move_to([3.25, -2.38, 0])
        bar_base2 = Line([bar_left_x, -2.60, 0], [bar_left_x, -2.88, 0], color=SLATE, stroke_width=2.5)
        bar2 = always_redraw(lambda: RoundedRectangle(
            corner_radius=0.05, width=max(0.08, bar_w * f2_track.get_value()), height=0.24,
            stroke_width=0, fill_color=ANALOG, fill_opacity=0.88,
        ).align_to([bar_left_x, 0, 0], LEFT).set_y(-2.74))

        self.play(FadeIn(survey_title), FadeIn(scale_lbl), FadeIn(bar_base1), FadeIn(bar_base2), FadeIn(lbl_2007), FadeIn(lbl_2008), run_time=0.7)
        self.add(bar1, bar2)
        self.play(
            f1_track.animate.set_value(1.0), f2_track.animate.set_value(1.0),
            *[km.body.animate.set_fill(INHIB, opacity=0.35) for km in others[:10]],
            run_time=2.8,
        )

        self.at("hit several kinases")
        dots = VGroup(*[
            Dot(km.get_center() + km.pocket_top + RIGHT * 0.38, radius=0.10, color=INHIB)
            for km in others[:10]
        ])
        self.play(LaggedStart(*[FadeIn(d, scale=1.4) for d in dots], lag_ratio=0.22), run_time=3.0)
        self.finish()


class S06AsymmetryRescue(SpokenScene):
    def construct(self):
        tag = scope_tag("schematic")
        head = T("An unselective inhibitor is one-sided", size=32, color=TEXT, weight=BOLD).move_to([0.0, HEAD_Y, 0])
        grid, x_mob, others = build_kinase_panel(origin=(-3.1, -0.1, 0), x_idx=(1, 2))
        resp_t = ValueTracker(1.0)
        meter = make_response_meter(resp_t, center=[5.15, 0.1, 0], w=0.95, h=3.4)

        self.add(tag, head, grid, meter)
        self.play(Indicate(x_mob, color=TARGET, scale_factor=1.08), run_time=2.4)

        plugged_targets = [x_mob] + others[:10]
        wedges = VGroup(*[
            make_wedge(color=INHIB).move_to(km.get_center() + km.pocket_mid + UP * 0.08)
            for km in plugged_targets
        ])

        # Case 1: Response survives -> X ruled out
        self.at("If X and many other")
        head_c1 = T("Case 1: X + off-targets blocked", size=32, color=TEXT, weight=BOLD).move_to([0.0, HEAD_Y, 0])
        self.play(swap(head, head_c1, run_time=0.5))
        self.play(
            FadeIn(wedges, shift=DOWN * 0.15, run_time=0.6),
            *[km.body.animate.set_fill(opacity=0.08).set_stroke(opacity=0.45) for km in plugged_targets],
            x_mob.label.animate.set_opacity(0.45),
            run_time=1.4,
        )
        head = head_c1

        self.at("yet the response survives")
        surv_ring = SurroundingRectangle(meter[0], color=PHOS, buff=0.08, stroke_width=4)
        self.play(Create(surv_ring), run_time=1.2)

        self.at("X is ruled out")
        b1 = boxed_label("X not needed\n(ruled out)", color=PHOS, size=26, box=(3.0, 1.2), fill_opacity=0.18)
        b1.move_to([2.25, 0.1, 0])
        self.play(FadeIn(b1), run_time=0.7)

        # Case 2: Clear previous answer, drop response -> ambiguous
        self.at("If the response stops")
        head_c2 = T("Case 2: response stops", size=32, color=INHIB, weight=BOLD).move_to([0.0, HEAD_Y, 0])
        self.play(
            FadeOut(b1, run_time=0.4), FadeOut(surv_ring, run_time=0.4),
            swap(head, head_c2, run_time=0.5),
        )
        self.play(resp_t.animate.set_value(0.0), run_time=1.6)
        head = head_c2

        self.at("could be responsible")
        q_marks = VGroup()
        for km in [x_mob, others[0], others[3], others[7]]:
            if km is x_mob:
                qm = T("?", size=24, color=GOLD, weight=BOLD).move_to(km.get_center() + [0.34, -0.24, 0])
            else:
                qm = T("?", size=24, color=INHIB, weight=BOLD).move_to(km.get_center() + [0.0, -0.24, 0])
            q_marks.add(qm)
        b2 = boxed_label("Ambiguous:\nX or off-target?", color=INHIB, size=26, box=(3.0, 1.2), fill_opacity=0.18)
        b2.move_to([2.25, 0.1, 0])
        self.play(FadeIn(q_marks), FadeIn(b2), run_time=0.9)

        # Case 3: Clear Case 2, swap X to drug-resistant X
        self.at("Express a drug")
        head_c3 = T("Case 3: drug-resistant mutant of X", size=32, color=TARGET, weight=BOLD).move_to([0.0, HEAD_Y, 0])
        res_x = make_small_kinase("X*", color=TARGET, w=1.35, h=0.98, resistant=True, fill_opacity=0.32).move_to(x_mob)
        self.play(
            FadeOut(b2, run_time=0.4), FadeOut(q_marks, run_time=0.4), FadeOut(wedges, run_time=0.4),
            *[km.body.animate.set_fill(opacity=0.18).set_stroke(opacity=1.0) for km in others[:10]],
            swap(head, head_c3, run_time=0.5),
            swap(x_mob, res_x, run_time=0.6),
        )
        head = head_c3
        x_mob = res_x

        self.at("If the response returns")
        slate_wedges = VGroup(*[
            make_wedge(color=INHIB).move_to(km.get_center() + km.pocket_top + UP * 0.14)
            for km in others[:10]
        ])
        x_wedge = make_wedge(color=INHIB).move_to(x_mob.get_center() + x_mob.pocket_top + UP * 0.14)
        self.add(slate_wedges, x_wedge)
        self.play(
            *[w.animate.move_to(km.get_center() + km.pocket_mid + UP * 0.08) for w, km in zip(slate_wedges, others[:10])],
            *[km.body.animate.set_fill(opacity=0.08).set_stroke(opacity=0.45) for km in others[:10]],
            x_wedge.animate.move_to(x_mob.get_center() + x_mob.pocket_top + UP * 0.12),
            run_time=1.1,
        )
        self.play(
            x_wedge.animate.shift(UP * 0.7 + LEFT * 0.4).set_opacity(0.0),
            resp_t.animate.set_value(1.0),
            run_time=1.8,
        )
        self.remove(x_wedge)

        self.at("the drug acted through")
        b3 = boxed_label("Drug acted through X\n(direct link not shown)", color=TARGET, size=24, box=(3.2, 1.25), fill_opacity=0.20)
        b3.move_to([2.25, 0.1, 0])
        self.play(FadeIn(b3, run_time=0.6), run_time=1.0)
        self.finish()


class S07NecSuffPredict(SpokenScene):
    def construct(self):
        tag = scope_tag("schematic").move_to([5.65, 3.35, 0])
        head = T("Necessary vs sufficient", size=34, color=TEXT, weight=BOLD).move_to([0.0, HEAD_Y, 0])

        hormone = boxed_label("Hormone: ON", color=HORMONE, size=28, box=(2.7, 1.15), fill_opacity=0.22).move_to([-4.6, 0.25, 0])
        kin_x = boxed_label("Kinase X", color=TARGET, size=28, box=(3.4, 1.35), fill_opacity=0.24).move_to([0.0, 0.25, 0])
        resp_t = ValueTracker(1.0)
        meter = make_response_meter(resp_t, center=[4.6, 0.25, 0], w=1.0, h=3.1)

        a1 = Arrow(hormone.get_right() + RIGHT * 0.12, kin_x.get_left() + LEFT * 0.12,
                   buff=0, color=HORMONE, stroke_width=4.5, max_tip_length_to_length_ratio=0.14)
        a2 = Arrow(kin_x.get_right() + RIGHT * 0.12, meter[0].get_left() + LEFT * 0.12,
                   buff=0, color=TARGET, stroke_width=4.5, max_tip_length_to_length_ratio=0.14)

        # Start visible immediately (prevents dark opening frame)
        self.add(tag, head, hormone, kin_x, meter, a1, a2)
        sig0 = Dot(a1.get_start(), radius=0.11, color=HORMONE)
        self.add(sig0)
        self.play(sig0.animate.move_to(a1.get_end()), run_time=1.3, rate_func=linear)
        sig0.set_color(TARGET).move_to(a2.get_start())
        self.play(sig0.animate.move_to(a2.get_end()), run_time=1.3, rate_func=linear)
        self.play(FadeOut(sig0, run_time=0.25), run_time=0.3)

        self.at("necessary and sufficient")
        # Keep nec_chip & suff_chip strictly separate and clear of "cell response"
        nec_chip = boxed_label("Necessary: remove -> stops", color=INHIB, size=24, box=(3.9, 0.72), fill_opacity=0.16).move_to([-4.05, 2.35, 0])
        suff_chip = boxed_label("Sufficient: on -> occurs", color=PHOS, size=24, box=(3.9, 0.72), fill_opacity=0.16).move_to([0.95, 2.35, 0])
        self.play(FadeIn(nec_chip), FadeIn(suff_chip), run_time=1.0)

        # Demonstrate Necessary: remove X -> response stops
        self.at("A step is necessary")
        x_cross = make_cross(kin_x, color=INHIB, scale=0.82, stroke=6)
        self.play(
            nec_chip.box.animate.set_stroke(INHIB, width=4),
            suff_chip.animate.set_opacity(0.35),
            kin_x.animate.set_opacity(0.30),
            Create(x_cross),
            a2.animate.set_opacity(0.20),
            resp_t.animate.set_value(0.0),
            run_time=3.2,
        )

        # Demonstrate Sufficient: Hormone OFF, turn X on alone -> response occurs
        self.at("It is sufficient")
        self.play(FadeOut(x_cross, run_time=0.35), run_time=0.4)
        no_horm = boxed_label("No hormone", color=SLATE, size=28, box=(2.7, 1.15), fill_opacity=0.14).move_to([-4.6, 0.25, 0])
        active_x = boxed_label("Always-active X", color=TARGET, size=28, box=(3.4, 1.35), fill_opacity=0.28).move_to([0.0, 0.25, 0])
        a1_off = DashedLine(no_horm.get_right() + RIGHT * 0.12, active_x.get_left() + LEFT * 0.12,
                            color=SLATE, stroke_width=3, dash_length=0.14).set_opacity(0.45)
        self.play(
            nec_chip.animate.set_opacity(0.35),
            suff_chip.animate.set_opacity(1.0),
            suff_chip.box.animate.set_stroke(PHOS, width=4),
            swap(hormone, no_horm, run_time=0.6),
            swap(a1, a1_off, run_time=0.6),
            swap(kin_x, active_x, run_time=0.6),
        )
        self.play(a2.animate.set_opacity(1.0), resp_t.animate.set_value(1.0), run_time=2.2)
        hormone, a1, kin_x = no_horm, a1_off, active_x

        # Settle into exact PredictPause backdrop + signal packet traveling X -> meter
        self.at("Suppose an always")
        sig = Dot(a2.get_start(), radius=0.18, color=TARGET)
        self.play(FadeOut(head, run_time=0.4), FadeOut(nec_chip, run_time=0.4), FadeOut(suff_chip, run_time=0.4), FadeIn(sig, run_time=0.4))
        for _ in range(3):
            sig.move_to(a2.get_start())
            self.play(
                sig.animate.move_to(a2.get_end()),
                kin_x.box.animate.set_fill(TARGET, opacity=0.42),
                run_time=0.9, rate_func=linear,
            )
            self.play(kin_x.box.animate.set_fill(TARGET, opacity=0.28), run_time=0.6)

        self.at("Does that prove")
        q = question_card("Always-active X triggers response without hormone. Is X necessary when hormone arrives?",
                          y=-2.95, max_w=10.2)
        self.play(FadeIn(q.question, run_time=0.5))
        # Keep signal packet pulsing into cell response up to scene end so frame isn't frozen
        for _ in range(2):
            sig.move_to(a2.get_start())
            self.play(
                sig.animate.move_to(a2.get_end()),
                kin_x.box.animate.set_fill(TARGET, opacity=0.42),
                run_time=0.8, rate_func=linear,
            )
            self.play(kin_x.box.animate.set_fill(TARGET, opacity=0.28), run_time=0.5)
        self.play(FadeOut(sig, run_time=0.2))
        self.finish()


class S08Pause(PredictPause):
    SECONDS = 4.5
    QUESTION = "Always-active X triggers response without hormone. Is X necessary when hormone arrives?"
    CARD = {"y": -2.95, "max_w": 10.2}

    def backdrop(self):
        grp, *_ = build_predict_world()
        return grp


class S09RevealClose(SpokenScene):
    def construct(self):
        grp, hormone, kin_x, meter, resp_t, a1, a2 = build_predict_world()
        q = question_card("Always-active X triggers response without hormone. Is X necessary when hormone arrives?",
                          y=-2.95, max_w=10.2)
        self.add(grp, q)

        ans_no = T("No.", size=36, color=INHIB, weight=BOLD).move_to([0.0, -2.95, 0])
        self.play(swap(q.question, ans_no, run_time=0.5), run_time=0.5)

        self.at("when hormone arrives")
        horm_on = boxed_label("Hormone: ON", color=HORMONE, size=28, box=(2.7, 1.15), fill_opacity=0.24).move_to([-4.6, 0.25, 0])
        plain_x = boxed_label("Kinase X", color=TARGET, size=28, box=(3.4, 1.35), fill_opacity=0.24).move_to([0.0, 0.25, 0]).set_opacity(0.30)
        a1_dim = Arrow(horm_on.get_right() + RIGHT * 0.12, plain_x.get_left() + LEFT * 0.12,
                       buff=0, color=SLATE, stroke_width=4, max_tip_length_to_length_ratio=0.14).set_opacity(0.25)
        self.play(
            swap(hormone, horm_on, run_time=0.5),
            swap(kin_x, plain_x, run_time=0.5),
            swap(a1, a1_dim, run_time=0.5),
            a2.animate.set_opacity(0.20),
            run_time=0.6,
        )
        x_cross = make_cross(plain_x, color=INHIB, scale=0.82, stroke=6)
        self.play(Create(x_cross), run_time=0.5)
        hormone, kin_x, a1 = horm_on, plain_x, a1_dim

        self.at("a parallel pathway")
        par_node = boxed_label("Parallel pathway", color=HORMONE, size=26, box=(3.4, 0.95), fill_opacity=0.22).move_to([0.0, 2.25, 0])
        p_arr1 = Arrow(hormone.get_top() + UP * 0.12, par_node.get_left() + LEFT * 0.12,
                       buff=0, color=HORMONE, stroke_width=4.5, max_tip_length_to_length_ratio=0.14)
        p_arr2 = Arrow(par_node.get_right() + RIGHT * 0.12, meter[0].get_left() + [-0.12, 1.15, 0],
                       buff=0, color=HORMONE, stroke_width=4.5, max_tip_length_to_length_ratio=0.14)
        self.play(GrowArrow(p_arr1), FadeIn(par_node), GrowArrow(p_arr2), run_time=1.5)

        sig = Dot(p_arr1.get_start(), radius=0.18, color=HORMONE)
        self.add(sig)
        for _ in range(2):
            sig.move_to(p_arr1.get_start())
            self.play(sig.animate.move_to(par_node.get_left()), par_node.box.animate.set_fill(HORMONE, opacity=0.40), run_time=0.9, rate_func=linear)
            sig.move_to(p_arr2.get_start())
            self.play(sig.animate.move_to(p_arr2.get_end()), par_node.box.animate.set_fill(HORMONE, opacity=0.22), run_time=1.0, rate_func=linear)
        self.play(FadeOut(sig, run_time=0.25), run_time=0.3)

        self.at("shows it is sufficient")
        rule_cap = T("Sufficient is not necessary.", size=32, color=TARGET, weight=BOLD).move_to([0.0, -2.95, 0])
        self.play(swap(ans_no, rule_cap, run_time=0.5), run_time=1.2)

        self.at("Every method fails")
        all_pathway = VGroup(hormone, kin_x, meter, a1, a2, x_cross, par_node, p_arr1, p_arr2, rule_cap)
        tag = grp[5]
        m1 = boxed_label("Chemical inhibitor", color=INHIB, size=26, box=(4.2, 1.05), fill_opacity=0.22).move_to([-3.6, 1.55, 0])
        m2 = boxed_label("Genetic knockout / mutant", color=GENETIC, size=26, box=(4.2, 1.05), fill_opacity=0.22).move_to([-3.6, -1.25, 0])
        claim_pending = boxed_label("Causal claim: ?", color=SLATE, size=28, box=(3.8, 1.45), fill_opacity=0.14).move_to([3.5, 0.15, 0])
        self.play(
            FadeOut(all_pathway, run_time=0.5),
            tag.animate.move_to(scope_tag("schematic").get_center()),
            FadeIn(m1), FadeIn(m2), FadeIn(claim_pending),
            run_time=1.1,
        )

        self.at("Inhibitors hit")
        blind1 = T("blind spot: off-targets", size=24, color=INHIB).next_to(m1, DOWN, buff=0.20)
        off_node = boxed_label("off-target", color=INHIB, size=22, box=(1.8, 0.65), fill_opacity=0.18).move_to([0.0, 1.55, 0])
        off_arr = Arrow(m1.get_right() + RIGHT * 0.12, off_node.get_left() + LEFT * 0.12, buff=0, color=INHIB, stroke_width=3.5)
        self.play(FadeIn(blind1), m1.box.animate.set_stroke(INHIB, width=3.5), FadeIn(off_node), GrowArrow(off_arr), run_time=0.8)

        self.at("knockouts disrupt")
        blind2 = T("blind spot: whole network", size=24, color=INHIB).next_to(m2, DOWN, buff=0.20)
        net_nodes = VGroup(
            Dot([-0.2, -0.9, 0], radius=0.16, color=GENETIC),
            Dot([0.5, -1.3, 0], radius=0.16, color=GENETIC),
            Dot([-0.2, -1.7, 0], radius=0.16, color=GENETIC),
        )
        net_edges = VGroup(
            Line(net_nodes[0], net_nodes[1], color=INHIB, stroke_width=3),
            Line(net_nodes[1], net_nodes[2], color=INHIB, stroke_width=3),
            Line(net_nodes[0], net_nodes[2], color=INHIB, stroke_width=3),
        )
        self.play(FadeIn(blind2), m2.box.animate.set_stroke(INHIB, width=3.5), FadeIn(net_nodes), Create(net_edges), run_time=0.8)

        self.at("Causal claims earn belief")
        m1_rescue = boxed_label("Drug-resistant rescue", color=TARGET, size=26, box=(4.2, 1.05), fill_opacity=0.22).move_to(m1)
        claim = boxed_label("Causal claim:\nX drives response", color=PHOS, size=28, box=(3.8, 1.55), fill_opacity=0.24).move_to([3.5, 0.15, 0])
        chk1 = T("✓", size=34, color=PHOS, weight=BOLD).next_to(m1_rescue, LEFT, buff=0.22)
        chk2 = T("✓", size=34, color=PHOS, weight=BOLD).next_to(m2, LEFT, buff=0.22)
        arr_c1 = Arrow(m1_rescue.get_right() + RIGHT * 0.14, claim.get_left() + [-0.14, 0.35, 0],
                       buff=0, color=PHOS, stroke_width=5, max_tip_length_to_length_ratio=0.14)
        arr_c2 = Arrow(m2.get_right() + RIGHT * 0.14, claim.get_left() + [-0.14, -0.35, 0],
                       buff=0, color=PHOS, stroke_width=5, max_tip_length_to_length_ratio=0.14)
        self.play(
            FadeOut(blind1, run_time=0.3), FadeOut(blind2, run_time=0.3),
            FadeOut(off_node, run_time=0.3), FadeOut(off_arr, run_time=0.3),
            FadeOut(net_nodes, run_time=0.3), FadeOut(net_edges, run_time=0.3),
            swap(m1, m1_rescue, run_time=0.5),
            m2.box.animate.set_stroke(GENETIC, width=3),
            swap(claim_pending, claim, run_time=0.5),
        )
        self.play(FadeIn(chk1), FadeIn(chk2), GrowArrow(arr_c1), GrowArrow(arr_c2), run_time=1.3)
        self.finish()


class S10End(EndCard):
    LINE = "Causal claims earn belief when two methods that fail differently agree."
