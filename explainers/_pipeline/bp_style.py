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


def _norm(w):
    return re.sub(r"[^a-z0-9']", "", w.lower())


class SpokenScene(NarratedScene):
    """NarratedScene + word-level sync to the REAL audio.

    self.at("phrase")      waits until the narrator starts saying that phrase (minus a 0.2 s lead).
    self.t_of("phrase")    seconds into the scene when the phrase starts.
    Word timings come from audio/words.json (written by align.py from a transcript of the audio).
    Match the phrase to the words as spoken (see script.json "narration"); punctuation/case ignored.
    Every phrase you sync to must exist, or the render fails loudly (good: it means a typo).
    A log of how late each cue landed goes to sync.log in the video directory.
    """

    def _words(self):
        if not hasattr(self, "_wl"):
            sid = os.environ["KX_SCENE_ID"]
            vdir = Path(os.environ["KX_SCRIPT"]).parent
            words = json.loads((vdir / "audio" / "words.json").read_text())[sid]
            self._wl = [(float(w[0]), _norm(w[2])) for w in words if _norm(w[2])]
        return self._wl

    def t_of(self, phrase, nth=0):
        toks = [_norm(p) for p in phrase.split() if _norm(p)]
        wl = self._words()
        hits = [wl[i][0] for i in range(len(wl) - len(toks) + 1) if [x[1] for x in wl[i:i + len(toks)]] == toks]
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


class EndCard(NarratedScene):
    """Closing card: the take-home line. Subclass and set LINE (<= 12 words)."""
    LINE = "Try the interactive in the lesson."

    def construct(self):
        line = T(self.LINE, size=40, font=TITLE_FONT)
        fit(line, max_w=11.5)
        sub = T("biochemistrypedia.com", size=22, color=TEAL)
        g = VGroup(line, sub).arrange(DOWN, buff=0.4)
        self.play(FadeIn(line, shift=UP * 0.15), run_time=self.beat(0.3))
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        self.finish()
