# Pattern Sketch for iPad

The same `index.html` powers the browser app, the Seamless Creative suite, and the iPad app.
Native behaviour lives in `native-bridge.js` and only switches on inside the iPad app
(`window.Capacitor.isNativePlatform()`), so the web and suite versions are unchanged.

## What was changed for the app

- **Exports use the iOS share sheet.** Project `.json` and tile `.png` saves go through
  `SketchpadNative.saveBlob()`. In a browser it is a normal download; on iPad it opens the share
  sheet (Save to Files, AirDrop, Photos, Mail).
- **Native touches.** Status bar hidden, splash screen dismissed, text selection and long-press
  callouts disabled while drawing.
- **Offline.** `npm run build:web` fails if `index.html` references anything over the network.
  Today it needs nothing external.

## View and drawing improvements

- **Fabric preview.** Zoom out and the repeat continues across the whole workspace (respects grid, half-drop,
  half-brick and diamond). Your tile has a subtle outline. It is display only: exports are unchanged.
- **Crisp deep zoom.** Zoom goes up to 3200%. The stroke being edited with Edit Path stays sharp while you drag a node. Once zooming settles, the visible part of the vector drawing is redrawn at full
  screen resolution so lines stay sharp (the soft view stays until the sharp one is ready). Placed pictures and motifs are
  bitmaps, so they stay soft.
- **Sharp while drawing.** The line under the Pencil is now drawn at full screen resolution, so it is as sharp while you draw as after you lift (it used to be drawn small and stretched, which looked soft once you zoomed in). Nothing changes when you lift the Pencil.
- **Select Area.** To work on just one drawing (say one goose), tap **Select Area** in the toolbar and drag a box round it. Only what is inside is selected, and the handles appear straight away: drag a corner to resize, drag inside the box to move.
- **Select same.** Select a stroke, open Stroke tools, then tap **Same colour**, **Same stroke** (same brush and thickness) or **Same fill** to select every match across your drawing. A panel lets you set one colour and line size for all of them at once (**Apply to all**), and the handles resize them together.
- **Motif brush export.** Brushes, brush sets and PNG packs are now drawn at the chosen size (2048 px by default) straight from the motif's saved strokes, so the brush picture is crisp instead of an enlarged small PNG.
- **Select All, Group and Ungroup.** Tap **Select All** (toolbar) to select your artwork only: never the background pattern, trace picture or guides. Tap **Group** to make it one piece. A group is not flattened: every line, fill, brush mark and picture stays a real object in its original stacking order, so **Ungroup** gives them all back and you can still edit any single path (or tap **Edit inside**). A box with handles appears: drag inside it to move, drag a corner to resize (proportions locked by default; tap the lock for free resizing, which also shows side handles), drag the round handle to turn (15 degree steps, tap it for 45). **Scale strokes** (on by default) makes line thickness grow and shrink with the artwork; turn it off to keep line thickness. **Size %** and **Turn** boxes take exact values. **Add / remove** lets you tap more objects into the selection. Everything is recomputed from the original strokes, so vectors stay sharp at any size. Undo, Redo, save and reopen keep groups.
- **Captured motifs.** Capture Motif is unchanged and separate from grouping. A captured motif is a picture, so it used to blur when enlarged: it is now redrawn sharp from its saved strokes whenever it is shown larger than its picture. Captured motifs also keep their proportions (tall or wide drawings were squashed before) and have bigger handles. **Release to Vectors** (Selected Motif panel) turns a placed motif back into its real strokes as a group you can resize at any size.
- **Steady zoom.** Pinch is anchored between your fingers; the +/- buttons zoom about the centre of the workspace.
- **View recovery.** Tap the zoom percentage (e.g. `100% ▾`): **100%**, **Fit to View**, **Reset View** (also resets rotation).
  These work even if the canvas is completely off-screen.
- **Stroke panel** only opens when you tap **🖊️ Stroke tools**; open/closed is remembered. Selecting a stroke in Edit mode
  also shows a small bar on the canvas with a one-tap **Edit Path** button.
- **Safe areas.** Toolbar sits below the iPad status bar in Safari and the installed app, portrait and landscape.

## Drawing, brushes and saving (features added for the app)

- **Smooth Pen** is a true monoline vector path (default 3 px) with smooth edges at any zoom.
- **On-canvas handles.** A selected stroke shows three handles: the round one at the top turns it (drag, or tap for a 45 degree step: 45, 90, 135, 180...; dragging turns in controlled 15 degree steps with the angle shown, and the box turns with it), the square one at the corner resizes it (drag, or tap for 25% bigger), and the colour dot at the top-left changes its colour.
- **Rotate & Repeat panel.** Tapping the rotate handle (or the Rotate & Repeat button in the Stroke panel) opens its own panel, so the Stroke panel stays short. It holds 45/90/135/180 quick turns, **Rotate by** an exact amount (type degrees, positive is clockwise) and **Repeat around a point**: choose the total number of copies, the angle between them (auto = 360 / copies) and the centre (start, end or middle of the stroke, middle of the canvas, or a point you tap). One Undo removes all the copies. Good for flowers, rosettes and borders.
- **Repeat last move** (like Affinity's duplicate-and-transform): tap Duplicate, then move, turn or resize the copy, then tap Repeat (set how many times with the x field). Every repeat applies the same step again, so spirals, fans and borders are quick. One Undo removes the whole batch.
- **Blend** (Stroke panel, tap Blend with a shape selected, then tap the second shape): inserts 1 to 40 steps between two vector shapes or two open paths. Controls: steps (slider or number), colour and opacity, shape, position, size, rotation, reverse direction. It previews live, then **Apply** (one Undo) or **Cancel**. The result is a live blend: edit either original and the steps follow. Select an original or a step and tap Blend to change it, or **Expand Blend** to turn the steps into ordinary separate shapes. Not supported yet: compound shapes (holes or several pieces), painted content, pictures and placed motifs, and a closed shape with an open path; the panel explains why and leaves your originals alone. Blend Along Path is planned.
- **Shapes.** Line, Rectangle, Rounded Rectangle, Ellipse, Circle, Triangle, Diamond, Polygon, Star, Heart, **Teardrop** (tip up, round base) and Spiral. Sharp corners stay sharp on the canvas, in Edit Path and in SVG; only Line and Spiral are open. Drag in any direction; Constrain makes squares and circles.
- **Edit Path.** Tap another stroke while editing to switch to it; the stroke keeps the shape it was drawn with.
- **Live brush preview** under the brush controls matches the canvas stroke and updates as you adjust.
- **Motif brushes.** Capture a drawing (or just a box-selected part with **Capture Area**) and it becomes a brush that
  stamps the picture along your line. Export motif brushes to Procreate as `.brushset`, separate `.brush` files, or a PNG pack.
- **Create custom brush** (Brush section): edge softness, texture, variation, uniform monoline, separate start and end
  taper, grain texture (Paper, Grit, Canvas weave, or your own image, with depth, scale, contrast, invert, fixed or moving),
  blend mode, colour variation (hue, saturation, brightness), and a dual brush (second tip with size, spacing, scatter,
  count, softness, optional image). Image tips are supported. Brushes are stored on the device and inside project files.
- **SVG export** (vector only; pictures are left out). Default size 3600 px.
- **Trace reference** can be moved in Edit mode (it always reopens locked) and is never in the way of drawing.
- **Drawing on a hidden or fully transparent layer** shows the layer again automatically.
- **Autosave safety.** The last session is restored automatically; autosave waits until it has been restored; a rolling set of
  earlier versions is kept under **Earlier saves**; **Start Fresh** keeps the old session as a backup.
  Use **Download Project** regularly as an off-device backup.

## Project files

| File | Purpose |
|---|---|
| `native-bridge.js` | Platform layer (web vs iPad) |
| `capacitor.config.json` | App ID, name, iOS options |
| `scripts/build-web.js` | Copies the web files into `www/` and checks they work offline |
| `manifest.webmanifest`, `sw.js`, `icons/` | Home-screen install and offline use for the web version |
| `scripts/configure-ios.sh` | Makes the Xcode project iPad-only, enables Files-app access |
| `codemagic.yaml` | Cloud build to TestFlight (no Mac needed) |

When you add a new script or image to the app, add its file name to the `files` list in
`scripts/build-web.js`.

## Test on your iPad today (no Apple account needed)

The app is also installable straight from the web, full screen and working offline:

1. On GitHub: repo **Settings > Pages > Build and deployment**. Set Source to **Deploy from a branch**,
   pick the `ipad-app` branch (or `main` after merging) and the `/ (root)` folder, then Save.
2. After a minute or two the site is live at `https://checkdesignz26.github.io/sketchpad/`.
3. Open that link in **Safari on your iPad**, tap **Share > Add to Home Screen**.
4. Open it from the new Pattern Sketch icon. It runs full screen and keeps working with no internet.

This is the same code that goes into the App Store build, so Pencil feel, speed and layout can be
tested now. Differences in the real app: the share sheet for saves, and no Safari "add to home
screen" step. Replace the placeholder icon by dropping your 1024x1024 artwork into
`icons/icon-1024.png` and running `python3 scripts/make-placeholder-icons.py --resize-only`.

## One-time setup (no Mac)

1. **Apple Developer Program** (US$99/year): https://developer.apple.com/programs/enroll/
2. **App Store Connect**: create the app record. Use bundle ID `com.seamlesscreative.patternsketch`
   (or change it in `capacitor.config.json` and `codemagic.yaml`). Note its numeric Apple ID.
3. **App Store Connect API key**: Users and Access > Integrations > App Store Connect API > generate a key.
4. **Codemagic** (https://codemagic.io, sign in with GitHub): add this repo, then
   Teams > Integrations > Apple Developer Portal and add the API key. Put the integration's name
   in `codemagic.yaml` (`integrations.app_store_connect`) and the app's Apple ID in `APP_STORE_APPLE_ID`.
5. Start the `patternsketch-ipad` workflow. When it finishes, the build appears in TestFlight.
6. Install **TestFlight** on your iPad and test with a real Apple Pencil.

## Two-row toolbar

- Row 1: **📁 Projects**, the project name with a ▾ menu (Rename, New Project, Save, Download Project, Import Project, Earlier Saves), small autosave text, Undo, Redo, **📸 Export ▾** (PNG tile / SVG options).
- Row 2: **Select ▾** (Select Area, Select All, Select same colour/stroke/fill; shows "Select Area ON" while armed), **🖊️ Stroke tools**, **100% ▾** (Fit, 100%, reset rotation, reset view) and **👁️ View ▾** (rotation value + reset, Guides, symmetry, tiling, theme, reset view).
- The original buttons still exist, hidden in `#tbLegacy`; menu items press them, so every handler is unchanged. When a row runs out of room, lowest-priority items move into a labelled **⋯ More** menu instead of wrapping.

## Blend between motifs and groups

- Select a motif, or a group, tap **🌀 Blend with another…** (motif panel) or **🌀 Blend two…** (selection panel), then tap the second motif or group. Or select exactly two first and tap Blend.
- **Shape morph** is real and only used when both are all vector paths that pair up reliably (same path count, matching open/closed, similar arrangement). Otherwise it is a **transform blend** (position, size, turn, opacity, colour) with each step a copy of the nearer original — never a crossfade — and the panel says why in plain English. Pictures are always transform-only and keep their full available quality.
- The result is live: edit either original and it regenerates; Reverse direction, steps and the toggles update it; Undo removes it in one step; Expand turns each step into its own editable group. Stored as `oblendId`/`oblendSpec` on ordinary strokes and placed copies, so save/load, SVG export and tiling work unchanged. Placed items gained an optional `alpha`.
- Limits: transform blends turn only when both ends are single motifs; morphed paths travel in straight lines, not arcs; colour shifts apply to vector strokes only; steps are capped for very heavy artwork.

## Sharper motif and pattern brush tips

- Motif stamp brushes now redraw their tip from the motif's saved vector paths at a power-of-two size (64–2048 px) chosen from the brush size times the canvas's current scale, so big stamps and deep zoom stay crisp. Tips are cached per motif and size, refresh when the motif is edited, and are trimmed to a 24-megapixel budget. Bitmap-only tips use progressively larger copies of the original picture, never enlarged beyond it.

## Projects (folders, autosave per project)

- **📁 Projects** and **➕ New Project** are the first two buttons in the toolbar; the open project's name sits next to them (tap it to rename).
- Storage: the same IndexedDB (`pkmSketchDocDB`, now v2) gains `projects` (small records + thumbnail), `projdocs` (the full editable document, the same `buildDocObject()` payload as before) and `folders`. The old `doc/current` and `backup:*` keys are never modified; on first launch they are copied into a **Recovered drawing** project (with its earlier saves).
- Autosave writes to the open project 1.2 s after a change. The pill shows Unsaved… / Saving… / Saved hh:mm, and Saved only appears after the write completes. A failed write turns it red and retries; creating, opening or switching a project first saves the current one and refuses (with a Download option) if that fails.
- Folders are one level deep. Delete moves a project to Trash (restore or delete forever there). Duplicate makes an independent copy. Export / Import use the existing editable `.json` project file, which now also carries the project name; importing creates a new project.
- Known limits: the canvas is still a fixed square 780 px tile on an 1800 px working canvas, so there is no per-project canvas size yet. Custom brushes live in one shared library, with copies stored inside each project.

## Before submitting to the App Store

- App icon (1024x1024 PNG, no transparency) and iPad screenshots (13-inch iPad: 2064x2752 or 2752x2064).
- Privacy policy URL. The app stores everything on-device, so the privacy answers are simple.
- App name, subtitle, description, keywords, category (Graphics and Design), price.
- Apple reviews for Guideline 4.2 (apps must be more than a website). Pencil pressure, offline
  drawing, autosave, and the share sheet all help. In the review notes, mention Apple Pencil support
  and that everything works offline.

## Local web preview

Open `index.html` in a browser, as before. To check the offline bundle: `npm run build:web`.

## Fine stroke sizes (v52)
- Brush Size and selected-stroke Width now go down to 0.05 (slider step 0.05).
- Each has a number box (type any value, e.g. 0.25 or 2) plus a ▾ dropdown of common sizes (0.1 … 400).

## Shape controls in the floating Stroke panel (v53)
- Selecting a polygon/star now shows Sides / Points / Depth sliders right in the floating Stroke panel (range 3–24), mirrored with the Shape Controls in the left Stroke tools panel.

## Calligraphy brush (v54)
- New "Calligraphy" brush (Inking family): flat nib at a fixed angle. Size = nib width; Nib angle (0–180°) and Nib thickness (2–60%) sliders appear under the brush settings. Drawn as one filled shape so opacity stays even; Pencil pressure thins the nib slightly.

## Bézier Pen + quick Pen/Eraser (v55)
- Top toolbar (row 2) now has 🖋️ Pen and 🧹 Eraser buttons next to Select.
- Pen: tap = corner point, drag = pull smooth curve handles, tap the pink first point (or Close shape) = close, Done/Enter = finish. Drag points/handles to reshape, double-tap a point = smooth/corner. Result is a normal stroke in the selected brush; keeps `stroke.bez` so Edit Mode → 🖋️ Edit Curve reopens it (hidden once the stroke has been moved/scaled/node-edited). Finger pans; Pencil/mouse places points. Symmetry is not applied to Pen paths.

## Pencil + brush dropdown in the toolbar (v56)
- ✏️ Pencil (back to freehand with the current brush, turning off Pen/Eraser/shape tools) plus a ▾ that lists every brush grouped by family; picking one selects it and starts drawing.

## Size box in the toolbar (v57)
- Number box + ▾ presets next to Pencil sets the size of the current brush (or the eraser while it's on); synced with the Size slider in the side panel. With the side panel open on a 10.2" iPad, zoom % and Stroke tools sit in ⋯ More.

## Resizable floating panels (v58)
- Every floating panel (Stroke, Blend, Group, Rotate, Edit Path…) has a ◢ grip at its bottom-right: drag to resize (grows left/up if it's against the canvas edge, scrolls inside when smaller), size remembered (localStorage `sp-fpSize`), double-tap the grip to reset.

## Warp, Smooth Path, simpler shape nodes (v59)
- 🌀 Warp (toolbar; in ⋯ More when narrow): drag to push/bend strokes on the active layer. Size and Strength sliders in its bar; shapes/node paths become free paths when warped. One undo step per drag.
- 〰️ Smooth Path (Stroke panel, both floating and left): amount 1–10, relaxes wobble, repeatable.
- Edit Path on a circle/ellipse now opens with 8 smooth nodes (was ~dozens); other curvy shapes (heart, teardrop, rounded rect) use the fewest nodes that stay within ~0.4% of the outline.

## Trace Image to Vector (v60)
- ✨ Trace Image to Vector (sidebar → Trace Reference, and the project name menu): pick an image → Colours (k-means, 2–24 colours, background removable) or Line art (threshold + ink colour) + Detail slider → filled vector shapes on a new "Trace: …" layer. Colours are stacked big→small (no gaps), holes/islands kept (holes use a zero-width slit so shapes stay single closed fills; those shapes have no nodes), shapes without holes keep editable smooth/corner nodes. Image is traced at ≤800 px then fitted to the canvas; undo removes the whole trace. SVG export works via the existing fill export.
- Test hook: `window.__sketchpadVT.run(opts)`.

## Trace: before/after + not tiled (v61)
- The trace dialog now shows Before and After (live vector preview, updates as options change; checkerboard shows removed background) and only places the result when you tap Place on canvas.
- "Size on canvas" defaults to filling the canvas; placing it turns tiling off so it's shown once. "Fit inside one repeat tile" is still available for patterns.

## v62 — Trace: Detail slider + zoom
- The Detail slider now visibly changes the result (resolution, simplification, speckle clean-up, smoothing).
- Before/After preview has zoom (− / slider / + / Fit), drag to pan, pinch and mouse-wheel. The vector side is redrawn sharp at every zoom level.

## v63 — Minimum default size 1
- Any saved brush size below 1 (e.g. a Pencil left at 0.1) is reset to 1 once; arming a shape tool with a size under 1 sets it to 1 so shapes stay visible. You can still type smaller sizes yourself.

## v64 — Trace dialog layout
- Zoom row moved above the Before/After panes; panes capped at 38% of screen height so zoom, panes and options fit without scrolling on iPad.

## v65 — Updates bypass the browser's HTTP cache
- The service worker now revalidates files with the server (cache: 'no-cache') so "⟳ Get latest version" picks up new releases straight away instead of a copy cached for up to ~10 minutes.

## v66 — Trace: Smooth shading
- New "🌈 Smooth shading" checkbox in the trace dialog (colour mode): uses at least 16 tones (up to 32) so gradients and shadows blend with finer steps instead of a few flat bands. More shapes, still fully vector.

## v67 — Trace dialog: options higher up
- "Remove the background" and "Smooth shading" checkboxes now sit directly under Mode, and the preview panes are a little shorter, so they're visible without scrolling on iPad.

## v68 — Quick Duplicate + double-tap
- New **⧉ Duplicate** button in the second toolbar row (moves into ⋯ More when the bar is narrow). Duplicates the selected shape/stroke, picture, or a multi-selection/group (copies appear offset, ungrouped).
- **Double-tap (or double-click) a selected item in Edit mode** to duplicate it. Turn this off any time in View ▾ → "Double-tap a selected item to duplicate it".

## v69 — Trace: centre-line strokes
- In **Line art** mode the trace dialog has a new **Result** menu: *Filled shapes* (as before) or *Centre-line strokes*. Centre-line thins each ink line to its middle and places it as a normal editable Smooth Pen stroke (curved nodes, width taken from the original line), so you can restyle, recolour, change width/brush or Edit Path afterwards.
- Works best on clean line art with fairly even line thickness. Lines that meet are split into separate strokes at the junction.

## v70 — Trace: exactly one repeat tile
- "Size on canvas" has a new option **Exactly one repeat tile (for a seamless pattern tile)**: the traced picture is placed to fill exactly the repeat tile (edge to edge), with tiling left on. Untick "Remove the background colour" when the picture is a full tile with its own background.

## v71 — Duplicate button always visible; sturdier double-tap
- The **⧉ Duplicate** button now sits right next to Select and never moves into ⋯ More.
- Double-tap duplicate is more forgiving (500 ms / 45 px) and always duplicates what the first tap selected. Use Apple Pencil (or mouse) in Edit mode — finger taps pan/zoom, as elsewhere in the app.

## v72 — ⚡ Quick actions floating panel
- New **⚡** button in the toolbar (next to Select) opens a floating panel you can drag anywhere on the canvas (it remembers where you left it): **☝️ Select**, **✥ Move**, **⧉ Duplicate**, **🗑 Delete**, **🧹 Erase**, **✏️ Draw**.
- **Move** lets you drag any shape, stroke or picture straight away (no select-first step). Delete works on shapes, strokes, pictures and multi-selections, and Undo brings them back. Erase toggles the eraser; Draw returns to the pen.

## v73 — Centre-line trace refinements (dense line art)
- Higher source resolution for centre-line mode (up to ~2600 px at Detail 10), so fine hatching stays separate.
- Solid black areas (thick blobs, filled flames, etc.) are now traced as filled shapes instead of fat strokes; only genuine lines become strokes.
- Short corner stubs left by thinning are removed, and long straight runs get extra nodes so rounded rectangles stay clean (no overshoot "ticks").
- The dialog reports "N editable strokes + M solid shapes".

## v74 — Version number shown
- The "⟳ Get latest version" button (View ▾ / ⋯ More, in the View panel) now shows which version you have, e.g. "(you have v74)". Bump this label with sw.js each release.

## v75 — Get latest version bypasses all caches
- "⟳ Get latest version" now re-downloads index/script files with cache bypass, clears the app's cached copies, then reloads with a fresh `?v=` address, so an update shows up on the first tap.
- If an update ever doesn't appear: open the site address in Safari with `?v=1` on the end, and check the repo's **Actions** tab for a failed "pages build and deployment".

## v76 — Slimmer side panel
- Left tools panel is narrower (236 px, was 300) and the collapse bar is thinner (22 px, was 40), so the whole top toolbar (Select, ⚡, Duplicate, Pencil, size, Pen, Eraser, View, More) fits on iPad.

## v77
- Line-art centre-line trace: adaptive (local-mean) thresholding so dense detail like pine needles no longer fuses into black blobs; solid-area detection is measured only on clearly dark pixels, faint borderline ink still becomes thin strokes.

## v78
- Line-art trace, Filled shapes: no pre-blur, up to 2x sampling and adaptive thresholding, so fine hatching like pine needles stays as separate thin shapes instead of merging.

## v79
- Centre-line trace: small thick clumps (needle junctions, dots) stay as line work; only large dark areas become solid fills.

## v80
- Trace dialog: "Line weight" slider for Centre-line strokes (60-220%, default 120%) so lines can be made bolder or thinner.

## v81
- Centre-line trace keeps tiny dark dots (eyes, buttons) that used to be discarded as too short; only clearly dark ones, so paper speckle is ignored.

## v82
- Trace dialog: "Trace just an area" - drag a box on the Before picture (zoom first if you like) and only that region is traced, which keeps small details sharp on big sheets. "Whole picture" goes back.

## v83 — Trace dialog
- **↺ Reset area & zoom** button.
- The picture (and its settings) you trace from is saved with the project; Done no longer loses it. "Forget" removes it.
- Adjust the area: drag inside to move it, drag edges/corners to resize, drag outside to draw a new one.
