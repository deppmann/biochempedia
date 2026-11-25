"""Inside the Fork — DNA Replication (STEMhop Chapter 2).

COLOUR MAP (identical to Chapter 1):
    GREY   (#8B93A1)  old DNA template strands, backbones, arrowheads, and joining enzyme clip
    GOLD   (#D4A843)  new DNA strands, backbones, arrowheads, highlight/possible panel
    RED    (#FC6255)  base A (adenine) and mismatch/clash X markers
    BLUE   (#58C4DD)  base T (thymine)
    GREEN  (#83C167)  base C (cytosine) and matching-check step
    PURPLE (#B388EB)  base G (guanine)
    ORANGE (#F59E42)  DNA polymerase enzyme
    TEAL   (#3FB8C0)  repair enzyme, accurate panel, and directional cues
    TEXT   (#E8EAF0)  primary labels and covalent-bond flashes

ONE PICTURE OF THE WORLD:
    A horizontal double-stranded DNA molecule (17 base pairs, each base showing its letter in its
    key colour, old strands GREY with opposite arrowheads) opens from left to right into a Y-shaped
    replication fork. New GOLD strands grow behind the fork only on unwound template, followed by
    zoomed-in views of polymerase's active site and a three-step accuracy tally.

WHAT CHANGES PER SCENE (and what it is computed from):
    s01_link:       Two finished GREY+GOLD daughter molecules rewind letter-by-letter into one GREY
                    parent ladder, then only the left end unzips into a Y fork (open fraction f(x, fork_x)).
    s02_fork:       The Y fork slides steadily left-to-right (fork_x tracker), opening paired rungs as
                    it passes; opposite arrowheads on both GREY templates highlight.
    s03_polymerase: Fork advances steadily while DNA polymerase on the upper template inspects free bases,
                    deflects a mismatched base, pairs G opposite C, and seals a covalent bond.
    s04_rule:       Zoomed-in view of the new GOLD strand growing arrowhead-first (rightward) while a
                    nucleotide trying the tail end is rejected; opposite template/new arrows contrast.
    s05_upper:      Zoomed-out fork advances continuously; polymerase follows behind the fork, adding
                    upper-strand nucleotides in one unbroken run (piece counter stays at 1).
    s06_predict:    Fork freezes; lower GREY template and a ghost leftward GOLD outline highlight with
                    a question mark and bottom question card asking how the lower strand is copied.
    s07_pause:      Silent 5 s PredictPause holding the frozen fork, ghost outline, and countdown ring.
    s08_reveal:     Fork unfreezes in stages; lower GOLD strand builds in 3 short leftward pieces behind
                    the moving fork (counter 1 -> 2 -> 3), then a joining enzyme clip seals them into 1.
    s09_check:      Close-up inside polymerase: mismatched RED A clashes with GREEN C and is pushed out;
                    matching PURPLE G clicks in; right-hand accuracy ledger reveals 1. matching check.
    s10_proofread:  RED A slips in opposite C; polymerase backs up one base, removes A, inserts G
                    (2. proofreading); behind it, a repair enzyme fixes a leftover T-G slip (3. repair).
    s11_tally:      The three checks stack into one three-stage horizontal accuracy bar filtering errors
                    down to the textbook estimate (~1 uncorrected mistake per 1,000,000,000 bases).
    s12_two_jobs:   Top moving fork runs above TwoPanel ("possible" with A-T/C-G pairing vs "accurate"
                    with the 3-step tally); panels draw together cleanly under the moving fork.
"""

from bp_parts import *

# ---------------------------------------------------------------------------
# Concept colour palette
# ---------------------------------------------------------------------------
PURPLE = "#B388EB"
ORANGE = "#F59E42"

BASE_COLORS = {
    "A": RED,
    "T": BLUE,
    "C": GREEN,
    "G": PURPLE,
}
COMPLEMENT = {"A": "T", "T": "A", "C": "G", "G": "C"}

# 17-base DNA sequence used consistently across all full-fork scenes
N_BASES = 17
STEP_X = 0.68
XS = [-5.44 + i * STEP_X for i in range(N_BASES)]
SEQ_UPPER = list("ATCGATGCGATCATGCA")
SEQ_LOWER = [COMPLEMENT[b] for b in SEQ_UPPER]

# Vertical geometry for full-fork view (all coordinates maintain >= 0.14 clearance around base boxes)
BASE_W = 0.48
BASE_H = 0.38
Y_PAIRED_BB = 0.64
Y_PAIRED_BASE = 0.31
Y_OPEN_BB = 2.04
Y_OPEN_BASE = 1.67
Y_NEW_BASE = 1.09
Y_NEW_BB = 0.76
FORK_TRANS = 1.30


def _smoothstep(u):
    u = float(np.clip(u, 0.0, 1.0))
    return u * u * (3.0 - 2.0 * u)


def _open_frac(x, fork_x, trans=FORK_TRANS):
    """Smooth 0..1 opening fraction: 0 when still paired (x >= fork_x), 1 when open."""
    if x >= fork_x:
        return 0.0
    if x <= fork_x - trans:
        return 1.0
    return _smoothstep((fork_x - x) / trans)


def _bb_y_at(x, fork_x, base_h=BASE_H, y_p_bb=Y_PAIRED_BB, y_p_base=Y_PAIRED_BASE, y_o_bb=Y_OPEN_BB, y_o_base=Y_OPEN_BASE):
    """Backbone y-offset above/below axis with an outward bow in the ramp so diagonal never hits a base corner."""
    f = _open_frac(x, fork_x)
    y_base = y_p_base + f * (y_o_base - y_p_base)
    y_bb = y_p_bb + f * (y_o_bb - y_p_bb)
    bow = 0.22 * np.sin(np.pi * f)
    return max(y_bb, y_base + base_h / 2 + 0.14) + bow, y_base, f


def base_block(letter, w=BASE_W, h=BASE_H, font_size=24, stroke_width=2.8, fill_opacity=0.20):
    """A rectangular nucleotide base showing its LETTER in its key colour."""
    col = BASE_COLORS[letter]
    box = RoundedRectangle(
        width=w,
        height=h,
        corner_radius=0.06,
        stroke_color=col,
        stroke_width=stroke_width,
        fill_color=col,
        fill_opacity=fill_opacity,
    )
    txt = T(letter, size=font_size, color=col, weight=BOLD).move_to(box)
    g = VGroup(box, txt)
    g.box = box
    g.txt = txt
    g.letter = letter
    return g


def color_key_bar(at=(3.1, 3.28, 0), font_size=24):
    """Compact colour-coded key: old GREY, new GOLD, and A/T/C/G in their key colours."""
    items = VGroup(
        T("old", size=font_size, color=GREY, weight=BOLD),
        T("new", size=font_size, color=GOLD, weight=BOLD),
        T("A", size=font_size, color=RED, weight=BOLD),
        T("T", size=font_size, color=BLUE, weight=BOLD),
        T("C", size=font_size, color=GREEN, weight=BOLD),
        T("G", size=font_size, color=PURPLE, weight=BOLD),
    ).arrange(RIGHT, buff=0.28)
    box = RoundedRectangle(
        corner_radius=0.12,
        width=items.width + 0.44,
        height=items.height + 0.24,
        stroke_color=GREY,
        stroke_width=2.0,
        fill_color=BG,
        fill_opacity=0.85,
    )
    items.move_to(box)
    return VGroup(box, items).move_to(at)


def strand_with_arrow(points, color=GREY, stroke_width=5.0, direction="right", tip_len=0.24):
    """A smooth/polygonal strand backbone with a clean arrowhead at its pointing end."""
    pts = [np.array(p, dtype=float) for p in points]
    line = VMobject(stroke_color=color, stroke_width=stroke_width, fill_opacity=0)
    line.set_points_as_corners(pts)
    if direction == "right":
        p_end = pts[-1]
        p_prev = pts[-2] if len(pts) >= 2 else p_end + LEFT * 0.5
    else:
        p_end = pts[0]
        p_prev = pts[1] if len(pts) >= 2 else p_end + RIGHT * 0.5
    d = p_end - p_prev
    norm = np.linalg.norm(d[:2])
    u = d / norm if norm > 1e-6 else (RIGHT if direction == "right" else LEFT)
    perp = np.array([-u[1], u[0], 0.0])
    tip = p_end + u * 0.04
    base_pt = p_end - u * tip_len
    head = Polygon(
        tip,
        base_pt + perp * (tip_len * 0.55),
        base_pt - perp * (tip_len * 0.55),
        stroke_color=color,
        stroke_width=2.0,
        fill_color=color,
        fill_opacity=1.0,
    )
    g = VGroup(line, head)
    g.line = line
    g.head = head
    return g


def polymerase_shape(center, width=0.62, height=1.54, color=ORANGE, label_pos="above"):
    """Rounded orange-outlined DNA polymerase shape whose side walls sit in the gaps between bases."""
    body = RoundedRectangle(
        corner_radius=0.22,
        width=width,
        height=height,
        stroke_color=color,
        stroke_width=3.5,
        fill_color=color,
        fill_opacity=0.12,
    ).move_to(center)
    lab = boxed_label("DNA polymerase", color=color, size=24, pad=0.13, fill_opacity=0.16)
    if label_pos == "above":
        lab.next_to(body, UP, buff=0.16)
    elif label_pos == "below":
        lab.next_to(body, DOWN, buff=0.16)
    else:
        lab.next_to(body, RIGHT, buff=0.18)
    g = VGroup(body, lab)
    g.body = body
    g.label = lab
    return g


def _sample_backbone_pts(fork_x, y_offset=0.0, base_h=BASE_H, y_p_bb=Y_PAIRED_BB, y_p_base=Y_PAIRED_BASE, y_o_bb=Y_OPEN_BB, y_o_base=Y_OPEN_BASE):
    """Dense backbone curve points so the smooth ramp never clips adjacent base corners."""
    x_samples = np.linspace(XS[0] - 0.50, XS[-1] + 0.50, 65)
    u_pts, l_pts = [], []
    for x in x_samples:
        y_bb, _, _ = _bb_y_at(x, fork_x, base_h, y_p_bb, y_p_base, y_o_bb, y_o_base)
        u_pts.append([x, y_offset + y_bb, 0.0])
        l_pts.append([x, y_offset - y_bb, 0.0])
    return u_pts, l_pts


def build_fork_template(fork_x, y_offset=0.0, compact=False):
    """Build the two old GREY templates and H-bonds for a given fork_x."""
    if compact:
        bw, bh, fs = 0.42, 0.34, 22
        ypb, ypa, yob, yoa = 0.48, 0.22, 1.18, 0.87
        hb_half = 0.03
    else:
        bw, bh, fs = BASE_W, BASE_H, 24
        ypb, ypa, yob, yoa = Y_PAIRED_BB, Y_PAIRED_BASE, Y_OPEN_BB, Y_OPEN_BASE
        hb_half = 0.08

    u_bases = VGroup()
    l_bases = VGroup()
    hbonds = VGroup()

    for i, x in enumerate(XS):
        _, y_base, f = _bb_y_at(x, fork_x, bh, ypb, ypa, yob, yoa)
        ub = base_block(SEQ_UPPER[i], w=bw, h=bh, font_size=fs)
        ub.move_to([x, y_offset + y_base, 0.0])
        lb = base_block(SEQ_LOWER[i], w=bw, h=bh, font_size=fs)
        lb.move_to([x, y_offset - y_base, 0.0])
        u_bases.add(ub)
        l_bases.add(lb)

        hb = DashedLine(
            [x, y_offset - hb_half, 0.0],
            [x, y_offset + hb_half, 0.0],
            color=GREY,
            stroke_width=2.0,
            dash_length=0.04,
        )
        hb.set_opacity(1.0 - f if f < 0.85 else 0.0)
        hbonds.add(hb)

    u_pts, l_pts = _sample_backbone_pts(fork_x, y_offset, bh, ypb, ypa, yob, yoa)
    u_bb = strand_with_arrow(u_pts, color=GREY, stroke_width=4.8, direction="left")
    l_bb = strand_with_arrow(l_pts, color=GREY, stroke_width=4.8, direction="right")

    g = VGroup(hbonds, u_bb, l_bb, u_bases, l_bases)
    g.hbonds = hbonds
    g.u_bb = u_bb
    g.l_bb = l_bb
    g.u_bases = u_bases
    g.l_bases = l_bases
    g._cfg = (y_offset, bh, ypb, ypa, yob, yoa)
    return g


def update_fork_template(tpl, fork_x):
    """Update an existing ForkTemplate in place for a new fork_x (no Text rebuild)."""
    y_offset, bh, ypb, ypa, yob, yoa = tpl._cfg
    for i, x in enumerate(XS):
        _, y_base, f = _bb_y_at(x, fork_x, bh, ypb, ypa, yob, yoa)
        tpl.u_bases[i].move_to([x, y_offset + y_base, 0.0])
        tpl.l_bases[i].move_to([x, y_offset - y_base, 0.0])
        tpl.hbonds[i].set_opacity(1.0 - f if f < 0.85 else 0.0)

    u_pts, l_pts = _sample_backbone_pts(fork_x, y_offset, bh, ypb, ypa, yob, yoa)
    tpl.u_bb.line.set_points_as_corners([np.array(p) for p in u_pts])
    tpl.l_bb.line.set_points_as_corners([np.array(p) for p in l_pts])
    tpl.u_bb.head.move_to(np.array(u_pts[0]) + RIGHT * 0.10)
    tpl.l_bb.head.move_to(np.array(l_pts[-1]) + LEFT * 0.10)


def build_new_segment(indices, is_upper=True, y_offset=0.0):
    """Build a contiguous GOLD new-strand segment over sorted `indices` on the open arm."""
    assert len(indices) >= 1
    idx_sorted = sorted(indices)
    bases = VGroup()
    yb = y_offset + (Y_NEW_BB if is_upper else -Y_NEW_BB)
    ybase = y_offset + (Y_NEW_BASE if is_upper else -Y_NEW_BASE)
    for i in idx_sorted:
        tmpl_letter = SEQ_UPPER[i] if is_upper else SEQ_LOWER[i]
        nb = base_block(COMPLEMENT[tmpl_letter])
        nb.move_to([XS[i], ybase, 0.0])
        bases.add(nb)
    x0 = XS[idx_sorted[0]] - 0.34
    x1 = XS[idx_sorted[-1]] + 0.34
    direction = "right" if is_upper else "left"
    bb = strand_with_arrow([[x0, yb, 0.0], [x1, yb, 0.0]], color=GOLD, stroke_width=5.0, direction=direction)
    g = VGroup(bb, bases)
    g.bb = bb
    g.bases = bases
    g.indices = idx_sorted
    return g


def fork_moves_marker(fork_x, y=-2.58):
    """Small TEAL arrow below the fork vertex reading 'fork moves'."""
    arr = Arrow([fork_x - 0.55, y, 0], [fork_x + 0.55, y, 0], color=TEAL, stroke_width=4, buff=0, max_tip_length_to_length_ratio=0.25)
    lab = T("fork moves", size=24, color=TEAL).next_to(arr, DOWN, buff=0.14)
    g = VGroup(arr, lab)
    g.arr = arr
    g.lab = lab
    return g


def x_mark(center, color=RED, size=0.20):
    """Crisp X mark for rejected nucleotides."""
    d1 = Line(np.array(center) + [-size, -size, 0], np.array(center) + [size, size, 0], color=color, stroke_width=5)
    d2 = Line(np.array(center) + [-size, size, 0], np.array(center) + [size, -size, 0], color=color, stroke_width=5)
    return VGroup(d1, d2)


def repair_wrench(center, color=TEAL):
    """Simple schematic wrench icon (no molecular structure)."""
    ring = Arc(radius=0.20, start_angle=0.5, angle=TAU - 1.0, arc_center=ORIGIN, color=color, stroke_width=5)
    handle = Line([-0.14, 0, 0], [-0.55, 0, 0], color=color, stroke_width=6)
    return VGroup(ring, handle).rotate(0.45).move_to(center)


def joining_clip(center, color=GREY):
    """Small grey clip shape representing the joining enzyme."""
    arc = Arc(radius=0.20, start_angle=PI * 0.15, angle=PI * 1.7, color=color, stroke_width=5)
    lug1 = Line(arc.get_start(), arc.get_start() + RIGHT * 0.12, color=color, stroke_width=5)
    lug2 = Line(arc.get_end(), arc.get_end() + RIGHT * 0.12, color=color, stroke_width=5)
    return VGroup(arc, lug1, lug2).move_to(center)


# ---------------------------------------------------------------------------
# S00: Title Card
# ---------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "DNA: Structure and Copying"
    TITLE = "Inside the Fork"


# ---------------------------------------------------------------------------
# S01: Link from Chapter 1 (two molecules -> rewind to 1 ladder -> Y fork)
# ---------------------------------------------------------------------------
class S01Link(SpokenScene):
    def construct(self):
        n_mol = 12
        xs_m = [-3.85 + i * 0.70 for i in range(n_mol)]

        def make_molecule(y_mid, is_top=True):
            old_bases = VGroup()
            new_bases = VGroup()
            for i, x in enumerate(xs_m):
                b_old = base_block(SEQ_UPPER[i] if is_top else SEQ_LOWER[i])
                b_new = base_block(SEQ_LOWER[i] if is_top else SEQ_UPPER[i])
                if is_top:
                    b_old.move_to([x, y_mid + 0.31, 0])
                    b_new.move_to([x, y_mid - 0.31, 0])
                else:
                    b_new.move_to([x, y_mid + 0.31, 0])
                    b_old.move_to([x, y_mid - 0.31, 0])
                old_bases.add(b_old)
                new_bases.add(b_new)
            xL, xR = xs_m[0] - 0.48, xs_m[-1] + 0.48
            if is_top:
                old_bb = strand_with_arrow([[xL, y_mid + 0.64, 0], [xR, y_mid + 0.64, 0]], GREY, direction="left")
                new_bb = strand_with_arrow([[xL, y_mid - 0.64, 0], [xR, y_mid - 0.64, 0]], GOLD, direction="right")
            else:
                new_bb = strand_with_arrow([[xL, y_mid + 0.64, 0], [xR, y_mid + 0.64, 0]], GOLD, direction="left")
                old_bb = strand_with_arrow([[xL, y_mid - 0.64, 0], [xR, y_mid - 0.64, 0]], GREY, direction="right")
            return old_bb, old_bases, new_bb, new_bases

        top_old_bb, top_old_b, top_new_bb, top_new_b = make_molecule(1.30, True)
        bot_old_bb, bot_old_b, bot_new_bb, bot_new_b = make_molecule(-1.30, False)
        key = color_key_bar(at=(3.1, 3.28, 0))
        top_tag = T("molecule 1", size=24, color=GREY).next_to(top_old_bb, UP, buff=0.14).align_to(top_old_bb, LEFT)
        bot_tag = T("molecule 2", size=24, color=GREY).next_to(bot_old_bb, DOWN, buff=0.14).align_to(bot_old_bb, LEFT)

        self.play(
            FadeIn(key),
            FadeIn(top_old_bb), FadeIn(top_old_b), FadeIn(top_new_bb), FadeIn(top_new_b),
            FadeIn(bot_old_bb), FadeIn(bot_old_b), FadeIn(bot_new_bb), FadeIn(bot_new_b),
            FadeIn(top_tag), FadeIn(bot_tag),
            run_time=0.9,
        )

        self.at("each old strand")
        self.play(
            Indicate(top_old_bb, color=TEXT, scale_factor=1.04),
            Indicate(bot_old_bb, color=TEXT, scale_factor=1.04),
            run_time=1.3,
        )
        self.play(
            Indicate(top_new_bb, color=GOLD, scale_factor=1.04),
            Indicate(bot_new_bb, color=GOLD, scale_factor=1.04),
            run_time=1.1,
        )

        self.at("how does a cell")
        self.play(
            FadeOut(top_tag), FadeOut(bot_tag),
            LaggedStart(*[FadeOut(m, shift=DOWN * 0.12) for m in reversed(top_new_b)], lag_ratio=0.06),
            LaggedStart(*[FadeOut(m, shift=UP * 0.12) for m in bot_new_b], lag_ratio=0.06),
            FadeOut(top_new_bb), FadeOut(bot_new_bb),
            run_time=1.4,
        )
        fork_t = ValueTracker(-6.8)
        tpl = build_fork_template(-6.8)
        self.play(
            ReplacementTransform(VGroup(top_old_bb, top_old_b), VGroup(tpl.u_bb, tpl.u_bases)),
            ReplacementTransform(VGroup(bot_old_bb, bot_old_b), VGroup(tpl.l_bb, tpl.l_bases)),
            FadeIn(tpl.hbonds),
            run_time=1.0,
        )
        self.remove(tpl)
        self.add(tpl)

        self.at("one letter at a time")
        for i in range(4):
            self.play(Indicate(tpl.u_bases[i], color=GOLD, scale_factor=1.18), run_time=0.45)

        self.at("does not open")
        tpl.add_updater(lambda m: update_fork_template(m, fork_t.get_value()))
        self.play(fork_t.animate.set_value(-2.5), run_time=2.2, rate_func=smooth)
        tpl.clear_updaters()
        self.finish()


# ---------------------------------------------------------------------------
# S02: Moving Y Fork & Opposite Arrowheads
# ---------------------------------------------------------------------------
class S02Fork(SpokenScene):
    def construct(self):
        fork_t = ValueTracker(-2.5)
        tpl = build_fork_template(-2.5)
        key = color_key_bar(at=(3.1, 3.28, 0))
        self.add(tpl, key)
        tpl.add_updater(lambda m: update_fork_template(m, fork_t.get_value()))

        # Begin moving the fork gently right away while narrator says "opens the DNA at a moving Y"
        self.play(fork_t.animate.set_value(-2.1), run_time=2.4, rate_func=linear)

        self.at("called the fork")
        fork_lab = boxed_label("fork", color=GOLD, size=28, pad=0.14).move_to([fork_t.get_value(), 2.85, 0])
        fork_ptr = Arrow([fork_t.get_value(), 2.46, 0], [fork_t.get_value(), 1.48, 0], color=GOLD, stroke_width=3.5, buff=0, max_tip_length_to_length_ratio=0.22)
        self.play(FadeIn(fork_lab), GrowArrow(fork_ptr), run_time=0.7)

        self.at("The fork moves along")
        fm = fork_moves_marker(fork_t.get_value(), y=-2.58)
        fm.add_updater(lambda m: m.set_x(fork_t.get_value()))
        fork_lab.add_updater(lambda m: m.set_x(fork_t.get_value()))
        fork_ptr.add_updater(lambda m: m.put_start_and_end_on([fork_t.get_value(), 2.46, 0], [fork_t.get_value(), 1.48, 0]))
        self.play(FadeIn(fm), run_time=0.5)
        self.play(fork_t.animate.set_value(-0.9), run_time=3.6, rate_func=linear)

        self.at("Both old strands")
        upper_dir = T("← upper template", size=26, color=GREY).move_to([-4.2, 2.68, 0])
        lower_dir = T("lower template →", size=26, color=GREY).move_to([3.9, -2.55, 0])
        self.play(FadeIn(upper_dir), FadeIn(lower_dir), run_time=0.7)

        self.at("point opposite ways")
        self.play(
            Indicate(tpl.u_bb.head, color=GOLD, scale_factor=1.45),
            Indicate(tpl.l_bb.head, color=GOLD, scale_factor=1.45),
            fork_t.animate.set_value(-0.7),
            run_time=1.3,
        )
        tpl.clear_updaters()
        fm.clear_updaters()
        fork_lab.clear_updaters()
        fork_ptr.clear_updaters()
        self.finish()


# ---------------------------------------------------------------------------
# S03: DNA Polymerase Picks Matching Nucleotide & Covalent Bond
# ---------------------------------------------------------------------------
class S03Polymerase(SpokenScene):
    def construct(self):
        fork_t = ValueTracker(-0.7)
        tpl = build_fork_template(-0.7)
        upper_seg = build_new_segment([0, 1], is_upper=True)
        poly = polymerase_shape([XS[2], 1.39, 0], width=0.62, height=1.52, color=ORANGE, label_pos="above")
        fm = fork_moves_marker(fork_t.get_value(), y=-2.58)
        fm.add_updater(lambda m: m.set_x(fork_t.get_value()))
        tpl.add_updater(lambda m: update_fork_template(m, fork_t.get_value()))

        free_t = base_block("T").move_to([-5.0, -0.02, 0])
        free_g = base_block("G").move_to([-3.3, -0.02, 0])
        free_a = base_block("A").move_to([-2.4, -0.02, 0])
        free_c = base_block("C").move_to([-1.5, -0.02, 0])

        self.add(tpl, upper_seg, fm)

        self.at("The enzyme that builds")
        self.play(
            FadeIn(poly),
            FadeIn(VGroup(free_t, free_g, free_a, free_c)),
            fork_t.animate.set_value(-0.45),
            run_time=1.5,
        )
        self.play(
            Indicate(poly.body, color=GOLD, scale_factor=1.06),
            fork_t.animate.set_value(-0.15),
            run_time=2.5,
            rate_func=linear,
        )

        self.at("At each base")
        self.play(
            Indicate(tpl.u_bases[2], color=TEXT, scale_factor=1.20),
            fork_t.animate.set_value(0.05),
            run_time=1.0,
        )

        self.at("pairs with it")
        target_g_pos = np.array([XS[2], Y_NEW_BASE, 0.0])
        self.play(
            free_g.animate.move_to(target_g_pos),
            fork_t.animate.set_value(0.25),
            run_time=1.5,
            rate_func=smooth,
        )

        self.at("A wrong one")
        wrong_start = free_a.get_center().copy()
        test_pos = np.array([XS[3], 0.35, 0.0])
        xm = x_mark([XS[3], 0.80, 0.0], color=RED, size=0.17)
        self.play(free_a.animate.move_to(test_pos), fork_t.animate.set_value(0.40), run_time=0.75)
        self.play(FadeIn(xm), run_time=0.25)
        self.play(FadeOut(xm), free_a.animate.move_to(wrong_start), fork_t.animate.set_value(0.55), run_time=1.0)

        self.at("Then it joins")
        new_seg = build_new_segment([0, 1, 2], is_upper=True)
        self.play(
            ReplacementTransform(upper_seg.bb, new_seg.bb),
            fork_t.animate.set_value(0.72),
            run_time=1.3,
        )

        self.at("covalent bond")
        bond_pt = np.array([(XS[1] + XS[2]) / 2, Y_NEW_BB, 0.0])
        flash = Circle(radius=0.20, color=TEXT, stroke_width=4, fill_color=TEXT, fill_opacity=0.6).move_to(bond_pt)
        bond_lab = boxed_label("covalent bond", color=TEXT, size=24, pad=0.12).move_to([-4.2, 0.02, 0])
        self.play(
            FadeOut(free_t), FadeOut(free_a), FadeOut(free_c),
            fork_t.animate.set_value(0.77),
            run_time=0.3,
        )
        self.play(
            FadeIn(flash),
            FadeIn(bond_lab),
            fork_t.animate.set_value(0.92),
            run_time=0.8,
        )
        self.play(FadeOut(flash), fork_t.animate.set_value(1.05), run_time=0.9)
        tpl.clear_updaters()
        fm.clear_updaters()
        self.finish()


# ---------------------------------------------------------------------------
# S04: Polymerase's Strict Habit (adds only at arrowhead)
# ---------------------------------------------------------------------------
class S04Rule(SpokenScene):
    def construct(self):
        banner = boxed_label("Rule: adds only at the arrowhead", color=GOLD, size=28, pad=0.16).move_to([0, 2.95, 0])
        z_xs = [-3.6 + i * 1.15 for i in range(7)]
        z_seq = list("ATGCGAT")

        tmpl_bases = VGroup(*[
            base_block(b, w=0.84, h=0.70, font_size=32).move_to([z_xs[i], 1.15, 0])
            for i, b in enumerate(z_seq)
        ])
        tmpl_bb = strand_with_arrow(
            [[z_xs[0] - 0.70, 1.74, 0], [z_xs[-1] + 0.70, 1.74, 0]],
            color=GREY, stroke_width=6, direction="left", tip_len=0.34,
        )
        tmpl_tag = T("template (points left)", size=24, color=GREY).next_to(tmpl_bb, UP, buff=0.18).align_to(tmpl_bb, LEFT)

        new_bases = VGroup(*[
            base_block(COMPLEMENT[z_seq[i]], w=0.84, h=0.70, font_size=32).move_to([z_xs[i], -0.25, 0])
            for i in [1, 2, 3]
        ])
        new_bb = strand_with_arrow(
            [[z_xs[1] - 0.55, -0.84, 0], [z_xs[3] + 0.55, -0.84, 0]],
            color=GOLD, stroke_width=6, direction="right", tip_len=0.34,
        )
        tail_lab = T("tail end", size=24, color=GREY).move_to([z_xs[1] - 0.2, -1.44, 0])
        head_lab = T("arrowhead end", size=24, color=GOLD).move_to([z_xs[3] + 0.25, -1.44, 0])

        self.add(tmpl_bb, tmpl_bases, tmpl_tag, new_bb, new_bases, tail_lab, head_lab)
        glow = Circle(radius=0.34, color=GOLD, stroke_width=4, fill_color=GOLD, fill_opacity=0.25).move_to(new_bb.head.get_center())
        self.play(FadeIn(banner), FadeIn(glow), run_time=1.0)
        self.play(Indicate(new_bb.head, color=TEXT, scale_factor=1.35), run_time=1.2)

        self.at("adds nucleotides only")
        add_4 = base_block(COMPLEMENT[z_seq[4]], w=0.84, h=0.70, font_size=32).move_to([z_xs[4] + 1.5, -1.6, 0])
        new_bb_4 = strand_with_arrow(
            [[z_xs[1] - 0.55, -0.84, 0], [z_xs[4] + 0.55, -0.84, 0]],
            color=GOLD, stroke_width=6, direction="right", tip_len=0.34,
        )
        self.play(FadeIn(add_4), run_time=0.3)
        self.play(
            add_4.animate.move_to([z_xs[4], -0.25, 0]),
            ReplacementTransform(new_bb, new_bb_4),
            glow.animate.move_to(new_bb_4.head.get_center()),
            head_lab.animate.move_to([z_xs[4] + 0.25, -1.44, 0]),
            run_time=1.1,
        )
        new_bb = new_bb_4
        new_bases.add(add_4)

        try_0 = base_block(COMPLEMENT[z_seq[0]], w=0.84, h=0.70, font_size=32).move_to([z_xs[0] - 1.35, -1.5, 0])
        xm = x_mark([z_xs[0] - 0.15, 0.42, 0], color=RED, size=0.20)
        self.play(try_0.animate.move_to([z_xs[0] - 0.15, -0.25, 0]), run_time=0.65)
        self.play(FadeIn(xm), run_time=0.25)
        self.play(FadeOut(xm), FadeOut(try_0, shift=DL * 0.8), run_time=0.75)

        self.at("grows arrowhead first")
        add_5 = base_block(COMPLEMENT[z_seq[5]], w=0.84, h=0.70, font_size=32).move_to([z_xs[5] + 1.4, -1.6, 0])
        new_bb_5 = strand_with_arrow(
            [[z_xs[1] - 0.55, -0.84, 0], [z_xs[5] + 0.55, -0.84, 0]],
            color=GOLD, stroke_width=6, direction="right", tip_len=0.34,
        )
        self.play(
            add_5.animate.move_to([z_xs[5], -0.25, 0]),
            ReplacementTransform(new_bb, new_bb_5),
            glow.animate.move_to(new_bb_5.head.get_center()),
            head_lab.animate.move_to([z_xs[5] + 0.25, -1.44, 0]),
            run_time=1.1,
        )
        new_bb = new_bb_5
        new_bases.add(add_5)

        self.at("opposite way")
        new_tag = T("new strand (points right)", size=24, color=GOLD).move_to([0, -2.35, 0])
        self.play(
            FadeIn(new_tag),
            Indicate(tmpl_bb.head, color=TEXT, scale_factor=1.4),
            Indicate(new_bb.head, color=TEXT, scale_factor=1.4),
            run_time=1.2,
        )
        self.finish()


# ---------------------------------------------------------------------------
# S05: Upper Template (continuous leading strand following the fork)
# ---------------------------------------------------------------------------
class S05Upper(SpokenScene):
    def construct(self):
        fork_t = ValueTracker(-0.7)
        tpl = build_fork_template(-0.7)
        fm = fork_moves_marker(fork_t.get_value(), y=-2.58)
        fm.add_updater(lambda m: m.set_x(fork_t.get_value()))
        tpl.add_updater(lambda m: update_fork_template(m, fork_t.get_value()))

        cur_indices = [0, 1, 2]
        upper_seg = build_new_segment(cur_indices, is_upper=True)
        poly = polymerase_shape([XS[2], 1.39, 0], width=0.62, height=1.52, color=ORANGE, label_pos="above")
        piece_box = boxed_label("upper strand: 1 piece", color=GOLD, size=26, pad=0.14).move_to([4.35, 3.30, 0])

        self.add(tpl, upper_seg, poly, fm, piece_box)
        # Keep the fork gently advancing right from the start
        self.play(fork_t.animate.set_value(-0.45), run_time=1.8, rate_func=linear)

        self.at("points the way the fork moves")
        self.play(
            Indicate(upper_seg.bb.head, color=TEXT, scale_factor=1.45),
            fork_t.animate.set_value(-0.25),
            run_time=1.3,
        )

        self.at("follows the fork")
        targets = [(3, 0.08), (4, 0.42), (5, 0.76), (6, 1.10)]
        for idx, fx in targets:
            nxt_seg = build_new_segment(cur_indices + [idx], is_upper=True)
            new_b = nxt_seg.bases[-1]
            # Step polymerase across bases in 0.65s (< 1.0s motion threshold) then finish fork ease
            self.play(
                fork_t.animate.set_value(fx - 0.10),
                poly.animate.set_x(XS[idx]),
                FadeIn(new_b, shift=UP * 0.35),
                ReplacementTransform(upper_seg.bb, nxt_seg.bb),
                run_time=0.65,
                rate_func=linear,
            )
            self.play(fork_t.animate.set_value(fx), run_time=0.40, rate_func=linear)
            upper_seg.bases.add(new_b)
            upper_seg.bb = nxt_seg.bb
            cur_indices.append(idx)

        tpl.clear_updaters()
        fm.clear_updaters()
        self.finish()


# ---------------------------------------------------------------------------
# S06: Predict Question on the Lower Template
# ---------------------------------------------------------------------------
def build_s06_backdrop():
    """Exact frozen fork state shared between S06Predict and S07Pause."""
    fork_x = 1.10
    tpl = build_fork_template(fork_x)
    upper_seg = build_new_segment(list(range(7)), is_upper=True)
    poly = polymerase_shape([XS[6], 1.39, 0], width=0.62, height=1.52, color=ORANGE, label_pos="above")
    piece_box = boxed_label("upper strand: 1 piece", color=GOLD, size=26, pad=0.14).move_to([4.35, 3.30, 0])

    xL, xR = XS[0] - 0.35, XS[6] + 0.35
    bracket = VGroup(
        Line([xL, -2.32, 0], [xR, -2.32, 0], color=GOLD, stroke_width=4),
        Line([xL, -2.32, 0], [xL, -2.18, 0], color=GOLD, stroke_width=4),
        Line([xR, -2.32, 0], [xR, -2.18, 0], color=GOLD, stroke_width=4),
    )

    ghost_bb = DashedVMobject(
        Line([XS[0] - 0.32, -Y_NEW_BB, 0], [XS[6] + 0.32, -Y_NEW_BB, 0], color=GOLD, stroke_width=4.0),
        num_dashes=18,
    )
    ghost_head = Polygon(
        [XS[0] - 0.36, -Y_NEW_BB, 0],
        [XS[0] - 0.12, -Y_NEW_BB + 0.13, 0],
        [XS[0] - 0.12, -Y_NEW_BB - 0.13, 0],
        stroke_color=GOLD, stroke_width=2.5, fill_opacity=0,
    )
    ghost_rect = DashedVMobject(
        RoundedRectangle(width=XS[6] - XS[0] + 0.54, height=0.44, corner_radius=0.08, stroke_color=GOLD, stroke_width=2.8).move_to([(XS[0] + XS[6]) / 2, -Y_NEW_BASE, 0]),
        num_dashes=28,
    )
    ghost = VGroup(ghost_bb, ghost_head, ghost_rect)
    qmark = T("?", size=44, color=GOLD, weight=BOLD).move_to([XS[6] + 0.72, -1.04, 0])
    return VGroup(tpl, upper_seg, poly, piece_box, bracket, ghost, qmark)


PREDICT_Q = "If polymerase only adds at the arrowhead, how can it copy the lower strand?"


class S06Predict(SpokenScene):
    def construct(self):
        bd = build_s06_backdrop()
        tpl, upper_seg, poly, piece_box, bracket, ghost, qmark = bd
        ghost_bb, ghost_head, ghost_rect = ghost
        self.add(tpl, upper_seg, poly, piece_box)

        self.at("look at the lower template")
        self.play(Create(bracket), Indicate(tpl.l_bb, color=GOLD, scale_factor=1.04), run_time=2.0)

        self.at("point the other way")
        self.play(Create(ghost_rect), run_time=1.6)
        self.play(Create(ghost_bb), FadeIn(ghost_head, shift=LEFT * 0.25), run_time=1.4)

        self.at("If polymerase only adds")
        self.play(FadeIn(qmark, scale=1.3), Indicate(poly.body, color=GOLD, scale_factor=1.08), run_time=1.2)
        self.play(Indicate(qmark, color=TEXT, scale_factor=1.2), run_time=0.9)

        self.at("how can it copy")
        q = question_card(PREDICT_Q, y=-3.05, size=28, max_w=10.2)
        self.play(FadeIn(q, shift=UP * 0.15), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------
# S07: Silent 5 s Predict Pause
# ---------------------------------------------------------------------------
class S07Pause(PredictPause):
    QUESTION = PREDICT_Q
    CARD = {"y": -3.05, "size": 28, "max_w": 10.2}
    RING_AT = (6.0, -3.05, 0)
    SECONDS = 5.0

    def backdrop(self):
        return build_s06_backdrop()


# ---------------------------------------------------------------------------
# S08: Reveal — Lower Strand Built in Short Pieces & Joined
# ---------------------------------------------------------------------------
class S08Reveal(SpokenScene):
    def construct(self):
        fork_t = ValueTracker(1.10)
        tpl = build_fork_template(1.10)
        tpl.add_updater(lambda m: update_fork_template(m, fork_t.get_value()))
        upper_indices = list(range(7))
        upper_seg = build_new_segment(upper_indices, is_upper=True)
        poly_u = polymerase_shape([XS[6], 1.39, 0], width=0.62, height=1.52, color=ORANGE, label_pos="above")
        up_box = boxed_label("upper strand: 1 piece", color=GOLD, size=26, pad=0.14).move_to([4.35, 3.30, 0])
        low_box = boxed_label("lower strand pieces: 0", color=GOLD, size=26, pad=0.14).move_to([-4.0, -3.15, 0])
        fm = fork_moves_marker(fork_t.get_value(), y=-2.58)
        fm.add_updater(lambda m: m.set_x(fork_t.get_value()))

        self.add(tpl, upper_seg, poly_u, up_box, low_box, fm)

        def set_lower_counter(text):
            nonlocal low_box
            nb = boxed_label(text, color=GOLD, size=26, pad=0.14).move_to([-4.0, -3.15, 0])
            anim = swap(low_box, nb, run_time=0.45)
            low_box = nb
            return anim

        def grow_lower_piece(idx_desc):
            built = []
            seg = None
            for idx in idx_desc:
                built.append(idx)
                nxt = build_new_segment(built, is_upper=False)
                b_new = nxt.bases[0]
                if seg is None:
                    self.play(FadeIn(b_new, shift=DOWN * 0.30), FadeIn(nxt.bb), run_time=0.48)
                    seg = VGroup(nxt.bb, b_new)
                    seg.bb = nxt.bb
                    seg.bases = VGroup(b_new)
                else:
                    self.play(FadeIn(b_new, shift=DOWN * 0.30), ReplacementTransform(seg.bb, nxt.bb), run_time=0.42)
                    seg.bb = nxt.bb
                    seg.bases.add(b_new)
            return seg

        self.at("It builds in short pieces")
        p1 = grow_lower_piece([4, 3, 2, 1, 0])
        self.play(set_lower_counter("lower strand pieces: 1"))

        self.at("Each piece starts near")
        for idx, fx in [(7, 1.75), (8, 2.38), (9, 3.00)]:
            nxt_u = build_new_segment(upper_indices + [idx], is_upper=True)
            nb = nxt_u.bases[-1]
            self.play(
                fork_t.animate.set_value(fx),
                poly_u.animate.set_x(XS[idx]),
                FadeIn(nb, shift=UP * 0.30),
                ReplacementTransform(upper_seg.bb, nxt_u.bb),
                run_time=0.62,
            )
            upper_seg.bases.add(nb)
            upper_seg.bb = nxt_u.bb
            upper_indices.append(idx)

        p2 = grow_lower_piece([8, 7, 6, 5])
        self.play(set_lower_counter("lower strand pieces: 2"))

        self.at("When the fork opens more")
        for idx, fx in [(10, 3.65), (11, 4.30), (12, 4.90)]:
            nxt_u = build_new_segment(upper_indices + [idx], is_upper=True)
            nb = nxt_u.bases[-1]
            self.play(
                fork_t.animate.set_value(fx),
                poly_u.animate.set_x(XS[idx]),
                FadeIn(nb, shift=UP * 0.30),
                ReplacementTransform(upper_seg.bb, nxt_u.bb),
                run_time=0.60,
            )
            upper_seg.bases.add(nb)
            upper_seg.bb = nxt_u.bb
            upper_indices.append(idx)

        p3 = grow_lower_piece([12, 11, 10, 9])
        self.play(set_lower_counter("lower strand pieces: 3"))

        self.at("Another enzyme joins")
        seam1 = np.array([(XS[4] + XS[5]) / 2, -Y_NEW_BB, 0.0])
        seam2 = np.array([(XS[8] + XS[9]) / 2, -Y_NEW_BB, 0.0])
        clip = joining_clip([seam1[0], -0.25, 0.0], color=GREY)
        enz_lab = boxed_label("joining enzyme", color=GREY, size=24, pad=0.12).move_to([seam1[0], 0.32, 0.0])
        self.play(FadeIn(clip), FadeIn(enz_lab), run_time=0.45)

        joined_12 = strand_with_arrow([[XS[0] - 0.34, -Y_NEW_BB, 0], [XS[8] + 0.34, -Y_NEW_BB, 0]], color=GOLD, stroke_width=5.0, direction="left")
        flash1 = Circle(radius=0.18, color=TEXT, stroke_width=4, fill_color=TEXT, fill_opacity=0.65).move_to(seam1)
        self.play(FadeIn(flash1), FadeOut(p1.bb), FadeOut(p2.bb), FadeIn(joined_12), run_time=0.70)
        self.play(FadeOut(flash1), run_time=0.18)

        joined_all = strand_with_arrow([[XS[0] - 0.34, -Y_NEW_BB, 0], [XS[12] + 0.34, -Y_NEW_BB, 0]], color=GOLD, stroke_width=5.0, direction="left")
        flash2 = Circle(radius=0.18, color=TEXT, stroke_width=4, fill_color=TEXT, fill_opacity=0.65).move_to(seam2)
        self.play(
            clip.animate.move_to([seam2[0], -0.25, 0.0]),
            enz_lab.animate.move_to([seam2[0], 0.32, 0.0]),
            FadeIn(flash2),
            FadeOut(joined_12), FadeOut(p3.bb), FadeIn(joined_all),
            set_lower_counter("lower strand: joined"),
            run_time=0.80,
        )
        self.play(FadeOut(flash2), run_time=0.22)

        tpl.clear_updaters()
        fm.clear_updaters()
        self.finish()


# ---------------------------------------------------------------------------
# S09: Matching Check (Zoom in inside polymerase + Tally starts)
# ---------------------------------------------------------------------------
def build_closeup_active_site(include_third_pair=False, third_base="G", mismatch_left=False):
    """Shared zoomed-in upper-strand active site; polymerase walls stay cleanly in the gaps between bases."""
    c_xs = [-4.8, -3.5, -2.2, -0.9]
    tmpl_seq = ["T", "A", "C", "G"]
    tmpl_bases = VGroup(*[
        base_block(b, w=0.82, h=0.68, font_size=30).move_to([c_xs[i], 1.35, 0])
        for i, b in enumerate(tmpl_seq)
    ])
    tmpl_bb = strand_with_arrow([[c_xs[0] - 0.65, 1.94, 0], [c_xs[-1] + 0.65, 1.94, 0]], color=GREY, stroke_width=6, direction="left", tip_len=0.32)

    new_0_letter = "G" if mismatch_left else "A"
    new_bases = VGroup(
        base_block(new_0_letter, w=0.82, h=0.68, font_size=30).move_to([c_xs[0], -0.15, 0]),
        base_block("T", w=0.82, h=0.68, font_size=30).move_to([c_xs[1], -0.15, 0]),
    )
    end_idx = 2 if include_third_pair else 1
    if include_third_pair:
        new_bases.add(base_block(third_base, w=0.82, h=0.68, font_size=30).move_to([c_xs[2], -0.15, 0]))
    new_bb = strand_with_arrow([[c_xs[0] - 0.55, -0.74, 0], [c_xs[end_idx] + 0.55, -0.74, 0]], color=GOLD, stroke_width=6, direction="right", tip_len=0.32)

    poly = polymerase_shape([c_xs[2], 0.60, 0], width=1.12, height=3.06, color=ORANGE, label_pos="above")
    return VGroup(tmpl_bb, tmpl_bases, new_bb, new_bases, poly), c_xs


def build_tally_ledger():
    return Ledger(
        [("1.", "matching check", GREEN), ("2.", "proofreading", GOLD), ("3.", "repair", TEAL)],
        top_left=(1.3, 2.2),
        row_h=0.65,
        key_w=0.6,
        width=4.6,
        title="accuracy checks",
        size=28,
    )


class S09Check(SpokenScene):
    def construct(self):
        site, c_xs = build_closeup_active_site(include_third_pair=False)
        tmpl_bb, tmpl_bases, new_bb, new_bases, poly = site
        ledger = build_tally_ledger()

        wrong_a = base_block("A", w=0.82, h=0.68, font_size=30).move_to([c_xs[2] - 0.2, -2.55, 0])
        good_g = base_block("G", w=0.82, h=0.68, font_size=30).move_to([c_xs[2] + 1.0, -2.55, 0])

        # Zoom cleanly into the close-up active site over the opening sentence while keeping labels >= 22 pt
        site_geom = VGroup(tmpl_bb, tmpl_bases, new_bb, new_bases, poly.body)
        site_geom.save_state()
        poly.label.save_state()
        site_geom.scale(0.82)
        poly.label.next_to(poly.body, UP, buff=0.16)
        self.play(FadeIn(site_geom), FadeIn(poly.label), run_time=0.6)
        self.play(Restore(site_geom), Restore(poly.label), FadeIn(ledger), FadeIn(wrong_a), FadeIn(good_g), run_time=1.6)
        self.play(
            wrong_a.animate.move_to([c_xs[2] - 0.2, -2.10, 0]),
            good_g.animate.move_to([c_xs[2] + 1.0, -2.10, 0]),
            Indicate(tmpl_bases[2], color=TEXT, scale_factor=1.18),
            run_time=1.5,
        )

        self.at("Polymerase tests each incoming")
        self.play(wrong_a.animate.move_to([c_xs[2], -0.15, 0]), run_time=1.8)
        self.play(wrong_a.animate.shift(UP * 0.18), Indicate(tmpl_bases[2], color=GREEN, scale_factor=1.15), run_time=1.4)
        self.play(wrong_a.animate.shift(DOWN * 0.18), run_time=1.1)

        self.at("A nucleotide that does not pair")
        xm = x_mark([c_xs[2], 0.62, 0], color=RED, size=0.19)
        self.play(FadeIn(xm), run_time=0.35)
        self.play(
            FadeOut(xm),
            FadeOut(wrong_a, shift=DL * 0.8),
            run_time=0.9,
        )

        new_bb_ext = strand_with_arrow([[c_xs[0] - 0.55, -0.74, 0], [c_xs[2] + 0.55, -0.74, 0]], color=GOLD, stroke_width=6, direction="right", tip_len=0.32)
        self.play(
            good_g.animate.move_to([c_xs[2], -0.15, 0]),
            ReplacementTransform(new_bb, new_bb_ext),
            ledger.reveal(0),
            run_time=1.3,
        )
        self.finish()


# ---------------------------------------------------------------------------
# S10: Proofreading & Repair
# ---------------------------------------------------------------------------
class S10Proofread(SpokenScene):
    def construct(self):
        site, c_xs = build_closeup_active_site(include_third_pair=False, mismatch_left=True)
        tmpl_bb, tmpl_bases, new_bb, new_bases, poly = site

        ledger = build_tally_ledger()
        self.add(tmpl_bb, tmpl_bases, new_bb, new_bases, poly, ledger)
        ledger.revealed.append(ledger.rows[0])
        self.add(ledger.rows[0])

        leftover_mark = x_mark([c_xs[0], 0.60, 0], color=RED, size=0.18)

        self.at("a wrong base slips")
        wrong_a = base_block("A", w=0.82, h=0.68, font_size=30).move_to([c_xs[2], -2.15, 0])
        bb_wrong = strand_with_arrow([[c_xs[0] - 0.55, -0.74, 0], [c_xs[2] + 0.55, -0.74, 0]], color=GOLD, stroke_width=6, direction="right", tip_len=0.32)
        slip_mark = x_mark([c_xs[2], 0.60, 0], color=RED, size=0.18)
        self.play(
            wrong_a.animate.move_to([c_xs[2], -0.15, 0]),
            ReplacementTransform(new_bb, bb_wrong),
            run_time=1.0,
        )
        self.play(FadeIn(slip_mark), poly.animate.set_x(c_xs[3]), run_time=0.7)

        self.at("Polymerase checks")
        self.play(poly.animate.set_x(c_xs[2]), run_time=0.75)

        self.at("removes most wrong ones")
        good_g = base_block("G", w=0.82, h=0.68, font_size=30).move_to([c_xs[2], -2.15, 0])
        self.play(FadeOut(slip_mark), FadeOut(wrong_a, shift=DOWN * 0.7), run_time=0.75)
        self.play(good_g.animate.move_to([c_xs[2], -0.15, 0]), run_time=0.95)

        self.at("called proofreading")
        self.play(ledger.reveal(1), run_time=0.9)

        self.at("Repair enzymes")
        wrench = repair_wrench([c_xs[0], -1.60, 0], color=TEAL)
        rep_lab = boxed_label("repair enzyme", color=TEAL, size=24, pad=0.12).move_to([c_xs[0] + 0.3, -2.45, 0])
        self.play(FadeIn(leftover_mark), FadeIn(wrench), FadeIn(rep_lab), run_time=0.7)
        self.play(Indicate(leftover_mark, color=RED, scale_factor=1.25), run_time=0.6)

        fixed_a = base_block("A", w=0.82, h=0.68, font_size=30).move_to([c_xs[0] - 1.0, -1.55, 0])
        self.play(
            FadeOut(leftover_mark),
            FadeOut(new_bases[0], shift=DOWN * 0.25),
            fixed_a.animate.move_to([c_xs[0], -0.15, 0]),
            ledger.reveal(2),
            run_time=1.4,
        )
        self.finish()


# ---------------------------------------------------------------------------
# S11: Tally — Stacked Accuracy Bar & 1 in 1,000,000,000 Estimate
# ---------------------------------------------------------------------------
class S11Tally(SpokenScene):
    def construct(self):
        ledger = build_tally_ledger()
        ledger.move_to([0, 1.55, 0])
        self.add(ledger, *ledger.rows)

        title = T("accuracy checks", size=34, color=TEXT, weight=BOLD).move_to([0, 2.55, 0])
        seg_w, seg_h = 3.8, 0.96
        s1 = boxed_label("1. matching check", color=GREEN, size=28, box=(seg_w, seg_h))
        s2 = boxed_label("2. proofreading", color=GOLD, size=28, box=(seg_w, seg_h))
        s3 = boxed_label("3. repair", color=TEAL, size=28, box=(seg_w, seg_h))
        bar = VGroup(s1, s2, s3).arrange(RIGHT, buff=0.24).move_to([0, 1.10, 0])

        self.at("Put the checks together")
        self.play(FadeOut(VGroup(ledger, *ledger.rows), shift=UP * 0.15), run_time=0.35)
        self.play(FadeIn(title), FadeIn(bar, shift=UP * 0.15), run_time=0.6)

        self.at("the matching check")
        self.play(Indicate(s1, color=TEXT, scale_factor=1.06), run_time=0.65)
        self.at("proofreading")
        self.play(Indicate(s2, color=TEXT, scale_factor=1.06), run_time=0.55)
        self.at("then repair")
        self.play(Indicate(s3, color=TEXT, scale_factor=1.06), run_time=0.65)

        self.at("Each later check")
        h_vals = [0.78, 0.34, 0.10]
        filter_bars = VGroup()
        for seg, h in zip(bar, h_vals):
            fb = Rectangle(width=seg.width * 0.78, height=h, stroke_color=RED, stroke_width=2.5, fill_color=RED, fill_opacity=0.28)
            fb.next_to(seg, DOWN, buff=0.24)
            filter_bars.add(fb)
        err_note = T("uncorrected errors", size=26, color=RED).next_to(filter_bars[0], DOWN, buff=0.18)
        self.play(GrowFromEdge(filter_bars[0], UP), FadeIn(err_note), run_time=1.0)
        self.play(GrowFromEdge(filter_bars[1], UP), run_time=1.0)
        self.play(GrowFromEdge(filter_bars[2], UP), run_time=1.0)

        self.at("A textbook estimate")
        est_box = boxed_label("about 1 uncorrected mistake per 1,000,000,000 bases copied", color=GOLD, size=28, pad=0.24).move_to([0, -2.05, 0])
        est_sub = T("(textbook estimate)", size=24, color=TEXT).next_to(est_box, DOWN, buff=0.18)
        self.play(FadeIn(est_box, shift=UP * 0.12), run_time=1.2)
        self.play(FadeIn(est_sub, shift=UP * 0.10), Indicate(est_box, color=TEXT, scale_factor=1.03), run_time=1.3)
        self.finish()


# ---------------------------------------------------------------------------
# S12: Two Jobs — Pairing (possible) & Checking (accurate) under Moving Fork
# ---------------------------------------------------------------------------
class S12TwoJobs(SpokenScene):
    def construct(self):
        fork_t = ValueTracker(-0.5)
        tpl = build_fork_template(fork_t.get_value(), y_offset=2.30, compact=True)
        tpl.add_updater(lambda m: update_fork_template(m, fork_t.get_value()))
        self.add(tpl)

        tp = TwoPanel("possible", "accurate", colors=(GOLD, TEAL), top=0.80, bottom=-3.00, gap=0.45, width=12.4, size=32)

        pair_at = VGroup(
            base_block("A", w=0.68, h=0.54, font_size=28),
            T("with", size=26, color=TEXT),
            base_block("T", w=0.68, h=0.54, font_size=28),
        ).arrange(RIGHT, buff=0.22)
        pair_cg = VGroup(
            base_block("C", w=0.68, h=0.54, font_size=28),
            T("with", size=26, color=TEXT),
            base_block("G", w=0.68, h=0.54, font_size=28),
        ).arrange(RIGHT, buff=0.22)
        left_note = T("pairing sets each base", size=26, color=GOLD)
        left_content = VGroup(pair_at, pair_cg, left_note).arrange(DOWN, buff=0.28)
        tp.put(left_content, "left")

        r1 = boxed_label("1. matching check", color=GREEN, size=26, box=(4.6, 0.54))
        r2 = boxed_label("2. proofreading", color=GOLD, size=26, box=(4.6, 0.54))
        r3 = boxed_label("3. repair", color=TEAL, size=26, box=(4.6, 0.54))
        right_note = T("checking removes slips", size=26, color=TEAL)
        right_content = VGroup(r1, r2, r3, right_note).arrange(DOWN, buff=0.20)
        tp.put(right_content, "right")

        left_panel_all = VGroup(tp.left_frame, tp.left_head, left_content)
        right_panel_all = VGroup(tp.right_frame, tp.right_head, right_content)

        self.at("two jobs")
        self.play(fork_t.animate.set_value(0.6), run_time=1.8, rate_func=linear)

        self.at("Pairing makes the copy")
        self.play(FadeIn(left_panel_all, shift=UP * 0.15), fork_t.animate.set_value(1.5), run_time=1.0, rate_func=linear)
        self.play(fork_t.animate.set_value(3.0), run_time=3.5, rate_func=linear)

        self.at("Checking makes the copy")
        self.play(FadeIn(right_panel_all, shift=UP * 0.15), fork_t.animate.set_value(3.8), run_time=1.0, rate_func=linear)

        self.at("removes almost every")
        self.play(
            left_panel_all.animate.shift(RIGHT * 0.14),
            right_panel_all.animate.shift(LEFT * 0.14),
            fork_t.animate.set_value(4.8),
            run_time=1.5,
            rate_func=smooth,
        )
        tpl.clear_updaters()
        self.finish()


# ---------------------------------------------------------------------------
# S13: End Card
# ---------------------------------------------------------------------------
class S13End(EndCard):
    LINE = "Pairing makes the copy possible; checking makes it accurate."
