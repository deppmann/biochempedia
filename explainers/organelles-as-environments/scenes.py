"""Organelles as distinct environments: pumps hold each room apart (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = free protons / acidity / the held "difference" (shading, dots, gauge, pH readouts)
  TEAL   = calcium
  BLUE   = the pump (V-ATPase, SERCA, the "heater")
  GOLD   = ATP
  RED    = leak, and a blocked pump (bafilomycin, thapsigargin)
  GREEN  = "steady state" / actively kept
  GREY   = membranes, outlines, axes, labels
"""
import numpy as np
from bp_style import *  # noqa: F401,F403


def bchip(text, color=BLUE, size=24, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def btext(text, size=24, color=GREY):
    t = T(text, size, color)
    back = Rectangle(width=t.width + 0.2, height=t.height + 0.14, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(t)
    return VGroup(back, t)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def cross(center, s=0.45, color=RED):
    c = np.array(center, float)
    return VGroup(Line(c + [-s, -s, 0], c + [s, s, 0], color=color, stroke_width=8),
                  Line(c + [-s, s, 0], c + [s, -s, 0], color=color, stroke_width=8))


def scatter(n, x0, x1, y0, y1, seed, mind=0.42):
    rng = np.random.default_rng(seed)
    pts = []
    tries = 0
    while len(pts) < n and tries < 5000:
        tries += 1
        p = np.array([rng.uniform(x0, x1), rng.uniform(y0, y1), 0])
        if all(np.linalg.norm(p - q) >= mind for q in pts):
            pts.append(p)
    return pts


def hold_flow(sc, phrase, fn, rt=1.5):
    while sc.elapsed() + rt + 0.1 < sc.t_of(phrase) - 0.2:
        fn(2, 2, rt)


def dot(p, color, r=0.12):
    return Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=1).move_to(p)


def path(*pts):
    m = VMobject()
    m.set_points_as_corners([np.array(p, float) for p in pts])
    return m


def acid_shade(color=YELLOW, o=0.3):
    return dict(fill_color=color, fill_opacity=o)


class S00Title(TitleCard):
    LESSON = "Organelles as distinct environments"
    TITLE = "Pumps hold each room apart"


# ---------------------------------------------------------------------------------------------
class S01Spread(SpokenScene):
    def construct(self):
        cell = RoundedRectangle(corner_radius=2.4, width=12.2, height=6.7, stroke_color=GREY, stroke_width=5,
                                fill_color=GREY, fill_opacity=0.07).move_to([0, -0.05, 0])
        ctag = T("HeLa cell", 24, GREY).move_to([-4.6, 2.55, 0])
        self.play(Create(cell), FadeIn(ctag), run_time=1.0)

        # mitochondrion (two outlines), Golgi (three stacked bars), lysosome (circle)
        mito_o = Ellipse(width=3.3, height=2.2, stroke_color=GREY, stroke_width=5, fill_color=YELLOW, fill_opacity=0.05)
        mito_i = Ellipse(width=2.5, height=1.5, stroke_color=GREY, stroke_width=3, fill_color=YELLOW, fill_opacity=0.08)
        mito = VGroup(mito_o, mito_i).move_to([-4.0, 0.3, 0])
        golgi = VGroup(*[RoundedRectangle(corner_radius=0.2, width=3.0 - 0.25 * abs(i - 1), height=0.5, stroke_color=GREY,
                                          stroke_width=4, fill_color=YELLOW, fill_opacity=0.28)
                         for i in range(3)]).arrange(DOWN, buff=0.22).move_to([0, 0.3, 0])
        lyso = Circle(radius=1.1, stroke_color=GREY, stroke_width=5, fill_color=YELLOW, fill_opacity=0.6).move_to([4.0, 0.3, 0])

        n_m = T("mitochondrion", 26, TEXT).move_to([-4.0, 1.95, 0])
        n_g = T("Golgi", 26, TEXT).move_to([0, 1.95, 0])
        n_l = T("lysosome", 26, TEXT).move_to([4.0, 1.95, 0])
        r_m = M("pH close to 8", 24, YELLOW).move_to([-4.0, -1.1, 0])
        r_g = M("pH close to 6.6", 24, YELLOW).move_to([0, -1.1, 0])
        r_l = M("pH 4.5 to 5.0", 24, YELLOW).move_to([4.0, -1.1, 0])
        s_l = T("mammalian cells", 22, GREY).move_to([4.0, -1.6, 0])

        self.at("mitochondrion")
        self.play(FadeIn(mito, scale=0.9), FadeIn(n_m), run_time=0.8)
        self.play(FadeIn(r_m, shift=UP * 0.1), run_time=0.5)
        self.at("Golgi measured")
        self.play(FadeIn(golgi, scale=0.9), FadeIn(n_g), run_time=0.8)
        self.play(FadeIn(r_g, shift=UP * 0.1), run_time=0.5)
        self.at("lysosome sits")
        self.play(FadeIn(lyso, scale=0.9), FadeIn(n_l), run_time=0.8)
        self.play(FadeIn(r_l, shift=UP * 0.1), FadeIn(s_l), run_time=0.5)

        cyto = T("one cytosol", 30, TEXT, weight=BOLD).move_to([0, -2.55, 0])
        self.at("one cytosol")
        self.play(FadeIn(cyto, shift=UP * 0.1), Indicate(cyto, color=TEXT, scale_factor=1.1), run_time=0.9)

        qs = VGroup(*[T("?", 44, GOLD, weight=BOLD).move_to(p) for p in
                      ([-2.0, 0.3, 0], [2.0, 0.3, 0], [0, -1.9, 0])])
        self.at("keep them apart")
        self.play(LaggedStart(*[FadeIn(q, scale=1.6) for q in qs], lag_ratio=0.25), run_time=1.1)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Log(SpokenScene):
    def construct(self):
        def X(p):
            return -4.5 + (p - 6.0) * 4.5

        OFF = -1.3
        axis = Line([X(6.0) - 0.4, 1.9 + OFF, 0], [X(8.0) + 0.5, 1.9 + OFF, 0], color=GREY, stroke_width=4)
        ticks = VGroup(); tl = VGroup()
        for p in (6, 7, 8):
            ticks.add(Line([X(p), 1.8 + OFF, 0], [X(p), 2.0 + OFF, 0], color=GREY, stroke_width=4))
            tl.add(M(str(p), 26, GREY).move_to([X(p), 1.45 + OFF, 0]))
        head = T("pH", 28, GREY).move_to([X(6.0) - 0.9, 1.9 + OFF, 0])
        self.play(Create(axis), FadeIn(ticks), FadeIn(tl), FadeIn(head), run_time=0.6)

        lawf = M("pH = −log10(aH+)", 40, TEXT).move_to([0, -0.5, 0])
        self.at("is a logarithm")
        self.play(Write(lawf), run_time=1.2)
        g = dot([X(6.58), 1.9 + OFF, 0], YELLOW, 0.22)
        gl = VGroup(T("Golgi", 30, TEXT), M("6.58", 30, YELLOW)).arrange(DOWN, buff=0.08).move_to([X(6.58), 2.95 + OFF, 0])
        m = dot([X(7.98), 1.9 + OFF, 0], YELLOW, 0.22)
        ml = VGroup(T("matrix", 30, TEXT), M("7.98", 30, YELLOW)).arrange(DOWN, buff=0.08).move_to([X(7.98), 2.95 + OFF, 0])
        self.at("Take the two")
        self.play(FadeOut(lawf), run_time=0.5)
        self.at("Golgi reads")
        self.play(FadeIn(g, scale=2), FadeIn(gl, shift=DOWN * 0.1), run_time=0.7)
        self.at("matrix is estimated")
        self.play(FadeIn(m, scale=2), FadeIn(ml, shift=DOWN * 0.1), run_time=0.7)

        br = VGroup(Line([X(6.58), 1.1 + OFF, 0], [X(7.98), 1.1 + OFF, 0], color=TEXT, stroke_width=4),
                    Line([X(6.58), 1.0 + OFF, 0], [X(6.58), 1.2 + OFF, 0], color=TEXT, stroke_width=4),
                    Line([X(7.98), 1.0 + OFF, 0], [X(7.98), 1.2 + OFF, 0], color=TEXT, stroke_width=4))
        brl = M("7.98 − 6.58 = 1.40", 32, TEXT).move_to([(X(6.58) + X(7.98)) / 2, 0.55 + OFF, 0])
        self.at("they differ")
        self.play(Create(br), FadeIn(brl, shift=DOWN * 0.1), run_time=0.9)

        eq = M("10^1.40 = 25.1", 48, YELLOW).move_to([0, -0.4 + OFF, 0])
        self.at("to the power")
        self.play(Write(eq), run_time=1.0)

        x0 = -3.6; u = 0.36
        cap = T("relative free proton activity", 24, GREY).move_to([0.8, -1.2, 0])
        bg = Rectangle(width=25.1 * u, height=0.7, stroke_width=0, fill_color=YELLOW, fill_opacity=0.85)
        bg.move_to([x0 + 25.1 * u / 2, -2.0, 0])
        bm = Rectangle(width=u, height=0.7, stroke_width=0, fill_color=YELLOW, fill_opacity=0.85)
        bm.move_to([x0 + u / 2, -3.0, 0])
        lg = T("Golgi", 26, TEXT).move_to([-5.0, -2.0, 0])
        lm = T("matrix", 26, TEXT).move_to([-5.0, -3.0, 0])
        vg = M("25.1", 28, BG, weight=BOLD).move_to(bg)
        vm = M("1", 28, YELLOW).next_to(bm, RIGHT, buff=0.2)
        self.at("So the Golgi has")
        top = Group(axis, ticks, tl, head, g, gl, m, ml, br, brl, eq)
        self.play(top.animate.shift(UP * 1.3), run_time=0.6)
        self.play(FadeIn(cap), FadeIn(lg), FadeIn(lm), run_time=0.4)
        self.play(GrowFromEdge(bg, LEFT), GrowFromEdge(bm, LEFT), FadeIn(vm), run_time=1.2)
        self.play(FadeIn(vg), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Steady(SpokenScene):
    def construct(self):
        L = ValueTracker(0.0)
        H = 4.4
        room = Rectangle(width=5.2, height=H, stroke_color=GREY, stroke_width=9, fill_color=YELLOW, fill_opacity=0.0)
        room.move_to([-2.0, 0, 0])
        room.add_updater(lambda m: m.set_fill(YELLOW, 0.5 * L.get_value()))
        rlabel = T("room", 30, GREY).move_to(room)
        self.play(Create(room), FadeIn(rlabel), run_time=1.0)

        gx = 2.4
        gbox = Rectangle(width=0.8, height=H, stroke_color=GREY, stroke_width=4).move_to([gx, 0, 0])
        gfill = always_redraw(lambda: Rectangle(width=0.8, height=max(0.001, H * L.get_value()), stroke_width=0,
                                                fill_color=YELLOW, fill_opacity=0.85)
                              .move_to([gx, -H / 2 + max(0.001, H * L.get_value()) / 2, 0]))
        sp_y = -H / 2 + H * 0.7
        sp = DashedLine([gx - 0.7, sp_y, 0], [gx + 0.7, sp_y, 0], color=TEXT, stroke_width=4)
        spl = T("set point", 24, TEXT).move_to([gx + 2.1, sp_y, 0])
        glab = T("warmth", 24, GREY).move_to([gx, -2.7, 0])
        self.at("thermostat")
        self.play(FadeIn(gbox), FadeIn(gfill), FadeIn(glab), FadeOut(rlabel), L.animate.set_value(0.7), run_time=0.8)
        self.play(Create(sp), FadeIn(spl), run_time=0.3)

        wall = T("wall", 26, TEXT).move_to([-5.7, 0, 0])
        self.at("The wall")
        self.play(FadeIn(wall), Indicate(room, color=TEXT, scale_factor=1.03), run_time=0.9)

        leaks = VGroup(*[arr([x, -2.25, 0], [x, -2.85, 0], RED, 6) for x in (-3.2, -2.0, -0.8)])
        lk = T("heat loss", 26, RED).move_to([-2.0, -3.2, 0])
        self.at("slows the loss")
        self.play(FadeIn(leaks, shift=DOWN * 0.15), FadeIn(lk), run_time=0.8)

        heater = bchip("heater", BLUE, 26).move_to([-2.0, 2.2, 0])
        harrow = arr([-2.0, 1.85, 0], [-2.0, 0.9, 0], BLUE, 7)
        self.at("so a heater")
        self.play(FadeIn(heater, scale=0.8), GrowArrow(harrow), run_time=0.9)

        self.at("works the same way")
        mem = T("membrane", 26, TEXT).move_to([-5.7, 0, 0])
        lum = T("lumen", 30, TEXT).move_to([-2.0, 0, 0])
        dif = T("difference", 24, GREY).move_to([gx, -2.7, 0])
        self.play(ReplacementTransform(wall, mem), FadeIn(lum), ReplacementTransform(glab, dif), run_time=0.8)
        self.at("pump is the heater")
        pump = bchip("pump", BLUE, 26).move_to([-2.0, 2.2, 0])
        self.play(ReplacementTransform(heater, pump), run_time=0.6)
        self.at("Leak is the lost heat")
        lk2 = T("leak", 26, RED).move_to([-2.0, -3.2, 0])
        self.play(ReplacementTransform(lk, lk2), run_time=0.6)

        ss = T("steady state", 28, GREEN, weight=BOLD).move_to([gx, 2.8, 0])
        self.at("steady state")
        self.play(FadeIn(ss, shift=DOWN * 0.1), Indicate(sp, color=GREEN), run_time=0.9)

        atp = bchip("ATP", GOLD, 24).move_to([-4.0, 2.2, 0])
        self.at("usually in")
        self.play(FadeIn(atp, scale=0.8), run_time=0.5)

        self.at("Stop the pump")
        x = cross([-2.0, 2.2, 0], 0.35)
        self.play(pump[1].animate.set_stroke(GREY).set_fill(GREY, 0.16), pump[2].animate.set_color(GREY),
                  FadeOut(harrow), FadeOut(atp), FadeIn(x), FadeOut(ss), run_time=0.6)
        self.play(L.animate.set_value(0.1), run_time=self.beat(0.1), rate_func=lambda t: 1 - (1 - t) ** 2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Vatpase(SpokenScene):
    def construct(self):
        lumen = RoundedRectangle(corner_radius=0.5, width=6.1, height=5.5, stroke_color=GREY, stroke_width=7,
                                 fill_color=YELLOW, fill_opacity=0.3).move_to([3.05, -0.35, 0])
        cy = T("cytosol", 28, GREY).move_to([-3.4, 2.7, 0])
        ln = T("Golgi lumen, HeLa cells", 26, TEXT).move_to([3.4, 2.1, 0])
        ph = M("pH 6.58", 30, YELLOW).move_to([3.4, -2.6, 0])
        pts = scatter(15, 0.8, 5.5, -2.0, 1.5, 7)
        inside = [dot(p, YELLOW) for p in pts]
        leak = DashedVMobject(Rectangle(width=0.5, height=0.9, color=RED, stroke_width=5), num_dashes=16)
        leakpatch = Rectangle(width=0.5, height=0.9, stroke_width=0, fill_color=BG, fill_opacity=1)
        leak.move_to([0, -1.6, 0]); leakpatch.move_to(leak)
        leakl = T("leak", 24, RED).move_to([-0.9, -2.35, 0])
        self.add(leakpatch)
        self.play(Create(lumen), FadeIn(cy), FadeIn(ln), FadeIn(ph), FadeIn(leak), FadeIn(leakl),
                  LaggedStart(*[FadeIn(d, scale=1.5) for d in inside], lag_ratio=0.03), run_time=1.1)

        pump = RoundedRectangle(corner_radius=0.3, width=1.0, height=1.7, stroke_color=BLUE, stroke_width=5,
                                fill_color=BLUE, fill_opacity=0.5).move_to([0, 0.6, 0])
        pl = btext("V-ATPase", 26, BLUE).move_to([-1.3, 2.0, 0])
        atp = bchip("ATP", GOLD, 24).move_to([-1.8, -0.5, 0])
        self.play(FadeIn(pump, scale=0.8), FadeIn(pl), run_time=0.5)
        self.at("spends")
        self.play(FadeIn(atp, scale=0.8), run_time=0.5)

        def flow(n_in, n_out, rt=1.6):
            anims = []
            newd = []
            for k in range(n_in):
                d = dot([-2.6, 0.2 + 0.25 * k, 0], YELLOW)
                tgt = scatter(1, 0.8, 5.5, -2.0, 1.5, 100 + k + len(inside))[0]
                newd.append((d, path([-2.6, 0.2 + 0.25 * k, 0], [0, 0.4, 0], tgt)))
            for d, p in newd:
                self.add(d)
                anims.append(MoveAlongPath(d, p))
                inside.append(d)
            pool = list(inside[:-n_in] if n_in else inside)
            rng = np.random.default_rng(int(self.elapsed() * 100))
            pick = [pool[i] for i in rng.permutation(len(pool))[:max(n_out, 0) + (3 if n_out < len(pool) - 3 else 0)]]
            outs = sorted(pick, key=lambda d: np.linalg.norm(d.get_center() - np.array([0, -1.6, 0])))[:n_out]
            for d in outs:
                c = d.get_center()
                anims.append(MoveAlongPath(d, path(c, [0, -1.6, 0], [-2.4, -1.6 + (hash(id(d)) % 5 - 2) * 0.12, 0])))
            self.play(*anims, run_time=rt, rate_func=linear)
            for d in outs:
                inside.remove(d)
                self.remove(d)

        self.at("move protons")
        flow(3, 3)
        hold_flow(self, "a drug called", flow)

        bafi = bchip("bafilomycin", RED, 26).move_to([-3.6, 1.0, 0])
        ba = arr([-2.4, 1.0, 0], [-0.6, 0.8, 0], RED, 6)
        self.at("a drug called")
        self.play(FadeIn(bafi, scale=0.8), run_time=0.6)
        self.at("blocks it")
        x = cross([0, 0.6, 0], 0.4)
        self.play(GrowArrow(ba), pump.animate.set_stroke(GREY).set_fill(GREY, 0.3), FadeIn(x), FadeOut(atp), run_time=0.7)
        self.at("less acid")
        newph = VGroup(M("pH rises", 30, YELLOW), T("less acid", 26, YELLOW)).arrange(DOWN, buff=0.1).move_to([3.4, -2.55, 0])
        self.play(FadeOut(ph), FadeIn(newph), lumen.animate.set_fill(YELLOW, 0.1), run_time=0.5)
        flow(0, 6, rt=2.0)
        key = T("actively kept", 30, GREEN, weight=BOLD).move_to([-3.4, -2.7, 0])
        self.at("actively kept")
        self.play(FadeIn(key, shift=UP * 0.1), run_time=0.7)
        self.finish()


class S05Serca(SpokenScene):
    def construct(self):
        lumen = RoundedRectangle(corner_radius=0.5, width=6.1, height=5.5, stroke_color=GREY, stroke_width=7,
                                 fill_color=TEAL, fill_opacity=0.14).move_to([3.05, -0.35, 0])
        cy = T("cytosol", 28, GREY).move_to([-3.4, 2.7, 0])
        ln = T("ER lumen", 28, TEXT).move_to([3.4, 2.1, 0])
        leak = DashedVMobject(Rectangle(width=0.5, height=0.9, color=RED, stroke_width=5), num_dashes=16)
        leakpatch = Rectangle(width=0.5, height=0.9, stroke_width=0, fill_color=BG, fill_opacity=1)
        leak.move_to([0, -1.6, 0]); leakpatch.move_to(leak)
        leakl = T("leak", 24, RED).move_to([-0.9, -2.35, 0])
        pts = scatter(26, 0.8, 5.5, -2.0, 1.5, 11, mind=0.5)
        inside = [dot(p, TEAL) for p in pts]
        outside = [dot([-4.2, 0.2, 0], TEAL), dot([-3.0, -0.2, 0], TEAL)]
        self.add(leakpatch)
        self.play(Create(lumen), FadeIn(cy), FadeIn(ln), FadeIn(leak), FadeIn(leakl), run_time=0.8)

        pump = RoundedRectangle(corner_radius=0.3, width=1.0, height=1.7, stroke_color=BLUE, stroke_width=5,
                                fill_color=BLUE, fill_opacity=0.5).move_to([0, 0.6, 0])
        pl = btext("SERCA", 26, BLUE).move_to([-1.3, 2.0, 0])
        atp = bchip("ATP", GOLD, 24).move_to([-1.8, -0.5, 0])
        cal = T("Calcium", 28, TEAL, weight=BOLD).move_to([-3.4, 2.0, 0])
        self.play(FadeIn(cal), run_time=0.3)
        self.at("The pump")
        self.play(FadeIn(pump, scale=0.8), FadeIn(pl), FadeIn(atp, scale=0.8), run_time=0.7)

        def flow(n_in, n_out, rt=1.6, seedoff=0):
            anims = []; newd = []
            for k in range(n_in):
                d = dot([-2.6, 0.2 + 0.25 * k, 0], TEAL)
                tgt = scatter(1, 0.8, 5.5, -2.0, 1.5, 300 + k + seedoff + int(self.elapsed() * 10))[0]
                newd.append((d, path([-2.6, 0.2 + 0.25 * k, 0], [0, 0.4, 0], tgt)))
            old = list(inside)
            for d, p in newd:
                self.add(d); anims.append(MoveAlongPath(d, p)); inside.append(d)
            rng = np.random.default_rng(int(self.elapsed() * 100))
            pick = [old[i] for i in rng.permutation(len(old))[:n_out + (3 if n_out < len(old) - 3 else 0)]]
            outs = sorted(pick, key=lambda d: np.linalg.norm(d.get_center() - np.array([0, -1.6, 0])))[:n_out]
            for i, d in enumerate(outs):
                c = d.get_center()
                anims.append(MoveAlongPath(d, path(c, [0, -1.6, 0], [-1.9, -2.3 + 0.15 * (i % 3), 0])))
            self.play(*anims, run_time=rt, rate_func=linear)
            for d in outs:
                inside.remove(d); self.remove(d)

        self.at("moves calcium")
        self.play(LaggedStart(*[FadeIn(d, scale=1.5) for d in inside], lag_ratio=0.03), FadeIn(outside[0]), FadeIn(outside[1]), run_time=1.2)
        flow(3, 0)

        cl = VGroup(T("cytosol:", 24, GREY), T("about 100 nM", 26, TEAL)).arrange(DOWN, buff=0.05).move_to([-3.4, -2.55, 0])
        ll = T("about 0.5 to 1 mM free Ca2+", 26, TEAL).move_to([3.4, -2.6, 0])
        hold_flow(self, "lumen holds", flow)
        self.at("lumen holds")
        self.play(FadeIn(ll, shift=UP * 0.1), run_time=0.6)
        hold_flow(self, "cytosol holds", flow)
        self.at("cytosol holds")
        self.play(FadeIn(cl, shift=UP * 0.1), run_time=0.6)
        fold = bchip("5,000- to 10,000-fold", TEXT, 26).move_to([-3.4, -1.35, 0])
        hold_flow(self, "difference", flow)
        self.at("difference")
        self.play(FadeIn(fold, scale=0.85), run_time=0.7)
        hold_flow(self, "with thapsigargin", flow)

        thap = bchip("thapsigargin", RED, 26).move_to([-3.6, 1.0, 0])
        ta = arr([-2.4, 1.0, 0], [-0.6, 0.8, 0], RED, 6)
        self.at("with thapsigargin")
        self.play(FadeIn(thap, scale=0.8), GrowArrow(ta), run_time=0.7)
        x = cross([0, 0.6, 0], 0.4)
        self.play(pump.animate.set_stroke(GREY).set_fill(GREY, 0.3), FadeIn(x), FadeOut(atp), FadeOut(fold), run_time=0.5)
        self.at("calcium leaks out")
        flow(0, 12, rt=2.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        def X(p):
            return -2.3 + (p - 4.0) * 1.6

        rows = [("Lysosome", (4.5, 5.0), "4.5 to 5.0"), ("Late endosome", (5.5, 5.5), "about 5.5"),
                ("Early endosome", (6.3, 6.5), "6.3 to 6.5"), ("Golgi", (6.58, 6.58), "6.58"),
                ("ER lumen", (7.0, 7.0), "near neutral"), ("Matrix", (7.98, 7.98), "7.98 (est.)")]
        ys = [2.9, 1.95, 1.0, 0.05, -0.9, -1.85]
        axis = Line([X(4.0) - 0.2, -2.5, 0], [X(8.2), -2.5, 0], color=GREY, stroke_width=4)
        tks = VGroup(); tls = VGroup()
        for p in range(4, 9):
            tks.add(Line([X(p), -2.6, 0], [X(p), -2.4, 0], color=GREY, stroke_width=4))
            tls.add(M(str(p), 24, GREY).move_to([X(p), -2.9, 0]))
        axl = T("pH", 24, GREY).move_to([X(8.2) + 0.5, -2.5, 0])
        self.play(Create(axis), FadeIn(tks), FadeIn(tls), FadeIn(axl), run_time=0.6)

        def row(i):
            name, (a, b), val = rows[i]
            y = ys[i]
            lab = T(name, 26, TEXT)
            lab.move_to([-4.5, y, 0]); lab.align_to([-6.25, 0, 0], LEFT)
            if a == b:
                mk = dot([X(a), y, 0], YELLOW, 0.17)
            else:
                mk = RoundedRectangle(corner_radius=0.14, width=X(b) - X(a), height=0.34, stroke_width=0,
                                      fill_color=YELLOW, fill_opacity=0.95).move_to([(X(a) + X(b)) / 2, y, 0])
            v = M(val, 24, YELLOW).next_to(mk, RIGHT, buff=0.25)
            return VGroup(lab, mk, v)

        R = [row(i) for i in range(6)]
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in R[:4]], lag_ratio=0.35), run_time=1.5)
        self.at("near neutral")
        self.play(FadeIn(R[4], shift=RIGHT * 0.2), run_time=0.7)
        self.at("alkaline")
        self.play(FadeIn(R[5], shift=RIGHT * 0.2), run_time=0.7)

        self.at("its own value")
        self.play(LaggedStart(*[Indicate(r[1], color=YELLOW, scale_factor=1.5) for r in R], lag_ratio=0.2), run_time=2.0)
        t1 = T("a steady state between pumping and leak", 30, GREEN, weight=BOLD).move_to([0, -3.4, 0])
        self.at("steady state")
        self.play(FadeIn(t1, shift=UP * 0.1), run_time=0.8)
        self.at("not set once")
        self.play(Indicate(t1, color=GREEN, scale_factor=1.08), run_time=1.0)
        t2 = T("lasts only while a pump keeps paying", 30, TEXT, weight=BOLD).move_to([0, -3.4, 0])
        self.at("only while")
        self.play(ReplacementTransform(t1, t2), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "A luminal difference lasts only while a pump keeps paying."
