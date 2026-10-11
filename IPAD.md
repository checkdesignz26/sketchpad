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
