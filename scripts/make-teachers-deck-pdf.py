#!/usr/bin/env python3
"""Rebuild public/teachers/Fast_Tools_Slow_Thinking.pdf: the MAIN path of the talk deck only.

    python3 scripts/make-teachers-deck-pdf.py

Needs the talk's local server running (python3 "<workshop folder>/talk/serve.py", port 8765),
Google Chrome, and Pillow. It screenshots each main step at 1920x1080 in headless Chrome and
combines the pictures into one PDF (JPEG pages, so it stays under 10 MB). The number of main steps
is read from public/teachers/talk/deck.json, so run scripts/refresh-teachers-deck.mjs first.
Movies show their poster frame. The PDF is pictures, so the same text is on /teachers.
"""
import json
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from PIL import Image

CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
SERVER = 'http://localhost:8765/slides/talk/'
OUT = Path('public/teachers/Fast_Tools_Slow_Thinking.pdf')
N = len(json.load(open('public/teachers/talk/deck.json'))['steps'])   # main steps only (the public deck has no appendix)

tmp = Path(tempfile.mkdtemp(prefix='deck-shots-'))


def shoot(i: int) -> Path:
    f = tmp / f's{i:02d}.png'
    subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=1',
                    '--window-size=1920,1080', '--virtual-time-budget=6000', f'--screenshot={f}', f'{SERVER}#{i}'],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    return f


with ThreadPoolExecutor(4) as ex:
    files = list(ex.map(shoot, range(1, N + 1)))
imgs = [Image.open(f).convert('RGB') for f in files]
imgs[0].save(OUT, save_all=True, append_images=imgs[1:], resolution=96.0, quality=80)
mb = OUT.stat().st_size / 1e6
print(f'{N} pages, {mb:.1f} MB -> {OUT}')
if mb > 10:
    sys.exit('over 10 MB: lower the JPEG quality')
