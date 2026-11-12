"""Reading the DNA Rung (domains, kingdoms and DNA), chapter 2 of the pair.

Same world as chapter 1 (../scenes.py): the evidence ladder at the left (x -6.7..-3.9) with the DNA rung
glowing gold, the same colour map (mushroom PURPLE, oak GREEN, deer BROWN, paramecium TEAL, bacterium
ORANGE, archaeon CRIMSON) and the same cards. Protein building blocks are round beads in five muted
colours; a matching position lights gold, a non-matching one stays grey. All of it is schematic.
"""
import importlib.util
import os
from pathlib import Path

import numpy as np
from bp_style import *  # noqa: F401,F403

# ---- bring in chapter 1's look (colours, cards, ladder, bob) without copying its scene classes -------------
_here = Path(__file__).resolve().parent if "__file__" in globals() else Path(os.getcwd())
_spec = importlib.util.spec_from_file_location("film1_scenes", str(_here.parent / "scenes.py"))
_F = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_F)
for _n, _v in vars(_F).items():
    if _n.startswith("__") or (_n.startswith("S") and _n[1:3].isdigit()):
        continue
    globals().setdefault(_n, _v)
globals()["Film"] = _F.Film

BEADS = ["#d98b94", "#7fa8d9", "#e0c36a", "#86bf95", "#b49ad6"]
GREYB = "#8a93a4"
INKB = "#1d2230"


# ------------------------------------------------------------------ small builders ------------------------
def ladder(sc, glow=True, add=True):
    """Chapter 1's ladder: eyes, microscope, cell chemistry done (green), DNA the current rung (gold)."""
    L = _F.build_ladder()
    for k, r in enumerate(L.rungs):
        if k < 3:
            r[0].set_stroke(CHLO, 3).set_fill(CHLO, 0.3)
        elif glow:
            r[0].set_stroke(GOLD, 4).set_fill(GOLD, 0.5)
            _F._pulse(r[0])
    if add:
        sc.add(L)
    return L


def chain(seq, sp, r, cx, y, gap=None):
    """A protein cartoon: beads on a thread. gap=(i, j) leaves beads i..j-1 out (a deletion)."""
    n = len(seq)
    xs = [cx + (i - (n - 1) / 2) * sp for i in range(n)]
    beads = []
    for i, c in enumerate(seq):
        if gap and gap[0] <= i < gap[1]:
            continue
        beads.append(Circle(radius=r, stroke_color=INKB, stroke_width=2, fill_color=BEADS[c], fill_opacity=1).move_to([xs[i], y, 0]))
    if gap:
        segs = [Line([xs[0], y, 0], [xs[gap[0] - 1], y, 0]), Line([xs[gap[1]], y, 0], [xs[-1], y, 0])]
    else:
        segs = [Line([xs[0], y, 0], [xs[-1], y, 0])]
    for s in segs:
        s.set_stroke(GREYB, 3)
    g = VGroup(*segs, *beads)
    g.beads, g.xs, g.y, g.r = beads, xs, y, r
    return g


def colrect(ch1, ch2, i, match, pad=0.1):
    b1, b2 = ch1.beads[i], ch2.beads[i]
    top = max(b1.get_y(), b2.get_y()) + ch1.r + pad
    bot = min(b1.get_y(), b2.get_y()) - ch1.r - pad
    col = GOLD if match else GREYB
    rc = Rectangle(width=ch1.sp * 0.9, height=top - bot, stroke_width=0, fill_color=col, fill_opacity=0.5 if match else 0.5)
    rc.move_to([b1.get_x(), (top + bot) / 2, 0])
    rc.set_z_index(-1)
    return rc


def mk_chain(seq, sp, r, cx, y):
    c = chain(seq, sp, r, cx, y)
    c.sp = sp
    return c


SEQ_A = [0, 1, 2, 3, 4, 0, 1, 2, 3, 4]
SEQ_B = list(SEQ_A)
SEQ_B[3], SEQ_B[7] = 0, 4          # differs at positions 4 and 8: 8 of 10 match
SEQ_C = list(SEQ_A)
for _i, _v in [(1, 3), (4, 2), (6, 4), (9, 0)]:
    SEQ_C[_i] = _v                 # differs at 4 positions: 6 of 10 match


def match_flags(a, b):
    return [x == y for x, y in zip(a, b)]


def pulse(sc, mob, f=1.1, rt=0.8):
    sc.play(mob.animate.scale(f), rate_func=there_and_back, run_time=rt)


def dna_tape(n, sp, cx, y, seed=2, size=34, half=0.38):
    rng = np.random.RandomState(seed)
    letters = []
    for i in range(n):
        t = T("ACGT"[rng.randint(4)], size, TEXT, weight=BOLD)
        t.move_to([cx + (i - (n - 1) / 2) * sp, y, 0])
        letters.append(t)
    top = Line([-3.5, y + half, 0], [6.5, y + half, 0]).set_stroke(GREYB, 4)
    bot = Line([-3.5, y - half, 0], [6.5, y - half, 0]).set_stroke(GREYB, 4)
    g = VGroup(top, bot, *letters)
    g.letters, g.span = letters, n * sp
    return g


def scroll(tape, tr, xmin=-3.3, xmax=6.3):
    for t in tape.letters:
        def u(m, dt, t=t):
            m.shift(LEFT * tr.get_value() * dt)
            if m.get_x() < xmin - 0.3:
                m.shift(RIGHT * tape.span)
            x = m.get_x()
            m.set_opacity(float(np.clip(min((x - xmin) / 0.5, (xmax - x) / 0.5, 1.0), 0, 1)))
        t.add_updater(u)


def dashed_or_solid(a, b, solid, col=TEXT, w=6):
    if solid:
        return Line([*a, 0], [*b, 0]).set_stroke(col, w)
    return DashedLine([*a, 0], [*b, 0], dash_length=0.16).set_stroke(col, w)


# ------------------------------------------------------------------ evidence-for-A,B,C tree (s06, s07) ---
def abc_tree(solid):
    s = solid
    parts = {
        "rootv": dashed_or_solid((2.9, -1.0), (2.9, 0.9), s),
        "stub": dashed_or_solid((2.5, -0.05), (2.9, -0.05), s),
        "stem": dashed_or_solid((2.9, 0.9), (4.6, 0.9), s),
        "forkv": dashed_or_solid((4.6, 0.4), (4.6, 1.4), s),
        "a": dashed_or_solid((4.6, 1.4), (6.0, 1.4), s),
        "b": dashed_or_solid((4.6, 0.4), (6.0, 0.4), s),
        "c": dashed_or_solid((2.9, -1.0), (6.0, -1.0), s),
    }
    labs = VGroup(T("A", 32).move_to([6.4, 1.4, 0]), T("B", 32).move_to([6.4, 0.4, 0]), T("C", 32).move_to([6.4, -1.0, 0]))
    g = VGroup(*parts.values(), labs)
    g.parts, g.labs = parts, labs
    return g


BAR_BASE = -1.4
BAR_X = (-2.0, 0.4)
BAR_W = 1.3


def bar(x, h, col):
    return Rectangle(width=BAR_W, height=h, stroke_width=0, fill_color=col, fill_opacity=0.9).move_to([x, BAR_BASE + h / 2, 0])


# ------------------------------------------------------------------ EF-1 alpha rows (s08..s11) -----------
ROWY = [1.35, 0.0, -1.35]
RCOL = [BROWN, PURPLE_L, OAKG]
RNAME = ["animal", "fungus", "plant"]
_rng = np.random.RandomState(5)
BASE = [int(v) for v in _rng.randint(0, 5, 24)]
SEQ_ANIMAL = list(BASE)
SEQ_FUNGUS = list(BASE)
SEQ_FUNGUS[2], SEQ_FUNGUS[20] = (BASE[2] + 1) % 5, (BASE[20] + 2) % 5
SEQ_PLANT = list(BASE)
for _i in (1, 4, 7, 9, 12, 14, 21):
    SEQ_PLANT[_i] = (BASE[_i] + 2) % 5
RUN = (6, 18)       # the twelve beads animals and fungi share


def ef_rows(sc, plant_gap=False, add=True):
    """Three framed bead chains. Returns dict with frames, labels, chains, gold run rectangles."""
    out = {"frames": [], "labels": [], "chains": [], "gold": []}
    for k, (seq, y, col, nm) in enumerate(zip([SEQ_ANIMAL, SEQ_FUNGUS, SEQ_PLANT], ROWY, RCOL, RNAME)):
        fr = RoundedRectangle(width=9.8, height=1.2, corner_radius=0.15, stroke_color=col, stroke_width=3,
                              fill_color=col, fill_opacity=0.08).move_to([1.6, y, 0])
        lab = T(nm, 28).move_to([-3.1, y + 0.3, 0]).align_to([-3.1, 0, 0], LEFT)
        ch = chain(seq, 0.4, 0.15, 1.6, y - 0.22, gap=RUN if (k == 2 and plant_gap) else None)
        out["frames"].append(fr)
        out["labels"].append(lab)
        out["chains"].append(ch)
    xa, xb = out["chains"][0].xs[RUN[0]] - 0.2, out["chains"][0].xs[RUN[1] - 1] + 0.2
    for k in (0, 1):
        g = Rectangle(width=xb - xa, height=0.5, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.4)
        g.move_to([(xa + xb) / 2, ROWY[k] - 0.22, 0])
        g.set_z_index(-1)
        out["gold"].append(g)
    out["xa"], out["xb"] = xa, xb
    if add:
        sc.add(*out["frames"], *out["labels"], *out["chains"])
    return out


def q_card(y):
    card_ = RoundedRectangle(width=4.9, height=0.8, corner_radius=0.12, stroke_color=GOLD, stroke_width=4, fill_color=BG, fill_opacity=1)
    q = T("?", 44, GOLD)
    g = VGroup(card_, q).move_to([1.6, y - 0.22, 0])
    g.set_z_index(3)
    return g


# ------------------------------------------------------------------ eukaryote tree (s11..s13) -------------
LEAF = {"animal": 2.3, "fungus": 0.1, "plant": -2.2}


def etree():
    p = {
        "rootv": Line([-2.4, -2.2, 0], [-2.4, 1.2, 0]).set_stroke(TEXT, 6),
        "stem": Line([-2.4, 1.2, 0], [1.0, 1.2, 0]).set_stroke(TEXT, 6),
        "forkv": Line([1.0, 0.1, 0], [1.0, 2.3, 0]).set_stroke(TEXT, 6),
        "animal": Line([1.0, 2.3, 0], [4.6, 2.3, 0]).set_stroke(BROWN, 7),
        "fungus": Line([1.0, 0.1, 0], [4.6, 0.1, 0]).set_stroke(PURPLE_L, 7),
        "plant": Line([-2.4, -2.2, 0], [4.6, -2.2, 0]).set_stroke(OAKG, 7),
    }
    return p


def gold_mark():
    return Line([-0.5, 0.92, 0], [-0.5, 1.48, 0]).set_stroke(GOLD, 12)


def leaf_labels():
    return {k: T(k, 28).next_to([4.6, y, 0], RIGHT, buff=0.2) for k, y in LEAF.items()}


def leaf_cards(named=True):
    return {"animal": card("deer", (5.7, LEAF["animal"]), 0.7, named),
            "fungus": card("mush", (5.7, LEAF["fungus"]), 0.7, named),
            "plant": card("oak", (5.7, LEAF["plant"]), 0.7, named)}


def ring_at(p, r=0.32, col=GOLD):
    return Circle(radius=r, stroke_color=col, stroke_width=7).move_to([*p, 0])


# ================================================================== scenes ===============================
class S00Title(TitleCard):
    LESSON = "Domains, Kingdoms and DNA"
    TITLE = "Reading the DNA Rung"


class S01Hook(Film):
    def construct(self):
        L = ladder(self, glow=False)
        fbox = RoundedRectangle(width=3.1, height=4.3, corner_radius=0.2, stroke_color=PURPLE_L, stroke_width=4,
                                fill_color=PURPLE, fill_opacity=0.12).move_to([1.0, -0.4, 0])
        flab = T("Fungi", 32).move_to([1.0, 1.4, 0])
        mush = card("mush", (1.0, -0.4), 0.9)
        self.play(FadeIn(fbox), FadeIn(flab), FadeIn(mush, shift=DOWN * 0.3), run_time=1.2)
        bob(mush, 0.05)
        self.at("cell clues")
        pulse(self, mush, 1.06, 1.5)
        self.at("they cannot show")
        oak = card("oak", (-1.6, 2.3), 0.7)
        deer = card("deer", (4.0, 2.3), 0.7)
        l1 = DashedLine([0.2, 1.75, 0], [-0.8, 1.55, 0], dash_length=0.14).set_stroke(GOLD, 5)
        l2 = DashedLine([1.9, 1.75, 0], [3.5, 1.6, 0], dash_length=0.14).set_stroke(GOLD, 5)
        q1 = T("?", 52, GOLD).move_to([-0.6, 2.3, 0])
        q2 = T("?", 52, GOLD).move_to([2.7, 2.3, 0])
        self.play(FadeIn(oak, shift=UP * 0.2), FadeIn(deer, shift=UP * 0.2), run_time=1.0)
        bob(oak, 0.05, 2.6, 1)
        bob(deer, 0.05, 2.6, 2)
        self.play(Create(l1), Create(l2), run_time=1.2)
        self.play(FadeIn(q1, scale=0.5), FadeIn(q2, scale=0.5), run_time=0.8)
        self.play(q1.animate.scale(1.25), q2.animate.scale(1.25), run_time=0.6)
        self.play(q1.animate.scale(1 / 1.25), q2.animate.scale(1 / 1.25), run_time=0.6)
        self.at("how could the")
        tape = dna_tape(17, 0.56, 1.0, -3.2)
        link = DashedLine([1.0, -2.6, 0], [1.0, -2.85, 0], dash_length=0.1).set_stroke(GOLD, 4)
        order = sorted(range(17), key=lambda i: abs(i - 8))
        self.play(FadeIn(tape[0]), FadeIn(tape[1]), FadeIn(link), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(tape.letters[i], scale=0.5) for i in order], lag_ratio=0.12), run_time=2.0)
        self.finish()


class S02Link(Film):
    def construct(self):
        L = ladder(self, glow=False, add=False)
        for r in L.rungs:
            r[0].set_stroke(GREY, 3).set_fill(GREY, 0.1)
        self.add(L)
        boxes = []
        for key, x, col, nm in [("bact", -2.25, ORANGE, "Bacteria"), ("arch", 0.15, CRIMSON, "Archaea")]:
            b = RoundedRectangle(width=2.17, height=4.13, corner_radius=0.15, stroke_color=col, stroke_width=4,
                                 fill_color=col, fill_opacity=0.06).move_to([x, -0.2, 0])
            lb = T(nm, 26).move_to([x, 1.5, 0])
            cd = card(key, (x, 0.15), 0.63)
            boxes.append(VGroup(b, lb, cd))
            bob(cd, 0.04, 2.6, 1 if key == "bact" else 3)
        eb = RoundedRectangle(width=5.2, height=6.0, corner_radius=0.2, stroke_color=TEAL, stroke_width=4,
                              fill_color=TEAL, fill_opacity=0.06).move_to([4.05, -0.3, 0])
        et = T("Eukarya", 34).move_to([4.05, 3.25, 0])
        slots = {"mush": (2.85, 0.8), "oak": (5.25, 0.8), "deer": (2.85, -2.05), "para": (5.25, -2.05)}
        cards4 = [card(k, p, 0.55, False) for k, p in slots.items()]
        for i, c in enumerate(cards4):
            bob(c, 0.04, 2.6, i)
        self.play(FadeIn(boxes[0]), FadeIn(boxes[1]), FadeIn(eb), FadeIn(et),
                  LaggedStart(*[FadeIn(c, shift=DOWN * 0.2) for c in cards4], lag_ratio=0.2), run_time=1.0)
        self.at("climbed three rungs")
        for k in range(3):
            self.play(L.rungs[k][0].animate.set_stroke(CHLO, 3).set_fill(CHLO, 0.3), run_time=0.5)
            self.wait(0.15)
        self.at("now climb the top")
        self.play(L.rungs[3][0].animate.set_stroke(GOLD, 4).set_fill(GOLD, 0.5), run_time=0.8)
        _F._pulse(L.rungs[3][0])
        self.at("six cards")
        self.play(*[c.animate.scale(1.12) for c in cards4], rate_func=there_and_back, run_time=1.2)
        self.finish()


class S03Seq(Film):
    def construct(self):
        L = ladder(self)
        tape = dna_tape(17, 0.6, 1.5, 0.9, seed=7, size=48, half=0.5)
        tr = ValueTracker(1.4)
        scroll(tape, tr)
        self.play(FadeIn(tape[0]), FadeIn(tape[1]), *[FadeIn(t) for t in tape.letters], run_time=0.8)
        self.at("its dna")
        seqlab = T("DNA sequence", 38, GOLD).move_to([1.5, 2.2, 0])
        self.play(FadeIn(seqlab, shift=DOWN * 0.15), run_time=0.7)
        self.at("each protein is built")
        self.play(tr.animate.set_value(0.0), FadeOut(seqlab), run_time=0.4, rate_func=smooth)
        for t in tape.letters:
            t.clear_updaters()
        self.play(tape.animate.shift(UP * 0.8), run_time=0.5)
        sel = [t for t in tape.letters if 0.2 <= t.get_x() <= 3.9]
        sel.sort(key=lambda t: t.get_x())
        xa, xb = sel[0].get_x() - 0.3, sel[-1].get_x() + 0.3
        rect = Rectangle(width=xb - xa, height=1.2, stroke_color=GOLD, stroke_width=6, fill_color=GOLD, fill_opacity=0.15).move_to([(xa + xb) / 2, 1.7, 0])
        glab = T("gene", 38, GOLD).move_to([(xa + xb) / 2, 2.95, 0])
        self.play(Create(rect), *[t.animate.set_color(GOLD) for t in sel], FadeIn(glab), run_time=0.6)
        cx = (xa + xb) / 2
        prot = mk_chain([0, 1, 2, 3, 4, 0, 1, 2, 3], 0.7, 0.26, cx, -1.2)
        arrow = Arrow([cx, 1.05, 0], [cx, -0.75, 0], buff=0, color=GOLD, stroke_width=8)
        plab = T("protein (schematic)", 30).move_to([cx, -2.3, 0])
        self.at("gene's instructions")
        self.play(GrowArrow(arrow), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(b, scale=0.4) for b in prot.beads], lag_ratio=0.1), Create(prot[0]), run_time=1.0)
        self.play(FadeIn(plab, shift=UP * 0.1), run_time=0.4)
        for i, b in enumerate(prot.beads):
            bob(b, 0.05, 2.4, i * 0.7)
        self.at("so comparing proteins")
        pulse(self, prot, 1.08, 1.5)
        self.at("compare genes")
        self.play(Indicate(rect, color=GOLD, scale_factor=1.05), arrow.animate.set_color(TEXT), run_time=1.2)
        self.play(arrow.animate.set_color(GOLD), run_time=0.8)
        self.finish()


class S04Line(Film):
    def construct(self):
        L = ladder(self)
        c1 = mk_chain(SEQ_A, 0.8, 0.27, 1.6, 0.3)
        self.play(Create(c1[0]), LaggedStart(*[FadeIn(b, scale=0.4) for b in c1.beads], lag_ratio=0.18), run_time=2.4)
        self.at("amino acids")
        lab = T("amino acid", 34, GOLD).move_to([c1.xs[3], 1.4, 0])
        ln = Line([c1.xs[3], 1.12, 0], [c1.xs[3], 0.6, 0]).set_stroke(GOLD, 4)
        self.play(FadeIn(lab, shift=DOWN * 0.1), Create(ln), Indicate(c1.beads[3], color=GOLD, scale_factor=1.4), run_time=1.0)
        self.at("to compare")
        self.play(FadeOut(lab), FadeOut(ln), c1.animate.shift(UP * 1.1), run_time=0.9)
        c2 = mk_chain(SEQ_B, 0.8, 0.27, 1.6 + 6.0, -0.7)
        self.at("line up the same")
        self.add(c2)
        self.play(c2.animate.shift(LEFT * 5.2), run_time=1.4)
        self.play(c2.animate.shift(LEFT * 0.8), run_time=0.8, rate_func=smooth)
        self.at("each place in the line")
        col = Rectangle(width=0.8, height=2.3, stroke_color=GOLD, stroke_width=6).move_to([c1.xs[3], 0.35, 0])
        plab = T("position", 34, GOLD).move_to([c1.xs[3], -1.85, 0])
        self.play(Create(col), FadeIn(plab, shift=UP * 0.1), run_time=1.0)
        self.at("at each position")
        self.play(Indicate(col, color=GOLD, scale_factor=1.05), run_time=1.0)
        self.at("the building blocks match")
        fl = match_flags(SEQ_A, SEQ_B)
        rects = [colrect(c1, c2, i, f) for i, f in enumerate(fl)]
        gm = [r for r, f in zip(rects, fl) if f]
        gn = [r for r, f in zip(rects, fl) if not f]
        sw1 = Square(0.3, stroke_width=0, fill_color=GOLD, fill_opacity=0.7).move_to([-0.2, -2.9, 0])
        t1 = T("match", 30).next_to(sw1, RIGHT, buff=0.2)
        self.play(FadeOut(col), LaggedStart(*[FadeIn(r) for r in gm], lag_ratio=0.12), FadeIn(sw1), FadeIn(t1), run_time=1.1)
        self.at("or they do not")
        sw2 = Square(0.3, stroke_width=0, fill_color=GREYB, fill_opacity=0.6).move_to([2.6, -2.9, 0])
        t2 = T("no match", 30).next_to(sw2, RIGHT, buff=0.2)
        self.play(LaggedStart(*[FadeIn(r) for r in gn], lag_ratio=0.2), FadeIn(sw2), FadeIn(t2), run_time=1.0)
        self.finish()


def abc_rows(sc, ys=(1.9, 0.5, -0.9), cx=2.2):
    rows = [mk_chain(s, 0.7, 0.24, cx, y) for s, y in zip([SEQ_A, SEQ_B, SEQ_C], ys)]
    tags = []
    for nm, y in zip("ABC", ys):
        fr = RoundedRectangle(width=0.9, height=0.8, corner_radius=0.12, stroke_color=GREY, stroke_width=3,
                              fill_color=GREY, fill_opacity=0.15).move_to([-2.7, y, 0])
        tags.append(VGroup(fr, T(nm, 36).move_to(fr)))
    return rows, tags


class S05Count(Film):
    def construct(self):
        L = ladder(self)
        rows, tags = abc_rows(self)
        ml = T("made-up example", 34, GOLD).move_to([2.2, 3.1, 0])
        self.play(FadeIn(ml, shift=DOWN * 0.1), run_time=0.5)
        self.play(LaggedStart(*[AnimationGroup(Create(r[0]), LaggedStart(*[FadeIn(b, scale=0.4) for b in r.beads], lag_ratio=0.1), FadeIn(t))
                               for r, t in zip(rows, tags)], lag_ratio=0.35), run_time=2.4)
        tr = ValueTracker(0)
        cnt = T("0 of 10", 44, GOLD).move_to([2.2, -2.5, 0])

        def upd(m):
            m.become(T(f"{int(round(tr.get_value()))} of 10", 44, GOLD).move_to([2.2, -2.5, 0]))
        cnt.add_updater(upd)
        self.at("line up living thing a")
        self.add(cnt)
        fl = match_flags(SEQ_A, SEQ_B)
        rects = [colrect(rows[0], rows[1], i, f) for i, f in enumerate(fl)]
        self.play(LaggedStart(*[FadeIn(r) for r in rects], lag_ratio=0.2), tr.animate.set_value(sum(fl)), run_time=2.4, rate_func=linear)
        self.at("count the matches")
        self.play(Indicate(cnt, color=GOLD, scale_factor=1.15), run_time=1.0)
        self.at("then line up a")
        # swap B and C so that C sits under A
        self.play(FadeOut(VGroup(*rects)), tr.animate.set_value(0),
                  rows[1].animate.shift(DOWN * 1.4), rows[2].animate.shift(UP * 1.4),
                  tags[1].animate.shift(DOWN * 1.4), tags[2].animate.shift(UP * 1.4), run_time=1.0)
        fl2 = match_flags(SEQ_A, SEQ_C)
        rects2 = [colrect(rows[0], rows[2], i, f) for i, f in enumerate(fl2)]
        self.play(LaggedStart(*[FadeIn(r) for r in rects2], lag_ratio=0.15), tr.animate.set_value(sum(fl2)), run_time=1.5, rate_func=linear)
        self.finish()


class S06Rule(Film):
    def construct(self):
        L = ladder(self)
        self.at("a matches b")
        bab = bar(BAR_X[0], 8 * 0.38, GOLD)
        bac = bar(BAR_X[1], 6 * 0.38, GOLD)
        bab.set_fill(GOLD, 0.9)
        bac.set_fill(GREYB, 0.9)
        l1 = T("A and B", 30).move_to([BAR_X[0], BAR_BASE - 0.4, 0])
        l2 = T("A and C", 30).move_to([BAR_X[1], BAR_BASE - 0.4, 0])
        n1 = T("8 of 10", 30, GOLD).move_to([BAR_X[0], BAR_BASE + 8 * 0.38 + 0.4, 0])
        n2 = T("6 of 10", 30).move_to([BAR_X[1], BAR_BASE + 6 * 0.38 + 0.4, 0])
        tag = T("made-up", 30, GOLD).move_to([-0.8, 3.1, 0])
        self.play(GrowFromEdge(bab, DOWN), GrowFromEdge(bac, DOWN), FadeIn(l1), FadeIn(l2), FadeIn(tag), run_time=1.4)
        self.play(FadeIn(n1), FadeIn(n2), run_time=0.6)
        self.at("that is one clue")
        clue = T("one clue: a guess to test", 26).move_to([4.2, -2.7, 0])
        self.play(FadeIn(clue, shift=UP * 0.1), Indicate(bab, color=GOLD, scale_factor=1.05), run_time=1.0)
        self.at("a and b may share")
        tree = abc_tree(False)
        self.play(*[Create(p) for p in tree.parts.values()], FadeIn(tree.labs), run_time=1.2)
        self.at("more recent common ancestor")
        anc = VGroup(T("more recent", 28, GOLD), T("common ancestor?", 28, GOLD)).arrange(DOWN, buff=0.08).move_to([3.3, 2.65, 0])
        lead = DashedLine([4.0, 2.0, 0], [4.55, 1.0, 0], dash_length=0.12).set_stroke(GOLD, 4)
        fdot = Dot([4.6, 0.9, 0], radius=0.13, color=GOLD)
        self.play(FadeIn(anc, shift=DOWN * 0.1), Create(lead), FadeIn(fdot, scale=0.4), run_time=1.0)
        self.at("an organism both")
        self.play(Indicate(fdot, color=GOLD, scale_factor=2.5), Indicate(tree.labs[0], color=GOLD), Indicate(tree.labs[1], color=GOLD), run_time=1.5)
        self.finish()


def s06_end(sc, tree_solid=False):
    L = ladder(sc)
    bab = bar(BAR_X[0], 8 * 0.38, GOLD)
    bac = bar(BAR_X[1], 6 * 0.38, GREYB)
    l1 = T("A and B", 30).move_to([BAR_X[0], BAR_BASE - 0.4, 0])
    l2 = T("A and C", 30).move_to([BAR_X[1], BAR_BASE - 0.4, 0])
    n1 = T("8 of 10", 30, GOLD).move_to([BAR_X[0], BAR_BASE + 8 * 0.38 + 0.4, 0])
    n2 = T("6 of 10", 30).move_to([BAR_X[1], BAR_BASE + 6 * 0.38 + 0.4, 0])
    tag = T("made-up", 30, GOLD).move_to([-0.8, 3.1, 0])
    tree = abc_tree(tree_solid)
    anc = VGroup(T("more recent", 28, GOLD), T("common ancestor?", 28, GOLD)).arrange(DOWN, buff=0.08).move_to([3.3, 2.65, 0])
    lead = DashedLine([4.0, 2.0, 0], [4.55, 1.0, 0], dash_length=0.12).set_stroke(GOLD, 4)
    fdot = Dot([4.6, 0.9, 0], radius=0.13, color=GOLD)
    clue = T("one clue: a guess to test", 26).move_to([4.2, -2.7, 0])
    sc.add(bab, bac, l1, l2, n1, n2, tag, tree, anc, lead, fdot, clue)
    return dict(bab=bab, bac=bac, l1=l1, l2=l2, n1=n1, n2=n2, tag=tag, tree=tree, anc=anc, lead=lead, fdot=fdot, clue=clue)


class S07Scope(Film):
    def construct(self):
        o = s06_end(self)
        self.at("a match count")
        newtag = T("one protein: a clue", 32, GOLD).move_to([-0.8, 3.1, 0])
        self.play(Transform(o["tag"], newtag), run_time=0.9)
        self.play(o["bab"].animate.scale(1.04), o["bac"].animate.scale(1.04), rate_func=there_and_back, run_time=1.2)
        self.at("one group's version")
        self.play(Indicate(o["l2"], color=GOLD), run_time=1.0)
        self.at("can change faster")
        nb = bar(BAR_X[0], 6.4 * 0.38, GOLD)
        self.play(Transform(o["bab"], nb), o["n1"].animate.move_to([BAR_X[0], BAR_BASE + 6.4 * 0.38 + 0.4, 0]), run_time=1.8)
        self.play(FadeOut(o["n1"]), FadeOut(o["n2"]), run_time=0.5)
        self.at("so scientists build")
        rng = np.random.RandomState(11)
        rows = VGroup()
        for k in range(6):
            y = 2.6 - k * 0.8
            la, lb = rng.uniform(2.4, 3.3), rng.uniform(1.6, 2.4)
            ra = Rectangle(width=la, height=0.2, stroke_width=0, fill_color=GOLD, fill_opacity=0.9)
            rb = Rectangle(width=lb, height=0.2, stroke_width=0, fill_color=GREYB, fill_opacity=0.9)
            ra.move_to([-3.2 + la / 2, y + 0.13, 0])
            rb.move_to([-3.2 + lb / 2, y - 0.13, 0])
            rows.add(VGroup(ra, rb))
        self.play(FadeOut(VGroup(o["bab"], o["bac"], o["l1"], o["l2"], o["tag"], o["clue"])),
                  LaggedStart(*[FadeIn(r, shift=RIGHT * 0.4) for r in rows], lag_ratio=0.2), run_time=1.2)
        solid = abc_tree(True)
        self.play(FadeOut(o["anc"]), FadeOut(o["lead"]), FadeOut(o["fdot"]),
                  *[ReplacementTransform(o["tree"].parts[k], solid.parts[k]) for k in solid.parts], run_time=0.8)
        arr = Arrow([0.9, 0.0, 0], [2.3, 0.0, 0], buff=0, color=GOLD, stroke_width=8)
        self.play(GrowArrow(arr), run_time=0.4)
        self.at("many genes")
        many = T("many genes agree", 34, GOLD).move_to([-1.0, -2.6, 0])
        self.play(FadeIn(many, shift=UP * 0.1), run_time=0.8)
        pulse(self, rows, 1.05, 1.5)
        self.play(Indicate(solid.parts["forkv"], color=GOLD), run_time=1.0)
        self.finish()


class S08Study(Film):
    def construct(self):
        L = ladder(self)
        title = T("1993: Baldauf and Palmer", 38).move_to([1.6, 3.3, 0])
        rows = ef_rows(self, add=False)
        self.play(FadeIn(title, shift=DOWN * 0.15), *[FadeIn(f) for f in rows["frames"]], *[FadeIn(l) for l in rows["labels"]],
                  *[FadeIn(c) for c in rows["chains"]], run_time=1.2)
        self.at("25 proteins")
        grid = VGroup(*[RoundedRectangle(width=0.19, height=0.19, corner_radius=0.03, stroke_width=0, fill_color=TEAL, fill_opacity=0.9)
                        .move_to([-2.9 + i * 0.24, 2.45, 0]) for i in range(25)])
        pl = T("25 proteins", 30).move_to([4.9, 2.45, 0])
        self.play(LaggedStart(*[FadeIn(g, scale=0.4) for g in grid], lag_ratio=0.04), FadeIn(pl), run_time=1.5)
        self.at("from animals")
        pulse(self, rows["chains"][0], 1.03, 0.9)
        self.at("fungi")
        pulse(self, rows["chains"][1], 1.03, 0.9)
        self.at("plants")
        pulse(self, rows["chains"][2], 1.03, 0.9)
        self.at("one protein is called")
        ef = T("EF-1 alpha (schematic)", 32, GOLD).move_to([1.6, -2.6, 0])
        self.play(FadeIn(ef, shift=UP * 0.1), grid[12].animate.set_fill(GOLD, 1).scale(1.8), run_time=0.9)
        self.play(LaggedStart(*[c.animate.scale(1.03) for c in rows["chains"]], lag_ratio=0.3), rate_func=there_and_back, run_time=2.0)
        self.finish()


class S09Predict(Film):
    def construct(self):
        L = ladder(self)
        rows = ef_rows(self, plant_gap=True, add=False)
        self.play(*[FadeIn(f) for f in rows["frames"]], *[FadeIn(l) for l in rows["labels"]],
                  *[FadeIn(c) for c in rows["chains"]], run_time=0.5)
        self.at("in this protein")
        pulse(self, rows["chains"][0], 1.02, 1.0)
        self.at("share an extra")
        self.play(*[FadeIn(g) for g in rows["gold"]], run_time=1.2)
        self.at("12 building blocks")
        xa, xb = rows["xa"], rows["xb"]
        brace = Line([xa, 2.1, 0], [xb, 2.1, 0]).set_stroke(GOLD, 6)
        ticks = VGroup(Line([xa, 2.1, 0], [xa, 1.95, 0]), Line([xb, 2.1, 0], [xb, 1.95, 0])).set_stroke(GOLD, 6)
        lab = T("12 extra building blocks", 34, GOLD).move_to([(xa + xb) / 2, 2.65, 0])
        self.play(Create(brace), Create(ticks), FadeIn(lab, shift=DOWN * 0.1), run_time=1.0)
        self.play(Indicate(rows["gold"][0], color=GOLD, scale_factor=1.04), Indicate(rows["gold"][1], color=GOLD, scale_factor=1.04), run_time=1.0)
        self.at("do the plants have")
        qc = q_card(ROWY[2])
        qc.shift(UP * 1.0)
        self.add(qc)
        self.play(qc.animate.shift(DOWN * 1.0), run_time=1.0)
        self.at("decide what each answer")
        self.play(Indicate(qc, color=GOLD, scale_factor=1.06), run_time=1.0)
        self.play(qc[1].animate.scale(1.3), run_time=0.5)
        self.play(qc[1].animate.scale(1 / 1.3), run_time=0.5)
        self.finish()


def s09_end(sc):
    L = ladder(sc)
    rows = ef_rows(sc, plant_gap=True)
    sc.add(*rows["gold"])
    xa, xb = rows["xa"], rows["xb"]
    brace = Line([xa, 2.1, 0], [xb, 2.1, 0]).set_stroke(GOLD, 6)
    ticks = VGroup(Line([xa, 2.1, 0], [xa, 1.95, 0]), Line([xb, 2.1, 0], [xb, 1.95, 0])).set_stroke(GOLD, 6)
    lab = T("12 extra building blocks", 34, GOLD).move_to([(xa + xb) / 2, 2.65, 0])
    qc = q_card(ROWY[2])
    sc.add(brace, ticks, lab, qc)
    return L, rows, qc, VGroup(brace, ticks, lab)


class S10Pause(Film):
    def construct(self):
        L, rows, qc, extra = s09_end(self)
        ring0 = Circle(radius=0.4, stroke_color=GREY, stroke_width=5).move_to([6.0, -3.1, 0])
        arc = Arc(radius=0.4, start_angle=PI / 2, angle=-TAU, stroke_color=GOLD, stroke_width=8).move_to([6.0, -3.1, 0])
        self.add(ring0)
        self.play(Create(arc), qc[0].animate.set_stroke(GOLD, 8), run_time=self.narration_s - 0.4, rate_func=linear)
        self.finish()


class S11Reveal(Film):
    def construct(self):
        L, rows, qc, extra = s09_end(self)
        gap = DashedVMobject(RoundedRectangle(width=4.9, height=0.5, corner_radius=0.1, stroke_color=OAKG, stroke_width=4),
                             num_dashes=40).move_to([1.6, ROWY[2] - 0.22, 0])
        self.at("the plants did not")
        self.add(gap)
        self.play(qc.animate.stretch(0.02, 0), run_time=0.7)
        self.remove(qc)
        self.play(Indicate(gap, color=OAKG, scale_factor=1.04), FadeOut(extra), run_time=1.2)
        self.at("the simplest story")
        old = [*rows["frames"], *rows["labels"], *rows["chains"], rows["gold"][1], gap]
        tr = etree()
        self.play(*[FadeOut(m) for m in old], Create(tr["rootv"]), Create(tr["stem"]), run_time=1.5)
        mark = gold_mark()
        ml = T("one change", 30, GOLD).move_to([-1.0, 1.85, 0])
        self.play(ReplacementTransform(rows["gold"][0], mark), FadeIn(ml, shift=DOWN * 0.1), run_time=1.0)
        self.at("ancestor that animals")
        labs = leaf_labels()
        self.play(Create(tr["forkv"]), Create(tr["animal"]), Create(tr["fungus"]), FadeIn(labs["animal"]), FadeIn(labs["fungus"]), run_time=1.2)
        ring = ring_at((1.0, 1.2))
        self.play(Create(ring), run_time=0.5)
        self.play(Indicate(tr["animal"], color=GOLD, scale_factor=1.0), Indicate(tr["fungus"], color=GOLD, scale_factor=1.0), run_time=0.8)
        self.at("but plants do not")
        self.play(FadeOut(ring), Create(tr["plant"]), FadeIn(labs["plant"]), run_time=1.2)
        self.play(Indicate(tr["plant"], color=GOLD, scale_factor=1.0), run_time=1.0)
        self.at("and all four")
        chip4 = chip("4 of 4 trees: animals with fungi", GOLD, 30).move_to([2.9, -3.1, 0])
        self.play(FadeIn(chip4, shift=UP * 0.15), run_time=0.8)
        ticks = [tick(-2.8 + 0.45 * i, -3.1, CHLO).scale(0.7) for i in range(4)]
        self.at("used to draw")
        self.play(LaggedStart(*[FadeIn(t, scale=0.5) for t in ticks], lag_ratio=0.35), run_time=1.4)
        self.at("grouped animals with fungi")
        self.play(Indicate(tr["animal"], color=GOLD, scale_factor=1.0), Indicate(tr["fungus"], color=GOLD, scale_factor=1.0), Indicate(tr["forkv"], color=GOLD, scale_factor=1.0), run_time=1.4)
        self.finish()


class S12Tree(Film):
    def construct(self):
        L = ladder(self)
        tr = etree()
        mark = gold_mark()
        labs = leaf_labels()
        self.add(*tr.values(), mark, *labs.values())
        eb = RoundedRectangle(width=10.2, height=6.9, corner_radius=0.2, stroke_color=TEAL, stroke_width=4,
                              fill_color=TEAL, fill_opacity=0.05).move_to([1.65, 0.1, 0])
        et = T("Eukarya", 34).move_to([-1.9, 3.2, 0])
        self.at("so the evidence")
        self.play(Create(eb), FadeIn(et), run_time=1.0)
        self.at("this tree")
        st = T("schematic tree", 24).move_to([2.2, -1.85, 0])
        self.play(FadeIn(st), run_time=0.6)
        cards = leaf_cards()
        self.at("fungi and animals sit")
        self.play(FadeOut(labs["fungus"]), FadeIn(cards["fungus"], shift=LEFT * 0.3), run_time=1.0)
        self.play(FadeOut(labs["animal"]), FadeIn(cards["animal"], shift=LEFT * 0.3), run_time=1.0)
        self.play(Indicate(tr["animal"], color=GOLD), Indicate(tr["fungus"], color=GOLD), run_time=1.0)
        self.at("plants sit farther")
        self.play(FadeOut(labs["plant"]), FadeIn(cards["plant"], shift=LEFT * 0.3), run_time=1.0)
        self.play(Indicate(tr["plant"], color=GOLD), run_time=1.0)
        for i, c in enumerate(cards.values()):
            bob(c, 0.04, 2.6, i)
        self.at("fungi and animals share")
        r1 = ring_at((1.0, 1.2))
        self.play(Create(r1), run_time=0.8)
        self.play(Indicate(r1, color=GOLD, scale_factor=1.3), run_time=1.2)
        self.at("than either")
        r2 = ring_at((-2.4, 1.2), col=TEXT)
        self.play(Create(r2), run_time=0.8)
        self.play(Indicate(r2, color=TEXT, scale_factor=1.3), run_time=1.0)
        self.play(FadeOut(r2), FadeOut(r1), run_time=0.5)
        self.at("many other proteins")
        genes = VGroup(*[gene_strip(p, c).move_to([x, -0.55, 0]) for p, c, x in [
            ([1, 0, 1, 1, 0], PURPLE_L, -1.2), ([1, 1, 0, 1, 0], BROWN, 0.8), ([1, 0, 1, 0, 1], OAKG, 2.8)]])
        gl = T("many other proteins agree", 30, GOLD).move_to([0.9, -1.2, 0])
        self.play(LaggedStart(*[FadeIn(g, shift=UP * 0.2) for g in genes], lag_ratio=0.3), FadeIn(gl), run_time=1.2)
        self.play(Indicate(genes, color=GOLD, scale_factor=1.05), run_time=1.0)
        self.finish()


class S13Kind(Film):
    def construct(self):
        L = ladder(self)
        tr = etree()
        mark = gold_mark()
        cards = leaf_cards()
        self.add(*tr.values(), mark, *cards.values())
        for i, c in enumerate(cards.values()):
            bob(c, 0.04, 2.6, i)
        self.at("one last warning")
        pulse(self, cards["fungus"], 1.08, 1.2)
        self.at("a closer relative")
        cr = T("closer relative", 36, GOLD).move_to([-0.8, -2.95, 0])
        self.play(FadeIn(cr, shift=UP * 0.1), run_time=0.8)
        sk = T("same kind", 36).move_to([2.6, -2.95, 0])
        strike = Line([sk.get_left()[0] - 0.1, -2.95, 0], [sk.get_right()[0] + 0.1, -2.95, 0]).set_stroke(RED, 8)
        self.play(FadeIn(sk), run_time=0.6)
        self.play(Create(strike), run_time=0.7)
        self.at("fungi are closer")
        link = DashedLine([5.7, 0.9, 0], [5.7, 1.4, 0], dash_length=0.1).set_stroke(GOLD, 5)
        self.play(cards["fungus"].animate.scale(1.1), cards["animal"].animate.scale(1.1), Indicate(tr["forkv"], color=GOLD), rate_func=there_and_back, run_time=1.6)
        self.at("a mushroom is still")
        fb = RoundedRectangle(width=1.95, height=2.1, corner_radius=0.12, stroke_color=PURPLE_L, stroke_width=5).move_to([5.7, 0.1, 0])
        ab = RoundedRectangle(width=1.95, height=2.1, corner_radius=0.12, stroke_color=BROWN, stroke_width=5).move_to([5.7, 2.3, 0])
        fl = T("Fungi", 30, PURPLE_L).move_to([3.7, 0.55, 0])
        al = T("Animals", 30).move_to([3.7, 2.75, 0])
        self.play(Create(fb), FadeIn(fl), run_time=1.0)
        self.play(Create(ab), FadeIn(al), run_time=1.0)
        self.at("closer means")
        ring = ring_at((1.0, 1.2))
        self.play(Create(ring), run_time=0.8)
        self.play(Indicate(ring, color=GOLD, scale_factor=1.3), Indicate(tr["stem"], color=GOLD), run_time=1.4)
        self.finish()


class S14End(EndCard):
    LINE = "When many genes agree, they point to a more recent common ancestor."
