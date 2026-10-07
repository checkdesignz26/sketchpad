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
