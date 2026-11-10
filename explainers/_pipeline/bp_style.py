"""Shared look for the Biochemistrypedia explainer videos (all 10 lessons use this).

    from bp_style import *          # NarratedScene, colors, fonts, helpers, and all of manim

Rules every scene follows:
- 3b1b look: dark background, things transform into each other, build piece by piece,
  hold still while the narration lands.
- ONE color per concept for the whole video (pick from BLUE/YELLOW/GREEN/RED/GREY and keep it).
- NEVER draw a molecular structure (no bond-line/skeletal formulas, no ball-and-stick, no ring
  drawings, no atom-by-atom geometry). Biochemistrypedia's integrity policy forbids AI-drawn
  molecules. Use labelled boxes/chips, schematic blobs, arrows, timelines, energy diagrams, and
  PLOTS COMPUTED FROM EQUATIONS (Michaelis-Menten, Hill, Henderson-Hasselbalch...). A name like
  "glucose" or "H2O" in text is fine; a drawn structure is not.
- Keep everything inside the safe frame (SAFE_W x SAFE_H), nothing overlapping, text >= 24 px
  at 1080p (font_size >= 22 in Manim units here).
- No burned-in subtitles: captions ship as a separate .vtt track.
"""
import json, os, re
import numpy as np
from pathlib import Path
from manim import *  # noqa: F401,F403
from kx_manim import NarratedScene, BG, BLUE, YELLOW, GREEN, RED, GREY, TEXT  # noqa: F401

# Manim's partial-movie cache reused STALE clips across re-renders in the first batch
# (scene lengths drifted between renders). Always render fresh.
config.disable_caching = True

FONT = "Avenir Next"     # labels and body
TITLE_FONT = "Georgia"   # titles (stands in for the site's Playfair Display)
MONO = "Menlo"           # numbers, units, equations
TEAL = "#3FB8C0"         # Biochemistrypedia's interactive cue, lifted for a dark ground
GOLD = "#D4A843"         # Biochemistrypedia gold, used sparingly (title rule, one highlight)

SAFE_W = 12.6   # Manim frame is 14.22 x 8 units; keep content inside this
SAFE_H = 7.0
VERTICAL = os.environ.get("KX_ASPECT") == "vertical"   # render.py --vertical: a 9:16 social cut
if VERTICAL:
    # Frame is 8 wide x 14.22 tall. Social apps cover the top ~10% and bottom ~20% with their own
    # buttons, and make_social.py burns captions at about y = -3.9, so keep the subject in
    # x -3.5..3.5, y -3.0..5.4 (centre near y = +1.2) and leave y -4.6..-3.2 clear for captions.
    config.frame_width, config.frame_height = 8.0, 8.0 * 16 / 9
    SAFE_W, SAFE_H = 7.0, 8.4
    V_CENTER = UP * 1.2


# Spoken number words and the digits a transcriber writes for them are the same token (Kokoro, 2026-10-31).
_NUM = {w: str(i) for i, w in enumerate("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty".split())}
_NUM.update(thirty="30", forty="40", fifty="50", sixty="60", seventy="70", eighty="80", ninety="90", hundred="100", thousand="1000", million="1000000")


def _norm(w):
    w = re.sub(r"[^a-z0-9']", "", w.lower())
    return _NUM.get(w, w)


class SpokenScene(NarratedScene):
    """NarratedScene + word-level sync to the REAL audio.

    self.at("phrase")      waits until the narrator starts saying that phrase (minus a 0.2 s lead).
    self.t_of("phrase")    seconds into the scene when the phrase starts.
    Word timings come from audio/words.json (written by align.py from a transcript of the audio).
    Match the phrase to the words as spoken (see script.json "narration"); punctuation/case ignored.
    Every phrase you sync to must exist, or the render fails loudly (good: it means a typo).
    A log of how late each cue landed goes to sync.log in the video directory.
    """

    def setup(self):
        """script.json "ambient": true adds a slow field of faint drifting motes behind everything, so a
        held frame is never a dead frame (a zero-token fix for old films; 2026-11-09). New films should
        animate their own world instead."""
        super().setup()
        try:
            on = json.loads(Path(os.environ["KX_SCRIPT"]).read_text()).get("ambient")
        except Exception:
            on = False
        if not on:
            return
        import random
        rng = random.Random(os.environ.get("KX_SCENE_ID", "x"))
        W, H = config.frame_width, config.frame_height
        motes = VGroup()
        for _ in range(26):
            d = Dot(radius=rng.uniform(0.02, 0.05), color=rng.choice([TEAL, GREY, TEXT])).set_opacity(rng.uniform(0.10, 0.28))
            d.move_to([rng.uniform(-W / 2, W / 2), rng.uniform(-H / 2, H / 2), 0])
            d.v = (rng.uniform(-0.10, 0.10), rng.uniform(0.04, 0.16))

            def drift(m, dt, W=W, H=H):
                m.shift([m.v[0] * dt, m.v[1] * dt, 0])
                if m.get_y() > H / 2 + 0.1:
                    m.shift(DOWN * (H + 0.2))
                if abs(m.get_x()) > W / 2 + 0.1:
                    m.shift(LEFT * (W + 0.2) * (1 if m.get_x() > 0 else -1))
            d.add_updater(drift)
            motes.add(d)
        motes.set_z_index(-10)
        self.add(motes)

    def _words(self):
        if not hasattr(self, "_wl"):
            sid = os.environ["KX_SCENE_ID"]
            vdir = Path(os.environ["KX_SCRIPT"]).parent
            words = json.loads((vdir / os.environ.get("KX_AUDIO", "audio") / "words.json").read_text())[sid]
            # A dash can glue two words into one transcript token ("1155—outward"): split it, both at the token's start.
            self._wl = [(float(w[0]), _norm(p)) for w in words for p in re.split(r"[\u2014\u2013]", w[2]) if _norm(p)]
        return self._wl

    def t_of(self, phrase, nth=0):
        toks = [_norm(p) for p in re.split(r"[\s\u2014\u2013]+", phrase) if _norm(p)]
        wl = self._words()
        hits = [wl[i][0] for i in range(len(wl) - len(toks) + 1) if [x[1] for x in wl[i:i + len(toks)]] == toks]
        if len(hits) <= nth and nth == 0 and toks:
            # A re-voiced line can be transcribed a little differently ("metabolisms" for "metabolism"): take
            # the closest run of words if it is a near match, so a re-pace needs no hand edits (2026-11-09).
            import difflib
            sim = lambda i: sum(difflib.SequenceMatcher(None, a, b[1]).ratio() for a, b in zip(toks, wl[i:i + len(toks)])) / len(toks)
            cand = [(sim(i), -i) for i in range(len(wl) - len(toks) + 1)]
            if cand and max(cand)[0] >= 0.82:
                i = -max(cand)[1]
                with open(Path(os.environ["KX_SCRIPT"]).parent / "sync.log", "a") as lg:
                    lg.write(f"{os.environ.get('KX_SCENE_ID')}  FUZZY {phrase!r} ~ {' '.join(w[1] for w in wl[i:i + len(toks)])!r}\n")
                return wl[i][0]
        if len(hits) <= nth:
            raise ValueError(f"phrase not spoken in {os.environ.get('KX_SCENE_ID')}: {phrase!r} (nth={nth})")
        return hits[nth]

    def at(self, phrase, lead=0.2, nth=0):
        target = self.t_of(phrase, nth) - lead
        rest = target - self.elapsed()
        with open(Path(os.environ["KX_SCRIPT"]).parent / "sync.log", "a") as lg:
            lg.write(f"{os.environ.get('KX_SCENE_ID')}  {phrase[:30]!r:36} at {target + lead:6.2f}  "
                     f"now {self.elapsed():6.2f}  late {-rest:+5.2f}\n")
        if rest > 0.02:
            self.wait(rest)


def T(text, size=30, color=TEXT, font=FONT, weight=NORMAL, **kw):
    """Plain label text in the house font."""
    return Text(text, font=font, font_size=size, color=color, weight=weight, **kw)


def M(text, size=30, color=TEXT, **kw):
    """Monospace text for numbers, units and equations (no LaTeX available)."""
    return Text(text, font=MONO, font_size=size, color=color, **kw)


def chip(text, color=BLUE, size=28, pad=0.22, fill_opacity=0.16):
    """A rounded labelled box: the standard stand-in for a molecule, enzyme or compartment."""
    label = T(text, size=size, color=color)
    box = RoundedRectangle(corner_radius=0.14, width=label.width + 2 * pad, height=label.height + 2 * pad,
                           stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=fill_opacity)
    return VGroup(box, label.move_to(box))


def fit(mob, max_w=SAFE_W, max_h=SAFE_H):
    """Scale a mobject down (never up) so it fits the safe frame."""
    s = min(1.0, max_w / max(mob.width, 1e-6), max_h / max(mob.height, 1e-6))
    return mob.scale(s)


class TitleCard(NarratedScene):
    """Opening card. Subclass and set LESSON and TITLE; it runs for the s00 silent clip."""
    LESSON = "Lesson"
    TITLE = "Explainer"

    def construct(self):
        brand = T("BIOCHEMISTRYPEDIA", size=20, color=TEAL, weight=BOLD).set_opacity(0.9)
        lesson = T(self.LESSON.upper(), size=22, color=GREY)
        title = T(self.TITLE, size=54, font=TITLE_FONT)
        fit(title, max_w=11.5)
        rule = Line(LEFT * 1.2, RIGHT * 1.2, color=GOLD, stroke_width=4)
        g = VGroup(brand, lesson, title, rule).arrange(DOWN, buff=0.32)
        self.play(FadeIn(brand, shift=UP * 0.1), FadeIn(lesson, shift=UP * 0.1), run_time=self.beat(0.25))
        self.play(Write(title), GrowFromCenter(rule), run_time=self.beat(0.35))
        self.wait(self.beat(0.2))
        self.play(FadeOut(g), run_time=self.beat(0.2))
        self.finish()


def hex_mascot(height=1.5):
    """Hex, the site's mascot (src/components/Hex.astro), drawn for a film's dark ground: a pale
    outline, gold for the three inner bonds and the feet. `.arm` is the waving arm and `.shoulder`
    the point it turns about. A hexagon with a face is a character, not a molecular structure."""
    P = lambda x, y: np.array([x - 32.0, 36.0 - y, 0.0])   # the component's 64 x 72 drawing, y up
    ink, gold = 4.2 * height, 3.6 * height
    body = Polygon(*[P(*q) for q in [(32, 10), (49.3, 20), (49.3, 40), (32, 50), (14.7, 40), (14.7, 20)]],
                   color=TEXT, stroke_width=ink, fill_color=TEXT, fill_opacity=0.07)
    bonds = VGroup(Line(P(32, 14.8), P(45.2, 22.4)), Line(P(45.2, 37.6), P(32, 45.2)), Line(P(18.8, 37.6), P(18.8, 22.4))).set_stroke(GOLD, gold)
    eyes = VGroup(Dot(P(26.5, 28), radius=2.2, color=TEXT), Dot(P(37.5, 28), radius=2.2, color=TEXT))
    smile = ArcBetweenPoints(P(28, 34.5), P(36, 34.5), angle=1.5).set_stroke(TEXT, ink * 0.8)
    legs = VGroup(Line(P(27, 48), P(25.5, 60)), Line(P(37, 48), P(38.5, 60))).set_stroke(TEXT, ink)
    feet = VGroup(Line(P(22.5, 61), P(27.5, 61)), Line(P(36.5, 61), P(41.5, 61))).set_stroke(GOLD, gold)
    arm_l = Line(P(14.7, 32), P(8, 39)).set_stroke(TEXT, ink)
    arm_r = Line(P(49.3, 27), P(58, 17)).set_stroke(TEXT, ink)
    g = VGroup(legs, feet, arm_l, arm_r, body, bonds, eyes, smile)
    for m in g.family_members_with_points():
        try:
            m.set_cap_style(CapStyleType.ROUND)
            m.joint_type = LineJointType.ROUND
        except Exception:
            pass
    g.set_height(height)
    g.arm = arm_r
    return g


class EndCard(NarratedScene):
    """Closing card: Hex waves over the take-home line. Subclass and set LINE (<= 12 words).
    Hex was added 2026-11-10; a film rendered before that keeps its plain card until it is re-rendered."""
    LINE = "Try the interactive in the lesson."

    def construct(self):
        hexm = hex_mascot(1.5)
        line = T(self.LINE, size=40, font=TITLE_FONT)
        fit(line, max_w=11.5)
        sub = T("biochemistrypedia.com", size=22, color=TEAL)
        g = VGroup(hexm, line, sub).arrange(DOWN, buff=0.4)
        self.play(FadeIn(hexm, shift=UP * 0.2), FadeIn(line, shift=UP * 0.15), run_time=self.beat(0.3))
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        shoulder = hexm.arm.get_start()
        for _ in range(2):
            self.play(Rotate(hexm.arm, angle=-0.55, about_point=shoulder), rate_func=there_and_back, run_time=self.beat(0.14))
        self.finish()
