# Bundled fonts

Oswald.bin: unchanged Oswald binary; copyright and full SIL OFL 1.1 in Oswald-LICENSE.txt.
LiberationSerif.bin: unchanged /usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf from Debian fonts-liberation; copyright and full SIL OFL 1.1 in LiberationSerif-LICENSE.txt. Only renamed file extension for Wrangler Data binding; font contents/names unchanged.

FreeSerif was removed from this candidate to avoid shipping a GPL font binary without its corresponding source. Liberation Serif is a visually similar Times-style serif with Cyrillic, Greek and Latin coverage. This is the only typeface change; Oswald headings remain unchanged.

name-metrics.json records cmap/hmtx advances divided by unitsPerEm from the exact bundled Liberation Serif, generated using fontTools. Image admission is narrower than cmap: Latin, Greek, Cyrillic, numbers, punctuation and separators, excluding combining/control characters. Unsupported scripts/emoji use the explicit “Имя — в подписи” label, never missing-glyph boxes. Caption retains the exact original profile string. No claim of universal Unicode/emoji image coverage.

Keep these copyright/license files with any redistribution of the binaries. Fonts may not be sold alone; modified fonts are subject to the reserved-name clauses. Images themselves are not subject to OFL.
