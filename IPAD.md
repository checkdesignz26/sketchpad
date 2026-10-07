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
- **Steady zoom.** Pinch is anchored between your fingers; the +/- buttons zoom about the centre of the workspace.
- **View recovery.** Tap the zoom percentage (e.g. `100% ▾`): **100%**, **Fit to View**, **Reset View** (also resets rotation).
  These work even if the canvas is completely off-screen.
- **Stroke panel** only opens when you tap **🖊️ Stroke tools**; open/closed is remembered. Selecting a stroke in Edit mode
  also shows a small bar on the canvas with a one-tap **Edit Path** button.
- **Safe areas.** Toolbar sits below the iPad status bar in Safari and the installed app, portrait and landscape.

## Drawing, brushes and saving (features added for the app)

- **Smooth Pen** is a true monoline vector path (default 3 px) with smooth edges at any zoom.
- **On-canvas handles.** A selected stroke shows three handles: the round one at the top turns it (drag, or tap for a 45 degree step: 45, 90, 135, 180...; dragging turns in controlled 15 degree steps with the angle shown, and the box turns with it), the square one at the corner resizes it (drag, or tap for 25% bigger), and the colour dot at the top-left changes its colour.
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

## Before submitting to the App Store

- App icon (1024x1024 PNG, no transparency) and iPad screenshots (13-inch iPad: 2064x2752 or 2752x2064).
- Privacy policy URL. The app stores everything on-device, so the privacy answers are simple.
- App name, subtitle, description, keywords, category (Graphics and Design), price.
- Apple reviews for Guideline 4.2 (apps must be more than a website). Pencil pressure, offline
  drawing, autosave, and the share sheet all help. In the review notes, mention Apple Pencil support
  and that everything works offline.

## Local web preview

Open `index.html` in a browser, as before. To check the offline bundle: `npm run build:web`.
