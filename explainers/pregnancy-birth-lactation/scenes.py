"""Pregnancy, birth and lactation: the lungs take over from the placenta  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = lungs and the pulmonary side (pulmonary resistance, pulmonary flow, pulmonary venous return, ventilate)
  ORANGE = placenta and the umbilical side (umbilical vessels, umbilical venous return, clamp the cord)
  GREEN  = the three fetal shunts (ductus venosus, foramen ovale, ductus arteriosus) and their flow
  YELLOW = pressure (the levels in the two atria in this sketch) and the flap that pressure moves
  RED    = the systemic side: the fetal body bed, systemic vascular resistance and afterload
  TEAL   = oxygen
  GREY   = chambers, structure, notes, assumptions
  GOLD   = question marks (the puzzle) and the title rule
  Every shape is a labelled schematic block; nothing is to scale. Only bars in scenes 1, 4 and 5 carry numbers,
  and they are the lesson's own.
"""
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
LUNG, PLAC, SHUNT, PRESS, SYS, OXY = BLUE, ORANGE, GREEN, YELLOW, RED, TEAL


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=14)


def box(label, color, w, h, size=22, op=0.12, sw=3, tcolor=None):
    r = RoundedRectangle(corner_radius=0.14, width=w, height=h, stroke_color=color, stroke_width=sw,
                         fill_color=color, fill_opacity=op)
    t = T(label, size, tcolor or color, line_spacing=0.9).move_to(r)
    return VGroup(r, t)


def path_arrow(pts, color, w=5, tip=0.22):
    """Polyline with an arrowhead on the last segment."""
    segs = [Line(pts[i], pts[i + 1], color=color, stroke_width=w) for i in range(len(pts) - 2)]
    return VGroup(*segs, arr(pts[-2], pts[-1], color, w, tip))


def P(x, y):
    return np.array([x, y, 0.0])


class S00Title(TitleCard):
    LESSON = "Pregnancy, birth and lactation"
    TITLE = "The lungs take over from the placenta"


# ---------------------------------------------------------------------------------------------
class S01Lungs(SpokenScene):
    """Where the fetal lamb's output goes: bars for placenta and lungs, question marks first."""

    def construct(self):
        X0, K = -0.9, 0.128           # bar start, units per percent
        BAR_H = 0.8
        yP, yL = 1.9, 0.2
        src = box("combined\nventricular\noutput", GREY, 2.4, 1.8, size=24).move_to([-4.9, 1.05, 0])
        self.play(FadeIn(src), run_time=0.3)
        lung_c = chip("Lungs", LUNG, 28).move_to([-2.1, yL, 0])
        plac_c = chip("Placenta", PLAC, 28).move_to([-2.1, yP, 0])
        self.at("does not use")
        self.play(FadeIn(lung_c, shift=RIGHT * 0.2), run_time=0.6)
        a_l = arr(P(-3.7, 0.7), P(lung_c.get_left()[0] - 0.1, yL), GREY, 4)
        a_p = arr(P(-3.7, 1.4), P(plac_c.get_left()[0] - 0.1, yP), GREY, 4)
        q1 = T("?", 70, GOLD, weight=BOLD).move_to([X0 + 1.2, yP, 0])
        q2 = T("?", 70, GOLD, weight=BOLD).move_to([X0 + 1.2, yL, 0])
        self.at("where does its blood go")
        self.play(FadeIn(plac_c, shift=RIGHT * 0.2), GrowArrow(a_l), GrowArrow(a_p), run_time=0.7)
        self.play(FadeIn(q1, scale=0.8), FadeIn(q2, scale=0.8), run_time=0.5)
        lab = T("fetal lambs:\nmicrospheres counted\norgan by organ", 22, GREY, line_spacing=0.9).move_to([-4.6, 2.95, 0])
        self.at("microspheres")
        self.play(FadeIn(lab), run_time=0.6)
        # axis
        yax = -0.9
        axis = Line(P(X0, yax), P(X0 + 50 * K, yax), color=GREY, stroke_width=3)
        ticks = VGroup(*[VGroup(Line(P(X0 + v * K, yax), P(X0 + v * K, yax - 0.12), color=GREY, stroke_width=3),
                                M(str(v), 22, GREY).move_to(P(X0 + v * K, yax - 0.42))) for v in range(0, 51, 10)])
        cap = T("percent of combined ventricular output", 22, GREY).move_to([X0 + 25 * K, yax - 0.95, 0])
        self.play(Create(axis), FadeIn(ticks), FadeIn(cap), run_time=0.8)
        # placenta bar: solid to 40, lighter band 40..45 (the lesson says roughly 40 to 45)
        b40 = Rectangle(width=40 * K, height=BAR_H, stroke_width=0, fill_color=PLAC, fill_opacity=0.9
                        ).move_to(P(X0 + 20 * K, yP))
        b45 = Rectangle(width=5 * K, height=BAR_H, stroke_width=0, fill_color=PLAC, fill_opacity=0.45
                        ).move_to(P(X0 + 42.5 * K, yP))
        tp = T("roughly 40 to 45 percent", 24, PLAC).move_to(P(X0 + 20 * K, yP + 0.72))
        self.at("Roughly")
        self.play(FadeOut(q1), run_time=0.2)
        self.play(GrowFromEdge(b40, LEFT), run_time=1.0)
        self.play(FadeIn(b45), FadeIn(tp), run_time=0.5)
        bl = VGroup(Rectangle(width=8.5 * K, height=BAR_H, stroke_width=0, fill_color=LUNG, fill_opacity=0.9
                              ).move_to(P(X0 + 4.25 * K, yL)),
                    Rectangle(width=1.5 * K, height=BAR_H, stroke_width=0, fill_color=LUNG, fill_opacity=0.35
                              ).move_to(P(X0 + 9.25 * K, yL)))
        tl = T("under 10 percent", 24, LUNG).move_to(P(X0 + 10 * K + 0.3 + 1.45, yL))
        self.at("Under")
        self.play(FadeOut(q2), run_time=0.2)
        self.play(GrowFromEdge(bl, LEFT), run_time=0.6)
        self.play(FadeIn(tl), run_time=0.4)
        n1 = T("Sheep numbers from an instrumented preparation.\nHuman proportions are inferred from imaging.",
               22, GREY, line_spacing=0.9).move_to([0.8, -3.0, 0])
        self.at("numbers from an instrumented")
        self.play(FadeIn(n1, shift=UP * 0.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Shunts(SpokenScene):
    """The fetal layout, built as the three shunts and the two umbilical vessels are named."""

    def construct(self):
        # chambers (body's right on the viewer's left)
        RV = box("right ventricle", GREY, 2.4, 1.4).move_to(P(-1.8, 1.1))
        LV = box("left ventricle", GREY, 2.4, 1.4).move_to(P(1.8, 1.1))
        RA = box("right atrium", GREY, 2.4, 1.2).move_to(P(-1.8, -0.8))
        LA = box("left atrium", GREY, 2.4, 1.2).move_to(P(1.8, -0.8))
        a_rv = arr(P(-1.8, -0.2), P(-1.8, 0.4), GREY, 4)
        a_lv = arr(P(1.8, -0.2), P(1.8, 0.4), GREY, 4)
        pa = box("pulmonary artery", LUNG, 2.7, 0.62, size=22).move_to(P(-1.8, 2.8))
        ao = box("aorta", GREY, 1.5, 0.62, size=22).move_to(P(1.8, 2.8))
        a_pa = arr(P(-1.8, 1.8), P(-1.8, 2.47), GREY, 4)
        a_ao = arr(P(1.8, 1.8), P(1.8, 2.47), GREY, 4)
        lungs = box("lungs", LUNG, 1.8, 0.9, size=24).move_to(P(-5.3, 2.8))
        a_lung = arr(P(-3.15, 2.8), P(-4.2, 2.8), LUNG, 2, tip=0.18)
        res = T("fluid-filled,\nhigh resistance", 22, LUNG, line_spacing=0.9).move_to(P(-5.2, 1.9))
        side = T("Left and right\nare the fetus's own", 22, GREY, line_spacing=0.9).move_to(P(-5.0, 0.2))
        self.play(FadeIn(RV), FadeIn(LV), FadeIn(RA), FadeIn(LA), FadeIn(a_rv), FadeIn(a_lv),
                  FadeIn(pa), FadeIn(ao), FadeIn(a_pa), FadeIn(a_ao), FadeIn(side), run_time=0.7)
        self.play(FadeIn(lungs), GrowArrow(a_lung), run_time=0.5)
        self.at("fluid filled")
        self.play(FadeIn(res, shift=DOWN * 0.1), run_time=0.5)

        # ductus venosus: umbilical vein from the placenta; a share past the liver
        plac = box("placenta", PLAC, 1.7, 2.6, size=24).move_to(P(5.4, 0.3))
        yv = -2.85
        vein_dir = arr(P(5.4, -1.0), P(5.4, -1.9), PLAC, 5)
        vein_l1 = Line(P(5.4, -1.9), P(5.4, yv), color=PLAC, stroke_width=5)
        vein_l2 = Line(P(5.4, yv), P(2.6, yv), color=PLAC, stroke_width=5)
        dv = Line(P(2.6, yv), P(-1.8, yv), color=SHUNT, stroke_width=5)
        dv_dir = arr(P(0.1, yv), P(-0.5, yv), SHUNT, 4)
        dv_up = arr(P(-1.8, yv), P(-1.8, -2.33), SHUNT, 4)
        liver = box("liver", GREY, 1.3, 0.7, size=22).move_to(P(2.6, -2.0))
        to_liver = arr(P(2.6, yv), P(2.6, -2.35), PLAC, 4, tip=0.18)
        ivc = box("inferior vena cava", GREY, 2.9, 0.6, size=22).move_to(P(-1.8, -2.0))
        l_vein = T("umbilical vein", 22, PLAC).move_to(P(4.1, yv - 0.38))
        l_dv = T("ductus venosus", 22, SHUNT).move_to(P(0.3, yv + 0.38))
        ivc_ra = arr(P(-1.8, -1.68), P(-1.8, -1.42), GREY, 3, tip=0.14)
        self.at("ductus venosus")
        self.play(FadeIn(plac), run_time=0.5)
        self.play(GrowArrow(vein_dir), Create(vein_l1), Create(vein_l2), FadeIn(l_vein), run_time=1.0)
        self.play(FadeIn(liver), FadeIn(ivc), GrowArrow(to_liver), run_time=0.5)
        self.play(Create(dv), GrowArrow(dv_dir), GrowArrow(dv_up), GrowArrow(ivc_ra), run_time=0.8)
        self.play(FadeIn(l_dv), run_time=0.4)

        # foramen ovale
        fo = arr(P(-0.55, -0.8), P(0.55, -0.8), SHUNT, 4, tip=0.22)
        l_fo = T("foramen ovale", 22, SHUNT).move_to(P(0.0, 0.05))
        l_fo2 = Line(P(0, -0.2), P(0, -0.65), color=SHUNT, stroke_width=2)
        self.at("foramen ovale")
        self.play(GrowArrow(fo), FadeIn(l_fo), Create(l_fo2), run_time=0.8)
        self.at("right atrium to the left")
        self.play(Indicate(RA, color=SHUNT, scale_factor=1.04), Indicate(LA, color=SHUNT, scale_factor=1.04), run_time=0.9)

        # ductus arteriosus
        da = arr(P(-0.45, 2.8), P(1.05, 2.8), SHUNT, 9, tip=0.28)
        l_da = T("ductus arteriosus", 22, SHUNT).move_to(P(0.3, 3.35))
        self.at("Most of the blood")
        self.play(GrowArrow(da), FadeIn(l_da), run_time=0.9)
        self.at("into the aorta")
        self.play(Indicate(ao, color=SHUNT, scale_factor=1.1), run_time=0.8)

        # umbilical arteries
        art = path_arrow([P(2.55, 2.8), P(5.4, 2.8), P(5.4, 1.6)], PLAC, 5)
        l_art = T("umbilical arteries", 22, PLAC).move_to(P(4.0, 3.3))
        self.at("Umbilical arteries")
        self.play(Create(art[0]), GrowArrow(art[1]), FadeIn(l_art), run_time=1.2)
        self.at("low resistance bed")
        self.play(Indicate(plac, color=PLAC, scale_factor=1.05), run_time=0.9)
        body = box("fetal body", SYS, 1.9, 0.6, size=22).move_to(P(3.95, 2.05))
        body_a = arr(P(3.95, 2.8), P(3.95, 2.38), SYS, 3, tip=0.14)
        self.at("in parallel")
        self.play(FadeIn(body), GrowArrow(body_a), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
def gauge(cx, cy, w, color, tracker, h=0.5):
    """A horizontal bar gauge whose fill follows `tracker` (0 to 1)."""
    out = Rectangle(width=w, height=h, stroke_color=color, stroke_width=3).move_to(P(cx, cy))
    x0 = cx - w / 2
    fill = always_redraw(lambda: Rectangle(width=max(0.02, w * tracker.get_value()), height=h - 0.06, stroke_width=0,
                                           fill_color=color, fill_opacity=0.6
                                           ).move_to(P(x0 + max(0.02, w * tracker.get_value()) / 2, cy)))
    return out, fill


class S03Breath(SpokenScene):
    """Lungs aerate -> resistance falls -> flow rises -> left atrial pressure passes right -> the flap closes."""

    def construct(self):
        yb, H = -2.8, 3.6                       # tank floor and height (top at 0.8)
        RAx, LAx, TW = -3.7, 0.0, 3.2
        o_lo, o_hi = -1.0, 0.0                  # the opening in the septum (the foramen ovale)
        ra_out = Rectangle(width=TW, height=H, stroke_color=GREY, stroke_width=3).move_to(P(RAx, yb + H / 2))
        la_out = Rectangle(width=TW, height=H, stroke_color=GREY, stroke_width=3).move_to(P(LAx, yb + H / 2))
        sx = -1.85
        sep_lo = Rectangle(width=0.3, height=(o_lo - yb), stroke_width=0, fill_color=GREY, fill_opacity=0.9
                           ).move_to(P(sx, (yb + o_lo) / 2))
        sep_hi = Rectangle(width=0.3, height=(yb + H - o_hi), stroke_width=0, fill_color=GREY, fill_opacity=0.9
                           ).move_to(P(sx, (yb + H + o_hi) / 2))
        lv_ra, lv_la = ValueTracker(0.70), ValueTracker(0.35)

        def level(tr, cx):
            def f():
                h = max(0.02, tr.get_value() * H)
                r = Rectangle(width=TW - 0.1, height=h, stroke_width=0, fill_color=PRESS, fill_opacity=0.32
                              ).move_to(P(cx, yb + h / 2))
                top = Line(P(cx - TW / 2 + 0.05, yb + h), P(cx + TW / 2 - 0.05, yb + h), color=PRESS, stroke_width=4)
                return VGroup(r, top)
            return f
        fill_ra = always_redraw(level(lv_ra, RAx))
        fill_la = always_redraw(level(lv_la, LAx))
        hinge = P(-1.62, o_hi)                  # the flap hangs from the top of the opening, on the left-atrial side
        flap = Rectangle(width=0.12, height=1.0, stroke_width=0, fill_color=TEXT, fill_opacity=1.0
                         ).move_to(hinge + DOWN * 0.5)
        flap.rotate(32 * DEGREES, about_point=hinge)
        lab_ra = T("right atrium\n(body's right)", 22, GREY, line_spacing=0.9).move_to(P(RAx, 2.75))
        lab_la = T("left atrium\n(body's left)", 22, GREY, line_spacing=0.9).move_to(P(LAx, 2.75))
        lab_fo = T("foramen ovale", 22, SHUNT).move_to(P(sx, 1.3))
        lab_flap = T("flap of septum primum", 22, TEXT).move_to(P(0.9, 1.3))
        lead = Line(P(-0.45, 1.15), P(-1.55, -0.05), color=TEXT, stroke_width=2)
        stream = arr(P(-3.3, -0.3), P(-0.9, -0.3), SHUNT, 7, tip=0.28)
        lab_stream = T("right-to-left stream", 22, SHUNT).move_to(P(-3.7, 0.45))
        note = T("water level = pressure, in this sketch", 22, GREY).move_to(P(-1.85, -3.45))
        lungs = box("lungs", LUNG, 2.0, 1.4, size=26, op=0.10).move_to(P(4.75, 1.9))
        pv = arr(P(3.75, 0.45), P(1.65, 0.45), LUNG, 2, tip=0.18).set_z_index(3)
        pv_lab = T("pulmonary\nvenous return", 22, LUNG, line_spacing=0.9).move_to(P(2.65, -0.15))
        res_lab = T("pulmonary vascular\nresistance", 22, LUNG, line_spacing=0.9).move_to(P(4.75, -1.05))
        g_tr = ValueTracker(0.90)
        g_out, g_fill = gauge(4.75, -2.0, 2.6, LUNG, g_tr)
        g_note = T("in this sketch, relative", 22, GREY).move_to(P(4.75, -2.7))

        self.play(FadeIn(ra_out), FadeIn(la_out), FadeIn(sep_lo), FadeIn(sep_hi), FadeIn(lab_ra), FadeIn(lab_la),
                  FadeIn(fill_ra), FadeIn(fill_la), FadeIn(flap), FadeIn(lab_fo), FadeIn(lungs), FadeIn(res_lab),
                  FadeIn(g_out), FadeIn(g_fill), FadeIn(g_note), FadeIn(pv), FadeIn(pv_lab), FadeIn(note),
                  FadeIn(stream), FadeIn(lab_stream), run_time=0.6)
        self.at("air fills the lungs")
        self.play(lungs[0].animate.set_fill(LUNG, opacity=0.38), run_time=0.7)
        self.at("pulmonary vascular resistance falls")
        self.play(g_tr.animate.set_value(0.25), run_time=1.3)
        pv2 = arr(P(3.75, 0.45), P(1.65, 0.45), LUNG, 10, tip=0.3).set_z_index(3)
        self.at("Pulmonary blood flow rises")
        self.play(ReplacementTransform(pv, pv2), run_time=0.9)
        self.at("raises pressure in the left atrium")
        cmp_ = T("left atrial pressure > right atrial pressure", 22, PRESS).move_to(P(-1.85, 1.9))
        self.play(lv_la.animate.set_value(0.70), run_time=1.3, rate_func=linear)
        self.play(FadeIn(cmp_), FadeOut(stream), FadeOut(lab_stream), lv_la.animate.set_value(0.88), run_time=0.7,
                  rate_func=linear)
        self.at("exceeds right atrial pressure")
        self.play(Indicate(fill_la, color=PRESS, scale_factor=1.02), run_time=0.8)
        flap_closed = Rectangle(width=0.12, height=1.0, stroke_width=0, fill_color=TEXT, fill_opacity=1.0
                                ).move_to(P(-1.62, -0.5))
        self.at("pressed against the septum")
        self.play(Transform(flap, flap_closed), FadeIn(lab_flap), Create(lead), run_time=1.0)
        self.at("stops carrying")
        stop = T("no right-to-left stream", 22, GREY).move_to(P(-3.7, 0.45))
        self.play(FadeIn(stop), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Placenta(SpokenScene):
    """Placental bed removed -> resistance up; oxygen narrows the duct; three bars for the neonate ultrasound."""

    def construct(self):
        # --- phase A: two beds in parallel -------------------------------------------------
        src = box("aorta", GREY, 1.6, 4.6, size=26).move_to(P(-5.2, 0.0))
        pl = box("placenta\n(low resistance)", PLAC, 3.6, 1.6, size=26).move_to(P(-1.4, 1.7))
        bd = box("fetal body", SYS, 3.6, 1.0, size=26).move_to(P(-1.4, -1.9))
        a_pl = arr(P(-4.4, 0.8), P(-3.25, 1.5), PLAC, 10, tip=0.3)
        a_bd = arr(P(-4.4, -0.8), P(-3.25, -1.6), SYS, 3, tip=0.2)
        g_lab = T("systemic vascular resistance\nand ventricular afterload", 24, SYS, line_spacing=0.9).move_to(P(3.9, 1.2))
        g_tr = ValueTracker(0.30)
        g_out, g_fill = gauge(3.9, 0.1, 3.2, SYS, g_tr, h=0.6)
        g_note = T("in this sketch, relative", 22, GREY).move_to(P(3.9, -0.6))
        self.play(FadeIn(src), FadeIn(pl), FadeIn(bd), GrowArrow(a_pl), GrowArrow(a_bd), FadeIn(g_lab), FadeIn(g_out),
                  FadeIn(g_fill), FadeIn(g_note), run_time=0.7)
        cross = VGroup(Line(pl.get_corner(UL) + DR * 0.15, pl.get_corner(DR) + UL * 0.15, color=GREY, stroke_width=6),
                       Line(pl.get_corner(UR) + DL * 0.15, pl.get_corner(DL) + UR * 0.15, color=GREY, stroke_width=6))
        self.at("removes a low resistance")
        self.play(FadeOut(a_pl), pl.animate.set_opacity(0.25), Create(cross), run_time=0.9)
        self.at("so systemic vascular")
        self.play(g_tr.animate.set_value(0.85), run_time=2.6)
        # --- phase B: oxygen and the ductus arteriosus ---------------------------------------
        self.at("Oxygen constricts")
        self.remove(g_fill)
        self.play(FadeOut(VGroup(src, pl, bd, a_bd, g_lab, g_out, g_note, cross)), run_time=0.5)
        pa = box("pulmonary\nartery", LUNG, 2.6, 1.4, size=28).move_to(P(-4.7, 0.4))
        ao = box("aorta", GREY, 2.2, 1.4, size=28).move_to(P(4.7, 0.4))
        duct = RoundedRectangle(corner_radius=0.25, width=4.8, height=1.7, stroke_color=SHUNT, stroke_width=4,
                                fill_color=SHUNT, fill_opacity=0.25).move_to(P(0.0, 0.4))
        l_duct = T("ductus arteriosus", 28, SHUNT).move_to(P(0.0, 1.8))
        ox = chip("oxygen", OXY, 30).move_to(P(0.0, -1.7))
        a_ox = arr(P(0.0, -1.2), P(0.0, -0.55), OXY, 6)
        ring = T("tested on fresh human ductal rings,\nfrom infants about nine days old, outside the body", 22, GREY,
                 line_spacing=0.9).move_to(P(0.0, -3.0))
        self.play(FadeIn(pa), FadeIn(ao), FadeIn(duct), FadeIn(l_duct), FadeIn(ox), GrowArrow(a_ox), run_time=0.7)
        narrowed = RoundedRectangle(corner_radius=0.12, width=4.8, height=0.34, stroke_color=SHUNT, stroke_width=4,
                                    fill_color=SHUNT, fill_opacity=0.25).move_to(P(0.0, 0.4))
        self.play(Transform(duct, narrowed), run_time=1.6)
        self.play(FadeIn(ring), run_time=0.6)
        # --- phase C: the neonate ultrasound -------------------------------------------------
        self.at("do not arrive together")
        self.play(FadeOut(VGroup(pa, ao, duct, l_duct, ox, a_ox, ring)), run_time=0.5)
        X0, K = -5.6, 0.11         # 100 percent = 11 units
        rows = [("ductus arteriosus closed before day 3", 94, 2.3),
                ("ductus venosus closed by then", 12, 1.0)]
        bars, labs = [], []
        for name, v, y in rows:
            lb = T(name, 24, SHUNT)
            lb.move_to(P(X0 + lb.width / 2, y + 0.55))
            labs.append(lb)
            bars.append(Rectangle(width=max(0.02, v * K), height=0.55, stroke_width=0, fill_color=SHUNT,
                                  fill_opacity=0.75).move_to(P(X0 + v * K / 2, y - 0.1)))
        yax = -0.3
        axis = Line(P(X0, yax), P(X0 + 100 * K, yax), color=GREY, stroke_width=3)
        ticks = VGroup(*[VGroup(Line(P(X0 + v * K, yax), P(X0 + v * K, yax - 0.12), color=GREY, stroke_width=3),
                                M(str(v), 22, GREY).move_to(P(X0 + v * K, yax - 0.42))) for v in (0, 50, 100)])
        cap = T("percent of 50 healthy term neonates", 22, GREY).move_to(P(X0 + 50 * K, yax - 0.95))
        rule = DashedLine(P(X0, -2.0), P(X0 + 100 * K, -2.0), color=GREY, stroke_width=2, stroke_opacity=0.5)
        stmt = T("foramen ovale: Doppler found flow in every infant studied", 28, SHUNT).move_to(P(0.0, -2.8))
        self.play(Create(axis), FadeIn(ticks), FadeIn(cap), run_time=0.5)
        self.play(FadeIn(labs[0]), run_time=0.4)
        self.play(FadeIn(labs[1]), run_time=0.4)
        self.at("healthy term neonates")
        v1 = M("94", 26, TEXT).next_to(bars[0], RIGHT, buff=0.15)
        self.at("had closed")
        self.play(GrowFromEdge(bars[0], LEFT), run_time=1.0)
        self.play(FadeIn(v1), run_time=0.3)
        self.at("Only")
        self.play(GrowFromEdge(bars[1], LEFT), run_time=0.8)
        v2 = M("12", 26, TEXT).next_to(bars[1], RIGHT, buff=0.15)
        self.play(FadeIn(v2), run_time=0.3)
        self.at("Doppler found")
        self.play(Create(rule), FadeIn(stmt), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Lambs(SpokenScene):
    """Two orders in preterm lambs: clamp first drops right ventricular output, ventilate first does not."""

    def construct(self):
        yb, SC = -1.9, 0.022         # axis floor; units per mL/min/kg
        bx1, bx2 = -5.2, -1.3
        note = T("preterm lambs, 126 ± 1 days of gestation, six per group", 22, GREY).move_to(P(0.0, -3.4))
        axis = Line(P(-6.0, yb), P(-0.2, yb), color=GREY, stroke_width=3)
        unit = T("mean right ventricular output,\nmL/min/kg (mean ± SEM)", 22, GREY, line_spacing=0.9).move_to(P(-3.2, 2.15))
        self.play(FadeIn(note), Create(axis), FadeIn(unit), run_time=0.5)
        c1 = chip("1  clamp cord", PLAC, 24).move_to(P(-4.4, 3.1))
        c2 = chip("2  ventilate", LUNG, 24).move_to(P(-1.4, 3.1))
        ca = arr(c1.get_right() + RIGHT * 0.08, c2.get_left() + LEFT * 0.08, GREY, 4, tip=0.18)
        d1 = chip("1  ventilate", LUNG, 24).move_to(P(2.0, 3.1))
        d2 = chip("2  clamp cord", PLAC, 24).move_to(P(5.0, 3.1))
        da = arr(d1.get_right() + RIGHT * 0.08, d2.get_left() + LEFT * 0.08, GREY, 4, tip=0.18)
        divider = DashedLine(P(0.15, 2.6), P(0.15, -2.9), color=GREY, stroke_width=2, stroke_opacity=0.5)
        self.at("clamped before ventilation")
        self.play(FadeIn(c1), FadeIn(c2), GrowArrow(ca), FadeIn(divider), run_time=0.8)
        self.at("or ventilated before clamping")
        self.play(FadeIn(d1), FadeIn(d2), GrowArrow(da), run_time=0.8)
        b1 = Rectangle(width=1.2, height=114.6 * SC, stroke_width=0, fill_color=PLAC, fill_opacity=0.9
                       ).move_to(P(bx1, yb + 114.6 * SC / 2))
        lb1 = T("before\nthe clamp", 22, GREY, line_spacing=0.9).move_to(P(bx1, yb - 0.5))
        self.at("Clamping first dropped")
        self.play(FadeIn(b1), FadeIn(lb1), run_time=0.7)
        b2 = Rectangle(width=1.2, height=114.6 * SC, stroke_width=0, fill_color=PLAC, fill_opacity=0.9
                       ).move_to(P(bx2, yb + 114.6 * SC / 2))
        lb2 = T("after the clamp,\nbefore ventilation", 22, GREY, line_spacing=0.9).move_to(P(bx2, yb - 0.5))
        self.play(FadeIn(b2), FadeIn(lb2), run_time=0.3)
        target = Rectangle(width=1.2, height=38.8 * SC, stroke_width=0, fill_color=PLAC, fill_opacity=0.9
                           ).move_to(P(bx2, yb + 38.8 * SC / 2))
        top1 = yb + 114.6 * SC
        level = DashedLine(P(bx1 + 0.6, top1), P(bx2 + 0.6, top1), color=PLAC, stroke_width=2)
        fall = T("about 66\npercent lower", 24, PLAC, weight=BOLD, line_spacing=0.9).move_to(P((bx1 + bx2) / 2, 0.15))
        self.play(Transform(b2, target), Create(level), run_time=1.3)
        self.play(FadeIn(fall), run_time=0.5)
        self.at("group means fell")

        def sem_bar(x, mean, sem):
            ya, yc = yb + (mean - sem) * SC, yb + (mean + sem) * SC
            return VGroup(Line(P(x, ya), P(x, yc), color=TEXT, stroke_width=3),
                          Line(P(x - 0.15, ya), P(x + 0.15, ya), color=TEXT, stroke_width=3),
                          Line(P(x - 0.15, yc), P(x + 0.15, yc), color=TEXT, stroke_width=3))
        e1, e2 = sem_bar(bx1, 114.6, 14.4), sem_bar(bx2, 38.8, 9.7)
        v1 = M("114.6", 24, TEXT).move_to(P(bx1, yb + (114.6 + 14.4) * SC + 0.32))
        v2 = M("38.8", 24, TEXT).move_to(P(bx2, yb + (38.8 + 9.7) * SC + 0.32))
        self.play(FadeIn(e1), FadeIn(v1), run_time=0.5)
        self.play(FadeIn(e2), FadeIn(v2), run_time=0.5)
        self.at("Heart rate")
        hr = T("heart rate\nalso down\nabout 40 percent", 22, PLAC, line_spacing=0.9).move_to(P((bx1 + bx2) / 2, -1.0))
        self.play(FadeIn(hr), run_time=0.6)
        self.at("Ventilating first")
        flat = Line(P(0.9, 0.2), P(5.9, 0.2), color=LUNG, stroke_width=8)
        flat_t = T("stable flows\nand pressures", 30, LUNG, line_spacing=0.9).move_to(P(3.4, 1.2))
        flat_s = T("across the transition", 24, GREY).move_to(P(3.4, -0.5))
        self.play(Create(flat), FadeIn(flat_t), FadeIn(flat_s), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Handover(SpokenScene):
    """Filling of the left ventricle changes source from umbilical to pulmonary venous return."""

    def construct(self):
        lv = box("left ventricle\nfilling", GREY, 3.2, 2.8, size=28).move_to(P(1.2, 0.9))
        u_thick = arr(P(-5.4, 1.7), P(-0.5, 1.7), PLAC, 14, tip=0.34)
        p_thin = arr(P(-5.4, 0.1), P(-0.5, 0.1), LUNG, 2, tip=0.18)
        u_lab = T("umbilical venous return", 28, PLAC).move_to(P(-2.9, 2.5))
        p_lab = T("pulmonary venous return", 28, LUNG).move_to(P(-2.9, -0.6))
        before = T("before aeration", 26, GREY, weight=BOLD).move_to(P(-4.6, 3.2))
        self.play(FadeIn(lv), run_time=0.6)
        self.at("before aeration")
        self.play(FadeIn(before), run_time=0.4)
        self.at("umbilical venous return supplies")
        self.play(GrowArrow(u_thick), FadeIn(u_lab), run_time=0.9)
        self.play(GrowArrow(p_thin), FadeIn(p_lab), run_time=0.6)
        lamb = chip("preterm lambs: a mechanism, no human outcome", GREY, 22).move_to(P(1.7, 3.2))
        self.at("mechanism in preterm lambs")
        self.play(FadeOut(before), FadeIn(lamb), run_time=0.6)
        k1 = box("transfusion of\nblood volume", GREY, 2.8, 1.1, size=24).move_to(P(4.75, 2.0))
        k2 = box("preload\nreplacement", GREY, 2.8, 1.1, size=24).move_to(P(4.75, -0.2))
        q = T("?", 64, GOLD, weight=BOLD).move_to(P(4.75, 0.9))
        self.at("cannot separate")
        self.play(FadeIn(k1), FadeIn(k2), FadeIn(q), run_time=0.8)
        self.at("Aeration lets")
        self.play(FadeOut(k1), FadeOut(k2), FadeOut(q), run_time=0.5)
        u_thin = arr(P(-5.4, 1.7), P(-0.5, 1.7), PLAC, 2, tip=0.18)
        p_thick = arr(P(-5.4, 0.1), P(-0.5, 0.1), LUNG, 14, tip=0.34)
        after = T("after aeration", 26, GREY, weight=BOLD).move_to(P(-4.6, 3.2))
        self.play(Transform(u_thick, u_thin), Transform(p_thin, p_thick), FadeIn(after), run_time=1.6)
        # the order
        ra = chip("clamp, then aerate", PLAC, 24).move_to(P(-3.7, -2.0))
        ra_t = T("reading: preload falls as afterload rises", 24, PLAC).move_to(P(2.8, -2.0))
        rb = chip("aerate, then clamp", LUNG, 24).move_to(P(-3.7, -3.0))
        rb_t = T("flows and pressures stable", 24, LUNG).move_to(P(2.8, -3.0))
        ar_a = arr(ra.get_right() + RIGHT * 0.1, P(-0.45, -2.0), GREY, 3, tip=0.16)
        ar_b = arr(rb.get_right() + RIGHT * 0.1, P(-0.45, -3.0), GREY, 3, tip=0.16)
        self.at("the order decides")
        self.play(FadeIn(ra), GrowArrow(ar_a), FadeIn(ra_t), run_time=0.8)
        self.at("falls as afterload rises")
        self.play(FadeIn(rb), GrowArrow(ar_b), FadeIn(rb_t), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "Aeration lets pulmonary venous return take over the filling."
