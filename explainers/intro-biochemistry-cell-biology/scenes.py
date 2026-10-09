"""Compartments Create Control: Intro to biochemistry & cell biology.

COLOR MAP (kept for the whole video)
  BLUE   = membranes and compartments (cell walls, rooms, bilayer, vesicles, lysosome)
  GREEN  = working protein machinery (channels, receptors, enzymes)
  YELLOW = cargo that moves (molecules, LDL, signals, labeled protein)
  RED    = failure / what piles up (broken receptor, GM2, stored lipid, harm)
  GREY   = labels, unlabeled things, de-emphasized
  GOLD   = the one highlight (banner, title rule)
No molecular structures are drawn: cells, rooms, vesicles, receptors and enzymes are schematic shapes.
"""
import random

from bp_style import *  # noqa: F401,F403

DARK_GREEN = "#24402f"


class Scn(NarratedScene):
    def at(self, f):
        """Wait until fraction f of the narration has played (absolute time, not a duration)."""
        r = f * self.narration_s - self.elapsed()
        if r > 0.02:
            self.wait(r)


def drift(dots, cx, cy, hw, hh, speed=0.55, seed=3):
    """Make dots wander inside a box and bounce off its walls (the 'one open room')."""
    rng = random.Random(seed)
    for d in dots:
        a = rng.uniform(0, TAU)
        d.vel = np.array([np.cos(a), np.sin(a), 0.0]) * speed * rng.uniform(0.6, 1.4)

        def upd(m, dt):
            m.shift(m.vel * dt)
            p = m.get_center()
            if abs(p[0] - cx) > hw:
                m.vel[0] *= -1
                m.shift(RIGHT * (np.sign(cx - p[0]) * (abs(p[0] - cx) - hw)))
            if abs(p[1] - cy) > hh:
                m.vel[1] *= -1
                m.shift(UP * (np.sign(cy - p[1]) * (abs(p[1] - cy) - hh)))

        d.add_updater(upd)


def cup(center, color=GREEN, r=0.32, w=7):
    """Schematic receptor binding cup (a U-shaped arc)."""
    return Arc(radius=r, start_angle=PI, angle=PI, color=color, stroke_width=w).move_to(center)


# --------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Intro to biochemistry & cell biology"
    TITLE = "Compartments Create Control"


# --------------------------------------------------------------------------------------------
class S01Floorplans(Scn):
    def construct(self):
        cxL, cxR, cy = -3.4, 3.4, 0.8
        cellL = RoundedRectangle(corner_radius=0.7, width=6.0, height=3.9, stroke_color=BLUE, stroke_width=5,
                                 fill_color=BLUE, fill_opacity=0.05).move_to([cxL, cy, 0])
        cellR = RoundedRectangle(corner_radius=0.7, width=6.0, height=3.9, stroke_color=BLUE, stroke_width=5,
                                 fill_color=BLUE, fill_opacity=0.05).move_to([cxR, cy, 0])
        tL = T("PROKARYOTE", 32, weight=BOLD).move_to([cxL, 3.2, 0])
        tR = T("EUKARYOTE", 32, weight=BOLD).move_to([cxR, 3.2, 0])
        div = DashedLine([0, -1.6, 0], [0, 3.5, 0], color=GREY, stroke_width=2, dash_length=0.15).set_opacity(0.5)

        # 0.00  "Two cellular floor plans."
        self.play(Create(cellL), Create(cellR), FadeIn(tL), FadeIn(tR), FadeIn(div), run_time=self.beat(0.05))

        # 0.06  prokaryote: an open plan, one room, everything mixed together
        rng = random.Random(7)
        dots = VGroup(*[Dot(radius=0.09, color=GREY).move_to(
            [cxL + rng.uniform(-2.6, 2.6), cy + rng.uniform(-1.6, 1.6), 0]) for _ in range(18)])
        big = VGroup(*[Dot(radius=0.16, color=YELLOW).move_to(
            [cxL + rng.uniform(-2.2, 2.2), cy + rng.uniform(-1.3, 1.3), 0]) for _ in range(4)])
        drift(list(dots) + list(big), cxL, cy, 2.55, 1.6, speed=0.6)
        l1 = T("a bacterium: an open plan", 28).move_to([cxL, -1.55, 0])
        self.at(0.06)
        self.play(FadeIn(dots), FadeIn(big), FadeIn(l1, shift=UP * 0.1), run_time=self.beat(0.05))

        # 0.17  no internal membranes, no true nucleus
        self.at(0.17)
        l2 = T("no internal membranes, no true nucleus", 24, color=GREY).move_to([cxL, -2.1, 0])
        self.play(FadeIn(l2), run_time=self.beat(0.05))

        # 0.33  eukaryote: a building of walled offices
        self.at(0.33)
        r1 = T("your cells: walled offices", 28).move_to([cxR, -1.55, 0])
        self.play(Indicate(cellR, color=BLUE, scale_factor=1.02), FadeIn(r1, shift=UP * 0.1), run_time=self.beat(0.07))

        # 0.47  the rooms appear one by one, as they are named
        self.at(0.47)
        specs = [("Nucleus", cxR - 1.35, cy + 1.05), ("ER", cxR + 1.35, cy + 1.05),
                 ("Golgi", cxR - 1.35, cy), ("Mitochondrion", cxR + 1.35, cy), ("Lysosome", cxR, cy - 1.05)]
        rooms = []
        for name, x, y in specs:
            box = RoundedRectangle(corner_radius=0.12, width=2.5, height=0.78, stroke_color=BLUE, stroke_width=3,
                                   fill_color=BLUE, fill_opacity=0.18)
            lab = T(name, 24).move_to(box)
            rooms.append(VGroup(box, lab).move_to([x, y, 0]))
        order = [0, 3, 1, 2, 4]  # spoken order: nucleus, mitochondria, ER, Golgi, lysosomes
        self.play(LaggedStart(*[GrowFromCenter(rooms[i]) for i in order], lag_ratio=0.7), run_time=self.beat(0.13))
        r2 = T("each room has its own membrane", 24, color=GREY).move_to([cxR, -2.1, 0])
        self.play(FadeIn(r2), run_time=self.beat(0.03))

        # 0.66  the banner
        self.at(0.66)
        banner = chip("Compartments enable specialization", GOLD, size=32, pad=0.25, fill_opacity=0.12).move_to([0, -3.05, 0])
        self.play(Write(banner[1]), Create(banner[0]), run_time=self.beat(0.1))

        # 0.79  specialization: names become jobs
        self.at(0.79)
        jobs = {"Nucleus": "genome", "ER": "proteins", "Golgi": "sorting", "Mitochondrion": "energy", "Lysosome": "recycling"}
        swaps = []
        for (name, _, _), room in zip(specs, rooms):
            new = T(jobs[name], 26, color=GREEN).move_to(room[0])
            swaps.append(AnimationGroup(FadeOut(room[1], scale=0.9), FadeIn(new, scale=1.1)))
            room[1] = new
        self.play(LaggedStart(*swaps, lag_ratio=0.25), run_time=self.beat(0.12))
        self.finish()


# --------------------------------------------------------------------------------------------
class S02Membrane(Scn):
    def construct(self):
        xs = [-4.2 + 0.6 * k for k in range(15)]
        title = T("Plasma membrane: a phospholipid bilayer", 34).move_to([0, 3.25, 0])
        water_t = Rectangle(width=12.4, height=1.5, stroke_width=0, fill_color=BLUE, fill_opacity=0.07).move_to([0, 2.05, 0])
        water_b = water_t.copy().move_to([0, -2.05, 0])
        core = Rectangle(width=9.0, height=1.2, stroke_width=0, fill_color=BLUE, fill_opacity=0.14).move_to(ORIGIN)
        heads_t = VGroup(*[Circle(radius=0.21, stroke_width=0, fill_color=BLUE, fill_opacity=1).move_to([x, 0.85, 0]) for x in xs])
        heads_b = VGroup(*[Circle(radius=0.21, stroke_width=0, fill_color=BLUE, fill_opacity=1).move_to([x, -0.85, 0]) for x in xs])

        # 0.00  the bilayer is built
        self.play(FadeIn(title), FadeIn(water_t), FadeIn(water_b), run_time=self.beat(0.04))
        self.play(FadeIn(core), LaggedStart(*[GrowFromCenter(h) for h in heads_t], lag_ratio=0.06),
                  LaggedStart(*[GrowFromCenter(h) for h in heads_b], lag_ratio=0.06), run_time=self.beat(0.12))

        # 0.17  hydrophilic heads face the water on both sides
        self.at(0.17)
        wl_t = T("water (outside)", 26, color=GREY).move_to([4.6, 2.5, 0])
        wl_b = T("water (inside)", 26, color=GREY).move_to([4.6, -2.5, 0])
        cl_t = T("hydrophilic heads", 26, color=BLUE).move_to([-3.3, 2.05, 0])
        cl_b = T("hydrophilic heads", 26, color=BLUE).move_to([-3.3, -2.05, 0])
        ar_t = Arrow([-3.3, 1.7, 0], [-3.3, 1.12, 0], buff=0, color=BLUE, stroke_width=4, max_tip_length_to_length_ratio=0.4)
        ar_b = Arrow([-3.3, -1.7, 0], [-3.3, -1.12, 0], buff=0, color=BLUE, stroke_width=4, max_tip_length_to_length_ratio=0.4)
        self.play(FadeIn(wl_t), FadeIn(wl_b), FadeIn(cl_t), FadeIn(cl_b), GrowArrow(ar_t), GrowArrow(ar_b), run_time=self.beat(0.06))

        # 0.27  the hydrophobic core blocks most molecules
        self.at(0.27)
        self.play(FadeOut(VGroup(cl_t, cl_b, ar_t, ar_b)), run_time=self.beat(0.02))
        core_lab = T("hydrophobic core", 26, color=BLUE).move_to([0.5, 0, 0])
        self.play(FadeIn(core_lab), run_time=self.beat(0.02))
        mols = VGroup(*[Dot(radius=0.14, color=YELLOW).move_to([x, 2.35, 0]) for x in (-3.3, -0.4, 0.9, 4.2)])
        self.play(FadeIn(mols), run_time=self.beat(0.015))
        self.play(LaggedStart(*[m.animate(rate_func=there_and_back_with_pause).shift(DOWN * 0.92) for m in mols],
                              lag_ratio=0.25), run_time=self.beat(0.07))
        self.play(FadeOut(mols), run_time=self.beat(0.015))

        # 0.42  studded with proteins
        self.at(0.42)
        gap = 0.04
        ch_l = RoundedRectangle(corner_radius=0.12, width=0.55, height=2.4, stroke_color=GREEN, stroke_width=4,
                                fill_color=DARK_GREEN, fill_opacity=1).move_to([-1.8 - 0.275 - gap / 2, 0, 0])
        ch_r = ch_l.copy().move_to([-1.8 + 0.275 + gap / 2, 0, 0])
        rc_body = RoundedRectangle(corner_radius=0.12, width=0.9, height=2.3, stroke_color=GREEN, stroke_width=4,
                                   fill_color=DARK_GREEN, fill_opacity=1).move_to([2.8, 0, 0])
        rc_cup = cup([2.8, 1.38, 0], r=0.45)  # sits on the receptor body
        gone = VGroup(*[h for h in heads_t if abs(h.get_x() + 1.8) < 0.7 or abs(h.get_x() - 2.8) < 0.65],
                      *[h for h in heads_b if abs(h.get_x() + 1.8) < 0.7 or abs(h.get_x() - 2.8) < 0.65])
        new_title = T("A selective barrier", 34).move_to(title)
        self.play(FadeOut(core_lab), ReplacementTransform(title, new_title), run_time=self.beat(0.05))
        self.at(0.57)
        self.play(FadeOut(gone), FadeIn(ch_l), FadeIn(ch_r), FadeIn(rc_body), Create(rc_cup), run_time=self.beat(0.06))
        title = new_title

        # 0.68  channel proteins open passages for specific ions
        self.at(0.68)
        lab_ch = T("channel", 26, color=GREEN).move_to([-3.2, -1.65, 0])
        ion = VGroup(Circle(radius=0.31, stroke_width=0, fill_color=YELLOW, fill_opacity=1),
                     T("Na⁺", 24, color=BG, weight=BOLD)).move_to([-1.8, 2.15, 0])
        self.play(FadeIn(lab_ch), FadeIn(ion), ch_l.animate.shift(LEFT * 0.4), ch_r.animate.shift(RIGHT * 0.4), run_time=self.beat(0.03))
        self.play(ion.animate.move_to([-1.8, -2.15, 0]), run_time=self.beat(0.065), rate_func=smooth)

        # 0.79  receptor proteins receive signals from outside
        self.at(0.78)
        lab_rc = T("receptor", 26, color=GREEN).move_to([4.5, 1.75, 0])
        sig = Dot(radius=0.2, color=YELLOW).move_to([2.8, 2.55, 0])
        sig_lab = T("signal", 26, color=YELLOW).next_to(sig, LEFT, buff=0.25)
        self.play(FadeIn(lab_rc), FadeIn(sig), FadeIn(sig_lab), FadeOut(ion), run_time=self.beat(0.02))
        self.play(sig.animate.move_to([2.8, 1.52, 0]), sig_lab.animate.set_opacity(0), run_time=self.beat(0.035))
        self.play(rc_cup.animate.set_color(YELLOW), Flash(sig, color=YELLOW, flash_radius=0.5), run_time=self.beat(0.025))

        # 0.89  the membrane decides what gets in and what stays out
        self.at(0.865)
        new_title2 = T("It decides what passes", 34).move_to(title)
        pass_ion = VGroup(Circle(radius=0.31, stroke_width=0, fill_color=YELLOW, fill_opacity=1),
                          T("Na⁺", 24, color=BG, weight=BOLD)).move_to([-1.8, 2.15, 0])
        blocked = Dot(radius=0.14, color=YELLOW).move_to([-0.2, 2.35, 0])
        self.play(ReplacementTransform(title, new_title2), FadeIn(pass_ion), FadeIn(blocked), run_time=self.beat(0.025))
        self.play(pass_ion.animate.move_to([-1.8, -2.15, 0]),
                  blocked.animate(rate_func=there_and_back_with_pause).shift(DOWN * 0.95), run_time=self.beat(0.07))
        self.finish()


# --------------------------------------------------------------------------------------------
class S03Traffic(Scn):
    def construct(self):
        div = DashedLine([0, -3.2, 0], [0, 3.5, 0], color=GREY, stroke_width=2, dash_length=0.15).set_opacity(0.5)
        hL = T("Into the cell", 32, color=TEXT).move_to([-3.3, 3.1, 0])
        hR = T("Out of the cell", 32, color=TEXT).move_to([3.4, 3.1, 0])
        mem_y = -0.3
        memL = Line([-6.2, mem_y, 0], [-0.5, mem_y, 0], color=BLUE, stroke_width=7)
        memR = Line([4.85, -0.7, 0], [4.85, 1.5, 0], color=BLUE, stroke_width=7)

        # 0.00  two ways across the barrier
        self.play(FadeIn(div), FadeIn(hL), FadeIn(hR), Create(memL), Create(memR), run_time=self.beat(0.03))
        in_ar = Arrow([-3.3, 1.2, 0], [-3.3, -1.3, 0], buff=0, color=YELLOW, stroke_width=6)
        out_ar = Arrow([3.9, 0.4, 0], [5.9, 0.4, 0], buff=0, color=YELLOW, stroke_width=6)
        self.play(GrowArrow(in_ar), GrowArrow(out_ar), run_time=self.beat(0.03))

        # 0.14  left: LDL receptors working (endocytosis)
        self.at(0.14)
        hL2 = T("Familial hypercholesterolemia", 28).move_to(hL)
        self.play(FadeOut(in_ar), FadeOut(out_ar), ReplacementTransform(hL, hL2), run_time=self.beat(0.02))
        rx = [-5.2, -3.9, -2.6, -1.3]
        recs = VGroup(*[VGroup(RoundedRectangle(corner_radius=0.05, width=0.2, height=0.4, stroke_width=0, fill_color=GREEN,
                                                fill_opacity=1).move_to([x, mem_y + 0.1, 0]),
                               cup([x, mem_y + 0.4, 0], r=0.17, w=5)) for x in rx])
        rec_lab = T("LDL receptor", 24, color=GREEN).move_to([-1.9, 0.75, 0])
        self.play(FadeIn(recs), FadeIn(rec_lab), run_time=self.beat(0.02))
        ldl = VGroup(Dot(radius=0.21, color=YELLOW))
        ldl.move_to([-3.9, 1.9, 0])
        ldl_lab = T("LDL", 24, color=YELLOW).next_to(ldl, RIGHT, buff=0.2)
        self.play(FadeIn(ldl), FadeIn(ldl_lab), run_time=self.beat(0.015))
        self.at(0.18)
        self.play(ldl.animate.move_to([-3.9, mem_y + 0.62, 0]), ldl_lab.animate.set_opacity(0), FadeOut(rec_lab), run_time=self.beat(0.025))
        ves = Circle(radius=0.4, stroke_color=BLUE, stroke_width=5, fill_color=BLUE, fill_opacity=0.15).move_to([-3.9, mem_y - 0.1, 0])
        self.play(FadeIn(ves, scale=0.5), ldl.animate.move_to([-3.9, mem_y - 0.1, 0]), run_time=self.beat(0.02))
        endo = T("endocytosis", 26, color=BLUE).move_to([-2.2, -1.9, 0])
        self.play(VGroup(ves, ldl).animate.shift(DOWN * 1.45), FadeIn(endo), run_time=self.beat(0.03))

        # 0.20  the receptors are broken: LDL cannot get in and piles up
        self.at(0.27)
        broken = T("broken receptors", 24, color=RED).move_to([-5.0, 0.75, 0])
        endo_n = T("normal uptake", 24, color=GREY).move_to(endo)
        self.play(*[recs[i][0].animate.set_color(RED) for i in range(4)],
                  *[recs[i][1].animate.set_color(RED) for i in range(4)], FadeIn(broken),
                  VGroup(ves, ldl).animate.set_opacity(0.3), ReplacementTransform(endo, endo_n), run_time=self.beat(0.03))
        endo = endo_n
        rows = [(0.62, 11), (1.0, 9), (1.38, 7), (1.76, 5)]
        heap = VGroup()
        for y, n in rows:
            for k in range(n):
                heap.add(Dot(radius=0.17, color=YELLOW).move_to([-3.3 + (k - (n - 1) / 2) * 0.46, y + 0.0, 0]))
        heap_lab = T("LDL cholesterol piles up", 26, color=YELLOW).move_to([-3.3, 2.55, 0])
        self.at(0.32)
        self.play(FadeOut(broken), LaggedStart(*[FadeIn(d, shift=DOWN * 0.8) for d in heap], lag_ratio=0.05), run_time=self.beat(0.08))
        for i, d in enumerate(heap):
            d.ph = i * 0.7
            d.add_updater(lambda m, dt: m.shift(UP * 0.0025 * np.sin(self.renderer.time * 3 + m.ph)))
        self.play(FadeIn(heap_lab), run_time=self.beat(0.02))

        # 0.42  endocytosis brings material in
        self.at(0.42)
        endo2 = T("endocytosis brings LDL in", 26, color=BLUE).move_to([-3.3, -2.75, 0])
        self.play(ves.animate.set_stroke(opacity=1).set_fill(opacity=0.15), ldl.animate.set_opacity(1),
                  ReplacementTransform(endo, endo2), run_time=self.beat(0.025))
        endo = endo2
        self.play(Indicate(VGroup(ves, ldl), color=BLUE, scale_factor=1.15), run_time=self.beat(0.03))

        # 0.47  right: the experiment that mapped the path out
        self.at(0.47)
        hR2 = T("Palade: pulse-chase", 30).move_to(hR)
        er = RoundedRectangle(corner_radius=0.14, width=1.6, height=1.6, stroke_color=BLUE, stroke_width=3,
                              fill_color=BLUE, fill_opacity=0.14).move_to([1.25, 0.4, 0])
        golgi = er.copy().move_to([3.25, 0.4, 0])
        er_lab = T("rough ER", 24).move_to([1.25, 0.95, 0])
        go_lab = T("Golgi", 24).move_to([3.25, 0.95, 0])
        arr1 = Arrow([2.27, 0.35, 0], [2.38, 0.35, 0], buff=0, color=GREY, stroke_width=3, max_tip_length_to_length_ratio=1)
        self.play(ReplacementTransform(hR, hR2), FadeIn(er), FadeIn(golgi), FadeIn(er_lab), FadeIn(go_lab), run_time=self.beat(0.05))
        time_ar = Arrow([0.8, -2.15, 0], [6.0, -2.15, 0], buff=0, color=GREY, stroke_width=3)
        time_lab = T("time", 24, color=GREY).move_to([5.6, -2.55, 0])
        marker = Dot(radius=0.12, color=YELLOW).move_to([0.8, -2.15, 0])
        self.play(Create(time_ar), FadeIn(time_lab), FadeIn(marker), run_time=self.beat(0.03))

        # 0.62  tag fresh protein with a brief radioactive pulse
        self.at(0.62)
        pulse = chip("radioactive pulse", YELLOW, size=24, pad=0.16).move_to([2.35, 2.1, 0])
        stage = T("pulse: new protein is labeled", 26, color=YELLOW).move_to([3.4, -1.2, 0])
        lab_dots = VGroup(*[Dot(radius=0.1, color=YELLOW).move_to([1.25 + dx, 0.3 + dy, 0]) for dx, dy in
                            [(-0.35, 0.2), (0.0, 0.3), (0.35, 0.2), (-0.2, -0.15), (0.2, -0.15)]])
        self.play(FadeIn(pulse, shift=DOWN * 0.2), FadeIn(stage), run_time=self.beat(0.03))
        self.play(LaggedStart(*[FadeIn(d, scale=0.2) for d in lab_dots], lag_ratio=0.2), run_time=self.beat(0.04))

        # 0.70  chase with unlabeled
        self.at(0.70)
        chase = chip("unlabeled chase", GREY, size=24, pad=0.16).move_to(pulse)
        stage2 = T("chase: unlabeled follows", 26, color=GREY).move_to(stage)
        grey_dots = VGroup(*[Dot(radius=0.1, color=GREY).move_to([1.25 + dx, -0.05 + dy, 0]) for dx, dy in
                             [(-0.4, -0.1), (0.0, -0.2), (0.4, -0.1), (0.15, -0.35), (-0.2, -0.35)]])
        self.play(ReplacementTransform(pulse, chase), ReplacementTransform(stage, stage2),
                  FadeIn(grey_dots, scale=0.2), marker.animate.move_to([2.2, -2.15, 0]), run_time=self.beat(0.04))

        # 0.74  the labeled cohort moves: ER -> Golgi -> vesicle -> out
        self.at(0.76)
        stage3 = T("the labeled cohort travels", 26, color=YELLOW).move_to(stage2)
        self.play(ReplacementTransform(stage2, stage3), FadeOut(chase), run_time=self.beat(0.015))
        self.at(0.79)
        self.play(lab_dots.animate.shift(RIGHT * 2.0), marker.animate.move_to([3.3, -2.15, 0]), run_time=self.beat(0.04))
        # secretory vesicle pinches off carrying the labeled protein
        ves2 = Circle(radius=0.3, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.18).move_to([4.5, 0.4, 0])
        self.play(FadeIn(ves2, scale=0.4), lab_dots.animate.move_to([4.5, 0.4, 0]).scale(0.6), marker.animate.move_to([4.2, -2.15, 0]),
                  run_time=self.beat(0.03))
        stage4 = T("secretion: labeled protein out", 26, color=YELLOW).move_to(stage3)
        outs = VGroup(*[Dot(radius=0.1, color=YELLOW).move_to([4.5, 0.4, 0]) for _ in range(5)])
        targets = [[5.5, 1.1], [5.9, 0.7], [5.6, 0.2], [5.95, -0.2], [5.45, -0.35]]
        self.play(ReplacementTransform(stage3, stage4), FadeOut(ves2), FadeOut(lab_dots), FadeIn(outs),
                  marker.animate.move_to([5.6, -2.15, 0]), run_time=self.beat(0.015))
        self.play(*[o.animate.move_to([tx, ty, 0]) for o, (tx, ty) in zip(outs, targets)], run_time=self.beat(0.035))

        # 0.91  that is how we know the secretory pathway is real
        self.at(0.91)
        self.play(FadeOut(stage4), run_time=self.beat(0.015))
        path = Arrow([0.5, -0.8, 0], [5.9, -0.8, 0], buff=0, color=YELLOW, stroke_width=6)
        final = T("ER → Golgi → secretion", 28, color=YELLOW).move_to([3.4, -1.3, 0])
        self.play(GrowArrow(path), FadeIn(final), run_time=self.beat(0.04))
        self.finish()


# --------------------------------------------------------------------------------------------
class S04Taysachs(Scn):
    def construct(self):
        C = np.array([-2.4, -0.1, 0.0])
        title = T("Tay-Sachs disease", 38, font=TITLE_FONT).move_to([0, 3.2, 0])

        # lysosome: membrane, enzymes
        rng = random.Random(11)
        lys = Circle(radius=1.6, stroke_color=BLUE, stroke_width=7, fill_color=BLUE, fill_opacity=0.1).move_to(C)
        enz = VGroup()
        for k in range(8):
            a = TAU * k / 8 + 0.3
            enz.add(Dot(radius=0.14, color=GREEN).move_to(C + 1.2 * np.array([np.cos(a), np.sin(a), 0])))
        hexa = enz[2]  # the one that goes missing
        lys_lab = T("lysosome: the recycling center", 28).move_to([C[0], 2.3, 0])

        # 0.00  the whole argument in one disease
        self.play(FadeIn(title), run_time=self.beat(0.05))

        # 0.09  the lysosome and its enzymes, sealed behind a membrane
        self.at(0.09)
        self.play(Create(lys), FadeIn(lys_lab, shift=UP * 0.1), run_time=self.beat(0.06))
        enz_lab = T("digestive enzymes", 26, color=GREEN).move_to([C[0], -2.4, 0])
        self.play(LaggedStart(*[GrowFromCenter(e) for e in enz], lag_ratio=0.15), FadeIn(enz_lab), run_time=self.beat(0.07))
        self.play(Indicate(lys, color=BLUE, scale_factor=1.04), run_time=self.beat(0.04))

        # 0.27  one enzyme, hexosaminidase A, is missing
        self.at(0.30)
        new_lab = T("hexosaminidase A", 26, color=GREEN).move_to(enz_lab)
        self.play(ReplacementTransform(enz_lab, new_lab), Indicate(hexa, color=GREEN, scale_factor=2.2), run_time=self.beat(0.05))
        cross = VGroup(Line(UR, DL), Line(UL, DR)).scale(0.25).set_color(RED).set_stroke(width=7).move_to(hexa)
        miss = T("missing", 26, color=RED).next_to(new_lab, RIGHT, buff=0.3)
        self.play(FadeOut(hexa), Create(cross), FadeIn(miss), run_time=self.beat(0.05))

        # 0.39  GM2 cannot be broken down: it accumulates, the lysosome swells
        self.at(0.40)
        self.play(FadeOut(lys_lab), FadeOut(new_lab), FadeOut(miss), FadeOut(cross), run_time=self.beat(0.02))
        gm2_lab = T("GM2 ganglioside", 26, color=RED).move_to([C[0], 2.7, 0])
        pos = [C]
        for r, n in ((0.42, 6), (0.8, 9)):
            for k in range(n):
                a = TAU * k / n + (0.2 if r > 0.5 else 0)
                pos.append(C + r * np.array([np.cos(a), np.sin(a), 0]))
        gm2 = VGroup(*[Square(side_length=0.26, stroke_width=0, fill_color=RED, fill_opacity=1).move_to([-6.2, p[1] + rng.uniform(-0.5, 0.5), 0])
                       for p in pos])
        # the bar of stored GM2, on the right
        bx, by0, bh = 2.8, -1.9, 3.6
        v = ValueTracker(0.0)
        base = Line([bx - 0.9, by0, 0], [bx + 0.9, by0, 0], color=GREY, stroke_width=3)
        bar = always_redraw(lambda: Rectangle(width=1.0, height=max(0.001, bh * v.get_value()), stroke_width=0,
                                              fill_color=RED, fill_opacity=0.9).move_to([bx, by0 + max(0.001, bh * v.get_value()) / 2, 0]))
        bar_lab = T("stored GM2", 26, color=RED).move_to([bx, by0 - 0.45, 0])
        self.at(0.45)
        self.play(FadeIn(gm2_lab), FadeIn(base), FadeIn(bar_lab), run_time=self.beat(0.03))
        self.add(bar)
        self.play(LaggedStart(*[g.animate.move_to(p) for g, p in zip(gm2, pos)], lag_ratio=0.12),
                  v.animate.set_value(0.5), run_time=self.beat(0.1))
        group = VGroup(lys, enz, gm2)
        self.at(0.57)
        self.play(group.animate.scale(1.4, about_point=C), v.animate.set_value(1.0), run_time=self.beat(0.1))
        self.play(lys.animate.set_color(RED), run_time=self.beat(0.03))

        # 0.67  the cell chokes: symptoms
        self.at(0.67)
        self.play(FadeOut(VGroup(bar, base, bar_lab, gm2_lab)), run_time=self.beat(0.02))
        lines = ["muscle weakness", "neurological decline", "early childhood death"]
        rows = VGroup(*[VGroup(Dot(radius=0.1, color=RED), T(s, 28)).arrange(RIGHT, buff=0.25) for s in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        rows.move_to([3.3, 0.0, 0])
        fit(rows, max_w=5.6)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.3) for r in rows], lag_ratio=0.9), run_time=self.beat(0.12))

        # 0.80  one enzyme, one compartment, one child's life
        self.at(0.80)
        self.play(FadeOut(VGroup(group, rows, title)), run_time=self.beat(0.02))
        c1 = chip("one enzyme", GREEN, size=30, pad=0.25)
        c2 = chip("one compartment", BLUE, size=30, pad=0.25)
        c3 = chip("one child's life", TEXT, size=30, pad=0.25)
        chips = VGroup(c1, c2, c3).arrange(RIGHT, buff=0.5).move_to([0, 0.4, 0])
        self.play(FadeIn(c1, shift=UP * 0.2), run_time=self.beat(0.015))
        self.wait(self.beat(0.01))
        self.play(FadeIn(c2, shift=UP * 0.2), run_time=self.beat(0.015))
        self.wait(self.beat(0.01))
        self.play(FadeIn(c3, shift=UP * 0.2), run_time=self.beat(0.015))

        # 0.88  when a compartment fails, everything it held back comes apart
        self.at(0.88)
        cb = c2[0]
        ctr = c2.get_center()
        pieces = VGroup()
        for k in range(10):
            a = TAU * k / 10
            pc = RoundedRectangle(corner_radius=0.05, width=0.55, height=0.3, stroke_color=BLUE, stroke_width=3,
                                  fill_color=BLUE, fill_opacity=0.25)
            pc.move_to(ctr + np.array([np.cos(a) * c2.width / 2.6, np.sin(a) * c2.height / 2.2, 0])).rotate(a)
            pieces.add(pc)
        spill = VGroup(*[Dot(radius=0.09, color=RED).move_to(ctr + [rng.uniform(-0.8, 0.8), rng.uniform(-0.2, 0.2), 0]) for _ in range(22)])
        self.play(FadeOut(c2), FadeIn(pieces), FadeIn(spill), run_time=self.beat(0.015))
        self.play(*[p.animate.shift(np.array([np.cos(i * TAU / 10), np.sin(i * TAU / 10), 0]) * 0.9).rotate(0.6)
                    for i, p in enumerate(pieces)],
                  *[d.animate.shift(np.array([rng.uniform(-3.2, 3.2), rng.uniform(-2.2, 2.2), 0])) for d in spill],
                  c1.animate.set_opacity(0.4), c3.animate.set_opacity(0.4), run_time=self.beat(0.09))
        self.finish()


class S05End(EndCard):
    LINE = "Compartments create control. Explore the cell in the lesson."
