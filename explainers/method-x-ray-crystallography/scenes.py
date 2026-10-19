"""X-ray crystallography: finding a protein's shape in spots  (Biochemistrypedia methods film)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = the molecule and the model (always an outline, never atoms, bonds or ribbons)
  TEAL   = electron-density contours (the map)
  YELLOW = the X-ray beam, the diffraction spots, their intensity
  PURPLE = phases
  ORANGE = heavy-atom tags
  GREEN  = what works: controls, the held-out R-free set, a solved structure
  RED    = lost, unknown, or a pitfall
  GREY   = apparatus, crystal frames, labels, de-emphasised text
  GOLD   = dates and the closing rule
"""
import json
from pathlib import Path

import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
MAP_S = 1.05
MAP_C = (2.6, 0.1)
MAPS = json.loads((Path(__file__).resolve().parent / "maps.json").read_text())


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def lab(text, size=24, color=GREY, **kw):
    return T(text, size, color, **kw)


def lines(*texts, size=24, color=TEXT, buff=0.14, align=LEFT, colors=None):
    g = VGroup(*[T(t, size, (colors[i] if colors else color)) for i, t in enumerate(texts)])
    return g.arrange(DOWN, aligned_edge=align, buff=buff)


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(np.array([a[0], a[1], 0.0]), np.array([b[0], b[1], 0.0]), buff=0.0, color=color, stroke_width=w,
                 tip_length=tip, max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def blob(cx, cy, rx=1.0, ry=None, phase=0.0, color=BLUE, fill=0.14, w=3.5, n=12):
    """A closed, smooth, irregular outline: the stand-in for 'one molecule'. No internal detail."""
    ry = ry or rx
    th = np.linspace(0, 2 * np.pi, n, endpoint=False)
    rad = 1 + 0.20 * np.sin(3 * th + phase) + 0.11 * np.cos(2 * th + 2 * phase)
    pts = [np.array([cx + rx * r * np.cos(t), cy + ry * r * np.sin(t), 0.0]) for r, t in zip(rad, th)]
    pts.append(pts[0].copy())
    m = VMobject()
    m.set_points_smoothly(pts)
    m.set_stroke(color, w).set_fill(color, fill)
    return m


def drop(c, r=0.6, color=GREY):
    return Circle(radius=r, stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.08).move_to([c[0], c[1], 0])


def crystal_poly(c, r=0.5, rot=0.3, color=GREY):
    return RegularPolygon(6, radius=r, start_angle=rot, stroke_color=color, stroke_width=3, fill_color=color,
                          fill_opacity=0.28).move_to([c[0], c[1], 0])


def contours(name, s, c, color=TEAL, widths=(2.2, 3.4)):
    """Electron-density contour lines from the precomputed schematic map (maps.json)."""
    g = VGroup()
    for i, lv in enumerate(MAPS[name]):
        for line in lv["lines"]:
            if len(line) < 3:
                continue
            m = VMobject()
            m.set_points_as_corners([np.array([c[0] + x * s, c[1] + y * s, 0.0]) for x, y in line])
            m.set_stroke(color, widths[i], opacity=0.6 if i == 0 else 1.0)
            g.add(m)
    return g


def spot_pattern(c, size, seed=3, n=5):
    """Diffraction spots on a detector. Returns (detector box, list of (dot, radius from centre))."""
    rng = np.random.RandomState(seed)
    half = size / 2
    box = Rectangle(width=size, height=size, stroke_color=GREY, stroke_width=3, fill_color="#171a23", fill_opacity=1.0)
    box.move_to([c[0], c[1], 0])
    a = np.array([1.0, 0.16]); b = np.array([-0.14, 1.0])
    step = size / (2 * n + 1.2)
    spots = []
    for i in range(-n, n + 1):
        for j in range(-n, n + 1):
            if i == 0 and j == 0:
                continue
            p = (i * a + j * b) * step
            if abs(p[0]) > half - 0.12 or abs(p[1]) > half - 0.12:
                continue
            rr = np.hypot(*p) / half
            inten = 0.12 + (rng.rand() ** 1.2) * np.exp(-(rr * 1.35) ** 2)
            rad = 0.05 + 0.12 * np.sqrt(min(inten, 1.0))
            d = Dot(point=[c[0] + p[0], c[1] + p[1], 0], radius=rad, color=YELLOW).set_opacity(min(1.0, 0.3 + inten))
            spots.append((d, float(np.hypot(*p))))
    return box, spots


def tick(color=GREEN, size=32):
    return T("✓", size, color, weight=BOLD)


def cross(color=RED, size=32):
    return T("✕", size, color, weight=BOLD)


def srctag(text, color=GREY):
    return T(text, 22, color)


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Methods library"
    TITLE = "Finding a Protein's Shape in Spots"


# ---------------------------------------------------------------------------------------------
class S01Problem(SpokenScene):
    """The question is posed in the picture: an unseen fold; chemistry shows composition and sequence only."""

    def construct(self):
        q = T("Where does each atom sit?", 46, TEXT, font=TITLE_FONT).move_to([0, 3.0, 0])
        bl = DashedVMobject(blob(-3.5, -0.2, 2.0, 1.6, 0.4, BLUE, 0.0, 4), num_dashes=40)
        bfill = blob(-3.5, -0.2, 2.0, 1.6, 0.4, BLUE, 0.10, 0).set_stroke(width=0)
        qm = T("?", 110, YELLOW, weight=BOLD).move_to([-3.5, -0.2, 0])

        self.at("Where does each")
        self.play(Write(q), FadeIn(bfill), Create(bl), run_time=0.9)
        self.play(FadeIn(qm, scale=1.3), run_time=0.4)

        c1 = chip("composition", GREY, 30).move_to([3.4, 1.5, 0])
        c2 = chip("sequence", GREY, 30).move_to([3.4, 0.4, 0])
        c3 = chip("fold", RED, 30).move_to([3.4, -0.7, 0])
        t1 = tick().next_to(c1, RIGHT, buff=0.25)
        t2 = tick().next_to(c2, RIGHT, buff=0.25)
        t3 = T("?", 44, RED, weight=BOLD).next_to(c3, RIGHT, buff=0.25)
        known = lab("what chemistry gives", 24, GREY).move_to([3.4, 2.3, 0])
        self.at("Chemistry gives")
        self.play(FadeIn(known), FadeIn(c1, shift=LEFT * 0.2), FadeIn(t1), run_time=0.5)
        self.play(FadeIn(c2, shift=LEFT * 0.2), FadeIn(t2), run_time=0.4)
        self.at("not its fold")
        self.play(FadeIn(c3, shift=LEFT * 0.2), FadeIn(t3), run_time=0.5)

        pka = lab("PKA catalytic subunit", 26, BLUE).move_to([-3.5, -2.45, 0])
        yr = M("1991", 34, GOLD).move_to([-3.5, 1.8, 0])
        self.at("nobody had seen")
        self.play(FadeIn(pka, shift=UP * 0.1), FadeIn(yr, shift=DOWN * 0.1), Indicate(qm, color=YELLOW, scale_factor=1.15),
                  Indicate(t3, color=RED, scale_factor=1.3), run_time=0.8)

        fn = chip("function", GREEN, 30).move_to([3.4, -2.2, 0])
        a1 = arr([3.4, -1.25, 0], [3.4, -1.75, 0], GREEN, w=5, tip=0.18)
        rd = lab("read from shape", 24, GREEN).move_to([5.3, -1.5, 0])
        self.at("Shape tells you")
        self.play(GrowArrow(a1), FadeIn(fn, shift=UP * 0.1), FadeIn(rd), run_time=0.6)

        # clear the right column; bring the method
        self.at("In the early")
        yr2 = lab("early 1940s", 34, GOLD).move_to([3.4, 2.1, 0])
        self.play(FadeOut(VGroup(known, c1, c2, c3, t1, t2, t3, fn, a1, rd, yr)), FadeIn(yr2, shift=DOWN * 0.1), run_time=0.5)
        nm = chip("no method", RED, 32).move_to([3.4, 1.15, 0])
        nm2 = lab("for molecules of thousands of atoms", 26, GREY).move_to([3.4, 0.35, 0])
        self.at("no method")
        self.play(FadeIn(nm, scale=1.1), run_time=0.5)
        self.at("thousands of atoms")
        self.play(FadeIn(nm2, shift=UP * 0.1), run_time=0.5)
        xr = chip("X-ray crystallography", YELLOW, 32).move_to([3.4, -0.85, 0])
        ar = arr([1.3, -0.85, 0], [-1.3, -0.1, 0], YELLOW, w=6, tip=0.25)
        self.at("Kendrew judged")
        self.play(FadeIn(xr, shift=LEFT * 0.2), GrowArrow(ar), run_time=0.6)
        n1 = lab("the only one with any chance", 28, TEXT).move_to([3.4, -1.85, 0])
        self.at("only one")
        self.play(FadeIn(n1, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
LAT_COLS, LAT_ROWS = 5, 3


def lattice(cx, cy, w, h, sc=0.36, color=BLUE):
    """Many identical molecule outlines on a regular lattice (all one orientation)."""
    g = VGroup()
    for i in range(LAT_COLS):
        for j in range(LAT_ROWS):
            x = cx + (i - (LAT_COLS - 1) / 2) * w / LAT_COLS
            y = cy + (j - (LAT_ROWS - 1) / 2) * h / LAT_ROWS
            g.add(blob(x, y, sc, sc * 0.85, 0.4, color, 0.14, 2.5, 10))
    return g


class S02Crystal(SpokenScene):
    """one protein -> a crystal; many solutions screened, one crystal grows; lattice of identical molecules."""

    def construct(self):
        mol = blob(-4.0, 0.8, 1.4, 1.15, 0.4)
        mol_lbl = lab("pure protein", 26, BLUE).move_to([-4.0, -1.0, 0])
        cr = crystal_poly([2.6, 0.8], 1.7, 0.3).set_stroke(GREY, 3)
        cr_lbl = lab("crystal", 26, GREY).move_to([2.6, -1.4, 0])
        a = arr([-2.2, 0.8, 0], [0.6, 0.8, 0], GREY, w=6, tip=0.25)
        self.at("Grow the pure")
        self.play(FadeIn(mol), FadeIn(mol_lbl), run_time=0.5)
        self.play(GrowArrow(a), GrowFromCenter(cr), FadeIn(cr_lbl), run_time=1.2)

        my = chip("myoglobin", BLUE, 30).move_to([-4.0, 2.7, 0])
        notes = lines("small", "easy to prepare in quantity", "readily crystallized", size=24, color=GREY, buff=0.16) \
            .move_to([-3.2, -2.4, 0]).align_to([-6.0, 0, 0], LEFT)
        self.at("chose")
        self.play(FadeIn(my, shift=DOWN * 0.15), run_time=0.4)
        self.at("small")
        self.play(FadeIn(notes[0]), run_time=0.3)
        self.at("easy to prepare")
        self.play(FadeIn(notes[1]), run_time=0.3)
        self.at("readily")
        self.play(FadeIn(notes[2]), run_time=0.3)

        # screen of many conditions; one drop grows a crystal
        ys = [1.6, 0.0, -1.6]
        xs = [-3.6, -1.2, 1.2, 3.6]
        drops = VGroup(*[drop([x, y], 0.62) for y in ys for x in xs])
        rng = np.random.RandomState(4)
        debris = VGroup()
        for d in drops:
            for _ in range(3):
                o = rng.randn(2) * 0.2
                debris.add(Dot(d.get_center() + np.array([o[0], o[1], 0]), radius=0.035, color=GREY).set_opacity(0.6))
        win = crystal_poly([xs[2], ys[0]], 0.34, 0.3)
        cap_top = lab("good conditions are hard to predict", 28, TEXT).move_to([0, 3.2, 0])
        cap_bot = lab("screen many solutions", 30, GREEN).move_to([0, -3.15, 0])
        self.at("Good conditions")
        self.play(FadeOut(VGroup(mol, mol_lbl, my, notes, cr, cr_lbl, a)), run_time=0.4)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in drops], lag_ratio=0.04), FadeIn(debris), FadeIn(cap_top),
                  run_time=0.8)
        self.at("screen many")
        self.play(FadeIn(cap_bot), LaggedStart(*[Indicate(d, color=GREEN, scale_factor=1.15) for d in drops],
                                               lag_ratio=0.05), run_time=1.0)
        self.play(GrowFromCenter(win), drops[2].animate.set_stroke(GREEN, 4), run_time=0.5)

        # zoom into the crystal: a lattice of many copies
        frame = RoundedRectangle(corner_radius=0.2, width=8.6, height=4.7, stroke_color=GREY, stroke_width=4,
                                 fill_color=GREY, fill_opacity=0.10).move_to([0, 0.2, 0])
        lat = lattice(0, 0.2, 8.0, 4.2, 0.46)
        lat_lbl = lab("molecules in a regular lattice", 30, TEXT).move_to([0, -3.0, 0])
        self.at("Inside the crystal")
        self.play(FadeOut(drops), FadeOut(debris), FadeOut(cap_top), FadeOut(cap_bot), ReplacementTransform(win, frame),
                  run_time=0.6)
        self.play(LaggedStart(*[FadeIn(m, scale=0.6) for m in lat], lag_ratio=0.04), run_time=0.9)
        self.at("regular lattice")
        self.play(FadeIn(lat_lbl, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Beam(SpokenScene):
    """wet mounted crystal rotated in a narrow beam; scattering adds up / cancels; a pattern of spots."""

    def construct(self):
        cx, cy = -1.9, 0.4
        crys = VGroup(RoundedRectangle(corner_radius=0.1, width=1.9, height=1.9, stroke_color=GREY, stroke_width=3.5,
                                       fill_color=GREY, fill_opacity=0.15).move_to([cx, cy, 0]),
                      lattice(cx, cy, 1.5, 1.35, 0.10))
        mount = Line([cx, cy + 0.95, 0], [cx, cy + 1.9, 0], color=GREY, stroke_width=5)
        c_lbl = lab("crystal, kept wet and mounted", 24, GREY).move_to([cx - 0.2, cy + 2.4, 0])

        self.at("Keep the crystal")
        self.play(FadeIn(crys, scale=0.8), Create(mount), FadeIn(c_lbl), run_time=0.7)

        src = chip("X-ray source", YELLOW, 24).move_to([-5.2, cy, 0])
        beam = arr([-4.15, cy, 0], [cx - 1.05, cy, 0], YELLOW, w=9, tip=0.28)
        b_lbl = lab("narrow beam", 24, YELLOW).move_to([-4.5, cy - 0.8, 0])
        self.at("shine a narrow")
        self.play(FadeIn(src), GrowArrow(beam), FadeIn(b_lbl), run_time=0.7)

        self.at("rotating")
        rot = CurvedArrow([cx + 1.35, cy - 0.6, 0], [cx + 1.35, cy + 0.6, 0], angle=-PI * 0.9, color=BLUE, stroke_width=4,
                          tip_length=0.2)
        rot.set_color(GREY)
        r_lbl = lab("rotate", 24, GREY).move_to([cx, cy - 1.55, 0])
        self.play(Create(rot), FadeIn(r_lbl), Rotate(crys, angle=0.45, about_point=crys.get_center()), run_time=0.9)

        det_c = np.array([3.9, 0.4])
        box, spots = spot_pattern(det_c, 4.3, seed=5, n=5)
        det_lbl = lab("detector", 24, GREY).move_to([det_c[0], det_c[1] + 2.45, 0])
        tgt = [(det_c[0] - 2.15, det_c[1] + y) for y in (1.7, 0.85, 0.0, -0.85, -1.7)]
        fan = VGroup(*[Line([cx + 0.95, cy, 0], [t[0], t[1], 0], color=YELLOW, stroke_width=3).set_opacity(0.5) for t in tgt])
        sc_lbl = lab("electrons around each atom scatter X-rays", 24, TEXT).move_to([-0.6, -2.95, 0])
        sch3 = lab("schematic", 22, GREY).move_to([-0.6, -3.4, 0])
        self.at("scatter from")
        self.play(FadeIn(sch3), FadeOut(beam), FadeOut(b_lbl), FadeIn(box), FadeIn(det_lbl), FadeIn(sc_lbl),
                  LaggedStart(*[Create(l) for l in fan], lag_ratio=0.1), run_time=1.0)

        self.at("In some directions")
        marks = VGroup(*[tick().move_to([tgt[i][0] + 0.25, tgt[i][1], 0]) for i in (0, 2, 4)])
        add_lbl = lab("adds up", 28, GREEN).move_to([0.45, -1.6, 0])
        self.play(*[fan[i].animate.set_stroke(YELLOW, 6).set_opacity(1.0) for i in (0, 2, 4)], FadeIn(marks),
                  FadeIn(add_lbl), run_time=0.6)
        self.at("In others it cancels")
        xs = VGroup(*[cross().move_to([tgt[i][0] + 0.25, tgt[i][1], 0]) for i in (1, 3)])
        can_lbl = lab("cancels", 28, RED).move_to([0.45, -2.15, 0])
        self.play(*[fan[i].animate.set_stroke(RED, 2).set_opacity(0.45) for i in (1, 3)], FadeIn(xs), FadeIn(can_lbl),
                  run_time=0.6)

        self.at("The crystal sends")
        self.play(FadeOut(VGroup(marks, xs, add_lbl, can_lbl, sc_lbl, sch3)), fan.animate.set_opacity(0.15),
                  LaggedStart(*[FadeIn(d, scale=0.3) for d, _ in spots], lag_ratio=0.02), run_time=1.6)
        pos = lab("position: how molecules are arranged", 24, TEXT).move_to([3.0, -2.4, 0])
        inn = lab("brightness: atoms inside each molecule", 24, YELLOW).move_to([3.0, -3.05, 0])
        self.at("Their positions")
        self.play(FadeIn(pos, shift=UP * 0.1), LaggedStart(*[Indicate(d, color=TEXT, scale_factor=1.6) for d, _ in spots[::4]],
                                                           lag_ratio=0.05), run_time=0.9)
        self.at("Their intensities")
        big = sorted(spots, key=lambda s: -s[0].radius)[:6]
        self.play(FadeIn(inn, shift=UP * 0.1), LaggedStart(*[Indicate(d, color=YELLOW, scale_factor=1.8) for d, _ in big],
                                                           lag_ratio=0.08), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Phase(SpokenScene):
    """intensity recorded, phase lost (half the information); heavy atoms fix the phases; sum to a density map."""

    def construct(self):
        det_c = np.array([-3.6, 0.5])
        box, spots = spot_pattern(det_c, 3.8, seed=5, n=5)
        det_group = VGroup(box, *[d for d, _ in spots])
        self.add(det_group)
        det_lbl = lab("detector", 24, GREY).move_to([det_c[0], det_c[1] + 2.2, 0])
        self.add(det_lbl)

        picks = sorted(spots, key=lambda s: -s[0].radius)[:4]
        rowy = [1.55, 0.5, -0.55, -1.6]
        rings = VGroup(*[Circle(radius=d.radius + 0.12, color=TEXT, stroke_width=2.5).move_to(d.get_center()) for d, _ in picks])
        widths = [2.3, 1.5, 1.9, 0.9]
        rows_spot = VGroup(*[Dot(point=[0.9, y, 0], radius=0.12, color=YELLOW) for y in rowy])
        bars = VGroup(*[Rectangle(width=w, height=0.3, stroke_width=0, fill_color=YELLOW, fill_opacity=0.9)
                        .move_to([1.7 + w / 2, y, 0]) for w, y in zip(widths, rowy)])
        h_int = lab("intensity", 24, YELLOW).move_to([2.9, 2.5, 0])
        h_ph = lab("phase", 24, PURPLE).move_to([5.3, 2.5, 0])
        h_sp = lab("spot", 24, GREY).move_to([0.9, 2.5, 0])
        rec = lab("recorded", 24, GREEN).move_to([2.9, -2.35, 0])

        self.at("The detector records")
        self.play(Create(rings), FadeIn(h_sp), FadeIn(rows_spot), run_time=0.6)
        self.play(FadeIn(h_int), LaggedStart(*[GrowFromEdge(b, LEFT) for b in bars], lag_ratio=0.15), FadeIn(rec),
                  run_time=0.8)

        lost = VGroup(*[VGroup(DashedVMobject(Circle(radius=0.3, stroke_color=RED, stroke_width=3).move_to([5.3, y, 0]), num_dashes=14),
                               T("?", 30, RED, weight=BOLD).move_to([5.3, y, 0])) for y in rowy])
        lost_lbl = lab("phase: lost", 24, RED).move_to([5.3, -2.35, 0])
        self.at("The phase of each")
        self.play(FadeIn(h_ph), FadeIn(lost), FadeIn(lost_lbl), run_time=0.4)

        half = VGroup(Rectangle(width=2.6, height=0.4, stroke_width=0, fill_color=YELLOW, fill_opacity=0.9).move_to([-4.9, -3.0, 0]),
                      DashedVMobject(Rectangle(width=2.6, height=0.4, stroke_color=RED, stroke_width=3).move_to([-2.3, -3.0, 0]),
                                     num_dashes=30))
        h1 = lab("intensity", 22, YELLOW).move_to([-4.9, -3.0, 0]).set_color("#0f1117")
        h2 = lab("phase missing", 22, RED).move_to([-2.3, -3.0, 0])
        hl = lab("half the information for the image", 24, TEXT).move_to([-3.6, -2.45, 0])
        self.at("half the information")
        self.play(FadeIn(half), FadeIn(h1), FadeIn(h2), FadeIn(hl), run_time=0.7)
        for _ in range(2):
            self.play(Indicate(half[1], color=RED, scale_factor=1.08), Indicate(h2, color=RED, scale_factor=1.15), run_time=1.1)

        # heavy atoms: native crystal, then two heavy-atom crystals
        bx = [-5.4, -3.5, -1.6]
        nat = blob(bx[0], 0.6, 0.62, 0.5, 0.4)
        het1 = blob(bx[1], 0.6, 0.62, 0.5, 0.4)
        het2 = blob(bx[2], 0.6, 0.62, 0.5, 0.4)

        def tg(cx, offs):
            return VGroup(*[Square(side_length=0.22, stroke_color=ORANGE, stroke_width=2.5, fill_color=ORANGE, fill_opacity=0.9)
                            .move_to([cx + dx, 0.6 + dy, 0]) for dx, dy in offs])
        tags1 = tg(bx[1], ((-0.75, 0.05), (0.2, 0.62), (0.62, -0.42)))
        tags2 = tg(bx[2], ((-0.3, -0.6), (0.78, 0.2), (-0.55, 0.5)))
        nat_lbl = lines("native", "crystal", size=20, color=GREY, buff=0.04, align=ORIGIN).move_to([bx[0], -0.5, 0])
        het1_lbl = lines("heavy-atom", "crystal 1", size=20, color=ORANGE, buff=0.04, align=ORIGIN).move_to([bx[1], -0.5, 0])
        het2_lbl = lines("heavy-atom", "crystal 2", size=20, color=ORANGE, buff=0.04, align=ORIGIN).move_to([bx[2], -0.5, 0])
        hv = lab("heavy atom, for example mercury,", 24, ORANGE).move_to([-3.5, -1.3, 0])
        hv2 = lab("at a few sites", 24, ORANGE).move_to([-3.5, -1.75, 0])
        self.at("solved it")
        self.play(FadeOut(VGroup(det_group, det_lbl, rings, half, h1, h2, hl)), FadeIn(nat), FadeIn(nat_lbl), run_time=0.6)
        self.at("heavy atoms")
        self.play(FadeIn(het1), FadeIn(het1_lbl), run_time=0.5)
        self.at("for example")
        self.play(FadeIn(hv), run_time=0.4)
        self.at("attached at")
        self.play(FadeIn(hv2), LaggedStart(*[GrowFromCenter(t) for t in tags1], lag_ratio=1.0), run_time=2.0)

        ticks = VGroup()
        for w, y in zip(widths, rowy):
            for k, dw in enumerate((0.45, -0.35)):
                x = 1.7 + w + dw
                ticks.add(Line([x, y - 0.25, 0], [x, y + 0.25, 0], color=ORANGE, stroke_width=5 if k == 0 else 3))
        t_lbl = lab("heavy-atom crystals change the intensities", 24, ORANGE).move_to([2.9, 3.05, 0])
        self.at("Two or more")
        self.play(FadeIn(het2), FadeIn(het2_lbl), run_time=0.5)
        self.play(LaggedStart(*[GrowFromCenter(t) for t in tags2], lag_ratio=0.6), run_time=0.9)
        self.play(FadeIn(t_lbl), LaggedStart(*[Create(t) for t in ticks], lag_ratio=0.1), FadeOut(rec), run_time=0.7)

        fixed = VGroup()
        for y, ang in zip(rowy, (0.5, 2.2, 3.7, 5.1)):
            c = Circle(radius=0.3, stroke_color=GREEN, stroke_width=3).move_to([5.3, y, 0])
            ndl = Line(c.get_center(), c.get_center() + 0.26 * np.array([np.cos(ang), np.sin(ang), 0]), color=GREEN, stroke_width=4)
            fixed.add(VGroup(c, ndl))
        ok_lbl = lab("phase: fixed", 24, GREEN).move_to([5.3, -2.35, 0])
        self.at("fix the phases")
        self.play(FadeOut(lost), FadeOut(lost_lbl), FadeIn(fixed), FadeIn(ok_lbl), run_time=0.4)

        # add up all the spots as waves -> density map
        self.at("Add up all")
        xs = np.linspace(-6.0, -3.0, 80)
        waves = VGroup()
        cols = (YELLOW, ORANGE, PURPLE)
        for k, (amp, fr, ph) in enumerate(((0.35, 5.0, 0.0), (0.25, 9.0, 1.3), (0.2, 14.0, 2.4))):
            m = VMobject()
            m.set_points_as_corners([np.array([x, 1.9 - 1.1 * k + amp * np.sin(fr * (x + 6.0) + ph), 0.0]) for x in xs])
            m.set_stroke(cols[k], 3)
            waves.add(m)
        dots = lab("…", 34, GREY).move_to([-4.5, -1.4, 0])
        arr_sum = arr([-2.8, 0.4, 0], [-1.7, 0.4, 0], TEXT, w=6, tip=0.25)
        self.play(FadeOut(VGroup(nat, nat_lbl, het1, het1_lbl, het2, het2_lbl, tags1, tags2, hv, hv2, bars, ticks, rows_spot,
                                 h_int, h_ph, h_sp, fixed, ok_lbl, t_lbl)),
                  FadeIn(waves), FadeIn(dots), run_time=0.7)
        dmap = contours("fine", MAP_S, MAP_C)
        m_lbl = lab("electron-density map", 28, TEAL).move_to([2.6, 3.15, 0])
        sch = lab("schematic", 22, GREY).move_to([5.7, 3.15, 0])
        self.at("electron density map")
        self.play(GrowArrow(arr_sum), FadeIn(m_lbl), LaggedStart(*[Create(m) for m in dmap], lag_ratio=0.02), FadeIn(sch),
                  run_time=1.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
def mp(x, y, s=MAP_S, c=MAP_C):
    return np.array([c[0] + x * s, c[1] + y * s, 0.0])


class S05Reading(SpokenScene):
    """contour map; model fitted and refined; resolution = how far out the spots go; myoglobin at 6, 2, 1.4 A."""

    def construct(self):
        fine = contours("fine", MAP_S, MAP_C)
        m_lbl = lab("electron-density map", 28, TEAL).move_to([2.6, 3.15, 0])
        sch = lab("schematic", 22, GREY).move_to([5.7, 3.15, 0])
        self.add(fine, m_lbl, sch)

        # model outline fitted into the map
        pts = [(-3.35, 1.2), (-3.0, 2.1), (-1.6, 2.3), (-0.3, 2.0), (0.6, 2.2), (2.2, 2.3), (3.3, 1.6), (3.2, 0.6),
               (2.7, -0.2), (2.8, -1.7), (1.0, -1.9), (0.3, -1.1), (-0.5, -1.6), (-2.2, -1.6), (-3.0, -0.5)]
        outline = VMobject()
        wp = [mp(x, y) for x, y in pts]
        wp.append(wp[0].copy())
        outline.set_points_smoothly(wp)
        outline.set_stroke(BLUE, 4).set_fill(BLUE, 0.07)
        mdl = lab("model", 28, BLUE).move_to([2.6, 3.15, 0])

        self.at("Read the map")
        self.play(Indicate(fine, color=TEAL, scale_factor=1.03), run_time=0.8)
        self.at("Build a model")
        self.play(Create(outline), FadeOut(m_lbl), FadeIn(mdl), run_time=0.8)
        pts2 = [(x + 0.07 * np.sin(3 * i), y + 0.06 * np.cos(2 * i)) for i, (x, y) in enumerate(pts)]
        wp2 = [mp(x, y) for x, y in pts2]
        wp2.append(wp2[0].copy())
        outline2 = VMobject()
        outline2.set_points_smoothly(wp2)
        outline2.set_stroke(BLUE, 4).set_fill(BLUE, 0.07)
        rf = lab("refined", 28, GREEN).move_to([2.6, 3.15, 0])
        self.at("and refine it")
        self.play(Transform(outline, outline2), ReplacementTransform(mdl, rf), run_time=0.7)

        # resolution
        det_c = np.array([-3.9, 0.3])
        box, spots = spot_pattern(det_c, 4.3, seed=5, n=5)
        dim = [d for d, _ in spots]
        for d in dim:
            d.set_color(GREY).set_opacity(0.3)
        det_lbl = lab("diffraction pattern", 24, GREY).move_to([det_c[0], det_c[1] + 2.5, 0])
        self.at("spots carry")
        self.play(FadeOut(outline), FadeOut(rf), FadeIn(box), FadeIn(det_lbl), FadeIn(VGroup(*dim)), run_time=0.8)

        def ring(r, col=YELLOW):
            return Circle(radius=r, stroke_color=col, stroke_width=3.5).move_to([det_c[0], det_c[1], 0])

        litd = [(Dot(point=d.get_center(), radius=d.radius, color=YELLOW).set_opacity(0.95), r) for d, r in spots]
        r6, r2, r14 = 0.95, 1.75, 2.15
        inner = [d for d, r in litd if r <= r6]
        outer = [d for d, r in litd if r6 < r <= r2]
        far = [d for d, r in litd if r2 < r <= r14]
        circ = ring(r2)
        res_lbl = lab("resolution limit", 24, YELLOW).move_to([det_c[0], det_c[1] - 2.5, 0])
        self.at("so resolution depends")
        self.play(Create(circ), FadeIn(res_lbl), *[FadeIn(d) for d in inner + outer], run_time=0.9)
        self.at("how far out")
        self.play(Transform(circ, ring(r14)), *[FadeIn(d) for d in far], run_time=1.4)
        self.play(Transform(circ, ring(r2)), *[FadeOut(d) for d in far], run_time=1.4)

        # 6 A
        coarse = contours("coarse", MAP_S, MAP_C)
        res_num = M("6 Å", 44, TEXT, weight=BOLD).move_to([det_c[0], -3.0, 0])
        self.at("six angstroms")
        self.play(Transform(circ, ring(r6)), *[FadeOut(d) for d in outer],
                  FadeTransform(fine, coarse), FadeIn(res_num, shift=UP * 0.1), run_time=0.9)
        rod_a = lab("rods of chain", 26, TEAL).move_to([0.0, 3.15, 0])
        disc_a = lab("one flat disc: the haem", 26, TEAL).move_to([3.3, -2.45, 0])
        rod_arrow = arr([0.3, 2.75, 0], mp(-2.0, 1.5), TEAL, w=3, tip=0.15)
        disc_arrow = arr([3.9, -2.15, 0], [4.2, -1.65, 0], TEAL, w=3, tip=0.15)
        self.at("rods of chain")
        self.play(FadeIn(rod_a), GrowArrow(rod_arrow), run_time=0.5)
        self.at("flat")
        self.play(FadeIn(disc_a), GrowArrow(disc_arrow), run_time=0.5)

        # 2 A
        res2 = M("2 Å", 44, TEXT, weight=BOLD).move_to([det_c[0], -3.0, 0])
        self.at("two angstroms")
        self.play(FadeOut(VGroup(rod_a, disc_a, rod_arrow, disc_arrow)), Transform(circ, ring(r2)),
                  *[FadeIn(d) for d in outer], FadeTransform(coarse, fine), ReplacementTransform(res_num, res2), run_time=0.9)
        hel = lab("helices: hollow cylinders", 26, TEAL).move_to([1.2, 3.15, 0])
        hel_arrow = arr([0.4, 2.75, 0], mp(-2.0, 1.5), TEAL, w=3, tip=0.15)
        iron = lines("iron out of the", "haem plane", size=24, color=ORANGE, buff=0.06, align=ORIGIN).move_to([5.5, -2.1, 0])
        iron_arrow = arr([5.5, -1.6, 0], [5.0, -0.55, 0], ORANGE, w=3, tip=0.15)
        self.at("helices appear")
        self.play(FadeIn(hel), GrowArrow(hel_arrow), run_time=0.5)
        self.at("the iron sits")
        self.play(FadeIn(iron), GrowArrow(iron_arrow), run_time=0.5)

        # 1.4 A
        res14 = M("1.4 Å", 44, TEXT, weight=BOLD).move_to([det_c[0], -3.0, 0])
        hi_lbl = lines("bonded neighbours:", "only just resolved", size=24, color=TEAL, buff=0.06).move_to([3.0, -2.3, 0])
        lim = lab("the limit for these crystals", 24, GREY).move_to([2.6, -3.1, 0])
        self.at("1 4 angstroms")
        self.play(FadeOut(VGroup(hel, hel_arrow, iron, iron_arrow, res_lbl)), Transform(circ, ring(r14)),
                  *[FadeIn(d) for d in far], ReplacementTransform(res2, res14), run_time=0.8)
        self.play(FadeIn(hi_lbl, shift=UP * 0.1), run_time=0.6)
        self.at("the limit for these")
        self.play(FadeIn(lim, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Pitfalls(SpokenScene):
    """no crystal; model bias; R-free from a held-out tenth."""

    def construct(self):
        # left panel: no crystal
        title_l = chip("no diffracting crystal", RED, 26).move_to([-3.45, 3.0, 0])
        drops = VGroup(*[drop([-5.2 + 1.75 * i, 1.4], 0.55) for i in range(3)])
        xs = VGroup(*[cross(RED, 38).move_to(d.get_center()) for d in drops])
        brr = lab("often the chief barrier", 24, GREY).move_to([-3.45, 0.45, 0])
        self.at("No crystal")
        self.play(FadeIn(title_l, shift=DOWN * 0.1), FadeIn(drops), FadeIn(xs), run_time=0.7)
        self.at("chief barrier")
        self.play(FadeIn(brr), run_time=0.4)

        w1 = chip("screen many conditions", GREEN, 26).move_to([-3.45, -0.55, 0])
        w2 = chip("add a binding partner", GREEN, 26).move_to([-3.45, -1.65, 0])
        self.at("Screen many")
        self.play(FadeIn(w1, shift=RIGHT * 0.2), run_time=0.5)
        self.at("binding partner")
        self.play(FadeIn(w2, shift=RIGHT * 0.2), run_time=0.5)
        win = crystal_poly(drops[2].get_center(), 0.3, 0.3)
        self.play(FadeOut(xs[2]), GrowFromCenter(win), drops[2].animate.set_stroke(GREEN, 4), run_time=0.6)

        # right panel: model bias loop
        title_r = chip("phases are weak too", PURPLE, 26).move_to([3.6, 3.0, 0])
        cm = chip("model", BLUE, 26).move_to([1.6, 2.0, 0])
        cp = chip("phases", PURPLE, 26).move_to([3.4, 2.0, 0])
        cd = chip("map", TEAL, 26).move_to([5.2, 2.0, 0])
        a1 = arr(cm.get_right() + [0.05, 0, 0], cp.get_left() + [-0.05, 0, 0], GREY, w=4, tip=0.15)
        a2 = arr(cp.get_right() + [0.05, 0, 0], cd.get_left() + [-0.05, 0, 0], GREY, w=4, tip=0.15)
        back = CurvedArrow([5.2, 1.65, 0], [1.6, 1.65, 0], angle=-PI * 0.45, color=RED, stroke_width=4, tip_length=0.2)
        bias = lab("shows density where the model has it: bias", 22, RED).move_to([3.4, 0.75, 0])
        self.at("A map made")
        self.play(FadeIn(title_r, shift=DOWN * 0.1), FadeIn(cm), GrowArrow(a1), FadeIn(cp), GrowArrow(a2), FadeIn(cd), run_time=0.9)
        self.at("tends to show")
        self.play(Create(back), FadeIn(bias), run_time=0.8)

        bad = chip("incorrect model", RED, 22, pad=0.15).move_to([1.65, -0.15, 0])
        good = chip("R value fairly good", RED, 22, pad=0.15).move_to([4.85, -0.15, 0])
        ba = arr(bad.get_right() + [0.05, 0, 0], good.get_left() + [-0.05, 0, 0], RED, w=4, tip=0.15)
        self.at("incorrect model")
        self.play(FadeIn(bad), GrowArrow(ba), FadeIn(good), run_time=0.8)

        # R-free: ten percent held out
        cells = VGroup()
        for k in range(20):
            col, row = k % 10, k // 10
            cells.add(Square(side_length=0.42, stroke_color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=0.3)
                      .move_to([1.3 + 0.46 * col, -1.9 - 0.46 * row, 0]))
        held = VGroup(cells[7], cells[16])
        c_lbl = lab("spots", 24, GREY).move_to([3.6, -1.3, 0])
        self.at("leave about")
        self.play(FadeIn(c_lbl), LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.03), run_time=0.8)
        self.play(*[h.animate.set_stroke(GREEN, 4).set_fill(GREEN, 0.7) for h in held], run_time=0.5)
        left = lab("left out: about 10%", 24, GREEN).move_to([3.6, -3.1, 0])
        self.at("of the spots")
        self.play(FadeIn(left), run_time=0.4)
        self.at("free value")
        rfree = chip("R-free guards against over-fitting", GREEN, 22).move_to([-3.45, -3.0, 0])
        self.play(FadeIn(rfree, shift=UP * 0.1), Indicate(held, color=GREEN, scale_factor=1.3), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07Myo(SpokenScene):
    """myoglobin (first protein structure) and haemoglobin (two subunits farther apart)."""

    def construct(self):
        t1 = chip("myoglobin", BLUE, 30).move_to([-3.3, 3.0, 0])
        mol = blob(-3.3, 0.6, 1.7, 1.4, 0.9)
        first = lab("late 1950s: first protein structure", 26, TEXT).move_to([-3.3, -1.5, 0])
        s1 = srctag("Kendrew and colleagues").move_to([-3.3, -3.1, 0])
        self.at("In the late")
        self.play(FadeIn(t1, shift=DOWN * 0.1), FadeIn(mol, scale=0.85), FadeIn(first, shift=UP * 0.1), FadeIn(s1), run_time=0.8)
        two = M("1960: 2 Å map published", 26, GOLD).move_to([-3.3, -2.2, 0])
        self.at("A two angstrom")
        self.play(FadeIn(two, shift=UP * 0.1), run_time=0.5)

        t2 = chip("haemoglobin", BLUE, 30).move_to([3.4, 3.0, 0])
        a1 = blob(0.95, 1.0, 0.45, 0.45, 0.2)
        a2 = blob(2.05, 1.0, 0.45, 0.45, 1.0)
        b1 = blob(4.0, 1.0, 0.45, 0.45, 0.2)
        b2 = blob(5.85, 1.0, 0.45, 0.45, 1.0)
        l_ox = lines("oxygen-carrying", "horse", size=22, color=GREY, buff=0.06, align=ORIGIN).move_to([1.5, -0.05, 0])
        l_no = lines("oxygen-free", "human", size=22, color=GREY, buff=0.06, align=ORIGIN).move_to([4.95, -0.05, 0])
        sc7 = lab("two beta subunits (schematic)", 22, GREY).move_to([3.4, 2.15, 0])
        self.at("Perutz compared")
        self.play(FadeIn(t2, shift=DOWN * 0.1), FadeIn(sc7), run_time=0.5)
        self.at("horse hemoglobin")
        self.play(FadeIn(VGroup(a1, a2)), FadeIn(l_ox), run_time=0.5)
        self.at("human hemoglobin")
        self.play(FadeIn(VGroup(b1, b2)), FadeIn(l_no), run_time=0.5)
        dbl = DoubleArrow([4.5, 1.0, 0], [5.4, 1.0, 0], buff=0, color=YELLOW, stroke_width=4, tip_length=0.15)
        mv_lbl = lab("separation changes by over 7 Å", 24, YELLOW).move_to([3.4, -0.95, 0])
        self.at("subunits rearranged")
        self.play(Indicate(VGroup(a1, a2), color=TEXT, scale_factor=1.1), Indicate(VGroup(b1, b2), color=TEXT, scale_factor=1.1),
                  run_time=0.6)
        self.at("separation")
        self.play(GrowArrow(dbl), FadeIn(mv_lbl), run_time=0.6)
        q = lab("quaternary structure differs", 28, TEXT).move_to([3.4, -1.7, 0])
        s2 = srctag("Perutz, 5.5 Å").move_to([3.4, -3.1, 0])
        self.at("quaternary structure")
        self.play(FadeIn(q, shift=UP * 0.1), FadeIn(s2), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S08Unlocked(SpokenScene):
    """first kinase (two lobes, cleft) and KcsA (selectivity filter), then the rule."""

    def construct(self):
        t1 = chip("PKA, the first protein kinase", BLUE, 28).move_to([-3.3, 3.0, 0])
        small = blob(-3.3, 1.65, 1.25, 0.7, 0.5)
        large = blob(-3.3, -1.2, 1.9, 0.95, 1.3)
        cleft = arr([-1.3, 0.4, 0], [-2.4, 0.4, 0], YELLOW, w=4, tip=0.18)
        cl_lbl = lab("a cleft", 26, YELLOW).move_to([-0.55, 0.4, 0])
        lobes = lab("two lobes", 26, TEXT).move_to([-3.3, -2.6, 0])
        s1 = srctag("Knighton, Taylor, Sowadski et al., 1991").move_to([-3.3, -3.1, 0])
        res1 = M("2.7 Å", 28, GOLD).move_to([-0.9, 1.9, 0])
        self.at("solved the first")
        self.play(FadeIn(t1, shift=DOWN * 0.1), FadeIn(small, shift=DOWN * 0.2), FadeIn(large, shift=UP * 0.2),
                  FadeIn(s1), FadeIn(res1), run_time=0.8)
        self.at("two lobes")
        self.play(FadeIn(lobes), run_time=0.4)
        self.at("with a cleft")
        self.play(GrowArrow(cleft), FadeIn(cl_lbl), run_time=0.6)

        t2 = chip("KcsA, a potassium channel", BLUE, 28).move_to([3.4, 3.0, 0])
        mem_l = RoundedRectangle(corner_radius=0.08, width=1.3, height=0.5, stroke_color=GREY, stroke_width=2.5, fill_color=GREY,
                                 fill_opacity=0.3).move_to([1.85, 0.7, 0])
        mem_r = mem_l.copy().move_to([4.15, 0.7, 0])
        pw = RoundedRectangle(corner_radius=0.1, width=0.5, height=2.2, stroke_color=BLUE, stroke_width=3, fill_color=BLUE,
                              fill_opacity=0.3)
        pl = pw.copy().move_to([2.74, 0.7, 0])
        pr = pw.copy().move_to([3.26, 0.7, 0])
        filt = DoubleArrow([5.2, 0.95, 0], [5.2, 1.8, 0], buff=0, color=YELLOW, stroke_width=3, tip_length=0.15)
        f_lbl = lab("selectivity filter", 24, YELLOW).move_to([4.7, 2.3, 0])
        l12 = M("12 Å", 26, YELLOW).move_to([5.85, 1.38, 0])
        mem_lbl = lab("membrane", 22, GREY).move_to([1.5, 0.1, 0])
        s2 = srctag("MacKinnon lab, 1998 (3.2 Å)").move_to([3.4, -3.1, 0])
        self.at("potassium channel")
        self.play(FadeIn(t2, shift=DOWN * 0.1), FadeIn(VGroup(mem_l, mem_r, pl, pr, mem_lbl)), FadeIn(s2), run_time=0.8)
        self.at("selectivity filter")
        self.play(Create(filt), FadeIn(f_lbl), FadeIn(l12), run_time=0.7)

        # the rule
        panels = VGroup(t1, small, large, cleft, cl_lbl, lobes, s1, res1, t2, mem_l, mem_r, pl, pr, filt, f_lbl, l12, mem_lbl, s2)
        k = lab("Keep this rule", 28, GOLD).move_to([0, 1.5, 0])
        r1 = T("A shape in a crystal is a clue,", 44, TEXT, font=TITLE_FONT)
        r2 = T("so test it in cells.", 44, GOLD, font=TITLE_FONT)
        rule = VGroup(r1, r2).arrange(DOWN, buff=0.25).move_to([0, 0.1, 0])
        box = SurroundingRectangle(rule, color=GOLD, buff=0.45, corner_radius=0.2, stroke_width=3)
        self.at("Keep this rule")
        self.play(FadeOut(panels), run_time=0.4)
        self.play(FadeIn(k, shift=DOWN * 0.1), run_time=0.3)
        self.at("A shape in")
        self.play(FadeIn(r1, shift=UP * 0.1), Create(box), run_time=0.6)
        self.at("so test it")
        self.play(FadeIn(r2, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S09End(EndCard):
    LINE = "A shape in a crystal is a clue; test it in cells."
