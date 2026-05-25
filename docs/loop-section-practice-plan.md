# Loop + Section Practice — Implementation Plan (V1.1+)

**Prerequisite:** V1 realtime slowdown is locked (`v1-realtime-practice-engine`).
Do not change SoundTouch profile, bridge, or preset/snap UX while executing this plan.

## Goal

Make repetition practice **fast, obvious, and addictive** — loop a hard phrase, drill it at practice speed, and return tomorrow without re-marking the song.

## What already exists (build on this)

| Area | Location | Notes |
|------|----------|-------|
| A/B loop state | `static/app.js` — `loopA`, `loopB`, `setLoop`, `clearLoop` | Seek-serialized `setLoop(a,b)` |
| Loop wrap + count-in | `app.js` tick / `startCountIn` | Wrap at B retriggers count-in |
| Saved loops API | `/api/loops`, `loadSavedLoops()` | Per-song named loops |
| Player API | `window.slopsmith.setLoop` / `getLoop` | Plugin-safe |
| Practice speed | `slopsmithPlayback.speed` | Locked V1 presets + snap |

## Gaps (priority order)

### Phase 1 — Loop markers & visibility

1. **Timeline markers** — draggable A/B on scrubber or highway ruler (not only “set at playhead”).
2. **Marker affordances** — keyboard shortcuts (e.g. `[` / `]` or `,` / `.`), double-tap A/B on mobile-friendly targets.
3. **Loop-active chrome** — highlight loop region on progress bar; show duration and current pass count.

### Phase 2 — Section practice workflow

1. **“Practice this section”** — one action: set A/B from selection or measure range (future: RS phrase boundaries).
2. **Auto slow on loop** — optional: when loop arms, apply last-used practice preset (70–80% sweet spot).
3. **Fast replay** — instant jump to A on button / shortcut without full stop-start.

### Phase 3 — Saved practice sections

1. Evolve saved loops → **practice sections** (name, speed, count-in bars, arrangement id).
2. **localStorage + server** — keep `/api/loops`; extend schema or add `/api/sections`.
3. **Recall on song open** — “Resume last section” chip in transport.

### Phase 4 — Count-in improvements

1. Configurable bars (1–4), click vs silent, respect loop boundary.
2. **Loop wrap count-in** — don’t full-stop; pre-roll only when crossing B→A.
3. JUCE path: ensure count-in uses same clock as `_audioSeek` / loop wrap.

### Phase 5 — Transport & highway polish

1. Bigger loop controls in `#player-controls`; reduce clutter.
2. Highway: optional loop band tint (read-only from `getLoop()`).
3. Note visibility in loop window (dim outside A–B).

## Architecture constraints (do not violate)

- No SoundTouch / `BackingTimeStretch` changes.
- No Electron IPC redesign; reuse `slopsmith` seek/play APIs.
- No JUCE transport rewrite; seek via existing `_audioSeek` / JUCE shim.
- Speed: call `setSpeed` / `slopsmithPlayback.speed.setRate` only.

## Suggested module boundary

```js
window.slopsmithPractice = {
  loop: { get, set, clear, markers },      // wraps existing loop API
  section: { save, load, list, recall },   // extends saved loops
  countIn: { bars, enabled, onWrap },
  transport: { replaySection, jumpToA },
};
```

## Success metrics

- Set A/B and hear loop in **&lt; 3 seconds** from first play.
- Save and reload section in **one click** next session.
- Loop wrap + count-in feels **continuous** (no audible full stop at B).

## Milestone target

Tag candidate: **`v1.1-loop-section-practice`** after Phase 1–2 shippable in desktop + web player.
