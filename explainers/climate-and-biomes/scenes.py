"""Climate and biomes: sunlight sets climate, not biomes  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = sunlight / solar energy (the Sun, rays, spots, the 1,360 and 340 numbers)
  TEAL   = the planet (Earth, its orbit)
  BLUE   = water: moist air, rain, the precipitation line
  ORANGE = dry: dry air, desert, dry-season marks
  RED    = heat: the temperature line, fire
  GREEN  = vegetation: trees, forest, the Af class chip
  GREY   = ground, axes, structure, de-emphasized
  TEXT   = air flow arrows, general labels
  GOLD   = title rule only
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
MONTHS = "JFMAMJJASOND"
RAIN = [140, 120, 150, 180, 200, 160, 140, 110, 90, 100, 130, 160]   # the lesson's made-up station, mm
TEMP = 26                                                            # degrees C every month


def arr(a, b, color=TEXT, w=5, tip=0.22):
    return Arrow(a, b, buff=0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def bt(text, size=24, color=TEXT, **kw):
    return T(text, size, color, **kw)


def mt(text, size=26, color=TEXT, **kw):
    return M(text, size, color, **kw)


def unit(v):
    v = np.array(v, float)
    return v / np.linalg.norm(v)


def sun_glyph(pos, r=0.34):
    core = Circle(radius=r, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.9)
    return core.move_to(pos)


def earth_glyph(pos, r=0.62, tilt=23.4, color=TEAL):
    body = Circle(radius=r, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.28).move_to(pos)
    th = np.radians(tilt)
    up = np.array([np.sin(th), np.cos(th), 0.0])
    axis = Line(pos - up * (r + 0.42), pos + up * (r + 0.42), color=TEXT, stroke_width=4)
    npole = Dot(pos + up * (r + 0.42), radius=0.09, color=TEXT)
    g = VGroup(body, axis, npole)
    g.body, g.axis, g.npole, g.up = body, axis, npole, up
    return g


class S00Title(TitleCard):
    LESSON = "Climate, biomes and environmental variation"
    TITLE = "Sunlight sets climate, not biomes"


# ---------------------------------------------------------------------------------------------
class S01Tilt(SpokenScene):
    """Earth nearest the Sun in January yet winter in the north: distance is crossed out, the tilt takes over."""

    def construct(self):
        C = np.array([0.0, -0.3, 0])
        EX = 4.7
        orbit = Ellipse(width=2 * EX, height=5.9, color=TEAL, stroke_width=3, stroke_opacity=0.55).move_to(C)
        sun = sun_glyph(C + np.array([0.12, 0, 0]), 0.85)
        sun_l = bt("Sun", 26, YELLOW).next_to(sun, DOWN, buff=0.18)
        right = earth_glyph(C + np.array([EX, 0, 0]), r=0.75)
        jan = bt("early January", 26).next_to(right.body, DOWN, buff=0.6)
        closest = bt("closest to the Sun", 24, GREY).next_to(jan, DOWN, buff=0.12)

        self.at("closest to the Sun")
        self.play(Create(orbit), FadeIn(sun, scale=0.8), FadeIn(sun_l), run_time=0.9)
        self.play(FadeIn(right, scale=0.8), FadeIn(jan), FadeIn(closest), run_time=0.6)

        self.at("winter in the north")
        north_w = bt("north: winter", 28, TEXT, weight=BOLD).move_to(right.body.get_center() + np.array([0, 2.0, 0]))
        self.play(FadeIn(north_w, shift=UP * 0.1), run_time=0.5)

        # distance: drawn, then set aside
        self.at("distance does not")
        dline = DoubleArrow(sun.get_right() + RIGHT * 0.1, right.body.get_left() + LEFT * 0.1, buff=0, color=GREY,
                            stroke_width=4, tip_length=0.2)
        dlab = bt("distance", 26, GREY).next_to(dline, UP, buff=0.12)
        few = bt("distance differs by a few percent", 24, GREY).move_to(C + np.array([0.1, -2.0, 0]))
        self.play(FadeIn(few), run_time=0.01)
        self.play(GrowFromCenter(dline), FadeIn(dlab), run_time=0.5)
        strike = Line(dlab.get_left() + LEFT * 0.12, dlab.get_right() + RIGHT * 0.12, color=TEXT, stroke_width=5)
        self.wait(0.2)
        self.play(Create(strike), dline.animate.set_opacity(0.25), run_time=0.4)
        self.wait(0.3)
        self.play(FadeOut(VGroup(dline, dlab, strike)), run_time=0.4)

        # the tilt
        self.at("axis is tilted")
        rc = right.body.get_center()
        vert = DashedLine(rc, rc + UP * 1.6, color=GREY, stroke_width=3)
        arc = Arc(radius=1.3, start_angle=PI / 2, angle=-np.radians(23.4), arc_center=rc, color=YELLOW, stroke_width=4)
        deg = mt("23.4°", 24, YELLOW).move_to(rc + np.array([-0.75, 1.45, 0]))
        self.play(Create(vert), Create(arc), FadeIn(deg), run_time=0.7)
        self.wait(0.2)

        self.at("each hemisphere")
        left = earth_glyph(C + np.array([-EX, 0, 0]), r=0.75)
        jul = bt("early July", 26).next_to(left.body, DOWN, buff=0.6)
        self.play(FadeIn(left, scale=0.8), FadeIn(jul), FadeOut(deg), FadeOut(vert), FadeOut(arc), run_time=0.6)

        self.at("leans toward the Sun")
        lean = bt("north leans toward the Sun", 24, YELLOW)
        more = bt("more direct light, longer days", 24, YELLOW)
        lab = VGroup(more, lean).arrange(DOWN, buff=0.1).move_to(left.body.get_center() + np.array([0.2, 2.0, 0]))
        glow = Circle(radius=0.26, color=YELLOW, stroke_width=4).move_to(left.npole)
        lit = Arc(radius=0.75, start_angle=-PI / 2, angle=PI, arc_center=left.body.get_center(), color=YELLOW,
                  stroke_width=7)
        lit_r = Arc(radius=0.75, start_angle=PI / 2, angle=PI, arc_center=right.body.get_center(), color=YELLOW,
                    stroke_width=7)
        self.play(FadeIn(lean), Create(glow), left.npole.animate.set_color(YELLOW), FadeIn(lit), FadeIn(lit_r),
                  run_time=0.7)
        self.at("more direct light")
        self.play(FadeIn(more, shift=UP * 0.1), run_time=0.6)
        self.wait(0.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Slant(SpokenScene):
    """Two beams of equal width: head-on makes a short bright spot, a slanted one spreads out and dims."""

    def construct(self):
        gy = -1.9
        th = np.radians(60)
        d = np.array([np.sin(th), -np.cos(th), 0])
        p = np.array([np.cos(th), np.sin(th), 0])
        w = 1.2

        # left: head-on
        lx = -3.7
        ground_l = Line([-5.9, gy, 0], [-1.5, gy, 0], color=GREY, stroke_width=5)
        beam_l = Polygon([lx - w / 2, 1.5, 0], [lx + w / 2, 1.5, 0], [lx + w / 2, gy, 0], [lx - w / 2, gy, 0],
                         stroke_width=0, fill_color=YELLOW, fill_opacity=0.28)
        rays_l = VGroup(*[arr([lx + k * 0.4, 1.4, 0], [lx + k * 0.4, gy + 0.05, 0], YELLOW, 4, 0.18) for k in (-1, 0, 1)])
        sun_l = sun_glyph([lx, 2.45, 0], 0.32)
        spot_l = Line([lx - w / 2, gy, 0], [lx + w / 2, gy, 0], color=YELLOW, stroke_width=14)
        lab_l = bt("head-on", 26).move_to([lx, gy - 0.6, 0])
        val_l = mt("1,360 W/m²", 26, YELLOW).move_to([lx, gy - 1.1, 0])

        # right: 60 degrees from overhead, same beam width
        g1x, g2x = 3.3, 5.7
        mid = np.array([(g1x + g2x) / 2, gy, 0])
        c = mid - d * 6.0
        t1, t2 = c + p * (w / 2), c - p * (w / 2)
        # extend each edge down to the ground
        e1 = t1 + d * ((t1[1] - gy) / (-d[1]))
        e2 = t2 + d * ((t2[1] - gy) / (-d[1]))
        ground_r = Line([2.3, gy, 0], [6.2, gy, 0], color=GREY, stroke_width=5)
        beam_r = Polygon(t1, t2, e2, e1, stroke_width=0, fill_color=YELLOW, fill_opacity=0.28)
        rays_r = VGroup(*[arr(c + p * k * 0.4 + d * 0.0, c + p * k * 0.4 + d * ((c[1] + p[1] * k * 0.4 - gy) / (-d[1]) - 0.1),
                              YELLOW, 4, 0.18) for k in (-1, 0, 1)])
        sun_r = sun_glyph(c - d * 0.9, 0.32)
        spot_r = Line(e2, e1, color=YELLOW, stroke_width=14).set_opacity(0.5)
        # angle from overhead
        over = DashedLine(mid, mid + UP * 1.7, color=GREY, stroke_width=3)
        arc = Arc(radius=1.3, start_angle=PI / 2, angle=np.radians(60), arc_center=mid, color=YELLOW, stroke_width=4)
        a60 = mt("60°", 24, YELLOW).move_to(mid + np.array([-0.55, 1.65, 0]))
        a60.shift(LEFT * 0.35)
        lab_r = bt("Sun 60° from overhead", 26).move_to([mid[0] - 0.5, gy - 0.5, 0])
        v1 = mt("1,360 × cos 60°", 24, YELLOW)
        v2 = mt("= 680 W/m² (half)", 26, YELLOW, weight=BOLD)
        val_r = VGroup(v1, v2).arrange(DOWN, buff=0.1)
        val_r.move_to([mid[0] - 0.5, gy - 1.3, 0])
        v2.set_opacity(0)

        self.at("straight down")
        self.play(FadeIn(ground_l), FadeIn(sun_l), run_time=0.4)
        self.play(FadeIn(beam_l), LaggedStart(*[GrowArrow(a) for a in rays_l], lag_ratio=0.2), run_time=0.9)
        self.at("small bright spot")
        self.play(Create(spot_l), FadeIn(lab_l), run_time=0.6)

        self.at("Tilt it")
        self.play(FadeIn(ground_r), FadeIn(sun_r), run_time=0.4)
        self.play(FadeIn(beam_r), LaggedStart(*[GrowArrow(a) for a in rays_r], lag_ratio=0.2), run_time=0.9)
        self.at("covers more ground")
        self.play(Create(spot_r), run_time=0.7)

        self.at("top of the atmosphere")
        self.play(FadeIn(val_l, shift=UP * 0.1), run_time=0.6)

        self.at("from overhead")
        self.play(Create(over), Create(arc), FadeIn(a60), FadeIn(lab_r), run_time=0.8)
        self.at("flat surface")
        self.play(FadeIn(v1, shift=UP * 0.1), run_time=0.5)
        self.at("half of that")
        self.play(v2.animate.set_opacity(1), run_time=0.4)
        self.play(Indicate(v2, color=YELLOW, scale_factor=1.06), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Planet(SpokenScene):
    """Rays on a planet: the disk it catches, the sphere it spreads over (4x), 1,360 / 4 = 340, tropics more than poles."""

    def construct(self):
        R = 2.3
        pc = np.array([-0.6, 0.0, 0])
        planet = Circle(radius=R, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.22).move_to(pc)
        ys = np.array([-0.9, -0.6, -0.3, 0.0, 0.3, 0.6, 0.9]) * R
        x0 = -6.1
        rays, dots = [], []
        for y in ys:
            hx = pc[0] - np.sqrt(R ** 2 - y ** 2)
            rays.append(arr([x0, y, 0], [hx - 0.03, y, 0], YELLOW, 4, 0.18))
            dots.append(Dot([hx, y, 0], radius=0.09, color=YELLOW))
        rays, dots = VGroup(*rays), VGroup(*dots)

        self.at("spread that light")
        self.play(FadeIn(planet, scale=0.9), run_time=0.6)
        self.play(LaggedStart(*[GrowArrow(a) for a in rays], lag_ratio=0.1), FadeIn(dots), run_time=1.0)

        self.at("on a disk")
        bx = -4.9
        disk = Line([bx, -R, 0], [bx, R, 0], color=YELLOW, stroke_width=10)
        disk_lab = bt("disk", 26, YELLOW).next_to(disk, UP, buff=0.2)
        disk_eq = mt("π r²", 26, YELLOW).next_to(disk, DOWN, buff=0.2)
        self.play(Create(disk), FadeIn(disk_lab), FadeIn(disk_eq), run_time=0.8)

        self.at("over a sphere")
        ring = Circle(radius=R + 0.14, stroke_color=YELLOW, stroke_width=7).move_to(pc)
        sph_eq = mt("sphere: 4 π r²", 26, YELLOW).move_to([pc[0] + 0.0, -R - 0.55, 0])
        self.play(Create(ring), FadeIn(sph_eq), run_time=0.9)

        self.at("four times the area")
        four = mt("4 × the disk", 28, YELLOW, weight=BOLD).move_to([4.7, 2.2, 0])
        self.play(Write(four), run_time=0.7)

        self.at("global mean")
        eq1 = mt("1,360 ÷ 4", 34, YELLOW).move_to([4.7, 0.9, 0])
        self.play(FadeIn(eq1, shift=UP * 0.1), run_time=0.6)
        self.at("watts per square")
        eq2 = mt("= 340 W/m²", 34, YELLOW, weight=BOLD).next_to(eq1, DOWN, buff=0.25)
        note = bt("global mean,\ntop of atmosphere", 24, GREY).next_to(eq2, DOWN, buff=0.25)
        self.play(FadeIn(eq2, shift=UP * 0.1), FadeIn(note), run_time=0.7)

        self.at("The tropics")
        self.play(FadeOut(VGroup(four, eq1, note)), eq2.animate.move_to([4.7, 2.3, 0]).scale(0.8), run_time=0.5)
        cosv = np.sqrt(1 - (ys / R) ** 2)
        anims = []
        for a, dd, cv in zip(rays, dots, cosv):
            anims.append(a.animate.set_stroke(opacity=0.25 + 0.75 * cv))
            anims.append(dd.animate.set_opacity(0.2 + 0.8 * cv).scale(0.5 + 0.7 * cv))
        trop = bt("tropics: more", 26, YELLOW, weight=BOLD).move_to([pc[0] + R + 1.75, 0, 0])
        tarr = arr([pc[0] + R + 0.2, 0.0, 0], [pc[0] + R + 0.6, 0.0, 0], YELLOW, 4, 0.16)
        self.play(*anims, FadeIn(trop), run_time=0.9)
        self.at("poles get less")
        pol_t = bt("poles: less", 26, GREY, weight=BOLD).move_to([pc[0] + 0.0, R + 0.62, 0])
        pol_b = bt("poles: less", 26, GREY, weight=BOLD).move_to([pc[0] + 0.0, -R - 0.62, 0])
        self.play(FadeIn(pol_t), FadeIn(pol_b), FadeOut(sph_eq), run_time=0.7)
        self.wait(0.3)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Cell(SpokenScene):
    """The Hadley cell: moist air rises and rains at the equator, dry air sinks over the desert."""

    def construct(self):
        W, H, CR = 7.0, 4.4, 0.9
        C = np.array([0.1, -0.15, 0])
        xL, xR, yB, yT = C[0] - W / 2, C[0] + W / 2, C[1] - H / 2, C[1] + H / 2
        arcl = np.pi / 2 * CR
        sv, sh = H - 2 * CR, W - 2 * CR
        # clockwise path, starting where the bottom edge meets the lower-left corner
        lens = [arcl, sv, arcl, sh, arcl, sv, arcl, sh]
        cum = np.concatenate([[0], np.cumsum(lens)])

        def pos(s):
            s = max(0.0, min(s, cum[-1] - 1e-6))
            k = int(np.searchsorted(cum, s, side="right") - 1)
            u = s - cum[k]
            if k == 0:
                a = np.radians(270) - u / CR
                return np.array([xL + CR + CR * np.cos(a), yB + CR + CR * np.sin(a), 0])
            if k == 1:
                return np.array([xL, yB + CR + u, 0])
            if k == 2:
                a = np.radians(180) - u / CR
                return np.array([xL + CR + CR * np.cos(a), yT - CR + CR * np.sin(a), 0])
            if k == 3:
                return np.array([xL + CR + u, yT, 0])
            if k == 4:
                a = np.radians(90) - u / CR
                return np.array([xR - CR + CR * np.cos(a), yT - CR + CR * np.sin(a), 0])
            if k == 5:
                return np.array([xR, yT - CR - u, 0])
            if k == 6:
                a = -u / CR
                return np.array([xR - CR + CR * np.cos(a), yB + CR + CR * np.sin(a), 0])
            return np.array([xR - CR - u, yB, 0])

        def seg(a, b, color, width=7):
            n = max(8, int((b - a) / 0.05))
            pts = [pos(a + (b - a) * i / n) for i in range(n + 1)]
            m = VMobject().set_points_as_corners(pts)
            m.set_stroke(color, width).set_fill(opacity=0)
            m.pts_end = (pts[-1], pts[-2])
            return m

        rise = (0, cum[3])
        aloft = (cum[3], cum[5])
        sink = (cum[5], cum[7])
        back = (cum[7], cum[8])

        def tip(m, color):
            end, prev = m.pts_end
            ang = angle_of_vector(end - prev)
            tp = ArrowTriangleFilledTip(color=color, length=0.3, width=0.3)
            tp.rotate(ang - tp.start_angle)
            tp.shift(end - tp.tip_point)
            m.tipobj = tp
            return m

        # ground and labels
        ground = Line([-6.3, -2.62, 0], [6.3, -2.62, 0], color=GREY, stroke_width=5)
        desert = Rectangle(width=2.6, height=0.22, stroke_width=0, fill_color=ORANGE, fill_opacity=0.85).move_to(
            [xR - 0.1, -2.62, 0])
        left_lab = bt("equator", 26, BLUE, weight=BOLD).move_to([xL, -3.2, 0])
        right_lab = bt("subtropics", 26, ORANGE, weight=BOLD).move_to([xR, -3.2, 0])
        right_lab2 = bt("subtropics: Sahara, Kalahari", 26, ORANGE, weight=BOLD).move_to([xR - 0.4, -3.2, 0])
        sun_l = VGroup(*[arr([xL - 0.5 + k * 0.5, 3.55, 0], [xL - 0.5 + k * 0.5, 2.9, 0], YELLOW, 5, 0.16) for k in range(3)])
        sun_r = VGroup(*[arr([xR - 0.5 + k * 0.5, 3.55, 0], [xR - 0.5 + k * 0.5, 3.15, 0], YELLOW, 3, 0.12) for k in range(3)])
        sun_r.set_opacity(0.5)

        def cloud(center):
            cs = [Circle(radius=r, stroke_width=0, fill_color=BLUE, fill_opacity=0.5).move_to(center + off)
                  for r, off in [(0.34, [-0.4, -0.05, 0]), (0.44, [0, 0.12, 0]), (0.36, [0.42, -0.02, 0]),
                                 (0.3, [0.12, -0.12, 0])]]
            return VGroup(*cs)
        cc = np.array([xL + 1.55, 0.95, 0])
        cl = cloud(cc)
        drops = VGroup(*[Line([cc[0] + dx, y1, 0], [cc[0] + dx - 0.1, y1 - 0.4, 0], color=BLUE, stroke_width=4)
                         for y1 in (0.4, -0.4, -1.2) for dx in (-0.45, -0.15, 0.15, 0.45)])

        hadley = T("Hadley cell", 34, font=TITLE_FONT).move_to(C + np.array([0.7, -0.35, 0]))
        ideal = bt("idealized model", 24, GREY).next_to(hadley, DOWN, buff=0.15)

        self.at("uneven heating")
        self.play(FadeIn(ground), FadeIn(left_lab), FadeIn(right_lab), FadeIn(sun_l), FadeIn(sun_r), run_time=0.8)

        self.at("warm moist air rises")
        up_lab = bt("warm, moist\nair rises", 26, BLUE).move_to([xL - 1.45, 0.1, 0])
        s1 = tip(seg(*rise, BLUE), BLUE)
        self.play(Create(s1, rate_func=linear), FadeIn(up_lab), run_time=1.6)
        self.add(s1.tipobj)

        self.at("it rains")
        self.play(FadeIn(cl, shift=DOWN * 0.1), run_time=0.4)
        self.play(LaggedStart(*[Create(x) for x in drops], lag_ratio=0.1), run_time=0.9)

        self.at("flows poleward")
        s2 = tip(seg(*aloft, ORANGE), ORANGE)
        dry_lab = bt("dry air flows poleward at height", 24, ORANGE).move_to([C[0], 2.95, 0])
        self.play(Create(s2, rate_func=linear), FadeIn(dry_lab), run_time=1.6)
        self.add(s2.tipobj)

        self.at("sinks in the subtropics")
        s3 = tip(seg(*sink, ORANGE), ORANGE)
        sink_lab = bt("sinks, is\ncompressed,\nwarms", 24, ORANGE).move_to([xR + 1.35, 0.3, 0])
        self.play(Create(s3, rate_func=linear), FadeIn(sink_lab), run_time=1.2)
        self.add(s3.tipobj)

        self.at("rain is suppressed")
        nodrop = bt("no rain", 24, ORANGE).move_to([xR - 1.5, -0.9, 0])
        self.play(FadeIn(nodrop), run_time=0.5)

        self.at("Sahara")
        self.play(FadeIn(desert), ReplacementTransform(right_lab, right_lab2), FadeOut(nodrop), run_time=0.6)

        self.at("This loop")
        s4 = tip(seg(*back, TEXT, 5), TEXT)
        self.play(Create(s4, rate_func=linear), run_time=1.2)
        self.add(s4.tipobj)
        self.play(FadeIn(hadley), FadeIn(ideal), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Diagram(SpokenScene):
    """A Walter-Lieth chart of the lesson's made-up station: rain stays above the temperature line."""

    def construct(self):
        x0, x1, y0, hgt = -5.9, 2.1, -2.45, 4.5
        mm_per = hgt / 200.0           # 200 mm spans the chart height; 10 C is level with 20 mm
        def X(i): return x0 + (i + 0.5) * (x1 - x0) / 12
        def Y(mm): return y0 + mm * mm_per

        title = bt("a made-up lowland station, 30-year means", 24, GREY).move_to([-1.9, 2.9, 0])
        axl = Line([x0, y0, 0], [x0, y0 + hgt, 0], color=GREY, stroke_width=3)
        axr = Line([x1, y0, 0], [x1, y0 + hgt, 0], color=GREY, stroke_width=3)
        axb = Line([x0, y0, 0], [x1, y0, 0], color=GREY, stroke_width=3)
        ticks_l = VGroup(*[VGroup(Line([x0 - 0.1, Y(2 * t), 0], [x0, Y(2 * t), 0], color=GREY, stroke_width=3),
                                  mt(str(t), 22, RED).move_to([x0 - 0.42, Y(2 * t), 0])) for t in (0, 10, 20, 30, 40)])
        ticks_r = VGroup(*[VGroup(Line([x1, Y(m), 0], [x1 + 0.1, Y(m), 0], color=GREY, stroke_width=3),
                                  mt(str(m), 22, BLUE).move_to([x1 + 0.5, Y(m), 0])) for m in (0, 50, 100, 150, 200)])
        mlab = VGroup(*[bt(m, 22, GREY).move_to([X(i), y0 - 0.3, 0]) for i, m in enumerate(MONTHS)])
        unit_l = bt("°C", 24, RED).move_to([x0 - 0.45, y0 + hgt + 0.3, 0])
        unit_r = bt("mm", 24, BLUE).move_to([x1 + 0.5, y0 + hgt + 0.3, 0])
        frame = VGroup(axl, axr, axb, ticks_l, ticks_r, mlab, unit_l, unit_r)

        pts = [[X(i), Y(v), 0] for i, v in enumerate(RAIN)]
        rain_line = VMobject(color=BLUE, stroke_width=6).set_points_as_corners(pts)
        humid = Polygon(*pts, [X(11), Y(2 * TEMP), 0], [X(0), Y(2 * TEMP), 0], stroke_width=0, fill_color=BLUE,
                        fill_opacity=0.22)
        tline = Line([x0, Y(2 * TEMP), 0], [x1, Y(2 * TEMP), 0], color=RED, stroke_width=6)

        self.at("Walter")
        self.play(FadeIn(frame), FadeIn(title), run_time=0.6)
        self.play(Create(rain_line, rate_func=linear), run_time=1.6)

        self.at("level with")
        ref = DashedLine([x0, Y(20), 0], [x1, Y(20), 0], color=GREY, stroke_width=3)
        l10 = mt("10 °C", 22, RED, weight=BOLD).move_to([x0 + 0.85, Y(20) + 0.25, 0])
        l20 = mt("20 mm", 22, BLUE, weight=BOLD).move_to([x1 - 0.95, Y(20) + 0.25, 0])
        self.play(Create(ref), FadeIn(l10), FadeIn(l20), run_time=0.8)
        self.wait(0.4)
        self.play(FadeOut(VGroup(ref, l10, l20)), run_time=0.4)

        self.at("all year")
        self.play(Create(tline, rate_func=linear), run_time=1.0)
        t_lab = mt("26 °C", 24, RED, weight=BOLD).move_to([x0 + 1.0, Y(2 * TEMP) + 0.0 - 0.35, 0])
        self.play(FadeIn(t_lab), run_time=0.4)

        self.at("plots at")
        m52 = mt("52 mm level", 24, RED, weight=BOLD).move_to([x1 - 1.35, Y(2 * TEMP) - 0.35, 0])
        self.play(FadeIn(m52, shift=UP * 0.1), Indicate(tline, color=RED, scale_factor=1.0), run_time=0.7)

        self.at("driest month")
        dot = Dot(pts[8], radius=0.13, color=BLUE)
        ring = Circle(radius=0.28, color=TEXT, stroke_width=4).move_to(pts[8])
        sep = mt("Sep: 90 mm", 24, TEXT, weight=BOLD).move_to([pts[8][0] + 0.2, pts[8][1] - 0.62, 0])
        self.play(FadeIn(dot), Create(ring), FadeIn(sep), run_time=0.7)

        self.at("no dry period")
        self.play(FadeIn(humid), run_time=0.6)
        nodry = bt("no dry period", 28, TEXT, weight=BOLD).move_to([5.0, 1.3, 0])
        self.play(FadeIn(nodry, shift=UP * 0.1), run_time=0.6)

        self.at("rules call it")
        af = chip("Af", GREEN, size=48, pad=0.3).move_to([5.0, -0.5, 0])
        af_lab = bt("tropical\nrainforest\nclimate", 26, GREEN).next_to(af, DOWN, buff=0.25)
        self.play(FadeIn(af, scale=0.8), run_time=0.5)
        self.play(FadeIn(af_lab, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
def tree(x, y, r=0.24, trunk=0.3):
    t = Line([x, y, 0], [x, y + trunk, 0], color=GREY, stroke_width=4)
    c = Circle(radius=r, stroke_color=GREEN, stroke_width=2, fill_color=GREEN, fill_opacity=0.85).move_to([x, y + trunk + r * 0.8, 0])
    return VGroup(t, c)


def flame(x, y, s=1.0):
    pts = [[0, 0.5, 0], [0.22, 0.12, 0], [0.12, -0.3, 0], [-0.12, -0.3, 0], [-0.22, 0.12, 0]]
    f = Polygon(*pts, stroke_width=0, fill_color=RED, fill_opacity=0.95).scale(s * 0.9)
    return f.move_to([x, y, 0])


class S06Biome(SpokenScene):
    """A climate match is a hypothesis; one climate can hold forest or savanna; climate does not fix the biome."""

    def construct(self):
        # beat 1: the hypothesis
        af = chip("Af climate", GREEN, size=34).move_to([0, 1.7, 0])
        q = RoundedRectangle(corner_radius=0.2, width=5.0, height=1.7, stroke_color=GREY, stroke_width=3,
                             fill_opacity=0).move_to([0, -1.0, 0])
        qm = T("?", 64, GREY, weight=BOLD).move_to(q)
        ql = bt("vegetation actually present", 28, GREY).next_to(q, DOWN, buff=0.25)
        ar = arr([0, 1.05, 0], [0, -0.1, 0], GREY, 5, 0.22)
        self.at("hypothesis")
        self.play(FadeIn(af, shift=DOWN * 0.1), run_time=0.5)
        self.play(GrowArrow(ar), FadeIn(q), FadeIn(qm), FadeIn(ql), run_time=0.8)

        # beat 2: Staver
        pw, ph, py = 5.4, 2.8, -1.1
        pl = RoundedRectangle(corner_radius=0.2, width=pw, height=ph, stroke_color=GREY, stroke_width=3,
                              fill_opacity=0).move_to([-3.2, py, 0])
        pr = RoundedRectangle(corner_radius=0.2, width=pw, height=ph, stroke_color=GREY, stroke_width=3,
                              fill_opacity=0).move_to([3.2, py, 0])
        forest = VGroup(*[tree(-3.2 + dx, py - 1.15 + row * 0.78, 0.31, 0.25) for row in range(3)
                          for dx in np.linspace(-2.2, 2.2, 7 if row % 2 == 0 else 6)])
        sav_pos = [(-1.7, 0.1), (-0.5, 0.55), (0.8, 0.1), (1.9, 0.5), (0.2, -0.35)]
        savanna = VGroup(*[tree(3.2 + sx, py - 0.95 + (sy + 0.35) * 1.0, 0.27, 0.25) for sx, sy in sav_pos])
        grass = VGroup(*[Line([3.2 + gx, py - 1.2, 0], [3.2 + gx + 0.07, py - 1.0, 0], color=GREY, stroke_width=2)
                         for gx in np.linspace(-2.4, 2.4, 16)])
        fl = bt("forest", 28, GREEN, weight=BOLD).move_to([-3.2, py + ph / 2 + 0.3, 0])
        sv = bt("savanna", 28, GREEN, weight=BOLD).move_to([3.2, py + ph / 2 + 0.3, 0])
        a1 = arr([-0.7, 1.45, 0], [-2.7, py + ph / 2 + 0.75, 0], GREY, 4, 0.18)
        a2 = arr([0.7, 1.45, 0], [2.7, py + ph / 2 + 0.75, 0], GREY, 4, 0.18)
        self.at("Staver")
        tag = bt("tropics of Africa, Australia and South America", 24, GREY).move_to([0, 3.2, 0])
        self.play(FadeOut(VGroup(af, ar, q, qm, ql)), FadeIn(tag), FadeIn(pl), FadeIn(pr), FadeIn(forest), FadeIn(savanna),
                  FadeIn(grass), FadeIn(fl), FadeIn(sv), run_time=0.8)

        self.at("yearly rain")
        clim = chip("one climate", TEXT, size=30).move_to([0, 2.45, 0])
        clim2 = bt("rain about 1,000 to 2,500 mm a year; dry season under seven months", 22, TEXT).move_to([0, 1.8, 0])
        self.play(FadeIn(clim, shift=DOWN * 0.1), FadeIn(clim2), run_time=0.7)
        self.play(GrowArrow(a1), GrowArrow(a2), run_time=0.5)

        self.at("savanna or forest")
        self.play(Indicate(VGroup(fl, sv), color=GREEN, scale_factor=1.12), run_time=0.7)

        self.at("Fire was")
        flames = VGroup(*[flame(3.2 + fx, py - 0.95, 1.0) for fx in (-2.2, -0.9, 1.3, 2.4)])
        fire_lab = bt("fire", 26, RED, weight=BOLD).move_to([3.2, py - ph / 2 - 0.32, 0])
        self.play(FadeIn(flames, shift=UP * 0.1), FadeIn(fire_lab), run_time=0.7)
        self.at("keeping areas open")
        self.play(Indicate(flames, color=RED, scale_factor=1.15), run_time=0.7)

        self.at("alternative states")
        alt = bt("alternative states, same climate", 28, TEXT).move_to([0, -3.3, 0])
        self.play(FadeIn(alt, shift=UP * 0.1), run_time=0.6)

        self.at("Climate predicts a biome roughly")
        rule1 = T("Climate predicts a biome roughly.", 38, font=TITLE_FONT)
        rule2 = T("It does not fix it.", 38, font=TITLE_FONT, color=GOLD)
        rules = VGroup(rule1, rule2).arrange(DOWN, buff=0.25).move_to([0, 0.0, 0])
        veil = Rectangle(width=15, height=9, stroke_width=0, fill_color=BG, fill_opacity=0.97)
        self.play(FadeIn(veil), run_time=0.6)
        self.play(FadeIn(rule1, shift=UP * 0.1), run_time=0.7)
        self.at("It does not fix it")
        self.play(FadeIn(rule2, shift=UP * 0.1), run_time=0.7)
        self.finish()


class S07End(EndCard):
    LINE = "Climate predicts a biome roughly. It does not fix it."
