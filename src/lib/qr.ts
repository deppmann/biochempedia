/* QR codes, drawn when the site is built. No outside service and no script on the page:
   the code is a plain SVG path in the HTML. Used by src/components/LessonShare.astro. */
import qrcode from 'qrcode-generator';

export interface QrSvg {
  /** Side of the square viewBox, in modules, quiet zone included. */
  size: number;
  /** One path for all the dark modules: a 1-unit-high bar for each run in each row. */
  path: string;
}

/** `text` as a QR code. Error correction M (15%); the smallest version that fits; a 4-module quiet zone. */
export function qrSvg(text: string, quiet = 4): QrSvg {
  const qr = qrcode(0, 'M');
  qr.addData(text, 'Byte');
  qr.make();
  const n = qr.getModuleCount();
  let path = '';
  for (let r = 0; r < n; r++) {
    for (let c = 0; c < n; c++) {
      if (!qr.isDark(r, c)) continue;
      let len = 1;
      while (c + len < n && qr.isDark(r, c + len)) len++;
      path += `M${c + quiet} ${r + quiet}h${len}v1h-${len}z`;
      c += len;
    }
  }
  return { size: n + 2 * quiet, path };
}
