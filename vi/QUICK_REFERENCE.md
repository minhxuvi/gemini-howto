# Google Antigravity & Gemini: Bảng Tham Khảo Nhanh (Quick Reference)

[English](../QUICK_REFERENCE.md) | **Tiếng Việt**

Tài liệu tra cứu nhanh trên một trang bao gồm toàn bộ các lệnh slash, đường dẫn file, cấu trúc YAML frontmatter, hợp đồng JSON của hook, cú pháp phân quyền, cờ CLI và đoạn mã mẫu Python SDK trong **Google Antigravity** (App v2.24+, CLI `agy` v1.4+, Python SDK `google-antigravity` v0.1.22+).

---

## 1. Vị Trí File & Phân Cấp Khám Phá (Discovery Hierarchy)

| Thành Phần Tùy Biến | Đường Dẫn Workspace (Cấp Dự Án) | Đường Dẫn Global (Cấp Người Dùng) | File Quản Lý Đa Dự Án |
| :--- | :--- | :--- | :--- |
| **Chỉ Dẫn Luôn Bật (Always-On)** | `./GEMINI.md`, `./AGENTS.md` (và các thư mục con) | `~/.gemini/GEMINI.md`, `~/.gemini/AGENTS.md`, `~/.gemini/config/GEMINI.md` | Nhúng qua `@[label](path)` |
| **Quy Tắc Mô-Đun (Scoped Rules)** | `.agents/rules/*.md` | `~/.gemini/config/rules/*.md` | `.agents/rules.json` |
| **Skills & `/commands`** | `.agents/skills/<name>/SKILL.md` | `~/.gemini/config/skills/<name>/SKILL.md` | `.agents/skills.json` |
| **Subagents** | `.agents/agents/<name>.md` | `~/.gemini/config/agents/<name>.md` | Đóng gói qua Plugins |
| **MCP Servers** | `<plugin-root>/mcp_config.json` | `~/.gemini/config/mcp_config.json` | Đóng gói qua Plugins |
| **Lifecycle Hooks** | `.agents/hooks.json` | `~/.gemini/config/hooks.json` | `<plugin-root>/hooks.json` |
| **Native Plugins** | `.agents/plugins/<name>/plugin.json` | `~/.gemini/config/plugins/<name>/plugin.json` | `.agents/plugins.json` |
| **Sidecars & Automations** | `<plugin-root>/sidecars/<id>/sidecar.json` | `~/.gemini/config/sidecars/<id>/sidecar.json` | Quản lý qua `/schedule` |
| **Cài Đặt & Phím Tắt CLI** | `.agents/settings.json` | `~/.gemini/antigravity-cli/settings.json`, `keybindings.json` | — |

---

## 2. Các Lệnh Slash Tích Hợp Sẵn (`01-slash-commands/`)

### Chế Độ Tự Hành & Đa Tác Nhân
| Lệnh | Mục Đích |
| :--- | :--- |
| `/boost <task>` | Khởi chạy suy luận sâu 3 giai đoạn (`Orchestrator` → các worktree `DeepCoder`/`DeepInvestigator` song song → kiểm thử đa vòng) |
| `/teamwork-preview <task>` | Khởi chạy đội ngũ đa tác nhân 2 giai đoạn (`Scoping Interview` → các tác nhân tự hành `Sentinel`, `Explorers`, `Workers`, `Critic`, `Challenger`, `Auditor`) |
| `/goal <objective>` | Chạy liên tục cho đến khi hoàn thành mục tiêu và vượt qua mọi bài kiểm tra xác thực |
| `/plan [task]` | Vào chế độ Lập kế hoạch và tạo artifact **Implementation Plan** để người dùng duyệt |
| `/grill-me` | Thực hiện cuộc phỏng vấn kiến trúc tương tác nhằm làm rõ mọi điểm mơ hồ trước khi viết code |
| `/browser <task>` | Ủy quyền việc duyệt web, kiểm thử giao diện hoặc trích xuất dữ liệu cho subagent trình duyệt trong sandbox |
| `/schedule <when> <task>` | Tạo lịch định kỳ cron hoặc tác vụ tự động chạy nền một lần (`sidecar.json`) |

### Quản Lý Phiên, Ngữ Cảnh & Checkpoints
| Lệnh | Bí Danh (Aliases) | Mục Đích |
| :--- | :--- | :--- |
| `/rewind` | `/undo` | Hoàn tác hội thoại và/hoặc các file trong workspace về một checkpoint trước đó |
| `/fork` | `/branch` | Nhân bản cuộc hội thoại hiện tại tại thời điểm này thành một phiên song song độc lập |
| `/btw <question>` | — | Hỏi nhanh một câu hỏi phụ trong lớp phủ tạm thời mà không làm bẩn lịch sử hội thoại chính |
| `/compact` | — | Tóm tắt lịch sử hội thoại để giải phóng dung lượng token trong cửa sổ ngữ cảnh |
| `/context` | — | Kiểm tra chi tiết lượng token đang dùng cho rules, skills, MCP tools và lịch sử chat |
| `/diff` | — | Xem các thay đổi git chưa commit và diff của các file trong lượt hiện tại |
| `/resume` | `/switch`, `/conversation` | Chuyển sang hoặc tiếp tục một luồng hội thoại trước đó |
| `/clear` | `/new` | Bắt đầu một phiên hội thoại hoàn toàn mới |
| `/copy [n\|btw]` | — | Sao chép câu trả lời mới nhất của agent, câu trả lời thứ *n*, hoặc kết quả `/btw` vừa hỏi |

### Quản Lý Tùy Biến, Mô Hình & Cấu Hình
| Lệnh | Bí Danh (Aliases) | Mục Đích |
| :--- | :--- | :--- |
| `/learn [instruction]` | — | Đúc kết các chỉnh sửa trong phiên thành một rule hoặc skill lâu dài qua `learning_proposal.md` |
| `/skills` | — | Liệt kê và kiểm tra toàn bộ các skill cấp workspace, global và plugin |
| `/agents` | — | Mở trình quản lý Subagents trực tiếp (xem trạng thái, nhảy tới yêu cầu duyệt quyền, dừng tác nhân) |
| `/mcp` | — | Kiểm tra các MCP server, xem danh sách công cụ, **Restart** hoặc chạy **Fix with Agent** |
| `/hooks` | — | Xem các lifecycle hook đã đăng ký ở cấp workspace, global và plugin |
| `/plugin` | `/plugins` | Mở trình quản lý plugin tương tác (cài đặt, bật, tắt, gỡ bỏ) |
| `/model` | — | Chuyển đổi mô hình đang hoạt động (`gemini-4-argon`, `gemini-3.8-flash`, `gemini-3.1-pro`...) |
| `/effort [level]` | — | Đặt mức độ suy luận (`low`, `medium`, `high`, `max`) |
| `/fast` | — | Bật/tắt nhanh chế độ tốc độ cao (`gemini-3.8-flash`) |
| `/permissions` | — | Xem và chỉnh sửa các quy tắc phân quyền `Allow`, `Ask` và `Deny` |
| `/remote-control [on\|off]` | — | Bật/tắt điều khiển từ xa qua trình duyệt tại `https://antigravity.google.com` |
| `/config` | `/settings` | Mở trình chỉnh sửa cài đặt tương tác |

---

## 3. Cẩm Nang Nhanh Về Rules & Memory (`02-memory/`)

### Frontmatter Quy Tắc Mô-Đun (`.agents/rules/*.md`)
```yaml
---
trigger: model_decision          # always_on | model_decision | glob | manual
description: Áp dụng khi viết hoặc review các bản migration PostgreSQL hoặc câu truy vấn SQL.
globs: "**/*.sql, db/migrations/**"  # Chỉ bắt buộc khi trigger: glob
---
```

### Nhúng File & Giới Hạn Ngân Sách
- **Nhúng trực tiếp nội dung file** (tự động lược bỏ YAML frontmatter của file đích): `@[Tiêu Chuẩn API](docs/api-standards.md)`
- **Tham chiếu con trỏ đường dẫn** (không tốn token ban đầu): `@docs/api-standards.md`
- **Giới hạn cứng**: **24 KB** (`24.000` byte) cho mỗi file quy tắc; **20.000 token** tổng ngân sách `defaultRulesBudget` cho các quy tắc `always_on`/global (các quy tắc vượt ngân sách sẽ được chuyển thành con trỏ `@path` thay vì bị bỏ sót).

---

## 4. Cẩm Nang Nhanh Về Skills (`03-skills/`)

Mỗi file `.agents/skills/<name>/SKILL.md` vừa là lệnh `/<name>` vừa tự động được kích hoạt theo ngữ nghĩa:

```yaml
---
name: code-review-specialist
description: Thực hiện review code có cấu trúc về bảo mật, hiệu năng và khả năng bảo trì. Sử dụng khi review PR, diff đã stage hoặc khi người dùng gọi /code-review-specialist.
---

# Hướng dẫn thực hiện
1. Chạy `bash scripts/check-metrics.sh` để thu thập các chỉ số độ phức tạp của bản diff.
2. Đối chiếu với `resources/checklist.md` và trình bày kết quả theo mẫu `examples/sample-review.md`.
```

---

## 5. Cẩm Nang Nhanh Về Subagents (`04-subagents/`)

### Subagent Tùy Chỉnh (`.agents/agents/secure-reviewer.md`)
```yaml
---
name: secure-reviewer
description: Tác nhân kiểm toán bảo mật ứng dụng chỉ đọc cho OWASP Top 10 và rò rỉ khóa bí mật.
tools:
  - view_file
  - grep_search
  - find_by_name
  - list_dir
  - run_command
subagent: true
mainAgent: false
model: inherit                   # inherit | flash_lite | flash | pro
commandExecutionPolicy: sandbox  # sandbox | auto | eager | off
---
```

### Các Chế Độ Cô Lập Workspace (`invoke_subagent`)
- `Workspace: "inherit"` — Dùng chung thư mục làm việc với tác nhân cha (tốt nhất cho tác vụ chỉ đọc hoặc sửa các file tách biệt).
- `Workspace: "branch"` — Tạo bản sao nhánh không gian làm việc hoàn toàn cô lập (tốt nhất khi thử nghiệm các phương án cạnh tranh song song).
- `Workspace: "share"` — Chia sẻ kho lưu trữ `.git` bên dưới theo kiểu git worktree nhưng có nhánh làm việc độc lập.

---

## 6. Cẩm Nang Nhanh Cấu Hình MCP (`05-mcp/`)

File cấu hình: `~/.gemini/config/mcp_config.json` (hoặc `<plugin-root>/mcp_config.json`)

```json
{
  "mcpServers": {
    "github": {
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": {
        "Authorization": "Bearer ${GITHUB_PERSONAL_ACCESS_TOKEN}"
      }
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "${DATABASE_URL}"]
    }
  }
}
```

---

## 7. Cẩm Nang Nhanh Lifecycle Hooks (`06-hooks/`)

File cấu hình: `.agents/hooks.json` | `~/.gemini/config/hooks.json` | `<plugin-root>/hooks.json`

| Sự Kiện | Cấu Trúc Cấu Hình | Có Thể Chặn / Sửa? | Các Trường JSON Đầu Ra Chính (stdout) |
| :--- | :--- | :---: | :--- |
| `SessionStart` | Mảng phẳng các handler | Tiêm ngữ cảnh | `{"injectSteps": [{"systemMessage": {"systemMessage": "..."}}]}` |
| `PreToolUse` | Mảng matcher (`matcher` + `hooks`) | **Có** (`deny`/`block`, `ask`, `allow`, `overwrite`) | `{"decision": "block", "reason": "...", "overwrite": {...}, "permissionOverrides": [...]}` |
| `PostToolUse` | Mảng matcher (`matcher` + `hooks`) | Tác vụ phụ / ghi log | `{}` |
| `PreInvocation` | Mảng phẳng các handler | Tiêm ngữ cảnh | `{"injectSteps": [{"ephemeralMessage": "..."}]}` |
| `PostInvocation` | Mảng phẳng các handler | Ép tiếp tục / dừng | `{"injectSteps": [...], "terminationBehavior": "force_continue"}` |
| `Stop` | Mảng phẳng các handler | **Có** (`continue` / `injectSteps`) | `{"decision": "continue", "reason": "Unit tests failed", "injectSteps": [...]}` |

**Payload Stdin Chung (camelCase)**: `conversationId`, `workspacePaths`, `transcriptPath`, `artifactDirectoryPath`, `modelName` (cộng thêm `toolName`, `toolInput` ở các hook công cụ; `fullyIdle`, `terminationReason` ở sự kiện `Stop`).

---

## 8. Phân Quyền & Sandbox Hệ Điều Hành (`09-advanced-features/`)

Thứ tự ưu tiên: **`Deny` > `Ask` > `Allow`**

| Cú Pháp Quy Tắc | Ý Nghĩa |
| :--- | :--- |
| `read_file(.env*)` | Khớp thao tác đọc các file `.env` (thường đặt trong `Deny`) |
| `write_file(src/**)` | Khớp thao tác ghi file bên trong thư mục `src/` |
| `command(npm test*)` | Khớp lệnh chạy `npm test` bên trong OS Sandbox |
| `command(regex:^git (status\|diff\|log))` | Khớp biểu thức chính quy cho các lệnh Git chỉ đọc an toàn |
| `unsandboxed(docker *)` | Cho phép chạy lệnh `docker` bên ngoài sandbox Seatbelt/`nsjail` |
| `read_url(docs.python.org)` | Cho phép kết nối mạng HTTP ra ngoài tới tên miền `docs.python.org` từ trong sandbox |
| `mcp(github/*)` | Khớp toàn bộ công cụ do MCP server `github` cung cấp |
| `mcp(postgres/query)` | Chỉ khớp công cụ `query` trên MCP server `postgres` |

---

## 9. Antigravity CLI (`agy`) & Python SDK (`10-cli/`)

### Các Lệnh `agy` CLI Phổ Biến
```bash
agy                                           # Khởi động giao diện TUI tương tác
agy -p "Tóm tắt các thay đổi đã stage"        # Chế độ print (headless) không tương tác
git diff | agy -p "Kiểm tra lỗi bảo mật"      # Truyền stdin vào tác nhân headless
agy --model gemini-4-argon --effort max       # Chạy với mô hình mạnh nhất & mức suy luận tối đa
agy --mode auto --sandbox -p "Sửa lỗi lint"   # Chế độ tự động bên trong OS Sandbox
agy --resume                                  # Tiếp tục phiên gần đây (-c / --continue cho phiên mới nhất)
agy plugin install pr-review@antigravity-plugins-official
agy plugin validate ./my-plugin --strict
agy remote-control start --name "workstation" # Khởi chạy daemon điều khiển từ xa
```

### Phím Tắt TUI
| Phím Tắt | Thao Tác |
| :--- | :--- |
| `Alt+M` | Chuyển đổi chế độ thực thi hoặc chế độ hàng đợi tin nhắn (`Queue` vs `Immediate Interrupt`) |
| `Ctrl+J` / `Alt+J` | Nhảy trực tiếp đến subagent chạy nền đang chờ phê duyệt quyền |
| `Ctrl+K` | Phê duyệt nhanh yêu cầu công cụ của subagent hoặc điều hướng lên |
| `Shift+Tab` | Chuyển đổi qua lại giữa các chế độ thực thi / lập kế hoạch |
| `Esc` / `Ctrl+C` | Ngắt quá trình sinh phản hồi hoặc dừng lệnh đang chạy |

### Ví Dụ Tối Thiểu Với Python SDK (`google-antigravity` v0.1.22+)
```python
from google.antigravity import Agent, GeminiModelOptions, LocalAgentConfig

agent = Agent(
    model="gemini-4-argon",
    config=LocalAgentConfig(workspace_dir="."),
    model_options=GeminiModelOptions(max_output_tokens=16384),
)

for chunk in agent.stream("Kiểm tra module xác thực và chạy pytest"):
    if chunk.thoughts:
        print(f"[Suy luận] {chunk.thoughts}")
    if chunk.text:
        print(chunk.text, end="", flush=True)
```
