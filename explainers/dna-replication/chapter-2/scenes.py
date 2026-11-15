"""Why One Strand Is Built in Pieces — animation for biochemistrypedia.com.

COLOUR MAP (one colour per concept across the whole film):
- PARENTAL_PURPLE (#B284E0): parental DNA template strands and intact parental duplex
- NEW_CYAN        (#58C4DD): newly synthesized DNA strands and dNTP building blocks
- PRIMER_YELLOW   (#F5D547): RNA primers laid by primase
- ENZYME_GREEN    (#83C167): replication enzymes and clamps (polymerase, primase, DnaB/CMG, SSB, gyrase, Pol I, ligase, PCNA)
- HIGHLIGHT_GOLD  (#D4A843): active 3' end focus, questions, observations, and synthesis direction highlights
- STOP_RED        (#FC6255): blocked 5' end / impossible growth direction / overwinding stress / nick markers
- GREY            (#8B93A1): structural ticks, dividers, schematic scope tag
- TEXT            (#E8EAF0): primary headings and body text on dark background BG (#0f1117)

ONE PICTURE OF THE WORLD (carried across scenes):
A horizontal Y-shaped DNA replication fork opening rightward along a parental purple duplex:
- Upper parental template: 3' (left) to 5' (right); 5'->3' polarity arrow points LEFT.
- Lower parental template: 5' (left) to 3' (right); 5'->3' polarity arrow points RIGHT.
- Ahead of the fork junction (right): zipped parental duplex with base-pair rungs that unzip as fork_x advances.
- Upper new strand (leading): grows continuously RIGHT (5'->3') toward the opening fork.
- Lower new strand (lagging): grows in short primed pieces LEFT (5'->3') away from the fork, later processed and sealed.

WHAT CHANGES ON SCREEN (computed per spoken scene):
- s00_link_and_question: Two paired purple-cyan daughter duplexes open into the large Y-fork as fork_x advances from -2.0 to -0.1, unzipping base-pair rungs computed from fork_x while opposite template arrows glide along the arms.
- s02_one_fork: Title clears and fork continues rightward (+0.25 to +1.65) unzipping rungs while opposite template arrowheads march along both arms and cyan starter blocks appear beside each template.
- s03_constraint: Zoomed template-primer chain grows rightward block-by-block as nucleotides click onto the 3' end (computed chain length n_nt), base-pair rungs pulse while checking template pairing, a blocked nucleotide rebounds at 5', and primase lays a 3-block yellow primer on bare template.
- s04_predict: Full fork advances rightward (fork_x -1.2 to +0.8) exposing bare template while both neutral cyan starters with 3' ends pulse synchronously without revealing an answer.
- s06_leading: Upper 3' end highlights in gold while fork_x advances (0.8 to 3.2); green clamp tracks lead_x as the continuous upper cyan leading strand lengthens linearly with fork_x while the lower starter stays fixed.
- s07_lagging: Lower template highlights while fork_x advances (-0.2 to +2.8) in two cycles; primase places two yellow primers near the fork and the green clamp steps leftward (5'->3') behind each primer, extending two separate cyan Okazaki fragments.
- s08_processing: Zoomed view of two Okazaki fragments; Pol I sweeps rightward across each yellow primer converting blocks from yellow to cyan, leaving a nick that ligase seals with a gold pulse before pulling back to a continuous strand.
- s09_jobs: Five green enzymes act sequentially on the advancing fork (DnaB unzips, SSB coats exposed strands, gyrase returns a computed overwinding gauge needle from 0.80 back toward centre 0.22, DnaG primes, Pol III + beta clamp extends cyan DNA) and dock into a 5-slot job strip.
- s10_eukaryotes: Bacterial job strip swaps in place to eukaryotic names (CMG, Pol alpha-primase, Pol epsilon on leading, Pol delta on PCNA on lagging) while three origins open expanding replication bubbles (width computed from bubble_w tracker) along a purple chromosome bar.
- s11_job_map: Carried eukaryotic fork advances underneath while a 5-node horizontal job map (open, start, extend, replace, seal) lights sequentially in sync with fork actions, then displays bacterial names above and eukaryotic names below without equating them.
- s12_rule: Full carried fork advances continuously (fork_x -1.4 to +3.1) while upper leading clamp grows continuously right and lower lagging primers + clamps build leftward fragments in sequence that join into one strand, both driven by 3' trackers.
"""

from bp_parts import *

PARENTAL_PURPLE = "#B284E0"
NEW_CYAN = BLUE
PRIMER_YELLOW = YELLOW
ENZYME_GREEN = GREEN
HIGHLIGHT_GOLD = GOLD
STOP_RED = RED

# Canonical Y-fork geometry (fits comfortably inside y in [-2.3, 2.3], x in [-5.8, 5.8])
X_LEFT = -5.6
X_RIGHT = 5.6
Y_TOP = 1.40
Y_BOT = -1.40
Y_DUP = 0.24
FORK_OPEN_DX = 0.95
RUNG_XS = np.arange(X_LEFT + 0.35, X_RIGHT - 0.15, 0.36)


def _fork_y(x, fx, sign, y_arm=Y_TOP, y_dup=Y_DUP, dx=FORK_OPEN_DX):
    """Smooth S-curve Y coordinate for upper (sign=+1) or lower (sign=-1) parental strand."""
    if x <= fx:
        return sign * y_arm
    if x >= fx + dx:
        return sign * y_dup
    u = (x - fx) / dx
    s = 0.5 * (1.0 - np.cos(np.pi * u))
    return sign * (y_arm + s * (y_dup - y_arm))


def _fork_pts(fx, sign, x0=X_LEFT, x1=X_RIGHT, y_arm=Y_TOP, y_dup=Y_DUP, dx=FORK_OPEN_DX):
    xs = [x0]
    if x0 < fx < x1:
        xs.append(fx)
    if x0 < fx + dx < x1:
        for u in np.linspace(0.08, 0.92, 9):
            px = fx + u * dx
            if x0 < px < x1:
                xs.append(px)
        xs.append(fx + dx)
    xs.append(x1)
    xs = sorted(set(xs))
    return [np.array([x, _fork_y(x, fx, sign, y_arm, y_dup, dx), 0.0]) for x in xs]


def _arrow_triangle(tip, direction, color=PARENTAL_PURPLE, size=0.18):
    d = np.array(direction, dtype=float)
    d = d / max(np.linalg.norm(d), 1e-9)
    n = np.array([-d[1], d[0], 0.0])
    p0 = tip + d * (size * 0.65)
    p1 = tip - d * (size * 0.55) + n * (size * 0.55)
    p2 = tip - d * (size * 0.55) - n * (size * 0.55)
    return Polygon(p0, p1, p2, color=color, fill_opacity=1.0, stroke_width=0)


def build_fork(fx_tracker, arrow_phase=None, y_arm=Y_TOP, y_dup=Y_DUP, x0=X_LEFT, x1=X_RIGHT,
               show_end_labels=True, stroke=7.0):
    """Dynamic Y-fork driven by fx_tracker (ValueTracker). Unzips base-pair rungs as fork_x moves right."""
    def _mk():
        fx = fx_tracker.get_value()
        g = VGroup()
        for rx in RUNG_XS:
            if rx < x0 + 0.1 or rx > x1 - 0.1:
                continue
            if rx >= fx + FORK_OPEN_DX - 0.05:
                y_u = _fork_y(rx, fx, +1, y_arm, y_dup)
                y_l = _fork_y(rx, fx, -1, y_arm, y_dup)
                g.add(Line([rx, y_l + 0.04, 0], [rx, y_u - 0.04, 0],
                           color=PARENTAL_PURPLE, stroke_width=2.5, stroke_opacity=0.42))
            elif rx > fx + 0.15:
                frac = (rx - fx - 0.15) / (FORK_OPEN_DX - 0.2)
                y_u = _fork_y(rx, fx, +1, y_arm, y_dup)
                y_l = _fork_y(rx, fx, -1, y_arm, y_dup)
                g.add(Line([rx, y_l + 0.08, 0], [rx, y_u - 0.08, 0],
                           color=PARENTAL_PURPLE, stroke_width=2.0, stroke_opacity=0.35 * np.clip(frac, 0, 1)))
        for sign in (+1, -1):
            strand = VMobject(stroke_color=PARENTAL_PURPLE, stroke_width=stroke, fill_opacity=0)
            strand.set_points_as_corners(_fork_pts(fx, sign, x0, x1, y_arm, y_dup))
            g.add(strand)

        ph = (arrow_phase.get_value() % 1.0) if arrow_phase is not None else 0.0
        arm_len = max(0.8, fx - x0)
        for k in range(2):
            u_top = ((0.28 + 0.48 * k - ph) % 1.0)
            ax_top = x0 + 0.35 + u_top * max(0.4, arm_len - 0.7)
            if ax_top < fx - 0.2:
                g.add(_arrow_triangle(np.array([ax_top, y_arm, 0.0]), LEFT, PARENTAL_PURPLE, 0.22))
            u_bot = ((0.22 + 0.48 * k + ph) % 1.0)
            ax_bot = x0 + 0.35 + u_bot * max(0.4, arm_len - 0.7)
            if ax_bot < fx - 0.2:
                g.add(_arrow_triangle(np.array([ax_bot, -y_arm, 0.0]), RIGHT, PARENTAL_PURPLE, 0.22))

        if show_end_labels:
            g.add(M("3′", 24, PARENTAL_PURPLE).move_to([x0 - 0.34, y_arm, 0]))
            g.add(M("5′", 24, PARENTAL_PURPLE).move_to([x1 + 0.34, y_dup, 0]))
            g.add(M("5′", 24, PARENTAL_PURPLE).move_to([x0 - 0.34, -y_arm, 0]))
            g.add(M("3′", 24, PARENTAL_PURPLE).move_to([x1 + 0.34, -y_dup, 0]))
        return g

    return always_redraw(_mk)


def poly_clamp(center, facing=RIGHT, color=ENZYME_GREEN, label=None, label_dir=UP, radius=0.38):
    """A C-shaped polymerase clamp block (shape that acts: grips the strand end)."""
    c = np.array(center, dtype=float)
    start = 0.55 if facing[0] > 0 else PI + 0.55
    ring = AnnularSector(
        inner_radius=radius * 0.48,
        outer_radius=radius,
        angle=TAU - 1.1,
        start_angle=start,
        arc_center=c,
        color=color,
        fill_opacity=0.88,
        stroke_color=TEXT,
        stroke_width=1.8,
    )
    g = VGroup(ring)
    if label:
        lab = T(label, 24, color)
        lab.next_to(ring, label_dir, buff=0.14)
        g.add(lab)
    return g


def primer_seg(x0, x1, y, color=PRIMER_YELLOW, height=0.18):
    """Segmented yellow RNA primer bar along template y."""
    n = max(2, int(round((x1 - x0) / 0.24)))
    w = (x1 - x0) / n
    g = VGroup()
    for i in range(n):
        bx = x0 + (i + 0.5) * w
        r = RoundedRectangle(
            corner_radius=0.04,
            width=max(0.08, w - 0.04),
            height=height,
            color=color,
            fill_opacity=0.92,
            stroke_width=1.5,
            stroke_color=TEXT,
        ).move_to([bx, y, 0])
        g.add(r)
    return g


def dna_seg(x0, x1, y, color=NEW_CYAN, stroke=8.0):
    """A continuous newly synthesized DNA strand segment."""
    if x1 - x0 < 0.03:
        return VMobject()
    return Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=stroke)


def end_badge(text, pos, color=HIGHLIGHT_GOLD, size=24):
    """Crisp 3' or 5' badge in a generously padded pill (no glyph/border collision)."""
    return boxed_label(text, color=color, size=size, pad=0.16, stroke=2.0, fill_opacity=0.22).move_to(pos)


def overwinding_gauge(tracker, center, radius=0.85, label="overwinding", color=STOP_RED):
    """Half-circle overwinding gauge without unrequested numeric percentages."""
    c = np.array(center, dtype=float)
    track = Arc(radius=radius, start_angle=PI, angle=-PI, arc_center=c, stroke_color=GREY, stroke_width=9)
    v = lambda: float(np.clip(tracker.get_value(), 0.02, 0.98))
    val = always_redraw(lambda: Arc(radius=radius, start_angle=PI, angle=-PI * v(), arc_center=c, stroke_color=color, stroke_width=9))
    needle = always_redraw(lambda: Line(
        c, c + 0.8 * radius * np.array([np.cos(PI - PI * v()), np.sin(PI - PI * v()), 0]),
        color=TEXT, stroke_width=5,
    ))
    hub = Dot(c, radius=0.06, color=TEXT)
    lbl = T(label, 24, color).move_to(c + DOWN * 0.42)
    return VGroup(track, val, needle, hub, lbl)


# ------------------------------------------------------------------ s00
class S00LinkAndQuestion(SpokenScene):
    def construct(self):
        pair1 = VGroup(
            Line([-3.8, 1.05, 0], [3.8, 1.05, 0], color=PARENTAL_PURPLE, stroke_width=7),
            Line([-3.8, 0.65, 0], [3.8, 0.65, 0], color=NEW_CYAN, stroke_width=7),
        )
        pair2 = VGroup(
            Line([-3.8, -0.65, 0], [3.8, -0.65, 0], color=NEW_CYAN, stroke_width=7),
            Line([-3.8, -1.05, 0], [3.8, -1.05, 0], color=PARENTAL_PURPLE, stroke_width=7),
        )
        rungs1 = VGroup(*[Line([rx, 0.69, 0], [rx, 1.01, 0], color=GREY, stroke_width=2)
                          for rx in np.arange(-3.5, 3.6, 0.45)])
        rungs2 = VGroup(*[Line([rx, -1.01, 0], [rx, -0.69, 0], color=GREY, stroke_width=2)
                          for rx in np.arange(-3.5, 3.6, 0.45)])
        hybrids = VGroup(rungs1, rungs2, pair1, pair2)

        tag_old = T("old strand", 26, PARENTAL_PURPLE).move_to([-4.95, 1.05, 0])
        tag_new = T("new strand", 26, NEW_CYAN).move_to([-4.95, 0.52, 0])
        sc = scope_tag("schematic")

        self.play(FadeIn(hybrids), FadeIn(tag_old), FadeIn(tag_new), FadeIn(sc), run_time=0.9)
        self.at("builds one new strand")

        fx = ValueTracker(-2.0)
        ph = ValueTracker(0.0)
        fork = build_fork(fx, ph)
        self.play(
            FadeOut(hybrids, run_time=0.6),
            FadeOut(tag_old, run_time=0.6),
            FadeOut(tag_new, run_time=0.6),
            FadeIn(fork, run_time=0.8),
        )

        self.at("two old strands")
        opp_top = T("3′ ← 5′", 26, PARENTAL_PURPLE).move_to([-3.8, Y_TOP + 0.55, 0])
        opp_bot = T("5′ → 3′", 26, PARENTAL_PURPLE).move_to([-3.8, -Y_TOP - 0.55, 0])
        self.play(
            FadeIn(opp_top), FadeIn(opp_bot),
            fx.animate(rate_func=linear).set_value(-0.9),
            ph.animate(rate_func=linear).set_value(0.8),
            run_time=2.6,
        )

        self.at("How can one fork")
        q = fit_text("How can one fork copy both?", max_w=11.0, size=34, color=HIGHLIGHT_GOLD).move_to([0, 3.15, 0])
        self.play(
            FadeIn(q, shift=DOWN * 0.1),
            fx.animate(rate_func=linear).set_value(-0.35),
            ph.animate(rate_func=linear).set_value(1.5),
            run_time=2.2,
        )
        rest = max(0.1, self.narration_s + 0.35 - self.elapsed())
        self.play(
            fx.animate(rate_func=linear).set_value(-0.1),
            ph.animate(rate_func=linear).set_value(1.9),
            run_time=rest,
        )
        self.finish()


# ------------------------------------------------------------------ s01
class S01Title(NarratedScene):
    def construct(self):
        fx = ValueTracker(-0.1)
        ph = ValueTracker(1.9)
        fork = build_fork(fx, ph)
        sc = scope_tag("schematic")
        lesson = T("DNA REPLICATION: SEMICONSERVATIVE COPYING AND ITS MACHINERY", 22, GREY)
        fit(lesson, max_w=11.8)
        title = T("Why One Strand Is Built in Pieces", 46, color=TEXT, font=TITLE_FONT)
        fit(title, max_w=11.8)
        rule = Line(LEFT * 1.4, RIGHT * 1.4, color=HIGHLIGHT_GOLD, stroke_width=4)
        banner = VGroup(lesson, title, rule).arrange(DOWN, buff=0.18).move_to([0, 2.75, 0])

        self.add(fork, sc)
        self.play(
            FadeIn(banner, shift=DOWN * 0.1),
            fx.animate(rate_func=linear).set_value(0.08),
            ph.animate(rate_func=linear).set_value(2.1),
            run_time=0.65,
        )
        self.play(
            fx.animate(rate_func=linear).set_value(0.25),
            ph.animate(rate_func=linear).set_value(2.4),
            run_time=1.35,
        )
        self.finish()


# ------------------------------------------------------------------ s02
class S02OneFork(SpokenScene):
    def construct(self):
        fx = ValueTracker(0.25)
        ph = ValueTracker(2.4)
        fork = build_fork(fx, ph)
        sc = scope_tag("schematic")

        title_old = T("Why One Strand Is Built in Pieces", 44, color=TEXT, font=TITLE_FONT).move_to([0, 2.75, 0])
        self.add(fork, sc, title_old)
        self.play(
            FadeOut(title_old, run_time=0.55),
            fx.animate(rate_func=linear).set_value(0.45),
            ph.animate(rate_func=linear).set_value(2.7),
            run_time=1.6,
        )

        self.at("Purple marks parental")
        lbl_p = T("parental template", 28, PARENTAL_PURPLE).move_to([-2.4, Y_TOP + 0.55, 0])
        self.play(FadeIn(lbl_p), fx.animate(rate_func=linear).set_value(0.6), run_time=0.8)

        self.at("and cyan")
        s_top_x = ValueTracker(-2.9)
        s_bot_x = ValueTracker(-3.2)
        s_top = always_redraw(lambda: dna_seg(-4.5, s_top_x.get_value(), Y_TOP - 0.30, NEW_CYAN, stroke=9))
        s_bot = always_redraw(lambda: dna_seg(s_bot_x.get_value(), -1.6, -Y_TOP + 0.30, NEW_CYAN, stroke=9))
        lbl_n = T("new DNA", 28, NEW_CYAN).move_to([-3.7, Y_TOP - 0.74, 0])
        self.play(FadeIn(s_top), FadeIn(s_bot), FadeIn(lbl_n), run_time=0.8)

        self.at("The parental duplex")
        leg_p = VGroup(
            Line([0, 0, 0], [0.45, 0, 0], color=PARENTAL_PURPLE, stroke_width=6),
            T("parental template", 24, PARENTAL_PURPLE),
        ).arrange(RIGHT, buff=0.14)
        leg_n = VGroup(
            Line([0, 0, 0], [0.45, 0, 0], color=NEW_CYAN, stroke_width=6),
            T("new DNA", 24, NEW_CYAN),
        ).arrange(RIGHT, buff=0.14)
        legend = VGroup(leg_p, leg_n).arrange(RIGHT, buff=0.45).move_to([-2.6, 3.25, 0])

        self.play(FadeOut(lbl_p, run_time=0.4), FadeOut(lbl_n, run_time=0.4))
        self.play(
            FadeIn(legend, run_time=0.6),
            fx.animate(rate_func=linear).set_value(1.3),
            s_top_x.animate(rate_func=linear).set_value(-1.6),
            ph.animate(rate_func=linear).set_value(4.4),
            run_time=4.8,
        )

        self.at("Each purple strand")
        dir_top = T("template runs 3′ → 5′", 26, PARENTAL_PURPLE).move_to([-2.6, Y_TOP + 0.55, 0])
        dir_bot = T("template runs 5′ → 3′", 26, PARENTAL_PURPLE).move_to([-2.6, -Y_TOP - 0.55, 0])
        self.play(
            FadeIn(dir_top), FadeIn(dir_bot),
            fx.animate(rate_func=linear).set_value(1.85),
            s_top_x.animate(rate_func=linear).set_value(-0.9),
            s_bot_x.animate(rate_func=linear).set_value(-4.0),
            ph.animate(rate_func=linear).set_value(5.6),
            run_time=3.2,
        )

        self.at("run in opposite")
        rest = max(0.1, self.narration_s + 0.3 - self.elapsed())
        self.play(
            ph.animate(rate_func=linear).set_value(6.8),
            fx.animate(rate_func=linear).set_value(2.2),
            s_top_x.animate(rate_func=linear).set_value(-0.3),
            run_time=rest,
        )
        self.finish()


# ------------------------------------------------------------------ s03
class S03Constraint(SpokenScene):
    def construct(self):
        head = T("Polymerase rule: add only to a paired 3′ end", 30, TEXT).move_to([0, 3.2, 0])
        sc = scope_tag("schematic")

        tmpl_y = -0.75
        new_y = -0.05
        tmpl = Line([-5.6, tmpl_y, 0], [5.6, tmpl_y, 0], color=PARENTAL_PURPLE, stroke_width=9)
        t_3 = M("3′", 26, PARENTAL_PURPLE).move_to([-5.95, tmpl_y, 0])
        t_5 = M("5′", 26, PARENTAL_PURPLE).move_to([5.95, tmpl_y, 0])
        t_lbl = T("parental template", 24, PARENTAL_PURPLE).move_to([-3.6, tmpl_y - 0.58, 0])

        dx = 0.62
        x_start = -4.2

        def nt_block(idx, color=NEW_CYAN):
            cx = x_start + idx * dx
            r = RoundedRectangle(corner_radius=0.07, width=0.54, height=0.44,
                                 color=color, fill_opacity=0.88, stroke_color=TEXT, stroke_width=1.8).move_to([cx, new_y, 0])
            rung = Line([cx, tmpl_y + 0.05, 0], [cx, new_y - 0.22, 0], color=GREY, stroke_width=2.5)
            return VGroup(rung, r)

        n_nt = ValueTracker(3)
        blocks = VGroup(*[nt_block(i) for i in range(3)])
        n_5 = end_badge("5′", [x_start - 0.72, new_y, 0], color=NEW_CYAN)

        def _3p_pos():
            return np.array([x_start + (n_nt.get_value() - 1) * dx + 0.58, new_y + 0.72, 0])

        b3 = always_redraw(lambda: end_badge("3′", _3p_pos(), color=HIGHLIGHT_GOLD))
        clamp = always_redraw(lambda: poly_clamp(
            [x_start + (n_nt.get_value() - 0.65) * dx, new_y, 0],
            facing=RIGHT, color=ENZYME_GREEN, radius=0.48
        ))

        self.add(head, sc, tmpl, t_3, t_5, t_lbl, blocks, n_5, b3, clamp)

        self.at("adds a nucleotide")
        inc1 = RoundedRectangle(corner_radius=0.07, width=0.54, height=0.44,
                                color=NEW_CYAN, fill_opacity=0.88, stroke_color=TEXT, stroke_width=1.8).move_to([0.2, 1.35, 0])
        inc1_lbl = T("nucleotide", 24, NEW_CYAN).next_to(inc1, UP, buff=0.14)
        self.play(FadeIn(inc1), FadeIn(inc1_lbl), run_time=0.6)
        target3 = np.array([x_start + 3 * dx, new_y, 0])
        self.play(inc1.animate.move_to(target3), FadeOut(inc1_lbl), run_time=0.9)
        rung3 = Line([target3[0], tmpl_y + 0.05, 0], [target3[0], new_y - 0.22, 0], color=GREY, stroke_width=2.5)
        self.add(rung3)
        self.play(n_nt.animate.set_value(4), run_time=0.6)

        self.at("New DNA therefore")
        growth_arr = VGroup(
            Arrow([-4.3, 1.40, 0], [-0.4, 1.40, 0], color=HIGHLIGHT_GOLD, stroke_width=5, buff=0),
            T("grows 5′ → 3′", 26, HIGHLIGHT_GOLD).move_to([-2.35, 1.85, 0]),
        )
        inc2 = RoundedRectangle(corner_radius=0.07, width=0.54, height=0.44,
                                color=NEW_CYAN, fill_opacity=0.88, stroke_color=TEXT, stroke_width=1.8).move_to([0.8, 1.35, 0])
        stop_x = VGroup(
            T("×", 36, STOP_RED).move_to([x_start - 0.72, new_y + 0.72, 0]),
            T("no 5′ growth", 24, STOP_RED).move_to([x_start - 0.72, new_y + 1.18, 0]),
        )
        self.play(FadeIn(growth_arr), FadeIn(inc2), FadeIn(stop_x), run_time=0.8)
        target4 = np.array([x_start + 4 * dx, new_y, 0])
        self.play(inc2.animate.move_to(target4), run_time=0.8)
        rung4 = Line([target4[0], tmpl_y + 0.05, 0], [target4[0], new_y - 0.22, 0], color=GREY, stroke_width=2.5)
        self.add(rung4)
        self.play(n_nt.animate.set_value(5), run_time=0.6)

        self.at("A copying polymerase")
        # Add two nucleotides sequentially to span 8.92s -> 15.34s cleanly without stalling
        inc3 = RoundedRectangle(corner_radius=0.07, width=0.54, height=0.44,
                                color=NEW_CYAN, fill_opacity=0.88, stroke_color=TEXT, stroke_width=1.8).move_to([1.1, 1.35, 0])
        target5 = np.array([x_start + 5 * dx, new_y, 0])
        pair_hl = SurroundingRectangle(VGroup(rung4, inc2), color=HIGHLIGHT_GOLD, buff=0.08, stroke_width=3)
        pair_lbl = T("3′ end paired to template", 26, HIGHLIGHT_GOLD).move_to([1.1, tmpl_y - 0.58, 0])
        self.play(Create(pair_hl), FadeIn(pair_lbl), FadeIn(inc3), run_time=1.0)
        self.play(inc3.animate.move_to(target5), run_time=1.3)
        rung5 = Line([target5[0], tmpl_y + 0.05, 0], [target5[0], new_y - 0.22, 0], color=GREY, stroke_width=2.5)
        self.add(rung5)
        self.play(
            n_nt.animate.set_value(6),
            pair_hl.animate.move_to([target5[0], (tmpl_y + new_y) / 2, 0]),
            run_time=1.4,
        )
        inc4 = RoundedRectangle(corner_radius=0.07, width=0.54, height=0.44,
                                color=NEW_CYAN, fill_opacity=0.88, stroke_color=TEXT, stroke_width=1.8).move_to([1.8, 1.35, 0])
        target6 = np.array([x_start + 6 * dx, new_y, 0])
        self.play(FadeIn(inc4), run_time=0.5)
        self.play(inc4.animate.move_to(target6), run_time=1.1)
        rung6 = Line([target6[0], tmpl_y + 0.05, 0], [target6[0], new_y - 0.22, 0], color=GREY, stroke_width=2.5)
        self.add(rung6)
        self.play(
            n_nt.animate.set_value(7),
            pair_hl.animate.move_to([target6[0], (tmpl_y + new_y) / 2, 0]),
            run_time=0.9,
        )

        self.at("Replicative polymerases")
        self.play(FadeOut(pair_hl), FadeOut(pair_lbl), FadeOut(stop_x), run_time=0.5)
        lone_x = 2.6
        lone_nt = RoundedRectangle(corner_radius=0.07, width=0.54, height=0.44,
                                   color=NEW_CYAN, fill_opacity=0.88, stroke_color=TEXT, stroke_width=1.8).move_to([lone_x, 1.15, 0])
        fail_lbl = T("cannot start alone", 26, STOP_RED).move_to([lone_x + 0.8, 1.85, 0])
        fail_mark = T("×", 36, STOP_RED).move_to([lone_x, new_y + 0.48, 0])
        self.play(FadeIn(lone_nt), run_time=0.5)
        self.play(lone_nt.animate.move_to([lone_x, new_y, 0]), run_time=0.8)
        self.play(FadeIn(fail_mark), FadeIn(fail_lbl), run_time=0.7)
        self.play(FadeOut(lone_nt), FadeOut(fail_mark), run_time=0.8)

        self.at("Primase must first")
        primase = boxed_label("primase", ENZYME_GREEN, size=26, fill_opacity=0.25).move_to([2.6, 0.95, 0])
        primer_blocks = primer_seg(1.7, 3.6, new_y, PRIMER_YELLOW, height=0.38)
        primer_rungs = VGroup(*[Line([px, tmpl_y + 0.05, 0], [px, new_y - 0.19, 0], color=GREY, stroke_width=2.5)
                                for px in np.linspace(1.95, 3.35, 3)])
        primer_lbl = T("RNA primer", 24, PRIMER_YELLOW).move_to([2.65, tmpl_y - 0.58, 0])
        new_3p = end_badge("3′", [3.95, new_y + 0.65, 0], color=HIGHLIGHT_GOLD)
        self.play(FadeOut(fail_lbl, run_time=0.3), FadeIn(primase, shift=DOWN * 0.15), run_time=0.7)
        self.play(FadeIn(primer_rungs), FadeIn(primer_blocks), FadeIn(primer_lbl), run_time=0.9)
        self.play(FadeIn(new_3p), run_time=0.7)
        self.finish()


# ------------------------------------------------------------------ s04 & s05
def _s04_s05_world(fx_val):
    """Shared world builder for S04Predict end state and S05PredictPause backdrop."""
    fx = ValueTracker(fx_val)
    fork = build_fork(fx)
    fork_arr = VGroup(
        Arrow([fx_val + 0.3, 2.15, 0], [fx_val + 1.5, 2.15, 0], color=TEXT, stroke_width=5, buff=0),
        T("fork moves right", 24, TEXT).move_to([fx_val + 0.9, 2.52, 0]),
    )
    # Upper starter (3' faces fork on right; 3' badge cleanly inside the Y at y = Y_TOP - 0.88)
    u_start = dna_seg(-4.8, -2.5, Y_TOP - 0.30, NEW_CYAN, stroke=9)
    u_5 = M("5′", 24, NEW_CYAN).move_to([-5.08, Y_TOP - 0.32, 0])
    u_3 = end_badge("3′", [-2.50, Y_TOP - 0.90, 0], color=NEW_CYAN)
    u_clamp = poly_clamp([-2.55, Y_TOP - 0.30, 0], facing=RIGHT, color=ENZYME_GREEN, radius=0.34)
    # Lower starter shifted left (-3.8 to -1.75) so fork arm at fx=-1.2 never touches 5'
    l_start = dna_seg(-3.8, -1.75, -Y_TOP + 0.30, NEW_CYAN, stroke=9)
    l_3 = end_badge("3′", [-3.80, -Y_TOP + 0.90, 0], color=NEW_CYAN)
    l_5 = M("5′", 24, NEW_CYAN).move_to([-1.46, -Y_TOP + 0.32, 0])
    l_clamp = poly_clamp([-3.75, -Y_TOP + 0.30, 0], facing=LEFT, color=ENZYME_GREEN, radius=0.34)
    sc = scope_tag("schematic").move_to([-5.4, -3.25, 0])
    return VGroup(fork, fork_arr, u_start, u_5, u_3, u_clamp, l_start, l_3, l_5, l_clamp, sc)


class S04Predict(SpokenScene):
    def construct(self):
        fx = ValueTracker(-1.2)
        ph = ValueTracker(0.0)
        fork = build_fork(fx, ph)
        sc = scope_tag("schematic").move_to([-5.4, -3.25, 0])

        fork_arr = always_redraw(lambda: VGroup(
            Arrow([fx.get_value() + 0.3, 2.15, 0], [fx.get_value() + 1.5, 2.15, 0], color=TEXT, stroke_width=5, buff=0),
            T("fork moves right", 24, TEXT).move_to([fx.get_value() + 0.9, 2.52, 0]),
        ))
        u_start = dna_seg(-4.8, -2.5, Y_TOP - 0.30, NEW_CYAN, stroke=9)
        u_5 = M("5′", 24, NEW_CYAN).move_to([-5.08, Y_TOP - 0.32, 0])
        u_3 = end_badge("3′", [-2.50, Y_TOP - 0.90, 0], color=NEW_CYAN)
        u_clamp = poly_clamp([-2.55, Y_TOP - 0.30, 0], facing=RIGHT, color=ENZYME_GREEN, radius=0.34)

        l_start = dna_seg(-3.8, -1.75, -Y_TOP + 0.30, NEW_CYAN, stroke=9)
        l_3 = end_badge("3′", [-3.80, -Y_TOP + 0.90, 0], color=NEW_CYAN)
        l_5 = M("5′", 24, NEW_CYAN).move_to([-1.46, -Y_TOP + 0.32, 0])
        l_clamp = poly_clamp([-3.75, -Y_TOP + 0.30, 0], facing=LEFT, color=ENZYME_GREEN, radius=0.34)

        self.add(fork, sc, fork_arr, u_start, u_5, u_3, u_clamp, l_start, l_3, l_5, l_clamp)
        self.play(
            fx.animate(rate_func=linear).set_value(0.2),
            ph.animate(rate_func=linear).set_value(1.0),
            run_time=4.3,
        )

        self.at("Which")
        q = question_card("Which strand can follow the fork?", y=3.25, color=HIGHLIGHT_GOLD, size=32, max_w=11.6)
        pulse(u_start, base=9.0, amp=3.0, speed=4.0)
        pulse(l_start, base=9.0, amp=3.0, speed=4.0)
        self.play(
            FadeIn(q.question, shift=DOWN * 0.1),
            fx.animate(rate_func=linear).set_value(0.4),
            ph.animate(rate_func=linear).set_value(1.4),
            run_time=1.0,
        )

        self.at("while its polymerase")
        rest = max(0.2, self.narration_s + 0.3 - self.elapsed())
        self.play(
            fx.animate(rate_func=linear).set_value(0.8),
            ph.animate(rate_func=linear).set_value(2.2),
            run_time=rest,
        )
        self.finish()


class S05PredictPause(PredictPause):
    QUESTION = "Which strand can follow the fork?"
    CARD = {"y": 3.25, "size": 32, "max_w": 11.6}
    RING_AT = (5.9, -3.05, 0)
    SECONDS = 4.5

    def backdrop(self):
        return _s04_s05_world(0.8)


# ------------------------------------------------------------------ s06
class S06Leading(SpokenScene):
    def construct(self):
        fx = ValueTracker(0.8)
        ph = ValueTracker(0.0)
        lead_x = ValueTracker(-2.5)
        fork = build_fork(fx, ph)
        sc = scope_tag("schematic")

        l_start = dna_seg(-3.8, -1.75, -Y_TOP + 0.30, NEW_CYAN, stroke=9)
        l_3 = end_badge("3′", [-3.80, -Y_TOP + 0.90, 0], color=NEW_CYAN)
        l_5 = M("5′", 24, NEW_CYAN).move_to([-1.46, -Y_TOP + 0.32, 0])
        l_clamp = poly_clamp([-3.75, -Y_TOP + 0.30, 0], facing=LEFT, color=ENZYME_GREEN, radius=0.34)

        u_5 = M("5′", 24, NEW_CYAN).move_to([-5.08, Y_TOP - 0.32, 0])
        u_strand = always_redraw(lambda: dna_seg(-4.8, lead_x.get_value(), Y_TOP - 0.30, NEW_CYAN, stroke=10))
        u_3 = always_redraw(lambda: end_badge("3′", [lead_x.get_value(), Y_TOP - 0.90, 0], color=HIGHLIGHT_GOLD))
        u_clamp = always_redraw(lambda: poly_clamp(
            [lead_x.get_value() - 0.05, Y_TOP - 0.30, 0],
            facing=RIGHT, color=ENZYME_GREEN, radius=0.36
        ))

        self.add(fork, sc, l_start, l_3, l_5, l_clamp, u_5, u_strand, u_3, u_clamp)

        ring_hl = Circle(radius=0.42, color=HIGHLIGHT_GOLD, stroke_width=4).move_to([-2.50, Y_TOP - 0.90, 0])
        face_lbl = T("3′ end faces fork", 28, HIGHLIGHT_GOLD).move_to([-1.4, Y_TOP + 0.58, 0])
        self.play(Create(ring_hl), FadeIn(face_lbl), run_time=0.8)
        # Advance fork visibly while holding the highlight until "Polymerase follows"
        self.play(
            FadeOut(ring_hl, run_time=0.6),
            fx.animate(rate_func=linear).set_value(1.75),
            ph.animate(rate_func=linear).set_value(1.0),
            run_time=3.5,
        )

        self.at("Polymerase follows")
        lead_lbl = T("leading strand", 30, NEW_CYAN).move_to([-2.8, Y_TOP + 0.58, 0])
        self.play(swap(face_lbl, lead_lbl, run_time=0.7))
        self.play(
            fx.animate(rate_func=linear).set_value(2.65),
            lead_x.animate(rate_func=linear).set_value(1.95),
            ph.animate(rate_func=linear).set_value(1.8),
            run_time=4.8,
        )

        self.at("Its direction of synthesis")
        syn_arr = VGroup(
            Arrow([-4.4, 2.55, 0], [0.8, 2.55, 0], color=HIGHLIGHT_GOLD, stroke_width=5, buff=0),
            T("synthesis: 5′ → 3′", 28, HIGHLIGHT_GOLD).move_to([-1.8, 2.98, 0]),
        )
        self.play(FadeIn(syn_arr), run_time=0.6)
        rest = max(0.2, self.narration_s + 0.3 - self.elapsed())
        self.play(
            fx.animate(rate_func=linear).set_value(3.35),
            lead_x.animate(rate_func=linear).set_value(2.65),
            ph.animate(rate_func=linear).set_value(2.6),
            run_time=rest,
        )
        self.finish()


# ------------------------------------------------------------------ s07
class S07Lagging(SpokenScene):
    def construct(self):
        fx = ValueTracker(-0.2)
        ph = ValueTracker(0.0)
        fork = build_fork(fx, ph)
        sc = scope_tag("schematic")

        u_5 = M("5′", 24, NEW_CYAN).move_to([-5.08, Y_TOP - 0.32, 0])
        u_strand = always_redraw(lambda: dna_seg(-4.8, fx.get_value() - 0.55, Y_TOP - 0.30, NEW_CYAN, stroke=8))
        u_clamp = always_redraw(lambda: poly_clamp(
            [fx.get_value() - 0.60, Y_TOP - 0.30, 0],
            facing=RIGHT, color=ENZYME_GREEN, radius=0.30
        ))
        u_lbl = T("leading", 24, NEW_CYAN).move_to([-4.0, Y_TOP + 0.55, 0])

        # Previous lagging piece on far left (-5.0 to -3.5) with 5' clear of next fragment (-2.65)
        prev_frag = dna_seg(-5.0, -3.5, -Y_TOP + 0.30, NEW_CYAN, stroke=9)
        prev_3 = end_badge("3′", [-5.0, -Y_TOP + 0.90, 0], color=HIGHLIGHT_GOLD)
        prev_5 = M("5′", 24, NEW_CYAN).move_to([-3.22, -Y_TOP + 0.30, 0])

        self.add(fork, sc, u_5, u_strand, u_clamp, u_lbl, prev_frag, prev_3, prev_5)

        away_arr = VGroup(
            Arrow([-3.2, -Y_TOP - 0.55, 0], [-5.3, -Y_TOP - 0.55, 0], color=HIGHLIGHT_GOLD, stroke_width=5, buff=0),
            T("3′ faces away from fork", 28, HIGHLIGHT_GOLD).move_to([-2.7, -Y_TOP - 1.05, 0]),
        )
        self.play(FadeIn(away_arr), run_time=0.9)
        self.play(
            fx.animate(rate_func=linear).set_value(0.85),
            ph.animate(rate_func=linear).set_value(1.2),
            run_time=4.5,
        )

        self.at("Polymerase cannot reverse")
        no_rev = VGroup(
            T("×", 34, STOP_RED).move_to([-1.2, -Y_TOP + 0.30, 0]),
            T("cannot reverse 3′ → 5′", 26, STOP_RED).move_to([1.2, -Y_TOP - 0.55, 0]),
        )
        self.play(FadeIn(no_rev), run_time=0.7)
        self.play(
            FadeOut(no_rev), FadeOut(away_arr),
            fx.animate(rate_func=linear).set_value(1.15),
            run_time=1.4,
        )

        self.at("Primase starts near")
        self.play(
            fx.animate(rate_func=linear).set_value(1.55),
            ph.animate(rate_func=linear).set_value(1.6),
            run_time=0.5,
        )
        # Keep primase box clearly above p1_3 badge (-Y_TOP + 0.88 = -0.42) so they never touch
        primase = boxed_label("primase", ENZYME_GREEN, size=24, fill_opacity=0.25).move_to([0.52, -Y_TOP + 1.56, 0])
        p1 = primer_seg(0.2, 0.85, -Y_TOP + 0.30, PRIMER_YELLOW, height=0.22)
        p1_3 = end_badge("3′", [0.2, -Y_TOP + 0.84, 0], color=HIGHLIGHT_GOLD)
        self.play(FadeIn(primase, shift=DOWN * 0.1), FadeIn(p1), FadeIn(p1_3), run_time=0.55)
        self.play(FadeOut(primase), FadeOut(p1_3), run_time=0.30)

        self.at("then polymerase extends")
        f1_x = ValueTracker(0.2)
        f1_strand = always_redraw(lambda: dna_seg(f1_x.get_value(), 0.2, -Y_TOP + 0.30, NEW_CYAN, stroke=9))
        lag_clamp = always_redraw(lambda: poly_clamp(
            [f1_x.get_value() + 0.05, -Y_TOP + 0.30, 0],
            facing=LEFT, color=ENZYME_GREEN, radius=0.33
        ))
        self.add(f1_strand, lag_clamp)
        self.play(
            f1_x.animate(rate_func=linear).set_value(-2.60),
            ph.animate(rate_func=linear).set_value(2.4),
            run_time=2.8,
        )

        self.at("As more template")
        self.play(
            fx.animate(rate_func=linear).set_value(2.85),
            ph.animate(rate_func=linear).set_value(3.0),
            FadeOut(lag_clamp, run_time=0.3),
            run_time=1.1,
        )
        p2 = primer_seg(1.9, 2.55, -Y_TOP + 0.30, PRIMER_YELLOW, height=0.22)
        primase2 = boxed_label("primase", ENZYME_GREEN, size=24, fill_opacity=0.25).move_to([2.22, -Y_TOP + 1.56, 0])
        self.play(FadeIn(primase2), FadeIn(p2), run_time=0.5)
        f2_x = ValueTracker(1.9)
        f2_strand = always_redraw(lambda: dna_seg(f2_x.get_value(), 1.9, -Y_TOP + 0.30, NEW_CYAN, stroke=9))
        lag_clamp2 = always_redraw(lambda: poly_clamp(
            [f2_x.get_value() + 0.05, -Y_TOP + 0.30, 0],
            facing=LEFT, color=ENZYME_GREEN, radius=0.33
        ))
        self.play(FadeOut(primase2, run_time=0.25))
        self.add(f2_strand, lag_clamp2)
        self.play(
            f2_x.animate(rate_func=linear).set_value(1.25),
            ph.animate(rate_func=linear).set_value(3.6),
            run_time=1.65,
        )

        self.at("These pieces")
        # Brace cleanly below lower purple template (-Y_TOP - 0.18)
        brace_ref = Line([-5.0, -Y_TOP - 0.18, 0], [2.55, -Y_TOP - 0.18, 0])
        ok_brace = Brace(brace_ref, DOWN, buff=0.04, color=HIGHLIGHT_GOLD)
        ok_lbl = T("Okazaki fragments (lagging strand)", 28, HIGHLIGHT_GOLD).next_to(ok_brace, DOWN, buff=0.14)
        self.play(
            Create(ok_brace), FadeIn(ok_lbl),
            f2_x.animate(rate_func=linear).set_value(0.95),
            run_time=1.0,
        )
        rest = max(0.1, self.narration_s + 0.3 - self.elapsed())
        self.play(
            f2_x.animate(rate_func=linear).set_value(0.60),
            fx.animate(rate_func=linear).set_value(3.3),
            ph.animate(rate_func=linear).set_value(4.3),
            run_time=rest,
        )
        self.finish()


# ------------------------------------------------------------------ s08
class S08Processing(SpokenScene):
    def construct(self):
        head = T("Joining Okazaki fragments into one continuous strand", 30, TEXT).move_to([0, 3.2, 0])
        sc = scope_tag("schematic")

        ty = -0.85
        ny = -0.25
        tmpl = Line([-5.8, ty, 0], [5.8, ty, 0], color=PARENTAL_PURPLE, stroke_width=9)
        t_lbl = T("lower parental template", 24, PARENTAL_PURPLE).move_to([-3.4, ty - 0.55, 0])

        frag_l = dna_seg(-5.6, -2.2, ny, NEW_CYAN, stroke=12)
        frag_m = dna_seg(-0.65, 2.1, ny, NEW_CYAN, stroke=12)
        frag_r = dna_seg(3.65, 5.6, ny, NEW_CYAN, stroke=12)

        def make_primer_blocks(x0, x1, count=4):
            w = (x1 - x0) / count
            return VGroup(*[
                RoundedRectangle(
                    corner_radius=0.06, width=w - 0.05, height=0.38,
                    color=PRIMER_YELLOW, fill_opacity=0.92, stroke_color=TEXT, stroke_width=1.6
                ).move_to([x0 + (i + 0.5) * w, ny, 0])
                for i in range(count)
            ])

        pr1 = make_primer_blocks(-2.05, -0.65, 4)
        pr2 = make_primer_blocks(2.25, 3.65, 4)
        pr_lbl = T("RNA primers", 26, PRIMER_YELLOW).move_to([0.75, ny + 0.65, 0])

        zoomed = VGroup(tmpl, t_lbl, frag_l, frag_m, frag_r, pr1, pr2, pr_lbl)
        self.play(FadeIn(head), FadeIn(sc), FadeIn(zoomed, scale=0.95), run_time=1.0)
        # Highlight primer 1 then primer 2 while waiting for "DNA polymerase"
        hl1 = SurroundingRectangle(pr1, color=PRIMER_YELLOW, buff=0.08, stroke_width=3)
        hl2 = SurroundingRectangle(pr2, color=PRIMER_YELLOW, buff=0.08, stroke_width=3)
        self.play(Create(hl1), run_time=1.1)
        self.play(ReplacementTransform(hl1, hl2), run_time=1.2)
        self.play(FadeOut(hl2), run_time=0.6)

        self.at("DNA polymerase")
        pol1 = boxed_label("Pol I", ENZYME_GREEN, size=26, fill_opacity=0.28).move_to([-2.4, ny + 0.78, 0])
        self.play(FadeOut(pr_lbl, run_time=0.25), FadeIn(pol1, shift=DOWN * 0.1), run_time=0.45)

        for b in pr1:
            bx = b.get_center()[0]
            self.play(pol1.animate.move_to([bx, ny + 0.78, 0]), run_time=0.26)
            new_b = RoundedRectangle(
                corner_radius=0.06, width=b.width, height=0.38,
                color=NEW_CYAN, fill_opacity=0.92, stroke_color=TEXT, stroke_width=1.6
            ).move_to(b.get_center())
            self.play(Transform(b, new_b), run_time=0.16)

        self.play(pol1.animate.move_to([2.0, ny + 0.78, 0]), run_time=0.4)
        for b in pr2:
            bx = b.get_center()[0]
            self.play(pol1.animate.move_to([bx, ny + 0.78, 0]), run_time=0.25)
            new_b = RoundedRectangle(
                corner_radius=0.06, width=b.width, height=0.38,
                color=NEW_CYAN, fill_opacity=0.92, stroke_color=TEXT, stroke_width=1.6
            ).move_to(b.get_center())
            self.play(Transform(b, new_b), run_time=0.16)

        nick1 = Arrow([-0.65, ny - 0.85, 0], [-0.65, ny - 0.16, 0], color=STOP_RED, stroke_width=4, buff=0)
        nick2 = Arrow([3.65, ny - 0.85, 0], [3.65, ny - 0.16, 0], color=STOP_RED, stroke_width=4, buff=0)
        nick_lbl = T("nick", 26, STOP_RED).move_to([-0.65, ny - 1.12, 0])
        self.play(FadeOut(pol1, run_time=0.25), FadeIn(nick1), FadeIn(nick2), FadeIn(nick_lbl), run_time=0.45)

        self.at("DNA ligase")
        lig = boxed_label("ligase", ENZYME_GREEN, size=26, fill_opacity=0.28).move_to([-0.65, ny + 0.82, 0])
        pulse1 = Circle(radius=0.38, color=HIGHLIGHT_GOLD, stroke_width=5).move_to([-0.65, ny, 0])
        pulse2 = Circle(radius=0.38, color=HIGHLIGHT_GOLD, stroke_width=5).move_to([3.65, ny, 0])
        solid_lag = dna_seg(-5.6, 5.6, ny, NEW_CYAN, stroke=12)

        self.play(FadeIn(lig, shift=DOWN * 0.1), run_time=0.5)
        self.play(
            Create(pulse1), FadeOut(nick1), FadeOut(nick_lbl),
            lig.animate.move_to([3.65, ny + 0.82, 0]),
            run_time=0.9,
        )
        self.play(Create(pulse2), FadeOut(nick2), run_time=0.6)
        self.play(
            FadeOut(lig), FadeOut(pulse1), FadeOut(pulse2),
            FadeOut(pr1), FadeOut(pr2), FadeOut(frag_l), FadeOut(frag_m), FadeOut(frag_r),
            FadeIn(solid_lag),
            run_time=0.7,
        )

        self.at("The finished lagging")
        fx = ValueTracker(0.5)
        ph = ValueTracker(0.0)
        fork = build_fork(fx, ph)
        full_lead = always_redraw(lambda: dna_seg(-4.8, fx.get_value() - 0.3, Y_TOP - 0.30, NEW_CYAN, stroke=9))
        full_lag = always_redraw(lambda: dna_seg(-4.8, fx.get_value() - 0.6, -Y_TOP + 0.30, NEW_CYAN, stroke=9))
        fin_lbl = T("finished lagging strand: continuous", 28, NEW_CYAN).move_to([-1.2, -Y_TOP - 0.65, 0])

        self.play(
            FadeOut(tmpl, run_time=0.5),
            FadeOut(t_lbl, run_time=0.5),
            FadeOut(solid_lag, run_time=0.5),
            FadeIn(fork, run_time=0.7),
            FadeIn(full_lead, run_time=0.7),
            FadeIn(full_lag, run_time=0.7),
            FadeIn(fin_lbl, run_time=0.8),
        )
        rest = max(0.1, self.narration_s + 0.3 - self.elapsed())
        self.play(
            fx.animate(rate_func=linear).set_value(3.0),
            ph.animate(rate_func=linear).set_value(2.0),
            run_time=rest,
        )
        self.finish()


# ------------------------------------------------------------------ s09
class S09Jobs(SpokenScene):
    def construct(self):
        slot_xs = [-4.6, -2.4, -0.2, 2.0, 4.4]
        slot_y = 3.15
        sc = scope_tag("schematic")
        org_tag = T("E. coli", 24, GREY).move_to([-5.6, -3.25, 0])

        fx = ValueTracker(-1.5)
        ph = ValueTracker(0.0)
        fork = build_fork(fx, ph, y_arm=1.25, y_dup=0.22)
        self.add(fork, sc, org_tag)

        self.play(fx.animate(rate_func=linear).set_value(-0.3), ph.animate(rate_func=linear).set_value(0.8), run_time=3.9)

        # 1. DnaB helicase opens the Y — placed cleanly inside the open mouth of the Y (y=0.0)
        self.at("helicase")
        dnab_fork = always_redraw(lambda: boxed_label(
            "DnaB", ENZYME_GREEN, size=24, fill_opacity=0.25
        ).move_to([fx.get_value() - 0.85, 0.0, 0]))
        self.play(FadeIn(dnab_fork), run_time=0.5)
        self.play(
            fx.animate(rate_func=linear).set_value(0.5),
            ph.animate(rate_func=linear).set_value(1.4),
            run_time=2.6,
        )
        slot1 = boxed_label("DnaB", ENZYME_GREEN, size=24, fill_opacity=0.22).move_to([slot_xs[0], slot_y, 0])
        self.play(FadeIn(slot1, shift=UP * 0.2), run_time=0.5)

        # 2. SSB coats exposed purple single strands (ahead of nascent duplexes near fork)
        self.at("binding protein")
        ssb_top = VGroup(*[Circle(radius=0.13, color=ENZYME_GREEN, fill_opacity=0.9, stroke_color=TEXT, stroke_width=1.2)
                           .move_to([x, 1.25, 0]) for x in (-1.5, -0.9, -0.3)])
        ssb_bot = VGroup(*[Circle(radius=0.13, color=ENZYME_GREEN, fill_opacity=0.9, stroke_color=TEXT, stroke_width=1.2)
                           .move_to([x, -1.25, 0]) for x in (-1.5, -0.9, -0.3)])
        ssb_lbl = T("SSB", 26, ENZYME_GREEN).move_to([-0.9, 1.75, 0])
        self.play(FadeIn(ssb_top), FadeIn(ssb_bot), FadeIn(ssb_lbl), run_time=0.8)
        slot2 = boxed_label("SSB", ENZYME_GREEN, size=24, fill_opacity=0.22).move_to([slot_xs[1], slot_y, 0])
        self.play(FadeOut(ssb_lbl, run_time=0.35), FadeIn(slot2, run_time=0.45))

        # 3. Gyrase relieves overwinding ahead (needle gauge without invented percentage)
        self.at("and gyrase")
        twist = ValueTracker(0.82)
        g_dial = overwinding_gauge(twist, center=[4.65, 1.85, 0], radius=0.85, label="overwinding", color=STOP_RED)
        gyr_block = boxed_label("gyrase", ENZYME_GREEN, size=24, fill_opacity=0.25).move_to([3.4, -0.82, 0])
        self.play(FadeIn(g_dial), FadeIn(gyr_block), run_time=0.7)
        self.play(twist.animate.set_value(0.22), run_time=1.8)
        slot3 = boxed_label("gyrase", ENZYME_GREEN, size=24, fill_opacity=0.22).move_to([slot_xs[2], slot_y, 0])
        self.play(FadeIn(slot3, shift=UP * 0.2), FadeOut(g_dial), run_time=0.6)

        # 4. DnaG primase places a yellow primer
        self.at("primase")
        dnag = boxed_label("DnaG", ENZYME_GREEN, size=24, fill_opacity=0.25).move_to([-0.2, -1.95, 0])
        p_yel = primer_seg(-0.5, 0.2, -0.95, PRIMER_YELLOW, height=0.20)
        self.play(FadeIn(dnag), FadeIn(p_yel), run_time=0.8)
        slot4 = boxed_label("DnaG", ENZYME_GREEN, size=24, fill_opacity=0.22).move_to([slot_xs[3], slot_y, 0])
        self.play(FadeOut(dnag, run_time=0.35), FadeIn(slot4, run_time=0.45))

        # 5. Pol III + beta clamp extends cyan DNA on both strands until narration ends
        self.at("DNA polymerase")
        lead_x = ValueTracker(-3.6)
        lag_x = ValueTracker(-0.5)
        lead_s = always_redraw(lambda: dna_seg(-4.8, lead_x.get_value(), 0.95, NEW_CYAN, stroke=8))
        lag_s = always_redraw(lambda: dna_seg(lag_x.get_value(), -0.5, -0.95, NEW_CYAN, stroke=8))
        c_lead = always_redraw(lambda: poly_clamp([lead_x.get_value() - 0.05, 0.95, 0], facing=RIGHT, color=ENZYME_GREEN, radius=0.30))
        c_lag = always_redraw(lambda: poly_clamp([lag_x.get_value() + 0.05, -0.95, 0], facing=LEFT, color=ENZYME_GREEN, radius=0.30))
        slot5 = boxed_label("Pol III + β clamp", ENZYME_GREEN, size=24, fill_opacity=0.22).move_to([slot_xs[4], slot_y, 0])
        self.add(lead_s, lag_s, c_lead, c_lag)
        rest = max(3.5, self.narration_s + 0.3 - self.elapsed())
        self.play(
            FadeIn(slot5, shift=UP * 0.2),
            fx.animate(rate_func=linear).set_value(1.8),
            lead_x.animate(rate_func=linear).set_value(-1.8),
            lag_x.animate(rate_func=linear).set_value(-3.2),
            ph.animate(rate_func=linear).set_value(2.8),
            run_time=rest,
        )
        self.finish()


# ------------------------------------------------------------------ s10
class S10Eukaryotes(SpokenScene):
    def construct(self):
        slot_y = 3.15
        sc = scope_tag("schematic")
        org = T("Eukaryotes", 26, TEXT).move_to([-5.3, -3.25, 0])

        b_dnab = boxed_label("DnaB", ENZYME_GREEN, size=24, fill_opacity=0.22).move_to([-4.6, slot_y, 0])
        b_ssb = boxed_label("SSB", ENZYME_GREEN, size=24, fill_opacity=0.22).move_to([-2.4, slot_y, 0])
        b_gyr = boxed_label("gyrase", ENZYME_GREEN, size=24, fill_opacity=0.22).move_to([-0.2, slot_y, 0])
        b_dnag = boxed_label("DnaG", ENZYME_GREEN, size=24, fill_opacity=0.22).move_to([2.0, slot_y, 0])
        b_pol3 = boxed_label("Pol III + β clamp", ENZYME_GREEN, size=24, fill_opacity=0.22).move_to([4.4, slot_y, 0])

        bw = ValueTracker(0.45)
        bar_y = 0.85
        orig_xs = [-3.6, 0.0, 3.6]

        def _bubbles():
            w = bw.get_value()
            g = VGroup()
            prev_x = -5.7
            for ox in orig_xs:
                lx, rx = ox - w, ox + w
                if lx > prev_x:
                    g.add(Line([prev_x, bar_y + 0.14, 0], [lx, bar_y + 0.14, 0], color=PARENTAL_PURPLE, stroke_width=5))
                    g.add(Line([prev_x, bar_y - 0.14, 0], [lx, bar_y - 0.14, 0], color=PARENTAL_PURPLE, stroke_width=5))
                g.add(VMobject(stroke_color=PARENTAL_PURPLE, stroke_width=5, fill_opacity=0).set_points_as_corners([
                    [lx, bar_y + 0.14, 0], [lx + 0.25, bar_y + 0.62, 0], [rx - 0.25, bar_y + 0.62, 0], [rx, bar_y + 0.14, 0]
                ]))
                g.add(VMobject(stroke_color=PARENTAL_PURPLE, stroke_width=5, fill_opacity=0).set_points_as_corners([
                    [lx, bar_y - 0.14, 0], [lx + 0.25, bar_y - 0.62, 0], [rx - 0.25, bar_y - 0.62, 0], [rx, bar_y - 0.14, 0]
                ]))
                if w > 0.35:
                    g.add(Line([ox - 0.1, bar_y + 0.44, 0], [rx - 0.32, bar_y + 0.44, 0], color=NEW_CYAN, stroke_width=5))
                    g.add(Line([lx + 0.32, bar_y - 0.44, 0], [ox + 0.1, bar_y - 0.44, 0], color=NEW_CYAN, stroke_width=5))
                prev_x = rx
            g.add(Line([prev_x, bar_y + 0.14, 0], [5.7, bar_y + 0.14, 0], color=PARENTAL_PURPLE, stroke_width=5))
            g.add(Line([prev_x, bar_y - 0.14, 0], [5.7, bar_y - 0.14, 0], color=PARENTAL_PURPLE, stroke_width=5))
            return g

        bubbles = always_redraw(_bubbles)
        many_lbl = T("many origins", 26, PARENTAL_PURPLE).move_to([0, 2.05, 0])

        ly_top, ly_bot = -0.82, -2.18
        l_tmpl_u = Line([-5.2, ly_top, 0], [5.2, ly_top, 0], color=PARENTAL_PURPLE, stroke_width=6)
        l_tmpl_l = Line([-5.2, ly_bot, 0], [5.2, ly_bot, 0], color=PARENTAL_PURPLE, stroke_width=6)
        lbl_lead_trk = T("leading track", 24, NEW_CYAN).move_to([-4.2, ly_top + 0.38, 0])
        lbl_lag_trk = T("lagging track", 24, NEW_CYAN).move_to([-4.2, ly_bot - 0.38, 0])

        self.add(sc, org, b_dnab, b_ssb, b_gyr, b_dnag, b_pol3, bubbles, many_lbl,
                 l_tmpl_u, l_tmpl_l, lbl_lead_trk, lbl_lag_trk)
        # Clear all E. coli header chips cleanly as eukaryotic origin bubbles expand (no mixed-organism row)
        self.play(
            FadeOut(b_dnab, run_time=1.0),
            FadeOut(b_ssb, run_time=0.8),
            FadeOut(b_gyr, run_time=0.8),
            FadeOut(b_dnag, run_time=1.0),
            FadeOut(b_pol3, run_time=1.0),
            bw.animate(rate_func=linear).set_value(0.95),
            run_time=4.5,
        )

        self.at("CMG is the helicase")
        e_cmg = boxed_label("CMG", ENZYME_GREEN, size=24, fill_opacity=0.22).move_to([-4.2, slot_y, 0])
        self.play(FadeIn(e_cmg, shift=DOWN * 0.1), bw.animate(rate_func=linear).set_value(1.15), run_time=1.8)

        self.at("Polymerase alpha primase")
        e_pola = boxed_label("Pol α-primase", ENZYME_GREEN, size=24, fill_opacity=0.22).move_to([-1.4, slot_y, 0])
        p_lag = primer_seg(1.4, 2.2, ly_bot + 0.28, PRIMER_YELLOW, height=0.20)
        self.play(FadeIn(e_pola, shift=DOWN * 0.1), FadeIn(p_lag), bw.animate(rate_func=linear).set_value(1.30), run_time=2.2)

        self.at("The usual summary")
        qual = boxed_label("usual summary", HIGHLIGHT_GOLD, size=24, pad=0.14, fill_opacity=0.18).move_to([0.0, -3.25, 0])
        e_pole = boxed_label("Pol ε", ENZYME_GREEN, size=24, fill_opacity=0.22).move_to([1.3, slot_y, 0])
        # Lead DNA ends cleanly left of Pol epsilon box (no straddle with box or purple track)
        lead_dna = dna_seg(-3.2, 2.0, ly_top - 0.28, NEW_CYAN, stroke=9)
        pole_fork = boxed_label("Pol ε", ENZYME_GREEN, size=24, fill_opacity=0.88).move_to([2.9, ly_top - 0.44, 0])
        pole_fork.box.set_stroke(TEXT, 2)
        pole_fork.label.set_color(BG)
        self.play(
            FadeIn(qual),
            FadeIn(e_pole, shift=DOWN * 0.1),
            Create(lead_dna),
            FadeIn(pole_fork),
            bw.animate(rate_func=linear).set_value(1.48),
            run_time=3.6,
        )

        self.at("It assigns most lagging")
        e_pold = boxed_label("Pol δ + PCNA", ENZYME_GREEN, size=24, fill_opacity=0.22).move_to([4.1, slot_y, 0])
        # Lagging DNA starts cleanly right of Pol delta box (no straddle with box or purple track)
        lag_dna = dna_seg(-0.7, 1.4, ly_bot + 0.28, NEW_CYAN, stroke=9)
        pold_fork = boxed_label("Pol δ + PCNA", ENZYME_GREEN, size=24, fill_opacity=0.88).move_to([-2.2, ly_bot + 0.46, 0])
        pold_fork.box.set_stroke(TEXT, 2)
        pold_fork.label.set_color(BG)
        rest = max(2.8, self.narration_s + 0.3 - self.elapsed())
        self.play(
            FadeIn(e_pold, shift=DOWN * 0.1),
            Create(lag_dna),
            FadeIn(pold_fork),
            bw.animate(rate_func=linear).set_value(1.65),
            run_time=rest,
        )
        self.finish()


# ------------------------------------------------------------------ s11
class S11JobMap(SpokenScene):
    def construct(self):
        fx = ValueTracker(-1.4)
        sc = scope_tag("schematic")

        def _low_fork():
            fval = fx.get_value()
            g = VGroup()
            y_off = -1.55
            for rx in RUNG_XS:
                if rx < -5.1 or rx > 5.1:
                    continue
                if rx >= fval + FORK_OPEN_DX - 0.05:
                    yu = _fork_y(rx, fval, +1, 0.85, 0.18) + y_off
                    yl = _fork_y(rx, fval, -1, 0.85, 0.18) + y_off
                    g.add(Line([rx, yl + 0.03, 0], [rx, yu - 0.03, 0], color=PARENTAL_PURPLE, stroke_width=2.0, stroke_opacity=0.4))
            for sign in (+1, -1):
                pts = [p + UP * y_off for p in _fork_pts(fval, sign, -5.2, 5.2, 0.85, 0.18)]
                s = VMobject(stroke_color=PARENTAL_PURPLE, stroke_width=6.0, fill_opacity=0).set_points_as_corners(pts)
                g.add(s)
            return g

        low_fork = always_redraw(_low_fork)

        jobs = ["open", "start", "extend", "replace", "seal"]
        j_xs = [-3.4, -1.45, 0.5, 2.45, 4.4]
        j_y = 1.45
        nodes = VGroup(*[
            boxed_label(j, GREY, size=26, box=(1.58, 0.68), fill_opacity=0.14).move_to([x, j_y, 0])
            for j, x in zip(jobs, j_xs)
        ])
        arrows = VGroup(*[
            Arrow([j_xs[i] + 0.84, j_y, 0], [j_xs[i + 1] - 0.84, j_y, 0], color=GREY, stroke_width=3, buff=0)
            for i in range(4)
        ])
        head = T("Every fork solves the same five jobs", 32, TEXT).move_to([0, 3.2, 0])

        self.add(low_fork, sc, head, nodes, arrows)
        self.play(fx.animate(rate_func=linear).set_value(-0.3), run_time=4.5)

        def light(idx):
            nodes[idx].box.set_stroke(HIGHLIGHT_GOLD, 3.5).set_fill(HIGHLIGHT_GOLD, 0.25)
            nodes[idx].label.set_color(HIGHLIGHT_GOLD)

        self.at("open DNA")
        light(0)
        self.play(fx.animate(rate_func=linear).set_value(0.3), run_time=1.2)

        self.at("Start new chains")
        light(1)
        p_mark = primer_seg(-1.0, -0.3, -1.55 - 0.65, PRIMER_YELLOW, height=0.18)
        self.play(FadeIn(p_mark), fx.animate(rate_func=linear).set_value(0.7), run_time=1.0)

        self.at("extend them")
        light(2)
        c_lead = dna_seg(-4.6, 0.7, -1.55 + 0.65, NEW_CYAN, stroke=7)
        c_lag = dna_seg(-2.4, -1.0, -1.55 - 0.65, NEW_CYAN, stroke=7)
        self.play(Create(c_lead), Create(c_lag), fx.animate(rate_func=linear).set_value(1.1), run_time=1.0)

        self.at("replace starter")
        light(3)
        rep_mark = dna_seg(-1.0, -0.3, -1.55 - 0.65, NEW_CYAN, stroke=7)
        self.play(FadeOut(p_mark), FadeIn(rep_mark), fx.animate(rate_func=linear).set_value(1.5), run_time=1.1)

        self.at("and seal")
        light(4)
        seal_dot = Circle(radius=0.25, color=HIGHLIGHT_GOLD, stroke_width=4).move_to([-1.0, -1.55 - 0.65, 0])
        pulse_dot = Dot(radius=0.14, color=HIGHLIGHT_GOLD).move_to([j_xs[0], j_y - 0.56, 0])
        self.play(Create(seal_dot), FadeIn(pulse_dot), run_time=0.45)
        self.play(
            FadeOut(seal_dot),
            pulse_dot.animate(rate_func=linear).move_to([j_xs[-1], j_y - 0.56, 0]),
            fx.animate(rate_func=linear).set_value(1.9),
            run_time=1.35,
        )
        self.play(FadeOut(pulse_dot), run_time=0.25)

        self.at("The text compares")
        bac_names = ["DnaB", "DnaG", "Pol III", "Pol I", "ligase"]
        euk_names = ["CMG", "Pol α-primase", "Pol ε / δ", "", ""]
        bac_row = VGroup(*[
            T(n, 24, ENZYME_GREEN).move_to([x, j_y + 0.72, 0])
            for n, x in zip(bac_names, j_xs)
        ])
        euk_row = VGroup(*[
            T(n, 24, NEW_CYAN).move_to([x, j_y - 0.78, 0])
            for n, x in zip(euk_names, j_xs) if n
        ])
        bac_tag = T("E. coli", 24, GREY).move_to([-5.35, j_y + 0.72, 0])
        euk_tag = T("Eukaryotes", 24, GREY).move_to([-5.35, j_y - 0.78, 0])
        self.play(
            FadeIn(bac_row), FadeIn(euk_row), FadeIn(bac_tag), FadeIn(euk_tag),
            fx.animate(rate_func=linear).set_value(2.4),
            run_time=2.5,
        )
        rest = max(0.1, self.narration_s + 0.3 - self.elapsed())
        self.play(fx.animate(rate_func=linear).set_value(3.0), run_time=rest)
        self.finish()


# ------------------------------------------------------------------ s12
class S12Rule(SpokenScene):
    def construct(self):
        fx = ValueTracker(-1.4)
        ph = ValueTracker(0.0)
        fork = build_fork(fx, ph)
        sc = scope_tag("schematic")

        lead_x = ValueTracker(-4.2)
        u_5 = M("5′", 24, NEW_CYAN).move_to([-5.08, Y_TOP - 0.32, 0])
        u_strand = always_redraw(lambda: dna_seg(-4.8, lead_x.get_value(), Y_TOP - 0.30, NEW_CYAN, stroke=10))
        u_3 = always_redraw(lambda: end_badge("3′", [lead_x.get_value(), Y_TOP - 0.90, 0], color=HIGHLIGHT_GOLD, size=24))
        u_clamp = always_redraw(lambda: poly_clamp([lead_x.get_value() - 0.05, Y_TOP - 0.30, 0], facing=RIGHT, color=ENZYME_GREEN, radius=0.36))

        f1 = dna_seg(-4.8, -2.6, -Y_TOP + 0.30, NEW_CYAN, stroke=10)
        p1 = primer_seg(-2.6, -2.0, -Y_TOP + 0.30, PRIMER_YELLOW, height=0.22)

        self.add(fork, sc, u_5, u_strand, u_3, u_clamp, f1, p1)

        p2 = primer_seg(-0.1, 0.5, -Y_TOP + 0.30, PRIMER_YELLOW, height=0.22)
        f2_x = ValueTracker(-0.1)
        f2 = always_redraw(lambda: dna_seg(f2_x.get_value(), -0.1, -Y_TOP + 0.30, NEW_CYAN, stroke=10))
        l_3 = always_redraw(lambda: end_badge("3′", [f2_x.get_value(), -Y_TOP + 0.90, 0], color=HIGHLIGHT_GOLD, size=24))
        l_clamp = always_redraw(lambda: poly_clamp([f2_x.get_value() + 0.05, -Y_TOP + 0.30, 0], facing=LEFT, color=ENZYME_GREEN, radius=0.36))

        self.play(
            FadeIn(p2),
            fx.animate(rate_func=linear).set_value(0.7),
            lead_x.animate(rate_func=linear).set_value(0.05),
            ph.animate(rate_func=linear).set_value(0.8),
            run_time=2.5,
        )
        self.add(f2, l_3, l_clamp)
        self.play(
            f2_x.animate(rate_func=linear).set_value(-1.95),
            fx.animate(rate_func=linear).set_value(1.5),
            lead_x.animate(rate_func=linear).set_value(0.85),
            ph.animate(rate_func=linear).set_value(1.6),
            run_time=3.2,
        )

        self.at("Both strands still obey")
        chem_lbl = T("same 5′ → 3′ chemistry on both strands", 30, HIGHLIGHT_GOLD).move_to([0, 3.15, 0])
        arr_u = Arrow([-4.2, Y_TOP + 0.50, 0], [-1.2, Y_TOP + 0.50, 0], color=HIGHLIGHT_GOLD, stroke_width=5, buff=0)
        arr_l = Arrow([0.4, -Y_TOP - 0.52, 0], [-2.6, -Y_TOP - 0.52, 0], color=HIGHLIGHT_GOLD, stroke_width=5, buff=0)
        self.play(
            FadeIn(chem_lbl), FadeIn(arr_u), FadeIn(arr_l),
            fx.animate(rate_func=linear).set_value(2.2),
            lead_x.animate(rate_func=linear).set_value(1.55),
            ph.animate(rate_func=linear).set_value(2.2),
            run_time=2.8,
        )

        self.at("The enzyme never changes")
        joined_left = dna_seg(-4.8, -0.1, -Y_TOP + 0.30, NEW_CYAN, stroke=10)
        p3 = primer_seg(1.7, 2.3, -Y_TOP + 0.30, PRIMER_YELLOW, height=0.22)
        f3_x = ValueTracker(1.7)
        f3 = always_redraw(lambda: dna_seg(f3_x.get_value(), 1.7, -Y_TOP + 0.30, NEW_CYAN, stroke=10))
        self.play(
            FadeOut(f1), FadeOut(p1), FadeOut(f2), FadeIn(joined_left),
            FadeOut(l_3), FadeOut(l_clamp),
            FadeIn(p3),
            fx.animate(rate_func=linear).set_value(2.6),
            lead_x.animate(rate_func=linear).set_value(1.95),
            ph.animate(rate_func=linear).set_value(2.8),
            run_time=2.5,
        )
        l_3b = always_redraw(lambda: end_badge("3′", [f3_x.get_value(), -Y_TOP + 0.90, 0], color=HIGHLIGHT_GOLD, size=24))
        l_clamp_b = always_redraw(lambda: poly_clamp([f3_x.get_value() + 0.05, -Y_TOP + 0.30, 0], facing=LEFT, color=ENZYME_GREEN, radius=0.36))
        self.add(f3, l_3b, l_clamp_b)

        self.at("This constraint turns")
        lbl_top = T("continuous leading strand", 28, NEW_CYAN).move_to([1.2, Y_TOP + 0.55, 0])
        lbl_bot = T("pieces on lagging strand", 28, NEW_CYAN).move_to([1.2, -Y_TOP - 1.05, 0])
        self.play(
            FadeIn(lbl_top), FadeIn(lbl_bot),
            f3_x.animate(rate_func=linear).set_value(0.55),
            fx.animate(rate_func=linear).set_value(3.2),
            lead_x.animate(rate_func=linear).set_value(2.55),
            ph.animate(rate_func=linear).set_value(3.6),
            run_time=4.0,
        )
        self.finish()


# ------------------------------------------------------------------ s13
class S13End(EndCard):
    LINE = "Polymerases extend a 3′ end, so one strand is built in pieces."
