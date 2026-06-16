from PIL import Image
import glob, os
pngs = sorted(glob.glob('public/slides/*/*.png'))
before = sum(os.path.getsize(f) for f in pngs)
full_bytes = thumb_bytes = 0
for f in pngs:
    base = f[:-4]  # strip .png
    with Image.open(f) as im:
        im = im.convert('RGB')
        w, h = im.size
        # full: cap width at 1320, never upscale
        fw = min(w, 1320); fh = round(h * fw / w)
        full = im.resize((fw, fh), Image.LANCZOS) if fw != w else im
        full.save(base + '.webp', 'WEBP', quality=80, method=6)
        full_bytes += os.path.getsize(base + '.webp')
        # thumb: cap width at 480
        tw = min(w, 480); th = round(h * tw / w)
        thumb = im.resize((tw, th), Image.LANCZOS)
        thumb.save(base + '.thumb.webp', 'WEBP', quality=72, method=6)
        thumb_bytes += os.path.getsize(base + '.thumb.webp')
print(f"converted {len(pngs)} PNGs")
print(f"  PNG total:   {before/1e6:.1f} MB")
print(f"  WebP full:   {full_bytes/1e6:.1f} MB")
print(f"  WebP thumb:  {thumb_bytes/1e6:.1f} MB")
print(f"  new total:   {(full_bytes+thumb_bytes)/1e6:.1f} MB  ({100*(full_bytes+thumb_bytes)/before:.0f}% of original)")
