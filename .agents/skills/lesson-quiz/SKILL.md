---
name: lesson-quiz
description: Interactive 5-question quiz for any specific module (01 through 10) of the gemini-howto curriculum. Trigger when the user types /lesson-quiz [module] or asks to be quizzed on a module they just read.
---

# Google Antigravity & Gemini — Module Lesson Quiz (`/lesson-quiz`)

Runs an interactive **5-question scenario-based quiz** for any single module (`01` through `10`) of the `gemini-howto` curriculum using Antigravity's `ask_question` tool, then scores the learner's performance and explains every answer in detail.

---

## Reference File

All 50 scenario-based questions (5 per module across Modules `01` through `10`) live in:
- `references/question-bank.md`

Always read `references/question-bank.md` before asking any questions. Never invent questions outside the bank.

---

## Execution Protocol

### Step 1: Resolve the Target Module (`01`–`10`)

Map the user's argument (e.g., `/lesson-quiz 06`, `/lesson-quiz hooks`, `/lesson-quiz mcp`) to the corresponding module:

| Argument / Alias | Target Module |
| :--- | :--- |
| `01`, `1`, `slash-commands`, `commands` | **Module 01: Slash Commands** (`01-slash-commands`) |
| `02`, `2`, `memory`, `rules`, `gemini-md` | **Module 02: Memory & Rules** (`02-memory`) |
| `03`, `3`, `skills`, `skill` | **Module 03: Skills** (`03-skills`) |
| `04`, `4`, `subagents`, `agents` | **Module 04: Subagents** (`04-subagents`) |
| `05`, `5`, `mcp` | **Module 05: MCP (Model Context Protocol)** (`05-mcp`) |
| `06`, `6`, `hooks`, `hook` | **Module 06: Hooks** (`06-hooks`) |
| `07`, `7`, `plugins`, `plugin` | **Module 07: Plugins** (`07-plugins`) |
| `08`, `8`, `checkpoints`, `ui`, `sidecars`, `schedule` | **Module 08: Checkpoints, Generative UI & Sidecars** (`08-checkpoints`) |
| `09`, `9`, `advanced`, `advanced-features`, `boost`, `teamwork` | **Module 09: Advanced Features** (`09-advanced-features`) |
| `10`, `cli`, `sdk`, `python-sdk` | **Module 10: CLI & Python SDK** (`10-cli`) |

If the user did not specify a module (e.g., typed `/lesson-quiz` with no argument), call `ask_question` to let them pick which module they want to be quizzed on.

---

### Step 2: Run the 5 Questions Sequentially via `ask_question`

Retrieve the 5 questions for the chosen module from `references/question-bank.md` and present them **one question at a time** using `ask_question` (`is_multi_select: false`):

1. **4 Options per Question**: Present all 4 choices from the question bank.
2. **Shuffle Option Order**: Randomize the order of the 4 options for each question so the correct answer is not always first. Record which option index holds the correct answer.
3. **No Spoilers During the Quiz**:
   - Do **NOT** mark any option with `(Recommended)`.
   - Do **NOT** reveal whether an answer was right or wrong until all 5 questions for the module have been answered (or if the user explicitly asks to stop early).
   - Format the prompt clearly: e.g., `"Module 06 (Hooks) — Question 2/5: <scenario question>"`.

---

### Step 3: Score & Explain Every Answer at the End

Once all 5 questions are answered, calculate the score (`N / 5`) and present a comprehensive review report:

| Score | Mastery Rating | Recommendation |
| :---: | :--- | :--- |
| **5 / 5** | 🏆 **Mastered** | Ready to move to the next module or build with these templates in production |
| **4 / 5** | ✅ **Proficient** | Solid grasp of core mechanics; review the 1 missed scenario below |
| **3 / 5** | 📘 **Developing** | Good foundation, but revisit the module's configuration tables and edge cases |
| **0 – 2 / 5** | 🔄 **Needs Review** | Re-read `[<module>/README.md](../../<module>/README.md)` and try the hands-on examples before retaking |

#### Required Report Sections

1. **Score Header**: `## Module XX Quiz Results: N/5 — [Mastery Rating]`
2. **Summary Table**: Question `1` through `5`, user's selected choice, correct choice, and status (`✅ Correct` or `❌ Incorrect`).
3. **Detailed Answer Explanations (All 5 Questions)**:
   - Even for questions the user got right, provide the concise architectural explanation from `references/question-bank.md` so the quiz reinforces *why* each answer works and why the distractors fail.
   - For any missed question, link directly to the relevant module tutorial (`../../<module>/README.md`).

---

### Step 4: Follow-Up Options

Call `ask_question` with 4 follow-up options:
- **Quiz the next module** — Advance to Module `XX+1`
- **Retake this module quiz** — Retry with freshly shuffled options
- **Walk through a missed scenario** — Show a concrete code/config example for a question I missed
- **Run full `/self-assessment`** — Evaluate proficiency across all 10 modules
