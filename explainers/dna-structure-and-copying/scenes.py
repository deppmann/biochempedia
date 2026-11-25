"""
COLOUR MAP (one colour per concept for the whole film):
  OLD_COL   = GREY (#8B93A1)   old strands, sugar, phosphate, and old backbones
  NEW_COL   = GOLD (#D4A843)   new strands and new backbones
  BASE_A    = RED (#FC6255)    adenine (A)
  BASE_T    = BLUE (#58C4DD)   thymine (T)
  BASE_C    = GREEN (#83C167)  cytosine (C)
  BASE_G    = PURPLE (#B378E8) guanine (G)
  ENZYME    = TEAL (#3FB8C0)   unzipping enzyme wedge
  TEXT      = WHITE (#E8EAF0)  labels on dark navy (#0F1117)

WORLD CARRIED THROUGH THE FILM:
  Backbones with directional arrowheads carrying notched, lettered, key-coloured
  base blocks (A/T/C/G) that snap into strands, pair across hydrogen bonds, twist
  into a schematic helix, unzip into templates, and build two daughter molecules.

WHAT CHANGES PER SPOKEN SCENE (and what it is computed from):
  s01_question   : 6-rung horizontal DNA ladder builds, is gripped and ripped lengthwise; lower strand slides into bin leaving upper strand + 6 '?' slots.
  s02_nucleotide : Sugar pentagon, phosphate circle, and base block fly in and assemble into one nucleotide, then split into 4 coloured A/T/C/G copies.
  s03_strand     : 4 nucleotides slide up one by one to snap sugar-to-phosphate covalent bonds with shared-electron markers, fusing into a grey backbone (strands: 1).
  s04_pairing    : Second opposite-pointing grey strand slides in; hydrogen bonds dash across the gap; complementary A-T and C-G notches click shut (strands: 2).
  s05_misfit     : Zoomed rung: A approaches C, notched edges clash and recoil with red X; T slides in and clicks with A, then C clicks with G; rule banner settles.
  s06_helix      : Opposite arrowheads pulse; glowing directional segments sweep opposite ways along both backbones; 6-rung ladder twists into a schematic double helix, then untwists.
  s07_predict    : Left G-A-T-T-C-A strand highlighted letter by letter beside 6 empty dashed slots, pencil icon, and question card.
  s09_reveal     : 6 empty slots fill top-to-bottom with C-T-A-A-G-T blocks clicking into place; partner backbone closes and bracket labels the pair.
  s10_unzip      : 10-rung grey ladder opens progressively into a Y-fork as an enzyme wedge moves down the middle, separating both strands into two labelled templates.
  s11_two        : New gold nucleotides build beside each grey template one base at a time into two readable daughter molecules; rung-by-rung highlight frames compare both.
  s12_rule       : Both large daughter molecules remain readable on left and right while center rule banner transforms to 'each strand fixes its partner' and 'accuracy ?' fades.
"""
from bp_parts import *

# ------------------------------------------------------------------ Colour Map
OLD_COL = GREY
NEW_COL = GOLD
PURPLE = "#B378E8"
BASE_COLORS = {
    "A": RED,
    "T": BLUE,
    "C": GREEN,
    "G": PURPLE,
}
PAIR = {"A": "T", "T": "A", "C": "G", "G": "C"}
SEQ_6 = ["G", "A", "T", "T", "C", "A"]
SEQ_10 = ["G", "A", "T", "T", "C", "A", "G", "C", "T", "A"]


# ------------------------------------------------------------------ Shared DNA Builders
def base_poly_pts(letter, dir_sign=1, w=0.94, h=0.48, axis="x"):
    """Polygon vertices around origin for a notched base block.
    dir_sign=+1 extends +axis (right or up); dir_sign=-1 extends -axis (left or down).
    """
    n = 0.16 * (w / 0.84)
    hw, hh = w / 2.0, h / 2.0
    if letter == "A":
        pts = [(-hw, hh), (hw - 0.3 * n, hh), (hw + 0.7 * n, 0.0), (hw - 0.3 * n, -hh), (-hw, -hh)]
    elif letter == "T":
        pts = [(-hw, hh), (hw + 0.2 * n, hh), (hw - 0.8 * n, 0.0), (hw + 0.2 * n, -hh), (-hw, -hh)]
    elif letter == "C":
        pts = [
            (-hw, hh),
            (hw - 0.4 * n, hh),
            (hw - 0.4 * n, 0.24 * h),
            (hw + 0.65 * n, 0.24 * h),
            (hw + 0.65 * n, -0.24 * h),
            (hw - 0.4 * n, -0.24 * h),
            (hw - 0.4 * n, -hh),
            (-hw, -hh),
        ]
    else:
        pts = [
            (-hw, hh),
            (hw + 0.25 * n, hh),
            (hw + 0.25 * n, 0.28 * h),
            (hw - 0.75 * n, 0.28 * h),
            (hw - 0.75 * n, -0.28 * h),
            (hw + 0.25 * n, -0.28 * h),
            (hw + 0.25 * n, -hh),
            (-hw, -hh),
        ]

    out = []
    for px, py in pts:
        x = px * dir_sign
        y = py
        out.append([y, x, 0.0] if axis == "y" else [x, y, 0.0])
    return [np.array(p, dtype=float) for p in out]


def make_base(letter, dir_sign=1, w=0.94, h=0.48, font_size=26, axis="x", fill_op=0.48, stroke_w=3.0):
    """Notched, key-coloured base block with upright legible letter."""
    col = BASE_COLORS[letter]
    poly = Polygon(
        *base_poly_pts(letter, dir_sign=dir_sign, w=w, h=h, axis=axis),
        stroke_color=col,
        stroke_width=stroke_w,
        fill_color=col,
        fill_opacity=fill_op,
    )
    txt = T(letter, size=font_size, color=TEXT, weight=BOLD)
    shift_amt = -dir_sign * 0.06 * (w / 0.84)
    txt.move_to([0.0, shift_amt, 0.0] if axis == "y" else [shift_amt, 0.0, 0.0])
    g = VGroup(poly, txt)
    g.poly, g.txt, g.letter = poly, txt, letter
    return g


def make_empty_slot(w=0.94, h=0.48, font_size=26, label="?", color=GREY):
    """Dashed empty base slot for prediction scenes."""
    rect = DashedVMobject(
        RoundedRectangle(corner_radius=0.08, width=w, height=h, stroke_color=color, stroke_width=2.8),
        num_dashes=14,
    )
    txt = T(label, size=font_size, color=color, weight=BOLD).move_to(rect)
    return VGroup(rect, txt)


def make_backbone_v(x, y_top, y_bot, arrow_dir=DOWN, color=OLD_COL, stroke_w=13.0, head_size=0.30):
    """Vertical strand backbone with a filled directional arrowhead at arrow_dir end."""
    if np.allclose(arrow_dir, DOWN):
        start = np.array([x, y_top, 0.0])
        end = np.array([x, y_bot + head_size * 0.6, 0.0])
        tip = np.array([x, y_bot - head_size * 0.55, 0.0])
        base_y = y_bot + head_size * 0.65
    else:
        start = np.array([x, y_bot, 0.0])
        end = np.array([x, y_top - head_size * 0.6, 0.0])
        tip = np.array([x, y_top + head_size * 0.55, 0.0])
        base_y = y_top - head_size * 0.65
    head = Polygon(
        [x - head_size * 0.65, base_y, 0.0],
        [x + head_size * 0.65, base_y, 0.0],
        tip,
        stroke_width=0,
        fill_color=color,
        fill_opacity=1.0,
    )
    line = Line(start, end, color=color, stroke_width=stroke_w)
    line.set_cap_style(CapStyleType.ROUND)
    g = VGroup(line, head)
    g.line, g.head = line, head
    return g


def make_backbone_h(y, x_left, x_right, arrow_dir=RIGHT, color=OLD_COL, stroke_w=13.0, head_size=0.32):
    """Horizontal strand backbone with a filled directional arrowhead."""
    if np.allclose(arrow_dir, RIGHT):
        start = np.array([x_left, y, 0.0])
        end = np.array([x_right - head_size * 0.6, y, 0.0])
        tip = np.array([x_right + head_size * 0.55, y, 0.0])
        bx = x_right - head_size * 0.65
    else:
        start = np.array([x_right, y, 0.0])
        end = np.array([x_left + head_size * 0.6, y, 0.0])
        tip = np.array([x_left - head_size * 0.55, y, 0.0])
        bx = x_left + head_size * 0.65
    head = Polygon(
        [bx, y + head_size * 0.65, 0.0],
        [bx, y - head_size * 0.65, 0.0],
        tip,
        stroke_width=0,
        fill_color=color,
        fill_opacity=1.0,
    )
    line = Line(start, end, color=color, stroke_width=stroke_w)
    line.set_cap_style(CapStyleType.ROUND)
    g = VGroup(line, head)
    g.line, g.head = line, head
    return g


def make_hbonds_v(x_left_tip, x_right_tip, y, color=TEXT):
    """Short hydrogen-bond bars sitting strictly inside the seam gap."""
    x0 = x_left_tip + 0.03
    x1 = x_right_tip - 0.03
    if x1 <= x0 + 0.02:
        xm = (x_left_tip + x_right_tip) / 2.0
        x0, x1 = xm - 0.03, xm + 0.03
    return VGroup(
        Line([x0, y + 0.08, 0], [x1, y + 0.08, 0], color=color, stroke_width=2.8),
        Line([x0, y - 0.08, 0], [x1, y - 0.08, 0], color=color, stroke_width=2.8),
    )


def make_key(pos=(-4.8, -3.15, 0)):
    """Compact 4-base colour key (A, T, C, G)."""
    items = []
    for b in ("A", "T", "C", "G"):
        col = BASE_COLORS[b]
        r = RoundedRectangle(corner_radius=0.08, width=0.48, height=0.46, stroke_color=col, stroke_width=2.6,
                             fill_color=col, fill_opacity=0.48)
        t = T(b, size=24, color=TEXT, weight=BOLD).move_to(r)
        items.append(VGroup(r, t))
    return VGroup(*items).arrange(RIGHT, buff=0.14).move_to(pos)


def make_counter(text, pos=(-4.75, 3.22, 0), color=TEXT):
    """Top-left status counter pill, leaving top-right corner clear for Hex."""
    return boxed_label(text, color=color, size=26, pad=0.16, fill_opacity=0.22).move_to(pos)


def make_strand_v(seq, x_bb, base_dir=1, arrow_dir=DOWN, y_top=2.2, pitch=0.72, w=0.94, h=0.48,
                  font_size=26, bb_color=OLD_COL, bb_gap=0.16):
    """Vertical strand: backbone with arrowhead + attached base blocks."""
    ys = [y_top - i * pitch for i in range(len(seq))]
    bb = make_backbone_v(x_bb, ys[0] + pitch * 0.48, ys[-1] - pitch * 0.48, arrow_dir=arrow_dir, color=bb_color)
    bases = VGroup()
    x_base = x_bb + base_dir * (bb_gap + w / 2.0)
    for b, y in zip(seq, ys):
        bm = make_base(b, dir_sign=base_dir, w=w, h=h, font_size=font_size)
        bm.move_to([x_base, y, 0.0])
        bases.add(bm)
    g = VGroup(bb, bases)
    g.bb, g.bases, g.ys = bb, bases, ys
    return g


def make_ladder_v(seq, cx=0.0, y_top=2.2, pitch=0.72, w=0.94, h=0.48, font_size=26,
                  left_col=OLD_COL, right_col=OLD_COL, half_sep=0.52, bb_gap=0.16):
    """Complete two-strand flat vertical ladder with hydrogen-bond dashes."""
    x_bb_l = cx - half_sep - w - bb_gap
    x_bb_r = cx + half_sep + w + bb_gap
    left = make_strand_v(seq, x_bb_l, base_dir=1, arrow_dir=DOWN, y_top=y_top, pitch=pitch, w=w, h=h,
                         font_size=font_size, bb_color=left_col, bb_gap=bb_gap)
    comp = [PAIR[b] for b in seq]
    right = make_strand_v(comp, x_bb_r, base_dir=-1, arrow_dir=UP, y_top=y_top, pitch=pitch, w=w, h=h,
                          font_size=font_size, bb_color=right_col, bb_gap=bb_gap)
    hbonds = VGroup()
    for y in left.ys:
        hbonds.add(make_hbonds_v(cx - half_sep + 0.06, cx + half_sep - 0.06, y))
    g = VGroup(left, right, hbonds)
    g.left, g.right, g.hbonds = left, right, hbonds
    return g


def make_pentagon(w=2.4, h=1.65, color=OLD_COL, fill_op=0.42):
    """Rounded pentagon block for deoxyribose sugar."""
    pts = [
        [-w * 0.42, -h * 0.48, 0.0],
        [w * 0.42, -h * 0.48, 0.0],
        [w * 0.50, h * 0.08, 0.0],
        [0.0, h * 0.50, 0.0],
        [-w * 0.50, h * 0.08, 0.0],
    ]
    return Polygon(*pts, stroke_color=color, stroke_width=3.2, fill_color=color, fill_opacity=fill_op).round_corners(0.14)


def make_pencil(pos=(2.85, 0.4, 0)):
    """Simple schematic pencil icon."""
    body = Rectangle(width=0.26, height=0.90, stroke_color=GOLD, stroke_width=2.6, fill_color=GOLD, fill_opacity=0.45)
    tip = Polygon([-0.13, -0.45, 0], [0.13, -0.45, 0], [0.0, -0.72, 0],
                  stroke_color=TEXT, stroke_width=2.0, fill_color=TEXT, fill_opacity=0.92)
    cap = Rectangle(width=0.26, height=0.16, stroke_color=RED, stroke_width=2.0, fill_color=RED, fill_opacity=0.55).next_to(body, UP, buff=0)
    return VGroup(body, tip, cap).rotate(-0.45).move_to(pos)


def make_hand(pos, flip_x=1.0, color=TEXT):
    """Clean schematic mitten hand for ripping the DNA ladder in s01."""
    palm = RoundedRectangle(corner_radius=0.16, width=0.72, height=0.50, stroke_color=color, stroke_width=3.0,
                            fill_color=TEAL, fill_opacity=0.24)
    thumb = RoundedRectangle(corner_radius=0.10, width=0.26, height=0.36, stroke_color=color, stroke_width=3.0,
                             fill_color=TEAL, fill_opacity=0.24).move_to([0.28 * flip_x, 0.25, 0])
    return VGroup(palm, thumb).move_to(pos)


# ------------------------------------------------------------------ Scenes
class S00Title(TitleCard):
    LESSON = "DNA: Structure and Copying"
    TITLE = "One Strand Is Enough"


class S01Question(SpokenScene):
    def construct(self):
        xs = [-3.40 + i * 1.36 for i in range(6)]
        top_y, bot_y = 1.33, -1.03
        top_bb = make_backbone_h(top_y, xs[0] - 0.80, xs[-1] + 0.80, arrow_dir=RIGHT, color=OLD_COL)
        bot_bb = make_backbone_h(bot_y, xs[0] - 0.80, xs[-1] + 0.80, arrow_dir=LEFT, color=OLD_COL)

        top_bases = VGroup()
        bot_bases = VGroup()
        hbonds = VGroup()
        for x, b in zip(xs, SEQ_6):
            tb = make_base(b, dir_sign=-1, w=1.02, h=0.98, font_size=32, axis="y").move_to([x, 0.70, 0])
            bb = make_base(PAIR[b], dir_sign=1, w=1.02, h=0.98, font_size=32, axis="y").move_to([x, -0.40, 0])
            hb = VGroup(
                Line([x - 0.14, 0.11, 0], [x - 0.14, 0.19, 0], color=TEXT, stroke_width=2.8),
                Line([x + 0.14, 0.11, 0], [x + 0.14, 0.19, 0], color=TEXT, stroke_width=2.8),
            )
            top_bases.add(tb)
            bot_bases.add(bb)
            hbonds.add(hb)

        top_half = VGroup(top_bb, top_bases)
        bot_half = VGroup(bot_bb, bot_bases)
        key = make_key(pos=(-4.75, 3.20, 0))

        self.play(Create(top_bb), Create(bot_bb), FadeIn(key), run_time=0.7)
        self.play(FadeIn(top_bases), FadeIn(bot_bases), Create(hbonds), run_time=0.9)

        self.at("down the middle")
        hand_top = make_hand((-4.65, 1.35, 0), flip_x=1.0)
        hand_bot = make_hand((-4.65, -1.05, 0), flip_x=1.0)
        bin_box = VGroup(
            Polygon([-0.92, 0.60, 0], [0.92, 0.60, 0], [0.70, -0.60, 0], [-0.70, -0.60, 0],
                    stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.28),
            T("bin", size=24, color=TEXT).move_to([0, -0.05, 0]),
        ).move_to([4.6, -2.55, 0])

        self.play(FadeIn(hand_top, shift=RIGHT * 0.2), FadeIn(hand_bot, shift=RIGHT * 0.2), run_time=0.4)
        self.play(
            FadeOut(hbonds, run_time=0.3),
            top_half.animate.shift(UP * 0.35),
            hand_top.animate.shift(UP * 0.35),
            bot_half.animate.shift(DOWN * 0.70),
            hand_bot.animate.shift(DOWN * 0.70),
            run_time=0.75,
        )

        self.at("threw one half")
        self.play(FadeIn(bin_box, shift=UP * 0.2), FadeOut(hand_top), FadeOut(hand_bot), run_time=0.35)
        self.play(
            bot_half.animate.scale(0.32).move_to(bin_box[0].get_top() + DOWN * 0.15).set_opacity(0.0),
            run_time=0.85,
        )
        self.play(FadeOut(bin_box, shift=RIGHT * 0.6), run_time=0.45)

        self.at("Could you rebuild")
        q_slots = VGroup(*[make_empty_slot(w=1.02, h=0.98, font_size=32).move_to([x, -0.42, 0]) for x in xs])
        q_mark = T("?", size=76, color=GOLD, weight=BOLD).move_to([0.0, -1.85, 0])
        self.play(FadeIn(q_slots), FadeIn(q_mark, shift=UP * 0.15), run_time=0.7)

        self.at("letter for letter")
        for sl in q_slots:
            self.play(sl[0].animate.set_stroke(GOLD, width=3.8), run_time=0.18)
            self.play(sl[0].animate.set_stroke(GREY, width=2.8), run_time=0.10)

        self.at("By the end")
        cap = caption("Rebuild the missing strand, letter for letter?", color=GOLD)
        cap.move_to([0.0, -3.10, 0])
        self.play(FadeIn(cap, shift=UP * 0.1), q_mark.animate.set_color(TEAL), run_time=0.7)
        self.finish()


class S02Nucleotide(SpokenScene):
    def construct(self):
        ghost = DashedVMobject(
            RoundedRectangle(corner_radius=0.22, width=10.8, height=4.5, stroke_color=GREY, stroke_width=2.4),
            num_dashes=52,
        ).move_to([0.0, 0.15, 0.0])
        title_nuc = boxed_label("NUCLEOTIDE", color=TEAL, size=28, pad=0.18, fill_opacity=0.22).move_to([0.0, 2.90, 0])
        self.play(Create(ghost), FadeIn(title_nuc, shift=DOWN * 0.1), run_time=0.9)

        self.at("three parts")
        self.play(ghost.animate.set_stroke(TEAL, width=2.8), run_time=0.55)

        self.at("sugar called deoxyribose")
        sugar_shape = make_pentagon(w=3.6, h=2.20, color=OLD_COL, fill_op=0.42).move_to([-0.15, -0.15, 0])
        sugar_lbl = T("sugar\n(deoxyribose)", size=24, color=TEXT, line_spacing=0.85).move_to(
            sugar_shape.get_center() + DOWN * 0.12
        )
        sugar = VGroup(sugar_shape, sugar_lbl)
        self.play(FadeIn(sugar, shift=UP * 0.35), run_time=0.8)

        self.at("a phosphate group")
        phos_circ = Circle(radius=0.58, stroke_color=OLD_COL, stroke_width=3.2, fill_color=OLD_COL, fill_opacity=0.46)
        phos_circ.move_to([-3.0, 0.90, 0])
        link_ps = Line(phos_circ.get_right() + DOWN * 0.10, sugar_shape.get_center() + LEFT * 1.15 + UP * 0.50,
                       color=OLD_COL, stroke_width=7.0)
        phos_lbl = T("phosphate", size=26, color=TEXT).next_to(phos_circ, UP, buff=0.16)
        self.play(FadeIn(phos_circ, shift=DR * 0.3), Create(link_ps), FadeIn(phos_lbl), run_time=0.7)

        self.at("and a base")
        base_rect = RoundedRectangle(corner_radius=0.12, width=2.4, height=1.30, stroke_color=TEXT, stroke_width=3.2,
                                     fill_color=TEAL, fill_opacity=0.30).move_to([3.10, -0.15, 0])
        link_sb = Line(sugar_shape.get_right() + LEFT * 0.08, base_rect.get_left(), color=OLD_COL, stroke_width=7.0)
        base_lbl = T("base", size=30, color=TEXT, weight=BOLD).move_to(base_rect)
        self.play(FadeIn(base_rect, shift=LEFT * 0.35), Create(link_sb), FadeIn(base_lbl), run_time=0.7)

        self.at("The base carries")
        self.play(FadeOut(ghost), base_rect.animate.set_stroke(GOLD, width=5.5), run_time=0.7)
        self.wait(0.6)
        self.play(base_rect.animate.set_stroke(TEXT, width=3.2), run_time=0.4)

        self.at("DNA uses")
        single = VGroup(sugar, phos_circ, phos_lbl, link_ps, base_rect, base_lbl, link_sb, title_nuc)
        self.play(FadeOut(single), run_time=0.35)

        xs = [-4.65, -1.55, 1.55, 4.65]
        bases = ["A", "T", "C", "G"]
        names = ["adenine", "thymine", "cytosine", "guanine"]
        row_nucs = VGroup()
        row_names = VGroup()
        for x, b, nm in zip(xs, bases, names):
            p = Circle(radius=0.34, stroke_color=OLD_COL, stroke_width=3.2, fill_color=OLD_COL, fill_opacity=0.46)
            p.move_to([x - 1.00, 1.25, 0])
            s = make_pentagon(w=1.12, h=0.92, color=OLD_COL, fill_op=0.42).move_to([x - 0.58, 0.15, 0])
            ln1 = Line(p.get_bottom() + RIGHT * 0.08, s.get_top() + LEFT * 0.24, color=OLD_COL, stroke_width=5.5)
            bm = make_base(b, dir_sign=1, w=1.22, h=0.72, font_size=32).move_to([x + 0.64, 0.15, 0])
            ln2 = Line(s.get_right(), bm.get_left(), color=OLD_COL, stroke_width=5.5)
            bm.poly.set_stroke(GREY, width=3.0).set_fill(GREY, opacity=0.24)
            bm.txt.set_opacity(0.0)
            nuc = VGroup(ln1, ln2, p, s, bm)
            nuc.bm = bm
            row_nucs.add(nuc)
            row_names.add(T(nm, size=30, color=BASE_COLORS[b], weight=BOLD).move_to([x, -1.25, 0]))

        self.play(FadeIn(row_nucs), run_time=0.45)

        for i, cue in enumerate(["adenine", "thymine", "cytosine", "guanine"]):
            self.at(cue, lead=0.15)
            b = bases[i]
            col = BASE_COLORS[b]
            bm = row_nucs[i].bm
            self.play(
                bm.poly.animate.set_stroke(col, width=3.5).set_fill(col, opacity=0.48),
                FadeIn(row_names[i], shift=UP * 0.14),
                run_time=0.42,
            )

        self.at("We write them")
        for i in range(4):
            self.play(row_nucs[i].bm.txt.animate.set_opacity(1.0), run_time=0.32)
        self.finish()


class S03Strand(SpokenScene):
    def construct(self):
        xs = [-4.65, -1.55, 1.55, 4.65]
        bases = ["A", "T", "C", "G"]
        nucs = VGroup()
        for x, b in zip(xs, bases):
            p = Circle(radius=0.24, stroke_color=OLD_COL, stroke_width=3.0, fill_color=OLD_COL, fill_opacity=0.46)
            p.move_to([x - 0.90, 0.96, 0])
            s = make_pentagon(w=0.84, h=0.66, color=OLD_COL, fill_op=0.42).move_to([x - 0.52, 0.0, 0])
            ln1 = Line(p.get_bottom() + RIGHT * 0.06, s.get_top() + LEFT * 0.18, color=OLD_COL, stroke_width=5.0)
            bm = make_base(b, dir_sign=1, w=1.06, h=0.58, font_size=28).move_to([x + 0.52, 0.0, 0])
            ln2 = Line(s.get_right(), bm.get_left(), color=OLD_COL, stroke_width=5.0)
            g = VGroup(ln1, ln2, p, s, bm)
            g.p, g.s, g.bm, g.ln1, g.ln2 = p, s, bm, ln1, ln2
            nucs.add(g)

        key = make_key(pos=(-4.8, -3.15, 0))
        self.add(nucs, key)

        self.at("Nucleotides join")
        # Arrange vertically with gaps so each bond visibly snaps together in the next beat
        ys_open = [2.10, 0.86, -0.78, -2.42]
        anims = []
        for nuc, y in zip(nucs, ys_open):
            target_p = np.array([-1.65, y + 0.44, 0.0])
            target_s = np.array([-1.65, y - 0.16, 0.0])
            target_bm = np.array([-0.62, y - 0.16, 0.0])
            anims.extend([
                nuc.p.animate.move_to(target_p),
                nuc.s.animate.move_to(target_s),
                nuc.bm.animate.move_to(target_bm),
                nuc.ln1.animate.put_start_and_end_on(target_p + DOWN * 0.24, target_s + UP * 0.33),
                nuc.ln2.animate.put_start_and_end_on(target_s + RIGHT * 0.42, target_bm + LEFT * 0.53),
            ])
        self.play(*anims, run_time=1.8)

        self.at("The sugar of one")
        # Slide nucleotides 2, 3, 4 smoothly upward to close each sugar-to-phosphate bond one by one
        ys = [2.10, 0.72, -0.66, -2.04]
        bonds = VGroup()
        for i in range(3):
            shift_up = UP * (ys[i + 1] - ys_open[i + 1])
            if i == 0:
                self.play(nucs[1].animate.shift(shift_up), run_time=0.85)
            elif i == 1:
                self.play(nucs[2].animate.shift(shift_up), run_time=0.85)
            else:
                self.play(nucs[3].animate.shift(shift_up), run_time=0.85)
            y_top = ys[i] - 0.16 - 0.33
            y_bot = ys[i + 1] + 0.44 + 0.24
            ln = Line([-1.65, y_top, 0], [-1.65, y_bot, 0], color=GOLD, stroke_width=8.0)
            bonds.add(ln)
            self.play(Create(ln), run_time=0.45)

        self.at("covalent bond")
        cov_lbl = boxed_label("covalent bond", color=GOLD, size=28, pad=0.18, fill_opacity=0.24).move_to([-4.35, 0.25, 0])
        cov_arr = Arrow(cov_lbl.get_right() + RIGHT * 0.08, bonds[1].get_center() + LEFT * 0.18,
                        buff=0.0, color=GOLD, stroke_width=3.5, max_tip_length_to_length_ratio=0.18)
        self.play(FadeIn(cov_lbl, shift=RIGHT * 0.15), Create(cov_arr), run_time=0.65)

        self.at("atoms share electrons")
        e_dots = VGroup()
        for b in bonds:
            c = b.get_center()
            e_dots.add(Dot(c + LEFT * 0.10, radius=0.08, color=TEAL), Dot(c + RIGHT * 0.10, radius=0.08, color=TEAL))
        self.play(FadeIn(e_dots, scale=1.4), run_time=0.5)
        self.play(Rotate(e_dots[0], PI, about_point=bonds[0].get_center()),
                  Rotate(e_dots[1], PI, about_point=bonds[0].get_center()),
                  Rotate(e_dots[2], PI, about_point=bonds[1].get_center()),
                  Rotate(e_dots[3], PI, about_point=bonds[1].get_center()),
                  Rotate(e_dots[4], PI, about_point=bonds[2].get_center()),
                  Rotate(e_dots[5], PI, about_point=bonds[2].get_center()),
                  run_time=1.35)

        bb_full = make_backbone_v(-1.65, 2.60, -2.70, arrow_dir=DOWN, color=OLD_COL, stroke_w=13.0)
        clean_bases = VGroup(*[
            make_base(b, dir_sign=1, w=1.06, h=0.58, font_size=28).move_to([-1.65 + 0.16 + 1.06 / 2.0, y - 0.16, 0.0])
            for b, y in zip(bases, ys)
        ])
        cnt = make_counter("strands: 1", pos=(-4.75, 3.22, 0), color=TEXT)
        self.play(
            FadeOut(VGroup(*[VGroup(n.p, n.s, n.ln1, n.ln2) for n in nucs])),
            FadeOut(bonds),
            FadeOut(e_dots),
            FadeOut(cov_lbl),
            FadeOut(cov_arr),
            ReplacementTransform(VGroup(*[n.bm for n in nucs]), clean_bases),
            FadeIn(bb_full),
            FadeIn(cnt, shift=DOWN * 0.1),
            run_time=0.9,
        )

        self.at("The bases stick out")
        for bm in clean_bases:
            self.play(bm.animate.shift(RIGHT * 0.28), run_time=0.24)
            self.play(bm.animate.shift(LEFT * 0.28), run_time=0.20)
        self.finish()


class S04Pairing(SpokenScene):
    def construct(self):
        seq = ["A", "T", "C", "G"]
        ys = [1.74, 0.58, -0.58, -1.74]
        left_strand = make_strand_v(seq, -1.62, base_dir=1, arrow_dir=DOWN, y_top=1.74, pitch=1.16,
                                  w=1.06, h=0.60, font_size=30, bb_color=OLD_COL)
        comp = [PAIR[b] for b in seq]
        right_strand = make_strand_v(comp, 4.5, base_dir=-1, arrow_dir=UP, y_top=1.74, pitch=1.16,
                                   w=1.06, h=0.60, font_size=30, bb_color=OLD_COL)
        cnt = make_counter("strands: 1", pos=(-4.75, 3.22, 0), color=TEXT)
        key = make_key(pos=(-4.8, -3.15, 0))
        self.add(left_strand, cnt, key)

        self.at("a second strand")
        self.play(FadeIn(right_strand, shift=LEFT * 0.6), run_time=0.7)
        self.play(right_strand.animate.shift(LEFT * 2.2), run_time=1.0)

        self.at("bases facing bases")
        cnt2 = make_counter("strands: 2", pos=(-4.75, 3.22, 0), color=TEXT)
        self.play(
            left_strand.animate.shift(RIGHT * 0.18),
            right_strand.animate.shift(LEFT * 0.52),
            swap(cnt, cnt2, run_time=0.6),
            run_time=0.9,
        )

        self.at("hydrogen bonds")
        hbonds = VGroup(*[make_hbonds_v(-0.26, 0.58, y) for y in ys])
        hb_lbl = boxed_label("hydrogen bonds", color=TEXT, size=26, pad=0.16).move_to([0.16, 2.98, 0])
        hb_arr = Arrow(hb_lbl.get_bottom() + DOWN * 0.06, [0.16, 1.94, 0],
                       buff=0.0, color=TEXT, stroke_width=2.8, max_tip_length_to_length_ratio=0.22)
        self.play(FadeIn(hb_lbl, shift=DOWN * 0.1), Create(hb_arr), run_time=0.6)
        for hb in hbonds:
            self.play(Create(hb), run_time=0.6)

        self.at("only two kinds")
        self.play(
            FadeOut(hb_lbl),
            FadeOut(hb_arr),
            left_strand.animate.shift(RIGHT * 0.24),
            right_strand.animate.shift(LEFT * 0.44),
            *[hb.animate.shift(LEFT * 0.10).stretch(0.20, dim=0) for hb in hbonds],
            run_time=1.0,
        )

        self.at("A fits with T")
        at_tag = boxed_label("A with T", color=BLUE, size=26, pad=0.14).move_to([3.95, 1.16, 0])
        self.play(
            FadeIn(at_tag, shift=LEFT * 0.15),
            left_strand.bases[0].animate.shift(RIGHT * 0.02),
            right_strand.bases[0].animate.shift(LEFT * 0.02),
            left_strand.bases[1].animate.shift(RIGHT * 0.02),
            right_strand.bases[1].animate.shift(LEFT * 0.02),
            run_time=0.8,
        )

        self.at("C fits with G")
        cg_tag = boxed_label("C with G", color=GREEN, size=26, pad=0.14).move_to([3.95, -1.16, 0])
        self.play(
            FadeIn(cg_tag, shift=LEFT * 0.15),
            left_strand.bases[2].animate.shift(RIGHT * 0.02),
            right_strand.bases[2].animate.shift(LEFT * 0.02),
            left_strand.bases[3].animate.shift(RIGHT * 0.02),
            right_strand.bases[3].animate.shift(LEFT * 0.02),
            run_time=0.8,
        )
        self.finish()


class S05Misfit(SpokenScene):
    def construct(self):
        key = make_key(pos=(-4.8, -3.15, 0))
        self.add(key)

        big_w, big_h, big_fs = 2.05, 1.04, 42
        a_blk = make_base("A", dir_sign=1, w=big_w, h=big_h, font_size=big_fs, stroke_w=3.5).move_to([-2.4, 0.78, 0])
        c_blk = make_base("C", dir_sign=-1, w=big_w, h=big_h, font_size=big_fs, stroke_w=3.5).move_to([2.4, 0.78, 0])
        self.play(FadeIn(a_blk, shift=RIGHT * 0.3), FadeIn(c_blk, shift=LEFT * 0.3), run_time=0.65)

        self.at("meet C")
        self.play(a_blk.animate.move_to([-1.28, 0.78, 0]), c_blk.animate.move_to([1.28, 0.78, 0]), run_time=0.85)

        self.at("Their edges do not match")
        bad_x = VGroup(
            Line([-0.22, 1.00, 0], [0.22, 0.56, 0], color=RED, stroke_width=6.0),
            Line([-0.22, 0.56, 0], [0.22, 1.00, 0], color=RED, stroke_width=6.0),
        )
        mis_lbl = T("poor fit", size=28, color=RED, weight=BOLD).move_to([0.0, 1.78, 0])
        self.play(Create(bad_x), FadeIn(mis_lbl, shift=DOWN * 0.1), run_time=0.55)

        self.at("fit badly")
        self.play(FadeOut(bad_x), FadeOut(mis_lbl), c_blk.animate.move_to([4.5, 0.78, 0]).set_opacity(0.0), run_time=0.85)
        self.remove(c_blk)

        self.at("That is the")
        t_blk = make_base("T", dir_sign=-1, w=big_w, h=big_h, font_size=big_fs, stroke_w=3.5).move_to([3.8, 0.78, 0])
        self.play(FadeIn(t_blk, shift=LEFT * 0.4), run_time=0.6)

        self.at("A always pairs with T")
        self.play(a_blk.animate.move_to([-1.10, 0.78, 0]), t_blk.animate.move_to([1.10, 0.78, 0]), run_time=0.8)
        hb_top = make_hbonds_v(-0.18, 0.18, 0.78)
        self.play(Create(hb_top), run_time=0.35)

        self.at("C always pairs with G")
        c2 = make_base("C", dir_sign=1, w=big_w, h=big_h, font_size=big_fs, stroke_w=3.5).move_to([-3.2, -0.78, 0])
        g2 = make_base("G", dir_sign=-1, w=big_w, h=big_h, font_size=big_fs, stroke_w=3.5).move_to([3.2, -0.78, 0])
        self.play(FadeIn(c2), FadeIn(g2), run_time=0.3)
        self.play(c2.animate.move_to([-1.10, -0.78, 0]), g2.animate.move_to([1.10, -0.78, 0]), run_time=0.65)
        hb_bot = make_hbonds_v(-0.18, 0.18, -0.78)
        rule = caption("A with T,   C with G", color=GOLD, size=32, y=-2.85)
        rule.move_to([0.0, -2.85, 0])
        self.play(Create(hb_bot), FadeIn(rule, shift=UP * 0.15), run_time=0.55)
        self.finish()


class S06Helix(SpokenScene):
    def construct(self):
        lad = make_ladder_v(SEQ_6, cx=0.0, y_top=2.0, pitch=0.78, w=0.96, h=0.49, font_size=26)
        key = make_key(pos=(-4.8, -3.15, 0))
        tag = scope_tag("schematic")
        self.add(lad, key, tag)

        self.at("Notice the two arrowheads")
        ah_l = lad.left.bb.head
        ah_r = lad.right.bb.head
        self.play(ah_l.animate.scale(1.4).set_color(GOLD), ah_r.animate.scale(1.4).set_color(GOLD), run_time=0.8)
        self.play(ah_l.animate.scale(1.0 / 1.4).set_color(OLD_COL), ah_r.animate.scale(1.0 / 1.4).set_color(OLD_COL), run_time=0.8)

        self.at("Each strand has")
        x_l = lad.left.bb.get_center()[0]
        x_r = lad.right.bb.get_center()[0]
        y_hi, y_lo = 2.0, -2.0
        prog = ValueTracker(0.0)
        pulse_l = always_redraw(lambda: Line(
            [x_l, y_hi - prog.get_value() * 3.1, 0],
            [x_l, y_hi - prog.get_value() * 3.1 - 0.9, 0],
            color=GOLD, stroke_width=18.0,
        ))
        pulse_r = always_redraw(lambda: Line(
            [x_r, y_lo + prog.get_value() * 3.1, 0],
            [x_r, y_lo + prog.get_value() * 3.1 + 0.9, 0],
            color=GOLD, stroke_width=18.0,
        ))
        dir_l = always_redraw(lambda: boxed_label("↓", color=GOLD, size=30, pad=0.12, fill_opacity=0.28).move_to(
            [x_l - 0.62, y_hi - prog.get_value() * 3.6 - 0.2, 0]
        ))
        dir_r = always_redraw(lambda: boxed_label("↑", color=GOLD, size=30, pad=0.12, fill_opacity=0.28).move_to(
            [x_r + 0.62, y_lo + prog.get_value() * 3.6 + 0.2, 0]
        ))
        self.add(pulse_l, pulse_r, dir_l, dir_r)
        self.play(prog.animate.set_value(1.0), run_time=2.3, rate_func=linear)

        self.at("point opposite ways")
        prog.set_value(0.0)
        self.play(prog.animate.set_value(1.0), run_time=2.3, rate_func=linear)
        self.remove(pulse_l, pulse_r, dir_l, dir_r)

        self.at("the ladder twists")
        twist = ValueTracker(0.0)
        ys_bb = np.linspace(-2.55, 2.55, 72)
        half_w = 1.60
        rung_ys = [2.0 - i * 0.78 for i in range(6)]
        rung_pairs = [(b, PAIR[b]) for b in SEQ_6]

        def build_helix():
            th_max = twist.get_value() * 1.45 * PI
            if th_max < 0.04:
                return lad.copy()
            k = th_max / 5.10
            pts1, pts2 = [], []
            for y in ys_bb:
                ang = k * (y + 2.55)
                pts1.append([-half_w * np.cos(ang), y, 0.0])
                pts2.append([half_w * np.cos(ang), y, 0.0])
            s1 = VMobject(stroke_color=OLD_COL, stroke_width=13.0).set_points_as_corners(pts1)
            s2 = VMobject(stroke_color=OLD_COL, stroke_width=13.0).set_points_as_corners(pts2)
            rungs_g = VGroup()
            for y, (lb, rb) in zip(rung_ys, rung_pairs):
                ang = k * (y + 2.55)
                x1 = -half_w * np.cos(ang)
                x2 = half_w * np.cos(ang)
                l_bar = Line([x1, y, 0], [0.0, y, 0], color=BASE_COLORS[lb], stroke_width=15.0)
                r_bar = Line([0.0, y, 0], [x2, y, 0], color=BASE_COLORS[rb], stroke_width=15.0)
                rungs_g.add(l_bar, r_bar)
            a1 = Triangle(color=OLD_COL, fill_color=OLD_COL, fill_opacity=1.0).scale(0.18).rotate(PI).move_to(pts1[0])
            a2 = Triangle(color=OLD_COL, fill_color=OLD_COL, fill_opacity=1.0).scale(0.18).move_to(pts2[-1])
            return VGroup(rungs_g, s1, s2, a1, a2)

        helix = always_redraw(build_helix)
        self.remove(lad)
        self.add(helix)
        self.play(twist.animate.set_value(1.0), run_time=2.6, rate_func=smooth)

        self.at("The backbones are the sides")
        sides_lbl = boxed_label("sides (backbones)", color=OLD_COL, size=26, pad=0.14).move_to([-4.25, 1.2, 0])
        sides_lbl.label.set_color(TEXT)
        sides_arr = Arrow(sides_lbl.get_right() + RIGHT * 0.08, [-1.72, 1.2, 0], buff=0.0, color=OLD_COL, stroke_width=3.0)
        self.play(FadeIn(sides_lbl, shift=RIGHT * 0.15), Create(sides_arr), run_time=0.65)

        self.at("the base pairs are the rungs", lead=0.95)
        rungs_lbl = boxed_label("rungs (base pairs)", color=GOLD, size=26, pad=0.14).move_to([4.15, 0.44, 0])
        rungs_arr = Arrow(rungs_lbl.get_left() + LEFT * 0.08, [0.55, 0.44, 0], buff=0.0, color=GOLD, stroke_width=3.0)
        self.play(FadeIn(rungs_lbl, shift=LEFT * 0.15), Create(rungs_arr), run_time=0.50)
        self.wait(1.60)
        self.play(
            FadeOut(sides_lbl), FadeOut(sides_arr),
            FadeOut(rungs_lbl), FadeOut(rungs_arr),
            twist.animate.set_value(0.0),
            run_time=0.70,
            rate_func=smooth,
        )
        self.finish()


def build_predict_backdrop():
    """Shared builder for s07_predict end state and s08_pause backdrop."""
    left = make_strand_v(SEQ_6, -1.56, base_dir=1, arrow_dir=DOWN, y_top=2.2, pitch=0.72,
                         w=0.98, h=0.49, font_size=26, bb_color=OLD_COL)
    slots = VGroup(*[make_empty_slot(w=0.98, h=0.49, font_size=26).move_to([0.92, y, 0]) for y in left.ys])
    pencil = make_pencil(pos=(2.85, 0.4, 0))
    key = make_key(pos=(-4.8, -3.15, 0))
    return VGroup(left, slots, pencil, key), left, slots, pencil


class S07Predict(SpokenScene):
    def construct(self):
        backdrop, left, slots, pencil = build_predict_backdrop()
        self.add(left, backdrop[3])
        self.play(FadeIn(slots), run_time=1.6)

        self.at("It reads")
        for b in left.bases:
            self.play(b.poly.animate.set_stroke(GOLD, width=4.2), run_time=0.24)
            self.play(b.poly.animate.set_stroke(BASE_COLORS[b.letter], width=3.0), run_time=0.14)

        self.at("Before I fill")
        q = question_card("Write the partner strand (top to bottom).", y=-3.05, size=28, max_w=8.2)
        q.move_to([0.45, -3.05, 0])
        self.play(FadeIn(pencil, shift=DOWN * 0.2), FadeIn(q, shift=UP * 0.15), run_time=0.7)

        self.at("write the")
        self.play(pencil.animate.move_to([2.45, left.ys[0], 0]), run_time=0.75)
        self.play(pencil.animate.move_to([2.85, 0.4, 0]), run_time=0.85)
        self.finish()


class S08Pause(PredictPause):
    QUESTION = "Write the partner strand (top to bottom)."
    CARD = {"y": -3.05, "size": 28, "max_w": 8.2}
    RING_AT = (5.70, -2.85, 0)
    SECONDS = 5.0

    def backdrop(self):
        bd, _, _, _ = build_predict_backdrop()
        return bd

    def construct(self):
        bd = self.backdrop()
        pencil = bd[2]
        q = question_card(self.QUESTION, y=-3.05, size=28, max_w=8.2).move_to([0.45, -3.05, 0])
        c = np.array(self.RING_AT, dtype=float)
        rem = ValueTracker(self.SECONDS)
        bg = Circle(radius=0.58, color=GREY, stroke_width=6).move_to(c).set_opacity(0.45)
        arc = always_redraw(lambda: Arc(
            radius=0.58,
            start_angle=PI / 2,
            angle=max(rem.get_value() / self.SECONDS, 0.001) * TAU,
            color=GOLD,
            stroke_width=12,
            arc_center=c,
        ))
        num = always_redraw(lambda: M(f"{max(1, int(np.ceil(rem.get_value())))}", size=28, color=TEXT).move_to(c))
        self.add(bd, q, bg, arc, num)
        bob(pencil, amp=0.06, speed=3.2)
        self.play(rem.animate.set_value(0.0), run_time=self.SECONDS, rate_func=linear)
        self.finish()


class S09Reveal(SpokenScene):
    def construct(self):
        bd, left, slots, pencil = build_predict_backdrop()
        self.add(bd)

        partner = [PAIR[b] for b in SEQ_6]
        new_bases = VGroup(*[
            make_base(b, dir_sign=-1, w=0.98, h=0.49, font_size=26).move_to([0.38, y, 0])
            for b, y in zip(partner, left.ys)
        ])

        self.at("across from G goes C")
        self.play(
            FadeOut(slots[0]),
            FadeIn(new_bases[0], shift=LEFT * 0.4),
            pencil.animate.move_to([2.85, left.ys[1], 0]),
            run_time=1.1,
        )

        self.at("across from a goes T")
        self.play(
            FadeOut(slots[1]),
            FadeIn(new_bases[1], shift=LEFT * 0.4),
            pencil.animate.move_to([2.85, left.ys[2], 0]),
            run_time=1.1,
        )

        self.at("So the partner reads")
        for idx in range(2, 6):
            self.play(
                FadeOut(slots[idx]),
                FadeIn(new_bases[idx], shift=LEFT * 0.35),
                pencil.animate.move_to([2.85, left.ys[min(idx + 1, 5)], 0]),
                run_time=0.65,
            )

        right_bb = make_backbone_v(1.04, left.ys[0] + 0.35, left.ys[-1] - 0.35, arrow_dir=UP, color=OLD_COL)
        self.play(FadeOut(pencil), FadeIn(right_bb), run_time=0.55)

        self.at("Not one letter")
        hbonds = VGroup(*[make_hbonds_v(-0.42, -0.06, y) for y in left.ys])
        for hb in hbonds:
            self.play(Create(hb), run_time=0.30)

        self.at("One strand fixed")
        pair_group = VGroup(left, new_bases, right_bb, hbonds)
        br = Brace(pair_group, RIGHT, buff=0.22, color=TEXT)
        lbl = fit_text("one strand fixes its partner", max_w=3.2, size=28, color=GOLD, max_lines=2)
        lbl.next_to(br, RIGHT, buff=0.20)
        self.play(GrowFromCenter(br), FadeIn(lbl, shift=RIGHT * 0.15), run_time=1.0)
        self.finish()


class S10Unzip(SpokenScene):
    def construct(self):
        # 10-rung grey ladder: wider bb_gap=0.26 + smooth Y-transition W=2.10 keeps backbone clear of all base boxes in motion
        y_top, pitch, w, h, fs = 2.25, 0.50, 0.88, 0.42, 24
        half_sep, bb_gap = 0.48, 0.26
        lad = make_ladder_v(SEQ_10, cx=0.0, y_top=y_top, pitch=pitch, w=w, h=h, font_size=fs,
                            half_sep=half_sep, bb_gap=bb_gap)
        key = make_key(pos=(-4.8, -3.18, 0))
        self.add(lad, key)

        self.at("copies DNA")
        self.play(lad.left.bb.head.animate.set_color(TEXT), lad.right.bb.head.animate.set_color(TEXT), run_time=0.45)
        self.play(lad.left.bb.head.animate.set_color(OLD_COL), lad.right.bb.head.animate.set_color(OLD_COL), run_time=0.45)

        self.at("Enzymes unzip")
        wedge = Polygon(
            [-0.78, 0.52, 0], [0.78, 0.52, 0], [0.78, 0.04, 0], [0.0, -0.58, 0], [-0.78, 0.04, 0],
            stroke_color=TEAL, stroke_width=3.2, fill_color=TEAL, fill_opacity=0.42,
        )
        enz_lbl = T("enzyme", size=22, color=TEXT, weight=BOLD).move_to([0.0, 0.25, 0])
        enzyme = VGroup(wedge, enz_lbl).move_to([0.0, 2.85, 0])

        enz_y = ValueTracker(2.85)
        enzyme.add_updater(lambda m: m.move_to([0.0, enz_y.get_value(), 0.0]))
        self.play(FadeIn(enzyme), run_time=0.35)

        left_bases_x0 = [b.get_center()[0] for b in lad.left.bases]
        right_bases_x0 = [b.get_center()[0] for b in lad.right.bases]
        bb_l_x0 = lad.left.bb.get_center()[0]
        bb_r_x0 = lad.right.bb.get_center()[0]
        sep = 2.30
        W_bend = 2.10

        def sep_frac(y_val):
            return float(np.clip((y_val + 0.70 - enz_y.get_value()) / W_bend, 0.0, 1.0))

        self.remove(lad.left.bb, lad.right.bb)
        ys_sample = np.linspace(2.49, -2.49, 60)

        def mk_fork_bb(x0, sign, arrow_dir):
            pts = [[x0 + sign * sep * sep_frac(y), y, 0.0] for y in ys_sample]
            line = VMobject(stroke_color=OLD_COL, stroke_width=12.0).set_points_as_corners(pts)
            if np.allclose(arrow_dir, DOWN):
                tip = pts[-1]
                head = Polygon([tip[0] - 0.18, tip[1] + 0.20, 0], [tip[0] + 0.18, tip[1] + 0.20, 0],
                               [tip[0], tip[1] - 0.16, 0], stroke_width=0, fill_color=OLD_COL, fill_opacity=1.0)
            else:
                tip = pts[0]
                head = Polygon([tip[0] - 0.18, tip[1] - 0.20, 0], [tip[0] + 0.18, tip[1] - 0.20, 0],
                               [tip[0], tip[1] + 0.16, 0], stroke_width=0, fill_color=OLD_COL, fill_opacity=1.0)
            return VGroup(line, head)

        dyn_bb_l = always_redraw(lambda: mk_fork_bb(bb_l_x0, -1.0, DOWN))
        dyn_bb_r = always_redraw(lambda: mk_fork_bb(bb_r_x0, 1.0, UP))
        self.add(dyn_bb_l, dyn_bb_r)

        for i, y in enumerate(lad.left.ys):
            lad.left.bases[i].add_updater(lambda m, idx=i, y0=y, x0=left_bases_x0[i]: m.move_to([x0 - sep * sep_frac(y0), y0, 0.0]))
            lad.right.bases[i].add_updater(lambda m, idx=i, y0=y, x0=right_bases_x0[i]: m.move_to([x0 + sep * sep_frac(y0), y0, 0.0]))
            lad.hbonds[i].add_updater(lambda m, y0=y: m.set_opacity(max(0.0, 1.0 - 3.5 * sep_frac(y0))))

        self.play(enz_y.animate.set_value(-3.20), run_time=2.0, rate_func=linear)

        for i, y in enumerate(lad.left.ys):
            lad.left.bases[i].clear_updaters()
            lad.right.bases[i].clear_updaters()
            lad.hbonds[i].clear_updaters()
            lad.left.bases[i].move_to([left_bases_x0[i] - sep, y, 0.0])
            lad.right.bases[i].move_to([right_bases_x0[i] + sep, y, 0.0])
        self.remove(lad.hbonds, dyn_bb_l, dyn_bb_r)
        enzyme.clear_updaters()

        final_bb_l = make_backbone_v(bb_l_x0 - sep, y_top + pitch * 0.48, lad.left.ys[-1] - pitch * 0.48,
                                     arrow_dir=DOWN, color=OLD_COL, stroke_w=12.0)
        final_bb_r = make_backbone_v(bb_r_x0 + sep, y_top + pitch * 0.48, lad.right.ys[-1] - pitch * 0.48,
                                     arrow_dir=UP, color=OLD_COL, stroke_w=12.0)
        self.add(final_bb_l, final_bb_r)

        self.at("each old strand")
        tmpl_l = boxed_label("template", color=OLD_COL, size=26, pad=0.12).move_to([bb_l_x0 - sep + 0.60, 3.04, 0])
        tmpl_r = boxed_label("template", color=OLD_COL, size=26, pad=0.12).move_to([bb_r_x0 + sep - 0.60, 3.04, 0])
        tmpl_l.label.set_color(TEXT)
        tmpl_r.label.set_color(TEXT)
        self.play(FadeOut(enzyme), FadeIn(tmpl_l, shift=DOWN * 0.1), FadeIn(tmpl_r, shift=DOWN * 0.1), run_time=0.6)

        self.at("A template is a pattern")
        cap = caption("template: a pattern that sets the new strand", size=28, color=TEXT, y=-3.15)
        cap.move_to([0.6, -3.15, 0])
        self.play(FadeIn(cap, shift=UP * 0.1), run_time=0.5)
        for i in range(10):
            self.play(
                lad.left.bases[i].poly.animate.set_stroke(GOLD, width=3.8),
                lad.right.bases[i].poly.animate.set_stroke(GOLD, width=3.8),
                run_time=0.16,
            )
            self.play(
                lad.left.bases[i].poly.animate.set_stroke(BASE_COLORS[lad.left.bases[i].letter], width=3.0),
                lad.right.bases[i].poly.animate.set_stroke(BASE_COLORS[lad.right.bases[i].letter], width=3.0),
                run_time=0.11,
            )
        self.finish()


class S11Two(SpokenScene):
    def construct(self):
        y_top, pitch, w, h, fs = 2.25, 0.50, 0.88, 0.42, 24
        left_tmpl = make_strand_v(SEQ_10, -3.90, base_dir=1, arrow_dir=DOWN, y_top=y_top, pitch=pitch,
                                  w=w, h=h, font_size=fs, bb_color=OLD_COL, bb_gap=0.18)
        comp_10 = [PAIR[b] for b in SEQ_10]
        right_tmpl = make_strand_v(comp_10, 3.90, base_dir=-1, arrow_dir=UP, y_top=y_top, pitch=pitch,
                                   w=w, h=h, font_size=fs, bb_color=OLD_COL, bb_gap=0.18)

        cnt = make_counter("molecules: 1", pos=(-4.75, 3.22, 0), color=TEXT)
        key = make_key(pos=(-4.8, -3.18, 0))
        self.add(left_tmpl, right_tmpl, cnt, key)

        new_l_bases = VGroup(*[
            make_base(PAIR[b], dir_sign=-1, w=w, h=h, font_size=fs).move_to([-2.32, y, 0])
            for b, y in zip(SEQ_10, left_tmpl.ys)
        ])
        new_r_bases = VGroup(*[
            make_base(b, dir_sign=1, w=w, h=h, font_size=fs).move_to([2.32, y, 0])
            for b, y in zip(SEQ_10, right_tmpl.ys)
        ])
        new_l_bb = make_backbone_v(-1.72, left_tmpl.ys[0] + pitch * 0.48, left_tmpl.ys[-1] - pitch * 0.48,
                                   arrow_dir=UP, color=NEW_COL)
        new_r_bb = make_backbone_v(1.72, right_tmpl.ys[0] + pitch * 0.48, right_tmpl.ys[-1] - pitch * 0.48,
                                   arrow_dir=DOWN, color=NEW_COL)

        self.at("New nucleotides line up")
        for i in range(5):
            nb_l, nb_r = new_l_bases[i], new_r_bases[i]
            tgt_l, tgt_r = nb_l.get_center().copy(), nb_r.get_center().copy()
            nb_l.move_to([-0.55, tgt_l[1], 0])
            nb_r.move_to([0.55, tgt_r[1], 0])
            self.play(FadeIn(nb_l), FadeIn(nb_r), run_time=0.12)
            self.play(nb_l.animate.move_to(tgt_l), nb_r.animate.move_to(tgt_r), run_time=0.38)

        self.at("matching the base")
        for i in range(5, 10):
            nb_l, nb_r = new_l_bases[i], new_r_bases[i]
            tgt_l, tgt_r = nb_l.get_center().copy(), nb_r.get_center().copy()
            nb_l.move_to([-0.55, tgt_l[1], 0])
            nb_r.move_to([0.55, tgt_r[1], 0])
            self.play(FadeIn(nb_l), FadeIn(nb_r), run_time=0.10)
            self.play(nb_l.animate.move_to(tgt_l), nb_r.animate.move_to(tgt_r), run_time=0.35)

        self.at("When copying ends")
        self.play(Create(new_l_bb), Create(new_r_bb), run_time=0.7)

        self.at("two molecules")
        mol_l = VGroup(left_tmpl, new_l_bases, new_l_bb)
        mol_r = VGroup(right_tmpl, new_r_bases, new_r_bb)
        cnt2 = make_counter("molecules: 2 (each 1 old + 1 new)", pos=(-3.75, 3.25, 0), color=GOLD)
        self.play(
            mol_l.animate.shift(LEFT * 0.35),
            mol_r.animate.shift(RIGHT * 0.35),
            swap(cnt, cnt2, run_time=0.7),
            run_time=0.95,
        )

        self.at("one old gray strand")
        old_tag = boxed_label("old (grey)", color=OLD_COL, size=26, pad=0.14).move_to([0.0, 1.35, 0])
        old_tag.label.set_color(TEXT)
        self.play(
            FadeIn(old_tag, shift=UP * 0.1),
            left_tmpl.bb.line.animate.set_stroke(TEXT, width=18.0),
            right_tmpl.bb.line.animate.set_stroke(TEXT, width=18.0),
            left_tmpl.bb.head.animate.set_fill(TEXT, opacity=1.0),
            right_tmpl.bb.head.animate.set_fill(TEXT, opacity=1.0),
            run_time=0.65,
        )
        self.play(
            left_tmpl.bb.line.animate.set_stroke(OLD_COL, width=13.0),
            right_tmpl.bb.line.animate.set_stroke(OLD_COL, width=13.0),
            left_tmpl.bb.head.animate.set_fill(OLD_COL, opacity=1.0),
            right_tmpl.bb.head.animate.set_fill(OLD_COL, opacity=1.0),
            run_time=0.55,
        )

        self.at("one new gold strand")
        new_tag = boxed_label("new (gold)", color=NEW_COL, size=26, pad=0.14).move_to([0.0, 0.35, 0])
        self.play(
            FadeIn(new_tag, shift=UP * 0.1),
            new_l_bb.line.animate.set_stroke(TEXT, width=18.0),
            new_r_bb.line.animate.set_stroke(TEXT, width=18.0),
            new_l_bb.head.animate.set_fill(TEXT, opacity=1.0),
            new_r_bb.head.animate.set_fill(TEXT, opacity=1.0),
            run_time=0.65,
        )
        self.play(
            new_l_bb.line.animate.set_stroke(NEW_COL, width=13.0),
            new_r_bb.line.animate.set_stroke(NEW_COL, width=13.0),
            new_l_bb.head.animate.set_fill(NEW_COL, opacity=1.0),
            new_r_bb.head.animate.set_fill(NEW_COL, opacity=1.0),
            run_time=0.55,
        )

        self.at("Both carry the same")
        chk = boxed_label("✓  identical", color=GREEN, size=28, pad=0.14, fill_opacity=0.22).move_to([0.0, -0.75, 0])
        self.play(FadeIn(chk, shift=UP * 0.1), run_time=0.35)
        # Moving rung highlight frames comparing Molecule 1 and Molecule 2 pair by pair
        f_l = SurroundingRectangle(VGroup(left_tmpl.bases[0], new_l_bases[0]), color=GREEN, stroke_width=3.5, buff=0.04, corner_radius=0.06)
        f_r = SurroundingRectangle(VGroup(new_r_bases[0], right_tmpl.bases[0]), color=GREEN, stroke_width=3.5, buff=0.04, corner_radius=0.06)
        self.play(FadeIn(f_l), FadeIn(f_r), run_time=0.25)
        for i in range(1, 10):
            self.play(
                f_l.animate.move_to(VGroup(left_tmpl.bases[i], new_l_bases[i])),
                f_r.animate.move_to(VGroup(new_r_bases[i], right_tmpl.bases[i])),
                run_time=0.22,
            )
        self.finish()


class S12Rule(SpokenScene):
    def construct(self):
        y_top, pitch, w, h, fs = 2.25, 0.50, 0.88, 0.42, 24
        left_tmpl = make_strand_v(SEQ_10, -4.25, base_dir=1, arrow_dir=DOWN, y_top=y_top, pitch=pitch,
                                  w=w, h=h, font_size=fs, bb_color=OLD_COL, bb_gap=0.18)
        comp_10 = [PAIR[b] for b in SEQ_10]
        new_l_bases = VGroup(*[
            make_base(PAIR[b], dir_sign=-1, w=w, h=h, font_size=fs).move_to([-2.67, y, 0])
            for b, y in zip(SEQ_10, left_tmpl.ys)
        ])
        new_l_bb = make_backbone_v(-2.07, left_tmpl.ys[0] + pitch * 0.48, left_tmpl.ys[-1] - pitch * 0.48,
                                   arrow_dir=UP, color=NEW_COL)

        right_tmpl = make_strand_v(comp_10, 4.25, base_dir=-1, arrow_dir=UP, y_top=y_top, pitch=pitch,
                                   w=w, h=h, font_size=fs, bb_color=OLD_COL, bb_gap=0.18)
        new_r_bases = VGroup(*[
            make_base(b, dir_sign=1, w=w, h=h, font_size=fs).move_to([2.67, y, 0])
            for b, y in zip(SEQ_10, right_tmpl.ys)
        ])
        new_r_bb = make_backbone_v(2.07, right_tmpl.ys[0] + pitch * 0.48, right_tmpl.ys[-1] - pitch * 0.48,
                                   arrow_dir=DOWN, color=NEW_COL)

        mol_l = VGroup(left_tmpl, new_l_bases, new_l_bb)
        mol_r = VGroup(right_tmpl, new_r_bases, new_r_bb)
        lbl_l = T("1 old + 1 new", size=24, color=GOLD).next_to(mol_l, DOWN, buff=0.20)
        lbl_r = T("1 old + 1 new", size=24, color=GOLD).next_to(mol_r, DOWN, buff=0.20)
        self.add(mol_l, mol_r, lbl_l, lbl_r)

        rule1 = boxed_label("A with T\nC with G", color=GOLD, size=34, pad=0.24, fill_opacity=0.24).move_to([0.0, 0.35, 0])
        self.play(FadeIn(rule1, scale=0.92), run_time=0.8)

        self.at("only with T")
        self.play(rule1.box.animate.set_stroke(BLUE, width=4.5), run_time=0.6)

        self.at("C only with G")
        self.play(rule1.box.animate.set_stroke(GREEN, width=4.5), run_time=0.6)

        self.at("each strand fixes its partner")
        rule2 = boxed_label("each strand\nfixes its partner", color=TEAL, size=32, pad=0.24, fill_opacity=0.24).move_to([0.0, 0.35, 0])
        self.play(swap(rule1, rule2, run_time=0.8), run_time=0.8)

        self.at("Pairing does not yet explain")
        acc_w = T("accuracy", size=30, color=TEXT, weight=BOLD)
        acc_q = T("?", size=34, color=OLD_COL, weight=BOLD)
        acc = VGroup(acc_w, acc_q).arrange(RIGHT, buff=0.18).move_to([0.0, -2.05, 0])
        self.play(FadeIn(acc, shift=UP * 0.15), run_time=0.7)

        self.at("almost every letter right")
        self.play(acc_q.animate.set_color(GOLD), run_time=0.5)
        self.wait(0.8)
        self.play(FadeOut(acc), run_time=0.5)
        self.finish()


class S13End(EndCard):
    LINE = "Each strand fixes its partner,\nso either can restore the whole molecule."
