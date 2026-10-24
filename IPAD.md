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

## v84 — Small areas trace in more detail
- When the picture or boxed area is small (under 500 px), it is enlarged up to 5x before tracing, so tiny details like house windows survive.

## v85 — Curve smoothing
- New "Curve smoothing (sharp to rounded)" slider (0-10, default 4) for centre-line traces. Higher = rounder curves and fewer sharp corners (good for lace and scrollwork). Saved with the project.

## v86 — Remove background in Line art
- New "Remove the background (coloured or dark backdrop)" option in Line art mode, with a Background tolerance slider. Finds the backdrop colour from the picture edge and clears it so it is not traced as ink. Off by default; saved with the project.

## v87 — Vector / Raster engine switch
- Every drawing brush now has an Engine switch (Vector | Raster) under the brush preview. Raster paints with grain and soft build-up, and can pick up colour already on the layer (Wet mix) or break up like dry media (Dry / grainy). Strokes are still kept as editable points, so undo, saving, the eraser and Apply Style all still work.
- Gouache, Dry Brush and the new Watercolour and Dry Ink brushes start on Raster. Switching engine only affects new strokes.

## v88 — Faster eraser
- The eraser now rubs out pixels instantly while you drag and does the exact stroke re-render once when you lift, and skips strokes that are nowhere near the eraser. Much smoother on drawings with lots of strokes.

## v89 — Eraser, exact and fast
- v88 erased pixels live and put some back when you lifted the pen, which looked odd. The eraser now redraws only the strokes near what it cut (exact every frame) instead of the whole layer, and no longer paints over thick strokes it did not actually touch.

## v90 — Layer names in a narrow panel
- When the left panel is narrow, each layer row now wraps: the name stays readable and the opacity slider and buttons move to a second line.

## v91 — Raster brush stability
- Raster brushes now redraw the whole stroke while you draw (no more seams or blobby stacking from drawing it in slices), cap the size of their scratch image so the iPad does not run out of memory when zoomed in, and fall back to the vector look if anything goes wrong.

## v92 — Less lag with raster brushes
- Raster strokes now read the canvas once per stroke instead of dozens of times (what made the iPad stall), use fewer dabs, and skip colour pick-up when Wet mix is near zero.

## v93 — Faster drawing in tiled mode
- While the pen is down only the tile you draw in is updated (other tiles catch up when you lift). Zoomed in with tiling on, the live stroke used to be redrawn 9 times per frame. New toggle "Live tile preview" (Off by default) brings the old behaviour back.

## v94 — Fewer re-renders while zooming
- Zooming back and forth around a sharpness threshold no longer re-renders every stroke each time (added hysteresis), and re-rendering at a coarser resolution waits until zooming settles.

## v95 — Smoother pinch zoom
- The sharpness re-render no longer runs while two fingers are still on the screen (it froze the app mid-pinch, which made the zoom stutter and jump). It waits until you let go.

## v96 — Pinch zoom no longer jumps
- If two fingers start very close together, the pinch used to multiply the zoom by a huge ratio and shoot to maximum. The starting gap now has a minimum, and zoom can change by at most 1.5x per touch update, so a stalled frame cannot cause a leap.

## v97 — Big groups resize smoothly
Groups with many strokes (or raster brushes) are drawn once into a picture while you drag a handle, so resizing the goose no longer redraws 381 strokes every frame. The sharp redraw happens once when you let go.

## v98 — Lighter group resize/move
While dragging a big group the preview picture is half-size, the canvas is no longer fully recomposited on every frame (about 4x less work per frame in my test), and letting go only redraws the layers the group sits on.

## v99 — Motifs stay where you drew them
Capture Motif / Capture Area now place the motif exactly where the drawing was, at its real size (no more jumping to the centre). New "Turn into motif (fast)" button in the Group panel for heavy drawings. A "Edit Motif" button now sits under a selected motif.

## v100 — Edit Motif in place, softer brush preview
Editing a motif now shows its strokes exactly where that motif sits (same position, size and turn) and hides the picture of it meanwhile, so there is no second copy. Tap Done and it goes back. The brush preview for very light colours uses a soft lilac instead of dark grey.

## v101-v102 — Style many strokes, alpha lock, blend modes
- Group panel: Opacity box (with Apply to all) and "Use my current brush" redraws every selected stroke with the chosen brush, keeping each stroke colour and size.
- Layers: α button = alpha lock (new paint only lands where the layer already has paint, so you can recolour without spilling). Blend-mode picker per layer (Multiply, Screen, Overlay, Soft light, Hard light, Darken, Lighten, Dodge, Burn, Colour, Luminosity). Both are saved with the project and undo.

## v103 — Double-tap a motif opens it for editing
Double-tapping a selected motif with editable artwork now opens Edit Motif instead of making a duplicate. The Duplicate button still copies.

## v104 — Edit Motif banner
While a motif is being edited a Done / Cancel banner stays at the top of the canvas (the old Done pill could be hidden in the cut-off toolbar). Cancel leaves the motif unchanged. After Done or Cancel the motif stays selected. Pressing Edit Motif while already editing now says so.

## v105 — Edit Motif opens in select mode
Editing a motif now starts in Edit (select) mode so tapping a stroke brings up its stroke panel (colour, width, Edit Path). Switch to Draw to add strokes.

## v106 — Error toast
If a script error happens a red note appears at the bottom of the screen with the message, so a screenshot shows exactly what failed. The More menu also reports its own errors there.

## v107 — Symmetry button in the toolbar
A 🦋 Symmetry button now sits in the main toolbar next to Eraser (it was hidden inside View, which can end up under the More menu). It shows the active mode.

## v108 — Floating Symmetry panel
The Symmetry panel is now a floating panel: drag it by its title bar, it stays where you leave it while you draw, and Done closes it.

## v109 — More button always on screen
The toolbar could end up one button too wide so the More button was pushed off the right edge. Duplicate, Quick actions, Pen and Eraser now tuck into More when space is short, and the Symmetry button is compact (just the butterfly, with the mode name when on). More now always fits on screen.

## v110 — Vector / Pixel filter for the left panel
A switch at the top of the left panel: All, Vector or Pixel. Vector-only sections (Trace Reference, Shapes, Vector Area Fill, Selected Stroke) carry a teal VECTOR tag; pixel-only sections (Pattern Brush, Motif Brush Set) carry a coral PIXEL tag. Vector hides the pixel ones and Pixel hides the vector ones; shared sections (Colour, Draw, Layers, etc.) always show. Remembered between sessions.

## v111 — Pixel tag colour
The Pixel filter button and PIXEL tags are now a soft blue instead of orange.

## v112 — Tidier top toolbar
Main drawing bar now: Select, Pencil (brush list), Stroke tools (🖊️, next to Pencil), size, Pen, Eraser, Symmetry. View, Zoom, Warp, Duplicate and Quick actions live in the ⋯ More menu. If the window is narrow, Symmetry then Eraser then Pen move into More first.

## v113 — Quick and Duplicate back on the bar
Quick actions (⚡) and Duplicate (⧉) are back on the main bar; Pen and Eraser are now icon-only to make room. Everything still tucks into More on narrow screens.

## v114 — Rotate the symmetry axis
The Symmetry panel has an Angle slider (-90 to 90) plus 0° and 45° buttons. The mirror line(s) turn around the axis point, and the on-canvas crosshair now shows the real direction (and is longer).

## v115 — Mirrored editing
Strokes drawn together with Symmetry on now share a link (symId + their own mirror matrix). Move, resize, turn, Edit Path, colour or size on ONE of them and its twin(s) follow, mirrored. If both are changed in the same step (e.g. both in one group move) nothing extra happens. The eraser does not mirror. Older strokes have no link.

## v116 — Eraser mirrors too
With Symmetry on, the eraser also erases at the mirrored spot(s), like drawing does.

## v117 — Long, draggable symmetry axis
The mirror line(s) now run across the whole canvas (only the lines that matter for the chosen mode), and the pink circle can be dragged with the pen to move the axis anywhere. The sliders still work.

## v118 — Axis locks on Done
The symmetry axis can only be dragged while the Symmetry panel is open. Tap Done and it is fixed (the pink circle ignores touches). Reopen the panel to move it again.

## v119 — Short or whole-canvas axis line
Symmetry panel: "Line: whole canvas" or "Line: short" with a Length slider. The short line is sized in canvas units, so it grows and shrinks with zoom and stays the size of the element. Only the drawn guide changes; mirroring itself is the same. Choice is remembered.

## v120 — 🎥 Timelapse (capture → replay → export)
**Where:** ⋯ More → 🎥 Timelapse. It opens a small panel with the replay, length (Auto / 10–90 s), size (720 / 1080), the seamless-repeat ending option, ▶ replay, 🎞️ Export video, recording on/off and 🗑️ Delete timelapse data.

**How it records (action log, not video):** every artwork change is stored as a small delta when the app records an undo step (strokes with their own brush/settings, erases, fills, group move/resize/turn, layer changes, placed motifs). Because all artwork (vector and pixel brushes) is rebuilt from stroke data, replay is exact; the replay re-draws into its own hidden canvases, so no UI, handles, grids, zoom, pan or rotation can appear. Only the time the pen was down is kept per action, so thinking pauses vanish. Undo trims the log (an undone edit never shows in the video), redo puts it back. Edit Motif sessions are not recorded; the result shows when the motif is finished.

**Storage/memory bounds:** one IndexedDB store `timelapse` (DB version 3), chunked, written only when changed (about 4 s after drawing). The log is capped at about 8 MB / 6000 actions; beyond that the oldest actions are folded into the starting picture. Nothing is saved per frame and no images are stored.

**Projects:** new (empty) projects record automatically (setting "Record every new project automatically"). Existing projects start with recording off — use "Start recording from now" (no earlier history is invented). Turning recording off and on again adds anything drawn meanwhile as one quick jump. The data is kept with the project, survives reopening, and is deleted with the project (or on its own with 🗑️).

**Export:** 30 fps square video of the finished tile (the same artwork as "Export image (PNG tile)"). Path 1: WebCodecs H.264 encoder -> built-in MP4 writer (works offline, fast, plays in Photos). Path 2 (if the device has no WebCodecs/H.264): MediaRecorder in real time (MP4 on Safari, WebM on Chrome/Firefox). Saved with the same save/share sheet as other exports. Optional ending: hold on the finished art, then zoom out to show the pattern repeating in the project's repeat layout.

**Limits:** placed motif pictures and the background image in the replay use their current versions; edits to older strokes made before recording started cannot be replayed; the replay renders at 1:1 tile size (1080 export is upscaled); the real-time fallback can drop frames on heavy brushes; H.264 export has been verified here with real H.264 data and the MP4 writer, but not yet on a physical iPad.

## v121 — Timelapse button on the toolbar, recording on for every project
A 🎥 button sits on the toolbar next to 🦋 (🎥🔴 while recording; it moves into ⋯ More only if the bar is full). Every project, new or existing, now starts recording automatically from how it looks when opened (nothing earlier is invented); the "Record every new project automatically" tickbox now defaults to on again (stored under a new key, so an earlier accidental untick no longer applies). Per-project off stays off.

## v122 — Faster timelapse
Auto length is about 15x faster than real drawing (min 5 s, max 40 s) and the Length list now has 4 s, 6 s, 10 s, 15 s and 20 s options.

## v123 — Timelapse drawing part twice as fast
Auto length is now about 30x real drawing speed (min 3 s, max 30 s); short strokes get a smaller minimum time. The ending (1 s hold on the finished tile, 2.8 s zoom-out to the repeat, 1.6 s hold) is unchanged. Fixed Length choices still set the drawing part exactly; a 3 s option was added.

## v124 — Timelapse speed in between
Auto length is now about 21x real drawing speed (min 4 s, max 35 s): between v122 (15x) and v123 (30x). The Length list overrides it.

## v125 — Timelapse a touch slower
Auto length is about 18x real drawing speed (min 5 s, max 40 s).

## v126 — tidier left panel, Edit button, steady top bar
- Left panel: tap any section title to fold it; "Collapse all / Expand all" under the Vector/Pixel filter. State in localStorage `sp-secFold`.
- ↔️ Edit button in the top bar (always visible) and in the ⚡ Quick panel; both follow `#editModeBtn`'s `active` class.
- Edit Path panel has 〰️ Smooth Path + amount slider (`smoothCurrentPath`, works on the live nodes; Done keeps it, Cancel/undo discards).
- Top bar: 🎥 no longer changes width (recording shows a red dot via `.rec`); `tbFitRow` has 28px hysteresis so items don't hop in/out of ⋯ More; Duplicate moves to More before 🎥.

## v127 — timelapse: duplicate keeps recording, style changes recorded correctly
- Duplicate Project copies the timelapse (`SPTimelapse.copyFor`).
- A colour/brush/fill change on an existing stroke was mistaken for a pure move/resize (`detectTransform`) and dropped; settings edited in place (width slider) were not noticed. Now: transforms require identical style fields, settings are compared by value (`setJ` taken when the record is made).

## v128 — copy a recording from another project
- 🎥 panel: "Copy recording from another project…" lists projects that have a recording and copies it into the open project (`copyFor` + reload). Drawing continues from there; a correction event covers any difference between the copied recording and the current artwork.

## v129 — text & fonts, text on a path, blend along a path
**Text**
- A text object is a stroke with a `text` block (`str, font{src,family}, weight, italic, size, align, ls, lh, opacity, path`); fill = `stroke.color`; `points` hold the box corners so move/scale/rotate/duplicate/layers/undo/save all reuse the stroke machinery. Drawn as live vector text (crisp at any zoom).
- Add via 🔤 Text section in the left panel, ⋯ More → Text, or ⚡ Quick → Text. Tap the canvas to place, edit wording in the panel; tap the text again to reopen.
- `fonts.js` (`window.SPFonts`) owns fonts: separate IndexedDB `sp-fonts`; sources Built-in (`fonts/*.woff`, 17 OFL families, licences in `fonts/licenses/`), Google (downloaded on demand from the public css2 endpoint — no API key — and kept offline), Imported (.ttf/.otf, validated, de-duplicated by SHA-256). The Google *name list* is `fonts/google-index.json` (names only). Nothing is loaded at startup except what the open project uses.
- Projects embed the font files they use (`doc.fonts`), so a project opens correctly on another device; a font that cannot be found is named in a banner and is never silently replaced.
- Convert to outlines is an undoable step (traced curves, dense polylines). SVG export: live `<text>` with embedded `@font-face`, or outlined paths (no font needed).
- Undo/Redo now trigger an autosave (previously an undo followed by closing the app could be lost).
**Text on a path**: text panel → "Text on a path" → tap any line/curve/shape. Start slider, align, distance, reverse, flip side, hide the guide, edit guide, straight again. Deleting the guide returns the text to a straight line. Hidden guides use `stroke.guideHidden` (not drawn, not exported, not hit-tested).
**Blend along a path** (extends the object blend; `spec.path`, `spec.rep`):
- Blend panel → "Along a path" → Choose a path. Copies are placed by arc length: closed paths use n copies at k/n (no doubled seam), open paths put copies on both ends or only between them; spacing mode derives the count from a gap (max 200 copies, and the existing point budget). Start/end gaps, reverse, turn with path + extra turn, hide the path.
- Morph (when the two shapes pair up) or transform blend runs first as before, then every copy is moved onto the path. Not-morphable pairs say why in the panel.
- "Repeat just this one along a path": one source, copies change size / opacity / spin along the path.
- Live: moving the path or either source regenerates the copies (`objSig` includes the guide). Expand makes ordinary groups (undoable). Deleting the path turns it back into a straight blend. A blend made the older way (two plain strokes, already applied) cannot take a path; new ones convert automatically when a path is chosen.
**Offline/PWA/Capacitor**: `sw.js` caches `fonts.js`, `fonts/*`; `scripts/build-web.js` copies them into `www/` for Capacitor. Google downloads need a connection once per family.
**Not tested on a real iPad.** Google download was tested only against a mocked endpoint (no network in the build sandbox).

## v130 — timelapse keeps more before merging early actions
Recordings merge their oldest actions into the starting picture once they pass a size limit (they then appear instantly instead of being drawn). Limits raised from 6000 actions / 8 MB to 20000 / 24 MB. The 🎥 panel status line says when this has happened ("the earliest N actions were merged…"). Already-merged recordings cannot be un-merged.

## v131 — save, download and import colour palettes
- 🎨 palette section: name box + "💾 Save this palette" stores the swatches currently shown (kept with the project in `savedPalettes`, alongside the image-extracted ones).
- Saved palettes: ⬇ per palette, "Download all", file type chooser (.json, Adobe .ase, GIMP/Krita .gpl, hex list .txt). "⬆ Import palette…" reads those same types plus any text/CSS/SVG with hex codes; duplicate names get "(2)"; unreadable files give a message.

## v132 — rectangular tiles (cards), stroke size box fix
- Tile shape: 📐 Repeat Layouts → "Tile shape" (Square, 5×7, 7×5, 4×6, 6×4, A-size, 3:4, 4:3, 9:16, custom ratio) and in the New Project dialog. The tile's long side stays 780 units (`TILE`); `TW`×`TH` is the real tile, centred on the 1800 canvas (`CX,CY`). Grid / half drop / half brick / diamond all use `tilePos()` with TW/TH. Saved in the project (`doc.tileW/tileH`, meta `canvas.tw/th`); older projects open as square. Changing the shape later does not move artwork.
- Updated for TW×TH: fabric repeat, background, guides, templates (`applyBricks`), align bounds, PNG tile export, SVG export (width/height/viewBox), thumbnails, trace fit, vector-trace fit, timelapse replay (letterboxed in the square video).
- Stroke size boxes: when a different stroke is selected the number box now drops focus and shows that stroke's real size, so typing the same number as before works (the box used to keep the old number while it still had the keyboard).
- Note: PNG tile export is still the tile at 780 px on its long side; use SVG for large sizes.

## v133 — startup safety net
If the app throws an error while opening (blank canvas, empty size box), a red banner at the bottom now says what failed; the last error is also kept in localStorage `sp-lastErr`.

## v134 – High-resolution card export
- Export menu → **🖼️ Export card (hi-res PNG)…**. Redraws all strokes (every brush), placed pictures and the background image at the chosen size, from the original stroke data, so it is sharp rather than a stretched small image. Just the card: no wrapped neighbour edges.
- You pick the **long side** in px (presets 2100 / 3000 / 4000, or type your own). It shows the pixel size and print size at 300 dpi. A transparent-background option is included. The file is tagged 300 dpi.
- Limited to about 14 million pixels in total so the iPad can make it (a 5×7-shaped card goes up to roughly 2850 × 4000).
- Saved as `pattern-sketch-card-WxH.png`.

## v135 – Stay in Draw lock + guide path stays hidden
- **More → 🔓 Stay in Draw** (saved on the device). When on, the app never jumps into Edit by itself, and the toolbar Edit button needs two taps within 1.5 s. Select menu / Select Area still switch to Edit when you choose them.
- "Hide the guide path" (text on a path) is now a lasting setting. The guide only shows while you are editing it (Edit guide path) and hides again once you deselect it.

## v136 – Move text on a path
- Select text that sits on a path, then drag it: its guide path moves with it (even when the guide is hidden) and the text follows live. Use "Edit guide path" to reshape the path instead.

## v137 – Smooth dragging of path text
- Dragging text on a path now moves a light picture of the text while you drag (like moving a stroke), and the guide path and text are re-laid out once when you let go. No more rebuilding every layer on every move.

## v138 – Motif opacity
- Selected Motif section now has an **Opacity** slider (5–100 %). Saved with the project and used in the PNG / hi-res exports.

## v139 – Text on its own layer
- New text is created on a layer called **Text** (made automatically, kept on top). In the text panel, **📚 Move to Text layer** moves existing text there.

## v140 – Eraser hits the visible paint
- The eraser used to test only against the thin centre line of a stroke, so a small eraser (e.g. size 5) could miss a brush mark even when it covered part of the paint. It now counts the brush width too, so touching any visible part of a stroke erases there.

## v141 – Eraser says why it erased nothing
- If an erase drag removes nothing, the status bar now says why: the paint is on another layer (names it), the layer is locked, it is a placed picture/motif, or it is the background image.

## v142 – Erase through the repeat clones
- With Tiling on, erasing a mark you see in an edge clone now erases the original too (the eraser works at every repeat position).

## v143 – Timelapse keeps much more (160 MB)
- The recording was already saved in the device database (IndexedDB), but it was also held in memory with a 24 MB limit, and past that the oldest actions were merged into the starting picture. The limit is now 160 MB / 60 000 actions, and the Timelapse panel shows "x MB of 160 MB room". A project already merged cannot get its old actions back.

## v144 – Hi-res export in inches
- Hi-res card export now takes the card's long side in **inches** (presets 5.5 / 7 / 10 in) plus a dpi choice (150 / 200 / 300 / 600), and shows the result in inches and pixels. Pixels can still be typed. The PNG is tagged with the chosen dpi. A 5 × 7 in card at 300 dpi is 1500 × 2100 px.

## v145 – Gentler eraser
- The eraser counts only 40 % of the brush width (was 100 % in v140), so it no longer slices straight across thick strokes. Thick strokes need a larger eraser to cut through.

## v146 – Eraser: no more blur, gentler again
- While erasing, the sharp zoomed-in picture is no longer thrown away on every move (that made the whole screen blurry). The eraser circle is cut out of it live and it is fully re-sharpened a moment after you lift.
- Brush width counts only 20 % towards erasing (was 40 %), so thick strokes are cut much less.

## v147 – Import SVG as vector
- **🖋️ Import SVG (vector)** (under Add Motifs). Brings an .svg in as real editable vector pieces (fills, outlines, holes in compound shapes) on a new layer called "SVG: filename", fitted inside the tile. Move, resize, recolour and erase them like anything you drew.
- Imported: path, rect, circle, ellipse, line, polyline, polygon, with fill / stroke colours, stroke widths, opacity and transforms. Not imported: text (convert to outlines first), pictures, "use" copies, clipping / masks. Gradients become one flat colour. Scripts and links in the file are stripped for safety.

## v148 – SVG Tray + faster import
- **🖋️ SVG Tray** (under Import SVG): every SVG you import is kept on this device with a thumbnail. Tap a thumbnail to place it again on a new layer; ✕ removes it from the tray. You can pick several SVG files at once.
- Importing shows "Reading the SVG…" first, samples curves less densely (every ~2.5 px instead of 1.5), and reports how long it took.

## v149 – Stroke tools open while editing a motif
While "Editing motif: …" is active, selecting a stroke now shows the Stroke panel automatically (even if the 🖊️ Stroke button is off) and scrolls it into view.

## v150 – Import Illustrator (.ai) and PDF vectors
"Import SVG / AI / PDF (vector)" now accepts .ai and .pdf. The file's first page is read with pdf.js (bundled in `vendor/`, loaded only when you import one), converted to SVG and placed exactly like an SVG (new layer, SVG Tray). Hidden Illustrator layers stay hidden. Skipped: live text, pictures, gradients, clipping. .ai files saved without "Create PDF Compatible File" can't be read; Affinity files need exporting as SVG or PDF.

## v151 – Import Procreate brushes
Brush maker panel → "Import Procreate brushes (.brush / .brushset)". Reads the zip and Procreate's settings file, then makes Custom Brushes from the shape and grain images plus size, spacing, jitter/scatter, taper and pressure response. Procreate's "_original" backup copies are skipped. Built-in Procreate shapes and Procreate-only effects (wet mix, tilt shading, dual brush) aren't included, so imports are close matches, not exact copies. Needs iPadOS 16.4+ for unzipping.

## v152 – Procreate import: any file can be picked
The iPad file picker greyed out .brush/.brushset files (unknown type), so the import button no longer filters by file type.

## v153/v154 – Watercolour rebuilt, faster; compact Brush Studio with a try-out pad
- Watercolour is now its own engine: even transparent wash, pooled darker edge, soft feathered rim, slow pigment variation and paper grain. Sliders (Edge pooling, Soft wash, Paper grain) appear when Watercolour is selected in the Raster options.
- Speed: while drawing, only the new part of the stroke is painted (no re-painting the whole stroke on every move, no colour read-backs), so long strokes and tiled previews stay smooth. About 7x less engine work per move in desktop tests.
- Older watercolour strokes re-render with the new look.
- Brush Studio is now two columns with tabs (Basics, Tip & grain, Blend & colour, Dual brush) and has a try-out pad (Draw or Stamp, Clear) on the left that updates as you move sliders.

## v155 – Eraser on watercolour / raster brushes
Erasing a raster-feel stroke (watercolour, gouache, dry brush) no longer slices the line into pieces, which made each piece paint a new full-width wash and edge ("extra colour"). The stroke now keeps its shape and the eraser rubs out soft round spots from it. Undo, move, duplicate and group resize keep the rubbed-out spots with the stroke. Vector brushes are cut as before.

## v156 – Eraser styles
With the eraser selected, "Eraser style" appears: Hard line (crisp, even edge), Soft (feathered), Rough (ragged, chalky) and Like my brush (copies the softness and texture of the brush you draw with). It shapes how the eraser rubs out watercolour, gouache and other raster strokes; vector strokes are still cut cleanly.

## v157 – Smudge tool, brush name + colour in the top bar, eraser style in the top bar, remembers your last brush
- 👆 Smudge (next to the eraser; under More if the bar is narrow): drag to smear the paint on the active layer. Size and Strength sliders at the bottom. Kept as a stroke, so Undo, saving and hi-res export replay it. Not included in SVG export; the eraser ignores it.
- The brush button now shows the name of the brush you are using, and a round colour swatch next to the size box shows (and changes) the current colour.
- With the eraser on, an "Eraser style" button appears beside it in the top bar.
- The brush you last used is selected again when the app starts, including after an update.

## v158 – Smudge uses the selected brush
- Smudge now takes the footprint of the brush you have selected: its tip shape, softness and texture (e.g. Chalk and Dry Brush give grainy smears, Technical Pen a crisp one).
- Pick the brush with the "🖌️ Brush ▾" button in the smudge bar, from the sidebar, or from the toolbar brush menu while smudging.
- Each smudge stroke remembers its brush so undo/redo replays it identically.

## v159 – Smudge memory fix
- Smudge reuses its small working canvases instead of creating four new ones per stroke (iPad Safari hoards canvases until it runs out of memory and turns them black).
- Very large smudge sizes are capped internally, and a failure while rebuilding after a smudge no longer stops the app.

## v160 – Crash guard for projects with smudges
- If opening a project never finished last time, the app now opens it without replaying smudge strokes (they stay in the file) and shows a button to bring them back.
- Smudge replay is lighter (fewer steps per stroke), so projects with many smudges open faster.

## v161 – Capture Motif takes the SVG's name
- Capture Motif now names the new motif after the SVG you last placed (apple, then apple 2, apple 3…), so the Brush Set list shows real names without retyping. With no SVG placed it still says "Motif N".

## v162 – Stroke panel always opens while editing a motif
- The Selected Stroke panel could stay folded away (or off screen in the side panel) on later Edit Motif sessions. It now unfolds itself and scrolls into view every time you select a stroke while editing a motif.

## v163 – Memory budget for canvases
- Every layer owns two canvases and the sharp one grows with the square of the view sharpness, so a project with many layers could use far more memory than iPad Safari allows (screen goes black or the app reloads). The sharpness is now lowered automatically as layers are added, to stay inside a ~300 MB budget (3 layers stay sharp-ish, 8+ layers use standard sharpness).
- Canvases of deleted layers, and of the old layers when a project or motif is opened, are released straight away instead of piling up.

## v164 – Tighter memory (3-layer projects)
- Memory budget lowered (~220 MB): a 3-layer project now uses standard sharpness for the stored layers; zoomed-in views are still redrawn sharp by the detail layer.
- Undo, redo and Edit Motif no longer throw away and re-create every layer canvas; existing layers keep theirs and only removed layers are released.

## v165 – Memory check + smaller undo history
- New "🧠 Memory check" in the ⋯ More menu: shows what is using memory (layer canvases, screen canvases, motif pictures, undo history, stroke count).
- Undo history is trimmed by size (about 30 M characters), keeping at least the last 6 steps, so very detailed drawings no longer carry 40 full copies.

## v166 – Smaller saved drawing data
- Stroke points are saved rounded to 0.01 px (invisible), making undo steps, autosaves and project files roughly 40% smaller.
- Undo history budget lowered to ~24 M characters (keeps at least the last 4 steps).

## v167 – Gouache / Dry Brush colour pick-up no longer hammers memory
- Colour pick-up (the brush mixing in paint it passes over) used to read many tiny spots straight from the big layer canvas, which makes iPad Safari copy the whole canvas each time. It now shrinks the layer once into a small picture and samples that, so drawing with Gouache and Dry Brush no longer spikes memory.

## v168 – Layers share one canvas at standard sharpness
- At standard sharpness (renderScale 1) each layer's second "sharp" canvas was an exact copy of the first. Layers now use a single canvas there: saves ~13 MB per layer and halves the drawing work for every stroke, undo and eraser rub.
- The zoomed-in detail canvases are released when not needed.

## v169 – Zoomed-in view no longer relies on a giant canvas
- When zoomed in (and especially when rotated), the browser had to scale and rotate the whole 1800 px drawing canvas to several thousand pixels, which iPad Safari cannot hold (screen goes blank or black). Once the sharp screen-sized picture exists, only that is shown; the big canvas is hidden (still receives touches).
- While you pinch, pan or rotate, the sharp picture is moved and scaled with your fingers and redrawn about 0.1 s after you stop.

## v170 – Eraser no longer shows a fake hole
- While zoomed in, the eraser punched a hole in the sharp picture wherever you dragged, even on a layer it was not allowed to erase from. When you lifted, the paint came back, so it looked like the eraser worked only sometimes. The hole is now only shown where something was really erased (the status line still says when the active layer has nothing there).

## v171 – Eraser no longer re-reads paint from the canvas
- Gouache / Dry Brush work out their colour pick-up once per stroke and remember it. Before, every eraser rub (and every undo or redraw) re-read the canvas for each such stroke in the area, dozens of times per frame, which is what made the iPad run out of memory when erasing a heavily painted area. Erasing now does no canvas read-backs at all.

## v172 – Eraser says why when it cannot erase
- If something on the active layer is under the eraser but cannot be erased (a smudge mark, a filled shape, text or an unexpected stroke), the status line now names it, instead of wrongly blaming another layer.

## v173 – Eraser reaches the soft edges of wide strokes
- The eraser only noticed a wide brush stroke when it touched its centre line, so erasing the edge of a big painted area (like the cherry colour) did nothing. All wide strokes (8 px and up) are now rubbed out like paint, and the "is the eraser near this stroke" check uses the stroke's real width. Thin pen lines are still cut cleanly as vectors.

## v174 — crash when zooming out after erasing
The eraser/colour code reused shared scratch canvases that were shrunk to 1×1 and re-grown over and over while many strokes were redrawn after erasing. iPad Safari frees that memory lazily, so the churn piled up right when zooming out forced a redraw. They now only grow (in 512 px steps) and are released once, 8 seconds after you stop.

## v175 — unlimited layers (sleeping layers)
Each layer used to keep its own full-size canvas, so memory grew with every layer you added. Now only the layer you are painting on (and any layer with a blend mode) keeps real canvases. All other layers live as stroke data and are drawn into one or two shared flattened pictures that sit below and above the layer you are working on. Stacking order, opacity, hide/show and blend modes behave the same. The first time you switch to another layer there can be a short pause while the pictures are rebuilt. Memory check now shows how many layers are awake.

## v176 — resize a whole layer
Each layer row has a new ⤢ button. Tap it to select everything on that layer, then use the corner handles to resize, the round handle to turn it, or drag inside to move it (like a pixel layer in Affinity). Strokes are redrawn sharp at the new size, and Undo returns it.

## v177 — black paper while erasing zoomed in
While erasing on a zoomed-in view, the eraser's hole was punched right through the sharp picture, including the white paper, so the hole showed black until you lifted the pencil. The hole now shows white paper, and the proper redraw (with the layers underneath) still happens when you lift.

## v178 — copy artwork between projects, and a crash log
- More › Copy selection stores the selected strokes (or a whole layer, via its ⤢ button) in the browser's storage. In any other project, More › Paste copied artwork puts them on the active layer, selected so you can move them. Undo removes the paste. Strokes only: placed pictures and motifs are not copied yet.
- The app now keeps a short log of its last steps. If it closes unexpectedly, More › Memory check shows those steps the next time you open it.

## v179 — missing layers come back
If a saved file lists fewer layers than the strokes use, the strokes used to be dumped onto the top layer (which merged several layers into Outline). Now the missing layers are recreated as "Recovered" layers, so the layering is kept. For files already affected, More › Earlier Saves has automatic older versions.

## v180 — no more black paper while drawing zoomed in
Zoomed in, the app shows a screen-sized sharp picture and hides the huge normal canvas (which iPad Safari draws as black). Every time something changed, the sharp picture was thrown away first, so for a moment the huge canvas was shown and could go black. Now the sharp picture stays on screen until the fresh one is ready.

## v181 — less work and memory at very high zoom
The crash log showed the app closing at 820% zoom right after switching layers: it rebuilt the flattened layer pictures (6 layers' worth of strokes) and then redrew the sharp view straight afterwards. Zoomed in, the normal canvas is hidden behind the sharp picture, so rebuilding it is wasted. The rebuild is now skipped while zoomed in and done when you zoom back out. The crash log also records how long each sharp redraw takes.

## v182 — reuse canvases instead of creating new ones
Switching or adding a layer woke one layer (a new 13 MB canvas) and put another to sleep (thrown away). iPad Safari hands that memory back slowly, so many switches could pile up until the screen went blank. Canvases are now reused from a small pool: 36 layer switches plus adding a layer created only 3 new canvases (it was one or more per switch before). The flattening scratch pictures are also kept instead of being recreated each time.

## v183 — the screen repairs itself if iPad Safari wipes a canvas
Your Memory check after the blank canvas showed no crash and only about 115 MB in use, so the app was not closing: iPad Safari had quietly wiped a canvas (blank beige or black paper). Every canvas the app draws now carries one almost invisible pixel in its corner. Every 2 seconds (and when you come back to the app) the app checks those pixels; if one is gone, that canvas was wiped, and it is redrawn from the strokes. Tested by wiping the main canvas, the sharp zoomed-in picture, the layer canvases, the flattened pictures and the display picture. All came back.

## v184-185
- Tiling off now shows just the tile at its real shape, fitted to the screen, with the area outside it hidden.
- New Project: "Custom size (real dimensions)…" with width, height, unit (in/cm/mm/px) and dpi. Saved with the project (`tilePhys`) and used as the default for the high-resolution export.
- Tile popover: "Tile size & dpi…" to change it later.
- Start screen: the app opens on the Projects screen with a "Continue <last project>" card, New project, folders and Import. "Open my last project automatically" is optional (localStorage `sp-autoOpen`).

## v186
- New Project is now a simple setup: name, width × height, units (px/in/cm), DPI (default 3600 × 3600 px at 300), and Repeat preview (Tiled / Single canvas). All size presets are gone, also from the editor's Repeat Layouts panel (which keeps the layouts and a "Tile size & dpi…" button).
- Repeat preview is saved per project. Single canvas darkens the workspace and gives the canvas a frame and shadow so the drawing and export edge is obvious.

## v187
- ⏱ Speed test (More menu, above Memory check): times layer switching, panning frame rate, zoom re-sharpen and the export flatten on the open project, without changing it. Results are shown, can be copied, and the last 6 runs are kept in localStorage 'sp-bench' for comparing versions/devices.

## v188 (superseded by v189)
- Layer picture cache: while the iPad is idle (2.5 s without touching), sleeping layers with many strokes are redrawn in small slices into one scratch canvas and kept as compressed pictures (in memory only). Tapping such a layer decodes the picture instead of replaying all its strokes. Each picture is checked against a signature of the layer's strokes (and any Paint Inside target) and discarded if anything changed. Falls back to the old redraw otherwise. Speed test step 2 now uses this path and reports how many switches came from pictures.

## v189
- Layer picture cache reworked. v188 measured on iPad: only the layer being woken used the picture, but every layer switch still replayed ALL sleeping layers to rebuild the flattened pictures behind/in front of the active layer (that was the 1.8 s). Now each idle-built picture is cropped to its ink box and kept as a small canvas (total capped at 4 full canvases), and both wakeLayer and the flatten step (replayLayerInto) copy it instead of replaying strokes. Used only at normal sharpness (renderScale ≤ 1), and only while the layer's strokes still match (layerSig). Desktop synthetic test (11 layers, 180k points): layer switch 335 ms → 200 ms; diff 0.
- Test hook window.__sketchpadInternals.

## v190
- Projects screen: 💾 Back up all (one file with every project and folder, via Share/Files on iPad) and 📥 Import / restore (a backup file adds its projects as new ones; nothing existing is replaced). A bar reminds you when you have never backed up or the last backup is over 7 days old (localStorage 'sp-lastBackup').

## v191
- Memory check and Speed test now show the Timelapse recorder: ON/off, steps recorded, MB held in memory, and the time one "save step" costs. (The recorder keeps up to 160 MB of event data in memory, which the old estimate did not count — a suspect for slowness/erratic behaviour on big projects.)

## v192
- Own file types: a single project exports as `name.psketch`, a full backup as `pattern-sketch-backup-DATE.psketchbackup`. The contents are still JSON, so older `.sketchpad.json` / `.json` files still import. The import pickers no longer filter by type (iPadOS greys out unknown extensions); files are recognised by their content. Tapping a .psketch file in Files to open the app needs the App Store (native) version.

## v193
- Back up all made sturdier after an iPad "Transaction aborted" failure: saving the open project first is optional (failure no longer stops the backup), each project is read separately and skipped (and listed) if it fails, the file is built one project at a time through a Blob so the iPad never holds all projects as text at once, and any failure now names the step and shows storage used/quota.

## v194
- Timelapse panel: Close is now a big sticky button (also closes on a tap outside the panel or Escape, cancels a running export, and cannot be blocked by a clean-up error). Export progress and messages moved to the top of the panel (they were below the fold on iPad, so a long export looked like nothing was happening). The export loop yields to the UI every frame so the panel stays responsive and Cancel works. When the video is finished a big "⬇️ Save video" button appears, and the save happens inside that fresh tap (before, it tried to save automatically minutes later, which iPad Safari can silently refuse). Export size defaults to 720 on touch devices.

## v195 — Compact icon toolbar + floating panels
- The big sidebar is gone. A 64px icon rail (left) holds Brush, Pen, Eraser, Smudge, Shapes, Area fill, Text, Warp, Select, Colour, Layers, Library (motifs/SVG/background/templates/trace), Brush maker, Repeat layouts, Symmetry, Timelapse. Every old sidebar section is still reachable: the same DOM sections are moved into floating panels (ids/handlers unchanged).
- Tap a tool = select it + open its panel; tap again = close panel, tool stays selected. Press-and-hold (~0.4 s) shows the tool name.
- One panel at a time; Colour and Layers can be pinned (📌) and stay open while others change. Panels drag by their header (transform only, no drawing), dock beside the canvas (dock button), remember position/dock/pin in localStorage `sp-panels-v1`, and are clamped to the canvas area on resize/rotation. View ▾ → "Reset panel positions".
- Row 2 of the top bar keeps brush chip, size, colour, Quick, Dup, Select menu, zoom. Debug hook: `window.__sketchpadPanels`.

## v196
- Zoom and View ▾ are back in the top bar (they only fold into ⋯ More when the bar is too narrow).
- New top-bar pill "🔁 Grid · Tiling On" (or "Single canvas · Tiling Off"); tap opens the Repeat panel, which also shows the same status line at its top.

## v197
- Blend icon added to the left rail (after Select). It opens the existing Blend panel for the selected shape/motifs; with nothing selected it says "Select a shape first".

## v198
- Motif tray ×: asks before removing a motif (warns when copies are placed on the canvas).
- Opening a project keeps a motif even if the device could not decode its picture, so autosave cannot drop it.

## v199
- Earlier Saves → Restore no longer switches the timelapse off (it detached the recorder and never re-attached it, so the panel said "Not recording" and nothing was recorded until the project was reopened). The recording stored for the project is picked up again after a restore.

## v200
- Blend panel: the "Shape morph" tick-box is hidden when the two motifs cannot morph (pictures), so only options that do something are shown.

## v201–v202
- Rail icons reordered by importance: Brush, Pen, Eraser, Colour, Layers, Repeat | Select, Shapes, Fill, Text | Smudge, Warp, Blend | Library, Pattern brush, Symmetry, Timelapse.
- Edit Path on a filled shape keeps it solid in the live preview (it used to show as a plain outline while editing).
- Detail (zoomed-in) picture: safety net so a stuck "busy" flag cannot leave the sharp picture stale (new stroke missing until zoom in/out a few times). Not reproduced in the lab; watchdog redraws after ~1 s.
- Timelapse: new "Zoom in" option (Whole tile / Fit to my drawing / 1.5x / 2x / 3x) for preview and exported video, centred on the finished artwork; the repeat-reveal ending cross-fades back to the whole tile.

## v203
- Timelapse zoom never crops the drawing: 1.5x/2x/3x are limits, the window always keeps the whole finished artwork (+12% margin); placed-motif bounds use their real rotated size.

## v204
- Timelapse zoom 1.5x/2x/3x is now a follow-the-pen camera: the window (tile/zoom) glides to wherever the latest action happened, and the ending pulls back to the whole finished piece. "Fit to my drawing" stays a fixed window around the finished art.

## v205
- Adaptive Colour: new Harmony menu (Vibe mix / Analogous / Monochrome / Complementary). It uses the same vibe saturation/brightness curve and Richness, but places the Secondary/Accent/Accent 2/Filler colours (and the Extra swatches) on neighbouring hues, one hue, or the opposite side of the wheel.

## v206
- Fix: while editing a motif (and with Stroke tools on in Edit mode), selecting a stroke now opens the Selection panel with the stroke tools (colour, size, Edit Path...). The auto-open added in v195 tested the wrong variable and never fired. Verified: without the fix the panel stayed closed, with it it opens.

## v207
- Procreate brush export: the preview thumbnail (QuickLook/Thumbnail.png) now shows ONE stamp instead of three, so the brush list matches what a single tap makes. Re-export the brush set to get the new previews.

## v208
- Procreate brush export: "Made by" field in the Pattern brush panel (remembered on the device, localStorage sp-author). The name is written into every exported brush (Brush.archive authorName, main + reset), so Procreate shows who made the brush/set. Verified by building the archive in node and finding the name in both.

## v209
- Procreate brush export: author Logo and Signature pictures (Pattern brush panel > Motif brush set, below Made by). Stored on the device resized to Procreate sizes (AuthorPicture/AuthorPicture.png 384x384, Signature/SignaturePicture.png 800x240) and written into every exported brush, matching the layout of a real Procreate brush (paths taken from a user-supplied Heart matcha .brush). Test hook window.__sketchpadBrushFiles.

## v210
- Author name is written only into the main Brush.archive (Procreate leaves it empty in Reset/Brush.archive), as seen in a real brush with Made by set.

## v211 — Time-lapse "Show replay frame" guide
- Timelapse panel → **Show replay frame on the canvas** (remembered, `sp-tlGuide`). Draws a thin dashed pink outline + small label showing what the exported video shows. Only visible while recording is on.
- Uses the same framing code as the export (`Framer` in the SPTimelapse IIFE: `fitRect`, `camWindow`, follow-pen camera). `Player.camPath/zoomRect` now use it too, so guide and video cannot disagree.
- Whole tile: the full video square. Fit: bounds of your artwork so far (grows as you draw; the video uses the finished artwork's size). 1.5×/2×/3×: the camera follows the pen, so the frame shows where the camera is after your latest action and moves as you draw; the video zooms back out at the end.
- DOM overlay `#replayGuide` (pointer-events:none, follows pan/zoom/rotate with `#tileOutline`); never drawn into canvases, so not in exports, stamps or video.

## v212 — Trace art sized by the art, not the picture
- Trace Image to Vector → "Size on the canvas": "Fit inside one repeat tile" now sizes by the traced shapes' own bounds (not the source picture's empty margins), so art fills the tile (90%). New option "Fill the whole tile, edge to edge" (100%). "Exactly one repeat tile" is unchanged (needed for seamless tiles).

## v213 — Trace picture: bounding box (move / resize / rotate, then lock)
- Trace Reference → "Trace Artwork": adding a picture now unlocks it and shows a pink box (`#traceBox`, DOM overlay in canvas coords, follows pan/zoom/rotate). Drag the body to move, corners to resize (opposite corner stays fixed), round top handle to rotate (snaps to 0/90/180), "🔒 Lock" chip (or the panel button) locks it; locked = box hidden and drawing works normally.
- Trace pictures now have `rot` (saved in the project, drawn rotated in `drawTraces`). Old "drag the canvas in Edit mode to move" removed. Button reads "🔓 Move & resize".

## v214 — Edit Path: snap to geometry
- Dragging a node in Edit Path snaps to a nearby node of another visible path (green ring, label "Node"; "Join" for the path's own other node) or, failing that, the nearest point along another path (green diamond, "Path"). Radius 16 screen px. Targets collected once per drag; erasers/hidden layers ignored.
- New `🧲 Snap on/off` button in the Edit Path bar (`#pathSnapBtn`, pref `sp-snapGeo`, default on).

## v215 — Snap ignores the path being edited
- Edit Path snap no longer targets the path's own nodes (the confusing "Join" highlight is gone); it snaps only to other paths. Use Close path to join a shape's own ends.

## v216 — "Join" only for the path's other end
- Edit Path snap: "Join" appears only when an END node is dragged onto the path's other END. Middle nodes of the same path never snap or show Join.

## v217 — Eraser: fine spacing for small erasers (bead-chain fix)
- `eraseSweep` spaced its rub-out circles at least 1 unit apart, which for a size-1 eraser equals the circle's own diameter, so zoomed in the erased band looked like a chain of beads / scattered flecks (beta tester report at 3200%). Now step = max(0.12, 0.35·r) for r<6 (was max(1, 0.5·r)); cuts stored to 2 decimals; per-stroke cut cap 1500→4000; sweep cap 64→400 samples. Measured gap for r=0.5: 0.89 → 0.17.

## v218 — "Hard" eraser is now truly hard
- The rub-out punch used a radial gradient even for Hard (fading over the outer 8%), so Hard looked soft on wide strokes. Cuts with h≥0.92 (Hard, and older saved Hard cuts) are now a solid circle: crisp edge, no grey transition (checked: edge samples are pure on/off). Soft/Rough/Like-my-brush unchanged.

## v219 — Brush / eraser size cursor
- A ring the size of the brush (size × zoom, min 6 px; dashed for the eraser) follows the mouse or Pencil (hover where supported, and while drawing) when a drawing brush or the eraser is active in Draw mode. Hidden for finger touches and for Select/Edit, Pen, Shapes, Fill, Smudge, Warp, Edit Path. The OS cursor is hidden while it shows.
- View ▾ → "⭕ Brush cursor: On/Off" (pref `sp-brushCursor`, default on). DOM element `#brushCursor`, never drawn into artwork.

## v220 — Less lag when moving things while zoomed in
- Cause: `drawTiles()` copied all 9 tile repeats of the full 1800×1800 canvas on every `redraw()` (~20 MP/frame) even when only a small part is on screen; moving a stroke redraws every frame. Now, once zoomed past the sharp-detail threshold (`detailNeeded()`), only the on-screen area plus a 50 % margin is copied (`visibleCanvasRect`); `applyTransform` triggers a redraw if the view leaves the drawn area, and zooming out redraws in full. Headless frame time while dragging a stroke at 350 %: ~27 ms → ~16 ms (vsync).
- Dragging a selected stroke also draws it once onto its own sheet and just slides that picture (bounding box only) instead of re-rendering the brush stroke on every pointer event; coalesced to one update per frame.

## v221 — Tiling on/off from the Repeat panel
- The first line of the Repeat & tiling panel (and so the 🔁 pill → panel) is now a button that turns tiling on/off in any project ("… — tap to turn off" / "🔲 Single canvas · Tiling Off — tap to turn on"). The underlying `#tilingBtn` was hidden since v195, so there was no in-app switch.

## v222 — Editing a motif: taps reach the strokes every time
- `selectAtBase` tested placed pictures first, by bounding box. While editing a motif the edited instance (hidden, but still in `placed`) and other pictures still counted, so any tap inside their invisible box selected the motif (box + handles) instead of the stroke, and the stroke panel only opened when a tap happened to land outside it ("works sometimes"). Placed pictures are now skipped while `editingMotifId` is set. Test: 4/4 stroke taps select a stroke inside the motif (before: motif selected instead).

## v223 — Edit Motif panels + deletes
- Selection panel no longer opens on top of the Stroke panel while editing a motif.
- Done now redraws every layer from the remaining strokes before rebuilding the motif picture, so deleted items (text, strokes) don't come back.
- Note: if you delete everything in a motif, the old picture is kept on purpose (safety).

## v224 — hold-to-straighten fixes
- Held line no longer comes out shorter: it ends at the pen tip.
- After the line snaps, keep the pen down and drag: the far end follows the pen exactly and stays straight (no jumping).
- Zooming out of the sharp view always redraws the normal canvas, so strokes can't be left missing until you tap.

## v225 — Edit Path size box
- Jumping from one stroke to another inside Edit Path now refreshes the size, colour and brush boxes to the new stroke (it kept showing the previous stroke's size).

## v226 — moving a stroke while zoomed in
- Zoomed in, dragging a stroke used to leave the original showing under the sharp picture and the moving copy was hidden, so it jumped/lagged. Now the real stroke is hidden and a picture of it slides under the pen (cheap per move), then it is committed on release.
- The sharp picture ignores strokes that are being dragged.

## v227 — duplicate on the same spot
- Duplicating a stroke (or text) now puts the copy exactly on top of the original instead of offset. (Duplicating pictures/groups still offsets.)

## v228 — top-bar size follows the stroke you're editing
- While a stroke is selected (or in Edit Path) the top-bar size box shows that stroke's size and editing it changes that stroke only; your brush size (e.g. 8) is never touched. With nothing selected it shows/edits the brush size as before.

## v229 — size dropdown tick matches the real size
- From a screen recording: the size dropdown (▾ next to the size box) kept its tick on the last size picked (6) even when the box said 8. It now always ticks the real size (panel and top bar), and re-syncs when you switch strokes.

## v230 — opens in Edit
- Opening a project that already has strokes (restart, Continue, Open) now starts in Edit, so tapping a stroke selects it instead of drawing. Tap Draw to draw. "Stay in Draw" (More menu) keeps the old start in Draw. Empty/new projects still start in Draw.

## v231 — Edit Path: tap to add, easier end drags
- In Edit Path (Select tool) tapping the path itself, away from any node, now adds a node there (Add Node still works the same). Tapping a different stroke still switches to it.
- Snapping no longer grabs a node the moment you touch it: it only starts after you have dragged ~14 px, and its pull range is smaller (11 px), so path ends next to another path or their own other end can be dragged freely.

## v232 — snapping back, without sticking
- Snap highlights work again as soon as you drag a node (pull range 15 px). A node that STARTS right next to another path/node stays free until you drag ~26 px away from it, then snapping turns on — so ends can still be picked up and moved.

## v233 — Shape builder panel + Rotate icon
- New rail icon (two overlapping circles) opens a floating **Shape builder** panel: Pick shapes, then Add, Subtract (top shape cuts those below), Intersect, Xor, Divide (every overlap becomes its own piece). Works on closed outline shapes; results are normal editable vector shapes; undo restores the originals. (The old Merge/Subtract/Intersect box is still in the Stroke tools.)
- New rail **Rotate** icon opens the Rotate panel (select a stroke first).
- The Selection panel no longer pops open over the Shape builder while it's open.

## v234 — Rotate panel was hidden
- The Rotate panel was opening underneath the Selection panel. It now sits on top and opens low on the left, clear of the other panels.

## v235 — Rotate icon during Edit Path
- Tapping the Rotate icon while Edit Path is open now finishes Edit Path for you and opens the Rotate & Repeat panel (it used to refuse with a message).

## v236 — linked repeat copies
- Rotate & Repeat → Make copies now creates LINKED copies. Edit the original (reshape in Edit Path, size, colour, brush, rotate, move) and every copy follows around the same centre. Select a copy and it tells you to edit the original.
- Pressing Make copies again REPLACES the earlier copies instead of stacking new ones on top; a copy that would land exactly on the original (a full 360°) is skipped.

## v237 — Easy fill + project palettes
- **Easy fill** block in the Stroke panel, Edit Path panel and Selection panel: Fill On/Off, fill colour, "Same colour as stroke", and a "Palette colour goes to Stroke / Fill / Both" switch. The fill is a linked shape under the outline and follows it when edited, moved, rotated or duplicated.
- **Project palette** (Colour panel): pick the adaptive palette or your own; saved with the project. ＋New, ＋Colour, ✎Edit, Rename, 🗑, and a 📚 Library (kept on the device) to copy palettes between projects.

## v238 — Contour & round corners
- New rail icon + floating panel "Contour & corners". Contour: make 1–12 copies of the selected outline, outside or inside, at a set gap (original kept; open paths work outside). Round corners: rounds sharp corners of a closed shape (optionally the dented ones too), radius slider, undoable.
- Built from PolyBool unions (retry with looser epsilon on tangent edges).
- Not yet reproduced: "sharp tip becomes round when resizing" (geometry scales exactly in tests).

## v239 — Linked contour copies; resize no longer rebuilds a stale shape
- Contour copies are linked to the original (like Rotate & Repeat): the Gap / Copies / Inside-Outside controls update them live while the panel is open, and editing, moving, rotating, resizing or deleting the original makes them follow. "Detach copies" makes them ordinary strokes. Selecting a copy selects its original.
- Resize/rotate: a stroke that still carried an old parametric .shape (e.g. a hold-recognised ellipse later reshaped) was rebuilt from that shape on resize, turning a sharp leaf into an ellipse. The shape is now only used while it still matches the points.

## v240 — Contour thickness option
- Contour panel: "Thickness" slider = size change per copy (default 0 = same as the original and follows it when the original's size changes; + thicker outer rings, − finer inner ones). Copies also follow the original's colour and brush.

## v241 — Contour fixes
- Outside contours no longer produce stray inner rings (holes that appeared where a shape has a narrow gap, e.g. a hook). Only outer boundaries are kept for Outside.
- Inside: if the gap leaves no room, the original's copies are no longer silently wiped; a message says there is no room (or "Only N of M copies fit"). 

## v242 — Contour: Remove copies
- New "Remove copies" button next to "Detach copies" (shown when the selected original has contour copies).

## v243 — Contour is live
- No Make step needed: touching Gap / Copies / Thickness / Inside-Outside on a selected outline makes the copies straight away and updates them as you go. The tool replaces its own set each time, so there are always exactly N copies in the chosen direction. Make / Detach / Remove buttons remain.

## v244 — Duplicate no longer clones contour links
- Duplicating (or pasting) an outline that had contour copies used to clone its contour settings too, so the duplicate sat exactly on top with its own (e.g. old Inside) ring set — looking like extra inside/outside rings. Duplicates now start as plain strokes; pasted copies are re-linked properly or become plain strokes.

## v245 — Contour keeps sharp tips
- Contour copies use mitered (sharp) corners like an offset path in a vector app, so a pointed leaf tip stays pointed in the outer and inner rings. Extremely sharp spikes (beyond a 3.2× miter limit) fall back to a round corner so they don't shoot out. Round-corners tool is unchanged.

## v246 — Contour: "Keep sharp tips" option
- Contour panel has a "Keep sharp tips" tick (default on). On: pointed tips, even very narrow ones (miter limit ~10×), are followed exactly in the outer and inner rings. Off: rounded corners. Status text no longer says "inside" when fewer copies fit.

## v247 — Gradient + Adjust colours
- New **Gradient** rail panel: Flat / Linear / Radial fill for closed shapes (start, optional middle, end colour, project palette strip, angle, radial centre, opacity). Stored on the outline's linked fill, so it moves/resizes/rotates with the shape, follows Edit Path, undoes, and exports to SVG as a real gradient.
- New **Adjust colours** rail panel: Invert, Hue, Saturation, Brightness for Selected / This layer / Everything (gradients included). Sliders snap back after applying; one undo step each.

## v248 — Layer blur
- Adjust panel now has **Blur this layer** (0–80 px) plus Remove blur. It is a layer setting, not baked in: change or remove any time, undo/redo, saved in the project, copied by Duplicate layer.
- Wraps around tile edges when tiling is on (and always in hi-res export) so patterns stay seamless. Shows in screen, zoomed view, PNG and hi-res export; SVG can't hold it.
- Uses the canvas blur filter when available, otherwise a built-in box-blur fallback (for iPads without it).

## v249 — Liquify modes
- Warp is now **Liquify**: Push (as before), **Pinch**, **Bloat**, **Twirl ↻** and **Twirl ↺**. Pinch/Bloat/Twirl work while you press and hold (or drag) with the pen; Size and Strength sliders apply to all.
- Acts on vector points of the active layer; one undo step per press.

## v250 — Clone tool
- New **Clone** tool (rail icon): tap the artwork you want to copy from (on the active layer), then paint where the copy should go. The first stroke fixes the offset; later strokes keep it (aligned). "Move source" picks a new spot. Size, Opacity, Softness sliders.
- Samples a snapshot taken at stroke start, so it never re-copies what it just painted. Stored as a replayed raster step (like Smudge): undo, save, hi-res export all replay it. Copies only the active layer's pixels; the eraser can't rub it out (Undo).

## v251 — Liquify Paint (marbling) + fill on open lines
- Liquify has a **Paint / Lines** switch (Paint is the default). **Paint** moves the actual pixels of the active layer, so neighbouring colours smear and swirl into each other like marbling (Push, Pinch, Bloat, Twirl). Stored as a replayed raster step like Smudge: undo, save and hi-res export match. **Lines** is the old vector behaviour (sharp, editable).
- Fill now works on open lines too (filled as if the ends were joined); the "only closed shapes" block is gone.

## v466 — Motif boxes fit the artwork
- Capture Motif ignores stray specks and faint ghost pixels when working out the box (alpha above 24, tiny far-away clusters dropped).
- New **✂ Trim box to artwork** (selected motif) and **All motifs** in Selected Motif: crops the motif picture and adjusts every placed copy so nothing moves; undoable. Repairs old projects whose motif boxes were much bigger than the art.

## v467 — Watermark logo grid is one row
- In Layers → Motifs, the watermark logo copies show as a single row ("Watermark logo · N copies") with show/hide, one opacity slider and delete for the whole grid, instead of one row per copy. (The copies were already all on the one "Watermark" layer.)

## v468 — Bigger Mix a colour swatch
- The live preview in Colour → Mix a colour is now a full-width 104 px swatch (was a thin strip) with the code under it, and stays at the top while you drag the sliders.

## v469 — Shadows & highlights from extracted colours
- Colour → Palette from an image has a new **🌗 Shadows & highlights** panel: pick how many darker (shadow) and lighter (highlight) tones, the strength, and an optional natural look (shadows lean cooler, highlights lean warmer). Each extracted colour (only the ones you chose, if any) becomes a column from lightest to darkest; tap a shade to use it.
- **Add shades to palette** adds just the new shades to the chosen saved palette; **New palette from all** saves the colours plus their shades.

## v470 — Simpler shades panel
- Shadows & highlights now defaults to 1 highlight + 1 shadow and shows just two tidy rows (lighter, darker), one swatch per extracted colour, instead of a full column per colour. Up to 3 of each if wanted.

## v471 — Fill swatch uses the Colour panel
- The toolbar **Fill** swatch now opens the app's Colour panel (on its Fill tab, with your project palette, Mix and eyedropper) instead of the iPad's own colour picker, same as the Stroke swatch. With a shape selected it changes that shape's fill; with nothing selected it sets the colour of new fills and turns fill on.
- Swatches that name a target (like Fill) keep it when the panel opens, instead of flipping back to Brush.

## v472 — Pen tool: auto-fill + cleaner look
- Closed pen shapes now fill automatically when fill colour = stroke colour (or Auto-fill is on).
- Pen overlay restyled: thin blue 1.25px path with faint width ghost, small square anchors, hollow ring on the first point, slim handles.

## v473/v474 — Inner shadow (v474 moves it into the Stroke panel Fill box)
- New "🌓 Inner shadow" section (above Shape builder): select a filled shape, choose light direction, size, darkness, tap Add shadow.
- Shadow = fill shape minus itself nudged toward the light (PolyBool), so it stays inside the fill; inserted straight above the fill and under the outline line. Strokes carry `shadowOf`; deleted with their shape, Remove button clears it.

## v475 — Inner shadow guard
- Add shadow on a plain outline (no fill) now explains to pick the coloured fill shape instead of painting a black blob.

## v476 — Tap a layer to select its shape
- Tapping a layer row (outside the name, thumbnail and buttons) now also selects the topmost shape on that layer, which opens the Stroke panel (works inside Edit Motif, so Fill layers can be picked for Inner shadow).

## v477 — Inner shadow works from the outline
- With a plain outline selected (Fill off), Add shadow finds the largest colour fill around the outline's centre and shades that, placed above the fill and under the outline.

## v478 — Shadow/highlight on their own layers
- Add shadow now creates a "Shadow" layer directly above the fill's layer (own opacity, blur, blend), made of normal editable closed paths (nodes). New ✨ Add highlight does the same on a "Highlight" layer on the light side (lightened fill colour). Remove clears both.

## v479 — Layer tap steps through pieces
- Tapping a layer selects its biggest shape first; tapping the same layer again selects the next piece (status shows "Piece n of m"). Lets you reach each part of a multi-piece Shadow/Highlight layer.

## v480 — One layer per shadow/highlight piece
- If a shadow or highlight comes out as several separate pieces, each piece now gets its own layer (Shadow, Shadow 2…; biggest first), stacked above the fill's layer.

## v481 — Pick the colour to shade
- Inner shadow section: "🎯 Pick the colour to shade". Next canvas tap selects the colour fill under the finger (skips outlines/face lines on top), then Add shadow / Add highlight.

## v482 — Tidy fills and layers
- Empty Fill / Shadow / Highlight layers are removed automatically when their last shape is deleted (Area Fill layers are now auto layers).
- Layers panel: "🧹 Remove duplicate fills" deletes identical stacked colour fills and the empty layers they leave.
- Selecting a shape scrolls its layer into view in the Layers panel.
- Test hook `__sketchpadShadow`.

## v483 — Separate delete buttons, Stroke panel reliability
- Inner shadow section: "✖ Delete shadow" and "✖ Delete highlight" are separate buttons.
- Tapping a layer row while Edit Path is open now finishes Edit Path first, so the Stroke panel is not left hidden.
