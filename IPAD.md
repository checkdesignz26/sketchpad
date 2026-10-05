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
