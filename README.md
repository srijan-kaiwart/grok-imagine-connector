# Grok Imagine Connector

Generate images and videos on [grok.com/imagine](https://grok.com/imagine) in
batches — from a Chrome side panel, or from your AI coding agent.

Everything runs in **your own browser, on your own Grok session**. No API keys,
no accounts, no daily limits, no cost.

---

## What this repo is

The **agent skill** and **docs**. The two things you install are:

| Piece | Where it comes from |
|---|---|
| Chrome extension | [Chrome Web Store](#) *(link once published)* |
| `grok-auto` CLI + local bridge | npm — `npm install -g grok-imagine-connector` |
| Agent skill | this repo → [`skills/grok-generate/`](skills/grok-generate/) |

The extension works on its own — the CLI and skill are only needed if you want
to drive generation from an AI coding agent (Claude Code, Codex, and others).

## Setup

### The easy way — let your agent do it

Open the extension's **Connect** tab and copy the setup prompt, then paste it
into your coding agent. It installs the CLI, fetches this skill, and verifies
the connection.

### Manually

```bash
npm install -g grok-imagine-connector
grok-auto --version
```

Then copy [`skills/grok-generate/`](skills/grok-generate/) into your agent's
skills directory:

- **Claude Code** → `~/.claude/skills/grok-generate/`
- other agents → the equivalent skills/tools directory

Check it worked:

```bash
grok-auto status     # expect: extension: connected
```

## Requirements — read this one

The tool has no API. It drives the **real grok.com interface** in your browser.
A `grok.com/imagine` tab must be:

- **open**, and
- **logged in**, and
- **visible on screen** — not minimised, not fully covered by another window.

That last point is the one people miss, and it is not optional: Chrome throttles
timers and rendering in hidden tabs, so a covered window makes generation stall
rather than run slowly. Chrome on a second monitor, or side-by-side with your
editor, is the setup that works.

## Usage

Once installed, just ask your agent:

> generate an image of a red fox in snow with grok

Or use the CLI directly:

```bash
grok-auto generate create text-to-image --prompt "a red fox in snow" --wait
grok-auto generate create text-to-video --prompt "waves at sunset" --duration 10 --wait --wait-timeout 20
```

Modes: `text-to-image`, `image-to-image`, `text-to-video`, `frame-to-video`,
`ingredients-to-video`.

## Privacy

Nothing leaves your machine. No analytics, no telemetry, no server of ours.
Full policy: [`docs/privacy.md`](docs/privacy.md).

## Support

Something broken? grok.com changes its interface often, and that is usually the
cause. [Open an issue](../../issues) — include what mode you ran and what the
Debug Logs tab showed.

## Free, and staying free

Every feature is available to everyone. There is no paid tier and donating
unlocks nothing. If it saved you time, a tip is welcome and entirely optional.

---

Not affiliated with, endorsed by, or sponsored by xAI or Grok. Automating a
website may be subject to that site's terms of service; use responsibly and at
your own discretion.
