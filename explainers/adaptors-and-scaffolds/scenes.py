"""Adaptors, docking proteins and scaffolds: switching on Ras without touching it  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = the growth factor (the signal outside the cell)
  BLUE   = the receptor and its tail
  GOLD   = a phosphate (the round "P" badge)
  PINK   = an SH2 domain (the cup that closes on a phosphate)
  TEAL   = Grb2, the adaptor
  ORANGE = an SH3 domain (the claw that holds a partner)
  PURPLE = Sos, the exchange factor
  GREEN  = on (Ras switched on, GTP)
  RED    = ruled out (the line from the receptor to Ras, the kinase that is not needed)
  GREY   = membrane, Ras while off (GDP), proteins not yet named, labels

No molecular structures: the receptor is a bar with a tail, proteins are labelled pills, the SH2 domain
is a cup, an SH3 domain is a claw, a phosphate is a "P" badge, the membrane is a bar.

One picture, two framings (the same parts, rebuilt bigger where they are the subject):
  STAGE  (scenes 1, 2, 4, 5, 6)  the membrane across the top; the receptor tail runs down the left,
         Ras hangs under the membrane on the right, and the space between them is the gap the film fills.
  CLOSE  (scene 3)               the adaptor and its partner fill the frame; no membrane.
The change of framing is animated after the narration (Film.outro), so each scene starts on the picture
the last one left.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
PINK = "#F08BB4"
ORANGE = "#F29E4C"

# ---------------------------------------------------------------------------------------------
# geometry of the STAGE (frame units)
# ---------------------------------------------------------------------------------------------
MEM_Y, MEM_H = 1.70, 0.38          # membrane bar
XR = -3.7                          # the receptor
BAR_TOP, BAR_BOT = 2.55, 1.25      # the receptor bar crosses the membrane
TAIL_END = -2.75
NUB = 0.45                         # the stub that carries a tyrosine
YP = (0.15, -0.95, -2.1)           # the three tyrosines on the tail
PR = 0.24                          # phosphate badge radius
PX = XR + NUB + PR                 # centre x of a phosphate
CUP_IN, CUP_OUT = 0.31, 0.47       # SH2 cup radii
OPEN, SHUT = 150, 290              # cup opening angle (degrees): open / closed on a phosphate
C_DOCK = np.array([PX, YP[2], 0.0])          # cup centre when it grips the lowest phosphate
PREDOCK = C_DOCK + np.array([1.0, 0.0, 0.0])

# the adaptor, offsets from the cup centre (scaled by k)
CUP_TO_BODY = CUP_OUT - 0.05
BODY_W, BODY_H = 2.1, 0.95
BODY_HG = 1.6                       # Grb2 is taller: SH3 claw, SH2 cup, SH3 claw run down its length
CLAW_DY = 0.62
BODY_DX = CUP_TO_BODY + BODY_W / 2
CLAW_X0 = CUP_TO_BODY + BODY_W     # right edge of the body
CLAW_LEN = 0.40
SOS_LEFT = CLAW_X0 + 0.48
SOS_W, SOS_H = 2.4, 3.8
SOS_DY = 1.0                        # Sos centre is this far above the cup centre
SOS_RIGHT = SOS_LEFT + SOS_W
RAS_W, RAS_H = 1.4, 0.9
RAS_X = C_DOCK[0] + SOS_RIGHT + RAS_W / 2          # Ras sits against the top of Sos
RAS_Y = C_DOCK[1] + 2.85


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=24, pad=0.2, **kw):
    """chip with an opaque backing so lines drawn behind it do not show through."""
    c = chip(text, color, size=size, pad=pad, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def ghost_chip(text, size=22):
    """a dashed grey chip: something that is NOT in this pathway."""
    t = T(text, size, GREY)
    box = RoundedRectangle(corner_radius=0.14, width=t.width + 0.4, height=t.height + 0.32)
    return VGroup(DashedVMobject(box, num_dashes=max(18, int(box.width * 9))).set_color(GREY), t)


def strike(m, color=RED):
    return Line(m.get_corner(DL) + [-0.08, -0.04, 0], m.get_corner(UR) + [0.08, 0.04, 0], color=color, stroke_width=7)


def cross_at(p, r=0.24, color=RED, w=7):
    p = np.array(p, float)
    return VGroup(Line(p + [-r, -r, 0], p + [r, r, 0], color=color, stroke_width=w),
                  Line(p + [-r, r, 0], p + [r, -r, 0], color=color, stroke_width=w))


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def pbadge(r=PR):
    c = Circle(radius=r, stroke_color=GOLD, stroke_width=2, fill_color=GOLD, fill_opacity=1)
    return VGroup(c, T("P", 22, BG, weight=BOLD).move_to(c))


def pop(m, s=1.35):
    """swell and settle, without recolouring (Indicate would hide the P on a badge)."""
    return m.animate(rate_func=there_and_back).scale(s)


def glow(*mobs, s=1.1, color=TEXT):
    """flash each mobject in place (one animation per mobject)."""
    return [Indicate(m, color=color, scale_factor=s) for m in mobs]


def membrane():
    return RoundedRectangle(corner_radius=0.12, width=12.6, height=MEM_H, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.35).move_to([0, MEM_Y, 0])


def receptor():
    """the receptor: a bar through the membrane and a tail with three tyrosines. [tail, stubs, dots, back, bar]"""
    mid = (BAR_TOP + BAR_BOT) / 2
    tail = Line([XR, BAR_BOT, 0], [XR, TAIL_END, 0], color=BLUE, stroke_width=7)
    stubs = VGroup(*[Line([XR, y, 0], [XR + NUB, y, 0], color=BLUE, stroke_width=6) for y in YP])
    dots = VGroup(*[Dot([XR + NUB, y, 0], radius=0.08, color=BLUE) for y in YP])
    back = RoundedRectangle(corner_radius=0.14, width=0.42, height=BAR_TOP - BAR_BOT, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to([XR, mid, 0])
    bar = RoundedRectangle(corner_radius=0.14, width=0.42, height=BAR_TOP - BAR_BOT, stroke_color=BLUE, stroke_width=4,
                           fill_color=BLUE, fill_opacity=0.4).move_to([XR, mid, 0])
    g = VGroup(tail, stubs, dots, back, bar)
    g.tail, g.bar = tail, bar
    return g


def ras(color=GREY, opacity=1.0):
    """Ras: a pill hanging from the inner face of the membrane on a short anchor. [stalk, back, body, label]"""
    stalk = Line([RAS_X, RAS_Y + RAS_H / 2, 0], [RAS_X, MEM_Y + 0.05, 0], color=color, stroke_width=7)
    back = RoundedRectangle(corner_radius=0.3, width=RAS_W, height=RAS_H, stroke_width=0, fill_color=BG,
                            fill_opacity=1).move_to([RAS_X, RAS_Y, 0])
    body = RoundedRectangle(corner_radius=0.3, width=RAS_W, height=RAS_H, stroke_color=color, stroke_width=4,
                            fill_color=color, fill_opacity=0.3).move_to([RAS_X, RAS_Y, 0])
    lab = T("Ras", 32, color, weight=BOLD).move_to(body)
    g = VGroup(stalk, back, body, lab)
    g.stalk, g.body, g.lab = stalk, body, lab
    if opacity < 1:
        stalk.set_stroke(opacity=opacity)
        body.set_stroke(opacity=opacity).set_fill(opacity=0.3 * opacity)
        lab.set_opacity(opacity)
    return g


def ras_to(r, color):
    """animations that turn Ras to a colour."""
    return [r.stalk.animate.set_stroke(color), r.body.animate.set_stroke(color).set_fill(color, 0.3),
            r.lab.animate.set_color(color)]


def ras_dim(r, o):
    return [r.stalk.animate.set_stroke(opacity=o), r.body.animate.set_stroke(opacity=o).set_fill(opacity=0.3 * o),
            r.lab.animate.set_opacity(o)]


def phos_pos(i):
    return np.array([PX, YP[i], 0.0])


class Stage:
    """the fixed part of the picture: membrane, receptor, growth factor, phosphates, Ras."""

    def __init__(self, gf=True, ps=(0, 1, 2), ras_opacity=1.0, ras_color=GREY, with_ras=True):
        self.mem = membrane()
        self.rec = receptor()
        self.rlab = T("receptor", 24, BLUE).move_to([XR - 1.15, 2.2, 0])
        self.gf = bchip("growth factor", YELLOW, 24).move_to([XR, 3.0, 0]) if gf else None
        self.ps = {i: pbadge().move_to(phos_pos(i)) for i in ps}
        self.ras = ras(ras_color, ras_opacity) if with_ras else None

    def parts(self, ras_too=True):
        ms = [self.mem, self.rec, self.rlab]
        if self.gf is not None:
            ms.append(self.gf)
        ms += list(self.ps.values())
        if ras_too and self.ras is not None:
            ms.append(self.ras)
        return ms


def cup_shape(c, deg, k=1.0, color=PINK):
    s = AnnularSector(inner_radius=CUP_IN * k, outer_radius=CUP_OUT * k, angle=deg * DEGREES,
                      start_angle=-deg / 2 * DEGREES, color=color, fill_opacity=1, stroke_width=0)
    return s.shift(np.array(c, float))


def reader(c, k=1.0, label="x", color=GREY, deg=SHUT, size=24, lcolor=None, show_label=True, bh=BODY_H):
    """a protein that carries an SH2 cup on its left end. c is the cup centre. [back, body, label, cup]"""
    c = np.array(c, float)
    ctr = c + k * np.array([BODY_DX, 0, 0])
    w, h = BODY_W * k, bh * k
    back = RoundedRectangle(corner_radius=0.4 * k, width=w, height=h, stroke_width=0, fill_color=BG,
                            fill_opacity=1).move_to(ctr)
    body = RoundedRectangle(corner_radius=0.4 * k, width=w, height=h, stroke_color=color, stroke_width=4 * k ** 0.5,
                            fill_color=color, fill_opacity=0.25).move_to(ctr)
    lab = T(label, size * k, lcolor or color, weight=BOLD, line_spacing=0.8).move_to(ctr)
    if not show_label:
        lab.set_opacity(0)
    cup = cup_shape(c, deg, k)
    g = VGroup(back, body, lab, cup)
    g.back, g.body, g.lab, g.cup, g.k = back, body, lab, cup, k
    return g


def cup_anim(g, d0, d1):
    """open or close the cup of a reader, wherever the reader now is."""
    k = g.k

    def upd(m, a):
        c = g.body.get_left() - np.array([CUP_TO_BODY * k, 0, 0])
        m.become(cup_shape(c, d0 + (d1 - d0) * a, k))
    return UpdateFromAlphaFunc(g.cup, upd)


def claws(c, k=1.0, color=ORANGE):
    """the two SH3 claws on the right end of the adaptor, opening to the right."""
    x0 = c[0] + CLAW_X0 * k
    g = VGroup()
    for dy in (CLAW_DY, -CLAW_DY):
        y = c[1] + dy * k
        m = VMobject().set_points_as_corners([[x0 + CLAW_LEN * k, y + 0.17 * k, 0], [x0, y + 0.17 * k, 0],
                                              [x0, y - 0.17 * k, 0], [x0 + CLAW_LEN * k, y - 0.17 * k, 0]])
        m.set_stroke(color, 9 * k ** 0.5).set_fill(opacity=0)
        g.add(m)
    return g


def sos(c, k=1.0):
    """Sos, held by the two claws. [back, body, label, tabs]"""
    c = np.array(c, float)
    ctr = c + k * np.array([SOS_LEFT + SOS_W / 2, SOS_DY, 0])
    w, h = SOS_W * k, SOS_H * k
    back = RoundedRectangle(corner_radius=0.45 * k, width=w, height=h, stroke_width=0, fill_color=BG,
                            fill_opacity=1).move_to(ctr)
    body = RoundedRectangle(corner_radius=0.45 * k, width=w, height=h, stroke_color=PURPLE, stroke_width=4 * k ** 0.5,
                            fill_color=PURPLE, fill_opacity=0.25).move_to(ctr)
    lab = T("Sos", 36 * k ** 0.6, PURPLE, weight=BOLD).move_to(ctr)
    tabs = VGroup()
    for dy in (CLAW_DY, -CLAW_DY):
        t = Rectangle(width=(SOS_LEFT - CLAW_X0 - 0.1) * k + 0.12 * k, height=0.14 * k, stroke_width=0,
                      fill_color=PURPLE, fill_opacity=0.8)
        t.move_to(c + k * np.array([(CLAW_X0 + 0.1 + SOS_LEFT) / 2, dy, 0]))
        tabs.add(t)
    g = VGroup(back, body, lab, tabs)
    g.back, g.body, g.lab, g.tabs = back, body, lab, tabs
    return g


def partner(c, k=1.0, gap=0.0, ph=0.75):
    """a protein that is not yet named, standing next to the adaptor. [back, body, label]"""
    c = np.array(c, float)
    w, h = 1.4 * k, ph * k
    ctr = c + k * np.array([CLAW_X0 + gap + 0.7, 0, 0])
    back = RoundedRectangle(corner_radius=0.3 * k, width=w, height=h, stroke_width=0, fill_color=BG,
                            fill_opacity=1).move_to(ctr)
    body = RoundedRectangle(corner_radius=0.3 * k, width=w, height=h, stroke_color=GREY, stroke_width=4 * k ** 0.5,
                            fill_color=GREY, fill_opacity=0.25).move_to(ctr)
    lab = T("partner", 22 * k, GREY, weight=BOLD).move_to(ctr)
    g = VGroup(back, body, lab)
    g.back, g.body, g.lab = back, body, lab
    return g


def gdp_chip():
    return bchip("GDP", GREY, 26, pad=0.16).move_to([RAS_X, RAS_Y - 1.05, 0])


def gtp_chip():
    return bchip("GTP", GREEN, 26, pad=0.16).move_to([RAS_X, RAS_Y - 1.05, 0])


def ring(c, r=0.6, color=TEXT, w=4):
    return Circle(radius=r, stroke_color=color, stroke_width=w).move_to(np.array(c, float))


class Film(SpokenScene):
    def frac(self, a, b, f, lead=0.2):
        """wait until a fraction f of the way from the start of phrase a to the start of phrase b."""
        t = self.t_of(a) + f * (self.t_of(b) - self.t_of(a)) - lead
        rest = t - self.elapsed()
        with open(Path(os.environ["KX_SCRIPT"]).parent / "sync.log", "a") as lg:
            lg.write(f"{os.environ.get('KX_SCENE_ID')}  {('%.2f of %s>%s' % (f, a, b))[:30]!r:36} at {t + lead:6.2f}  "
                     f"now {self.elapsed():6.2f}  late {-rest:+5.2f}\n")
        if rest > 0.02:
            self.wait(rest)

    def outro(self, *anims, then=None, after=None, run_time=0.38):
        """hold until the narration ends, clear what the next scene does not inherit, then (optionally)
        change framing. These run after the last word, so they add a short breath between scenes."""
        rest = self.narration_s - 0.02 - self.elapsed()
        if rest > 0:
            self.wait(rest)
        if anims:
            self.play(*anims, run_time=run_time)
        if then:
            self.play(*then, run_time=0.9)
        if after:
            self.play(*after, run_time=0.45)
        if then or after:
            self.wait(0.15)
        self.finish()


HOME_Z, HOME_C = 1.18, np.array([0.0, 0.25, 0.0])           # scenes 1, 4, 5, 6: the whole stage, a little closer
Z2, CEN2 = 1.5, np.array([-1.3, -0.67, 0.0])              # scenes 2 and 3 open on the tail, a little closer
C_CLOSE = C_DOCK + np.array([2.0, 0.0, 0.0])               # where the adaptor floats free in the close-up
Z3A, CEN3A = 2.0, np.array([C_CLOSE[0] + 1.9, C_DOCK[1] + 0.2, 0.0])     # close on Grb2 and the claws
Z3, CEN3 = 1.5, np.array([C_CLOSE[0] + (SOS_RIGHT - CUP_OUT) / 2, C_DOCK[1] + 1.1, 0.0])   # back far enough for all of Sos


class ZFilm(Film, MovingCameraScene):
    """a Film whose frame can move in on the action."""

    def look(self, z, cen):
        """the camera move, as an animation."""
        return self.camera.frame.animate.set(width=config.frame_width / z).move_to(cen)

    def look_now(self, z, cen):
        self.camera.frame.set(width=config.frame_width / z).move_to(cen)

    def look_home(self):
        return self.look(HOME_Z, HOME_C)




class S00Title(TitleCard):
    LESSON = "Adaptors, Docking Proteins and Scaffolds"
    TITLE = "Switching On Ras Without Touching It"


# ---------------------------------------------------------------------------------------------
class S01Gap(ZFilm):
    """a growth factor switches on Ras, yet the receptor never touches it: what sits in between? (STAGE)"""

    def construct(self):
        self.look_now(HOME_Z, HOME_C)
        st = Stage(gf=False, ps=())
        gf = bchip("growth factor", YELLOW, 24).move_to([XR + 2.2, 3.0, 0])
        self.play(FadeIn(st.mem), FadeIn(st.rec), FadeIn(st.rlab), FadeIn(st.ras), FadeIn(gf), run_time=0.5)

        self.at("binds its")
        self.play(gf.animate.move_to([XR, 3.0, 0]), run_time=0.7)
        on = T("on", 32, GREEN, weight=BOLD).move_to([RAS_X + 1.2, RAS_Y, 0])
        self.at("switches on")
        self.play(Indicate(st.ras.body, color=GREEN, scale_factor=1.12), Indicate(st.ras.lab, color=GREEN, scale_factor=1.12),
                  FadeIn(on, shift=RIGHT * 0.15), run_time=0.8)

        # the receptor and Ras never meet: a dimension line across the gap
        y = RAS_Y
        x0, x1 = XR + 0.4, RAS_X - RAS_W / 2 - 0.1
        dim_line = DashedLine([x0, y, 0], [x1, y, 0], color=RED, stroke_width=5, dash_length=0.16)
        caps = VGroup(Line([x0, y - 0.2, 0], [x0, y + 0.2, 0], color=RED, stroke_width=5),
                      Line([x1, y - 0.2, 0], [x1, y + 0.2, 0], color=RED, stroke_width=5))
        never = T("never touches", 26, RED).move_to([(x0 + x1) / 2, y + 0.42, 0])
        self.at("never touches")
        self.play(FadeOut(on), Create(dim_line), FadeIn(caps), FadeIn(never, shift=DOWN * 0.1), run_time=0.9)

        small = T("small switch protein", 24, GREY).move_to([RAS_X + 0.35, RAS_Y - 0.9, 0])
        self.at("small switch")
        self.play(FadeIn(small, shift=UP * 0.1), Indicate(st.ras.body, color=TEXT, scale_factor=1.1),
                  Indicate(st.ras.lab, color=TEXT, scale_factor=1.1), run_time=0.7)

        inner_y = MEM_Y - MEM_H / 2
        inner = Line([-6.3, inner_y, 0], [6.3, inner_y, 0], color=TEXT, stroke_width=5)
        inner_lbl = T("inner face", 24, TEXT).move_to([RAS_X + 2.05, inner_y - 0.32, 0])
        self.at("interface")
        self.play(Create(inner), FadeIn(inner_lbl), run_time=0.6)
        pm = T("plasma membrane", 24, GREY).move_to([4.2, MEM_Y + 0.55, 0])
        self.at("plasma membrane")
        self.play(FadeIn(pm, shift=DOWN * 0.1), run_time=0.5)

        # the receptor writes phosphates on its own tail
        ps = [pbadge().move_to([XR, BAR_BOT - 0.35, 0]) for _ in YP]
        self.at("adds phosphates")
        self.play(FadeOut(inner), FadeOut(inner_lbl), FadeOut(small), FadeOut(dim_line), FadeOut(caps), FadeOut(never),
                  FadeIn(VGroup(*ps), scale=0.5), run_time=0.5)
        self.play(LaggedStart(*[p.animate.move_to(phos_pos(i)) for i, p in enumerate(ps)], lag_ratio=0.3), run_time=1.5)
        tl = T("tail", 26, BLUE).move_to([XR - 0.6, -1.0, 0])
        self.at("own tail")
        self.play(FadeIn(tl, shift=RIGHT * 0.1), run_time=0.4)
        self.at("nothing can read")
        self.play(LaggedStart(*[pop(p, 1.4) for p in ps], lag_ratio=0.2), run_time=1.1)

        # the unknown path from the lowest phosphate to Ras
        a, b = phos_pos(2) + [0.45, 0, 0], np.array([1.15, YP[2], 0])
        c, d = np.array([1.15, RAS_Y, 0]), np.array([RAS_X - RAS_W / 2 - 0.12, RAS_Y, 0])
        path = DashedVMobject(VMobject().set_points_as_corners([a, b, c, d]), num_dashes=46).set_color(GREY)
        tip = Triangle(fill_color=GREY, fill_opacity=1, stroke_width=0).scale(0.13).rotate(-PI / 2).move_to(d + [0.05, 0, 0])
        qs = VGroup()
        for p in (np.array([-0.75, YP[2], 0]), np.array([1.15, -0.65, 0])):
            shape = RoundedRectangle(corner_radius=0.12, width=0.85, height=0.75)
            bk = shape.copy().set_stroke(width=0).set_fill(BG, 1).move_to(p)
            edge = DashedVMobject(shape.copy().move_to(p), num_dashes=20).set_color(GREY)
            qs.add(VGroup(bk, edge, T("?", 30, TEXT, weight=BOLD).move_to(p)))
        self.at("in between")
        self.play(Create(path), FadeIn(tip), FadeOut(pm), LaggedStart(*[FadeIn(q, scale=0.8) for q in qs], lag_ratio=0.35),
                  run_time=1.3)
        self.play(LaggedStart(*[pop(q[2], 1.5) for q in qs], lag_ratio=0.3), run_time=0.9)
        self.outro(FadeOut(VGroup(path, tip, qs, tl)), *ras_dim(st.ras, 0.35))


def s2_stage(with_ras=True):
    return Stage(gf=True, ps=(0, 1, 2), ras_opacity=0.35, with_ras=with_ras)


def pulse_body(g):
    return Indicate(g.body, color=TEXT, scale_factor=1.05)


class S02Reader(ZFilm):
    """each phosphate is a handhold; the SH2 cup closes on it; the proteins that carry a cup are enzymes or not. (TAIL)"""

    def construct(self):
        self.look_now(HOME_Z, HOME_C)
        st = s2_stage()
        self.add(*st.parts())
        P = st.ps

        self.at("phosphorylated tyrosine")
        self.play(self.look(Z2, CEN2), FadeOut(st.ras), LaggedStart(*[pop(P[i], 1.4) for i in (0, 1, 2)], lag_ratio=0.2), run_time=1.3)
        hand = T("handhold", 28, GOLD).next_to(P[0], RIGHT, buff=0.3)
        self.at("handhold")
        self.play(FadeIn(hand, shift=LEFT * 0.12), pop(P[0], 1.4), run_time=0.7)

        # a lone SH2 cup, then it grips the middle phosphate
        c_far = phos_pos(1) + np.array([1.5, 0, 0])
        cup = cup_shape(c_far, OPEN)
        self.at("that carry")
        self.play(FadeOut(hand), FadeIn(cup, scale=0.6), run_time=0.5)
        sh2 = T("SH2 domain", 28, PINK, weight=BOLD).move_to(c_far + [0.45, 0.95, 0])
        self.at("small folded")
        self.play(FadeIn(sh2, shift=DOWN * 0.1), Indicate(cup, color=TEXT, scale_factor=1.3), run_time=0.8)
        self.at("it grips")
        sh2_to = phos_pos(1) + np.array([2.0, 0.8, 0])
        lead2 = Line(sh2_to + [-0.85, -0.2, 0], phos_pos(1) + [0.42, 0.3, 0], color=PINK, stroke_width=3)
        self.play(cup.animate.shift(LEFT * 1.5), sh2.animate.move_to(sh2_to), run_time=0.7)
        cup2 = cup_shape(phos_pos(1), SHUT)
        self.play(Transform(cup, cup2), pop(P[1], 1.3), Create(lead2), run_time=0.45)
        self.play(*glow(cup, s=1.25), run_time=0.4)

        # the proteins that carry the cup arrive: one is an enzyme, one is not
        A = reader(phos_pos(1), 1.0, "enzyme", GREY, deg=SHUT, size=26, lcolor=TEXT)
        B = reader(phos_pos(2) + [2.2, 0, 0], 1.0, "no enzyme\nactivity", GREY, deg=OPEN, size=22, lcolor=TEXT)
        self.remove(cup)
        self.add(A.cup)                       # the cup that is already there
        self.at("recruiting these")
        self.play(FadeOut(sh2), FadeOut(lead2), GrowFromEdge(VGroup(A.back, A.body), LEFT), run_time=0.7)
        self.add(B.back, B.body, B.cup)
        self.play(B.animate.shift(LEFT * 2.2), run_time=1.0)
        self.play(cup_anim(B, OPEN, SHUT), pop(P[2], 1.3), run_time=0.45)
        self.at("enzymes")
        self.play(FadeIn(A.lab), pulse_body(A), run_time=0.7)
        self.at("have no enzyme")
        self.play(FadeIn(B.lab), pulse_body(B), run_time=0.8)
        pt = partner(phos_pos(2), 1.0)
        self.at("stands next to")
        self.play(GrowFromEdge(pt, LEFT), run_time=0.6)
        self.play(*glow(st.rec.tail, s=1.0, color=TEXT), *glow(pt.body, pt.lab, s=1.1), run_time=0.8)
        self.outro()


# ---------------------------------------------------------------------------------------------
class S03Adaptor(ZFilm):
    """the protein with no enzyme is Grb2: one SH2 cup, two SH3 claws that already hold Sos. (TAIL, then CLOSE)"""

    def construct(self):
        self.look_now(Z2, CEN2)
        st = s2_stage(with_ras=False)
        A = reader(phos_pos(1), 1.0, "enzyme", GREY, deg=SHUT, size=26, lcolor=TEXT)
        B = reader(phos_pos(2), 1.0, "no enzyme\nactivity", GREY, deg=SHUT, size=22, lcolor=TEXT)
        pt = partner(phos_pos(2), 1.0)
        self.add(*st.parts(), A, B, pt)

        self.at("One of those")
        self.play(FadeOut(A), run_time=0.5)
        self.at("no enzyme activity")
        self.play(Indicate(B.lab, color=TEXT, scale_factor=1.12), run_time=0.7)
        g_lab = T("Grb2", 30, TEAL, weight=BOLD).move_to(B.body)
        self.frac("at all", "It has", 0.4)            # "Grab two" is heard as one word, so cue on the words around it
        tall = reader(phos_pos(2), 1.0, "Grb2", TEAL, deg=SHUT, bh=BODY_HG)
        self.play(Transform(B.lab, g_lab), Transform(B.back, tall.back), Transform(B.body, tall.body), run_time=0.7)

        # let go of the tail and close in on the adaptor: it holds its partner with nothing gripped
        c2 = C_CLOSE
        gone = VGroup(*st.parts())
        movers = VGroup(B.back, B.body, B.lab, pt)
        self.at("It has")
        self.play(movers.animate.shift(RIGHT * 2.0), cup_anim(B, SHUT, OPEN), FadeOut(gone), self.look(Z3A, CEN3A),
                  run_time=1.3)

        sh2 = T("SH2 domain", 28, PINK, weight=BOLD).move_to(c2 + [0.0, 1.15, 0])
        lead = Line(sh2.get_bottom() + [-0.1, -0.05, 0], c2 + [0, CUP_OUT + 0.02, 0], color=PINK, stroke_width=3)
        self.frac("has one", "nothing else", 0.22)
        self.play(FadeIn(sh2, shift=DOWN * 0.1), Create(lead), Indicate(B.cup, color=TEXT, scale_factor=1.2), run_time=0.7)

        cl = claws(c2, 1.0)
        gapx = SOS_LEFT - CLAW_X0
        sh3 = T("SH3 domains", 28, ORANGE, weight=BOLD).move_to(c2 + [CLAW_X0 - 0.35, 1.15, 0])
        self.frac("has one", "nothing else", 0.6)
        tp = partner(c2, 1.0, gap=SOS_LEFT - CLAW_X0, ph=1.5)
        self.play(FadeOut(sh2), FadeOut(lead), Transform(pt.back, tp.back), Transform(pt.body, tp.body),
                  pt.lab.animate.shift(RIGHT * gapx), run_time=0.5)
        self.play(Create(cl), FadeIn(sh3, shift=DOWN * 0.1), run_time=0.7)
        ne = T("nothing else", 26, GREY).move_to(B.body.get_center() + [0, -BODY_HG / 2 - 0.4, 0])
        self.at("nothing else")
        self.play(FadeIn(ne, shift=UP * 0.1), Indicate(B.body, color=TEXT, scale_factor=1.04), run_time=0.8)

        # what an SH3 domain is: the camera backs off slowly while the claws take hold of short stretches on the partner
        self.at("another small")
        frame = self.camera.frame
        frame.add_updater(lambda m, dt: m.scale(1 + 0.016 * dt))
        self.play(FadeOut(ne), *glow(cl[0], cl[1], s=1.3, color=TEXT), run_time=0.8)
        tabs = sos(c2, 1.0).tabs.set_fill(GREY, 0.8)
        self.at("short stretches")
        self.play(FadeIn(tabs, shift=RIGHT * 0.2), *glow(cl[0], cl[1], s=1.2, color=TEXT), run_time=0.8)

        # the claws already hold Sos
        S = sos(c2, 1.0)
        self.at("already hold")
        self.play(*glow(cl[0], cl[1], s=1.2, color=TEXT), run_time=0.6)
        self.at("called")
        frame.clear_updaters()
        self.play(Transform(pt.back, S.back), Transform(pt.body, S.body), Transform(tabs, S.tabs), FadeOut(pt.lab),
                  FadeIn(S.lab, rate_func=lambda t: smooth(max(0.0, 2 * t - 1))),
                  FadeOut(sh3), self.look(Z3, CEN3), run_time=1.0)
        pt.remove(pt.lab)
        pt.add(S.lab)
        p_visit = pbadge().move_to(c2 + np.array([CLAW_X0, 1.1, 0]))
        self.at("with or")
        self.play(FadeIn(p_visit, scale=0.5), *glow(cl[0], cl[1], s=1.15, color=TEXT), run_time=0.5)
        self.at("without")
        self.play(FadeOut(p_visit), *glow(cl[0], cl[1], s=1.15, color=TEXT), run_time=0.5)

        # only the SH2 cup needs a phosphate
        self.at("Only the")
        p_cup = pbadge(PR * 1.4).move_to(c2 + np.array([-1.1, 0.0, 0]))
        self.play(FadeIn(p_cup, scale=0.5), run_time=0.4)
        self.play(p_cup.animate.move_to(c2), run_time=0.6)
        self.play(cup_anim(B, OPEN, SHUT), pop(p_cup, 1.25), run_time=0.5)

        # back out to the stage: the adaptor goes to just beside the tail
        st4 = Stage(gf=True, ps=(0, 1, 2), with_ras=False)
        asm = VGroup(B, cl, pt, tabs)
        self.outro(FadeOut(p_cup), cup_anim(B, SHUT, OPEN),
                   then=[asm.animate.shift(LEFT * 1.0), self.look_home(), FadeIn(VGroup(*st4.parts()))])


# ---------------------------------------------------------------------------------------------
def adaptor_group(c, k=1.0, deg=SHUT):
    """Grb2 and Sos together, as they stand at the tail."""
    B = reader(c, k, "Grb2", TEAL, deg=deg, size=28, lcolor=TEAL, bh=BODY_HG)
    S = sos(c, k)
    cl = claws(c, k)
    return B, cl, S


class S04Dock(ZFilm):
    """the cup clamps the phosphate on the tail; the receptor holds Grb2, Grb2 holds Sos; Sos stands against Ras. (STAGE)"""

    def construct(self):
        self.look_now(HOME_Z, HOME_C)
        st = Stage(gf=True, ps=(0, 1, 2), with_ras=False)
        B, cl, S = adaptor_group(PREDOCK, 1.0, OPEN)
        self.add(*st.parts(), S, B, cl)
        P3 = st.ps[2]
        asm = VGroup(B, cl, S)
        r1 = ring([PX - 0.05, YP[2], 0], 0.68)
        r2 = ring([C_DOCK[0] + CLAW_X0 + 0.55, YP[2], 0], 0.88)
        r3 = ring([C_DOCK[0] + SOS_RIGHT - 0.04, RAS_Y - 0.25, 0], 0.3)

        self.play(asm.animate.shift(LEFT * 1.0), run_time=1.0)
        self.at("clamps down")
        self.play(cup_anim(B, OPEN, SHUT), pop(P3, 1.35), run_time=0.7)
        self.at("receptor tail")
        self.play(*glow(st.rec.tail, st.rec.bar, s=1.0, color=TEXT), run_time=0.7)

        # the two holds, each drawn as it is named
        self.at("So the receptor holds")
        self.play(Create(r1), *glow(st.rec.tail, s=1.0, color=BLUE), *glow(B.body, s=1.08, color=TEAL), run_time=0.8)
        self.at("holds", nth=1)
        self.play(Create(r2), *glow(cl[0], cl[1], s=1.3, color=TEXT), *glow(S.body, s=1.03, color=PURPLE), run_time=0.9)

        r = ras()
        self.at("now stands at")
        self.play(FadeIn(r), run_time=0.8)
        contact = np.array([C_DOCK[0] + SOS_RIGHT, RAS_Y - 0.15, 0])
        self.at("where")
        self.play(Flash(contact, color=TEXT, line_length=0.3, flash_radius=0.38, num_lines=10), Create(r3),
                  Indicate(r.body, color=TEXT, scale_factor=1.1), run_time=0.8)

        # the message from the phosphate to Ras, by position alone: the holds light up in order
        self.at("one phosphatira")
        self.play(pop(P3, 1.4), run_time=0.5)
        self.at("positioning")
        self.play(pop(P3, 1.35),
                  LaggedStart(Indicate(B.cup, color=TEXT, scale_factor=1.1), Indicate(B.body, color=TEXT, scale_factor=1.05),
                              Indicate(cl, color=TEXT, scale_factor=1.15), Indicate(S.body, color=TEXT, scale_factor=1.03),
                              Indicate(r.body, color=TEXT, scale_factor=1.1), lag_ratio=0.4), run_time=2.2)
        self.at("Position is")
        self.play(Indicate(r.body, color=TEXT, scale_factor=1.12), Indicate(S.body, color=TEXT, scale_factor=1.03), run_time=0.9)
        self.outro(FadeOut(VGroup(r1, r2, r3)))


# ---------------------------------------------------------------------------------------------
class S05Flip(ZFilm):
    """Sos swaps GDP for GTP on Ras: off to on, no kinase; Grb2 never grips Ras. (STAGE)"""

    def construct(self):
        self.look_now(HOME_Z, HOME_C)
        st = Stage(gf=True, ps=(0, 1, 2))
        B, cl, S = adaptor_group(C_DOCK, 1.0, SHUT)
        self.add(*st.parts(), S, B, cl)
        r = st.ras

        self.at("has one task")
        self.play(Indicate(S.body, color=TEXT, scale_factor=1.03), Indicate(S.lab, color=TEXT, scale_factor=1.1), run_time=0.8)
        sos_c = S.body.get_center()
        exch = T("exchange\nfactor", 24, PURPLE, weight=BOLD, line_spacing=0.8).move_to(sos_c + [0, -0.95, 0])
        self.at("exchange factor")
        self.play(FadeIn(exch, shift=UP * 0.12), run_time=0.7)

        gdp = gdp_chip()
        tether = Line([RAS_X, RAS_Y - RAS_H / 2, 0], gdp.get_top(), color=GREY, stroke_width=4)
        self.at("swaps the")
        self.play(FadeIn(gdp, shift=UP * 0.15), Create(tether), run_time=0.7)
        gtp = gtp_chip().move_to([RAS_X + 2.0, RAS_Y - 1.05, 0])
        self.frac("swaps the", "flips", 0.55)
        self.play(FadeIn(gtp, shift=LEFT * 0.15), run_time=0.35)
        gtp_tether = Line([RAS_X, RAS_Y - RAS_H / 2, 0], [RAS_X, RAS_Y - 1.05 + 0.31, 0], color=GREEN, stroke_width=4)
        self.play(gdp.animate.shift(DOWN * 1.0).set_opacity(0), FadeOut(tether),
                  gtp.animate.move_to([RAS_X, RAS_Y - 1.05, 0]), Create(gtp_tether), run_time=0.9)

        on = T("on", 32, GREEN, weight=BOLD).move_to([RAS_X + 1.2, RAS_Y, 0])
        self.at("flips")
        self.play(*ras_to(r, GREEN), FadeIn(on, shift=RIGHT * 0.15), run_time=0.8)

        kin = ghost_chip("kinase").move_to([RAS_X + 2.0, RAS_Y - 1.05, 0])
        kx = strike(kin)
        self.at("no kinase")
        self.play(FadeIn(kin), run_time=0.4)
        self.play(Create(kx), run_time=0.4)

        # Grb2 never reaches Ras
        a, b, c = np.array([C_DOCK[0] + BODY_DX, YP[2] + BODY_HG / 2 + 0.03, 0]), None, None
        x_up = C_DOCK[0] + BODY_DX
        corner = np.array([x_up, RAS_Y + 0.3, 0])
        end = np.array([RAS_X - RAS_W / 2 - 0.08, RAS_Y + 0.3, 0])
        direct = DashedVMobject(VMobject().set_points_as_corners([a, corner, end]), num_dashes=40).set_color(GREY)
        self.at("never grips")
        self.play(FadeOut(VGroup(kin, kx)), Create(direct), run_time=1.0)
        xmark = cross_at([0.55, RAS_Y + 0.3, 0])
        self.at("at all")
        self.play(Create(xmark), direct.animate.set_color(RED), run_time=0.5)

        self.at("only holds")
        self.play(*glow(cl[0], cl[1], s=1.3, color=TEXT), *glow(S.body, s=1.03, color=PURPLE), run_time=0.8)
        contact = np.array([C_DOCK[0] + SOS_RIGHT, RAS_Y - 0.15, 0])
        self.at("which acts")
        self.play(Flash(contact, color=TEXT, line_length=0.3, flash_radius=0.38, num_lines=10),
                  Indicate(r.body, color=TEXT, scale_factor=1.08), run_time=0.8)
        self.outro(FadeOut(VGroup(direct, xmark, exch)))


# ---------------------------------------------------------------------------------------------
class S06Rule(ZFilm):
    """the whole chain: receptor holds Grb2, Grb2 holds Sos, position does the rest. (STAGE)"""

    def construct(self):
        self.look_now(HOME_Z, HOME_C)
        st = Stage(gf=True, ps=(0, 1, 2), ras_color=GREEN)
        B, cl, S = adaptor_group(C_DOCK, 1.0, SHUT)
        gtp = gtp_chip()
        gtp_tether = Line([RAS_X, RAS_Y - RAS_H / 2, 0], [RAS_X, RAS_Y - 1.05 + 0.31, 0], color=GREEN, stroke_width=4)
        self.add(*st.parts(), S, B, cl, gtp, gtp_tether)
        r = st.ras

        y = RAS_Y + 0.3
        x0, x1 = XR + 0.4, RAS_X - RAS_W / 2 - 0.1
        dim_line = DashedLine([x0, y, 0], [x1, y, 0], color=RED, stroke_width=5, dash_length=0.16)
        caps = VGroup(Line([x0, y - 0.2, 0], [x0, y + 0.2, 0], color=RED, stroke_width=5),
                      Line([x1, y - 0.2, 0], [x1, y + 0.2, 0], color=RED, stroke_width=5))
        never = T("never touched", 26, RED).move_to([-1.55, y - 0.45, 0])
        self.at("never touched")
        self.play(Create(dim_line), FadeIn(caps), FadeIn(never, shift=DOWN * 0.1), run_time=0.9)

        self.at("clamped a")
        self.play(FadeOut(dim_line), FadeOut(caps), FadeOut(never), pop(st.ps[2], 1.4), *glow(B.cup, s=1.3), run_time=0.8)
        self.at("already in its")
        self.play(*glow(cl[0], cl[1], s=1.3, color=TEXT), run_time=0.8)
        self.at("then flipped")
        self.play(Indicate(r.body, color=TEXT, scale_factor=1.12), Indicate(r.lab, color=TEXT, scale_factor=1.12), run_time=0.8)

        ad = T("adaptor", 32, TEAL, weight=BOLD).move_to([C_DOCK[0] + BODY_DX, -0.3, 0])
        self.at("is called an")
        self.play(FadeIn(ad, shift=DOWN * 0.1), Indicate(B.body, color=TEXT, scale_factor=1.05), run_time=0.8)
        ne = T("no enzyme\nactivity", 22, GREY, line_spacing=0.8).move_to([C_DOCK[0] + BODY_DX, -0.95, 0])
        self.at("no enzyme")
        self.play(FadeIn(ne, shift=DOWN * 0.1), run_time=0.6)
        two_l = T("partner", 24, GREY).move_to([XR - 0.95, YP[2], 0])
        two_r = T("partner", 24, GREY).move_to([C_DOCK[0] + SOS_LEFT + SOS_W / 2, C_DOCK[1] + SOS_DY + SOS_H / 2 + 0.32, 0])
        self.at("links two")
        self.play(FadeIn(two_l, shift=RIGHT * 0.1), FadeIn(two_r, shift=DOWN * 0.1),
                  *glow(st.rec.tail, s=1.0, color=TEAL), *glow(S.body, s=1.03, color=TEAL), run_time=0.9)

        # the rule: three holds, one after another
        r1 = ring([PX - 0.05, YP[2], 0], 0.68)
        r2 = ring([C_DOCK[0] + CLAW_X0 + 0.55, YP[2], 0], 0.88)
        r3 = ring([C_DOCK[0] + SOS_RIGHT - 0.04, RAS_Y - 0.25, 0], 0.3)
        self.at("Keep this")
        self.play(FadeOut(ad), FadeOut(ne), FadeOut(two_l), FadeOut(two_r), run_time=0.5)
        self.at("the receptor holds")
        self.play(Create(r1), run_time=0.7)
        self.at("holds", nth=1)
        self.play(Create(r2), run_time=0.7)
        self.at("position is")
        self.play(Create(r3), Indicate(r.body, color=TEXT, scale_factor=1.1), run_time=0.9)
        self.finish()


class S07End(EndCard):
    LINE = "The receptor holds Grb2, Grb2 holds Sos, position is the first step."
