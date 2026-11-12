"""The Receptor That Does Not Come Back (endocytosis, chapter 2).

Same world and colour map as chapter 1 (../scenes.py). New colours for this chapter:
  SKY     growth-factor receptor            LIME   ubiquitin tag
  CORAL   ESCRT                             CYAN   PCSK9
  white   signal dot / questions / tags
"""
import importlib.util
from pathlib import Path

from bp_style import *  # noqa: F401,F403
import numpy as np

_spec = importlib.util.spec_from_file_location("ch1_scenes", Path(__file__).resolve().parent.parent / "scenes.py")
ch1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ch1)

world_base, label, ldl_dot, curved_arrow, pathway_traces = (
    ch1.world_base, ch1.label, ch1.ldl_dot, ch1.curved_arrow, ch1.pathway_traces)
MEM_Y, ENDO_C, ENDO_R, LYSO_C, LYSO_R = ch1.MEM_Y, ch1.ENDO_C, ch1.ENDO_R, ch1.LYSO_C, ch1.LYSO_R
NAVY, WARM, ROSE, PI, LDL = ch1.NAVY, ch1.WARM, ch1.ROSE, ch1.PI, ch1.LDL

SKY = "#5AA9F0"
LIME = "#9BE04A"
CORAL = "#FF7F6B"
CYAN = "#8AF3FF"
WHITE = "#FFFFFF"

TA = (100, 50, 150)            # rim angles of the three tagged receptors
PLAIN_ANG = (205, 240, 275, 310, 345)   # where plain buds form
GREY_ANG = 180
MERGE = np.array([3.15, -0.97, 0.0])    # endosome centre (-1.75,-.65) -> (1.4,-1.62), touching the lysosome
MCENTER = np.array([2.4, -1.6, 0.0])    # centre of the fused multivesicular body + lysosome
MR = 1.95


def P3(p):
    return np.array([p[0], p[1], 0.0])


def jig(m, amp=0.035, f=2.2, ph=0.0):
    st = {"t": ph}

    def u(mm, dt):
        a = amp * np.array([np.sin(f * st["t"]), np.cos(1.3 * f * st["t"]), 0])
        st["t"] += dt
        b = amp * np.array([np.sin(f * st["t"]), np.cos(1.3 * f * st["t"]), 0])
        mm.shift(b - a)
    m.add_updater(u)
    return m


def rec(color=SKY, s=0.8, chip=False):
    stem = RoundedRectangle(corner_radius=0.07, width=0.22, height=0.86, stroke_color=color,
                            stroke_width=3, fill_color=color, fill_opacity=0.78)
    tail = Line([0, -0.42, 0], [0.15, -0.68, 0], color=color, stroke_width=4)
    parts = [stem, tail]
    if chip:
        parts.append(Square(0.22, stroke_width=0, fill_color=LIME, fill_opacity=1).move_to([0.21, -0.82, 0]))
    return VGroup(*parts).scale(s, about_point=ORIGIN)


def put(m, p, ang=0.0):
    m.rotate(ang, about_point=ORIGIN)
    m.shift(P3(p))
    return m


def nrm(deg):
    a = np.radians(deg)
    return np.array([np.cos(a), np.sin(a), 0.0])


def rim_rec(deg, color=SKY, s=1.0, chip=False, c=ENDO_C, R=ENDO_R, inward=False):
    a = np.radians(deg)
    ang = a - PI / 2 if inward else a + PI / 2
    return put(rec(color, s, chip), c + nrm(deg) * R, ang)


def surf_rec(x, color=SKY, s=0.95, chip=False):
    return put(rec(color, s, chip), [x, MEM_Y, 0])


def vesicle(c, r=0.19, inside=WARM):
    return Circle(radius=r, stroke_color=GREY, stroke_width=4, fill_color=inside, fill_opacity=1).move_to(P3(c))


REC_POS = ((0.0, 0.42), (0.5, 0.2), (-0.5, 0.2))


def ves_rec(i):
    """Inner vesicle i (cytosol inside) carrying a tagged sky receptor: ectodomain out, tail inside."""
    c = ENDO_C + P3(REC_POS[i])
    b = np.arctan2(REC_POS[i][1], REC_POS[i][0])
    v = vesicle(c)
    r = put(rec(SKY, 0.48, True), c + np.array([np.cos(b), np.sin(b), 0]) * 0.19, b - PI / 2)
    return v, r


def plain_pos(i):
    return ENDO_C + nrm(PLAIN_ANG[i]) * 0.72


def enz(center, rmin, rmax, n=5, seed=0, speed=0.35, orbit=True):
    rng = np.random.RandomState(seed)
    c = P3(center)
    g = VGroup()
    for _ in range(n):
        x = VGroup(Rectangle(width=0.26, height=0.06, stroke_width=0, fill_color=RED, fill_opacity=1).rotate(0.6),
                   Rectangle(width=0.26, height=0.06, stroke_width=0, fill_color=RED, fill_opacity=1).rotate(-0.6))
        r = rng.uniform(rmin, rmax)
        a = rng.uniform(0, 2 * PI)
        x.move_to(c + np.array([r * np.cos(a), r * np.sin(a), 0]))
        if orbit:
            w = speed * rng.choice([-1, 1]) * rng.uniform(0.6, 1.2)
            x.add_updater(lambda m, dt, w=w, c=c: m.rotate(w * dt, about_point=c))
        g.add(x)
    return g


def coral(p):
    blocks = VGroup(*[Square(0.2, stroke_width=0, fill_color=CORAL, fill_opacity=1) for _ in range(3)])
    blocks.arrange(RIGHT, buff=0.05)
    return blocks.move_to(P3(p))


class St:
    pass


def state(scene, tagged=(), plain=0, recves=0, grey=False, lyso=True, ambient=True):
    st = St()
    st.w = world_base(scene, ambient=ambient)
    if ambient:
        drifters(scene, st.w)
    st.lyso_enz = enz(LYSO_C, 0.15, 0.5, 5, seed=3) if lyso else VGroup()
    scene.add(st.lyso_enz)
    st.rim = {d: jig(rim_rec(d, SKY, 1.0, True), ph=d / 40) for d in tagged}
    scene.add(*st.rim.values())
    st.plain = []
    for i in range(plain):
        v = jig(vesicle(plain_pos(i)), amp=0.02, ph=i)
        st.plain.append(v)
        scene.add(v)
    st.recves = []
    for i in range(recves):
        v, r = ves_rec(i)
        g = jig(VGroup(v, r), amp=0.02, ph=i + 2)
        st.recves.append(g)
        scene.add(g)
    st.grey = None
    if grey:
        st.grey = jig(rim_rec(GREY_ANG, GREY, 1.0, False), ph=1.0)
        scene.add(st.grey)
    return st


def mvb_group(st):
    return VGroup(st.w["endo"], *st.rim.values(), *st.plain, *st.recves, *([st.grey] if st.grey else []))


def pore():
    return Ellipse(width=0.34, height=0.95, stroke_width=0, fill_color=NAVY, fill_opacity=1).move_to(
        [ENDO_C[0] + MERGE[0] + ENDO_R - 0.1, LYSO_C[1] - 0.0, 0]).set_z_index(3)


def merged_circle():
    return Circle(radius=MR, stroke_color=RED, stroke_width=7, fill_color=NAVY, fill_opacity=1).move_to(MCENTER)


def drifters(scene, w):
    """Faster gold LDL drifting in the outside band (below any top label)."""
    scene.remove(w["drifters"])
    g = VGroup()
    for i, (x, y) in enumerate([(-6.0, 2.62), (-3.7, 2.95), (-0.9, 2.72), (2.2, 3.02), (5.0, 2.7)]):
        d = ldl_dot([x, y, 0], 0.13 + 0.015 * (i % 2)).set_opacity(0.75)
        sp = 0.38 + 0.04 * i
        d.add_updater(lambda m, dt, sp=sp: (m.shift(RIGHT * sp * dt), m.shift(LEFT * 13.6) if m.get_x() > 6.85 else None))
        g.add(d)
    scene.add(g)
    w["drifters"] = g
    return g


def tag(text, x=4.9, y=-3.4, size=28):
    return label(text, size, WHITE).move_to([x, y, 0])


# ---------------------------------------------------------------- scenes

class S00Hook(SpokenScene, TitleCard):
    TITLE = "The Receptor That Does Not Come Back"
    LESSON = "Endocytosis"

    def construct(self):
        w = world_base(self)
        drifters(self, w)
        r = jig(rim_rec(15, SKY, 0.95, False))
        r.set_opacity(0.0)
        self.add(r)
        start, end = P3(ENDO_C + nrm(15) * (ENDO_R + 0.9)), P3(LYSO_C + np.array([-LYSO_R - 0.08, 0.05, 0]))
        arrow = DashedLine(start, end, color=WHITE, stroke_width=6, dash_length=0.2).add_tip(tip_length=0.28)
        q = T("?", 60, WHITE).move_to([1.7, -0.6, 0])
        runner = Dot(start, radius=0.09, color=WHITE)
        runner.add_updater(lambda m, dt, st={"t": 0.0}: (st.__setitem__("t", st["t"] + dt),
                                                          m.move_to(start + (end - start) * ((st["t"] * 0.35) % 1.0))))
        self.play(r.animate.set_opacity(1.0), run_time=0.4)
        self.play(r.animate.scale(1.3), rate_func=there_and_back, run_time=0.5)
        self.at("destroy")
        top = label("Destroy the receptor itself. How?", 34, WHITE).move_to([0, 3.5, 0])
        self.play(FadeIn(top), run_time=0.8)
        self.at("without leaving")
        self.play(Create(arrow), run_time=0.9)
        self.play(FadeIn(q), FadeIn(runner), run_time=0.5)
        self.at("chapter 1")
        teal, gold = pathway_traces()
        for m in (teal, gold):
            m[0].set_stroke(opacity=0.4)
            m[1].set_fill(opacity=0.4)
        tg = tag("chapter 1", 5.6, -3.35)
        self.play(Create(teal), Create(gold), FadeIn(tg), run_time=1.3)
        self.at("escaped")
        tr = rec(TEAL, 0.6)
        path = VMobject(color=TEAL).set_points_smoothly([P3(p) for p in [(-1.3, 0.45), (-0.6, 1.2), (0.3, 2.0)]])
        put(tr, path.get_start(), 0.9)
        tubule = path.copy().set_stroke(TEAL, 5, 0.7)
        self.add(tubule, tr)
        self.play(MoveAlongPath(tr, path), run_time=3.0, rate_func=smooth)
        self.at("acid")
        acid = Circle(radius=ENDO_R, stroke_width=0, fill_color=ROSE, fill_opacity=0.28).move_to(ENDO_C)
        self.play(FadeIn(acid), run_time=0.8)
        self.at("meant to be destroyed")
        self.play(FadeOut(teal), FadeOut(gold), FadeOut(tg), FadeOut(tr), FadeOut(tubule), FadeOut(acid), run_time=0.9)
        self.play(r.animate.scale(1.35), q.animate.scale(1.3), rate_func=there_and_back, run_time=1.0)
        self.finish()


class S01Title(TitleCard):
    TITLE = "The Receptor That Does Not Come Back"
    LESSON = "Endocytosis"


class S02Tagged(SpokenScene):
    def construct(self):
        w = world_base(self)
        drifters(self, w)
        x0 = 0.2
        sr = jig(surf_rec(x0, SKY, 0.95, False))
        self.add(sr)
        sig = Dot([x0 + 3.0, 3.3, 0], radius=0.13, color=WHITE)
        self.add(sig)
        self.at("activated")
        self.play(sig.animate.move_to([x0, MEM_Y + 0.62, 0]), run_time=1.2)
        self.play(Flash(sig, color=WHITE, flash_radius=0.4, line_length=0.15), run_time=0.6)
        self.at("shown here in sky blue")
        gl = label("growth-factor receptor", 30, SKY).move_to([-2.9, 1.45, 0])
        self.play(FadeIn(gl), Indicate(sr, color=SKY, scale_factor=1.2), run_time=1.0)
        self.at("ubiquitin")
        tagged = surf_rec(x0, SKY, 0.95, True)
        chip = tagged[2].copy().shift(np.array([1.6, -0.9, 0]))
        self.add(chip)
        self.play(chip.animate.move_to(tagged[2].get_center()), run_time=0.8)
        self.remove(chip)
        jig(tagged)
        self.add(tagged)
        self.remove(sr)
        sr = tagged
        ul = label("ubiquitin tag", 30, LIME).move_to([2.7, 1.3, 0])
        self.play(FadeIn(ul), Flash(sr[2].get_center(), color=LIME, flash_radius=0.35), run_time=0.8)
        self.at("tagged receptors enter")
        vc = np.array([x0, 1.45, 0])
        ves = Circle(radius=0.5, stroke_color=GREY, stroke_width=5, fill_color=NAVY, fill_opacity=1).move_to(vc)
        r2 = put(rec(SKY, 0.55, True), vc + nrm(200) * 0.5, np.radians(200) + PI / 2)
        vg = VGroup(ves, r2)
        self.play(FadeOut(ul), FadeOut(gl), FadeOut(sig), FadeIn(ves), ReplacementTransform(sr, r2), run_time=0.5)
        tgt = ENDO_C + nrm(TA[0]) * (ENDO_R + 0.5)
        self.play(vg.animate.move_to(tgt), run_time=0.9)
        self.at("early endosome")
        final = [rim_rec(d, SKY, 1.0, True) for d in TA]
        self.play(FadeOut(ves), ReplacementTransform(r2, final[0]),
                  FadeIn(final[1]), FadeIn(final[2]), run_time=0.9)
        for f in final:
            jig(f, ph=1.0)
        gl2 = label("growth-factor receptor", 30, SKY).move_to([-1.75, -2.55, 0])
        self.play(FadeIn(gl2), run_time=0.9)
        self.at("Ubiquitin helps")
        self.play(*[Indicate(f[2], color=LIME, scale_factor=1.8) for f in final], run_time=1.0)
        self.at("lysosomal")
        self.play(*[Indicate(f[2], color=LIME, scale_factor=1.8) for f in final], run_time=1.0)
        self.finish()


def s03_final(scene, animate=False):
    """Endosome fused (schematic) to the lysosome, enzymes at the lumen end, dimmed world, question card."""
    st = state(scene, tagged=TA, lyso=False)
    mvb_group(st).shift(MERGE)
    po = pore()
    shade = Rectangle(width=14.4, height=8.2, stroke_width=0, fill_color=BG, fill_opacity=0.5).set_z_index(2)
    mvb_group(st).set_z_index(3)
    tg = tag("schematic, suppose", 4.7, -3.35).set_z_index(5)
    q = T("Can enzymes reach every part?", 36, WHITE).move_to([0, 3.35, 0]).set_z_index(5)
    a = st.rim[TA[0]]
    tip = a.get_center() - nrm(TA[0]) * 0.30
    tg_pts = [tip + np.array(o) for o in [(-0.15, -0.15, 0), (0.25, -0.2, 0), (-0.45, -0.45, 0), (0.1, -0.5, 0), (0.45, -0.1, 0)]]
    es = enz(LYSO_C, 0.2, 0.3, 5, seed=5, orbit=False)
    for e, p in zip(es, tg_pts):
        e.move_to(p)
        jig(e, amp=0.03, ph=p[0])
    es.set_z_index(4)
    po.set_z_index(3)
    scene.add(po, shade, tg, q, es)
    return st, po, shade, tg, q, es


class S03Problem(SpokenScene):
    def construct(self):
        st = state(self, tagged=TA, lyso=False)
        A = st.rim[TA[0]]
        self.at("The receptor sits")
        ring = Circle(radius=0.6, stroke_color=WHITE, stroke_width=4).move_to(A)
        self.play(Create(ring), run_time=0.9)
        self.at("its tail")
        tail_pt = A[1].get_end() + nrm(TA[0]) * 0.12
        tr = Circle(radius=0.28, stroke_color=LIME, stroke_width=5).move_to(A[2].get_center())
        cl = label("cytosol", 28, WHITE).move_to([0.45, 0.95, 0])
        self.play(Create(tr), FadeIn(cl), run_time=0.9)
        self.play(Indicate(A[2], color=LIME, scale_factor=1.8), run_time=0.9)
        self.at("Suppose")
        self.play(FadeOut(ring), FadeOut(tr), FadeOut(cl), FadeOut(st.w["drifters"]), run_time=0.4)
        tg = tag("schematic, suppose", 4.7, -3.35)
        self.play(FadeIn(tg), mvb_group(st).animate.shift(MERGE), run_time=1.3)
        self.at("fused with a lysosome")
        po = pore()
        self.play(GrowFromCenter(po), run_time=0.7)
        es = enz(LYSO_C, 0.2, 0.3, 5, seed=5, orbit=False)
        tip = A.get_center() - nrm(TA[0]) * 0.30
        tg_pts = [tip + np.array(o) for o in [(-0.15, -0.15, 0), (0.25, -0.2, 0), (-0.45, -0.45, 0), (0.1, -0.5, 0), (0.45, -0.1, 0)]]
        self.play(FadeIn(es), *[e.animate.move_to(p) for e, p in zip(es, tg_pts)], run_time=1.6)
        for e, p in zip(es, tg_pts):
            jig(e, amp=0.03, ph=p[0])
        self.at("Could the enzymes")
        shade = Rectangle(width=14.4, height=8.2, stroke_width=0, fill_color=BG, fill_opacity=0.5).set_z_index(2)
        mvb_group(st).set_z_index(3)
        po.set_z_index(3)
        es.set_z_index(4)
        tg.set_z_index(5)
        q = T("Can enzymes reach every part?", 36, WHITE).move_to([0, 3.35, 0]).set_z_index(5)
        self.play(FadeIn(shade), FadeIn(q), run_time=1.0)
        self.at("whole receptor")
        self.play(Indicate(A, color=SKY, scale_factor=1.4), run_time=1.0)
        self.finish()


class S04Pause(Scene):
    def construct(self):
        s03_final(self)
        self.wait(4.5)


class S05Answer(SpokenScene):
    def construct(self):
        st, po, shade, tg, q, es = s03_final(self)
        A = st.rim[TA[0]]
        self.play(FadeOut(shade), FadeOut(q), run_time=0.8)
        self.play(FadeOut(po), FadeOut(tg), FadeOut(es), mvb_group(st).animate.shift(-MERGE), run_time=1.2)
        for m in mvb_group(st):
            m.set_z_index(0)
        lyso_e = enz(LYSO_C, 0.15, 0.5, 5, seed=3)
        self.play(FadeIn(lyso_e), run_time=0.4)
        self.at("only the part facing")
        ring = Circle(radius=0.3, stroke_color=RED, stroke_width=6).move_to(A.get_center() - nrm(TA[0]) * 0.28)
        self.play(Create(ring), run_time=0.8)
        self.at("within their reach")
        ol = label("out of reach", 28, WHITE).move_to([0.55, 0.62, 0])
        self.play(FadeIn(ol), run_time=0.7)
        self.at("moving the receptor")
        arrow = Arrow(A.get_center() - nrm(TA[0]) * 0.35, ENDO_C + np.array([0.0, 0.0, 0]), color=WHITE,
                      stroke_width=7, buff=0.0, max_tip_length_to_length_ratio=0.3)
        self.play(FadeOut(ring), FadeOut(ol), Create(arrow), run_time=1.0)
        self.at("off that outer membrane")
        self.play(Indicate(A, color=SKY, scale_factor=1.3), run_time=1.0)
        self.finish()


def s05_state(scene):
    st = state(scene, tagged=TA)
    A = st.rim[TA[0]]
    arrow = Arrow(A.get_center() - nrm(TA[0]) * 0.35, ENDO_C, color=WHITE, stroke_width=7, buff=0.0,
                  max_tip_length_to_length_ratio=0.3)
    scene.add(arrow)
    return st, arrow


class S05bRest(Scene):
    def construct(self):
        st, arrow = s05_state(self)
        self.play(arrow.animate.set_opacity(0.6), run_time=1.0, rate_func=there_and_back)
        self.wait(1.0)


def bud_vesicles(scene, st, idx, t_dimple=0.6, t_deep=1.4, t_in=1.2, start_at=None):
    """Form plain buds idx (indices into PLAIN_ANG): dimple, deepen, pinch off. Returns the vesicles."""
    out = []
    for i in idx:
        n = nrm(PLAIN_ANG[i])
        v = vesicle(ENDO_C + n * ENDO_R).scale(0.55)
        out.append((v, n, i))
    scene.play(*[FadeIn(v) for v, n, i in out], run_time=t_dimple)
    scene.play(*[v.animate.scale(1 / 0.55).shift(-n * 0.18) for v, n, i in out], run_time=t_deep)
    return out


def pinch(scene, out, st, run_time=1.2):
    scene.play(*[v.animate.move_to(plain_pos(i)) for v, n, i in out], run_time=run_time)
    for v, n, i in out:
        jig(v, amp=0.02, ph=i)
        st.plain.append(v)


class S06Bud(SpokenScene):
    def construct(self):
        st = state(self, tagged=TA)
        self.at("patches of its outer")
        arcs = VGroup(*[Arc(radius=ENDO_R, start_angle=np.radians(PLAIN_ANG[i] - 9), angle=np.radians(18),
                            stroke_width=12, color=WHITE).move_arc_center_to(ENDO_C) for i in range(3)])
        self.play(LaggedStart(*[Create(a) for a in arcs], lag_ratio=0.5), run_time=1.6)
        self.at("the limiting membrane")
        lm = label("limiting membrane", 28, WHITE).move_to([-4.85, -0.95, 0])
        self.play(FadeIn(lm), run_time=0.7)
        self.at("bud inward")
        out = bud_vesicles(self, st, [0, 1, 2])
        self.play(FadeOut(arcs), run_time=0.3)
        self.at("pinches off")
        pinch(self, out, st, 1.4)
        self.at("small vesicle inside")
        self.play(*[v.animate.scale(1.5) for v, n, i in out], rate_func=there_and_back, run_time=1.0)
        self.at("An endosome full")
        out2 = bud_vesicles(self, st, [3, 4], 0.5, 0.8)
        pinch(self, out2, st, 0.8)
        self.at("multivesicular body")
        mv = label("multivesicular body", 30, WHITE).move_to([-4.85, 1.3, 0])
        self.play(ReplacementTransform(lm, mv), run_time=0.9)
        self.finish()


class S07Escrt(SpokenScene):
    def construct(self):
        st = state(self, tagged=TA, plain=5)
        q = T("?", 60, WHITE).move_to([0.6, 1.0, 0])
        self.play(FadeIn(q), run_time=0.5)
        self.play(*[Indicate(st.rim[d][2], color=LIME, scale_factor=1.8) for d in TA], run_time=1.2)
        self.at("Complexes called ESCRT")
        clusters = {}
        for d in TA:
            chip_p = st.rim[d][2].get_center()
            clusters[d] = coral(chip_p + nrm(d) * 0.8)
        self.play(FadeOut(q), *[FadeIn(c) for c in clusters.values()], run_time=1.0)
        self.at("in coral")
        el = label("ESCRT", 30, CORAL).move_to([1.7, 0.45, 0])
        self.play(FadeIn(el), Indicate(clusters[TA[1]], color=CORAL, scale_factor=1.4), run_time=1.0)
        self.at("recognize the ubiquitin tag")
        self.play(*[clusters[d].animate.move_to(st.rim[d][2].get_center() + nrm(d) * 0.28) for d in TA], run_time=1.2)
        self.play(*[Indicate(st.rim[d][2], color=LIME, scale_factor=1.8) for d in TA], run_time=0.9)
        self.at("They sort")
        for k, d in enumerate(TA):
            i = TA.index(d)
            v, r2 = ves_rec(i)
            v0 = vesicle(ENDO_C + nrm(d) * ENDO_R).scale(0.5)
            self.play(FadeIn(v0), run_time=0.4)
            vg = VGroup(v, r2)
            self.play(ReplacementTransform(v0, v), ReplacementTransform(st.rim[d], r2),
                      clusters[d].animate.shift(nrm(d) * 0.7).set_opacity(0.0), run_time=0.9)
            jig(vg, amp=0.02, ph=i)
            self.remove(clusters[d])
            st.recves.append(vg)
            if k < 2:
                self.wait(0.15)
        self.at("In this comparison")
        gr = jig(rim_rec(GREY_ANG, GREY, 1.0, False), ph=1.0)
        gr.set_opacity(0.0)
        self.add(gr)
        self.play(gr.animate.set_opacity(1.0), run_time=0.5)
        self.at("untagged")
        c4 = coral(gr.get_center() + nrm(GREY_ANG) * 1.25)
        ul = label("untagged", 28, WHITE).move_to([-4.85, -0.3, 0])
        self.play(FadeIn(c4), FadeIn(ul), c4.animate.shift(-nrm(GREY_ANG) * 0.55), run_time=1.0)
        self.at("stays behind")
        self.play(c4.animate.shift(nrm(GREY_ANG) * 1.0).set_opacity(0.0), gr.animate.scale(1.2),
                  run_time=1.2)
        self.finish()


class S07bRest(Scene):
    def construct(self):
        st = state(self, plain=5, recves=3, grey=True)
        cs = VGroup(*[coral(ENDO_C + nrm(d) * 1.9) for d in (30, 120, 250)])
        self.add(cs)
        self.play(cs.animate.shift(RIGHT * 0.5 + UP * 0.2).set_opacity(0.0), run_time=2.0, rate_func=linear)


class S08Digest(SpokenScene):
    def construct(self):
        st = state(self, plain=5, recves=3, grey=True)
        self.at("multivesicular body then")
        mv = mvb_group(st)
        self.play(mv.animate.shift(MERGE), run_time=1.7)
        self.at("fuses with a lysosome")
        po = pore().set_z_index(3)
        self.play(GrowFromCenter(po), run_time=0.7)
        mc = merged_circle()
        mc.set_z_index(-1)
        self.add(mc)
        grey_new = rim_rec(180, GREY, 1.0, False, c=MCENTER, R=MR)
        self.play(FadeOut(st.w["endo"]), FadeOut(st.w["lyso"]), FadeOut(po), ReplacementTransform(st.grey, grey_new),
                  run_time=1.1)
        mc.set_z_index(0)
        # the merged lumen needs a visible fill behind the vesicles
        self.remove(mc)
        self.add(mc)
        for m in list(st.plain) + list(st.recves):
            self.bring_to_front(m)
        sw = enz(MCENTER, 0.5, 1.35, 6, seed=9, speed=0.3)
        self.at("Each")
        self.play(FadeIn(sw), run_time=0.8)
        self.at("floats whole")
        self.play(*[Indicate(g, color=WHITE, scale_factor=1.25) for g in st.recves], run_time=1.0)
        self.at("receptor and all")
        self.play(*[Indicate(g[1], color=SKY, scale_factor=1.6) for g in st.recves], run_time=0.9)
        self.at("enzymes digest")
        dl = label("digested", 30, SKY).move_to([2.4, 0.78, 0])
        rng = np.random.RandomState(4)
        frags = VGroup()
        for g in list(st.recves) + list(st.plain):
            c0 = g.get_center()
            for k in range(5):
                col = SKY if (g in st.recves and k < 3) else GREY
                frags.add(Dot(c0, radius=0.045, color=col))
        self.play(*[FadeOut(g) for g in list(st.recves) + list(st.plain)], FadeIn(frags), FadeIn(dl), run_time=0.6)
        self.play(*[f.animate.shift(np.array([rng.uniform(-0.45, 0.45), rng.uniform(-0.4, 0.4), 0])) for f in frags],
                  run_time=1.6)
        self.play(mc.animate.set_stroke(width=16), rate_func=there_and_back, run_time=0.9)
        self.at("switched off")
        sg = Dot(MCENTER + np.array([-0.6, -0.2, 0]), radius=0.13, color=WHITE)
        sr = Circle(radius=0.15, stroke_color=WHITE, stroke_width=4).move_to(sg)
        stag = tag("schematic", 5.7, -3.4)
        self.play(FadeIn(sg), FadeIn(stag), run_time=0.4)
        self.play(sr.animate.scale(4).set_opacity(0.0), sg.animate.set_opacity(0.0), run_time=1.0)
        self.finish()


def merged_scene(scene):
    w = world_base(scene, ambient=True)
    scene.remove(w["endo"], w["lyso"])
    mc = merged_circle()
    grey_new = rim_rec(180, GREY, 1.0, False, c=MCENTER, R=MR)
    sw = enz(MCENTER, 0.5, 1.35, 6, seed=9, speed=0.3)
    lyso_e = enz(LYSO_C, 0.15, 0.5, 5, seed=3)
    scene.add(mc, grey_new, sw)
    return w, mc, grey_new, sw


class S08bRest(Scene):
    def construct(self):
        w, mc, grey, sw = merged_scene(self)
        rng = np.random.RandomState(7)
        frags = VGroup(*[Dot(MCENTER + np.array([rng.uniform(-1, 1), rng.uniform(-0.8, 0.8), 0]), radius=0.05,
                             color=SKY if k % 2 else GREY) for k in range(26)])
        self.add(frags)
        self.play(frags.animate.shift(RIGHT * 0.3).set_opacity(0.0), run_time=2.0, rate_func=linear)


def rule_objs():
    teal = pathway_traces()[0]
    sky = curved_arrow([[-2.55, 0.2, 0], [-2.05, -0.35, 0], [-1.3, -1.4, 0], [0.4, -2.0, 0], [2.52, -1.7, 0]], SKY)
    vs = vesicle([-2.05, -0.35], r=0.2)
    return teal, sky, vs


class S09Rule(SpokenScene):
    def construct(self):
        w, mc, grey, sw = merged_scene(self)
        endo, lyso = w["endo"], w["lyso"]
        lyso_e = enz(LYSO_C, 0.15, 0.5, 5, seed=3)
        self.play(FadeOut(mc), FadeOut(grey), FadeOut(sw), FadeIn(endo), FadeIn(lyso), FadeIn(lyso_e), run_time=1.1)
        self.at("sorts more than cargo")
        ring = Circle(radius=ENDO_R + 0.14, stroke_color=WHITE, stroke_width=5).move_to(ENDO_C)
        self.play(Create(ring), run_time=0.9)
        self.play(FadeOut(ring), run_time=0.6)
        self.at("A receptor left in")
        teal, sky, vs = rule_objs()
        rl = label("return", 30, TEAL).move_to([2.3, 1.2, 0])
        self.play(Create(teal), FadeIn(rl), run_time=1.5)
        dot = Dot(teal[0].get_start(), radius=0.1, color=TEAL)
        self.play(MoveAlongPath(dot, teal[0]), run_time=1.6, rate_func=linear)
        self.play(FadeOut(dot), run_time=0.2)
        self.at("ubiquitin tag can select")
        chip = Square(0.18, stroke_width=0, fill_color=LIME, fill_opacity=1).move_to(sky[0].get_start())
        part = sky[0].copy()
        part.pointwise_become_partial(sky[0], 0, 0.3)
        self.play(Create(sky), run_time=2.2)
        self.at("inward budding")
        self.add(chip)
        self.play(FadeIn(vs), MoveAlongPath(chip, part), run_time=1.2)
        self.play(FadeOut(chip), run_time=0.3)
        tl = label("tagged: inward, then digested", 30, SKY).move_to([-0.9, -3.05, 0])
        self.play(FadeIn(tl), run_time=0.7)
        self.at("lysosome can then")
        ring2 = Circle(radius=ENDO_R + 0.14, stroke_color=WHITE, stroke_width=5).move_to(ENDO_C)
        pulse = Circle(radius=ENDO_R, stroke_width=0, fill_color=ROSE, fill_opacity=0.35).move_to(ENDO_C)
        self.play(Create(ring2), FadeIn(pulse), run_time=0.9)
        self.play(Indicate(sky, color=SKY, scale_factor=1.03), Indicate(teal, color=TEAL, scale_factor=1.03),
                  run_time=1.2)
        self.play(FadeOut(pulse), run_time=0.6)
        self.finish()


def rule_state(scene):
    w = world_base(scene, ambient=True)
    scene.add(enz(LYSO_C, 0.15, 0.5, 5, seed=3))
    teal, sky, vs = rule_objs()
    rl = label("return", 30, TEAL).move_to([2.3, 1.2, 0])
    tl = label("tagged: inward, then digested", 30, SKY).move_to([-0.9, -3.05, 0])
    ring = Circle(radius=ENDO_R + 0.14, stroke_color=WHITE, stroke_width=5).move_to(ENDO_C)
    scene.add(teal, sky, vs, rl, tl, ring)
    return w, teal, sky, vs, rl, tl, ring


class S09bRest(Scene):
    def construct(self):
        w, teal, sky, vs, rl, tl, ring = rule_state(self)
        d1 = Dot(teal[0].get_start(), radius=0.1, color=TEAL)
        d2 = Dot(sky[0].get_start(), radius=0.1, color=SKY)
        chip = Square(0.18, stroke_width=0, fill_color=LIME, fill_opacity=1).move_to(sky[0].get_start())
        part = sky[0].copy()
        part.pointwise_become_partial(sky[0], 0, 0.3)
        self.add(d1, d2, chip)
        self.play(MoveAlongPath(d1, teal[0]), MoveAlongPath(d2, sky[0]), MoveAlongPath(chip, part),
                  run_time=2.5, rate_func=linear)


class S10Pcsk9(SpokenScene):
    def construct(self):
        w, teal, sky, vs, rl, tl, ring = rule_state(self)
        self.play(FadeOut(sky), FadeOut(vs), FadeOut(tl), FadeOut(ring), run_time=1.0)
        self.at("pulled out of its loop")
        self.play(FadeOut(teal), FadeOut(rl), run_time=0.8)
        x0 = 0.45
        tr = jig(surf_rec(x0, TEAL, 0.95, False))
        tr.set_opacity(0.0)
        self.add(tr)
        self.play(tr.animate.set_opacity(1.0), run_time=0.9)
        self.at("PCSK9")
        wedge = Polygon([0, -0.26, 0], [-0.2, 0.2, 0], [0.2, 0.2, 0], stroke_width=0, fill_color=CYAN, fill_opacity=1)
        wedge.rotate(-PI / 4).move_to([4.9, 2.95, 0])
        pl = label("PCSK9", 30, CYAN).move_to([3.3, 3.55, 0])
        self.play(FadeIn(wedge), FadeIn(pl), run_time=0.8)
        self.at("protein that cells secrete")
        self.play(wedge.animate.shift(LEFT * 0.4 + DOWN * 0.05), Indicate(wedge, color=CYAN, scale_factor=1.3), run_time=1.2)
        self.at("It binds")
        dock = np.array([0.74, 2.68, 0])
        self.play(wedge.animate.move_to(dock), run_time=0.7)
        self.at("one small part")
        sp = label("one small part", 28, WHITE).move_to([-2.2, 3.15, 0])
        dr = Circle(radius=0.26, stroke_color=WHITE, stroke_width=4).move_to([0.6, 2.6, 0])
        self.play(FadeIn(sp), Create(dr), run_time=0.8)
        self.at("outer region")
        vc = np.array([x0, 1.4, 0])
        ves = Circle(radius=0.55, stroke_color=GREY, stroke_width=5, fill_color=NAVY, fill_opacity=1).move_to(vc)
        r2 = put(rec(TEAL, 0.55, False), vc + nrm(200) * 0.55, np.radians(200) + PI / 2)
        w2 = Polygon([0, -0.2, 0], [-0.15, 0.15, 0], [0.15, 0.15, 0], stroke_width=0, fill_color=CYAN, fill_opacity=1)
        w2.rotate(np.radians(200) + PI / 2).move_to(vc + nrm(200) * 0.2)
        vg = VGroup(ves, r2, w2)
        stg = tag("schematic", 5.7, -3.4)
        self.play(FadeOut(sp), FadeOut(dr), FadeOut(pl), FadeIn(ves), ReplacementTransform(tr, r2),
                  ReplacementTransform(wedge, w2), FadeIn(stg), run_time=0.9)
        self.play(vg.animate.move_to([-0.35, 0.45, 0]), run_time=1.0)
        self.finish()


def lumen_wedge(deg, s=1.0):
    wg = Polygon([0, -0.2, 0], [-0.15, 0.15, 0], [0.15, 0.15, 0], stroke_width=0, fill_color=CYAN, fill_opacity=1)
    wg.scale(s)
    wg.rotate(np.radians(deg) + PI / 2)
    return wg.move_to(ENDO_C + nrm(deg) * (ENDO_R - 0.5))


def oneway_objs():
    teal1 = curved_arrow([[0.25, 2.55, 0], [-0.95, 0.5, 0], [-1.35, -0.8, 0], [0.9, -1.15, 0], [2.5, -1.5, 0]], TEAL)
    gold = curved_arrow([[0.0, 2.75, 0], [-1.0, 0.5, 0], [-1.4, -0.75, 0], [0.7, -1.2, 0], [2.55, -1.55, 0]], LDL)
    return teal1, gold


class S11Detour(SpokenScene):
    def construct(self):
        w = world_base(self)
        drifters(self, w)
        lyso_e = enz(LYSO_C, 0.15, 0.5, 5, seed=3)
        self.add(lyso_e)
        tr = jig(rim_rec(45, TEAL, 1.0, False))
        wg = jig(lumen_wedge(45))
        self.add(tr, wg)
        tg = tag("in cultured human cells tested", 3.85, -3.45)
        self.play(FadeIn(tg), run_time=0.8)
        self.at("A receptor bound this way")
        self.play(tr.animate.scale(1.3), wg.animate.scale(1.3), rate_func=there_and_back, run_time=0.6)
        tub = CubicBezier(P3([-1.1, 0.55]), P3([-0.7, 1.2]), P3([-0.2, 1.4]), P3([0.1, 1.95]))
        tub.set_stroke(TEAL, 6)
        self.play(Create(tub), run_time=0.7)
        empty = Circle(radius=0.14, stroke_color=TEAL, stroke_width=4).move_to(tub.get_end())
        self.play(FadeIn(empty), FadeOut(tub), run_time=0.4)
        self.at("goes to the lysosome")
        self.play(FadeOut(empty), run_time=0.3)
        route = DashedLine(P3(ENDO_C + nrm(0) * (ENDO_R + 0.08) + [0, -0.1, 0]), P3(LYSO_C + [-LYSO_R - 0.08, 0.0, 0]),
                           color=TEAL, stroke_width=6, dash_length=0.18).add_tip(tip_length=0.26)
        token = VGroup(rec(TEAL, 0.5), lumen_wedge(0, 0.6).move_to([0, 0.4, 0])).move_to(tr.get_center())
        self.add(token)
        self.play(FadeOut(tr), FadeOut(wg), Create(route), run_time=0.5)
        sl = label("sorting not shown", 28, WHITE).move_to([1.35, -0.38, 0])
        self.play(FadeIn(sl), token.animate.move_to(route.get_end()), run_time=0.9)
        self.play(FadeOut(token), run_time=0.2)
        self.at("instead of returning")
        dl = label("LDL receptor degraded", 30, TEAL).move_to([3.7, 0.45, 0])
        self.play(FadeIn(dl), run_time=0.8)
        self.at("Its loop has")
        teal = pathway_traces()[0]
        self.play(FadeOut(sl), Create(teal), run_time=1.3)
        self.at("one-way trip")
        teal1, gold = oneway_objs()
        self.play(ReplacementTransform(teal, teal1), Create(gold), run_time=1.6)
        self.at("does not come back")
        self.play(Indicate(teal1, color=TEAL, scale_factor=1.03), Indicate(gold, color=LDL, scale_factor=1.03),
                  run_time=1.2)
        self.finish()


class S11bRest(Scene):
    def construct(self):
        w = world_base(self)
        drifters(self, w)
        self.add(enz(LYSO_C, 0.15, 0.5, 5, seed=3))
        teal1, gold = oneway_objs()
        self.add(teal1, gold)
        d = ldl_dot([-5.0, 2.95, 0], 0.18)
        self.add(d)
        self.play(d.animate.move_to([-1.0, 2.95, 0]), run_time=2.0, rate_func=linear)


class S12Close(SpokenScene):
    def construct(self):
        st = state(self, tagged=(TA[0],))
        # a teal receptor sits at the endosome rim and returns to the surface
        tr = jig(rim_rec(165, TEAL, 1.0, False))
        self.add(tr)
        self.at("destroy a receptor")
        path = VMobject(color=TEAL).set_points_smoothly([P3(p) for p in [(-2.5, 0.2), (-1.6, 1.4), (-0.6, 2.0)]])
        tub = path.copy().set_stroke(TEAL, 5, 0.7)
        self.add(tub)
        self.play(FadeOut(tr), run_time=0.3)
        tok = rec(TEAL, 0.6)
        put(tok, path.get_start(), 0.9)
        self.add(tok)
        self.play(MoveAlongPath(tok, path), run_time=3.2, rate_func=smooth)
        self.play(FadeOut(tub), run_time=0.3)
        tsurf = surf_rec(-0.6, TEAL, 0.95, False)
        self.play(ReplacementTransform(tok, tsurf), run_time=0.4)
        jig(tsurf)
        self.at("ubiquitin tag can select")
        A = st.rim[TA[0]]
        self.play(Indicate(A[2], color=LIME, scale_factor=2.0), Flash(A[2].get_center(), color=LIME, flash_radius=0.35),
                  run_time=1.2)
        c = coral(A[2].get_center() + nrm(TA[0]) * 1.0)
        self.play(FadeIn(c), run_time=0.6)
        self.at("inward budding at")
        self.play(c.animate.move_to(A[2].get_center() + nrm(TA[0]) * 0.28), run_time=0.8)
        v, r2 = ves_rec(0)
        v0 = vesicle(ENDO_C + nrm(TA[0]) * ENDO_R).scale(0.5)
        self.play(FadeIn(v0), run_time=0.4)
        vg = VGroup(v, r2)
        self.play(ReplacementTransform(v0, v), ReplacementTransform(A, r2),
                  c.animate.shift(nrm(TA[0]) * 0.7).set_opacity(0.0), run_time=1.0)
        jig(vg, amp=0.02)
        self.remove(c)
        self.at("puts the whole receptor")
        grp = VGroup(st.w["endo"], vg)
        self.play(grp.animate.shift(MERGE), run_time=0.9)
        po = pore().set_z_index(3)
        mc = merged_circle()
        self.add(mc)
        self.bring_to_front(vg)
        self.play(FadeOut(st.w["endo"]), FadeOut(st.w["lyso"]), FadeOut(st.lyso_enz), FadeIn(mc), run_time=0.5)
        sw = enz(MCENTER, 0.5, 1.35, 6, seed=9, speed=0.3)
        self.add(sw)
        self.bring_to_front(vg)
        self.play(FadeIn(sw), run_time=0.3)
        self.at("within lysosomal enzymes")
        c0 = vg.get_center()
        frags = VGroup(*[Dot(c0, radius=0.05, color=SKY if k < 3 else GREY) for k in range(5)])
        rng = np.random.RandomState(2)
        self.play(FadeOut(vg), FadeIn(frags), run_time=0.5)
        self.play(*[f.animate.shift(np.array([rng.uniform(-0.6, 0.6), rng.uniform(-0.5, 0.5), 0])) for f in frags],
                  run_time=1.3)
        self.play(Indicate(frags, color=SKY, scale_factor=1.5), Indicate(tsurf, color=TEAL, scale_factor=1.3), run_time=1.0)
        self.finish()


class S13End(EndCard):
    LINE = "A cell can destroy a receptor itself by budding it toward lysosomes."
