/* export-canvas.js — reliable 1080×1920 PNG renderer for the cover templates.
   Canvas draws text with the already-loaded document fonts (no embedding) and
   drawImage for photos, so it never hangs the way html-to-image does on the
   heavy Google-Fonts @import. Mirrors the layouts in Templates.jsx.

   window.renderCoverCanvas(cfg, tplId) -> Promise<HTMLCanvasElement> (1080×1920)
*/
(function () {
  const W = 1080, H = 1920, M = Math.round(0.095 * W); // 103 outer margin

  const DISPLAY = '"Cormorant Garamond", serif';
  const ROMAN   = '"Forum", serif';
  const COND    = '"Oswald", sans-serif';

  const gradeHex = (g) => {
    const G = window.GRADES || {};
    return G[g] ? G[g].hex : (g || '#1B2838');
  };
  const inkFor = (grade, source) =>
    (source === 'color' && ['rose', 'sand', 'cyan'].includes(grade)) ? '#1C1A16' : '#EDE9E0';

  function loadImg(src) {
    return new Promise((res) => {
      if (!src) return res(null);
      const im = new Image();
      im.crossOrigin = 'anonymous';
      im.onload = () => res(im);
      im.onerror = () => res(null);
      im.src = src;
    });
  }

  function drawPhoto(ctx, img, focusX, focusY, filter, scaleMul) {
    const s = Math.max(W / img.width, H / img.height) * (scaleMul || 1);
    const dw = img.width * s, dh = img.height * s;
    const dx = (W - dw) * (focusX / 100), dy = (H - dh) * (focusY / 100);
    ctx.save();
    if (filter) ctx.filter = filter;
    ctx.drawImage(img, dx, dy, dw, dh);
    ctx.restore();
  }

  function gradeWash(ctx, grade) {
    ctx.save();
    ctx.globalCompositeOperation = 'soft-light';
    ctx.globalAlpha = 0.55;
    ctx.fillStyle = gradeHex(grade);
    ctx.fillRect(0, 0, W, H);
    ctx.restore();
  }

  function duotone(ctx) {
    ctx.save();
    ctx.globalCompositeOperation = 'lighten';
    ctx.globalAlpha = 0.92;
    const g = ctx.createLinearGradient(0, 0, W * 0.55, H); // ~155deg
    g.addColorStop(0, '#E5267F');
    g.addColorStop(1, '#F5A623');
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, W, H);
    ctx.restore();
  }

  function scrim(ctx, kind) {
    if (!kind || kind === 'none') return;
    ctx.save();
    if (kind === 'vignette') {
      const g = ctx.createRadialGradient(W / 2, H * 0.42, W * 0.30, W / 2, H * 0.42, W * 0.85);
      g.addColorStop(0, 'rgba(8,8,9,0)');
      g.addColorStop(1, 'rgba(8,8,9,0.55)');
      ctx.fillStyle = g; ctx.fillRect(0, 0, W, H); ctx.restore(); return;
    }
    let g;
    if (kind === 'bottom') {
      g = ctx.createLinearGradient(0, H, 0, 0);
      g.addColorStop(0, 'rgba(8,8,9,0.88)');
      g.addColorStop(0.22, 'rgba(8,8,9,0.55)');
      g.addColorStop(0.52, 'rgba(8,8,9,0)');
    } else if (kind === 'top') {
      g = ctx.createLinearGradient(0, 0, 0, H);
      g.addColorStop(0, 'rgba(8,8,9,0.78)');
      g.addColorStop(0.26, 'rgba(8,8,9,0.30)');
      g.addColorStop(0.50, 'rgba(8,8,9,0)');
    } else { // full
      g = ctx.createLinearGradient(0, H, 0, 0);
      g.addColorStop(0, 'rgba(8,8,9,0.80)');
      g.addColorStop(0.55, 'rgba(8,8,9,0.30)');
      g.addColorStop(1, 'rgba(8,8,9,0.45)');
    }
    ctx.fillStyle = g; ctx.fillRect(0, 0, W, H); ctx.restore();
  }

  let grainTile = null;
  function makeGrain() {
    if (grainTile) return grainTile;
    const t = document.createElement('canvas'); t.width = 160; t.height = 160;
    const tc = t.getContext('2d');
    const id = tc.createImageData(160, 160);
    for (let i = 0; i < id.data.length; i += 4) {
      const v = (Math.random() * 255) | 0;
      id.data[i] = id.data[i + 1] = id.data[i + 2] = v; id.data[i + 3] = 255;
    }
    tc.putImageData(id, 0, 0);
    grainTile = t; return t;
  }
  function grain(ctx, heavy) {
    ctx.save();
    ctx.globalCompositeOperation = 'overlay';
    ctx.globalAlpha = heavy ? 0.18 : 0.10;
    const p = ctx.createPattern(makeGrain(), 'repeat');
    ctx.fillStyle = p; ctx.fillRect(0, 0, W, H);
    ctx.restore();
  }

  // wrap text into lines that fit maxW (letterSpacing already set on ctx)
  function wrap(ctx, text, maxW) {
    const words = String(text).split(' ');
    const out = []; let cur = '';
    for (const w of words) {
      const t = cur ? cur + ' ' + w : w;
      if (ctx.measureText(t).width > maxW && cur) { out.push(cur); cur = w; }
      else cur = t;
    }
    if (cur) out.push(cur);
    return out;
  }

  // A text item: { text, family, weight, size, lh, trackEm, color, alpha, upper, italic, maxW }
  // Auto-fit: wrap() can only break on spaces, so a single long word (frequent in
  // Russian titles) overflows maxW at the template's base size. Shrink the font
  // until the widest unbreakable word fits, floor at 50% of the base size.
  function prep(ctx, it) {
    let size = it.size;
    const maxW = it.maxW || (W - 2 * M);
    const txt = it.upper ? String(it.text).toUpperCase() : String(it.text);
    const floor = size * 0.5;
    const setFont = () => {
      ctx.font = (it.italic ? 'italic ' : '') + (it.weight || 400) + ' ' + size + 'px ' + it.family;
      ctx.letterSpacing = ((it.trackEm || 0) * size) + 'px';
    };
    for (let pass = 0; pass < 4; pass++) {
      setFont();
      const words = txt.split(' ').filter(Boolean);
      const widest = words.length ? Math.max.apply(null, words.map(w => ctx.measureText(w).width)) : 0;
      if (widest <= maxW || size <= floor) break;
      size = Math.max(floor, size * (maxW / widest) * 0.99);
    }
    it.size = size;
    setFont();
    const ls = wrap(ctx, txt, maxW);
    it._lines = ls;
    it._lineH = size * (it.lh || 1.1);
    it._h = ls.length * it._lineH;
    // QA hook: expose fit metrics so the gate can assert lines stay inside maxW
    const maxLine = ls.length ? Math.max.apply(null, ls.map(l => ctx.measureText(l).width)) : 0;
    (window.__fitMetrics = window.__fitMetrics || []).push({ size: size, maxLine: maxLine, maxW: maxW });
    return it;
  }

  function drawItem(ctx, it, cx, topY) {
    ctx.save();
    ctx.textAlign = 'center';
    ctx.textBaseline = 'alphabetic';
    ctx.fillStyle = it.color;
    ctx.globalAlpha = it.alpha == null ? 1 : it.alpha;
    ctx.font = (it.italic ? 'italic ' : '') + (it.weight || 400) + ' ' + it.size + 'px ' + it.family;
    const trackPx = (it.trackEm || 0) * it.size;
    ctx.letterSpacing = trackPx + 'px';
    // nudge left by half the trailing letter-spacing so centered text stays centered
    const x = cx - trackPx / 2;
    it._lines.forEach((ln, i) => {
      const baseline = topY + i * it._lineH + it.size * 0.80;
      ctx.fillText(ln, x, baseline);
    });
    ctx.restore();
  }

  // Stack a set of items vertically; anchor controls vertical placement.
  function drawStack(ctx, items, opts) {
    items.forEach(it => prep(ctx, it));
    const gaps = opts.gaps || [];
    const total = items.reduce((s, it) => s + it._h, 0) + gaps.reduce((s, g) => s + g, 0);
    let y;
    if (opts.anchor === 'top') y = opts.topY;
    else if (opts.anchor === 'bottom') y = opts.bottomY - total;
    else y = (H - total) / 2; // center
    const cx = opts.cx == null ? W / 2 : opts.cx;
    items.forEach((it, i) => {
      drawItem(ctx, it, cx, y);
      y += it._h + (gaps[i] || 0);
    });
  }

  function base(ctx, cfg, tplId, img, scrimKind, grainHeavy, isDuotone) {
    ctx.save(); ctx.translate(-(cfg.textX || 0), -(cfg.textY || 0));
    // background
    if (cfg.source === 'photo' && img) {
      var _bw = (isDuotone || cfg.bw);
      var _f = (_bw ? 'grayscale(1) ' : '') + 'brightness(' + ((cfg.brightness ?? 1) * (_bw ? 0.95 : 1)) + ') contrast(' + ((cfg.contrast ?? 1) * (_bw ? 1.15 : 1)) + ')';
      drawPhoto(ctx, img, cfg.focusX ?? 50, focusYFor(cfg, tplId), _f, cfg.photoScale ?? 1);
      if (isDuotone) duotone(ctx); else gradeWash(ctx, cfg.grade);
    } else {
      ctx.fillStyle = gradeHex(cfg.grade);
      ctx.fillRect(0, 0, W, H);
    }
    scrim(ctx, cfg.source === 'photo' || isDuotone ? scrimKind : 'none');
    if (cfg.darken) { ctx.save(); ctx.fillStyle = 'rgba(8,8,9,' + cfg.darken + ')'; ctx.fillRect(0, 0, W, H); ctx.restore(); }
    grain(ctx, grainHeavy);
    ctx.restore();
  }

  function focusYFor(cfg, tplId) {
    if (cfg.focusY != null) return cfg.focusY;
    return ({ whisper: 62, centerpiece: 78, monolith: 50, billing: 32, duotone: 42, spine: 64 })[tplId] ?? 50;
  }

  const RENDER = {
    whisper(ctx, cfg, img) {
      base(ctx, cfg, 'whisper', img, 'vignette', false, false);
      const ink = inkFor(cfg.grade, cfg.source);
      const ts = cfg.titleScale ?? 1;
      const items = [{ text: cfg.title, family: COND, weight: 300, size: 60 * ts, lh: 1.0,
        trackEm: 0.62, color: ink, upper: true, maxW: W - 1.4 * M }];
      drawStack(ctx, items, { anchor: 'center', gaps: [] });
    },
    centerpiece(ctx, cfg, img) {
      base(ctx, cfg, 'centerpiece', img, 'top', false, false);
      const ink = inkFor(cfg.grade, cfg.source);
      const ts = cfg.titleScale ?? 1;
      const items = []; const gaps = [];
      items.push({ text: cfg.title, family: DISPLAY, weight: 500, size: 150 * ts, lh: 0.96, trackEm: 0.02,
        color: ink, maxW: W - 1.2 * M });
      if (cfg.tagline) { gaps.push(48); items.push({ text: cfg.tagline, family: DISPLAY, italic: true,
        weight: 400, size: 40 * (cfg.taglineScale ?? 1), lh: 1.2, trackEm: 0.01, color: ink, alpha: 0.92, maxW: W * 0.74 }); }
      drawStack(ctx, items, { anchor: 'top', topY: H * 0.18, gaps });
    },
    monolith(ctx, cfg, img) {
      base(ctx, cfg, 'monolith', img, 'none', false, false);
      const ink = inkFor(cfg.grade, cfg.source);
      const sz = Math.round(150 * (cfg.titleScale ?? 1));
      // title: top-left, can wrap; prep() may shrink the size (auto-fit) — draw with it.size
      const it = prep(ctx, { text: cfg.title, family: COND, weight: 700, size: sz, lh: 0.84,
        trackEm: -0.02, color: ink, upper: true, maxW: W - 2 * M });
      const fsz = it.size;
      ctx.save();
      ctx.textAlign = 'left'; ctx.textBaseline = 'alphabetic'; ctx.fillStyle = ink;
      ctx.font = '700 ' + fsz + 'px ' + COND; ctx.letterSpacing = (-0.02 * fsz) + 'px';
      const startY = H * 0.12 + M + fsz * 0.80;
      it._lines.forEach((ln, i) => ctx.fillText(ln, M, startY + i * it._lineH));
      ctx.restore();
    },
    billing(ctx, cfg, img) {
      base(ctx, cfg, 'billing', img, 'full', true, false);
      const ink = inkFor(cfg.grade, cfg.source);
      const ts = cfg.titleScale ?? 1;
      const items = []; const gaps = [];
      if (cfg.tagline) { items.push({ text: cfg.tagline, family: COND, weight: 300, size: 30 * (cfg.taglineScale ?? 1), lh: 1.3,
        trackEm: 0.34, color: ink, upper: true, maxW: W - 1.6 * M }); gaps.push(34); }
      items.push({ text: cfg.title, family: ROMAN, weight: 400, size: 110 * ts, lh: 1.06, trackEm: 0.08,
        color: ink, upper: true, maxW: W - 1.4 * M });
      drawStack(ctx, items, { anchor: 'bottom', bottomY: H - 360, gaps });
    },
    duotone(ctx, cfg, img) {
      base(ctx, cfg, 'duotone', img, 'none', false, true);
      const ts = cfg.titleScale ?? 1;
      const items = [{ text: cfg.title, family: COND, weight: 600, size: 120 * ts, lh: 0.9, trackEm: -0.01,
        color: '#fff', upper: true, maxW: W - 1.2 * M }];
      drawStack(ctx, items, { anchor: 'bottom', bottomY: H - 320, gaps: [] });
      if (cfg.tagline) {
        // right-aligned tagline at ~54% height
        const tsz = 28 * (cfg.taglineScale ?? 1);
        ctx.save();
        ctx.textAlign = 'right'; ctx.textBaseline = 'top'; ctx.fillStyle = '#fff';
        ctx.font = '300 ' + tsz + 'px ' + COND; ctx.letterSpacing = (0.34 * tsz) + 'px';
        const lines = wrap(ctx, String(cfg.tagline).toUpperCase(), W * 0.42);
        lines.forEach((ln, i) => ctx.fillText(ln, W - M, H * 0.54 + i * tsz * 1.5));
        ctx.restore();
      }
    },
    spine(ctx, cfg, img) {
      base(ctx, cfg, 'spine', img, 'top', false, false);
      const ink = inkFor(cfg.grade, cfg.source);
      const items = [{ text: cfg.title, family: DISPLAY, weight: 500, size: 120 * (cfg.titleScale ?? 1), lh: 0.96, trackEm: 0.02,
        color: ink, maxW: W - 2 * M - 120 }];
      drawStack(ctx, items, { anchor: 'top', topY: H * 0.16, gaps: [], cx: (W + 96) / 2 });
      // left spine bar
      ctx.save(); ctx.translate(-(cfg.textX || 0), -(cfg.textY || 0));
      ctx.fillStyle = 'rgba(236,231,220,0.92)';
      ctx.fillRect(0, 0, 96, H);
      ctx.fillStyle = '#1C1A16';
      ctx.textAlign = 'center'; ctx.textBaseline = 'alphabetic';
      ctx.font = '600 52px ' + DISPLAY; ctx.letterSpacing = '0px';
      ctx.fillText('C', 48, 40 + 52);
      // vertical collection label (center)
      ctx.translate(48, H / 2); ctx.rotate(Math.PI / 2);
      ctx.font = '300 22px ' + COND; ctx.letterSpacing = (0.34 * 22) + 'px';
      ctx.fillText(String(cfg.collection || 'THE REELS COLLECTION').toUpperCase(), 0, 8);
      ctx.restore();
      // year at bottom of bar (vertical)
      ctx.save(); ctx.translate(-(cfg.textX || 0), -(cfg.textY || 0));
      ctx.fillStyle = '#1C1A16'; ctx.textAlign = 'center'; ctx.textBaseline = 'alphabetic';
      ctx.translate(48, H - 40); ctx.rotate(Math.PI / 2);
      ctx.font = '400 22px ' + COND; ctx.letterSpacing = (0.2 * 22) + 'px';
      ctx.fillText(String(cfg.year || '2026'), 0, 8);
      ctx.restore();
    },
  };

  window.renderCoverCanvas = async function (cfg, tplId) {
    if (document.fonts && document.fonts.ready) { try { await document.fonts.ready; } catch (e) {} }
    const cv = document.createElement('canvas');
    cv.width = W; cv.height = H;
    const ctx = cv.getContext('2d');
    ctx.fillStyle = '#0A0A0B'; ctx.fillRect(0, 0, W, H);
    let img = null;
    if (cfg.source === 'photo') img = await loadImg(cfg.photo || (window.PHOTOS && window.PHOTOS[5] && window.PHOTOS[5].src));
    ctx.save(); ctx.translate(cfg.textX || 0, cfg.textY || 0);
    (RENDER[tplId] || RENDER.centerpiece)(ctx, cfg, img);
    ctx.restore();
    return cv;
  };
})();
