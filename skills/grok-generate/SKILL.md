---
version: 0.1.0
name: grok-generate
description: |
  Generate images/videos for free via Grok Imagine (grok.com/imagine)
  using the user's own browser session — no API cost. Wraps the
  `grok-auto` CLI which drives the Grok Imagine Connector
  Chrome extension.
  Use when: "generate an image with grok", "make a video with grok",
  "batch generate", "animate this image", "image-to-image on grok",
  "make a longer video / extend", "storyboard video", "merge/stitch
  clips into one", or when the user wants free/unlimited generation
  instead of paid APIs. Modes: text-to-image, image-to-image,
  text-to-video, frame-to-video, ingredients-to-video; plus
  auto-extend (longer clips), merge (montage via ffmpeg), and
  clean (remove the Grok corner mark from your own generations —
  also "remove watermark", "clean this reference image").
  NOT for: Grok chat/text tasks, paid API generation (use
  higgsfield-generate for Higgsfield models).
argument-hint: "[prompt] [--mode <mode>] [--image <path>]"
allowed-tools: Bash
---

# Grok Generate

Submit generation jobs to grok.com/imagine through the Grok Imagine Connector extension. Everything runs in the user's own logged-in browser — zero API cost, real files land in the Downloads folder.

## Step 0 — Bootstrap

Before any generation:

1. Run `grok-auto status`. The bridge daemon auto-starts on first use; you never start it manually.
2. If it prints `extension: NOT CONNECTED` — walk the user through the **Browser requirement** below, wait for their confirmation, then re-check.
3. If a job fails with `not logged in` — ask the user to log in to grok.com in that Chrome window and confirm.

## Browser requirement — state this clearly, don't assume it

This tool has no API. It drives the **real grok.com interface** in the user's
own Chrome. Generation therefore needs a `grok.com/imagine` tab that is:

- **open**, and
- **logged in**, and
- **visible on screen** — not minimised, not fully covered by another window,
  not in a collapsed window.

That last one is the requirement users miss, and it is not optional: Chrome
throttles timers and rendering in hidden tabs, so a covered window makes
generation stall or fail rather than run slowly.

Practical setups that work: Chrome on a second monitor, or Chrome side-by-side
with the user's editor. Tell them this in plain words the first time, and again
any time the symptom below appears.

**Whenever `NOT CONNECTED`, a timeout, or a stall occurs — stop and instruct the
user.** Never retry silently, and never assume the window is visible because it
was earlier. Say something like:

> Open https://grok.com/imagine in Chrome, log in, and keep that window visible
> beside this one — don't minimise it or cover it while it generates.

Then wait for their confirmation before re-running.

## UX Rules

1. Be concise. No raw JSON or job ids in chat. Deliver the local file path(s) plus a one-line summary (mode, duration for video).
2. Don't narrate internals ("connecting to bridge", "polling job").
3. Detect the user's language and reply in it; technical flags stay English.
4. Always pass `--wait` so the command blocks and prints file paths itself.
5. Videos take 1–5 minutes; images ~10–60s. Use `--wait-timeout 20` for videos.
6. Generation is uncapped — never tell the user they have a daily quota.

## Mode selection

| Task | Mode | Required flags |
|---|---|---|
| Image from text | `text-to-image` | `--prompt` |
| Restyle/remix an image | `image-to-image` | `--prompt --image <path>` |
| Video from text | `text-to-video` | `--prompt [--duration 6\|10\|15]` |
| Animate a still frame | `frame-to-video` | `--prompt --image <path> [--duration]` |
| Video from reference images | `ingredients-to-video` | `--prompt --image <p1> --image <p2> ... [--duration]` |

## Commands

```bash
grok-auto status
grok-auto modes
grok-auto generate create text-to-image --prompt "a red fox in snow, cinematic" --aspect-ratio 16:9 --wait
grok-auto generate create image-to-image --prompt "make it watercolor" --image ./photo.png --wait
grok-auto generate create text-to-video --prompt "camera dollies through a neon market" --duration 10 --wait --wait-timeout 20
grok-auto generate create frame-to-video --prompt "she turns and smiles" --image ./frame.png --duration 6 --wait --wait-timeout 20
grok-auto generate list          # recent jobs
grok-auto generate get <id>      # one job
```

Useful flags: `--aspect-ratio 16:9|9:16`, `--model quality|speed` (images), `--outputs N` (repeat count), `--folder <name>` (Downloads subfolder), `--json` (machine-readable).

Stdin prompt works: `echo "prompt" | grok-auto generate create text-to-image --wait`.

On success the command prints absolute file paths of the downloaded media — deliver those to the user.

## Auto-extend (longer videos)

Any video mode chains grok's native extend to make a longer, continuous clip. Each extension adds ~6s and only the FINAL stitched video is downloaded.

```bash
# 6s base + 2 extensions = ~18s, same prompt each beat
grok-auto generate create text-to-video --prompt "a paper boat down a rain gutter" \
  --extend 2 --wait --wait-timeout 25
# different prompt for the extensions
grok-auto generate create text-to-video --prompt "..." --extend 2 --extend-prompt "it speeds up" --wait
```

- `--extend N` = number of +6s extensions after the base. Videos take longer (~2–4 min per beat) — bump `--wait-timeout`.
- **grok caps one continuously-extended video at ~30s** (≈5×6s beats). For longer, generate separate clips and `merge` them (below).
- `--extend-prompt` is optional: without it every beat reuses the base prompt; with it, all extensions use that prompt instead.
- Extend is CLI/agent-only — the extension's side panel deliberately doesn't expose it, so don't tell the user to look for it there.

## Merge separate videos

Concatenate independent clips (a montage — different scenes, not a continuous story) into one file with ffmpeg:

```bash
grok-auto merge "clip1.mp4" "clip2.mp4" "clip3.mp4" -o "montage.mp4"
```

- Re-encodes by default so mixed resolutions (480p + 720p) merge cleanly with exact duration + A/V sync. `--fast` stream-copies (quicker, but may drift the total duration).
- Needs ffmpeg installed (`winget install Gyan.FFmpeg`, or set `FFMPEG_PATH`). Use extend (above) for a continuous shot; use merge for stitching unrelated clips.
- **No limit** on clip count or total length (unlike grok's 30s extend cap) — this is how you build videos longer than 30s: make several ≤30s clips, then merge.

## Remove the Grok mark

Grok stamps a semi-transparent mark in the bottom-right corner. `clean` removes it from images and videos:

```bash
grok-auto clean in.mp4  -o out.mp4                          # crop (default)
grok-auto clean in.png  -o out.png  --mode delogo
grok-auto clean in.mp4  -o out.mp4  --mode cover --logo my_logo.png
```

| Mode | What it does | Cost |
|---|---|---|
| `crop` | Largest same-aspect window excluding the mark, rescaled to the original size | ~12% zoom, no artifacts |
| `delogo` | Interpolates over the box, full frame kept | faint blur patch |
| `cover` | Overlays your own logo on the mark | none (rebrands it) |

### Which approach, by aspect ratio

The mark is ~17% of frame WIDTH, so what a crop costs depends entirely on the
shape of the frame. These figures were measured, not estimated:

| Case | Do this | Cost |
|---|---|---|
| **9:16 (vertical)** | `clean --cut bottom` | **~3.8%** — effectively free, no planning needed |
| **16:9, not generated yet** | reserve an empty bottom band in the prompt, then `--cut bottom` | **zero** — see recipe below |
| **16:9, already generated** | `--cut bottom`, or `--mode cover` to brand it | ~12.8% of the framing |
| **Stills** | same as above | crop only |

`--cut auto` (the default) already picks `bottom` for both 16:9 and 9:16, so
plain `grok-auto clean in.mp4 -o out.mp4` is usually right.

**The 16:9 reservation recipe — this is the one worth using.** Because the mark
always lands bottom-right, a shot composed with an empty bottom band loses
nothing when that band is cropped away. Add to the prompt:

> …all subjects kept in the upper two thirds of the frame, a large empty
> ground/road filling the entire bottom quarter, nothing near the bottom edge

then run `clean --cut bottom`. The mark sits on the empty band; the crop removes
only that band. Prompt for this whenever the user asks for 16:9 output they
intend to publish.

### Rules

- **Clean reference images BEFORE reusing them.** When a marked image is fed into `frame-to-video` or `ingredients-to-video`, grok paints the mark INTO the new scene — it is no longer an overlay and cannot be removed afterwards. Cleaning the reference first is the only fix, so do it automatically whenever a generated image becomes an input.
- **Never use `delogo` for a final.** It leaves a visible blur band on any busy corner. It is a draft/preview mode only, fine on plain moving backgrounds.
- `--cut` alternatives when `bottom` crops something important: `right`, `center` (subject stays centred), `topleft` (preserves the left edge — good when the subject sits left of centre).
- Needs ffmpeg. Dimensions are always preserved.
- Seamless erase (AI inpainting) is not available here — it needs a Python toolchain with model weights. Crop is the artifact-free option in this package; don't claim an inpaint mode exists.
- Only use this on generations the user made themselves. Don't offer it for other people's content, and don't imply it changes anything about disclosing that media is AI-generated.

## Errors

- `extension: NOT CONNECTED` → ask user to open Chrome with the extension + grok.com/imagine tab.
- `not logged in to grok.com` → ask user to log in, then retry once.
- `moderation: ...` → the prompt was content-blocked; suggest a reworded prompt. Not retryable as-is.
- `generation timed out` / `SELECTOR_TIMEOUT:*` → grok.com UI may have changed or is slow. Suggest the user run the Selector Healthcheck from the extension's Debug Logs tab; retry once.
- `bridge not running and no spawnArgs given` → run any `grok-auto generate ...` command, which auto-starts the daemon.
