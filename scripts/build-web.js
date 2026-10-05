#!/usr/bin/env node
/* Copies the web app into ./www so Capacitor can bundle it.
 * index.html and its scripts stay the single source of truth; the browser and suite versions
 * keep running straight from the repo root exactly as before. */
const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const out = path.join(root, 'www');

// Files the app needs at runtime. Add new scripts/assets here.
const files = ['index.html', 'brush-engine.js', 'polybool.min.js', 'native-bridge.js'];

fs.rmSync(out, { recursive: true, force: true });
fs.mkdirSync(out, { recursive: true });

for (const f of files) {
  const src = path.join(root, f);
  if (!fs.existsSync(src)) {
    console.error('Missing required file: ' + f);
    process.exit(1);
  }
  fs.copyFileSync(src, path.join(out, f));
}

// Offline check: every local <script src> in index.html must be bundled, and nothing may
// load from the network.
const html = fs
  .readFileSync(path.join(out, 'index.html'), 'utf8')
  .replace(/<script(?![^>]*\bsrc=)[^>]*>[\s\S]*?<\/script>/gi, '') // ignore inline JS bodies
  .replace(/<!--[\s\S]*?-->/g, '');
const refs = [...html.matchAll(/<(?:script|link|img)[^>]+(?:src|href)=["']([^"']+)["']/gi)].map(m => m[1]);
let bad = 0;
for (const r of refs) {
  if (/^(data:|#)/.test(r)) continue;
  if (/^https?:\/\//i.test(r)) { console.error('Network resource (breaks offline): ' + r); bad++; continue; }
  if (!fs.existsSync(path.join(out, r))) { console.error('Referenced but not bundled: ' + r); bad++; }
}
if (bad) process.exit(1);

console.log('www/ ready: ' + files.join(', '));
