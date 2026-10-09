"""NarratedScene: a Manim CE Scene that is paced to its narration length.

Usage in scenes.py (render.py puts this directory on PYTHONPATH):
    from kx_manim import NarratedScene, BLUE, YELLOW, GREEN, RED, GREY

    class S01Problem(NarratedScene):
        def construct(self):
            self.play(FadeIn(dot), run_time=self.beat(0.2))   # 20% of the narration
            self.wait(self.beat(0.3))                          # hold while the words land
            self.finish()                                      # wait out the rest + 0.4 s tail

KX_DURATION (seconds, float) is the narration length; render.py sets it from durations.json.
No LaTeX: use Text / MarkupText only.
"""
import os

from manim import Scene, config

# 3b1b-like: dark background, one color per concept for the whole video.
BG = "#0f1117"
BLUE = "#58C4DD"    # the enzyme / main subject
YELLOW = "#F5D547"  # the thing that moves or is highlighted
GREEN = "#83C167"   # on / go / product
RED = "#FC6255"     # off / stop / problem
GREY = "#8B93A1"    # labels, structure, de-emphasized
TEXT = "#E8EAF0"
PALETTE = {"blue": BLUE, "yellow": YELLOW, "green": GREEN, "red": RED, "grey": GREY}

TAIL = 0.4  # seconds of stillness after the narration ends


class NarratedScene(Scene):
    def __init__(self, *args, **kwargs):
        config.background_color = BG
        super().__init__(*args, **kwargs)
        # not `self.duration`: Manim's Scene uses that name internally
        self.narration_s = float(os.environ.get("KX_DURATION", "5.0"))

    def beat(self, fraction):
        """Seconds equal to `fraction` of the narration length (for run_time or wait)."""
        return max(0.05, fraction * self.narration_s)

    def elapsed(self):
        return self.renderer.time

    def finish(self):
        """Hold the last frame until the scene is at least narration length + TAIL."""
        remaining = self.narration_s + TAIL - self.elapsed()
        if remaining > 0:
            self.wait(remaining)
