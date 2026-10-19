# Pattern Sketch browser tests (Playwright, headless Chromium)

Serve this folder's parent (`python3 -m http.server 8790`) then, from `tests/`, run each file with `python3 <file>`.
They draw with real mouse events and read canvas geometry through `window.__sketchpadGetState()` / `__sketchpadInternals()`.

- test_flower_undo_save.py: teardrop -> Edit Path -> 6 linked petals -> edit source -> undo/redo -> reload -> edit again (copies must follow every time)
- test_repeat_counts_live.py: 3/4/5/6/8/12 copies (total includes the original), copies follow a node while it is still being dragged
- test_live_count.py: +/- and typed count change a live flower (7=51.43°, custom angle kept, panel open during Edit Path, undo/redo, reload)
- test_linked_fill.py: Fill on/off, colour, node drag, count change and reload across 6-8 linked petals
- test_pivot_drag.py: drag the centre marker, copies turn about the new centre live, undo restores it
- test_stroke_width_state.py: size box follows the selected stroke, mixed selections show "mixed", the drawing tool width is never overwritten by editing a stroke
