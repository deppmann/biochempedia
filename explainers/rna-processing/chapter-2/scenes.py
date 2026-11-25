"""
RNA Processing — Chapter 2: "When the Joins Change"

COLOUR MAP (identical to Chapter 1 so the pair reads as one film):
  BLUE = retained exons and the processed message
  RED  = introns that leave (or are abnormally retained)
  GOLD = added end marks (5' cap, 3' poly(A) tail) and affected/shifted downstream codons or reacting exon edges
  TEAL = recognition signals, spliceosome guides, and competing join arcs
  GREY = DNA/gene structure, neutral frames, axis/ruler ticks, and scope tags
  (Outside the colour map: WHITE outline marks the single invented exon under test in s06/s09; GREEN marks the aligned downstream frame in s08.)

CARRIED WORLD:
  A horizontal eukaryotic transcript strip (5' cap on left, exons, introns when unspliced, 3' poly(A) tail on right)
  positioned in the upper-middle stage, paired below with a computed nucleotide/codon triplet ruler whose 3-base
  boxes are derived directly from cumulative coding nucleotide counts (divisible by 3 vs remainder 1).

WHAT CHANGES IN EACH SPOKEN SCENE (and what it is computed from):
  s00_link:     Finished capped/tailed mRNA pulses at its BLUE exon joins; a fresh pre-mRNA copy with RED introns builds below it while TEAL signals and a reading-frame '?' strip appear.
  s01_title:    Title 'When the Joins Change' fades in above the carried pre-mRNA while two TEAL possible join arcs trace above it.
  s02_patterns: One centered pre-mRNA transforms sequentially through exon skipping, splice-site shift, mutually exclusive exon swap, and intron retention, adding each resulting mRNA to a right-hand stack.
  s03_variant:  A weakened TEAL normal splice site dims while two nearby cryptic TEAL sites brighten and competing join arcs pulse, then the transcript branches into three schematic product lanes ('skip (most often)', 'cryptic site', 'retain').
  s04_evidence: A 'studied beta-thalassemia allele' block feeds two schematic lanes whose widths grow into a wider 'main product' lane (short RED intron piece retained) and a narrower 'smaller amount' lane (non-adjacent exons joined).
  s05_ruler:    A computed triplet ruler (3 nucleotides per codon box) reveals under the BLUE coding message; a reading marker steps across codons, then exon 2 loses 1 base and downstream codon boxes slide 1 nt left and turn GOLD.
  s06_predict:  A computed 12-nt (4 complete triplet boxes) BLUE exon receives a bright WHITE outline and hovers above a 12-nt gap while the triplet ruler highlights the exact 4-box span and poses the question.
  s07_pause:    Holds the lifted 12-nt exon, gap, triplet ruler, and question card while the 4.5 s countdown ring empties.
  s08_reveal:   The WHITE-outlined 12-nt exon exits and the downstream BLUE exon slides left by 12 nt so its codons lock onto the fixed triplet ruler grid, marked by a GREEN 'aligned' bracket and a pulsing junction '?'.
  s09_shift:    Transcript resets with a WHITE-outlined 10-nt exon (computed as 3 full triplet boxes + 1 leftover WHITE-outlined base); lifting it slides downstream bases left by 10 nt (remainder 1), shifting every downstream codon boundary and drifting a 'STOP ?' marker.
  s10_scope:    Brackets separate 'untranslated' ends from the middle 'coding sequence', restricting the computed triplet ruler strictly under the coding region while three unanswered question tags ('export?', 'decay?', 'translation?') appear below.
  s11_rules:    Capped/tailed transcript pulses GOLD end marks and TEAL join arcs while the triplet ruler locks beneath coding sequence and steps the reading marker; the bottom rule swaps from Film 1's rule to Film 2's coding-frame rule.
"""

from bp_parts import *

# ------------------------------------------------------------------ shared geometry & helpers
WHITE_HL = "#FFFFFF"
EXON_H = 0.86
INTRON_H = 0.28
NT_W = 0.26          # width of 1 coding nucleotide on the computed ruler (3 * NT_W = 0.78 per codon)
CODON_W = 3 * NT_W


def make_cap(label_text="5' cap"):
    """GOLD 5' cap pill, always padded cleanly around its label."""
    return boxed_label(label_text, GOLD, size=24, pad=0.15, fill_opacity=0.28, corner_radius=0.12)


def make_tail(label_text="poly(A)"):
    """GOLD 3' poly(A) tail pill, always padded cleanly around its label."""
    return boxed_label(label_text, GOLD, size=24, pad=0.15, fill_opacity=0.28, corner_radius=0.12)


def make_exon(width, label=None, height=EXON_H, color=BLUE, stroke_color=None, stroke_width=2.5,
              fill_opacity=0.46, label_size=26):
    """BLUE exon block, optionally labelled inside if wide enough."""
    sc = stroke_color or color
    rect = RoundedRectangle(corner_radius=0.10, width=width, height=height,
                            stroke_color=sc, stroke_width=stroke_width,
                            fill_color=color, fill_opacity=fill_opacity)
    if label:
        lab = T(label, size=label_size, color=TEXT).move_to(rect)
        if lab.width > width - 0.16 and label_size > 24:
            lab = T(label, size=24, color=TEXT).move_to(rect)
        return VGroup(rect, lab)
    return VGroup(rect)


def make_intron(width, height=INTRON_H, label=None, color=RED, fill_opacity=0.55):
    """RED intron ribbon."""
    rect = Rectangle(width=width, height=height, stroke_color=color, stroke_width=2.0,
                     fill_color=color, fill_opacity=fill_opacity)
    if label:
        lab = T(label, size=24, color=RED).next_to(rect, DOWN, buff=0.14)
        return VGroup(rect, lab)
    return VGroup(rect)


def join_arc(p1, p2, height=0.80, color=TEAL, stroke_width=3.5, dashed=False):
    """Curved TEAL splice join arc between two top points."""
    p1 = np.array(p1, dtype=float)
    p2 = np.array(p2, dtype=float)
    c1 = p1 + UP * height + RIGHT * 0.12 * (p2[0] - p1[0])
    c2 = p2 + UP * height - RIGHT * 0.12 * (p2[0] - p1[0])
    curve = CubicBezier(p1, c1, c2, p2, color=color, stroke_width=stroke_width)
    if dashed:
        return DashedVMobject(curve, num_dashes=12, color=color)
    return curve


def splice_flag(pos, direction=UP, color=TEAL, height=0.45, opacity=1.0):
    """Small TEAL flag/pin marking a splice site signal."""
    pos = np.array(pos, dtype=float)
    tip = pos + direction * height
    stem = Line(pos, tip, color=color, stroke_width=3.5).set_opacity(opacity)
    head = Dot(tip, radius=0.08, color=color).set_opacity(opacity)
    return VGroup(stem, head)


def build_transcript(exon_widths, intron_widths=None, exon_labels=None, y=0.6, x_center=0.0,
                     with_ends=True, height=EXON_H, cap_label="5' cap", tail_label="poly(A)",
                     buff=0.08, label_size=26):
    """Build a horizontal capped/tailed transcript (pre-mRNA if intron_widths given, else mRNA)."""
    n = len(exon_widths)
    if intron_widths is None:
        intron_widths = [0.0] * (n - 1)
    parts = []
    exons = []
    introns = []
    cap = make_cap(label_text=cap_label) if with_ends else None
    tail = make_tail(label_text=tail_label) if with_ends else None

    seq = []
    if cap is not None:
        seq.append(("cap", cap))
    for i, ew in enumerate(exon_widths):
        lbl = exon_labels[i] if exon_labels and i < len(exon_labels) else None
        ex = make_exon(ew, label=lbl, height=height, label_size=label_size)
        exons.append(ex)
        seq.append(("exon", ex))
        if i < n - 1 and intron_widths[i] > 0:
            intr = make_intron(intron_widths[i])
            introns.append(intr)
            seq.append(("intron", intr))
    if tail is not None:
        seq.append(("tail", tail))

    total_w = sum(m.width for _, m in seq) + buff * max(0, len(seq) - 1)
    x = x_center - total_w / 2.0
    for idx, (_, m) in enumerate(seq):
        m.move_to([x + m.width / 2.0, y, 0.0])
        x += m.width + buff
        parts.append(m)

    g = VGroup(*parts)
    g.cap = cap
    g.tail = tail
    g.exons = exons
    g.introns = introns
    return g


def build_codon_boxes(x_start, y, n_codons, nt_w=NT_W, height=0.58, color=BLUE, fill_opacity=0.32,
                      highlight_from=None, hl_color=GOLD, with_placeholders=True):
    """Computed triplet codon boxes: each box is strictly 3 * nt_w wide with 3 internal base slots."""
    boxes = VGroup()
    cw = 3 * nt_w
    for k in range(n_codons):
        c = hl_color if (highlight_from is not None and k >= highlight_from) else color
        rect = Rectangle(width=cw, height=height, stroke_color=c, stroke_width=2.5,
                         fill_color=c, fill_opacity=fill_opacity)
        cx = x_start + (k + 0.5) * cw
        rect.move_to([cx, y, 0.0])
        cell = VGroup(rect)
        if with_placeholders:
            for b in range(3):
                bx = x_start + k * cw + (b + 0.5) * nt_w
                dot = RoundedRectangle(corner_radius=0.02, width=nt_w * 0.56, height=height * 0.36,
                                       stroke_width=0, fill_color=TEXT, fill_opacity=0.58).move_to([bx, y, 0.0])
                cell.add(dot)
        boxes.add(cell)
    return boxes


def build_nt_ruler(x_start, y, n_codons, nt_w=NT_W, tick_h=0.18):
    """Fixed reference triplet ruler axis underneath codon boxes: major ticks every 3 nt, minor every 1 nt."""
    total_w = n_codons * 3 * nt_w
    line = Line([x_start, y, 0], [x_start + total_w, y, 0], color=GREY, stroke_width=2.5)
    ticks = VGroup()
    for i in range(n_codons * 3 + 1):
        px = x_start + i * nt_w
        is_major = (i % 3 == 0)
        h = tick_h * (1.7 if is_major else 0.85)
        sw = 2.8 if is_major else 1.4
        col = TEXT if is_major else GREY
        ticks.add(Line([px, y, 0], [px, y - h, 0], color=col, stroke_width=sw))
    return VGroup(line, ticks)


def build_reading_marker(x_center, y_box, codon_w=CODON_W, box_h=0.58):
    """Bold filled reading marker frame + ribosome cap centered on one codon box."""
    frame = RoundedRectangle(corner_radius=0.06, width=codon_w + 0.06, height=box_h + 0.14,
                             stroke_color=TEAL, stroke_width=4.0, fill_color=TEAL, fill_opacity=0.40)
    frame.move_to([x_center, y_box, 0.0])
    cap_bar = RoundedRectangle(corner_radius=0.06, width=codon_w + 0.16, height=0.18,
                               stroke_width=0, fill_color=TEAL, fill_opacity=0.90)
    cap_bar.next_to(frame, UP, buff=0.04)
    return VGroup(frame, cap_bar)


def build_mini_mrna(blocks, width=3.1, height=0.34):
    """Compact schematic mRNA strip for the stack in s02_patterns. blocks = list of (rel_w, color)."""
    total = sum(w for w, _ in blocks)
    cap = Rectangle(width=0.18, height=height * 0.85, stroke_width=1.5, stroke_color=GOLD,
                    fill_color=GOLD, fill_opacity=0.6)
    tail = Rectangle(width=0.28, height=height * 0.5, stroke_width=1.5, stroke_color=GOLD,
                     fill_color=GOLD, fill_opacity=0.6)
    body_w = width - cap.width - tail.width
    segs = [cap]
    for rw, col in blocks:
        h = height if col == BLUE else height * 0.45
        segs.append(Rectangle(width=body_w * rw / total, height=h, stroke_color=col, stroke_width=1.8,
                              fill_color=col, fill_opacity=0.48))
    segs.append(tail)
    return VGroup(*segs).arrange(RIGHT, buff=0.02)


def carried_s00_premrna(y=-0.35):
    """Shared builder for the pre-mRNA copy carried from s00_link into s01_title."""
    tr = build_transcript([1.45, 1.35, 1.30, 1.45], [0.9, 0.9, 0.9],
                          exon_labels=["E1", "E2", "E3", "E4"], y=y, x_center=0.0, buff=0.08)
    a1 = join_arc(tr.exons[0].get_top() + RIGHT * 0.35, tr.exons[1].get_top() + LEFT * 0.35,
                  height=0.52, color=TEAL, stroke_width=3.2)
    a2 = join_arc(tr.exons[0].get_top() + RIGHT * 0.35, tr.exons[2].get_top() + LEFT * 0.30,
                  height=0.82, color=TEAL, stroke_width=3.2, dashed=True)
    f1 = splice_flag(tr.exons[0].get_corner(UR) + LEFT * 0.05, UP, TEAL, 0.34)
    f2 = splice_flag(tr.exons[1].get_corner(UL) + RIGHT * 0.05, UP, TEAL, 0.34)
    f3 = splice_flag(tr.exons[2].get_corner(UL) + RIGHT * 0.05, UP, TEAL, 0.34)
    return tr, VGroup(a1, a2), VGroup(f1, f2, f3)


def carried_s06_world(lifted=True):
    """Shared builder for s06_predict and s07_pause so the pause frame matches s06_predict identically."""
    x0 = -18 * NT_W  # -4.68
    y_rna = 0.75
    y_box = -0.55
    y_rul = -1.05

    w1, w2, w3 = 12 * NT_W, 12 * NT_W, 12 * NT_W
    e1 = make_exon(w1, label="12 nt", height=EXON_H).move_to([x0 + w1 / 2, y_rna, 0])
    e2 = make_exon(w2, label="4 codons", height=EXON_H, stroke_color=WHITE_HL, stroke_width=4.5)
    e2.move_to([x0 + w1 + w2 / 2, y_rna + (0.75 if lifted else 0.0), 0])
    e3 = make_exon(w3, label="12 nt", height=EXON_H).move_to([x0 + w1 + w2 + w3 / 2, y_rna, 0])

    cap = make_cap().next_to(e1, LEFT, buff=0.08)
    tail = make_tail().next_to(e3, RIGHT, buff=0.08)

    e2_lab = T("12 coding nucleotides", size=28, color=TEXT).next_to(e2, UP, buff=0.22)
    boxes = build_codon_boxes(x0, y_box, 12, nt_w=NT_W, color=BLUE)
    mid_outline = SurroundingRectangle(VGroup(*boxes[4:8]), color=WHITE_HL, buff=0.04, stroke_width=2.5, corner_radius=0.04)
    ruler = build_nt_ruler(x0, y_rul, 12, nt_w=NT_W)
    ruler_lab = T("triplet ruler (3 bases per codon)", size=24, color=TEXT).next_to(ruler, DOWN, buff=0.18)
    marker = build_reading_marker(boxes[3 if lifted else 1].get_center()[0], y_box)

    g = VGroup(cap, e1, e2, e3, tail, e2_lab, boxes, mid_outline, ruler, ruler_lab, marker)
    g.cap, g.e1, g.e2, g.e3, g.tail = cap, e1, e2, e3, tail
    g.e2_lab, g.boxes, g.mid_outline, g.ruler, g.ruler_lab, g.marker = (
        e2_lab, boxes, mid_outline, ruler, ruler_lab, marker
    )
    return g


# ------------------------------------------------------------------ scenes
class S00Link(SpokenScene):
    def construct(self):
        # Finished capped & tailed mRNA from Film 1 (fills ~65% width)
        mrna = build_transcript([1.8, 1.65, 1.65, 1.7], exon_labels=["E1", "E2", "E3", "E4"],
                                y=1.15, x_center=0.0, buff=0.08)
        stag = scope_tag("schematic")

        joins = VGroup(*[
            Line(mrna.exons[i].get_corner(UR) + RIGHT * 0.04 + DOWN * 0.06,
                 mrna.exons[i].get_corner(DR) + RIGHT * 0.04 + UP * 0.06, color=TEAL, stroke_width=5)
            for i in range(len(mrna.exons) - 1)
        ])

        self.add(mrna, stag)
        self.wait(0.4)
        self.at("marked both ends")
        self.play(Indicate(mrna.cap, color=GOLD, scale_factor=1.10),
                  Indicate(mrna.tail, color=GOLD, scale_factor=1.10), run_time=1.0)

        self.at("joined blue exons")
        self.play(FadeIn(joins), run_time=0.5)
        self.play(ShowPassingFlash(joins.copy().set_color(WHITE_HL).set_stroke(width=7), time_width=0.5),
                  run_time=1.3)

        # Question: reading frame change?
        self.at("If those joins change")
        alt_arc1 = join_arc(mrna.exons[0].get_top() + RIGHT * 0.3, mrna.exons[2].get_top() + LEFT * 0.3,
                            height=0.75, color=TEAL, stroke_width=3.5, dashed=True)
        alt_arc2 = join_arc(mrna.exons[1].get_top() + RIGHT * 0.3, mrna.exons[3].get_top() + LEFT * 0.3,
                            height=0.68, color=TEAL, stroke_width=3.5, dashed=True)
        strip_bg = RoundedRectangle(corner_radius=0.10, width=8.6, height=0.58,
                                    stroke_color=GREY, stroke_width=2.5, fill_color=BLUE, fill_opacity=0.16)
        strip_bg.move_to([0.0, -1.45, 0.0])
        strip_ticks = VGroup(*[
            Line([x, -1.74, 0], [x, -1.16, 0], color=GREY, stroke_width=2.0)
            for x in np.linspace(-3.6, 3.6, 11)
        ])
        strip_q = boxed_label("reading frame ?", GOLD, size=28, pad=0.14, fill_opacity=0.2).next_to(strip_bg, DOWN, buff=0.24)
        strip = VGroup(strip_bg, strip_ticks, strip_q)

        self.play(Create(alt_arc1), Create(alt_arc2), FadeIn(strip, shift=UP * 0.15), run_time=1.8)
        self.at("reading frame")
        self.play(Indicate(strip_q, color=GOLD, scale_factor=1.08), run_time=1.4)

        # Follow different copies: move finished mRNA up WITHOUT shrinking labels below 22 pt
        self.at("Follow different copies")
        top_group = VGroup(mrna, joins, alt_arc1, alt_arc2)
        prem, arcs, flags = carried_s00_premrna(y=-0.45)
        copy_lab = T("another copy of the same gene's transcript", size=28, color=TEXT).move_to([0.0, 1.05, 0.0])

        self.play(
            top_group.animate.shift(UP * 1.15),
            FadeOut(strip),
            run_time=1.4,
        )
        self.play(FadeIn(copy_lab), FadeIn(prem, shift=RIGHT * 0.2), run_time=1.8)

        # Highlight introns sequentially during the narration stretch (keeps frame active & purposeful)
        for intr in prem.introns:
            self.play(Indicate(intr, color=RED, scale_factor=1.12), run_time=1.2)

        # Regulatory signals steer spliceosome to different junctions
        self.at("regulatory signals")
        sig_lab = T("regulatory signals steer junctions", size=28, color=TEAL).move_to([0.0, -1.65, 0.0])
        self.play(FadeIn(flags, shift=DOWN * 0.15), FadeIn(sig_lab), run_time=1.2)
        self.play(Create(arcs[0]), run_time=1.1)
        self.at("different junctions")
        self.play(Create(arcs[1]), run_time=1.2)
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        prem, arcs, flags = carried_s00_premrna(y=-0.85)
        stag = scope_tag("schematic")
        lesson = T("RNA PROCESSING: CAPS, TAILS AND SPLICING", size=22, color=TEXT).set_opacity(0.85)
        title = T("When the Joins Change", size=54, font=TITLE_FONT, color=TEXT)
        rule = Line(LEFT * 2.2, RIGHT * 2.2, color=GOLD, stroke_width=4)
        head = VGroup(lesson, title, rule).arrange(DOWN, buff=0.22).move_to([0.0, 1.95, 0.0])

        self.add(prem, flags, stag)
        self.play(FadeIn(head, shift=UP * 0.12), Create(arcs[0]), Create(arcs[1]), run_time=1.1)
        self.play(ShowPassingFlash(arcs.copy().set_color(WHITE_HL).set_stroke(width=6), time_width=0.6),
                  run_time=0.9)
        self.finish()


class S02Patterns(SpokenScene):
    def construct(self):
        # Persistent stage: copy label, right-hand finished mRNA stack, bottom pattern label
        x_mid = -1.95
        y_rna = 0.25
        stag = scope_tag("schematic")
        copy_lab = T("one of many copies", size=28, color=TEXT).move_to([x_mid, 2.35, 0.0])

        stack_head = T("finished mRNAs", size=28, color=BLUE).move_to([4.10, 2.35, 0.0])
        stack_frame = RoundedRectangle(corner_radius=0.16, width=3.55, height=4.4,
                                       stroke_color=GREY, stroke_width=2.0, fill_color=BG, fill_opacity=0.6)
        stack_frame.move_to([4.10, -0.1, 0.0])
        stack_slots = [np.array([4.10, 1.55 - k * 1.08, 0.0]) for k in range(4)]

        # Build first copy with individual pieces added directly so cleanup is 100% exact
        ew = [1.15, 1.15, 1.15]
        iw = [0.62, 0.62]
        prem = build_transcript(ew, iw, exon_labels=["E1", "E2", "E3"], y=y_rna, x_center=x_mid,
                                tail_label="tail", buff=0.08)
        cur_mobs = [prem.cap, prem.exons[0], prem.introns[0], prem.exons[1], prem.introns[1], prem.exons[2], prem.tail]
        pat_lab = T("pre-mRNA", size=30, color=TEXT).move_to([x_mid, -1.65, 0.0])

        self.add(copy_lab, *cur_mobs, pat_lab, stack_head, stack_frame, stag)
        self.wait(0.4)
        for ex in prem.exons:
            self.play(Indicate(ex, color=BLUE, scale_factor=1.06), run_time=0.7)

        # 1. Skip an exon
        self.at("skip an exon")
        new_lab = T("skip an exon", size=30, color=TEAL).move_to([x_mid, -1.65, 0.0])
        skip_arc = join_arc(prem.exons[0].get_top() + RIGHT * 0.2, prem.exons[2].get_top() + LEFT * 0.2,
                            height=0.85, color=TEAL, stroke_width=3.5)
        m1 = build_mini_mrna([(1.2, BLUE), (1.2, BLUE)]).move_to(stack_slots[0])
        m1_tag = T("skipped", size=24, color=TEXT).next_to(m1, DOWN, buff=0.10)
        self.play(swap(pat_lab, new_lab, run_time=0.35), Create(skip_arc, run_time=0.45))
        self.play(
            prem.introns[0].animate.shift(UP * 0.60).set_opacity(0.25),
            prem.exons[1].animate.shift(UP * 0.60).set_opacity(0.25),
            prem.introns[1].animate.shift(UP * 0.60).set_opacity(0.25),
            FadeIn(m1), FadeIn(m1_tag), run_time=0.6,
        )
        pat_lab = new_lab

        # 2. Shift a splice site
        self.at("shift a splice site")
        self.remove(*cur_mobs, skip_arc)
        prem2 = build_transcript(ew, iw, exon_labels=["E1", "E2", "E3"], y=y_rna, x_center=x_mid,
                                 tail_label="tail", buff=0.08)
        cur_mobs = [prem2.cap, prem2.exons[0], prem2.introns[0], prem2.exons[1], prem2.introns[1], prem2.exons[2], prem2.tail]
        self.add(*cur_mobs)
        new_lab = T("shift a splice site", size=30, color=TEAL).move_to([x_mid, -1.65, 0.0])
        site_pin = splice_flag(prem2.exons[1].get_corner(UL) + RIGHT * 0.05, UP, TEAL, 0.45)
        m2 = build_mini_mrna([(1.2, BLUE), (0.8, BLUE), (1.2, BLUE)]).move_to(stack_slots[1])
        m2_tag = T("shifted site", size=24, color=TEXT).next_to(m2, DOWN, buff=0.10)
        self.play(swap(pat_lab, new_lab, run_time=0.32), FadeIn(site_pin, run_time=0.25))
        self.play(
            site_pin.animate.shift(RIGHT * 0.34),
            prem2.exons[1][0].animate.stretch_to_fit_width(0.81).shift(RIGHT * 0.17),
            prem2.exons[1][1].animate.shift(RIGHT * 0.17),
            FadeIn(m2), FadeIn(m2_tag), run_time=0.65,
        )
        pat_lab = new_lab

        # 3. Choose between exons (no arc crossing labels)
        self.at("choose between exons")
        self.remove(*cur_mobs, site_pin, pat_lab)
        new_lab = T("choose between exons", size=30, color=TEAL).move_to([x_mid, -1.65, 0.0])
        prem3 = build_transcript([1.05, 1.05, 1.05, 1.05], [0.50, 0.25, 0.50],
                                 exon_labels=["E1", "E2a", "E2b", "E3"], y=y_rna, x_center=x_mid,
                                 tail_label="tail", buff=0.08, label_size=24)
        prem3.exons[1].shift(UP * 0.58)
        prem3.exons[2].shift(DOWN * 0.58)
        cur_mobs = [prem3.cap, prem3.exons[0], prem3.introns[0], prem3.exons[1],
                    prem3.introns[1], prem3.exons[2], prem3.introns[2], prem3.exons[3], prem3.tail]
        self.add(*cur_mobs, new_lab)
        pat_lab = new_lab
        link_l = Line(prem3.exons[0].get_corner(DR), prem3.exons[2].get_left(), color=TEAL, stroke_width=3.5)
        link_r = Line(prem3.exons[2].get_right(), prem3.exons[3].get_corner(DL), color=TEAL, stroke_width=3.5)
        m3 = build_mini_mrna([(1.15, BLUE), (1.05, BLUE), (1.15, BLUE)]).move_to(stack_slots[2])
        m3_tag = T("one of two exons", size=24, color=TEXT).next_to(m3, DOWN, buff=0.10)
        self.play(Create(link_l, run_time=0.35), Create(link_r, run_time=0.35))
        self.play(
            prem3.exons[1].animate.set_opacity(0.25),
            prem3.exons[2].animate.shift(UP * 0.58),
            FadeOut(link_l), FadeOut(link_r),
            FadeIn(m3), FadeIn(m3_tag), run_time=0.55,
        )

        # 4. Retain an intron (highlight ONLY the retained intron + flanking edges, clear of 5' cap)
        self.at("retain an intron")
        self.remove(*cur_mobs, link_l, link_r)
        prem4 = build_transcript(ew, iw, exon_labels=["E1", "E2", "E3"], y=y_rna, x_center=x_mid,
                                 tail_label="tail", buff=0.08)
        cur_mobs = [prem4.cap, prem4.exons[0], prem4.introns[0], prem4.exons[1], prem4.introns[1], prem4.exons[2], prem4.tail]
        self.add(*cur_mobs)
        new_lab = T("retain an intron", size=30, color=RED).move_to([x_mid, -1.65, 0.0])
        keep_box = SurroundingRectangle(prem4.introns[0], color=RED, buff=0.07, stroke_width=3, corner_radius=0.06)
        m4 = build_mini_mrna([(1.15, BLUE), (0.75, RED), (1.15, BLUE), (1.15, BLUE)]).move_to(stack_slots[3])
        m4_tag = T("retained intron", size=24, color=RED).next_to(m4, DOWN, buff=0.10)
        self.play(
            swap(pat_lab, new_lab, run_time=0.35),
            prem4.introns[0].animate.stretch_to_fit_height(0.42).set_fill(opacity=0.85),
            Create(keep_box), FadeIn(m4), FadeIn(m4_tag), run_time=0.85,
        )
        pat_lab = new_lab

        # Each choice makes a different messenger RNA
        self.at("Each choice")
        stack_items = [VGroup(m1, m1_tag), VGroup(m2, m2_tag), VGroup(m3, m3_tag), VGroup(m4, m4_tag)]
        for it in stack_items:
            self.play(Indicate(it, color=GOLD, scale_factor=1.06), run_time=0.7)

        # Regulatory signals can make these patterns differ among tissues
        self.at("Regulatory signals")
        reg_lab = T("tissue signals steer which pattern wins", size=28, color=TEAL).move_to([x_mid, -1.65, 0.0])
        sig_pins = VGroup(
            splice_flag(prem4.exons[0].get_corner(UR) + LEFT * 0.05, UP, TEAL, 0.45),
            splice_flag(prem4.exons[1].get_corner(UL) + RIGHT * 0.05, UP, TEAL, 0.45),
            splice_flag(prem4.exons[1].get_corner(UR) + LEFT * 0.05, UP, TEAL, 0.45),
        )
        self.play(swap(pat_lab, reg_lab, run_time=0.6), FadeIn(sig_pins, shift=DOWN * 0.15), run_time=0.9)
        self.play(Indicate(sig_pins[0], color=GOLD, scale_factor=1.2), Indicate(m1, color=TEAL, scale_factor=1.06), run_time=1.1)
        self.play(Indicate(sig_pins[1], color=GOLD, scale_factor=1.2), Indicate(m4, color=GOLD, scale_factor=1.06), run_time=1.1)
        self.finish()


class S03Variant(SpokenScene):
    def construct(self):
        stag = scope_tag("schematic")
        y_top = 1.45
        prem = build_transcript([1.7, 1.7, 1.7], [1.2, 1.2], exon_labels=["E1", "E2", "E3"],
                                y=y_top, x_center=0.4, with_ends=False, buff=0.08)
        norm_flag = splice_flag(prem.exons[1].get_corner(UL) + RIGHT * 0.06, UP, TEAL, 0.48)
        norm_lab = T("normal site", size=24, color=TEAL).move_to([-1.6, 2.88, 0.0])
        norm_ptr = Line(norm_lab.get_bottom() + DOWN * 0.10, norm_flag[1].get_center() + UP * 0.12,
                        color=TEAL, stroke_width=2.0)
        var_mark = Dot(prem.exons[1].get_corner(UL) + RIGHT * 0.06, radius=0.10, color=GOLD)
        var_lab = T("sequence change", size=24, color=GOLD).next_to(prem.exons[1].get_corner(DL), DOWN, buff=0.16)

        self.add(prem, norm_flag, norm_lab, norm_ptr, stag)
        self.play(prem.exons[1][0].animate.set_fill(BLUE, opacity=0.62), run_time=1.0)
        self.at("weaken")
        self.play(
            FadeIn(var_mark, scale=1.4), FadeIn(var_lab),
            prem.exons[1][0].animate.set_fill(BLUE, opacity=0.30),
            norm_flag.animate.set_opacity(0.30),
            norm_lab.animate.set_opacity(0.45),
            norm_ptr.animate.set_opacity(0.30),
            run_time=1.6,
        )

        # Nearby sites compete differently
        self.at("Nearby sites")
        cryp1 = splice_flag(prem.exons[1].get_top() + LEFT * 0.25, UP, TEAL, 0.40)
        cryp2 = splice_flag(prem.introns[1].get_top() + LEFT * 0.15, UP, TEAL, 0.40)
        cryp_lab = T("possible cryptic sites", size=24, color=TEAL).move_to([2.9, 2.85, 0.0])

        arc_skip = join_arc(prem.exons[0].get_top() + RIGHT * 0.3, prem.exons[2].get_top() + LEFT * 0.3,
                            height=0.80, color=TEAL, stroke_width=4.0)
        arc_cryp = join_arc(prem.exons[0].get_top() + RIGHT * 0.3, prem.exons[1].get_top() + LEFT * 0.25,
                            height=0.48, color=TEAL, stroke_width=2.5, dashed=True)

        self.play(FadeIn(cryp1), FadeIn(cryp2), FadeIn(cryp_lab), Create(arc_skip), Create(arc_cryp), run_time=1.4)
        self.play(
            prem.exons[0][0].animate.set_fill(TEAL, opacity=0.55),
            prem.exons[2][0].animate.set_fill(TEAL, opacity=0.55),
            arc_skip.animate.set_stroke(width=6.0),
            run_time=1.3,
        )
        self.play(
            prem.exons[0][0].animate.set_fill(BLUE, opacity=0.46),
            prem.exons[2][0].animate.set_fill(BLUE, opacity=0.46),
            prem.exons[1][0].animate.set_fill(TEAL, opacity=0.55),
            arc_skip.animate.set_stroke(width=4.0),
            arc_cryp.animate.set_stroke(width=4.2),
            run_time=1.3,
        )
        self.play(
            prem.exons[1][0].animate.set_fill(BLUE, opacity=0.35),
            arc_cryp.animate.set_stroke(width=2.5),
            run_time=0.8,
        )

        # Three branching schematic lanes below (keep left side clear for 'one allele')
        lane_x = 0.0
        self.at("most often")
        l1_y = -0.15
        l1_bar = VGroup(
            make_exon(2.3, "E1", height=0.66),
            make_exon(2.3, "E3", height=0.66),
        ).arrange(RIGHT, buff=0.06).move_to([lane_x, l1_y, 0.0])
        stem_pt = np.array([-3.3, y_top - 0.45, 0.0])
        l1_arrow = Arrow(stem_pt, [l1_bar.get_left()[0] - 0.15, l1_y, 0.0],
                         color=TEAL, stroke_width=6, buff=0.0)
        l1_lab = T("skip (most often)", size=28, color=BLUE).next_to(l1_bar, RIGHT, buff=0.3)
        self.play(GrowArrow(l1_arrow), FadeIn(l1_bar, shift=RIGHT * 0.2), FadeIn(l1_lab), run_time=1.4)

        self.at("Less often")
        l2_y = -1.30
        l2_bar = VGroup(
            make_exon(2.0, "E1", height=0.44, label_size=24),
            make_exon(1.2, None, height=0.44, stroke_color=TEAL),
            make_exon(1.8, "E3", height=0.44, label_size=24),
        ).arrange(RIGHT, buff=0.06).move_to([lane_x + 0.2, l2_y, 0.0])
        l2_arrow = Arrow(stem_pt, [l2_bar.get_left()[0] - 0.15, l2_y, 0.0],
                         color=TEAL, stroke_width=2.8, buff=0.0)
        l2_lab = T("cryptic site", size=26, color=TEAL).next_to(l2_bar, RIGHT, buff=0.3)
        self.play(GrowArrow(l2_arrow), FadeIn(l2_bar, shift=RIGHT * 0.2), FadeIn(l2_lab), run_time=1.3)

        self.at("intron is retained")
        l3_y = -2.35
        l3_bar = VGroup(
            make_exon(1.5, "E1", height=0.44, label_size=24),
            make_intron(0.95, height=0.24),
            make_exon(1.3, "E2", height=0.44, label_size=24),
            make_exon(1.3, "E3", height=0.44, label_size=24),
        ).arrange(RIGHT, buff=0.06).move_to([lane_x + 0.25, l3_y, 0.0])
        l3_arrow = Arrow(stem_pt, [l3_bar.get_left()[0] - 0.15, l3_y, 0.0],
                         color=RED, stroke_width=2.8, buff=0.0)
        l3_lab = T("retain", size=26, color=RED).next_to(l3_bar, RIGHT, buff=0.3)
        self.play(GrowArrow(l3_arrow), FadeIn(l3_bar, shift=RIGHT * 0.2), FadeIn(l3_lab), run_time=1.3)

        self.at("One allele")
        allele_tag = boxed_label("one allele", GOLD, size=26, pad=0.14).move_to([-4.85, -0.85, 0.0])
        self.play(FadeIn(allele_tag), Indicate(VGroup(l1_bar, l2_bar, l3_bar), color=GOLD, scale_factor=1.03),
                  run_time=1.5)
        self.finish()


class S04Evidence(SpokenScene):
    def construct(self):
        stag = scope_tag("schematic")
        allele_box = RoundedRectangle(corner_radius=0.16, width=4.0, height=2.2,
                                      stroke_color=GOLD, stroke_width=3.0, fill_color=BG, fill_opacity=0.9)
        allele_box.move_to([-4.0, 0.1, 0.0])
        allele_lbl = fit_text("studied beta-thalassemia allele", max_w=3.5, size=28, color=TEXT)
        allele_lbl.move_to(allele_box.get_top() + DOWN * 0.55)
        allele_gene = build_transcript([0.9, 0.9, 0.9], [0.5, 0.5], y=allele_box.get_bottom()[1] + 0.6,
                                       x_center=-4.0, with_ends=False, height=0.45, buff=0.05)
        sig_dot = Dot(allele_gene.introns[0].get_left() + RIGHT * 0.05, radius=0.09, color=TEAL)
        allele_grp = VGroup(allele_box, allele_lbl, allele_gene, sig_dot)
        cells_lab = T("in cultured cells", size=26, color=TEXT).next_to(allele_box, DOWN, buff=0.35)

        self.add(allele_grp, stag)
        self.play(Indicate(sig_dot, color=GOLD, scale_factor=1.5), FadeIn(cells_lab), run_time=1.8)

        # Two schematic lane guides branching right
        self.at("two abnormal")
        main_y = 1.25
        small_y = -1.15
        g1 = Arrow(allele_box.get_right() + UP * 0.35, [-0.5, main_y, 0], color=TEAL, stroke_width=7, buff=0.12)
        g2 = Arrow(allele_box.get_right() + DOWN * 0.35, [-0.5, small_y, 0], color=TEAL, stroke_width=3, buff=0.12)
        self.play(GrowArrow(g1), GrowArrow(g2), run_time=2.2)

        # Wider lane: main product (BLUE exon - short RED retained segment - BLUE exon)
        self.at("The main product")
        mp_e1 = make_exon(1.8, "exon", height=0.80)
        mp_int = make_intron(1.05, height=0.42)
        mp_e2 = make_exon(2.2, "exon", height=0.80)
        main_prod = VGroup(mp_e1, mp_int, mp_e2).arrange(RIGHT, buff=0.06).move_to([2.35, main_y, 0.0])
        main_lab = T("main product (part of intron kept)", size=26, color=TEXT).next_to(main_prod, UP, buff=0.22)
        self.play(FadeIn(main_lab), FadeIn(mp_e1, shift=RIGHT * 0.2), run_time=0.9)
        self.play(FadeIn(mp_int, shift=RIGHT * 0.2), FadeIn(mp_e2, shift=RIGHT * 0.2), run_time=1.5)

        # Narrower lane: smaller amount (non-adjacent exons joined)
        self.at("A smaller amount")
        sp_e1 = make_exon(1.9, "exon", height=0.46, label_size=24)
        sp_e2 = make_exon(2.4, "later exon", height=0.46, label_size=24)
        small_prod = VGroup(sp_e1, sp_e2).arrange(RIGHT, buff=0.06).move_to([2.1, small_y, 0.0])
        small_lab = T("smaller amount (non-adjacent exons joined)", size=26, color=BLUE).next_to(small_prod, DOWN, buff=0.25)
        self.play(FadeIn(small_lab), FadeIn(sp_e1, shift=RIGHT * 0.2), FadeIn(sp_e2, shift=RIGHT * 0.2), run_time=2.2)

        # One changed splice signal shifted competition in more than one way
        self.at("One changed splice")
        for prod, arr in ((main_prod, g1), (small_prod, g2)):
            self.play(
                Indicate(sig_dot, color=GOLD, scale_factor=1.5),
                ShowPassingFlash(arr.copy().set_color(GOLD).set_stroke(width=8), time_width=0.6),
                Indicate(prod, color=GOLD, scale_factor=1.04),
                run_time=1.9,
            )
        self.finish()


class S05Ruler(SpokenScene):
    def construct(self):
        # BLUE coding message across the frame: 12 codons = 36 nt
        x0 = -18 * NT_W  # -4.68
        y_rna = 1.05
        y_box = -0.35
        y_rul = -0.85

        e1 = make_exon(12 * NT_W, "exon 1", height=EXON_H).move_to([x0 + 6 * NT_W, y_rna, 0])
        e2 = make_exon(12 * NT_W, "exon 2", height=EXON_H).move_to([x0 + 18 * NT_W, y_rna, 0])
        e3 = make_exon(12 * NT_W, "exon 3", height=EXON_H).move_to([x0 + 30 * NT_W, y_rna, 0])
        cap = make_cap().next_to(e1, LEFT, buff=0.08)
        tail = make_tail().next_to(e3, RIGHT, buff=0.08)
        msg = VGroup(cap, e1, e2, e3, tail)
        msg_lab = T("coding sequence", size=28, color=BLUE).move_to([0.0, 2.2, 0.0])

        self.add(msg, msg_lab)
        self.play(
            e1[0].animate.set_fill(BLUE, opacity=0.78),
            e2[0].animate.set_fill(BLUE, opacity=0.78),
            e3[0].animate.set_fill(BLUE, opacity=0.78),
            run_time=0.9,
        )
        self.play(
            e1[0].animate.set_fill(BLUE, opacity=0.46),
            e2[0].animate.set_fill(BLUE, opacity=0.46),
            e3[0].animate.set_fill(BLUE, opacity=0.46),
            run_time=0.9,
        )

        # Computed triplet ruler reveals underneath; reading marker advances left to right
        self.at("In coding sequence")
        boxes = build_codon_boxes(x0, y_box, 12, nt_w=NT_W, color=BLUE)
        ruler = build_nt_ruler(x0, y_rul, 12, nt_w=NT_W)
        codon_lab = T("codons (groups of 3 bases)", size=28, color=TEXT).move_to([0.0, -1.9, 0.0])
        marker = build_reading_marker(boxes[0].get_center()[0], y_box)
        marker_y = marker.get_center()[1]

        self.play(FadeIn(boxes), Create(ruler), FadeIn(codon_lab), FadeIn(marker), run_time=1.5)
        self.at("groups called codons")
        for k in range(1, 6):
            self.play(marker.animate.move_to([boxes[k].get_center()[0], marker_y, 0]),
                      run_time=0.55, rate_func=smooth)

        # Exon 2 loses 1 nt (12 -> 11 nt); exon 3 + downstream codons (boxes[8:]) slide left by 1 nt WITHOUT overlap!
        self.at("Changing the length")
        downstream_boxes = VGroup(*boxes[8:])
        shift_lab = T("downstream codons shifted -> amino acids change", size=28, color=GOLD).move_to([0.0, -1.9, 0.0])
        # Replace boxes[7] (the 3-nt box at the end of E2) cleanly with a 2-nt leftover cell so boxes[8:] abuts it at x0 + 23*NT_W
        two_nt_rect = Rectangle(width=2 * NT_W, height=0.58, stroke_color=GOLD, stroke_width=2.5,
                                fill_color=GOLD, fill_opacity=0.28).move_to([x0 + 22 * NT_W, y_box, 0])
        two_nt_dots = [
            RoundedRectangle(corner_radius=0.02, width=NT_W * 0.56, height=0.58 * 0.36,
                             stroke_width=0, fill_color=TEXT, fill_opacity=0.58).move_to([bx, y_box, 0])
            for bx in (x0 + 21.5 * NT_W, x0 + 22.5 * NT_W)
        ]
        two_nt = VGroup(two_nt_rect, *two_nt_dots)
        self.play(
            e2.animate.stretch_to_fit_width(11 * NT_W).align_to(e1.get_right(), LEFT).shift(UP * 0.40),
            FadeOut(boxes[7]), FadeIn(two_nt),
            VGroup(e3, tail).animate.shift(LEFT * NT_W),
            downstream_boxes.animate.shift(LEFT * NT_W).set_color(GOLD),
            swap(codon_lab, shift_lab, run_time=0.9),
            run_time=2.2,
        )
        codon_lab = shift_lab

        # Reading marker advances into the shifted GOLD codon boundaries
        self.at("A shift after one junction")
        junc_line = DashedLine([x0 + 23 * NT_W, y_rna + 0.5, 0], [x0 + 23 * NT_W, y_rul - 0.3, 0],
                               color=TEAL, stroke_width=3.5)
        self.play(Create(junc_line), run_time=0.7)
        for idx, k in enumerate((7, 8, 9, 10)):
            grid_cx = x0 + (k + 0.5) * CODON_W
            ds_box = downstream_boxes[min(idx, len(downstream_boxes) - 1)]
            self.play(
                marker.animate.move_to([grid_cx, marker_y, 0]),
                ds_box[0].animate.set_fill(GOLD, opacity=0.60),
                run_time=0.9, rate_func=smooth,
            )
        self.finish()


class S06Predict(SpokenScene):
    def construct(self):
        w = carried_s06_world(lifted=False)
        self.add(w.cap, w.e1, w.e2, w.e3, w.tail, w.boxes, w.ruler, w.ruler_lab, w.marker)
        self.play(FadeIn(w.e2_lab), Create(w.mid_outline), run_time=1.3)
        self.play(Indicate(VGroup(*w.boxes[4:8]), color=WHITE_HL, scale_factor=1.06), run_time=1.8)

        self.at("Imagine that splicing skips it")
        self.play(
            w.e2.animate.shift(UP * 0.75),
            w.e2_lab.animate.shift(UP * 0.75),
            run_time=1.8,
        )

        self.at("Use the ruler")
        marker_y = w.marker.get_center()[1]
        self.play(
            ShowPassingFlash(VGroup(*w.boxes[4:8]).copy().set_color(TEAL), time_width=0.6),
            w.marker.animate.move_to([w.boxes[3].get_center()[0], marker_y, 0]),
            run_time=2.0,
        )

        self.at("Will the downstream")
        q = question_card("Do downstream triplets stay aligned?", options=(), y=BOTTOM_Y + 0.15, color=GOLD, size=32)
        self.play(FadeIn(q.question, shift=UP * 0.12), run_time=1.5)
        self.finish()


class S07Pause(PredictPause):
    QUESTION = "Do downstream triplets stay aligned?"
    OPTIONS = ()
    CARD = {"y": BOTTOM_Y + 0.15, "color": GOLD, "size": 32}
    SECONDS = 4.5

    def backdrop(self):
        return carried_s06_world(lifted=True)


class S08Reveal(SpokenScene):
    def construct(self):
        w = carried_s06_world(lifted=True)
        q = question_card("Do downstream triplets stay aligned?", options=(), y=BOTTOM_Y + 0.15, color=GOLD, size=32)
        self.add(w, q)

        # Clear question, WHITE exon leaves, flanking BLUE blocks slide together by 12 nt (4 codons)
        self.at("They stay aligned")
        shift_vec = LEFT * (12 * NT_W)
        ds_boxes = VGroup(*w.boxes[8:])
        self.play(
            FadeOut(q),
            FadeOut(w.ruler_lab),
            FadeOut(w.e2, shift=UP * 0.4),
            FadeOut(w.e2_lab, shift=UP * 0.4),
            FadeOut(w.mid_outline),
            FadeOut(VGroup(*w.boxes[4:8])),
            run_time=1.0,
        )
        self.play(
            VGroup(w.e3, w.tail).animate.shift(shift_vec),
            ds_boxes.animate.shift(shift_vec),
            run_time=1.4,
        )

        # Green 'aligned' bracket appears under the downstream triplet boxes
        self.at("Removing complete codon")
        bracket = Brace(ds_boxes, DOWN, color=GREEN, buff=0.62)
        aligned_lab = T("aligned", size=28, color=GREEN).next_to(bracket, DOWN, buff=0.12)
        len_note = T("36 nt -> 24 nt (12 removed = 4 codons)", size=26, color=TEXT).move_to([0.0, -3.0, 0.0])
        self.play(FadeIn(bracket), FadeIn(aligned_lab), FadeIn(len_note), run_time=1.3)
        for box in ds_boxes:
            self.play(box[0].animate.set_fill(GREEN, opacity=0.30).set_stroke(GREEN), run_time=0.9)

        # Whole triplets leave, so the next base begins a codon normally
        self.at("Whole triplets leave")
        marker_y = w.marker.get_center()[1]
        for k in (4, 5, 6, 7):
            cx = w.boxes[0].get_center()[0] + k * CODON_W
            self.play(w.marker.animate.move_to([cx, marker_y, 0]), run_time=0.9, rate_func=smooth)

        # New junction pulses with '?' labelled 'sequence still matters'
        self.at("The new junction")
        junc_x = w.e1.get_right()[0]
        junc_pulse = Line([junc_x, 0.75 + 0.45, 0], [junc_x, 0.75 - 0.45, 0], color=GOLD, stroke_width=6)
        seq_q = boxed_label("?  sequence still matters", GOLD, size=26, pad=0.14).move_to([junc_x, 1.85, 0])
        self.play(Create(junc_pulse), FadeIn(seq_q, shift=DOWN * 0.12), run_time=1.1)
        self.play(Indicate(junc_pulse, color=WHITE_HL, scale_factor=1.2),
                  Indicate(seq_q, color=GOLD, scale_factor=1.06), run_time=1.8)
        self.finish()


class S09Shift(SpokenScene):
    def construct(self):
        # Reset transcript: E1 = 12 nt (4 codons), E2 = 10 nt (3 codons + 1 leftover base), E3 = 12 nt (4 codons)
        nt_w = NT_W
        cw = 3 * nt_w
        x0 = -17 * nt_w  # -4.42
        y_rna = 0.75
        y_box = -0.55
        y_rul = -1.05

        w1, w2, w3 = 12 * nt_w, 10 * nt_w, 12 * nt_w
        e1 = make_exon(w1, "12 nt", height=EXON_H).move_to([x0 + w1 / 2, y_rna, 0])
        e2 = make_exon(w2, "10 nt", height=EXON_H, stroke_color=WHITE_HL, stroke_width=4.5).move_to([x0 + w1 + w2 / 2, y_rna, 0])
        e3 = make_exon(w3, "12 nt", height=EXON_H).move_to([x0 + w1 + w2 + w3 / 2, y_rna, 0])
        cap = make_cap().next_to(e1, LEFT, buff=0.08)
        tail = make_tail().next_to(e3, RIGHT, buff=0.08)
        e2_lab = T("10 coding nucleotides", size=28, color=TEXT).next_to(e2, UP, buff=0.22)

        boxes_e1 = build_codon_boxes(x0, y_box, 4, nt_w=nt_w, color=BLUE)
        boxes_e2_full = build_codon_boxes(x0 + w1, y_box, 3, nt_w=nt_w, color=BLUE)
        leftover_x = x0 + w1 + 3 * cw + nt_w / 2
        leftover_rect = Rectangle(width=nt_w, height=0.52, stroke_color=WHITE_HL, stroke_width=3.5,
                                  fill_color=WHITE_HL, fill_opacity=0.24).move_to([leftover_x, y_box, 0])
        leftover_dot = RoundedRectangle(corner_radius=0.02, width=nt_w * 0.56, height=0.52 * 0.36,
                                        stroke_width=0, fill_color=WHITE_HL, fill_opacity=0.95).move_to([leftover_x, y_box, 0])
        leftover_box = VGroup(leftover_rect, leftover_dot)
        # Initial codon 8 spans E2's leftover base (tick 21) + first 2 bases of E3 (ticks 22-23);
        # remaining full downstream codon boxes start at tick 24 (x0 + w1 + w2 + 2 * nt_w).
        codon8_box = Rectangle(width=cw, height=0.58, stroke_color=BLUE, stroke_width=2.5,
                               fill_color=BLUE, fill_opacity=0.32).move_to([x0 + w1 + 3 * cw + 1.5 * nt_w, y_box, 0])
        e3_head_box = Rectangle(width=2 * nt_w, height=0.58, stroke_color=BLUE, stroke_width=2.5, stroke_opacity=0.0,
                                fill_color=BLUE, fill_opacity=0.0).move_to([x0 + w1 + w2 + nt_w, y_box, 0])
        e3_head_dots = VGroup(*[
            RoundedRectangle(corner_radius=0.02, width=nt_w * 0.56, height=0.58 * 0.36,
                             stroke_width=0, fill_color=TEXT, fill_opacity=0.58).move_to(
                [x0 + w1 + w2 + (b + 0.5) * nt_w, y_box, 0]
            )
            for b in range(2)
        ])
        boxes_e3_full = build_codon_boxes(x0 + w1 + w2 + 2 * nt_w, y_box, 3, nt_w=nt_w, color=BLUE)
        e3_tail_rect = Rectangle(width=nt_w, height=0.58, stroke_color=BLUE, stroke_width=2.5,
                                 fill_color=BLUE, fill_opacity=0.32).move_to([x0 + w1 + w2 + 11.5 * nt_w, y_box, 0])
        e3_tail_dot = RoundedRectangle(corner_radius=0.02, width=nt_w * 0.56, height=0.58 * 0.36,
                                       stroke_width=0, fill_color=TEXT, fill_opacity=0.58).move_to(
            [x0 + w1 + w2 + 11.5 * nt_w, y_box, 0]
        )
        e3_tail = VGroup(e3_tail_rect, e3_tail_dot)
        boxes_e3 = VGroup(e3_head_dots, boxes_e3_full, e3_tail)

        ruler = build_nt_ruler(x0, y_rul, 12, nt_w=nt_w)
        marker = build_reading_marker(boxes_e1[2].get_center()[0], y_box, codon_w=cw)
        plus1_lab = T("3 triplets + 1 leftover base", size=24, color=TEXT).move_to([0.2, -1.95, 0])

        # Start immediately with the reset transcript on screen (never a black frame!)
        self.add(cap, e1, e2, e3, tail, boxes_e1, boxes_e2_full, codon8_box, leftover_box,
                 e3_head_box, boxes_e3, ruler, marker, e2_lab)
        self.wait(0.4)
        self.at("one extra base")
        self.play(FadeIn(plus1_lab), Indicate(leftover_box, color=WHITE_HL, scale_factor=1.22), run_time=2.0)

        # Lift out 10-nt exon; slide every downstream base/boundary left by 10 nt (remainder 1)
        self.at("Every downstream boundary")
        shift_vec = LEFT * w2
        self.play(
            FadeOut(VGroup(e2, e2_lab, boxes_e2_full, leftover_box, codon8_box, plus1_lab), shift=UP * 0.45),
            run_time=0.8,
        )
        self.play(
            VGroup(e3, tail).animate.shift(shift_vec),
            boxes_e3.animate.shift(shift_vec).set_color(GOLD),
            e3_head_box.animate.shift(shift_vec).set_stroke(GOLD, width=2.5, opacity=1.0).set_fill(GOLD, opacity=0.32),
            run_time=1.5,
        )
        shift_tag = T("every downstream boundary shifted by 1 base", size=26, color=GOLD).move_to([0.0, -2.05, 0])
        self.play(FadeIn(shift_tag), run_time=0.7)

        # Reading marker meets different base groups on the fixed ruler grid
        self.at("The reading marker")
        marker_y = marker.get_center()[1]
        for k in (4, 5, 6):
            grid_cx = x0 + (k + 0.5) * cw
            self.play(marker.animate.move_to([grid_cx, marker_y, 0]), run_time=0.95, rate_func=smooth)

        # A premature stop becomes likely (drifting 'STOP ?' marker along downstream region, no definite position)
        self.at("A premature stop")
        stop_badge = boxed_label("STOP ?", RED, size=26, pad=0.12, fill_opacity=0.25)
        ds_left = x0 + w1 + 0.4
        ds_right = x0 + w1 + w3 - 0.4
        stop_badge.move_to([ds_left, 1.85, 0])
        note_seq = T("only sequence shows where", size=24, color=TEXT).move_to([0.0, -2.85, 0])
        self.play(FadeIn(stop_badge), FadeIn(note_seq), run_time=0.8)
        self.play(stop_badge.animate.move_to([ds_right, 1.85, 0]), run_time=2.6, rate_func=linear)
        self.play(stop_badge.animate.move_to([(ds_left + ds_right) / 2, 1.85, 0]), run_time=1.5, rate_func=smooth)
        self.finish()


class S10Scope(SpokenScene):
    def construct(self):
        nt_w = NT_W
        coding_w = 8 * 3 * nt_w  # 24 nt = 8 codons = 6.24
        utr5_w, utr3_w = 1.35, 1.45
        y_rna = 0.85
        y_box = -0.35
        y_rul = -0.85

        cap = make_cap()
        utr5 = make_exon(utr5_w, height=EXON_H, color=BLUE, fill_opacity=0.14)
        coding = make_exon(coding_w, "coding", height=EXON_H, color=BLUE, fill_opacity=0.38)
        utr3 = make_exon(utr3_w, height=EXON_H, color=BLUE, fill_opacity=0.14)
        tail = make_tail()
        rna_row = VGroup(cap, utr5, coding, utr3, tail).arrange(RIGHT, buff=0.08).move_to([0.0, y_rna, 0])

        coding_x0 = coding.get_left()[0]
        boxes = build_codon_boxes(coding_x0, y_box, 8, nt_w=nt_w, color=BLUE)
        ruler = build_nt_ruler(coding_x0, y_rul, 8, nt_w=nt_w)

        br_coding = Brace(coding, UP, color=BLUE, buff=0.12)
        lab_coding = T("coding sequence", size=28, color=BLUE).next_to(br_coding, UP, buff=0.12)
        test_lab = T("remainder test applies here", size=24, color=TEXT).next_to(ruler, DOWN, buff=0.14)

        self.add(rna_row, boxes, ruler, br_coding, lab_coding, test_lab)
        # Step reading marker across the 8 coding codon boxes during opening sentence
        scanner = build_reading_marker(boxes[0].get_center()[0], y_box, codon_w=3 * nt_w)
        scanner_y = scanner.get_center()[1]
        self.play(FadeIn(scanner), boxes[0][0].animate.set_fill(TEAL, opacity=0.60), run_time=0.6)
        for k in range(1, 8):
            self.play(
                scanner.animate.move_to([boxes[k].get_center()[0], scanner_y, 0]),
                boxes[k - 1][0].animate.set_fill(BLUE, opacity=0.32),
                boxes[k][0].animate.set_fill(TEAL, opacity=0.60),
                run_time=0.58, rate_func=smooth,
            )
        self.play(boxes[7][0].animate.set_fill(BLUE, opacity=0.32), FadeOut(scanner), run_time=0.5)

        # Untranslated brackets at both ends (no triplet ruler beneath them)
        self.at("untranslated")
        br_u5 = Brace(utr5, UP, color=GREY, buff=0.12)
        lab_u5 = T("untranslated", size=24, color=TEXT).next_to(br_u5, UP, buff=0.12)
        br_u3 = Brace(utr3, UP, color=GREY, buff=0.12)
        lab_u3 = T("untranslated", size=24, color=TEXT).next_to(br_u3, UP, buff=0.12)
        self.play(FadeIn(br_u5), FadeIn(lab_u5), FadeIn(br_u3), FadeIn(lab_u3), run_time=1.3)
        self.play(utr5[0].animate.set_fill(GOLD, opacity=0.55), run_time=1.1)
        self.play(utr5[0].animate.set_fill(BLUE, opacity=0.18), utr3[0].animate.set_fill(GOLD, opacity=0.55), run_time=1.2)
        self.play(utr3[0].animate.set_fill(BLUE, opacity=0.18), run_time=1.0)

        # Three neutral unanswered question tags below
        tag_y = -2.25
        tag_exp = boxed_label("export?", TEXT, size=28, pad=0.18, fill_opacity=0.10).move_to([-3.4, tag_y, 0])
        tag_dec = boxed_label("decay?", TEXT, size=28, pad=0.18, fill_opacity=0.10).move_to([0.0, tag_y, 0])
        tag_trn = boxed_label("translation?", TEXT, size=28, pad=0.18, fill_opacity=0.10).move_to([3.5, tag_y, 0])

        self.at("exported")
        self.play(FadeIn(tag_exp, shift=UP * 0.12), run_time=0.7)
        self.at("degraded")
        self.play(FadeIn(tag_dec, shift=UP * 0.12), run_time=0.7)
        self.at("translated")
        self.play(FadeIn(tag_trn, shift=UP * 0.12), run_time=0.8)

        self.at("Those fates")
        limit_lab = T("beyond a length calculation", size=26, color=GOLD).move_to([0.0, -3.12, 0])
        self.play(FadeIn(limit_lab), run_time=0.8)
        for tag in (tag_exp, tag_dec, tag_trn):
            self.play(Indicate(tag, color=GOLD, scale_factor=1.06), run_time=0.95)
        self.finish()


class S11Rules(SpokenScene):
    def construct(self):
        nt_w = NT_W
        cw = 3 * nt_w
        y_rna = 1.15
        y_box = -0.15
        y_rul = -0.62

        cap = make_cap()
        e1 = make_exon(3 * cw, "E1", height=EXON_H)
        e2 = make_exon(3 * cw, "E2", height=EXON_H)
        e3 = make_exon(4 * cw, "E3", height=EXON_H)
        tail = make_tail()
        tr = VGroup(cap, e1, e2, e3, tail).arrange(RIGHT, buff=0.08).move_to([0.0, y_rna, 0])

        a1 = join_arc(e1.get_top() + RIGHT * 0.2, e2.get_top() + LEFT * 0.2, height=0.62, color=TEAL, stroke_width=3.5)
        a2 = join_arc(e2.get_top() + RIGHT * 0.2, e3.get_top() + LEFT * 0.2, height=0.62, color=TEAL, stroke_width=3.5)
        a3 = join_arc(e1.get_top() + RIGHT * 0.2, e3.get_top() + LEFT * 0.2, height=1.00, color=TEAL, stroke_width=2.8, dashed=True)

        coding_x0 = e1.get_left()[0]
        boxes = build_codon_boxes(coding_x0, y_box, 10, nt_w=nt_w, color=BLUE)
        ruler = build_nt_ruler(coding_x0, y_rul, 10, nt_w=nt_w)
        marker = build_reading_marker(boxes[0].get_center()[0], y_box, codon_w=cw)

        rule1 = fit(VGroup(
            T("Processing marks transcript ends and", size=28, color=TEXT),
            T("chooses which segments join into mRNA.", size=28, color=TEXT),
        ).arrange(DOWN, buff=0.10), max_w=11.4).move_to([0.0, -2.45, 0.0])

        self.add(tr, rule1)
        cap_home, tail_home = cap.get_center().copy(), tail.get_center().copy()
        cap.shift(LEFT * 0.45), tail.shift(RIGHT * 0.45)
        self.at("marks transcript ends")
        self.play(cap.animate.move_to(cap_home), tail.animate.move_to(tail_home), run_time=0.9)
        self.play(cap[0].animate.set_fill(GOLD, opacity=0.55), tail[0].animate.set_fill(GOLD, opacity=0.55), run_time=0.6)
        self.play(cap[0].animate.set_fill(GOLD, opacity=0.28), tail[0].animate.set_fill(GOLD, opacity=0.28), run_time=0.6)

        self.at("chooses which segments")
        self.play(Create(a1), Create(a2), Create(a3), run_time=1.4)
        self.play(
            e1[0].animate.set_fill(TEAL, opacity=0.55),
            e2[0].animate.set_fill(TEAL, opacity=0.55),
            e3[0].animate.set_fill(TEAL, opacity=0.55),
            run_time=1.1,
        )
        self.play(
            e1[0].animate.set_fill(BLUE, opacity=0.46),
            e2[0].animate.set_fill(BLUE, opacity=0.46),
            e3[0].animate.set_fill(BLUE, opacity=0.46),
            run_time=0.9,
        )

        # Lock triplet ruler beneath coding region
        self.at("keep a second rule")
        marker_y = marker.get_center()[1]
        self.play(FadeIn(boxes), Create(ruler), FadeIn(marker), run_time=1.4)
        self.play(marker.animate.move_to([boxes[1].get_center()[0], marker_y, 0]), run_time=0.9)

        # Transform Film 1 rule -> Film 2 coding rule while reading marker steps along codons
        self.at("Coding length changes")
        rule2 = fit(VGroup(
            T("Coding-length changes keep the downstream frame", size=30, color=GOLD),
            T("only in multiples of three.", size=30, color=GOLD),
        ).arrange(DOWN, buff=0.10), max_w=11.4).move_to([0.0, -2.45, 0.0])
        self.play(swap(rule1, rule2, run_time=0.55))
        self.play(marker.animate.move_to([boxes[3].get_center()[0], marker_y, 0]), run_time=2.0)
        self.play(marker.animate.move_to([boxes[6].get_center()[0], marker_y, 0]), run_time=2.2)

        # Applies only when changed nucleotides are coding (brace BELOW ruler ticks!)
        self.at("only when")
        coding_scope = Brace(VGroup(boxes, ruler), DOWN, color=BLUE, buff=0.10)
        coding_scope_lab = T("coding nucleotides only", size=24, color=BLUE).next_to(coding_scope, DOWN, buff=0.10)
        self.play(FadeIn(coding_scope), FadeIn(coding_scope_lab),
                  marker.animate.move_to([boxes[8].get_center()[0], marker_y, 0]),
                  run_time=2.0)

        # Sequence decides the actual protein outcome
        self.at("Sequence decides")
        seq_note = T("sequence decides protein outcome", size=24, color=TEXT).move_to([0.0, -3.25, 0])
        self.play(FadeIn(seq_note), Indicate(boxes[8], color=GOLD, scale_factor=1.12),
                  Indicate(boxes[9], color=GOLD, scale_factor=1.12), run_time=2.0)

        self.at("scope of this rule")
        self.play(Indicate(rule2, color=GOLD, scale_factor=1.03), run_time=1.4)
        self.finish()


class S12End(EndCard):
    LINE = "Coding-length changes keep the downstream frame\nonly in multiples of three."
