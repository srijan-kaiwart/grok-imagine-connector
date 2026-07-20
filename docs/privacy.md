# Privacy Policy — Grok Imagine Connector

_Last updated: 2026-07-20_

Grok Imagine Connector ("the extension") automates image and video generation on
**grok.com/imagine** using the Grok session you are already logged into. This
policy describes every piece of data the extension touches.

## Short version

The extension runs **entirely on your computer**. It collects nothing, transmits
nothing to us, and contains no analytics or tracking of any kind. We operate no
server that receives your data, because there is no such server.

We cannot see how you use the extension. The only numbers we ever see are the
aggregate install and active-user counts that the Chrome Web Store shows every
developer, and those come from Google — never from the extension.

## What is stored, and where

All of the following lives **locally** in your browser (`chrome.storage`) and
never leaves your machine:

- **Settings** — generation preferences (mode, aspect ratio, resolution,
  concurrency, download folder).
- **Prompt queue** — the prompts you enter and each job's status.
- **Reference images** — any images you add for use as generation inputs.
- **Debug log** — a rolling local log for diagnosing problems. It records
  request metadata (method, URL, status, timing) for grok.com, and request or
  response bodies **only for grok's generation endpoints**. Ordinary grok.com
  traffic, including your chats, is never recorded with its contents. You can
  clear this log at any time from the Debug Logs tab.

Generated images and videos are saved to **your own Downloads folder** by
Chrome's download manager.

## Your Grok account

The extension uses the Grok session **you are already logged into**. It never
asks for, stores, or transmits your Grok (or any other) username, password,
cookies, or tokens, and it never logs request headers, which can carry
authentication material. It drives the grok.com interface the same way you would
by hand.

## Network activity

The extension makes only these kinds of network requests:

1. **grok.com and its media hosts** (`assets.grok.com`, `imagine-public.x.ai`) —
   the same servers your browser already contacts when you use Grok — to submit
   prompts and retrieve the results. Your prompts go to Grok because that is
   what generates the media; they are subject to xAI's own privacy policy.
2. **A selector-configuration file** from the developer's static host. grok.com
   changes its interface frequently, which breaks automation; this small file
   lets those breakages be fixed without waiting for a Chrome Web Store update.
   The request downloads configuration only. It sends **no personal data, no
   prompts, and no identifiers** — it is an ordinary file download, and we
   cannot distinguish one user's request from another's beyond the IP address
   that any web request necessarily carries.
3. **An optional local bridge** on `127.0.0.1` (loopback — your own machine),
   used when you drive the extension from a CLI or an AI coding agent. It is
   reachable only by programs already running on your computer, accepts
   connections only from the extension itself and local tools, and sends nothing
   to the internet. It is inactive unless you install and start it.

## Donations

The Support tab links to an external donation page (Ko-fi). Following that link
takes you to Ko-fi, whose own privacy policy then applies. The extension itself
processes no payments and receives no information about whether you donated.

**Donating does not unlock anything.** Every feature is free and unlimited for
everyone, with or without a donation.

## What the extension does NOT do

- No analytics, telemetry, or usage reporting.
- No advertising, profiling, or fingerprinting.
- No selling or sharing of data with anyone.
- No access to any site other than grok.com and its media hosts.
- No daily limits, accounts, or license checks.

## Permissions

Each permission exists solely to deliver the extension's single purpose
(automating grok.com/imagine). The store listing explains each one individually.

## Changes

Any change affecting data handling will be published here before it ships. If a
future version ever collects anything, it will be opt-in and disclosed in the
Chrome Web Store data-usage section.

## Contact

Questions, bug reports, or privacy concerns:
https://github.com/srijan-kaiwart/grok-imagine-connector/issues

## Disclaimer

Not affiliated with, endorsed by, or sponsored by xAI or Grok. Automating a
website may be subject to that site's terms of service; use responsibly.
