---
name: blog-draft
description: >-
  Draft high-signal technical blog posts, engineering deep-dives, and architecture articles
  with concrete benchmarks, Mermaid diagrams, and runnable code snippets. Use when the user
  asks to write a blog post, technical article, or engineering postmortem, or runs /blog-draft.
---

# Technical Blog Post Drafter (`blog-draft`)

Use this skill to research, outline, and draft engineering blog posts that read like authentic, high-signal practitioner articles rather than generic AI-generated marketing prose.

## Contrastive Few-Shot Examples (Stage 3 Progressive Disclosure)

Before writing the first draft, **always read both example files** to calibrate tone, pacing, and specificity:
- ✅ **Target Quality**: [`examples/good-post.md`](./examples/good-post.md) — Leads with a concrete production metric, shows real stack traces/code, includes a Mermaid architecture diagram, and explains trade-offs candidly.
- ❌ **Anti-Pattern to Avoid**: [`examples/bad-post.md`](./examples/bad-post.md) — Opens with hollow throat-clearing (*"In today's fast-paced digital landscape..."*), uses vague buzzwords without numbers, and lacks runnable code.

---

## Step-by-Step Drafting Workflow

### Step 1: Clarify Angle, Audience & Hard Evidence
Identify from the user's prompt (or ask 2–3 brief questions if missing):
1. **Core Thesis & Hook**: What specific engineering problem failed, how much did the fix improve things (e.g., p99 latency, memory, build time), and what was the non-obvious lesson?
2. **Target Reader**: Staff/Senior engineers, framework users, or technical decision-makers?
3. **Source Material**: Inspect any referenced commits, PRs, benchmarks, or codebase modules so every code snippet and metric in the post is grounded in reality.

### Step 2: Propose a Structured Outline
Present a concise outline for approval before drafting full prose:
1. **Title Options (3 variants)**: Specific, metric- or mechanism-driven titles (e.g., *"How We Cut p99 Checkout Latency by 78% by Eliminating Hidden N+1 Serialization"*).
2. **The Hook (Paragraph 1)**: Drop the reader directly into the production symptom, benchmark chart, or architectural bottleneck.
3. **Root Cause Investigation**: What we measured, the hypotheses we ruled out, and the culprit code.
4. **The Architecture Fix (with Mermaid Diagram)**: Before/after design and runnable implementation snippet.
5. **Trade-Offs, Benchmarks & Takeaways**: Honest discussion of where this approach does *not* work and final metrics table.

### Step 3: Write the Draft (Enforcing Quality Invariants)
Read [`examples/good-post.md`](./examples/good-post.md) and [`examples/bad-post.md`](./examples/bad-post.md), then write the full post adhering to these rules:
- **Ban Hollow Openers**: Never start with *"In the ever-evolving world of software..."* or *"As engineers, we all know..."*. Start with a concrete incident, metric, or code snippet.
- **Show, Don't Tell**: Every major section must include either a real code block, a benchmark table, or a valid **Mermaid diagram** (with special-character node labels properly quoted).
- **Cite Every Number**: State exact hardware/workload parameters alongside every latency or throughput figure.

### Step 4: Self-Audit & Polish
Verify the draft against [`examples/bad-post.md`](./examples/bad-post.md) to eliminate filler adjectives (*"seamless"*, *"revolutionary"*, *"game-changing"*) and ensure every sentence adds technical signal.
