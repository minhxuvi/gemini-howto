# Danh Mục Toàn Bộ Template & Thành Phần Mẫu (Catalog)

[English](../CATALOG.md) | **Tiếng Việt**

> Danh mục tổng hợp toàn bộ các template lệnh slash, quy tắc bộ nhớ, agent skills, subagents, cấu hình MCP, lifecycle hooks, native plugins và kịch bản SDK có sẵn trong repository `gemini-howto`, kèm lệnh sao chép nhanh.

**Điều hướng nhanh**: [01. Slash Commands](#01-slash-commands-lệnh-tắt-dựa-trên-skill) | [02. Rules & Memory](#02-rules--memory-bộ-nhớ--quy-tắc) | [03. Agent Skills](#03-agent-skills-kỹ-năng-tác-nhân) | [04. Subagents](#04-subagents-tác-nhân-con-chuyên-biệt) | [05. MCP Configs](#05-mcp-configs-kết-nối-dữ-liệu-ngoài) | [06. Lifecycle Hooks](#06-lifecycle-hooks-tự-động-hóa-sự-kiện) | [07. Native Plugins](#07-native-plugins-gói-mở-rộng) | [08. Checkpoints & Sidecars](#08-checkpoints-artifacts--sidecars) | [09. Advanced Features](#09-tính-năng-nâng-cao--bảo-mật) | [10. CLI & Python SDK](#10-cli--python-sdk)

---

## Tóm Tắt Tổng Quan

| Phân Loại | Số Lượng Tích Hợp Sẵn | Số Template Mẫu Trong Repo | Đường Dẫn Module |
| :--- | :---: | :---: | :--- |
| **01. Slash Commands** | 35+ lệnh tích hợp | 8 lệnh mẫu | [01-slash-commands/](01-slash-commands/README.md) |
| **02. Rules & Memory** | 4 chế độ `trigger` | 6 file mẫu (`GEMINI.md`, `AGENTS.md`, `rules/`) | [02-memory/](02-memory/README.md) |
| **03. Agent Skills** | 2 skill học tập tương tác | 6 gói skill đa file | [03-skills/](03-skills/README.md) |
| **04. Subagents** | 4 (`research`, `browser`, `self`, `image-generator`) | 9 subagent chuyên gia | [04-subagents/](04-subagents/README.md) |
| **05. Giao Thức MCP** | Stdio & Streamable HTTP | 4 cấu hình `mcp_config.json` | [05-mcp/](05-mcp/README.md) |
| **06. Lifecycle Hooks** | 6 sự kiện vòng đời | 9 script + `hooks.json` | [06-hooks/](06-hooks/README.md) |
| **07. Native Plugins** | Quản lý qua `agy plugin` | 3 gói plugin hoàn chỉnh | [07-plugins/](07-plugins/README.md) |
| **08. Checkpoints & UI** | `/rewind`, `/fork`, `<agent-embed>`, `sidecar.json` | Mẫu kế hoạch, widget UI & sidecar | [08-checkpoints/](08-checkpoints/README.md) |
| **09. Advanced Features** | `/boost`, `/teamwork-preview`, OS Sandbox | Cấu hình quyền & kịch bản điều phối | [09-advanced-features/](09-advanced-features/README.md) |
| **10. CLI & Python SDK** | `agy` CLI & `google-antigravity` SDK | Kịch bản CI/CD & workflow Python | [10-cli/](10-cli/README.md) |

---

## 01. Slash Commands (Lệnh Tắt Dựa Trên Skill)

Trong Google Antigravity, mỗi lệnh tùy chỉnh được cài đặt dưới dạng một skill tại `.agents/skills/<name>/SKILL.md` (cấp dự án) hoặc `~/.gemini/config/skills/<name>/SKILL.md` (cấp người dùng).

| Lệnh | File Nguồn | Công Dụng Chính | Lệnh Sao Chép Nhanh |
| :--- | :--- | :--- | :--- |
| `/optimize` | [`../01-slash-commands/optimize.md`](../01-slash-commands/optimize.md) | Phân tích điểm nghẽn hiệu năng, độ phức tạp thuật toán và truy vấn N+1 | `mkdir -p .agents/skills/optimize && cp ../01-slash-commands/optimize.md .agents/skills/optimize/SKILL.md` |
| `/pr` | [`../01-slash-commands/pr.md`](../01-slash-commands/pr.md) | Phân tích nhánh hiện tại và tạo mô tả Pull Request chuẩn chỉnh | `mkdir -p .agents/skills/pr && cp ../01-slash-commands/pr.md .agents/skills/pr/SKILL.md` |
| `/commit` | [`../01-slash-commands/commit.md`](../01-slash-commands/commit.md) | Tạo thông điệp commit chuẩn Conventional Commits từ các file đã stage | `mkdir -p .agents/skills/commit && cp ../01-slash-commands/commit.md .agents/skills/commit/SKILL.md` |
| `/push-all` | [`../01-slash-commands/push-all.md`](../01-slash-commands/push-all.md) | Kiểm tra an toàn, chạy lint/test nhanh, commit và đẩy code lên nhánh từ xa | `mkdir -p .agents/skills/push-all && cp ../01-slash-commands/push-all.md .agents/skills/push-all/SKILL.md` |
| `/generate-api-docs` | [`../01-slash-commands/generate-api-docs.md`](../01-slash-commands/generate-api-docs.md) | Trích xuất route/schema và sinh tài liệu OpenAPI / Markdown | `mkdir -p .agents/skills/generate-api-docs && cp ../01-slash-commands/generate-api-docs.md .agents/skills/generate-api-docs/SKILL.md` |
| `/doc-refactor` | [`../01-slash-commands/doc-refactor.md`](../01-slash-commands/doc-refactor.md) | Làm sạch, chuẩn hóa cấu trúc và bổ sung sơ đồ Mermaid cho tài liệu | `mkdir -p .agents/skills/doc-refactor && cp ../01-slash-commands/doc-refactor.md .agents/skills/doc-refactor/SKILL.md` |
| `/setup-ci-cd` | [`../01-slash-commands/setup-ci-cd.md`](../01-slash-commands/setup-ci-cd.md) | Thiết lập đường ống GitHub Actions / Cloud Build tích hợp kiểm thử | `mkdir -p .agents/skills/setup-ci-cd && cp ../01-slash-commands/setup-ci-cd.md .agents/skills/setup-ci-cd/SKILL.md` |
| `/unit-test-expand` | [`../01-slash-commands/unit-test-expand.md`](../01-slash-commands/unit-test-expand.md) | Phát hiện các nhánh logic chưa có test và viết unit test bao phủ | `mkdir -p .agents/skills/unit-test-expand && cp ../01-slash-commands/unit-test-expand.md .agents/skills/unit-test-expand/SKILL.md` |

---

## 02. Rules & Memory (Bộ Nhớ & Quy Tắc)

| Template | File Nguồn | Phạm Vi & Cơ Chế Kích Hoạt | Lệnh Sao Chép Nhanh |
| :--- | :--- | :--- | :--- |
| **Bộ Nhớ Dự Án (`GEMINI.md`)** | [`../02-memory/project-GEMINI.md`](../02-memory/project-GEMINI.md) | Toàn bộ workspace (`always_on`) | `cp ../02-memory/project-GEMINI.md ./GEMINI.md` |
| **Bộ Nhớ Cá Nhân** | [`../02-memory/personal-GEMINI.md`](../02-memory/personal-GEMINI.md) | Toàn cục cho người dùng (`~/.gemini/GEMINI.md`) | `cp ../02-memory/personal-GEMINI.md ~/.gemini/GEMINI.md` |
| **Bộ Nhớ Cấp Thư Mục (`AGENTS.md`)** | [`../02-memory/directory-api-AGENTS.md`](../02-memory/directory-api-AGENTS.md) | Tự động nạp khi làm việc trong thư mục `src/api/` | `cp ../02-memory/directory-api-AGENTS.md ./src/api/AGENTS.md` |
| **Quy Tắc Mô-Đun (`.agents/rules/`)** | `../02-memory/rules/*.md` | Hỗ trợ `always_on`, `model_decision`, `glob`, `manual` | `mkdir -p .agents/rules && cp ../02-memory/rules/*.md .agents/rules/` |

---

## 03. Agent Skills (Kỹ Năng Tác Nhân)

| Skill | Thư Mục Nguồn | Khi Nào Tự Động Kích Hoạt | Lệnh Sao Chép Nhanh |
| :--- | :--- | :--- | :--- |
| **`self-assessment`** | [`../.agents/skills/self-assessment/`](../.agents/skills/self-assessment/) | Khi gõ `/self-assessment` hoặc yêu cầu kiểm tra trình độ Antigravity | Đã tích hợp sẵn trong `.agents/skills/self-assessment/` |
| **`lesson-quiz`** | [`../.agents/skills/lesson-quiz/`](../.agents/skills/lesson-quiz/) | Khi gõ `/lesson-quiz [01-10]` để ôn tập từng bài học | Đã tích hợp sẵn trong `.agents/skills/lesson-quiz/` |
| **`code-review-specialist`** | `../03-skills/code-review-specialist/` | Khi yêu cầu review PR, kiểm tra chất lượng code hoặc bảo mật | `cp -r ../03-skills/code-review-specialist .agents/skills/` |
| **`refactor`** | `../03-skills/refactor/` | Khi yêu cầu tái cấu trúc hàm lớn, khử code smell theo chuẩn Martin Fowler | `cp -r ../03-skills/refactor .agents/skills/` |
| **`doc-generator`** | `../03-skills/doc-generator/` | Khi yêu cầu sinh tài liệu kỹ thuật hoặc API từ mã nguồn | `cp -r ../03-skills/doc-generator .agents/skills/` |
| **`brand-voice`** | `../03-skills/brand-voice/` | Khi soạn thảo thông cáo, nội dung sản phẩm hoặc email chuẩn giọng điệu thương hiệu | `cp -r ../03-skills/brand-voice .agents/skills/` |
| **`blog-draft`** | `../03-skills/blog-draft/` | Khi viết bài blog kỹ thuật có dàn ý và ví dụ minh họa | `cp -r ../03-skills/blog-draft .agents/skills/` |
| **`gemini-md`** | `../03-skills/gemini-md/` | Khi khởi tạo hoặc tối ưu hóa ngân sách token cho `GEMINI.md` và `.agents/rules/` | `cp -r ../03-skills/gemini-md .agents/skills/` |

---

## 04. Subagents (Tác Nhân Con Chuyên Biệt)

| Subagent | File Nguồn | Quyền Công Cụ & Chế Độ | Lệnh Sao Chép Nhanh |
| :--- | :--- | :--- | :--- |
| **`code-reviewer`** | [`../04-subagents/code-reviewer.md`](../04-subagents/code-reviewer.md) | Chỉ đọc + chạy linter trong sandbox | `cp ../04-subagents/code-reviewer.md .agents/agents/` |
| **`secure-reviewer`** | [`../04-subagents/secure-reviewer.md`](../04-subagents/secure-reviewer.md) | Kiểm toán bảo mật chỉ đọc (OWASP Top 10, rò rỉ khóa) | `cp ../04-subagents/secure-reviewer.md .agents/agents/` |
| **`clean-code-reviewer`** | [`../04-subagents/clean-code-reviewer.md`](../04-subagents/clean-code-reviewer.md) | Đánh giá nguyên lý SOLID, DRY, đặt tên và độ phức tạp | `cp ../04-subagents/clean-code-reviewer.md .agents/agents/` |
| **`test-engineer`** | [`../04-subagents/test-engineer.md`](../04-subagents/test-engineer.md) | Đọc/ghi file test và chạy bộ kiểm thử tự động | `cp ../04-subagents/test-engineer.md .agents/agents/` |
| **`debugger`** | [`../04-subagents/debugger.md`](../04-subagents/debugger.md) | Điều tra nguyên nhân gốc rễ (RCA), tái hiện lỗi và khoanh vùng bug | `cp ../04-subagents/debugger.md .agents/agents/` |
| **`performance-optimizer`** | [`../04-subagents/performance-optimizer.md`](../04-subagents/performance-optimizer.md) | Phân tích độ trễ, bộ nhớ và đề xuất tối ưu hóa | `cp ../04-subagents/performance-optimizer.md .agents/agents/` |
| **`documentation-writer`** | [`../04-subagents/documentation-writer.md`](../04-subagents/documentation-writer.md) | Viết và cập nhật tài liệu hướng dẫn, kiến trúc, API | `cp ../04-subagents/documentation-writer.md .agents/agents/` |
| **`implementation-agent`** | [`../04-subagents/implementation-agent.md`](../04-subagents/implementation-agent.md) | Triển khai tính năng đầu-cuối trong worktree cô lập (`branch`/`share`) | `cp ../04-subagents/implementation-agent.md .agents/agents/` |
| **`data-scientist`** | [`../04-subagents/data-scientist.md`](../04-subagents/data-scientist.md) | Truy vấn SQL, phân tích thống kê và trực quan hóa dữ liệu | `cp ../04-subagents/data-scientist.md .agents/agents/` |

---

## 05. MCP Configs (Kết Nối Dữ Liệu Ngoài)

| Cấu Hình Mẫu | File Nguồn | Giao Thức & Dịch Vụ | Lệnh Sao Chép Nhanh |
| :--- | :--- | :--- | :--- |
| **GitHub MCP** | `../05-mcp/github-mcp.json` | Streamable HTTP (`${GITHUB_PERSONAL_ACCESS_TOKEN}`) | `cp ../05-mcp/github-mcp.json ~/.gemini/config/mcp_config.json` |
| **Database MCP** | `../05-mcp/database-mcp.json` | Stdio PostgreSQL (`${DATABASE_URL}`) | `cp ../05-mcp/database-mcp.json ~/.gemini/config/mcp_config.json` |
| **Filesystem MCP** | `../05-mcp/filesystem-mcp.json` | Stdio truy cập thư mục cục bộ được cấp phép | `cp ../05-mcp/filesystem-mcp.json ~/.gemini/config/mcp_config.json` |
| **Multi-Server MCP** | `../05-mcp/multi-mcp.json` | Kết hợp GitHub + PostgreSQL + Sentry/Slack | `cp ../05-mcp/multi-mcp.json ~/.gemini/config/mcp_config.json` |

---

## 06. Lifecycle Hooks (Tự Động Hóa Sự Kiện)

| File / Script | Sự Kiện Vòng Đời | Chức Năng |
| :--- | :--- | :--- |
| `../06-hooks/hooks.json` | Tất cả 6 sự kiện | File cấu hình `.agents/hooks.json` mẫu kết nối các script bên dưới |
| `../06-hooks/security-scan.sh` | `PreToolUse` | Quét nội dung file hoặc lệnh shell để chặn rò rỉ API key/token (`decision: "block"`) |
| `../06-hooks/validate-prompt.sh` | `PreInvocation` | Kiểm tra và bổ sung ngữ cảnh trước khi gửi lượt gọi tới mô hình |
| `../06-hooks/format-code.sh` | `PostToolUse` | Tự động chạy `ruff` / `prettier` ngay sau khi agent ghi hoặc sửa file |
| `../06-hooks/log-bash.sh` | `PostToolUse` | Ghi nhật ký kiểm toán mọi lệnh `run_command` đã thực thi |
| `../06-hooks/pre-commit.sh` | `PreToolUse` | Chạy kiểm tra chất lượng trước khi cho phép thực thi `git commit` |
| `../06-hooks/dependency-check.sh` | `PreToolUse` | Kiểm tra tính an toàn của gói thư viện trước khi chạy `npm install` / `pip install` |
| `../06-hooks/context-tracker.py` | `PostInvocation` | Theo dõi mức tiêu thụ token và trạng thái phiên làm việc |
| `../06-hooks/notify-team.sh` | `Stop` | Kiểm tra `fullyIdle: true`, ép chạy test (`injectSteps`) hoặc gửi thông báo khi hoàn tất |

---

## 07. Native Plugins (Gói Mở Rộng)

| Plugin | Thư Mục Nguồn | Thành Phần Đóng Gói | Lệnh Kiểm Định & Cài Đặt |
| :--- | :--- | :--- | :--- |
| **`pr-review`** | [`../07-plugins/pr-review/`](../07-plugins/pr-review/) | `plugin.json`, `hooks.json`, `skills/`, `agents/`, `rules/` | `agy plugin validate ../07-plugins/pr-review --strict` |
| **`devops-automation`** | [`../07-plugins/devops-automation/`](../07-plugins/devops-automation/) | `plugin.json`, `hooks.json`, `mcp_config.json`, `skills/`, `agents/`, `rules/` | `agy plugin validate ../07-plugins/devops-automation --strict` |
| **`documentation`** | [`../07-plugins/documentation/`](../07-plugins/documentation/) | `plugin.json`, `skills/`, `agents/`, `rules/` | `agy plugin validate ../07-plugins/documentation --strict` |

---

## 08. Checkpoints, Artifacts & Sidecars

- **Hướng dẫn & Mẫu thực hành**: [`08-checkpoints/README.md`](08-checkpoints/README.md) (và [`../08-checkpoints/`](../08-checkpoints/))
- Bao gồm kịch bản hoàn tác `/rewind` (`/undo`), phân nhánh `/fork` (`/branch`), mẫu bình luận trực tiếp trên Implementation Plan, mẫu widget HTML `<agent-embed>` dùng `tailwindcss.min.js` và cấu hình `sidecar.json` kèm lịch `CRON_TZ`.

---

## 09. Tính Năng Nâng Cao & Bảo Mật

- **Hướng dẫn & Mẫu cấu hình**: [`09-advanced-features/README.md`](09-advanced-features/README.md) (và [`../09-advanced-features/`](../09-advanced-features/))
- Bao gồm các mẫu prompt chiến lược cho `/boost` (3 giai đoạn), `/teamwork-preview` (2 giai đoạn với `Sentinel`, `Critic`, `Challenger`, `Auditor`), cấu hình phân quyền `Deny > Ask > Allow` với biểu thức chính quy `regex:` và cấu hình OS Sandbox (Seatbelt / `nsjail`).

---

## 10. CLI & Python SDK

- **Hướng dẫn & Kịch bản mẫu**: [`10-cli/README.md`](10-cli/README.md) (và [`../10-cli/`](../10-cli/))
- Bao gồm các đường ống CI/CD dùng `agy -p --mode auto --output-format json`, bảng phím tắt TUI (`alt+m`, `Ctrl+J`/`Ctrl+K`) và các ví dụ Python SDK `google-antigravity` (`Agent`, `@beta.workflows.define`, `LiteRTAgentConfig`).
