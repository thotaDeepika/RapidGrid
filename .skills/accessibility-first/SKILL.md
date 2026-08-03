---
name: accessibility-first
description: >
  Apply accessibility requirements whenever building or reviewing any
  GeoAgentic citizen-facing surface — the Citizen App, SOS flow,
  emergency-reporting forms, or the Accessibility Agent itself. Use this
  skill for ANY UI work on GeoAgentic, not just screens explicitly labeled
  "accessibility" — accessibility is one of the project's core
  differentiators and must be the default, not an opt-in layer. Trigger
  on mentions of citizen app, SOS button, emergency reporting UI, voice
  input, sign language, screen reader, or "make it accessible."
---

# GeoAgentic — Accessibility-First Interface

Accessibility is a named differentiator for this project (see
`geoagentic-architecture` SKILL.md), not a nice-to-have. Every citizen
app screen and the Accessibility Agent's flows must satisfy these
requirements by default.

## Requirements checklist (apply to every citizen-facing screen)

- Keyboard-only navigation works end-to-end (no mouse-only interactions).
- All interactive elements have screen-reader labels (not just visible
  text — icon-only buttons especially).
- High-contrast interface available; never rely on color alone to convey
  status (pair color with an icon or text label).
- Large emergency buttons — SOS and "raise emergency" must be reachable
  in as few taps/steps as possible; treat step count as a metric to
  minimize, not just a UX nicety.
- Voice-based reporting, with a text alternative always available for
  users who can't or don't want to speak.
- Visual **and** vibration/haptic alerts, so status changes reach deaf
  users and users in loud/silent-required environments.
- Multilingual emergency prompts — don't hardcode English-only strings in
  emergency-critical paths.
- No color-only status indicators anywhere (routes, hospital status,
  dispatch status).

## Accessibility Agent input modalities

The Accessibility Agent must normalise all of these into the same
downstream incident-report shape (see
`geoagentic-architecture/references/agent-contracts.md`):

1. Voice (speech-to-text via Whisper)
2. Sign-language input (video → avatar/interpretation pipeline, or at
   minimum a structured sign/symbol picker if full sign recognition is
   out of scope for a hackathon build — be explicit in the demo about
   which level you actually implemented)
3. Text / symbols (icon-based reporting for users who can't read/type
   fluently, or for young/elderly users)
4. One-tap SOS (minimal-step, pre-filled with device location)

## Minimal-step SOS flow (reference target)

1. Tap SOS button (always visible, large, high-contrast).
2. Location auto-captured (no manual entry required).
3. One follow-up screen: emergency type (icon grid, not free text) —
   optional, auto-times-out and submits as "unspecified/general" if the
   citizen can't complete it.
4. Confirmation with clear visual + haptic feedback that help is coming.

If you're implementing a hackathon-scope demo rather than the full
pipeline, it's fine to mock the sign-language recognition step — but
say so explicitly in the "How You Built It" narrative and keep the
*input contract* consistent so it's a drop-in replacement later, not a
divergent code path (see `geoagentic-testing` Scenario 6 for the test
case this should satisfy).

## What NOT to do

- Don't build an "accessible mode" as a separate, secondary flow from the
  main citizen app — these requirements apply to the default flow.
- Don't gate accessibility features behind a settings toggle the citizen
  has to find during an emergency.
- Don't let a demo's time pressure drop the text alternative to voice, or
  the visual alternative to sound/vibration — pairs, not either/or.
