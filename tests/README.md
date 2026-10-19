# Pattern Sketch browser tests (Playwright, headless Chromium)

Serve this folder's parent (`python3 -m http.server 8790`) then, from `tests/`, run each file with `python3 <file>`.
They draw with real mouse events and read canvas geometry through `window.__sketchpadGetState()` / `__sketchpadInternals()`.

- test_flower_undo_save.py: teardrop -> Edit Path -> 6 linked petals -> edit source -> undo/redo -> reload -> edit again (copies must follow every time)
- test_repeat_counts_live.py: 3/4/5/6/8/12 copies (total includes the original), copies follow a node while it is still being dragged
- test_live_count.py: +/- and typed count change a live flower (7=51.43°, custom angle kept, panel open during Edit Path, undo/redo, reload)
- test_linked_fill.py: Fill on/off, colour, node drag, count change and reload across 6-8 linked petals
- test_pivot_drag.py: drag the centre marker, copies turn about the new centre live, undo restores it
- test_stroke_width_state.py: size box follows the selected stroke, mixed selections show "mixed", the drawing tool width is never overwritten by editing a stroke

## Tiled export (v322)
- `test_tiled_export.py`: every layout (Grid / Half Drop / Half Brick) at 1×1, 2×2, 3×3 is compared pixel by pixel with the lattice rule built from the seamless tile; checks transparency and the size limits.
- `test_tiled_export_ui.py`: Export menu → Tiled export → Save through the real buttons; PNG validity (IDAT inflates to the right size), project untouched, 49 MP save, large-size warning, plain exports still work.

## Canvas Tiling (v323)
`tests/test_canvas_tiling.py` checks 1×1 / 2×2 / 3×3 pattern scale on Grid, Half Drop and Half Brick: the strokes never change, drawing inside a small copy lands in the source tile, and "Save canvas as shown" keeps the tile size. `tests/test_tile_preview.py` covers the live Tiled Export preview.

`tests/test_save_tiled_pattern.py` (v324): Save as New Pattern adds exactly one filmstrip entry with independent editable vectors (Grid, Half Drop, Half Brick counted), leaves the original untouched, and edits in either pattern stay in that pattern.

`tests/test_rotate_group.py` (v326): Make copies groups the flower; tap = whole flower, double-tap = one petal (no accidental duplicate); ungroup keeps the repeat links, Unlink repeats keeps the group; Duplicate makes a new group with its own links; other groups untouched. Older flower tests now use `common.pick_petal()` (double-tap) because a tap on a grouped flower selects the whole flower.
