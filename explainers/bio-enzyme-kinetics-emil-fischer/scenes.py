"""Emil Fischer: scientist profile video (Biochemistrypedia, enzyme-kinetics lesson)

The portrait (public/scientists/emil-fischer.png, an AI-generated engraving-style illustration from
The Molecule Hunters) is the anchor: the title scene pushes in on it, then it stays as a framed inset on
the left while the right side animates the story's beats as the narrator reaches them.
Every cue is a self.at("spoken words") lookup in audio/words.json (word timestamps of the real audio).
Nothing on screen adds a fact that is not in the lesson entry (name, dates, contribution, story, quotes).
No molecule is drawn: the lock-and-key picture is a schematic cup (the "lock") and a block (the "key").

COLOR MAP (one color per concept, whole video)
  GOLD   = Emil Fischer, the portrait frame, his rigid "lock and key" picture, the fit
  YELLOW = years / dates, "most of a century"
  TEAL   = places (Berlin)
  BLUE   = enzymes (the cup), pure enzyme
  GREEN  = substrate, glucose, sugars, what the enzyme binds
  AMBER  = behavior: the measurements (melting points, degradation products)
  PURPLE = glycerol
  PINK   = the crystallographers
  RED    = distrust, the ignored near-twin's X, the phenylhydrazine that poisoned him
  GREY   = structure, frames, labels
"""
import os
from pathlib import Path

import numpy as np
from bp_style import *  # noqa: F401,F403

config.disable_caching = True

AMBER = "#E0A458"
PURPLE = "#B58CD9"
PINK = "#E88AB0"

CX = 2.0            # centre of the content area to the right of the portrait column
PORT_X = -4.65      # portrait column centre
PORT_H = 3.3
PORT_Y = 1.35
AR = 460 / 430.0    # fischer_crop.png (the figure cropped from public/scientists/emil-fischer.png)
IMG = Path(os.environ.get("KX_SCRIPT", __file__)).resolve().parent / "fischer_crop.png"
NAME = "Emil Fischer"
DATES = "1852–1919"
CAPTION = "illustration · AI-generated"
CAV = 2.0           # cavity width of the schematic enzyme "lock"
SUB_W = 1.9
SUB_H = 0.9
JAW_H = 1.3
JT = 0.7
BT = 0.55


def portrait(height=PORT_H, center=(PORT_X, PORT_Y)):
    img = ImageMobject(str(IMG))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["cubic"])
    img.set_height(height)
    img.move_to([center[0], center[1], 0])
    img.set_z_index(0)
    border = Rectangle(width=img.width, height=img.height, stroke_color=GOLD, stroke_width=3, fill_opacity=0)
    border.move_to(img).set_z_index(3)
    return img, border


def block(w, h, color, op=1.0):
    return Rectangle(width=w, height=h, stroke_width=0, fill_color=color, fill_opacity=op)


def cup(color, cav=CAV, x=0.0, base_y=0.0, jaw_h=JAW_H, jt=JT, bt=BT):
    """The schematic enzyme: a base with two jaws (a plain cup, not a molecule). Its BASE is centred at (x, base_y)."""
    total = cav + 2 * jt
    base = block(total, bt, color)
    jl = block(jt, jaw_h, color).move_to([-(cav / 2 + jt / 2), bt / 2 + jaw_h / 2, 0])
    jr = block(jt, jaw_h, color).move_to([(cav / 2 + jt / 2), bt / 2 + jaw_h / 2, 0])
    return VGroup(base, jl, jr).shift([x, base_y, 0])


def pivots(g, cav):
    c = g[0].get_center()
    top = g[0].get_top()[1]
    return np.array([c[0] - cav / 2 - JT, top, 0.0]), np.array([c[0] + cav / 2 + JT, top, 0.0])


def jaws(g, cav, theta):
    """Animations that swing both jaws inward by theta radians (negative = outward), hinged at their outer base corners."""
    pl, pr = pivots(g, cav)
    return [Rotate(g[1], -theta, about_point=pl), Rotate(g[2], theta, about_point=pr)]


def substrate(w=SUB_W, h=SUB_H, color=GREEN):
    """The 'key': two halves of one block (so it can be torn apart)."""
    a = block(w / 2, h, color).move_to([-w / 4, 0, 0])
    b = block(w / 2, h, color).move_to([w / 4, 0, 0])
    return VGroup(a, b)


def cavity_slot(g, h=SUB_H, cav=CAV):
    """Centre of a substrate sitting in the cup's cavity."""
    c = g[0].get_center()
    return np.array([c[0], g[0].get_top()[1] + h / 2, 0.0])


class BioScene(SpokenScene):
    def add_column(self):
        img, border = portrait()
        w = img.width
        y = PORT_Y - PORT_H / 2
        self.cap = T(CAPTION, 22, GREY).move_to([PORT_X, y - 0.32, 0])
        self.nm = T(NAME, 28, TEXT, font=TITLE_FONT).move_to([PORT_X, y - 0.95, 0])
        self.dt = T(DATES, 24, GOLD).move_to([PORT_X, y - 1.4, 0])
        self.dim = Rectangle(width=w, height=img.height, stroke_width=0, fill_color=BG,
                             fill_opacity=0).move_to(img).set_z_index(2)
        self.img, self.border = img, border
        self.add(img, border, self.dim, self.cap, self.nm, self.dt)

    def chip_at(self, text, color, x, y, size=28, **kw):
        c = chip(text, color, size, **kw)
        c.move_to([x, y, 0])
        return c

    def dashed_chip(self, text, color, x, y, size=28):
        c = chip(text, color, size).move_to([x, y, 0])
        return VGroup(DashedVMobject(c[0], num_dashes=44, dashed_ratio=0.55).set_color(color), c[1])


class S00Title(BioScene):
    def construct(self):
        brand = T("BIOCHEMISTRYPEDIA  ·  SCIENTIST PROFILE", 22, TEAL, weight=BOLD).move_to([0, 3.4, 0])
        img, border = portrait()
        big_h = 4.0
        k = big_h / PORT_H
        big_c = np.array([0.0, 0.8, 0.0])
        for m in (img, border):
            m.scale(k, about_point=ORIGIN).move_to(big_c)
        cap = T(CAPTION, 22, GREY).move_to([0, 0.8 - big_h / 2 - 0.3, 0])
        name = T(NAME, 52, font=TITLE_FONT)
        name.move_to([0, -2.5, 0])
        dates = T(DATES, 28, GOLD).move_to([0, -3.2, 0])
        rule = Line(LEFT * 1.0, RIGHT * 1.0, color=GOLD, stroke_width=4).move_to([0, -2.9, 0])

        self.play(FadeIn(img), FadeIn(border), FadeIn(brand), FadeIn(cap), run_time=0.4)
        # slow push-in while the name and dates arrive
        self.play(img.animate.scale(1.05), border.animate.scale(1.05),
                  Write(name, run_time=1.0), run_time=1.5, rate_func=linear)
        self.play(GrowFromCenter(rule), FadeIn(dates), run_time=0.35)
        # hand over to the inset layout used by every later scene
        y = PORT_Y - PORT_H / 2
        cap2 = T(CAPTION, 22, GREY).move_to([PORT_X, y - 0.32, 0])
        nm = T(NAME, 28, TEXT, font=TITLE_FONT).move_to([PORT_X, y - 0.95, 0])
        dt = T(DATES, 24, GOLD).move_to([PORT_X, y - 1.4, 0])
        self.play(AnimationGroup(
            img.animate.scale(1 / (k * 1.05)).move_to([PORT_X, PORT_Y, 0]),
            border.animate.scale(1 / (k * 1.05)).move_to([PORT_X, PORT_Y, 0]),
            cap.animate.move_to(cap2),
            Succession(AnimationGroup(FadeOut(name), FadeOut(dates), FadeOut(rule), FadeOut(brand)),
                       AnimationGroup(FadeIn(nm), FadeIn(dt))),
            run_time=0.8))
        self.finish()


class S01Lecture(BioScene):
    def construct(self):
        self.add_column()
        fx = CX
        frame = RoundedRectangle(corner_radius=0.2, width=7.6, height=3.0, stroke_color=GREY, stroke_width=3,
                                 fill_opacity=0).move_to([fx, 1.55, 0])
        yr = M("1894", 36, YELLOW).move_to([fx - 2.7, 2.6, 0])
        berlin = self.chip_at("Berlin", TEAL, fx, 2.6, 26)
        lect = T("lecture", 28, GREY).move_to([fx + 2.5, 2.6, 0])

        self.at("1894")
        self.play(Create(frame), Write(yr), run_time=0.6)
        self.at("Berlin")
        self.play(FadeIn(berlin, shift=UP * 0.1), run_time=0.4)
        self.at("lecture")
        self.play(FadeIn(lect, shift=UP * 0.1), run_time=0.4)

        # the lecture was mostly careful: tidy lines of text
        self.at("mostly spent")
        widths = [6.2, 5.4, 6.0, 4.2]
        bars = VGroup(*[Rectangle(width=w, height=0.12, stroke_width=0, fill_color=GREY, fill_opacity=0.55)
                        .move_to([fx - 3.1 + w / 2, 2.0 - 0.4 * i, 0]) for i, w in enumerate(widths)])
        self.play(LaggedStart(*[GrowFromEdge(b, LEFT) for b in bars], lag_ratio=0.3), run_time=1.1)
        self.at("careful")
        careful = T("mostly careful", 26, GREY).move_to([fx, 0.32, 0])
        self.play(FadeIn(careful, shift=UP * 0.1), run_time=0.4)

        # the most formidable organic chemist in Germany
        self.at("the most formidable")
        l1 = T("the most formidable organic chemist", 28, GOLD)
        l2 = T("in Germany", 28, GOLD)
        txt = VGroup(l1, l2).arrange(DOWN, buff=0.12)
        box = RoundedRectangle(corner_radius=0.14, width=txt.width + 0.5, height=txt.height + 0.4, stroke_color=GOLD,
                               stroke_width=2.5, fill_color=GOLD, fill_opacity=0.14)
        gchip = VGroup(box, txt.move_to(box)).move_to([fx, -2.0, 0])
        self.play(FadeIn(gchip, shift=UP * 0.15), Indicate(self.border, color=GOLD, scale_factor=1.03), run_time=0.7)

        # let one metaphor escape
        self.at("let one")
        self.play(FadeOut(careful), run_time=0.15)
        meta = self.chip_at("one metaphor", GOLD, fx, -0.6, 30)
        meta.set_z_index(5)
        self.play(FadeIn(meta, shift=DOWN * 1.0), run_time=0.8)
        self.at("escape")
        self.play(bars.animate.set_opacity(0.2), Indicate(meta, color=GOLD, scale_factor=1.08), run_time=0.6)

        # --- the lock-and-key schematic: to explain why an enzyme tears apart one molecule and ignores its near-twin
        self.at("To explain")
        phaseA = Group(frame, yr, berlin, lect, bars, gchip, meta)
        ez = cup(BLUE, x=CX, base_y=-0.8)
        sub = substrate().move_to([CX, 1.7, 0])
        self.play(FadeOut(phaseA), run_time=0.4)
        self.play(FadeIn(ez, shift=UP * 0.15), FadeIn(sub, shift=DOWN * 0.15), run_time=0.5)
        self.at("an enzyme")
        lab_e = T("enzyme", 28, BLUE).move_to([CX, -0.8 - BT / 2 - 0.45, 0])
        self.play(FadeIn(lab_e, shift=UP * 0.1), run_time=0.3)

        self.at("would tear", lead=0.45)
        self.play(sub.animate.move_to(cavity_slot(ez)), run_time=0.5, rate_func=smooth)
        self.at("apart")
        self.play(sub[0].animate.shift(LEFT * 1.3 + UP * 1.6).rotate(0.3),
                  sub[1].animate.shift(RIGHT * 1.3 + UP * 1.6).rotate(-0.3), run_time=0.45)
        self.at("one molecule")
        lab_m = T("one molecule", 30, GREEN).move_to([CX, 2.8, 0])
        self.play(FadeIn(lab_m, shift=UP * 0.1), run_time=0.3)

        # ... and ignores its near-twin
        self.at("ignore")
        twin = block(2.5, SUB_H, GREEN, 0.5).move_to([CX, 1.7, 0])
        self.play(FadeOut(sub), FadeIn(twin, shift=DOWN * 0.1), run_time=0.3)
        self.at("near twin")
        lab_t = T("its near-twin", 30, GREY).move_to([CX, 2.8, 0])
        rim = ez[1].get_top()[1] + SUB_H / 2
        self.play(ReplacementTransform(lab_m, lab_t), twin.animate.move_to([CX, rim, 0]), run_time=0.6)
        cross = VGroup(Line(UL, DR), Line(UR, DL)).scale(0.34).set_color(RED).set_stroke(width=8).move_to([CX, rim, 0])
        cross.set_z_index(6)
        self.play(Create(cross), run_time=0.3)
        self.play(twin.animate.shift(UP * 0.9 + RIGHT * 2.2).set_opacity(0.0),
                  cross.animate.shift(UP * 0.9 + RIGHT * 2.2).set_opacity(0.0), run_time=0.5)

        # ... enzyme and substrate had to fit like lock and key
        self.at("enzyme and substrate")
        sub2 = substrate().move_to(cavity_slot(ez))
        self.play(FadeIn(sub2, shift=DOWN * 1.2), run_time=0.45)
        self.at("substrate")
        lab_s = T("substrate", 30, GREEN).move_to([CX, 2.8, 0])
        self.play(ReplacementTransform(lab_t, lab_s), run_time=0.3)
        self.at("had to fit")
        fitbox = Rectangle(width=CAV + 0.3, height=SUB_H + 0.3, stroke_color=GOLD, stroke_width=5,
                           fill_opacity=0).move_to(cavity_slot(ez)).set_z_index(6)
        self.play(Create(fitbox), run_time=0.5)
        self.at("like lock and key")
        quote = T("“like lock and key”", 40, GOLD, font=TITLE_FONT).move_to([CX, -2.75, 0])
        self.play(Write(quote), Indicate(fitbox, color=GOLD, scale_factor=1.12), run_time=1.5)
        self.finish()


class S02Distrust(BioScene):
    def construct(self):
        self.add_column()
        py = 0.0          # row centred on the frame so the lower half is not left empty
        pcx = -0.85
        # the picture: cup + key in a gold frame
        pic = VGroup(cup(BLUE), substrate())
        pic[1].move_to(cavity_slot(pic[0]))
        pic.scale(0.55).move_to([pcx, py, 0])
        pframe = RoundedRectangle(corner_radius=0.15, width=2.4, height=1.5, stroke_color=GOLD, stroke_width=3.5,
                                  fill_opacity=0).move_to([pcx, py, 0])
        ptxt = T("the picture", 24, GOLD).move_to([pcx, py - 1.1, 0])

        self.at("distrusted")
        dis = self.chip_at("distrusted", RED, -1.3, 1.7, 26)
        self.play(FadeIn(dis, shift=DOWN * 0.1), run_time=0.4)
        self.at("the picture")
        self.play(Create(pframe), FadeIn(pic), FadeIn(ptxt), run_time=0.6)
        self.at("offered it")
        off = self.chip_at("offered it", GOLD, 1.15, 1.7, 26)
        self.play(FadeIn(off, shift=DOWN * 0.1), run_time=0.4)

        self.at("confirmed")
        a1 = Arrow([pcx + 1.35, py, 0], [2.15, py, 0], buff=0, color=GREY, stroke_width=4, max_tip_length_to_length_ratio=0.3)
        conf = T("confirmed?", 24, GOLD).move_to([(pcx + 1.35 + 2.15) / 2, py + 0.45, 0])
        self.play(GrowArrow(a1), FadeIn(conf), run_time=0.5)

        self.at("isolate")
        tx = 2.85
        tube = RoundedRectangle(corner_radius=0.25, width=1.0, height=2.0, stroke_color=GREY, stroke_width=4,
                                fill_opacity=0).move_to([tx, py, 0])
        self.play(Create(tube), run_time=0.4)
        self.at("pure enzyme")
        liquid = RoundedRectangle(corner_radius=0.2, width=0.86, height=1.25, stroke_width=0, fill_color=BLUE,
                                  fill_opacity=0.85).move_to([tx, py - 1.0 + 0.625 + 0.07, 0])
        tl = T("pure enzyme", 26, BLUE).move_to([tx, py - 1.5, 0])
        self.play(GrowFromEdge(liquid, DOWN), FadeIn(tl, shift=UP * 0.1), run_time=0.5)

        self.at("see its shape")
        bx = 5.25
        a2 = Arrow([tx + 0.65, py, 0], [bx - 0.95, py, 0], buff=0, color=GREY, stroke_width=4, max_tip_length_to_length_ratio=0.35)
        blob = ParametricFunction(
            lambda t: np.array([0.72 * (1 + 0.16 * np.sin(2 * t) + 0.1 * np.sin(3 * t + 1)) * np.cos(t),
                                0.58 * (1 + 0.16 * np.sin(2 * t) + 0.1 * np.sin(3 * t + 1)) * np.sin(t), 0]),
            t_range=[0, TAU, 0.05], color=BLUE, stroke_width=5, fill_color=BLUE, fill_opacity=0.25).move_to([bx, py, 0])
        sh = T("its shape", 26, BLUE).move_to([bx, py - 1.5, 0])
        self.play(GrowArrow(a2), Create(blob), FadeIn(sh, shift=UP * 0.1), run_time=0.8)
        self.finish()


class S03Flex(BioScene):
    def construct(self):
        self.add_column()
        # --- most of a century
        self.at("He was right", lead=0.0)
        right = T("He was right.", 44, GOLD, font=TITLE_FONT).move_to([CX, 2.65, 0])
        self.play(Write(right), run_time=0.8)
        self.at("most of a century")
        x0, x1, by = -1.0, 5.3, 0.9
        yr = M("1894", 30, YELLOW).move_to([x0, by - 0.55, 0])
        tick = Line([x0, by - 0.2, 0], [x0, by + 0.2, 0], color=YELLOW, stroke_width=5)
        bar = Line([x0, by, 0], [x1, by, 0], color=YELLOW, stroke_width=7)
        lab = T("most of a century", 30, YELLOW).move_to([CX + 0.15, by + 0.7, 0])
        self.play(FadeIn(tick), FadeIn(yr), Create(bar), FadeIn(lab, shift=UP * 0.1), run_time=1.4, rate_func=linear)
        self.at("crystallographers")
        cr = self.chip_at("crystallographers", PINK, CX + 1.0, -0.8, 28)
        self.play(FadeIn(cr, shift=UP * 0.1), run_time=0.5)
        self.at("finally")
        arr = Arrow([x1, -0.45, 0], [x1, by - 0.1, 0], buff=0, color=PINK, stroke_width=5, max_tip_length_to_length_ratio=0.3)
        end = Dot([x1, by, 0], radius=0.14, color=PINK)
        self.play(GrowArrow(arr), FadeIn(end, scale=0.5), run_time=0.6)

        # --- rigid brass lock vs. flexing enzyme
        self.at("found enzymes", lead=0.55)
        self.play(FadeOut(Group(right, tick, yr, bar, lab, cr, arr, end)), run_time=0.35)
        self.at("found enzymes")
        ech = self.chip_at("enzymes", BLUE, CX, 2.95, 30)
        self.play(FadeIn(ech, shift=DOWN * 0.1), run_time=0.4)
        cav, by0 = 2.5, -0.45
        gold_cup = cup(GOLD, cav=cav, x=CX, base_y=by0)
        self.at("sit rigid")
        self.play(FadeIn(gold_cup, shift=UP * 0.15), run_time=0.5)
        self.at("brass lock")
        lock_lab = T("rigid brass lock", 28, GOLD).move_to([CX, by0 - BT / 2 - 0.5, 0])
        self.play(FadeIn(lock_lab, shift=UP * 0.1), run_time=0.4)

        self.at("but flex")
        blue_cup = cup(BLUE, cav=cav, x=CX, base_y=by0)
        flex_lab = T("flex", 28, BLUE).move_to([CX, by0 - BT / 2 - 0.5, 0])
        self.play(ReplacementTransform(gold_cup, blue_cup), ReplacementTransform(lock_lab, flex_lab), run_time=0.4)
        self.play(*jaws(blue_cup, cav, -0.16), run_time=0.25)
        self.play(*jaws(blue_cup, cav, 0.16), run_time=0.25)

        self.at("close around")
        sub = substrate(w=1.9, h=SUB_H).move_to(cavity_slot(blue_cup))
        self.play(FadeIn(sub, shift=DOWN * 0.5), run_time=0.3)
        self.play(*jaws(blue_cup, cav, 0.29), run_time=0.55)
        self.at("what they bind")
        bind = T("what they bind", 28, GREEN).move_to([CX, 2.15, 0])
        barr = Arrow([CX, 1.85, 0], [CX, 1.4, 0], buff=0, color=GREEN, stroke_width=4, max_tip_length_to_length_ratio=0.35)
        self.play(FadeIn(bind, shift=UP * 0.1), GrowArrow(barr), run_time=0.5)

        # --- induced fit, Koshland
        self.at("induced fit")
        ind = T("“induced fit”", 46, GOLD, font=TITLE_FONT).move_to([CX, -1.3, 0])
        self.play(FadeOut(flex_lab), Write(ind), run_time=0.8)
        self.at("Koshland")
        kos = self.chip_at("Koshland", TEXT, CX, -2.6, 30)
        ka = Arrow([CX, -2.15, 0], [CX, -1.75, 0], buff=0, color=TEXT, stroke_width=4, max_tip_length_to_length_ratio=0.5)
        self.play(FadeIn(kos, shift=UP * 0.1), GrowArrow(ka), run_time=0.6)
        self.finish()


class S04Sugars(BioScene):
    def construct(self):
        self.add_column()
        # --- read the structure off the behavior
        self.at("cracked the sugars")
        sug = self.chip_at("the sugars", GREEN, CX, 2.75, 30)
        self.play(FadeIn(sug, shift=DOWN * 0.1), run_time=0.4)
        self.at("read the structure")
        struct = self.dashed_chip("structure", GREY, 4.3, 0.7)
        self.play(FadeIn(struct, shift=LEFT * 0.1), run_time=0.4)
        self.at("off the behavior")
        beh = self.chip_at("behavior", AMBER, -0.4, 0.7, 28)
        ra = Arrow([0.75, 0.7, 0], [3.1, 0.7, 0], buff=0, color=GOLD, stroke_width=5, max_tip_length_to_length_ratio=0.25)
        rl = T("read off", 24, GOLD).move_to([1.95, 1.2, 0])
        self.play(FadeIn(beh, shift=RIGHT * 0.1), GrowArrow(ra), FadeIn(rl), run_time=0.7)

        # --- caged the invisible geometry of glucose
        self.at("He had caged", lead=0.35)
        self.play(FadeOut(Group(sug, struct, beh, ra, rl)), run_time=0.3)
        self.at("caged")
        cx0, cy0 = 0.0, 0.95
        bars = VGroup(*[Line([cx0 - 1.3 + i * 0.4333, cy0 - 1.0, 0], [cx0 - 1.3 + i * 0.4333, cy0 + 1.0, 0],
                             color=GREY, stroke_width=6) for i in range(7)])
        top = Line([cx0 - 1.3, cy0 + 1.0, 0], [cx0 + 1.3, cy0 + 1.0, 0], color=GREY, stroke_width=6)
        bot = Line([cx0 - 1.3, cy0 - 1.0, 0], [cx0 + 1.3, cy0 - 1.0, 0], color=GREY, stroke_width=6)
        cage = VGroup(top, bot, bars)
        self.play(Create(top), Create(bot), LaggedStart(*[Create(b) for b in bars], lag_ratio=0.12), run_time=0.7)
        self.at("invisible")
        inner = DashedVMobject(Rectangle(width=1.5, height=1.2, color=GREEN, stroke_width=3), num_dashes=28,
                               dashed_ratio=0.55).set_color(GREEN).move_to([cx0, cy0, 0])
        inv = T("invisible geometry", 26, GREEN).move_to([cx0, cy0 - 1.45, 0])
        self.play(Create(inner), FadeIn(inv, shift=UP * 0.1), run_time=0.6)
        self.at("of glucose")
        glu = self.chip_at("glucose", GREEN, cx0, cy0 + 1.8, 30)
        self.play(FadeIn(glu, shift=DOWN * 0.1), run_time=0.4)
        self.at("melting points")
        mp = self.chip_at("melting points", AMBER, 4.2, 1.7, 26)
        a1 = Arrow([mp.get_left()[0] - 0.1, 1.7, 0], [cx0 + 1.45, 1.35, 0], buff=0, color=AMBER, stroke_width=4,
                   max_tip_length_to_length_ratio=0.2)
        self.play(FadeIn(mp, shift=LEFT * 0.15), GrowArrow(a1), run_time=0.6)
        self.at("degradation products")
        dp = self.chip_at("degradation products", AMBER, 4.2, 0.4, 26)
        a2 = Arrow([dp.get_left()[0] - 0.1, 0.4, 0], [cx0 + 1.45, 0.6, 0], buff=0, color=AMBER, stroke_width=4,
                   max_tip_length_to_length_ratio=0.2)
        self.play(FadeIn(dp, shift=LEFT * 0.15), GrowArrow(a2), run_time=0.6)

        # --- built sugars from glycerol
        self.at("built sugars", lead=0.6)
        self.play(FadeOut(Group(cage, inner, inv, glu, mp, a1, dp, a2)), run_time=0.35)
        self.at("built sugars")
        sg = self.chip_at("sugars", GREEN, 4.4, 0.9, 30)
        self.play(FadeIn(sg, shift=LEFT * 0.1), run_time=0.4)
        self.at("from glycerol")
        gl = self.chip_at("glycerol", PURPLE, -0.4, 0.9, 30)
        ba = Arrow([0.8, 0.9, 0], [3.25, 0.9, 0], buff=0, color=GREY, stroke_width=5, max_tip_length_to_length_ratio=0.25)
        bl = T("built", 24, GREY).move_to([2.0, 1.35, 0])
        self.play(FadeIn(gl, shift=RIGHT * 0.1), GrowArrow(ba), FadeIn(bl), run_time=0.7)
        self.at("life holds")
        l1 = T("life holds no chemistry", 38, TEXT, font=TITLE_FONT)
        l2 = T("beyond the ordinary", 38, TEXT, font=TITLE_FONT)
        lg = VGroup(l1, l2).arrange(DOWN, buff=0.2).move_to([CX, -1.2, 0])
        ul = Line(lg.get_corner(DL) + DOWN * 0.15, lg.get_corner(DR) + DOWN * 0.15, color=GOLD, stroke_width=4)
        self.play(Write(lg), run_time=1.7)
        self.play(Create(ul), run_time=0.4)

        # --- named the peptide bond
        self.at("named the peptide", lead=0.7)
        self.play(FadeOut(Group(sg, gl, ba, bl, lg, ul)), run_time=0.35)
        self.at("named")
        nm = T("named", 28, GREY).move_to([CX, 1.85, 0])
        self.play(FadeIn(nm, shift=DOWN * 0.1), run_time=0.3)
        self.at("peptide bond")
        pb = self.chip_at("the peptide bond", TEXT, CX, 0.85, 34)
        self.play(FadeIn(pb, shift=UP * 0.1), run_time=0.5)

        # --- trained a generation of Nobel laureates
        self.at("and trained", lead=0.5)
        self.play(FadeOut(Group(nm, pb)), run_time=0.3)
        self.at("and trained", lead=0.4)
        dots = VGroup(*[Circle(radius=0.3, color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.3)
                        .move_to([CX - 2.975 + 0.85 * i, 0.6, 0]) for i in range(8)])
        self.play(LaggedStart(*[FadeIn(d, scale=0.6) for d in dots], lag_ratio=0.15), run_time=0.55)
        self.at("a generation")
        gen = T("a generation", 30, GREY).move_to([CX, 1.7, 0])
        self.play(FadeIn(gen, shift=DOWN * 0.1), run_time=0.4)
        self.at("Nobel")
        nl = T("Nobel laureates", 36, GOLD, font=TITLE_FONT).move_to([CX, -0.55, 0])
        self.play(*[d.animate.set_color(GOLD).set_fill(GOLD, 0.3) for d in dots], FadeIn(nl, shift=UP * 0.1),
                  gen.animate.set_color(GOLD), run_time=0.7)
        self.finish()


class S05End(BioScene):
    def construct(self):
        self.add_column()
        self.at("phenylhydrazine")
        ph = self.chip_at("phenylhydrazine", RED, 1.6, 2.5, 30)
        self.play(FadeIn(ph, shift=DOWN * 0.1), run_time=0.5)
        self.at("fingerprinted")
        sg = self.chip_at("his sugars", GREEN, 4.3, 1.0, 28)
        fa = Arrow([2.2, 2.0, 0], [3.6, 1.45, 0], buff=0, color=RED, stroke_width=4, max_tip_length_to_length_ratio=0.3)
        fl = T("fingerprinted", 24, RED).move_to([4.5, 2.1, 0])
        self.play(GrowArrow(fa), FadeIn(fl), FadeIn(sg, shift=UP * 0.1), run_time=0.7)
        self.at("slowly")
        pa = Arrow([-0.15, 2.5, 0], [-2.7, 2.5, 0], buff=0, color=RED, stroke_width=5, max_tip_length_to_length_ratio=0.18)
        pl = T("slowly", 26, RED).move_to([-1.4, 2.95, 0])
        self.play(GrowArrow(pa), FadeIn(pl), self.dim.animate.set_fill(BG, 0.55), run_time=1.8, rate_func=smooth)
        self.at("He died")
        x0, x1, ty = -0.4, 4.4, -1.3
        line = Line([x0, ty, 0], [x1, ty, 0], color=GREY, stroke_width=4)
        t0 = Line([x0, ty - 0.18, 0], [x0, ty + 0.18, 0], color=YELLOW, stroke_width=5)
        t1 = Line([x1, ty - 0.18, 0], [x1, ty + 0.18, 0], color=YELLOW, stroke_width=5)
        y0 = M("1852", 32, YELLOW).move_to([x0, ty + 0.6, 0])
        self.play(Create(line), FadeIn(t0), FadeIn(y0), run_time=0.5)
        self.at("1919")
        y1 = M("1919", 54, YELLOW).move_to([x1 - 0.3, ty + 0.75, 0])
        self.play(FadeIn(t1), Write(y1), run_time=0.7)
        self.finish()


class S06Quote(BioScene):
    def construct(self):
        self.add_column()
        lines = [T("“Enzyme and glucoside must fit", 40, TEXT, font=TITLE_FONT),
                 T("together like a lock and key.”", 40, TEXT, font=TITLE_FONT)]
        qg = VGroup(*lines).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        fit(qg, max_w=8.0)
        qg.move_to([CX + 0.1, 1.0, 0])
        att = T("— Emil Fischer", 30, GOLD).next_to(qg, DOWN, buff=0.6).align_to(qg, RIGHT)
        bar = Rectangle(width=0.07, height=qg.height, stroke_width=0, fill_color=GOLD, fill_opacity=1)
        bar.next_to(qg, LEFT, buff=0.2)
        self.wait(0.4)
        self.play(FadeIn(bar), run_time=0.4)
        for ln in lines:
            self.play(FadeIn(ln, shift=RIGHT * 0.15), run_time=0.8)
            self.wait(0.3)
        self.play(FadeIn(att, shift=UP * 0.1), run_time=0.6)
        # the picture the quote describes: the key drops into the lock
        ez = VGroup(cup(BLUE, x=CX + 0.1, base_y=-3.05)).scale(0.6, about_point=[CX + 0.1, -3.05, 0])
        key = substrate().scale(0.6).move_to([CX + 0.1, -1.6, 0])
        self.play(FadeIn(ez), FadeIn(key), run_time=0.4)
        self.play(key.animate.move_to([CX + 0.1, -3.05 + (BT / 2 + SUB_H / 2) * 0.6, 0]), run_time=0.7)
        self.finish()


class S07End(BioScene):
    def construct(self):
        img, border = portrait(height=2.3, center=(0, 2.0))
        cap = T(CAPTION, 22, GREY).move_to([0, 2.0 - 1.15 - 0.3, 0])
        l1 = T("Framed enzyme specificity as a", 38, font=TITLE_FONT)
        l2 = T("geometric lock-and-key fit.", 38, font=TITLE_FONT)
        lg = VGroup(l1, l2).arrange(DOWN, buff=0.2).move_to([0, -0.55, 0])
        fit(lg, max_w=11.5)
        sub = T("biochemistrypedia.com", 24, TEAL).move_to([0, -1.85, 0])
        src = T("Source: The Molecule Hunters (v10), “The Invisible Machines: Enzymes and Catalysis”", 22, GREY)
        fit(src, max_w=11.8)
        src.move_to([0, -2.6, 0])
        self.play(FadeIn(img), FadeIn(border), FadeIn(cap), run_time=0.5)
        self.play(FadeIn(lg, shift=UP * 0.15), run_time=0.6)
        self.play(FadeIn(sub), FadeIn(src), run_time=0.4)
        self.finish()
