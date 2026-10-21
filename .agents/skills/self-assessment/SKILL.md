---
name: self-assessment
description: Run an interactive 10-question assessment to evaluate your Google Antigravity and Gemini proficiency and receive a personalized learning roadmap across Modules 01-10. Trigger when the user types /self-assessment or asks to test their level or find where to start.
---

# Google Antigravity & Gemini — Interactive Self-Assessment

Evaluates a developer's proficiency across all 10 modules of the **Google Antigravity & Gemini How-To Guide** (`01-slash-commands` through `10-cli`), scores their current tier (**Beginner**, **Intermediate**, or **Advanced**), identifies specific knowledge gaps, and generates a personalized study roadmap.

---

## Reference Files

Before starting the assessment, read the bundled reference files in this skill directory:
1. `references/question-bank.md` — Contains 20+ multiple-choice questions (at least 2 per module across Modules 01–10).
2. `references/scoring-and-paths.md` — Contains the scoring rubric, mastery table templates, and persona-based learning paths (**Newcomer**, **Everyday Developer**, **Systems Architect**, **SDK & Platform Engineer**).

---

## Execution Protocol

### Step 1: Select Persona & Prepare the 10-Question Assessment

1. Read `references/question-bank.md` and `references/scoring-and-paths.md`.
2. Select **1 question from each of the 10 modules** (`01` through `10`) from `references/question-bank.md` so all 10 modules are tested in a 10-question sequence.
   - Vary between Variant A and Variant B across runs so retakes stay fresh.
3. Optionally ask the user which learning persona best describes their goal using `ask_question` (or infer from conversation if they already stated it):
   - **Newcomer** — Getting productive with core daily workflows in Antigravity IDE & `agy` CLI
   - **Everyday Developer** — Automating coding, memory rules, skills, and subagent delegation
   - **Systems Architect** — Multi-agent orchestration (`/boost`, `/teamwork-preview`), MCP, hooks, and team plugins
   - **SDK & Platform Engineer** — Headless `agy -p` CI/CD pipelines, Python SDK (`google-antigravity`), and on-device LiteRT

---

### Step 2: Run the 10 Questions One at a Time (`ask_question`)

Present **10 questions sequentially — one question per `ask_question` tool call**:

- **Tool**: Always use Antigravity's native `ask_question` tool (`is_multi_select: false`).
- **4 Options per Question**: Provide the 4 multiple-choice options from `references/question-bank.md`.
- **Shuffle Option Order**: Randomize the order of the 4 options before calling `ask_question` so the correct answer is not always in the same position. Track which option holds the correct answer.
- **No Spoilers Before Answering**:
  - Do **NOT** prefix any option with `(Recommended)` or hint at the right answer.
  - Do **NOT** reveal the answer or explanation before the user submits their choice.
  - Keep the question prompt clean: e.g., `"Question 3/10 (Module 03 — Skills): <question text>"`.

---

### Step 3: Score the Assessment

After the user completes all 10 questions, calculate their total score out of 10 and per-module breakdown:

| Score Range | Tier | Summary |
| :--- | :--- | :--- |
| **0 – 3 / 10** | **Level 1: Beginner** | Building foundational mental models of Antigravity IDE, `GEMINI.md`, and slash commands |
| **4 – 7 / 10** | **Level 2: Intermediate** | Comfortable with core workflows; ready to master event hooks, MCP, subagent workspaces, and plugins |
| **8 – 10 / 10** | **Level 3: Advanced** | Power user ready for `/boost`, `/teamwork-preview`, sandbox security, headless CI/CD, and the Python SDK |

---

### Step 4: Present Detailed Results & Tailored Study Plan

Output a structured Markdown report containing:

1. **Overall Score & Tier Badge**:
   - Total score (`N / 10`), assigned tier (**Beginner**, **Intermediate**, or **Advanced**), and a concise summary of strengths.
2. **Module-by-Module Breakdown Table**:
   - List all 10 modules (`01` to `10`), the user's answer, whether it was ✅ Correct or ❌ Missed, and a 1-sentence explanation for any missed question.
3. **Tailored Learning Roadmap**:
   - Use the rubric in `references/scoring-and-paths.md` to generate a prioritized study plan.
   - Skip modules the user answered 100% confident on (or mark them as "Optional Skim") and prioritize missed modules in dependency order.
   - Provide clickable links to each recommended module directory (e.g., `[01-slash-commands](../../01-slash-commands/README.md)`, `[02-memory](../../02-memory/README.md)`, etc.) and suggest running `/lesson-quiz <module>` after reading each module.

---

### Step 5: Follow-Up Prompt

Use `ask_question` at the end of the report to offer next steps:
- **Start first recommended module** — Walk me through the top priority module in my study plan right now
- **Review missed questions in depth** — Explain the concepts behind the questions I missed with code examples
- **Take a module quiz (`/lesson-quiz`)** — Jump straight into a 5-question deep-dive quiz on a specific module
- **Retake `/self-assessment` with alternate questions** — Run a fresh 10-question set from the bank
