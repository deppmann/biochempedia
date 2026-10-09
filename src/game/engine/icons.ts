/* Small line icons for the arcade's game cards. Single colour (currentColor),
   24px grid, 1.75 stroke, matching the lessons' line-icon style. */
const wrap = (body: string): string =>
  `<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">${body}</svg>`;

export const GAME_ICONS: Record<string, string> = {
  // receipt / ledger with a tally line
  ledger: wrap('<path d="M6 3h12v18l-2.5-1.7L13 21l-2.5-1.7L8 21l-2-1.4z"/><path d="M9 8h6M9 12h6M9 16h3"/>'),
  // magnifier
  autopsy: wrap('<circle cx="10.5" cy="10.5" r="6"/><path d="m15 15 5.5 5.5"/><path d="M8 10.5h5M10.5 8v5"/>'),
  // plug
  wire: wrap('<path d="M9 3v5M15 3v5"/><path d="M6 8h12v3a6 6 0 0 1-12 0z"/><path d="M12 17v4"/>'),
  // factory
  foundry: wrap('<path d="M3 21V10l6 3.5V10l6 3.5V5h3v16z"/><path d="M7 17h2M12 17h2M17 17h1"/>'),
  // sliders
  mixing: wrap('<path d="M5 4v16M12 4v16M19 4v16"/><rect x="3" y="14" width="4" height="3" rx="1"/><rect x="10" y="7" width="4" height="3" rx="1"/><rect x="17" y="12" width="4" height="3" rx="1"/>'),
  // graduation cap
  gauntlet: wrap('<path d="m2.5 9.5 9.5-5 9.5 5-9.5 5z"/><path d="M6.5 12v4.5c0 1.2 2.5 2.5 5.5 2.5s5.5-1.3 5.5-2.5V12"/><path d="M21.5 9.5V15"/>'),
};
