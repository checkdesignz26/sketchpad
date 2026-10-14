#!/usr/bin/env bash
# Run AFTER `npx cap add ios` (macOS only: uses PlistBuddy). Safe to re-run.
# Makes the app iPad-only and lets people reach saved files from the Files app.
set -euo pipefail

PLIST="ios/App/App/Info.plist"
PBX="ios/App/App.xcodeproj/project.pbxproj"
PB=/usr/libexec/PlistBuddy

[ -f "$PLIST" ] || { echo "Run 'npx cap add ios' first ($PLIST not found)"; exit 1; }

set_key() { # key type value
  "$PB" -c "Delete :$1" "$PLIST" 2>/dev/null || true
  "$PB" -c "Add :$1 $2 $3" "$PLIST"
}

set_key CFBundleDisplayName string "Pattern Sketch"
set_key UIFileSharingEnabled bool true
set_key LSSupportsOpeningDocumentsInPlace bool true
set_key ITSAppUsesNonExemptEncryption bool false
set_key UIRequiresFullScreen bool false
set_key UIStatusBarHidden bool true
set_key UIViewControllerBasedStatusBarAppearance bool false

# iPad orientations (all four)
"$PB" -c "Delete :UISupportedInterfaceOrientations~ipad" "$PLIST" 2>/dev/null || true
"$PB" -c "Add :UISupportedInterfaceOrientations~ipad array" "$PLIST"
i=0
for o in UIInterfaceOrientationPortrait UIInterfaceOrientationPortraitUpsideDown \
         UIInterfaceOrientationLandscapeLeft UIInterfaceOrientationLandscapeRight; do
  "$PB" -c "Add :UISupportedInterfaceOrientations~ipad:$i string $o" "$PLIST"; i=$((i+1))
done

# iPad only (2 = iPad, 1 = iPhone)
sed -i.bak 's/TARGETED_DEVICE_FAMILY = "1,2";/TARGETED_DEVICE_FAMILY = 2;/g; s/TARGETED_DEVICE_FAMILY = 1;/TARGETED_DEVICE_FAMILY = 2;/g' "$PBX"
rm -f "$PBX.bak"

echo "iOS project configured for iPad."
