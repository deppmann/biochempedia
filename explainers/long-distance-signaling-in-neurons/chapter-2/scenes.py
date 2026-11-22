"""
Courier or Relay? Testing What Travels
Lesson: Long-Distance Signaling in Neurons (Chapter 2)

COLOUR MAP (one colour per concept for the whole film):
- Membrane / axon & cell-body boundary : MEMBRANE (#CBD5E1, slate-white)
- Cytoplasm fill                       : CYTO     (#263248, dark slate-blue)
- Nucleus / cell body interior         : NUCLEUS  (#6C72E8, indigo; dim when inactive, bright when CREB active)
- Microtubule tracks                   : BLUE     (#58C4DD, steel-blue; minus end left, plus end right)
- NGF (survival ligand)                : GOLD     (#D4A843, gold)
- TrkA receptor                        : TEAL     (#3FB8C0, teal)
- Active TrkA kinase / relay signal    : KINASE   (#E86CD0, magenta)
- Dynein motor                         : GREEN    (#83C167, emerald)
- Block / inhibitor / antibody / fail  : RED      (#FC6255, crimson)
- Barriers / dividers                  : BARRIER_COL (#CBD5E1, schematic slate-white)
- Labels / text                        : TEXT     (#E8EAF0, full-opacity off-white)

CARRIED WORLD:
A schematic sympathetic neuron (cell body and indigo nucleus on the left, long axon with steel-blue
microtubule spanning to the NGF-bathed tip on the right), which in s01 splits vertically into two
identical parallel axon tracks (top: Courier, bottom: Relay) kept at fixed coordinates through s08,
and shown side by side in miniature in s09.

WHAT CHANGES IN EACH SPOKEN SCENE (computed from the lesson):
- s01_bridge_hook   : Dynein steps leftward driving the NGF-TrkA endosome along the 1 cm axon (distance &
                      hours computed from v = 1 um/s -> 2.8 h), the axon splits into two parallel tracks
                      with '?', and a local relay wave marches leftward on the bottom track.
- s02_two_models    : Top courier endosome moves linearly from tip to nucleus (u_c: 0 -> 1); bottom relay
                      wave propagates across 5 axon stretches (u_r: 0 -> 5); both nuclei light CREB.
- s03_dynein_predict: Both tracks race to the cell body on time (0 -> 2.8 h); tracks reset, crimson X
                      locks over dynein, NGF stays at tips, nuclei dim ('Neurons die'), predict card shows.
- s05_dynein_reveal : Question card clears; courier halts near tip under X; tiny dyneins appear at each
                      relay stretch, lock under X marks, and halt the brigade; both nuclei dim ('Dies').
- s06_middle_setup  : X marks clear; two vertical barriers drop across both tracks creating 3 chambers;
                      crimson TrkA inhibitor wash fills only the center chamber.
- s07_middle_outcome: Relay wave hops into the middle chamber and decays to zero in the inhibitor; courier
                      vesicle crosses the middle chamber with kinase glow dimmed and NGF locked inside,
                      then relights kinase and illuminates the left nucleus in the drug-free cell body.
- s08_neutralize_ngf: Observed result tag appears; middle wash clears; crimson Y antibodies in the left
                      chamber bind arriving NGF, extinguishing kinase glow and dimming the nucleus.
- s09_takeaway      : TwoPanel miniature runs both experiments live: left shows dynein block halting both
                      tracks; right shows middle TrkA block splitting courier survival from relay failure.
"""

from bp_parts import *

# ------------------------------------------------------------------ Colour map
MEMBRANE = "#CBD5E1"
CYTO = "#263248"
NUCLEUS = "#6C72E8"
KINASE = "#E86CD0"
NGF_COL = GOLD
TRKA_COL = TEAL
DYNEIN_COL = GREEN
MT_COL = BLUE
BLOCK_COL = RED
BARRIER_COL = "#CBD5E1"

# ------------------------------------------------------------------ Shared world coordinates
SOMA_X = -4.65
SOMA_R = 0.80
NUC_R = 0.42
AXON_X0 = -4.00
AXON_X1 = 4.95
AXON_HH = 0.39
TIP_X = 5.34
TIP_R = 0.54

TOP_Y = 1.58
BOT_Y = -1.06
SINGLE_Y = 0.26

BAR_X1 = -1.75
BAR_X2 = 1.95
CHAMBER_TOP = 2.86
CHAMBER_BOT = -2.02

TRACK_RIGHT_X = 4.55
TRACK_LEFT_X = -3.45


# ------------------------------------------------------------------ Shared builders
def make_polarity_mark(kind, pos, color=MT_COL, size=0.11):
    """Geometric + or - microtubule polarity marker (no tiny Text)."""
    h = Line(pos + LEFT * size, pos + RIGHT * size, color=color, stroke_width=3.2)
    if kind == "-":
        return VGroup(h)
    v = Line(pos + DOWN * size, pos + UP * size, color=color, stroke_width=3.2)
    return VGroup(h, v)


def make_neuron_track(y, nuc_lit=0.28, ngf_at_tip=True, show_mt=True):
    """Build one schematic sympathetic neuron track (soma left, axon spanning to tip right)."""
    soma_c = np.array([SOMA_X, y, 0.0])

    # Cytoplasm interior fills (explicit CYTO fill_color on every circle/rect so opacity changes never leak default RED)
    axon_fill = Rectangle(width=AXON_X1 - AXON_X0 + 0.15, height=AXON_HH * 2,
                          stroke_width=0, fill_color=CYTO, fill_opacity=0.68).move_to(
        [(AXON_X0 + AXON_X1) / 2, y, 0.0]
    )
    tip_fill = Circle(radius=TIP_R, stroke_width=0, fill_color=CYTO, fill_opacity=0.68).move_to([TIP_X, y, 0])
    soma_fill = Circle(radius=SOMA_R, stroke_width=0, fill_color=CYTO, fill_opacity=0.75).move_to(soma_c)

    soma_ring = Circle(radius=SOMA_R, stroke_color=MEMBRANE, stroke_width=3.8,
                       fill_color=CYTO, fill_opacity=0.0).move_to(soma_c)
    top_wall = Line([AXON_X0, y + AXON_HH, 0], [AXON_X1, y + AXON_HH, 0], color=MEMBRANE, stroke_width=3.6)
    bot_wall = Line([AXON_X0, y - AXON_HH, 0], [AXON_X1, y - AXON_HH, 0], color=MEMBRANE, stroke_width=3.6)
    tip_arc = Arc(radius=TIP_R, start_angle=-PI * 0.72, angle=PI * 1.44, arc_center=[TIP_X, y, 0],
                  stroke_color=MEMBRANE, stroke_width=3.6, fill_opacity=0)
    top_join = Line([AXON_X1, y + AXON_HH, 0], tip_arc.get_start() if tip_arc.get_start()[1] > y else tip_arc.get_end(),
                    color=MEMBRANE, stroke_width=3.6)
    bot_join = Line([AXON_X1, y - AXON_HH, 0], tip_arc.get_end() if tip_arc.get_end()[1] < y else tip_arc.get_start(),
                    color=MEMBRANE, stroke_width=3.6)

    nuc = Circle(radius=NUC_R, stroke_color=NUCLEUS, stroke_width=3.5,
                 fill_color=NUCLEUS, fill_opacity=nuc_lit).move_to(soma_c)

    mt_grp = VGroup()
    if show_mt:
        mt_y = y - 0.16
        mt = Line([AXON_X0 + 0.15, mt_y, 0], [AXON_X1 + 0.10, mt_y, 0], color=MT_COL, stroke_width=4.2)
        minus = make_polarity_mark("-", np.array([AXON_X0 - 0.04, mt_y, 0]), color=MT_COL, size=0.08)
        plus = make_polarity_mark("+", np.array([AXON_X1 + 0.30, mt_y, 0]), color=MT_COL, size=0.08)
        mt_grp.add(mt, minus, plus)

    tip_ngf = VGroup()
    if ngf_at_tip:
        for dx, dy in [(0.16, 0.24), (0.34, -0.02), (0.14, -0.26), (0.42, 0.20)]:
            tip_ngf.add(Dot([TIP_X + dx, y + dy, 0], radius=0.072, color=NGF_COL))

    g = VGroup(axon_fill, tip_fill, soma_fill, soma_ring, top_wall, bot_wall,
               tip_arc, top_join, bot_join, mt_grp, nuc, tip_ngf)
    g.nuc = nuc
    g.tip_ngf = tip_ngf
    g.mt = mt_grp
    g.fills = VGroup(axon_fill, tip_fill, soma_fill)
    g.walls = VGroup(soma_ring, top_wall, bot_wall, tip_arc, top_join, bot_join)
    return g


def dim_track(track, factor=0.40):
    """Dim a track's membrane, microtubule and fills without ever turning circles red or greying text."""
    return AnimationGroup(
        track.fills.animate.set_fill(opacity=0.22 * factor),
        track.walls.animate.set_stroke(opacity=factor),
        track.mt.animate.set_stroke(opacity=factor),
        track.tip_ngf.animate.set_opacity(factor),
    )


def make_cross(center, size=0.26, color=BLOCK_COL, width=5.5):
    """Crisp crimson X mark."""
    c = np.array(center, dtype=float)
    return VGroup(
        Line(c + [-size, -size, 0], c + [size, size, 0], color=color, stroke_width=width),
        Line(c + [-size, size, 0], c + [size, -size, 0], color=color, stroke_width=width),
    )


def make_dynein(foot_pos, phase=0.0, blocked=False, scale=1.0, pulse_amp=0.0):
    """Emerald dynein motor walking leftward along the microtubule."""
    p = np.array(foot_pos, dtype=float)
    step = 0.0 if blocked else 0.08 * np.sin(phase)
    s1 = Line(p + UP * 0.16 * scale, p + LEFT * (0.08 + step) * scale, color=DYNEIN_COL, stroke_width=3.8 * scale)
    s2 = Line(p + UP * 0.16 * scale, p + RIGHT * (0.08 - step) * scale, color=DYNEIN_COL, stroke_width=3.8 * scale)
    head = Circle(radius=0.095 * scale, stroke_color=DYNEIN_COL, stroke_width=2.8 * scale,
                  fill_color=DYNEIN_COL, fill_opacity=0.88).move_to(p + UP * 0.19 * scale)
    g = VGroup(s1, s2, head)
    if blocked:
        g.add(make_cross(p + UP * 0.16 * scale, size=0.22 * scale, width=(5.5 + pulse_amp)))
    return g


def make_endosome(x, y, kinase=1.0, has_dynein=True, dynein_blocked=False, phase=0.0, ngf_bound=True,
                  scale=1.0, pulse_amp=0.0, wake=True):
    """Signaling endosome: vesicle holding gold NGF inside teal TrkA, magenta kinase field, emerald dynein."""
    mt_y = y - 0.16 * scale
    vc = np.array([x, y + 0.12 * scale, 0.0])
    r = 0.24 * scale

    g = VGroup()
    if kinase > 0.06:
        if wake:
            # Local active cytoplasmic kinase field around the traveling endosome
            halo = Rectangle(width=1.15 * scale, height=0.68 * scale, stroke_width=0,
                             fill_color=KINASE, fill_opacity=0.22 * min(1.0, kinase)).move_to([x, y, 0])
            g.add(halo)
        glow = Circle(radius=r * 1.48, stroke_color=KINASE, stroke_width=4.4 * scale * kinase,
                      fill_color=KINASE, fill_opacity=0.32 * kinase).move_to(vc)
        g.add(glow)

    vesicle = Circle(radius=r, stroke_color=MEMBRANE, stroke_width=2.8 * scale,
                     fill_color=BG, fill_opacity=0.94).move_to(vc)
    g.add(vesicle)

    # Teal TrkA receptor gripping NGF inside vesicle, kinase tail extending outside
    trka_in = Arc(radius=r * 0.48, start_angle=-PI * 0.2, angle=PI * 1.4, arc_center=vc,
                  stroke_color=TRKA_COL, stroke_width=3.4 * scale)
    trka_tail = Line(vc + UP * r * 0.85, vc + UP * r * 1.38, color=TRKA_COL, stroke_width=3.8 * scale)
    k_tip = Dot(vc + UP * r * 1.42, radius=0.062 * scale,
                color=KINASE if kinase > 0.2 else GREY).set_opacity(max(0.45, kinase))
    g.add(trka_in, trka_tail, k_tip)

    if ngf_bound:
        ngf_pair = VGroup(
            Dot(vc + LEFT * 0.05 * scale, radius=0.068 * scale, color=NGF_COL),
            Dot(vc + RIGHT * 0.05 * scale, radius=0.068 * scale, color=NGF_COL),
        )
        g.add(ngf_pair)

    if has_dynein:
        g.add(make_dynein([x, mt_y, 0.0], phase=phase, blocked=dynein_blocked, scale=scale, pulse_amp=pulse_amp))

    return g


def make_tip_trka(y, x=4.68, active=1.0):
    """Fixed TrkA + NGF anchored at the right axon tip (Relay model)."""
    c = np.array([x, y + 0.04, 0.0])
    g = VGroup()
    if active > 0.05:
        g.add(Circle(radius=0.25, stroke_color=KINASE, stroke_width=3.5 * active,
                     fill_color=KINASE, fill_opacity=0.28 * active).move_to(c))
    g.add(RoundedRectangle(corner_radius=0.07, width=0.16, height=0.38, stroke_color=TRKA_COL,
                           stroke_width=2.8, fill_color=TRKA_COL, fill_opacity=0.55).move_to(c))
    g.add(Dot(c + RIGHT * 0.16, radius=0.075, color=NGF_COL))
    return g


RELAY_XS = [4.25, 2.70, 1.15, -0.40, -1.95, -3.50]


def make_relay_pulses(y, progress, amp=1.0):
    """Bucket-brigade magenta wave lighting each active axon stretch leftward across RELAY_XS."""
    g = VGroup()
    if amp <= 0.02:
        return g
    for i, px in enumerate(RELAY_XS):
        dist = abs(progress - i)
        if dist < 1.15:
            strength = amp * float(np.exp(-(dist / 0.55) ** 2))
            if strength > 0.05:
                # Active local stretch glow band inside the axon
                band = Rectangle(width=1.10, height=AXON_HH * 1.65, stroke_width=0,
                                 fill_color=KINASE, fill_opacity=0.30 * strength).move_to([px, y, 0])
                ring = Circle(radius=0.17 + 0.09 * (1.0 - strength), stroke_color=KINASE,
                              stroke_width=4.0 * strength, fill_color=KINASE,
                              fill_opacity=0.40 * strength).move_to([px, y + 0.05, 0])
                g.add(band, ring)
        if i < len(RELAY_XS) - 1:
            if i - 0.1 <= progress <= i + 1.1:
                hop_alpha = amp * float(np.clip(1.0 - abs(progress - (i + 0.5)) * 1.4, 0.0, 1.0))
                if hop_alpha > 0.06:
                    arc = CurvedArrow([px - 0.15, y + 0.18, 0], [RELAY_XS[i + 1] + 0.15, y + 0.18, 0],
                                      angle=0.55, color=KINASE, stroke_width=3.6 * hop_alpha,
                                      tip_length=0.15).set_opacity(hop_alpha)
                    g.add(arc)
    return g


def make_antibody(pos, angle=0.0, scale=1.0):
    """Schematic crimson Y-shaped neutralizing antibody."""
    stem = Line(DOWN * 0.16 * scale, ORIGIN, color=BLOCK_COL, stroke_width=4.2 * scale)
    arm_l = Line(ORIGIN, np.array([-0.14, 0.16, 0.0]) * scale, color=BLOCK_COL, stroke_width=4.2 * scale)
    arm_r = Line(ORIGIN, np.array([0.14, 0.16, 0.0]) * scale, color=BLOCK_COL, stroke_width=4.2 * scale)
    g = VGroup(stem, arm_l, arm_r)
    if angle:
        g.rotate(angle, about_point=ORIGIN)
    return g.move_to(pos)


def make_chambers(with_inhibitor=True):
    """Two vertical Campenot barriers dividing both tracks into 3 chambers, plus optional middle inhibitor wash."""
    b1 = Line([BAR_X1, CHAMBER_BOT, 0], [BAR_X1, CHAMBER_TOP, 0], color=BARRIER_COL, stroke_width=5)
    b2 = Line([BAR_X2, CHAMBER_BOT, 0], [BAR_X2, CHAMBER_TOP, 0], color=BARRIER_COL, stroke_width=5)
    h1 = T("Cell body", 26, TEXT).move_to([(-6.35 + BAR_X1) / 2, 3.36, 0])
    h2 = T("Middle axon", 26, TEXT).move_to([(BAR_X1 + BAR_X2) / 2, 3.36, 0])
    h3 = T("Axon tip", 26, TEXT).move_to([(BAR_X2 + 6.10) / 2, 3.36, 0])
    g = VGroup(b1, b2, h1, h2, h3)
    g.barriers = VGroup(b1, b2)
    g.headers = VGroup(h1, h2, h3)
    if with_inhibitor:
        wash = Rectangle(width=BAR_X2 - BAR_X1 - 0.08, height=CHAMBER_TOP - CHAMBER_BOT - 0.08,
                         stroke_width=0, fill_color=BLOCK_COL, fill_opacity=0.22).move_to(
            [(BAR_X1 + BAR_X2) / 2, (CHAMBER_TOP + CHAMBER_BOT) / 2, 0])
        wash.layout_ok = True
        tag = boxed_label("TrkA inhibitor", BLOCK_COL, size=26, pad=0.14).move_to(
            [(BAR_X1 + BAR_X2) / 2, 0.28, 0])
        g.wash = wash
        g.inhib_tag = tag
        g.add(wash, tag)
    return g


def make_world_tracks(top_nuc=0.28, bot_nuc=0.28, label_y_bot=0.20):
    """Build the carried two-track world (Courier on top, Relay on bottom) with labels inside left chamber."""
    top_t = make_neuron_track(TOP_Y, nuc_lit=top_nuc)
    bot_t = make_neuron_track(BOT_Y, nuc_lit=bot_nuc)
    l_cour = T("Courier", 28, TEXT).move_to([-6.35, 2.66, 0], aligned_edge=LEFT)
    l_rel = T("Relay", 28, TEXT).move_to([-6.35, label_y_bot, 0], aligned_edge=LEFT)
    g = VGroup(top_t, bot_t, l_cour, l_rel)
    g.top = top_t
    g.bot = bot_t
    g.l_cour = l_cour
    g.l_rel = l_rel
    return g


def build_predict_backdrop():
    """Exact frozen world at the end of s03_dynein_predict, reused by S04Pause."""
    w = make_world_tracks(top_nuc=0.28, bot_nuc=0.28)
    endo = make_endosome(TRACK_RIGHT_X - 0.15, TOP_Y, kinase=0.9, has_dynein=True, dynein_blocked=True)
    tip_r = make_tip_trka(BOT_Y, active=1.0)
    ngf_tag = boxed_label("NGF at tip only", NGF_COL, size=24, pad=0.12).move_to([4.6, 2.62, 0])
    obs_die = boxed_label("Observed: neurons die", TEXT, size=24, pad=0.12).move_to([0.0, 0.26, 0])
    return VGroup(w, endo, tip_r, ngf_tag, obs_die)


# ------------------------------------------------------------------ Scenes
class S00Title(TitleCard):
    LESSON = "Long-Distance Signaling in Neurons"
    TITLE = "Courier or Relay? Testing What Travels"


class S01BridgeHook(SpokenScene):
    def construct(self):
        # Single sympathetic neuron from Film 1 with 1 cm distance bar & computed transport readout (1 cm / 1 um/s -> 2.8 h)
        single = make_neuron_track(SINGLE_Y, nuc_lit=0.32)
        stag = scope_tag("schematic", size=24, color=TEXT)
        scale_line = Line([TRACK_LEFT_X, SINGLE_Y - 0.85, 0], [TRACK_RIGHT_X, SINGLE_Y - 0.85, 0], color=TEXT, stroke_width=2.5)
        tick_l = Line([TRACK_LEFT_X, SINGLE_Y - 0.96, 0], [TRACK_LEFT_X, SINGLE_Y - 0.74, 0], color=TEXT, stroke_width=2.5)
        tick_r = Line([TRACK_RIGHT_X, SINGLE_Y - 0.96, 0], [TRACK_RIGHT_X, SINGLE_Y - 0.74, 0], color=TEXT, stroke_width=2.5)
        cm_lbl = T("1 cm", 26, TEXT).next_to(scale_line, DOWN, buff=0.14)
        scale_grp = VGroup(scale_line, tick_l, tick_r, cm_lbl)

        u = ValueTracker(0.0)
        prog_bar = always_redraw(lambda: Line(
            [TRACK_RIGHT_X, SINGLE_Y - 0.85, 0],
            [TRACK_RIGHT_X + (TRACK_LEFT_X - TRACK_RIGHT_X) * u.get_value(), SINGLE_Y - 0.85, 0],
            color=DYNEIN_COL, stroke_width=6
        ))
        ro = Readout(
            [("distance", lambda: 1.0 * u.get_value(), "{:4.2f} cm", DYNEIN_COL),
             ("elapsed", lambda: 2.78 * u.get_value(), "{:4.1f} h", TEXT)],
            at=[3.85, 2.45, 0], widest=[1.00, 2.78], size=26, title="at 1 µm/s"
        )
        endo = always_redraw(lambda: make_endosome(
            TRACK_RIGHT_X + (TRACK_LEFT_X - TRACK_RIGHT_X) * u.get_value(),
            SINGLE_Y,
            kinase=1.0,
            has_dynein=True,
            phase=u.get_value() * 34.0,
        ))
        self.add(single, scale_grp, prog_bar, ro, stag, endo)

        # Glide leftward continuously across full 1 cm as narrator describes dynein crossing 1 cm in hours
        self.at("The first film")
        self.play(u.animate(rate_func=linear).set_value(1.0), run_time=4.9)
        self.wait(1.6)
        self.play(FadeOut(scale_grp), FadeOut(ro), FadeOut(prog_bar), FadeOut(endo), run_time=0.45)

        # Smoothly split vertically into two parallel axon tracks
        self.at("Since a relay")
        top_t = make_neuron_track(TOP_Y, nuc_lit=0.28)
        bot_t = make_neuron_track(BOT_Y, nuc_lit=0.28)
        single_top = single.copy()
        single_bot = single.copy()
        self.remove(single)
        self.add(single_top, single_bot)

        u_top = ValueTracker(0.0)
        endo_top = always_redraw(lambda: make_endosome(
            TRACK_RIGHT_X + (TRACK_LEFT_X - TRACK_RIGHT_X) * u_top.get_value(),
            TOP_Y,
            kinase=1.0,
            has_dynein=True,
            phase=u_top.get_value() * 34.0,
        ))
        tip_bot = make_tip_trka(BOT_Y, active=1.0)
        q_mark = boxed_label("?", NGF_COL, size=42, pad=0.22).move_to([0.4, 0.26, 0])

        self.play(
            Transform(single_top, top_t),
            Transform(single_bot, bot_t),
            run_time=1.8,
        )
        self.remove(single_top, single_bot)
        self.add(top_t, bot_t)
        self.play(FadeIn(endo_top), FadeIn(tip_bot), FadeIn(q_mark), run_time=0.5)

        self.at("whether the receptor")
        self.play(u_top.animate(rate_func=linear).set_value(0.55), run_time=3.2)

        # Bottom track shows local signals marching home while receptor stays at tip
        self.at("Or does it stay")
        r_prog = ValueTracker(0.0)
        pulses = always_redraw(lambda: make_relay_pulses(BOT_Y, r_prog.get_value(), amp=1.0))
        self.add(pulses)
        self.play(
            u_top.animate(rate_func=linear).set_value(1.0),
            r_prog.animate(rate_func=linear).set_value(5.0),
            run_time=3.6,
        )
        self.finish()


class S02TwoModels(SpokenScene):
    def construct(self):
        w = make_world_tracks(top_nuc=0.25, bot_nuc=0.25)
        stag = scope_tag("schematic", size=24, color=TEXT)
        u_c = ValueTracker(0.0)
        tip_pulse = ValueTracker(0.4)
        endo = always_redraw(lambda: make_endosome(
            TRACK_RIGHT_X + (TRACK_LEFT_X - TRACK_RIGHT_X) * u_c.get_value(),
            TOP_Y, kinase=0.55 + 0.45 * tip_pulse.get_value(), has_dynein=True, phase=u_c.get_value() * 34.0
        ))
        tip_r = always_redraw(lambda: make_tip_trka(BOT_Y, active=0.55 + 0.45 * tip_pulse.get_value()))
        r_prog = ValueTracker(-0.8)
        pulses = always_redraw(lambda: make_relay_pulses(BOT_Y, r_prog.get_value(), amp=1.0))

        self.add(w.top, w.bot, stag, endo, tip_r, pulses)

        # Introduce labels & NGF activation at the tip during opening sentence
        self.play(FadeIn(w.l_cour), FadeIn(w.l_rel), run_time=1.0)
        self.play(tip_pulse.animate(rate_func=there_and_back).set_value(1.0), run_time=3.1)

        self.at("In the courier model")
        self.play(u_c.animate(rate_func=linear).set_value(1.0), run_time=6.8)

        self.at("In the relay model")
        stay_tag = boxed_label("TrkA stays at tip", TRKA_COL, size=24, pad=0.12).move_to([4.05, 0.20, 0])
        self.play(FadeIn(stay_tag), tip_pulse.animate(rate_func=there_and_back).set_value(1.0), run_time=3.2)

        self.at("Like a bucket brigade")
        self.play(r_prog.animate(rate_func=linear).set_value(5.0), run_time=4.8)

        self.at("Both wake")
        creb_top = boxed_label("CREB active", KINASE, size=24, pad=0.12).move_to([-1.90, 2.66, 0], aligned_edge=RIGHT)
        creb_bot = boxed_label("CREB active", KINASE, size=24, pad=0.12).move_to([-1.90, 0.20, 0], aligned_edge=RIGHT)
        self.play(
            w.top.nuc.animate.set_fill(NUCLEUS, opacity=0.88),
            w.bot.nuc.animate.set_fill(NUCLEUS, opacity=0.88),
            FadeIn(creb_top),
            FadeIn(creb_bot),
            run_time=0.7,
        )
        self.finish()


class S03DyneinPredict(SpokenScene):
    def construct(self):
        w = make_world_tracks(top_nuc=0.28, bot_nuc=0.28)
        u_c = ValueTracker(0.0)
        r_prog = ValueTracker(0.0)
        t_clock = ValueTracker(0.0)
        clk = Readout(
            [("arrival", lambda: t_clock.get_value(), "{:4.1f} h", TEXT)],
            at=[4.35, 2.88, 0], widest=[2.78], size=26
        )
        endo = always_redraw(lambda: make_endosome(
            TRACK_RIGHT_X + (TRACK_LEFT_X - TRACK_RIGHT_X) * u_c.get_value(),
            TOP_Y, kinase=1.0, has_dynein=True, phase=u_c.get_value() * 30.0
        ))
        tip_r = make_tip_trka(BOT_Y, active=1.0)
        pulses = always_redraw(lambda: make_relay_pulses(BOT_Y, r_prog.get_value(), amp=1.0))
        self.add(w, clk, endo, tip_r, pulses)

        self.at("Timing alone cannot choose")
        self.play(
            u_c.animate(rate_func=linear).set_value(1.0),
            r_prog.animate(rate_func=linear).set_value(5.0),
            t_clock.animate(rate_func=linear).set_value(2.78),
            run_time=5.8,
        )

        # Reset tracks to start of experiment, disable dynein with crimson X
        self.at("disable the motor dynein")
        self.remove(endo, pulses)
        xpulse = ValueTracker(0.0)
        endo_locked = always_redraw(lambda: make_endosome(
            TRACK_RIGHT_X - 0.15, TOP_Y, kinase=0.9, has_dynein=True, dynein_blocked=True,
            pulse_amp=2.2 * np.sin(xpulse.get_value() * PI)
        ))
        self.play(FadeOut(clk, run_time=0.5), FadeIn(endo_locked), run_time=1.8)

        self.at("give NGF only")
        ngf_tag = boxed_label("NGF at tip only", NGF_COL, size=24, pad=0.12).move_to([4.6, 2.62, 0])
        self.play(FadeIn(ngf_tag), xpulse.animate(rate_func=linear).set_value(1.0), run_time=1.1)

        self.at("the neurons die")
        obs_die = boxed_label("Observed: neurons die", TEXT, size=24, pad=0.12).move_to([0.0, 0.26, 0])
        self.play(FadeIn(obs_die), run_time=0.85)

        self.at("Predict")
        q = question_card("Does blocking dynein prove a courier?", y=-3.05, size=30, color=GOLD)
        # Highlight ring around the blocked dynein motor while the predict question is posed
        lock_ring = always_redraw(lambda: Circle(
            radius=0.34 + 0.08 * np.sin(xpulse.get_value() * TAU),
            stroke_color=BLOCK_COL, stroke_width=3.5, fill_opacity=0
        ).move_to([TRACK_RIGHT_X - 0.15, TOP_Y - 0.02, 0]))
        self.play(FadeIn(q), run_time=0.7)
        self.add(lock_ring)
        xpulse.set_value(0.0)
        self.play(xpulse.animate(rate_func=linear).set_value(2.0), run_time=4.6)
        self.remove(lock_ring)
        self.finish()


class S04Pause(PredictPause):
    QUESTION = "Does blocking dynein prove a courier?"
    SECONDS = 4.5
    CARD = {"y": -3.05, "size": 30, "color": GOLD}
    RING_AT = (5.9, -3.05, 0)

    def backdrop(self):
        return build_predict_backdrop()


class S05DyneinReveal(SpokenScene):
    def construct(self):
        w = make_world_tracks(top_nuc=0.28, bot_nuc=0.28)
        ngf_tag = boxed_label("NGF at tip only", NGF_COL, size=24, pad=0.12).move_to([4.6, 2.62, 0])
        obs_die = boxed_label("Observed: neurons die", TEXT, size=24, pad=0.12).move_to([0.0, 0.26, 0])
        q = question_card("Does blocking dynein prove a courier?", y=-3.05, size=30, color=GOLD)
        tip_r = make_tip_trka(BOT_Y, active=1.0)

        u_c = ValueTracker(0.01875)
        c_blocked = ValueTracker(1.0)
        endo_live = always_redraw(lambda: make_endosome(
            TRACK_RIGHT_X + (TRACK_LEFT_X - TRACK_RIGHT_X) * u_c.get_value(),
            TOP_Y, kinase=0.9, has_dynein=True,
            dynein_blocked=(c_blocked.get_value() > 0.5),
            phase=u_c.get_value() * 24.0,
        ))
        self.add(w, ngf_tag, obs_die, q, tip_r, endo_live)

        # Clear question card & observed-outcome chip immediately on "No"
        ans_tag = boxed_label("No — both can need dynein", BLOCK_COL, size=26, pad=0.14).move_to([0.0, -3.05, 0])
        self.play(
            FadeOut(obs_die, run_time=0.5),
            swap(q, ans_tag, run_time=1.0),
        )

        # Courier remains locked near tip under crimson X; top nucleus dims
        self.at("Blocking it stops")
        dies_t = boxed_label("Dies", BLOCK_COL, size=24, pad=0.12).move_to([-1.90, 2.66, 0], aligned_edge=RIGHT)
        self.play(
            u_c.animate(rate_func=linear).set_value(0.05625),
            w.top.nuc.animate.set_fill(NUCLEUS, opacity=0.12),
            FadeIn(dies_t),
            run_time=1.8,
        )

        # Relay reveals tiny dyneins assisting each local stretch
        self.at("But a relay")
        hyp_tag = T("if each local step needs dynein", 24, DYNEIN_COL).move_to([2.1, -2.08, 0])
        local_dyns = VGroup(*[
            make_dynein([px - 0.55, BOT_Y - 0.16, 0], blocked=False, scale=0.84)
            for px in RELAY_XS[:-1]
        ])
        r_prog = ValueTracker(0.0)
        r_amp = ValueTracker(1.0)
        pulses = always_redraw(lambda: make_relay_pulses(BOT_Y, r_prog.get_value(), amp=r_amp.get_value()))
        self.add(pulses)
        self.play(FadeIn(hyp_tag), FadeIn(local_dyns), run_time=1.4)
        self.play(r_prog.animate(rate_func=linear).set_value(0.85), run_time=4.0)

        # Block every local dynein -> brigade halts completely
        self.at("If each local step")
        local_xs = VGroup(*[
            make_cross([px - 0.55, BOT_Y - 0.02, 0], size=0.19)
            for px in RELAY_XS[:-1]
        ])
        dies_b = boxed_label("Dies", BLOCK_COL, size=24, pad=0.12).move_to([-1.90, 0.20, 0], aligned_edge=RIGHT)
        self.play(
            LaggedStart(*[FadeIn(x) for x in local_xs], lag_ratio=0.15),
            r_amp.animate.set_value(0.0),
            w.bot.nuc.animate.set_fill(NUCLEUS, opacity=0.12),
            FadeIn(dies_b),
            run_time=3.4,
        )

        self.at("Both models predict death")
        verdict = boxed_label("Same prediction — inconclusive", GOLD, size=28, pad=0.16).move_to([0.0, -3.05, 0])
        self.play(swap(ans_tag, verdict, run_time=1.4))
        self.finish()


class S06MiddleSetup(SpokenScene):
    def construct(self):
        w = make_world_tracks(top_nuc=0.14, bot_nuc=0.14)
        endo = make_endosome(TRACK_RIGHT_X - 0.45, TOP_Y, kinase=0.95, has_dynein=True, dynein_blocked=True)
        tip_r = make_tip_trka(BOT_Y, active=1.0)
        local_xs = VGroup(*[
            make_dynein([px - 0.55, BOT_Y - 0.16, 0], blocked=True, scale=0.84)
            for px in RELAY_XS[:-1]
        ])
        verdict = boxed_label("Same prediction — inconclusive", GOLD, size=28, pad=0.16).move_to([0.0, -3.05, 0])
        self.add(w, endo, tip_r, local_xs, verdict)

        # Clear old dynein X marks and verdict right away as narrator opens
        endo_free = make_endosome(TRACK_RIGHT_X, TOP_Y, kinase=1.0, has_dynein=True, dynein_blocked=False)
        self.play(
            FadeOut(local_xs),
            FadeOut(verdict),
            Transform(endo, endo_free),
            w.top.nuc.animate.set_fill(NUCLEUS, opacity=0.32),
            w.bot.nuc.animate.set_fill(NUCLEUS, opacity=0.32),
            run_time=4.2,
        )

        # Drop two vertical barriers creating 3 sealed chambers
        self.at("divide the axon")
        ch = make_chambers(with_inhibitor=False)
        b1_target = ch.barriers[0].copy()
        b2_target = ch.barriers[1].copy()
        ch.barriers[0].shift(UP * 5.0)
        ch.barriers[1].shift(UP * 5.0)
        self.play(
            Transform(ch.barriers[0], b1_target),
            Transform(ch.barriers[1], b2_target),
            run_time=2.6,
        )

        # Label the three chambers in spoken order: Tip, middle stretch, cell body
        self.at("Tip")
        self.play(FadeIn(ch.headers[2]), run_time=0.45)
        self.at("middle stretch")
        self.play(FadeIn(ch.headers[1]), run_time=0.55)
        self.at("cell body")
        self.play(FadeIn(ch.headers[0]), run_time=1.0)

        # Fill ONLY the middle chamber with crimson TrkA inhibitor wash
        self.at("Now add a drug")
        ch_full = make_chambers(with_inhibitor=True)
        wash = ch_full.wash
        inhib_tag = ch_full.inhib_tag
        wash_final = wash.copy()
        wash.stretch_to_fit_height(0.05).move_to([(BAR_X1 + BAR_X2) / 2, CHAMBER_BOT + 0.04, 0])
        self.add(wash)
        self.play(Transform(wash, wash_final), FadeIn(inhib_tag), run_time=4.8)
        self.finish()


class S07MiddleOutcome(SpokenScene):
    def construct(self):
        w = make_world_tracks(top_nuc=0.28, bot_nuc=0.28)
        ch = make_chambers(with_inhibitor=True)
        tip_r = make_tip_trka(BOT_Y, active=1.0)

        u_c = ValueTracker(0.0)
        r_prog = ValueTracker(0.0)
        r_amp = ValueTracker(1.0)

        def courier_x():
            return TRACK_RIGHT_X + (TRACK_LEFT_X - TRACK_RIGHT_X) * u_c.get_value()

        def courier_kinase():
            x = courier_x()
            if BAR_X1 + 0.15 < x < BAR_X2 - 0.15:
                return 0.05
            return 1.0

        endo = always_redraw(lambda: make_endosome(
            courier_x(), TOP_Y,
            kinase=courier_kinase(),
            has_dynein=True,
            phase=u_c.get_value() * 42.0,
            ngf_bound=True,
        ))
        pulses = always_redraw(lambda: make_relay_pulses(BOT_Y, r_prog.get_value(), amp=r_amp.get_value()))
        self.add(ch.wash, w, ch.barriers, ch.headers, ch.inhib_tag, tip_r, endo, pulses)

        # Both start moving when narrator says "Watch how the two tracks split"
        self.at("Watch how the two")
        self.play(
            u_c.animate(rate_func=linear).set_value(0.14),
            r_prog.animate(rate_func=linear).set_value(1.2),
            run_time=2.5,
        )

        # Relay hits middle inhibitor and dies
        self.at("A relay")
        self.play(
            u_c.animate(rate_func=linear).set_value(0.28),
            r_prog.animate(rate_func=linear).set_value(2.15),
            run_time=2.8,
        )

        self.at("hits the inhibitor")
        pred_fail = boxed_label("Predicts: fails", BLOCK_COL, size=24, pad=0.12).move_to([-1.90, 0.20, 0], aligned_edge=RIGHT)
        self.play(
            u_c.animate(rate_func=linear).set_value(0.38),
            r_prog.animate(rate_func=linear).set_value(2.5),
            r_amp.animate(rate_func=linear).set_value(0.0),
            w.bot.nuc.animate.set_fill(NUCLEUS, opacity=0.12),
            FadeIn(pred_fail),
            run_time=2.8,
        )

        # Courier enters middle chamber: kinase dims while NGF stays locked inside
        self.at("The courier behaves differently")
        self.play(u_c.animate(rate_func=linear).set_value(0.50), run_time=2.4)

        self.at("Even if the drug")
        quiet_tag = boxed_label("Kinase quiet; NGF inside", NGF_COL, size=24, pad=0.12).move_to([0.0, -3.05, 0])
        self.play(
            u_c.animate(rate_func=linear).set_value(0.62),
            FadeIn(quiet_tag),
            run_time=3.2,
        )

        self.at("dynein carries the vesicle")
        self.play(u_c.animate(rate_func=linear).set_value(0.74), run_time=4.4)

        # Exits into drug-free cell body -> kinase relights and illuminates nucleus
        self.at("In the drug")
        pred_surv = boxed_label("Predicts: survives", GOLD, size=22, pad=0.10).move_to([-1.85, 2.72, 0], aligned_edge=RIGHT)
        self.play(
            u_c.animate(rate_func=linear).set_value(1.0),
            w.top.nuc.animate.set_fill(NUCLEUS, opacity=0.92),
            FadeOut(quiet_tag, run_time=0.6),
            FadeIn(pred_surv),
            run_time=3.4,
        )
        self.finish()


class S08NeutralizeNgf(SpokenScene):
    def construct(self):
        w = make_world_tracks(top_nuc=0.92, bot_nuc=0.12)
        ch = make_chambers(with_inhibitor=True)
        tip_r = make_tip_trka(BOT_Y, active=1.0)
        pred_surv = boxed_label("Predicts: survives", GOLD, size=22, pad=0.10).move_to([-1.85, 2.72, 0], aligned_edge=RIGHT)
        pred_fail = boxed_label("Predicts: fails", BLOCK_COL, size=24, pad=0.12).move_to([-1.90, 0.20, 0], aligned_edge=RIGHT)
        k_init = ValueTracker(0.75)
        endo = always_redraw(lambda: make_endosome(
            TRACK_LEFT_X, TOP_Y, kinase=k_init.get_value(), has_dynein=True, ngf_bound=True
        ))
        self.add(ch.wash, w, ch.barriers, ch.headers, ch.inhib_tag, tip_r, pred_surv, pred_fail, endo)

        # Observed result from Ye et al. (2003)
        self.at("In 2003")
        obs_tag = boxed_label("Observed: survival spared (Ye et al., 2003)", TEXT, size=25, pad=0.14).move_to([0.0, -3.05, 0])
        self.play(FadeIn(obs_tag), k_init.animate.set_value(1.15), run_time=2.8)

        self.at("and survival was spared")
        self.play(k_init.animate.set_value(0.95), run_time=2.0)

        self.at("That argues against")
        relay_out = make_cross([0.2, BOT_Y, 0], size=0.30, color=BLOCK_COL)
        # Dim only the bottom track shapes cleanly, keeping "Relay" and "Predicts: fails" at full opacity
        self.play(
            FadeIn(relay_out),
            dim_track(w.bot, factor=0.40),
            tip_r.animate.set_opacity(0.42),
            run_time=3.2,
        )

        # Clear middle wash and earlier experiment chips quickly, dim nucleus, and show non-NGF signal while NGF stays at tip
        self.at("Still, what if")
        self.play(
            FadeOut(ch.wash),
            FadeOut(ch.inhib_tag),
            FadeOut(obs_tag),
            FadeOut(pred_surv),
            FadeOut(pred_fail),
            FadeOut(relay_out),
            FadeOut(endo),
            w.top.nuc.animate.set_fill(NUCLEUS, opacity=0.28),
            run_time=0.8,
        )
        other_sig = VGroup(
            Circle(radius=0.18, stroke_color=KINASE, stroke_width=3.6, fill_color=KINASE, fill_opacity=0.28),
            Dot(ORIGIN, radius=0.075, color=KINASE),
        ).move_to([TRACK_RIGHT_X, TOP_Y, 0])
        self.play(FadeIn(other_sig), run_time=0.3)
        self.play(other_sig.animate(rate_func=linear).move_to([TRACK_LEFT_X, TOP_Y, 0]), run_time=2.1)
        self.play(FadeOut(other_sig), run_time=0.6)

        u_c = ValueTracker(0.0)
        k_lvl = ValueTracker(1.0)
        endo_live = always_redraw(lambda: make_endosome(
            TRACK_RIGHT_X + (TRACK_LEFT_X - TRACK_RIGHT_X) * u_c.get_value(),
            TOP_Y,
            kinase=k_lvl.get_value(),
            has_dynein=True,
            phase=u_c.get_value() * 34.0,
            ngf_bound=True,
        ))
        ab1 = make_antibody([-3.95, TOP_Y + 0.66, 0], angle=PI * 0.85, scale=0.95)
        ab2 = make_antibody([-3.15, TOP_Y + 0.66, 0], angle=-PI * 0.85, scale=0.95)
        ab3 = make_antibody([-3.65, TOP_Y - 0.62, 0], angle=0.0, scale=0.95)
        abs_grp = VGroup(ab1, ab2, ab3)
        ab_tag = T("anti-NGF", 24, BLOCK_COL).move_to([-2.62, TOP_Y - 0.68, 0])

        self.add(endo_live)
        self.play(u_c.animate(rate_func=linear).set_value(0.41), run_time=2.1)

        # Neutralize NGF upon arrival in cell body
        self.at("Neutralizing NGF")
        self.play(
            FadeIn(abs_grp),
            FadeIn(ab_tag),
            u_c.animate(rate_func=linear).set_value(0.53),
            run_time=0.6,
        )
        self.play(
            u_c.animate(rate_func=linear).set_value(1.0),
            ab1.animate.move_to([TRACK_LEFT_X - 0.25, TOP_Y + 0.30, 0]),
            ab2.animate.move_to([TRACK_LEFT_X + 0.25, TOP_Y + 0.30, 0]),
            ab3.animate.move_to([TRACK_LEFT_X, TOP_Y - 0.28, 0]),
            run_time=2.4,
        )

        self.at("takes survival away")
        fail_tag = boxed_label("Survival fails", BLOCK_COL, size=24, pad=0.12).move_to([-1.90, 2.66, 0], aligned_edge=RIGHT)
        self.play(
            k_lvl.animate.set_value(0.05),
            w.top.nuc.animate.set_fill(NUCLEUS, opacity=0.12),
            FadeIn(fail_tag),
            run_time=2.2,
        )

        self.at("So the carried ligand")
        honest = boxed_label("Supports carried NGF-TrkA; other routes open", GOLD, size=25, pad=0.14).move_to([0.0, -3.05, 0])
        self.play(FadeIn(honest), run_time=2.6)
        self.finish()


class S09Takeaway(SpokenScene):
    def _mini_world(self, with_chambers=False):
        """Compact 2-track miniature built from the same proportions, ready for TwoPanel.put()."""
        top = make_neuron_track(1.45, nuc_lit=0.26)
        bot = make_neuron_track(-1.35, nuc_lit=0.26)
        l_c = T("Courier", 28, TEXT).move_to([-4.65, 2.65, 0])
        l_r = T("Relay", 28, TEXT).move_to([-4.65, -0.15, 0])
        g = VGroup(top, bot, l_c, l_r)
        if with_chambers:
            b1 = Line([BAR_X1, -2.25, 0], [BAR_X1, 2.45, 0], color=BARRIER_COL, stroke_width=5)
            b2 = Line([BAR_X2, -2.25, 0], [BAR_X2, 2.45, 0], color=BARRIER_COL, stroke_width=5)
            wash = Rectangle(width=BAR_X2 - BAR_X1 - 0.08, height=4.62,
                             stroke_width=0, fill_color=BLOCK_COL, fill_opacity=0.22).move_to([(BAR_X1 + BAR_X2) / 2, 0.10, 0])
            wash.layout_ok = True
            g.add(wash, b1, b2)
            g.wash = wash
        g.top = top
        g.bot = bot
        g.l_c = l_c
        g.l_r = l_r
        return g

    def construct(self):
        tp = TwoPanel("Dynein block -> both fail", "Middle TrkA block -> diverge",
                      colors=(BLOCK_COL, GOLD), top=3.15, bottom=-2.20, gap=0.35, width=12.8, size=28)

        left_w = self._mini_world(with_chambers=False)
        right_w = self._mini_world(with_chambers=True)
        tp.put(left_w, "left")
        tp.put(right_w, "right")
        left_w.scale(0.90)
        right_w.scale(0.90)

        for lbl in (left_w.l_c, left_w.l_r, right_w.l_c, right_w.l_r):
            lbl.set(font_size=24)

        u_l = ValueTracker(0.0)
        l_blocked = ValueTracker(0.0)
        u_r = ValueTracker(0.0)
        r_prog = ValueTracker(0.0)
        r_amp = ValueTracker(1.0)

        lc_top = left_w.top.nuc.get_center()
        lc_bot = left_w.bot.nuc.get_center()
        l_x1 = left_w.top.get_right()[0] - 0.36
        l_x0 = lc_top[0] + 0.55

        rc_top = right_w.top.nuc.get_center()
        rc_bot = right_w.bot.nuc.get_center()
        r_x1 = right_w.top.get_right()[0] - 0.36
        r_x0 = rc_top[0] + 0.55
        r_mid_l = rc_top[0] + (r_x1 - rc_top[0]) * 0.30
        r_mid_r = rc_top[0] + (r_x1 - rc_top[0]) * 0.68

        left_endo = always_redraw(lambda: make_endosome(
            l_x1 + (l_x0 - l_x1) * u_l.get_value(), lc_top[1],
            kinase=0.9, has_dynein=True, dynein_blocked=(l_blocked.get_value() > 0.5),
            phase=u_l.get_value() * 18.0, scale=0.48,
        ))
        left_bot_x = make_dynein([l_x1 - 0.18, lc_bot[1] - 0.08, 0], blocked=True, scale=0.48)

        def r_kinase():
            x = r_x1 + (r_x0 - r_x1) * u_r.get_value()
            return 0.08 if r_mid_l < x < r_mid_r else 1.0

        right_endo = always_redraw(lambda: make_endosome(
            r_x1 + (r_x0 - r_x1) * u_r.get_value(), rc_top[1],
            kinase=r_kinase(), has_dynein=True, dynein_blocked=False,
            phase=u_r.get_value() * 32.0, scale=0.48,
        ))

        def right_pulse():
            p = r_prog.get_value()
            px = r_x1 + (r_x0 - r_x1) * p
            a = r_amp.get_value()
            if a <= 0.05:
                return VGroup()
            band = Rectangle(width=0.52, height=0.28, stroke_width=0,
                             fill_color=KINASE, fill_opacity=0.35 * a).move_to([px, rc_bot[1], 0])
            dot = Circle(radius=0.12, stroke_color=KINASE, stroke_width=3.0 * a,
                         fill_color=KINASE, fill_opacity=0.42 * a).move_to([px, rc_bot[1], 0])
            return VGroup(band, dot)

        right_relay_dot = always_redraw(right_pulse)

        self.add(tp, left_w, right_w, left_endo, right_endo, right_relay_dot)

        # Beat 1: both models run; left hits dynein block, right begins entering middle chamber
        self.at("Notice why")
        self.play(
            u_l.animate(rate_func=linear).set_value(0.10),
            u_r.animate(rate_func=linear).set_value(0.32),
            r_prog.animate(rate_func=linear).set_value(0.44),
            run_time=2.8,
        )

        self.at("where disabling")
        l_blocked.set_value(1.0)
        self.play(
            FadeIn(left_bot_x),
            left_w.top.nuc.animate.set_fill(NUCLEUS, opacity=0.10),
            left_w.bot.nuc.animate.set_fill(NUCLEUS, opacity=0.10),
            r_amp.animate.set_value(0.0),
            right_w.bot.nuc.animate.set_fill(NUCLEUS, opacity=0.10),
            u_r.animate(rate_func=linear).set_value(0.50),
            run_time=2.5,
        )

        # Beat 2: shared requirement -> inconclusive (dim only left neuron tracks cleanly)
        self.at("A perturbation")
        left_note = T("shared requirement: both fail", 24, BLOCK_COL).move_to([-3.2, -1.78, 0])
        self.play(
            FadeIn(left_note),
            u_r.animate(rate_func=linear).set_value(0.75),
            run_time=5.4,
        )

        # Beat 3: right courier arrives & lights nucleus; highlight diverging middle step + takeaway caption
        self.at("When two hypotheses")
        right_note = T("courier survives; relay fails", 24, GOLD).move_to([3.2, -1.78, 0])
        mid_hl = SurroundingRectangle(right_w.wash, color=GOLD, buff=0.0, stroke_width=3.5)
        mid_hl.layout_ok = True
        self.play(
            dim_track(left_w.top, factor=0.42),
            dim_track(left_w.bot, factor=0.42),
            u_r.animate(rate_func=linear).set_value(1.0),
            right_w.top.nuc.animate.set_fill(NUCLEUS, opacity=0.92),
            FadeIn(right_note),
            Create(mid_hl),
            run_time=2.4,
        )

        self.at("aim your test")
        cap = caption("Aim your test at the exact step where predictions diverge.", size=28, color=GOLD, y=-3.00)
        self.play(FadeIn(cap), run_time=2.8)
        self.finish()


class S10End(EndCard):
    LINE = "To separate courier from relay, test what only one model predicts."
