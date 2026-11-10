"""Where ffmpeg and ffprobe live on this machine.

The films were first built with the copies in ~/miniconda3/bin, so those are used when they
exist; on any other machine the copies on PATH (Homebrew, for example) are used.
"""
import shutil
from pathlib import Path


def _find(name):
    conda = Path.home() / "miniconda3/bin" / name
    return str(conda) if conda.exists() else (shutil.which(name) or name)


FFMPEG = _find("ffmpeg")
FFPROBE = _find("ffprobe")
