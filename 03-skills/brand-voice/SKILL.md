---
name: brand-voice
description: >-
  Enforce our developer-first brand voice, technical terminology, and clear formatting across
  release notes, changelogs, error messages, UI microcopy, and public documentation. Use when
  the user asks to write or edit customer-facing copy, release notes, CLI/UI messages, or
  invokes /brand-voice.
---

# Developer-First Brand Voice & Terminology (`brand-voice`)

Use this skill whenever drafting or editing public-facing documentation, changelogs, CLI output, error messages, or UI copy.

---

## 1. Core Voice Pillars

| Pillar | What It Means in Practice | What It Is NOT |
| :--- | :--- | :--- |
| **1. Practitioner-Direct** | Write from one senior engineer to another. Lead with the technical mechanism, exact flag, or breaking change in sentence one. | Corporate PR fluff, passive voice, or burying the lede in paragraph three. |
| **2. Empathetic & Actionable** | Every error message or deprecation warning states: **(a)** what failed, **(b)** why it failed, and **(c)** the exact command or link to fix it. | Blaming the user (*"Illegal input"*) or returning opaque error codes without remediation. |
| **3. Quantified & Honest** | State concrete numbers (`"Reduces cold-start latency by 40% on Node 22"`) and openly document known limitations. | Unverifiable superlatives (*"blazingly fast"*, *"infinite scale"*, *"zero overhead"*). |

---

## 2. Banned Words & Preferred Replacements

Never use the terms in the left column in any documentation, release note, or UI string:

| ❌ Banned Term / Phrase | ✅ Preferred Replacement |
| :--- | :--- |
| *"Simply" / "Just" / "Obviously" / "Easily"* | Omit completely—what seems "simple" is frustrating when a user is debugging an error at 2 AM. |
| *"Seamless" / "Seamlessly"* | State the actual integration mechanism (*"Authenticates via OIDC without static keys"*). |
| *"Blazingly fast" / "Lightning-fast"* | State the measured latency or complexity (*"Completes in <15ms p99"*). |
| *"Leverage" / "Utilize"* | *"Use"* |
| *"In order to"* | *"To"* |
| *"Please note that..."* | Use a `> [!NOTE]` callout or state the fact directly. |

---

## 3. Product & Technical Capitalization Rules

- **Google Antigravity** on first mention; **Antigravity** thereafter.
- **Antigravity CLI** or **`agy`** (always lowercase in backticks when referring to the binary).
- **`GEMINI.md`** and **`AGENTS.md`** (always uppercase filename in backticks).
- **Skill** / **Rules** / **Subagents** / **MCP Server** (capitalize when referring to the named Antigravity customization tab; lowercase in general prose).

---

## 4. Before / After Copy Calibration

### CLI / API Error Message
- ❌ **Before**: `Error 403: Invalid token scope.`
- ✅ **After**: `403 Forbidden: Your API key is missing the 'orders:write' scope required by 'POST /v1/orders'. Generate a scoped key at https://console.example.com/settings/keys or run 'acme auth refresh --scope orders:write'.`

### Changelog / Release Note Entry
- ❌ **Before**: `We are thrilled to announce a seamless new way to share rules across repositories!`
- ✅ **After**: **Cross-repository rule inheritance (`.agents/rules.json`)**: Share `.agents/rules/*.md` files across multiple repositories using `"inherits"` and `"entries"` in `.agents/rules.json`, with per-path `"include_only"` and `"exclude"` filters.

---

## 5. Verification Checklist
Before returning final copy:
- [ ] Zero occurrences of *"simply"*, *"just"*, *"seamless"*, *"blazingly"*, or *"leverage"*.
- [ ] All sentences in procedural steps use active voice and imperative verbs (*"Run..."*, *"Add..."*, *"Verify..."*).
- [ ] Every CLI flag, file path, environment variable, and HTTP status code is wrapped in backticks.
