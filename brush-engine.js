/**
 * Sketch Pad Brush Engine.
 *
 * Pure logic + rendering, no DOM assumptions beyond a CanvasRenderingContext2D.
 * Owns: the brush registry, pressure curves, the shared dab-stamping
 * renderer every brush is built from, and persistence for per-brush
 * settings / recents / favourites.
 *
 * DESIGN — one rendering primitive, retained/replayable strokes:
 * every one of the 13 drawing brushes (Inking, Pencil, Marker, Paint/
 * Texture) is `renderMode:'vector'` — a stroke is retained as
 * {id, brushId, color, points:[{x,y,pressure}]} in the app's own
 * `strokes` array, and rendered by stamping dabs along those points
 * via BE.renderStroke(). Re-rendering a stroke with a NEW brushId
 * reproduces the exact same geometry in the new brush's appearance —
 * the brush is purely a set of parameters BE.renderStroke() uses to
 * decide how to stamp along the existing points, never a transform of
 * the points themselves. That's what makes every drawing brush here
 * re-brushable after the fact (Sketch Pad's "interchangeable outline
 * brushes"), texture brushes (Chalk, Crayon, Dry Brush, Gouache)
 * included — their texture comes from this same dab primitive's
 * hardness/jitter/streaky parameters, not from a separate raster path.
 *
 * The one deliberate exception is the Eraser (see ERASER below): it is
 * `renderMode:'raster'` because erasing is inherently destructive —
 * it removes whole strokes it crosses rather than being itself a
 * retained, re-brushable mark. That is the "raster tool, cleanly
 * separated" the brush spec allows for, kept to the one tool that
 * actually needs it rather than applied to any drawing brush.
 *
 * Every brush, drawing or eraser, calls the SAME BE.stampDab()
 * primitive, so adding a new brush is a new entry in BRUSHES with new
 * parameters, never a new code path — that's what keeps this
 * extensible rather than hard-coded around the 13 initial brushes.
 */
(function (global) {
  'use strict';

  // ---- Brush registry -------------------------------------------------
  //
  // family: purely a UI grouping label.
  // renderMode: 'vector' (retained, replayable, re-brushable) | 'raster'
  //   (immediate, flattened, never re-brushable — see file header).
  // pressureAffects: which channels respond to pencil pressure BY
  //   DEFAULT for this brush; the user's own settings (widthStrength/
  //   opacityStrength, persisted per-brush) are what actually drive the
  //   math — a strength of 0 is equivalent to "disabled" for that
  //   channel without needing a separate on/off flag.
  // jitter: 0-1, per-dab random offset/size wobble (Rough Ink, Chalk,
  //   Dry Brush, Crayon) — seeded from the stroke id + dab index so the
  //   SAME stroke always re-renders identically (required for vector
  //   brushes: re-rendering after an undo/reload must reproduce the
  //   same pixels).
  // streaky: 0-1, probability a given dab is skipped/thinned — gives
  //   Dry Brush / Chalk / Crayon their broken-coverage look.
  // taper: 'none' | 'both' — tapers the first/last few dabs of a stroke
  //   down to a point, independent of pressure (Tapered Ink).
  const BRUSHES = [
    // -- Inking (vector) --
    { id: 'smoothPen', name: 'Smooth Pen', family: 'inking', renderMode: 'vector',
      defaults: { size: 3, opacity: 100, smoothing: 35, pressureWidth: 0, pressureOpacity: 0, spacing: 6 },
      // Monoline pen: one constant width and opacity whatever the Pencil pressure (forced, so settings
      // saved before this change cannot bring pressure variation back).
      lock: { pressureWidth: 0, pressureOpacity: 0 },
      hardness: 1, jitter: 0, streaky: 0, taper: 'none', path: true },
    { id: 'technicalPen', name: 'Technical Pen', family: 'inking', renderMode: 'vector',
      defaults: { size: 4, opacity: 100, smoothing: 45, pressureWidth: 5, pressureOpacity: 0, spacing: 5 },
      hardness: 1, jitter: 0, streaky: 0, taper: 'none' },
    { id: 'taperedInk', name: 'Tapered Ink', family: 'inking', renderMode: 'vector',
      defaults: { size: 7, opacity: 100, smoothing: 30, pressureWidth: 70, pressureOpacity: 0, spacing: 6 },
      hardness: 1, jitter: 0, streaky: 0, taper: 'both' },
    { id: 'roughInk', name: 'Rough Ink', family: 'inking', renderMode: 'vector',
      defaults: { size: 8, opacity: 100, smoothing: 20, pressureWidth: 60, pressureOpacity: 15, spacing: 7 },
      hardness: 0.85, jitter: 0.35, streaky: 0.08, taper: 'none' },

    // -- Pencil (vector, textured via per-dab opacity noise) --
    { id: 'sketchPencil', name: 'Sketch Pencil', family: 'pencil', renderMode: 'vector',
      defaults: { size: 3, opacity: 75, smoothing: 15, pressureWidth: 30, pressureOpacity: 45, spacing: 8 },
      hardness: 0.7, jitter: 0.15, streaky: 0.12, taper: 'none' },
    { id: 'softPencil', name: 'Soft Pencil', family: 'pencil', renderMode: 'vector',
      defaults: { size: 9, opacity: 55, smoothing: 25, pressureWidth: 25, pressureOpacity: 55, spacing: 10 },
      hardness: 0.45, jitter: 0.2, streaky: 0.18, taper: 'none' },
    { id: 'texturedPencil', name: 'Textured Pencil', family: 'pencil', renderMode: 'vector',
      defaults: { size: 10, opacity: 65, smoothing: 10, pressureWidth: 20, pressureOpacity: 40, spacing: 5 },
      hardness: 0.4, jitter: 0.3, streaky: 0.3, taper: 'none' },

    // -- Marker (vector, flat coverage) --
    { id: 'solidMarker', name: 'Solid Marker', family: 'marker', renderMode: 'vector',
      defaults: { size: 22, opacity: 90, smoothing: 25, pressureWidth: 10, pressureOpacity: 0, spacing: 9 },
      hardness: 1, jitter: 0, streaky: 0, taper: 'none' },
    { id: 'softMarker', name: 'Soft Marker', family: 'marker', renderMode: 'vector',
      defaults: { size: 30, opacity: 55, smoothing: 25, pressureWidth: 15, pressureOpacity: 20, spacing: 12 },
      hardness: 0.55, jitter: 0.05, streaky: 0, taper: 'none' },

    // -- Paint / Texture (raster-only, see file header) --
    { id: 'gouache', name: 'Gouache', family: 'paint', renderMode: 'vector',
      defaults: { size: 34, opacity: 95, smoothing: 15, pressureWidth: 35, pressureOpacity: 15, spacing: 14 },
      hardness: 0.8, jitter: 0.12, streaky: 0.06, taper: 'none' },
    { id: 'dryBrush', name: 'Dry Brush', family: 'paint', renderMode: 'vector',
      defaults: { size: 26, opacity: 85, smoothing: 10, pressureWidth: 40, pressureOpacity: 35, spacing: 8 },
      hardness: 0.5, jitter: 0.3, streaky: 0.45, taper: 'none' },
    { id: 'chalk', name: 'Chalk', family: 'paint', renderMode: 'vector',
      defaults: { size: 20, opacity: 70, smoothing: 5, pressureWidth: 20, pressureOpacity: 40, spacing: 6 },
      hardness: 0.35, jitter: 0.4, streaky: 0.4, taper: 'none' },
    { id: 'crayon', name: 'Crayon', family: 'paint', renderMode: 'vector',
      defaults: { size: 16, opacity: 80, smoothing: 5, pressureWidth: 25, pressureOpacity: 25, spacing: 5 },
      hardness: 0.6, jitter: 0.25, streaky: 0.3, taper: 'none' },
  ];

  const FAMILY_ORDER = ['inking', 'pencil', 'marker', 'paint', 'custom', 'stamp'];
  const FAMILY_LABEL = { inking: 'Inking', pencil: 'Pencil', marker: 'Marker', paint: 'Paint / Texture', custom: 'Custom Brushes', stamp: 'Motif Brushes' };

  const ERASER = { id: 'eraser', name: 'Eraser', family: 'eraser', renderMode: 'raster',
    defaults: { size: 26, opacity: 100, smoothing: 15, pressureWidth: 30, pressureOpacity: 0, spacing: 6 },
    hardness: 0.9, jitter: 0, streaky: 0, taper: 'none' };

  const byId = new Map(BRUSHES.map((b) => [b.id, b]));
  byId.set(ERASER.id, ERASER);

  function getBrush(id) { return byId.get(id) || BRUSHES[0]; }
  // ---- Motif (stamp) brushes ----------------------------------------------
  // A captured motif becomes a brush: the stroke is still an ordinary retained path, but it is
  // drawn by stamping the motif's picture along it. Registered at runtime by the app.
  function registerStampBrush(id, name, img, noRegister) {
    const max = 512, w = img.naturalWidth || img.width, h = img.naturalHeight || img.height;
    if (!w || !h) return null;
    const k = Math.min(1, max / Math.max(w, h));
    const c = document.createElement('canvas');
    c.width = Math.max(1, Math.round(w * k)); c.height = Math.max(1, Math.round(h * k));
    const g = c.getContext('2d'); g.imageSmoothingQuality = 'high'; g.drawImage(img, 0, 0, c.width, c.height);
    const old = byId.get(id);
    const brush = {
      id, name, family: 'stamp', renderMode: 'vector', stamp: true, stampImg: img, stampCanvas: c, tinted: {},
      defaults: { size: 90, opacity: 100, smoothing: 35, pressureWidth: 0, pressureOpacity: 0, spacing: 100, follow: 0, tint: 0 },
      hardness: 1, jitter: 0, streaky: 0, taper: 'none',
    };
    if (noRegister) return brush;
    if (old) { BRUSHES[BRUSHES.indexOf(old)] = brush; } else { BRUSHES.push(brush); }
    byId.set(id, brush);
    return brush;
  }
  // ---- User-made brushes ---------------------------------------------------
  // def: { id, name, softness(0-100), grain(0-80), wobble(0-100), taper, mono, tipImg?, defaults:{size,opacity,smoothing,pressureWidth,pressureOpacity,spacing,...} }
  function applyFx(b, def) {
    const fx = def.fx || {};
    let ts = fx.taperStart, te = fx.taperEnd;
    if (ts == null && te == null && def.taper) { ts = te = 12; }
    ts = Math.max(0, Math.min(60, ts || 0)); te = Math.max(0, Math.min(60, te || 0));
    b.taperS = ts / 100; b.taperE = te / 100; b.taper = (ts > 0 || te > 0) ? 'both' : 'none';
    const c = fx.color || {};
    b.cdyn = { h: c.h || 0, s: c.s || 0, b: c.b || 0 };
    const grain = fx.grain && (def.grainImg) ? Object.assign({}, fx.grain, { img: def.grainImg }) : null;
    const dual = fx.dual && fx.dual.on ? Object.assign({}, fx.dual, { img: def.dualImg || null }) : null;
    b.fx = { grain, blend: fx.blend || 'source-over', dual };
    return b;
  }
  function makeCustomBrush(def) {
    const d = Object.assign({ size: 20, opacity: 100, smoothing: 30, pressureWidth: 0, pressureOpacity: 0, spacing: 8 }, def.defaults || {});
    if (def.tipImg) {
      const b = registerStampBrush(def.id, def.name, def.tipImg, true);
      if (!b) return null;
      b.family = 'custom'; b.custom = true; b.def = def;
      b.defaults = Object.assign({}, b.defaults, d, { follow: d.follow || 0, tint: d.tint || 0 });
      return applyFx(b, def);
    }
    const brush = {
      id: def.id, name: def.name, family: 'custom', renderMode: 'vector', custom: true, def,
      defaults: d,
      hardness: Math.max(0.05, Math.min(1, (def.softness == null ? 100 : def.softness) / 100)),
      jitter: Math.max(0, Math.min(1, (def.wobble || 0) / 100)),
      streaky: Math.max(0, Math.min(0.9, (def.grain || 0) / 100)),
      taper: 'none',
    };
    applyFx(brush, def);
    if (def.mono) {
      brush.hardness = 1; brush.jitter = 0; brush.streaky = 0; brush.lock = { pressureWidth: 0, pressureOpacity: 0 };
      // a true monoline path cannot narrow, so a tapered monoline is drawn as hard dabs instead
      if (brush.taper === 'none') { brush.path = true; brush.cdyn = { h: 0, s: 0, b: 0 }; }
    }
    return brush;
  }
  function registerCustomBrush(def) {
    const b = makeCustomBrush(def); if (!b) return null;
    const old = byId.get(def.id);
    if (old) BRUSHES[BRUSHES.indexOf(old)] = b; else BRUSHES.push(b);
    byId.set(def.id, b);
    return b;
  }
  function unregisterStampBrush(id) {
    const old = byId.get(id); if (!old) return;
    BRUSHES.splice(BRUSHES.indexOf(old), 1); byId.delete(id);
  }

  function isVector(brushOrId) {
    const b = typeof brushOrId === 'string' ? getBrush(brushOrId) : brushOrId;
    return b.renderMode === 'vector';
  }

  // ---- Settings persistence -------------------------------------------
  //
  // One JSON blob per key rather than one localStorage key per brush —
  // keeps this to 3 keys total, well inside any reasonable storage quota,
  // and trivial to include in a future full project export.
  const LS_SETTINGS = 'pkmBrushSettingsV1';
  const LS_RECENTS = 'pkmBrushRecentsV1';
  const LS_FAVORITES = 'pkmBrushFavoritesV1';
  const RECENTS_MAX = 8;

  function loadJSON(key, fallback) {
    try { const raw = localStorage.getItem(key); return raw ? JSON.parse(raw) : fallback; }
    catch (e) { return fallback; }
  }
  function saveJSON(key, value) {
    try { localStorage.setItem(key, JSON.stringify(value)); } catch (e) {}
  }

  let settingsStore = loadJSON(LS_SETTINGS, {});
  let recents = loadJSON(LS_RECENTS, []);
  let favorites = loadJSON(LS_FAVORITES, []);

  function getSettings(brushId) {
    const brush = getBrush(brushId);
    return Object.assign({}, brush.defaults, settingsStore[brushId] || {}, brush.lock || {});
  }
  function setSettings(brushId, patch) {
    settingsStore[brushId] = Object.assign({}, getSettings(brushId), patch);
    saveJSON(LS_SETTINGS, settingsStore);
  }
  function touchRecent(brushId) {
    recents = [brushId].concat(recents.filter((id) => id !== brushId)).slice(0, RECENTS_MAX);
    saveJSON(LS_RECENTS, recents);
  }
  function getRecents() { return recents.slice(); }
  function isFavorite(brushId) { return favorites.indexOf(brushId) !== -1; }
  function toggleFavorite(brushId) {
    favorites = isFavorite(brushId) ? favorites.filter((id) => id !== brushId) : favorites.concat([brushId]);
    saveJSON(LS_FAVORITES, favorites);
    return isFavorite(brushId);
  }
  function getFavorites() { return favorites.slice(); }

  // ---- Pressure curves --------------------------------------------------
  //
  // strength 0..100. 0 = channel ignores pressure entirely (constant).
  // 100 = channel fully follows pressure. Anything between blends the
  // two linearly — this single formula is what "pressure -> width",
  // "-> opacity", "-> both" and "disabled" all reduce to, per brush,
  // per user setting, with no separate code path per mode.
  function pressureFactor(pressure, strength) {
    const p = Math.max(0, Math.min(1, pressure == null ? 0.5 : pressure));
    const s = Math.max(0, Math.min(100, strength)) / 100;
    return (1 - s) + s * p;
  }

  // Deterministic per-dab pseudo-random, seeded from the stroke id + dab
  // index — same stroke always re-renders identically (required so
  // undo/redo and brush re-assignment reproduce exact pixels), but
  // varies dab-to-dab and stroke-to-stroke.
  function seededRandom(seedStr) {
    let h = 0;
    for (let i = 0; i < seedStr.length; i++) { h = (h * 31 + seedStr.charCodeAt(i)) | 0; }
    return function () {
      h = (h * 1664525 + 1013904223) | 0;
      return ((h >>> 0) / 4294967296);
    };
  }

  // ---- Core stamping primitive -----------------------------------------
  //
  // Every brush, vector or raster, resolves to a sequence of calls to
  // this one function. `hardness` controls edge softness (1 = hard disc,
  // <1 = radial-gradient falloff, giving pencil/chalk/dry-brush their
  // soft edges without a second rendering path).
  function stampDab(ctx, x, y, radius, opacity, color, hardness) {
    if (radius <= 0 || opacity <= 0) return;
    ctx.save();
    ctx.globalAlpha = Math.max(0, Math.min(1, opacity));
    if (hardness >= 0.98) {
      ctx.fillStyle = color;
      ctx.beginPath();
      ctx.arc(x, y, radius, 0, Math.PI * 2);
      ctx.fill();
    } else {
      const grad = ctx.createRadialGradient(x, y, Math.max(0, radius * hardness), x, y, radius);
      grad.addColorStop(0, color);
      grad.addColorStop(1, colorWithAlpha(color, 0));
      ctx.fillStyle = grad;
      ctx.beginPath();
      ctx.arc(x, y, radius, 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.restore();
  }

  // Cheap hex/rgb -> "same colour, alpha 0" for the gradient stop above.
  // Only needs to handle the #rrggbb / #rgb the app's own <input
  // type=color> produces plus the eraser's synthetic rgba(...) — good
  // enough without pulling in a colour-parsing library for this.
  function colorWithAlpha(color, alpha) {
    if (color.charAt(0) === '#') {
      let hex = color.slice(1);
      if (hex.length === 3) hex = hex.split('').map((c) => c + c).join('');
      const r = parseInt(hex.slice(0, 2), 16), g = parseInt(hex.slice(2, 4), 16), b = parseInt(hex.slice(4, 6), 16);
      return 'rgba(' + r + ',' + g + ',' + b + ',' + alpha + ')';
    }
    if (color.indexOf('rgba(') === 0) return color.replace(/[\d.]+\)$/, alpha + ')');
    if (color.indexOf('rgb(') === 0) return color.replace('rgb(', 'rgba(').replace(')', ',' + alpha + ')');
    return color;
  }

  // Resample a raw point list at even arc-length spacing (in canvas
  // px) so dab density stays consistent regardless of how fast the
  // pencil moved — fast strokes would otherwise get sparse/gappy dabs
  // since pointermove fires less often per pixel of travel at speed.
  // Pressure is linearly interpolated between the two source points a
  // resampled point falls between.
  function resample(points, spacing) {
    if (points.length < 2) return points.slice();
    const out = [points[0]];
    let carry = 0;
    for (let i = 1; i < points.length; i++) {
      const a = points[i - 1], b = points[i];
      const segLen = Math.hypot(b.x - a.x, b.y - a.y);
      if (segLen <= 0) continue;
      let dist = carry;
      while (dist < segLen) {
        const t = dist / segLen;
        out.push({ x: a.x + (b.x - a.x) * t, y: a.y + (b.y - a.y) * t, pressure: a.pressure + (b.pressure - a.pressure) * t });
        dist += spacing;
      }
      carry = dist - segLen;
    }
    out.push(points[points.length - 1]);
    return out;
  }

  // Monoline pens: one true anti-aliased curved path (round caps/joins) instead of
  // stamped dabs, so edges stay perfectly smooth at any zoom.
  function renderPathStroke(ctx, stroke, settings, alphaMul) {
    const src = stroke.points, color = stroke.color || '#000000';
    const pts = [src[0]];
    for (let i = 1; i < src.length; i++) {
      const l = pts[pts.length - 1];
      if (Math.hypot(src[i].x - l.x, src[i].y - l.y) >= 0.3) pts.push(src[i]);
    }
    ctx.save();
    ctx.globalAlpha = Math.max(0, Math.min(1, (settings.opacity / 100) * alphaMul));
    ctx.strokeStyle = color; ctx.fillStyle = color;
    ctx.lineWidth = settings.size; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
    if (pts.length < 2) {
      ctx.beginPath(); ctx.arc(pts[0].x, pts[0].y, settings.size / 2, 0, Math.PI * 2); ctx.fill();
    } else {
      ctx.beginPath();
      ctx.moveTo(pts[0].x, pts[0].y);
      for (let i = 1; i < pts.length - 1; i++) {
        const mx = (pts[i].x + pts[i + 1].x) / 2, my = (pts[i].y + pts[i + 1].y) / 2;
        ctx.quadraticCurveTo(pts[i].x, pts[i].y, mx, my);
      }
      const e = pts[pts.length - 1];
      ctx.lineTo(e.x, e.y);
      ctx.stroke();
    }
    ctx.restore();
  }

  // Motif brush: stamp the motif picture along the path. size = the motif's longest side in canvas px.
  function renderStampStroke(ctx, stroke, brush, settings, alphaMul) {
    const src = brush.stampCanvas; if (!src) return;
    let img = src;
    if (settings.tint) {
      const key = stroke.color || '#000000';
      img = brush.tinted[key];
      if (!img) {
        img = document.createElement('canvas'); img.width = src.width; img.height = src.height;
        const g = img.getContext('2d'); g.drawImage(src, 0, 0);
        g.globalCompositeOperation = 'source-in'; g.fillStyle = key; g.fillRect(0, 0, img.width, img.height);
        brush.tinted[key] = img;
      }
    }
    const pts0 = stroke.points; if (!pts0 || !pts0.length) return;
    const spacingPx = Math.max(2, (settings.spacing / 100) * settings.size);
    let pts = pts0.length < 2 ? pts0.slice() : resample(pts0, spacingPx);
    if (pts.length > 2) {
      const a = pts[pts.length - 1], b = pts[pts.length - 2];
      if (Math.hypot(a.x - b.x, a.y - b.y) < spacingPx * 0.5) pts.pop();
    }
    const longest = Math.max(src.width, src.height);
    const sBase = (settings.tint && hasCdyn(brush)) ? hexToHsl(stroke.color || '#000000') : null;
    let variants = null;
    if (sBase) { const r0 = seededRandom((stroke.id || 'live') + 'v'); variants = []; for (let v = 0; v < 8; v++) variants.push(dynColor(sBase, brush.cdyn, r0)); }
    const rv = seededRandom((stroke.id || 'live') + 'p');
    ctx.save();
    for (let i = 0; i < pts.length; i++) {
      const pt = pts[i];
      if (variants) {
        const key = variants[Math.floor(rv() * 8)];
        let tv = brush.tinted[key];
        if (!tv) {
          tv = document.createElement('canvas'); tv.width = src.width; tv.height = src.height;
          const g = tv.getContext('2d'); g.drawImage(src, 0, 0);
          g.globalCompositeOperation = 'source-in'; g.fillStyle = key; g.fillRect(0, 0, tv.width, tv.height);
          brush.tinted[key] = tv;
        }
        img = tv;
      }
      const sz = settings.size * pressureFactor(pt.pressure, settings.pressureWidth) * taperAt(brush, i, pts.length);
      const op = (settings.opacity / 100) * pressureFactor(pt.pressure, settings.pressureOpacity) * alphaMul;
      if (sz <= 0.5 || op <= 0) continue;
      const k = sz / longest, w = src.width * k, h = src.height * k;
      ctx.globalAlpha = Math.max(0, Math.min(1, op));
      ctx.save();
      ctx.translate(pt.x, pt.y);
      if (settings.follow && pts.length > 1) {
        const p0 = pts[Math.max(0, i - 1)], p1 = pts[Math.min(pts.length - 1, i + 1)];
        ctx.rotate(Math.atan2(p1.y - p0.y, p1.x - p0.x));
      }
      ctx.drawImage(img, -w / 2, -h / 2, w, h);
      ctx.restore();
    }
    ctx.restore();
  }

  // Renders one stroke (vector or, called from the app's raster path,
  // one in-progress raster segment) onto `ctx` using `brush`'s current
  // settings. This is the single function both the vector replay path
  // and the live raster-paint path call — see file header.
  function renderStroke(ctx, stroke, brush, settings, alphaMul) {
    if (!stroke.points || stroke.points.length === 0) return;
    if (alphaMul === undefined) alphaMul = 1;
    if (alphaMul <= 0) return; // fully hidden — skip dabs entirely rather than stamp at opacity 0
    if (brush.fx && fxActive(brush)) { renderWithFx(ctx, stroke, brush, settings, alphaMul); return; }
    renderBase(ctx, stroke, brush, settings, alphaMul);
  }
  function renderBase(ctx, stroke, brush, settings, alphaMul) {
    if (brush.path) { renderPathStroke(ctx, stroke, settings, alphaMul); return; }
    if (brush.stamp) { renderStampStroke(ctx, stroke, brush, settings, alphaMul); return; }
    let spacingPx = Math.max(1, (settings.spacing / 100) * Math.max(4, settings.size));
    // Thin brushes: a 1-unit minimum gap is wider than the dab itself at size ~1-3 (and wider still
    // when light pressure shrinks it), so the stroke breaks into visible dots, worst when zoomed in.
    // Cap the gap to a fraction of the dab's narrowest width; sizes of ~3.5+ are unchanged.
    const narrow = Math.max(0.35, 1 - settings.pressureWidth / 100);
    spacingPx = Math.max(0.2, Math.min(spacingPx, settings.size * narrow * 0.6));
    const pts = resample(stroke.points, spacingPx);
    const rand = seededRandom(stroke.id || 'live');
    const baseHsl = hasCdyn(brush) ? hexToHsl(stroke.color || '#000000') : null;
    const cdyn = !!baseHsl, rand2 = cdyn ? seededRandom((stroke.id || 'live') + 'c') : null;
    const n = pts.length;
    const hold = Math.max(1, Math.round(settings.size * 0.2 / spacingPx));
    let curCol = stroke.color || '#000000';
    pts.forEach((pt, i) => {
      const widthMul = pressureFactor(pt.pressure, settings.pressureWidth);
      const opMul = pressureFactor(pt.pressure, settings.pressureOpacity);
      const taperMul = taperAt(brush, i, n);
      let radius = (settings.size / 2) * widthMul * taperMul;
      let opacity = (settings.opacity / 100) * opMul * alphaMul;
      if (brush.jitter > 0) {
        radius *= (1 - brush.jitter * 0.3) + rand() * brush.jitter * 0.6;
        opacity *= (1 - brush.jitter * 0.2) + rand() * brush.jitter * 0.4;
      }
      if (brush.streaky > 0 && rand() < brush.streaky) return; // skipped dab -> broken coverage
      let x = pt.x, y = pt.y;
      if (brush.jitter > 0) {
        const jr = radius * brush.jitter * 0.5;
        x += (rand() - 0.5) * jr;
        y += (rand() - 0.5) * jr;
      }
      stampDab(ctx, x, y, radius, opacity, (cdyn && i % hold === 0 ? (curCol = dynColor(baseHsl, brush.cdyn, rand2)) : curCol), brush.hardness);
    });
  }

  // ---- Taper (separate start / end lengths, as a fraction of the stroke) ----
  function taperAt(brush, i, n) {
    let ts, te;
    if (brush.taperS != null || brush.taperE != null) { ts = brush.taperS || 0; te = brush.taperE || 0; }
    else if (brush.taper === 'both') { ts = te = 0.12; }
    else return 1;
    let m = 1;
    if (ts > 0) { const len = Math.max(2, Math.round(n * ts)); if (i < len) m = Math.min(m, Math.max(0.12, i / len)); }
    if (te > 0) { const len = Math.max(2, Math.round(n * te)), e = n - 1 - i; if (e < len) m = Math.min(m, Math.max(0.12, e / len)); }
    return m;
  }

  // ---- Colour dynamics (per-dab hue / saturation / brightness variation) ----
  function hexToHsl(hex) {
    if (!hex || hex.charAt(0) !== '#') return null;
    let h = hex.slice(1); if (h.length === 3) h = h.split('').map((c) => c + c).join('');
    const r = parseInt(h.slice(0, 2), 16) / 255, g = parseInt(h.slice(2, 4), 16) / 255, b = parseInt(h.slice(4, 6), 16) / 255;
    if (isNaN(r + g + b)) return null;
    const mx = Math.max(r, g, b), mn = Math.min(r, g, b), l = (mx + mn) / 2, d = mx - mn;
    let hh = 0, ss = 0;
    if (d) {
      ss = d / (1 - Math.abs(2 * l - 1));
      if (mx === r) hh = ((g - b) / d) % 6; else if (mx === g) hh = (b - r) / d + 2; else hh = (r - g) / d + 4;
      hh *= 60; if (hh < 0) hh += 360;
    }
    return { h: hh, s: ss, l };
  }
  function hslToHex(h, s, l) {
    h = ((h % 360) + 360) % 360; s = Math.max(0, Math.min(1, s)); l = Math.max(0, Math.min(1, l));
    const c = (1 - Math.abs(2 * l - 1)) * s, x = c * (1 - Math.abs((h / 60) % 2 - 1)), m = l - c / 2;
    let r = 0, g = 0, b = 0;
    if (h < 60) { r = c; g = x; } else if (h < 120) { r = x; g = c; } else if (h < 180) { g = c; b = x; }
    else if (h < 240) { g = x; b = c; } else if (h < 300) { r = x; b = c; } else { r = c; b = x; }
    const to = (v) => ('0' + Math.round((v + m) * 255).toString(16)).slice(-2);
    return '#' + to(r) + to(g) + to(b);
  }
  // cd = {h,s,b} each 0..100
  function dynColor(base, cd, rand) {
    const j = () => rand() * 2 - 1;
    return hslToHex(base.h + j() * (cd.h / 100) * 60, base.s + j() * (cd.s / 100) * 0.5, base.l + j() * (cd.b / 100) * 0.35);
  }
  function hasCdyn(brush) { const c = brush.cdyn; return !!(c && (c.h > 0 || c.s > 0 || c.b > 0)); }

  // ---- Grain, blend and dual-brush layers -----------------------------------
  // A brush using any of these is drawn into a small scratch canvas covering just the stroke, then
  // shaped (grain / second tip multiply the coverage) and composited with its blend mode.
  function makeGrainMask(brush) {
    const g = brush.fx && brush.fx.grain; if (!g || !g.img) return null;
    if (brush._grainMask && brush._grainMask.src === g.img) return brush._grainMask.canvas;
    const img = g.img, w = img.naturalWidth || img.width, h = img.naturalHeight || img.height;
    if (!w || !h) return null;
    const k = Math.min(1, 512 / Math.max(w, h)), cw = Math.max(1, Math.round(w * k)), ch = Math.max(1, Math.round(h * k));
    const c = document.createElement('canvas'); c.width = cw; c.height = ch;
    const x = c.getContext('2d'); x.drawImage(img, 0, 0, cw, ch);
    let d; try { d = x.getImageData(0, 0, cw, ch); } catch (e) { return null; }
    const depth = Math.max(0, Math.min(1, (g.depth == null ? 70 : g.depth) / 100));
    for (let i = 0; i < d.data.length; i += 4) {
      let lum = (0.299 * d.data[i] + 0.587 * d.data[i + 1] + 0.114 * d.data[i + 2]) / 255;
      const a = d.data[i + 3] / 255; lum = lum * a + (1 - a); // transparent = full paint
      if (g.invert) lum = 1 - lum;
      if (g.contrast) lum = Math.max(0, Math.min(1, (lum - 0.5) * (1 + g.contrast / 50) + 0.5));
      d.data[i] = d.data[i + 1] = d.data[i + 2] = 0;
      d.data[i + 3] = Math.round(((1 - depth) + depth * lum) * 255);
    }
    x.putImageData(d, 0, 0);
    brush._grainMask = { src: g.img, canvas: c };
    return c;
  }
  function fxActive(brush) {
    const f = brush.fx; if (!f) return false;
    return !!((f.grain && f.grain.img) || (f.blend && f.blend !== 'source-over') || (f.dual && f.dual.on));
  }
  function renderWithFx(ctx, stroke, brush, settings, alphaMul) {
    const f = brush.fx, pts = stroke.points;
    let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
    for (let i = 0; i < pts.length; i++) { const p = pts[i]; if (p.x < minX) minX = p.x; if (p.x > maxX) maxX = p.x; if (p.y < minY) minY = p.y; if (p.y > maxY) maxY = p.y; }
    const pad = settings.size * ((f.dual && f.dual.on ? 1 + (f.dual.scatter || 0) / 100 : 1)) + 4;
    const bx = Math.floor(minX - pad), by = Math.floor(minY - pad), bw = Math.ceil(maxX - minX + pad * 2), bh = Math.ceil(maxY - minY + pad * 2);
    const m = ctx.getTransform ? ctx.getTransform() : { a: 1, b: 0 };
    let sc = Math.hypot(m.a, m.b) || 1;
    const MAXPX = 12e6;
    if (bw * bh * sc * sc > MAXPX) sc = Math.sqrt(MAXPX / (bw * bh));
    const W = Math.max(1, Math.round(bw * sc)), H = Math.max(1, Math.round(bh * sc));
    const tmp = document.createElement('canvas'); tmp.width = W; tmp.height = H;
    const t = tmp.getContext('2d');
    t.setTransform(W / bw, 0, 0, H / bh, -bx * (W / bw), -by * (H / bh));
    renderBase(t, stroke, brush, settings, alphaMul);
    if (f.grain && f.grain.img) {
      const mask = makeGrainMask(brush);
      if (mask) {
        const pat = t.createPattern(mask, 'repeat');
        const gs = Math.max(0.05, (f.grain.scale == null ? 100 : f.grain.scale) / 100);
        const ox = f.grain.moving ? pts[0].x : 0, oy = f.grain.moving ? pts[0].y : 0;
        if (pat.setTransform && typeof DOMMatrix !== 'undefined') pat.setTransform(new DOMMatrix().translate(ox, oy).scale(gs));
        t.save(); t.globalCompositeOperation = 'destination-in'; t.fillStyle = pat; t.fillRect(bx, by, bw, bh); t.restore();
      }
    }
    if (f.dual && f.dual.on) {
      const mk = document.createElement('canvas'); mk.width = W; mk.height = H;
      const q = mk.getContext('2d'); q.setTransform(W / bw, 0, 0, H / bh, -bx * (W / bw), -by * (H / bh));
      const d = f.dual, rr = seededRandom((stroke.id || 'live') + 'd');
      const dsize = Math.max(1, settings.size * (d.size || 40) / 100);
      const step = Math.max(0.6, dsize * Math.max(0.05, (d.spacing || 50) / 100));
      const line = resample(pts, step);
      const sp = settings.size * (d.scatter || 0) / 100;
      q.fillStyle = '#000';
      for (let i = 0; i < line.length; i++) {
        const cnt = Math.max(1, Math.round(d.count || 1));
        for (let c = 0; c < cnt; c++) {
          const x = line[i].x + (rr() - 0.5) * 2 * sp, y = line[i].y + (rr() - 0.5) * 2 * sp;
          if (d.img) {
            const iw = d.img.naturalWidth || d.img.width, ih = d.img.naturalHeight || d.img.height, kk = dsize / Math.max(iw, ih);
            q.save(); q.translate(x, y); q.rotate(rr() * Math.PI * 2); q.drawImage(d.img, -iw * kk / 2, -ih * kk / 2, iw * kk, ih * kk); q.restore();
          } else {
            const soft = Math.max(0.05, Math.min(1, (d.soft == null ? 100 : d.soft) / 100));
            if (soft >= 0.98) { q.beginPath(); q.arc(x, y, dsize / 2, 0, Math.PI * 2); q.fill(); }
            else { const gr = q.createRadialGradient(x, y, dsize / 2 * soft, x, y, dsize / 2); gr.addColorStop(0, '#000'); gr.addColorStop(1, 'rgba(0,0,0,0)'); q.fillStyle = gr; q.beginPath(); q.arc(x, y, dsize / 2, 0, Math.PI * 2); q.fill(); q.fillStyle = '#000'; }
          }
        }
      }
      t.save(); t.setTransform(1, 0, 0, 1, 0, 0); t.globalCompositeOperation = 'destination-in'; t.drawImage(mk, 0, 0); t.restore();
    }
    ctx.save();
    if (f.blend && f.blend !== 'source-over') ctx.globalCompositeOperation = f.blend;
    ctx.drawImage(tmp, bx, by, bw, bh);
    ctx.restore();
  }

  // Smooths a raw captured point list before it's committed as a
  // stroke — the app's pre-existing brushSmooth technique (exponential
  // lerp toward each new point) generalised to run over a whole
  // finished stroke rather than only live, point-by-point. Reused as-is
  // because it already works well and stays cheap; see index.html's
  // strokeTo() for the live version applied during the stroke itself.
  function smoothPoints(points, amount) {
    const a = Math.max(0, Math.min(0.95, amount / 100));
    if (a <= 0 || points.length < 3) return points.slice();
    const out = [points[0]];
    for (let i = 1; i < points.length; i++) {
      const prev = out[out.length - 1];
      out.push({
        x: prev.x + (points[i].x - prev.x) * (1 - a),
        y: prev.y + (points[i].y - prev.y) * (1 - a),
        pressure: points[i].pressure,
      });
    }
    out.push(points[points.length - 1]);
    return out;
  }

  global.BrushEngine = {
    BRUSHES, FAMILY_ORDER, FAMILY_LABEL, ERASER,
    getBrush, isVector, taperAt, registerStampBrush, unregisterStampBrush, makeCustomBrush, registerCustomBrush,
    getSettings, setSettings,
    touchRecent, getRecents,
    isFavorite, toggleFavorite, getFavorites,
    pressureFactor, stampDab, colorWithAlpha, resample, renderStroke, smoothPoints, seededRandom,
  };
})(window);
