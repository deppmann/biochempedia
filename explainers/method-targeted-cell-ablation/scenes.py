"""Targeted cell ablation: remove one cell type, see what fails  (Biochemistrypedia methods film)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  GREEN  = the chosen target cells (the ones you mean to remove)
  GREY   = every other cell, structure, tissue, de-emphasised text
  TEAL   = read-out cells that carry on (germ cells, stem cells)
  RED    = missing / killed (dashed ghost outline, minus mark), pitfalls, the STOP cassette
  ORANGE = diphtheria toxin
  PURPLE = the human toxin receptor
  BLUE   = apparatus and driver (laser box, syringe, Cre)
  YELLOW = laser beam and light, and the measured values
  GOLD   = years and the closing rule
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
CAP_COL = TEXT


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def lab(text, size=24, color=GREY, **kw):
    return T(text, size, color, **kw)


def lines(*texts, size=24, color=TEXT, buff=0.14, align=LEFT, colors=None):
    g = VGroup(*[T(t, size, (colors[i] if colors else color)) for i, t in enumerate(texts)])
    return g.arrange(DOWN, aligned_edge=align, buff=buff)


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def shape(kind, x, y, r=0.32):
    if kind == "c":
        m = Circle(radius=r)
    elif kind == "s":
        m = RoundedRectangle(corner_radius=r * 0.3, width=2 * r * 0.92, height=2 * r * 0.92)
    elif kind == "d":
        m = Square(side_length=2 * r * 0.85).rotate(PI / 4)
    else:
        m = RegularPolygon(n=6, radius=r * 1.05)
    return m.move_to([x, y, 0])


def cell(kind, x, y, r=0.32, color=GREY, fill=0.14, sw=2.6):
    m = shape(kind, x, y, r)
    m.set_stroke(color, sw).set_fill(color, fill)
    return m


def ghost(kind, x, y, r=0.32, sw=3.0, n=12):
    m = shape(kind, x, y, r).set_fill(opacity=0).set_stroke(RED, sw)
    return DashedVMobject(m, num_dashes=n)


def minus(x, y, w=0.26, color=RED):
    return Line([x - w / 2, y, 0], [x + w / 2, y, 0], color=color, stroke_width=5)


def xmark(x, y, s=0.2, color=RED, w=5):
    return VGroup(Line([x - s, y - s, 0], [x + s, y + s, 0], color=color, stroke_width=w),
                  Line([x - s, y + s, 0], [x + s, y - s, 0], color=color, stroke_width=w))


def recmark(x, y, r=0.32, ang=90, w=0.24):
    """A little purple receptor stub on a cell edge."""
    a = np.deg2rad(ang)
    px, py = x + (r + 0.06) * np.cos(a), y + (r + 0.06) * np.sin(a)
    m = Rectangle(width=w, height=0.14, stroke_width=0, fill_color=PURPLE, fill_opacity=1.0)
    m.rotate(a - PI / 2).move_to([px, py, 0])
    return m


def dot(x, y, color=ORANGE, r=0.09):
    return Dot([x, y, 0], radius=r, color=color)


def capline(text, color=CAP_COL, size=28, pos=(0, 3.3)):
    t = T(text, size, color)
    fit(t, max_w=SAFE_W)
    return t.move_to([pos[0], pos[1], 0])


def tagline(text, pos, color=GOLD, size=24):
    return T(text, size, color).move_to([pos[0], pos[1], 0])


def swap(scene, old, new, run=0.4):
    scene.play(FadeOut(old), FadeIn(new, shift=UP * 0.08), run_time=run)
    return new


def panel_box(x, y, w, h, color=GREY):
    return RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_color=color, stroke_width=2.5,
                            fill_color=color, fill_opacity=0.05).move_to([x, y, 0])


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Methods library"
    TITLE = "Remove One Cell, See What Fails"


# ---------------------------------------------------------------------------------------------
class S01Problem(SpokenScene):
    """delete a gene = every cell, from birth; remove chosen cells instead and ask if they are needed."""

    def construct(self):
        cols, rows, dx, dy = 8, 5, 1.15, 1.0
        cx, cy = 0.0, 0.2
        rng = np.random.RandomState(4)
        kinds = ["s", "d", "h"]
        tgt = set()
        while len(tgt) < 13:
            tgt.add((int(rng.randint(cols)), int(rng.randint(rows))))
        cells, tcells, tpos, marks = VGroup(), VGroup(), [], VGroup()
        for i in range(cols):
            for j in range(rows):
                x = cx + (i - (cols - 1) / 2) * dx
                y = cy + ((rows - 1) / 2 - j) * dy
                if (i, j) in tgt:
                    c = cell("c", x, y, 0.42, GREEN, 0.28)
                    tcells.add(c)
                    tpos.append((x, y))
                else:
                    c = cell(kinds[(i + 2 * j) % 3], x, y, 0.4)
                cells.add(c)
                marks.add(minus(x, y, 0.3))
        cap = capline("a gene deleted in every cell", pos=(cx, 3.3))
        self.play(FadeIn(cells), FadeIn(marks), FadeIn(cap, shift=UP * 0.1), run_time=0.7)
        self.at("what a protein does")
        self.play(Indicate(marks, color=RED, scale_factor=1.15), run_time=0.8)
        self.at("not what a cell type does")
        cap2 = capline("one cell type", GREEN, pos=(cx, 3.3))
        self.play(FadeOut(cap), FadeIn(cap2), Indicate(tcells, color=GREEN, scale_factor=1.25), run_time=0.9)

        # timeline
        ty = -2.95
        x0, x1 = cx - 4.2, cx + 4.2
        line = Line([x0, ty, 0], [x1, ty, 0], color=GREY, stroke_width=4)
        b_t = lab("birth", 24, GREY).next_to([x0, ty, 0], DOWN, buff=0.18)
        t_t = lab("test", 24, YELLOW).next_to([x1, ty, 0], DOWN, buff=0.18)
        b_d = Dot([x0, ty, 0], radius=0.1, color=GREY)
        t_d = Dot([x1, ty, 0], radius=0.1, color=YELLOW)
        adj = lab("the animal adjusts", 28, TEAL).move_to([cx, ty + 0.42, 0])
        self.at("developmental experiment")
        cap3 = capline("deleted from birth", pos=(cx, 3.3))
        self.play(FadeOut(cap2), FadeIn(cap3), Create(line), FadeIn(b_d), FadeIn(b_t), FadeIn(t_d), FadeIn(t_t),
                  run_time=0.7)
        self.at("the animal can adjust")
        self.play(FadeIn(adj, shift=UP * 0.1), run_time=0.5)

        # remove chosen cells
        self.at("Remove chosen cells")
        ghosts = VGroup(*[ghost("c", x, y, 0.42) for x, y in tpos])
        cap4 = capline("remove chosen cells instead", GREEN, pos=(cx, 3.3))
        self.play(FadeOut(cap3), FadeIn(cap4), FadeOut(marks), FadeOut(tcells), FadeIn(ghosts),
                  FadeOut(VGroup(line, b_t, t_t, b_d, t_d, adj)), run_time=0.9)
        # test panel; the field makes room
        px = 4.4
        box = panel_box(px, 0.2, 3.6, 5.2, YELLOW)
        hd = lab("TEST THE ANIMAL", 26, YELLOW, weight=BOLD).move_to([px, 2.3, 0])
        q = T("?", 140, YELLOW, weight=BOLD).move_to([px, 0.6, 0])
        field = VGroup(*[c for c in cells if c not in tcells], ghosts)
        self.at("ask whether")
        self.play(field.animate.scale(0.8).move_to([-2.45, 0.2, 0]), cap4.animate.move_to([-2.45, 3.3, 0]),
                  FadeIn(box), FadeIn(hd), FadeIn(q, scale=0.6), run_time=0.9)
        need = lines("are those", "cells needed?", size=30, color=TEXT, buff=0.1, align=ORIGIN).move_to([px, -1.3, 0])
        self.play(FadeIn(need, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Laser(SpokenScene):
    """laser route in a worm larva: identify by position + nucleus, focus, brief pulse, nucleus gone."""

    def construct(self):
        LY = -0.55
        # slide, larva, coverslip, laser
        slide = Rectangle(width=12.8, height=0.42, stroke_color=GREY, stroke_width=2.5, fill_color=GREY,
                          fill_opacity=0.25).move_to([0, -2.5, 0])
        slide_l = lab("slide with agar pad", 22, GREY).move_to([0, -2.5, 0])
        larva = RoundedRectangle(corner_radius=1.5, width=12.4, height=3.1, stroke_color=GREY, stroke_width=3.5,
                                 fill_color=GREY, fill_opacity=0.06).move_to([0, LY, 0])
        cover = Line([-6.3, 1.3, 0], [6.3, 1.3, 0], color=GREY, stroke_width=3)
        cover_l = lab("coverslip", 22, GREY).move_to([5.2, 1.62, 0])
        TX = 2.7
        laser = chip("pulsed laser", BLUE, 26).move_to([TX, 3.15, 0])
        rows_y = [0.5, -0.55, -1.6]
        xs = [-5.1 + 1.13 * k for k in range(10)]
        rng = np.random.RandomState(8)
        kinds = ["s", "d", "h", "c"]
        cells, nuclei, pos = VGroup(), VGroup(), {}
        for j, y in enumerate(rows_y):
            for i, x in enumerate(xs):
                if abs(x - TX) < 0.2 and j == 1:
                    continue
                k = kinds[int(rng.randint(4))]
                cells.add(cell(k, x, y, 0.34))
                nk = i % 3
                if nk == 0:
                    n = Dot([x, y, 0], radius=0.09, color=GREY)
                elif nk == 1:
                    n = Circle(radius=0.15, stroke_color=GREY, stroke_width=2.5).move_to([x, y, 0])
                else:
                    n = Dot([x, y, 0], radius=0.15, color=GREY)
                nuclei.add(n)
        tx_y = rows_y[1]
        target = cell("c", TX, tx_y, 0.38, GREY, 0.14)
        tnuc = Circle(radius=0.18, stroke_color=GREY, stroke_width=3).move_to([TX, tx_y, 0])
        target_g = VGroup(target, tnuc)

        self.at("a laser could kill")
        self.play(FadeIn(slide), FadeIn(slide_l), FadeIn(larva), FadeIn(cells), FadeIn(target), FadeIn(laser),
                  run_time=1.0)
        cap = capline("a laser kills one identified cell", pos=(-3.4, 2.5), size=26)
        cap.align_to([-6.3, 0, 0], LEFT)
        self.play(FadeIn(cap), run_time=0.4)
        self.at("A young larva")
        ll = lab("young larva", 24, TEXT).move_to([-5.0, -3.1, 0])
        self.play(FadeIn(ll), run_time=0.4)
        self.at("held still with azide")
        az = lab("azide holds it still", 24, ORANGE).move_to([-1.5, -3.1, 0])
        self.play(FadeIn(cover), FadeIn(cover_l), FadeIn(az), run_time=0.6)

        self.at("reproducible positions")
        cap2 = capline("reproducible positions", TEAL, pos=(-3.4, 2.5), size=26).align_to([-6.3, 0, 0], LEFT)
        grid = VGroup(*[DashedLine([x, 1.0, 0], [x, -2.05, 0], color=TEAL, stroke_width=1.8, dash_length=0.1)
                        for x in xs])
        self.play(FadeOut(cap), FadeIn(cap2), FadeIn(grid), run_time=0.8)
        self.at("typical nucleus under Nomarski optics")
        cap3 = capline("Nomarski: a typical nucleus per type", TEAL, pos=(-3.4, 2.5), size=26)
        cap3.align_to([-6.3, 0, 0], LEFT)
        self.play(FadeOut(cap2), FadeIn(cap3), FadeOut(grid), FadeIn(nuclei, lag_ratio=0.02), FadeIn(tnuc), run_time=1.2)
        self.at("names the cell")
        ring = Circle(radius=0.62, stroke_color=GREEN, stroke_width=5).move_to([TX, tx_y, 0])
        cap4 = capline("position plus nucleus names the cell", GREEN, pos=(-3.4, 2.5), size=26)
        cap4.align_to([-6.3, 0, 0], LEFT)
        self.play(FadeOut(cap3), FadeIn(cap4), target.animate.set_stroke(GREEN, 4).set_fill(GREEN, 0.3),
                  Create(ring), run_time=0.8)

        # beam
        self.at("focused on a single spot")
        cone = Polygon([TX - 0.75, 2.8, 0], [TX + 0.75, 2.8, 0], [TX + 0.06, tx_y + 0.1, 0], [TX - 0.06, tx_y + 0.1, 0],
                       stroke_width=0, fill_color=YELLOW, fill_opacity=0.45)
        beam = Line([TX, 2.8, 0], [TX, tx_y, 0], color=YELLOW, stroke_width=4)
        spot = Dot([TX, tx_y, 0], radius=0.11, color=YELLOW)
        cap5 = capline("beam aligned with that cell", YELLOW, pos=(-3.4, 2.5), size=26).align_to([-6.3, 0, 0], LEFT)
        self.play(FadeOut(cap4), FadeIn(cap5), FadeIn(cone), Create(beam), FadeIn(spot), FadeOut(ring), run_time=0.8)

        # pulses
        self.at("Pulses are brief")
        px0 = -6.2
        base = Line([px0, 3.1, 0], [px0 + 2.6, 3.1, 0], color=GREY, stroke_width=2)
        spikes = VGroup(*[Line([px0 + 0.45 + 0.8 * k, 3.1, 0], [px0 + 0.45 + 0.8 * k, 3.5, 0], color=YELLOW,
                               stroke_width=6) for k in range(3)])
        # a pulse train sits above the caption line
        self.play(FadeOut(cap5), Create(base), FadeIn(spikes, lag_ratio=0.3), run_time=0.7)
        cap6 = capline("brief pulses", YELLOW, pos=(-3.4, 2.5), size=26).align_to([-6.3, 0, 0], LEFT)
        self.play(FadeIn(cap6), run_time=0.3)
        self.at("heat has little time")
        halo = Circle(radius=0.5, stroke_color=RED, stroke_width=3.5).move_to([TX, tx_y, 0])
        halo_f = Circle(radius=0.5, stroke_width=0, fill_color=RED, fill_opacity=0.25).move_to([TX, tx_y, 0])
        cap7 = capline("heat has little time to spread", RED, pos=(-3.4, 2.5), size=26).align_to([-6.3, 0, 0], LEFT)
        self.play(FadeOut(cap6), FadeIn(cap7), GrowFromCenter(halo_f), Create(halo), run_time=0.7)
        self.at("they lasted three nanoseconds")
        ns = lab("3 ns, one 1995 system", 24, YELLOW).move_to([-3.0, 3.2, 0])
        ns.align_to([-3.4, 0, 0], LEFT)
        self.play(FadeIn(ns, shift=UP * 0.1), run_time=0.5)

        # later
        self.at("An hour to a day later")
        clock = lab("1 hour to 1 day later", 28, GOLD).move_to([-3.4, 2.7, 0]).align_to([-6.3, 0, 0], LEFT)
        gh = ghost("c", TX, tx_y, 0.38)
        self.play(FadeOut(cap7), FadeIn(clock), FadeOut(cone), FadeOut(beam), FadeOut(spot), FadeOut(halo),
                  FadeOut(halo_f), FadeOut(spikes), FadeOut(base), FadeOut(ns), run_time=0.8)
        self.at("the killed nucleus is gone")
        self.play(FadeOut(target), FadeOut(tnuc), FadeIn(gh), run_time=0.8)
        gl = lab("nucleus gone", 26, RED).move_to([TX, -3.1, 0])
        self.play(FadeIn(gl), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Receptor(SpokenScene):
    """laser needs see-through tissue; toxin reaches any receptor cell; human receptor; Cre removes STOP."""

    def construct(self):
        cols, rows, dx, dy = 9, 4, 1.25, 1.0
        cx, cy = 0.0, -0.35
        rng = np.random.RandomState(2)
        kinds = ["s", "d", "h"]
        cells = VGroup()
        grid = {}
        for i in range(cols):
            for j in range(rows):
                x = cx + (i - (cols - 1) / 2) * dx
                y = cy + ((rows - 1) / 2 - j) * dy
                grid[(i, j)] = (x, y)
        # receptor cell, deep, right half
        RC = (7, 3)
        rcx, rcy = grid[RC]
        for (i, j), (x, y) in grid.items():
            if (i, j) == RC:
                continue
            cells.add(cell(kinds[(i + j * 2) % 3], x, y, 0.38))
        rc = cell("c", rcx, rcy, 0.4, GREEN, 0.3)
        rcm = recmark(rcx, rcy, 0.4)
        # extra receptor cells on right half (shows "any cell that carries its receptor")
        extra = [(6, 1), (8, 2), (6, 3)]
        ex_c, ex_m = VGroup(), VGroup()
        for (i, j) in extra:
            x, y = grid[(i, j)]
            ex_c.add(cell("c", x, y, 0.4, GREEN, 0.3))
            ex_m.add(recmark(x, y, 0.4))
        # remove replaced shapes
        remove = [m for m in cells if any(np.hypot(m.get_center()[0] - grid[e][0], m.get_center()[1] - grid[e][1]) < 0.05
                                          for e in extra)]
        for m in remove:
            cells.remove(m)

                # opaque tissue on the left, laser beam blocked
        lx = -3.1
        laser = chip("laser", BLUE, 26).move_to([lx, 3.1, 0])
        top_y = grid[(2, 0)][1]
        beam = Line([lx, 2.75, 0], [lx, 0.55, 0], color=YELLOW, stroke_width=5)
        opaque = Rectangle(width=12.4, height=2.9, stroke_color=GREY, stroke_width=2,
                           fill_color=BG, fill_opacity=0.82).move_to([0.0, -0.9, 0])
        op_l = lab("opaque: cannot see in", 24, GREY).move_to([-3.4, -0.9, 0])
        self.play(FadeIn(cells), FadeIn(laser), Create(beam), run_time=0.8)
        self.play(FadeIn(opaque), FadeIn(op_l), run_time=0.6)
        self.play(FadeIn(rc), FadeIn(ex_c), run_time=0.4)
        # genetic toxin
        tx = 3.1
        vial = chip("toxin", ORANGE, 26).move_to([tx, 3.1, 0])
        self.at("A genetic toxin reaches")
        self.play(FadeIn(vial), run_time=0.4)
        dots = VGroup(*[dot(tx + (k - 1) * 0.35, 2.55 - 0.0, ORANGE) for k in range(3)])
        self.play(FadeIn(dots), run_time=0.3)
        self.at("that carries its receptor")
        self.play(FadeIn(ex_m), FadeIn(rcm), Indicate(ex_m, color=PURPLE, scale_factor=1.6),
                  run_time=0.8)
        self.at("even deep in the brain")
        # dots travel to the deep receptor cell
        path = [Line([tx + (k - 1) * 0.35, 2.55, 0], [rcx + (k - 1) * 0.1, rcy + 0.45, 0]) for k in range(3)]
        anims = [MoveAlongPath(dots[k], path[k]) for k in range(3)]
        self.play(*anims, run_time=1.1)
        gh = ghost("c", rcx, rcy, 0.4)
        deep = lab("deep in the tissue", 24, RED).move_to([rcx + 0.2, rcy - 0.78, 0])
        self.play(FadeOut(rc), FadeOut(rcm), FadeIn(gh), FadeOut(dots), FadeIn(deep), run_time=0.5)

        # clear
        self.at("Mouse cells are poor targets")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.5)
        mx, hx = -3.3, 3.3
        mcell = cell("c", mx, 0.4, 1.35, GREY, 0.12, 4)
        hcell = cell("c", hx, 0.4, 1.35, GREEN, 0.25, 4)
        m_rec = recmark(mx, 0.4, 1.35, 90, 0.45)
        m_rec.set_fill(GREY, 0.55)
        h_rec = recmark(hx, 0.4, 1.35, 90, 0.9)
        h_rec.scale([1, 2.2, 1])
        mt = lab("mouse cell", 30, GREY).move_to([mx, -1.9, 0])
        ht = lab("cell with the human receptor", 30, GREEN).move_to([hx, -1.9, 0])
        mtox = dot(mx - 2.0, 2.3, ORANGE, 0.16)
        htox = dot(hx - 2.0, 2.3, ORANGE, 0.16)
        self.play(FadeIn(mcell), FadeIn(hcell), FadeIn(m_rec), FadeIn(h_rec), FadeIn(mt), FadeIn(ht), run_time=0.7)
        self.play(FadeIn(mtox), FadeIn(htox), run_time=0.3)
        self.play(mtox.animate.move_to([mx + 2.2, 2.9, 0]), htox.animate.move_to([hx, 1.95, 0]), run_time=1.0)
        aff = M("about 100,000x higher affinity", 30, PURPLE).move_to([0, -2.85, 0])
        aff_arr = arr([mx + 0.4, -2.7, 0], [hx - 3.1, -2.7, 0], PURPLE) if False else None
        self.at("times higher affinity")
        self.play(FadeIn(aff, shift=UP * 0.1), run_time=0.6)

        # constructs
        self.at("So the human receptor gene")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.5)
        ctl = chip("a chosen gene's control", BLUE, 36)
        rg = chip("human receptor gene", PURPLE, 36)
        strip1 = VGroup(ctl, rg).arrange(RIGHT, buff=0.0).scale(1.3)
        fit(strip1, max_w=12.4)
        strip1.move_to([0, 2.6, 0])
        self.play(FadeIn(strip1, shift=UP * 0.1), run_time=0.7)
        self.at("or into an allele")
        ctl2 = chip("control", BLUE, 34)
        stop = chip("STOP", RED, 34)
        rg2 = chip("human receptor gene", PURPLE, 34)
        strip2 = VGroup(ctl2, stop, rg2).arrange(RIGHT, buff=0.0).scale(1.3)
        fit(strip2, max_w=12.4)
        strip2.move_to([0, 0.85, 0])
        al = lab("allele", 26, GREY).next_to(strip2, UP, buff=0.12).align_to(strip2, LEFT)
        self.play(FadeIn(strip2, shift=UP * 0.1), FadeIn(al), run_time=0.7)
        cre = chip("Cre", BLUE, 40).move_to([stop.get_center()[0], -0.5, 0])
        self.at("removes a stop cassette")
        self.play(FadeIn(cre, shift=UP * 0.2), run_time=0.5)
        self.play(stop.animate.shift(UP * 0.0).set_opacity(0.0), cre.animate.shift(UP * 0.0), run_time=0.7)
        ok = Arrow([rg2.get_center()[0], 0.35, 0], [rg2.get_center()[0], 0.35, 0], buff=0) if False else None
        self.at("line chooses the cells")
        row_y = -2.05
        xs = [-5.6 + 1.6 * k for k in range(8)]
        cre_set = {1, 2, 5}
        row, extra_m = VGroup(), VGroup()
        lbl_g = VGroup()
        for k, x in enumerate(xs):
            if k in cre_set:
                row.add(cell("c", x, row_y, 0.5, GREEN, 0.28, 3))
                row.add(Dot([x, row_y, 0], radius=0.14, color=BLUE))
                extra_m.add(recmark(x, row_y, 0.5, 90, 0.34))
            else:
                row.add(cell(["s", "d", "h"][k % 3], x, row_y, 0.5, GREY, 0.12, 3))
        l1 = lab("cells with Cre", 26, BLUE).move_to([(xs[1] + xs[2]) / 2, row_y - 0.9, 0])
        l2 = lab("carry the receptor", 26, PURPLE).move_to([(xs[1] + xs[2]) / 2, row_y - 1.3, 0])
        self.play(FadeOut(cre), FadeIn(row), run_time=0.7)
        self.play(FadeIn(extra_m), FadeIn(l1), FadeIn(l2), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Inject(SpokenScene):
    """inject toxin when you choose; dose and timing; protein synthesis stops; newborn or adult."""

    def construct(self):
        # animal block
        ax, ay, aw, ah = -1.2, 0.25, 6.4, 4.0
        animal = RoundedRectangle(corner_radius=0.7, width=aw, height=ah, stroke_color=GREY, stroke_width=3.5,
                                  fill_color=GREY, fill_opacity=0.06).move_to([ax, ay, 0])
        al = lab("mouse", 24, GREY).move_to([ax + 1.8, ay + ah / 2 + 0.3, 0])
        cols, rows, dx, dy = 6, 4, 1.0, 0.92
        cells, tc, tm, tpos = VGroup(), VGroup(), VGroup(), []
        tset = {(1, 1), (2, 2), (4, 1), (3, 0), (4, 3), (1, 3)}
        kinds = ["s", "d", "h"]
        for i in range(cols):
            for j in range(rows):
                x = ax + (i - (cols - 1) / 2) * dx
                y = ay - 0.05 + ((rows - 1) / 2 - j) * dy
                if (i, j) in tset:
                    tc.add(cell("c", x, y, 0.34, GREEN, 0.3))
                    tm.add(recmark(x, y, 0.34))
                    tpos.append((x, y))
                else:
                    cells.add(cell(kinds[(i + j) % 3], x, y, 0.32))
        # syringe
        sx = -5.0
        barrel = Rectangle(width=2.0, height=0.7, stroke_color=BLUE, stroke_width=4, fill_color=ORANGE,
                           fill_opacity=0.55).move_to([sx + 0.1, 2.75, 0])
        plunger = Rectangle(width=0.2, height=1.0, stroke_color=BLUE, stroke_width=4, fill_color=BLUE,
                            fill_opacity=0.8).move_to([sx - 1.05, 2.75, 0])
        rod = Line([sx - 1.15, 2.75, 0], [sx - 0.9, 2.75, 0], color=BLUE, stroke_width=6)
        needle = Line([sx + 1.1, 2.9, 0], [ax - 3.4 + 1.5 + 0.0, 2.9 - 0.9, 0], color=BLUE, stroke_width=5)
        needle_end = np.array([ax - 1.7, 2.0, 0])
        needle = Line([sx + 1.1, 2.75, 0], needle_end, color=BLUE, stroke_width=5)
        syr = VGroup(barrel, plunger, needle)
        syr_l = lab("toxin", 26, ORANGE).move_to([sx + 0.1, 3.3, 0])
        self.at("The toxin is injected")
        self.play(FadeIn(animal), FadeIn(al), FadeIn(cells), FadeIn(tc), FadeIn(tm), FadeIn(syr), FadeIn(syr_l),
                  run_time=0.6)
        drops = VGroup(*[dot(needle_end[0] + 0.25 * k, needle_end[1] - 0.2 * k, ORANGE, 0.1) for k in range(3)])
        self.play(plunger.animate.shift(RIGHT * 0.5), FadeIn(drops, lag_ratio=0.3), run_time=0.6)
        tl_y = -3.0
        x0, x1 = -6.2, 4.4
        # timeline for the dose
        self.at("For example")
        dose = M("100 micrograms per kg", 28, ORANGE).move_to([ax - 0.0, -2.5, 0])
        dose2 = lab("for example", 22, GREY).next_to(dose, UP, buff=0.12)
        self.play(FadeIn(dose), FadeIn(dose2), run_time=0.5)
        self.at("on two days")
        d1 = Dot([-4.2, tl_y, 0], radius=0.12, color=ORANGE)
        d2 = Dot([1.0, tl_y, 0], radius=0.12, color=ORANGE)
        tline = Line([-5.4, tl_y, 0], [2.2, tl_y, 0], color=GREY, stroke_width=4)
        l1 = lab("day 1", 24, ORANGE).next_to(d1, DOWN, buff=0.15)
        l2 = lab("day 2", 24, ORANGE).next_to(d2, DOWN, buff=0.15)
        self.play(Create(tline), FadeIn(d1), FadeIn(l1), FadeIn(d2), FadeIn(l2), run_time=0.7)
        self.at("hours apart")
        brace = lab("72 hours", 24, YELLOW).move_to([-1.6, tl_y - 0.45, 0])
        self.play(FadeIn(brace), run_time=0.4)

        # inside a cell
        self.at("Inside a sensitive cell")
        zx = 4.4
        zbox = panel_box(zx, 0.75, 3.7, 4.6, GREEN)
        zc = cell("c", zx, 1.85, 1.0, GREEN, 0.28, 4)
        zr = recmark(zx, 1.85, 1.0, 90, 0.5)
        zt = dot(zx - 0.0, 3.25, ORANGE, 0.13)
        self.play(FadeIn(zbox), FadeIn(zc), FadeIn(zr), FadeIn(zt), run_time=0.7)
        self.play(zt.animate.move_to([zx, 1.85, 0]), run_time=0.6)
        bar_bg = Rectangle(width=2.6, height=0.4, stroke_color=GREY, stroke_width=2.5).move_to([zx, -0.45, 0])
        bar = Rectangle(width=2.6, height=0.4, stroke_width=0, fill_color=YELLOW, fill_opacity=0.9)
        bar.move_to(bar_bg.get_center())
        bl = lab("protein synthesis", 26, YELLOW).move_to([zx, 0.2, 0])
        self.at("it inhibits protein synthesis")
        self.play(FadeIn(bar_bg), FadeIn(bar), FadeIn(bl), run_time=0.5)
        self.play(bar.animate.stretch_to_fit_width(0.05, about_edge=LEFT), run_time=1.0)
        dead = ghost("c", zx, 1.85, 1.0, 4, 20)
        self.play(FadeOut(zc), FadeOut(zr), FadeOut(zt), FadeIn(dead),
                  *[FadeOut(c) for c in tc], *[FadeOut(m) for m in tm],
                  *[FadeIn(ghost("c", x, y, 0.34)) for x, y in tpos], run_time=0.8)

        # timing
        self.at("Because the timing is yours")
        self.play(FadeOut(VGroup(tline, d1, d2, l1, l2, brace, dose, dose2)), run_time=0.4)
        nl, adl = -5.2, 1.4
        tline2 = Line([-5.6, tl_y, 0], [2.8, tl_y, 0], color=GREY, stroke_width=4)
        n_d = Dot([-4.6, tl_y, 0], radius=0.14, color=ORANGE)
        a_d = Dot([1.6, tl_y, 0], radius=0.14, color=ORANGE)
        n_l = lab("newborn", 28, TEXT).next_to(n_d, DOWN, buff=0.15)
        a_l = lab("adult", 28, TEXT).next_to(a_d, DOWN, buff=0.15)
        self.play(Create(tline2), FadeIn(n_d), FadeIn(n_l), FadeIn(a_d), FadeIn(a_l), run_time=0.7)
        self.at("the same cells can be removed")
        same = lab("the same cells, removed at either age", 28, GREEN).move_to([-1.0, -2.45, 0])
        self.play(FadeIn(same, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Reading(SpokenScene):
    """a real result (Cavanaugh 2009): count of cells left; threshold with controls."""

    def construct(self):
        # three panels, full height
        P1x, P2x, P3x = -4.4, -0.1, 4.4
        W1, W2, W3 = 3.8, 4.8, 3.8
        H, CY = 6.4, -0.1
        real = lab("REAL RESULT", 22, GOLD, weight=BOLD).move_to([4.9, 3.45, 0])
        # panel 1: count
        b1 = panel_box(P1x, CY, W1, H, GREEN)
        h1 = lines("1  count the", "target cells left", size=26, color=GREEN, buff=0.05, align=ORIGIN).move_to([P1x, 2.65, 0])
        dots = VGroup()
        kept = None
        for i in range(10):
            for j in range(10):
                d = Dot([P1x - 1.5 + i * 0.333, 1.65 - j * 0.34, 0], radius=0.125, color=GREEN)
                if (i, j) == (5, 5):
                    kept = d
                dots.add(d)
        # panel 2
        b2 = panel_box(P2x, CY, W2, H, YELLOW)
        h2 = lines("2  the behaviour", "against controls", size=26, color=YELLOW, buff=0.05, align=ORIGIN).move_to([P2x, 2.65, 0])
        # panel 3
        b3 = panel_box(P3x, CY, W3, H, GREY)
        h3 = lines("controls and", "other tests", size=26, color=GREY, buff=0.05, align=ORIGIN).move_to([P3x, 2.65, 0])

        self.at("Results have")
        self.play(FadeIn(b1), FadeIn(h1), FadeIn(dots), FadeIn(real), run_time=0.8)
        self.at("compared with controls")
        self.play(FadeIn(b2), FadeIn(h2), FadeIn(b3), FadeIn(h3), run_time=0.8)
        self.at("In one study")
        self.wait(0.1)
        gone = VGroup(*[d for d in dots if d is not kept])
        gl = lines("Mrgprd neurons:", "over 98% gone", size=30, color=TEXT, buff=0.06, align=ORIGIN).move_to([P1x, -2.15, 0])
        gl2 = lab("(schematic)", 22, GREY).move_to([P1x, -2.95, 0])
        self.at("were gone")
        self.play(*[d.animate.set_opacity(0.0) for d in gone], FadeIn(gl), FadeIn(gl2), run_time=1.3)
        # axes
        ox, oy = P2x - 1.5, -2.0
        axh = 3.0
        yax = Line([ox, oy, 0], [ox, oy + 1.1 * axh, 0], color=GREY, stroke_width=3)
        xax = Line([ox, oy, 0], [ox + 3.4, oy, 0], color=GREY, stroke_width=3)
        ticks = VGroup(*[VGroup(Line([ox - 0.1, oy + v * axh, 0], [ox, oy + v * axh, 0], color=GREY, stroke_width=3),
                                M(f"{v:.1f}", 22, GREY).move_to([ox - 0.5, oy + v * axh, 0])) for v in (0.0, 0.5, 1.0)])
        yl = lines("mechanical withdrawal", "threshold (g)", size=24, color=YELLOW, buff=0.04, align=ORIGIN).move_to([P2x + 0.0, 1.8, 0])
        self.at("The mechanical withdrawal threshold")
        self.play(FadeIn(yax), FadeIn(xax), FadeIn(ticks), FadeIn(yl), run_time=0.7)
        bw = 0.95
        bx1, bx2 = ox + 1.0, ox + 2.5
        bar1 = Rectangle(width=bw, height=0.41 * axh, stroke_width=0, fill_color=YELLOW, fill_opacity=0.55)
        bar1.move_to([bx1, oy + 0.41 * axh / 2, 0])
        bar2 = Rectangle(width=bw, height=0.99 * axh, stroke_width=0, fill_color=YELLOW, fill_opacity=0.9)
        bar2.move_to([bx2, oy + 0.99 * axh / 2, 0])
        v1 = M("0.41", 26, BG, weight=BOLD).move_to([bx1, oy + 0.41 * axh * 0.5, 0])
        v2 = M("0.99", 26, BG, weight=BOLD).move_to([bx2, oy + 0.99 * axh * 0.5, 0])
        e1 = VGroup(Line([bx1, oy + 0.37 * axh, 0], [bx1, oy + 0.45 * axh, 0], color=TEXT, stroke_width=3))
        e2 = VGroup(Line([bx2, oy + 0.84 * axh, 0], [bx2, oy + 1.14 * axh, 0], color=TEXT, stroke_width=3))
        c1 = lab("before", 24, TEXT).move_to([bx1, oy - 0.3, 0])
        c2 = lab("after toxin", 24, TEXT).move_to([bx2, oy - 0.3, 0])
        cd = lab("receptor mice", 26, PURPLE).move_to([P2x + 0.2, oy - 0.68, 0])
        eb = lab("mean ± error, as reported", 20, GREY).move_to([P2x + 0.1, oy - 1.0, 0])
        self.at("rose from")
        self.play(GrowFromEdge(bar1, DOWN), FadeIn(c1), FadeIn(cd), run_time=0.6)
        self.play(FadeIn(v1), FadeIn(e1), FadeIn(eb), run_time=0.3)
        self.at("grams to")
        self.play(GrowFromEdge(bar2, DOWN), FadeIn(c2), run_time=0.8)
        self.play(FadeIn(v2), FadeIn(e2), run_time=0.3)
        # controls
        wt = VGroup(chip("wild-type littermates", GREY, 26), chip("given the toxin", ORANGE, 26)).arrange(DOWN, buff=0.16)
        wt.move_to([P3x, 0.95, 0])
        wt_r = lines("no significant", "change", size=28, color=GREEN, buff=0.05, align=ORIGIN).move_to([P3x, -0.6, 0])
        self.at("no significant change")
        self.play(FadeIn(wt, shift=UP * 0.1), run_time=0.5)
        self.play(FadeIn(wt_r), run_time=0.4)
        heat = chip("heat", RED, 30)
        cold = chip("cold", BLUE, 30)
        hc = VGroup(heat, cold).arrange(RIGHT, buff=0.3).move_to([P3x, -1.6, 0])
        hcr = lines("sensitivity", "not reduced", size=28, color=GREEN, buff=0.05, align=ORIGIN).move_to([P3x, -2.6, 0])
        self.at("Heat and cold")
        self.play(FadeIn(hc, shift=UP * 0.1), run_time=0.5)
        self.play(FadeIn(hcr), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Pitfalls(SpokenScene):
    """three controls: toxin without receptor; count what died; neighbours."""

    def construct(self):
        CX = [-4.4, 0.0, 4.4]
        W, H, CY = 3.9, 6.4, -0.1
        boxes = [panel_box(x, CY, W, H, c) for x, c in zip(CX, (ORANGE, GREEN, RED))]
        heads = [
            lines("toxin, no receptor?", size=26, color=ORANGE, align=ORIGIN).move_to([CX[0], 2.7, 0]),
            lines("too few cells die?", size=26, color=GREEN, align=ORIGIN).move_to([CX[1], 2.7, 0]),
            lines("other cells die too?", size=26, color=RED, align=ORIGIN).move_to([CX[2], 2.7, 0]),
        ]
        kinds = ["s", "d", "h"]

        def cluster(cx, cy, cols, rows, dx, dy, tmask, r=0.3):
            """returns (all cells group, list of (x,y,is_target))"""
            g, info = VGroup(), []
            for i in range(cols):
                for j in range(rows):
                    x = cx + (i - (cols - 1) / 2) * dx
                    y = cy + ((rows - 1) / 2 - j) * dy
                    t = (i, j) in tmask
                    info.append((x, y, t, (i + j) % 3))
            return info

        # ---- column 1: receptor mice vs wild-type
        info_r = cluster(CX[0], 1.0, 3, 2, 0.95, 0.9, {(0, 0), (1, 1), (2, 0)})
        info_w = cluster(CX[0], -1.55, 3, 2, 0.95, 0.9, set())
        r_cells, w_cells = VGroup(), VGroup()
        r_t, r_m, r_pos = VGroup(), VGroup(), []
        for x, y, t, k in info_r:
            if t:
                r_t.add(cell("c", x, y, 0.33, GREEN, 0.3))
                r_m.add(recmark(x, y, 0.33))
                r_pos.append((x, y))
            else:
                r_cells.add(cell(kinds[k], x, y, 0.3))
        for x, y, t, k in info_w:
            w_cells.add(cell(kinds[k], x, y, 0.3))
        rl = lab("receptor mice", 24, PURPLE).move_to([CX[0], 2.05, 0])
        wl = lab("wild-type littermates", 24, GREY).move_to([CX[0], -0.15, 0])
        wl2 = lab("given the toxin", 24, ORANGE).move_to([CX[0], -0.5, 0])
        w_note = lab("compare the two", 26, GREEN).move_to([CX[0], -3.05, 0])

        self.at("The toxin might act")
        self.play(*[FadeIn(b) for b in boxes], *[FadeIn(h) for h in heads], run_time=0.7)
        self.play(FadeIn(r_cells), FadeIn(r_t), FadeIn(r_m), FadeIn(rl), run_time=0.6)
        ghs = VGroup(*[ghost("c", x, y, 0.33) for x, y in r_pos])
        self.play(FadeOut(r_t), FadeOut(r_m), FadeIn(ghs), run_time=0.6)
        self.at("type littermates")
        self.play(FadeIn(w_cells), FadeIn(wl), FadeIn(wl2), run_time=0.6)
        tox = VGroup(*[dot(CX[0] - 1.65 + 0.55 * k, -2.65, ORANGE, 0.1) for k in range(7)])
        self.play(FadeIn(tox, lag_ratio=0.1), run_time=0.6)
        self.play(FadeIn(w_note), run_time=0.4)

        # ---- column 2: count
        # Cre-driven: 4 of 12 survive (incomplete); knock-in: 1 of 12 survives
        def block(cx, cy, survive, label, lc, tag):
            tgs, gs, pos = VGroup(), VGroup(), []
            for i in range(4):
                for j in range(3):
                    x = cx + (i - 1.5) * 0.78
                    y = cy + (1 - j) * 0.7
                    pos.append((x, y, (i, j) in survive))
            for x, y, s in pos:
                tgs.add(cell("c", x, y, 0.27, GREEN, 0.3, 2.6))
            lb = lab(label, 24, lc).move_to([cx, cy + 1.2, 0])
            return tgs, pos, lb

        b_a, p_a, l_a = block(CX[1], 0.9, {(0, 0), (2, 1), (3, 2), (1, 2)}, "Cre-driven toxin", BLUE, 0)
        b_b, p_b, l_b = block(CX[1], -1.7, {(3, 0)}, "receptor knock-in", PURPLE, 0)
        cnt = lab("count the target cells", 26, GREEN).move_to([CX[1], -3.0, 0])
        self.at("Too few")
        self.play(FadeIn(b_a), FadeIn(l_a), FadeIn(b_b), FadeIn(l_b), run_time=0.7)
        self.at("count them")
        self.play(FadeIn(cnt), run_time=0.4)
        self.at("incompletely")
        gh_a = VGroup(*[ghost("c", x, y, 0.27, 2.6, 10) for x, y, s in p_a if not s])
        self.play(*[FadeOut(b_a[i]) for i, (x, y, s) in enumerate(p_a) if not s], FadeIn(gh_a), run_time=0.8)
        l_a2 = lab("Cre-driven: incomplete", 24, BLUE).move_to(l_a.get_center())
        self.play(FadeOut(l_a), FadeIn(l_a2), run_time=0.3)
        self.at("removed virtually all")
        gh_b = VGroup(*[ghost("c", x, y, 0.27, 2.6, 10) for x, y, s in p_b if not s])
        self.play(*[FadeOut(b_b[i]) for i, (x, y, s) in enumerate(p_b) if not s], FadeIn(gh_b), run_time=0.8)
        l_b2 = lab("knock-in: virtually all", 24, PURPLE).move_to(l_b.get_center())
        self.play(FadeOut(l_b), FadeIn(l_b2), run_time=0.3)

        # ---- column 3: bystanders
        cx3 = CX[2]
        info3 = cluster(cx3, 0.7, 3, 3, 0.95, 0.95, {(1, 1)})
        c3_cells, c3_pos = VGroup(), []
        by_idx = {(0, 1), (2, 1)}
        by_gh = []
        tgt3 = None
        pos3 = {}
        for n, (x, y, t, k) in enumerate(info3):
            i, j = n // 3, n % 3
            pos3[(i, j)] = (x, y, k)
            if t:
                tgt3 = cell("c", x, y, 0.34, GREEN, 0.3)
            else:
                c3_cells.add(cell(kinds[k], x, y, 0.32))
        self.at("toxin depleted")
        self.play(FadeIn(c3_cells), FadeIn(tgt3), run_time=0.6)
        x, y, k = pos3[(1, 1)]
        gh3 = ghost("c", x, y, 0.34)
        self.play(FadeOut(tgt3), FadeIn(gh3), run_time=0.5)
        by_l = lab("neighbours, too", 24, RED).move_to([cx3, -1.15, 0])
        outs, ghs3 = [], []
        for (i, j) in [(0, 1), (2, 1)]:
            x, y, k = pos3[(i, j)]
            ghs3.append(ghost(kinds[k], x, y, 0.32))
        # fade the two neighbour cells
        victims = []
        for m in c3_cells:
            for (i, j) in [(0, 1), (2, 1)]:
                x, y, k = pos3[(i, j)]
                if np.hypot(m.get_center()[0] - x, m.get_center()[1] - y) < 0.05:
                    victims.append(m)
        self.play(*[FadeOut(v) for v in victims], *[FadeIn(g) for g in ghs3], FadeIn(by_l), run_time=0.7)
        self.at("Check other cells")
        sc = lab("check other cells", 26, GREEN).move_to([cx3, -1.9, 0])
        sm = lab("use a second method", 26, BLUE).move_to([cx3, -2.5, 0])
        self.play(FadeIn(sc, shift=UP * 0.1), run_time=0.5)
        self.at("use a second method")
        self.play(FadeIn(sm, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07Kimble(SpokenScene):
    """Kimble and White 1981: laser kills the distal tip cell; Austin and Kimble 1987: glp-1 mimics it; Notch-like."""

    def construct(self):
        TY1, TY2 = 0.2, -1.35          # row one starts centred, then slides up to 1.9
        GX0, GX1 = -6.1, 6.1
        TH = 1.9
        tube1 = RoundedRectangle(corner_radius=0.95, width=GX1 - GX0, height=TH, stroke_color=GREY, stroke_width=3.5,
                                 fill_color=GREY, fill_opacity=0.06).move_to([0, TY1, 0])
        tube2 = tube1.copy().move_to([0, TY2, 0])
        xs = [-4.3 + 0.97 * k for k in range(10)]
        TIPX = -5.35

        def germ(x, y, meiosis):
            if meiosis:
                return cell("d", x, y, 0.4, TEAL, 0.3, 3)
            return cell("c", x, y, 0.36, TEAL, 0.3, 3)

        tip1 = cell("c", TIPX, TY1, 0.58, GREEN, 0.35, 4)
        tip1_l = lab("distal tip cell", 24, GREEN).move_to([-4.0, TY1 - 1.3, 0])
        g1 = VGroup(*[germ(x, TY1, False) for x in xs])
        t1 = lab("Kimble and White, 1981", 24, GOLD).move_to([4.2, TY1 + 1.35, 0])
        mit = lab("germ cells divide", 24, TEAL).move_to([0.8, TY1 - 1.3, 0])
        lbl_g = lab("worm gonad", 24, GREY).move_to([-1.6, TY1 + 1.35, 0])

        self.at("In 1981")
        self.play(FadeIn(tube1), FadeIn(tip1), FadeIn(g1), FadeIn(t1), FadeIn(lbl_g), run_time=0.9)
        self.play(FadeIn(tip1_l), FadeIn(mit), run_time=0.5)
        self.at("used a laser to kill")
        beam = Line([TIPX, 3.5, 0], [TIPX, TY1 + 0.55, 0], color=YELLOW, stroke_width=5)
        spot = Dot([TIPX, TY1, 0], radius=0.13, color=YELLOW)
        self.play(Create(beam), FadeIn(spot), run_time=0.6)
        gh = ghost("c", TIPX, TY1, 0.58, 4, 16)
        self.play(FadeOut(tip1), FadeIn(gh), FadeOut(beam), FadeOut(spot), run_time=0.6)
        self.at("entered meiosis instead")
        new = VGroup(*[germ(x, TY1, True) for x in xs])
        self.play(*[Transform(g1[k], new[k]) for k in range(10)], FadeOut(mit), run_time=1.0)
        mei2 = lab("germ cells enter meiosis", 24, TEAL).move_to([0.8, TY1 - 1.3, 0])
        self.play(FadeIn(mei2), run_time=0.3)

        tip2 = cell("c", TIPX, TY2, 0.58, GREEN, 0.35, 4)
        g2 = VGroup(*[germ(x, TY2, True) for x in xs])
        t2 = lab("Austin & Kimble, 1987", 24, GOLD).move_to([4.2, TY2 + 1.35, 0])
        gl = lab("glp-1 mutant", 24, TEXT).move_to([-4.4, TY2 + 1.35, 0])
        r1 = VGroup(tube1, gh, g1, tip1_l, t1, lbl_g, mei2)
        self.at("In 1987")
        self.play(r1.animate.shift(UP * 1.85), FadeIn(tube2), FadeIn(tip2), FadeIn(g2), FadeIn(t2), FadeIn(gl),
                  run_time=1.0)
        mm = lab("germ cells enter meiosis", 24, TEAL).move_to([0.8, TY2 - 1.25, 0])
        self.at("which led to")
        self.play(FadeIn(mm), run_time=0.4)
        nt = chip("Notch-like receptor", PURPLE, 30).move_to([4.0, -3.25, 0])
        ar = arr([0.2, -3.25, 0], [nt.get_left()[0] - 0.1, -3.2, 0], PURPLE, 5)
        self.at("like receptor")
        self.play(GrowArrow(ar), FadeIn(nt), run_time=0.7)
        self.at("no gene was yet known")
        nk = lab("laser first: no gene yet known", 26, YELLOW).move_to([-3.4, -3.3, 0])
        self.play(FadeIn(nk, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S08Timing(SpokenScene):
    """Luquet 2005 adult vs newborn; van Es 2019 Paneth cells; the rule."""

    def construct(self):
        cy, ch = 0.5, 5.6
        RX = 3.35

        def mk(cx, w):
            """The Luquet card in its final state, centred on cx and w wide."""
            k = w / 6.1
            d = {}
            d["b"] = panel_box(cx, cy, w, ch, GREEN)
            d["yr"] = T("2005", 40, GOLD, font=TITLE_FONT).move_to([cx - w / 2 + 1.35, cy + 2.35, 0])
            d["t"] = lab("Luquet et al., 2005", 22, GOLD).move_to([cx + w / 2 - 1.9, cy + 2.4, 0])
            ax, nx = cx - 0.25 * w, cx + 0.25 * w
            d["adl"] = lab("adult", 28, TEXT).move_to([ax, cy + 1.45, 0])
            d["nbl"] = lab("newborn", 28, TEXT).move_to([nx, cy + 1.45, 0])
            d["ag"] = lab("AgRP neurons", 24, GREEN).move_to([cx, cy - 0.3, 0])
            d["gad"] = VGroup(*[ghost("c", ax - 0.8 * k + 0.8 * k * i, cy + 0.6, 0.3, 2.8, 10) for i in range(3)])
            d["gnb"] = VGroup(*[ghost("c", nx - 0.8 * k + 0.8 * k * i, cy + 0.6, 0.3, 2.8, 10) for i in range(3)])
            d["adr"] = chip("rapid starvation", RED, 24).move_to([ax, cy - 1.15, 0])
            d["nbr"] = chip("minimal effect", GREEN, 24).move_to([nx, cy - 1.15, 0])
            d["cmp"] = lab("timing exposed compensation", 26, YELLOW).move_to([cx, cy - 2.0, 0])
            d["ad"] = VGroup(*[cell("c", ax - 0.8 * k + 0.8 * k * i, cy + 0.6, 0.3, GREEN, 0.3, 2.8) for i in range(3)])
            d["nb"] = VGroup(*[cell("c", nx - 0.8 * k + 0.8 * k * i, cy + 0.6, 0.3, GREEN, 0.3, 2.8) for i in range(3)])
            return d

        big = mk(0.0, 8.6)
        small = mk(-3.35, 6.1)
        b2 = panel_box(RX, cy, 6.1, ch, TEAL)
        yr2 = T("2019", 40, GOLD, font=TITLE_FONT).move_to([RX - 1.75, cy + 2.35, 0])
        t2 = lab("van Es et al., 2019", 22, GOLD).move_to([RX + 1.25, cy + 2.4, 0])
        pc = VGroup(*[cell("c", RX - 2.0 + 0.8 * i, cy + 0.6, 0.3, GREEN, 0.3, 2.8) for i in range(3)])
        lg = VGroup(*[cell("d", RX + 0.7 + 0.8 * i, cy + 0.6, 0.32, TEAL, 0.3, 2.8) for i in range(3)])
        pcl = lab("Paneth cells", 26, GREEN).move_to([RX - 1.2, cy + 1.45, 0])
        lgl = lab("Lgr5 stem cells", 26, TEAL).move_to([RX + 1.5, cy + 1.45, 0])
        pcr = lab("removed", 26, RED).move_to([RX - 1.2, cy - 0.5, 0])
        lgr = lab("persisted", 26, TEAL).move_to([RX + 1.5, cy - 0.5, 0])

        self.play(FadeIn(big["b"]), FadeIn(big["yr"]), FadeIn(big["t"]), FadeIn(big["ad"]), FadeIn(big["nb"]),
                  FadeIn(big["adl"]), FadeIn(big["nbl"]), FadeIn(big["ag"]), run_time=0.7)
        self.at("killed")
        self.play(FadeOut(big["ad"]), FadeIn(big["gad"]), run_time=0.5)
        self.at("rapid starvation")
        self.play(FadeIn(big["adr"]), run_time=0.4)
        self.at("Killed in newborns")
        self.play(FadeOut(big["nb"]), FadeIn(big["gnb"]), run_time=0.6)
        self.at("minimal effect")
        self.play(FadeIn(big["nbr"]), run_time=0.5)
        self.at("exposed compensation")
        self.play(FadeIn(big["cmp"], shift=UP * 0.1), run_time=0.5)

        self.at("and colleagues removed")
        keys = ["b", "yr", "t", "adl", "nbl", "ag", "gad", "gnb", "adr", "nbr", "cmp"]
        self.play(Transform(VGroup(*[big[k] for k in keys]), VGroup(*[small[k] for k in keys])), run_time=0.7)
        self.play(FadeIn(b2), FadeIn(yr2), FadeIn(t2), FadeIn(pc), FadeIn(lg), FadeIn(pcl), FadeIn(lgl), run_time=0.4)
        gpc = VGroup(*[ghost("c", c.get_center()[0], c.get_center()[1], 0.3, 2.8, 10) for c in pc])
        self.at("removed Paneth cells")
        self.play(FadeOut(pc), FadeIn(gpc), FadeIn(pcr), run_time=0.7)
        self.at("stem cells persisted")
        self.play(FadeIn(lgr), Indicate(lg, color=TEAL, scale_factor=1.15), run_time=0.7)

        self.at("Keep this rule")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.6)
        rule = lines("Removal shows whether cells are needed,", "for that assay, age and targeting tool,",
                     "not what they can do alone.", size=42, color=TEXT, buff=0.22, align=ORIGIN)
        rbox = SurroundingRectangle(rule, color=GOLD, stroke_width=3, buff=0.5, corner_radius=0.2)
        head = lab("KEEP THIS RULE", 28, GOLD, weight=BOLD).next_to(rbox, UP, buff=0.3)
        self.play(FadeIn(head), Create(rbox), run_time=0.5)
        self.at("removal shows whether")
        self.play(FadeIn(rule, shift=UP * 0.15), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S09End(EndCard):
    LINE = "Removal shows whether cells are needed, not what they can do alone."
